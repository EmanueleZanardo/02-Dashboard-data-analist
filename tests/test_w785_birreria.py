"""Test tab785 "Birreria: scaldare il mosto con pompa di
calore + recupero calore dal raffreddamento batte
caldaia a gas + chiller tradizionale?"
(titolo completo nel frammento UI).
(File repo: tests/test_w785_birreria.py,
contenuto pronto da scrivere in repo.)

Business case deterministico di una birreria
guidata dagli hl/anno di birra: DUE carichi,
calore di brassatura/bollitura del mosto +
freddo di fermentazione/conservazione. Calore
Q_boll = V x q_boll kWh_th/anno; freddo
Q_freddo = V x q_freddo kWh_f/anno; gas baseline
G = Q_boll / eta_caldaia kWh/anno; recupero dal
raffreddamento del mosto Q_rec = eta_rec x
Q_boll kWh/anno (preriscalda l'acqua di
brassatura successiva); calore residuo Q_res =
Q_boll - Q_rec; elettricita' pompa di calore
E_pdc = Q_res / COP_pdc; freddo base
E_freddo_base = Q_freddo / EER_base e freddo
alternativo E_freddo_alt = Q_freddo / EER_alt
kWh_e/anno (il freddo resta elettrico in
entrambi i casi, cambia solo l'EER); C_base =
G / 1000 x p_gas + E_freddo_base / 1000 x p_el
+ O&M_base EUR/anno; C_alt = (E_pdc +
E_freddo_alt) / 1000 x p_el + O&M_alt EUR/anno
(prezzi EUR/MWh, energie kWh: / 1000 esatto);
risparmio = C_base - C_alt; CO2_base = G / 1000
x f_gas + E_freddo_base / 1000 x f_el t/anno;
CO2_alt = (E_pdc + E_freddo_alt) / 1000 x f_el
t/anno; CO2_evitata = CO2_base - CO2_alt; flussi
[-CAPEX, risparmio x vita]; VAN, TIR, payback
(primo anno con cumulato >= 0); breakeven gas
p_gas_be = ((E_pdc + E_freddo_alt -
E_freddo_base) / 1000 x p_el + O&M_alt -
O&M_base) / (G / 1000) EUR/MWh, None se
G <= 0 o numeratore < 0, SOGLIA MINIMA quando
esiste. Verdetto: NON_CALCOLABILE se risparmio
<= 0 (guard degenere: UI salta KPI, grafico,
tabella e CSV); altrimenti CONVIENTE se VAN > 0,
MARGINALE se VAN negativa entro tolleranza %
del CAPEX, NON_CONVIENTE se VAN negativa oltre
la tolleranza. Distinzione esplicita: NON la
distilleria (distillazione), NON la cantina
vinicola (vino, geotermia reversibile), NON la
gelateria (pastorizzazione + freddo alimentare):
qui il driver sono gli hl/anno di birra, con DUE
carichi - calore di brassatura/bollitura del
mosto + freddo di fermentazione/conservazione -
e il recupero avviene sul raffreddamento del
mosto (preriscalda l'acqua di brassatura
successiva); il freddo resta elettrico in
entrambi i casi ma con EER diverso (chiller
tradizionale vs efficiente).

Demo (birreria media): V 5.000 hl/anno, q_boll
35 kWh_th/hl, q_freddo 12 kWh_f/hl, caldaia 0,9,
recupero 0,35, COP 3,2, EER base 2,8, EER alt
4,0, gas 90, el 250 EUR/MWh, O&M base 4.000,
alt 6.000, CAPEX 60.000, WACC 5 %, vita 15,
f_gas 0,20, f_el 0,35, tolleranza 10 % del
CAPEX. Valori calcolati eseguendo
mh785_demo_calcoli(): Q_boll 175.000, Q_freddo
60.000, G 194.444,44444444444, Q_rec 61.250,
Q_res 113.750, E_pdc 35.546,875, E_freddo_base
21.428,57142857143, E_freddo_alt 15.000, C_base
26.857,14285714286, C_alt 18.636,71875,
risparmio 8.220,424107142859, CO2_base
46,388888888888886, CO2_alt 17,69140625,
CO2_evitata 28,697482638888886, VAN
25.325,191160958875, TIR 10,73110222999736 %,
payback 8, breakeven gas 47,7235331632653,
verdetto CONVIENTE.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w786_helpers import (
    demo_calcoli,
    mh785_breakeven_gas,
    mh785_c_alt,
    mh785_c_base,
    mh785_calcola,
    mh785_co2_alt,
    mh785_co2_base,
    mh785_co2_evitata,
    mh785_cop,
    mh785_csv,
    mh785_demo,
    mh785_demo_calcoli,
    mh785_e_freddo,
    mh785_e_pdc,
    mh785_eta,
    mh785_eta_rec,
    mh785_flussi,
    mh785_gas,
    mh785_int_pos,
    mh785_num,
    mh785_nneg,
    mh785_payback,
    mh785_pct_tolleranza,
    mh785_pct_wacc,
    mh785_pos,
    mh785_q_boll,
    mh785_q_freddo,
    mh785_q_rec,
    mh785_q_res,
    mh785_risparmio,
    mh785_tir,
    mh785_valida,
    mh785_van,
    mh785_verdetto,
)

_DEMO = {
    "q_boll_kwh_anno": 175000.0,
    "q_freddo_kwh_anno": 60000.0,
    "gas_kwh_anno": 194444.44444444444,
    "q_rec_kwh_anno": 61249.99999999999,
    "q_res_kwh_anno": 113750.0,
    "e_pdc_kwh_anno": 35546.875,
    "e_freddo_base_kwh_anno": 21428.57142857143,
    "e_freddo_alt_kwh_anno": 15000.0,
    "c_base_eur_anno": 26857.14285714286,
    "c_alt_eur_anno": 18636.71875,
    "risparmio_eur_anno": 8220.424107142859,
    "co2_base_t_anno": 46.388888888888886,
    "co2_alt_t_anno": 17.69140625,
    "co2_evitata_t_anno": 28.697482638888886,
    "van": 25325.191160958875,
    "tir": 10.73110222999736,
    "breakeven_gas_eur_mwh": 47.7235331632653,
}


def _demo_kwargs():
    return dict(mh785_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh785_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh785_num(3, "x") == 3.0
    assert mh785_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh785_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh785_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh785_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh785_pos(0, "x")
    with pytest.raises(ValueError):
        mh785_pos(-1, "x")
    assert mh785_pos(0.5, "x") == 0.5


def test_cop_maggiore_di_uno():
    assert mh785_cop(3.2, "x") == 3.2
    assert mh785_cop(1.01, "x") == 1.01
    with pytest.raises(ValueError):
        mh785_cop(1.0, "x")
    with pytest.raises(ValueError):
        mh785_cop(0.5, "x")
    with pytest.raises(ValueError):
        mh785_cop(0, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh785_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh785_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh785_int_pos(0, "x")


def test_eta_limiti():
    assert mh785_eta(1.0, "x") == 1.0
    assert mh785_eta(0.9, "x") == 0.9
    with pytest.raises(ValueError):
        mh785_eta(0, "x")
    with pytest.raises(ValueError):
        mh785_eta(1.01, "x")


def test_eta_rec_limiti():
    assert mh785_eta_rec(0.0, "x") == 0.0
    assert mh785_eta_rec(1.0, "x") == 1.0
    assert mh785_eta_rec(0.35, "x") == 0.35
    with pytest.raises(ValueError):
        mh785_eta_rec(-0.1, "x")
    with pytest.raises(ValueError):
        mh785_eta_rec(1.01, "x")


def test_pct_wacc_limiti():
    assert mh785_pct_wacc(0, "x") == 0.0
    assert mh785_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh785_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh785_pct_tolleranza(0, "x") == 0.0
    assert mh785_pct_tolleranza(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh785_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh785_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_q_boll_q_freddo_gas_rec_res():
    assert mh785_q_boll(5000, 35) == 175000.0
    assert mh785_q_boll(2500, 35) == 87500.0
    assert mh785_q_freddo(5000, 12) == 60000.0
    assert mh785_q_freddo(5000, 0) == 0.0
    assert mh785_gas(175000, 0.9) == pytest.approx(194444.44444444444)
    assert mh785_gas(0, 0.9) == 0.0
    assert mh785_q_rec(175000, 0.35) == pytest.approx(61250.0)
    assert mh785_q_rec(175000, 0) == 0.0
    assert mh785_q_rec(175000, 1.0) == 175000.0
    assert mh785_q_res(175000, 61250.0) == pytest.approx(113750.0)
    assert mh785_q_res(175000, 0) == 175000.0
    with pytest.raises(ValueError):
        mh785_q_boll(0, 35)
    with pytest.raises(ValueError):
        mh785_q_boll(5000.5, 35)
    with pytest.raises(ValueError):
        mh785_q_boll(5000, 0)
    with pytest.raises(ValueError):
        mh785_q_freddo(5000, -0.1)
    with pytest.raises(ValueError):
        mh785_gas(175000, 0)
    with pytest.raises(ValueError):
        mh785_gas(175000, 1.01)
    with pytest.raises(ValueError):
        mh785_q_rec(175000, 1.01)
    with pytest.raises(ValueError):
        mh785_q_rec(175000, -0.1)


def test_e_pdc_e_freddo():
    assert mh785_e_pdc(113750, 3.2) == pytest.approx(35546.875)
    assert mh785_e_pdc(175000, 3.2) == pytest.approx(54687.5)
    assert mh785_e_pdc(0, 3.2) == 0.0
    assert mh785_e_freddo(60000, 2.8) == pytest.approx(21428.57142857143)
    assert mh785_e_freddo(60000, 4.0) == 15000.0
    assert mh785_e_freddo(0, 2.8) == 0.0
    with pytest.raises(ValueError):
        mh785_e_pdc(113750, 1.0)
    with pytest.raises(ValueError):
        mh785_e_pdc(113750, 0.5)
    with pytest.raises(ValueError):
        mh785_e_freddo(60000, 0)
    with pytest.raises(ValueError):
        mh785_e_freddo(60000, -2.0)


def test_c_base_c_alt_scomposizione():
    assert mh785_c_base(194444.44444444444, 21428.57142857143, 90, 250,
                        4000) == pytest.approx(26857.14285714286)
    assert mh785_c_base(194444.44444444444, 0, 90, 250,
                        4000) == pytest.approx(21500.0)
    assert mh785_c_base(0, 0, 90, 250, 4000) == pytest.approx(4000.0)
    assert mh785_c_alt(35546.875, 15000, 250,
                       6000) == pytest.approx(18636.71875)
    assert mh785_c_alt(0, 0, 250, 6000) == pytest.approx(6000.0)
    with pytest.raises(ValueError):
        mh785_c_base(194444.44444444444, 21428.57142857143, -1, 250, 4000)
    with pytest.raises(ValueError):
        mh785_c_alt(35546.875, 15000, 250, -1)


def test_risparmio_segno():
    assert mh785_risparmio(26857.14285714286, 18636.71875) == \
        pytest.approx(8220.424107142859)
    assert mh785_risparmio(18636.71875, 18636.71875) == 0.0
    assert mh785_risparmio(17134.920634920636, 18636.71875) == \
        pytest.approx(-1501.798115079364)


def test_co2_base_alt_evitata():
    assert mh785_co2_base(194444.44444444444, 21428.57142857143, 0.20,
                          0.35) == pytest.approx(46.388888888888886)
    assert mh785_co2_alt(35546.875, 15000,
                         0.35) == pytest.approx(17.69140625)
    assert mh785_co2_evitata(194444.44444444444, 21428.57142857143,
                             0.20, 35546.875, 15000,
                             0.35) == pytest.approx(28.697482638888886)
    # Il freddo resta elettrico in entrambi i casi:
    # la CO2 dipende da G e dalle elettricita', che
    # invece dipendono da Q_rec e dagli EER.
    assert mh785_co2_base(0, 0, 0.20, 0.35) == 0.0
    assert mh785_co2_alt(0, 0, 0.35) == 0.0
    with pytest.raises(ValueError):
        mh785_co2_base(194444.44444444444, 21428.57142857143, -0.10, 0.35)
    with pytest.raises(ValueError):
        mh785_co2_alt(35546.875, 15000, -0.10)


def test_breakeven_gas_demo_e_varianti():
    assert mh785_breakeven_gas(35546.875, 15000, 21428.57142857143, 250,
                               6000, 4000,
                               194444.44444444444) == \
        pytest.approx(47.7235331632653)
    assert mh785_breakeven_gas(35546.875, 15000, 21428.57142857143, 400,
                               6000, 4000,
                               194444.44444444444) == \
        pytest.approx(70.18622448979592)
    assert mh785_breakeven_gas(54687.5, 15000, 21428.57142857143, 250,
                               6000, 4000,
                               194444.44444444444) == \
        pytest.approx(72.3329081632653)
    assert mh785_breakeven_gas(35546.875, 15000, 21428.57142857143, 250,
                               6000, 4000, 0) is None
    # Numeratore negativo: alternativa gia' piu'
    # conveniente a prezzo gas zero -> nessun pareggio.
    assert mh785_breakeven_gas(1000.0, 15000, 21428.57142857143, 250,
                               100, 4000,
                               194444.44444444444) is None
    with pytest.raises(ValueError):
        mh785_breakeven_gas(35546.875, 15000, 21428.57142857143, 250,
                            6000, 4000, -1)


def test_breakeven_verifica_pareggio():
    """Al prezzo gas di pareggio i costi si eguagliano
    e il risparmio e' zero: scatta la guard
    NON_CALCOLABILE, non un verdetto di convenienza."""
    bc = _variante(p_gas_eur_mwh=47.7235331632653)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    demo = mh785_demo_calcoli()
    assert ((demo["e_pdc_kwh_anno"]
             + demo["e_freddo_alt_kwh_anno"]
             - demo["e_freddo_base_kwh_anno"]) / 1000.0
            * demo["p_el_eur_mwh"]
            + demo["om_alt_eur_anno"]
            - demo["om_base_eur_anno"]) == pytest.approx(
        demo["gas_kwh_anno"] / 1000.0
        * demo["breakeven_gas_eur_mwh"])


def test_breakeven_soglia_minima():
    """Sopra la soglia l'alternativa vince, sotto perde."""
    be = mh785_demo_calcoli()["breakeven_gas_eur_mwh"]
    assert _variante(p_gas_eur_mwh=be + 1)[
        "c_alt_eur_anno"] < _variante(p_gas_eur_mwh=be + 1)[
        "c_base_eur_anno"]
    assert _variante(p_gas_eur_mwh=be - 1)[
        "c_alt_eur_anno"] > _variante(p_gas_eur_mwh=be - 1)[
        "c_base_eur_anno"]


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh785_flussi(60000, 8220.424107142859, 15)
    assert len(fl) == 16
    assert fl[0] == -60000
    assert all(f == 8220.424107142859 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh785_demo_calcoli()
    assert bc["van"] == pytest.approx(25325.191160958875)
    assert mh785_van([-60000] + [8220.424107142859] * 15,
                     0) == pytest.approx(63306.361607142855)
    assert mh785_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh785_demo_calcoli()
    assert bc["tir"] == pytest.approx(10.73110222999736)
    assert mh785_tir([-60000] + [8220.424107142859] * 15) == \
        pytest.approx(0.1073110222999736)
    tir = mh785_tir([-60000] + [8220.424107142859] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-60000] + [8220.424107142859] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh785_payback([-60000] + [8220.424107142859] * 15) == 8
    assert mh785_payback([-60000] + [-1000.0] * 15) is None
    assert mh785_payback([0] + [8220.424107142859] * 15) == 0
    assert mh785_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh785_verdetto(8220.424107142859, 25325.191160958875, 60000,
                          10.0) == "CONVIENTE"
    assert mh785_verdetto(8220.424107142859, 0.0, 60000, 10.0) == "MARGINALE"
    assert mh785_verdetto(8220.424107142859, -6000.0, 60000, 10.0) == "MARGINALE"
    assert mh785_verdetto(8220.424107142859, -6000.01, 60000, 10.0) == "NON_CONVIENTE"
    assert mh785_verdetto(8220.424107142859, -35222.81, 60000, 10.0) == "NON_CONVIENTE"
    assert mh785_verdetto(0.0, 25325.191160958875, 60000,
                          10.0) == "NON_CALCOLABILE"
    assert mh785_verdetto(-1501.798115079364, -75588.15, 60000,
                          10.0) == "NON_CALCOLABILE"
    assert mh785_verdetto(None, 25325.191160958875, 60000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh785_verdetto(float("nan"), 25325.19, 60000, 10.0)
    with pytest.raises(ValueError):
        mh785_verdetto(8220.42, 25325.19, -1, 10.0)
    with pytest.raises(ValueError):
        mh785_verdetto(8220.42, 25325.19, 60000, 100.1)


def test_valida_demo_ok():
    v = mh785_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("v_hl_anno", "5000"),
                       ("v_hl_anno", float("nan")),
                       ("v_hl_anno", float("inf")),
                       ("v_hl_anno", True),
                       ("p_gas_eur_mwh", None),
                       ("q_boll_kwh_per_hl", "35")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh785_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("v_hl_anno", 0), ("v_hl_anno", -1),
                          ("v_hl_anno", 5000.5),
                          ("q_boll_kwh_per_hl", 0),
                          ("q_boll_kwh_per_hl", -5),
                          ("q_freddo_kwh_per_hl", -0.1),
                          ("eta_caldaia", 0),
                          ("eta_caldaia", 1.01),
                          ("eta_rec", -0.1),
                          ("eta_rec", 1.01),
                          ("cop_pdc", 1.0),
                          ("cop_pdc", 0.5),
                          ("eer_base", 0),
                          ("eer_base", -2.0),
                          ("eer_alt", 0),
                          ("eer_alt", -4.0),
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
        assert mh785_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"q_freddo_kwh_per_hl": 0,
              "eta_rec": 0,
              "p_gas_eur_mwh": 0,
              "p_el_eur_mwh": 0,
              "om_base_eur_anno": 0, "om_alt_eur_anno": 0,
              "capex_eur": 0, "wacc_pct": 0,
              "f_gas_t_per_mwh": 0, "f_el_t_per_mwh": 0,
              "tolleranza_pct": 0})
    assert mh785_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["eta_rec"] = 1
    d["q_freddo_kwh_per_hl"] = 12
    assert mh785_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh785_demo()
    assert d["v_hl_anno"] == 5000
    assert d["q_boll_kwh_per_hl"] == 35
    assert d["q_freddo_kwh_per_hl"] == 12
    assert d["eta_caldaia"] == 0.9
    assert d["eta_rec"] == 0.35
    assert d["cop_pdc"] == 3.2
    assert d["eer_base"] == 2.8
    assert d["eer_alt"] == 4.0
    assert d["p_gas_eur_mwh"] == 90
    assert d["p_el_eur_mwh"] == 250
    assert d["om_base_eur_anno"] == 4000
    assert d["om_alt_eur_anno"] == 6000
    assert d["capex_eur"] == 60000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["f_gas_t_per_mwh"] == 0.20
    assert d["f_el_t_per_mwh"] == 0.35
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    """Tutti gli output numerici demo a tolleranza
    1e-9 relativa: confronto delle costanti _DEMO
    contro mh785_demo_calcoli()."""
    bc = mh785_demo_calcoli()
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
    bc = mh785_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(26857.14285714286)
    assert bc["c_alt_eur_anno"] == pytest.approx(18636.71875)
    assert bc["risparmio_eur_anno"] == pytest.approx(8220.424107142859)
    assert bc["co2_base_t_anno"] == pytest.approx(46.388888888888886)
    assert bc["co2_alt_t_anno"] == pytest.approx(17.69140625)
    assert bc["co2_evitata_t_anno"] == pytest.approx(28.697482638888886)
    assert bc["gas_kwh_anno"] == pytest.approx(194444.44444444444)


