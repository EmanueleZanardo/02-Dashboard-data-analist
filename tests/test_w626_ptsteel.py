"""Test tab626 "🏭💚 Power-to-Steel: l'acciaio verde da H2 (DRI)".

Demo calcolata a mano: 100 kg/h x 4000 h -> 400.000 kg H2/anno;
stechiometria ((2 x 55,845) / (3 x 2,016)) x eta 0,95 ->
7.017,5595238095 t DRI/anno (54,149879 kg H2 per t); LCOH 5,13 ->
H2 2.052.000; impianto 120 €/t -> 842.107,1428571427; pellet 180
€/t -> 1.263.160,714285714; totale 4.157.267,857142857; LCoS
592,409347300564 €/t contro benchmark 760 (BF-BOF 600 + 1,6 x ETS
100) -> CONVIENTE; acciaio spostato 4.210.535,714285714, CO2
valorizzata 1.122.809,5238095238, netto -1.176.077,3809523806
€/anno.
"""

import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh626_num", "mh626_nneg", "mh626_pos", "mh626_frac01",
           "mh626_kg_h2_annui", "mh626_t_dri_annue",
           "mh626_costo_h2", "mh626_costo_impianto",
           "mh626_costo_pellet", "mh626_costo_totale", "mh626_lcos",
           "mh626_acciaio_spostato", "mh626_valore_co2",
           "mh626_costo_netto", "mh626_benchmark", "mh626_verdetto",
           "mh626_sensibilita", "mh626_demo")

TITLE626 = ("🏭💚 Power-to-Steel: l'acciaio verde da H2 (DRI)")

DEMO = _F["mh626_demo"]()
KG_DEMO = 400000.0
DRI_DEMO = 7017.559523809523
CH2_DEMO = 2052000.0
CIMP_DEMO = 842107.1428571427
CPEL_DEMO = 1263160.714285714
TOT_DEMO = 4157267.857142857
LCOS_DEMO = 592.409347300564
BM_DEMO = 760.0
SPOST_DEMO = 4210535.714285714
VC_DEMO = 1122809.5238095238
NETTO_DEMO = -1176077.3809523806


class TestW626Validatori:
    def test_num(self):
        assert _F["mh626_num"](3, "x") == 3.0
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh626_num"](bad, "x")

    def test_nneg_pos_frac01(self):
        assert _F["mh626_nneg"](0, "x") == 0.0
        assert _F["mh626_pos"](0.001, "x") == 0.001
        assert _F["mh626_frac01"](1, "x") == 1.0
        for bad in (-1.0,):
            with pytest.raises(ValueError):
                _F["mh626_nneg"](bad, "x")
        for bad in (0.0, -2.0):
            with pytest.raises(ValueError):
                _F["mh626_pos"](bad, "x")
        for bad in (-0.1, 1.1):
            with pytest.raises(ValueError):
                _F["mh626_frac01"](bad, "x")


class TestW626Catena:
    def test_kg_h2(self):
        assert _F["mh626_kg_h2_annui"](100.0, 4000.0) == KG_DEMO
        with pytest.raises(ValueError):
            _F["mh626_kg_h2_annui"](-1.0, 4000.0)

    def test_stechiometria(self):
        # 54,149879 kg H2 -> 1 t di DRI a eta' 1
        assert _F["mh626_t_dri_annue"](54.14987912973409, 1.0) == \
            pytest.approx(1.0)
        assert _F["mh626_t_dri_annue"](KG_DEMO, 0.95) == \
            pytest.approx(DRI_DEMO)
        with pytest.raises(ValueError):
            _F["mh626_t_dri_annue"](KG_DEMO, 1.5)

    def test_costi(self):
        dri = _F["mh626_t_dri_annue"](KG_DEMO, 0.95)
        assert _F["mh626_costo_h2"](KG_DEMO, 5.13) == CH2_DEMO
        assert _F["mh626_costo_impianto"](dri, 120.0) == \
            pytest.approx(CIMP_DEMO)
        assert _F["mh626_costo_pellet"](dri, 180.0) == \
            pytest.approx(CPEL_DEMO)
        tot = _F["mh626_costo_totale"](CH2_DEMO, CIMP_DEMO, CPEL_DEMO)
        assert tot == pytest.approx(TOT_DEMO)

    def test_lcos(self):
        assert _F["mh626_lcos"](TOT_DEMO, DRI_DEMO) == \
            pytest.approx(LCOS_DEMO)
        assert _F["mh626_lcos"](TOT_DEMO, 0.0) is None

    def test_spostato_valore_netto(self):
        assert _F["mh626_acciaio_spostato"](DRI_DEMO, 600.0) == \
            pytest.approx(SPOST_DEMO)
        assert _F["mh626_valore_co2"](DRI_DEMO, 1.6, 100.0) == \
            pytest.approx(VC_DEMO)
        assert _F["mh626_costo_netto"](TOT_DEMO, SPOST_DEMO,
                                       VC_DEMO) == pytest.approx(NETTO_DEMO)

    def test_benchmark(self):
        assert _F["mh626_benchmark"](600.0, 1.6, 100.0) == BM_DEMO
        assert _F["mh626_benchmark"](600.0, 0.0, 200.0) == 600.0

    def test_verdetto_stati(self):
        assert _F["mh626_verdetto"](LCOS_DEMO, BM_DEMO)["verdetto"] == \
            "CONVIENTE"
        assert _F["mh626_verdetto"](BM_DEMO, BM_DEMO)["verdetto"] == \
            "CONVIENTE"  # pareggio
        assert _F["mh626_verdetto"](BM_DEMO * 1.15, BM_DEMO)[
            "verdetto"] == "MARGINALE"  # soglia 1.15
        assert _F["mh626_verdetto"](BM_DEMO * 1.16, BM_DEMO)[
            "verdetto"] == "NON_CONVIENTE"
        assert _F["mh626_verdetto"](None, BM_DEMO)["verdetto"] == \
            "NON_CALCOLABILE"


