"""Test tab665 "♨️🕳️ Trappole di vapore: quanto vapore perdi dalle trappole rotte?"

Demo calcolata eseguendo mh665_demo_calcoli() (non a mano):
rete con 40 trappole, 25 % guaste; vapore a 10 bar assoluti;
orifizio equivalente 3,2 mm; 8.000 h/anno; calore latente
2,0 MJ/kg; rendimento caldaia 90 %; gas 75 EUR/MWh; ETS
100 EUR/tCO2; fattore CO2 gas 0,202 t CO2/MWh; acqua 3 EUR/t;
sostituzione 450 EUR/trappola; O&M ispezione 5.000 EUR/anno;
perdita residua 3 %; tasso 6 %; vita 15 anni; tolleranza 10 %.

- m_dot = 0,2472 x 10 x 3,2^2 = 25.313280000000002 kg/h per
  trappola guasta (formula di Napier in SI)
- N_gua = round(40 x 25 %) = 10
- vapore perso = 10 x 25.313280000000002 x 8000.0 / 1000
               = 2025.0624000000003 t/anno
- E_termica = 2025.0624000000003 x 1000 x 2,0 / 3600
            = 1125.0346666666667 MWh/anno
- F_gas = 1125.0346666666667 / 0,90
        = 1250.0385185185185 MWh PCI/anno
- F_gas_residuo = 1250.0385185185185 x 3 %
                = 37.50115555555555 MWh PCI/anno
- costo combustibile = 1250.0385185185185 x 75
                     = 93752.88888888889 EUR/anno
- costo ETS = 1250.0385185185185 x 0,202 x 100
            = 25250.778074074075 EUR/anno
- costo acqua = 2025.0624000000003 x 3 = 6075.1872 EUR/anno
- costo base = 93752.88888888889 + 25250.778074074075
             + 6075.1872 = 125078.85416296296 EUR/anno
- residuo = 125078.85416296296 x 3 %
          = 3752.3656248888888 EUR/anno
- CAPEX = 10 x 450 = 4500.0 EUR
- risparmio = 125078.85416296296 - 3752.3656248888888 - 5000
            = 116326.48853807407 EUR/anno
- CO2 evitata = (1250.0385185185185 - 37.50115555555555) x 0,202
              = 244.93254731851854 t/anno
- flussi [-4500.0, 116326.48853807407 x 15];
  VAN(6 %) = 1125291.820551373 EUR -> CONVIENTE (VAN > 0)
- TIR = None (nessun cambio di segno di NPV in [-0.9999, 10]:
  NPV > 0 a entrambi gli estremi della bisezione)
- payback = 1 (primo anno con cumulato >= 0)
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
    if (p / "w665_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w665_helpers.py via AST
    (stesso pattern di tests/appfuncs.py: niente Streamlit)."""
    src = (_new_dir() / "w665_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w665_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w665_helpers.py: {missing}")
    return out


_F = _load("mh665_num", "mh665_nneg", "mh665_pos", "mh665_int_pos",
           "mh665_pct100",
           "mh665_m_dot", "mh665_n_guaste",
           "mh665_vapore_perso_t_anno", "mh665_e_termica_mwh",
           "mh665_f_gas_mwh", "mh665_costo_combustibile",
           "mh665_costo_ets", "mh665_costo_acqua",
           "mh665_costo_base", "mh665_residuo", "mh665_capex",
           "mh665_risparmio", "mh665_co2_evitata_t_anno",
           "mh665_flussi", "mh665_van", "mh665_tir",
           "mh665_payback", "mh665_verdetto",
           "mh665_demo", "mh665_demo_calcoli")

TITLE665 = ("♨️🕳️ Trappole di vapore: quanto vapore perdi "
            "dalle trappole rotte?")

