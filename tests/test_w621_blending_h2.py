"""Test tab621 "💧⚗️ Blending idrogeno in rete gas: il premium per decarbonizzare".

Demo calcolata a mano: 100 kg/h x 4000 h -> 400.000 kg/anno =
4.448.000 Nm3 (x 11,12) = 13.332 MWh LHV (x 33,33 kWh/kg); EF gas
0,202 -> 2.693,064 tCO2/anno; LCOH 5,13 eur/kg -> costo 2.052.000;
gas 50 eur/MWh -> 666.600 evitati; CO2 100 eur/t -> 269.306,4
valorizzati; costo netto 1.116.093,6; MAC 414,43263138195005 eur/t
contro ETS 100 -> NON_CONVIENTE; quota blend 8,169262415515721 %
su 50 MSm3 serviti (sotto il limite 20 %).
"""

import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh621_num", "mh621_nneg", "mh621_pos", "mh621_frac01",
           "mh621_kg_annui", "mh621_nm3_annui", "mh621_energia_mwh",
           "mh621_tco2_evitate", "mh621_costo_h2", "mh621_gas_evitato",
           "mh621_valore_co2", "mh621_costo_netto", "mh621_mac",
           "mh621_quota_blend_pct", "mh621_verdetto", "mh621_sensibilita",
           "mh621_demo")

TITLE621 = ("💧⚗️ Blending idrogeno in rete gas: il premium per "
            "decarbonizzare")

DEMO = _F["mh621_demo"]()
KG_DEMO = 400000.0
NM3_DEMO = 4448000.0
EN_DEMO = 13332.0
TCO2_DEMO = 2693.0640000000003
COSTO_DEMO = 2052000.0
GAS_EV_DEMO = 666600.0
VAL_CO2_DEMO = 269306.4
NETTO_DEMO = 1116093.6
MAC_DEMO = 414.43263138195005
BLEND_DEMO = 8.169262415515721


class TestW621Validatori:
    def test_num(self):
        assert _F["mh621_num"](3, "x") == 3.0
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh621_num"](bad, "x")

    def test_nneg_pos_frac01(self):
        assert _F["mh621_nneg"](0, "x") == 0.0
        assert _F["mh621_pos"](0.001, "x") == 0.001
        assert _F["mh621_frac01"](1, "x") == 1.0
        for bad in (-1.0,):
            with pytest.raises(ValueError):
                _F["mh621_nneg"](bad, "x")
        with pytest.raises(ValueError):
            _F["mh621_pos"](0.0, "x")
        with pytest.raises(ValueError):
            _F["mh621_frac01"](1.5, "x")


class TestW621Catena:
    def test_kg_nm3_energia(self):
        kg = _F["mh621_kg_annui"](100.0, 4000.0)
        assert kg == pytest.approx(KG_DEMO)
        assert _F["mh621_nm3_annui"](kg) == pytest.approx(NM3_DEMO)
        assert _F["mh621_energia_mwh"](kg) == pytest.approx(EN_DEMO)

    def test_kg_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh621_kg_annui"](0.0, 4000.0)

    def test_tco2(self):
        assert _F["mh621_tco2_evitate"](EN_DEMO, 0.202) == \
            pytest.approx(TCO2_DEMO)

    def test_costi_e_valori(self):
        assert _F["mh621_costo_h2"](KG_DEMO, 5.13) == \
            pytest.approx(COSTO_DEMO)
        assert _F["mh621_gas_evitato"](EN_DEMO, 50.0) == \
            pytest.approx(GAS_EV_DEMO)
        assert _F["mh621_valore_co2"](TCO2_DEMO, 100.0) == \
            pytest.approx(VAL_CO2_DEMO)
        netto = _F["mh621_costo_netto"](COSTO_DEMO, GAS_EV_DEMO,
                                        VAL_CO2_DEMO)
        assert netto == pytest.approx(NETTO_DEMO)


class TestW621Mac:
    def test_mac_demo(self):
        mac = _F["mh621_mac"](COSTO_DEMO, GAS_EV_DEMO, VAL_CO2_DEMO,
                              TCO2_DEMO)
        assert mac == pytest.approx(MAC_DEMO)

    def test_mac_none_senza_tco2(self):
        assert _F["mh621_mac"](100.0, 50.0, 20.0, 0.0) is None

    def test_mac_negativo(self):
        # H2 regalato: il costo netto e' negativo -> MAC negativo
        mac = _F["mh621_mac"](100.0, 500.0, 200.0, 10.0)
        assert mac == pytest.approx(-60.0)
        ver = _F["mh621_verdetto"](mac, 100.0)
        assert ver["verdetto"] == "CONVIENTE"


class TestW621Blend:
    def test_quota_demo(self):
        assert _F["mh621_quota_blend_pct"](NM3_DEMO, 50.0) == \
            pytest.approx(BLEND_DEMO)

    def test_quota_rete_solo_h2(self):
        assert _F["mh621_quota_blend_pct"](100.0, 0.0) == 100.0

    def test_quota_zero_zero(self):
        with pytest.raises(ValueError):
            _F["mh621_quota_blend_pct"](0.0, 0.0)


