"""Test tab751 "Calore di scarto industriale: il recupero
termico paga contro la caldaia a gas?"

Nuova tab tab751 (calore di
scarto industriale, w752).
Business case deterministico di
un recupero diretto di calore di
scarto industriale contro una
caldaia a gas: potenza termica
di scarto per ore annue e
disponibilita', eta di recupero
con clamp in [0, 1], cap del
calore utile sul fabbisogno
termico del sito, combustibile
risparmiato diviso per l'eta
della caldaia, costo baseline
del gas contro O&M del recupero
piu' ausiliari elettrici, CO2
evitata come CO2 del gas
risparmiato meno CO2 ausiliaria,
CAPEX totale scambiatore piu'
integrazione, VAN, TIR, payback
(primo anno con cumulato >= 0)
e prezzo del gas di pareggio.
Distinta dalla tab ATES
(accumulo stagionale in
acquifero, non recupero diretto),
dalla cogenerazione (produzione
combinata, non recupero), dalle
pompe di calore (COP, non
scambio diretto) e dal solare
termico (collettori, non scarto
di processo): qui recupero
diretto di calore di scarto
industriale con cap sul
fabbisogno utile.

Demo calcolata eseguendo demo_calcoli()
(e ricontrollata a mano, riga per riga):
sorgente industriale da 800 kW,
6000 ore/anno, disponibilita'
0,90, eta di recupero 0,65,
fabbisogno 5000000 kWh_t/anno,
eta caldaia 0,90, prezzo gas
0,09 EUR/kWh, O&M 25000 EUR/anno,
ausiliari 120000 kWh_el/anno a
0,22 EUR/kWh, fattore gas 0,20
kg/kWh e fattore elettricita'
0,35 kg/kWh, CAPEX scambiatore
300000 EUR e CAPEX integrazione
150000 EUR (totale 450000 EUR),
WACC 5 %, vita 15 anni,
tolleranza 10 % del CAPEX totale.

- q_scarto_kwh = 4320000.0
- q_rec_kwh = 2808000.0
- q_utile_kwh = 2808000.0
- copertura = 0.5616
- risparmio_combustibile_kwh = 3120000.0
- costo_base_eur = 280800.0
- costo_rec_eur = 51400.0
- risparmio_eur_anno = 229400.0
- risparmio_eur_kwh = 0.0816951566951567
- co2_base_t = 624.0
- co2_aux_t = 42.0
- co2_evitata_t = 582.0
- capex_totale_eur = 450000.0
- crf = 0.09634228760924432
- quota_capex_eur = 43354.02942415995
- costo_livellato_rec_eur = 94754.02942415995
- costo_livellato_base_eur = 280800.0
- van = 1931093.5539586274
- tir = 50.87104633870801
- payback = 2
- prezzo_pareggio_eur_kwh = 0.016474358974358973
- verdetto = 'CONVIENTE'

Scomposizione: Q scarto = 800 x
6000 x 0,90 = 4320000 kWh_t;
Q recuperato = 4320000 x 0,65 =
2808000 kWh_t; il fabbisogno e'
5000000 kWh_t, quindi il cap non
scatta e Q utile = 2808000 kWh_t
(copertura 0,5616); combustibile
risparmiato 2808000 / 0,90 =
3120000 kWh PCI; costo baseline
3120000 x 0,09 = 280800,00 EUR;
costo recupero 25000 + 120000 x
0,22 = 51400,00 EUR; risparmio
280800,00 - 51400,00 = 229400,00
EUR/anno = 0,0817 EUR/kWh_t;
CO2 base 3120000 x 0,20 / 1000 =
624,00 t; CO2 ausiliaria 120000 x
0,35 / 1000 = 42,00 t; evitata
582,00 t; CAPEX totale 300000 +
150000 = 450000 EUR; CRF 0,05 x
1,05^15 / (1,05^15 - 1) =
0.09634228760924432; quota CAPEX
450000 x 0,096342 = 43354,03
EUR/anno; costo livellato recupero
51400,00 + 43354,03 = 94754,03
EUR/anno contro 280800,00 EUR/anno
della baseline; flussi: anno 0
-450000, anni 1-15 risparmio
229400 (piatti); VAN -450000 +
229400 x 10,37965804 (annuita'
15 anni al 5 %) = 1931093,55 EUR;
TIR circa 50,87 %; payback 2 anni
(il cumulato all'anno 1 e'
-220600, all'anno 2 e' 8800);
prezzo gas di pareggio 51400 /
3120000 = 0,016474358974358973
EUR/kWh; verdetto CONVIENTE
perche' VAN > 0.
NOTA: il CRF entra solo nel costo
livellato, mai nei flussi: il CAPEX
totale compare una sola volta,
all'anno 0. NOTA 2: in questo brief
il risparmio nullo o negativo NON
e' degenere: al prezzo di pareggio
il risparmio si azzera (0 EUR/anno)
e il caso resta calcolabile
(valid=True, VAN -450000 EUR,
NON_CONVIENTE perche' |VAN| =
450000 > 10 % di 450000). NOTA 3:
la CO2 evitata negativa NON e'
degenere di per se': se il
risparmio resta > 0 il caso resta
calcolabile e la CO2 evitata
negativa va detta (fattore
elettricita' 6,00 kg/kWh: CO2
ausiliaria 720 t, evitata -96 t,
valid=True). NOTA 4: il prezzo di
pareggio segue la formula del
brief (vedi test_prezzo_pareggio):
con gli input demo vale 0,016474
EUR/kWh, non 0,09: 0,09 e' il
prezzo del gas pagato, il pareggio
e' il prezzo al quale il risparmio
si azzera (51400 / 3120000).
NOTA 5: l'eta di recupero sopra 1
viene clampata a 1 (vedi
test_eta_recupero_clamp): non e'
un errore, e' la regola del brief.
"""

