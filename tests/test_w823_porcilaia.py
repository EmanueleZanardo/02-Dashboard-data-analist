"""Test nuova scheda tab823 "Porcilaia /
allevamento suino: ventilazione con
inverter + raffrescamento evaporativo +
recupero calore aria esausta battono
ventilazione on/off + raffrescamento
tradizionale + riscaldamento a gas?".

Business case deterministico di una
porcilaia guidata dai CAPI SUINI
allevati/anno: E_vent_base = capi x
e_vent_base; E_vent_alt = capi x
e_vent_alt (l'inverter riduce solo la
ventilazione); E_raff_base = capi x
e_raff_base; E_raff_alt = capi x
e_raff_alt (l'evaporativo riduce solo il
raffrescamento); E_base = E_vent_base +
E_raff_base; E_alt = E_vent_alt +
E_raff_alt; gas_base = capi x g_base;
gas_alt = capi x g_alt (il recupero
calore RIDUCE il gas, non lo azzera:
gas_alt resta positivo nel demo);
C_base = E_base x p_el + gas_base x
p_gas + OM_base; C_alt = E_alt x p_el
+ gas_alt x p_gas + OM_alt (prezzi in
EUR/kWh, nessuna conversione / 1000);
risparmio = C_base - C_alt; CO2 evitata
= (E_base x 0,25 + gas_base x 0,202 -
E_alt x 0,25 - gas_alt x 0,202) / 1000
(fattori letterali); flussi [-CAPEX,
risparmio x vita]; VAN, TIR, payback
(primo anno con cumulato >= 0);
breakeven gas = (E_alt x p_el + OM_alt
- E_base x p_el - OM_base) /
(gas_base - gas_alt) EUR/kWh, None se
gas_base <= gas_alt o numeratore < 0,
SOGLIA MINIMA quando esiste. Nel demo
il breakeven e' 0,05476190476190476
EUR/kWh (numeratore 5.750 EUR,
denominatore 105.000 kWh/anno).
Verdetto: NON_CALCOLABILE se input
degenere (capi <= 0, specifici negativi,
prezzi <= 0, O&M negativi, CAPEX <= 0,
WACC negativo, vita <= 0, tolleranza
negativa) o se risparmio <= 0 (guard
degenere: UI salta KPI, grafico,
tabella e CSV); altrimenti CONVIENTE
se VAN > 0, MARGINALE se VAN negativa
entro tolleranza % del CAPEX,
NON_CONVIENTE se VAN negativa oltre
la tolleranza. Guard UI IDENTICA agli
helper: nessuna divergenza di verdetto.
Tutti gli slider UI hanno minimo 0,
quindi i casi negativi sono NON
RAGGIUNGIBILI via slider, ma la guard
li controlla comunque; i casi = 0
raggiungibili via slider sono bloccati
in UI esattamente come negli helper
dove previsto (capi, prezzi, CAPEX,
vita). Gli zeri ammessi in entrambi
(specifici elettrici e gas, O&M, WACC,
tolleranza) non creano divergenza: con
gas specifico base uguale a gas
specifico alternativo il breakeven e'
None, e il caso resta calcolabile in
entrambi. WACC sopra 20 % e tolleranza
sopra 100 % sono ammessi negli helper
e limitati solo dagli slider UI
(20, 100): nessuna divergenza nel range
raggiungibile, perche' la guard
controlla solo gli stessi limiti degli
helper.
Distinzione esplicita: distinta dalla
sala mungitura (litri di latte, vuoto,
refrigerazione latte: qui niente litri
di latte, niente vuoto, niente
refrigerazione latte), dal mulino
(tonnellate di cereale, macinazione,
pneumatico: qui niente cereali, niente
macinazione, niente pneumatico), dal
caseificio (litri di latte,
pastorizzazione: qui niente
pastorizzazione, niente latte
pastorizzato): qui driver CAPO SUINO
+ VENTILAZIONE CON INVERTER +
RAFFRESCAMENTO EVAPORATIVO + RECUPERO
CALORE ARIA ESAUSTA.

Demo (porcilaia): 5.000 capi suini,
ventilazione specifica base 55
(275.000 kWh_e/anno) e alternativa 45
(225.000 kWh_e/anno), raffrescamento
specifico base 18 (90.000 kWh_e/anno)
e alternativo 15 (75.000 kWh_e/anno),
elettricita' base 365.000 e alternativa
300.000 kWh_e/anno, gas specifico base
30 (150.000 kWh/anno) e alternativo 9
(45.000 kWh/anno, il recupero riduce il
gas del 70 %, non lo azzera), prezzi
elettricita' 0,25 e gas 0,10 EUR/kWh,
O&M base 8.000 e alternativo 30.000
EUR/anno, CAPEX 35.000 EUR, WACC 5 %,
vita 15 anni, tolleranza 10 % del
CAPEX. Valori calcolati eseguendo
mh823_demo_calcoli(): E_base 365.000,
E_alt 300.000, gas_base 150.000,
gas_alt 45.000, C_base 114.250, C_alt
109.500, risparmio 4.750, CO2_base
121,55, CO2_alt 84,09, CO2_evitata
37,46, VAN 14303,375681357806, TIR
10,561376493118297 %, payback 8,
breakeven gas 0,05476190476190476
EUR/kWh, verdetto CONVIENTE.
NOTA DISCREPANZA BRIEF: il brief
attendeva C_base 118.250, C_alt
104.500, CO2_alt 61,59 e CO2_evitata
59,96; il ricalcolo reale da'
114.250, 109.500, 84,09 e 37,46 (il
risparmio resta 4.750, la VAN circa
14.303, il payback 8 e il breakeven
0,0548 restano confermati). I test
usano i valori reali, non quelli
attesi nel brief.
"""

