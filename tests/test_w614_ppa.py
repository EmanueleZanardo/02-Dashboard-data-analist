"""Test tab614 "🟢📄 PPA vs merchant: il prezzo fisso vale lo sconto?".

I valori della demo sono calcolati a mano (script indipendente) e
contro-verificati per plausibilita': 50 GWh/anno, PPA 70 eur/MWh,
merchant 85, vol 30 %, tasso 6 %, 10 anni -> sconto 17,65 %,
haircut 49,35 %, prezzo prudente 43,0525 eur/MWh, ricavo PPA
3,5 mln/anno, VAN PPA 25,76 mln, VAN merchant 31,28 mln,
delta prudente +1,35 mln/anno -> CONVIENE.
"""

import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh614_num", "mh614_nneg", "mh614_pos", "mh614_frac01",
           "mh614_intero", "mh614_factor", "mh614_ricavo", "mh614_sconto",
           "mh614_haircut", "mh614_prezzo_prudente", "mh614_van",
           "mh614_delta", "mh614_verdetto", "mh614_sensitivita",
           "mh614_demo")

TITLE614 = "🟢📄 PPA vs merchant: il prezzo fisso vale lo sconto?"

# Demo: 50000 MWh/anno, PPA 70, merchant 85, vol 30 %, tasso 6 %, 10 anni
DEMO = _F["mh614_demo"]()
FACTOR = 7.360087051721735       # (1 - 1,06^-10)/0,06
R_PPA = 3500000.0               # 50000*70
R_MER = 4250000.0               # 50000*85
VAN_PPA = 25760304.680026073    # 3,5 mln * FACTOR
VAN_MER = 31280369.969817372    # 4,25 mln * FACTOR
SCONTO = 0.17647058823529413    # 15/85
HAIRCUT = 0.4935                # 1,645*0,30
P_PRUD = 43.0525                # 85*(1-0,4935)
R_PRUD = 2152625.0              # 50000*43,0525
DELTA_PRUD = 1347375.0          # 3,5 mln - 2,152625 mln


class TestW614Validatori:
    def test_num(self):
        assert _F["mh614_num"](3, "x") == 3.0
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh614_num"](bad, "x")

    def test_nneg(self):
        assert _F["mh614_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh614_nneg"](-1.0, "x")

    def test_pos(self):
        with pytest.raises(ValueError):
            _F["mh614_pos"](0.0, "x")
        with pytest.raises(ValueError):
            _F["mh614_pos"](-2.0, "x")

    def test_frac01(self):
        assert _F["mh614_frac01"](1.0, "x") == 1.0
        with pytest.raises(ValueError):
            _F["mh614_frac01"](1.0001, "x")

    def test_intero(self):
        assert _F["mh614_intero"](10, "x", 1, 40) == 10
        assert _F["mh614_intero"](10.0, "x", 1, 40) == 10
        for bad in (True, 10.5, 0, 41):
            with pytest.raises(ValueError):
                _F["mh614_intero"](bad, "x", 1, 40)


class TestW614Modello:
    def test_factor(self):
        assert _F["mh614_factor"](0.0, 10) == 10.0
        assert _F["mh614_factor"](0.06, 10) == pytest.approx(FACTOR)
        assert _F["mh614_factor"](0.05, 25) == pytest.approx(14.0939445719)

    def test_ricavo(self):
        assert _F["mh614_ricavo"](50000.0, 70.0) == R_PPA

    def test_sconto(self):
        assert _F["mh614_sconto"](70.0, 85.0) == pytest.approx(SCONTO)
        assert _F["mh614_sconto"](85.0, 85.0) == pytest.approx(0.0)
        assert _F["mh614_sconto"](90.0, 85.0) < 0.0  # PPA a premio

    def test_haircut(self):
        assert _F["mh614_haircut"](0.30) == pytest.approx(HAIRCUT)
        assert _F["mh614_haircut"](0.0) == 0.0

    def test_prezzo_prudente(self):
        assert _F["mh614_prezzo_prudente"](85.0, 0.30) == \
            pytest.approx(P_PRUD)

    def test_van(self):
        assert _F["mh614_van"](R_PPA, 0.06, 10) == pytest.approx(VAN_PPA)
        assert _F["mh614_van"](R_MER, 0.06, 10) == pytest.approx(VAN_MER)

    def test_delta(self):
        assert _F["mh614_delta"](70.0, 85.0, 50000.0) == -750000.0
        assert _F["mh614_delta"](85.0, 70.0, 50000.0) == 750000.0

    def test_demo(self):
        d = DEMO
        assert d["energia_mwh"] == 50000.0
        assert d["p_ppa"] == 70.0
        assert d["p_mer"] == 85.0
        assert d["vol"] == 0.30
        assert d["tasso"] == 0.06
        assert d["anni"] == 10