M_DOT_DEMO = 25.313280000000002
N_GUA_DEMO = 10
VAPORE_DEMO = 2025.0624000000003
E_TERM_DEMO = 1125.0346666666667
F_GAS_DEMO = 1250.0385185185185
F_GAS_RESIDUO_DEMO = 37.50115555555555
COMB_DEMO = 93752.88888888889
ETS_DEMO = 25250.778074074075
ACQUA_DEMO = 6075.1872
BASE_DEMO = 125078.85416296296
RESIDUO_DEMO = 3752.3656248888888
CAPEX_DEMO = 4500.0
RISP_DEMO = 116326.48853807407
CO2_DEMO = 244.93254731851854
VAN_DEMO = 1125291.820551373
TIR_DEMO = None
PAYBACK_DEMO = 1
VITA_DEMO = 15
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w665_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w665_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh665_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh665_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh665_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh665_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh665_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh665_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh665_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh665_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh665_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh665_int_pos"](True, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh665_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh665_int_pos"](40.0, "x") == 40

    def test_pct100_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh665_pct100"](-0.1, "x")

    def test_pct100_rifiuta_sopra_100(self):
        with pytest.raises(ValueError):
            _F["mh665_pct100"](100.1, "x")

    def test_pct100_accetta_bordi(self):
        assert _F["mh665_pct100"](0.0, "x") == 0.0
        assert _F["mh665_pct100"](100.0, "x") == 100.0


