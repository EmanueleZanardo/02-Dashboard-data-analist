"""Test tab786 "Palestra: pompa di calore + recupero
calore dalle docce batte la caldaia a gas per acqua
calda e riscaldamento?"
(titolo completo nel frammento UI).
(File repo: tests/test_w786_palestra.py,
contenuto pronto da scrivere in repo.)

Business case deterministico di una palestra
guidata dalle docce/anno degli utenti e dalla
superficie riscaldata in m2: DUE usi termici,
acqua calda sanitaria delle docce +
riscaldamento degli ambienti. Acqua calda
sanitaria Q_acs = D x L x 4,186 x (T_uso - T_in)
/ 3600 kWh_th/anno; riscaldamento Q_risc = S x
q_risc kWh_th/anno; gas baseline G = (Q_acs +
Q_risc) / eta_caldaia kWh/anno; recupero SOLO
sulla frazione acqua calda sanitaria Q_rec =
eta_rec x Q_acs kWh/anno (acque di scarico delle
docce; il riscaldamento ambienti NON e'
recuperabile); calore residuo Q_res = Q_acs +
Q_risc - Q_rec; elettricita' pompa di calore
E_pdc = Q_res / COP_pdc kWh_e/anno; C_base =
G / 1000 x p_gas + O&M_base EUR/anno; C_alt =
E_pdc / 1000 x p_el + O&M_alt EUR/anno
(prezzi EUR/MWh, energie kWh: / 1000 esatto);
risparmio = C_base - C_alt; CO2_base = G / 1000
x f_gas t/anno; CO2_alt = E_pdc / 1000 x f_el
t/anno; CO2_evitata = CO2_base - CO2_alt; flussi
[-CAPEX, risparmio x vita]; VAN, TIR, payback
(primo anno con cumulato >= 0); breakeven gas
p_gas_be = (C_alt - O&M_base) x 1000 / G
EUR/MWh, None se G <= 0 o numeratore < 0,
SOGLIA MINIMA quando esiste. Verdetto:
NON_CALCOLABILE se risparmio <= 0 (guard
degenere: UI salta KPI, grafico, tabella e CSV);
altrimenti CONVIENTE se VAN > 0, MARGINALE se
VAN negativa entro tolleranza % del CAPEX,
NON_CONVIENTE se VAN negativa oltre la
tolleranza. Distinzione esplicita: NON
l'autolavaggio (veicoli, acqua di lavaggio +
aria di asciugatura), NON la lavanderia (panni)
e NON la tab di produzione alimentare con
brassatura e fermentazione: qui il driver sono
le docce/anno degli utenti + la superficie
riscaldata in m2, con DUE usi termici - acqua
calda sanitaria delle docce + riscaldamento
degli ambienti - e il recupero avviene SOLO
sulla frazione acqua calda sanitaria (acque di
scarico delle docce); il riscaldamento ambienti
non e' recuperabile.

Demo (palestra media): D 60.000 docce/anno, L
45 litri/doccia, T_uso 38 e T_in 12 gradi, S
1.000 m2, q_risc 90 kWh_th/m2/anno, caldaia 0,9,
recupero 0,4, COP 3,5, gas 90, el 250 EUR/MWh,
O&M base 3.000, alt 5.000, CAPEX 35.000, WACC
5 %, vita 15, f_gas 0,20, f_el 0,35, tolleranza
10 % del CAPEX. Valori calcolati eseguendo
mh786_demo_calcoli(): Q_acs 81.627, Q_risc
90.000, G 190.696,66666666666, Q_rec
32.650,800000000003, Q_res 138.976,2, E_pdc
39.707,485714285714, C_base 20.162,7, C_alt
14.926,871428571429, risparmio 5.235,828571428572,
CO2_base 38,13933333333333, CO2_alt 13,89762,
CO2_evitata 24,241713333333333, VAN
19.346,110117964177, TIR 12,35219118846879 %,
payback 7, breakeven gas 62,54368068960179,
verdetto CONVIENTE.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w787_helpers import (
    demo_calcoli,
    mh786_breakeven_gas,
    mh786_c_alt,
    mh786_c_base,
    mh786_calcola,
    mh786_co2_alt,
    mh786_co2_base,
    mh786_co2_evitata,
    mh786_cop,
    mh786_csv,
    mh786_demo,
    mh786_demo_calcoli,
    mh786_e_pdc,
    mh786_eta,
    mh786_eta_rec,
    mh786_flussi,
    mh786_gas,
    mh786_int_pos,
    mh786_num,
    mh786_nneg,
    mh786_payback,
    mh786_pct_tolleranza,
    mh786_pct_wacc,
    mh786_pos,
    mh786_q_acs,
    mh786_q_rec,
    mh786_q_res,
    mh786_q_risc,
    mh786_risparmio,
    mh786_t_uso,
    mh786_tir,
    mh786_valida,
    mh786_van,
    mh786_verdetto,
)

_DEMO = {
    "q_acs_kwh_anno": 81627.0,
    "q_risc_kwh_anno": 90000.0,
    "gas_kwh_anno": 190696.66666666666,
    "q_rec_kwh_anno": 32650.800000000003,
    "q_res_kwh_anno": 138976.2,
    "e_pdc_kwh_anno": 39707.485714285714,
    "c_base_eur_anno": 20162.7,
    "c_alt_eur_anno": 14926.871428571429,
    "risparmio_eur_anno": 5235.828571428572,
    "co2_base_t_anno": 38.13933333333333,
    "co2_alt_t_anno": 13.89762,
    "co2_evitata_t_anno": 24.241713333333333,
    "van": 19346.110117964177,
    "tir": 12.35219118846879,
    "breakeven_gas_eur_mwh": 62.54368068960179,
}


def _demo_kwargs():
    return dict(mh786_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh786_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh786_num(3, "x") == 3.0
    assert mh786_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh786_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh786_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh786_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh786_pos(0, "x")
    with pytest.raises(ValueError):
        mh786_pos(-1, "x")
    assert mh786_pos(0.5, "x") == 0.5


def test_cop_maggiore_di_uno():
    assert mh786_cop(3.5, "x") == 3.5
    assert mh786_cop(1.01, "x") == 1.01
    with pytest.raises(ValueError):
        mh786_cop(1.0, "x")
    with pytest.raises(ValueError):
        mh786_cop(0.5, "x")
    with pytest.raises(ValueError):
        mh786_cop(0, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh786_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh786_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh786_int_pos(0, "x")


def test_eta_limiti():
    assert mh786_eta(1.0, "x") == 1.0
    assert mh786_eta(0.9, "x") == 0.9
    with pytest.raises(ValueError):
        mh786_eta(0, "x")
    with pytest.raises(ValueError):
        mh786_eta(1.01, "x")


def test_eta_rec_limiti():
    assert mh786_eta_rec(0.0, "x") == 0.0
    assert mh786_eta_rec(1.0, "x") == 1.0
    assert mh786_eta_rec(0.4, "x") == 0.4
    with pytest.raises(ValueError):
        mh786_eta_rec(-0.1, "x")
    with pytest.raises(ValueError):
        mh786_eta_rec(1.01, "x")


def test_pct_wacc_limiti():
    assert mh786_pct_wacc(0, "x") == 0.0
    assert mh786_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh786_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh786_pct_tolleranza(0, "x") == 0.0
    assert mh786_pct_tolleranza(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh786_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh786_pct_tolleranza(100.1, "x")


def test_t_uso_limiti():
    assert mh786_t_uso(38, 12) == 38.0
    assert mh786_t_uso(100, 12) == 100.0
    with pytest.raises(ValueError):
        mh786_t_uso(12, 12)
    with pytest.raises(ValueError):
        mh786_t_uso(10, 12)
    with pytest.raises(ValueError):
        mh786_t_uso(101, 12)
    with pytest.raises(ValueError):
        mh786_t_uso(38, -1)


# ---------------------------------------------------------------- fisica base
def test_q_acs_formula():
    assert mh786_q_acs(60000, 45, 38, 12) == pytest.approx(81627.0)
    assert mh786_q_acs(30000, 45, 38, 12) == pytest.approx(40813.5)
    assert mh786_q_acs(60000, 40, 38, 12) == pytest.approx(72557.33333333333)
    assert mh786_q_acs(1000, 10, 30, 10) == pytest.approx(232.55555555555557)
    # Il salto termico guida tutto: stesso delta, stessa energia.
    assert mh786_q_acs(1000, 10, 40, 20) == pytest.approx(232.55555555555557)
    with pytest.raises(ValueError):
        mh786_q_acs(0, 45, 38, 12)
    with pytest.raises(ValueError):
        mh786_q_acs(60000.5, 45, 38, 12)
    with pytest.raises(ValueError):
        mh786_q_acs(60000, 0, 38, 12)
    with pytest.raises(ValueError):
        mh786_q_acs(60000, 45, 12, 12)
    with pytest.raises(ValueError):
        mh786_q_acs(60000, 45, 38, -1)


def test_q_risc_gas_rec_res():
    assert mh786_q_risc(1000, 90) == 90000.0
    assert mh786_q_risc(500, 90) == 45000.0
    assert mh786_q_risc(1000, 0) == 0.0
    assert mh786_gas(171627, 0.9) == pytest.approx(190696.66666666666)
    assert mh786_gas(0, 0.9) == 0.0
    assert mh786_q_rec(81627, 0.4) == pytest.approx(32650.8)
    assert mh786_q_rec(81627, 0) == 0.0
    assert mh786_q_rec(81627, 1.0) == 81627.0
    assert mh786_q_res(81627, 90000, 32650.8) == pytest.approx(138976.2)
    assert mh786_q_res(81627, 90000, 0) == 171627.0
    # Il recupero NON tocca il riscaldamento: Q_res
    # cala solo della frazione ACS recuperata.
    assert mh786_q_res(0, 90000, 0) == 90000.0
    with pytest.raises(ValueError):
        mh786_q_risc(0, 90)
    with pytest.raises(ValueError):
        mh786_q_risc(1000, -0.1)
    with pytest.raises(ValueError):
        mh786_gas(171627, 0)
    with pytest.raises(ValueError):
        mh786_gas(171627, 1.01)
    with pytest.raises(ValueError):
        mh786_q_rec(81627, 1.01)
    with pytest.raises(ValueError):
        mh786_q_rec(81627, -0.1)


def test_e_pdc():
    assert mh786_e_pdc(138976.2, 3.5) == pytest.approx(39707.485714285714)
    assert mh786_e_pdc(171627, 3.5) == pytest.approx(49036.28571428572)
    assert mh786_e_pdc(0, 3.5) == 0.0
    with pytest.raises(ValueError):
        mh786_e_pdc(138976.2, 1.0)
    with pytest.raises(ValueError):
        mh786_e_pdc(138976.2, 0.5)


def test_c_base_c_alt_scomposizione():
    assert mh786_c_base(190696.66666666666, 90,
                        3000) == pytest.approx(20162.7)
    assert mh786_c_base(0, 90, 3000) == pytest.approx(3000.0)
    assert mh786_c_alt(39707.485714285714, 250,
                       5000) == pytest.approx(14926.871428571429)
    assert mh786_c_alt(0, 250, 5000) == pytest.approx(5000.0)
    with pytest.raises(ValueError):
        mh786_c_base(190696.66666666666, -1, 3000)
    with pytest.raises(ValueError):
        mh786_c_alt(39707.485714285714, 250, -1)


def test_risparmio_segno():
    assert mh786_risparmio(20162.7, 14926.871428571429) == \
        pytest.approx(5235.828571428572)
    assert mh786_risparmio(14926.871428571429, 14926.871428571429) == 0.0
    assert mh786_risparmio(14441.8, 14926.871428571429) == \
        pytest.approx(-485.071428571429)


def test_co2_base_alt_evitata():
    assert mh786_co2_base(190696.66666666666, 0.20) == \
        pytest.approx(38.13933333333333)
    assert mh786_co2_alt(39707.485714285714, 0.35) == \
        pytest.approx(13.89762)
    assert mh786_co2_evitata(190696.66666666666, 0.20,
                             39707.485714285714,
                             0.35) == pytest.approx(24.241713333333333)
    assert mh786_co2_base(0, 0.20) == 0.0
    assert mh786_co2_alt(0, 0.35) == 0.0
    with pytest.raises(ValueError):
        mh786_co2_base(190696.66666666666, -0.10)
    with pytest.raises(ValueError):
        mh786_co2_alt(39707.485714285714, -0.10)


def test_breakeven_gas_demo_e_varianti():
    assert mh786_breakeven_gas(14926.871428571429, 3000,
                               190696.66666666666) == \
        pytest.approx(62.54368068960179)
    assert mh786_breakeven_gas(18897.62, 3000,
                               190696.66666666666) == \
        pytest.approx(83.3660088447622)
    assert mh786_breakeven_gas(17259.07142857143, 3000,
                               190696.66666666666) == \
        pytest.approx(74.77357458741507)
    assert mh786_breakeven_gas(14926.871428571429, 3000, 0) is None
    # Numeratore negativo: alternativa gia' piu'
    # conveniente a prezzo gas zero -> nessun pareggio.
    assert mh786_breakeven_gas(200, 3000, 190696.66666666666) is None
    with pytest.raises(ValueError):
        mh786_breakeven_gas(14926.871428571429, 3000, -1)


def test_breakeven_verifica_pareggio():
    """Al prezzo gas di pareggio i costi si eguagliano
    e il risparmio e' zero: scatta la guard
    NON_CALCOLABILE, non un verdetto di convenienza."""
    bc = _variante(p_gas_eur_mwh=62.54368068960179)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    demo = mh786_demo_calcoli()
    assert (demo["c_alt_eur_anno"]
            - demo["om_base_eur_anno"]) * 1000.0 / demo["gas_kwh_anno"] == \
        pytest.approx(demo["breakeven_gas_eur_mwh"])


def test_breakeven_soglia_minima():
    """Sopra la soglia l'alternativa vince, sotto perde."""
    be = mh786_demo_calcoli()["breakeven_gas_eur_mwh"]
    assert _variante(p_gas_eur_mwh=be + 1)[
        "c_alt_eur_anno"] < _variante(p_gas_eur_mwh=be + 1)[
        "c_base_eur_anno"]
    assert _variante(p_gas_eur_mwh=be - 1)[
        "c_alt_eur_anno"] > _variante(p_gas_eur_mwh=be - 1)[
        "c_base_eur_anno"]


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh786_flussi(35000, 5235.828571428572, 15)
    assert len(fl) == 16
    assert fl[0] == -35000
    assert all(f == 5235.828571428572 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh786_demo_calcoli()
    assert bc["van"] == pytest.approx(19346.110117964177)
    assert mh786_van([-35000] + [5235.828571428572] * 15,
                     0) == pytest.approx(43537.428571428594)
    assert mh786_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh786_demo_calcoli()
    assert bc["tir"] == pytest.approx(12.35219118846879)
    assert mh786_tir([-35000] + [5235.828571428572] * 15) == \
        pytest.approx(0.1235219118846879)
    tir = mh786_tir([-35000] + [5235.828571428572] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-35000] + [5235.828571428572] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh786_payback([-35000] + [5235.828571428572] * 15) == 7
    assert mh786_payback([-35000] + [-1000.0] * 15) is None
    assert mh786_payback([0] + [5235.828571428572] * 15) == 0
    assert mh786_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh786_verdetto(5235.828571428572, 19346.110117964177, 35000,
                          10.0) == "CONVIENTE"
    assert mh786_verdetto(5235.828571428572, 0.0, 35000, 10.0) == "MARGINALE"
    assert mh786_verdetto(5235.828571428572, -3500.0, 35000, 10.0) == "MARGINALE"
    assert mh786_verdetto(5235.828571428572, -3500.01, 35000, 10.0) == "NON_CONVIENTE"
    assert mh786_verdetto(5235.828571428572, -10344.38, 35000, 10.0) == "NON_CONVIENTE"
    assert mh786_verdetto(0.0, 19346.110117964177, 35000,
                          10.0) == "NON_CALCOLABILE"
    assert mh786_verdetto(-485.071428571429, -40034.88, 35000,
                          10.0) == "NON_CALCOLABILE"
    assert mh786_verdetto(None, 19346.110117964177, 35000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh786_verdetto(float("nan"), 19346.11, 35000, 10.0)
    with pytest.raises(ValueError):
        mh786_verdetto(5235.83, 19346.11, -1, 10.0)
    with pytest.raises(ValueError):
        mh786_verdetto(5235.83, 19346.11, 35000, 100.1)


def test_valida_demo_ok():
    v = mh786_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("docce_anno", "60000"),
                       ("docce_anno", float("nan")),
                       ("docce_anno", float("inf")),
                       ("docce_anno", True),
                       ("p_gas_eur_mwh", None),
                       ("litri_doccia", "45")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh786_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("docce_anno", 0), ("docce_anno", -1),
                          ("docce_anno", 60000.5),
                          ("litri_doccia", 0),
                          ("litri_doccia", -5),
                          ("t_uso_c", 12),
                          ("t_uso_c", 101),
                          ("t_in_c", -1),
                          ("superficie_m2", 0),
                          ("superficie_m2", -10),
                          ("q_risc_kwh_m2_anno", -0.1),
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
        assert mh786_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"q_risc_kwh_m2_anno": 0,
              "eta_rec": 0,
              "p_gas_eur_mwh": 0,
              "p_el_eur_mwh": 0,
              "om_base_eur_anno": 0, "om_alt_eur_anno": 0,
              "capex_eur": 0, "wacc_pct": 0,
              "f_gas_t_per_mwh": 0, "f_el_t_per_mwh": 0,
              "tolleranza_pct": 0})
    assert mh786_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["eta_rec"] = 1
    d["q_risc_kwh_m2_anno"] = 90
    assert mh786_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh786_demo()
    assert d["docce_anno"] == 60000
    assert d["litri_doccia"] == 45
    assert d["t_uso_c"] == 38
    assert d["t_in_c"] == 12
    assert d["superficie_m2"] == 1000
    assert d["q_risc_kwh_m2_anno"] == 90
    assert d["eta_caldaia"] == 0.9
    assert d["eta_rec"] == 0.4
    assert d["cop_pdc"] == 3.5
    assert d["p_gas_eur_mwh"] == 90
    assert d["p_el_eur_mwh"] == 250
    assert d["om_base_eur_anno"] == 3000
    assert d["om_alt_eur_anno"] == 5000
    assert d["capex_eur"] == 35000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["f_gas_t_per_mwh"] == 0.20
    assert d["f_el_t_per_mwh"] == 0.35
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    """Tutti gli output numerici demo a tolleranza
    1e-9 relativa: confronto delle costanti _DEMO
    contro mh786_demo_calcoli()."""
    bc = mh786_demo_calcoli()
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
    bc = mh786_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(20162.7)
    assert bc["c_alt_eur_anno"] == pytest.approx(14926.871428571429)
    assert bc["risparmio_eur_anno"] == pytest.approx(5235.828571428572)
    assert bc["co2_base_t_anno"] == pytest.approx(38.13933333333333)
    assert bc["co2_alt_t_anno"] == pytest.approx(13.89762)
    assert bc["co2_evitata_t_anno"] == pytest.approx(24.241713333333333)
    assert bc["gas_kwh_anno"] == pytest.approx(190696.66666666666)


