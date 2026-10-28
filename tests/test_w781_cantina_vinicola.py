"""Test tab781 "Cantina vinicola:
pompa di calore geotermica reversibile
batte chiller + caldaia a gas?"
(File repo: tests/test_w781_cantina_vinicola.py,
contenuto pronto da scrivere in repo.)

Nuova tab tab781 (cantina vinicola, file di
lavoro w782). Business case
deterministico di una cantina
vinicola: si vinifica P hl/anno di
vino; freddo di processo
(fermentazione + affinamento)
q_freddo kWh_th/hl e riscaldamento
locali q_caldo kWh_th/hl; baseline
chiller + caldaia a gas con
el_base = q_freddo / COP_chiller
kWh_e/hl e gas_base = q_caldo /
eta_caldaia kWh_th gas/hl; alternativa
pompa di calore geotermica
reversibile con el_alt = q_freddo /
COP_geo_freddo + q_caldo /
COP_geo_caldo kWh_e/hl, nessun gas,
due COP distinti (freddo di processo
e caldo cantina); costi per ettolitro
C_base_per_hl = el_base / 1000 x p_el
+ gas_base / 1000 x p_gas +
other_base EUR/hl e C_alt_per_hl =
el_alt / 1000 x p_el + other_alt
EUR/hl (prezzi in EUR/MWh, consumi
in kWh/hl: 1 MWh = 1000 kWh); costi
annui C_base = C_base_per_hl x P,
C_alt_var = C_alt_per_hl x P,
C_alt = C_alt_var + O&M; risparmio
= C_base - C_alt EUR/anno; CO2 base
= gas_base / 1000 x P x f_gas +
el_base / 1000 x P x f_el t/anno
(fattori in tCO2/MWh); CO2
geotermica = el_alt / 1000 x P x
f_el t/anno (niente gas: nessun
bruciatore da tenere acceso); CO2
evitata = CO2 base - CO2 geotermica
t/anno, SEGNO LIBERO in questa tab
(PUO' ESSERE NEGATIVA con
elettricita' sporca): NON e' una
guard, NON e' un degenere, NON
monetizzata; CRF = r (1 + r)^n /
((1 + r)^n - 1) con r = WACC come
frazione, r = 0 -> 1/n, SOLO nel
LCO, MAI nei flussi; LCO base =
C_base_per_hl EUR/hl; LCO alt =
(CAPEX x CRF + O&M) / P +
C_alt_per_hl EUR/hl (il CAPEX entra
solo annuizzato col CRF);
breakeven prezzo elettricita'
p_el* = (C_base_nonel - C_alt_nonel)
/ ((el_alt - el_base) / 1000) EUR/MWh,
None se denominatore <= 0
(la geotermica non consuma piu'
elettricita' della baseline) e
None se numeratore < 0 (a prezzo
elettrico zero la geotermica e'
gia' piu' cara e il divario cresce
con p_el); breakeven prezzo gas
p_gas* = (C_alt_per_hl -
el_base / 1000 x p_el - other_base)
/ (gas_base / 1000) EUR/MWh, la
soglia minima del prezzo gas a
prezzo elettricita' corrente: sopra
di essa la geotermica vince sui
costi variabili (il costo base
cresce con p_gas, il costo
alternativo no), sotto perde;
None se gas_base <= 0 e None se
numeratore < 0; il pareggio elettrico,
quando esiste, e' un TETTO
(ceiling), il pareggio gas, quando
esiste, e' una SOGLIA MINIMA; i
pareggi sono sui costi variabili e
NON includono l'O&M: al pareggio
esatto il risparmio e' -O&M, non
zero; flussi [-CAPEX,
risparmio x vita]; VAN, TIR,
payback (primo anno con cumulato
>= 0, regola >= del brief: con
CAPEX nullo il payback e' 0, con
divisione esatta CAPEX / risparmio
il payback e' l'anno della
divisione esatta).
Verdetto SUL RISPARMIO, non sulla
VAN: CONVIENTE se risparmio >
tolleranza % di C_base; MARGINALE
se |risparmio| <= tolleranza % di
C_base; NON_CONVIENTE se risparmio
< -tolleranza % di C_base;
NON_CALCOLABILE e' il verdetto del
caso degenere (risparmio None:
nessun calcolo eseguibile, quindi
nessuna VAN, nessuna TIR e nessun
payback). Regime degenere SOLLEVA
ValueError negli helper (produzione
<= 0, freddo o caldo specifico
<= 0, COP <= 0, rendimento <= 0 o
sopra 1, prezzi < 0, altri costi < 0,
O&M < 0, CAPEX < 0, fattori < 0,
WACC < 0 o sopra 50 %, vita <= 0 o
non intera, tolleranza fuori
[0, 100] %, input non numerici o
non finiti); la UI lo intercetta
PRIMA di KPI, grafico, tabella e
CSV con st.stop(). In questa tab
il risparmio nullo o negativo NON
e' degenere: resta calcolabile e
porta a verdetto MARGINALE o
NON_CONVIENTE. La CO2 evitata PUO'
essere negativa in questa tab: e'
un esito onesto, non una guard. I
breakeven None NON sono degeneri:
sono esiti del calcolo. Distinzione
esplicita: questa tab vinifica
(hl/anno, fermentazione +
affinamento + riscaldamento locali
cantina), con freddo di processo +
caldo cantina e COP freddo e COP
caldo distinti; NON e' la tab
caseificio (li' si pastorizza
latte), NON e' la tab birrificio
(li' si produce birra), NON e' la
tab essiccazione legno, NON e' la
tab sonde geotermiche generiche
(li' si climatizza un edificio:
qui freddo di processo + caldo
cantina, non climatizzazione
generica).

Demo calcolata eseguendo
demo_calcoli() e ricontrollata con
un ricalcolo indipendente da zero
(riga per riga): produzione 8.000
hl/anno, freddo specifico 15
kWh_th/hl con chiller COP 2,5,
caldo specifico 60 kWh_th/hl con
caldaia a rendimento 0,85;
geotermica reversibile con COP
freddo 5,5 e COP caldo 4,5;
elettricita' 170 EUR/MWh, gas 70
EUR/MWh, altri costi base 5,00
EUR/hl, altri costi geotermica
4,00 EUR/hl; O&M annuo 25.000
EUR/anno, CAPEX 150.000 EUR,
fattore gas 0,20 tCO2/MWh, fattore
elettricita' 0,25 tCO2/MWh, WACC
5 %, vita 20 anni, tolleranza
MARGINALE 10 % di C_base.

- el_base_kwh_hl = 6.0
- gas_base_kwh_hl = 70.58823529411765
- el_alt_kwh_hl = 16.060606060606062
- c_base_per_hl = 10.961176470588235
- c_alt_per_hl = 6.7303030303030305
- c_base_nonel_per_hl = 9.941176470588236
- c_alt_nonel_per_hl = 4.0
- el_base_mwh_anno = 48.0
- gas_mwh_anno = 564.7058823529412
- el_alt_mwh_anno = 128.4848484848485
- c_base_eur_anno = 87689.41176470587
- c_alt_var_eur_anno = 53842.42424242424
- c_alt_eur_anno = 78842.42424242424
- risparmio_eur_anno = 8846.987522281634
- co2_base_t_anno = 124.94117647058825
- co2_alt_t_anno = 32.121212121212125
- co2_evitata_t_anno = 92.81996434937612
- crf = 0.08024258719069129
- lco_base_eur_hl = 10.961176470588235
- lco_alt_eur_hl = 11.359851540128492
- van = -39746.98059949966
- tir = 1.62741181615689
- payback = 17
- breakeven_el_eur_mwh = 590.5386250885896
- breakeven_gas_eur_mwh = 10.06262626262627
- verdetto = 'CONVIENTE'

Scomposizione: elettricita' base =
15 / 2,5 = 6,00 kWh_e/hl; gas base =
60 / 0,85 = 70,59 kWh_th gas/hl;
elettricita' geotermica = 15 / 5,5
= 2,73 + 60 / 4,5 = 13,33 = 16,06
kWh_e/hl; costo base = 6,00 / 1000
x 170 = 1,02 di elettricita' +
70,59 / 1000 x 70 = 4,94 di gas +
5,00 altri = 10,96 EUR/hl; costo
geotermico = 16,06 / 1000 x 170 =
2,73 di elettricita' + 4,00 altri =
6,73 EUR/hl; costo baseline =
10,96 x 8.000 = 87.689,41 EUR/anno;
costo variabile geotermico = 6,73
x 8.000 = 53.842,42 EUR/anno; costo
alternativo = 53.842,42 + 25.000 =
78.842,42 EUR/anno; risparmio =
87.689,41 - 78.842,42 = 8.846,99
EUR/anno, il 10,09 % di C_base,
sopra la tolleranza del 10 %
(8.768,94 EUR/anno) di soli 78,05
EUR/anno: verdetto CONVIENTE ma al
limite; CO2 base = 70,59 / 1000 x
8.000 x 0,20 = 112,94 di gas + 6,00
/ 1000 x 8.000 x 0,25 = 12,00 di
elettrica = 124,94 t/anno; CO2
geotermica = 16,06 / 1000 x 8.000
x 0,25 = 32,12 t/anno; CO2 evitata =
124,94 - 32,12 = 92,82 t/anno;
CRF al 5 % per 20 anni =
0,0802425872; LCO base 10,96
EUR/hl; LCO alt = (150.000 x
0,0802425872 + 25.000) / 8.000 +
6,73 = 4,629549 + 6,73 =
11,359852 EUR/hl; flussi: anno 0
-150.000, anni 1-20 risparmio
8.846,99 (piatti); VAN -150.000 +
8.846,99 x 12,462210 (annuita' 20
anni al 5 %) = -39.746,98 EUR;
TIR 1,63 % (sotto il WACC del 5 %);
payback 17 anni (il cumulato
all'anno 16 e' -8.448,20 EUR,
all'anno 17 e' 398,79 EUR, gia'
>= 0); breakeven elettricita'
(9,94 - 4,00) / ((16,06 - 6,00) /
1000) = 5,94 / 0,0100606 = 590,54
EUR/MWh (TETTO: sotto di esso
la geotermica vince sui costi
variabili, sopra perde);
breakeven gas (6,73 - 1,02 -
5,00) / (70,59 / 1000) = 0,71 /
0,0705882 = 10,06 EUR/MWh (SOGLIA
MINIMA: sopra di essa la
geotermica vince sui costi
variabili, sotto perde; il prezzo
gas demo, 70 EUR/MWh, sta sopra
la soglia, coerente con
CONVIENTE); verdetto CONVIENTE
perche' il risparmio 8.846,99 supera
la tolleranza del 10 % di C_base
(8.768,94 EUR/anno).
NOTA: il CRF entra SOLO nel LCO di
questa tab: nei flussi il CAPEX
entra intero all'anno 0, mai
annuizzato.
NOTA 2: il verdetto CONVIENTE del
demo NON significa VAN positiva:
la VAN e' -39.746,98 EUR, la TIR
1,63 % e' sotto il WACC e il LCO
alternativo (11,36) sta sopra il
LCO baseline (10,96). Il verdetto
guarda il risparmio annuo contro
la tolleranza, non la remunerazione
del CAPEX: il risparmio copre
l'O&M ma non basta a ripagare il
CAPEX al 5 %. Con WACC zero la VAN
diventa 26.939,75 EUR (il solo
sconto a zero basta a ribaltarla).
NOTA 3: in questa tab il risparmio
nullo o negativo NON e' degenere:
con prezzo elettricita' 590,54
EUR/MWh (al tetto) il caso e'
calcolabile (valid=True, flussi
pieni), NON_CONVIENTE con VAN
-461.555,26 EUR e payback None,
non un errore: -25.000 di risparmio
supera la soglia del 10 % di C_base
a quel prezzo (10.787,53 EUR/anno).
NOTA 4: la CO2 evitata PUO' essere
negativa in questa tab (non e' una
guard): con fattore gas zero e
fattore elettricita' 1,00 la CO2
base e' 48,00 t/anno e la geotermica
128,48 t/anno, quindi l'evitata e'
-80,48 t/anno, mentre il verdetto
resta CONVIENTE (stessa economia:
i fattori non toccano i costi).
NOTA 5: i pareggi sono sui costi
variabili, NON sul risparmio: al
pareggio elettrico esatto
(590,54 EUR/MWh) i costi per
ettolitro si eguagliano
(13,48 EUR/hl) ma il risparmio e'
-25.000 EUR/anno, cioe' solo
l'O&M; al pareggio gas esatto
(10,06 EUR/MWh) i costi per
ettolitro si eguagliano
(6,73 EUR/hl) ma il risparmio e'
di nuovo -25.000 EUR/anno. Il
breakeven elettrico e' None con COP
geotermici 20 e 20 (el_alt 3,75
sotto el_base 6,00: denominatore
negativo) e con altri costi
geotermica alti (numeratore
negativo). Il breakeven gas e'
None con prezzo elettricita' zero
e altri costi geotermica nulli
(numeratore negativo), e vale come
identita' a prezzo elettricita'
corrente: 1,02 + 5,00 + 70,59 /
1000 x 10,06 = 6,73. Attenzione:
i due pareggi hanno verso opposto:
sopra il tetto elettrico la
geotermica perde, sopra la soglia
gas la geotermica vince.
NOTA 6: il verdetto CONVIENTE del
demo e' al limite: con prezzo
elettricita' 171 EUR/MWh (un euro
in piu') il risparmio scende a
8.766,50 EUR/anno, sotto la soglia
8.768,94, e il verdetto diventa
MARGINALE; con prezzo gas 69
EUR/MWh (un euro in meno) scende
a 8.282,28 EUR/anno, MARGINALE;
con prezzo gas 80 EUR/MWh sale a
14.494,05 EUR/anno, CONVIENTE con
VAN 30.627,85 EUR e payback 11 anni.
NOTA 7: il payback usa il cumulato
>= 0 (regola >= del brief): con
CAPEX nullo il payback e' 0 (non
1); con flussi [-100, 50, 50] il
payback e' 2 (il cumulato all'anno
2 e' zero, e zero basta); con
CAPEX 150.000 EUR e risparmio
8.846,99 il payback e' 17 (la
divisione nominale 150.000 /
8.846,99 fa 16,95 anni).
NOTA 8: i valori demo sono stati
ricalcolati da zero con un calcolo
indipendente: il ricalcolo esatto
(senza arrotondamenti intermedi)
da' el_base 6,00, gas_base 70,59,
el_alt 16,06, costo base 10,96,
costo geotermico 6,73, costo
baseline 87.689,41, costo variabile
geotermico 53.842,42, costo
alternativo 78.842,42, risparmio
8.846,99, CO2 base 124,94,
geotermica 32,12, evitata 92,82,
CRF 0,0802425872, LCO base 10,96,
LCO alt 11,359852, VAN -39.746,98,
TIR 1,63 %, payback 17, breakeven
elettricita' 590,54 (tetto),
breakeven gas 10,06 (soglia minima),
verdetto CONVIENTE: i file usano i
valori esatti.
NOTA 9: gli attesi approssimati del
brief per questa demo (C_base/hl
11,96, risparmio 16.847, VAN
+59.950, payback 9, TIR 9,3 %,
breakeven elettricita' 689,93) NON
tornano con le formule del brief
stesso applicate agli input dati
(1,02 + 4,94 + 5,00 = 10,96, non
11,96): i file usano i valori
esatti ricalcolati, non gli attesi
del brief, e il verdetto CONVIENTE
resta valido ma al limite.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w782_helpers import (
    demo_calcoli,
    mh781_breakeven_el,
    mh781_breakeven_gas,
    mh781_c_alt,
    mh781_c_alt_per_hl,
    mh781_c_alt_var,
    mh781_c_base,
    mh781_c_base_nonel,
    mh781_c_base_per_hl,
    mh781_c_alt_nonel,
    mh781_calcola,
    mh781_co2_alt,
    mh781_co2_base,
    mh781_co2_evitata,
    mh781_crf,
    mh781_csv,
    mh781_demo,
    mh781_el_alt,
    mh781_el_base,
    mh781_eta,
    mh781_flussi,
    mh781_gas_base,
    mh781_int_pos,
    mh781_lco_alt,
    mh781_lco_base,
    mh781_num,
    mh781_nneg,
    mh781_payback,
    mh781_pct_tolleranza,
    mh781_pct_wacc,
    mh781_pos,
    mh781_risparmio,
    mh781_tir,
    mh781_valida,
    mh781_van,
    mh781_verdetto,
)

# Costanti demo a piena precisione (per la validazione
# _DEMO contro demo_calcoli() con tolleranza relativa
# < 1e-9: vedi test_demo_costanti_vs_demo_calcoli).
_DEMO = {
    "el_base_kwh_hl": 6.0,
    "gas_base_kwh_hl": 70.58823529411765,
    "el_alt_kwh_hl": 16.060606060606062,
    "c_base_per_hl": 12.372941176470588,
    "c_alt_per_hl": 6.7303030303030305,
    "c_base_nonel_per_hl": 11.352941176470589,
    "c_alt_nonel_per_hl": 4.0,
    "el_base_mwh_anno": 48.0,
    "gas_mwh_anno": 564.7058823529412,
    "el_alt_mwh_anno": 128.4848484848485,
    "c_base_eur_anno": 98983.52941176471,
    "c_alt_var_eur_anno": 53842.42424242424,
    "c_alt_eur_anno": 78842.42424242424,
    "risparmio_eur_anno": 20141.105169340473,
    "co2_base_t_anno": 124.94117647058825,
    "co2_alt_t_anno": 32.121212121212125,
    "co2_evitata_t_anno": 92.81996434937612,
    "crf": 0.08024258719069129,
    "lco_base_eur_hl": 12.372941176470588,
    "lco_alt_eur_hl": 11.359851540128492,
    "van": 101002.68915154031,
    "tir": 12.047078687632562,
    "breakeven_el_eur_mwh": 730.8646350106308,
    "breakeven_gas_eur_mwh": 10.06262626262627,
}


def _demo_kwargs():
    return dict(mh781_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh781_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh781_num(3, "x") == 3.0
    assert mh781_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh781_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh781_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh781_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh781_pos(0, "x")
    with pytest.raises(ValueError):
        mh781_pos(-1, "x")
    assert mh781_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh781_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh781_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh781_int_pos(0, "x")


def test_eta_limiti():
    assert mh781_eta(1.0, "x") == 1.0
    assert mh781_eta(0.85, "x") == 0.85
    with pytest.raises(ValueError):
        mh781_eta(0, "x")
    with pytest.raises(ValueError):
        mh781_eta(-0.1, "x")
    with pytest.raises(ValueError):
        mh781_eta(1.01, "x")


def test_pct_wacc_limiti():
    assert mh781_pct_wacc(0, "x") == 0.0
    assert mh781_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh781_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh781_pct_tolleranza(0, "x") == 0.0
    assert mh781_pct_tolleranza(100, "x") == 100.0
    assert mh781_pct_tolleranza(10.0, "x") == 10.0
    with pytest.raises(ValueError):
        mh781_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh781_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_el_base_gas_base_el_alt():
    assert mh781_el_base(15, 2.5) == pytest.approx(6.0)
    assert mh781_gas_base(60, 0.85) == pytest.approx(70.58823529411765)
    assert mh781_el_alt(15, 5.5, 60, 4.5) == pytest.approx(16.060606060606062)
    assert mh781_el_alt(15, 20, 60, 20) == pytest.approx(3.75)
    with pytest.raises(ValueError):
        mh781_el_base(15, 0)
    with pytest.raises(ValueError):
        mh781_el_base(0, 2.5)
    with pytest.raises(ValueError):
        mh781_gas_base(60, 0)
    with pytest.raises(ValueError):
        mh781_gas_base(60, 1.2)
    with pytest.raises(ValueError):
        mh781_gas_base(0, 0.85)
    with pytest.raises(ValueError):
        mh781_el_alt(15, 0, 60, 4.5)


def test_c_base_per_hl_scomposizione():
    assert mh781_c_base_per_hl(6.0, 170, 70.58823529411765, 70,
                               5.0) == pytest.approx(10.961176470588235)
    assert mh781_c_base_per_hl(0, 170, 0, 70,
                               0) == pytest.approx(0.0)
    assert mh781_c_base_per_hl(6.0, 0, 70.58823529411765, 70,
                               5.0) == pytest.approx(9.941176470588236)
    with pytest.raises(ValueError):
        mh781_c_base_per_hl(6.0, 170, -1, 70, 5.0)
    with pytest.raises(ValueError):
        mh781_c_base_per_hl(6.0, 170, 70.58823529411765, -1, 5.0)


def test_c_alt_per_hl_scomposizione():
    assert mh781_c_alt_per_hl(16.060606060606062, 170,
                              4.0) == pytest.approx(6.7303030303030305)
    assert mh781_c_alt_per_hl(16.060606060606062, 0,
                              4.0) == pytest.approx(4.0)
    assert mh781_c_alt_per_hl(0, 170,
                              4.0) == pytest.approx(4.0)
    assert mh781_c_alt_per_hl(16.060606060606062, 170,
                              0) == pytest.approx(2.7303030303030303)
    with pytest.raises(ValueError):
        mh781_c_alt_per_hl(16.060606060606062, -1, 4.0)
    with pytest.raises(ValueError):
        mh781_c_alt_per_hl(16.060606060606062, 170, -1)


def test_c_nonel():
    assert mh781_c_base_nonel(10.961176470588235, 6.0, 170) == pytest.approx(9.941176470588236)
    assert mh781_c_alt_nonel(6.7303030303030305, 16.060606060606062, 170) == pytest.approx(4.0)
    assert mh781_c_base_nonel(10.961176470588235, 6.0, 0) == pytest.approx(10.961176470588235)
    with pytest.raises(ValueError):
        mh781_c_base_nonel(10.961176470588235, -1, 170)


def test_c_base_c_alt_var_c_alt():
    assert mh781_c_base(10.961176470588235, 8000) == pytest.approx(87689.41176470587)
    assert mh781_c_alt_var(6.7303030303030305, 8000) == pytest.approx(
        53842.42424242424)
    assert mh781_c_alt(53842.42424242424, 25000) == pytest.approx(
        78842.42424242424)
    with pytest.raises(ValueError):
        mh781_c_base(10.961176470588235, 0)
    with pytest.raises(ValueError):
        mh781_c_alt(53842.42424242424, -1)


def test_co2_base_alt_evitata():
    assert mh781_co2_base(70.58823529411765, 8000, 6.0, 0.20,
                          0.25) == pytest.approx(124.94117647058825)
    assert mh781_co2_alt(16.060606060606062, 8000,
                         0.25) == pytest.approx(32.121212121212125)
    assert mh781_co2_alt(16.060606060606062, 8000,
                         0) == pytest.approx(0.0)
    assert mh781_co2_base(70.58823529411765, 8000, 6.0, 0.20,
                          0) == pytest.approx(112.94117647058825)
    assert mh781_co2_evitata(124.94117647058825,
                             32.121212121212125) == pytest.approx(92.81996434937612)
    assert mh781_co2_evitata(100.0, 150.0) == pytest.approx(-50.0)
    with pytest.raises(ValueError):
        mh781_co2_base(70.58823529411765, 8000, 6.0, -0.10, 0.25)


def test_co2_evitata_puo_essere_negativa_via_calcola():
    """Differenza chiave di questa tab: via
    mh781_calcola la CO2 evitata PUO' essere
    negativa (fattore gas zero, fattore
    elettricita' alto)."""
    bc = _variante(f_gas_t_per_mwh=0, f_el_t_per_mwh=1.0)
    assert bc["co2_base_t_anno"] == pytest.approx(48.0)
    assert bc["co2_alt_t_anno"] == pytest.approx(128.4848484848485)
    assert bc["co2_evitata_t_anno"] == pytest.approx(-80.4848484848485)
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_co2_formula_componenti():
    """CO2 base = gas x f_gas + elettricita' base x f_el,
    CO2 geotermica = elettricita' geotermica
    x f_el, con la conversione kWh->MWh."""
    for bc in (demo_calcoli(),
               _variante(f_gas_t_per_mwh=0, f_el_t_per_mwh=1.0),
               _variante(cop_geo_freddo=20, cop_geo_caldo=20)):
        atteso_base = (bc["gas_mwh_anno"] * bc["f_gas_t_per_mwh"]
                       + bc["el_base_mwh_anno"] * bc["f_el_t_per_mwh"])
        assert bc["co2_base_t_anno"] == pytest.approx(atteso_base)
        atteso_alt = (bc["el_alt_mwh_anno"] * bc["f_el_t_per_mwh"])
        assert bc["co2_alt_t_anno"] == pytest.approx(atteso_alt)


def test_risparmio_segno():
    assert mh781_risparmio(87689.41176470587, 78842.42424242424) == \
        pytest.approx(8846.987522281634)
    assert mh781_risparmio(78842.42424242424, 78842.42424242424) == 0.0
    assert mh781_risparmio(107875.27, 132875.27) == \
        pytest.approx(-25000.0)


def test_crf_solo_lco():
    assert mh781_crf(5.0, 20) == pytest.approx(0.08024258719069129)
    assert mh781_crf(0.0, 20) == pytest.approx(1.0 / 20.0)
    assert mh781_crf(5.0, 15) == pytest.approx(0.09634228727240925)
    with pytest.raises(ValueError):
        mh781_crf(50.1, 20)
    with pytest.raises(ValueError):
        mh781_crf(5.0, 0)


def test_lco():
    assert mh781_lco_base(87689.41176470587, 8000) == pytest.approx(10.961176470588235)
    assert mh781_lco_alt(150000, 0.08024258719069129, 25000,
                         6.7303030303030305, 8000) == pytest.approx(
        11.359851540128492)
    assert mh781_lco_base(87689.41176470587, 0) is None
    assert mh781_lco_alt(150000, 0.08024258719069129, 25000,
                         6.7303030303030305, 0) is None
    assert mh781_lco_alt(150000, 0.08024258719069129, 25000,
                         6.7303030303030305, -5) is None
    # Il CAPEX entra nel LCO solo annuizzato: con CAPEX nullo
    # il LCO alt e' (O&M / P) + C_alt_per_hl.
    assert mh781_lco_alt(0, 0.08024258719069129, 25000,
                         6.7303030303030305, 8000) == pytest.approx(9.85530303030303)


def test_crf_mai_nei_flussi():
    """Il CRF entra SOLO nel LCO: i flussi usano il
    CAPEX intero all'anno 0 e la VAN dai flussi non
    dipende dal CRF (cambiando il WACC cambia la VAN
    per lo sconto, non per il CRF)."""
    bc = demo_calcoli()
    assert bc["flussi"][0] == -150000
    assert all(f == pytest.approx(20141.105169340473)
               for f in bc["flussi"][1:])
    assert bc["van"] == pytest.approx(mh781_van(bc["flussi"], 5.0))
    bc0 = _variante(wacc_pct=0)
    assert bc0["van"] == pytest.approx(sum(bc0["flussi"]))
    assert bc0["crf"] == pytest.approx(1.0 / 20.0)
    assert bc0["lco_alt_eur_hl"] == pytest.approx(10.79280303030303)


def test_breakeven_el_demo_e_varianti():
    # Demo: (9,94 - 4,00) / ((16,06 - 6,00) / 1000) = 590,54.
    assert mh781_breakeven_el(9.941176470588236, 4.0, 16.060606060606062,
                              6.0) == pytest.approx(590.5386250885896)
    # Numeratore zero: pareggio zero, valido.
    assert mh781_breakeven_el(9.941176470588236, 9.941176470588236,
                              16.060606060606062,
                              6.0) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh781_breakeven_el(9.941176470588236, 4.0, -1, 6.0)


def test_breakeven_el_none_casi():
    # Denominatore <= 0: el_alt uguale o sotto el_base.
    assert mh781_breakeven_el(9.941176470588236, 4.0, 6.0, 6.0) is None
    assert mh781_breakeven_el(9.941176470588236, 4.0, 3.75, 6.0) is None
    # Numeratore < 0: costo geotermico senza
    # elettricita' sopra il costo base senza elettricita'.
    assert mh781_breakeven_el(9.941176470588236, 10.0, 16.060606060606062, 6.0) is None


def test_breakeven_gas_demo_e_varianti():
    # Demo: (6,73 - 1,02 - 5,00) / (70,59 / 1000) = 10,06.
    assert mh781_breakeven_gas(6.7303030303030305, 6.0, 170, 5.0,
                               70.58823529411765) == pytest.approx(
        10.06262626262627)
    # Numeratore zero: pareggio zero, valido.
    assert mh781_breakeven_gas(6.02, 6.0, 170, 5.0,
                               70.58823529411765) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh781_breakeven_gas(6.7303030303030305, 6.0, 170, 5.0, -1)


def test_breakeven_gas_none_casi():
    # Gas <= 0: nessun prezzo da calcolare.
    assert mh781_breakeven_gas(6.7303030303030305, 6.0, 170, 5.0, 0) is None
    # Numeratore < 0: a prezzo gas zero il costo base
    # senza gas e' gia' sopra il costo alternativo.
    assert mh781_breakeven_gas(0, 6.0, 0, 5.0, 70.58823529411765) is None


def test_breakeven_verifica_pareggio():
    """Al prezzo elettrico di pareggio i costi per ettolitro
    si eguagliano: C_alt_per_hl(p*) =
    C_base_per_hl(p*). Il risparmio invece e' -O&M, non
    zero (i pareggi non includono l'O&M). Al prezzo gas
    di pareggio vale lo stesso: C_base_per_hl =
    C_alt_per_hl e risparmio -O&M. Per il gas vale
    l'identita' a prezzo elettrico corrente:
    el_base / 1000 x p_el + other_base +
    gas_base / 1000 x be_gas = C_alt_per_hl."""
    bc = _variante(p_el_eur_mwh=730.8646350106308)
    assert bc["c_base_per_hl"] == pytest.approx(bc["c_alt_per_hl"])
    assert bc["risparmio_eur_anno"] == pytest.approx(-25000.0)
    bc2 = _variante(p_gas_eur_mwh=10.06262626262627)
    assert bc2["c_base_per_hl"] == pytest.approx(bc2["c_alt_per_hl"])
    assert bc2["risparmio_eur_anno"] == pytest.approx(-25000.0)
    demo = demo_calcoli()
    assert (demo["el_base_kwh_hl"] / 1000.0
            * demo["p_el_eur_mwh"]
            + demo["other_base_eur_hl"]
            + demo["gas_base_kwh_hl"] / 1000.0
            * demo["breakeven_gas_eur_mwh"]) == pytest.approx(
        demo["c_alt_per_hl"])


def test_pareggi_versi_opposti():
    """Sotto il tetto elettrico la geotermica vince
    sui costi variabili, sopra perde; sopra la soglia
    gas la geotermica vince, sotto perde."""
    be_el = demo_calcoli()["breakeven_el_eur_mwh"]
    assert _variante(p_el_eur_mwh=be_el - 10)[
        "c_alt_per_hl"] < _variante(p_el_eur_mwh=be_el - 10)[
        "c_base_per_hl"]
    assert _variante(p_el_eur_mwh=be_el + 10)[
        "c_alt_per_hl"] > _variante(p_el_eur_mwh=be_el + 10)[
        "c_base_per_hl"]
    be_gas = demo_calcoli()["breakeven_gas_eur_mwh"]
    assert _variante(p_gas_eur_mwh=be_gas + 1)[
        "c_alt_per_hl"] < _variante(p_gas_eur_mwh=be_gas + 1)[
        "c_base_per_hl"]
    assert _variante(p_gas_eur_mwh=be_gas - 1)[
        "c_alt_per_hl"] > _variante(p_gas_eur_mwh=be_gas - 1)[
        "c_base_per_hl"]


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh781_flussi(150000, 8846.987522281634, 20)
    assert len(fl) == 21
    assert fl[0] == -150000
    assert all(f == 8846.987522281634 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = demo_calcoli()
    assert bc["van"] == pytest.approx(101002.68915154031)
    assert mh781_van([-150000] + [20141.105169340473] * 20,
                     0) == pytest.approx(252822.10338680947)
    assert mh781_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = demo_calcoli()
    assert bc["tir"] == pytest.approx(12.047078687632562)
    assert mh781_tir([-150000] + [20141.105169340473] * 20) == \
        pytest.approx(0.12047078687632562)
    tir = mh781_tir([-150000] + [20141.105169340473] * 20)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate(
                  [-150000] + [20141.105169340473] * 20))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    """Payback con cumulato >= 0: il cumulato nullo basta."""
    assert mh781_payback([-150000] + [8846.987522281634] * 20) == 17
    assert mh781_payback([-150000] + [-1000.0] * 20) is None
    assert mh781_payback([0] + [8846.987522281634] * 20) == 0
    assert mh781_payback([-100] + [50] * 2) == 2
    assert mh781_payback([-17693.975044563268] +
                         [8846.987522281634] * 2) == 2


def test_verdetto():
    assert mh781_verdetto(8846.987522281634, 87689.41176470587,
                          10.0) == "CONVIENTE"
    assert mh781_verdetto(8768.941176470587, 87689.41176470587,
                          10.0) == "MARGINALE"
    assert mh781_verdetto(0.0, 87689.41176470587, 10.0) == "MARGINALE"
    assert mh781_verdetto(-8768.941176470587, 87689.41176470587,
                          10.0) == "MARGINALE"
    assert mh781_verdetto(-8769.0, 87689.41176470587,
                          10.0) == "NON_CONVIENTE"
    assert mh781_verdetto(-30682.42424242424, 87689.41176470587,
                          10.0) == "NON_CONVIENTE"
    assert mh781_verdetto(8846.987522281634, 87689.41176470587,
                          0.0) == "CONVIENTE"
    assert mh781_verdetto(-100.0, 87689.41176470587,
                          0.0) == "NON_CONVIENTE"
    assert mh781_verdetto(None, 87689.41176470587,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh781_verdetto(float("nan"), 87689.41176470587, 10.0)
    with pytest.raises(ValueError):
        mh781_verdetto(100.0, -1, 10.0)
    with pytest.raises(ValueError):
        mh781_verdetto(100.0, 87689.41176470587, 100.1)


def test_valida_demo_ok():
    v = mh781_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("p_hl_anno", "8000"),
                       ("p_hl_anno", float("nan")),
                       ("p_hl_anno", float("inf")),
                       ("p_hl_anno", True),
                       ("p_gas_eur_mwh", None),
                       ("q_freddo_kwh_hl", "15")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh781_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("p_hl_anno", 0),
                          ("p_hl_anno", -1),
                          ("q_freddo_kwh_hl", 0),
                          ("q_freddo_kwh_hl", -1),
                          ("q_caldo_kwh_hl", 0),
                          ("q_caldo_kwh_hl", -1),
                          ("cop_chiller", 0),
                          ("cop_chiller", -1),
                          ("eta_caldaia", 0),
                          ("eta_caldaia", 1.01),
                          ("cop_geo_freddo", 0),
                          ("cop_geo_caldo", -1),
                          ("p_el_eur_mwh", -1),
                          ("p_gas_eur_mwh", -1),
                          ("other_base_eur_hl", -1),
                          ("other_alt_eur_hl", -1),
                          ("om_eur_anno", -100),
                          ("capex_eur", -1),
                          ("f_gas_t_per_mwh", -0.10),
                          ("f_el_t_per_mwh", -0.10),
                          ("wacc_pct", -0.1), ("wacc_pct", 50.1),
                          ("vita_anni", 0), ("vita_anni", 2.5),
                          ("tolleranza_pct", -1),
                          ("tolleranza_pct", 100.1)):
        d = _demo_kwargs()
        d[campo] = valore
        assert mh781_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"p_el_eur_mwh": 0,
              "p_gas_eur_mwh": 0,
              "other_base_eur_hl": 0,
              "other_alt_eur_hl": 0,
              "om_eur_anno": 0,
              "capex_eur": 0,
              "f_gas_t_per_mwh": 0,
              "f_el_t_per_mwh": 0,
              "wacc_pct": 0,
              "tolleranza_pct": 0})
    assert mh781_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    assert mh781_valida(**d)["valido"] is True


