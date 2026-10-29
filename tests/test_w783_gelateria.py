"""Test tab783 "Gelateria: pastorizzare con pompa di
calore e freddo efficiente batte caldaia a gas +
chiller tradizionale?" (titolo completo nel
frammento UI).
(File repo: tests/test_w783_gelateria.py,
contenuto pronto da scrivere in repo.)

Business case deterministico di una gelateria
artigianale guidata dalla produzione annua in kg:
pastorizzazione Q_past = kg x q_past kWh_th/anno
e freddo Q_freddo = kg x q_freddo kWh_th/anno;
gas baseline G = Q_past / eta_caldaia kWh/anno;
elettricita' chiller tradizionale E_chill_base =
Q_freddo / COP_chill_base; elettricita' pompa di
calore E_pdc = Q_past / COP_pdc; elettricita'
chiller efficiente E_chill_alt = Q_freddo /
COP_chill_alt; elettricita' alternativa E_alt =
E_pdc + E_chill_alt kWh_e/anno; C_base =
G / 1000 x p_gas + E_chill_base / 1000 x p_el +
O&M_base EUR/anno; C_alt = E_alt / 1000 x p_el +
O&M_alt EUR/anno (prezzi EUR/MWh, energie kWh:
/ 1000 esatto); risparmio = C_base - C_alt;
CO2_base = G / 1000 x f_gas + E_chill_base /
1000 x f_el t/anno; CO2_alt = E_alt / 1000 x
f_el t/anno; CO2_evitata = CO2_base - CO2_alt;
flussi [-CAPEX, risparmio x vita]; VAN, TIR,
payback (primo anno con cumulato >= 0);
breakeven gas p_gas_be = (E_alt / 1000 x p_el +
O&M_alt - E_chill_base / 1000 x p_el - O&M_base)
/ (G / 1000) EUR/MWh, None se G <= 0 o
numeratore < 0, SOGLIA MINIMA quando esiste.
Verdetto: NON_CALCOLABILE se risparmio <= 0
(guard degenere: UI salta KPI, grafico, tabella
e CSV); altrimenti CONVIENTE se VAN > 0,
MARGINALE se VAN negativa entro tolleranza %
del CAPEX, NON_CONVIENTE se VAN negativa oltre
la tolleranza. Distinzione esplicita: gelateria
artigianale con DUE vettori guidati dai kg
(pastorizzazione + mantecazione e conservazione),
baseline caldaia a gas + chiller tradizionale
contro pompa di calore + chiller efficiente;
NON il caso del recupero del calore di scarto
dei frigoriferi per acqua calda sanitaria e
riscaldamento di un negozio, con l'elettricita'
dei frigoriferi come costo comune escluso dal
confronto: qui l'elettricita' del freddo entra
in entrambi i casi e il calore di
pastorizzazione e' prodotto dalla pompa di
calore, non recuperato da uno scarto.

Demo (gelateria media): kg 60.000, q_past 0,25,
q_freddo 0,60 kWh_th/kg, caldaia 0,9, COP chiller
tradizionale 2,5, COP pompa di calore 3,5, COP
chiller efficiente 3,2, gas 90, el 250 EUR/MWh,
O&M base 800, alt 1.000, CAPEX 8.000, WACC 5 %,
vita 12, f_gas 0,20, f_el 0,35, tolleranza 10 %
del CAPEX. Valori calcolati eseguendo
mh783_demo_calcoli(): Q_past 15.000, Q_freddo
36.000, G 16.666,666666666668, E_chill_base
14.400, E_pdc 4.285,714285714285, E_chill_alt
11.250, E_alt 15.535,714285714286, C_base 5.900,
C_alt 4.883,928571428572, risparmio
1.016,0714285714284, CO2_base 8,373333333333335,
CO2_alt 5,4375, CO2_evitata 2,935833333333335,
VAN 1.005,6967520345902, TIR 7,16463253469231 %,
payback 8, breakeven gas 29,035714285714292,
verdetto CONVIENTE.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w784_helpers import (
    demo_calcoli,
    mh783_breakeven_gas,
    mh783_c_alt,
    mh783_c_base,
    mh783_calcola,
    mh783_co2_alt,
    mh783_co2_base,
    mh783_co2_evitata,
    mh783_cop,
    mh783_csv,
    mh783_demo,
    mh783_demo_calcoli,
    mh783_e_alt,
    mh783_e_chill_alt,
    mh783_e_chill_base,
    mh783_e_pdc,
    mh783_eta,
    mh783_flussi,
    mh783_gas,
    mh783_int_pos,
    mh783_num,
    mh783_nneg,
    mh783_payback,
    mh783_pct_tolleranza,
    mh783_pct_wacc,
    mh783_pos,
    mh783_q_freddo,
    mh783_q_past,
    mh783_risparmio,
    mh783_tir,
    mh783_valida,
    mh783_van,
    mh783_verdetto,
)

_DEMO = {
    "q_past_kwh_anno": 15000.0,
    "q_freddo_kwh_anno": 36000.0,
    "gas_kwh_anno": 16666.666666666668,
    "e_chill_base_kwh_anno": 14400.0,
    "e_pdc_kwh_anno": 4285.714285714285,
    "e_chill_alt_kwh_anno": 11250.0,
    "e_alt_kwh_anno": 15535.714285714286,
    "c_base_eur_anno": 5900.0,
    "c_alt_eur_anno": 4883.928571428572,
    "risparmio_eur_anno": 1016.0714285714284,
    "co2_base_t_anno": 8.373333333333335,
    "co2_alt_t_anno": 5.4375,
    "co2_evitata_t_anno": 2.935833333333335,
    "van": 1005.6967520345902,
    "tir": 7.16463253469231,
    "breakeven_gas_eur_mwh": 29.035714285714292,
}


def _demo_kwargs():
    return dict(mh783_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh783_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh783_num(3, "x") == 3.0
    assert mh783_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh783_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh783_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh783_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh783_pos(0, "x")
    with pytest.raises(ValueError):
        mh783_pos(-1, "x")
    assert mh783_pos(0.5, "x") == 0.5


def test_cop_maggiore_di_uno():
    assert mh783_cop(2.5, "x") == 2.5
    assert mh783_cop(1.01, "x") == 1.01
    with pytest.raises(ValueError):
        mh783_cop(1.0, "x")
    with pytest.raises(ValueError):
        mh783_cop(0.5, "x")
    with pytest.raises(ValueError):
        mh783_cop(0, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh783_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh783_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh783_int_pos(0, "x")


def test_eta_limiti():
    assert mh783_eta(1.0, "x") == 1.0
    assert mh783_eta(0.9, "x") == 0.9
    with pytest.raises(ValueError):
        mh783_eta(0, "x")
    with pytest.raises(ValueError):
        mh783_eta(1.01, "x")


def test_pct_wacc_limiti():
    assert mh783_pct_wacc(0, "x") == 0.0
    assert mh783_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh783_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh783_pct_tolleranza(0, "x") == 0.0
    assert mh783_pct_tolleranza(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh783_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh783_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_q_past_q_freddo_gas():
    assert mh783_q_past(60000, 0.25) == 15000.0
    assert mh783_q_freddo(60000, 0.60) == pytest.approx(36000.0)
    assert mh783_q_past(60000, 0) == 0.0
    assert mh783_gas(15000, 0.9) == pytest.approx(16666.666666666668)
    assert mh783_gas(0, 0.9) == 0.0
    with pytest.raises(ValueError):
        mh783_q_past(0, 0.25)
    with pytest.raises(ValueError):
        mh783_q_past(60000, -0.1)
    with pytest.raises(ValueError):
        mh783_gas(15000, 0)
    with pytest.raises(ValueError):
        mh783_gas(15000, 1.01)


def test_elettricita_vettori():
    assert mh783_e_chill_base(36000, 2.5) == pytest.approx(14400.0)
    assert mh783_e_pdc(15000, 3.5) == pytest.approx(4285.714285714285)
    assert mh783_e_chill_alt(36000, 3.2) == pytest.approx(11250.0)
    assert mh783_e_alt(4285.714285714285, 11250.0) == \
        pytest.approx(15535.714285714286)
    assert mh783_e_alt(0, 11250.0) == 11250.0
    with pytest.raises(ValueError):
        mh783_e_chill_base(36000, 1.0)
    with pytest.raises(ValueError):
        mh783_e_pdc(15000, 0.5)
    with pytest.raises(ValueError):
        mh783_e_chill_alt(36000, 1.0)


def test_c_base_c_alt_scomposizione():
    assert mh783_c_base(16666.666666666668, 90, 14400, 250,
                        800) == pytest.approx(5900.0)
    assert mh783_c_base(16666.666666666668, 0, 14400, 250,
                        800) == pytest.approx(4400.0)
    assert mh783_c_base(0, 90, 14400, 250, 800) == pytest.approx(4400.0)
    assert mh783_c_alt(15535.714285714286, 250,
                       1000) == pytest.approx(4883.928571428572)
    assert mh783_c_alt(11250.0, 250, 1000) == pytest.approx(3812.5)
    assert mh783_c_alt(0, 250, 1000) == pytest.approx(1000.0)
    with pytest.raises(ValueError):
        mh783_c_base(16666.666666666668, -1, 14400, 250, 800)
    with pytest.raises(ValueError):
        mh783_c_alt(15535.714285714286, 250, -1)


def test_risparmio_segno():
    assert mh783_risparmio(5900.0, 4883.928571428572) == \
        pytest.approx(1016.0714285714284)
    assert mh783_risparmio(4883.928571428572, 4883.928571428572) == 0.0
    assert mh783_risparmio(4733.333333333334, 4883.928571428572) == \
        pytest.approx(-150.59523809523762)


def test_co2_base_alt_evitata():
    assert mh783_co2_base(16666.666666666668, 0.20, 14400,
                          0.35) == pytest.approx(8.373333333333335)
    assert mh783_co2_alt(15535.714285714286,
                         0.35) == pytest.approx(5.4375)
    assert mh783_co2_evitata(16666.666666666668, 0.20, 14400,
                             15535.714285714286,
                             0.35) == pytest.approx(2.935833333333335)
    assert mh783_co2_evitata(0, 0.20, 14400, 11250.0,
                             0.35) == pytest.approx(1.1025)
    # Gas diviso per eta gia' in G: qui G e' gia' gas
    # bruciato, quindi CO2 gas = G / 1000 x f_gas.
    assert mh783_co2_base(16666.666666666668, 0.20, 0,
                          0.35) == pytest.approx(16666.666666666668 / 1000.0 * 0.20)
    with pytest.raises(ValueError):
        mh783_co2_base(16666.666666666668, -0.10, 14400, 0.35)
    with pytest.raises(ValueError):
        mh783_co2_alt(15535.714285714286, -0.10)


def test_breakeven_gas_demo_e_varianti():
    assert mh783_breakeven_gas(15535.714285714286, 250, 1000, 14400,
                               800, 16666.666666666668) == \
        pytest.approx(29.035714285714292)
    assert mh783_breakeven_gas(15535.714285714286, 400, 1000, 14400,
                               800, 16666.666666666668) == \
        pytest.approx(39.25714285714288)
    assert mh783_breakeven_gas(4285.714285714285, 250, 1000, 0,
                               800, 16666.666666666668) == \
        pytest.approx(76.28571428571429)
    assert mh783_breakeven_gas(11250.0, 250, 1000, 14400, 800,
                               0) is None
    # Numeratore negativo: alternativa gia' piu'
    # conveniente a prezzo gas zero -> nessun pareggio.
    assert mh783_breakeven_gas(1000.0, 250, 100, 14400, 800,
                               16666.666666666668) is None
    with pytest.raises(ValueError):
        mh783_breakeven_gas(15535.714285714286, 250, 1000, 14400,
                            800, -1)


def test_breakeven_verifica_pareggio():
    """Al prezzo gas di pareggio i costi si eguagliano
    e il risparmio e' zero: scatta la guard
    NON_CALCOLABILE, non un verdetto di convenienza."""
    bc = _variante(p_gas_eur_mwh=29.035714285714292)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    demo = mh783_demo_calcoli()
    assert (demo["e_alt_kwh_anno"] / 1000.0
            * demo["p_el_eur_mwh"]
            + demo["om_alt_eur_anno"]
            - demo["e_chill_base_kwh_anno"] / 1000.0
            * demo["p_el_eur_mwh"]
            - demo["om_base_eur_anno"]) == pytest.approx(
        demo["gas_kwh_anno"] / 1000.0
        * demo["breakeven_gas_eur_mwh"])


def test_breakeven_soglia_minima():
    """Sopra la soglia l'alternativa vince, sotto perde."""
    be = mh783_demo_calcoli()["breakeven_gas_eur_mwh"]
    assert _variante(p_gas_eur_mwh=be + 1)[
        "c_alt_eur_anno"] < _variante(p_gas_eur_mwh=be + 1)[
        "c_base_eur_anno"]
    assert _variante(p_gas_eur_mwh=be - 1)[
        "c_alt_eur_anno"] > _variante(p_gas_eur_mwh=be - 1)[
        "c_base_eur_anno"]


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh783_flussi(8000, 1016.0714285714284, 12)
    assert len(fl) == 13
    assert fl[0] == -8000
    assert all(f == 1016.0714285714284 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh783_demo_calcoli()
    assert bc["van"] == pytest.approx(1005.6967520345902)
    assert mh783_van([-8000] + [1016.0714285714284] * 12,
                     0) == pytest.approx(4192.857142857141)
    assert mh783_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh783_demo_calcoli()
    assert bc["tir"] == pytest.approx(7.16463253469231)
    assert mh783_tir([-8000] + [1016.0714285714284] * 12) == \
        pytest.approx(0.0716463253469231)
    tir = mh783_tir([-8000] + [1016.0714285714284] * 12)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-8000] + [1016.0714285714284] * 12))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh783_payback([-8000] + [1016.0714285714284] * 12) == 8
    assert mh783_payback([-8000] + [-1000.0] * 12) is None
    assert mh783_payback([0] + [1016.0714285714284] * 12) == 0
    assert mh783_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh783_verdetto(1016.0714285714284, 1005.6967520345902, 8000,
                          10.0) == "CONVIENTE"
    assert mh783_verdetto(1016.0714285714284, 0.0, 8000, 10.0) == "MARGINALE"
    assert mh783_verdetto(1016.0714285714284, -800.0, 8000, 10.0) == "MARGINALE"
    assert mh783_verdetto(1016.0714285714284, -800.01, 8000, 10.0) == "NON_CONVIENTE"
    assert mh783_verdetto(1016.0714285714284, -7857.55, 8000, 10.0) == "NON_CONVIENTE"
    assert mh783_verdetto(0.0, 1005.6967520345902, 8000,
                          10.0) == "NON_CALCOLABILE"
    assert mh783_verdetto(-150.59523809523762, -9334.76, 8000,
                          10.0) == "NON_CALCOLABILE"
    assert mh783_verdetto(None, 1005.6967520345902, 8000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh783_verdetto(float("nan"), 1005.0, 8000, 10.0)
    with pytest.raises(ValueError):
        mh783_verdetto(1016.07, 1005.0, -1, 10.0)
    with pytest.raises(ValueError):
        mh783_verdetto(1016.07, 1005.0, 8000, 100.1)


def test_valida_demo_ok():
    v = mh783_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("kg", "60000"),
                       ("kg", float("nan")),
                       ("kg", float("inf")),
                       ("kg", True),
                       ("p_gas_eur_mwh", None),
                       ("q_past_kwh_per_kg", "0.25")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh783_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("kg", 0), ("kg", -1),
                          ("q_past_kwh_per_kg", -0.1),
                          ("q_freddo_kwh_per_kg", -0.1),
                          ("eta_caldaia", 0),
                          ("eta_caldaia", 1.01),
                          ("cop_chill_base", 1.0),
                          ("cop_chill_base", 0.5),
                          ("cop_pdc", 1.0),
                          ("cop_chill_alt", 1.0),
                          ("p_gas_eur_mwh", -1),
                          ("p_el_eur_mwh", -1),
                          ("om_base_eur_anno", -100),
                          ("om_alt_eur_anno", -100),
                          ("capex_eur", -1),
                          ("wacc_pct", -0.1), ("wacc_pct", 50.1),
                          ("vita_anni", 0), ("vita_anni", 2.5),
                          ("f_gas_t_per_mwh", -0.10),
                          ("f_el_t_per_mwh", -0.10),
                          ("tolleranza_pct", -1),
                          ("tolleranza_pct", 100.1)):
        d = _demo_kwargs()
        d[campo] = valore
        assert mh783_valida(**d)["valido"] is False