def test_demo_flussi_e_cumulato():
    bc = mh786_demo_calcoli()
    assert bc["flussi"][0] == -35000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(5235.828571428572) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -35000
    assert righe.iloc[6]["Cumulato (EUR)"] == pytest.approx(-3585.028571428562)
    assert righe.iloc[7]["Cumulato (EUR)"] == pytest.approx(1650.8000000000102)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(43537.428571428594)


def test_demo_tabella_righe():
    bc = mh786_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Acqua calda sanitaria docce (kWh_th/anno)"] == pytest.approx(81627.0)
    assert mappa["Riscaldamento ambienti (kWh_th/anno)"] == pytest.approx(90000.0)
    assert mappa["Calore totale (kWh_th/anno)"] == pytest.approx(171627.0)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(190696.66666666666)
    assert mappa["Calore recuperato dalle docce (kWh/anno)"] == pytest.approx(32650.8)
    assert mappa["Calore residuo (kWh/anno)"] == pytest.approx(138976.2)
    assert mappa["Elettricita' pompa di calore (kWh_e/anno)"] == pytest.approx(39707.485714285714)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(20162.7)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(14926.871428571429)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(5235.828571428572)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(24.241713333333333)
    assert mappa["Payback (anni)"] == 7
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] == \
        pytest.approx(62.54368068960179)