class TestW626Sensibilita:
    def _args(self):
        return (100.0, 4000.0, 0.95, 120.0, 180.0, 600.0, 1.6)

    def test_geometria(self):
        rows = _F["mh626_sensibilita"](*self._args(), [2.0, 5.0],
                                       [60.0, 100.0])
        assert len(rows) == 4
        assert rows[0]["lcoh_eur_kg"] == 2.0
        assert rows[0]["ets_eur_t"] == 60.0

    def test_riga_estrema_hand_computed(self):
        # LCOH 2, ETS 60: H2 800.000; impianto+pellet = 7017,56*300;
        # LCoS = 2.905.267,86/7017,56 = 413,99974553628226; bm = 696
        rows = _F["mh626_sensibilita"](*self._args(), [2.0], [60.0])
        r = rows[0]
        assert r["lcos"] == pytest.approx(413.99974553628226)
        assert r["benchmark"] == pytest.approx(696.0)
        assert r["giudizio"] == "CONVIENTE"

    def test_monotonia_lcos(self):
        rows = _F["mh626_sensibilita"](*self._args(),
                                       [2.0, 5.0, 8.0], [100.0])
        lcos = [r["lcos"] for r in rows]
        assert lcos == sorted(lcos)

    def test_non_conviente_estremo(self):
        # LCOH 10, ETS 60: LCoS = 869,8 > bm 696 x 1.15 = 800,4
        rows = _F["mh626_sensibilita"](*self._args(), [10.0], [60.0])
        assert rows[0]["giudizio"] == "NON_CONVIENTE"

    def test_liste_vuote(self):
        assert _F["mh626_sensibilita"](*self._args(), [], [100.0]) == []
        assert _F["mh626_sensibilita"](*self._args(), [5.0], []) == []

    def test_demo_catena_completa(self):
        d = DEMO
        kg = _F["mh626_kg_h2_annui"](d["portata_kg_h"], d["ore_annue"])
        dri = _F["mh626_t_dri_annue"](kg, d["eta_dri"])
        ch2 = _F["mh626_costo_h2"](kg, d["lcoh_eur_kg"])
        cimp = _F["mh626_costo_impianto"](dri, d["costo_dri_eur_t"])
        cpel = _F["mh626_costo_pellet"](dri, d["costo_pellet_eur_t"])
        tot = _F["mh626_costo_totale"](ch2, cimp, cpel)
        lcos = _F["mh626_lcos"](tot, dri)
        bm = _F["mh626_benchmark"](d["prezzo_bfbof_eur_t"],
                                   d["ef_evitata_tco2_t"],
                                   d["prezzo_ets_eur_t"])
        spost = _F["mh626_acciaio_spostato"](dri,
                                             d["prezzo_bfbof_eur_t"])
        vc = _F["mh626_valore_co2"](dri, d["ef_evitata_tco2_t"],
                                    d["prezzo_ets_eur_t"])
        netto = _F["mh626_costo_netto"](tot, spost, vc)
        ver = _F["mh626_verdetto"](lcos, bm)
        assert kg == pytest.approx(KG_DEMO)
        assert dri == pytest.approx(DRI_DEMO)
        assert tot == pytest.approx(TOT_DEMO)
        assert lcos == pytest.approx(LCOS_DEMO)
        assert bm == pytest.approx(BM_DEMO)
        assert ver["verdetto"] == "CONVIENTE"
        assert netto == pytest.approx(NETTO_DEMO)


class TestW626Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def _ui(self):
        return self._src().split("with tab626:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 766
        assert TITLE626 in titles
        assert TITLE626 in titles

    def test_chain(self):
        assert ", tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766 = st.tabs([" in self._src()
        assert "with tab626:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st626_[a-z0-9_]+", self._ui()))
        attese = {"st626_port", "st626_ore", "st626_lcoh", "st626_eta",
                  "st626_imp", "st626_pel", "st626_pf", "st626_ef",
                  "st626_ets", "st626_tab", "st626_graf", "st626_go",
                  "st626_fig", "st626_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st626_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        sec = self._src().split('# W626 (21/10/2026)')[1]
        sec = sec.split('# W625 (21/10/2026)')[0]
        for w in ("api_key", "apikey", "password", "passwd", "secret",
                  "token"):
            assert w not in sec.lower(), f"sospetto segreto: {w}"
