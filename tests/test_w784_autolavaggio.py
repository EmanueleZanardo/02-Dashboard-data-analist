"""Test tab784 "Autolavaggio: pompa di calore +
recupero calore dalle acque reflue batte la
caldaia a gas per acqua calda e asciugatura?"
(titolo completo nel frammento UI).
(File repo: tests/test_w784_autolavaggio.py,
contenuto pronto da scrivere in repo.)

Business case deterministico di un autolavaggio
guidato dai lavaggi annui di veicoli: DUE usi
termici, acqua calda di lavaggio + aria calda di
asciugatura. Acqua calda Q_acs = N x L x 4.186
x (T_uso - T_in) / 3600 kWh/anno; asciugatura
Q_asc = N x q_asc kWh/anno; gas baseline
G = (Q_acs + Q_asc) / eta_caldaia kWh/anno;
recupero solo sulla frazione acqua Q_rec =
eta_rec x Q_acs kWh/anno; calore residuo Q_res
= Q_acs + Q_asc - Q_rec; elettricita' pompa di
calore E_pdc = Q_res / COP_pdc; C_base =
G / 1000 x p_gas + O&M_base EUR/anno; C_alt =
E_pdc / 1000 x p_el + O&M_alt EUR/anno (prezzi
EUR/MWh, energie kWh: / 1000 esatto); risparmio
= C_base - C_alt; CO2_base = G / 1000 x f_gas
t/anno; CO2_alt = E_pdc / 1000 x f_el t/anno;
CO2_evitata = CO2_base - CO2_alt; flussi
[-CAPEX, risparmio x vita]; VAN, TIR, payback
(primo anno con cumulato >= 0); breakeven gas
p_gas_be = (E_pdc / 1000 x p_el + O&M_alt
- O&M_base) / (G / 1000) EUR/MWh, None se
G <= 0 o numeratore < 0, SOGLIA MINIMA quando
esiste. Verdetto: NON_CALCOLABILE se risparmio
<= 0 (guard degenere: UI salta KPI, grafico,
tabella e CSV); altrimenti CONVIENTE se VAN > 0,
MARGINALE se VAN negativa entro tolleranza %
del CAPEX, NON_CONVIENTE se VAN negativa oltre
la tolleranza. Distinzione esplicita: NON la
lavanderia industriale (panni, bagni di
lavaggio) e NON la tab precedente sui prodotti
freschi (pastorizzazione + freddo): qui il
driver sono i lavaggi/anno di veicoli, con DUE
usi termici, acqua calda di lavaggio + aria
calda di asciugatura, e il recupero avviene
solo sulla frazione acqua (acque reflue di
lavaggio), l'aria di asciugatura non e'
recuperabile; l'elettricita' di pompe e nastri
e' costo comune escluso dal confronto.

Demo (autolavaggio medio): N 30.000, L 60
L/lavaggio, T_in 10, T_uso 40 gradi C, q_asc
0,8 kWh/lavaggio, caldaia 0,9, recupero 0,4,
COP 3,5, gas 90, el 250 EUR/MWh, O&M base 1.200,
alt 1.500, CAPEX 25.000, WACC 5 %, vita 12,
f_gas 0,20, f_el 0,35, tolleranza 10 % del
CAPEX. Valori calcolati eseguendo
mh784_demo_calcoli(): Q_acs 62.790, Q_asc
24.000, G 96.433,33333333333, Q_rec 25.116,
Q_res 61.674, E_pdc 17.621,14285714286, C_base
8.979 circa (8.978,999999999998), C_alt
5.905,285714285715, risparmio 3.973,7142857142835,
CO2_base 19,286666666666665, CO2_alt 6,1674,
CO2_evitata 13,119266666666665, VAN
10.220,02964563713, TIR 11,666319454401842 %,
payback 7, breakeven gas 48,79314601748063,
verdetto CONVIENTE.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w785_helpers import (
    demo_calcoli,
    mh784_breakeven_gas,
    mh784_c_alt,
    mh784_c_base,
    mh784_calcola,
    mh784_co2_alt,
    mh784_co2_base,
    mh784_co2_evitata,
    mh784_cop,
    mh784_csv,
    mh784_demo,
    mh784_demo_calcoli,
    mh784_e_pdc,
    mh784_eta,
    mh784_eta_rec,
    mh784_flussi,
    mh784_gas,
    mh784_int_pos,
    mh784_num,
    mh784_nneg,
    mh784_payback,
    mh784_pct_tolleranza,
    mh784_pct_wacc,
    mh784_pos,
    mh784_q_acs,
    mh784_q_asc,
    mh784_q_rec,
    mh784_q_res,
    mh784_risparmio,
    mh784_tir,
    mh784_valida,
    mh784_van,
    mh784_verdetto,
)

_DEMO = {
    "q_acs_kwh_anno": 62790.0,
    "q_asc_kwh_anno": 24000.0,
    "gas_kwh_anno": 96433.33333333333,
    "q_rec_kwh_anno": 25116.0,
    "q_res_kwh_anno": 61674.0,
    "e_pdc_kwh_anno": 17621.14285714286,
    "c_base_eur_anno": 9878.999999999998,
    "c_alt_eur_anno": 5905.285714285715,
    "risparmio_eur_anno": 3973.7142857142835,
    "co2_base_t_anno": 19.286666666666665,
    "co2_alt_t_anno": 6.1674,
    "co2_evitata_t_anno": 13.119266666666665,
    "van": 10220.02964563713,
    "tir": 11.666319454401842,
    "breakeven_gas_eur_mwh": 48.79314601748063,
}


def _demo_kwargs():
    return dict(mh784_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh784_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh784_num(3, "x") == 3.0
    assert mh784_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh784_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh784_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh784_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh784_pos(0, "x")
    with pytest.raises(ValueError):
        mh784_pos(-1, "x")
    assert mh784_pos(0.5, "x") == 0.5


def test_cop_maggiore_di_uno():
    assert mh784_cop(3.5, "x") == 3.5
    assert mh784_cop(1.01, "x") == 1.01
    with pytest.raises(ValueError):
        mh784_cop(1.0, "x")
    with pytest.raises(ValueError):
        mh784_cop(0.5, "x")
    with pytest.raises(ValueError):
        mh784_cop(0, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh784_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh784_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh784_int_pos(0, "x")


def test_eta_limiti():
    assert mh784_eta(1.0, "x") == 1.0
    assert mh784_eta(0.9, "x") == 0.9
    with pytest.raises(ValueError):
        mh784_eta(0, "x")
    with pytest.raises(ValueError):
        mh784_eta(1.01, "x")


def test_eta_rec_limiti():
    assert mh784_eta_rec(0.0, "x") == 0.0
    assert mh784_eta_rec(1.0, "x") == 1.0
    assert mh784_eta_rec(0.4, "x") == 0.4
    with pytest.raises(ValueError):
        mh784_eta_rec(-0.1, "x")
    with pytest.raises(ValueError):
        mh784_eta_rec(1.01, "x")


def test_pct_wacc_limiti():
    assert mh784_pct_wacc(0, "x") == 0.0
    assert mh784_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh784_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh784_pct_tolleranza(0, "x") == 0.0
    assert mh784_pct_tolleranza(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh784_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh784_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_q_acs_formula_e_temperature():
    assert mh784_q_acs(30000, 60, 10, 40) == 62790.0
    assert mh784_q_acs(30000, 60, 20, 40) == pytest.approx(41860.0)
    assert mh784_q_acs(30000, 60, 10, 25) == pytest.approx(31395.0)
    with pytest.raises(ValueError):
        mh784_q_acs(30000, 60, 40, 40)
    with pytest.raises(ValueError):
        mh784_q_acs(30000, 60, 40, 10)
    with pytest.raises(ValueError):
        mh784_q_acs(0, 60, 10, 40)
    with pytest.raises(ValueError):
        mh784_q_acs(30000.5, 60, 10, 40)
    with pytest.raises(ValueError):
        mh784_q_acs(30000, 0, 10, 40)
    with pytest.raises(ValueError):
        mh784_q_acs(30000, -5, 10, 40)


def test_q_asc_gas_rec_res():
    assert mh784_q_asc(30000, 0.8) == 24000.0
    assert mh784_q_asc(30000, 0) == 0.0
    assert mh784_gas(62790, 24000, 0.9) == pytest.approx(96433.33333333333)
    assert mh784_gas(0, 24000, 0.9) == pytest.approx(26666.666666666668)
    assert mh784_q_rec(62790, 0.4) == pytest.approx(25116.0)
    assert mh784_q_rec(62790, 0) == 0.0
    assert mh784_q_rec(62790, 1.0) == 62790.0
    assert mh784_q_res(62790, 24000, 25116) == 61674.0
    assert mh784_q_res(62790, 24000, 0) == 86790.0
    with pytest.raises(ValueError):
        mh784_q_asc(30000, -0.1)
    with pytest.raises(ValueError):
        mh784_gas(62790, 24000, 0)
    with pytest.raises(ValueError):
        mh784_gas(62790, 24000, 1.01)
    with pytest.raises(ValueError):
        mh784_q_rec(62790, 1.01)
    with pytest.raises(ValueError):
        mh784_q_rec(62790, -0.1)


def test_e_pdc():
    assert mh784_e_pdc(61674, 3.5) == pytest.approx(17621.14285714286)
    assert mh784_e_pdc(86790, 3.5) == pytest.approx(24797.14285714286)
    assert mh784_e_pdc(0, 3.5) == 0.0
    with pytest.raises(ValueError):
        mh784_e_pdc(61674, 1.0)
    with pytest.raises(ValueError):
        mh784_e_pdc(61674, 0.5)


def test_c_base_c_alt_scomposizione():
    assert mh784_c_base(96433.33333333333, 90,
                        1200) == pytest.approx(9879.0)
    assert mh784_c_base(96433.33333333333, 0,
                        1200) == pytest.approx(1200.0)
    assert mh784_c_base(0, 90, 1200) == pytest.approx(1200.0)
    assert mh784_c_alt(17621.14285714286, 250,
                       1500) == pytest.approx(5905.285714285715)
    assert mh784_c_alt(0, 250, 1500) == pytest.approx(1500.0)
    with pytest.raises(ValueError):
        mh784_c_base(96433.33333333333, -1, 1200)
    with pytest.raises(ValueError):
        mh784_c_alt(17621.14285714286, 250, -1)


def test_risparmio_segno():
    assert mh784_risparmio(9879.0, 5905.285714285715) == \
        pytest.approx(3973.7142857142835)
    assert mh784_risparmio(5905.285714285715, 5905.285714285715) == 0.0
    assert mh784_risparmio(5057.333333333333, 5905.285714285715) == \
        pytest.approx(-847.9523809523816)


def test_co2_base_alt_evitata():
    assert mh784_co2_base(96433.33333333333,
                          0.20) == pytest.approx(19.286666666666665)
    assert mh784_co2_alt(17621.14285714286,
                         0.35) == pytest.approx(6.1674)
    assert mh784_co2_evitata(96433.33333333333, 0.20,
                             17621.14285714286,
                             0.35) == pytest.approx(13.119266666666665)
    # Solo frazione acqua recuperata: la CO2 non
    # dipende da Q_rec direttamente, ma da G e da
    # E_pdc, che invece ne dipendono.
    assert mh784_co2_base(0, 0.20) == 0.0
    assert mh784_co2_alt(0, 0.35) == 0.0
    with pytest.raises(ValueError):
        mh784_co2_base(96433.33333333333, -0.10)
    with pytest.raises(ValueError):
        mh784_co2_alt(17621.14285714286, -0.10)


def test_breakeven_gas_demo_e_varianti():
    assert mh784_breakeven_gas(17621.14285714286, 250, 1500, 1200,
                               96433.33333333333) == \
        pytest.approx(48.79314601748063)
    assert mh784_breakeven_gas(17621.14285714286, 400, 1500, 1200,
                               96433.33333333333) == \
        pytest.approx(76.20245913782037)
    assert mh784_breakeven_gas(10764.0, 250, 1500, 1200,
                               69766.66666666667) == pytest.approx(42.87147634973722)
    assert mh784_breakeven_gas(17621.14285714286, 250, 1500, 1200,
                               0) is None
    # Numeratore negativo: alternativa gia' piu'
    # conveniente a prezzo gas zero -> nessun pareggio.
    assert mh784_breakeven_gas(1000.0, 250, 100, 1200,
                               96433.33333333333) is None
    with pytest.raises(ValueError):
        mh784_breakeven_gas(17621.14285714286, 250, 1500, 1200, -1)


def test_breakeven_verifica_pareggio():
    """Al prezzo gas di pareggio i costi si eguagliano
    e il risparmio e' zero: scatta la guard
    NON_CALCOLABILE, non un verdetto di convenienza."""
    bc = _variante(p_gas_eur_mwh=48.79314601748063)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    demo = mh784_demo_calcoli()
    assert (demo["e_pdc_kwh_anno"] / 1000.0
            * demo["p_el_eur_mwh"]
            + demo["om_alt_eur_anno"]
            - demo["om_base_eur_anno"]) == pytest.approx(
        demo["gas_kwh_anno"] / 1000.0
        * demo["breakeven_gas_eur_mwh"])


def test_breakeven_soglia_minima():
    """Sopra la soglia l'alternativa vince, sotto perde."""
    be = mh784_demo_calcoli()["breakeven_gas_eur_mwh"]
    assert _variante(p_gas_eur_mwh=be + 1)[
        "c_alt_eur_anno"] < _variante(p_gas_eur_mwh=be + 1)[
        "c_base_eur_anno"]
    assert _variante(p_gas_eur_mwh=be - 1)[
        "c_alt_eur_anno"] > _variante(p_gas_eur_mwh=be - 1)[
        "c_base_eur_anno"]


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh784_flussi(25000, 3973.7142857142835, 12)
    assert len(fl) == 13
    assert fl[0] == -25000
    assert all(f == 3973.7142857142835 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh784_demo_calcoli()
    assert bc["van"] == pytest.approx(10220.02964563713)
    assert mh784_van([-25000] + [3973.7142857142835] * 12,
                     0) == pytest.approx(22684.571428571395)
    assert mh784_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh784_demo_calcoli()
    assert bc["tir"] == pytest.approx(11.666319454401842)
    assert mh784_tir([-25000] + [3973.7142857142835] * 12) == \
        pytest.approx(0.11666319454401842)
    tir = mh784_tir([-25000] + [3973.7142857142835] * 12)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-25000] + [3973.7142857142835] * 12))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh784_payback([-25000] + [3973.7142857142835] * 12) == 7
    assert mh784_payback([-25000] + [-1000.0] * 12) is None
    assert mh784_payback([0] + [3973.7142857142835] * 12) == 0
    assert mh784_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh784_verdetto(3973.7142857142835, 10220.02964563713, 25000,
                          10.0) == "CONVIENTE"
    assert mh784_verdetto(3973.7142857142835, 0.0, 25000, 10.0) == "MARGINALE"
    assert mh784_verdetto(3973.7142857142835, -2500.0, 25000, 10.0) == "MARGINALE"
    assert mh784_verdetto(3973.7142857142835, -2500.01, 25000, 10.0) == "NON_CONVIENTE"
    assert mh784_verdetto(3973.7142857142835, -15421.36, 25000, 10.0) == "NON_CONVIENTE"
    assert mh784_verdetto(0.0, 10220.02964563713, 25000,
                          10.0) == "NON_CALCOLABILE"
    assert mh784_verdetto(-847.9523809523816, -32515.62, 25000,
                          10.0) == "NON_CALCOLABILE"
    assert mh784_verdetto(None, 10220.02964563713, 25000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh784_verdetto(float("nan"), 10220.0, 25000, 10.0)
    with pytest.raises(ValueError):
        mh784_verdetto(3973.71, 10220.0, -1, 10.0)
    with pytest.raises(ValueError):
        mh784_verdetto(3973.71, 10220.0, 25000, 100.1)


def test_valida_demo_ok():
    v = mh784_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("n_lavaggi", "30000"),
                       ("n_lavaggi", float("nan")),
                       ("n_lavaggi", float("inf")),
                       ("n_lavaggi", True),
                       ("p_gas_eur_mwh", None),
                       ("litri_per_lavaggio", "60")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh784_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("n_lavaggi", 0), ("n_lavaggi", -1),
                          ("n_lavaggi", 30000.5),
                          ("litri_per_lavaggio", 0),
                          ("litri_per_lavaggio", -5),
                          ("q_asc_kwh_per_lavaggio", -0.1),
                          ("eta_caldaia", 0),
                          ("eta_caldaia", 1.01),
                          ("eta_rec", -0.1),
                          ("eta_rec", 1.01),
                          ("cop_pdc", 1.0),
                          ("cop_pdc", 0.5),
                          ("p_gas_eur_mwh", -1),
                          ("p_el_eur_mwh", -1),
                          ("om_base_eur_anno", -100),
                          ("om_alt_eur_anno", -100),
                          ("capex_eur", -1),
                          ("wacc_pct", -0.1), ("wacc_pct", 50.1),
                          ("vita_anni", 0), ("vita_anni", 2.5),
                          ("f_gas_t_per_mwh", -0.10),
                          ("f_el_t_per_mwh", -0.10),
                          ("tolleranza_pct", -1),
                          ("tolleranza_pct", 100.1)):
        d = _demo_kwargs()
        d[campo] = valore
        assert mh784_valida(**d)["valido"] is False


