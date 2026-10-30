"""Test nuova scheda "Lavanderia self-service /
a gettoni: lavatrici efficienti + asciugatrici
a pompa di calore + recupero calore acque
reflue su ACS batte lavatrici tradizionali +
asciugatrici elettriche tradizionali +
caldaia a gas?" (titolo completo nel frammento UI).
Contenuto pronto da scrivere in repo come test
della scheda lavanderia self-service.

Business case deterministico di una lavanderia
self-service / a gettoni guidato dai CICLI DI
LAVAGGIO AL GIORNO, dai KG PER CICLO e dai
GIORNI DI APERTURA ALL'ANNO: i cicli guidano
l'elettricita' delle lavatrici (kWh_e per
ciclo) e l'acqua calda per ciclo, i kg per
ciclo guidano il carico di asciugatura
(kWh_th per kg); i litri di ACS per ciclo
guidano l'acqua calda di lavaggio.
Cicli annui = cicli al giorno x giorni;
kg annui = cicli annui x kg per ciclo;
elettricita' lavaggio base e alt = cicli
annui x kWh_e per ciclo x fattore (base
1,00, alt 0,70); calore asciugatura = kg
annui x kWh_th per kg; elettricita'
asciugatura base = Q_asc (resistiva, COP = 1
implicito) e alt = Q_asc / COP_asc_alt
(stesso calore, pompa di calore invece della
resistenza); ACS = litri per ciclo x cicli
annui x 4,186 x delta_T / 3600; recupero =
min(ACS, cicli annui x litri per ciclo x
4,186 x delta_rec / 3600) (saturato all'ACS;
nel demo NON satura: il recupero grezzo
18.418,40 e' sotto l'ACS 41.441,40); ACS netta =
max(0, ACS - recupero); gas ACS baseline = ACS /
eta_caldaia (senza recupero); elettricita' PdC
ACS = ACS netta / COP_pdc_acs; C_base =
gas_acs_base / 1000 x p_gas +
(E_lav_base + E_asc_base) / 1000 x p_el +
O&M_base; C_alt = (E_lav_alt +
E_asc_alt + E_pdc_acs) / 1000 x p_el +
O&M_alt (niente gas: l'alternativa non ha
caldaia); risparmio = C_base - C_alt;
CO2_base = gas_acs_base / 1000 x f_gas +
(E_lav_base + E_asc_base) / 1000 x f_el;
CO2_alt = (E_lav_alt + E_asc_alt +
E_pdc_acs) / 1000 x f_el; CO2_evitata =
CO2_base - CO2_alt; flussi [-CAPEX, risparmio
x vita]; VAN, TIR, payback (primo anno con
cumulato >= 0); breakeven gas =
((E_lav_alt + E_asc_alt + E_pdc_acs)
/ 1000 x p_el + O&M_alt - (E_lav_base +
E_asc_base) / 1000 x p_el - O&M_base) /
(gas_acs_base / 1000) EUR/MWh, None se
denominatore gas <= 0 o numeratore < 0,
SOGLIA MINIMA quando esiste.
Verdetto: NON_CALCOLABILE se input degenere
(cicli <= 0, kg < 0, giorni <= 0, eta
<= 0 o > 1, COP <= 1, delta_T <= 0, delta_rec
< 0, prezzi <= 0, CAPEX <= 0, vita <= 0) o
se risparmio <= 0 (guard degenere: UI salta
KPI, grafico, tabella e CSV); altrimenti
CONVIENTE se VAN > 0, MARGINALE se VAN
negativa entro tolleranza % del CAPEX,
NON_CONVIENTE se VAN negativa oltre la
tolleranza. Differenze UI-vs-helper
documentate: cicli = 0 e' calcolabile negli
helper (risparmio negativo, verdetto
NON_CALCOLABILE) ma bloccato dalla guard UI;
CAPEX = 0 e' CONVIENTE negli helper (VAN
positiva, TIR None, payback 0) ma bloccato
dalla guard UI; prezzi = 0 sono ammessi negli
helper ma bloccati dalla guard UI; p_gas = 0
da' risparmio ANCORA POSITIVO negli helper
(11.085,95 EUR/anno, verdetto CONVIENTE:
l'elettricita' risparmiata basta da sola),
quindi QUI c'e' divergenza di verdetto
helper-vs-UI (la UI lo blocca con la guard
sui prezzi, gli helper lo calcolano come
CONVIENTE).
Distinzione esplicita: distinto dalla
lavanderia industriale (kg di biancheria
all'anno in processo industriale continuo,
calore per 1000 kg, recupero da reflui di
processo: qui nessun processo industriale,
driver cicli al giorno di una lavanderia a
gettoni al dettaglio, kg per ciclo, acqua
calda per ciclo, recupero sull'ACS di lavaggio
dei cicli), dal bar / caffetteria (tazzine al
giorno per espresso, bibite al giorno per
frigo, recupero dal calore della macchina
espresso: qui nessuna tazzina, nessuna bibita,
nessuna macchina espresso, driver cicli di
lavaggio al giorno e kg per ciclo, recupero
dalle acque reflue di lavaggio), dalla tavola
calda (porzioni al giorno, forno combinato,
banchi caldi, celle di porzioni: qui nessuna
porzione, nessun forno, driver cicli di
lavaggio al giorno, non porzioni), dal
parrucchiere (lavaggi di capelli, ACS,
recupero dalle acque reflue di lavaggio dei
capelli: qui nessun lavaggio di capelli, il
recupero viene dalle acque reflue dei cicli
di lavaggio dei panni), dalla palestra (docce
utenti, recupero dalle acque delle docce: qui
nessuna doccia, nessun utente che fa sport,
il recupero viene dalle acque reflue dei
cicli), dall'albergo (pernottamento, ACS
docce ospiti: qui nessun ospite, nessuna
doccia), dall'autolavaggio (veicoli lavati,
acque di lavaggio dei veicoli, aria di
asciugatura dei veicoli: qui nessun veicolo,
il carico di asciugatura e' quello dei panni
per kg, guidato dai kg per ciclo): qui driver
CICLI + KG + GIORNI + ACQUA + ASCIUGATURA =
cicli al giorno per lavaggio e ACS, kg per
ciclo per asciugatura, giorni di apertura per
l'anno, litri per ciclo per l'ACS, kWh_th per
kg per il calore di asciugatura; niente
porzioni, niente kg di biancheria industriale
annua, niente tazzine, niente bibite, niente
lavaggi di capelli, niente coperti, niente
docce, niente veicoli.

Demo (lavanderia self-service): 60 cicli al
giorno da 8 kg per ciclo per 330 giorni di
apertura all'anno (19.800 cicli all'anno,
158.400 kg all'anno), carico lavaggio 1,2
kWh_e per ciclo (23.760 kWh_e/anno base,
16.632 alt con fattore 0,70), acqua calda 40
litri per ciclo con delta_T 45 K, salto
recuperato 20 K, carico asciugatura 0,5
kWh_th per kg (79.200 kWh_th/anno), COP
asciugatrice alt 3,0 (base resistiva, COP = 1
implicito), caldaia 0,85, COP PdC ACS 3,0,
gas 90, el 260 EUR/MWh, O&M base 2.000, alt
4.500, CAPEX 60.000, WACC 5 %, vita 12, f_gas
0,20, f_el 0,35, tolleranza 10 % del CAPEX.
Valori calcolati eseguendo mh807_demo_calcoli():
cicli annui 19.800, kg annui 158.400,
E_lav_base 23.760, E_lav_alt 16.632, Q_asc
79.200, E_asc_base 79.200, E_asc_alt 26.400,
Q_acs 41.441,4, Q_rec 18.418,4 (NON
saturato: il recupero grezzo 19.800 x 40 x
4,186 x 20 / 3600 = 18.418,40 e' sotto l'ACS),
Q_acs_net 23.023, gas_acs_base
48.754,58823529412, E_pdc_acs
7.674,333333333333, C_base
33.157,512941176465, C_alt
17.683,646666666667, risparmio
15.473,866274509797, CO2_base
45,78691764705882, CO2_alt
17,747216666666667, CO2_evitata
28,039700980392155, VAN 77.148,77057973898,
TIR 23,80002600275105 %, payback 4,
breakeven gas None (numeratore negativo: a
prezzo gas zero l'alternativa e' gia' piu'
conveniente), verdetto CONVIENTE.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w808_helpers import (
    demo_calcoli,
    mh807_breakeven_gas,
    mh807_c_alt,
    mh807_c_base,
    mh807_calcola,
    mh807_cicli_anno,
    mh807_co2_alt,
    mh807_co2_base,
    mh807_co2_evitata,
    mh807_cop,
    mh807_csv,
    mh807_demo,
    mh807_demo_calcoli,
    mh807_e_asc_alt,
    mh807_e_asc_base,
    mh807_e_lav,
    mh807_e_pdc_acs,
    mh807_eta,
    mh807_flussi,
    mh807_frazione,
    mh807_gas_acs,
    mh807_int_pos,
    mh807_kg_anno,
    mh807_num,
    mh807_nneg,
    mh807_payback,
    mh807_pct_tolleranza,
    mh807_pos,
    mh807_pct_wacc,
    mh807_q_acs,
    mh807_q_acs_net,
    mh807_q_asc,
    mh807_q_rec,
    mh807_risparmio,
    mh807_tir,
    mh807_valida,
    mh807_van,
    mh807_verdetto,
)

_DEMO = {
    "cicli_anno": 19800.0,
    "kg_anno": 158400.0,
    "e_lav_base_kwh_anno": 23760.0,
    "e_lav_alt_kwh_anno": 16632.0,
    "q_asc_kwh_anno": 79200.0,
    "e_asc_base_kwh_anno": 79200.0,
    "e_asc_alt_kwh_anno": 26400.0,
    "q_acs_kwh_anno": 41441.4,
    "q_rec_kwh_anno": 18418.4,
    "q_acs_net_kwh_anno": 23023.0,
    "gas_acs_base_kwh_anno": 48754.58823529412,
    "e_pdc_acs_kwh_anno": 7674.333333333333,
    "c_base_eur_anno": 33157.512941176465,
    "c_alt_eur_anno": 17683.646666666667,
    "risparmio_eur_anno": 15473.866274509797,
    "co2_base_t_anno": 45.78691764705882,
    "co2_alt_t_anno": 17.747216666666667,
    "co2_evitata_t_anno": 28.039700980392155,
    "van": 77148.77057973898,
    "tir": 23.80002600275105,
}


def _demo_kwargs():
    return dict(mh807_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh807_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh807_num(3, "x") == 3.0
    assert mh807_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh807_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh807_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh807_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh807_pos(0, "x")
    with pytest.raises(ValueError):
        mh807_pos(-1, "x")
    assert mh807_pos(0.5, "x") == 0.5


def test_cop_maggiore_di_uno():
    assert mh807_cop(3.0, "x") == 3.0
    assert mh807_cop(1.01, "x") == 1.01
    with pytest.raises(ValueError):
        mh807_cop(1.0, "x")
    with pytest.raises(ValueError):
        mh807_cop(0.5, "x")
    with pytest.raises(ValueError):
        mh807_cop(0, "x")


def test_frazione_limiti():
    assert mh807_frazione(0, "x") == 0.0
    assert mh807_frazione(1, "x") == 1.0
    assert mh807_frazione(0.70, "x") == 0.70
    with pytest.raises(ValueError):
        mh807_frazione(-0.01, "x")
    with pytest.raises(ValueError):
        mh807_frazione(1.01, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh807_int_pos(5.0, "x") == 5
    assert mh807_int_pos(330.0, "x") == 330
    with pytest.raises(ValueError):
        mh807_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh807_int_pos(0, "x")


def test_eta_limiti():
    assert mh807_eta(1.0, "x") == 1.0
    assert mh807_eta(0.85, "x") == 0.85
    with pytest.raises(ValueError):
        mh807_eta(0, "x")
    with pytest.raises(ValueError):
        mh807_eta(1.01, "x")


def test_pct_wacc_limiti():
    assert mh807_pct_wacc(0, "x") == 0.0
    assert mh807_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh807_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh807_pct_tolleranza(0, "x") == 0.0
    assert mh807_pct_tolleranza(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh807_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh807_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_cicli_kg_anno_e_lav():
    assert mh807_cicli_anno(60, 330) == 19800.0
    assert mh807_cicli_anno(0, 330) == 0.0
    assert mh807_cicli_anno(30, 330) == 9900.0
    assert mh807_kg_anno(19800, 8) == 158400.0
    assert mh807_kg_anno(0, 8) == 0.0
    assert mh807_kg_anno(19800, 0) == 0.0
    assert mh807_e_lav(19800, 1.2, 1.0) == 23760.0
    assert mh807_e_lav(19800, 1.2, 0.70) == 16632.0
    assert mh807_e_lav(0, 1.2, 1.0) == 0.0
    assert mh807_e_lav(19800, 0, 0.70) == 0.0
    with pytest.raises(ValueError):
        mh807_cicli_anno(-1, 330)
    with pytest.raises(ValueError):
        mh807_cicli_anno(60, 0)
    with pytest.raises(ValueError):
        mh807_cicli_anno(60, 2.5)
    with pytest.raises(ValueError):
        mh807_kg_anno(-1, 8)
    with pytest.raises(ValueError):
        mh807_e_lav(19800, 1.2, 0)
    with pytest.raises(ValueError):
        mh807_e_lav(19800, 1.2, 1.01)
    with pytest.raises(ValueError):
        mh807_e_lav(19800, -0.1, 0.70)
    with pytest.raises(ValueError):
        mh807_e_lav(-1, 1.2, 0.70)


def test_q_asc_e_asc():
    assert mh807_q_asc(158400, 0.5) == 79200.0
    assert mh807_q_asc(0, 0.5) == 0.0
    assert mh807_q_asc(158400, 0) == 0.0
    assert mh807_e_asc_base(79200.0) == 79200.0
    assert mh807_e_asc_base(0) == 0.0
    assert mh807_e_asc_alt(79200.0, 3.0) == pytest.approx(26400.0)
    assert mh807_e_asc_alt(0, 3.0) == 0.0
    with pytest.raises(ValueError):
        mh807_q_asc(158400, -0.1)
    with pytest.raises(ValueError):
        mh807_e_asc_alt(79200.0, 1.0)
    with pytest.raises(ValueError):
        mh807_e_asc_base(-1)


def test_q_acs_formula():
    assert mh807_q_acs(40, 19800, 45) == pytest.approx(41441.4)
    assert mh807_q_acs(0, 19800, 45) == 0.0
    assert mh807_q_acs(80, 19800, 45) == pytest.approx(82882.8)
    assert mh807_q_acs(40, 19800, 22.5) == pytest.approx(20720.7)
    with pytest.raises(ValueError):
        mh807_q_acs(-1, 19800, 45)
    with pytest.raises(ValueError):
        mh807_q_acs(40, -1, 45)
    with pytest.raises(ValueError):
        mh807_q_acs(40, 19800, 0)


def test_q_rec_saturazione_e_acs_netta():
    # Demo: recupero grezzo 18.418,40 sotto l'ACS -> NON satura.
    assert mh807_q_rec(19800, 40, 20, 41441.4) == pytest.approx(18418.4)
    assert mh807_q_rec(19800, 40, 0, 41441.4) == 0.0
    assert mh807_q_rec(19800, 40, 10, 41441.4) == pytest.approx(9209.2)
    # Con delta_rec 50 > delta_T 45 il recupero satura all'ACS.
    assert mh807_q_rec(19800, 40, 50, 41441.4) == 41441.4
    assert mh807_q_rec(19800, 40, 45, 41441.4) == pytest.approx(41441.4)
    with pytest.raises(ValueError):
        mh807_q_rec(19800, 40, -0.1, 41441.4)
    with pytest.raises(ValueError):
        mh807_q_rec(-1, 40, 20, 41441.4)
    assert mh807_q_acs_net(41441.4, 18418.4) == pytest.approx(23023.0)
    assert mh807_q_acs_net(41441.4, 0.0) == pytest.approx(41441.4)
    assert mh807_q_acs_net(41441.4, 41441.4) == 0.0
    with pytest.raises(ValueError):
        mh807_q_acs_net(-1, 18418.4)
    with pytest.raises(ValueError):
        mh807_q_acs_net(41441.4, -1)


def test_gas_acs_e_pdc_acs():
    assert mh807_gas_acs(41441.4, 0.85) == pytest.approx(48754.58823529412)
    assert mh807_gas_acs(0, 0.85) == 0.0
    assert mh807_gas_acs(41441.4, 1.0) == pytest.approx(41441.4)
    assert mh807_e_pdc_acs(23023.0, 3.0) == pytest.approx(7674.333333333333)
    assert mh807_e_pdc_acs(0.0, 3.0) == 0.0
    with pytest.raises(ValueError):
        mh807_gas_acs(41441.4, 0)
    with pytest.raises(ValueError):
        mh807_gas_acs(41441.4, 1.01)
    with pytest.raises(ValueError):
        mh807_e_pdc_acs(23023.0, 1.0)


def test_c_base_c_alt_scomposizione():
    assert mh807_c_base(48754.58823529412, 90, 23760.0,
                        79200.0, 260,
                        2000) == pytest.approx(33157.512941176465)
    assert mh807_c_base(48754.58823529412, 0, 23760.0,
                        79200.0, 260,
                        2000) == pytest.approx(28769.6)
    assert mh807_c_alt(16632.0, 26400.0, 7674.333333333333, 260,
                       4500) == pytest.approx(17683.646666666667)
    assert mh807_c_alt(16632.0, 26400.0, 0.0, 260,
                       4500) == pytest.approx(15688.32)
    with pytest.raises(ValueError):
        mh807_c_base(48754.59, 90, 23760.0, 79200.0, 260, -1)
    with pytest.raises(ValueError):
        mh807_c_alt(16632.0, 26400.0, 7674.33, 260, -1)


def test_risparmio_segno():
    assert mh807_risparmio(33157.512941176465, 17683.646666666667) == pytest.approx(15473.866274509797)
    assert mh807_risparmio(17683.65, 17683.65) == 0.0


def test_co2_base_alt_evitata():
    assert mh807_co2_base(48754.58823529412, 0.20, 23760.0,
                          79200.0,
                          0.35) == pytest.approx(45.78691764705882)
    assert mh807_co2_alt(16632.0, 26400.0, 7674.333333333333,
                         0.35) == pytest.approx(17.747216666666667)
    assert mh807_co2_evitata(48754.58823529412, 0.20, 23760.0,
                             79200.0, 16632.0,
                             26400.0, 7674.333333333333,
                             0.35) == pytest.approx(28.039700980392155)
    assert mh807_co2_base(0, 0.20, 0, 0, 0.35) == pytest.approx(0.0)
    assert mh807_co2_alt(0, 0, 0, 0.35) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh807_co2_base(48754.59, -0.10, 23760.0, 79200.0, 0.35)
    with pytest.raises(ValueError):
        mh807_co2_alt(16632.0, 26400.0, 7674.33, -0.10)


def test_breakeven_demo_none_e_varianti():
    # Demo: numeratore negativo -> None (non una soglia).
    assert mh807_demo_calcoli()["breakeven_gas_eur_mwh"] is None
    assert mh807_breakeven_gas(16632.0, 26400.0, 7674.333333333333,
                               260, 4500,
                               23760.0, 79200.0, 2000,
                               48754.58823529412) is None
    # Variante O&M alternativo 20.000: be 90,54 (soglia minima).
    bc = _variante(om_alt=20000)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(90.53602597080862)
    # Variante senza kg: be 54,19 (solo lavaggio + ACS da pareggiare).
    assert _variante(kg_per_ciclo=0)["breakeven_gas_eur_mwh"] == pytest.approx(54.190728755946154)
    # Variante senza ACS: denominatore gas nullo -> None.
    assert _variante(litri_acs_per_ciclo=0)["breakeven_gas_eur_mwh"] is None
    # Denominatore gas nullo diretto -> None.
    assert mh807_breakeven_gas(16632.0, 26400.0, 7674.333333333333,
                               260, 4500,
                               23760.0, 79200.0, 2000,
                               0) is None
    with pytest.raises(ValueError):
        mh807_breakeven_gas(16632.0, 26400.0, 7674.33, 260, 4500,
                            23760.0, 79200.0, 2000,
                            -1)


def test_breakeven_verifica_pareggio():
    be = _variante(om_alt=20000)["breakeven_gas_eur_mwh"]
    assert be == pytest.approx(90.53602597080862)
    bc = _variante(om_alt=20000, p_gas=be)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert mh807_demo_calcoli()["breakeven_gas_eur_mwh"] is None
    assert mh807_demo_calcoli()["gas_acs_base_kwh_anno"] > 0.0


def test_breakeven_soglia_minima():
    bc_alto = _variante(om_alt=20000, p_gas=91.53602597080862)
    bc_basso = _variante(om_alt=20000, p_gas=89.0)
    assert bc_alto["c_alt_eur_anno"] < bc_alto["c_base_eur_anno"]
    assert bc_basso["c_alt_eur_anno"] > bc_basso["c_base_eur_anno"]
    assert bc_alto["verdetto"] == "NON_CONVIENTE"
    assert bc_basso["verdetto"] == "NON_CALCOLABILE"


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh807_flussi(60000, 15473.866274509797, 12)
    assert len(fl) == 13
    assert fl[0] == -60000
    assert all(f == 15473.866274509797 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh807_demo_calcoli()
    assert bc["van"] == pytest.approx(77148.77057973898)
    assert mh807_van([-60000] + [15473.866274509797] * 12,
                     0) == pytest.approx(125686.39529411757)
    assert mh807_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh807_demo_calcoli()
    assert bc["tir"] == pytest.approx(23.80002600275105)
    assert mh807_tir([-60000] + [15473.866274509797] * 12) == \
        pytest.approx(0.2380002600275105)
    tir = mh807_tir([-60000] + [15473.866274509797] * 12)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-60000] + [15473.866274509797] * 12))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh807_payback([-60000] + [15473.866274509797] * 12) == 4
    assert mh807_payback([-60000] + [-1000.0] * 12) is None
    assert mh807_payback([0] + [15473.866274509797] * 12) == 0
    assert mh807_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh807_verdetto(15473.866274509797, 77148.77057973898, 60000,
                          10.0) == "CONVIENTE"
    assert mh807_verdetto(6486.933137254899, -2504.6792556915248, 60000,
                          10.0) == "MARGINALE"
    assert mh807_verdetto(6486.933137254899, -6000.0, 60000, 10.0) == "MARGINALE"
    assert mh807_verdetto(6486.933137254899, -6000.01, 60000, 10.0) == "NON_CONVIENTE"
    assert mh807_verdetto(15473.866274509797, 0.0, 60000, 10.0) == "MARGINALE"
    assert mh807_verdetto(0.0, 77148.77, 60000,
                          10.0) == "NON_CALCOLABILE"
    assert mh807_verdetto(-2500.0, -82158.13, 60000,
                          10.0) == "NON_CALCOLABILE"
    assert mh807_verdetto(None, 77148.77, 60000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh807_verdetto(float("nan"), 77148.77, 60000, 10.0)
    with pytest.raises(ValueError):
        mh807_verdetto(15473.866274509797, 77148.77, -1, 10.0)
    with pytest.raises(ValueError):
        mh807_verdetto(15473.866274509797, 77148.77, 60000, 100.1)


def test_valida_demo_ok():
    v = mh807_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("cicli_giorno", "60"),
                       ("cicli_giorno", float("nan")),
                       ("cicli_giorno", float("inf")),
                       ("cicli_giorno", True),
                       ("p_gas", None),
                       ("q_asc_per_kg", "0.5")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh807_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("cicli_giorno", -10),
                          ("kg_per_ciclo", -10),
                          ("giorni_anno", 0),
                          ("giorni_anno", 2.5),
                          ("e_lav_per_ciclo_base", -0.1),
                          ("fattore_lav_alt", 0),
                          ("fattore_lav_alt", 1.01),
                          ("litri_acs_per_ciclo", -1),
                          ("delta_t_acs", 0),
                          ("delta_t_acs", -5),
                          ("delta_rec", -0.1),
                          ("q_asc_per_kg", -0.1),
                          ("cop_asc_alt", 1.0),
                          ("cop_asc_alt", 0.5),
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
        assert mh807_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"cicli_giorno": 0,
              "kg_per_ciclo": 0,
              "e_lav_per_ciclo_base": 0,
              "litri_acs_per_ciclo": 0,
              "delta_rec": 0,
              "q_asc_per_kg": 0,
              "p_gas": 0,
              "p_el": 0,
              "om_base": 0, "om_alt": 0,
              "capex": 0, "wacc_pct": 0,
              "f_gas": 0, "f_el": 0,
              "tolleranza_pct": 0})
    assert mh807_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["delta_rec"] = 50
    d["cicli_giorno"] = 60
    assert mh807_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh807_demo()
    assert d["cicli_giorno"] == 60
    assert d["giorni_anno"] == 330
    assert d["kg_per_ciclo"] == 8
    assert d["e_lav_per_ciclo_base"] == 1.2
    assert d["fattore_lav_alt"] == 0.70
    assert d["litri_acs_per_ciclo"] == 40
    assert d["delta_t_acs"] == 45
    assert d["delta_rec"] == 20
    assert d["q_asc_per_kg"] == 0.5
    assert d["cop_asc_alt"] == 3.0
    assert d["eta_caldaia_base"] == 0.85
    assert d["cop_pdc_acs"] == 3.0
    assert d["p_gas"] == 90
    assert d["p_el"] == 260
    assert d["om_base"] == 2000
    assert d["om_alt"] == 4500
    assert d["capex"] == 60000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 12
    assert d["f_gas"] == 0.20
    assert d["f_el"] == 0.35
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    bc = mh807_demo_calcoli()
    for chiave, atteso in _DEMO.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert got == pytest.approx(atteso, rel=1e-9), chiave
    assert bc["payback"] == 4
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True
    assert demo_calcoli()["van"] == bc["van"]


def test_demo_calcoli_fisica_economia():
    bc = mh807_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(33157.512941176465)
    assert bc["c_alt_eur_anno"] == pytest.approx(17683.646666666667)
    assert bc["risparmio_eur_anno"] == pytest.approx(15473.866274509797)
    assert bc["co2_base_t_anno"] == pytest.approx(45.78691764705882)
    assert bc["co2_alt_t_anno"] == pytest.approx(17.747216666666667)
    assert bc["co2_evitata_t_anno"] == pytest.approx(28.039700980392155)
    assert bc["cicli_anno"] == pytest.approx(19800.0)
    assert bc["kg_anno"] == pytest.approx(158400.0)
    assert bc["q_asc_kwh_anno"] == pytest.approx(79200.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(18418.4)
    assert bc["q_acs_net_kwh_anno"] == pytest.approx(23023.0)


def test_demo_flussi_e_cumulato():
    bc = mh807_demo_calcoli()
    assert bc["flussi"][0] == -60000
    assert len(bc["flussi"]) == 13
    assert all(f == pytest.approx(15473.866274509797) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -60000
    assert righe.iloc[3]["Cumulato (EUR)"] == pytest.approx(-13578.401176470608)
    assert righe.iloc[4]["Cumulato (EUR)"] == pytest.approx(1895.465098039189)
    assert righe.iloc[12]["Cumulato (EUR)"] == pytest.approx(125686.39529411757)


def test_demo_tabella_righe():
    bc = mh807_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Cicli all'anno"] == pytest.approx(19800.0)
    assert mappa["Kg all'anno"] == pytest.approx(158400.0)
    assert mappa["Elettricita' lavaggio base (kWh_e/anno)"] == pytest.approx(23760.0)
    assert mappa["Elettricita' lavaggio alt (kWh_e/anno)"] == pytest.approx(16632.0)
    assert mappa["Calore asciugatura (kWh_th/anno)"] == pytest.approx(79200.0)
    assert mappa["Elettricita' asciugatura base (kWh_e/anno)"] == pytest.approx(79200.0)
    assert mappa["Elettricita' asciugatura alt (kWh_e/anno)"] == pytest.approx(26400.0)
    assert mappa["ACS di lavaggio cicli (kWh_th/anno)"] == pytest.approx(41441.4)
    assert mappa["Calore acque reflue recuperato (kWh_th/anno)"] == pytest.approx(18418.4)
    assert mappa["ACS netta (kWh_th/anno)"] == pytest.approx(23023.0)
    assert mappa["Gas ACS baseline (kWh/anno)"] == pytest.approx(48754.58823529412)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(33157.512941176465)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(17683.646666666667)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(15473.866274509797)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(28.039700980392155)
    assert mappa["Payback (anni)"] == 4
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] is None


def test_demo_coerenza_interna():
    bc = mh807_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["cicli_anno"] == pytest.approx(
        bc["cicli_giorno"] * bc["giorni_anno"])
    assert bc["kg_anno"] == pytest.approx(
        bc["cicli_anno"] * bc["kg_per_ciclo"])
    assert bc["e_lav_base_kwh_anno"] == pytest.approx(
        bc["cicli_anno"] * bc["e_lav_per_ciclo_base"] * 1.0)
    assert bc["e_lav_alt_kwh_anno"] == pytest.approx(
        bc["cicli_anno"] * bc["e_lav_per_ciclo_base"]
        * bc["fattore_lav_alt"])
    assert bc["q_asc_kwh_anno"] == pytest.approx(
        bc["kg_anno"] * bc["q_asc_per_kg"])
    assert bc["e_asc_base_kwh_anno"] == pytest.approx(
        bc["q_asc_kwh_anno"])
    assert bc["e_asc_alt_kwh_anno"] == pytest.approx(
        bc["q_asc_kwh_anno"] / bc["cop_asc_alt"])
    assert bc["q_acs_kwh_anno"] == pytest.approx(
        bc["litri_acs_per_ciclo"] * bc["cicli_anno"]
        * 4.186 * bc["delta_t_acs"] / 3600.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(
        min(bc["q_acs_kwh_anno"],
            bc["cicli_anno"] * bc["litri_acs_per_ciclo"]
            * 4.186 * bc["delta_rec"] / 3600.0))
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
        + (bc["e_lav_base_kwh_anno"]
           + bc["e_asc_base_kwh_anno"]) / 1000.0 * bc["p_el"]
        + bc["om_base"])
    assert bc["c_alt_eur_anno"] == pytest.approx(
        (bc["e_lav_alt_kwh_anno"]
         + bc["e_asc_alt_kwh_anno"]
         + bc["e_pdc_acs_kwh_anno"])
        / 1000.0 * bc["p_el"]
        + bc["om_alt"])


def test_demo_contro_riconteggio_indipendente():
    ci, kgc, gg = 60, 8, 330
    elc, fla = 1.2, 0.70
    lit, dt, drec = 40, 45, 20
    qak, copa = 0.5, 3.0
    eta, copp = 0.85, 3.0
    pg, pel = 90, 260
    omb, oma, cx = 2000, 4500, 60000
    fg, fel, wacc, vita = 0.20, 0.35, 5.0, 12
    cia = ci * gg
    kga = cia * kgc
    elb = cia * elc * 1.0
    ela = cia * elc * fla
    qask = kga * qak
    eabk = qask
    eaak = qask / copa
    qacs = lit * cia * 4.186 * dt / 3600.0
    qrec = min(qacs, cia * lit * 4.186 * drec / 3600.0)
    qnet = max(0.0, qacs - qrec)
    gasa = qacs / eta
    epdc = qnet / copp
    cb = gasa / 1000.0 * pg + (elb + eabk) / 1000.0 * pel + omb
    ca = (ela + eaak + epdc) / 1000.0 * pel + oma
    risp = cb - ca
    co2b = gasa / 1000.0 * fg + (elb + eabk) / 1000.0 * fel
    co2a = (ela + eaak + epdc) / 1000.0 * fel
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    bc = mh807_demo_calcoli()
    assert bc["cicli_anno"] == pytest.approx(cia)
    assert bc["kg_anno"] == pytest.approx(kga)
    assert bc["e_lav_base_kwh_anno"] == pytest.approx(elb)
    assert bc["e_lav_alt_kwh_anno"] == pytest.approx(ela)
    assert bc["q_asc_kwh_anno"] == pytest.approx(qask)
    assert bc["e_asc_base_kwh_anno"] == pytest.approx(eabk)
    assert bc["e_asc_alt_kwh_anno"] == pytest.approx(eaak)
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
    assert bc["breakeven_gas_eur_mwh"] is None


# ---------------------------------------------------------------- varianti
def test_variante_gas_zero_helper_conviente_ma_ui_guard():
    # Negli helper p_gas = 0 e' ammesso e qui il
    # risparmio RESTA POSITIVO (11.085,95
    # EUR/anno): verdetto CONVIENTE anche negli
    # helper, quindi DIVERGENZA di verdetto con
    # la guard UI (prezzi <= 0), che lo
    # intercetta prima (diversa dalla scheda
    # bar, dove gas zero dava risparmio
    # negativo anche negli helper).
    bc = _variante(p_gas=0)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(11085.953333333331)
    assert bc["van"] == pytest.approx(38257.594023261765)
    assert bc["payback"] == 6
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_senza_recupero_conviente():
    bc = _variante(delta_rec=0)
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["q_acs_net_kwh_anno"] == pytest.approx(41441.4)
    assert bc["e_pdc_acs_kwh_anno"] == pytest.approx(13813.8)
    assert bc["risparmio_eur_anno"] == pytest.approx(13877.604941176462)
    assert bc["van"] == pytest.approx(63000.704704872325)
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["payback"] == 5
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_recupero_parziale():
    bc = _variante(delta_rec=10)
    assert bc["q_rec_kwh_anno"] == pytest.approx(9209.2)
    assert bc["q_acs_net_kwh_anno"] == pytest.approx(32232.2)
    assert bc["e_pdc_acs_kwh_anno"] == pytest.approx(10744.066666666667)
    assert bc["risparmio_eur_anno"] == pytest.approx(14675.735607843133)
    assert bc["van"] == pytest.approx(70074.73764230567)
    assert bc["payback"] == 5
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_recupero_pieno_satura():
    bc = _variante(delta_rec=50)
    assert bc["q_rec_kwh_anno"] == pytest.approx(41441.4)
    assert bc["q_acs_net_kwh_anno"] == 0.0
    assert bc["e_pdc_acs_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(17469.192941176465)
    assert bc["van"] == pytest.approx(94833.85292332227)
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["payback"] == 4
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_cicli_piccoli_marginale():
    bc = _variante(cicli_giorno=30)
    assert bc["cicli_anno"] == pytest.approx(9900.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(6486.933137254899)
    assert bc["van"] == pytest.approx(-2504.6792556915248)
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["payback"] == 10
    assert bc["verdetto"] == "MARGINALE"


def test_variante_capex_conviente():
    bc = _variante(capex=120000)
    assert bc["risparmio_eur_anno"] == pytest.approx(15473.866274509797)
    assert bc["van"] == pytest.approx(17148.770579738964)
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    # Negli helper CAPEX = 0 e' CONVIENTE (VAN
    # positiva, TIR None, payback 0); in UI e'
    # guard degenere (NON_CALCOLABILE): divergenza
    # documentata, vedi test_ui_guard_degenere_stretta.
    bc = _variante(capex=0)
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(137148.77057973895, rel=1e-6)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(125686.39529411757)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(59485.09370141714)
    assert bc2["payback"] == 4
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_el_alto_e_om_alt_alto():
    bc = _variante(p_el=400)
    assert bc["risparmio_eur_anno"] == pytest.approx(22789.37960784314)
    assert bc["van"] == pytest.approx(141988.00610286882)
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["payback"] == 3
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(om_alt=10000)
    assert bc2["risparmio_eur_anno"] == pytest.approx(9973.866274509797)
    assert bc2["van"] == pytest.approx(28400.886579270533)
    assert bc2["payback"] == 7
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_senza_kg_e_senza_acs():
    bc = _variante(kg_per_ciclo=0)
    assert bc["kg_anno"] == 0.0
    assert bc["q_asc_kwh_anno"] == 0.0
    assert bc["e_asc_base_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(1745.8662745098045)
    assert bc["van"] == pytest.approx(-44525.94788543019)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(54.190728755946154)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"
    bc2 = _variante(litri_acs_per_ciclo=0)
    assert bc2["q_acs_kwh_anno"] == 0.0
    assert bc2["q_rec_kwh_anno"] == 0.0
    assert bc2["gas_acs_base_kwh_anno"] == 0.0
    assert bc2["breakeven_gas_eur_mwh"] is None
    assert bc2["risparmio_eur_anno"] == pytest.approx(13081.28)
    assert bc2["van"] == pytest.approx(55942.67636684504)
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_senza_cicli_non_calcolabile():
    # Negli helper cicli = 0 resta calcolabile
    # (risparmio negativo, verdetto
    # NON_CALCOLABILE); in UI e' guard degenere
    # (cicli <= 0): divergenza documentata.
    bc = _variante(cicli_giorno=0)
    assert bc["cicli_anno"] == 0.0
    assert bc["e_lav_base_kwh_anno"] == 0.0
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["risparmio_eur_anno"] == pytest.approx(-2500.0)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_lav_alt_uguale_base():
    bc = _variante(fattore_lav_alt=1.0)
    assert bc["e_lav_alt_kwh_anno"] == pytest.approx(23760.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(13620.586274509798)
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["verdetto"] == "CONVIENTE"


def test_monotonia_prezzo_gas_crescente():
    base = mh807_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas=91)["risparmio_eur_anno"]
    basso = _variante(p_gas=89)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(48.75458823529412, abs=1e-2)
    assert base - basso == pytest.approx(48.75458823529412, abs=1e-2)


def test_monotonia_cicli_crescente():
    assert _variante(cicli_giorno=30)["risparmio_eur_anno"] < \
        mh807_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(cicli_giorno=120)["risparmio_eur_anno"] > \
        mh807_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(cicli_giorno=120)["cicli_anno"] == \
        pytest.approx(39600.0)


def test_demo_deterministica_due_chiamate():
    a = mh807_demo_calcoli()
    b = mh807_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh807_demo().keys()) == {
        "cicli_giorno", "giorni_anno",
        "kg_per_ciclo", "e_lav_per_ciclo_base",
        "fattore_lav_alt",
        "litri_acs_per_ciclo", "delta_t_acs",
        "delta_rec",
        "q_asc_per_kg", "cop_asc_alt",
        "eta_caldaia_base", "cop_pdc_acs",
        "p_gas", "p_el",
        "om_base", "om_alt",
        "capex", "wacc_pct", "vita_anni",
        "f_gas", "f_el",
        "tolleranza_pct"}


# ---------------------------------------------------------------- degenere
def test_degenere_cop_uguale_uno_sollevela():
    with pytest.raises(ValueError):
        _variante(cop_asc_alt=1.0)
    with pytest.raises(ValueError):
        _variante(cop_pdc_acs=1.0)


def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"cicli_giorno": -10},
               {"kg_per_ciclo": -10},
               {"giorni_anno": 0},
               {"giorni_anno": 2.5},
               {"e_lav_per_ciclo_base": -0.1},
               {"fattore_lav_alt": 0}, {"fattore_lav_alt": 1.01},
               {"litri_acs_per_ciclo": -1},
               {"delta_t_acs": 0}, {"delta_t_acs": -5},
               {"delta_rec": -0.1},
               {"q_asc_per_kg": -0.1},
               {"cop_asc_alt": 1.0}, {"cop_asc_alt": 0.5},
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
        assert mh807_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"cicli_giorno": "60"},
               {"cicli_giorno": float("nan")},
               {"p_gas": float("inf")},
               {"capex": True},
               {"q_asc_per_kg": "0.5"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh807_valida(**d)["valido"] is False


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    for kw in ({"cicli_giorno": 0},
               {"om_alt": 20000}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] <= 0.0
        assert bc["verdetto"] == "NON_CALCOLABILE"
        assert bc["flussi"]


def test_pareggio_esatto_tolleranza_float():
    # A pareggio esatto (prezzo gas = breakeven
    # della variante om_alt 20.000) il risparmio
    # e' zero (circa 0.0, quindi guard
    # NON_CALCOLABILE): in nessun caso
    # CONVIENTE.
    be = _variante(om_alt=20000)["breakeven_gas_eur_mwh"]
    bc = _variante(om_alt=20000, p_gas=be)
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["verdetto"] != "CONVIENTE"
    bc2 = _variante(om_alt=20000, p_gas=be + 1)
    assert bc2["risparmio_eur_anno"] == pytest.approx(48.75458823529412, abs=1e-2)
    assert bc2["verdetto"] == "NON_CONVIENTE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh807_demo_calcoli()
    testo = mh807_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_gas_eur_mwh" in testo
    assert "co2_evitata_t_anno" in testo
    assert "q_asc_kwh_anno" in testo
    assert "cicli_giorno" in testo
    assert "kg_per_ciclo" in testo
    assert "e_asc_alt_kwh_anno" in testo
    assert "e_lav_alt_kwh_anno" in testo
    assert "q_rec_kwh_anno" in testo
    assert "q_acs_net_kwh_anno" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh807_demo_calcoli()
    testo = mh807_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"cicli_anno;{bc['cicli_anno']}" in testo
    assert f"gas_acs_base_kwh_anno;{bc['gas_acs_base_kwh_anno']}" in testo
    assert f"q_asc_kwh_anno;{bc['q_asc_kwh_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh807_demo_calcoli()
    testo = mh807_csv(bc, _demo_kwargs())
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
    return ["mh" + "80" + "6", "st" + "80" + "6",
            "tab" + "80" + "6", "w" + "80" + "7",
            "mh" + "80" + "5", "tab" + "80" + "5"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w808_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w808_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab807:")


def test_ui_apre_scheda_attesa_una_volta():
    """Il frammento UI apre la scheda attesa, una sola volta."""
    src = _leggi("w808_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert m.group(1) == "807"
    assert src.count("with tab807:") == 1


def test_ui_titolo_atteso():
    src = _leggi("w808_ui.py")
    titolo = ("Lavanderia self-service / a gettoni: lavatrici "
              "efficienti + asciugatrici a pompa di calore + "
              "recupero calore acque reflue su ACS batte "
              "lavatrici tradizionali + asciugatrici "
              "elettriche tradizionali + caldaia a gas?")
    assert src.count(titolo) == 2


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w808_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w808_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st807_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) >= 28
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w808_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 4
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_ui_guard_degenere_stretta():
    """La guard UI della scheda dichiara NON_CALCOLABILE
    anche per cicli <= 0, prezzi <= 0 e CAPEX <= 0 (piu'
    stretta degli helper, che ammettono lo zero)."""
    src = _leggi("w808_ui.py")
    assert "float(_ci807) <= 0.0" in src
    assert "float(_pg807) <= 0.0" in src
    assert "float(_pel807) <= 0.0" in src
    assert "float(_cx807) <= 0.0" in src
    assert "int(_vita807) <= 0" in src
    assert "Verdetto: NON_CALCOLABILE" in src


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w808_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def807[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w808_ui.py")
        usate = set(re.findall(r'_def807\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 22
        assert usate <= set(mh807_demo().keys())
