"""Test tab777 "Acciaieria: forno
elettrico ad arco (EAF) vs altoforno
- quando il rottame batte la ghisa?"
(File repo: tests/test_w777_acciaieria.py,
contenuto pronto da scrivere in repo.)

Nuova tab tab777 (acciaieria, file di
lavoro w778). Business case
deterministico di un'acciaieria:
produzione P t/anno di acciaio;
baseline altoforno BF-BOF con costo
per tonnellata C_bf_per_t =
coke x p_coke + el_bf / 1000 x p_el
+ ore x p_ore + other_bf EUR/t
(el_bf in kWh/t: 1 MWh = 1000 kWh);
alternativa EAF a rottame con costo
per tonnellata C_eaf_per_t = scrap
x p_scrap + el_eaf / 1000 x p_el +
gas x p_gas + electrodes x p_elec +
other_eaf EUR/t; costi annui C_base
= C_bf_per_t x P, C_eaf_var =
C_eaf_per_t x P, C_alt = C_eaf_var
+ O&M; risparmio = C_base - C_alt
EUR/anno; CO2 base = f_bf x P
t/anno (f_bf in tCO2/t acciaio);
CO2 EAF = el_eaf / 1000 x P x f_el
+ gas x P / 3,6 x f_gas t/anno
(gas in GJ/t: 1 MWh = 3,6 GJ;
fattori in tCO2/MWh); CO2 evitata =
CO2 base - CO2 EAF t/anno, PUO'
ESSERE NEGATIVA in questa tab
(elettricita' sporca, o fattore
altoforno basso: l'EAF puo' emettere
piu' della baseline): NON e' una
guard, NON e' un degenere, NON
monetizzata; CRF = r (1 + r)^n /
((1 + r)^n - 1) con r = WACC come
frazione, r = 0 -> 1/n, SOLO nel
LCO, MAI nei flussi; LCO base =
C_bf_per_t EUR/t; LCO alt =
(CAPEX x CRF + O&M) / P + C_eaf_per_t
EUR/t (il CAPEX entra solo
annuizzato col CRF); breakeven
prezzo elettricita' p_el* =
(C_bf_nonel - C_eaf_nonel) /
((el_eaf - el_bf) / 1000) EUR/MWh,
None se denominatore <= 0 (l'EAF
non consuma piu' elettricita' della
baseline) e None se numeratore < 0
(a prezzo elettrico zero l'EAF e'
gia' piu' caro e il divario cresce
con p_el); breakeven prezzo rottame
p_scrap* = (C_bf_per_t -
C_eaf_non_scrap) / scrap EUR/t,
None se scrap <= 0 e None se
numeratore < 0; entrambi i pareggi,
quando esistono, sono TETTI
(ceiling), non pavimenti: il
risparmio CALA con p_el (l'EAF
consuma piu' elettricita' della
baseline) e CALA con p_scrap; i
pareggi sono sui costi variabili e
NON includono l'O&M: al pareggio
esatto il risparmio e' -O&M, non
zero; flussi [-CAPEX, risparmio
x vita]; VAN, TIR, payback (primo
anno con cumulato >= 0, regola >=
del brief: con CAPEX nullo il
payback e' 0, con divisione esatta
CAPEX / risparmio il payback e'
l'anno della divisione esatta).
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
questa tab confronta EAF a rottame
contro altoforno BF-BOF per
tonnellata di acciaio, non EAF a
preridotto (DRI), non forno a
induzione, non alluminio, non rame.

Demo calcolata eseguendo
demo_calcoli() e ricontrollata con
un ricalcolo indipendente da zero
(riga per riga): produzione acciaio
500.000 t/anno, altoforno BF-BOF
con coke 14 GJ/t a 12 EUR/GJ,
elettricita' 150 kWh/t a 80 EUR/MWh,
minerale 1,6 t/t a 110 EUR/t, altri
costi 40 EUR/t; EAF a rottame con
rottame 1,05 t/t a 260 EUR/t,
elettricita' 450 kWh/t, gas 1,2 GJ/t
a 18 EUR/GJ, elettrodi 2 kg/t a 5
EUR/kg, altri costi 35 EUR/t; O&M
annuo 2.000.000 EUR/anno, CAPEX
60.000.000 EUR, fattore altoforno
1,9 tCO2/t, fattore elettricita'
0,35 tCO2/MWh, fattore gas 0,20
tCO2/MWh, WACC 6 %, vita 20 anni,
tolleranza MARGINALE 10 % di C_base.

- c_bf_per_t = 396.0
- c_eaf_per_t = 375.6
- c_bf_nonel_per_t = 384.0
- c_eaf_nonel_per_t = 339.6
- c_eaf_non_scrap_per_t = 102.60000000000002
- el_bf_mwh_anno = 75000.0
- el_eaf_mwh_anno = 225000.0
- gas_mwh_anno = 166666.66666666666
- c_base_eur_anno = 198000000.0
- c_eaf_var_eur_anno = 187800000.0
- c_alt_eur_anno = 189800000.0
- risparmio_eur_anno = 8200000.0
- co2_base_t_anno = 950000.0
- co2_eaf_t_anno = 112083.33333333334
- co2_evitata_t_anno = 837916.6666666666
- crf = 0.0871845569768514
- lco_base_eur_t = 396.0
- lco_alt_eur_t = 390.0621468372222
- van = 34053353.992235065
- tir = 12.331112926146998
- payback = 8
- breakeven_el_eur_mwh = 147.99999999999994
- breakeven_scrap_eur_t = 279.4285714285714
- verdetto = 'MARGINALE'

Scomposizione: costo BF = 14 x 12
= 168 di coke + 150 / 1000 x 80 =
12 di elettricita' + 1,6 x 110 =
176 di minerale + 40 altri = 396
EUR/t; costo EAF = 1,05 x 260 =
273 di rottame + 450 / 1000 x 80 =
36 di elettricita' + 1,2 x 18 =
21,60 di gas + 2 x 5 = 10 di
elettrodi + 35 altri = 375,60
EUR/t; costo base = 396 x 500.000
= 198.000.000 EUR/anno; costo
variabile EAF = 375,60 x 500.000 =
187.800.000 EUR/anno; costo
alternativo = 187.800.000 +
2.000.000 = 189.800.000 EUR/anno;
risparmio = 198.000.000 -
189.800.000 = 8.200.000 EUR/anno;
CO2 base = 1,9 x 500.000 =
950.000 t/anno; CO2 EAF = 450 /
1000 x 500.000 x 0,35 = 78.750 di
elettrica + 1,2 x 500.000 / 3,6 x
0,20 = 33.333,33 di gas =
112.083,33 t/anno; CO2 evitata =
950.000 - 112.083,33 = 837.916,67
t/anno; CRF al 6 % per 20 anni =
0,0871845570; LCO base 396,00
EUR/t; LCO alt = (60.000.000 x
0,0871845570 + 2.000.000) /
500.000 + 375,60 = 14,462147 +
375,60 = 390,062147 EUR/t; flussi:
anno 0 -60.000.000, anni 1-20
risparmio 8.200.000 (piatti); VAN
-60.000.000 + 8.200.000 x 11,469921
(annuita' 20 anni al 6 %) =
34.053.353,99 EUR; TIR 12,33 %;
payback 8 anni (il cumulato
all'anno 7 e' -2.600.000 EUR,
all'anno 8 e' 5.600.000 EUR, gia'
>= 0); breakeven elettricita' (384
- 339,60) / ((450 - 150) / 1000) =
44,40 / 0,30 = 148,00 EUR/MWh
(TETTO: sotto di esso l'EAF vince
sui costi variabili, sopra perde);
breakeven rottame (396 - 102,60) /
1,05 = 293,40 / 1,05 = 279,43
EUR/t (TETTO); verdetto MARGINALE
perche' il risparmio 8.200.000
resta entro la tolleranza del 10 %
di C_base (19.800.000 EUR/anno):
il verdetto e' sul risparmio, non
sulla VAN (che pure e' positiva).
NOTA: il CRF entra SOLO nel LCO di
questa tab: nei flussi il CAPEX
entra intero all'anno 0, mai
annuizzato.
NOTA 2: in questa tab il risparmio
nullo o negativo NON e' degenere:
con prezzo elettricita' 200 EUR/MWh
(sopra il tetto 148) il caso e'
calcolabile (valid=True, flussi
pieni), MARGINALE con VAN
-172.405.227,94 EUR e payback None,
non un errore: 9.800.000 di
risparmio negativo resta entro la
soglia del 10 % di C_base
(20.700.000 a quel prezzo).
NOTA 3: la CO2 evitata PUO' essere
negativa in questa tab (non e' una
guard): con fattore altoforno 0,10
la CO2 base e' 50.000 t/anno e
l'EAF 112.083,33 t/anno, quindi
l'evitata e' -62.083,33 t/anno,
mentre il verdetto resta MARGINALE
(stessa economia: i fattori non
toccano i costi).
NOTA 4: i pareggi sono TETTI, non
pavimenti, e sono sui costi
variabili, NON sul risparmio: al
pareggio esatto (elettricita' 148
EUR/MWh, oppure rottame 279,43
EUR/t) i costi per tonnellata si
eguagliano ma il risparmio e'
-2.000.000 EUR/anno, cioe' solo
l'O&M. Il breakeven elettrico e'
None con elettricita' EAF 150 kWh/t
(denominatore nullo: l'EAF non
consuma piu' elettricita' della
baseline) e None con rottame 400
EUR/t (numeratore negativo: costo
EAF senza elettricita' 486,60 sopra
il costo BF senza elettricita'
384). Il breakeven rottame e' None
con rottame nullo.
NOTA 5: il verdetto MARGINALE del
demo non e' un errore: con
tolleranza 0 % lo stesso caso
diventa CONVIENTE (risparmio
positivo, soglia nulla); con
rottame 100 EUR/t diventa
CONVIENTE (risparmio 92.200.000,
VAN 997.526.736,35, payback 1);
con rottame 400 EUR/t diventa
NON_CONVIENTE (risparmio
-65.300.000, VAN -808.985.855,57).
NOTA 6: il payback usa il cumulato
>= 0 (regola >= del brief): con
CAPEX nullo il payback e' 0 (non
1); con flussi [-100, 50, 50] il
payback e' 2 (il cumulato all'anno
2 e' zero, e zero basta); con CAPEX
41.000.000 EUR il payback e' 5
(divisione esatta 41.000.000 /
8.200.000).
NOTA 7: i valori demo sono stati
ricalcolati da zero con un calcolo
indipendente: il ricalcolo esatto
(senza arrotondamenti intermedi)
da' costo BF 396, costo EAF 375,60,
costo base 198.000.000, costo
variabile EAF 187.800.000, costo
alternativo 189.800.000, risparmio
8.200.000, CO2 base 950.000, EAF
112.083,33, evitata 837.916,67, CRF
0,0871845570, LCO base 396,00, LCO
alt 390,062147, VAN 34.053.353,99,
TIR 12,33 %, payback 8, breakeven
elettricita' 148 (tetto), breakeven
rottame 279,43 (tetto), verdetto
MARGINALE: i file usano i valori
esatti.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w778_helpers import (
    demo_calcoli,
    mh777_breakeven_el,
    mh777_breakeven_scrap,
    mh777_c_alt,
    mh777_c_base,
    mh777_c_bf_nonel,
    mh777_c_bf_per_t,
    mh777_c_eaf_non_scrap,
    mh777_c_eaf_nonel,
    mh777_c_eaf_per_t,
    mh777_c_eaf_var,
    mh777_calcola,
    mh777_co2_base,
    mh777_co2_eaf,
    mh777_co2_evitata,
    mh777_crf,
    mh777_csv,
    mh777_demo,
    mh777_flussi,
    mh777_int_pos,
    mh777_lco_alt,
    mh777_lco_base,
    mh777_num,
    mh777_nneg,
    mh777_payback,
    mh777_pct_tolleranza,
    mh777_pct_wacc,
    mh777_pos,
    mh777_risparmio,
    mh777_tir,
    mh777_valida,
    mh777_van,
    mh777_verdetto,
)

# Costanti demo a piena precisione (per la validazione
# _DEMO contro demo_calcoli() con tolleranza relativa
# < 1e-9: vedi test_demo_costanti_vs_demo_calcoli).
_DEMO = {
    "c_bf_per_t": 396.0,
    "c_eaf_per_t": 375.6,
    "c_bf_nonel_per_t": 384.0,
    "c_eaf_nonel_per_t": 339.6,
    "c_eaf_non_scrap_per_t": 102.60000000000002,
    "el_bf_mwh_anno": 75000.0,
    "el_eaf_mwh_anno": 225000.0,
    "gas_mwh_anno": 166666.66666666666,
    "c_base_eur_anno": 198000000.0,
    "c_eaf_var_eur_anno": 187800000.0,
    "c_alt_eur_anno": 189800000.0,
    "risparmio_eur_anno": 8200000.0,
    "co2_base_t_anno": 950000.0,
    "co2_eaf_t_anno": 112083.33333333334,
    "co2_evitata_t_anno": 837916.6666666666,
    "crf": 0.0871845569768514,
    "lco_base_eur_t": 396.0,
    "lco_alt_eur_t": 390.0621468372222,
    "van": 34053353.992235065,
    "tir": 12.331112926146998,
    "breakeven_el_eur_mwh": 147.99999999999994,
    "breakeven_scrap_eur_t": 279.4285714285714,
}


def _demo_kwargs():
    return dict(mh777_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh777_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh777_num(3, "x") == 3.0
    assert mh777_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh777_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh777_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh777_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh777_pos(0, "x")
    with pytest.raises(ValueError):
        mh777_pos(-1, "x")
    assert mh777_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh777_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh777_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh777_int_pos(0, "x")


def test_pct_wacc_limiti():
    assert mh777_pct_wacc(0, "x") == 0.0
    assert mh777_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh777_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh777_pct_tolleranza(0, "x") == 0.0
    assert mh777_pct_tolleranza(100, "x") == 100.0
    assert mh777_pct_tolleranza(10.0, "x") == 10.0
    with pytest.raises(ValueError):
        mh777_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh777_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_c_bf_per_t_scomposizione():
    assert mh777_c_bf_per_t(14, 12, 150, 80, 1.6, 110,
                             40) == pytest.approx(396.0)
    assert mh777_c_bf_per_t(0, 12, 0, 80, 0, 110,
                             0) == pytest.approx(0.0)
    assert mh777_c_bf_per_t(14, 12, 150, 0, 1.6, 110,
                             40) == pytest.approx(384.0)
    with pytest.raises(ValueError):
        mh777_c_bf_per_t(-1, 12, 150, 80, 1.6, 110, 40)
    with pytest.raises(ValueError):
        mh777_c_bf_per_t(14, -1, 150, 80, 1.6, 110, 40)


def test_c_eaf_per_t_scomposizione():
    assert mh777_c_eaf_per_t(1.05, 260, 450, 80, 1.2, 18, 2, 5,
                             35) == pytest.approx(375.6)
    assert mh777_c_eaf_per_t(1.05, 100, 450, 80, 1.2, 18, 2, 5,
                             35) == pytest.approx(207.6)
    assert mh777_c_eaf_per_t(1.05, 400, 450, 80, 1.2, 18, 2, 5,
                             35) == pytest.approx(522.6)
    assert mh777_c_eaf_per_t(0, 260, 450, 80, 1.2, 18, 2, 5,
                             35) == pytest.approx(102.6)
    with pytest.raises(ValueError):
        mh777_c_eaf_per_t(1.05, -1, 450, 80, 1.2, 18, 2, 5, 35)
    with pytest.raises(ValueError):
        mh777_c_eaf_per_t(1.05, 260, 450, 80, 1.2, 18, -1, 5, 35)


def test_c_nonel_e_non_scrap():
    assert mh777_c_bf_nonel(396.0, 150, 80) == pytest.approx(384.0)
    assert mh777_c_eaf_nonel(375.6, 450, 80) == pytest.approx(339.6)
    assert mh777_c_eaf_non_scrap(375.6, 1.05,
                                 260) == pytest.approx(102.6)
    assert mh777_c_bf_nonel(396.0, 150, 0) == pytest.approx(396.0)
    with pytest.raises(ValueError):
        mh777_c_bf_nonel(396.0, -1, 80)


def test_c_base_c_eaf_var_c_alt():
    assert mh777_c_base(396.0, 500000) == pytest.approx(198000000.0)
    assert mh777_c_eaf_var(375.6, 500000) == pytest.approx(
        187800000.0)
    assert mh777_c_alt(187800000.0, 2000000) == pytest.approx(
        189800000.0)
    with pytest.raises(ValueError):
        mh777_c_base(396.0, 0)
    with pytest.raises(ValueError):
        mh777_c_alt(187800000.0, -1)


def test_co2_base_eaf_evitata():
    assert mh777_co2_base(1.9, 500000) == pytest.approx(950000.0)
    assert mh777_co2_eaf(450, 500000, 1.2, 0.35,
                         0.20) == pytest.approx(112083.33333333334)
    assert mh777_co2_eaf(450, 500000, 0, 0.35,
                         0.20) == pytest.approx(78750.0)
    assert mh777_co2_eaf(0, 500000, 1.2, 0.35,
                         0.20) == pytest.approx(33333.333333333336)
    assert mh777_co2_evitata(950000.0,
                             112083.33333333334) == pytest.approx(
        837916.6666666666)
    assert mh777_co2_evitata(100.0, 150.0) == pytest.approx(-50.0)
    with pytest.raises(ValueError):
        mh777_co2_base(-0.10, 500000)


def test_co2_evitata_puo_essere_negativa_via_calcola():
    """Differenza chiave di questa tab: via
    mh777_calcola la CO2 evitata PUO' essere
    negativa (fattore altoforno basso)."""
    bc = _variante(f_bf_t_per_t=0.10)
    assert bc["co2_base_t_anno"] == pytest.approx(50000.0)
    assert bc["co2_eaf_t_anno"] == pytest.approx(112083.33333333334)
    assert bc["co2_evitata_t_anno"] == pytest.approx(-62083.33333333334)
    assert bc["verdetto"] == "MARGINALE"
    assert bc["valid"] is True


def test_co2_eaf_formula_componenti():
    """CO2 EAF = elettricita' EAF x f_el + gas x f_gas,
    con le conversioni kWh->MWh e GJ->MWh."""
    for bc in (demo_calcoli(),
               _variante(f_bf_t_per_t=0.10),
               _variante(el_eaf_kwh_per_t=150)):
        atteso = (bc["el_eaf_mwh_anno"] * bc["f_el_t_per_mwh"]
                  + bc["gas_mwh_anno"] * bc["f_gas_t_per_mwh"])
        assert bc["co2_eaf_t_anno"] == pytest.approx(atteso)


def test_risparmio_segno():
    assert mh777_risparmio(198000000.0, 189800000.0) == \
        pytest.approx(8200000.0)
    assert mh777_risparmio(198000000.0, 198000000.0) == 0.0
    assert mh777_risparmio(207000000.0, 216800000.0) == \
        pytest.approx(-9800000.0)


def test_crf_solo_lco():
    assert mh777_crf(6.0, 20) == pytest.approx(0.0871845569768514)
    assert mh777_crf(0.0, 20) == pytest.approx(1.0 / 20.0)
    assert mh777_crf(6.0, 10) == pytest.approx(0.13586795843164435)
    with pytest.raises(ValueError):
        mh777_crf(50.1, 20)
    with pytest.raises(ValueError):
        mh777_crf(6.0, 0)


def test_lco():
    assert mh777_lco_base(198000000.0, 500000) == pytest.approx(396.0)
    assert mh777_lco_alt(60000000, 0.0871845569768514, 2000000,
                         375.6, 500000) == pytest.approx(
        390.0621468372222)
    assert mh777_lco_base(198000000.0, 0) is None
    assert mh777_lco_alt(60000000, 0.0871845569768514, 2000000,
                         375.6, 0) is None
    assert mh777_lco_alt(60000000, 0.0871845569768514, 2000000,
                         375.6, -5) is None
    # Il CAPEX entra nel LCO solo annuizzato: con CAPEX nullo
    # il LCO alt e' (O&M / P) + C_eaf_per_t.
    assert mh777_lco_alt(0, 0.0871845569768514, 2000000,
                         375.6, 500000) == pytest.approx(379.6)


def test_crf_mai_nei_flussi():
    """Il CRF entra SOLO nel LCO: i flussi usano il
    CAPEX intero all'anno 0 e la VAN dai flussi non
    dipende dal CRF (cambiando il WACC cambia la VAN
    per lo sconto, non per il CRF)."""
    bc = demo_calcoli()
    assert bc["flussi"][0] == -60000000
    assert bc["flussi"][1:] == [8200000.0] * 20
    assert bc["van"] == pytest.approx(mh777_van(bc["flussi"], 6.0))
    bc0 = _variante(wacc_pct=0)
    assert bc0["van"] == pytest.approx(sum(bc0["flussi"]))
    assert bc0["crf"] == pytest.approx(1.0 / 20.0)
    assert bc0["lco_alt_eur_t"] == pytest.approx(385.6)


def test_breakeven_el_demo_e_varianti():
    # Demo: (384 - 339,60) / ((450 - 150) / 1000) = 148,00.
    assert mh777_breakeven_el(384.0, 339.6, 450,
                              150) == pytest.approx(148.0)
    # A rottame 279,43 (pareggio rottame): nonel EAF 360,
    # (384 - 360) / 0,30 = 80,00.
    assert mh777_breakeven_el(384.0, 360.0, 450,
                              150) == pytest.approx(80.0)
    # Numeratore zero: pareggio zero, valido.
    assert mh777_breakeven_el(384.0, 384.0, 450,
                              150) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh777_breakeven_el(384.0, 339.6, -1, 150)


def test_breakeven_el_none_casi():
    # Denominatore <= 0: el_eaf uguale o sotto el_bf.
    assert mh777_breakeven_el(384.0, 339.6, 150, 150) is None
    assert mh777_breakeven_el(384.0, 339.6, 100, 150) is None
    # Numeratore < 0: costo EAF senza elettricita'
    # sopra il costo BF senza elettricita'.
    assert mh777_breakeven_el(384.0, 486.6, 450, 150) is None


def test_breakeven_scrap_demo_e_varianti():
    # Demo: (396 - 102,60) / 1,05 = 279,428571.
    assert mh777_breakeven_scrap(396.0, 102.6,
                                 1.05) == pytest.approx(
        279.4285714285714)
    # Numeratore zero: pareggio zero, valido.
    assert mh777_breakeven_scrap(396.0, 396.0,
                                 1.05) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh777_breakeven_scrap(396.0, 102.6, -1)


def test_breakeven_scrap_none_casi():
    # Scrap <= 0: nessun prezzo da calcolare.
    assert mh777_breakeven_scrap(396.0, 102.6, 0) is None
    # Numeratore < 0: a prezzo rottame zero l'EAF e'
    # gia' piu' caro (altri costi EAF alti).
    assert mh777_breakeven_scrap(396.0, 467.6, 1.05) is None


def test_breakeven_verifica_pareggio():
    """Al prezzo di pareggio i costi per tonnellata
    si eguagliano: C_eaf_per_t(p*) = C_bf_per_t(p*),
    per entrambi i pareggi. Il risparmio invece e'
    -O&M, non zero (i pareggi non includono l'O&M)."""
    bc = _variante(p_el_eur_mwh=148.0)
    assert bc["c_bf_per_t"] == pytest.approx(bc["c_eaf_per_t"])
    assert bc["risparmio_eur_anno"] == pytest.approx(-2000000.0,
                                                     abs=1e-3)
    bc2 = _variante(p_scrap_eur_t=279.4285714285714)
    assert bc2["c_bf_per_t"] == pytest.approx(bc2["c_eaf_per_t"])
    assert bc2["risparmio_eur_anno"] == pytest.approx(-2000000.0,
                                                      abs=1e-3)


def test_pareggi_tetti_non_pavimenti():
    """Sotto il tetto l'EAF vince sui costi variabili,
    sopra perde: il costo EAF scende sotto il costo
    BF sotto il tetto e sale sopra oltre il tetto,
    per entrambi i prezzi."""
    be_el = demo_calcoli()["breakeven_el_eur_mwh"]
    assert _variante(p_el_eur_mwh=be_el - 10)[
        "c_eaf_per_t"] < _variante(p_el_eur_mwh=be_el - 10)[
        "c_bf_per_t"]
    assert _variante(p_el_eur_mwh=be_el + 10)[
        "c_eaf_per_t"] > _variante(p_el_eur_mwh=be_el + 10)[
        "c_bf_per_t"]
    be_sc = demo_calcoli()["breakeven_scrap_eur_t"]
    assert _variante(p_scrap_eur_t=be_sc - 10)[
        "c_eaf_per_t"] < _variante(p_scrap_eur_t=be_sc - 10)[
        "c_bf_per_t"]
    assert _variante(p_scrap_eur_t=be_sc + 10)[
        "c_eaf_per_t"] > _variante(p_scrap_eur_t=be_sc + 10)[
        "c_bf_per_t"]


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh777_flussi(60000000, 8200000.0, 20)
    assert len(fl) == 21
    assert fl[0] == -60000000
    assert all(f == 8200000.0 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = demo_calcoli()
    assert bc["van"] == pytest.approx(34053353.992235065)
    assert mh777_van([-60000000] + [8200000.0] * 20,
                     0) == pytest.approx(104000000.0)
    assert mh777_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = demo_calcoli()
    assert bc["tir"] == pytest.approx(12.331112926146998)
    assert mh777_tir([-60000000] + [8200000.0] * 20) == \
        pytest.approx(0.12331112926146998)
    tir = mh777_tir([-60000000] + [8200000.0] * 20)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate(
                  [-60000000] + [8200000.0] * 20))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    """Payback con cumulato >= 0: il cumulato nullo basta."""
    assert mh777_payback([-60000000] + [8200000.0] * 20) == 8
    assert mh777_payback([-60000000] + [-1000.0] * 20) is None
    assert mh777_payback([0] + [8200000.0] * 20) == 0
    assert mh777_payback([-100] + [50] * 2) == 2
    assert mh777_payback([-41000000.0] +
                         [8200000.0] * 5) == 5


def test_verdetto():
    assert mh777_verdetto(92200000.0, 198000000.0,
                          10.0) == "CONVIENTE"
    assert mh777_verdetto(8200000.0, 198000000.0,
                          10.0) == "MARGINALE"
    assert mh777_verdetto(0.0, 198000000.0, 10.0) == "MARGINALE"
    assert mh777_verdetto(-19800000.0, 198000000.0,
                          10.0) == "MARGINALE"
    assert mh777_verdetto(-19800001.0, 198000000.0,
                          10.0) == "NON_CONVIENTE"
    assert mh777_verdetto(-65300000.0, 198000000.0,
                          10.0) == "NON_CONVIENTE"
    assert mh777_verdetto(8200000.0, 198000000.0,
                          0.0) == "CONVIENTE"
    assert mh777_verdetto(-100.0, 198000000.0,
                          0.0) == "NON_CONVIENTE"
    assert mh777_verdetto(None, 198000000.0,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh777_verdetto(float("nan"), 198000000.0, 10.0)
    with pytest.raises(ValueError):
        mh777_verdetto(100.0, -1, 10.0)
    with pytest.raises(ValueError):
        mh777_verdetto(100.0, 198000000.0, 100.1)


def test_valida_demo_ok():
    v = mh777_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("p_t_anno", "500000"),
                       ("p_t_anno", float("nan")),
                       ("p_t_anno", float("inf")),
                       ("p_t_anno", True),
                       ("p_scrap_eur_t", None),
                       ("coke_gj_per_t", "14")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh777_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("p_t_anno", 0),
                          ("p_t_anno", -1),
                          ("coke_gj_per_t", -1),
                          ("p_coke_eur_gj", -1),
                          ("el_bf_kwh_per_t", -1),
                          ("p_el_eur_mwh", -1),
                          ("ore_t_per_t", -1),
                          ("p_ore_eur_t", -1),
                          ("other_bf_eur_t", -1),
                          ("scrap_t_per_t", -1),
                          ("p_scrap_eur_t", -1),
                          ("el_eaf_kwh_per_t", -1),
                          ("gas_gj_per_t", -1),
                          ("p_gas_eur_gj", -1),
                          ("electrodes_kg_per_t", -1),
                          ("p_elec_eur_kg", -1),
                          ("other_eaf_eur_t", -1),
                          ("om_eur_anno", -100),
                          ("capex_eur", -1),
                          ("f_bf_t_per_t", -0.10),
                          ("f_el_t_per_mwh", -0.10),
                          ("f_gas_t_per_mwh", -0.10),
                          ("wacc_pct", -0.1), ("wacc_pct", 50.1),
                          ("vita_anni", 0), ("vita_anni", 2.5),
                          ("tolleranza_pct", -1),
                          ("tolleranza_pct", 100.1)):
        d = _demo_kwargs()
        d[campo] = valore
        assert mh777_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"coke_gj_per_t": 0,
              "p_coke_eur_gj": 0,
              "el_bf_kwh_per_t": 0,
              "p_el_eur_mwh": 0,
              "ore_t_per_t": 0,
              "p_ore_eur_t": 0,
              "other_bf_eur_t": 0,
              "scrap_t_per_t": 0,
              "p_scrap_eur_t": 0,
              "el_eaf_kwh_per_t": 0,
              "gas_gj_per_t": 0,
              "p_gas_eur_gj": 0,
              "electrodes_kg_per_t": 0,
              "p_elec_eur_kg": 0,
              "other_eaf_eur_t": 0,
              "om_eur_anno": 0,
              "capex_eur": 0,
              "f_bf_t_per_t": 0,
              "f_el_t_per_mwh": 0,
              "f_gas_t_per_mwh": 0,
              "wacc_pct": 0,
              "tolleranza_pct": 0})
    assert mh777_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    assert mh777_valida(**d)["valido"] is True


