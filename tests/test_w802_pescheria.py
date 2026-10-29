"""Test nuova scheda "Pescheria: macchina del
ghiaccio in loco + celle efficienti + recupero
calore condensatori su ACS batte ghiaccio
comprato + celle tradizionali + caldaia a gas?"
(titolo completo nel frammento UI).
Contenuto pronto da scrivere in repo come test
della scheda pescheria.

Business case deterministico di una pescheria
guidato dai KG DI PESCE VENDUTI AL GIORNO e
dai GIORNI DI APERTURA ALL'ANNO: il pesce
guida il ghiaccio in scaglie (kg di ghiaccio
per kg di pesce) e il carico frigorifero di
celle e banchi (kWh_c per kg di pesce); i litri
di ACS al giorno guidano il lavaggio di banchi
e attrezzature. Pesce annuo = kg al giorno x
giorni; ghiaccio annuo = pesce annuo x
rapporto ghiaccio/pesce; freddo ghiaccio =
kg ghiaccio x (4,186 x T_acqua + 334) / 3600
kWh_c/anno (acqua da T_acqua a 0 C piu'
latente 334 kJ/kg); elettricita' macchina =
Q_ghiaccio / COP_macchina (solo alternativa:
la baseline compra il ghiaccio); calore
condensatore = Q_ghiaccio + E_macchina (primo
principio); ACS = litri x giorni x 4,186 x
delta_T / 3600; recupero = min(ACS, Q_cond x
f_rec) (saturato all'ACS); ACS netta = max(0,
ACS - recupero); gas baseline = ACS /
eta_caldaia (senza recupero); carico celle =
pesce annuo x kWh_c per kg; elettricita' celle
base e alt = Q_celle / COP (stesso carico, COP
diverso); elettricita' PdC ACS = ACS netta /
COP_pdc_acs; C_base = kg ghiaccio x prezzo
ghiaccio + E_celle_base / 1000 x p_el + G_acs
/ 1000 x p_gas + O&M_base; C_alt =
(E_macchina + E_celle_alt + E_pdc_acs) / 1000
x p_el + O&M_alt; risparmio = C_base - C_alt;
CO2_base = G_acs / 1000 x f_gas + E_celle_base
/ 1000 x f_el; CO2_alt = (E_macchina +
E_celle_alt + E_pdc_acs) / 1000 x f_el;
CO2_evitata = CO2_base - CO2_alt; flussi
[-CAPEX, risparmio x vita]; VAN, TIR, payback
(primo anno con cumulato >= 0); breakeven
ghiaccio = (C_alt - E_celle_base / 1000 x p_el
- G_acs / 1000 x p_gas - O&M_base) /
kg_ghiaccio_anno EUR/kg, None se kg ghiaccio
<= 0 o numeratore < 0, SOGLIA MINIMA quando
esiste.
Verdetto: NON_CALCOLABILE se risparmio <= 0
(guard degenere: UI salta KPI, grafico, tabella
e CSV); altrimenti CONVIENTE se VAN > 0,
MARGINALE se VAN negativa entro tolleranza %
del CAPEX, NON_CONVIENTE se VAN negativa oltre
la tolleranza. Distinzione esplicita: distinto
dal fioraio (superficie negozio per
riscaldamento piu' cella fiori, recupero sul
riscaldamento: qui niente riscaldamento,
recupero sull'ACS di lavaggio, ghiaccio
prodotto in loco), dal parrucchiere (lavaggi
di capelli, ACS, recupero dalle acque reflue),
dal ristorante (coperti, ACS di cucina, celle
frigo di cucina), dalla farmacia (superficie
di vendita piu' frigoriferi farmaceutici,
recupero dai frigoriferi, nessuna macchina del
ghiaccio), dall'albergo (pernottamento, ACS
docce ospiti), dalla palestra (docce utenti,
recupero dalle acque delle docce),
dall'autolavaggio (veicoli lavati, acque di
lavaggio dei veicoli) e dal palaghiaccio
(pista da pattinaggio, freddo di pista verso
spogliatoi): qui driver PESCE + GIORNI + ACS =
kg di pesce al giorno per ghiaccio e freddo,
giorni di apertura per l'anno, litri di ACS
per il lavaggio; niente lavaggi, niente
coperti, niente docce, niente veicoli, niente
frigoriferi farmaceutici, niente pista.

Demo (pescheria): 120 kg di pesce al giorno
per 300 giorni di apertura all'anno (36.000 kg
all'anno), rapporto ghiaccio/pesce 0,50 kg/kg
(18.000 kg di ghiaccio in scaglie all'anno),
acqua di rete a 15 C, COP macchina del
ghiaccio 2,8, f_rec 0,70, carico celle 0,25
kWh_c per kg di pesce, COP celle base 2,2 e
alt 3,0, ACS di lavaggio 300 litri al giorno
con delta_T 40 K, caldaia 0,90, COP PdC ACS
3,2, ghiaccio comprato 0,40 EUR/kg, gas 90,
el 250 EUR/MWh, O&M base 1.200, alt 2.000,
CAPEX 25.000, WACC 5 %, vita 15, f_gas 0,20,
f_el 0,35, tolleranza 10 % del CAPEX. Valori
calcolati eseguendo mh802_demo_calcoli():
pesce annuo 36.000, ghiaccio annuo 18.000,
Q_ghiaccio 1.983,95, E_macchina 708,5535714285714,
Q_cond 2.692,5035714285714, Q_acs 4.186,0,
Q_rec 1.884,7524999999998, Q_acs_net
2.301,2475000000004, G_acs 4.651,111111111111,
Q_celle 9.000, E_celle_base 4.090,9090909090905,
E_celle_alt 3.000, E_pdc_acs 719,1398437500001,
C_base 9.841,327272727272, C_alt
3.106,923353794643, risparmio 6.734,4039189326295,
CO2_base 2,362040404040404, CO2_alt
1,5496926953125, CO2_evitata 0,8123477087279041,
VAN 44.900,80976950394, TIR 26,10727347297239 %,
payback 4, breakeven ghiaccio
0,025866448948187223 EUR/kg (soglia minima),
verdetto CONVIENTE.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w803_helpers import (
    demo_calcoli,
    mh802_breakeven_ghiaccio,
    mh802_c_alt,
    mh802_c_base,
    mh802_calcola,
    mh802_co2_alt,
    mh802_co2_base,
    mh802_co2_evitata,
    mh802_cop,
    mh802_csv,
    mh802_demo,
    mh802_demo_calcoli,
    mh802_e_celle,
    mh802_e_macchina,
    mh802_e_pdc_acs,
    mh802_eta,
    mh802_flussi,
    mh802_frazione,
    mh802_gas_acs,
    mh802_int_pos,
    mh802_kg_ghiaccio_anno,
    mh802_kg_pesce_anno,
    mh802_num,
    mh802_nneg,
    mh802_payback,
    mh802_pct_tolleranza,
    mh802_pct_wacc,
    mh802_pos,
    mh802_q_acs,
    mh802_q_acs_net,
    mh802_q_celle,
    mh802_q_cond,
    mh802_q_ghiaccio,
    mh802_q_rec,
    mh802_risparmio,
    mh802_tir,
    mh802_valida,
    mh802_van,
    mh802_verdetto,
)

_DEMO = {
    "kg_pesce_anno": 36000.0,
    "kg_ghiaccio_anno": 18000.0,
    "q_ghiaccio_kwh_anno": 1983.95,
    "e_macchina_kwh_anno": 708.5535714285714,
    "q_cond_kwh_anno": 2692.5035714285714,
    "q_acs_kwh_anno": 4186.0,
    "q_rec_kwh_anno": 1884.7524999999998,
    "q_acs_net_kwh_anno": 2301.2475000000004,
    "gas_acs_kwh_anno": 4651.111111111111,
    "q_celle_kwh_anno": 9000.0,
    "e_celle_base_kwh_anno": 4090.9090909090905,
    "e_celle_alt_kwh_anno": 3000.0,
    "e_pdc_acs_kwh_anno": 719.1398437500001,
    "c_base_eur_anno": 9841.327272727272,
    "c_alt_eur_anno": 3106.923353794643,
    "risparmio_eur_anno": 6734.4039189326295,
    "co2_base_t_anno": 2.362040404040404,
    "co2_alt_t_anno": 1.5496926953125,
    "co2_evitata_t_anno": 0.8123477087279041,
    "van": 44900.80976950394,
    "tir": 26.10727347297239,
}


def _demo_kwargs():
    return dict(mh802_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh802_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh802_num(3, "x") == 3.0
    assert mh802_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh802_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh802_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh802_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh802_pos(0, "x")
    with pytest.raises(ValueError):
        mh802_pos(-1, "x")
    assert mh802_pos(0.5, "x") == 0.5


def test_cop_maggiore_di_uno():
    assert mh802_cop(3.2, "x") == 3.2
    assert mh802_cop(1.01, "x") == 1.01
    with pytest.raises(ValueError):
        mh802_cop(1.0, "x")
    with pytest.raises(ValueError):
        mh802_cop(0.5, "x")
    with pytest.raises(ValueError):
        mh802_cop(0, "x")


def test_frazione_limiti():
    assert mh802_frazione(0, "x") == 0.0
    assert mh802_frazione(1, "x") == 1.0
    assert mh802_frazione(0.70, "x") == 0.70
    with pytest.raises(ValueError):
        mh802_frazione(-0.01, "x")
    with pytest.raises(ValueError):
        mh802_frazione(1.01, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh802_int_pos(5.0, "x") == 5
    assert mh802_int_pos(300.0, "x") == 300
    with pytest.raises(ValueError):
        mh802_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh802_int_pos(0, "x")


def test_eta_limiti():
    assert mh802_eta(1.0, "x") == 1.0
    assert mh802_eta(0.9, "x") == 0.9
    with pytest.raises(ValueError):
        mh802_eta(0, "x")
    with pytest.raises(ValueError):
        mh802_eta(1.01, "x")


def test_pct_wacc_limiti():
    assert mh802_pct_wacc(0, "x") == 0.0
    assert mh802_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh802_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh802_pct_tolleranza(0, "x") == 0.0
    assert mh802_pct_tolleranza(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh802_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh802_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_kg_pesce_e_ghiaccio_anno():
    assert mh802_kg_pesce_anno(120, 300) == 36000.0
    assert mh802_kg_pesce_anno(0, 300) == 0.0
    assert mh802_kg_pesce_anno(60, 300) == 18000.0
    assert mh802_kg_ghiaccio_anno(36000, 0.50) == 18000.0
    assert mh802_kg_ghiaccio_anno(36000, 0) == 0.0
    assert mh802_kg_ghiaccio_anno(18000, 0.50) == 9000.0
    with pytest.raises(ValueError):
        mh802_kg_pesce_anno(-1, 300)
    with pytest.raises(ValueError):
        mh802_kg_pesce_anno(120, 0)
    with pytest.raises(ValueError):
        mh802_kg_pesce_anno(120, 2.5)
    with pytest.raises(ValueError):
        mh802_kg_ghiaccio_anno(36000, -0.1)


def test_q_ghiaccio_formula_latente_domina():
    assert mh802_q_ghiaccio(18000, 15) == pytest.approx(1983.95)
    assert mh802_q_ghiaccio(0, 15) == 0.0
    assert mh802_q_ghiaccio(18000, 0) == pytest.approx(1670.0)
    assert mh802_q_ghiaccio(18000, 25) == pytest.approx(2193.25)
    assert mh802_q_ghiaccio(9000, 15) == pytest.approx(991.975)
    with pytest.raises(ValueError):
        mh802_q_ghiaccio(-1, 15)
    with pytest.raises(ValueError):
        mh802_q_ghiaccio(18000, -1)


def test_e_macchina_e_q_cond():
    assert mh802_e_macchina(1983.95, 2.8) == pytest.approx(708.5535714285714)
    assert mh802_e_macchina(0, 2.8) == 0.0
    assert mh802_q_cond(1983.95, 708.5535714285714) == pytest.approx(2692.5035714285714)
    assert mh802_q_cond(0, 0) == 0.0
    with pytest.raises(ValueError):
        mh802_e_macchina(1983.95, 1.0)
    with pytest.raises(ValueError):
        mh802_q_cond(-1, 708.55)
    with pytest.raises(ValueError):
        mh802_q_cond(1983.95, -1)


def test_q_acs_formula():
    assert mh802_q_acs(300, 300, 40) == pytest.approx(4186.0)
    assert mh802_q_acs(0, 300, 40) == 0.0
    assert mh802_q_acs(50, 300, 40) == pytest.approx(697.6666666666666)
    assert mh802_q_acs(300, 300, 20) == pytest.approx(2093.0)
    with pytest.raises(ValueError):
        mh802_q_acs(-1, 300, 40)
    with pytest.raises(ValueError):
        mh802_q_acs(300, 0, 40)
    with pytest.raises(ValueError):
        mh802_q_acs(300, 300, 0)
    with pytest.raises(ValueError):
        mh802_q_acs(300, 2.5, 40)


def test_q_rec_saturazione_e_acs_netta():
    assert mh802_q_rec(2692.5035714285714, 0.70, 4186.0) == pytest.approx(1884.7525)
    assert mh802_q_rec(2692.5035714285714, 0, 4186.0) == 0.0
    assert mh802_q_rec(2692.5035714285714, 1.0, 4186.0) == pytest.approx(2692.5035714285714)
    assert mh802_q_rec(2692.5035714285714, 0.70, 697.6666666666666) == 697.6666666666666
    assert mh802_q_rec(2692.5035714285714, 1.0, 697.6666666666666) == 697.6666666666666
    with pytest.raises(ValueError):
        mh802_q_rec(2692.50, 1.01, 4186.0)
    with pytest.raises(ValueError):
        mh802_q_rec(2692.50, -0.1, 4186.0)
    assert mh802_q_acs_net(4186.0, 1884.7525) == pytest.approx(2301.2475)
    assert mh802_q_acs_net(697.6666666666666, 697.6666666666666) == 0.0
    assert mh802_q_acs_net(4186.0, 0.0) == 4186.0
    with pytest.raises(ValueError):
        mh802_q_acs_net(-1, 1884.75)
    with pytest.raises(ValueError):
        mh802_q_acs_net(4186.0, -1)


def test_gas_acs_e_celle_e_pdc_acs():
    assert mh802_gas_acs(4186.0, 0.9) == pytest.approx(4651.111111111111)
    assert mh802_gas_acs(0, 0.9) == 0.0
    assert mh802_gas_acs(4186.0, 1.0) == pytest.approx(4186.0)
    assert mh802_q_celle(36000, 0.25) == pytest.approx(9000.0)
    assert mh802_q_celle(0, 0.25) == 0.0
    assert mh802_q_celle(36000, 0) == 0.0
    assert mh802_e_celle(9000.0, 2.2) == pytest.approx(4090.9090909090905)
    assert mh802_e_celle(9000.0, 3.0) == pytest.approx(3000.0)
    assert mh802_e_celle(0, 2.2) == 0.0
    assert mh802_e_pdc_acs(2301.2475, 3.2) == pytest.approx(719.1398437500001)
    assert mh802_e_pdc_acs(0, 3.2) == 0.0
    with pytest.raises(ValueError):
        mh802_gas_acs(4186.0, 0)
    with pytest.raises(ValueError):
        mh802_gas_acs(4186.0, 1.01)
    with pytest.raises(ValueError):
        mh802_e_celle(9000.0, 1.0)
    with pytest.raises(ValueError):
        mh802_e_pdc_acs(2301.2475, 1.0)


def test_c_base_c_alt_scomposizione():
    assert mh802_c_base(18000, 0.40, 4090.9090909090905, 250,
                        4651.111111111111, 90,
                        1200) == pytest.approx(9841.327272727272)
    assert mh802_c_base(18000, 0, 4090.9090909090905, 250,
                        4651.111111111111, 90,
                        1200) == pytest.approx(2641.327272727272)
    assert mh802_c_alt(708.5535714285714, 3000.0,
                       719.1398437500001, 250,
                       2000) == pytest.approx(3106.923353794643)
    assert mh802_c_alt(0, 3000.0, 0, 250,
                       2000) == pytest.approx(2750.0)
    with pytest.raises(ValueError):
        mh802_c_base(18000, -0.1, 4090.91, 250,
                     4651.11, 90, 1200)
    with pytest.raises(ValueError):
        mh802_c_alt(708.55, 3000.0, 719.14, 250, -1)


def test_risparmio_segno():
    assert mh802_risparmio(9841.327272727272, 3106.923353794643) == pytest.approx(6734.4039189326295)
    assert mh802_risparmio(3106.92, 3106.92) == 0.0


def test_co2_base_alt_evitata():
    assert mh802_co2_base(4651.111111111111, 0.20, 4090.9090909090905,
                          0.35) == pytest.approx(2.362040404040404)
    assert mh802_co2_alt(708.5535714285714, 3000.0,
                         719.1398437500001,
                         0.35) == pytest.approx(1.5496926953125)
    assert mh802_co2_evitata(4651.111111111111, 0.20,
                             4090.9090909090905,
                             708.5535714285714, 3000.0,
                             719.1398437500001,
                             0.35) == pytest.approx(0.8123477087279041)
    assert mh802_co2_base(0, 0.20, 0, 0.35) == pytest.approx(0.0)
    assert mh802_co2_alt(0, 0, 0, 0.35) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh802_co2_base(4651.11, -0.10, 4090.91, 0.35)
    with pytest.raises(ValueError):
        mh802_co2_alt(708.55, 3000.0, 719.14, -0.10)


def test_breakeven_demo_e_varianti():
    assert mh802_breakeven_ghiaccio(3106.923353794643, 4090.9090909090905,
                                    250, 4651.111111111111, 90,
                                    1200,
                                    18000) == \
        pytest.approx(0.025866448948187223)
    assert mh802_breakeven_ghiaccio(3106.92, 4090.91,
                                    250, 4651.11, 90,
                                    1200, 0) is None
    assert mh802_breakeven_ghiaccio(2006.92, 4090.9090909090905,
                                    250, 4651.111111111111, 90,
                                    1200, 18000) is None
    with pytest.raises(ValueError):
        mh802_breakeven_ghiaccio(3106.92, 4090.91,
                                 250, 4651.11, 90,
                                 1200, -1)


def test_breakeven_verifica_pareggio():
    be = mh802_demo_calcoli()["breakeven_ghiaccio_eur_kg"]
    assert be == pytest.approx(0.025866448948187223)
    bc = _variante(p_ghiaccio_eur_kg=be)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    demo = mh802_demo_calcoli()
    assert demo["breakeven_ghiaccio_eur_kg"] is not None
    assert (demo["c_alt_eur_anno"]
            - demo["e_celle_base_kwh_anno"]
            / 1000.0 * demo["p_el_eur_mwh"]
            - demo["gas_acs_kwh_anno"]
            / 1000.0 * demo["p_gas_eur_mwh"]
            - demo["om_base_eur_anno"]) > 0.0


def test_breakeven_soglia_minima():
    bc_alto = _variante(p_ghiaccio_eur_kg=0.035866448948187223)
    bc_basso = _variante(p_ghiaccio_eur_kg=0.015866448948187223)
    assert bc_alto["c_alt_eur_anno"] < bc_alto["c_base_eur_anno"]
    assert bc_basso["c_alt_eur_anno"] > bc_basso["c_base_eur_anno"]
    assert bc_alto["verdetto"] == "NON_CONVIENTE"
    assert bc_basso["verdetto"] == "NON_CALCOLABILE"


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh802_flussi(25000, 6734.4039189326295, 15)
    assert len(fl) == 16
    assert fl[0] == -25000
    assert all(f == 6734.4039189326295 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh802_demo_calcoli()
    assert bc["van"] == pytest.approx(44900.80976950394)
    assert mh802_van([-25000] + [6734.4039189326295] * 15,
                     0) == pytest.approx(76016.05878398944)
    assert mh802_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh802_demo_calcoli()
    assert bc["tir"] == pytest.approx(26.10727347297239)
    assert mh802_tir([-25000] + [6734.4039189326295] * 15) == \
        pytest.approx(0.2610727347297239)
    tir = mh802_tir([-25000] + [6734.4039189326295] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-25000] + [6734.4039189326295] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh802_payback([-25000] + [6734.4039189326295] * 15) == 4
    assert mh802_payback([-25000] + [-1000.0] * 15) is None
    assert mh802_payback([0] + [6734.4039189326295] * 15) == 0
    assert mh802_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh802_verdetto(6734.4039189326295, 44900.80976950394, 25000,
                          10.0) == "CONVIENTE"
    assert mh802_verdetto(6734.4039189326295, 0.0, 25000, 10.0) == "MARGINALE"
    assert mh802_verdetto(6734.4039189326295, -2500.0, 25000, 10.0) == "MARGINALE"
    assert mh802_verdetto(6734.4039189326295, -2500.01, 25000, 10.0) == "NON_CONVIENTE"
    assert mh802_verdetto(6734.4039189326295, -11149.34, 25000, 10.0) == "NON_CONVIENTE"
    assert mh802_verdetto(0.0, 44900.80976950394, 25000,
                          10.0) == "NON_CALCOLABILE"
    assert mh802_verdetto(-465.60, -29832.73, 25000,
                          10.0) == "NON_CALCOLABILE"
    assert mh802_verdetto(None, 44900.80976950394, 25000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh802_verdetto(float("nan"), 44900.81, 25000, 10.0)
    with pytest.raises(ValueError):
        mh802_verdetto(6734.4039189326295, 44900.81, -1, 10.0)
    with pytest.raises(ValueError):
        mh802_verdetto(6734.4039189326295, 44900.81, 25000, 100.1)


def test_valida_demo_ok():
    v = mh802_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("kg_pesce_giorno", "120"),
                       ("kg_pesce_giorno", float("nan")),
                       ("kg_pesce_giorno", float("inf")),
                       ("kg_pesce_giorno", True),
                       ("p_gas_eur_mwh", None),
                       ("q_celle_per_kg", "0.25")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh802_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("kg_pesce_giorno", -10),
                          ("giorni_anno", 0),
                          ("giorni_anno", 2.5),
                          ("rapporto_ghiaccio_pesce", -0.1),
                          ("t_acqua_c", -1),
                          ("cop_macchina", 1.0),
                          ("cop_macchina", 0.5),
                          ("f_rec", -0.1),
                          ("f_rec", 1.01),
                          ("q_celle_per_kg", -0.1),
                          ("cop_celle_base", 1.0),
                          ("cop_celle_base", 0.5),
                          ("cop_celle_alt", 1.0),
                          ("cop_celle_alt", 0.5),
                          ("litri_acs_giorno", -1),
                          ("delta_t_acs_k", 0),
                          ("delta_t_acs_k", -5),
                          ("eta_caldaia", 0),
                          ("eta_caldaia", 1.01),
                          ("cop_pdc_acs", 1.0),
                          ("cop_pdc_acs", 0.5),
                          ("p_ghiaccio_eur_kg", -0.1),
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
        assert mh802_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"kg_pesce_giorno": 0,
              "rapporto_ghiaccio_pesce": 0,
              "t_acqua_c": 0,
              "f_rec": 0,
              "q_celle_per_kg": 0,
              "litri_acs_giorno": 0,
              "p_ghiaccio_eur_kg": 0,
              "p_gas_eur_mwh": 0,
              "p_el_eur_mwh": 0,
              "om_base_eur_anno": 0, "om_alt_eur_anno": 0,
              "capex_eur": 0, "wacc_pct": 0,
              "f_gas_t_per_mwh": 0, "f_el_t_per_mwh": 0,
              "tolleranza_pct": 0})
    assert mh802_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["f_rec"] = 1.0
    d["kg_pesce_giorno"] = 120
    assert mh802_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh802_demo()
    assert d["kg_pesce_giorno"] == 120
    assert d["giorni_anno"] == 300
    assert d["rapporto_ghiaccio_pesce"] == 0.50
    assert d["t_acqua_c"] == 15
    assert d["cop_macchina"] == 2.8
    assert d["f_rec"] == 0.70
    assert d["q_celle_per_kg"] == 0.25
    assert d["cop_celle_base"] == 2.2
    assert d["cop_celle_alt"] == 3.0
    assert d["litri_acs_giorno"] == 300
    assert d["delta_t_acs_k"] == 40
    assert d["eta_caldaia"] == 0.90
    assert d["cop_pdc_acs"] == 3.2
    assert d["p_ghiaccio_eur_kg"] == 0.40
    assert d["p_gas_eur_mwh"] == 90
    assert d["p_el_eur_mwh"] == 250
    assert d["om_base_eur_anno"] == 1200
    assert d["om_alt_eur_anno"] == 2000
    assert d["capex_eur"] == 25000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["f_gas_t_per_mwh"] == 0.20
    assert d["f_el_t_per_mwh"] == 0.35
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    bc = mh802_demo_calcoli()
    for chiave, atteso in _DEMO.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert got == pytest.approx(atteso, rel=1e-9), chiave
    assert bc["payback"] == 4
    assert bc["breakeven_ghiaccio_eur_kg"] == pytest.approx(0.025866448948187223)
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True
    assert demo_calcoli()["van"] == bc["van"]


def test_demo_calcoli_fisica_economia():
    bc = mh802_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(9841.327272727272)
    assert bc["c_alt_eur_anno"] == pytest.approx(3106.923353794643)
    assert bc["risparmio_eur_anno"] == pytest.approx(6734.4039189326295)
    assert bc["co2_base_t_anno"] == pytest.approx(2.362040404040404)
    assert bc["co2_alt_t_anno"] == pytest.approx(1.5496926953125)
    assert bc["co2_evitata_t_anno"] == pytest.approx(0.8123477087279041)
    assert bc["kg_ghiaccio_anno"] == pytest.approx(18000.0)
    assert bc["q_ghiaccio_kwh_anno"] == pytest.approx(1983.95)
    assert bc["q_cond_kwh_anno"] == pytest.approx(2692.5035714285714)
    assert bc["q_rec_kwh_anno"] == pytest.approx(1884.7524999999998)
    assert bc["q_acs_net_kwh_anno"] == pytest.approx(2301.2475000000004)


def test_demo_flussi_e_cumulato():
    bc = mh802_demo_calcoli()
    assert bc["flussi"][0] == -25000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(6734.4039189326295) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -25000
    assert righe.iloc[3]["Cumulato (EUR)"] == pytest.approx(-4796.788243202113)
    assert righe.iloc[4]["Cumulato (EUR)"] == pytest.approx(1937.6156757305162)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(76016.05878398944)


def test_demo_tabella_righe():
    bc = mh802_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Kg di pesce all'anno"] == pytest.approx(36000.0)
    assert mappa["Kg di ghiaccio all'anno"] == pytest.approx(18000.0)
    assert mappa["Freddo per il ghiaccio (kWh_c/anno)"] == pytest.approx(1983.95)
    assert mappa["Elettricita' macchina del ghiaccio (kWh_e/anno)"] == pytest.approx(708.5535714285714)
    assert mappa["Calore del condensatore (kWh_th/anno)"] == pytest.approx(2692.5035714285714)
    assert mappa["ACS di lavaggio (kWh_th/anno)"] == pytest.approx(4186.0)
    assert mappa["Calore recuperato dal condensatore (kWh_th/anno)"] == pytest.approx(1884.7524999999998)
    assert mappa["ACS netta (kWh_th/anno)"] == pytest.approx(2301.2475000000004)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(4651.111111111111)
    assert mappa["Carico celle e banchi (kWh_c/anno)"] == pytest.approx(9000.0)
    assert mappa["Elettricita' celle base (kWh_e/anno)"] == pytest.approx(4090.9090909090905)
    assert mappa["Elettricita' celle alt (kWh_e/anno)"] == pytest.approx(3000.0)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(9841.327272727272)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(3106.923353794643)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(6734.4039189326295)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(0.8123477087279041)
    assert mappa["Payback (anni)"] == 4
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo ghiaccio (EUR/kg)"] == pytest.approx(0.025866448948187223)


def test_demo_coerenza_interna():
    bc = mh802_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["kg_pesce_anno"] == pytest.approx(
        bc["kg_pesce_giorno"] * bc["giorni_anno"])
    assert bc["kg_ghiaccio_anno"] == pytest.approx(
        bc["kg_pesce_anno"] * bc["rapporto_ghiaccio_pesce"])
    assert bc["q_ghiaccio_kwh_anno"] == pytest.approx(
        bc["kg_ghiaccio_anno"]
        * (4.186 * bc["t_acqua_c"] + 334.0) / 3600.0)
    assert bc["e_macchina_kwh_anno"] == pytest.approx(
        bc["q_ghiaccio_kwh_anno"] / bc["cop_macchina"])
    assert bc["q_cond_kwh_anno"] == pytest.approx(
        bc["q_ghiaccio_kwh_anno"] + bc["e_macchina_kwh_anno"])
    assert bc["q_acs_kwh_anno"] == pytest.approx(
        bc["litri_acs_giorno"] * bc["giorni_anno"]
        * 4.186 * bc["delta_t_acs_k"] / 3600.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(
        min(bc["q_acs_kwh_anno"],
            bc["q_cond_kwh_anno"] * bc["f_rec"]))
    assert bc["q_acs_net_kwh_anno"] == pytest.approx(
        max(0.0, bc["q_acs_kwh_anno"] - bc["q_rec_kwh_anno"]))
    assert bc["gas_acs_kwh_anno"] == pytest.approx(
        bc["q_acs_kwh_anno"] / bc["eta_caldaia"])
    assert bc["q_celle_kwh_anno"] == pytest.approx(
        bc["kg_pesce_anno"] * bc["q_celle_per_kg"])
    assert bc["e_celle_base_kwh_anno"] == pytest.approx(
        bc["q_celle_kwh_anno"] / bc["cop_celle_base"])
    assert bc["e_celle_alt_kwh_anno"] == pytest.approx(
        bc["q_celle_kwh_anno"] / bc["cop_celle_alt"])
    assert bc["e_pdc_acs_kwh_anno"] == pytest.approx(
        bc["q_acs_net_kwh_anno"] / bc["cop_pdc_acs"])
    assert bc["co2_evitata_t_anno"] == pytest.approx(
        bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])
    assert bc["c_base_eur_anno"] == pytest.approx(
        bc["kg_ghiaccio_anno"] * bc["p_ghiaccio_eur_kg"]
        + bc["e_celle_base_kwh_anno"] / 1000.0 * bc["p_el_eur_mwh"]
        + bc["gas_acs_kwh_anno"] / 1000.0 * bc["p_gas_eur_mwh"]
        + bc["om_base_eur_anno"])
    assert bc["c_alt_eur_anno"] == pytest.approx(
        (bc["e_macchina_kwh_anno"] + bc["e_celle_alt_kwh_anno"]
         + bc["e_pdc_acs_kwh_anno"])
        / 1000.0 * bc["p_el_eur_mwh"]
        + bc["om_alt_eur_anno"])


def test_demo_contro_riconteggio_indipendente():
    kgg, gg, rap = 120, 300, 0.50
    tac, copm, frec = 15, 2.8, 0.70
    qc, copb, copa = 0.25, 2.2, 3.0
    lit, dt, eta, copp = 300, 40, 0.90, 3.2
    pghi, pg, pel = 0.40, 90, 250
    omb, oma, cx = 1200, 2000, 25000
    fg, fel, wacc, vita = 0.20, 0.35, 5.0, 15
    kgpa = kgg * gg
    kggh = kgpa * rap
    qghi = kggh * (4.186 * tac + 334.0) / 3600.0
    emac = qghi / copm
    qcond = qghi + emac
    qacs = lit * gg * 4.186 * dt / 3600.0
    qrec = min(qacs, qcond * frec)
    qnet = max(0.0, qacs - qrec)
    gas = qacs / eta
    qcel = kgpa * qc
    ecb = qcel / copb
    eca = qcel / copa
    epdc = qnet / copp
    cb = kggh * pghi + ecb / 1000.0 * pel + gas / 1000.0 * pg + omb
    ca = (emac + eca + epdc) / 1000.0 * pel + oma
    risp = cb - ca
    co2b = gas / 1000.0 * fg + ecb / 1000.0 * fel
    co2a = (emac + eca + epdc) / 1000.0 * fel
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    bc = mh802_demo_calcoli()
    assert bc["kg_pesce_anno"] == pytest.approx(kgpa)
    assert bc["kg_ghiaccio_anno"] == pytest.approx(kggh)
    assert bc["q_ghiaccio_kwh_anno"] == pytest.approx(qghi)
    assert bc["e_macchina_kwh_anno"] == pytest.approx(emac)
    assert bc["q_cond_kwh_anno"] == pytest.approx(qcond)
    assert bc["q_acs_kwh_anno"] == pytest.approx(qacs)
    assert bc["q_rec_kwh_anno"] == pytest.approx(qrec)
    assert bc["q_acs_net_kwh_anno"] == pytest.approx(qnet)
    assert bc["gas_acs_kwh_anno"] == pytest.approx(gas)
    assert bc["q_celle_kwh_anno"] == pytest.approx(qcel)
    assert bc["e_celle_base_kwh_anno"] == pytest.approx(ecb)
    assert bc["e_celle_alt_kwh_anno"] == pytest.approx(eca)
    assert bc["e_pdc_acs_kwh_anno"] == pytest.approx(epdc)
    assert bc["c_base_eur_anno"] == pytest.approx(cb)
    assert bc["c_alt_eur_anno"] == pytest.approx(ca)
    assert bc["risparmio_eur_anno"] == pytest.approx(risp)
    assert bc["co2_base_t_anno"] == pytest.approx(co2b)
    assert bc["co2_alt_t_anno"] == pytest.approx(co2a)
    assert bc["co2_evitata_t_anno"] == pytest.approx(co2)
    assert bc["van"] == pytest.approx(van)
    assert bc["breakeven_ghiaccio_eur_kg"] == pytest.approx(
        (ca - ecb / 1000.0 * pel - gas / 1000.0 * pg - omb) / kggh)


# ---------------------------------------------------------------- varianti
def test_variante_ghiaccio_010_non_conviente():
    bc = _variante(p_ghiaccio_eur_kg=0.10)
    assert bc["risparmio_eur_anno"] == pytest.approx(1334.4039189326295)
    assert bc["van"] == pytest.approx(-11149.34363667125)
    assert bc["tir"] == pytest.approx(-2.6586809960961695)
    assert bc["payback"] is None
    assert bc["breakeven_ghiaccio_eur_kg"] == pytest.approx(0.025866448948187223)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_ghiaccio_zero_non_calcolabile():
    bc = _variante(p_ghiaccio_eur_kg=0)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(-465.59608106737005)
    assert bc["van"] == pytest.approx(-29832.728105396305)
    assert bc["payback"] is None
    assert bc["breakeven_ghiaccio_eur_kg"] == pytest.approx(0.025866448948187223)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_senza_recupero_conveniente():
    bc = _variante(f_rec=0)
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["q_acs_net_kwh_anno"] == 4186.0
    assert bc["risparmio_eur_anno"] == pytest.approx(6587.157629870129)
    assert bc["van"] == pytest.approx(43372.443641644095)
    assert bc["breakeven_ghiaccio_eur_kg"] == pytest.approx(0.03404679834054835)
    assert bc["payback"] == 4
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_recupero_pieno_conveniente():
    bc = _variante(f_rec=1.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(2692.5035714285714)
    assert bc["q_acs_net_kwh_anno"] == pytest.approx(1493.4964285714286)
    assert bc["risparmio_eur_anno"] == pytest.approx(6797.509471387986)
    assert bc["van"] == pytest.approx(45555.823824301)
    assert bc["tir"] == pytest.approx(26.3784936558082)
    assert bc["breakeven_ghiaccio_eur_kg"] == pytest.approx(0.022360584922889604)
    assert bc["payback"] == 4
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_acs_piccola_satura_conveniente():
    bc = _variante(litri_acs_giorno=50)
    assert bc["q_acs_kwh_anno"] == pytest.approx(697.6666666666666)
    assert bc["q_rec_kwh_anno"] == 697.6666666666666
    assert bc["q_acs_net_kwh_anno"] == 0.0
    assert bc["e_pdc_acs_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(6565.355546536795)
    assert bc["van"] == pytest.approx(43146.14547212416)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_pesce_piccolo_e_grande():
    bc = _variante(kg_pesce_giorno=60)
    assert bc["kg_pesce_anno"] == pytest.approx(18000.0)
    assert bc["kg_ghiaccio_anno"] == pytest.approx(9000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(3012.986334466315)
    assert bc["van"] == pytest.approx(6273.767825471558)
    assert bc["breakeven_ghiaccio_eur_kg"] == pytest.approx(0.06522374061485389)
    assert bc["payback"] == 9
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(kg_pesce_giorno=240)
    assert bc2["risparmio_eur_anno"] == pytest.approx(14177.239087865257)
    assert bc2["van"] == pytest.approx(122154.89365756868)
    assert bc2["payback"] == 2
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_capex_marginale_e_non_conviente():
    bc = _variante(capex_eur=40000)
    assert bc["risparmio_eur_anno"] == pytest.approx(6734.4039189326295)
    assert bc["van"] == pytest.approx(29900.809769503943)
    assert bc["payback"] == 6
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(capex_eur=75000)
    assert bc2["van"] == pytest.approx(-5099.190230496071)
    assert bc2["payback"] == 12
    assert bc2["verdetto"] == "MARGINALE"
    bc3 = _variante(capex_eur=80000)
    assert bc3["van"] == pytest.approx(-10099.190230496073)
    assert bc3["payback"] == 12
    assert bc3["verdetto"] == "NON_CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex_eur=0)
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(69900.80976950392, rel=1e-6)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(76016.05878398944)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(27001.28196806116)
    assert bc2["payback"] == 4
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_el_alto_e_om_alt_alto():
    bc = _variante(p_el_eur_mwh=400)
    assert bc["risparmio_eur_anno"] == pytest.approx(6683.886270292208)
    assert bc["van"] == pytest.approx(44376.4538517234)
    assert bc["payback"] == 4
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(om_alt_eur_anno=5000)
    assert bc2["risparmio_eur_anno"] == pytest.approx(3734.4039189326295)
    assert bc2["van"] == pytest.approx(13761.835654962166)
    assert bc2["breakeven_ghiaccio_eur_kg"] == pytest.approx(0.19253311561485387)
    assert bc2["payback"] == 7
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_senza_acs_e_senza_celle():
    bc = _variante(litri_acs_giorno=0)
    assert bc["q_acs_kwh_anno"] == 0.0
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["gas_acs_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(6495.588879870129)
    assert bc["van"] == pytest.approx(42421.99132966044)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(q_celle_per_kg=0)
    assert bc2["q_celle_kwh_anno"] == 0.0
    assert bc2["e_celle_base_kwh_anno"] == 0.0
    assert bc2["e_celle_alt_kwh_anno"] == 0.0
    assert bc2["risparmio_eur_anno"] == pytest.approx(6461.676646205357)
    assert bc2["van"] == pytest.approx(42069.99394090924)
    assert bc2["breakeven_ghiaccio_eur_kg"] == pytest.approx(0.04101796409970239)
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_om_alt_basso_be_none():
    bc = _variante(om_alt_eur_anno=900)
    assert bc["breakeven_ghiaccio_eur_kg"] is None
    assert bc["risparmio_eur_anno"] == pytest.approx(7834.4039189326295)
    assert bc["van"] == pytest.approx(56318.43361150258)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_senza_pesce_be_none_non_calcolabile():
    bc = _variante(kg_pesce_giorno=0)
    assert bc["kg_pesce_anno"] == 0.0
    assert bc["kg_ghiaccio_anno"] == 0.0
    assert bc["breakeven_ghiaccio_eur_kg"] is None
    assert bc["risparmio_eur_anno"] == pytest.approx(-708.4312500000001)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_acqua_calda_e_cop_macchina_basso():
    bc = _variante(t_acqua_c=25)
    assert bc["q_ghiaccio_kwh_anno"] == pytest.approx(2193.25)
    assert bc["risparmio_eur_anno"] == pytest.approx(6731.250403307629)
    assert bc["van"] == pytest.approx(44868.07735569838)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(cop_macchina=2.0)
    assert bc2["risparmio_eur_anno"] == pytest.approx(6679.048171164773)
    assert bc2["van"] == pytest.approx(44326.236037225804)
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_rapporto_zero_be_none():
    bc = _variante(rapporto_ghiaccio_pesce=0)
    assert bc["kg_ghiaccio_anno"] == 0.0
    assert bc["breakeven_ghiaccio_eur_kg"] is None
    assert bc["risparmio_eur_anno"] == pytest.approx(-435.70, abs=1e-2)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_monotonia_prezzo_ghiaccio_crescente():
    base = mh802_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_ghiaccio_eur_kg=0.41)["risparmio_eur_anno"]
    basso = _variante(p_ghiaccio_eur_kg=0.39)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(180.0)
    assert base - basso == pytest.approx(180.0)


def test_monotonia_pesce_crescente():
    assert _variante(kg_pesce_giorno=60)["risparmio_eur_anno"] < \
        mh802_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(kg_pesce_giorno=240)["risparmio_eur_anno"] > \
        mh802_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(kg_pesce_giorno=240)["kg_pesce_anno"] == \
        pytest.approx(72000.0)


def test_demo_deterministica_due_chiamate():
    a = mh802_demo_calcoli()
    b = mh802_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh802_demo().keys()) == {
        "kg_pesce_giorno", "giorni_anno",
        "rapporto_ghiaccio_pesce",
        "t_acqua_c", "cop_macchina", "f_rec",
        "q_celle_per_kg",
        "cop_celle_base", "cop_celle_alt",
        "litri_acs_giorno", "delta_t_acs_k",
        "eta_caldaia", "cop_pdc_acs",
        "p_ghiaccio_eur_kg",
        "p_gas_eur_mwh", "p_el_eur_mwh",
        "om_base_eur_anno", "om_alt_eur_anno",
        "capex_eur", "wacc_pct", "vita_anni",
        "f_gas_t_per_mwh", "f_el_t_per_mwh",
        "tolleranza_pct"}


# ---------------------------------------------------------------- degenere
def test_degenere_cop_uguale_uno_sollevela():
    with pytest.raises(ValueError):
        _variante(cop_macchina=1.0)
    with pytest.raises(ValueError):
        _variante(cop_celle_base=1.0)
    with pytest.raises(ValueError):
        _variante(cop_celle_alt=1.0)
    with pytest.raises(ValueError):
        _variante(cop_pdc_acs=1.0)


def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"kg_pesce_giorno": -10},
               {"giorni_anno": 0},
               {"giorni_anno": 2.5},
               {"rapporto_ghiaccio_pesce": -0.1},
               {"t_acqua_c": -1},
               {"cop_macchina": 1.0}, {"cop_macchina": 0.5},
               {"f_rec": -0.1},
               {"f_rec": 1.01},
               {"q_celle_per_kg": -0.1},
               {"cop_celle_base": 1.0}, {"cop_celle_base": 0.5},
               {"cop_celle_alt": 1.0}, {"cop_celle_alt": 0.5},
               {"litri_acs_giorno": -1},
               {"delta_t_acs_k": 0}, {"delta_t_acs_k": -5},
               {"eta_caldaia": 0}, {"eta_caldaia": 1.01},
               {"cop_pdc_acs": 1.0}, {"cop_pdc_acs": 0.5},
               {"p_ghiaccio_eur_kg": -0.1},
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
        assert mh802_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"kg_pesce_giorno": "120"},
               {"kg_pesce_giorno": float("nan")},
               {"p_gas_eur_mwh": float("inf")},
               {"capex_eur": True},
               {"q_celle_per_kg": "0.25"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh802_valida(**d)["valido"] is False


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    for kw in ({"p_ghiaccio_eur_kg": 0},
               {"kg_pesce_giorno": 0},
               {"rapporto_ghiaccio_pesce": 0}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] <= 0.0
        assert bc["verdetto"] == "NON_CALCOLABILE"
        assert bc["flussi"]


def test_pareggio_esatto_tolleranza_float():
    # A pareggio esatto (prezzo ghiaccio = breakeven)
    # il risparmio e' zero (circa 0.0, quindi guard
    # NON_CALCOLABILE): in nessun caso CONVIENTE.
    be = mh802_demo_calcoli()["breakeven_ghiaccio_eur_kg"]
    bc = _variante(p_ghiaccio_eur_kg=be)
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["verdetto"] != "CONVIENTE"
    bc2 = _variante(p_ghiaccio_eur_kg=be + 0.01)
    assert bc2["risparmio_eur_anno"] == pytest.approx(180.0)
    assert bc2["van"] == pytest.approx(-23131.6615531275)
    assert bc2["verdetto"] == "NON_CONVIENTE"
    bc3 = _variante(p_ghiaccio_eur_kg=be - 0.01)
    assert bc3["risparmio_eur_anno"] == pytest.approx(-180.0)
    assert bc3["verdetto"] == "NON_CALCOLABILE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh802_demo_calcoli()
    testo = mh802_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_ghiaccio_eur_kg" in testo
    assert "co2_evitata_t_anno" in testo
    assert "q_ghiaccio_kwh_anno" in testo
    assert "kg_pesce_giorno" in testo
    assert "e_macchina_kwh_anno" in testo
    assert "e_celle_alt_kwh_anno" in testo
    assert "q_cond_kwh_anno" in testo
    assert "q_rec_kwh_anno" in testo
    assert "q_acs_net_kwh_anno" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh802_demo_calcoli()
    testo = mh802_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"kg_ghiaccio_anno;{bc['kg_ghiaccio_anno']}" in testo
    assert f"gas_acs_kwh_anno;{bc['gas_acs_kwh_anno']}" in testo
    assert f"q_celle_kwh_anno;{bc['q_celle_kwh_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh802_demo_calcoli()
    testo = mh802_csv(bc, _demo_kwargs())
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
    return ["mh" + "80" + "1", "st" + "80" + "1",
            "tab" + "80" + "1", "w" + "80" + "2",
            "mh" + "80" + "0", "tab" + "80" + "0"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w803_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w803_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab802:")


def test_ui_apre_scheda_attesa_una_volta():
    """Il frammento UI apre la scheda attesa, una sola volta."""
    src = _leggi("w803_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert src.count("with tab802:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w803_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w803_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st802_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) >= 28
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w803_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 4
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w803_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def802[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w803_ui.py")
        usate = set(re.findall(r'_def802\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 24
        assert usate <= set(mh802_demo().keys())
