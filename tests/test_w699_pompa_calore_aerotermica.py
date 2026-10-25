"""Test tab699 "🌬️🔥 Pompa di calore aerotermica: l'aria esterna scalda l'edificio a prezzo giusto?"

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
domanda 300 MWh/anno; picco 150 kW; SCOP 3,5;
prezzo elettricita' 200 EUR/MWh; OPEX annuo
1500 EUR/anno; rendimento caldaia 0,9; prezzo
gas 100 EUR/MWh; costo specifico 800 EUR/kW;
costo fisso 5000 EUR; vita 20 anni; WACC 5 %;
tolleranza 10 % del CAPEX; fattore gas 0,20
tCO2/MWh; fattore elettricita' 0,35 tCO2/MWh.

- energia_elettrica_mwh_a = 85.71428571428571
- costo_baseline_eur_a = 33333.33333333333
- costo_pompa_eur_a = 18642.85714285714
- risparmio_eur_a = 14690.476190476187
- co2_evitata_t_a = 36.66666666666667
- capex_eur = 125000.0
- van = 58075.80431778982
- tir = 10.008005037433062
- payback = 9
- verdetto = 'CONVIENTE'

Scomposizione: e_el 300 / 3,5 =
85,71428571428571; c_base 300 / 0,9 x 100 =
33333,33333333333; c_hp 85,71428571428571 x
200 + 1500 = 18642,85714285714; risparmio
33333,33333333333 - 18642,85714285714 =
14690,476190476187; co2 300 / 0,9 x 0,20 -
85,71428571428571 x 0,35 = 36,66666666666667;
capex 150 x 800 + 5000 = 125000,0; VAN
-125000,0 + 14690,476190476187 x
(1 - 1,05^-20) / 0,05 = 58075,80431778982;
TIR per bisezione su [-0,99, 5,0] dei flussi
[-125000, 14690,476190476187 x 20]:
10,008005037433062 % (VAN a quella TIR ~0);
payback: cumulato anno 8 -7476,19047619048,
anno 9 +7214,28571428572 -> 9.
NOTA: il brief indicava "TIR ~9 %": il valore
esatto ricalcolato e' 10,01 %, non 9 % — il
test fissa il valore esatto, non la stima
del brief.
"""

import ast
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w700_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w700_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w700_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w700_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w700_helpers.py: {missing}")
    return out


_F = _load("mh699_num", "mh699_nneg", "mh699_pos",
           "mh699_int_pos", "mh699_scop_valido",
           "mh699_rendimento_valido",
           "mh699_energia_elettrica",
           "mh699_costo_baseline", "mh699_costo_pompa",
           "mh699_risparmio", "mh699_co2_evitata",
           "mh699_capex", "mh699_crf", "mh699_van",
           "mh699_tir", "mh699_payback",
           "mh699_verdetto", "mh699_valida",
           "_mh699_neutro", "mh699_calcola",
           "mh699_sensitivita", "mh699_csv",
           "mh699_demo", "demo_calcoli")

TITLE699 = ("🌬️🔥 Pompa di calore aerotermica: "
            "l'aria esterna scalda l'edificio "
            "a prezzo giusto?")

