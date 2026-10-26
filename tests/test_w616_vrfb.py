"""Test tab616 "🔋🌊 Batterie a flusso (VRFB): accumulo long-duration".

I valori della demo sono calcolati a mano (script indipendente) e
contro-verificati per plausibilita': VRFB 2 MW / 6 h, capex 350
eur/kW + 180 eur/kWh, RTE 72 %, 330 cicli/anno, acquisto 45
eur/MWh, vendita 160 eur/MWh, capacita' 0, opex 1,5 % capex,
tasso 6 %, 25 anni ->
energia 12 MWh, capex 2,86 mln, scaricata 3.960 MWh/anno,
caricata 5.500 MWh/anno, ricavo vendita 633.600 eur/anno, costo
ricarica 247.500 eur/anno, opex 42.900 eur/anno, margine 343.200
eur/anno, VAN 1.527.248 eur, TIR ~11,15 %, payback anno 9, LCOS
129,83 eur/MWh, margine di sicurezza 23,24 % -> CONVIENE.
"""

import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh616_num", "mh616_nneg", "mh616_pos", "mh616_frac01",
           "mh616_intero", "mh616_energia_mwh", "mh616_capex",
           "mh616_energia_scaricata_annua", "mh616_energia_caricata_annua",
           "mh616_ricavo_vendita", "mh616_costo_ricarica",
           "mh616_ricavo_capacita", "mh616_opex_annuo",
           "mh616_margine_annuo", "mh616_factor", "mh616_flussi",
           "mh616_van", "mh616_tir", "mh616_payback", "mh616_lcos",
           "mh616_verdetto", "mh616_sensitivita", "mh616_demo")

TITLE616 = "🔋🌊 Batterie a flusso (VRFB): accumulo long-duration"

# Demo: 2 MW / 6 h, 350 eur/kW, 180 eur/kWh, RTE 72 %, 330 cicli,
# acquisto 45, vendita 160, capacita' 0, opex 1,5 %, tasso 6 %, 25 anni
DEMO = _F["mh616_demo"]()
ENERGIA = 12.0                 # 2*6
CAPEX = 2860000.0              # 2*1000*350 + 12*1000*180
E_SCAR = 3960.0                # 2*6*330
E_CAR = 5500.0                 # 3960/0,72
RIC_VEND = 633600.0            # 3960*160
COSTO_RIC = 247500.0           # 5500*45
OPEX = 42900.0                 # 2,86 mln*0,015
MARGINE = 343200.0             # 633600-247500-42900
FACTOR = 12.783356158268413    # (1 - 1,06^-25)/0,06
VAN = 1527247.833517719        # -2,86 mln + 343200*FACTOR
LCOS = 129.8304075977534       # VAN(costi)/VAN(MWh scaricati)
MS = 0.2323769366550818        # (160-129,8304)/129,8304
TIR = 0.11145080732360979      # bisezione sui flussi demo
PAYBACK = 9


