"""Test tab753 "Pannelli ibridi PVT: elettricita'
+ calore dallo stesso tetto - il doppio
rendimento paga?"

Nuova tab tab753 (pannelli ibridi
PVT, w754). Business case
deterministico di un impianto di
pannelli ibridi fotovoltaico-termici:
stesso modulo, stessa irradiazione
sullo stesso tetto, due prodotti
(elettricita' e calore). Energia
elettrica = area x irradiazione x
eta elettrica; calore prodotto =
area x irradiazione x eta termica;
calore utile = min(calore prodotto,
domanda termica); calore in eccesso
= prodotto - utile; gas risparmiato
= calore utile / eta caldaia;
risparmio elettrico, risparmio gas,
risparmio lordo e netto; CO2 evitata
sempre maggiore o uguale a zero
qui; CAPEX, VAN, TIR, payback
(primo anno con cumulato >= 0),
costo livellato combinato
dell'energia utile e prezzo
elettrico di pareggio (puo' essere
negativo: il solo risparmio gas
copre gia' l'O&M). Distinta dal
fotovoltaico solo-elettrico (nessun
calore recuperato), dal solare
termico solo-calore (nessuna
elettricita') e dalla pompa di
calore (calore da elettricita'
con COP, non da irradiazione sullo
stesso modulo): qui un solo tetto,
una sola irradiazione, due
rendimenti sullo stesso modulo.

Demo calcolata eseguendo demo_calcoli()
(e ricontrollata a mano, riga per riga):
impianto PVT da 100 m2, irradiazione
1200 kWh/m2/anno, eta elettrica
0,20 e eta termica 0,50, domanda
termica 20000 kWh/anno, eta caldaia
0,90, prezzo elettrico 0,25 EUR/kWh
e prezzo gas 0,10 EUR/kWh, O&M 500
EUR/anno, CAPEX 30000 EUR, fattore
elettrico 0,30 kg/kWh e fattore gas
0,20 kg/kWh, WACC 5 %, vita 20 anni,
tolleranza 10 % del CAPEX.

- e_el_kwh_anno = 24000.0
- q_th_prod_kwh_anno = 60000.0
- q_th_used_kwh_anno = 20000.0
- q_th_excess_kwh_anno = 40000.0
- gas_risparmiato_kwh_anno = 22222.222222222223
- risparmio_el_eur_anno = 6000.0
- risparmio_gas_eur_anno = 2222.222222222222
- risparmio_lordo_eur_anno = 8222.222222222223
- risparmio_netto_eur_anno = 7722.222222222223
- co2_evitata_t_anno = 11.644444444444446
- crf = 0.08024258719069129
- quota_capex_eur_anno = 2407.2776157207386
- costo_livellato_eur_kwh = 0.06607449126638042
- van = 66235.95764516985
- tir = 25.465220203207362
- payback = 4
- prezzo_pareggio_eur_kwh = -0.07175925925925926
- verdetto = 'CONVIENTE'

Scomposizione: E_el = 100 x
1200 x 0,20 = 24000 kWh/anno;
Q_th prodotto = 100 x 1200 x
0,50 = 60000 kWh/anno; Q_th utile
= min(60000, 20000) = 20000
kWh/anno; eccesso = 60000 - 20000
= 40000 kWh/anno; gas risparmiato
= 20000 / 0,90 = 22222,22 kWh/anno;
risparmio elettrico = 24000 x 0,25
= 6000,00 EUR/anno; risparmio gas
= 22222,22 x 0,10 = 2222,22
EUR/anno; lordo = 8222,22
EUR/anno; netto = 8222,22 - 500 =
7722,22 EUR/anno; CO2 evitata =
(24000 x 0,30 + 22222,22 x 0,20) /
1000 = 11,64 t/anno (7,20 t parte
elettrica + 4,44 t parte gas);
CAPEX 30000 EUR; CRF 0,05 x
1,05^20 / (1,05^20 - 1) =
0.08024258719069129; quota CAPEX
30000 x 0,080243 = 2407,28
EUR/anno; costo livellato
combinato (2407,28 + 500) / (24000
+ 20000) = 0,06607 EUR/kWh utile
contro prezzo elettrico 0,25;
flussi: anno 0 -30000, anni 1-20
risparmio netto 7722,22 (piatti);
VAN -30000 + 7722,22 x 12,46221034
(annuita' 20 anni al 5 %) =
66235,96 EUR; TIR circa 25,47 %;
payback 4 anni (il cumulato
all'anno 3 e' -6833,33, all'anno 4
e' 888,89); prezzo elettrico di
pareggio (500 - 2222,22) / 24000 =
-0,07175925925925926 EUR/kWh;
verdetto CONVIENTE perche' VAN > 0.
NOTA: il CRF entra solo nel costo
livellato combinato, mai nei
flussi: il CAPEX compare una sola
volta, all'anno 0.
NOTA 2: in questo brief il
risparmio netto nullo o negativo
NON e' degenere: con O&M
8222,22 EUR/anno il risparmio
netto si azzera (0 EUR/anno) e il
caso resta calcolabile (valid=True,
VAN -30000 EUR, NON_CONVIENTE
perche' |VAN| = 30000 > 3000, cioe'
oltre il 10 % del CAPEX; il pareggio
elettrico vale 0,25 EUR/kWh, cioe'
il prezzo elettrico pagato).
NOTA 3: il prezzo elettrico di
pareggio della demo e' NEGATIVO
(-0,0718 EUR/kWh): non e' un
errore, significa che il solo
risparmio gas (2222,22 EUR) copre
gia' l'O&M (500 EUR) con 1722,22
EUR di margine, quindi anche con
prezzo elettrico nullo il risparmio
netto resterebbe 1722,22 EUR/anno.
NOTA 4: la domanda termica nulla
NON e' degenere: con Q_demand = 0
il calore utile e' 0, l'eccesso e'
60000 kWh/anno e il caso elettrico
resta calcolabile (valid=True,
risparmio netto 5500 EUR/anno,
VAN 38542,16 EUR, CONVIENTE).
NOTA 5: le eta sopra 1 vengono
clampate a 1 (vedi test_eta_clamp):
non e' un errore, e' la regola
del brief.
"""

