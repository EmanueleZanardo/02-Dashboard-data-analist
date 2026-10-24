"""Test tab692 "🔋♻️ Second life batterie EV: il riuso stazionario paga?"

Demo calcolata eseguendo demo_calcoli() (non a mano):
pacchi 120/anno; capacita' pacco 75 kWh;
SoH 0,70; resa selezione 0,75; costo
acquisto 2000 EUR/pacco; costo test 600
EUR/pacco; prezzo vendita 150 EUR/kWh;
ricavo servizi 8 EUR/kWh/anno; OPEX fisso
60000 EUR/anno; CAPEX 600000 EUR; vita 10
anni; WACC 0,06 (6 %); tolleranza 0,10
(10 % del CAPEX); fattore CO2 0,06 t/kWh.

- kwh_usabili_pacco_kwh = 52.5
- pacchi_venduti = 90.0
- kwh_venduti_kwh_a = 4725.0
- ricavi_vendita_eur_a = 708750.0
- ricavi_servizi_eur_a = 37800.0
- ricavi_tot_eur_a = 746550.0
- costi_acquisto_eur_a = 240000.0
- costi_test_eur_a = 72000.0
- opex_fisso_eur_a = 60000.0
- costi_tot_eur_a = 372000.0
- margine_eur_a = 374550.0
- co2_evitata_t_a = 283.5
- capex_eur = 600000.0
- van = 2156720.6051073773
- tir = 61.921124264620865
- payback = 2
- verdetto = 'CONVIENTE'

Scomposizione: kWh usabili 75 x 0,70 = 52,5;
pacchi venduti 120 x 0,75 = 90 (reale, non
arrotondato); kWh venduti 90 x 52,5 = 4725;
ricavi vendita 4725 x 150 = 708750; servizi
4725 x 8 = 37800; ricavi 746550; acquisto
120 x 2000 = 240000; test 120 x 600 = 72000;
costi 240000 + 72000 + 60000 = 372000;
margine 746550 - 372000 = 374550; CO2
4725 x 0,06 = 283,5 t.
"""

