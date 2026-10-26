"""Test tab738 "🧂🔥 Sali fusi: il calore stoccato ridà elettricità a prezzo giusto?"

Nuova tab tab738 (accumulo termico a sali
fusi, w739). Business case deterministico
di un accumulo a calore sensibile in sale
nitrato fuso: capacita' termica da massa
e salto termico, energia per ciclo,
energie annue di scarica e di carica,
CAPEX di potenza e di energia, opex,
costo di carica, costi annui, ricavo,
netto, VAN, TIR, payback, LCOS, margine
sul prezzo di scarica, CO2 evitata e
verdetto.

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
potenza scarica 50 MW; massa sale 20000 t;
salto termico 250 K; rendimento scarica
0,40; rendimento carica 0,98; cicli annui
300; CAPEX potenza 800 EUR/kW; CAPEX
energia 30 EUR/kWh termici; opex fisso 20
EUR/kW/anno; opex variabile 2 EUR/MWh;
prezzo scarica 180 EUR/MWh; prezzo carica
55 EUR/MWh; WACC 0,07 (7 %); vita 25 anni;
tolleranza 0,10 (10 % del CAPEX); fattore
rete 0,35 kg/kWh.

- capacita_MWh_th = 2083.3333333333335
- energia_ciclo_MWh = 833.3333333333335
- energia_carica_ciclo_MWh = 2125.8503401360545
- energia_scaricata_MWh_anno = 250000.00000000006
- energia_carica_MWh_anno = 637755.1020408163
- capex_EUR = 102500000.0
- opex_EUR_anno = 1500000.0
- costo_carica_EUR_anno = 35076530.6122449
- costi_annui_EUR = 36576530.6122449
- ricavo_EUR_anno = 45000000.00000001
- netto_EUR_anno = 8423469.38775511
- van = -4336398.840321963
- tir = 6.5261846137235
- payback = 13
- lcos_EUR_MWh = 162.70612244897956
- margine_EUR_MWh = 17.293877551020444
- co2_evitata_t_anno = 87500.00000000001
- verdetto = 'MARGINALE'

Scomposizione: capacita' 20000 x 1000 x
1,5 x 250 / 3600000 = 2083.3333333333335
MWh termici; energia per ciclo 2083.3333333333335
x 0,40 = 833.3333333333335 MWh; energia di
carica per ciclo 2083.3333333333335 / 0,98 =
2125.8503401360545 MWh; energia scaricata
833.3333333333335 x 300 = 250000.00000000006
MWh/anno; energia di carica 2125.8503401360545
x 300 = 637755.1020408163 MWh/anno; CAPEX
50 x 1000 x 800 + 2083.3333333333335 x 1000 x
30 = 102500000.0 EUR; opex 50 x 1000 x 20 +
250000.00000000006 x 2 = 1500000.0 EUR/anno;
costo carica 637755.1020408163 x 55 =
35076530.6122449 EUR/anno; costi annui
1500000.0 + 35076530.6122449 = 36576530.6122449
EUR/anno; ricavo 250000.00000000006 x 180 =
45000000.00000001 EUR/anno; netto
45000000.00000001 - 36576530.6122449 =
8423469.38775511 EUR/anno; flussi: anno 0
-102500000.0, anni 1-25 netto 8423469.38775511
(piatti); VAN -102500000.0 + 8423469.38775511 x
11,653583178253722 (annuita' 25 anni al 7 %) =
-4336398.840321963 EUR; TIR
6.5261846137235 % (il tasso che azzera
il VAN dei flussi); payback 13 (il
cumulato supera lo zero al tredicesimo
anno: -102500000.0 + 13 x 8423469.38775511 =
7005013.038...); LCOS (102500000.0 / 25 +
36576530.6122449) / 250000.00000000006 =
162.70612244897956 EUR/MWh; margine 180 -
162.70612244897956 = 17.293877551020444
EUR/MWh; CO2 evitata (250000.00000000006 x
1000 x 0,35) / 1000 = 87500.00000000001
t/anno; verdetto MARGINALE perche' VAN < 0
ma |VAN| = 4.336.398,84 EUR <= 10 % del
CAPEX (10.250.000 EUR).
"""

import ast
import re
from pathlib import Path
import sys
import textwrap

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w739_helpers.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w739_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w739_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w739_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w739_helpers.py: {missing}")
    return out


