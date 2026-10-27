"""Test tab752 "Accumulo a gravita': sollevare pesi quando
l'energia costa poco, venderla quando costa tanto?"

Nuova tab tab752 (accumulo a
gravita', w753). Business case
deterministico di un sistema di
accumulo a gravita' che fa
arbitraggio di prezzo: massa
sollevata, altezza, energia
potenziale per ciclo, eta di
carica e scarica con clamp in
[0, 1], cicli annui, energia
erogata e assorbita annue, costo
di ricarica a prezzo off-peak
contro ricavo di vendita a prezzo
peak, margine, CO2 evitata come
CO2 erogata meno CO2 assorbita,
CAPEX, VAN, TIR, payback
(primo anno con cumulato >= 0),
costo livellato dell'accumulo e
prezzo peak di pareggio. Distinta
dalle batterie (accumulo
elettrochimico, non masse
sollevate), dall'ATES (accumulo
stagionale in acquifero, non
sollevamento), dal pompaggio
idroelettrico (acqua tra bacini,
non masse solide) e dal calore
di scarto (recupero termico, non
accumulo meccanico): qui masse
solide sollevate e abbassate con
arbitraggio off-peak contro peak.

Demo calcolata eseguendo demo_calcoli()
(e ricontrollata a mano, riga per riga):
sistema da 8000 t sollevate a
150 m, eta carica 0,90 e eta
scarica 0,90, 2 cicli al giorno
per 350 giorni all'anno, prezzo
off-peak 0,08 EUR/kWh e prezzo
peak 0,22 EUR/kWh, O&M 60000
EUR/anno, CAPEX 2000000 EUR,
fattore off-peak 0,30 kg/kWh e
fattore peak 0,35 kg/kWh, WACC
5 %, vita 25 anni, tolleranza
10 % del CAPEX.

- massa_kg = 8000000.0
- e_pot_kwh = 3270.0
- e_erogata_ciclo_kwh = 2943.0
- e_assorbita_ciclo_kwh = 3633.333333333333
- cicli_anno = 700.0
- e_out_anno_kwh = 2060100.0
- e_in_anno_kwh = 2543333.333333333
- costo_ricarica_eur = 203466.66666666666
- ricavo_vendita_eur = 453222.0
- margine_eur_anno = 189755.33333333334
- co2_erogata_t = 721.035
- co2_assorbita_t = 762.9999999999999
- co2_evitata_t = -41.96499999999992
- capex_totale_eur = 2000000.0
- crf = 0.0709524572992296
- quota_capex_eur = 141904.9145984592
- costo_livellato_eur_kwh = 0.19677276892632684
- van = 674401.149111344
- tir = 8.149462358515787
- payback = 11
- prezzo_pareggio_eur_kwh = 0.127890231865767
- verdetto = 'CONVIENTE'

Scomposizione: E_pot = 8000000 x
9,81 x 150 / 3600000 = 3270 kWh
per ciclo; E_erogata per ciclo =
3270 x 0,90 = 2943 kWh; E_assorbita
per ciclo = 3270 / 0,90 =
3633,33 kWh; cicli annui = 2 x
350 = 700; E_out annua = 2943 x
700 = 2060100 kWh; E_in annua =
3633,33 x 700 = 2543333,33 kWh;
costo ricarica = 2543333,33 x
0,08 = 203466,67 EUR; ricavo =
2060100 x 0,22 = 453222,00 EUR;
margine = 453222,00 - 203466,67 -
60000 = 189755,33 EUR/anno; CO2
erogata = 2060100 x 0,35 / 1000 =
721,04 t; CO2 assorbita =
2543333,33 x 0,30 / 1000 = 763,00
t; evitata = -41,96 t (negativa:
l'energia di ricarica e' piu'
sporca di quella venduta e il
round-trip 0,81 fa comprare piu'
energia di quanta se ne venda);
CAPEX 2000000 EUR; CRF 0,05 x
1,05^25 / (1,05^25 - 1) =
0.0709524572992296; quota CAPEX
2000000 x 0,070952 = 141904,91
EUR/anno; costo livellato
(141904,91 + 60000 + 203466,67) /
2060100 = 0,1968 EUR/kWh contro
prezzo peak 0,22; flussi: anno 0
-2000000, anni 1-25 margine
189755,33 (piatti); VAN -2000000
+ 189755,33 x 14,09394457 (annuita'
25 anni al 5 %) = 674401,15 EUR;
TIR circa 8,15 %; payback 11 anni
(il cumulato all'anno 10 e'
-102446,67, all'anno 11 e'
87308,67); prezzo peak di pareggio
(203466,67 + 60000) / 2060100 =
0,127890231865767 EUR/kWh;
verdetto CONVIENTE perche' VAN > 0.
NOTA: il CRF entra solo nel costo
livellato, mai nei flussi: il CAPEX
compare una sola volta, all'anno 0.
NOTA 2: in questo brief il margine
nullo o negativo NON e' degenere:
al prezzo di pareggio il margine
si azzera (0 EUR/anno) e il caso
resta calcolabile (valid=True, VAN
-2000000 EUR, NON_CONVIENTE perche'
|VAN| = 2000000 > 10 % di 2000000).
NOTA 3: la CO2 evitata negativa
NON e' degenere di per se': se il
margine resta > 0 il caso resta
calcolabile e la CO2 evitata
negativa va detta (demo: -41,96 t,
valid=True, CONVIENTE).
NOTA 4: il prezzo di pareggio segue
la formula del brief (vedi
test_prezzo_pareggio): con gli input
demo vale 0,127890231865767
EUR/kWh, non 0,22: 0,22 e' il
prezzo peak pagato, il pareggio e'
il prezzo al quale il margine si
azzera ((203466,67 + 60000) /
2060100). NOTA 5: le eta sopra 1
vengono clampate a 1 (vedi
test_eta_clamp): non e' un errore,
e' la regola del brief.
"""

