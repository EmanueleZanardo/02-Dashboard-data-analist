"""Test tab666 "🌡️🔥 Pompa di calore industriale ad alta temperatura: il COP di Carnot dal calore di scarto"

Demo calcolata eseguendo mh666_demo_calcoli() (non a mano):
HTHP da 800 kW termici, 6.000 h/anno; fonte di scarto a 55 °C,
utenza a 130 °C, approccio 5 K; efficienza di secondo
principio 50 %, caldaia baseline 90 %; gas 75 EUR/MWh, ETS
100 EUR/tCO2, fattore CO2 gas 0,202 t CO2/MWh; elettricita'
140 EUR/MWh, fattore CO2 rete 0,28 t CO2/MWh; CAPEX specifico
1.100 EUR/kWth, O&M 3 % del CAPEX/anno; tasso 6 %, vita
20 anni, tolleranza 10 %.

- T_evap = (55 - 5) + 273,15 = 323.15 K
- T_cond = (130 + 5) + 273,15 = 408.15 K
- lift = 408.15 - 323.15 = 85.0 K
- COP_carnot = 408.15 / 85.0 = 4.801764705882353
- COP_reale = 4.801764705882353 x 50 % = 2.4008823529411765
- Q_th = 800 x 6000 / 1000 = 4800.0 MWh/anno
- E_el = 4800.0 / 2.4008823529411765 = 1999.2649761117236
  MWh/anno
- Q_sorgente = 4800.0 - 1999.2649761117236
             = 2800.7350238882764 MWh/anno
- F_gas = 4800.0 / 0,90 = 5333.333333333333 MWh PCI/anno
- costo base = 5333.333333333333 x 75
             + 5333.333333333333 x 0,202 x 100
             = 507733.3333333333 EUR/anno
- costo elettrico = 1999.2649761117236 x 140
                  = 279897.09665564133 EUR/anno
- CAPEX = 800 x 1100 = 880000.0 EUR
- O&M = 880000.0 x 3 % = 26400.0 EUR/anno
- risparmio = 507733.3333333333 - 279897.09665564133 - 26400.0
            = 201436.23667769198 EUR/anno
- CO2 evitata = 5333.333333333333 x 0,202
              - 1999.2649761117236 x 0,28
              = 517.5391400220506 t/anno
- flussi [-880000.0, 201436.23667769198 x 20];
  VAN(6 %) = 1430457.7652573911 EUR -> CONVIENTE (VAN > 0)
- TIR = 0.22494842671375903 (bisezione su [-0.9999, 10])
- payback = 5 (primo anno con cumulato >= 0)
- verdetto = 'CONVIENTE'
"""