def test_demo_flussi_e_cumulato():
    bc = mh785_demo_calcoli()
    assert bc["flussi"][0] == -60000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(8220.424107142859) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -60000
    assert righe.iloc[7]["Cumulato (EUR)"] == pytest.approx(-2457.03125)
    assert righe.iloc[8]["Cumulato (EUR)"] == pytest.approx(5763.392857142859)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(63306.361607142855)


def test_demo_tabella_righe():
    bc = mh785_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Calore brassatura/bollitura (kWh_th/anno)"] == pytest.approx(175000.0)
    assert mappa["Freddo fermentazione/conservazione (kWh_f/anno)"] == pytest.approx(60000.0)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(194444.44444444444)
    assert mappa["Calore recuperato dal mosto (kWh/anno)"] == pytest.approx(61250.0)
    assert mappa["Calore residuo (kWh/anno)"] == pytest.approx(113750.0)
    assert mappa["Elettricita' pompa di calore (kWh_e/anno)"] == pytest.approx(35546.875)
    assert mappa["Elettricita' freddo base (kWh_e/anno)"] == pytest.approx(21428.57142857143)
    assert mappa["Elettricita' freddo alternativo (kWh_e/anno)"] == pytest.approx(15000.0)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(26857.14285714286)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(18636.71875)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(8220.424107142859)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(28.697482638888886)
    assert mappa["Payback (anni)"] == 8
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] == \
        pytest.approx(47.7235331632653)


