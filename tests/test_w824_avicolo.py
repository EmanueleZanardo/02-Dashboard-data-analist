"""Test nuova scheda tab824 "Allevamento avicolo /
pollaio da carne: ventilazione con inverter +
raffrescamento evaporativo + recupero calore aria
esausta battono ventilazione on/off +
raffrescamento tradizionale + riscaldamento a gas?".

Business case deterministico di un pollaio da carne
guidato dai CAPI AVICOLI allevati/anno:
E_vent_base = capi x e_vent_base; E_vent_alt = capi x
e_vent_alt (l'inverter riduce solo la ventilazione);
E_raff_base = capi x e_raff_base; E_raff_alt = capi x
e_raff_alt (l'evaporativo riduce solo il
raffrescamento); E_base = E_vent_base + E_raff_base;
E_alt = E_vent_alt + E_raff_alt; gas_base = capi x
g_base; gas_alt = capi x g_alt (il recupero calore
RIDUCE il gas, non lo azzera: gas_alt resta positivo
nel demo); C_base = E_base x p_el + gas_base x p_gas
+ OM_base; C_alt = E_alt x p_el + gas_alt x p_gas
+ OM_alt (prezzi in EUR/kWh, nessuna conversione
/ 1000); risparmio = C_base - C_alt; CO2 evitata =
(E_base x 0,25 + gas_base x 0,202 - E_alt x 0,25 -
gas_alt x 0,202) / 1000 (fattori letterali); flussi
[-CAPEX, risparmio x vita]; VAN, TIR, payback (primo
anno con cumulato >= 0); breakeven gas =
(E_alt x p_el + OM_alt - E_base x p_el - OM_base) /
(gas_base - gas_alt) EUR/kWh, None se gas_base <=
gas_alt o numeratore < 0, SOGLIA MINIMA quando
esiste. Nel demo il breakeven e' 0,05 EUR/kWh
(numeratore 5.000 EUR, denominatore 100.000
kWh/anno). Verdetto: NON_CALCOLABILE se input
degenere (capi <= 0, specifici negativi, prezzi <= 0,
O&M negativi, CAPEX <= 0, WACC negativo, vita <= 0,
tolleranza negativa) o se risparmio <= 0 (guard
degenere: UI salta KPI, grafico, tabella e CSV);
altrimenti CONVIENTE se VAN > 0, MARGINALE se VAN
negativa entro tolleranza % del CAPEX,
NON_CONVIENTE se VAN negativa oltre la tolleranza.
Guard UI IDENTICA agli helper: nessuna divergenza
di verdetto. Tutti gli slider UI hanno minimo 0,
quindi i casi negativi sono NON RAGGIUNGIBILI via
slider, ma la guard li controlla comunque; i casi
= 0 raggiungibili via slider sono bloccati in UI
esattamente come negli helper dove previsto (capi,
prezzi, CAPEX, vita). Gli zeri ammessi in entrambi
(specifici elettrici e gas, O&M, WACC, tolleranza)
non creano divergenza: con gas specifico base
uguale a gas specifico alternativo il breakeven e'
None, e il caso resta calcolabile in entrambi. WACC
sopra 20 % e tolleranza sopra 100 % sono ammessi
negli helper e limitati solo dagli slider UI
(20, 100): nessuna divergenza nel range
raggiungibile, perche' la guard controlla solo gli
stessi limiti degli helper.
Distinzione esplicita: distinto dalla porcilaia
(capi suini, acqua di lavaggio suina: qui niente
capi suini, niente acqua di lavaggio suina), dalla
sala mungitura (litri di latte, vuoto,
refrigerazione latte: qui niente litri di latte,
niente vuoto, niente refrigerazione latte), dal
mulino (tonnellate di cereale, macinazione,
pneumatico: qui niente cereali, niente macinazione,
niente pneumatico): qui driver CAPO AVICOLO +
VENTILAZIONE CON INVERTER + RAFFRESCAMENTO
EVAPORATIVO + RECUPERO CALORE ARIA ESAUSTA.

Demo (pollaio da carne): 40.000 capi avicoli,
ventilazione specifica base 4,0 (160.000
kWh_e/anno) e alternativa 2,8 (112.000
kWh_e/anno), raffrescamento specifico base 1,2
(48.000 kWh_e/anno) e alternativo 0,9 (36.000
kWh_e/anno), elettricita' base 208.000 e
alternativa 148.000 kWh_e/anno, gas specifico
base 3,5 (140.000 kWh/anno) e alternativo 1,0
(40.000 kWh/anno, il recupero riduce il gas del
71,4 %, non lo azzera), prezzi elettricita' 0,25
e gas 0,10 EUR/kWh, O&M base 12.000 e alternativo
32.000 EUR/anno, CAPEX 30.000 EUR, WACC 5 %,
vita 15 anni, tolleranza 10 % del CAPEX. Valori
calcolati eseguendo mh824_demo_calcoli(): E_base
208.000, E_alt 148.000, gas_base 140.000, gas_alt
40.000, C_base 78.000, C_alt 73.000, risparmio
5.000, CO2_base 80,28, CO2_alt 45,08, CO2_evitata
35,20, VAN 21898,290190902957, TIR
14,47206297262965 %, payback 6, breakeven gas
0,05 EUR/kWh, verdetto CONVIENTE.
"""