_F = _load("mh738_num", "mh738_nneg", "mh738_pos",
           "mh738_int_pos", "mh738_frac_01",
           "mh738_frac_cf", "mh738_frac_toll",
           "mh738_deltat", "mh738_cicli",
           "mh738_capacita",
           "mh738_energia_ciclo",
           "mh738_energia_carica_ciclo",
           "mh738_energia_annua",
           "mh738_capex", "mh738_opex",
           "mh738_costo_carica",
           "mh738_ricavo", "mh738_netto",
           "mh738_flussi", "mh738_van",
           "mh738_tir", "mh738_payback",
           "mh738_lcos", "mh738_margine",
           "mh738_co2_evitata", "mh738_verdetto",
           "mh738_valida", "_mh738_neutro",
           "mh738_calcola", "mh738_csv",
           "mh738_demo", "demo_calcoli")

TITLE738 = ("🧂🔥 Sali fusi: il calore stoccato ridà elettricità a prezzo giusto?")

CAP_DEMO = 2083.3333333333335
ECICLO_DEMO = 833.3333333333335
CCICLO_DEMO = 2125.8503401360545
EANN_DEMO = 250000.00000000006
CANN_DEMO = 637755.1020408163
CAPEX_DEMO = 102500000.0
OPEX_DEMO = 1500000.0
CCOSTO_DEMO = 35076530.6122449
COSTI_DEMO = 36576530.6122449
RICAVO_DEMO = 45000000.00000001
NETTO_DEMO = 8423469.38775511
VAN_DEMO = -4336398.840321963
TIR_DEMO = 6.5261846137235
PAYBACK_DEMO = 13
LCOS_DEMO = 162.70612244897956
MARGINE_DEMO = 17.293877551020444
CO2_DEMO = 87500.00000000001
VERDETTO_DEMO = "MARGINALE"

