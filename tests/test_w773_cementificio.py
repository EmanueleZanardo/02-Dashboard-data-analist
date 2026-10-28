"""Test tab773 "Cementificio: recuperare
calore dai fumi del forno per
preriscaldare la farina batte il
combustibile comprato?"

Nuova tab tab773 (cementificio, file di
lavoro w774). Business case
deterministico di un cementificio:
produzione P t/anno di clinker;
calore utile Q_term = P x q_th / 3,6
MWh/anno (q_th in GJ/t: 1 MWh =
3,6 GJ, conversione esatta); consumo
elettrico E_base = P x e_spec / 1000
MWh/anno (e_spec in kWh/t, identico
nei due casi: il recupero non cambia
il consumo elettrico specifico);
combustibile baseline fuel_base =
Q_term / eta_forno MWh/anno (eta
come frazione); calore recuperato
Q_rec = quota_rec x Q_term MWh/anno
(quota come frazione, scambio
termico dai fumi per preriscaldare
la farina, senza combustibile in
piu'); combustibile alternativo
fuel_alt = (Q_term - Q_rec) /
eta_forno MWh/anno (sempre >= 0 per
costruzione se quota_rec <= 1);
costo base C_base = fuel_base x
p_fuel + E_base x p_el EUR/anno;
costo variabile alternativo
C_alt_var = fuel_alt x p_fuel +
E_base x p_el EUR/anno; costo
alternativo C_alt = C_alt_var + O&M
EUR/anno; risparmio = C_base -
C_alt = (fuel_base - fuel_alt) x
p_fuel - O&M EUR/anno; CO2 base =
fuel_base x f_fuel + E_base x f_el
t/anno; CO2 alt = fuel_alt x f_fuel
+ E_base x f_el t/anno; CO2 evitata
= CO2 base - CO2 alt = (fuel_base -
fuel_alt) x f_fuel t/anno, sempre
>= 0 per costruzione (fuel_alt <=
fuel_base, f_fuel >= 0, elettricita'
identica: il fattore elettrico NON
cambia la CO2 evitata), NON
monetizzata; fattore di emissione in
tCO2/MWh, numericamente uguale a
kg/kWh (1 kg/kWh = 1 t/MWh); CRF =
r (1 + r)^n / ((1 + r)^n - 1) con r
= WACC come frazione, r = 0 -> 1/n,
SOLO nel LCO, MAI nei flussi;
LCO base = C_base / P EUR/t; LCO
alt = (CAPEX x CRF + O&M) / P +
C_alt_var / P EUR/t (il CAPEX entra
solo annuizzato col CRF); prezzo
combustibile di pareggio p_fuel* =
O&M / (fuel_base - fuel_alt)
EUR/MWh (formula chiusa: il
risparmio e' lineare in p_fuel con
pendenza fuel_base - fuel_alt,
perche' l'elettricita' e' identica
nei due casi e si elide), None se il
denominatore <= 0 (quota_rec = 0:
nessun combustibile risparmiato),
e' un pavimento (sopra di esso
l'alternativa vince); flussi
[-CAPEX, risparmio x vita]; VAN,
TIR, payback (primo anno con
cumulato >= 0, regola >= del brief:
con CAPEX nullo il payback e' 0, con
divisione esatta CAPEX / risparmio
il payback e' l'anno della divisione
esatta). Verdetto: CONVIENTE se VAN
> 0, MARGINALE se VAN < 0 e |VAN| <=
tolleranza % del CAPEX, altrimenti
NON_CONVIENTE; NON_CALCOLABILE e'
il verdetto del caso degenere (VAN
None: nessun calcolo eseguibile,
quindi nessuna VAN, nessuna TIR e
nessun payback). Regime degenere
SOLLEVA ValueError negli helper
(produzione <= 0, consumo termico
specifico <= 0, rendimento forno
<= 0 o > 1, quota recupero fuori
[0, 100] %, consumo elettrico
specifico <= 0, prezzi < 0, O&M < 0,
CAPEX < 0, fattori < 0, WACC < 0 o
sopra 50 %, vita <= 0 o non intera,
tolleranza fuori [0, 100] %, input
non numerici o non finiti, quota
recupero sopra 100 % che darebbe un
calore utile residuo negativo); la
UI lo intercetta PRIMA di KPI,
grafico, tabella e CSV con st.stop().
In questa tab il risparmio nullo o
negativo NON e' degenere: resta
calcolabile e porta a VAN negativa
(NON_CONVIENTE o MARGINALE). La CO2
evitata NON puo' essere negativa in
questa tab: e' un'identita' >= 0,
non una guard. Distinzione esplicita:
questa tab fa clinker in un forno da
cemento (fumi -> preriscaldo della
farina), non calce, non ceramica,
non vetro.

Demo calcolata eseguendo
demo_calcoli() e ricontrollata con
un ricalcolo indipendente da zero
(riga per riga): produzione clinker
500.000 t/anno, consumo termico
specifico 3,6 GJ/t, rendimento forno
90 %, quota recupero 25 %, consumo
elettrico specifico 110 kWh/t, prezzo
combustibile 45 EUR/MWh, prezzo
elettricita' 180 EUR/MWh, O&M annuo
800.000 EUR/anno, CAPEX 12.000.000
EUR, fattore combustibile 0,30
tCO2/MWh, fattore elettricita' 0,25
tCO2/MWh, WACC 5 %, vita 20 anni,
tolleranza MARGINALE 10 % del CAPEX.

- q_term_mwh_anno = 500000.0
- e_base_mwh_anno = 55000.0
- fuel_base_mwh_anno = 555555.5555555555
- q_rec_mwh_anno = 125000.0
- fuel_alt_mwh_anno = 416666.6666666666
- c_base_eur_anno = 34900000.0
- c_alt_var_eur_anno = 28650000.0
- c_alt_eur_anno = 29450000.0
- co2_base_t_anno = 180416.66666666666
- co2_alt_t_anno = 138750.0
- risparmio_eur_anno = 5450000.0
- co2_evitata_t_anno = 41666.66666666666
- crf = 0.08024258719069129
- lco_base_eur_t = 69.8
- lco_alt_eur_t = 60.82582209257659
- van = 55919046.366842896
- tir = 45.39117169544289
- payback = 3
- prezzo_pareggio_eur_mwh = 5.760000000000001
- verdetto = 'CONVIENTE'

Scomposizione: calore utile =
500.000 x 3,6 / 3,6 = 500.000
MWh/anno; consumo elettrico =
500.000 x 110 / 1000 = 55.000
MWh/anno; combustibile baseline =
500.000 / 0,90 = 555.555,555556
MWh/anno; calore recuperato = 0,25
x 500.000 = 125.000 MWh/anno;
combustibile alternativo =
(500.000 - 125.000) / 0,90 =
416.666,666667 MWh/anno; costo base
= 555.555,555556 x 45 + 55.000 x 180
= 25.000.000 + 9.900.000 =
34.900.000 EUR/anno; costo variabile
alternativo = 416.666,666667 x 45 +
55.000 x 180 = 18.750.000 +
9.900.000 = 28.650.000 EUR/anno;
costo alternativo = 28.650.000 +
800.000 = 29.450.000 EUR/anno;
risparmio = 34.900.000 - 29.450.000
= 5.450.000 EUR/anno; CO2 base =
555.555,555556 x 0,30 + 55.000 x
0,25 = 166.666,666667 + 13.750 =
180.416,666667 t/anno; CO2 alt =
416.666,666667 x 0,30 + 55.000 x
0,25 = 125.000 + 13.750 = 138.750
t/anno; CO2 evitata = 180.416,666667
- 138.750 = 41.666,666667 t/anno;
CRF al 5 % per 20 anni =
0,0802425872; LCO base 34.900.000 /
500.000 = 69,80 EUR/t; LCO alt =
(12.000.000 x 0,0802425872 +
800.000) / 500.000 + 28.650.000 /
500.000 = 3,525822 + 57,30 = 60,825822
EUR/t; flussi: anno 0 -12.000.000,
anni 1-20 risparmio 5.450.000
(piatti); VAN -12.000.000 +
5.450.000 x 12,462210 (annuita' 20
anni al 5 %) = 55.919.046,37 EUR;
TIR 45,39 %; payback 3 anni (il
cumulato all'anno 2 e' -1.100.000
EUR, all'anno 3 e' 4.350.000 EUR,
gia' >= 0); prezzo combustibile di
pareggio 800.000 / (555.555,555556 -
416.666,666667) = 5,76 EUR/MWh
(pavimento: sopra di esso
l'alternativa vince, sotto perde);
verdetto CONVIENTE perche' VAN > 0.
NOTA: il CRF entra SOLO nel LCO di
questa tab: nei flussi il CAPEX
entra intero all'anno 0, mai
annuizzato.
NOTA 2: in questa tab il risparmio
nullo o negativo NON e' degenere:
con prezzo combustibile 5 EUR/MWh
(sotto il pareggio 5,76) il caso e'
calcolabile (valid=True, flussi
pieni), NON_CONVIENTE con VAN
-13.315.455,54 EUR e payback None,
non un errore.
NOTA 3: la CO2 evitata ha segno
sempre >= 0 in questa tab (non e'
una guard, e' un'identita'):
(555.555,555556 - 416.666,666667) x
0,30 = 41.666,666667 t/anno; con
fattore combustibile zero l'evitata
e' zero (55.000 = 55.000 t/anno nei
due casi, solo elettricita'), e il
fattore elettrico non la cambia mai
perche' l'elettricita' e' identica
nei due casi e si elide.
NOTA 4: il prezzo combustibile di
pareggio e' None con quota recupero
zero (denominatore nullo: nessun
combustibile risparmiato, nessun
pareggio su p_fuel). Al pareggio
esatto (5,76 EUR/MWh) il risparmio
e' zero: il caso resta calcolabile
con VAN -12.000.000 EUR (solo il
CAPEX, senza risparmi) e verdetto
NON_CONVIENTE.
NOTA 5: la quota di recupero scala
il risparmio in modo lineare: con
quota 50 % il calore recuperato e'
250.000 MWh/anno, il risparmio
11.700.000 EUR/anno, la VAN
133.807.861,01 EUR e il payback 2
anni; con quota 100 % il combustibile
alternativo va a zero, il risparmio
a 24.200.000 EUR/anno, la VAN a
289.585.490,29 EUR e il payback a 1
anno (ma il calore utile residuo
nullo e' un limite teorico: un forno
reale non lavora mai a combustibile
zero).
NOTA 6: il payback usa il cumulato
>= 0 (regola >= del brief): con
CAPEX nullo il payback e' 0 (non
1); con flussi [-100, 50, 50] il
payback e' 2 (il cumulato all'anno
2 e' zero, e zero basta).
NOTA 7: il verdetto MARGINALE
richiede VAN negativa entro la
tolleranza % del CAPEX: con CAPEX
70.000.000 EUR la VAN e'
-2.080.953,63 EUR, entro 7.000.000
EUR (10 % di 70.000.000), quindi
MARGINALE; con tolleranza 0 % lo
stesso caso e' NON_CONVIENTE.
NOTA 8: i valori demo sono stati
ricalcolati da zero con un calcolo
indipendente: il ricalcolo esatto
(senza arrotondamenti intermedi)
da' calore utile 500.000, elettrico
55.000, combustibile base
555.555,555556, recuperato 125.000,
combustibile alt 416.666,666667,
costo base 34.900.000, costo
variabile alt 28.650.000, costo alt
29.450.000, risparmio 5.450.000, CO2
base 180.416,666667, CO2 alt
138.750, evitata 41.666,666667, CRF
0,0802425872, LCO base 69,80, LCO
alt 60,825822, VAN 55.919.046,37,
TIR 45,39 %, payback 3 e pareggio
5,76: i file usano i valori esatti.
Le stime del brief (Q_term 500.000,
fuel_base 555.555,56, Q_rec 125.000,
fuel_alt 416.666,67, C_base
34.900.000, C_alt 29.450.000,
risparmio 5.450.000, CO2 base
180.416,67, alt 138.750, evitata
41.666,67, LCO base 69,80, LCO alt
60,83, pareggio 5,76, payback anno
3) sono tutte confermate dal
ricalcolo; VAN e TIR, non stimati
nel brief, sono calcolati
esattamente qui.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w774_helpers import (
    demo_calcoli,
    mh773_c_alt,
    mh773_c_alt_var,
    mh773_c_base,
    mh773_calcola,
    mh773_co2_alt,
    mh773_co2_base,
    mh773_co2_evitata,
    mh773_crf,
    mh773_csv,
    mh773_demo,
    mh773_e_base,
    mh773_flussi,
    mh773_fuel_alt,
    mh773_fuel_base,
    mh773_int_pos,
    mh773_lco_alt,
    mh773_lco_base,
    mh773_num,
    mh773_nneg,
    mh773_payback,
    mh773_pct_0_100,
    mh773_pct_0_100_escl0,
    mh773_pct_tolleranza,
    mh773_pct_wacc,
    mh773_pos,
    mh773_prezzo_pareggio,
    mh773_q_rec,
    mh773_q_term,
    mh773_risparmio,
    mh773_tir,
    mh773_valida,
    mh773_van,
    mh773_verdetto,
)

# Costanti demo a piena precisione (per la validazione
# _DEMO contro demo_calcoli() con tolleranza relativa
# < 1e-9: vedi test_demo_costanti_vs_demo_calcoli).
_DEMO = {
    "q_term_mwh_anno": 500000.0,
    "e_base_mwh_anno": 55000.0,
    "fuel_base_mwh_anno": 555555.5555555555,
    "q_rec_mwh_anno": 125000.0,
    "fuel_alt_mwh_anno": 416666.6666666666,
    "c_base_eur_anno": 34900000.0,
    "c_alt_var_eur_anno": 28650000.0,
    "c_alt_eur_anno": 29450000.0,
    "co2_base_t_anno": 180416.66666666666,
    "co2_alt_t_anno": 138750.0,
    "risparmio_eur_anno": 5450000.0,
    "co2_evitata_t_anno": 41666.66666666666,
    "crf": 0.08024258719069129,
    "lco_base_eur_t": 69.8,
    "lco_alt_eur_t": 60.82582209257659,
    "van": 55919046.366842896,
    "tir": 45.39117169544289,
    "prezzo_pareggio_eur_mwh": 5.760000000000001,
}


def _demo_kwargs():
    return dict(mh773_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh773_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh773_num(3, "x") == 3.0
    assert mh773_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh773_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh773_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh773_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh773_pos(0, "x")
    with pytest.raises(ValueError):
        mh773_pos(-1, "x")
    assert mh773_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh773_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh773_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh773_int_pos(0, "x")


def test_pct_wacc_limiti():
    assert mh773_pct_wacc(0, "x") == 0.0
    assert mh773_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh773_pct_wacc(50.1, "x")


def test_pct_0_100_escl0_limiti():
    assert mh773_pct_0_100_escl0(100, "x") == 100.0
    assert mh773_pct_0_100_escl0(65.0, "x") == 65.0
    with pytest.raises(ValueError):
        mh773_pct_0_100_escl0(0, "x")
    with pytest.raises(ValueError):
        mh773_pct_0_100_escl0(100.1, "x")
    with pytest.raises(ValueError):
        mh773_pct_0_100_escl0(-1, "x")


def test_pct_0_100_limiti():
    assert mh773_pct_0_100(0, "x") == 0.0
    assert mh773_pct_0_100(100, "x") == 100.0
    assert mh773_pct_0_100(50.0, "x") == 50.0
    with pytest.raises(ValueError):
        mh773_pct_0_100(-0.1, "x")
    with pytest.raises(ValueError):
        mh773_pct_0_100(100.1, "x")


def test_pct_tolleranza_limiti():
    assert mh773_pct_tolleranza(0, "x") == 0.0
    assert mh773_pct_tolleranza(100, "x") == 100.0
    assert mh773_pct_tolleranza(10.0, "x") == 10.0
    with pytest.raises(ValueError):
        mh773_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh773_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_q_term_e_e_base():
    assert mh773_q_term(500000, 3.6) == pytest.approx(500000.0)
    assert mh773_q_term(500000, 1.8) == pytest.approx(250000.0)
    assert mh773_e_base(500000, 110) == pytest.approx(55000.0)
    assert mh773_e_base(500000, 55) == pytest.approx(27500.0)
    with pytest.raises(ValueError):
        mh773_q_term(500000, 0)
    with pytest.raises(ValueError):
        mh773_q_term(0, 3.6)
    with pytest.raises(ValueError):
        mh773_e_base(500000, 0)
    with pytest.raises(ValueError):
        mh773_e_base(500000, -1)


def test_fuel_base_q_rec_fuel_alt():
    assert mh773_fuel_base(500000.0, 0.90) == pytest.approx(
        555555.5555555555)
    assert mh773_fuel_base(500000.0, 1.0) == pytest.approx(500000.0)
    assert mh773_q_rec(500000.0, 0.25) == pytest.approx(125000.0)
    assert mh773_q_rec(500000.0, 0.0) == 0.0
    assert mh773_q_rec(500000.0, 1.0) == pytest.approx(500000.0)
    assert mh773_fuel_alt(500000.0, 125000.0,
                          0.90) == pytest.approx(416666.6666666666)
    assert mh773_fuel_alt(500000.0, 500000.0,
                          0.90) == 0.0
    assert mh773_fuel_alt(500000.0, 0.0,
                          0.90) == pytest.approx(555555.5555555555)
    with pytest.raises(ValueError):
        mh773_q_rec(500000.0, 1.1)
    with pytest.raises(ValueError):
        mh773_q_rec(500000.0, -0.1)
    with pytest.raises(ValueError):
        mh773_fuel_alt(500000.0, 500001.0, 0.90)
    with pytest.raises(ValueError):
        mh773_fuel_base(500000.0, 0.0)
    with pytest.raises(ValueError):
        mh773_fuel_base(500000.0, 1.1)


def test_bilancio_energetico_demo_e_varianti():
    """Bilancio esatto: Q_rec + fuel_alt x eta_forno = Q_term,
    nel demo e nelle varianti (il calore utile si conserva:
    recuperato piu' residuo da combustibile)."""
    for bc in (demo_calcoli(),
               _variante(quota_rec_pct=0.0),
               _variante(quota_rec_pct=50.0),
               _variante(quota_rec_pct=100.0),
               _variante(eta_forno_pct=80.0)):
        eta = bc["eta_forno_pct"] / 100.0
        assert bc["q_rec_mwh_anno"] + \
            bc["fuel_alt_mwh_anno"] * eta == pytest.approx(
                bc["q_term_mwh_anno"], rel=1e-9)


def test_c_base_c_alt_var_c_alt():
    assert mh773_c_base(555555.5555555555, 55000.0, 45,
                        180) == pytest.approx(34900000.0)
    assert mh773_c_base(500000.0, 55000.0, 45,
                        180) == pytest.approx(32400000.0)
    assert mh773_c_alt_var(416666.6666666666, 55000.0, 45,
                           180) == pytest.approx(28650000.0)
    assert mh773_c_alt_var(0.0, 55000.0, 45,
                           180) == pytest.approx(9900000.0)
    assert mh773_c_alt(28650000.0, 800000) == pytest.approx(
        29450000.0)
    with pytest.raises(ValueError):
        mh773_c_base(555555.5555555555, 55000.0, -1, 180)
    with pytest.raises(ValueError):
        mh773_c_alt_var(416666.6666666666, 55000.0, 45, -1)
    with pytest.raises(ValueError):
        mh773_c_alt(28650000.0, -1)


def test_co2_base_alt_evitata():
    assert mh773_co2_base(555555.5555555555, 55000.0, 0.30,
                          0.25) == pytest.approx(180416.66666666666)
    assert mh773_co2_alt(416666.6666666666, 55000.0, 0.30,
                         0.25) == pytest.approx(138750.0)
    assert mh773_co2_alt(0.0, 55000.0, 0.30,
                         0.25) == pytest.approx(13750.0)
    assert mh773_co2_evitata(180416.66666666666,
                             138750.0) == pytest.approx(
        41666.66666666666)
    assert mh773_co2_evitata(100.0, 150.0) == pytest.approx(-50.0)
    with pytest.raises(ValueError):
        mh773_co2_base(555555.5555555555, 55000.0, -0.10, 0.25)


def test_co2_evitata_mai_negativa_via_calcola():
    """Identita' della tab: via mh773_calcola la CO2
    evitata e' sempre >= 0 (combustibile alt <= base,
    fattore >= 0, elettricita' identica)."""
    for bc in (demo_calcoli(),
               _variante(quota_rec_pct=0.0),
               _variante(quota_rec_pct=100.0),
               _variante(f_fuel_t_per_mwh=0.0),
               _variante(f_el_t_per_mwh=1.0),
               _variante(f_el_t_per_mwh=0.0)):
        assert bc["co2_evitata_t_anno"] >= 0.0
        assert bc["co2_evitata_t_anno"] == pytest.approx(
            (bc["fuel_base_mwh_anno"] - bc["fuel_alt_mwh_anno"])
            * bc["f_fuel_t_per_mwh"])


def test_co2_evitata_indipendente_da_fattore_elettrico():
    """Il fattore elettrico NON cambia la CO2 evitata:
    l'elettricita' e' identica nei due casi e si elide."""
    base = demo_calcoli()["co2_evitata_t_anno"]
    for fel in (0.0, 0.25, 1.0):
        assert _variante(f_el_t_per_mwh=fel)[
            "co2_evitata_t_anno"] == pytest.approx(base)


def test_risparmio_segno():
    assert mh773_risparmio(34900000.0, 29450000.0) == \
        pytest.approx(5450000.0)
    assert mh773_risparmio(34900000.0, 34900000.0) == 0.0
    assert mh773_risparmio(12783333.333333332, 12888888.88888889) == \
        pytest.approx(-105555.5555555541)


def test_crf_solo_lco():
    assert mh773_crf(5.0, 20) == pytest.approx(0.08024258719069129)
    assert mh773_crf(0.0, 20) == pytest.approx(0.05)
    assert mh773_crf(5.0, 10) == pytest.approx(0.1295045749654566)
    with pytest.raises(ValueError):
        mh773_crf(50.1, 20)
    with pytest.raises(ValueError):
        mh773_crf(5.0, 0)


def test_lco():
    assert mh773_lco_base(34900000.0, 500000) == pytest.approx(69.8)
    assert mh773_lco_alt(12000000, 0.08024258719069129, 800000,
                         28650000.0, 500000) == pytest.approx(
        60.82582209257659)
    assert mh773_lco_base(34900000.0, 0) is None
    assert mh773_lco_alt(12000000, 0.08024258719069129, 800000,
                         28650000.0, 0) is None
    assert mh773_lco_alt(12000000, 0.08024258719069129, 800000,
                         28650000.0, -5) is None
    # Il CAPEX entra nel LCO solo annuizzato: con CAPEX nullo
    # il LCO alt e' (O&M + C_alt_var) / P = C_alt / P.
    assert mh773_lco_alt(0, 0.08024258719069129, 800000,
                         28650000.0, 500000) == pytest.approx(58.9)


def test_prezzo_pareggio_formula_zero_e_pavimento():
    assert mh773_prezzo_pareggio(
        800000, 555555.5555555555,
        416666.6666666666) == pytest.approx(5.760000000000001)
    assert mh773_prezzo_pareggio(
        800000, 555555.5555555555,
        555555.5555555555) is None
    assert mh773_prezzo_pareggio(
        2000000, 555555.5555555555,
        416666.6666666666) == pytest.approx(14.4)
    with pytest.raises(ValueError):
        mh773_prezzo_pareggio(-1, 555555.5555555555,
                              416666.6666666666)


def test_prezzo_pareggio_verifica_pareggio():
    """Al prezzo di pareggio il risparmio si azzera:
    C_alt(p*) = C_base(p*)."""
    bc = demo_calcoli()
    par = bc["prezzo_pareggio_eur_mwh"]
    d = _demo_kwargs()
    d["prezzo_fuel_eur_mwh"] = par
    bc_par = mh773_calcola(**d)
    assert bc_par["risparmio_eur_anno"] == pytest.approx(
        0.0, abs=1e-6)
    assert bc_par["c_alt_eur_anno"] == pytest.approx(
        bc_par["c_base_eur_anno"], rel=1e-9)


def test_prezzo_pareggio_none_quota_zero():
    """Caso None del brief: quota recupero zero ->
    nessun combustibile risparmiato -> denominatore
    nullo -> pareggio None."""
    bc = _variante(quota_rec_pct=0)
    assert bc["q_rec_mwh_anno"] == 0.0
    assert bc["fuel_alt_mwh_anno"] == pytest.approx(
        bc["fuel_base_mwh_anno"])
    assert bc["prezzo_pareggio_eur_mwh"] is None


def test_pareggio_pavimento_non_tetto():
    """Sopra il pareggio l'alternativa vince, sotto
    perde: il pareggio e' un pavimento (il risparmio
    cresce con p_fuel, pendenza fuel_base - fuel_alt
    > 0)."""
    par = demo_calcoli()["prezzo_pareggio_eur_mwh"]
    assert _variante(prezzo_fuel_eur_mwh=par + 10)[
        "risparmio_eur_anno"] > 0.0
    assert _variante(prezzo_fuel_eur_mwh=par - 1)[
        "risparmio_eur_anno"] < 0.0


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh773_flussi(12000000, 5450000.0, 20)
    assert len(fl) == 21
    assert fl[0] == -12000000
    assert all(f == 5450000.0 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = demo_calcoli()
    assert bc["van"] == pytest.approx(55919046.366842896)
    assert mh773_van([-12000000] + [5450000.0] * 20,
                     0) == pytest.approx(97000000.0)
    assert mh773_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = demo_calcoli()
    assert bc["tir"] == pytest.approx(45.39117169544289)
    assert mh773_tir([-12000000] + [5450000.0] * 20) == \
        pytest.approx(0.4539117169544289)
    tir = mh773_tir([-12000000] + [5450000.0] * 20)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate(
                  [-12000000] + [5450000.0] * 20))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    """Payback con cumulato >= 0: il cumulato nullo basta."""
    assert mh773_payback([-12000000] + [5450000.0] * 20) == 3
    assert mh773_payback([-12000000] + [-1000.0] * 20) is None
    assert mh773_payback([0] + [5450000.0] * 20) == 0
    assert mh773_payback([-100] + [50] * 2) == 2
    assert mh773_payback([-10900000.0] +
                         [5450000.0] * 2) == 2


def test_verdetto():
    assert mh773_verdetto(100.0, 12000000, 10.0) == "CONVIENTE"
    assert mh773_verdetto(0.0, 12000000, 10.0) == "NON_CONVIENTE"
    assert mh773_verdetto(-2080953.6331571029, 70000000,
                          10.0) == "MARGINALE"
    assert mh773_verdetto(-2080953.6331571029, 70000000,
                          0.0) == "NON_CONVIENTE"
    assert mh773_verdetto(-13315455.53615698, 12000000,
                          10.0) == "NON_CONVIENTE"
    assert mh773_verdetto(-100.0, 0, 10.0) == "NON_CONVIENTE"
    assert mh773_verdetto(None, 12000000, 10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh773_verdetto(float("nan"), 12000000, 10.0)
    with pytest.raises(ValueError):
        mh773_verdetto(100.0, -1, 10.0)
    with pytest.raises(ValueError):
        mh773_verdetto(100.0, 12000000, 100.1)


def test_valida_demo_ok():
    v = mh773_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("p_t_anno", "500000"),
                       ("p_t_anno", float("nan")),
                       ("p_t_anno", float("inf")),
                       ("p_t_anno", True),
                       ("prezzo_fuel_eur_mwh", None),
                       ("eta_forno_pct", "90")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh773_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("p_t_anno", 0),
                          ("p_t_anno", -1),
                          ("q_th_gj_per_t", 0),
                          ("q_th_gj_per_t", -1),
                          ("eta_forno_pct", 0),
                          ("eta_forno_pct", 100.1),
                          ("quota_rec_pct", -1),
                          ("quota_rec_pct", 100.1),
                          ("e_spec_kwh_per_t", 0),
                          ("e_spec_kwh_per_t", -1),
                          ("prezzo_fuel_eur_mwh", -1),
                          ("prezzo_el_eur_mwh", -1),
                          ("om_eur_anno", -100),
                          ("capex_eur", -1),
                          ("f_fuel_t_per_mwh", -0.10),
                          ("f_el_t_per_mwh", -0.10),
                          ("wacc_pct", -0.1), ("wacc_pct", 50.1),
                          ("vita_anni", 0), ("vita_anni", 2.5),
                          ("tolleranza_pct", -1),
                          ("tolleranza_pct", 100.1)):
        d = _demo_kwargs()
        d[campo] = valore
        assert mh773_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"quota_rec_pct": 0,
              "eta_forno_pct": 100,
              "prezzo_fuel_eur_mwh": 0,
              "prezzo_el_eur_mwh": 0,
              "f_fuel_t_per_mwh": 0,
              "f_el_t_per_mwh": 0,
              "om_eur_anno": 0,
              "capex_eur": 0, "wacc_pct": 0,
              "tolleranza_pct": 0})
    assert mh773_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    assert mh773_valida(**d)["valido"] is True