def test_demo_coerenza_interna():
    bc = mh785_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["q_boll_kwh_anno"] == pytest.approx(
        bc["v_hl_anno"] * bc["q_boll_kwh_per_hl"])
    assert bc["q_freddo_kwh_anno"] == pytest.approx(
        bc["v_hl_anno"] * bc["q_freddo_kwh_per_hl"])
    assert bc["gas_kwh_anno"] == pytest.approx(
        bc["q_boll_kwh_anno"] / bc["eta_caldaia"])
    assert bc["q_rec_kwh_anno"] == pytest.approx(
        bc["eta_rec"] * bc["q_boll_kwh_anno"])
    assert bc["q_res_kwh_anno"] == pytest.approx(
        bc["q_boll_kwh_anno"] - bc["q_rec_kwh_anno"])
    assert bc["e_pdc_kwh_anno"] == pytest.approx(
        bc["q_res_kwh_anno"] / bc["cop_pdc"])
    assert bc["e_freddo_base_kwh_anno"] == pytest.approx(
        bc["q_freddo_kwh_anno"] / bc["eer_base"])
    assert bc["e_freddo_alt_kwh_anno"] == pytest.approx(
        bc["q_freddo_kwh_anno"] / bc["eer_alt"])
    assert bc["co2_evitata_t_anno"] == pytest.approx(
        bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])
    assert bc["c_base_eur_anno"] == pytest.approx(
        bc["gas_kwh_anno"] / 1000.0 * bc["p_gas_eur_mwh"]
        + bc["e_freddo_base_kwh_anno"] / 1000.0
        * bc["p_el_eur_mwh"]
        + bc["om_base_eur_anno"])
    assert bc["c_alt_eur_anno"] == pytest.approx(
        (bc["e_pdc_kwh_anno"] + bc["e_freddo_alt_kwh_anno"])
        / 1000.0 * bc["p_el_eur_mwh"]
        + bc["om_alt_eur_anno"])


