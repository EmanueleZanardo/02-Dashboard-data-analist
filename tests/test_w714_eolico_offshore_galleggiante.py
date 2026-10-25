"""Test tab714 "🌊⚡ Eolico offshore galleggiante: l'acqua profonda paga?"

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
potenza galleggiante 500 MW; capacity
factor galleggiante 0,60; capacity factor
fissa 0,40; costo specifico galleggiante
3800 EUR/kW; costo specifico fissa 2500
EUR/kW; costo fisso galleggiante 50000000
EUR; costo fisso fissa 30000000 EUR; O&M
galleggiante 90 EUR/kW/anno; O&M fissa 80
EUR/kW/anno; vita in anni galleggiante 25;
vita in anni fissa 25; vita di progetto 25
anni; WACC 0,06 (6 %); tolleranza 0,10
(10 % del |CAPEX delta|); fattore rete
0,35 t/MWh.

- e_mwh_a = 2628000.0
- p_fissa_mw = 750.0
- capex_float_eur = 1950000000.0
- capex_fissa_eur = 1905000000.0
- capex_delta_eur = 45000000.0
- costo_base_eur_a = 60000000.0
- costo_alt_eur_a = 45000000.0
- risparmio_eur_a = 15000000.0
- anni_sost_float = []
- anni_sost_fissa = []
- co2_evitata_t_a = 919799.9999999999
- van = 146750342.37402603
- tir = 33.3081297170159
- payback = 3
- verdetto = 'CONVIENTE'

Scomposizione: E 500 x 8760 x 0,60 =
2628000.0 MWh/anno; P_fissa 2628000.0 /
(8760 x 0,40) = 750.0 MW; CAPEX galleggiante
500 x 1000 x 3800 + 50000000 =
1950000000.0 EUR; CAPEX fissa 750 x 1000 x
2500 + 30000000 = 1905000000.0 EUR; CAPEX
delta 1950000000.0 - 1905000000.0 =
45000000.0 EUR; C_base 750 x 1000 x 80 =
60000000.0 EUR/anno; C_alt 500 x 1000 x 90 =
45000000.0 EUR/anno; risparmio 60000000.0 -
45000000.0 = 15000000.0 EUR/anno; vite 25
anni in entrambi i rami: nessuna
sostituzione entro 25 anni; flussi
[-45000000.0, 15000000.0 x 25]; VAN
146750342.37402603 a WACC 6 % su 25 anni
(fattore di attualizzazione 12,783356158268413:
-45000000.0 + 15000000.0 x 12,783356158268413);
TIR 33.3081297170159 % (il VAN si azzera a
quel tasso: -45000000.0 + 15000000.0 x
a(r, 25) = 0 con a(r, 25) = 3,0); payback 3
(cumulato anno 2 = -15000000.0 < 0, cumulato
anno 3 = 0.0 >= 0); VAN >= 0 -> CONVIENTE.
CO2: 2628000.0 x 0,35 = 919799.9999999999 t/anno
(≈ 919.800 t/anno, informativa, non differenziale: entrambi i
rami sono a zero emissioni operative, quindi
la CO2 evitata vs rete e' identica per
galleggiante e fisso).
"""

import ast
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w715_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w715_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w715_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w715_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w715_helpers.py: {missing}")
    return out


_F = _load("mh714_num", "mh714_nneg", "mh714_pos",
           "mh714_int_pos", "mh714_int_nneg",
           "mh714_quota_valida", "mh714_cf_valido",
           "mh714_e_annua", "mh714_p_fissa",
           "mh714_capex", "mh714_costo_annuo",
           "mh714_risparmio", "mh714_anni_sostituzione",
           "mh714_flussi",
           "mh714_van_flussi", "mh714_tir_flussi",
           "mh714_payback_flussi", "mh714_verdetto",
           "mh714_co2_evitata", "mh714_valida",
           "_mh714_neutro", "mh714_calcola",
           "mh714_sensitivita", "mh714_csv",
           "mh714_demo", "demo_calcoli")

TITLE714 = ("🌊⚡ Eolico offshore galleggiante: "
            "l'acqua profonda paga?")