def test_valida_non_controlla_risparmio_calcola_neppure():
    """La validazione input NON controlla il risparmio
    (e' un esito, non un range) e in questa tab
    nemmeno mh773_calcola lo controlla: con prezzo
    combustibile 5 EUR/MWh (sotto il pareggio 5,76)
    il caso resta CALCOLABILE."""
    d = _demo_kwargs()
    d["prezzo_fuel_eur_mwh"] = 5
    assert mh773_valida(**d)["valido"] is True
    bc = _variante(prezzo_fuel_eur_mwh=5)
    assert bc["valid"] is True
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["flussi"]
    assert bc["payback"] is None


def test_demo_dict():
    d = mh773_demo()
    assert d["p_t_anno"] == 500000
    assert d["q_th_gj_per_t"] == 3.6
    assert d["eta_forno_pct"] == 90.0
    assert d["quota_rec_pct"] == 25.0
    assert d["e_spec_kwh_per_t"] == 110
    assert d["prezzo_fuel_eur_mwh"] == 45
    assert d["prezzo_el_eur_mwh"] == 180
    assert d["om_eur_anno"] == 800000
    assert d["capex_eur"] == 12000000
    assert d["f_fuel_t_per_mwh"] == 0.30
    assert d["f_el_t_per_mwh"] == 0.25
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 20
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    """Tutti gli output numerici demo a tolleranza
    1e-9 relativa (richiesta del brief): confronto
    delle costanti _DEMO contro demo_calcoli()."""
    bc = demo_calcoli()
    for chiave, atteso in _DEMO.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert got == pytest.approx(atteso, rel=1e-9), chiave
    assert bc["payback"] == 3
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_demo_calcoli_fisica():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["q_term_mwh_anno"] == pytest.approx(500000.0)
    assert bc["e_base_mwh_anno"] == pytest.approx(55000.0)
    assert bc["fuel_base_mwh_anno"] == pytest.approx(555555.5555555555)
    assert bc["q_rec_mwh_anno"] == pytest.approx(125000.0)
    assert bc["fuel_alt_mwh_anno"] == pytest.approx(416666.6666666666)
    assert bc["co2_evitata_t_anno"] == pytest.approx(41666.66666666666)


