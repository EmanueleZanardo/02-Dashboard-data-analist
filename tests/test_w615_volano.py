"""Test tab615 "🌀 Volano (flywheel): accumulo cinetico per FCR e servizi di rete".

I valori della demo sono calcolati a mano (script indipendente) e
contro-verificati per plausibilita': volano 1 MW / 0,25 MWh, capex
1500 eur/kW, opex 2 % capex, standby 3 % Pn, energia 80 eur/MWh,
FCR 28 eur/MW/h, disponibilita' 95 %, tasso 6 %, 20 anni ->
capex 1,5 mln, standby 262,8 MWh/anno (21.024 eur/anno), opex
30.000 eur/anno, ricavo FCR 233.016 eur/anno, margine 181.992
eur/anno, VAN 587.434 eur, TIR ~10,48 %, payback anno 9, costo
livellato FCR 21,8458 eur/MW/h, margine di sicurezza 28,17 %
-> CONVIENE.
"""

import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh615_num", "mh615_nneg", "mh615_pos", "mh615_frac01",
           "mh615_intero", "mh615_capex", "mh615_energia_standby",
           "mh615_costo_standby", "mh615_opex_annuo", "mh615_ricavo_fcr",
           "mh615_margine_annuo", "mh615_factor", "mh615_flussi",
           "mh615_van", "mh615_tir", "mh615_payback",
           "mh615_costo_fcr_livellato", "mh615_verdetto",
           "mh615_sensitivita", "mh615_demo")

TITLE615 = "🌀 Volano (flywheel): accumulo cinetico per FCR e servizi di rete"

# Demo: 1 MW, capex 1500 eur/kW, opex 2 %, standby 3 %, energia 80,
# FCR 28 eur/MW/h, disp 95 %, tasso 6 %, 20 anni
DEMO = _F["mh615_demo"]()
FACTOR = 11.469921218565263    # (1 - 1,06^-20)/0,06
CAPEX = 1500000.0              # 1*1000*1500
E_STANDBY = 262.8              # 1*0,03*8760 MWh
C_STANDBY = 21024.0            # 262,8*80
OPEX = 30000.0                # 1,5 mln*0,02
RICAVO = 233016.0              # 1*28*0,95*8760
MARGINE = 181992.0             # 233016-30000-21024
VAN = 587433.9024091291        # -1,5 mln + 181992*FACTOR
C_LIV = 21.845810558192394     # VAN(costi)/VAN(MW-anni)/8760
MS = 0.28171028149375416       # (28-21,8458)/21,8458
TIR = 0.10479633797386244      # bisezione sui flussi demo
PAYBACK = 9