import ast
import math
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w752_helpers import (
    demo_calcoli,
    mh751_calcola,
    mh751_capex_totale,
    mh751_co2_aux,
    mh751_co2_base,
    mh751_co2_evitata,
    mh751_copertura,
    mh751_costo_base,
    mh751_costo_livellato_rec,
    mh751_costo_rec,
    mh751_crf,
    mh751_csv,
    mh751_demo,
    mh751_eta_recupero,
    mh751_flussi,
    mh751_frac_0_1,
    mh751_int_nneg,
    mh751_int_pos,
    mh751_nneg,
    mh751_num,
    mh751_pct_0_100,
    mh751_pct_wacc,
    mh751_pos,
    mh751_prezzo_pareggio,
    mh751_q_rec,
    mh751_q_scarto,
    mh751_q_utile,
    mh751_quota_capex,
    mh751_risparmio,
    mh751_risparmio_combustibile,
    mh751_risparmio_per_kwh,
    mh751_tir,
    mh751_valida,
    mh751_van,
    mh751_verdetto,
    mh751_payback,
)


def _demo_kwargs():
    return dict(mh751_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh751_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh751_num(3, "x") == 3.0
    assert mh751_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh751_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh751_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh751_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh751_pos(0, "x")
    with pytest.raises(ValueError):
        mh751_pos(-1, "x")
    assert mh751_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh751_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh751_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh751_int_pos(0, "x")


def test_int_nneg_zero_ok():
    assert mh751_int_nneg(0, "x") == 0
    with pytest.raises(ValueError):
        mh751_int_nneg(-1, "x")


def test_pct_0_100_limiti():
    assert mh751_pct_0_100(0, "x") == 0.0
    assert mh751_pct_0_100(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh751_pct_0_100(100.1, "x")
    with pytest.raises(ValueError):
        mh751_pct_0_100(-1, "x")


def test_pct_wacc_limiti():
    assert mh751_pct_wacc(0, "x") == 0.0
    assert mh751_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh751_pct_wacc(50.1, "x")


def test_frac_0_1_limiti():
    assert mh751_frac_0_1(1.0, "x") == 1.0
    assert mh751_frac_0_1(0.9, "x") == 0.9
    with pytest.raises(ValueError):
        mh751_frac_0_1(0, "x")
    with pytest.raises(ValueError):
        mh751_frac_0_1(1.1, "x")
    with pytest.raises(ValueError):
        mh751_frac_0_1(-0.1, "x")


def test_eta_recupero_clamp():
    assert mh751_eta_recupero(0.65, "x") == 0.65
    assert mh751_eta_recupero(1.0, "x") == 1.0
    assert mh751_eta_recupero(1.5, "x") == 1.0
    with pytest.raises(ValueError):
        mh751_eta_recupero(0, "x")
    with pytest.raises(ValueError):
        mh751_eta_recupero(-0.1, "x")


# ---------------------------------------------------------------- fisica base
def test_q_scarto():
    assert mh751_q_scarto(800, 6000, 0.9) == 4320000.0
    assert mh751_q_scarto(800, 6000, 1.0) == 4800000.0
    with pytest.raises(ValueError):
        mh751_q_scarto(0, 6000, 0.9)
    with pytest.raises(ValueError):
        mh751_q_scarto(800, 0, 0.9)
    with pytest.raises(ValueError):
        mh751_q_scarto(800, 6000, 0)


def test_q_rec_e_clamp():
    assert mh751_q_rec(4320000.0, 0.65) == 2808000.0
    assert mh751_q_rec(4320000.0, 1.5) == 4320000.0
    assert mh751_q_rec(0.0, 0.65) == 0.0
    with pytest.raises(ValueError):
        mh751_q_rec(4320000.0, 0)


def test_q_utile_cap():
    assert mh751_q_utile(2808000.0, 5000000) == 2808000.0
    assert mh751_q_utile(4320000.0, 2000000) == 2000000.0
    assert mh751_q_utile(0.0, 5000000) == 0.0


def test_copertura():
    assert mh751_copertura(2808000.0, 5000000) == pytest.approx(0.5616)
    assert mh751_copertura(2000000.0, 2000000) == 1.0
    assert mh751_copertura(2808000.0, 0) is None
    assert mh751_copertura(0.0, 5000000) == 0.0


def test_risparmio_combustibile():
    assert mh751_risparmio_combustibile(2808000.0, 0.9) == 3120000.0
    assert mh751_risparmio_combustibile(0.0, 0.9) == 0.0
    with pytest.raises(ValueError):
        mh751_risparmio_combustibile(2808000.0, 0)


def test_costo_base_e_rec():
    assert mh751_costo_base(3120000.0, 0.09) == 280800.0
    assert mh751_costo_rec(25000, 120000, 0.22) == 51400.0
    assert mh751_costo_rec(0, 0, 0.22) == 0.0
    assert mh751_costo_base(0.0, 0.09) == 0.0


def test_risparmio_e_per_kwh():
    assert mh751_risparmio(280800.0, 51400.0) == 229400.0
    assert mh751_risparmio_per_kwh(229400.0, 2808000.0) == pytest.approx(
        0.0816951566951567)
    assert mh751_risparmio_per_kwh(229400.0, 0) is None
    assert mh751_risparmio(51400.0, 51400.0) == 0.0


def test_co2_base_aux_evitata():
    assert mh751_co2_base(3120000.0, 0.20) == 624.0
    assert mh751_co2_aux(120000, 0.35) == 42.0
    assert mh751_co2_evitata(624.0, 42.0) == 582.0
    assert mh751_co2_aux(0, 0.35) == 0.0


def test_co2_evitata_segno_libero():
    assert mh751_co2_evitata(624.0, 720.0) == pytest.approx(-96.0)


# ---------------------------------------------------------------- finanza base
def test_capex_totale():
    assert mh751_capex_totale(300000, 150000) == 450000
    assert mh751_capex_totale(600000, 300000) == 900000
    assert mh751_capex_totale(0, 0) == 0


def test_crf():
    assert mh751_crf(5.0, 15) == pytest.approx(0.09634228760924432)
    assert mh751_crf(0, 15) == pytest.approx(1.0 / 15.0)
    assert mh751_crf(5.0, 1) == pytest.approx(1.05)
    assert mh751_crf(5.0, 10) == pytest.approx(0.1295045749654566)


def test_quota_capex_e_livellato():
    assert mh751_quota_capex(450000, 0.09634228760924432) == pytest.approx(
        43354.02942415995)
    assert mh751_costo_livellato_rec(51400.0, 43354.02942415995) == pytest.approx(
        94754.02942415995)
    assert mh751_costo_livellato_rec(51400.0, 0.0) == 51400.0


def test_prezzo_pareggio_formula_brief():
    assert mh751_prezzo_pareggio(51400.0, 3120000.0) == pytest.approx(
        0.016474358974358973)
    assert mh751_prezzo_pareggio(51400.0, 0) is None
    assert mh751_prezzo_pareggio(0.0, 3120000.0) == 0.0


def test_flussi_lunghezza_e_primo():
    fl = mh751_flussi(450000, 229400.0, 15)
    assert len(fl) == 16
    assert fl[0] == -450000
    assert all(f == 229400.0 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = demo_calcoli()
    assert bc["van"] == pytest.approx(1931093.5539586274)
    assert mh751_van([-450000] + [229400.0] * 15, 0) == 2991000.0
    assert mh751_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo_e_conviente():
    bc = demo_calcoli()
    assert bc["tir"] == pytest.approx(50.87104633870801)
    assert mh751_tir([-450000] + [229400.0] * 15) == pytest.approx(
        0.5087104633870801)
    tir = mh751_tir([-450000] + [229400.0] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-450000] + [229400.0] * 15))
    assert npv == pytest.approx(0.0, abs=1e-4)


def test_payback():
    assert mh751_payback([-450000] + [229400.0] * 15) == 2
    assert mh751_payback([-450000] + [80.0] * 15) is None
    assert mh751_payback([0] + [229400.0] * 15) == 0
    assert mh751_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh751_verdetto(100.0, 450000, 10.0) == "CONVIENTE"
    assert mh751_verdetto(-11978.43, 450000, 10.0) == "MARGINALE"
    assert mh751_verdetto(-45000.0, 450000, 10.0) == "MARGINALE"
    assert mh751_verdetto(-45000.01, 450000, 10.0) == "NON_CONVIENTE"
    assert mh751_verdetto(-1931093.55, 450000, 10.0) == "NON_CONVIENTE"
    assert mh751_verdetto(float("nan"), 450000, 10.0) == "NON_CALCOLABILE"
    assert mh751_verdetto(0.0, 0, 10.0) == "MARGINALE"


def test_valida_demo_ok():
    v = mh751_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("potenza_scarto_kw", "800"),
                       ("potenza_scarto_kw", float("nan")),
                       ("potenza_scarto_kw", float("inf")),
                       ("potenza_scarto_kw", True),
                       ("prezzo_gas_eur_kwh", None)):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh751_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("potenza_scarto_kw", 0),
                          ("ore_anno", 0),
                          ("disponibilita", 0),
                          ("disponibilita", 1.5),
                          ("eta_recupero", 0),
                          ("eta_recupero", -0.1),
                          ("fabbisogno_kwh_t", 0),
                          ("eta_caldaia", 0),
                          ("prezzo_gas_eur_kwh", -0.01),
                          ("om_eur_anno", -100),
                          ("aux_kwh_el", -1),
                          ("prezzo_el_eur_kwh", -0.01),
                          ("f_gas_kg_kwh", -0.20),
                          ("f_el_kg_kwh", -0.35),
                          ("capex_scambiatore_eur", -1),
                          ("capex_integrazione_eur", -1),
                          ("wacc_pct", -0.1), ("wacc_pct", 50.1),
                          ("vita_anni", 0), ("vita_anni", 2.5),
                          ("tolleranza_pct", -1),
                          ("tolleranza_pct", 100.1)):
        d = _demo_kwargs()
        d[campo] = valore
        assert mh751_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"prezzo_gas_eur_kwh": 0, "om_eur_anno": 0,
              "aux_kwh_el": 0, "f_gas_kg_kwh": 0,
              "f_el_kg_kwh": 0, "capex_scambiatore_eur": 0,
              "capex_integrazione_eur": 0, "wacc_pct": 0,
              "tolleranza_pct": 0, "disponibilita": 1.0,
              "eta_recupero": 1.0})
    assert mh751_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    assert mh751_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh751_demo()
    assert d["potenza_scarto_kw"] == 800
    assert d["ore_anno"] == 6000
    assert d["disponibilita"] == 0.9
    assert d["eta_recupero"] == 0.65
    assert d["fabbisogno_kwh_t"] == 5000000
    assert d["eta_caldaia"] == 0.9
    assert d["prezzo_gas_eur_kwh"] == 0.09
    assert d["om_eur_anno"] == 25000
    assert d["aux_kwh_el"] == 120000
    assert d["prezzo_el_eur_kwh"] == 0.22
    assert d["f_gas_kg_kwh"] == 0.20
    assert d["f_el_kg_kwh"] == 0.35
    assert d["capex_scambiatore_eur"] == 300000
    assert d["capex_integrazione_eur"] == 150000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["tolleranza_pct"] == 10.0


