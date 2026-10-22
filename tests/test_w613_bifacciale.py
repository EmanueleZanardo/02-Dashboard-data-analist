"""Test tab613 "☀️🪞 FV bifacciale: il guadagno posteriore ripaga il sovraccosto?".

I valori della demo sono calcolati a mano (script indipendente) e
contro-verificati per plausibilita': 10 MWp, yield frontale 1150
kWh/kWp/anno, gain 8 %, capex mono 750 eur/kWp, premium 4 %, opex 12
eur/kWp/anno, tasso 5 %, 25 anni -> LCOE mono 56,71 eur/MWh, LCOE bif
54,22 eur/MWh, delta +2,49 eur/MWh, gain di break-even 3,26 % -> CONVIENE.
"""

import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh613_num", "mh613_nneg", "mh613_pos", "mh613_frac01",
           "mh613_frac01_open", "mh613_intero", "mh613_crf",
           "mh613_energia_annua", "mh613_capex_tot", "mh613_opex_annuo",
           "mh613_lcoe", "mh613_gain_breakeven", "mh613_delta_lcoe",
           "mh613_verdetto", "mh613_sensitivita", "mh613_demo")

TITLE613 = "☀️🪞 FV bifacciale: il guadagno posteriore ripaga il sovraccosto?"

# Demo: 10 MWp, yield 1150, gain 8 %, capex 750, premium 4 %,
# opex 12, tasso 5 %, anni 25
DEMO = _F["mh613_demo"]()
CRF525 = 0.0709524572992296
E_MONO = 11500.0                  # 10000*1150/1000 MWh/anno
E_BIF = 12420.0                   # *1,08 MWh/anno
LCOE_MONO = 56.70812432558452
LCOE_BIF = 54.221349994685255
DELTA = 2.486774330899266
GSTAR = 0.0326396559697264        # 3,26 %
CAPEX_MONO = 7500000.0            # 10000*750
CAPEX_BIF = 7800000.0             # *1,04
OPEX_A = 120000.0                 # 10000*12


def _demo_lcoe():
    d = DEMO
    e_m = _F["mh613_energia_annua"](d["pot_kwp"], d["yield_kwh_kwp"], 0.0)
    e_b = _F["mh613_energia_annua"](d["pot_kwp"], d["yield_kwh_kwp"],
                                    d["gain"])
    c_m = _F["mh613_capex_tot"](d["pot_kwp"], d["capex_mono_kwp"], 0.0)
    c_b = _F["mh613_capex_tot"](d["pot_kwp"], d["capex_mono_kwp"],
                                d["premium"])
    ox = _F["mh613_opex_annuo"](d["pot_kwp"], d["opex_kwp"])
    lm = _F["mh613_lcoe"](c_m, ox, e_m, d["tasso"], d["anni"])
    lb = _F["mh613_lcoe"](c_b, ox, e_b, d["tasso"], d["anni"])
    return e_m, e_b, c_m, c_b, ox, lm, lb


class TestW613Validatori:
    def test_num(self):
        assert _F["mh613_num"](3, "x") == 3.0
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh613_num"](bad, "x")

    def test_nneg_pos(self):
        assert _F["mh613_nneg"](0, "x") == 0.0
        assert _F["mh613_pos"](0.5, "x") == 0.5
        with pytest.raises(ValueError):
            _F["mh613_nneg"](-0.1, "x")
        with pytest.raises(ValueError):
            _F["mh613_pos"](0.0, "x")

    def test_frac(self):
        assert _F["mh613_frac01"](0.0, "x") == 0.0
        assert _F["mh613_frac01"](1.0, "x") == 1.0
        with pytest.raises(ValueError):
            _F["mh613_frac01"](1.1, "x")
        with pytest.raises(ValueError):
            _F["mh613_frac01_open"](0.0, "x")
        with pytest.raises(ValueError):
            _F["mh613_frac01_open"](1.0, "x")
        assert _F["mh613_frac01_open"](0.5, "x") == 0.5

    def test_intero(self):
        assert _F["mh613_intero"](25.0, "x", 1, 60) == 25
        for bad in (True, 25.5, "25", 0, 61):
            with pytest.raises(ValueError):
                _F["mh613_intero"](bad, "x", 1, 60)


