"""Test tab625 "✈️⛽ Power-to-SAF: il cherosene sintetico da CO₂ (Fischer-Tropsch)".

Demo calcolata a mano: 100 kg/h x 4000 h -> 400.000 kg H2/anno;
stechiometria (12 x 44,009 / (37 x 2,016)) -> 2.831.981,9819819815 kg
CO2/anno; (12 x 12,011 + 26 x 1,008) / (37 x 2,016) x eta 0,90 ->
822,1042471042 t SAF/anno; LCOH 5,13 -> H2 2.052.000; CO2 a 100 €/t ->
283.198,1981981981; treno FT 250 €/t -> 205.526,0617760618; totale
2.540.724,2599742603; LCoS 3.090,5134828382 €/t contro benchmark 1.116
(fossile 800 + 3,16 x ETS 100) -> NON_CONVIENTE; Jet spostato
657.683,3976833978, CO2 valorizzata 259.784,9420849421, netto
1.623.255,9202059205 €/anno.
"""

import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh625_num", "mh625_nneg", "mh625_pos", "mh625_frac01",
           "mh625_kg_h2_annui", "mh625_kg_co2_annue", "mh625_t_saf_annue",
           "mh625_costo_h2", "mh625_costo_co2", "mh625_costo_sintesi",
           "mh625_costo_totale", "mh625_lcos", "mh625_jet_spostato",
           "mh625_valore_co2", "mh625_costo_netto", "mh625_benchmark",
           "mh625_verdetto", "mh625_sensibilita", "mh625_demo")

TITLE625 = ("✈️⛽ Power-to-SAF: il cherosene sintetico da CO₂ "
            "(Fischer-Tropsch)")

DEMO = _F["mh625_demo"]()
KG_DEMO = 400000.0
CO2_DEMO = 2831981.9819819815
SAF_DEMO = 822.1042471042472
CH2_DEMO = 2052000.0
CCO2_DEMO = 283198.1981981981
CSIN_DEMO = 205526.0617760618
TOT_DEMO = 2540724.2599742603
LCOS_DEMO = 3090.513482838245
BM_DEMO = 1116.0
SPOST_DEMO = 657683.3976833978
VC_DEMO = 259784.94208494213
NETTO_DEMO = 1623255.9202059205


class TestW625Validatori:
    def test_num(self):
        assert _F["mh625_num"](3, "x") == 3.0
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh625_num"](bad, "x")

    def test_nneg_pos_frac01(self):
        assert _F["mh625_nneg"](0, "x") == 0.0
        assert _F["mh625_pos"](0.001, "x") == 0.001
        assert _F["mh625_frac01"](1, "x") == 1.0
        for bad in (-1.0,):
            with pytest.raises(ValueError):
                _F["mh625_nneg"](bad, "x")
        with pytest.raises(ValueError):
            _F["mh625_pos"](0.0, "x")
        with pytest.raises(ValueError):
            _F["mh625_frac01"](1.5, "x")
        with pytest.raises(ValueError):
            _F["mh625_frac01"](-0.1, "x")


class TestW625Catena:
    def test_stechiometria(self):
        kg = _F["mh625_kg_h2_annui"](100.0, 4000.0)
        assert kg == pytest.approx(KG_DEMO)
        # 7,079955 kg CO2 per kg H2 (12 x 44,009 / (37 x 2,016))
        assert _F["mh625_kg_co2_annue"](kg) == pytest.approx(CO2_DEMO)
        # 2,283623 kg SAF per kg H2 x eta 0,90
        assert _F["mh625_t_saf_annue"](kg, 0.90) == pytest.approx(SAF_DEMO)

    def test_kg_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh625_kg_h2_annui"](0.0, 4000.0)

    def test_eta_fuori_intervallo(self):
        with pytest.raises(ValueError):
            _F["mh625_t_saf_annue"](KG_DEMO, 1.2)

    def test_eta_zero_niente_saf(self):
        assert _F["mh625_t_saf_annue"](KG_DEMO, 0.0) == 0.0

    def test_costi(self):
        assert _F["mh625_costo_h2"](KG_DEMO, 5.13) == \
            pytest.approx(CH2_DEMO)
        assert _F["mh625_costo_co2"](CO2_DEMO, 100.0) == \
            pytest.approx(CCO2_DEMO)
        assert _F["mh625_costo_sintesi"](SAF_DEMO, 250.0) == \
            pytest.approx(CSIN_DEMO)
        tot = _F["mh625_costo_totale"](CH2_DEMO, CCO2_DEMO, CSIN_DEMO)
        assert tot == pytest.approx(TOT_DEMO)


class TestW625Lcos:
    def test_lcos_demo(self):
        assert _F["mh625_lcos"](TOT_DEMO, SAF_DEMO) == \
            pytest.approx(LCOS_DEMO)

    def test_lcos_none_senza_saf(self):
        assert _F["mh625_lcos"](100.0, 0.0) is None

    def test_benchmark_demo(self):
        assert _F["mh625_benchmark"](800.0, 3.16, 100.0) == \
            pytest.approx(BM_DEMO)

    def test_spostato_e_valore(self):
        assert _F["mh625_jet_spostato"](SAF_DEMO, 800.0) == \
            pytest.approx(SPOST_DEMO)
        assert _F["mh625_valore_co2"](SAF_DEMO, 3.16, 100.0) == \
            pytest.approx(VC_DEMO)
        netto = _F["mh625_costo_netto"](TOT_DEMO, SPOST_DEMO, VC_DEMO)
        assert netto == pytest.approx(NETTO_DEMO)