def test_demo_calcoli_fisica():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["q_scarto_kwh"] == 4320000.0
    assert bc["q_rec_kwh"] == 2808000.0
    assert bc["q_utile_kwh"] == 2808000.0
    assert bc["copertura"] == pytest.approx(0.5616)
    assert bc["risparmio_combustibile_kwh"] == 3120000.0
    assert bc["co2_base_t"] == 624.0
    assert bc["co2_aux_t"] == 42.0
    assert bc["co2_evitata_t"] == 582.0


def test_demo_calcoli_economia():
    bc = demo_calcoli()
    assert bc["costo_base_eur"] == 280800.0
    assert bc["costo_rec_eur"] == 51400.0
    assert bc["risparmio_eur_anno"] == 229400.0
    assert bc["risparmio_eur_kwh"] == pytest.approx(0.0816951566951567)
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx(
        0.016474358974358973)


def test_demo_calcoli_finanza():
    bc = demo_calcoli()
    assert bc["capex_totale_eur"] == 450000.0
    assert bc["crf"] == pytest.approx(0.09634228760924432)
    assert bc["quota_capex_eur"] == pytest.approx(43354.02942415995)
    assert bc["costo_livellato_rec_eur"] == pytest.approx(
        94754.02942415995)
    assert bc["costo_livellato_base_eur"] == 280800.0
    assert bc["van"] == pytest.approx(1931093.5539586274)
    assert bc["tir"] == pytest.approx(50.87104633870801)
    assert bc["payback"] == 2
    assert bc["verdetto"] == "CONVIENTE"


