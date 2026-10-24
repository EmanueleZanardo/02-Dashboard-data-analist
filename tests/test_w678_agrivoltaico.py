"""Test tab678 "☀️🌾 Agrivoltaico: doppio raccolto, un solo terreno?"

Demo calcolata eseguendo demo_calcoli() (non a mano):
10 ettari con impianto agrivoltaico da 5000 kWp,
produzione specifica 1150 kWh/kWp; prezzo energia
90 EUR/MWh; reddito agricolo base 2500 EUR/ha con
perdita di resa 0,15 (15 %) da ombreggiamento;
costo di coltivazione 1800 EUR/ha; CAPEX 950
EUR/kWp; OPEX 14 EUR/kWp/anno; vita 25 anni; WACC
0,05 (5 %); tolleranza 0,10 (10 % del CAPEX).

- produzione_mwh = 5750.0
- ricavi_el = 517500.0
- ricavi_agri = 21250.0
- costi_agri = 18000.0
- opex_annuo = 70000.0
- margine = 450750.0
- capex_tot = 4750000.0
- crf = 0.0709524572992296
- lcoe = 70.7868125515375
- ricavo_ha = 45075.0
- van = 1602845.5131446766
- tir = 8.15158530682194 (in uscita: percentuale)
- payback = 11
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
    if (p / "w678_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w678_helpers.py via AST
    (stesso pattern di tests/appfuncs.py: niente Streamlit)."""
    src = (_new_dir() / "w678_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w678_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w678_helpers.py: {missing}")
    return out


_F = _load("mh678_num", "mh678_nneg", "mh678_pos",
           "mh678_int_pos", "mh678_quota", "mh678_pct",
           "mh678_produzione", "mh678_ricavi_el",
           "mh678_ricavi_agri", "mh678_costi_agri",
           "mh678_opex", "mh678_margine",
           "mh678_capex_tot", "mh678_crf", "mh678_lcoe",
           "mh678_ricavo_ha", "mh678_van", "mh678_tir",
           "mh678_payback", "mh678_verdetto",
           "_mh678_neutro", "mh678_calcola",
           "mh678_sensitivita", "mh678_csv",
           "mh678_demo", "demo_calcoli")

TITLE678 = ("☀️🌾 Agrivoltaico: doppio raccolto, un solo "
            "terreno?")

PROD_DEMO = 5750.0
RICAVI_EL_DEMO = 517500.0
RICAVI_AGRI_DEMO = 21250.0
COSTI_AGRI_DEMO = 18000.0
OPEX_DEMO = 70000.0
MARG_DEMO = 450750.0
CAPEX_DEMO = 4750000.0
CRF_DEMO = 0.0709524572992296
LCOE_DEMO = 70.7868125515375
RICAVO_HA_DEMO = 45075.0
VAN_DEMO = 1602845.5131446766
TIR_DEMO = 8.15158530682194
PAYBACK_DEMO = 11
VITA_DEMO = 25
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w678_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w678_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh678_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh678_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh678_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh678_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh678_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh678_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh678_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh678_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh678_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh678_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh678_int_pos"](25.0, "x") == 25

    def test_quota_rifiuta_oltre_1(self):
        with pytest.raises(ValueError):
            _F["mh678_quota"](1.01, "x")

    def test_quota_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh678_quota"](-0.01, "x")

    def test_quota_accetta_estremi(self):
        assert _F["mh678_quota"](0.0, "x") == 0.0
        assert _F["mh678_quota"](1.0, "x") == 1.0
        assert _F["mh678_quota"](0.15, "x") == 0.15

    def test_pct_rifiuta_oltre_100(self):
        with pytest.raises(ValueError):
            _F["mh678_pct"](100.01, "x")

    def test_pct_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh678_pct"](-0.01, "x")


