"""Test tab623 "⚗️💚 Power-to-Ammonia: l'ammoniaca verde da H2 (Haber-Bosch)".

Demo calcolata a mano: 100 kg/h x 4000 h -> 400.000 kg H2/anno;
stechiometria (28,014 / (3 x 2,016)) -> 1.852,7777777777778 t N2/anno;
34,062 / (3 x 2,016) x eta 0,92 -> 2.072,5555555555557 t NH3/anno;
LCOH 5,13 -> H2 2.052.000; N2 a 50 €/t -> 92.638,88888888889;
sintesi 150 €/t -> 310.883,3333333334; totale 2.455.522,2222222225;
LCoA 1.184,77992816169 €/t contro benchmark 980 (grigia 800 + 1,8 x
ETS 100) -> NON_CONVIENTE; grigia spostata 1.658.044,4444444445, CO2
valorizzata 373.060,00000000006, netto 424.417,7777777779 €/anno.
"""

import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh623_num", "mh623_nneg", "mh623_pos", "mh623_frac01",
           "mh623_kg_h2_annui", "mh623_kg_n2_annue", "mh623_t_nh3_annue",
           "mh623_costo_h2", "mh623_costo_n2", "mh623_costo_sintesi",
           "mh623_costo_totale", "mh623_lcoa", "mh623_ammoniaca_spostata",
           "mh623_valore_co2", "mh623_costo_netto", "mh623_benchmark",
           "mh623_verdetto", "mh623_sensibilita", "mh623_demo")

TITLE623 = ("⚗️💚 Power-to-Ammonia: l'ammoniaca verde da H2 "
            "(Haber-Bosch)")

DEMO = _F["mh623_demo"]()
KG_DEMO = 400000.0
N2_DEMO = 1852777.7777777778
NH3_DEMO = 2072.5555555555557
CH2_DEMO = 2052000.0
CN2_DEMO = 92638.88888888889
CSIN_DEMO = 310883.3333333334
TOT_DEMO = 2455522.2222222225
LCOA_DEMO = 1184.77992816169
BM_DEMO = 980.0
SPOST_DEMO = 1658044.4444444445
VC_DEMO = 373060.00000000006
NETTO_DEMO = 424417.7777777779


class TestW623Validatori:
    def test_num(self):
        assert _F["mh623_num"](3, "x") == 3.0
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh623_num"](bad, "x")

    def test_nneg_pos_frac01(self):
        assert _F["mh623_nneg"](0, "x") == 0.0
        assert _F["mh623_pos"](0.001, "x") == 0.001
        assert _F["mh623_frac01"](1, "x") == 1.0
        for bad in (-1.0,):
            with pytest.raises(ValueError):
                _F["mh623_nneg"](bad, "x")
        with pytest.raises(ValueError):
            _F["mh623_pos"](0.0, "x")
        with pytest.raises(ValueError):
            _F["mh623_frac01"](1.5, "x")
        with pytest.raises(ValueError):
            _F["mh623_frac01"](-0.1, "x")


class TestW623Catena:
    def test_stechiometria(self):
        kg = _F["mh623_kg_h2_annui"](100.0, 4000.0)
        assert kg == pytest.approx(KG_DEMO)
        # 4,6319 kg N2 per kg H2 (28,014 / 6,048)
        assert _F["mh623_kg_n2_annue"](kg) == pytest.approx(N2_DEMO)
        # 5,6319 kg NH3 per kg H2 (34,062 / 6,048) x eta 0,92
        assert _F["mh623_t_nh3_annue"](kg, 0.92) == pytest.approx(NH3_DEMO)

    def test_kg_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh623_kg_h2_annui"](0.0, 4000.0)

    def test_eta_fuori_intervallo(self):
        with pytest.raises(ValueError):
            _F["mh623_t_nh3_annue"](KG_DEMO, 1.2)

    def test_eta_zero_niente_nh3(self):
        assert _F["mh623_t_nh3_annue"](KG_DEMO, 0.0) == 0.0

    def test_costi(self):
        assert _F["mh623_costo_h2"](KG_DEMO, 5.13) == \
            pytest.approx(CH2_DEMO)
        assert _F["mh623_costo_n2"](N2_DEMO, 50.0) == \
            pytest.approx(CN2_DEMO)
        assert _F["mh623_costo_sintesi"](NH3_DEMO, 150.0) == \
            pytest.approx(CSIN_DEMO)
        tot = _F["mh623_costo_totale"](CH2_DEMO, CN2_DEMO, CSIN_DEMO)
        assert tot == pytest.approx(TOT_DEMO)


class TestW623Lcoa:
    def test_lcoa_demo(self):
        assert _F["mh623_lcoa"](TOT_DEMO, NH3_DEMO) == \
            pytest.approx(LCOA_DEMO)

    def test_lcoa_none_senza_nh3(self):
        assert _F["mh623_lcoa"](100.0, 0.0) is None

    def test_benchmark_demo(self):
        assert _F["mh623_benchmark"](800.0, 1.8, 100.0) == \
            pytest.approx(BM_DEMO)

    def test_spostata_e_valore(self):
        assert _F["mh623_ammoniaca_spostata"](NH3_DEMO, 800.0) == \
            pytest.approx(SPOST_DEMO)
        assert _F["mh623_valore_co2"](NH3_DEMO, 1.8, 100.0) == \
            pytest.approx(VC_DEMO)
        netto = _F["mh623_costo_netto"](TOT_DEMO, SPOST_DEMO, VC_DEMO)
        assert netto == pytest.approx(NETTO_DEMO)