def test_demo_flussi_e_cumulato():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -450000
    assert len(bc["flussi"]) == 16
    assert all(f == 229400.0 for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -450000
    assert righe.iloc[1]["Cumulato (EUR)"] == -220600.0
    assert righe.iloc[2]["Cumulato (EUR)"] == 8800.0
    assert righe.iloc[15]["Cumulato (EUR)"] == 2991000.0
    assert righe.iloc[15]["Flusso (EUR/anno)"] == 229400.0


def test_demo_tabella_righe():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Q scarto (kWh_t/anno)"] == 4320000.0
    assert mappa["Q utile (kWh_t/anno)"] == 2808000.0
    assert mappa["Copertura fabbisogno (-)"] == pytest.approx(0.5616)
    assert mappa["CAPEX totale (EUR)"] == 450000.0
    assert mappa["Payback (anni)"] == 2
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Prezzo gas di pareggio (EUR/kWh)"] == pytest.approx(
        0.016474358974358973)


def test_demo_coerenza_interna():
    bc = demo_calcoli()
    assert bc["costo_base_eur"] - bc["costo_rec_eur"] == pytest.approx(
        bc["risparmio_eur_anno"])
    assert bc["co2_base_t"] - bc["co2_aux_t"] == pytest.approx(
        bc["co2_evitata_t"])
    assert bc["risparmio_eur_anno"] / bc["q_utile_kwh"] == pytest.approx(
        bc["risparmio_eur_kwh"])
    assert bc["q_utile_kwh"] / bc["fabbisogno_kwh_t"] == pytest.approx(
        bc["copertura"])
    assert bc["capex_totale_eur"] * bc["crf"] == pytest.approx(
        bc["quota_capex_eur"])
    assert bc["costo_rec_eur"] + bc["quota_capex_eur"] == pytest.approx(
        bc["costo_livellato_rec_eur"])
    assert bc["costo_livellato_base_eur"] == bc["costo_base_eur"]