def test_valida_temperature_uso_non_maggiore_ingresso():
    d = _demo_kwargs()
    d["t_uso_c"] = 10
    assert mh784_valida(**d)["valido"] is False
    d["t_uso_c"] = 5
    assert mh784_valida(**d)["valido"] is False
    with pytest.raises(ValueError):
        _variante(t_uso_c=10)


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"q_asc_kwh_per_lavaggio": 0,
              "eta_rec": 0,
              "p_gas_eur_mwh": 0,
              "p_el_eur_mwh": 0,
              "om_base_eur_anno": 0, "om_alt_eur_anno": 0,
              "capex_eur": 0, "wacc_pct": 0,
              "f_gas_t_per_mwh": 0, "f_el_t_per_mwh": 0,
              "tolleranza_pct": 0})
    assert mh784_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["eta_rec"] = 1
    d["q_asc_kwh_per_lavaggio"] = 0.8
    assert mh784_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh784_demo()
    assert d["n_lavaggi"] == 30000
    assert d["litri_per_lavaggio"] == 60
    assert d["t_in_c"] == 10
    assert d["t_uso_c"] == 40
    assert d["q_asc_kwh_per_lavaggio"] == 0.8
    assert d["eta_caldaia"] == 0.9
    assert d["eta_rec"] == 0.4
    assert d["cop_pdc"] == 3.5
    assert d["p_gas_eur_mwh"] == 90
    assert d["p_el_eur_mwh"] == 250
    assert d["om_base_eur_anno"] == 1200
    assert d["om_alt_eur_anno"] == 1500
    assert d["capex_eur"] == 25000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 12
    assert d["f_gas_t_per_mwh"] == 0.20
    assert d["f_el_t_per_mwh"] == 0.35
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    """Tutti gli output numerici demo a tolleranza
    1e-9 relativa: confronto delle costanti _DEMO
    contro mh784_demo_calcoli()."""
    bc = mh784_demo_calcoli()
    for chiave, atteso in _DEMO.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert got == pytest.approx(atteso, rel=1e-9), chiave
    assert bc["payback"] == 7
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True
    assert demo_calcoli()["van"] == bc["van"]


