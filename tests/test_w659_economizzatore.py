"""Test tab659 "🔥 Economizzatore fumi: il calore che esce dal camino".

Demo calcolata a mano: fumi di caldaia a gas — portata 2,5 kg/s,
cp 1,15 kJ/kgK, T_in 220 °C, T_out 130 °C, rendimento recupero 85 %,
6.000 h/anno, caldaia 92 %, prezzo combustibile 0,09 EUR/kWh,
O&M 3.000 EUR/anno, fattore CO2 gas 0,202 kg/kWh, CAPEX diretto
180.000 EUR, 6 %, 15 anni, tolleranza 0,10 (frazione del CAPEX).

- P_rec = 2,5 x 1,15 x (220 - 130) x 0,85
       = 2,875 x 90 x 0,85 = 258,75 x 0,85 = 219,9375 kW
- E_rec = 219,9375 x 6.000 = 1.319.625 kWh/anno
- E_comb_risp = 1.319.625 / 0,92 = 1.434.375 kWh/anno
- lordo = 1.434.375 x 0,09 = 129.093,75 EUR/anno
- netto = 129.093,75 - 3.000 = 126.093,75 EUR/anno
- CO2 evitata = 1.434.375 x 0,202 / 1.000 = 289,74375 t/anno
- flussi [-180.000, 126.093,75 x 15];
  VAN(6 %) = 1.044.653,8957979647 EUR -> CONVIENTE
- TIR = 0,7002767000433059 (70,0277 %); payback anno 2
  (-180.000 + 126.093,75 = -53.906,25 < 0;
   + 126.093,75 = 72.043,50 >= 0)
- rischio corrosione: T_out 130 °C NON < 130 -> False
"""

import math
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh659_num", "mh659_nneg", "mh659_pos", "mh659_int_pos",
           "mh659_frazione", "mh659_efficienza",
           "mh659_potenza_rec_kw", "mh659_energia_rec_kwh",
           "mh659_energia_comb_risp_kwh", "mh659_risparmio_lordo_eur",
           "mh659_risparmio_netto_eur", "mh659_co2_t",
           "mh659_capex_da_specifico", "mh659_flussi", "mh659_van",
           "mh659_tir", "mh659_payback", "mh659_verdetto",
           "mh659_rischio_corrosione", "mh659_demo",
           "mh659_demo_calcoli")

TITLE659 = "🔥 Economizzatore fumi: il calore che esce dal camino"

P_REC_DEMO = 219.9375
E_REC_DEMO = 1319625.0
E_COMB_DEMO = 1434375.0
LORDO_DEMO = 129093.75
NETTO_DEMO = 126093.75
CO2_DEMO = 289.74375
CAPEX_DEMO = 180000.0
VAN_DEMO = 1044653.8957979647
TIR_DEMO = 0.7002767000433059
VITA_DEMO = 15
PAYBACK_DEMO = 2
VERDETTO_DEMO = "CONVIENTE"


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w659_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _helpers_src():
    return (_new_dir() / "w659_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w659_ui.py").read_text(encoding="utf-8")