import ast
import math
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w754_helpers import (
    demo_calcoli,
    mh753_calcola,
    mh753_co2_evitata,
    mh753_costo_livellato,
    mh753_crf,
    mh753_csv,
    mh753_demo,
    mh753_e_el,
    mh753_eta,
    mh753_flussi,
    mh753_gas_risparmiato,
    mh753_int_nneg,
    mh753_int_pos,
    mh753_nneg,
    mh753_num,
    mh753_payback,
    mh753_pct_0_100,
    mh753_pct_wacc,
    mh753_pos,
    mh753_prezzo_pareggio,
    mh753_q_th_excess,
    mh753_q_th_prod,
    mh753_q_th_used,
    mh753_quota_capex,
    mh753_risparmio_el,
    mh753_risparmio_gas,
    mh753_risparmio_lordo,
    mh753_risparmio_netto,
    mh753_tir,
    mh753_valida,
    mh753_van,
    mh753_verdetto,
)


def _demo_kwargs():
    return dict(mh753_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh753_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh753_num(3, "x") == 3.0
    assert mh753_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh753_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh753_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh753_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh753_pos(0, "x")
    with pytest.raises(ValueError):
        mh753_pos(-1, "x")
    assert mh753_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh753_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh753_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh753_int_pos(0, "x")


def test_int_nneg_zero_ok():
    assert mh753_int_nneg(0, "x") == 0
    with pytest.raises(ValueError):
        mh753_int_nneg(-1, "x")


def test_pct_0_100_limiti():
    assert mh753_pct_0_100(0, "x") == 0.0
    assert mh753_pct_0_100(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh753_pct_0_100(100.1, "x")
    with pytest.raises(ValueError):
        mh753_pct_0_100(-1, "x")


def test_pct_wacc_limiti():
    assert mh753_pct_wacc(0, "x") == 0.0
    assert mh753_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh753_pct_wacc(50.1, "x")


def test_eta_clamp():
    assert mh753_eta(0.20, "x") == 0.20
    assert mh753_eta(1.0, "x") == 1.0
    assert mh753_eta(1.5, "x") == 1.0
    with pytest.raises(ValueError):
        mh753_eta(0, "x")
    with pytest.raises(ValueError):
        mh753_eta(-0.1, "x")


# ---------------------------------------------------------------- fisica base
def test_e_el_e_q_th_prod():
    assert mh753_e_el(100, 1200, 0.20) == 24000.0
    assert mh753_e_el(100, 1200, 0.50) == 60000.0
    assert mh753_q_th_prod(100, 1200, 0.50) == 60000.0
    assert mh753_q_th_prod(100, 1200, 0.20) == 24000.0
    with pytest.raises(ValueError):
        mh753_e_el(0, 1200, 0.20)
    with pytest.raises(ValueError):
        mh753_e_el(100, 0, 0.20)
    with pytest.raises(ValueError):
        mh753_e_el(100, 1200, 0)
    assert mh753_e_el(100, 1200, 1.5) == 120000.0


def test_q_th_used_e_excess():
    assert mh753_q_th_used(60000.0, 20000) == 20000.0
    assert mh753_q_th_used(60000.0, 100000) == 60000.0
    assert mh753_q_th_used(60000.0, 0) == 0.0
    assert mh753_q_th_excess(60000.0, 20000.0) == 40000.0
    assert mh753_q_th_excess(60000.0, 60000.0) == 0.0
    assert mh753_q_th_excess(60000.0, 0.0) == 60000.0
    with pytest.raises(ValueError):
        mh753_q_th_used(60000.0, -1)


def test_gas_risparmiato():
    assert mh753_gas_risparmiato(20000.0, 0.90) == pytest.approx(
        22222.222222222223)
    assert mh753_gas_risparmiato(20000.0, 1.0) == 20000.0
    assert mh753_gas_risparmiato(20000.0, 1.5) == 20000.0
    assert mh753_gas_risparmiato(0.0, 0.90) == 0.0
    with pytest.raises(ValueError):
        mh753_gas_risparmiato(20000.0, 0)


def test_risparmi_lordo_netto():
    assert mh753_risparmio_el(24000.0, 0.25) == 6000.0
    assert mh753_risparmio_gas(22222.222222222223, 0.10) == pytest.approx(
        2222.222222222222)
    assert mh753_risparmio_lordo(6000.0, 2222.222222222222) == pytest.approx(
        8222.222222222223)
    assert mh753_risparmio_netto(8222.222222222223, 500) == pytest.approx(
        7722.222222222223)
    assert mh753_risparmio_netto(500.0, 500) == 0.0
    assert mh753_risparmio_netto(0.0, 500) == -500.0
    assert mh753_risparmio_el(0.0, 0.25) == 0.0


def test_co2_evitata():
    assert mh753_co2_evitata(24000.0, 22222.222222222223, 0.30,
                              0.20) == pytest.approx(11.644444444444446)
    assert mh753_co2_evitata(24000.0, 0.0, 0.30, 0.20) == pytest.approx(7.2)
    assert mh753_co2_evitata(0.0, 0.0, 0.30, 0.20) == 0.0
    assert mh753_co2_evitata(24000.0, 22222.222222222223, 0.0,
                             0.0) == 0.0


# ---------------------------------------------------------------- finanza base
def test_crf():
    assert mh753_crf(5.0, 20) == pytest.approx(0.08024258719069129)
    assert mh753_crf(0, 20) == pytest.approx(1.0 / 20.0)
    assert mh753_crf(5.0, 1) == pytest.approx(1.05)
    assert mh753_crf(5.0, 10) == pytest.approx(0.12950457496545661)


def test_quota_capex_e_livellato():
    assert mh753_quota_capex(30000, 0.08024258719069129) == pytest.approx(
        2407.2776157207386)
    assert mh753_costo_livellato(30000, 0.08024258719069129, 500,
                                 24000.0,
                                 20000.0) == pytest.approx(
        0.06607449126638042)
    assert mh753_costo_livellato(30000, 0.08024258719069129, 500,
                                 0, 0) is None
    assert mh753_costo_livellato(30000, 0.08024258719069129, 500,
                                 24000.0, 0) == pytest.approx(
        0.12113656732169745)
    assert mh753_costo_livellato(0, 0.08024258719069129, 500,
                                 24000.0,
                                 20000.0) == pytest.approx(
        0.011363636363636364)


def test_prezzo_pareggio_formula_brief_e_negativo():
    assert mh753_prezzo_pareggio(500, 2222.222222222222,
                                 24000.0) == pytest.approx(
        -0.07175925925925926)
    assert mh753_prezzo_pareggio(500, 2222.222222222222, 0) is None
    assert mh753_prezzo_pareggio(0.0, 0, 24000.0) == 0.0
    assert mh753_prezzo_pareggio(8222.222222222222, 2222.222222222222,
                                 24000.0) == pytest.approx(0.25)
    assert mh753_prezzo_pareggio(500, 0.0, 24000.0) == pytest.approx(
        0.020833333333333332)


def test_flussi_lunghezza_e_primo():
    fl = mh753_flussi(30000, 7722.222222222223, 20)
    assert len(fl) == 21
    assert fl[0] == -30000
    assert all(f == 7722.222222222223 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = demo_calcoli()
    assert bc["van"] == pytest.approx(66235.95764516985)
    assert mh753_van([-30000] + [7722.222222222223] * 20,
                     0) == pytest.approx(124444.44444444444)
    assert mh753_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo_e_conviente():
    bc = demo_calcoli()
    assert bc["tir"] == pytest.approx(25.465220203207362)
    assert mh753_tir([-30000] + [7722.222222222223] * 20) == pytest.approx(
        0.2546522020320736)
    tir = mh753_tir([-30000] + [7722.222222222223] * 20)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-30000] + [7722.222222222223] * 20))
    assert npv == pytest.approx(0.0, abs=1e-4)