def test_demo_coerenza_interna():
    bc = mh786_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["q_acs_kwh_anno"] == pytest.approx(
        bc["docce_anno"] * bc["litri_doccia"] * 4.186
        * (bc["t_uso_c"] - bc["t_in_c"]) / 3600.0)
    assert bc["q_risc_kwh_anno"] == pytest.approx(
        bc["superficie_m2"] * bc["q_risc_kwh_m2_anno"])
    assert bc["gas_kwh_anno"] == pytest.approx(
        (bc["q_acs_kwh_anno"] + bc["q_risc_kwh_anno"])
        / bc["eta_caldaia"])
    assert bc["q_rec_kwh_anno"] == pytest.approx(
        bc["eta_rec"] * bc["q_acs_kwh_anno"])
    assert bc["q_res_kwh_anno"] == pytest.approx(
        bc["q_acs_kwh_anno"] + bc["q_risc_kwh_anno"]
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
    d, lit, tuso, tin = 60000, 45, 38, 12
    sup, qr_spec = 1000, 90
    eta, erec, copp = 0.9, 0.4, 3.5
    pg, pel, omb, oma, cx = 90, 250, 3000, 5000, 35000
    fg, fel, wacc, vita = 0.20, 0.35, 5.0, 15
    qacs = d * lit * 4.186 * (tuso - tin) / 3600.0
    qrisc = sup * qr_spec
    gas = (qacs + qrisc) / eta
    qrec = erec * qacs
    qres = qacs + qrisc - qrec
    ep = qres / copp
    cb = gas / 1000.0 * pg + omb
    ca = ep / 1000.0 * pel + oma
    risp = cb - ca
    co2b = gas / 1000.0 * fg
    co2a = ep / 1000.0 * fel
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    be = (ca - omb) * 1000.0 / gas
    bc = mh786_demo_calcoli()
    assert bc["q_acs_kwh_anno"] == pytest.approx(qacs)
    assert bc["q_risc_kwh_anno"] == pytest.approx(qrisc)
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
def test_variante_gas_75_risparmio_positivo_ma_non_conviente():
    """Gas 75 EUR/MWh: risparmio ancora positivo
    (2.375,38) ma VAN -10.344,38 oltre la tolleranza
    (3.500): NON_CONVIENTE con payback 15. Il
    verdetto guarda la VAN, non il solo risparmio
    positivo."""
    bc = _variante(p_gas_eur_mwh=75)
    assert bc["risparmio_eur_anno"] == pytest.approx(2375.3785714285714)
    assert bc["van"] == pytest.approx(-10344.3827173495)
    assert bc["payback"] == 15
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_gas_60_non_calcolabile():
    """Gas 60 EUR/MWh: risparmio -485,07, verdetto
    NON_CALCOLABILE, ma helper calcolabili
    (flussi pieni, VAN -40.034,88, TIR None,
    payback None)."""
    bc = _variante(p_gas_eur_mwh=60)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(-485.07142857142935)
    assert bc["van"] == pytest.approx(-40034.87555266318)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_gas_40_non_calcolabile():
    bc = _variante(p_gas_eur_mwh=40)
    assert bc["risparmio_eur_anno"] == pytest.approx(-4299.004761904762)
    assert bc["van"] == pytest.approx(-79622.19933308139)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_capex_alto_marginale_e_non_conviente():
    bc = _variante(capex_eur=55000)
    assert bc["risparmio_eur_anno"] == pytest.approx(5235.828571428572)
    assert bc["van"] == pytest.approx(-653.8898820358249)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"
    bc2 = _variante(capex_eur=65000)
    assert bc2["van"] == pytest.approx(-10653.889882035837)
    assert bc2["payback"] == 13
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex_eur=0)
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(54346.110117964185, rel=1e-6)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(43537.428571428594)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(5429.680363223816)
    assert bc2["payback"] == 7
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_el_alto_non_conviente():
    """Elettricita' 350 EUR/MWh: risparmio 1.265,08,
    VAN -21.868,90 oltre la tolleranza (3.500):
    NON_CONVIENTE, payback None, breakeven gas
    83,37 (sale perche' l'alternativa elettrica
    costa di piu')."""
    bc = _variante(p_el_eur_mwh=350)
    assert bc["risparmio_eur_anno"] == pytest.approx(1265.079999999998)
    assert bc["van"] == pytest.approx(-21868.90220905852)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(83.3660088447622)


