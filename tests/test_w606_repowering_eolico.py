"""Test tab606 "🌬️♻️ Repowering eolico: più MWh dagli stessi MW".

Tutti i valori attesi sono calcolati a mano nei commenti (aritmetica
indipendente dagli helper) e contro-verificati con gli helper stessi.
"""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh606_num", "mh606_nneg", "mh606_pos", "mh606_pct",
           "mh606_str", "mh606_aep", "mh606_delta_aep", "mh606_opex_tot",
           "mh606_flusso_rep", "mh606_investimento_rep",
           "mh606_rendita_attuale", "mh606_van_rep", "mh606_payback",
           "mh606_crf", "mh606_lcoe", "mh606_flusso_ext", "mh606_van_ext",
           "mh606_verdetto", "mh606_sensibilita_prezzo", "mh606_demo")

TITLE606 = "🌬️♻️ Repowering eolico: più MWh dagli stessi MW"

DEMO = _F["mh606_demo"]()
# Demo: vecchio 20 MW CF 22% opex 45 k€/MW; nuovo 24 MW CF 32%,
# capex 1,2 M€/MW, dismissione 80 k€/MW, opex 35 k€/MW, vita 25 a;
# estensione: capex 600 k€/MW, 8 anni extra, opex 70 k€/MW;
# WACC 6%, prezzo 100 €/MWh.
# AEP_old = 20*0,22*8760 = 38544,0 MWh
# AEP_new = 24*0,32*8760 = 67276,8 MWh ; ΔE = 28732,8 MWh
# O&M_old = 900000 € ; O&M_new = 840000 €
# F_rep = 28732,8*100 - (840000-900000) = 2873280 + 60000 = 2933280,0 €
# I_rep = 1200000*24 + 80000*20 = 30400000,0 €
# a(6%,25) = (1-1,06^-25)/0,06 = 12,783356158268413
# VAN_rep = -30400000 + 2933280*12,783356158268413 = 7097162,951925576 €
# payback = 30400000/2933280 = 10,363824796814486 a
# CRF(6%,25) = 0,07822671821227395
# LCOE_new = (1200000*0,07822671821227395+35000)/(0,32*8760)
#          = 128872,06185472874/2803,2 = 45,973195581738274 €/MWh
# F_ext = 38544*100 - 70000*20 = 2454400,0 €
# a(6%,8) = 6,2097938109695585
# VAN_ext = -600000*20 + 2454400*6,2097938109695585 = 3241317,929643687 €
# LCOE_ext = (600000*CRF(6%,8)+70000)/(0,22*8760) ; CRF(6%,8)=0,1610359428...
#          = 166621,5657/1927,2 = 86,45784847907709 €/MWh
# verdetto: VAN_rep > 0 e > VAN_ext -> REPOWER_CONVIENE
AEP_OLD = 38544.0
AEP_NEW = 67276.8
DELTA_E = 28732.800000000003
F_REP = 2933280.0000000005
INV_REP = 30400000.0
VAN_REP = 7097162.951925576
PAYBACK = 10.363824796814486
LCOE_NEW = 45.973195581738274
F_EXT = 2454400.0
VAN_EXT = 3241317.929643687
LCOE_EXT = 86.45784847907709
# sensibilita' prezzo [60, 80, 100, 120, 140]:
# p=60:  F_rep=1785024 -> VAN_rep=-7594901,681046214 ;
#        F_ext=912640  -> VAN_ext=-6332693,776356742 -> DISMISSIONE
# p=80:  F_rep=2359152 -> VAN_rep=-248869,36456032097 ;
#        F_ext=1684480 -> VAN_ext=-1545687,9233565275 -> DISMISSIONE
# p=100: REPOWER_CONVIENE ; p=120: REPOWER_CONVIENE ; p=140: REPOWER_CONVIENE
S60_VR = -7594901.681046214
S60_VX = -6332693.776356742
S80_VR = -248869.36456032097
S80_VX = -1545687.9233565275
S140_VR = 21789227.58489736
S140_VX = 12815329.635644112


