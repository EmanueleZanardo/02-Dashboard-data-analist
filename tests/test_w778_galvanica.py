"""Test tab778 "Galvanica: zincatura
a caldo vs elettrolitica - quando
lo zinco freddo batte il bagno a
450 C?"
(File repo: tests/test_w778_galvanica.py,
contenuto pronto da scrivere in repo.)

Nuova tab tab778 (galvanica, file di
lavoro w779). Business case
deterministico di una galvanica:
si zincano P t/anno di acciaio;
baseline zincatura a caldo
(hot-dip, bagno ~450 C) con costo
per tonnellata C_hd_per_t =
zn_hd x p_zn + gas_hd x p_gas +
el_hd / 1000 x p_el + other_hd
EUR/t (el_hd in kWh/t: 1 MWh =
1000 kWh); alternativa zincatura
elettrolitica con costo per
tonnellata C_el_per_t = zn_el x
p_zn + el_el / 1000 x p_el +
other_el EUR/t; costi annui C_base
= C_hd_per_t x P, C_el_var =
C_el_per_t x P, C_alt = C_el_var
+ O&M; risparmio = C_base - C_alt
EUR/anno; CO2 base = gas_hd / 3,6
x P x f_gas + el_hd / 1000 x P x
f_el t/anno (gas in GJ/t: 1 MWh =
3,6 GJ; fattori in tCO2/MWh);
CO2 elettrolitica = el_el / 1000
x P x f_el t/anno (niente gas:
nessun bagno a 450 C da tenere
caldo); CO2 evitata = CO2 base -
CO2 elettrolitica t/anno, PUO'
ESSERE NEGATIVA in questa tab
(elettricita' sporca, o elettricita'
elettrolitica alta: l'elettrolitica
puo' emettere piu' della baseline):
NON e' una guard, NON e' un
degenere, NON monetizzata; CRF =
r (1 + r)^n / ((1 + r)^n - 1) con
r = WACC come frazione, r = 0 ->
1/n, SOLO nel LCO, MAI nei flussi;
LCO base = C_hd_per_t EUR/t; LCO
alt = (CAPEX x CRF + O&M) / P +
C_el_per_t EUR/t (il CAPEX entra
solo annuizzato col CRF);
breakeven prezzo elettricita'
p_el* = (C_hd_nonel - C_el_nonel)
/ ((el_el - el_hd) / 1000) EUR/MWh,
None se denominatore <= 0
(l'elettrolitica non consuma piu'
elettricita' della baseline) e
None se numeratore < 0 (a prezzo
elettrico zero l'elettrolitica e'
gia' piu' cara e il divario cresce
con p_el); breakeven prezzo zinco
p_zn* = (C_hd_per_t -
C_el_non_zn) / zn_el EUR/kg, il
prezzo zinco che l'elettrolitica
puo' sopportare a costo a caldo
corrente, None se zn_el <= 0 e
None se numeratore < 0; entrambi
i pareggi, quando esistono, sono
TETTI (ceiling): il breakeven
elettrico e' un tetto sul prezzo
elettricita' (il risparmio CALA
con p_el, l'elettrolitica consuma
piu' elettricita' della baseline)
e il breakeven zinco e' un tetto
per il prezzo zinco
dell'elettrolitica a costo a caldo
corrente; i pareggi sono sui costi
variabili e NON includono l'O&M:
al pareggio esatto il risparmio e'
-O&M, non zero; flussi [-CAPEX,
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
questa tab confronta SOLO zincatura
a caldo (hot-dip) contro zincatura
elettrolitica per tonnellata di
acciaio zincato, NON
sherardizzazione, NON zincatura a
spruzzo, NON inox.

Demo calcolata eseguendo
demo_calcoli() e ricontrollata con
un ricalcolo indipendente da zero
(riga per riga): produzione zincata
20.000 t/anno, zincatura a caldo
con zinco 60 kg/t a 2,80 EUR/kg,
gas 2,0 GJ/t a 20 EUR/GJ,
elettricita' 60 kWh/t a 160
EUR/MWh, altri costi 25 EUR/t;
zincatura elettrolitica con zinco
18 kg/t a 2,80 EUR/kg, elettricita'
320 kWh/t, altri costi 120 EUR/t;
O&M annuo 300.000 EUR/anno, CAPEX
1.500.000 EUR, fattore gas 0,20
tCO2/MWh, fattore elettricita'
0,25 tCO2/MWh, WACC 6 %, vita 15
anni, tolleranza MARGINALE 10 %
di C_base.

- c_hd_per_t = 242.6
- c_el_per_t = 221.6
- c_hd_nonel_per_t = 233.0
- c_el_nonel_per_t = 170.39999999999998
- c_el_non_zn_per_t = 171.2
- el_hd_mwh_anno = 1200.0
- el_el_mwh_anno = 6400.0
- gas_mwh_anno = 11111.111111111111
- c_base_eur_anno = 4852000.0
- c_el_var_eur_anno = 4432000.0
- c_alt_eur_anno = 4732000.0
- risparmio_eur_anno = 120000.0
- co2_base_t_anno = 2522.222222222222
- co2_el_t_anno = 1600.0
- co2_evitata_t_anno = 922.2222222222222
- crf = 0.10296276395531265
- lco_base_eur_t = 242.6
- lco_alt_eur_t = 244.32220729664843
- van = -334530.1214710822
- tir = 2.3706630960697876
- payback = 13
- breakeven_el_eur_mwh = 240.76923076923086
- breakeven_zn_eur_kg = 3.966666666666667
- verdetto = 'MARGINALE'

Scomposizione: costo a caldo = 60 x
2,80 = 168 di zinco + 2,0 x 20 =
40 di gas + 60 / 1000 x 160 = 9,60
di elettricita' + 25 altri = 242,60
EUR/t; costo elettrolitico = 18 x
2,80 = 50,40 di zinco + 320 / 1000
x 160 = 51,20 di elettricita' + 120
altri = 221,60 EUR/t; costo base =
242,60 x 20.000 = 4.852.000
EUR/anno; costo variabile
elettrolitico = 221,60 x 20.000 =
4.432.000 EUR/anno; costo
alternativo = 4.432.000 + 300.000 =
4.732.000 EUR/anno; risparmio =
4.852.000 - 4.732.000 = 120.000
EUR/anno; CO2 base = 2,0 x 20.000 /
3,6 x 0,20 = 2.222,22 di gas + 60 /
1000 x 20.000 x 0,25 = 300 di
elettrica = 2.522,22 t/anno; CO2
elettrolitica = 320 / 1000 x 20.000
x 0,25 = 1.600 t/anno; CO2 evitata =
2.522,22 - 1.600 = 922,22 t/anno;
CRF al 6 % per 15 anni =
0,1029627640; LCO base 242,60
EUR/t; LCO alt = (1.500.000 x
0,1029627640 + 300.000) / 20.000 +
221,60 = 22,722207 + 221,60 =
244,322207 EUR/t; flussi: anno 0
-1.500.000, anni 1-15 risparmio
120.000 (piatti); VAN -1.500.000 +
120.000 x 9,712248 (annuita' 15
anni al 6 %) = -334.530,12 EUR;
TIR 2,37 %; payback 13 anni (il
cumulato all'anno 12 e' -60.000
EUR, all'anno 13 e' 60.000 EUR,
gia' >= 0); breakeven elettricita'
(233,00 - 170,40) / ((320 - 60) /
1000) = 62,60 / 0,26 = 240,77
EUR/MWh (TETTO: sotto di esso
l'elettrolitica vince sui costi
variabili, sopra perde);
breakeven zinco (242,60 - 171,20)
/ 18 = 71,40 / 18 = 3,97 EUR/kg
(TETTO a costo a caldo corrente:
171,20 + 18 x 3,97 = 242,60);
verdetto MARGINALE perche' il
risparmio 120.000 resta entro la
tolleranza del 10 % di C_base
(485.200 EUR/anno): il verdetto e'
sul risparmio, non sulla VAN (che
pure qui e' negativa, ma piccola).
NOTA: il CRF entra SOLO nel LCO di
questa tab: nei flussi il CAPEX
entra intero all'anno 0, mai
annuizzato.
NOTA 2: in questa tab il risparmio
nullo o negativo NON e' degenere:
con prezzo elettricita' 300
EUR/MWh (sopra il tetto 240,77) il
caso e' calcolabile (valid=True,
flussi pieni), NON_CONVIENTE con
VAN -7.405.047,38 EUR e payback
None, non un errore: -608.000 di
risparmio negativo supera la soglia
del 10 % di C_base (502.000 a quel
prezzo).
NOTA 3: la CO2 evitata PUO' essere
negativa in questa tab (non e' una
guard): con fattore elettricita'
1,00 la CO2 base e' 3.422,22
t/anno e l'elettrolitica 6.400
t/anno, quindi l'evitata e'
-2.977,78 t/anno, mentre il
verdetto resta MARGINALE (stessa
economia: i fattori non toccano
i costi).
NOTA 4: i pareggi sono TETTI, non
pavimenti, e sono sui costi
variabili, NON sul risparmio: al
pareggio elettrico esatto
(240,77 EUR/MWh) i costi per
tonnellata si eguagliano ma il
risparmio e' -300.000 EUR/anno,
cioe' solo l'O&M. Il breakeven
elettrico e' None con elettricita'
elettrolitica 60 kWh/t (denominatore
nullo: l'elettrolitica non consuma
piu' elettricita' della baseline).
Il breakeven zinco e' None con
zinco elettrolitico nullo, e vale
come identita' a costo a caldo
corrente: 171,20 + 18 x 3,97 =
242,60. Attenzione: il prezzo zinco
e' comune ai due processi, quindi a
prezzo zinco comune il risparmio
CRESCE con p_zn (60 contro 18
kg/t): il tetto zinco va letto a
costo a caldo corrente, non come
soglia oltre la quale il caso
peggiora a prezzo comune.
NOTA 5: il verdetto MARGINALE del
demo non e' un errore: con
tolleranza 0 % lo stesso caso
diventa CONVIENTE (risparmio
positivo, soglia nulla); con zinco
5,00 EUR/kg diventa CONVIENTE
(risparmio 1.968.000, VAN
17.613.706,01, payback 1); con
zinco 2,00 EUR/kg diventa
NON_CONVIENTE (risparmio -552.000,
VAN -6.861.161,44).
NOTA 6: il payback usa il cumulato
>= 0 (regola >= del brief): con
CAPEX nullo il payback e' 0 (non
1); con flussi [-100, 50, 50] il
payback e' 2 (il cumulato all'anno
2 e' zero, e zero basta); con CAPEX
1.440.000 EUR il payback e' 12
(divisione esatta 1.440.000 /
120.000).
NOTA 7: i valori demo sono stati
ricalcolati da zero con un calcolo
indipendente: il ricalcolo esatto
(senza arrotondamenti intermedi)
da' costo a caldo 242,60, costo
elettrolitico 221,60, costo base
4.852.000, costo variabile
elettrolitico 4.432.000, costo
alternativo 4.732.000, risparmio
120.000, CO2 base 2.522,22,
elettrolitica 1.600, evitata
922,22, CRF 0,1029627640, LCO base
242,60, LCO alt 244,322207, VAN
-334.530,12, TIR 2,37 %, payback
13, breakeven elettricita' 240,77
(tetto), breakeven zinco 3,97
(tetto a costo a caldo corrente),
verdetto MARGINALE: i file usano i
valori esatti.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w779_helpers import (
    demo_calcoli,
    mh778_breakeven_el,
    mh778_breakeven_zn,
    mh778_c_alt,
    mh778_c_base,
    mh778_c_el_non_zn,
    mh778_c_el_nonel,
    mh778_c_el_per_t,
    mh778_c_el_var,
    mh778_c_hd_nonel,
    mh778_c_hd_per_t,
    mh778_calcola,
    mh778_co2_base,
    mh778_co2_el,
    mh778_co2_evitata,
    mh778_crf,
    mh778_csv,
    mh778_demo,
    mh778_flussi,
    mh778_int_pos,
    mh778_lco_alt,
    mh778_lco_base,
    mh778_num,
    mh778_nneg,
    mh778_payback,
    mh778_pct_tolleranza,
    mh778_pct_wacc,
    mh778_pos,
    mh778_risparmio,
    mh778_tir,
    mh778_valida,
    mh778_van,
    mh778_verdetto,
)

# Costanti demo a piena precisione (per la validazione
# _DEMO contro demo_calcoli() con tolleranza relativa
# < 1e-9: vedi test_demo_costanti_vs_demo_calcoli).
_DEMO = {
    "c_hd_per_t": 242.6,
    "c_el_per_t": 221.6,
    "c_hd_nonel_per_t": 233.0,
    "c_el_nonel_per_t": 170.39999999999998,
    "c_el_non_zn_per_t": 171.2,
    "el_hd_mwh_anno": 1200.0,
    "el_el_mwh_anno": 6400.0,
    "gas_mwh_anno": 11111.111111111111,
    "c_base_eur_anno": 4852000.0,
    "c_el_var_eur_anno": 4432000.0,
    "c_alt_eur_anno": 4732000.0,
    "risparmio_eur_anno": 120000.0,
    "co2_base_t_anno": 2522.222222222222,
    "co2_el_t_anno": 1600.0,
    "co2_evitata_t_anno": 922.2222222222222,
    "crf": 0.10296276395531265,
    "lco_base_eur_t": 242.6,
    "lco_alt_eur_t": 244.32220729664843,
    "van": -334530.1214710822,
    "tir": 2.3706630960697876,
    "breakeven_el_eur_mwh": 240.76923076923086,
    "breakeven_zn_eur_kg": 3.966666666666667,
}


def _demo_kwargs():
    return dict(mh778_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh778_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh778_num(3, "x") == 3.0
    assert mh778_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh778_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh778_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh778_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh778_pos(0, "x")
    with pytest.raises(ValueError):
        mh778_pos(-1, "x")
    assert mh778_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh778_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh778_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh778_int_pos(0, "x")


def test_pct_wacc_limiti():
    assert mh778_pct_wacc(0, "x") == 0.0
    assert mh778_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh778_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh778_pct_tolleranza(0, "x") == 0.0
    assert mh778_pct_tolleranza(100, "x") == 100.0
    assert mh778_pct_tolleranza(10.0, "x") == 10.0
    with pytest.raises(ValueError):
        mh778_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh778_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_c_hd_per_t_scomposizione():
    assert mh778_c_hd_per_t(60, 2.80, 2.0, 20, 60, 160,
                             25) == pytest.approx(242.6)
    assert mh778_c_hd_per_t(0, 2.80, 0, 20, 0, 160,
                             0) == pytest.approx(0.0)
    assert mh778_c_hd_per_t(60, 2.80, 2.0, 20, 60, 0,
                             25) == pytest.approx(233.0)
    with pytest.raises(ValueError):
        mh778_c_hd_per_t(-1, 2.80, 2.0, 20, 60, 160, 25)
    with pytest.raises(ValueError):
        mh778_c_hd_per_t(60, -1, 2.0, 20, 60, 160, 25)


def test_c_el_per_t_scomposizione():
    assert mh778_c_el_per_t(18, 2.80, 320, 160,
                             120) == pytest.approx(221.6)
    assert mh778_c_el_per_t(18, 5.0, 320, 160,
                             120) == pytest.approx(261.2)
    assert mh778_c_el_per_t(18, 2.0, 320, 160,
                             120) == pytest.approx(207.2)
    assert mh778_c_el_per_t(0, 2.80, 320, 160,
                             120) == pytest.approx(171.2)
    with pytest.raises(ValueError):
        mh778_c_el_per_t(18, -1, 320, 160, 120)
    with pytest.raises(ValueError):
        mh778_c_el_per_t(18, 2.80, 320, 160, -1)


def test_c_nonel_e_non_zn():
    assert mh778_c_hd_nonel(242.6, 60, 160) == pytest.approx(233.0)
    assert mh778_c_el_nonel(221.6, 320, 160) == pytest.approx(170.4)
    assert mh778_c_el_non_zn(221.6, 18,
                             2.80) == pytest.approx(171.2)
    assert mh778_c_hd_nonel(242.6, 60, 0) == pytest.approx(242.6)
    with pytest.raises(ValueError):
        mh778_c_hd_nonel(242.6, -1, 160)


def test_c_base_c_el_var_c_alt():
    assert mh778_c_base(242.6, 20000) == pytest.approx(4852000.0)
    assert mh778_c_el_var(221.6, 20000) == pytest.approx(
        4432000.0)
    assert mh778_c_alt(4432000.0, 300000) == pytest.approx(
        4732000.0)
    with pytest.raises(ValueError):
        mh778_c_base(242.6, 0)
    with pytest.raises(ValueError):
        mh778_c_alt(4432000.0, -1)


def test_co2_base_el_evitata():
    assert mh778_co2_base(2.0, 20000, 60, 0.20,
                          0.25) == pytest.approx(2522.222222222222)
    assert mh778_co2_el(320, 20000,
                        0.25) == pytest.approx(1600.0)
    assert mh778_co2_el(320, 20000,
                        0) == pytest.approx(0.0)
    assert mh778_co2_base(0, 20000, 60, 0.20,
                          0.25) == pytest.approx(300.0)
    assert mh778_co2_evitata(2522.222222222222,
                             1600.0) == pytest.approx(
        922.2222222222222)
    assert mh778_co2_evitata(100.0, 150.0) == pytest.approx(-50.0)
    with pytest.raises(ValueError):
        mh778_co2_base(2.0, 20000, 60, -0.10, 0.25)


def test_co2_evitata_puo_essere_negativa_via_calcola():
    """Differenza chiave di questa tab: via
    mh778_calcola la CO2 evitata PUO' essere
    negativa (fattore elettricita' alto)."""
    bc = _variante(f_el_t_per_mwh=1.0)
    assert bc["co2_base_t_anno"] == pytest.approx(3422.222222222222)
    assert bc["co2_el_t_anno"] == pytest.approx(6400.0)
    assert bc["co2_evitata_t_anno"] == pytest.approx(-2977.777777777778)
    assert bc["verdetto"] == "MARGINALE"
    assert bc["valid"] is True


def test_co2_formula_componenti():
    """CO2 base = gas x f_gas + elettricita' a caldo x f_el,
    CO2 elettrolitica = elettricita' elettrolitica x f_el,
    con le conversioni kWh->MWh e GJ->MWh."""
    for bc in (demo_calcoli(),
               _variante(f_el_t_per_mwh=1.0),
               _variante(el_el_kwh_per_t=60)):
        atteso_base = (bc["gas_mwh_anno"] * bc["f_gas_t_per_mwh"]
                       + bc["el_hd_mwh_anno"] * bc["f_el_t_per_mwh"])
        assert bc["co2_base_t_anno"] == pytest.approx(atteso_base)
        atteso_el = (bc["el_el_mwh_anno"] * bc["f_el_t_per_mwh"])
        assert bc["co2_el_t_anno"] == pytest.approx(atteso_el)


def test_risparmio_segno():
    assert mh778_risparmio(4852000.0, 4732000.0) == \
        pytest.approx(120000.0)
    assert mh778_risparmio(4852000.0, 4852000.0) == 0.0
    assert mh778_risparmio(5020000.0, 5628000.0) == \
        pytest.approx(-608000.0)


def test_crf_solo_lco():
    assert mh778_crf(6.0, 15) == pytest.approx(0.10296276395531265)
    assert mh778_crf(0.0, 15) == pytest.approx(1.0 / 15.0)
    assert mh778_crf(6.0, 20) == pytest.approx(0.0871845569768514)
    with pytest.raises(ValueError):
        mh778_crf(50.1, 15)
    with pytest.raises(ValueError):
        mh778_crf(6.0, 0)


def test_lco():
    assert mh778_lco_base(4852000.0, 20000) == pytest.approx(242.6)
    assert mh778_lco_alt(1500000, 0.10296276395531265, 300000,
                         221.6, 20000) == pytest.approx(
        244.32220729664843)
    assert mh778_lco_base(4852000.0, 0) is None
    assert mh778_lco_alt(1500000, 0.10296276395531265, 300000,
                         221.6, 0) is None
    assert mh778_lco_alt(1500000, 0.10296276395531265, 300000,
                         221.6, -5) is None
    # Il CAPEX entra nel LCO solo annuizzato: con CAPEX nullo
    # il LCO alt e' (O&M / P) + C_el_per_t.
    assert mh778_lco_alt(0, 0.10296276395531265, 300000,
                         221.6, 20000) == pytest.approx(236.6)


def test_crf_mai_nei_flussi():
    """Il CRF entra SOLO nel LCO: i flussi usano il
    CAPEX intero all'anno 0 e la VAN dai flussi non
    dipende dal CRF (cambiando il WACC cambia la VAN
    per lo sconto, non per il CRF)."""
    bc = demo_calcoli()
    assert bc["flussi"][0] == -1500000
    assert bc["flussi"][1:] == [120000.0] * 15
    assert bc["van"] == pytest.approx(mh778_van(bc["flussi"], 6.0))
    bc0 = _variante(wacc_pct=0)
    assert bc0["van"] == pytest.approx(sum(bc0["flussi"]))
    assert bc0["crf"] == pytest.approx(1.0 / 15.0)
    assert bc0["lco_alt_eur_t"] == pytest.approx(241.6)


def test_breakeven_el_demo_e_varianti():
    # Demo: (233,00 - 170,40) / ((320 - 60) / 1000) = 240,77.
    assert mh778_breakeven_el(233.0, 170.4, 320,
                              60) == pytest.approx(240.76923076923086)
    # A zinco 5,00: nonel a caldo 365,00, nonel elettrolitica
    # 210,00, (365,00 - 210,00) / 0,26 = 596,15.
    assert mh778_breakeven_el(365.0, 210.0, 320,
                              60) == pytest.approx(596.1538461538462)
    # Numeratore zero: pareggio zero, valido.
    assert mh778_breakeven_el(233.0, 233.0, 320,
                              60) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh778_breakeven_el(233.0, 170.4, -1, 60)


def test_breakeven_el_none_casi():
    # Denominatore <= 0: el_el uguale o sotto el_hd.
    assert mh778_breakeven_el(233.0, 170.4, 60, 60) is None
    assert mh778_breakeven_el(233.0, 170.4, 50, 60) is None
    # Numeratore < 0: costo elettrolitico senza elettricita'
    # sopra il costo a caldo senza elettricita'.
    assert mh778_breakeven_el(233.0, 300.0, 320, 60) is None


def test_breakeven_zn_demo_e_varianti():
    # Demo: (242,60 - 171,20) / 18 = 3,9666667.
    assert mh778_breakeven_zn(242.6, 171.2,
                              18) == pytest.approx(
        3.966666666666667)
    # Numeratore zero: pareggio zero, valido.
    assert mh778_breakeven_zn(242.6, 242.6,
                              18) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh778_breakeven_zn(242.6, 171.2, -1)


def test_breakeven_zn_none_casi():
    # Zinco elettrolitico <= 0: nessun prezzo da calcolare.
    assert mh778_breakeven_zn(242.6, 171.2, 0) is None
    # Numeratore < 0: a prezzo zinco zero l'elettrolitica e'
    # gia' piu' cara del costo a caldo corrente.
    assert mh778_breakeven_zn(100.0, 171.2, 18) is None


def test_breakeven_verifica_pareggio():
    """Al prezzo elettrico di pareggio i costi per tonnellata
    si eguagliano: C_el_per_t(p*) = C_hd_per_t(p*).
    Il risparmio invece e' -O&M, non zero (i pareggi non
    includono l'O&M). Per lo zinco vale l'identita' a costo
    a caldo corrente: C_el_non_zn + zn_el x be_zn = C_hd_per_t."""
    bc = _variante(p_el_eur_mwh=240.76923076923086)
    assert bc["c_hd_per_t"] == pytest.approx(bc["c_el_per_t"])
    assert bc["risparmio_eur_anno"] == pytest.approx(-300000.0,
                                                     abs=1e-3)
    demo = demo_calcoli()
    assert (demo["c_el_non_zn_per_t"]
            + demo["zn_el_kg_per_t"]
            * demo["breakeven_zn_eur_kg"]) == pytest.approx(
        demo["c_hd_per_t"])


def test_pareggi_tetti_non_pavimenti():
    """Sotto il tetto elettrico l'elettrolitica vince sui costi
    variabili, sopra perde: il costo elettrolitico scende sotto
    il costo a caldo sotto il tetto e sale sopra oltre il tetto."""
    be_el = demo_calcoli()["breakeven_el_eur_mwh"]
    assert _variante(p_el_eur_mwh=be_el - 10)[
        "c_el_per_t"] < _variante(p_el_eur_mwh=be_el - 10)[
        "c_hd_per_t"]
    assert _variante(p_el_eur_mwh=be_el + 10)[
        "c_el_per_t"] > _variante(p_el_eur_mwh=be_el + 10)[
        "c_hd_per_t"]


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh778_flussi(1500000, 120000.0, 15)
    assert len(fl) == 16
    assert fl[0] == -1500000
    assert all(f == 120000.0 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = demo_calcoli()
    assert bc["van"] == pytest.approx(-334530.1214710822)
    assert mh778_van([-1500000] + [120000.0] * 15,
                     0) == pytest.approx(300000.0)
    assert mh778_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = demo_calcoli()
    assert bc["tir"] == pytest.approx(2.3706630960697876)
    assert mh778_tir([-1500000] + [120000.0] * 15) == \
        pytest.approx(0.023706630960697876)
    tir = mh778_tir([-1500000] + [120000.0] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate(
                  [-1500000] + [120000.0] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    """Payback con cumulato >= 0: il cumulato nullo basta."""
    assert mh778_payback([-1500000] + [120000.0] * 15) == 13
    assert mh778_payback([-1500000] + [-1000.0] * 15) is None
    assert mh778_payback([0] + [120000.0] * 15) == 0
    assert mh778_payback([-100] + [50] * 2) == 2
    assert mh778_payback([-1440000.0] +
                         [120000.0] * 12) == 12


def test_verdetto():
    assert mh778_verdetto(1968000.0, 4852000.0,
                          10.0) == "CONVIENTE"
    assert mh778_verdetto(120000.0, 4852000.0,
                          10.0) == "MARGINALE"
    assert mh778_verdetto(0.0, 4852000.0, 10.0) == "MARGINALE"
    assert mh778_verdetto(-485200.0, 4852000.0,
                          10.0) == "MARGINALE"
    assert mh778_verdetto(-485201.0, 4852000.0,
                          10.0) == "NON_CONVIENTE"
    assert mh778_verdetto(-552000.0, 4852000.0,
                          10.0) == "NON_CONVIENTE"
    assert mh778_verdetto(120000.0, 4852000.0,
                          0.0) == "CONVIENTE"
    assert mh778_verdetto(-100.0, 4852000.0,
                          0.0) == "NON_CONVIENTE"
    assert mh778_verdetto(None, 4852000.0,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh778_verdetto(float("nan"), 4852000.0, 10.0)
    with pytest.raises(ValueError):
        mh778_verdetto(100.0, -1, 10.0)
    with pytest.raises(ValueError):
        mh778_verdetto(100.0, 4852000.0, 100.1)


def test_valida_demo_ok():
    v = mh778_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("p_t_anno", "20000"),
                       ("p_t_anno", float("nan")),
                       ("p_t_anno", float("inf")),
                       ("p_t_anno", True),
                       ("p_zn_eur_kg", None),
                       ("zn_hd_kg_per_t", "60")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh778_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("p_t_anno", 0),
                          ("p_t_anno", -1),
                          ("zn_hd_kg_per_t", -1),
                          ("p_zn_eur_kg", -1),
                          ("gas_hd_gj_per_t", -1),
                          ("p_gas_eur_gj", -1),
                          ("el_hd_kwh_per_t", -1),
                          ("p_el_eur_mwh", -1),
                          ("other_hd_eur_t", -1),
                          ("zn_el_kg_per_t", -1),
                          ("el_el_kwh_per_t", -1),
                          ("other_el_eur_t", -1),
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
        assert mh778_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"zn_hd_kg_per_t": 0,
              "p_zn_eur_kg": 0,
              "gas_hd_gj_per_t": 0,
              "p_gas_eur_gj": 0,
              "el_hd_kwh_per_t": 0,
              "p_el_eur_mwh": 0,
              "other_hd_eur_t": 0,
              "zn_el_kg_per_t": 0,
              "el_el_kwh_per_t": 0,
              "other_el_eur_t": 0,
              "om_eur_anno": 0,
              "capex_eur": 0,
              "f_gas_t_per_mwh": 0,
              "f_el_t_per_mwh": 0,
              "wacc_pct": 0,
              "tolleranza_pct": 0})
    assert mh778_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    assert mh778_valida(**d)["valido"] is True


def test_valida_non_controlla_risparmio_calcola_neppure():
    """La validazione input NON controlla il risparmio
    (e' un esito, non un range) e in questa tab
    nemmeno mh778_calcola lo controlla: con prezzo
    elettricita' 300 EUR/MWh (sopra il tetto 240,77)
    il caso resta CALCOLABILE."""
    d = _demo_kwargs()
    d["p_el_eur_mwh"] = 300
    assert mh778_valida(**d)["valido"] is True
    bc = _variante(p_el_eur_mwh=300)
    assert bc["valid"] is True
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["flussi"]
    assert bc["payback"] is None


def test_demo_dict():
    d = mh778_demo()
    assert d["p_t_anno"] == 20000
    assert d["zn_hd_kg_per_t"] == 60
    assert d["p_zn_eur_kg"] == 2.80
    assert d["gas_hd_gj_per_t"] == 2.0
    assert d["p_gas_eur_gj"] == 20
    assert d["el_hd_kwh_per_t"] == 60
    assert d["p_el_eur_mwh"] == 160
    assert d["other_hd_eur_t"] == 25
    assert d["zn_el_kg_per_t"] == 18
    assert d["el_el_kwh_per_t"] == 320
    assert d["other_el_eur_t"] == 120
    assert d["om_eur_anno"] == 300000
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
    assert bc["payback"] == 13
    assert bc["verdetto"] == "MARGINALE"
    assert bc["valid"] is True


def test_demo_calcoli_fisica():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["c_hd_per_t"] == pytest.approx(242.6)
    assert bc["c_el_per_t"] == pytest.approx(221.6)
    assert bc["el_hd_mwh_anno"] == pytest.approx(1200.0)
    assert bc["el_el_mwh_anno"] == pytest.approx(6400.0)
    assert bc["gas_mwh_anno"] == pytest.approx(11111.111111111111)
    assert bc["co2_evitata_t_anno"] == pytest.approx(922.2222222222222)


def test_demo_calcoli_economia():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(4852000.0)
    assert bc["c_el_var_eur_anno"] == pytest.approx(4432000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(4732000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(120000.0)
    assert bc["breakeven_el_eur_mwh"] == pytest.approx(240.76923076923086)
    assert bc["breakeven_zn_eur_kg"] == pytest.approx(
        3.966666666666667)


def test_demo_calcoli_finanza():
    bc = demo_calcoli()
    assert bc["crf"] == pytest.approx(0.10296276395531265)
    assert bc["lco_base_eur_t"] == pytest.approx(242.6)
    assert bc["lco_alt_eur_t"] == pytest.approx(244.32220729664843)
    assert bc["van"] == pytest.approx(-334530.1214710822)
    assert bc["tir"] == pytest.approx(2.3706630960697876)
    assert bc["payback"] == 13
    assert bc["verdetto"] == "MARGINALE"


def test_demo_flussi_e_cumulato():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -1500000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(120000.0)
               for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -1500000
    assert righe.iloc[12]["Cumulato (EUR)"] == pytest.approx(-60000.0)
    assert righe.iloc[13]["Cumulato (EUR)"] == pytest.approx(60000.0)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(
        300000.0)
    assert righe.iloc[15]["Flusso (EUR/anno)"] == pytest.approx(
        120000.0)


def test_demo_tabella_righe():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Produzione zincata (t/anno)"] == pytest.approx(
        20000.0)
    assert mappa["Costo a caldo per tonnellata (EUR/t)"] == pytest.approx(
        242.6)
    assert mappa["Costo elettrolitico per tonnellata (EUR/t)"] == pytest.approx(
        221.6)
    assert mappa["Elettricita' elettrolitica (MWh/anno)"] == pytest.approx(
        6400.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(
        4732000.0)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(120000.0)
    assert mappa["Payback (anni)"] == 13
    assert mappa["Verdetto"] == "MARGINALE"
    assert mappa["Breakeven prezzo elettricita' (EUR/MWh)"] == \
        pytest.approx(240.76923076923086)
    assert mappa["Breakeven prezzo zinco (EUR/kg)"] == \
        pytest.approx(3.966666666666667)


def test_demo_coerenza_interna():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["c_hd_per_t"] * bc["p_t_anno"] == \
        pytest.approx(bc["c_base_eur_anno"])
    assert bc["c_el_per_t"] * bc["p_t_anno"] == \
        pytest.approx(bc["c_el_var_eur_anno"])
    assert bc["co2_base_t_anno"] - bc["co2_el_t_anno"] == \
        pytest.approx(bc["co2_evitata_t_anno"])
    assert bc["c_base_eur_anno"] / bc["p_t_anno"] == \
        pytest.approx(bc["lco_base_eur_t"])
    assert (bc["capex_eur"] * bc["crf"] + bc["om_eur_anno"]) / \
        bc["p_t_anno"] + bc["c_el_per_t"] == \
        pytest.approx(bc["lco_alt_eur_t"])
    assert bc["c_hd_nonel_per_t"] + \
        bc["el_hd_kwh_per_t"] / 1000.0 * bc["p_el_eur_mwh"] == \
        pytest.approx(bc["c_hd_per_t"])
    assert bc["c_el_non_zn_per_t"] + \
        bc["zn_el_kg_per_t"] * bc["p_zn_eur_kg"] == \
        pytest.approx(bc["c_el_per_t"])


def test_demo_contro_riconteggio_indipendente():
    p, znh, pz = 20000, 60, 2.80
    gas, pg, elh, pel, oh = 2.0, 20, 60, 160, 25
    zne, ele, oe, om, cx = 18, 320, 120, 300000, 1500000
    fg, fel, wacc, vita = 0.20, 0.25, 6.0, 15
    ch = znh * pz + gas * pg + elh / 1000.0 * pel + oh
    ce = zne * pz + ele / 1000.0 * pel + oe
    cbase = ch * p
    cav = ce * p
    ca = cav + om
    risp = cbase - ca
    co2b = gas / 3.6 * p * fg + elh / 1000.0 * p * fel
    co2a = ele / 1000.0 * p * fel
    r = wacc / 100.0
    crf = r * (1 + r) ** vita / ((1 + r) ** vita - 1.0)
    lco_b = ch
    lco_a = (cx * crf + om) / p + ce
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    be_el = (ch - elh / 1000.0 * pel
             - (ce - ele / 1000.0 * pel)) / ((ele - elh) / 1000.0)
    be_zn = (ch - (ce - zne * pz)) / zne
    bc = demo_calcoli()
    assert bc["c_hd_per_t"] == pytest.approx(ch)
    assert bc["c_el_per_t"] == pytest.approx(ce)
    assert bc["c_base_eur_anno"] == pytest.approx(cbase)
    assert bc["c_el_var_eur_anno"] == pytest.approx(cav)
    assert bc["c_alt_eur_anno"] == pytest.approx(ca)
    assert bc["risparmio_eur_anno"] == pytest.approx(risp)
    assert bc["co2_base_t_anno"] == pytest.approx(co2b)
    assert bc["co2_el_t_anno"] == pytest.approx(co2a)
    assert bc["crf"] == pytest.approx(crf)
    assert bc["lco_base_eur_t"] == pytest.approx(lco_b)
    assert bc["lco_alt_eur_t"] == pytest.approx(lco_a)
    assert bc["van"] == pytest.approx(van)
    assert bc["breakeven_el_eur_mwh"] == pytest.approx(be_el)
    assert bc["breakeven_zn_eur_kg"] == pytest.approx(be_zn)


# ---------------------------------------------------------------- varianti
def test_demo_marginale_non_conviente():
    """Il demo e' MARGINALE, non CONVIENTE: il
    verdetto e' sul risparmio, e 120.000 resta
    entro la tolleranza del 10 % di C_base
    (485.200), anche se il payback e' 13 anni
    e la VAN e' negativa ma piccola."""
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] < 0.0
    assert bc["payback"] == 13
    assert bc["verdetto"] == "MARGINALE"


def test_variante_zinco_alto_conviente():
    """Zinco 5,00 EUR/kg: risparmio 1.968.000,
    VAN 17.613.706,01, payback 1, CONVIENTE."""
    bc = _variante(p_zn_eur_kg=5.0)
    assert bc["valid"] is True
    assert bc["c_el_per_t"] == pytest.approx(261.2)
    assert bc["c_el_var_eur_anno"] == pytest.approx(5224000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(5524000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(1968000.0)
    assert bc["van"] == pytest.approx(17613706.007874254)
    assert bc["payback"] == 1
    assert bc["lco_alt_eur_t"] == pytest.approx(283.9222072966484)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_zinco_basso_non_conviente():
    """Zinco 2,00 EUR/kg: risparmio -552.000,
    VAN -6.861.161,44, payback mai,
    NON_CONVIENTE."""
    bc = _variante(p_zn_eur_kg=2.0)
    assert bc["valid"] is True
    assert bc["c_el_per_t"] == pytest.approx(207.2)
    assert bc["risparmio_eur_anno"] == pytest.approx(-552000.0)
    assert bc["van"] == pytest.approx(-6861161.441233023)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_pareggio_el_esatto():
    """Al tetto elettrico esatto (240,77 EUR/MWh) i
    costi per tonnellata si eguagliano ma il
    risparmio e' -300.000 (solo l'O&M): VAN
    -4.413.674,70, TIR None, payback mai,
    verdetto MARGINALE."""
    bc = _variante(p_el_eur_mwh=240.76923076923086)
    assert bc["c_hd_per_t"] == pytest.approx(bc["c_el_per_t"])
    assert bc["risparmio_eur_anno"] == pytest.approx(-300000.0,
                                                     abs=1e-3)
    assert bc["van"] == pytest.approx(-4413674.696322295)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "MARGINALE"


def test_variante_sopra_tetto_el():
    """Prezzo elettricita' 300 EUR/MWh (sopra il
    tetto 240,77): risparmio -608.000, VAN
    -7.405.047,38, TIR None, payback mai,
    verdetto NON_CONVIENTE (oltre la soglia
    del 10 % di C_base a quel prezzo)."""
    bc = _variante(p_el_eur_mwh=300)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(-608000.0)
    assert bc["van"] == pytest.approx(-7405047.384546517)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_tolleranza_zero_demo_conviente():
    """Con tolleranza 0 % la fascia MARGINALE e'
    nulla: lo stesso demo diventa CONVIENTE
    (risparmio positivo, soglia zero)."""
    bc = _variante(tolleranza_pct=0)
    assert bc["risparmio_eur_anno"] == pytest.approx(120000.0)
    assert bc["van"] == pytest.approx(-334530.1214710822)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    """Payback regola >=: con CAPEX nullo il payback e' 0,
    non 1 (all'anno 0 il cumulato e' gia' zero)."""
    bc = _variante(capex_eur=0)
    assert bc["capex_eur"] == 0
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(1165469.878528918)
    assert bc["lco_alt_eur_t"] == pytest.approx(236.6)
    assert bc["verdetto"] == "MARGINALE"


def test_variante_capex_divisione_esatta_payback():
    """CAPEX 1.440.000 EUR: divisione esatta
    1.440.000 / 120.000 = 12 anni, payback 12
    (regola >=: il cumulato nullo basta)."""
    bc = _variante(capex_eur=1440000)
    assert bc["payback"] == 12
    assert bc["van"] == pytest.approx(-274530.1214710822)
    assert bc["tir"] == pytest.approx(2.9283950062936666)
    assert bc["verdetto"] == "MARGINALE"


def test_variante_wacc_zero():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(300000.0)
    assert bc["lco_alt_eur_t"] == pytest.approx(241.6)
    assert bc["verdetto"] == "MARGINALE"


def test_variante_vita_diversa():
    bc = _variante(vita_anni=10)
    assert len(bc["flussi"]) == 11
    assert bc["van"] == pytest.approx(-616789.5538302368)
    assert bc["tir"] == pytest.approx(-3.8641905262609884)
    assert bc["payback"] is None
    assert bc["verdetto"] == "MARGINALE"


def test_variante_om_alto():
    """O&M 600.000 EUR/anno: risparmio -180.000,
    VAN -3.248.204,82, payback mai,
    verdetto MARGINALE."""
    bc = _variante(om_eur_anno=600000)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(-180000.0)
    assert bc["van"] == pytest.approx(-3248204.8177933777)
    assert bc["payback"] is None
    assert bc["lco_alt_eur_t"] == pytest.approx(259.32220729664846)
    assert bc["verdetto"] == "MARGINALE"


def test_variante_breakeven_el_none_denominatore():
    """Elettricita' elettrolitica uguale alla baseline
    (60 kWh/t): breakeven elettrico None,
    caso calcolabile CONVIENTE."""
    bc = _variante(el_el_kwh_per_t=60)
    assert bc["valid"] is True
    assert bc["breakeven_el_eur_mwh"] is None
    assert bc["risparmio_eur_anno"] == pytest.approx(952000.0)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_breakeven_zn_none_zinco_nullo():
    """Zinco elettrolitico nullo: breakeven zinco None,
    caso calcolabile CONVIENTE."""
    bc = _variante(zn_el_kg_per_t=0)
    assert bc["valid"] is True
    assert bc["breakeven_zn_eur_kg"] is None
    assert bc["c_el_per_t"] == pytest.approx(171.2)
    assert bc["risparmio_eur_anno"] == pytest.approx(1128000.0)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_breakeven_zn_none_numeratore():
    """Costo a caldo nullo (zinco, gas, elettricita' e
    altri a caldo a zero): costo a caldo 0 sotto il
    costo elettrolitico senza zinco 171,20:
    breakeven zinco None (numeratore negativo)."""
    bc = _variante(zn_hd_kg_per_t=0, gas_hd_gj_per_t=0,
                   el_hd_kwh_per_t=0, other_hd_eur_t=0)
    assert bc["valid"] is True
    assert bc["breakeven_zn_eur_kg"] is None


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
    assert mh778_verdetto(None, 4852000.0, 10.0) == "NON_CALCOLABILE"
    assert demo_calcoli()["verdetto"] != "NON_CALCOLABILE"


def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"p_t_anno": 0}, {"p_t_anno": -1},
               {"zn_hd_kg_per_t": -1},
               {"p_zn_eur_kg": -1},
               {"gas_hd_gj_per_t": -1},
               {"p_gas_eur_gj": -1},
               {"el_hd_kwh_per_t": -1},
               {"p_el_eur_mwh": -1},
               {"other_hd_eur_t": -1},
               {"zn_el_kg_per_t": -1},
               {"el_el_kwh_per_t": -1},
               {"other_el_eur_t": -1},
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
        assert mh778_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"p_t_anno": "20000"},
               {"p_t_anno": float("nan")},
               {"p_zn_eur_kg": float("inf")},
               {"capex_eur": True},
               {"zn_hd_kg_per_t": "60"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh778_valida(**d)["valido"] is False


def test_risparmio_negativo_non_degenere():
    """Differenza chiave: risparmio nullo o
    negativo resta calcolabile, con flussi pieni e
    VAN negativa; cosi' anche la CO2 evitata
    negativa resta calcolabile, e cosi' i
    breakeven None restano calcolabili."""
    for kw in ({"p_el_eur_mwh": 300},
               {"p_zn_eur_kg": 2.0}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["verdetto"] in ("NON_CONVIENTE", "MARGINALE")
        assert bc["flussi"]
    bc = _variante(f_el_t_per_mwh=1.0)
    assert bc["co2_evitata_t_anno"] < 0.0
    assert bc["valid"] is True
    bc2 = _variante(el_el_kwh_per_t=60)
    assert bc2["breakeven_el_eur_mwh"] is None
    assert bc2["valid"] is True


def test_co2_evitata_segno_funzione_pura():
    assert mh778_co2_evitata(100.0, 150.0) == pytest.approx(-50.0)


def test_verdetto_non_calcolabile_solo_risparmio_none():
    assert mh778_verdetto(None, 4852000.0, 10.0) == "NON_CALCOLABILE"
    assert demo_calcoli()["verdetto"] != "NON_CALCOLABILE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = demo_calcoli()
    testo = mh778_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert "c_hd_per_t;242.6" in testo
    assert "c_el_per_t;221.6" in testo
    assert "c_base_eur_anno;4852000.0" in testo
    assert "c_el_var_eur_anno;4432000.0" in testo
    assert "verdetto;MARGINALE" in testo
    assert "breakeven_el_eur_mwh" in testo
    assert "breakeven_zn_eur_kg" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = demo_calcoli()
    testo = mh778_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"c_el_per_t;{bc['c_el_per_t']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = demo_calcoli()
    testo = mh778_csv(bc, _demo_kwargs())
    for chiave in _demo_kwargs():
        assert f"{chiave};" in testo


def test_monotonia_prezzo_el_decrescente():
    # Il risparmio CALA con p_el (l'elettrolitica consuma piu'
    # elettricita' della baseline): pendenza
    # -5.200 EUR/anno per EUR/MWh (20.000 t x
    # (320 - 60) / 1000 = 5.200 MWh/anno).
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_el_eur_mwh=170)["risparmio_eur_anno"]
    basso = _variante(p_el_eur_mwh=150)["risparmio_eur_anno"]
    assert basso > base > alto
    assert base - alto == pytest.approx(52000.0)
    assert basso - base == pytest.approx(52000.0)


def test_monotonia_prezzo_zn_crescente():
    # Il risparmio CRESCE con p_zn a prezzo comune (la baseline
    # consuma piu' zinco dell'alternativa): pendenza
    # +840.000 EUR/anno per EUR/kg (20.000 t x
    # (60 - 18) kg/t = 840.000 kg/anno).
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_zn_eur_kg=3.80)["risparmio_eur_anno"]
    basso = _variante(p_zn_eur_kg=1.80)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(840000.0)
    assert base - basso == pytest.approx(840000.0)


def test_monotonia_elettricita_el():
    # Piu' elettricita' elettrolitica, piu' cara l'alternativa:
    # +10 kWh/t a 160 EUR/MWh = +1,60 EUR/t =
    # -32.000 EUR/anno di risparmio.
    base = demo_calcoli()["risparmio_eur_anno"]
    assert _variante(el_el_kwh_per_t=330)[
        "risparmio_eur_anno"] == pytest.approx(base - 32000.0)
    assert _variante(el_el_kwh_per_t=310)[
        "risparmio_eur_anno"] == pytest.approx(base + 32000.0)


def test_demo_deterministica_due_chiamate():
    a = demo_calcoli()
    b = demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh778_demo().keys()) == {
        "p_t_anno",
        "zn_hd_kg_per_t", "p_zn_eur_kg",
        "gas_hd_gj_per_t", "p_gas_eur_gj",
        "el_hd_kwh_per_t", "p_el_eur_mwh",
        "other_hd_eur_t",
        "zn_el_kg_per_t",
        "el_el_kwh_per_t", "other_el_eur_t",
        "om_eur_anno", "capex_eur",
        "f_gas_t_per_mwh", "f_el_t_per_mwh",
        "wacc_pct", "vita_anni", "tolleranza_pct"}


@pytest.mark.parametrize("p_zn,atteso", [
    (2.80, 221.6),
    (5.0, 261.2),
    (2.0, 207.2),
])
def test_c_el_per_t_parametrizzato(p_zn, atteso):
    assert mh778_c_el_per_t(18, p_zn, 320, 160,
                             120) == pytest.approx(atteso)


@pytest.mark.parametrize("campo,valore", [
    ("p_t_anno", 0), ("p_t_anno", -3),
    ("zn_hd_kg_per_t", -1),
    ("p_zn_eur_kg", -1),
    ("gas_hd_gj_per_t", -1),
    ("p_gas_eur_gj", -1),
    ("el_hd_kwh_per_t", -1),
    ("p_el_eur_mwh", -1),
    ("other_hd_eur_t", -1),
    ("zn_el_kg_per_t", -1),
    ("el_el_kwh_per_t", -1),
    ("other_el_eur_t", -1),
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
    assert mh778_valida(**d)["valido"] is False


@pytest.mark.parametrize("campo,valore", [
    ("p_t_anno", 0), ("p_t_anno", -3),
    ("zn_hd_kg_per_t", -1),
    ("p_zn_eur_kg", -1),
    ("gas_hd_gj_per_t", -1),
    ("p_gas_eur_gj", -1),
    ("el_hd_kwh_per_t", -1),
    ("p_el_eur_mwh", -1),
    ("other_hd_eur_t", -1),
    ("zn_el_kg_per_t", -1),
    ("el_el_kwh_per_t", -1),
    ("other_el_eur_t", -1),
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
        mh778_calcola(**d)


def test_df_tabella_valori_demo_selezionati():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Produzione zincata (t/anno)"] == 20000.0
    assert mappa["Costo a caldo per tonnellata (EUR/t)"] == pytest.approx(
        242.6)


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
    return ["mh" + "77" + "7", "st" + "77" + "7",
            "tab" + "77" + "7"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w779_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w779_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab778:")


def test_registry_chain_tail_and_count():
    """Registry della nuova tab: il frammento UI apre la tab
    numero 778 (la coda della catena termina con la nuova tab
    e il conteggio atteso delle tab e' 778)."""
    src = _leggi("w779_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 778
    assert src.count("with tab778:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w779_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w779_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st778_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert "key=f" not in src and "key = f" not in src
    assert "st.stop()" in src
    # guard degenere prima di KPI / grafico / tabella / CSV
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w779_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def778[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w779_ui.py")
        usate = set(re.findall(r'_def778\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 18
        assert usate <= set(mh778_demo().keys())
        assert usate == set(mh778_demo().keys())


def test_ui_chiavi_demo_coerenti():
    """Ogni _def778[...] letto dalla UI esiste nel dict demo:
    sweep anti-KeyError a render (lezione dello sweep chiavi demo vs UI)."""
    src = _leggi("w779_ui.py")
    usate = set(re.findall(r'_def778\["([^"]+)"\]', src))
    assert usate
    assert len(usate) == 18
    assert usate <= set(mh778_demo().keys())


def test_ui_riferisce_solo_helper_nuovi():
    src = _leggi("w779_ui.py")
    usati = set(re.findall(r"\b(mh\d+_\w+)\b", src))
    assert usati
    assert all(u.startswith("mh778_") for u in usati)