def test_variante_senza_recupero_non_conviente():
    """Senza recupero (eta_rec zero): calore residuo
    171.627, E_pdc 49.036,29, risparmio 2.903,63,
    VAN -4.861,33, breakeven 74,77, NON_CONVIENTE.
    Il recupero sulle docce e' decisivo: il
    riscaldamento resta interamente a carico della
    pompa di calore in entrambi i casi."""
    bc = _variante(eta_rec=0)
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["q_res_kwh_anno"] == pytest.approx(171627.0)
    assert bc["e_pdc_kwh_anno"] == pytest.approx(49036.28571428572)
    assert bc["risparmio_eur_anno"] == pytest.approx(2903.628571428573)
    assert bc["van"] == pytest.approx(-4861.328358680579)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(74.77357458741507)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_cop_basso_non_conviente():
    """COP pompa di calore 2,5 invece di 3,5:
    E_pdc 55.590,48, risparmio 1.265,08,
    VAN -21.868,90, breakeven 83,37,
    NON_CONVIENTE."""
    bc = _variante(cop_pdc=2.5)
    assert bc["e_pdc_kwh_anno"] == pytest.approx(55590.48)
    assert bc["risparmio_eur_anno"] == pytest.approx(1265.079999999998)
    assert bc["van"] == pytest.approx(-21868.90220905852)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(83.3660088447622)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_docce_dimezzate():
    """Docce 30.000/anno: l'acqua calda sanitaria si
    dimezza (40.813,50), il riscaldamento resta
    90.000, il risparmio scende a 2.903,63, la
    VAN e' -4.861,33, NON_CONVIENTE (il CAPEX non
    si dimezza, e il breakeven sale a 70,02 perche'
    gli O&M fissi pesano di piu')."""
    bc = _variante(docce_anno=30000)
    assert bc["q_acs_kwh_anno"] == pytest.approx(40813.5)
    assert bc["q_risc_kwh_anno"] == pytest.approx(90000.0)
    assert bc["gas_kwh_anno"] == pytest.approx(145348.33333333334)
    assert bc["q_rec_kwh_anno"] == pytest.approx(16325.400000000001)
    assert bc["risparmio_eur_anno"] == pytest.approx(2903.6285714285714)
    assert bc["van"] == pytest.approx(-4861.328358680608)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(70.02296617485416)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_superficie_dimezzata_conviente():
    """Superficie 500 m2: riscaldamento 45.000,
    risparmio 3.950,11, VAN 6.000,84 ancora
    positiva, CONVIENTE con payback 9 e breakeven
    61,92: le docce restano 60.000 e reggono il
    caso anche con meta' riscaldamento."""
    bc = _variante(superficie_m2=500)
    assert bc["q_risc_kwh_anno"] == pytest.approx(45000.0)
    assert bc["gas_kwh_anno"] == pytest.approx(140696.66666666666)
    assert bc["q_res_kwh_anno"] == pytest.approx(93976.2)
    assert bc["e_pdc_kwh_anno"] == pytest.approx(26850.342857142856)
    assert bc["risparmio_eur_anno"] == pytest.approx(3950.114285714286)
    assert bc["van"] == pytest.approx(6000.835497446268)
    assert bc["payback"] == 9
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(61.924606465107296)
    assert bc["verdetto"] == "CONVIENTE"