import ast
import math
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w753_helpers import (
    demo_calcoli,
    mh752_calcola,
    mh752_cicli_anno,
    mh752_co2_assorbita,
    mh752_co2_erogata,
    mh752_co2_evitata,
    mh752_costo_livellato,
    mh752_costo_ricarica,
    mh752_crf,
    mh752_csv,
    mh752_demo,
    mh752_e_assorbita,
    mh752_e_erogata,
    mh752_e_in_anno,
    mh752_e_out_anno,
    mh752_e_pot,
    mh752_eta,
    mh752_flussi,
    mh752_int_nneg,
    mh752_int_pos,
    mh752_margine,
    mh752_massa_kg,
    mh752_nneg,
    mh752_num,
    mh752_pct_0_100,
    mh752_pct_wacc,
    mh752_pos,
    mh752_prezzo_pareggio,
    mh752_quota_capex,
    mh752_ricavo_vendita,
    mh752_tir,
    mh752_valida,
    mh752_van,
    mh752_verdetto,
    mh752_payback,
)


def _demo_kwargs():
    return dict(mh752_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh752_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh752_num(3, "x") == 3.0
    assert mh752_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh752_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh752_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh752_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh752_pos(0, "x")
    with pytest.raises(ValueError):
        mh752_pos(-1, "x")
    assert mh752_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh752_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh752_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh752_int_pos(0, "x")


def test_int_nneg_zero_ok():
    assert mh752_int_nneg(0, "x") == 0
    with pytest.raises(ValueError):
        mh752_int_nneg(-1, "x")


def test_pct_0_100_limiti():
    assert mh752_pct_0_100(0, "x") == 0.0
    assert mh752_pct_0_100(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh752_pct_0_100(100.1, "x")
    with pytest.raises(ValueError):
        mh752_pct_0_100(-1, "x")


def test_pct_wacc_limiti():
    assert mh752_pct_wacc(0, "x") == 0.0
    assert mh752_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh752_pct_wacc(50.1, "x")


def test_eta_clamp():
    assert mh752_eta(0.90, "x") == 0.90
    assert mh752_eta(1.0, "x") == 1.0
    assert mh752_eta(1.5, "x") == 1.0
    with pytest.raises(ValueError):
        mh752_eta(0, "x")
    with pytest.raises(ValueError):
        mh752_eta(-0.1, "x")


def test_massa_kg():
    assert mh752_massa_kg(8000) == 8000000.0
    assert mh752_massa_kg(0.5) == 500.0
    with pytest.raises(ValueError):
        mh752_massa_kg(0)


# ---------------------------------------------------------------- fisica base
def test_e_pot():
    assert mh752_e_pot(8000000.0, 150) == 3270.0
    assert mh752_e_pot(8000000.0, 100) == 2180.0
    with pytest.raises(ValueError):
        mh752_e_pot(0, 150)
    with pytest.raises(ValueError):
        mh752_e_pot(8000000.0, 0)


def test_e_erogata_e_assorbita_e_clamp():
    assert mh752_e_erogata(3270.0, 0.90) == pytest.approx(2943.0)
    assert mh752_e_assorbita(3270.0, 0.90) == pytest.approx(3633.333333333333)
    assert mh752_e_erogata(3270.0, 1.5) == 3270.0
    assert mh752_e_assorbita(3270.0, 1.5) == 3270.0
    assert mh752_e_erogata(0.0, 0.90) == 0.0
    with pytest.raises(ValueError):
        mh752_e_erogata(3270.0, 0)
    with pytest.raises(ValueError):
        mh752_e_assorbita(3270.0, 0)


def test_cicli_anno():
    assert mh752_cicli_anno(2, 350) == 700.0
    assert mh752_cicli_anno(1.5, 350) == 525.0
    with pytest.raises(ValueError):
        mh752_cicli_anno(0, 350)
    with pytest.raises(ValueError):
        mh752_cicli_anno(2, 0)
    with pytest.raises(ValueError):
        mh752_cicli_anno(2, 350.5)


def test_e_out_e_in_anno():
    assert mh752_e_out_anno(2943.0, 700) == 2060100.0
    assert mh752_e_in_anno(3633.333333333333, 700) == pytest.approx(
        2543333.333333333)
    assert mh752_e_out_anno(0.0, 700) == 0.0


def test_costo_ricarica_e_ricavo():
    assert mh752_costo_ricarica(2543333.333333333, 0.08) == pytest.approx(
        203466.66666666666)
    assert mh752_ricavo_vendita(2060100.0, 0.22) == 453222.0
    assert mh752_costo_ricarica(0.0, 0.08) == 0.0


def test_margine():
    assert mh752_margine(453222.0, 203466.66666666666, 60000) == pytest.approx(
        189755.33333333334)
    assert mh752_margine(453222.0, 453222.0, 60000) == -60000.0


def test_co2_erogata_assorbita_evitata():
    assert mh752_co2_erogata(2060100.0, 0.35) == pytest.approx(721.035)
    assert mh752_co2_assorbita(2543333.333333333, 0.30) == pytest.approx(
        763.0)
    assert mh752_co2_evitata(721.035, 763.0) == pytest.approx(-41.965)


def test_co2_evitata_segno_libero():
    assert mh752_co2_evitata(721.035, 0.0) == pytest.approx(721.035)


# ---------------------------------------------------------------- finanza base
def test_crf():
    assert mh752_crf(5.0, 25) == pytest.approx(0.0709524572992296)
    assert mh752_crf(0, 25) == pytest.approx(1.0 / 25.0)
    assert mh752_crf(5.0, 1) == pytest.approx(1.05)
    assert mh752_crf(5.0, 10) == pytest.approx(0.1295045749654566)


def test_quota_capex_e_livellato():
    assert mh752_quota_capex(2000000, 0.0709524572992296) == pytest.approx(
        141904.9145984592)
    assert mh752_costo_livellato(2000000, 0.0709524572992296, 60000,
                                 203466.66666666666,
                                 2060100.0) == pytest.approx(
        0.19677276892632684)
    assert mh752_costo_livellato(2000000, 0.0709524572992296, 60000,
                                 203466.66666666666, 0) is None
    assert mh752_costo_livellato(0, 0.0709524572992296, 60000,
                                 203466.66666666666,
                                 2060100.0) == pytest.approx(
        0.127890231865767)


def test_prezzo_pareggio_formula_brief():
    assert mh752_prezzo_pareggio(203466.66666666666, 60000,
                                 2060100.0) == pytest.approx(
        0.127890231865767)
    assert mh752_prezzo_pareggio(203466.66666666666, 60000, 0) is None
    assert mh752_prezzo_pareggio(0.0, 0, 2060100.0) == 0.0


def test_flussi_lunghezza_e_primo():
    fl = mh752_flussi(2000000, 189755.33333333334, 25)
    assert len(fl) == 26
    assert fl[0] == -2000000
    assert all(f == 189755.33333333334 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = demo_calcoli()
    assert bc["van"] == pytest.approx(674401.149111344)
    assert mh752_van([-2000000] + [189755.33333333334] * 25,
                     0) == pytest.approx(2743883.3333333335)
    assert mh752_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo_e_conviente():
    bc = demo_calcoli()
    assert bc["tir"] == pytest.approx(8.149462358515787)
    assert mh752_tir([-2000000] + [189755.33333333334] * 25) == pytest.approx(
        0.08149462358515787)
    tir = mh752_tir([-2000000] + [189755.33333333334] * 25)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-2000000] + [189755.33333333334] * 25))
    assert npv == pytest.approx(0.0, abs=1e-4)