class TestW606Validatori:
    def test_num(self):
        assert _F["mh606_num"](3, "x") == 3.0
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh606_num"](bad, "x")

    def test_nneg_pos_pct(self):
        assert _F["mh606_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh606_nneg"](-0.1, "x")
        with pytest.raises(ValueError):
            _F["mh606_pos"](0, "x")
        assert _F["mh606_pct"](100, "x") == 100.0
        with pytest.raises(ValueError):
            _F["mh606_pct"](100.1, "x")

    def test_str(self):
        assert _F["mh606_str"]("a", "x") == "a"
        with pytest.raises(ValueError):
            _F["mh606_str"](1, "x")


class TestW606Calcoli:
    def test_aep(self):
        assert _F["mh606_aep"](20.0, 22.0) == AEP_OLD
        assert _F["mh606_aep"](24.0, 32.0) == AEP_NEW
        assert _F["mh606_aep"](10.0, 0.0) == 0.0

    def test_delta_aep(self):
        assert _F["mh606_delta_aep"](AEP_NEW, AEP_OLD) == DELTA_E
        # il repowering può anche perdere energia (turbine più piccole)
        assert _F["mh606_delta_aep"](100.0, 200.0) == -100.0

    def test_opex_tot(self):
        assert _F["mh606_opex_tot"](45000.0, 20.0) == 900000.0
        assert _F["mh606_opex_tot"](35000.0, 24.0) == 840000.0

    def test_flusso_rep(self):
        assert _F["mh606_flusso_rep"](DELTA_E, 100.0, 840000.0,
                                      900000.0) == F_REP

    def test_investimento_rep(self):
        assert _F["mh606_investimento_rep"](1200000.0, 24.0, 80000.0,
                                            20.0) == INV_REP

    def test_rendita_attuale(self):
        assert _F["mh606_rendita_attuale"](2933280.0, 6.0,
                                           25) == 2933280.0 * 12.783356158268413
        # tasso zero: rendita = flusso * anni
        assert _F["mh606_rendita_attuale"](1000.0, 0.0, 10) == 10000.0

    def test_van_rep(self):
        assert _F["mh606_van_rep"](INV_REP, F_REP, 6.0, 25) == VAN_REP

    def test_payback(self):
        assert _F["mh606_payback"](INV_REP, F_REP) == PAYBACK
        assert _F["mh606_payback"](1e6, 0.0) is None
        assert _F["mh606_payback"](1e6, -5.0) is None

    def test_crf(self):
        assert _F["mh606_crf"](6.0, 25) == 0.07822671821227395
        assert _F["mh606_crf"](0.0, 10) == 0.1

    def test_lcoe(self):
        assert _F["mh606_lcoe"](1200000.0, 35000.0, 32.0, 6.0,
                                25) == LCOE_NEW
        assert _F["mh606_lcoe"](600000.0, 70000.0, 22.0, 6.0,
                                8) == LCOE_EXT
        with pytest.raises(ValueError):
            _F["mh606_lcoe"](1200000.0, 35000.0, 0.0, 6.0, 25)

    def test_flusso_ext(self):
        assert _F["mh606_flusso_ext"](AEP_OLD, 100.0, 70000.0,
                                      20.0) == F_EXT

    def test_van_ext(self):
        assert _F["mh606_van_ext"](600000.0, 20.0, F_EXT, 6.0,
                                   8) == VAN_EXT