class TestFisica:
    def test_produzione_demo(self):
        assert _F["mh678_produzione"](
            5000.0, 1150.0) == pytest.approx(PROD_DEMO,
                                             rel=REL)

    def test_produzione_formula(self):
        assert _F["mh678_produzione"](
            100.0, 1000.0) == pytest.approx(
            100.0 * 1000.0 / 1000.0, rel=1e-12)

    def test_produzione_rifiuta_potenza_zero(self):
        with pytest.raises(ValueError):
            _F["mh678_produzione"](0.0, 1150.0)

    def test_produzione_rifiuta_potenza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh678_produzione"](-10.0, 1150.0)

    def test_produzione_rifiuta_specifica_zero(self):
        with pytest.raises(ValueError):
            _F["mh678_produzione"](5000.0, 0.0)

    def test_produzione_rifiuta_specifica_negativa(self):
        with pytest.raises(ValueError):
            _F["mh678_produzione"](5000.0, -1.0)

    def test_ricavi_el_demo(self):
        assert _F["mh678_ricavi_el"](
            PROD_DEMO, 90.0) == pytest.approx(
            RICAVI_EL_DEMO, rel=REL)

    def test_ricavi_el_zero_se_prezzo_zero(self):
        assert _F["mh678_ricavi_el"](PROD_DEMO, 0.0) == 0.0

    def test_ricavi_el_rifiuta_produzione_negativa(self):
        with pytest.raises(ValueError):
            _F["mh678_ricavi_el"](-1.0, 90.0)

    def test_ricavi_el_rifiuta_prezzo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh678_ricavi_el"](PROD_DEMO, -0.01)

    def test_ricavi_agri_demo(self):
        assert _F["mh678_ricavi_agri"](
            10.0, 2500.0, 0.15) == pytest.approx(
            RICAVI_AGRI_DEMO, rel=REL)

    def test_ricavi_agri_senza_perdita(self):
        assert _F["mh678_ricavi_agri"](
            10.0, 2500.0, 0.0) == pytest.approx(
            25000.0, rel=REL)

    def test_ricavi_agri_nulli_con_perdita_totale(self):
        # perdita di resa 100 %: nessuna resa
        # agricola, il FV resta in piedi
        assert _F["mh678_ricavi_agri"](
            10.0, 2500.0, 1.0) == 0.0

    def test_ricavi_agri_rifiuta_area_zero(self):
        with pytest.raises(ValueError):
            _F["mh678_ricavi_agri"](0.0, 2500.0, 0.15)

    def test_ricavi_agri_rifiuta_base_negativo(self):
        with pytest.raises(ValueError):
            _F["mh678_ricavi_agri"](10.0, -1.0, 0.15)

    def test_ricavi_agri_rifiuta_perdita_oltre_1(self):
        with pytest.raises(ValueError):
            _F["mh678_ricavi_agri"](10.0, 2500.0, 1.01)

    def test_ricavi_agri_rifiuta_perdita_negativa(self):
        with pytest.raises(ValueError):
            _F["mh678_ricavi_agri"](10.0, 2500.0, -0.01)

    def test_costi_agri_demo(self):
        assert _F["mh678_costi_agri"](
            10.0, 1800.0) == pytest.approx(
            COSTI_AGRI_DEMO, rel=REL)

    def test_costi_agri_restano_pieni_con_ombreggiamento(
            self):
        # i costi di coltivazione non scontano la
        # perdita di resa: stesso costo con o senza
        # ombreggiamento
        assert _F["mh678_costi_agri"](
            10.0, 1800.0) == pytest.approx(
            COSTI_AGRI_DEMO, rel=REL)

    def test_costi_agri_rifiuta_area_zero(self):
        with pytest.raises(ValueError):
            _F["mh678_costi_agri"](0.0, 1800.0)

    def test_costi_agri_rifiuta_costo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh678_costi_agri"](10.0, -1.0)

    def test_opex_demo(self):
        assert _F["mh678_opex"](
            5000.0, 14.0) == pytest.approx(OPEX_DEMO,
                                           rel=REL)

    def test_opex_rifiuta_potenza_zero(self):
        with pytest.raises(ValueError):
            _F["mh678_opex"](0.0, 14.0)

    def test_opex_rifiuta_unitario_negativo(self):
        with pytest.raises(ValueError):
            _F["mh678_opex"](5000.0, -0.01)

    def test_margine_demo(self):
        assert _F["mh678_margine"](
            RICAVI_EL_DEMO, RICAVI_AGRI_DEMO,
            COSTI_AGRI_DEMO, OPEX_DEMO) == pytest.approx(
            MARG_DEMO, rel=REL)

    def test_margine_somma_due_ricavi(self):
        # il doppio raccolto: entrambi i ricavi
        # contribuiscono al margine
        m = _F["mh678_margine"](517500.0, 21250.0,
                                18000.0, 70000.0)
        assert m == pytest.approx(
            517500.0 + 21250.0 - 18000.0 - 70000.0,
            rel=1e-12)

    def test_margine_puo_essere_negativo(self):
        # 100 + 50 - 80 - 100 = -30
        assert _F["mh678_margine"](100.0, 50.0, 80.0,
                                   100.0) == -30.0

    def test_margine_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh678_margine"](float("nan"), 0.0, 0.0, 0.0)

    def test_capex_tot_demo(self):
        assert _F["mh678_capex_tot"](
            5000.0, 950.0) == pytest.approx(CAPEX_DEMO,
                                            rel=REL)

    def test_capex_tot_zero_se_unitario_zero(self):
        # (potenza_kwp, capex_eur_kwp): unitario zero
        # -> CAPEX zero
        assert _F["mh678_capex_tot"](5000.0, 0.0) == 0.0

    def test_capex_tot_rifiuta_unitario_negativo(self):
        with pytest.raises(ValueError):
            _F["mh678_capex_tot"](5000.0, -1.0)

    def test_capex_tot_rifiuta_potenza_zero(self):
        with pytest.raises(ValueError):
            _F["mh678_capex_tot"](0.0, 950.0)

    def test_crf_demo(self):
        assert _F["mh678_crf"](
            0.05, 25) == pytest.approx(CRF_DEMO, rel=REL)

    def test_crf_wacc_zero(self):
        assert _F["mh678_crf"](
            0.0, 25) == pytest.approx(1.0 / 25.0, rel=1e-12)

    def test_crf_rifiuta_wacc_negativo(self):
        with pytest.raises(ValueError):
            _F["mh678_crf"](-0.01, 25)

    def test_crf_rifiuta_vita_zero(self):
        with pytest.raises(ValueError):
            _F["mh678_crf"](0.05, 0)

    def test_lcoe_demo(self):
        assert _F["mh678_lcoe"](
            CAPEX_DEMO, CRF_DEMO, OPEX_DEMO,
            PROD_DEMO) == pytest.approx(LCOE_DEMO, rel=REL)

    def test_lcoe_formula(self):
        c, f, o, e = 4.75e6, 0.0709524, 70000.0, 5750.0
        assert _F["mh678_lcoe"](
            c, f, o, e) == pytest.approx((c * f + o) / e,
                                         rel=1e-9)

    def test_lcoe_sotto_prezzo_energia_demo(self):
        # margine elettrico per MWh positivo nella
        # demo: ogni MWh crea valore
        assert LCOE_DEMO < 90.0
        assert 90.0 - LCOE_DEMO == pytest.approx(
            19.2131874484625, rel=1e-9)

    def test_lcoe_solo_elettrico(self):
        # il LCOE non include i ricavi agricoli:
        # stesso valore con o senza agricoltura
        assert _F["mh678_lcoe"](
            CAPEX_DEMO, CRF_DEMO, OPEX_DEMO,
            PROD_DEMO) == pytest.approx(LCOE_DEMO, rel=REL)

    def test_lcoe_rifiuta_produzione_zero(self):
        with pytest.raises(ValueError):
            _F["mh678_lcoe"](CAPEX_DEMO, CRF_DEMO,
                             OPEX_DEMO, 0.0)

    def test_ricavo_ha_demo(self):
        assert _F["mh678_ricavo_ha"](
            MARG_DEMO, 10.0) == pytest.approx(
            RICAVO_HA_DEMO, rel=REL)

    def test_ricavo_ha_formula(self):
        assert _F["mh678_ricavo_ha"](
            90000.0, 20.0) == pytest.approx(
            4500.0, rel=1e-12)

    def test_ricavo_ha_rifiuta_area_zero(self):
        with pytest.raises(ValueError):
            _F["mh678_ricavo_ha"](MARG_DEMO, 0.0)

    def test_ricavo_ha_accetta_margine_negativo(self):
        assert _F["mh678_ricavo_ha"](-1000.0, 10.0) == -100.0