def test_payback():
    assert mh752_payback([-2000000] + [189755.33333333334] * 25) == 11
    assert mh752_payback([-2000000] + [80.0] * 25) is None
    assert mh752_payback([0] + [189755.33333333334] * 25) == 0
    assert mh752_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh752_verdetto(100.0, 2000000, 10.0) == "CONVIENTE"
    assert mh752_verdetto(-100831.62, 2000000, 10.0) == "MARGINALE"
    assert mh752_verdetto(-200000.0, 2000000, 10.0) == "MARGINALE"
    assert mh752_verdetto(-200000.01, 2000000, 10.0) == "NON_CONVIENTE"
    assert mh752_verdetto(-674401.15, 2000000, 10.0) == "NON_CONVIENTE"
    assert mh752_verdetto(float("nan"), 2000000, 10.0) == "NON_CALCOLABILE"
    assert mh752_verdetto(0.0, 0, 10.0) == "MARGINALE"


def test_valida_demo_ok():
    v = mh752_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("massa_t", "8000"),
                       ("massa_t", float("nan")),
                       ("massa_t", float("inf")),
                       ("massa_t", True),
                       ("prezzo_peak_eur_kwh", None)):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh752_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("massa_t", 0),
                          ("altezza_m", 0),
                          ("eta_carica", 0),
                          ("eta_carica", -0.1),
                          ("eta_scarica", 0),
                          ("eta_scarica", -0.1),
                          ("cicli_giorno", 0),
                          ("giorni_anno", 0),
                          ("giorni_anno", 350.5),
                          ("prezzo_offpeak_eur_kwh", -0.01),
                          ("prezzo_peak_eur_kwh", 0),
                          ("prezzo_peak_eur_kwh", -0.01),
                          ("om_eur_anno", -100),
                          ("capex_eur", -1),
                          ("f_offpeak_kg_kwh", -0.30),
                          ("f_peak_kg_kwh", -0.35),
                          ("wacc_pct", -0.1), ("wacc_pct", 50.1),
                          ("vita_anni", 0), ("vita_anni", 2.5),
                          ("tolleranza_pct", -1),
                          ("tolleranza_pct", 100.1)):
        d = _demo_kwargs()
        d[campo] = valore
        assert mh752_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"prezzo_offpeak_eur_kwh": 0, "om_eur_anno": 0,
              "capex_eur": 0, "f_offpeak_kg_kwh": 0,
              "f_peak_kg_kwh": 0, "wacc_pct": 0,
              "tolleranza_pct": 0, "eta_carica": 1.0,
              "eta_scarica": 1.0})
    assert mh752_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    assert mh752_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh752_demo()
    assert d["massa_t"] == 8000
    assert d["altezza_m"] == 150
    assert d["eta_carica"] == 0.90
    assert d["eta_scarica"] == 0.90
    assert d["cicli_giorno"] == 2
    assert d["giorni_anno"] == 350
    assert d["prezzo_offpeak_eur_kwh"] == 0.08
    assert d["prezzo_peak_eur_kwh"] == 0.22
    assert d["om_eur_anno"] == 60000
    assert d["capex_eur"] == 2000000
    assert d["f_offpeak_kg_kwh"] == 0.30
    assert d["f_peak_kg_kwh"] == 0.35
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 25
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    """Ogni _DEMO del test contro demo_calcoli():
    scarto relativo < 1e-9 (zero atteso:
    confronto assoluto)."""
    bc = demo_calcoli()
    attesi = {
        "massa_kg": 8000000.0,
        "e_pot_kwh": 3270.0,
        "e_erogata_ciclo_kwh": 2943.0,
        "e_assorbita_ciclo_kwh": 3633.333333333333,
        "cicli_anno": 700.0,
        "e_out_anno_kwh": 2060100.0,
        "e_in_anno_kwh": 2543333.333333333,
        "costo_ricarica_eur": 203466.66666666666,
        "ricavo_vendita_eur": 453222.0,
        "margine_eur_anno": 189755.33333333334,
        "co2_erogata_t": 721.035,
        "co2_assorbita_t": 762.9999999999999,
        "co2_evitata_t": -41.96499999999992,
        "capex_totale_eur": 2000000.0,
        "crf": 0.0709524572992296,
        "quota_capex_eur": 141904.9145984592,
        "costo_livellato_eur_kwh": 0.19677276892632684,
        "van": 674401.149111344,
        "tir": 8.149462358515787,
        "prezzo_pareggio_eur_kwh": 0.127890231865767,
    }
    for chiave, atteso in attesi.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert abs(got - atteso) / abs(atteso) < 1e-9, chiave
    assert bc["payback"] == 11
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_demo_calcoli_fisica():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["massa_kg"] == 8000000.0
    assert bc["e_pot_kwh"] == 3270.0
    assert bc["e_erogata_ciclo_kwh"] == pytest.approx(2943.0)
    assert bc["e_assorbita_ciclo_kwh"] == pytest.approx(3633.333333333333)
    assert bc["cicli_anno"] == 700.0
    assert bc["e_out_anno_kwh"] == 2060100.0
    assert bc["e_in_anno_kwh"] == pytest.approx(2543333.333333333)
    assert bc["co2_erogata_t"] == pytest.approx(721.035)
    assert bc["co2_assorbita_t"] == pytest.approx(763.0)
    assert bc["co2_evitata_t"] == pytest.approx(-41.965)


