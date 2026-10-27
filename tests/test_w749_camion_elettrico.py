"""Test tab749 "Camion elettrico a batteria: la ricarica megawatt batte
il diesel sul lungo raggio?"

Nuova tab tab749 (camion
elettrico, w750). Business case
deterministico di un camion merci
su strada a lungo raggio: confronta
DIESEL = camion diesel contro
BATTERIA = camion elettrico a
batteria con ricarica in deposito
+ ricarica megawatt MCS in rotta.
Km annui diretti, consumi per km
(kWh/km e L/km), energia di
trazione da km e consumo elettrico,
energia da rete da energia di
trazione e rendimento di ricarica,
split deposito / MCS per quota
share, costo energia pesato ai due
prezzi, litri diesel da km e consumo
diesel, CO2 da litri e fattore per
litro (diesel) e da MWh e fattore di
rete (elettrico), costi da energia,
O&M e EUA, CAPEX delta da camion
elettrico + ricarica meno camion
diesel, VAN, TIR, payback (primo
anno con cumulato >= 0), prezzo
medio di pareggio e potenza MCS
(energia per tratta / tempo di
sosta MCS).
Distinta dalla tab sul camion
pesante a idrogeno (fuel-cell,
altra propulsione e altra
infrastruttura), dalla tab708 sui
bus in deposito (bus urbani, non
merci a lungo raggio) e dalla tab
sul traghetto elettrico (navale,
non strada): qui merci su strada a
lungo raggio, km annui diretti,
due prezzi elettrici e potenza MCS
da sosta.

Demo calcolata eseguendo demo_calcoli()
(e ricontrollata a mano, riga per riga):
camion da 120000 km/anno, consumo
elettrico 1,20 kWh/km e consumo
diesel 0,32 L/km, quota deposito
0,70, prezzo deposito 180 EUR/MWh
e prezzo MCS 450 EUR/MWh, rendimento
ricarica 0,92, prezzo diesel 1,90
EUR/L, O&M diesel 25000 EUR/anno e
O&M elettrico 18000 EUR/anno,
fattore diesel 2,68 kg/L e fattore
rete 150 kg/MWh, prezzo EUA 85
EUR/t, CAPEX camion elettrico
250000 EUR, CAPEX camion diesel
130000 EUR e CAPEX ricarica 60000
EUR, tratta MCS 300 km con sosta
MCS 45 minuti, WACC 5 %, vita 8
anni, tolleranza 10 % del CAPEX
delta.

- e_trazione_mwh = 144.0
- e_rete_mwh = 156.52173913043478
- e_deposito_mwh = 109.56521739130434
- e_mcs_mwh = 46.956521739130444
- costo_energia_eur = 40852.17391304348
- litri_diesel = 38400.0
- co2_diesel_t = 102.912
- co2_elettrica_t = 23.478260869565215
- co2_evitata_t = 79.43373913043479
- costo_diesel_eur = 72960.0
- costo_co2_diesel_eur = 8747.52
- costo_co2_elettrica_eur = 1995.6521739130433
- totale_diesel_eur = 106707.52
- totale_elettrico_eur = 60847.82608695652
- risparmio_eur_anno = 45859.693913043484
- risparmio_eur_km = 0.38216411594202904
- risparmio_eur_mwh = 292.99248888888894
- e_tratta_mwh = 0.36
- potenza_mcs_mw = 0.48
- capex_delta_eur = 180000.0
- crf = 0.15472181362768103
- quota_capex_eur = 27849.926452982585
- costo_livellato_elettrico_eur = 88697.7525399391
- costo_livellato_diesel_eur = 106707.52
- van = 116400.95884216517
- tir = 19.245803235185406
- payback = 4
- prezzo_pareggio_eur_mwh = 553.9924888888889
- verdetto = 'CONVIENTE'

Scomposizione: E_trazione = 120000 x
1,20 / 1000 = 144,00 MWh; E_rete =
144,00 / 0,92 = 156,52 MWh; E_deposito
= 156,52 x 0,70 = 109,57 MWh; E_mcs =
156,52 x 0,30 = 46,96 MWh; costo
energia 109,57 x 180 + 46,96 x 450 =
19721,74 + 21130,43 = 40852,17 EUR;
litri = 120000 x 0,32 = 38400 L;
E_tratta = 300 x 1,20 / 1000 = 0,36
MWh; P_mcs = 0,36 / (45 / 60) = 0,48
MW; CO2 diesel 38400 x 2,68 / 1000 =
102,91 t; CO2 elettrica 156,52 x 150
/ 1000 = 23,48 t; evitata 79,43 t;
costo diesel 38400 x 1,90 = 72960,00
EUR; costo CO2 diesel 102,91 x 85 =
8747,52 EUR; totale diesel 72960,00
+ 8747,52 + 25000 = 106707,52 EUR;
costo CO2 elettrica 23,48 x 85 =
1995,65 EUR; totale elettrico
40852,17 + 1995,65 + 18000 =
60847,83 EUR; risparmio 106707,52 -
60847,83 = 45859,69 EUR/anno = 0,38
EUR/km = 292,99 EUR/MWh da rete;
CAPEX delta 250000 + 60000 - 130000
= 180000 EUR; CRF 0,05 x 1,05^8 /
(1,05^8 - 1) = 0.15472181362768103;
quota CAPEX 180000 x 0,154722 =
27849,93 EUR/anno; costo livellato
60847,83 + 27849,93 = 88697,75
EUR/anno contro 106707,52 EUR/anno
del diesel; flussi: anno 0 -180000,
anni 1-8 risparmio 45859,69 (piatti);
VAN -180000 + 45859,69 x 6,46321276
(annuita' 8 anni al 5 %) = 116400,96
EUR; TIR 19,25 % (bisezione esatta,
intervallo 15-30 %); payback 4
(cumulato anno 3: -180000 + 3 x
45859,69 = -42420,92 EUR, mai >= 0;
anno 4: +3438,78 EUR); prezzo medio
di pareggio (72960,00 + 8747,52 +
25000 - 18000 - 1995,65) / 156,52
= 553.9924888888889 EUR/MWh;
verdetto CONVIENTE perche' VAN > 0.
NOTA: il CRF entra solo nel costo
livellato, mai nei flussi: il CAPEX
delta compare una sola volta,
all'anno 0. NOTA 2: in questo brief
il risparmio nullo o negativo NON
e' degenere (a differenza della tab
sul traghetto): il camion elettrico
piu' caro del diesel resta
calcolabile e il verdetto e'
NON_CONVIENTE (prezzo MCS 1500
EUR/MWh: risparmio -3444,65
EUR/anno, VAN -202263,53 EUR,
payback mai, valid=True). NOTA 3:
la CO2 evitata negativa NON e'
degenere di per se': se il risparmio
resta > 0 il caso resta calcolabile
e la CO2 evitata negativa va detta
(rete 800 kg/MWh: CO2 elettrica
125,22 t, evitata -22,31 t, risparmio
37211,87 EUR/anno, VAN +60508,22
EUR, CONVIENTE). NOTA 4: il prezzo
di pareggio segue la formula del
brief (vedi test_prezzo_pareggio):
con gli input demo vale 553,99
EUR/MWh, non 560,35: 560,35 non si
ottiene dalla formula del brief con
questi input (numeratore 86711,87 /
156,52 = 553,99), quindi il test
asserisce il valore della formula.
"""