def test_payback():
    assert mh753_payback([-30000] + [7722.222222222223] * 20) == 4
    assert mh753_payback([-30000] + [80.0] * 20) is None
    assert mh753_payback([0] + [7722.222222222223] * 20) == 0
    assert mh753_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh753_verdetto(100.0, 30000, 10.0) == "CONVIENTE"
    assert mh753_verdetto(-2555.44, 30000, 10.0) == "MARGINALE"
    assert mh753_verdetto(-3000.0, 30000, 10.0) == "MARGINALE"
    assert mh753_verdetto(-3000.01, 30000, 10.0) == "NON_CONVIENTE"
    assert mh753_verdetto(-66235.96, 30000, 10.0) == "NON_CONVIENTE"
    assert mh753_verdetto(float("nan"), 30000, 10.0) == "NON_CALCOLABILE"
    assert mh753_verdetto(0.0, 0, 10.0) == "MARGINALE"


def test_valida_demo_ok():
    v = mh753_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("area_m2", "100"),
                       ("area_m2", float("nan")),
                       ("area_m2", float("inf")),
                       ("area_m2", True),
                       ("prezzo_el_eur_kwh", None)):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh753_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("area_m2", 0),
                          ("h_kwh_m2_anno", 0),
                          ("eta_el", 0),
                          ("eta_el", -0.1),
                          ("eta_th", 0),
                          ("eta_th", -0.1),
                          ("q_demand_kwh_anno", -1),
                          ("eta_caldaia", 0),
                          ("eta_caldaia", -0.1),
                          ("prezzo_el_eur_kwh", -0.01),
                          ("prezzo_gas_eur_kwh", -0.01),
                          ("om_eur_anno", -100),
                          ("capex_eur", -1),
                          ("f_el_kg_kwh", -0.30),
                          ("f_gas_kg_kwh", -0.20),
                          ("wacc_pct", -0.1), ("wacc_pct", 50.1),
                          ("vita_anni", 0), ("vita_anni", 2.5),
                          ("tolleranza_pct", -1),
                          ("tolleranza_pct", 100.1)):
        d = _demo_kwargs()
        d[campo] = valore
        assert mh753_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"prezzo_el_eur_kwh": 0, "prezzo_gas_eur_kwh": 0,
              "om_eur_anno": 0, "capex_eur": 0,
              "f_el_kg_kwh": 0, "f_gas_kg_kwh": 0,
              "wacc_pct": 0, "tolleranza_pct": 0,
              "eta_el": 1.0, "eta_th": 1.0,
              "eta_caldaia": 1.0, "q_demand_kwh_anno": 0})
    assert mh753_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    assert mh753_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh753_demo()
    assert d["area_m2"] == 100
    assert d["h_kwh_m2_anno"] == 1200
    assert d["eta_el"] == 0.20
    assert d["eta_th"] == 0.50
    assert d["q_demand_kwh_anno"] == 20000
    assert d["eta_caldaia"] == 0.90
    assert d["prezzo_el_eur_kwh"] == 0.25
    assert d["prezzo_gas_eur_kwh"] == 0.10
    assert d["om_eur_anno"] == 500
    assert d["capex_eur"] == 30000
    assert d["f_el_kg_kwh"] == 0.30
    assert d["f_gas_kg_kwh"] == 0.20
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 20
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    """Ogni _DEMO del test contro demo_calcoli():
    scarto relativo < 1e-9 (zero atteso:
    confronto assoluto)."""
    bc = demo_calcoli()
    attesi = {
        "e_el_kwh_anno": 24000.0,
        "q_th_prod_kwh_anno": 60000.0,
        "q_th_used_kwh_anno": 20000.0,
        "q_th_excess_kwh_anno": 40000.0,
        "gas_risparmiato_kwh_anno": 22222.222222222223,
        "risparmio_el_eur_anno": 6000.0,
        "risparmio_gas_eur_anno": 2222.222222222222,
        "risparmio_lordo_eur_anno": 8222.222222222223,
        "risparmio_netto_eur_anno": 7722.222222222223,
        "co2_evitata_t_anno": 11.644444444444446,
        "crf": 0.08024258719069129,
        "quota_capex_eur_anno": 2407.2776157207386,
        "costo_livellato_eur_kwh": 0.06607449126638042,
        "van": 66235.95764516985,
        "tir": 25.465220203207362,
        "prezzo_pareggio_eur_kwh": -0.07175925925925926,
    }
    for chiave, atteso in attesi.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert abs(got - atteso) / abs(atteso) < 1e-9, chiave
    assert bc["payback"] == 4
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_demo_calcoli_fisica():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["e_el_kwh_anno"] == 24000.0
    assert bc["q_th_prod_kwh_anno"] == 60000.0
    assert bc["q_th_used_kwh_anno"] == 20000.0
    assert bc["q_th_excess_kwh_anno"] == 40000.0
    assert bc["gas_risparmiato_kwh_anno"] == pytest.approx(
        22222.222222222223)
    assert bc["co2_evitata_t_anno"] == pytest.approx(11.644444444444446)


