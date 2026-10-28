"""Test tab776 "Cartotecnica: la
cogenerazione (CHP) batte caldaia +
rete per un cartotecnico?"
(File repo: tests/test_w776_cartotecnica.py,
contenuto pronto da scrivere in repo.)

Nuova tab tab776 (cartotecnica, file di
lavoro w777). Business case
deterministico di un cartotecnico:
produzione P t/anno di cartone;
calore utile Q_term = P x q_th /
3,6 MWh/anno (q_th in GJ/t: 1 MWh
= 3,6 GJ, conversione esatta);
domanda elettrica E_base = P x
e_spec / 1000 MWh/anno (e_spec in
kWh/t); combustibile baseline
fuel_base = Q_term / eta_boiler
MWh/anno (eta come frazione);
combustibile CHP F_chp = Q_term /
eta_th_chp MWh/anno (guida termica:
il CHP brucia quanto serve per
produrre esattamente Q_term);
elettricita' cogenerata E_chp =
F_chp x eta_el_chp MWh/anno (eta
elettrica come frazione, zero
ammesso: CHP solo termico); deficit
comprato bought = max(E_base -
E_chp, 0) MWh/anno; eccedenza
venduta surplus = max(E_chp -
E_base, 0) MWh/anno (bought e
surplus mai entrambi positivi:
regime comprato oppure regime
venduto); costo base C_base =
fuel_base x p_fuel + E_base x p_el
EUR/anno; costo variabile alternativo
C_alt_var = F_chp x p_fuel +
bought x p_el - surplus x p_sell
EUR/anno (ricavo di cessione con
segno meno); costo alternativo
C_alt = C_alt_var + O&M EUR/anno;
risparmio = C_base - C_alt EUR/anno;
CO2 base = fuel_base x f_fuel +
E_base x f_el t/anno; CO2 alt =
F_chp x f_fuel + bought x f_el -
surplus x f_el t/anno (eccedenza
spiazza rete al fattore elettrico);
CO2 evitata = CO2 base - CO2 alt
t/anno, PUO' ESSERE NEGATIVA in
questa tab (il CHP brucia piu'
combustibile della caldaia e
l'extra-CO2 puo' superare la CO2
elettrica spiazzata): NON e' una
guard, NON e' un degenere, NON
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
combustibile di pareggio regime-aware:
risparmio lineare in p_fuel con
pendenza (fuel_base - F_chp), uguale
nei due regimi, termine noto =
beneficio elettrico (regime comprato:
E_chp x p_el; regime venduto:
E_base x p_el + surplus x p_sell);
posto D = F_chp - fuel_base,
p_fuel* = (beneficio - O&M) / D
EUR/MWh, None se D <= 0
(convenzione di questa tab) e None
se beneficio - O&M < 0; quando
esiste e' un TETTO (ceiling), non un
pavimento: sotto di esso il CHP
vince, sopra perde, perche' il
risparmio cala con p_fuel (il CHP
brucia piu' combustibile della
caldaia); flussi [-CAPEX, risparmio
x vita]; VAN, TIR, payback (primo
anno con cumulato >= 0, regola >=
del brief: con CAPEX nullo il
payback e' 0, con divisione esatta
CAPEX / risparmio il payback e'
l'anno della divisione esatta).
Verdetto: CONVIENTE se VAN > 0,
MARGINALE se VAN < 0 e |VAN| <=
tolleranza % del CAPEX, altrimenti
NON_CONVIENTE; NON_CALCOLABILE e'
il verdetto del caso degenere (VAN
None: nessun calcolo eseguibile,
quindi nessuna VAN, nessuna TIR e
nessun payback). Regime degenere
SOLLEVA ValueError negli helper
(produzione <= 0, consumo termico
specifico <= 0, rendimento caldaia
<= 0 o > 1, rendimento termico CHP
<= 0 o > 1, rendimento elettrico CHP
< 0 o > 1, somma termico + elettrico
> 1, consumo elettrico specifico < 0,
prezzi < 0, O&M < 0, CAPEX < 0,
fattori < 0, WACC < 0 o sopra 50 %,
vita <= 0 o non intera, tolleranza
fuori [0, 100] %, input non numerici
o non finiti); la UI lo intercetta
PRIMA di KPI, grafico, tabella e CSV
con st.stop(). In questa tab il
risparmio nullo o negativo NON e'
degenere: resta calcolabile e porta
a VAN negativa (NON_CONVIENTE o
MARGINALE). La CO2 evitata PUO'
essere negativa in questa tab: e'
un esito onesto, non una guard.
Distinzione esplicita: questa tab fa
cartone in un cartotecnico con
cogeneratore a guida termica, non
carta in cartiera, non scatole
stampate a freddo, non plastica.

Demo calcolata eseguendo
demo_calcoli() e ricontrollata con
un ricalcolo indipendente da zero
(riga per riga): produzione cartone
40.000 t/anno, consumo termico
specifico 3,6 GJ/t, rendimento
caldaia 90 %, rendimento termico
CHP 50 %, rendimento elettrico CHP
35 %, consumo elettrico specifico
250 kWh/t, prezzo combustibile 45
EUR/MWh, prezzo elettricita' 180
EUR/MWh, prezzo cessione 90 EUR/MWh,
O&M annuo 300.000 EUR/anno, CAPEX
4.000.000 EUR, fattore combustibile
0,20 tCO2/MWh, fattore elettricita'
0,40 tCO2/MWh, WACC 5 %, vita 15
anni, tolleranza MARGINALE 10 % del
CAPEX.

- q_term_mwh_anno = 40000.0
- e_base_mwh_anno = 10000.0
- fuel_base_mwh_anno = 44444.444444444445
- fuel_chp_mwh_anno = 80000.0
- e_chp_mwh_anno = 28000.0
- bought_mwh_anno = 0.0
- surplus_mwh_anno = 18000.0
- c_base_eur_anno = 3800000.0
- c_alt_var_eur_anno = 1980000.0
- c_alt_eur_anno = 2280000.0
- co2_base_t_anno = 12888.888888888889
- co2_alt_t_anno = 8800.0
- risparmio_eur_anno = 1520000.0
- co2_evitata_t_anno = 4088.8888888888887
- crf = 0.09634228760924432
- lco_base_eur_t = 95.0
- lco_alt_eur_t = 66.63422876092443
- van = 11777080.218034498
- tir = 37.68636869512414
- payback = 3
- prezzo_pareggio_eur_mwh = 87.75
- verdetto = 'CONVIENTE'

Scomposizione: calore utile =
40.000 x 3,6 / 3,6 = 40.000
MWh/anno; domanda elettrica =
40.000 x 250 / 1000 = 10.000
MWh/anno; combustibile baseline =
40.000 / 0,90 = 44.444,444444
MWh/anno; combustibile CHP =
40.000 / 0,50 = 80.000 MWh/anno
(guida termica); elettricita'
cogenerata = 80.000 x 0,35 =
28.000 MWh/anno; regime venduto:
deficit comprato max(10.000 -
28.000, 0) = 0, eccedenza venduta
max(28.000 - 10.000, 0) = 18.000
MWh/anno; costo base =
44.444,444444 x 45 + 10.000 x 180
= 2.000.000 + 1.800.000 =
3.800.000 EUR/anno; costo variabile
alternativo = 80.000 x 45 + 0 x 180
- 18.000 x 90 = 3.600.000 -
1.620.000 = 1.980.000 EUR/anno;
costo alternativo = 1.980.000 +
300.000 = 2.280.000 EUR/anno;
risparmio = 3.800.000 - 2.280.000
= 1.520.000 EUR/anno; CO2 base =
44.444,444444 x 0,20 + 10.000 x
0,40 = 8.888,89 + 4.000 =
12.888,89 t/anno; CO2 alt =
80.000 x 0,20 + 0 x 0,40 -
18.000 x 0,40 = 16.000 - 7.200 =
8.800 t/anno; CO2 evitata =
12.888,89 - 8.800 = 4.088,89
t/anno; CRF al 5 % per 15 anni =
0,0963422876; LCO base 3.800.000 /
40.000 = 95,00 EUR/t; LCO alt =
(4.000.000 x 0,0963422876 +
300.000) / 40.000 + 1.980.000 /
40.000 = 17,134229 + 49,50 =
66,634229 EUR/t; flussi: anno 0
-4.000.000, anni 1-15 risparmio
1.520.000 (piatti); VAN -4.000.000
+ 1.520.000 x 10,379658 (annuita'
15 anni al 5 %) = 11.777.080,22
EUR; TIR 37,69 %; payback 3 anni
(il cumulato all'anno 2 e'
-960.000 EUR, all'anno 3 e'
560.000 EUR, gia' >= 0); prezzo
combustibile di pareggio (beneficio
elettrico 10.000 x 180 + 18.000 x
90 = 3.420.000 meno O&M 300.000 =
3.120.000) / (80.000 - 44.444,444444
= 35.555,555556) = 87,75 EUR/MWh
(TETTO: sotto di esso il CHP vince,
sopra perde); verdetto CONVIENTE
perche' VAN > 0.
NOTA: il CRF entra SOLO nel LCO di
questa tab: nei flussi il CAPEX
entra intero all'anno 0, mai
annuizzato.
NOTA 2: in questa tab il risparmio
nullo o negativo NON e' degenere:
con prezzo combustibile 100 EUR/MWh
(sopra il tetto 87,75) il caso e'
calcolabile (valid=True, flussi
pieni), NON_CONVIENTE con VAN
-8.520.917,72 EUR e payback None,
non un errore.
NOTA 3: la CO2 evitata PUO' essere
negativa in questa tab (non e' una
guard): con fattore elettrico 0,10
la CO2 base e' 9.888,89 t/anno e
l'alternativa 14.200 t/anno, quindi
l'evitata e' -4.311,11 t/anno, mentre
il verdetto resta CONVIENTE (stessa
economia: il fattore elettrico non
tocca i costi). Con rendimento
elettrico CHP zero l'evitata e'
-7.111,11 t/anno (solo extra
combustibile, nessuno spiazzamento).
NOTA 4: il prezzo combustibile di
pareggio e' un TETTO, non un
pavimento, e il verso e' il punto
centrale di questa tab: con prezzo
combustibile 100 EUR/MWh (sopra il
tetto) il risparmio e' -435.555,56
EUR/anno; al pareggio esatto
(87,75 EUR/MWh) il risparmio e'
zero e la VAN -4.000.000 EUR (solo
il CAPEX, senza risparmi). E' None
con rendimento termico CHP 95 % e
elettrico 5 % (F_chp 42.105,26 <
fuel_base 44.444,44: D negativo,
convenzione della tab) e None con
rendimento elettrico zero (beneficio
elettrico nullo, O&M non coperto).
NOTA 5: il regime cambia il numeratore
del pareggio ma non la sua natura di
tetto: con consumo elettrico specifico
800 kWh/t (regime comprato: domanda
32.000, cogenerata 28.000, deficit
4.000, surplus zero) il risparmio e'
3.140.000 EUR/anno, la VAN
28.592.126,24 EUR, il payback 2 anni
e il pareggio 133,31 EUR/MWh
(beneficio 28.000 x 180 = 5.040.000
meno O&M 300.000 = 4.740.000 diviso
35.555,56), sempre un tetto.
NOTA 6: il payback usa il cumulato
>= 0 (regola >= del brief): con
CAPEX nullo il payback e' 0 (non
1); con flussi [-100, 50, 50] il
payback e' 2 (il cumulato all'anno
2 e' zero, e zero basta).
NOTA 7: il verdetto MARGINALE
richiede VAN negativa entro la
tolleranza % del CAPEX: con CAPEX
17.000.000 EUR la VAN e'
-1.222.919,78 EUR, entro 1.700.000
EUR (10 % di 17.000.000), quindi
MARGINALE; con tolleranza 0 % lo
stesso caso e' NON_CONVIENTE.
NOTA 8: i valori demo sono stati
ricalcolati da zero con un calcolo
indipendente: il ricalcolo esatto
(senza arrotondamenti intermedi)
da' calore utile 40.000,
elettrico 10.000, combustibile base
44.444,444444, combustibile CHP
80.000, cogenerata 28.000, deficit
zero, surplus 18.000, costo base
3.800.000, costo variabile alt
1.980.000, costo alt 2.280.000,
risparmio 1.520.000, CO2 base
12.888,89, alt 8.800, evitata
4.088,89, CRF 0,0963422876, LCO base
95,00, LCO alt 66,634229, VAN
11.777.080,22, TIR 37,69 %, payback
3 e pareggio 87,75 (tetto): i file
usano i valori esatti.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w777_helpers import (
    demo_calcoli,
    mh776_bought,
    mh776_c_alt,
    mh776_c_alt_var,
    mh776_c_base,
    mh776_calcola,
    mh776_co2_alt,
    mh776_co2_base,
    mh776_co2_evitata,
    mh776_crf,
    mh776_csv,
    mh776_demo,
    mh776_e_base,
    mh776_e_chp,
    mh776_flussi,
    mh776_fuel_base,
    mh776_fuel_chp,
    mh776_int_pos,
    mh776_lco_alt,
    mh776_lco_base,
    mh776_num,
    mh776_nneg,
    mh776_payback,
    mh776_pct_0_100,
    mh776_pct_0_100_escl0,
    mh776_pct_tolleranza,
    mh776_pct_wacc,
    mh776_pos,
    mh776_prezzo_pareggio,
    mh776_q_term,
    mh776_risparmio,
    mh776_surplus,
    mh776_tir,
    mh776_valida,
    mh776_van,
    mh776_verdetto,
)

# Costanti demo a piena precisione (per la validazione
# _DEMO contro demo_calcoli() con tolleranza relativa
# < 1e-9: vedi test_demo_costanti_vs_demo_calcoli).
_DEMO = {
    "q_term_mwh_anno": 40000.0,
    "e_base_mwh_anno": 10000.0,
    "fuel_base_mwh_anno": 44444.444444444445,
    "fuel_chp_mwh_anno": 80000.0,
    "e_chp_mwh_anno": 28000.0,
    "bought_mwh_anno": 0.0,
    "surplus_mwh_anno": 18000.0,
    "c_base_eur_anno": 3800000.0,
    "c_alt_var_eur_anno": 1980000.0,
    "c_alt_eur_anno": 2280000.0,
    "co2_base_t_anno": 12888.888888888889,
    "co2_alt_t_anno": 8800.0,
    "risparmio_eur_anno": 1520000.0,
    "co2_evitata_t_anno": 4088.8888888888887,
    "crf": 0.09634228760924432,
    "lco_base_eur_t": 95.0,
    "lco_alt_eur_t": 66.63422876092443,
    "van": 11777080.218034498,
    "tir": 37.68636869512414,
    "prezzo_pareggio_eur_mwh": 87.75,
}


def _demo_kwargs():
    return dict(mh776_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh776_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh776_num(3, "x") == 3.0
    assert mh776_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh776_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh776_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh776_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh776_pos(0, "x")
    with pytest.raises(ValueError):
        mh776_pos(-1, "x")
    assert mh776_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh776_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh776_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh776_int_pos(0, "x")


def test_pct_wacc_limiti():
    assert mh776_pct_wacc(0, "x") == 0.0
    assert mh776_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh776_pct_wacc(50.1, "x")


def test_pct_0_100_escl0_limiti():
    assert mh776_pct_0_100_escl0(100, "x") == 100.0
    assert mh776_pct_0_100_escl0(65.0, "x") == 65.0
    with pytest.raises(ValueError):
        mh776_pct_0_100_escl0(0, "x")
    with pytest.raises(ValueError):
        mh776_pct_0_100_escl0(100.1, "x")
    with pytest.raises(ValueError):
        mh776_pct_0_100_escl0(-1, "x")


def test_pct_0_100_limiti():
    assert mh776_pct_0_100(0, "x") == 0.0
    assert mh776_pct_0_100(100, "x") == 100.0
    assert mh776_pct_0_100(50.0, "x") == 50.0
    with pytest.raises(ValueError):
        mh776_pct_0_100(-0.1, "x")
    with pytest.raises(ValueError):
        mh776_pct_0_100(100.1, "x")


def test_pct_tolleranza_limiti():
    assert mh776_pct_tolleranza(0, "x") == 0.0
    assert mh776_pct_tolleranza(100, "x") == 100.0
    assert mh776_pct_tolleranza(10.0, "x") == 10.0
    with pytest.raises(ValueError):
        mh776_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh776_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_q_term_e_e_base():
    assert mh776_q_term(40000, 3.6) == pytest.approx(40000.0)
    assert mh776_q_term(40000, 1.8) == pytest.approx(20000.0)
    assert mh776_e_base(40000, 250) == pytest.approx(10000.0)
    assert mh776_e_base(40000, 800) == pytest.approx(32000.0)
    assert mh776_e_base(40000, 0) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh776_q_term(40000, 0)
    with pytest.raises(ValueError):
        mh776_q_term(0, 3.6)
    with pytest.raises(ValueError):
        mh776_e_base(40000, -1)


def test_fuel_base_fuel_chp_e_chp():
    assert mh776_fuel_base(40000.0, 0.90) == pytest.approx(
        44444.444444444445)
    assert mh776_fuel_base(40000.0, 1.0) == pytest.approx(40000.0)
    assert mh776_fuel_chp(40000.0, 0.50) == pytest.approx(80000.0)
    assert mh776_fuel_chp(40000.0, 1.0) == pytest.approx(40000.0)
    assert mh776_e_chp(80000.0, 0.35) == pytest.approx(28000.0)
    assert mh776_e_chp(80000.0, 0.0) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh776_fuel_base(40000.0, 0.0)
    with pytest.raises(ValueError):
        mh776_fuel_base(40000.0, 1.1)
    with pytest.raises(ValueError):
        mh776_fuel_chp(40000.0, 0.0)
    with pytest.raises(ValueError):
        mh776_e_chp(80000.0, -0.1)
    with pytest.raises(ValueError):
        mh776_e_chp(80000.0, 1.1)


def test_bought_surplus_regimi_mutuamente_esclusivi():
    assert mh776_bought(10000.0, 28000.0) == 0.0
    assert mh776_surplus(10000.0, 28000.0) == pytest.approx(18000.0)
    assert mh776_bought(32000.0, 28000.0) == pytest.approx(4000.0)
    assert mh776_surplus(32000.0, 28000.0) == 0.0
    assert mh776_bought(28000.0, 28000.0) == 0.0
    assert mh776_surplus(28000.0, 28000.0) == 0.0
    assert mh776_bought(0.0, 28000.0) == 0.0
    assert mh776_surplus(0.0, 28000.0) == pytest.approx(28000.0)
    for eb, eg in ((10000.0, 28000.0), (32000.0, 28000.0),
                   (28000.0, 28000.0), (0.0, 28000.0)):
        assert mh776_bought(eb, eg) * mh776_surplus(eb, eg) == 0.0


def test_bilancio_energetico_demo_e_varianti():
    """Bilancio esatto: F_chp x eta_th_chp = Q_term e
    F_chp x eta_el_chp = E_chp, nel demo e nelle
    varianti (guida termica: il calore utile e'
    fissato, l'elettricita' e' il coprodotto)."""
    for bc in (demo_calcoli(),
               _variante(e_spec_kwh_per_t=800),
               _variante(e_spec_kwh_per_t=0),
               _variante(eta_el_chp_pct=0.0),
               _variante(eta_th_chp_pct=70.0, eta_el_chp_pct=10.0)):
        assert bc["fuel_chp_mwh_anno"] * \
            bc["eta_th_chp_pct"] / 100.0 == pytest.approx(
                bc["q_term_mwh_anno"], rel=1e-9)
        assert bc["fuel_chp_mwh_anno"] * \
            bc["eta_el_chp_pct"] / 100.0 == pytest.approx(
                bc["e_chp_mwh_anno"], rel=1e-9)
        assert bc["e_base_mwh_anno"] - bc["bought_mwh_anno"] + \
            bc["surplus_mwh_anno"] == pytest.approx(
                bc["e_chp_mwh_anno"], rel=1e-9)


def test_c_base_c_alt_var_c_alt():
    assert mh776_c_base(44444.444444444445, 10000.0, 45,
                        180) == pytest.approx(3800000.0)
    assert mh776_c_alt_var(80000.0, 0.0, 18000.0, 45, 180,
                           90) == pytest.approx(1980000.0)
    assert mh776_c_alt_var(80000.0, 4000.0, 0.0, 45, 180,
                           90) == pytest.approx(4320000.0)
    assert mh776_c_alt(1980000.0, 300000) == pytest.approx(2280000.0)
    with pytest.raises(ValueError):
        mh776_c_base(44444.444444444445, 10000.0, -1, 180)
    with pytest.raises(ValueError):
        mh776_c_alt_var(80000.0, 0.0, 18000.0, 45, 180, -1)
    with pytest.raises(ValueError):
        mh776_c_alt(1980000.0, -1)


def test_co2_base_alt_evitata():
    assert mh776_co2_base(44444.444444444445, 10000.0, 0.20,
                          0.40) == pytest.approx(12888.888888888889)
    assert mh776_co2_alt(80000.0, 0.0, 18000.0, 0.20,
                         0.40) == pytest.approx(8800.0)
    assert mh776_co2_alt(80000.0, 4000.0, 0.0, 0.20,
                         0.40) == pytest.approx(17600.0)
    assert mh776_co2_evitata(12888.888888888889,
                             8800.0) == pytest.approx(4088.8888888888887)
    assert mh776_co2_evitata(100.0, 150.0) == pytest.approx(-50.0)
    with pytest.raises(ValueError):
        mh776_co2_base(44444.444444444445, 10000.0, -0.10, 0.40)


def test_co2_evitata_puo_essere_negativa_via_calcola():
    """Differenza chiave di questa tab: via
    mh776_calcola la CO2 evitata PUO' essere
    negativa (fattore elettrico basso, o
    rendimento elettrico nullo)."""
    bc = _variante(f_el_t_per_mwh=0.10)
    assert bc["co2_base_t_anno"] == pytest.approx(9888.888888888889)
    assert bc["co2_alt_t_anno"] == pytest.approx(14200.0)
    assert bc["co2_evitata_t_anno"] == pytest.approx(-4311.111111111111)
    assert bc["verdetto"] == "CONVIENTE"
    bc0 = _variante(eta_el_chp_pct=0.0)
    assert bc0["co2_evitata_t_anno"] == pytest.approx(-7111.111111111111)
    assert bc0["valid"] is True


def test_co2_evitata_formula_spiazzamento():
    """CO2 evitata = (fuel_base - F_chp) x f_fuel +
    (E_base - bought + surplus) x f_el: il termine
    elettrico e' E_chp x f_el in entrambi i regimi
    (domanda evitata + surplus venduto)."""
    for bc in (demo_calcoli(),
               _variante(e_spec_kwh_per_t=800),
               _variante(f_el_t_per_mwh=0.10)):
        atteso = (bc["fuel_base_mwh_anno"]
                  - bc["fuel_chp_mwh_anno"]) * bc["f_fuel_t_per_mwh"] \
            + bc["e_chp_mwh_anno"] * bc["f_el_t_per_mwh"]
        assert bc["co2_evitata_t_anno"] == pytest.approx(atteso)


def test_risparmio_segno():
    assert mh776_risparmio(3800000.0, 2280000.0) == \
        pytest.approx(1520000.0)
    assert mh776_risparmio(3800000.0, 3800000.0) == 0.0
    assert mh776_risparmio(3800000.0, 4235555.555555555) == \
        pytest.approx(-435555.555555555)


def test_crf_solo_lco():
    assert mh776_crf(5.0, 15) == pytest.approx(0.09634228760924432)
    assert mh776_crf(0.0, 15) == pytest.approx(1.0 / 15.0)
    assert mh776_crf(5.0, 10) == pytest.approx(0.1295045749654566)
    with pytest.raises(ValueError):
        mh776_crf(50.1, 15)
    with pytest.raises(ValueError):
        mh776_crf(5.0, 0)


def test_lco():
    assert mh776_lco_base(3800000.0, 40000) == pytest.approx(95.0)
    assert mh776_lco_alt(4000000, 0.09634228760924432, 300000,
                         1980000.0, 40000) == pytest.approx(
        66.63422876092443)
    assert mh776_lco_base(3800000.0, 0) is None
    assert mh776_lco_alt(4000000, 0.09634228760924432, 300000,
                         1980000.0, 0) is None
    assert mh776_lco_alt(4000000, 0.09634228760924432, 300000,
                         1980000.0, -5) is None
    # Il CAPEX entra nel LCO solo annuizzato: con CAPEX nullo
    # il LCO alt e' (O&M + C_alt_var) / P = C_alt / P.
    assert mh776_lco_alt(0, 0.09634228760924432, 300000,
                         1980000.0, 40000) == pytest.approx(57.0)


def test_crf_mai_nei_flussi():
    """Il CRF entra SOLO nel LCO: i flussi usano il
    CAPEX intero all'anno 0 e la VAN dai flussi non
    dipende dal CRF (cambiando il WACC cambia la VAN
    per lo sconto, non per il CRF)."""
    bc = demo_calcoli()
    assert bc["flussi"][0] == -4000000
    assert bc["flussi"][1:] == [1520000.0] * 15
    assert bc["van"] == pytest.approx(mh776_van(bc["flussi"], 5.0))
    bc0 = _variante(wacc_pct=0)
    assert bc0["van"] == pytest.approx(sum(bc0["flussi"]))
    assert bc0["crf"] == pytest.approx(1.0 / 15.0)
    assert bc0["lco_alt_eur_t"] == pytest.approx(63.666666666666664)


def test_prezzo_pareggio_regime_venduto_e_comprato():
    # Demo, regime venduto: beneficio 10000x180 + 18000x90
    # = 3420000; (3420000 - 300000) / (80000 - 44444,44) = 87,75.
    assert mh776_prezzo_pareggio(
        300000, 44444.444444444445, 80000.0, 10000.0, 28000.0,
        180, 90) == pytest.approx(87.75)
    # Regime comprato: beneficio 28000x180 = 5040000;
    # (5040000 - 300000) / 35555,56 = 133,3125.
    assert mh776_prezzo_pareggio(
        300000, 44444.444444444445, 80000.0, 32000.0, 28000.0,
        180, 90) == pytest.approx(133.3125)
    # Regime comprato con cessione irrilevante: cambiare
    # p_sell non cambia il pareggio (non si vende nulla).
    assert mh776_prezzo_pareggio(
        300000, 44444.444444444445, 80000.0, 32000.0, 28000.0,
        180, 0) == pytest.approx(133.3125)
    with pytest.raises(ValueError):
        mh776_prezzo_pareggio(
            -1, 44444.444444444445, 80000.0, 10000.0, 28000.0,
            180, 90)


def test_prezzo_pareggio_none_casi():
    # D <= 0: F_chp 42105,26 < fuel_base 44444,44
    # (termico 95 %, elettrico 5 %): convenzione None.
    assert mh776_prezzo_pareggio(
        300000, 44444.444444444445, 42105.26315789474, 10000.0,
        2105.263157894737, 180, 90) is None
    # D = 0: F_chp = fuel_base: None.
    assert mh776_prezzo_pareggio(
        300000, 44444.444444444445, 44444.444444444445, 10000.0,
        15555.555555555555, 180, 90) is None
    # Beneficio - O&M < 0: elettrico zero, beneficio
    # nullo, O&M 300000: a prezzo combustibile zero il
    # risparmio e' gia' negativo e cala ancora: None.
    assert mh776_prezzo_pareggio(
        300000, 44444.444444444445, 80000.0, 10000.0, 0.0,
        180, 90) is None
    # Beneficio - O&M = 0: pareggio zero, valido.
    assert mh776_prezzo_pareggio(
        300000, 44444.444444444445, 80000.0, 10000.0, 28000.0,
        180, 90) is not None


def test_prezzo_pareggio_verifica_pareggio():
    """Al prezzo di pareggio il risparmio si azzera:
    C_alt(p*) = C_base(p*), in entrambi i regimi."""
    for kw in ({}, {"e_spec_kwh_per_t": 800}):
        bc = _variante(**kw)
        par = bc["prezzo_pareggio_eur_mwh"]
        d = _demo_kwargs()
        d.update(kw)
        d["prezzo_fuel_eur_mwh"] = par
        bc_par = mh776_calcola(**d)
        assert bc_par["risparmio_eur_anno"] == pytest.approx(
            0.0, abs=1e-6)
        assert bc_par["c_alt_eur_anno"] == pytest.approx(
            bc_par["c_base_eur_anno"], rel=1e-9)


def test_pareggio_tetto_non_pavimento():
    """Sotto il tetto il CHP vince, sopra perde: il
    risparmio CALA con p_fuel (pendenza negativa),
    il verso opposto al pavimento delle tab di
    risparmio di combustibile."""
    par = demo_calcoli()["prezzo_pareggio_eur_mwh"]
    assert _variante(prezzo_fuel_eur_mwh=par - 10)[
        "risparmio_eur_anno"] > 0.0
    assert _variante(prezzo_fuel_eur_mwh=par + 10)[
        "risparmio_eur_anno"] < 0.0
    par_b = _variante(e_spec_kwh_per_t=800)[
        "prezzo_pareggio_eur_mwh"]
    assert _variante(e_spec_kwh_per_t=800,
                     prezzo_fuel_eur_mwh=par_b - 10)[
        "risparmio_eur_anno"] > 0.0
    assert _variante(e_spec_kwh_per_t=800,
                     prezzo_fuel_eur_mwh=par_b + 10)[
        "risparmio_eur_anno"] < 0.0


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh776_flussi(4000000, 1520000.0, 15)
    assert len(fl) == 16
    assert fl[0] == -4000000
    assert all(f == 1520000.0 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = demo_calcoli()
    assert bc["van"] == pytest.approx(11777080.218034498)
    assert mh776_van([-4000000] + [1520000.0] * 15,
                     0) == pytest.approx(18800000.0)
    assert mh776_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = demo_calcoli()
    assert bc["tir"] == pytest.approx(37.68636869512414)
    assert mh776_tir([-4000000] + [1520000.0] * 15) == \
        pytest.approx(0.3768636869512414)
    tir = mh776_tir([-4000000] + [1520000.0] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate(
                  [-4000000] + [1520000.0] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    """Payback con cumulato >= 0: il cumulato nullo basta."""
    assert mh776_payback([-4000000] + [1520000.0] * 15) == 3
    assert mh776_payback([-4000000] + [-1000.0] * 15) is None
    assert mh776_payback([0] + [1520000.0] * 15) == 0
    assert mh776_payback([-100] + [50] * 2) == 2
    assert mh776_payback([-3040000.0] +
                         [1520000.0] * 2) == 2


def test_verdetto():
    assert mh776_verdetto(100.0, 4000000, 10.0) == "CONVIENTE"
    assert mh776_verdetto(0.0, 4000000, 10.0) == "NON_CONVIENTE"
    assert mh776_verdetto(-1222919.78, 17000000,
                          10.0) == "MARGINALE"
    assert mh776_verdetto(-1222919.78, 17000000,
                          0.0) == "NON_CONVIENTE"
    assert mh776_verdetto(-8520917.72, 4000000,
                          10.0) == "NON_CONVIENTE"
    assert mh776_verdetto(-100.0, 0, 10.0) == "NON_CONVIENTE"
    assert mh776_verdetto(None, 4000000, 10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh776_verdetto(float("nan"), 4000000, 10.0)
    with pytest.raises(ValueError):
        mh776_verdetto(100.0, -1, 10.0)
    with pytest.raises(ValueError):
        mh776_verdetto(100.0, 4000000, 100.1)


def test_valida_demo_ok():
    v = mh776_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("p_t_anno", "40000"),
                       ("p_t_anno", float("nan")),
                       ("p_t_anno", float("inf")),
                       ("p_t_anno", True),
                       ("prezzo_fuel_eur_mwh", None),
                       ("eta_boiler_pct", "90")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh776_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("p_t_anno", 0),
                          ("p_t_anno", -1),
                          ("q_th_gj_per_t", 0),
                          ("q_th_gj_per_t", -1),
                          ("eta_boiler_pct", 0),
                          ("eta_boiler_pct", 100.1),
                          ("eta_th_chp_pct", 0),
                          ("eta_th_chp_pct", 100.1),
                          ("eta_el_chp_pct", -1),
                          ("eta_el_chp_pct", 100.1),
                          ("e_spec_kwh_per_t", -1),
                          ("prezzo_fuel_eur_mwh", -1),
                          ("prezzo_el_eur_mwh", -1),
                          ("prezzo_sell_eur_mwh", -1),
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
        assert mh776_valida(**d)["valido"] is False


def test_valida_rifiuta_somma_rendimenti_oltre_cento():
    for th, el in ((70.0, 35.0), (50.0, 51.0), (100.0, 0.1)):
        d = _demo_kwargs()
        d["eta_th_chp_pct"] = th
        d["eta_el_chp_pct"] = el
        assert mh776_valida(**d)["valido"] is False
        with pytest.raises(ValueError):
            mh776_calcola(**d)


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"eta_el_chp_pct": 0,
              "e_spec_kwh_per_t": 0,
              "eta_boiler_pct": 100,
              "eta_th_chp_pct": 100,
              "prezzo_fuel_eur_mwh": 0,
              "prezzo_el_eur_mwh": 0,
              "prezzo_sell_eur_mwh": 0,
              "f_fuel_t_per_mwh": 0,
              "f_el_t_per_mwh": 0,
              "om_eur_anno": 0,
              "capex_eur": 0, "wacc_pct": 0,
              "tolleranza_pct": 0})
    # Somma termico + elettrico: 100 + 0 = 100, ammessa.
    assert mh776_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    assert mh776_valida(**d)["valido"] is True


def test_valida_non_controlla_risparmio_calcola_neppure():
    """La validazione input NON controlla il risparmio
    (e' un esito, non un range) e in questa tab
    nemmeno mh776_calcola lo controlla: con prezzo
    combustibile 100 EUR/MWh (sopra il tetto 87,75)
    il caso resta CALCOLABILE."""
    d = _demo_kwargs()
    d["prezzo_fuel_eur_mwh"] = 100
    assert mh776_valida(**d)["valido"] is True
    bc = _variante(prezzo_fuel_eur_mwh=100)
    assert bc["valid"] is True
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["flussi"]
    assert bc["payback"] is None


def test_demo_dict():
    d = mh776_demo()
    assert d["p_t_anno"] == 40000
    assert d["q_th_gj_per_t"] == 3.6
    assert d["eta_boiler_pct"] == 90.0
    assert d["eta_th_chp_pct"] == 50.0
    assert d["eta_el_chp_pct"] == 35.0
    assert d["e_spec_kwh_per_t"] == 250
    assert d["prezzo_fuel_eur_mwh"] == 45
    assert d["prezzo_el_eur_mwh"] == 180
    assert d["prezzo_sell_eur_mwh"] == 90
    assert d["om_eur_anno"] == 300000
    assert d["capex_eur"] == 4000000
    assert d["f_fuel_t_per_mwh"] == 0.20
    assert d["f_el_t_per_mwh"] == 0.40
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
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
    assert bc["q_term_mwh_anno"] == pytest.approx(40000.0)
    assert bc["e_base_mwh_anno"] == pytest.approx(10000.0)
    assert bc["fuel_base_mwh_anno"] == pytest.approx(44444.444444444445)
    assert bc["fuel_chp_mwh_anno"] == pytest.approx(80000.0)
    assert bc["e_chp_mwh_anno"] == pytest.approx(28000.0)
    assert bc["bought_mwh_anno"] == 0.0
    assert bc["surplus_mwh_anno"] == pytest.approx(18000.0)
    assert bc["co2_evitata_t_anno"] == pytest.approx(4088.8888888888887)


def test_demo_calcoli_economia():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(3800000.0)
    assert bc["c_alt_var_eur_anno"] == pytest.approx(1980000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(2280000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(1520000.0)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(87.75)


def test_demo_calcoli_finanza():
    bc = demo_calcoli()
    assert bc["crf"] == pytest.approx(0.09634228760924432)
    assert bc["lco_base_eur_t"] == pytest.approx(95.0)
    assert bc["lco_alt_eur_t"] == pytest.approx(66.63422876092443)
    assert bc["van"] == pytest.approx(11777080.218034498)
    assert bc["tir"] == pytest.approx(37.68636869512414)
    assert bc["payback"] == 3
    assert bc["verdetto"] == "CONVIENTE"


def test_demo_flussi_e_cumulato():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -4000000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(1520000.0)
               for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -4000000
    assert righe.iloc[2]["Cumulato (EUR)"] == pytest.approx(-960000.0)
    assert righe.iloc[3]["Cumulato (EUR)"] == pytest.approx(560000.0)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(18800000.0)
    assert righe.iloc[15]["Flusso (EUR/anno)"] == pytest.approx(
        1520000.0)


def test_demo_tabella_righe():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Produzione cartone (t/anno)"] == pytest.approx(
        40000.0)
    assert mappa["Calore utile (MWh/anno)"] == pytest.approx(40000.0)
    assert mappa["Domanda elettrica (MWh/anno)"] == pytest.approx(
        10000.0)
    assert mappa["Combustibile CHP (MWh/anno)"] == pytest.approx(
        80000.0)
    assert mappa["Elettricita' cogenerata (MWh/anno)"] == pytest.approx(
        28000.0)
    assert mappa["Eccedenza venduta (MWh/anno)"] == pytest.approx(
        18000.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(
        2280000.0)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(1520000.0)
    assert mappa["Payback (anni)"] == 3
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Prezzo combustibile di pareggio (EUR/MWh)"] == \
        pytest.approx(87.75)


def test_demo_coerenza_interna():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["fuel_chp_mwh_anno"] * bc["eta_th_chp_pct"] / 100.0 == \
        pytest.approx(bc["q_term_mwh_anno"])
    assert bc["fuel_chp_mwh_anno"] * bc["eta_el_chp_pct"] / 100.0 == \
        pytest.approx(bc["e_chp_mwh_anno"])
    assert bc["fuel_base_mwh_anno"] == pytest.approx(
        bc["q_term_mwh_anno"] / (bc["eta_boiler_pct"] / 100.0))
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
    p, qsp, ebo = 40000, 3.6, 90.0
    eth, eel, esp = 50.0, 35.0, 250
    pf, pel, ps, om, cx = 45, 180, 90, 300000, 4000000
    ff, fel, wacc, vita = 0.20, 0.40, 5.0, 15
    qt = p * qsp / 3.6
    eb = p * esp / 1000.0
    fb = qt / (ebo / 100.0)
    fc = qt / (eth / 100.0)
    eg = fc * (eel / 100.0)
    bo = max(eb - eg, 0.0)
    su = max(eg - eb, 0.0)
    cb = fb * pf + eb * pel
    cav = fc * pf + bo * pel - su * ps
    ca = cav + om
    risp = cb - ca
    co2b = fb * ff + eb * fel
    co2a = fc * ff + bo * fel - su * fel
    r = wacc / 100.0
    crf = r * (1 + r) ** vita / ((1 + r) ** vita - 1.0)
    lco_b = cb / p
    lco_a = (cx * crf + om) / p + cav / p
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    par = (eb * pel + su * ps - om) / (fc - fb)
    bc = demo_calcoli()
    assert bc["q_term_mwh_anno"] == pytest.approx(qt)
    assert bc["e_base_mwh_anno"] == pytest.approx(eb)
    assert bc["fuel_base_mwh_anno"] == pytest.approx(fb)
    assert bc["fuel_chp_mwh_anno"] == pytest.approx(fc)
    assert bc["e_chp_mwh_anno"] == pytest.approx(eg)
    assert bc["bought_mwh_anno"] == pytest.approx(bo)
    assert bc["surplus_mwh_anno"] == pytest.approx(su)
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


def test_variante_regime_comprato():
    """Regime comprato sul demo (e_spec 800): domanda
    32.000, deficit 4.000, surplus zero, risparmio
    3.140.000, VAN 28.592.126,24, payback 2, pareggio
    133,31 (tetto, numeratore comprato)."""
    bc = _variante(e_spec_kwh_per_t=800)
    assert bc["valid"] is True
    assert bc["e_base_mwh_anno"] == pytest.approx(32000.0)
    assert bc["bought_mwh_anno"] == pytest.approx(4000.0)
    assert bc["surplus_mwh_anno"] == 0.0
    assert bc["c_base_eur_anno"] == pytest.approx(7760000.0)
    assert bc["c_alt_var_eur_anno"] == pytest.approx(4320000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(4620000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(3140000.0)
    assert bc["van"] == pytest.approx(28592126.24)
    assert bc["payback"] == 2
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(133.3125)
    assert bc["lco_base_eur_t"] == pytest.approx(194.0)
    assert bc["lco_alt_eur_t"] == pytest.approx(125.13422876092443)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_co2_negativa_resta_conviente():
    """CO2 negativa con economia invariata: fattore
    elettrico 0,10 -> evitata -4.311,11, verdetto
    sempre CONVIENTE (il fattore elettrico non tocca
    i costi)."""
    bc = _variante(f_el_t_per_mwh=0.10)
    assert bc["valid"] is True
    assert bc["co2_evitata_t_anno"] == pytest.approx(-4311.111111111111)
    assert bc["risparmio_eur_anno"] == pytest.approx(1520000.0)
    assert bc["van"] == pytest.approx(11777080.218034498)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_sopra_tetto_non_conviente():
    """Prezzo combustibile 100 EUR/MWh (sopra il tetto
    87,75): risparmio negativo, VAN negativa oltre
    la tolleranza, payback mai, TIR None (flussi
    tutti negativi dopo l'anno 0)."""
    bc = _variante(prezzo_fuel_eur_mwh=100)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(-435555.555555555)
    assert bc["van"] == pytest.approx(-8520917.72)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["flussi"]


def test_variante_pareggio_esatto_risparmio_zero():
    """Al tetto esatto il risparmio e' zero: il caso
    resta calcolabile con VAN -4.000.000 EUR (solo il
    CAPEX, senza risparmi) e verdetto NON_CONVIENTE."""
    bc = _variante(prezzo_fuel_eur_mwh=87.75)
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["van"] == pytest.approx(-4000000.0)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_marginale_capex_alto():
    """Fascia MARGINALE: CAPEX 17.000.000 EUR, VAN
    negativa entro la tolleranza del 10 % del
    CAPEX (1.700.000 EUR)."""
    bc = _variante(capex_eur=17000000)
    assert bc["valid"] is True
    assert bc["van"] == pytest.approx(-1222919.78)
    assert bc["tir"] == pytest.approx(3.9157)
    assert bc["payback"] == 12
    assert bc["verdetto"] == "MARGINALE"
    bc0 = _variante(capex_eur=17000000, tolleranza_pct=0)
    assert bc0["verdetto"] == "NON_CONVIENTE"
    assert bc0["van"] == pytest.approx(-1222919.78)


def test_variante_capex_zero_payback_zero_tir_none():
    """Payback regola >=: con CAPEX nullo il payback e' 0,
    non 1 (all'anno 0 il cumulato e' gia' zero)."""
    bc = _variante(capex_eur=0)
    assert bc["capex_eur"] == 0
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(15777080.218034498)
    assert bc["lco_alt_eur_t"] == pytest.approx(57.0)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_pareggio_none_termico_alto():
    """F_chp < fuel_base (termico 95 %, elettrico 5 %):
    pareggio None per convenzione, caso calcolabile
    NON_CONVIENTE."""
    bc = _variante(eta_th_chp_pct=95.0, eta_el_chp_pct=5.0)
    assert bc["valid"] is True
    assert bc["fuel_chp_mwh_anno"] == pytest.approx(42105.26315789474)
    assert bc["fuel_chp_mwh_anno"] < bc["fuel_base_mwh_anno"]
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["risparmio_eur_anno"] == pytest.approx(184210.53)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_elettrico_zero_pareggio_none():
    """Rendimento elettrico zero: beneficio elettrico
    nullo, O&M non coperto, pareggio None; caso
    calcolabile con risparmio -1.900.000."""
    bc = _variante(eta_el_chp_pct=0.0)
    assert bc["valid"] is True
    assert bc["e_chp_mwh_anno"] == 0.0
    assert bc["bought_mwh_anno"] == pytest.approx(10000.0)
    assert bc["surplus_mwh_anno"] == 0.0
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["risparmio_eur_anno"] == pytest.approx(-1900000.0)
    assert bc["co2_evitata_t_anno"] == pytest.approx(-7111.111111111111)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_domanda_elettrica_zero_tutto_surplus():
    """Domanda elettrica zero: tutto il CHP va in
    surplus (28.000 MWh/anno), risparmio 620.000,
    VAN 2.435.387,98, payback 7, pareggio 62,44."""
    bc = _variante(e_spec_kwh_per_t=0)
    assert bc["valid"] is True
    assert bc["e_base_mwh_anno"] == 0.0
    assert bc["bought_mwh_anno"] == 0.0
    assert bc["surplus_mwh_anno"] == pytest.approx(28000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(620000.0)
    assert bc["van"] == pytest.approx(2435387.98)
    assert bc["payback"] == 7
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(62.4375)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(18800000.0)
    assert bc["lco_alt_eur_t"] == pytest.approx(63.666666666666664)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_vita_diversa():
    bc = _variante(vita_anni=10)
    assert len(bc["flussi"]) == 11
    assert bc["van"] == pytest.approx(7737037.09)
    assert bc["tir"] == pytest.approx(36.2803)
    assert bc["payback"] == 3
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_om_alto_pareggio_none():
    """O&M 5.000.000 EUR/anno: beneficio elettrico
    3.420.000 non copre l'O&M, pareggio None,
    risparmio -3.180.000, NON_CONVIENTE."""
    bc = _variante(om_eur_anno=5000000)
    assert bc["valid"] is True
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["risparmio_eur_anno"] == pytest.approx(-3180000.0)
    assert bc["van"] == pytest.approx(-37007312.56)
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
        _variante(eta_boiler_pct=0)
    with pytest.raises(ValueError):
        _variante(eta_th_chp_pct=0)
    assert mh776_verdetto(None, 4000000, 10.0) == "NON_CALCOLABILE"
    assert demo_calcoli()["verdetto"] != "NON_CALCOLABILE"


def test_degenere_guard_rendimenti_somma():
    """Guard su rendimenti e somma: caldaia zero o
    sopra 100, termico zero o sopra 100, elettrico
    fuori [0, 100], somma sopra 100 sollevano
    ValueError."""
    for kw in ({"eta_boiler_pct": 0},
               {"eta_boiler_pct": 100.1},
               {"eta_th_chp_pct": 0},
               {"eta_th_chp_pct": 100.1},
               {"eta_el_chp_pct": -1},
               {"eta_el_chp_pct": 100.1},
               {"eta_th_chp_pct": 70.0, "eta_el_chp_pct": 35.0}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh776_valida(**d)["valido"] is False


def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"p_t_anno": 0}, {"p_t_anno": -1},
               {"q_th_gj_per_t": 0},
               {"q_th_gj_per_t": -1},
               {"eta_boiler_pct": 0},
               {"eta_boiler_pct": 100.1},
               {"eta_th_chp_pct": 0},
               {"eta_th_chp_pct": 100.1},
               {"eta_el_chp_pct": -1},
               {"eta_el_chp_pct": 100.1},
               {"eta_th_chp_pct": 70.0, "eta_el_chp_pct": 35.0},
               {"e_spec_kwh_per_t": -1},
               {"prezzo_fuel_eur_mwh": -1},
               {"prezzo_el_eur_mwh": -1},
               {"prezzo_sell_eur_mwh": -1},
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
        assert mh776_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"p_t_anno": "40000"},
               {"p_t_anno": float("nan")},
               {"prezzo_fuel_eur_mwh": float("inf")},
               {"capex_eur": True},
               {"eta_boiler_pct": "90"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh776_valida(**d)["valido"] is False


def test_risparmio_negativo_non_degenere():
    """Differenza chiave: risparmio nullo o
    negativo resta calcolabile, con flussi pieni e
    VAN negativa; cosi' anche la CO2 evitata
    negativa resta calcolabile."""
    for kw in ({"prezzo_fuel_eur_mwh": 100},
               {"eta_el_chp_pct": 0.0}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["verdetto"] in ("NON_CONVIENTE", "MARGINALE")
        assert bc["flussi"]
    bc = _variante(f_el_t_per_mwh=0.10)
    assert bc["co2_evitata_t_anno"] < 0.0
    assert bc["valid"] is True


def test_co2_evitata_segno_funzione_pura():
    assert mh776_co2_evitata(100.0, 150.0) == pytest.approx(-50.0)


def test_verdetto_non_calcolabile_solo_van_none():
    assert mh776_verdetto(None, 4000000, 10.0) == "NON_CALCOLABILE"
    assert demo_calcoli()["verdetto"] != "NON_CALCOLABILE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = demo_calcoli()
    testo = mh776_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert "q_term_mwh_anno;40000.0" in testo
    assert "e_base_mwh_anno;10000.0" in testo
    assert "fuel_base_mwh_anno;44444.444444444445" in testo
    assert "fuel_chp_mwh_anno;80000.0" in testo
    assert "e_chp_mwh_anno;28000.0" in testo
    assert "surplus_mwh_anno;18000.0" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "prezzo_pareggio_eur_mwh" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = demo_calcoli()
    testo = mh776_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"fuel_chp_mwh_anno;{bc['fuel_chp_mwh_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = demo_calcoli()
    testo = mh776_csv(bc, _demo_kwargs())
    for chiave in _demo_kwargs():
        assert f"{chiave};" in testo


def test_monotonia_prezzo_fuel_decrescente():
    # Il risparmio CALA con p_fuel (il CHP brucia piu'
    # combustibile della caldaia): pendenza negativa,
    # il contrario delle tab di risparmio di combustibile.
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(prezzo_fuel_eur_mwh=55)["risparmio_eur_anno"]
    basso = _variante(prezzo_fuel_eur_mwh=35)["risparmio_eur_anno"]
    assert basso > base > alto
    assert base - alto == pytest.approx(355555.5555555556)
    assert basso - base == pytest.approx(355555.5555555556)


def test_monotonia_prezzo_el_e_sell():
    # Piu' caro il prezzo elettrico, piu' vale il CHP
    # (evita acquisti); piu' cara la cessione, piu'
    # vale il surplus: entrambe crescenti.
    base = demo_calcoli()["risparmio_eur_anno"]
    assert _variante(prezzo_el_eur_mwh=190)[
        "risparmio_eur_anno"] > base
    assert _variante(prezzo_sell_eur_mwh=100)[
        "risparmio_eur_anno"] > base
    # In regime comprato la cessione e' irrilevante.
    bc_b = _variante(e_spec_kwh_per_t=800)
    assert _variante(e_spec_kwh_per_t=800,
                     prezzo_sell_eur_mwh=0)[
        "risparmio_eur_anno"] == pytest.approx(
            bc_b["risparmio_eur_anno"])


def test_monotonia_rendimento_elettrico():
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(eta_el_chp_pct=40)["risparmio_eur_anno"]
    basso = _variante(eta_el_chp_pct=30)["risparmio_eur_anno"]
    assert alto > base > basso


def test_demo_deterministica_due_chiamate():
    a = demo_calcoli()
    b = demo_calcoli()
    assert a["van"] == b["van"]
    assert a["flussi"] == b["flussi"]
    assert a["tir"] == b["tir"]


def test_demo_chiavi_attese():
    assert set(mh776_demo().keys()) == {
        "p_t_anno",
        "q_th_gj_per_t", "eta_boiler_pct",
        "eta_th_chp_pct", "eta_el_chp_pct",
        "e_spec_kwh_per_t",
        "prezzo_fuel_eur_mwh", "prezzo_el_eur_mwh",
        "prezzo_sell_eur_mwh",
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
    return ["mh" + "77" + "5", "st" + "77" + "5",
            "tab" + "77" + "5"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w777_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w777_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab776:")


def test_registry_chain_tail_and_count():
    """Registry della nuova tab: il frammento UI apre la tab
    numero 776 (la coda della catena termina con la nuova tab
    e il conteggio atteso delle tab e' 776)."""
    src = _leggi("w777_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 776
    assert src.count("with tab776:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w777_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w777_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st776_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert "key=f" not in src and 'key = f' not in src
    assert "st.stop()" in src
    # guard degenere prima di KPI / grafico / tabella / CSV
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w777_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def776[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w777_ui.py")
        usate = set(re.findall(r'_def776\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 16
        assert usate == {
            "p_t_anno",
            "q_th_gj_per_t", "eta_boiler_pct",
            "eta_th_chp_pct", "eta_el_chp_pct",
            "e_spec_kwh_per_t",
            "prezzo_fuel_eur_mwh", "prezzo_el_eur_mwh",
            "prezzo_sell_eur_mwh",
            "om_eur_anno", "capex_eur",
            "f_fuel_t_per_mwh", "f_el_t_per_mwh",
            "wacc_pct", "vita_anni", "tolleranza_pct"}
        assert usate <= set(mh776_demo().keys())


def test_ui_chiavi_demo_coerenti():
    """Ogni _def776[...] letto dalla UI esiste nel dict demo:
    sweep anti-KeyError a render (lezione dello sweep chiavi demo vs UI)."""
    src = _leggi("w777_ui.py")
    usate = set(re.findall(r'_def776\["([^"]+)"\]', src))
    assert usate
    assert len(usate) == 16
    assert usate <= set(mh776_demo().keys())


def test_ui_riferisce_solo_helper_nuovi():
    src = _leggi("w777_ui.py")
    usati = set(re.findall(r'\b(mh\d+_\w+)\b', src))
    assert usati
    assert all(u.startswith("mh776_") for u in usati)


@pytest.mark.parametrize("e_spec,atteso", [
    (250, 10000.0),
    (800, 32000.0),
    (0, 0.0),
])
def test_e_base_parametrizzato(e_spec, atteso):
    assert mh776_e_base(40000, e_spec) == pytest.approx(atteso)


@pytest.mark.parametrize("campo,valore", [
    ("p_t_anno", 0), ("p_t_anno", -3),
    ("q_th_gj_per_t", 0), ("q_th_gj_per_t", -1),
    ("eta_boiler_pct", 0), ("eta_boiler_pct", 100.1),
    ("eta_th_chp_pct", 0), ("eta_th_chp_pct", 100.1),
    ("eta_el_chp_pct", -1), ("eta_el_chp_pct", 100.1),
    ("e_spec_kwh_per_t", -1),
    ("prezzo_fuel_eur_mwh", -1),
    ("prezzo_el_eur_mwh", -1),
    ("prezzo_sell_eur_mwh", -1),
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
    assert mh776_valida(**d)["valido"] is False


@pytest.mark.parametrize("campo,valore", [
    ("p_t_anno", 0), ("p_t_anno", -3),
    ("q_th_gj_per_t", 0), ("q_th_gj_per_t", -1),
    ("eta_boiler_pct", 0), ("eta_boiler_pct", 100.1),
    ("eta_th_chp_pct", 0), ("eta_th_chp_pct", 100.1),
    ("eta_el_chp_pct", -1), ("eta_el_chp_pct", 100.1),
    ("e_spec_kwh_per_t", -1),
    ("prezzo_fuel_eur_mwh", -1),
    ("prezzo_el_eur_mwh", -1),
    ("prezzo_sell_eur_mwh", -1),
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
        mh776_calcola(**d)


def test_df_tabella_valori_demo_selezionati():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Produzione cartone (t/anno)"] == 40000.0
    assert mappa["Calore utile (MWh/anno)"] == pytest.approx(40000.0)