class TestFisica:
    def test_m_dot_demo(self):
        assert _F["mh665_m_dot"](10.0, 3.2) == pytest.approx(
            M_DOT_DEMO, rel=REL)

    def test_m_dot_scala_con_diametro_quadrato(self):
        m1 = _F["mh665_m_dot"](10.0, 3.2)
        m2 = _F["mh665_m_dot"](10.0, 6.4)
        assert m2 == pytest.approx(4.0 * m1, rel=REL)

    def test_m_dot_rifiuta_pressione_zero(self):
        with pytest.raises(ValueError):
            _F["mh665_m_dot"](0.0, 3.2)

    def test_m_dot_rifiuta_diametro_negativo(self):
        with pytest.raises(ValueError):
            _F["mh665_m_dot"](10.0, -1.0)

    def test_n_guaste_demo(self):
        assert _F["mh665_n_guaste"](40, 25.0) == N_GUA_DEMO

    def test_n_guaste_zero_a_quota_zero(self):
        assert _F["mh665_n_guaste"](40, 0.0) == 0

    def test_n_guaste_tutte_a_quota_100(self):
        assert _F["mh665_n_guaste"](40, 100.0) == 40

    def test_n_guaste_arrotonda(self):
        assert _F["mh665_n_guaste"](40, 12.5) == 5

    def test_n_guaste_rifiuta_quota_sopra_100(self):
        with pytest.raises(ValueError):
            _F["mh665_n_guaste"](40, 100.1)

    def test_n_guaste_rifiuta_n_frazionario(self):
        with pytest.raises(ValueError):
            _F["mh665_n_guaste"](40.5, 25.0)

    def test_vapore_perso_demo(self):
        assert _F["mh665_vapore_perso_t_anno"](
            N_GUA_DEMO, M_DOT_DEMO, 8000.0) == pytest.approx(
            VAPORE_DEMO, rel=REL)

    def test_vapore_perso_zero_a_n_gua_zero(self):
        assert _F["mh665_vapore_perso_t_anno"](
            0, M_DOT_DEMO, 8000.0) == pytest.approx(0.0)

    def test_e_termica_demo(self):
        assert _F["mh665_e_termica_mwh"](
            VAPORE_DEMO, 2.0) == pytest.approx(E_TERM_DEMO,
                                               rel=REL)

    def test_e_termica_rifiuta_h_fg_zero(self):
        with pytest.raises(ValueError):
            _F["mh665_e_termica_mwh"](VAPORE_DEMO, 0.0)

    def test_f_gas_demo(self):
        assert _F["mh665_f_gas_mwh"](
            E_TERM_DEMO, 90.0) == pytest.approx(F_GAS_DEMO,
                                                rel=REL)

    def test_f_gas_rifiuta_eta_zero(self):
        with pytest.raises(ValueError):
            _F["mh665_f_gas_mwh"](E_TERM_DEMO, 0.0)

    def test_costo_combustibile_demo(self):
        assert _F["mh665_costo_combustibile"](
            F_GAS_DEMO, 75.0) == pytest.approx(COMB_DEMO,
                                               rel=REL)

    def test_costo_ets_demo(self):
        assert _F["mh665_costo_ets"](
            F_GAS_DEMO, 0.202, 100.0) == pytest.approx(ETS_DEMO,
                                                       rel=REL)

    def test_costo_ets_zero_a_f_gas_zero(self):
        assert _F["mh665_costo_ets"](0.0, 0.202,
                                     100.0) == pytest.approx(0.0)

    def test_costo_ets_rifiuta_f_co2_negativo(self):
        with pytest.raises(ValueError):
            _F["mh665_costo_ets"](F_GAS_DEMO, -0.1, 100.0)

    def test_costo_acqua_demo(self):
        assert _F["mh665_costo_acqua"](
            VAPORE_DEMO, 3.0) == pytest.approx(ACQUA_DEMO,
                                                rel=REL)

    def test_costo_base_demo_e_somma_voci(self):
        assert _F["mh665_costo_base"](COMB_DEMO, ETS_DEMO,
                                      ACQUA_DEMO) == \
            pytest.approx(BASE_DEMO, rel=REL)
        assert BASE_DEMO == pytest.approx(
            COMB_DEMO + ETS_DEMO + ACQUA_DEMO, rel=REL)

    def test_residuo_demo(self):
        assert _F["mh665_residuo"](
            BASE_DEMO, 3.0) == pytest.approx(RESIDUO_DEMO,
                                             rel=REL)

    def test_residuo_zero_a_quota_zero(self):
        assert _F["mh665_residuo"](BASE_DEMO,
                                   0.0) == pytest.approx(0.0)

    def test_capex_demo(self):
        assert _F["mh665_capex"](
            N_GUA_DEMO, 450.0) == pytest.approx(CAPEX_DEMO,
                                                rel=REL)

    def test_capex_rifiuta_costo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh665_capex"](N_GUA_DEMO, -1.0)

    def test_risparmio_demo(self):
        assert _F["mh665_risparmio"](
            BASE_DEMO, RESIDUO_DEMO, 5000.0) == pytest.approx(
            RISP_DEMO, rel=REL)

    def test_risparmio_negativo_possibile(self):
        assert _F["mh665_risparmio"](10000.0, 2000.0,
                                     20000.0) == pytest.approx(
            -12000.0)

    def test_co2_evitata_demo(self):
        assert _F["mh665_co2_evitata_t_anno"](
            F_GAS_DEMO, F_GAS_RESIDUO_DEMO, 0.202) == \
            pytest.approx(CO2_DEMO, rel=REL)

    def test_co2_evitata_zero_se_tutto_residuo(self):
        assert _F["mh665_co2_evitata_t_anno"](
            F_GAS_DEMO, F_GAS_DEMO, 0.202) == pytest.approx(0.0)

    def test_co2_evitata_rifiuta_f_gas_negativo(self):
        with pytest.raises(ValueError):
            _F["mh665_co2_evitata_t_anno"](-1.0, 0.0, 0.202)