def test_demo_calcoli_economia():
    bc = demo_calcoli()
    assert bc["risparmio_el_eur_anno"] == 6000.0
    assert bc["risparmio_gas_eur_anno"] == pytest.approx(
        2222.222222222222)
    assert bc["risparmio_lordo_eur_anno"] == pytest.approx(
        8222.222222222223)
    assert bc["risparmio_netto_eur_anno"] == pytest.approx(
        7722.222222222223)
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx(
        -0.07175925925925926)


def test_demo_calcoli_finanza():
    bc = demo_calcoli()
    assert bc["crf"] == pytest.approx(0.08024258719069129)
    assert bc["quota_capex_eur_anno"] == pytest.approx(2407.2776157207386)
    assert bc["costo_livellato_eur_kwh"] == pytest.approx(
        0.06607449126638042)
    assert bc["van"] == pytest.approx(66235.95764516985)
    assert bc["tir"] == pytest.approx(25.465220203207362)
    assert bc["payback"] == 4
    assert bc["verdetto"] == "CONVIENTE"


def test_demo_flussi_e_cumulato():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -30000
    assert len(bc["flussi"]) == 21
    assert all(f == 7722.222222222223 for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -30000
    assert righe.iloc[3]["Cumulato (EUR)"] == pytest.approx(
        -6833.333333333332)
    assert righe.iloc[4]["Cumulato (EUR)"] == pytest.approx(
        888.8888888888905)
    assert righe.iloc[20]["Cumulato (EUR)"] == pytest.approx(
        124444.44444444444)
    assert righe.iloc[20]["Flusso (EUR/anno)"] == 7722.222222222223


def test_demo_tabella_righe():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Energia elettrica (kWh/anno)"] == 24000.0
    assert mappa["Calore utile (kWh/anno)"] == 20000.0
    assert mappa["Risparmio netto (EUR/anno)"] == pytest.approx(
        7722.222222222223)
    assert mappa["Payback (anni)"] == 4
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Prezzo elettrico di pareggio (EUR/kWh)"] == pytest.approx(
        -0.07175925925925926)