class TestW616Validatori:
    def test_num(self):
        assert _F["mh616_num"](3, "x") == 3.0
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh616_num"](bad, "x")

    def test_nneg(self):
        assert _F["mh616_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh616_nneg"](-1.0, "x")

    def test_pos(self):
        with pytest.raises(ValueError):
            _F["mh616_pos"](0.0, "x")
        with pytest.raises(ValueError):
            _F["mh616_pos"](-2.0, "x")

    def test_frac01(self):
        assert _F["mh616_frac01"](1.0, "x") == 1.0
        assert _F["mh616_frac01"](0.0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh616_frac01"](1.5, "x")

    def test_intero(self):
        assert _F["mh616_intero"](25.0, "x", 1, 60) == 25
        with pytest.raises(ValueError):
            _F["mh616_intero"](2.5, "x", 1, 60)
        with pytest.raises(ValueError):
            _F["mh616_intero"](True, "x", 1, 60)
        with pytest.raises(ValueError):
            _F["mh616_intero"](0, "x", 1, 60)


class TestW616Calcoli:
    def test_energia_e_capex(self):
        assert _F["mh616_energia_mwh"](2.0, 6.0) == ENERGIA
        assert _F["mh616_capex"](2.0, 6.0, 350.0, 180.0) == CAPEX

    def test_energie_annue(self):
        assert _F["mh616_energia_scaricata_annua"](2.0, 6.0, 330.0) \
            == E_SCAR
        assert _F["mh616_energia_caricata_annua"](E_SCAR, 0.72) == E_CAR
        with pytest.raises(ValueError):
            _F["mh616_energia_caricata_annua"](E_SCAR, 0.0)

    def test_ricavi_costi(self):
        assert _F["mh616_ricavo_vendita"](E_SCAR, 160.0) == RIC_VEND
        assert _F["mh616_costo_ricarica"](E_CAR, 45.0) == COSTO_RIC
        assert _F["mh616_ricavo_capacita"](2.0, 0.0) == 0.0
        assert _F["mh616_ricavo_capacita"](2.0, 5000.0) == 10000.0
        assert _F["mh616_opex_annuo"](CAPEX, 0.015) == OPEX
        assert _F["mh616_margine_annuo"](RIC_VEND, 0.0, COSTO_RIC,
                                         OPEX) == MARGINE

    def test_factor(self):
        assert _F["mh616_factor"](0.06, 25) == pytest.approx(FACTOR)
        assert _F["mh616_factor"](0.0, 25) == 25.0

    def test_flussi_van(self):
        fl = _F["mh616_flussi"](CAPEX, MARGINE, 25)
        assert fl[0] == -CAPEX and len(fl) == 26
        assert all(f == MARGINE for f in fl[1:])
        assert _F["mh616_van"](fl, 0.06) == pytest.approx(VAN)

    def test_tir(self):
        fl = _F["mh616_flussi"](CAPEX, MARGINE, 25)
        assert _F["mh616_tir"](fl) == pytest.approx(TIR)
        # TIR > 100 % (estremo superiore espanso)
        assert _F["mh616_tir"]([-100.0, 300.0]) == pytest.approx(2.0)
        # TIR negativo
        assert _F["mh616_tir"]([-100.0, 90.0]) == pytest.approx(-0.1)
        # nessun cambio di segno -> None
        assert _F["mh616_tir"]([-100.0, -10.0]) is None
        assert _F["mh616_tir"]([100.0, 10.0]) is None
        assert _F["mh616_tir"]([]) is None

    def test_payback(self):
        fl = _F["mh616_flussi"](CAPEX, MARGINE, 25)
        assert _F["mh616_payback"](fl) == PAYBACK
        assert _F["mh616_payback"]([-100.0, 10.0, 10.0]) is None

    def test_lcos(self):
        lc = _F["mh616_lcos"](CAPEX, OPEX, COSTO_RIC, E_SCAR, 0.06, 25)
        assert lc == pytest.approx(LCOS)
        with pytest.raises(ValueError):
            _F["mh616_lcos"](CAPEX, OPEX, COSTO_RIC, 0.0, 0.06, 25)

    def test_verdetto(self):
        v = _F["mh616_verdetto"](160.0, LCOS)
        assert v["verdetto"] == "CONVIENE"
        assert v["margine_sicurezza"] == pytest.approx(MS)
        v2 = _F["mh616_verdetto"](LCOS * 1.05, LCOS)
        assert v2["verdetto"] == "MARGINALE"
        v3 = _F["mh616_verdetto"](LCOS * 0.9, LCOS)
        assert v3["verdetto"] == "NON_CONVIENE"


class TestW616Demo:
    def _p(self):
        d = DEMO
        cx = _F["mh616_capex"](d["potenza_mw"], d["durata_h"],
                               d["capex_kw"], d["capex_kwh"])
        ed = _F["mh616_energia_scaricata_annua"](d["potenza_mw"],
                                                 d["durata_h"],
                                                 d["cicli_anno"])
        ech = _F["mh616_energia_caricata_annua"](ed, d["rte"])
        rv = _F["mh616_ricavo_vendita"](ed, d["p_vendita"])
        cr = _F["mh616_costo_ricarica"](ech, d["p_acquisto"])
        ox = _F["mh616_opex_annuo"](cx, d["opex_frac"])
        mg = _F["mh616_margine_annuo"](
            rv, _F["mh616_ricavo_capacita"](d["potenza_mw"],
                                            d["eur_mw_anno"]), cr, ox)
        return cx, ed, ech, rv, cr, ox, mg

    def test_demo_end_to_end(self):
        cx, ed, ech, rv, cr, ox, mg = self._p()
        assert cx == CAPEX
        assert ed == E_SCAR
        assert ech == E_CAR
        assert rv == RIC_VEND
        assert cr == COSTO_RIC
        assert ox == OPEX
        assert mg == MARGINE
        d = DEMO
        fl = _F["mh616_flussi"](cx, mg, d["anni"])
        assert _F["mh616_van"](fl, d["tasso"]) == pytest.approx(VAN)
        assert _F["mh616_tir"](fl) == pytest.approx(TIR)
        assert _F["mh616_payback"](fl) == PAYBACK
        lc = _F["mh616_lcos"](cx, ox, cr, ed, d["tasso"], d["anni"])
        assert lc == pytest.approx(LCOS)
        v = _F["mh616_verdetto"](d["p_vendita"], lc)
        assert v["verdetto"] == "CONVIENE"


class TestW616Sensitivita:
    def _args(self):
        return (2.0, 6.0, 350.0, 0.015, 0.72, 330.0, 45.0, 0.0, 0.06, 25)

    def test_griglia(self):
        rows = _F["mh616_sensitivita"](*self._args(), [160.0], [180.0])
        assert len(rows) == 1
        r = rows[0]
        # il LCOS non dipende dal prezzo di vendita
        assert r["lcos"] == pytest.approx(LCOS)
        assert r["margine_sicurezza"] == pytest.approx(MS)
        assert r["van"] == pytest.approx(VAN)
        assert r["verdetto"] == "CONVIENE"

    def test_lcos_cresce_col_capex_energia(self):
        rows = _F["mh616_sensitivita"](*self._args(), [160.0],
                                       [120.0, 260.0])
        assert rows[0]["lcos"] < rows[1]["lcos"]
        assert rows[0]["capex"] < rows[1]["capex"]

    def test_liste_vuote(self):
        with pytest.raises(ValueError):
            _F["mh616_sensitivita"](*self._args(), [], [180.0])
        with pytest.raises(ValueError):
            _F["mh616_sensitivita"](*self._args(), [160.0], [])


class TestW616Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def _ui(self):
        return self._src().split("with tab616:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 723
        assert TITLE616 in titles
        assert TITLE616 in titles

    def test_chain(self):
        assert ", tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723 = st.tabs([" in self._src()
        assert "with tab616:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st616_[a-z0-9_]+", self._ui()))
        attese = {"st616_pot", "st616_dur", "st616_ckw", "st616_ckwh",
                  "st616_rte", "st616_cicli", "st616_pacq", "st616_pven",
                  "st616_cap", "st616_opex", "st616_tasso", "st616_anni",
                  "st616_tab", "st616_graf", "st616_go", "st616_fig",
                  "st616_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st616_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        sec = self._src().split('# W616 (21/10/2026)')[1]
        sec = sec.split('# W615 (21/10/2026)')[0]
        for w in ("api_key", "apikey", "password", "passwd", "secret",
                  "token"):
            assert w not in sec.lower(), f"sospetto segreto: {w}"