def test_demo_calcoli_economia():
    bc = demo_calcoli()
    assert bc["costo_ricarica_eur"] == pytest.approx(203466.66666666666)
    assert bc["ricavo_vendita_eur"] == 453222.0
    assert bc["margine_eur_anno"] == pytest.approx(189755.33333333334)
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx(
        0.127890231865767)


def test_demo_calcoli_finanza():
    bc = demo_calcoli()
    assert bc["capex_totale_eur"] == 2000000.0
    assert bc["crf"] == pytest.approx(0.0709524572992296)
    assert bc["quota_capex_eur"] == pytest.approx(141904.9145984592)
    assert bc["costo_livellato_eur_kwh"] == pytest.approx(
        0.19677276892632684)
    assert bc["van"] == pytest.approx(674401.149111344)
    assert bc["tir"] == pytest.approx(8.149462358515787)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "CONVIENTE"


def test_demo_flussi_e_cumulato():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -2000000
    assert len(bc["flussi"]) == 26
    assert all(f == 189755.33333333334 for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -2000000
    assert righe.iloc[10]["Cumulato (EUR)"] == pytest.approx(-102446.66666666657)
    assert righe.iloc[11]["Cumulato (EUR)"] == pytest.approx(87308.66666666677)
    assert righe.iloc[25]["Cumulato (EUR)"] == pytest.approx(
        2743883.3333333335)
    assert righe.iloc[25]["Flusso (EUR/anno)"] == 189755.33333333334


def test_demo_tabella_righe():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["E potenziale (kWh/ciclo)"] == 3270.0
    assert mappa["E erogata (kWh/anno)"] == 2060100.0
    assert mappa["Margine (EUR/anno)"] == pytest.approx(189755.33333333334)
    assert mappa["CAPEX totale (EUR)"] == 2000000.0
    assert mappa["Payback (anni)"] == 11
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Prezzo peak di pareggio (EUR/kWh)"] == pytest.approx(
        0.127890231865767)


