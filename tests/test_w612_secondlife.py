"""Test tab612 "🔋♻️ Second-life: batterie EV → storage stazionario".

I valori della demo sono calcolati a mano (script indipendente) e
contro-verificati per plausibilita': 500 kWh residui, 2 cicli/giorno,
DoD 80 %, eta 85 %, degrado 3 %/anno, spread 60 -> 140 eur/MWh,
capex 70 keur -> VAN +48,0 keur al 6 %, TIR ~19,0 %, payback anno 5,
LCOS ~118,1 eur/MWh -> CONVIENE.
"""

import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh612_num", "mh612_nneg", "mh612_pos", "mh612_frac01",
           "mh612_frac01_open", "mh612_intero",
           "mh612_energia_scarica_giorno", "mh612_capacita_residua",
           "mh612_energie_annue", "mh612_margine_giorno", "mh612_capex",
           "mh612_riciclo_fine_vita", "mh612_flussi", "mh612_van",
           "mh612_tir", "mh612_payback", "mh612_lcos", "mh612_verdetto",
           "mh612_demo")

TITLE612 = "🔋♻️ Second-life: batterie EV → storage stazionario"

# Demo: 500 kWh, 2 cicli/giorno, DoD 0,8, eta 0,85, degrado 0,03,
# p_dis=140, p_ch=60, acq=80, ric=40, fisso=10000, opex 4 %, riciclo=30,
# anni=10, tasso=6 %
DEMO = _F["mh612_demo"]()
E_DIS0 = 0.8                    # 500*2*0,8/1000 MWh/giorno
E_CH0 = 0.9411764705882353      # 0,8/0,85 MWh/giorno
MARGINE_G = 55.52941176470588   # 0,8*140 - E_CH0*60 eur/giorno
CAPEX = 70000.0                 # 500*80 + 500*40 + 10000
OPEX_A = 2800.0                 # 0,04*70000
FLUSSO_1 = 17468.235294117647   # MARGINE_G*365 - OPEX_A
RICICLO = 11061.361903423922    # 500*0,97^10*30
VAN6 = 48038.445372040514
TIR_DEMO = 0.1899652367314571
PAYBACK = 5
LCOS = 118.06520504498693


def _flussi_demo():
    d = DEMO
    return _F["mh612_flussi"](d["cap_kwh"], d["cicli_giorno"], d["dod"],
                              d["eta"], d["degrado"], d["p_dis"], d["p_ch"],
                              d["costo_acq_kwh"], d["costo_ric_kwh"],
                              d["capex_fisso"], d["opex_frac"],
                              d["valore_riciclo_kwh"], d["anni"])


class TestW612Validatori:
    def test_num(self):
        assert _F["mh612_num"](3, "x") == 3.0
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh612_num"](bad, "x")

    def test_nneg_pos(self):
        assert _F["mh612_nneg"](0, "x") == 0.0
        assert _F["mh612_pos"](0.5, "x") == 0.5
        with pytest.raises(ValueError):
            _F["mh612_nneg"](-0.1, "x")
        with pytest.raises(ValueError):
            _F["mh612_pos"](0.0, "x")

    def test_frac(self):
        assert _F["mh612_frac01"](0.0, "x") == 0.0
        assert _F["mh612_frac01"](1.0, "x") == 1.0
        with pytest.raises(ValueError):
            _F["mh612_frac01"](1.1, "x")
        with pytest.raises(ValueError):
            _F["mh612_frac01_open"](0.0, "x")
        with pytest.raises(ValueError):
            _F["mh612_frac01_open"](1.0, "x")
        assert _F["mh612_frac01_open"](0.5, "x") == 0.5

    def test_intero(self):
        assert _F["mh612_intero"](3.0, "x", 1, 60) == 3
        for bad in (True, 3.5, "3", 0, 61):
            with pytest.raises(ValueError):
                _F["mh612_intero"](bad, "x", 1, 60)