def test_valida_specifici_entrambi_nulli_rifiutata():
    d = _demo_kwargs()
    d["q_past_kwh_per_kg"] = 0
    d["q_freddo_kwh_per_kg"] = 0
    assert mh783_valida(**d)["valido"] is False
    with pytest.raises(ValueError):
        _variante(q_past_kwh_per_kg=0, q_freddo_kwh_per_kg=0)


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"q_past_kwh_per_kg": 0,
              "p_gas_eur_mwh": 0,
              "p_el_eur_mwh": 0,
              "om_base_eur_anno": 0, "om_alt_eur_anno": 0,
              "capex_eur": 0, "wacc_pct": 0,
              "f_gas_t_per_mwh": 0, "f_el_t_per_mwh": 0,
              "tolleranza_pct": 0})
    assert mh783_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["q_past_kwh_per_kg"] = 0.25
    d["q_freddo_kwh_per_kg"] = 0
    assert mh783_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh783_demo()
    assert d["kg"] == 60000
    assert d["q_past_kwh_per_kg"] == 0.25
    assert d["q_freddo_kwh_per_kg"] == 0.60
    assert d["eta_caldaia"] == 0.9
    assert d["cop_chill_base"] == 2.5
    assert d["cop_pdc"] == 3.5
    assert d["cop_chill_alt"] == 3.2
    assert d["p_gas_eur_mwh"] == 90
    assert d["p_el_eur_mwh"] == 250
    assert d["om_base_eur_anno"] == 800
    assert d["om_alt_eur_anno"] == 1000
    assert d["capex_eur"] == 8000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 12
    assert d["f_gas_t_per_mwh"] == 0.20
    assert d["f_el_t_per_mwh"] == 0.35
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    """Tutti gli output numerici demo a tolleranza
    1e-9 relativa: confronto delle costanti _DEMO
    contro mh783_demo_calcoli()."""
    bc = mh783_demo_calcoli()
    for chiave, atteso in _DEMO.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert got == pytest.approx(atteso, rel=1e-9), chiave
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True
    assert demo_calcoli()["van"] == bc["van"]


