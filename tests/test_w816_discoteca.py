"""Test nuova scheda "Discoteca / locale
notturno: pompa di calore + recupero
calore ventilazione + LED battono caldaia
a gas + chiller + illuminazione
tradizionale?" (titolo completo nel
frammento UI).

Business case deterministico di una
discoteca guidato dalla SUPERFICIE in m2
piu' le SERATE di apertura: Q_risc = S x
q_risc; Q_raff = S x q_raff; Q_acs =
n_serate x q_acs_serata; Q_risc_net =
Q_risc x (1 - f_rec) (il recupero riduce
solo il riscaldamento); E_pdc_risc =
Q_risc_net / cop_risc; E_pdc_raff = Q_raff
/ cop_raff_alt; E_raff_base = Q_raff /
cop_chiller; E_ill_base = S x e_ill;
E_ill_alt = E_ill_base x f_led (i LED
riducono solo l'illuminazione); E_bar_base
= S x e_bar; E_bar_alt = E_bar_base x
f_bar (i frigo efficienti riducono solo i
frigo bar); E_base = E_raff_base +
E_ill_base + E_bar_base; E_alt = E_pdc_risc
+ E_pdc_raff + E_ill_alt + E_bar_alt;
gas_base = (Q_risc + Q_acs) / eta_cald;
gas_alt = Q_acs / eta_cald (l'ACS resta a
gas in entrambi); C_base = E_base / 1000 x
p_el + gas_base / 1000 x p_gas + OM_base;
C_alt = E_alt / 1000 x p_el + gas_alt /
1000 x p_gas + OM_alt; risparmio = C_base
- C_alt; CO2 evitata = (E_base x 0,35 +
gas_base x 0,20 - E_alt x 0,35 - gas_alt x
0,20) / 1000 (fattori letterali);
flussi [-CAPEX, risparmio x vita]; VAN,
TIR, payback (primo anno con cumulato >=
0); breakeven gas = (E_alt / 1000 x p_el +
OM_alt - E_base / 1000 x p_el - OM_base) x
1000 / (gas_base - gas_alt) EUR/MWh, None
se gas_base <= gas_alt o numeratore < 0,
SOGLIA MINIMA quando esiste. Nel demo il
breakeven e' 9,867857142857169 EUR/MWh
(numeratore 1.052,5714285714286 EUR,
denominatore 106.666,66666666666 kWh/anno).
Verdetto: NON_CALCOLABILE se input
degenere (superficie <= 0, specifici
negativi, recupero fuori [0, 1], COP <= 0,
fattori fuori [0, 1], ACS o serate
negative, rendimento caldaia <= 0 o sopra
1, prezzi <= 0, O&M negativi, CAPEX <= 0,
WACC negativo, vita <= 0, tolleranza
negativa) o se risparmio <= 0 (guard
degenere: UI salta KPI, grafico, tabella
e CSV); altrimenti CONVIENTE se VAN > 0,
MARGINALE se VAN negativa entro tolleranza
% del CAPEX, NON_CONVIENTE se VAN negativa
oltre la tolleranza. Guard UI IDENTICA
agli helper: nessuna divergenza di
verdetto. Tutti gli slider UI hanno minimo
0, quindi i casi negativi sono NON
RAGGIUNGIBILI via slider, ma la guard li
controlla comunque; i casi = 0 raggiungibili
via slider sono bloccati in UI esattamente
come negli helper dove previsto
(superficie, COP, rendimento caldaia,
prezzi, CAPEX, vita). Gli zeri ammessi in
entrambi (specifici, recupero 0 o 1,
fattore LED 0 o 1, fattore frigo bar 0 o 1,
ACS per serata, serate, O&M, WACC,
tolleranza) non creano divergenza: con
serate zero l'ACS e' zero e il gas
alternativo e' zero, e il caso resta
calcolabile in entrambi. COP sopra 6, WACC
sopra 20 % e tolleranza sopra 100 % sono
ammessi negli helper e limitati solo dagli
slider UI (6, 20, 100): nessuna divergenza
nel range raggiungibile, perche' la guard
controlla solo gli stessi limiti degli
helper. Distinzione esplicita: distinto
dal depuratore (m3 di reflui, cogenerazione
e soffianti: qui niente reflui, niente
cogenerazione, niente soffianti), dal
centro commerciale (m2 di superficie di
vendita, ore di apertura, banchi frigo,
scale mobili: qui niente superficie di
vendita, niente banchi frigo, niente scale
mobili), dall'officina (m2 di capannone,
portata di aria compressa: qui niente aria
compressa, niente compressore), dalla
chiesa (m2 di navata, panche: qui niente
panche, niente navata), dall'asilo (giorni
di apertura, mensa, lavanderia: qui niente
mensa, niente pasti, niente lavanderia),
dall'albergo (pernottamenti e camere: qui
nessun pernottamento, nessuna camera): qui
driver SUPERFICIE + SERATE + RECUPERO +
LED + FRIGO BAR.

Demo (discoteca): 800 m2, riscaldamento
specifico 120 (96.000 kWh_th/anno) e
raffrescamento specifico 90 (72.000
kWh_th/anno), recupero 0,35 (riscaldamento
netto 62.400 kWh_th/anno), COP riscaldamento
3,2 (19.500 kWh_e/anno) e COP raffrescamento
alternativo 4,0 (18.000 kWh_e/anno), COP
chiller 2,8 (25.714,285714285717
kWh_e/anno), illuminazione specifica 60
(48.000 kWh_e/anno) con fattore LED 0,45
(21.600 kWh_e/anno), frigo bar specifico 25
(20.000 kWh_e/anno) con fattore frigo bar
0,70 (14.000 kWh_e/anno), ACS 120 kWh_th a
serata per 150 serate (18.000 kWh_th/anno),
rendimento caldaia 0,90 (gas base
126.666,66666666666 e gas alternativo
20.000 kWh/anno), prezzi elettricita' 240 e
gas 100 EUR/MWh, O&M base 8.000 e
alternativo 14.000 EUR/anno, CAPEX 85.000
EUR, WACC 5 %, vita 15 anni, tolleranza
10 % del CAPEX. Valori calcolati
eseguendo mh816_demo_calcoli(): E_base
93.714,28571428571, E_alt 73.100, C_base
43.158,09523809524, C_alt 33.544, risparmio
9.614,095238095237, CO2_base
58,133333333333326, CO2_alt 29,585,
CO2_evitata 28,548333333333325, VAN
14.791,020917928967, TIR 7,474372201258057
%, payback 9, breakeven gas
9,867857142857169 EUR/MWh (SOGLIA MINIMA),
verdetto CONVIENTE. I valori del brief
(C_base 43.158,10, C_alt 33.544,00,
risparmio 9.614,10, CO2 evitata 28,55 t,
VAN circa 14.791, TIR circa 7,5 %,
payback 9, breakeven circa 9,87 EUR/MWh)
sono gli stessi numeri arrotondati:
nessuna discrepanza sostanziale, solo
arrotondamento (TIR esatta 7,474 %,
arrotondata a una cifra 7,5 %).
"""