import ast
import inspect
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w825_helpers import (
    demo_calcoli,
    mh823_breakeven_gas,
    mh823_c_alt,
    mh823_c_base,
    mh823_calcola,
    mh823_co2_alt,
    mh823_co2_base,
    mh823_co2_evitata,
    mh823_csv,
    mh823_demo,
    mh823_demo_calcoli,
    mh823_e_alt,
    mh823_e_base,
    mh823_e_raff_alt,
    mh823_e_raff_base,
    mh823_e_vent_alt,
    mh823_e_vent_base,
    mh823_flussi,
    mh823_gas_alt,
    mh823_gas_base,
    mh823_int_pos,
    mh823_nneg,
    mh823_num,
    mh823_payback,
    mh823_pos,
    mh823_risparmio,
    mh823_tir,
    mh823_valida,
    mh823_van,
    mh823_verdetto,
)

_DEMO = {
    "e_vent_base_kwh_e_anno": 275000.0,
    "e_vent_alt_kwh_e_anno": 225000.0,
    "e_raff_base_kwh_e_anno": 90000.0,
    "e_raff_alt_kwh_e_anno": 75000.0,
    "e_base_kwh_e_anno": 365000.0,
    "e_alt_kwh_e_anno": 300000.0,
    "gas_base_kwh_anno": 150000.0,
    "gas_alt_kwh_anno": 45000.0,
    "c_base_eur_anno": 114250.0,
    "c_alt_eur_anno": 109500.0,
    "risparmio_eur_anno": 4750.0,
    "co2_base_t_anno": 121.55,
    "co2_alt_t_anno": 84.09,
    "co2_evitata_t_anno": 37.46,
    "van": 14303.375681357806,
    "tir": 10.561376493118297,
}