class TestFinanza:
    def _flussi_demo(self):
        return _F["mh665_flussi"](CAPEX_DEMO, RISP_DEMO,
                                  VITA_DEMO)

    def test_flussi_struttura(self):
        fl = self._flussi_demo()
        assert fl[0] == -CAPEX_DEMO and len(fl) == 16
        assert all(f == RISP_DEMO for f in fl[1:])

    def test_flussi_rifiuta_vita_zero(self):
        with pytest.raises(ValueError):
            _F["mh665_flussi"](4500.0, 100.0, 0)

    def test_van_demo(self):
        assert _F["mh665_van"](self._flussi_demo(),
                               0.06) == pytest.approx(VAN_DEMO,
                                                      rel=REL)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh665_van"](self._flussi_demo(), -0.01)

    def test_van_tasso_zero(self):
        fl = [-4500.0, 116326.49, 116326.49]
        assert _F["mh665_van"](fl, 0.0) == pytest.approx(
            228152.98, rel=1e-6)

    def test_tir_demo_none(self):
        # NPV > 0 a entrambi gli estremi di [-0.9999, 10]:
        # nessun cambio di segno
        assert _F["mh665_tir"](self._flussi_demo()) is None

    def test_tir_none_senza_cambio_segno(self):
        assert _F["mh665_tir"]([-100.0, -10.0, -10.0]) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh665_tir"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo(self):
        assert _F["mh665_payback"](self._flussi_demo()) == \
            PAYBACK_DEMO

    def test_payback_none_mai(self):
        assert _F["mh665_payback"]([-100.0, 1.0, 1.0]) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh665_verdetto"](VAN_DEMO, CAPEX_DEMO,
                                    RISP_DEMO, 0.10) == \
            VERDETTO_DEMO

    def test_verdetto_marginale_tolleranza_ampia(self):
        assert _F["mh665_verdetto"](-0.05 * CAPEX_DEMO,
                                    CAPEX_DEMO, RISP_DEMO,
                                    0.10) == "MARGINALE"

    def test_verdetto_non_conviente_van_oltre_tolleranza(self):
        assert _F["mh665_verdetto"](-CAPEX_DEMO, CAPEX_DEMO,
                                    RISP_DEMO, 0.10) == \
            "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_zero(self):
        assert _F["mh665_verdetto"](500.0, CAPEX_DEMO, 0.0,
                                    0.10) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_risparmio_negativo(self):
        assert _F["mh665_verdetto"](500.0, CAPEX_DEMO, -100.0,
                                    0.10) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_van_none(self):
        assert _F["mh665_verdetto"](None, CAPEX_DEMO, 100.0,
                                    0.10) == "NON_CALCOLABILE"

    def test_verdetto_rifiuta_tolleranza_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh665_verdetto"](100.0, CAPEX_DEMO, 100.0, 1.5)


