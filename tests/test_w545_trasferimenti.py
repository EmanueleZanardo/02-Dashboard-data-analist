"""Test tab545 'Trasferimenti di attivita' finanziarie (IFRS 7.42A-42H)': registry + funzioni pure."""

import math
import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh545_num", "mh545_str", "mh545_bool", "mh545_cat",
           "mh545_nat", "mh545_voce", "mh545_demo", "mh545_riepilogo")

TITLE545 = "🔄📤 Trasferimenti di attività finanziarie (IFRS 7.42A-42H)"


def _v(vid="V-1", d="x", cp="cp", vct=1000.0, pas=0.0, cr=0.0, der=True,
       tp="CARTOLARIZZAZIONE", nat="NESSUNA"):
    return {"id": vid, "descrizione": d, "controparte": cp,
            "valore_contabile_trasferito": vct, "passivita_associata": pas,
            "coinvolgimento_residuo": cr, "derecognized": der, "tipo": tp,
            "natura_mantenuta": nat}


class TestW545Validatori:
    def test_num_ok(self):
        assert _F["mh545_num"](2, "x") == 2.0
        assert _F["mh545_num"](0, "x") == 0.0
        assert _F["mh545_num"](2.5, "x") == 2.5

    def test_num_ko(self):
        for bad in (True, False, "1", None, math.nan, math.inf,
                    -math.inf, -1, -0.01):
            with pytest.raises(ValueError):
                _F["mh545_num"](bad, "x")

    def test_str_ok_ko(self):
        assert _F["mh545_str"]("  abc  ", "x") == "abc"
        for bad in ("", "   ", None, 12, True):
            with pytest.raises(ValueError):
                _F["mh545_str"](bad, "x")

    def test_bool_ok_ko(self):
        assert _F["mh545_bool"](True, "x") is True
        for bad in (1, 0, "s", None):
            with pytest.raises(ValueError):
                _F["mh545_bool"](bad, "x")

    def test_cat_ok_ko(self):
        for ok in ("CARTOLARIZZAZIONE", "FACTORING_PRO_SOLVENDO",
                   "FACTORING_PRO_SOLUTO", "PRESTITO_TITOLI",
                   "PRONTI_CONTRO_TERMINE_REPO"):
            assert _F["mh545_cat"](ok, "x") == ok
        for bad in ("LEASING", "cartolarizzazione", "", None, 1):
            with pytest.raises(ValueError):
                _F["mh545_cat"](bad, "x")

    def test_nat_ok_ko(self):
        for ok in ("RISCHI_PREMI", "CONTROLLO", "GARANZIA_RESIDUA",
                   "NESSUNA"):
            assert _F["mh545_nat"](ok, "x") == ok
        for bad in ("PARZIALE", "nessuna", "", None):
            with pytest.raises(ValueError):
                _F["mh545_nat"](bad, "x")


class TestW545Voce:
    def test_cancellata(self):
        o = _F["mh545_voce"](_v(vct=45000000.0))
        assert o["esposizione_residua"] == 0.0
        assert o["esito"] == "CANCELLATA"
        assert o["anomalie"] == []

    def test_coinvolgimento_residuo(self):
        o = _F["mh545_voce"](_v(vct=1000.0, pas=100.0, cr=50.0))
        assert o["esposizione_residua"] == 150.0
        assert o["esito"] == "COINVOLGIMENTO_RESIDUO"

    def test_mantenuta_totale(self):
        o = _F["mh545_voce"](_v(vct=1000.0, pas=900.0, cr=100.0,
                                der=False, nat="RISCHI_PREMI"))
        assert o["esposizione_residua"] == 1000.0
        assert o["esito"] == "MANTENUTA_TOTALE"

    def test_mantenuta_totale_boundary(self):
        o = _F["mh545_voce"](_v(vct=1000.0, pas=1000.0, der=False,
                                nat="CONTROLLO"))
        assert o["esito"] == "MANTENUTA_TOTALE"

    def test_mantenuta_parziale(self):
        o = _F["mh545_voce"](_v(vct=1000.0, pas=800.0, der=False,
                                nat="RISCHI_PREMI"))
        assert o["esito"] == "MANTENUTA_PARZIALE"

    def test_coinvolgimento_none_come_zero(self):
        o = _F["mh545_voce"](_v(cr=None))
        assert o["coinvolgimento_residuo"] == 0.0
        assert o["esito"] == "CANCELLATA"

    def test_anomalia_passivita_senza_trasferimento(self):
        o = _F["mh545_voce"](_v(vct=0.0, pas=200.0, der=False,
                                nat="GARANZIA_RESIDUA"))
        assert "passivita' associata senza trasferimento" in \
            o["anomalie"][0]

    def test_anomalia_derec_con_passivita(self):
        o = _F["mh545_voce"](_v(pas=100.0))
        assert any("passivita' associate" in a for a in o["anomalie"])

    def test_anomalia_coinvolgimento_natura_nessuna(self):
        o = _F["mh545_voce"](_v(cr=50.0))
        assert o["esito"] == "COINVOLGIMENTO_RESIDUO"
        assert any("NESSUNA" in a for a in o["anomalie"])

    def test_anomalia_prosoluto_esposizione(self):
        o = _F["mh545_voce"](_v(vct=1000.0, pas=300.0, der=False,
                                tp="FACTORING_PRO_SOLUTO",
                                nat="RISCHI_PREMI"))
        assert any("pro-soluto" in a for a in o["anomalie"])
        assert o["esito"] == "MANTENUTA_PARZIALE"

    def test_voce_ko(self):
        with pytest.raises(ValueError):
            _F["mh545_voce"]("non-dict")
        with pytest.raises(ValueError):
            _F["mh545_voce"](_v(vct=-1.0))
        with pytest.raises(ValueError):
            _F["mh545_voce"](_v(pas=-5.0))
        with pytest.raises(ValueError):
            _F["mh545_voce"](_v(cr=-2.0))
        with pytest.raises(ValueError):
            _F["mh545_voce"](_v(vid=""))
        with pytest.raises(ValueError):
            _F["mh545_voce"](_v(tp="LEASING"))
        with pytest.raises(ValueError):
            _F["mh545_voce"](_v(nat="PARZIALE"))
        with pytest.raises(ValueError):
            _F["mh545_voce"](_v(der="si"))