def test_demo_crf_solo_nel_livellato_non_nei_flussi():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -bc["capex_totale_eur"]
    assert all(f == bc["risparmio_eur_anno"] for f in bc["flussi"][1:])
    assert bc["crf"] not in bc["flussi"]
    assert bc["quota_capex_eur"] not in bc["flussi"]
    van_da_flussi = mh751_van(bc["flussi"], bc["wacc_pct"])
    assert van_da_flussi == pytest.approx(bc["van"])
    assert bc["costo_livellato_rec_eur"] == pytest.approx(
        bc["costo_rec_eur"] + bc["capex_totale_eur"] * bc["crf"])


def test_demo_contro_riconteggio_indipendente():
    po, orr, di = 800, 6000, 0.9
    er, fa, ec = 0.65, 5000000, 0.9
    pg, om, au, pe = 0.09, 25000, 120000, 0.22
    fg, fe = 0.20, 0.35
    cs, ci = 300000, 150000
    wacc, vita = 5.0, 15
    qs = po * orr * di
    qr = qs * er
    qu = min(qr, fa)
    rc = qu / ec
    cb = rc * pg
    cr = om + au * pe
    risp = cb - cr
    co2b = rc * fg / 1000.0
    co2a = au * fe / 1000.0
    cxt = cs + ci
    r = wacc / 100.0
    crf = r * (1 + r) ** vita / ((1 + r) ** vita - 1)
    van = -cxt + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    bc = demo_calcoli()
    assert bc["q_scarto_kwh"] == qs
    assert bc["q_rec_kwh"] == qr
    assert bc["q_utile_kwh"] == qu
    assert bc["costo_base_eur"] == cb
    assert bc["costo_rec_eur"] == cr
    assert bc["risparmio_eur_anno"] == risp
    assert bc["co2_base_t"] == co2b
    assert bc["co2_aux_t"] == co2a
    assert bc["crf"] == pytest.approx(crf)
    assert bc["van"] == pytest.approx(van)
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx(cr / rc)


