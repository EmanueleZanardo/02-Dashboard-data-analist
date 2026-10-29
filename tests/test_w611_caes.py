"""Test tab611 "🌬️📦 CAES: l'accumulo ad aria compressa".

I valori della demo sono calcolati a mano (script indipendente) e
contro-verificati per plausibilita': adiabatico 100 MW x 8 h/giorno,
eta 68 %, spread 40 -> 120 eur/MWh, capex 128 Meur -> VAN +82,7 Meur
al 6 %, TIR ~11,5 %, payback anno 9, LCOS ~99,4 eur/MWh.
"""

import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh611_num", "mh611_nneg", "mh611_pos", "mh611_frac01",
           "mh611_frac01_open", "mh611_ore", "mh611_intero", "mh611_tipo",
           "mh611_energia_scarica_giorno", "mh611_energia_carica_giorno",
           "mh611_margine_giorno", "mh611_capex", "mh611_flussi",
           "mh611_van", "mh611_tir", "mh611_payback", "mh611_lcos",
           "mh611_verdetto", "mh611_demo")

TITLE611 = "🌬️📦 CAES: l'accumulo ad aria compressa"

# Demo: adiabatico 100 MW, 8 h/giorno, eta 0,68, p_ch=40, p_dis=120,
# capex_kw=800, capex_kwh=60, opex 2 %, anni=30, tasso=6 %
DEMO = _F["mh611_demo"]()
E_DIS = 800.0                 # 100*8 MWh/giorno
E_CH = 1176.4705882352942     # 800/0,68 MWh/giorno
MARGINE_G = 48941.1764705882  # 800*120 - E_CH*40 eur/giorno
CAPEX = 128000000.0           # 100*1000*800 + 800*1000*60
FLUSSO_A = 15303529.411765    # MARGINE_G*365 - 0,02*CAPEX
VAN6 = 82650498.37            # FLUSSO_A * A(6 %, 30a) - CAPEX
TIR_DEMO = 0.11499422
PAYBACK = 9
LCOS = 99.436751


def _flussi_demo():
    d = DEMO
    return _F["mh611_flussi"](d["potenza_mw"], d["ore_scarica"], d["eta"],
                              d["tipo"], d["heat_rate"], d["p_dis"],
                              d["p_ch"], d["costo_fuel"], d["capex_kw"],
                              d["capex_kwh"], d["capex_fisso"],
                              d["opex_frac"], d["prezzo_cap_kw"],
                              d["cicli_giorno"], d["anni"])


class TestW611Validatori:
    def test_num(self):
        assert _F["mh611_num"](3, "x") == 3.0
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh611_num"](bad, "x")

    def test_nneg_pos(self):
        assert _F["mh611_nneg"](0, "x") == 0.0
        assert _F["mh611_pos"](0.5, "x") == 0.5
        with pytest.raises(ValueError):
            _F["mh611_nneg"](-0.1, "x")
        with pytest.raises(ValueError):
            _F["mh611_pos"](0, "x")

    def test_frac_ore_intero(self):
        assert _F["mh611_frac01"](1, "x") == 1.0
        with pytest.raises(ValueError):
            _F["mh611_frac01"](1.1, "x")
        with pytest.raises(ValueError):
            _F["mh611_frac01_open"](1.0, "x")
        assert _F["mh611_ore"](24, "x") == 24.0
        with pytest.raises(ValueError):
            _F["mh611_ore"](24.1, "x")
        assert _F["mh611_intero"](30.0, "x", 1, 60) == 30
        with pytest.raises(ValueError):
            _F["mh611_intero"](30.5, "x", 1, 60)
        with pytest.raises(ValueError):
            _F["mh611_intero"](61, "x", 1, 60)

    def test_tipo(self):
        assert _F["mh611_tipo"]("  Diabatico ") == "diabatico"
        assert _F["mh611_tipo"]("adiabatico") == "adiabatico"
        with pytest.raises(ValueError):
            _F["mh611_tipo"]("isentropico")
        with pytest.raises(ValueError):
            _F["mh611_tipo"](None)


