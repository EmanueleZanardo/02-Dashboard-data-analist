"""Test tab772 "Distilleria: distillare
con pompa di calore + recupero calore
dai condensatori batte la caldaia a
gas?"

Nuova tab tab772 (distilleria, file di
lavoro w773). Business case
deterministico di una distilleria:
produzione P LPA/anno di alcol puro;
domanda termica Q_dem = P x q_th_spec
/ 1000 MWh/anno (q_th_spec in kWh/LPA:
distillazione); domanda di freddo
E_dem = P x e_el_spec / 1000 MWh/anno
(e_el_spec in kWh/LPA di freddo
termico di condensazione: E_dem e'
freddo, non elettricita'); calore da
pompa di calore Q_hp = quota_hp x
Q_dem MWh/anno (quota come frazione);
elettricita' pompa di calore E_hp =
Q_hp / COP_hp MWh/anno; elettricita'
chiller residua E_chiller = E_dem /
COP_base MWh/anno (il chiller resta
anche nell'alternativa, identico nei
due casi); calore di condensazione
Q_cond = E_dem + E_chiller MWh/anno
(primo principio); calore recuperato
Q_rec = min(quota_recupero x Q_cond,
Q_dem - Q_hp) MWh/anno (quota come
frazione, resa di recupero esplicita,
con tetto alla domanda residua);
calore residuo da caldaia
Q_gas_residuo = Q_dem - Q_hp - Q_rec
MWh/anno (bilancio esatto: Q_hp +
Q_rec + Q_gas_residuo = Q_dem); costo
base C_base = (Q_dem / eta_caldaia) x
p_gas + (E_dem / COP_base) x p_el
EUR/anno; costo alternativo C_alt =
O&M annuo + (Q_gas_residuo /
eta_caldaia) x p_gas + (E_hp +
E_chiller) x p_el EUR/anno; risparmio
= C_base - C_alt EUR/anno; CO2 base =
(Q_dem / eta_caldaia) x f_gas + (E_dem
/ COP_base) x f_el t/anno; CO2 alt =
(Q_gas_residuo / eta_caldaia) x f_gas
+ (E_hp + E_chiller) x f_el t/anno;
CO2 evitata = CO2 base - CO2 alt,
segno libero (negativa se il fattore
elettrico e' alto e il fattore gas e'
basso), NON monetizzata; fattore di
emissione in tCO2/MWh, numericamente
uguale a kg/kWh (1 kg/kWh = 1 t/MWh);
LCO base = C_base / P; LCO alt =
C_alt / P (il CAPEX NON entra nel
LCO di questa tab: entra nei flussi,
nella VAN, nella TIR e nel payback);
prezzo elettricita' di pareggio =
-(O&M + ((Q_gas_residuo - Q_dem) /
eta_caldaia) x p_gas) / E_hp EUR/MWh
(formula chiusa: il chiller si elide,
il coefficiente di p_el
nell'alternativa meno la base e'
E_hp), None se E_hp = 0 (quota_hp =
0: coefficiente nullo), puo' essere
negativo (nessun prezzo elettrico
>= 0 pareggia i conti), e' un tetto
(sopra di esso l'alternativa perde);
flussi [-CAPEX, risparmio x vita];
VAN, TIR, payback (primo anno con
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
(produzione <= 0, calore specifico
<= 0, freddo specifico <= 0,
rendimento caldaia <= 0 o > 1, COP
chiller <= 0, COP pompa di calore
<= 0, quote fuori [0, 100] %, prezzi
< 0, O&M < 0, CAPEX < 0, fattori < 0,
WACC < 0 o sopra 50 %, vita <= 0 o
non intera, tolleranza fuori [0,
100] %, input non numerici o non
finiti); la UI lo intercetta PRIMA
di KPI, grafico, tabella e CSV con
st.stop(). In questa tab il risparmio
nullo o negativo NON e' degenere:
resta calcolabile e porta a VAN
negativa (NON_CONVIENTE o
MARGINALE). La CO2 evitata negativa
NON e' degenere: e' un numero, non
una guard. Distinzione esplicita:
questa tab distilla alcol, non birra,
non latte, non salumi.

Demo calcolata eseguendo
demo_calcoli() e ricontrollata con
un ricalcolo indipendente da zero
(riga per riga): produzione alcol
puro 200.000 LPA/anno, calore
specifico 8,0 kWh/LPA, freddo
specifico 1,5 kWh/LPA, rendimento
caldaia 90 %, COP chiller 3,0, COP
pompa di calore 4,5, quota pompa di
calore 60 %, quota recupero 60 %,
prezzo elettricita' 200 EUR/MWh,
prezzo gas 60 EUR/MWh, O&M annuo
10.000 EUR/anno, CAPEX 250.000 EUR,
fattore elettricita' 0,25 tCO2/MWh,
fattore gas 0,20 tCO2/MWh, WACC 5 %,
vita 15 anni, tolleranza MARGINALE
10 % del CAPEX.

- q_dem_mwh_anno = 1600.0
- e_dem_mwh_anno = 300.0
- q_hp_mwh_anno = 960.0
- q_cond_mwh_anno = 400.0
- q_rec_mwh_anno = 240.0
- q_gas_residuo_mwh_anno = 400.0
- e_hp_mwh_anno = 213.33333333333334
- e_chiller_residuo_mwh_anno = 100.0
- e_alt_mwh_anno = 313.33333333333337
- c_base_eur_anno = 126666.66666666667
- c_alt_eur_anno = 99333.33333333334
- co2_base_t_anno = 380.5555555555556
- co2_alt_t_anno = 167.22222222222223
- risparmio_eur_anno = 27333.33333333333
- co2_evitata_t_anno = 213.33333333333337
- lco_base_eur_t = 0.6333333333333333
- lco_alt_eur_t = 0.4966666666666667
- van = 33710.6530436028
- tir = 6.933416761516635
- payback = 10
- prezzo_pareggio_eur_mwh = 328.125
- verdetto = 'CONVIENTE'

Scomposizione: domanda termica =
200.000 x 8,0 / 1000 = 1.600
MWh/anno; domanda di freddo =
200.000 x 1,5 / 1000 = 300 MWh/anno;
calore da pompa di calore = 0,60 x
1.600 = 960 MWh/anno; elettricita'
pompa di calore = 960 / 4,5 =
213,333333 MWh/anno; elettricita'
chiller = 300 / 3,0 = 100 MWh/anno;
calore di condensazione = 300 + 100 =
400 MWh/anno; calore recuperato =
min(0,60 x 400, 1.600 - 960) = 240
MWh/anno; calore residuo = 1.600 -
960 - 240 = 400 MWh/anno; bilancio
960 + 240 + 400 = 1.600; costo base
= (1.600 / 0,90) x 60 + 100 x 200 =
126.666,666667 EUR/anno; costo alt =
10.000 + (400 / 0,90) x 60 + (213,333333
+ 100) x 200 = 99.333,333333 EUR/anno;
risparmio = 126.666,666667 -
99.333,333333 = 27.333,333333
EUR/anno; CO2 base = (1.600 / 0,90)
x 0,20 + 100 x 0,25 = 380,555556
t/anno; CO2 alt = (400 / 0,90) x 0,20
+ 313,333333 x 0,25 = 167,222222
t/anno; CO2 evitata = 380,555556 -
167,222222 = 213,333333 t/anno; LCO
base 126.666,666667 / 200.000 =
0,633333 EUR/LPA; LCO alt
99.333,333333 / 200.000 = 0,496667
EUR/LPA; flussi: anno 0 -250.000,
anni 1-15 risparmio 27.333,333333
(piatti); VAN -250.000 +
27.333,333333 x 10,379658 (annuita'
15 anni al 5 %) = 33.710,65 EUR;
TIR 6,93 %; payback 10 anni (il
cumulato all'anno 9 e' -4.000 EUR,
all'anno 10 e' 23.333,33 EUR, gia'
>= 0); prezzo elettricita' di
pareggio -(10.000 + ((400 - 1.600) /
0,90) x 60) / 213,333333 = 328,125
EUR/MWh (tetto: sopra di esso
l'alternativa perde); verdetto
CONVIENTE perche' VAN > 0.
NOTA: il CAPEX non entra nel LCO
di questa tab: entra solo nei
flussi, nella VAN, nella TIR e
nel payback.
NOTA 2: in questa tab il risparmio
nullo o negativo NON e' degenere:
con prezzo elettricita' 400
EUR/MWh il caso e' calcolabile
(valid=True, flussi pieni),
NON_CONVIENTE con VAN -409.154,76
EUR e payback None, non un
errore.
NOTA 3: la CO2 evitata ha segno
libero in generale (NON monetizzata):
con fattore elettricita' 1,0
tCO2/MWh e fattore gas 0 la CO2
evitata diventa -213,333333 t/anno
(0 di gas evitato meno 213,333333
di elettricita' in piu' della pompa
di calore) e il caso resta
calcolabile e CONVIENTE
economicamente; la funzione pura
resta a segno libero.
NOTA 4: il prezzo elettricita' di
pareggio e' None con quota pompa
di calore zero (E_hp = 0): non e'
un valore mancante, e' la formula
chiusa (coefficiente di prezzo
elettricita' nullo). Puo' essere
negativo (con O&M 90.000 EUR/anno
il pareggio e' -46,875 EUR/MWh:
nessun prezzo elettrico >= 0
pareggia i conti).
NOTA 5: il recupero ha un tetto:
con quota pompa di calore 90 % e
quota recupero 100 % il grezzo e'
400 MWh/anno ma il tetto 160 =
1.600 - 1.440 taglia a 160 MWh/anno,
il calore residuo va a zero e il
risparmio e' 32.666,67 EUR/anno
(VAN 89.068,83 EUR, payback 8).
Con quota recupero 100 % sul demo
invece il grezzo 400 resta sotto
il tetto 640 e il recupero vale 400
MWh/anno (VAN 144.427,01 EUR,
payback 7).
NOTA 6: il payback usa il cumulato
>= 0 (regola >= del brief): con
CAPEX nullo il payback e' 0 (non
1); con flussi [-100, 50, 50] il
payback e' 2 (il cumulato all'anno
2 e' zero, e zero basta).
NOTA 7: il verdetto MARGINALE
richiede VAN negativa entro la
tolleranza % del CAPEX: con CAPEX
300.000 EUR la VAN e' -16.289,35
EUR, entro 30.000 EUR (10 % di
300.000), quindi MARGINALE; con
tolleranza 0 % lo stesso caso e'
NON_CONVIENTE.
NOTA 8: i valori demo sono stati
ricalcolati da zero con un calcolo
indipendente: il ricalcolo esatto
(senza arrotondamenti intermedi)
da' domanda termica 1.600, domanda
di freddo 300, calore pompa di
calore 960, condensazione 400,
recupero 240, residuo 400,
elettricita' pompa di calore
213,333333, chiller 100, costo base
126.666,666667, costo alt
99.333,333333, risparmio
27.333,333333, CO2 base 380,555556,
CO2 alt 167,222222, CO2 evitata
213,333333, LCO base 0,633333, LCO
alt 0,496667, VAN 33.710,65, TIR
6,93 %, payback 10 e pareggio
328,125: i file usano i valori
esatti. Il brief iniziale indicava
CO2 alternativa 166,11 ed evitata
214,44 e TIR 7,3 %: il ricalcolo
indipendente li smentisce (CO2 alt
= 88,888889 + 78,333333 = 167,222222;
TIR = 6,933417 %), e i test usano
i valori ricalcolati, non quelli
del brief.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w773_helpers import (
    demo_calcoli,
    mh772_c_alt,
    mh772_c_base,
    mh772_calcola,
    mh772_co2_alt,
    mh772_co2_base,
    mh772_co2_evitata,
    mh772_cop_pos,
    mh772_csv,
    mh772_demo,
    mh772_e_chiller,
    mh772_e_dem,
    mh772_e_hp,
    mh772_flussi,
    mh772_int_pos,
    mh772_lco_alt,
    mh772_lco_base,
    mh772_num,
    mh772_nneg,
    mh772_payback,
    mh772_pct_0_100,
    mh772_pct_0_100_escl0,
    mh772_pct_tolleranza,
    mh772_pct_wacc,
    mh772_pos,
    mh772_prezzo_pareggio,
    mh772_q_cond,
    mh772_q_dem,
    mh772_q_gas_residuo,
    mh772_q_hp,
    mh772_q_rec,
    mh772_risparmio,
    mh772_tir,
    mh772_valida,
    mh772_van,
    mh772_verdetto,
)


def _demo_kwargs():
    return dict(mh772_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh772_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh772_num(3, "x") == 3.0
    assert mh772_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh772_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh772_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh772_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh772_pos(0, "x")
    with pytest.raises(ValueError):
        mh772_pos(-1, "x")
    assert mh772_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh772_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh772_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh772_int_pos(0, "x")


def test_pct_wacc_limiti():
    assert mh772_pct_wacc(0, "x") == 0.0
    assert mh772_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh772_pct_wacc(50.1, "x")


def test_pct_0_100_escl0_limiti():
    assert mh772_pct_0_100_escl0(100, "x") == 100.0
    assert mh772_pct_0_100_escl0(65.0, "x") == 65.0
    with pytest.raises(ValueError):
        mh772_pct_0_100_escl0(0, "x")
    with pytest.raises(ValueError):
        mh772_pct_0_100_escl0(100.1, "x")
    with pytest.raises(ValueError):
        mh772_pct_0_100_escl0(-1, "x")


def test_pct_0_100_limiti():
    assert mh772_pct_0_100(0, "x") == 0.0
    assert mh772_pct_0_100(100, "x") == 100.0
    assert mh772_pct_0_100(50.0, "x") == 50.0
    with pytest.raises(ValueError):
        mh772_pct_0_100(-0.1, "x")
    with pytest.raises(ValueError):
        mh772_pct_0_100(100.1, "x")


def test_pct_tolleranza_limiti():
    assert mh772_pct_tolleranza(0, "x") == 0.0
    assert mh772_pct_tolleranza(100, "x") == 100.0
    assert mh772_pct_tolleranza(10.0, "x") == 10.0
    with pytest.raises(ValueError):
        mh772_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh772_pct_tolleranza(100.1, "x")


def test_cop_pos_senza_tetto_superiore():
    assert mh772_cop_pos(3.0, "x") == 3.0
    assert mh772_cop_pos(0.5, "x") == 0.5
    assert mh772_cop_pos(8.0, "x") == 8.0
    with pytest.raises(ValueError):
        mh772_cop_pos(0, "x")
    with pytest.raises(ValueError):
        mh772_cop_pos(-1, "x")


# ---------------------------------------------------------------- fisica base
def test_q_dem_e_e_dem():
    assert mh772_q_dem(200000, 8.0) == pytest.approx(1600.0)
    assert mh772_q_dem(200000, 4.0) == pytest.approx(800.0)
    assert mh772_e_dem(200000, 1.5) == pytest.approx(300.0)
    assert mh772_e_dem(200000, 3.0) == pytest.approx(600.0)
    with pytest.raises(ValueError):
        mh772_q_dem(200000, 0)
    with pytest.raises(ValueError):
        mh772_q_dem(0, 8.0)
    with pytest.raises(ValueError):
        mh772_e_dem(200000, 0)
    with pytest.raises(ValueError):
        mh772_e_dem(200000, -1)


def test_q_hp_e_hp_e_chiller():
    assert mh772_q_hp(1600.0, 0.6) == pytest.approx(960.0)
    assert mh772_q_hp(1600.0, 0.0) == 0.0
    assert mh772_q_hp(1600.0, 1.0) == pytest.approx(1600.0)
    assert mh772_e_hp(960.0, 4.5) == pytest.approx(213.33333333333334)
    assert mh772_e_hp(0.0, 4.5) == 0.0
    assert mh772_e_chiller(300.0, 3.0) == pytest.approx(100.0)
    assert mh772_e_chiller(300.0, 4.0) == pytest.approx(75.0)
    with pytest.raises(ValueError):
        mh772_q_hp(1600.0, 1.1)
    with pytest.raises(ValueError):
        mh772_q_hp(1600.0, -0.1)
    with pytest.raises(ValueError):
        mh772_e_hp(960.0, 0.0)
    with pytest.raises(ValueError):
        mh772_e_chiller(300.0, 0.0)


def test_q_cond_q_rec_q_gas():
    assert mh772_q_cond(300.0, 100.0) == pytest.approx(400.0)
    assert mh772_q_cond(300.0, 0.0) == pytest.approx(300.0)
    assert mh772_q_rec(400.0, 0.6, 1600.0,
                       960.0) == pytest.approx(240.0)
    assert mh772_q_rec(400.0, 1.0, 1600.0,
                       960.0) == pytest.approx(400.0)
    assert mh772_q_rec(400.0, 0.0, 1600.0,
                       960.0) == 0.0
    assert mh772_q_gas_residuo(1600.0, 960.0,
                               240.0) == pytest.approx(400.0)
    assert mh772_q_gas_residuo(1600.0, 960.0, 640.0) == 0.0
    assert mh772_q_gas_residuo(1600.0, 1600.0, 0.0) == 0.0
    with pytest.raises(ValueError):
        mh772_q_rec(400.0, 1.1, 1600.0, 960.0)
    with pytest.raises(ValueError):
        mh772_q_rec(400.0, 0.6, 1600.0, 1700.0)
    with pytest.raises(ValueError):
        mh772_q_gas_residuo(1600.0, 960.0, 700.0)


def test_cap_recupero_tetto():
    """Il tetto del recupero: con quota pompa di calore 90 %
    il grezzo 400 supera il tetto 160 = 1.600 - 1.440."""
    assert mh772_q_rec(400.0, 1.0, 1600.0,
                       1440.0) == pytest.approx(160.0)
    bc = _variante(quota_hp_pct=90.0, quota_recupero_pct=100.0)
    assert bc["q_rec_mwh_anno"] == pytest.approx(160.0)
    assert bc["q_gas_residuo_mwh_anno"] == 0.0
    assert bc["q_hp_mwh_anno"] + bc["q_rec_mwh_anno"] + \
        bc["q_gas_residuo_mwh_anno"] == pytest.approx(
            bc["q_dem_mwh_anno"], rel=1e-9)


def test_bilancio_energetico_demo_e_varianti():
    """Bilancio esatto: Q_hp + Q_rec + Q_gas_residuo = Q_dem,
    nel demo e nelle varianti con tetto di recupero."""
    for bc in (demo_calcoli(),
               _variante(quota_recupero_pct=100.0),
               _variante(quota_hp_pct=100.0),
               _variante(quota_hp_pct=0.0),
               _variante(quota_hp_pct=90.0, quota_recupero_pct=100.0),
               _variante(cop_hp=2.0)):
        assert bc["q_hp_mwh_anno"] + bc["q_rec_mwh_anno"] + \
            bc["q_gas_residuo_mwh_anno"] == pytest.approx(
                bc["q_dem_mwh_anno"], rel=1e-9)


def test_c_base_c_alt():
    assert mh772_c_base(1600.0, 300.0, 0.90, 3.0, 200,
                        60) == pytest.approx(126666.66666666667)
    assert mh772_c_base(1600.0, 300.0, 1.0, 3.0, 200,
                        60) == pytest.approx(116000.0)
    assert mh772_c_alt(10000, 400.0, 0.90, 213.33333333333334,
                       100.0, 200,
                       60) == pytest.approx(99333.33333333334)
    assert mh772_c_alt(10000, 0.0, 0.90, 213.33333333333334,
                       100.0, 200,
                       60) == pytest.approx(72666.66666666667)
    with pytest.raises(ValueError):
        mh772_c_base(1600.0, 300.0, 0.0, 3.0, 200, 60)
    with pytest.raises(ValueError):
        mh772_c_base(1600.0, 300.0, 1.1, 3.0, 200, 60)
    with pytest.raises(ValueError):
        mh772_c_base(1600.0, 300.0, 0.90, 0.0, 200, 60)
    with pytest.raises(ValueError):
        mh772_c_alt(10000, 400.0, 0.90, 213.33333333333334,
                    100.0, -1, 60)


def test_co2_base_alt_evitata():
    assert mh772_co2_base(1600.0, 300.0, 0.90, 3.0, 0.25,
                          0.20) == pytest.approx(380.5555555555556)
    assert mh772_co2_alt(400.0, 0.90, 213.33333333333334,
                         100.0, 0.25,
                         0.20) == pytest.approx(167.22222222222223)
    assert mh772_co2_alt(0.0, 0.90, 213.33333333333334,
                         100.0, 0.25,
                         0.20) == pytest.approx(78.33333333333333)
    assert mh772_co2_evitata(380.5555555555556,
                             167.22222222222223) == pytest.approx(
        213.33333333333337)
    assert mh772_co2_evitata(100.0, 150.0) == pytest.approx(-50.0)
    with pytest.raises(ValueError):
        mh772_co2_base(1600.0, 300.0, 0.90, 3.0, -0.10, 0.20)


def test_risparmio_segno():
    assert mh772_risparmio(126666.66666666667, 99333.33333333334) == \
        pytest.approx(27333.33333333333)
    assert mh772_risparmio(126666.66666666667, 126666.66666666667) == 0.0
    assert mh772_risparmio(146666.66666666667, 162000.0) == \
        pytest.approx(-15333.33333333333)


def test_lco():
    assert mh772_lco_base(126666.66666666667, 200000) == pytest.approx(
        0.6333333333333333)
    assert mh772_lco_alt(99333.33333333334, 200000) == pytest.approx(
        0.4966666666666667)
    assert mh772_lco_base(126666.66666666667, 0) is None
    assert mh772_lco_alt(99333.33333333334, 0) is None
    assert mh772_lco_alt(99333.33333333334, -5) is None


def test_prezzo_pareggio_formula_zero_e_negativo():
    assert mh772_prezzo_pareggio(
        10000, 1600.0, 400.0, 0.90, 213.33333333333334,
        60) == pytest.approx(328.125)
    assert mh772_prezzo_pareggio(
        10000, 1600.0, 400.0, 0.90, 0.0,
        60) is None
    assert mh772_prezzo_pareggio(
        90000, 1600.0, 400.0, 0.90, 213.33333333333334,
        60) == pytest.approx(-46.875)
    with pytest.raises(ValueError):
        mh772_prezzo_pareggio(
            10000, 1600.0, 400.0, 0.0, 213.33333333333334, 60)


def test_prezzo_pareggio_verifica_pareggio():
    """Al prezzo di pareggio il risparmio si azzera:
    C_alt(p*) = C_base(p*) a meno del gas residuo."""
    bc = demo_calcoli()
    par = bc["prezzo_pareggio_eur_mwh"]
    d = _demo_kwargs()
    d["prezzo_el_eur_mwh"] = par
    bc_par = mh772_calcola(**d)
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
    fl = mh772_flussi(250000, 27333.333333333333, 15)
    assert len(fl) == 16
    assert fl[0] == -250000
    assert all(f == 27333.333333333333 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = demo_calcoli()
    assert bc["van"] == pytest.approx(33710.6530436028)
    assert mh772_van([-250000] + [27333.333333333333] * 15,
                     0) == pytest.approx(160000.0)
    assert mh772_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = demo_calcoli()
    assert bc["tir"] == pytest.approx(6.933416761516635)
    assert mh772_tir([-250000] + [27333.333333333333] * 15) == \
        pytest.approx(0.06933416761516635)
    tir = mh772_tir([-250000] + [27333.333333333333] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate(
                  [-250000] + [27333.333333333333] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    """Payback con cumulato >= 0: il cumulato nullo basta."""
    assert mh772_payback([-250000] + [27333.333333333333] * 15) == 10
    assert mh772_payback([-250000] + [-1000.0] * 15) is None
    assert mh772_payback([0] + [27333.333333333333] * 15) == 0
    assert mh772_payback([-100] + [50] * 2) == 2
    assert mh772_payback([-54666.666666666666] +
                         [27333.333333333333] * 2) == 2


def test_verdetto():
    assert mh772_verdetto(100.0, 250000, 10.0) == "CONVIENTE"
    assert mh772_verdetto(0.0, 250000, 10.0) == "NON_CONVIENTE"
    assert mh772_verdetto(-16289.346956, 300000,
                          10.0) == "MARGINALE"
    assert mh772_verdetto(-16289.346956, 300000,
                          0.0) == "NON_CONVIENTE"
    assert mh772_verdetto(-409154.756585, 250000,
                          10.0) == "NON_CONVIENTE"
    assert mh772_verdetto(-100.0, 0, 10.0) == "NON_CONVIENTE"
    assert mh772_verdetto(None, 250000, 10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh772_verdetto(float("nan"), 250000, 10.0)
    with pytest.raises(ValueError):
        mh772_verdetto(100.0, -1, 10.0)
    with pytest.raises(ValueError):
        mh772_verdetto(100.0, 250000, 100.1)


def test_valida_demo_ok():
    v = mh772_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("p_lpa_anno", "200000"),
                       ("p_lpa_anno", float("nan")),
                       ("p_lpa_anno", float("inf")),
                       ("p_lpa_anno", True),
                       ("prezzo_gas_eur_mwh", None),
                       ("cop_hp", "4.5")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh772_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("p_lpa_anno", 0),
                          ("p_lpa_anno", -1),
                          ("q_th_spec_kwh_per_lpa", 0),
                          ("q_th_spec_kwh_per_lpa", -1),
                          ("e_el_spec_kwh_per_lpa", 0),
                          ("e_el_spec_kwh_per_lpa", -1),
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
        assert mh772_valida(**d)["valido"] is False


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
    assert mh772_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    assert mh772_valida(**d)["valido"] is True


def test_valida_non_controlla_risparmio_calcola_neppure():
    """La validazione input NON controlla il risparmio
    (e' un esito, non un range) e in questa tab
    nemmeno mh772_calcola lo controlla: con prezzo
    elettricita' 400 EUR/MWh il caso resta CALCOLABILE."""
    d = _demo_kwargs()
    d["prezzo_el_eur_mwh"] = 400
    assert mh772_valida(**d)["valido"] is True
    bc = _variante(prezzo_el_eur_mwh=400)
    assert bc["valid"] is True
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["flussi"]
    assert bc["payback"] is None


def test_demo_dict():
    d = mh772_demo()
    assert d["p_lpa_anno"] == 200000
    assert d["q_th_spec_kwh_per_lpa"] == 8.0
    assert d["e_el_spec_kwh_per_lpa"] == 1.5
    assert d["eta_caldaia_pct"] == 90.0
    assert d["cop_base"] == 3.0
    assert d["cop_hp"] == 4.5
    assert d["quota_hp_pct"] == 60.0
    assert d["quota_recupero_pct"] == 60.0
    assert d["prezzo_el_eur_mwh"] == 200
    assert d["prezzo_gas_eur_mwh"] == 60
    assert d["om_eur_anno"] == 10000
    assert d["capex_eur"] == 250000
    assert d["f_el_t_per_mwh"] == 0.25
    assert d["f_gas_t_per_mwh"] == 0.20
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    """Tutti gli output numerici demo a tolleranza
    1e-6 relativa (richiesta del brief): confronto
    contro demo_calcoli(), con valori da ricalcolo
    indipendente (vedi docstring: NON i valori del
    brief per CO2 alt/evitata e TIR)."""
    bc = demo_calcoli()
    attesi = {
        "q_dem_mwh_anno": 1600.0,
        "e_dem_mwh_anno": 300.0,
        "q_hp_mwh_anno": 960.0,
        "q_cond_mwh_anno": 400.0,
        "q_rec_mwh_anno": 240.0,
        "q_gas_residuo_mwh_anno": 400.0,
        "e_hp_mwh_anno": 213.33333333333334,
        "e_chiller_residuo_mwh_anno": 100.0,
        "e_alt_mwh_anno": 313.33333333333337,
        "c_base_eur_anno": 126666.66666666667,
        "c_alt_eur_anno": 99333.33333333334,
        "co2_base_t_anno": 380.5555555555556,
        "co2_alt_t_anno": 167.22222222222223,
        "risparmio_eur_anno": 27333.33333333333,
        "co2_evitata_t_anno": 213.33333333333337,
        "lco_base_eur_t": 0.6333333333333333,
        "lco_alt_eur_t": 0.4966666666666667,
        "van": 33710.6530436028,
        "tir": 6.933416761516635,
        "prezzo_pareggio_eur_mwh": 328.125,
    }
    for chiave, atteso in attesi.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert got == pytest.approx(atteso, rel=1e-6), chiave
    assert bc["payback"] == 10
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_demo_calcoli_fisica():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["q_dem_mwh_anno"] == pytest.approx(1600.0)
    assert bc["e_dem_mwh_anno"] == pytest.approx(300.0)
    assert bc["q_hp_mwh_anno"] == pytest.approx(960.0)
    assert bc["q_cond_mwh_anno"] == pytest.approx(400.0)
    assert bc["q_rec_mwh_anno"] == pytest.approx(240.0)
    assert bc["q_gas_residuo_mwh_anno"] == pytest.approx(400.0)
    assert bc["e_hp_mwh_anno"] == pytest.approx(213.33333333333334)
    assert bc["e_chiller_residuo_mwh_anno"] == pytest.approx(100.0)
    assert bc["co2_evitata_t_anno"] == pytest.approx(213.33333333333337)


def test_demo_calcoli_economia():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(126666.66666666667)
    assert bc["c_alt_eur_anno"] == pytest.approx(99333.33333333334)
    assert bc["risparmio_eur_anno"] == pytest.approx(27333.33333333333)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(328.125)


def test_demo_calcoli_finanza():
    bc = demo_calcoli()
    assert bc["lco_base_eur_t"] == pytest.approx(0.6333333333333333)
    assert bc["lco_alt_eur_t"] == pytest.approx(0.4966666666666667)
    assert bc["van"] == pytest.approx(33710.6530436028)
    assert bc["tir"] == pytest.approx(6.933416761516635)
    assert bc["payback"] == 10
    assert bc["verdetto"] == "CONVIENTE"


def test_demo_flussi_e_cumulato():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -250000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(27333.333333333333)
               for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -250000
    assert righe.iloc[9]["Cumulato (EUR)"] == pytest.approx(-4000.0)
    assert righe.iloc[10]["Cumulato (EUR)"] == pytest.approx(
        23333.33333333333)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(160000.0)
    assert righe.iloc[15]["Flusso (EUR/anno)"] == pytest.approx(
        27333.333333333333)


def test_demo_tabella_righe():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Produzione alcol puro (LPA/anno)"] == pytest.approx(
        200000.0)
    assert mappa["Domanda termica (MWh/anno)"] == pytest.approx(1600.0)
    assert mappa["Domanda di freddo (MWh/anno)"] == pytest.approx(300.0)
    assert mappa["Calore da pompa di calore (MWh/anno)"] == pytest.approx(
        960.0)
    assert mappa["Calore recuperato (MWh/anno)"] == pytest.approx(240.0)
    assert mappa["Calore residuo da caldaia (MWh/anno)"] == pytest.approx(
        400.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(
        99333.33333333334)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(
        27333.33333333333)
    assert mappa["Payback (anni)"] == 10
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Prezzo elettricita' di pareggio (EUR/MWh)"] == \
        pytest.approx(328.125)


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
        bc["p_lpa_anno"] * bc["q_th_spec_kwh_per_lpa"] / 1000.0)
    assert bc["e_dem_mwh_anno"] == pytest.approx(
        bc["p_lpa_anno"] * bc["e_el_spec_kwh_per_lpa"] / 1000.0)
    assert bc["co2_base_t_anno"] - bc["co2_alt_t_anno"] == \
        pytest.approx(bc["co2_evitata_t_anno"])
    assert bc["c_base_eur_anno"] / bc["p_lpa_anno"] == \
        pytest.approx(bc["lco_base_eur_t"])
    assert bc["c_alt_eur_anno"] / bc["p_lpa_anno"] == \
        pytest.approx(bc["lco_alt_eur_t"])