_DEMO = {
    "potenza_scarica_MW": 50.0,
    "massa_sale_t": 20000.0,
    "deltaT_K": 250.0,
    "rend_scarica": 0.40,
    "rend_carica": 0.98,
    "cicli_anno": 300,
    "capex_potenza_EUR_per_kW": 800.0,
    "capex_energia_EUR_per_kWh_th": 30.0,
    "opex_fisso_EUR_per_kW_anno": 20.0,
    "opex_var_EUR_per_MWh": 2.0,
    "prezzo_scarica_EUR_per_MWh": 180.0,
    "prezzo_carica_EUR_per_MWh": 55.0,
    "wacc_frac": 0.07,
    "vita_anni": 25,
    "tolleranza_frac": 0.10,
    "fattore_rete_kg_per_kWh": 0.35,
}

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w739_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w739_ui.py").read_text(encoding="utf-8")


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh738_demo"]()
        d.update(kw)
        return _F["mh738_valida"](**d)

    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh738_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh738_num"]("500", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh738_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh738_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh738_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh738_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh738_pos"](0.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh738_int_pos"](2.5, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh738_int_pos"](25.0, "x") == 25

    def test_frac_01_rifiuta_zero_e_uno(self):
        with pytest.raises(ValueError):
            _F["mh738_frac_01"](0.0, "x")
        with pytest.raises(ValueError):
            _F["mh738_frac_01"](1.0, "x")

    def test_frac_cf_accetta_uno_rifiuta_zero_e_oltre(self):
        assert _F["mh738_frac_cf"](1.0, "x") == 1.0
        with pytest.raises(ValueError):
            _F["mh738_frac_cf"](0.0, "x")
        with pytest.raises(ValueError):
            _F["mh738_frac_cf"](1.01, "x")

    def test_frac_toll_accetta_zero_rifiuta_uno(self):
        assert _F["mh738_frac_toll"](0.0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh738_frac_toll"](1.0, "x")
        with pytest.raises(ValueError):
            _F["mh738_frac_toll"](-0.01, "x")

    def test_deltat_accetta_400_rifiuta_zero_e_oltre(self):
        assert _F["mh738_deltat"](400.0, "x") == 400.0
        with pytest.raises(ValueError):
            _F["mh738_deltat"](0.0, "x")
        with pytest.raises(ValueError):
            _F["mh738_deltat"](401.0, "x")

    def test_cicli_accetta_1_e_365_rifiuta_altri(self):
        assert _F["mh738_cicli"](1, "x") == 1
        assert _F["mh738_cicli"](365, "x") == 365
        with pytest.raises(ValueError):
            _F["mh738_cicli"](0, "x")
        with pytest.raises(ValueError):
            _F["mh738_cicli"](366, "x")
        with pytest.raises(ValueError):
            _F["mh738_cicli"](100.5, "x")

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_potenza_zero_e_negativa_non_valide(self):
        assert self._val(potenza_scarica_MW=0.0)["valido"] is False
        assert self._val(potenza_scarica_MW=-1.0)["valido"] is False

    def test_massa_zero_non_valida(self):
        assert self._val(massa_sale_t=0.0)["valido"] is False

    def test_deltat_non_validi(self):
        assert self._val(deltaT_K=0.0)["valido"] is False
        assert self._val(deltaT_K=401.0)["valido"] is False
        assert self._val(deltaT_K=400.0)["valido"] is True

    def test_rendimenti_non_validi(self):
        assert self._val(rend_scarica=0.0)["valido"] is False
        assert self._val(rend_scarica=1.01)["valido"] is False
        assert self._val(rend_carica=0.0)["valido"] is False
        assert self._val(rend_scarica=1.0)["valido"] is True
        assert self._val(rend_carica=1.0)["valido"] is True

    def test_cicli_non_validi(self):
        assert self._val(cicli_anno=0)["valido"] is False
        assert self._val(cicli_anno=366)["valido"] is False
        assert self._val(cicli_anno=300.5)["valido"] is False
        assert self._val(cicli_anno=365)["valido"] is True

    def test_negativi_non_validi(self):
        for k in ("capex_potenza_EUR_per_kW",
                  "capex_energia_EUR_per_kWh_th",
                  "opex_fisso_EUR_per_kW_anno",
                  "opex_var_EUR_per_MWh",
                  "prezzo_scarica_EUR_per_MWh",
                  "prezzo_carica_EUR_per_MWh",
                  "fattore_rete_kg_per_kWh"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_vita_zero_e_frazione_non_valide(self):
        assert self._val(vita_anni=0)["valido"] is False
        assert self._val(vita_anni=25.5)["valido"] is False

    def test_wacc_zero_uno_e_negativo_non_validi(self):
        assert self._val(wacc_frac=0.0)["valido"] is False
        assert self._val(wacc_frac=1.0)["valido"] is False
        assert self._val(wacc_frac=-0.01)["valido"] is False
        assert self._val(wacc_frac=0.07)["valido"] is True

    def test_tolleranza_uno_non_valida_zero_valida(self):
        assert self._val(tolleranza_frac=1.0)["valido"] is False
        assert self._val(tolleranza_frac=0.0)["valido"] is True

    def test_nan_non_valido(self):
        assert self._val(massa_sale_t=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(massa_sale_t=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(vita_anni=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(massa_sale_t="500")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(prezzo_scarica_EUR_per_MWh=0.0)["valido"] is True
        assert self._val(capex_potenza_EUR_per_kW=0.0)["valido"] is True
        assert self._val(fattore_rete_kg_per_kWh=0.0)["valido"] is True
        assert self._val(tolleranza_frac=0.0)["valido"] is True


class TestFunzioni:
    def test_capacita_demo(self):
        assert _F["mh738_capacita"](
            20000.0, 250.0) == pytest.approx(
            CAP_DEMO, rel=REL)

    def test_capacita_formula_letterale(self):
        assert _F["mh738_capacita"](
            1000.0, 100.0) == pytest.approx(
            1000.0 * 1000.0 * 1.5 * 100.0 / 3600000.0, rel=REL)

    def test_capacita_rifiuta_deltat_zero(self):
        with pytest.raises(ValueError):
            _F["mh738_capacita"](20000.0, 0.0)

    def test_energia_ciclo_demo(self):
        assert _F["mh738_energia_ciclo"](
            CAP_DEMO, 0.40) == pytest.approx(
            ECICLO_DEMO, rel=REL)

    def test_energia_carica_ciclo_demo(self):
        assert _F["mh738_energia_carica_ciclo"](
            CAP_DEMO, 0.98) == pytest.approx(
            CCICLO_DEMO, rel=REL)

    def test_energia_carica_rifiuta_rendimento_zero(self):
        with pytest.raises(ValueError):
            _F["mh738_energia_carica_ciclo"](CAP_DEMO, 0.0)

    def test_energia_annua_demo(self):
        assert _F["mh738_energia_annua"](
            ECICLO_DEMO, 300) == pytest.approx(
            EANN_DEMO, rel=REL)

    def test_capex_demo(self):
        assert _F["mh738_capex"](
            50.0, 800.0, CAP_DEMO, 30.0) == pytest.approx(
            CAPEX_DEMO, rel=REL)

    def test_capex_solo_energia(self):
        assert _F["mh738_capex"](
            0.0, 800.0, CAP_DEMO, 30.0) == pytest.approx(
            CAP_DEMO * 1000.0 * 30.0, rel=REL)

    def test_opex_demo(self):
        assert _F["mh738_opex"](
            50.0, 20.0, EANN_DEMO, 2.0) == pytest.approx(
            OPEX_DEMO, rel=REL)

    def test_costo_carica_demo(self):
        assert _F["mh738_costo_carica"](
            CANN_DEMO, 55.0) == pytest.approx(
            CCOSTO_DEMO, rel=REL)

    def test_ricavo_demo(self):
        assert _F["mh738_ricavo"](
            EANN_DEMO, 180.0) == pytest.approx(
            RICAVO_DEMO, rel=REL)

    def test_netto_demo(self):
        assert _F["mh738_netto"](
            RICAVO_DEMO, COSTI_DEMO) == pytest.approx(
            NETTO_DEMO, rel=REL)

    def test_netto_puo_essere_negativo(self):
        assert _F["mh738_netto"](
            1000.0, COSTI_DEMO) == pytest.approx(
            -36575530.6122449, rel=REL)

    def test_flussi_demo(self):
        flussi = _F["mh738_flussi"](CAPEX_DEMO, NETTO_DEMO, 25)
        assert len(flussi) == 26
        assert flussi[0] == pytest.approx(-CAPEX_DEMO, rel=REL)
        assert all(f == pytest.approx(NETTO_DEMO, rel=REL)
                   for f in flussi[1:])

    def test_van_demo(self):
        flussi = _F["mh738_flussi"](CAPEX_DEMO, NETTO_DEMO, 25)
        assert abs(_F["mh738_van"](
            flussi, 0.07) - VAN_DEMO) <= 1.0

    def test_van_tasso_zero(self):
        flussi = _F["mh738_flussi"](CAPEX_DEMO, NETTO_DEMO, 25)
        atteso = -CAPEX_DEMO + NETTO_DEMO * 25
        assert _F["mh738_van"](
            flussi, 0.0) == pytest.approx(atteso, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh738_van"]([100.0, 100.0], -0.01)

    def test_tir_none_flussi_tutti_negativi(self):
        flussi = _F["mh738_flussi"](CAPEX_DEMO, -1000.0, 25)
        assert _F["mh738_tir"](flussi) is None

    def test_tir_none_tutti_flussi_non_negativi(self):
        assert _F["mh738_tir"](
            [0.0] + [NETTO_DEMO] * 25) is None

    def test_tir_esiste_caso_semplice_100_120(self):
        assert _F["mh738_tir"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_caso_semplice_1000_500_500_zero(self):
        assert abs(_F["mh738_tir"](
            [-1000.0, 500.0, 500.0])) <= 1e-9

    def test_tir_demo(self):
        flussi = _F["mh738_flussi"](CAPEX_DEMO, NETTO_DEMO, 25)
        tir = _F["mh738_tir"](flussi)
        assert tir is not None
        assert tir * 100.0 == pytest.approx(TIR_DEMO, rel=1e-9)

    def test_payback_demo(self):
        flussi = _F["mh738_flussi"](CAPEX_DEMO, NETTO_DEMO, 25)
        assert _F["mh738_payback"](flussi) == PAYBACK_DEMO

    def test_payback_semplice_due(self):
        assert _F["mh738_payback"](
            [-1000.0, 500.0, 500.0, 500.0]) == 2

    def test_payback_zero_se_cumulato_anno_zero_non_negativo(self):
        assert _F["mh738_payback"](
            [0.0, 100.0]) == 0

    def test_payback_none_se_mai(self):
        assert _F["mh738_payback"](
            [-10000000000.0] + [NETTO_DEMO] * 25) is None

    def test_lcos_demo(self):
        assert _F["mh738_lcos"](
            CAPEX_DEMO, 25, COSTI_DEMO,
            EANN_DEMO) == pytest.approx(LCOS_DEMO, rel=REL)

    def test_lcos_none_se_energia_zero(self):
        assert _F["mh738_lcos"](
            102500000.0, 25, COSTI_DEMO, 0.0) is None

    def test_lcos_formula_indipendente(self):
        assert _F["mh738_lcos"](
            120000.0, 10, 5000.0,
            1000.0) == pytest.approx(
            (12000.0 + 5000.0) / 1000.0, rel=REL)

    def test_margine_demo(self):
        assert _F["mh738_margine"](
            180.0, LCOS_DEMO) == pytest.approx(
            MARGINE_DEMO, rel=REL)

    def test_margine_none_se_lcos_none(self):
        assert _F["mh738_margine"](100.0, None) is None

    def test_co2_demo(self):
        assert _F["mh738_co2_evitata"](
            EANN_DEMO, 0.35) == pytest.approx(
            CO2_DEMO, rel=REL)

    def test_co2_fattore_zero(self):
        assert _F["mh738_co2_evitata"](
            EANN_DEMO, 0.0) == pytest.approx(0.0, abs=1e-9)

    def test_verdetto_demo(self):
        assert _F["mh738_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10, EANN_DEMO,
            NETTO_DEMO) == VERDETTO_DEMO

    def test_verdetto_conviente_van_positivo(self):
        assert _F["mh738_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, EANN_DEMO,
            NETTO_DEMO) == "CONVIENTE"

    def test_verdetto_van_zero_marginale(self):
        assert _F["mh738_verdetto"](
            0.0, CAPEX_DEMO, 0.10, EANN_DEMO,
            NETTO_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh738_verdetto"](
            -0.10 * CAPEX_DEMO, CAPEX_DEMO, 0.10,
            EANN_DEMO, NETTO_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_oltre_limite(self):
        assert _F["mh738_verdetto"](
            -0.10 * CAPEX_DEMO - 1.0, CAPEX_DEMO, 0.10,
            EANN_DEMO, NETTO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_netto_negativo_non_e_non_calcolabile(self):
        assert _F["mh738_verdetto"](
            -1000.0, CAPEX_DEMO, 0.10, EANN_DEMO,
            -5000.0) == "MARGINALE"

    def test_verdetto_non_calcolabile_energia_zero(self):
        assert _F["mh738_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0,
            NETTO_DEMO) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_netto_nan(self):
        assert _F["mh738_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, EANN_DEMO,
            float("nan")) == "NON_CALCOLABILE"


class TestDemo:
    def _bc(self, **kw):
        d = _F["mh738_demo"]()
        d.update(kw)
        return _F["mh738_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["capacita_MWh_th"] == pytest.approx(
            CAP_DEMO, rel=REL)
        assert c["energia_ciclo_MWh"] == pytest.approx(
            ECICLO_DEMO, rel=REL)
        assert c["energia_carica_ciclo_MWh"] == pytest.approx(
            CCICLO_DEMO, rel=REL)
        assert c["energia_scaricata_MWh_anno"] == pytest.approx(
            EANN_DEMO, rel=REL)
        assert c["energia_carica_MWh_anno"] == pytest.approx(
            CANN_DEMO, rel=REL)
        assert c["capex_EUR"] == pytest.approx(
            CAPEX_DEMO, rel=REL)
        assert c["opex_EUR_anno"] == pytest.approx(
            OPEX_DEMO, rel=REL)
        assert c["costo_carica_EUR_anno"] == pytest.approx(
            CCOSTO_DEMO, rel=REL)
        assert c["costi_annui_EUR"] == pytest.approx(
            COSTI_DEMO, rel=REL)
        assert c["ricavo_EUR_anno"] == pytest.approx(
            RICAVO_DEMO, rel=REL)
        assert c["netto_EUR_anno"] == pytest.approx(
            NETTO_DEMO, rel=REL)
        assert abs(c["van"] - VAN_DEMO) <= 1.0
        assert abs(c["tir"] - TIR_DEMO) <= 0.01
        assert c["payback"] == PAYBACK_DEMO
        assert c["lcos_EUR_MWh"] == pytest.approx(
            LCOS_DEMO, rel=REL)
        assert c["margine_EUR_MWh"] == pytest.approx(
            MARGINE_DEMO, rel=REL)
        assert c["co2_evitata_t_anno"] == pytest.approx(
            CO2_DEMO, rel=REL)
        assert c["verdetto"] == VERDETTO_DEMO
        assert len(c["flussi"]) == 26

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()["van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()["lcos_EUR_MWh"] == \
            _F["demo_calcoli"]()["lcos_EUR_MWh"]

    def test_demo_defaults_contro_costanti_test(self):
        d = _F["mh738_demo"]()
        for k, v in _DEMO.items():
            assert d[k] == v, k
        assert len(d) == 16

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("capacita_MWh_th",
                       "energia_ciclo_MWh",
                       "energia_carica_ciclo_MWh",
                       "energia_scaricata_MWh_anno",
                       "energia_carica_MWh_anno",
                       "capex_EUR",
                       "opex_EUR_anno",
                       "costo_carica_EUR_anno",
                       "costi_annui_EUR",
                       "ricavo_EUR_anno",
                       "netto_EUR_anno",
                       "van",
                       "tir",
                       "lcos_EUR_MWh",
                       "margine_EUR_MWh",
                       "co2_evitata_t_anno"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 13" in doc
        assert "verdetto = 'MARGINALE'" in doc

    def test_prezzo_al_lcos_margine_zero_van_negativo(self):
        # Prezzo di scarica = LCOS: margine 0 per
        # costruzione, ma VAN negativa (il LCOS
        # ripartisce il CAPEX in quote lineari,
        # il VAN lo attualizza): NON_CONVIENTE.
        n = self._bc(prezzo_scarica_EUR_per_MWh=LCOS_DEMO)
        assert n["valid"] is True
        assert n["margine_EUR_MWh"] == pytest.approx(
            0.0, abs=1e-9)
        assert n["van"] < 0.0
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_prezzo_scarica_220_conviente(self):
        # Prezzo scarica 220 EUR/MWh: netto
        # 18.423.469 EUR/anno, VAN circa
        # +112.199.432,94 EUR -> CONVIENTE.
        n = self._bc(prezzo_scarica_EUR_per_MWh=220.0)
        assert n["valid"] is True
        assert n["verdetto"] == "CONVIENTE"
        assert n["van"] > 0.0

    def test_prezzo_scarica_150_non_conviente(self):
        # Prezzo scarica 150 EUR/MWh: netto
        # 923.469 EUR/anno, VAN circa
        # -91.738.272,68 EUR, oltre la tolleranza
        # 10.250.000 EUR -> NON_CONVIENTE.
        n = self._bc(prezzo_scarica_EUR_per_MWh=150.0)
        assert n["valid"] is True
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["van"] < -0.10 * CAPEX_DEMO

    def test_prezzo_carica_40_conviente(self):
        # Prezzo carica 40 EUR/MWh: netto
        # 17.989.796 EUR/anno, VAN circa
        # +107.145.583,09 EUR -> CONVIENTE.
        n = self._bc(prezzo_carica_EUR_per_MWh=40.0)
        assert n["valid"] is True
        assert n["verdetto"] == "CONVIENTE"
        assert n["van"] > 0.0

    def test_prezzo_scarica_zero_non_conviente(self):
        # Prezzo scarica 0: ricavo zero, netto
        # negativo pari a -costi annui, VAN
        # negativa oltre tolleranza ->
        # NON_CONVIENTE.
        n = self._bc(prezzo_scarica_EUR_per_MWh=0.0)
        assert n["valid"] is True
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_capex_zero_tir_none_payback_zero(self):
        # CAPEX zero (potenza ed energia a zero)
        # e prezzi demo: tutti i flussi >= 0 ->
        # TIR None, payback 0, VAN positiva ->
        # CONVIENTE.
        n = self._bc(capex_potenza_EUR_per_kW=0.0,
                     capex_energia_EUR_per_kWh_th=0.0)
        assert n["valid"] is True
        assert n["capex_EUR"] == pytest.approx(0.0, abs=1e-9)
        assert n["tir"] is None
        assert n["payback"] == 0
        assert n["verdetto"] == "CONVIENTE"

    def test_potenza_zero_neutro(self):
        n = self._bc(potenza_scarica_MW=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["lcos_EUR_MWh"] is None

    def test_massa_zero_neutro(self):
        n = self._bc(massa_sale_t=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_deltat_zero_e_oltre_400_neutri(self):
        assert self._bc(deltaT_K=0.0)["verdetto"] == "NON_CALCOLABILE"
        assert self._bc(deltaT_K=401.0)["verdetto"] == "NON_CALCOLABILE"

    def test_cicli_non_validi_neutri(self):
        assert self._bc(cicli_anno=0)["verdetto"] == "NON_CALCOLABILE"
        assert self._bc(cicli_anno=366)["verdetto"] == "NON_CALCOLABILE"
        assert self._bc(cicli_anno=300.5)["verdetto"] == "NON_CALCOLABILE"

    def test_rendimenti_zero_neutri(self):
        assert self._bc(rend_scarica=0.0)["verdetto"] == "NON_CALCOLABILE"
        assert self._bc(rend_carica=0.0)["verdetto"] == "NON_CALCOLABILE"

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_zero_uno_e_negativo_neutri(self):
        assert self._bc(wacc_frac=0.0)["verdetto"] == "NON_CALCOLABILE"
        assert self._bc(wacc_frac=1.0)["verdetto"] == "NON_CALCOLABILE"
        assert self._bc(wacc_frac=-0.01)["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_uno_neutro(self):
        n = self._bc(tolleranza_frac=1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(massa_sale_t=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["netto_EUR_anno"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(massa_sale_t=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(vita_anni=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_stringa_neutro(self):
        n = self._bc(massa_sale_t="500")
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_capex_negativo_neutro(self):
        n = self._bc(capex_potenza_EUR_per_kW=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_fattore_rete_zero_valido_co2_zero(self):
        n = self._bc(fattore_rete_kg_per_kWh=0.0)
        assert n["valid"] is True
        assert n["co2_evitata_t_anno"] == pytest.approx(
            0.0, abs=1e-9)

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh738_neutro"]()
        assert n["valid"] is False
        assert n["errore"] == ""
        assert list(n["df_flussi"].columns) == ["Anno",
                                               "Flusso (EUR/anno)",
                                               "Cumulato (EUR)"]
        assert len(n["df_flussi"]) == 0
        assert list(n["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(n["df_tabella"]) == 0
        assert n["flussi"] == []
        assert n["tir"] is None
        assert n["payback"] is None
        assert n["lcos_EUR_MWh"] is None
        assert n["margine_EUR_MWh"] is None
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh738_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "potenza_scarica_MW", "massa_sale_t",
                       "deltaT_K", "rend_scarica",
                       "rend_carica", "cicli_anno",
                       "capex_potenza_EUR_per_kW",
                       "capex_energia_EUR_per_kWh_th",
                       "opex_fisso_EUR_per_kW_anno",
                       "opex_var_EUR_per_MWh",
                       "prezzo_scarica_EUR_per_MWh",
                       "prezzo_carica_EUR_per_MWh",
                       "wacc_frac", "vita_anni",
                       "tolleranza_frac",
                       "fattore_rete_kg_per_kWh",
                       "capacita_MWh_th",
                       "energia_ciclo_MWh",
                       "energia_carica_ciclo_MWh",
                       "energia_scaricata_MWh_anno",
                       "energia_carica_MWh_anno",
                       "capex_EUR", "opex_EUR_anno",
                       "costo_carica_EUR_anno",
                       "costi_annui_EUR",
                       "ricavo_EUR_anno",
                       "netto_EUR_anno", "flussi", "van",
                       "tir", "payback", "lcos_EUR_MWh",
                       "margine_EUR_MWh",
                       "co2_evitata_t_anno", "verdetto",
                       "df_flussi", "df_tabella"):
            assert chiave in n, chiave
        assert n["errore"] == "errore di prova"
        assert n["tir"] is None

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert b["valid"] is True
        assert list(b["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(b["df_tabella"]) == 34
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Capacita' termica (MWh termici)" in voci
        assert "Energia per ciclo (MWh)" in voci
        assert "Energia scaricata (MWh/anno)" in voci
        assert "Energia carica (MWh/anno)" in voci
        assert "CAPEX (EUR)" in voci
        assert "Opex (EUR/anno)" in voci
        assert "Costo carica (EUR/anno)" in voci
        assert "Costi annui (EUR/anno)" in voci
        assert "Ricavo (EUR/anno)" in voci
        assert "VAN (EUR)" in voci
        assert "LCOS (EUR/MWh)" in voci
        assert "Margine (EUR/MWh)" in voci
        assert "CO2 evitata (t/anno)" in voci
        assert "Verdetto" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (EUR/anno)",
                                               "Cumulato (EUR)"]
        assert len(b["df_flussi"]) == 26
        assert b["df_flussi"]["Flusso (EUR/anno)"].iloc[0] == \
            pytest.approx(-CAPEX_DEMO, rel=REL)
        assert b["df_flussi"]["Flusso (EUR/anno)"].iloc[1] == \
            pytest.approx(NETTO_DEMO, rel=REL)


class TestCsv:
    def _ing(self):
        return _F["mh738_demo"]()

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh738_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") == 35

    def test_csv_contiene_verdetti_e_costi(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh738_csv"](bc, self._ing())
        assert "verdetto;MARGINALE" in txt
        assert "capex_EUR" in txt
        assert "van_eur" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "lcos_EUR_MWh" in txt
        assert "margine_EUR_MWh" in txt
        assert "co2_evitata_t_anno" in txt
        assert "potenza_scarica_MW" in txt
        assert "energia_scaricata_MWh_anno" in txt
        assert "costi_annui_EUR" in txt
        assert "capacita_MWh_th" in txt
        assert "costo_carica_EUR_anno" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh738_csv"](bc, self._ing())
        assert f"netto_EUR_anno;{bc['netto_EUR_anno']}" in txt
        assert f"energia_scaricata_MWh_anno;{bc['energia_scaricata_MWh_anno']}" in txt
        assert "potenza_scarica_MW;50.0" in txt
        assert "capex_potenza_EUR_per_kW;800.0" in txt
        assert f"lcos_EUR_MWh;{bc['lcos_EUR_MWh']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def738["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def738\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 16, ui_keys
        demo_keys = set(_F["mh738_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh738_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh738_demo():")
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
        ui_keys = set(re.findall(r'_def738\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W739 (26/10/2026) - tab738' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh738_num", "mh738_nneg", "mh738_pos",
                     "mh738_int_pos", "mh738_frac_01",
                     "mh738_frac_cf", "mh738_frac_toll",
                     "mh738_deltat", "mh738_cicli",
                     "mh738_capacita",
                     "mh738_energia_ciclo",
                     "mh738_energia_carica_ciclo",
                     "mh738_energia_annua",
                     "mh738_capex", "mh738_opex",
                     "mh738_costo_carica",
                     "mh738_ricavo", "mh738_netto",
                     "mh738_flussi", "mh738_van",
                     "mh738_tir", "mh738_payback",
                     "mh738_lcos", "mh738_margine",
                     "mh738_co2_evitata", "mh738_verdetto",
                     "mh738_valida", "_mh738_neutro",
                     "mh738_calcola", "mh738_csv",
                     "mh738_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_nessun_residuo_precedente(self):
        # Token del ciclo precedente costruiti per
        # concatenazione, cosi' questo file non li
        # contiene come letterali.
        mh_old = "mh" + "737"
        st_old = "st" + "737"
        tab_old = "tab" + "737"
        w_old = "W" + "738"
        assert mh_old not in _helpers_src()
        assert mh_old not in _ui_src()
        assert st_old not in _ui_src()
        assert tab_old not in _ui_src()
        assert w_old not in _helpers_src()
        assert w_old not in _ui_src()
        assert "mh738" in _helpers_src()
        assert "st738" in _ui_src()

    def test_helpers_parse_ast(self):
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w739_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE738) == 1

    def test_blocco_with_tab738(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab738:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE738

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st738_[A-Za-z0-9_]+)"', _ui_src())
        assert len(keys) == 19, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st738_") for k in keys)

    def test_chiavi_st_input_presenti(self):
        keys = re.findall(r'key="(st738_[A-Za-z0-9_]+)"', _ui_src())
        attese = ["st738_potenza", "st738_massa",
                  "st738_deltaT", "st738_rend_scarica",
                  "st738_rend_carica", "st738_cicli",
                  "st738_prezzo_carica",
                  "st738_prezzo_scarica",
                  "st738_capex_potenza",
                  "st738_capex_energia",
                  "st738_opex_fisso", "st738_opex_var",
                  "st738_fattore_rete", "st738_vita",
                  "st738_wacc", "st738_tolleranza",
                  "st738_calcola"]
        assert len(attese) == 17
        for k in attese:
            assert k in keys, k

    def test_chiavi_st_niente_fstring_dinamiche(self):
        src = _ui_src()
        assert 'key=f"' not in src
        assert "key=f'" not in src

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg738" in src
        assert "NON_CALCOLABILE" in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg738") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg738")
        assert g < src.index("st.bar_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "LCOS (EUR/MWh)" in src
        assert "Margine (EUR/MWh)" in src
        assert "VAN (EUR)" in src
        assert "Payback (anni)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON_CALCOLABILE"):
            assert v in src

    def test_distinzioni_presenti(self):
        src = _ui_src()
        assert "CSP" in src
        assert "ATES" in src
        assert "PCM" in src
        assert "sabbia" in src
        assert "sali fusi" in src

    def test_distinzioni_in_header_helpers(self):
        src = _helpers_src()
        assert "CSP" in src
        assert "ATES" in src
        assert "PCM" in src
        assert "sabbia" in src
        assert "sali fusi" in src

    def test_nota_didattica_presente(self):
        src = _ui_src()
        assert "NOTA DIDATTICA" in src
        assert "250.000" in src
        assert "87.500" in src

    def test_grafico_bar_chart_presente(self):
        src = _ui_src()
        assert "st.bar_chart" in src
        assert "_dati738" in src
        assert '"EUR/MWh"' in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh738_csv" in src
        assert "sali_fusi.csv" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st738_show_flussi" in src
        assert "st.checkbox" in src

    def test_niente_nome(self):
        assert "Emanuele" not in _helpers_src()
        assert "Emanuele" not in _ui_src()

    def test_ancora_helper_presente(self):
        assert "# W739 (26/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab738:")