def test_valida_non_controlla_risparmio_calcola_neppure():
    """La validazione input NON controlla il risparmio
    (e' un esito, non un range) e in questa tab
    nemmeno mh777_calcola lo controlla: con prezzo
    elettricita' 200 EUR/MWh (sopra il tetto 148)
    il caso resta CALCOLABILE."""
    d = _demo_kwargs()
    d["p_el_eur_mwh"] = 200
    assert mh777_valida(**d)["valido"] is True
    bc = _variante(p_el_eur_mwh=200)
    assert bc["valid"] is True
    assert bc["verdetto"] == "MARGINALE"
    assert bc["flussi"]
    assert bc["payback"] is None


def test_demo_dict():
    d = mh777_demo()
    assert d["p_t_anno"] == 500000
    assert d["coke_gj_per_t"] == 14
    assert d["p_coke_eur_gj"] == 12
    assert d["el_bf_kwh_per_t"] == 150
    assert d["p_el_eur_mwh"] == 80
    assert d["ore_t_per_t"] == 1.6
    assert d["p_ore_eur_t"] == 110
    assert d["other_bf_eur_t"] == 40
    assert d["scrap_t_per_t"] == 1.05
    assert d["p_scrap_eur_t"] == 260
    assert d["el_eaf_kwh_per_t"] == 450
    assert d["gas_gj_per_t"] == 1.2
    assert d["p_gas_eur_gj"] == 18
    assert d["electrodes_kg_per_t"] == 2
    assert d["p_elec_eur_kg"] == 5
    assert d["other_eaf_eur_t"] == 35
    assert d["om_eur_anno"] == 2000000
    assert d["capex_eur"] == 60000000
    assert d["f_bf_t_per_t"] == 1.9
    assert d["f_el_t_per_mwh"] == 0.35
    assert d["f_gas_t_per_mwh"] == 0.20
    assert d["wacc_pct"] == 6.0
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
    assert bc["verdetto"] == "MARGINALE"
    assert bc["valid"] is True