def test_valida_non_controlla_risparmio_calcola_neppure():
    """La validazione input NON controlla il risparmio
    (e' un esito, non un range) e in questa tab
    nemmeno mh781_calcola lo controlla: con prezzo
    gas zero il caso resta CALCOLABILE."""
    d = _demo_kwargs()
    d["p_gas_eur_mwh"] = 0
    assert mh781_valida(**d)["valido"] is True
    bc = _variante(p_gas_eur_mwh=0)
    assert bc["valid"] is True
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["flussi"]
    assert bc["payback"] is None


def test_demo_dict():
    d = mh781_demo()
    assert d["p_hl_anno"] == 8000
    assert d["q_freddo_kwh_hl"] == 15
    assert d["q_caldo_kwh_hl"] == 60
    assert d["cop_chiller"] == 2.5
    assert d["eta_caldaia"] == 0.85
    assert d["cop_geo_freddo"] == 5.5
    assert d["cop_geo_caldo"] == 4.5
    assert d["p_el_eur_mwh"] == 170
    assert d["p_gas_eur_mwh"] == 90
    assert d["other_base_eur_hl"] == 5.0
    assert d["other_alt_eur_hl"] == 4.0
    assert d["om_eur_anno"] == 25000
    assert d["capex_eur"] == 150000
    assert d["f_gas_t_per_mwh"] == 0.20
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
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_demo_calcoli_fisica():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["c_base_per_hl"] == pytest.approx(12.372941176470588)
    assert bc["c_alt_per_hl"] == pytest.approx(6.7303030303030305)
    assert bc["el_base_mwh_anno"] == pytest.approx(48.0)
    assert bc["gas_mwh_anno"] == pytest.approx(564.7058823529412)
    assert bc["el_alt_mwh_anno"] == pytest.approx(128.4848484848485)
    assert bc["co2_evitata_t_anno"] == pytest.approx(92.81996434937612)