def _app_src():
    return (Path.home() / "workspace/repo-dashboard/Dashboard-data-analist"
            / "app.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh659_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh659_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh659_num"](float("nan"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh659_nneg"](-0.1, "x")

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh659_pos"](0.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh659_int_pos"](2.5, "x")

    def test_frazione_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh659_frazione"](1.1, "x")

    def test_efficienza_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh659_efficienza"](0.0, "x")

    def test_efficienza_accetta_uno(self):
        assert _F["mh659_efficienza"](1.0, "x") == 1.0


class TestFisica:
    def test_potenza_rec_demo(self):
        assert _F["mh659_potenza_rec_kw"](2.5, 1.15, 220.0, 130.0,
                                          0.85) == pytest.approx(P_REC_DEMO)

    def test_potenza_rec_rifiuta_tout_maggiore_tin(self):
        with pytest.raises(ValueError, match="T_out deve essere minore"):
            _F["mh659_potenza_rec_kw"](2.5, 1.15, 130.0, 220.0, 0.85)

    def test_potenza_rec_rifiuta_tout_uguale_tin(self):
        with pytest.raises(ValueError):
            _F["mh659_potenza_rec_kw"](2.5, 1.15, 130.0, 130.0, 0.85)

    def test_potenza_rec_rifiuta_eta_fuori_limite(self):
        with pytest.raises(ValueError):
            _F["mh659_potenza_rec_kw"](2.5, 1.15, 220.0, 130.0, 1.5)

    def test_potenza_rec_zero_se_portata_zero(self):
        assert _F["mh659_potenza_rec_kw"](0.0, 1.15, 220.0, 130.0,
                                          0.85) == pytest.approx(0.0)

    def test_energia_rec_demo(self):
        assert _F["mh659_energia_rec_kwh"](P_REC_DEMO, 6000.0) == \
            pytest.approx(E_REC_DEMO)

    def test_energia_rec_rifiuta_ore_oltre_8760(self):
        with pytest.raises(ValueError):
            _F["mh659_energia_rec_kwh"](100.0, 9000.0)

    def test_energia_comb_demo(self):
        assert _F["mh659_energia_comb_risp_kwh"](E_REC_DEMO, 0.92) == \
            pytest.approx(E_COMB_DEMO)

    def test_energia_comb_maggiore_se_caldaia_inefficiente(self):
        assert _F["mh659_energia_comb_risp_kwh"](E_REC_DEMO, 0.5) > \
            E_COMB_DEMO

    def test_risparmio_lordo_demo(self):
        assert _F["mh659_risparmio_lordo_eur"](E_COMB_DEMO, 0.09) == \
            pytest.approx(LORDO_DEMO)

    def test_risparmio_netto_demo(self):
        assert _F["mh659_risparmio_netto_eur"](LORDO_DEMO, 3000.0) == \
            pytest.approx(NETTO_DEMO)

    def test_risparmio_netto_negativo_possibile(self):
        assert _F["mh659_risparmio_netto_eur"](1000.0, 3000.0) == \
            pytest.approx(-2000.0)

    def test_co2_demo(self):
        assert _F["mh659_co2_t"](E_COMB_DEMO, 0.202) == \
            pytest.approx(CO2_DEMO)

    def test_co2_none_se_non_positiva(self):
        assert _F["mh659_co2_t"](0.0, 0.202) is None
        assert _F["mh659_co2_t"](-5.0, 0.202) is None

    def test_capex_da_specifico(self):
        assert _F["mh659_capex_da_specifico"](P_REC_DEMO, 900.0) == \
            pytest.approx(P_REC_DEMO * 900.0)

    def test_rischio_corrosione_false_bordo(self):
        assert _F["mh659_rischio_corrosione"](130.0) is False

    def test_rischio_corrosione_true_sotto(self):
        assert _F["mh659_rischio_corrosione"](120.0) is True

    def test_rischio_corrosione_false_sopra(self):
        assert _F["mh659_rischio_corrosione"](200.0) is False


class TestFinanza:
    def _flussi_demo(self):
        return _F["mh659_flussi"](CAPEX_DEMO, NETTO_DEMO, VITA_DEMO)

    def test_flussi_struttura(self):
        fl = _F["mh659_flussi"](CAPEX_DEMO, NETTO_DEMO, VITA_DEMO)
        assert fl[0] == -CAPEX_DEMO and len(fl) == 16
        assert all(f == NETTO_DEMO for f in fl[1:])

    def test_van_demo(self):
        assert _F["mh659_van"](self._flussi_demo(), 6.0) == \
            pytest.approx(VAN_DEMO)

    def test_tir_demo(self):
        assert _F["mh659_tir"](self._flussi_demo()) == \
            pytest.approx(TIR_DEMO)

    def test_tir_none_senza_cambio_segno(self):
        assert _F["mh659_tir"]([-100.0, -10.0, -10.0]) is None

    def test_payback_demo(self):
        assert _F["mh659_payback"](self._flussi_demo()) == PAYBACK_DEMO

    def test_payback_none_mai(self):
        assert _F["mh659_payback"]([-100.0, 1.0, 1.0]) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh659_verdetto"](VAN_DEMO, CAPEX_DEMO, NETTO_DEMO,
                                    0.10) == VERDETTO_DEMO

    def test_verdetto_marginale(self):
        assert _F["mh659_verdetto"](-9000.0, 180000.0, 5000.0,
                                    0.10) == "MARGINALE"

    def test_verdetto_non_conviente(self):
        assert _F["mh659_verdetto"](-90000.0, 180000.0, 5000.0,
                                    0.10) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile(self):
        assert _F["mh659_verdetto"](500.0, 180000.0, 0.0,
                                    0.10) == "NON_CALCOLABILE"
        assert _F["mh659_verdetto"](500.0, 180000.0, None,
                                    0.10) == "NON_CALCOLABILE"
        assert _F["mh659_verdetto"](None, 180000.0, 5000.0,
                                    0.10) == "NON_CALCOLABILE"

    def test_verdetto_rifiuta_tolleranza_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh659_verdetto"](100.0, 180000.0, 5000.0, 1.5)