def test_demo_calcoli_fisica_economia():
    bc = mh783_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(5900.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(4883.928571428572)
    assert bc["risparmio_eur_anno"] == pytest.approx(1016.0714285714284)
    assert bc["co2_base_t_anno"] == pytest.approx(8.373333333333335)
    assert bc["co2_alt_t_anno"] == pytest.approx(5.4375)
    assert bc["co2_evitata_t_anno"] == pytest.approx(2.935833333333335)
    assert bc["gas_kwh_anno"] == pytest.approx(16666.666666666668)


def test_demo_flussi_e_cumulato():
    bc = mh783_demo_calcoli()
    assert bc["flussi"][0] == -8000
    assert len(bc["flussi"]) == 13
    assert all(f == pytest.approx(1016.0714285714284) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -8000
    assert righe.iloc[7]["Cumulato (EUR)"] == pytest.approx(-887.5)
    assert righe.iloc[8]["Cumulato (EUR)"] == pytest.approx(128.57142857142753)
    assert righe.iloc[12]["Cumulato (EUR)"] == pytest.approx(4192.857142857141)


def test_demo_tabella_righe():
    bc = mh783_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Calore pastorizzazione (kWh_th/anno)"] == pytest.approx(15000.0)
    assert mappa["Freddo mantecazione e conservazione (kWh_th/anno)"] == pytest.approx(36000.0)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(16666.666666666668)
    assert mappa["Elettricita' alternativa totale (kWh_e/anno)"] == pytest.approx(15535.714285714286)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(5900.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(4883.928571428572)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(1016.0714285714284)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(2.935833333333335)
    assert mappa["Payback (anni)"] == 8
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] == \
        pytest.approx(29.035714285714292)


def test_demo_coerenza_interna():
    bc = mh783_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["q_past_kwh_anno"] == pytest.approx(
        bc["kg"] * bc["q_past_kwh_per_kg"])
    assert bc["q_freddo_kwh_anno"] == pytest.approx(
        bc["kg"] * bc["q_freddo_kwh_per_kg"])
    assert bc["gas_kwh_anno"] == pytest.approx(
        bc["q_past_kwh_anno"] / bc["eta_caldaia"])
    assert bc["e_alt_kwh_anno"] == pytest.approx(
        bc["e_pdc_kwh_anno"] + bc["e_chill_alt_kwh_anno"])
    assert bc["co2_evitata_t_anno"] == pytest.approx(
        bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])
    # L'elettricita' del freddo entra in entrambi i
    # casi: C_base usa il chiller tradizionale,
    # C_alt usa pompa di calore + chiller efficiente.
    assert bc["c_base_eur_anno"] == pytest.approx(
        bc["gas_kwh_anno"] / 1000.0 * bc["p_gas_eur_mwh"]
        + bc["e_chill_base_kwh_anno"] / 1000.0
        * bc["p_el_eur_mwh"] + bc["om_base_eur_anno"])
    assert bc["c_alt_eur_anno"] == pytest.approx(
        bc["e_alt_kwh_anno"] / 1000.0 * bc["p_el_eur_mwh"]
        + bc["om_alt_eur_anno"])


def test_demo_contro_riconteggio_indipendente():
    kg, qp_spec, qf_spec = 60000, 0.25, 0.60
    eta, copb, copp, copa = 0.9, 2.5, 3.5, 3.2
    pg, pel, omb, oma, cx = 90, 250, 800, 1000, 8000
    fg, fel, wacc, vita = 0.20, 0.35, 5.0, 12
    qp = kg * qp_spec
    qf = kg * qf_spec
    gas = qp / eta
    eb = qf / copb
    ep = qp / copp
    ea_chill = qf / copa
    ea = ep + ea_chill
    cb = gas / 1000.0 * pg + eb / 1000.0 * pel + omb
    ca = ea / 1000.0 * pel + oma
    risp = cb - ca
    co2b = gas / 1000.0 * fg + eb / 1000.0 * fel
    co2a = ea / 1000.0 * fel
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    be = (ea / 1000.0 * pel + oma - eb / 1000.0 * pel - omb) / (gas / 1000.0)
    bc = mh783_demo_calcoli()
    assert bc["q_past_kwh_anno"] == pytest.approx(qp)
    assert bc["q_freddo_kwh_anno"] == pytest.approx(qf)
    assert bc["gas_kwh_anno"] == pytest.approx(gas)
    assert bc["e_chill_base_kwh_anno"] == pytest.approx(eb)
    assert bc["e_pdc_kwh_anno"] == pytest.approx(ep)
    assert bc["e_chill_alt_kwh_anno"] == pytest.approx(ea_chill)
    assert bc["e_alt_kwh_anno"] == pytest.approx(ea)
    assert bc["c_base_eur_anno"] == pytest.approx(cb)
    assert bc["c_alt_eur_anno"] == pytest.approx(ca)
    assert bc["risparmio_eur_anno"] == pytest.approx(risp)
    assert bc["co2_base_t_anno"] == pytest.approx(co2b)
    assert bc["co2_alt_t_anno"] == pytest.approx(co2a)
    assert bc["co2_evitata_t_anno"] == pytest.approx(co2)
    assert bc["van"] == pytest.approx(van)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(be)


# ---------------------------------------------------------------- varianti
def test_variante_gas_basso_risparmio_positivo_ma_non_conviente():
    """Gas 30 EUR/MWh: risparmio ancora positivo
    (16,07) ma VAN -7.857,55 oltre la tolleranza
    (800): NON_CONVIENTE. Il verdetto guarda la
    VAN, non il solo risparmio positivo."""
    bc = _variante(p_gas_eur_mwh=30)
    assert bc["risparmio_eur_anno"] == pytest.approx(16.07142857142844)
    assert bc["van"] == pytest.approx(-7857.554884414216)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_gas_20_non_calcolabile():
    """Gas 20 EUR/MWh: risparmio -150,60, verdetto
    NON_CALCOLABILE, ma helper calcolabili
    (flussi pieni, VAN -9.334,76, TIR None,
    payback None)."""
    bc = _variante(p_gas_eur_mwh=20)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(-150.59523809523762)
    assert bc["van"] == pytest.approx(-9334.763490489013)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_capex_alto_marginale_e_non_conviente():
    bc = _variante(capex_eur=10000)
    assert bc["risparmio_eur_anno"] == pytest.approx(1016.0714285714284)
    assert bc["van"] == pytest.approx(-994.3032479654106)
    assert bc["payback"] == 10
    assert bc["verdetto"] == "MARGINALE"
    bc2 = _variante(capex_eur=11000)
    assert bc2["van"] == pytest.approx(-1994.303247965409)
    assert bc2["payback"] == 11
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex_eur=0)
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(9005.696752034592, rel=1e-6)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(4192.857142857141)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=8)
    assert len(bc2["flussi"]) == 9
    assert bc2["van"] == pytest.approx(-1432.9141783686819)
    assert bc2["payback"] == 8
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_el_alto_marginale():
    """Elettricita' 400 EUR/MWh: risparmio 845,71,
    VAN -504,22 entro la tolleranza (800):
    MARGINALE, payback 10, breakeven gas 39,26
    (sale perche' l'alternativa elettrica costa
    di piu')."""
    bc = _variante(p_el_eur_mwh=400)
    assert bc["risparmio_eur_anno"] == pytest.approx(845.7142857142853)
    assert bc["van"] == pytest.approx(-504.2214731747251)
    assert bc["payback"] == 10
    assert bc["verdetto"] == "MARGINALE"
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(39.25714285714288)


