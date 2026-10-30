"""Test nuova scheda "Officina meccanica /
autoriparazione: pompa di calore aria-aria +
compressore VSD con recupero calore + LED
battono caldaia a gas + compressore standard
+ illuminazione tradizionale?" (titolo
completo nel frammento UI). Contenuto pronto
da scrivere in repo come test della scheda
officina.

Business case deterministico di un'officina
meccanica guidata dai M2 DI SUPERFICIE DEL
CAPANNONE e dalle ORE ALL'ANNO: i m2 guidano
il riscaldamento, la portata per le ore annue
guida l'aria compressa, i consumi specifici
guidano l'elettricita' dei compressori, la
quota di calore recuperato dal VSD scalda il
capannone e riduce il calore residuo della
pompa di calore, la potenza di illuminazione
per le ore annue guida l'illuminazione.
Riscaldamento = S x q_risc; aria annua =
portata x ore; compressore base = aria x
c_base e VSD = aria x c_vsd (kWh/Nm3);
calore recuperato = f_rec x E_comp_alt;
calore residuo pompa di calore = max(Q_risc -
Q_rec, 0); pompa di calore = calore residuo /
3,2; illuminazione base = ore x potenza e LED
= base x f_led; gas baseline = riscaldamento
/ 0,90 (eta_caldaia letterale, senza recupero
e senza pompa di calore); E_base =
compressore base + illuminazione base;
E_alt = pompa di calore + compressore VSD +
illuminazione LED; C_base = gas_base / 1000 x
p_gas + E_base / 1000 x p_el + O&M_base;
C_alt = E_alt / 1000 x p_el + O&M_alt (niente
gas: l'alternativa non ha caldaia); risparmio
= C_base - C_alt; CO2 evitata = (gas_base x
0,20 + E_base x 0,35 - E_alt x 0,35) / 1000
(fattori letterali); flussi [-CAPEX, risparmio
x vita]; VAN, TIR, payback (primo anno con
cumulato >= 0); breakeven gas = (C_alt -
O&M_base - E_base / 1000 x p_el) x 1000 /
gas_base EUR/MWh, None se gas_base <= 0 o
numeratore < 0, SOGLIA MINIMA quando esiste.
Verdetto: NON_CALCOLABILE se input degenere
(superficie <= 0, q <= 0, portata <= 0, ore
<= 0, consumi specifici <= 0, quota di recupero
o fattore LED fuori [0, 1], potenza <= 0,
prezzi <= 0, CAPEX <= 0, vita <= 0) o se
risparmio <= 0 (guard degenere: UI salta KPI,
grafico, tabella e CSV); altrimenti CONVIENTE
se VAN > 0, MARGINALE se VAN negativa entro
tolleranza % del CAPEX, NON_CONVIENTE se VAN
negativa oltre la tolleranza. Differenze
UI-vs-helper documentate: S = 0 e' CONVIENTE
negli helper (risparmio 4.616,00 EUR/anno, VAN
2.912,50 EUR, TIR 5,94 %, payback 10,
breakeven None perche' gas_base = 0) ma
bloccato dalla guard UI (NON_CALCOLABILE):
qui c'e' DIVERGENZA di verdetto, perche'
compressore e illuminazione da soli
risparmiano anche senza riscaldamento;
portata = 0 e' CONVIENTE negli helper
(risparmio 5.683,78 EUR/anno, VAN 13.995,67
EUR, payback 8, breakeven 41,87 EUR/MWh) ma
bloccata dalla guard UI: divergenza analoga;
CAPEX = 0 e' CONVIENTE negli helper (VAN
85.510,51 EUR, TIR None, payback 0) ma
bloccato dalla guard UI; prezzi = 0 sono
ammessi negli helper ma bloccati dalla guard
UI (p_el = 0 resta CONVIENTE negli helper,
risparmio 8.777,78 EUR/anno, VAN 46.110,33
EUR; p_gas = 0 da' invece risparmio NEGATIVO
negli helper, -1.539,50 EUR/anno, verdetto
NON_CALCOLABILE: per gas zero QUI NON c'e'
divergenza di verdetto helper-vs-UI, solo
guard prima).
Distinzione esplicita: distinto dalla chiesa
(m2 di navata, ore di uso a settimana, quota
panche con mantenimento antigelo: qui niente
panche, niente zona occupata a comfort,
niente mantenimento antigelo), dall'asilo
(giorni di apertura, mensa con pasti al
giorno, lavanderia con kg al giorno: qui
niente mensa, niente pasti, niente
lavanderia), dall'albergo (pernottamenti e
camere: qui nessun pernottamento, nessuna
camera): qui driver M2 + PORTATA + ORE +
RECUPERO + ILLUMINAZIONE, con capannone
produttivo e aria compressa di processo.

Demo (officina): superficie 800 m2, 110
kWh_th/m2 di riscaldamento (88.000
kWh_th/anno), portata 120 Nm3/h per 2.000 ore
all'anno (240.000 Nm3/anno), consumo specifico
base 0,11 kWh/Nm3 (26.400 kWh_e/anno) e VSD
0,085 kWh/Nm3 (20.400 kWh_e/anno), quota di
recupero 0,60 (12.240 kWh_th/anno, calore
residuo pompa di calore 75.760 kWh_th/anno),
illuminazione di base 12 kW (24.000
kWh_e/anno) con fattore LED 0,35 (8.400
kWh_e/anno), gas 100, el 260 EUR/MWh, O&M base
2.500, alt 3.500, CAPEX 45.000, WACC 5 %, vita
15, tolleranza 10 % del CAPEX. Valori calcolati
eseguendo mh813_demo_calcoli():
Q_risc 88.000, V_anno 240.000, E_comp_base
26.400, E_comp_alt 20.400, Q_rec 12.240,
Q_pdc_th 75.760, E_pdc 23.675, E_ill_base
24.000, E_ill_alt 8.400, gas_base
97.777,77777777778, E_base 50.400, E_alt
52.475, C_base 25.381,77777777778, C_alt
17.143,5, risparmio 8.238,277777777781,
CO2_base 37,195555555555565, CO2_alt
18,36625, CO2_evitata 18,82930555555556, VAN
40.510,50615687568, TIR 16,440675801827126 %,
payback 6, breakeven gas 15,744886363636363
EUR/MWh (soglia minima), verdetto CONVIENTE.
"""