class TestW623Verdetto:
    def test_conviente(self):
        v = _F["mh623_verdetto"](900.0, 980.0)
        assert v["verdetto"] == "CONVIENTE"
        assert v["lcoa"] == pytest.approx(900.0)

    def test_pareggio_conviente(self):
        assert _F["mh623_verdetto"](980.0, 980.0)["verdetto"] == \
            "CONVIENTE"

    def test_marginale_entro_15(self):
        v = _F["mh623_verdetto"](1127.0, 980.0)
        assert v["verdetto"] == "MARGINALE"

    def test_non_conviente(self):
        v = _F["mh623_verdetto"](LCOA_DEMO, BM_DEMO)
        assert v["verdetto"] == "NON_CONVIENTE"

    def test_non_calcolabile(self):
        v = _F["mh623_verdetto"](None, 980.0)
        assert v["verdetto"] == "NON_CALCOLABILE"


class TestW623Sensibilita:
    def test_geometria(self):
        rows = _F["mh623_sensibilita"](100.0, 4000.0, 0.92, 50.0, 150.0,
                                       800.0, 1.8, [2.0, 5.0],
                                       [60.0, 100.0])
        assert len(rows) == 4
        # riga estrema hand-computed: LCOH 2 -> lcoa =
        # (400000*2 + 92638.89 + 310883.33) / 2072.5556
        r0 = rows[0]
        assert r0["lcoa"] == pytest.approx(
            (800000.0 + 92638.88888888889 + 310883.3333333334) / NH3_DEMO)
        assert r0["benchmark"] == pytest.approx(800.0 + 1.8 * 60.0)

    def test_monotonia_lcoa(self):
        rows = _F["mh623_sensibilita"](100.0, 4000.0, 0.92, 50.0, 150.0,
                                       800.0, 1.8, [1.0, 5.0, 10.0],
                                       [100.0])
        lcoas = [r["lcoa"] for r in rows]
        assert lcoas == sorted(lcoas)

    def test_giudizio_conviente_lcoh_basso(self):
        rows = _F["mh623_sensibilita"](100.0, 4000.0, 0.92, 50.0, 150.0,
                                       800.0, 1.8, [1.0], [300.0])
        assert rows[0]["giudizio"] == "CONVIENTE"

    def test_liste_vuote(self):
        with pytest.raises(ValueError):
            _F["mh623_sensibilita"](100.0, 4000.0, 0.92, 50.0, 150.0,
                                    800.0, 1.8, [], [100.0])
        with pytest.raises(ValueError):
            _F["mh623_sensibilita"](100.0, 4000.0, 0.92, 50.0, 150.0,
                                    800.0, 1.8, [5.0], [])

    def test_demo_catena_completa(self):
        d = DEMO
        kg = _F["mh623_kg_h2_annui"](d["portata_kg_h"], d["ore_annue"])
        n2 = _F["mh623_kg_n2_annue"](kg)
        nh3 = _F["mh623_t_nh3_annue"](kg, d["eta_sintesi"])
        h2 = _F["mh623_costo_h2"](kg, d["lcoh_eur_kg"])
        c_n2 = _F["mh623_costo_n2"](n2, d["prezzo_n2_eur_t"])
        sin = _F["mh623_costo_sintesi"](
            nh3, d["costo_haber_bosch_eur_t"])
        tot = _F["mh623_costo_totale"](h2, c_n2, sin)
        lcoa = _F["mh623_lcoa"](tot, nh3)
        bm = _F["mh623_benchmark"](d["prezzo_fossile_eur_t"],
                                   d["ef_grigia_tco2_t"],
                                   d["prezzo_ets_eur_t"])
        ver = _F["mh623_verdetto"](lcoa, bm)
        spost = _F["mh623_ammoniaca_spostata"](nh3,
                                               d["prezzo_fossile_eur_t"])
        vc = _F["mh623_valore_co2"](nh3, d["ef_grigia_tco2_t"],
                                    d["prezzo_ets_eur_t"])
        netto = _F["mh623_costo_netto"](tot, spost, vc)
        assert kg == pytest.approx(KG_DEMO)
        assert nh3 == pytest.approx(NH3_DEMO)
        assert tot == pytest.approx(TOT_DEMO)
        assert lcoa == pytest.approx(LCOA_DEMO)
        assert bm == pytest.approx(BM_DEMO)
        assert ver["verdetto"] == "NON_CONVIENTE"
        assert netto == pytest.approx(NETTO_DEMO)


class TestW623Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def _ui(self):
        return self._src().split("with tab623:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 685
        assert TITLE623 in titles
        assert TITLE623 in titles

    def test_chain(self):
        assert ", tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685 = st.tabs([" in self._src()
        assert "with tab623:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st623_[a-z0-9_]+", self._ui()))
        attese = {"st623_port", "st623_ore", "st623_lcoh", "st623_eta",
                  "st623_pn2", "st623_sin", "st623_pf", "st623_ef",
                  "st623_ets", "st623_tab", "st623_graf", "st623_go",
                  "st623_fig", "st623_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st623_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        sec = self._src().split('# W623 (21/10/2026)')[1]
        sec = sec.split('# W622 (21/10/2026)')[0]
        for w in ("api_key", "apikey", "password", "passwd", "secret",
                  "token"):
            assert w not in sec.lower(), f"sospetto segreto: {w}"