class TestW545Demo:
    def test_demo_verdetto(self):
        demo = _F["mh545_demo"]()
        assert len(demo) == 3
        assert [r["id"] for r in demo] == ["SEC-IT-001", "FAC-DE-002",
                                          "REPO-UK-003"]
        ri = _F["mh545_riepilogo"](demo)
        assert ri["valore_contabile_tot"] == pytest.approx(87500000.0)
        assert ri["esposizione_residua_tot"] == pytest.approx(29700000.0)
        assert ri["quota_residua_pct"] == pytest.approx(
            29700000.0 / 87500000.0)
        assert ri["verdetto"] == "ESPOSIZIONE_RESIDUA_TESA"
        assert ri["n_anomalie"] == 0
        assert ri["per_esito"] == {"CANCELLATA": 2,
                                  "MANTENUTA_PARZIALE": 1}
        assert ri["per_tipo"]["CARTOLARIZZAZIONE"] == 1
        assert ri["per_tipo"]["PRONTI_CONTRO_TERMINE_REPO"] == 1


class TestW545Riepilogo:
    def test_verdetto_critico(self):
        ri = _F["mh545_riepilogo"](
            [_v(vid="A", vct=1000.0, pas=500.0, der=False,
                nat="RISCHI_PREMI")])
        assert ri["quota_residua_pct"] == pytest.approx(0.5)
        assert ri["verdetto"] == "ESPOSIZIONE_RESIDUA_CRITICA"

    def test_verdetto_critico_boundary(self):
        ri = _F["mh545_riepilogo"](
            [_v(vid="A", vct=1000.0, pas=400.0, der=False,
                nat="CONTROLLO")])
        assert ri["verdetto"] == "ESPOSIZIONE_RESIDUA_CRITICA"

    def test_verdetto_tesa_boundary(self):
        ri = _F["mh545_riepilogo"](
            [_v(vid="A", vct=1000.0, pas=200.0, der=False,
                nat="GARANZIA_RESIDUA")])
        assert ri["verdetto"] == "ESPOSIZIONE_RESIDUA_TESA"

    def test_verdetto_adeguata(self):
        ri = _F["mh545_riepilogo"]([_v(vid="A", vct=1000.0)])
        assert ri["verdetto"] == "INFORMATIVA_ADEGUATA"

    def test_per_tipo(self):
        ri = _F["mh545_riepilogo"](
            [_v(vid="A"), _v(vid="B", tp="FACTORING_PRO_SOLUTO")])
        assert ri["per_tipo"] == {"CARTOLARIZZAZIONE": 1,
                                  "FACTORING_PRO_SOLUTO": 1}

    def test_riepilogo_ko(self):
        with pytest.raises(ValueError):
            _F["mh545_riepilogo"]([])
        with pytest.raises(ValueError):
            _F["mh545_riepilogo"]("non-lista")


class TestW545Registry:
    def test_titolo_545_presente(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert src.count(TITLE545) == 3

    def test_registry_tab_count_545(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        assert len(re.findall(r"tab\d+", line.split("= st.tabs([")[0])) == 824
        assert len(re.findall(r"^\s*with (tab\d+):", src, re.M)) == 824
