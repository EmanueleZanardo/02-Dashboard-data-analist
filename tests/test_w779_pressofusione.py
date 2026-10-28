"""Test tab779 "Pressofusione alluminio:
forno fusorio elettrico a induzione batte il forno a gas?"
(File repo: tests/test_w779_pressofusione.py,
contenuto pronto da scrivere in repo.)

Nuova tab tab779 (pressofusione, file di
lavoro w780). Business case
deterministico di una pressofusione
di alluminio: si fondono P t/anno
di alluminio; baseline forno
fusorio a gas con costo per
tonnellata C_base_per_t =
gas x p_gas + el_base / 1000 x
p_el + other_base EUR/t (el_base
in kWh/t: 1 MWh = 1000 kWh);
alternativa forno fusorio elettrico
a induzione con costo per
tonnellata C_alt_per_t =
el_alt / 1000 x p_el + other_alt
EUR/t; costi annui C_base =
C_base_per_t x P, C_alt_var =
C_alt_per_t x P, C_alt = C_alt_var
+ O&M; risparmio = C_base - C_alt
EUR/anno; CO2 base = gas / 3,6
x P x f_gas + el_base / 1000 x P x
f_el t/anno (gas in GJ/t: 1 MWh =
3,6 GJ; fattori in tCO2/MWh);
CO2 induzione = el_alt / 1000
x P x f_el t/anno (niente gas:
nessun bruciatore da tenere
acceso); CO2 evitata = CO2 base -
CO2 induzione t/anno, PUO'
ESSERE NEGATIVA in questa tab
(elettricita' sporca, o elettricita'
induzione alta: l'induzione puo'
emettere piu' della baseline):
NON e' una guard, NON e' un
degenere, NON monetizzata; CRF =
r (1 + r)^n / ((1 + r)^n - 1) con
r = WACC come frazione, r = 0 ->
1/n, SOLO nel LCO, MAI nei flussi;
LCO base = C_base_per_t EUR/t; LCO
alt = (CAPEX x CRF + O&M) / P +
C_alt_per_t EUR/t (il CAPEX entra
solo annuizzato col CRF);
breakeven prezzo elettricita'
p_el* = (C_base_nonel - C_alt_nonel)
/ ((el_alt - el_base) / 1000) EUR/MWh,
None se denominatore <= 0
(l'induzione non consuma piu'
elettricita' della baseline) e
None se numeratore < 0 (a prezzo
elettrico zero l'induzione e'
gia' piu' cara e il divario cresce
con p_el); breakeven prezzo gas
p_gas* = (C_alt_per_t -
el_base / 1000 x p_el - other_base)
/ gas EUR/GJ, la soglia minima del
prezzo gas a prezzo elettricita'
corrente: sopra di essa l'induzione
vince sui costi variabili (il costo
base cresce con p_gas, il costo
alternativo no), sotto perde;
None se gas <= 0 e None se
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
questa tab confronta SOLO forno
fusorio a gas contro forno fusorio
elettrico a induzione per tonnellata
di alluminio fuso, NON forno a
resistenza, NON forno a crogiolo a
gasolio, NON pressofusione di zinco
o magnesio.

Demo calcolata eseguendo
demo_calcoli() e ricontrollata con
un ricalcolo indipendente da zero
(riga per riga): produzione fusa
5.000 t/anno, forno a gas con
gas 12 GJ/t a 20 EUR/GJ,
elettricita' base 150 kWh/t a 180
EUR/MWh, altri costi base 80 EUR/t;
forno a induzione con elettricita'
550 kWh/t a 180 EUR/MWh, altri
costi 120 EUR/t; O&M annuo 150.000
EUR/anno, CAPEX 2.000.000 EUR,
fattore gas 0,202 tCO2/MWh, fattore
elettricita' 0,35 tCO2/MWh, WACC
6 %, vita 15 anni, tolleranza
MARGINALE 10 % di C_base.

- c_base_per_t = 347.0
- c_alt_per_t = 219.0
- c_base_nonel_per_t = 320.0
- c_alt_nonel_per_t = 120.0
- el_base_mwh_anno = 750.0
- el_alt_mwh_anno = 2750.0
- gas_mwh_anno = 16666.666666666668
- c_base_eur_anno = 1735000.0
- c_alt_var_eur_anno = 1095000.0
- c_alt_eur_anno = 1245000.0
- risparmio_eur_anno = 490000.0
- co2_base_t_anno = 3629.1666666666665
- co2_alt_t_anno = 962.5
- co2_evitata_t_anno = 2666.6666666666665
- crf = 0.10296276395531265
- lco_base_eur_t = 347.0
- lco_alt_eur_t = 290.18510558212506
- van = 2759002.003993082
- tir = 23.46208447627053
- payback = 5
- breakeven_el_eur_mwh = 500.0
- breakeven_gas_eur_gj = 9.333333333333334
- verdetto = 'CONVIENTE'

Scomposizione: costo base = 12 x
20 = 240 di gas + 150 / 1000 x 180
= 27 di elettricita' + 80 altri =
347,00 EUR/t; costo induzione =
550 / 1000 x 180 = 99 di elettricita'
+ 120 altri = 219,00 EUR/t; costo
baseline = 347,00 x 5.000 =
1.735.000 EUR/anno; costo variabile
induzione = 219,00 x 5.000 =
1.095.000 EUR/anno; costo
alternativo = 1.095.000 + 150.000 =
1.245.000 EUR/anno; risparmio =
1.735.000 - 1.245.000 = 490.000
EUR/anno, il 28,24 % di C_base,
sopra la tolleranza del 10 %
(173.500 EUR/anno): verdetto
CONVIENTE; CO2 base = 12 x 5.000 /
3,6 x 0,202 = 3.366,67 di gas + 150
/ 1000 x 5.000 x 0,35 = 262,50 di
elettrica = 3.629,17 t/anno; CO2
induzione = 550 / 1000 x 5.000
x 0,35 = 962,50 t/anno; CO2 evitata =
3.629,17 - 962,50 = 2.666,67 t/anno;
CRF al 6 % per 15 anni =
0,1029627640; LCO base 347,00
EUR/t; LCO alt = (2.000.000 x
0,1029627640 + 150.000) / 5.000 +
219,00 = 71,185106 + 219,00 =
290,185106 EUR/t; flussi: anno 0
-2.000.000, anni 1-15 risparmio
490.000 (piatti); VAN -2.000.000 +
490.000 x 9,712248 (annuita' 15
anni al 6 %) = 2.759.002,00 EUR;
TIR 23,46 %; payback 5 anni (il
cumulato all'anno 4 e' -40.000
EUR, all'anno 5 e' 450.000 EUR,
gia' >= 0); breakeven elettricita'
(320,00 - 120,00) / ((550 - 150) /
1000) = 200,00 / 0,40 = 500,00
EUR/MWh (TETTO: sotto di esso
l'induzione vince sui costi
variabili, sopra perde);
breakeven gas (219,00 - 27,00 -
80,00) / 12 = 112,00 / 12 = 9,33
EUR/GJ (SOGLIA MINIMA: sopra di
essa l'induzione vince sui costi
variabili, sotto perde; il prezzo
gas demo, 20 EUR/GJ, sta sopra la
soglia, coerente con CONVIENTE);
verdetto CONVIENTE perche' il
risparmio 490.000 supera la
tolleranza del 10 % di C_base
(173.500 EUR/anno).
NOTA: il CRF entra SOLO nel LCO di
questa tab: nei flussi il CAPEX
entra intero all'anno 0, mai
annuizzato.
NOTA 2: in questa tab il risparmio
nullo o negativo NON e' degenere:
con prezzo elettricita' 500
EUR/MWh (al tetto) il caso e'
calcolabile (valid=True, flussi
pieni), MARGINALE con VAN
-3.456.837,35 EUR e payback None,
non un errore: -150.000 di
risparmio resta entro la soglia
del 10 % di C_base a quel prezzo
(197.500 EUR/anno).
NOTA 3: la CO2 evitata PUO' essere
negativa in questa tab (non e' una
guard): con fattore gas zero e
fattore elettricita' 1,00 la CO2
base e' 750 t/anno e l'induzione
2.750 t/anno, quindi l'evitata e'
-2.000 t/anno, mentre il verdetto
resta CONVIENTE (stessa economia:
i fattori non toccano i costi).
NOTA 4: i pareggi sono sui costi
variabili, NON sul risparmio: al
pareggio elettrico esatto
(500 EUR/MWh) i costi per
tonnellata si eguagliano (395,00
EUR/t) ma il risparmio e' -150.000
EUR/anno, cioe' solo l'O&M; al
pareggio gas esatto (9,33 EUR/GJ)
i costi per tonnellata si
eguagliano (219,00 EUR/t) ma il
risparmio e' di nuovo -150.000
EUR/anno. Il breakeven elettrico
e' None con elettricita' induzione
150 kWh/t (denominatore nullo:
l'induzione non consuma piu'
elettricita' della baseline) e con
altri costi induzione 400 EUR/t
(numeratore negativo). Il
breakeven gas e' None con gas
nullo, e vale come identita' a
prezzo elettricita' corrente:
27,00 + 80,00 + 12 x 9,33 = 219,00.
Attenzione: i due pareggi hanno
verso opposto: sopra il tetto
elettrico l'induzione perde, sopra
la soglia gas l'induzione vince.
NOTA 5: il verdetto CONVIENTE del
demo non e' un errore: con prezzo
gas 5 EUR/GJ (sotto la soglia
9,33) il caso diventa NON_CONVIENTE
(risparmio -410.000 EUR/anno);
con prezzo elettricita' 600 EUR/MWh
(sopra il tetto 500) diventa
NON_CONVIENTE (risparmio -350.000,
VAN -5.399.287,15).
NOTA 6: il payback usa il cumulato
>= 0 (regola >= del brief): con
CAPEX nullo il payback e' 0 (non
1); con flussi [-100, 50, 50] il
payback e' 2 (il cumulato all'anno
2 e' zero, e zero basta); con CAPEX
1.960.000 EUR il payback e' 4
(divisione esatta 1.960.000 /
490.000).
NOTA 7: i valori demo sono stati
ricalcolati da zero con un calcolo
indipendente: il ricalcolo esatto
(senza arrotondamenti intermedi)
da' costo base 347,00, costo
induzione 219,00, costo baseline
1.735.000, costo variabile
induzione 1.095.000, costo
alternativo 1.245.000, risparmio
490.000, CO2 base 3.629,17,
induzione 962,50, evitata
2.666,67, CRF 0,1029627640, LCO base
347,00, LCO alt 290,185106, VAN
2.759.002,00, TIR 23,46 %, payback
5, breakeven elettricita' 500,00
(tetto), breakeven gas 9,33
(soglia minima), verdetto
CONVIENTE: i file usano i valori
esatti.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w780_helpers import (
    demo_calcoli,
    mh779_breakeven_el,
    mh779_breakeven_gas,
    mh779_c_alt,
    mh779_c_alt_per_t,
    mh779_c_alt_var,
    mh779_c_base,
    mh779_c_base_nonel,
    mh779_c_base_per_t,
    mh779_c_alt_nonel,
    mh779_calcola,
    mh779_co2_alt,
    mh779_co2_base,
    mh779_co2_evitata,
    mh779_crf,
    mh779_csv,
    mh779_demo,
    mh779_flussi,
    mh779_int_pos,
    mh779_lco_alt,
    mh779_lco_base,
    mh779_num,
    mh779_nneg,
    mh779_payback,
    mh779_pct_tolleranza,
    mh779_pct_wacc,
    mh779_pos,
    mh779_risparmio,
    mh779_tir,
    mh779_valida,
    mh779_van,
    mh779_verdetto,
)

# Costanti demo a piena precisione (per la validazione
# _DEMO contro demo_calcoli() con tolleranza relativa
# < 1e-9: vedi test_demo_costanti_vs_demo_calcoli).
_DEMO = {
    "c_base_per_t": 347.0,
    "c_alt_per_t": 219.0,
    "c_base_nonel_per_t": 320.0,
    "c_alt_nonel_per_t": 120.0,
    "el_base_mwh_anno": 750.0,
    "el_alt_mwh_anno": 2750.0,
    "gas_mwh_anno": 16666.666666666668,
    "c_base_eur_anno": 1735000.0,
    "c_alt_var_eur_anno": 1095000.0,
    "c_alt_eur_anno": 1245000.0,
    "risparmio_eur_anno": 490000.0,
    "co2_base_t_anno": 3629.1666666666665,
    "co2_alt_t_anno": 962.5,
    "co2_evitata_t_anno": 2666.6666666666665,
    "crf": 0.10296276395531265,
    "lco_base_eur_t": 347.0,
    "lco_alt_eur_t": 290.18510558212506,
    "van": 2759002.003993082,
    "tir": 23.46208447627053,
    "breakeven_el_eur_mwh": 500.0,
    "breakeven_gas_eur_gj": 9.333333333333334,
}


def _demo_kwargs():
    return dict(mh779_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh779_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh779_num(3, "x") == 3.0
    assert mh779_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh779_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh779_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh779_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh779_pos(0, "x")
    with pytest.raises(ValueError):
        mh779_pos(-1, "x")
    assert mh779_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh779_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh779_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh779_int_pos(0, "x")


def test_pct_wacc_limiti():
    assert mh779_pct_wacc(0, "x") == 0.0
    assert mh779_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh779_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh779_pct_tolleranza(0, "x") == 0.0
    assert mh779_pct_tolleranza(100, "x") == 100.0
    assert mh779_pct_tolleranza(10.0, "x") == 10.0
    with pytest.raises(ValueError):
        mh779_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh779_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_c_base_per_t_scomposizione():
    assert mh779_c_base_per_t(12, 20, 150, 180,
                              80) == pytest.approx(347.0)
    assert mh779_c_base_per_t(0, 20, 0, 180,
                              0) == pytest.approx(0.0)
    assert mh779_c_base_per_t(12, 20, 150, 0,
                              80) == pytest.approx(320.0)
    with pytest.raises(ValueError):
        mh779_c_base_per_t(-1, 20, 150, 180, 80)
    with pytest.raises(ValueError):
        mh779_c_base_per_t(12, -1, 150, 180, 80)


def test_c_alt_per_t_scomposizione():
    assert mh779_c_alt_per_t(550, 180,
                             120) == pytest.approx(219.0)
    assert mh779_c_alt_per_t(550, 0,
                             120) == pytest.approx(120.0)
    assert mh779_c_alt_per_t(0, 180,
                             120) == pytest.approx(120.0)
    assert mh779_c_alt_per_t(550, 180,
                             0) == pytest.approx(99.0)
    with pytest.raises(ValueError):
        mh779_c_alt_per_t(550, -1, 120)
    with pytest.raises(ValueError):
        mh779_c_alt_per_t(550, 180, -1)


def test_c_nonel():
    assert mh779_c_base_nonel(347.0, 150, 180) == pytest.approx(320.0)
    assert mh779_c_alt_nonel(219.0, 550, 180) == pytest.approx(120.0)
    assert mh779_c_base_nonel(347.0, 150, 0) == pytest.approx(347.0)
    with pytest.raises(ValueError):
        mh779_c_base_nonel(347.0, -1, 180)


def test_c_base_c_alt_var_c_alt():
    assert mh779_c_base(347.0, 5000) == pytest.approx(1735000.0)
    assert mh779_c_alt_var(219.0, 5000) == pytest.approx(
        1095000.0)
    assert mh779_c_alt(1095000.0, 150000) == pytest.approx(
        1245000.0)
    with pytest.raises(ValueError):
        mh779_c_base(347.0, 0)
    with pytest.raises(ValueError):
        mh779_c_alt(1095000.0, -1)


def test_co2_base_alt_evitata():
    assert mh779_co2_base(12, 5000, 150, 0.202,
                          0.35) == pytest.approx(3629.1666666666665)
    assert mh779_co2_alt(550, 5000,
                         0.35) == pytest.approx(962.5)
    assert mh779_co2_alt(550, 5000,
                         0) == pytest.approx(0.0)
    assert mh779_co2_base(0, 5000, 150, 0.202,
                          0.35) == pytest.approx(262.5)
    assert mh779_co2_evitata(3629.1666666666665,
                             962.5) == pytest.approx(
        2666.6666666666665)
    assert mh779_co2_evitata(100.0, 150.0) == pytest.approx(-50.0)
    with pytest.raises(ValueError):
        mh779_co2_base(12, 5000, 150, -0.10, 0.35)


def test_co2_evitata_puo_essere_negativa_via_calcola():
    """Differenza chiave di questa tab: via
    mh779_calcola la CO2 evitata PUO' essere
    negativa (fattore gas zero, fattore
    elettricita' alto)."""
    bc = _variante(f_gas_t_per_mwh=0, f_el_t_per_mwh=1.0)
    assert bc["co2_base_t_anno"] == pytest.approx(750.0)
    assert bc["co2_alt_t_anno"] == pytest.approx(2750.0)
    assert bc["co2_evitata_t_anno"] == pytest.approx(-2000.0)
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_co2_formula_componenti():
    """CO2 base = gas x f_gas + elettricita' base x f_el,
    CO2 induzione = elettricita' induzione x f_el,
    con le conversioni kWh->MWh e GJ->MWh."""
    for bc in (demo_calcoli(),
               _variante(f_gas_t_per_mwh=0, f_el_t_per_mwh=1.0),
               _variante(el_alt_kwh_per_t=150)):
        atteso_base = (bc["gas_mwh_anno"] * bc["f_gas_t_per_mwh"]
                       + bc["el_base_mwh_anno"] * bc["f_el_t_per_mwh"])
        assert bc["co2_base_t_anno"] == pytest.approx(atteso_base)
        atteso_alt = (bc["el_alt_mwh_anno"] * bc["f_el_t_per_mwh"])
        assert bc["co2_alt_t_anno"] == pytest.approx(atteso_alt)


def test_risparmio_segno():
    assert mh779_risparmio(1735000.0, 1245000.0) == \
        pytest.approx(490000.0)
    assert mh779_risparmio(1735000.0, 1735000.0) == 0.0
    assert mh779_risparmio(1975000.0, 2125000.0) == \
        pytest.approx(-150000.0)


def test_crf_solo_lco():
    assert mh779_crf(6.0, 15) == pytest.approx(0.10296276395531265)
    assert mh779_crf(0.0, 15) == pytest.approx(1.0 / 15.0)
    assert mh779_crf(6.0, 20) == pytest.approx(0.0871845569768514)
    with pytest.raises(ValueError):
        mh779_crf(50.1, 15)
    with pytest.raises(ValueError):
        mh779_crf(6.0, 0)


def test_lco():
    assert mh779_lco_base(1735000.0, 5000) == pytest.approx(347.0)
    assert mh779_lco_alt(2000000, 0.10296276395531265, 150000,
                         219.0, 5000) == pytest.approx(
        290.18510558212506)
    assert mh779_lco_base(1735000.0, 0) is None
    assert mh779_lco_alt(2000000, 0.10296276395531265, 150000,
                         219.0, 0) is None
    assert mh779_lco_alt(2000000, 0.10296276395531265, 150000,
                         219.0, -5) is None
    # Il CAPEX entra nel LCO solo annuizzato: con CAPEX nullo
    # il LCO alt e' (O&M / P) + C_alt_per_t.
    assert mh779_lco_alt(0, 0.10296276395531265, 150000,
                         219.0, 5000) == pytest.approx(249.0)


def test_crf_mai_nei_flussi():
    """Il CRF entra SOLO nel LCO: i flussi usano il
    CAPEX intero all'anno 0 e la VAN dai flussi non
    dipende dal CRF (cambiando il WACC cambia la VAN
    per lo sconto, non per il CRF)."""
    bc = demo_calcoli()
    assert bc["flussi"][0] == -2000000
    assert bc["flussi"][1:] == [490000.0] * 15
    assert bc["van"] == pytest.approx(mh779_van(bc["flussi"], 6.0))
    bc0 = _variante(wacc_pct=0)
    assert bc0["van"] == pytest.approx(sum(bc0["flussi"]))
    assert bc0["crf"] == pytest.approx(1.0 / 15.0)
    assert bc0["lco_alt_eur_t"] == pytest.approx(275.6666666666667)


def test_breakeven_el_demo_e_varianti():
    # Demo: (320,00 - 120,00) / ((550 - 150) / 1000) = 500,00.
    assert mh779_breakeven_el(320.0, 120.0, 550,
                              150) == pytest.approx(500.0)
    # Numeratore zero: pareggio zero, valido.
    assert mh779_breakeven_el(320.0, 320.0, 550,
                              150) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh779_breakeven_el(320.0, 120.0, -1, 150)


def test_breakeven_el_none_casi():
    # Denominatore <= 0: el_alt uguale o sotto el_base.
    assert mh779_breakeven_el(320.0, 120.0, 150, 150) is None
    assert mh779_breakeven_el(320.0, 120.0, 100, 150) is None
    # Numeratore < 0: costo induzione senza elettricita'
    # sopra il costo base senza elettricita'.
    assert mh779_breakeven_el(320.0, 400.0, 550, 150) is None


def test_breakeven_gas_demo_e_varianti():
    # Demo: (219,00 - 27,00 - 80,00) / 12 = 9,3333333.
    assert mh779_breakeven_gas(219.0, 150, 180, 80,
                               12) == pytest.approx(
        9.333333333333334)
    # Numeratore zero: pareggio zero, valido.
    assert mh779_breakeven_gas(107.0, 150, 180, 80,
                               12) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh779_breakeven_gas(219.0, 150, 180, 80, -1)


def test_breakeven_gas_none_casi():
    # Gas <= 0: nessun prezzo da calcolare.
    assert mh779_breakeven_gas(219.0, 150, 180, 80, 0) is None
    # Numeratore < 0: a prezzo gas zero il costo base
    # senza gas e' gia' sopra il costo alternativo.
    assert mh779_breakeven_gas(0, 150, 0, 80, 12) is None


def test_breakeven_verifica_pareggio():
    """Al prezzo elettrico di pareggio i costi per tonnellata
    si eguagliano: C_alt_per_t(p*) = C_base_per_t(p*).
    Il risparmio invece e' -O&M, non zero (i pareggi non
    includono l'O&M). Al prezzo gas di pareggio vale lo
    stesso: C_base_per_t = C_alt_per_t e risparmio -O&M.
    Per il gas vale l'identita' a prezzo elettrico
    corrente: el_base / 1000 x p_el + other_base +
    gas x be_gas = C_alt_per_t."""
    bc = _variante(p_el_eur_mwh=500.0)
    assert bc["c_base_per_t"] == pytest.approx(bc["c_alt_per_t"])
    assert bc["risparmio_eur_anno"] == pytest.approx(-150000.0)
    bc2 = _variante(p_gas_eur_gj=9.333333333333334)
    assert bc2["c_base_per_t"] == pytest.approx(bc2["c_alt_per_t"])
    assert bc2["risparmio_eur_anno"] == pytest.approx(-150000.0)
    demo = demo_calcoli()
    assert (demo["el_base_kwh_per_t"] / 1000.0
            * demo["p_el_eur_mwh"]
            + demo["other_base_eur_t"]
            + demo["gas_gj_per_t"]
            * demo["breakeven_gas_eur_gj"]) == pytest.approx(
        demo["c_alt_per_t"])


def test_pareggi_versi_opposti():
    """Sotto il tetto elettrico l'induzione vince sui costi
    variabili, sopra perde; sopra la soglia gas
    l'induzione vince, sotto perde."""
    be_el = demo_calcoli()["breakeven_el_eur_mwh"]
    assert _variante(p_el_eur_mwh=be_el - 10)[
        "c_alt_per_t"] < _variante(p_el_eur_mwh=be_el - 10)[
        "c_base_per_t"]
    assert _variante(p_el_eur_mwh=be_el + 10)[
        "c_alt_per_t"] > _variante(p_el_eur_mwh=be_el + 10)[
        "c_base_per_t"]
    be_gas = demo_calcoli()["breakeven_gas_eur_gj"]
    assert _variante(p_gas_eur_gj=be_gas + 1)[
        "c_alt_per_t"] < _variante(p_gas_eur_gj=be_gas + 1)[
        "c_base_per_t"]
    assert _variante(p_gas_eur_gj=be_gas - 1)[
        "c_alt_per_t"] > _variante(p_gas_eur_gj=be_gas - 1)[
        "c_base_per_t"]


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh779_flussi(2000000, 490000.0, 15)
    assert len(fl) == 16
    assert fl[0] == -2000000
    assert all(f == 490000.0 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = demo_calcoli()
    assert bc["van"] == pytest.approx(2759002.003993082)
    assert mh779_van([-2000000] + [490000.0] * 15,
                     0) == pytest.approx(5350000.0)
    assert mh779_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = demo_calcoli()
    assert bc["tir"] == pytest.approx(23.46208447627053)
    assert mh779_tir([-2000000] + [490000.0] * 15) == \
        pytest.approx(0.2346208447627053)
    tir = mh779_tir([-2000000] + [490000.0] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate(
                  [-2000000] + [490000.0] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    """Payback con cumulato >= 0: il cumulato nullo basta."""
    assert mh779_payback([-2000000] + [490000.0] * 15) == 5
    assert mh779_payback([-2000000] + [-1000.0] * 15) is None
    assert mh779_payback([0] + [490000.0] * 15) == 0
    assert mh779_payback([-100] + [50] * 2) == 2
    assert mh779_payback([-1960000.0] +
                         [490000.0] * 4) == 4


def test_verdetto():
    assert mh779_verdetto(490000.0, 1735000.0,
                          10.0) == "CONVIENTE"
    assert mh779_verdetto(173500.0, 1735000.0,
                          10.0) == "MARGINALE"
    assert mh779_verdetto(0.0, 1735000.0, 10.0) == "MARGINALE"
    assert mh779_verdetto(-173500.0, 1735000.0,
                          10.0) == "MARGINALE"
    assert mh779_verdetto(-173501.0, 1735000.0,
                          10.0) == "NON_CONVIENTE"
    assert mh779_verdetto(-410000.0, 1735000.0,
                          10.0) == "NON_CONVIENTE"
    assert mh779_verdetto(490000.0, 1735000.0,
                          0.0) == "CONVIENTE"
    assert mh779_verdetto(-100.0, 1735000.0,
                          0.0) == "NON_CONVIENTE"
    assert mh779_verdetto(None, 1735000.0,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh779_verdetto(float("nan"), 1735000.0, 10.0)
    with pytest.raises(ValueError):
        mh779_verdetto(100.0, -1, 10.0)
    with pytest.raises(ValueError):
        mh779_verdetto(100.0, 1735000.0, 100.1)


def test_valida_demo_ok():
    v = mh779_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("p_t_anno", "5000"),
                       ("p_t_anno", float("nan")),
                       ("p_t_anno", float("inf")),
                       ("p_t_anno", True),
                       ("p_gas_eur_gj", None),
                       ("gas_gj_per_t", "12")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh779_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("p_t_anno", 0),
                          ("p_t_anno", -1),
                          ("gas_gj_per_t", -1),
                          ("p_gas_eur_gj", -1),
                          ("el_base_kwh_per_t", -1),
                          ("p_el_eur_mwh", -1),
                          ("other_base_eur_t", -1),
                          ("el_alt_kwh_per_t", -1),
                          ("other_alt_eur_t", -1),
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
        assert mh779_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"gas_gj_per_t": 0,
              "p_gas_eur_gj": 0,
              "el_base_kwh_per_t": 0,
              "p_el_eur_mwh": 0,
              "other_base_eur_t": 0,
              "el_alt_kwh_per_t": 0,
              "other_alt_eur_t": 0,
              "om_eur_anno": 0,
              "capex_eur": 0,
              "f_gas_t_per_mwh": 0,
              "f_el_t_per_mwh": 0,
              "wacc_pct": 0,
              "tolleranza_pct": 0})
    assert mh779_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    assert mh779_valida(**d)["valido"] is True


def test_valida_non_controlla_risparmio_calcola_neppure():
    """La validazione input NON controlla il risparmio
    (e' un esito, non un range) e in questa tab
    nemmeno mh779_calcola lo controlla: con prezzo
    elettricita' 600 EUR/MWh (sopra il tetto 500)
    il caso resta CALCOLABILE."""
    d = _demo_kwargs()
    d["p_el_eur_mwh"] = 600
    assert mh779_valida(**d)["valido"] is True
    bc = _variante(p_el_eur_mwh=600)
    assert bc["valid"] is True
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["flussi"]
    assert bc["payback"] is None


def test_demo_dict():
    d = mh779_demo()
    assert d["p_t_anno"] == 5000
    assert d["gas_gj_per_t"] == 12
    assert d["p_gas_eur_gj"] == 20
    assert d["el_base_kwh_per_t"] == 150
    assert d["p_el_eur_mwh"] == 180
    assert d["other_base_eur_t"] == 80
    assert d["el_alt_kwh_per_t"] == 550
    assert d["other_alt_eur_t"] == 120
    assert d["om_eur_anno"] == 150000
    assert d["capex_eur"] == 2000000
    assert d["f_gas_t_per_mwh"] == 0.202
    assert d["f_el_t_per_mwh"] == 0.35
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
    assert bc["payback"] == 5
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_demo_calcoli_fisica():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["c_base_per_t"] == pytest.approx(347.0)
    assert bc["c_alt_per_t"] == pytest.approx(219.0)
    assert bc["el_base_mwh_anno"] == pytest.approx(750.0)
    assert bc["el_alt_mwh_anno"] == pytest.approx(2750.0)
    assert bc["gas_mwh_anno"] == pytest.approx(16666.666666666668)
    assert bc["co2_evitata_t_anno"] == pytest.approx(2666.6666666666665)


def test_demo_calcoli_economia():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(1735000.0)
    assert bc["c_alt_var_eur_anno"] == pytest.approx(1095000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(1245000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(490000.0)
    assert bc["breakeven_el_eur_mwh"] == pytest.approx(500.0)
    assert bc["breakeven_gas_eur_gj"] == pytest.approx(
        9.333333333333334)


def test_demo_calcoli_finanza():
    bc = demo_calcoli()
    assert bc["crf"] == pytest.approx(0.10296276395531265)
    assert bc["lco_base_eur_t"] == pytest.approx(347.0)
    assert bc["lco_alt_eur_t"] == pytest.approx(290.18510558212506)
    assert bc["van"] == pytest.approx(2759002.003993082)
    assert bc["tir"] == pytest.approx(23.46208447627053)
    assert bc["payback"] == 5
    assert bc["verdetto"] == "CONVIENTE"


def test_demo_flussi_e_cumulato():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -2000000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(490000.0)
               for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -2000000
    assert righe.iloc[4]["Cumulato (EUR)"] == pytest.approx(-40000.0)
    assert righe.iloc[5]["Cumulato (EUR)"] == pytest.approx(450000.0)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(
        5350000.0)
    assert righe.iloc[15]["Flusso (EUR/anno)"] == pytest.approx(
        490000.0)


def test_demo_tabella_righe():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Produzione fusa (t/anno)"] == pytest.approx(
        5000.0)
    assert mappa["Costo base per tonnellata (EUR/t)"] == pytest.approx(
        347.0)
    assert mappa["Costo induzione per tonnellata (EUR/t)"] == pytest.approx(
        219.0)
    assert mappa["Elettricita' induzione (MWh/anno)"] == pytest.approx(
        2750.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(
        1245000.0)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(490000.0)
    assert mappa["Payback (anni)"] == 5
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo elettricita' (EUR/MWh)"] == \
        pytest.approx(500.0)
    assert mappa["Breakeven prezzo gas (EUR/GJ)"] == \
        pytest.approx(9.333333333333334)


def test_demo_coerenza_interna():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["c_base_per_t"] * bc["p_t_anno"] == \
        pytest.approx(bc["c_base_eur_anno"])
    assert bc["c_alt_per_t"] * bc["p_t_anno"] == \
        pytest.approx(bc["c_alt_var_eur_anno"])
    assert bc["co2_base_t_anno"] - bc["co2_alt_t_anno"] == \
        pytest.approx(bc["co2_evitata_t_anno"])
    assert bc["c_base_eur_anno"] / bc["p_t_anno"] == \
        pytest.approx(bc["lco_base_eur_t"])
    assert (bc["capex_eur"] * bc["crf"] + bc["om_eur_anno"]) / \
        bc["p_t_anno"] + bc["c_alt_per_t"] == \
        pytest.approx(bc["lco_alt_eur_t"])
    assert bc["c_base_nonel_per_t"] + \
        bc["el_base_kwh_per_t"] / 1000.0 * bc["p_el_eur_mwh"] == \
        pytest.approx(bc["c_base_per_t"])


def test_demo_contro_riconteggio_indipendente():
    p, gas, pg = 5000, 12, 20
    elb, pel, ob = 150, 180, 80
    ela, oa, om, cx = 550, 120, 150000, 2000000
    fg, fel, wacc, vita = 0.202, 0.35, 6.0, 15
    cb = gas * pg + elb / 1000.0 * pel + ob
    ca = ela / 1000.0 * pel + oa
    cbase = cb * p
    cav = ca * p
    caa = cav + om
    risp = cbase - caa
    co2b = gas / 3.6 * p * fg + elb / 1000.0 * p * fel
    co2a = ela / 1000.0 * p * fel
    r = wacc / 100.0
    crf = r * (1 + r) ** vita / ((1 + r) ** vita - 1.0)
    lco_b = cb
    lco_a = (cx * crf + om) / p + ca
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    be_el = (cb - elb / 1000.0 * pel
             - (ca - ela / 1000.0 * pel)) / ((ela - elb) / 1000.0)
    be_gas = (ca - elb / 1000.0 * pel - ob) / gas
    bc = demo_calcoli()
    assert bc["c_base_per_t"] == pytest.approx(cb)
    assert bc["c_alt_per_t"] == pytest.approx(ca)
    assert bc["c_base_eur_anno"] == pytest.approx(cbase)
    assert bc["c_alt_var_eur_anno"] == pytest.approx(cav)
    assert bc["c_alt_eur_anno"] == pytest.approx(caa)
    assert bc["risparmio_eur_anno"] == pytest.approx(risp)
    assert bc["co2_base_t_anno"] == pytest.approx(co2b)
    assert bc["co2_alt_t_anno"] == pytest.approx(co2a)
    assert bc["crf"] == pytest.approx(crf)
    assert bc["lco_base_eur_t"] == pytest.approx(lco_b)
    assert bc["lco_alt_eur_t"] == pytest.approx(lco_a)
    assert bc["van"] == pytest.approx(van)
    assert bc["breakeven_el_eur_mwh"] == pytest.approx(be_el)
    assert bc["breakeven_gas_eur_gj"] == pytest.approx(be_gas)


# ---------------------------------------------------------------- varianti
def test_demo_conviente():
    """Il demo e' CONVIENTE: il risparmio 490.000 supera
    la tolleranza del 10 % di C_base (173.500), la VAN e'
    positiva e il payback e' 5 anni."""
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] > 0.0
    assert bc["payback"] == 5
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_gas_sotto_soglia_non_conviente():
    """Gas 5 EUR/GJ (sotto la soglia 9,33): costo base
    167 EUR/t, risparmio -410.000, NON_CONVIENTE."""
    bc = _variante(p_gas_eur_gj=5)
    assert bc["valid"] is True
    assert bc["c_base_per_t"] == pytest.approx(167.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-410000.0)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_pareggio_el_esatto():
    """Al tetto elettrico esatto (500 EUR/MWh) i
    costi per tonnellata si eguagliano (395,00 EUR/t)
    ma il risparmio e' -150.000 (solo l'O&M): VAN
    -3.456.837,35, TIR None, payback mai,
    verdetto MARGINALE."""
    bc = _variante(p_el_eur_mwh=500.0)
    assert bc["c_base_per_t"] == pytest.approx(bc["c_alt_per_t"])
    assert bc["risparmio_eur_anno"] == pytest.approx(-150000.0)
    assert bc["van"] == pytest.approx(-3456837.3481611474)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "MARGINALE"


def test_variante_pareggio_gas_esatto():
    """Al prezzo gas di pareggio esatto (9,33 EUR/GJ) i
    costi per tonnellata si eguagliano (219,00 EUR/t)
    ma il risparmio e' -150.000 (solo l'O&M): VAN
    -3.456.837,35, payback mai, NON_CONVIENTE (a
    questo prezzo C_base e' solo 1.095.000 EUR/anno,
    quindi la soglia del 10 % e' 109.500 EUR/anno e
    150.000 la supera: a differenza del pareggio
    elettrico, dove C_base e' 1.975.000 e la soglia
    197.500 rende lo stesso -150.000 MARGINALE)."""
    bc = _variante(p_gas_eur_gj=9.333333333333334)
    assert bc["c_base_per_t"] == pytest.approx(bc["c_alt_per_t"])
    assert bc["risparmio_eur_anno"] == pytest.approx(-150000.0)
    assert bc["van"] == pytest.approx(-3456837.3481611474)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_sopra_tetto_el():
    """Prezzo elettricita' 600 EUR/MWh (sopra il
    tetto 500): risparmio -350.000, VAN
    -5.399.287,15, TIR None, payback mai,
    verdetto NON_CONVIENTE."""
    bc = _variante(p_el_eur_mwh=600)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(-350000.0)
    assert bc["van"] == pytest.approx(-5399287.145709344)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_tolleranza_zero_demo_conviente():
    """Con tolleranza 0 % lo stesso demo resta
    CONVIENTE (risparmio positivo, soglia zero)."""
    bc = _variante(tolleranza_pct=0)
    assert bc["risparmio_eur_anno"] == pytest.approx(490000.0)
    assert bc["van"] == pytest.approx(2759002.003993082)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    """Payback regola >=: con CAPEX nullo il payback e' 0,
    non 1 (all'anno 0 il cumulato e' gia' zero)."""
    bc = _variante(capex_eur=0)
    assert bc["capex_eur"] == 0
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(4759002.003993082)
    assert bc["lco_alt_eur_t"] == pytest.approx(249.0)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_divisione_esatta_payback():
    """CAPEX 1.960.000 EUR: divisione esatta
    1.960.000 / 490.000 = 4 anni, payback 4
    (regola >=: il cumulato nullo basta)."""
    bc = _variante(capex_eur=1960000)
    assert bc["payback"] == 4
    assert bc["van"] == pytest.approx(2799002.003993082)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(5350000.0)
    assert bc["lco_alt_eur_t"] == pytest.approx(275.6666666666667)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_vita_diversa():
    bc = _variante(vita_anni=10)
    assert len(bc["flussi"]) == 11
    assert bc["van"] == pytest.approx(1606442.6551932008)
    assert bc["payback"] == 5
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_om_alto():
    """O&M 700.000 EUR/anno: risparmio -60.000,
    verdetto MARGINALE (entro la soglia 173.500)."""
    bc = _variante(om_eur_anno=700000)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(-60000.0)
    assert bc["payback"] is None
    assert bc["verdetto"] == "MARGINALE"


def test_variante_breakeven_el_none_denominatore():
    """Elettricita' induzione uguale alla baseline
    (150 kWh/t): breakeven elettrico None,
    caso calcolabile CONVIENTE."""
    bc = _variante(el_alt_kwh_per_t=150)
    assert bc["valid"] is True
    assert bc["breakeven_el_eur_mwh"] is None
    assert bc["risparmio_eur_anno"] == pytest.approx(850000.0)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_breakeven_el_none_numeratore():
    """Altri costi induzione 400 EUR/t: costo induzione
    senza elettricita' 400 sopra il costo base senza
    elettricita' 320: breakeven elettrico None."""
    bc = _variante(other_alt_eur_t=400)
    assert bc["valid"] is True
    assert bc["breakeven_el_eur_mwh"] is None


def test_variante_breakeven_gas_none_gas_nullo():
    """Gas nullo: breakeven gas None, caso calcolabile
    (risparmio -710.000, NON_CONVIENTE)."""
    bc = _variante(gas_gj_per_t=0)
    assert bc["valid"] is True
    assert bc["breakeven_gas_eur_gj"] is None
    assert bc["risparmio_eur_anno"] == pytest.approx(-710000.0)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_breakeven_gas_none_numeratore():
    """Prezzo elettricita' zero e altri costi induzione
    nulli: costo induzione 0 sotto il costo base senza
    gas 80: breakeven gas None (numeratore negativo)."""
    bc = _variante(p_el_eur_mwh=0, other_alt_eur_t=0)
    assert bc["valid"] is True
    assert bc["breakeven_gas_eur_gj"] is None


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
    assert mh779_verdetto(None, 1735000.0, 10.0) == "NON_CALCOLABILE"
    assert demo_calcoli()["verdetto"] != "NON_CALCOLABILE"


def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"p_t_anno": 0}, {"p_t_anno": -1},
               {"gas_gj_per_t": -1},
               {"p_gas_eur_gj": -1},
               {"el_base_kwh_per_t": -1},
               {"p_el_eur_mwh": -1},
               {"other_base_eur_t": -1},
               {"el_alt_kwh_per_t": -1},
               {"other_alt_eur_t": -1},
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
        assert mh779_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"p_t_anno": "5000"},
               {"p_t_anno": float("nan")},
               {"p_gas_eur_gj": float("inf")},
               {"capex_eur": True},
               {"gas_gj_per_t": "12"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh779_valida(**d)["valido"] is False


def test_risparmio_negativo_non_degenere():
    """Differenza chiave: risparmio nullo o
    negativo resta calcolabile, con flussi pieni e
    VAN negativa; cosi' anche la CO2 evitata
    negativa resta calcolabile, e cosi' i
    breakeven None restano calcolabili."""
    for kw in ({"p_el_eur_mwh": 600},
               {"p_gas_eur_gj": 5}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["verdetto"] in ("NON_CONVIENTE", "MARGINALE")
        assert bc["flussi"]
    bc = _variante(f_gas_t_per_mwh=0, f_el_t_per_mwh=1.0)
    assert bc["co2_evitata_t_anno"] < 0.0
    assert bc["valid"] is True
    bc2 = _variante(el_alt_kwh_per_t=150)
    assert bc2["breakeven_el_eur_mwh"] is None
    assert bc2["valid"] is True
    bc3 = _variante(gas_gj_per_t=0)
    assert bc3["breakeven_gas_eur_gj"] is None
    assert bc3["valid"] is True


def test_co2_evitata_segno_funzione_pura():
    assert mh779_co2_evitata(100.0, 150.0) == pytest.approx(-50.0)


def test_verdetto_non_calcolabile_solo_risparmio_none():
    assert mh779_verdetto(None, 1735000.0, 10.0) == "NON_CALCOLABILE"
    assert demo_calcoli()["verdetto"] != "NON_CALCOLABILE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = demo_calcoli()
    testo = mh779_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert "c_base_per_t;347.0" in testo
    assert "c_alt_per_t;219.0" in testo
    assert "c_base_eur_anno;1735000.0" in testo
    assert "c_alt_var_eur_anno;1095000.0" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_el_eur_mwh" in testo
    assert "breakeven_gas_eur_gj" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = demo_calcoli()
    testo = mh779_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"c_alt_per_t;{bc['c_alt_per_t']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = demo_calcoli()
    testo = mh779_csv(bc, _demo_kwargs())
    for chiave in _demo_kwargs():
        assert f"{chiave};" in testo


def test_monotonia_prezzo_el_decrescente():
    # Il risparmio CALA con p_el (l'induzione consuma piu'
    # elettricita' della baseline): pendenza
    # -2.000 EUR/anno per EUR/MWh (5.000 t x
    # (550 - 150) / 1000 = 2.000 MWh/anno).
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_el_eur_mwh=190)["risparmio_eur_anno"]
    basso = _variante(p_el_eur_mwh=170)["risparmio_eur_anno"]
    assert basso > base > alto
    assert base - alto == pytest.approx(20000.0)
    assert basso - base == pytest.approx(20000.0)


def test_monotonia_prezzo_gas_crescente():
    # Il risparmio CRESCE con p_gas (solo la baseline
    # brucia gas): pendenza +60.000 EUR/anno per EUR/GJ
    # (5.000 t x 12 GJ/t).
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas_eur_gj=21)["risparmio_eur_anno"]
    basso = _variante(p_gas_eur_gj=19)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(60000.0)
    assert base - basso == pytest.approx(60000.0)


def test_monotonia_elettricita_alt():
    # Piu' elettricita' induzione, piu' cara l'alternativa:
    # +10 kWh/t a 180 EUR/MWh = +1,80 EUR/t =
    # -9.000 EUR/anno di risparmio.
    base = demo_calcoli()["risparmio_eur_anno"]
    assert _variante(el_alt_kwh_per_t=560)[
        "risparmio_eur_anno"] == pytest.approx(base - 9000.0)
    assert _variante(el_alt_kwh_per_t=540)[
        "risparmio_eur_anno"] == pytest.approx(base + 9000.0)


def test_demo_deterministica_due_chiamate():
    a = demo_calcoli()
    b = demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh779_demo().keys()) == {
        "p_t_anno",
        "gas_gj_per_t", "p_gas_eur_gj",
        "el_base_kwh_per_t", "p_el_eur_mwh",
        "other_base_eur_t",
        "el_alt_kwh_per_t", "other_alt_eur_t",
        "om_eur_anno", "capex_eur",
        "f_gas_t_per_mwh", "f_el_t_per_mwh",
        "wacc_pct", "vita_anni", "tolleranza_pct"}


@pytest.mark.parametrize("p_gas,atteso", [
    (20, 347.0),
    (5, 167.0),
    (9.333333333333334, 219.0),
])
def test_c_base_per_t_parametrizzato(p_gas, atteso):
    assert mh779_c_base_per_t(12, p_gas, 150, 180,
                              80) == pytest.approx(atteso)


@pytest.mark.parametrize("campo,valore", [
    ("p_t_anno", 0), ("p_t_anno", -3),
    ("gas_gj_per_t", -1),
    ("p_gas_eur_gj", -1),
    ("el_base_kwh_per_t", -1),
    ("p_el_eur_mwh", -1),
    ("other_base_eur_t", -1),
    ("el_alt_kwh_per_t", -1),
    ("other_alt_eur_t", -1),
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
    assert mh779_valida(**d)["valido"] is False


@pytest.mark.parametrize("campo,valore", [
    ("p_t_anno", 0), ("p_t_anno", -3),
    ("gas_gj_per_t", -1),
    ("p_gas_eur_gj", -1),
    ("el_base_kwh_per_t", -1),
    ("p_el_eur_mwh", -1),
    ("other_base_eur_t", -1),
    ("el_alt_kwh_per_t", -1),
    ("other_alt_eur_t", -1),
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
        mh779_calcola(**d)


def test_df_tabella_valori_demo_selezionati():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Produzione fusa (t/anno)"] == 5000.0
    assert mappa["Costo base per tonnellata (EUR/t)"] == pytest.approx(
        347.0)


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
    return ["mh" + "77" + "8", "st" + "77" + "8",
            "tab" + "77" + "8"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w780_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w780_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab779:")


def test_registry_chain_tail_and_count():
    """Registry della nuova tab: il frammento UI apre la tab
    numero 779 (la coda della catena termina con la nuova tab
    e il conteggio atteso delle tab e' 779)."""
    src = _leggi("w780_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 779
    assert src.count("with tab779:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w780_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w780_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st779_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert "key=f" not in src and "key = f" not in src
    assert "st.stop()" in src
    # guard degenere prima di KPI / grafico / tabella / CSV
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w780_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def779[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w780_ui.py")
        usate = set(re.findall(r'_def779\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 15
        assert usate <= set(mh779_demo().keys())
        assert usate == set(mh779_demo().keys())


def test_ui_chiavi_demo_coerenti():
    """Ogni _def779[...] letto dalla UI esiste nel dict demo:
    sweep anti-KeyError a render (lezione dello sweep chiavi demo vs UI)."""
    src = _leggi("w780_ui.py")
    usate = set(re.findall(r'_def779\["([^"]+)"\]', src))
    assert usate
    assert len(usate) == 15
    assert usate <= set(mh779_demo().keys())


def test_ui_riferisce_solo_helper_nuovi():
    src = _leggi("w780_ui.py")
    usati = set(re.findall(r"\b(mh\d+_\w+)\b", src))
    assert usati
    assert all(u.startswith("mh779_") for u in usati)
