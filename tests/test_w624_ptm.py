"""Test tab624 "🧪⛽ Power-to-Methanol: il metanolo verde da CO₂ (sintesi catalitica)".

Demo calcolata a mano: 100 kg/h x 4000 h -> 400.000 kg H2/anno;
stechiometria (44,009 / (3 x 2,016)) -> 2.910.648,1481481483 kg CO2/anno;
32,042 / (3 x 2,016) x eta 0,90 -> 1.907,2619047619 t CH3OH/anno;
LCOH 5,13 -> H2 2.052.000; CO2 a 100 €/t -> 291.064,8148148148;
sintesi 250 €/t -> 476.815,4761904762; totale 2.819.880,291005291;
LCoMe 1.478,4966259562 €/t contro benchmark 680 (fossile 600 + 0,8 x
ETS 100) -> NON_CONVIENTE; fossile spostato 1.144.357,142857143,
CO2 valorizzata 152.580,9523809524, netto 1.522.942,1957671957 €/anno.
"""

import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh624_num", "mh624_nneg", "mh624_pos", "mh624_frac01",
           "mh624_kg_h2_annui", "mh624_kg_co2_annue", "mh624_t_meoh_annue",
           "mh624_costo_h2", "mh624_costo_co2", "mh624_costo_sintesi",
           "mh624_costo_totale", "mh624_lcome", "mh624_metanolo_spostato",
           "mh624_valore_co2", "mh624_costo_netto", "mh624_benchmark",
           "mh624_verdetto", "mh624_sensibilita", "mh624_demo")

TITLE624 = ("🧪⛽ Power-to-Methanol: il metanolo verde da CO₂ "
            "(sintesi catalitica)")

DEMO = _F["mh624_demo"]()
KG_DEMO = 400000.0
CO2_DEMO = 2910648.1481481483
MEOH_DEMO = 1907.2619047619
CH2_DEMO = 2052000.0
CCO2_DEMO = 291064.8148148148
CSIN_DEMO = 476815.4761904762
TOT_DEMO = 2819880.291005291
LCOME_DEMO = 1478.4966259562
BM_DEMO = 680.0
SPOST_DEMO = 1144357.142857143
VC_DEMO = 152580.9523809524
NETTO_DEMO = 1522942.1957671957


class TestW624Validatori:
    def test_num(self):
        assert _F["mh624_num"](3, "x") == 3.0
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh624_num"](bad, "x")

    def test_nneg_pos_frac01(self):
        assert _F["mh624_nneg"](0, "x") == 0.0
        assert _F["mh624_pos"](0.001, "x") == 0.001
        assert _F["mh624_frac01"](1, "x") == 1.0
        for bad in (-1.0,):
            with pytest.raises(ValueError):
                _F["mh624_nneg"](bad, "x")
        with pytest.raises(ValueError):
            _F["mh624_pos"](0.0, "x")
        with pytest.raises(ValueError):
            _F["mh624_frac01"](1.5, "x")
        with pytest.raises(ValueError):
            _F["mh624_frac01"](-0.1, "x")


class TestW624Catena:
    def test_stechiometria(self):
        kg = _F["mh624_kg_h2_annui"](100.0, 4000.0)
        assert kg == pytest.approx(KG_DEMO)
        # 7,2766 kg CO2 per kg H2 (44,009 / 6,048)
        assert _F["mh624_kg_co2_annue"](kg) == pytest.approx(CO2_DEMO)
        # 5,2979 kg CH3OH per kg H2 (32,042 / 6,048) x eta 0,90
        assert _F["mh624_t_meoh_annue"](kg, 0.90) == pytest.approx(MEOH_DEMO)

    def test_kg_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh624_kg_h2_annui"](0.0, 4000.0)

    def test_eta_fuori_intervallo(self):
        with pytest.raises(ValueError):
            _F["mh624_t_meoh_annue"](KG_DEMO, 1.2)

    def test_eta_zero_niente_meoh(self):
        assert _F["mh624_t_meoh_annue"](KG_DEMO, 0.0) == 0.0

    def test_costi(self):
        assert _F["mh624_costo_h2"](KG_DEMO, 5.13) == \
            pytest.approx(CH2_DEMO)
        assert _F["mh624_costo_co2"](CO2_DEMO, 100.0) == \
            pytest.approx(CCO2_DEMO)
        assert _F["mh624_costo_sintesi"](MEOH_DEMO, 250.0) == \
            pytest.approx(CSIN_DEMO)
        tot = _F["mh624_costo_totale"](CH2_DEMO, CCO2_DEMO, CSIN_DEMO)
        assert tot == pytest.approx(TOT_DEMO)


class TestW624Lcome:
    def test_lcome_demo(self):
        assert _F["mh624_lcome"](TOT_DEMO, MEOH_DEMO) == \
            pytest.approx(LCOME_DEMO)

    def test_lcome_none_senza_meoh(self):
        assert _F["mh624_lcome"](100.0, 0.0) is None

    def test_benchmark_demo(self):
        assert _F["mh624_benchmark"](600.0, 0.8, 100.0) == \
            pytest.approx(BM_DEMO)

    def test_spostato_e_valore(self):
        assert _F["mh624_metanolo_spostato"](MEOH_DEMO, 600.0) == \
            pytest.approx(SPOST_DEMO)
        assert _F["mh624_valore_co2"](MEOH_DEMO, 0.8, 100.0) == \
            pytest.approx(VC_DEMO)
        netto = _F["mh624_costo_netto"](TOT_DEMO, SPOST_DEMO, VC_DEMO)
        assert netto == pytest.approx(NETTO_DEMO)