class TestW615Validatori:
    def test_num(self):
        assert _F["mh615_num"](3, "x") == 3.0
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh615_num"](bad, "x")

    def test_nneg(self):
        assert _F["mh615_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh615_nneg"](-1.0, "x")

    def test_pos(self):
        with pytest.raises(ValueError):
            _F["mh615_pos"](0.0, "x")
        with pytest.raises(ValueError):
            _F["mh615_pos"](-2.0, "x")

    def test_frac01(self):
        assert _F["mh615_frac01"](1.0, "x") == 1.0
        assert _F["mh615_frac01"](0.0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh615_frac01"](1.0001, "x")
        with pytest.raises(ValueError):
            _F["mh615_frac01"](-0.1, "x")

    def test_intero(self):
        assert _F["mh615_intero"](20, "x", 1, 40) == 20
        assert _F["mh615_intero"](20.0, "x", 1, 40) == 20
        for bad in (True, 20.5, 0, 41):
            with pytest.raises(ValueError):
                _F["mh615_intero"](bad, "x", 1, 40)


class TestW615Modello:
    def test_capex(self):
        assert _F["mh615_capex"](1.0, 1500.0) == CAPEX
        assert _F["mh615_capex"](2.5, 1000.0) == 2500000.0

    def test_energia_standby(self):
        assert _F["mh615_energia_standby"](1.0, 0.03) == \
            pytest.approx(E_STANDBY)
        assert _F["mh615_energia_standby"](1.0, 0.0) == 0.0

    def test_costo_standby(self):
        assert _F["mh615_costo_standby"](1.0, 0.03, 80.0) == \
            pytest.approx(C_STANDBY)

    def test_opex(self):
        assert _F["mh615_opex_annuo"](CAPEX, 0.02) == pytest.approx(OPEX)

    def test_ricavo_fcr(self):
        assert _F["mh615_ricavo_fcr"](1.0, 28.0, 0.95) == \
            pytest.approx(RICAVO)
        assert _F["mh615_ricavo_fcr"](1.0, 28.0, 0.0) == 0.0

    def test_margine(self):
        assert _F["mh615_margine_annuo"](RICAVO, OPEX, C_STANDBY) == \
            pytest.approx(MARGINE)

    def test_factor(self):
        assert _F["mh615_factor"](0.0, 20) == 20.0
        assert _F["mh615_factor"](0.06, 20) == pytest.approx(FACTOR)

    def test_flussi(self):
        fl = _F["mh615_flussi"](CAPEX, MARGINE, 20)
        assert len(fl) == 21
        assert fl[0] == -CAPEX
        assert all(f == MARGINE for f in fl[1:])

    def test_van(self):
        fl = _F["mh615_flussi"](CAPEX, MARGINE, 20)
        assert _F["mh615_van"](fl, 0.06) == pytest.approx(VAN)
        with pytest.raises(ValueError):
            _F["mh615_van"]([], 0.06)

    def test_tir(self):
        fl = _F["mh615_flussi"](CAPEX, MARGINE, 20)
        tir = _F["mh615_tir"](fl)
        assert tir == pytest.approx(TIR, rel=1e-4)
        # flussi a segno costante -> None (lezione tab611)
        assert _F["mh615_tir"]([-100.0, -10.0, -5.0]) is None
        assert _F["mh615_tir"]([-100.0, 10.0, 5.0]) is not None
        with pytest.raises(ValueError):
            _F["mh615_tir"]([])

    def test_payback(self):
        fl = _F["mh615_flussi"](CAPEX, MARGINE, 20)
        assert _F["mh615_payback"](fl) == PAYBACK
        assert _F["mh615_payback"]([-100.0, 1.0, 1.0]) is None

    def test_costo_fcr_livellato(self):
        c = _F["mh615_costo_fcr_livellato"](CAPEX, OPEX, C_STANDBY,
                                            1.0, 0.95, 0.06, 20)
        assert c == pytest.approx(C_LIV)

    def test_demo(self):
        d = DEMO
        assert d["potenza_mw"] == 1.0
        assert d["energia_mwh"] == 0.25
        assert d["capex_kw"] == 1500.0
        assert d["opex_frac"] == 0.02
        assert d["standby_frac"] == 0.03
        assert d["prezzo_mwh"] == 80.0
        assert d["prezzo_fcr"] == 28.0
        assert d["disponibilita"] == 0.95
        assert d["tasso"] == 0.06
        assert d["anni"] == 20


class TestW615Verdetto:
    def test_conviene_demo(self):
        v = _F["mh615_verdetto"](28.0, C_LIV)
        assert v["verdetto"] == "CONVIENE"
        assert v["margine_sicurezza"] == pytest.approx(MS)
        assert "msg" in v

    def test_marginale(self):
        v = _F["mh615_verdetto"](C_LIV * 1.10, C_LIV)
        assert v["verdetto"] == "MARGINALE"

    def test_non_conviene(self):
        v = _F["mh615_verdetto"](C_LIV * 0.90, C_LIV)
        assert v["verdetto"] == "NON_CONVIENE"

    def test_bordi(self):
        # margine esattamente 15 % -> CONVIENE
        v = _F["mh615_verdetto"](C_LIV * 1.15, C_LIV)
        assert v["verdetto"] == "CONVIENE"
        # break-even esatto -> MARGINALE
        v2 = _F["mh615_verdetto"](C_LIV, C_LIV)
        assert v2["verdetto"] == "MARGINALE"


class TestW615Sensitivita:
    def _args(self):
        d = DEMO
        return (d["potenza_mw"], d["energia_mwh"], d["opex_frac"],
                d["standby_frac"], d["prezzo_mwh"], d["disponibilita"],
                d["tasso"], d["anni"])

    def test_shape_e_chiavi(self):
        rows = _F["mh615_sensitivita"](*self._args(), [20.0, 28.0],
                                       [1200.0, 1500.0])
        assert len(rows) == 4
        attese = {"prezzo_fcr", "capex_kw", "costo_fcr",
                  "margine_sicurezza", "van", "verdetto"}
        assert set(rows[0].keys()) == attese

    def test_valori_riga(self):
        rows = _F["mh615_sensitivita"](*self._args(), [28.0], [1500.0])
        r = rows[0]
        # il costo livellato non dipende dal prezzo FCR
        assert r["costo_fcr"] == pytest.approx(C_LIV)
        assert r["margine_sicurezza"] == pytest.approx(MS)
        assert r["van"] == pytest.approx(VAN)
        assert r["verdetto"] == "CONVIENE"

    def test_costo_livellato_cresce_col_capex(self):
        rows = _F["mh615_sensitivita"](*self._args(), [28.0],
                                       [1200.0, 2500.0])
        assert rows[0]["costo_fcr"] < rows[1]["costo_fcr"]

    def test_liste_vuote(self):
        with pytest.raises(ValueError):
            _F["mh615_sensitivita"](*self._args(), [], [1500.0])
        with pytest.raises(ValueError):
            _F["mh615_sensitivita"](*self._args(), [28.0], [])


class TestW615Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def _ui(self):
        return self._src().split("with tab615:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 751
        assert TITLE615 in titles
        assert TITLE615 in titles

    def test_chain(self):
        assert ", tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751 = st.tabs([" in self._src()
        assert "with tab615:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st615_[a-z0-9_]+", self._ui()))
        attese = {"st615_pot", "st615_en", "st615_capex", "st615_opex",
                  "st615_standby", "st615_pel", "st615_pfcr", "st615_disp",
                  "st615_tasso", "st615_anni", "st615_tab", "st615_graf",
                  "st615_go", "st615_fig", "st615_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st615_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        sec = self._src().split('# W615 (21/10/2026)')[1]
        sec = sec.split('# W614 (21/10/2026)')[0]
        for w in ("api_key", "apikey", "password", "passwd", "secret",
                  "token"):
            assert w not in sec.lower(), f"sospetto segreto: {w}"