def test_demo_calcoli_fisica_economia():
    bc = mh784_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(9879.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(5905.285714285715)
    assert bc["risparmio_eur_anno"] == pytest.approx(3973.7142857142835)
    assert bc["co2_base_t_anno"] == pytest.approx(19.286666666666665)
    assert bc["co2_alt_t_anno"] == pytest.approx(6.1674)
    assert bc["co2_evitata_t_anno"] == pytest.approx(13.119266666666665)
    assert bc["gas_kwh_anno"] == pytest.approx(96433.33333333333)


def test_demo_flussi_e_cumulato():
    bc = mh784_demo_calcoli()
    assert bc["flussi"][0] == -25000
    assert len(bc["flussi"]) == 13
    assert all(f == pytest.approx(3973.7142857142835) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -25000
    assert righe.iloc[6]["Cumulato (EUR)"] == pytest.approx(-1157.7142857143026)
    assert righe.iloc[7]["Cumulato (EUR)"] == pytest.approx(2816.0)
    assert righe.iloc[12]["Cumulato (EUR)"] == pytest.approx(22684.571428571395)


def test_demo_tabella_righe():
    bc = mh784_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Acqua calda di lavaggio (kWh/anno)"] == pytest.approx(62790.0)
    assert mappa["Aria calda di asciugatura (kWh/anno)"] == pytest.approx(24000.0)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(96433.33333333333)
    assert mappa["Calore recuperato acque reflue (kWh/anno)"] == pytest.approx(25116.0)
    assert mappa["Calore residuo (kWh/anno)"] == pytest.approx(61674.0)
    assert mappa["Elettricita' pompa di calore (kWh_e/anno)"] == pytest.approx(17621.14285714286)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(9879.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(5905.285714285715)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(3973.7142857142835)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(13.119266666666665)
    assert mappa["Payback (anni)"] == 7
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] == \
        pytest.approx(48.79314601748063)


def test_demo_coerenza_interna():
    bc = mh784_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["q_acs_kwh_anno"] == pytest.approx(
        bc["n_lavaggi"] * bc["litri_per_lavaggio"] * 4.186
        * (bc["t_uso_c"] - bc["t_in_c"]) / 3600.0)
    assert bc["q_asc_kwh_anno"] == pytest.approx(
        bc["n_lavaggi"] * bc["q_asc_kwh_per_lavaggio"])
    assert bc["gas_kwh_anno"] == pytest.approx(
        (bc["q_acs_kwh_anno"] + bc["q_asc_kwh_anno"])
        / bc["eta_caldaia"])
    assert bc["q_rec_kwh_anno"] == pytest.approx(
        bc["eta_rec"] * bc["q_acs_kwh_anno"])
    assert bc["q_res_kwh_anno"] == pytest.approx(
        bc["q_acs_kwh_anno"] + bc["q_asc_kwh_anno"]
        - bc["q_rec_kwh_anno"])
    assert bc["e_pdc_kwh_anno"] == pytest.approx(
        bc["q_res_kwh_anno"] / bc["cop_pdc"])
    assert bc["co2_evitata_t_anno"] == pytest.approx(
        bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])
    assert bc["c_base_eur_anno"] == pytest.approx(
        bc["gas_kwh_anno"] / 1000.0 * bc["p_gas_eur_mwh"]
        + bc["om_base_eur_anno"])
    assert bc["c_alt_eur_anno"] == pytest.approx(
        bc["e_pdc_kwh_anno"] / 1000.0 * bc["p_el_eur_mwh"]
        + bc["om_alt_eur_anno"])


def test_demo_contro_riconteggio_indipendente():
    n, lit, tin, tuso, qasc_spec = 30000, 60, 10, 40, 0.8
    eta, erec, copp = 0.9, 0.4, 3.5
    pg, pel, omb, oma, cx = 90, 250, 1200, 1500, 25000
    fg, fel, wacc, vita = 0.20, 0.35, 5.0, 12
    qacs = n * lit * 4.186 * (tuso - tin) / 3600.0
    qasc = n * qasc_spec
    gas = (qacs + qasc) / eta
    qrec = erec * qacs
    qres = qacs + qasc - qrec
    ep = qres / copp
    cb = gas / 1000.0 * pg + omb
    ca = ep / 1000.0 * pel + oma
    risp = cb - ca
    co2b = gas / 1000.0 * fg
    co2a = ep / 1000.0 * fel
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    be = (ep / 1000.0 * pel + oma - omb) / (gas / 1000.0)
    bc = mh784_demo_calcoli()
    assert bc["q_acs_kwh_anno"] == pytest.approx(qacs)
    assert bc["q_asc_kwh_anno"] == pytest.approx(qasc)
    assert bc["gas_kwh_anno"] == pytest.approx(gas)
    assert bc["q_rec_kwh_anno"] == pytest.approx(qrec)
    assert bc["q_res_kwh_anno"] == pytest.approx(qres)
    assert bc["e_pdc_kwh_anno"] == pytest.approx(ep)
    assert bc["c_base_eur_anno"] == pytest.approx(cb)
    assert bc["c_alt_eur_anno"] == pytest.approx(ca)
    assert bc["risparmio_eur_anno"] == pytest.approx(risp)
    assert bc["co2_base_t_anno"] == pytest.approx(co2b)
    assert bc["co2_alt_t_anno"] == pytest.approx(co2a)
    assert bc["co2_evitata_t_anno"] == pytest.approx(co2)
    assert bc["van"] == pytest.approx(van)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(be)


# ---------------------------------------------------------------- varianti
def test_variante_gas_basso_risparmio_positivo_ma_non_conviente():
    """Gas 60 EUR/MWh: risparmio ancora positivo
    (1.080,71) ma VAN -15.421,36 oltre la tolleranza
    (2.500): NON_CONVIENTE. Il verdetto guarda la
    VAN, non il solo risparmio positivo."""
    bc = _variante(p_gas_eur_mwh=60)
    assert bc["risparmio_eur_anno"] == pytest.approx(1080.7142857142844)
    assert bc["van"] == pytest.approx(-15421.357338609265)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_gas_40_non_calcolabile():
    """Gas 40 EUR/MWh: risparmio -847,95, verdetto
    NON_CALCOLABILE, ma helper calcolabili
    (flussi pieni, VAN -32.515,62, TIR None,
    payback None)."""
    bc = _variante(p_gas_eur_mwh=40)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(-847.9523809523816)
    assert bc["van"] == pytest.approx(-32515.61532810686)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_capex_alto_marginale_e_non_conviente():
    bc = _variante(capex_eur=37500)
    assert bc["risparmio_eur_anno"] == pytest.approx(3973.7142857142835)
    assert bc["van"] == pytest.approx(-2279.970354362876)
    assert bc["payback"] == 10
    assert bc["verdetto"] == "MARGINALE"
    bc2 = _variante(capex_eur=40000)
    assert bc2["van"] == pytest.approx(-4779.970354362873)
    assert bc2["payback"] == 11
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex_eur=0)
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(35220.02964563713, rel=1e-6)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(22684.571428571395)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=8)
    assert len(bc2["flussi"]) == 9
    assert bc2["van"] == pytest.approx(682.9608737429462)
    assert bc2["payback"] == 7
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_el_alto_non_conviente():
    """Elettricita' 400 EUR/MWh: risparmio 1.330,54,
    VAN -13.207,06 oltre la tolleranza (2.500):
    NON_CONVIENTE, payback None, breakeven gas
    76,20 (sale perche' l'alternativa elettrica
    costa di piu')."""
    bc = _variante(p_el_eur_mwh=400)
    assert bc["risparmio_eur_anno"] == pytest.approx(1330.5428571428547)
    assert bc["van"] == pytest.approx(-13207.063844063325)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(76.20245913782037)