class TestW613Modello:
    def test_crf(self):
        assert _F["mh613_crf"](0.05, 25) == pytest.approx(CRF525, rel=1e-12)
        # tasso 0 -> 1/n
        assert _F["mh613_crf"](0.0, 25) == pytest.approx(1.0 / 25)
        # definizione a mano: r(1+r)^n / ((1+r)^n - 1)
        r, n = 0.07, 20
        f = (1.0 + r) ** n
        assert _F["mh613_crf"](r, n) == pytest.approx(r * f / (f - 1.0))
        with pytest.raises(ValueError):
            _F["mh613_crf"](-0.01, 25)
        with pytest.raises(ValueError):
            _F["mh613_crf"](0.05, 0)

    def test_energia_annua(self):
        assert _F["mh613_energia_annua"](10000.0, 1150.0, 0.0) == \
            pytest.approx(E_MONO)
        assert _F["mh613_energia_annua"](10000.0, 1150.0, 0.08) == \
            pytest.approx(E_BIF)
        with pytest.raises(ValueError):
            _F["mh613_energia_annua"](0.0, 1150.0, 0.08)
        with pytest.raises(ValueError):
            _F["mh613_energia_annua"](10000.0, 1150.0, -0.01)

    def test_capex_opex(self):
        assert _F["mh613_capex_tot"](10000.0, 750.0, 0.0) == \
            pytest.approx(CAPEX_MONO)
        assert _F["mh613_capex_tot"](10000.0, 750.0, 0.04) == \
            pytest.approx(CAPEX_BIF)
        assert _F["mh613_opex_annuo"](10000.0, 12.0) == \
            pytest.approx(OPEX_A)
        with pytest.raises(ValueError):
            _F["mh613_capex_tot"](10000.0, 750.0, -0.01)

    def test_lcoe_demo(self):
        e_m, e_b, c_m, c_b, ox, lm, lb = _demo_lcoe()
        assert e_m == pytest.approx(E_MONO)
        assert e_b == pytest.approx(E_BIF)
        assert c_m == pytest.approx(CAPEX_MONO)
        assert c_b == pytest.approx(CAPEX_BIF)
        assert ox == pytest.approx(OPEX_A)
        assert lm == pytest.approx(LCOE_MONO, rel=1e-9)
        assert lb == pytest.approx(LCOE_BIF, rel=1e-9)
        with pytest.raises(ValueError):
            _F["mh613_lcoe"](c_m, ox, 0.0, 0.05, 25)

    def test_delta_e_breakeven(self):
        assert _F["mh613_delta_lcoe"](LCOE_MONO, LCOE_BIF) == \
            pytest.approx(DELTA, rel=1e-9)
        assert _F["mh613_gain_breakeven"](750.0, 0.04, 12.0, 0.05, 25) == \
            pytest.approx(GSTAR, rel=1e-9)
        # senza sovrapprezzo il break-even e' a gain nullo
        assert _F["mh613_gain_breakeven"](750.0, 0.0, 12.0, 0.05, 25) == 0.0
        # coerenza: LCOE_bif(g*) = LCOE_mono entro tolleranza
        d = DEMO
        e_star = _F["mh613_energia_annua"](d["pot_kwp"], d["yield_kwh_kwp"],
                                           GSTAR)
        c_b = _F["mh613_capex_tot"](d["pot_kwp"], d["capex_mono_kwp"],
                                    d["premium"])
        ox = _F["mh613_opex_annuo"](d["pot_kwp"], d["opex_kwp"])
        assert _F["mh613_lcoe"](c_b, ox, e_star, d["tasso"], d["anni"]) == \
            pytest.approx(LCOE_MONO, rel=1e-9)

    def test_verdetto(self):
        assert _F["mh613_verdetto"](DELTA)["verdetto"] == "CONVIENE"
        assert _F["mh613_verdetto"](1.0)["verdetto"] == "CONVIENE"
        assert _F["mh613_verdetto"](0.5)["verdetto"] == "MARGINALE"
        assert _F["mh613_verdetto"](0.0)["verdetto"] == "NON_CONVIENE"
        assert _F["mh613_verdetto"](-2.0)["verdetto"] == "NON_CONVIENE"

    def test_demo_dict(self):
        assert DEMO["pot_kwp"] == 10000.0
        assert DEMO["anni"] == 25
        assert set(DEMO) == {"pot_kwp", "yield_kwh_kwp", "gain",
                             "capex_mono_kwp", "premium", "opex_kwp",
                             "tasso", "anni"}


class TestW613Sensitivita:
    def test_shape_e_spot(self):
        righe = _F["mh613_sensitivita"](10000.0, 1150.0, 750.0, 12.0,
                                        0.05, 25, [0.0, 0.08], [0.0, 0.04])
        assert len(righe) == 4
        m = {(r["gain"], r["premium"]): r["delta_lcoe"] for r in righe}
        # gain 0, premium 4 % -> solo costo, delta negativo
        assert m[(0.0, 0.04)] == pytest.approx(-1.8509336686755589,
                                              rel=1e-9)
        # gain 8 %, premium 0 -> tutto guadagno
        assert m[(0.08, 0.0)] == pytest.approx(4.200601801895154, rel=1e-9)
        # demo: gain 8 %, premium 4 %
        assert m[(0.08, 0.04)] == pytest.approx(DELTA, rel=1e-9)

    def test_monotonia(self):
        righe = _F["mh613_sensitivita"](10000.0, 1150.0, 750.0, 12.0,
                                        0.05, 25,
                                        [0.0, 0.05, 0.10, 0.15],
                                        [0.04])
        ds = [r["delta_lcoe"] for r in righe]
        assert ds == sorted(ds)  # delta cresce col gain
        righe2 = _F["mh613_sensitivita"](10000.0, 1150.0, 750.0, 12.0,
                                         0.05, 25, [0.08],
                                         [0.0, 0.04, 0.08, 0.12])
        ds2 = [r["delta_lcoe"] for r in righe2]
        assert ds2 == sorted(ds2, reverse=True)  # delta cala col premium

    def test_liste_vuote(self):
        with pytest.raises(ValueError):
            _F["mh613_sensitivita"](10000.0, 1150.0, 750.0, 12.0, 0.05, 25,
                                    [], [0.04])


class TestW613Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def _ui(self):
        return self._src().split("with tab613:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 647
        assert TITLE613 in titles
        assert TITLE613 in titles

    def test_chain(self):
        assert ", tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647 = st.tabs([" in self._src()
        assert "with tab613:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st613_[a-z0-9_]+", self._ui()))
        attese = {"st613_pot", "st613_yield", "st613_gain", "st613_cxm",
                  "st613_prem", "st613_opex", "st613_tasso", "st613_anni",
                  "st613_tab", "st613_graf", "st613_go", "st613_fig",
                  "st613_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st613_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        sec = self._src().split('# W613 (21/10/2026)')[1]
        sec = sec.split('# W612 (21/10/2026)')[0]
        for w in ("api_key", "apikey", "password", "passwd", "secret",
                  "token"):
            assert w not in sec.lower(), f"sospetto segreto: {w}"