def test_variante_solo_freddo_breakeven_none():
    """Solo freddo (q_past zero): gas zero, breakeven
    None, risparmio 587,50 (solo chiller
    efficiente), VAN -2.792,84, NON_CONVIENTE."""
    bc = _variante(q_past_kwh_per_kg=0)
    assert bc["gas_kwh_anno"] == 0.0
    assert bc["e_pdc_kwh_anno"] == 0.0
    assert bc["e_alt_kwh_anno"] == pytest.approx(11250.0)
    assert bc["c_base_eur_anno"] == pytest.approx(4400.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(3812.5)
    assert bc["risparmio_eur_anno"] == pytest.approx(587.5)
    assert bc["van"] == pytest.approx(-2792.839663586327)
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_solo_pastorizzazione():
    """Solo pastorizzazione (q_freddo zero):
    risparmio 228,57, breakeven 76,29, VAN
    -5.974,11, NON_CONVIENTE."""
    bc = _variante(q_freddo_kwh_per_kg=0)
    assert bc["q_freddo_kwh_anno"] == 0.0
    assert bc["e_chill_base_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(228.57142857142844)
    assert bc["van"] == pytest.approx(-5974.1139116688455)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(76.28571428571429)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_cop_pdc_basso():
    """COP pompa di calore 2,5 invece di 3,5:
    E_pdc 6.000, E_alt 17.250, risparmio 587,50,
    VAN -2.792,84, breakeven 54,75, NON_CONVIENTE."""
    bc = _variante(cop_pdc=2.5)
    assert bc["e_pdc_kwh_anno"] == pytest.approx(6000.0)
    assert bc["e_alt_kwh_anno"] == pytest.approx(17250.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(587.5)
    assert bc["van"] == pytest.approx(-2792.839663586327)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(54.75)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_produzione_dimezzata():
    """Produzione 30.000 kg: tutti i vettori si
    dimezzano, il risparmio scende a 408,04, la VAN
    e' -4.383,48, NON_CONVIENTE (il CAPEX non si
    dimezza)."""
    bc = _variante(kg=30000)
    assert bc["q_past_kwh_anno"] == pytest.approx(7500.0)
    assert bc["q_freddo_kwh_anno"] == pytest.approx(18000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(408.0357142857142)
    assert bc["van"] == pytest.approx(-4383.4767876275855)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(41.03571428571429)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_monotonia_prezzo_gas_crescente():
    base = mh783_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas_eur_mwh=91)["risparmio_eur_anno"]
    basso = _variante(p_gas_eur_mwh=89)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(16.666666666666668)
    assert base - basso == pytest.approx(16.666666666666668)


def test_monotonia_produzione_crescente():
    """Il risparmio cresce con la produzione (meno
    O&M fissi per kg) finche' i vettori crescono."""
    assert _variante(kg=30000)["risparmio_eur_anno"] < \
        mh783_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(kg=120000)["risparmio_eur_anno"] > \
        mh783_demo_calcoli()["risparmio_eur_anno"]


def test_demo_deterministica_due_chiamate():
    a = mh783_demo_calcoli()
    b = mh783_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh783_demo().keys()) == {
        "kg", "q_past_kwh_per_kg", "q_freddo_kwh_per_kg",
        "eta_caldaia", "cop_chill_base", "cop_pdc",
        "cop_chill_alt", "p_gas_eur_mwh", "p_el_eur_mwh",
        "om_base_eur_anno", "om_alt_eur_anno",
        "capex_eur", "wacc_pct", "vita_anni",
        "f_gas_t_per_mwh", "f_el_t_per_mwh",
        "tolleranza_pct"}


# ---------------------------------------------------------------- degenere
def test_degenere_cop_uguale_uno_sollevela():
    with pytest.raises(ValueError):
        _variante(cop_pdc=1.0)


def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"kg": 0}, {"kg": -1},
               {"q_past_kwh_per_kg": -0.1},
               {"q_freddo_kwh_per_kg": -0.1},
               {"eta_caldaia": 0}, {"eta_caldaia": 1.01},
               {"cop_chill_base": 1.0},
               {"cop_chill_base": 0.5},
               {"cop_pdc": 1.0}, {"cop_chill_alt": 1.0},
               {"p_gas_eur_mwh": -1},
               {"p_el_eur_mwh": -1},
               {"om_base_eur_anno": -100},
               {"om_alt_eur_anno": -100},
               {"capex_eur": -1},
               {"wacc_pct": -1}, {"wacc_pct": 60},
               {"vita_anni": 0}, {"vita_anni": 2.5},
               {"f_gas_t_per_mwh": -0.10},
               {"f_el_t_per_mwh": -0.10},
               {"tolleranza_pct": -1},
               {"tolleranza_pct": 100.1}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh783_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"kg": "60000"},
               {"kg": float("nan")},
               {"p_gas_eur_mwh": float("inf")},
               {"capex_eur": True},
               {"q_past_kwh_per_kg": "0.25"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh783_valida(**d)["valido"] is False


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    """Differenza chiave: risparmio <= 0 NON solleva
    negli helper (resta calcolabile con flussi, VAN,
    TIR e payback), ma il verdetto e' NON_CALCOLABILE
    e la UI salta KPI, grafico, tabella e CSV."""
    for kw in ({"p_gas_eur_mwh": 20},
               {"p_gas_eur_mwh": 29.035714285714292}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] <= 0.0
        assert bc["verdetto"] == "NON_CALCOLABILE"
        assert bc["flussi"]


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh783_demo_calcoli()
    testo = mh783_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_gas_eur_mwh" in testo
    assert "co2_evitata_t_anno" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh783_demo_calcoli()
    testo = mh783_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"q_past_kwh_anno;{bc['q_past_kwh_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh783_demo_calcoli()
    testo = mh783_csv(bc, _demo_kwargs())
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
    # Token della tab precedente, costruiti
    # per concatenazione: questo stesso file non li contiene
    # come sottostringhe contigue.
    return ["mh" + "78" + "2", "st" + "78" + "2",
            "tab" + "78" + "2", "mace" + "lleria"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w784_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w784_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab783:")


def test_registry_chain_tail_and_count():
    """Registry della nuova tab: il frammento UI apre la tab
    numero 783 (la coda della catena termina con la nuova tab
    e il conteggio atteso delle tab e' 783)."""
    src = _leggi("w784_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 783
    assert src.count("with tab783:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w784_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w784_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st783_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) >= 19
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w784_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 2
    # Entrambe le guard (input degenere e risparmio <= 0)
    # stanno prima di KPI / grafico / tabella / CSV.
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w784_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def783[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w784_ui.py")
        usate = set(re.findall(r'_def783\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 17
        assert usate <= set(mh783_demo().keys())