def test_variante_senza_recupero_non_conviente():
    """Senza recupero (eta_rec zero): calore residuo
    86.790, E_pdc 24.797,14, risparmio 2.179,71,
    VAN -5.680,64, breakeven 67,40, NON_CONVIENTE.
    Il recupero solo sulla frazione acqua e'
    decisivo."""
    bc = _variante(eta_rec=0)
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["q_res_kwh_anno"] == pytest.approx(86790.0)
    assert bc["e_pdc_kwh_anno"] == pytest.approx(24797.14285714286)
    assert bc["risparmio_eur_anno"] == pytest.approx(2179.7142857142835)
    assert bc["van"] == pytest.approx(-5680.643790152035)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(67.39667176929535)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_senza_asciugatura():
    """Senza asciugatura (q_asc zero): l'aria non
    recuperabile sparisce, ma il caso resta
    CONVIENTE con risparmio 3.288, VAN 4.142,37
    e breakeven 42,87."""
    bc = _variante(q_asc_kwh_per_lavaggio=0)
    assert bc["q_asc_kwh_anno"] == 0.0
    assert bc["e_pdc_kwh_anno"] == pytest.approx(10764.0)
    assert bc["c_base_eur_anno"] == pytest.approx(7479.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(4191.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(3288.0)
    assert bc["van"] == pytest.approx(4142.371380643677)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(42.87147634973722)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_cop_pdc_basso():
    """COP pompa di calore 2,5 invece di 3,5:
    E_pdc 24.669,60, risparmio 2.211,60,
    VAN -5.398,03, breakeven 67,07, payback 12,
    NON_CONVIENTE."""
    bc = _variante(cop_pdc=2.5)
    assert bc["e_pdc_kwh_anno"] == pytest.approx(24669.6)
    assert bc["risparmio_eur_anno"] == pytest.approx(2211.5999999999985)
    assert bc["van"] == pytest.approx(-5398.0326808298305)
    assert bc["payback"] == 12
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(67.06602143104044)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_lavaggi_dimezzati():
    """Lavaggi 15.000: tutti i vettori si dimezzano,
    il risparmio scende a 1.836,86, la VAN e'
    -8.719,47, NON_CONVIENTE (il CAPEX non si
    dimezza, e il breakeven sale a 51,90 perche'
    gli O&M fissi pesano di piu')."""
    bc = _variante(n_lavaggi=15000)
    assert bc["q_acs_kwh_anno"] == pytest.approx(31395.0)
    assert bc["q_asc_kwh_anno"] == pytest.approx(12000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(1836.8571428571418)
    assert bc["van"] == pytest.approx(-8719.472922648758)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(51.904103501061684)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_monotonia_prezzo_gas_crescente():
    base = mh784_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas_eur_mwh=91)["risparmio_eur_anno"]
    basso = _variante(p_gas_eur_mwh=89)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(96.43333333333333)
    assert base - basso == pytest.approx(96.43333333333333)


def test_monotonia_lavaggi_crescente():
    """Il risparmio cresce con i lavaggi (meno O&M
    fissi per lavaggio) finche' i vettori crescono."""
    assert _variante(n_lavaggi=15000)["risparmio_eur_anno"] < \
        mh784_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(n_lavaggi=60000)["risparmio_eur_anno"] > \
        mh784_demo_calcoli()["risparmio_eur_anno"]


def test_demo_deterministica_due_chiamate():
    a = mh784_demo_calcoli()
    b = mh784_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh784_demo().keys()) == {
        "n_lavaggi", "litri_per_lavaggio", "t_in_c",
        "t_uso_c", "q_asc_kwh_per_lavaggio",
        "eta_caldaia", "eta_rec", "cop_pdc",
        "p_gas_eur_mwh", "p_el_eur_mwh",
        "om_base_eur_anno", "om_alt_eur_anno",
        "capex_eur", "wacc_pct", "vita_anni",
        "f_gas_t_per_mwh", "f_el_t_per_mwh",
        "tolleranza_pct"}


# ---------------------------------------------------------------- degenere
def test_degenere_cop_uguale_uno_sollevela():
    with pytest.raises(ValueError):
        _variante(cop_pdc=1.0)


def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"n_lavaggi": 0}, {"n_lavaggi": -1},
               {"n_lavaggi": 30000.5},
               {"litri_per_lavaggio": 0},
               {"litri_per_lavaggio": -5},
               {"t_uso_c": 10}, {"t_uso_c": 5},
               {"q_asc_kwh_per_lavaggio": -0.1},
               {"eta_caldaia": 0}, {"eta_caldaia": 1.01},
               {"eta_rec": -0.1}, {"eta_rec": 1.01},
               {"cop_pdc": 1.0}, {"cop_pdc": 0.5},
               {"p_gas_eur_mwh": -1},
               {"p_el_eur_mwh": -1},
               {"om_base_eur_anno": -100},
               {"om_alt_eur_anno": -100},
               {"capex_eur": -1},
               {"wacc_pct": -1}, {"wacc_pct": 60},
               {"vita_anni": 0}, {"vita_anni": 2.5},
               {"f_gas_t_per_mwh": -0.10},
               {"f_el_t_per_mwh": -0.10},
               {"tolleranza_pct": -1},
               {"tolleranza_pct": 100.1}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh784_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"n_lavaggi": "30000"},
               {"n_lavaggi": float("nan")},
               {"p_gas_eur_mwh": float("inf")},
               {"capex_eur": True},
               {"litri_per_lavaggio": "60"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh784_valida(**d)["valido"] is False


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    """Differenza chiave: risparmio <= 0 NON solleva
    negli helper (resta calcolabile con flussi, VAN,
    TIR e payback), ma il verdetto e' NON_CALCOLABILE
    e la UI salta KPI, grafico, tabella e CSV."""
    for kw in ({"p_gas_eur_mwh": 40},
               {"p_gas_eur_mwh": 48.79314601748063}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] <= 0.0
        assert bc["verdetto"] == "NON_CALCOLABILE"
        assert bc["flussi"]


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh784_demo_calcoli()
    testo = mh784_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_gas_eur_mwh" in testo
    assert "co2_evitata_t_anno" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh784_demo_calcoli()
    testo = mh784_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"q_acs_kwh_anno;{bc['q_acs_kwh_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh784_demo_calcoli()
    testo = mh784_csv(bc, _demo_kwargs())
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
    # Token della tab precedente, costruiti
    # per concatenazione: questo stesso file non li contiene
    # come sottostringhe contigue.
    return ["mh" + "78" + "3", "st" + "78" + "3",
            "tab" + "78" + "3"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w785_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w785_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab784:")


def test_registry_chain_tail_and_count():
    """Registry della nuova tab: il frammento UI apre la tab
    numero 784 (la coda della catena termina con la nuova tab
    e il conteggio atteso delle tab e' 784)."""
    src = _leggi("w785_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 784
    assert src.count("with tab784:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w785_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w785_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st784_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) >= 19
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w785_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 2
    # Entrambe le guard (input degenere e risparmio <= 0)
    # stanno prima di KPI / grafico / tabella / CSV.
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w785_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def784[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w785_ui.py")
        usate = set(re.findall(r'_def784\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 18
        assert usate <= set(mh784_demo().keys())
