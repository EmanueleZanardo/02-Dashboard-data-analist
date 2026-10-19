"""Test tab544 'Collateral & garanzie reali (IFRS 7.15)': registry + funzioni pure."""

import math
import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh544_num", "mh544_str", "mh544_bool", "mh544_dir",
           "mh544_tipo", "mh544_voce", "mh544_demo", "mh544_riepilogo")

TITLE544 = "🏦📥 Collateral & garanzie reali (IFRS 7.15)"


def _v(vid="V-1", d="x", cp="cp", esp=1000.0, dr="RICEVUTA", tp="CONTANTE",
       fv=0.0, esc=True, esc2=False):
    return {"id": vid, "descrizione": d, "controparte": cp,
            "esposizione_eur": esp, "direzione": dr, "tipo": tp,
            "fair_value_garanzia": fv, "escutibile": esc, "escussa": esc2}


class TestW544Validatori:
    def test_num_ok(self):
        assert _F["mh544_num"](2, "x") == 2.0
        assert _F["mh544_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, False, "1", None, math.nan, math.inf,
                    -math.inf):
            with pytest.raises(ValueError):
                _F["mh544_num"](bad, "x")

    def test_str_ok_ko(self):
        assert _F["mh544_str"]("  abc  ", "x") == "abc"
        for bad in ("", "   ", None, 12, True):
            with pytest.raises(ValueError):
                _F["mh544_str"](bad, "x")

    def test_bool_ok_ko(self):
        assert _F["mh544_bool"](True, "x") is True
        for bad in (1, 0, "s", None):
            with pytest.raises(ValueError):
                _F["mh544_bool"](bad, "x")

    def test_dir_ok_ko(self):
        for ok in ("RICEVUTA", "DATA"):
            assert _F["mh544_dir"](ok, "x") == ok
        for bad in ("ricevuta", "", None, 1):
            with pytest.raises(ValueError):
                _F["mh544_dir"](bad, "x")

    def test_tipo_ok_ko(self):
        for ok in ("CONTANTE", "TITOLI", "LETTERA_CREDITO", "PEGNO_CREDITI",
                   "PEGNO_SCORTE", "GARANZIA_CORPORATE", "ALTRO"):
            assert _F["mh544_tipo"](ok, "x") == ok
        for bad in ("CASH", "", None):
            with pytest.raises(ValueError):
                _F["mh544_tipo"](bad, "x")


class TestW544Voce:
    def test_copertura_calcolo(self):
        o = _F["mh544_voce"](_v(esp=8500000.0, fv=8925000.0))
        assert o["copertura"] == pytest.approx(1.05)
        assert o["esito"] == "COPERTA"
        assert o["anomalie"] == []

    def test_esiti_soglie(self):
        assert _F["mh544_voce"](_v(esp=1000.0, fv=900.0))["esito"] == \
            "SOTTO_GARANZIA"
        assert _F["mh544_voce"](_v(esp=1000.0, fv=499.0))["esito"] == "CRITICA"
        assert _F["mh544_voce"](_v(esp=1000.0, fv=0.0))["esito"] == \
            "NESSUNA_COPERTURA"

    def test_garanzia_senza_esposizione_anomalia(self):
        o = _F["mh544_voce"](_v(esp=0.0, fv=500.0))
        assert o["anomalie"] == ["garanzia senza esposizione"]
        assert o["copertura"] is None
        assert o["esito"] == "COPERTA"

    def test_escussa_non_escutibile_anomalia(self):
        o = _F["mh544_voce"](_v(esp=1000.0, fv=1000.0, esc=False,
                                esc2=True))
        assert len(o["anomalie"]) == 1
        assert "non escutibile" in o["anomalie"][0]

    def test_voce_ko(self):
        with pytest.raises(ValueError):
            _F["mh544_voce"]("non-dict")
        with pytest.raises(ValueError):
            _F["mh544_voce"](_v(esp=-1.0))
        with pytest.raises(ValueError):
            _F["mh544_voce"](_v(fv=-5.0))
        with pytest.raises(ValueError):
            _F["mh544_voce"](_v(dr="ALTROVE"))
        with pytest.raises(ValueError):
            _F["mh544_voce"](_v(tp="ORO"))


class TestW544Demo:
    def test_demo_verdetto(self):
        demo = _F["mh544_demo"]()
        assert len(demo) == 3
        assert [r["id"] for r in demo] == ["COLL-DE-001", "COLL-IT-002",
                                          "COLL-UK-003"]
        ri = _F["mh544_riepilogo"](demo)
        assert ri["esposizione_tot"] == pytest.approx(12700000.0)
        assert ri["garanzia_tot"] == pytest.approx(13125000.0)
        assert ri["copertura"] == pytest.approx(13125000.0 / 12700000.0)
        assert ri["verdetto"] == "COPERTURA_ADEGUATA"
        assert ri["n_anomalie"] == 0
        assert ri["per_esito"] == {"COPERTA": 2, "SOTTO_GARANZIA": 1}
        assert ri["per_direzione"]["RICEVUTA"]["n"] == 2
        assert ri["per_direzione"]["DATA"]["copertura"] == \
            pytest.approx(1.25)


class TestW544Riepilogo:
    def test_verdetto_da_rafforzare_anomalia(self):
        ri = _F["mh544_riepilogo"]([_v(vid="A", esp=0.0, fv=500.0)])
        assert ri["verdetto"] == "COPERTURE_DA_RAFFORZARE"
        assert ri["n_anomalie"] == 1

    def test_verdetto_da_rafforzare_copertura_bassa(self):
        ri = _F["mh544_riepilogo"]([_v(vid="A", esp=1000.0, fv=800.0)])
        assert ri["verdetto"] == "COPERTURE_DA_RAFFORZARE"

    def test_verdetto_tesa(self):
        ri = _F["mh544_riepilogo"]([_v(vid="A", esp=1000.0, fv=950.0)])
        assert ri["verdetto"] == "COPERTURA_TESA"

    def test_riepilogo_ko(self):
        with pytest.raises(ValueError):
            _F["mh544_riepilogo"]([])
        with pytest.raises(ValueError):
            _F["mh544_riepilogo"]("non-lista")


class TestW544Registry:
    def test_titolo_544_presente(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert src.count(TITLE544) == 3

    def test_registry_tab_count_544(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        assert len(re.findall(r"tab\d+", line.split("= st.tabs([")[0])) == 563
        assert len(re.findall(r"^\s*with (tab\d+):", src, re.M)) == 563

    def test_tab544_chain(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert ", tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563 = st.tabs([" in src
        assert "with tab544:" in src

    def test_chiavi_st544_uniche(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        keys = re.findall(r'key=f?"(st544_[^\\"]+)"', src)
        assert len(set(keys)) == len(keys) >= 10