import ast
import inspect
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w817_helpers import (
    demo_calcoli,
    mh816_breakeven_gas,
    mh816_c_alt,
    mh816_c_base,
    mh816_calcola,
    mh816_co2_alt,
    mh816_co2_base,
    mh816_co2_evitata,
    mh816_csv,
    mh816_demo,
    mh816_demo_calcoli,
    mh816_e_alt,
    mh816_e_bar_alt,
    mh816_e_bar_base,
    mh816_e_base,
    mh816_e_ill_alt,
    mh816_e_ill_base,
    mh816_e_pdc_raff,
    mh816_e_pdc_risc,
    mh816_e_raff_base,
    mh816_eta,
    mh816_flussi,
    mh816_frazione,
    mh816_gas_alt,
    mh816_gas_base,
    mh816_int_pos,
    mh816_nneg,
    mh816_num,
    mh816_payback,
    mh816_pos,
    mh816_q_acs,
    mh816_q_raff,
    mh816_q_risc,
    mh816_q_risc_net,
    mh816_risparmio,
    mh816_tir,
    mh816_valida,
    mh816_van,
    mh816_verdetto,
)

_DEMO = {
    "q_risc_kwh_th_anno": 96000.0,
    "q_raff_kwh_th_anno": 72000.0,
    "q_acs_kwh_th_anno": 18000.0,
    "q_risc_net_kwh_th_anno": 62400.0,
    "e_pdc_risc_kwh_e_anno": 19500.0,
    "e_pdc_raff_kwh_e_anno": 18000.0,
    "e_raff_base_kwh_e_anno": 25714.285714285717,
    "e_ill_base_kwh_e_anno": 48000.0,
    "e_ill_alt_kwh_e_anno": 21600.0,
    "e_bar_base_kwh_e_anno": 20000.0,
    "e_bar_alt_kwh_e_anno": 14000.0,
    "e_base_kwh_e_anno": 93714.28571428571,
    "e_alt_kwh_e_anno": 73100.0,
    "gas_base_kwh_anno": 126666.66666666666,
    "gas_alt_kwh_anno": 20000.0,
    "c_base_eur_anno": 43158.09523809524,
    "c_alt_eur_anno": 33544.0,
    "risparmio_eur_anno": 9614.095238095237,
    "co2_base_t_anno": 58.133333333333326,
    "co2_alt_t_anno": 29.585,
    "co2_evitata_t_anno": 28.548333333333325,
    "van": 14791.020917928967,
    "tir": 7.474372201258057,
}