class TestW625Verdetto:
    def test_conviente(self):
        v = _F["mh625_verdetto"](1000.0, 1116.0)
        assert v["verdetto"] == "CONVIENTE"
        assert v["lcos"] == pytest.approx(1000.0)

    def test_pareggio_conviente(self):
        assert _F["mh625_verdetto"](1116.0, 1116.0)["verdetto"] == \
            "CONVIENTE"

    def test_marginale_entro_15(self):
        v = _F["mh625_verdetto"](1200.0, 1116.0)
        assert v["verdetto"] == "MARGINALE"

    def test_non_conviente(self):
        v = _F["mh625_verdetto"](LCOS_DEMO, BM_DEMO)
        assert v["verdetto"] == "NON_CONVIENTE"

    def test_non_calcolabile(self):
        v = _F["mh625_verdetto"](None, 1116.0)
        assert v["verdetto"] == "NON_CALCOLABILE"


class TestW625Sensibilita:
    def test_geometria(self):
        rows = _F["mh625_sensibilita"](100.0, 4000.0, 0.90, 100.0, 250.0,
                                       800.0, 3.16, [2.0, 5.0],
                                       [60.0, 100.0])
        assert len(rows) == 4
        # riga estrema hand-computed: LCOH 2 -> lcos =
        # (400000*2 + 283198.20 + 205526.06) / 822,1042471042
        r0 = rows[0]
        assert r0["lcos"] == pytest.approx(
            (800000.0 + 283198.1981981981 + 205526.0617760618) / SAF_DEMO)
        assert r0["benchmark"] == pytest.approx(800.0 + 3.16 * 60.0)

    def test_monotonia_lcos(self):
        rows = _F["mh625_sensibilita"](100.0, 4000.0, 0.90, 100.0, 250.0,
                                       800.0, 3.16, [1.0, 5.0, 10.0],
                                       [100.0])
        lcoes = [r["lcos"] for r in rows]
        assert lcoes == sorted(lcoes)

    def test_giudizio_conviente_lcoh_basso(self):
        rows = _F["mh625_sensibilita"](100.0, 4000.0, 0.90, 100.0, 250.0,
                                       800.0, 3.16, [1.0], [300.0])
        assert rows[0]["giudizio"] == "CONVIENTE"

    def test_liste_vuote(self):
        with pytest.raises(ValueError):
            _F["mh625_sensibilita"](100.0, 4000.0, 0.90, 100.0, 250.0,
                                    800.0, 3.16, [], [100.0])
        with pytest.raises(ValueError):
            _F["mh625_sensibilita"](100.0, 4000.0, 0.90, 100.0, 250.0,
                                    800.0, 3.16, [5.0], [])

    def test_demo_catena_completa(self):
        d = DEMO
        kg = _F["mh625_kg_h2_annui"](d["portata_kg_h"], d["ore_annue"])
        co2 = _F["mh625_kg_co2_annue"](kg)
        saf = _F["mh625_t_saf_annue"](kg, d["eta_ft"])
        h2 = _F["mh625_costo_h2"](kg, d["lcoh_eur_kg"])
        c_co2 = _F["mh625_costo_co2"](co2, d["prezzo_co2_eur_t"])
        sin = _F["mh625_costo_sintesi"](
            saf, d["costo_ft_eur_t"])
        tot = _F["mh625_costo_totale"](h2, c_co2, sin)
        lcos = _F["mh625_lcos"](tot, saf)
        bm = _F["mh625_benchmark"](d["prezzo_fossile_eur_t"],
                                   d["ef_fossile_tco2_t"],
                                   d["prezzo_ets_eur_t"])
        ver = _F["mh625_verdetto"](lcos, bm)
        spost = _F["mh625_jet_spostato"](saf,
                                         d["prezzo_fossile_eur_t"])
        vc = _F["mh625_valore_co2"](saf, d["ef_fossile_tco2_t"],
                                    d["prezzo_ets_eur_t"])
        netto = _F["mh625_costo_netto"](tot, spost, vc)
        assert kg == pytest.approx(KG_DEMO)
        assert saf == pytest.approx(SAF_DEMO)
        assert tot == pytest.approx(TOT_DEMO)
        assert lcos == pytest.approx(LCOS_DEMO)
        assert bm == pytest.approx(BM_DEMO)
        assert ver["verdetto"] == "NON_CONVIENTE"
        assert netto == pytest.approx(NETTO_DEMO)


class TestW625Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def _ui(self):
        return self._src().split("with tab625:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 831
        assert TITLE625 in titles
        assert TITLE625 in titles

    def test_chain(self):
        assert ", tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790, tab791, tab792, tab793, tab794, tab795, tab796, tab797, tab798, tab799, tab800, tab801, tab802, tab803, tab804, tab805, tab806, tab807, tab808, tab809, tab810, tab811, tab812, tab813, tab814, tab815, tab816, tab817, tab818, tab819, tab820, tab821, tab822, tab823, tab824, tab825, tab826, tab827, tab828, tab829, tab830, tab831 = st.tabs([" in self._src()
        assert "with tab625:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st625_[a-z0-9_]+", self._ui()))
        attese = {"st625_port", "st625_ore", "st625_lcoh", "st625_eta",
                  "st625_pco2", "st625_sin", "st625_pf", "st625_ef",
                  "st625_ets", "st625_tab", "st625_graf", "st625_go",
                  "st625_fig", "st625_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st625_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        sec = self._src().split('# W625 (21/10/2026)')[1]
        sec = sec.split('# W624 (21/10/2026)')[0]
        for w in ("api_key", "apikey", "password", "passwd", "secret",
                  "token"):
            assert w not in sec.lower(), f"sospetto segreto: {w}"