E_DEMO = 2628000.0
P_FISSA_DEMO = 750.0
CX_FLOAT_DEMO = 1950000000.0
CX_FISSA_DEMO = 1905000000.0
DELTA_DEMO = 45000000.0
C_BASE_DEMO = 60000000.0
C_ALT_DEMO = 45000000.0
RISPARMIO_DEMO = 15000000.0
CO2_EV_DEMO = 919799.9999999999
VAN_DEMO = 146750342.37402603
TIR_DEMO = 33.3081297170159
PAYBACK_DEMO = 3
VITA_DEMO = 25
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w715_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w715_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh714_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh714_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh714_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh714_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh714_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh714_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh714_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh714_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh714_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh714_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh714_int_pos"](25.0, "x") == 25

    def test_int_nneg_accetta_zero(self):
        assert _F["mh714_int_nneg"](0, "x") == 0

    def test_int_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh714_int_nneg"](-1, "x")

    def test_quota_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh714_quota_valida"](-0.1, "x")

    def test_quota_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh714_quota_valida"](1.1, "x")

    def test_quota_accetta_zeri_e_uno(self):
        assert _F["mh714_quota_valida"](0.0, "x") == 0.0
        assert _F["mh714_quota_valida"](1.0, "x") == 1.0

    def test_cf_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh714_cf_valido"](0.0, "x")

    def test_cf_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh714_cf_valido"](1.1, "x")

    def test_cf_accetta_uno_e_demo(self):
        assert _F["mh714_cf_valido"](1.0, "x") == 1.0
        assert _F["mh714_cf_valido"](0.60, "x") == 0.60


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh714_demo"]()
        d.update(kw)
        return _F["mh714_valida"](**d)

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_p_float_zero_non_valido(self):
        assert self._val(p_float_mw=0.0)["valido"] is False

    def test_p_float_negativo_non_valido(self):
        assert self._val(p_float_mw=-1.0)["valido"] is False

    def test_cf_float_zero_non_valido(self):
        assert self._val(cf_float=0.0)["valido"] is False

    def test_cf_float_sopra_uno_non_valido(self):
        assert self._val(cf_float=1.1)["valido"] is False

    def test_cf_float_uno_valido(self):
        assert self._val(cf_float=1.0)["valido"] is True

    def test_cf_fissa_zero_non_valido(self):
        assert self._val(cf_fissa=0.0)["valido"] is False

    def test_cf_fissa_sopra_uno_non_valido(self):
        assert self._val(cf_fissa=1.1)["valido"] is False

    def test_cf_fissa_uno_valida(self):
        assert self._val(cf_fissa=1.0)["valido"] is True

    def test_negativi_non_validi(self):
        for k in ("c_float_eur_kw", "c_fissa_eur_kw",
                  "fisso_float_eur", "fisso_fissa_eur",
                  "om_float_eur_kw_a", "om_fissa_eur_kw_a",
                  "wacc_frac", "f_rete_t_mwh"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_vita_anni_zero_non_valida(self):
        assert self._val(vita_anni_float=0)["valido"] is False
        assert self._val(vita_anni_fissa=0)["valido"] is False

    def test_vita_anni_non_intera_non_valida(self):
        assert self._val(vita_anni_float=24.5)["valido"] is False

    def test_vita_progetto_zero_non_valida(self):
        assert self._val(vita_progetto_anni=0)["valido"] is False

    def test_vita_progetto_non_intera_non_valida(self):
        assert self._val(vita_progetto_anni=24.5)["valido"] is False

    def test_tolleranza_negativa_non_valida(self):
        assert self._val(tolleranza_frac=-0.01)["valido"] is False

    def test_tolleranza_sopra_uno_non_valida(self):
        assert self._val(tolleranza_frac=1.5)["valido"] is False

    def test_tolleranza_uno_valida(self):
        assert self._val(tolleranza_frac=1.0)["valido"] is True

    def test_wacc_senza_tetto_superiore(self):
        assert self._val(wacc_frac=1.5)["valido"] is True

    def test_nan_non_valido(self):
        assert self._val(cf_float=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(p_float_mw=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(p_float_mw=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(cf_float="0.6")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(c_float_eur_kw=0.0)["valido"] is True
        assert self._val(om_float_eur_kw_a=0.0)["valido"] is True
        assert self._val(fisso_float_eur=0.0)["valido"] is True
        assert self._val(f_rete_t_mwh=0.0)["valido"] is True


class TestFisicaEconomia:
    def test_e_annua_demo(self):
        assert _F["mh714_e_annua"](
            500.0, 0.60) == pytest.approx(E_DEMO, rel=REL)

    def test_e_annua_rifiuta_cf_zero(self):
        with pytest.raises(ValueError):
            _F["mh714_e_annua"](500.0, 0.0)

    def test_p_fissa_demo(self):
        assert _F["mh714_p_fissa"](
            E_DEMO, 0.40) == pytest.approx(P_FISSA_DEMO, rel=REL)

    def test_p_fissa_rifiuta_cf_zero(self):
        with pytest.raises(ValueError):
            _F["mh714_p_fissa"](E_DEMO, 0.0)

    def test_capex_float_demo(self):
        assert _F["mh714_capex"](
            500.0, 3800.0, 50000000.0) == pytest.approx(
            CX_FLOAT_DEMO, rel=REL)

    def test_capex_fissa_demo(self):
        assert _F["mh714_capex"](
            750.0, 2500.0, 30000000.0) == pytest.approx(
            CX_FISSA_DEMO, rel=REL)

    def test_capex_conversione_mw_kw(self):
        # 1 MW x 1000 = 1000 kW: il fattore 1000
        # deve esserci (senza, il CAPEX sarebbe
        # 1000 volte piu' piccolo).
        assert _F["mh714_capex"](
            1.0, 3800.0, 0.0) == pytest.approx(3800000.0, rel=REL)

    def test_costo_base_demo(self):
        assert _F["mh714_costo_annuo"](
            P_FISSA_DEMO, 80.0) == pytest.approx(
            C_BASE_DEMO, rel=REL)

    def test_costo_alt_demo(self):
        assert _F["mh714_costo_annuo"](
            500.0, 90.0) == pytest.approx(C_ALT_DEMO, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh714_risparmio"](
            C_BASE_DEMO, C_ALT_DEMO) == pytest.approx(
            RISPARMIO_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh714_risparmio"](
            10000.0, 15000.0) == pytest.approx(
            -5000.0, rel=REL)

    def test_anni_sostituzione_demo(self):
        assert _F["mh714_anni_sostituzione"](25, 25) == []

    def test_anni_sostituzione_multipli(self):
        assert _F["mh714_anni_sostituzione"](5, 25) == [5, 10, 15, 20]
        assert _F["mh714_anni_sostituzione"](10, 25) == [10, 20]

    def test_anni_sostituzione_sotto_anno_vuota(self):
        assert _F["mh714_anni_sostituzione"](0.5, 25) == []

    def test_anni_sostituzione_esclude_vita_progetto(self):
        assert _F["mh714_anni_sostituzione"](25, 25) == []

    def test_co2_evitata_demo(self):
        assert _F["mh714_co2_evitata"](
            E_DEMO, 0.35) == pytest.approx(CO2_EV_DEMO, rel=REL)
        assert CO2_EV_DEMO > 0.0

    def test_co2_evitata_zero_se_fattore_zero(self):
        assert _F["mh714_co2_evitata"](
            E_DEMO, 0.0) == pytest.approx(0.0, abs=1e-9)


class TestFinanza:
    def test_van_flussi_demo(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 25
        assert abs(_F["mh714_van_flussi"](
            flussi, 0.06) - VAN_DEMO) <= 1.0

    def test_van_flussi_formula_chiusa_senza_sostituzioni(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 25
        atteso = -DELTA_DEMO + RISPARMIO_DEMO * (
            1.0 - 1.06 ** (-25)) / 0.06
        assert _F["mh714_van_flussi"](
            flussi, 0.06) == pytest.approx(atteso, rel=1e-12)

    def test_van_flussi_tasso_zero(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 25
        assert _F["mh714_van_flussi"](
            flussi, 0.0) == pytest.approx(
            -DELTA_DEMO + RISPARMIO_DEMO * 25, rel=1e-12)

    def test_van_flussi_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh714_van_flussi"]([100.0, 100.0], -0.01)

    def test_flussi_demo(self):
        flussi = _F["mh714_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CX_FISSA_DEMO, CX_FLOAT_DEMO, [], [], 25)
        assert len(flussi) == 26
        assert flussi[0] == pytest.approx(-DELTA_DEMO, rel=REL)
        assert flussi[1] == pytest.approx(RISPARMIO_DEMO, rel=REL)

    def test_flussi_con_sostituzione_entrambi(self):
        flussi = _F["mh714_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CX_FISSA_DEMO, CX_FLOAT_DEMO, [15], [10, 20], 25)
        assert flussi[10] == pytest.approx(
            -1935000000.0, rel=REL)
        assert flussi[15] == pytest.approx(
            1920000000.0, rel=REL)
        assert flussi[20] == pytest.approx(
            -1935000000.0, rel=REL)

    def test_tir_demo_verifica_npv_zero(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 25
        tir = _F["mh714_tir_flussi"](flussi)
        assert tir is not None
        assert abs(tir * 100.0 - TIR_DEMO) <= 0.01
        npv = -DELTA_DEMO + sum(
            flussi[i] / (1.0 + tir) ** i
            for i in range(1, 26))
        assert abs(npv) <= 1e-6 * DELTA_DEMO

    def test_tir_none_tutti_flussi_non_negativi(self):
        assert _F["mh714_tir_flussi"](
            [0.0] + [RISPARMIO_DEMO] * 25) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh714_tir_flussi"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo_tre(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 25
        assert _F["mh714_payback_flussi"](flussi) == PAYBACK_DEMO

    def test_payback_primo_anno_cumulato_non_negativo(self):
        assert _F["mh714_payback_flussi"](
            [-1000.0, 300.0, 300.0, 300.0, 300.0]) == 4
        assert -1000.0 + 300.0 * 3 < 0.0
        assert -1000.0 + 300.0 * 4 >= 0.0

    def test_payback_none_se_mai(self):
        assert _F["mh714_payback_flussi"](
            [-500000000.0] + [RISPARMIO_DEMO] * 25) is None

    def test_payback_zero_se_cumulato_anno_zero_non_negativo(self):
        assert _F["mh714_payback_flussi"](
            [0.0] + [RISPARMIO_DEMO] * 25) == 0

    def test_verdetto_conviente_demo(self):
        assert _F["mh714_verdetto"](
            VAN_DEMO, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == VERDETTO_DEMO

    def test_verdetto_van_zero_conviente(self):
        assert _F["mh714_verdetto"](
            0.0, DELTA_DEMO, 0.10, RISPARMIO_DEMO) == "CONVIENTE"

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh714_verdetto"](
            -100.0, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh714_verdetto"](
            -4500000.0, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh714_verdetto"](
            -4500001.0, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_non_positivo(
            self):
        assert _F["mh714_verdetto"](
            1000.0, DELTA_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh714_verdetto"](
            1000.0, DELTA_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_delta_zero_van_positivo_conviente(
            self):
        assert _F["mh714_verdetto"](
            1000.0, 0.0, 0.10, RISPARMIO_DEMO) == "CONVIENTE"

    def test_verdetto_delta_zero_van_negativo_non_conviente(
            self):
        assert _F["mh714_verdetto"](
            -1.0, 0.0, 0.10, RISPARMIO_DEMO) != "MARGINALE"
        assert _F["mh714_verdetto"](
            -1.0, 0.0, 0.10, RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh714_verdetto"](100.0, DELTA_DEMO, -0.01, RISPARMIO_DEMO)

    def test_verdetto_rifiuta_tolleranza_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh714_verdetto"](100.0, DELTA_DEMO, 1.5, RISPARMIO_DEMO)


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh714_demo"]()
        d.update(kw)
        return _F["mh714_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["e_mwh_a"] == pytest.approx(E_DEMO, rel=REL)
        assert c["p_fissa_mw"] == pytest.approx(
            P_FISSA_DEMO, rel=REL)
        assert c["capex_float_eur"] == pytest.approx(
            CX_FLOAT_DEMO, rel=REL)
        assert c["capex_fissa_eur"] == pytest.approx(
            CX_FISSA_DEMO, rel=REL)
        assert c["capex_delta_eur"] == pytest.approx(
            DELTA_DEMO, rel=REL)
        assert c["costo_base_eur_a"] == pytest.approx(
            C_BASE_DEMO, rel=REL)
        assert c["costo_alt_eur_a"] == pytest.approx(
            C_ALT_DEMO, rel=REL)
        assert c["risparmio_eur_a"] == pytest.approx(
            RISPARMIO_DEMO, rel=REL)
        assert c["anni_sost_float"] == []
        assert c["anni_sost_fissa"] == []
        assert c["co2_evitata_t_a"] == pytest.approx(
            CO2_EV_DEMO, rel=REL)
        assert abs(c["van"] - VAN_DEMO) <= 1.0
        assert abs(c["tir"] - TIR_DEMO) <= 0.01
        assert c["payback"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()[
            "van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()[
            "risparmio_eur_a"] == _F["demo_calcoli"]()[
            "risparmio_eur_a"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        d = _F["mh714_demo"]()
        b = _F["mh714_calcola"](**d)
        coppie = [("e_mwh_a", E_DEMO),
                  ("p_fissa_mw", P_FISSA_DEMO),
                  ("capex_float_eur", CX_FLOAT_DEMO),
                  ("capex_fissa_eur", CX_FISSA_DEMO),
                  ("capex_delta_eur", DELTA_DEMO),
                  ("costo_base_eur_a", C_BASE_DEMO),
                  ("costo_alt_eur_a", C_ALT_DEMO),
                  ("risparmio_eur_a", RISPARMIO_DEMO),
                  ("co2_evitata_t_a", CO2_EV_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert abs(b["van"] - VAN_DEMO) <= 1.0
        assert abs(b["tir"] - TIR_DEMO) <= 0.01
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh714_demo"]()
        assert d["p_float_mw"] == 500.0
        assert d["cf_float"] == 0.60
        assert d["cf_fissa"] == 0.40
        assert d["c_float_eur_kw"] == 3800.0
        assert d["c_fissa_eur_kw"] == 2500.0
        assert d["fisso_float_eur"] == 50000000.0
        assert d["fisso_fissa_eur"] == 30000000.0
        assert d["om_float_eur_kw_a"] == 90.0
        assert d["om_fissa_eur_kw_a"] == 80.0
        assert d["vita_anni_float"] == 25
        assert d["vita_anni_fissa"] == 25
        assert d["vita_progetto_anni"] == 25
        assert d["wacc_frac"] == 0.06
        assert d["tolleranza_frac"] == 0.10
        assert d["f_rete_t_mwh"] == 0.35

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("e_mwh_a",
                       "p_fissa_mw",
                       "capex_float_eur",
                       "capex_fissa_eur",
                       "capex_delta_eur",
                       "costo_base_eur_a",
                       "costo_alt_eur_a",
                       "risparmio_eur_a",
                       "co2_evitata_t_a", "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 3" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_cf_float_basso_non_conviente(self):
        # CF galleggiante 0,50: E 2190000, P_fissa
        # 625, CAPEX fissa 1592500000, delta
        # 357500000, risparmio 5000000; VAN
        # -293583219,21 -> NON_CONVIENTE, payback
        # mai entro 25 anni
        n = self._bc(cf_float=0.50)
        assert n["valid"] is True
        assert n["e_mwh_a"] == pytest.approx(
            2190000.0, rel=REL)
        assert n["p_fissa_mw"] == pytest.approx(
            625.0, rel=REL)
        assert n["capex_fissa_eur"] == pytest.approx(
            1592500000.0, rel=REL)
        assert n["capex_delta_eur"] == pytest.approx(
            357500000.0, rel=REL)
        assert n["risparmio_eur_a"] == pytest.approx(
            5000000.0, rel=REL)
        assert abs(n["van"] - (-293583219.208658)) <= 1.0
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["payback"] is None

    def test_costo_float_marginale(self):
        # Costo specifico galleggiante 4100
        # EUR/kW: delta 195000000; VAN
        # -3249657,63 entro tolleranza 19500000
        # -> MARGINALE; payback 13
        n = self._bc(c_float_eur_kw=4100.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            195000000.0, rel=REL)
        assert abs(n["van"] - (-3249657.625973986)) <= 1.0
        assert n["verdetto"] == "MARGINALE"
        assert n["payback"] == 13

    def test_costo_float_non_conviente(self):
        # Costo specifico galleggiante 4500
        # EUR/kW: delta 395000000; VAN
        # -203249657,63 oltre tolleranza
        # 39500000 -> NON_CONVIENTE; payback mai
        n = self._bc(c_float_eur_kw=4500.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            395000000.0, rel=REL)
        assert abs(n["van"] - (-203249657.625974)) <= 1.0
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["payback"] is None

    def test_om_float_alto_non_calcolabile(self):
        # O&M galleggiante 200: C_alt 100000000
        # > C_base 60000000 -> risparmio -40000000
        # -> dict neutro NON_CALCOLABILE
        n = self._bc(om_float_eur_kw_a=200.0)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_capex_delta_zero_mai_marginale(self):
        # Tutti i costi CAPEX a zero -> delta 0
        n = self._bc(c_float_eur_kw=0.0, fisso_float_eur=0.0,
                     c_fissa_eur_kw=0.0, fisso_fissa_eur=0.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            0.0, abs=1e-6)
        assert n["verdetto"] == "CONVIENTE"
        assert n["verdetto"] != "MARGINALE"
        assert n["payback"] == 0
        assert n["tir"] is None

    def test_sostituzioni_entrambi(self):
        # Vita anni galleggiante 10 e fissa 15:
        # sostituzioni float 10, 20 e fissa 15;
        # flusso anno 10 = -1935000000, anno 15 =
        # 1920000000, anno 20 = -1935000000;
        # VAN -755248749,34 circa
        n = self._bc(vita_anni_float=10, vita_anni_fissa=15)
        assert n["valid"] is True
        assert n["anni_sost_float"] == [10, 20]
        assert n["anni_sost_fissa"] == [15]
        assert n["df_flussi"]["Flusso (€/anno)"].iloc[10] == \
            pytest.approx(-1935000000.0, rel=REL)
        assert n["df_flussi"]["Flusso (€/anno)"].iloc[15] == \
            pytest.approx(1920000000.0, rel=REL)
        assert n["df_flussi"]["Flusso (€/anno)"].iloc[20] == \
            pytest.approx(-1935000000.0, rel=REL)
        assert abs(n["van"] - (-755248749.3371135)) <= 1.0

    def test_cf_float_zero_neutro(self):
        n = self._bc(cf_float=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_cf_fissa_sopra_uno_neutro(self):
        n = self._bc(cf_fissa=1.1)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_p_float_zero_neutro(self):
        n = self._bc(p_float_mw=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_progetto_zero_neutro(self):
        n = self._bc(vita_progetto_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_anni_zero_neutro(self):
        n = self._bc(vita_anni_float=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_negativo_neutro(self):
        n = self._bc(wacc_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_sopra_uno_neutro(self):
        n = self._bc(tolleranza_frac=1.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(cf_float=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(p_float_mw=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(p_float_mw=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_zero_calcolabile_conviente(self):
        # WACC 0: VAN -45000000 + 15000000 x 25
        # = 330000000
        n = self._bc(wacc_frac=0.0)
        assert n["van"] == pytest.approx(
            330000000.0, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh714_neutro"]()
        assert n["valid"] is False
        assert n["errore"] == ""
        assert list(n["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(n["df_flussi"]) == 0
        assert list(n["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(n["df_tabella"]) == 0

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh714_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "p_float_mw", "cf_float",
                       "cf_fissa",
                       "e_mwh_a", "p_fissa_mw",
                       "capex_float_eur",
                       "capex_fissa_eur",
                       "capex_delta_eur",
                       "costo_base_eur_a",
                       "costo_alt_eur_a",
                       "risparmio_eur_a",
                       "anni_sost_float",
                       "anni_sost_fissa",
                       "co2_evitata_t_a",
                       "van", "tir", "payback",
                       "verdetto", "df_flussi",
                       "df_tabella"):
            assert chiave in n, chiave
        assert n["errore"] == "errore di prova"
        assert n["tir"] is None

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert b["valid"] is True
        assert list(b["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(b["df_tabella"]) == 22
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Energia annua (MWh/anno)" in voci
        assert "Potenza fissa equivalente (MW)" in voci
        assert "CAPEX galleggiante (EUR)" in voci
        assert "CAPEX fissa (EUR)" in voci
        assert "CAPEX delta (EUR)" in voci
        assert "Costo annuo baseline (EUR/anno)" in voci
        assert "Costo annuo alternativa (EUR/anno)" in voci
        assert "Risparmio annuo (EUR/anno)" in voci
        assert "CO2 evitata vs rete (t/anno)" in voci
        assert "VAN (EUR)" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(b["df_flussi"]) == VITA_DEMO + 1
        assert b["df_flussi"]["Flusso (€/anno)"].iloc[0] == \
            pytest.approx(-DELTA_DEMO, rel=REL)
        assert b["df_flussi"]["Flusso (€/anno)"].iloc[1] == \
            pytest.approx(RISPARMIO_DEMO, rel=REL)


class TestSensitivitaCsv:
    def _ing(self):
        return _F["mh714_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh714_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.9", "x1.0", "x1.1"]
        assert list(s.index) == ["x0.9", "x1.0", "x1.1"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh714_sensitivita"](self._ing())
        assert abs(s.loc["x1.0", "x1.0"] - VAN_DEMO) <= 1.0

    def test_sensitivita_crescente_con_cf(self):
        s = _F["mh714_sensitivita"](self._ing())
        for colonna in ("x0.9", "x1.0", "x1.1"):
            assert s.loc["x0.9", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.1", colonna]

    def test_sensitivita_decrescente_con_costo_float(self):
        s = _F["mh714_sensitivita"](self._ing())
        for riga in ("x0.9", "x1.0", "x1.1"):
            assert s.loc[riga, "x0.9"] > \
                s.loc[riga, "x1.0"] > \
                s.loc[riga, "x1.1"]

    def test_sensitivita_diagonale_non_uguale_centro(self):
        # A differenza di un prodotto puro, qui il
        # CF cambia anche P_fissa, CAPEX_fissa e
        # C_base, mentre il costo cambia solo il
        # CAPEX_float: sulla diagonale il VAN NON
        # resta quello del centro (proprieta'
        # strutturale, non errore).
        s = _F["mh714_sensitivita"](self._ing())
        assert abs(s.loc["x0.9", "x0.9"] - VAN_DEMO) > 1.0
        assert abs(s.loc["x1.1", "x1.1"] - VAN_DEMO) > 1.0

    def test_sensitivita_nessuna_colonna_degenere(self):
        s = _F["mh714_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_nessuna_colonna_costante(self):
        s = _F["mh714_sensitivita"](self._ing())
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3

    def test_sensitivita_angoli(self):
        s = _F["mh714_sensitivita"](self._ing())
        assert abs(s.loc["x0.9", "x0.9"] - 72550205.4244156) <= 1.0
        assert abs(s.loc["x0.9", "x1.1"] - (-307449794.5755844)) <= 1.0
        assert abs(s.loc["x1.1", "x0.9"] - 600950479.3236364) <= 1.0
        assert abs(s.loc["x1.1", "x1.1"] - 220950479.3236364) <= 1.0

    def test_sensitivita_con_sostituzioni_ricalcolate(self):
        # Con vita anni galleggiante 10 e fissa
        # 15 la griglia deve includere le
        # sostituzioni: il centro deve coincidere
        # col VAN del caso con sostituzioni
        ing = self._ing()
        ing["vita_anni_float"] = 10
        ing["vita_anni_fissa"] = 15
        s = _F["mh714_sensitivita"](ing)
        assert abs(s.loc["x1.0", "x1.0"] - (-755248749.3371135)) <= 1.0

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh714_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 29

    def test_csv_contiene_verdetto_e_risparmio(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh714_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "risparmio_eur_a" in txt
        assert "costo_base_eur_a" in txt
        assert "costo_alt_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "p_float_mw" in txt
        assert "e_mwh_a" in txt
        assert "co2_evitata_t_a" in txt
        assert "cf_float" in txt
        assert "capex_float_eur" in txt
        assert "capex_delta_eur" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh714_csv"](bc, self._ing())
        assert f"risparmio_eur_a;{bc['risparmio_eur_a']}" in txt
        assert f"costo_base_eur_a;{bc['costo_base_eur_a']}" in txt
        assert "p_float_mw;500.0" in txt
        assert "om_float_eur_kw_a;90.0" in txt
        assert f"capex_delta_eur;{bc['capex_delta_eur']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def714["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def714\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 15, ui_keys
        demo_keys = set(_F["mh714_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh714_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh714_demo():")
        depth = 0
        body = ""
        started = False
        for ch in src[start:]:
            body += ch
            if ch == "{":
                depth += 1
                started = True
            elif ch == "}":
                depth -= 1
                if started and depth == 0:
                    break
        demo_keys = set(re.findall(r'"([A-Za-z0-9_]+)":', body))
        ui_keys = set(re.findall(r'_def714\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W715 (25/10/2026) - tab714' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh714_num", "mh714_nneg", "mh714_pos",
                     "mh714_int_pos", "mh714_int_nneg",
                     "mh714_quota_valida", "mh714_cf_valido",
                     "mh714_e_annua", "mh714_p_fissa",
                     "mh714_capex", "mh714_costo_annuo",
                     "mh714_risparmio", "mh714_anni_sostituzione",
                     "mh714_flussi",
                     "mh714_van_flussi", "mh714_tir_flussi",
                     "mh714_payback_flussi", "mh714_verdetto",
                     "mh714_co2_evitata", "mh714_valida",
                     "_mh714_neutro", "mh714_calcola",
                     "mh714_sensitivita", "mh714_csv",
                     "mh714_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_helpers_nessun_residuo_tab_precedente(self):
        # La tab precedente e' la tab713
        # (teleriscaldamento 5G): i frammenti
        # nuovi non devono contenere i suoi
        # identificatori.
        assert "mh713" not in _helpers_src()
        assert "tab713" not in _helpers_src()
        assert "mh713" not in _ui_src()
        assert "tab713" not in _ui_src()

    def test_chain_riferimento_tab_precedente(self):
        # Catena: questo file test fa riferimento
        # alla tab precedente tab713 come punto di
        # confronto (test residuo sopra) e la
        # nuova tab e' tab714.
        src = Path(__file__).read_text(encoding="utf-8")
        assert "tab713" in src
        assert "tab714" in src
        assert _ui_src().startswith("    with tab714:")

    def test_helpers_parse_ast(self):
        import textwrap
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w715_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE714) == 1

    def test_blocco_with_tab714(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab714:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE714

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st714_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 20, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st714_") for k in keys)

    def test_chiavi_st_input_sono_16(self):
        """Le 16 chiavi di input/bottone (15 input +
        bottone calcola) sono tutte presenti; le
        altre 4 sono solo chiavi di
        visualizzazione (fig, heatmap, flussi, CSV)."""
        keys = re.findall(r'key="(st714_[a-z0-9_]+)"', _ui_src())
        attese = ["st714_p_float", "st714_cf_float",
                  "st714_cf_fissa", "st714_c_float",
                  "st714_c_fissa", "st714_fisso_float",
                  "st714_fisso_fissa", "st714_om_float",
                  "st714_om_fissa", "st714_vita_float",
                  "st714_vita_fissa", "st714_vita_progetto",
                  "st714_wacc", "st714_tolleranza",
                  "st714_f_rete", "st714_calcola"]
        assert len(attese) == 16
        for k in attese:
            assert k in keys, k

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg714" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg714") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg714")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Energia annua (MWh/anno)" in src
        assert "Risparmio annuo (€/anno)" in src
        assert "VAN (€)" in src
        assert "CO2 evitata vs rete (t/anno)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_ver714" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_distinzioni_presente(self):
        src = _ui_src().lower()
        assert "tab272" in src
        assert "tab685" in src
        assert "tab679" in src
        assert "informative" in src
        assert "capex" in src
        assert "profonde" in src
        assert "pari energia" in src

    def test_distinzione_altre_tab_in_helpers(self):
        src = _helpers_src()
        assert "tab272" in src.lower()
        assert "tab685" in src.lower()
        assert "tab679" in src.lower()

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Costo annuo baseline" in src
        assert "Costo annuo alternativa" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh714_csv" in src
        assert "eolico_offshore_galleggiante_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh714_sensitivita" in src
        assert "Heatmap" in src
        assert "CF galleggiante" in src
        assert "Costo specifico galleggiante" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st714_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W715 (25/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab714:")
