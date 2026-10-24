"""Test tab680 "🏔️⚖️ Accumulo gravitazionale: blocchi, altezza e gravità come batteria?"

Demo calcolata eseguendo demo_calcoli() (non a mano):
impianto gravitazionale da 500 kW con blocchi da
2000 t sollevati a 120 m (654,0 kWh per ciclo),
300 cicli/anno, rendimento di carica 0,90 e di
scarica 0,90 (rendimento di ciclo 0,81); prezzo di
acquisto 60 EUR/MWh, prezzo di vendita 180
EUR/MWh; ricavi da servizi 30 EUR/kW/anno; CAPEX
800 EUR/kW + 150 EUR/kWh di ciclo; OPEX 15
EUR/kW/anno; vita 30 anni; WACC 5,0 %;
tolleranza 10,0 % del CAPEX.

- energia_ciclo_kwh = 654.0
- scaricata_mwh = 176.58
- caricata_mwh = 218.0
- eta_rt = 0.81
- ricavi_arbitraggio = 31784.4
- costo_carica = 13080.0
- ricavi_servizi = 15000.0
- opex = 7500.0
- margine = 26204.4
- capex_tot = 498100.0
- crf = 0.06505143508027657
- lcos = 300.045983766484
- van = -95274.14431115118
- tir = 3.2391073052108594 (in uscita: percentuale)
- payback = 20
- verdetto = 'NON_CONVIENTE'
"""