def test_demo_coerenza_interna():
    bc = demo_calcoli()
    assert bc["risparmio_el_eur_anno"] + bc["risparmio_gas_eur_anno"] == \
        pytest.approx(bc["risparmio_lordo_eur_anno"])
    assert bc["risparmio_lordo_eur_anno"] - bc["om_eur_anno"] == \
        pytest.approx(bc["risparmio_netto_eur_anno"])
    assert (bc["e_el_kwh_anno"] * bc["f_el_kg_kwh"] +
            bc["gas_risparmiato_kwh_anno"] * bc["f_gas_kg_kwh"]) / 1000.0 == \
        pytest.approx(bc["co2_evitata_t_anno"])
    assert bc["capex_eur"] * bc["crf"] == pytest.approx(
        bc["quota_capex_eur_anno"])
    assert (bc["quota_capex_eur_anno"] + bc["om_eur_anno"]) / \
        (bc["e_el_kwh_anno"] + bc["q_th_used_kwh_anno"]) == \
        pytest.approx(bc["costo_livellato_eur_kwh"])
    assert bc["om_eur_anno"] - bc["risparmio_gas_eur_anno"] == pytest.approx(
        bc["prezzo_pareggio_eur_kwh"] * bc["e_el_kwh_anno"])


def test_demo_crf_solo_nel_livellato_non_nei_flussi():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -bc["capex_eur"]
    assert all(f == bc["risparmio_netto_eur_anno"] for f in bc["flussi"][1:])
    assert bc["crf"] not in bc["flussi"]
    assert bc["quota_capex_eur_anno"] not in bc["flussi"]
    van_da_flussi = mh753_van(bc["flussi"], bc["wacc_pct"])
    assert van_da_flussi == pytest.approx(bc["van"])
    assert bc["costo_livellato_eur_kwh"] == pytest.approx(
        (bc["capex_eur"] * bc["crf"] + bc["om_eur_anno"]) /
        (bc["e_el_kwh_anno"] + bc["q_th_used_kwh_anno"]))


def test_demo_contro_riconteggio_indipendente():
    ar, hh = 100, 1200
    ee, et = 0.20, 0.50
    qd, ec = 20000, 0.90
    pe, pg = 0.25, 0.10
    om, cx = 500, 30000
    fe, fg = 0.30, 0.20
    wacc, vita = 5.0, 20
    e_el = ar * hh * ee
    qp = ar * hh * et
    qu = min(qp, qd)
    gas = qu / ec
    rel = e_el * pe
    rgas = gas * pg
    netto = rel + rgas - om
    co2 = (e_el * fe + gas * fg) / 1000.0
    r = wacc / 100.0
    crf = r * (1 + r) ** vita / ((1 + r) ** vita - 1)
    van = -cx + sum(netto / (1 + r) ** t for t in range(1, vita + 1))
    bc = demo_calcoli()
    assert bc["e_el_kwh_anno"] == e_el
    assert bc["q_th_prod_kwh_anno"] == qp
    assert bc["q_th_used_kwh_anno"] == qu
    assert bc["gas_risparmiato_kwh_anno"] == gas
    assert bc["risparmio_el_eur_anno"] == rel
    assert bc["risparmio_gas_eur_anno"] == rgas
    assert bc["risparmio_netto_eur_anno"] == netto
    assert bc["co2_evitata_t_anno"] == co2
    assert bc["crf"] == pytest.approx(crf)
    assert bc["van"] == pytest.approx(van)
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx((om - rgas) / e_el)


