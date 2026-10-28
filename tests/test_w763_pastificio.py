"""Test tab763 "Pastificio:
essiccare la pasta con calore
recuperato e pompa di calore batte
l'essiccatore a gas?"

Nuova tab tab763 (essiccazione pasta,
file di lavoro w764).
Business case deterministico
dell'essiccazione della pasta fresca
in un pastificio: la pasta fresca va
essiccata dal contenuto di umidita'
iniziale al contenuto di umidita'
finale (base umida), scaldata dalla
temperatura di ingresso alla
temperatura di essiccazione, e il
calore puo' arrivare
dall'essiccatore a gas (baseline,
tutto il calore lordo, senza
recupero) oppure in parte dal calore
recuperato dall'aria esausta calda e
in parte da una pompa di calore che
copre una quota del calore netto, con
il resto che resta a gas.
Massa secca = pasta fresca x (1 - u_i /
100); massa essiccata = massa secca /
(1 - u_f / 100); acqua evaporata =
pasta fresca - massa essiccata;
delta_T = T_ess - T_ingresso; Q_evap =
acqua evaporata x 1000 x 2257 /
3600000; Q_risc = massa essiccata x
1000 x 1,8 x delta_T / 3600000 (cp
1,8 kJ/kgK sulla MASSA FINALE, non
sulla pasta fresca); Q_lordo =
Q_evap + Q_risc; Q_rec =
quota_recupero / 100 x Q_lordo;
Q_netto = Q_lordo - Q_rec;
gas_base = Q_lordo / eta_gas;
C_base = gas_base x p_gas;
co2_base = gas_base x f_gas;
Q_pdc = quota_pdc / 100 x Q_netto;
E_el = Q_pdc / COP; gas_res =
(1 - quota_pdc / 100) x Q_netto /
eta_gas; C_alt_var = gas_res x
p_gas + E_el x p_el; C_alt =
C_alt_var + OM_fisso; co2_alt =
gas_res x f_gas + E_el x f_el;
risparmio = C_base - C_alt;
CO2 evitata = co2_base - co2_alt,
segno libero (puo' essere negativa),
NON monetizzata; fattori di emissione
in tCO2/MWh, numericamente uguali a
kg/kWh (1 kg/kWh = 1 t/MWh: il x1000
MWh -> kWh e il /1000 kg -> t del
brief si cancellano); CRF solo nel
LCO, mai nei flussi; LCO_base =
C_base / massa essiccata; LCO_alt =
(CAPEX x CRF + OM_fisso) / massa
essiccata + C_alt_var / massa
essiccata; prezzo elettrico di
pareggio = (C_base - gas_res x
p_gas - OM_fisso) / E_el, None se
E_el <= 0, sempre positivo nei casi
calcolabili (numeratore = risparmio
+ E_el x p_el > 0); flussi [-CAPEX,
risparmio x vita]; VAN, TIR, payback
(primo anno con cumulato >= 0).
DIFFERENZA CHIAVE RISPETTO ALLA TAB
PRECEDENTE: in questa tab il
risparmio nullo o negativo E'
degenere (NON_CALCOLABILE), non un
caso calcolabile. Distinta dalla tab
dell'essiccazione del legname (li'
si essicca legname verde, con calore
specifico del legname umido 2,0
kJ/kgK applicato al legname verde),
dalla tab della cartiera (li' si
essicca carta, senza pasta, senza
umidita' della pasta in % base umida,
senza massa secca di pasta, senza
acqua evaporata dalla pasta), dalla
tab della tintoria (li' si tinge
tessuto in bagni caldi, senza pasta,
senza umidita' della pasta, senza
acqua evaporata, senza calore latente
di evaporazione), dalla tab del
caseificio (li' si pastorizza latte,
senza pasta e senza essiccazione),
dalla tab del birrificio (li' si
produce birra, senza pasta e senza
essiccazione), dalla tab del
conservificio (li' si sterilizzano
conserve in autoclave, senza pasta e
senza essiccazione), dalla tab della
lavanderia (li' si lava biancheria,
senza pasta, senza umidita' della
pasta, senza acqua evaporata), dalla
caldaia a elettrodi generica (li' il
calore viene da elettrodi, senza
processo di essiccazione della pasta
e senza quota di recupero) e dal
recupero calore generico (li' il
calore recuperato va a un uso
generico, senza essiccazione della
pasta e senza pompa di calore sul
calore netto).

Demo calcolata eseguendo demo_calcoli()
(e ricontrollata a mano, riga per
riga): pasta fresca 4.000 t/anno,
umidita' iniziale 30 % (base umida),
umidita' finale 12,5 %, temperatura
ingresso 25 C, temperatura
essiccazione 55 C, rendimento gas
0,90, quota recupero 35 %, quota PdC
70 %, COP 3,4, prezzo gas 45 EUR/MWh,
prezzo elettrico 110 EUR/MWh, O&M
fisso 12.000 EUR/anno, CAPEX 260.000
EUR, fattore gas 0,20 tCO2/MWh e
fattore elettrico 0,25 tCO2/MWh,
WACC 5 %, vita 15 anni, tolleranza
10 % del CAPEX.

- m_secca_t_anno = 2800.0
- m_finale_t_anno = 3200.0
- m_acqua_t_anno = 800.0
- delta_t_K = 30.0
- q_evap_mwh_anno = 501.55555555555554
- q_risc_mwh_anno = 48.0
- q_lordo_mwh_anno = 549.5555555555555
- q_rec_mwh_anno = 192.34444444444443
- q_netto_mwh_anno = 357.2111111111111
- gas_base_mwh_anno = 610.6172839506172
- c_base_eur_anno = 27477.777777777774
- q_pdc_mwh_anno = 250.04777777777775
- e_el_mwh_anno = 73.54346405228758
- gas_res_mwh_anno = 119.0703703703704
- c_alt_var_eur_anno = 13447.947712418301
- c_alt_eur_anno = 25447.947712418303
- risparmio_eur_anno = 2029.8300653594706
- co2_base_t_anno = 122.12345679012344
- co2_alt_gas_t_anno = 23.81407407407408
- co2_alt_el_t_anno = 18.385866013071894
- co2_alt_t_anno = 42.199940087145976
- co2_evitata_t_anno = 79.92351670297747
- crf = 0.09634228760924432
- quota_capex_eur_anno = 25048.994778403525
- lco_base_eur_t = 8.586805555555554
- lco_alt_eur_t = 15.78029452838182
- van = -238931.05804595098
- tir = -19.525780621104964
- payback = None
- prezzo_pareggio_eur_mwh = 137.60041414307483
- verdetto = 'NON_CONVIENTE'

Scomposizione: massa secca = 4.000 x
(1 - 0,30) = 2.800 t/anno; massa
essiccata = 2.800 / (1 - 0,125) =
3.200 t/anno; acqua evaporata =
4.000 - 3.200 = 800 t/anno;
delta_T = 55 - 25 = 30 K; Q_evap =
800 x 1000 x 2257 / 3.600.000 =
501,56 MWh/anno; Q_risc = 3.200 x 1000
x 1,8 x 30 / 3.600.000 = 48,00
MWh/anno (sulla massa finale, cp
1,8); Q_lordo = 501,56 + 48,00 =
549,56 MWh/anno; Q_rec = 0,35 x 549,56
= 192,34 MWh/anno; Q_netto = 549,56 -
192,34 = 357,21 MWh/anno; gas_base =
549,56 / 0,90 = 610,62 MWh/anno;
C_base = 610,62 x 45 = 27.477,78
EUR/anno; Q_pdc = 0,70 x 357,21 =
250,05 MWh/anno; E_el = 250,05 / 3,4 =
73,54 MWh/anno; gas_res = 0,30 x 357,21
/ 0,90 = 119,07 MWh/anno;
C_alt_var = 119,07 x 45 + 73,54 x 110
= 5.358,17 + 8.089,78 = 13.447,95
EUR/anno; C_alt = 13.447,95 + 12.000 =
25.447,95 EUR/anno; risparmio =
27.477,78 - 25.447,95 = 2.029,83
EUR/anno; CO2 base = 610,62 x 0,20 =
122,12 t/anno; CO2 alt = 119,07 x 0,20 +
73,54 x 0,25 = 23,81 + 18,39 = 42,20
t/anno; CO2 evitata = 79,92 t/anno;
CRF 0,05 x 1,05^15 / (1,05^15 - 1) =
0.09634228760924432; quota CAPEX
260.000 x 0,096342 = 25.048,99
EUR/anno; LCO base 27.477,78 /
3.200 = 8,59 EUR/t; LCO alt
(25.048,99 + 12.000) / 3.200 +
13.447,95 / 3.200 = 15,78 EUR/t;
flussi: anno 0 -260.000, anni 1-15
risparmio 2.029,83 (piatti); VAN
-260.000 + 2.029,83 x 10,379658
(annuita' 15 anni al 5 %) =
-238.931,06 EUR; TIR -19,53 %; nessun
payback (il cumulato all'anno 15 e'
-229.552,55 EUR); prezzo elettrico di
pareggio (27.477,78 - 5.358,17 -
12.000) / 73,54 = 137,60 EUR/MWh;
verdetto NON_CONVIENTE perche' VAN < 0
e |VAN| = 238.931,06 > 10 % del CAPEX
(26.000): il risparmio annuo positivo
NON basta a ripagare il CAPEX in 15
anni al 5 %.
NOTA: il CRF entra solo nel LCO,
mai nei flussi: il CAPEX compare una
sola volta, all'anno 0.
NOTA 2: in questa tab il risparmio
nullo o negativo E' degenere: con
prezzo gas 30 EUR/MWh il caso e'
NON_CALCOLABILE (valid=False, flussi
vuoti), non un caso calcolabile.
NOTA 3: la CO2 evitata puo' essere
negativa: con fattore elettrico 2,00
tCO2/MWh la CO2 evitata e'
-48,78 t/anno, pur restando il caso
calcolabile.
NOTA 4: il prezzo elettrico di
pareggio nei casi calcolabili e'
sempre positivo (numeratore =
risparmio + E_el x p_el > 0); come
valore della funzione pura puo'
essere negativo: con O&M fisso
5.000.000 EUR/anno il pareggio e'
-67.686,24 EUR/MWh, perche' il solo
O&M fisso piu' il gas residuo
superano gia' il costo baseline (ma
quel caso e' degenere per la regola
del risparmio).
NOTA 5: la quota PdC zero NON e'
degenere di per se', ma con la demo
il risparmio che ne risulta e'
negativo, quindi il caso diventa
degenere (NON_CALCOLABILE) per la
regola del risparmio.
NOTA 6: il calore netto nullo (quota
recupero 100 %) NON e' degenere:
il risparmio e' 15.477,78 EUR/anno
(27.477,78 - 12.000 di solo O&M fisso)
e la VAN -99.345,96 EUR, e il
pareggio non e' definito.
NOTA 7: l'umidita' iniziale deve
superare l'umidita' finale e la
temperatura di essiccazione deve
superare la temperatura di ingresso:
con u_i = u_f (nessuna acqua da
evaporare) o con T_ess = T_ingresso
(delta_T 0) o sotto, il caso e'
degenere (valid=False,
NON_CALCOLABILE).
NOTA 8: Q_risc usa la massa finale
(cp 1,8 kJ/kgK), non la pasta fresca:
con la demo Q_risc = 48,00 MWh/anno,
mentre sulla pasta fresca sarebbe
60,00 MWh/anno.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w764_helpers import (
    demo_calcoli,
    mh763_c_alt,
    mh763_c_alt_var,
    mh763_c_base,
    mh763_calcola,
    mh763_co2_alt,
    mh763_co2_base,
    mh763_co2_evitata,
    mh763_crf,
    mh763_csv,
    mh763_delta_t,
    mh763_demo,
    mh763_e_el,
    mh763_eta,
    mh763_flussi,
    mh763_gas_base,
    mh763_gas_res,
    mh763_int_pos,
    mh763_lco_alt,
    mh763_lco_base,
    mh763_m_acqua,
    mh763_m_finale,
    mh763_m_secca,
    mh763_nneg,
    mh763_num,
    mh763_payback,
    mh763_pct_0_100,
    mh763_pct_wacc,
    mh763_pos,
    mh763_prezzo_pareggio,
    mh763_q_evap,
    mh763_q_lordo,
    mh763_q_netto,
    mh763_q_pdc,
    mh763_q_rec,
    mh763_q_risc,
    mh763_quota_capex,
    mh763_risparmio,
    mh763_temp_ess,
    mh763_temp_ingresso,
    mh763_tir,
    mh763_u_finale,
    mh763_u_iniziale,
    mh763_valida,
    mh763_van,
    mh763_verdetto,
)


def _demo_kwargs():
    return dict(mh763_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh763_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh763_num(3, "x") == 3.0
    assert mh763_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh763_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh763_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh763_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh763_pos(0, "x")
    with pytest.raises(ValueError):
        mh763_pos(-1, "x")
    assert mh763_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh763_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh763_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh763_int_pos(0, "x")


def test_pct_0_100_limiti():
    assert mh763_pct_0_100(0, "x") == 0.0
    assert mh763_pct_0_100(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh763_pct_0_100(100.1, "x")
    with pytest.raises(ValueError):
        mh763_pct_0_100(-1, "x")


def test_pct_wacc_limiti():
    assert mh763_pct_wacc(0, "x") == 0.0
    assert mh763_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh763_pct_wacc(50.1, "x")


def test_eta_limiti():
    assert mh763_eta(1.0, "x") == 1.0
    assert mh763_eta(0.90, "x") == 0.90
    with pytest.raises(ValueError):
        mh763_eta(0, "x")
    with pytest.raises(ValueError):
        mh763_eta(-0.1, "x")
    with pytest.raises(ValueError):
        mh763_eta(1.01, "x")


def test_temp_limiti():
    assert mh763_temp_ingresso(0, "x") == 0.0
    assert mh763_temp_ingresso(99.0, "x") == 99.0
    with pytest.raises(ValueError):
        mh763_temp_ingresso(100, "x")
    with pytest.raises(ValueError):
        mh763_temp_ingresso(-1, "x")
    assert mh763_temp_ess(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh763_temp_ess(0, "x")
    with pytest.raises(ValueError):
        mh763_temp_ess(100.1, "x")


def test_umidita_limiti():
    assert mh763_u_iniziale(30, "x") == 30.0
    assert mh763_u_iniziale(99.9, "x") == 99.9
    with pytest.raises(ValueError):
        mh763_u_iniziale(0, "x")
    with pytest.raises(ValueError):
        mh763_u_iniziale(100, "x")
    with pytest.raises(ValueError):
        mh763_u_iniziale(-1, "x")
    assert mh763_u_finale(0, "x") == 0.0
    assert mh763_u_finale(12.5, "x") == 12.5
    with pytest.raises(ValueError):
        mh763_u_finale(100, "x")
    with pytest.raises(ValueError):
        mh763_u_finale(-1, "x")


# ---------------------------------------------------------------- fisica base
def test_masse():
    assert mh763_m_secca(4000, 30.0) == pytest.approx(2800.0)
    assert mh763_m_secca(4000, 0) == pytest.approx(4000.0)
    assert mh763_m_secca(4000, 100) == pytest.approx(0.0)
    assert mh763_m_finale(2800.0, 12.5) == pytest.approx(3200.0)
    assert mh763_m_finale(2800.0, 0) == pytest.approx(2800.0)
    assert mh763_m_acqua(4000, 3200.0) == pytest.approx(800.0)
    assert mh763_m_acqua(4000, 4000) == 0.0
    with pytest.raises(ValueError):
        mh763_m_finale(2800.0, 100)
    with pytest.raises(ValueError):
        mh763_m_secca(4000, 100.1)


def test_delta_q_evap_q_risc_q_lordo():
    assert mh763_delta_t(25, 55) == pytest.approx(30.0)
    assert mh763_delta_t(55, 25) == pytest.approx(-30.0)
    assert mh763_q_evap(800.0) == pytest.approx(501.55555555555554)
    assert mh763_q_evap(0) == 0.0
    assert mh763_q_risc(3200, 30.0) == pytest.approx(48.0)
    assert mh763_q_risc(4000, 30.0) == pytest.approx(60.0)
    assert mh763_q_risc(3200, 0) == 0.0
    assert mh763_q_lordo(501.55555555555554, 48.0) == \
        pytest.approx(549.5555555555555)
    with pytest.raises(ValueError):
        mh763_q_evap(-1)
    with pytest.raises(ValueError):
        mh763_q_risc(-1, 30.0)


def test_q_rec_netto():
    assert mh763_q_rec(549.5555555555555, 35.0) == pytest.approx(
        192.34444444444443)
    assert mh763_q_rec(549.5555555555555, 0) == 0.0
    assert mh763_q_rec(549.5555555555555, 100) == pytest.approx(
        549.5555555555555)
    assert mh763_q_netto(549.5555555555555, 192.34444444444443) == \
        pytest.approx(357.2111111111111)
    assert mh763_q_netto(549.5555555555555, 549.5555555555555) == 0.0
    with pytest.raises(ValueError):
        mh763_q_rec(549.5555555555555, 100.1)


def test_gas_base_e_c_base_e_co2_base():
    assert mh763_gas_base(549.5555555555555, 0.90) == pytest.approx(
        610.6172839506172)
    assert mh763_gas_base(549.5555555555555, 1.0) == pytest.approx(
        549.5555555555555)
    assert mh763_c_base(610.6172839506172, 45) == pytest.approx(
        27477.777777777774)
    assert mh763_co2_base(610.6172839506172, 0.20) == pytest.approx(
        122.12345679012344)
    with pytest.raises(ValueError):
        mh763_gas_base(549.5555555555555, 0)


def test_q_pdc_e_e_el():
    assert mh763_q_pdc(357.2111111111111, 70.0) == pytest.approx(
        250.04777777777775)
    assert mh763_q_pdc(357.2111111111111, 0) == 0.0
    assert mh763_q_pdc(357.2111111111111, 100) == pytest.approx(
        357.2111111111111)
    assert mh763_e_el(250.04777777777775, 3.4) == pytest.approx(
        73.54346405228758)
    assert mh763_e_el(250.04777777777775, 0) is None
    assert mh763_e_el(250.04777777777775, -1.0) is None
    assert mh763_e_el(0.0, 3.4) == 0.0
    with pytest.raises(ValueError):
        mh763_q_pdc(357.2111111111111, 100.1)


def test_gas_res():
    assert mh763_gas_res(357.2111111111111, 70.0, 0.90) == pytest.approx(
        119.0703703703704)
    assert mh763_gas_res(357.2111111111111, 0, 0.90) == pytest.approx(
        396.9012345679012)
    assert mh763_gas_res(357.2111111111111, 100, 0.90) == 0.0
    with pytest.raises(ValueError):
        mh763_gas_res(357.2111111111111, 70.0, 0)


def test_c_alt_var_e_c_alt():
    assert mh763_c_alt_var(119.0703703703704, 45, 73.54346405228758,
                           110) == pytest.approx(13447.947712418301)
    assert mh763_c_alt_var(119.0703703703704, 45, 0.0,
                           110) == pytest.approx(5358.166666666668)
    assert mh763_c_alt(13447.947712418301, 12000) == pytest.approx(
        25447.947712418303)
    assert mh763_c_alt(13447.947712418301, 0) == pytest.approx(
        13447.947712418301)
    with pytest.raises(ValueError):
        mh763_c_alt_var(119.0703703703704, -1, 73.54346405228758, 110)


def test_risparmio_segno():
    assert mh763_risparmio(27477.777777777774, 25447.947712418303) == \
        pytest.approx(2029.8300653594706)
    assert mh763_risparmio(27477.777777777774, 27477.777777777774) == 0.0


def test_co2_alt_e_evitata_segno_libero():
    assert mh763_co2_alt(119.0703703703704, 0.20, 73.54346405228758,
                         0.25) == pytest.approx(42.199940087145976)
    assert mh763_co2_evitata(122.12345679012344,
                             42.199940087145976) == pytest.approx(
        79.92351670297747)
    assert mh763_co2_evitata(122.12345679012344,
                             722.12345679012344) == pytest.approx(
        -600.0, abs=1e-6)


# ---------------------------------------------------------------- finanza base
def test_crf():
    assert mh763_crf(5.0, 15) == pytest.approx(0.09634228760924432)
    assert mh763_crf(0, 15) == pytest.approx(1.0 / 15.0)
    assert mh763_crf(5.0, 1) == pytest.approx(1.05)
    assert mh763_crf(5.0, 10) == pytest.approx(0.12950457496545661)


def test_quota_capex_e_lco():
    assert mh763_quota_capex(260000, 0.09634228760924432) == pytest.approx(
        25048.994778403525)
    assert mh763_lco_base(27477.777777777774, 3200.0) == \
        pytest.approx(8.586805555555554)
    assert mh763_lco_base(27477.777777777774, 0) is None
    assert mh763_lco_alt(260000, 0.09634228760924432, 12000,
                         13447.947712418301,
                         3200.0) == pytest.approx(
        15.78029452838182)
    assert mh763_lco_alt(260000, 0.09634228760924432, 12000,
                         13447.947712418301, 0) is None
    assert mh763_lco_alt(0, 0.09634228760924432, 12000,
                         13447.947712418301,
                         3200.0) == pytest.approx(
        7.952483660130719)


def test_prezzo_pareggio_formula_brief_negativo_e_none():
    assert mh763_prezzo_pareggio(27477.777777777774, 119.0703703703704,
                                 45, 12000,
                                 73.54346405228758) == pytest.approx(
        137.60041414307483)
    assert mh763_prezzo_pareggio(27477.777777777774, 119.0703703703704,
                                 45, 22119.611111111106,
                                 73.54346405228758) == pytest.approx(
        0.0, abs=1e-6)
    assert mh763_prezzo_pareggio(27477.777777777774, 119.0703703703704,
                                 45, 12000, 0.0) is None
    assert mh763_prezzo_pareggio(27477.777777777774, 119.0703703703704,
                                 45, 12000, None) is None


def test_prezzo_pareggio_negativo_solo_funzione_pura():
    """Il pareggio negativo esiste solo come valore della
    funzione pura: con O&M fisso 5.000.000 il numeratore e'
    negativo, ma quel caso e' degenere per la regola del
    risparmio e mh763_calcola non lo restituisce mai."""
    bc = demo_calcoli()
    assert mh763_prezzo_pareggio(bc["c_base_eur_anno"],
                                 bc["gas_res_mwh_anno"], 45, 5000000,
                                 bc["e_el_mwh_anno"]) == pytest.approx(
        -67686.23769679572)
    assert bc["prezzo_pareggio_eur_mwh"] > 0.0


def test_flussi_lunghezza_e_primo():
    fl = mh763_flussi(260000, 2029.8300653594706, 15)
    assert len(fl) == 16
    assert fl[0] == -260000
    assert all(f == 2029.8300653594706 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = demo_calcoli()
    assert bc["van"] == pytest.approx(-238931.05804595098)
    assert mh763_van([-260000] + [2029.8300653594706] * 15,
                     0) == pytest.approx(-229552.54901960783)
    assert mh763_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo_e_negativa():
    bc = demo_calcoli()
    assert bc["tir"] == pytest.approx(-19.525780621104964)
    assert mh763_tir([-260000] + [2029.8300653594706] * 15) == pytest.approx(
        -0.19525780621104964)
    tir = mh763_tir([-260000] + [2029.8300653594706] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-260000] + [2029.8300653594706] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback():
    assert mh763_payback([-260000] + [2029.8300653594706] * 15) is None
    assert mh763_payback([-260000] + [-1000.0] * 15) is None
    assert mh763_payback([0] + [2029.8300653594706] * 15) == 0
    assert mh763_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh763_verdetto(100.0, 260000, 10.0) == "CONVIENTE"
    assert mh763_verdetto(-25000.0, 260000, 10.0) == "MARGINALE"
    assert mh763_verdetto(-26000.0, 260000, 10.0) == "MARGINALE"
    assert mh763_verdetto(-26000.01, 260000, 10.0) == "NON_CONVIENTE"
    assert mh763_verdetto(float("nan"), 260000, 10.0) == "NON_CALCOLABILE"
    assert mh763_verdetto(0.0, 0, 10.0) == "MARGINALE"


def test_valida_demo_ok():
    v = mh763_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("m_pasta_t_anno", "4000"),
                       ("m_pasta_t_anno", float("nan")),
                       ("m_pasta_t_anno", float("inf")),
                       ("m_pasta_t_anno", True),
                       ("prezzo_el_eur_mwh", None)):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh763_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("m_pasta_t_anno", 0),
                          ("m_pasta_t_anno", -1),
                          ("u_i_pct", 0),
                          ("u_i_pct", 100),
                          ("u_i_pct", -1),
                          ("u_f_pct", -1),
                          ("u_f_pct", 100),
                          ("t_ingresso_C", -1),
                          ("t_ingresso_C", 100),
                          ("t_ess_C", 0),
                          ("t_ess_C", 100.1),
                          ("eta_gas", 0),
                          ("eta_gas", 1.01),
                          ("quota_recupero_pct", -1),
                          ("quota_recupero_pct", 100.1),
                          ("quota_pdc_pct", -1),
                          ("quota_pdc_pct", 100.1),
                          ("cop", 0), ("cop", -1),
                          ("prezzo_gas_eur_mwh", -1),
                          ("prezzo_el_eur_mwh", -1),
                          ("om_fisso_eur_anno", -100),
                          ("capex_eur", -1),
                          ("f_gas_t_per_mwh", -0.10),
                          ("f_el_t_per_mwh", -0.10),
                          ("wacc_pct", -0.1), ("wacc_pct", 50.1),
                          ("vita_anni", 0), ("vita_anni", 2.5),
                          ("tolleranza_pct", -1),
                          ("tolleranza_pct", 100.1)):
        d = _demo_kwargs()
        d[campo] = valore
        assert mh763_valida(**d)["valido"] is False


def test_valida_rifiuta_delta_e_umidita_non_validi():
    for ti, te in ((55, 55), (55, 25), (25, 25)):
        d = _demo_kwargs()
        d["t_ingresso_C"] = ti
        d["t_ess_C"] = te
        assert mh763_valida(**d)["valido"] is False
    for ui, uf in ((12.5, 12.5), (12.5, 30), (5, 12.5)):
        d = _demo_kwargs()
        d["u_i_pct"] = ui
        d["u_f_pct"] = uf
        assert mh763_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"quota_recupero_pct": 0, "quota_pdc_pct": 0,
              "prezzo_gas_eur_mwh": 0,
              "prezzo_el_eur_mwh": 0, "om_fisso_eur_anno": 0,
              "capex_eur": 0, "f_gas_t_per_mwh": 0,
              "f_el_t_per_mwh": 0, "wacc_pct": 0,
              "tolleranza_pct": 0, "eta_gas": 1.0,
              "t_ingresso_C": 0, "t_ess_C": 100,
              "u_i_pct": 99, "u_f_pct": 0})
    assert mh763_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["quota_pdc_pct"] = 100
    d["quota_recupero_pct"] = 100
    assert mh763_valida(**d)["valido"] is True


def test_valida_non_controlla_risparmio_calcola_si():
    """La validazione input NON controlla il risparmio
    (e' un esito, non un range): con gas 30 la
    validazione passa, ma mh763_calcola e' degenere
    per la regola del risparmio."""
    d = _demo_kwargs()
    d["prezzo_gas_eur_mwh"] = 30
    assert mh763_valida(**d)["valido"] is True
    bc = _variante(prezzo_gas_eur_mwh=30)
    assert bc["valid"] is False
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_demo_dict():
    d = mh763_demo()
    assert d["m_pasta_t_anno"] == 4000
    assert d["u_i_pct"] == 30.0
    assert d["u_f_pct"] == 12.5
    assert d["t_ingresso_C"] == 25
    assert d["t_ess_C"] == 55
    assert d["eta_gas"] == 0.90
    assert d["quota_recupero_pct"] == 35.0
    assert d["quota_pdc_pct"] == 70.0
    assert d["cop"] == 3.4
    assert d["prezzo_gas_eur_mwh"] == 45
    assert d["prezzo_el_eur_mwh"] == 110
    assert d["om_fisso_eur_anno"] == 12000
    assert d["capex_eur"] == 260000
    assert d["f_gas_t_per_mwh"] == 0.20
    assert d["f_el_t_per_mwh"] == 0.25
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    """Ogni _DEMO del test contro demo_calcoli():
    scarto relativo < 1e-9 (zero atteso:
    confronto assoluto)."""
    bc = demo_calcoli()
    attesi = {
        "m_secca_t_anno": 2800.0,
        "m_finale_t_anno": 3200.0,
        "m_acqua_t_anno": 800.0,
        "delta_t_K": 30.0,
        "q_evap_mwh_anno": 501.55555555555554,
        "q_risc_mwh_anno": 48.0,
        "q_lordo_mwh_anno": 549.5555555555555,
        "q_rec_mwh_anno": 192.34444444444443,
        "q_netto_mwh_anno": 357.2111111111111,
        "gas_base_mwh_anno": 610.6172839506172,
        "c_base_eur_anno": 27477.777777777774,
        "q_pdc_mwh_anno": 250.04777777777775,
        "e_el_mwh_anno": 73.54346405228758,
        "gas_res_mwh_anno": 119.0703703703704,
        "c_alt_var_eur_anno": 13447.947712418301,
        "c_alt_eur_anno": 25447.947712418303,
        "risparmio_eur_anno": 2029.8300653594706,
        "co2_base_t_anno": 122.12345679012344,
        "co2_alt_t_anno": 42.199940087145976,
        "co2_evitata_t_anno": 79.92351670297747,
        "crf": 0.09634228760924432,
        "quota_capex_eur_anno": 25048.994778403525,
        "lco_base_eur_t": 8.586805555555554,
        "lco_alt_eur_t": 15.78029452838182,
        "van": -238931.05804595098,
        "tir": -19.525780621104964,
        "prezzo_pareggio_eur_mwh": 137.60041414307483,
    }
    for chiave, atteso in attesi.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert abs(got - atteso) / abs(atteso) < 1e-9, chiave
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_demo_calcoli_fisica():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["m_secca_t_anno"] == pytest.approx(2800.0)
    assert bc["m_finale_t_anno"] == pytest.approx(3200.0)
    assert bc["m_acqua_t_anno"] == pytest.approx(800.0)
    assert bc["q_evap_mwh_anno"] == pytest.approx(501.55555555555554)
    assert bc["q_risc_mwh_anno"] == pytest.approx(48.0)
    assert bc["q_lordo_mwh_anno"] == pytest.approx(549.5555555555555)
    assert bc["q_rec_mwh_anno"] == pytest.approx(192.34444444444443)
    assert bc["q_netto_mwh_anno"] == pytest.approx(357.2111111111111)
    assert bc["gas_base_mwh_anno"] == pytest.approx(610.6172839506172)
    assert bc["co2_evitata_t_anno"] == pytest.approx(79.92351670297747)


def test_demo_calcoli_economia():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(27477.777777777774)
    assert bc["c_alt_var_eur_anno"] == pytest.approx(13447.947712418301)
    assert bc["c_alt_eur_anno"] == pytest.approx(25447.947712418303)
    assert bc["risparmio_eur_anno"] == pytest.approx(2029.8300653594706)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(137.60041414307483)


def test_demo_calcoli_finanza():
    bc = demo_calcoli()
    assert bc["crf"] == pytest.approx(0.09634228760924432)
    assert bc["quota_capex_eur_anno"] == pytest.approx(25048.994778403525)
    assert bc["lco_base_eur_t"] == pytest.approx(8.586805555555554)
    assert bc["lco_alt_eur_t"] == pytest.approx(15.78029452838182)
    assert bc["van"] == pytest.approx(-238931.05804595098)
    assert bc["tir"] == pytest.approx(-19.525780621104964)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_demo_flussi_e_cumulato():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -260000
    assert len(bc["flussi"]) == 16
    assert all(f == 2029.8300653594706 for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -260000
    assert righe.iloc[5]["Cumulato (EUR)"] == pytest.approx(-249850.85)
    assert righe.iloc[9]["Cumulato (EUR)"] == pytest.approx(-241731.53)
    assert righe.iloc[10]["Cumulato (EUR)"] == pytest.approx(-239701.70)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(-229552.55)
    assert righe.iloc[15]["Flusso (EUR/anno)"] == 2029.8300653594706


def test_demo_tabella_righe():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Calore lordo (MWh/anno)"] == pytest.approx(549.5555555555555)
    assert mappa["Calore recuperato (MWh/anno)"] == pytest.approx(192.34444444444443)
    assert mappa["Calore netto (MWh/anno)"] == pytest.approx(357.2111111111111)
    assert mappa["Massa essiccata (t/anno)"] == pytest.approx(3200.0)
    assert mappa["Acqua evaporata (t/anno)"] == pytest.approx(800.0)
    assert mappa["Salto termico (K)"] == pytest.approx(30.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(25447.947712418303)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(2029.8300653594706)
    assert mappa["Payback (anni)"] is None
    assert mappa["Verdetto"] == "NON_CONVIENTE"
    assert mappa["Prezzo elettrico di pareggio (EUR/MWh)"] == pytest.approx(
        137.60041414307483)


def test_demo_coerenza_interna():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["c_alt_var_eur_anno"] + bc["om_fisso_eur_anno"] == \
        pytest.approx(bc["c_alt_eur_anno"])
    assert bc["gas_base_mwh_anno"] * bc["prezzo_gas_eur_mwh"] == \
        pytest.approx(bc["c_base_eur_anno"])
    assert bc["co2_base_t_anno"] - bc["co2_alt_t_anno"] == \
        pytest.approx(bc["co2_evitata_t_anno"])
    assert bc["capex_eur"] * bc["crf"] == pytest.approx(
        bc["quota_capex_eur_anno"])
    assert (bc["quota_capex_eur_anno"] + bc["om_fisso_eur_anno"]) / \
        bc["m_finale_t_anno"] + bc["c_alt_var_eur_anno"] / \
        bc["m_finale_t_anno"] == pytest.approx(bc["lco_alt_eur_t"])
    assert bc["c_base_eur_anno"] - bc["gas_res_mwh_anno"] * \
        bc["prezzo_gas_eur_mwh"] - bc["om_fisso_eur_anno"] == \
        pytest.approx(bc["prezzo_pareggio_eur_mwh"] *
                      bc["e_el_mwh_anno"])
    assert bc["q_lordo_mwh_anno"] - bc["q_rec_mwh_anno"] == \
        pytest.approx(bc["q_netto_mwh_anno"])
    assert bc["q_evap_mwh_anno"] + bc["q_risc_mwh_anno"] == \
        pytest.approx(bc["q_lordo_mwh_anno"])
    assert bc["m_pasta_t_anno"] * (1.0 - bc["u_i_pct"] / 100.0) == \
        pytest.approx(bc["m_secca_t_anno"])
    assert bc["m_secca_t_anno"] / (1.0 - bc["u_f_pct"] / 100.0) == \
        pytest.approx(bc["m_finale_t_anno"])
    assert bc["m_pasta_t_anno"] - bc["m_finale_t_anno"] == \
        pytest.approx(bc["m_acqua_t_anno"])
    assert bc["m_acqua_t_anno"] * 1000.0 * 2257.0 / \
        3600000.0 == pytest.approx(bc["q_evap_mwh_anno"])
    assert bc["m_finale_t_anno"] * 1000.0 * 1.8 * \
        bc["delta_t_K"] / 3600000.0 == pytest.approx(
        bc["q_risc_mwh_anno"])


def test_demo_crf_solo_nel_lco_non_nei_flussi():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -bc["capex_eur"]
    assert all(f == bc["risparmio_eur_anno"] for f in bc["flussi"][1:])
    assert bc["crf"] not in bc["flussi"]
    assert bc["quota_capex_eur_anno"] not in bc["flussi"]
    van_da_flussi = mh763_van(bc["flussi"], bc["wacc_pct"])
    assert van_da_flussi == pytest.approx(bc["van"])
    assert bc["lco_alt_eur_t"] == pytest.approx(
        (bc["capex_eur"] * bc["crf"] + bc["om_fisso_eur_anno"]) /
        bc["m_finale_t_anno"] + bc["c_alt_var_eur_anno"] /
        bc["m_finale_t_anno"])


def test_demo_contro_riconteggio_indipendente():
    mp, ui, uf, ti, te = 4000, 30.0, 12.5, 25, 55
    eta, qr, quota, cop = 0.90, 35.0, 70.0, 3.4
    pg, pe, om, cx = 45, 110, 12000, 260000
    fg, fe, wacc, vita = 0.20, 0.25, 5.0, 15
    ms = mp * (1 - ui / 100)
    mf = ms / (1 - uf / 100)
    ma = mp - mf
    qe = ma * 1000 * 2257 / 3600000.0
    qri = mf * 1000 * 1.8 * (te - ti) / 3600000.0
    ql = qe + qri
    qrec = qr / 100 * ql
    qn = ql - qrec
    gb = ql / eta
    cb = gb * pg
    qp = quota / 100 * qn
    ee = qp / cop
    gr = (1 - quota / 100) * qn / eta
    cav = gr * pg + ee * pe
    ca = cav + om
    risp = cb - ca
    co2b = gb * fg
    co2a = gr * fg + ee * fe
    r = wacc / 100.0
    crf = r * (1 + r) ** vita / ((1 + r) ** vita - 1)
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    bc = demo_calcoli()
    assert bc["m_secca_t_anno"] == pytest.approx(ms)
    assert bc["m_finale_t_anno"] == pytest.approx(mf)
    assert bc["m_acqua_t_anno"] == pytest.approx(ma)
    assert bc["q_evap_mwh_anno"] == pytest.approx(qe)
    assert bc["q_risc_mwh_anno"] == pytest.approx(qri)
    assert bc["q_lordo_mwh_anno"] == pytest.approx(ql)
    assert bc["q_rec_mwh_anno"] == pytest.approx(qrec)
    assert bc["q_netto_mwh_anno"] == pytest.approx(qn)
    assert bc["gas_base_mwh_anno"] == pytest.approx(gb)
    assert bc["c_base_eur_anno"] == pytest.approx(cb)
    assert bc["q_pdc_mwh_anno"] == pytest.approx(qp)
    assert bc["e_el_mwh_anno"] == pytest.approx(ee)
    assert bc["gas_res_mwh_anno"] == pytest.approx(gr)
    assert bc["c_alt_var_eur_anno"] == pytest.approx(cav)
    assert bc["c_alt_eur_anno"] == pytest.approx(ca)
    assert bc["risparmio_eur_anno"] == pytest.approx(risp)
    assert bc["co2_base_t_anno"] == pytest.approx(co2b)
    assert bc["co2_alt_t_anno"] == pytest.approx(co2a)
    assert bc["crf"] == pytest.approx(crf)
    assert bc["van"] == pytest.approx(van)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(
        (cb - gr * pg - om) / ee)


# ---------------------------------------------------------------- varianti
def test_demo_non_conviente():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] < 0.0
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_gas_trenta_degenere_per_risparmio():
    """Sensibilita' richiesta dal brief: gas 30 EUR/MWh.
    In questa tab il risparmio negativo e' degenere."""
    bc = _variante(prezzo_gas_eur_mwh=30)
    assert bc["valid"] is False
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"] == []
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["errore"]


def test_variante_prezzo_el_alto_non_conviente():
    bc = _variante(prezzo_el_eur_mwh=130)
    assert bc["risparmio_eur_anno"] == pytest.approx(558.9607843137201)
    assert bc["van"] == pytest.approx(-254198.17820207038)
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(137.60041414307483)
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_variante_prezzo_el_zero_non_conviente():
    bc = _variante(prezzo_el_eur_mwh=0.0)
    assert bc["c_alt_var_eur_anno"] == pytest.approx(5358.166666666668)
    assert bc["c_alt_eur_anno"] == pytest.approx(17358.166666666668)
    assert bc["risparmio_eur_anno"] == pytest.approx(10119.611111111106)
    assert bc["van"] == pytest.approx(-154961.89718729397)
    assert bc["tir"] == pytest.approx(-6.078835207050988, abs=1e-4)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_variante_gas_alto_conviente():
    bc = _variante(prezzo_gas_eur_mwh=150)
    assert bc["risparmio_eur_anno"] == pytest.approx(53642.25599128539)
    assert bc["van"] == pytest.approx(296788.27358608635)
    assert bc["tir"] == pytest.approx(19.139971980434833, abs=1e-4)
    assert bc["payback"] == 5
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_variante_gas_marginale():
    bc = _variante(prezzo_gas_eur_mwh=91.75)
    assert bc["risparmio_eur_anno"] == pytest.approx(25009.64827523601)
    assert bc["van"] == pytest.approx(-408.40324787724603)
    assert bc["van"] < 0.0
    assert abs(bc["van"]) <= 0.10 * 260000
    assert bc["tir"] == pytest.approx(4.976752233089254, abs=1e-4)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"
    assert bc["valid"] is True


def test_variante_quota_zero_degenere_per_risparmio():
    """Sensibilita' richiesta dal brief: quota PdC 0 %.
    La quota zero non e' degenere di per se', ma con
    la demo il risparmio che ne risulta e' negativo,
    quindi il caso e' degenere per la regola del
    risparmio (differenza rispetto alla tab
    precedente)."""
    bc = _variante(quota_pdc_pct=0)
    assert bc["valid"] is False
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"] == []
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["errore"]


def test_variante_quota_quaranta_calcolabile():
    bc = _variante(quota_pdc_pct=40)
    assert bc["valid"] is True
    assert bc["q_pdc_mwh_anno"] == pytest.approx(142.88444444444445)
    assert bc["e_el_mwh_anno"] == pytest.approx(42.02483660130719)
    assert bc["gas_res_mwh_anno"] == pytest.approx(238.1407407407407)
    assert bc["risparmio_eur_anno"] == pytest.approx(138.71241830065264)
    assert bc["van"] == pytest.approx(-258560.21253239017)
    assert bc["tir"] == pytest.approx(-35.128338662075244, abs=1e-4)
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(113.30072475038097)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_quota_ottanta_calcolabile():
    bc = _variante(quota_pdc_pct=80)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(2660.2026143790827)
    assert bc["van"] == pytest.approx(-232388.00655047115)
    assert bc["tir"] == pytest.approx(-17.582412815967185, abs=1e-4)
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(141.65036237519047)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_quota_recupero_cento_calcolabile_non_degenere():
    """Sensibilita' richiesta dal brief: recupero 100 %."""
    bc = _variante(quota_recupero_pct=100)
    assert bc["valid"] is True
    assert bc["q_netto_mwh_anno"] == 0.0
    assert bc["q_pdc_mwh_anno"] == 0.0
    assert bc["e_el_mwh_anno"] == 0.0
    assert bc["gas_res_mwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(15477.777777777774)
    assert bc["van"] == pytest.approx(-99345.959475716)
    assert bc["tir"] == pytest.approx(-1.3830525484841614, abs=1e-4)
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_quota_recupero_zero_degenere():
    bc = _variante(quota_recupero_pct=0)
    assert bc["valid"] is False
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_cop_alto_calcolabile():
    bc = _variante(cop=5.0)
    assert bc["e_el_mwh_anno"] == pytest.approx(50.00955555555555)
    assert bc["risparmio_eur_anno"] == pytest.approx(4618.559999999994)
    assert bc["van"] == pytest.approx(-212060.92657118075)
    assert bc["tir"] == pytest.approx(-13.279482493216676, abs=1e-4)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(202.35355021040414)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_cop_basso_degenere():
    bc = _variante(cop=2.0)
    assert bc["valid"] is False
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_co2_evitata_negativa_con_fattore_el_alto():
    bc = _variante(f_el_t_per_mwh=2.0)
    assert bc["co2_alt_t_anno"] == pytest.approx(170.90100217864924)
    assert bc["co2_evitata_t_anno"] == pytest.approx(-48.777545388525795)
    assert bc["co2_evitata_t_anno"] < 0.0
    assert bc["van"] == pytest.approx(-238931.05804595098)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_wacc_zero():
    bc = _variante(wacc_pct=0)
    assert bc["crf"] == pytest.approx(1.0 / 15.0)
    assert bc["quota_capex_eur_anno"] == pytest.approx(17333.333333333332)
    assert bc["van"] == pytest.approx(-229552.54901960783)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex_eur=0)
    assert bc["capex_eur"] == 0
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(21068.94195404906)
    assert bc["lco_alt_eur_t"] == pytest.approx(7.952483660130719)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_vita_dieci():
    bc = _variante(vita_anni=10)
    assert len(bc["flussi"]) == 11
    assert bc["crf"] == pytest.approx(0.12950457496545661)
    assert bc["van"] == pytest.approx(-244326.1902840043)
    assert bc["tir"] == pytest.approx(-30.96280447036618, abs=1e-4)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_fattori_zero_calcolabile():
    bc = _variante(f_gas_t_per_mwh=0, f_el_t_per_mwh=0)
    assert bc["valid"] is True
    assert bc["co2_base_t_anno"] == 0.0
    assert bc["co2_alt_t_anno"] == 0.0
    assert bc["co2_evitata_t_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(2029.8300653594706)


# ---------------------------------------------------------------- degenere
def test_degenere_pasta_zero():
    bc = _variante(m_pasta_t_anno=0)
    assert bc["valid"] is False
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"] == []
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["lco_base_eur_t"] is None
    assert bc["lco_alt_eur_t"] is None
    assert bc["errore"]


def test_degenere_umidita_delta_cop_vita():
    for kw in ({"u_i_pct": 12.5},
               {"u_i_pct": 5},
               {"u_f_pct": 100},
               {"t_ingresso_C": 55, "t_ess_C": 55},
               {"t_ingresso_C": 55, "t_ess_C": 25},
               {"cop": 0}, {"cop": -1},
               {"m_pasta_t_anno": 0},
               {"m_pasta_t_anno": -1},
               {"vita_anni": 0}, {"vita_anni": 2.5}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_eta_wacc_tolleranza_quote_prezzi_negativi():
    for kw in ({"eta_gas": 0}, {"eta_gas": 1.01},
               {"wacc_pct": -1}, {"wacc_pct": 60},
               {"tolleranza_pct": -1}, {"tolleranza_pct": 101},
               {"quota_recupero_pct": -1}, {"quota_recupero_pct": 101},
               {"quota_pdc_pct": -1}, {"quota_pdc_pct": 101},
               {"prezzo_gas_eur_mwh": -1},
               {"prezzo_el_eur_mwh": -1},
               {"om_fisso_eur_anno": -100},
               {"capex_eur": -1},
               {"u_i_pct": 0}, {"u_i_pct": 100},
               {"u_f_pct": -1},
               {"t_ingresso_C": -1}, {"t_ingresso_C": 100},
               {"t_ess_C": 0}, {"t_ess_C": 100.1}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_stringa_nan_inf():
    for kw in ({"m_pasta_t_anno": "4000"},
               {"m_pasta_t_anno": float("nan")},
               {"prezzo_el_eur_mwh": float("inf")},
               {"capex_eur": True}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_risparmio_zero_o_negativo():
    for kw in ({"prezzo_gas_eur_mwh": 30},
               {"prezzo_gas_eur_mwh": 0},
               {"quota_pdc_pct": 0},
               {"quota_recupero_pct": 0},
               {"cop": 2.0},
               {"prezzo_el_eur_mwh": 400}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"
        assert bc["flussi"] == []


def test_degenere_neutro_campi():
    bc = _variante(m_pasta_t_anno=0)
    assert bc["q_lordo_mwh_anno"] == 0.0
    assert bc["gas_base_mwh_anno"] == 0.0
    assert bc["c_base_eur_anno"] == 0.0
    assert bc["c_alt_eur_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == 0.0
    assert bc["van"] == 0.0
    assert list(bc["df_flussi"].columns) == [
        "Anno", "Flusso (EUR/anno)", "Cumulato (EUR)"]
    assert list(bc["df_tabella"].columns) == ["Voce", "Valore"]


def test_pareggio_none_quando_e_el_zero():
    assert mh763_prezzo_pareggio(27477.777777777774, 119.0703703703704,
                                 45, 12000, 0.0) is None
    assert mh763_prezzo_pareggio(27477.777777777774, 119.0703703703704,
                                 45, 12000, None) is None
    assert mh763_lco_base(27477.777777777774, 0) is None
    assert mh763_e_el(250.04777777777775, 0) is None
    bc = _variante(quota_recupero_pct=100)
    assert bc["prezzo_pareggio_eur_mwh"] is None


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = demo_calcoli()
    testo = mh763_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert "q_lordo_mwh_anno;549.5555555555555" in testo
    assert "q_netto_mwh_anno;357.2111111111111" in testo
    assert "verdetto;NON_CONVIENTE" in testo
    assert "prezzo_pareggio_eur_mwh" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = demo_calcoli()
    testo = mh763_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"quota_capex_eur_anno;{bc['quota_capex_eur_anno']}" in testo
    assert f"q_lordo_mwh_anno;{bc['q_lordo_mwh_anno']}" in testo


def test_csv_degenere_solo_zeri():
    bc = _variante(m_pasta_t_anno=0)
    testo = mh763_csv(bc, _demo_kwargs())
    assert "van_eur;0.0" in testo
    assert "q_lordo_mwh_anno;0.0" in testo
    assert "verdetto;NON_CALCOLABILE" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = demo_calcoli()
    testo = mh763_csv(bc, _demo_kwargs())
    for chiave in _demo_kwargs():
        assert f"{chiave};" in testo


def test_calcola_non_sollevela_per_input_numerici():
    bc = _variante(f_gas_t_per_mwh=0, f_el_t_per_mwh=0)
    assert bc["valid"] is True
    assert bc["co2_base_t_anno"] == 0.0
    assert bc["co2_alt_t_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(2029.8300653594706)


def test_monotonia_prezzo_el():
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(prezzo_el_eur_mwh=120)["risparmio_eur_anno"]
    basso = _variante(prezzo_el_eur_mwh=100)["risparmio_eur_anno"]
    assert basso > base > alto
    assert basso - base == pytest.approx(735.4346405228758)
    assert base - alto == pytest.approx(735.4346405228758)


def test_monotonia_quota_pdc():
    base = demo_calcoli()["risparmio_eur_anno"]
    alta = _variante(quota_pdc_pct=80)["risparmio_eur_anno"]
    bassa = _variante(quota_pdc_pct=40)["risparmio_eur_anno"]
    assert alta > base > bassa


def test_demo_deterministica_due_chiamate():
    a = demo_calcoli()
    b = demo_calcoli()
    assert a["van"] == b["van"]
    assert a["flussi"] == b["flussi"]
    assert a["tir"] == b["tir"]


def test_demo_chiavi_attese():
    assert set(mh763_demo().keys()) == {
        "m_pasta_t_anno", "u_i_pct",
        "u_f_pct", "t_ingresso_C", "t_ess_C",
        "eta_gas", "quota_recupero_pct",
        "quota_pdc_pct", "cop",
        "prezzo_gas_eur_mwh", "prezzo_el_eur_mwh",
        "om_fisso_eur_anno", "capex_eur",
        "f_gas_t_per_mwh", "f_el_t_per_mwh",
        "wacc_pct", "vita_anni", "tolleranza_pct"}


# ---------------------------------------------------------------- AST / regole dure
_HF_FALLBACK = os.path.expanduser("~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files")


def _leggi(nome):
    qui = os.path.dirname(os.path.abspath(__file__))
    p = os.path.join(qui, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    with open(p, encoding="utf-8") as f:
        return f.read()


def _vietati():
    # Token della tab precedente e dei file precedenti, costruiti
    # per concatenazione: questo stesso file non li contiene
    # come sottostringhe contigue.
    return ["mh" + "76" + "2", "st" + "76" + "2",
            "tab" + "76" + "2", "w" + "76" + "3_",
            "mh" + "76" + "1", "st" + "76" + "1",
            "tab" + "76" + "1", "w" + "76" + "2_"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w764_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w764_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab763:")


def test_registry_chain_tail_and_count():
    """Registry della nuova tab: il frammento UI apre la tab
    numero 763 (la coda della catena termina con la nuova tab
    e il conteggio atteso delle tab e' 763)."""
    src = _leggi("w764_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 763
    assert src.count("with tab763:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w764_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w764_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st763_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert "key=f" not in src and 'key = f' not in src
    assert "st.stop()" in src
    # guard degenere prima di KPI / grafico / tabella / CSV
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w764_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def763[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w764_ui.py")
        usate = set(re.findall(r'_def763\["([^"]+)"\]', src))
        assert usate
        assert usate <= set(mh763_demo().keys())


def test_ui_chiavi_demo_coerenti():
    """Ogni _def763[...] letto dalla UI esiste nel dict demo:
    sweep anti-KeyError a render (lezione dello sweep chiavi demo vs UI)."""
    src = _leggi("w764_ui.py")
    usate = set(re.findall(r'_def763\["([^"]+)"\]', src))
    assert usate
    assert usate <= set(mh763_demo().keys())


def test_ui_riferisce_solo_helper_nuovi():
    src = _leggi("w764_ui.py")
    usati = set(re.findall(r'\b(mh\d+_\w+)\b', src))
    assert usati
    assert all(u.startswith("mh763_") for u in usati)


@pytest.mark.parametrize("wacc,vita,atteso", [
    (5.0, 15, 0.09634228760924432),
    (0, 15, 1.0 / 15.0),
    (10.0, 10, 0.16274539488251152),
    (5.0, 1, 1.05),
    (50.0, 5, 0.5758293838862559),
])
def test_crf_parametrizzato(wacc, vita, atteso):
    assert mh763_crf(wacc, vita) == pytest.approx(atteso)


@pytest.mark.parametrize("campo,valore", [
    ("m_pasta_t_anno", 0), ("m_pasta_t_anno", -3),
    ("u_i_pct", 0), ("u_i_pct", 100),
    ("u_f_pct", -1), ("u_f_pct", 100),
    ("t_ingresso_C", -1), ("t_ingresso_C", 100),
    ("t_ess_C", 0), ("t_ess_C", 100.1),
    ("eta_gas", 0), ("eta_gas", 1.01),
    ("quota_recupero_pct", -1), ("quota_recupero_pct", 100.1),
    ("quota_pdc_pct", -1), ("quota_pdc_pct", 100.1),
    ("cop", 0), ("cop", -1),
    ("prezzo_gas_eur_mwh", -1),
    ("prezzo_el_eur_mwh", -1),
    ("om_fisso_eur_anno", -100),
    ("capex_eur", -1),
    ("f_gas_t_per_mwh", -0.10), ("f_el_t_per_mwh", -0.10),
    ("wacc_pct", -0.1), ("wacc_pct", 50.1),
    ("vita_anni", -1), ("vita_anni", 2.5),
    ("tolleranza_pct", -1), ("tolleranza_pct", 100.1),
])
def test_valida_rifiuta_singoli_campi(campo, valore):
    d = _demo_kwargs()
    d[campo] = valore
    assert mh763_valida(**d)["valido"] is False


def test_df_tabella_valori_demo_selezionati():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Pasta fresca (t/anno)"] == 4000.0
    assert mappa["Calore lordo (MWh/anno)"] == pytest.approx(549.5555555555555)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(2029.8300653594706)
    assert mappa["Verdetto"] == "NON_CONVIENTE"


def test_lco_alt_maggiore_di_lco_base_demo():
    bc = demo_calcoli()
    assert bc["lco_alt_eur_t"] > bc["lco_base_eur_t"]
    assert bc["lco_alt_eur_t"] - bc["lco_base_eur_t"] == pytest.approx(
        7.193488972826266)