import ast
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w692_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w692_helpers.py via AST
    (stesso pattern di tests/appfuncs.py: niente Streamlit)."""
    src = (_new_dir() / "w692_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w692_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w692_helpers.py: {missing}")
    return out


_F = _load("mh692_num", "mh692_nneg", "mh692_pos",
           "mh692_int_pos", "mh692_frac", "mh692_tol",
           "mh692_kwh_usabili_pacco",
           "mh692_pacchi_venduti", "mh692_kwh_venduti",
           "mh692_ricavi_vendita", "mh692_ricavi_servizi",
           "mh692_ricavi_tot", "mh692_costi_acquisto",
           "mh692_costi_test", "mh692_costi_tot",
           "mh692_margine", "mh692_co2", "mh692_capex",
           "mh692_van", "mh692_tir",
           "mh692_payback", "mh692_verdetto",
           "_mh692_neutro", "mh692_calcola",
           "mh692_sensitivita", "mh692_csv",
           "mh692_demo", "demo_calcoli")

TITLE692 = ("🔋♻️ Second life batterie EV: "
            "il riuso stazionario paga?")

KU_DEMO = 52.5
PVEND_DEMO = 90.0
KV_DEMO = 4725.0
RVEND_DEMO = 708750.0
RSERV_DEMO = 37800.0
RTOT_DEMO = 746550.0
CACQ_DEMO = 240000.0
CTEST_DEMO = 72000.0
OPEX_DEMO = 60000.0
CTOT_DEMO = 372000.0
MARG_DEMO = 374550.0
CO2_DEMO = 283.5
CAPEX_DEMO = 600000.0
VAN_DEMO = 2156720.6051073773
TIR_DEMO = 61.921124264620865
PAYBACK_DEMO = 2
VITA_DEMO = 10
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w692_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w692_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh692_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh692_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh692_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh692_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh692_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh692_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh692_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh692_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh692_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh692_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh692_int_pos"](10.0, "x") == 10

    def test_tol_rifiuta_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh692_tol"](1.01, "x")

    def test_tol_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh692_tol"](-0.01, "x")

    def test_tol_accetta_estremi(self):
        assert _F["mh692_tol"](0.0, "x") == 0.0
        assert _F["mh692_tol"](1.0, "x") == 1.0

    def test_frac_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh692_frac"](0.0, "x")

    def test_frac_rifiuta_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh692_frac"](1.01, "x")

    def test_frac_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh692_frac"](-0.01, "x")

    def test_frac_accetta_uno(self):
        assert _F["mh692_frac"](1.0, "x") == 1.0

    def test_frac_accetta_demo(self):
        assert _F["mh692_frac"](0.70, "x") == 0.70
        assert _F["mh692_frac"](0.75, "x") == 0.75


class TestFisicaEconomia:
    def test_kwh_usabili_demo(self):
        assert _F["mh692_kwh_usabili_pacco"](
            75.0, 0.70) == pytest.approx(KU_DEMO, rel=REL)

    def test_kwh_usabili_formula(self):
        assert _F["mh692_kwh_usabili_pacco"](
            100.0, 0.5) == pytest.approx(50.0, rel=1e-12)

    def test_kwh_usabili_rifiuta_capacita_zero(self):
        with pytest.raises(ValueError):
            _F["mh692_kwh_usabili_pacco"](0.0, 0.70)

    def test_kwh_usabili_rifiuta_soh_zero(self):
        with pytest.raises(ValueError):
            _F["mh692_kwh_usabili_pacco"](75.0, 0.0)

    def test_kwh_usabili_rifiuta_soh_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh692_kwh_usabili_pacco"](75.0, 1.01)

    def test_pacchi_venduti_demo(self):
        assert _F["mh692_pacchi_venduti"](
            120, 0.75) == pytest.approx(PVEND_DEMO, rel=REL)

    def test_pacchi_venduti_non_arrotondato(self):
        # Quantita' attesa annua: 121 x 0,75 = 90,75
        assert _F["mh692_pacchi_venduti"](
            121, 0.75) == pytest.approx(90.75, rel=1e-12)

    def test_pacchi_venduti_rifiuta_frazione_pacchi(self):
        with pytest.raises(ValueError):
            _F["mh692_pacchi_venduti"](120.5, 0.75)

    def test_pacchi_venduti_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh692_pacchi_venduti"](0, 0.75)

    def test_kwh_venduti_demo(self):
        assert _F["mh692_kwh_venduti"](
            PVEND_DEMO, KU_DEMO) == pytest.approx(
            KV_DEMO, rel=REL)

    def test_ricavi_vendita_demo(self):
        assert _F["mh692_ricavi_vendita"](
            KV_DEMO, 150.0) == pytest.approx(
            RVEND_DEMO, rel=REL)

    def test_ricavi_vendita_rifiuta_prezzo_zero(self):
        with pytest.raises(ValueError):
            _F["mh692_ricavi_vendita"](KV_DEMO, 0.0)

    def test_ricavi_servizi_demo(self):
        assert _F["mh692_ricavi_servizi"](
            KV_DEMO, 8.0) == pytest.approx(
            RSERV_DEMO, rel=REL)

    def test_ricavi_servizi_zero(self):
        assert _F["mh692_ricavi_servizi"](KV_DEMO, 0.0) == 0.0

    def test_ricavi_tot_demo(self):
        assert _F["mh692_ricavi_tot"](
            RVEND_DEMO, RSERV_DEMO) == pytest.approx(
            RTOT_DEMO, rel=REL)

    def test_ricavi_tot_rifiuta_negativi(self):
        with pytest.raises(ValueError):
            _F["mh692_ricavi_tot"](-1.0, RSERV_DEMO)

    def test_costi_acquisto_demo(self):
        assert _F["mh692_costi_acquisto"](
            120, 2000.0) == pytest.approx(
            CACQ_DEMO, rel=REL)

    def test_costi_test_demo(self):
        assert _F["mh692_costi_test"](
            120, 600.0) == pytest.approx(
            CTEST_DEMO, rel=REL)

    def test_costi_tot_demo(self):
        assert _F["mh692_costi_tot"](
            CACQ_DEMO, CTEST_DEMO,
            OPEX_DEMO) == pytest.approx(CTOT_DEMO, rel=REL)

    def test_margine_demo(self):
        assert _F["mh692_margine"](
            RTOT_DEMO, CTOT_DEMO) == pytest.approx(
            MARG_DEMO, rel=REL)

    def test_margine_puo_essere_negativo(self):
        assert _F["mh692_margine"](100.0, 200.0) == -100.0

    def test_co2_demo(self):
        assert _F["mh692_co2"](
            KV_DEMO, 0.06) == pytest.approx(CO2_DEMO, rel=REL)

    def test_co2_zero_se_nessun_kwh(self):
        assert _F["mh692_co2"](0.0, 0.06) == 0.0

    def test_co2_rifiuta_fattore_negativo(self):
        with pytest.raises(ValueError):
            _F["mh692_co2"](KV_DEMO, -0.01)

    def test_capex_demo(self):
        assert _F["mh692_capex"](600000.0) == pytest.approx(
            CAPEX_DEMO, rel=REL)

    def test_capex_zero(self):
        assert _F["mh692_capex"](0.0) == 0.0

    def test_capex_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh692_capex"](-1.0)


class TestFinanza:
    def test_van_demo(self):
        assert _F["mh692_van"](
            MARG_DEMO, CAPEX_DEMO, 0.06,
            VITA_DEMO) == pytest.approx(VAN_DEMO, rel=REL)

    def test_van_formula_chiusa(self):
        atteso = -CAPEX_DEMO + MARG_DEMO * (
            1.0 - 1.06 ** (-10)) / 0.06
        assert _F["mh692_van"](
            MARG_DEMO, CAPEX_DEMO, 0.06,
            VITA_DEMO) == pytest.approx(atteso, rel=1e-12)

    def test_van_tasso_zero(self):
        assert _F["mh692_van"](
            MARG_DEMO, CAPEX_DEMO, 0.0,
            10) == pytest.approx(
            -CAPEX_DEMO + MARG_DEMO * 10, rel=1e-12)

    def test_van_tasso_zero_valore(self):
        assert -CAPEX_DEMO + MARG_DEMO * 10 == pytest.approx(
            3145500.0, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh692_van"](MARG_DEMO, CAPEX_DEMO, -0.01, 10)

    def test_van_rifiuta_capex_negativo(self):
        with pytest.raises(ValueError):
            _F["mh692_van"](MARG_DEMO, -1.0, 0.06, 10)

    def test_tir_demo(self):
        assert _F["mh692_tir"](
            CAPEX_DEMO, MARG_DEMO,
            VITA_DEMO) == pytest.approx(TIR_DEMO / 100.0,
                                        rel=1e-9)

    def test_tir_none_se_margine_non_positivo(self):
        assert _F["mh692_tir"](CAPEX_DEMO, 0.0, 10) is None
        assert _F["mh692_tir"](CAPEX_DEMO, -100.0, 10) is None

    def test_tir_none_se_capex_zero(self):
        assert _F["mh692_tir"](0.0, MARG_DEMO, 10) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh692_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_verifica_npv_zero(self):
        tir = _F["mh692_tir"](CAPEX_DEMO, MARG_DEMO,
                              VITA_DEMO)
        npv = -CAPEX_DEMO + sum(
            MARG_DEMO / (1.0 + tir) ** i
            for i in range(1, 11))
        assert abs(npv) <= 1e-6 * CAPEX_DEMO

    def test_payback_demo(self):
        assert _F["mh692_payback"](
            CAPEX_DEMO, MARG_DEMO,
            VITA_DEMO) == PAYBACK_DEMO

    def test_payback_primo_anno_cumulato_non_negativo(self):
        assert -CAPEX_DEMO + MARG_DEMO * 1 < 0.0
        assert -CAPEX_DEMO + MARG_DEMO * 2 >= 0.0

    def test_payback_ceil_coerente(self):
        assert _F["mh692_payback"](1000.0, 300.0, 10) == 4

    def test_payback_anno_1_se_margine_ge_capex(self):
        assert _F["mh692_payback"](1000.0, 1000.0, 10) == 1
        assert _F["mh692_payback"](1000.0, 2000.0, 10) == 1

    def test_payback_none_se_mai_entro_vita(self):
        # -5000000 + 374550 x 10 = -1254500 < 0 -> None
        assert _F["mh692_payback"](
            5000000.0, MARG_DEMO, 10) is None

    def test_payback_zero_se_capex_zero(self):
        assert _F["mh692_payback"](0.0, MARG_DEMO, 10) == 0

    def test_payback_none_se_margine_non_positivo(self):
        assert _F["mh692_payback"](CAPEX_DEMO, 0.0, 10) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh692_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10,
            MARG_DEMO) == VERDETTO_DEMO

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh692_verdetto"](
            -10000.0, CAPEX_DEMO, 0.10,
            MARG_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh692_verdetto"](
            -60000.0, CAPEX_DEMO, 0.10,
            MARG_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh692_verdetto"](
            -60001.0, CAPEX_DEMO, 0.10,
            MARG_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_margine_non_positivo(
            self):
        assert _F["mh692_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh692_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_non_negativo_conviente(
            self):
        assert _F["mh692_verdetto"](
            0.0, 0.0, 0.10, MARG_DEMO) == "CONVIENTE"
        assert _F["mh692_verdetto"](
            1000.0, 0.0, 0.10, MARG_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(
            self):
        assert _F["mh692_verdetto"](
            -1.0, 0.0, 0.10, MARG_DEMO) == "NON_CONVIENTE"

    def test_verdetto_capex_zero_mai_marginale(self):
        assert _F["mh692_verdetto"](
            -1.0, 0.0, 0.10, MARG_DEMO) != "MARGINALE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh692_verdetto"](100.0, CAPEX_DEMO, -0.01,
                                 MARG_DEMO)

    def test_verdetto_rifiuta_tolleranza_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh692_verdetto"](100.0, CAPEX_DEMO, 1.01,
                                 MARG_DEMO)


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh692_demo"]()
        d.update(kw)
        return _F["mh692_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["kwh_usabili_pacco_kwh"] == pytest.approx(
            KU_DEMO, rel=REL)
        assert c["pacchi_venduti"] == pytest.approx(
            PVEND_DEMO, rel=REL)
        assert c["kwh_venduti_kwh_a"] == pytest.approx(
            KV_DEMO, rel=REL)
        assert c["ricavi_vendita_eur_a"] == pytest.approx(
            RVEND_DEMO, rel=REL)
        assert c["ricavi_servizi_eur_a"] == pytest.approx(
            RSERV_DEMO, rel=REL)
        assert c["ricavi_tot_eur_a"] == pytest.approx(
            RTOT_DEMO, rel=REL)
        assert c["costi_acquisto_eur_a"] == pytest.approx(
            CACQ_DEMO, rel=REL)
        assert c["costi_test_eur_a"] == pytest.approx(
            CTEST_DEMO, rel=REL)
        assert c["costi_tot_eur_a"] == pytest.approx(
            CTOT_DEMO, rel=REL)
        assert c["margine_eur_a"] == pytest.approx(
            MARG_DEMO, rel=REL)
        assert c["co2_evitata_t_a"] == pytest.approx(
            CO2_DEMO, rel=REL)
        assert c["capex_eur"] == pytest.approx(
            CAPEX_DEMO, rel=REL)
        assert c["van"] == pytest.approx(VAN_DEMO, rel=REL)
        assert c["tir"] == pytest.approx(TIR_DEMO, rel=REL)
        assert c["payback"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()[
            "van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()[
            "co2_evitata_t_a"] == _F["demo_calcoli"]()[
            "co2_evitata_t_a"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        """mh692_calcola(**mh692_demo()) deve matchare le
        costanti _DEMO entro 1e-9 relativo (mismatch
        vietato), chiave per chiave."""
        d = _F["mh692_demo"]()
        b = _F["mh692_calcola"](**d)
        coppie = [("kwh_usabili_pacco_kwh", KU_DEMO),
                  ("pacchi_venduti", PVEND_DEMO),
                  ("kwh_venduti_kwh_a", KV_DEMO),
                  ("ricavi_vendita_eur_a", RVEND_DEMO),
                  ("ricavi_servizi_eur_a", RSERV_DEMO),
                  ("ricavi_tot_eur_a", RTOT_DEMO),
                  ("costi_acquisto_eur_a", CACQ_DEMO),
                  ("costi_test_eur_a", CTEST_DEMO),
                  ("costi_tot_eur_a", CTOT_DEMO),
                  ("margine_eur_a", MARG_DEMO),
                  ("co2_evitata_t_a", CO2_DEMO),
                  ("capex_eur", CAPEX_DEMO),
                  ("van", VAN_DEMO),
                  ("tir", TIR_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh692_demo"]()
        assert d["pacchi_anno"] == 120
        assert d["capacita_pacco_kwh"] == 75.0
        assert d["soh_frac"] == 0.70
        assert d["resa_selezione_frac"] == 0.75
        assert d["costo_acquisto_eur_pacco"] == 2000.0
        assert d["costo_test_eur_pacco"] == 600.0
        assert d["prezzo_vendita_eur_kwh"] == 150.0
        assert d["ricavo_servizi_eur_kwh_a"] == 8.0
        assert d["opex_fisso_eur_a"] == 60000.0
        assert d["capex_eur"] == 600000.0
        assert d["vita_a"] == 10
        assert d["wacc_frac"] == 0.06
        assert d["toll_frac"] == 0.10
        assert d["fattore_co2_t_kwh"] == 0.06

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("kwh_usabili_pacco_kwh",
                       "pacchi_venduti",
                       "kwh_venduti_kwh_a",
                       "ricavi_vendita_eur_a",
                       "ricavi_servizi_eur_a",
                       "ricavi_tot_eur_a",
                       "costi_acquisto_eur_a",
                       "costi_test_eur_a",
                       "costi_tot_eur_a",
                       "margine_eur_a",
                       "co2_evitata_t_a",
                       "capex_eur", "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 2" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_pacchi_zero_neutro(self):
        n = self._bc(pacchi_anno=0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["margine_eur_a"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_pacchi_negativo_neutro(self):
        n = self._bc(pacchi_anno=-10)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_pacchi_frazione_neutro(self):
        n = self._bc(pacchi_anno=120.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_capacita_zero_neutro(self):
        n = self._bc(capacita_pacco_kwh=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_soh_zero_neutro(self):
        n = self._bc(soh_frac=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_soh_oltre_uno_neutro(self):
        n = self._bc(soh_frac=1.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_soh_uno_calcolabile(self):
        # SoH 1,0: kWh 75, venduti 90, kWh 6750,
        # vendita 1012500, servizi 54000, ricavi
        # 1066500, margine 694500
        n = self._bc(soh_frac=1.0)
        assert n["valid"] is True
        assert n["kwh_usabili_pacco_kwh"] == pytest.approx(
            75.0, rel=REL)
        assert n["margine_eur_a"] == pytest.approx(
            694500.0, rel=REL)

    def test_resa_zero_neutro(self):
        n = self._bc(resa_selezione_frac=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_resa_oltre_uno_neutro(self):
        n = self._bc(resa_selezione_frac=1.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_resa_uno_calcolabile(self):
        # Resa 1,0: venduti 120, kWh 6300, vendita
        # 945000, servizi 50400, ricavi 995400,
        # margine 623400
        n = self._bc(resa_selezione_frac=1.0)
        assert n["valid"] is True
        assert n["pacchi_venduti"] == pytest.approx(
            120.0, rel=REL)
        assert n["margine_eur_a"] == pytest.approx(
            623400.0, rel=REL)

    def test_prezzo_vendita_zero_neutro(self):
        n = self._bc(prezzo_vendita_eur_kwh=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzo_vendita_negativo_neutro(self):
        n = self._bc(prezzo_vendita_eur_kwh=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzi_costi_negativi_neutro(self):
        for k in ("costo_acquisto_eur_pacco",
                  "costo_test_eur_pacco",
                  "ricavo_servizi_eur_kwh_a",
                  "opex_fisso_eur_a",
                  "capex_eur",
                  "fattore_co2_t_kwh"):
            n = self._bc(**{k: -0.01})
            assert n["verdetto"] == "NON_CALCOLABILE", k

    def test_vita_zero_neutro(self):
        n = self._bc(vita_a=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_non_intera_neutro(self):
        n = self._bc(vita_a=9.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_negativo_neutro(self):
        n = self._bc(wacc_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_negativa_neutro(self):
        n = self._bc(toll_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_oltre_uno_neutro(self):
        n = self._bc(toll_frac=1.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(prezzo_vendita_eur_kwh=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["margine_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(pacchi_anno=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(pacchi_anno=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_margine_negativo_neutro(self):
        # OPEX fisso enorme: 746550 - 1112000 < 0
        n = self._bc(opex_fisso_eur_a=800000.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["margine_eur_a"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_wacc_zero_calcolabile_conviente(self):
        n = self._bc(wacc_frac=0.0)
        assert n["van"] == pytest.approx(
            -CAPEX_DEMO + MARG_DEMO * 10, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_zero_mai_marginale(self):
        n = self._bc(capex_eur=0.0)
        assert n["capex_eur"] == 0.0
        assert n["verdetto"] == "CONVIENTE"
        assert n["verdetto"] != "MARGINALE"
        assert n["payback"] == 0
        assert n["tir"] is None

    def test_verdetto_marginale_end_to_end(self):
        # CAPEX 2800000: VAN circa -43279, entro il
        # 10 % di 2800000
        n = self._bc(capex_eur=2800000.0)
        assert n["capex_eur"] == pytest.approx(
            2800000.0, rel=REL)
        assert n["van"] < 0.0
        assert abs(n["van"]) <= 0.10 * 2800000.0
        assert n["verdetto"] == "MARGINALE"

    def test_verdetto_non_conviente_end_to_end(self):
        n = self._bc(capex_eur=4000000.0)
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh692_neutro"]()
        assert n["valid"] is False
        assert list(n["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(n["df_flussi"]) == 0
        assert list(n["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(n["df_tabella"]) == 0

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh692_neutro"]()
        for chiave in ("valid",
                       "kwh_usabili_pacco_kwh",
                       "pacchi_venduti",
                       "kwh_venduti_kwh_a",
                       "ricavi_vendita_eur_a",
                       "ricavi_servizi_eur_a",
                       "ricavi_tot_eur_a",
                       "costi_acquisto_eur_a",
                       "costi_test_eur_a",
                       "opex_fisso_eur_a",
                       "costi_tot_eur_a",
                       "margine_eur_a",
                       "co2_evitata_t_a",
                       "capex_eur", "van", "tir", "payback",
                       "verdetto", "df_flussi",
                       "df_tabella"):
            assert chiave in n, chiave

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert b["valid"] is True
        assert list(b["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(b["df_tabella"]) == 18
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Pacchi trattati (n/anno)" in voci
        assert "kWh usabili per pacco (kWh)" in voci
        assert "Pacchi venduti (n/anno)" in voci
        assert "Ricavi vendita (EUR/anno)" in voci
        assert "Ricavi totali (EUR/anno)" in voci
        assert "Costi test (EUR/anno)" in voci
        assert "Costi totali (EUR/anno)" in voci
        assert "Margine (EUR/anno)" in voci
        assert "CO2 evitata (t/anno)" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(b["df_flussi"]) == VITA_DEMO + 1
        assert b["df_flussi"]["Cumulato (€)"].iloc[-1] == \
            pytest.approx(-CAPEX_DEMO + MARG_DEMO * VITA_DEMO,
                          rel=REL)


class TestSensitivitaCsv:
    def _ing(self):
        return _F["mh692_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh692_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.8", "x1.0", "x1.2"]
        assert list(s.index) == ["x0.8", "x1.0", "x1.2"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh692_sensitivita"](self._ing())
        assert s.loc["x1.0", "x1.0"] == \
            pytest.approx(VAN_DEMO, rel=REL)

    def test_sensitivita_monotona_prezzo_vendita(self):
        # VAN cresce con il prezzo vendita
        s = _F["mh692_sensitivita"](self._ing())
        centro = s.loc["x1.0", "x1.0"]
        assert s.loc["x0.8", "x1.0"] < centro
        assert s.loc["x1.2", "x1.0"] > centro

    def test_sensitivita_crescente_con_resa(self):
        # Ogni punto di resa in piu' vende piu' kWh:
        # VAN cresce con la resa.
        s = _F["mh692_sensitivita"](self._ing())
        for riga in ("x0.8", "x1.0", "x1.2"):
            assert s.loc[riga, "x0.8"] < \
                s.loc[riga, "x1.0"] < \
                s.loc[riga, "x1.2"]
        for colonna in ("x0.8", "x1.0", "x1.2"):
            assert s.loc["x0.8", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.2", colonna]

    def test_sensitivita_nessuna_colonna_degenere(self):
        # Entrambi gli assi variano davvero sulla
        # demo (prezzo vendita e resa senza tetto
        # attivo a 1,2 x 0,75 = 0,90): il margine
        # resta positivo su tutta la griglia,
        # nessuna cella puo' essere 0,0 per
        # regime degenere
        s = _F["mh692_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_assi_variano_davvero(self):
        s = _F["mh692_sensitivita"](self._ing())
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh692_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 31

    def test_csv_contiene_verdetto_e_co2(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh692_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "co2_evitata_t_a" in txt
        assert "ricavi_tot_eur_a" in txt
        assert "margine_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "costi_tot_eur_a" in txt
        assert "prezzo_vendita_eur_kwh" in txt
        assert "pacchi_anno" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh692_csv"](bc, self._ing())
        assert f"ricavi_tot_eur_a;{RTOT_DEMO}" in txt
        assert f"margine_eur_a;{MARG_DEMO}" in txt
        assert f"capex_eur;{CAPEX_DEMO}" in txt
        assert f"ricavi_vendita_eur_a;{RVEND_DEMO}" in txt
        assert f"costi_tot_eur_a;{CTOT_DEMO}" in txt
        assert "ricavi_servizi_eur_a;37800.0" in txt


class TestStruttura:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def692["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def692\["([a-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 14, ui_keys
        demo_keys = set(_F["mh692_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_header_helpers_presente(self):
        assert '# W692 (24/10/2026) - tab692' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh692_num", "mh692_nneg", "mh692_pos",
                     "mh692_int_pos", "mh692_frac",
                     "mh692_tol",
                     "mh692_kwh_usabili_pacco",
                     "mh692_pacchi_venduti",
                     "mh692_kwh_venduti",
                     "mh692_ricavi_vendita",
                     "mh692_ricavi_servizi",
                     "mh692_ricavi_tot",
                     "mh692_costi_acquisto",
                     "mh692_costi_test",
                     "mh692_costi_tot", "mh692_margine",
                     "mh692_co2", "mh692_capex",
                     "mh692_van", "mh692_tir",
                     "mh692_payback", "mh692_verdetto",
                     "_mh692_neutro", "mh692_calcola",
                     "mh692_sensitivita", "mh692_csv",
                     "mh692_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_helpers_parse_ast(self):
        import textwrap
        ast.parse(_helpers_src())
        # il frammento UI e' indentato di 4 spazi per
        # l'apply (come w691_ui.py): si dedenta prima
        # del parse, come farebbe l'apply
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w692_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE692) == 1

    def test_blocco_with_tab692(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab692:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE692

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st692_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 19, keys
        assert len(set(keys)) == len(keys)
        assert not any(k.startswith("st691_") for k in keys)
        assert not any(k.startswith("st690_") for k in keys)

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg692" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg692") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg692")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Ricavi totali (€/anno)" in src
        assert "Margine (€/anno)" in src
        assert "VAN (€)" in src
        assert "CO2 evitata (t/anno)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd692" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_second_life_presente(self):
        src = _ui_src()
        assert "second life ≠ riciclo" in src
        assert "SoH" in src
        assert "selezione" in src
        assert "test" in src
        assert "degrado" in src

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Ricavi vendita" in src
        assert "Margine" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh692_csv" in src
        assert "second_life_batterie_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh692_sensitivita" in src
        assert "Heatmap" in src
        assert "Prezzo vendita" in src
        assert "Resa selezione" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st692_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W692 (24/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab692:")
        assert "mh692_calcola" in _helpers_src()
        assert "demo_calcoli" in _helpers_src()
        assert "import streamlit" not in _helpers_src()
        assert "tab692" in (_new_dir() / "w692_test.py")\
            .read_text(encoding="utf-8")

    def test_nessun_segreto_nei_file(self):
        for fn in ("w692_helpers.py", "w692_ui.py",
                   "w692_test.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            assert not re.search(
                r"(?i)(api[_-]?key|secret|password|passwd|token)"
                r"\s*=\s*[\"']",
                src), fn

    def test_nessun_riferimento_alle_tab_precedenti(self):
        src = _ui_src()
        assert "tab691" not in src
        assert "tab690" not in src
        assert "tab689" not in src

    def test_topic_second_life_non_riciclo(self):
        # Topic corretto: il titolo e' second life
        assert "Second life" in TITLE692
        assert "riciclo" not in TITLE692.lower()