import ast
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w666_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w666_helpers.py via AST
    (stesso pattern di tests/appfuncs.py: niente Streamlit)."""
    src = (_new_dir() / "w666_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w666_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w666_helpers.py: {missing}")
    return out


_F = _load("mh666_num", "mh666_nneg", "mh666_pos", "mh666_int_pos",
           "mh666_pct100",
           "mh666_t_k", "mh666_lift_k", "mh666_cop_carnot",
           "mh666_cop_reale", "mh666_q_th_mwh",
           "mh666_e_el_mwh", "mh666_q_sorgente_mwh",
           "mh666_f_gas_baseline", "mh666_costo_base",
           "mh666_costo_elettrico", "mh666_capex", "mh666_om",
           "mh666_risparmio", "mh666_co2_evitata_t_anno",
           "mh666_flussi", "mh666_van", "mh666_tir",
           "mh666_payback", "mh666_verdetto",
           "mh666_demo", "mh666_demo_calcoli")

TITLE666 = ("🌡️🔥 Pompa di calore industriale ad alta temperatura: "
            "il COP di Carnot dal calore di scarto")

T_EVAP_DEMO = 323.15
T_COND_DEMO = 408.15
LIFT_DEMO = 85.0
COP_CARNOT_DEMO = 4.801764705882353
COP_REALE_DEMO = 2.4008823529411765
Q_TH_DEMO = 4800.0
E_EL_DEMO = 1999.2649761117236
Q_SORG_DEMO = 2800.7350238882764
F_GAS_DEMO = 5333.333333333333
BASE_DEMO = 507733.3333333333
COSTO_EL_DEMO = 279897.09665564133
CAPEX_DEMO = 880000.0
OM_DEMO = 26400.0
RISP_DEMO = 201436.23667769198
CO2_DEMO = 517.5391400220506
VAN_DEMO = 1430457.7652573911
TIR_DEMO = 0.22494842671375903
PAYBACK_DEMO = 5
VITA_DEMO = 20
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w666_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w666_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh666_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh666_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh666_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh666_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh666_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh666_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh666_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh666_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh666_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh666_int_pos"](True, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh666_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh666_int_pos"](20.0, "x") == 20

    def test_pct100_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh666_pct100"](-0.1, "x")

    def test_pct100_rifiuta_sopra_100(self):
        with pytest.raises(ValueError):
            _F["mh666_pct100"](100.1, "x")

    def test_pct100_accetta_bordi(self):
        assert _F["mh666_pct100"](0.0, "x") == 0.0
        assert _F["mh666_pct100"](100.0, "x") == 100.0


class TestFisica:
    def test_t_k_evap_demo(self):
        assert _F["mh666_t_k"](55.0, 5.0, -1) == pytest.approx(
            T_EVAP_DEMO, rel=REL)

    def test_t_k_cond_demo(self):
        assert _F["mh666_t_k"](130.0, 5.0, 1) == pytest.approx(
            T_COND_DEMO, rel=REL)

    def test_t_k_segno_invalido(self):
        with pytest.raises(ValueError):
            _F["mh666_t_k"](55.0, 5.0, 0)

    def test_lift_demo(self):
        assert _F["mh666_lift_k"](
            T_COND_DEMO, T_EVAP_DEMO) == pytest.approx(
            LIFT_DEMO, rel=REL)

    def test_lift_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh666_lift_k"](323.15, 323.15)

    def test_lift_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh666_lift_k"](300.0, 400.0)

    def test_cop_carnot_demo(self):
        assert _F["mh666_cop_carnot"](
            T_COND_DEMO, T_EVAP_DEMO) == pytest.approx(
            COP_CARNOT_DEMO, rel=REL)

    def test_cop_carnot_unita_e_lift_unitario(self):
        # T_cond = 2 x lift -> COP = 2
        assert _F["mh666_cop_carnot"](200.0, 100.0) == \
            pytest.approx(2.0, rel=REL)

    def test_cop_carnot_rifiuta_lift_non_positivo(self):
        with pytest.raises(ValueError):
            _F["mh666_cop_carnot"](300.0, 300.0)

    def test_cop_reale_demo(self):
        assert _F["mh666_cop_reale"](
            COP_CARNOT_DEMO, 50.0) == pytest.approx(
            COP_REALE_DEMO, rel=REL)

    def test_cop_reale_proporzionale_a_eta(self):
        c1 = _F["mh666_cop_reale"](COP_CARNOT_DEMO, 50.0)
        c2 = _F["mh666_cop_reale"](COP_CARNOT_DEMO, 100.0)
        assert c2 == pytest.approx(2.0 * c1, rel=REL)

    def test_cop_reale_rifiuta_eta_sopra_100(self):
        with pytest.raises(ValueError):
            _F["mh666_cop_reale"](COP_CARNOT_DEMO, 101.0)

    def test_q_th_demo(self):
        assert _F["mh666_q_th_mwh"](
            800.0, 6000.0) == pytest.approx(Q_TH_DEMO,
                                             rel=REL)

    def test_e_el_demo(self):
        assert _F["mh666_e_el_mwh"](
            Q_TH_DEMO, COP_REALE_DEMO) == pytest.approx(
            E_EL_DEMO, rel=REL)

    def test_e_el_rifiuta_cop_zero(self):
        with pytest.raises(ValueError):
            _F["mh666_e_el_mwh"](Q_TH_DEMO, 0.0)

    def test_q_sorgente_demo_e_primo_principio(self):
        assert _F["mh666_q_sorgente_mwh"](
            Q_TH_DEMO, E_EL_DEMO) == pytest.approx(
            Q_SORG_DEMO, rel=REL)
        assert Q_SORG_DEMO == pytest.approx(
            Q_TH_DEMO - E_EL_DEMO, rel=REL)

    def test_f_gas_baseline_demo(self):
        assert _F["mh666_f_gas_baseline"](
            Q_TH_DEMO, 90.0) == pytest.approx(F_GAS_DEMO,
                                              rel=REL)

    def test_f_gas_rifiuta_eta_zero(self):
        with pytest.raises(ValueError):
            _F["mh666_f_gas_baseline"](Q_TH_DEMO, 0.0)

    def test_costo_base_demo(self):
        assert _F["mh666_costo_base"](
            F_GAS_DEMO, 75.0, 0.202, 100.0) == pytest.approx(
            BASE_DEMO, rel=REL)

    def test_costo_base_senza_ets(self):
        assert _F["mh666_costo_base"](
            F_GAS_DEMO, 75.0, 0.202, 0.0) == pytest.approx(
            F_GAS_DEMO * 75.0, rel=REL)

    def test_costo_elettrico_demo(self):
        assert _F["mh666_costo_elettrico"](
            E_EL_DEMO, 140.0) == pytest.approx(
            COSTO_EL_DEMO, rel=REL)

    def test_capex_demo(self):
        assert _F["mh666_capex"](
            800.0, 1100.0) == pytest.approx(CAPEX_DEMO,
                                             rel=REL)

    def test_om_demo(self):
        assert _F["mh666_om"](
            CAPEX_DEMO, 3.0) == pytest.approx(OM_DEMO,
                                              rel=REL)

    def test_om_zero_a_quota_zero(self):
        assert _F["mh666_om"](CAPEX_DEMO,
                              0.0) == pytest.approx(0.0)

    def test_risparmio_demo(self):
        assert _F["mh666_risparmio"](
            BASE_DEMO, COSTO_EL_DEMO, OM_DEMO) == \
            pytest.approx(RISP_DEMO, rel=REL)

    def test_risparmio_negativo_possibile(self):
        assert _F["mh666_risparmio"](100000.0, 200000.0,
                                     50000.0) == pytest.approx(
            -150000.0)

    def test_co2_evitata_demo(self):
        assert _F["mh666_co2_evitata_t_anno"](
            F_GAS_DEMO, 0.202, E_EL_DEMO,
            0.28) == pytest.approx(CO2_DEMO, rel=REL)

    def test_co2_evitata_rifiuta_fattore_rete_negativo(self):
        with pytest.raises(ValueError):
            _F["mh666_co2_evitata_t_anno"](F_GAS_DEMO, 0.202,
                                           E_EL_DEMO, -0.1)


class TestFinanza:
    def _flussi_demo(self):
        return _F["mh666_flussi"](CAPEX_DEMO, RISP_DEMO,
                                  VITA_DEMO)

    def test_flussi_struttura(self):
        fl = self._flussi_demo()
        assert fl[0] == -CAPEX_DEMO and len(fl) == 21
        assert all(f == RISP_DEMO for f in fl[1:])

    def test_flussi_rifiuta_vita_zero(self):
        with pytest.raises(ValueError):
            _F["mh666_flussi"](880000.0, 100.0, 0)

    def test_van_demo(self):
        assert _F["mh666_van"](self._flussi_demo(),
                               0.06) == pytest.approx(VAN_DEMO,
                                                      rel=REL)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh666_van"](self._flussi_demo(), -0.01)

    def test_van_tasso_zero(self):
        fl = [-880000.0, 201436.24, 201436.24]
        assert _F["mh666_van"](fl, 0.0) == pytest.approx(
            -477127.52, rel=1e-6)

    def test_tir_demo(self):
        assert _F["mh666_tir"](self._flussi_demo()) == \
            pytest.approx(TIR_DEMO, rel=REL)

    def test_tir_none_senza_cambio_segno(self):
        assert _F["mh666_tir"]([-100.0, -10.0, -10.0]) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh666_tir"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo(self):
        assert _F["mh666_payback"](self._flussi_demo()) == \
            PAYBACK_DEMO

    def test_payback_none_mai(self):
        assert _F["mh666_payback"]([-100.0, 1.0, 1.0]) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh666_verdetto"](VAN_DEMO, CAPEX_DEMO,
                                    RISP_DEMO, 0.10) == \
            VERDETTO_DEMO

    def test_verdetto_marginale_tolleranza_ampia(self):
        assert _F["mh666_verdetto"](-0.05 * CAPEX_DEMO,
                                    CAPEX_DEMO, RISP_DEMO,
                                    0.10) == "MARGINALE"

    def test_verdetto_non_conviente_van_oltre_tolleranza(self):
        assert _F["mh666_verdetto"](-CAPEX_DEMO, CAPEX_DEMO,
                                    RISP_DEMO, 0.10) == \
            "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_zero(self):
        assert _F["mh666_verdetto"](500.0, CAPEX_DEMO, 0.0,
                                    0.10) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_risparmio_negativo(self):
        assert _F["mh666_verdetto"](500.0, CAPEX_DEMO, -100.0,
                                    0.10) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_van_none(self):
        assert _F["mh666_verdetto"](None, CAPEX_DEMO, 100.0,
                                    0.10) == "NON_CALCOLABILE"

    def test_verdetto_rifiuta_tolleranza_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh666_verdetto"](100.0, CAPEX_DEMO, 100.0, 1.5)


class TestDemo:
    def test_demo_calcoli_end_to_end(self):
        c = _F["mh666_demo_calcoli"]()
        assert c["t_evap_k"] == pytest.approx(T_EVAP_DEMO,
                                              rel=REL)
        assert c["t_cond_k"] == pytest.approx(T_COND_DEMO,
                                              rel=REL)
        assert c["lift_k"] == pytest.approx(LIFT_DEMO, rel=REL)
        assert c["cop_carnot"] == pytest.approx(
            COP_CARNOT_DEMO, rel=REL)
        assert c["cop_reale"] == pytest.approx(COP_REALE_DEMO,
                                               rel=REL)
        assert c["q_th_mwh_anno"] == pytest.approx(Q_TH_DEMO,
                                                  rel=REL)
        assert c["e_el_mwh_anno"] == pytest.approx(E_EL_DEMO,
                                                  rel=REL)
        assert c["q_sorgente_mwh_anno"] == pytest.approx(
            Q_SORG_DEMO, rel=REL)
        assert c["f_gas_mwh_pci_anno"] == pytest.approx(
            F_GAS_DEMO, rel=REL)
        assert c["costo_base_eur_anno"] == pytest.approx(
            BASE_DEMO, rel=REL)
        assert c["costo_elettrico_eur_anno"] == pytest.approx(
            COSTO_EL_DEMO, rel=REL)
        assert c["capex_eur"] == pytest.approx(CAPEX_DEMO,
                                               rel=REL)
        assert c["om_eur_anno"] == pytest.approx(OM_DEMO,
                                                 rel=REL)
        assert c["risparmio_eur_anno"] == pytest.approx(
            RISP_DEMO, rel=REL)
        assert c["co2_evitata_t_anno"] == pytest.approx(
            CO2_DEMO, rel=REL)
        assert c["van_eur"] == pytest.approx(VAN_DEMO, rel=REL)
        assert c["tir"] == pytest.approx(TIR_DEMO, rel=REL)
        assert c["payback_anni"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO

    def test_demo_calcoli_deterministico(self):
        assert _F["mh666_demo_calcoli"]() == _F["mh666_demo_calcoli"]()

    def test_demo_defaults(self):
        d = _F["mh666_demo"]()
        assert d["p_th_kw"] == 800.0
        assert d["ore_anno"] == 6000.0
        assert d["t_fonte_c"] == 55.0
        assert d["t_utenza_c"] == 130.0
        assert d["dt_approccio_k"] == 5.0
        assert d["eta_lorentz_pct"] == 50.0
        assert d["eta_caldaia_pct"] == 90.0
        assert d["p_gas_eur_mwh"] == 75.0
        assert d["p_ets_eur_t"] == 100.0
        assert d["f_co2_gas_t_mwh"] == 0.202
        assert d["p_el_eur_mwh"] == 140.0
        assert d["f_co2_el_t_mwh"] == 0.28
        assert d["capex_eur_kw_th"] == 1100.0
        assert d["om_pct_capex"] == 3.0
        assert d["tasso_pct"] == 6.0
        assert d["vita_anni"] == 20
        assert d["tolleranza_pct"] == 10.0

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        mh666_demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["mh666_demo_calcoli"]()
        doc = __doc__
        for chiave in ("t_evap_k", "t_cond_k", "lift_k",
                       "cop_carnot", "cop_reale",
                       "q_th_mwh_anno", "e_el_mwh_anno",
                       "q_sorgente_mwh_anno",
                       "f_gas_mwh_pci_anno",
                       "costo_base_eur_anno",
                       "costo_elettrico_eur_anno",
                       "capex_eur", "om_eur_anno",
                       "risparmio_eur_anno",
                       "co2_evitata_t_anno", "van_eur", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "lift = 408.15 - 323.15 = 85.0 K" in doc
        assert "payback = 5" in doc
        assert "verdetto = 'CONVIENTE'" in doc


class TestUI:
    def test_header_helpers_presente(self):
        assert '# W666 (23/10/2026) - tab666' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh666_num", "mh666_nneg", "mh666_pos",
                     "mh666_int_pos", "mh666_pct100",
                     "mh666_t_k", "mh666_lift_k",
                     "mh666_cop_carnot", "mh666_cop_reale",
                     "mh666_q_th_mwh", "mh666_e_el_mwh",
                     "mh666_q_sorgente_mwh",
                     "mh666_f_gas_baseline", "mh666_costo_base",
                     "mh666_costo_elettrico", "mh666_capex",
                     "mh666_om", "mh666_risparmio",
                     "mh666_co2_evitata_t_anno",
                     "mh666_flussi", "mh666_van", "mh666_tir",
                     "mh666_payback", "mh666_verdetto",
                     "mh666_demo", "mh666_demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE666) == 1

    def test_blocco_with_tab666(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab666:"

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st666_[a-z0-9_]+)"', _ui_src())
        assert len(keys) >= 20
        assert len(set(keys)) == len(keys)
        # nessuna collisione con le chiavi del ciclo precedente
        assert not any(k.startswith("st665_") for k in keys)

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_rm666 <= 0.0" in src
        assert "NON_CALCOLABILE" in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_rm666 <= 0.0") < src.index(".metric(")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "COP reale" in src
        assert "Risparmio (€/anno)" in src
        assert "CO2 evitata (t/anno)" in src
        assert "Payback (anni)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd666" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_grafico_costi_presente(self):
        src = _ui_src()
        assert "plotly.graph_objects" in src
        assert "Caldaia gas (baseline)" in src
        assert "HTHP (scenario)" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert 'sep=";"' in src
        assert "hthp_alta_temperatura.csv" in src

    def test_differenziazione_da_feature_esistenti(self):
        src = _ui_src()
        assert "Carnot" in src
        assert "alta temperatura" in src.lower()

    def test_nessun_segreto_nella_sezione(self):
        assert not re.search(r'(?i)(api_key|secret|password)\s*=\s*["\']',
                             _ui_src())