class TestW606Verdetto:
    def test_repower_conviene(self):
        v = _F["mh606_verdetto"](VAN_REP, VAN_EXT)
        assert v["verdetto"] == "REPOWER_CONVIENE"
        assert "msg" in v

    def test_estensione_meglio(self):
        v = _F["mh606_verdetto"](1.0, 2.0)
        assert v["verdetto"] == "ESTENSIONE_MEGLIO"

    def test_pareggio_vince_repower(self):
        v = _F["mh606_verdetto"](5.0, 5.0)
        assert v["verdetto"] == "REPOWER_CONVIENE"

    def test_dismissione(self):
        v = _F["mh606_verdetto"](-10.0, -5.0)
        assert v["verdetto"] == "DISMISSIONE"
        v2 = _F["mh606_verdetto"](0.0, 0.0)
        assert v2["verdetto"] == "DISMISSIONE"


class TestW606Sensibilita:
    def test_righe(self):
        righe = _F["mh606_sensibilita_prezzo"](
            20.0, 22.0, 45000.0, 24.0, 32.0, 1200000.0, 80000.0, 35000.0,
            25, 600000.0, 8, 70000.0, 6.0, [60.0, 80.0, 100.0, 120.0,
                                            140.0])
        assert len(righe) == 5
        assert righe[0]["prezzo"] == 60.0
        assert righe[0]["van_rep"] == S60_VR
        assert righe[0]["van_ext"] == S60_VX
        assert righe[0]["verdetto"] == "DISMISSIONE"
        assert righe[1]["van_rep"] == S80_VR
        assert righe[1]["van_ext"] == S80_VX
        assert righe[1]["verdetto"] == "DISMISSIONE"
        assert righe[2]["van_rep"] == VAN_REP
        assert righe[2]["verdetto"] == "REPOWER_CONVIENE"
        assert righe[4]["van_rep"] == S140_VR
        assert righe[4]["van_ext"] == S140_VX
        assert righe[4]["verdetto"] == "REPOWER_CONVIENE"

    def test_lista_vuota(self):
        with pytest.raises(ValueError):
            _F["mh606_sensibilita_prezzo"](
                20.0, 22.0, 45000.0, 24.0, 32.0, 1200000.0, 80000.0,
                35000.0, 25, 600000.0, 8, 70000.0, 6.0, [])

    def test_demo(self):
        d = DEMO
        assert d["p_old"] == 20.0
        assert d["cf_new"] == 32.0
        assert d["prezzo"] == 100.0
        assert d["wacc_pct"] == 6.0


class TestW606Registro:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def _ui(self):
        return self._src().split("with tab606:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 719
        assert TITLE606 in titles
        assert TITLE606 in titles

    def test_chain(self):
        assert ", tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719 = st.tabs([" in self._src()
        assert "with tab606:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st606_[a-z0-9_]+", self._ui()))
        attese = {"st606_pold", "st606_cfold", "st606_opexold",
                  "st606_pnew", "st606_cfnew", "st606_capexnew",
                  "st606_dismiss", "st606_opexnew", "st606_vitanew",
                  "st606_capexext", "st606_anniext", "st606_opexext",
                  "st606_prezzo", "st606_wacc", "st606_tabc", "st606_graf",
                  "st606_go", "st606_tab", "st606_tab2", "st606_chart",
                  "st606_csv"}
        assert keys == attese, keys ^ attese

    def test_helpers(self):
        src = self._src()
        mh = set(re.findall(r"def (mh606_\w+)\(", src))
        attesi = {"mh606_num", "mh606_nneg", "mh606_pos", "mh606_pct",
                  "mh606_str", "mh606_aep", "mh606_delta_aep",
                  "mh606_opex_tot", "mh606_flusso_rep",
                  "mh606_investimento_rep", "mh606_rendita_attuale",
                  "mh606_van_rep", "mh606_payback", "mh606_crf",
                  "mh606_lcoe", "mh606_flusso_ext", "mh606_van_ext",
                  "mh606_verdetto", "mh606_sensibilita_prezzo",
                  "mh606_demo"}
        assert mh == attesi, (mh ^ attesi)

    def test_no_secrets(self):
        src = self._ui().lower()
        for pat in ("api_key", "apikey", "password", "secret"):
            assert pat not in src, pat