def test_demo_coerenza_interna():
    bc = demo_calcoli()
    assert bc["ricavo_vendita_eur"] - bc["costo_ricarica_eur"] - \
        bc["om_eur_anno"] == pytest.approx(bc["margine_eur_anno"])
    assert bc["co2_erogata_t"] - bc["co2_assorbita_t"] == pytest.approx(
        bc["co2_evitata_t"])
    assert bc["e_erogata_ciclo_kwh"] / bc["e_assorbita_ciclo_kwh"] == \
        pytest.approx(0.81)
    assert bc["capex_totale_eur"] * bc["crf"] == pytest.approx(
        bc["quota_capex_eur"])
    assert (bc["quota_capex_eur"] + bc["om_eur_anno"] +
            bc["costo_ricarica_eur"]) / bc["e_out_anno_kwh"] == \
        pytest.approx(bc["costo_livellato_eur_kwh"])
    assert bc["costo_ricarica_eur"] + bc["om_eur_anno"] == pytest.approx(
        bc["prezzo_pareggio_eur_kwh"] * bc["e_out_anno_kwh"])


def test_demo_crf_solo_nel_livellato_non_nei_flussi():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -bc["capex_totale_eur"]
    assert all(f == bc["margine_eur_anno"] for f in bc["flussi"][1:])
    assert bc["crf"] not in bc["flussi"]
    assert bc["quota_capex_eur"] not in bc["flussi"]
    van_da_flussi = mh752_van(bc["flussi"], bc["wacc_pct"])
    assert van_da_flussi == pytest.approx(bc["van"])
    assert bc["costo_livellato_eur_kwh"] == pytest.approx(
        (bc["capex_totale_eur"] * bc["crf"] + bc["om_eur_anno"] +
         bc["costo_ricarica_eur"]) / bc["e_out_anno_kwh"])


def test_demo_contro_riconteggio_indipendente():
    m, h = 8000000.0, 150
    ec, es = 0.90, 0.90
    cg, ga = 2, 350
    po, pp = 0.08, 0.22
    om, cx = 60000, 2000000
    fo, fp = 0.30, 0.35
    wacc, vita = 5.0, 25
    ep = m * 9.81 * h / 3600000.0
    eo_c = ep * es
    ea_c = ep / ec
    ca = cg * ga
    eo = eo_c * ca
    ea = ea_c * ca
    cr = ea * po
    rv = eo * pp
    mg = rv - cr - om
    co2e = eo * fp / 1000.0
    co2a = ea * fo / 1000.0
    r = wacc / 100.0
    crf = r * (1 + r) ** vita / ((1 + r) ** vita - 1)
    van = -cx + sum(mg / (1 + r) ** t for t in range(1, vita + 1))
    bc = demo_calcoli()
    assert bc["e_pot_kwh"] == ep
    assert bc["e_erogata_ciclo_kwh"] == eo_c
    assert bc["e_assorbita_ciclo_kwh"] == ea_c
    assert bc["costo_ricarica_eur"] == cr
    assert bc["ricavo_vendita_eur"] == rv
    assert bc["margine_eur_anno"] == mg
    assert bc["co2_erogata_t"] == co2e
    assert bc["co2_assorbita_t"] == co2a
    assert bc["crf"] == pytest.approx(crf)
    assert bc["van"] == pytest.approx(van)
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx((cr + om) / eo)