def test_demo_riconteggio_crf_van_payback_pareggio_a_mano():
    bc = demo_calcoli()
    r = 0.05
    annuita = (1 - (1 + r) ** -15) / r
    assert annuita == pytest.approx(10.3796580381806)
    assert bc["van"] == pytest.approx(-450000 + 229400.0 * annuita)
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx(
        51400.0 / 3120000.0)
    assert bc["flussi"][0] + 15 * bc["flussi"][1] == 2991000.0
    assert bc["flussi"][0] + 2 * bc["flussi"][1] == 8800.0


# ---------------------------------------------------------------- varianti
def test_variante_prezzo_gas_basso():
    bc = _variante(prezzo_gas_eur_kwh=0.05)
    assert bc["risparmio_eur_anno"] == 104600.0
    assert bc["van"] == pytest.approx(635712.2307936896)
    assert bc["payback"] == 5
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_variante_prezzo_gas_marginale():
    bc = _variante(prezzo_gas_eur_kwh=0.03)
    assert bc["risparmio_eur_anno"] == 42200.0
    assert bc["van"] == pytest.approx(-11978.430788779118)
    assert bc["van"] < 0.0
    assert abs(bc["van"]) <= 0.10 * 450000
    assert bc["tir"] == pytest.approx(4.603534451456481)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"


def test_variante_prezzo_gas_quasi_pareggio():
    bc = _variante(prezzo_gas_eur_kwh=0.0165)
    assert bc["risparmio_eur_anno"] == 80.0
    assert bc["van"] == pytest.approx(-449169.6273569456)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_eta_recupero_bassa():
    bc = _variante(eta_recupero=0.40)
    assert bc["q_rec_kwh"] == 1728000.0
    assert bc["q_utile_kwh"] == 1728000.0
    assert bc["risparmio_eur_anno"] == 121400.0
    assert bc["van"] == pytest.approx(810090.4858351237)
    assert bc["copertura"] == pytest.approx(0.3456)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_eta_recupero_clamp_sopra_uno():
    bc = _variante(eta_recupero=1.5)
    assert bc["valid"] is True
    assert bc["eta_recupero"] == 1.0
    assert bc["q_rec_kwh"] == 4320000.0
    assert bc["q_utile_kwh"] == 4320000.0
    assert bc["risparmio_eur_anno"] == 380600.0
    assert bc["van"] == pytest.approx(3500497.849331532)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_cap_fabbisogno():
    bc = _variante(fabbisogno_kwh_t=2000000)
    assert bc["q_rec_kwh"] == 2808000.0
    assert bc["q_utile_kwh"] == 2000000.0
    assert bc["copertura"] == 1.0
    assert bc["risparmio_eur_anno"] == pytest.approx(148600.0)
    assert bc["van"] == pytest.approx(1092417.1844736354)
    assert bc["co2_evitata_t"] == pytest.approx(402.44444444444446)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_potenza_doppia_cap_attivo():
    bc = _variante(potenza_scarto_kw=1600)
    assert bc["q_scarto_kwh"] == 8640000.0
    assert bc["q_rec_kwh"] == 5616000.0
    assert bc["q_utile_kwh"] == 5000000.0
    assert bc["risparmio_eur_anno"] == pytest.approx(448600.0)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_pareggio_azzera_risparmio():
    bc = _variante(prezzo_gas_eur_kwh=0.016474358974358973)
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["van"] == pytest.approx(-450000.0)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_variante_wacc_zero():
    bc = _variante(wacc_pct=0)
    assert bc["crf"] == pytest.approx(1.0 / 15.0)
    assert bc["quota_capex_eur"] == 30000.0
    assert bc["costo_livellato_rec_eur"] == 81400.0
    assert bc["van"] == 2991000.0
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_alto():
    bc = _variante(capex_scambiatore_eur=600000,
                   capex_integrazione_eur=300000)
    assert bc["capex_totale_eur"] == 900000
    assert bc["van"] == pytest.approx(1481093.5539586274)
    assert bc["payback"] == 4
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex_scambiatore_eur=0, capex_integrazione_eur=0)
    assert bc["capex_totale_eur"] == 0
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(2381093.553958628)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_vita_dieci():
    bc = _variante(vita_anni=10)
    assert len(bc["flussi"]) == 11
    assert bc["crf"] == pytest.approx(0.1295045749654566)
    assert bc["van"] == pytest.approx(1321365.9927549956)
    assert bc["payback"] == 2


def test_variante_om_alto():
    bc = _variante(om_eur_anno=100000)
    assert bc["costo_rec_eur"] == 126400.0
    assert bc["risparmio_eur_anno"] == 154400.0
    assert bc["van"] == pytest.approx(1152619.2010950833)
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx(
        0.04051282051282051)


