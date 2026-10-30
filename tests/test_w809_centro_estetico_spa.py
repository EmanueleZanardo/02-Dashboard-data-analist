"""Test nuova scheda "Centro estetico / SPA: pompa
di calore + recupero calore acque reflue su ACS
batte caldaia a gas + chiller + sauna elettrica
tradizionale?" (titolo completo nel frammento UI).
Contenuto pronto da scrivere in repo come test
della scheda centro estetico / SPA.

Business case deterministico di un centro
estetico / SPA guidato dalle CABINE DI
TRATTAMENTO, dai M2 DI SUPERFICIE e dai
GIORNI DI APERTURA ALL'ANNO: i m2 guidano
riscaldamento e raffrescamento, i giorni
guidano l'anno, numero x potenza x ore al
giorno x giorni guidano sauna e hammam, litri
al giorno di vasca idromassaggio e di docce
guidano l'ACS, kg al giorno di biancheria
guidano la lavanderia, il recupero dalle acque
reflue riduce l'ACS netta.
Riscaldamento = S x q_risc; raffrescamento =
S x q_raff; sauna base = n_saune x P_sauna x
ore_sauna x giorni e alt = base x fattore
(0,85); hammam base = n_hammam x P_hammam x
ore_hammam x giorni e alt = base x fattore
(0,85); litri vasca anno = litri_vasca_giorno
x giorni; Q_vasca = litri_vasca_anno x 4,186 x
delta_T_vasca / 3600; litri docce anno =
litri_docce_giorno x giorni; Q_docce =
litri_docce_anno x 4,186 x delta_T_docce /
3600; Q_acs = Q_vasca + Q_docce; kg anno =
kg_giorno x giorni; lavanderia base = kg_anno
x kWh_e per kg e alt = base x fattore (0,55);
recupero potenziale = eta_rec x f_disp x
Q_acs; recupero = min(Q_acs, potenziale) (nel
demo NON satura: il potenziale 5.180,175 e'
sotto l'ACS 17.267,25); ACS netta = max(0, ACS
- recupero); gas baseline = (riscaldamento +
ACS) / eta_caldaia (senza recupero); chiller
= raffrescamento / COP_chiller; E_base =
chiller + sauna base + hammam base + lavanderia
base; E_alt = riscaldamento / COP_risc +
raffrescamento / COP_raff + ACS netta / COP_acs
+ sauna alt + hammam alt + lavanderia alt;
C_base = gas_base / 1000 x p_gas + E_base /
1000 x p_el + O&M_base; C_alt = E_alt / 1000
x p_el + O&M_alt (niente gas: l'alternativa
non ha caldaia); risparmio = C_base - C_alt;
CO2_base = gas_base / 1000 x f_gas + E_base /
1000 x f_el; CO2_alt = E_alt / 1000 x f_el;
CO2_evitata = CO2_base - CO2_alt; flussi
[-CAPEX, risparmio x vita]; VAN, TIR, payback
(primo anno con cumulato >= 0); breakeven gas
= (E_alt / 1000 x p_el + O&M_alt - E_base /
1000 x p_el - O&M_base) / (gas_base / 1000)
EUR/MWh, None se denominatore gas <= 0 o
numeratore < 0, SOGLIA MINIMA quando esiste.
Verdetto: NON_CALCOLABILE se input degenere
(cabine <= 0, giorni <= 0, S <= 0, eta
<= 0 o > 1, COP <= 1, delta_T <= 0, eta_rec o
f_disp fuori [0, 1], fattori <= 0 o > 1,
prezzi <= 0, CAPEX <= 0, vita <= 0) o se
risparmio <= 0 (guard degenere: UI salta KPI,
grafico, tabella e CSV); altrimenti CONVIENTE
se VAN > 0, MARGINALE se VAN negativa entro
tolleranza % del CAPEX, NON_CONVIENTE se VAN
negativa oltre la tolleranza. Differenze
UI-vs-helper documentate: cabine = 0 e'
calcolabile negli helper (le cabine NON
scalano l'energia: stessi KPI del demo,
verdetto CONVIENTE) ma bloccato dalla guard
UI (NON_CALCOLABILE): DIVERGENZA di verdetto;
CAPEX = 0 e' CONVIENTE negli helper (VAN
positiva, TIR None, payback 0) ma bloccato
dalla guard UI; prezzi = 0 sono ammessi negli
helper ma bloccati dalla guard UI (p_el = 0
resta CONVIENTE negli helper, p_gas = 0 da'
invece risparmio NEGATIVO negli helper,
-533,17 EUR/anno, verdetto NON_CALCOLABILE:
per gas zero QUI NON c'e' divergenza di
verdetto helper-vs-UI, solo guard prima);
S = 0 e' calcolabile negli helper (risparmio
positivo, VAN positiva, verdetto CONVIENTE,
breakeven None per numeratore negativo) ma
bloccato dalla guard UI.
NOTA CABINE: i litri e i kg al giorno sono
TOTALI DI CENTRO, non per cabina: cambiare
solo le cabine non cambia nessun KPI.
Distinzione esplicita: distinto dalla palestra
(docce post-allenamento e sale fitness: qui
nessuna sala fitness, nessun utente che fa
sport, l'ACS e' quella di vasca idromassaggio
e docce del centro estetico, con sauna,
hammam e lavanderia asciugamani), dal
parrucchiere (lavaggi capelli: qui nessun
lavaggio capelli, nessuna postazione
lavatesta, l'ACS e' quella di vasca e docce,
con sauna, hammam e lavanderia asciugamani),
dalla piscina (vasca natatoria riscaldata in
continuo: qui nessuna vasca natatoria, nessun
nuoto, la vasca e' una vasca idromassaggio
per trattamento, con cabine, sauna, hammam e
lavanderia): qui driver CABINE + M2 + GIORNI
+ SAUNE + HAMMAM + VASCA + DOCCE + LAVANDERIA.

Demo (centro estetico / SPA): 6 cabine per 300
giorni di apertura all'anno, superficie 400 m2
con 90 kWh_th/m2 di riscaldamento (36.000
kWh_th/anno) e 55 kWh_th/m2 di raffrescamento
(22.000 kWh_th/anno), 2 saune da 9 kW per 6 ore
al giorno (32.400 kWh_e/anno base, 27.540 alt
con fattore 0,85), 1 hammam da 6 kW per 6 ore
al giorno (10.800 kWh_e/anno base, 9.180 alt
con fattore 0,85), vasca 1.500 litri al giorno
con delta_T 25 K (450.000 litri all'anno,
13.081,25 kWh_th/anno), docce 400 litri al
giorno con delta_T 30 K (120.000 litri
all'anno, 4.186,00 kWh_th/anno), ACS totale
17.267,25 kWh_th/anno, lavanderia 60 kg al
giorno da 1,2 kWh_e/kg (18.000 kg all'anno,
21.600 kWh_e/anno base, 11.880 alt con fattore
0,55), rendimento di recupero 0,50 e frazione
di disponibilita' 0,60 (potenziale 5.180,175,
NON saturato: ACS netta 12.087,075
kWh_th/anno), caldaia 0,90, chiller COP 3,0,
pompa di calore COP riscaldamento 3,5 /
raffrescamento 4,0 / ACS 3,0, gas 100, el 260
EUR/MWh, O&M base 4.000, alt 5.500, CAPEX
25.000, WACC 5 %, vita 15, f_gas 0,20, f_el
0,35, tolleranza 10 % del CAPEX. Valori
calcolati eseguendo mh809_demo_calcoli():
Q_risc 36.000, Q_raff 22.000, E_sauna_base
32.400, E_sauna_alt 27.540, E_hammam_base
10.800, E_hammam_alt 9.180, litri vasca
450.000, Q_vasca 13.081,25, litri docce
120.000, Q_docce 4.186,00, Q_acs 17.267,25,
kg anno 18.000, E_lav_base 21.600, E_lav_alt
11.880, Q_rec_pot 5.180,175, Q_rec 5.180,175
(NON saturato), Q_acs_net 12.087,075, gas_base
59.185,83333333333, E_chiller 7.333,333333333333,
E_pdc_risc 10.285,714285714286, E_pdc_raff
5.500, E_pdc_acs 4.029,025, E_base
72.133,33333333334, E_alt 68.414,73928571428,
C_base 28.673,25, C_alt 23.287,832214285714,
risparmio 5.385,417785714286, CO2_base
37,08383333333333, CO2_alt 23,94515875,
CO2_evitata 13,13867458333333, VAN
30.898,795008450004, TIR 20,17346840752664 %,
payback 5, breakeven gas 9,008330500582284
EUR/MWh (soglia minima), verdetto CONVIENTE.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w810_helpers import (
    demo_calcoli,
    mh809_breakeven_gas,
    mh809_c_alt,
    mh809_c_base,
    mh809_calcola,
    mh809_co2_alt,
    mh809_co2_base,
    mh809_co2_evitata,
    mh809_cop,
    mh809_csv,
    mh809_demo,
    mh809_demo_calcoli,
    mh809_e_alt,
    mh809_e_base,
    mh809_e_chiller,
    mh809_e_hammam_alt,
    mh809_e_hammam_base,
    mh809_e_lav_alt,
    mh809_e_lav_base,
    mh809_e_pdc,
    mh809_e_sauna_alt,
    mh809_e_sauna_base,
    mh809_eta,
    mh809_fattore_alt,
    mh809_flussi,
    mh809_frazione,
    mh809_gas_base,
    mh809_int_pos,
    mh809_kg_anno,
    mh809_litri_docce_anno,
    mh809_litri_vasca_anno,
    mh809_num,
    mh809_nneg,
    mh809_payback,
    mh809_pct_tolleranza,
    mh809_pos,
    mh809_pct_wacc,
    mh809_q_acqua,
    mh809_q_acs_net,
    mh809_q_raff,
    mh809_q_rec,
    mh809_q_rec_pot,
    mh809_q_risc,
    mh809_risparmio,
    mh809_tir,
    mh809_valida,
    mh809_van,
    mh809_verdetto,
)

_DEMO = {
    "q_risc_kwh_anno": 36000.0,
    "q_raff_kwh_anno": 22000.0,
    "e_sauna_base_kwh_anno": 32400.0,
    "e_sauna_alt_kwh_anno": 27540.0,
    "e_hammam_base_kwh_anno": 10800.0,
    "e_hammam_alt_kwh_anno": 9180.0,
    "litri_vasca_anno": 450000.0,
    "q_vasca_kwh_anno": 13081.25,
    "litri_docce_anno": 120000.0,
    "q_docce_kwh_anno": 4186.0,
    "q_acs_kwh_anno": 17267.25,
    "kg_anno": 18000.0,
    "e_lav_base_kwh_anno": 21600.0,
    "e_lav_alt_kwh_anno": 11880.0,
    "q_rec_pot_kwh_anno": 5180.175,
    "q_rec_kwh_anno": 5180.175,
    "q_acs_net_kwh_anno": 12087.075,
    "gas_base_kwh_anno": 59185.83333333333,
    "e_chiller_kwh_anno": 7333.333333333333,
    "e_pdc_risc_kwh_anno": 10285.714285714286,
    "e_pdc_raff_kwh_anno": 5500.0,
    "e_pdc_acs_kwh_anno": 4029.025,
    "e_base_kwh_anno": 72133.33333333334,
    "e_alt_kwh_anno": 68414.73928571428,
    "c_base_eur_anno": 28673.25,
    "c_alt_eur_anno": 23287.832214285714,
    "risparmio_eur_anno": 5385.417785714286,
    "co2_base_t_anno": 37.08383333333333,
    "co2_alt_t_anno": 23.94515875,
    "co2_evitata_t_anno": 13.13867458333333,
    "van": 30898.795008450004,
    "tir": 20.17346840752664,
    "breakeven_gas_eur_mwh": 9.008330500582284,
}


def _demo_kwargs():
    return dict(mh809_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh809_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh809_num(3, "x") == 3.0
    assert mh809_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh809_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh809_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh809_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh809_pos(0, "x")
    with pytest.raises(ValueError):
        mh809_pos(-1, "x")
    assert mh809_pos(0.5, "x") == 0.5


def test_cop_maggiore_di_uno():
    assert mh809_cop(3.0, "x") == 3.0
    assert mh809_cop(3.5, "x") == 3.5
    with pytest.raises(ValueError):
        mh809_cop(1.0, "x")
    with pytest.raises(ValueError):
        mh809_cop(0.5, "x")
    with pytest.raises(ValueError):
        mh809_cop(0, "x")


def test_frazione_limiti():
    assert mh809_frazione(0, "x") == 0.0
    assert mh809_frazione(1, "x") == 1.0
    assert mh809_frazione(0.50, "x") == 0.50
    assert mh809_frazione(0.60, "x") == 0.60
    with pytest.raises(ValueError):
        mh809_frazione(-0.01, "x")
    with pytest.raises(ValueError):
        mh809_frazione(1.01, "x")


def test_fattore_alt_limiti():
    assert mh809_fattore_alt(0.85, "x") == 0.85
    assert mh809_fattore_alt(1.0, "x") == 1.0
    with pytest.raises(ValueError):
        mh809_fattore_alt(0, "x")
    with pytest.raises(ValueError):
        mh809_fattore_alt(1.01, "x")
    with pytest.raises(ValueError):
        mh809_fattore_alt(-0.1, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh809_int_pos(5.0, "x") == 5
    assert mh809_int_pos(300.0, "x") == 300
    with pytest.raises(ValueError):
        mh809_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh809_int_pos(0, "x")


def test_eta_limiti():
    assert mh809_eta(1.0, "x") == 1.0
    assert mh809_eta(0.90, "x") == 0.90
    with pytest.raises(ValueError):
        mh809_eta(0, "x")
    with pytest.raises(ValueError):
        mh809_eta(1.01, "x")


def test_pct_wacc_limiti():
    assert mh809_pct_wacc(0, "x") == 0.0
    assert mh809_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh809_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh809_pct_tolleranza(0, "x") == 0.0
    assert mh809_pct_tolleranza(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh809_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh809_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_q_risc_raff():
    assert mh809_q_risc(400, 90) == 36000.0
    assert mh809_q_raff(400, 55) == 22000.0
    assert mh809_q_risc(0, 90) == 0.0
    with pytest.raises(ValueError):
        mh809_q_risc(-1, 90)


def test_sauna_hammam():
    assert mh809_e_sauna_base(2, 9, 6, 300) == 32400.0
    assert mh809_e_sauna_base(0, 9, 6, 300) == 0.0
    assert mh809_e_sauna_alt(32400.0, 0.85) == 27540.0
    assert mh809_e_sauna_alt(32400.0, 1.0) == 32400.0
    with pytest.raises(ValueError):
        mh809_e_sauna_alt(32400.0, 0)
    with pytest.raises(ValueError):
        mh809_e_sauna_alt(32400.0, 1.01)
    assert mh809_e_hammam_base(1, 6, 6, 300) == 10800.0
    assert mh809_e_hammam_alt(10800.0, 0.85) == 9180.0
    with pytest.raises(ValueError):
        mh809_e_hammam_base(-1, 6, 6, 300)
    with pytest.raises(ValueError):
        mh809_e_hammam_base(1, 6, 6, 0)


def test_litri_q_acqua_vasca_docce():
    assert mh809_litri_vasca_anno(1500, 300) == 450000.0
    assert mh809_litri_docce_anno(400, 300) == 120000.0
    assert mh809_q_acqua(450000, 25) == pytest.approx(13081.25)
    assert mh809_q_acqua(120000, 30) == pytest.approx(4186.0)
    assert mh809_q_acqua(0, 25) == 0.0
    assert mh809_q_acqua(450000, 12.5) == pytest.approx(6540.625)
    with pytest.raises(ValueError):
        mh809_q_acqua(-1, 25)
    with pytest.raises(ValueError):
        mh809_q_acqua(450000, 0)


def test_lavanderia():
    assert mh809_kg_anno(60, 300) == 18000.0
    assert mh809_e_lav_base(18000, 1.2) == 21600.0
    assert mh809_e_lav_alt(21600.0, 0.55) == pytest.approx(11880.0)
    assert mh809_e_lav_alt(21600.0, 1.0) == 21600.0
    with pytest.raises(ValueError):
        mh809_e_lav_alt(21600.0, 0)


def test_recupero_non_saturato_e_saturazione():
    assert mh809_q_rec_pot(17267.25, 0.50, 0.60) == pytest.approx(5180.175)
    assert mh809_q_rec_pot(17267.25, 0, 0.60) == 0.0
    # Demo: potenziale 5.180,175 sotto l'ACS -> NON satura.
    assert mh809_q_rec(17267.25, 5180.175) == pytest.approx(5180.175)
    # Recupero saturato con eta_rec e f_disp al massimo.
    assert mh809_q_rec(17267.25, 17267.25) == pytest.approx(17267.25)
    assert mh809_q_rec(17267.25, 20000.0) == pytest.approx(17267.25)
    assert mh809_q_rec(17267.25, 0.0) == 0.0
    with pytest.raises(ValueError):
        mh809_q_rec(-1, 5180.175)
    with pytest.raises(ValueError):
        mh809_q_rec(17267.25, -1)
    assert mh809_q_acs_net(17267.25, 5180.175) == pytest.approx(12087.075)
    assert mh809_q_acs_net(17267.25, 17267.25) == 0.0
    assert mh809_q_acs_net(17267.25, 0.0) == pytest.approx(17267.25)
    with pytest.raises(ValueError):
        mh809_q_acs_net(-1, 5180.175)


def test_gas_chiller_pdc_e_totali():
    assert mh809_gas_base(36000.0, 17267.25, 0.90) == pytest.approx(59185.83333333333)
    assert mh809_gas_base(0, 0, 0.90) == 0.0
    assert mh809_e_chiller(22000.0, 3.0) == pytest.approx(7333.333333333333)
    assert mh809_e_pdc(36000.0, 3.5) == pytest.approx(10285.714285714286)
    assert mh809_e_pdc(22000.0, 4.0) == 5500.0
    assert mh809_e_pdc(12087.075, 3.0) == pytest.approx(4029.025)
    assert mh809_e_pdc(0.0, 3.0) == 0.0
    with pytest.raises(ValueError):
        mh809_gas_base(36000.0, 17267.25, 0)
    with pytest.raises(ValueError):
        mh809_gas_base(36000.0, 17267.25, 1.01)
    with pytest.raises(ValueError):
        mh809_e_chiller(22000.0, 1.0)
    with pytest.raises(ValueError):
        mh809_e_pdc(36000.0, 1.0)
    assert mh809_e_base(7333.333333333333, 32400.0, 10800.0,
                        21600.0) == pytest.approx(72133.33333333334)
    assert mh809_e_alt(10285.714285714286, 5500.0, 4029.025,
                       27540.0, 9180.0,
                       11880.0) == pytest.approx(68414.73928571428)


def test_c_base_c_alt_scomposizione():
    assert mh809_c_base(59185.83333333333, 100, 72133.33333333334,
                        260,
                        4000) == pytest.approx(28673.25)
    assert mh809_c_base(59185.83333333333, 0, 72133.33333333334,
                        260,
                        4000) == pytest.approx(22754.666666666668)
    assert mh809_c_alt(68414.73928571428, 260,
                       5500) == pytest.approx(23287.832214285714)
    with pytest.raises(ValueError):
        mh809_c_base(59185.83, 100, 72133.33, 260, -1)
    with pytest.raises(ValueError):
        mh809_c_alt(68414.74, 260, -1)


def test_risparmio_segno():
    assert mh809_risparmio(28673.25, 23287.832214285714) == pytest.approx(5385.417785714286)
    assert mh809_risparmio(23287.83, 23287.83) == 0.0


def test_co2_base_alt_evitata():
    assert mh809_co2_base(59185.83333333333, 0.20, 72133.33333333334,
                          0.35) == pytest.approx(37.08383333333333)
    assert mh809_co2_alt(68414.73928571428,
                         0.35) == pytest.approx(23.94515875)
    assert mh809_co2_evitata(59185.83333333333, 0.20, 72133.33333333334,
                             68414.73928571428,
                             0.35) == pytest.approx(13.13867458333333)
    assert mh809_co2_base(0, 0.20, 0, 0.35) == pytest.approx(0.0)
    assert mh809_co2_alt(0, 0.35) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh809_co2_base(59185.83, -0.10, 72133.33, 0.35)
    with pytest.raises(ValueError):
        mh809_co2_alt(68414.74, -0.10)


def test_breakeven_demo_e_varianti():
    # Demo: 9,01 EUR/MWh (soglia minima, esiste).
    assert mh809_demo_calcoli()["breakeven_gas_eur_mwh"] == pytest.approx(9.008330500582284)
    assert mh809_breakeven_gas(68414.73928571428,
                               260, 5500,
                               72133.33333333334,
                               4000,
                               59185.83333333333) == pytest.approx(9.008330500582284)
    # Variante O&M alternativo 10.000: be 85,04 (soglia minima).
    bc = _variante(om_alt=10000)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(85.04003853882342)
    # Variante senza superficie: be None (numeratore negativo).
    assert _variante(superficie_m2=0)["breakeven_gas_eur_mwh"] is None
    # Variante senza superficie ne' litri: denominatore gas nullo -> None.
    assert _variante(superficie_m2=0, litri_vasca_giorno=0,
                     litri_docce_giorno=0)["breakeven_gas_eur_mwh"] is None
    # Variante numeratore negativo (elettricita' bassa, O&M alt zero): None.
    assert _variante(p_el=50, om_alt=0)["breakeven_gas_eur_mwh"] is None
    # Denominatore gas nullo diretto -> None.
    assert mh809_breakeven_gas(68414.73928571428,
                               260, 5500,
                               72133.33333333334,
                               4000,
                               0) is None
    with pytest.raises(ValueError):
        mh809_breakeven_gas(68414.74,
                            260, 5500,
                            72133.33,
                            4000,
                            -1)


def test_breakeven_verifica_pareggio():
    be = mh809_demo_calcoli()["breakeven_gas_eur_mwh"]
    assert be == pytest.approx(9.008330500582284)
    bc = _variante(p_gas=be)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert mh809_demo_calcoli()["gas_base_kwh_anno"] > 0.0


def test_breakeven_soglia_minima():
    bc_alto = _variante(p_gas=10.008330500582284)
    bc_basso = _variante(p_gas=8.0)
    assert bc_alto["c_alt_eur_anno"] < bc_alto["c_base_eur_anno"]
    assert bc_basso["c_alt_eur_anno"] > bc_basso["c_base_eur_anno"]
    # Sopra il breakeven il risparmio e' positivo ma
    # piccolo (59,19 EUR/anno): la VAN resta negativa
    # oltre la tolleranza, quindi NON_CONVIENTE
    # (il breakeven pareggia i costi, non la finanza).
    assert bc_alto["risparmio_eur_anno"] > 0.0
    assert bc_alto["verdetto"] == "NON_CONVIENTE"
    assert bc_basso["verdetto"] == "NON_CALCOLABILE"


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh809_flussi(25000, 5385.417785714286, 15)
    assert len(fl) == 16
    assert fl[0] == -25000
    assert all(f == 5385.417785714286 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh809_demo_calcoli()
    assert bc["van"] == pytest.approx(30898.795008450004)
    assert mh809_van([-25000] + [5385.417785714286] * 15,
                     0) == pytest.approx(55781.26678571429)
    assert mh809_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh809_demo_calcoli()
    assert bc["tir"] == pytest.approx(20.17346840752664)
    assert mh809_tir([-25000] + [5385.417785714286] * 15) == \
        pytest.approx(0.2017346840752664)
    tir = mh809_tir([-25000] + [5385.417785714286] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-25000] + [5385.417785714286] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh809_payback([-25000] + [5385.417785714286] * 15) == 5
    assert mh809_payback([-25000] + [-1000.0] * 15) is None
    assert mh809_payback([0] + [5385.417785714286] * 15) == 0
    assert mh809_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh809_verdetto(5385.417785714286, 30898.795008450004, 25000,
                          10.0) == "CONVIENTE"
    assert mh809_verdetto(5385.417785714286, -1101.204991549996, 57000,
                          10.0) == "MARGINALE"
    assert mh809_verdetto(5385.417785714286, -5700.0, 57000, 10.0) == "MARGINALE"
    assert mh809_verdetto(5385.417785714286, -5700.01, 57000, 10.0) == "NON_CONVIENTE"
    assert mh809_verdetto(5385.417785714286, 0.0, 25000, 10.0) == "MARGINALE"
    assert mh809_verdetto(0.0, 30898.80, 25000,
                          10.0) == "NON_CALCOLABILE"
    assert mh809_verdetto(-533.1655476190463, -30534.08, 25000,
                          10.0) == "NON_CALCOLABILE"
    assert mh809_verdetto(None, 30898.80, 25000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh809_verdetto(float("nan"), 30898.80, 25000, 10.0)
    with pytest.raises(ValueError):
        mh809_verdetto(5385.417785714286, 30898.80, -1, 10.0)
    with pytest.raises(ValueError):
        mh809_verdetto(5385.417785714286, 30898.80, 25000, 100.1)


def test_valida_demo_ok():
    v = mh809_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("n_cabine", "6"),
                       ("n_cabine", float("nan")),
                       ("n_cabine", float("inf")),
                       ("n_cabine", True),
                       ("p_gas", None),
                       ("q_risc_per_m2", "90")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh809_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("n_cabine", -1),
                          ("superficie_m2", -10),
                          ("q_risc_per_m2", -10),
                          ("q_raff_per_m2", -10),
                          ("giorni_anno", 0),
                          ("giorni_anno", 2.5),
                          ("n_saune", -1),
                          ("p_sauna_kw", -0.5),
                          ("ore_sauna_giorno", -1),
                          ("f_sauna_alt", 0),
                          ("f_sauna_alt", 1.01),
                          ("n_hammam", -1),
                          ("p_hammam_kw", -0.5),
                          ("ore_hammam_giorno", -1),
                          ("f_hammam_alt", 0),
                          ("f_hammam_alt", 1.01),
                          ("litri_vasca_giorno", -1),
                          ("delta_t_vasca", 0),
                          ("delta_t_vasca", -5),
                          ("litri_docce_giorno", -1),
                          ("delta_t_docce", 0),
                          ("delta_t_docce", -5),
                          ("kg_giorno", -1),
                          ("e_lav_per_kg", -0.1),
                          ("f_lav_alt", 0),
                          ("f_lav_alt", 1.01),
                          ("eta_rec", -0.1),
                          ("eta_rec", 1.01),
                          ("f_disp", -0.1),
                          ("f_disp", 1.01),
                          ("eta_caldaia", 0),
                          ("eta_caldaia", 1.01),
                          ("cop_chiller", 1.0),
                          ("cop_chiller", 0.5),
                          ("cop_risc", 1.0),
                          ("cop_raff", 1.0),
                          ("cop_acs", 1.0),
                          ("p_gas", -1),
                          ("p_el", -1),
                          ("om_base", -100),
                          ("om_alt", -100),
                          ("capex", -1),
                          ("wacc_pct", -0.1), ("wacc_pct", 50.1),
                          ("vita_anni", 0), ("vita_anni", 2.5),
                          ("f_gas", -0.10),
                          ("f_el", -0.10),
                          ("tolleranza_pct", -1),
                          ("tolleranza_pct", 100.1)):
        d = _demo_kwargs()
        d[campo] = valore
        assert mh809_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"n_cabine": 0,
              "superficie_m2": 0,
              "q_risc_per_m2": 0,
              "q_raff_per_m2": 0,
              "n_saune": 0,
              "p_sauna_kw": 0,
              "ore_sauna_giorno": 0,
              "n_hammam": 0,
              "p_hammam_kw": 0,
              "ore_hammam_giorno": 0,
              "litri_vasca_giorno": 0,
              "litri_docce_giorno": 0,
              "kg_giorno": 0,
              "e_lav_per_kg": 0,
              "eta_rec": 0,
              "f_disp": 0,
              "p_gas": 0,
              "p_el": 0,
              "om_base": 0, "om_alt": 0,
              "capex": 0, "wacc_pct": 0,
              "f_gas": 0, "f_el": 0,
              "tolleranza_pct": 0})
    assert mh809_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["eta_rec"] = 1
    d["f_disp"] = 1
    d["n_cabine"] = 6
    assert mh809_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh809_demo()
    assert d["n_cabine"] == 6
    assert d["superficie_m2"] == 400
    assert d["giorni_anno"] == 300
    assert d["q_risc_per_m2"] == 90
    assert d["q_raff_per_m2"] == 55
    assert d["n_saune"] == 2
    assert d["p_sauna_kw"] == 9
    assert d["ore_sauna_giorno"] == 6
    assert d["f_sauna_alt"] == 0.85
    assert d["n_hammam"] == 1
    assert d["p_hammam_kw"] == 6
    assert d["ore_hammam_giorno"] == 6
    assert d["f_hammam_alt"] == 0.85
    assert d["litri_vasca_giorno"] == 1500
    assert d["delta_t_vasca"] == 25
    assert d["litri_docce_giorno"] == 400
    assert d["delta_t_docce"] == 30
    assert d["kg_giorno"] == 60
    assert d["e_lav_per_kg"] == 1.2
    assert d["f_lav_alt"] == 0.55
    assert d["eta_rec"] == 0.50
    assert d["f_disp"] == 0.60
    assert d["eta_caldaia"] == 0.90
    assert d["cop_chiller"] == 3.0
    assert d["cop_risc"] == 3.5
    assert d["cop_raff"] == 4.0
    assert d["cop_acs"] == 3.0
    assert d["p_gas"] == 100
    assert d["p_el"] == 260
    assert d["om_base"] == 4000
    assert d["om_alt"] == 5500
    assert d["capex"] == 25000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["f_gas"] == 0.20
    assert d["f_el"] == 0.35
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    bc = mh809_demo_calcoli()
    for chiave, atteso in _DEMO.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert got == pytest.approx(atteso, rel=1e-9), chiave
    assert bc["payback"] == 5
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True
    assert demo_calcoli()["van"] == bc["van"]


def test_demo_calcoli_fisica_economia():
    bc = mh809_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(28673.25)
    assert bc["c_alt_eur_anno"] == pytest.approx(23287.832214285714)
    assert bc["risparmio_eur_anno"] == pytest.approx(5385.417785714286)
    assert bc["co2_base_t_anno"] == pytest.approx(37.08383333333333)
    assert bc["co2_alt_t_anno"] == pytest.approx(23.94515875)
    assert bc["co2_evitata_t_anno"] == pytest.approx(13.13867458333333)
    assert bc["q_risc_kwh_anno"] == pytest.approx(36000.0)
    assert bc["q_raff_kwh_anno"] == pytest.approx(22000.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(5180.175)
    assert bc["q_rec_pot_kwh_anno"] == pytest.approx(5180.175)
    assert bc["q_acs_net_kwh_anno"] == pytest.approx(12087.075)


def test_demo_flussi_e_cumulato():
    bc = mh809_demo_calcoli()
    assert bc["flussi"][0] == -25000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(5385.417785714286) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -25000
    assert righe.iloc[4]["Cumulato (EUR)"] == pytest.approx(-3458.3288571428566)
    assert righe.iloc[5]["Cumulato (EUR)"] == pytest.approx(1927.0889285714293)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(55781.26678571429)


def test_demo_tabella_righe():
    bc = mh809_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Riscaldamento (kWh_th/anno)"] == pytest.approx(36000.0)
    assert mappa["Raffrescamento (kWh_th/anno)"] == pytest.approx(22000.0)
    assert mappa["ACS (kWh_th/anno)"] == pytest.approx(17267.25)
    assert mappa["Elettricita' sauna base (kWh_e/anno)"] == pytest.approx(32400.0)
    assert mappa["Elettricita' sauna alt (kWh_e/anno)"] == pytest.approx(27540.0)
    assert mappa["Elettricita' hammam base (kWh_e/anno)"] == pytest.approx(10800.0)
    assert mappa["Elettricita' hammam alt (kWh_e/anno)"] == pytest.approx(9180.0)
    assert mappa["Calore vasca (kWh_th/anno)"] == pytest.approx(13081.25)
    assert mappa["Calore docce (kWh_th/anno)"] == pytest.approx(4186.0)
    assert mappa["Elettricita' lavanderia base (kWh_e/anno)"] == pytest.approx(21600.0)
    assert mappa["Elettricita' lavanderia alt (kWh_e/anno)"] == pytest.approx(11880.0)
    assert mappa["Recupero potenziale (kWh_th/anno)"] == pytest.approx(5180.175)
    assert mappa["Calore recuperato su ACS (kWh_th/anno)"] == pytest.approx(5180.175)
    assert mappa["ACS netta (kWh_th/anno)"] == pytest.approx(12087.075)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(59185.83333333333)
    assert mappa["Elettricita' totale base (kWh_e/anno)"] == pytest.approx(72133.33333333334)
    assert mappa["Elettricita' totale alternativa (kWh_e/anno)"] == pytest.approx(68414.73928571428)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(28673.25)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(23287.832214285714)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(5385.417785714286)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(13.13867458333333)
    assert mappa["Payback (anni)"] == 5
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] == pytest.approx(9.008330500582284)


def test_demo_coerenza_interna():
    bc = mh809_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["q_risc_kwh_anno"] == pytest.approx(
        bc["superficie_m2"] * bc["q_risc_per_m2"])
    assert bc["q_raff_kwh_anno"] == pytest.approx(
        bc["superficie_m2"] * bc["q_raff_per_m2"])
    assert bc["e_sauna_base_kwh_anno"] == pytest.approx(
        bc["n_saune"] * bc["p_sauna_kw"]
        * bc["ore_sauna_giorno"] * bc["giorni_anno"])
    assert bc["e_sauna_alt_kwh_anno"] == pytest.approx(
        bc["e_sauna_base_kwh_anno"] * bc["f_sauna_alt"])
    assert bc["e_hammam_base_kwh_anno"] == pytest.approx(
        bc["n_hammam"] * bc["p_hammam_kw"]
        * bc["ore_hammam_giorno"] * bc["giorni_anno"])
    assert bc["e_hammam_alt_kwh_anno"] == pytest.approx(
        bc["e_hammam_base_kwh_anno"] * bc["f_hammam_alt"])
    assert bc["litri_vasca_anno"] == pytest.approx(
        bc["litri_vasca_giorno"] * bc["giorni_anno"])
    assert bc["q_vasca_kwh_anno"] == pytest.approx(
        bc["litri_vasca_anno"] * 4.186 * bc["delta_t_vasca"] / 3600.0)
    assert bc["litri_docce_anno"] == pytest.approx(
        bc["litri_docce_giorno"] * bc["giorni_anno"])
    assert bc["q_docce_kwh_anno"] == pytest.approx(
        bc["litri_docce_anno"] * 4.186 * bc["delta_t_docce"] / 3600.0)
    assert bc["q_acs_kwh_anno"] == pytest.approx(
        bc["q_vasca_kwh_anno"] + bc["q_docce_kwh_anno"])
    assert bc["kg_anno"] == pytest.approx(
        bc["kg_giorno"] * bc["giorni_anno"])
    assert bc["e_lav_base_kwh_anno"] == pytest.approx(
        bc["kg_anno"] * bc["e_lav_per_kg"])
    assert bc["e_lav_alt_kwh_anno"] == pytest.approx(
        bc["e_lav_base_kwh_anno"] * bc["f_lav_alt"])
    assert bc["q_rec_pot_kwh_anno"] == pytest.approx(
        bc["eta_rec"] * bc["f_disp"] * bc["q_acs_kwh_anno"])
    assert bc["q_rec_kwh_anno"] == pytest.approx(
        min(bc["q_acs_kwh_anno"], bc["q_rec_pot_kwh_anno"]))
    assert bc["q_acs_net_kwh_anno"] == pytest.approx(
        max(0.0, bc["q_acs_kwh_anno"] - bc["q_rec_kwh_anno"]))
    assert bc["gas_base_kwh_anno"] == pytest.approx(
        (bc["q_risc_kwh_anno"] + bc["q_acs_kwh_anno"])
        / bc["eta_caldaia"])
    assert bc["e_chiller_kwh_anno"] == pytest.approx(
        bc["q_raff_kwh_anno"] / bc["cop_chiller"])
    assert bc["e_base_kwh_anno"] == pytest.approx(
        bc["e_chiller_kwh_anno"] + bc["e_sauna_base_kwh_anno"]
        + bc["e_hammam_base_kwh_anno"] + bc["e_lav_base_kwh_anno"])
    assert bc["e_alt_kwh_anno"] == pytest.approx(
        bc["e_pdc_risc_kwh_anno"] + bc["e_pdc_raff_kwh_anno"]
        + bc["e_pdc_acs_kwh_anno"] + bc["e_sauna_alt_kwh_anno"]
        + bc["e_hammam_alt_kwh_anno"] + bc["e_lav_alt_kwh_anno"])
    assert bc["co2_evitata_t_anno"] == pytest.approx(
        bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])
    assert bc["c_base_eur_anno"] == pytest.approx(
        bc["gas_base_kwh_anno"] / 1000.0 * bc["p_gas"]
        + bc["e_base_kwh_anno"] / 1000.0 * bc["p_el"]
        + bc["om_base"])
    assert bc["c_alt_eur_anno"] == pytest.approx(
        bc["e_alt_kwh_anno"] / 1000.0 * bc["p_el"]
        + bc["om_alt"])


def test_demo_contro_riconteggio_indipendente():
    sup, qri, qra = 400, 90, 55
    gg = 300
    nsa, psa, osa, fsa = 2, 9, 6, 0.85
    nha, pha, oha, fha = 1, 6, 6, 0.85
    lvg, dtv, ldg, dtd = 1500, 25, 400, 30
    kgg, elp, fla = 60, 1.2, 0.55
    ere, fdi = 0.50, 0.60
    eta, copc, copr, copf, copa = 0.90, 3.0, 3.5, 4.0, 3.0
    pg, pel = 100, 260
    omb, oma, cx = 4000, 5500, 25000
    fg, fel, wacc, vita = 0.20, 0.35, 5.0, 15
    qrisc = sup * qri
    qraff = sup * qra
    esb = nsa * psa * osa * gg
    esa = esb * fsa
    ehb = nha * pha * oha * gg
    eha = ehb * fha
    lva = lvg * gg
    qvas = lva * 4.186 * dtv / 3600.0
    lda = ldg * gg
    qdoc = lda * 4.186 * dtd / 3600.0
    qacs = qvas + qdoc
    kga = kgg * gg
    elb = kga * elp
    ela = elb * fla
    qrpo = ere * fdi * qacs
    qrec = min(qacs, qrpo)
    qnet = max(0.0, qacs - qrec)
    gasb = (qrisc + qacs) / eta
    ech = qraff / copc
    epr = qrisc / copr
    epf = qraff / copf
    epa = qnet / copa
    eb = ech + esb + ehb + elb
    ea = epr + epf + epa + esa + eha + ela
    cb = gasb / 1000.0 * pg + eb / 1000.0 * pel + omb
    ca = ea / 1000.0 * pel + oma
    risp = cb - ca
    co2b = gasb / 1000.0 * fg + eb / 1000.0 * fel
    co2a = ea / 1000.0 * fel
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    be = ((ea / 1000.0 * pel + oma
           - eb / 1000.0 * pel - omb)
          / (gasb / 1000.0))
    bc = mh809_demo_calcoli()
    assert bc["q_risc_kwh_anno"] == pytest.approx(qrisc)
    assert bc["q_raff_kwh_anno"] == pytest.approx(qraff)
    assert bc["e_sauna_base_kwh_anno"] == pytest.approx(esb)
    assert bc["e_sauna_alt_kwh_anno"] == pytest.approx(esa)
    assert bc["e_hammam_base_kwh_anno"] == pytest.approx(ehb)
    assert bc["e_hammam_alt_kwh_anno"] == pytest.approx(eha)
    assert bc["litri_vasca_anno"] == pytest.approx(lva)
    assert bc["q_vasca_kwh_anno"] == pytest.approx(qvas)
    assert bc["litri_docce_anno"] == pytest.approx(lda)
    assert bc["q_docce_kwh_anno"] == pytest.approx(qdoc)
    assert bc["q_acs_kwh_anno"] == pytest.approx(qacs)
    assert bc["kg_anno"] == pytest.approx(kga)
    assert bc["e_lav_base_kwh_anno"] == pytest.approx(elb)
    assert bc["e_lav_alt_kwh_anno"] == pytest.approx(ela)
    assert bc["q_rec_pot_kwh_anno"] == pytest.approx(qrpo)
    assert bc["q_rec_kwh_anno"] == pytest.approx(qrec)
    assert bc["q_acs_net_kwh_anno"] == pytest.approx(qnet)
    assert bc["gas_base_kwh_anno"] == pytest.approx(gasb)
    assert bc["e_chiller_kwh_anno"] == pytest.approx(ech)
    assert bc["e_pdc_risc_kwh_anno"] == pytest.approx(epr)
    assert bc["e_pdc_raff_kwh_anno"] == pytest.approx(epf)
    assert bc["e_pdc_acs_kwh_anno"] == pytest.approx(epa)
    assert bc["e_base_kwh_anno"] == pytest.approx(eb)
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
def test_variante_recupero_saturato_e_senza():
    # eta_rec 1,00 e f_disp 1,00: potenziale sopra
    # l'ACS -> SATURA, ACS netta zero, CONVIENTE.
    bc = _variante(eta_rec=1, f_disp=1)
    assert bc["q_rec_pot_kwh_anno"] == pytest.approx(17267.25)
    assert bc["q_rec_kwh_anno"] == pytest.approx(17267.25)
    assert bc["q_acs_net_kwh_anno"] == pytest.approx(0.0, abs=1e-12)
    assert bc["e_pdc_acs_kwh_anno"] == pytest.approx(0.0, abs=1e-12)
    assert bc["risparmio_eur_anno"] == pytest.approx(6432.964285714286)
    assert bc["van"] == pytest.approx(41771.969457542946)
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["payback"] == 4
    assert bc["verdetto"] == "CONVIENTE"
    bc0 = _variante(eta_rec=0)
    assert bc0["q_rec_kwh_anno"] == 0.0
    assert bc0["q_acs_net_kwh_anno"] == pytest.approx(17267.25)
    assert bc0["e_pdc_acs_kwh_anno"] == pytest.approx(5755.75)
    assert bc0["risparmio_eur_anno"] == pytest.approx(4936.469285714284)
    assert bc0["van"] == pytest.approx(26238.86310169586)
    assert bc0["breakeven_gas_eur_mwh"] == pytest.approx(16.593735228628166)
    assert bc0["payback"] == 6
    assert bc0["verdetto"] == "CONVIENTE"


def test_variante_gas_zero_helper_non_calcolabile_come_ui():
    # Negli helper p_gas = 0 e' ammesso e qui il
    # risparmio e' NEGATIVO (-533,17 EUR/anno):
    # verdetto NON_CALCOLABILE anche negli helper,
    # quindi NESSUNA divergenza di verdetto con
    # la guard UI (prezzi <= 0), che lo
    # intercetta prima.
    bc = _variante(p_gas=0)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(-533.1655476190463)
    assert bc["van"] == pytest.approx(-30534.07606202499)
    assert bc["payback"] is None
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(9.008330500582284)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_breakeven_none_numeratore_negativo():
    # p_el 50 e O&M alt zero: numeratore negativo
    # -> breakeven None (a prezzo gas zero
    # l'alternativa e' gia' piu' conveniente).
    bc = _variante(p_el=50, om_alt=0)
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["risparmio_eur_anno"] == pytest.approx(10104.513035714284)
    assert bc["van"] == pytest.approx(79881.38995305233)
    assert bc["payback"] == 3
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_breakeven_none_denominatore_nullo():
    # S = 0 e litri = 0: nessun gas baseline ->
    # breakeven None, ma VAN positiva -> CONVIENTE.
    bc = _variante(superficie_m2=0, litri_vasca_giorno=0,
                   litri_docce_giorno=0)
    assert bc["gas_base_kwh_anno"] == 0.0
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["risparmio_eur_anno"] == pytest.approx(2712.0)
    assert bc["van"] == pytest.approx(3149.632599545759)
    assert bc["payback"] == 10
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_cabine_non_scalano_energia():
    # Le cabine NON scalano l'energia: cambiare
    # solo le cabine lascia identici tutti i KPI.
    bc = _variante(n_cabine=0)
    demo = mh809_demo_calcoli()
    for chiave in ("q_risc_kwh_anno", "q_raff_kwh_anno",
                   "e_sauna_base_kwh_anno", "e_hammam_base_kwh_anno",
                   "q_acs_kwh_anno", "e_lav_base_kwh_anno",
                   "gas_base_kwh_anno", "e_base_kwh_anno",
                   "e_alt_kwh_anno", "c_base_eur_anno",
                   "c_alt_eur_anno", "risparmio_eur_anno",
                   "co2_evitata_t_anno", "van", "tir"):
        assert bc[chiave] == pytest.approx(demo[chiave])
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(n_cabine=12)
    assert bc2["risparmio_eur_anno"] == pytest.approx(demo["risparmio_eur_anno"])


def test_variante_superficie_zero_helper_convinte():
    # Negli helper S = 0 resta calcolabile
    # (risparmio positivo, VAN positiva, verdetto
    # CONVIENTE, breakeven None per numeratore
    # negativo); in UI e' guard degenere
    # (S <= 0): divergenza documentata.
    bc = _variante(superficie_m2=0)
    assert bc["q_risc_kwh_anno"] == 0.0
    assert bc["q_raff_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(3583.0368333333317)
    assert bc["van"] == pytest.approx(12190.697068205445)
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["payback"] == 7
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_conviente_e_zero():
    bc = _variante(capex=50000)
    assert bc["risparmio_eur_anno"] == pytest.approx(5385.417785714286)
    assert bc["van"] == pytest.approx(5898.795008450004)
    assert bc["payback"] == 10
    assert bc["verdetto"] == "CONVIENTE"
    bc0 = _variante(capex=0)
    assert bc0["flussi"][0] == 0
    assert bc0["payback"] == 0
    assert bc0["tir"] is None
    assert bc0["van"] == pytest.approx(55898.795008450004, rel=1e-6)
    assert bc0["verdetto"] == "CONVIENTE"
    # CAPEX 57.000: VAN negativa entro la
    # tolleranza del 10 % (5.700) -> MARGINALE.
    bc2 = _variante(capex=57000)
    assert bc2["van"] == pytest.approx(-1101.204991549996)
    assert bc2["payback"] == 11
    assert bc2["verdetto"] == "MARGINALE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(55781.26678571429)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(16584.76862420312)
    assert bc2["payback"] == 5
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_el_alto_e_om_alt_alto():
    bc = _variante(p_el=400)
    assert bc["risparmio_eur_anno"] == pytest.approx(5906.0209523809535)
    assert bc["van"] == pytest.approx(36302.47785204395)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(0.21225317351926382)
    assert bc["payback"] == 5
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(om_alt=10000)
    assert bc2["risparmio_eur_anno"] == pytest.approx(885.4177857142859)
    assert bc2["van"] == pytest.approx(-15809.666163362654)
    assert bc2["breakeven_gas_eur_mwh"] == pytest.approx(85.04003853882342)
    assert bc2["payback"] is None
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_fattori_alt_uguali_uno():
    # Nessun efficientamento: risparmio positivo
    # ma piccolo, VAN negativa oltre la
    # tolleranza -> NON_CONVIENTE, payback mai.
    bc = _variante(f_sauna_alt=1, f_hammam_alt=1, f_lav_alt=1)
    assert bc["risparmio_eur_anno"] == pytest.approx(1173.4177857142859)
    assert bc["van"] == pytest.approx(-12820.324648366643)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(80.174009224376)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_cop_risc_basso():
    bc = _variante(cop_risc=2.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(3379.703499999996)
    assert bc["van"] == pytest.approx(10080.166600442033)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(42.89674894048412)
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"


def test_monotonia_prezzo_gas_crescente():
    base = mh809_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas=101)["risparmio_eur_anno"]
    basso = _variante(p_gas=99)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(59.18583333333333, abs=1e-2)
    assert base - basso == pytest.approx(59.18583333333333, abs=1e-2)


def test_monotonia_saune_crescente():
    assert _variante(n_saune=1)["risparmio_eur_anno"] < \
        mh809_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(n_saune=4)["risparmio_eur_anno"] > \
        mh809_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(n_saune=4)["e_sauna_base_kwh_anno"] == \
        pytest.approx(64800.0)


def test_demo_deterministica_due_chiamate():
    a = mh809_demo_calcoli()
    b = mh809_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh809_demo().keys()) == {
        "n_cabine", "superficie_m2", "giorni_anno",
        "q_risc_per_m2", "q_raff_per_m2",
        "n_saune", "p_sauna_kw", "ore_sauna_giorno",
        "f_sauna_alt",
        "n_hammam", "p_hammam_kw", "ore_hammam_giorno",
        "f_hammam_alt",
        "litri_vasca_giorno", "delta_t_vasca",
        "litri_docce_giorno", "delta_t_docce",
        "kg_giorno", "e_lav_per_kg", "f_lav_alt",
        "eta_rec", "f_disp",
        "eta_caldaia", "cop_chiller", "cop_risc",
        "cop_raff", "cop_acs",
        "p_gas", "p_el",
        "om_base", "om_alt",
        "capex", "wacc_pct", "vita_anni",
        "f_gas", "f_el",
        "tolleranza_pct"}


# ---------------------------------------------------------------- degenere
def test_degenere_cop_uguale_uno_sollevela():
    with pytest.raises(ValueError):
        _variante(cop_chiller=1.0)
    with pytest.raises(ValueError):
        _variante(cop_risc=1.0)
    with pytest.raises(ValueError):
        _variante(cop_raff=1.0)
    with pytest.raises(ValueError):
        _variante(cop_acs=1.0)


def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"n_cabine": -1},
               {"superficie_m2": -10},
               {"q_risc_per_m2": -10},
               {"q_raff_per_m2": -10},
               {"giorni_anno": 0},
               {"giorni_anno": 2.5},
               {"n_saune": -1},
               {"p_sauna_kw": -0.5},
               {"ore_sauna_giorno": -1},
               {"f_sauna_alt": 0}, {"f_sauna_alt": 1.01},
               {"n_hammam": -1},
               {"p_hammam_kw": -0.5},
               {"ore_hammam_giorno": -1},
               {"f_hammam_alt": 0}, {"f_hammam_alt": 1.01},
               {"litri_vasca_giorno": -1},
               {"delta_t_vasca": 0}, {"delta_t_vasca": -5},
               {"litri_docce_giorno": -1},
               {"delta_t_docce": 0}, {"delta_t_docce": -5},
               {"kg_giorno": -1},
               {"e_lav_per_kg": -0.1},
               {"f_lav_alt": 0}, {"f_lav_alt": 1.01},
               {"eta_rec": -0.1}, {"eta_rec": 1.01},
               {"f_disp": -0.1}, {"f_disp": 1.01},
               {"eta_caldaia": 0}, {"eta_caldaia": 1.01},
               {"cop_chiller": 1.0}, {"cop_chiller": 0.5},
               {"cop_risc": 1.0}, {"cop_risc": 0.5},
               {"cop_raff": 1.0},
               {"cop_acs": 1.0},
               {"p_gas": -1},
               {"p_el": -1},
               {"om_base": -100},
               {"om_alt": -100},
               {"capex": -1},
               {"wacc_pct": -1}, {"wacc_pct": 60},
               {"vita_anni": 0}, {"vita_anni": 2.5},
               {"f_gas": -0.10},
               {"f_el": -0.10},
               {"tolleranza_pct": -1},
               {"tolleranza_pct": 100.1}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh809_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"n_cabine": "6"},
               {"n_cabine": float("nan")},
               {"p_gas": float("inf")},
               {"capex": True},
               {"q_risc_per_m2": "90"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh809_valida(**d)["valido"] is False


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    for kw in ({"p_gas": 0},):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] <= 0.0
        assert bc["verdetto"] == "NON_CALCOLABILE"
        assert bc["flussi"]


def test_pareggio_esatto_tolleranza_float():
    # A pareggio esatto (prezzo gas = breakeven
    # demo) il risparmio e' zero (circa 0.0,
    # quindi guard NON_CALCOLABILE): in nessun
    # caso CONVIENTE.
    be = mh809_demo_calcoli()["breakeven_gas_eur_mwh"]
    bc = _variante(p_gas=be)
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["verdetto"] != "CONVIENTE"
    bc2 = _variante(p_gas=be + 1)
    assert bc2["risparmio_eur_anno"] == pytest.approx(59.18583333333333, abs=1e-2)
    # Risparmio positivo ma piccolo: VAN negativa oltre
    # la tolleranza, quindi NON_CONVIENTE (non CONVIENTE).
    assert bc2["verdetto"] == "NON_CONVIENTE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh809_demo_calcoli()
    testo = mh809_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_gas_eur_mwh" in testo
    assert "co2_evitata_t_anno" in testo
    assert "q_rec_kwh_anno" in testo
    assert "q_rec_pot_kwh_anno" in testo
    assert "n_cabine" in testo
    assert "n_saune" in testo
    assert "e_sauna_alt_kwh_anno" in testo
    assert "e_hammam_alt_kwh_anno" in testo
    assert "e_lav_alt_kwh_anno" in testo
    assert "q_acs_net_kwh_anno" in testo
    assert "e_pdc_risc_kwh_anno" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh809_demo_calcoli()
    testo = mh809_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"q_vasca_kwh_anno;{bc['q_vasca_kwh_anno']}" in testo
    assert f"gas_base_kwh_anno;{bc['gas_base_kwh_anno']}" in testo
    assert f"q_risc_kwh_anno;{bc['q_risc_kwh_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh809_demo_calcoli()
    testo = mh809_csv(bc, _demo_kwargs())
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
    return ["mh" + "80" + "8", "st" + "80" + "8",
            "tab" + "80" + "8", "w" + "80" + "9",
            "mh" + "80" + "7", "tab" + "80" + "7"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w810_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w810_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab809:")


def test_ui_apre_scheda_attesa_una_volta():
    """Il frammento UI apre la scheda attesa, una sola volta."""
    src = _leggi("w810_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert m.group(1) == "809"
    assert src.count("with tab809:") == 1


def test_ui_titolo_atteso():
    src = _leggi("w810_ui.py")
    titolo = ("Centro estetico / SPA: pompa di calore + recupero "
              "calore acque reflue su ACS batte caldaia a gas + "
              "chiller + sauna elettrica tradizionale?")
    assert src.count(titolo) == 2


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w810_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w810_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st809_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) >= 40
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w810_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 4
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_ui_guard_degenere_stretta():
    """La guard UI della scheda dichiara NON_CALCOLABILE
    anche per cabine <= 0, superficie <= 0, prezzi
    <= 0 e CAPEX <= 0 (piu' stretta degli helper,
    che ammettono lo zero)."""
    src = _leggi("w810_ui.py")
    assert "float(_cab809) <= 0.0" in src
    assert "float(_sup809) <= 0.0" in src
    assert "float(_pg809) <= 0.0" in src
    assert "float(_pel809) <= 0.0" in src
    assert "float(_cx809) <= 0.0" in src
    assert "int(_vita809) <= 0" in src
    assert "Verdetto: NON_CALCOLABILE" in src


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w810_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def809[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w810_ui.py")
        usate = set(re.findall(r'_def809\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 37
        assert usate <= set(mh809_demo().keys())