class TestW621Verdetto:
    def test_conviente(self):
        ver = _F["mh621_verdetto"](80.0, 100.0)
        assert ver["verdetto"] == "CONVIENTE"

    def test_bordo_conviene(self):
        # mac == benchmark -> CONVIENTE (disuguaglianza <=)
        ver = _F["mh621_verdetto"](100.0, 100.0)
        assert ver["verdetto"] == "CONVIENTE"

    def test_bordo_marginale(self):
        # mac == benchmark x 1,15 (stessa espressione del helper)
        ver = _F["mh621_verdetto"](100.0 * 1.15, 100.0)
        assert ver["verdetto"] == "MARGINALE"

    def test_non_conviene(self):
        # 115.0 > 100 x 1,15 (= 114,99999999999999)
        ver = _F["mh621_verdetto"](115.0, 100.0)
        assert ver["verdetto"] == "NON_CONVIENTE"

    def test_non_calcolabile(self):
        ver = _F["mh621_verdetto"](None, 100.0)
        assert ver["verdetto"] == "NON_CALCOLABILE"


class TestW621Sensibilita:
    def _args(self):
        d = DEMO
        return (d["portata_kg_h"], d["ore_annue"], d["ef_tco2_mwh"],
                d["prezzo_gas_eur_mwh"], d["gas_msm3_annui"])

    def test_griglia_forma_e_demo(self):
        rows = _F["mh621_sensibilita"](*self._args(),
                                      [5.13], [100.0])
        assert len(rows) == 1
        assert rows[0]["mac"] == pytest.approx(MAC_DEMO)
        assert rows[0]["giudizio"] == "NON_CONVIENTE"

    def test_mac_invariante_alla_portata(self):
        # raddoppio la portata: il MAC non cambia (tutto scala lineare)
        d = DEMO
        r1 = _F["mh621_sensibilita"](d["portata_kg_h"], d["ore_annue"],
                                    d["ef_tco2_mwh"],
                                    d["prezzo_gas_eur_mwh"],
                                    d["gas_msm3_annui"], [5.13], [100.0])
        r2 = _F["mh621_sensibilita"](2 * d["portata_kg_h"],
                                    d["ore_annue"], d["ef_tco2_mwh"],
                                    d["prezzo_gas_eur_mwh"],
                                    d["gas_msm3_annui"], [5.13], [100.0])
        assert r1[0]["mac"] == pytest.approx(r2[0]["mac"])
        assert r2[0]["tco2_evitate"] == \
            pytest.approx(2 * r1[0]["tco2_evitate"])

    def test_mac_cresce_col_lcoh(self):
        rows = _F["mh621_sensibilita"](*self._args(),
                                      [2.0, 5.0, 8.0], [100.0])
        macs = [r["mac"] for r in rows]
        assert macs[0] < macs[1] < macs[2]
        # a LCOH 2 e CO2 100 il MAC e' sotto l'ETS
        assert rows[0]["giudizio"] == "CONVIENTE"

    def test_liste_vuote(self):
        with pytest.raises(ValueError):
            _F["mh621_sensibilita"](*self._args(), [], [100.0])
        with pytest.raises(ValueError):
            _F["mh621_sensibilita"](*self._args(), [5.13], [])


class TestW621Demo:
    def test_demo_end_to_end(self):
        d = DEMO
        kg = _F["mh621_kg_annui"](d["portata_kg_h"], d["ore_annue"])
        en = _F["mh621_energia_mwh"](kg)
        tco2 = _F["mh621_tco2_evitate"](en, d["ef_tco2_mwh"])
        co = _F["mh621_costo_h2"](kg, d["lcoh_eur_kg"])
        ge = _F["mh621_gas_evitato"](en, d["prezzo_gas_eur_mwh"])
        vc = _F["mh621_valore_co2"](tco2, d["prezzo_co2_eur_t"])
        mac = _F["mh621_mac"](co, ge, vc, tco2)
        ver = _F["mh621_verdetto"](mac, d["prezzo_co2_eur_t"])
        bl = _F["mh621_quota_blend_pct"](_F["mh621_nm3_annui"](kg),
                                         d["gas_msm3_annui"])
        assert kg == pytest.approx(KG_DEMO)
        assert tco2 == pytest.approx(TCO2_DEMO)
        assert mac == pytest.approx(MAC_DEMO)
        assert ver["verdetto"] == "NON_CONVIENTE"
        assert bl == pytest.approx(BLEND_DEMO)
        assert bl < d["limite_blend_pct"]


class TestW621Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def _ui(self):
        return self._src().split("with tab621:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 714
        assert TITLE621 in titles
        assert TITLE621 in titles

    def test_chain(self):
        assert ", tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714 = st.tabs([" in self._src()
        assert "with tab621:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st621_[a-z0-9_]+", self._ui()))
        attese = {"st621_port", "st621_ore", "st621_lcoh", "st621_pg",
                  "st621_pco2", "st621_ef", "st621_gas", "st621_lim",
                  "st621_tab", "st621_graf", "st621_go", "st621_fig",
                  "st621_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st621_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        sec = self._src().split('# W621 (21/10/2026)')[1]
        sec = sec.split('# W620 (21/10/2026)')[0]
        for w in ("api_key", "apikey", "password", "passwd", "secret",
                  "token"):
            assert w not in sec.lower(), f"sospetto segreto: {w}"