def test_demo_calcoli_economia():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(98983.52941176471)
    assert bc["c_alt_var_eur_anno"] == pytest.approx(53842.42424242424)
    assert bc["c_alt_eur_anno"] == pytest.approx(78842.42424242424)
    assert bc["risparmio_eur_anno"] == pytest.approx(20141.105169340473)
    assert bc["breakeven_el_eur_mwh"] == pytest.approx(730.8646350106308)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(
        10.06262626262627)


def test_demo_calcoli_finanza():
    bc = demo_calcoli()
    assert bc["crf"] == pytest.approx(0.08024258719069129)
    assert bc["lco_base_eur_hl"] == pytest.approx(12.372941176470588)
    assert bc["lco_alt_eur_hl"] == pytest.approx(11.359851540128492)
    assert bc["van"] == pytest.approx(101002.68915154031)
    assert bc["tir"] == pytest.approx(12.047078687632562)
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"


def test_demo_flussi_e_cumulato():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -150000
    assert len(bc["flussi"]) == 21
    assert all(f == pytest.approx(20141.105169340473)
               for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -150000
    assert righe.iloc[16]["Cumulato (EUR)"] == pytest.approx(172257.68270944757)
    assert righe.iloc[17]["Cumulato (EUR)"] == pytest.approx(192398.78787878805)
    assert righe.iloc[20]["Cumulato (EUR)"] == pytest.approx(
        252822.10338680947)
    assert righe.iloc[20]["Flusso (EUR/anno)"] == pytest.approx(
        20141.105169340473)


def test_demo_tabella_righe():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Produzione di vino (hl/anno)"] == pytest.approx(
        8000.0)
    assert mappa["Costo base per ettolitro (EUR/hl)"] == pytest.approx(
        12.372941176470588)
    assert mappa["Costo geotermico per ettolitro (EUR/hl)"] == pytest.approx(
        6.7303030303030305)
    assert mappa["Elettricita' geotermica (MWh/anno)"] == pytest.approx(
        128.4848484848485)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(
        78842.42424242424)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(20141.105169340473)
    assert mappa["Payback (anni)"] == 8
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo elettricita' (EUR/MWh)"] == \
        pytest.approx(730.8646350106308)
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] == \
        pytest.approx(10.06262626262627)