class TestW611Modello:
    def test_energia_scarica(self):
        assert _F["mh611_energia_scarica_giorno"](100, 8) == E_DIS
        with pytest.raises(ValueError):
            _F["mh611_energia_scarica_giorno"](100, 25)

    def test_energia_carica_adiabatico(self):
        e_ch, e_fuel = _F["mh611_energia_carica_giorno"](
            E_DIS, 0.68, "adiabatico", 1.17)
        assert e_ch == pytest.approx(E_CH, rel=1e-9)
        assert e_fuel == 0.0

    def test_energia_carica_diabatico(self):
        # e_dis=400, eta=0,42, HR=1,17 -> E_fuel=468, E_ch=484,380952381
        e_ch, e_fuel = _F["mh611_energia_carica_giorno"](
            400.0, 0.42, "diabatico", 1.17)
        assert e_fuel == pytest.approx(468.0, rel=1e-9)
        assert e_ch == pytest.approx(484.380952381, rel=1e-9)

    def test_energia_carica_rifiuta_eta_bassa(self):
        # 1/0,9 = 1,111 < 1,17 -> E_ch negativa
        with pytest.raises(ValueError):
            _F["mh611_energia_carica_giorno"](400.0, 0.9, "diabatico", 1.17)

    def test_margine_giorno(self):
        mg = _F["mh611_margine_giorno"](E_DIS, E_CH, 0.0, 120.0, 40.0, 30.0)
        assert mg == pytest.approx(MARGINE_G, rel=1e-9)
        # diabatico: 400*120 - 484,380952381*40 - 468*30 = 14584,7619
        mg2 = _F["mh611_margine_giorno"](400.0, 484.380952381, 468.0,
                                         120.0, 40.0, 30.0)
        assert mg2 == pytest.approx(14584.761905, rel=1e-6)

    def test_capex(self):
        assert _F["mh611_capex"](100.0, E_DIS, 800.0, 60.0, 0.0) == CAPEX

    def test_flussi_demo(self):
        fl = _flussi_demo()
        assert len(fl) == 31
        assert fl[0] == pytest.approx(-CAPEX)
        for f in fl[1:]:
            assert f == pytest.approx(FLUSSO_A, rel=1e-9)

    def test_van_demo(self):
        van = _F["mh611_van"](_flussi_demo(), 0.06)
        assert van == pytest.approx(VAN6, abs=1.0)

    def test_tir_demo(self):
        tir = _F["mh611_tir"](_flussi_demo())
        assert tir == pytest.approx(TIR_DEMO, abs=1e-4)

    def test_tir_none(self):
        assert _F["mh611_tir"]([0.0, 0.0, 0.0]) is None
        assert _F["mh611_tir"]([10.0, 5.0, 5.0]) is None
        assert _F["mh611_tir"]([-10.0, -5.0, -5.0]) is None

    def test_payback_demo(self):
        assert _F["mh611_payback"](_flussi_demo()) == PAYBACK

    def test_payback_none(self):
        assert _F["mh611_payback"]([-100.0, 1.0, 1.0]) is None

    def test_lcos_demo(self):
        costo_a = 0.02 * CAPEX + E_CH * 40.0 * 365.0
        lcos = _F["mh611_lcos"](CAPEX, costo_a, E_DIS * 365.0, 30, 0.06)
        assert lcos == pytest.approx(LCOS, abs=1e-3)

    def test_lcos_none(self):
        assert _F["mh611_lcos"](CAPEX, 100.0, 0.0, 30, 0.06) is None

    def test_verdetto(self):
        v = _F["mh611_verdetto"](VAN6, PAYBACK, 30)
        assert v["verdetto"] == "CONVIENE"
        assert _F["mh611_verdetto"](10.0, 40, 30)["verdetto"] == "MARGINALE"
        assert _F["mh611_verdetto"](-5.0, None, 30)["verdetto"] \
            == "NON_CONVIENE"

    def test_demo_dict(self):
        assert DEMO["tipo"] == "adiabatico"
        assert DEMO["anni"] == 30


class TestW611Registry:
    def _src(self):
        return (Path(__file__).resolve().parent.parent / "app.py") \
            .read_text(encoding="utf-8")

    def _ui(self):
        return self._src().split("with tab611:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 788
        assert TITLE611 in titles
        assert TITLE611 in titles

    def test_chain(self):
        assert ", tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788 = st.tabs([" in self._src()
        assert "with tab611:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st611_[a-z0-9_]+", self._ui()))
        attese = {"st611_pw", "st611_ore", "st611_eta", "st611_tipo",
                  "st611_hr", "st611_pdis", "st611_pch", "st611_fuel",
                  "st611_ckw", "st611_ckwh", "st611_cfix", "st611_opex",
                  "st611_cap", "st611_cicli", "st611_anni", "st611_tasso",
                  "st611_go", "st611_graf", "st611_tab", "st611_chart",
                  "st611_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st611_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        sec = self._src().split('# W611 (21/10/2026)')[1]
        sec = sec.split('# W610 (21/10/2026)')[0]
        for w in ("api_key", "apikey", "password", "passwd", "secret",
                  "token"):
            assert w not in sec.lower(), f"sospetto segreto: {w}"