import ast
import math
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w750_helpers import (
    demo_calcoli,
    mh749_calcola,
    mh749_capex_delta,
    mh749_co2_diesel,
    mh749_co2_evitata,
    mh749_co2_rete,
    mh749_costo_co2,
    mh749_costo_diesel,
    mh749_costo_energia,
    mh749_costo_livellato,
    mh749_costo_totale,
    mh749_crf,
    mh749_csv,
    mh749_demo,
    mh749_e_deposito,
    mh749_e_mcs,
    mh749_e_rete,
    mh749_e_tratta,
    mh749_e_trazione,
    mh749_eta,
    mh749_flussi,
    mh749_int_nneg,
    mh749_int_pos,
    mh749_litri_diesel,
    mh749_nneg,
    mh749_num,
    mh749_pct_0_100,
    mh749_pct_wacc,
    mh749_pos,
    mh749_potenza_mcs,
    mh749_prezzo_pareggio,
    mh749_quota_capex,
    mh749_risparmio,
    mh749_risparmio_per_km,
    mh749_risparmio_per_mwh,
    mh749_share,
    mh749_tir,
    mh749_valida,
    mh749_van,
    mh749_verdetto,
    mh749_payback,
)


def _demo_kwargs():
    return dict(mh749_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh749_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh749_num(3, "x") == 3.0
    assert mh749_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh749_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh749_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh749_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh749_pos(0, "x")
    with pytest.raises(ValueError):
        mh749_pos(-1, "x")
    assert mh749_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh749_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh749_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh749_int_pos(0, "x")


def test_int_nneg_zero_ok():
    assert mh749_int_nneg(0, "x") == 0
    with pytest.raises(ValueError):
        mh749_int_nneg(-1, "x")


def test_pct_0_100_limiti():
    assert mh749_pct_0_100(0, "x") == 0.0
    assert mh749_pct_0_100(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh749_pct_0_100(100.1, "x")
    with pytest.raises(ValueError):
        mh749_pct_0_100(-1, "x")


def test_pct_wacc_limiti():
    assert mh749_pct_wacc(0, "x") == 0.0
    assert mh749_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh749_pct_wacc(50.1, "x")


def test_eta_limiti():
    assert mh749_eta(1.0, "x") == 1.0
    with pytest.raises(ValueError):
        mh749_eta(0.0, "x")
    with pytest.raises(ValueError):
        mh749_eta(1.01, "x")


def test_share_limiti():
    assert mh749_share(0.0, "x") == 0.0
    assert mh749_share(1.0, "x") == 1.0
    assert mh749_share(0.7, "x") == 0.7
    with pytest.raises(ValueError):
        mh749_share(-0.01, "x")
    with pytest.raises(ValueError):
        mh749_share(1.01, "x")


# ---------------------------------------------------------------- fisica base
def test_e_trazione():
    assert mh749_e_trazione(120000, 1.2) == 144.0
    assert mh749_e_trazione(0, 1.2) == 0.0


def test_e_rete():
    assert mh749_e_rete(144.0, 0.92) == pytest.approx(156.52173913043478)
    assert mh749_e_rete(100.0, 1.0) == 100.0


def test_e_deposito_e_mcs_somma_rete():
    assert mh749_e_deposito(156.52173913043478, 0.7) == pytest.approx(
        109.56521739130434)
    assert mh749_e_mcs(156.52173913043478, 0.7) == pytest.approx(
        46.956521739130444)
    assert mh749_e_deposito(100.0, 0.0) == 0.0
    assert mh749_e_mcs(100.0, 0.0) == 100.0
    assert mh749_e_deposito(100.0, 1.0) == 100.0
    assert mh749_e_mcs(100.0, 1.0) == 0.0
    assert mh749_e_deposito(156.52173913043478, 0.7) + mh749_e_mcs(
        156.52173913043478, 0.7) == pytest.approx(156.52173913043478)


def test_costo_energia_pesato():
    assert mh749_costo_energia(109.56521739130434, 180,
                               46.956521739130444, 450) == pytest.approx(
        40852.17391304348)
    assert mh749_costo_energia(100.0, 180, 0.0, 450) == 18000.0
    assert mh749_costo_energia(0.0, 180, 100.0, 450) == 45000.0


def test_litri_diesel():
    assert mh749_litri_diesel(120000, 0.32) == 38400.0
    assert mh749_litri_diesel(0, 0.32) == 0.0


def test_e_tratta_e_potenza_mcs():
    assert mh749_e_tratta(300, 1.2) == 0.36
    assert mh749_e_tratta(600, 1.2) == 0.72
    assert mh749_potenza_mcs(0.36, 45) == pytest.approx(0.48)
    assert mh749_potenza_mcs(0.72, 30) == pytest.approx(1.44)
    assert mh749_potenza_mcs(0.36, 60) == pytest.approx(0.36)
    with pytest.raises(ValueError):
        mh749_potenza_mcs(0.36, 0)


def test_co2_diesel():
    assert mh749_co2_diesel(38400, 2.68) == pytest.approx(102.912)


def test_co2_rete():
    assert mh749_co2_rete(156.52173913043478, 150) == pytest.approx(
        23.478260869565215)


def test_co2_evitata_segno_libero():
    assert mh749_co2_evitata(102.912, 23.478260869565215) == pytest.approx(
        79.43373913043479)
    assert mh749_co2_evitata(100.0, 200.0) == -100.0


def test_costo_energia_e_diesel_e_co2():
    assert mh749_costo_diesel(38400, 1.9) == 72960.0
    assert mh749_costo_co2(102.912, 85) == pytest.approx(8747.52)
    assert mh749_costo_co2(23.478260869565215, 85) == pytest.approx(
        1995.6521739130433)


def test_costo_totale():
    assert mh749_costo_totale(72960.0, 25000, 8747.52) == 106707.52
    assert mh749_costo_totale(0, 0, 0) == 0.0


def test_risparmio_e_per_km_e_per_mwh_rete():
    assert mh749_risparmio(106707.52, 60847.82608695652) == pytest.approx(
        45859.693913043484)
    assert mh749_risparmio(100.0, 200.0) == -100.0
    assert mh749_risparmio_per_km(45859.693913043484, 120000) == pytest.approx(
        0.38216411594202904)
    # denominatore E_rete, non E_trazione
    assert mh749_risparmio_per_mwh(45859.693913043484,
                                   156.52173913043478) == pytest.approx(
        292.99248888888894)
    assert mh749_risparmio_per_mwh(45859.693913043484, 144.0) == pytest.approx(
        318.4700967128028)
    with pytest.raises(ValueError):
        mh749_risparmio_per_km(100.0, 0)
    with pytest.raises(ValueError):
        mh749_risparmio_per_mwh(100.0, 0)


def test_capex_delta():
    assert mh749_capex_delta(250000, 60000, 130000) == 180000.0
    assert mh749_capex_delta(250000, 60000, 320000) == -10000.0
    assert mh749_capex_delta(0, 0, 0) == 0.0


def test_crf():
    assert mh749_crf(5.0, 8) == pytest.approx(0.15472181362768103)
    assert mh749_crf(0, 8) == 0.125
    assert mh749_crf(10.0, 10) == pytest.approx(0.16274539488251152)
    assert mh749_crf(5.0, 1) == pytest.approx(1.05)


def test_quota_capex_e_livellato():
    assert mh749_quota_capex(180000.0, 0.15472181362768103) == pytest.approx(
        27849.926452982585)
    assert mh749_quota_capex(-10000.0, 0.15472181362768103) == pytest.approx(
        -1547.2181362768103)
    assert mh749_costo_livellato(60847.82608695652, 27849.926452982585) == (
        pytest.approx(88697.7525399391))


def test_prezzo_pareggio_formula_brief():
    # formula del brief, ricalcolata a mano dagli input demo:
    # (72960,00 + 8747,52 + 25000 - 18000 - 1995,65) / 156,52
    num = 72960.0 + 8747.52 + 25000 - 18000 - 1995.6521739130433
    par = mh749_prezzo_pareggio(72960.0, 8747.52, 25000, 18000,
                                1995.6521739130433, 156.52173913043478)
    assert par == pytest.approx(num / 156.52173913043478)
    assert par == pytest.approx(553.9924888888889)
    assert mh749_prezzo_pareggio(100.0, 0, 0, 0, 0, 0) is None


# ---------------------------------------------------------------- flussi/VAN/TIR
def test_flussi_lunghezza_e_primo():
    f = mh749_flussi(180000.0, 45859.693913043484, 8)
    assert len(f) == 9
    assert f[0] == -180000.0
    assert all(v == 45859.693913043484 for v in f[1:])


def test_van_demo_e_zero_wacc():
    f = mh749_flussi(180000.0, 45859.693913043484, 8)
    assert mh749_van(f, 5.0) == pytest.approx(116400.95884216519)
    assert mh749_van([-100.0, 50.0, 50.0], 0) == 0.0


def test_tir_demo_intervallo_e_npv_zero():
    f = mh749_flussi(180000.0, 45859.693913043484, 8)
    r = mh749_tir(f)
    assert r == pytest.approx(0.19245803235185532)
    assert 0.15 < r < 0.30
    npv = sum(v / (1.0 + r) ** i for i, v in enumerate(f))
    assert abs(npv) < 1.0
    assert mh749_tir([100.0, 100.0]) is None
    assert mh749_tir([-100.0, -100.0]) is None
    assert mh749_tir([-100.0, 110.0]) == pytest.approx(0.1)


def test_payback():
    assert mh749_payback([-180000.0] + [45859.693913043484] * 8) == 4
    assert mh749_payback([-100.0, 10.0, 10.0]) is None
    assert mh749_payback([0.0, 10.0]) == 0
    assert mh749_payback([10000.0, 100.0]) == 0
    assert mh749_payback([-100.0, 50.0, 50.0]) == 2


def test_verdetto():
    assert mh749_verdetto(100.0, 180000.0, 10.0) == "CONVIENTE"
    assert mh749_verdetto(-5000.0, 180000.0, 10.0) == "MARGINALE"
    assert mh749_verdetto(-50000.0, 180000.0, 10.0) == "NON_CONVIENTE"
    assert mh749_verdetto(0.0, 180000.0, 10.0) == "MARGINALE"
    assert mh749_verdetto(float("nan"), 180000.0, 10.0) == "NON_CALCOLABILE"
    assert mh749_verdetto(100.0, 180000.0, 101.0) == "NON_CALCOLABILE"
    assert mh749_verdetto(-18000.0, 180000.0, 10.0) == "MARGINALE"
    assert mh749_verdetto(-18000.01, 180000.0, 10.0) == "NON_CONVIENTE"
    assert mh749_verdetto(-100.0, -10000.0, 10.0) == "MARGINALE"


# ---------------------------------------------------------------- valida
def test_valida_demo_ok():
    v = mh749_valida(**_demo_kwargs())
    assert v == {"valido": True, "errore": ""}


def test_valida_rifiuta_stringa_nan_inf_bool():
    base = _demo_kwargs()
    for campo, bad in (("km_anno", "120000"), ("km_anno", float("nan")),
                       ("km_anno", float("inf")), ("km_anno", True),
                       ("prezzo_mcs_eur_mwh", None)):
        d = dict(base)
        d[campo] = bad
        assert mh749_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    base = _demo_kwargs()
    casi = [("km_anno", 0), ("km_anno", -1),
            ("consumo_kwh_km", 0), ("consumo_l_km", -1),
            ("share_deposito", -0.1), ("share_deposito", 1.1),
            ("eta_ricarica", 0), ("eta_ricarica", 1.5),
            ("prezzo_deposito_eur_mwh", -1), ("prezzo_mcs_eur_mwh", -1),
            ("prezzo_diesel_eur_l", -0.1),
            ("om_diesel_eur_anno", -1), ("om_elettrico_eur_anno", -1),
            ("f_diesel_kg_l", -1), ("f_rete_kg_mwh", -1),
            ("prezzo_eua_eur_t", -1), ("capex_elettrico_eur", -1),
            ("capex_diesel_eur", -1), ("capex_ricarica_eur", -1),
            ("tratta_km", 0), ("sosta_mcs_min", 0),
            ("wacc_pct", 51), ("vita_anni", 0), ("vita_anni", 2.5),
            ("tolleranza_pct", 101)]
    for campo, val in casi:
        d = dict(base)
        d[campo] = val
        assert mh749_valida(**d)["valido"] is False, campo


def test_valida_accetta_limiti():
    base = _demo_kwargs()
    d = dict(base)
    d.update({"share_deposito": 0.0, "share_deposito_2": 0})
    d.pop("share_deposito_2")
    d.update({"eta_ricarica": 1.0, "wacc_pct": 0, "tolleranza_pct": 0,
              "prezzo_mcs_eur_mwh": 0, "capex_elettrico_eur": 0})
    assert mh749_valida(**d)["valido"] is True
    d2 = dict(base)
    d2.update({"share_deposito": 1.0})
    assert mh749_valida(**d2)["valido"] is True


# ---------------------------------------------------------------- demo esatta
def test_demo_dict():
    d = mh749_demo()
    assert d["km_anno"] == 120000
    assert d["consumo_kwh_km"] == 1.2
    assert d["consumo_l_km"] == 0.32
    assert d["share_deposito"] == 0.7
    assert d["prezzo_deposito_eur_mwh"] == 180
    assert d["prezzo_mcs_eur_mwh"] == 450
    assert d["eta_ricarica"] == 0.92
    assert d["prezzo_diesel_eur_l"] == 1.9
    assert d["om_diesel_eur_anno"] == 25000
    assert d["om_elettrico_eur_anno"] == 18000
    assert d["f_diesel_kg_l"] == 2.68
    assert d["f_rete_kg_mwh"] == 150
    assert d["prezzo_eua_eur_t"] == 85
    assert d["capex_elettrico_eur"] == 250000
    assert d["capex_diesel_eur"] == 130000
    assert d["capex_ricarica_eur"] == 60000
    assert d["tratta_km"] == 300
    assert d["sosta_mcs_min"] == 45
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 8
    assert d["tolleranza_pct"] == 10.0


def test_demo_calcoli_fisica():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["errore"] == ""
    assert bc["e_trazione_mwh"] == 144.0
    assert bc["e_rete_mwh"] == 156.52173913043478
    assert bc["e_deposito_mwh"] == 109.56521739130434
    assert bc["e_mcs_mwh"] == 46.956521739130444
    assert bc["costo_energia_eur"] == 40852.17391304348
    assert bc["litri_diesel"] == 38400.0
    assert bc["e_tratta_mwh"] == 0.36
    assert bc["potenza_mcs_mw"] == pytest.approx(0.48)
    assert bc["co2_diesel_t"] == 102.912
    assert bc["co2_elettrica_t"] == 23.478260869565215
    assert bc["co2_evitata_t"] == 79.43373913043479


def test_demo_calcoli_economia():
    bc = demo_calcoli()
    assert bc["costo_diesel_eur"] == 72960.0
    assert bc["costo_co2_diesel_eur"] == 8747.52
    assert bc["costo_co2_elettrica_eur"] == 1995.6521739130433
    assert bc["totale_diesel_eur"] == 106707.52
    assert bc["totale_elettrico_eur"] == 60847.82608695652
    assert bc["risparmio_eur_anno"] == 45859.693913043484
    assert bc["risparmio_eur_km"] == 0.38216411594202904
    assert bc["risparmio_eur_mwh"] == 292.99248888888894


def test_demo_calcoli_finanza():
    bc = demo_calcoli()
    assert bc["capex_delta_eur"] == 180000.0
    assert bc["crf"] == 0.15472181362768103
    assert bc["quota_capex_eur"] == 27849.926452982585
    assert bc["costo_livellato_elettrico_eur"] == 88697.7525399391
    assert bc["costo_livellato_diesel_eur"] == 106707.52
    assert bc["van"] == 116400.95884216517
    assert bc["tir"] == 19.245803235185406
    assert bc["payback"] == 4
    assert bc["prezzo_pareggio_eur_mwh"] == 553.9924888888889
    assert bc["verdetto"] == "CONVIENTE"


def test_demo_flussi_e_cumulato():
    bc = demo_calcoli()
    assert len(bc["flussi"]) == 9
    assert bc["flussi"][0] == -180000.0
    assert bc["flussi"][1] == 45859.693913043484
    assert len(bc["df_flussi"]) == 9
    assert bc["df_flussi"].iloc[3]["Cumulato (EUR)"] == pytest.approx(
        -42420.918260869556)
    assert bc["df_flussi"].iloc[4]["Cumulato (EUR)"] == pytest.approx(
        3438.7756521739284)
    assert bc["df_flussi"].iloc[8]["Cumulato (EUR)"] == pytest.approx(
        186877.55130434787)


def test_demo_tabella_righe():
    bc = demo_calcoli()
    assert len(bc["df_tabella"]) == 50
    voci = list(bc["df_tabella"]["Voce"])
    assert "Km annui (km/anno)" in voci
    assert "Energia da deposito (MWh/anno)" in voci
    assert "Energia da MCS (MWh/anno)" in voci
    assert "Potenza MCS (MW)" in voci
    assert "CAPEX delta (EUR)" in voci
    assert "Verdetto" in voci
    riga = bc["df_tabella"][bc["df_tabella"]["Voce"] == "VAN (EUR)"]
    assert float(riga["Valore"].iloc[0]) == 116400.95884216517


def test_demo_coerenza_interna():
    bc = demo_calcoli()
    assert bc["totale_diesel_eur"] - bc["totale_elettrico_eur"] == (
        pytest.approx(bc["risparmio_eur_anno"]))
    assert bc["co2_diesel_t"] - bc["co2_elettrica_t"] == pytest.approx(
        bc["co2_evitata_t"])
    assert bc["e_deposito_mwh"] + bc["e_mcs_mwh"] == pytest.approx(
        bc["e_rete_mwh"])
    assert bc["capex_elettrico_eur"] + bc["capex_ricarica_eur"] - (
        bc["capex_diesel_eur"]) == bc["capex_delta_eur"]
    assert bc["totale_elettrico_eur"] + bc["quota_capex_eur"] == (
        pytest.approx(bc["costo_livellato_elettrico_eur"]))
    assert bc["risparmio_eur_anno"] / bc["km_anno"] == pytest.approx(
        bc["risparmio_eur_km"])
    assert bc["risparmio_eur_anno"] / bc["e_rete_mwh"] == pytest.approx(
        bc["risparmio_eur_mwh"])


def test_demo_crf_solo_nel_livellato_non_nei_flussi():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -bc["capex_delta_eur"]
    van_senza_crf = -bc["capex_delta_eur"] + sum(
        bc["risparmio_eur_anno"] / (1.05 ** t) for t in range(1, 9))
    assert bc["van"] == pytest.approx(van_senza_crf)


def test_demo_contro_riconteggio_indipendente():
    """_DEMO del test contro demo_calcoli(): ogni uscita e'
    ricalcolata da zero dagli input demo, mismatch < 1e-9 relativo
    dove applicabile (valori nulli esatti)."""
    d = mh749_demo()
    km = d["km_anno"]
    etr = km * d["consumo_kwh_km"] / 1000.0
    er = etr / d["eta_ricarica"]
    ed = er * d["share_deposito"]
    em = er * (1.0 - d["share_deposito"])
    cen = ed * d["prezzo_deposito_eur_mwh"] + em * d["prezzo_mcs_eur_mwh"]
    li = km * d["consumo_l_km"]
    co2d = li * d["f_diesel_kg_l"] / 1000.0
    co2e = er * d["f_rete_kg_mwh"] / 1000.0
    cdi = li * d["prezzo_diesel_eur_l"]
    ccd = co2d * d["prezzo_eua_eur_t"]
    cce = co2e * d["prezzo_eua_eur_t"]
    td = cdi + d["om_diesel_eur_anno"] + ccd
    te = cen + d["om_elettrico_eur_anno"] + cce
    risp = td - te
    etv = d["tratta_km"] * d["consumo_kwh_km"] / 1000.0
    pmw = etv / (d["sosta_mcs_min"] / 60.0)
    delta = (d["capex_elettrico_eur"] + d["capex_ricarica_eur"]
             - d["capex_diesel_eur"])
    r = d["wacc_pct"] / 100.0
    crf = r * (1.0 + r) ** d["vita_anni"] / ((1.0 + r) ** d["vita_anni"]
                                            - 1.0)
    quota = delta * crf
    liv = te + quota
    par = (cdi + ccd + d["om_diesel_eur_anno"]
           - d["om_elettrico_eur_anno"] - cce) / er
    flussi = [-delta] + [risp] * d["vita_anni"]
    van = sum(f / (1.0 + r) ** t for t, f in enumerate(flussi))

    def _rel(a, b):
        if b == 0:
            return a == 0
        return abs(a - b) / abs(b) < 1e-9

    bc = demo_calcoli()
    attesi = {"e_trazione_mwh": etr, "e_rete_mwh": er,
              "e_deposito_mwh": ed, "e_mcs_mwh": em,
              "costo_energia_eur": cen, "litri_diesel": li,
              "co2_diesel_t": co2d, "co2_elettrica_t": co2e,
              "co2_evitata_t": co2d - co2e, "costo_diesel_eur": cdi,
              "costo_co2_diesel_eur": ccd, "costo_co2_elettrica_eur": cce,
              "totale_diesel_eur": td, "totale_elettrico_eur": te,
              "risparmio_eur_anno": risp, "risparmio_eur_km": risp / km,
              "risparmio_eur_mwh": risp / er, "e_tratta_mwh": etv,
              "potenza_mcs_mw": pmw, "capex_delta_eur": delta,
              "crf": crf, "quota_capex_eur": quota,
              "costo_livellato_elettrico_eur": liv,
              "costo_livellato_diesel_eur": td, "van": van,
              "prezzo_pareggio_eur_mwh": par}
    for chiave, atteso in attesi.items():
        assert _rel(bc[chiave], atteso), chiave
    assert bc["flussi"] == flussi


def test_demo_riconteggio_crf_van_payback_pareggio_mcs_a_mano():
    """CRF, VAN, payback, pareggio e P_mcs ricalcolati a mano,
    senza usare gli helper omonimi (solo aritmetica diretta)."""
    bc = demo_calcoli()
    crf_mano = 0.05 * 1.05 ** 8 / (1.05 ** 8 - 1.0)
    assert bc["crf"] == pytest.approx(crf_mano)
    annuita = (1.0 - 1.05 ** -8) / 0.05
    van_mano = -180000.0 + 45859.693913043484 * annuita
    assert bc["van"] == pytest.approx(van_mano)
    cum = -180000.0
    pb_mano = None
    for anno in range(1, 9):
        cum += 45859.693913043484
        if cum >= 0.0 and pb_mano is None:
            pb_mano = anno
    assert bc["payback"] == pb_mano == 4
    par_mano = (72960.0 + 8747.52 + 25000 - 18000 - 1995.6521739130433) / (
        144.0 / 0.92)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(par_mano)
    assert bc["potenza_mcs_mw"] == pytest.approx((300 * 1.2 / 1000.0)
                                                 / (45 / 60.0))


# ---------------------------------------------------------------- varianti
def test_variante_share_zero_tutto_mcs():
    v = _variante(share_deposito=0.0)
    assert v["valid"] is True
    assert v["e_deposito_mwh"] == 0.0
    assert v["costo_energia_eur"] == pytest.approx(70434.78260869565)
    assert v["risparmio_eur_anno"] == pytest.approx(16277.08695652174)
    assert v["van"] == pytest.approx(-74797.73747478426)
    assert v["verdetto"] == "NON_CONVIENTE"
    assert v["payback"] is None


def test_variante_share_uno_tutto_deposito():
    v = _variante(share_deposito=1.0)
    assert v["valid"] is True
    assert v["e_mcs_mwh"] == 0.0
    assert v["costo_energia_eur"] == pytest.approx(28173.91304347826)
    assert v["risparmio_eur_anno"] == pytest.approx(58537.95652173913)
    assert v["van"] == pytest.approx(198343.26432710586)
    assert v["verdetto"] == "CONVIENTE"


def test_variante_marginale_ad_hoc():
    # VAN demo +10000 di CAPEX in piu' -> VAN -10000, entro il 10 %
    # di 190000 circa: MARGINALE. Costruito da VAN demo, non da
    # un numero magico: VAN_nuova = VAN_demo - delta_capex.
    bc = demo_calcoli()
    extra = bc["van"] + 10000.0
    v = _variante(capex_elettrico_eur=250000 + extra)
    assert v["van"] == pytest.approx(-10000.0)
    assert v["verdetto"] == "MARGINALE"
    assert v["payback"] == 7


def test_variante_non_conviente_capex_alto():
    v = _variante(capex_elettrico_eur=420000)
    assert v["capex_delta_eur"] == 350000.0
    assert v["van"] == pytest.approx(-53599.04115783481)
    assert v["verdetto"] == "NON_CONVIENTE"


def test_variante_risparmio_negativo_calcolabile_non_degenere():
    v = _variante(prezzo_mcs_eur_mwh=1500)
    assert v["valid"] is True
    assert v["risparmio_eur_anno"] == pytest.approx(-3444.6521739130433)
    assert v["van"] == pytest.approx(-202263.5292331601)
    assert v["verdetto"] == "NON_CONVIENTE"
    assert v["payback"] is None
    assert v["tir"] is None


def test_variante_rete_sporca_co2_negativa_ma_calcolabile():
    v = _variante(f_rete_kg_mwh=800)
    assert v["valid"] is True
    assert v["co2_elettrica_t"] == pytest.approx(125.21739130434781)
    assert v["co2_evitata_t"] == pytest.approx(-22.30539130434781)
    assert v["risparmio_eur_anno"] == pytest.approx(37211.86756521739)
    assert v["van"] == pytest.approx(60508.22138395109)
    assert v["verdetto"] == "CONVIENTE"


def test_variante_eta_uno():
    v = _variante(eta_ricarica=1.0)
    assert v["e_rete_mwh"] == 144.0
    assert v["totale_elettrico_eur"] == 57420.0
    assert v["risparmio_eur_anno"] == pytest.approx(49287.52)
    assert v["van"] == pytest.approx(138555.72814447674)
    assert v["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero():
    v = _variante(wacc_pct=0)
    assert v["crf"] == 0.125
    assert v["quota_capex_eur"] == 22500.0
    assert v["costo_livellato_elettrico_eur"] == pytest.approx(
        83347.82608695652)
    assert v["van"] == pytest.approx(186877.55130434787)
    assert v["verdetto"] == "CONVIENTE"


def test_variante_sosta_e_tratta_piu_potenza():
    v = _variante(tratta_km=600, sosta_mcs_min=30)
    assert v["e_tratta_mwh"] == pytest.approx(0.72)
    assert v["potenza_mcs_mw"] == pytest.approx(1.44)


def test_variante_delta_negativo_payback_zero():
    v = _variante(capex_diesel_eur=320000)
    assert v["capex_delta_eur"] == -10000.0
    assert v["payback"] == 0
    assert v["van"] == pytest.approx(306400.9588421652)
    assert v["verdetto"] == "CONVIENTE"


def test_variante_delta_zero_payback_zero_tir_none():
    v = _variante(capex_elettrico_eur=0, capex_ricarica_eur=0,
                  capex_diesel_eur=0)
    assert v["capex_delta_eur"] == 0.0
    assert v["payback"] == 0
    assert v["tir"] is None
    assert v["verdetto"] == "CONVIENTE"


def test_variante_vita_uno():
    v = _variante(vita_anni=1)
    assert v["flussi"] == [-180000.0, 45859.693913043484]
    assert v["payback"] is None
    assert v["van"] == pytest.approx(-136324.10103519668)


def test_variante_prezzo_mcs_alto_non_conviente():
    v = _variante(prezzo_mcs_eur_mwh=900)
    assert v["risparmio_eur_anno"] == pytest.approx(24729.260869565216)
    assert v["van"] == pytest.approx(-20169.54237627641)
    assert v["verdetto"] == "NON_CONVIENTE"


# ---------------------------------------------------------------- degeneri
def test_degenere_km_zero():
    v = _variante(km_anno=0)
    assert v["valid"] is False
    assert v["verdetto"] == "NON_CALCOLABILE"
    assert v["e_rete_mwh"] == 0.0
    assert v["prezzo_pareggio_eur_mwh"] is None
    assert v["flussi"] == []


def test_degenere_eta_zero_e_sopra_uno():
    assert _variante(eta_ricarica=0)["valid"] is False
    assert _variante(eta_ricarica=1.5)["valid"] is False
    assert _variante(eta_ricarica=0)["verdetto"] == "NON_CALCOLABILE"


def test_degenere_consumi_zero():
    assert _variante(consumo_kwh_km=0)["valid"] is False
    assert _variante(consumo_l_km=0)["valid"] is False
    assert _variante(consumo_kwh_km=0)["verdetto"] == "NON_CALCOLABILE"


def test_degenere_share_fuori_range():
    assert _variante(share_deposito=-0.1)["valid"] is False
    assert _variante(share_deposito=1.1)["valid"] is False


def test_degenere_tratta_sosta_zero():
    assert _variante(tratta_km=0)["valid"] is False
    assert _variante(sosta_mcs_min=0)["valid"] is False


def test_degenere_wacc_vita_tolleranza():
    assert _variante(wacc_pct=60)["valid"] is False
    assert _variante(wacc_pct=-1)["valid"] is False
    assert _variante(vita_anni=0)["valid"] is False
    assert _variante(tolleranza_pct=101)["valid"] is False


def test_degenere_stringa_nan_inf():
    assert _variante(prezzo_diesel_eur_l="1.9")["valid"] is False
    assert _variante(prezzo_mcs_eur_mwh=float("nan"))["valid"] is False
    assert _variante(capex_diesel_eur=float("inf"))["valid"] is False
    assert _variante(km_anno=True)["valid"] is False


def test_degenere_neutro_campi():
    v = _variante(km_anno=-5)
    assert v["valid"] is False
    assert v["errore"] != ""
    assert v["e_trazione_mwh"] == 0.0
    assert v["e_rete_mwh"] == 0.0
    assert v["risparmio_eur_km"] is None
    assert v["risparmio_eur_mwh"] is None
    assert v["van"] == 0.0
    assert list(v["df_flussi"].columns) == ["Anno", "Flusso (EUR/anno)",
                                           "Cumulato (EUR)"]
    assert list(v["df_tabella"].columns) == ["Voce", "Valore"]


def test_pareggio_none_quando_e_rete_zero():
    assert mh749_prezzo_pareggio(100.0, 0, 0, 0, 0, 0) is None
    v = _variante(km_anno=0)
    assert v["prezzo_pareggio_eur_mwh"] is None


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = demo_calcoli()
    csv = mh749_csv(bc, mh749_demo())
    righe = csv.strip().split("\n")
    assert righe[0] == "voce;valore"
    assert any(r.startswith("km_anno;120000") for r in righe)
    assert any(r.startswith("verdetto;CONVIENTE") for r in righe)
    assert any(r.startswith("potenza_mcs_mw;") for r in righe)
    assert any(r.startswith("capex_delta_eur;180000") for r in righe)
    assert any(r.startswith("e_deposito_mwh;") for r in righe)
    assert any(r.startswith("e_mcs_mwh;") for r in righe)
    assert len(righe) == 51


def test_csv_valori_coerenti_con_calcola():
    bc = demo_calcoli()
    csv = mh749_csv(bc, mh749_demo())
    assert "van_eur;116400.95884216517" in csv
    assert "tir_pct;19.245803235185406" in csv
    assert "payback_anni;4" in csv
    assert "prezzo_pareggio_eur_mwh;553.9924888888889" in csv


def test_csv_degenere_solo_zeri():
    bc = _variante(km_anno=0)
    csv = mh749_csv(bc, mh749_demo())
    assert "verdetto;NON_CALCOLABILE" in csv
    assert "van_eur;0.0" in csv


def test_csv_contiene_tutte_le_chiavi_input():
    bc = demo_calcoli()
    csv = mh749_csv(bc, mh749_demo())
    for chiave in ("km_anno", "consumo_kwh_km", "consumo_l_km",
                   "share_deposito", "prezzo_deposito_eur_mwh",
                   "prezzo_mcs_eur_mwh", "eta_ricarica",
                   "prezzo_diesel_eur_l", "om_diesel_eur_anno",
                   "om_elettrico_eur_anno", "f_diesel_kg_l",
                   "f_rete_kg_mwh", "prezzo_eua_eur_t",
                   "capex_elettrico_eur", "capex_diesel_eur",
                   "capex_ricarica_eur", "tratta_km", "sosta_mcs_min",
                   "wacc_pct", "vita_anni", "tolleranza_pct"):
        assert f"\n{chiave};" in csv


# ---------------------------------------------------------------- misc
def test_calcola_non_sollevela_per_input_numerici():
    for kw in ({"km_anno": 0}, {"eta_ricarica": 2},
               {"vita_anni": -3}, {"share_deposito": 2}):
        v = _variante(**kw)
        assert v["valid"] is False
        assert v["verdetto"] == "NON_CALCOLABILE"


def test_monotonia_prezzo_mcs():
    vans = [_variante(prezzo_mcs_eur_mwh=p)["van"]
            for p in (300, 450, 600, 900)]
    assert vans[0] > vans[1] > vans[2] > vans[3]


def test_monotonia_km():
    risp = [_variante(km_anno=k)["risparmio_eur_anno"]
            for k in (60000, 120000, 200000)]
    assert risp[0] < risp[1] < risp[2]


def test_scala_km_doppia():
    a = _variante(km_anno=120000)
    b = _variante(km_anno=240000)
    assert b["e_trazione_mwh"] == pytest.approx(2 * a["e_trazione_mwh"])
    assert b["litri_diesel"] == 2 * a["litri_diesel"]
    assert b["e_rete_mwh"] == pytest.approx(2 * a["e_rete_mwh"])


def test_risparmio_lineare_in_prezzo_diesel():
    a = _variante(prezzo_diesel_eur_l=1.9)
    b = _variante(prezzo_diesel_eur_l=2.9)
    assert b["risparmio_eur_anno"] - a["risparmio_eur_anno"] == pytest.approx(
        38400.0)


def test_demo_deterministica_due_chiamate():
    a = demo_calcoli()
    b = demo_calcoli()
    assert a["van"] == b["van"]
    assert a["flussi"] == b["flussi"]
    assert a["tir"] == b["tir"]


def test_demo_chiavi_attese():
    assert set(mh749_demo().keys()) == {
        "km_anno", "consumo_kwh_km", "consumo_l_km",
        "share_deposito", "prezzo_deposito_eur_mwh",
        "prezzo_mcs_eur_mwh", "eta_ricarica",
        "prezzo_diesel_eur_l", "om_diesel_eur_anno",
        "om_elettrico_eur_anno", "f_diesel_kg_l",
        "f_rete_kg_mwh", "prezzo_eua_eur_t",
        "capex_elettrico_eur", "capex_diesel_eur",
        "capex_ricarica_eur", "tratta_km", "sosta_mcs_min",
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


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w750_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w750_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab749:")


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    # token vietati costruiti per concatenazione, cosi' questo
    # stesso file non li contiene come sottostringhe contigue.
    src = _leggi("w750_helpers.py")
    vietati = ["mh" + "74" + "8", "st" + "74" + "8",
               "tab" + "74" + "8", "74" + "8"]
    assert "streamlit" not in src
    assert all(t not in src for t in vietati)


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w750_ui.py")
    vietati = ["mh" + "74" + "8", "st" + "74" + "8",
               "tab" + "74" + "8", "74" + "8"]
    assert all(t not in src for t in vietati)
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st749_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert "key=f" not in src and 'key = f' not in src
    assert "st.stop()" in src
    # guard degenere prima di KPI / grafico / tabella / CSV
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")


def test_test_senza_residui_vecchia_tab():
    # token costruiti per concatenazione: il sorgente di questo
    # stesso test non deve contenere i token vietati come
    # sottostringhe contigue (altrimenti il test sarebbe
    # autoreferenziale e fallirebbe sempre).
    src = _leggi("w750_test.py")
    vietati = ["mh" + "74" + "8", "st" + "74" + "8",
               "tab" + "74" + "8", "74" + "8"]
    assert all(t not in src for t in vietati)


def test_ui_chiavi_demo_coerenti():
    """Ogni _def749[...] letto dalla UI esiste nel dict demo:
    sweep anti-KeyError a render (lezione tab674)."""
    src = _leggi("w750_ui.py")
    usate = set(re.findall(r'_def749\["([^"]+)"\]', src))
    assert usate
    assert usate <= set(mh749_demo().keys())


def test_ui_riferisce_solo_helper_nuovi():
    src = _leggi("w750_ui.py")
    usati = set(re.findall(r'\b(mh\d+_\w+)\b', src))
    assert usati
    assert all(u.startswith("mh749_") for u in usati)


@pytest.mark.parametrize("wacc,vita,atteso", [
    (5.0, 8, 0.15472181362768103),
    (0, 8, 0.125),
    (10.0, 10, 0.16274539488251152),
    (5.0, 1, 1.05),
    (50.0, 5, 0.5758293838862559),
])
def test_crf_parametrizzato(wacc, vita, atteso):
    assert mh749_crf(wacc, vita) == pytest.approx(atteso)


@pytest.mark.parametrize("campo,valore", [
    ("km_anno", 0), ("km_anno", -3),
    ("consumo_kwh_km", -0.5), ("consumo_l_km", 0),
    ("share_deposito", -0.1), ("share_deposito", 1.1),
    ("eta_ricarica", 0), ("eta_ricarica", 2),
    ("prezzo_deposito_eur_mwh", -5), ("prezzo_mcs_eur_mwh", -5),
    ("prezzo_diesel_eur_l", -0.01), ("om_diesel_eur_anno", -100),
    ("om_elettrico_eur_anno", -100), ("f_diesel_kg_l", -2.68),
    ("f_rete_kg_mwh", -150), ("prezzo_eua_eur_t", -85),
    ("capex_elettrico_eur", -1), ("capex_ricarica_eur", -1),
    ("capex_diesel_eur", -1), ("tratta_km", -10),
    ("sosta_mcs_min", -10), ("wacc_pct", -0.1),
    ("wacc_pct", 50.1), ("vita_anni", -1), ("vita_anni", 2.5),
    ("tolleranza_pct", -1), ("tolleranza_pct", 100.1),
])
def test_valida_rifiuta_singoli_campi(campo, valore):
    d = _demo_kwargs()
    d[campo] = valore
    assert mh749_valida(**d)["valido"] is False


def test_e_rete_maggiore_di_trazione_per_eta_minore_uno():
    assert mh749_e_rete(1000.0, 0.5) == 2000.0
    assert mh749_e_rete(1000.0, 0.8) == 1250.0


def test_df_tabella_valori_demo_selezionati():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Km annui (km/anno)"] == 120000.0
    assert mappa["Litri diesel (L/anno)"] == 38400.0
    assert mappa["Potenza MCS (MW)"] == pytest.approx(0.48)
    assert mappa["CAPEX delta (EUR)"] == 180000.0
    assert mappa["Payback (anni)"] == 4
    assert mappa["Verdetto"] == "CONVIENTE"