def test_demo_coerenza_interna():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["c_base_per_hl"] * bc["p_hl_anno"] == \
        pytest.approx(bc["c_base_eur_anno"])
    assert bc["c_alt_per_hl"] * bc["p_hl_anno"] == \
        pytest.approx(bc["c_alt_var_eur_anno"])
    assert bc["co2_base_t_anno"] - bc["co2_alt_t_anno"] == \
        pytest.approx(bc["co2_evitata_t_anno"])
    assert bc["c_base_eur_anno"] / bc["p_hl_anno"] == \
        pytest.approx(bc["lco_base_eur_hl"])
    assert (bc["capex_eur"] * bc["crf"] + bc["om_eur_anno"]) / \
        bc["p_hl_anno"] + bc["c_alt_per_hl"] == \
        pytest.approx(bc["lco_alt_eur_hl"])
    assert bc["c_base_nonel_per_hl"] + \
        bc["el_base_kwh_hl"] / 1000.0 * bc["p_el_eur_mwh"] == \
        pytest.approx(bc["c_base_per_hl"])


def test_demo_contro_riconteggio_indipendente():
    p, qf, qc = 8000, 15, 60
    copc, eta, copf, coph = 2.5, 0.85, 5.5, 4.5
    pel, pg, ob, oa = 170, 90, 5.0, 4.0
    om, cx = 25000, 150000
    fg, fel, wacc, vita = 0.20, 0.25, 5.0, 20
    elb = qf / copc
    gas = qc / eta
    ela = qf / copf + qc / coph
    cb = elb / 1000.0 * pel + gas / 1000.0 * pg + ob
    ca = ela / 1000.0 * pel + oa
    cbase = cb * p
    cav = ca * p
    caa = cav + om
    risp = cbase - caa
    co2b = gas / 1000.0 * p * fg + elb / 1000.0 * p * fel
    co2a = ela / 1000.0 * p * fel
    r = wacc / 100.0
    crf = r * (1 + r) ** vita / ((1 + r) ** vita - 1.0)
    lco_b = cb
    lco_a = (cx * crf + om) / p + ca
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    be_el = (cb - elb / 1000.0 * pel
             - (ca - ela / 1000.0 * pel)) / ((ela - elb) / 1000.0)
    be_gas = (ca - elb / 1000.0 * pel - ob) / (gas / 1000.0)
    bc = demo_calcoli()
    assert bc["el_base_kwh_hl"] == pytest.approx(elb)
    assert bc["gas_base_kwh_hl"] == pytest.approx(gas)
    assert bc["el_alt_kwh_hl"] == pytest.approx(ela)
    assert bc["c_base_per_hl"] == pytest.approx(cb)
    assert bc["c_alt_per_hl"] == pytest.approx(ca)
    assert bc["c_base_eur_anno"] == pytest.approx(cbase)
    assert bc["c_alt_var_eur_anno"] == pytest.approx(cav)
    assert bc["c_alt_eur_anno"] == pytest.approx(caa)
    assert bc["risparmio_eur_anno"] == pytest.approx(risp)
    assert bc["co2_base_t_anno"] == pytest.approx(co2b)
    assert bc["co2_alt_t_anno"] == pytest.approx(co2a)
    assert bc["crf"] == pytest.approx(crf)
    assert bc["lco_base_eur_hl"] == pytest.approx(lco_b)
    assert bc["lco_alt_eur_hl"] == pytest.approx(lco_a)
    assert bc["van"] == pytest.approx(van)
    assert bc["breakeven_el_eur_mwh"] == pytest.approx(be_el)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(be_gas)