class TestW624Verdetto:
    def test_conviente(self):
        v = _F["mh624_verdetto"](600.0, 680.0)
        assert v["verdetto"] == "CONVIENTE"
        assert v["lcome"] == pytest.approx(600.0)

    def test_pareggio_conviente(self):
        assert _F["mh624_verdetto"](680.0, 680.0)["verdetto"] == \
            "CONVIENTE"

    def test_marginale_entro_15(self):
        v = _F["mh624_verdetto"](700.0, 680.0)
        assert v["verdetto"] == "MARGINALE"

    def test_non_conviente(self):
        v = _F["mh624_verdetto"](LCOME_DEMO, BM_DEMO)
        assert v["verdetto"] == "NON_CONVIENTE"

    def test_non_calcolabile(self):
        v = _F["mh624_verdetto"](None, 680.0)
        assert v["verdetto"] == "NON_CALCOLABILE"


class TestW624Sensibilita:
    def test_geometria(self):
        rows = _F["mh624_sensibilita"](100.0, 4000.0, 0.90, 100.0, 250.0,
                                       600.0, 0.8, [2.0, 5.0],
                                       [60.0, 100.0])
        assert len(rows) == 4
        # riga estrema hand-computed: LCOH 2 -> lcome =
        # (400000*2 + 291064.81 + 476815.48) / 1907.2619
        r0 = rows[0]
        assert r0["lcome"] == pytest.approx(
            (800000.0 + 291064.8148148148 + 476815.4761904762) / MEOH_DEMO)
        assert r0["benchmark"] == pytest.approx(600.0 + 0.8 * 60.0)

    def test_monotonia_lcome(self):
        rows = _F["mh624_sensibilita"](100.0, 4000.0, 0.90, 100.0, 250.0,
                                       600.0, 0.8, [1.0, 5.0, 10.0],
                                       [100.0])
        lcomes = [r["lcome"] for r in rows]
        assert lcomes == sorted(lcomes)

    def test_giudizio_conviente_lcoh_basso(self):
        rows = _F["mh624_sensibilita"](100.0, 4000.0, 0.90, 100.0, 250.0,
                                       600.0, 0.8, [1.0], [300.0])
        assert rows[0]["giudizio"] == "CONVIENTE"

    def test_liste_vuote(self):
        with pytest.raises(ValueError):
            _F["mh624_sensibilita"](100.0, 4000.0, 0.90, 100.0, 250.0,
                                    600.0, 0.8, [], [100.0])
        with pytest.raises(ValueError):
            _F["mh624_sensibilita"](100.0, 4000.0, 0.90, 100.0, 250.0,
                                    600.0, 0.8, [5.0], [])

    def test_demo_catena_completa(self):
        d = DEMO
        kg = _F["mh624_kg_h2_annui"](d["portata_kg_h"], d["ore_annue"])
        co2 = _F["mh624_kg_co2_annue"](kg)
        meoh = _F["mh624_t_meoh_annue"](kg, d["eta_sintesi"])
        h2 = _F["mh624_costo_h2"](kg, d["lcoh_eur_kg"])
        c_co2 = _F["mh624_costo_co2"](co2, d["prezzo_co2_eur_t"])
        sin = _F["mh624_costo_sintesi"](
            meoh, d["costo_loop_eur_t"])
        tot = _F["mh624_costo_totale"](h2, c_co2, sin)
        lcome = _F["mh624_lcome"](tot, meoh)
        bm = _F["mh624_benchmark"](d["prezzo_fossile_eur_t"],
                                   d["ef_fossile_tco2_t"],
                                   d["prezzo_ets_eur_t"])
        ver = _F["mh624_verdetto"](lcome, bm)
        spost = _F["mh624_metanolo_spostato"](meoh,
                                              d["prezzo_fossile_eur_t"])
        vc = _F["mh624_valore_co2"](meoh, d["ef_fossile_tco2_t"],
                                    d["prezzo_ets_eur_t"])
        netto = _F["mh624_costo_netto"](tot, spost, vc)
        assert kg == pytest.approx(KG_DEMO)
        assert meoh == pytest.approx(MEOH_DEMO)
        assert tot == pytest.approx(TOT_DEMO)
        assert lcome == pytest.approx(LCOME_DEMO)
        assert bm == pytest.approx(BM_DEMO)
        assert ver["verdetto"] == "NON_CONVIENTE"
        assert netto == pytest.approx(NETTO_DEMO)


class TestW624Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def _ui(self):
        return self._src().split("with tab624:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 625
        assert TITLE624 in titles
        assert TITLE624 in titles

    def test_chain(self):
        assert ", tab623, tab624, tab625 = st.tabs([" in self._src()
        assert "with tab624:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st624_[a-z0-9_]+", self._ui()))
        attese = {"st624_port", "st624_ore", "st624_lcoh", "st624_eta",
                  "st624_pco2", "st624_sin", "st624_pf", "st624_ef",
                  "st624_ets", "st624_tab", "st624_graf", "st624_go",
                  "st624_fig", "st624_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st624_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        sec = self._src().split('# W624 (21/10/2026)')[1]
        sec = sec.split('# W623 (21/10/2026)')[0]
        for w in ("api_key", "apikey", "password", "passwd", "secret",
                  "token"):
            assert w not in sec.lower(), f"sospetto segreto: {w}"
