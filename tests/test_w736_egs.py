"""Test tab736 "🌡️🌋 Geotermia avanzata (EGS): il calore profondo diventa elettricità?"

Nuova tab tab736 (impianto geotermico
avanzato EGS, w737).
Business case deterministico di un
impianto EGS (rocce calde secche
stimolate, pozzi di iniezione e
produzione, fluido geotermico in
circuito chiuso, turbina ORC/binaria):
energia da potenza e fattore di
capacita', CAPEX, costi annui, ricavo,
netto, VAN, TIR, payback, LCOE, margine
sul prezzo, CO2 evitata e verdetto.

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
potenza 20 MW; fattore capacita' 0,90;
CAPEX 9000 EUR/kW; opex fisso 150
EUR/kW/anno; opex variabile 8 EUR/MWh;
prezzo elettricita' 110 EUR/MWh; WACC
0,07 (7 %); vita 30 anni; tolleranza
0,10 (10 % del CAPEX); fattore rete
0,35 kg/kWh.

- energia_MWh_anno = 157680.0
- capex_EUR = 180000000.0
- costi_annui_EUR = 4261440.0
- ricavo_EUR_anno = 17344800.0
- netto_EUR_anno = 13083360.0
- van = -17648046.941366874
- tir = 6.004684858347045
- payback = 14
- lcoe_EUR_MWh = 65.07762557077625
- margine_EUR_MWh = 44.92237442922375
- co2_evitata_t_anno = 55188.0
- verdetto = 'MARGINALE'

Scomposizione: energia 20 x 8760 x
0,90 = 157.680 MWh/anno; CAPEX 20 x
1000 x 9000 = 180.000.000 EUR; costi
annui 20 x 1000 x 150 + 157.680 x 8 =
4.261.440 EUR/anno; ricavo 157.680 x
110 = 17.344.800 EUR/anno; netto
17.344.800 - 4.261.440 = 13.083.360
EUR/anno; flussi: anno 0 -180.000.000,
anni 1-30 netto 13.083.360 (piatti);
VAN -180.000.000 + 13.083.360 x
12,409041 (annuita' 30 anni al 7 %) =
-17648046.941366874 EUR; TIR
6.004684858347045 % (il tasso che azzera
il VAN dei flussi); payback 14 (il
cumulato supera lo zero al quattordicesimo
anno: -180.000.000 + 14 x 13.083.360 =
3.167.040); LCOE (180.000.000 / 30 +
4.261.440) / 157.680 =
65.07762557077625 EUR/MWh; margine 110 -
65.07762557077625 = 44.92237442922375
EUR/MWh; CO2 evitata (157.680 x 1000 x
0,35) / 1000 = 55188.0 t/anno;
verdetto MARGINALE perche' VAN < 0 ma
|VAN| = 17.648.046,94 EUR <= 10 % del
CAPEX (18.000.000 EUR).
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
    if (p / "w737_helpers.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w737_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w737_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w737_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w737_helpers.py: {missing}")
    return out


_F = _load("mh736_num", "mh736_nneg", "mh736_pos",
           "mh736_int_pos", "mh736_frac_01",
           "mh736_frac_cf", "mh736_frac_toll",
           "mh736_energia", "mh736_capex",
           "mh736_costi", "mh736_ricavo",
           "mh736_netto", "mh736_flussi",
           "mh736_van", "mh736_tir", "mh736_payback",
           "mh736_lcoe", "mh736_margine",
           "mh736_co2_evitata", "mh736_verdetto",
           "mh736_valida", "_mh736_neutro",
           "mh736_calcola", "mh736_csv",
           "mh736_demo", "demo_calcoli")

TITLE736 = ("🌡️🌋 Geotermia avanzata (EGS): il calore profondo "
            "diventa elettricità?")

ENERGIA_DEMO = 157680.0
CAPEX_DEMO = 180000000.0
COSTI_DEMO = 4261440.0
RICAVO_DEMO = 17344800.0
NETTO_DEMO = 13083360.0
VAN_DEMO = -17648046.941366874
TIR_DEMO = 6.004684858347045
PAYBACK_DEMO = 14
LCOE_DEMO = 65.07762557077625
MARGINE_DEMO = 44.92237442922375
CO2_DEMO = 55188.0
VERDETTO_DEMO = "MARGINALE"

_DEMO = {
    "potenza_MW": 20.0,
    "fattore_capacita": 0.90,
    "capex_EUR_per_kW": 9000.0,
    "opex_fisso_EUR_per_kW_anno": 150.0,
    "opex_var_EUR_per_MWh": 8.0,
    "prezzo_el_EUR_per_MWh": 110.0,
    "wacc_frac": 0.07,
    "vita_anni": 30,
    "tolleranza_frac": 0.10,
    "fattore_rete_kg_per_kWh": 0.35,
}

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w737_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w737_ui.py").read_text(encoding="utf-8")


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh736_demo"]()
        d.update(kw)
        return _F["mh736_valida"](**d)

    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh736_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh736_num"]("500", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh736_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh736_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh736_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh736_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh736_pos"](0.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh736_int_pos"](2.5, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh736_int_pos"](30.0, "x") == 30

    def test_frac_01_rifiuta_zero_e_uno(self):
        with pytest.raises(ValueError):
            _F["mh736_frac_01"](0.0, "x")
        with pytest.raises(ValueError):
            _F["mh736_frac_01"](1.0, "x")

    def test_frac_cf_accetta_uno_rifiuta_zero_e_oltre(self):
        assert _F["mh736_frac_cf"](1.0, "x") == 1.0
        with pytest.raises(ValueError):
            _F["mh736_frac_cf"](0.0, "x")
        with pytest.raises(ValueError):
            _F["mh736_frac_cf"](1.01, "x")

    def test_frac_toll_accetta_zero_rifiuta_uno(self):
        assert _F["mh736_frac_toll"](0.0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh736_frac_toll"](1.0, "x")
        with pytest.raises(ValueError):
            _F["mh736_frac_toll"](-0.01, "x")

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_potenza_zero_e_negativa_non_valide(self):
        assert self._val(potenza_MW=0.0)["valido"] is False
        assert self._val(potenza_MW=-1.0)["valido"] is False

    def test_cf_zero_e_oltre_uno_non_validi_uno_valido(self):
        assert self._val(fattore_capacita=0.0)["valido"] is False
        assert self._val(fattore_capacita=1.01)["valido"] is False
        assert self._val(fattore_capacita=1.0)["valido"] is True

    def test_negativi_non_validi(self):
        for k in ("capex_EUR_per_kW",
                  "opex_fisso_EUR_per_kW_anno",
                  "opex_var_EUR_per_MWh",
                  "prezzo_el_EUR_per_MWh",
                  "fattore_rete_kg_per_kWh"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_vita_zero_e_frazione_non_valide(self):
        assert self._val(vita_anni=0)["valido"] is False
        assert self._val(vita_anni=30.5)["valido"] is False

    def test_wacc_zero_uno_e_negativo_non_validi(self):
        assert self._val(wacc_frac=0.0)["valido"] is False
        assert self._val(wacc_frac=1.0)["valido"] is False
        assert self._val(wacc_frac=-0.01)["valido"] is False
        assert self._val(wacc_frac=0.07)["valido"] is True

    def test_tolleranza_uno_non_valida_zero_valida(self):
        assert self._val(tolleranza_frac=1.0)["valido"] is False
        assert self._val(tolleranza_frac=0.0)["valido"] is True

    def test_nan_non_valido(self):
        assert self._val(potenza_MW=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(potenza_MW=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(vita_anni=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(potenza_MW="500")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(prezzo_el_EUR_per_MWh=0.0)["valido"] is True
        assert self._val(capex_EUR_per_kW=0.0)["valido"] is True
        assert self._val(fattore_rete_kg_per_kWh=0.0)["valido"] is True
        assert self._val(tolleranza_frac=0.0)["valido"] is True


class TestFunzioni:
    def test_energia_demo(self):
        assert _F["mh736_energia"](
            20.0, 0.90) == pytest.approx(
            ENERGIA_DEMO, rel=REL)

    def test_energia_formula_letterale(self):
        assert _F["mh736_energia"](
            100.0, 1.0) == pytest.approx(876000.0, rel=REL)

    def test_energia_rifiuta_cf_zero(self):
        with pytest.raises(ValueError):
            _F["mh736_energia"](20.0, 0.0)

    def test_energia_rifiuta_cf_oltre_uno(self):
        with pytest.raises(ValueError):
            _F["mh736_energia"](20.0, 1.01)

    def test_capex_demo(self):
        assert _F["mh736_capex"](
            20.0, 9000.0) == pytest.approx(
            CAPEX_DEMO, rel=REL)

    def test_capex_formula_indipendente(self):
        assert _F["mh736_capex"](
            20.0, 9000.0) == pytest.approx(
            180000000.0, rel=REL)

    def test_costi_demo(self):
        assert _F["mh736_costi"](
            20.0, 150.0, ENERGIA_DEMO, 8.0) == pytest.approx(
            COSTI_DEMO, rel=REL)

    def test_costi_solo_fisso(self):
        assert _F["mh736_costi"](
            20.0, 150.0, ENERGIA_DEMO, 0.0) == pytest.approx(
            3000000.0, rel=REL)

    def test_ricavo_demo(self):
        assert _F["mh736_ricavo"](
            ENERGIA_DEMO, 110.0) == pytest.approx(
            RICAVO_DEMO, rel=REL)

    def test_netto_demo(self):
        assert _F["mh736_netto"](
            RICAVO_DEMO, COSTI_DEMO) == pytest.approx(
            NETTO_DEMO, rel=REL)

    def test_netto_puo_essere_negativo(self):
        assert _F["mh736_netto"](
            1000.0, COSTI_DEMO) == pytest.approx(
            -4260440.0, rel=REL)

    def test_flussi_demo(self):
        flussi = _F["mh736_flussi"](CAPEX_DEMO, NETTO_DEMO, 30)
        assert len(flussi) == 31
        assert flussi[0] == pytest.approx(-CAPEX_DEMO, rel=REL)
        assert all(f == pytest.approx(NETTO_DEMO, rel=REL)
                   for f in flussi[1:])

    def test_van_demo(self):
        flussi = _F["mh736_flussi"](CAPEX_DEMO, NETTO_DEMO, 30)
        assert abs(_F["mh736_van"](
            flussi, 0.07) - VAN_DEMO) <= 1.0

    def test_van_tasso_zero(self):
        flussi = _F["mh736_flussi"](CAPEX_DEMO, NETTO_DEMO, 30)
        atteso = -CAPEX_DEMO + NETTO_DEMO * 30
        assert _F["mh736_van"](
            flussi, 0.0) == pytest.approx(atteso, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh736_van"]([100.0, 100.0], -0.01)

    def test_tir_none_flussi_tutti_negativi(self):
        flussi = _F["mh736_flussi"](CAPEX_DEMO, -1000.0, 30)
        assert _F["mh736_tir"](flussi) is None

    def test_tir_none_tutti_flussi_non_negativi(self):
        assert _F["mh736_tir"](
            [0.0] + [NETTO_DEMO] * 30) is None

    def test_tir_none_nessun_cambio_segno_negativo(self):
        assert _F["mh736_tir"](
            [-1000.0] + [-100.0] * 10) is None

    def test_tir_esiste_caso_semplice_100_120(self):
        assert _F["mh736_tir"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_caso_semplice_1000_500_500_zero(self):
        assert abs(_F["mh736_tir"](
            [-1000.0, 500.0, 500.0])) <= 1e-9

    def test_tir_demo(self):
        flussi = _F["mh736_flussi"](CAPEX_DEMO, NETTO_DEMO, 30)
        tir = _F["mh736_tir"](flussi)
        assert tir is not None
        assert tir * 100.0 == pytest.approx(TIR_DEMO, rel=1e-9)

    def test_payback_demo(self):
        flussi = _F["mh736_flussi"](CAPEX_DEMO, NETTO_DEMO, 30)
        assert _F["mh736_payback"](flussi) == PAYBACK_DEMO

    def test_payback_semplice_due(self):
        assert _F["mh736_payback"](
            [-1000.0, 500.0, 500.0, 500.0]) == 2

    def test_payback_zero_se_cumulato_anno_zero_non_negativo(self):
        assert _F["mh736_payback"](
            [0.0, 100.0]) == 0

    def test_payback_none_se_mai(self):
        assert _F["mh736_payback"](
            [-10000000000.0] + [NETTO_DEMO] * 30) is None

    def test_lcoe_demo(self):
        assert _F["mh736_lcoe"](
            CAPEX_DEMO, 30, COSTI_DEMO,
            ENERGIA_DEMO) == pytest.approx(LCOE_DEMO, rel=REL)

    def test_lcoe_none_se_energia_zero(self):
        assert _F["mh736_lcoe"](
            180000000.0, 30, 4261440.0, 0.0) is None

    def test_lcoe_formula_indipendente(self):
        assert _F["mh736_lcoe"](
            120000.0, 10, 5000.0,
            1000.0) == pytest.approx(
            (12000.0 + 5000.0) / 1000.0, rel=REL)

    def test_margine_demo(self):
        assert _F["mh736_margine"](
            110.0, LCOE_DEMO) == pytest.approx(
            MARGINE_DEMO, rel=REL)

    def test_margine_none_se_lcoe_none(self):
        assert _F["mh736_margine"](100.0, None) is None

    def test_co2_demo(self):
        assert _F["mh736_co2_evitata"](
            ENERGIA_DEMO, 0.35) == pytest.approx(
            CO2_DEMO, rel=REL)

    def test_co2_fattore_zero(self):
        assert _F["mh736_co2_evitata"](
            ENERGIA_DEMO, 0.0) == pytest.approx(0.0, abs=1e-9)

    def test_verdetto_demo(self):
        assert _F["mh736_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10, ENERGIA_DEMO,
            NETTO_DEMO) == VERDETTO_DEMO

    def test_verdetto_conviente_van_positivo(self):
        assert _F["mh736_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, ENERGIA_DEMO,
            NETTO_DEMO) == "CONVIENTE"

    def test_verdetto_van_zero_marginale(self):
        assert _F["mh736_verdetto"](
            0.0, CAPEX_DEMO, 0.10, ENERGIA_DEMO,
            NETTO_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh736_verdetto"](
            -0.10 * CAPEX_DEMO, CAPEX_DEMO, 0.10,
            ENERGIA_DEMO, NETTO_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_oltre_limite(self):
        assert _F["mh736_verdetto"](
            -0.10 * CAPEX_DEMO - 1.0, CAPEX_DEMO, 0.10,
            ENERGIA_DEMO, NETTO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_netto_negativo_non_e_non_calcolabile(self):
        assert _F["mh736_verdetto"](
            -1000.0, CAPEX_DEMO, 0.10, ENERGIA_DEMO,
            -5000.0) == "MARGINALE"

    def test_verdetto_non_calcolabile_energia_zero(self):
        assert _F["mh736_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0,
            NETTO_DEMO) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_netto_nan(self):
        assert _F["mh736_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, ENERGIA_DEMO,
            float("nan")) == "NON_CALCOLABILE"


class TestDemo:
    def _bc(self, **kw):
        d = _F["mh736_demo"]()
        d.update(kw)
        return _F["mh736_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["energia_MWh_anno"] == pytest.approx(
            ENERGIA_DEMO, rel=REL)
        assert c["capex_EUR"] == pytest.approx(
            CAPEX_DEMO, rel=REL)
        assert c["costi_annui_EUR"] == pytest.approx(
            COSTI_DEMO, rel=REL)
        assert c["ricavo_EUR_anno"] == pytest.approx(
            RICAVO_DEMO, rel=REL)
        assert c["netto_EUR_anno"] == pytest.approx(
            NETTO_DEMO, rel=REL)
        assert abs(c["van"] - VAN_DEMO) <= 1.0
        assert abs(c["tir"] - TIR_DEMO) <= 0.01
        assert c["payback"] == PAYBACK_DEMO
        assert c["lcoe_EUR_MWh"] == pytest.approx(
            LCOE_DEMO, rel=REL)
        assert c["margine_EUR_MWh"] == pytest.approx(
            MARGINE_DEMO, rel=REL)
        assert c["co2_evitata_t_anno"] == pytest.approx(
            CO2_DEMO, rel=REL)
        assert c["verdetto"] == VERDETTO_DEMO
        assert len(c["flussi"]) == 31

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()["van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()["lcoe_EUR_MWh"] == \
            _F["demo_calcoli"]()["lcoe_EUR_MWh"]

    def test_demo_defaults_contro_costanti_test(self):
        d = _F["mh736_demo"]()
        for k, v in _DEMO.items():
            assert d[k] == v, k
        assert len(d) == 10

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("energia_MWh_anno",
                       "capex_EUR",
                       "costi_annui_EUR",
                       "ricavo_EUR_anno",
                       "netto_EUR_anno",
                       "van",
                       "tir",
                       "lcoe_EUR_MWh",
                       "margine_EUR_MWh",
                       "co2_evitata_t_anno"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 14" in doc
        assert "verdetto = 'MARGINALE'" in doc

    def test_prezzo_al_lcoe_margine_zero_van_negativo(self):
        # Prezzo = LCOE: margine 0 per costruzione,
        # ma VAN negativa (il LCOE ripartisce il
        # CAPEX in quote lineari, il VAN lo
        # attualizza): NON_CONVIENTE, non VAN=0.
        n = self._bc(prezzo_el_EUR_per_MWh=LCOE_DEMO)
        assert n["valid"] is True
        assert n["margine_EUR_MWh"] == pytest.approx(
            0.0, abs=1e-9)
        assert n["van"] < 0.0
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_prezzo_140_conviente(self):
        # Prezzo 140 EUR/MWh: netto 17.813.760
        # EUR/anno, VAN circa +41.051.681,47 EUR
        # -> CONVIENTE.
        n = self._bc(prezzo_el_EUR_per_MWh=140.0)
        assert n["valid"] is True
        assert n["verdetto"] == "CONVIENTE"
        assert n["van"] > 0.0

    def test_prezzo_40_non_conviente(self):
        # Prezzo 40 EUR/MWh: netto 2.045.760
        # EUR/anno, VAN circa -154.614.079,91
        # EUR, oltre la tolleranza 18.000.000
        # EUR -> NON_CONVIENTE.
        n = self._bc(prezzo_el_EUR_per_MWh=40.0)
        assert n["valid"] is True
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["van"] < -0.10 * CAPEX_DEMO

    def test_prezzo_zero_non_conviente(self):
        # Prezzo 0: ricavo zero, netto negativo
        # pari a -costi annui, VAN negativa oltre
        # tolleranza -> NON_CONVIENTE.
        n = self._bc(prezzo_el_EUR_per_MWh=0.0)
        assert n["valid"] is True
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_capex_zero_tir_none_payback_zero(self):
        # CAPEX zero e prezzo 100: tutti i flussi
        # >= 0 -> TIR None, payback 0, VAN
        # positiva -> CONVIENTE.
        n = self._bc(capex_EUR_per_kW=0.0)
        assert n["valid"] is True
        assert n["capex_EUR"] == pytest.approx(0.0, abs=1e-9)
        assert n["tir"] is None
        assert n["payback"] == 0
        assert n["verdetto"] == "CONVIENTE"

    def test_potenza_zero_neutro(self):
        n = self._bc(potenza_MW=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["lcoe_EUR_MWh"] is None

    def test_cf_zero_neutro(self):
        n = self._bc(fattore_capacita=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_cf_oltre_uno_neutro(self):
        n = self._bc(fattore_capacita=1.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_cf_uno_valido(self):
        n = self._bc(fattore_capacita=1.0)
        assert n["valid"] is True

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
        n = self._bc(potenza_MW=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["netto_EUR_anno"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(potenza_MW=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(vita_anni=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_stringa_neutro(self):
        n = self._bc(potenza_MW="500")
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_capex_negativo_neutro(self):
        n = self._bc(capex_EUR_per_kW=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_fattore_rete_zero_valido_co2_zero(self):
        n = self._bc(fattore_rete_kg_per_kWh=0.0)
        assert n["valid"] is True
        assert n["co2_evitata_t_anno"] == pytest.approx(
            0.0, abs=1e-9)

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh736_neutro"]()
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
        assert n["lcoe_EUR_MWh"] is None
        assert n["margine_EUR_MWh"] is None
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh736_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "potenza_MW", "fattore_capacita",
                       "capex_EUR_per_kW",
                       "opex_fisso_EUR_per_kW_anno",
                       "opex_var_EUR_per_MWh",
                       "prezzo_el_EUR_per_MWh",
                       "wacc_frac", "vita_anni",
                       "tolleranza_frac",
                       "fattore_rete_kg_per_kWh",
                       "energia_MWh_anno",
                       "capex_EUR", "costi_annui_EUR",
                       "ricavo_EUR_anno",
                       "netto_EUR_anno", "flussi", "van",
                       "tir", "payback", "lcoe_EUR_MWh",
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
        assert len(b["df_tabella"]) == 22
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Energia (MWh/anno)" in voci
        assert "CAPEX (EUR)" in voci
        assert "Costi annui (EUR/anno)" in voci
        assert "Ricavo (EUR/anno)" in voci
        assert "VAN (EUR)" in voci
        assert "LCOE (EUR/MWh)" in voci
        assert "Margine (EUR/MWh)" in voci
        assert "CO2 evitata (t/anno)" in voci
        assert "Verdetto" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (EUR/anno)",
                                               "Cumulato (EUR)"]
        assert len(b["df_flussi"]) == 31
        assert b["df_flussi"]["Flusso (EUR/anno)"].iloc[0] == \
            pytest.approx(-CAPEX_DEMO, rel=REL)
        assert b["df_flussi"]["Flusso (EUR/anno)"].iloc[1] == \
            pytest.approx(NETTO_DEMO, rel=REL)


class TestCsv:
    def _ing(self):
        return _F["mh736_demo"]()

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh736_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") == 23

    def test_csv_contiene_verdetti_e_costi(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh736_csv"](bc, self._ing())
        assert "verdetto;MARGINALE" in txt
        assert "capex_EUR" in txt
        assert "van_eur" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "lcoe_EUR_MWh" in txt
        assert "margine_EUR_MWh" in txt
        assert "co2_evitata_t_anno" in txt
        assert "potenza_MW" in txt
        assert "energia_MWh_anno" in txt
        assert "costi_annui_EUR" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh736_csv"](bc, self._ing())
        assert f"netto_EUR_anno;{bc['netto_EUR_anno']}" in txt
        assert f"energia_MWh_anno;{bc['energia_MWh_anno']}" in txt
        assert "potenza_MW;20.0" in txt
        assert "capex_EUR_per_kW;9000.0" in txt
        assert f"lcoe_EUR_MWh;{bc['lcoe_EUR_MWh']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def736["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def736\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 10, ui_keys
        demo_keys = set(_F["mh736_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh736_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh736_demo():")
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
        ui_keys = set(re.findall(r'_def736\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W737 (26/10/2026) - tab736' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh736_num", "mh736_nneg", "mh736_pos",
                     "mh736_int_pos", "mh736_frac_01",
                     "mh736_frac_cf", "mh736_frac_toll",
                     "mh736_energia", "mh736_capex",
                     "mh736_costi",
                     "mh736_ricavo", "mh736_netto",
                     "mh736_flussi", "mh736_van",
                     "mh736_tir", "mh736_payback",
                     "mh736_lcoe", "mh736_margine",
                     "mh736_co2_evitata", "mh736_verdetto",
                     "mh736_valida", "_mh736_neutro",
                     "mh736_calcola", "mh736_csv",
                     "mh736_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_nessun_residuo_736(self):
        assert "mh735" not in _helpers_src()
        assert "mh735" not in _ui_src()
        assert "st735" not in _ui_src()
        assert "tab735" not in _ui_src()
        assert "W736" not in _helpers_src()
        assert "W736" not in _ui_src()
        assert "mh736" in _helpers_src()
        assert "st736" in _ui_src()

    def test_helpers_parse_ast(self):
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w737_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE736) == 1

    def test_blocco_with_tab736(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab736:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE736

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st736_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 13, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st736_") for k in keys)

    def test_chiavi_st_input_presenti(self):
        keys = re.findall(r'key="(st736_[a-z0-9_]+)"', _ui_src())
        attese = ["st736_potenza", "st736_cf",
                  "st736_capex", "st736_opex_fisso",
                  "st736_opex_var", "st736_prezzo",
                  "st736_fattore_rete", "st736_vita",
                  "st736_wacc", "st736_tolleranza",
                  "st736_calcola"]
        assert len(attese) == 11
        for k in attese:
            assert k in keys, k

    def test_chiavi_st_niente_fstring_dinamiche(self):
        src = _ui_src()
        assert 'key=f"' not in src
        assert "key=f'" not in src

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg736" in src
        assert "NON_CALCOLABILE" in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg736") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg736")
        assert g < src.index("st.bar_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "LCOE (EUR/MWh)" in src
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
        assert "sonde" in src
        assert "convenzionale" in src
        assert "idrotermali" in src
        assert "EGS" in src

    def test_distinzioni_in_header_helpers(self):
        src = _helpers_src()
        assert "sonde" in src
        assert "convenzionale" in src
        assert "idrotermali" in src
        assert "EGS" in src

    def test_nota_didattica_presente(self):
        src = _ui_src()
        assert "NOTA DIDATTICA" in src
        assert "157.680" in src
        assert "55.188" in src

    def test_grafico_bar_chart_presente(self):
        src = _ui_src()
        assert "st.bar_chart" in src
        assert "_dati736" in src
        assert '"EUR/MWh"' in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh736_csv" in src
        assert "geotermia-egs.csv" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st736_show_flussi" in src
        assert "st.checkbox" in src

    def test_niente_nome(self):
        assert "Emanuele" not in _helpers_src()
        assert "Emanuele" not in _ui_src()

    def test_ancora_helper_presente(self):
        assert "# W737 (26/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab736:")