import ast
import inspect
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w814_helpers import (
    demo_calcoli,
    mh813_breakeven_gas,
    mh813_c_alt,
    mh813_c_base,
    mh813_calcola,
    mh813_co2_alt,
    mh813_co2_base,
    mh813_co2_evitata,
    mh813_csv,
    mh813_demo,
    mh813_demo_calcoli,
    mh813_e_alt,
    mh813_e_base,
    mh813_e_comp_alt,
    mh813_e_comp_base,
    mh813_e_ill_alt,
    mh813_e_ill_base,
    mh813_e_pdc,
    mh813_flussi,
    mh813_frazione,
    mh813_gas_base,
    mh813_int_pos,
    mh813_num,
    mh813_nneg,
    mh813_payback,
    mh813_pct_tolleranza,
    mh813_pos,
    mh813_pct_wacc,
    mh813_q_pdc_th,
    mh813_q_rec,
    mh813_q_risc,
    mh813_risparmio,
    mh813_tir,
    mh813_v_anno,
    mh813_valida,
    mh813_van,
    mh813_verdetto,
)

_DEMO = {
    "q_risc_kwh_anno": 88000.0,
    "v_anno_nm3": 240000.0,
    "e_comp_base_kwh_anno": 26400.0,
    "e_comp_alt_kwh_anno": 20400.0,
    "q_rec_kwh_anno": 12240.0,
    "q_pdc_th_kwh_anno": 75760.0,
    "e_pdc_kwh_anno": 23675.0,
    "e_ill_base_kwh_anno": 24000.0,
    "e_ill_alt_kwh_anno": 8400.0,
    "gas_base_kwh_anno": 97777.77777777778,
    "e_base_kwh_anno": 50400.0,
    "e_alt_kwh_anno": 52475.0,
    "c_base_eur_anno": 25381.77777777778,
    "c_alt_eur_anno": 17143.5,
    "risparmio_eur_anno": 8238.277777777781,
    "co2_base_t_anno": 37.195555555555565,
    "co2_alt_t_anno": 18.36625,
    "co2_evitata_t_anno": 18.82930555555556,
    "van": 40510.50615687568,
    "tir": 16.440675801827126,
    "breakeven_gas_eur_mwh": 15.744886363636363,
}