def _demo_kwargs():
    return dict(mh823_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh823_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh823_num(3, "x") == 3.0
    assert mh823_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh823_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh823_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh823_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh823_pos(0, "x")
    with pytest.raises(ValueError):
        mh823_pos(-1, "x")
    assert mh823_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh823_int_pos(5.0, "x") == 5
    assert mh823_int_pos(15.0, "x") == 15
    with pytest.raises(ValueError):
        mh823_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh823_int_pos(0, "x")


# ---------------------------------------------------------------- fisica base
def test_e_vent_e_raff_e_base():
    assert mh823_e_vent_base(5000, 55) == 275000.0
    assert mh823_e_vent_alt(5000, 45) == 225000.0
    assert mh823_e_raff_base(5000, 18) == 90000.0
    assert mh823_e_raff_alt(5000, 15) == 75000.0
    assert mh823_e_base(275000.0, 90000.0) == 365000.0
    with pytest.raises(ValueError):
        mh823_e_base(-1, 90000.0)
    with pytest.raises(ValueError):
        mh823_e_vent_base(0, 55)


def test_e_alt():
    assert mh823_e_alt(225000.0, 75000.0) == 300000.0
    with pytest.raises(ValueError):
        mh823_e_alt(225000.0, -1)
    with pytest.raises(ValueError):
        mh823_e_vent_alt(0, 45)


def test_gas_base_alt():
    assert mh823_gas_base(5000, 30) == 150000.0
    assert mh823_gas_alt(5000, 9) == 45000.0
    assert mh823_gas_alt(5000, 0) == 0.0
    with pytest.raises(ValueError):
        mh823_gas_base(5000, -1)
    with pytest.raises(ValueError):
        mh823_gas_base(0, 30)


def test_c_base_c_alt_scomposizione():
    assert mh823_c_base(365000.0, 0.25, 150000.0, 0.10,
                        8000) == pytest.approx(114250.0)
    assert mh823_c_alt(300000.0, 0.25, 45000.0, 0.10,
                       30000) == pytest.approx(109500.0)
    with pytest.raises(ValueError):
        mh823_c_base(365000.0, 0, 150000.0, 0.10, 8000)
    with pytest.raises(ValueError):
        mh823_c_alt(300000.0, 0.25, 45000.0, 0, 30000)
    with pytest.raises(ValueError):
        mh823_c_base(365000.0, 0.25, 150000.0, 0.10, -1)


def test_risparmio_segno():
    assert mh823_risparmio(114250.0, 109500.0) == pytest.approx(4750.0)
    assert mh823_risparmio(109500.0, 109500.0) == pytest.approx(0.0, abs=1e-9)


def test_co2_base_alt_evitata():
    assert mh823_co2_base(365000.0, 150000.0) == pytest.approx(121.55)
    assert mh823_co2_alt(300000.0, 45000.0) == pytest.approx(84.09)
    assert mh823_co2_evitata(365000.0, 150000.0,
                             300000.0, 45000.0) == pytest.approx(37.46)
    assert mh823_co2_base(0, 0) == 0.0
    assert mh823_co2_alt(0, 0) == 0.0
    with pytest.raises(ValueError):
        mh823_co2_base(365000.0, -1)
    with pytest.raises(ValueError):
        mh823_co2_alt(-1, 0.0)


def test_breakeven_demo_valore():
    bc = mh823_demo_calcoli()
    assert bc["breakeven_gas_eur_kwh"] == pytest.approx(0.05476190476190476)
    # Numeratore: 300000*0,25 + 30000 - 365000*0,25 - 8000 = 5750;
    # denominatore: 150000 - 45000 = 105000.
    assert mh823_breakeven_gas(300000.0, 0.25, 30000, 365000.0,
                               8000, 150000.0,
                               45000.0) == pytest.approx(0.05476190476190476)
    # Gas base uguale a gas alternativo -> None.
    assert mh823_breakeven_gas(300000.0, 0.25, 30000, 365000.0,
                               8000, 150000.0, 150000.0) is None
    # Gas base minore di gas alternativo -> None.
    assert mh823_breakeven_gas(300000.0, 0.25, 30000, 365000.0,
                               8000, 10000.0, 45000.0) is None
    # Variante gas alternativo uguale al base -> breakeven None.
    assert _variante(g_alt_kwh_capo=30)["breakeven_gas_eur_kwh"] is None
    with pytest.raises(ValueError):
        mh823_breakeven_gas(300000.0, 0.25, 30000, 365000.0,
                            8000, -1, 45000.0)


def test_breakeven_numeratore_negativo_none():
    # Con O&M alternativo 0 il numeratore
    # diventa negativo: 300000*0,25 + 0 - 365000*0,25 - 8000 < 0.
    assert mh823_breakeven_gas(300000.0, 0.25, 0, 365000.0,
                               8000, 150000.0,
                               45000.0) is None
    assert _variante(om_alt=0)["breakeven_gas_eur_kwh"] is None


def test_breakeven_verifica_pareggio_su_demo():
    be = mh823_demo_calcoli()["breakeven_gas_eur_kwh"]
    bc = _variante(p_gas=be)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_breakeven_soglia_minima_su_demo():
    be = mh823_demo_calcoli()["breakeven_gas_eur_kwh"]
    bc_alto = _variante(p_gas=0.10)
    bc_basso = _variante(p_gas=0.04)
    assert bc_alto["c_alt_eur_anno"] < bc_alto["c_base_eur_anno"]
    assert bc_basso["c_alt_eur_anno"] > bc_basso["c_base_eur_anno"]
    assert bc_alto["risparmio_eur_anno"] > 0.0
    assert bc_basso["verdetto"] == "NON_CALCOLABILE"
    assert bc_alto["risparmio_eur_anno"] == pytest.approx(4750.0)
    assert bc_basso["risparmio_eur_anno"] == pytest.approx(-1550.0)
    assert bc_alto["verdetto"] == "CONVIENTE"
    assert be < 0.10


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh823_flussi(35000, 4750.0, 15)
    assert len(fl) == 16
    assert fl[0] == -35000
    assert all(f == pytest.approx(4750.0) for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh823_demo_calcoli()
    assert bc["van"] == pytest.approx(14303.375681357806)
    assert mh823_van([-35000] + [4750.0] * 15,
                     0) == pytest.approx(36250.0)
    assert mh823_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh823_demo_calcoli()
    assert bc["tir"] == pytest.approx(10.561376493118297)
    assert mh823_tir([-35000] + [4750.0] * 15) == \
        pytest.approx(0.10561376493118297)
    tir = mh823_tir([-35000] + [4750.0] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-35000] + [4750.0] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh823_payback([-35000] + [4750.0] * 15) == 8
    assert mh823_payback([-35000] + [-1000.0] * 15) is None
    assert mh823_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh823_verdetto(4750.0, 14303.375681357806, 35000,
                          10.0) == "CONVIENTE"
    assert mh823_verdetto(4750.0, -1500.0, 35000,
                          10.0) == "MARGINALE"
    assert mh823_verdetto(4750.0, -3500.0, 35000, 10.0) == "MARGINALE"
    assert mh823_verdetto(4750.0, -3500.01, 35000, 10.0) == "NON_CONVIENTE"
    assert mh823_verdetto(4750.0, 0.0, 35000, 10.0) == "MARGINALE"
    assert mh823_verdetto(0.0, 14303.37, 35000,
                          10.0) == "NON_CALCOLABILE"
    assert mh823_verdetto(-1000.0, -55379.66, 35000,
                          10.0) == "NON_CALCOLABILE"
    assert mh823_verdetto(None, 14303.37, 35000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh823_verdetto(float("nan"), 14303.37, 35000, 10.0)
    with pytest.raises(ValueError):
        mh823_verdetto(4750.0, 14303.37, 0, 10.0)
    with pytest.raises(ValueError):
        mh823_verdetto(4750.0, 14303.37, 35000, -1)


def test_valida_demo_ok():
    v = mh823_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("capi", "5000"),
                       ("capi", float("nan")),
                       ("capi", float("inf")),
                       ("capi", True),
                       ("p_gas", None),
                       ("g_base_kwh_capo", "30")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh823_valida(**d)["valido"] is False


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
        assert mh823_valida(**d)["valido"] is False


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
    assert mh823_valida(**d)["valido"] is True
    # Il brief non impone tetti superiori a WACC
    # e tolleranza: gli helper li ammettono.
    d["wacc_pct"] = 60
    d["tolleranza_pct"] = 200
    assert mh823_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh823_demo()
    assert d["capi"] == 5000
    assert d["e_vent_base_kwh_e_capo"] == 55
    assert d["e_vent_alt_kwh_e_capo"] == 45
    assert d["e_raff_base_kwh_e_capo"] == 18
    assert d["e_raff_alt_kwh_e_capo"] == 15
    assert d["g_base_kwh_capo"] == 30
    assert d["g_alt_kwh_capo"] == 9
    assert d["p_el"] == 0.25
    assert d["p_gas"] == 0.10
    assert d["om_base"] == 8000
    assert d["om_alt"] == 30000
    assert d["capex"] == 35000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    bc = mh823_demo_calcoli()
    for chiave, atteso in _DEMO.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert got == pytest.approx(atteso, rel=1e-9), chiave
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True
    assert bc["breakeven_gas_eur_kwh"] == pytest.approx(0.05476190476190476)
    assert demo_calcoli()["van"] == bc["van"]


def test_demo_calcoli_fisica_economia():
    bc = mh823_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(114250.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(109500.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(4750.0)
    assert bc["co2_base_t_anno"] == pytest.approx(121.55)
    assert bc["co2_alt_t_anno"] == pytest.approx(84.09)
    assert bc["co2_evitata_t_anno"] == pytest.approx(37.46)
    assert bc["gas_base_kwh_anno"] == pytest.approx(150000.0)
    assert bc["gas_alt_kwh_anno"] == pytest.approx(45000.0)
    assert bc["e_vent_base_kwh_e_anno"] == pytest.approx(275000.0)
    assert bc["e_vent_alt_kwh_e_anno"] == pytest.approx(225000.0)
    assert bc["e_raff_base_kwh_e_anno"] == pytest.approx(90000.0)
    assert bc["e_raff_alt_kwh_e_anno"] == pytest.approx(75000.0)
    assert bc["e_base_kwh_e_anno"] == pytest.approx(365000.0)
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(300000.0)


def test_demo_flussi_e_cumulato():
    bc = mh823_demo_calcoli()
    assert bc["flussi"][0] == -35000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(4750.0) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -35000
    assert righe.iloc[7]["Cumulato (EUR)"] == pytest.approx(-1750.0)
    assert righe.iloc[8]["Cumulato (EUR)"] == pytest.approx(3000.0)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(36250.0)


def test_demo_tabella_righe():
    bc = mh823_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Ventilazione baseline (kWh_e/anno)"] == pytest.approx(275000.0)
    assert mappa["Ventilazione alternativa (kWh_e/anno)"] == pytest.approx(225000.0)
    assert mappa["Raffrescamento baseline (kWh_e/anno)"] == pytest.approx(90000.0)
    assert mappa["Raffrescamento alternativa (kWh_e/anno)"] == pytest.approx(75000.0)
    assert mappa["Elettricita' base (kWh_e/anno)"] == pytest.approx(365000.0)
    assert mappa["Elettricita' alternativa (kWh_e/anno)"] == pytest.approx(300000.0)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(150000.0)
    assert mappa["Gas alternativo (kWh/anno)"] == pytest.approx(45000.0)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(114250.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(109500.0)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(4750.0)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(37.46)
    assert mappa["Payback (anni)"] == 8
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/kWh)"] == pytest.approx(0.05476190476190476)


def test_demo_coerenza_interna():
    bc = mh823_demo_calcoli()
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
    cp, evb, eva = 5000, 55, 45
    erb, era, gab, gaa = 18, 15, 30, 9
    pel, pg = 0.25, 0.10
    omb, oma, cx = 8000, 30000, 35000
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
    bc = mh823_demo_calcoli()
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
    assert bc["breakeven_gas_eur_kwh"] == pytest.approx(5750.0 / 105000.0)


def test_demo_verdetto_coerente_con_risparmio_e_van():
    bc = mh823_demo_calcoli()
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] > 0.0
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["tir"] is not None and bc["tir"] > bc["wacc_pct"]
    assert bc["payback"] == 8


# ---------------------------------------------------------------- varianti
def test_variante_senza_inverter_non_calcolabile():
    # Ventilazione alternativa 55 = niente
    # risparmio dall'inverter: il risparmio
    # diventa negativo negli helper
    # (calcolabile, non solleva), verdetto
    # NON_CALCOLABILE; stessa guard della UI.
    bc = _variante(e_vent_alt_kwh_e_capo=55)
    assert bc["e_vent_alt_kwh_e_anno"] == pytest.approx(275000.0)
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(350000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(122000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-7750.0)
    assert bc["van"] == pytest.approx(-115442.34979589959)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["breakeven_gas_eur_kwh"] == pytest.approx(0.1738095238095238)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_senza_evaporativo_non_convinte():
    # Raffrescamento alternativo 18 =
    # niente risparmio dall'evaporativo:
    # il caso diventa NON_CONVIENTE.
    bc = _variante(e_raff_alt_kwh_e_capo=18)
    assert bc["e_raff_alt_kwh_e_anno"] == pytest.approx(90000.0)
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(315000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(113250.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(1000.0)
    assert bc["van"] == pytest.approx(-24620.341961819406)
    assert bc["tir"] == pytest.approx(-9.104347863459513)
    assert bc["payback"] is None
    assert bc["breakeven_gas_eur_kwh"] == pytest.approx(0.09047619047619047)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_senza_recupero_non_calcolabile():
    # Gas alternativo 30 = niente recupero
    # calore: il risparmio diventa negativo
    # negli helper (calcolabile, non solleva),
    # verdetto NON_CALCOLABILE; stessa guard
    # della UI. Il breakeven e' None perche'
    # gas base uguale a gas alternativo.
    bc = _variante(g_alt_kwh_capo=30)
    assert bc["valid"] is True
    assert bc["gas_alt_kwh_anno"] == pytest.approx(150000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(120000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-5750.0)
    assert bc["van"] == pytest.approx(-94683.03371953842)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"]
    assert bc["payback"] is None
    assert bc["tir"] is None
    assert bc["breakeven_gas_eur_kwh"] is None


def test_variante_capex_60000_non_convinte():
    bc = _variante(capex=60000)
    assert bc["risparmio_eur_anno"] == pytest.approx(4750.0)
    assert bc["van"] == pytest.approx(-10696.624318642193)
    assert bc["tir"] == pytest.approx(2.229274251604975)
    assert bc["payback"] == 13
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_om_alt_31500_marginale():
    # O&M alternativo 31.500: risparmio 3.250,
    # VAN negativa entro il 10 % del CAPEX
    # (3.500 EUR), quindi MARGINALE.
    bc = _variante(om_alt=31500)
    assert bc["c_alt_eur_anno"] == pytest.approx(111000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(3250.0)
    assert bc["van"] == pytest.approx(-1266.1113759130783)
    assert bc["tir"] == pytest.approx(4.459877355880335)
    assert bc["payback"] == 11
    assert bc["breakeven_gas_eur_kwh"] == pytest.approx(0.06904761904761905)
    assert bc["verdetto"] == "MARGINALE"


def test_variante_om_alt_40000_non_calcolabile():
    # O&M alt 40.000: risparmio negativo negli
    # helper (calcolabile, non solleva), verdetto
    # NON_CALCOLABILE; stessa guard della UI.
    bc = _variante(om_alt=40000)
    assert bc["valid"] is True
    assert bc["c_alt_eur_anno"] == pytest.approx(119500.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-5250.0)
    assert bc["van"] == pytest.approx(-89493.20470044807)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"]
    assert bc["payback"] is None
    assert bc["tir"] is None
    assert bc["breakeven_gas_eur_kwh"] == pytest.approx(0.15)


def test_variante_gas_basso_e_alto():
    bc_basso = _variante(p_gas=0.04)
    assert bc_basso["risparmio_eur_anno"] == pytest.approx(-1550.0)
    assert bc_basso["van"] == pytest.approx(-51088.469959179914)
    assert bc_basso["verdetto"] == "NON_CALCOLABILE"
    bc_alto = _variante(p_gas=0.20)
    assert bc_alto["risparmio_eur_anno"] == pytest.approx(15250.0)
    assert bc_alto["van"] == pytest.approx(123289.78508225402)
    assert bc_alto["tir"] == pytest.approx(43.375509282543426)
    assert bc_alto["payback"] == 3
    assert bc_alto["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(36250.0)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(1678.2409136278534)
    assert bc2["tir"] == pytest.approx(5.976120486920247)
    assert bc2["payback"] == 8
    assert bc2["verdetto"] == "CONVIENTE"
    bc3 = _variante(vita_anni=7)
    assert bc3["van"] == pytest.approx(-7514.726362361552)
    assert bc3["payback"] is None
    assert bc3["verdetto"] == "NON_CONVIENTE"


def test_monotonia_prezzo_gas_crescente():
    base = mh823_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas=0.101)["risparmio_eur_anno"]
    basso = _variante(p_gas=0.099)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(105.0, abs=1e-6)
    assert base - basso == pytest.approx(105.0, abs=1e-6)


def test_monotonia_ventilazione_e_recupero():
    # Piu' elettricita' di ventilazione alternativa,
    # meno risparmio; piu' gas alternativo
    # (meno recupero), meno risparmio.
    assert _variante(e_vent_alt_kwh_e_capo=50)["risparmio_eur_anno"] < \
        mh823_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(g_alt_kwh_capo=15)["risparmio_eur_anno"] < \
        mh823_demo_calcoli()["risparmio_eur_anno"]


def test_demo_deterministica_due_chiamate():
    a = mh823_demo_calcoli()
    b = mh823_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh823_demo().keys()) == {
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
        assert mh823_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"capi": "5000"},
               {"capi": float("nan")},
               {"p_gas": float("inf")},
               {"capex": True},
               {"g_base_kwh_capo": "30"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh823_valida(**d)["valido"] is False


def test_zeri_ammessi_non_sollevano_e_nessuna_divergenza():
    # Zeri ammessi in entrambi (helper e UI):
    # specifici elettrici e gas, O&M, WACC,
    # tolleranza. Qui si verifica che non
    # sollevano e restano calcolabili.
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
    bc = _variante(g_alt_kwh_capo=30)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] <= 0.0
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"]


def test_pareggio_esatto_tolleranza_float():
    # A pareggio esatto (prezzo gas = breakeven
    # del demo) il risparmio e' zero (circa
    # 0.0, quindi guard NON_CALCOLABILE): in
    # nessun caso CONVIENTE.
    be = mh823_demo_calcoli()["breakeven_gas_eur_kwh"]
    bc = _variante(p_gas=be)
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["verdetto"] != "CONVIENTE"
    bc2 = _variante(p_gas=0.10)
    assert bc2["risparmio_eur_anno"] == pytest.approx(4750.0, abs=1e-6)
    assert bc2["verdetto"] == "CONVIENTE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh823_demo_calcoli()
    testo = mh823_csv(bc, _demo_kwargs())
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
    bc = mh823_demo_calcoli()
    testo = mh823_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"e_raff_base_kwh_e_anno;{bc['e_raff_base_kwh_e_anno']}" in testo
    assert f"gas_base_kwh_anno;{bc['gas_base_kwh_anno']}" in testo
    assert f"e_vent_base_kwh_e_anno;{bc['e_vent_base_kwh_e_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh823_demo_calcoli()
    testo = mh823_csv(bc, _demo_kwargs())
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
    return ["mh" + "82" + "2", "st" + "82" + "2",
            "tab" + "82" + "2", "w" + "82" + "3"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w825_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    raw = _leggi("w825_ui.py")
    assert raw.startswith("    # W825")
    src = textwrap.dedent(raw)
    ast.parse(src)
    assert src.startswith("# W825")
    assert "with tab823:" in src


def test_ui_apre_scheda_attesa_una_volta():
    """Il frammento UI apre la scheda attesa, una sola volta."""
    src = _leggi("w825_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert m.group(1) == "823"
    assert src.count("with tab823:") == 1
    assert src.count("    with tab823:") == 1


def test_ui_titolo_atteso():
    src = _leggi("w825_ui.py")
    titolo = ("🐖 Porcilaia / allevamento suino: "
              "ventilazione con inverter + "
              "raffrescamento evaporativo + "
              "recupero calore aria esausta battono "
              "ventilazione on/off + "
              "raffrescamento tradizionale + "
              "riscaldamento a gas?")
    assert src.count(titolo) == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w825_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_helpers_senza_costanti_di_modulo():
    src = _leggi("w825_helpers.py")
    albero = ast.parse(src)
    for nodo in albero.body:
        assert not isinstance(nodo, ast.Assign), \
            "costante di modulo vietata: i fattori devono essere letterali dentro le funzioni"


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w825_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st823_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) == 22
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w825_ui.py")
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
    src = _leggi("w825_ui.py")
    assert "float(_cp823) <= 0.0" in src
    assert "float(_pel823) <= 0.0" in src
    assert "float(_pg823) <= 0.0" in src
    assert "float(_cx823) <= 0.0" in src
    assert "int(_vita823) <= 0" in src
    assert "Verdetto: NON_CALCOLABILE" in src


def test_ui_chiamata_calcola_keyword_uguali_firma():
    """La chiamata UI a calcola usa come keyword
    esattamente i parametri della firma helper."""
    src = textwrap.dedent(_leggi("w825_ui.py"))
    albero = ast.parse(src)
    chiamate = []
    for nodo in ast.walk(albero):
        if isinstance(nodo, ast.Call):
            func = nodo.func
            if isinstance(func, ast.Name) and func.id == "mh823_calcola":
                chiamate.append({kw.arg for kw in nodo.keywords})
    assert len(chiamate) == 1
    attesi = set(inspect.signature(mh823_calcola).parameters.keys())
    assert chiamate[0] == attesi


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w825_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def823[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w825_ui.py")
        usate = set(re.findall(r'_def823\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 15
        assert usate <= set(mh823_demo().keys())