E_EL_DEMO = 85.71428571428571
C_BASE_DEMO = 33333.33333333333
C_HP_DEMO = 18642.85714285714
RISP_DEMO = 14690.476190476187
CO2_DEMO = 36.66666666666667
CAPEX_DEMO = 125000.0
VAN_DEMO = 58075.80431778982
TIR_DEMO = 10.008005037433062
PAYBACK_DEMO = 9
VITA_DEMO = 20
VERDETTO_DEMO = "CONVIENTE"
CRF_DEMO = 0.08024258719069129

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w700_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w700_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh699_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh699_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh699_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh699_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh699_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh699_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh699_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh699_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh699_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh699_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh699_int_pos"](20.0, "x") == 20

    def test_scop_rifiuta_uno(self):
        with pytest.raises(ValueError):
            _F["mh699_scop_valido"](1.0, "x")

    def test_scop_rifiuta_sotto_uno(self):
        with pytest.raises(ValueError):
            _F["mh699_scop_valido"](0.5, "x")

    def test_scop_accetta_sopra_uno(self):
        assert _F["mh699_scop_valido"](3.5, "x") == 3.5

    def test_rendimento_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh699_rendimento_valido"](0.0, "x")

    def test_rendimento_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh699_rendimento_valido"](1.2, "x")

    def test_rendimento_accetta_uno(self):
        assert _F["mh699_rendimento_valido"](1.0, "x") == 1.0


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh699_demo"]()
        d.update(kw)
        return _F["mh699_valida"](**d)

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_scop_uno_non_valido(self):
        v = self._val(scop=1.0)
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_scop_sotto_uno_non_valido(self):
        v = self._val(scop=0.8)
        assert v["valido"] is False

    def test_rendimento_zero_non_valido(self):
        v = self._val(rendimento_caldaia=0.0)
        assert v["valido"] is False

    def test_rendimento_sopra_uno_non_valido(self):
        v = self._val(rendimento_caldaia=1.2)
        assert v["valido"] is False

    def test_vita_zero_non_valida(self):
        v = self._val(vita_anni=0)
        assert v["valido"] is False

    def test_vita_non_intera_non_valida(self):
        v = self._val(vita_anni=19.5)
        assert v["valido"] is False

    def test_negativi_non_validi(self):
        for k in ("domanda_mwh_a", "potenza_picco_kw",
                  "prezzo_elettricita_eur_mwh", "opex_annuo",
                  "prezzo_gas_eur_mwh",
                  "costo_specifico_eur_kw", "costo_fisso_eur",
                  "wacc_pct", "tolleranza_pct",
                  "fattore_gas", "fattore_elettricita"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_nan_non_valido(self):
        v = self._val(scop=float("nan"))
        assert v["valido"] is False

    def test_inf_non_valido(self):
        v = self._val(domanda_mwh_a=float("inf"))
        assert v["valido"] is False

    def test_bool_non_valido(self):
        v = self._val(domanda_mwh_a=True)
        assert v["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        # mh699_valida non deve MAI sollevare:
        # tipi non numerici -> dict non valido
        v = self._val(scop="3.5")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        # Brief tab699: finiti e >= 0 (SCOP > 1,
        # eta in (0, 1] escluse); domanda 0, picco
        # 0 e prezzi 0 passano la validazione e
        # cadono solo nella guard di calcola
        # (risparmio <= 0 -> NON_CALCOLABILE).
        assert self._val(domanda_mwh_a=0.0)["valido"] is True
        assert self._val(potenza_picco_kw=0.0)["valido"] is True
        assert self._val(
            prezzo_elettricita_eur_mwh=0.0)["valido"] is True
        assert self._val(prezzo_gas_eur_mwh=0.0)["valido"] is True

    def test_wacc_senza_tetto_superiore(self):
        # Brief tab699: WACC >= 0 senza tetto
        # (diversa dalla tab precedente, che chiudeva a 100)
        assert self._val(wacc_pct=150.0)["valido"] is True
        assert self._val(tolleranza_pct=150.0)["valido"] is True


class TestFisicaEconomia:
    def test_energia_elettrica_demo(self):
        assert _F["mh699_energia_elettrica"](
            300.0, 3.5) == pytest.approx(E_EL_DEMO, rel=REL)

    def test_energia_elettrica_rifiuta_scop_uno(self):
        with pytest.raises(ValueError):
            _F["mh699_energia_elettrica"](300.0, 1.0)

    def test_costo_baseline_demo(self):
        assert _F["mh699_costo_baseline"](
            300.0, 0.9, 100.0) == pytest.approx(
            C_BASE_DEMO, rel=REL)

    def test_costo_baseline_rifiuta_rendimento_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh699_costo_baseline"](300.0, 1.2, 100.0)

    def test_costo_baseline_rifiuta_eta_zero(self):
        with pytest.raises(ValueError):
            _F["mh699_costo_baseline"](300.0, 0.0, 100.0)

    def test_costo_pompa_demo(self):
        assert _F["mh699_costo_pompa"](
            E_EL_DEMO, 200.0, 1500.0) == pytest.approx(
            C_HP_DEMO, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh699_risparmio"](
            C_BASE_DEMO, C_HP_DEMO) == pytest.approx(
            RISP_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh699_risparmio"](
            10000.0, 18642.85714285714) == pytest.approx(
            -8642.85714285714, rel=REL)

    def test_co2_demo(self):
        assert _F["mh699_co2_evitata"](
            300.0, 0.9, 0.20,
            E_EL_DEMO, 0.35) == pytest.approx(
            CO2_DEMO, rel=REL)

    def test_co2_puo_essere_negativa(self):
        assert _F["mh699_co2_evitata"](
            300.0, 0.9, 0.05,
            E_EL_DEMO, 0.90) < 0.0

    def test_capex_demo(self):
        assert _F["mh699_capex"](
            150.0, 800.0, 5000.0) == pytest.approx(
            CAPEX_DEMO, rel=REL)

    def test_capex_solo_fisso(self):
        assert _F["mh699_capex"](
            0.0, 800.0, 5000.0) == 5000.0

    def test_capex_scala_con_picco(self):
        assert _F["mh699_capex"](
            300.0, 800.0, 5000.0) == pytest.approx(
            245000.0, rel=REL)

    def test_crf_demo(self):
        assert _F["mh699_crf"](
            0.05, 20) == pytest.approx(CRF_DEMO, rel=REL)

    def test_crf_wacc_zero(self):
        assert _F["mh699_crf"](0.0, 20) == pytest.approx(
            0.05, rel=1e-12)

    def test_crf_formula_chiusa(self):
        atteso = 0.05 * 1.05 ** 20 / (1.05 ** 20 - 1.0)
        assert _F["mh699_crf"](0.05, 20) == pytest.approx(
            atteso, rel=1e-12)


class TestFinanza:
    def test_van_demo_tolleranza_1_eur(self):
        assert abs(_F["mh699_van"](
            RISP_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) - VAN_DEMO) <= 1.0

    def test_van_formula_chiusa(self):
        atteso = -CAPEX_DEMO + RISP_DEMO * (
            1.0 - 1.05 ** (-20)) / 0.05
        assert _F["mh699_van"](
            RISP_DEMO, CAPEX_DEMO, 0.05,
            VITA_DEMO) == pytest.approx(atteso, rel=1e-12)

    def test_van_tasso_zero(self):
        assert _F["mh699_van"](
            RISP_DEMO, CAPEX_DEMO, 0.0,
            20) == pytest.approx(
            -CAPEX_DEMO + RISP_DEMO * 20, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh699_van"](RISP_DEMO, CAPEX_DEMO, -0.01, 20)

    def test_van_rifiuta_capex_negativo(self):
        with pytest.raises(ValueError):
            _F["mh699_van"](RISP_DEMO, -1.0, 0.05, 20)

    def test_tir_demo_tolleranza_005_punti(self):
        tir_pct = _F["mh699_tir"](
            CAPEX_DEMO, RISP_DEMO, VITA_DEMO) * 100.0
        assert abs(tir_pct - TIR_DEMO) <= 0.05

    def test_tir_bisezione_indipendente(self):
        # Ricalcolo indipendente: bisezione dei
        # flussi [-CAPEX, risparmio x 20] su
        # [-0.99, 5.0]; il test non usa la TIR
        # attesa come oracolo, ma il suo zero.
        flussi = [-CAPEX_DEMO] + [RISP_DEMO] * 20

        def _npv(x):
            return sum(f / (1.0 + x) ** i
                       for i, f in enumerate(flussi))

        lo, hi = -0.99, 5.0
        n_lo = _npv(lo)
        for _ in range(200):
            mid = (lo + hi) / 2.0
            n_mid = _npv(mid)
            if (n_lo > 0.0) == (n_mid > 0.0):
                lo, n_lo = mid, n_mid
            else:
                hi = mid
            if hi - lo < 1e-12:
                break
        tir_ind = (lo + hi) / 2.0
        assert abs(tir_ind * 100.0 - TIR_DEMO) <= 0.05
        tir = _F["mh699_tir"](CAPEX_DEMO, RISP_DEMO, VITA_DEMO)
        assert abs(tir - tir_ind) <= 1e-9

    def test_tir_none_se_risparmio_non_positivo(self):
        assert _F["mh699_tir"](CAPEX_DEMO, 0.0, 20) is None
        assert _F["mh699_tir"](CAPEX_DEMO, -100.0, 20) is None

    def test_tir_none_se_capex_zero(self):
        assert _F["mh699_tir"](0.0, RISP_DEMO, 20) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh699_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_verifica_npv_zero(self):
        tir = _F["mh699_tir"](CAPEX_DEMO, RISP_DEMO, VITA_DEMO)
        npv = -CAPEX_DEMO + sum(
            RISP_DEMO / (1.0 + tir) ** i
            for i in range(1, 21))
        assert abs(npv) <= 1e-6 * CAPEX_DEMO

    def test_payback_demo(self):
        assert _F["mh699_payback"](
            CAPEX_DEMO, RISP_DEMO, VITA_DEMO) == PAYBACK_DEMO

    def test_payback_primo_anno_cumulato_non_negativo(self):
        assert -CAPEX_DEMO + RISP_DEMO * 8 < 0.0
        assert -CAPEX_DEMO + RISP_DEMO * 9 >= 0.0

    def test_payback_ceil_coerente(self):
        assert _F["mh699_payback"](1000.0, 300.0, 10) == 4

    def test_payback_anno_1_se_risparmio_ge_capex(self):
        assert _F["mh699_payback"](1000.0, 1000.0, 10) == 1
        assert _F["mh699_payback"](1000.0, 2000.0, 10) == 1

    def test_payback_none_se_mai_entro_vita(self):
        assert _F["mh699_payback"](
            50000000.0, RISP_DEMO, 20) is None

    def test_payback_zero_se_capex_zero(self):
        assert _F["mh699_payback"](0.0, RISP_DEMO, 20) == 0

    def test_payback_none_se_risparmio_non_positivo(self):
        assert _F["mh699_payback"](CAPEX_DEMO, 0.0, 20) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh699_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10,
            RISP_DEMO) == VERDETTO_DEMO

    def test_verdetto_van_zero_conviente(self):
        assert _F["mh699_verdetto"](
            0.0, CAPEX_DEMO, 0.10, RISP_DEMO) == "CONVIENTE"

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh699_verdetto"](
            -100.0, CAPEX_DEMO, 0.10, RISP_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        # |VAN| = 12500 = 10 % di CAPEX 125000
        assert _F["mh699_verdetto"](
            -12500.0, CAPEX_DEMO, 0.10,
            RISP_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh699_verdetto"](
            -12500.1, CAPEX_DEMO, 0.10,
            RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_non_positivo(
            self):
        assert _F["mh699_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh699_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_positivo_conviente(
            self):
        assert _F["mh699_verdetto"](
            1000.0, 0.0, 0.10, RISP_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(
            self):
        assert _F["mh699_verdetto"](
            -1.0, 0.0, 0.10, RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_capex_zero_mai_marginale(self):
        assert _F["mh699_verdetto"](
            -1.0, 0.0, 0.10, RISP_DEMO) != "MARGINALE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh699_verdetto"](100.0, CAPEX_DEMO, -0.01, RISP_DEMO)


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh699_demo"]()
        d.update(kw)
        return _F["mh699_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["energia_elettrica_mwh_a"] == pytest.approx(
            E_EL_DEMO, rel=REL)
        assert c["costo_baseline_eur_a"] == pytest.approx(
            C_BASE_DEMO, rel=REL)
        assert c["costo_pompa_eur_a"] == pytest.approx(
            C_HP_DEMO, rel=REL)
        assert c["risparmio_eur_a"] == pytest.approx(
            RISP_DEMO, rel=REL)
        assert c["co2_evitata_t_a"] == pytest.approx(
            CO2_DEMO, rel=REL)
        assert c["capex_eur"] == pytest.approx(
            CAPEX_DEMO, rel=REL)
        assert abs(c["van"] - VAN_DEMO) <= 1.0
        assert abs(c["tir"] - TIR_DEMO) <= 0.05
        assert c["payback"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()[
            "van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()[
            "risparmio_eur_a"] == _F["demo_calcoli"]()[
            "risparmio_eur_a"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        """mh699_calcola(**mh699_demo()) deve matchare le
        costanti _DEMO entro 1e-9 relativo (VAN ±1 EUR,
        TIR ±0,05 punti), chiave per chiave."""
        d = _F["mh699_demo"]()
        b = _F["mh699_calcola"](**d)
        coppie = [("energia_elettrica_mwh_a", E_EL_DEMO),
                  ("costo_baseline_eur_a", C_BASE_DEMO),
                  ("costo_pompa_eur_a", C_HP_DEMO),
                  ("risparmio_eur_a", RISP_DEMO),
                  ("co2_evitata_t_a", CO2_DEMO),
                  ("capex_eur", CAPEX_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert abs(b["van"] - VAN_DEMO) <= 1.0
        assert abs(b["tir"] - TIR_DEMO) <= 0.05
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh699_demo"]()
        assert d["domanda_mwh_a"] == 300.0
        assert d["potenza_picco_kw"] == 150.0
        assert d["scop"] == 3.5
        assert d["prezzo_elettricita_eur_mwh"] == 200.0
        assert d["opex_annuo"] == 1500.0
        assert d["rendimento_caldaia"] == 0.9
        assert d["prezzo_gas_eur_mwh"] == 100.0
        assert d["costo_specifico_eur_kw"] == 800.0
        assert d["costo_fisso_eur"] == 5000.0
        assert d["vita_anni"] == 20
        assert d["wacc_pct"] == 5.0
        assert d["tolleranza_pct"] == 10.0
        assert d["fattore_gas"] == 0.20
        assert d["fattore_elettricita"] == 0.35

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("energia_elettrica_mwh_a",
                       "costo_baseline_eur_a",
                       "costo_pompa_eur_a",
                       "risparmio_eur_a",
                       "co2_evitata_t_a",
                       "capex_eur",
                       "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 9" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_domanda_dimezzata(self):
        # Domanda 150 MWh/a (picco invariato):
        # e_el 42,8571; c_base 16666,6667; c_hp
        # 10071,4286; risparmio 6595,2381; co2
        # 18,3333; capex invariato 125000,0
        n = self._bc(domanda_mwh_a=150.0)
        assert n["valid"] is True
        assert n["energia_elettrica_mwh_a"] == pytest.approx(
            42.857142857142854, rel=REL)
        assert n["risparmio_eur_a"] == pytest.approx(
            6595.238095238094, rel=REL)
        assert n["co2_evitata_t_a"] == pytest.approx(
            18.333333333333336, rel=REL)
        assert n["capex_eur"] == pytest.approx(
            CAPEX_DEMO, rel=REL)

    def test_scop_cinque(self):
        # SCOP 5,0: e_el 60,0; c_hp 13500,0;
        # risparmio 19833,3333; capex invariato
        n = self._bc(scop=5.0)
        assert n["valid"] is True
        assert n["energia_elettrica_mwh_a"] == pytest.approx(
            60.0, rel=REL)
        assert n["risparmio_eur_a"] == pytest.approx(
            19833.33333333333, rel=REL)
        assert n["capex_eur"] == pytest.approx(
            CAPEX_DEMO, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_scop_uno_neutro(self):
        n = self._bc(scop=1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["errore"] != ""
        assert n["tir"] is None
        assert n["payback"] is None

    def test_scop_sotto_uno_neutro(self):
        n = self._bc(scop=0.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_rendimento_sopra_uno_neutro(self):
        n = self._bc(rendimento_caldaia=1.2)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_rendimento_zero_neutro(self):
        n = self._bc(rendimento_caldaia=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_non_intera_neutro(self):
        n = self._bc(vita_anni=19.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_uno_non_conviente(self):
        # VAN -125000 + 14690,48 / 1,05 < 0, oltre
        # tolleranza; payback mai
        n = self._bc(vita_anni=1)
        assert n["valid"] is True
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["payback"] is None

    def test_vita_undici_marginale(self):
        # VAN circa -2974,82, entro il 10 % del
        # CAPEX (12500); payback 9
        n = self._bc(vita_anni=11)
        assert n["valid"] is True
        assert n["verdetto"] == "MARGINALE"
        assert n["payback"] == 9

    def test_vita_nove_non_conviente(self):
        # VAN circa -20582,71, oltre il 10 % del
        # CAPEX; payback 9 (ma VAN negativo)
        n = self._bc(vita_anni=9)
        assert n["valid"] is True
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["payback"] == 9

    def test_vita_dodici_conviente(self):
        n = self._bc(vita_anni=12)
        assert n["valid"] is True
        assert n["verdetto"] == "CONVIENTE"

    def test_wacc_negativo_neutro(self):
        n = self._bc(wacc_pct=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_negativa_neutro(self):
        n = self._bc(tolleranza_pct=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(scop=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(domanda_mwh_a=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(domanda_mwh_a=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_domanda_zero_neutro_via_risparmio(self):
        # Domanda 0 passa la validazione (brief:
        # >= 0) ma il risparmio e' -OPEX <= 0, per
        # cui calcola resta NON_CALCOLABILE.
        n = self._bc(domanda_mwh_a=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["tir"] is None
        assert n["payback"] is None

    def test_risparmio_negativo_neutro(self):
        # Prezzo elettricita' 600: c_hp 52928,57
        # contro c_base 33333,33 -> risparmio < 0
        n = self._bc(prezzo_elettricita_eur_mwh=600.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_risparmio_zero_non_calcolabile(self):
        assert _F["mh699_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"

    def test_wacc_zero_calcolabile_conviente(self):
        n = self._bc(wacc_pct=0.0)
        assert n["van"] == pytest.approx(
            -CAPEX_DEMO + RISP_DEMO * 20, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_zero_conviente_non_marginale(self):
        n = self._bc(costo_specifico_eur_kw=0.0,
                     costo_fisso_eur=0.0)
        assert n["verdetto"] == "CONVIENTE"
        assert n["verdetto"] != "MARGINALE"
        assert n["payback"] == 0
        assert n["tir"] is None

    def test_capex_zero_van_negativo_mai_marginale(self):
        # Caso costruito via verdetto: CAPEX 0 e
        # VAN negativo non puo' essere MARGINALE
        assert _F["mh699_verdetto"](
            -1.0, 0.0, 0.10, RISP_DEMO) == "NON_CONVIENTE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh699_neutro"]()
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
        n = _F["_mh699_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "energia_elettrica_mwh_a",
                       "costo_baseline_eur_a",
                       "costo_pompa_eur_a",
                       "risparmio_eur_a",
                       "co2_evitata_t_a",
                       "capex_eur",
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
        assert len(b["df_tabella"]) == 18
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Energia elettrica annua (MWh/anno)" in voci
        assert "Costo baseline (EUR/anno)" in voci
        assert "Risparmio annuo (EUR/anno)" in voci
        assert "CO2 evitata (t/anno)" in voci
        assert "CAPEX (EUR)" in voci
        assert "VAN (EUR)" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(b["df_flussi"]) == VITA_DEMO + 1
        assert b["df_flussi"]["Cumulato (€)"].iloc[-1] == \
            pytest.approx(-CAPEX_DEMO + RISP_DEMO * VITA_DEMO,
                          rel=REL)


class TestSensitivitaCsv:
    def _ing(self):
        return _F["mh699_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh699_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.9", "x1.0", "x1.1"]
        assert list(s.index) == ["x0.9", "x1.0", "x1.1"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh699_sensitivita"](self._ing())
        assert abs(s.loc["x1.0", "x1.0"] - VAN_DEMO) <= 1.0

    def test_sensitivita_crescente_con_scop(self):
        # VAN cresce con lo SCOP: meno elettricita'
        # assorbita e piu' risparmio, a parita'
        # di prezzo
        s = _F["mh699_sensitivita"](self._ing())
        for colonna in ("x0.9", "x1.0", "x1.1"):
            assert s.loc["x0.9", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.1", colonna]

    def test_sensitivita_decrescente_con_prezzo_elettricita(self):
        # VAN cala con il prezzo elettricita':
        # il costo della pompa sale, il risparmio
        # scende
        s = _F["mh699_sensitivita"](self._ing())
        for riga in ("x0.9", "x1.0", "x1.1"):
            assert s.loc[riga, "x0.9"] > \
                s.loc[riga, "x1.0"] > \
                s.loc[riga, "x1.1"]

    def test_sensitivita_nessuna_colonna_degenere(self):
        # Il risparmio resta positivo su tutta la
        # griglia demo, nessuna cella puo' essere
        # 0,0 per regime degenere
        s = _F["mh699_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_nessuna_colonna_costante(self):
        # Ogni colonna (prezzo) varia davvero al
        # variare dello SCOP, e ogni riga varia
        # al variare del prezzo: nessuna colonna
        # o riga costante per costruzione.
        s = _F["mh699_sensitivita"](self._ing())
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3

    def test_sensitivita_payback_coerente(self):
        # Payback demo 9: cumulato anno 8 < 0,
        # anno 9 >= 0
        assert -CAPEX_DEMO + RISP_DEMO * 8 < 0.0
        assert -CAPEX_DEMO + RISP_DEMO * 9 >= 0.0

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh699_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 25

    def test_csv_contiene_verdetto_e_risparmio(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh699_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "risparmio_eur_a" in txt
        assert "costo_baseline_eur_a" in txt
        assert "costo_pompa_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "domanda_mwh_a" in txt
        assert "energia_elettrica_mwh_a" in txt
        assert "co2_evitata_t_a" in txt
        assert "scop" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh699_csv"](bc, self._ing())
        assert f"costo_baseline_eur_a;{bc['costo_baseline_eur_a']}" in txt
        assert f"risparmio_eur_a;{bc['risparmio_eur_a']}" in txt
        assert f"energia_elettrica_mwh_a;{E_EL_DEMO}" in txt
        assert "opex_annuo;1500.0" in txt


class TestStruttura:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def699["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def699\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 14, ui_keys
        demo_keys = set(_F["mh699_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh699_demo
        (mai regex \\{[^}]*\\} sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh699_demo():")
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
        ui_keys = set(re.findall(r'_def699\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys

    def test_header_helpers_presente(self):
        assert '# W700 (25/10/2026) - tab699' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh699_num", "mh699_nneg", "mh699_pos",
                     "mh699_int_pos", "mh699_scop_valido",
                     "mh699_rendimento_valido",
                     "mh699_energia_elettrica",
                     "mh699_costo_baseline",
                     "mh699_costo_pompa",
                     "mh699_risparmio", "mh699_co2_evitata",
                     "mh699_capex", "mh699_crf",
                     "mh699_van", "mh699_tir",
                     "mh699_payback", "mh699_verdetto",
                     "mh699_valida", "_mh699_neutro",
                     "mh699_calcola", "mh699_sensitivita",
                     "mh699_csv", "mh699_demo",
                     "demo_calcoli"):
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
        # l'apply: si dedenta prima del parse,
        # come farebbe l'apply
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w700_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE699) == 1

    def test_blocco_with_tab699(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab699:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE699

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st699_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 19, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st699_") for k in keys)

    def test_chiavi_st_input_sono_15(self):
        """Le 15 chiavi di input/bottone del brief
        (14 input + bottone calcola) sono tutte
        presenti; le altre 4 sono solo chiavi di
        visualizzazione (fig, heatmap, flussi, CSV)."""
        keys = re.findall(r'key="(st699_[a-z0-9_]+)"', _ui_src())
        attese = ["st699_domanda", "st699_picco",
                  "st699_scop",
                  "st699_prezzo_elettricita", "st699_opex",
                  "st699_rendimento", "st699_prezzo_gas",
                  "st699_fattore_gas",
                  "st699_fattore_elettricita",
                  "st699_costo_specifico", "st699_costo_fisso",
                  "st699_vita", "st699_wacc_pct",
                  "st699_tolleranza_pct", "st699_calcola"]
        assert len(attese) == 15
        for k in attese:
            assert k in keys, k

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg699" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg699") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg699")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Energia elettrica annua (MWh/anno)" in src
        assert "Risparmio annuo (€/anno)" in src
        assert "VAN (€)" in src
        assert "CO2 evitata (t/anno)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd699" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_aerotermica_presente(self):
        src = _ui_src().lower()
        assert "aerotermica" in src
        assert "geotermica" in src
        assert "aria esterna" in src
        assert "scop" in src
        assert "freddo" in src
        assert "perforazioni" in src
        assert "trivellazione" in src
        assert "pavimento radiante" in src
        assert "sbrinament" in src
        assert "mandata" in src

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Baseline caldaia a gas" in src
        assert "Pompa di calore" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh699_csv" in src
        assert "pompa_calore_aerotermica_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh699_sensitivita" in src
        assert "Heatmap" in src
        assert "SCOP" in src
        assert "Prezzo elettricità" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st699_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W700 (25/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab699:")
        assert "mh699_calcola" in _helpers_src()
        assert "demo_calcoli" in _helpers_src()
        assert "import streamlit" not in _helpers_src()
        assert "tab699" in (_new_dir() / "w700_test.py")\
            .read_text(encoding="utf-8")

    def test_nessun_segreto_nei_file(self):
        for fn in ("w700_helpers.py", "w700_ui.py",
                   "w700_test.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            assert not re.search(
                r"(?i)(api[_-]?key|secret|password|passwd|token)"
                r"\s*=\s*[\"']",
                src), fn

    def test_nessun_riferimento_alle_tab_precedenti(self):
        src = _ui_src()
        tabs = set(re.findall(r"tab\d+", src))
        assert tabs == {"tab699"}, tabs

    def test_nessun_residuo_tab_precedente_in_helpers_ui(self):
        # Token vietati costruiti per parti, cosi' questo
        # stesso file non contiene i letterali vietati.
        prev = "69" + "8"
        vietati = ["mh" + prev, "tab" + prev, "st" + prev + "_"]
        for fn in ("w700_helpers.py", "w700_ui.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            for tok in vietati:
                assert tok not in src, (fn, tok)

    def test_topic_aerotermica_non_geotermica(self):
        # Topic corretto: il titolo parla di pompa
        # di calore aerotermica (aria esterna),
        # non di sonde geotermiche
        assert "aerotermica" in TITLE699.lower()
        assert "aria esterna" in TITLE699.lower()