def _demo_kwargs():
    return dict(mh816_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh816_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh816_num(3, "x") == 3.0
    assert mh816_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh816_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh816_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh816_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh816_pos(0, "x")
    with pytest.raises(ValueError):
        mh816_pos(-1, "x")
    assert mh816_pos(0.5, "x") == 0.5


def test_frazione_limiti():
    assert mh816_frazione(0, "x") == 0.0
    assert mh816_frazione(1, "x") == 1.0
    assert mh816_frazione(0.35, "x") == 0.35
    with pytest.raises(ValueError):
        mh816_frazione(-0.01, "x")
    with pytest.raises(ValueError):
        mh816_frazione(1.01, "x")


def test_eta_limiti():
    assert mh816_eta(1, "x") == 1.0
    assert mh816_eta(0.90, "x") == 0.90
    with pytest.raises(ValueError):
        mh816_eta(0, "x")
    with pytest.raises(ValueError):
        mh816_eta(-0.1, "x")
    with pytest.raises(ValueError):
        mh816_eta(1.01, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh816_int_pos(5.0, "x") == 5
    assert mh816_int_pos(15.0, "x") == 15
    with pytest.raises(ValueError):
        mh816_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh816_int_pos(0, "x")


# ---------------------------------------------------------------- fisica base
def test_q_risc_q_raff_q_acs():
    assert mh816_q_risc(800, 120) == 96000.0
    assert mh816_q_raff(800, 90) == 72000.0
    assert mh816_q_acs(150, 120) == 18000.0
    assert mh816_q_risc(800, 0) == 0.0
    assert mh816_q_acs(0, 120) == 0.0
    with pytest.raises(ValueError):
        mh816_q_risc(0, 120)
    with pytest.raises(ValueError):
        mh816_q_risc(800, -1)
    with pytest.raises(ValueError):
        mh816_q_acs(150, -1)
    with pytest.raises(ValueError):
        mh816_q_acs(-1, 120)


def test_q_risc_net_e_pdc():
    assert mh816_q_risc_net(96000.0, 0.35) == 62400.0
    assert mh816_q_risc_net(96000.0, 0) == 96000.0
    assert mh816_q_risc_net(96000.0, 1) == 0.0
    with pytest.raises(ValueError):
        mh816_q_risc_net(96000.0, 1.01)
    assert mh816_e_pdc_risc(62400.0, 3.2) == 19500.0
    assert mh816_e_pdc_raff(72000.0, 4.0) == 18000.0
    assert mh816_e_raff_base(72000.0, 2.8) == pytest.approx(25714.285714285717)
    with pytest.raises(ValueError):
        mh816_e_pdc_risc(62400.0, 0)
    with pytest.raises(ValueError):
        mh816_e_pdc_raff(72000.0, 0)
    with pytest.raises(ValueError):
        mh816_e_raff_base(72000.0, 0)
    # COP sopra 6 ammessi negli helper (slider li limita a 6).
    assert mh816_e_pdc_risc(62400.0, 7.0) == pytest.approx(8914.285714285714)


def test_e_ill_e_bar():
    assert mh816_e_ill_base(800, 60) == 48000.0
    assert mh816_e_ill_alt(48000.0, 0.45) == 21600.0
    assert mh816_e_ill_alt(48000.0, 1) == 48000.0
    assert mh816_e_ill_alt(48000.0, 0) == 0.0
    assert mh816_e_bar_base(800, 25) == 20000.0
    assert mh816_e_bar_alt(20000.0, 0.70) == 14000.0
    with pytest.raises(ValueError):
        mh816_e_ill_alt(48000.0, 1.01)
    with pytest.raises(ValueError):
        mh816_e_bar_alt(20000.0, -0.01)
    with pytest.raises(ValueError):
        mh816_e_ill_base(0, 60)


def test_e_base_e_alt():
    assert mh816_e_base(25714.285714285717, 48000.0,
                        20000.0) == pytest.approx(93714.28571428571)
    assert mh816_e_alt(19500.0, 18000.0, 21600.0,
                       14000.0) == 73100.0
    with pytest.raises(ValueError):
        mh816_e_base(-1, 48000.0, 20000.0)
    with pytest.raises(ValueError):
        mh816_e_alt(19500.0, 18000.0, 21600.0, -1)


def test_gas_base_alt():
    assert mh816_gas_base(96000.0, 18000.0,
                          0.90) == pytest.approx(126666.66666666666)
    assert mh816_gas_alt(18000.0, 0.90) == 20000.0
    assert mh816_gas_alt(0, 0.90) == 0.0
    assert mh816_gas_base(96000.0, 0, 0.90) == pytest.approx(106666.66666666666)
    with pytest.raises(ValueError):
        mh816_gas_base(96000.0, 18000.0, 0)
    with pytest.raises(ValueError):
        mh816_gas_alt(18000.0, 1.01)


def test_c_base_c_alt_scomposizione():
    assert mh816_c_base(93714.28571428571, 240, 126666.66666666666, 100,
                        8000) == pytest.approx(43158.09523809524)
    assert mh816_c_alt(73100.0, 240, 20000.0, 100,
                       14000) == pytest.approx(33544.0)
    with pytest.raises(ValueError):
        mh816_c_base(93714.28571428571, 0, 126666.66666666666, 100, 8000)
    with pytest.raises(ValueError):
        mh816_c_alt(73100.0, 240, 20000.0, 0, 14000)
    with pytest.raises(ValueError):
        mh816_c_base(93714.28571428571, 240, 126666.66666666666, 100, -1)


def test_risparmio_segno():
    assert mh816_risparmio(43158.09523809524, 33544.0) == pytest.approx(9614.095238095237)
    assert mh816_risparmio(33544.0, 33544.0) == pytest.approx(0.0, abs=1e-9)


def test_co2_base_alt_evitata():
    assert mh816_co2_base(93714.28571428571,
                          126666.66666666666) == pytest.approx(58.133333333333326)
    assert mh816_co2_alt(73100.0, 20000.0) == pytest.approx(29.585)
    assert mh816_co2_evitata(93714.28571428571, 126666.66666666666,
                             73100.0, 20000.0) == pytest.approx(28.548333333333325)
    assert mh816_co2_base(0, 0) == 0.0
    assert mh816_co2_alt(0, 0) == 0.0
    with pytest.raises(ValueError):
        mh816_co2_base(93714.28571428571, -1)
    with pytest.raises(ValueError):
        mh816_co2_alt(-1, 20000.0)


def test_breakeven_demo_e_varianti():
    bc = mh816_demo_calcoli()
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(9.867857142857169)
    assert mh816_breakeven_gas(73100.0, 240, 14000, 93714.28571428571,
                               8000, 126666.66666666666,
                               20000.0) == pytest.approx(9.867857142857169)
    # Denominatore nullo (gas_alt = gas_base) -> None.
    assert mh816_breakeven_gas(73100.0, 240, 14000, 93714.28571428571,
                               8000, 20000.0, 20000.0) is None
    # Numeratore negativo (elettricita' a 400) -> None.
    assert _variante(p_el=400)["breakeven_gas_eur_mwh"] is None
    with pytest.raises(ValueError):
        mh816_breakeven_gas(73100.0, 240, 14000, 93714.28571428571,
                            8000, -1, 20000.0)


def test_breakeven_verifica_pareggio_su_variante():
    # Variante breakeven valida: O&M alternativo
    # 20.000 EUR/anno, breakeven 66,11785714285718.
    be = _variante(om_alt=20000)["breakeven_gas_eur_mwh"]
    assert be == pytest.approx(66.11785714285718)
    bc = _variante(om_alt=20000, p_gas=be)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_breakeven_soglia_minima_su_variante():
    be = _variante(om_alt=20000)["breakeven_gas_eur_mwh"]
    bc_alto = _variante(om_alt=20000, p_gas=be + 1)
    bc_basso = _variante(om_alt=20000, p_gas=be - 1)
    assert bc_alto["c_alt_eur_anno"] < bc_alto["c_base_eur_anno"]
    assert bc_basso["c_alt_eur_anno"] > bc_basso["c_base_eur_anno"]
    assert bc_alto["risparmio_eur_anno"] > 0.0
    assert bc_alto["verdetto"] == "NON_CONVIENTE"
    assert bc_basso["verdetto"] == "NON_CALCOLABILE"


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh816_flussi(85000, 9614.095238095237, 15)
    assert len(fl) == 16
    assert fl[0] == -85000
    assert all(f == pytest.approx(9614.095238095237) for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh816_demo_calcoli()
    assert bc["van"] == pytest.approx(14791.020917928967)
    assert mh816_van([-85000] + [9614.095238095237] * 15,
                     0) == pytest.approx(59211.42857142855)
    assert mh816_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh816_demo_calcoli()
    assert bc["tir"] == pytest.approx(7.474372201258057)
    assert mh816_tir([-85000] + [9614.095238095237] * 15) == \
        pytest.approx(0.07474372201258057)
    tir = mh816_tir([-85000] + [9614.095238095237] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-85000] + [9614.095238095237] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh816_payback([-85000] + [9614.095238095237] * 15) == 9
    assert mh816_payback([-85000] + [-1000.0] * 15) is None
    assert mh816_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh816_verdetto(9614.095238095237, 14791.020917928967, 85000,
                          10.0) == "CONVIENTE"
    assert mh816_verdetto(9614.095238095237, -1500.0, 85000,
                          10.0) == "MARGINALE"
    assert mh816_verdetto(9614.095238095237, -8500.0, 85000, 10.0) == "MARGINALE"
    assert mh816_verdetto(9614.095238095237, -8500.01, 85000, 10.0) == "NON_CONVIENTE"
    assert mh816_verdetto(9614.095238095237, 0.0, 85000, 10.0) == "MARGINALE"
    assert mh816_verdetto(0.0, 14791.02, 85000,
                          10.0) == "NON_CALCOLABILE"
    assert mh816_verdetto(-6385.90, -151283.51, 85000,
                          10.0) == "NON_CALCOLABILE"
    assert mh816_verdetto(None, 14791.02, 85000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh816_verdetto(float("nan"), 14791.02, 85000, 10.0)
    with pytest.raises(ValueError):
        mh816_verdetto(9614.095238095237, 14791.02, 0, 10.0)
    with pytest.raises(ValueError):
        mh816_verdetto(9614.095238095237, 14791.02, 85000, -1)


def test_valida_demo_ok():
    v = mh816_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("superficie_m2", "800"),
                       ("superficie_m2", float("nan")),
                       ("superficie_m2", float("inf")),
                       ("superficie_m2", True),
                       ("p_gas", None),
                       ("f_rec", "0.35")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh816_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("superficie_m2", 0),
                          ("superficie_m2", -10),
                          ("q_risc_kwh_th_m2", -0.1),
                          ("q_raff_kwh_th_m2", -0.1),
                          ("f_rec", -0.1),
                          ("f_rec", 1.01),
                          ("cop_risc", 0),
                          ("cop_risc", -1),
                          ("cop_raff_alt", 0),
                          ("cop_chiller", 0),
                          ("e_ill_kwh_e_m2", -0.1),
                          ("f_led", -0.1),
                          ("f_led", 1.01),
                          ("e_bar_kwh_e_m2", -0.1),
                          ("f_bar", -0.1),
                          ("f_bar", 1.01),
                          ("q_acs_serata_kwh_th", -0.1),
                          ("n_serate", -1),
                          ("eta_cald", 0),
                          ("eta_cald", 1.01),
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
        assert mh816_valida(**d)["valido"] is False


def test_valida_accetta_limiti_e_nessun_tetto_cop_wacc_tolleranza():
    d = _demo_kwargs()
    d.update({"q_risc_kwh_th_m2": 0,
              "q_raff_kwh_th_m2": 0,
              "f_rec": 0,
              "e_ill_kwh_e_m2": 0,
              "f_led": 0,
              "e_bar_kwh_e_m2": 0,
              "f_bar": 0,
              "q_acs_serata_kwh_th": 0,
              "n_serate": 0,
              "om_base": 0, "om_alt": 0,
              "wacc_pct": 0,
              "tolleranza_pct": 0})
    assert mh816_valida(**d)["valido"] is True
    d["f_rec"] = 1
    d["f_led"] = 1
    d["f_bar"] = 1
    d["eta_cald"] = 1
    # Il brief non impone tetti superiori a COP,
    # WACC e tolleranza: gli helper li ammettono.
    d["cop_risc"] = 7.0
    d["cop_raff_alt"] = 8.0
    d["cop_chiller"] = 7.5
    d["wacc_pct"] = 60
    d["tolleranza_pct"] = 200
    assert mh816_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh816_demo()
    assert d["superficie_m2"] == 800
    assert d["q_risc_kwh_th_m2"] == 120
    assert d["q_raff_kwh_th_m2"] == 90
    assert d["f_rec"] == 0.35
    assert d["cop_risc"] == 3.2
    assert d["cop_raff_alt"] == 4.0
    assert d["cop_chiller"] == 2.8
    assert d["e_ill_kwh_e_m2"] == 60
    assert d["f_led"] == 0.45
    assert d["e_bar_kwh_e_m2"] == 25
    assert d["f_bar"] == 0.70
    assert d["q_acs_serata_kwh_th"] == 120
    assert d["n_serate"] == 150
    assert d["eta_cald"] == 0.90
    assert d["p_el"] == 240
    assert d["p_gas"] == 100
    assert d["om_base"] == 8000
    assert d["om_alt"] == 14000
    assert d["capex"] == 85000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    bc = mh816_demo_calcoli()
    for chiave, atteso in _DEMO.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert got == pytest.approx(atteso, rel=1e-9), chiave
    assert bc["payback"] == 9
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(9.867857142857169)
    assert demo_calcoli()["van"] == bc["van"]


def test_demo_calcoli_fisica_economia():
    bc = mh816_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(43158.09523809524)
    assert bc["c_alt_eur_anno"] == pytest.approx(33544.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(9614.095238095237)
    assert bc["co2_base_t_anno"] == pytest.approx(58.133333333333326)
    assert bc["co2_alt_t_anno"] == pytest.approx(29.585)
    assert bc["co2_evitata_t_anno"] == pytest.approx(28.548333333333325)
    assert bc["q_risc_kwh_th_anno"] == pytest.approx(96000.0)
    assert bc["q_raff_kwh_th_anno"] == pytest.approx(72000.0)
    assert bc["q_acs_kwh_th_anno"] == pytest.approx(18000.0)
    assert bc["q_risc_net_kwh_th_anno"] == pytest.approx(62400.0)
    assert bc["e_pdc_risc_kwh_e_anno"] == pytest.approx(19500.0)
    assert bc["e_pdc_raff_kwh_e_anno"] == pytest.approx(18000.0)
    assert bc["e_raff_base_kwh_e_anno"] == pytest.approx(25714.285714285717)
    assert bc["e_ill_base_kwh_e_anno"] == pytest.approx(48000.0)
    assert bc["e_ill_alt_kwh_e_anno"] == pytest.approx(21600.0)
    assert bc["e_bar_base_kwh_e_anno"] == pytest.approx(20000.0)
    assert bc["e_bar_alt_kwh_e_anno"] == pytest.approx(14000.0)
    assert bc["e_base_kwh_e_anno"] == pytest.approx(93714.28571428571)
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(73100.0)
    assert bc["gas_base_kwh_anno"] == pytest.approx(126666.66666666666)
    assert bc["gas_alt_kwh_anno"] == pytest.approx(20000.0)


def test_demo_flussi_e_cumulato():
    bc = mh816_demo_calcoli()
    assert bc["flussi"][0] == -85000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(9614.095238095237) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -85000
    assert righe.iloc[8]["Cumulato (EUR)"] == pytest.approx(-8087.238095238106)
    assert righe.iloc[9]["Cumulato (EUR)"] == pytest.approx(1526.8571428571304)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(59211.42857142855)


def test_demo_tabella_righe():
    bc = mh816_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Riscaldamento (kWh_th/anno)"] == pytest.approx(96000.0)
    assert mappa["Raffrescamento (kWh_th/anno)"] == pytest.approx(72000.0)
    assert mappa["ACS (kWh_th/anno)"] == pytest.approx(18000.0)
    assert mappa["Riscaldamento netto (kWh_th/anno)"] == pytest.approx(62400.0)
    assert mappa["Elettricita' pompa di calore riscaldamento (kWh_e/anno)"] == pytest.approx(19500.0)
    assert mappa["Elettricita' pompa di calore raffrescamento (kWh_e/anno)"] == pytest.approx(18000.0)
    assert mappa["Elettricita' chiller baseline (kWh_e/anno)"] == pytest.approx(25714.285714285717)
    assert mappa["Illuminazione baseline (kWh_e/anno)"] == pytest.approx(48000.0)
    assert mappa["Illuminazione alternativa (kWh_e/anno)"] == pytest.approx(21600.0)
    assert mappa["Frigo bar baseline (kWh_e/anno)"] == pytest.approx(20000.0)
    assert mappa["Frigo bar alternativi (kWh_e/anno)"] == pytest.approx(14000.0)
    assert mappa["Elettricita' base (kWh_e/anno)"] == pytest.approx(93714.28571428571)
    assert mappa["Elettricita' alternativa (kWh_e/anno)"] == pytest.approx(73100.0)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(126666.66666666666)
    assert mappa["Gas alternativo (kWh/anno)"] == pytest.approx(20000.0)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(43158.09523809524)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(33544.0)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(9614.095238095237)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(28.548333333333325)
    assert mappa["Payback (anni)"] == 9
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] == pytest.approx(9.867857142857169)


def test_demo_coerenza_interna():
    bc = mh816_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["q_risc_kwh_th_anno"] == pytest.approx(
        bc["superficie_m2"] * bc["q_risc_kwh_th_m2"])
    assert bc["q_raff_kwh_th_anno"] == pytest.approx(
        bc["superficie_m2"] * bc["q_raff_kwh_th_m2"])
    assert bc["q_acs_kwh_th_anno"] == pytest.approx(
        bc["n_serate"] * bc["q_acs_serata_kwh_th"])
    assert bc["q_risc_net_kwh_th_anno"] == pytest.approx(
        bc["q_risc_kwh_th_anno"] * (1.0 - bc["f_rec"]))
    assert bc["e_pdc_risc_kwh_e_anno"] == pytest.approx(
        bc["q_risc_net_kwh_th_anno"] / bc["cop_risc"])
    assert bc["e_pdc_raff_kwh_e_anno"] == pytest.approx(
        bc["q_raff_kwh_th_anno"] / bc["cop_raff_alt"])
    assert bc["e_raff_base_kwh_e_anno"] == pytest.approx(
        bc["q_raff_kwh_th_anno"] / bc["cop_chiller"])
    assert bc["e_ill_base_kwh_e_anno"] == pytest.approx(
        bc["superficie_m2"] * bc["e_ill_kwh_e_m2"])
    assert bc["e_ill_alt_kwh_e_anno"] == pytest.approx(
        bc["e_ill_base_kwh_e_anno"] * bc["f_led"])
    assert bc["e_bar_base_kwh_e_anno"] == pytest.approx(
        bc["superficie_m2"] * bc["e_bar_kwh_e_m2"])
    assert bc["e_bar_alt_kwh_e_anno"] == pytest.approx(
        bc["e_bar_base_kwh_e_anno"] * bc["f_bar"])
    assert bc["e_base_kwh_e_anno"] == pytest.approx(
        bc["e_raff_base_kwh_e_anno"] + bc["e_ill_base_kwh_e_anno"]
        + bc["e_bar_base_kwh_e_anno"])
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(
        bc["e_pdc_risc_kwh_e_anno"] + bc["e_pdc_raff_kwh_e_anno"]
        + bc["e_ill_alt_kwh_e_anno"] + bc["e_bar_alt_kwh_e_anno"])
    assert bc["gas_base_kwh_anno"] == pytest.approx(
        (bc["q_risc_kwh_th_anno"] + bc["q_acs_kwh_th_anno"])
        / bc["eta_cald"])
    assert bc["gas_alt_kwh_anno"] == pytest.approx(
        bc["q_acs_kwh_th_anno"] / bc["eta_cald"])
    assert bc["co2_evitata_t_anno"] == pytest.approx(
        bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])
    assert bc["c_base_eur_anno"] == pytest.approx(
        bc["e_base_kwh_e_anno"] / 1000.0 * bc["p_el"]
        + bc["gas_base_kwh_anno"] / 1000.0 * bc["p_gas"]
        + bc["om_base"])
    assert bc["c_alt_eur_anno"] == pytest.approx(
        bc["e_alt_kwh_e_anno"] / 1000.0 * bc["p_el"]
        + bc["gas_alt_kwh_anno"] / 1000.0 * bc["p_gas"]
        + bc["om_alt"])


def test_demo_contro_riconteggio_indipendente():
    sup, qr, qf, frec = 800, 120, 90, 0.35
    copr, copf, copc = 3.2, 4.0, 2.8
    eill, fled, ebar, fbar = 60, 0.45, 25, 0.70
    qacs, nser, etac = 120, 150, 0.90
    pel, pg = 240, 100
    omb, oma, cx = 8000, 14000, 85000
    wacc, vita = 5.0, 15
    q_risc = sup * qr
    q_raff = sup * qf
    q_acs = nser * qacs
    q_net = q_risc * (1 - frec)
    ep_risc = q_net / copr
    ep_raff = q_raff / copf
    er_base = q_raff / copc
    ei_base = sup * eill
    ei_alt = ei_base * fled
    eb_base = sup * ebar
    eb_alt = eb_base * fbar
    eb = er_base + ei_base + eb_base
    ea = ep_risc + ep_raff + ei_alt + eb_alt
    gasb = (q_risc + q_acs) / etac
    gasa = q_acs / etac
    cb = eb / 1000.0 * pel + gasb / 1000.0 * pg + omb
    ca = ea / 1000.0 * pel + gasa / 1000.0 * pg + oma
    risp = cb - ca
    co2b = (eb * 0.35 + gasb * 0.20) / 1000.0
    co2a = (ea * 0.35 + gasa * 0.20) / 1000.0
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    be = (ea / 1000.0 * pel + oma - eb / 1000.0 * pel - omb) * 1000.0 / (gasb - gasa)
    bc = mh816_demo_calcoli()
    assert bc["q_risc_kwh_th_anno"] == pytest.approx(q_risc)
    assert bc["q_raff_kwh_th_anno"] == pytest.approx(q_raff)
    assert bc["q_acs_kwh_th_anno"] == pytest.approx(q_acs)
    assert bc["q_risc_net_kwh_th_anno"] == pytest.approx(q_net)
    assert bc["e_pdc_risc_kwh_e_anno"] == pytest.approx(ep_risc)
    assert bc["e_pdc_raff_kwh_e_anno"] == pytest.approx(ep_raff)
    assert bc["e_raff_base_kwh_e_anno"] == pytest.approx(er_base)
    assert bc["e_ill_base_kwh_e_anno"] == pytest.approx(ei_base)
    assert bc["e_ill_alt_kwh_e_anno"] == pytest.approx(ei_alt)
    assert bc["e_bar_base_kwh_e_anno"] == pytest.approx(eb_base)
    assert bc["e_bar_alt_kwh_e_anno"] == pytest.approx(eb_alt)
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
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(be)


def test_demo_verdetto_coerente_con_risparmio_e_van():
    bc = mh816_demo_calcoli()
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] > 0.0
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["tir"] is not None and bc["tir"] > bc["wacc_pct"]
    assert bc["payback"] == 9


# ---------------------------------------------------------------- varianti
def test_variante_senza_recupero_non_convinte():
    # Recupero zero: la pompa di calore in
    # riscaldamento assorbe 30.000 kWh_e/anno,
    # il caso diventa NON_CONVIENTE.
    bc = _variante(f_rec=0)
    assert bc["q_risc_net_kwh_th_anno"] == pytest.approx(96000.0)
    assert bc["e_pdc_risc_kwh_e_anno"] == pytest.approx(30000.0)
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(83600.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(36064.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(7094.095238095237)
    assert bc["van"] == pytest.approx(-11365.717338286122)
    assert bc["tir"] == pytest.approx(2.949341097694113)
    assert bc["payback"] == 12
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(33.49285714285717)
    assert bc["co2_evitata_t_anno"] == pytest.approx(24.87333333333333)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_senza_led_non_convinte():
    # Fattore LED 1 = niente risparmio dai LED:
    # il caso diventa NON_CONVIENTE.
    bc = _variante(f_led=1)
    assert bc["e_ill_alt_kwh_e_anno"] == pytest.approx(48000.0)
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(99500.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(39880.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(3278.0952380952367)
    assert bc["van"] == pytest.approx(-50974.49241198326)
    assert bc["tir"] == pytest.approx(-6.172911115372987)
    assert bc["payback"] is None
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(69.26785714285717)
    assert bc["co2_evitata_t_anno"] == pytest.approx(19.30833333333333)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_capex_marginale_e_non_convinte():
    bc = _variante(capex=100000)
    assert bc["risparmio_eur_anno"] == pytest.approx(9614.095238095237)
    assert bc["van"] == pytest.approx(-208.9790820710332)
    assert bc["tir"] == pytest.approx(4.969066825594321)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"
    bc2 = _variante(capex=150000)
    assert bc2["van"] == pytest.approx(-50208.97908207103)
    assert bc2["tir"] == pytest.approx(-0.487949594394368)
    assert bc2["payback"] is None
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_om_alt_20000_breakeven_valido():
    # O&M alternativo 20.000: risparmio positivo
    # ma VAN negativa oltre la tolleranza, quindi
    # NON_CONVIENTE a prezzo gas 100; il
    # breakeven 66,12 EUR/MWh resta una soglia
    # minima valida (verifica di pareggio nel
    # test dedicato sopra).
    bc = _variante(om_alt=20000)
    assert bc["c_alt_eur_anno"] == pytest.approx(39544.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(3614.0952380952367)
    assert bc["van"] == pytest.approx(-47486.927311154584)
    assert bc["tir"] == pytest.approx(-5.158613388230891)
    assert bc["payback"] is None
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(66.11785714285718)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_om_alt_30000_non_calcolabile():
    # O&M alt 30.000: risparmio negativo negli
    # helper (calcolabile, non solleva), verdetto
    # NON_CALCOLABILE; stessa guard della UI.
    # Il breakeven qui ESISTE (159,87 EUR/MWh):
    # a quel prezzo il risparmio sarebbe zero,
    # ma a prezzo gas 100 il caso e' gia'
    # NON_CALCOLABILE per risparmio negativo.
    bc = _variante(om_alt=30000)
    assert bc["valid"] is True
    assert bc["c_alt_eur_anno"] == pytest.approx(49544.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-6385.904761904763)
    assert bc["van"] == pytest.approx(-151283.5076929605)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"]
    assert bc["payback"] is None
    assert bc["tir"] is None
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(159.8678571428572)


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(59211.42857142855)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(-10762.504987490662)
    assert bc2["payback"] == 9
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_prezzo_el_alto_resta_convinte():
    # Elettricita' a 400 EUR/MWh: il risparmio
    # cresce perche' l'alternativa consuma meno
    # elettricita' della base; il breakeven
    # diventa None (numeratore negativo:
    # l'alternativa vince anche a gas zero).
    bc = _variante(p_el=400)
    assert bc["c_base_eur_anno"] == pytest.approx(58152.38095238095)
    assert bc["c_alt_eur_anno"] == pytest.approx(45240.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(12912.380952380947)
    assert bc["van"] == pytest.approx(49026.09874443084)
    assert bc["tir"] == pytest.approx(12.644609662327804)
    assert bc["payback"] == 7
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_serate_zero_gas_alt_zero():
    # Serate zero: ACS zero e gas alternativo
    # zero, ma il risparmio demo non cambia
    # perche' gas base e gas alt calano insieme
    # di 20.000 kWh/anno (2.000 EUR/anno in
    # entrambi i costi): il caso resta
    # calcolabile in entrambi, CONVIENTE.
    bc = _variante(n_serate=0)
    assert bc["q_acs_kwh_th_anno"] == 0.0
    assert bc["gas_alt_kwh_anno"] == 0.0
    assert bc["gas_base_kwh_anno"] == pytest.approx(106666.66666666666)
    assert bc["risparmio_eur_anno"] == pytest.approx(9614.095238095237)
    assert bc["verdetto"] == "CONVIENTE"


def test_monotonia_prezzo_gas_crescente():
    base = mh816_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas=101)["risparmio_eur_anno"]
    basso = _variante(p_gas=99)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(106.66666666666666, abs=1e-2)
    assert base - basso == pytest.approx(106.66666666666666, abs=1e-2)


def test_monotonia_f_rec_crescente_risparmio_cresce():
    assert _variante(f_rec=0.50)["risparmio_eur_anno"] > \
        mh816_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(f_rec=0.0)["risparmio_eur_anno"] < \
        mh816_demo_calcoli()["risparmio_eur_anno"]


def test_demo_deterministica_due_chiamate():
    a = mh816_demo_calcoli()
    b = mh816_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh816_demo().keys()) == {
        "superficie_m2", "q_risc_kwh_th_m2", "q_raff_kwh_th_m2",
        "f_rec", "cop_risc", "cop_raff_alt", "cop_chiller",
        "e_ill_kwh_e_m2", "f_led", "e_bar_kwh_e_m2", "f_bar",
        "q_acs_serata_kwh_th", "n_serate", "eta_cald",
        "p_el", "p_gas", "om_base", "om_alt",
        "capex", "wacc_pct", "vita_anni",
        "tolleranza_pct"}


# ---------------------------------------------------------------- degenere
def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"superficie_m2": 0},
               {"superficie_m2": -10},
               {"q_risc_kwh_th_m2": -0.1},
               {"q_raff_kwh_th_m2": -0.1},
               {"f_rec": -0.1}, {"f_rec": 1.01},
               {"cop_risc": 0}, {"cop_risc": -1},
               {"cop_raff_alt": 0}, {"cop_chiller": 0},
               {"e_ill_kwh_e_m2": -0.1},
               {"f_led": -0.1}, {"f_led": 1.01},
               {"e_bar_kwh_e_m2": -0.1},
               {"f_bar": -0.1}, {"f_bar": 1.01},
               {"q_acs_serata_kwh_th": -0.1},
               {"n_serate": -1},
               {"eta_cald": 0}, {"eta_cald": 1.01},
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
        assert mh816_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"superficie_m2": "800"},
               {"superficie_m2": float("nan")},
               {"p_gas": float("inf")},
               {"capex": True},
               {"f_rec": "0.35"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh816_valida(**d)["valido"] is False


def test_zeri_ammessi_non_sollevano_e_nessuna_divergenza():
    # Zeri ammessi in entrambi (helper e UI):
    # specifici, recupero 0 e 1, fattore LED 0
    # e 1, fattore frigo bar 0 e 1, ACS per
    # serata, serate, O&M, WACC, tolleranza.
    # Qui si verifica che non sollevano e
    # restano calcolabili.
    for kw in ({"q_risc_kwh_th_m2": 0},
               {"q_raff_kwh_th_m2": 0},
               {"f_rec": 0},
               {"f_rec": 1},
               {"e_ill_kwh_e_m2": 0},
               {"f_led": 0},
               {"f_led": 1},
               {"e_bar_kwh_e_m2": 0},
               {"f_bar": 0},
               {"f_bar": 1},
               {"q_acs_serata_kwh_th": 0},
               {"n_serate": 0},
               {"om_base": 0},
               {"om_alt": 0},
               {"wacc_pct": 0},
               {"tolleranza_pct": 0}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["verdetto"] in ("CONVIENTE", "MARGINALE",
                                  "NON_CONVIENTE", "NON_CALCOLABILE")


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    bc = _variante(om_alt=30000)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] <= 0.0
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"]


def test_pareggio_esatto_tolleranza_float():
    # A pareggio esatto (prezzo gas = breakeven
    # della variante OM_alt 20.000) il
    # risparmio e' zero (circa 0.0, quindi
    # guard NON_CALCOLABILE): in nessun caso
    # CONVIENTE.
    be = _variante(om_alt=20000)["breakeven_gas_eur_mwh"]
    bc = _variante(om_alt=20000, p_gas=be)
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["verdetto"] != "CONVIENTE"
    bc2 = _variante(om_alt=20000, p_gas=be + 1)
    assert bc2["risparmio_eur_anno"] == pytest.approx(106.66666666666666, abs=1e-2)
    # Risparmio positivo ma piccolo: VAN negativa oltre
    # la tolleranza, quindi NON_CONVIENTE (non CONVIENTE).
    assert bc2["verdetto"] == "NON_CONVIENTE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh816_demo_calcoli()
    testo = mh816_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_gas_eur_mwh" in testo
    assert "co2_evitata_t_anno" in testo
    assert "q_risc_kwh_th_anno" in testo
    assert "e_pdc_risc_kwh_e_anno" in testo
    assert "e_ill_alt_kwh_e_anno" in testo
    assert "e_bar_alt_kwh_e_anno" in testo
    assert "gas_alt_kwh_anno" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh816_demo_calcoli()
    testo = mh816_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"e_pdc_risc_kwh_e_anno;{bc['e_pdc_risc_kwh_e_anno']}" in testo
    assert f"gas_base_kwh_anno;{bc['gas_base_kwh_anno']}" in testo
    assert f"q_risc_kwh_th_anno;{bc['q_risc_kwh_th_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh816_demo_calcoli()
    testo = mh816_csv(bc, _demo_kwargs())
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
    return ["mh" + "81" + "5", "st" + "81" + "5",
            "tab" + "81" + "5", "w" + "81" + "6"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w817_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w817_ui.py"))
    ast.parse(src)
    assert src.startswith("# W817")
    assert "with tab816:" in src


def test_ui_apre_scheda_attesa_una_volta():
    """Il frammento UI apre la scheda attesa, una sola volta."""
    src = _leggi("w817_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert m.group(1) == "816"
    assert src.count("with tab816:") == 1


def test_ui_titolo_atteso():
    src = _leggi("w817_ui.py")
    titolo = ("Discoteca / locale notturno: pompa di calore + "
              "recupero calore ventilazione + LED battono "
              "caldaia a gas + chiller + illuminazione "
              "tradizionale?")
    assert src.count(titolo) == 2


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w817_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w817_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st816_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) == 32
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w817_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 4
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_ui_guard_degenere_identica_helper():
    """La guard UI della scheda dichiara NON_CALCOLABILE
    per gli stessi casi degeneri degli helper:
    superficie <= 0, COP <= 0, rendimento caldaia
    <= 0 o sopra 1, prezzi <= 0, CAPEX <= 0,
    vita <= 0 (nessuna divergenza helper-vs-UI)."""
    src = _leggi("w817_ui.py")
    assert "float(_s816) <= 0.0" in src
    assert "float(_copr816) <= 0.0" in src
    assert "float(_copf816) <= 0.0" in src
    assert "float(_copch816) <= 0.0" in src
    assert "float(_etac816) <= 0.0" in src
    assert "float(_etac816) > 1.0" in src
    assert "float(_pel816) <= 0.0" in src
    assert "float(_pg816) <= 0.0" in src
    assert "float(_cx816) <= 0.0" in src
    assert "int(_vita816) <= 0" in src
    assert "Verdetto: NON_CALCOLABILE" in src


def test_ui_chiamata_calcola_keyword_uguali_firma():
    """La chiamata UI a calcola usa come keyword
    esattamente i parametri della firma helper."""
    src = textwrap.dedent(_leggi("w817_ui.py"))
    albero = ast.parse(src)
    chiamate = []
    for nodo in ast.walk(albero):
        if isinstance(nodo, ast.Call):
            func = nodo.func
            if isinstance(func, ast.Name) and func.id == "mh816_calcola":
                chiamate.append({kw.arg for kw in nodo.keywords})
    assert len(chiamate) == 1
    attesi = set(inspect.signature(mh816_calcola).parameters.keys())
    assert chiamate[0] == attesi


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w817_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def816[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w817_ui.py")
        usate = set(re.findall(r'_def816\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 22
        assert usate <= set(mh816_demo().keys())