def _demo_kwargs():
    return dict(mh813_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh813_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh813_num(3, "x") == 3.0
    assert mh813_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh813_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh813_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh813_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh813_pos(0, "x")
    with pytest.raises(ValueError):
        mh813_pos(-1, "x")
    assert mh813_pos(0.5, "x") == 0.5


def test_frazione_limiti():
    assert mh813_frazione(0, "x") == 0.0
    assert mh813_frazione(1, "x") == 1.0
    assert mh813_frazione(0.60, "x") == 0.60
    assert mh813_frazione(0.35, "x") == 0.35
    with pytest.raises(ValueError):
        mh813_frazione(-0.01, "x")
    with pytest.raises(ValueError):
        mh813_frazione(1.01, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh813_int_pos(5.0, "x") == 5
    assert mh813_int_pos(2000.0, "x") == 2000
    with pytest.raises(ValueError):
        mh813_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh813_int_pos(0, "x")


def test_pct_wacc_limiti():
    assert mh813_pct_wacc(0, "x") == 0.0
    assert mh813_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh813_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh813_pct_tolleranza(0, "x") == 0.0
    assert mh813_pct_tolleranza(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh813_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh813_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_q_risc_v_anno_comp_rec_pdc():
    assert mh813_q_risc(800, 110) == 88000.0
    assert mh813_q_risc(0, 110) == 0.0
    with pytest.raises(ValueError):
        mh813_q_risc(-1, 110)
    assert mh813_v_anno(120, 2000) == 240000.0
    assert mh813_v_anno(120, 2000.0) == 240000.0
    with pytest.raises(ValueError):
        mh813_v_anno(120, 0)
    with pytest.raises(ValueError):
        mh813_v_anno(120, 2000.5)
    with pytest.raises(ValueError):
        mh813_v_anno(-1, 2000)
    assert mh813_e_comp_base(240000.0, 0.11) == pytest.approx(26400.0)
    assert mh813_e_comp_base(240000.0, 0) == 0.0
    with pytest.raises(ValueError):
        mh813_e_comp_base(240000.0, -0.01)
    assert mh813_e_comp_alt(240000.0, 0.085) == pytest.approx(20400.0)
    assert mh813_e_comp_alt(240000.0, 0) == 0.0
    assert mh813_q_rec(20400.0, 0.60) == pytest.approx(12240.0)
    assert mh813_q_rec(20400.0, 0) == 0.0
    assert mh813_q_rec(20400.0, 1) == pytest.approx(20400.0)
    with pytest.raises(ValueError):
        mh813_q_rec(20400.0, 1.01)
    assert mh813_q_pdc_th(88000.0, 12240.0) == pytest.approx(75760.0)
    assert mh813_q_pdc_th(88000.0, 0.0) == pytest.approx(88000.0)
    assert mh813_q_pdc_th(1000.0, 1500.0) == 0.0
    assert mh813_q_pdc_th(0.0, 0.0) == 0.0
    with pytest.raises(ValueError):
        mh813_q_pdc_th(-1, 12240.0)


def test_pdc_illuminazione_gas_totali():
    assert mh813_e_pdc(75760.0) == pytest.approx(23675.0)
    assert mh813_e_pdc(0.0) == 0.0
    assert mh813_e_ill_base(2000, 12) == 24000.0
    assert mh813_e_ill_base(2000, 0) == 0.0
    with pytest.raises(ValueError):
        mh813_e_ill_base(2000, -1)
    with pytest.raises(ValueError):
        mh813_e_ill_base(0, 12)
    assert mh813_e_ill_alt(24000.0, 0.35) == pytest.approx(8400.0)
    assert mh813_e_ill_alt(24000.0, 0) == 0.0
    assert mh813_e_ill_alt(24000.0, 1) == pytest.approx(24000.0)
    with pytest.raises(ValueError):
        mh813_e_ill_alt(24000.0, 1.01)
    assert mh813_gas_base(88000.0) == pytest.approx(97777.77777777778)
    assert mh813_gas_base(0) == 0.0
    with pytest.raises(ValueError):
        mh813_gas_base(-1)
    assert mh813_e_base(26400.0, 24000.0) == pytest.approx(50400.0)
    assert mh813_e_alt(23675.0, 20400.0, 8400.0) == pytest.approx(52475.0)


def test_c_base_c_alt_scomposizione():
    assert mh813_c_base(97777.77777777778, 100, 50400.0, 260,
                        2500) == pytest.approx(25381.77777777778)
    assert mh813_c_base(97777.77777777778, 0, 50400.0, 260,
                        2500) == pytest.approx(15604.0)
    assert mh813_c_alt(52475.0, 260,
                       3500) == pytest.approx(17143.5)
    with pytest.raises(ValueError):
        mh813_c_base(97777.78, 100, 50400.0, 260, -1)
    with pytest.raises(ValueError):
        mh813_c_alt(52475.0, 260, -1)


def test_risparmio_segno():
    assert mh813_risparmio(25381.77777777778, 17143.5) == pytest.approx(8238.277777777781)
    assert mh813_risparmio(17143.5, 17143.5) == pytest.approx(0.0, abs=1e-9)


def test_co2_base_alt_evitata():
    assert mh813_co2_base(97777.77777777778, 50400.0) == pytest.approx(37.195555555555565)
    assert mh813_co2_alt(52475.0) == pytest.approx(18.36625)
    assert mh813_co2_evitata(97777.77777777778, 50400.0,
                             52475.0) == pytest.approx(18.82930555555556)
    assert mh813_co2_base(0, 0) == 0.0
    assert mh813_co2_alt(0) == 0.0
    with pytest.raises(ValueError):
        mh813_co2_base(97777.78, -1)
    with pytest.raises(ValueError):
        mh813_co2_alt(-1)


def test_breakeven_demo_e_varianti():
    assert mh813_demo_calcoli()["breakeven_gas_eur_mwh"] == pytest.approx(15.744886363636363)
    assert mh813_breakeven_gas(17143.5,
                               2500, 50400.0, 260,
                               97777.77777777778) == pytest.approx(15.744886363636363)
    bc = _variante(om_alt=15000)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(133.3585227272727)
    assert _variante(superficie_m2=0)["breakeven_gas_eur_mwh"] is None
    assert mh813_breakeven_gas(17143.5,
                               2500, 50400.0, 260,
                               0) is None
    assert mh813_breakeven_gas(1000, 2500, 50400.0, 260,
                               97777.77777777778) is None
    with pytest.raises(ValueError):
        mh813_breakeven_gas(17143.5, 2500, 50400.0, 260, -1)


def test_breakeven_verifica_pareggio():
    be = mh813_demo_calcoli()["breakeven_gas_eur_mwh"]
    assert be == pytest.approx(15.744886363636363)
    bc = _variante(p_gas=be)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert mh813_demo_calcoli()["gas_base_kwh_anno"] > 0.0


def test_breakeven_soglia_minima():
    bc_alto = _variante(p_gas=16.744886363636363)
    bc_basso = _variante(p_gas=14.0)
    assert bc_alto["c_alt_eur_anno"] < bc_alto["c_base_eur_anno"]
    assert bc_basso["c_alt_eur_anno"] > bc_basso["c_base_eur_anno"]
    assert bc_alto["risparmio_eur_anno"] > 0.0
    assert bc_alto["verdetto"] == "NON_CONVIENTE"
    assert bc_basso["verdetto"] == "NON_CALCOLABILE"


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh813_flussi(45000, 8238.277777777781, 15)
    assert len(fl) == 16
    assert fl[0] == -45000
    assert all(f == 8238.277777777781 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh813_demo_calcoli()
    assert bc["van"] == pytest.approx(40510.50615687568)
    assert mh813_van([-45000] + [8238.277777777781] * 15,
                     0) == pytest.approx(78574.16666666672)
    assert mh813_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh813_demo_calcoli()
    assert bc["tir"] == pytest.approx(16.440675801827126)
    assert mh813_tir([-45000] + [8238.277777777781] * 15) == \
        pytest.approx(0.16440675801827126)
    tir = mh813_tir([-45000] + [8238.277777777781] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-45000] + [8238.277777777781] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh813_payback([-45000] + [8238.277777777781] * 15) == 6
    assert mh813_payback([-45000] + [-1000.0] * 15) is None
    assert mh813_payback([0] + [8238.277777777781] * 15) == 0
    assert mh813_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh813_verdetto(8238.277777777781, 40510.50615687568, 45000,
                          10.0) == "CONVIENTE"
    assert mh813_verdetto(8238.277777777781, -1500.0, 45000,
                          10.0) == "MARGINALE"
    assert mh813_verdetto(8238.277777777781, -4500.0, 45000, 10.0) == "MARGINALE"
    assert mh813_verdetto(8238.277777777781, -4500.01, 45000, 10.0) == "NON_CONVIENTE"
    assert mh813_verdetto(8238.277777777781, 0.0, 45000, 10.0) == "MARGINALE"
    assert mh813_verdetto(0.0, 40510.51, 45000,
                          10.0) == "NON_CALCOLABILE"
    assert mh813_verdetto(-1539.5, -60979.48, 45000,
                          10.0) == "NON_CALCOLABILE"
    assert mh813_verdetto(None, 40510.51, 45000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh813_verdetto(float("nan"), 40510.51, 45000, 10.0)
    with pytest.raises(ValueError):
        mh813_verdetto(8238.277777777781, 40510.51, -1, 10.0)
    with pytest.raises(ValueError):
        mh813_verdetto(8238.277777777781, 40510.51, 45000, 100.1)


def test_valida_demo_ok():
    v = mh813_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("superficie_m2", "800"),
                       ("superficie_m2", float("nan")),
                       ("superficie_m2", float("inf")),
                       ("superficie_m2", True),
                       ("p_gas", None),
                       ("q_risc_per_m2", "110")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh813_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("superficie_m2", -10),
                          ("q_risc_per_m2", -10),
                          ("portata_nm3h", -10),
                          ("ore_anno", 0),
                          ("ore_anno", 2.5),
                          ("c_base_kwh_nm3", -0.01),
                          ("c_vsd_kwh_nm3", -0.01),
                          ("f_rec", -0.1),
                          ("f_rec", 1.01),
                          ("p_ill_base_kw", -1),
                          ("f_led", -0.1),
                          ("f_led", 1.01),
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
        assert mh813_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"superficie_m2": 0,
              "q_risc_per_m2": 0,
              "portata_nm3h": 0,
              "c_base_kwh_nm3": 0,
              "c_vsd_kwh_nm3": 0,
              "f_rec": 0,
              "p_ill_base_kw": 0,
              "f_led": 0,
              "p_gas": 0,
              "p_el": 0,
              "om_base": 0, "om_alt": 0,
              "capex": 0, "wacc_pct": 0,
              "tolleranza_pct": 0})
    assert mh813_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["f_rec"] = 1
    d["f_led"] = 1
    assert mh813_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh813_demo()
    assert d["superficie_m2"] == 800
    assert d["q_risc_per_m2"] == 110
    assert d["portata_nm3h"] == 120
    assert d["ore_anno"] == 2000
    assert d["c_base_kwh_nm3"] == 0.11
    assert d["c_vsd_kwh_nm3"] == 0.085
    assert d["f_rec"] == 0.60
    assert d["p_ill_base_kw"] == 12
    assert d["f_led"] == 0.35
    assert d["p_gas"] == 100
    assert d["p_el"] == 260
    assert d["om_base"] == 2500
    assert d["om_alt"] == 3500
    assert d["capex"] == 45000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    bc = mh813_demo_calcoli()
    for chiave, atteso in _DEMO.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert got == pytest.approx(atteso, rel=1e-9), chiave
    assert bc["payback"] == 6
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True
    assert demo_calcoli()["van"] == bc["van"]


def test_demo_calcoli_fisica_economia():
    bc = mh813_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(25381.77777777778)
    assert bc["c_alt_eur_anno"] == pytest.approx(17143.5)
    assert bc["risparmio_eur_anno"] == pytest.approx(8238.277777777781)
    assert bc["co2_base_t_anno"] == pytest.approx(37.195555555555565)
    assert bc["co2_alt_t_anno"] == pytest.approx(18.36625)
    assert bc["co2_evitata_t_anno"] == pytest.approx(18.82930555555556)
    assert bc["q_risc_kwh_anno"] == pytest.approx(88000.0)
    assert bc["v_anno_nm3"] == pytest.approx(240000.0)
    assert bc["e_comp_base_kwh_anno"] == pytest.approx(26400.0)
    assert bc["e_comp_alt_kwh_anno"] == pytest.approx(20400.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(12240.0)
    assert bc["q_pdc_th_kwh_anno"] == pytest.approx(75760.0)
    assert bc["e_pdc_kwh_anno"] == pytest.approx(23675.0)


def test_demo_flussi_e_cumulato():
    bc = mh813_demo_calcoli()
    assert bc["flussi"][0] == -45000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(8238.277777777781) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -45000
    assert righe.iloc[5]["Cumulato (EUR)"] == pytest.approx(-3808.611111111095)
    assert righe.iloc[6]["Cumulato (EUR)"] == pytest.approx(4429.666666666686)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(78574.16666666672)


def test_demo_tabella_righe():
    bc = mh813_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Riscaldamento (kWh_th/anno)"] == pytest.approx(88000.0)
    assert mappa["Aria compressa annua (Nm3/anno)"] == pytest.approx(240000.0)
    assert mappa["Elettricita' compressore base (kWh_e/anno)"] == pytest.approx(26400.0)
    assert mappa["Elettricita' compressore VSD (kWh_e/anno)"] == pytest.approx(20400.0)
    assert mappa["Calore recuperato (kWh_th/anno)"] == pytest.approx(12240.0)
    assert mappa["Calore residuo pompa di calore (kWh_th/anno)"] == pytest.approx(75760.0)
    assert mappa["Elettricita' pompa di calore (kWh_e/anno)"] == pytest.approx(23675.0)
    assert mappa["Illuminazione base (kWh_e/anno)"] == pytest.approx(24000.0)
    assert mappa["Illuminazione LED (kWh_e/anno)"] == pytest.approx(8400.0)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(97777.77777777778)
    assert mappa["Elettricita' totale base (kWh_e/anno)"] == pytest.approx(50400.0)
    assert mappa["Elettricita' totale alternativa (kWh_e/anno)"] == pytest.approx(52475.0)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(25381.77777777778)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(17143.5)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(8238.277777777781)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(18.82930555555556)
    assert mappa["Payback (anni)"] == 6
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] == pytest.approx(15.744886363636363)


def test_demo_coerenza_interna():
    bc = mh813_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["q_risc_kwh_anno"] == pytest.approx(
        bc["superficie_m2"] * bc["q_risc_per_m2"])
    assert bc["v_anno_nm3"] == pytest.approx(
        bc["portata_nm3h"] * bc["ore_anno"])
    assert bc["e_comp_base_kwh_anno"] == pytest.approx(
        bc["v_anno_nm3"] * bc["c_base_kwh_nm3"])
    assert bc["e_comp_alt_kwh_anno"] == pytest.approx(
        bc["v_anno_nm3"] * bc["c_vsd_kwh_nm3"])
    assert bc["q_rec_kwh_anno"] == pytest.approx(
        bc["f_rec"] * bc["e_comp_alt_kwh_anno"])
    assert bc["q_pdc_th_kwh_anno"] == pytest.approx(
        max(bc["q_risc_kwh_anno"] - bc["q_rec_kwh_anno"], 0.0))
    assert bc["e_pdc_kwh_anno"] == pytest.approx(
        bc["q_pdc_th_kwh_anno"] / 3.2)
    assert bc["e_ill_base_kwh_anno"] == pytest.approx(
        bc["ore_anno"] * bc["p_ill_base_kw"])
    assert bc["e_ill_alt_kwh_anno"] == pytest.approx(
        bc["e_ill_base_kwh_anno"] * bc["f_led"])
    assert bc["gas_base_kwh_anno"] == pytest.approx(
        bc["q_risc_kwh_anno"] / 0.90)
    assert bc["e_base_kwh_anno"] == pytest.approx(
        bc["e_comp_base_kwh_anno"] + bc["e_ill_base_kwh_anno"])
    assert bc["e_alt_kwh_anno"] == pytest.approx(
        bc["e_pdc_kwh_anno"] + bc["e_comp_alt_kwh_anno"]
        + bc["e_ill_alt_kwh_anno"])
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
    sup, qri = 800, 110
    por, ore = 120, 2000
    cba, cvs, fre = 0.11, 0.085, 0.60
    pil, fle = 12, 0.35
    pg, pel = 100, 260
    omb, oma, cx = 2500, 3500, 45000
    wacc, vita = 5.0, 15
    qrisc = sup * qri
    vann = por * ore
    ecb = vann * cba
    eca = vann * cvs
    qrec = fre * eca
    qpdc = max(qrisc - qrec, 0.0)
    epdc = qpdc / 3.2
    eib = ore * pil
    eia = eib * fle
    gasb = qrisc / 0.90
    eb = ecb + eib
    ea = epdc + eca + eia
    cb = gasb / 1000.0 * pg + eb / 1000.0 * pel + omb
    ca = ea / 1000.0 * pel + oma
    risp = cb - ca
    co2b = (gasb * 0.20 + eb * 0.35) / 1000.0
    co2a = ea * 0.35 / 1000.0
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    be = ((ca - omb - eb / 1000.0 * pel) * 1000.0 / gasb)
    bc = mh813_demo_calcoli()
    assert bc["q_risc_kwh_anno"] == pytest.approx(qrisc)
    assert bc["v_anno_nm3"] == pytest.approx(vann)
    assert bc["e_comp_base_kwh_anno"] == pytest.approx(ecb)
    assert bc["e_comp_alt_kwh_anno"] == pytest.approx(eca)
    assert bc["q_rec_kwh_anno"] == pytest.approx(qrec)
    assert bc["q_pdc_th_kwh_anno"] == pytest.approx(qpdc)
    assert bc["e_pdc_kwh_anno"] == pytest.approx(epdc)
    assert bc["e_ill_base_kwh_anno"] == pytest.approx(eib)
    assert bc["e_ill_alt_kwh_anno"] == pytest.approx(eia)
    assert bc["gas_base_kwh_anno"] == pytest.approx(gasb)
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
    bc = mh813_demo_calcoli()
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] > 0.0
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["tir"] is not None and bc["tir"] > bc["wacc_pct"]
    assert bc["payback"] == 6


# ---------------------------------------------------------------- varianti
def test_variante_recupero_estremi():
    # Quota 0 = nessun recupero: il caso peggiora
    # ma resta CONVIENTE (VSD e LED bastano).
    bc0 = _variante(f_rec=0)
    assert bc0["q_rec_kwh_anno"] == 0.0
    assert bc0["q_pdc_th_kwh_anno"] == pytest.approx(88000.0)
    assert bc0["risparmio_eur_anno"] == pytest.approx(7243.777777777781)
    assert bc0["van"] == pytest.approx(30187.936237905076)
    assert bc0["breakeven_gas_eur_mwh"] == pytest.approx(25.91590909090909)
    assert bc0["payback"] == 7
    assert bc0["verdetto"] == "CONVIENTE"
    # Quota 1 = recupero pieno: il caso migliora.
    bc1 = _variante(f_rec=1)
    assert bc1["q_rec_kwh_anno"] == pytest.approx(20400.0)
    assert bc1["q_pdc_th_kwh_anno"] == pytest.approx(67600.0)
    assert bc1["risparmio_eur_anno"] == pytest.approx(8901.277777777781)
    assert bc1["van"] == pytest.approx(47392.21943618941)
    assert bc1["breakeven_gas_eur_mwh"] == pytest.approx(8.964204545454546)
    assert bc1["payback"] == 6
    assert bc1["verdetto"] == "CONVIENTE"


def test_variante_senza_vsd_resta_convinte():
    # Consumo VSD uguale al base: niente risparmio
    # dal compressore, ma pompa di calore, recupero
    # e LED bastano a restare CONVIENTE.
    bc = _variante(c_vsd_kwh_nm3=0.11)
    assert bc["e_comp_alt_kwh_anno"] == pytest.approx(26400.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(15840.0)
    assert bc["q_pdc_th_kwh_anno"] == pytest.approx(72160.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(6970.777777777781)
    assert bc["van"] == pytest.approx(27354.289593481775)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(28.707954545454545)
    assert bc["payback"] == 7
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_risparmio_nonpositivo_non_calcolabile():
    # Prezzo gas zero e O&M alt alto: risparmio
    # negativo negli helper (calcolabile, non
    # solleva), verdetto NON_CALCOLABILE; stessa
    # guard della UI.
    for kw in ({"p_gas": 0}, {"om_alt": 15000}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] <= 0.0
        assert bc["verdetto"] == "NON_CALCOLABILE"
        assert bc["flussi"]
    bc = _variante(p_gas=0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-1539.5)
    assert bc["van"] == pytest.approx(-60979.48354977902)
    assert bc["payback"] is None
    bc2 = _variante(om_alt=15000)
    assert bc2["risparmio_eur_anno"] == pytest.approx(-3261.722222222219)
    assert bc2["breakeven_gas_eur_mwh"] == pytest.approx(133.3585227272727)


def test_variante_prezzo_el_zero_helper_convinte():
    # Negli helper p_el = 0 e' ammesso e resta
    # CONVIENTE; in UI e' guard degenere:
    # divergenza documentata.
    bc = _variante(p_el=0)
    assert bc["risparmio_eur_anno"] == pytest.approx(8777.77777777778)
    assert bc["van"] == pytest.approx(46110.331668474086)
    assert bc["payback"] == 6
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_superficie_zero_helper_convinte_divergenza():
    # Negli helper S = 0 resta calcolabile e il
    # risparmio resta POSITIVO (compressore e
    # illuminazione da soli risparmiano): verdetto
    # CONVIENTE con breakeven None (gas_base
    # nullo); in UI e' guard degenere
    # (NON_CALCOLABILE): qui c'e' DIVERGENZA di
    # verdetto helper-vs-UI.
    bc = _variante(superficie_m2=0)
    assert bc["q_risc_kwh_anno"] == 0.0
    assert bc["q_pdc_th_kwh_anno"] == 0.0
    assert bc["gas_base_kwh_anno"] == 0.0
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["risparmio_eur_anno"] == pytest.approx(4616.0)
    assert bc["van"] == pytest.approx(2912.501504241605)
    assert bc["payback"] == 10
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_portata_zero_helper_convinte_divergenza():
    # Negli helper portata = 0 resta calcolabile e
    # il risparmio resta POSITIVO (riscaldamento
    # con pompa di calore e LED bastano): verdetto
    # CONVIENTE; in UI e' guard degenere
    # (NON_CALCOLABILE): divergenza analoga.
    bc = _variante(portata_nm3h=0)
    assert bc["v_anno_nm3"] == 0.0
    assert bc["e_comp_base_kwh_anno"] == 0.0
    assert bc["e_comp_alt_kwh_anno"] == 0.0
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["q_pdc_th_kwh_anno"] == pytest.approx(88000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(5683.777777777781)
    assert bc["van"] == pytest.approx(13995.669698343358)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(41.87045454545454)
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_marginale_non_convinte_e_zero():
    bc = _variante(capex=90000)
    assert bc["risparmio_eur_anno"] == pytest.approx(8238.277777777781)
    assert bc["van"] == pytest.approx(-4489.4938431243245)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"
    bc2 = _variante(capex=100000)
    assert bc2["van"] == pytest.approx(-14489.493843124324)
    assert bc2["payback"] == 13
    assert bc2["verdetto"] == "NON_CONVIENTE"
    bc0 = _variante(capex=0)
    assert bc0["flussi"][0] == 0
    assert bc0["payback"] == 0
    assert bc0["tir"] is None
    assert bc0["van"] == pytest.approx(85510.50615687568, rel=1e-6)
    assert bc0["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(78574.16666666672)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(18613.797272993714)
    assert bc2["payback"] == 6
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_el_alto_resta_convinte():
    # Elettricita' cara NON uccide questo caso
    # (base e alternativa consumano elettricita'
    # simile: 50.400 contro 52.475): risparmio e
    # VAN restano positivi.
    bc = _variante(p_el=400)
    assert bc["risparmio_eur_anno"] == pytest.approx(7947.777777777781)
    assert bc["van"] == pytest.approx(37495.215496784214)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(18.71590909090909)
    assert bc["payback"] == 6
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_om_alt_alto_non_convinte():
    # O&M alternativo 10.000: risparmio ancora
    # positivo ma VAN negativa oltre la
    # tolleranza, quindi NON_CONVIENTE.
    bc = _variante(om_alt=10000)
    assert bc["risparmio_eur_anno"] == pytest.approx(1738.277777777781)
    assert bc["van"] == pytest.approx(-26957.271091298164)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(82.22215909090909)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_monotonia_prezzo_gas_crescente():
    base = mh813_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas=101)["risparmio_eur_anno"]
    basso = _variante(p_gas=99)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(97.77777777777778, abs=1e-2)
    assert base - basso == pytest.approx(97.77777777777778, abs=1e-2)


def test_monotonia_recupero_crescente_risparmio_cresce():
    assert _variante(f_rec=0.80)["risparmio_eur_anno"] > \
        mh813_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(f_rec=0.40)["risparmio_eur_anno"] < \
        mh813_demo_calcoli()["risparmio_eur_anno"]


def test_demo_deterministica_due_chiamate():
    a = mh813_demo_calcoli()
    b = mh813_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh813_demo().keys()) == {
        "superficie_m2", "q_risc_per_m2",
        "portata_nm3h", "ore_anno",
        "c_base_kwh_nm3", "c_vsd_kwh_nm3",
        "f_rec",
        "p_ill_base_kw", "f_led",
        "p_gas", "p_el",
        "om_base", "om_alt",
        "capex", "wacc_pct", "vita_anni",
        "tolleranza_pct"}


# ---------------------------------------------------------------- degenere
def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"superficie_m2": -10},
               {"q_risc_per_m2": -10},
               {"portata_nm3h": -10},
               {"ore_anno": 0}, {"ore_anno": 2.5},
               {"c_base_kwh_nm3": -0.01},
               {"c_vsd_kwh_nm3": -0.01},
               {"f_rec": -0.1}, {"f_rec": 1.01},
               {"p_ill_base_kw": -1},
               {"f_led": -0.1}, {"f_led": 1.01},
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
        assert mh813_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"superficie_m2": "800"},
               {"superficie_m2": float("nan")},
               {"p_gas": float("inf")},
               {"capex": True},
               {"q_risc_per_m2": "110"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh813_valida(**d)["valido"] is False


def test_degenere_superficie_zero_o_gas_zero_non_sollevano():
    # Superficie 0: calcolabile negli helper,
    # risparmio positivo qui (divergenza
    # documentata); gas 0: risparmio negativo,
    # quindi NON_CALCOLABILE (non solleva).
    bc = _variante(superficie_m2=0)
    assert bc["valid"] is True
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(p_gas=0)
    assert bc2["valid"] is True
    assert bc2["risparmio_eur_anno"] <= 0.0
    assert bc2["verdetto"] == "NON_CALCOLABILE"


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    for kw in ({"p_gas": 0}, {"om_alt": 15000}):
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
    be = mh813_demo_calcoli()["breakeven_gas_eur_mwh"]
    bc = _variante(p_gas=be)
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["verdetto"] != "CONVIENTE"
    bc2 = _variante(p_gas=be + 1)
    assert bc2["risparmio_eur_anno"] == pytest.approx(97.77777777777778, abs=1e-2)
    # Risparmio positivo ma piccolo: VAN negativa oltre
    # la tolleranza, quindi NON_CONVIENTE (non CONVIENTE).
    assert bc2["verdetto"] == "NON_CONVIENTE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh813_demo_calcoli()
    testo = mh813_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_gas_eur_mwh" in testo
    assert "co2_evitata_t_anno" in testo
    assert "q_rec_kwh_anno" in testo
    assert "q_pdc_th_kwh_anno" in testo
    assert "e_comp_alt_kwh_anno" in testo
    assert "e_pdc_kwh_anno" in testo
    assert "v_anno_nm3" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh813_demo_calcoli()
    testo = mh813_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"q_rec_kwh_anno;{bc['q_rec_kwh_anno']}" in testo
    assert f"gas_base_kwh_anno;{bc['gas_base_kwh_anno']}" in testo
    assert f"q_risc_kwh_anno;{bc['q_risc_kwh_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh813_demo_calcoli()
    testo = mh813_csv(bc, _demo_kwargs())
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
    return ["mh" + "81" + "2", "st" + "81" + "2",
            "tab" + "81" + "2", "w" + "81" + "3",
            "mh" + "81" + "1", "tab" + "81" + "1"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w814_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w814_ui.py"))
    ast.parse(src)
    assert src.startswith("# W814")
    assert "with tab813:" in src


def test_ui_apre_scheda_attesa_una_volta():
    """Il frammento UI apre la scheda attesa, una sola volta."""
    src = _leggi("w814_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert m.group(1) == "813"
    assert src.count("with tab813:") == 1


def test_ui_titolo_atteso():
    src = _leggi("w814_ui.py")
    titolo = ("Officina meccanica / autoriparazione: "
              "pompa di calore aria-aria + compressore "
              "VSD con recupero calore + LED battono "
              "caldaia a gas + compressore standard + "
              "illuminazione tradizionale?")
    assert src.count(titolo) == 2


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w814_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w814_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st813_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) == 27
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w814_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 4
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_ui_guard_degenere_stretta():
    """La guard UI della scheda dichiara NON_CALCOLABILE
    anche per superficie <= 0, carico <= 0, portata
    <= 0, ore <= 0, consumi specifici <= 0,
    potenza <= 0, prezzi <= 0 e CAPEX <= 0
    (piu' stretta degli helper, che ammettono lo
    zero)."""
    src = _leggi("w814_ui.py")
    assert "float(_sup813) <= 0.0" in src
    assert "float(_qri813) <= 0.0" in src
    assert "float(_port813) <= 0.0" in src
    assert "int(_ore813) <= 0" in src
    assert "float(_cb813) <= 0.0" in src
    assert "float(_cv813) <= 0.0" in src
    assert "float(_frec813) < 0.0" in src
    assert "float(_pil813) <= 0.0" in src
    assert "float(_pg813) <= 0.0" in src
    assert "float(_pel813) <= 0.0" in src
    assert "float(_cx813) <= 0.0" in src
    assert "int(_vita813) <= 0" in src
    assert "Verdetto: NON_CALCOLABILE" in src


def test_ui_chiamata_calcola_keyword_uguali_firma():
    """La chiamata UI a calcola usa come keyword
    esattamente i parametri della firma helper."""
    src = textwrap.dedent(_leggi("w814_ui.py"))
    albero = ast.parse(src)
    chiamate = []
    for nodo in ast.walk(albero):
        if isinstance(nodo, ast.Call):
            func = nodo.func
            if isinstance(func, ast.Name) and func.id == "mh813_calcola":
                chiamate.append({kw.arg for kw in nodo.keywords})
    assert len(chiamate) == 1
    attesi = set(inspect.signature(mh813_calcola).parameters.keys())
    assert chiamate[0] == attesi


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w814_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def813[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w814_ui.py")
        usate = set(re.findall(r'_def813\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 17
        assert usate <= set(mh813_demo().keys())