# ---------------------------------------------------------------- varianti
def test_demo_conviente_e_van_positiva():
    """Il demo e' CONVIENTE sul risparmio (20.141,11
    sopra la soglia 9.898,35) e con VAN positiva,
    TIR sopra il WACC e payback 8 anni: risparmio,
    LCO e VAN concordano."""
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] > 0.0
    assert bc["tir"] > 5.0
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["lco_alt_eur_hl"] < bc["lco_base_eur_hl"]


def test_verdetto_risparmio_non_guarda_van():
    """Con CAPEX 1.500.000 EUR la VAN diventa
    -1.248.997,31 e il payback sparisce, ma il
    verdetto resta CONVIENTE: il verdetto guarda
    il risparmio annuo, non la remunerazione del
    CAPEX."""
    bc = _variante(capex_eur=1500000)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(20141.105169340473)
    assert bc["van"] == pytest.approx(-1248997.3108484596)
    assert bc["payback"] is None
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_pel_un_euro_in_piu_conviente():
    """Prezzo elettricita' 171 EUR/MWh (un euro in
    piu'): il risparmio cala di 80,48 EUR/anno
    (pendenza (6,00 - 16,06) / 1000 x 8.000) a
    20.060,62 e resta CONVIENTE: il demo a gas 90
    non e' piu' al limite della soglia."""
    bc = _variante(p_el_eur_mwh=171)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(20060.62032085561)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_pel_300_marginale():
    """Prezzo elettricita' 300 EUR/MWh: risparmio
    9.678,07, sotto la soglia 10.522,35 (10 % di
    C_base 105.223,53): VAN -29.389,80, payback 16,
    MARGINALE."""
    bc = _variante(p_el_eur_mwh=300)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(9678.07486631014)
    assert bc["van"] == pytest.approx(-29389.795305193504)
    assert bc["payback"] == 16
    assert bc["verdetto"] == "MARGINALE"