class TestW612Modello:
    def test_energia_scarica_giorno(self):
        assert _F["mh612_energia_scarica_giorno"](500.0, 2.0, 0.8) == \
            pytest.approx(E_DIS0)
        with pytest.raises(ValueError):
            _F["mh612_energia_scarica_giorno"](0.0, 2.0, 0.8)
        with pytest.raises(ValueError):
            _F["mh612_energia_scarica_giorno"](500.0, 2.0, 0.0)

    def test_capacita_residua(self):
        assert _F["mh612_capacita_residua"](500.0, 0.03, 0) == \
            pytest.approx(500.0)
        assert _F["mh612_capacita_residua"](500.0, 0.03, 10) == \
            pytest.approx(368.71206344796405)
        with pytest.raises(ValueError):
            _F["mh612_capacita_residua"](500.0, 1.0, 5)

    def test_energie_annue(self):
        en = _F["mh612_energie_annue"](500.0, 2.0, 0.8, 0.85, 0.03, 10)
        assert len(en["e_dis"]) == 10 and len(en["e_ch"]) == 10
        assert en["e_dis"][0] == pytest.approx(292.0)      # 0,8*365
        assert en["e_dis"][1] == pytest.approx(283.24)     # *0,97
        assert en["e_ch"][0] == pytest.approx(292.0 / 0.85)
        with pytest.raises(ValueError):
            _F["mh612_energie_annue"](500.0, 2.0, 0.8, 0.85, 0.03, 0)

    def test_margine_giorno(self):
        assert _F["mh612_margine_giorno"](E_DIS0, 0.85, 140.0, 60.0) == \
            pytest.approx(MARGINE_G)
        # spread negativo -> margine negativo
        assert _F["mh612_margine_giorno"](E_DIS0, 0.85, 10.0, 60.0) < 0.0

    def test_capex(self):
        assert _F["mh612_capex"](500.0, 80.0, 40.0, 10000.0) == \
            pytest.approx(CAPEX)

    def test_riciclo(self):
        assert _F["mh612_riciclo_fine_vita"](500.0, 0.03, 10, 30.0) == \
            pytest.approx(RICICLO)
        assert _F["mh612_riciclo_fine_vita"](500.0, 0.03, 10, 0.0) == \
            pytest.approx(0.0)


class TestW612Finanza:
    def test_flussi_demo(self):
        fl = _flussi_demo()
        assert len(fl) == 11
        assert fl[0] == pytest.approx(-CAPEX)
        assert fl[1] == pytest.approx(FLUSSO_1)
        assert fl[-1] > fl[-2]  # l'ultimo anno include il riciclo

    def test_van_tir_payback(self):
        fl = _flussi_demo()
        assert _F["mh612_van"](fl, 0.06) == pytest.approx(VAN6, rel=1e-6)
        assert _F["mh612_tir"](fl) == pytest.approx(TIR_DEMO, rel=1e-4)
        assert _F["mh612_payback"](fl) == PAYBACK
        # TIR assente su flussi a segno costante (lezione tab611)
        assert _F["mh612_tir"]([10.0, 5.0, 5.0]) is None
        assert _F["mh612_tir"]([-10.0, -5.0, -5.0]) is None
        assert _F["mh612_payback"]([-10.0, -1.0, -1.0]) is None

    def test_lcos_demo(self):
        en = _F["mh612_energie_annue"](500.0, 2.0, 0.8, 0.85, 0.03, 10)
        lcos = _F["mh612_lcos"](CAPEX, OPEX_A, en["e_ch"], 60.0,
                                en["e_dis"], 10, 0.06)
        assert lcos == pytest.approx(LCOS, rel=1e-6)
        assert _F["mh612_lcos"](CAPEX, OPEX_A, [0.0] * 10, 60.0,
                                [0.0] * 10, 10, 0.06) is None

    def test_verdetto(self):
        assert _F["mh612_verdetto"](VAN6, PAYBACK, 10)["verdetto"] == \
            "CONVIENE"
        assert _F["mh612_verdetto"](1000.0, None, 10)["verdetto"] == \
            "MARGINALE"
        assert _F["mh612_verdetto"](1000.0, 9, 10)["verdetto"] == \
            "MARGINALE"
        assert _F["mh612_verdetto"](-100.0, None, 10)["verdetto"] == \
            "NON_CONVIENE"
        assert _F["mh612_verdetto"](0.0, None, 10)["verdetto"] == \
            "NON_CONVIENE"

    def test_demo_dict(self):
        assert DEMO["cap_kwh"] == 500.0
        assert DEMO["anni"] == 10
        assert set(DEMO) == {"cap_kwh", "cicli_giorno", "dod", "eta",
                             "degrado", "p_dis", "p_ch", "costo_acq_kwh",
                             "costo_ric_kwh", "capex_fisso", "opex_frac",
                             "valore_riciclo_kwh", "anni", "tasso"}


class TestW612Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def _ui(self):
        return self._src().split("with tab612:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 625
        assert TITLE612 in titles
        assert TITLE612 in titles

    def test_chain(self):
        assert ", tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625 = st.tabs([" in self._src()
        assert "with tab612:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st612_[a-z0-9_]+", self._ui()))
        attese = {"st612_cap", "st612_cicli", "st612_dod", "st612_eta",
                  "st612_degr", "st612_pdis", "st612_pch", "st612_caq",
                  "st612_cr", "st612_cfix", "st612_opex", "st612_ric",
                  "st612_anni", "st612_tasso", "st612_go", "st612_graf",
                  "st612_tab", "st612_chart", "st612_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st612_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        sec = self._src().split('# W612 (21/10/2026)')[1]
        sec = sec.split('# W611 (21/10/2026)')[0]
        for w in ("api_key", "apikey", "password", "passwd", "secret",
                  "token"):
            assert w not in sec.lower(), f"sospetto segreto: {w}"
