"""Test tab750 "Treno regionale a idrogeno: il fuel-cell batte
il diesel sulle linee non elettrificate?"

Nuova tab tab750 (treno
regionale a idrogeno, w751).
Business case deterministico di
un treno regionale fuel-cell
contro un'automotrice diesel
(DMU) sulla stessa linea non
elettrificata, stessi km/anno.
Km annui diretti, consumi per km
(kg H2/km e L diesel/km), H2
annuo da km e consumo H2, litri
diesel da km e consumo diesel,
CO2 da litri e fattore per litro
(diesel) e da kg e fattore per kg
(H2), costi da H2, diesel, O&M e
EUA, CAPEX delta da treno H2 +
stazione di rifornimento meno
treno diesel, VAN, TIR, payback
(primo anno con cumulato >= 0),
autonomia da serbatoio e prezzo
H2 di pareggio.
Distinta dalla tab sul camion
pesante a idrogeno su gomma
(trasporto stradale, non
ferrovia), dal treno FT
Fischer-Tropsch (processo
chimico, non veicolo), dalla tab
sugli elettrolizzatori
(produzione di idrogeno, non
consumo a bordo), dalla tab
sull'idrogeno liquido LH2
(liquefazione, non trazione
ferroviaria) e dalla tab sul
traghetto elettrico (navale, non
ferrovia): qui ferrovia
regionale, stessa linea non
elettrificata, stessi km/anno,
serbatoio in kg e autonomia da
rifornimento.

Demo calcolata eseguendo demo_calcoli()
(e ricontrollata a mano, riga per riga):
treno regionale da 150000 km/anno,
consumo H2 0,30 kg/km e consumo
diesel 0,90 L/km, prezzo H2 6,00
EUR/kg e prezzo diesel 1,80 EUR/L,
O&M H2 130000 EUR/anno e O&M
diesel 110000 EUR/anno, fattore
diesel 2,68 kg/L e fattore H2
0,50 kg/kg, prezzo EUA 85 EUR/t,
CAPEX treno H2 6500000 EUR,
CAPEX rifornimento 1500000 EUR e
CAPEX treno diesel 4500000 EUR,
serbatoio 260 kg, WACC 5 %,
vita 20 anni, tolleranza 10 %
del CAPEX delta.

- h2_anno_kg = 45000.0
- litri_diesel = 135000.0
- costo_h2_eur = 270000.0
- costo_diesel_eur = 243000.0
- co2_diesel_t = 361.8
- co2_h2_t = 22.5
- co2_evitata_t = 339.3
- costo_co2_diesel_eur = 30753.0
- costo_co2_h2_eur = 1912.5
- totale_diesel_eur = 383753.0
- totale_h2_eur = 401912.5
- risparmio_eur_anno = -18159.5
- risparmio_eur_km = -0.12106333333333333
- autonomia_km = 866.6666666666667
- rifornimenti_anno = 173.07692307692307
- capex_delta_eur = 3500000.0
- crf = 0.08024258719069129
- quota_capex_eur = 280849.0551674195
- costo_livellato_h2_eur = 682761.5551674195
- costo_livellato_diesel_eur = 383753.0
- van = -3726307.508715355
- tir = None
- payback = None
- prezzo_pareggio_eur_kg = 5.596455555555556
- verdetto = 'NON_CONVIENTE'

Scomposizione: H2 annuo = 150000 x
0,30 = 45000 kg; litri = 150000 x
0,90 = 135000 L; costo H2 45000 x
6,00 = 270000,00 EUR; costo diesel
135000 x 1,80 = 243000,00 EUR;
CO2 diesel 135000 x 2,68 / 1000 =
361,80 t; CO2 H2 45000 x 0,50 /
1000 = 22,50 t; evitata 339,30 t;
costo CO2 diesel 361,80 x 85 =
30753,00 EUR; costo CO2 H2 22,50
x 85 = 1912,50 EUR; totale diesel
243000,00 + 30753,00 + 110000 =
383753,00 EUR; totale H2 270000,00
+ 1912,50 + 130000 = 401912,50 EUR;
risparmio 383753,00 - 401912,50 =
-18159,50 EUR/anno = -0,1211
EUR/km; autonomia 260 / 0,30 =
866,67 km; rifornimenti 150000 /
866,67 = 173,08 all'anno; CAPEX
delta 6500000 + 1500000 - 4500000
= 3500000 EUR; CRF 0,05 x 1,05^20 /
(1,05^20 - 1) = 0.08024258719069129;
quota CAPEX 3500000 x 0,080243 =
280849,06 EUR/anno; costo livellato
H2 401912,50 + 280849,06 =
682761,56 EUR/anno contro 383753,00
EUR/anno del diesel; flussi: anno 0
-3500000, anni 1-20 risparmio
-18159,50 (piatti, negativi); VAN
-3500000 - 18159,50 x 12,46221034
(annuita' 20 anni al 5 %) =
-3726307,51 EUR; TIR None (flussi
tutti negativi: nessun cambio di
segno); payback mai (il cumulato
scende sempre: anno 20 a
-3863190,00 EUR); prezzo H2 di
pareggio (243000,00 + 30753,00 +
110000 - 130000 - 1912,50) / 45000
= 5.596455555555556 EUR/kg;
verdetto NON_CONVIENTE perche'
VAN < 0 e |VAN| = 3726307,51 >
10 % di 3500000 = 350000.
NOTA: il CRF entra solo nel costo
livellato, mai nei flussi: il CAPEX
delta compare una sola volta,
all'anno 0. NOTA 2: in questo brief
il risparmio nullo o negativo NON
e' degenere: la demo stessa ha
risparmio negativo ed e' calcolabile
(valid=True, NON_CONVIENTE, payback
mai, TIR None). NOTA 3: la CO2
evitata negativa NON e' degenere
di per se': se il risparmio resta
> 0 il caso resta calcolabile e la
CO2 evitata negativa va detta
(fattore H2 10 kg/kg: CO2 H2 450 t,
evitata -88,20 t, valid=True). NOTA 4:
il prezzo di pareggio segue la
formula del brief (vedi
test_prezzo_pareggio): con gli input
demo vale 5,5965 EUR/kg, non 7,82:
7,82 non si ottiene dalla formula
del brief con questi input
(numeratore 251840,50 / 45000 =
5,5965), quindi il test asserisce
il valore della formula.
"""