class TestDemo:
    def test_demo_calcoli_end_to_end(self):
        c = _F["mh659_demo_calcoli"]()
        assert c["p_rec_kw"] == pytest.approx(P_REC_DEMO)
        assert c["e_rec_kwh_anno"] == pytest.approx(E_REC_DEMO)
        assert c["e_comb_risp_kwh_anno"] == pytest.approx(E_COMB_DEMO)
        assert c["risparmio_lordo_eur_anno"] == pytest.approx(LORDO_DEMO)
        assert c["risparmio_netto_eur_anno"] == pytest.approx(NETTO_DEMO)
        assert c["co2_t_anno"] == pytest.approx(CO2_DEMO)
        assert c["capex_eur"] == CAPEX_DEMO
        assert c["van_eur"] == pytest.approx(VAN_DEMO)
        assert c["tir"] == pytest.approx(TIR_DEMO)
        assert c["payback_anni"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO
        assert c["rischio_corrosione"] is False

    def test_demo_calcoli_deterministico(self):
        assert _F["mh659_demo_calcoli"]() == _F["mh659_demo_calcoli"]()

    def test_demo_defaults(self):
        d = _F["mh659_demo"]()
        assert d["m_dot"] == 2.5
        assert d["cp"] == 1.15
        assert d["t_in"] == 220.0
        assert d["t_out"] == 130.0
        assert d["modo_capex"] == "CAPEX diretto (€)"
        assert d["capex_eur"] == 180000.0
        assert d["vita_anni"] == 15


class TestUI:
    def test_header_helpers_presente(self):
        assert '# W659 (23/10/2026) - tab659' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh659_num", "mh659_nneg", "mh659_pos",
                     "mh659_int_pos", "mh659_frazione",
                     "mh659_efficienza", "mh659_potenza_rec_kw",
                     "mh659_energia_rec_kwh",
                     "mh659_energia_comb_risp_kwh",
                     "mh659_risparmio_lordo_eur",
                     "mh659_risparmio_netto_eur", "mh659_co2_t",
                     "mh659_capex_da_specifico", "mh659_flussi",
                     "mh659_van", "mh659_tir", "mh659_payback",
                     "mh659_verdetto", "mh659_rischio_corrosione",
                     "mh659_demo", "mh659_demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE659) == 1

    def test_blocco_with_tab659(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab659:"

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st659_[a-z0-9_]+)"', _ui_src())
        assert len(keys) >= 16
        assert len(set(keys)) == len(keys)
        # nessuna collisione con le chiavi del ciclo precedente
        assert not any(k.startswith("st658_") for k in keys)

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg659" in src
        assert "(_rs659 is None) or (_rs659 <= 0.0)" in src
        assert "st.stop()" in src

    def test_warning_corrosione_presente(self):
        assert "_cor659" in _ui_src()
        assert "130 °C" in _ui_src()

    def test_grafico_plotly_presente(self):
        assert "plotly.graph_objects" in _ui_src()

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert 'sep=";"' in src
        assert "economizzatore.csv" in _ui_src()

    def test_nessun_segreto_nella_sezione(self):
        assert not re.search(r'(?i)(api_key|secret|password)\s*=\s*["\']',
                             _ui_src())


class TestRegistry:
    def test_titolo_in_app(self):
        # titolo registrato nella lista di st.tabs + h1 della tab
        assert _app_src().count(TITLE659) >= 2

    def test_with_tab659_presente(self):
        assert "    with tab659:" in _app_src()

    def test_count_withs_659(self):
        assert len(re.findall(r"^    with tab\d+:$", _app_src(),
                              flags=re.M)) == 793

    def test_bump_catena_solo_append(self):
        # l'ancora finale e' la terna tab670, tab671, tab672 (APPEND boundary-safe)
        assert "tab791, tab792, tab793 = st.tabs" in _app_src()

    def test_helpers_applicati(self):
        assert _app_src().count("def mh659_") == 21
