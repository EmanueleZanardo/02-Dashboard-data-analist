"""Test tab622 "🔥⛽ Metanazione (Power-to-Methane): il metano sintetico da CO2 catturata".

Demo calcolata a mano: 100 kg/h x 4000 h -> 400.000 kg H2/anno;
stechiometria (44,01 / (4 x 2,016)) -> 2.183,035714285714 tCO2/anno;
eta 78 % -> 10.398,96 MWh SNG/anno; LCOH 5,13 -> H2 2.052.000;
CO2 a 100 €/t -> 218.303,57142857142; metanazione 25 €/MWh ->
259.974,00000000003; totale 2.530.277,5714285714; LCoM
243,3202523549058 €/MWh contro benchmark 70,2 (gas 50 + 0,202 x ETS
100) -> NON_CONVIENTE; gas evitato 519.948,00000000006, CO2
valorizzata 210.058,99200000003, netto 1.800.270,5794285713 €/anno.
"""

import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh622_num", "mh622_nneg", "mh622_pos", "mh622_frac01",
           "mh622_kg_annui", "mh622_co2_tco2_annue",
           "mh622_energia_sng_mwh", "mh622_costo_h2", "mh622_costo_co2",
           "mh622_costo_metanazione", "mh622_costo_totale", "mh622_lcom",
           "mh622_gas_evitato", "mh622_valore_co2", "mh622_costo_netto",
           "mh622_benchmark", "mh622_verdetto", "mh622_sensibilita",
           "mh622_demo")

TITLE622 = ("🔥⛽ Metanazione (Power-to-Methane): il metano sintetico "
            "da CO2 catturata")

DEMO = _F["mh622_demo"]()
KG_DEMO = 400000.0
TCO2_DEMO = 2183.035714285714
EN_DEMO = 10398.960000000001
CH2_DEMO = 2052000.0
CCO2_DEMO = 218303.57142857142
CMET_DEMO = 259974.00000000003
TOT_DEMO = 2530277.5714285714
LCOM_DEMO = 243.3202523549058
BM_DEMO = 70.2
GE_DEMO = 519948.00000000006
VC_DEMO = 210058.99200000003
NETTO_DEMO = 1800270.5794285713


class TestW622Validatori:
    def test_num(self):
        assert _F["mh622_num"](3, "x") == 3.0
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh622_num"](bad, "x")

    def test_nneg_pos_frac01(self):
        assert _F["mh622_nneg"](0, "x") == 0.0
        assert _F["mh622_pos"](0.001, "x") == 0.001
        assert _F["mh622_frac01"](1, "x") == 1.0
        for bad in (-1.0,):
            with pytest.raises(ValueError):
                _F["mh622_nneg"](bad, "x")
        with pytest.raises(ValueError):
            _F["mh622_pos"](0.0, "x")
        with pytest.raises(ValueError):
            _F["mh622_frac01"](1.5, "x")
        with pytest.raises(ValueError):
            _F["mh622_frac01"](-0.1, "x")


class TestW622Catena:
    def test_kg_co2_energia(self):
        kg = _F["mh622_kg_annui"](100.0, 4000.0)
        assert kg == pytest.approx(KG_DEMO)
        assert _F["mh622_co2_tco2_annue"](kg) == pytest.approx(TCO2_DEMO)
        assert _F["mh622_energia_sng_mwh"](kg, 0.78) == \
            pytest.approx(EN_DEMO)

    def test_kg_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh622_kg_annui"](0.0, 4000.0)

    def test_eta_fuori_intervallo(self):
        with pytest.raises(ValueError):
            _F["mh622_energia_sng_mwh"](KG_DEMO, 1.2)

    def test_eta_zero_niente_sng(self):
        assert _F["mh622_energia_sng_mwh"](KG_DEMO, 0.0) == 0.0

    def test_costi(self):
        assert _F["mh622_costo_h2"](KG_DEMO, 5.13) == \
            pytest.approx(CH2_DEMO)
        assert _F["mh622_costo_co2"](TCO2_DEMO, 100.0) == \
            pytest.approx(CCO2_DEMO)
        assert _F["mh622_costo_metanazione"](EN_DEMO, 25.0) == \
            pytest.approx(CMET_DEMO)
        tot = _F["mh622_costo_totale"](CH2_DEMO, CCO2_DEMO, CMET_DEMO)
        assert tot == pytest.approx(TOT_DEMO)


