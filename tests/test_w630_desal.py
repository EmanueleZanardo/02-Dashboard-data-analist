"""Test tab630 "💧🌊 Desalinizzazione RO: il costo dell'acqua dall'energia".

Demo calcolata a mano: 100 m³/h x 8000 h -> 800.000 m³/anno;
capacita' 100 x 24 = 2.400 m³/giorno; CRF(7 %, 25 a) =
0,0858105172206656; capex 1500 €/(m³/g) x 2400 = 3.600.000;
capitale annuo = 3,6M x CRF + 3,6M x 3 % = 416.917,86199439614;
energia 800000 x 3,5 x 70/1000 = 196.000; consumabili 800000 x 0,08
= 64.000; totale 676.917,8619943962; LCOW = 0,8461473274929953 €/m³.
Benchmark 1,20 €/m³ -> CONVIENTE (margine 0,3539). Fisso 0,5211473,
variabile 0,325; quota energia 0,2895476851837344 (28,95 %).
"""

import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh630_num", "mh630_nneg", "mh630_pos", "mh630_frac01",
           "mh630_m3_annui", "mh630_capacita_m3_g", "mh630_crf",
           "mh630_capex_totale", "mh630_costo_capitale_annuo",
           "mh630_costo_energia", "mh630_costo_consumabili",
           "mh630_lcow", "mh630_fisso_m3", "mh630_variabile_m3",
           "mh630_quota_energia", "mh630_verdetto",
           "mh630_sensibilita", "mh630_demo")

TITLE630 = ("💧🌊 Desalinizzazione RO: il costo dell'acqua dall'energia")

DEMO = _F["mh630_demo"]()
T_DEMO = 800000.0
CAP_DEMO = 2400.0
CRF_DEMO = 0.0858105172206656
CAPEX_TOT_DEMO = 3600000.0
CAP_ANN_DEMO = 416917.86199439614
EN_DEMO = 196000.0
CONS_DEMO = 64000.0
TOT_DEMO = 676917.8619943962
LCOW_DEMO = 0.8461473274929953
FISSO_DEMO = 0.5211473274929952
VAR_DEMO = 0.325
QEN_DEMO = 0.2895476851837344


class TestW630Validatori:
    def test_num(self):
        assert _F["mh630_num"](3, "x") == 3.0
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh630_num"](bad, "x")

    def test_nneg_pos_frac01(self):
        assert _F["mh630_nneg"](0, "x") == 0.0
        assert _F["mh630_pos"](0.001, "x") == 0.001
        assert _F["mh630_frac01"](1, "x") == 1.0
        for bad in (-1.0,):
            with pytest.raises(ValueError):
                _F["mh630_nneg"](bad, "x")
        for bad in (0.0, -2.0):
            with pytest.raises(ValueError):
                _F["mh630_pos"](bad, "x")
        for bad in (-0.1, 1.1):
            with pytest.raises(ValueError):
                _F["mh630_frac01"](bad, "x")