class TestFinanza:
    def test_van_demo(self):
        assert _F["mh678_van"](
            MARG_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) == pytest.approx(VAN_DEMO, rel=REL)

    def test_van_tasso_zero(self):
        assert _F["mh678_van"](
            MARG_DEMO, CAPEX_DEMO, 0.0,
            25) == pytest.approx(
            -CAPEX_DEMO + MARG_DEMO * 25, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh678_van"](MARG_DEMO, CAPEX_DEMO, -0.01, 25)

    def test_van_rifiuta_capex_negativo(self):
        with pytest.raises(ValueError):
            _F["mh678_van"](MARG_DEMO, -1.0, 0.05, 25)

    def test_tir_demo(self):
        # mh678_tir ritorna la frazione; il calcola la
        # converte in percentuale
        assert _F["mh678_tir"](
            CAPEX_DEMO, MARG_DEMO,
            VITA_DEMO) == pytest.approx(TIR_DEMO / 100.0,
                                       rel=1e-9)

    def test_tir_none_se_margine_non_positivo(self):
        assert _F["mh678_tir"](CAPEX_DEMO, 0.0, 25) is None
        assert _F["mh678_tir"](CAPEX_DEMO, -100.0, 25) is None

    def test_tir_none_se_capex_zero(self):
        # CAPEX = 0 con margine positivo: nessun cambio
        # di segno nei flussi -> None
        assert _F["mh678_tir"](0.0, MARG_DEMO, 25) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh678_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo(self):
        assert _F["mh678_payback"](
            CAPEX_DEMO, MARG_DEMO,
            VITA_DEMO) == PAYBACK_DEMO

    def test_payback_anno_1_se_margine_ge_capex(self):
        assert _F["mh678_payback"](1000.0, 1000.0, 25) == 1
        assert _F["mh678_payback"](1000.0, 2000.0, 25) == 1

    def test_payback_none_mai(self):
        assert _F["mh678_payback"](CAPEX_DEMO, 1.0, 25) is None

    def test_payback_none_se_margine_non_positivo(self):
        assert _F["mh678_payback"](CAPEX_DEMO, 0.0, 25) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh678_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10,
            MARG_DEMO) == VERDETTO_DEMO

    def test_verdetto_marginale_ad_hoc(self):
        # |VAN| = 100000 <= 0.10 x 4750000
        assert _F["mh678_verdetto"](
            -100000.0, CAPEX_DEMO, 0.10,
            MARG_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        # |VAN| = 500000 > 0.10 x 4750000
        assert _F["mh678_verdetto"](
            -500000.0, CAPEX_DEMO, 0.10,
            MARG_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_margine_non_positivo(
            self):
        assert _F["mh678_verdetto"](
            1000.0, CAPEX_DEMO, 0.10,
            0.0) == "NON_CALCOLABILE"
        assert _F["mh678_verdetto"](
            1000.0, CAPEX_DEMO, 0.10,
            -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_non_negativo_conviente(
            self):
        assert _F["mh678_verdetto"](
            0.0, 0.0, 0.10, MARG_DEMO) == "CONVIENTE"
        assert _F["mh678_verdetto"](
            1000.0, 0.0, 0.10, MARG_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(
            self):
        # CAPEX == 0: tolleranza zero, mai MARGINALE
        assert _F["mh678_verdetto"](
            -1.0, 0.0, 0.10, MARG_DEMO) == "NON_CONVIENTE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh678_verdetto"](100.0, CAPEX_DEMO, -0.01,
                                 MARG_DEMO)


class TestGuard:
    def _bc(self, **kw):
        d = _F["mh678_demo"]()
        d.update(kw)
        return _F["mh678_calcola"](**d)

    def test_area_zero_neutro(self):
        n = self._bc(area_ha=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["produzione_mwh"] == 0.0
        assert n["margine"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_area_negativa_neutro(self):
        n = self._bc(area_ha=-5.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_potenza_zero_neutro(self):
        n = self._bc(potenza_kwp=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_potenza_negativa_neutro(self):
        n = self._bc(potenza_kwp=-100.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_produzione_specifica_zero_neutro(self):
        n = self._bc(produzione_specifica_kwh_kwp=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_produzione_specifica_negativa_neutro(self):
        n = self._bc(produzione_specifica_kwh_kwp=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzo_negativo_neutro(self):
        n = self._bc(prezzo_energia_eur_mwh=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_ricavo_base_negativo_neutro(self):
        n = self._bc(ricavo_agricolo_base_eur_ha=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_perdita_resa_oltre_1_neutro(self):
        n = self._bc(perdita_resa=1.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_perdita_resa_negativa_neutro(self):
        n = self._bc(perdita_resa=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_costo_coltivazione_negativo_neutro(self):
        n = self._bc(costo_coltivazione_eur_ha=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_capex_negativo_neutro(self):
        n = self._bc(capex_eur_kwp=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_opex_negativo_neutro(self):
        n = self._bc(opex_eur_kwp=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_non_intera_neutro(self):
        n = self._bc(vita_anni=24.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_negativo_neutro(self):
        n = self._bc(wacc=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_negativa_neutro(self):
        n = self._bc(tolleranza=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(prezzo_energia_eur_mwh=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["ricavi_el"] == 0.0

    def test_bool_neutro(self):
        n = self._bc(potenza_kwp=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzo_zero_margine_negativo_neutro(self):
        # prezzo nullo: ricavi elettrici 0, costi e
        # OPEX positivi -> margine < 0 -> neutro
        n = self._bc(prezzo_energia_eur_mwh=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["margine"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_prezzo_basso_margine_non_positivo_neutro(self):
        # 10 EUR/MWh: ricavi 57500 < costi+OPEX 88000
        n = self._bc(prezzo_energia_eur_mwh=10.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_perdita_resa_totale_calcolabile(self):
        # perdita 100 %: ricavi agricoli zero ma il
        # business elettrico resta in piedi
        n = self._bc(perdita_resa=1.0)
        assert n["ricavi_agri"] == 0.0
        assert n["verdetto"] != "NON_CALCOLABILE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh678_neutro"]()
        assert list(n["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(n["df_flussi"]) == 0
        assert list(n["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(n["df_tabella"]) == 0

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh678_neutro"]()
        for chiave in ("produzione_mwh", "ricavi_el",
                       "ricavi_agri", "costi_agri",
                       "opex_annuo", "margine",
                       "capex_tot", "crf", "lcoe",
                       "ricavo_ha", "van", "tir",
                       "payback", "verdetto", "df_flussi",
                       "df_tabella"):
            assert chiave in n, chiave

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert list(b["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(b["df_tabella"]) == 11
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Produzione annua (MWh/anno)" in voci
        assert "LCOE elettrico (EUR/MWh)" in voci
        assert "Margine operativo (EUR/anno)" in voci
        assert "Ricavo doppio raccolto (EUR/ha/anno)" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(b["df_flussi"]) == VITA_DEMO + 1
        assert b["df_flussi"]["Cumulato (€)"].iloc[-1] == \
            pytest.approx(-CAPEX_DEMO + MARG_DEMO * VITA_DEMO,
                          rel=REL)


class TestSensitivitaCsv:
    def _ing(self):
        return _F["mh678_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh678_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["Perdita resa 0 %",
                                   "Perdita resa 15 %",
                                   "Perdita resa 30 %"]
        assert list(s.index) == ["x0.8", "x1.0", "x1.2"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh678_sensitivita"](self._ing())
        assert s.loc["x1.0", "Perdita resa 15 %"] == \
            pytest.approx(VAN_DEMO, rel=REL)

    def test_sensitivita_monotona(self):
        # VAN cresce col prezzo energia e cala con la
        # perdita di resa da ombreggiamento
        s = _F["mh678_sensitivita"](self._ing())
        centro = s.loc["x1.0", "Perdita resa 15 %"]
        assert s.loc["x1.2", "Perdita resa 0 %"] > centro
        assert s.loc["x0.8", "Perdita resa 30 %"] < centro
        assert s.loc["x1.0", "Perdita resa 0 %"] > centro
        assert s.loc["x1.0", "Perdita resa 30 %"] < centro

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh678_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 26

    def test_csv_contiene_verdetto_e_lcoe(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh678_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "lcoe_elettrico_eur_mwh" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "ricavo_doppio_raccolto_eur_ha_anno" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh678_csv"](bc, self._ing())
        assert f"produzione_mwh_anno;{PROD_DEMO}" in txt
        assert f"margine_eur_anno;{MARG_DEMO}" in txt
        assert f"ricavi_agricoltura_eur_anno;{RICAVI_AGRI_DEMO}" \
            in txt


class TestDemo:
    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["produzione_mwh"] == pytest.approx(
            PROD_DEMO, rel=REL)
        assert c["ricavi_el"] == pytest.approx(
            RICAVI_EL_DEMO, rel=REL)
        assert c["ricavi_agri"] == pytest.approx(
            RICAVI_AGRI_DEMO, rel=REL)
        assert c["costi_agri"] == pytest.approx(
            COSTI_AGRI_DEMO, rel=REL)
        assert c["opex_annuo"] == pytest.approx(
            OPEX_DEMO, rel=REL)
        assert c["margine"] == pytest.approx(
            MARG_DEMO, rel=REL)
        assert c["capex_tot"] == pytest.approx(
            CAPEX_DEMO, rel=REL)
        assert c["crf"] == pytest.approx(CRF_DEMO, rel=REL)
        assert c["lcoe"] == pytest.approx(
            LCOE_DEMO, rel=REL)
        assert c["ricavo_ha"] == pytest.approx(
            RICAVO_HA_DEMO, rel=REL)
        assert c["van"] == pytest.approx(VAN_DEMO, rel=REL)
        assert c["tir"] == pytest.approx(TIR_DEMO, rel=REL)
        assert c["payback"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()[
            "van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()[
            "lcoe"] == _F["demo_calcoli"]()["lcoe"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        """mh678_calcola(**mh678_demo()) deve matchare le
        costanti _DEMO entro 1e-9 relativo (mismatch
        vietato), chiave per chiave."""
        d = _F["mh678_demo"]()
        b = _F["mh678_calcola"](**d)
        coppie = [("produzione_mwh", PROD_DEMO),
                  ("ricavi_el", RICAVI_EL_DEMO),
                  ("ricavi_agri", RICAVI_AGRI_DEMO),
                  ("costi_agri", COSTI_AGRI_DEMO),
                  ("opex_annuo", OPEX_DEMO),
                  ("margine", MARG_DEMO),
                  ("capex_tot", CAPEX_DEMO),
                  ("crf", CRF_DEMO),
                  ("lcoe", LCOE_DEMO),
                  ("ricavo_ha", RICAVO_HA_DEMO),
                  ("van", VAN_DEMO),
                  ("tir", TIR_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh678_demo"]()
        assert d["area_ha"] == 10.0
        assert d["potenza_kwp"] == 5000.0
        assert d["produzione_specifica_kwh_kwp"] == 1150.0
        assert d["prezzo_energia_eur_mwh"] == 90.0
        assert d["ricavo_agricolo_base_eur_ha"] == 2500.0
        assert d["perdita_resa"] == 0.15
        assert d["costo_coltivazione_eur_ha"] == 1800.0
        assert d["capex_eur_kwp"] == 950.0
        assert d["opex_eur_kwp"] == 14.0
        assert d["vita_anni"] == 25
        assert d["wacc"] == 0.05
        assert d["tolleranza"] == 0.10

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("produzione_mwh", "ricavi_el",
                       "ricavi_agri", "costi_agri",
                       "opex_annuo", "margine",
                       "capex_tot", "crf", "lcoe",
                       "ricavo_ha", "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 11" in doc
        assert "verdetto = 'CONVIENTE'" in doc


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def678["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def678\["([a-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) >= 12, ui_keys
        demo_keys = set(_F["mh678_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestUI:
    def test_header_helpers_presente(self):
        assert '# W678 (24/10/2026) - tab678' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh678_num", "mh678_nneg", "mh678_pos",
                     "mh678_int_pos", "mh678_quota",
                     "mh678_pct", "mh678_produzione",
                     "mh678_ricavi_el", "mh678_ricavi_agri",
                     "mh678_costi_agri", "mh678_opex",
                     "mh678_margine", "mh678_capex_tot",
                     "mh678_crf", "mh678_lcoe",
                     "mh678_ricavo_ha", "mh678_van",
                     "mh678_tir", "mh678_payback",
                     "mh678_verdetto", "_mh678_neutro",
                     "mh678_calcola", "mh678_sensitivita",
                     "mh678_csv", "mh678_demo",
                     "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE678) == 1

    def test_blocco_with_tab678(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab678:"

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st678_[a-z0-9_]+)"', _ui_src())
        assert len(keys) >= 14
        assert len(set(keys)) == len(keys)
        # nessuna collisione con le chiavi dei cicli precedenti
        assert not any(k.startswith("st677_") for k in keys)
        assert not any(k.startswith("st676_") for k in keys)
        assert not any(k.startswith("st675_") for k in keys)

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg678" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg678") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg678")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Produzione (MWh/anno)" in src
        assert "Doppio raccolto (€/ha/anno)" in src
        assert "VAN (€)" in src
        assert "TIR / Payback" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd678" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_lcoe_vs_prezzo_presente(self):
        src = _ui_src()
        assert "LCOE vs prezzo" in src
        assert "margine per MWh" in src
        assert "prezzo energia" in src

    def test_nota_doppio_raccolto_vs_fv_a_terra_presente(
            self):
        src = _ui_src()
        assert "FV a terra" in src
        assert "ombreggiamento" in src
        assert "doppio raccolto" in src.lower()

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Ricavi elettricit" in src
        assert "Ricavi agricoltura" in src
        assert "Margine doppio raccolto" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert 'sep=";"' in src or "mh678_csv" in src
        assert "agrivoltaico_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitiv" in src
        assert "mh678_sensitivita" in src
        assert "Heatmap" in src
        assert "Prezzo energia" in src
        assert "Perdita di resa" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st678_show_flussi" in src
        assert "st.checkbox" in src

    def test_differenziazione_da_feature_esistenti(self):
        src = _ui_src()
        assert "agrivoltaico" in src
        assert "doppio raccolto" in src.lower()
        assert "ombreggiamento" in src


class TestApplyContract:
    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE678

    def test_ancora_helper_presente(self):
        assert "# W678 (24/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab678:")
        assert "mh678_calcola" in _helpers_src()
        assert "demo_calcoli" in _helpers_src()
        assert "import streamlit" not in _helpers_src()
        assert "tab678" in (_new_dir() / "w678_test.py")\
            .read_text(encoding="utf-8")


class TestSegreti:
    def test_nessun_segreto_nei_file(self):
        for fn in ("w678_helpers.py", "w678_ui.py",
                   "w678_test.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            assert not re.search(
                r"(?i)(api[_-]?key|secret|password|passwd|token)"
                r"\s*=\s*[\"']",
                src), fn