class TestW622Lcom:
    def test_lcom_demo(self):
        assert _F["mh622_lcom"](TOT_DEMO, EN_DEMO) == \
            pytest.approx(LCOM_DEMO)

    def test_lcom_none_senza_sng(self):
        assert _F["mh622_lcom"](100.0, 0.0) is None

    def test_benchmark_demo(self):
        assert _F["mh622_benchmark"](50.0, 0.202, 100.0) == \
            pytest.approx(BM_DEMO)

    def test_gas_e_valore(self):
        assert _F["mh622_gas_evitato"](EN_DEMO, 50.0) == \
            pytest.approx(GE_DEMO)
        assert _F["mh622_valore_co2"](EN_DEMO, 0.202, 100.0) == \
            pytest.approx(VC_DEMO)
        netto = _F["mh622_costo_netto"](TOT_DEMO, GE_DEMO, VC_DEMO)
        assert netto == pytest.approx(NETTO_DEMO)


class TestW622Verdetto:
    def test_conviene(self):
        ver = _F["mh622_verdetto"](60.0, 70.2)
        assert ver["verdetto"] == "CONVIENTE"

    def test_bordo_conviene(self):
        # lcom == benchmark -> CONVIENTE (disuguaglianza <=)
        ver = _F["mh622_verdetto"](70.2, 70.2)
        assert ver["verdetto"] == "CONVIENTE"

    def test_bordo_marginale(self):
        # lcom == benchmark x 1,15 (stessa espressione del helper)
        ver = _F["mh622_verdetto"](70.2 * 1.15, 70.2)
        assert ver["verdetto"] == "MARGINALE"

    def test_non_conviene(self):
        # 80.74 > 70.2 x 1,15 (= 80.73)
        ver = _F["mh622_verdetto"](80.74, 70.2)
        assert ver["verdetto"] == "NON_CONVIENTE"

    def test_non_calcolabile(self):
        ver = _F["mh622_verdetto"](None, 70.2)
        assert ver["verdetto"] == "NON_CALCOLABILE"


class TestW622Sensibilita:
    def _args(self):
        d = DEMO
        return (d["portata_kg_h"], d["ore_annue"], d["eta_metanazione"],
                d["prezzo_co2_eur_t"], d["costo_metanazione_eur_mwh"],
                d["prezzo_gas_eur_mwh"], d["ef_gas_tco2_mwh"])

    def test_griglia_forma_e_demo(self):
        rows = _F["mh622_sensibilita"](*self._args(),
                                       [5.13], [100.0])
        assert len(rows) == 1
        assert rows[0]["lcom"] == pytest.approx(LCOM_DEMO)
        assert rows[0]["benchmark"] == pytest.approx(BM_DEMO)
        assert rows[0]["giudizio"] == "NON_CONVIENTE"

    def test_lcom_invariante_alla_portata(self):
        # raddoppio la portata: il LCoM non cambia (tutto scala lineare)
        d = DEMO
        r1 = _F["mh622_sensibilita"](d["portata_kg_h"], d["ore_annue"],
                                     d["eta_metanazione"],
                                     d["prezzo_co2_eur_t"],
                                     d["costo_metanazione_eur_mwh"],
                                     d["prezzo_gas_eur_mwh"],
                                     d["ef_gas_tco2_mwh"], [5.13], [100.0])
        r2 = _F["mh622_sensibilita"](2 * d["portata_kg_h"], d["ore_annue"],
                                     d["eta_metanazione"],
                                     d["prezzo_co2_eur_t"],
                                     d["costo_metanazione_eur_mwh"],
                                     d["prezzo_gas_eur_mwh"],
                                     d["ef_gas_tco2_mwh"], [5.13], [100.0])
        assert r1[0]["lcom"] == pytest.approx(r2[0]["lcom"])
        assert r2[0]["sng_mwh"] == pytest.approx(2 * r1[0]["sng_mwh"])
        assert r2[0]["tco2_richieste"] == \
            pytest.approx(2 * r1[0]["tco2_richieste"])

    def test_lcom_cresce_col_lcoh(self):
        rows = _F["mh622_sensibilita"](*self._args(),
                                       [2.0, 5.0, 8.0], [100.0])
        lcoms = [r["lcom"] for r in rows]
        assert lcoms[0] < lcoms[1] < lcoms[2]
        # a ETS 300 il giudizio migliora col benchmark che sale
        rows2 = _F["mh622_sensibilita"](*self._args(),
                                        [2.0], [60.0, 150.0, 300.0])
        giudizi = [r["giudizio"] for r in rows2]
        assert giudizi[0] in ("NON_CONVIENTE", "MARGINALE")
        assert giudizi[-1] in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE")

    def test_liste_vuote(self):
        with pytest.raises(ValueError):
            _F["mh622_sensibilita"](*self._args(), [], [100.0])
        with pytest.raises(ValueError):
            _F["mh622_sensibilita"](*self._args(), [5.13], [])


