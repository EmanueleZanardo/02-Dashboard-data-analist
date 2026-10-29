"""Test nuova scheda "Bar / caffetteria: macchina
espresso efficiente + frigo bibite efficiente +
recupero calore macchina su ACS batte macchina
espresso tradizionale + frigo tradizionale +
caldaia a gas?" (titolo completo nel frammento UI).
Contenuto pronto da scrivere in repo come test
della scheda bar / caffetteria.

Business case deterministico di un bar guidato
dalle TAZZINE AL GIORNO e dalle BIBITE AL
GIORNO, insieme ai GIORNI DI APERTURA
ALL'ANNO: le tazzine guidano l'elettricita'
della macchina espresso (kWh_e per tazzina) e
il calore recuperabile della macchina, le
bibite guidano il carico frigorifero del frigo
bibite (kWh_c per bibita); i litri di ACS al
giorno guidano il lavaggio delle tazzine.
Tazzine annue = tazzine al giorno x giorni;
bibite annue = bibite al giorno x giorni;
elettricita' espresso base e alt = tazzine
annue x kWh_e per tazzina x fattore (base
1,00, alt 0,65); carico frigo = bibite annue x
kWh_c per bibita; elettricita' frigo base e
alt = Q_frigo / COP (stesso carico, COP
diverso); ACS = litri x giorni x 4,186 x
delta_T / 3600; recupero = min(ACS,
E_espresso_alt x f_rec) (saturato all'ACS; nel
demo NON satura: il recupero grezzo 3.040,54
e' sotto l'ACS 7.674,33); ACS netta =
max(0, ACS - recupero); gas ACS baseline = ACS /
eta_caldaia (senza recupero); elettricita' PdC
ACS = ACS netta / COP_pdc_acs; C_base =
gas_acs_base / 1000 x p_gas +
(E_espresso_base + E_frigo_base) / 1000 x p_el +
O&M_base; C_alt = (E_espresso_alt +
E_frigo_alt + E_pdc_acs) / 1000 x p_el +
O&M_alt (niente gas: l'alternativa non ha
caldaia); risparmio = C_base - C_alt;
CO2_base = gas_acs_base / 1000 x f_gas +
(E_espresso_base + E_frigo_base) / 1000 x f_el;
CO2_alt = (E_espresso_alt + E_frigo_alt +
E_pdc_acs) / 1000 x f_el; CO2_evitata =
CO2_base - CO2_alt; flussi [-CAPEX, risparmio
x vita]; VAN, TIR, payback (primo anno con
cumulato >= 0); breakeven gas =
((E_espresso_alt + E_frigo_alt + E_pdc_acs)
/ 1000 x p_el + O&M_alt - (E_espresso_base +
E_frigo_base) / 1000 x p_el - O&M_base) /
(gas_acs_base / 1000) EUR/MWh, None se
denominatore gas <= 0 o numeratore < 0,
SOGLIA MINIMA quando esiste.
Verdetto: NON_CALCOLABILE se input degenere
(tazzine <= 0, bibite < 0, giorni <= 0, eta
<= 0 o > 1, COP <= 1, delta_T <= 0, f_rec fuori
[0, 1], prezzi <= 0, CAPEX <= 0, vita <= 0) o
se risparmio <= 0 (guard degenere: UI salta
KPI, grafico, tabella e CSV); altrimenti
CONVIENTE se VAN > 0, MARGINALE se VAN
negativa entro tolleranza % del CAPEX,
NON_CONVIENTE se VAN negativa oltre la
tolleranza. Differenze UI-vs-helper
documentate: tazzine = 0 e' calcolabile negli
helper (risparmio negativo, verdetto
NON_CALCOLABILE) ma bloccata dalla guard UI;
CAPEX = 0 e' CONVIENTE negli helper (VAN
positiva, TIR None, payback 0) ma bloccato
dalla guard UI; prezzi = 0 sono ammessi negli
helper ma bloccati dalla guard UI; p_gas = 0
da' risparmio negativo anche negli helper
(-160,67 EUR/anno), quindi nessuna divergenza
di verdetto in quel caso (solo la guard UI lo
intercetta prima).
Distinzione esplicita: distinto dalla tavola
calda (porzioni al giorno, forno combinato,
banchi caldi, celle di porzioni: qui nessuna
porzione, nessun forno, driver tazzine al
giorno per espresso e bibite al giorno per
frigo, recupero dal calore della macchina
espresso), dalla rosticceria (kg di prodotto
arrosto al giorno, girarrosto, banchi e celle
del prodotto arrosto: qui nessun prodotto
pesato in kg, nessun girarrosto, driver
tazzine al giorno per espresso, bibite al
giorno per frigo, recupero sull'ACS di
lavaggio delle tazzine), dalla pasticceria
(kg di dolci, abbattitore da T_in a T_out,
celle dei dolci: qui nessun dolce, nessun
abbattitore, il freddo e' quello del frigo
bibite), dal ristorante (coperti, ACS di
cucina, celle frigo di cucina: qui niente
coperti, niente ACS di cucina, il freddo
segue le bibite), dal panificio (kg di pane
per la cottura del pane: qui nessun pane),
dalla gelateria (litri di gelato,
pastorizzazione, freddo del gelato: qui
nessuna pastorizzazione, nessun gelato, il
freddo e' quello del frigo bibite), dalla
pescheria (kg di pesce, macchina del ghiaccio
in scaglie, recupero dai condensatori: qui
nessun pesce, nessun ghiaccio, il recupero
viene dal calore della macchina espresso),
dal fioraio (superficie negozio per
riscaldamento piu' cella fiori, recupero sul
riscaldamento: qui niente riscaldamento,
recupero sull'ACS di lavaggio delle tazzine),
dal parrucchiere (lavaggi di capelli, ACS,
recupero dalle acque reflue), dalla farmacia
(superficie di vendita piu' frigoriferi
farmaceutici, recupero dai frigoriferi,
nessuna macchina espresso), dall'albergo
(pernottamento, ACS docce ospiti), dalla
palestra (docce utenti, recupero dalle acque
delle docce), dall'autolavaggio (veicoli
lavati, acque di lavaggio dei veicoli) e dal
palaghiaccio (pista da pattinaggio, freddo di
pista verso spogliatoi): qui driver TAZZINE +
BIBITE + GIORNI + ACS = tazzine al giorno per
espresso e recupero, bibite al giorno per
frigo, giorni di apertura per l'anno, litri di
ACS per il lavaggio delle tazzine; niente
porzioni, niente kg di prodotto arrosto,
niente dolci, niente gelato, niente pesce,
niente lavaggi, niente coperti, niente docce,
niente veicoli, niente frigoriferi
farmaceutici, niente pista.

Demo (bar): 450 tazzine al giorno e 220 bibite
al giorno per 330 giorni di apertura all'anno
(148.500 tazzine all'anno, 72.600 bibite
all'anno), carico espresso 0,09 kWh_e per
tazzina (13.365 kWh_e/anno base, 8.687,25 alt
con fattore 0,65), carico frigo 0,12 kWh_c per
bibita (8.712 kWh_c/anno), COP frigo base 2,0
e alt 3,2, ACS di lavaggio delle tazzine 400
litri al giorno con delta_T 50 K, f_rec 0,35,
caldaia 0,85, COP PdC ACS 3,0, gas 90, el 260
EUR/MWh, O&M base 1.200, alt 2.600, CAPEX
6.000, WACC 5 %, vita 12, f_gas 0,20, f_el
0,35, tolleranza 10 % del CAPEX.
Valori calcolati eseguendo mh806_demo_calcoli():
tazzine annue 148.500, bibite annue 72.600,
E_espresso_base 13.365, E_espresso_alt
8.687,25, Q_frigo 8.712, E_frigo_base 4.356,
E_frigo_alt 2.722,5, Q_acs
7.674,333333333333, Q_rec 3.040,5375 (NON
saturato: il recupero grezzo 8.687,25 x 0,35 =
3.040,54 e' sotto l'ACS), Q_acs_net
4.633,795833333334, gas_acs_base
9.028,627450980392, E_pdc_acs
1.544,5986111111113, C_base
6.620,036470588235, C_alt 5.968,130638888889,
risparmio 651,905831699346, CO2_base
8,008075490196077, CO2_alt
4,5340220138888885, CO2_evitata
3,474053476307189, VAN -221,994570380251,
TIR 4,3377924080209 %, payback 10,
breakeven gas 17,79568818862296 EUR/MWh
(soglia minima: sopra vince, sotto perde),
verdetto MARGINALE (VAN negativa entro la
tolleranza del 10 % = 600 EUR).
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w807_helpers import (
    demo_calcoli,
    mh806_breakeven_gas,
    mh806_bibite_anno,
    mh806_c_alt,
    mh806_c_base,
    mh806_calcola,
    mh806_co2_alt,
    mh806_co2_base,
    mh806_co2_evitata,
    mh806_cop,
    mh806_csv,
    mh806_demo,
    mh806_demo_calcoli,
    mh806_e_espresso,
    mh806_e_frigo,
    mh806_e_pdc_acs,
    mh806_eta,
    mh806_flussi,
    mh806_frazione,
    mh806_gas_acs,
    mh806_int_pos,
    mh806_num,
    mh806_nneg,
    mh806_payback,
    mh806_pct_tolleranza,
    mh806_pos,
    mh806_pct_wacc,
    mh806_q_acs,
    mh806_q_acs_net,
    mh806_q_frigo,
    mh806_q_rec,
    mh806_risparmio,
    mh806_tazzine_anno,
    mh806_tir,
    mh806_valida,
    mh806_van,
    mh806_verdetto,
)

_DEMO = {
    "tazzine_anno": 148500.0,
    "bibite_anno": 72600.0,
    "e_espresso_base_kwh_anno": 13365.0,
    "e_espresso_alt_kwh_anno": 8687.25,
    "q_frigo_kwh_anno": 8712.0,
    "e_frigo_base_kwh_anno": 4356.0,
    "e_frigo_alt_kwh_anno": 2722.5,
    "q_acs_kwh_anno": 7674.333333333333,
    "q_rec_kwh_anno": 3040.5375,
    "q_acs_net_kwh_anno": 4633.795833333334,
    "gas_acs_base_kwh_anno": 9028.627450980392,
    "e_pdc_acs_kwh_anno": 1544.5986111111113,
    "c_base_eur_anno": 6620.036470588235,
    "c_alt_eur_anno": 5968.130638888889,
    "risparmio_eur_anno": 651.905831699346,
    "co2_base_t_anno": 8.008075490196077,
    "co2_alt_t_anno": 4.5340220138888885,
    "co2_evitata_t_anno": 3.474053476307189,
    "van": -221.994570380251,
    "tir": 4.3377924080209,
}


def _demo_kwargs():
    return dict(mh806_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh806_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh806_num(3, "x") == 3.0
    assert mh806_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh806_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh806_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh806_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh806_pos(0, "x")
    with pytest.raises(ValueError):
        mh806_pos(-1, "x")
    assert mh806_pos(0.5, "x") == 0.5


def test_cop_maggiore_di_uno():
    assert mh806_cop(3.0, "x") == 3.0
    assert mh806_cop(1.01, "x") == 1.01
    with pytest.raises(ValueError):
        mh806_cop(1.0, "x")
    with pytest.raises(ValueError):
        mh806_cop(0.5, "x")
    with pytest.raises(ValueError):
        mh806_cop(0, "x")


def test_frazione_limiti():
    assert mh806_frazione(0, "x") == 0.0
    assert mh806_frazione(1, "x") == 1.0
    assert mh806_frazione(0.35, "x") == 0.35
    with pytest.raises(ValueError):
        mh806_frazione(-0.01, "x")
    with pytest.raises(ValueError):
        mh806_frazione(1.01, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh806_int_pos(5.0, "x") == 5
    assert mh806_int_pos(330.0, "x") == 330
    with pytest.raises(ValueError):
        mh806_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh806_int_pos(0, "x")


def test_eta_limiti():
    assert mh806_eta(1.0, "x") == 1.0
    assert mh806_eta(0.85, "x") == 0.85
    with pytest.raises(ValueError):
        mh806_eta(0, "x")
    with pytest.raises(ValueError):
        mh806_eta(1.01, "x")


def test_pct_wacc_limiti():
    assert mh806_pct_wacc(0, "x") == 0.0
    assert mh806_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh806_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh806_pct_tolleranza(0, "x") == 0.0
    assert mh806_pct_tolleranza(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh806_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh806_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_tazzine_bibite_anno_e_espresso():
    assert mh806_tazzine_anno(450, 330) == 148500.0
    assert mh806_tazzine_anno(0, 330) == 0.0
    assert mh806_tazzine_anno(225, 330) == 74250.0
    assert mh806_bibite_anno(220, 330) == 72600.0
    assert mh806_bibite_anno(0, 330) == 0.0
    assert mh806_e_espresso(148500, 0.09, 1.0) == 13365.0
    assert mh806_e_espresso(148500, 0.09, 0.65) == 8687.25
    assert mh806_e_espresso(0, 0.09, 1.0) == 0.0
    assert mh806_e_espresso(148500, 0, 0.65) == 0.0
    with pytest.raises(ValueError):
        mh806_tazzine_anno(-1, 330)
    with pytest.raises(ValueError):
        mh806_tazzine_anno(450, 0)
    with pytest.raises(ValueError):
        mh806_tazzine_anno(450, 2.5)
    with pytest.raises(ValueError):
        mh806_bibite_anno(-1, 330)
    with pytest.raises(ValueError):
        mh806_e_espresso(148500, 0.09, 0)
    with pytest.raises(ValueError):
        mh806_e_espresso(148500, 0.09, 1.01)
    with pytest.raises(ValueError):
        mh806_e_espresso(148500, -0.1, 0.65)
    with pytest.raises(ValueError):
        mh806_e_espresso(-1, 0.09, 0.65)


def test_q_frigo_e_frigo():
    assert mh806_q_frigo(72600, 0.12) == 8712.0
    assert mh806_q_frigo(0, 0.12) == 0.0
    assert mh806_q_frigo(72600, 0) == 0.0
    assert mh806_e_frigo(8712.0, 2.0) == pytest.approx(4356.0)
    assert mh806_e_frigo(8712.0, 3.2) == pytest.approx(2722.5)
    assert mh806_e_frigo(0, 2.0) == 0.0
    with pytest.raises(ValueError):
        mh806_q_frigo(72600, -0.1)
    with pytest.raises(ValueError):
        mh806_e_frigo(8712.0, 1.0)
    with pytest.raises(ValueError):
        mh806_e_frigo(-1, 2.0)


def test_q_acs_formula():
    assert mh806_q_acs(400, 330, 50) == pytest.approx(7674.333333333333)
    assert mh806_q_acs(0, 330, 50) == 0.0
    assert mh806_q_acs(800, 330, 50) == pytest.approx(15348.666666666666)
    assert mh806_q_acs(400, 330, 25) == pytest.approx(3837.1666666666665)
    with pytest.raises(ValueError):
        mh806_q_acs(-1, 330, 50)
    with pytest.raises(ValueError):
        mh806_q_acs(400, 0, 50)
    with pytest.raises(ValueError):
        mh806_q_acs(400, 330, 0)
    with pytest.raises(ValueError):
        mh806_q_acs(400, 2.5, 50)


def test_q_rec_saturazione_e_acs_netta():
    # Demo: recupero grezzo 3.040,54 sotto l'ACS -> NON satura.
    assert mh806_q_rec(8687.25, 0.35, 7674.333333333333) == pytest.approx(3040.5375)
    assert mh806_q_rec(8687.25, 0, 7674.333333333333) == 0.0
    assert mh806_q_rec(8687.25, 0.20, 7674.333333333333) == pytest.approx(1737.45)
    # Con f_rec 1,0 il recupero satura all'ACS.
    assert mh806_q_rec(8687.25, 1.0, 7674.333333333333) == 7674.333333333333
    with pytest.raises(ValueError):
        mh806_q_rec(8687.25, 1.01, 7674.333333333333)
    with pytest.raises(ValueError):
        mh806_q_rec(8687.25, -0.1, 7674.333333333333)
    assert mh806_q_acs_net(7674.333333333333, 3040.5375) == pytest.approx(4633.795833333334)
    assert mh806_q_acs_net(7674.333333333333, 0.0) == pytest.approx(7674.333333333333)
    assert mh806_q_acs_net(7674.333333333333, 7674.333333333333) == 0.0
    with pytest.raises(ValueError):
        mh806_q_acs_net(-1, 3040.5375)
    with pytest.raises(ValueError):
        mh806_q_acs_net(7674.333333333333, -1)


def test_gas_acs_e_pdc_acs():
    assert mh806_gas_acs(7674.333333333333, 0.85) == pytest.approx(9028.627450980392)
    assert mh806_gas_acs(0, 0.85) == 0.0
    assert mh806_gas_acs(7674.333333333333, 1.0) == pytest.approx(7674.333333333333)
    assert mh806_e_pdc_acs(4633.795833333334, 3.0) == pytest.approx(1544.5986111111113)
    assert mh806_e_pdc_acs(0.0, 3.0) == 0.0
    with pytest.raises(ValueError):
        mh806_gas_acs(7674.333333333333, 0)
    with pytest.raises(ValueError):
        mh806_gas_acs(7674.333333333333, 1.01)
    with pytest.raises(ValueError):
        mh806_e_pdc_acs(4633.795833333334, 1.0)


def test_c_base_c_alt_scomposizione():
    assert mh806_c_base(9028.627450980392, 90, 13365.0,
                        4356.0, 260,
                        1200) == pytest.approx(6620.036470588235)
    assert mh806_c_base(9028.627450980392, 0, 13365.0,
                        4356.0, 260,
                        1200) == pytest.approx(5807.46)
    assert mh806_c_alt(8687.25, 2722.5, 1544.5986111111113, 260,
                       2600) == pytest.approx(5968.130638888889)
    assert mh806_c_alt(8687.25, 2722.5, 0.0, 260,
                       2600) == pytest.approx(5566.535)
    with pytest.raises(ValueError):
        mh806_c_base(9028.63, 90, 13365.0, 4356.0, 260, -1)
    with pytest.raises(ValueError):
        mh806_c_alt(8687.25, 2722.5, 1544.60, 260, -1)


def test_risparmio_segno():
    assert mh806_risparmio(6620.036470588235, 5968.130638888889) == pytest.approx(651.905831699346)
    assert mh806_risparmio(5968.13, 5968.13) == 0.0


def test_co2_base_alt_evitata():
    assert mh806_co2_base(9028.627450980392, 0.20, 13365.0,
                          4356.0,
                          0.35) == pytest.approx(8.008075490196077)
    assert mh806_co2_alt(8687.25, 2722.5, 1544.5986111111113,
                         0.35) == pytest.approx(4.5340220138888885)
    assert mh806_co2_evitata(9028.627450980392, 0.20, 13365.0,
                             4356.0, 8687.25,
                             2722.5, 1544.5986111111113,
                             0.35) == pytest.approx(3.474053476307189)
    assert mh806_co2_base(0, 0.20, 0, 0, 0.35) == pytest.approx(0.0)
    assert mh806_co2_alt(0, 0, 0, 0.35) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh806_co2_base(9028.63, -0.10, 13365.0, 4356.0, 0.35)
    with pytest.raises(ValueError):
        mh806_co2_alt(8687.25, 2722.5, 1544.60, -0.10)


def test_breakeven_demo_e_varianti():
    # Demo: breakeven 17,80 EUR/MWh (soglia minima, non None).
    assert mh806_demo_calcoli()["breakeven_gas_eur_mwh"] == pytest.approx(17.79568818862296)
    assert mh806_breakeven_gas(8687.25, 2722.5, 1544.5986111111113,
                               260, 2600,
                               13365.0, 4356.0, 1200,
                               9028.627450980392) == pytest.approx(17.79568818862296)
    # Variante senza recupero: be 46,98.
    bc = _variante(f_rec=0)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(46.98210123210122)
    # Variante 900 tazzine: numeratore negativo -> None.
    assert _variante(tazzine_giorno=900)["breakeven_gas_eur_mwh"] is None
    # Variante senza ACS: denominatore gas nullo -> None.
    assert _variante(litri_acs_giorno=0)["breakeven_gas_eur_mwh"] is None
    # Denominatore gas nullo diretto -> None.
    assert mh806_breakeven_gas(8687.25, 2722.5, 1544.5986111111113,
                               260, 2600,
                               13365.0, 4356.0, 1200,
                               0) is None
    with pytest.raises(ValueError):
        mh806_breakeven_gas(8687.25, 2722.5, 1544.60, 260, 2600,
                            13365.0, 4356.0, 1200,
                            -1)


def test_breakeven_verifica_pareggio():
    be = _variante(f_rec=0)["breakeven_gas_eur_mwh"]
    assert be == pytest.approx(46.98210123210122)
    bc = _variante(f_rec=0, p_gas=be)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    demo = mh806_demo_calcoli()
    assert demo["breakeven_gas_eur_mwh"] == pytest.approx(17.79568818862296)
    assert demo["gas_acs_base_kwh_anno"] > 0.0


def test_breakeven_soglia_minima():
    bc_alto = _variante(f_rec=0, p_gas=47.98210123210122)
    bc_basso = _variante(f_rec=0, p_gas=45.0)
    assert bc_alto["c_alt_eur_anno"] < bc_alto["c_base_eur_anno"]
    assert bc_basso["c_alt_eur_anno"] > bc_basso["c_base_eur_anno"]
    assert bc_alto["verdetto"] == "NON_CONVIENTE"
    assert bc_basso["verdetto"] == "NON_CALCOLABILE"


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh806_flussi(6000, 651.905831699346, 12)
    assert len(fl) == 13
    assert fl[0] == -6000
    assert all(f == 651.905831699346 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh806_demo_calcoli()
    assert bc["van"] == pytest.approx(-221.994570380251)
    assert mh806_van([-6000] + [651.905831699346] * 12,
                     0) == pytest.approx(1822.8699803921518)
    assert mh806_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh806_demo_calcoli()
    assert bc["tir"] == pytest.approx(4.3377924080209)
    assert mh806_tir([-6000] + [651.905831699346] * 12) == \
        pytest.approx(0.043377924080209)
    tir = mh806_tir([-6000] + [651.905831699346] * 12)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-6000] + [651.905831699346] * 12))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh806_payback([-6000] + [651.905831699346] * 12) == 10
    assert mh806_payback([-6000] + [-1000.0] * 12) is None
    assert mh806_payback([0] + [651.905831699346] * 12) == 0
    assert mh806_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh806_verdetto(651.905831699346, -221.994570380251, 6000,
                          10.0) == "MARGINALE"
    assert mh806_verdetto(651.905831699346, 0.0, 6000, 10.0) == "MARGINALE"
    assert mh806_verdetto(651.905831699346, -600.0, 6000, 10.0) == "MARGINALE"
    assert mh806_verdetto(651.905831699346, -600.01, 6000, 10.0) == "NON_CONVIENTE"
    assert mh806_verdetto(651.905831699346, 778.01, 6000, 10.0) == "CONVIENTE"
    assert mh806_verdetto(0.0, 778.01, 6000,
                          10.0) == "NON_CALCOLABILE"
    assert mh806_verdetto(-827.82, -13337.20, 6000,
                          10.0) == "NON_CALCOLABILE"
    assert mh806_verdetto(None, 778.01, 6000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh806_verdetto(float("nan"), 778.01, 6000, 10.0)
    with pytest.raises(ValueError):
        mh806_verdetto(651.905831699346, 778.01, -1, 10.0)
    with pytest.raises(ValueError):
        mh806_verdetto(651.905831699346, 778.01, 6000, 100.1)


def test_valida_demo_ok():
    v = mh806_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("tazzine_giorno", "450"),
                       ("tazzine_giorno", float("nan")),
                       ("tazzine_giorno", float("inf")),
                       ("tazzine_giorno", True),
                       ("p_gas", None),
                       ("q_frigo_per_bibita", "0.12")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh806_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("tazzine_giorno", -10),
                          ("bibite_giorno", -10),
                          ("giorni_anno", 0),
                          ("giorni_anno", 2.5),
                          ("q_espresso_per_tazzina", -0.1),
                          ("fattore_espresso_alt", 0),
                          ("fattore_espresso_alt", 1.01),
                          ("q_frigo_per_bibita", -0.1),
                          ("cop_frigo_base", 1.0),
                          ("cop_frigo_base", 0.5),
                          ("cop_frigo_alt", 1.0),
                          ("cop_frigo_alt", 0.5),
                          ("litri_acs_giorno", -1),
                          ("delta_t_acs", 0),
                          ("delta_t_acs", -5),
                          ("f_rec", -0.1),
                          ("f_rec", 1.01),
                          ("eta_caldaia_base", 0),
                          ("eta_caldaia_base", 1.01),
                          ("cop_pdc_acs", 1.0),
                          ("cop_pdc_acs", 0.5),
                          ("p_gas", -1),
                          ("p_el", -1),
                          ("om_base", -100),
                          ("om_alt", -100),
                          ("capex", -1),
                          ("wacc_pct", -0.1), ("wacc_pct", 50.1),
                          ("vita_anni", 0), ("vita_anni", 2.5),
                          ("f_gas", -0.10),
                          ("f_el", -0.10),
                          ("tolleranza_pct", -1),
                          ("tolleranza_pct", 100.1)):
        d = _demo_kwargs()
        d[campo] = valore
        assert mh806_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"tazzine_giorno": 0,
              "bibite_giorno": 0,
              "q_espresso_per_tazzina": 0,
              "q_frigo_per_bibita": 0,
              "litri_acs_giorno": 0,
              "f_rec": 0,
              "p_gas": 0,
              "p_el": 0,
              "om_base": 0, "om_alt": 0,
              "capex": 0, "wacc_pct": 0,
              "f_gas": 0, "f_el": 0,
              "tolleranza_pct": 0})
    assert mh806_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["f_rec"] = 1.0
    d["tazzine_giorno"] = 450
    assert mh806_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh806_demo()
    assert d["tazzine_giorno"] == 450
    assert d["giorni_anno"] == 330
    assert d["q_espresso_per_tazzina"] == 0.09
    assert d["fattore_espresso_alt"] == 0.65
    assert d["bibite_giorno"] == 220
    assert d["q_frigo_per_bibita"] == 0.12
    assert d["cop_frigo_base"] == 2.0
    assert d["cop_frigo_alt"] == 3.2
    assert d["litri_acs_giorno"] == 400
    assert d["delta_t_acs"] == 50
    assert d["f_rec"] == 0.35
    assert d["eta_caldaia_base"] == 0.85
    assert d["cop_pdc_acs"] == 3.0
    assert d["p_gas"] == 90
    assert d["p_el"] == 260
    assert d["om_base"] == 1200
    assert d["om_alt"] == 2600
    assert d["capex"] == 6000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 12
    assert d["f_gas"] == 0.20
    assert d["f_el"] == 0.35
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    bc = mh806_demo_calcoli()
    for chiave, atteso in _DEMO.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert got == pytest.approx(atteso, rel=1e-9), chiave
    assert bc["payback"] == 10
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(17.79568818862296)
    assert bc["verdetto"] == "MARGINALE"
    assert bc["valid"] is True
    assert demo_calcoli()["van"] == bc["van"]


def test_demo_calcoli_fisica_economia():
    bc = mh806_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(6620.036470588235)
    assert bc["c_alt_eur_anno"] == pytest.approx(5968.130638888889)
    assert bc["risparmio_eur_anno"] == pytest.approx(651.905831699346)
    assert bc["co2_base_t_anno"] == pytest.approx(8.008075490196077)
    assert bc["co2_alt_t_anno"] == pytest.approx(4.5340220138888885)
    assert bc["co2_evitata_t_anno"] == pytest.approx(3.474053476307189)
    assert bc["tazzine_anno"] == pytest.approx(148500.0)
    assert bc["bibite_anno"] == pytest.approx(72600.0)
    assert bc["q_frigo_kwh_anno"] == pytest.approx(8712.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(3040.5375)
    assert bc["q_acs_net_kwh_anno"] == pytest.approx(4633.795833333334)


def test_demo_flussi_e_cumulato():
    bc = mh806_demo_calcoli()
    assert bc["flussi"][0] == -6000
    assert len(bc["flussi"]) == 13
    assert all(f == pytest.approx(651.905831699346) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -6000
    assert righe.iloc[9]["Cumulato (EUR)"] == pytest.approx(-132.84751470588617)
    assert righe.iloc[10]["Cumulato (EUR)"] == pytest.approx(519.0583169934598)
    assert righe.iloc[12]["Cumulato (EUR)"] == pytest.approx(1822.8699803921518)


def test_demo_tabella_righe():
    bc = mh806_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Tazzine all'anno"] == pytest.approx(148500.0)
    assert mappa["Bibite all'anno"] == pytest.approx(72600.0)
    assert mappa["Elettricita' espresso base (kWh_e/anno)"] == pytest.approx(13365.0)
    assert mappa["Elettricita' espresso alt (kWh_e/anno)"] == pytest.approx(8687.25)
    assert mappa["Carico frigo (kWh_c/anno)"] == pytest.approx(8712.0)
    assert mappa["Elettricita' frigo base (kWh_e/anno)"] == pytest.approx(4356.0)
    assert mappa["Elettricita' frigo alt (kWh_e/anno)"] == pytest.approx(2722.5)
    assert mappa["ACS di lavaggio tazzine (kWh_th/anno)"] == pytest.approx(7674.333333333333)
    assert mappa["Calore macchina recuperato (kWh_th/anno)"] == pytest.approx(3040.5375)
    assert mappa["ACS netta (kWh_th/anno)"] == pytest.approx(4633.795833333334)
    assert mappa["Gas ACS baseline (kWh/anno)"] == pytest.approx(9028.627450980392)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(6620.036470588235)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(5968.130638888889)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(651.905831699346)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(3.474053476307189)
    assert mappa["Payback (anni)"] == 10
    assert mappa["Verdetto"] == "MARGINALE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] == pytest.approx(17.79568818862296)


def test_demo_coerenza_interna():
    bc = mh806_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["tazzine_anno"] == pytest.approx(
        bc["tazzine_giorno"] * bc["giorni_anno"])
    assert bc["bibite_anno"] == pytest.approx(
        bc["bibite_giorno"] * bc["giorni_anno"])
    assert bc["e_espresso_base_kwh_anno"] == pytest.approx(
        bc["tazzine_anno"] * bc["q_espresso_per_tazzina"] * 1.0)
    assert bc["e_espresso_alt_kwh_anno"] == pytest.approx(
        bc["tazzine_anno"] * bc["q_espresso_per_tazzina"]
        * bc["fattore_espresso_alt"])
    assert bc["q_frigo_kwh_anno"] == pytest.approx(
        bc["bibite_anno"] * bc["q_frigo_per_bibita"])
    assert bc["e_frigo_base_kwh_anno"] == pytest.approx(
        bc["q_frigo_kwh_anno"] / bc["cop_frigo_base"])
    assert bc["e_frigo_alt_kwh_anno"] == pytest.approx(
        bc["q_frigo_kwh_anno"] / bc["cop_frigo_alt"])
    assert bc["q_acs_kwh_anno"] == pytest.approx(
        bc["litri_acs_giorno"] * bc["giorni_anno"]
        * 4.186 * bc["delta_t_acs"] / 3600.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(
        min(bc["q_acs_kwh_anno"],
            bc["e_espresso_alt_kwh_anno"] * bc["f_rec"]))
    assert bc["q_acs_net_kwh_anno"] == pytest.approx(
        max(0.0, bc["q_acs_kwh_anno"] - bc["q_rec_kwh_anno"]))
    assert bc["gas_acs_base_kwh_anno"] == pytest.approx(
        bc["q_acs_kwh_anno"] / bc["eta_caldaia_base"])
    assert bc["e_pdc_acs_kwh_anno"] == pytest.approx(
        bc["q_acs_net_kwh_anno"] / bc["cop_pdc_acs"])
    assert bc["co2_evitata_t_anno"] == pytest.approx(
        bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])
    assert bc["c_base_eur_anno"] == pytest.approx(
        bc["gas_acs_base_kwh_anno"] / 1000.0 * bc["p_gas"]
        + (bc["e_espresso_base_kwh_anno"]
           + bc["e_frigo_base_kwh_anno"]) / 1000.0 * bc["p_el"]
        + bc["om_base"])
    assert bc["c_alt_eur_anno"] == pytest.approx(
        (bc["e_espresso_alt_kwh_anno"]
         + bc["e_frigo_alt_kwh_anno"]
         + bc["e_pdc_acs_kwh_anno"])
        / 1000.0 * bc["p_el"]
        + bc["om_alt"])


def test_demo_contro_riconteggio_indipendente():
    tz, bb, gg = 450, 220, 330
    qe, fea = 0.09, 0.65
    qf, cfb, cfa = 0.12, 2.0, 3.2
    lit, dt, frec = 400, 50, 0.35
    eta, copp = 0.85, 3.0
    pg, pel = 90, 260
    omb, oma, cx = 1200, 2600, 6000
    fg, fel, wacc, vita = 0.20, 0.35, 5.0, 12
    tza = tz * gg
    bba = bb * gg
    eeb = tza * qe * 1.0
    eea = tza * qe * fea
    qfk = bba * qf
    efbk = qfk / cfb
    efak = qfk / cfa
    qacs = lit * gg * 4.186 * dt / 3600.0
    qrec = min(qacs, eea * frec)
    qnet = max(0.0, qacs - qrec)
    gasa = qacs / eta
    epdc = qnet / copp
    cb = gasa / 1000.0 * pg + (eeb + efbk) / 1000.0 * pel + omb
    ca = (eea + efak + epdc) / 1000.0 * pel + oma
    risp = cb - ca
    co2b = gasa / 1000.0 * fg + (eeb + efbk) / 1000.0 * fel
    co2a = (eea + efak + epdc) / 1000.0 * fel
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    bc = mh806_demo_calcoli()
    assert bc["tazzine_anno"] == pytest.approx(tza)
    assert bc["bibite_anno"] == pytest.approx(bba)
    assert bc["e_espresso_base_kwh_anno"] == pytest.approx(eeb)
    assert bc["e_espresso_alt_kwh_anno"] == pytest.approx(eea)
    assert bc["q_frigo_kwh_anno"] == pytest.approx(qfk)
    assert bc["e_frigo_base_kwh_anno"] == pytest.approx(efbk)
    assert bc["e_frigo_alt_kwh_anno"] == pytest.approx(efak)
    assert bc["q_acs_kwh_anno"] == pytest.approx(qacs)
    assert bc["q_rec_kwh_anno"] == pytest.approx(qrec)
    assert bc["q_acs_net_kwh_anno"] == pytest.approx(qnet)
    assert bc["gas_acs_base_kwh_anno"] == pytest.approx(gasa)
    assert bc["e_pdc_acs_kwh_anno"] == pytest.approx(epdc)
    assert bc["c_base_eur_anno"] == pytest.approx(cb)
    assert bc["c_alt_eur_anno"] == pytest.approx(ca)
    assert bc["risparmio_eur_anno"] == pytest.approx(risp)
    assert bc["co2_base_t_anno"] == pytest.approx(co2b)
    assert bc["co2_alt_t_anno"] == pytest.approx(co2a)
    assert bc["co2_evitata_t_anno"] == pytest.approx(co2)
    assert bc["van"] == pytest.approx(van)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(17.79568818862296)


# ---------------------------------------------------------------- varianti
def test_variante_gas_zero_helper_calcola_ma_ui_guard():
    # Negli helper p_gas = 0 e' ammesso (non negativo)
    # ma qui il risparmio va in negativo (-160,67
    # EUR/anno): verdetto NON_CALCOLABILE anche
    # negli helper, quindi nessuna divergenza di
    # verdetto con la guard UI (prezzi <= 0), che
    # lo intercetta solo prima.
    bc = _variante(p_gas=0)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(-160.6706388888888)
    assert bc["van"] == pytest.approx(-7424.064303061219)
    assert bc["payback"] is None
    assert bc["tir"] is None
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(17.79568818862296)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_gas_alto_conviente():
    bc = _variante(p_gas=150)
    assert bc["risparmio_eur_anno"] == pytest.approx(1193.6234787581698)
    assert bc["van"] == pytest.approx(4579.385251407067)
    assert bc["tir"] == pytest.approx(16.811244462539715)
    assert bc["payback"] == 6
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_senza_recupero_non_conviente():
    bc = _variante(f_rec=0)
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["q_acs_net_kwh_anno"] == pytest.approx(7674.333333333333)
    assert bc["e_pdc_acs_kwh_anno"] == pytest.approx(2558.111111111111)
    assert bc["risparmio_eur_anno"] == pytest.approx(388.392581699346)
    assert bc["van"] == pytest.approx(-2557.5788146686946)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(46.98210123210122)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_recupero_parziale_senza_saturazione():
    bc = _variante(f_rec=0.20)
    assert bc["q_rec_kwh_anno"] == pytest.approx(1737.45)
    assert bc["q_acs_net_kwh_anno"] == pytest.approx(5936.883333333333)
    assert bc["e_pdc_acs_kwh_anno"] == pytest.approx(1978.961111111111)
    assert bc["risparmio_eur_anno"] == pytest.approx(538.9715816993457)
    assert bc["van"] == pytest.approx(-1222.9592465038718)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(30.304150921542245)
    assert bc["payback"] == 12
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_recupero_pieno_satura():
    bc = _variante(f_rec=1.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(7674.333333333333)
    assert bc["q_acs_net_kwh_anno"] == 0.0
    assert bc["e_pdc_acs_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(1053.501470588235)
    assert bc["van"] == pytest.approx(3337.448633192398)
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["payback"] == 6
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_tazzine_piccole_e_grandi():
    bc = _variante(tazzine_giorno=225)
    assert bc["tazzine_anno"] == pytest.approx(74250.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-87.95829330065317)
    assert bc["van"] == pytest.approx(-6779.596487036259)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(99.74215557992733)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CALCOLABILE"
    bc2 = _variante(tazzine_giorno=900)
    assert bc2["risparmio_eur_anno"] == pytest.approx(2131.634081699345)
    assert bc2["van"] == pytest.approx(12893.209262931772)
    assert bc2["breakeven_gas_eur_mwh"] is None
    assert bc2["payback"] == 3
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_capex_conviente():
    bc = _variante(capex=5000)
    assert bc["risparmio_eur_anno"] == pytest.approx(651.905831699346)
    assert bc["van"] == pytest.approx(778.0054296197491)
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(capex=4000)
    assert bc2["van"] == pytest.approx(1778.005429619749)
    assert bc2["payback"] == 7
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    # Negli helper CAPEX = 0 e' CONVIENTE (VAN
    # positiva, TIR None, payback 0); in UI e'
    # guard degenere (NON_CALCOLABILE): divergenza
    # documentata, vedi test_ui_guard_degenere_stretta.
    bc = _variante(capex=0)
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(5778.005429619749, rel=1e-6)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(1822.8699803921518)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(-966.1559688278855)
    assert bc2["payback"] == 10
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_el_alto_e_om_alt_alto():
    bc = _variante(p_el=400)
    assert bc["risparmio_eur_anno"] == pytest.approx(1319.237026143791)
    assert bc["van"] == pytest.approx(5692.7297308328125)
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["payback"] == 5
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(om_alt=3600)
    assert bc2["risparmio_eur_anno"] == pytest.approx(-348.094168300654)
    assert bc2["breakeven_gas_eur_mwh"] == pytest.approx(128.5544945996033)
    assert bc2["verdetto"] == "NON_CALCOLABILE"


def test_variante_senza_bibite_e_senza_acs():
    bc = _variante(bibite_giorno=0)
    assert bc["bibite_anno"] == 0.0
    assert bc["q_frigo_kwh_anno"] == 0.0
    assert bc["e_frigo_base_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(227.19583169934594)
    assert bc["van"] == pytest.approx(-3986.3061728964244)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(64.83606085943048)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"
    bc2 = _variante(litri_acs_giorno=0)
    assert bc2["q_acs_kwh_anno"] == 0.0
    assert bc2["q_rec_kwh_anno"] == 0.0
    assert bc2["gas_acs_base_kwh_anno"] == 0.0
    assert bc2["breakeven_gas_eur_mwh"] is None
    assert bc2["risparmio_eur_anno"] == pytest.approx(240.925)
    assert bc2["van"] == pytest.approx(-3864.6210994885696)
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_senza_tazzine_non_calcolabile():
    # Negli helper tazzine = 0 resta calcolabile
    # (risparmio negativo, verdetto
    # NON_CALCOLABILE); in UI e' guard degenere
    # (tazzine <= 0): divergenza documentata.
    bc = _variante(tazzine_giorno=0)
    assert bc["tazzine_anno"] == 0.0
    assert bc["e_espresso_base_kwh_anno"] == 0.0
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(181.6886229712317)
    assert bc["risparmio_eur_anno"] == pytest.approx(-827.8224183006537)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_espresso_alt_uguale_base():
    bc = _variante(fattore_espresso_alt=1.0)
    assert bc["e_espresso_alt_kwh_anno"] == pytest.approx(13365.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-422.4174183006535)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(136.78644905818814)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_monotonia_prezzo_gas_crescente():
    base = mh806_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas=91)["risparmio_eur_anno"]
    basso = _variante(p_gas=89)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(9.028627450980392, abs=1e-2)
    assert base - basso == pytest.approx(9.028627450980392, abs=1e-2)


def test_monotonia_tazzine_crescente():
    assert _variante(tazzine_giorno=225)["risparmio_eur_anno"] < \
        mh806_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(tazzine_giorno=900)["risparmio_eur_anno"] > \
        mh806_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(tazzine_giorno=900)["tazzine_anno"] == \
        pytest.approx(297000.0)


def test_demo_deterministica_due_chiamate():
    a = mh806_demo_calcoli()
    b = mh806_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh806_demo().keys()) == {
        "tazzine_giorno", "giorni_anno",
        "q_espresso_per_tazzina", "fattore_espresso_alt",
        "bibite_giorno", "q_frigo_per_bibita",
        "cop_frigo_base", "cop_frigo_alt",
        "litri_acs_giorno", "delta_t_acs",
        "f_rec", "eta_caldaia_base", "cop_pdc_acs",
        "p_gas", "p_el",
        "om_base", "om_alt",
        "capex", "wacc_pct", "vita_anni",
        "f_gas", "f_el",
        "tolleranza_pct"}


# ---------------------------------------------------------------- degenere
def test_degenere_cop_uguale_uno_sollevela():
    with pytest.raises(ValueError):
        _variante(cop_frigo_base=1.0)
    with pytest.raises(ValueError):
        _variante(cop_frigo_alt=1.0)
    with pytest.raises(ValueError):
        _variante(cop_pdc_acs=1.0)


def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"tazzine_giorno": -10},
               {"bibite_giorno": -10},
               {"giorni_anno": 0},
               {"giorni_anno": 2.5},
               {"q_espresso_per_tazzina": -0.1},
               {"fattore_espresso_alt": 0}, {"fattore_espresso_alt": 1.01},
               {"q_frigo_per_bibita": -0.1},
               {"cop_frigo_base": 1.0}, {"cop_frigo_base": 0.5},
               {"cop_frigo_alt": 1.0}, {"cop_frigo_alt": 0.5},
               {"litri_acs_giorno": -1},
               {"delta_t_acs": 0}, {"delta_t_acs": -5},
               {"f_rec": -0.1},
               {"f_rec": 1.01},
               {"eta_caldaia_base": 0}, {"eta_caldaia_base": 1.01},
               {"cop_pdc_acs": 1.0}, {"cop_pdc_acs": 0.5},
               {"p_gas": -1},
               {"p_el": -1},
               {"om_base": -100},
               {"om_alt": -100},
               {"capex": -1},
               {"wacc_pct": -1}, {"wacc_pct": 60},
               {"vita_anni": 0}, {"vita_anni": 2.5},
               {"f_gas": -0.10},
               {"f_el": -0.10},
               {"tolleranza_pct": -1},
               {"tolleranza_pct": 100.1}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh806_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"tazzine_giorno": "450"},
               {"tazzine_giorno": float("nan")},
               {"p_gas": float("inf")},
               {"capex": True},
               {"q_frigo_per_bibita": "0.12"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh806_valida(**d)["valido"] is False


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    for kw in ({"tazzine_giorno": 0},
               {"p_gas": 0},
               {"om_alt": 3600}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] <= 0.0
        assert bc["verdetto"] == "NON_CALCOLABILE"
        assert bc["flussi"]


def test_pareggio_esatto_tolleranza_float():
    # A pareggio esatto (prezzo gas = breakeven
    # demo) il risparmio e' zero (circa 0.0,
    # quindi guard NON_CALCOLABILE): in nessun
    # caso CONVIENTE.
    be = mh806_demo_calcoli()["breakeven_gas_eur_mwh"]
    bc = _variante(p_gas=be)
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["verdetto"] != "CONVIENTE"
    bc2 = _variante(p_gas=be + 1)
    assert bc2["risparmio_eur_anno"] == pytest.approx(9.028627450980392, abs=1e-2)
    assert bc2["verdetto"] == "NON_CONVIENTE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh806_demo_calcoli()
    testo = mh806_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;MARGINALE" in testo
    assert "breakeven_gas_eur_mwh" in testo
    assert "co2_evitata_t_anno" in testo
    assert "q_frigo_kwh_anno" in testo
    assert "tazzine_giorno" in testo
    assert "bibite_giorno" in testo
    assert "e_frigo_alt_kwh_anno" in testo
    assert "e_espresso_alt_kwh_anno" in testo
    assert "q_rec_kwh_anno" in testo
    assert "q_acs_net_kwh_anno" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh806_demo_calcoli()
    testo = mh806_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"tazzine_anno;{bc['tazzine_anno']}" in testo
    assert f"gas_acs_base_kwh_anno;{bc['gas_acs_base_kwh_anno']}" in testo
    assert f"q_frigo_kwh_anno;{bc['q_frigo_kwh_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh806_demo_calcoli()
    testo = mh806_csv(bc, _demo_kwargs())
    for chiave in _demo_kwargs():
        assert f"{chiave};" in testo


# ------------------------------------------------------- test strutturali
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
    # Token della scheda precedente, costruiti
    # per concatenazione: questo stesso file non li contiene
    # come sottostringhe contigue.
    return ["mh" + "80" + "5", "st" + "80" + "5",
            "tab" + "80" + "5", "w" + "80" + "6",
            "mh" + "80" + "4", "tab" + "80" + "4"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w807_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w807_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab806:")


def test_ui_apre_scheda_attesa_una_volta():
    """Il frammento UI apre la scheda attesa, una sola volta."""
    src = _leggi("w807_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert m.group(1) == "806"
    assert src.count("with tab806:") == 1


def test_ui_titolo_atteso():
    src = _leggi("w807_ui.py")
    titolo = ("Bar / caffetteria: macchina espresso efficiente + "
              "frigo bibite efficiente + recupero calore "
              "macchina su ACS batte macchina espresso "
              "tradizionale + frigo tradizionale + caldaia "
              "a gas?")
    assert src.count(titolo) == 2


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w807_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w807_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st806_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) >= 28
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w807_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 4
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_ui_guard_degenere_stretta():
    """La guard UI della scheda dichiara NON_CALCOLABILE
    anche per tazzine <= 0, prezzi <= 0 e CAPEX <= 0 (piu'
    stretta degli helper, che ammettono lo zero)."""
    src = _leggi("w807_ui.py")
    assert "float(_taz806) <= 0.0" in src
    assert "float(_pg806) <= 0.0" in src
    assert "float(_pel806) <= 0.0" in src
    assert "float(_cx806) <= 0.0" in src
    assert "int(_vita806) <= 0" in src
    assert "Verdetto: NON_CALCOLABILE" in src


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w807_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def806[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w807_ui.py")
        usate = set(re.findall(r'_def806\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 23
        assert usate <= set(mh806_demo().keys())