import ast
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w680_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w680_helpers.py via AST
    (stesso pattern di tests/appfuncs.py: niente Streamlit)."""
    src = (_new_dir() / "w680_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w680_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w680_helpers.py: {missing}")
    return out


_F = _load("mh680_num", "mh680_nneg", "mh680_pos",
           "mh680_int_pos", "mh680_quota", "mh680_pct",
           "mh680_energia_ciclo_kwh", "mh680_eta_rt",
           "mh680_scaricata_mwh",
           "mh680_caricata_mwh",
           "mh680_ricavi_arbitraggio",
           "mh680_costo_carica", "mh680_ricavi_servizi",
           "mh680_opex", "mh680_margine",
           "mh680_capex_tot", "mh680_crf", "mh680_lcos",
           "mh680_van", "mh680_tir", "mh680_payback",
           "mh680_verdetto", "_mh680_neutro",
           "mh680_calcola", "mh680_sensitivita",
           "mh680_csv", "mh680_demo", "demo_calcoli")

TITLE680 = ("🏔️⚖️ Accumulo gravitazionale: blocchi, "
            "altezza e gravità come batteria?")

ENERGIA_DEMO = 654.0
SCAR_DEMO = 176.58
CAR_DEMO = 218.0
ETA_RT_DEMO = 0.81
RICAVI_ARB_DEMO = 31784.4
COSTO_CARICA_DEMO = 13080.0
RICAVI_SERV_DEMO = 15000.0
OPEX_DEMO = 7500.0
MARG_DEMO = 26204.4
CAPEX_DEMO = 498100.0
CRF_DEMO = 0.06505143508027657
LCOS_DEMO = 300.045983766484
VAN_DEMO = -95274.14431115118
TIR_DEMO = 3.2391073052108594
PAYBACK_DEMO = 20
VITA_DEMO = 30
VERDETTO_DEMO = "NON_CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w680_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w680_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh680_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh680_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh680_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh680_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh680_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh680_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh680_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh680_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh680_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh680_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh680_int_pos"](30.0, "x") == 30

    def test_quota_rifiuta_oltre_1(self):
        with pytest.raises(ValueError):
            _F["mh680_quota"](1.01, "x")

    def test_quota_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh680_quota"](-0.01, "x")

    def test_quota_accetta_estremi(self):
        assert _F["mh680_quota"](0.0, "x") == 0.0
        assert _F["mh680_quota"](1.0, "x") == 1.0
        assert _F["mh680_quota"](0.90, "x") == 0.90

    def test_pct_rifiuta_oltre_100(self):
        with pytest.raises(ValueError):
            _F["mh680_pct"](100.01, "x")

    def test_pct_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh680_pct"](-0.01, "x")

    def test_pct_accetta_estremi(self):
        assert _F["mh680_pct"](0.0, "x") == 0.0
        assert _F["mh680_pct"](100.0, "x") == 100.0
        assert _F["mh680_pct"](5.0, "x") == 5.0


class TestFisica:
    def test_energia_demo(self):
        assert _F["mh680_energia_ciclo_kwh"](
            2000.0, 120.0) == pytest.approx(ENERGIA_DEMO,
                                            rel=REL)

    def test_energia_formula_massa_gravita_altezza(self):
        # 1000 t a 100 m: 1000*1000*9,81*100/3600000
        assert _F["mh680_energia_ciclo_kwh"](
            1000.0, 100.0) == pytest.approx(272.5, rel=1e-12)

    def test_energia_altezza_lineare(self):
        # altezza doppia -> energia doppia a parita'
        # di massa: 240 m danno 1308 kWh
        assert _F["mh680_energia_ciclo_kwh"](
            2000.0, 240.0) == pytest.approx(
            2.0 * ENERGIA_DEMO, rel=REL)

    def test_energia_massa_lineare(self):
        # massa doppia -> energia doppia a parita'
        # di altezza
        assert _F["mh680_energia_ciclo_kwh"](
            4000.0, 120.0) == pytest.approx(
            2.0 * ENERGIA_DEMO, rel=REL)

    def test_energia_rifiuta_massa_zero(self):
        with pytest.raises(ValueError):
            _F["mh680_energia_ciclo_kwh"](0.0, 120.0)

    def test_energia_rifiuta_altezza_zero(self):
        with pytest.raises(ValueError):
            _F["mh680_energia_ciclo_kwh"](2000.0, 0.0)

    def test_energia_rifiuta_altezza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh680_energia_ciclo_kwh"](2000.0, -10.0)

    def test_energia_rifiuta_massa_negativa(self):
        with pytest.raises(ValueError):
            _F["mh680_energia_ciclo_kwh"](-1.0, 120.0)

    def test_eta_rt_demo(self):
        assert _F["mh680_eta_rt"](
            0.90, 0.90) == pytest.approx(ETA_RT_DEMO,
                                         rel=REL)

    def test_eta_rt_prodotto(self):
        assert _F["mh680_eta_rt"](
            0.8, 0.9) == pytest.approx(0.72, rel=1e-12)

    def test_eta_rt_uno_se_entrambi_uno(self):
        assert _F["mh680_eta_rt"](1.0, 1.0) == 1.0

    def test_eta_rt_zero_se_uno_zero(self):
        assert _F["mh680_eta_rt"](0.0, 0.9) == 0.0
        assert _F["mh680_eta_rt"](0.9, 0.0) == 0.0

    def test_eta_rt_rifiuta_oltre_1(self):
        with pytest.raises(ValueError):
            _F["mh680_eta_rt"](1.01, 0.9)
        with pytest.raises(ValueError):
            _F["mh680_eta_rt"](0.9, 1.01)

    def test_scaricata_demo(self):
        assert _F["mh680_scaricata_mwh"](
            ENERGIA_DEMO, 300.0,
            0.90) == pytest.approx(SCAR_DEMO, rel=REL)

    def test_scaricata_formula(self):
        assert _F["mh680_scaricata_mwh"](
            654.0, 100.0, 0.9) == pytest.approx(
            654.0 * 100.0 * 0.9 / 1000.0, rel=1e-12)

    def test_scaricata_rifiuta_cicli_zero(self):
        with pytest.raises(ValueError):
            _F["mh680_scaricata_mwh"](ENERGIA_DEMO, 0.0, 0.9)

    def test_scaricata_rifiuta_cicli_negativi(self):
        with pytest.raises(ValueError):
            _F["mh680_scaricata_mwh"](ENERGIA_DEMO, -5.0,
                                       0.9)

    def test_scaricata_rifiuta_eta_zero(self):
        with pytest.raises(ValueError):
            _F["mh680_scaricata_mwh"](ENERGIA_DEMO, 300.0,
                                       0.0)

    def test_scaricata_rifiuta_energia_zero(self):
        with pytest.raises(ValueError):
            _F["mh680_scaricata_mwh"](0.0, 300.0, 0.9)

    def test_caricata_demo(self):
        assert _F["mh680_caricata_mwh"](
            SCAR_DEMO, ETA_RT_DEMO) == pytest.approx(
            CAR_DEMO, rel=REL)

    def test_caricata_maggiore_della_scaricata(self):
        # eta_rt 0,81: si compra piu' energia di
        # quanta se ne rivende
        assert CAR_DEMO > SCAR_DEMO

    def test_caricata_none_se_eta_zero(self):
        assert _F["mh680_caricata_mwh"](
            SCAR_DEMO, 0.0) is None

    def test_caricata_none_se_eta_negativa(self):
        assert _F["mh680_caricata_mwh"](
            SCAR_DEMO, -0.1) is None

    def test_caricata_rifiuta_eta_oltre_1(self):
        with pytest.raises(ValueError):
            _F["mh680_caricata_mwh"](SCAR_DEMO, 1.01)

    def test_caricata_rifiuta_scaricata_negativa(self):
        with pytest.raises(ValueError):
            _F["mh680_caricata_mwh"](-1.0, ETA_RT_DEMO)

    def test_ricavi_arbitraggio_demo(self):
        assert _F["mh680_ricavi_arbitraggio"](
            SCAR_DEMO, 180.0) == pytest.approx(
            RICAVI_ARB_DEMO, rel=REL)

    def test_ricavi_arbitraggio_zero_se_prezzo_zero(self):
        assert _F["mh680_ricavi_arbitraggio"](
            SCAR_DEMO, 0.0) == 0.0

    def test_ricavi_arbitraggio_rifiuta_negativi(self):
        with pytest.raises(ValueError):
            _F["mh680_ricavi_arbitraggio"](-1.0, 180.0)
        with pytest.raises(ValueError):
            _F["mh680_ricavi_arbitraggio"](SCAR_DEMO, -0.01)

    def test_costo_carica_demo(self):
        assert _F["mh680_costo_carica"](
            CAR_DEMO, 60.0) == pytest.approx(
            COSTO_CARICA_DEMO, rel=REL)

    def test_costo_carica_rifiuta_negativi(self):
        with pytest.raises(ValueError):
            _F["mh680_costo_carica"](-1.0, 60.0)
        with pytest.raises(ValueError):
            _F["mh680_costo_carica"](CAR_DEMO, -0.01)

    def test_ricavi_servizi_demo(self):
        assert _F["mh680_ricavi_servizi"](
            500.0, 30.0) == pytest.approx(
            RICAVI_SERV_DEMO, rel=REL)

    def test_ricavi_servizi_rifiuta_potenza_zero(self):
        with pytest.raises(ValueError):
            _F["mh680_ricavi_servizi"](0.0, 30.0)

    def test_ricavi_servizi_rifiuta_unitario_negativo(self):
        with pytest.raises(ValueError):
            _F["mh680_ricavi_servizi"](500.0, -0.01)

    def test_opex_demo(self):
        assert _F["mh680_opex"](
            500.0, 15.0) == pytest.approx(OPEX_DEMO,
                                          rel=REL)

    def test_opex_rifiuta_potenza_zero(self):
        with pytest.raises(ValueError):
            _F["mh680_opex"](0.0, 15.0)

    def test_opex_rifiuta_unitario_negativo(self):
        with pytest.raises(ValueError):
            _F["mh680_opex"](500.0, -0.01)

    def test_margine_demo(self):
        assert _F["mh680_margine"](
            RICAVI_ARB_DEMO, RICAVI_SERV_DEMO,
            COSTO_CARICA_DEMO, OPEX_DEMO) == pytest.approx(
            MARG_DEMO, rel=REL)

    def test_margine_formula(self):
        assert _F["mh680_margine"](
            31784.4, 15000.0, 13080.0,
            7500.0) == pytest.approx(MARG_DEMO, rel=REL)

    def test_margine_puo_essere_negativo(self):
        assert _F["mh680_margine"](100.0, 50.0, 80.0,
                                   100.0) == -30.0

    def test_margine_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh680_margine"](float("nan"), 0.0, 0.0, 0.0)

    def test_capex_tot_demo(self):
        assert _F["mh680_capex_tot"](
            500.0, 800.0, ENERGIA_DEMO,
            150.0) == pytest.approx(CAPEX_DEMO, rel=REL)

    def test_capex_tot_split_kw_piu_kwh_ciclo(self):
        # 500 x 800 (gru/generatori) +
        # 654 x 150 (torri/blocchi per ciclo)
        assert 500.0 * 800.0 + 654.0 * 150.0 == CAPEX_DEMO

    def test_capex_tot_non_cresce_con_cicli_annui(self):
        # la struttura e' dimensionata su un ciclo:
        # stessi input danno lo stesso CAPEX
        # qualunque siano i cicli annui (che non
        # entrano nella formula)
        assert _F["mh680_capex_tot"](
            500.0, 800.0, ENERGIA_DEMO,
            150.0) == CAPEX_DEMO

    def test_capex_tot_solo_kw_se_energia_zero(self):
        assert _F["mh680_capex_tot"](
            500.0, 800.0, 0.0, 150.0) == pytest.approx(
            400000.0, rel=REL)

    def test_capex_tot_zero_se_unitari_zero(self):
        assert _F["mh680_capex_tot"](
            500.0, 0.0, ENERGIA_DEMO, 0.0) == 0.0

    def test_capex_tot_rifiuta_negativi(self):
        with pytest.raises(ValueError):
            _F["mh680_capex_tot"](500.0, -1.0, ENERGIA_DEMO,
                                  150.0)
        with pytest.raises(ValueError):
            _F["mh680_capex_tot"](500.0, 800.0, ENERGIA_DEMO,
                                  -1.0)
        with pytest.raises(ValueError):
            _F["mh680_capex_tot"](500.0, 800.0, -1.0, 150.0)

    def test_capex_tot_rifiuta_potenza_zero(self):
        with pytest.raises(ValueError):
            _F["mh680_capex_tot"](0.0, 800.0, ENERGIA_DEMO,
                                  150.0)

    def test_crf_demo(self):
        # wacc_pct in percentuale: 5,0 = 5 %
        assert _F["mh680_crf"](
            5.0, 30) == pytest.approx(CRF_DEMO, rel=REL)

    def test_crf_wacc_zero(self):
        assert _F["mh680_crf"](
            0.0, 30) == pytest.approx(1.0 / 30.0, rel=1e-12)

    def test_crf_rifiuta_wacc_negativo(self):
        with pytest.raises(ValueError):
            _F["mh680_crf"](-0.01, 30)

    def test_crf_rifiuta_wacc_oltre_100(self):
        with pytest.raises(ValueError):
            _F["mh680_crf"](100.01, 30)

    def test_crf_rifiuta_vita_zero(self):
        with pytest.raises(ValueError):
            _F["mh680_crf"](5.0, 0)

    def test_lcos_demo(self):
        assert _F["mh680_lcos"](
            CAPEX_DEMO, CRF_DEMO, OPEX_DEMO,
            COSTO_CARICA_DEMO,
            SCAR_DEMO) == pytest.approx(LCOS_DEMO, rel=REL)

    def test_lcos_formula(self):
        c, f, o, cc, e = (CAPEX_DEMO, CRF_DEMO, OPEX_DEMO,
                          COSTO_CARICA_DEMO, SCAR_DEMO)
        assert _F["mh680_lcos"](
            c, f, o, cc, e) == pytest.approx(
            (c * f + o + cc) / e, rel=1e-9)

    def test_lcos_sopra_prezzo_vendita_demo(self):
        # LCOS 300,05 > prezzo vendita 180: ogni MWh
        # venduto distrugge valore prima dei servizi
        assert LCOS_DEMO > 180.0
        assert 180.0 - LCOS_DEMO == pytest.approx(
            -120.045983766484, rel=1e-9)

    def test_lcos_include_costo_carica(self):
        # senza costo di carica il LCOS sarebbe molto
        # piu' basso: la carica e' parte del LCOS
        senza = _F["mh680_lcos"](
            CAPEX_DEMO, CRF_DEMO, OPEX_DEMO, 0.0,
            SCAR_DEMO)
        assert senza < LCOS_DEMO

    def test_lcos_none_se_scaricata_zero(self):
        assert _F["mh680_lcos"](
            CAPEX_DEMO, CRF_DEMO, OPEX_DEMO,
            COSTO_CARICA_DEMO, 0.0) is None

    def test_lcos_none_se_scaricata_negativa(self):
        assert _F["mh680_lcos"](
            CAPEX_DEMO, CRF_DEMO, OPEX_DEMO,
            COSTO_CARICA_DEMO, -1.0) is None


class TestFinanza:
    def test_van_demo(self):
        assert _F["mh680_van"](
            MARG_DEMO, CAPEX_DEMO, 5.0,
            VITA_DEMO) == pytest.approx(VAN_DEMO, rel=REL)

    def test_van_tasso_zero(self):
        assert _F["mh680_van"](
            MARG_DEMO, CAPEX_DEMO, 0.0,
            30) == pytest.approx(
            -CAPEX_DEMO + MARG_DEMO * 30, rel=1e-12)

    def test_van_tasso_zero_valore(self):
        assert -CAPEX_DEMO + MARG_DEMO * 30 == pytest.approx(
            288032.0, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh680_van"](MARG_DEMO, CAPEX_DEMO, -0.01, 30)

    def test_van_rifiuta_tasso_oltre_100(self):
        with pytest.raises(ValueError):
            _F["mh680_van"](MARG_DEMO, CAPEX_DEMO, 100.01, 30)

    def test_van_rifiuta_capex_negativo(self):
        with pytest.raises(ValueError):
            _F["mh680_van"](MARG_DEMO, -1.0, 5.0, 30)

    def test_tir_demo(self):
        # mh680_tir ritorna la frazione; il calcola la
        # converte in percentuale
        assert _F["mh680_tir"](
            CAPEX_DEMO, MARG_DEMO,
            VITA_DEMO) == pytest.approx(TIR_DEMO / 100.0,
                                       rel=1e-9)

    def test_tir_none_se_margine_non_positivo(self):
        assert _F["mh680_tir"](CAPEX_DEMO, 0.0, 30) is None
        assert _F["mh680_tir"](CAPEX_DEMO, -100.0, 30) is None

    def test_tir_none_se_capex_zero(self):
        # CAPEX = 0 con margine positivo: nessun cambio
        # di segno nei flussi -> None
        assert _F["mh680_tir"](0.0, MARG_DEMO, 30) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh680_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo(self):
        assert _F["mh680_payback"](
            CAPEX_DEMO, MARG_DEMO,
            VITA_DEMO) == PAYBACK_DEMO

    def test_payback_anno_1_se_margine_ge_capex(self):
        assert _F["mh680_payback"](1000.0, 1000.0, 30) == 1
        assert _F["mh680_payback"](1000.0, 2000.0, 30) == 1

    def test_payback_none_mai(self):
        assert _F["mh680_payback"](CAPEX_DEMO, 1.0, 30) is None

    def test_payback_none_se_margine_non_positivo(self):
        assert _F["mh680_payback"](CAPEX_DEMO, 0.0, 30) is None

    def test_verdetto_non_conviente_demo(self):
        # |VAN| 95274 > 10 % x 498100 = 49810
        assert _F["mh680_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 10.0,
            MARG_DEMO) == VERDETTO_DEMO

    def test_verdetto_marginale_ad_hoc(self):
        # |VAN| = 40000 <= 10 % x 498100 = 49810
        assert _F["mh680_verdetto"](
            -40000.0, CAPEX_DEMO, 10.0,
            MARG_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        # |VAN| = 100000 > 10 % x 498100 = 49810
        assert _F["mh680_verdetto"](
            -100000.0, CAPEX_DEMO, 10.0,
            MARG_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_margine_non_positivo(
            self):
        assert _F["mh680_verdetto"](
            1000.0, CAPEX_DEMO, 10.0,
            0.0) == "NON_CALCOLABILE"
        assert _F["mh680_verdetto"](
            1000.0, CAPEX_DEMO, 10.0,
            -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_non_negativo_conviente(
            self):
        assert _F["mh680_verdetto"](
            0.0, 0.0, 10.0, MARG_DEMO) == "CONVIENTE"
        assert _F["mh680_verdetto"](
            1000.0, 0.0, 10.0, MARG_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(
            self):
        # CAPEX == 0: tolleranza zero, mai MARGINALE
        assert _F["mh680_verdetto"](
            -1.0, 0.0, 10.0, MARG_DEMO) == "NON_CONVIENTE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh680_verdetto"](100.0, CAPEX_DEMO, -0.01,
                                 MARG_DEMO)

    def test_verdetto_rifiuta_tolleranza_oltre_100(self):
        with pytest.raises(ValueError):
            _F["mh680_verdetto"](100.0, CAPEX_DEMO, 100.01,
                                 MARG_DEMO)


class TestGuard:
    def _bc(self, **kw):
        d = _F["mh680_demo"]()
        d.update(kw)
        return _F["mh680_calcola"](**d)

    def test_potenza_zero_neutro(self):
        n = self._bc(potenza_kw=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["energia_ciclo_kwh"] == 0.0
        assert n["margine"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_potenza_negativa_neutro(self):
        n = self._bc(potenza_kw=-100.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_altezza_zero_neutro(self):
        n = self._bc(altezza_m=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_altezza_negativa_neutro(self):
        n = self._bc(altezza_m=-10.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_massa_zero_neutro(self):
        n = self._bc(massa_ciclo_t=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_massa_negativa_neutro(self):
        n = self._bc(massa_ciclo_t=-100.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_cicli_zero_neutro(self):
        n = self._bc(cicli_annui=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_cicli_negativi_neutro(self):
        n = self._bc(cicli_annui=-10.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_carica_zero_neutro(self):
        n = self._bc(eta_carica=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_scarica_zero_neutro(self):
        n = self._bc(eta_scarica=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_carica_negativa_neutro(self):
        n = self._bc(eta_carica=-0.1)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_scarica_oltre_1_neutro(self):
        n = self._bc(eta_scarica=1.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_carica_oltre_1_neutro(self):
        n = self._bc(eta_carica=1.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzo_acquisto_negativo_neutro(self):
        n = self._bc(prezzo_acquisto_eur_mwh=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzo_vendita_negativo_neutro(self):
        n = self._bc(prezzo_vendita_eur_mwh=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_servizi_negativi_neutro(self):
        n = self._bc(ricavi_servizi_eur_kw_a=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_capex_kw_negativo_neutro(self):
        n = self._bc(capex_eur_kw=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_capex_kwh_negativo_neutro(self):
        n = self._bc(capex_eur_kwh=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_opex_negativo_neutro(self):
        n = self._bc(opex_eur_kw_a=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_non_intera_neutro(self):
        n = self._bc(vita_anni=29.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_negativo_neutro(self):
        n = self._bc(wacc_pct=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_oltre_100_neutro(self):
        n = self._bc(wacc_pct=100.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_negativa_neutro(self):
        n = self._bc(toll_pct=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_oltre_100_neutro(self):
        n = self._bc(toll_pct=100.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(prezzo_vendita_eur_mwh=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["ricavi_arbitraggio"] == 0.0

    def test_bool_neutro(self):
        n = self._bc(potenza_kw=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzo_vendita_zero_margine_negativo_neutro(self):
        # vendita a zero: arbitraggio 0, servizi
        # 15000 < carica 13080 + OPEX 7500 -> margine
        # -5580 -> neutro
        n = self._bc(prezzo_vendita_eur_mwh=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["margine"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_acquisto_alto_margine_negativo_neutro(self):
        # acquisto 300: carica 65400 > arbitraggio
        # 31784 + servizi 15000 - OPEX 7500
        n = self._bc(prezzo_acquisto_eur_mwh=300.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_uno_calcolabile(self):
        # rendimenti ideali 100 %: carica = scaricata
        # 196,2 MWh, margine positivo
        n = self._bc(eta_carica=1.0, eta_scarica=1.0)
        assert n["caricata_mwh"] == pytest.approx(
            n["scaricata_mwh"], rel=REL)
        assert n["scaricata_mwh"] == pytest.approx(
            196.2, rel=REL)
        assert n["verdetto"] != "NON_CALCOLABILE"
        assert n["valid"] is True

    def test_wacc_zero_calcolabile_conviente(self):
        # WACC 0: VAN = -498100 + 26204,4 x 30 =
        # 288032 -> CONVIENTE
        n = self._bc(wacc_pct=0.0)
        assert n["van"] == pytest.approx(288032.0, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_zero_mai_marginale(self):
        n = self._bc(capex_eur_kw=0.0, capex_eur_kwh=0.0)
        assert n["capex_tot"] == 0.0
        assert n["verdetto"] == "CONVIENTE"
        assert n["verdetto"] != "MARGINALE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh680_neutro"]()
        assert n["valid"] is False
        assert list(n["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(n["df_flussi"]) == 0
        assert list(n["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(n["df_tabella"]) == 0

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh680_neutro"]()
        for chiave in ("valid", "energia_ciclo_kwh",
                       "scaricata_mwh",
                       "caricata_mwh", "eta_rt",
                       "ricavi_arbitraggio",
                       "costo_carica", "ricavi_servizi",
                       "opex", "margine", "capex_tot",
                       "crf", "lcos", "van", "tir",
                       "payback", "verdetto", "df_flussi",
                       "df_tabella"):
            assert chiave in n, chiave

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert b["valid"] is True
        assert list(b["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(b["df_tabella"]) == 13
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Energia per ciclo (kWh)" in voci
        assert "LCOS (EUR/MWh)" in voci
        assert "Margine operativo (EUR/anno)" in voci
        assert "Energia scaricata (MWh/anno)" in voci
        assert "Rendimento di ciclo (frazione)" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(b["df_flussi"]) == VITA_DEMO + 1
        assert b["df_flussi"]["Cumulato (€)"].iloc[-1] == \
            pytest.approx(-CAPEX_DEMO + MARG_DEMO * VITA_DEMO,
                          rel=REL)


class TestSensitivitaCsv:
    def _ing(self):
        return _F["mh680_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh680_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["Cicli x0.8",
                                   "Cicli x1.0",
                                   "Cicli x1.2"]
        assert list(s.index) == ["x0.8", "x1.0", "x1.2"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh680_sensitivita"](self._ing())
        assert s.loc["x1.0", "Cicli x1.0"] == \
            pytest.approx(VAN_DEMO, rel=REL)

    def test_sensitivita_monotona(self):
        # VAN cresce col prezzo di vendita e coi
        # cicli annui (a margine positivo in tutta
        # la griglia)
        s = _F["mh680_sensitivita"](self._ing())
        centro = s.loc["x1.0", "Cicli x1.0"]
        assert s.loc["x1.2", "Cicli x1.2"] > centro
        assert s.loc["x0.8", "Cicli x0.8"] < centro
        assert s.loc["x1.0", "Cicli x1.2"] > centro
        assert s.loc["x1.0", "Cicli x0.8"] < centro
        assert s.loc["x1.2", "Cicli x1.0"] > centro
        assert s.loc["x0.8", "Cicli x1.0"] < centro

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh680_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 31

    def test_csv_contiene_verdetto_e_lcos(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh680_csv"](bc, self._ing())
        assert "verdetto;NON_CONVIENTE" in txt
        assert "lcos_eur_mwh" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "scaricata_mwh_anno" in txt
        assert "capex_eur_kwh" in txt
        assert "eta_rt_frazione" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh680_csv"](bc, self._ing())
        assert f"scaricata_mwh_anno;{SCAR_DEMO}" in txt
        assert f"margine_eur_anno;{MARG_DEMO}" in txt
        assert f"ricavi_arbitraggio_eur_anno;{RICAVI_ARB_DEMO}" \
            in txt
        assert f"energia_ciclo_kwh;{ENERGIA_DEMO}" in txt
        assert f"eta_rt_frazione;{ETA_RT_DEMO}" in txt


class TestDemo:
    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["energia_ciclo_kwh"] == pytest.approx(
            ENERGIA_DEMO, rel=REL)
        assert c["scaricata_mwh"] == pytest.approx(
            SCAR_DEMO, rel=REL)
        assert c["caricata_mwh"] == pytest.approx(
            CAR_DEMO, rel=REL)
        assert c["eta_rt"] == pytest.approx(
            ETA_RT_DEMO, rel=REL)
        assert c["ricavi_arbitraggio"] == pytest.approx(
            RICAVI_ARB_DEMO, rel=REL)
        assert c["costo_carica"] == pytest.approx(
            COSTO_CARICA_DEMO, rel=REL)
        assert c["ricavi_servizi"] == pytest.approx(
            RICAVI_SERV_DEMO, rel=REL)
        assert c["opex"] == pytest.approx(
            OPEX_DEMO, rel=REL)
        assert c["margine"] == pytest.approx(
            MARG_DEMO, rel=REL)
        assert c["capex_tot"] == pytest.approx(
            CAPEX_DEMO, rel=REL)
        assert c["crf"] == pytest.approx(CRF_DEMO, rel=REL)
        assert c["lcos"] == pytest.approx(
            LCOS_DEMO, rel=REL)
        assert c["van"] == pytest.approx(VAN_DEMO, rel=REL)
        assert c["tir"] == pytest.approx(TIR_DEMO, rel=REL)
        assert c["payback"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()[
            "van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()[
            "lcos"] == _F["demo_calcoli"]()["lcos"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        """mh680_calcola(**mh680_demo()) deve matchare le
        costanti _DEMO entro 1e-9 relativo (mismatch
        vietato), chiave per chiave."""
        d = _F["mh680_demo"]()
        b = _F["mh680_calcola"](**d)
        coppie = [("energia_ciclo_kwh", ENERGIA_DEMO),
                  ("scaricata_mwh", SCAR_DEMO),
                  ("caricata_mwh", CAR_DEMO),
                  ("eta_rt", ETA_RT_DEMO),
                  ("ricavi_arbitraggio", RICAVI_ARB_DEMO),
                  ("costo_carica", COSTO_CARICA_DEMO),
                  ("ricavi_servizi", RICAVI_SERV_DEMO),
                  ("opex", OPEX_DEMO),
                  ("margine", MARG_DEMO),
                  ("capex_tot", CAPEX_DEMO),
                  ("crf", CRF_DEMO),
                  ("lcos", LCOS_DEMO),
                  ("van", VAN_DEMO),
                  ("tir", TIR_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh680_demo"]()
        assert d["potenza_kw"] == 500.0
        assert d["altezza_m"] == 120.0
        assert d["massa_ciclo_t"] == 2000.0
        assert d["cicli_annui"] == 300.0
        assert d["eta_carica"] == 0.90
        assert d["eta_scarica"] == 0.90
        assert d["prezzo_acquisto_eur_mwh"] == 60.0
        assert d["prezzo_vendita_eur_mwh"] == 180.0
        assert d["ricavi_servizi_eur_kw_a"] == 30.0
        assert d["capex_eur_kw"] == 800.0
        assert d["capex_eur_kwh"] == 150.0
        assert d["opex_eur_kw_a"] == 15.0
        assert d["vita_anni"] == 30
        assert d["wacc_pct"] == 5.0
        assert d["toll_pct"] == 10.0

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("energia_ciclo_kwh", "scaricata_mwh",
                       "caricata_mwh", "eta_rt",
                       "ricavi_arbitraggio",
                       "costo_carica", "ricavi_servizi",
                       "opex", "margine", "capex_tot",
                       "crf", "lcos", "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 20" in doc
        assert "verdetto = 'NON_CONVIENTE'" in doc


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def680["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def680\["([a-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 15, ui_keys
        demo_keys = set(_F["mh680_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys


class TestUI:
    def test_header_helpers_presente(self):
        assert '# W680 (24/10/2026) - tab680' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh680_num", "mh680_nneg", "mh680_pos",
                     "mh680_int_pos", "mh680_quota",
                     "mh680_pct", "mh680_energia_ciclo_kwh",
                     "mh680_eta_rt",
                     "mh680_scaricata_mwh",
                     "mh680_caricata_mwh",
                     "mh680_ricavi_arbitraggio",
                     "mh680_costo_carica",
                     "mh680_ricavi_servizi", "mh680_opex",
                     "mh680_margine", "mh680_capex_tot",
                     "mh680_crf", "mh680_lcos",
                     "mh680_van", "mh680_tir",
                     "mh680_payback", "mh680_verdetto",
                     "_mh680_neutro", "mh680_calcola",
                     "mh680_sensitivita", "mh680_csv",
                     "mh680_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE680) == 1

    def test_blocco_with_tab680(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab680:"

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st680_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 20, keys
        assert len(set(keys)) == len(keys)
        # nessuna collisione con le chiavi dei cicli precedenti
        assert not any(k.startswith("st679_") for k in keys)
        assert not any(k.startswith("st678_") for k in keys)
        assert not any(k.startswith("st677_") for k in keys)

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg680" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg680") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg680")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "MWh scaricati / anno" in src
        assert "LCOS (€/MWh)" in src
        assert "VAN (€)" in src
        assert "TIR / Payback" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd680" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_lcos_vs_prezzo_presente(self):
        src = _ui_src()
        assert "LCOS vs prezzo di vendita" in src
        assert "costo di carica" in src
        assert "spread" in src

    def test_nota_altezza_lineare_presente(self):
        src = _ui_src()
        assert "LINEARMENTE" in src or "linearmente" in src
        assert "altezza" in src.lower()
        assert "m x g x h" in src

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Ricavi arbitraggio" in src
        assert "Ricavi servizi" in src
        assert "Margine gravitazionale" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert 'sep=";"' in src or "mh680_csv" in src
        assert "accumulo_gravitazionale_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitiv" in src
        assert "mh680_sensitivita" in src
        assert "Heatmap" in src
        assert "Prezzo di vendita" in src
        assert "Cicli" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st680_show_flussi" in src
        assert "st.checkbox" in src

    def test_differenziazione_da_feature_esistenti(self):
        src = _ui_src()
        assert "blocchi" in src.lower()
        assert "gravit" in src.lower()
        assert "CAES" in src
        assert "pompaggio" in src.lower()
        assert "volano" in src.lower()


class TestApplyContract:
    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE680

    def test_ancora_helper_presente(self):
        assert "# W680 (24/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab680:")
        assert "mh680_calcola" in _helpers_src()
        assert "demo_calcoli" in _helpers_src()
        assert "import streamlit" not in _helpers_src()
        assert "tab680" in (_new_dir() / "w680_test.py")\
            .read_text(encoding="utf-8")


class TestSegreti:
    def test_nessun_segreto_nei_file(self):
        for fn in ("w680_helpers.py", "w680_ui.py",
                   "w680_test.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            assert not re.search(
                r"(?i)(api[_-]?key|secret|password|passwd|token)"
                r"\s*=\s*[\"']",
                src), fn