import ast
import math
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w751_helpers import (
    demo_calcoli,
    mh750_autonomia,
    mh750_calcola,
    mh750_capex_delta,
    mh750_co2_diesel,
    mh750_co2_evitata,
    mh750_co2_h2,
    mh750_costo_co2,
    mh750_costo_diesel,
    mh750_costo_h2,
    mh750_costo_livellato,
    mh750_costo_totale,
    mh750_crf,
    mh750_csv,
    mh750_demo,
    mh750_flussi,
    mh750_h2_anno,
    mh750_int_nneg,
    mh750_int_pos,
    mh750_litri_diesel,
    mh750_nneg,
    mh750_num,
    mh750_pct_0_100,
    mh750_pct_wacc,
    mh750_pos,
    mh750_prezzo_pareggio,
    mh750_quota_capex,
    mh750_rifornimenti,
    mh750_risparmio,
    mh750_risparmio_per_km,
    mh750_tir,
    mh750_valida,
    mh750_van,
    mh750_verdetto,
    mh750_payback,
)


def _demo_kwargs():
    return dict(mh750_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh750_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh750_num(3, "x") == 3.0
    assert mh750_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh750_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh750_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh750_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh750_pos(0, "x")
    with pytest.raises(ValueError):
        mh750_pos(-1, "x")
    assert mh750_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh750_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh750_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh750_int_pos(0, "x")


def test_int_nneg_zero_ok():
    assert mh750_int_nneg(0, "x") == 0
    with pytest.raises(ValueError):
        mh750_int_nneg(-1, "x")


def test_pct_0_100_limiti():
    assert mh750_pct_0_100(0, "x") == 0.0
    assert mh750_pct_0_100(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh750_pct_0_100(100.1, "x")
    with pytest.raises(ValueError):
        mh750_pct_0_100(-1, "x")


def test_pct_wacc_limiti():
    assert mh750_pct_wacc(0, "x") == 0.0
    assert mh750_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh750_pct_wacc(50.1, "x")


# ---------------------------------------------------------------- fisica base
def test_h2_anno():
    assert mh750_h2_anno(150000, 0.3) == 45000.0
    assert mh750_h2_anno(0, 0.3) == 0.0
    with pytest.raises(ValueError):
        mh750_h2_anno(150000, 0)


def test_litri_diesel():
    assert mh750_litri_diesel(150000, 0.9) == 135000.0
    assert mh750_litri_diesel(0, 0.9) == 0.0


def test_costi_h2_e_diesel():
    assert mh750_costo_h2(45000.0, 6.0) == 270000.0
    assert mh750_costo_diesel(135000.0, 1.8) == 243000.0
    assert mh750_costo_h2(0.0, 6.0) == 0.0


def test_co2_diesel_h2_evitata():
    assert mh750_co2_diesel(135000.0, 2.68) == 361.8
    assert mh750_co2_h2(45000.0, 0.5) == 22.5
    assert mh750_co2_evitata(361.8, 22.5) == pytest.approx(339.3)
    assert mh750_co2_h2(45000.0, 0.0) == 0.0


def test_co2_evitata_segno_libero():
    assert mh750_co2_evitata(361.8, 450.0) == pytest.approx(-88.2)


def test_costo_co2_e_totale():
    assert mh750_costo_co2(361.8, 85) == pytest.approx(30753.0)
    assert mh750_costo_co2(22.5, 85) == 1912.5
    assert mh750_costo_totale(243000.0, 110000, 30753.0) == 383753.0
    assert mh750_costo_totale(270000.0, 130000, 1912.5) == 401912.5


def test_risparmio_e_per_km():
    assert mh750_risparmio(383753.0, 401912.5) == -18159.5
    assert mh750_risparmio_per_km(-18159.5, 150000) == pytest.approx(
        -0.12106333333333333)
    with pytest.raises(ValueError):
        mh750_risparmio_per_km(-18159.5, 0)


def test_autonomia_e_rifornimenti():
    assert mh750_autonomia(260, 0.3) == pytest.approx(866.6666666666667)
    assert mh750_autonomia(260, 0) is None
    assert mh750_autonomia(260, -0.1) is None
    assert mh750_autonomia(0, 0.3) == 0.0
    assert mh750_rifornimenti(150000, 866.6666666666667) == pytest.approx(
        173.07692307692307)
    assert mh750_rifornimenti(150000, None) is None
    assert mh750_rifornimenti(150000, 0) is None
    assert mh750_rifornimenti(0, 866.6666666666667) == 0.0


# ---------------------------------------------------------------- finanza base
def test_capex_delta():
    assert mh750_capex_delta(6500000, 1500000, 4500000) == 3500000
    assert mh750_capex_delta(6500000, 1500000, 9000000) == -1000000
    assert mh750_capex_delta(0, 0, 0) == 0


def test_crf():
    assert mh750_crf(5.0, 20) == pytest.approx(0.08024258719069129)
    assert mh750_crf(0, 20) == 0.05
    assert mh750_crf(5.0, 1) == pytest.approx(1.05)


def test_quota_capex_e_livellato():
    assert mh750_quota_capex(3500000, 0.08024258719069129) == pytest.approx(
        280849.0551674195)
    assert mh750_costo_livellato(401912.5, 280849.0551674195) == pytest.approx(
        682761.5551674195)
    assert mh750_costo_livellato(401912.5, 0.0) == 401912.5


def test_prezzo_pareggio_formula_brief():
    assert mh750_prezzo_pareggio(243000.0, 30753.0, 110000, 130000,
                                 1912.5, 45000.0) == pytest.approx(
        5.596455555555556)
    assert mh750_prezzo_pareggio(243000.0, 30753.0, 110000, 130000,
                                 1912.5, 0) is None
    assert mh750_prezzo_pareggio(0.0, 0.0, 0, 0, 0.0, 45000.0) == 0.0


def test_flussi_lunghezza_e_primo():
    fl = mh750_flussi(3500000, -18159.5, 20)
    assert len(fl) == 21
    assert fl[0] == -3500000
    assert all(f == -18159.5 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = demo_calcoli()
    assert bc["van"] == pytest.approx(-3726307.508715355)
    assert mh750_van([-3500000] + [-18159.5] * 20, 0) == -3863190.0
    assert mh750_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo_none_e_conviente():
    bc = demo_calcoli()
    assert bc["tir"] is None
    assert mh750_tir([-3500000] + [-18159.5] * 20) is None
    tir = mh750_tir([-1000000] + [116840.5] * 20)
    assert tir is not None
    assert 0.09 < tir < 0.11
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-1000000] + [116840.5] * 20))
    assert npv == pytest.approx(0.0, abs=1e-4)