class TestW614Verdetto:
    def test_conviene_demo(self):
        v = _F["mh614_verdetto"](SCONTO, HAIRCUT)
        assert v["verdetto"] == "CONVIENE"
        assert "msg" in v

    def test_marginale(self):
        v = _F["mh614_verdetto"](HAIRCUT + 0.02, HAIRCUT)
        assert v["verdetto"] == "MARGINALE"

    def test_non_conviene(self):
        v = _F["mh614_verdetto"](0.50, 0.10)
        assert v["verdetto"] == "NON_CONVIENE"
        v2 = _F["mh614_verdetto"](HAIRCUT + 0.031, HAIRCUT)
        assert v2["verdetto"] == "NON_CONVIENE"

    def test_bordo(self):
        # sconto esattamente uguale all'haircut -> CONVIENE
        v = _F["mh614_verdetto"](HAIRCUT, HAIRCUT)
        assert v["verdetto"] == "CONVIENE"


class TestW614Sensitivita:
    def test_shape_e_chiavi(self):
        rows = _F["mh614_sensitivita"](50000.0, 70.0, [80.0, 90.0],
                                       [0.2, 0.3], 0.06, 10)
        assert len(rows) == 4
        attese = {"p_mer", "vol", "sconto", "haircut", "ricavo_ppa",
                  "ricavo_prudente", "delta_prudente", "verdetto"}
        assert set(rows[0].keys()) == attese

    def test_valori_riga(self):
        rows = _F["mh614_sensitivita"](50000.0, 70.0, [85.0], [0.30],
                                       0.06, 10)
        r = rows[0]
        assert r["sconto"] == pytest.approx(SCONTO)
        assert r["haircut"] == pytest.approx(HAIRCUT)
        assert r["ricavo_prudente"] == pytest.approx(R_PRUD)
        assert r["delta_prudente"] == pytest.approx(DELTA_PRUD)
        assert r["verdetto"] == "CONVIENE"

    def test_liste_vuote(self):
        with pytest.raises(ValueError):
            _F["mh614_sensitivita"](50000.0, 70.0, [], [0.3], 0.06, 10)
        with pytest.raises(ValueError):
            _F["mh614_sensitivita"](50000.0, 70.0, [85.0], [], 0.06, 10)


class TestW614Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def _ui(self):
        return self._src().split("with tab614:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 655
        assert TITLE614 in titles
        assert TITLE614 in titles

    def test_chain(self):
        assert ", tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655 = st.tabs([" in self._src()
        assert "with tab614:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st614_[a-z0-9_]+", self._ui()))
        attese = {"st614_vol", "st614_ppa", "st614_mer", "st614_vola",
                  "st614_tasso", "st614_anni", "st614_tab", "st614_graf",
                  "st614_go", "st614_fig", "st614_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st614_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        sec = self._src().split('# W614 (21/10/2026)')[1]
        sec = sec.split('# W613 (21/10/2026)')[0]
        for w in ("api_key", "apikey", "password", "passwd", "secret",
                  "token"):
            assert w not in sec.lower(), f"sospetto segreto: {w}"