def test_demo_contro_riconteggio_indipendente():
    v, qb_spec, qf_spec = 5000, 35, 12
    eta, erec, copp, eerb, eera = 0.9, 0.35, 3.2, 2.8, 4.0
    pg, pel, omb, oma, cx = 90, 250, 4000, 6000, 60000
    fg, fel, wacc, vita = 0.20, 0.35, 5.0, 15
    qboll = v * qb_spec
    qfred = v * qf_spec
    gas = qboll / eta
    qrec = erec * qboll
    qres = qboll - qrec
    ep = qres / copp
    efb = qfred / eerb
    efa = qfred / eera
    cb = gas / 1000.0 * pg + efb / 1000.0 * pel + omb
    ca = (ep + efa) / 1000.0 * pel + oma
    risp = cb - ca
    co2b = gas / 1000.0 * fg + efb / 1000.0 * fel
    co2a = (ep + efa) / 1000.0 * fel
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    be = ((ep + efa - efb) / 1000.0 * pel + oma - omb) / (gas / 1000.0)
    bc = mh785_demo_calcoli()
    assert bc["q_boll_kwh_anno"] == pytest.approx(qboll)
    assert bc["q_freddo_kwh_anno"] == pytest.approx(qfred)
    assert bc["gas_kwh_anno"] == pytest.approx(gas)
    assert bc["q_rec_kwh_anno"] == pytest.approx(qrec)
    assert bc["q_res_kwh_anno"] == pytest.approx(qres)
    assert bc["e_pdc_kwh_anno"] == pytest.approx(ep)
    assert bc["e_freddo_base_kwh_anno"] == pytest.approx(efb)
    assert bc["e_freddo_alt_kwh_anno"] == pytest.approx(efa)
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
    (2.387,09) ma VAN -35.222,81 oltre la tolleranza
    (6.000): NON_CONVIENTE. Il verdetto guarda la
    VAN, non il solo risparmio positivo."""
    bc = _variante(p_gas_eur_mwh=60)
    assert bc["risparmio_eur_anno"] == pytest.approx(2387.090773809523)
    assert bc["van"] == pytest.approx(-35222.814061761266)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_gas_40_non_calcolabile():
    """Gas 40 EUR/MWh: risparmio -1.501,80, verdetto
    NON_CALCOLABILE, ma helper calcolabili
    (flussi pieni, VAN -75.588,15, TIR None,
    payback None)."""
    bc = _variante(p_gas_eur_mwh=40)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(-1501.798115079364)
    assert bc["van"] == pytest.approx(-75588.150876908)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_capex_alto_marginale_e_non_conviente():
    bc = _variante(capex_eur=90000)
    assert bc["risparmio_eur_anno"] == pytest.approx(8220.424107142859)
    assert bc["van"] == pytest.approx(-4674.808839041125)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"
    bc2 = _variante(capex_eur=100000)
    assert bc2["van"] == pytest.approx(-14674.808839041127)
    assert bc2["payback"] == 13
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex_eur=0)
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(85325.19116095889, rel=1e-6)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(63306.361607142855)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(3475.9359608378736)
    assert bc2["payback"] == 8
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_el_alto_non_conviente():
    """Elettricita' 400 EUR/MWh: risparmio 3.852,68,
    VAN -20.010,51 oltre la tolleranza (6.000):
    NON_CONVIENTE, payback None, breakeven gas
    70,19 (sale perche' l'alternativa elettrica
    costa di piu')."""
    bc = _variante(p_el_eur_mwh=400)
    assert bc["risparmio_eur_anno"] == pytest.approx(3852.6785714285725)
    assert bc["van"] == pytest.approx(-20010.513897545294)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(70.18622448979592)


def test_variante_senza_recupero_non_conviente():
    """Senza recupero (eta_rec zero): calore residuo
    175.000, E_pdc 54.687,50, risparmio 3.435,27,
    VAN -24.343,09, breakeven 72,33, NON_CONVIENTE.
    Il recupero sul raffreddamento del mosto e'
    decisivo."""
    bc = _variante(eta_rec=0)
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["q_res_kwh_anno"] == pytest.approx(175000.0)
    assert bc["e_pdc_kwh_anno"] == pytest.approx(54687.5)
    assert bc["risparmio_eur_anno"] == pytest.approx(3435.2678571428587)
    assert bc["van"] == pytest.approx(-24343.09437330372)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(72.3329081632653)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_cop_basso_marginale():
    """COP pompa di calore 2,5 invece di 3,2:
    E_pdc 45.500, risparmio 5.732,14,
    VAN -502,32 entro la tolleranza (6.000),
    breakeven 60,52, payback 11,
    MARGINALE."""
    bc = _variante(cop_pdc=2.5)
    assert bc["e_pdc_kwh_anno"] == pytest.approx(45500.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(5732.142857142859)
    assert bc["van"] == pytest.approx(-502.3173168576809)
    assert bc["payback"] == 11
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(60.5204081632653)
    assert bc["verdetto"] == "MARGINALE"


def test_variante_produzione_dimezzata():
    """Produzione 2.500 hl/anno: tutti i vettori si
    dimezzano, il risparmio scende a 3.110,21, la
    VAN e' -27.717,06, NON_CONVIENTE (il CAPEX non
    si dimezza, e il breakeven sale a 58,01 perche'
    gli O&M fissi pesano di piu')."""
    bc = _variante(v_hl_anno=2500)
    assert bc["q_boll_kwh_anno"] == pytest.approx(87500.0)
    assert bc["q_freddo_kwh_anno"] == pytest.approx(30000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(3110.2120535714294)
    assert bc["van"] == pytest.approx(-27717.06245770115)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(58.009247448979586)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_freddo_stesso_eer():
    """EER alternativo uguale al base (2,8): il
    vantaggio sul freddo sparisce, ma il caso
    resta CONVIENTE con risparmio 6.613,28, VAN
    8.643,60 e breakeven 55,99."""
    bc = _variante(eer_alt=2.8)
    assert bc["e_freddo_alt_kwh_anno"] == pytest.approx(21428.57142857143)
    assert bc["risparmio_eur_anno"] == pytest.approx(6613.28125)
    assert bc["van"] == pytest.approx(8643.597885311476)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(55.98883928571429)
    assert bc["verdetto"] == "CONVIENTE"


def test_monotonia_prezzo_gas_crescente():
    base = mh785_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas_eur_mwh=91)["risparmio_eur_anno"]
    basso = _variante(p_gas_eur_mwh=89)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(194.44444444444446)
    assert base - basso == pytest.approx(194.44444444444446)


def test_monotonia_produzione_crescente():
    """Il risparmio cresce con la produzione (meno O&M
    fissi per hl) finche' i vettori crescono."""
    assert _variante(v_hl_anno=2500)["risparmio_eur_anno"] < \
        mh785_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(v_hl_anno=10000)["risparmio_eur_anno"] > \
        mh785_demo_calcoli()["risparmio_eur_anno"]


def test_demo_deterministica_due_chiamate():
    a = mh785_demo_calcoli()
    b = mh785_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh785_demo().keys()) == {
        "v_hl_anno", "q_boll_kwh_per_hl",
        "q_freddo_kwh_per_hl",
        "eta_caldaia", "eta_rec", "cop_pdc",
        "eer_base", "eer_alt",
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
    for kw in ({"v_hl_anno": 0}, {"v_hl_anno": -1},
               {"v_hl_anno": 5000.5},
               {"q_boll_kwh_per_hl": 0},
               {"q_boll_kwh_per_hl": -5},
               {"q_freddo_kwh_per_hl": -0.1},
               {"eta_caldaia": 0}, {"eta_caldaia": 1.01},
               {"eta_rec": -0.1}, {"eta_rec": 1.01},
               {"cop_pdc": 1.0}, {"cop_pdc": 0.5},
               {"eer_base": 0}, {"eer_base": -2.0},
               {"eer_alt": 0}, {"eer_alt": -4.0},
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
        assert mh785_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"v_hl_anno": "5000"},
               {"v_hl_anno": float("nan")},
               {"p_gas_eur_mwh": float("inf")},
               {"capex_eur": True},
               {"q_boll_kwh_per_hl": "35"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh785_valida(**d)["valido"] is False


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    """Differenza chiave: risparmio <= 0 NON solleva
    negli helper (resta calcolabile con flussi, VAN,
    TIR e payback), ma il verdetto e' NON_CALCOLABILE
    e la UI salta KPI, grafico, tabella e CSV."""
    for kw in ({"p_gas_eur_mwh": 40},
               {"p_gas_eur_mwh": 47.7235331632653}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] <= 0.0
        assert bc["verdetto"] == "NON_CALCOLABILE"
        assert bc["flussi"]


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh785_demo_calcoli()
    testo = mh785_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_gas_eur_mwh" in testo
    assert "co2_evitata_t_anno" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh785_demo_calcoli()
    testo = mh785_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"q_boll_kwh_anno;{bc['q_boll_kwh_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh785_demo_calcoli()
    testo = mh785_csv(bc, _demo_kwargs())
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
    return ["mh" + "78" + "4", "st" + "78" + "4",
            "tab" + "78" + "4"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w786_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w786_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab785:")


def test_registry_chain_tail_and_count():
    """Registry della nuova tab: il frammento UI apre la tab
    numero 785 (la coda della catena termina con la nuova tab
    e il conteggio atteso delle tab e' 785)."""
    src = _leggi("w786_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 785
    assert src.count("with tab785:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w786_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w786_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st785_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) >= 19
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w786_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 2
    # Entrambe le guard (input degenere e risparmio <= 0)
    # stanno prima di KPI / grafico / tabella / CSV.
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w786_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def785[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w786_ui.py")
        usate = set(re.findall(r'_def785\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 18
        assert usate <= set(mh785_demo().keys())