def test_variante_aux_zero():
    bc = _variante(aux_kwh_el=0)
    assert bc["costo_rec_eur"] == 25000.0
    assert bc["risparmio_eur_anno"] == 255800.0
    assert bc["co2_evitata_t"] == 624.0
    assert bc["van"] == pytest.approx(2205116.526166595)
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx(
        0.008012820512820512)


def test_variante_fattore_el_zero():
    bc = _variante(f_el_kg_kwh=0.0)
    assert bc["co2_aux_t"] == 0.0
    assert bc["co2_evitata_t"] == 624.0
    assert bc["risparmio_eur_anno"] == 229400.0


def test_variante_risparmio_negativo_calcolabile_non_degenere():
    bc = _variante(prezzo_gas_eur_kwh=0.0165)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] > 0.0
    bc2 = _variante(prezzo_gas_eur_kwh=0.01)
    assert bc2["valid"] is True
    assert bc2["risparmio_eur_anno"] == -20200.0
    assert bc2["verdetto"] == "NON_CONVIENTE"
    assert bc2["payback"] is None


def test_variante_co2_negativa_ma_calcolabile():
    bc = _variante(f_el_kg_kwh=6.0)
    assert bc["co2_aux_t"] == 720.0
    assert bc["co2_evitata_t"] == pytest.approx(-96.0)
    assert bc["valid"] is True
    assert bc["verdetto"] == "CONVIENTE"


# ---------------------------------------------------------------- degenere
def test_degenere_potenza_zero():
    bc = _variante(potenza_scarto_kw=0)
    assert bc["valid"] is False
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"] == []
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_kwh"] is None
    assert bc["errore"]