def test_payback():
    assert mh750_payback([-3500000] + [-18159.5] * 20) is None
    assert mh750_payback([-1000000] + [116840.5] * 20) == 9
    assert mh750_payback([1000000] + [-18159.5] * 20) == 0
    assert mh750_payback([0] + [-18159.5] * 20) == 0
    assert mh750_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh750_verdetto(100.0, 3500000, 10.0) == "CONVIENTE"
    assert mh750_verdetto(-48628.63, 1000000, 10.0) == "MARGINALE"
    assert mh750_verdetto(-3726307.51, 3500000, 10.0) == "NON_CONVIENTE"
    assert mh750_verdetto(-100000.0, 1000000, 10.0) == "MARGINALE"
    assert mh750_verdetto(-100000.01, 1000000, 10.0) == "NON_CONVIENTE"
    assert mh750_verdetto(float("nan"), 3500000, 10.0) == "NON_CALCOLABILE"
    assert mh750_verdetto(0.0, 0, 10.0) == "MARGINALE"


def test_valida_demo_ok():
    v = mh750_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("km_anno", "150000"), ("km_anno", float("nan")),
                       ("km_anno", float("inf")), ("km_anno", True),
                       ("prezzo_h2_eur_kg", None)):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh750_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("km_anno", 0), ("consumo_h2_kg_km", 0),
                          ("consumo_diesel_L_km", -0.1),
                          ("prezzo_h2_eur_kg", -1),
                          ("prezzo_diesel_eur_l", -0.01),
                          ("om_h2_eur_anno", -100),
                          ("om_diesel_eur_anno", -100),
                          ("f_diesel_kg_l", -2.68),
                          ("f_h2_kg_kg", -0.5),
                          ("prezzo_eua_eur_t", -85),
                          ("capex_h2_eur", -1),
                          ("capex_rifornimento_eur", -1),
                          ("capex_diesel_eur", -1),
                          ("serbatoio_kg", -10),
                          ("wacc_pct", -0.1), ("wacc_pct", 50.1),
                          ("vita_anni", 0), ("vita_anni", 2.5),
                          ("tolleranza_pct", -1),
                          ("tolleranza_pct", 100.1)):
        d = _demo_kwargs()
        d[campo] = valore
        assert mh750_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"prezzo_h2_eur_kg": 0, "om_h2_eur_anno": 0,
              "f_h2_kg_kg": 0, "prezzo_eua_eur_t": 0,
              "capex_h2_eur": 0, "capex_rifornimento_eur": 0,
              "capex_diesel_eur": 0, "serbatoio_kg": 0,
              "wacc_pct": 0, "tolleranza_pct": 0})
    assert mh750_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    assert mh750_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh750_demo()
    assert d["km_anno"] == 150000
    assert d["consumo_h2_kg_km"] == 0.3
    assert d["consumo_diesel_L_km"] == 0.9
    assert d["prezzo_h2_eur_kg"] == 6.0
    assert d["prezzo_diesel_eur_l"] == 1.8
    assert d["om_h2_eur_anno"] == 130000
    assert d["om_diesel_eur_anno"] == 110000
    assert d["f_diesel_kg_l"] == 2.68
    assert d["f_h2_kg_kg"] == 0.5
    assert d["prezzo_eua_eur_t"] == 85
    assert d["capex_h2_eur"] == 6500000
    assert d["capex_rifornimento_eur"] == 1500000
    assert d["capex_diesel_eur"] == 4500000
    assert d["serbatoio_kg"] == 260
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 20
    assert d["tolleranza_pct"] == 10.0