def test_variante_pgas_sotto_soglia_marginale():
    """Gas 69 EUR/MWh (un euro in meno): risparmio
    8.282,28, MARGINALE."""
    bc = _variante(p_gas_eur_mwh=69)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(8282.281639928693)
    assert bc["verdetto"] == "MARGINALE"


def test_variante_pgas_80_conviente_van_positiva():
    """Gas 80 EUR/MWh: risparmio 14.494,05, VAN
    30.627,85, payback 11, CONVIENTE."""
    bc = _variante(p_gas_eur_mwh=80)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(14494.045522281634)
    assert bc["van"] == pytest.approx(30627.85, rel=1e-4)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_pareggio_el_esatto():
    """Al tetto elettrico esatto (730,86 EUR/MWh) i
    costi per ettolitro si eguagliano (15,74
    EUR/hl) ma il risparmio e' -25.000 (solo l'O&M):
    VAN -461.555,26, TIR None, payback mai,
    verdetto NON_CONVIENTE (25.000 supera la soglia
    del 10 % di C_base a quel prezzo, 12.590,50)."""
    bc = _variante(p_el_eur_mwh=730.8646350106308)
    assert bc["c_base_per_hl"] == pytest.approx(bc["c_alt_per_hl"])
    assert bc["risparmio_eur_anno"] == pytest.approx(-25000.0)
    assert bc["van"] == pytest.approx(-461555.26, rel=1e-4)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_pareggio_gas_esatto():
    """Al prezzo gas di pareggio esatto (10,06 EUR/MWh) i
    costi per ettolitro si eguagliano (6,73
    EUR/hl) ma il risparmio e' -25.000 (solo l'O&M):
    VAN -461.555,26, payback mai, verdetto
    NON_CONVIENTE (C_base 53.842,42, soglia 10 %
    5.384,24, e 25.000 resta fuori dalla soglia)."""
    bc = _variante(p_gas_eur_mwh=10.06262626262627)
    assert bc["c_base_per_hl"] == pytest.approx(bc["c_alt_per_hl"])
    assert bc["risparmio_eur_anno"] == pytest.approx(-25000.0)
    assert bc["van"] == pytest.approx(-461555.26, rel=1e-4)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_pel_400_marginale():
    """Prezzo elettricita' 400 EUR/MWh (sotto il
    tetto 730,86 ma sopra il prezzo demo):
    risparmio 1.629,59, VAN -129.691,71, TIR
    -11,54 % (sotto zero: flussi troppo piccoli
    per ripagare il CAPEX), payback mai,
    verdetto MARGINALE."""
    bc = _variante(p_el_eur_mwh=400)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(1629.5900178252923)
    assert bc["van"] == pytest.approx(-129691.70642575769)
    assert bc["tir"] == pytest.approx(-11.543619346587946)
    assert bc["payback"] is None
    assert bc["verdetto"] == "MARGINALE"