class TestW622Demo:
    def test_demo_end_to_end(self):
        d = DEMO
        kg = _F["mh622_kg_annui"](d["portata_kg_h"], d["ore_annue"])
        tco2 = _F["mh622_co2_tco2_annue"](kg)
        en = _F["mh622_energia_sng_mwh"](kg, d["eta_metanazione"])
        h2 = _F["mh622_costo_h2"](kg, d["lcoh_eur_kg"])
        co2 = _F["mh622_costo_co2"](tco2, d["prezzo_co2_eur_t"])
        met = _F["mh622_costo_metanazione"](
            en, d["costo_metanazione_eur_mwh"])
        tot = _F["mh622_costo_totale"](h2, co2, met)
        lcom = _F["mh622_lcom"](tot, en)
        bm = _F["mh622_benchmark"](d["prezzo_gas_eur_mwh"],
                                   d["ef_gas_tco2_mwh"],
                                   d["prezzo_ets_eur_t"])
        ver = _F["mh622_verdetto"](lcom, bm)
        ge = _F["mh622_gas_evitato"](en, d["prezzo_gas_eur_mwh"])
        vc = _F["mh622_valore_co2"](en, d["ef_gas_tco2_mwh"],
                                    d["prezzo_ets_eur_t"])
        netto = _F["mh622_costo_netto"](tot, ge, vc)
        assert kg == pytest.approx(KG_DEMO)
        assert tco2 == pytest.approx(TCO2_DEMO)
        assert en == pytest.approx(EN_DEMO)
        assert tot == pytest.approx(TOT_DEMO)
        assert lcom == pytest.approx(LCOM_DEMO)
        assert bm == pytest.approx(BM_DEMO)
        assert ver["verdetto"] == "NON_CONVIENTE"
        assert netto == pytest.approx(NETTO_DEMO)


class TestW622Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def _ui(self):
        return self._src().split("with tab622:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 682
        assert TITLE622 in titles
        assert TITLE622 in titles

    def test_chain(self):
        assert ", tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682 = st.tabs([" in self._src()
        assert "with tab622:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st622_[a-z0-9_]+", self._ui()))
        attese = {"st622_port", "st622_ore", "st622_lcoh", "st622_eta",
                  "st622_met", "st622_pco2", "st622_pg", "st622_ef",
                  "st622_ets", "st622_tab", "st622_graf", "st622_go",
                  "st622_fig", "st622_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st622_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        sec = self._src().split('# W622 (21/10/2026)')[1]
        sec = sec.split('# W621 (21/10/2026)')[0]
        for w in ("api_key", "apikey", "password", "passwd", "secret",
                  "token"):
            assert w not in sec.lower(), f"sospetto segreto: {w}"
