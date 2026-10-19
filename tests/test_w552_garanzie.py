"""Test tab552 'Garanzie reali acquisite in possesso (IFRS 7.38)': registry + funzioni pure."""

import math
import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh552_num", "mh552_str", "mh552_int0", "mh552_tipo",
           "mh552_politica", "mh552_garanzia", "mh552_demo",
           "mh552_riepilogo")

TITLE552 = "🏦🔑 Garanzie reali acquisite in possesso (IFRS 7.38)"


def _g(vid="G-1", d="x", tp="MACCHINARI", vc=1000000.0, fv=1100000.0,
       cr=1200000.0, gg=30, po="ALIENAZIONE_ENTRO_12_MESI"):
    return {"id": vid, "descrizione": d, "tipo": tp,
            "valore_contabile": vc, "fair_value": fv,
            "credito_estinto": cr, "giorni_detenzione": gg,
            "politica": po}


class TestW552Validatori:
    def test_num_ok(self):
        assert _F["mh552_num"](2, "x") == 2.0
        assert _F["mh552_num"](0, "x") == 0.0
        assert _F["mh552_num"](2.5, "x") == 2.5

    def test_num_ko(self):
        for bad in (True, False, "1", None, math.nan, math.inf,
                    -math.inf, -1, -0.01):
            with pytest.raises(ValueError):
                _F["mh552_num"](bad, "x")

    def test_str_ok_ko(self):
        assert _F["mh552_str"]("  abc  ", "x") == "abc"
        for bad in ("", "   ", None, 5, True):
            with pytest.raises(ValueError):
                _F["mh552_str"](bad, "x")

    def test_int0_ok_ko(self):
        assert _F["mh552_int0"](0, "x") == 0
        assert _F["mh552_int0"](365, "x") == 365
        for bad in (-1, 1.5, "3", None, True, math.nan):
            with pytest.raises(ValueError):
                _F["mh552_int0"](bad, "x")

    def test_tipo_ok_ko(self):
        for ok in ("IMMOBILE", "IMPIANTO_FV", "IMPIANTO_EOLICO",
                   "MACCHINARI", "TITOLI_QUOTATI", "MERCE",
                   "ALTRE_ATTIVITA"):
            assert _F["mh552_tipo"](ok) == ok
        for bad in ("ALTRO", "", None, 3, True):
            with pytest.raises(ValueError):
                _F["mh552_tipo"](bad)

    def test_politica_ok_ko(self):
        for ok in ("ALIENAZIONE_ENTRO_12_MESI", "UTILIZZO_IN_ATTIVITA",
                   "IN_ATTESA_DECISIONE"):
            assert _F["mh552_politica"](ok) == ok
        for bad in ("VENDITA", "", None, 3, True):
            with pytest.raises(ValueError):
                _F["mh552_politica"](bad)


class TestW552Garanzia:
    def test_garanzia_ok(self):
        o = _F["mh552_garanzia"](_g())
        assert o["rapporto_copertura"] == pytest.approx(1000000.0 / 1200000.0)
        assert o["scarto_valutazione"] == pytest.approx(-100000.0)
        assert o["anomalie"] == []

    def test_garanzia_ko_struttura(self):
        with pytest.raises(ValueError):
            _F["mh552_garanzia"]("non-dict")
        with pytest.raises(ValueError):
            _F["mh552_garanzia"]({"id": "x"})
        with pytest.raises(ValueError):
            _F["mh552_garanzia"](_g(vc=-1))
        with pytest.raises(ValueError):
            _F["mh552_garanzia"](_g(fv=math.nan))
        with pytest.raises(ValueError):
            _F["mh552_garanzia"](_g(gg=-5))
        with pytest.raises(ValueError):
            _F["mh552_garanzia"](_g(tp="ALTRO"))
        with pytest.raises(ValueError):
            _F["mh552_garanzia"](_g(po="VENDITA"))
        with pytest.raises(ValueError):
            _F["mh552_garanzia"](_g(vid="  "))

    def test_anomalia_fair_value_mancante(self):
        o = _F["mh552_garanzia"](_g(fv=0.0))
        assert any("Fair value non indicato" in a for a in o["anomalie"])

    def test_anomalia_vc_sopra_fair_value(self):
        o = _F["mh552_garanzia"](_g(vc=1300000.0, fv=1100000.0))
        assert any("impairment" in a for a in o["anomalie"])

    def test_anomalia_copertura_voce_bassa(self):
        o = _F["mh552_garanzia"](_g(vc=500000.0, fv=600000.0,
                                   cr=1200000.0))
        assert any("oltre il doppio" in a for a in o["anomalie"])

    def test_nessuna_anomalia_sotto_doppio(self):
        o = _F["mh552_garanzia"](_g(vc=500000.0, fv=600000.0,
                                   cr=1000000.0))
        assert o["anomalie"] == []

    def test_anomalia_senza_credito(self):
        o = _F["mh552_garanzia"](_g(cr=0.0))
        assert any("senza credito estinto" in a for a in o["anomalie"])

    def test_anomalia_politica_troppo_attesa(self):
        o = _F["mh552_garanzia"](_g(po="IN_ATTESA_DECISIONE", gg=400))
        assert any("365 giorni" in a for a in o["anomalie"])

    def test_politica_attesa_breve_ok(self):
        o = _F["mh552_garanzia"](_g(po="IN_ATTESA_DECISIONE", gg=45))
        assert o["anomalie"] == []