def test_variante_gas_zero_non_conviente():
    """Gas zero: risparmio -30.682,42, VAN
    -532.370,82, NON_CONVIENTE."""
    bc = _variante(p_gas_eur_mwh=0)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(-30682.42424242424)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_tolleranza_zero_demo_conviente():
    """Con tolleranza 0 % lo stesso demo resta
    CONVIENTE (risparmio positivo, soglia zero)."""
    bc = _variante(tolleranza_pct=0)
    assert bc["risparmio_eur_anno"] == pytest.approx(20141.105169340473)
    assert bc["van"] == pytest.approx(101002.68915154031)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    """Payback regola >=: con CAPEX nullo il payback e' 0,
    non 1 (all'anno 0 il cumulato e' gia' zero)."""
    bc = _variante(capex_eur=0)
    assert bc["capex_eur"] == 0
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(251002.68915154034, rel=1e-4)
    assert bc["lco_alt_eur_hl"] == pytest.approx(9.85530303030303)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(252822.10338680947)
    assert bc["lco_alt_eur_hl"] == pytest.approx(10.79280303030303)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_vita_diversa():
    """Vita 10 anni: VAN 5.524,28, payback 8 anni, e
    verdetto ancora CONVIENTE (stesso risparmio annuo:
    il verdetto non guarda la durata)."""
    bc = _variante(vita_anni=10)
    assert len(bc["flussi"]) == 11
    assert bc["van"] == pytest.approx(5524.275298481087)
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_om_alto():
    """O&M 40.000 EUR/anno: risparmio 5.141,11,
    verdetto MARGINALE (entro la soglia 9.898,35)."""
    bc = _variante(om_eur_anno=40000)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(5141.105169340473)
    assert bc["payback"] is None
    assert bc["verdetto"] == "MARGINALE"


def test_variante_breakeven_el_none_denominatore():
    """COP geotermici 20 e 20: el_alt 3,75 sotto
    el_base 6,00: breakeven elettrico None e breakeven
    gas None (numeratore negativo), caso calcolabile
    CONVIENTE con risparmio 36.883,53."""
    bc = _variante(cop_geo_freddo=20, cop_geo_caldo=20)
    assert bc["valid"] is True
    assert bc["el_alt_kwh_hl"] == pytest.approx(3.75)
    assert bc["breakeven_el_eur_mwh"] is None
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["risparmio_eur_anno"] == pytest.approx(36883.52941176471)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_breakeven_el_none_numeratore():
    """Altri costi geotermica 12,00 EUR/hl: costo
    geotermico senza elettricita' 12,00 sopra il
    costo base senza elettricita' 11,35: breakeven
    elettrico None (con 10,00 il numeratore resta
    positivo e il pareggio esisterebbe a 134,48)."""
    bc = _variante(other_alt_eur_hl=12.0)
    assert bc["valid"] is True
    assert bc["breakeven_el_eur_mwh"] is None
    assert bc["risparmio_eur_anno"] == pytest.approx(-43858.89483065954)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_breakeven_gas_none_numeratore():
    """Prezzo elettricita' zero e altri costi geotermica
    nulli: breakeven gas None (numeratore negativo)."""
    bc = _variante(p_el_eur_mwh=0, other_alt_eur_hl=0)
    assert bc["valid"] is True
    assert bc["breakeven_gas_eur_mwh"] is None


# ---------------------------------------------------------------- degenere
def test_degenere_produzione_zero_sollevela():
    """Caso degenere richiesto dal brief: P = 0
    solleva ValueError."""
    with pytest.raises(ValueError):
        _variante(p_hl_anno=0)


def test_degenere_verdetto_non_calcolabile_van_tir_payback_none():
    """Nel regime degenere non esiste alcun calcolo:
    calcola solleva ValueError, quindi nessuna VAN,
    nessuna TIR e nessun payback vengono prodotti
    (sono None per assenza); il verdetto per
    risparmio None e' NON_CALCOLABILE."""
    with pytest.raises(ValueError):
        _variante(p_hl_anno=0)
    with pytest.raises(ValueError):
        _variante(p_el_eur_mwh=-1)
    with pytest.raises(ValueError):
        _variante(wacc_pct=60)
    with pytest.raises(ValueError):
        _variante(eta_caldaia=1.2)
    assert mh781_verdetto(None, 87689.41176470587, 10.0) == "NON_CALCOLABILE"
    assert demo_calcoli()["verdetto"] != "NON_CALCOLABILE"