def test_demo_calcoli_fisica():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["c_bf_per_t"] == pytest.approx(396.0)
    assert bc["c_eaf_per_t"] == pytest.approx(375.6)
    assert bc["el_bf_mwh_anno"] == pytest.approx(75000.0)
    assert bc["el_eaf_mwh_anno"] == pytest.approx(225000.0)
    assert bc["gas_mwh_anno"] == pytest.approx(166666.66666666666)
    assert bc["co2_evitata_t_anno"] == pytest.approx(837916.6666666666)


def test_demo_calcoli_economia():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(198000000.0)
    assert bc["c_eaf_var_eur_anno"] == pytest.approx(187800000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(189800000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(8200000.0)
    assert bc["breakeven_el_eur_mwh"] == pytest.approx(148.0)
    assert bc["breakeven_scrap_eur_t"] == pytest.approx(
        279.4285714285714)


def test_demo_calcoli_finanza():
    bc = demo_calcoli()
    assert bc["crf"] == pytest.approx(0.0871845569768514)
    assert bc["lco_base_eur_t"] == pytest.approx(396.0)
    assert bc["lco_alt_eur_t"] == pytest.approx(390.0621468372222)
    assert bc["van"] == pytest.approx(34053353.992235065)
    assert bc["tir"] == pytest.approx(12.331112926146998)
    assert bc["payback"] == 8
    assert bc["verdetto"] == "MARGINALE"


def test_demo_flussi_e_cumulato():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -60000000
    assert len(bc["flussi"]) == 21
    assert all(f == pytest.approx(8200000.0)
               for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -60000000
    assert righe.iloc[7]["Cumulato (EUR)"] == pytest.approx(-2600000.0)
    assert righe.iloc[8]["Cumulato (EUR)"] == pytest.approx(5600000.0)
    assert righe.iloc[20]["Cumulato (EUR)"] == pytest.approx(
        104000000.0)
    assert righe.iloc[20]["Flusso (EUR/anno)"] == pytest.approx(
        8200000.0)


def test_demo_tabella_righe():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Produzione acciaio (t/anno)"] == pytest.approx(
        500000.0)
    assert mappa["Costo BF per tonnellata (EUR/t)"] == pytest.approx(
        396.0)
    assert mappa["Costo EAF per tonnellata (EUR/t)"] == pytest.approx(
        375.6)
    assert mappa["Elettricita' EAF (MWh/anno)"] == pytest.approx(
        225000.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(
        189800000.0)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(8200000.0)
    assert mappa["Payback (anni)"] == 8
    assert mappa["Verdetto"] == "MARGINALE"
    assert mappa["Breakeven prezzo elettricita' (EUR/MWh)"] == \
        pytest.approx(148.0)
    assert mappa["Breakeven prezzo rottame (EUR/t)"] == \
        pytest.approx(279.4285714285714)


def test_demo_coerenza_interna():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["c_bf_per_t"] * bc["p_t_anno"] == \
        pytest.approx(bc["c_base_eur_anno"])
    assert bc["c_eaf_per_t"] * bc["p_t_anno"] == \
        pytest.approx(bc["c_eaf_var_eur_anno"])
    assert bc["co2_base_t_anno"] - bc["co2_eaf_t_anno"] == \
        pytest.approx(bc["co2_evitata_t_anno"])
    assert bc["c_base_eur_anno"] / bc["p_t_anno"] == \
        pytest.approx(bc["lco_base_eur_t"])
    assert (bc["capex_eur"] * bc["crf"] + bc["om_eur_anno"]) / \
        bc["p_t_anno"] + bc["c_eaf_per_t"] == \
        pytest.approx(bc["lco_alt_eur_t"])
    assert bc["c_bf_nonel_per_t"] + \
        bc["el_bf_kwh_per_t"] / 1000.0 * bc["p_el_eur_mwh"] == \
        pytest.approx(bc["c_bf_per_t"])
    assert bc["c_eaf_non_scrap_per_t"] + \
        bc["scrap_t_per_t"] * bc["p_scrap_eur_t"] == \
        pytest.approx(bc["c_eaf_per_t"])


def test_demo_contro_riconteggio_indipendente():
    p, coke, pc = 500000, 14, 12
    elb, pel, ore, po, ob = 150, 80, 1.6, 110, 40
    sc, ps, ele, gas, pg = 1.05, 260, 450, 1.2, 18
    elc, pe, oe, om, cx = 2, 5, 35, 2000000, 60000000
    fb, fel, fg, wacc, vita = 1.9, 0.35, 0.20, 6.0, 20
    cb = coke * pc + elb / 1000.0 * pel + ore * po + ob
    ce = sc * ps + ele / 1000.0 * pel + gas * pg + elc * pe + oe
    cbase = cb * p
    cav = ce * p
    ca = cav + om
    risp = cbase - ca
    co2b = fb * p
    co2a = ele / 1000.0 * p * fel + gas * p / 3.6 * fg
    r = wacc / 100.0
    crf = r * (1 + r) ** vita / ((1 + r) ** vita - 1.0)
    lco_b = cb
    lco_a = (cx * crf + om) / p + ce
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    be_el = (cb - elb / 1000.0 * pel
             - (ce - ele / 1000.0 * pel)) / ((ele - elb) / 1000.0)
    be_sc = (cb - (ce - sc * ps)) / sc
    bc = demo_calcoli()
    assert bc["c_bf_per_t"] == pytest.approx(cb)
    assert bc["c_eaf_per_t"] == pytest.approx(ce)
    assert bc["c_base_eur_anno"] == pytest.approx(cbase)
    assert bc["c_eaf_var_eur_anno"] == pytest.approx(cav)
    assert bc["c_alt_eur_anno"] == pytest.approx(ca)
    assert bc["risparmio_eur_anno"] == pytest.approx(risp)
    assert bc["co2_base_t_anno"] == pytest.approx(co2b)
    assert bc["co2_eaf_t_anno"] == pytest.approx(co2a)
    assert bc["crf"] == pytest.approx(crf)
    assert bc["lco_base_eur_t"] == pytest.approx(lco_b)
    assert bc["lco_alt_eur_t"] == pytest.approx(lco_a)
    assert bc["van"] == pytest.approx(van)
    assert bc["breakeven_el_eur_mwh"] == pytest.approx(be_el)
    assert bc["breakeven_scrap_eur_t"] == pytest.approx(be_sc)


# ---------------------------------------------------------------- varianti
def test_demo_marginale_non_conviente():
    """Il demo e' MARGINALE, non CONVIENTE: il
    verdetto e' sul risparmio, e 8.200.000 resta
    entro la tolleranza del 10 % di C_base
    (19.800.000), anche se la VAN e' positiva."""
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] > 0.0
    assert bc["payback"] == 8
    assert bc["verdetto"] == "MARGINALE"


def test_variante_rottame_basso_conviente():
    """Rottame 100 EUR/t: risparmio 92.200.000,
    VAN 997.526.736,35, payback 1, CONVIENTE."""
    bc = _variante(p_scrap_eur_t=100)
    assert bc["valid"] is True
    assert bc["c_eaf_per_t"] == pytest.approx(207.6)
    assert bc["c_eaf_var_eur_anno"] == pytest.approx(103800000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(105800000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(92200000.0)
    assert bc["van"] == pytest.approx(997526736.351716)
    assert bc["payback"] == 1
    assert bc["lco_alt_eur_t"] == pytest.approx(222.06214683722217)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_rottame_alto_non_conviente():
    """Rottame 400 EUR/t: risparmio -65.300.000,
    VAN -808.985.855,57, payback mai,
    NON_CONVIENTE, breakeven elettrico None
    (numeratore negativo)."""
    bc = _variante(p_scrap_eur_t=400)
    assert bc["valid"] is True
    assert bc["c_eaf_per_t"] == pytest.approx(522.6)
    assert bc["risparmio_eur_anno"] == pytest.approx(-65300000.0)
    assert bc["van"] == pytest.approx(-808985855.5723109)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["breakeven_el_eur_mwh"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_pareggio_el_esatto():
    """Al tetto elettrico esatto (148 EUR/MWh) i
    costi per tonnellata si eguagliano ma il
    risparmio e' -2.000.000 (solo l'O&M): VAN
    -82.939.842,44, TIR None, payback mai,
    verdetto MARGINALE."""
    bc = _variante(p_el_eur_mwh=148)
    assert bc["c_bf_per_t"] == pytest.approx(bc["c_eaf_per_t"])
    assert bc["risparmio_eur_anno"] == pytest.approx(-2000000.0,
                                                     abs=1e-3)
    assert bc["van"] == pytest.approx(-82939842.43713085)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "MARGINALE"


def test_variante_pareggio_scrap_esatto():
    """Al tetto rottame esatto (279,43 EUR/t) i
    costi per tonnellata si eguagliano ma il
    risparmio e' -2.000.000 (solo l'O&M): stessa
    VAN del pareggio elettrico, verdetto
    MARGINALE."""
    bc = _variante(p_scrap_eur_t=279.4285714285714)
    assert bc["c_bf_per_t"] == pytest.approx(bc["c_eaf_per_t"])
    assert bc["risparmio_eur_anno"] == pytest.approx(-2000000.0,
                                                     abs=1e-3)
    assert bc["van"] == pytest.approx(-82939842.4371305)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "MARGINALE"


def test_variante_sopra_tetto_el():
    """Prezzo elettricita' 200 EUR/MWh (sopra il
    tetto 148): risparmio -9.800.000, VAN
    -172.405.227,94, TIR None, payback mai,
    verdetto MARGINALE (entro la soglia del
    10 % di C_base a quel prezzo)."""
    bc = _variante(p_el_eur_mwh=200)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(-9800000.0)
    assert bc["van"] == pytest.approx(-172405227.94193944)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "MARGINALE"


def test_variante_tolleranza_zero_demo_conviente():
    """Con tolleranza 0 % la fascia MARGINALE e'
    nulla: lo stesso demo diventa CONVIENTE
    (risparmio positivo, soglia zero)."""
    bc = _variante(tolleranza_pct=0)
    assert bc["risparmio_eur_anno"] == pytest.approx(8200000.0)
    assert bc["van"] == pytest.approx(34053353.992235065)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    """Payback regola >=: con CAPEX nullo il payback e' 0,
    non 1 (all'anno 0 il cumulato e' gia' zero)."""
    bc = _variante(capex_eur=0)
    assert bc["capex_eur"] == 0
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(94053353.99223508)
    assert bc["lco_alt_eur_t"] == pytest.approx(379.6)
    assert bc["verdetto"] == "MARGINALE"


def test_variante_capex_divisione_esatta_payback():
    """CAPEX 41.000.000 EUR: divisione esatta
    41.000.000 / 8.200.000 = 5 anni, payback 5
    (regola >=: il cumulato nullo basta)."""
    bc = _variante(capex_eur=41000000)
    assert bc["payback"] == 5
    assert bc["van"] == pytest.approx(53053353.99223507)
    assert bc["tir"] == pytest.approx(19.42579469894764)
    assert bc["verdetto"] == "MARGINALE"


def test_variante_wacc_zero():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(104000000.0)
    assert bc["lco_alt_eur_t"] == pytest.approx(385.6)
    assert bc["verdetto"] == "MARGINALE"


def test_variante_vita_diversa():
    bc = _variante(vita_anni=10)
    assert len(bc["flussi"]) == 11
    assert bc["van"] == pytest.approx(352713.82160049863)
    assert bc["tir"] == pytest.approx(6.123905297351764)
    assert bc["payback"] == 8
    assert bc["verdetto"] == "MARGINALE"


def test_variante_om_alto():
    """O&M 5.000.000 EUR/anno: risparmio 5.200.000,
    VAN -356.409,66 (negativa ma piccola),
    payback 12, verdetto MARGINALE."""
    bc = _variante(om_eur_anno=5000000)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(5200000.0)
    assert bc["van"] == pytest.approx(-356409.663460698)
    assert bc["payback"] == 12
    assert bc["lco_alt_eur_t"] == pytest.approx(396.0621468372222)
    assert bc["verdetto"] == "MARGINALE"


def test_variante_breakeven_el_none_denominatore():
    """Elettricita' EAF uguale alla baseline
    (150 kWh/t): breakeven elettrico None,
    caso calcolabile CONVIENTE."""
    bc = _variante(el_eaf_kwh_per_t=150)
    assert bc["valid"] is True
    assert bc["breakeven_el_eur_mwh"] is None
    assert bc["risparmio_eur_anno"] == pytest.approx(20200000.0)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_breakeven_scrap_none_rottame_nullo():
    """Rottame nullo: breakeven rottame None,
    caso calcolabile CONVIENTE."""
    bc = _variante(scrap_t_per_t=0)
    assert bc["valid"] is True
    assert bc["breakeven_scrap_eur_t"] is None
    assert bc["c_eaf_per_t"] == pytest.approx(102.6)
    assert bc["risparmio_eur_anno"] == pytest.approx(144700000.0)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_breakeven_scrap_none_numeratore():
    """Altri costi EAF 400 EUR/t: costo EAF senza
    rottame 467,60 sopra il costo BF 396:
    breakeven rottame None (numeratore negativo)."""
    bc = _variante(other_eaf_eur_t=400)
    assert bc["valid"] is True
    assert bc["breakeven_scrap_eur_t"] is None


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
    (sono None per assenza); il verdetto per
    risparmio None e' NON_CALCOLABILE."""
    with pytest.raises(ValueError):
        _variante(p_t_anno=0)
    with pytest.raises(ValueError):
        _variante(p_el_eur_mwh=-1)
    with pytest.raises(ValueError):
        _variante(wacc_pct=60)
    assert mh777_verdetto(None, 198000000.0, 10.0) == "NON_CALCOLABILE"
    assert demo_calcoli()["verdetto"] != "NON_CALCOLABILE"


def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"p_t_anno": 0}, {"p_t_anno": -1},
               {"coke_gj_per_t": -1},
               {"p_coke_eur_gj": -1},
               {"el_bf_kwh_per_t": -1},
               {"p_el_eur_mwh": -1},
               {"ore_t_per_t": -1},
               {"p_ore_eur_t": -1},
               {"other_bf_eur_t": -1},
               {"scrap_t_per_t": -1},
               {"p_scrap_eur_t": -1},
               {"el_eaf_kwh_per_t": -1},
               {"gas_gj_per_t": -1},
               {"p_gas_eur_gj": -1},
               {"electrodes_kg_per_t": -1},
               {"p_elec_eur_kg": -1},
               {"other_eaf_eur_t": -1},
               {"om_eur_anno": -100},
               {"capex_eur": -1},
               {"f_bf_t_per_t": -0.10},
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
        assert mh777_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"p_t_anno": "500000"},
               {"p_t_anno": float("nan")},
               {"p_scrap_eur_t": float("inf")},
               {"capex_eur": True},
               {"coke_gj_per_t": "14"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh777_valida(**d)["valido"] is False


def test_risparmio_negativo_non_degenere():
    """Differenza chiave: risparmio nullo o
    negativo resta calcolabile, con flussi pieni e
    VAN negativa; cosi' anche la CO2 evitata
    negativa resta calcolabile, e cosi' i
    breakeven None restano calcolabili."""
    for kw in ({"p_el_eur_mwh": 200},
               {"p_scrap_eur_t": 400}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["verdetto"] in ("NON_CONVIENTE", "MARGINALE")
        assert bc["flussi"]
    bc = _variante(f_bf_t_per_t=0.10)
    assert bc["co2_evitata_t_anno"] < 0.0
    assert bc["valid"] is True
    bc2 = _variante(el_eaf_kwh_per_t=150)
    assert bc2["breakeven_el_eur_mwh"] is None
    assert bc2["valid"] is True


def test_co2_evitata_segno_funzione_pura():
    assert mh777_co2_evitata(100.0, 150.0) == pytest.approx(-50.0)


def test_verdetto_non_calcolabile_solo_risparmio_none():
    assert mh777_verdetto(None, 198000000.0, 10.0) == "NON_CALCOLABILE"
    assert demo_calcoli()["verdetto"] != "NON_CALCOLABILE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = demo_calcoli()
    testo = mh777_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert "c_bf_per_t;396.0" in testo
    assert "c_eaf_per_t;375.6" in testo
    assert "c_base_eur_anno;198000000.0" in testo
    assert "c_eaf_var_eur_anno;187800000.0" in testo
    assert "verdetto;MARGINALE" in testo
    assert "breakeven_el_eur_mwh" in testo
    assert "breakeven_scrap_eur_t" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = demo_calcoli()
    testo = mh777_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"c_eaf_per_t;{bc['c_eaf_per_t']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = demo_calcoli()
    testo = mh777_csv(bc, _demo_kwargs())
    for chiave in _demo_kwargs():
        assert f"{chiave};" in testo


def test_monotonia_prezzo_el_decrescente():
    # Il risparmio CALA con p_el (l'EAF consuma piu'
    # elettricita' della baseline): pendenza
    # -150.000 EUR/anno per EUR/MWh (500.000 t x
    # (450 - 150) / 1000 = 150.000 MWh/anno).
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_el_eur_mwh=90)["risparmio_eur_anno"]
    basso = _variante(p_el_eur_mwh=70)["risparmio_eur_anno"]
    assert basso > base > alto
    assert base - alto == pytest.approx(1500000.0)
    assert basso - base == pytest.approx(1500000.0)


def test_monotonia_prezzo_scrap_decrescente():
    # Il risparmio CALA con p_scrap: pendenza
    # -525.000 EUR/anno per EUR/t (500.000 t x
    # 1,05 t/t = 525.000 t/anno di rottame).
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_scrap_eur_t=270)["risparmio_eur_anno"]
    basso = _variante(p_scrap_eur_t=250)["risparmio_eur_anno"]
    assert basso > base > alto
    assert base - alto == pytest.approx(5250000.0)
    assert basso - base == pytest.approx(5250000.0)


def test_monotonia_elettricita_eaf():
    # Piu' elettricita' EAF, piu' caro l'EAF:
    # +10 kWh/t a 80 EUR/MWh = +0,80 EUR/t =
    # -400.000 EUR/anno di risparmio.
    base = demo_calcoli()["risparmio_eur_anno"]
    assert _variante(el_eaf_kwh_per_t=460)[
        "risparmio_eur_anno"] == pytest.approx(base - 400000.0)
    assert _variante(el_eaf_kwh_per_t=440)[
        "risparmio_eur_anno"] == pytest.approx(base + 400000.0)


def test_demo_deterministica_due_chiamate():
    a = demo_calcoli()
    b = demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh777_demo().keys()) == {
        "p_t_anno",
        "coke_gj_per_t", "p_coke_eur_gj",
        "el_bf_kwh_per_t", "p_el_eur_mwh",
        "ore_t_per_t", "p_ore_eur_t", "other_bf_eur_t",
        "scrap_t_per_t", "p_scrap_eur_t",
        "el_eaf_kwh_per_t", "gas_gj_per_t", "p_gas_eur_gj",
        "electrodes_kg_per_t", "p_elec_eur_kg",
        "other_eaf_eur_t", "om_eur_anno", "capex_eur",
        "f_bf_t_per_t", "f_el_t_per_mwh", "f_gas_t_per_mwh",
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
    return ["mh" + "77" + "6", "st" + "77" + "6",
            "tab" + "77" + "6"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w778_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w778_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab777:")


def test_registry_chain_tail_and_count():
    """Registry della nuova tab: il frammento UI apre la tab
    numero 777 (la coda della catena termina con la nuova tab
    e il conteggio atteso delle tab e' 777)."""
    src = _leggi("w778_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 777
    assert src.count("with tab777:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w778_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w778_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st777_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert "key=f" not in src and 'key = f' not in src
    assert "st.stop()" in src
    # guard degenere prima di KPI / grafico / tabella / CSV
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w778_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def777[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w778_ui.py")
        usate = set(re.findall(r'_def777\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 24
        assert usate == {
            "p_t_anno",
            "coke_gj_per_t", "p_coke_eur_gj",
            "el_bf_kwh_per_t", "p_el_eur_mwh",
            "ore_t_per_t", "p_ore_eur_t", "other_bf_eur_t",
            "scrap_t_per_t", "p_scrap_eur_t",
            "el_eaf_kwh_per_t", "gas_gj_per_t", "p_gas_eur_gj",
            "electrodes_kg_per_t", "p_elec_eur_kg",
            "other_eaf_eur_t", "om_eur_anno", "capex_eur",
            "f_bf_t_per_t", "f_el_t_per_mwh", "f_gas_t_per_mwh",
            "wacc_pct", "vita_anni", "tolleranza_pct"}
        assert usate <= set(mh777_demo().keys())


def test_ui_chiavi_demo_coerenti():
    """Ogni _def777[...] letto dalla UI esiste nel dict demo:
    sweep anti-KeyError a render (lezione dello sweep chiavi demo vs UI)."""
    src = _leggi("w778_ui.py")
    usate = set(re.findall(r'_def777\["([^"]+)"\]', src))
    assert usate
    assert len(usate) == 24
    assert usate <= set(mh777_demo().keys())


def test_ui_riferisce_solo_helper_nuovi():
    src = _leggi("w778_ui.py")
    usati = set(re.findall(r'\b(mh\d+_\w+)\b', src))
    assert usati
    assert all(u.startswith("mh777_") for u in usati)


@pytest.mark.parametrize("p_scrap,atteso", [
    (260, 375.6),
    (100, 207.6),
    (400, 522.6),
])
def test_c_eaf_per_t_parametrizzato(p_scrap, atteso):
    assert mh777_c_eaf_per_t(1.05, p_scrap, 450, 80, 1.2, 18, 2, 5,
                             35) == pytest.approx(atteso)


@pytest.mark.parametrize("campo,valore", [
    ("p_t_anno", 0), ("p_t_anno", -3),
    ("coke_gj_per_t", -1),
    ("p_coke_eur_gj", -1),
    ("el_bf_kwh_per_t", -1),
    ("p_el_eur_mwh", -1),
    ("ore_t_per_t", -1),
    ("p_ore_eur_t", -1),
    ("other_bf_eur_t", -1),
    ("scrap_t_per_t", -1),
    ("p_scrap_eur_t", -1),
    ("el_eaf_kwh_per_t", -1),
    ("gas_gj_per_t", -1),
    ("p_gas_eur_gj", -1),
    ("electrodes_kg_per_t", -1),
    ("p_elec_eur_kg", -1),
    ("other_eaf_eur_t", -1),
    ("om_eur_anno", -100),
    ("capex_eur", -1),
    ("f_bf_t_per_t", -0.10),
    ("f_el_t_per_mwh", -0.10),
    ("f_gas_t_per_mwh", -0.10),
    ("wacc_pct", -0.1), ("wacc_pct", 50.1),
    ("vita_anni", -1), ("vita_anni", 2.5),
    ("tolleranza_pct", -1), ("tolleranza_pct", 100.1),
])
def test_valida_rifiuta_singoli_campi(campo, valore):
    d = _demo_kwargs()
    d[campo] = valore
    assert mh777_valida(**d)["valido"] is False


@pytest.mark.parametrize("campo,valore", [
    ("p_t_anno", 0), ("p_t_anno", -3),
    ("coke_gj_per_t", -1),
    ("p_coke_eur_gj", -1),
    ("el_bf_kwh_per_t", -1),
    ("p_el_eur_mwh", -1),
    ("ore_t_per_t", -1),
    ("p_ore_eur_t", -1),
    ("other_bf_eur_t", -1),
    ("scrap_t_per_t", -1),
    ("p_scrap_eur_t", -1),
    ("el_eaf_kwh_per_t", -1),
    ("gas_gj_per_t", -1),
    ("p_gas_eur_gj", -1),
    ("electrodes_kg_per_t", -1),
    ("p_elec_eur_kg", -1),
    ("other_eaf_eur_t", -1),
    ("om_eur_anno", -100),
    ("capex_eur", -1),
    ("f_bf_t_per_t", -0.10),
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
        mh777_calcola(**d)


def test_df_tabella_valori_demo_selezionati():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Produzione acciaio (t/anno)"] == 500000.0
    assert mappa["Costo BF per tonnellata (EUR/t)"] == pytest.approx(
        396.0)


# ------------------------------------------------------- test strutturali
# Aggiunti nel ciclo QA tab777 (adattati dallo schema della tab
# precedente): AST, registry chain-tail, assenza residui della tab
# precedente, chiavi statiche, guard prima degli output, regressione
# sweep chiavi demo vs UI (lezione tab675: KeyError a render).
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
    # Token della tab precedente, costruiti per concatenazione:
    # questo stesso file non li contiene come sottostringhe contigue.
    return ["mh" + "77" + "6", "st" + "77" + "6",
            "tab" + "77" + "6"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w778_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w778_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab777:")


def test_registry_chain_tail_and_count():
    """Registry della nuova tab: il frammento UI apre la tab
    numero 777 (la coda della catena termina con la nuova tab
    e il conteggio atteso delle tab e' 777)."""
    src = _leggi("w778_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 777
    assert src.count("with tab777:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w778_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w778_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st777_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert "key=f" not in src and "key = f" not in src
    assert "st.stop()" in src
    # guard degenere prima di KPI / grafico / tabella / CSV
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w778_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def777[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w778_ui.py")
        usate = set(re.findall(r'_def777\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 24
        assert usate <= set(mh777_demo().keys())
        assert usate == set(mh777_demo().keys())


def test_ui_chiavi_demo_coerenti():
    """Ogni _def777[...] letto dalla UI esiste nel dict demo:
    sweep anti-KeyError a render (lezione dello sweep chiavi demo vs UI)."""
    src = _leggi("w778_ui.py")
    usate = set(re.findall(r'_def777\["([^"]+)"\]', src))
    assert usate
    assert len(usate) == 24
    assert usate <= set(mh777_demo().keys())


def test_ui_riferisce_solo_helper_nuovi():
    src = _leggi("w778_ui.py")
    usati = set(re.findall(r"\b(mh\d+_\w+)\b", src))
    assert usati
    assert all(u.startswith("mh777_") for u in usati)