import ast
import inspect
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w826_helpers import (
    demo_calcoli,
    mh824_breakeven_gas,
    mh824_c_alt,
    mh824_c_base,
    mh824_calcola,
    mh824_co2_alt,
    mh824_co2_base,
    mh824_co2_evitata,
    mh824_csv,
    mh824_demo,
    mh824_demo_calcoli,
    mh824_e_alt,
    mh824_e_base,
    mh824_e_raff_alt,
    mh824_e_raff_base,
    mh824_e_vent_alt,
    mh824_e_vent_base,
    mh824_flussi,
    mh824_gas_alt,
    mh824_gas_base,
    mh824_int_pos,
    mh824_nneg,
    mh824_num,
    mh824_payback,
    mh824_pos,
    mh824_risparmio,
    mh824_tir,
    mh824_valida,
    mh824_van,
    mh824_verdetto,
)

_DEMO = {
    "e_vent_base_kwh_e_anno": 160000.0,
    "e_vent_alt_kwh_e_anno": 112000.0,
    "e_raff_base_kwh_e_anno": 48000.0,
    "e_raff_alt_kwh_e_anno": 36000.0,
    "e_base_kwh_e_anno": 208000.0,
    "e_alt_kwh_e_anno": 148000.0,
    "gas_base_kwh_anno": 140000.0,
    "gas_alt_kwh_anno": 40000.0,
    "c_base_eur_anno": 78000.0,
    "c_alt_eur_anno": 73000.0,
    "risparmio_eur_anno": 5000.0,
    "co2_base_t_anno": 80.28,
    "co2_alt_t_anno": 45.08,
    "co2_evitata_t_anno": 35.2,
    "van": 21898.290190902957,
    "tir": 14.47206297262965,
}