class TestDemo:
    def test_demo_calcoli_end_to_end(self):
        c = _F["mh665_demo_calcoli"]()
        assert c["m_dot_kg_h"] == pytest.approx(M_DOT_DEMO,
                                                rel=REL)
        assert c["n_guaste"] == N_GUA_DEMO
        assert c["vapore_perso_t_anno"] == pytest.approx(
            VAPORE_DEMO, rel=REL)
        assert c["e_termica_mwh_anno"] == pytest.approx(
            E_TERM_DEMO, rel=REL)
        assert c["f_gas_mwh_anno"] == pytest.approx(
            F_GAS_DEMO, rel=REL)
        assert c["f_gas_residuo_mwh_anno"] == pytest.approx(
            F_GAS_RESIDUO_DEMO, rel=REL)
        assert c["costo_comb_eur_anno"] == pytest.approx(
            COMB_DEMO, rel=REL)
        assert c["costo_ets_eur_anno"] == pytest.approx(
            ETS_DEMO, rel=REL)
        assert c["costo_acqua_eur_anno"] == pytest.approx(
            ACQUA_DEMO, rel=REL)
        assert c["costo_base_eur_anno"] == pytest.approx(
            BASE_DEMO, rel=REL)
        assert c["residuo_eur_anno"] == pytest.approx(
            RESIDUO_DEMO, rel=REL)
        assert c["capex_eur"] == pytest.approx(CAPEX_DEMO,
                                               rel=REL)
        assert c["risparmio_eur_anno"] == pytest.approx(
            RISP_DEMO, rel=REL)
        assert c["co2_evitata_t_anno"] == pytest.approx(
            CO2_DEMO, rel=REL)
        assert c["van_eur"] == pytest.approx(VAN_DEMO, rel=REL)
        assert c["tir"] is None
        assert c["payback_anni"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO

    def test_demo_calcoli_deterministico(self):
        assert _F["mh665_demo_calcoli"]() == _F["mh665_demo_calcoli"]()

    def test_demo_defaults(self):
        d = _F["mh665_demo"]()
        assert d["n_trappole"] == 40
        assert d["quota_guaste_pct"] == 25.0
        assert d["pressione_bar_abs"] == 10.0
        assert d["ore_anno"] == 8000.0
        assert d["diametro_mm"] == 3.2
        assert d["h_fg_mj_kg"] == 2.0
        assert d["eta_caldaia_pct"] == 90.0
        assert d["p_gas_eur_mwh"] == 75.0
        assert d["p_ets_eur_t"] == 100.0
        assert d["f_co2_gas_t_mwh"] == 0.202
        assert d["p_acqua_eur_t"] == 3.0
        assert d["costo_trappola_eur"] == 450.0
        assert d["om_ispezione_eur_anno"] == 5000.0
        assert d["quota_residua_pct"] == 3.0
        assert d["tasso_pct"] == 6.0
        assert d["vita_anni"] == 15
        assert d["tolleranza_pct"] == 10.0

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        mh665_demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["mh665_demo_calcoli"]()
        doc = __doc__
        for chiave in ("m_dot_kg_h", "vapore_perso_t_anno",
                       "e_termica_mwh_anno", "f_gas_mwh_anno",
                       "f_gas_residuo_mwh_anno",
                       "costo_comb_eur_anno",
                       "costo_ets_eur_anno",
                       "costo_acqua_eur_anno",
                       "costo_base_eur_anno",
                       "residuo_eur_anno", "capex_eur",
                       "risparmio_eur_anno",
                       "co2_evitata_t_anno", "van_eur"):
            assert repr(c[chiave]) in doc, chiave
        assert "N_gua = round(40 x 25 %) = 10" in doc
        assert "TIR = None" in doc
        assert "payback = 1" in doc
        assert "verdetto = 'CONVIENTE'" in doc


class TestUI:
    def test_header_helpers_presente(self):
        assert '# W665 (23/10/2026) - tab665' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh665_num", "mh665_nneg", "mh665_pos",
                     "mh665_int_pos", "mh665_pct100",
                     "mh665_m_dot", "mh665_n_guaste",
                     "mh665_vapore_perso_t_anno",
                     "mh665_e_termica_mwh", "mh665_f_gas_mwh",
                     "mh665_costo_combustibile", "mh665_costo_ets",
                     "mh665_costo_acqua", "mh665_costo_base",
                     "mh665_residuo", "mh665_capex",
                     "mh665_risparmio", "mh665_co2_evitata_t_anno",
                     "mh665_flussi", "mh665_van", "mh665_tir",
                     "mh665_payback", "mh665_verdetto",
                     "mh665_demo", "mh665_demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE665) == 1

    def test_blocco_with_tab665(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab665:"

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st665_[a-z0-9_]+)"', _ui_src())
        assert len(keys) >= 20
        assert len(set(keys)) == len(keys)
        # nessuna collisione con le chiavi del ciclo precedente
        assert not any(k.startswith("st664_") for k in keys)

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_rm665 <= 0.0" in src
        assert "NON_CALCOLABILE" in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_rm665 <= 0.0") < src.index(".metric(")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Vapore perso (t/anno)" in src
        assert "Risparmio (€/anno)" in src
        assert "CO2 evitata (t/anno)" in src
        assert "Payback (anni)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd665" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_grafico_costi_presente(self):
        src = _ui_src()
        assert "plotly.graph_objects" in src
        assert "Combustibile (baseline)" in src
        assert "Perdita residua (scenario)" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert 'sep=";"' in src
        assert "trappole_vapore.csv" in src

    def test_differenziazione_da_feature_esistenti(self):
        src = _ui_src()
        assert "Napier" in src
        assert "trappole" in src.lower()

    def test_nessun_segreto_nella_sezione(self):
        assert not re.search(r'(?i)(api_key|secret|password)\s*=\s*["\']',
                             _ui_src())
