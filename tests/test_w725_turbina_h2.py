"""Test tab725 "🔥💧 Turbina a gas H2-ready: il co-firing a idrogeno paga il retrofit?"

Nuova tab tab725 (H2-ready, w726).
Business case INCREMENTALE del retrofit di una
turbina a gas per co-firing H2: tutta
l'economia di investimento (flussi, VAN, TIR,
payback, verdetto) e' sul margine incrementale
(margine mix meno margine baseline gas 100 %).
Fisica: E_el = P_nom x ore; eta_mix =
eta_base - delta_eta x fraz_H2; E_fuel_mix =
E_el / eta_mix; E_H2 = fraz_H2 x E_fuel_mix;
E_gas = (1 - fraz_H2) x E_fuel_mix. Baseline:
E_fuel_base = E_el / eta_base. CO2 evitata
INFORMATIVA, mai nel conto economico.

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
potenza nominale 100 MW; ore annue 6000;
rendimento base 0,55; perdita di rendimento
a H2 100 % 0,02; frazione H2 0,30 (base
energetica); prezzo gas 40 EUR/MWh_th; prezzo
H2 50 EUR/MWh_th; prezzo elettricita' 120
EUR/MWh_el; fattore CO2 gas 0,202 t/MWh_th;
prezzo ETS 90 EUR/t; opex fisso 2000000
EUR/anno; opex variabile 3 EUR/MWh_el; CAPEX
retrofit 15000000 EUR; vita 15 anni; WACC 0,06
(6 %); tolleranza 0,10 (10 % del CAPEX).

- e_el_mwh = 600000.0
- eta_mix = 0.544
- e_fuel_mix_mwh = 1102941.1764705882
- e_gas_mwh = 772058.8235294117
- e_h2_mwh = 330882.35294117645
- costo_comb_mix_eur_anno = 47426470.58823529
- ets_mix_eur_anno = 14036029.411764706
- ricavi_eur_anno = 72000000.0
- margine_mix_eur_anno = 6737500.000000007
- e_fuel_base_mwh = 1090909.0909090908
- costo_comb_base_eur_anno = 43636363.63636363
- ets_base_eur_anno = 19832727.272727273
- costo_base_eur_anno = 67269090.9090909
- margine_base_eur_anno = 4730909.090909094
- margine_incr_eur_anno = 2006590.9090909138
- co2_emessa_mix_t_anno = 155955.88235294117
- co2_emessa_base_t_anno = 220363.63636363635
- co2_evitata_t_anno = 64407.75401069519
- van = 4488510.525628488
- tir = 10.305245043451858
- payback = 8
- verdetto = 'CONVIENTE'

Scomposizione: E_el 100 x 6000 = 600000,0
MWh/anno; eta_mix 0,55 - 0,02 x 0,30 = 0,544;
E_fuel_mix 600000 / 0,544 = 1102941,1764705882
MWh_th/anno; E_H2 0,30 x 1102941,1764705882 =
330882,35294117645 MWh_th/anno; E_gas 0,70 x
1102941,1764705882 = 772058,8235294117
MWh_th/anno; costo combustibile mix 772058,8235
x 40 + 330882,3529 x 50 = 47426470,58823529
EUR/anno; ETS mix 772058,8235 x 0,202 x 90 =
14036029,411764706 EUR/anno; costo mix
2000000 + 3 x 600000 + 47426470,58823529 +
14036029,411764706 = 65262500,0 EUR/anno;
ricavi 600000 x 120 = 72000000,0 EUR/anno;
margine mix 72000000,0 - 65262500,0 =
6737500,0 EUR/anno; baseline: E_fuel_base
600000 / 0,55 = 1090909,0909090908
MWh_th/anno; costo combustibile base
1090909,0909 x 40 = 43636363,63636363
EUR/anno; ETS base 1090909,0909 x 0,202 x 90
= 19832727,272727273 EUR/anno; costo base
67269090,9090909 EUR/anno; margine base
72000000,0 - 67269090,9090909 =
4730909,090909094 EUR/anno; margine
incrementale 6737500,0 - 4730909,090909094 =
2006590,9090909138 EUR/anno; flussi:
anno 0 -15000000,0, anni 1-15 margine
incrementale 2006590,9090909138 (piatti);
VAN 4488510,525628488 a WACC 6 % su 15 anni;
TIR 10,305245043451858 % (il tasso che azzera
il VAN dei flussi sopra); payback 8 (il
cumulato diventa positivo all'anno 8:
-15000000,0 + 7 x 2006590,9090909138 =
-953863,6363636364 all'anno 7, poi +
2006590,9090909138 = 1052727,2727272727
all'anno 8); CO2 emessa mix 772058,8235294117
x 0,202 = 155955,88235294117 t/anno; CO2
evitata (1090909,0909090908 - 772058,8235294117)
x 0,202 = 64407,75401069519 t/anno
(INFORMATIVA: non entra nel conto economico);
VAN >= 0 -> CONVIENTE.
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
    if (p / "w726_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w726_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w726_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w726_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w726_helpers.py: {missing}")
    return out


_F = _load("mh725_num", "mh725_nneg", "mh725_pos",
           "mh725_int_pos", "mh725_eta_valida",
           "mh725_fraz_valida", "mh725_e_el",
           "mh725_eta_mix", "mh725_e_fuel_mix",
           "mh725_e_h2", "mh725_e_gas",
           "mh725_e_fuel_base", "mh725_costo_comb_mix",
           "mh725_ets_mix", "mh725_costo_totale",
           "mh725_ricavi", "mh725_margine",
           "mh725_margine_incr", "mh725_flussi",
           "mh725_van_flussi", "mh725_tir_flussi",
           "mh725_payback_flussi", "mh725_verdetto",
           "mh725_co2_emessa_mix", "mh725_co2_evitata",
           "mh725_confronto", "mh725_valida",
           "_mh725_neutro", "mh725_calcola",
           "mh725_sensitivita", "mh725_csv",
           "mh725_demo", "demo_calcoli")

TITLE725 = ("🔥💧 Turbina a gas H2-ready: "
            "il co-firing a idrogeno paga il retrofit?")

E_EL_DEMO = 600000.0
ETA_MIX_DEMO = 0.544
E_FUEL_MIX_DEMO = 1102941.1764705882
E_GAS_DEMO = 772058.8235294117
E_H2_DEMO = 330882.35294117645
COSTO_COMB_MIX_DEMO = 47426470.58823529
ETS_MIX_DEMO = 14036029.411764706
COSTO_MIX_DEMO = 65262500.0
RIC_DEMO = 72000000.0
MARGINE_MIX_DEMO = 6737500.0
E_FUEL_BASE_DEMO = 1090909.0909090908
COSTO_COMB_BASE_DEMO = 43636363.63636363
ETS_BASE_DEMO = 19832727.272727273
COSTO_BASE_DEMO = 67269090.9090909
MARGINE_BASE_DEMO = 4730909.090909094
MARGINE_INCR_DEMO = 2006590.9090909138
CO2_MIX_DEMO = 155955.88235294117
CO2_BASE_DEMO = 220363.63636363635
CO2_EVITATA_DEMO = 64407.75401069519
VAN_DEMO = 4488510.525628488
TIR_DEMO = 10.305245043451858
PAYBACK_DEMO = 8
CAPEX_DEMO = 15000000.0
VITA_DEMO = 15
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w726_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w726_ui.py").read_text(encoding="utf-8")


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh725_demo"]()
        d.update(kw)
        return _F["mh725_valida"](**d)

    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh725_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh725_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh725_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh725_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh725_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh725_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh725_pos"](0.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh725_int_pos"](2.5, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh725_int_pos"](15.0, "x") == 15

    def test_eta_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh725_eta_valida"](0.0, "x")

    def test_eta_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh725_eta_valida"](-0.1, "x")

    def test_eta_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh725_eta_valida"](1.01, "x")

    def test_eta_accetta_uno(self):
        assert _F["mh725_eta_valida"](1.0, "x") == 1.0

    def test_fraz_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh725_fraz_valida"](-0.1, "x")

    def test_fraz_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh725_fraz_valida"](1.5, "x")

    def test_fraz_accetta_zero_e_uno(self):
        assert _F["mh725_fraz_valida"](0.0, "x") == 0.0
        assert _F["mh725_fraz_valida"](1.0, "x") == 1.0

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_p_nom_zero_non_valido(self):
        assert self._val(p_nom_mw=0.0)["valido"] is False

    def test_ore_zero_non_valide(self):
        assert self._val(ore_annue=0.0)["valido"] is False

    def test_eta_base_zero_non_valida(self):
        assert self._val(eta_base=0.0)["valido"] is False

    def test_eta_base_sopra_uno_non_valida(self):
        assert self._val(eta_base=1.5)["valido"] is False

    def test_eta_base_uno_valida(self):
        assert self._val(eta_base=1.0)["valido"] is True

    def test_delta_negativo_non_valido(self):
        assert self._val(delta_eta=-0.01)["valido"] is False

    def test_delta_zero_valido(self):
        assert self._val(delta_eta=0.0)["valido"] is True

    def test_fraz_fuori_intervallo_non_valide(self):
        assert self._val(fraz_h2=-0.1)["valido"] is False
        assert self._val(fraz_h2=1.1)["valido"] is False

    def test_fraz_estremi_validi(self):
        assert self._val(fraz_h2=0.0)["valido"] is True
        assert self._val(fraz_h2=1.0)["valido"] is True

    def test_eta_mix_non_positiva_non_valida(self):
        # eta_base 0,55 - delta 0,60 x fraz 1,0 = -0,05.
        v = self._val(eta_base=0.55, delta_eta=0.60, fraz_h2=1.0)
        assert v["valido"] is False
        assert "miscela" in v["errore"]

    def test_eta_mix_zero_non_valida(self):
        # eta_base 0,55 - delta 0,55 x fraz 1,0 = 0.
        v = self._val(eta_base=0.55, delta_eta=0.55, fraz_h2=1.0)
        assert v["valido"] is False

    def test_negativi_non_validi(self):
        for k in ("prezzo_gas_eur_mwh_th",
                  "prezzo_h2_eur_mwh_th",
                  "prezzo_elettricita_eur_mwh_el",
                  "fattore_co2_gas_t_mwh_th",
                  "prezzo_ets_eur_t",
                  "opex_fisso_eur_anno",
                  "opex_var_eur_mwh_el",
                  "capex_retrofit_eur",
                  "wacc_frac", "tolleranza_frac"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_vita_zero_non_valida(self):
        assert self._val(vita_anni=0)["valido"] is False

    def test_vita_non_intera_non_valida(self):
        assert self._val(vita_anni=15.5)["valido"] is False

    def test_tolleranza_sopra_uno_valida_brief(self):
        assert self._val(tolleranza_frac=1.5)["valido"] is True

    def test_wacc_senza_tetto_superiore(self):
        assert self._val(wacc_frac=1.5)["valido"] is True

    def test_nan_non_valido(self):
        assert self._val(eta_base=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(p_nom_mw=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(vita_anni=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(eta_base="0.55")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(prezzo_gas_eur_mwh_th=0.0)["valido"] is True
        assert self._val(prezzo_h2_eur_mwh_th=0.0)["valido"] is True
        assert self._val(prezzo_elettricita_eur_mwh_el=0.0)["valido"] is True
        assert self._val(fattore_co2_gas_t_mwh_th=0.0)["valido"] is True
        assert self._val(prezzo_ets_eur_t=0.0)["valido"] is True
        assert self._val(opex_fisso_eur_anno=0.0)["valido"] is True
        assert self._val(opex_var_eur_mwh_el=0.0)["valido"] is True
        assert self._val(capex_retrofit_eur=0.0)["valido"] is True
        assert self._val(wacc_frac=0.0)["valido"] is True
        assert self._val(tolleranza_frac=0.0)["valido"] is True


class TestFunzioni:
    def test_e_el_demo(self):
        assert _F["mh725_e_el"](100.0, 6000.0) == pytest.approx(
            E_EL_DEMO, rel=REL)

    def test_eta_mix_demo(self):
        assert _F["mh725_eta_mix"](0.55, 0.02, 0.30) == pytest.approx(
            ETA_MIX_DEMO, rel=REL)

    def test_eta_mix_fraz_zero_uguale_base(self):
        assert _F["mh725_eta_mix"](0.55, 0.02, 0.0) == pytest.approx(
            0.55, rel=REL)

    def test_eta_mix_fraz_uno(self):
        assert _F["mh725_eta_mix"](0.55, 0.02, 1.0) == pytest.approx(
            0.53, rel=REL)

    def test_eta_mix_rifiuta_non_positiva(self):
        with pytest.raises(ValueError):
            _F["mh725_eta_mix"](0.55, 0.60, 1.0)

    def test_e_fuel_mix_demo(self):
        assert _F["mh725_e_fuel_mix"](
            E_EL_DEMO, ETA_MIX_DEMO) == pytest.approx(
            E_FUEL_MIX_DEMO, rel=REL)

    def test_e_h2_demo(self):
        assert _F["mh725_e_h2"](
            E_FUEL_MIX_DEMO, 0.30) == pytest.approx(
            E_H2_DEMO, rel=REL)

    def test_e_gas_demo(self):
        assert _F["mh725_e_gas"](
            E_FUEL_MIX_DEMO, 0.30) == pytest.approx(
            E_GAS_DEMO, rel=REL)

    def test_split_somma_combustibile(self):
        assert _F["mh725_e_h2"](E_FUEL_MIX_DEMO, 0.30) + \
            _F["mh725_e_gas"](E_FUEL_MIX_DEMO, 0.30) == pytest.approx(
            E_FUEL_MIX_DEMO, rel=REL)

    def test_e_fuel_base_demo(self):
        assert _F["mh725_e_fuel_base"](
            E_EL_DEMO, 0.55) == pytest.approx(
            E_FUEL_BASE_DEMO, rel=REL)

    def test_costo_comb_mix_demo(self):
        assert _F["mh725_costo_comb_mix"](
            E_GAS_DEMO, 40.0, E_H2_DEMO, 50.0) == pytest.approx(
            COSTO_COMB_MIX_DEMO, rel=REL)

    def test_ets_mix_demo(self):
        assert _F["mh725_ets_mix"](
            E_GAS_DEMO, 0.202, 90.0) == pytest.approx(
            ETS_MIX_DEMO, rel=REL)

    def test_costo_totale_demo_mix(self):
        assert _F["mh725_costo_totale"](
            2000000.0, 3.0, E_EL_DEMO,
            COSTO_COMB_MIX_DEMO, ETS_MIX_DEMO) == pytest.approx(
            COSTO_MIX_DEMO, rel=REL)

    def test_ricavi_demo(self):
        assert _F["mh725_ricavi"](
            E_EL_DEMO, 120.0) == pytest.approx(
            RIC_DEMO, rel=REL)

    def test_margine_mix_demo(self):
        assert _F["mh725_margine"](
            RIC_DEMO, COSTO_MIX_DEMO) == pytest.approx(
            MARGINE_MIX_DEMO, rel=REL)

    def test_margine_puo_essere_negativo(self):
        assert _F["mh725_margine"](
            1000000.0, 2000000.0) == pytest.approx(
            -1000000.0, rel=REL)

    def test_margine_incr_demo(self):
        assert _F["mh725_margine_incr"](
            MARGINE_MIX_DEMO, MARGINE_BASE_DEMO) == pytest.approx(
            MARGINE_INCR_DEMO, rel=REL)

    def test_margine_incr_zero_se_casi_uguali(self):
        assert _F["mh725_margine_incr"](
            5000000.0, 5000000.0) == pytest.approx(0.0, abs=1e-9)

    def test_flussi_demo_incrementali(self):
        flussi = _F["mh725_flussi"](CAPEX_DEMO, MARGINE_INCR_DEMO,
                                     VITA_DEMO)
        assert len(flussi) == VITA_DEMO + 1
        assert flussi[0] == pytest.approx(-CAPEX_DEMO, rel=REL)
        assert all(f == pytest.approx(MARGINE_INCR_DEMO, rel=REL)
                   for f in flussi[1:])

    def test_van_flussi_demo(self):
        flussi = _F["mh725_flussi"](CAPEX_DEMO, MARGINE_INCR_DEMO,
                                     VITA_DEMO)
        assert abs(_F["mh725_van_flussi"](
            flussi, 0.06) - VAN_DEMO) <= 1.0

    def test_van_flussi_tasso_zero(self):
        flussi = _F["mh725_flussi"](CAPEX_DEMO, MARGINE_INCR_DEMO,
                                     VITA_DEMO)
        atteso = -CAPEX_DEMO + MARGINE_INCR_DEMO * VITA_DEMO
        assert _F["mh725_van_flussi"](
            flussi, 0.0) == pytest.approx(atteso, rel=1e-12)

    def test_van_flussi_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh725_van_flussi"]([100.0, 100.0], -0.01)

    def test_tir_demo(self):
        flussi = _F["mh725_flussi"](CAPEX_DEMO, MARGINE_INCR_DEMO,
                                     VITA_DEMO)
        tir = _F["mh725_tir_flussi"](flussi)
        assert tir is not None
        assert tir * 100.0 == pytest.approx(TIR_DEMO, rel=1e-9)

    def test_tir_none_tutti_flussi_non_negativi(self):
        assert _F["mh725_tir_flussi"](
            [0.0] + [MARGINE_INCR_DEMO] * 15) is None

    def test_tir_none_nessun_cambio_segno_negativo(self):
        assert _F["mh725_tir_flussi"](
            [-1000.0] + [-100.0] * 10) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh725_tir_flussi"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo_otto(self):
        flussi = _F["mh725_flussi"](CAPEX_DEMO, MARGINE_INCR_DEMO,
                                     VITA_DEMO)
        assert _F["mh725_payback_flussi"](flussi) == PAYBACK_DEMO

    def test_payback_none_se_mai(self):
        assert _F["mh725_payback_flussi"](
            [-100000000.0] + [MARGINE_INCR_DEMO] * 15) is None

    def test_payback_zero_se_cumulato_anno_zero_non_negativo(self):
        assert _F["mh725_payback_flussi"](
            [0.0] + [MARGINE_INCR_DEMO] * 15) == 0

    def test_verdetto_conviente_demo(self):
        assert _F["mh725_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10,
            MARGINE_INCR_DEMO) == VERDETTO_DEMO

    def test_verdetto_van_zero_conviente(self):
        assert _F["mh725_verdetto"](
            0.0, CAPEX_DEMO, 0.10, MARGINE_INCR_DEMO) == "CONVIENTE"

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh725_verdetto"](
            -100.0, CAPEX_DEMO, 0.10,
            MARGINE_INCR_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh725_verdetto"](
            -0.10 * CAPEX_DEMO, CAPEX_DEMO, 0.10,
            MARGINE_INCR_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_oltre_limite(self):
        assert _F["mh725_verdetto"](
            -0.10 * CAPEX_DEMO - 1.0, CAPEX_DEMO, 0.10,
            MARGINE_INCR_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_incr_non_positivo(self):
        assert _F["mh725_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh725_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_positivo_conviente(self):
        assert _F["mh725_verdetto"](
            1000.0, 0.0, 0.10, MARGINE_INCR_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(self):
        assert _F["mh725_verdetto"](
            -1.0, 0.0, 0.10, MARGINE_INCR_DEMO) == "NON_CONVIENTE"

    def test_verdetto_capex_zero_mai_marginale(self):
        for van in (-1.0, -100.0, -1000000.0):
            assert _F["mh725_verdetto"](
                van, 0.0, 0.10, MARGINE_INCR_DEMO) == "NON_CONVIENTE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh725_verdetto"](100.0, CAPEX_DEMO, -0.01,
                                 MARGINE_INCR_DEMO)

    def test_co2_emessa_mix_demo(self):
        assert _F["mh725_co2_emessa_mix"](
            E_GAS_DEMO, 0.202) == pytest.approx(
            CO2_MIX_DEMO, rel=REL)

    def test_co2_evitata_demo(self):
        assert _F["mh725_co2_evitata"](
            E_FUEL_BASE_DEMO, E_GAS_DEMO, 0.202) == pytest.approx(
            CO2_EVITATA_DEMO, rel=REL)

    def test_co2_evitata_zero_se_fattore_zero(self):
        assert _F["mh725_co2_evitata"](
            E_FUEL_BASE_DEMO, E_GAS_DEMO, 0.0) == pytest.approx(
            0.0, abs=1e-9)

    def test_co2_evitata_zero_se_gas_uguale_base(self):
        assert _F["mh725_co2_evitata"](
            E_FUEL_BASE_DEMO, E_FUEL_BASE_DEMO,
            0.202) == pytest.approx(0.0, abs=1e-9)

    def test_confronto_demo(self):
        df = _F["mh725_confronto"](
            E_EL_DEMO, E_FUEL_MIX_DEMO, E_GAS_DEMO, E_H2_DEMO,
            COSTO_COMB_MIX_DEMO, ETS_MIX_DEMO, 2000000.0, 3.0,
            COSTO_MIX_DEMO, RIC_DEMO, MARGINE_MIX_DEMO,
            E_FUEL_BASE_DEMO, COSTO_COMB_BASE_DEMO, ETS_BASE_DEMO,
            COSTO_BASE_DEMO, MARGINE_BASE_DEMO, MARGINE_INCR_DEMO,
            CO2_MIX_DEMO, CO2_BASE_DEMO, CO2_EVITATA_DEMO)
        assert list(df.columns) == ["Voce", "Mix",
                                    "Baseline gas 100 %",
                                    "Incrementale"]
        assert len(df) == 13
        voci = df["Voce"].tolist()
        assert "Margine (EUR/anno)" in voci
        assert "CO2 evitata vs baseline (t/anno)" in voci
        riga_marg = df[df["Voce"] == "Margine (EUR/anno)"].iloc[0]
        assert riga_marg["Incrementale"] == pytest.approx(
            MARGINE_INCR_DEMO, rel=REL)
        riga_ric = df[df["Voce"] == "Ricavi (EUR/anno)"].iloc[0]
        assert riga_ric["Incrementale"] == pytest.approx(
            0.0, abs=1e-9)
        riga_h2 = df[df["Voce"] == "Energia da H2 (MWh_th/anno)"].iloc[0]
        assert riga_h2["Baseline gas 100 %"] == pytest.approx(
            0.0, abs=1e-9)
        assert riga_h2["Incrementale"] == pytest.approx(
            E_H2_DEMO, rel=REL)


class TestDemo:
    def _bc(self, **kw):
        d = _F["mh725_demo"]()
        d.update(kw)
        return _F["mh725_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["e_el_mwh"] == pytest.approx(E_EL_DEMO, rel=REL)
        assert c["eta_mix"] == pytest.approx(ETA_MIX_DEMO, rel=REL)
        assert c["e_fuel_mix_mwh"] == pytest.approx(
            E_FUEL_MIX_DEMO, rel=REL)
        assert c["e_gas_mwh"] == pytest.approx(E_GAS_DEMO, rel=REL)
        assert c["e_h2_mwh"] == pytest.approx(E_H2_DEMO, rel=REL)
        assert c["costo_comb_mix_eur_anno"] == pytest.approx(
            COSTO_COMB_MIX_DEMO, rel=REL)
        assert c["ets_mix_eur_anno"] == pytest.approx(
            ETS_MIX_DEMO, rel=REL)
        assert c["costo_mix_eur_anno"] == pytest.approx(
            COSTO_MIX_DEMO, rel=REL)
        assert c["ricavi_eur_anno"] == pytest.approx(
            RIC_DEMO, rel=REL)
        assert c["margine_mix_eur_anno"] == pytest.approx(
            MARGINE_MIX_DEMO, rel=REL)
        assert c["e_fuel_base_mwh"] == pytest.approx(
            E_FUEL_BASE_DEMO, rel=REL)
        assert c["costo_comb_base_eur_anno"] == pytest.approx(
            COSTO_COMB_BASE_DEMO, rel=REL)
        assert c["ets_base_eur_anno"] == pytest.approx(
            ETS_BASE_DEMO, rel=REL)
        assert c["costo_base_eur_anno"] == pytest.approx(
            COSTO_BASE_DEMO, rel=REL)
        assert c["margine_base_eur_anno"] == pytest.approx(
            MARGINE_BASE_DEMO, rel=REL)
        assert c["margine_incr_eur_anno"] == pytest.approx(
            MARGINE_INCR_DEMO, rel=REL)
        assert c["co2_emessa_mix_t_anno"] == pytest.approx(
            CO2_MIX_DEMO, rel=REL)
        assert c["co2_emessa_base_t_anno"] == pytest.approx(
            CO2_BASE_DEMO, rel=REL)
        assert c["co2_evitata_t_anno"] == pytest.approx(
            CO2_EVITATA_DEMO, rel=REL)
        assert abs(c["van"] - VAN_DEMO) <= 1.0
        assert abs(c["tir"] - TIR_DEMO) <= 0.01
        assert c["payback"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO
        assert c["flussi"][0] == pytest.approx(-CAPEX_DEMO, rel=REL)
        assert all(f == pytest.approx(MARGINE_INCR_DEMO, rel=REL)
                   for f in c["flussi"][1:])
        assert len(c["flussi"]) == VITA_DEMO + 1

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()[
            "van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()[
            "margine_incr_eur_anno"] == _F["demo_calcoli"]()[
            "margine_incr_eur_anno"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        d = _F["mh725_demo"]()
        b = _F["mh725_calcola"](**d)
        coppie = [("e_el_mwh", E_EL_DEMO),
                  ("eta_mix", ETA_MIX_DEMO),
                  ("e_fuel_mix_mwh", E_FUEL_MIX_DEMO),
                  ("e_gas_mwh", E_GAS_DEMO),
                  ("e_h2_mwh", E_H2_DEMO),
                  ("costo_comb_mix_eur_anno", COSTO_COMB_MIX_DEMO),
                  ("ets_mix_eur_anno", ETS_MIX_DEMO),
                  ("costo_mix_eur_anno", COSTO_MIX_DEMO),
                  ("ricavi_eur_anno", RIC_DEMO),
                  ("margine_mix_eur_anno", MARGINE_MIX_DEMO),
                  ("e_fuel_base_mwh", E_FUEL_BASE_DEMO),
                  ("costo_base_eur_anno", COSTO_BASE_DEMO),
                  ("margine_base_eur_anno", MARGINE_BASE_DEMO),
                  ("margine_incr_eur_anno", MARGINE_INCR_DEMO),
                  ("co2_emessa_mix_t_anno", CO2_MIX_DEMO),
                  ("co2_evitata_t_anno", CO2_EVITATA_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert abs(b["van"] - VAN_DEMO) <= 1.0
        assert abs(b["tir"] - TIR_DEMO) <= 0.01
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh725_demo"]()
        assert d["p_nom_mw"] == 100.0
        assert d["ore_annue"] == 6000.0
        assert d["eta_base"] == 0.55
        assert d["delta_eta"] == 0.02
        assert d["fraz_h2"] == 0.30
        assert d["prezzo_gas_eur_mwh_th"] == 40.0
        assert d["prezzo_h2_eur_mwh_th"] == 50.0
        assert d["prezzo_elettricita_eur_mwh_el"] == 120.0
        assert d["fattore_co2_gas_t_mwh_th"] == 0.202
        assert d["prezzo_ets_eur_t"] == 90.0
        assert d["opex_fisso_eur_anno"] == 2000000.0
        assert d["opex_var_eur_mwh_el"] == 3.0
        assert d["capex_retrofit_eur"] == 15000000.0
        assert d["vita_anni"] == 15
        assert d["wacc_frac"] == 0.06
        assert d["tolleranza_frac"] == 0.10
        assert len(d) == 16

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("e_el_mwh", "eta_mix",
                       "e_fuel_mix_mwh", "e_gas_mwh",
                       "e_h2_mwh",
                       "costo_comb_mix_eur_anno",
                       "ets_mix_eur_anno",
                       "ricavi_eur_anno",
                       "margine_mix_eur_anno",
                       "e_fuel_base_mwh",
                       "costo_comb_base_eur_anno",
                       "ets_base_eur_anno",
                       "costo_base_eur_anno",
                       "margine_base_eur_anno",
                       "margine_incr_eur_anno",
                       "co2_emessa_mix_t_anno",
                       "co2_emessa_base_t_anno",
                       "co2_evitata_t_anno", "van"):
            assert repr(c[chiave]) in doc, chiave
        assert f"tir = {repr(c['tir'])}" in doc
        assert "payback = 8" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_prezzo_elettricita_non_muove_incrementale(self):
        # Nel confronto incrementale puro i ricavi
        # si elidono: prezzo elettricita' 200 lascia
        # invariati margine incrementale, VAN, TIR,
        # payback e verdetto (ma non il margine mix).
        n = self._bc(prezzo_elettricita_eur_mwh_el=200.0)
        assert n["valid"] is True
        assert n["margine_incr_eur_anno"] == pytest.approx(
            MARGINE_INCR_DEMO, rel=REL)
        assert abs(n["van"] - VAN_DEMO) <= 1.0
        assert abs(n["tir"] - TIR_DEMO) <= 0.01
        assert n["payback"] == PAYBACK_DEMO
        assert n["verdetto"] == VERDETTO_DEMO
        assert n["margine_mix_eur_anno"] == pytest.approx(
            MARGINE_MIX_DEMO + E_EL_DEMO * 80.0, rel=REL)

    def test_capex_20m_marginale(self):
        # CAPEX 20000000: VAN -511489,47, TIR
        # 5,61 %, payback 10 -> MARGINALE (|VAN|
        # <= 10 % di CAPEX = 2000000).
        n = self._bc(capex_retrofit_eur=20000000.0)
        assert n["valid"] is True
        assert n["margine_incr_eur_anno"] == pytest.approx(
            MARGINE_INCR_DEMO, rel=REL)
        assert abs(n["van"] - (-511489.47437151347)) <= 1.0
        assert abs(n["tir"] - 5.606140533539188) <= 0.01
        assert n["payback"] == 10
        assert n["verdetto"] == "MARGINALE"

    def test_capex_22m_non_conviente(self):
        # CAPEX 22000000: VAN -2511489,47, TIR
        # 4,20 %, payback 11 -> NON_CONVIENTE
        # (fuori tolleranza: 10 % di 22000000 =
        # 2200000 < |VAN|).
        n = self._bc(capex_retrofit_eur=22000000.0)
        assert n["valid"] is True
        assert abs(n["van"] - (-2511489.474371515)) <= 1.0
        assert abs(n["tir"] - 4.200828122197945) <= 0.01
        assert n["payback"] == 11
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_capex_zero_tir_none_payback_zero(self):
        # CAPEX 0: tutti i flussi >= 0 -> TIR None,
        # payback 0, VAN 19488510,53 -> CONVIENTE.
        n = self._bc(capex_retrofit_eur=0.0)
        assert n["valid"] is True
        assert n["tir"] is None
        assert n["payback"] == 0
        assert abs(n["van"] - 19488510.525628485) <= 1.0
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_enorme_payback_none(self):
        # CAPEX 100000000: VAN -80511489,47, TIR
        # -12,26 %, payback None -> NON_CONVIENTE.
        n = self._bc(capex_retrofit_eur=100000000.0)
        assert n["valid"] is True
        assert n["payback"] is None
        assert abs(n["van"] - (-80511489.47437151)) <= 1.0
        assert abs(n["tir"] - (-12.256023219728549)) <= 0.01
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_prezzo_h2_52_non_conviente(self):
        # Prezzo H2 52 EUR/MWh_th: margine
        # incrementale 1344826,20, VAN -1938713,07,
        # TIR 3,95 %, payback 12 -> NON_CONVIENTE.
        n = self._bc(prezzo_h2_eur_mwh_th=52.0)
        assert n["valid"] is True
        assert n["margine_incr_eur_anno"] == pytest.approx(
            1344826.2032085583, rel=REL)
        assert abs(n["van"] - (-1938713.069200133)) <= 1.0
        assert abs(n["tir"] - 3.9544834514753657) <= 0.01
        assert n["payback"] == 12
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_prezzo_h2_60_incr_negativo_neutro(self):
        # Prezzo H2 60: margine incrementale
        # negativo -> dict neutro NON_CALCOLABILE.
        n = self._bc(prezzo_h2_eur_mwh_th=60.0)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["margine_incr_eur_anno"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_fraz_zero_neutro(self):
        # Frazione H2 0: mix e baseline
        # coincidono, margine incrementale 0 ->
        # dict neutro NON_CALCOLABILE.
        n = self._bc(fraz_h2=0.0)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["margine_incr_eur_anno"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_fraz_uno_conviente(self):
        # Frazione H2 1: eta_mix 0,53, margine
        # incrementale 6865317,32, VAN 51677671,23,
        # TIR 45,61 %, payback 3 -> CONVIENTE.
        n = self._bc(fraz_h2=1.0)
        assert n["valid"] is True
        assert n["eta_mix"] == pytest.approx(0.53, rel=REL)
        assert n["e_gas_mwh"] == pytest.approx(0.0, abs=1e-9)
        assert n["margine_incr_eur_anno"] == pytest.approx(
            6865317.324185245, rel=REL)
        assert abs(n["van"] - 51677671.232338786) <= 1.0
        assert abs(n["tir"] - 45.60551379799852) <= 0.01
        assert n["payback"] == 3
        assert n["verdetto"] == "CONVIENTE"

    def test_vita_10_marginale(self):
        # Vita 10 anni: VAN -231316,23, TIR
        # 5,67 %, payback 8 -> MARGINALE (|VAN|
        # <= 10 % di CAPEX = 1500000).
        n = self._bc(vita_anni=10)
        assert n["valid"] is True
        assert abs(n["van"] - (-231316.23251352273)) <= 1.0
        assert abs(n["tir"] - 5.6732904837244265) <= 0.01
        assert n["payback"] == 8
        assert n["verdetto"] == "MARGINALE"

    def test_ets_zero_incr_negativo_neutro(self):
        # Senza ETS non c'e' risparmio ETS a
        # compensare l'H2 piu' caro: margine
        # incrementale negativo -> neutro.
        n = self._bc(prezzo_ets_eur_t=0.0)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_delta_zero_conviente(self):
        # Senza perdita di rendimento il margine
        # incrementale sale a 2677090,91, VAN
        # 11000573,47, TIR 15,89 %, payback 6.
        n = self._bc(delta_eta=0.0)
        assert n["valid"] is True
        assert n["eta_mix"] == pytest.approx(0.55, rel=REL)
        assert n["margine_incr_eur_anno"] == pytest.approx(
            2677090.9090909213, rel=REL)
        assert abs(n["van"] - 11000573.471908888) <= 1.0
        assert abs(n["tir"] - 15.89463377638668) <= 0.01
        assert n["payback"] == 6
        assert n["verdetto"] == "CONVIENTE"

    def test_p_nom_zero_neutro(self):
        n = self._bc(p_nom_mw=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_base_zero_neutro(self):
        n = self._bc(eta_base=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_base_sopra_uno_neutro(self):
        n = self._bc(eta_base=1.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_mix_non_positiva_neutro(self):
        n = self._bc(eta_base=0.55, delta_eta=0.60, fraz_h2=1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert "miscela" in n["errore"]

    def test_fraz_fuori_intervallo_neutro(self):
        assert self._bc(fraz_h2=1.5)["verdetto"] == "NON_CALCOLABILE"
        assert self._bc(fraz_h2=-0.1)["verdetto"] == "NON_CALCOLABILE"

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_negativo_neutro(self):
        n = self._bc(wacc_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_negativa_neutro(self):
        n = self._bc(tolleranza_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(eta_base=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["margine_incr_eur_anno"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(p_nom_mw=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(vita_anni=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_zero_calcolabile(self):
        # WACC 0: VAN = somma flussi =
        # -15000000 + 2006590,9090909138 x 15 =
        # 15098863,636363707.
        n = self._bc(wacc_frac=0.0)
        assert n["van"] == pytest.approx(
            15098863.636363707, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh725_neutro"]()
        assert n["valid"] is False
        assert n["errore"] == ""
        assert list(n["df_confronto"].columns) == ["Voce", "Mix",
                                                  "Baseline gas 100 %",
                                                  "Incrementale"]
        assert len(n["df_confronto"]) == 0
        assert list(n["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(n["df_flussi"]) == 0
        assert list(n["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(n["df_tabella"]) == 0
        assert n["flussi"] == []
        assert n["tir"] is None
        assert n["payback"] is None

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh725_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "p_nom_mw", "ore_annue",
                       "eta_base", "delta_eta",
                       "fraz_h2",
                       "prezzo_gas_eur_mwh_th",
                       "prezzo_h2_eur_mwh_th",
                       "prezzo_elettricita_eur_mwh_el",
                       "fattore_co2_gas_t_mwh_th",
                       "prezzo_ets_eur_t",
                       "opex_fisso_eur_anno",
                       "opex_var_eur_mwh_el",
                       "capex_retrofit_eur",
                       "vita_anni", "wacc_frac",
                       "tolleranza_frac",
                       "e_el_mwh", "eta_mix",
                       "e_fuel_mix_mwh", "e_gas_mwh",
                       "e_h2_mwh",
                       "costo_comb_mix_eur_anno",
                       "ets_mix_eur_anno",
                       "costo_mix_eur_anno",
                       "ricavi_eur_anno",
                       "margine_mix_eur_anno",
                       "e_fuel_base_mwh",
                       "costo_comb_base_eur_anno",
                       "ets_base_eur_anno",
                       "costo_base_eur_anno",
                       "margine_base_eur_anno",
                       "margine_incr_eur_anno",
                       "co2_emessa_mix_t_anno",
                       "co2_emessa_base_t_anno",
                       "co2_evitata_t_anno", "flussi",
                       "van", "tir", "payback",
                       "verdetto", "df_confronto",
                       "df_flussi", "df_tabella"):
            assert chiave in n, chiave
        assert n["errore"] == "errore di prova"
        assert n["tir"] is None

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert b["valid"] is True
        assert list(b["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(b["df_tabella"]) == 36
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Potenza nominale (MW)" in voci
        assert "Rendimento miscela" in voci
        assert "Energia da H2 (MWh_th/anno)" in voci
        assert "Margine incrementale (EUR/anno)" in voci
        assert "CO2 evitata vs baseline (t/anno)" in voci
        assert "VAN incrementale (EUR)" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(b["df_flussi"]) == VITA_DEMO + 1
        assert b["df_flussi"]["Flusso (€/anno)"].iloc[0] == \
            pytest.approx(-CAPEX_DEMO, rel=REL)
        assert b["df_flussi"]["Flusso (€/anno)"].iloc[1] == \
            pytest.approx(MARGINE_INCR_DEMO, rel=REL)
        assert b["df_flussi"]["Flusso (€/anno)"].iloc[15] == \
            pytest.approx(MARGINE_INCR_DEMO, rel=REL)
        assert list(b["df_confronto"].columns) == ["Voce", "Mix",
                                                  "Baseline gas 100 %",
                                                  "Incrementale"]
        assert len(b["df_confronto"]) == 13


class TestSensitivita:
    def _ing(self):
        return _F["mh725_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh725_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.9", "x1.0", "x1.1"]
        assert list(s.index) == ["x0.9", "x1.0", "x1.1"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh725_sensitivita"](self._ing())
        assert abs(s.loc["x1.0", "x1.0"] - VAN_DEMO) <= 1.0

    def test_sensitivita_crescente_con_prezzo_elettricita(self):
        s = _F["mh725_sensitivita"](self._ing())
        for riga in ("x0.9", "x1.0", "x1.1"):
            assert s.loc[riga, "x0.9"] < \
                s.loc[riga, "x1.0"] < \
                s.loc[riga, "x1.1"]

    def test_sensitivita_decrescente_con_prezzo_h2(self):
        s = _F["mh725_sensitivita"](self._ing())
        for colonna in ("x0.9", "x1.0", "x1.1"):
            assert s.loc["x0.9", colonna] > \
                s.loc["x1.0", colonna] > \
                s.loc["x1.1", colonna]

    def test_sensitivita_nessuna_colonna_degenere(self):
        s = _F["mh725_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_nessuna_colonna_costante(self):
        s = _F["mh725_sensitivita"](self._ing())
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3

    def test_sensitivita_angoli(self):
        s = _F["mh725_sensitivita"](self._ing())
        assert abs(s.loc["x0.9", "x0.9"] - (-49371623.19903512)) <= 1.0
        assert abs(s.loc["x0.9", "x1.1"] - 90484762.22443503) <= 1.0
        assert abs(s.loc["x1.1", "x0.9"] - (-81507741.17317806)) <= 1.0
        assert abs(s.loc["x1.1", "x1.1"] - 58348644.25029209) <= 1.0

    def test_sensitivita_centro_con_vita_corta(self):
        # Con vita 10 anni il centro deve
        # coincidere col VAN del caso con vita
        # 10 anni (flussi incrementali piatti,
        # nessun altro effetto).
        ing = self._ing()
        ing["vita_anni"] = 10
        s = _F["mh725_sensitivita"](ing)
        b = _F["mh725_calcola"](**ing)
        assert abs(s.loc["x1.0", "x1.0"] - b["van"]) <= 1.0


class TestCsv:
    def _ing(self):
        return _F["mh725_demo"]()

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh725_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") == 40

    def test_csv_contiene_verdetto_e_margini(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh725_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "margine_incr_eur_anno" in txt
        assert "margine_mix_eur_anno" in txt
        assert "margine_base_eur_anno" in txt
        assert "ricavi_eur_anno" in txt
        assert "costo_mix_eur_anno" in txt
        assert "costo_base_eur_anno" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "p_nom_mw" in txt
        assert "e_fuel_mix_mwh" in txt
        assert "e_h2_mwh" in txt
        assert "co2_evitata_t_anno" in txt
        assert "capex_retrofit_eur" in txt
        assert "fattore_co2_gas_t_mwh_th" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh725_csv"](bc, self._ing())
        assert f"margine_incr_eur_anno;{bc['margine_incr_eur_anno']}" in txt
        assert f"ricavi_eur_anno;{bc['ricavi_eur_anno']}" in txt
        assert "p_nom_mw;100.0" in txt
        assert "opex_fisso_eur_anno;2000000.0" in txt
        assert f"e_h2_mwh;{bc['e_h2_mwh']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def725["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def725\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 16, ui_keys
        demo_keys = set(_F["mh725_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh725_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh725_demo():")
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
        ui_keys = set(re.findall(r'_def725\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W726 (26/10/2026) - tab725' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh725_num", "mh725_nneg", "mh725_pos",
                     "mh725_int_pos", "mh725_eta_valida",
                     "mh725_fraz_valida", "mh725_e_el",
                     "mh725_eta_mix", "mh725_e_fuel_mix",
                     "mh725_e_h2", "mh725_e_gas",
                     "mh725_e_fuel_base",
                     "mh725_costo_comb_mix", "mh725_ets_mix",
                     "mh725_costo_totale", "mh725_ricavi",
                     "mh725_margine", "mh725_margine_incr",
                     "mh725_flussi", "mh725_van_flussi",
                     "mh725_tir_flussi",
                     "mh725_payback_flussi", "mh725_verdetto",
                     "mh725_co2_emessa_mix", "mh725_co2_evitata",
                     "mh725_confronto", "mh725_valida",
                     "_mh725_neutro", "mh725_calcola",
                     "mh725_sensitivita", "mh725_csv",
                     "mh725_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_nessun_identificatore_futura_tab(self):
        assert "mh726" not in _helpers_src()
        assert "mh726" not in _ui_src()
        assert "st726" not in _ui_src()
        assert "tab726" not in _ui_src()

    def test_helpers_parse_ast(self):
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w726_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE725) == 1

    def test_blocco_with_tab725(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab725:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE725

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st725_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 21, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st725_") for k in keys)

    def test_chiavi_st_input_sono_17(self):
        """Le 17 chiavi di input/bottone (16 input +
        bottone calcola) sono tutte presenti; le
        altre 4 sono solo chiavi di
        visualizzazione (fig, heatmap, flussi, CSV)."""
        keys = re.findall(r'key="(st725_[a-z0-9_]+)"', _ui_src())
        attese = ["st725_p_nom", "st725_ore",
                  "st725_eta_base", "st725_delta_eta",
                  "st725_fraz_h2", "st725_prezzo_gas",
                  "st725_prezzo_h2", "st725_prezzo_elec",
                  "st725_fattore_co2", "st725_prezzo_ets",
                  "st725_opex_fisso", "st725_opex_var",
                  "st725_capex", "st725_vita",
                  "st725_wacc", "st725_tolleranza",
                  "st725_calcola"]
        assert len(attese) == 17
        for k in attese:
            assert k in keys, k

    def test_chiavi_st_niente_fstring_dinamiche(self):
        src = _ui_src()
        assert 'key=f"' not in src
        assert "key=f'" not in src

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg725" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg725") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg725")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Energia annua (MWh/anno)" in src
        assert "Margine incrementale annuo (€/anno)" in src
        assert "VAN incrementale (€)" in src
        assert "CO2 evitata vs baseline (t/anno)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_presente(self):
        src = _ui_src().lower()
        assert "tab621" in src
        assert "spark spread" in src
        assert "unit commitment" in src
        assert "incrementale" in src
        assert "upstream" in src

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert '"Costo combustibile"' in src
        assert '"Costo ETS"' in src
        assert '"Costo totale"' in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh725_csv" in src
        assert "h2_ready_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN incrementale" in src
        assert "mh725_sensitivita" in src
        assert "Heatmap" in src
        assert "Fattore prezzo H2" in src
        assert "Fattore prezzo elettricità" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st725_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W726 (26/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab725:")