def test_demo_riconteggio_crf_van_payback_pareggio_a_mano():
    bc = demo_calcoli()
    r = 0.05
    annuita = (1 - (1 + r) ** -20) / r
    assert annuita == pytest.approx(12.462210342539992)
    assert bc["van"] == pytest.approx(-30000 + 7722.222222222223 * annuita)
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx(
        (500 - 2222.222222222222) / 24000.0)
    assert bc["flussi"][0] + 20 * bc["flussi"][1] == pytest.approx(
        124444.44444444444)
    assert bc["flussi"][0] + 4 * bc["flussi"][1] == pytest.approx(
        888.8888888888905)


# ---------------------------------------------------------------- varianti
def test_variante_prezzo_el_basso():
    bc = _variante(prezzo_el_eur_kwh=0.10)
    assert bc["risparmio_netto_eur_anno"] == pytest.approx(
        4122.222222222223)
    assert bc["van"] == pytest.approx(21372.00041202593)
    assert bc["tir"] == pytest.approx(12.418723364739485)
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_variante_prezzo_el_marginale():
    bc = _variante(prezzo_el_eur_kwh=0.02)
    assert bc["risparmio_netto_eur_anno"] == pytest.approx(
        2202.222222222222)
    assert bc["van"] == pytest.approx(-2555.443445650844)
    assert bc["van"] < 0.0
    assert abs(bc["van"]) <= 0.10 * 30000
    assert bc["tir"] == pytest.approx(3.9732260457989774)
    assert bc["payback"] == 14
    assert bc["verdetto"] == "MARGINALE"


def test_variante_q_demand_zero_calcolabile():
    bc = _variante(q_demand_kwh_anno=0)
    assert bc["valid"] is True
    assert bc["q_th_used_kwh_anno"] == 0.0
    assert bc["q_th_excess_kwh_anno"] == 60000.0
    assert bc["gas_risparmiato_kwh_anno"] == 0.0
    assert bc["risparmio_gas_eur_anno"] == 0.0
    assert bc["risparmio_netto_eur_anno"] == 5500.0
    assert bc["co2_evitata_t_anno"] == pytest.approx(7.2)
    assert bc["van"] == pytest.approx(38542.156883969896)
    assert bc["tir"] == pytest.approx(17.61939142635338)
    assert bc["payback"] == 6
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx(
        0.020833333333333332)
    assert bc["costo_livellato_eur_kwh"] == pytest.approx(
        0.12113656732169745)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_pareggio_azzera_netto():
    bc = _variante(om_eur_anno=8222.222222222222)
    assert bc["risparmio_netto_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["van"] == pytest.approx(-30000.0)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx(0.25)
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_variante_eta_clamp_sopra_uno():
    bc = _variante(eta_el=1.5, eta_th=1.5)
    assert bc["valid"] is True
    assert bc["eta_el"] == 1.0
    assert bc["eta_th"] == 1.0
    assert bc["e_el_kwh_anno"] == 120000.0
    assert bc["q_th_prod_kwh_anno"] == 120000.0
    assert bc["risparmio_netto_eur_anno"] == pytest.approx(
        31722.222222222223)
    assert bc["van"] == pytest.approx(365329.0058661294)
    assert bc["payback"] == 1
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_eta_caldaia_clamp_sopra_uno():
    bc = _variante(eta_caldaia=1.5)
    assert bc["valid"] is True
    assert bc["eta_caldaia"] == 1.0
    assert bc["gas_risparmiato_kwh_anno"] == 20000.0
    assert bc["risparmio_netto_eur_anno"] == 7500.0
    assert bc["van"] == pytest.approx(63466.57756904985)
    assert bc["tir"] == pytest.approx(24.6974562951089)
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx(-0.0625)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_area_doppia():
    bc = _variante(area_m2=200)
    assert bc["e_el_kwh_anno"] == 48000.0
    assert bc["q_th_prod_kwh_anno"] == 120000.0
    assert bc["q_th_used_kwh_anno"] == 20000.0
    assert bc["risparmio_netto_eur_anno"] == pytest.approx(
        13722.222222222223)
    assert bc["van"] == pytest.approx(141009.21970040974)
    assert bc["tir"] == pytest.approx(45.716185323073255)
    assert bc["payback"] == 3
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_domanda_alta_tutto_utile():
    bc = _variante(q_demand_kwh_anno=100000)
    assert bc["q_th_used_kwh_anno"] == 60000.0
    assert bc["q_th_excess_kwh_anno"] == 0.0
    assert bc["gas_risparmiato_kwh_anno"] == pytest.approx(
        66666.66666666667)
    assert bc["risparmio_netto_eur_anno"] == pytest.approx(
        12166.666666666668)
    assert bc["co2_evitata_t_anno"] == pytest.approx(20.533333333333335)
    assert bc["van"] == pytest.approx(121623.5591675698)
    assert bc["payback"] == 3
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx(
        -0.2569444444444445)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero():
    bc = _variante(wacc_pct=0)
    assert bc["crf"] == pytest.approx(1.0 / 20.0)
    assert bc["quota_capex_eur_anno"] == 1500.0
    assert bc["costo_livellato_eur_kwh"] == pytest.approx(
        0.045454545454545456)
    assert bc["van"] == pytest.approx(124444.44444444441)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex_eur=0)
    assert bc["capex_eur"] == 0
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(96235.95764516987)
    assert bc["costo_livellato_eur_kwh"] == pytest.approx(
        0.011363636363636364)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_vita_dieci():
    bc = _variante(vita_anni=10)
    assert len(bc["flussi"]) == 11
    assert bc["crf"] == pytest.approx(0.12950457496545661)
    assert bc["van"] == pytest.approx(29628.95306426048)
    assert bc["payback"] == 4
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_netto_negativo_calcolabile_non_degenere():
    bc = _variante(prezzo_el_eur_kwh=0.0, prezzo_gas_eur_kwh=0.0)
    assert bc["valid"] is True
    assert bc["risparmio_netto_eur_anno"] == -500.0
    assert bc["van"] == pytest.approx(-36231.10517126998)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx(
        0.020833333333333332)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_pareggio_negativo_demo():
    bc = demo_calcoli()
    assert bc["prezzo_pareggio_eur_kwh"] < 0.0
    assert bc["valid"] is True
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["risparmio_netto_eur_anno"] > 0.0