def test_degenere_ore_disponibilita_eta_fabbisogno_caldaia():
    for kw in ({"ore_anno": 0}, {"disponibilita": 0},
               {"disponibilita": 1.5}, {"eta_recupero": 0},
               {"eta_recupero": -0.1}, {"fabbisogno_kwh_t": 0},
               {"eta_caldaia": 0}, {"eta_caldaia": -0.1}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_wacc_vita_tolleranza():
    for kw in ({"wacc_pct": -1}, {"wacc_pct": 60},
               {"vita_anni": 0}, {"vita_anni": 2.5},
               {"tolleranza_pct": -1}, {"tolleranza_pct": 101}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_stringa_nan_inf():
    for kw in ({"potenza_scarto_kw": "800"},
               {"potenza_scarto_kw": float("nan")},
               {"prezzo_gas_eur_kwh": float("inf")},
               {"capex_scambiatore_eur": True}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_neutro_campi():
    bc = _variante(potenza_scarto_kw=0)
    assert bc["q_scarto_kwh"] == 0.0
    assert bc["q_rec_kwh"] == 0.0
    assert bc["q_utile_kwh"] == 0.0
    assert bc["copertura"] is None
    assert bc["costo_base_eur"] == 0.0
    assert bc["costo_rec_eur"] == 0.0
    assert bc["risparmio_eur_anno"] == 0.0
    assert bc["risparmio_eur_kwh"] is None
    assert bc["van"] == 0.0
    assert list(bc["df_flussi"].columns) == [
        "Anno", "Flusso (EUR/anno)", "Cumulato (EUR)"]
    assert list(bc["df_tabella"].columns) == ["Voce", "Valore"]


def test_pareggio_none_quando_combustibile_zero():
    assert mh751_prezzo_pareggio(51400.0, 0) is None


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = demo_calcoli()
    testo = mh751_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert "q_scarto_kwh;4320000.0" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "prezzo_pareggio_eur_kwh" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = demo_calcoli()
    testo = mh751_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"capex_totale_eur;{bc['capex_totale_eur']}" in testo
    assert f"q_utile_kwh;{bc['q_utile_kwh']}" in testo


def test_csv_degenere_solo_zeri():
    bc = _variante(potenza_scarto_kw=0)
    testo = mh751_csv(bc, _demo_kwargs())
    assert "van_eur;0.0" in testo
    assert "q_scarto_kwh;0.0" in testo
    assert "verdetto;NON_CALCOLABILE" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = demo_calcoli()
    testo = mh751_csv(bc, _demo_kwargs())
    for chiave in _demo_kwargs():
        assert f"{chiave};" in testo


def test_calcola_non_sollevela_per_input_numerici():
    bc = _variante(prezzo_gas_eur_kwh=0, om_eur_anno=0, aux_kwh_el=0,
                   f_gas_kg_kwh=0, prezzo_el_eur_kwh=0)
    assert bc["valid"] is True
    assert bc["costo_base_eur"] == 0.0
    assert bc["costo_rec_eur"] == 0.0
    assert bc["risparmio_eur_anno"] == 0.0


def test_monotonia_prezzo_gas():
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(prezzo_gas_eur_kwh=0.12)["risparmio_eur_anno"]
    basso = _variante(prezzo_gas_eur_kwh=0.05)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(93600.0)
    assert base - basso == pytest.approx(124800.0)


def test_demo_deterministica_due_chiamate():
    a = demo_calcoli()
    b = demo_calcoli()
    assert a["van"] == b["van"]
    assert a["flussi"] == b["flussi"]
    assert a["tir"] == b["tir"]


def test_demo_chiavi_attese():
    assert set(mh751_demo().keys()) == {
        "potenza_scarto_kw", "ore_anno", "disponibilita",
        "eta_recupero", "fabbisogno_kwh_t", "eta_caldaia",
        "prezzo_gas_eur_kwh", "om_eur_anno", "aux_kwh_el",
        "prezzo_el_eur_kwh", "f_gas_kg_kwh", "f_el_kg_kwh",
        "capex_scambiatore_eur", "capex_integrazione_eur",
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
    ast.parse(_leggi("w752_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w752_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab751:")


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    # token vietati costruiti per concatenazione, cosi' questo
    # stesso file non li contiene come sottostringhe contigue.
    src = _leggi("w752_helpers.py")
    vietati = ["mh" + "75" + "0", "st" + "75" + "0",
               "tab" + "75" + "0", "75" + "0"]
    assert "streamlit" not in src
    assert all(t not in src for t in vietati)


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w752_ui.py")
    vietati = ["mh" + "75" + "0", "st" + "75" + "0",
               "tab" + "75" + "0", "75" + "0"]
    assert all(t not in src for t in vietati)
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st751_") for c in chiavi)
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
    src = _leggi("w752_test.py")
    vietati = ["mh" + "75" + "0", "st" + "75" + "0",
               "tab" + "75" + "0", "75" + "0"]
    assert all(t not in src for t in vietati)


def test_ui_chiavi_demo_coerenti():
    """Ogni _def751[...] letto dalla UI esiste nel dict demo:
    sweep anti-KeyError a render (lezione tab674)."""
    src = _leggi("w752_ui.py")
    usate = set(re.findall(r'_def751\["([^"]+)"\]', src))
    assert usate
    assert usate <= set(mh751_demo().keys())


def test_ui_riferisce_solo_helper_nuovi():
    src = _leggi("w752_ui.py")
    usati = set(re.findall(r'\b(mh\d+_\w+)\b', src))
    assert usati
    assert all(u.startswith("mh751_") for u in usati)


@pytest.mark.parametrize("wacc,vita,atteso", [
    (5.0, 15, 0.09634228760924432),
    (0, 15, 0.06666666666666667),
    (10.0, 10, 0.16274539488251152),
    (5.0, 1, 1.05),
    (50.0, 5, 0.5758293838862559),
])
def test_crf_parametrizzato(wacc, vita, atteso):
    assert mh751_crf(wacc, vita) == pytest.approx(atteso)


@pytest.mark.parametrize("campo,valore", [
    ("potenza_scarto_kw", 0), ("potenza_scarto_kw", -3),
    ("ore_anno", 0), ("ore_anno", -100),
    ("disponibilita", 0), ("disponibilita", 1.5),
    ("eta_recupero", 0), ("eta_recupero", -0.5),
    ("fabbisogno_kwh_t", 0), ("eta_caldaia", 0),
    ("prezzo_gas_eur_kwh", -0.01), ("om_eur_anno", -100),
    ("aux_kwh_el", -1), ("prezzo_el_eur_kwh", -0.01),
    ("f_gas_kg_kwh", -0.20), ("f_el_kg_kwh", -0.35),
    ("capex_scambiatore_eur", -1), ("capex_integrazione_eur", -1),
    ("wacc_pct", -0.1), ("wacc_pct", 50.1),
    ("vita_anni", -1), ("vita_anni", 2.5),
    ("tolleranza_pct", -1), ("tolleranza_pct", 100.1),
])
def test_valida_rifiuta_singoli_campi(campo, valore):
    d = _demo_kwargs()
    d[campo] = valore
    assert mh751_valida(**d)["valido"] is False


def test_df_tabella_valori_demo_selezionati():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Potenza di scarto (kW)"] == 800.0
    assert mappa["Q utile (kWh_t/anno)"] == 2808000.0
    assert mappa["Copertura fabbisogno (-)"] == pytest.approx(0.5616)
    assert mappa["CAPEX totale (EUR)"] == 450000.0
    assert mappa["Payback (anni)"] == 2
    assert mappa["Verdetto"] == "CONVIENTE"
