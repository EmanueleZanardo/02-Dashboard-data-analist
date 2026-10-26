"""Test tab734 "🌡️💧 Accumulo termico in acquifero (ATES): il calore estivo paga d'inverno?"

Nuova tab tab734 (doppietto ATES, w735).
Business case deterministico di un doppietto
ATES: volume pompato da portata e ore di
carica, calore caricato da volume e salto
termico, calore erogato dopo il recupero in
falda, energia di pompaggio, costo energia,
CAPEX, costi annui, ricavo, netto, VAN, TIR,
payback, LCOE, margine sul prezzo, CO2
evitata e verdetto.

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
portata 100 m3/ora; ore carica 2000
ore/anno; salto termico 10 K; recupero
0,75; consumo pompaggio 0,5 kWh/m3;
prezzo elettricita' 0,10 EUR/kWh; CAPEX
3000 EUR/(m3/ora); opex variabile 5
EUR/MWh; opex fisso 10000 EUR/anno;
prezzo calore 80 EUR/MWh; rendimento
caldaia 0,90; fattore gas 0,20 kg/kWh;
WACC 0,05 (5 %); vita 25 anni; tolleranza
0,10 (10 % del CAPEX).

- volume_m3_anno = 200000.0
- calore_caricato_kWh = 1600000.0
- calore_erogato_kWh = 1200000.0
- calore_erogato_MWh = 1200.0
- energia_pompaggio_kWh = 100000.0
- costo_energia_EUR = 10000.0
- capex_EUR = 300000.0
- costi_annui_EUR = 26000.0
- ricavo_EUR_anno = 96000.0
- netto_EUR_anno = 70000.0
- van = 686576.1196231324
- tir = 23.20682843846629
- payback = 5
- lcoe_EUR_MWh = 31.666666666666668
- margine_EUR_MWh = 48.33333333333333
- co2_evitata_t_anno = 266.6666666666667
- verdetto = 'CONVIENTE'

Scomposizione: volume 100 x 2000 =
200.000 m3/anno; calore caricato 200.000 x
10 x 0,8 = 1.600.000 kWh/anno; calore
erogato 1.600.000 x 0,75 = 1.200.000
kWh/anno (1200 MWh/anno); energia
pompaggio 200.000 x 0,5 = 100.000
kWh/anno; costo energia 100.000 x 0,10 =
10.000 EUR/anno; CAPEX 100 x 3000 =
300.000 EUR; costi annui 10.000 + 1200 x
5 + 10.000 = 26.000 EUR/anno; ricavo 1200
x 80 = 96.000 EUR/anno; netto 96.000 -
26.000 = 70.000 EUR/anno; flussi: anno 0
-300.000, anni 1-25 netto 70.000 (piatti);
VAN -300.000 + 70.000 x 14,093944
(annuita' 25 anni al 5 %) =
686576.1196231324 EUR; TIR
23.20682843846629 % (il tasso che azzera
il VAN dei flussi); payback 5 (il
cumulato supera lo zero al quinto anno:
-300.000 + 5 x 70.000 = 50.000); LCOE
(300.000 / 25 + 26.000) / 1200 =
31.666666666666668 EUR/MWh; margine 80 -
31.666666666666668 = 48.33333333333333
EUR/MWh; CO2 evitata (1.200.000 / 0,90 x
0,20) / 1000 = 266.6666666666667 t/anno;
verdetto CONVIENTE perche' VAN > 0.
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
    if (p / "w735_helpers.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w735_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w735_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w735_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w735_helpers.py: {missing}")
    return out


_F = _load("mh734_num", "mh734_nneg", "mh734_pos",
           "mh734_int_pos", "mh734_frac_01",
           "mh734_frac_rec", "mh734_frac_rend",
           "mh734_frac_toll",
           "mh734_volume", "mh734_caricato",
           "mh734_erogato", "mh734_pompaggio",
           "mh734_costo_energia", "mh734_capex",
           "mh734_costi", "mh734_ricavo",
           "mh734_netto", "mh734_flussi",
           "mh734_van", "mh734_tir", "mh734_payback",
           "mh734_lcoe", "mh734_margine",
           "mh734_co2_evitata", "mh734_verdetto",
           "mh734_valida", "_mh734_neutro",
           "mh734_calcola", "mh734_csv",
           "mh734_demo", "demo_calcoli")

TITLE734 = ("🌡️💧 Accumulo termico in acquifero (ATES): "
            "il calore estivo paga d'inverno?")

VOLUME_DEMO = 200000.0
CARICATO_DEMO = 1600000.0
EROGATO_KWH_DEMO = 1200000.0
EROGATO_MWH_DEMO = 1200.0
POMPAGGIO_DEMO = 100000.0
COSTO_ENE_DEMO = 10000.0
CAPEX_DEMO = 300000.0
COSTI_DEMO = 26000.0
RICAVO_DEMO = 96000.0
NETTO_DEMO = 70000.0
VAN_DEMO = 686576.1196231324
TIR_DEMO = 23.20682843846629
PAYBACK_DEMO = 5
LCOE_DEMO = 31.666666666666668
MARGINE_DEMO = 48.33333333333333
CO2_DEMO = 266.6666666666667
VERDETTO_DEMO = "CONVIENTE"

_DEMO = {
    "portata_m3_ora": 100.0,
    "ore_carica_anno": 2000,
    "delta_T_K": 10.0,
    "recupero_frazione": 0.75,
    "consumo_pompaggio_kWh_m3": 0.5,
    "prezzo_el_EUR_kWh": 0.10,
    "capex_EUR_per_m3h": 3000.0,
    "opex_var_EUR_MWh": 5.0,
    "opex_fisso_EUR_anno": 10000.0,
    "prezzo_calore_EUR_MWh": 80.0,
    "rendimento_caldaia": 0.90,
    "fattore_gas_kg_kWh": 0.20,
    "wacc_frac": 0.05,
    "vita_anni": 25,
    "tolleranza_frac": 0.10,
}

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w735_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w735_ui.py").read_text(encoding="utf-8")


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh734_demo"]()
        d.update(kw)
        return _F["mh734_valida"](**d)

    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh734_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh734_num"]("100", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh734_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh734_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh734_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh734_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh734_pos"](0.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh734_int_pos"](2.5, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh734_int_pos"](25.0, "x") == 25

    def test_frac_01_rifiuta_zero_e_uno(self):
        with pytest.raises(ValueError):
            _F["mh734_frac_01"](0.0, "x")
        with pytest.raises(ValueError):
            _F["mh734_frac_01"](1.0, "x")

    def test_frac_rec_accetta_zero_rifiuta_uno_e_oltre(self):
        assert _F["mh734_frac_rec"](0.0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh734_frac_rec"](1.0, "x")
        with pytest.raises(ValueError):
            _F["mh734_frac_rec"](1.01, "x")

    def test_frac_rend_accetta_uno_rifiuta_zero_e_oltre(self):
        assert _F["mh734_frac_rend"](1.0, "x") == 1.0
        with pytest.raises(ValueError):
            _F["mh734_frac_rend"](0.0, "x")
        with pytest.raises(ValueError):
            _F["mh734_frac_rend"](1.01, "x")

    def test_frac_toll_accetta_zero_rifiuta_uno(self):
        assert _F["mh734_frac_toll"](0.0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh734_frac_toll"](1.0, "x")
        with pytest.raises(ValueError):
            _F["mh734_frac_toll"](-0.01, "x")

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_portata_zero_e_negativa_non_valide(self):
        assert self._val(portata_m3_ora=0.0)["valido"] is False
        assert self._val(portata_m3_ora=-1.0)["valido"] is False

    def test_ore_zero_frazione_e_oltre_8760_non_validi(self):
        assert self._val(ore_carica_anno=0)["valido"] is False
        assert self._val(ore_carica_anno=2000.5)["valido"] is False
        assert self._val(ore_carica_anno=8761)["valido"] is False
        assert self._val(ore_carica_anno=8760)["valido"] is True

    def test_recupero_uno_e_oltre_non_validi_zero_valido(self):
        assert self._val(recupero_frazione=1.0)["valido"] is False
        assert self._val(recupero_frazione=1.01)["valido"] is False
        assert self._val(recupero_frazione=0.0)["valido"] is True

    def test_delta_T_zero_e_negativo_non_validi(self):
        assert self._val(delta_T_K=0.0)["valido"] is False
        assert self._val(delta_T_K=-1.0)["valido"] is False

    def test_rendimento_zero_e_oltre_uno_non_validi_uno_valido(self):
        assert self._val(rendimento_caldaia=0.0)["valido"] is False
        assert self._val(rendimento_caldaia=1.01)["valido"] is False
        assert self._val(rendimento_caldaia=1.0)["valido"] is True

    def test_negativi_non_validi(self):
        for k in ("consumo_pompaggio_kWh_m3",
                  "prezzo_el_EUR_kWh",
                  "capex_EUR_per_m3h",
                  "opex_var_EUR_MWh",
                  "opex_fisso_EUR_anno",
                  "prezzo_calore_EUR_MWh",
                  "fattore_gas_kg_kWh"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_vita_zero_e_frazione_non_valide(self):
        assert self._val(vita_anni=0)["valido"] is False
        assert self._val(vita_anni=25.5)["valido"] is False

    def test_wacc_zero_e_uno_non_validi(self):
        assert self._val(wacc_frac=0.0)["valido"] is False
        assert self._val(wacc_frac=1.0)["valido"] is False
        assert self._val(wacc_frac=0.05)["valido"] is True

    def test_tolleranza_uno_non_valida_zero_valida(self):
        assert self._val(tolleranza_frac=1.0)["valido"] is False
        assert self._val(tolleranza_frac=0.0)["valido"] is True

    def test_nan_non_valido(self):
        assert self._val(portata_m3_ora=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(portata_m3_ora=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(vita_anni=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(portata_m3_ora="100")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(prezzo_calore_EUR_MWh=0.0)["valido"] is True
        assert self._val(capex_EUR_per_m3h=0.0)["valido"] is True
        assert self._val(fattore_gas_kg_kWh=0.0)["valido"] is True
        assert self._val(tolleranza_frac=0.0)["valido"] is True
        assert self._val(recupero_frazione=0.0)["valido"] is True


class TestFunzioni:
    def test_volume_demo(self):
        assert _F["mh734_volume"](
            100.0, 2000) == pytest.approx(
            VOLUME_DEMO, rel=REL)

    def test_volume_rifiuta_oltre_8760(self):
        with pytest.raises(ValueError):
            _F["mh734_volume"](100.0, 8761)

    def test_caricato_demo(self):
        assert _F["mh734_caricato"](
            VOLUME_DEMO, 10.0) == pytest.approx(
            CARICATO_DEMO, rel=REL)

    def test_caricato_formula_letterale(self):
        assert _F["mh734_caricato"](
            1000.0, 10.0) == pytest.approx(8000.0, rel=REL)

    def test_caricato_rifiuta_delta_T_zero(self):
        with pytest.raises(ValueError):
            _F["mh734_caricato"](VOLUME_DEMO, 0.0)

    def test_erogato_demo(self):
        assert _F["mh734_erogato"](
            CARICATO_DEMO, 0.75) == pytest.approx(
            EROGATO_KWH_DEMO, rel=REL)

    def test_erogato_recupero_zero(self):
        assert _F["mh734_erogato"](
            CARICATO_DEMO, 0.0) == pytest.approx(0.0, abs=1e-9)

    def test_erogato_rifiuta_recupero_uno(self):
        with pytest.raises(ValueError):
            _F["mh734_erogato"](CARICATO_DEMO, 1.0)

    def test_pompaggio_demo(self):
        assert _F["mh734_pompaggio"](
            VOLUME_DEMO, 0.5) == pytest.approx(
            POMPAGGIO_DEMO, rel=REL)

    def test_costo_energia_demo(self):
        assert _F["mh734_costo_energia"](
            POMPAGGIO_DEMO, 0.10) == pytest.approx(
            COSTO_ENE_DEMO, rel=REL)

    def test_capex_demo(self):
        assert _F["mh734_capex"](
            100.0, 3000.0) == pytest.approx(
            CAPEX_DEMO, rel=REL)

    def test_capex_formula_indipendente(self):
        assert _F["mh734_capex"](
            100.0, 3000.0) == pytest.approx(
            300000.0, rel=REL)

    def test_costi_demo(self):
        assert _F["mh734_costi"](
            COSTO_ENE_DEMO, EROGATO_MWH_DEMO, 5.0,
            10000.0) == pytest.approx(COSTI_DEMO, rel=REL)

    def test_costi_solo_fisso(self):
        assert _F["mh734_costi"](
            0.0, EROGATO_MWH_DEMO, 0.0,
            10000.0) == pytest.approx(10000.0, rel=REL)

    def test_ricavo_demo(self):
        assert _F["mh734_ricavo"](
            EROGATO_MWH_DEMO, 80.0) == pytest.approx(
            RICAVO_DEMO, rel=REL)

    def test_netto_demo(self):
        assert _F["mh734_netto"](
            RICAVO_DEMO, COSTI_DEMO) == pytest.approx(
            NETTO_DEMO, rel=REL)

    def test_netto_puo_essere_negativo(self):
        assert _F["mh734_netto"](
            1000.0, COSTI_DEMO) == pytest.approx(
            -25000.0, rel=REL)

    def test_flussi_demo(self):
        flussi = _F["mh734_flussi"](CAPEX_DEMO, NETTO_DEMO, 25)
        assert len(flussi) == 26
        assert flussi[0] == pytest.approx(-CAPEX_DEMO, rel=REL)
        assert all(f == pytest.approx(NETTO_DEMO, rel=REL)
                   for f in flussi[1:])

    def test_van_demo(self):
        flussi = _F["mh734_flussi"](CAPEX_DEMO, NETTO_DEMO, 25)
        assert abs(_F["mh734_van"](
            flussi, 0.05) - VAN_DEMO) <= 1.0

    def test_van_tasso_zero(self):
        flussi = _F["mh734_flussi"](CAPEX_DEMO, NETTO_DEMO, 25)
        atteso = -CAPEX_DEMO + NETTO_DEMO * 25
        assert _F["mh734_van"](
            flussi, 0.0) == pytest.approx(atteso, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh734_van"]([100.0, 100.0], -0.01)

    def test_tir_none_flussi_tutti_negativi(self):
        flussi = _F["mh734_flussi"](CAPEX_DEMO, -1000.0, 25)
        assert _F["mh734_tir"](flussi) is None

    def test_tir_none_tutti_flussi_non_negativi(self):
        assert _F["mh734_tir"](
            [0.0] + [NETTO_DEMO] * 25) is None

    def test_tir_none_nessun_cambio_segno_negativo(self):
        assert _F["mh734_tir"](
            [-1000.0] + [-100.0] * 10) is None

    def test_tir_esiste_caso_semplice_100_120(self):
        assert _F["mh734_tir"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_caso_semplice_1000_500_500_zero(self):
        assert abs(_F["mh734_tir"](
            [-1000.0, 500.0, 500.0])) <= 1e-9

    def test_tir_demo(self):
        flussi = _F["mh734_flussi"](CAPEX_DEMO, NETTO_DEMO, 25)
        tir = _F["mh734_tir"](flussi)
        assert tir is not None
        assert tir * 100.0 == pytest.approx(TIR_DEMO, rel=1e-9)

    def test_payback_demo(self):
        flussi = _F["mh734_flussi"](CAPEX_DEMO, NETTO_DEMO, 25)
        assert _F["mh734_payback"](flussi) == PAYBACK_DEMO

    def test_payback_semplice_due(self):
        assert _F["mh734_payback"](
            [-1000.0, 500.0, 500.0, 500.0]) == 2

    def test_payback_zero_se_cumulato_anno_zero_non_negativo(self):
        assert _F["mh734_payback"](
            [0.0, 100.0]) == 0

    def test_payback_none_se_mai(self):
        assert _F["mh734_payback"](
            [-1000000000.0] + [NETTO_DEMO] * 25) is None

    def test_lcoe_demo(self):
        assert _F["mh734_lcoe"](
            CAPEX_DEMO, 25, COSTI_DEMO,
            EROGATO_MWH_DEMO) == pytest.approx(LCOE_DEMO, rel=REL)

    def test_lcoe_none_se_erogato_zero(self):
        assert _F["mh734_lcoe"](
            300000.0, 25, 26000.0, 0.0) is None

    def test_lcoe_formula_indipendente(self):
        assert _F["mh734_lcoe"](
            120000.0, 10, 5000.0,
            1000.0) == pytest.approx(
            (12000.0 + 5000.0) / 1000.0, rel=REL)

    def test_margine_demo(self):
        assert _F["mh734_margine"](
            80.0, LCOE_DEMO) == pytest.approx(
            MARGINE_DEMO, rel=REL)

    def test_margine_none_se_lcoe_none(self):
        assert _F["mh734_margine"](80.0, None) is None

    def test_co2_demo(self):
        assert _F["mh734_co2_evitata"](
            EROGATO_KWH_DEMO, 0.90, 0.20) == pytest.approx(
            CO2_DEMO, rel=REL)

    def test_co2_rendimento_uno(self):
        assert _F["mh734_co2_evitata"](
            EROGATO_KWH_DEMO, 1.0, 0.20) == pytest.approx(
            EROGATO_KWH_DEMO * 0.20 / 1000.0, rel=REL)

    def test_co2_fattore_zero(self):
        assert _F["mh734_co2_evitata"](
            EROGATO_KWH_DEMO, 0.90, 0.0) == pytest.approx(0.0, abs=1e-9)

    def test_verdetto_demo(self):
        assert _F["mh734_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10, EROGATO_MWH_DEMO,
            NETTO_DEMO) == VERDETTO_DEMO

    def test_verdetto_conviente_van_positivo(self):
        assert _F["mh734_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, EROGATO_MWH_DEMO,
            NETTO_DEMO) == "CONVIENTE"

    def test_verdetto_van_zero_marginale(self):
        assert _F["mh734_verdetto"](
            0.0, CAPEX_DEMO, 0.10, EROGATO_MWH_DEMO,
            NETTO_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh734_verdetto"](
            -0.10 * CAPEX_DEMO, CAPEX_DEMO, 0.10,
            EROGATO_MWH_DEMO, NETTO_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_oltre_limite(self):
        assert _F["mh734_verdetto"](
            -0.10 * CAPEX_DEMO - 1.0, CAPEX_DEMO, 0.10,
            EROGATO_MWH_DEMO, NETTO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_netto_negativo_non_e_non_calcolabile(self):
        assert _F["mh734_verdetto"](
            -1000.0, CAPEX_DEMO, 0.10, EROGATO_MWH_DEMO,
            -5000.0) == "MARGINALE"

    def test_verdetto_non_calcolabile_erogato_zero(self):
        assert _F["mh734_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0,
            NETTO_DEMO) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_netto_nan(self):
        assert _F["mh734_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, EROGATO_MWH_DEMO,
            float("nan")) == "NON_CALCOLABILE"


class TestDemo:
    def _bc(self, **kw):
        d = _F["mh734_demo"]()
        d.update(kw)
        return _F["mh734_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["volume_m3_anno"] == pytest.approx(
            VOLUME_DEMO, rel=REL)
        assert c["calore_caricato_kWh"] == pytest.approx(
            CARICATO_DEMO, rel=REL)
        assert c["calore_erogato_kWh"] == pytest.approx(
            EROGATO_KWH_DEMO, rel=REL)
        assert c["calore_erogato_MWh"] == pytest.approx(
            EROGATO_MWH_DEMO, rel=REL)
        assert c["energia_pompaggio_kWh"] == pytest.approx(
            POMPAGGIO_DEMO, rel=REL)
        assert c["costo_energia_EUR"] == pytest.approx(
            COSTO_ENE_DEMO, rel=REL)
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
        assert len(c["flussi"]) == 26

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()["van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()["lcoe_EUR_MWh"] == \
            _F["demo_calcoli"]()["lcoe_EUR_MWh"]

    def test_demo_defaults_contro_costanti_test(self):
        d = _F["mh734_demo"]()
        for k, v in _DEMO.items():
            assert d[k] == v, k
        assert len(d) == 15

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("volume_m3_anno",
                       "calore_caricato_kWh",
                       "calore_erogato_kWh",
                       "calore_erogato_MWh",
                       "energia_pompaggio_kWh",
                       "costo_energia_EUR",
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
        assert "payback = 5" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_prezzo_38_marginale(self):
        # Prezzo 38 EUR/MWh: netto 19.600
        # EUR/anno, VAN circa -23.758,69 EUR,
        # entro la tolleranza 10 % di
        # 300.000 = 30.000 -> MARGINALE.
        n = self._bc(prezzo_calore_EUR_MWh=38.0)
        assert n["valid"] is True
        assert n["verdetto"] == "MARGINALE"
        assert -30000.0 < n["van"] < 0.0

    def test_prezzo_30_non_conviente(self):
        # Prezzo 30 EUR/MWh: netto 10.000
        # EUR/anno, VAN circa -159.060,55 EUR,
        # oltre la tolleranza 30.000 EUR
        # -> NON_CONVIENTE.
        n = self._bc(prezzo_calore_EUR_MWh=30.0)
        assert n["valid"] is True
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["van"] < -30000.0

    def test_prezzo_zero_non_conviente(self):
        # Prezzo 0: ricavo zero, netto negativo
        # pari a -costi annui, VAN negativa oltre
        # tolleranza -> NON_CONVIENTE.
        n = self._bc(prezzo_calore_EUR_MWh=0.0)
        assert n["valid"] is True
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_capex_zero_tir_none_payback_zero(self):
        # CAPEX zero e prezzo 80: tutti i flussi
        # >= 0 -> TIR None, payback 0, VAN
        # positiva -> CONVIENTE.
        n = self._bc(capex_EUR_per_m3h=0.0)
        assert n["valid"] is True
        assert n["capex_EUR"] == pytest.approx(0.0, abs=1e-9)
        assert n["tir"] is None
        assert n["payback"] == 0
        assert n["verdetto"] == "CONVIENTE"

    def test_recupero_zero_erogato_nullo_neutro(self):
        n = self._bc(recupero_frazione=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["lcoe_EUR_MWh"] is None

    def test_portata_zero_neutro(self):
        n = self._bc(portata_m3_ora=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["lcoe_EUR_MWh"] is None

    def test_ore_zero_neutro(self):
        n = self._bc(ore_carica_anno=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_ore_oltre_8760_neutro(self):
        n = self._bc(ore_carica_anno=8761)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_ore_8760_valido(self):
        n = self._bc(ore_carica_anno=8760)
        assert n["valid"] is True

    def test_delta_T_zero_neutro(self):
        n = self._bc(delta_T_K=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_recupero_uno_neutro(self):
        n = self._bc(recupero_frazione=1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_rendimento_zero_neutro(self):
        n = self._bc(rendimento_caldaia=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_rendimento_uno_valido(self):
        n = self._bc(rendimento_caldaia=1.0)
        assert n["valid"] is True

    def test_wacc_zero_e_uno_neutri(self):
        assert self._bc(wacc_frac=0.0)["verdetto"] == "NON_CALCOLABILE"
        assert self._bc(wacc_frac=1.0)["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_uno_neutro(self):
        n = self._bc(tolleranza_frac=1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(portata_m3_ora=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["netto_EUR_anno"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(portata_m3_ora=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(vita_anni=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_stringa_neutro(self):
        n = self._bc(portata_m3_ora="100")
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_capex_negativo_neutro(self):
        n = self._bc(capex_EUR_per_m3h=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh734_neutro"]()
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
        n = _F["_mh734_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "portata_m3_ora", "ore_carica_anno",
                       "delta_T_K",
                       "recupero_frazione",
                       "consumo_pompaggio_kWh_m3",
                       "prezzo_el_EUR_kWh",
                       "capex_EUR_per_m3h",
                       "opex_var_EUR_MWh",
                       "opex_fisso_EUR_anno",
                       "prezzo_calore_EUR_MWh",
                       "rendimento_caldaia",
                       "fattore_gas_kg_kWh",
                       "wacc_frac", "vita_anni",
                       "tolleranza_frac",
                       "volume_m3_anno",
                       "calore_caricato_kWh",
                       "calore_erogato_kWh",
                       "calore_erogato_MWh",
                       "energia_pompaggio_kWh",
                       "costo_energia_EUR",
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
        assert len(b["df_tabella"]) == 32
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Volume pompato (m3/anno)" in voci
        assert "Calore caricato (kWh/anno)" in voci
        assert "Calore erogato (MWh/anno)" in voci
        assert "Energia pompaggio (kWh/anno)" in voci
        assert "VAN (EUR)" in voci
        assert "LCOE (EUR/MWh)" in voci
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
        return _F["mh734_demo"]()

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh734_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") == 33

    def test_csv_contiene_verdetti_e_costi(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh734_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "capex_EUR" in txt
        assert "van_eur" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "lcoe_EUR_MWh" in txt
        assert "margine_EUR_MWh" in txt
        assert "co2_evitata_t_anno" in txt
        assert "portata_m3_ora" in txt
        assert "calore_caricato_kWh" in txt
        assert "calore_erogato_MWh" in txt
        assert "costo_energia_EUR" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh734_csv"](bc, self._ing())
        assert f"netto_EUR_anno;{bc['netto_EUR_anno']}" in txt
        assert f"calore_caricato_kWh;{bc['calore_caricato_kWh']}" in txt
        assert "portata_m3_ora;100.0" in txt
        assert "capex_EUR_per_m3h;3000.0" in txt
        assert f"lcoe_EUR_MWh;{bc['lcoe_EUR_MWh']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def734["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def734\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 15, ui_keys
        demo_keys = set(_F["mh734_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh734_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh734_demo():")
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
        ui_keys = set(re.findall(r'_def734\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W735 (26/10/2026) - tab734' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh734_num", "mh734_nneg", "mh734_pos",
                     "mh734_int_pos", "mh734_frac_01",
                     "mh734_frac_rec", "mh734_frac_rend",
                     "mh734_frac_toll",
                     "mh734_volume", "mh734_caricato",
                     "mh734_erogato", "mh734_pompaggio",
                     "mh734_costo_energia", "mh734_capex",
                     "mh734_costi",
                     "mh734_ricavo", "mh734_netto",
                     "mh734_flussi", "mh734_van",
                     "mh734_tir", "mh734_payback",
                     "mh734_lcoe", "mh734_margine",
                     "mh734_co2_evitata", "mh734_verdetto",
                     "mh734_valida", "_mh734_neutro",
                     "mh734_calcola", "mh734_csv",
                     "mh734_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_nessun_residuo_733(self):
        assert "mh733" not in _helpers_src()
        assert "mh733" not in _ui_src()
        assert "st733" not in _ui_src()
        assert "tab733" not in _ui_src()
        assert "W734" not in _helpers_src()
        assert "W734" not in _ui_src()
        assert "mh734" in _helpers_src()
        assert "st734" in _ui_src()

    def test_helpers_parse_ast(self):
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w735_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE734) == 1

    def test_blocco_with_tab734(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab734:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE734

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st734_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 18, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st734_") for k in keys)

    def test_chiavi_st_input_presenti(self):
        keys = re.findall(r'key="(st734_[a-z0-9_]+)"', _ui_src())
        attese = ["st734_portata", "st734_ore_carica",
                  "st734_delta_t", "st734_recupero",
                  "st734_pompaggio", "st734_prezzo_el",
                  "st734_capex", "st734_opex_var",
                  "st734_opex_fisso", "st734_prezzo_calore",
                  "st734_rendimento", "st734_fattore_gas",
                  "st734_vita", "st734_wacc",
                  "st734_tolleranza", "st734_calcola"]
        assert len(attese) == 16
        for k in attese:
            assert k in keys, k

    def test_chiavi_st_niente_fstring_dinamiche(self):
        src = _ui_src()
        assert 'key=f"' not in src
        assert "key=f'" not in src

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg734" in src
        assert "NON_CALCOLABILE" in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg734") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg734")
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
        assert "sonde geotermiche" in src
        assert "stagionale" in src
        assert "sabbia" in src
        assert "PCM" in src

    def test_distinzioni_in_header_helpers(self):
        src = _helpers_src()
        assert "sonde geotermiche" in src
        assert "stagionale" in src
        assert "sabbia" in src
        assert "PCM" in src

    def test_nota_didattica_presente(self):
        src = _ui_src()
        assert "NOTA DIDATTICA" in src
        assert "200.000" in src
        assert "1.200.000" in src

    def test_grafico_bar_chart_presente(self):
        src = _ui_src()
        assert "st.bar_chart" in src
        assert "_dati734" in src
        assert '"EUR/MWh"' in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh734_csv" in src
        assert "ates.csv" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st734_show_flussi" in src
        assert "st.checkbox" in src

    def test_niente_nome(self):
        assert "Emanuele" not in _helpers_src()
        assert "Emanuele" not in _ui_src()

    def test_ancora_helper_presente(self):
        assert "# W735 (26/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab734:")
