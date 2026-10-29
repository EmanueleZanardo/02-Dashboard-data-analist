"""Test tab795 "Supermercato: recupero calore
banchi frigo + pompa di calore batte caldaia
a gas + chiller?"
(titolo completo nel frammento UI).
Contenuto pronto da scrivere in repo come test
della tab supermercato.

Business case deterministico di un supermercato
guidato dai m2 di vendita per riscaldamento,
raffrescamento e carico termico dei banchi
frigo, sempre accesi. Riscaldamento supermercato
Q_risc = S x q_risc kWh_th/anno; raffrescamento
supermercato Q_raff = S x q_raff kWh_c/anno;
carico termico frigo Q_frigo = S x q_frigo
kWh_th/anno; elettricita' frigo E_frigo =
Q_frigo / COP_frigo kWh_e/anno (uguale in
baseline e alternativa); calore di scarto
frigo Q_scartato = Q_frigo + E_frigo
kWh_th/anno; calore recuperato sul
riscaldamento Q_rec = eta_rec x Q_scartato
kWh_th/anno, SOLO dallo scarto dei frighi
(puo' superare Q_risc, perche' lo scarto e'
indipendente dal riscaldamento);
riscaldamento residuo Q_risc_res =
max(0, Q_risc - Q_rec) kWh_th/anno (l'eccesso
viene sprecato, senza export); gas baseline
G_base = Q_risc / eta_caldaia kWh/anno;
elettricita' chiller E_chiller =
Q_raff / COP_chiller kWh_e/anno; elettricita'
pompa di calore in riscaldamento E_pdc_risc =
Q_risc_res / COP_risc kWh_e/anno; in
raffrescamento E_pdc_raff = Q_raff / COP_raff
kWh_e/anno; C_base = (E_chiller + E_frigo)
/ 1000 x p_el + G_base / 1000 x p_gas + O&M_base
EUR/anno; C_alt = (E_pdc_risc + E_pdc_raff
+ E_frigo) / 1000 x p_el + O&M_alt EUR/anno
(prezzi EUR/MWh, energie kWh: / 1000 esatto);
risparmio = C_base - C_alt; CO2_base =
G_base / 1000 x f_gas + (E_chiller + E_frigo)
/ 1000 x f_el t/anno; CO2_alt = (E_pdc_risc
+ E_pdc_raff + E_frigo) / 1000 x f_el t/anno;
CO2_evitata = CO2_base - CO2_alt; flussi
[-CAPEX, risparmio x vita]; VAN, TIR, payback
(primo anno con cumulato >= 0); breakeven gas
p_gas_be = (C_alt - (E_chiller + E_frigo)
/ 1000 x p_el - O&M_base) x 1000 / G_base
EUR/MWh, None se G_base <= 0 o numeratore < 0,
SOGLIA MINIMA quando esiste. Verdetto:
NON_CALCOLABILE se risparmio <= 0 (guard
degenere: UI salta KPI, grafico, tabella e
CSV); altrimenti CONVIENTE se VAN > 0,
MARGINALE se VAN negativa entro tolleranza %
del CAPEX, NON_CONVIENTE se VAN negativa oltre
la tolleranza. Distinzione esplicita: distinto
dall'ospedale (ventilazione di reparto 24h,
recupero SOLO da aria esausta), dall'albergo
(pernottamento turistico, ACS docce ospiti),
dalla scuola (chiusure stagionali, aule +
mensa), dalla piscina (vasca riscaldata) e
dalla palestra (docce utenti): qui driver = m2
di vendita per riscaldamento/raffrescamento/
carico frigo; banchi frigo sempre accesi;
recupero SOLO da calore di scarto dei frighi
sul riscaldamento.

Demo (supermercato): 3.000 m2 di vendita a 150
kWh_th/m2/anno di riscaldamento, 80
kWh_c/m2/anno di raffrescamento e 250
kWh_th/m2/anno di carico termico frigo,
recupero 0,30, caldaia 0,90, chiller COP 3,0,
frigo COP 2,5, pompa di calore COP
riscaldamento 3,8 e COP raffrescamento 3,4,
gas 90, el 250 EUR/MWh, O&M base 30.000, alt
40.000, CAPEX 200.000, WACC 5 %, vita 15,
f_gas 0,20, f_el 0,35, tolleranza 10 % del
CAPEX. Valori calcolati eseguendo
mh795_demo_calcoli(): Q_risc 450.000, Q_raff
240.000, Q_frigo 750.000, E_frigo 300.000,
Q_scartato 1.050.000, Q_rec 315.000,
Q_risc_res 135.000, G_base 500.000,
E_chiller 80.000, E_pdc_risc
35.526,31578947369, E_pdc_raff
70.588,23529411765, C_base 170.000, C_alt
141.528,63777089783, risparmio
28.471,362229102175, CO2_base 233,0, CO2_alt
142,14009287925694, CO2_evitata
90,85990712074306, VAN 95.523,00381925161,
TIR 11,426799832343992 %, payback 8,
breakeven gas 33,05727554179565, verdetto
CONVIENTE.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w796_helpers import (
    demo_calcoli,
    mh795_breakeven_gas,
    mh795_c_alt,
    mh795_c_base,
    mh795_calcola,
    mh795_co2_alt,
    mh795_co2_base,
    mh795_co2_evitata,
    mh795_cop,
    mh795_csv,
    mh795_demo,
    mh795_demo_calcoli,
    mh795_e_chiller,
    mh795_e_frigo,
    mh795_e_pdc_raff,
    mh795_e_pdc_risc,
    mh795_eta,
    mh795_eta_rec,
    mh795_flussi,
    mh795_gas,
    mh795_int_pos,
    mh795_num,
    mh795_nneg,
    mh795_payback,
    mh795_pct_tolleranza,
    mh795_pct_wacc,
    mh795_pos,
    mh795_q_frigo,
    mh795_q_raff,
    mh795_q_rec,
    mh795_q_risc,
    mh795_q_risc_res,
    mh795_q_scartato,
    mh795_risparmio,
    mh795_tir,
    mh795_valida,
    mh795_van,
    mh795_verdetto,
)

_DEMO = {
    "q_risc_kwh_anno": 450000.0,
    "q_raff_kwh_anno": 240000.0,
    "q_frigo_kwh_anno": 750000.0,
    "e_frigo_kwh_anno": 300000.0,
    "q_scartato_kwh_anno": 1050000.0,
    "q_rec_kwh_anno": 315000.0,
    "q_risc_res_kwh_anno": 135000.0,
    "gas_base_kwh_anno": 500000.0,
    "e_chiller_kwh_anno": 80000.0,
    "e_pdc_risc_kwh_anno": 35526.31578947369,
    "e_pdc_raff_kwh_anno": 70588.23529411765,
    "c_base_eur_anno": 170000.0,
    "c_alt_eur_anno": 141528.63777089783,
    "risparmio_eur_anno": 28471.362229102175,
    "co2_base_t_anno": 233.0,
    "co2_alt_t_anno": 142.14009287925694,
    "co2_evitata_t_anno": 90.85990712074306,
    "van": 95523.00381925161,
    "tir": 11.426799832343992,
    "breakeven_gas_eur_mwh": 33.05727554179565,
}


def _demo_kwargs():
    return dict(mh795_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh795_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh795_num(3, "x") == 3.0
    assert mh795_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh795_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh795_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh795_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh795_pos(0, "x")
    with pytest.raises(ValueError):
        mh795_pos(-1, "x")
    assert mh795_pos(0.5, "x") == 0.5


def test_cop_maggiore_di_uno():
    assert mh795_cop(3.8, "x") == 3.8
    assert mh795_cop(1.01, "x") == 1.01
    with pytest.raises(ValueError):
        mh795_cop(1.0, "x")
    with pytest.raises(ValueError):
        mh795_cop(0.5, "x")
    with pytest.raises(ValueError):
        mh795_cop(0, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh795_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh795_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh795_int_pos(0, "x")


def test_eta_limiti():
    assert mh795_eta(1.0, "x") == 1.0
    assert mh795_eta(0.9, "x") == 0.9
    with pytest.raises(ValueError):
        mh795_eta(0, "x")
    with pytest.raises(ValueError):
        mh795_eta(1.01, "x")


def test_eta_rec_limiti():
    assert mh795_eta_rec(0.0, "x") == 0.0
    assert mh795_eta_rec(1.0, "x") == 1.0
    assert mh795_eta_rec(0.30, "x") == 0.30
    with pytest.raises(ValueError):
        mh795_eta_rec(-0.1, "x")
    with pytest.raises(ValueError):
        mh795_eta_rec(1.01, "x")


def test_pct_wacc_limiti():
    assert mh795_pct_wacc(0, "x") == 0.0
    assert mh795_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh795_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh795_pct_tolleranza(0, "x") == 0.0
    assert mh795_pct_tolleranza(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh795_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh795_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_q_risc_q_raff_q_frigo():
    assert mh795_q_risc(3000, 150) == 450000.0
    assert mh795_q_risc(3000, 0) == 0.0
    assert mh795_q_raff(3000, 80) == 240000.0
    assert mh795_q_raff(3000, 0) == 0.0
    assert mh795_q_frigo(3000, 250) == 750000.0
    assert mh795_q_frigo(3000, 0) == 0.0
    with pytest.raises(ValueError):
        mh795_q_risc(0, 150)
    with pytest.raises(ValueError):
        mh795_q_risc(3000, -10)
    with pytest.raises(ValueError):
        mh795_q_raff(0, 80)
    with pytest.raises(ValueError):
        mh795_q_raff(3000, -10)
    with pytest.raises(ValueError):
        mh795_q_frigo(0, 250)
    with pytest.raises(ValueError):
        mh795_q_frigo(3000, -10)


def test_e_frigo_e_scartato():
    assert mh795_e_frigo(750000, 2.5) == 300000.0
    assert mh795_e_frigo(0, 2.5) == 0.0
    assert mh795_q_scartato(750000, 300000.0) == 1050000.0
    assert mh795_q_scartato(0, 0) == 0.0
    assert mh795_q_scartato(750000, 0) == 750000.0
    with pytest.raises(ValueError):
        mh795_e_frigo(750000, 1.0)
    with pytest.raises(ValueError):
        mh795_q_scartato(750000, -1)


def test_q_rec_solo_scartato_frigo():
    assert mh795_q_rec(1050000.0, 0.30) == 315000.0
    assert mh795_q_rec(1050000.0, 0) == 0.0
    assert mh795_q_rec(1050000.0, 1.0) == 1050000.0
    assert mh795_q_rec(0, 0.30) == 0.0
    with pytest.raises(ValueError):
        mh795_q_rec(1050000.0, 1.01)
    with pytest.raises(ValueError):
        mh795_q_rec(1050000.0, -0.1)
    with pytest.raises(ValueError):
        mh795_q_rec(-1, 0.30)


def test_q_risc_res_con_troncamento_a_zero():
    assert mh795_q_risc_res(450000, 315000.0) == 135000.0
    assert mh795_q_risc_res(450000, 450000.0) == 0.0
    assert mh795_q_risc_res(450000, 1050000.0) == 0.0
    with pytest.raises(ValueError):
        mh795_q_risc_res(450000, -1)


def test_gas_e_chiller():
    assert mh795_gas(450000, 0.9) == 500000.0
    assert mh795_gas(0, 0.9) == 0.0
    assert mh795_e_chiller(240000, 3.0) == 80000.0
    assert mh795_e_chiller(0, 3.0) == 0.0
    with pytest.raises(ValueError):
        mh795_gas(450000, 0)
    with pytest.raises(ValueError):
        mh795_gas(450000, 1.01)
    with pytest.raises(ValueError):
        mh795_e_chiller(240000, 1.0)


def test_e_pdc_risc_raff():
    assert mh795_e_pdc_risc(135000.0, 3.8) == pytest.approx(35526.31578947369)
    assert mh795_e_pdc_risc(0, 3.8) == 0.0
    assert mh795_e_pdc_raff(240000, 3.4) == pytest.approx(70588.23529411765)
    assert mh795_e_pdc_raff(0, 3.4) == 0.0
    with pytest.raises(ValueError):
        mh795_e_pdc_risc(135000.0, 1.0)
    with pytest.raises(ValueError):
        mh795_e_pdc_raff(240000, 0.5)


def test_c_base_c_alt_scomposizione():
    assert mh795_c_base(80000, 300000, 250, 500000, 90,
                        30000) == pytest.approx(170000.0)
    assert mh795_c_base(80000, 300000, 250, 500000, 0,
                        30000) == pytest.approx(125000.0)
    assert mh795_c_alt(35526.31578947369, 70588.23529411765, 300000,
                       250, 40000) == pytest.approx(141528.63777089783)
    assert mh795_c_alt(0, 0, 0, 250, 40000) == pytest.approx(40000.0)
    with pytest.raises(ValueError):
        mh795_c_base(80000, 300000, 250, 500000, -1, 30000)
    with pytest.raises(ValueError):
        mh795_c_alt(35526.31578947369, 70588.23529411765, 300000,
                    250, -1)


def test_risparmio_segno():
    assert mh795_risparmio(170000.0, 141528.63777089783) == pytest.approx(28471.362229102175)
    assert mh795_risparmio(141528.63777089783, 141528.63777089783) == 0.0
    assert mh795_risparmio(125000.0, 141528.63777089783) == pytest.approx(-16528.63777089783)


def test_co2_base_alt_evitata():
    assert mh795_co2_base(500000, 0.20, 80000, 300000,
                          0.35) == pytest.approx(233.0)
    assert mh795_co2_alt(35526.31578947369, 70588.23529411765, 300000,
                         0.35) == pytest.approx(142.14009287925694)
    assert mh795_co2_evitata(500000, 0.20, 80000, 300000,
                             35526.31578947369, 70588.23529411765,
                             0.35) == pytest.approx(90.85990712074306)
    assert mh795_co2_base(0, 0.20, 0, 0, 0.35) == pytest.approx(0.0)
    assert mh795_co2_alt(0, 0, 0, 0.35) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh795_co2_base(500000, -0.10, 80000, 300000, 0.35)
    with pytest.raises(ValueError):
        mh795_co2_alt(35526.31578947369, 70588.23529411765, 300000,
                      -0.10)


def test_breakeven_gas_demo_e_varianti():
    assert mh795_breakeven_gas(141528.63777089783, 80000, 300000, 250,
                               30000,
                               500000) == \
        pytest.approx(33.05727554179565)
    assert mh795_breakeven_gas(162252.32198142415, 80000, 300000, 250,
                               30000,
                               500000) == \
        pytest.approx(74.50464396284829)
    assert mh795_breakeven_gas(132647.0588235294, 80000, 300000, 250,
                               30000,
                               500000) == \
        pytest.approx(15.294117647058796)
    assert mh795_breakeven_gas(141528.63777089783, 80000, 300000, 250,
                               30000, 0) is None
    assert mh795_breakeven_gas(200, 80000, 300000, 250, 30000,
                               500000) is None
    with pytest.raises(ValueError):
        mh795_breakeven_gas(141528.63777089783, 80000, 300000, 250,
                            30000, -1)


def test_breakeven_verifica_pareggio():
    bc = _variante(p_gas_eur_mwh=33.05727554179565)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    demo = mh795_demo_calcoli()
    assert (demo["c_alt_eur_anno"]
            - (demo["e_chiller_kwh_anno"] + demo["e_frigo_kwh_anno"])
            / 1000.0
            * demo["p_el_eur_mwh"]
            - demo["om_base_eur_anno"]) * 1000.0 / demo["gas_base_kwh_anno"] == \
        pytest.approx(demo["breakeven_gas_eur_mwh"])


def test_breakeven_soglia_minima():
    be = mh795_demo_calcoli()["breakeven_gas_eur_mwh"]
    assert _variante(p_gas_eur_mwh=be + 1)[
        "c_alt_eur_anno"] < _variante(p_gas_eur_mwh=be + 1)[
        "c_base_eur_anno"]
    assert _variante(p_gas_eur_mwh=be - 1)[
        "c_alt_eur_anno"] > _variante(p_gas_eur_mwh=be - 1)[
        "c_base_eur_anno"]


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh795_flussi(200000, 28471.362229102175, 15)
    assert len(fl) == 16
    assert fl[0] == -200000
    assert all(f == 28471.362229102175 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh795_demo_calcoli()
    assert bc["van"] == pytest.approx(95523.00381925161)
    assert mh795_van([-200000] + [28471.362229102175] * 15,
                     0) == pytest.approx(227070.43343653262)
    assert mh795_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh795_demo_calcoli()
    assert bc["tir"] == pytest.approx(11.426799832343992)
    assert mh795_tir([-200000] + [28471.362229102175] * 15) == \
        pytest.approx(0.11426799832343992)
    tir = mh795_tir([-200000] + [28471.362229102175] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-200000] + [28471.362229102175] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh795_payback([-200000] + [28471.362229102175] * 15) == 8
    assert mh795_payback([-200000] + [-1000.0] * 15) is None
    assert mh795_payback([0] + [28471.362229102175] * 15) == 0
    assert mh795_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh795_verdetto(28471.362229102175, 95523.00381925161, 200000,
                          10.0) == "CONVIENTE"
    assert mh795_verdetto(28471.362229102175, 0.0, 200000, 10.0) == "MARGINALE"
    assert mh795_verdetto(28471.362229102175, -20000.0, 200000, 10.0) == "MARGINALE"
    assert mh795_verdetto(28471.362229102175, -20000.01, 200000, 10.0) == "NON_CONVIENTE"
    assert mh795_verdetto(28471.362229102175, -60171.87, 200000, 10.0) == "NON_CONVIENTE"
    assert mh795_verdetto(0.0, 95523.00381925161, 200000,
                          10.0) == "NON_CALCOLABILE"
    assert mh795_verdetto(-1528.6377708978252, -215866.74, 200000,
                          10.0) == "NON_CALCOLABILE"
    assert mh795_verdetto(None, 95523.00381925161, 200000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh795_verdetto(float("nan"), 95523.00, 200000, 10.0)
    with pytest.raises(ValueError):
        mh795_verdetto(28471.362229102175, 95523.00, -1, 10.0)
    with pytest.raises(ValueError):
        mh795_verdetto(28471.362229102175, 95523.00, 200000, 100.1)


def test_valida_demo_ok():
    v = mh795_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("superficie_m2", "3000"),
                       ("superficie_m2", float("nan")),
                       ("superficie_m2", float("inf")),
                       ("superficie_m2", True),
                       ("p_gas_eur_mwh", None),
                       ("q_risc_kwh_m2_anno", "150")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh795_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("superficie_m2", 0),
                          ("superficie_m2", -10),
                          ("q_risc_kwh_m2_anno", -0.1),
                          ("q_raff_kwh_m2_anno", -0.1),
                          ("q_frigo_kwh_m2_anno", -0.1),
                          ("eta_rec", -0.1),
                          ("eta_rec", 1.01),
                          ("eta_caldaia", 0),
                          ("eta_caldaia", 1.01),
                          ("cop_chiller", 1.0),
                          ("cop_chiller", 0.5),
                          ("cop_frigo", 1.0),
                          ("cop_frigo", 0.5),
                          ("cop_risc", 1.0),
                          ("cop_raff", 1.0),
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
        assert mh795_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"q_risc_kwh_m2_anno": 0,
              "q_raff_kwh_m2_anno": 0,
              "q_frigo_kwh_m2_anno": 0,
              "eta_rec": 0,
              "p_gas_eur_mwh": 0,
              "p_el_eur_mwh": 0,
              "om_base_eur_anno": 0, "om_alt_eur_anno": 0,
              "capex_eur": 0, "wacc_pct": 0,
              "f_gas_t_per_mwh": 0, "f_el_t_per_mwh": 0,
              "tolleranza_pct": 0})
    assert mh795_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["eta_rec"] = 1
    d["q_risc_kwh_m2_anno"] = 150
    assert mh795_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh795_demo()
    assert d["superficie_m2"] == 3000
    assert d["q_risc_kwh_m2_anno"] == 150
    assert d["q_raff_kwh_m2_anno"] == 80
    assert d["q_frigo_kwh_m2_anno"] == 250
    assert d["eta_rec"] == 0.30
    assert d["eta_caldaia"] == 0.90
    assert d["cop_chiller"] == 3.0
    assert d["cop_frigo"] == 2.5
    assert d["cop_risc"] == 3.8
    assert d["cop_raff"] == 3.4
    assert d["p_gas_eur_mwh"] == 90
    assert d["p_el_eur_mwh"] == 250
    assert d["om_base_eur_anno"] == 30000
    assert d["om_alt_eur_anno"] == 40000
    assert d["capex_eur"] == 200000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["f_gas_t_per_mwh"] == 0.20
    assert d["f_el_t_per_mwh"] == 0.35
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    bc = mh795_demo_calcoli()
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
    bc = mh795_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(170000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(141528.63777089783)
    assert bc["risparmio_eur_anno"] == pytest.approx(28471.362229102175)
    assert bc["co2_base_t_anno"] == pytest.approx(233.0)
    assert bc["co2_alt_t_anno"] == pytest.approx(142.14009287925694)
    assert bc["co2_evitata_t_anno"] == pytest.approx(90.85990712074306)
    assert bc["gas_base_kwh_anno"] == pytest.approx(500000.0)


def test_demo_flussi_e_cumulato():
    bc = mh795_demo_calcoli()
    assert bc["flussi"][0] == -200000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(28471.362229102175) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -200000
    assert righe.iloc[4]["Cumulato (EUR)"] == pytest.approx(-86114.5510835913)
    assert righe.iloc[7]["Cumulato (EUR)"] == pytest.approx(-700.4643962847767)
    assert righe.iloc[8]["Cumulato (EUR)"] == pytest.approx(27770.897832817398)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(227070.43343653262)


def test_demo_tabella_righe():
    bc = mh795_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Riscaldamento supermercato (kWh_th/anno)"] == pytest.approx(450000.0)
    assert mappa["Raffrescamento supermercato (kWh_c/anno)"] == pytest.approx(240000.0)
    assert mappa["Carico termico frigo (kWh_th/anno)"] == pytest.approx(750000.0)
    assert mappa["Elettricita' frigo (kWh_e/anno)"] == pytest.approx(300000.0)
    assert mappa["Calore di scarto frigo (kWh_th/anno)"] == pytest.approx(1050000.0)
    assert mappa["Calore recuperato frigo (kWh_th/anno)"] == pytest.approx(315000.0)
    assert mappa["Riscaldamento residuo (kWh_th/anno)"] == pytest.approx(135000.0)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(500000.0)
    assert mappa["Elettricita' chiller (kWh_e/anno)"] == pytest.approx(80000.0)
    assert mappa["Elettricita' pompa di calore riscaldamento (kWh_e/anno)"] == pytest.approx(35526.31578947369)
    assert mappa["Elettricita' pompa di calore raffrescamento (kWh_e/anno)"] == pytest.approx(70588.23529411765)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(170000.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(141528.63777089783)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(28471.362229102175)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(90.85990712074306)
    assert mappa["Payback (anni)"] == 8
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] == \
        pytest.approx(33.05727554179565)


def test_demo_coerenza_interna():
    bc = mh795_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["q_risc_kwh_anno"] == pytest.approx(
        bc["superficie_m2"] * bc["q_risc_kwh_m2_anno"])
    assert bc["q_raff_kwh_anno"] == pytest.approx(
        bc["superficie_m2"] * bc["q_raff_kwh_m2_anno"])
    assert bc["q_frigo_kwh_anno"] == pytest.approx(
        bc["superficie_m2"] * bc["q_frigo_kwh_m2_anno"])
    assert bc["e_frigo_kwh_anno"] == pytest.approx(
        bc["q_frigo_kwh_anno"] / bc["cop_frigo"])
    assert bc["q_scartato_kwh_anno"] == pytest.approx(
        bc["q_frigo_kwh_anno"] + bc["e_frigo_kwh_anno"])
    assert bc["q_rec_kwh_anno"] == pytest.approx(
        bc["eta_rec"] * bc["q_scartato_kwh_anno"])
    assert bc["q_risc_res_kwh_anno"] == pytest.approx(
        max(0.0, bc["q_risc_kwh_anno"] - bc["q_rec_kwh_anno"]))
    assert bc["gas_base_kwh_anno"] == pytest.approx(
        bc["q_risc_kwh_anno"] / bc["eta_caldaia"])
    assert bc["e_chiller_kwh_anno"] == pytest.approx(
        bc["q_raff_kwh_anno"] / bc["cop_chiller"])
    assert bc["e_pdc_risc_kwh_anno"] == pytest.approx(
        bc["q_risc_res_kwh_anno"] / bc["cop_risc"])
    assert bc["e_pdc_raff_kwh_anno"] == pytest.approx(
        bc["q_raff_kwh_anno"] / bc["cop_raff"])
    assert bc["co2_evitata_t_anno"] == pytest.approx(
        bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])
    assert bc["c_base_eur_anno"] == pytest.approx(
        (bc["e_chiller_kwh_anno"] + bc["e_frigo_kwh_anno"])
        / 1000.0 * bc["p_el_eur_mwh"]
        + bc["gas_base_kwh_anno"] / 1000.0 * bc["p_gas_eur_mwh"]
        + bc["om_base_eur_anno"])
    assert bc["c_alt_eur_anno"] == pytest.approx(
        (bc["e_pdc_risc_kwh_anno"] + bc["e_pdc_raff_kwh_anno"]
         + bc["e_frigo_kwh_anno"])
        / 1000.0 * bc["p_el_eur_mwh"]
        + bc["om_alt_eur_anno"])


def test_demo_contro_riconteggio_indipendente():
    s_sup = 3000
    qr_spec, qf_spec, qfr_spec = 150, 80, 250
    erec = 0.30
    eta, copc, copfr, copr, copf = 0.90, 3.0, 2.5, 3.8, 3.4
    pg, pel, omb, oma, cx = 90, 250, 30000, 40000, 200000
    fg, fel, wacc, vita = 0.20, 0.35, 5.0, 15
    qrisc = s_sup * qr_spec
    qraff = s_sup * qf_spec
    qfrigo = s_sup * qfr_spec
    efrigo = qfrigo / copfr
    qscart = qfrigo + efrigo
    qrec = erec * qscart
    qres = max(0.0, qrisc - qrec)
    gas = qrisc / eta
    ech = qraff / copc
    epr = qres / copr
    epf = qraff / copf
    cb = (ech + efrigo) / 1000.0 * pel + gas / 1000.0 * pg + omb
    ca = (epr + epf + efrigo) / 1000.0 * pel + oma
    risp = cb - ca
    co2b = gas / 1000.0 * fg + (ech + efrigo) / 1000.0 * fel
    co2a = (epr + epf + efrigo) / 1000.0 * fel
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    be = (ca - (ech + efrigo) / 1000.0 * pel - omb) * 1000.0 / gas
    bc = mh795_demo_calcoli()
    assert bc["q_risc_kwh_anno"] == pytest.approx(qrisc)
    assert bc["q_raff_kwh_anno"] == pytest.approx(qraff)
    assert bc["q_frigo_kwh_anno"] == pytest.approx(qfrigo)
    assert bc["e_frigo_kwh_anno"] == pytest.approx(efrigo)
    assert bc["q_scartato_kwh_anno"] == pytest.approx(qscart)
    assert bc["q_rec_kwh_anno"] == pytest.approx(qrec)
    assert bc["q_risc_res_kwh_anno"] == pytest.approx(qres)
    assert bc["gas_base_kwh_anno"] == pytest.approx(gas)
    assert bc["e_chiller_kwh_anno"] == pytest.approx(ech)
    assert bc["e_pdc_risc_kwh_anno"] == pytest.approx(epr)
    assert bc["e_pdc_raff_kwh_anno"] == pytest.approx(epf)
    assert bc["c_base_eur_anno"] == pytest.approx(cb)
    assert bc["c_alt_eur_anno"] == pytest.approx(ca)
    assert bc["risparmio_eur_anno"] == pytest.approx(risp)
    assert bc["co2_base_t_anno"] == pytest.approx(co2b)
    assert bc["co2_alt_t_anno"] == pytest.approx(co2a)
    assert bc["co2_evitata_t_anno"] == pytest.approx(co2)
    assert bc["van"] == pytest.approx(van)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(be)


# ---------------------------------------------------------------- varianti
def test_variante_gas_60_non_conviente():
    bc = _variante(p_gas_eur_mwh=60)
    assert bc["risparmio_eur_anno"] == pytest.approx(13471.362229102175)
    assert bc["van"] == pytest.approx(-60171.86675345723)
    assert bc["payback"] == 15
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_gas_30_non_calcolabile():
    bc = _variante(p_gas_eur_mwh=30)
    assert bc["risparmio_eur_anno"] == pytest.approx(-1528.6377708978252)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_gas_zero_non_calcolabile():
    bc = _variante(p_gas_eur_mwh=0)
    assert bc["valid"] is True
    assert bc["c_base_eur_anno"] == pytest.approx(125000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-16528.637770897825)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_senza_recupero_non_conviente():
    bc = _variante(eta_rec=0)
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["q_risc_res_kwh_anno"] == pytest.approx(450000.0)
    assert bc["e_pdc_risc_kwh_anno"] == pytest.approx(118421.05263157895)
    assert bc["risparmio_eur_anno"] == pytest.approx(7747.678018575854)
    assert bc["van"] == pytest.approx(-119581.75157725406)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(74.50464396284829)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_recupero_totale_conviente():
    bc = _variante(eta_rec=1.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(1050000.0)
    assert bc["q_risc_res_kwh_anno"] == 0.0
    assert bc["e_pdc_risc_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(37352.9411764706)
    assert bc["van"] == pytest.approx(187710.75613203982)
    assert bc["payback"] == 6
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(15.294117647058796)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_senza_raffrescamento_conviente():
    bc = _variante(q_raff_kwh_m2_anno=0)
    assert bc["q_raff_kwh_anno"] == 0.0
    assert bc["e_chiller_kwh_anno"] == 0.0
    assert bc["e_pdc_raff_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(26118.421052631573)
    assert bc["van"] == pytest.approx(71100.27902353246)
    assert bc["payback"] == 8
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(37.76315789473686)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_alto_marginale_e_non_conviente():
    bc = _variante(capex_eur=300000)
    assert bc["risparmio_eur_anno"] == pytest.approx(28471.362229102175)
    assert bc["van"] == pytest.approx(-4476.996180748392)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"
    bc2 = _variante(capex_eur=400000)
    assert bc2["van"] == pytest.approx(-104476.99618074839)
    assert bc2["payback"] == 15
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex_eur=0)
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(295523.0038192516, rel=1e-6)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(227070.43343653262)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(19848.312205931376)
    assert bc2["payback"] == 8
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_el_alto_e_cop_risc_basso():
    bc = _variante(p_el_eur_mwh=350)
    assert bc["risparmio_eur_anno"] == pytest.approx(25859.90712074304)
    assert bc["van"] == pytest.approx(68416.99281242397)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(38.28018575851392)
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(cop_risc=2.5)
    assert bc2["e_pdc_risc_kwh_anno"] == pytest.approx(54000.0)
    assert bc2["risparmio_eur_anno"] == pytest.approx(23852.941176470602)
    assert bc2["van"] == pytest.approx(47585.372616601875)
    assert bc2["breakeven_gas_eur_mwh"] == pytest.approx(42.2941176470588)
    assert bc2["payback"] == 9
    assert bc2["verdetto"] == "CONVIENTE"


def test_monotonia_prezzo_gas_crescente():
    base = mh795_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas_eur_mwh=91)["risparmio_eur_anno"]
    basso = _variante(p_gas_eur_mwh=89)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(500.0)
    assert base - basso == pytest.approx(500.0)


def test_monotonia_recupero_crescente_con_tetto():
    assert _variante(eta_rec=0)["risparmio_eur_anno"] < \
        mh795_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(eta_rec=1.0)["risparmio_eur_anno"] > \
        mh795_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(eta_rec=1.0)["q_rec_kwh_anno"] == \
        pytest.approx(1050000.0)
    assert _variante(eta_rec=1.0)["q_risc_res_kwh_anno"] == 0.0


def test_demo_deterministica_due_chiamate():
    a = mh795_demo_calcoli()
    b = mh795_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh795_demo().keys()) == {
        "superficie_m2",
        "q_risc_kwh_m2_anno", "q_raff_kwh_m2_anno",
        "q_frigo_kwh_m2_anno",
        "eta_rec",
        "eta_caldaia", "cop_chiller", "cop_frigo",
        "cop_risc", "cop_raff",
        "p_gas_eur_mwh", "p_el_eur_mwh",
        "om_base_eur_anno", "om_alt_eur_anno",
        "capex_eur", "wacc_pct", "vita_anni",
        "f_gas_t_per_mwh", "f_el_t_per_mwh",
        "tolleranza_pct"}


# ---------------------------------------------------------------- degenere
def test_degenere_cop_uguale_uno_sollevela():
    with pytest.raises(ValueError):
        _variante(cop_risc=1.0)


def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"superficie_m2": 0},
               {"superficie_m2": -10},
               {"q_risc_kwh_m2_anno": -0.1},
               {"q_raff_kwh_m2_anno": -0.1},
               {"q_frigo_kwh_m2_anno": -0.1},
               {"eta_rec": -0.1}, {"eta_rec": 1.01},
               {"eta_caldaia": 0}, {"eta_caldaia": 1.01},
               {"cop_chiller": 1.0}, {"cop_chiller": 0.5},
               {"cop_frigo": 1.0}, {"cop_frigo": 0.5},
               {"cop_risc": 1.0}, {"cop_risc": 0.5},
               {"cop_raff": 1.0}, {"cop_raff": 0.5},
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
        assert mh795_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"superficie_m2": "3000"},
               {"superficie_m2": float("nan")},
               {"p_gas_eur_mwh": float("inf")},
               {"capex_eur": True},
               {"q_risc_kwh_m2_anno": "150"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh795_valida(**d)["valido"] is False


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    for kw in ({"p_gas_eur_mwh": 0},
               {"p_gas_eur_mwh": 33.05727554179565},
               {"p_gas_eur_mwh": 30}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] <= 0.0
        assert bc["verdetto"] == "NON_CALCOLABILE"
        assert bc["flussi"]


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh795_demo_calcoli()
    testo = mh795_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_gas_eur_mwh" in testo
    assert "co2_evitata_t_anno" in testo
    assert "q_raff_kwh_anno" in testo
    assert "q_risc_res_kwh_anno" in testo
    assert "e_chiller_kwh_anno" in testo
    assert "e_frigo_kwh_anno" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh795_demo_calcoli()
    testo = mh795_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"q_risc_kwh_anno;{bc['q_risc_kwh_anno']}" in testo
    assert f"gas_base_kwh_anno;{bc['gas_base_kwh_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh795_demo_calcoli()
    testo = mh795_csv(bc, _demo_kwargs())
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
    return ["mh" + "79" + "4", "st" + "79" + "4",
            "tab" + "79" + "4", "w" + "79" + "5"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w796_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w796_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab795:")


def test_registry_chain_tail_and_count():
    """Registry della nuova tab: il frammento UI apre la tab
    numero 795 (la coda della catena, in append dopo la
    coda precedente che termina a 794, termina con la nuova
    tab e il conteggio atteso delle tab e' 795)."""
    src = _leggi("w796_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 795
    assert src.count("with tab795:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w796_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w796_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st795_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) >= 24
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w796_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 4
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w796_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def795[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w796_ui.py")
        usate = set(re.findall(r'_def795\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 20
        assert usate <= set(mh795_demo().keys())