def test_demo_riconteggio_crf_van_payback_pareggio_a_mano():
    bc = demo_calcoli()
    r = 0.05
    annuita = (1 - (1 + r) ** -25) / r
    assert annuita == pytest.approx(14.093944566861066)
    assert bc["van"] == pytest.approx(-2000000 + 189755.33333333334 * annuita)
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx(
        263466.66666666666 / 2060100.0)
    assert bc["flussi"][0] + 25 * bc["flussi"][1] == pytest.approx(
        2743883.3333333335)
    assert bc["flussi"][0] + 11 * bc["flussi"][1] == pytest.approx(
        87308.66666666677)


# ---------------------------------------------------------------- varianti
def test_variante_prezzo_peak_basso():
    bc = _variante(prezzo_peak_eur_kwh=0.15)
    assert bc["margine_eur_anno"] == pytest.approx(45548.33333333334)
    assert bc["van"] == pytest.approx(-1358044.3149242718)
    assert bc["tir"] == pytest.approx(-3.9337880756313)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_variante_prezzo_peak_marginale():
    bc = _variante(prezzo_peak_eur_kwh=0.1933)
    assert bc["margine_eur_anno"] == pytest.approx(134750.66333333336)
    assert bc["van"] == pytest.approx(-100831.6207422408)
    assert bc["van"] < 0.0
    assert abs(bc["van"]) <= 0.10 * 2000000
    assert bc["tir"] == pytest.approx(4.490821657368824)
    assert bc["payback"] == 15
    assert bc["verdetto"] == "MARGINALE"


def test_variante_prezzo_peak_negativo_margine():
    bc = _variante(prezzo_peak_eur_kwh=0.10)
    assert bc["margine_eur_anno"] == pytest.approx(-57456.66666666666)
    assert bc["van"] == pytest.approx(-2809791.074949711)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_pareggio_azzera_margine():
    bc = _variante(prezzo_peak_eur_kwh=0.127890231865767)
    assert bc["margine_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["van"] == pytest.approx(-2000000.0)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_variante_eta_clamp_sopra_uno():
    bc = _variante(eta_carica=1.5, eta_scarica=1.5)
    assert bc["valid"] is True
    assert bc["eta_carica"] == 1.0
    assert bc["eta_scarica"] == 1.0
    assert bc["e_erogata_ciclo_kwh"] == 3270.0
    assert bc["e_assorbita_ciclo_kwh"] == 3270.0
    assert bc["margine_eur_anno"] == 260460.0
    assert bc["van"] == pytest.approx(1670908.8016720156)
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_massa_doppia():
    bc = _variante(massa_t=16000)
    assert bc["e_pot_kwh"] == 6540.0
    assert bc["e_out_anno_kwh"] == 4120200.0
    assert bc["margine_eur_anno"] == pytest.approx(439510.6666666667)
    assert bc["van"] == pytest.approx(4194438.972185372)
    assert bc["payback"] == 5
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero():
    bc = _variante(wacc_pct=0)
    assert bc["crf"] == pytest.approx(1.0 / 25.0)
    assert bc["quota_capex_eur"] == 80000.0
    assert bc["costo_livellato_eur_kwh"] == pytest.approx(
        0.16672329822176915)
    assert bc["van"] == pytest.approx(2743883.3333333335)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex_eur=0)
    assert bc["capex_totale_eur"] == 0
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(2674401.1491113445)
    assert bc["costo_livellato_eur_kwh"] == pytest.approx(
        0.127890231865767)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_vita_dieci():
    bc = _variante(vita_anni=10)
    assert len(bc["flussi"]) == 11
    assert bc["crf"] == pytest.approx(0.1295045749654566)
    assert bc["van"] == pytest.approx(-534759.6146008929)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_om_alto():
    bc = _variante(om_eur_anno=150000)
    assert bc["margine_eur_anno"] == pytest.approx(99755.33333333334)
    assert bc["van"] == pytest.approx(-594053.861832684)
    assert bc["payback"] == 21
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx(
        0.17157743151626942)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_cicli_uno():
    bc = _variante(cicli_giorno=1)
    assert bc["cicli_anno"] == 350.0
    assert bc["e_out_anno_kwh"] == 1030050.0
    assert bc["margine_eur_anno"] == pytest.approx(64877.66666666667)
    assert bc["van"] == pytest.approx(-1085617.7624256704)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_fattore_offpeak_zero():
    bc = _variante(f_offpeak_kg_kwh=0.0)
    assert bc["co2_assorbita_t"] == 0.0
    assert bc["co2_evitata_t"] == pytest.approx(721.035)
    assert bc["margine_eur_anno"] == pytest.approx(189755.33333333334)


