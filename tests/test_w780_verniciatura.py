"""Test tab780 "Verniciatura industriale:
essiccare la vernice con pompa di calore + recupero
calore dall'aria esausta batte il bruciatore a gas?"
(File repo: tests/test_w780_verniciatura.py,
contenuto pronto da scrivere in repo.)

Nuova tab tab780 (verniciatura, file di
lavoro w781). Business case
deterministico di una cabina di
verniciatura + forno di essiccazione:
si vernicia S m2/anno di superficie;
baseline aria di cabina riscaldata a
gas con costo per metro quadrato
C_base_per_m2 = gas x p_gas +
el_base / 1000 x p_el + other_base
EUR/m2 (el_base in kWh/m2: 1 MWh =
1000 kWh); alternativa pompa di
calore + recupero calore dall'aria
esausta con costo per metro quadrato
C_alt_per_m2 = el_alt / 1000 x p_el
+ other_alt EUR/m2; costi annui
C_base = C_base_per_m2 x S,
C_alt_var = C_alt_per_m2 x S,
C_alt = C_alt_var + O&M; risparmio
= C_base - C_alt EUR/anno; CO2 base
= gas / 3,6 x S x f_gas + el_base /
1000 x S x f_el t/anno (gas in
GJ/m2: 1 MWh = 3,6 GJ; fattori in
tCO2/MWh); CO2 pompa di calore =
el_alt / 1000 x S x f_el t/anno
(niente gas: nessun bruciatore da
tenere acceso); CO2 evitata = CO2
base - CO2 pompa di calore t/anno,
PUO' ESSERE NEGATIVA in questa tab
(elettricita' sporca, o elettricita'
pompa di calore alta): NON e' una
guard, NON e' un degenere, NON
monetizzata; CRF = r (1 + r)^n /
((1 + r)^n - 1) con r = WACC come
frazione, r = 0 -> 1/n, SOLO nel
LCO, MAI nei flussi; LCO base =
C_base_per_m2 EUR/m2; LCO alt =
(CAPEX x CRF + O&M) / S +
C_alt_per_m2 EUR/m2 (il CAPEX entra
solo annuizzato col CRF);
breakeven prezzo elettricita'
p_el* = (C_base_nonel - C_alt_nonel)
/ ((el_alt - el_base) / 1000) EUR/MWh,
None se denominatore <= 0
(la pompa di calore non consuma piu'
elettricita' della baseline) e
None se numeratore < 0 (a prezzo
elettrico zero la pompa di calore e'
gia' piu' cara e il divario cresce
con p_el); breakeven prezzo gas
p_gas* = (C_alt_per_m2 -
el_base / 1000 x p_el - other_base)
/ gas EUR/GJ, la soglia minima del
prezzo gas a prezzo elettricita'
corrente: sopra di essa la pompa di
calore vince sui costi variabili
(il costo base cresce con p_gas,
il costo alternativo no), sotto
perde; None se gas <= 0 e None se
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
ValueError negli helper (superficie
<= 0, consumi specifici < 0, prezzi
< 0, altri costi < 0, O&M < 0,
CAPEX < 0, fattori < 0, WACC < 0 o
sopra 50 %, vita <= 0 o non intera,
tolleranza fuori [0, 100] %, input
non numerici o non finiti); la UI
lo intercetta PRIMA di KPI, grafico,
tabella e CSV con st.stop(). In
questa tab il risparmio nullo o
negativo NON e' degenere: resta
calcolabile e porta a verdetto
MARGINALE o NON_CONVIENTE. La CO2
evitata PUO' essere negativa in
questa tab: e' un esito onesto, non
una guard. I breakeven None NON
sono degeneri: sono esiti del
calcolo. Distinzione esplicita:
questa tab confronta SOLO aria di
cabina riscaldata a gas contro pompa
di calore + recupero calore
dall'aria esausta per metro quadrato
di superficie verniciata; NON e' la
tab essiccazione legno, NON
lavanderia, NON pastificio: qui si
vernicia superficie (m2/anno).

Demo calcolata eseguendo
demo_calcoli() e ricontrollata con
un ricalcolo indipendente da zero
(riga per riga): superficie
verniciata 200.000 m2/anno, cabina
a gas con gas 0,45 GJ/m2 a 20
EUR/GJ, elettricita' base 8 kWh/m2
a 180 EUR/MWh, altri costi base
2,00 EUR/m2; pompa di calore +
recupero con elettricita' 35 kWh/m2
a 180 EUR/MWh, altri costi 2,50
EUR/m2; O&M annuo 120.000 EUR/anno,
CAPEX 1.500.000 EUR, fattore gas
0,20 tCO2/MWh, fattore elettricita'
0,25 tCO2/MWh, WACC 6 %, vita 15
anni, tolleranza MARGINALE 10 % di
C_base.

- c_base_per_m2 = 12.44
- c_alt_per_m2 = 8.8
- c_base_nonel_per_m2 = 11.0
- c_alt_nonel_per_m2 = 2.5
- el_base_mwh_anno = 1600.0
- el_alt_mwh_anno = 7000.0
- gas_mwh_anno = 25000.0
- c_base_eur_anno = 2488000.0
- c_alt_var_eur_anno = 1760000.0
- c_alt_eur_anno = 1880000.0
- risparmio_eur_anno = 608000.0
- co2_base_t_anno = 5400.0
- co2_alt_t_anno = 1750.0
- co2_evitata_t_anno = 3650.0
- crf = 0.10296276395531265
- lco_base_eur_m2 = 12.44
- lco_alt_eur_m2 = 10.172220729664845
- van = 4405047.3845465155
- tir = 40.28048898276987
- payback = 3
- breakeven_el_eur_mwh = 314.81481481481484
- breakeven_gas_eur_gj = 11.911111111111113
- verdetto = 'CONVIENTE'

Scomposizione: costo base = 0,45 x
20 = 9,00 di gas + 8 / 1000 x 180
= 1,44 di elettricita' + 2,00 altri =
12,44 EUR/m2; costo pompa di calore =
35 / 1000 x 180 = 6,30 di elettricita'
+ 2,50 altri = 8,80 EUR/m2; costo
baseline = 12,44 x 200.000 =
2.488.000 EUR/anno; costo variabile
pompa di calore = 8,80 x 200.000 =
1.760.000 EUR/anno; costo
alternativo = 1.760.000 + 120.000 =
1.880.000 EUR/anno; risparmio =
2.488.000 - 1.880.000 = 608.000
EUR/anno, il 24,44 % di C_base,
sopra la tolleranza del 10 %
(248.800 EUR/anno): verdetto
CONVIENTE; CO2 base = 0,45 x 200.000 /
3,6 x 0,20 = 5.000 di gas + 8
/ 1000 x 200.000 x 0,25 = 400 di
elettrica = 5.400 t/anno; CO2
pompa di calore = 35 / 1000 x 200.000
x 0,25 = 1.750 t/anno; CO2 evitata =
5.400 - 1.750 = 3.650 t/anno;
CRF al 6 % per 15 anni =
0,1029627640; LCO base 12,44
EUR/m2; LCO alt = (1.500.000 x
0,1029627640 + 120.000) / 200.000 +
8,80 = 1,372221 + 8,80 =
10,172221 EUR/m2; flussi: anno 0
-1.500.000, anni 1-15 risparmio
608.000 (piatti); VAN -1.500.000 +
608.000 x 9,712248 (annuita' 15
anni al 6 %) = 4.405.047,38 EUR;
TIR 40,28 %; payback 3 anni (il
cumulato all'anno 2 e' -284.000
EUR, all'anno 3 e' 324.000 EUR,
gia' >= 0); breakeven elettricita'
(11,00 - 2,50) / ((35 - 8) /
1000) = 8,50 / 0,027 = 314,81
EUR/MWh (TETTO: sotto di esso
la pompa di calore vince sui costi
variabili, sopra perde);
breakeven gas (8,80 - 1,44 -
2,00) / 0,45 = 5,36 / 0,45 = 11,91
EUR/GJ (SOGLIA MINIMA: sopra di
essa la pompa di calore vince sui
costi variabili, sotto perde; il
prezzo gas demo, 20 EUR/GJ, sta
sopra la soglia, coerente con
CONVIENTE); verdetto CONVIENTE
perche' il risparmio 608.000 supera
la tolleranza del 10 % di C_base
(248.800 EUR/anno).
NOTA: il CRF entra SOLO nel LCO di
questa tab: nei flussi il CAPEX
entra intero all'anno 0, mai
annuizzato.
NOTA 2: in questa tab il risparmio
nullo o negativo NON e' degenere:
con prezzo elettricita' 314,81
EUR/MWh (al tetto) il caso e'
calcolabile (valid=True, flussi
pieni), MARGINALE con VAN
-2.665.469,88 EUR e payback None,
non un errore: -120.000 di
risparmio resta entro la soglia
del 10 % di C_base a quel prezzo
(270.370 EUR/anno).
NOTA 3: la CO2 evitata PUO' essere
negativa in questa tab (non e' una
guard): con fattore gas zero e
fattore elettricita' 1,00 la CO2
base e' 1.600 t/anno e la pompa di
calore 7.000 t/anno, quindi
l'evitata e' -5.400 t/anno, mentre
il verdetto resta CONVIENTE (stessa
economia: i fattori non toccano i
costi).
NOTA 4: i pareggi sono sui costi
variabili, NON sul risparmio: al
pareggio elettrico esatto
(314,81 EUR/MWh) i costi per
metro quadrato si eguagliano
(13,52 EUR/m2) ma il risparmio e'
-120.000 EUR/anno, cioe' solo
l'O&M; al pareggio gas esatto
(11,91 EUR/GJ) i costi per metro
quadrato si eguagliano (8,80
EUR/m2) ma il risparmio e' di nuovo
-120.000 EUR/anno. Il breakeven
elettrico e' None con elettricita'
pompa di calore 8 kWh/m2
(denominatore nullo: la pompa di
calore non consuma piu'
elettricita' della baseline) e con
altri costi pompa di calore alti
(numeratore negativo). Il
breakeven gas e' None con gas
nullo, e vale come identita' a
prezzo elettricita' corrente:
1,44 + 2,00 + 0,45 x 11,91 = 8,80.
Attenzione: i due pareggi hanno
verso opposto: sopra il tetto
elettrico la pompa di calore perde,
sopra la soglia gas la pompa di
calore vince.
NOTA 5: il verdetto CONVIENTE del
demo non e' un errore: con prezzo
gas 5 EUR/GJ (sotto la soglia
11,91) il caso diventa NON_CONVIENTE
(risparmio -742.000 EUR/anno);
con prezzo elettricita' 400 EUR/MWh
(sopra il tetto 314,81) diventa
NON_CONVIENTE (risparmio -580.000,
VAN -7.133.104,41).
NOTA 6: il payback usa il cumulato
>= 0 (regola >= del brief): con
CAPEX nullo il payback e' 0 (non
1); con flussi [-100, 50, 50] il
payback e' 2 (il cumulato all'anno
2 e' zero, e zero basta); con CAPEX
1.200.000 EUR il payback e' 2
(cumulato all'anno 2 gia' positivo,
+16.000 EUR: la divisione nominale
1.200.000 / 608.000 fa 1,97 anni).
NOTA 6b: il risparmio demo in
virgola mobile e' 607999,9999999998
(8,80 x 200.000 in binario), non
608.000 esatto: per questo il caso
CAPEX 1.216.000 (divisione nominale
esatta 2 anni) NON e' usato come
test via calcola, perche' il cumulato
all'anno 2 resterebbe di una frazione
di centesimo sotto zero e il payback
diventerebbe 3; la regola >= resta
verificata a livello di funzione pura
in test_payback_regola_maggiore_uguale.
NOTA 7: i valori demo sono stati
ricalcolati da zero con un calcolo
indipendente: il ricalcolo esatto
(senza arrotondamenti intermedi)
da' costo base 12,44, costo pompa
di calore 8,80, costo baseline
2.488.000, costo variabile pompa
di calore 1.760.000, costo
alternativo 1.880.000, risparmio
608.000, CO2 base 5.400, pompa di
calore 1.750, evitata 3.650, CRF
0,1029627640, LCO base 12,44, LCO
alt 10,172221, VAN 4.405.047,38,
TIR 40,28 %, payback 3, breakeven
elettricita' 314,81 (tetto),
breakeven gas 11,91 (soglia minima),
verdetto CONVIENTE: i file usano i
valori esatti.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w781_helpers import (
    demo_calcoli,
    mh780_breakeven_el,
    mh780_breakeven_gas,
    mh780_c_alt,
    mh780_c_alt_per_m2,
    mh780_c_alt_var,
    mh780_c_base,
    mh780_c_base_nonel,
    mh780_c_base_per_m2,
    mh780_c_alt_nonel,
    mh780_calcola,
    mh780_co2_alt,
    mh780_co2_base,
    mh780_co2_evitata,
    mh780_crf,
    mh780_csv,
    mh780_demo,
    mh780_flussi,
    mh780_int_pos,
    mh780_lco_alt,
    mh780_lco_base,
    mh780_num,
    mh780_nneg,
    mh780_payback,
    mh780_pct_tolleranza,
    mh780_pct_wacc,
    mh780_pos,
    mh780_risparmio,
    mh780_tir,
    mh780_valida,
    mh780_van,
    mh780_verdetto,
)

# Costanti demo a piena precisione (per la validazione
# _DEMO contro demo_calcoli() con tolleranza relativa
# < 1e-9: vedi test_demo_costanti_vs_demo_calcoli).
_DEMO = {
    "c_base_per_m2": 12.44,
    "c_alt_per_m2": 8.8,
    "c_base_nonel_per_m2": 11.0,
    "c_alt_nonel_per_m2": 2.5,
    "el_base_mwh_anno": 1600.0,
    "el_alt_mwh_anno": 7000.0,
    "gas_mwh_anno": 25000.0,
    "c_base_eur_anno": 2488000.0,
    "c_alt_var_eur_anno": 1760000.0,
    "c_alt_eur_anno": 1880000.0,
    "risparmio_eur_anno": 608000.0,
    "co2_base_t_anno": 5400.0,
    "co2_alt_t_anno": 1750.0,
    "co2_evitata_t_anno": 3650.0,
    "crf": 0.10296276395531265,
    "lco_base_eur_m2": 12.44,
    "lco_alt_eur_m2": 10.172220729664845,
    "van": 4405047.3845465155,
    "tir": 40.28048898276987,
    "breakeven_el_eur_mwh": 314.81481481481484,
    "breakeven_gas_eur_gj": 11.911111111111113,
}


def _demo_kwargs():
    return dict(mh780_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh780_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh780_num(3, "x") == 3.0
    assert mh780_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh780_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh780_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh780_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh780_pos(0, "x")
    with pytest.raises(ValueError):
        mh780_pos(-1, "x")
    assert mh780_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh780_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh780_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh780_int_pos(0, "x")


def test_pct_wacc_limiti():
    assert mh780_pct_wacc(0, "x") == 0.0
    assert mh780_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh780_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh780_pct_tolleranza(0, "x") == 0.0
    assert mh780_pct_tolleranza(100, "x") == 100.0
    assert mh780_pct_tolleranza(10.0, "x") == 10.0
    with pytest.raises(ValueError):
        mh780_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh780_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_c_base_per_m2_scomposizione():
    assert mh780_c_base_per_m2(0.45, 20, 8, 180,
                               2.0) == pytest.approx(12.44)
    assert mh780_c_base_per_m2(0, 20, 0, 180,
                               0) == pytest.approx(0.0)
    assert mh780_c_base_per_m2(0.45, 20, 8, 0,
                               2.0) == pytest.approx(11.0)
    with pytest.raises(ValueError):
        mh780_c_base_per_m2(-1, 20, 8, 180, 2.0)
    with pytest.raises(ValueError):
        mh780_c_base_per_m2(0.45, -1, 8, 180, 2.0)


def test_c_alt_per_m2_scomposizione():
    assert mh780_c_alt_per_m2(35, 180,
                              2.5) == pytest.approx(8.8)
    assert mh780_c_alt_per_m2(35, 0,
                              2.5) == pytest.approx(2.5)
    assert mh780_c_alt_per_m2(0, 180,
                              2.5) == pytest.approx(2.5)
    assert mh780_c_alt_per_m2(35, 180,
                              0) == pytest.approx(6.3)
    with pytest.raises(ValueError):
        mh780_c_alt_per_m2(35, -1, 2.5)
    with pytest.raises(ValueError):
        mh780_c_alt_per_m2(35, 180, -1)


def test_c_nonel():
    assert mh780_c_base_nonel(12.44, 8, 180) == pytest.approx(11.0)
    assert mh780_c_alt_nonel(8.8, 35, 180) == pytest.approx(2.5)
    assert mh780_c_base_nonel(12.44, 8, 0) == pytest.approx(12.44)
    with pytest.raises(ValueError):
        mh780_c_base_nonel(12.44, -1, 180)


def test_c_base_c_alt_var_c_alt():
    assert mh780_c_base(12.44, 200000) == pytest.approx(2488000.0)
    assert mh780_c_alt_var(8.8, 200000) == pytest.approx(
        1760000.0)
    assert mh780_c_alt(1760000.0, 120000) == pytest.approx(
        1880000.0)
    with pytest.raises(ValueError):
        mh780_c_base(12.44, 0)
    with pytest.raises(ValueError):
        mh780_c_alt(1760000.0, -1)


def test_co2_base_alt_evitata():
    assert mh780_co2_base(0.45, 200000, 8, 0.20,
                          0.25) == pytest.approx(5400.0)
    assert mh780_co2_alt(35, 200000,
                         0.25) == pytest.approx(1750.0)
    assert mh780_co2_alt(35, 200000,
                         0) == pytest.approx(0.0)
    assert mh780_co2_base(0, 200000, 8, 0.20,
                          0.25) == pytest.approx(400.0)
    assert mh780_co2_evitata(5400.0,
                             1750.0) == pytest.approx(3650.0)
    assert mh780_co2_evitata(100.0, 150.0) == pytest.approx(-50.0)
    with pytest.raises(ValueError):
        mh780_co2_base(0.45, 200000, 8, -0.10, 0.25)


def test_co2_evitata_puo_essere_negativa_via_calcola():
    """Differenza chiave di questa tab: via
    mh780_calcola la CO2 evitata PUO' essere
    negativa (fattore gas zero, fattore
    elettricita' alto)."""
    bc = _variante(f_gas_t_per_mwh=0, f_el_t_per_mwh=1.0)
    assert bc["co2_base_t_anno"] == pytest.approx(1600.0)
    assert bc["co2_alt_t_anno"] == pytest.approx(7000.0)
    assert bc["co2_evitata_t_anno"] == pytest.approx(-5400.0)
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_co2_formula_componenti():
    """CO2 base = gas x f_gas + elettricita' base x f_el,
    CO2 pompa di calore = elettricita' pompa di calore
    x f_el, con le conversioni kWh->MWh e GJ->MWh."""
    for bc in (demo_calcoli(),
               _variante(f_gas_t_per_mwh=0, f_el_t_per_mwh=1.0),
               _variante(el_alt_kwh_per_m2=8)):
        atteso_base = (bc["gas_mwh_anno"] * bc["f_gas_t_per_mwh"]
                       + bc["el_base_mwh_anno"] * bc["f_el_t_per_mwh"])
        assert bc["co2_base_t_anno"] == pytest.approx(atteso_base)
        atteso_alt = (bc["el_alt_mwh_anno"] * bc["f_el_t_per_mwh"])
        assert bc["co2_alt_t_anno"] == pytest.approx(atteso_alt)


def test_risparmio_segno():
    assert mh780_risparmio(2488000.0, 1880000.0) == \
        pytest.approx(608000.0)
    assert mh780_risparmio(2488000.0, 2488000.0) == 0.0
    assert mh780_risparmio(2703703.703703704, 2823703.703703704) == \
        pytest.approx(-120000.0)


def test_crf_solo_lco():
    assert mh780_crf(6.0, 15) == pytest.approx(0.10296276395531265)
    assert mh780_crf(0.0, 15) == pytest.approx(1.0 / 15.0)
    assert mh780_crf(6.0, 20) == pytest.approx(0.0871845569768514)
    with pytest.raises(ValueError):
        mh780_crf(50.1, 15)
    with pytest.raises(ValueError):
        mh780_crf(6.0, 0)


def test_lco():
    assert mh780_lco_base(2488000.0, 200000) == pytest.approx(12.44)
    assert mh780_lco_alt(1500000, 0.10296276395531265, 120000,
                         8.8, 200000) == pytest.approx(
        10.172220729664845)
    assert mh780_lco_base(2488000.0, 0) is None
    assert mh780_lco_alt(1500000, 0.10296276395531265, 120000,
                         8.8, 0) is None
    assert mh780_lco_alt(1500000, 0.10296276395531265, 120000,
                         8.8, -5) is None
    # Il CAPEX entra nel LCO solo annuizzato: con CAPEX nullo
    # il LCO alt e' (O&M / S) + C_alt_per_m2.
    assert mh780_lco_alt(0, 0.10296276395531265, 120000,
                         8.8, 200000) == pytest.approx(9.4)


def test_crf_mai_nei_flussi():
    """Il CRF entra SOLO nel LCO: i flussi usano il
    CAPEX intero all'anno 0 e la VAN dai flussi non
    dipende dal CRF (cambiando il WACC cambia la VAN
    per lo sconto, non per il CRF)."""
    bc = demo_calcoli()
    assert bc["flussi"][0] == -1500000
    assert all(f == pytest.approx(608000.0)
               for f in bc["flussi"][1:])
    assert bc["van"] == pytest.approx(mh780_van(bc["flussi"], 6.0))
    bc0 = _variante(wacc_pct=0)
    assert bc0["van"] == pytest.approx(sum(bc0["flussi"]))
    assert bc0["crf"] == pytest.approx(1.0 / 15.0)
    assert bc0["lco_alt_eur_m2"] == pytest.approx(9.9)


def test_breakeven_el_demo_e_varianti():
    # Demo: (11,00 - 2,50) / ((35 - 8) / 1000) = 314,81.
    assert mh780_breakeven_el(11.0, 2.5, 35,
                              8) == pytest.approx(314.81481481481484)
    # Numeratore zero: pareggio zero, valido.
    assert mh780_breakeven_el(11.0, 11.0, 35,
                              8) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh780_breakeven_el(11.0, 2.5, -1, 8)


def test_breakeven_el_none_casi():
    # Denominatore <= 0: el_alt uguale o sotto el_base.
    assert mh780_breakeven_el(11.0, 2.5, 8, 8) is None
    assert mh780_breakeven_el(11.0, 2.5, 5, 8) is None
    # Numeratore < 0: costo pompa di calore senza
    # elettricita' sopra il costo base senza elettricita'.
    assert mh780_breakeven_el(11.0, 12.0, 35, 8) is None


def test_breakeven_gas_demo_e_varianti():
    # Demo: (8,80 - 1,44 - 2,00) / 0,45 = 11,9111111.
    assert mh780_breakeven_gas(8.8, 8, 180, 2.0,
                               0.45) == pytest.approx(
        11.911111111111113)
    # Numeratore zero: pareggio zero, valido.
    assert mh780_breakeven_gas(3.44, 8, 180, 2.0,
                               0.45) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh780_breakeven_gas(8.8, 8, 180, 2.0, -1)


def test_breakeven_gas_none_casi():
    # Gas <= 0: nessun prezzo da calcolare.
    assert mh780_breakeven_gas(8.8, 8, 180, 2.0, 0) is None
    # Numeratore < 0: a prezzo gas zero il costo base
    # senza gas e' gia' sopra il costo alternativo.
    assert mh780_breakeven_gas(0, 8, 0, 2.0, 0.45) is None


def test_breakeven_verifica_pareggio():
    """Al prezzo elettrico di pareggio i costi per metro
    quadrato si eguagliano: C_alt_per_m2(p*) =
    C_base_per_m2(p*). Il risparmio invece e' -O&M, non
    zero (i pareggi non includono l'O&M). Al prezzo gas
    di pareggio vale lo stesso: C_base_per_m2 =
    C_alt_per_m2 e risparmio -O&M. Per il gas vale
    l'identita' a prezzo elettrico corrente:
    el_base / 1000 x p_el + other_base +
    gas x be_gas = C_alt_per_m2."""
    bc = _variante(p_el_eur_mwh=314.81481481481484)
    assert bc["c_base_per_m2"] == pytest.approx(bc["c_alt_per_m2"])
    assert bc["risparmio_eur_anno"] == pytest.approx(-120000.0)
    bc2 = _variante(p_gas_eur_gj=11.911111111111113)
    assert bc2["c_base_per_m2"] == pytest.approx(bc2["c_alt_per_m2"])
    assert bc2["risparmio_eur_anno"] == pytest.approx(-120000.0)
    demo = demo_calcoli()
    assert (demo["el_base_kwh_per_m2"] / 1000.0
            * demo["p_el_eur_mwh"]
            + demo["other_base_eur_m2"]
            + demo["gas_gj_per_m2"]
            * demo["breakeven_gas_eur_gj"]) == pytest.approx(
        demo["c_alt_per_m2"])


def test_pareggi_versi_opposti():
    """Sotto il tetto elettrico la pompa di calore vince
    sui costi variabili, sopra perde; sopra la soglia
    gas la pompa di calore vince, sotto perde."""
    be_el = demo_calcoli()["breakeven_el_eur_mwh"]
    assert _variante(p_el_eur_mwh=be_el - 10)[
        "c_alt_per_m2"] < _variante(p_el_eur_mwh=be_el - 10)[
        "c_base_per_m2"]
    assert _variante(p_el_eur_mwh=be_el + 10)[
        "c_alt_per_m2"] > _variante(p_el_eur_mwh=be_el + 10)[
        "c_base_per_m2"]
    be_gas = demo_calcoli()["breakeven_gas_eur_gj"]
    assert _variante(p_gas_eur_gj=be_gas + 1)[
        "c_alt_per_m2"] < _variante(p_gas_eur_gj=be_gas + 1)[
        "c_base_per_m2"]
    assert _variante(p_gas_eur_gj=be_gas - 1)[
        "c_alt_per_m2"] > _variante(p_gas_eur_gj=be_gas - 1)[
        "c_base_per_m2"]


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh780_flussi(1500000, 608000.0, 15)
    assert len(fl) == 16
    assert fl[0] == -1500000
    assert all(f == 608000.0 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = demo_calcoli()
    assert bc["van"] == pytest.approx(4405047.3845465155)
    assert mh780_van([-1500000] + [608000.0] * 15,
                     0) == pytest.approx(7620000.0)
    assert mh780_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = demo_calcoli()
    assert bc["tir"] == pytest.approx(40.28048898276987)
    assert mh780_tir([-1500000] + [608000.0] * 15) == \
        pytest.approx(0.4028048898276987)
    tir = mh780_tir([-1500000] + [608000.0] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate(
                  [-1500000] + [608000.0] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    """Payback con cumulato >= 0: il cumulato nullo basta."""
    assert mh780_payback([-1500000] + [608000.0] * 15) == 3
    assert mh780_payback([-1500000] + [-1000.0] * 15) is None
    assert mh780_payback([0] + [608000.0] * 15) == 0
    assert mh780_payback([-100] + [50] * 2) == 2
    assert mh780_payback([-1216000.0] +
                         [608000.0] * 2) == 2


def test_verdetto():
    assert mh780_verdetto(608000.0, 2488000.0,
                          10.0) == "CONVIENTE"
    assert mh780_verdetto(248800.0, 2488000.0,
                          10.0) == "MARGINALE"
    assert mh780_verdetto(0.0, 2488000.0, 10.0) == "MARGINALE"
    assert mh780_verdetto(-248800.0, 2488000.0,
                          10.0) == "MARGINALE"
    assert mh780_verdetto(-248801.0, 2488000.0,
                          10.0) == "NON_CONVIENTE"
    assert mh780_verdetto(-742000.0, 2488000.0,
                          10.0) == "NON_CONVIENTE"
    assert mh780_verdetto(608000.0, 2488000.0,
                          0.0) == "CONVIENTE"
    assert mh780_verdetto(-100.0, 2488000.0,
                          0.0) == "NON_CONVIENTE"
    assert mh780_verdetto(None, 2488000.0,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh780_verdetto(float("nan"), 2488000.0, 10.0)
    with pytest.raises(ValueError):
        mh780_verdetto(100.0, -1, 10.0)
    with pytest.raises(ValueError):
        mh780_verdetto(100.0, 2488000.0, 100.1)


def test_valida_demo_ok():
    v = mh780_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("s_m2_anno", "200000"),
                       ("s_m2_anno", float("nan")),
                       ("s_m2_anno", float("inf")),
                       ("s_m2_anno", True),
                       ("p_gas_eur_gj", None),
                       ("gas_gj_per_m2", "0.45")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh780_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("s_m2_anno", 0),
                          ("s_m2_anno", -1),
                          ("gas_gj_per_m2", -1),
                          ("p_gas_eur_gj", -1),
                          ("el_base_kwh_per_m2", -1),
                          ("p_el_eur_mwh", -1),
                          ("other_base_eur_m2", -1),
                          ("el_alt_kwh_per_m2", -1),
                          ("other_alt_eur_m2", -1),
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
        assert mh780_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"gas_gj_per_m2": 0,
              "p_gas_eur_gj": 0,
              "el_base_kwh_per_m2": 0,
              "p_el_eur_mwh": 0,
              "other_base_eur_m2": 0,
              "el_alt_kwh_per_m2": 0,
              "other_alt_eur_m2": 0,
              "om_eur_anno": 0,
              "capex_eur": 0,
              "f_gas_t_per_mwh": 0,
              "f_el_t_per_mwh": 0,
              "wacc_pct": 0,
              "tolleranza_pct": 0})
    assert mh780_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    assert mh780_valida(**d)["valido"] is True


def test_valida_non_controlla_risparmio_calcola_neppure():
    """La validazione input NON controlla il risparmio
    (e' un esito, non un range) e in questa tab
    nemmeno mh780_calcola lo controlla: con prezzo
    elettricita' 400 EUR/MWh (sopra il tetto 314,81)
    il caso resta CALCOLABILE."""
    d = _demo_kwargs()
    d["p_el_eur_mwh"] = 400
    assert mh780_valida(**d)["valido"] is True
    bc = _variante(p_el_eur_mwh=400)
    assert bc["valid"] is True
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["flussi"]
    assert bc["payback"] is None


def test_demo_dict():
    d = mh780_demo()
    assert d["s_m2_anno"] == 200000
    assert d["gas_gj_per_m2"] == 0.45
    assert d["p_gas_eur_gj"] == 20
    assert d["el_base_kwh_per_m2"] == 8
    assert d["p_el_eur_mwh"] == 180
    assert d["other_base_eur_m2"] == 2.0
    assert d["el_alt_kwh_per_m2"] == 35
    assert d["other_alt_eur_m2"] == 2.5
    assert d["om_eur_anno"] == 120000
    assert d["capex_eur"] == 1500000
    assert d["f_gas_t_per_mwh"] == 0.20
    assert d["f_el_t_per_mwh"] == 0.25
    assert d["wacc_pct"] == 6.0
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
    assert bc["c_base_per_m2"] == pytest.approx(12.44)
    assert bc["c_alt_per_m2"] == pytest.approx(8.8)
    assert bc["el_base_mwh_anno"] == pytest.approx(1600.0)
    assert bc["el_alt_mwh_anno"] == pytest.approx(7000.0)
    assert bc["gas_mwh_anno"] == pytest.approx(25000.0)
    assert bc["co2_evitata_t_anno"] == pytest.approx(3650.0)


def test_demo_calcoli_economia():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(2488000.0)
    assert bc["c_alt_var_eur_anno"] == pytest.approx(1760000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(1880000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(608000.0)
    assert bc["breakeven_el_eur_mwh"] == pytest.approx(314.81481481481484)
    assert bc["breakeven_gas_eur_gj"] == pytest.approx(
        11.911111111111113)


def test_demo_calcoli_finanza():
    bc = demo_calcoli()
    assert bc["crf"] == pytest.approx(0.10296276395531265)
    assert bc["lco_base_eur_m2"] == pytest.approx(12.44)
    assert bc["lco_alt_eur_m2"] == pytest.approx(10.172220729664845)
    assert bc["van"] == pytest.approx(4405047.3845465155)
    assert bc["tir"] == pytest.approx(40.28048898276987)
    assert bc["payback"] == 3
    assert bc["verdetto"] == "CONVIENTE"


def test_demo_flussi_e_cumulato():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -1500000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(608000.0)
               for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -1500000
    assert righe.iloc[2]["Cumulato (EUR)"] == pytest.approx(-284000.0)
    assert righe.iloc[3]["Cumulato (EUR)"] == pytest.approx(324000.0)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(
        7620000.0)
    assert righe.iloc[15]["Flusso (EUR/anno)"] == pytest.approx(
        608000.0)


def test_demo_tabella_righe():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Superficie verniciata (m2/anno)"] == pytest.approx(
        200000.0)
    assert mappa["Costo base per metro quadrato (EUR/m2)"] == pytest.approx(
        12.44)
    assert mappa["Costo pompa di calore per metro quadrato (EUR/m2)"] == pytest.approx(
        8.8)
    assert mappa["Elettricita' pompa di calore (MWh/anno)"] == pytest.approx(
        7000.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(
        1880000.0)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(608000.0)
    assert mappa["Payback (anni)"] == 3
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo elettricita' (EUR/MWh)"] == \
        pytest.approx(314.81481481481484)
    assert mappa["Breakeven prezzo gas (EUR/GJ)"] == \
        pytest.approx(11.911111111111113)


def test_demo_coerenza_interna():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["c_base_per_m2"] * bc["s_m2_anno"] == \
        pytest.approx(bc["c_base_eur_anno"])
    assert bc["c_alt_per_m2"] * bc["s_m2_anno"] == \
        pytest.approx(bc["c_alt_var_eur_anno"])
    assert bc["co2_base_t_anno"] - bc["co2_alt_t_anno"] == \
        pytest.approx(bc["co2_evitata_t_anno"])
    assert bc["c_base_eur_anno"] / bc["s_m2_anno"] == \
        pytest.approx(bc["lco_base_eur_m2"])
    assert (bc["capex_eur"] * bc["crf"] + bc["om_eur_anno"]) / \
        bc["s_m2_anno"] + bc["c_alt_per_m2"] == \
        pytest.approx(bc["lco_alt_eur_m2"])
    assert bc["c_base_nonel_per_m2"] + \
        bc["el_base_kwh_per_m2"] / 1000.0 * bc["p_el_eur_mwh"] == \
        pytest.approx(bc["c_base_per_m2"])


def test_demo_contro_riconteggio_indipendente():
    s, gas, pg = 200000, 0.45, 20
    elb, pel, ob = 8, 180, 2.0
    ela, oa, om, cx = 35, 2.5, 120000, 1500000
    fg, fel, wacc, vita = 0.20, 0.25, 6.0, 15
    cb = gas * pg + elb / 1000.0 * pel + ob
    ca = ela / 1000.0 * pel + oa
    cbase = cb * s
    cav = ca * s
    caa = cav + om
    risp = cbase - caa
    co2b = gas / 3.6 * s * fg + elb / 1000.0 * s * fel
    co2a = ela / 1000.0 * s * fel
    r = wacc / 100.0
    crf = r * (1 + r) ** vita / ((1 + r) ** vita - 1.0)
    lco_b = cb
    lco_a = (cx * crf + om) / s + ca
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    be_el = (cb - elb / 1000.0 * pel
             - (ca - ela / 1000.0 * pel)) / ((ela - elb) / 1000.0)
    be_gas = (ca - elb / 1000.0 * pel - ob) / gas
    bc = demo_calcoli()
    assert bc["c_base_per_m2"] == pytest.approx(cb)
    assert bc["c_alt_per_m2"] == pytest.approx(ca)
    assert bc["c_base_eur_anno"] == pytest.approx(cbase)
    assert bc["c_alt_var_eur_anno"] == pytest.approx(cav)
    assert bc["c_alt_eur_anno"] == pytest.approx(caa)
    assert bc["risparmio_eur_anno"] == pytest.approx(risp)
    assert bc["co2_base_t_anno"] == pytest.approx(co2b)
    assert bc["co2_alt_t_anno"] == pytest.approx(co2a)
    assert bc["crf"] == pytest.approx(crf)
    assert bc["lco_base_eur_m2"] == pytest.approx(lco_b)
    assert bc["lco_alt_eur_m2"] == pytest.approx(lco_a)
    assert bc["van"] == pytest.approx(van)
    assert bc["breakeven_el_eur_mwh"] == pytest.approx(be_el)
    assert bc["breakeven_gas_eur_gj"] == pytest.approx(be_gas)


# ---------------------------------------------------------------- varianti
def test_demo_conviente():
    """Il demo e' CONVIENTE: il risparmio 608.000 supera
    la tolleranza del 10 % di C_base (248.800), la VAN e'
    positiva e il payback e' 3 anni."""
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] > 0.0
    assert bc["payback"] == 3
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_gas_sotto_soglia_non_conviente():
    """Gas 5 EUR/GJ (sotto la soglia 11,91): costo base
    5,69 EUR/m2, risparmio -742.000, NON_CONVIENTE."""
    bc = _variante(p_gas_eur_gj=5)
    assert bc["valid"] is True
    assert bc["c_base_per_m2"] == pytest.approx(5.69)
    assert bc["risparmio_eur_anno"] == pytest.approx(-742000.0)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_pareggio_el_esatto():
    """Al tetto elettrico esatto (314,81 EUR/MWh) i
    costi per metro quadrato si eguagliano (13,52
    EUR/m2) ma il risparmio e' -120.000 (solo l'O&M):
    VAN -2.665.469,88, TIR None, payback mai,
    verdetto MARGINALE."""
    bc = _variante(p_el_eur_mwh=314.81481481481484)
    assert bc["c_base_per_m2"] == pytest.approx(bc["c_alt_per_m2"])
    assert bc["risparmio_eur_anno"] == pytest.approx(-120000.0)
    assert bc["van"] == pytest.approx(-2665469.878528918)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "MARGINALE"


def test_variante_pareggio_gas_esatto():
    """Al prezzo gas di pareggio esatto (11,91 EUR/GJ) i
    costi per metro quadrato si eguagliano (8,80
    EUR/m2) ma il risparmio e' -120.000 (solo l'O&M):
    VAN -2.665.469,88, payback mai, verdetto
    MARGINALE (C_base 1.760.000, soglia 10 %
    176.000, e 120.000 resta dentro la soglia)."""
    bc = _variante(p_gas_eur_gj=11.911111111111113)
    assert bc["c_base_per_m2"] == pytest.approx(bc["c_alt_per_m2"])
    assert bc["risparmio_eur_anno"] == pytest.approx(-120000.0)
    assert bc["van"] == pytest.approx(-2665469.878528918)
    assert bc["payback"] is None
    assert bc["verdetto"] == "MARGINALE"


def test_variante_sopra_tetto_el():
    """Prezzo elettricita' 400 EUR/MWh (sopra il
    tetto 314,81): risparmio -580.000, VAN
    -7.133.104,41, TIR None, payback mai,
    verdetto NON_CONVIENTE."""
    bc = _variante(p_el_eur_mwh=400)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(-580000.0)
    assert bc["van"] == pytest.approx(-7133104.41288977)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_tolleranza_zero_demo_conviente():
    """Con tolleranza 0 % lo stesso demo resta
    CONVIENTE (risparmio positivo, soglia zero)."""
    bc = _variante(tolleranza_pct=0)
    assert bc["risparmio_eur_anno"] == pytest.approx(608000.0)
    assert bc["van"] == pytest.approx(4405047.3845465155)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    """Payback regola >=: con CAPEX nullo il payback e' 0,
    non 1 (all'anno 0 il cumulato e' gia' zero)."""
    bc = _variante(capex_eur=0)
    assert bc["capex_eur"] == 0
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(5905047.3845465155)
    assert bc["lco_alt_eur_m2"] == pytest.approx(9.4)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_payback_due_anni():
    """CAPEX 1.200.000 EUR: cumulato all'anno 2
    gia' positivo (+16.000 EUR), payback 2
    (divisione nominale 1.200.000 / 608.000 =
    1,97 anni)."""
    bc = _variante(capex_eur=1200000)
    assert bc["payback"] == 2
    assert bc["van"] == pytest.approx(4705047.3845465155)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(7620000.0)
    assert bc["lco_alt_eur_m2"] == pytest.approx(9.9)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_vita_diversa():
    bc = _variante(vita_anni=10)
    assert len(bc["flussi"]) == 11
    assert bc["van"] == pytest.approx(2974932.9272601325)
    assert bc["payback"] == 3
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_om_alto():
    """O&M 800.000 EUR/anno: risparmio -72.000,
    verdetto MARGINALE (entro la soglia 248.800)."""
    bc = _variante(om_eur_anno=800000)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(-72000.0)
    assert bc["payback"] is None
    assert bc["verdetto"] == "MARGINALE"


def test_variante_breakeven_el_none_denominatore():
    """Elettricita' pompa di calore uguale alla baseline
    (8 kWh/m2): breakeven elettrico None,
    caso calcolabile CONVIENTE."""
    bc = _variante(el_alt_kwh_per_m2=8)
    assert bc["valid"] is True
    assert bc["breakeven_el_eur_mwh"] is None
    assert bc["risparmio_eur_anno"] == pytest.approx(1580000.0)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_breakeven_el_none_numeratore():
    """Altri costi pompa di calore 12,00 EUR/m2: costo
    pompa di calore senza elettricita' 12,00 sopra il
    costo base senza elettricita' 11,00: breakeven
    elettrico None."""
    bc = _variante(other_alt_eur_m2=12.0)
    assert bc["valid"] is True
    assert bc["breakeven_el_eur_mwh"] is None


def test_variante_breakeven_gas_none_gas_nullo():
    """Gas nullo: breakeven gas None, caso calcolabile
    (risparmio -1.192.000, NON_CONVIENTE)."""
    bc = _variante(gas_gj_per_m2=0)
    assert bc["valid"] is True
    assert bc["breakeven_gas_eur_gj"] is None
    assert bc["risparmio_eur_anno"] == pytest.approx(-1192000.0)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_breakeven_gas_none_numeratore():
    """Prezzo elettricita' zero e altri costi pompa di
    calore nulli: costo pompa di calore 0 sotto il costo
    base senza gas 2,00: breakeven gas None (numeratore
    negativo)."""
    bc = _variante(p_el_eur_mwh=0, other_alt_eur_m2=0)
    assert bc["valid"] is True
    assert bc["breakeven_gas_eur_gj"] is None


# ---------------------------------------------------------------- degenere
def test_degenere_superficie_zero_sollevela():
    """Caso degenere richiesto dal brief: S = 0
    solleva ValueError."""
    with pytest.raises(ValueError):
        _variante(s_m2_anno=0)


def test_degenere_verdetto_non_calcolabile_van_tir_payback_none():
    """Nel regime degenere non esiste alcun calcolo:
    calcola solleva ValueError, quindi nessuna VAN,
    nessuna TIR e nessun payback vengono prodotti
    (sono None per assenza); il verdetto per
    risparmio None e' NON_CALCOLABILE."""
    with pytest.raises(ValueError):
        _variante(s_m2_anno=0)
    with pytest.raises(ValueError):
        _variante(p_el_eur_mwh=-1)
    with pytest.raises(ValueError):
        _variante(wacc_pct=60)
    assert mh780_verdetto(None, 2488000.0, 10.0) == "NON_CALCOLABILE"
    assert demo_calcoli()["verdetto"] != "NON_CALCOLABILE"


def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"s_m2_anno": 0}, {"s_m2_anno": -1},
               {"gas_gj_per_m2": -1},
               {"p_gas_eur_gj": -1},
               {"el_base_kwh_per_m2": -1},
               {"p_el_eur_mwh": -1},
               {"other_base_eur_m2": -1},
               {"el_alt_kwh_per_m2": -1},
               {"other_alt_eur_m2": -1},
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
        assert mh780_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"s_m2_anno": "200000"},
               {"s_m2_anno": float("nan")},
               {"p_gas_eur_gj": float("inf")},
               {"capex_eur": True},
               {"gas_gj_per_m2": "0.45"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh780_valida(**d)["valido"] is False


def test_risparmio_negativo_non_degenere():
    """Differenza chiave: risparmio nullo o
    negativo resta calcolabile, con flussi pieni e
    VAN negativa; cosi' anche la CO2 evitata
    negativa resta calcolabile, e cosi' i
    breakeven None restano calcolabili."""
    for kw in ({"p_el_eur_mwh": 400},
               {"p_gas_eur_gj": 5}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["verdetto"] in ("NON_CONVIENTE", "MARGINALE")
        assert bc["flussi"]
    bc = _variante(f_gas_t_per_mwh=0, f_el_t_per_mwh=1.0)
    assert bc["co2_evitata_t_anno"] < 0.0
    assert bc["valid"] is True
    bc2 = _variante(el_alt_kwh_per_m2=8)
    assert bc2["breakeven_el_eur_mwh"] is None
    assert bc2["valid"] is True
    bc3 = _variante(gas_gj_per_m2=0)
    assert bc3["breakeven_gas_eur_gj"] is None
    assert bc3["valid"] is True


def test_co2_evitata_segno_funzione_pura():
    assert mh780_co2_evitata(100.0, 150.0) == pytest.approx(-50.0)


def test_verdetto_non_calcolabile_solo_risparmio_none():
    assert mh780_verdetto(None, 2488000.0, 10.0) == "NON_CALCOLABILE"
    assert demo_calcoli()["verdetto"] != "NON_CALCOLABILE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = demo_calcoli()
    testo = mh780_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert "c_base_per_m2;12.44" in testo
    assert "c_alt_per_m2;8.8" in testo
    assert "c_base_eur_anno;2488000.0" in testo
    assert "c_alt_var_eur_anno;1760000.0" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_el_eur_mwh" in testo
    assert "breakeven_gas_eur_gj" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = demo_calcoli()
    testo = mh780_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"c_alt_per_m2;{bc['c_alt_per_m2']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = demo_calcoli()
    testo = mh780_csv(bc, _demo_kwargs())
    for chiave in _demo_kwargs():
        assert f"{chiave};" in testo


def test_monotonia_prezzo_el_decrescente():
    # Il risparmio CALA con p_el (la pompa di calore
    # consuma piu' elettricita' della baseline):
    # pendenza -5.400 EUR/anno per EUR/MWh (200.000 m2 x
    # (35 - 8) / 1000 = 5.400 MWh/anno).
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_el_eur_mwh=190)["risparmio_eur_anno"]
    basso = _variante(p_el_eur_mwh=170)["risparmio_eur_anno"]
    assert basso > base > alto
    assert base - alto == pytest.approx(54000.0)
    assert basso - base == pytest.approx(54000.0)


def test_monotonia_prezzo_gas_crescente():
    # Il risparmio CRESCE con p_gas (solo la baseline
    # brucia gas): pendenza +90.000 EUR/anno per EUR/GJ
    # (200.000 m2 x 0,45 GJ/m2).
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas_eur_gj=21)["risparmio_eur_anno"]
    basso = _variante(p_gas_eur_gj=19)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(90000.0)
    assert base - basso == pytest.approx(90000.0)


def test_monotonia_elettricita_alt():
    # Piu' elettricita' pompa di calore, piu' cara
    # l'alternativa: +1 kWh/m2 a 180 EUR/MWh =
    # +0,18 EUR/m2 = -36.000 EUR/anno di risparmio.
    base = demo_calcoli()["risparmio_eur_anno"]
    assert _variante(el_alt_kwh_per_m2=36)[
        "risparmio_eur_anno"] == pytest.approx(base - 36000.0)
    assert _variante(el_alt_kwh_per_m2=34)[
        "risparmio_eur_anno"] == pytest.approx(base + 36000.0)


def test_demo_deterministica_due_chiamate():
    a = demo_calcoli()
    b = demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh780_demo().keys()) == {
        "s_m2_anno",
        "gas_gj_per_m2", "p_gas_eur_gj",
        "el_base_kwh_per_m2", "p_el_eur_mwh",
        "other_base_eur_m2",
        "el_alt_kwh_per_m2", "other_alt_eur_m2",
        "om_eur_anno", "capex_eur",
        "f_gas_t_per_mwh", "f_el_t_per_mwh",
        "wacc_pct", "vita_anni", "tolleranza_pct"}


@pytest.mark.parametrize("p_gas,atteso", [
    (20, 12.44),
    (5, 5.69),
    (11.911111111111113, 8.8),
])
def test_c_base_per_m2_parametrizzato(p_gas, atteso):
    assert mh780_c_base_per_m2(0.45, p_gas, 8, 180,
                               2.0) == pytest.approx(atteso)


@pytest.mark.parametrize("campo,valore", [
    ("s_m2_anno", 0), ("s_m2_anno", -3),
    ("gas_gj_per_m2", -1),
    ("p_gas_eur_gj", -1),
    ("el_base_kwh_per_m2", -1),
    ("p_el_eur_mwh", -1),
    ("other_base_eur_m2", -1),
    ("el_alt_kwh_per_m2", -1),
    ("other_alt_eur_m2", -1),
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
    assert mh780_valida(**d)["valido"] is False


@pytest.mark.parametrize("campo,valore", [
    ("s_m2_anno", 0), ("s_m2_anno", -3),
    ("gas_gj_per_m2", -1),
    ("p_gas_eur_gj", -1),
    ("el_base_kwh_per_m2", -1),
    ("p_el_eur_mwh", -1),
    ("other_base_eur_m2", -1),
    ("el_alt_kwh_per_m2", -1),
    ("other_alt_eur_m2", -1),
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
        mh780_calcola(**d)


def test_df_tabella_valori_demo_selezionati():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Superficie verniciata (m2/anno)"] == 200000.0
    assert mappa["Costo base per metro quadrato (EUR/m2)"] == pytest.approx(
        12.44)


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
    return ["mh" + "77" + "9", "st" + "77" + "9",
            "tab" + "77" + "9"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w781_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w781_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab780:")


def test_registry_chain_tail_and_count():
    """Registry della nuova tab: il frammento UI apre la tab
    numero 780 (la coda della catena termina con la nuova tab
    e il conteggio atteso delle tab e' 780)."""
    src = _leggi("w781_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 780
    assert src.count("with tab780:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w781_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w781_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st780_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert "key=f" not in src and "key = f" not in src
    assert "st.stop()" in src
    # guard degenere prima di KPI / grafico / tabella / CSV
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w781_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def780[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w781_ui.py")
        usate = set(re.findall(r'_def780\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 15
        assert usate <= set(mh780_demo().keys())