def test_demo_calcoli_fisica():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["h2_anno_kg"] == 45000.0
    assert bc["litri_diesel"] == 135000.0
    assert bc["autonomia_km"] == pytest.approx(866.6666666666667)
    assert bc["rifornimenti_anno"] == pytest.approx(173.07692307692307)
    assert bc["co2_diesel_t"] == 361.8
    assert bc["co2_h2_t"] == 22.5
    assert bc["co2_evitata_t"] == pytest.approx(339.3)


def test_demo_calcoli_economia():
    bc = demo_calcoli()
    assert bc["costo_h2_eur"] == 270000.0
    assert bc["costo_diesel_eur"] == 243000.0
    assert bc["costo_co2_diesel_eur"] == pytest.approx(30753.0)
    assert bc["costo_co2_h2_eur"] == 1912.5
    assert bc["totale_diesel_eur"] == 383753.0
    assert bc["totale_h2_eur"] == 401912.5
    assert bc["risparmio_eur_anno"] == -18159.5
    assert bc["risparmio_eur_km"] == pytest.approx(-0.12106333333333333)
    assert bc["prezzo_pareggio_eur_kg"] == pytest.approx(5.596455555555556)


def test_demo_calcoli_finanza():
    bc = demo_calcoli()
    assert bc["capex_delta_eur"] == 3500000.0
    assert bc["crf"] == pytest.approx(0.08024258719069129)
    assert bc["quota_capex_eur"] == pytest.approx(280849.0551674195)
    assert bc["costo_livellato_h2_eur"] == pytest.approx(682761.5551674195)
    assert bc["costo_livellato_diesel_eur"] == 383753.0
    assert bc["van"] == pytest.approx(-3726307.508715355)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_demo_flussi_e_cumulato():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -3500000
    assert len(bc["flussi"]) == 21
    assert all(f == -18159.5 for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -3500000
    assert righe.iloc[20]["Cumulato (EUR)"] == -3863190.0
    assert righe.iloc[20]["Flusso (EUR/anno)"] == -18159.5


def test_demo_tabella_righe():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["H2 annuo (kg/anno)"] == 45000.0
    assert mappa["Litri diesel (L/anno)"] == 135000.0
    assert mappa["Autonomia (km)"] == pytest.approx(866.6666666666667)
    assert mappa["CAPEX delta (EUR)"] == 3500000.0
    assert mappa["Payback (anni)"] is None
    assert mappa["Verdetto"] == "NON_CONVIENTE"
    assert mappa["Prezzo H2 di pareggio (EUR/kg)"] == pytest.approx(
        5.596455555555556)


def test_demo_coerenza_interna():
    bc = demo_calcoli()
    assert bc["totale_diesel_eur"] - bc["totale_h2_eur"] == pytest.approx(
        bc["risparmio_eur_anno"])
    assert bc["co2_diesel_t"] - bc["co2_h2_t"] == pytest.approx(
        bc["co2_evitata_t"])
    assert bc["risparmio_eur_anno"] / bc["km_anno"] == pytest.approx(
        bc["risparmio_eur_km"])
    assert bc["serbatoio_kg"] / bc["consumo_h2_kg_km"] == pytest.approx(
        bc["autonomia_km"])
    assert bc["km_anno"] / bc["autonomia_km"] == pytest.approx(
        bc["rifornimenti_anno"])
    assert bc["capex_delta_eur"] * bc["crf"] == pytest.approx(
        bc["quota_capex_eur"])
    assert bc["totale_h2_eur"] + bc["quota_capex_eur"] == pytest.approx(
        bc["costo_livellato_h2_eur"])
    assert bc["costo_livellato_diesel_eur"] == bc["totale_diesel_eur"]


def test_demo_crf_solo_nel_livellato_non_nei_flussi():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -bc["capex_delta_eur"]
    assert all(f == bc["risparmio_eur_anno"] for f in bc["flussi"][1:])
    assert bc["crf"] not in bc["flussi"]
    assert bc["quota_capex_eur"] not in bc["flussi"]
    van_da_flussi = mh750_van(bc["flussi"], bc["wacc_pct"])
    assert van_da_flussi == pytest.approx(bc["van"])
    assert bc["costo_livellato_h2_eur"] == pytest.approx(
        bc["totale_h2_eur"] + bc["capex_delta_eur"] * bc["crf"])


def test_demo_contro_riconteggio_indipendente():
    km, ch, cd = 150000, 0.3, 0.9
    ph, pd = 6.0, 1.8
    omh, omd = 130000, 110000
    fd, fh, eua = 2.68, 0.5, 85
    cxh, cxr, cxd = 6500000, 1500000, 4500000
    se, wacc, vita = 260, 5.0, 20
    ha = km * ch
    li = km * cd
    co2d = li * fd / 1000.0
    co2h = ha * fh / 1000.0
    td = li * pd + omd + co2d * eua
    th = ha * ph + omh + co2h * eua
    risp = td - th
    delta = cxh + cxr - cxd
    r = wacc / 100.0
    crf = r * (1 + r) ** vita / ((1 + r) ** vita - 1)
    van = -delta + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    bc = demo_calcoli()
    assert bc["h2_anno_kg"] == ha
    assert bc["litri_diesel"] == li
    assert bc["totale_diesel_eur"] == td
    assert bc["totale_h2_eur"] == th
    assert bc["risparmio_eur_anno"] == risp
    assert bc["autonomia_km"] == se / ch
    assert bc["rifornimenti_anno"] == km / (se / ch)
    assert bc["crf"] == pytest.approx(crf)
    assert bc["van"] == pytest.approx(van)
    assert bc["prezzo_pareggio_eur_kg"] == pytest.approx(
        (li * pd + co2d * eua + omd - omh - co2h * eua) / ha)


def test_demo_riconteggio_crf_van_payback_pareggio_a_mano():
    bc = demo_calcoli()
    r = 0.05
    annuita = (1 - (1 + r) ** -20) / r
    assert annuita == pytest.approx(12.462210342976)
    assert bc["van"] == pytest.approx(-3500000 - 18159.5 * annuita)
    assert bc["prezzo_pareggio_eur_kg"] == pytest.approx(
        251840.5 / 45000.0)
    assert bc["flussi"][0] + 20 * bc["flussi"][1] == -3863190.0


# ---------------------------------------------------------------- varianti
def test_variante_prezzo_h2_basso():
    bc = _variante(prezzo_h2_eur_kg=4.0)
    assert bc["risparmio_eur_anno"] == 71840.5
    assert bc["van"] == pytest.approx(-2604708.5778867565)
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_variante_prezzo_h2_3():
    bc = _variante(prezzo_h2_eur_kg=3.0)
    assert bc["risparmio_eur_anno"] == 116840.5
    assert bc["van"] == pytest.approx(-2043909.1124724573)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_eua_alto():
    bc = _variante(prezzo_eua_eur_t=150)
    assert bc["risparmio_eur_anno"] == 3895.0
    assert bc["van"] == pytest.approx(-3451459.6907158066)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_capex_diesel_alto():
    bc = _variante(capex_diesel_eur=6500000)
    assert bc["capex_delta_eur"] == 1500000
    assert bc["van"] == pytest.approx(-1726307.5087153548)


def test_variante_om_h2_basso():
    bc = _variante(om_h2_eur_anno=80000)
    assert bc["risparmio_eur_anno"] == 31840.5
    assert bc["van"] == pytest.approx(-3103196.9915883555)


def test_variante_h2_verde_fattore_zero():
    bc = _variante(f_h2_kg_kg=0.0)
    assert bc["co2_h2_t"] == 0.0
    assert bc["co2_evitata_t"] == 361.8
    assert bc["risparmio_eur_anno"] == -16247.0
    assert bc["van"] == pytest.approx(-3702473.531435247)


def test_variante_km_alti():
    bc = _variante(km_anno=250000)
    assert bc["h2_anno_kg"] == 75000.0
    assert bc["litri_diesel"] == 225000.0
    assert bc["risparmio_eur_anno"] == -16932.5
    assert bc["co2_evitata_t"] == 565.5


def test_variante_marginale_ad_hoc():
    bc = _variante(capex_diesel_eur=7000000, prezzo_h2_eur_kg=3.9)
    assert bc["capex_delta_eur"] == 1000000
    assert bc["risparmio_eur_anno"] == 76340.5
    assert bc["van"] == pytest.approx(-48628.631345326554)
    assert bc["van"] < 0.0
    assert abs(bc["van"]) <= 0.10 * 1000000
    assert bc["verdetto"] == "MARGINALE"


def test_variante_conviente_ad_hoc():
    bc = _variante(capex_diesel_eur=7000000, prezzo_h2_eur_kg=3.0)
    assert bc["capex_delta_eur"] == 1000000
    assert bc["risparmio_eur_anno"] == 116840.5
    assert bc["van"] == pytest.approx(456090.88752754265)
    assert bc["tir"] is not None
    assert 9.0 < bc["tir"] < 11.0
    assert bc["payback"] == 9
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_risparmio_negativo_calcolabile_non_degenere():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] < 0.0
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["payback"] is None
    assert bc["tir"] is None


