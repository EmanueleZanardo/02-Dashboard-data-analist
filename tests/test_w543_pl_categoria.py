"""Test tab543 '📊📋 P&L per categoria (IFRS 7.20)': registry + funzioni pure."""

import math
import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh543_num", "mh543_str", "mh543_cat",
           "mh543_voce", "mh543_demo", "mh543_riepilogo")

TITLE543 = "📊📋 P&L per categoria (IFRS 7.20)"


def _v(vid="V-1", d="x", cat="FVTPL", ia=0.0, uf=0.0, dv=0.0, ip=0.0,
       ie=0.0, cn=0.0):
    return {"id": vid, "descrizione": d, "categoria": cat,
            "interessi_attivi": ia, "utili_fv": uf, "dividendi": dv,
            "interessi_passivi": ip, "impairment_ecl": ie,
            "commissioni_nette": cn}


class TestW543Validatori:
    def test_num_ok(self):
        assert _F["mh543_num"](2, "x") == 2.0
        assert _F["mh543_num"](-3.5, "x") == -3.5

    def test_num_ko(self):
        for bad in (True, False, "1", None, math.nan, math.inf,
                    -math.inf):
            with pytest.raises(ValueError):
                _F["mh543_num"](bad, "x")

    def test_str_ok_ko(self):
        assert _F["mh543_str"]("  abc  ", "x") == "abc"
        for bad in ("", "   ", None, 12, True):
            with pytest.raises(ValueError):
                _F["mh543_str"](bad, "x")

    def test_cat_ok_ko(self):
        for c in ("FVTPL", "COSTO_AMMORTIZZATO", "FVOCI"):
            assert _F["mh543_cat"](c, "x") == c
        for bad in ("AC", "fvtpl", "", None, 1):
            with pytest.raises(ValueError):
                _F["mh543_cat"](bad, "x")


class TestW543Voce:
    def test_pl_calcolo(self):
        o = _F["mh543_voce"](_v(cat="COSTO_AMMORTIZZATO", ia=1000.0,
                               uf=0.0, dv=0.0, ip=200.0, ie=50.0,
                               cn=-30.0))
        assert o["pl_netto"] == pytest.approx(720.0)
        assert o["anomalie"] == []

    def test_fv_su_non_fvtpl_anomalia(self):
        o = _F["mh543_voce"](_v(cat="COSTO_AMMORTIZZATO", uf=500.0))
        assert len(o["anomalie"]) == 1
        assert "FVTPL" in o["anomalie"][0]

    def test_ecl_su_fvtpl_anomalia(self):
        o = _F["mh543_voce"](_v(ie=100.0, uf=50.0))
        assert len(o["anomalie"]) == 1
        assert "5.5.1" in o["anomalie"][0]

    def test_dividendi_su_ac_anomalia(self):
        o = _F["mh543_voce"](_v(cat="COSTO_AMMORTIZZATO", dv=80.0))
        assert len(o["anomalie"]) == 1
        assert "dividendi" in o["anomalie"][0]

    def test_fvtpl_senza_movimenti_anomalia(self):
        o = _F["mh543_voce"](_v())
        assert len(o["anomalie"]) == 1
        assert "senza alcun movimento" in o["anomalie"][0]

    def test_voce_ko(self):
        with pytest.raises(ValueError):
            _F["mh543_voce"]("x")
        with pytest.raises(ValueError):
            _F["mh543_voce"]({k: 0 for k in ()} | {"id": "A"})
        with pytest.raises(ValueError):
            _F["mh543_voce"](_v(vid="  "))
        with pytest.raises(ValueError):
            _F["mh543_voce"](_v(cat="X"))
        with pytest.raises(ValueError):
            _F["mh543_voce"](_v(ia=-1.0))
        with pytest.raises(ValueError):
            _F["mh543_voce"](_v(dv=-1.0))
        with pytest.raises(ValueError):
            _F["mh543_voce"](_v(ip=-1.0))
        with pytest.raises(ValueError):
            _F["mh543_voce"](_v(ie=-1.0))


class TestW543Demo:
    def test_demo_totali(self):
        righe = [_F["mh543_voce"](d) for d in _F["mh543_demo"]()]
        assert [r["categoria"] for r in righe] == [
            "FVTPL", "COSTO_AMMORTIZZATO", "FVOCI"]
        assert [r["pl_netto"] for r in righe] == [
            pytest.approx(85000.0), pytest.approx(10500.0),
            pytest.approx(19500.0)]
        assert all(r["anomalie"] == [] for r in righe)


class TestW543Riepilogo:
    def _demo(self):
        return [_F["mh543_voce"](d) for d in _F["mh543_demo"]()]

    def test_totali_demo(self):
        ri = _F["mh543_riepilogo"](self._demo())
        assert ri["n"] == 3
        assert ri["pl_totale"] == pytest.approx(115000.0)
        assert ri["per_categoria"] == {
            "FVTPL": pytest.approx(85000.0),
            "COSTO_AMMORTIZZATO": pytest.approx(10500.0),
            "FVOCI": pytest.approx(19500.0)}
        assert ri["categoria_dominante"] == "FVTPL"
        assert ri["quota_dominante_pct"] == pytest.approx(
            85000.0 / 115000.0 * 100.0)
        assert ri["n_anomalie"] == 0
        assert ri["verdetto"] == "REDDITO_NETTO_POSITIVO"

    def test_verdetto_negativo(self):
        righe = [_F["mh543_voce"](_v("A", "a", "FVTPL", uf=-50.0))]
        ri = _F["mh543_riepilogo"](righe)
        assert ri["verdetto"] == "REDDITO_NETTO_NEGATIVO"

    def test_verdetto_pareggio(self):
        righe = [_F["mh543_voce"](_v("A", "a", "FVTPL", uf=50.0)),
                 _F["mh543_voce"](_v("B", "b", "FVOCI", uf=0.0,
                                     ia=50.0, ip=100.0))]
        ri = _F["mh543_riepilogo"](righe)
        assert ri["pl_totale"] == pytest.approx(0.0)
        assert ri["verdetto"] == "PAREGGIO"

    def test_verdetto_anomalie(self):
        righe = [_F["mh543_voce"](_v("A", "a", "COSTO_AMMORTIZZATO",
                                     uf=100.0, ia=500.0))]
        ri = _F["mh543_riepilogo"](righe)
        assert ri["n_anomalie"] == 1
        assert ri["verdetto"] == "ANOMALIE_DA_VERIFICARE"

    def test_riepilogo_ko(self):
        with pytest.raises(ValueError):
            _F["mh543_riepilogo"]([])
        with pytest.raises(ValueError):
            _F["mh543_riepilogo"]("x")
        with pytest.raises(ValueError):
            _F["mh543_riepilogo"]([_F["mh543_voce"](_v(uf=1.0))] * 5)
        with pytest.raises(ValueError):
            _F["mh543_riepilogo"](["x"])
        with pytest.raises(ValueError):
            _F["mh543_riepilogo"]([{"id": "A"}])


class TestW543Registry:
    def test_titolo_543_presente(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert src.count(TITLE543) == 3

    def test_registry_tab_count_543(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        assert len(re.findall(r"tab\d+", line.split("= st.tabs([")[0])) == 558
        assert len(re.findall(r"^\s*with (tab\d+):", src, re.M)) == 558

    def test_tab543_chain(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert ", tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558 = st.tabs([" in src
        assert "with tab543:" in src

    def test_chiavi_st543_uniche(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        keys = re.findall(r'key=f?"(st543_[^\\"]+)"', src)
        assert len(set(keys)) == len(keys) >= 10