class TestW552Demo:
    def test_demo_struttura(self):
        d = _F["mh552_demo"]()
        assert len(d) == 3
        assert {x["id"] for x in d} == {"FV-SIC-001", "MAC-DE-002",
                                       "TIT-UK-003"}

    def test_demo_anomalie_zero(self):
        for v in _F["mh552_demo"]():
            assert _F["mh552_garanzia"](v)["anomalie"] == []

    def test_demo_verdetto_adeguata(self):
        r = _F["mh552_riepilogo"](_F["mh552_demo"]())
        assert r["verdetto"] == "COPERTURA_ADEGUATA"
        assert r["rapporto_copertura"] == pytest.approx(6000000.0 / 7000000.0)
        assert r["n_anomalie"] == 0


class TestW552Riepilogo:
    def test_riepilogo_aggregati(self):
        r = _F["mh552_riepilogo"]([_g(), _g("G-2", tp="IMMOBILE",
                                           vc=500000.0, fv=500000.0,
                                           cr=500000.0)])
        assert r["n_voci"] == 2
        assert r["valore_contabile_tot"] == pytest.approx(1500000.0)
        assert r["crediti_estinti_tot"] == pytest.approx(1700000.0)
        assert r["scarto_valutazione_tot"] == pytest.approx(-100000.0)
        assert r["per_tipo"]["MACCHINARI"]["n"] == 1
        assert r["per_tipo"]["IMMOBILE"]["valore_contabile"] == \
            pytest.approx(500000.0)

    def test_verdetto_insufficiente(self):
        r = _F["mh552_riepilogo"]([_g(vc=500000.0, fv=600000.0,
                                     cr=800000.0)], 0.80)
        assert r["verdetto"] == "COPERTURA_INSUFFICIENTE"
        assert r["rapporto_copertura"] == pytest.approx(500000.0 / 800000.0)
        assert r["n_anomalie"] == 0

    def test_verdetto_soglia_custom(self):
        r = _F["mh552_riepilogo"]([_g(vc=500000.0, fv=600000.0,
                                     cr=800000.0)], 0.40)
        assert r["verdetto"] == "COPERTURA_ADEGUATA"

    def test_verdetto_nessuna(self):
        r = _F["mh552_riepilogo"]([_g(vc=0.0, fv=0.0, cr=0.0)])
        assert r["verdetto"] == "NESSUNA_GARANZIA"

    def test_verdetto_anomalie(self):
        r = _F["mh552_riepilogo"]([_g(fv=0.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 1

    def test_riepilogo_ko(self):
        for bad in ([], "x", None):
            with pytest.raises(ValueError):
                _F["mh552_riepilogo"](bad)
        for sg in (0.0, 1.5, -0.1, "0.8", True, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh552_riepilogo"]([_g()], sg)


class TestW552Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_titolo_552_presente(self):
        assert self._src().count(TITLE552) == 3

    def test_counts_552(self):
        src = self._src()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        assert "\n" not in line
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"    with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 564
        assert TITLE552 in titoli
        assert "tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564 = st.tabs([" in src

    def test_chiavi_552_univoche(self):
        src = self._src()
        righe = [ln for ln in src.split("\n")
                 if "key=" in ln and "st552_" in ln]
        # le f-string st552_id_{_i552} generano istanze a runtime: la base
        # e' fino al suffisso numerico; csv1/csv2 sono chiavi distinte
        basi = []
        for ln in righe:
            basi.append(re.search(r"st552_[a-z]+\d*", ln).group(0))
        assert len(basi) == len(set(basi))
        assert len(basi) >= 13