class TestW630Catena:
    def test_m3_e_capacita(self):
        assert _F["mh630_m3_annui"](100.0, 8000.0) == T_DEMO
        assert _F["mh630_capacita_m3_g"](100.0) == CAP_DEMO
        with pytest.raises(ValueError):
            _F["mh630_m3_annui"](-1.0, 8000.0)

    def test_crf(self):
        assert _F["mh630_crf"](7.0, 25.0) == pytest.approx(CRF_DEMO)
        assert _F["mh630_crf"](0.0, 25.0) == pytest.approx(1.0 / 25.0)
        with pytest.raises(ValueError):
            _F["mh630_crf"](7.0, 0.0)

    def test_capex_e_capitale(self):
        assert _F["mh630_capex_totale"](1500.0, CAP_DEMO) == CAPEX_TOT_DEMO
        ca = _F["mh630_costo_capitale_annuo"](CAPEX_TOT_DEMO, CRF_DEMO, 3.0)
        assert ca == pytest.approx(CAP_ANN_DEMO)
        with pytest.raises(ValueError):
            _F["mh630_capex_totale"](-5.0, CAP_DEMO)

    def test_energia_e_consumabili(self):
        assert _F["mh630_costo_energia"](T_DEMO, 3.5, 70.0) == EN_DEMO
        assert _F["mh630_costo_consumabili"](T_DEMO, 0.08) == CONS_DEMO
        assert _F["mh630_costo_energia"](T_DEMO, 3.5, 0.0) == 0.0

    def test_lcow(self):
        assert _F["mh630_lcow"](TOT_DEMO, T_DEMO) == \
            pytest.approx(LCOW_DEMO)
        assert _F["mh630_lcow"](TOT_DEMO, 0.0) is None
        with pytest.raises(ValueError):
            _F["mh630_lcow"](-1.0, T_DEMO)

    def test_fisso_variabile_quota(self):
        assert _F["mh630_fisso_m3"](CAP_ANN_DEMO, T_DEMO) == \
            pytest.approx(FISSO_DEMO)
        assert _F["mh630_variabile_m3"](EN_DEMO, CONS_DEMO, T_DEMO) == \
            pytest.approx(VAR_DEMO)
        assert _F["mh630_fisso_m3"](CAP_ANN_DEMO, T_DEMO) + \
            _F["mh630_variabile_m3"](EN_DEMO, CONS_DEMO, T_DEMO) == \
            pytest.approx(LCOW_DEMO)
        assert _F["mh630_quota_energia"](EN_DEMO, TOT_DEMO) == \
            pytest.approx(QEN_DEMO)
        assert _F["mh630_quota_energia"](EN_DEMO, 0.0) is None
        assert _F["mh630_fisso_m3"](CAP_ANN_DEMO, 0.0) is None
        assert _F["mh630_variabile_m3"](EN_DEMO, CONS_DEMO, 0.0) is None

    def test_verdetto(self):
        v = _F["mh630_verdetto"](LCOW_DEMO, 1.20)
        assert v["verdetto"] == "CONVIENTE"
        assert v["gap"] == pytest.approx(LCOW_DEMO - 1.20)
        assert "0.846" in v["msg"]
        v2 = _F["mh630_verdetto"](1.30, 1.20)
        assert v2["verdetto"] == "MARGINALE"
        v3 = _F["mh630_verdetto"](1.50, 1.20)
        assert v3["verdetto"] == "NON_CONVIENTE"
        assert "1.500" in v3["msg"]  # pareggio citato nel msg
        v4 = _F["mh630_verdetto"](None, 1.20)
        assert v4["verdetto"] == "NON_CALCOLABILE"
        with pytest.raises(ValueError):
            _F["mh630_verdetto"](LCOW_DEMO, -1.0)

    def test_sensibilita(self):
        rows = _F["mh630_sensibilita"](
            100.0, 8000.0, 7.0, 25.0, 3.0, 1500.0, 0.08, 1.20,
            [2.5, 3.5], [30.0, 70.0])
        assert len(rows) == 4
        r00 = rows[0]
        assert r00["kwh_m3"] == 2.5
        assert r00["prezzo_el_eur_mwh"] == 30.0
        # riga hand-computed: en = 800000 x 2,5 x 30/1000 = 60.000
        u00 = (CAP_ANN_DEMO + 60000.0 + CONS_DEMO) / T_DEMO
        assert r00["lcow_eur_m3"] == pytest.approx(u00)
        assert r00["lcow_eur_m3"] == pytest.approx(0.6761473274929951)
        assert r00["verdetto"] == "CONVIENTE"
        r13 = rows[3]
        assert r13["kwh_m3"] == 3.5
        assert r13["prezzo_el_eur_mwh"] == 70.0
        assert r13["lcow_eur_m3"] == pytest.approx(LCOW_DEMO)
        assert r13["verdetto"] == "CONVIENTE"

    def test_demo(self):
        d = DEMO
        assert d["portata_m3_h"] == 100.0
        assert d["ore_annue"] == 8000.0
        assert d["benchmark_eur_m3"] == 1.20

    def test_catena_completa(self):
        d = dict(DEMO)
        m3 = _F["mh630_m3_annui"](d["portata_m3_h"], d["ore_annue"])
        cap = _F["mh630_capacita_m3_g"](d["portata_m3_h"])
        crf = _F["mh630_crf"](d["tasso_pct"], d["anni"])
        cp = _F["mh630_capex_totale"](d["capex_spec_eur_m3g"], cap)
        ca = _F["mh630_costo_capitale_annuo"](cp, crf, d["opex_pct"])
        ce = _F["mh630_costo_energia"](m3, d["kwh_m3"], d["prezzo_el_mwh"])
        cc = _F["mh630_costo_consumabili"](m3, d["eur_m3_cons"])
        tot = ca + ce + cc
        u = _F["mh630_lcow"](tot, m3)
        ver = _F["mh630_verdetto"](u, d["benchmark_eur_m3"])
        assert m3 == pytest.approx(T_DEMO)
        assert cap == pytest.approx(CAP_DEMO)
        assert crf == pytest.approx(CRF_DEMO)
        assert cp == pytest.approx(CAPEX_TOT_DEMO)
        assert ca == pytest.approx(CAP_ANN_DEMO)
        assert ce == pytest.approx(EN_DEMO)
        assert cc == pytest.approx(CONS_DEMO)
        assert tot == pytest.approx(TOT_DEMO)
        assert u == pytest.approx(LCOW_DEMO)
        assert ver["verdetto"] == "CONVIENTE"


class TestW630Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def _ui(self):
        return self._src().split("with tab630:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 794
        assert TITLE630 in titles
        assert TITLE630 in titles

    def test_chain(self):
        assert ", tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790, tab791, tab792, tab793, tab794 = st.tabs([" in self._src()
        assert "with tab630:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st630_[a-z0-9_]+", self._ui()))
        attese = {"st630_port", "st630_ore", "st630_pel", "st630_cx",
                  "st630_anni", "st630_tasso", "st630_opex", "st630_bm",
                  "st630_kwh", "st630_cons", "st630_tab", "st630_graf",
                  "st630_go", "st630_fig", "st630_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st630_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        sec = self._src().split('# W630 (22/10/2026)')[1]
        sec = sec.split('# W629 (22/10/2026)')[0]
        for w in ("api_key", "apikey", "password", "passwd", "secret",
                  "token"):
            assert w not in sec.lower(), f"sospetto segreto: {w}"
