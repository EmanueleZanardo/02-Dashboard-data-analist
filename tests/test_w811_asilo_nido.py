"""Test nuova scheda "Asilo nido: pompa di
calore + recupero calore ventilazione aule +
mensa e lavanderia efficienti batte caldaia a
gas + chiller + mensa tradizionale?" (titolo
completo nel frammento UI). Contenuto pronto
da scrivere in repo come test della scheda
asilo nido.

Business case deterministico di un asilo nido
guidato dai M2 DI SUPERFICIE e dai GIORNI DI
APERTURA ALL'ANNO: i m2 guidano riscaldamento
e raffrescamento, i giorni guidano l'anno,
eta_rec e f_vent guidano il recupero di calore
dalla ventilazione delle aule, pasti al giorno
x giorni guidano la mensa (kWh termici per
pasto in baseline, kWh elettrici per pasto
nell'alternativa), litri al giorno x giorni x
4,186 x delta_T / 3600 guidano l'ACS, kg al
giorno x giorni x kWh per kg guidano la
lavanderia.
Riscaldamento = S x q_risc; raffrescamento =
S x q_raff; recupero ventilazione = eta_rec x
f_vent x Q_risc; riscaldamento netto = Q_risc
- recupero; ACS = litri_giorno x giorni x
4,186 x delta_T / 3600; pasti all'anno = pasti
al giorno x giorni; calore mensa base = pasti
all'anno x kWh termici per pasto; elettricita'
mensa alt = pasti all'anno x kWh elettrici per
pasto; lavanderia base = kg x giorni x kWh per
kg e alt = base x 0,55 (letterale); gas
baseline = (riscaldamento + ACS + calore mensa
base) / 0,90 (eta_caldaia letterale, senza
recupero); chiller = raffrescamento / 3,0;
E_base = chiller + lavanderia base; E_pdc =
riscaldamento netto / 3,4 + raffrescamento /
3,2 + ACS / 3,0 (COP letterali); E_alt = E_pdc
+ mensa alt + lavanderia alt; C_base =
gas_base / 1000 x p_gas + E_base / 1000 x p_el
+ O&M_base; C_alt = E_alt / 1000 x p_el +
O&M_alt (niente gas: l'alternativa non ha
caldaia); risparmio = C_base - C_alt; CO2
evitata = (gas_base x 0,20 + E_base x 0,35 -
E_alt x 0,35) / 1000 (fattori letterali);
flussi [-CAPEX, risparmio x vita]; VAN, TIR,
payback (primo anno con cumulato >= 0);
breakeven gas = (C_alt - O&M_base - E_base /
1000 x p_el) x 1000 / gas_base EUR/MWh, None
se gas_base <= 0 o numeratore < 0, SOGLIA
MINIMA quando esiste.
Verdetto: NON_CALCOLABILE se input degenere
(superficie <= 0, giorni <= 0, carichi <= 0,
eta_rec o f_vent fuori [0, 1], litri <= 0,
delta_T <= 0, pasti <= 0, kWh per pasto
negativi, kg <= 0, energia per kg negativa,
prezzi <= 0, CAPEX <= 0, vita <= 0) o se
risparmio <= 0 (guard degenere: UI salta KPI,
grafico, tabella e CSV); altrimenti CONVIENTE
se VAN > 0, MARGINALE se VAN negativa entro
tolleranza % del CAPEX, NON_CONVIENTE se VAN
negativa oltre la tolleranza. Differenze
UI-vs-helper documentate: S = 0 e' calcolabile
negli helper (risparmio -704,81 EUR/anno, VAN
-22.315,67 EUR, verdetto NON_CALCOLABILE,
breakeven 147,89 EUR/MWh) e bloccato dalla
guard UI (NON_CALCOLABILE): qui NON c'e'
divergenza di verdetto, solo guard prima (la
mensa a gas resta anche senza superficie, ma
non basta a rendere positivo il risparmio);
CAPEX = 0 e' CONVIENTE negli helper (VAN
positiva, TIR None, payback 0) ma bloccato
dalla guard UI; prezzi = 0 sono ammessi negli
helper ma bloccati dalla guard UI (p_el = 0
resta CONVIENTE negli helper, p_gas = 0 da'
invece risparmio NEGATIVO negli helper,
-5.048,22 EUR/anno, verdetto NON_CALCOLABILE:
per gas zero QUI NON c'e' divergenza di
verdetto helper-vs-UI, solo guard prima).
Distinzione esplicita: distinto dalla clinica
veterinaria (autoclave, frigoriferi farmaci e
lavanderia lettiere: qui nessuna autoclave,
nessun frigorifero farmaci, la mensa e' dei
bambini con pasti al giorno e kWh per pasto,
e il recupero e' quello della ventilazione
delle aule, non delle sale operatorie),
dall'ospedale (posti letto e reparti di
degenza umana: qui nessun posto letto umano,
nessun reparto ospedaliero), dalla scuola
generica senza mensa interna (qui la mensa
interna e' un driver a pieno titolo): qui
driver M2 + GIORNI + VENTILAZIONE + MENSA +
LAVANDERIA + ACS.

Demo (asilo nido): superficie 500 m2 per 220
giorni di apertura all'anno, 100 kWh_th/m2 di
riscaldamento (50.000 kWh_th/anno) e 55
kWh_th/m2 di raffrescamento (27.500
kWh_th/anno), rendimento di recupero 0,60 e
frazione di ventilazione 0,35 (recupero
10.500 kWh_th/anno, riscaldamento netto
39.500 kWh_th/anno), ACS 300 litri al giorno
con delta_T 35 K (66.000 litri all'anno,
2.686,016... kWh_th/anno), mensa 60 pasti al
giorno (13.200 pasti all'anno, 10.560
kWh_th/anno base da 0,8 kWh_th per pasto,
6.600 kWh_e/anno alt da 0,5 kWh_e per pasto),
lavanderia 30 kg al giorno da 1,0 kWh_e/kg
(6.600 kg all'anno, 6.600 kWh_e/anno base,
3.630 alt con fattore 0,55), gas 100, el 260
EUR/MWh, O&M base 3.500, alt 4.500, CAPEX
15.000, WACC 5 %, vita 15, tolleranza 10 %
del CAPEX. Valori calcolati eseguendo
mh811_demo_calcoli():
Q_risc 50.000, Q_raff 27.500, Q_vent_rec
10.500, Q_risc_net 39.500, Q_acs
2.686,016666666667, pasti_annui 13.200,
Q_mensa_th_base 10.560, E_mensa_alt 6.600,
E_lav_base 6.600, E_lav_alt 3.630,
gas_base 70.273,35185185185, E_chiller
9.166,666666666666, E_pdc 21.106,73594771242,
E_base 15.766,666666666666, E_alt
31.336,73594771242, C_base 14.626,66851851852,
C_alt 12.647,55134640523, risparmio
1.979,1171721132905, CO2_base
19,573003703703705, CO2_alt 10,967857581699345,
CO2_evitata 8,60514612200436, VAN
5.542,559464026955, TIR 10,062231328468963 %,
payback 8, breakeven gas 71,83687528829414
EUR/MWh (soglia minima), verdetto CONVIENTE.
NOTA: i valori E_alt / C_alt / risparmio /
CO2 evitata di questo ricalcolo differiscono
di esattamente 1.000 kWh_e (260 EUR, 0,35 t)
dai numeri riassuntivi del brief di authoring
(E_alt 32.336,74, C_alt 12.907,55, risparmio
1.719,12, CO2 evitata circa 8,26): le formule
del brief stesso danno E_pdc 21.106,74 +
6.600 + 3.630 = 31.336,74, quindi i valori
qui sopra (ricalcolo indipendente eseguito)
sono quelli corretti e il verdetto CONVIENTE
resta invariato.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w812_helpers import (
    demo_calcoli,
    mh811_breakeven_gas,
    mh811_c_alt,
    mh811_c_base,
    mh811_calcola,
    mh811_co2_alt,
    mh811_co2_base,
    mh811_co2_evitata,
    mh811_cop,
    mh811_csv,
    mh811_demo,
    mh811_demo_calcoli,
    mh811_e_alt,
    mh811_e_base,
    mh811_e_chiller,
    mh811_e_lav_alt,
    mh811_e_lav_base,
    mh811_e_mensa_alt,
    mh811_e_pdc,
    mh811_flussi,
    mh811_frazione,
    mh811_gas_base,
    mh811_int_pos,
    mh811_num,
    mh811_nneg,
    mh811_pasti_annui,
    mh811_payback,
    mh811_pct_tolleranza,
    mh811_pos,
    mh811_pct_wacc,
    mh811_q_acs,
    mh811_q_mensa_th_base,
    mh811_q_raff,
    mh811_q_risc,
    mh811_q_risc_net,
    mh811_q_vent_rec,
    mh811_risparmio,
    mh811_tir,
    mh811_valida,
    mh811_van,
    mh811_verdetto,
)

_DEMO = {
    "q_risc_kwh_anno": 50000.0,
    "q_raff_kwh_anno": 27500.0,
    "q_vent_rec_kwh_anno": 10500.0,
    "q_risc_net_kwh_anno": 39500.0,
    "q_acs_kwh_anno": 2686.016666666667,
    "pasti_annui": 13200.0,
    "q_mensa_th_base_kwh_anno": 10560.0,
    "e_mensa_alt_kwh_anno": 6600.0,
    "e_lav_base_kwh_anno": 6600.0,
    "e_lav_alt_kwh_anno": 3630.0000000000005,
    "gas_base_kwh_anno": 70273.35185185185,
    "e_chiller_kwh_anno": 9166.666666666666,
    "e_pdc_kwh_anno": 21106.73594771242,
    "e_base_kwh_anno": 15766.666666666666,
    "e_alt_kwh_anno": 31336.73594771242,
    "c_base_eur_anno": 14626.66851851852,
    "c_alt_eur_anno": 12647.55134640523,
    "risparmio_eur_anno": 1979.1171721132905,
    "co2_base_t_anno": 19.573003703703705,
    "co2_alt_t_anno": 10.967857581699345,
    "co2_evitata_t_anno": 8.60514612200436,
    "van": 5542.559464026955,
    "tir": 10.062231328468963,
    "breakeven_gas_eur_mwh": 71.83687528829414,
}


def _demo_kwargs():
    return dict(mh811_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh811_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh811_num(3, "x") == 3.0
    assert mh811_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh811_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh811_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh811_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh811_pos(0, "x")
    with pytest.raises(ValueError):
        mh811_pos(-1, "x")
    assert mh811_pos(0.5, "x") == 0.5


def test_cop_maggiore_di_uno():
    assert mh811_cop(3.0, "x") == 3.0
    with pytest.raises(ValueError):
        mh811_cop(1.0, "x")
    with pytest.raises(ValueError):
        mh811_cop(0.5, "x")


def test_frazione_limiti():
    assert mh811_frazione(0, "x") == 0.0
    assert mh811_frazione(1, "x") == 1.0
    assert mh811_frazione(0.60, "x") == 0.60
    assert mh811_frazione(0.35, "x") == 0.35
    with pytest.raises(ValueError):
        mh811_frazione(-0.01, "x")
    with pytest.raises(ValueError):
        mh811_frazione(1.01, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh811_int_pos(5.0, "x") == 5
    assert mh811_int_pos(220.0, "x") == 220
    with pytest.raises(ValueError):
        mh811_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh811_int_pos(0, "x")


def test_pct_wacc_limiti():
    assert mh811_pct_wacc(0, "x") == 0.0
    assert mh811_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh811_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh811_pct_tolleranza(0, "x") == 0.0
    assert mh811_pct_tolleranza(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh811_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh811_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_q_risc_raff_vent_rec_net():
    assert mh811_q_risc(500, 100) == 50000.0
    assert mh811_q_raff(500, 55) == 27500.0
    assert mh811_q_risc(0, 100) == 0.0
    with pytest.raises(ValueError):
        mh811_q_risc(-1, 100)
    assert mh811_q_vent_rec(50000.0, 0.60, 0.35) == pytest.approx(10500.0)
    assert mh811_q_vent_rec(50000.0, 0, 0.35) == 0.0
    assert mh811_q_vent_rec(50000.0, 1, 1) == pytest.approx(50000.0)
    assert mh811_q_risc_net(50000.0, 10500.0) == pytest.approx(39500.0)
    assert mh811_q_risc_net(50000.0, 50000.0) == 0.0
    with pytest.raises(ValueError):
        mh811_q_vent_rec(50000.0, 1.01, 0.35)
    with pytest.raises(ValueError):
        mh811_q_vent_rec(50000.0, 0.60, -0.1)


def test_q_acs():
    assert mh811_q_acs(300, 220, 35) == pytest.approx(2686.016666666667)
    assert mh811_q_acs(0, 220, 35) == 0.0
    with pytest.raises(ValueError):
        mh811_q_acs(-1, 220, 35)
    with pytest.raises(ValueError):
        mh811_q_acs(300, 220, 0)
    with pytest.raises(ValueError):
        mh811_q_acs(300, 0, 35)


def test_pasti_mensa_lavanderia():
    assert mh811_pasti_annui(60, 220) == 13200.0
    assert mh811_pasti_annui(0, 220) == 0.0
    with pytest.raises(ValueError):
        mh811_pasti_annui(-1, 220)
    assert mh811_q_mensa_th_base(13200.0, 0.8) == pytest.approx(10560.0)
    assert mh811_e_mensa_alt(13200.0, 0.5) == pytest.approx(6600.0)
    assert mh811_q_mensa_th_base(0.0, 0.8) == 0.0
    with pytest.raises(ValueError):
        mh811_q_mensa_th_base(13200.0, -0.1)
    assert mh811_e_lav_base(30, 220, 1.0) == 6600.0
    assert mh811_e_lav_alt(6600.0) == pytest.approx(3630.0)
    with pytest.raises(ValueError):
        mh811_e_lav_base(-1, 220, 1.0)


def test_gas_chiller_pdc_e_totali():
    assert mh811_gas_base(50000.0, 2686.016666666667,
                          10560.0) == pytest.approx(70273.35185185185)
    assert mh811_gas_base(0, 0, 0) == 0.0
    with pytest.raises(ValueError):
        mh811_gas_base(-1, 2686.02, 10560.0)
    assert mh811_e_chiller(27500.0) == pytest.approx(9166.666666666666)
    assert mh811_e_pdc(39500.0, 27500.0,
                       2686.016666666667) == pytest.approx(21106.73594771242)
    assert mh811_e_pdc(0.0, 0.0, 0.0) == 0.0
    assert mh811_e_base(9166.666666666666, 6600.0) == pytest.approx(15766.666666666666)
    assert mh811_e_alt(21106.73594771242, 6600.0,
                       3630.0000000000005) == pytest.approx(31336.73594771242)


def test_c_base_c_alt_scomposizione():
    assert mh811_c_base(70273.35185185185, 100, 15766.666666666666, 260,
                        3500) == pytest.approx(14626.66851851852)
    assert mh811_c_base(70273.35185185185, 0, 15766.666666666666, 260,
                        3500) == pytest.approx(7599.333333333333)
    assert mh811_c_alt(31336.73594771242, 260,
                       4500) == pytest.approx(12647.55134640523)
    with pytest.raises(ValueError):
        mh811_c_base(70273.35, 100, 15766.67, 260, -1)
    with pytest.raises(ValueError):
        mh811_c_alt(31336.74, 260, -1)


def test_risparmio_segno():
    assert mh811_risparmio(14626.66851851852, 12647.55134640523) == pytest.approx(1979.1171721132905)
    assert mh811_risparmio(12647.55, 12647.55) == pytest.approx(0.0, abs=1e-9)


def test_co2_base_alt_evitata():
    assert mh811_co2_base(70273.35185185185, 15766.666666666666) == pytest.approx(19.573003703703705)
    assert mh811_co2_alt(31336.73594771242) == pytest.approx(10.967857581699345)
    assert mh811_co2_evitata(70273.35185185185, 15766.666666666666,
                             31336.73594771242) == pytest.approx(8.60514612200436)
    assert mh811_co2_base(0, 0) == 0.0
    assert mh811_co2_alt(0) == 0.0
    with pytest.raises(ValueError):
        mh811_co2_base(70273.35, -1)
    with pytest.raises(ValueError):
        mh811_co2_alt(-1)


def test_breakeven_demo_e_varianti():
    assert mh811_demo_calcoli()["breakeven_gas_eur_mwh"] == pytest.approx(71.83687528829414)
    assert mh811_breakeven_gas(31336.73594771242,
                               260, 4500,
                               15766.666666666666,
                               3500,
                               70273.35185185185) == pytest.approx(71.83687528829414)
    bc = _variante(om_alt=10000)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(150.10267384583173)
    assert _variante(superficie_m2=0)["breakeven_gas_eur_mwh"] == pytest.approx(147.88818022021715)
    assert mh811_breakeven_gas(31336.73594771242,
                               260, 4500,
                               15766.666666666666,
                               3500,
                               0) is None
    with pytest.raises(ValueError):
        mh811_breakeven_gas(31336.74, 260, 4500, 15766.67, 3500, -1)


def test_breakeven_verifica_pareggio():
    be = mh811_demo_calcoli()["breakeven_gas_eur_mwh"]
    assert be == pytest.approx(71.83687528829414)
    bc = _variante(p_gas=be)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert mh811_demo_calcoli()["gas_base_kwh_anno"] > 0.0


def test_breakeven_soglia_minima():
    bc_alto = _variante(p_gas=72.83687528829414)
    bc_basso = _variante(p_gas=70.0)
    assert bc_alto["c_alt_eur_anno"] < bc_alto["c_base_eur_anno"]
    assert bc_basso["c_alt_eur_anno"] > bc_basso["c_base_eur_anno"]
    assert bc_alto["risparmio_eur_anno"] > 0.0
    assert bc_alto["verdetto"] == "NON_CONVIENTE"
    assert bc_basso["verdetto"] == "NON_CALCOLABILE"


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh811_flussi(15000, 1979.1171721132905, 15)
    assert len(fl) == 16
    assert fl[0] == -15000
    assert all(f == 1979.1171721132905 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh811_demo_calcoli()
    assert bc["van"] == pytest.approx(5542.559464026955)
    assert mh811_van([-15000] + [1979.1171721132905] * 15,
                     0) == pytest.approx(14686.757581699358)
    assert mh811_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh811_demo_calcoli()
    assert bc["tir"] == pytest.approx(10.062231328468963)
    assert mh811_tir([-15000] + [1979.1171721132905] * 15) == \
        pytest.approx(0.10062231328468962)
    tir = mh811_tir([-15000] + [1979.1171721132905] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-15000] + [1979.1171721132905] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh811_payback([-15000] + [1979.1171721132905] * 15) == 8
    assert mh811_payback([-15000] + [-1000.0] * 15) is None
    assert mh811_payback([0] + [1979.1171721132905] * 15) == 0
    assert mh811_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh811_verdetto(1979.1171721132905, 5542.559464026955, 15000,
                          10.0) == "CONVIENTE"
    assert mh811_verdetto(1979.1171721132905, -750.0, 15000,
                          10.0) == "MARGINALE"
    assert mh811_verdetto(1979.1171721132905, -1500.0, 15000, 10.0) == "MARGINALE"
    assert mh811_verdetto(1979.1171721132905, -1500.01, 15000, 10.0) == "NON_CONVIENTE"
    assert mh811_verdetto(1979.1171721132905, 0.0, 15000, 10.0) == "MARGINALE"
    assert mh811_verdetto(0.0, 5542.56, 15000,
                          10.0) == "NON_CALCOLABILE"
    assert mh811_verdetto(-5048.218013071896, -67398.78, 15000,
                          10.0) == "NON_CALCOLABILE"
    assert mh811_verdetto(None, 5542.56, 15000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh811_verdetto(float("nan"), 5542.56, 15000, 10.0)
    with pytest.raises(ValueError):
        mh811_verdetto(1979.1171721132905, 5542.56, -1, 10.0)
    with pytest.raises(ValueError):
        mh811_verdetto(1979.1171721132905, 5542.56, 15000, 100.1)


def test_valida_demo_ok():
    v = mh811_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("superficie_m2", "500"),
                       ("superficie_m2", float("nan")),
                       ("superficie_m2", float("inf")),
                       ("superficie_m2", True),
                       ("p_gas", None),
                       ("q_risc_per_m2", "100")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh811_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("superficie_m2", -10),
                          ("q_risc_per_m2", -10),
                          ("q_raff_per_m2", -10),
                          ("giorni_anno", 0),
                          ("giorni_anno", 2.5),
                          ("eta_rec", -0.1),
                          ("eta_rec", 1.01),
                          ("f_vent", -0.1),
                          ("f_vent", 1.01),
                          ("litri_giorno", -1),
                          ("delta_t", 0),
                          ("delta_t", -5),
                          ("pasti_giorno", -1),
                          ("kwh_th_per_pasto", -0.1),
                          ("kwh_e_per_pasto", -0.1),
                          ("kg_giorno", -1),
                          ("e_per_kg", -0.1),
                          ("p_gas", -1),
                          ("p_el", -1),
                          ("om_base", -100),
                          ("om_alt", -100),
                          ("capex", -1),
                          ("wacc_pct", -0.1), ("wacc_pct", 50.1),
                          ("vita_anni", 0), ("vita_anni", 2.5),
                          ("tolleranza_pct", -1),
                          ("tolleranza_pct", 100.1)):
        d = _demo_kwargs()
        d[campo] = valore
        assert mh811_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"superficie_m2": 0,
              "q_risc_per_m2": 0,
              "q_raff_per_m2": 0,
              "eta_rec": 0,
              "f_vent": 0,
              "litri_giorno": 0,
              "pasti_giorno": 0,
              "kwh_th_per_pasto": 0,
              "kwh_e_per_pasto": 0,
              "kg_giorno": 0,
              "e_per_kg": 0,
              "p_gas": 0,
              "p_el": 0,
              "om_base": 0, "om_alt": 0,
              "capex": 0, "wacc_pct": 0,
              "tolleranza_pct": 0})
    assert mh811_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["eta_rec"] = 1
    d["f_vent"] = 1
    assert mh811_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh811_demo()
    assert d["superficie_m2"] == 500
    assert d["giorni_anno"] == 220
    assert d["q_risc_per_m2"] == 100
    assert d["q_raff_per_m2"] == 55
    assert d["eta_rec"] == 0.60
    assert d["f_vent"] == 0.35
    assert d["litri_giorno"] == 300
    assert d["delta_t"] == 35
    assert d["pasti_giorno"] == 60
    assert d["kwh_th_per_pasto"] == 0.8
    assert d["kwh_e_per_pasto"] == 0.5
    assert d["kg_giorno"] == 30
    assert d["e_per_kg"] == 1.0
    assert d["p_gas"] == 100
    assert d["p_el"] == 260
    assert d["om_base"] == 3500
    assert d["om_alt"] == 4500
    assert d["capex"] == 15000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    bc = mh811_demo_calcoli()
    for chiave, atteso in _DEMO.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert got == pytest.approx(atteso, rel=1e-9), chiave
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True
    assert demo_calcoli()["van"] == bc["van"]


def test_demo_calcoli_fisica_economia():
    bc = mh811_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(14626.66851851852)
    assert bc["c_alt_eur_anno"] == pytest.approx(12647.55134640523)
    assert bc["risparmio_eur_anno"] == pytest.approx(1979.1171721132905)
    assert bc["co2_base_t_anno"] == pytest.approx(19.573003703703705)
    assert bc["co2_alt_t_anno"] == pytest.approx(10.967857581699345)
    assert bc["co2_evitata_t_anno"] == pytest.approx(8.60514612200436)
    assert bc["q_risc_kwh_anno"] == pytest.approx(50000.0)
    assert bc["q_raff_kwh_anno"] == pytest.approx(27500.0)
    assert bc["q_vent_rec_kwh_anno"] == pytest.approx(10500.0)
    assert bc["q_risc_net_kwh_anno"] == pytest.approx(39500.0)


def test_demo_flussi_e_cumulato():
    bc = mh811_demo_calcoli()
    assert bc["flussi"][0] == -15000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(1979.1171721132905) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -15000
    assert righe.iloc[7]["Cumulato (EUR)"] == pytest.approx(-1146.1797952069664)
    assert righe.iloc[8]["Cumulato (EUR)"] == pytest.approx(832.9373769063241)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(14686.757581699358)


def test_demo_tabella_righe():
    bc = mh811_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Riscaldamento (kWh_th/anno)"] == pytest.approx(50000.0)
    assert mappa["Raffrescamento (kWh_th/anno)"] == pytest.approx(27500.0)
    assert mappa["Recupero calore ventilazione (kWh_th/anno)"] == pytest.approx(10500.0)
    assert mappa["Riscaldamento netto (kWh_th/anno)"] == pytest.approx(39500.0)
    assert mappa["ACS (kWh_th/anno)"] == pytest.approx(2686.016666666667)
    assert mappa["Pasti all'anno"] == pytest.approx(13200.0)
    assert mappa["Calore mensa base (kWh_th/anno)"] == pytest.approx(10560.0)
    assert mappa["Elettricita' mensa alt (kWh_e/anno)"] == pytest.approx(6600.0)
    assert mappa["Elettricita' lavanderia base (kWh_e/anno)"] == pytest.approx(6600.0)
    assert mappa["Elettricita' lavanderia alt (kWh_e/anno)"] == pytest.approx(3630.0)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(70273.35185185185)
    assert mappa["Elettricita' totale base (kWh_e/anno)"] == pytest.approx(15766.666666666666)
    assert mappa["Elettricita' totale alternativa (kWh_e/anno)"] == pytest.approx(31336.73594771242)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(14626.66851851852)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(12647.55134640523)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(1979.1171721132905)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(8.60514612200436)
    assert mappa["Payback (anni)"] == 8
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] == pytest.approx(71.83687528829414)


def test_demo_coerenza_interna():
    bc = mh811_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["q_risc_kwh_anno"] == pytest.approx(
        bc["superficie_m2"] * bc["q_risc_per_m2"])
    assert bc["q_raff_kwh_anno"] == pytest.approx(
        bc["superficie_m2"] * bc["q_raff_per_m2"])
    assert bc["q_vent_rec_kwh_anno"] == pytest.approx(
        bc["eta_rec"] * bc["f_vent"] * bc["q_risc_kwh_anno"])
    assert bc["q_risc_net_kwh_anno"] == pytest.approx(
        bc["q_risc_kwh_anno"] - bc["q_vent_rec_kwh_anno"])
    assert bc["q_acs_kwh_anno"] == pytest.approx(
        bc["litri_giorno"] * bc["giorni_anno"] * 4.186
        * bc["delta_t"] / 3600.0)
    assert bc["pasti_annui"] == pytest.approx(
        bc["pasti_giorno"] * bc["giorni_anno"])
    assert bc["q_mensa_th_base_kwh_anno"] == pytest.approx(
        bc["pasti_annui"] * bc["kwh_th_per_pasto"])
    assert bc["e_mensa_alt_kwh_anno"] == pytest.approx(
        bc["pasti_annui"] * bc["kwh_e_per_pasto"])
    assert bc["e_lav_base_kwh_anno"] == pytest.approx(
        bc["kg_giorno"] * bc["giorni_anno"] * bc["e_per_kg"])
    assert bc["e_lav_alt_kwh_anno"] == pytest.approx(
        bc["e_lav_base_kwh_anno"] * 0.55)
    assert bc["gas_base_kwh_anno"] == pytest.approx(
        (bc["q_risc_kwh_anno"] + bc["q_acs_kwh_anno"]
         + bc["q_mensa_th_base_kwh_anno"]) / 0.90)
    assert bc["e_chiller_kwh_anno"] == pytest.approx(
        bc["q_raff_kwh_anno"] / 3.0)
    assert bc["e_pdc_kwh_anno"] == pytest.approx(
        bc["q_risc_net_kwh_anno"] / 3.4 + bc["q_raff_kwh_anno"] / 3.2
        + bc["q_acs_kwh_anno"] / 3.0)
    assert bc["e_base_kwh_anno"] == pytest.approx(
        bc["e_chiller_kwh_anno"] + bc["e_lav_base_kwh_anno"])
    assert bc["e_alt_kwh_anno"] == pytest.approx(
        bc["e_pdc_kwh_anno"] + bc["e_mensa_alt_kwh_anno"]
        + bc["e_lav_alt_kwh_anno"])
    assert bc["co2_evitata_t_anno"] == pytest.approx(
        bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])
    assert bc["c_base_eur_anno"] == pytest.approx(
        bc["gas_base_kwh_anno"] / 1000.0 * bc["p_gas"]
        + bc["e_base_kwh_anno"] / 1000.0 * bc["p_el"]
        + bc["om_base"])
    assert bc["c_alt_eur_anno"] == pytest.approx(
        bc["e_alt_kwh_anno"] / 1000.0 * bc["p_el"]
        + bc["om_alt"])


def test_demo_contro_riconteggio_indipendente():
    sup, qri, qra = 500, 100, 55
    gg = 220
    ere, fve = 0.60, 0.35
    lit, dta = 300, 35
    pas, kth, kep = 60, 0.8, 0.5
    kgg, epk = 30, 1.0
    pg, pel = 100, 260
    omb, oma, cx = 3500, 4500, 15000
    wacc, vita = 5.0, 15
    qrisc = sup * qri
    qraff = sup * qra
    qven = ere * fve * qrisc
    qnet = qrisc - qven
    qacs = lit * gg * 4.186 * dta / 3600.0
    pann = pas * gg
    qmen = pann * kth
    emen = pann * kep
    elb = kgg * gg * epk
    ela = elb * 0.55
    gasb = (qrisc + qacs + qmen) / 0.90
    ech = qraff / 3.0
    epdc = qnet / 3.4 + qraff / 3.2 + qacs / 3.0
    eb = ech + elb
    ea = epdc + emen + ela
    cb = gasb / 1000.0 * pg + eb / 1000.0 * pel + omb
    ca = ea / 1000.0 * pel + oma
    risp = cb - ca
    co2b = (gasb * 0.20 + eb * 0.35) / 1000.0
    co2a = ea * 0.35 / 1000.0
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    be = ((ca - omb - eb / 1000.0 * pel) * 1000.0 / gasb)
    bc = mh811_demo_calcoli()
    assert bc["q_risc_kwh_anno"] == pytest.approx(qrisc)
    assert bc["q_raff_kwh_anno"] == pytest.approx(qraff)
    assert bc["q_vent_rec_kwh_anno"] == pytest.approx(qven)
    assert bc["q_risc_net_kwh_anno"] == pytest.approx(qnet)
    assert bc["q_acs_kwh_anno"] == pytest.approx(qacs)
    assert bc["pasti_annui"] == pytest.approx(pann)
    assert bc["q_mensa_th_base_kwh_anno"] == pytest.approx(qmen)
    assert bc["e_mensa_alt_kwh_anno"] == pytest.approx(emen)
    assert bc["e_lav_base_kwh_anno"] == pytest.approx(elb)
    assert bc["e_lav_alt_kwh_anno"] == pytest.approx(ela)
    assert bc["gas_base_kwh_anno"] == pytest.approx(gasb)
    assert bc["e_chiller_kwh_anno"] == pytest.approx(ech)
    assert bc["e_pdc_kwh_anno"] == pytest.approx(epdc)
    assert bc["e_base_kwh_anno"] == pytest.approx(eb)
    assert bc["e_alt_kwh_anno"] == pytest.approx(ea)
    assert bc["c_base_eur_anno"] == pytest.approx(cb)
    assert bc["c_alt_eur_anno"] == pytest.approx(ca)
    assert bc["risparmio_eur_anno"] == pytest.approx(risp)
    assert bc["co2_base_t_anno"] == pytest.approx(co2b)
    assert bc["co2_alt_t_anno"] == pytest.approx(co2a)
    assert bc["co2_evitata_t_anno"] == pytest.approx(co2)
    assert bc["van"] == pytest.approx(van)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(be)


def test_demo_verdetto_coerente_con_risparmio_e_van():
    bc = mh811_demo_calcoli()
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] > 0.0
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["tir"] is not None and bc["tir"] > bc["wacc_pct"]
    assert bc["payback"] == 8


# ---------------------------------------------------------------- varianti
def test_variante_senza_recupero_non_convinte():
    # eta_rec zero: il recupero e' nullo, il caso
    # NON regge piu' (il recupero e' decisivo).
    bc0 = _variante(eta_rec=0)
    assert bc0["q_vent_rec_kwh_anno"] == 0.0
    assert bc0["q_risc_net_kwh_anno"] == pytest.approx(50000.0)
    assert bc0["risparmio_eur_anno"] == pytest.approx(1176.1759956427031)
    assert bc0["van"] == pytest.approx(-2791.6953725121575)
    assert bc0["breakeven_gas_eur_mwh"] == pytest.approx(83.26284481033036)
    assert bc0["payback"] == 13
    assert bc0["verdetto"] == "NON_CONVIENTE"


def test_variante_recupero_massimo():
    # eta_rec 1,00 e f_vent 1,00: recupero pari
    # all'intero riscaldamento, netto zero.
    bc = _variante(eta_rec=1, f_vent=1)
    assert bc["q_vent_rec_kwh_anno"] == pytest.approx(50000.0)
    assert bc["q_risc_net_kwh_anno"] == pytest.approx(0.0, abs=1e-12)
    assert bc["risparmio_eur_anno"] == pytest.approx(4999.705407407408)
    assert bc["van"] == pytest.approx(36895.23242053126)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(28.853466133967345)
    assert bc["payback"] == 4
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_risparmio_nonpositivo_non_calcolabile():
    # Prezzo gas zero e O&M alt alto: risparmio
    # negativo negli helper (calcolabile, non
    # solleva), verdetto NON_CALCOLABILE; stessa
    # guard della UI.
    for kw in ({"p_gas": 0}, {"om_alt": 10000}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] <= 0.0
        assert bc["verdetto"] == "NON_CALCOLABILE"
        assert bc["flussi"]
    bc = _variante(p_gas=0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-5048.218013071896)
    assert bc["van"] == pytest.approx(-67398.77667786976)
    assert bc["payback"] is None
    bc2 = _variante(om_alt=10000)
    assert bc2["risparmio_eur_anno"] == pytest.approx(-3520.8828278867077)
    assert bc2["breakeven_gas_eur_mwh"] == pytest.approx(150.10267384583173)


def test_variante_prezzo_el_zero_helper_convinte():
    # Negli helper p_el = 0 e' ammesso e resta
    # CONVIENTE; in UI e' guard degenere:
    # divergenza documentata.
    bc = _variante(p_el=0)
    assert bc["risparmio_eur_anno"] == pytest.approx(6027.335185185186)
    assert bc["van"] == pytest.approx(47561.67810371611)
    assert bc["payback"] == 3
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_superficie_zero_helper_non_calcolabile():
    # Negli helper S = 0 resta calcolabile ma il
    # risparmio e' negativo (la mensa a gas
    # resta, ma non basta): verdetto
    # NON_CALCOLABILE con breakeven 147,89; in
    # UI e' guard degenere (S <= 0): qui NON
    # c'e' divergenza di verdetto, solo guard
    # prima.
    bc = _variante(superficie_m2=0)
    assert bc["q_risc_kwh_anno"] == 0.0
    assert bc["q_raff_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(-704.808481481482)
    assert bc["van"] == pytest.approx(-22315.67102018712)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(147.88818022021715)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_capex_conviente_e_zero():
    bc = _variante(capex=30000)
    assert bc["risparmio_eur_anno"] == pytest.approx(1979.1171721132905)
    assert bc["van"] == pytest.approx(-9457.440535973046)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"
    bc0 = _variante(capex=0)
    assert bc0["flussi"][0] == 0
    assert bc0["payback"] == 0
    assert bc0["tir"] is None
    assert bc0["van"] == pytest.approx(20542.559464026956, rel=1e-6)
    assert bc0["verdetto"] == "CONVIENTE"


def test_variante_capex_marginale():
    # CAPEX 22.000: VAN negativa entro il 10 %
    # del CAPEX (2.200 EUR), quindi MARGINALE.
    bc = _variante(capex=22000)
    assert bc["van"] == pytest.approx(-1457.4405359730445)
    assert bc["verdetto"] == "MARGINALE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(14686.757581699358)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(282.21819685666196)
    assert bc2["payback"] == 8
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_el_alto_non_calcolabile():
    # Elettricita' cara uccide il caso prima
    # della finanza (l'alternativa consuma piu'
    # elettricita' della base): risparmio
    # negativo, quindi NON_CALCOLABILE.
    bc = _variante(p_el=400)
    assert bc["risparmio_eur_anno"] == pytest.approx(-200.6925272331173)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(102.85588380153278)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_monotonia_prezzo_gas_crescente():
    base = mh811_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas=101)["risparmio_eur_anno"]
    basso = _variante(p_gas=99)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(70.27335185185185, abs=1e-2)
    assert base - basso == pytest.approx(70.27335185185185, abs=1e-2)


def test_monotonia_recupero_crescente():
    assert _variante(eta_rec=0.30)["risparmio_eur_anno"] < \
        mh811_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(eta_rec=0.90)["risparmio_eur_anno"] > \
        mh811_demo_calcoli()["risparmio_eur_anno"]


def test_demo_deterministica_due_chiamate():
    a = mh811_demo_calcoli()
    b = mh811_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh811_demo().keys()) == {
        "superficie_m2", "giorni_anno",
        "q_risc_per_m2", "q_raff_per_m2",
        "eta_rec", "f_vent",
        "litri_giorno", "delta_t",
        "pasti_giorno", "kwh_th_per_pasto",
        "kwh_e_per_pasto",
        "kg_giorno", "e_per_kg",
        "p_gas", "p_el",
        "om_base", "om_alt",
        "capex", "wacc_pct", "vita_anni",
        "tolleranza_pct"}


# ---------------------------------------------------------------- degenere
def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"superficie_m2": -10},
               {"q_risc_per_m2": -10},
               {"q_raff_per_m2": -10},
               {"giorni_anno": 0},
               {"giorni_anno": 2.5},
               {"eta_rec": -0.1}, {"eta_rec": 1.01},
               {"f_vent": -0.1}, {"f_vent": 1.01},
               {"litri_giorno": -1},
               {"delta_t": 0}, {"delta_t": -5},
               {"pasti_giorno": -1},
               {"kwh_th_per_pasto": -0.1},
               {"kwh_e_per_pasto": -0.1},
               {"kg_giorno": -1},
               {"e_per_kg": -0.1},
               {"p_gas": -1},
               {"p_el": -1},
               {"om_base": -100},
               {"om_alt": -100},
               {"capex": -1},
               {"wacc_pct": -1}, {"wacc_pct": 60},
               {"vita_anni": 0}, {"vita_anni": 2.5},
               {"tolleranza_pct": -1},
               {"tolleranza_pct": 100.1}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh811_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"superficie_m2": "500"},
               {"superficie_m2": float("nan")},
               {"p_gas": float("inf")},
               {"capex": True},
               {"q_risc_per_m2": "100"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh811_valida(**d)["valido"] is False


def test_degenere_superficie_zero_e_gas_zero():
    # Superficie 0: calcolabile negli helper ma
    # risparmio negativo, quindi NON_CALCOLABILE
    # (non solleva); gas 0: stessa guard.
    for kw in ({"superficie_m2": 0}, {"p_gas": 0}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] <= 0.0
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    for kw in ({"p_gas": 0}, {"om_alt": 10000}):
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
    be = mh811_demo_calcoli()["breakeven_gas_eur_mwh"]
    bc = _variante(p_gas=be)
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["verdetto"] != "CONVIENTE"
    bc2 = _variante(p_gas=be + 1)
    assert bc2["risparmio_eur_anno"] == pytest.approx(70.27335185185257, abs=1e-2)
    # Risparmio positivo ma piccolo: VAN negativa oltre
    # la tolleranza, quindi NON_CONVIENTE (non CONVIENTE).
    assert bc2["verdetto"] == "NON_CONVIENTE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh811_demo_calcoli()
    testo = mh811_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_gas_eur_mwh" in testo
    assert "co2_evitata_t_anno" in testo
    assert "q_vent_rec_kwh_anno" in testo
    assert "q_risc_net_kwh_anno" in testo
    assert "e_mensa_alt_kwh_anno" in testo
    assert "q_mensa_th_base_kwh_anno" in testo
    assert "e_lav_alt_kwh_anno" in testo
    assert "e_pdc_kwh_anno" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh811_demo_calcoli()
    testo = mh811_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"q_vent_rec_kwh_anno;{bc['q_vent_rec_kwh_anno']}" in testo
    assert f"gas_base_kwh_anno;{bc['gas_base_kwh_anno']}" in testo
    assert f"q_risc_kwh_anno;{bc['q_risc_kwh_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh811_demo_calcoli()
    testo = mh811_csv(bc, _demo_kwargs())
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
    return ["mh" + "81" + "0", "st" + "81" + "0",
            "tab" + "81" + "0", "w" + "81" + "1",
            "mh" + "80" + "9", "tab" + "80" + "9"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w812_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w812_ui.py"))
    ast.parse(src)
    assert src.startswith("# W812")
    assert "with tab811:" in src


def test_ui_apre_scheda_attesa_una_volta():
    """Il frammento UI apre la scheda attesa, una sola volta."""
    src = _leggi("w812_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert m.group(1) == "811"
    assert src.count("with tab811:") == 1


def test_ui_titolo_atteso():
    src = _leggi("w812_ui.py")
    titolo = ("Asilo nido: pompa di calore + recupero "
              "calore ventilazione aule + mensa e "
              "lavanderia efficienti batte caldaia "
              "a gas + chiller + mensa tradizionale?")
    assert src.count(titolo) == 2


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w812_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w812_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st811_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) >= 30
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w812_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 4
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_ui_guard_degenere_stretta():
    """La guard UI della scheda dichiara NON_CALCOLABILE
    anche per superficie <= 0, carichi <= 0, litri <= 0,
    pasti <= 0, kg <= 0, prezzi <= 0 e CAPEX <= 0
    (piu' stretta degli helper, che ammettono lo
    zero)."""
    src = _leggi("w812_ui.py")
    assert "float(_sup811) <= 0.0" in src
    assert "float(_qri811) <= 0.0" in src
    assert "float(_qra811) <= 0.0" in src
    assert "float(_lit811) <= 0.0" in src
    assert "float(_pas811) <= 0.0" in src
    assert "float(_kgg811) <= 0.0" in src
    assert "float(_pg811) <= 0.0" in src
    assert "float(_pel811) <= 0.0" in src
    assert "float(_cx811) <= 0.0" in src
    assert "int(_vita811) <= 0" in src
    assert "Verdetto: NON_CALCOLABILE" in src


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w812_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def811[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w812_ui.py")
        usate = set(re.findall(r'_def811\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 21
        assert usate <= set(mh811_demo().keys())