def test_variante_co2_negativa_ma_calcolabile():
    bc = _variante(f_h2_kg_kg=10.0)
    assert bc["co2_h2_t"] == 450.0
    assert bc["co2_evitata_t"] == pytest.approx(-88.2)
    assert bc["valid"] is True


def test_variante_pareggio_azzera_risparmio():
    bc = _variante(prezzo_h2_eur_kg=5.596455555555556)
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["prezzo_pareggio_eur_kg"] == pytest.approx(5.596455555555556)


def test_variante_wacc_zero():
    bc = _variante(wacc_pct=0)
    assert bc["crf"] == 0.05
    assert bc["quota_capex_eur"] == 175000.0
    assert bc["costo_livellato_h2_eur"] == 576912.5
    assert bc["van"] == -3863190.0
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_serbatoio_zero():
    bc = _variante(serbatoio_kg=0)
    assert bc["valid"] is True
    assert bc["autonomia_km"] == 0.0
    assert bc["rifornimenti_anno"] is None


def test_variante_delta_negativo_payback_zero():
    bc = _variante(capex_diesel_eur=9000000)
    assert bc["capex_delta_eur"] == -1000000
    assert bc["flussi"][0] == 1000000
    assert bc["payback"] == 0


def test_variante_delta_zero_payback_zero_tir_none():
    bc = _variante(capex_diesel_eur=8000000)
    assert bc["capex_delta_eur"] == 0
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None


