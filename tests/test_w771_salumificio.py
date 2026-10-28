"""Test tab771 "Salumificio: stagionare
e cuocere i salumi con pompa di
calore + recupero calore batte
caldaia a gas + frigorifero
elettrico?"

Nuova tab tab771 (salumificio,
file di lavoro w772).
Business case deterministico
di un salumificio: produzione P
t/anno di salumi; domanda termica
Q_dem = P x q_th_spec / 1000
MWh/anno (q_th_spec in kWh/t
salumi: cottura + stagionatura);
domanda di freddo E_dem = P x
e_el_spec / 1000 MWh/anno
(e_el_spec in kWh/t salumi di
freddo termico di celle frigorifere
e stagionatura: E_dem e' freddo,
non elettricita'); calore da pompa
di calore Q_hp = quota_hp x Q_dem
MWh/anno (quota come frazione);
elettricita' pompa di calore E_hp
= Q_hp / COP_hp MWh/anno;
elettricita' chiller residua
E_chiller = E_dem / COP_base
MWh/anno (il chiller resta anche
nell'alternativa, identico nei due
casi); calore di condensazione
Q_cond = E_dem + E_chiller
MWh/anno (primo principio);
calore recuperato Q_rec =
min(quota_recupero x Q_cond,
Q_dem - Q_hp) MWh/anno (quota come
frazione, resa di recupero
esplicita, con tetto alla domanda
residua); calore residuo da caldaia
Q_gas_residuo = Q_dem - Q_hp -
Q_rec MWh/anno (bilancio esatto:
Q_hp + Q_rec + Q_gas_residuo =
Q_dem); costo base C_base =
(Q_dem / eta_caldaia) x p_gas +
(E_dem / COP_base) x p_el
EUR/anno; costo alternativo C_alt
= O&M annuo + (Q_gas_residuo /
eta_caldaia) x p_gas + (E_hp +
E_chiller) x p_el EUR/anno;
risparmio = C_base - C_alt
EUR/anno; CO2 base = (Q_dem /
eta_caldaia) x f_gas + (E_dem /
COP_base) x f_el t/anno; CO2 alt
= (Q_gas_residuo / eta_caldaia) x
f_gas + (E_hp + E_chiller) x f_el
t/anno; CO2 evitata = CO2 base -
CO2 alt, segno libero (negativa
se il fattore elettrico e' alto e
il fattore gas e' basso), NON
monetizzata; fattore di emissione
in tCO2/MWh, numericamente uguale
a kg/kWh (1 kg/kWh = 1 t/MWh);
LCO base = C_base / P; LCO alt =
C_alt / P (il CAPEX NON entra nel
LCO di questa tab: entra nei
flussi, nella VAN, nella TIR e nel
payback); prezzo elettricita' di
pareggio = -(O&M + ((Q_gas_residuo
- Q_dem) / eta_caldaia) x p_gas) /
E_hp EUR/MWh (formula chiusa:
il chiller si elide, il
coefficiente di p_el
nell'alternativa meno la base e'
E_hp), None se E_hp = 0 (quota_hp
= 0: coefficiente nullo), puo'
essere negativo (nessun prezzo
elettrico >= 0 pareggia i conti),
e' un tetto (sopra di esso
l'alternativa perde); flussi
[-CAPEX, risparmio x vita]; VAN,
TIR, payback (primo anno con
cumulato >= 0, regola >= del
brief: con CAPEX nullo il payback
e' 0, con divisione esatta CAPEX
/ risparmio il payback e' l'anno
della divisione esatta).
Verdetto: CONVIENTE se VAN > 0,
MARGINALE se VAN < 0 e |VAN| <=
tolleranza % del CAPEX, altrimenti
NON_CONVIENTE; NON_CALCOLABILE e'
il verdetto del caso degenere
(VAN None: nessun calcolo
eseguibile, quindi nessuna VAN,
nessuna TIR e nessun payback).
Regime degenere SOLLEVA ValueError
negli helper (produzione <= 0,
calore specifico <= 0, freddo
specifico <= 0, rendimento caldaia
<= 0 o > 1, COP chiller <= 0, COP
pompa di calore <= 0, quote fuori
[0, 100] %, prezzi < 0, O&M < 0,
CAPEX < 0, fattori < 0, WACC < 0 o
sopra 50 %, vita <= 0 o non intera,
tolleranza fuori [0, 100] %, input
non numerici o non finiti); la UI
lo intercetta PRIMA di KPI,
grafico, tabella e CSV con
st.stop(). In questa tab il
risparmio nullo o negativo NON e'
degenere: resta calcolabile e
porta a VAN negativa
(NON_CONVIENTE o MARGINALE). La
CO2 evitata negativa NON e'
degenere: e' un numero, non una
guard. Distinta dall'oleificio
(li' si moliscono olive, si produce
sansa e la si brucia in un
cogeneratore a biomassa con vendita
di elettricita': qui niente olive,
niente sansa, niente cogeneratore,
niente vendita di elettricita'),
dal caseificio (li' si pastorizza
latte: qui niente latte, niente
pastorizzazione), dal conservificio
(li' si sterilizzano conserve: qui
niente sterilizzazione di conserve)
e dal macello (li' si macella: qui
niente macellazione, solo salumi
gia' da stagionare e cuocere).

Demo calcolata eseguendo demo_calcoli()
(e ricontrollata a mano, riga per
riga): produzione salumi 1.000
t/anno, calore specifico 800
kWh/t, freddo specifico 500
kWh/t, rendimento caldaia 90 %,
COP chiller 3,0, COP pompa di
calore 4,0, quota pompa di calore
50 %, quota recupero 50 %, prezzo
elettricita' 200 EUR/MWh, prezzo
gas 60 EUR/MWh, O&M annuo 10.000
EUR/anno, CAPEX 150.000 EUR,
fattore elettricita' 0,25
tCO2/MWh, fattore gas 0,20
tCO2/MWh, WACC 5 %, vita 15 anni,
tolleranza MARGINALE 10 % del
CAPEX.

- q_dem_mwh_anno = 800.0
- e_dem_mwh_anno = 500.0
- q_hp_mwh_anno = 400.0
- q_cond_mwh_anno = 666.6666666666666
- q_rec_mwh_anno = 333.3333333333333
- q_gas_residuo_mwh_anno = 66.66666666666669
- e_hp_mwh_anno = 100.0
- e_chiller_residuo_mwh_anno = 166.66666666666666
- e_alt_mwh_anno = 266.66666666666663
- c_base_eur_anno = 86666.66666666666
- c_alt_eur_anno = 67777.77777777778
- co2_base_t_anno = 219.44444444444446
- co2_alt_t_anno = 81.48148148148148
- risparmio_eur_anno = 18888.888888888876
- co2_evitata_t_anno = 137.962962962963
- lco_base_eur_t = 86.66666666666666
- lco_alt_eur_t = 67.77777777777779
- van = 46060.207387855444
- tir = 9.254120168783228
- payback = 8
- prezzo_pareggio_eur_mwh = 388.88888888888886
- verdetto = 'CONVIENTE'

Scomposizione: domanda termica =
1.000 x 800 / 1000 = 800 MWh/anno;
domanda di freddo = 1.000 x 500 /
1000 = 500 MWh/anno; calore da
pompa di calore = 0,50 x 800 = 400
MWh/anno; elettricita' pompa di
calore = 400 / 4,0 = 100 MWh/anno;
elettricita' chiller = 500 / 3,0 =
166,666667 MWh/anno; calore di
condensazione = 500 + 166,666667 =
666,666667 MWh/anno; calore
recuperato = min(0,50 x 666,666667,
800 - 400) = 333,333333 MWh/anno;
calore residuo = 800 - 400 -
333,333333 = 66,666667 MWh/anno;
bilancio 400 + 333,333333 +
66,666667 = 800; costo base =
(800 / 0,90) x 60 + 166,666667 x
200 = 86.666,666667 EUR/anno;
costo alt = 10.000 + (66,666667 /
0,90) x 60 + (100 + 166,666667) x
200 = 67.777,777778 EUR/anno;
risparmio = 86.666,666667 -
67.777,777778 = 18.888,888889
EUR/anno; CO2 base = (800 / 0,90)
x 0,20 + 166,666667 x 0,25 =
219,444444 t/anno; CO2 alt =
(66,666667 / 0,90) x 0,20 +
266,666667 x 0,25 = 81,481481
t/anno; CO2 evitata = 219,444444 -
81,481481 = 137,962963 t/anno;
LCO base 86.666,666667 / 1.000 =
86,666667 EUR/t; LCO alt
67.777,777778 / 1.000 = 67,777778
EUR/t; flussi: anno 0 -150.000,
anni 1-15 risparmio 18.888,888889
(piatti); VAN -150.000 +
18.888,888889 x 10,379658 (annuita'
15 anni al 5 %) = 46.060,21 EUR;
TIR 9,25 %; payback 8 anni (il
cumulato all'anno 7 e' -17.777,78
EUR, all'anno 8 e' 1.111,11 EUR,
gia' >= 0); prezzo elettricita'
di pareggio -(10.000 + ((66,666667
- 800) / 0,90) x 60) / 100 =
388,888889 EUR/MWh (tetto: sopra
di esso l'alternativa perde);
verdetto CONVIENTE perche' VAN > 0.
NOTA: il CAPEX non entra nel LCO
di questa tab: entra solo nei
flussi, nella VAN, nella TIR e
nel payback.
NOTA 2: in questa tab il risparmio
nullo o negativo NON e' degenere:
con prezzo elettricita' 400
EUR/MWh il caso e' calcolabile
(valid=True, flussi pieni),
NON_CONVIENTE con VAN -161.532,95
EUR e payback None, non un
errore.
NOTA 3: la CO2 evitata ha segno
libero in generale (NON monetizzata):
con fattore elettricita' 1,0
tCO2/MWh e fattore gas 0 la CO2
evitata diventa -100 t/anno (0 di
gas evitato meno 100 di
elettricita' in piu' della pompa di
calore) e il caso resta calcolabile
e CONVIENTE economicamente; la
funzione pura resta a segno libero.
NOTA 4: il prezzo elettricita' di
pareggio e' None con quota pompa
di calore zero (E_hp = 0): non e'
un valore mancante, e' la formula
chiusa (coefficiente di prezzo
elettricita' nullo). Puo' essere
negativo (con O&M 60.000 EUR/anno
il pareggio e' -111,11 EUR/MWh:
nessun prezzo elettrico >= 0
pareggia i conti).
NOTA 5: il recupero ha un tetto:
con quota recupero 100 % il grezzo
e' 666,67 MWh/anno ma il tetto
400 = 800 - 400 taglia a 400
MWh/anno, il calore residuo va a
zero e il risparmio sale a
23.333,33 EUR/anno (VAN 92.192,02
EUR, payback 7).
NOTA 6: il payback usa il cumulato
>= 0 (regola >= del brief): con
CAPEX nullo il payback e' 0 (non
1); con flussi [-100, 50, 50] il
payback e' 2 (il cumulato all'anno
2 e' zero, e zero basta).
NOTA 7: il verdetto MARGINALE
richiede VAN negativa entro la
tolleranza % del CAPEX: con CAPEX
210.000 EUR la VAN e' -13.939,79
EUR, entro 21.000 EUR (10 % di
210.000), quindi MARGINALE; con
tolleranza 0 % lo stesso caso e'
NON_CONVIENTE.
NOTA 8: i valori demo sono stati
ricalcolati da zero: il ricalcolo
esatto (senza arrotondamenti
intermedi) da' domanda termica
800, domanda di freddo 500, calore
pompa di calore 400, condensazione
666,666667, recupero 333,333333,
residuo 66,666667, elettricita'
pompa di calore 100, chiller
166,666667, costo base
86.666,666667, costo alt
67.777,777778, risparmio
18.888,888889, CO2 evitata
137,962963, LCO base 86,666667,
LCO alt 67,777778, VAN 46.060,21,
TIR 9,25 %, payback 8 e pareggio
388,888889: i file usano i
valori esatti.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w772_helpers import (
    demo_calcoli,
    mh771_c_alt,
    mh771_c_base,
    mh771_calcola,
    mh771_co2_alt,
    mh771_co2_base,
    mh771_co2_evitata,
    mh771_cop_pos,
    mh771_csv,
    mh771_demo,
    mh771_e_chiller,
    mh771_e_dem,
    mh771_e_hp,
    mh771_flussi,
    mh771_int_pos,
    mh771_lco_alt,
    mh771_lco_base,
    mh771_num,
    mh771_nneg,
    mh771_payback,
    mh771_pct_0_100,
    mh771_pct_0_100_escl0,
    mh771_pct_tolleranza,
    mh771_pct_wacc,
    mh771_pos,
    mh771_prezzo_pareggio,
    mh771_q_cond,
    mh771_q_dem,
    mh771_q_gas_residuo,
    mh771_q_hp,
    mh771_q_rec,
    mh771_risparmio,
    mh771_tir,
    mh771_valida,
    mh771_van,
    mh771_verdetto,
)


def _demo_kwargs():
    return dict(mh771_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh771_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh771_num(3, "x") == 3.0
    assert mh771_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh771_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh771_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh771_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh771_pos(0, "x")
    with pytest.raises(ValueError):
        mh771_pos(-1, "x")
    assert mh771_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh771_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh771_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh771_int_pos(0, "x")


def test_pct_wacc_limiti():
    assert mh771_pct_wacc(0, "x") == 0.0
    assert mh771_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh771_pct_wacc(50.1, "x")


def test_pct_0_100_escl0_limiti():
    assert mh771_pct_0_100_escl0(100, "x") == 100.0
    assert mh771_pct_0_100_escl0(65.0, "x") == 65.0
    with pytest.raises(ValueError):
        mh771_pct_0_100_escl0(0, "x")
    with pytest.raises(ValueError):
        mh771_pct_0_100_escl0(100.1, "x")
    with pytest.raises(ValueError):
        mh771_pct_0_100_escl0(-1, "x")


def test_pct_0_100_limiti():
    assert mh771_pct_0_100(0, "x") == 0.0
    assert mh771_pct_0_100(100, "x") == 100.0
    assert mh771_pct_0_100(50.0, "x") == 50.0
    with pytest.raises(ValueError):
        mh771_pct_0_100(-0.1, "x")
    with pytest.raises(ValueError):
        mh771_pct_0_100(100.1, "x")


def test_pct_tolleranza_limiti():
    assert mh771_pct_tolleranza(0, "x") == 0.0
    assert mh771_pct_tolleranza(100, "x") == 100.0
    assert mh771_pct_tolleranza(10.0, "x") == 10.0
    with pytest.raises(ValueError):
        mh771_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh771_pct_tolleranza(100.1, "x")


def test_cop_pos_senza_tetto_superiore():
    assert mh771_cop_pos(3.0, "x") == 3.0
    assert mh771_cop_pos(0.5, "x") == 0.5
    assert mh771_cop_pos(8.0, "x") == 8.0
    with pytest.raises(ValueError):
        mh771_cop_pos(0, "x")
    with pytest.raises(ValueError):
        mh771_cop_pos(-1, "x")


# ---------------------------------------------------------------- fisica base
def test_q_dem_e_e_dem():
    assert mh771_q_dem(1000, 800) == pytest.approx(800.0)
    assert mh771_q_dem(1000, 400) == pytest.approx(400.0)
    assert mh771_e_dem(1000, 500) == pytest.approx(500.0)
    assert mh771_e_dem(1000, 1000) == pytest.approx(1000.0)
    with pytest.raises(ValueError):
        mh771_q_dem(1000, 0)
    with pytest.raises(ValueError):
        mh771_q_dem(0, 800)
    with pytest.raises(ValueError):
        mh771_e_dem(1000, 0)
    with pytest.raises(ValueError):
        mh771_e_dem(1000, -1)


def test_q_hp_e_hp_e_chiller():
    assert mh771_q_hp(800.0, 0.5) == pytest.approx(400.0)
    assert mh771_q_hp(800.0, 0.0) == 0.0
    assert mh771_q_hp(800.0, 1.0) == pytest.approx(800.0)
    assert mh771_e_hp(400.0, 4.0) == pytest.approx(100.0)
    assert mh771_e_hp(0.0, 4.0) == 0.0
    assert mh771_e_chiller(500.0, 3.0) == pytest.approx(166.66666666666666)
    assert mh771_e_chiller(500.0, 4.0) == pytest.approx(125.0)
    with pytest.raises(ValueError):
        mh771_q_hp(800.0, 1.1)
    with pytest.raises(ValueError):
        mh771_q_hp(800.0, -0.1)
    with pytest.raises(ValueError):
        mh771_e_hp(400.0, 0.0)
    with pytest.raises(ValueError):
        mh771_e_chiller(500.0, 0.0)


def test_q_cond_q_rec_q_gas():
    assert mh771_q_cond(500.0, 166.66666666666666) == pytest.approx(
        666.6666666666666)
    assert mh771_q_cond(500.0, 0.0) == pytest.approx(500.0)
    assert mh771_q_rec(666.6666666666666, 0.5, 800.0,
                       400.0) == pytest.approx(333.3333333333333)
    assert mh771_q_rec(666.6666666666666, 1.0, 800.0,
                       400.0) == pytest.approx(400.0)
    assert mh771_q_rec(666.6666666666666, 0.0, 800.0,
                       400.0) == 0.0
    assert mh771_q_gas_residuo(800.0, 400.0,
                               333.3333333333333) == pytest.approx(
        66.66666666666669)
    assert mh771_q_gas_residuo(800.0, 400.0, 400.0) == 0.0
    assert mh771_q_gas_residuo(800.0, 800.0, 0.0) == 0.0
    with pytest.raises(ValueError):
        mh771_q_rec(666.6666666666666, 1.1, 800.0, 400.0)
    with pytest.raises(ValueError):
        mh771_q_rec(666.6666666666666, 0.5, 800.0, 900.0)
    with pytest.raises(ValueError):
        mh771_q_gas_residuo(800.0, 400.0, 500.0)


def test_bilancio_energetico_demo_e_varianti():
    """Bilancio esatto: Q_hp + Q_rec + Q_gas_residuo = Q_dem,
    nel demo e nelle varianti con tetto di recupero."""
    for bc in (demo_calcoli(),
               _variante(quota_recupero_pct=100.0),
               _variante(quota_hp_pct=100.0),
               _variante(quota_hp_pct=0.0),
               _variante(cop_hp=2.0)):
        assert bc["q_hp_mwh_anno"] + bc["q_rec_mwh_anno"] + \
            bc["q_gas_residuo_mwh_anno"] == pytest.approx(
                bc["q_dem_mwh_anno"], rel=1e-9)


def test_c_base_c_alt():
    assert mh771_c_base(800.0, 500.0, 0.90, 3.0, 200,
                        60) == pytest.approx(86666.66666666666)
    assert mh771_c_base(800.0, 500.0, 1.0, 3.0, 200,
                        60) == pytest.approx(81333.33333333333)
    assert mh771_c_alt(10000, 66.66666666666669, 0.90, 100.0,
                       166.66666666666666, 200,
                       60) == pytest.approx(67777.77777777778)
    assert mh771_c_alt(10000, 0.0, 0.90, 100.0,
                       166.66666666666666, 200,
                       60) == pytest.approx(63333.33333333333)
    with pytest.raises(ValueError):
        mh771_c_base(800.0, 500.0, 0.0, 3.0, 200, 60)
    with pytest.raises(ValueError):
        mh771_c_base(800.0, 500.0, 1.1, 3.0, 200, 60)
    with pytest.raises(ValueError):
        mh771_c_base(800.0, 500.0, 0.90, 0.0, 200, 60)
    with pytest.raises(ValueError):
        mh771_c_alt(10000, 66.66666666666669, 0.90, 100.0,
                    166.66666666666666, -1, 60)


def test_co2_base_alt_evitata():
    assert mh771_co2_base(800.0, 500.0, 0.90, 3.0, 0.25,
                          0.20) == pytest.approx(219.44444444444446)
    assert mh771_co2_alt(66.66666666666669, 0.90, 100.0,
                         166.66666666666666, 0.25,
                         0.20) == pytest.approx(81.48148148148148)
    assert mh771_co2_alt(0.0, 0.90, 100.0,
                         166.66666666666666, 0.25,
                         0.20) == pytest.approx(66.66666666666666)
    assert mh771_co2_evitata(219.44444444444446,
                             81.48148148148148) == pytest.approx(
        137.962962962963)
    assert mh771_co2_evitata(100.0, 150.0) == pytest.approx(-50.0)
    with pytest.raises(ValueError):
        mh771_co2_base(800.0, 500.0, 0.90, 3.0, -0.10, 0.20)


def test_risparmio_segno():
    assert mh771_risparmio(86666.66666666666, 67777.77777777778) == \
        pytest.approx(18888.888888888876)
    assert mh771_risparmio(86666.66666666666, 86666.66666666666) == 0.0
    assert mh771_risparmio(120000.0, 121111.1111111111) == \
        pytest.approx(-1111.111111111095)


def test_lco():
    assert mh771_lco_base(86666.66666666666, 1000) == pytest.approx(
        86.66666666666666)
    assert mh771_lco_alt(67777.77777777778, 1000) == pytest.approx(
        67.77777777777779)
    assert mh771_lco_base(86666.66666666666, 0) is None
    assert mh771_lco_alt(67777.77777777778, 0) is None
    assert mh771_lco_alt(67777.77777777778, -5) is None


def test_prezzo_pareggio_formula_zero_e_negativo():
    assert mh771_prezzo_pareggio(
        10000, 800.0, 66.66666666666669, 0.90, 100.0,
        60) == pytest.approx(388.88888888888886)
    assert mh771_prezzo_pareggio(
        10000, 800.0, 66.66666666666669, 0.90, 0.0,
        60) is None
    assert mh771_prezzo_pareggio(
        60000, 800.0, 66.66666666666669, 0.90, 100.0,
        60) == pytest.approx(-111.11111111111111)
    with pytest.raises(ValueError):
        mh771_prezzo_pareggio(
            10000, 800.0, 66.66666666666669, 0.0, 100.0, 60)


def test_prezzo_pareggio_verifica_pareggio():
    """Al prezzo di pareggio il risparmio si azzera:
    C_alt(p*) = C_base(p*) a meno del gas residuo."""
    bc = demo_calcoli()
    par = bc["prezzo_pareggio_eur_mwh"]
    d = _demo_kwargs()
    d["prezzo_el_eur_mwh"] = par
    bc_par = mh771_calcola(**d)
    assert bc_par["risparmio_eur_anno"] == pytest.approx(
        0.0, abs=1e-6)
    assert bc_par["c_alt_eur_anno"] == pytest.approx(
        bc_par["c_base_eur_anno"], rel=1e-9)


def test_prezzo_pareggio_none_quota_hp_zero():
    """Caso None del brief: quota pompa di calore zero
    -> E_hp zero -> coefficiente di prezzo elettricita'
    nullo -> pareggio None."""
    bc = _variante(quota_hp_pct=0)
    assert bc["e_hp_mwh_anno"] == 0.0
    assert bc["prezzo_pareggio_eur_mwh"] is None
    bc2 = _variante(quota_hp_pct=0, quota_recupero_pct=0)
    assert bc2["prezzo_pareggio_eur_mwh"] is None


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh771_flussi(150000, 18888.888888888876, 15)
    assert len(fl) == 16
    assert fl[0] == -150000
    assert all(f == 18888.888888888876 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = demo_calcoli()
    assert bc["van"] == pytest.approx(46060.207387855444)
    assert mh771_van([-150000] + [18888.888888888876] * 15,
                     0) == pytest.approx(133333.33333333314)
    assert mh771_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = demo_calcoli()
    assert bc["tir"] == pytest.approx(9.254120168783228)
    assert mh771_tir([-150000] + [18888.888888888876] * 15) == \
        pytest.approx(0.09254120168783228)
    tir = mh771_tir([-150000] + [18888.888888888876] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate(
                  [-150000] + [18888.888888888876] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    """Payback con cumulato >= 0: il cumulato nullo basta."""
    assert mh771_payback([-150000] + [18888.888888888876] * 15) == 8
    assert mh771_payback([-150000] + [-1000.0] * 15) is None
    assert mh771_payback([0] + [18888.888888888876] * 15) == 0
    assert mh771_payback([-100] + [50] * 2) == 2
    assert mh771_payback([-37777.77777777775] +
                         [18888.888888888876] * 2) == 2


def test_verdetto():
    assert mh771_verdetto(100.0, 150000, 10.0) == "CONVIENTE"
    assert mh771_verdetto(0.0, 150000, 10.0) == "NON_CONVIENTE"
    assert mh771_verdetto(-13939.792612144558, 210000,
                          10.0) == "MARGINALE"
    assert mh771_verdetto(-13939.792612144558, 210000,
                          0.0) == "NON_CONVIENTE"
    assert mh771_verdetto(-115401.13987273142, 150000,
                          10.0) == "NON_CONVIENTE"
    assert mh771_verdetto(-100.0, 0, 10.0) == "NON_CONVIENTE"
    assert mh771_verdetto(None, 150000, 10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh771_verdetto(float("nan"), 150000, 10.0)
    with pytest.raises(ValueError):
        mh771_verdetto(100.0, -1, 10.0)
    with pytest.raises(ValueError):
        mh771_verdetto(100.0, 150000, 100.1)


def test_valida_demo_ok():
    v = mh771_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("p_t_anno", "1000"),
                       ("p_t_anno", float("nan")),
                       ("p_t_anno", float("inf")),
                       ("p_t_anno", True),
                       ("prezzo_gas_eur_mwh", None),
                       ("cop_hp", "4.0")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh771_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("p_t_anno", 0),
                          ("p_t_anno", -1),
                          ("q_th_spec_kwh_per_t", 0),
                          ("q_th_spec_kwh_per_t", -1),
                          ("e_el_spec_kwh_per_t", 0),
                          ("e_el_spec_kwh_per_t", -1),
                          ("eta_caldaia_pct", 0),
                          ("eta_caldaia_pct", 100.1),
                          ("cop_base", 0),
                          ("cop_base", -1),
                          ("cop_hp", 0),
                          ("cop_hp", -2),
                          ("quota_hp_pct", -1),
                          ("quota_hp_pct", 100.1),
                          ("quota_recupero_pct", -1),
                          ("quota_recupero_pct", 100.1),
                          ("prezzo_el_eur_mwh", -1),
                          ("prezzo_gas_eur_mwh", -1),
                          ("om_eur_anno", -100),
                          ("capex_eur", -1),
                          ("f_el_t_per_mwh", -0.10),
                          ("f_gas_t_per_mwh", -0.10),
                          ("wacc_pct", -0.1), ("wacc_pct", 50.1),
                          ("vita_anni", 0), ("vita_anni", 2.5),
                          ("tolleranza_pct", -1),
                          ("tolleranza_pct", 100.1)):
        d = _demo_kwargs()
        d[campo] = valore
        assert mh771_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"quota_hp_pct": 0,
              "quota_recupero_pct": 0,
              "eta_caldaia_pct": 100,
              "prezzo_gas_eur_mwh": 0,
              "prezzo_el_eur_mwh": 0,
              "f_el_t_per_mwh": 0,
              "f_gas_t_per_mwh": 0,
              "om_eur_anno": 0,
              "capex_eur": 0, "wacc_pct": 0,
              "tolleranza_pct": 0})
    assert mh771_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    assert mh771_valida(**d)["valido"] is True


def test_valida_non_controlla_risparmio_calcola_neppure():
    """La validazione input NON controlla il risparmio
    (e' un esito, non un range) e in questa tab
    nemmeno mh771_calcola lo controlla: con prezzo
    elettricita' 400 EUR/MWh il caso resta CALCOLABILE."""
    d = _demo_kwargs()
    d["prezzo_el_eur_mwh"] = 400
    assert mh771_valida(**d)["valido"] is True
    bc = _variante(prezzo_el_eur_mwh=400)
    assert bc["valid"] is True
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["flussi"]
    assert bc["payback"] is None


def test_demo_dict():
    d = mh771_demo()
    assert d["p_t_anno"] == 1000
    assert d["q_th_spec_kwh_per_t"] == 800
    assert d["e_el_spec_kwh_per_t"] == 500
    assert d["eta_caldaia_pct"] == 90.0
    assert d["cop_base"] == 3.0
    assert d["cop_hp"] == 4.0
    assert d["quota_hp_pct"] == 50.0
    assert d["quota_recupero_pct"] == 50.0
    assert d["prezzo_el_eur_mwh"] == 200
    assert d["prezzo_gas_eur_mwh"] == 60
    assert d["om_eur_anno"] == 10000
    assert d["capex_eur"] == 150000
    assert d["f_el_t_per_mwh"] == 0.25
    assert d["f_gas_t_per_mwh"] == 0.20
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    """Tutti gli output numerici demo a tolleranza
    1e-6 relativa (richiesta del brief): confronto
    contro demo_calcoli()."""
    bc = demo_calcoli()
    attesi = {
        "q_dem_mwh_anno": 800.0,
        "e_dem_mwh_anno": 500.0,
        "q_hp_mwh_anno": 400.0,
        "q_cond_mwh_anno": 666.6666666666666,
        "q_rec_mwh_anno": 333.3333333333333,
        "q_gas_residuo_mwh_anno": 66.66666666666669,
        "e_hp_mwh_anno": 100.0,
        "e_chiller_residuo_mwh_anno": 166.66666666666666,
        "e_alt_mwh_anno": 266.66666666666663,
        "c_base_eur_anno": 86666.66666666666,
        "c_alt_eur_anno": 67777.77777777778,
        "co2_base_t_anno": 219.44444444444446,
        "co2_alt_t_anno": 81.48148148148148,
        "risparmio_eur_anno": 18888.888888888876,
        "co2_evitata_t_anno": 137.962962962963,
        "lco_base_eur_t": 86.66666666666666,
        "lco_alt_eur_t": 67.77777777777779,
        "van": 46060.207387855444,
        "tir": 9.254120168783228,
        "prezzo_pareggio_eur_mwh": 388.88888888888886,
    }
    for chiave, atteso in attesi.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert got == pytest.approx(atteso, rel=1e-6), chiave
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_demo_calcoli_fisica():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["q_dem_mwh_anno"] == pytest.approx(800.0)
    assert bc["e_dem_mwh_anno"] == pytest.approx(500.0)
    assert bc["q_hp_mwh_anno"] == pytest.approx(400.0)
    assert bc["q_cond_mwh_anno"] == pytest.approx(666.6666666666666)
    assert bc["q_rec_mwh_anno"] == pytest.approx(333.3333333333333)
    assert bc["q_gas_residuo_mwh_anno"] == pytest.approx(66.66666666666669)
    assert bc["e_hp_mwh_anno"] == pytest.approx(100.0)
    assert bc["e_chiller_residuo_mwh_anno"] == pytest.approx(
        166.66666666666666)
    assert bc["co2_evitata_t_anno"] == pytest.approx(137.962962962963)


def test_demo_calcoli_economia():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(86666.66666666666)
    assert bc["c_alt_eur_anno"] == pytest.approx(67777.77777777778)
    assert bc["risparmio_eur_anno"] == pytest.approx(18888.888888888876)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(
        388.88888888888886)


def test_demo_calcoli_finanza():
    bc = demo_calcoli()
    assert bc["lco_base_eur_t"] == pytest.approx(86.66666666666666)
    assert bc["lco_alt_eur_t"] == pytest.approx(67.77777777777779)
    assert bc["van"] == pytest.approx(46060.207387855444)
    assert bc["tir"] == pytest.approx(9.254120168783228)
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"


def test_demo_flussi_e_cumulato():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -150000
    assert len(bc["flussi"]) == 16
    assert all(f == 18888.888888888876 for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -150000
    assert righe.iloc[7]["Cumulato (EUR)"] == pytest.approx(
        -17777.77777777787)
    assert righe.iloc[8]["Cumulato (EUR)"] == pytest.approx(
        1111.1111111110076)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(
        133333.33333333314)
    assert righe.iloc[15]["Flusso (EUR/anno)"] == 18888.888888888876


def test_demo_tabella_righe():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Produzione salumi (t/anno)"] == pytest.approx(1000.0)
    assert mappa["Domanda termica (MWh/anno)"] == pytest.approx(800.0)
    assert mappa["Domanda di freddo (MWh/anno)"] == pytest.approx(500.0)
    assert mappa["Calore da pompa di calore (MWh/anno)"] == pytest.approx(
        400.0)
    assert mappa["Calore recuperato (MWh/anno)"] == pytest.approx(
        333.3333333333333)
    assert mappa["Calore residuo da caldaia (MWh/anno)"] == pytest.approx(
        66.66666666666669)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(
        67777.77777777778)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(
        18888.888888888876)
    assert mappa["Payback (anni)"] == 8
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Prezzo elettricita' di pareggio (EUR/MWh)"] == \
        pytest.approx(388.88888888888886)


def test_demo_coerenza_interna():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["q_hp_mwh_anno"] + bc["q_rec_mwh_anno"] + \
        bc["q_gas_residuo_mwh_anno"] == pytest.approx(
            bc["q_dem_mwh_anno"])
    assert bc["q_hp_mwh_anno"] == pytest.approx(
        bc["q_dem_mwh_anno"] * bc["quota_hp_pct"] / 100.0)
    assert bc["e_hp_mwh_anno"] == pytest.approx(
        bc["q_hp_mwh_anno"] / bc["cop_hp"])
    assert bc["e_chiller_residuo_mwh_anno"] == pytest.approx(
        bc["e_dem_mwh_anno"] / bc["cop_base"])
    assert bc["q_cond_mwh_anno"] == pytest.approx(
        bc["e_dem_mwh_anno"] + bc["e_chiller_residuo_mwh_anno"])
    assert bc["q_dem_mwh_anno"] == pytest.approx(
        bc["p_t_anno"] * bc["q_th_spec_kwh_per_t"] / 1000.0)
    assert bc["e_dem_mwh_anno"] == pytest.approx(
        bc["p_t_anno"] * bc["e_el_spec_kwh_per_t"] / 1000.0)
    assert bc["co2_base_t_anno"] - bc["co2_alt_t_anno"] == \
        pytest.approx(bc["co2_evitata_t_anno"])
    assert bc["c_base_eur_anno"] / bc["p_t_anno"] == \
        pytest.approx(bc["lco_base_eur_t"])
    assert bc["c_alt_eur_anno"] / bc["p_t_anno"] == \
        pytest.approx(bc["lco_alt_eur_t"])


def test_demo_contro_riconteggio_indipendente():
    p, qsp, esp = 1000, 800, 500
    ecal, copb, coph = 90.0, 3.0, 4.0
    qhp, qrec = 50.0, 50.0
    pel, pg, om, cx = 200, 60, 10000, 150000
    fel, fg, wacc, vita = 0.25, 0.20, 5.0, 15
    qd = p * qsp / 1000.0
    ed = p * esp / 1000.0
    qh = (qhp / 100.0) * qd
    eh = qh / coph
    ec = ed / copb
    qc = ed + ec
    qr = min((qrec / 100.0) * qc, qd - qh)
    qg = qd - qh - qr
    cb = (qd / (ecal / 100.0)) * pg + (ed / copb) * pel
    ca = om + (qg / (ecal / 100.0)) * pg + (eh + ec) * pel
    risp = cb - ca
    co2b = (qd / (ecal / 100.0)) * fg + (ed / copb) * fel
    co2a = (qg / (ecal / 100.0)) * fg + (eh + ec) * fel
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    par = -(om + ((qg - qd) / (ecal / 100.0)) * pg) / eh
    bc = demo_calcoli()
    assert bc["q_dem_mwh_anno"] == pytest.approx(qd)
    assert bc["e_dem_mwh_anno"] == pytest.approx(ed)
    assert bc["q_hp_mwh_anno"] == pytest.approx(qh)
    assert bc["e_hp_mwh_anno"] == pytest.approx(eh)
    assert bc["e_chiller_residuo_mwh_anno"] == pytest.approx(ec)
    assert bc["q_cond_mwh_anno"] == pytest.approx(qc)
    assert bc["q_rec_mwh_anno"] == pytest.approx(qr)
    assert bc["q_gas_residuo_mwh_anno"] == pytest.approx(qg)
    assert bc["c_base_eur_anno"] == pytest.approx(cb)
    assert bc["c_alt_eur_anno"] == pytest.approx(ca)
    assert bc["risparmio_eur_anno"] == pytest.approx(risp)
    assert bc["co2_base_t_anno"] == pytest.approx(co2b)
    assert bc["co2_alt_t_anno"] == pytest.approx(co2a)
    assert bc["van"] == pytest.approx(van)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(par)


# ---------------------------------------------------------------- varianti
def test_demo_conviente():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] > 0.0
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_recupero_tetto():
    """Recupero al 100 %: il grezzo 666,67 supera il
    tetto 400 = 800 - 400, quindi Q_rec = 400 e il
    calore residuo va a zero."""
    bc = _variante(quota_recupero_pct=100.0)
    assert bc["valid"] is True
    assert bc["q_rec_mwh_anno"] == pytest.approx(400.0)
    assert bc["q_gas_residuo_mwh_anno"] == 0.0
    assert bc["c_alt_eur_anno"] == pytest.approx(63333.33333333333)
    assert bc["risparmio_eur_anno"] == pytest.approx(23333.33333333333)
    assert bc["van"] == pytest.approx(92192.0208908804)
    assert bc["tir"] == pytest.approx(13.101703848589114)
    assert bc["payback"] == 7
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(
        433.33333333333337)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_quota_hp_zero():
    """Quota pompa di calore zero: E_hp zero, pareggio
    None, risparmio solo da recupero, VAN negativa
    oltre la tolleranza."""
    bc = _variante(quota_hp_pct=0)
    assert bc["valid"] is True
    assert bc["q_hp_mwh_anno"] == 0.0
    assert bc["e_hp_mwh_anno"] == 0.0
    assert bc["q_rec_mwh_anno"] == pytest.approx(333.3333333333333)
    assert bc["q_gas_residuo_mwh_anno"] == pytest.approx(
        466.6666666666667)
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["risparmio_eur_anno"] == pytest.approx(12222.222222222219)
    assert bc["van"] == pytest.approx(-23137.512866681707)
    assert bc["payback"] == 13
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_quota_hp_cento():
    """Quota pompa di calore 100 %: tutto il calore
    dalla pompa, recupero zero (tetto zero), residuo
    zero, risparmio piccolo perche' l'elettricita'
    della pompa pesa."""
    bc = _variante(quota_hp_pct=100.0)
    assert bc["valid"] is True
    assert bc["q_hp_mwh_anno"] == pytest.approx(800.0)
    assert bc["q_rec_mwh_anno"] == 0.0
    assert bc["q_gas_residuo_mwh_anno"] == 0.0
    assert bc["e_hp_mwh_anno"] == pytest.approx(200.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(3333.3333333333285)
    assert bc["van"] == pytest.approx(-115401.13987273142)
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(
        216.66666666666669)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_marginale_capex_alto():
    """Fascia MARGINALE: CAPEX 210.000 EUR, VAN
    negativa entro la tolleranza del 10 % del
    CAPEX (21.000 EUR)."""
    bc = _variante(capex_eur=210000)
    assert bc["valid"] is True
    assert bc["van"] == pytest.approx(-13939.792612144558)
    assert bc["tir"] == pytest.approx(4.000952367749103)
    assert bc["payback"] == 12
    assert bc["verdetto"] == "MARGINALE"
    bc0 = _variante(capex_eur=210000, tolleranza_pct=0)
    assert bc0["verdetto"] == "NON_CONVIENTE"
    assert bc0["van"] == pytest.approx(-13939.792612144558)


def test_variante_non_conviente_prezzo_el_alto():
    """NON_CONVIENTE: prezzo elettricita' 400 EUR/MWh,
    sopra il pareggio 388,89: risparmio negativo,
    VAN negativa oltre la tolleranza, payback mai."""
    bc = _variante(prezzo_el_eur_mwh=400)
    assert bc["valid"] is True
    assert bc["c_base_eur_anno"] == pytest.approx(120000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(121111.1111111111)
    assert bc["risparmio_eur_anno"] == pytest.approx(-1111.111111111095)
    assert bc["van"] == pytest.approx(-161532.95337575604)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["flussi"]


def test_variante_non_conviente_cop_hp_basso():
    """NON_CONVIENTE per COP basso: COP pompa di
    calore 2,0, elettricita' pompa raddoppiata."""
    bc = _variante(cop_hp=2.0)
    assert bc["valid"] is True
    assert bc["e_hp_mwh_anno"] == pytest.approx(200.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-1111.111111111124)
    assert bc["van"] == pytest.approx(-161532.9533757564)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_wacc_zero():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(133333.33333333314)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    """Payback regola >=: con CAPEX nullo il payback e' 0,
    non 1 (all'anno 0 il cumulato e' gia' zero)."""
    bc = _variante(capex_eur=0)
    assert bc["capex_eur"] == 0
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(196060.20738785548)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_vita_diversa():
    bc = _variante(vita_anni=20)
    assert len(bc["flussi"]) == 21
    assert bc["van"] == pytest.approx(85397.30647019946)
    assert bc["tir"] == pytest.approx(11.042634210570377)
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_co2_evitata_negativa_non_degenere():
    """CO2 evitata negativa NON degenere: fattore
    elettrico 1,0 e fattore gas zero -> evitata
    -100 t/anno, caso calcolabile e CONVIENTE."""
    bc = _variante(f_el_t_per_mwh=1.0, f_gas_t_per_mwh=0.0)
    assert bc["valid"] is True
    assert bc["co2_base_t_anno"] == pytest.approx(166.66666666666666)
    assert bc["co2_alt_t_anno"] == pytest.approx(266.66666666666663)
    assert bc["co2_evitata_t_anno"] == pytest.approx(-100.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(18888.888888888876)
    assert bc["verdetto"] == "CONVIENTE"


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
        _variante(cop_hp=0)
    assert mh771_verdetto(None, 150000, 10.0) == "NON_CALCOLABILE"
    assert demo_calcoli()["verdetto"] != "NON_CALCOLABILE"


def test_degenere_guard_cop_rendimenti_nulli():
    """Guard su COP e rendimenti nulli: COP chiller
    zero, COP pompa di calore zero, rendimento
    caldaia zero sollevano ValueError."""
    for kw in ({"cop_base": 0}, {"cop_base": -1},
               {"cop_hp": 0}, {"cop_hp": -2},
               {"eta_caldaia_pct": 0},
               {"eta_caldaia_pct": 100.1}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh771_valida(**d)["valido"] is False


def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"p_t_anno": 0}, {"p_t_anno": -1},
               {"q_th_spec_kwh_per_t": 0},
               {"q_th_spec_kwh_per_t": -1},
               {"e_el_spec_kwh_per_t": 0},
               {"e_el_spec_kwh_per_t": -1},
               {"eta_caldaia_pct": 0},
               {"eta_caldaia_pct": 100.1},
               {"cop_base": 0}, {"cop_base": -1},
               {"cop_hp": 0}, {"cop_hp": -2},
               {"quota_hp_pct": -1},
               {"quota_hp_pct": 100.1},
               {"quota_recupero_pct": -1},
               {"quota_recupero_pct": 100.1},
               {"prezzo_el_eur_mwh": -1},
               {"prezzo_gas_eur_mwh": -1},
               {"om_eur_anno": -100},
               {"capex_eur": -1},
               {"f_el_t_per_mwh": -0.10},
               {"f_gas_t_per_mwh": -0.10},
               {"wacc_pct": -1}, {"wacc_pct": 60},
               {"vita_anni": 0}, {"vita_anni": 2.5},
               {"tolleranza_pct": -1},
               {"tolleranza_pct": 100.1}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh771_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"p_t_anno": "1000"},
               {"p_t_anno": float("nan")},
               {"prezzo_gas_eur_mwh": float("inf")},
               {"capex_eur": True},
               {"cop_hp": "4.0"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh771_valida(**d)["valido"] is False


def test_risparmio_negativo_non_degenere():
    """Differenza chiave: risparmio nullo o
    negativo resta calcolabile, con flussi pieni e
    VAN negativa."""
    for kw in ({"prezzo_el_eur_mwh": 400},
               {"cop_hp": 2.0}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["verdetto"] in ("NON_CONVIENTE", "MARGINALE")
        assert bc["flussi"]


def test_co2_evitata_segno_libero_funzione_pura():
    assert mh771_co2_evitata(100.0, 150.0) == pytest.approx(-50.0)


def test_verdetto_non_calcolabile_solo_van_none():
    assert mh771_verdetto(None, 150000, 10.0) == "NON_CALCOLABILE"
    assert demo_calcoli()["verdetto"] != "NON_CALCOLABILE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = demo_calcoli()
    testo = mh771_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert "q_dem_mwh_anno;800.0" in testo
    assert "e_dem_mwh_anno;500.0" in testo
    assert "q_hp_mwh_anno;400.0" in testo
    assert "q_rec_mwh_anno;333.3333333333333" in testo
    assert "q_gas_residuo_mwh_anno;66.66666666666669" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "prezzo_pareggio_eur_mwh" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = demo_calcoli()
    testo = mh771_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"q_hp_mwh_anno;{bc['q_hp_mwh_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = demo_calcoli()
    testo = mh771_csv(bc, _demo_kwargs())
    for chiave in _demo_kwargs():
        assert f"{chiave};" in testo


def test_monotonia_prezzo_gas():
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(prezzo_gas_eur_mwh=70)["risparmio_eur_anno"]
    basso = _variante(prezzo_gas_eur_mwh=50)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(8148.148148148148)
    assert base - basso == pytest.approx(8148.148148148148)


def test_monotonia_prezzo_el():
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(prezzo_el_eur_mwh=210)["risparmio_eur_anno"]
    basso = _variante(prezzo_el_eur_mwh=190)["risparmio_eur_anno"]
    assert alto < base < basso
    assert base - alto == pytest.approx(1000.0)
    assert basso - base == pytest.approx(1000.0)


def test_monotonia_quota_hp():
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(quota_hp_pct=60)["risparmio_eur_anno"]
    basso = _variante(quota_hp_pct=40)["risparmio_eur_anno"]
    assert alto > base > basso


def test_demo_deterministica_due_chiamate():
    a = demo_calcoli()
    b = demo_calcoli()
    assert a["van"] == b["van"]
    assert a["flussi"] == b["flussi"]
    assert a["tir"] == b["tir"]


def test_demo_chiavi_attese():
    assert set(mh771_demo().keys()) == {
        "p_t_anno",
        "q_th_spec_kwh_per_t", "e_el_spec_kwh_per_t",
        "eta_caldaia_pct",
        "cop_base", "cop_hp",
        "quota_hp_pct", "quota_recupero_pct",
        "prezzo_el_eur_mwh", "prezzo_gas_eur_mwh",
        "om_eur_anno", "capex_eur",
        "f_el_t_per_mwh", "f_gas_t_per_mwh",
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
    return ["mh" + "77" + "0", "st" + "77" + "0",
            "tab" + "77" + "0", "w" + "77" + "1_",
            "mh" + "76" + "9", "st" + "76" + "9",
            "tab" + "76" + "9", "w" + "77" + "0_"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w772_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w772_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab771:")


def test_registry_chain_tail_and_count():
    """Registry della nuova tab: il frammento UI apre la tab
    numero 771 (la coda della catena termina con la nuova tab
    e il conteggio atteso delle tab e' 771)."""
    src = _leggi("w772_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 771
    assert src.count("with tab771:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w772_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w772_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st771_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert "key=f" not in src and 'key = f' not in src
    assert "st.stop()" in src
    # guard degenere prima di KPI / grafico / tabella / CSV
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w772_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def771[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w772_ui.py")
        usate = set(re.findall(r'_def771\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 17
        assert usate <= set(mh771_demo().keys())


def test_ui_chiavi_demo_coerenti():
    """Ogni _def771[...] letto dalla UI esiste nel dict demo:
    sweep anti-KeyError a render (lezione dello sweep chiavi demo vs UI)."""
    src = _leggi("w772_ui.py")
    usate = set(re.findall(r'_def771\["([^"]+)"\]', src))
    assert usate
    assert len(usate) == 17
    assert usate <= set(mh771_demo().keys())


def test_ui_riferisce_solo_helper_nuovi():
    src = _leggi("w772_ui.py")
    usati = set(re.findall(r'\b(mh\d+_\w+)\b', src))
    assert usati
    assert all(u.startswith("mh771_") for u in usati)


@pytest.mark.parametrize("e_el_spec,atteso", [
    (500, 500.0),
    (1000, 1000.0),
    (250, 250.0),
])
def test_e_dem_parametrizzato(e_el_spec, atteso):
    assert mh771_e_dem(1000, e_el_spec) == pytest.approx(atteso)


@pytest.mark.parametrize("campo,valore", [
    ("p_t_anno", 0), ("p_t_anno", -3),
    ("q_th_spec_kwh_per_t", 0), ("q_th_spec_kwh_per_t", -1),
    ("e_el_spec_kwh_per_t", 0), ("e_el_spec_kwh_per_t", -1),
    ("eta_caldaia_pct", 0), ("eta_caldaia_pct", 100.1),
    ("cop_base", 0), ("cop_base", -1),
    ("cop_hp", 0), ("cop_hp", -2),
    ("quota_hp_pct", -1), ("quota_hp_pct", 100.1),
    ("quota_recupero_pct", -1), ("quota_recupero_pct", 100.1),
    ("prezzo_el_eur_mwh", -1),
    ("prezzo_gas_eur_mwh", -1),
    ("om_eur_anno", -100),
    ("capex_eur", -1),
    ("f_el_t_per_mwh", -0.10),
    ("f_gas_t_per_mwh", -0.10),
    ("wacc_pct", -0.1), ("wacc_pct", 50.1),
    ("vita_anni", -1), ("vita_anni", 2.5),
    ("tolleranza_pct", -1), ("tolleranza_pct", 100.1),
])
def test_valida_rifiuta_singoli_campi(campo, valore):
    d = _demo_kwargs()
    d[campo] = valore
    assert mh771_valida(**d)["valido"] is False


@pytest.mark.parametrize("campo,valore", [
    ("p_t_anno", 0), ("p_t_anno", -3),
    ("q_th_spec_kwh_per_t", 0), ("q_th_spec_kwh_per_t", -1),
    ("e_el_spec_kwh_per_t", 0), ("e_el_spec_kwh_per_t", -1),
    ("eta_caldaia_pct", 0), ("eta_caldaia_pct", 100.1),
    ("cop_base", 0), ("cop_base", -1),
    ("cop_hp", 0), ("cop_hp", -2),
    ("quota_hp_pct", -1), ("quota_hp_pct", 100.1),
    ("quota_recupero_pct", -1), ("quota_recupero_pct", 100.1),
    ("prezzo_el_eur_mwh", -1),
    ("prezzo_gas_eur_mwh", -1),
    ("om_eur_anno", -100),
    ("capex_eur", -1),
    ("f_el_t_per_mwh", -0.10),
    ("f_gas_t_per_mwh", -0.10),
    ("wacc_pct", -0.1), ("wacc_pct", 50.1),
    ("vita_anni", -1), ("vita_anni", 2.5),
    ("tolleranza_pct", -1), ("tolleranza_pct", 100.1),
])
def test_calcola_sollevela_singoli_campi(campo, valore):
    d = _demo_kwargs()
    d[campo] = valore
    with pytest.raises(ValueError):
        mh771_calcola(**d)


def test_df_tabella_valori_demo_selezionati():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Produzione salumi (t/anno)"] == 1000.0
    assert mappa["Domanda termica (MWh/anno)"] == pytest.approx(800.0)
    assert mappa["Calore recuperato (MWh/anno)"] == pytest.approx(
        333.3333333333333)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(
        18888.888888888876)
    assert mappa["Verdetto"] == "CONVIENTE"


def test_lco_alt_minore_di_lco_base_demo():
    bc = demo_calcoli()
    assert bc["lco_alt_eur_t"] < bc["lco_base_eur_t"]
    assert bc["lco_base_eur_t"] - bc["lco_alt_eur_t"] == pytest.approx(
        18.88888888888887)