def _demo_kwargs():
    return dict(mh824_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh824_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh824_num(3, "x") == 3.0
    assert mh824_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh824_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh824_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh824_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh824_pos(0, "x")
    with pytest.raises(ValueError):
        mh824_pos(-1, "x")
    assert mh824_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh824_int_pos(5.0, "x") == 5
    assert mh824_int_pos(15.0, "x") == 15
    with pytest.raises(ValueError):
        mh824_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh824_int_pos(0, "x")


# ---------------------------------------------------------------- fisica base
def test_e_vent_e_raff_e_base():
    assert mh824_e_vent_base(40000, 4.0) == 160000.0
    assert mh824_e_vent_alt(40000, 2.8) == 112000.0
    assert mh824_e_raff_base(40000, 1.2) == 48000.0
    assert mh824_e_raff_alt(40000, 0.9) == 36000.0
    assert mh824_e_base(160000.0, 48000.0) == 208000.0
    with pytest.raises(ValueError):
        mh824_e_base(-1, 48000.0)
    with pytest.raises(ValueError):
        mh824_e_vent_base(0, 4.0)


def test_e_alt():
    assert mh824_e_alt(112000.0, 36000.0) == 148000.0
    with pytest.raises(ValueError):
        mh824_e_alt(112000.0, -1)
    with pytest.raises(ValueError):
        mh824_e_vent_alt(0, 2.8)


def test_gas_base_alt():
    assert mh824_gas_base(40000, 3.5) == 140000.0
    assert mh824_gas_alt(40000, 1.0) == 40000.0
    assert mh824_gas_alt(40000, 0) == 0.0
    with pytest.raises(ValueError):
        mh824_gas_base(40000, -1)
    with pytest.raises(ValueError):
        mh824_gas_base(0, 3.5)


def test_c_base_c_alt_scomposizione():
    assert mh824_c_base(208000.0, 0.25, 140000.0, 0.10,
                        12000) == pytest.approx(78000.0)
    assert mh824_c_alt(148000.0, 0.25, 40000.0, 0.10,
                       32000) == pytest.approx(73000.0)
    with pytest.raises(ValueError):
        mh824_c_base(208000.0, 0, 140000.0, 0.10, 12000)
    with pytest.raises(ValueError):
        mh824_c_alt(148000.0, 0.25, 40000.0, 0, 32000)
    with pytest.raises(ValueError):
        mh824_c_base(208000.0, 0.25, 140000.0, 0.10, -1)


def test_risparmio_segno():
    assert mh824_risparmio(78000.0, 73000.0) == pytest.approx(5000.0)
    assert mh824_risparmio(73000.0, 73000.0) == pytest.approx(0.0, abs=1e-9)


def test_co2_base_alt_evitata():
    assert mh824_co2_base(208000.0, 140000.0) == pytest.approx(80.28)
    assert mh824_co2_alt(148000.0, 40000.0) == pytest.approx(45.08)
    assert mh824_co2_evitata(208000.0, 140000.0,
                             148000.0, 40000.0) == pytest.approx(35.2)
    assert mh824_co2_base(0, 0) == 0.0
    assert mh824_co2_alt(0, 0) == 0.0
    with pytest.raises(ValueError):
        mh824_co2_base(208000.0, -1)
    with pytest.raises(ValueError):
        mh824_co2_alt(-1, 0.0)


def test_breakeven_demo_valore():
    bc = mh824_demo_calcoli()
    assert bc["breakeven_gas_eur_kwh"] == pytest.approx(0.05)
    # Numeratore: 148000*0,25 + 32000 - 208000*0,25 - 12000 = 5000;
    # denominatore: 140000 - 40000 = 100000.
    assert mh824_breakeven_gas(148000.0, 0.25, 32000, 208000.0,
                               12000, 140000.0,
                               40000.0) == pytest.approx(0.05)
    assert mh824_breakeven_gas(148000.0, 0.25, 32000, 208000.0,
                               12000, 140000.0, 140000.0) is None
    assert mh824_breakeven_gas(148000.0, 0.25, 32000, 208000.0,
                               12000, 10000.0, 40000.0) is None
    assert _variante(g_alt_kwh_capo=3.5)["breakeven_gas_eur_kwh"] is None
    with pytest.raises(ValueError):
        mh824_breakeven_gas(148000.0, 0.25, 32000, 208000.0,
                            12000, -1, 40000.0)


def test_breakeven_numeratore_negativo_none():
    # Con O&M alternativo 0 il numeratore diventa negativo:
    # 148000*0,25 + 0 - 208000*0,25 - 12000 < 0.
    assert mh824_breakeven_gas(148000.0, 0.25, 0, 208000.0,
                               12000, 140000.0,
                               40000.0) is None
    assert _variante(om_alt=0)["breakeven_gas_eur_kwh"] is None


def test_breakeven_verifica_pareggio_su_demo():
    be = mh824_demo_calcoli()["breakeven_gas_eur_kwh"]
    bc = _variante(p_gas=be)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_breakeven_soglia_minima_su_demo():
    be = mh824_demo_calcoli()["breakeven_gas_eur_kwh"]
    bc_alto = _variante(p_gas=0.10)
    bc_basso = _variante(p_gas=0.04)
    assert bc_alto["c_alt_eur_anno"] < bc_alto["c_base_eur_anno"]
    assert bc_basso["c_alt_eur_anno"] > bc_basso["c_base_eur_anno"]
    assert bc_alto["risparmio_eur_anno"] > 0.0
    assert bc_basso["verdetto"] == "NON_CALCOLABILE"
    assert bc_alto["risparmio_eur_anno"] == pytest.approx(5000.0)
    assert bc_basso["risparmio_eur_anno"] == pytest.approx(-1000.0)
    assert bc_alto["verdetto"] == "CONVIENTE"
    assert be < 0.10


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh824_flussi(30000, 5000.0, 15)
    assert len(fl) == 16
    assert fl[0] == -30000
    assert all(f == pytest.approx(5000.0) for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh824_demo_calcoli()
    assert bc["van"] == pytest.approx(21898.290190902957)
    assert mh824_van([-30000] + [5000.0] * 15,
                     0) == pytest.approx(45000.0)
    assert mh824_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh824_demo_calcoli()
    assert bc["tir"] == pytest.approx(14.47206297262965)
    assert mh824_tir([-30000] + [5000.0] * 15) == \
        pytest.approx(0.1447206297262965)
    tir = mh824_tir([-30000] + [5000.0] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-30000] + [5000.0] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh824_payback([-30000] + [5000.0] * 15) == 6
    assert mh824_payback([-30000] + [-1000.0] * 15) is None
    assert mh824_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh824_verdetto(5000.0, 21898.290190902957, 30000,
                          10.0) == "CONVIENTE"
    assert mh824_verdetto(5000.0, -1500.0, 30000,
                          10.0) == "MARGINALE"
    assert mh824_verdetto(5000.0, -3000.0, 30000, 10.0) == "MARGINALE"
    assert mh824_verdetto(5000.0, -3000.01, 30000, 10.0) == "NON_CONVIENTE"
    assert mh824_verdetto(5000.0, 0.0, 30000, 10.0) == "MARGINALE"
    assert mh824_verdetto(0.0, 21898.29, 30000,
                          10.0) == "NON_CALCOLABILE"
    assert mh824_verdetto(-1000.0, -40379.66, 30000,
                          10.0) == "NON_CALCOLABILE"
    assert mh824_verdetto(None, 21898.29, 30000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh824_verdetto(float("nan"), 21898.29, 30000, 10.0)
    with pytest.raises(ValueError):
        mh824_verdetto(5000.0, 21898.29, 0, 10.0)
    with pytest.raises(ValueError):
        mh824_verdetto(5000.0, 21898.29, 30000, -1)


def test_valida_demo_ok():
    v = mh824_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("capi", "40000"),
                       ("capi", float("nan")),
                       ("capi", float("inf")),
                       ("capi", True),
                       ("p_gas", None),
                       ("g_base_kwh_capo", "3.5")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh824_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("capi", 0),
                          ("capi", -10),
                          ("e_vent_base_kwh_e_capo", -1),
                          ("e_vent_alt_kwh_e_capo", -1),
                          ("e_raff_base_kwh_e_capo", -1),
                          ("e_raff_alt_kwh_e_capo", -1),
                          ("g_base_kwh_capo", -1),
                          ("g_alt_kwh_capo", -1),
                          ("p_el", 0),
                          ("p_el", -1),
                          ("p_gas", 0),
                          ("p_gas", -1),
                          ("om_base", -100),
                          ("om_alt", -100),
                          ("capex", 0),
                          ("capex", -1),
                          ("wacc_pct", -0.1),
                          ("vita_anni", 0), ("vita_anni", 2.5),
                          ("tolleranza_pct", -1)):
        d = _demo_kwargs()
        d.update({campo: valore})
        assert mh824_valida(**d)["valido"] is False


def test_valida_accetta_limiti_e_nessun_tetto_wacc_tolleranza():
    d = _demo_kwargs()
    d.update({"e_vent_base_kwh_e_capo": 0,
              "e_vent_alt_kwh_e_capo": 0,
              "e_raff_base_kwh_e_capo": 0,
              "e_raff_alt_kwh_e_capo": 0,
              "g_base_kwh_capo": 0,
              "g_alt_kwh_capo": 0,
              "om_base": 0, "om_alt": 0,
              "wacc_pct": 0,
              "tolleranza_pct": 0})
    assert mh824_valida(**d)["valido"] is True
    d["wacc_pct"] = 60
    d["tolleranza_pct"] = 200
    assert mh824_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh824_demo()
    assert d["capi"] == 40000
    assert d["e_vent_base_kwh_e_capo"] == 4.0
    assert d["e_vent_alt_kwh_e_capo"] == 2.8
    assert d["e_raff_base_kwh_e_capo"] == 1.2
    assert d["e_raff_alt_kwh_e_capo"] == 0.9
    assert d["g_base_kwh_capo"] == 3.5
    assert d["g_alt_kwh_capo"] == 1.0
    assert d["p_el"] == 0.25
    assert d["p_gas"] == 0.10
    assert d["om_base"] == 12000
    assert d["om_alt"] == 32000
    assert d["capex"] == 30000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    bc = mh824_demo_calcoli()
    for chiave, atteso in _DEMO.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert got == pytest.approx(atteso, rel=1e-9), chiave
    assert bc["payback"] == 6
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True
    assert bc["breakeven_gas_eur_kwh"] == pytest.approx(0.05)
    assert demo_calcoli()["van"] == bc["van"]


def test_demo_calcoli_fisica_economia():
    bc = mh824_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(78000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(73000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(5000.0)
    assert bc["co2_base_t_anno"] == pytest.approx(80.28)
    assert bc["co2_alt_t_anno"] == pytest.approx(45.08)
    assert bc["co2_evitata_t_anno"] == pytest.approx(35.2)
    assert bc["gas_base_kwh_anno"] == pytest.approx(140000.0)
    assert bc["gas_alt_kwh_anno"] == pytest.approx(40000.0)
    assert bc["e_vent_base_kwh_e_anno"] == pytest.approx(160000.0)
    assert bc["e_vent_alt_kwh_e_anno"] == pytest.approx(112000.0)
    assert bc["e_raff_base_kwh_e_anno"] == pytest.approx(48000.0)
    assert bc["e_raff_alt_kwh_e_anno"] == pytest.approx(36000.0)
    assert bc["e_base_kwh_e_anno"] == pytest.approx(208000.0)
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(148000.0)


def test_demo_flussi_e_cumulato():
    bc = mh824_demo_calcoli()
    assert bc["flussi"][0] == -30000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(5000.0) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -30000
    assert righe.iloc[5]["Cumulato (EUR)"] == pytest.approx(-5000.0)
    assert righe.iloc[6]["Cumulato (EUR)"] == pytest.approx(0.0)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(45000.0)


def test_demo_tabella_righe():
    bc = mh824_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Ventilazione baseline (kWh_e/anno)"] == pytest.approx(160000.0)
    assert mappa["Ventilazione alternativa (kWh_e/anno)"] == pytest.approx(112000.0)
    assert mappa["Raffrescamento baseline (kWh_e/anno)"] == pytest.approx(48000.0)
    assert mappa["Raffrescamento alternativa (kWh_e/anno)"] == pytest.approx(36000.0)
    assert mappa["Elettricita' base (kWh_e/anno)"] == pytest.approx(208000.0)
    assert mappa["Elettricita' alternativa (kWh_e/anno)"] == pytest.approx(148000.0)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(140000.0)
    assert mappa["Gas alternativo (kWh/anno)"] == pytest.approx(40000.0)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(78000.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(73000.0)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(5000.0)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(35.2)
    assert mappa["Payback (anni)"] == 6
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/kWh)"] == pytest.approx(0.05)


def test_demo_coerenza_interna():
    bc = mh824_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["gas_base_kwh_anno"] == pytest.approx(
        bc["capi"] * bc["g_base_kwh_capo"])
    assert bc["gas_alt_kwh_anno"] == pytest.approx(
        bc["capi"] * bc["g_alt_kwh_capo"])
    assert bc["e_vent_base_kwh_e_anno"] == pytest.approx(
        bc["capi"] * bc["e_vent_base_kwh_e_capo"])
    assert bc["e_vent_alt_kwh_e_anno"] == pytest.approx(
        bc["capi"] * bc["e_vent_alt_kwh_e_capo"])
    assert bc["e_raff_base_kwh_e_anno"] == pytest.approx(
        bc["capi"] * bc["e_raff_base_kwh_e_capo"])
    assert bc["e_raff_alt_kwh_e_anno"] == pytest.approx(
        bc["capi"] * bc["e_raff_alt_kwh_e_capo"])
    assert bc["e_base_kwh_e_anno"] == pytest.approx(
        bc["e_vent_base_kwh_e_anno"] + bc["e_raff_base_kwh_e_anno"])
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(
        bc["e_vent_alt_kwh_e_anno"] + bc["e_raff_alt_kwh_e_anno"])
    assert bc["co2_evitata_t_anno"] == pytest.approx(
        bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])
    assert bc["c_base_eur_anno"] == pytest.approx(
        bc["e_base_kwh_e_anno"] * bc["p_el"]
        + bc["gas_base_kwh_anno"] * bc["p_gas"]
        + bc["om_base"])
    assert bc["c_alt_eur_anno"] == pytest.approx(
        bc["e_alt_kwh_e_anno"] * bc["p_el"]
        + bc["gas_alt_kwh_anno"] * bc["p_gas"]
        + bc["om_alt"])


def test_demo_contro_riconteggio_indipendente():
    cp, evb, eva = 40000, 4.0, 2.8
    erb, era, gab, gaa = 1.2, 0.9, 3.5, 1.0
    pel, pg = 0.25, 0.10
    omb, oma, cx = 12000, 32000, 30000
    wacc, vita = 5.0, 15
    e_vent_b = cp * evb
    e_vent_a = cp * eva
    e_raff_b = cp * erb
    e_raff_a = cp * era
    eb = e_vent_b + e_raff_b
    ea = e_vent_a + e_raff_a
    gasb = cp * gab
    gasa = cp * gaa
    cb = eb * pel + gasb * pg + omb
    ca = ea * pel + gasa * pg + oma
    risp = cb - ca
    co2b = (eb * 0.25 + gasb * 0.202) / 1000.0
    co2a = (ea * 0.25 + gasa * 0.202) / 1000.0
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    bc = mh824_demo_calcoli()
    assert bc["e_vent_base_kwh_e_anno"] == pytest.approx(e_vent_b)
    assert bc["e_vent_alt_kwh_e_anno"] == pytest.approx(e_vent_a)
    assert bc["e_raff_base_kwh_e_anno"] == pytest.approx(e_raff_b)
    assert bc["e_raff_alt_kwh_e_anno"] == pytest.approx(e_raff_a)
    assert bc["e_base_kwh_e_anno"] == pytest.approx(eb)
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(ea)
    assert bc["gas_base_kwh_anno"] == pytest.approx(gasb)
    assert bc["gas_alt_kwh_anno"] == pytest.approx(gasa)
    assert bc["c_base_eur_anno"] == pytest.approx(cb)
    assert bc["c_alt_eur_anno"] == pytest.approx(ca)
    assert bc["risparmio_eur_anno"] == pytest.approx(risp)
    assert bc["co2_base_t_anno"] == pytest.approx(co2b)
    assert bc["co2_alt_t_anno"] == pytest.approx(co2a)
    assert bc["co2_evitata_t_anno"] == pytest.approx(co2)
    assert bc["van"] == pytest.approx(van)
    assert bc["breakeven_gas_eur_kwh"] == pytest.approx(5000.0 / 100000.0)


def test_demo_verdetto_coerente_con_risparmio_e_van():
    bc = mh824_demo_calcoli()
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] > 0.0
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["tir"] is not None and bc["tir"] > bc["wacc_pct"]
    assert bc["payback"] == 6


# ---------------------------------------------------------------- varianti
def test_variante_senza_inverter_non_calcolabile():
    bc = _variante(e_vent_alt_kwh_e_capo=4.0)
    assert bc["e_vent_alt_kwh_e_anno"] == pytest.approx(160000.0)
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(196000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(85000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-7000.0)
    assert bc["van"] == pytest.approx(-102657.60626726414)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["breakeven_gas_eur_kwh"] == pytest.approx(0.17)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_senza_evaporativo_non_convinte():
    bc = _variante(e_raff_alt_kwh_e_capo=1.2)
    assert bc["e_raff_alt_kwh_e_anno"] == pytest.approx(48000.0)
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(160000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(76000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(2000.0)
    assert bc["van"] == pytest.approx(-9240.683923638824)
    assert bc["tir"] == pytest.approx(0.0, abs=1e-6)
    assert bc["payback"] == 15
    assert bc["breakeven_gas_eur_kwh"] == pytest.approx(0.08)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_senza_recupero_non_calcolabile():
    bc = _variante(g_alt_kwh_capo=3.5)
    assert bc["valid"] is True
    assert bc["gas_alt_kwh_anno"] == pytest.approx(140000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(83000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-5000.0)
    assert bc["van"] == pytest.approx(-81898.29019090292)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"]
    assert bc["payback"] is None
    assert bc["tir"] is None
    assert bc["breakeven_gas_eur_kwh"] is None


def test_variante_capex_60000_non_convinte():
    bc = _variante(capex=60000)
    assert bc["risparmio_eur_anno"] == pytest.approx(5000.0)
    assert bc["van"] == pytest.approx(-8101.7098090970485)
    assert bc["tir"] == pytest.approx(2.9283950062936666)
    assert bc["payback"] == 12
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_om_alt_34300_marginale():
    bc = _variante(om_alt=34300)
    assert bc["c_alt_eur_anno"] == pytest.approx(75300.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(2700.0)
    assert bc["van"] == pytest.approx(-1974.923296912408)
    assert bc["tir"] == pytest.approx(4.009363868950285)
    assert bc["payback"] == 12
    assert bc["breakeven_gas_eur_kwh"] == pytest.approx(0.073)
    assert bc["verdetto"] == "MARGINALE"


def test_variante_om_alt_40000_non_calcolabile():
    bc = _variante(om_alt=40000)
    assert bc["valid"] is True
    assert bc["c_alt_eur_anno"] == pytest.approx(81000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-3000.0)
    assert bc["van"] == pytest.approx(-61138.974114541765)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"]
    assert bc["payback"] is None
    assert bc["tir"] is None
    assert bc["breakeven_gas_eur_kwh"] == pytest.approx(0.13)


def test_variante_gas_basso_e_alto():
    bc_basso = _variante(p_gas=0.04)
    assert bc_basso["risparmio_eur_anno"] == pytest.approx(-1000.0)
    assert bc_basso["van"] == pytest.approx(-40379.65803818059)
    assert bc_basso["verdetto"] == "NON_CALCOLABILE"
    bc_alto = _variante(p_gas=0.20)
    assert bc_alto["risparmio_eur_anno"] == pytest.approx(15000.0)
    assert bc_alto["van"] == pytest.approx(125694.87057270884)
    assert bc_alto["tir"] == pytest.approx(49.88448999926908)
    assert bc_alto["payback"] == 2
    assert bc_alto["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(45000.0)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(8608.674645924058)
    assert bc2["tir"] == pytest.approx(10.557981604995739)
    assert bc2["payback"] == 6
    assert bc2["verdetto"] == "CONVIENTE"
    bc3 = _variante(vita_anni=5)
    assert bc3["van"] == pytest.approx(-8352.616646845901)
    assert bc3["payback"] is None
    assert bc3["verdetto"] == "NON_CONVIENTE"


def test_monotonia_prezzo_gas_crescente():
    base = mh824_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas=0.101)["risparmio_eur_anno"]
    basso = _variante(p_gas=0.099)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(100.0, abs=1e-6)
    assert base - basso == pytest.approx(100.0, abs=1e-6)


def test_monotonia_ventilazione_e_recupero():
    assert _variante(e_vent_alt_kwh_e_capo=3.0)["risparmio_eur_anno"] < \
        mh824_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(g_alt_kwh_capo=1.5)["risparmio_eur_anno"] < \
        mh824_demo_calcoli()["risparmio_eur_anno"]


def test_demo_deterministica_due_chiamate():
    a = mh824_demo_calcoli()
    b = mh824_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh824_demo().keys()) == {
        "capi", "e_vent_base_kwh_e_capo", "e_vent_alt_kwh_e_capo",
        "e_raff_base_kwh_e_capo", "e_raff_alt_kwh_e_capo",
        "g_base_kwh_capo", "g_alt_kwh_capo",
        "p_el", "p_gas", "om_base", "om_alt",
        "capex", "wacc_pct", "vita_anni",
        "tolleranza_pct"}


# ---------------------------------------------------------------- degenere
def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"capi": 0},
               {"capi": -10},
               {"e_vent_base_kwh_e_capo": -1},
               {"e_vent_alt_kwh_e_capo": -1},
               {"e_raff_base_kwh_e_capo": -1},
               {"e_raff_alt_kwh_e_capo": -1},
               {"g_base_kwh_capo": -1},
               {"g_alt_kwh_capo": -1},
               {"p_el": 0}, {"p_el": -1},
               {"p_gas": 0}, {"p_gas": -1},
               {"om_base": -100},
               {"om_alt": -100},
               {"capex": 0}, {"capex": -1},
               {"wacc_pct": -1},
               {"vita_anni": 0}, {"vita_anni": 2.5},
               {"tolleranza_pct": -1}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh824_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"capi": "40000"},
               {"capi": float("nan")},
               {"p_gas": float("inf")},
               {"capex": True},
               {"g_base_kwh_capo": "3.5"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh824_valida(**d)["valido"] is False


def test_zeri_ammessi_non_sollevano_e_nessuna_divergenza():
    for kw in ({"e_vent_base_kwh_e_capo": 0},
               {"e_vent_alt_kwh_e_capo": 0},
               {"e_raff_base_kwh_e_capo": 0},
               {"e_raff_alt_kwh_e_capo": 0},
               {"g_base_kwh_capo": 0},
               {"g_alt_kwh_capo": 0},
               {"om_base": 0},
               {"om_alt": 0},
               {"wacc_pct": 0},
               {"tolleranza_pct": 0}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["verdetto"] in ("CONVIENTE", "MARGINALE",
                                  "NON_CONVIENTE", "NON_CALCOLABILE")


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    bc = _variante(g_alt_kwh_capo=3.5)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] <= 0.0
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"]


def test_pareggio_esatto_tolleranza_float():
    be = mh824_demo_calcoli()["breakeven_gas_eur_kwh"]
    bc = _variante(p_gas=be)
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["verdetto"] != "CONVIENTE"
    bc2 = _variante(p_gas=0.10)
    assert bc2["risparmio_eur_anno"] == pytest.approx(5000.0, abs=1e-6)
    assert bc2["verdetto"] == "CONVIENTE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh824_demo_calcoli()
    testo = mh824_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_gas_eur_kwh" in testo
    assert "co2_evitata_t_anno" in testo
    assert "gas_base_kwh_anno" in testo
    assert "e_raff_alt_kwh_e_anno" in testo
    assert "e_vent_alt_kwh_e_anno" in testo
    assert "gas_alt_kwh_anno" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh824_demo_calcoli()
    testo = mh824_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"e_raff_base_kwh_e_anno;{bc['e_raff_base_kwh_e_anno']}" in testo
    assert f"gas_base_kwh_anno;{bc['gas_base_kwh_anno']}" in testo
    assert f"e_vent_base_kwh_e_anno;{bc['e_vent_base_kwh_e_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh824_demo_calcoli()
    testo = mh824_csv(bc, _demo_kwargs())
    for chiave in _demo_kwargs():
        assert f"{chiave};" in testo


# ------------------------------------------------------- test strutturali
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _leggi(nome):
    qui = os.path.dirname(os.path.abspath(__file__))
    p = os.path.join(qui, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    with open(p, encoding="utf-8") as f:
        return f.read()


def _vietati():
    # Token della scheda precedente, costruiti
    # per concatenazione: questo stesso file non li contiene
    # come sottostringhe contigue.
    return ["mh" + "82" + "3", "st" + "82" + "3",
            "tab" + "82" + "3", "w" + "82" + "5"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w826_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    raw = _leggi("w826_ui.py")
    assert raw.startswith("    # W826")
    src = textwrap.dedent(raw)
    ast.parse(src)
    assert src.startswith("# W826")
    assert "with tab824:" in src


def test_ui_apre_scheda_attesa_una_volta():
    """Il frammento UI apre la scheda attesa, una sola volta."""
    src = _leggi("w826_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert m.group(1) == "824"
    assert src.count("with tab824:") == 1
    assert src.count("    with tab824:") == 1


def test_ui_titolo_atteso():
    src = _leggi("w826_ui.py")
    titolo = ("🐔 Allevamento avicolo / pollaio da carne: "
              "ventilazione con inverter + "
              "raffrescamento evaporativo + "
              "recupero calore aria esausta battono "
              "ventilazione on/off + "
              "raffrescamento tradizionale + "
              "riscaldamento a gas?")
    assert src.count(titolo) == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w826_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_helpers_senza_costanti_di_modulo():
    src = _leggi("w826_helpers.py")
    albero = ast.parse(src)
    for nodo in albero.body:
        assert not isinstance(nodo, ast.Assign), \
            "costante di modulo vietata: i fattori devono essere letterali dentro le funzioni"


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w826_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st824_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) == 22
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w826_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 4
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.line_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_ui_guard_degenere_identica_helper():
    """La guard UI della scheda dichiara NON_CALCOLABILE
    per gli stessi casi degeneri degli helper:
    capi <= 0, prezzi <= 0, CAPEX <= 0,
    vita <= 0 (nessuna divergenza helper-vs-UI)."""
    src = _leggi("w826_ui.py")
    assert "float(_cp824) <= 0.0" in src
    assert "float(_pel824) <= 0.0" in src
    assert "float(_pg824) <= 0.0" in src
    assert "float(_cx824) <= 0.0" in src
    assert "int(_vita824) <= 0" in src
    assert "Verdetto: NON_CALCOLABILE" in src


def test_ui_chiamata_calcola_keyword_uguali_firma():
    """La chiamata UI a calcola usa come keyword
    esattamente i parametri della firma helper."""
    src = textwrap.dedent(_leggi("w826_ui.py"))
    albero = ast.parse(src)
    chiamate = []
    for nodo in ast.walk(albero):
        if isinstance(nodo, ast.Call):
            func = nodo.func
            if isinstance(func, ast.Name) and func.id == "mh824_calcola":
                chiamate.append({kw.arg for kw in nodo.keywords})
    assert len(chiamate) == 1
    attesi = set(inspect.signature(mh824_calcola).parameters.keys())
    assert chiamate[0] == attesi


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w826_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def824[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w826_ui.py")
        usate = set(re.findall(r'_def824\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 15
        assert usate <= set(mh824_demo().keys())
