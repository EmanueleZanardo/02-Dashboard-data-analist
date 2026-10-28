"""Test tab775 "Mangimificio: cuocere i
mangime con recupero calore dai aria esausta
batte il essiccatore a gas?"
(File repo: tests/test_w775_mangimificio.py,
contenuto pronto da scrivere in repo.)

Nuova tab tab775 (mangimificio, file di
lavoro w775). Business case
deterministico di un essiccatore per
mangimificio: produzione P t/anno di
mangime; calore utile Q_term = P x
q_th / 3,6 MWh/anno (q_th in GJ/t:
1 MWh = 3,6 GJ, conversione esatta);
consumo elettrico E_base = P x e_spec
/ 1000 MWh/anno (e_spec in kWh/t,
identico nei due casi: il recupero
non cambia il consumo elettrico
specifico); combustibile baseline
fuel_base = Q_term / eta_essiccatore
MWh/anno (eta come frazione); calore
recuperato Q_rec = quota_rec x Q_term
MWh/anno (quota come frazione,
scambio termico dai aria esausta per
preriscaldare l'aria di essiccazione,
senza combustibile in piu');
combustibile alternativo fuel_alt =
(Q_term - Q_rec) / eta_essiccatore MWh/anno
(sempre >= 0 per costruzione se
quota_rec <= 1); costo base C_base =
fuel_base x p_fuel + E_base x p_el
EUR/anno; costo variabile alternativo
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
specifico <= 0, rendimento essiccatore
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
questa tab fa mangime in un essiccatore
per mangimificio (aria esausta ->
preriscaldo dell'aria di essiccazione),
non pastificio, non molino, non laterizi,
non cemento.

Demo calcolata eseguendo
demo_calcoli() e ricontrollata con
un ricalcolo indipendente da zero
(riga per riga): produzione mangime
60.000 t/anno, consumo termico
specifico 0,9 GJ/t, rendimento essiccatore
85 %, quota recupero 35 %, consumo
elettrico specifico 50 kWh/t, prezzo
combustibile 45 EUR/MWh, prezzo
elettricita' 180 EUR/MWh, O&M annuo
150.000 EUR/anno, CAPEX 1.200.000
EUR, fattore combustibile 0,30
tCO2/MWh, fattore elettricita' 0,25
tCO2/MWh, WACC 5 %, vita 20 anni,
tolleranza MARGINALE 10 % del CAPEX.

- q_term_mwh_anno = 15000.0
- e_base_mwh_anno = 3000.0
- fuel_base_mwh_anno = 17647.058823529413
- q_rec_mwh_anno = 5250.0
- fuel_alt_mwh_anno = 11470.588235294117
- c_base_eur_anno = 1334117.6470588236
- c_alt_var_eur_anno = 1056176.4705882352
- c_alt_eur_anno = 1206176.4705882352
- co2_base_t_anno = 6044.117647058823
- co2_alt_t_anno = 4191.176470588235
- risparmio_eur_anno = 127941.17647058843
- co2_evitata_t_anno = 1852.9411764705883
- crf = 0.08024258719069129
- lco_base_eur_t = 22.23529411764706
- lco_alt_eur_t = 21.70779292028441
- van = 394429.85264850024
- tir = 8.622803645823122
- payback = 10
- prezzo_pareggio_eur_mwh = 24.28571428571428
- verdetto = 'CONVIENTE'

Scomposizione: calore utile =
60.000 x 0,9 / 3,6 = 15.000
MWh/anno; consumo elettrico =
60.000 x 50 / 1000 = 3.000
MWh/anno; combustibile baseline =
15.000 / 0,85 = 17.647,058824
MWh/anno; calore recuperato = 0,35
x 15.000 = 5.250
MWh/anno; combustibile alternativo =
(15.000 - 5.250) / 0,85 =
11.470,588235 MWh/anno; costo base
= 17.647,058824 x 45 + 3.000 x 180
= 794.117,65 + 540.000 =
1.334.117,65 EUR/anno; costo variabile
alternativo = 11.470,588235 x 45 +
3.000 x 180 = 516.176,47 +
540.000 = 1.056.176,47 EUR/anno;
costo alternativo = 1.056.176,47 +
150.000 = 1.206.176,47 EUR/anno;
risparmio = 1.334.117,65 - 1.206.176,47
= 127.941,18 EUR/anno; CO2 base =
17.647,058824 x 0,30 + 3.000 x
0,25 = 5.294,12 + 750 =
6.044,12 t/anno; CO2 alt =
11.470,588235 x 0,30 + 3.000 x
0,25 = 3.441,18 + 750 = 4.191,18
t/anno; CO2 evitata = 6.044,12
- 4.191,18 = 1.852,94 t/anno;
CRF al 5 % per 20 anni =
0,0802425872; LCO base 1.334.117,65 /
60.000 = 22,235294 EUR/t; LCO alt =
(1.200.000 x 0,0802425872 +
150.000) / 60.000 + 1.056.176,47 /
60.000 = 4,104851 + 17,602941 = 21,707792
EUR/t; flussi: anno 0 -1.200.000,
anni 1-20 risparmio 127.941,18
(piatti); VAN -1.200.000 +
127.941,18 x 12,462210 (annuita' 20
anni al 5 %) = 394.429,85 EUR;
TIR 8,62 %; payback 10 anni (il
cumulato all'anno 9 e' -48.529,41
EUR, all'anno 10 e' 79.411,76 EUR,
gia' >= 0); prezzo combustibile di
pareggio 150.000 / (17.647,058824 -
11.470,588235) = 24,29 EUR/MWh
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
(sotto il pareggio 24,29) il caso e'
calcolabile (valid=True, flussi
pieni), NON_CONVIENTE con VAN
-2.684.469,17 EUR e payback None,
non un errore.
NOTA 3: la CO2 evitata ha segno
sempre >= 0 in questa tab (non e'
una guard, e' un'identita'):
(17.647,058824 - 11.470,588235) x
0,30 = 1.852,94 t/anno; con
fattore combustibile zero l'evitata
e' zero (3.000 = 3.000 t/anno nei
due casi, solo elettricita'), e il
fattore elettrico non la cambia mai
perche' l'elettricita' e' identica
nei due casi e si elide.
NOTA 4: il prezzo combustibile di
pareggio e' None con quota recupero
zero (denominatore nullo: nessun
combustibile risparmiato, nessun
pareggio su p_fuel). Al pareggio
esatto (24,29 EUR/MWh) il risparmio
e' zero: il caso resta calcolabile
con VAN -1.200.000 EUR (solo il
CAPEX, senza risparmi) e verdetto
NON_CONVIENTE.
NOTA 5: la quota di recupero scala
il risparmio in modo lineare: con
quota 50 % il calore recuperato e'
7.500 MWh/anno, il risparmio
247.058,82 EUR/anno, la VAN
1.878.899,03 EUR e il payback 5
anni; con quota 100 % il combustibile
alternativo va a zero, il risparmio
a 644.117,65 EUR/anno, la VAN a
6.827.129,60 EUR e il payback a 2
anni (ma il calore utile residuo
nullo e' un limite teorico: un essiccatore
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
1.700.000 EUR la VAN e'
-105.570,15 EUR, entro 170.000
EUR (10 % di 1.700.000), quindi
MARGINALE; con tolleranza 0 % lo
stesso caso e' NON_CONVIENTE.
NOTA 8: i valori demo sono stati
ricalcolati da zero con un calcolo
indipendente: il ricalcolo esatto
(senza arrotondamenti intermedi)
da' calore utile 15.000,
elettrico 3.000, combustibile base
17.647,058824, recuperato 5.250,
combustibile alt 11.470,588235,
costo base 1.334.117,65, costo
variabile alt 1.056.176,47, costo alt
1.206.176,47, risparmio 127.941,18, CO2
base 6.044,12, CO2 alt 4.191,18,
evitata 1.852,94, CRF
0,0802425872, LCO base 22,235294, LCO
alt 21,707792, VAN 394.429,85,
TIR 8,62 %, payback 10 e pareggio
24,29: i file usano i valori esatti.
Le stime del brief (Q_term 15.000,
fuel_base 17.647,06, Q_rec 5.250,
fuel_alt 11.470,59, C_base
1.334.117,65, C_alt 1.206.176,47,
risparmio 127.941,18, CO2 base
6.044,12, alt 4.191,18, evitata
1.852,94, LCO base 22,24, LCO alt
21,71, pareggio 24,29, payback anno
10) sono tutte confermate dal
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

from w776_helpers import (
    demo_calcoli,
    mh775_c_alt,
    mh775_c_alt_var,
    mh775_c_base,
    mh775_calcola,
    mh775_co2_alt,
    mh775_co2_base,
    mh775_co2_evitata,
    mh775_crf,
    mh775_csv,
    mh775_demo,
    mh775_e_base,
    mh775_flussi,
    mh775_fuel_alt,
    mh775_fuel_base,
    mh775_int_pos,
    mh775_lco_alt,
    mh775_lco_base,
    mh775_num,
    mh775_nneg,
    mh775_payback,
    mh775_pct_0_100,
    mh775_pct_0_100_escl0,
    mh775_pct_tolleranza,
    mh775_pct_wacc,
    mh775_pos,
    mh775_prezzo_pareggio,
    mh775_q_rec,
    mh775_q_term,
    mh775_risparmio,
    mh775_tir,
    mh775_valida,
    mh775_van,
    mh775_verdetto,
)

# Costanti demo a piena precisione (per la validazione
# _DEMO contro demo_calcoli() con tolleranza relativa
# < 1e-9: vedi test_demo_costanti_vs_demo_calcoli).
_DEMO = {
    "q_term_mwh_anno": 15000.0,
    "e_base_mwh_anno": 3000.0,
    "fuel_base_mwh_anno": 17647.058823529413,
    "q_rec_mwh_anno": 5250.0,
    "fuel_alt_mwh_anno": 11470.588235294117,
    "c_base_eur_anno": 1334117.6470588236,
    "c_alt_var_eur_anno": 1056176.4705882352,
    "c_alt_eur_anno": 1206176.4705882352,
    "co2_base_t_anno": 6044.117647058823,
    "co2_alt_t_anno": 4191.176470588235,
    "risparmio_eur_anno": 127941.17647058843,
    "co2_evitata_t_anno": 1852.9411764705883,
    "crf": 0.08024258719069129,
    "lco_base_eur_t": 22.23529411764706,
    "lco_alt_eur_t": 21.70779292028441,
    "van": 394429.85264850024,
    "tir": 8.622803645823122,
    "prezzo_pareggio_eur_mwh": 24.28571428571428,
}


def _demo_kwargs():
    return dict(mh775_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh775_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh775_num(3, "x") == 3.0
    assert mh775_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh775_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh775_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh775_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh775_pos(0, "x")
    with pytest.raises(ValueError):
        mh775_pos(-1, "x")
    assert mh775_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh775_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh775_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh775_int_pos(0, "x")


def test_pct_wacc_limiti():
    assert mh775_pct_wacc(0, "x") == 0.0
    assert mh775_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh775_pct_wacc(50.1, "x")


def test_pct_0_100_escl0_limiti():
    assert mh775_pct_0_100_escl0(100, "x") == 100.0
    assert mh775_pct_0_100_escl0(65.0, "x") == 65.0
    with pytest.raises(ValueError):
        mh775_pct_0_100_escl0(0, "x")
    with pytest.raises(ValueError):
        mh775_pct_0_100_escl0(100.1, "x")
    with pytest.raises(ValueError):
        mh775_pct_0_100_escl0(-1, "x")


def test_pct_0_100_limiti():
    assert mh775_pct_0_100(0, "x") == 0.0
    assert mh775_pct_0_100(100, "x") == 100.0
    assert mh775_pct_0_100(50.0, "x") == 50.0
    with pytest.raises(ValueError):
        mh775_pct_0_100(-0.1, "x")
    with pytest.raises(ValueError):
        mh775_pct_0_100(100.1, "x")


def test_pct_tolleranza_limiti():
    assert mh775_pct_tolleranza(0, "x") == 0.0
    assert mh775_pct_tolleranza(100, "x") == 100.0
    assert mh775_pct_tolleranza(10.0, "x") == 10.0
    with pytest.raises(ValueError):
        mh775_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh775_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_q_term_e_e_base():
    assert mh775_q_term(80000, 2.5) == pytest.approx(55555.555555555555)
    assert mh775_q_term(80000, 1.25) == pytest.approx(27777.777777777777)
    assert mh775_q_term(80000, 2.5) == pytest.approx(55555.555555555555)
    assert mh775_q_term(80000, 1.25) == pytest.approx(27777.777777777777)
    assert mh775_e_base(80000, 60) == pytest.approx(4800.0)
    assert mh775_e_base(80000, 30) == pytest.approx(2400.0)
    assert mh775_e_base(80000, 60) == pytest.approx(4800.0)
    assert mh775_e_base(80000, 30) == pytest.approx(2400.0)
    with pytest.raises(ValueError):
        mh775_q_term(80000, 0)
    with pytest.raises(ValueError):
        mh775_q_term(0, 2.5)
    with pytest.raises(ValueError):
        mh775_e_base(80000, 0)
    with pytest.raises(ValueError):
        mh775_e_base(80000, -1)


def test_fuel_base_q_rec_fuel_alt():
    assert mh775_fuel_base(55555.555555555555, 0.85) == pytest.approx(
        65359.47712418301)
    assert mh775_fuel_base(55555.555555555555, 1.0) == pytest.approx(
        55555.555555555555)
    assert mh775_q_rec(55555.555555555555, 0.30) == pytest.approx(
        16666.666666666664)
    assert mh775_q_rec(55555.555555555555, 0.0) == 0.0
    assert mh775_q_rec(55555.555555555555, 1.0) == pytest.approx(
        55555.555555555555)
    assert mh775_fuel_alt(55555.555555555555, 16666.666666666664,
                          0.85) == pytest.approx(45751.63398692811)
    assert mh775_fuel_alt(55555.555555555555, 55555.555555555555,
                          0.85) == 0.0
    assert mh775_fuel_alt(55555.555555555555, 0.0,
                          0.85) == pytest.approx(65359.47712418301)
    with pytest.raises(ValueError):
        mh775_q_rec(55555.555555555555, 1.1)
    with pytest.raises(ValueError):
        mh775_q_rec(55555.555555555555, -0.1)
    with pytest.raises(ValueError):
        mh775_fuel_alt(55555.555555555555, 55556.0, 0.85)
    with pytest.raises(ValueError):
        mh775_fuel_base(55555.555555555555, 0.0)
    with pytest.raises(ValueError):
        mh775_fuel_base(55555.555555555555, 1.1)


def test_bilancio_energetico_demo_e_varianti():
    """Bilancio esatto: Q_rec + fuel_alt x eta_essiccatore = Q_term,
    nel demo e nelle varianti (il calore utile si conserva:
    recuperato piu' residuo da combustibile)."""
    for bc in (demo_calcoli(),
               _variante(quota_rec_pct=0.0),
               _variante(quota_rec_pct=50.0),
               _variante(quota_rec_pct=100.0),
               _variante(eta_essiccatore_pct=80.0)):
        eta = bc["eta_essiccatore_pct"] / 100.0
        assert bc["q_rec_mwh_anno"] + \
            bc["fuel_alt_mwh_anno"] * eta == pytest.approx(
                bc["q_term_mwh_anno"], rel=1e-9)


def test_c_base_c_alt_var_c_alt():
    assert mh775_c_base(65359.47712418301, 4800.0, 45,
                        180) == pytest.approx(3805176.4705882357)
    assert mh775_c_base(55555.555555555555, 4800.0, 45,
                        180) == pytest.approx(3364000.0)
    assert mh775_c_alt_var(45751.63398692811, 4800.0, 45,
                           180) == pytest.approx(2922823.529411765)
    assert mh775_c_alt_var(0.0, 4800.0, 45,
                           180) == pytest.approx(864000.0)
    assert mh775_c_alt(2922823.529411765, 300000) == pytest.approx(
        3222823.529411765)
    with pytest.raises(ValueError):
        mh775_c_base(65359.47712418301, 4800.0, -1, 180)
    with pytest.raises(ValueError):
        mh775_c_alt_var(45751.63398692811, 4800.0, 45, -1)
    with pytest.raises(ValueError):
        mh775_c_alt(2922823.529411765, -1)


def test_co2_base_alt_evitata():
    assert mh775_co2_base(65359.47712418301, 4800.0, 0.30,
                          0.25) == pytest.approx(20807.843137254902)
    assert mh775_co2_alt(45751.63398692811, 4800.0, 0.30,
                         0.25) == pytest.approx(14925.490196078432)
    assert mh775_co2_alt(0.0, 4800.0, 0.30,
                         0.25) == pytest.approx(1200.0)
    assert mh775_co2_evitata(20807.843137254902,
                             14925.490196078432) == pytest.approx(
        5882.35294117647)
    assert mh775_co2_evitata(100.0, 150.0) == pytest.approx(-50.0)
    with pytest.raises(ValueError):
        mh775_co2_base(65359.47712418301, 4800.0, -0.10, 0.25)


def test_co2_evitata_mai_negativa_via_calcola():
    """Identita' della tab: via mh775_calcola la CO2
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
    assert mh775_risparmio(3805176.4705882357, 3222823.529411765) == \
        pytest.approx(582352.9411764708)
    assert mh775_risparmio(3805176.4705882357, 3805176.4705882357) == 0.0
    assert mh775_risparmio(1190797.385620915, 1392758.1699346406) == \
        pytest.approx(-201960.78431372554)


def test_crf_solo_lco():
    assert mh775_crf(5.0, 20) == pytest.approx(0.08024258719069129)
    assert mh775_crf(0.0, 20) == pytest.approx(0.05)
    assert mh775_crf(5.0, 10) == pytest.approx(0.1295045749654566)
    with pytest.raises(ValueError):
        mh775_crf(50.1, 20)
    with pytest.raises(ValueError):
        mh775_crf(5.0, 0)


def test_lco():
    assert mh775_lco_base(3805176.4705882357, 80000) == pytest.approx(47.564705882352946)
    assert mh775_lco_alt(4000000, 0.08024258719069129, 300000,
                         2922823.529411765, 80000) == pytest.approx(
        44.297423477181624)
    assert mh775_lco_base(3805176.4705882357, 0) is None
    assert mh775_lco_alt(4000000, 0.08024258719069129, 300000,
                         2922823.529411765, 0) is None
    assert mh775_lco_alt(4000000, 0.08024258719069129, 300000,
                         2922823.529411765, -5) is None
    # Il CAPEX entra nel LCO solo annuizzato: con CAPEX nullo
    # il LCO alt e' (O&M + C_alt_var) / P = C_alt / P.
    assert mh775_lco_alt(0, 0.08024258719069129, 300000,
                         2922823.529411765, 80000) == pytest.approx(40.28529411764706)


def test_prezzo_pareggio_formula_zero_e_pavimento():
    assert mh775_prezzo_pareggio(
        300000, 65359.47712418301,
        45751.63398692811) == pytest.approx(15.3)
    assert mh775_prezzo_pareggio(
        300000, 65359.47712418301,
        65359.47712418301) is None
    assert mh775_prezzo_pareggio(
        600000, 65359.47712418301,
        45751.63398692811) == pytest.approx(30.6)
    with pytest.raises(ValueError):
        mh775_prezzo_pareggio(-1, 65359.47712418301,
                              45751.63398692811)


def test_prezzo_pareggio_verifica_pareggio():
    """Al prezzo di pareggio il risparmio si azzera:
    C_alt(p*) = C_base(p*)."""
    bc = demo_calcoli()
    par = bc["prezzo_pareggio_eur_mwh"]
    d = _demo_kwargs()
    d["prezzo_fuel_eur_mwh"] = par
    bc_par = mh775_calcola(**d)
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
    fl = mh775_flussi(4000000, 582352.9411764708, 20)
    assert len(fl) == 21
    assert fl[0] == -4000000
    assert all(f == 582352.9411764708 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = demo_calcoli()
    assert bc["van"] == pytest.approx(394429.85264850024)
    assert mh775_van([-1200000] + [127941.17647058843] * 20,
                     0) == pytest.approx(1358823.5294117685)
    assert mh775_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = demo_calcoli()
    assert bc["tir"] == pytest.approx(8.622803645823122)
    assert mh775_tir([-1200000] + [127941.17647058843] * 20) == \
        pytest.approx(0.08622803645823122)
    tir = mh775_tir([-1200000] + [127941.17647058843] * 20)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate(
                  [-1200000] + [127941.17647058843] * 20))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    """Payback con cumulato >= 0: il cumulato nullo basta."""
    assert mh775_payback([-4000000] + [582352.9411764708] * 20) == 7
    assert mh775_payback([-4000000] + [-1000.0] * 20) is None
    assert mh775_payback([0] + [582352.9411764708] * 20) == 0
    assert mh775_payback([-100] + [50] * 2) == 2
    assert mh775_payback([-1164705.8823529416] +
                         [582352.9411764708] * 2) == 2


def test_verdetto():
    assert mh775_verdetto(100.0, 4000000, 10.0) == "CONVIENTE"
    assert mh775_verdetto(0.0, 4000000, 10.0) == "NON_CONVIENTE"
    assert mh775_verdetto(-242595.15346200744, 7500000,
                          10.0) == "MARGINALE"
    assert mh775_verdetto(-242595.15346200744, 7500000,
                          0.0) == "NON_CONVIENTE"
    assert mh775_verdetto(-6516877.775061996, 4000000,
                          10.0) == "NON_CONVIENTE"
    assert mh775_verdetto(-100.0, 0, 10.0) == "NON_CONVIENTE"
    assert mh775_verdetto(None, 4000000, 10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh775_verdetto(float("nan"), 4000000, 10.0)
    with pytest.raises(ValueError):
        mh775_verdetto(100.0, -1, 10.0)
    with pytest.raises(ValueError):
        mh775_verdetto(100.0, 4000000, 100.1)


def test_valida_demo_ok():
    v = mh775_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("p_t_anno", "80000"),
                       ("p_t_anno", float("nan")),
                       ("p_t_anno", float("inf")),
                       ("p_t_anno", True),
                       ("prezzo_fuel_eur_mwh", None),
                       ("eta_essiccatore_pct", "90")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh775_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("p_t_anno", 0),
                          ("p_t_anno", -1),
                          ("q_th_gj_per_t", 0),
                          ("q_th_gj_per_t", -1),
                          ("eta_essiccatore_pct", 0),
                          ("eta_essiccatore_pct", 100.1),
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
        assert mh775_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"quota_rec_pct": 0,
              "eta_essiccatore_pct": 100,
              "prezzo_fuel_eur_mwh": 0,
              "prezzo_el_eur_mwh": 0,
              "f_fuel_t_per_mwh": 0,
              "f_el_t_per_mwh": 0,
              "om_eur_anno": 0,
              "capex_eur": 0, "wacc_pct": 0,
              "tolleranza_pct": 0})
    assert mh775_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    assert mh775_valida(**d)["valido"] is True


def test_valida_non_controlla_risparmio_calcola_neppure():
    """La validazione input NON controlla il risparmio
    (e' un esito, non un range) e in questa tab
    nemmeno mh775_calcola lo controlla: con prezzo
    combustibile 5 EUR/MWh (sotto il pareggio 24,29)
    il caso resta CALCOLABILE."""
    d = _demo_kwargs()
    d["prezzo_fuel_eur_mwh"] = 5
    assert mh775_valida(**d)["valido"] is True
    bc = _variante(prezzo_fuel_eur_mwh=5)
    assert bc["valid"] is True
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["flussi"]
    assert bc["payback"] is None


def test_demo_dict():
    d = mh775_demo()
    assert d["p_t_anno"] == 60000
    assert d["q_th_gj_per_t"] == 0.9
    assert d["eta_essiccatore_pct"] == 85.0
    assert d["quota_rec_pct"] == 35.0
    assert d["e_spec_kwh_per_t"] == 50
    assert d["prezzo_fuel_eur_mwh"] == 45
    assert d["prezzo_el_eur_mwh"] == 180
    assert d["om_eur_anno"] == 150000
    assert d["capex_eur"] == 1200000
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
    assert bc["payback"] == 10
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_demo_calcoli_fisica():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["q_term_mwh_anno"] == pytest.approx(15000.0)
    assert bc["e_base_mwh_anno"] == pytest.approx(3000.0)
    assert bc["fuel_base_mwh_anno"] == pytest.approx(17647.058823529413)
    assert bc["q_rec_mwh_anno"] == pytest.approx(5250.0)
    assert bc["fuel_alt_mwh_anno"] == pytest.approx(11470.588235294117)
    assert bc["co2_evitata_t_anno"] == pytest.approx(1852.9411764705883)


def test_demo_calcoli_economia():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(1334117.6470588236)
    assert bc["c_alt_var_eur_anno"] == pytest.approx(1056176.4705882352)
    assert bc["c_alt_eur_anno"] == pytest.approx(1206176.4705882352)
    assert bc["risparmio_eur_anno"] == pytest.approx(127941.17647058843)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(
        24.28571428571428)


def test_demo_calcoli_finanza():
    bc = demo_calcoli()
    assert bc["crf"] == pytest.approx(0.08024258719069129)
    assert bc["lco_base_eur_t"] == pytest.approx(22.23529411764706)
    assert bc["lco_alt_eur_t"] == pytest.approx(21.70779292028441)
    assert bc["van"] == pytest.approx(394429.85264850024)
    assert bc["tir"] == pytest.approx(8.622803645823122)
    assert bc["payback"] == 10
    assert bc["verdetto"] == "CONVIENTE"


def test_demo_flussi_e_cumulato():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -1200000
    assert len(bc["flussi"]) == 21
    assert all(f == pytest.approx(127941.17647058843)
               for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -1200000
    assert righe.iloc[9]["Cumulato (EUR)"] == pytest.approx(-48529.41176470416)
    assert righe.iloc[10]["Cumulato (EUR)"] == pytest.approx(79411.76470588427)
    assert righe.iloc[20]["Cumulato (EUR)"] == pytest.approx(1358823.5294117685)
    assert righe.iloc[20]["Flusso (EUR/anno)"] == pytest.approx(
        127941.17647058843)


def test_demo_tabella_righe():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Produzione mangime (t/anno)"] == pytest.approx(
        60000.0)
    assert mappa["Calore utile (MWh/anno)"] == pytest.approx(15000.0)
    assert mappa["Consumo elettrico (MWh/anno)"] == pytest.approx(
        3000.0)
    assert mappa["Calore recuperato (MWh/anno)"] == pytest.approx(
        5250.0)
    assert mappa["Combustibile alternativo (MWh/anno)"] == pytest.approx(
        11470.588235294117)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(
        1206176.4705882352)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(127941.17647058843)
    assert mappa["Payback (anni)"] == 10
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Prezzo combustibile di pareggio (EUR/MWh)"] == \
        pytest.approx(24.28571428571428)


def test_demo_coerenza_interna():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["q_rec_mwh_anno"] + \
        bc["fuel_alt_mwh_anno"] * bc["eta_essiccatore_pct"] / 100.0 == \
        pytest.approx(bc["q_term_mwh_anno"])
    assert bc["q_rec_mwh_anno"] == pytest.approx(
        bc["q_term_mwh_anno"] * bc["quota_rec_pct"] / 100.0)
    assert bc["fuel_base_mwh_anno"] == pytest.approx(
        bc["q_term_mwh_anno"] / (bc["eta_essiccatore_pct"] / 100.0))
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
    p, qsp, efor = 60000, 0.9, 85.0
    qrec, esp = 35.0, 50
    pf, pel, om, cx = 45, 180, 150000, 1200000
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
    assert bc["payback"] == 10
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_recupero_cinquanta():
    """Recupero al 50 % sul demo: Q_rec 7.500,
    fuel_alt 8.823,53, risparmio 247.058,82,
    VAN 1.878.899,03, payback 5."""
    bc = _variante(quota_rec_pct=50.0)
    assert bc["valid"] is True
    assert bc["q_rec_mwh_anno"] == pytest.approx(7500.0)
    assert bc["fuel_alt_mwh_anno"] == pytest.approx(8823.529411764706)
    assert bc["c_alt_eur_anno"] == pytest.approx(1087058.8235294118)
    assert bc["risparmio_eur_anno"] == pytest.approx(247058.8235294118)
    assert bc["van"] == pytest.approx(1878899.0258039958)
    assert bc["tir"] == pytest.approx(20.05621771723526)
    assert bc["payback"] == 5
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(
        17.0)
    assert bc["lco_alt_eur_t"] == pytest.approx(19.722498802637357)
    assert bc["co2_evitata_t_anno"] == pytest.approx(2647.0588235294117)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_recupero_cento():
    """Recupero al 100 % sul demo: fuel_alt zero
    (limite teorico), risparmio 644.117,65, VAN
    6.827.129,60, payback 2."""
    bc = _variante(quota_rec_pct=100.0)
    assert bc["valid"] is True
    assert bc["q_rec_mwh_anno"] == pytest.approx(15000.0)
    assert bc["fuel_alt_mwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(644117.6470588236)
    assert bc["van"] == pytest.approx(6827129.602988988)
    assert bc["payback"] == 2
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(
        8.5)
    assert bc["lco_alt_eur_t"] == pytest.approx(13.104851743813825)
    assert bc["co2_evitata_t_anno"] == pytest.approx(5294.117647058823)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_recupero_zero():
    """Quota recupero zero: nessun risparmio di
    combustibile, solo O&M in piu': risparmio
    -150.000, VAN -3.069.331,55, pareggio None,
    payback None."""
    bc = _variante(quota_rec_pct=0)
    assert bc["valid"] is True
    assert bc["q_rec_mwh_anno"] == 0.0
    assert bc["fuel_alt_mwh_anno"] == pytest.approx(
        bc["fuel_base_mwh_anno"])
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["risparmio_eur_anno"] == pytest.approx(-150000.0)
    assert bc["van"] == pytest.approx(-3069331.5513809975)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_marginale_capex_alto():
    """Fascia MARGINALE: CAPEX 1.700.000 EUR, VAN
    negativa entro la tolleranza del 10 % del
    CAPEX (170.000 EUR)."""
    bc = _variante(capex_eur=1700000)
    assert bc["valid"] is True
    assert bc["van"] == pytest.approx(-105570.14735150008)
    assert bc["tir"] == pytest.approx(4.256021537697445)
    assert bc["payback"] == 14
    assert bc["verdetto"] == "MARGINALE"
    bc0 = _variante(capex_eur=1700000, tolleranza_pct=0)
    assert bc0["verdetto"] == "NON_CONVIENTE"
    assert bc0["van"] == pytest.approx(-105570.14735150008)


def test_variante_non_conviente_prezzo_fuel_basso():
    """NON_CONVIENTE: prezzo combustibile 5 EUR/MWh,
    sotto il pareggio 24,29: risparmio negativo,
    VAN negativa oltre la tolleranza, payback mai,
    TIR None (flussi tutti negativi dopo l'anno 0)."""
    bc = _variante(prezzo_fuel_eur_mwh=5)
    assert bc["valid"] is True
    assert bc["c_base_eur_anno"] == pytest.approx(628235.2941176471)
    assert bc["c_alt_eur_anno"] == pytest.approx(747352.9411764706)
    assert bc["risparmio_eur_anno"] == pytest.approx(-119117.6470588235)
    assert bc["van"] == pytest.approx(-2684469.1731554978)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["flussi"]


def test_variante_prezzo_fuel_35_sopra_pareggio_ma_van_negativa():
    """Prezzo combustibile 35 EUR/MWh (sopra il pareggio
    24,29): il risparmio operativo e' positivo
    (66.176,47 EUR/anno) ma la VAN resta negativa
    (-375.294,90 EUR) perche' lo sconto al 5 % su 20
    anni non ripaga il CAPEX: il pareggio sui costi
    operativi NON basta per la VAN. Payback 19 anni,
    TIR 0,95 %."""
    bc = _variante(prezzo_fuel_eur_mwh=35)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(66176.47058823542)
    assert bc["van"] == pytest.approx(-375294.9038024999)
    assert bc["tir"] == pytest.approx(0.9518541250034186)
    assert bc["payback"] == 19
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_rendimento_basso():
    """Rendimento essiccatore 80 %: piu' combustibile in
    ingresso in entrambi i casi, ma piu' combustibile
    risparmiato in assoluto: risparmio 145.312,50,
    VAN 610.914,94, payback 9, pareggio 22,86."""
    bc = _variante(eta_essiccatore_pct=80.0)
    assert bc["valid"] is True
    assert bc["fuel_base_mwh_anno"] == pytest.approx(18750.0)
    assert bc["fuel_alt_mwh_anno"] == pytest.approx(12187.5)
    assert bc["risparmio_eur_anno"] == pytest.approx(145312.5)
    assert bc["van"] == pytest.approx(610914.9404003411)
    assert bc["payback"] == 9
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(22.857142857142858)
    assert bc["co2_evitata_t_anno"] == pytest.approx(1968.75)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(1358823.5294117685)
    assert bc["lco_alt_eur_t"] == pytest.approx(21.102941176470587)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    """Payback regola >=: con CAPEX nullo il payback e' 0,
    non 1 (all'anno 0 il cumulato e' gia' zero)."""
    bc = _variante(capex_eur=0)
    assert bc["capex_eur"] == 0
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(1594429.8526484994)
    assert bc["lco_alt_eur_t"] == pytest.approx(20.102941176470587)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_vita_diversa():
    bc = _variante(vita_anni=10)
    assert len(bc["flussi"]) == 11
    assert bc["van"] == pytest.approx(-212072.1487660593)
    assert bc["tir"] == pytest.approx(1.1823665450535232)
    assert bc["payback"] == 10
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_pareggio_esatto_risparmio_zero():
    """Al pareggio esatto il risparmio e' zero: il caso
    resta calcolabile con VAN -1.200.000 EUR (solo il
    CAPEX, senza risparmi) e verdetto NON_CONVIENTE."""
    bc = _variante(prezzo_fuel_eur_mwh=24.28571428571428)
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["van"] == pytest.approx(-1200000.0)
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
        _variante(eta_essiccatore_pct=0)
    assert mh775_verdetto(None, 4000000, 10.0) == "NON_CALCOLABILE"
    assert demo_calcoli()["verdetto"] != "NON_CALCOLABILE"


def test_degenere_guard_rendimento_quota_nulli():
    """Guard su rendimento e quota: rendimento essiccatore
    zero o sopra 100, quota recupero fuori [0, 100]
    sollevano ValueError."""
    for kw in ({"eta_essiccatore_pct": 0},
               {"eta_essiccatore_pct": 100.1},
               {"quota_rec_pct": -1},
               {"quota_rec_pct": 100.1}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh775_valida(**d)["valido"] is False


def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"p_t_anno": 0}, {"p_t_anno": -1},
               {"q_th_gj_per_t": 0},
               {"q_th_gj_per_t": -1},
               {"eta_essiccatore_pct": 0},
               {"eta_essiccatore_pct": 100.1},
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
        assert mh775_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"p_t_anno": "80000"},
               {"p_t_anno": float("nan")},
               {"prezzo_fuel_eur_mwh": float("inf")},
               {"capex_eur": True},
               {"eta_essiccatore_pct": "90"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh775_valida(**d)["valido"] is False


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
    assert mh775_co2_evitata(100.0, 150.0) == pytest.approx(-50.0)


def test_verdetto_non_calcolabile_solo_van_none():
    assert mh775_verdetto(None, 4000000, 10.0) == "NON_CALCOLABILE"
    assert demo_calcoli()["verdetto"] != "NON_CALCOLABILE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = demo_calcoli()
    testo = mh775_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert "q_term_mwh_anno;15000.0" in testo
    assert "e_base_mwh_anno;3000.0" in testo
    assert "fuel_base_mwh_anno;17647.058823529413" in testo
    assert "q_rec_mwh_anno;5250.0" in testo
    assert "fuel_alt_mwh_anno;11470.588235294117" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "prezzo_pareggio_eur_mwh" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = demo_calcoli()
    testo = mh775_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"q_rec_mwh_anno;{bc['q_rec_mwh_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = demo_calcoli()
    testo = mh775_csv(bc, _demo_kwargs())
    for chiave in _demo_kwargs():
        assert f"{chiave};" in testo


def test_monotonia_prezzo_fuel():
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(prezzo_fuel_eur_mwh=55)["risparmio_eur_anno"]
    basso = _variante(prezzo_fuel_eur_mwh=35)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(61764.70588235294)
    assert base - basso == pytest.approx(61764.70588235294)


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
    alto = _variante(quota_rec_pct=40)["risparmio_eur_anno"]
    basso = _variante(quota_rec_pct=15)["risparmio_eur_anno"]
    assert alto > base > basso


def test_demo_deterministica_due_chiamate():
    a = demo_calcoli()
    b = demo_calcoli()
    assert a["van"] == b["van"]
    assert a["flussi"] == b["flussi"]
    assert a["tir"] == b["tir"]


def test_demo_chiavi_attese():
    assert set(mh775_demo().keys()) == {
        "p_t_anno",
        "q_th_gj_per_t", "eta_essiccatore_pct",
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
    return ["mh" + "77" + "4", "st" + "77" + "4",
            "tab" + "77" + "4"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w776_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w776_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab775:")


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w776_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w776_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st775_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert "key=f" not in src and 'key = f' not in src
    assert "st.stop()" in src
    # guard degenere prima di KPI / grafico / tabella / CSV
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w776_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def775[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w776_ui.py")
        usate = set(re.findall(r'_def775\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 14
        assert usate == {
            "p_t_anno",
            "q_th_gj_per_t", "eta_essiccatore_pct",
            "quota_rec_pct", "e_spec_kwh_per_t",
            "prezzo_fuel_eur_mwh", "prezzo_el_eur_mwh",
            "om_eur_anno", "capex_eur",
            "f_fuel_t_per_mwh", "f_el_t_per_mwh",
            "wacc_pct", "vita_anni", "tolleranza_pct"}
        assert usate <= set(mh775_demo().keys())


def test_ui_chiavi_demo_coerenti():
    """Ogni _def775[...] letto dalla UI esiste nel dict demo:
    sweep anti-KeyError a render (lezione dello sweep chiavi demo vs UI)."""
    src = _leggi("w776_ui.py")
    usate = set(re.findall(r'_def775\["([^"]+)"\]', src))
    assert usate
    assert len(usate) == 14
    assert usate <= set(mh775_demo().keys())


def test_ui_riferisce_solo_helper_nuovi():
    src = _leggi("w776_ui.py")
    usati = set(re.findall(r'\b(mh\d+_\w+)\b', src))
    assert usati
    assert all(u.startswith("mh775_") for u in usati)


@pytest.mark.parametrize("e_spec,atteso", [
    (60, 4800.0),
    (30, 2400.0),
    (120, 9600.0),
])
def test_e_base_parametrizzato(e_spec, atteso):
    assert mh775_e_base(80000, e_spec) == pytest.approx(atteso)


@pytest.mark.parametrize("campo,valore", [
    ("p_t_anno", 0), ("p_t_anno", -3),
    ("q_th_gj_per_t", 0), ("q_th_gj_per_t", -1),
    ("eta_essiccatore_pct", 0), ("eta_essiccatore_pct", 100.1),
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
    assert mh775_valida(**d)["valido"] is False


@pytest.mark.parametrize("campo,valore", [
    ("p_t_anno", 0), ("p_t_anno", -3),
    ("q_th_gj_per_t", 0), ("q_th_gj_per_t", -1),
    ("eta_essiccatore_pct", 0), ("eta_essiccatore_pct", 100.1),
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
        mh775_calcola(**d)


def test_df_tabella_valori_demo_selezionati():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Produzione mangime (t/anno)"] == 60000.0
    assert mappa["Calore utile (MWh/anno)"] == pytest.approx(15000.0)