def test_demo_calcoli_economia():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(34900000.0)
    assert bc["c_alt_var_eur_anno"] == pytest.approx(28650000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(29450000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(5450000.0)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(
        5.760000000000001)


def test_demo_calcoli_finanza():
    bc = demo_calcoli()
    assert bc["crf"] == pytest.approx(0.08024258719069129)
    assert bc["lco_base_eur_t"] == pytest.approx(69.8)
    assert bc["lco_alt_eur_t"] == pytest.approx(60.82582209257659)
    assert bc["van"] == pytest.approx(55919046.366842896)
    assert bc["tir"] == pytest.approx(45.39117169544289)
    assert bc["payback"] == 3
    assert bc["verdetto"] == "CONVIENTE"


def test_demo_flussi_e_cumulato():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -12000000
    assert len(bc["flussi"]) == 21
    assert all(f == pytest.approx(5450000.0)
               for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -12000000
    assert righe.iloc[2]["Cumulato (EUR)"] == pytest.approx(-1100000.0)
    assert righe.iloc[3]["Cumulato (EUR)"] == pytest.approx(4350000.0)
    assert righe.iloc[20]["Cumulato (EUR)"] == pytest.approx(97000000.0)
    assert righe.iloc[20]["Flusso (EUR/anno)"] == pytest.approx(
        5450000.0)


def test_demo_tabella_righe():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Produzione clinker (t/anno)"] == pytest.approx(
        500000.0)
    assert mappa["Calore utile (MWh/anno)"] == pytest.approx(500000.0)
    assert mappa["Consumo elettrico (MWh/anno)"] == pytest.approx(
        55000.0)
    assert mappa["Calore recuperato (MWh/anno)"] == pytest.approx(
        125000.0)
    assert mappa["Combustibile alternativo (MWh/anno)"] == pytest.approx(
        416666.6666666666)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(
        29450000.0)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(5450000.0)
    assert mappa["Payback (anni)"] == 3
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Prezzo combustibile di pareggio (EUR/MWh)"] == \
        pytest.approx(5.760000000000001)


def test_demo_coerenza_interna():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["q_rec_mwh_anno"] + \
        bc["fuel_alt_mwh_anno"] * bc["eta_forno_pct"] / 100.0 == \
        pytest.approx(bc["q_term_mwh_anno"])
    assert bc["q_rec_mwh_anno"] == pytest.approx(
        bc["q_term_mwh_anno"] * bc["quota_rec_pct"] / 100.0)
    assert bc["fuel_base_mwh_anno"] == pytest.approx(
        bc["q_term_mwh_anno"] / (bc["eta_forno_pct"] / 100.0))
    assert bc["e_base_mwh_anno"] == pytest.approx(
        bc["p_t_anno"] * bc["e_spec_kwh_per_t"] / 1000.0)
    assert bc["q_term_mwh_anno"] == pytest.approx(
        bc["p_t_anno"] * bc["q_th_gj_per_t"] / 3.6)
    assert bc["co2_base_t_anno"] - bc["co2_alt_t_anno"] == \
        pytest.approx(bc["co2_evitata_t_anno"])
    assert bc["c_base_eur_anno"] / bc["p_t_anno"] == \
        pytest.approx(bc["lco_base_eur_t"])
    assert (bc["capex_eur"] * bc["crf"] + bc["om_eur_anno"]) / \
        bc["p_t_anno"] + bc["c_alt_var_eur_anno"] / bc["p_t_anno"] == \
        pytest.approx(bc["lco_alt_eur_t"])


def test_demo_contro_riconteggio_indipendente():
    p, qsp, efor = 500000, 3.6, 90.0
    qrec, esp = 25.0, 110
    pf, pel, om, cx = 45, 180, 800000, 12000000
    ff, fel, wacc, vita = 0.30, 0.25, 5.0, 20
    qt = p * qsp / 3.6
    eb = p * esp / 1000.0
    fb = qt / (efor / 100.0)
    qr = (qrec / 100.0) * qt
    fa = (qt - qr) / (efor / 100.0)
    cb = fb * pf + eb * pel
    cav = fa * pf + eb * pel
    ca = cav + om
    risp = cb - ca
    co2b = fb * ff + eb * fel
    co2a = fa * ff + eb * fel
    r = wacc / 100.0
    crf = r * (1 + r) ** vita / ((1 + r) ** vita - 1.0)
    lco_b = cb / p
    lco_a = (cx * crf + om) / p + cav / p
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    par = om / (fb - fa)
    bc = demo_calcoli()
    assert bc["q_term_mwh_anno"] == pytest.approx(qt)
    assert bc["e_base_mwh_anno"] == pytest.approx(eb)
    assert bc["fuel_base_mwh_anno"] == pytest.approx(fb)
    assert bc["q_rec_mwh_anno"] == pytest.approx(qr)
    assert bc["fuel_alt_mwh_anno"] == pytest.approx(fa)
    assert bc["c_base_eur_anno"] == pytest.approx(cb)
    assert bc["c_alt_var_eur_anno"] == pytest.approx(cav)
    assert bc["c_alt_eur_anno"] == pytest.approx(ca)
    assert bc["risparmio_eur_anno"] == pytest.approx(risp)
    assert bc["co2_base_t_anno"] == pytest.approx(co2b)
    assert bc["co2_alt_t_anno"] == pytest.approx(co2a)
    assert bc["crf"] == pytest.approx(crf)
    assert bc["lco_base_eur_t"] == pytest.approx(lco_b)
    assert bc["lco_alt_eur_t"] == pytest.approx(lco_a)
    assert bc["van"] == pytest.approx(van)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(par)


# ---------------------------------------------------------------- varianti
def test_demo_conviente():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] > 0.0
    assert bc["payback"] == 3
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_recupero_cinquanta():
    """Recupero al 50 % sul demo: Q_rec 250.000,
    fuel_alt 277.777,78, risparmio 11.700.000,
    VAN 133.807.861,01, payback 2."""
    bc = _variante(quota_rec_pct=50.0)
    assert bc["valid"] is True
    assert bc["q_rec_mwh_anno"] == pytest.approx(250000.0)
    assert bc["fuel_alt_mwh_anno"] == pytest.approx(277777.77777777775)
    assert bc["c_alt_eur_anno"] == pytest.approx(23200000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(11700000.0)
    assert bc["van"] == pytest.approx(133807861.00771777)
    assert bc["tir"] == pytest.approx(97.49988041744763)
    assert bc["payback"] == 2
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(
        2.8800000000000003)
    assert bc["lco_alt_eur_t"] == pytest.approx(48.32582209257659)
    assert bc["co2_evitata_t_anno"] == pytest.approx(83333.33333333333)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_recupero_cento():
    """Recupero al 100 % sul demo: fuel_alt zero
    (limite teorico), risparmio 24.200.000, VAN
    289.585.490,29, payback 1."""
    bc = _variante(quota_rec_pct=100.0)
    assert bc["valid"] is True
    assert bc["q_rec_mwh_anno"] == pytest.approx(500000.0)
    assert bc["fuel_alt_mwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(24200000.0)
    assert bc["van"] == pytest.approx(289585490.2894676)
    assert bc["payback"] == 1
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(
        1.4400000000000002)
    assert bc["lco_alt_eur_t"] == pytest.approx(23.32582209257659)
    assert bc["co2_evitata_t_anno"] == pytest.approx(166666.66666666666)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_recupero_zero():
    """Quota recupero zero: nessun risparmio di
    combustibile, solo O&M in piu': risparmio
    -800.000, VAN -21.969.768,27, pareggio None,
    payback None."""
    bc = _variante(quota_rec_pct=0)
    assert bc["valid"] is True
    assert bc["q_rec_mwh_anno"] == 0.0
    assert bc["fuel_alt_mwh_anno"] == pytest.approx(
        bc["fuel_base_mwh_anno"])
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["risparmio_eur_anno"] == pytest.approx(-800000.0)
    assert bc["van"] == pytest.approx(-21969768.27403198)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_marginale_capex_alto():
    """Fascia MARGINALE: CAPEX 70.000.000 EUR, VAN
    negativa entro la tolleranza del 10 % del
    CAPEX (7.000.000 EUR)."""
    bc = _variante(capex_eur=70000000)
    assert bc["valid"] is True
    assert bc["van"] == pytest.approx(-2080953.6331571029)
    assert bc["tir"] == pytest.approx(4.646800823855468)
    assert bc["payback"] == 13
    assert bc["verdetto"] == "MARGINALE"
    bc0 = _variante(capex_eur=70000000, tolleranza_pct=0)
    assert bc0["verdetto"] == "NON_CONVIENTE"
    assert bc0["van"] == pytest.approx(-2080953.6331571029)


def test_variante_non_conviente_prezzo_fuel_basso():
    """NON_CONVIENTE: prezzo combustibile 5 EUR/MWh,
    sotto il pareggio 5,76: risparmio negativo,
    VAN negativa oltre la tolleranza, payback mai,
    TIR None (flussi tutti negativi dopo l'anno 0)."""
    bc = _variante(prezzo_fuel_eur_mwh=5)
    assert bc["valid"] is True
    assert bc["c_base_eur_anno"] == pytest.approx(12677777.777777778)
    assert bc["c_alt_eur_anno"] == pytest.approx(12783333.333333332)
    assert bc["risparmio_eur_anno"] == pytest.approx(-105555.5555555541)
    assert bc["van"] == pytest.approx(-13315455.53615698)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["flussi"]


def test_variante_non_conviente_prezzo_fuel_alto_no():
    """Controllo opposto: prezzo combustibile 30
    EUR/MWh (sopra il pareggio) resta CONVIENTE,
    con risparmio 3.366.666,67 e payback 4."""
    bc = _variante(prezzo_fuel_eur_mwh=30)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(3366666.666666664)
    assert bc["van"] == pytest.approx(29956108.15321791)
    assert bc["tir"] == pytest.approx(27.849473589390584)
    assert bc["payback"] == 4
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_rendimento_basso():
    """Rendimento forno 80 %: piu' combustibile in
    ingresso in entrambi i casi, ma piu' combustibile
    risparmiato in assoluto: risparmio 6.231.250,
    VAN 65.655.148,20, payback 2, pareggio 5,12."""
    bc = _variante(eta_forno_pct=80.0)
    assert bc["valid"] is True
    assert bc["fuel_base_mwh_anno"] == pytest.approx(625000.0)
    assert bc["fuel_alt_mwh_anno"] == pytest.approx(468750.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(6231250.0)
    assert bc["van"] == pytest.approx(65655148.19695227)
    assert bc["payback"] == 2
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(5.12)
    assert bc["co2_evitata_t_anno"] == pytest.approx(46875.0)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(97000000.0)
    assert bc["lco_alt_eur_t"] == pytest.approx(60.099999999999994)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    """Payback regola >=: con CAPEX nullo il payback e' 0,
    non 1 (all'anno 0 il cumulato e' gia' zero)."""
    bc = _variante(capex_eur=0)
    assert bc["capex_eur"] == 0
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(67919046.36684291)
    assert bc["lco_alt_eur_t"] == pytest.approx(58.9)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_vita_diversa():
    bc = _variante(vita_anni=10)
    assert len(bc["flussi"]) == 11
    assert bc["van"] == pytest.approx(30083455.364057217)
    assert bc["tir"] == pytest.approx(44.252597355532366)
    assert bc["payback"] == 3
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_pareggio_esatto_risparmio_zero():
    """Al pareggio esatto il risparmio e' zero: il caso
    resta calcolabile con VAN -12.000.000 EUR (solo il
    CAPEX, senza risparmi) e verdetto NON_CONVIENTE."""
    bc = _variante(prezzo_fuel_eur_mwh=5.76)
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["van"] == pytest.approx(-12000000.0)
    assert bc["verdetto"] == "NON_CONVIENTE"


# ---------------------------------------------------------------- degenere
def test_degenere_produzione_zero_sollevela():
    """Caso degenere richiesto dal brief: P = 0
    solleva ValueError."""
    with pytest.raises(ValueError):
        _variante(p_t_anno=0)


def test_degenere_verdetto_non_calcolabile_van_tir_payback_none():
    """Nel regime degenere non esiste alcun calcolo:
    calcola solleva ValueError, quindi nessuna VAN,
    nessuna TIR e nessun payback vengono prodotti
    (sono None per assenza); il verdetto per VAN
    None e' NON_CALCOLABILE."""
    with pytest.raises(ValueError):
        _variante(p_t_anno=0)
    with pytest.raises(ValueError):
        _variante(q_th_gj_per_t=0)
    with pytest.raises(ValueError):
        _variante(eta_forno_pct=0)
    assert mh773_verdetto(None, 12000000, 10.0) == "NON_CALCOLABILE"
    assert demo_calcoli()["verdetto"] != "NON_CALCOLABILE"


def test_degenere_guard_rendimento_quota_nulli():
    """Guard su rendimento e quota: rendimento forno
    zero o sopra 100, quota recupero fuori [0, 100]
    sollevano ValueError."""
    for kw in ({"eta_forno_pct": 0},
               {"eta_forno_pct": 100.1},
               {"quota_rec_pct": -1},
               {"quota_rec_pct": 100.1}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh773_valida(**d)["valido"] is False


def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"p_t_anno": 0}, {"p_t_anno": -1},
               {"q_th_gj_per_t": 0},
               {"q_th_gj_per_t": -1},
               {"eta_forno_pct": 0},
               {"eta_forno_pct": 100.1},
               {"quota_rec_pct": -1},
               {"quota_rec_pct": 100.1},
               {"e_spec_kwh_per_t": 0},
               {"e_spec_kwh_per_t": -1},
               {"prezzo_fuel_eur_mwh": -1},
               {"prezzo_el_eur_mwh": -1},
               {"om_eur_anno": -100},
               {"capex_eur": -1},
               {"f_fuel_t_per_mwh": -0.10},
               {"f_el_t_per_mwh": -0.10},
               {"wacc_pct": -1}, {"wacc_pct": 60},
               {"vita_anni": 0}, {"vita_anni": 2.5},
               {"tolleranza_pct": -1},
               {"tolleranza_pct": 100.1}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh773_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"p_t_anno": "500000"},
               {"p_t_anno": float("nan")},
               {"prezzo_fuel_eur_mwh": float("inf")},
               {"capex_eur": True},
               {"eta_forno_pct": "90"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh773_valida(**d)["valido"] is False


def test_risparmio_negativo_non_degenere():
    """Differenza chiave: risparmio nullo o
    negativo resta calcolabile, con flussi pieni e
    VAN negativa."""
    for kw in ({"prezzo_fuel_eur_mwh": 5},
               {"quota_rec_pct": 0}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["verdetto"] in ("NON_CONVIENTE", "MARGINALE")
        assert bc["flussi"]


def test_co2_evitata_segno_funzione_pura():
    assert mh773_co2_evitata(100.0, 150.0) == pytest.approx(-50.0)


def test_verdetto_non_calcolabile_solo_van_none():
    assert mh773_verdetto(None, 12000000, 10.0) == "NON_CALCOLABILE"
    assert demo_calcoli()["verdetto"] != "NON_CALCOLABILE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = demo_calcoli()
    testo = mh773_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert "q_term_mwh_anno;500000.0" in testo
    assert "e_base_mwh_anno;55000.0" in testo
    assert "fuel_base_mwh_anno;555555.5555555555" in testo
    assert "q_rec_mwh_anno;125000.0" in testo
    assert "fuel_alt_mwh_anno;416666.6666666666" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "prezzo_pareggio_eur_mwh" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = demo_calcoli()
    testo = mh773_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"q_rec_mwh_anno;{bc['q_rec_mwh_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = demo_calcoli()
    testo = mh773_csv(bc, _demo_kwargs())
    for chiave in _demo_kwargs():
        assert f"{chiave};" in testo


def test_monotonia_prezzo_fuel():
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(prezzo_fuel_eur_mwh=55)["risparmio_eur_anno"]
    basso = _variante(prezzo_fuel_eur_mwh=35)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(1388888.8888888888)
    assert base - basso == pytest.approx(1388888.8888888888)


def test_monotonia_prezzo_el():
    # L'elettricita' e' identica nei due casi: il prezzo
    # elettrico NON cambia il risparmio (si elide).
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(prezzo_el_eur_mwh=190)["risparmio_eur_anno"]
    basso = _variante(prezzo_el_eur_mwh=170)["risparmio_eur_anno"]
    assert alto == pytest.approx(base)
    assert basso == pytest.approx(base)


def test_monotonia_quota_rec():
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(quota_rec_pct=35)["risparmio_eur_anno"]
    basso = _variante(quota_rec_pct=15)["risparmio_eur_anno"]
    assert alto > base > basso


def test_demo_deterministica_due_chiamate():
    a = demo_calcoli()
    b = demo_calcoli()
    assert a["van"] == b["van"]
    assert a["flussi"] == b["flussi"]
    assert a["tir"] == b["tir"]


def test_demo_chiavi_attese():
    assert set(mh773_demo().keys()) == {
        "p_t_anno",
        "q_th_gj_per_t", "eta_forno_pct",
        "quota_rec_pct", "e_spec_kwh_per_t",
        "prezzo_fuel_eur_mwh", "prezzo_el_eur_mwh",
        "om_eur_anno", "capex_eur",
        "f_fuel_t_per_mwh", "f_el_t_per_mwh",
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
    # Token della tab precedente, costruiti
    # per concatenazione: questo stesso file non li contiene
    # come sottostringhe contigue.
    return ["mh" + "77" + "2", "st" + "77" + "2",
            "tab" + "77" + "2"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w774_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w774_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab773:")


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w774_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w774_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st773_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert "key=f" not in src and 'key = f' not in src
    assert "st.stop()" in src
    # guard degenere prima di KPI / grafico / tabella / CSV
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w774_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def773[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w774_ui.py")
        usate = set(re.findall(r'_def773\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 14
        assert usate == {
            "p_t_anno",
            "q_th_gj_per_t", "eta_forno_pct",
            "quota_rec_pct", "e_spec_kwh_per_t",
            "prezzo_fuel_eur_mwh", "prezzo_el_eur_mwh",
            "om_eur_anno", "capex_eur",
            "f_fuel_t_per_mwh", "f_el_t_per_mwh",
            "wacc_pct", "vita_anni", "tolleranza_pct"}
        assert usate <= set(mh773_demo().keys())


def test_ui_chiavi_demo_coerenti():
    """Ogni _def773[...] letto dalla UI esiste nel dict demo:
    sweep anti-KeyError a render (lezione dello sweep chiavi demo vs UI)."""
    src = _leggi("w774_ui.py")
    usate = set(re.findall(r'_def773\["([^"]+)"\]', src))
    assert usate
    assert len(usate) == 14
    assert usate <= set(mh773_demo().keys())


def test_ui_riferisce_solo_helper_nuovi():
    src = _leggi("w774_ui.py")
    usati = set(re.findall(r'\b(mh\d+_\w+)\b', src))
    assert usati
    assert all(u.startswith("mh773_") for u in usati)


@pytest.mark.parametrize("e_spec,atteso", [
    (110, 55000.0),
    (55, 27500.0),
    (220, 110000.0),
])
def test_e_base_parametrizzato(e_spec, atteso):
    assert mh773_e_base(500000, e_spec) == pytest.approx(atteso)


@pytest.mark.parametrize("campo,valore", [
    ("p_t_anno", 0), ("p_t_anno", -3),
    ("q_th_gj_per_t", 0), ("q_th_gj_per_t", -1),
    ("eta_forno_pct", 0), ("eta_forno_pct", 100.1),
    ("quota_rec_pct", -1), ("quota_rec_pct", 100.1),
    ("e_spec_kwh_per_t", 0), ("e_spec_kwh_per_t", -1),
    ("prezzo_fuel_eur_mwh", -1),
    ("prezzo_el_eur_mwh", -1),
    ("om_eur_anno", -100),
    ("capex_eur", -1),
    ("f_fuel_t_per_mwh", -0.10),
    ("f_el_t_per_mwh", -0.10),
    ("wacc_pct", -0.1), ("wacc_pct", 50.1),
    ("vita_anni", -1), ("vita_anni", 2.5),
    ("tolleranza_pct", -1), ("tolleranza_pct", 100.1),
])
def test_valida_rifiuta_singoli_campi(campo, valore):
    d = _demo_kwargs()
    d[campo] = valore
    assert mh773_valida(**d)["valido"] is False


@pytest.mark.parametrize("campo,valore", [
    ("p_t_anno", 0), ("p_t_anno", -3),
    ("q_th_gj_per_t", 0), ("q_th_gj_per_t", -1),
    ("eta_forno_pct", 0), ("eta_forno_pct", 100.1),
    ("quota_rec_pct", -1), ("quota_rec_pct", 100.1),
    ("e_spec_kwh_per_t", 0), ("e_spec_kwh_per_t", -1),
    ("prezzo_fuel_eur_mwh", -1),
    ("prezzo_el_eur_mwh", -1),
    ("om_eur_anno", -100),
    ("capex_eur", -1),
    ("f_fuel_t_per_mwh", -0.10),
    ("f_el_t_per_mwh", -0.10),
    ("wacc_pct", -0.1), ("wacc_pct", 50.1),
    ("vita_anni", -1), ("vita_anni", 2.5),
    ("tolleranza_pct", -1), ("tolleranza_pct", 100.1),
])
def test_calcola_sollevela_singoli_campi(campo, valore):
    d = _demo_kwargs()
    d[campo] = valore
    with pytest.raises(ValueError):
        mh773_calcola(**d)


def test_df_tabella_valori_demo_selezionati():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Produzione clinker (t/anno)"] == 500000.0
    assert mappa["Calore utile (MWh/anno)"] == pytest.approx(500000.0)