# ---------------------------------------------------------------- degenere
def test_degenere_area_zero():
    bc = _variante(area_m2=0)
    assert bc["valid"] is False
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"] == []
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_kwh"] is None
    assert bc["costo_livellato_eur_kwh"] is None
    assert bc["errore"]


def test_degenere_irradiazione_eta_vita():
    for kw in ({"h_kwh_m2_anno": 0}, {"eta_el": 0},
               {"eta_el": -0.1}, {"eta_th": 0},
               {"eta_th": -0.1}, {"eta_caldaia": 0},
               {"eta_caldaia": -0.1}, {"vita_anni": 0},
               {"vita_anni": 2.5}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_wacc_tolleranza_prezzi_negativi():
    for kw in ({"wacc_pct": -1}, {"wacc_pct": 60},
               {"tolleranza_pct": -1}, {"tolleranza_pct": 101},
               {"prezzo_el_eur_kwh": -0.01},
               {"prezzo_gas_eur_kwh": -0.01},
               {"om_eur_anno": -100}, {"capex_eur": -1},
               {"q_demand_kwh_anno": -1}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_stringa_nan_inf():
    for kw in ({"area_m2": "100"},
               {"area_m2": float("nan")},
               {"prezzo_el_eur_kwh": float("inf")},
               {"capex_eur": True}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_neutro_campi():
    bc = _variante(area_m2=0)
    assert bc["e_el_kwh_anno"] == 0.0
    assert bc["q_th_prod_kwh_anno"] == 0.0
    assert bc["q_th_used_kwh_anno"] == 0.0
    assert bc["q_th_excess_kwh_anno"] == 0.0
    assert bc["gas_risparmiato_kwh_anno"] == 0.0
    assert bc["risparmio_el_eur_anno"] == 0.0
    assert bc["risparmio_gas_eur_anno"] == 0.0
    assert bc["risparmio_netto_eur_anno"] == 0.0
    assert bc["van"] == 0.0
    assert list(bc["df_flussi"].columns) == [
        "Anno", "Flusso (EUR/anno)", "Cumulato (EUR)"]
    assert list(bc["df_tabella"].columns) == ["Voce", "Valore"]


def test_pareggio_none_quando_e_el_zero():
    assert mh753_prezzo_pareggio(500, 2222.222222222222, 0) is None
    assert mh753_costo_livellato(30000, 0.08024258719069129, 500, 0, 0) is None


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = demo_calcoli()
    testo = mh753_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert "e_el_kwh_anno;24000.0" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "prezzo_pareggio_eur_kwh" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = demo_calcoli()
    testo = mh753_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"quota_capex_eur_anno;{bc['quota_capex_eur_anno']}" in testo
    assert f"e_el_kwh_anno;{bc['e_el_kwh_anno']}" in testo


def test_csv_degenere_solo_zeri():
    bc = _variante(area_m2=0)
    testo = mh753_csv(bc, _demo_kwargs())
    assert "van_eur;0.0" in testo
    assert "e_el_kwh_anno;0.0" in testo
    assert "verdetto;NON_CALCOLABILE" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = demo_calcoli()
    testo = mh753_csv(bc, _demo_kwargs())
    for chiave in _demo_kwargs():
        assert f"{chiave};" in testo


def test_calcola_non_sollevela_per_input_numerici():
    bc = _variante(prezzo_el_eur_kwh=0, prezzo_gas_eur_kwh=0,
                   om_eur_anno=0, f_el_kg_kwh=0, f_gas_kg_kwh=0)
    assert bc["valid"] is True
    assert bc["risparmio_el_eur_anno"] == 0.0
    assert bc["risparmio_gas_eur_anno"] == 0.0
    assert bc["risparmio_netto_eur_anno"] == 0.0


def test_monotonia_prezzo_el():
    base = demo_calcoli()["risparmio_netto_eur_anno"]
    alto = _variante(prezzo_el_eur_kwh=0.30)["risparmio_netto_eur_anno"]
    basso = _variante(prezzo_el_eur_kwh=0.10)["risparmio_netto_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(1200.0)
    assert base - basso == pytest.approx(3600.0)


def test_demo_deterministica_due_chiamate():
    a = demo_calcoli()
    b = demo_calcoli()
    assert a["van"] == b["van"]
    assert a["flussi"] == b["flussi"]
    assert a["tir"] == b["tir"]


def test_demo_chiavi_attese():
    assert set(mh753_demo().keys()) == {
        "area_m2", "h_kwh_m2_anno", "eta_el", "eta_th",
        "q_demand_kwh_anno", "eta_caldaia",
        "prezzo_el_eur_kwh", "prezzo_gas_eur_kwh",
        "om_eur_anno", "capex_eur",
        "f_el_kg_kwh", "f_gas_kg_kwh",
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
    ast.parse(_leggi("w754_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w754_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab753:")


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    # token vietati costruiti per concatenazione, cosi' questo
    # stesso file non li contiene come sottostringhe contigue.
    src = _leggi("w754_helpers.py")
    vietati = ["mh" + "75" + "2", "st" + "75" + "2",
               "tab" + "75" + "2", "75" + "2"]
    assert "streamlit" not in src
    assert all(t not in src for t in vietati)


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w754_ui.py")
    vietati = ["mh" + "75" + "2", "st" + "75" + "2",
               "tab" + "75" + "2", "75" + "2"]
    assert all(t not in src for t in vietati)
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st753_") for c in chiavi)
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
    src = _leggi("w754_test.py")
    vietati = ["mh" + "75" + "2", "st" + "75" + "2",
               "tab" + "75" + "2", "75" + "2"]
    assert all(t not in src for t in vietati)


def test_ui_chiavi_demo_coerenti():
    """Ogni _def753[...] letto dalla UI esiste nel dict demo:
    sweep anti-KeyError a render (lezione dello sweep chiavi demo vs UI)."""
    src = _leggi("w754_ui.py")
    usate = set(re.findall(r'_def753\["([^"]+)"\]', src))
    assert usate
    assert usate <= set(mh753_demo().keys())


def test_ui_riferisce_solo_helper_nuovi():
    src = _leggi("w754_ui.py")
    usati = set(re.findall(r'\b(mh\d+_\w+)\b', src))
    assert usati
    assert all(u.startswith("mh753_") for u in usati)


@pytest.mark.parametrize("wacc,vita,atteso", [
    (5.0, 20, 0.08024258719069129),
    (0, 20, 0.05),
    (10.0, 10, 0.16274539488251152),
    (5.0, 1, 1.05),
    (50.0, 5, 0.5758293838862559),
])
def test_crf_parametrizzato(wacc, vita, atteso):
    assert mh753_crf(wacc, vita) == pytest.approx(atteso)


@pytest.mark.parametrize("campo,valore", [
    ("area_m2", 0), ("area_m2", -3),
    ("h_kwh_m2_anno", 0), ("h_kwh_m2_anno", -100),
    ("eta_el", 0), ("eta_el", -0.5),
    ("eta_th", 0), ("eta_th", -0.5),
    ("q_demand_kwh_anno", -1),
    ("eta_caldaia", 0), ("eta_caldaia", -0.5),
    ("prezzo_el_eur_kwh", -0.01),
    ("prezzo_gas_eur_kwh", -0.01),
    ("om_eur_anno", -100), ("capex_eur", -1),
    ("f_el_kg_kwh", -0.30), ("f_gas_kg_kwh", -0.20),
    ("wacc_pct", -0.1), ("wacc_pct", 50.1),
    ("vita_anni", -1), ("vita_anni", 2.5),
    ("tolleranza_pct", -1), ("tolleranza_pct", 100.1),
])
def test_valida_rifiuta_singoli_campi(campo, valore):
    d = _demo_kwargs()
    d[campo] = valore
    assert mh753_valida(**d)["valido"] is False


def test_df_tabella_valori_demo_selezionati():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Area (m2)"] == 100.0
    assert mappa["Energia elettrica (kWh/anno)"] == 24000.0
    assert mappa["Risparmio netto (EUR/anno)"] == pytest.approx(
        7722.222222222223)
    assert mappa["Payback (anni)"] == 4
    assert mappa["Verdetto"] == "CONVIENTE"
