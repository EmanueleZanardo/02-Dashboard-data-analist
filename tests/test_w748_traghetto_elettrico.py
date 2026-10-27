"""Test tab748 "Traghetto elettrico a batteria: la batteria batte il diesel sulla rotta breve?"

Nuova tab tab748 (traghetto
elettrico, w749). Business case
deterministico di un traghetto su
rotta breve: confronta DIESEL =
traghetto con motori diesel contro
BATTERIA = traghetto elettrico a
batteria con ricarica in banchina.
Km annui da distanza e traversate,
energia di trazione da km e consumo
elettrico, energia da rete da energia
di trazione e rendimento di ricarica,
litri diesel da km e consumo diesel,
CO2 da litri e fattore per litro
(diesel) e da MWh e fattore di rete
(elettrico), costi da energia, O&M e
EUA, CAPEX delta da traghetto
elettrico + ricarica meno traghetto
diesel, VAN, TIR, payback (primo anno
con cumulato >= 0), prezzo elettrico
di pareggio e potenza di ricarica in
banchina (energia per traversata /
tempo di sosta).
Nessuna altra tab e' dedicata al
traghetto elettrico a batteria: 0
occorrenze di "traghetto", "ferry"
e "aliscafo" in app.py prima di
questa tab. La tab708 sui bus
elettrici in deposito e la tab cold ironing
sul cold ironing sono analoghe ma
diverse (non propulsione navale per
km con litri diesel, potenza di
ricarica da sosta e CAPEX delta su
tre voci).

Demo calcolata eseguendo demo_calcoli()
(e ricontrollata a mano, riga per riga):
traghetto su rotta da 10 km con 3650
traversate all'anno (10 al giorno),
consumo elettrico 30 kWh/km e consumo
diesel 5 L/km, rendimento ricarica
0,92 e sosta 20 minuti, prezzo
elettricita' 180 EUR/MWh e prezzo
diesel 1,90 EUR/L, O&M diesel 400000
EUR/anno e O&M elettrico 250000
EUR/anno, fattore diesel 2,68 kg/L e
fattore rete 150 kg/MWh, prezzo EUA
85 EUR/t, CAPEX traghetto elettrico
10000000 EUR, CAPEX ricarica 1500000
EUR e CAPEX traghetto diesel 8000000
EUR, WACC 5 %, vita 20 anni,
tolleranza 10 % del CAPEX delta.

- km_anno = 36500.0
- e_trazione_mwh = 1095.0
- e_rete_mwh = 1190.2173913043478
- litri_diesel = 182500.0
- e_traversata_mwh = 0.3
- potenza_ricarica_mw = 0.9
- co2_diesel_t = 489.1000000000001
- co2_elettrica_t = 178.53260869565216
- co2_evitata_t = 310.5673913043479
- costo_diesel_eur = 346750.0
- costo_co2_diesel_eur = 41573.50000000001
- costo_energia_elettrica_eur = 214239.1304347826
- costo_co2_elettrica_eur = 15175.271739130434
- totale_diesel_eur = 788323.5
- totale_elettrico_eur = 479414.402173913
- risparmio_eur_anno = 308909.097826087
- risparmio_eur_km = 8.463262954139369
- risparmio_eur_mwh = 282.108765137979
- capex_delta_eur = 3500000.0
- crf = 0.08024258719069129
- quota_capex_eur = 280849.0551674195
- costo_livellato_elettrico_eur = 760263.4573413325
- costo_livellato_elettrico_eur_km = 20.82913581757075
- costo_diesel_eur_km = 21.59790410958904
- van = 349690.15383295575
- tir = 6.151481017884801
- payback = 12
- prezzo_pareggio_eur_mwh = 439.54006392694066
- verdetto = 'CONVIENTE'

Scomposizione: km = 10 x 3650 =
36500 km; E_trazione = 36500 x 30 /
1000 = 1095,00 MWh; E_rete = 1095 /
0,92 = 1190,22 MWh; litri = 36500 x
5 = 182500 L; E_traversata = 10 x 30
/ 1000 = 0,30 MWh; P_ricarica = 0,30
/ (20 / 60) = 0,90 MW; CO2 diesel
182500 x 2,68 / 1000 = 489,10 t; CO2
elettrica 1190,22 x 150 / 1000 =
178,53 t; evitata 310,57 t; costo
diesel 182500 x 1,90 = 346750,00 EUR;
costo CO2 diesel 489,10 x 85 =
41573,50 EUR; totale diesel 346750,00
+ 41573,50 + 400000 = 788323,50 EUR;
costo energia 1190,22 x 180 =
214239,13 EUR; costo CO2 elettrica
178,53 x 85 = 15175,27 EUR; totale
elettrico 214239,13 + 15175,27 +
250000 = 479414,40 EUR; risparmio
788323,50 - 479414,40 = 308909,10
EUR/anno = 8,46 EUR/km = 282,11
EUR/MWh; CAPEX delta 10000000 +
1500000 - 8000000 = 3500000 EUR; CRF
0,05 x 1,05^20 / (1,05^20 - 1) =
0.08024258719069129; quota CAPEX
3500000 x 0,080243 = 280849,06
EUR/anno; costo livellato 479414,40
+ 280849,06 = 760263,46 EUR/anno =
20,83 EUR/km contro 21,60 EUR/km del
diesel; flussi: anno 0 -3500000, anni
1-20 risparmio 308909,10 (piatti); VAN
-3500000 + 308909,10 x 12,462210343296
(annuita' 20 anni al 5 %) = 349690,15
EUR; TIR 6,15 % (bisezione esatta);
payback 12 (cumulato anno 11:
-3500000 + 11 x 308909,10 =
-101999,92 EUR, mai >= 0; anno 12:
+206909,17 EUR); prezzo elettrico di
pareggio (346750,00 + 41573,50 +
400000 - 250000 - 15175,27) / 1190,22
= 439.54006392694066 EUR/MWh;
verdetto CONVIENTE perche' VAN > 0.
NOTA: il CRF entra solo nel costo
livellato, mai nei flussi: il CAPEX
delta compare una sola volta,
all'anno 0. NOTA 2: in questo brief
il risparmio nullo o negativo E'
degenere (come nella tab cold ironing): il
traghetto elettrico piu' caro del
diesel non ha senso economico da
mostrare come caso calcolabile, e al
prezzo di pareggio esatto il caso e'
degenere (risparmio 0). NOTA 3: la
CO2 evitata negativa NON e' degenere
di per se': se il risparmio resta > 0
il caso resta calcolabile e la CO2
evitata negativa va detta (rete 800
kg/MWh: CO2 elettrica 952,17 t,
evitata -463,07 t, risparmio
243149,59 EUR/anno, VAN -469818,70
EUR, NON_CONVIENTE).
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w749_helpers import (
    demo_calcoli,
    mh748_calcola,
    mh748_capex_delta,
    mh748_co2_diesel,
    mh748_co2_evitata,
    mh748_co2_rete,
    mh748_costo_co2,
    mh748_costo_diesel,
    mh748_costo_energia,
    mh748_costo_livellato,
    mh748_costo_per_km,
    mh748_costo_totale,
    mh748_crf,
    mh748_csv,
    mh748_demo,
    mh748_e_rete,
    mh748_e_trazione,
    mh748_e_traversata,
    mh748_eta,
    mh748_flussi,
    mh748_int_nneg,
    mh748_int_pos,
    mh748_km_anno,
    mh748_litri_diesel,
    mh748_nneg,
    mh748_num,
    mh748_pct_0_100,
    mh748_pct_wacc,
    mh748_pos,
    mh748_potenza_ricarica,
    mh748_prezzo_pareggio,
    mh748_quota_capex,
    mh748_risparmio,
    mh748_risparmio_per_km,
    mh748_risparmio_per_mwh,
    mh748_tir,
    mh748_valida,
    mh748_van,
    mh748_verdetto,
    mh748_payback,
)


def _demo_kwargs():
    return dict(mh748_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh748_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh748_num(3, "x") == 3.0
    assert mh748_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh748_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh748_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh748_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh748_pos(0, "x")
    with pytest.raises(ValueError):
        mh748_pos(-1, "x")
    assert mh748_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh748_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh748_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh748_int_pos(0, "x")


def test_int_nneg_zero_ok():
    assert mh748_int_nneg(0, "x") == 0
    with pytest.raises(ValueError):
        mh748_int_nneg(-1, "x")


def test_pct_0_100_limiti():
    assert mh748_pct_0_100(0, "x") == 0.0
    assert mh748_pct_0_100(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh748_pct_0_100(100.1, "x")
    with pytest.raises(ValueError):
        mh748_pct_0_100(-1, "x")


def test_pct_wacc_limiti():
    assert mh748_pct_wacc(0, "x") == 0.0
    assert mh748_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh748_pct_wacc(50.1, "x")


def test_eta_limiti():
    assert mh748_eta(1.0, "x") == 1.0
    with pytest.raises(ValueError):
        mh748_eta(0.0, "x")
    with pytest.raises(ValueError):
        mh748_eta(1.01, "x")


# ---------------------------------------------------------------- fisica base
def test_km_anno():
    assert mh748_km_anno(10, 3650) == 36500
    assert mh748_km_anno(2.5, 100) == 250.0


def test_e_trazione():
    assert mh748_e_trazione(36500, 30) == 1095.0
    assert mh748_e_trazione(0, 30) == 0.0


def test_e_rete():
    assert mh748_e_rete(1095.0, 0.92) == pytest.approx(1190.2173913043478)
    assert mh748_e_rete(100.0, 1.0) == 100.0


def test_litri_diesel():
    assert mh748_litri_diesel(36500, 5) == 182500.0
    assert mh748_litri_diesel(0, 5) == 0.0


def test_e_traversata():
    assert mh748_e_traversata(10, 30) == 0.3
    assert mh748_e_traversata(20, 25) == 0.5


def test_potenza_ricarica():
    assert mh748_potenza_ricarica(0.3, 20) == pytest.approx(0.9)
    assert mh748_potenza_ricarica(0.3, 10) == pytest.approx(1.8)
    assert mh748_potenza_ricarica(0.3, 60) == pytest.approx(0.3)
    with pytest.raises(ValueError):
        mh748_potenza_ricarica(0.3, 0)


def test_co2_diesel():
    assert mh748_co2_diesel(182500, 2.68) == pytest.approx(489.1)


def test_co2_rete():
    assert mh748_co2_rete(1190.2173913043478, 150) == pytest.approx(
        178.53260869565216)


def test_co2_evitata_segno_libero():
    assert mh748_co2_evitata(489.1, 178.53) == pytest.approx(310.57)
    assert mh748_co2_evitata(100.0, 200.0) == -100.0


def test_costo_energia_e_diesel_e_co2():
    assert mh748_costo_energia(1190.2173913043478, 180) == pytest.approx(
        214239.1304347826)
    assert mh748_costo_diesel(182500, 1.9) == 346750.0
    assert mh748_costo_co2(489.1, 85) == pytest.approx(41573.5)


def test_costo_totale():
    assert mh748_costo_totale(346750.0, 400000, 41573.5) == 788323.5
    assert mh748_costo_totale(0, 0, 0) == 0.0


def test_risparmio_e_per_km_e_per_mwh():
    assert mh748_risparmio(788323.5, 479414.402173913) == pytest.approx(
        308909.097826087)
    assert mh748_risparmio(100.0, 200.0) == -100.0
    assert mh748_risparmio_per_km(308909.097826087, 36500) == pytest.approx(
        8.463262954139369)
    assert mh748_risparmio_per_mwh(308909.097826087, 1095.0) == pytest.approx(
        282.108765137979)
    with pytest.raises(ValueError):
        mh748_risparmio_per_km(100.0, 0)
    with pytest.raises(ValueError):
        mh748_risparmio_per_mwh(100.0, 0)


def test_capex_delta():
    assert mh748_capex_delta(10000000, 1500000, 8000000) == 3500000.0
    assert mh748_capex_delta(10000000, 1500000, 12000000) == -500000.0
    assert mh748_capex_delta(0, 0, 0) == 0.0


def test_crf():
    assert mh748_crf(5.0, 20) == pytest.approx(0.08024258719069129)
    assert mh748_crf(0, 20) == 0.05
    assert mh748_crf(10.0, 10) == pytest.approx(0.16274539488251152)


def test_quota_capex_e_livellato():
    assert mh748_quota_capex(3500000.0, 0.08024258719069129) == pytest.approx(
        280849.0551674195)
    assert mh748_quota_capex(-500000.0, 0.08024258719069129) == pytest.approx(
        -40121.29359534565)
    assert mh748_costo_livellato(479414.402173913, 280849.0551674195) == (
        pytest.approx(760263.4573413325))


def test_costo_per_km():
    assert mh748_costo_per_km(788323.5, 36500) == pytest.approx(
        21.59790410958904)
    with pytest.raises(ValueError):
        mh748_costo_per_km(100.0, 0)


def test_prezzo_pareggio():
    par = mh748_prezzo_pareggio(346750.0, 41573.5, 400000, 250000,
                                15175.271739130434, 1190.2173913043478)
    assert par == pytest.approx(439.54006392694066)
    assert mh748_prezzo_pareggio(100.0, 0, 0, 0, 0, 0) is None


# ---------------------------------------------------------------- flussi/VAN/TIR
def test_flussi_lunghezza_e_primo():
    f = mh748_flussi(3500000.0, 308909.097826087, 20)
    assert len(f) == 21
    assert f[0] == -3500000.0
    assert all(v == 308909.097826087 for v in f[1:])


def test_van_demo_e_zero_wacc():
    f = mh748_flussi(3500000.0, 308909.097826087, 20)
    assert mh748_van(f, 5.0) == pytest.approx(349690.15383295575)
    assert mh748_van([-100.0, 50.0, 50.0], 0) == 0.0


def test_tir_demo_e_casi_none():
    f = mh748_flussi(3500000.0, 308909.097826087, 20)
    assert mh748_tir(f) == pytest.approx(0.06151481017884801)
    assert mh748_tir([100.0, 100.0]) is None
    assert mh748_tir([-100.0, -100.0]) is None


def test_tir_verifica_npv_zero():
    f = mh748_flussi(3500000.0, 308909.097826087, 20)
    r = mh748_tir(f)
    npv = sum(v / (1.0 + r) ** i for i, v in enumerate(f))
    assert abs(npv) < 1.0


def test_payback():
    assert mh748_payback([-3500000.0] + [308909.097826087] * 20) == 12
    assert mh748_payback([-100.0, 10.0, 10.0]) is None
    assert mh748_payback([0.0, 10.0]) == 0
    assert mh748_payback([500000.0, 100.0]) == 0


def test_verdetto():
    assert mh748_verdetto(100.0, 3500000.0, 10.0) == "CONVIENTE"
    assert mh748_verdetto(-50000.0, 3500000.0, 10.0) == "MARGINALE"
    assert mh748_verdetto(-500000.0, 3500000.0, 10.0) == "NON_CONVIENTE"
    assert mh748_verdetto(0.0, 3500000.0, 10.0) == "MARGINALE"
    assert mh748_verdetto(float("nan"), 3500000.0, 10.0) == "NON_CALCOLABILE"
    assert mh748_verdetto(100.0, 3500000.0, 101.0) == "NON_CALCOLABILE"
    assert mh748_verdetto(-350000.0, 3500000.0, 10.0) == "MARGINALE"


# ---------------------------------------------------------------- valida
def test_valida_demo_ok():
    v = mh748_valida(**_demo_kwargs())
    assert v == {"valido": True, "errore": ""}


def test_valida_rifiuta_stringa_nan_inf_bool():
    base = _demo_kwargs()
    for campo, bad in (("distanza_km", "10"), ("distanza_km", float("nan")),
                       ("distanza_km", float("inf")), ("distanza_km", True),
                       ("p_elettrica_eur_mwh", None)):
        d = dict(base)
        d[campo] = bad
        assert mh748_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    base = _demo_kwargs()
    casi = [("distanza_km", 0), ("traversate_anno", 0),
            ("traversate_anno", 10.5), ("consumo_kwh_km", 0),
            ("consumo_l_km", -1), ("eta_ricarica", 0),
            ("eta_ricarica", 1.5), ("sosta_min", 0),
            ("p_elettrica_eur_mwh", -1), ("p_diesel_eur_l", -0.1),
            ("om_diesel_eur_anno", -1), ("f_diesel_kg_l", -1),
            ("f_rete_kg_mwh", -1), ("prezzo_eua_eur_t", -1),
            ("capex_elettrico_eur", -1), ("wacc_pct", 51),
            ("vita_anni", 0), ("tolleranza_pct", 101)]
    for campo, val in casi:
        d = dict(base)
        d[campo] = val
        assert mh748_valida(**d)["valido"] is False, campo


def test_valida_accetta_limiti():
    base = _demo_kwargs()
    d = dict(base)
    d.update({"eta_ricarica": 1.0, "wacc_pct": 0, "tolleranza_pct": 0,
              "p_elettrica_eur_mwh": 0, "capex_elettrico_eur": 0})
    assert mh748_valida(**d)["valido"] is True


# ---------------------------------------------------------------- demo esatta
def test_demo_dict():
    d = mh748_demo()
    assert d["distanza_km"] == 10
    assert d["traversate_anno"] == 3650
    assert d["consumo_kwh_km"] == 30
    assert d["consumo_l_km"] == 5
    assert d["eta_ricarica"] == 0.92
    assert d["sosta_min"] == 20
    assert d["p_elettrica_eur_mwh"] == 180
    assert d["p_diesel_eur_l"] == 1.9
    assert d["om_diesel_eur_anno"] == 400000
    assert d["om_elettrico_eur_anno"] == 250000
    assert d["f_diesel_kg_l"] == 2.68
    assert d["f_rete_kg_mwh"] == 150
    assert d["prezzo_eua_eur_t"] == 85
    assert d["capex_elettrico_eur"] == 10000000
    assert d["capex_ricarica_eur"] == 1500000
    assert d["capex_diesel_eur"] == 8000000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 20
    assert d["tolleranza_pct"] == 10.0


def test_demo_calcoli_fisica():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["errore"] == ""
    assert bc["km_anno"] == 36500.0
    assert bc["e_trazione_mwh"] == 1095.0
    assert bc["e_rete_mwh"] == 1190.2173913043478
    assert bc["litri_diesel"] == 182500.0
    assert bc["e_traversata_mwh"] == 0.3
    assert bc["potenza_ricarica_mw"] == pytest.approx(0.9)
    assert bc["co2_diesel_t"] == 489.1000000000001
    assert bc["co2_elettrica_t"] == 178.53260869565216
    assert bc["co2_evitata_t"] == 310.5673913043479


def test_demo_calcoli_economia():
    bc = demo_calcoli()
    assert bc["costo_diesel_eur"] == 346750.0
    assert bc["costo_co2_diesel_eur"] == 41573.50000000001
    assert bc["costo_energia_elettrica_eur"] == 214239.1304347826
    assert bc["costo_co2_elettrica_eur"] == 15175.271739130434
    assert bc["totale_diesel_eur"] == 788323.5
    assert bc["totale_elettrico_eur"] == 479414.402173913
    assert bc["risparmio_eur_anno"] == 308909.097826087
    assert bc["risparmio_eur_km"] == 8.463262954139369
    assert bc["risparmio_eur_mwh"] == 282.108765137979


def test_demo_calcoli_finanza():
    bc = demo_calcoli()
    assert bc["capex_delta_eur"] == 3500000.0
    assert bc["crf"] == 0.08024258719069129
    assert bc["quota_capex_eur"] == 280849.0551674195
    assert bc["costo_livellato_elettrico_eur"] == 760263.4573413325
    assert bc["costo_livellato_elettrico_eur_km"] == 20.82913581757075
    assert bc["costo_diesel_eur_km"] == 21.59790410958904
    assert bc["van"] == 349690.15383295575
    assert bc["tir"] == 6.151481017884801
    assert bc["payback"] == 12
    assert bc["prezzo_pareggio_eur_mwh"] == 439.54006392694066
    assert bc["verdetto"] == "CONVIENTE"


def test_demo_flussi_e_cumulato():
    bc = demo_calcoli()
    assert len(bc["flussi"]) == 21
    assert bc["flussi"][0] == -3500000.0
    assert bc["flussi"][1] == 308909.097826087
    assert len(bc["df_flussi"]) == 21
    assert bc["df_flussi"].iloc[11]["Cumulato (EUR)"] == pytest.approx(
        -101999.923913043)
    assert bc["df_flussi"].iloc[12]["Cumulato (EUR)"] == pytest.approx(
        206909.173913044)
    assert bc["df_flussi"].iloc[20]["Cumulato (EUR)"] == pytest.approx(
        2678181.95652174)


def test_demo_tabella_righe():
    bc = demo_calcoli()
    assert len(bc["df_tabella"]) == 48
    voci = list(bc["df_tabella"]["Voce"])
    assert "Km annui (km/anno)" in voci
    assert "Potenza ricarica (MW)" in voci
    assert "CAPEX delta (EUR)" in voci
    assert "Verdetto" in voci
    riga = bc["df_tabella"][bc["df_tabella"]["Voce"] == "VAN (EUR)"]
    assert float(riga["Valore"].iloc[0]) == 349690.15383295575


def test_demo_coerenza_interna():
    bc = demo_calcoli()
    assert bc["totale_diesel_eur"] - bc["totale_elettrico_eur"] == (
        pytest.approx(bc["risparmio_eur_anno"]))
    assert bc["co2_diesel_t"] - bc["co2_elettrica_t"] == pytest.approx(
        bc["co2_evitata_t"])
    assert bc["capex_elettrico_eur"] + bc["capex_ricarica_eur"] - (
        bc["capex_diesel_eur"]) == bc["capex_delta_eur"]
    assert bc["totale_elettrico_eur"] + bc["quota_capex_eur"] == (
        pytest.approx(bc["costo_livellato_elettrico_eur"]))
    assert bc["risparmio_eur_anno"] / bc["km_anno"] == pytest.approx(
        bc["risparmio_eur_km"])
    assert bc["risparmio_eur_anno"] / bc["e_trazione_mwh"] == pytest.approx(
        bc["risparmio_eur_mwh"])


def test_demo_crf_solo_nel_livellato_non_nei_flussi():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -bc["capex_delta_eur"]
    van_senza_crf = -bc["capex_delta_eur"] + sum(
        bc["risparmio_eur_anno"] / (1.05 ** t) for t in range(1, 21))
    assert bc["van"] == pytest.approx(van_senza_crf)


# ---------------------------------------------------------------- varianti
def test_variante_capex_alto_non_conviente():
    v = _variante(capex_elettrico_eur=14000000)
    assert v["capex_delta_eur"] == 7500000.0
    assert v["van"] == pytest.approx(-3650309.846167044)
    assert v["verdetto"] == "NON_CONVIENTE"
    assert v["payback"] is None


def test_variante_marginale():
    v = _variante(capex_elettrico_eur=10400000)
    assert v["capex_delta_eur"] == 3900000.0
    assert v["van"] == pytest.approx(-50309.846167044234)
    assert v["verdetto"] == "MARGINALE"
    assert v["payback"] == 13
    assert v["tir"] == pytest.approx(4.8473775005888315)


def test_variante_prezzo_elettrico_alto_non_conviente():
    v = _variante(p_elettrica_eur_mwh=290)
    assert v["risparmio_eur_anno"] == pytest.approx(177985.18478260865)
    assert v["van"] == pytest.approx(-1281911.189383285)
    assert v["verdetto"] == "NON_CONVIENTE"


def test_variante_rete_sporca_co2_negativa_ma_calcolabile():
    v = _variante(f_rete_kg_mwh=800)
    assert v["valid"] is True
    assert v["co2_elettrica_t"] == pytest.approx(952.1739130434781)
    assert v["co2_evitata_t"] == pytest.approx(-463.07391304347806)
    assert v["risparmio_eur_anno"] == pytest.approx(243149.58695652173)
    assert v["van"] == pytest.approx(-469818.7026461101)
    assert v["verdetto"] == "NON_CONVIENTE"


def test_variante_eta_uno():
    v = _variante(eta_ricarica=1.0)
    assert v["e_rete_mwh"] == 1095.0
    assert v["totale_elettrico_eur"] == 461061.25
    assert v["risparmio_eur_anno"] == 327262.25
    assert v["van"] == pytest.approx(578410.9966729056)
    assert v["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero():
    v = _variante(wacc_pct=0)
    assert v["crf"] == 0.05
    assert v["quota_capex_eur"] == 175000.0
    assert v["costo_livellato_elettrico_eur"] == pytest.approx(
        654414.4021739131)
    assert v["van"] == pytest.approx(2678181.956521739)
    assert v["verdetto"] == "CONVIENTE"


def test_variante_sosta_corta_piu_potenza():
    v = _variante(sosta_min=10)
    assert v["potenza_ricarica_mw"] == pytest.approx(1.8)
    v2 = _variante(sosta_min=60)
    assert v2["potenza_ricarica_mw"] == pytest.approx(0.3)


def test_variante_delta_negativo_payback_zero():
    v = _variante(capex_diesel_eur=12000000)
    assert v["capex_delta_eur"] == -500000.0
    assert v["payback"] == 0
    assert v["van"] == pytest.approx(4349690.153832957)
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
    assert v["flussi"] == [-3500000.0, 308909.097826087]
    assert v["payback"] is None
    assert v["van"] == pytest.approx(-3205800.8592132507)


def test_variante_diesel_economico_ma_non_degenere():
    v = _variante(p_diesel_eur_l=1.2)
    assert v["valid"] is True
    assert v["verdetto"] == "NON_CONVIENTE"


# ---------------------------------------------------------------- degeneri
def test_degenere_pareggio_esatto():
    v = _variante(p_elettrica_eur_mwh=439.54006392694066)
    assert v["valid"] is False
    assert v["verdetto"] == "NON_CALCOLABILE"
    assert "nullo o negativo" in v["errore"]
    assert v["flussi"] == []
    assert v["tir"] is None
    assert v["payback"] is None
    assert v["prezzo_pareggio_eur_mwh"] is None


def test_degenere_elettrico_caro():
    v = _variante(p_elettrica_eur_mwh=600)
    assert v["valid"] is False
    assert v["verdetto"] == "NON_CALCOLABILE"
    assert v["van"] == 0.0
    assert len(v["df_flussi"]) == 0
    assert len(v["df_tabella"]) == 0


def test_degenere_distanza_zero():
    v = _variante(distanza_km=0)
    assert v["valid"] is False
    assert v["verdetto"] == "NON_CALCOLABILE"
    assert v["km_anno"] == 0.0


def test_degenere_traversate_zero_e_frazionarie():
    assert _variante(traversate_anno=0)["valid"] is False
    assert _variante(traversate_anno=10.5)["valid"] is False


def test_degenere_eta_fuori_range():
    assert _variante(eta_ricarica=0)["valid"] is False
    assert _variante(eta_ricarica=1.5)["valid"] is False


def test_degenere_sosta_zero_consumi_zero():
    assert _variante(sosta_min=0)["valid"] is False
    assert _variante(consumo_kwh_km=0)["valid"] is False
    assert _variante(consumo_l_km=0)["valid"] is False


def test_degenere_wacc_vita_tolleranza():
    assert _variante(wacc_pct=60)["valid"] is False
    assert _variante(wacc_pct=-1)["valid"] is False
    assert _variante(vita_anni=0)["valid"] is False
    assert _variante(tolleranza_pct=101)["valid"] is False


def test_degenere_stringa_nan_inf():
    assert _variante(p_diesel_eur_l="1.9")["valid"] is False
    assert _variante(p_elettrica_eur_mwh=float("nan"))["valid"] is False
    assert _variante(capex_diesel_eur=float("inf"))["valid"] is False
    assert _variante(distanza_km=True)["valid"] is False


def test_degenere_neutro_campi():
    v = _variante(distanza_km=-5)
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


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = demo_calcoli()
    csv = mh748_csv(bc, mh748_demo())
    righe = csv.strip().split("\n")
    assert righe[0] == "voce;valore"
    assert any(r.startswith("km_anno;36500.0") for r in righe)
    assert any(r.startswith("verdetto;CONVIENTE") for r in righe)
    assert any(r.startswith("potenza_ricarica_mw;") for r in righe)
    assert any(r.startswith("capex_delta_eur;3500000.0") for r in righe)
    assert len(righe) == 49


def test_csv_valori_coerenti_con_calcola():
    bc = demo_calcoli()
    csv = mh748_csv(bc, mh748_demo())
    assert "van_eur;349690.15383295575" in csv
    assert "tir_pct;6.151481017884801" in csv
    assert "payback_anni;12" in csv
    assert "prezzo_pareggio_eur_mwh;439.54006392694066" in csv


def test_csv_degenere_solo_zeri():
    bc = _variante(p_elettrica_eur_mwh=600)
    csv = mh748_csv(bc, mh748_demo())
    assert "verdetto;NON_CALCOLABILE" in csv
    assert "van_eur;0.0" in csv


# ---------------------------------------------------------------- pareggio
def test_pareggio_verifica_risparmio_zero():
    bc = demo_calcoli()
    par = bc["prezzo_pareggio_eur_mwh"]
    v = _variante(p_elettrica_eur_mwh=par)
    assert v["valid"] is False


def test_pareggio_sotto_demo_risparmio_positivo():
    v = _variante(p_elettrica_eur_mwh=400)
    assert v["valid"] is True
    assert v["risparmio_eur_anno"] > 0
    v2 = _variante(p_elettrica_eur_mwh=500)
    assert v2["valid"] is False


# ---------------------------------------------------------------- misc
def test_calcola_non_sollevela_per_input_numerici():
    for kw in ({"distanza_km": 0}, {"eta_ricarica": 2},
               {"vita_anni": -3}):
        v = _variante(**kw)
        assert v["valid"] is False
        assert v["verdetto"] == "NON_CALCOLABILE"


def test_monotonia_prezzo_elettrico():
    vans = [_variante(p_elettrica_eur_mwh=p)["van"]
            for p in (100, 150, 180, 220)]
    assert vans[0] > vans[1] > vans[2] > vans[3]


def test_monotonia_traversate():
    risp = [_variante(traversate_anno=t)["risparmio_eur_anno"]
            for t in (1000, 2000, 3650)]
    assert risp[0] < risp[1] < risp[2]


def test_scala_distanza_doppia():
    a = _variante(distanza_km=10)
    b = _variante(distanza_km=20)
    assert b["km_anno"] == 2 * a["km_anno"]
    assert b["e_trazione_mwh"] == pytest.approx(2 * a["e_trazione_mwh"])
    assert b["litri_diesel"] == 2 * a["litri_diesel"]


def test_risparmio_lineare_in_prezzo_diesel():
    a = _variante(p_diesel_eur_l=1.9)
    b = _variante(p_diesel_eur_l=2.9)
    assert b["risparmio_eur_anno"] - a["risparmio_eur_anno"] == pytest.approx(
        182500.0)


# ---------------------------------------------------------------- extra (copertura 100+)
@pytest.mark.parametrize("wacc,vita,atteso", [
    (5.0, 20, 0.08024258719069129),
    (0, 10, 0.1),
    (10.0, 10, 0.16274539488251152),
    (5.0, 1, 1.05),
    (50.0, 5, 0.5758293838862559),
])
def test_crf_parametrizzato(wacc, vita, atteso):
    assert mh748_crf(wacc, vita) == pytest.approx(atteso)


@pytest.mark.parametrize("campo,valore", [
    ("distanza_km", 0), ("distanza_km", -3),
    ("traversate_anno", -1), ("consumo_kwh_km", -0.5),
    ("consumo_l_km", 0), ("eta_ricarica", 0), ("eta_ricarica", 2),
    ("sosta_min", -10), ("p_elettrica_eur_mwh", -5),
    ("p_diesel_eur_l", -0.01), ("om_diesel_eur_anno", -100),
    ("om_elettrico_eur_anno", -100), ("f_diesel_kg_l", -2.68),
    ("f_rete_kg_mwh", -150), ("prezzo_eua_eur_t", -85),
    ("capex_elettrico_eur", -1), ("capex_ricarica_eur", -1),
    ("capex_diesel_eur", -1), ("wacc_pct", -0.1),
    ("wacc_pct", 50.1), ("vita_anni", -1), ("vita_anni", 2.5),
    ("tolleranza_pct", -1), ("tolleranza_pct", 100.1),
])
def test_valida_rifiuta_singoli_campi(campo, valore):
    d = _demo_kwargs()
    d[campo] = valore
    assert mh748_valida(**d)["valido"] is False


def test_demo_deterministica_due_chiamate():
    a = demo_calcoli()
    b = demo_calcoli()
    assert a["van"] == b["van"]
    assert a["flussi"] == b["flussi"]
    assert a["tir"] == b["tir"]


def test_verdetto_soglia_tolleranza_esatta():
    assert mh748_verdetto(-350000.0, 3500000.0, 10.0) == "MARGINALE"
    assert mh748_verdetto(-350000.01, 3500000.0, 10.0) == "NON_CONVIENTE"


def test_verdetto_delta_negativo():
    assert mh748_verdetto(-100.0, -500000.0, 10.0) == "MARGINALE"
    assert mh748_verdetto(-60000.0, -500000.0, 10.0) == "NON_CONVIENTE"


def test_flussi_delta_negativo():
    f = mh748_flussi(-500000.0, 308909.097826087, 20)
    assert f[0] == 500000.0
    assert len(f) == 21


def test_van_wacc_50():
    f = [-1000.0, 600.0, 600.0]
    assert mh748_van(f, 50.0) == pytest.approx(-1000.0 + 400.0 + 266.6666666666667)


def test_tir_flusso_semplice():
    assert mh748_tir([-100.0, 110.0]) == pytest.approx(0.1)


def test_tir_nessun_cambio_segno_tutti_positivi():
    assert mh748_tir([10.0, 20.0, 30.0]) is None


def test_payback_cumulato_esatto_zero():
    assert mh748_payback([-100.0, 50.0, 50.0]) == 2
    assert mh748_payback([-100.0, 100.0]) == 1


def test_risparmio_helper_negativo_ammesso():
    assert mh748_risparmio(100.0, 300.0) == -200.0
    assert mh748_risparmio_per_km(-200.0, 1000) == -0.2
    assert mh748_risparmio_per_mwh(-200.0, 50) == -4.0


def test_potenza_ricarica_scala_con_distanza_e_consumo():
    assert mh748_potenza_ricarica(mh748_e_traversata(20, 30), 20) == (
        pytest.approx(1.8))
    assert mh748_potenza_ricarica(mh748_e_traversata(10, 60), 20) == (
        pytest.approx(1.8))


def test_e_rete_maggiore_di_trazione_per_eta_minore_uno():
    assert mh748_e_rete(1000.0, 0.5) == 2000.0
    assert mh748_e_rete(1000.0, 0.8) == 1250.0


def test_df_tabella_valori_demo_selezionati():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Km annui (km/anno)"] == 36500.0
    assert mappa["Litri diesel (L/anno)"] == 182500.0
    assert mappa["Potenza ricarica (MW)"] == pytest.approx(0.9)
    assert mappa["CAPEX delta (EUR)"] == 3500000.0
    assert mappa["Payback (anni)"] == 12
    assert mappa["Verdetto"] == "CONVIENTE"


def test_csv_contiene_tutte_le_chiavi_input():
    bc = demo_calcoli()
    csv = mh748_csv(bc, mh748_demo())
    for chiave in ("distanza_km", "traversate_anno", "consumo_kwh_km",
                   "consumo_l_km", "eta_ricarica", "sosta_min",
                   "p_elettrica_eur_mwh", "p_diesel_eur_l",
                   "om_diesel_eur_anno", "om_elettrico_eur_anno",
                   "f_diesel_kg_l", "f_rete_kg_mwh", "prezzo_eua_eur_t",
                   "capex_elettrico_eur", "capex_ricarica_eur",
                   "capex_diesel_eur", "wacc_pct", "vita_anni",
                   "tolleranza_pct"):
        assert f"\n{chiave};" in csv


def test_demo_chiavi_attese():
    assert set(mh748_demo().keys()) == {
        "distanza_km", "traversate_anno", "consumo_kwh_km",
        "consumo_l_km", "eta_ricarica", "sosta_min",
        "p_elettrica_eur_mwh", "p_diesel_eur_l",
        "om_diesel_eur_anno", "om_elettrico_eur_anno",
        "f_diesel_kg_l", "f_rete_kg_mwh", "prezzo_eua_eur_t",
        "capex_elettrico_eur", "capex_ricarica_eur",
        "capex_diesel_eur", "wacc_pct", "vita_anni",
        "tolleranza_pct"}


def test_calcola_con_float_interi_per_traversate():
    v = _variante(traversate_anno=3650.0)
    assert v["valid"] is True
    assert v["traversate_anno"] == 3650