def test_variante_vita_uno():
    bc = _variante(vita_anni=1)
    assert len(bc["flussi"]) == 2
    assert bc["crf"] == pytest.approx(1.05)


# ---------------------------------------------------------------- degenere
def test_degenere_km_zero():
    bc = _variante(km_anno=0)
    assert bc["valid"] is False
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"] == []
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_kg"] is None
    assert bc["errore"]


def test_degenere_consumi_zero():
    bc = _variante(consumo_h2_kg_km=0)
    assert bc["valid"] is False
    assert bc["verdetto"] == "NON_CALCOLABILE"
    bc = _variante(consumo_diesel_L_km=0)
    assert bc["valid"] is False
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_consumi_negativi():
    bc = _variante(consumo_h2_kg_km=-0.1)
    assert bc["valid"] is False
    bc = _variante(consumo_diesel_L_km=-0.5)
    assert bc["valid"] is False


def test_degenere_wacc_vita_tolleranza():
    for kw in ({"wacc_pct": -1}, {"wacc_pct": 60},
               {"vita_anni": 0}, {"vita_anni": 2.5},
               {"tolleranza_pct": -1}, {"tolleranza_pct": 101}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_stringa_nan_inf():
    for kw in ({"km_anno": "150000"}, {"km_anno": float("nan")},
               {"prezzo_h2_eur_kg": float("inf")},
               {"capex_h2_eur": True}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_neutro_campi():
    bc = _variante(km_anno=0)
    assert bc["h2_anno_kg"] == 0.0
    assert bc["litri_diesel"] == 0.0
    assert bc["totale_diesel_eur"] == 0.0
    assert bc["totale_h2_eur"] == 0.0
    assert bc["risparmio_eur_anno"] == 0.0
    assert bc["risparmio_eur_km"] is None
    assert bc["autonomia_km"] is None
    assert bc["rifornimenti_anno"] is None
    assert bc["van"] == 0.0
    assert list(bc["df_flussi"].columns) == [
        "Anno", "Flusso (EUR/anno)", "Cumulato (EUR)"]
    assert list(bc["df_tabella"].columns) == ["Voce", "Valore"]


def test_pareggio_none_quando_h2_zero():
    assert mh750_prezzo_pareggio(243000.0, 30753.0, 110000, 130000,
                                 1912.5, 0) is None


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = demo_calcoli()
    testo = mh750_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert "h2_anno_kg;45000.0" in testo
    assert "verdetto;NON_CONVIENTE" in testo
    assert "prezzo_pareggio_eur_kg" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = demo_calcoli()
    testo = mh750_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"capex_delta_eur;{bc['capex_delta_eur']}" in testo
    assert f"autonomia_km;{bc['autonomia_km']}" in testo


def test_csv_degenere_solo_zeri():
    bc = _variante(km_anno=0)
    testo = mh750_csv(bc, _demo_kwargs())
    assert "van_eur;0.0" in testo
    assert "h2_anno_kg;0.0" in testo
    assert "verdetto;NON_CALCOLABILE" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = demo_calcoli()
    testo = mh750_csv(bc, _demo_kwargs())
    for chiave in _demo_kwargs():
        assert f"{chiave};" in testo


def test_calcola_non_sollevela_per_input_numerici():
    bc = _variante(prezzo_h2_eur_kg=0, prezzo_diesel_eur_l=0,
                   om_h2_eur_anno=0, f_h2_kg_kg=0, prezzo_eua_eur_t=0)
    assert bc["valid"] is True
    assert bc["costo_h2_eur"] == 0.0
    assert bc["costo_diesel_eur"] == 0.0


def test_monotonia_prezzo_h2():
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(prezzo_h2_eur_kg=8.0)["risparmio_eur_anno"]
    basso = _variante(prezzo_h2_eur_kg=4.0)["risparmio_eur_anno"]
    assert alto < base < basso
    assert basso - base == pytest.approx(90000.0)


def test_scala_km_doppia():
    base = demo_calcoli()
    doppio = _variante(km_anno=300000)
    assert doppio["h2_anno_kg"] == 2 * base["h2_anno_kg"]
    assert doppio["litri_diesel"] == 2 * base["litri_diesel"]
    assert doppio["risparmio_eur_anno"] == pytest.approx(-16319.0)


def test_demo_deterministica_due_chiamate():
    a = demo_calcoli()
    b = demo_calcoli()
    assert a["van"] == b["van"]
    assert a["flussi"] == b["flussi"]
    assert a["tir"] == b["tir"]


def test_demo_chiavi_attese():
    assert set(mh750_demo().keys()) == {
        "km_anno", "consumo_h2_kg_km", "consumo_diesel_L_km",
        "prezzo_h2_eur_kg", "prezzo_diesel_eur_l",
        "om_h2_eur_anno", "om_diesel_eur_anno",
        "f_diesel_kg_l", "f_h2_kg_kg", "prezzo_eua_eur_t",
        "capex_h2_eur", "capex_rifornimento_eur",
        "capex_diesel_eur", "serbatoio_kg",
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
    ast.parse(_leggi("w751_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w751_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab750:")


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    # token vietati costruiti per concatenazione, cosi' questo
    # stesso file non li contiene come sottostringhe contigue.
    src = _leggi("w751_helpers.py")
    vietati = ["mh" + "74" + "9", "st" + "74" + "9",
               "tab" + "74" + "9", "74" + "9"]
    assert "streamlit" not in src
    assert all(t not in src for t in vietati)


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w751_ui.py")
    vietati = ["mh" + "74" + "9", "st" + "74" + "9",
               "tab" + "74" + "9", "74" + "9"]
    assert all(t not in src for t in vietati)
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st750_") for c in chiavi)
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
    src = _leggi("w751_test.py")
    vietati = ["mh" + "74" + "9", "st" + "74" + "9",
               "tab" + "74" + "9", "74" + "9"]
    assert all(t not in src for t in vietati)


def test_ui_chiavi_demo_coerenti():
    """Ogni _def750[...] letto dalla UI esiste nel dict demo:
    sweep anti-KeyError a render (lezione tab674)."""
    src = _leggi("w751_ui.py")
    usate = set(re.findall(r'_def750\["([^"]+)"\]', src))
    assert usate
    assert usate <= set(mh750_demo().keys())


def test_ui_riferisce_solo_helper_nuovi():
    src = _leggi("w751_ui.py")
    usati = set(re.findall(r'\b(mh\d+_\w+)\b', src))
    assert usati
    assert all(u.startswith("mh750_") for u in usati)


@pytest.mark.parametrize("wacc,vita,atteso", [
    (5.0, 20, 0.08024258719069129),
    (0, 20, 0.05),
    (10.0, 10, 0.16274539488251152),
    (5.0, 1, 1.05),
    (50.0, 5, 0.5758293838862559),
])
def test_crf_parametrizzato(wacc, vita, atteso):
    assert mh750_crf(wacc, vita) == pytest.approx(atteso)


@pytest.mark.parametrize("campo,valore", [
    ("km_anno", 0), ("km_anno", -3),
    ("consumo_h2_kg_km", -0.5), ("consumo_diesel_L_km", 0),
    ("prezzo_h2_eur_kg", -5), ("prezzo_diesel_eur_l", -0.01),
    ("om_h2_eur_anno", -100), ("om_diesel_eur_anno", -100),
    ("f_diesel_kg_l", -2.68), ("f_h2_kg_kg", -0.5),
    ("prezzo_eua_eur_t", -85), ("capex_h2_eur", -1),
    ("capex_rifornimento_eur", -1), ("capex_diesel_eur", -1),
    ("serbatoio_kg", -10), ("wacc_pct", -0.1),
    ("wacc_pct", 50.1), ("vita_anni", -1), ("vita_anni", 2.5),
    ("tolleranza_pct", -1), ("tolleranza_pct", 100.1),
])
def test_valida_rifiuta_singoli_campi(campo, valore):
    d = _demo_kwargs()
    d[campo] = valore
    assert mh750_valida(**d)["valido"] is False


def test_df_tabella_valori_demo_selezionati():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Km annui (km/anno)"] == 150000.0
    assert mappa["Litri diesel (L/anno)"] == 135000.0
    assert mappa["Autonomia (km)"] == pytest.approx(866.6666666666667)
    assert mappa["CAPEX delta (EUR)"] == 3500000.0
    assert mappa["Payback (anni)"] is None
    assert mappa["Verdetto"] == "NON_CONVIENTE"