def test_variante_altezza_cento():
    bc = _variante(altezza_m=100)
    assert bc["e_pot_kwh"] == 2180.0
    assert bc["e_out_anno_kwh"] == 1373400.0
    assert bc["margine_eur_anno"] == pytest.approx(106503.55555555556)
    assert bc["van"] == pytest.approx(-498944.7919133323)
    assert bc["payback"] == 19
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_margine_negativo_calcolabile_non_degenere():
    bc = _variante(prezzo_peak_eur_kwh=0.10)
    assert bc["valid"] is True
    assert bc["margine_eur_anno"] < 0.0
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["payback"] is None


def test_variante_co2_negativa_ma_calcolabile():
    bc = demo_calcoli()
    assert bc["co2_evitata_t"] == pytest.approx(-41.965)
    assert bc["valid"] is True
    assert bc["verdetto"] == "CONVIENTE"


# ---------------------------------------------------------------- degenere
def test_degenere_massa_zero():
    bc = _variante(massa_t=0)
    assert bc["valid"] is False
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"] == []
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_kwh"] is None
    assert bc["costo_livellato_eur_kwh"] is None
    assert bc["errore"]


def test_degenere_altezza_eta_cicli_giorni_peak():
    for kw in ({"altezza_m": 0}, {"eta_carica": 0},
               {"eta_carica": -0.1}, {"eta_scarica": 0},
               {"eta_scarica": -0.1}, {"cicli_giorno": 0},
               {"giorni_anno": 0}, {"giorni_anno": 350.5},
               {"prezzo_peak_eur_kwh": 0},
               {"prezzo_peak_eur_kwh": -0.01}):
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
    for kw in ({"massa_t": "8000"},
               {"massa_t": float("nan")},
               {"prezzo_peak_eur_kwh": float("inf")},
               {"capex_eur": True}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_neutro_campi():
    bc = _variante(massa_t=0)
    assert bc["e_pot_kwh"] == 0.0
    assert bc["e_erogata_ciclo_kwh"] == 0.0
    assert bc["e_assorbita_ciclo_kwh"] == 0.0
    assert bc["e_out_anno_kwh"] == 0.0
    assert bc["e_in_anno_kwh"] == 0.0
    assert bc["costo_ricarica_eur"] == 0.0
    assert bc["ricavo_vendita_eur"] == 0.0
    assert bc["margine_eur_anno"] == 0.0
    assert bc["van"] == 0.0
    assert list(bc["df_flussi"].columns) == [
        "Anno", "Flusso (EUR/anno)", "Cumulato (EUR)"]
    assert list(bc["df_tabella"].columns) == ["Voce", "Valore"]


def test_pareggio_none_quando_e_out_zero():
    assert mh752_prezzo_pareggio(203466.66666666666, 60000, 0) is None
    assert mh752_costo_livellato(2000000, 0.0709524572992296, 60000,
                                 203466.66666666666, 0) is None


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = demo_calcoli()
    testo = mh752_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert "e_pot_kwh;3270.0" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "prezzo_pareggio_eur_kwh" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = demo_calcoli()
    testo = mh752_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"capex_totale_eur;{bc['capex_totale_eur']}" in testo
    assert f"e_out_anno_kwh;{bc['e_out_anno_kwh']}" in testo


def test_csv_degenere_solo_zeri():
    bc = _variante(massa_t=0)
    testo = mh752_csv(bc, _demo_kwargs())
    assert "van_eur;0.0" in testo
    assert "e_pot_kwh;0.0" in testo
    assert "verdetto;NON_CALCOLABILE" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = demo_calcoli()
    testo = mh752_csv(bc, _demo_kwargs())
    for chiave in _demo_kwargs():
        assert f"{chiave};" in testo


def test_calcola_non_sollevela_per_input_numerici():
    bc = _variante(prezzo_offpeak_eur_kwh=0, om_eur_anno=0,
                   f_offpeak_kg_kwh=0, f_peak_kg_kwh=0)
    assert bc["valid"] is True
    assert bc["costo_ricarica_eur"] == 0.0
    assert bc["ricavo_vendita_eur"] == 453222.0
    assert bc["margine_eur_anno"] == 453222.0


def test_monotonia_prezzo_peak():
    base = demo_calcoli()["margine_eur_anno"]
    alto = _variante(prezzo_peak_eur_kwh=0.30)["margine_eur_anno"]
    basso = _variante(prezzo_peak_eur_kwh=0.15)["margine_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(164808.0)
    assert base - basso == pytest.approx(144207.0)


def test_demo_deterministica_due_chiamate():
    a = demo_calcoli()
    b = demo_calcoli()
    assert a["van"] == b["van"]
    assert a["flussi"] == b["flussi"]
    assert a["tir"] == b["tir"]


def test_demo_chiavi_attese():
    assert set(mh752_demo().keys()) == {
        "massa_t", "altezza_m", "eta_carica", "eta_scarica",
        "cicli_giorno", "giorni_anno",
        "prezzo_offpeak_eur_kwh", "prezzo_peak_eur_kwh",
        "om_eur_anno", "capex_eur",
        "f_offpeak_kg_kwh", "f_peak_kg_kwh",
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
    ast.parse(_leggi("w753_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w753_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab752:")


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    # token vietati costruiti per concatenazione, cosi' questo
    # stesso file non li contiene come sottostringhe contigue.
    src = _leggi("w753_helpers.py")
    vietati = ["mh" + "75" + "1", "st" + "75" + "1",
               "tab" + "75" + "1", "75" + "1"]
    assert "streamlit" not in src
    assert all(t not in src for t in vietati)


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w753_ui.py")
    vietati = ["mh" + "75" + "1", "st" + "75" + "1",
               "tab" + "75" + "1", "75" + "1"]
    assert all(t not in src for t in vietati)
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st752_") for c in chiavi)
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
    src = _leggi("w753_test.py")
    vietati = ["mh" + "75" + "1", "st" + "75" + "1",
               "tab" + "75" + "1", "75" + "1"]
    assert all(t not in src for t in vietati)


def test_ui_chiavi_demo_coerenti():
    """Ogni _def752[...] letto dalla UI esiste nel dict demo:
    sweep anti-KeyError a render (lezione dello sweep chiavi demo vs UI)."""
    src = _leggi("w753_ui.py")
    usate = set(re.findall(r'_def752\["([^"]+)"\]', src))
    assert usate
    assert usate <= set(mh752_demo().keys())


def test_ui_riferisce_solo_helper_nuovi():
    src = _leggi("w753_ui.py")
    usati = set(re.findall(r'\b(mh\d+_\w+)\b', src))
    assert usati
    assert all(u.startswith("mh752_") for u in usati)


@pytest.mark.parametrize("wacc,vita,atteso", [
    (5.0, 25, 0.0709524572992296),
    (0, 25, 0.04),
    (10.0, 10, 0.16274539488251152),
    (5.0, 1, 1.05),
    (50.0, 5, 0.5758293838862559),
])
def test_crf_parametrizzato(wacc, vita, atteso):
    assert mh752_crf(wacc, vita) == pytest.approx(atteso)


@pytest.mark.parametrize("campo,valore", [
    ("massa_t", 0), ("massa_t", -3),
    ("altezza_m", 0), ("altezza_m", -100),
    ("eta_carica", 0), ("eta_carica", -0.5),
    ("eta_scarica", 0), ("eta_scarica", -0.5),
    ("cicli_giorno", 0), ("cicli_giorno", -1),
    ("giorni_anno", 0), ("giorni_anno", 350.5),
    ("prezzo_offpeak_eur_kwh", -0.01),
    ("prezzo_peak_eur_kwh", 0), ("prezzo_peak_eur_kwh", -0.01),
    ("om_eur_anno", -100), ("capex_eur", -1),
    ("f_offpeak_kg_kwh", -0.30), ("f_peak_kg_kwh", -0.35),
    ("wacc_pct", -0.1), ("wacc_pct", 50.1),
    ("vita_anni", -1), ("vita_anni", 2.5),
    ("tolleranza_pct", -1), ("tolleranza_pct", 100.1),
])
def test_valida_rifiuta_singoli_campi(campo, valore):
    d = _demo_kwargs()
    d[campo] = valore
    assert mh752_valida(**d)["valido"] is False


def test_df_tabella_valori_demo_selezionati():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Massa (t)"] == 8000.0
    assert mappa["E erogata (kWh/anno)"] == 2060100.0
    assert mappa["Margine (EUR/anno)"] == pytest.approx(189755.33333333334)
    assert mappa["CAPEX totale (EUR)"] == 2000000.0
    assert mappa["Payback (anni)"] == 11
    assert mappa["Verdetto"] == "CONVIENTE"