def test_demo_contro_riconteggio_indipendente():
    p, qsp, esp = 200000, 8.0, 1.5
    ecal, copb, coph = 90.0, 3.0, 4.5
    qhp, qrec = 60.0, 60.0
    pel, pg, om, cx = 200, 60, 10000, 250000
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
    assert bc["payback"] == 10
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_recupero_cento():
    """Recupero al 100 % sul demo: il grezzo 400 resta
    sotto il tetto 640, quindi Q_rec = 400 e il calore
    residuo scende a 240."""
    bc = _variante(quota_recupero_pct=100.0)
    assert bc["valid"] is True
    assert bc["q_rec_mwh_anno"] == pytest.approx(400.0)
    assert bc["q_gas_residuo_mwh_anno"] == pytest.approx(240.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(88666.666667)
    assert bc["risparmio_eur_anno"] == pytest.approx(38000.0)
    assert bc["van"] == pytest.approx(144427.005451)
    assert bc["tir"] == pytest.approx(12.655897)
    assert bc["payback"] == 7
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(378.125)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_quota_hp_zero():
    """Quota pompa di calore zero: E_hp zero, pareggio
    None, risparmio solo da recupero, VAN negativa
    oltre la tolleranza."""
    bc = _variante(quota_hp_pct=0)
    assert bc["valid"] is True
    assert bc["q_hp_mwh_anno"] == 0.0
    assert bc["e_hp_mwh_anno"] == 0.0
    assert bc["q_rec_mwh_anno"] == pytest.approx(240.0)
    assert bc["q_gas_residuo_mwh_anno"] == pytest.approx(1360.0)
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["risparmio_eur_anno"] == pytest.approx(6000.0)
    assert bc["van"] == pytest.approx(-187722.051771)
    assert bc["tir"] == pytest.approx(-10.695776)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_quota_hp_cento():
    """Quota pompa di calore 100 %: tutto il calore
    dalla pompa, recupero zero (tetto zero), residuo
    zero."""
    bc = _variante(quota_hp_pct=100.0)
    assert bc["valid"] is True
    assert bc["q_hp_mwh_anno"] == pytest.approx(1600.0)
    assert bc["q_rec_mwh_anno"] == 0.0
    assert bc["q_gas_residuo_mwh_anno"] == 0.0
    assert bc["e_hp_mwh_anno"] == pytest.approx(355.555556)
    assert bc["risparmio_eur_anno"] == pytest.approx(25555.555556)
    assert bc["van"] == pytest.approx(15257.927642)
    assert bc["tir"] == pytest.approx(5.889732)
    assert bc["payback"] == 10
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(271.875)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_marginale_capex_alto():
    """Fascia MARGINALE: CAPEX 300.000 EUR, VAN
    negativa entro la tolleranza del 10 % del
    CAPEX (30.000 EUR)."""
    bc = _variante(capex_eur=300000)
    assert bc["valid"] is True
    assert bc["van"] == pytest.approx(-16289.346956)
    assert bc["tir"] == pytest.approx(4.185421)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"
    bc0 = _variante(capex_eur=300000, tolleranza_pct=0)
    assert bc0["verdetto"] == "NON_CONVIENTE"
    assert bc0["van"] == pytest.approx(-16289.346956)


def test_variante_non_conviente_prezzo_el_alto():
    """NON_CONVIENTE: prezzo elettricita' 400 EUR/MWh,
    sopra il pareggio 328,125: risparmio negativo,
    VAN negativa oltre la tolleranza, payback mai."""
    bc = _variante(prezzo_el_eur_mwh=400)
    assert bc["valid"] is True
    assert bc["c_base_eur_anno"] == pytest.approx(146666.666667)
    assert bc["c_alt_eur_anno"] == pytest.approx(162000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-15333.333333)
    assert bc["van"] == pytest.approx(-409154.756585)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["flussi"]


def test_variante_non_conviente_cop_hp_basso():
    """NON_CONVIENTE per COP basso: COP pompa di
    calore 2,0, elettricita' pompa salita a 480."""
    bc = _variante(cop_hp=2.0)
    assert bc["valid"] is True
    assert bc["e_hp_mwh_anno"] == pytest.approx(480.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-26000.0)
    assert bc["van"] == pytest.approx(-519871.108993)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_wacc_zero():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(160000.0)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    """Payback regola >=: con CAPEX nullo il payback e' 0,
    non 1 (all'anno 0 il cumulato e' gia' zero)."""
    bc = _variante(capex_eur=0)
    assert bc["capex_eur"] == 0
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(283710.653044)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_vita_diversa():
    bc = _variante(vita_anni=20)
    assert len(bc["flussi"]) == 21
    assert bc["van"] == pytest.approx(90633.749363)
    assert bc["tir"] == pytest.approx(8.972686)
    assert bc["payback"] == 10
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_co2_evitata_negativa_non_degenere():
    """CO2 evitata negativa NON degenere: fattore
    elettrico 1,0 e fattore gas zero -> evitata
    -213,333333 t/anno, caso calcolabile e CONVIENTE."""
    bc = _variante(f_el_t_per_mwh=1.0, f_gas_t_per_mwh=0.0)
    assert bc["valid"] is True
    assert bc["co2_base_t_anno"] == pytest.approx(100.0)
    assert bc["co2_alt_t_anno"] == pytest.approx(313.333333)
    assert bc["co2_evitata_t_anno"] == pytest.approx(-213.333333)
    assert bc["risparmio_eur_anno"] == pytest.approx(27333.333333333333)
    assert bc["verdetto"] == "CONVIENTE"


# ---------------------------------------------------------------- degenere
def test_degenere_produzione_zero_sollevela():
    """Caso degenere richiesto dal brief: P = 0
    solleva ValueError."""
    with pytest.raises(ValueError):
        _variante(p_lpa_anno=0)


def test_degenere_verdetto_non_calcolabile_van_tir_payback_none():
    """Nel regime degenere non esiste alcun calcolo:
    calcola solleva ValueError, quindi nessuna VAN,
    nessuna TIR e nessun payback vengono prodotti
    (sono None per assenza); il verdetto per VAN
    None e' NON_CALCOLABILE."""
    with pytest.raises(ValueError):
        _variante(p_lpa_anno=0)
    with pytest.raises(ValueError):
        _variante(cop_hp=0)
    assert mh772_verdetto(None, 250000, 10.0) == "NON_CALCOLABILE"
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
        assert mh772_valida(**d)["valido"] is False


def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"p_lpa_anno": 0}, {"p_lpa_anno": -1},
               {"q_th_spec_kwh_per_lpa": 0},
               {"q_th_spec_kwh_per_lpa": -1},
               {"e_el_spec_kwh_per_lpa": 0},
               {"e_el_spec_kwh_per_lpa": -1},
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
        assert mh772_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"p_lpa_anno": "200000"},
               {"p_lpa_anno": float("nan")},
               {"prezzo_gas_eur_mwh": float("inf")},
               {"capex_eur": True},
               {"cop_hp": "4.5"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh772_valida(**d)["valido"] is False


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
    assert mh772_co2_evitata(100.0, 150.0) == pytest.approx(-50.0)


def test_verdetto_non_calcolabile_solo_van_none():
    assert mh772_verdetto(None, 250000, 10.0) == "NON_CALCOLABILE"
    assert demo_calcoli()["verdetto"] != "NON_CALCOLABILE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = demo_calcoli()
    testo = mh772_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert "q_dem_mwh_anno;1600.0" in testo
    assert "e_dem_mwh_anno;300.0" in testo
    assert "q_hp_mwh_anno;960.0" in testo
    assert "q_rec_mwh_anno;240.0" in testo
    assert "q_gas_residuo_mwh_anno;400.0" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "prezzo_pareggio_eur_mwh" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = demo_calcoli()
    testo = mh772_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"q_hp_mwh_anno;{bc['q_hp_mwh_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = demo_calcoli()
    testo = mh772_csv(bc, _demo_kwargs())
    for chiave in _demo_kwargs():
        assert f"{chiave};" in testo


def test_monotonia_prezzo_gas():
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(prezzo_gas_eur_mwh=70)["risparmio_eur_anno"]
    basso = _variante(prezzo_gas_eur_mwh=50)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(13333.333333333333)
    assert base - basso == pytest.approx(13333.333333333333)


def test_monotonia_prezzo_el():
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(prezzo_el_eur_mwh=210)["risparmio_eur_anno"]
    basso = _variante(prezzo_el_eur_mwh=190)["risparmio_eur_anno"]
    assert alto < base < basso
    assert base - alto == pytest.approx(2133.333333333333)
    assert basso - base == pytest.approx(2133.333333333333)


def test_monotonia_quota_hp():
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(quota_hp_pct=70)["risparmio_eur_anno"]
    basso = _variante(quota_hp_pct=50)["risparmio_eur_anno"]
    assert alto > base > basso


def test_demo_deterministica_due_chiamate():
    a = demo_calcoli()
    b = demo_calcoli()
    assert a["van"] == b["van"]
    assert a["flussi"] == b["flussi"]
    assert a["tir"] == b["tir"]


def test_demo_chiavi_attese():
    assert set(mh772_demo().keys()) == {
        "p_lpa_anno",
        "q_th_spec_kwh_per_lpa", "e_el_spec_kwh_per_lpa",
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
    return ["mh" + "77" + "1", "st" + "77" + "1",
            "tab" + "77" + "1", "w" + "77" + "2_",
            "mh" + "77" + "0", "st" + "77" + "0",
            "tab" + "77" + "0", "w" + "77" + "1_"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w773_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w773_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab772:")


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w773_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w773_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st772_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert "key=f" not in src and 'key = f' not in src
    assert "st.stop()" in src
    # guard degenere prima di KPI / grafico / tabella / CSV
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w773_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def772[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w773_ui.py")
        usate = set(re.findall(r'_def772\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 17
        assert usate == {
            "p_lpa_anno",
            "q_th_spec_kwh_per_lpa", "e_el_spec_kwh_per_lpa",
            "eta_caldaia_pct",
            "cop_base", "cop_hp",
            "quota_hp_pct", "quota_recupero_pct",
            "prezzo_el_eur_mwh", "prezzo_gas_eur_mwh",
            "om_eur_anno", "capex_eur",
            "f_el_t_per_mwh", "f_gas_t_per_mwh",
            "wacc_pct", "vita_anni", "tolleranza_pct"}
        assert usate <= set(mh772_demo().keys())


def test_ui_chiavi_demo_coerenti():
    """Ogni _def772[...] letto dalla UI esiste nel dict demo:
    sweep anti-KeyError a render (lezione dello sweep chiavi demo vs UI)."""
    src = _leggi("w773_ui.py")
    usate = set(re.findall(r'_def772\["([^"]+)"\]', src))
    assert usate
    assert len(usate) == 17
    assert usate <= set(mh772_demo().keys())


def test_ui_riferisce_solo_helper_nuovi():
    src = _leggi("w773_ui.py")
    usati = set(re.findall(r'\b(mh\d+_\w+)\b', src))
    assert usati
    assert all(u.startswith("mh772_") for u in usati)


@pytest.mark.parametrize("e_el_spec,atteso", [
    (1.5, 300.0),
    (3.0, 600.0),
    (0.75, 150.0),
])
def test_e_dem_parametrizzato(e_el_spec, atteso):
    assert mh772_e_dem(200000, e_el_spec) == pytest.approx(atteso)


@pytest.mark.parametrize("campo,valore", [
    ("p_lpa_anno", 0), ("p_lpa_anno", -3),
    ("q_th_spec_kwh_per_lpa", 0), ("q_th_spec_kwh_per_lpa", -1),
    ("e_el_spec_kwh_per_lpa", 0), ("e_el_spec_kwh_per_lpa", -1),
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
    assert mh772_valida(**d)["valido"] is False


@pytest.mark.parametrize("campo,valore", [
    ("p_lpa_anno", 0), ("p_lpa_anno", -3),
    ("q_th_spec_kwh_per_lpa", 0), ("q_th_spec_kwh_per_lpa", -1),
    ("e_el_spec_kwh_per_lpa", 0), ("e_el_spec_kwh_per_lpa", -1),
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
        mh772_calcola(**d)


def test_df_tabella_valori_demo_selezionati():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Produzione alcol puro (LPA/anno)"] == 200000.0
    assert mappa["Domanda termica (MWh/anno)"] == pytest.approx(1600.0)
    assert mappa["Calore recuperato (MWh/anno)"] == pytest.approx(240.0)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(
        27333.333333333333)
    assert mappa["Verdetto"] == "CONVIENTE"


def test_lco_alt_minore_di_lco_base_demo():
    bc = demo_calcoli()
    assert bc["lco_alt_eur_t"] < bc["lco_base_eur_t"]
    assert bc["lco_base_eur_t"] - bc["lco_alt_eur_t"] == pytest.approx(
        0.13666666666666665)