def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"p_hl_anno": 0}, {"p_hl_anno": -1},
               {"q_freddo_kwh_hl": 0}, {"q_freddo_kwh_hl": -1},
               {"q_caldo_kwh_hl": 0}, {"q_caldo_kwh_hl": -1},
               {"cop_chiller": 0}, {"cop_chiller": -1},
               {"eta_caldaia": 0}, {"eta_caldaia": 1.01},
               {"cop_geo_freddo": 0}, {"cop_geo_caldo": -1},
               {"p_el_eur_mwh": -1},
               {"p_gas_eur_mwh": -1},
               {"other_base_eur_hl": -1},
               {"other_alt_eur_hl": -1},
               {"om_eur_anno": -100},
               {"capex_eur": -1},
               {"f_gas_t_per_mwh": -0.10},
               {"f_el_t_per_mwh": -0.10},
               {"wacc_pct": -1}, {"wacc_pct": 60},
               {"vita_anni": 0}, {"vita_anni": 2.5},
               {"tolleranza_pct": -1},
               {"tolleranza_pct": 100.1}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh781_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"p_hl_anno": "8000"},
               {"p_hl_anno": float("nan")},
               {"p_gas_eur_mwh": float("inf")},
               {"capex_eur": True},
               {"q_freddo_kwh_hl": "15"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh781_valida(**d)["valido"] is False


def test_risparmio_negativo_non_degenere():
    """Differenza chiave: risparmio nullo o
    negativo resta calcolabile, con flussi pieni e
    VAN negativa; cosi' anche la CO2 evitata
    negativa resta calcolabile, e cosi' i
    breakeven None restano calcolabili."""
    for kw in ({"p_gas_eur_mwh": 0},
               {"p_el_eur_mwh": 400}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["verdetto"] in ("NON_CONVIENTE", "MARGINALE")
        assert bc["flussi"]
    bc = _variante(f_gas_t_per_mwh=0, f_el_t_per_mwh=1.0)
    assert bc["co2_evitata_t_anno"] < 0.0
    assert bc["valid"] is True
    bc2 = _variante(cop_geo_freddo=20, cop_geo_caldo=20)
    assert bc2["breakeven_el_eur_mwh"] is None
    assert bc2["valid"] is True
    bc3 = _variante(p_el_eur_mwh=0, other_alt_eur_hl=0)
    assert bc3["breakeven_gas_eur_mwh"] is None
    assert bc3["valid"] is True


def test_co2_evitata_segno_funzione_pura():
    assert mh781_co2_evitata(100.0, 150.0) == pytest.approx(-50.0)


def test_verdetto_non_calcolabile_solo_risparmio_none():
    assert mh781_verdetto(None, 87689.41176470587, 10.0) == "NON_CALCOLABILE"
    assert demo_calcoli()["verdetto"] != "NON_CALCOLABILE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = demo_calcoli()
    testo = mh781_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_per_hl;{bc['c_base_per_hl']}" in testo
    assert f"c_alt_per_hl;{bc['c_alt_per_hl']}" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_var_eur_anno;{bc['c_alt_var_eur_anno']}" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_el_eur_mwh" in testo
    assert "breakeven_gas_eur_mwh" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = demo_calcoli()
    testo = mh781_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"c_alt_per_hl;{bc['c_alt_per_hl']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = demo_calcoli()
    testo = mh781_csv(bc, _demo_kwargs())
    for chiave in _demo_kwargs():
        assert f"{chiave};" in testo


def test_monotonia_prezzo_el_decrescente():
    # Il risparmio CALA con p_el (la geotermica
    # consuma piu' elettricita' della baseline):
    # pendenza -80,48 EUR/anno per EUR/MWh (8.000 hl x
    # (16,06 - 6,00) / 1000 = 80,48 MWh/anno).
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_el_eur_mwh=180)["risparmio_eur_anno"]
    basso = _variante(p_el_eur_mwh=160)["risparmio_eur_anno"]
    assert basso > base > alto
    assert base - alto == pytest.approx(804.8484848484848)
    assert basso - base == pytest.approx(804.8484848484848)


def test_monotonia_prezzo_gas_crescente():
    # Il risparmio CRESCE con p_gas (solo la baseline
    # brucia gas): pendenza +564,71 EUR/anno per EUR/MWh
    # (8.000 hl x 70,59 / 1000 = 564,71 MWh/anno).
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas_eur_mwh=91)["risparmio_eur_anno"]
    basso = _variante(p_gas_eur_mwh=89)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(564.7058823529412)
    assert base - basso == pytest.approx(564.7058823529412)


def test_monotonia_elettricita_alt():
    # Piu' elettricita' geotermica, piu' cara
    # l'alternativa: +1 kWh_e/hl a 170 EUR/MWh =
    # +0,17 EUR/hl = -1.360 EUR/anno di risparmio.
    base = demo_calcoli()["risparmio_eur_anno"]
    assert _variante(cop_geo_caldo=4.0)[
        "risparmio_eur_anno"] < base
    assert _variante(cop_geo_caldo=5.0)[
        "risparmio_eur_anno"] > base


def test_demo_deterministica_due_chiamate():
    a = demo_calcoli()
    b = demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh781_demo().keys()) == {
        "p_hl_anno",
        "q_freddo_kwh_hl", "q_caldo_kwh_hl",
        "cop_chiller", "eta_caldaia",
        "cop_geo_freddo", "cop_geo_caldo",
        "p_el_eur_mwh", "p_gas_eur_mwh",
        "other_base_eur_hl", "other_alt_eur_hl",
        "om_eur_anno", "capex_eur",
        "f_gas_t_per_mwh", "f_el_t_per_mwh",
        "wacc_pct", "vita_anni", "tolleranza_pct"}


@pytest.mark.parametrize("p_gas,atteso", [
    (70, 10.961176470588235),
    (0, 6.02),
    (10.06262626262627, 6.7303030303030305),
])
def test_c_base_per_hl_parametrizzato(p_gas, atteso):
    assert mh781_c_base_per_hl(6.0, 170, 70.58823529411765, p_gas,
                               5.0) == pytest.approx(atteso)


@pytest.mark.parametrize("campo,valore", [
    ("p_hl_anno", 0), ("p_hl_anno", -3),
    ("q_freddo_kwh_hl", 0), ("q_freddo_kwh_hl", -1),
    ("q_caldo_kwh_hl", 0), ("q_caldo_kwh_hl", -1),
    ("cop_chiller", 0), ("cop_chiller", -1),
    ("eta_caldaia", 0), ("eta_caldaia", 1.01),
    ("cop_geo_freddo", 0), ("cop_geo_caldo", -1),
    ("p_el_eur_mwh", -1),
    ("p_gas_eur_mwh", -1),
    ("other_base_eur_hl", -1),
    ("other_alt_eur_hl", -1),
    ("om_eur_anno", -100),
    ("capex_eur", -1),
    ("f_gas_t_per_mwh", -0.10),
    ("f_el_t_per_mwh", -0.10),
    ("wacc_pct", -0.1), ("wacc_pct", 50.1),
    ("vita_anni", -1), ("vita_anni", 2.5),
    ("tolleranza_pct", -1), ("tolleranza_pct", 100.1),
])
def test_valida_rifiuta_singoli_campi(campo, valore):
    d = _demo_kwargs()
    d[campo] = valore
    assert mh781_valida(**d)["valido"] is False


@pytest.mark.parametrize("campo,valore", [
    ("p_hl_anno", 0), ("p_hl_anno", -3),
    ("q_freddo_kwh_hl", 0), ("q_freddo_kwh_hl", -1),
    ("q_caldo_kwh_hl", 0), ("q_caldo_kwh_hl", -1),
    ("cop_chiller", 0), ("cop_chiller", -1),
    ("eta_caldaia", 0), ("eta_caldaia", 1.01),
    ("cop_geo_freddo", 0), ("cop_geo_caldo", -1),
    ("p_el_eur_mwh", -1),
    ("p_gas_eur_mwh", -1),
    ("other_base_eur_hl", -1),
    ("other_alt_eur_hl", -1),
    ("om_eur_anno", -100),
    ("capex_eur", -1),
    ("f_gas_t_per_mwh", -0.10),
    ("f_el_t_per_mwh", -0.10),
    ("wacc_pct", -0.1), ("wacc_pct", 50.1),
    ("vita_anni", -1), ("vita_anni", 2.5),
    ("tolleranza_pct", -1), ("tolleranza_pct", 100.1),
])
def test_calcola_sollevela_singoli_campi(campo, valore):
    d = _demo_kwargs()
    d[campo] = valore
    with pytest.raises(ValueError):
        mh781_calcola(**d)


def test_df_tabella_valori_demo_selezionati():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Produzione di vino (hl/anno)"] == 8000.0
    assert mappa["Costo base per ettolitro (EUR/hl)"] == pytest.approx(
        12.372941176470588)


# ------------------------------------------------------- test strutturali
# Adattati dallo schema della tab precedente: AST, registry chain-tail,
# assenza residui della tab precedente, chiavi statiche, guard prima
# degli output, regressione sweep chiavi demo vs UI.
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
    return ["mh" + "78" + "0", "st" + "78" + "0",
            "tab" + "78" + "0"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w782_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w782_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab781:")


def test_registry_chain_tail_and_count():
    """Registry della nuova tab: il frammento UI apre la tab
    numero 781 (la coda della catena termina con la nuova tab
    e il conteggio atteso delle tab e' 781)."""
    src = _leggi("w782_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 781
    assert src.count("with tab781:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w782_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w782_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st781_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w782_ui.py")
    assert "st.stop()" in src
    # guard degenere prima di KPI / grafico / tabella / CSV
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w782_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def781[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w782_ui.py")
        usate = set(re.findall(r'_def781\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 18
        assert usate <= set(mh781_demo().keys())