def test_monotonia_prezzo_gas_crescente():
    base = mh786_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas_eur_mwh=91)["risparmio_eur_anno"]
    basso = _variante(p_gas_eur_mwh=89)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(190.69666666666672)
    assert base - basso == pytest.approx(190.69666666666672)


def test_monotonia_docce_crescente():
    """Il risparmio cresce con le docce (meno O&M
    fissi per doccia) finche' i vettori crescono."""
    assert _variante(docce_anno=30000)["risparmio_eur_anno"] < \
        mh786_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(docce_anno=120000)["risparmio_eur_anno"] > \
        mh786_demo_calcoli()["risparmio_eur_anno"]


def test_demo_deterministica_due_chiamate():
    a = mh786_demo_calcoli()
    b = mh786_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh786_demo().keys()) == {
        "docce_anno", "litri_doccia",
        "t_uso_c", "t_in_c",
        "superficie_m2", "q_risc_kwh_m2_anno",
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
    for kw in ({"docce_anno": 0}, {"docce_anno": -1},
               {"docce_anno": 60000.5},
               {"litri_doccia": 0},
               {"litri_doccia": -5},
               {"t_uso_c": 12},
               {"t_uso_c": 101},
               {"t_in_c": -1},
               {"superficie_m2": 0},
               {"superficie_m2": -10},
               {"q_risc_kwh_m2_anno": -0.1},
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
        assert mh786_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"docce_anno": "60000"},
               {"docce_anno": float("nan")},
               {"p_gas_eur_mwh": float("inf")},
               {"capex_eur": True},
               {"litri_doccia": "45"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh786_valida(**d)["valido"] is False


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    """Differenza chiave: risparmio <= 0 NON solleva
    negli helper (resta calcolabile con flussi, VAN,
    TIR e payback), ma il verdetto e' NON_CALCOLABILE
    e la UI salta KPI, grafico, tabella e CSV."""
    for kw in ({"p_gas_eur_mwh": 60},
               {"p_gas_eur_mwh": 62.54368068960179}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] <= 0.0
        assert bc["verdetto"] == "NON_CALCOLABILE"
        assert bc["flussi"]


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh786_demo_calcoli()
    testo = mh786_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_gas_eur_mwh" in testo
    assert "co2_evitata_t_anno" in testo
    assert "q_acs_kwh_anno" in testo
    assert "q_risc_kwh_anno" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh786_demo_calcoli()
    testo = mh786_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"q_acs_kwh_anno;{bc['q_acs_kwh_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh786_demo_calcoli()
    testo = mh786_csv(bc, _demo_kwargs())
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
    return ["mh" + "78" + "5", "st" + "78" + "5",
            "tab" + "78" + "5"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w787_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w787_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab786:")


def test_registry_chain_tail_and_count():
    """Registry della nuova tab: il frammento UI apre la tab
    numero 786 (la coda della catena termina con la nuova tab
    e il conteggio atteso delle tab e' 786)."""
    src = _leggi("w787_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 786
    assert src.count("with tab786:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w787_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w787_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st786_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) >= 19
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w787_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 2
    # Entrambe le guard (input degenere e risparmio <= 0)
    # stanno prima di KPI / grafico / tabella / CSV.
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w787_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def786[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w787_ui.py")
        usate = set(re.findall(r'_def786\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 19
        assert usate <= set(mh786_demo().keys())
