"""Test nuova scheda "Biblioteca: pompa di
calore reversibile + recupero calore dalla
ventilazione sale lettura batte caldaia a gas
+ chiller?"
(titolo completo nel frammento UI).
Contenuto pronto da scrivere in repo come test
della scheda biblioteca.

Business case deterministico di una biblioteca
guidata dalla SUPERFICIE delle sale lettura in
m2 per riscaldamento E raffrescamento.
Riscaldamento sale lettura Q_risc = S_sale x
q_risc kWh_th/anno (q_risc kWh_th/m2/anno);
raffrescamento stesse sale lettura Q_raff =
S_sale x q_raff kWh_c/anno (stessa superficie:
le sale lettura sono le stesse); gas baseline
G_base = Q_risc / eta_caldaia kWh/anno;
elettricita' chiller E_chiller = Q_raff /
COP_chiller kWh_e/anno; elettricita' pompa di
calore in riscaldamento E_pdc_risc = Q_risc /
COP_pdc_risc kWh_e/anno; in raffrescamento
E_pdc_raff = Q_raff / COP_pdc_raff kWh_e/anno;
C_base = E_chiller / 1000 x p_el + G_base /
1000 x p_gas + O&M_base EUR/anno; C_alt =
(E_pdc_risc + E_pdc_raff) / 1000 x p_el +
O&M_alt EUR/anno (prezzi EUR/MWh, energie kWh:
 / 1000 esatto); risparmio = C_base - C_alt;
CO2_base = G_base / 1000 x f_gas + E_chiller /
1000 x f_el t/anno; CO2_alt = (E_pdc_risc +
E_pdc_raff) / 1000 x f_el t/anno; CO2_evitata =
CO2_base - CO2_alt; flussi [-CAPEX, risparmio x
vita]; VAN, TIR, payback (primo anno con
cumulato >= 0); breakeven gas p_gas_be =
(C_alt - E_chiller / 1000 x p_el - O&M_base) x
1000 / G_base EUR/MWh, None se G_base <= 0 o
numeratore < 0, SOGLIA MINIMA quando esiste.
Verdetto: NON_CALCOLABILE se risparmio <= 0
(guard degenere: UI salta KPI, grafico, tabella
e CSV); altrimenti CONVIENTE se VAN > 0,
MARGINALE se VAN negativa entro tolleranza %
del CAPEX, NON_CONVIENTE se VAN negativa oltre
la tolleranza. Distinzione esplicita: distinto
dal supermercato (superficie di vendita, banchi
frigo, recupero sul riscaldamento), dal
ristorante (coperti, ACS, celle frigo, recupero
su ACS), dall'albergo (pernottamento, ACS docce
ospiti), dalla scuola (aule + mensa, chiusure
stagionali scolastiche), dall'ospedale (reparti
24h, ventilazione di reparto, ACS posti letto),
dalla palestra (docce utenti) e dalla piscina
(vasca riscaldata), dal teatro/cinema (sala
spettacolo, affollamento serale) e dal centro
logistico (magazzino volumetrico in m3, uffici
SOLO per il raffrescamento): qui driver
SUPERFICIE = m2 di sale lettura per
riscaldamento E raffrescamento, occupazione
diurna continuativa, recupero dalla ventilazione
delle sale lettura; niente ACS, niente celle
frigo, niente recupero dai banchi o dalle celle.

Demo (biblioteca): 2000 m2 di sale lettura a
120 kWh_th/m2/anno di riscaldamento e 60
kWh_c/m2/anno di raffrescamento, caldaia 0,90,
chiller COP 3,0, pompa di calore COP
riscaldamento 3,4 e COP raffrescamento 3,8,
gas 90, el 250 EUR/MWh, O&M base 8.000, alt
10.000, CAPEX 60.000, WACC 5 %, vita 15,
f_gas 0,20, f_el 0,35, tolleranza 10 % del
CAPEX. Valori calcolati eseguendo
mh798_demo_calcoli(): Q_risc 240.000, Q_raff
120.000, G_base 266.666,6666666667, E_chiller
40.000, E_pdc_risc 70.588,23529411765, E_pdc_raff
31.578,947368421053, C_base 42.000, C_alt
35.541,79566563468, risparmio 6.458,20433436532,
CO2_base 67,33333333333334, CO2_alt
35,758513931888544, CO2_evitata
31,5748194014448, VAN 7.033,9525314077255, TIR
6,687395527965288 %, payback 10, breakeven gas
65,78173374613004, verdetto CONVIENTE.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w799_helpers import (
    demo_calcoli,
    mh798_breakeven_gas,
    mh798_c_alt,
    mh798_c_base,
    mh798_calcola,
    mh798_co2_alt,
    mh798_co2_base,
    mh798_co2_evitata,
    mh798_cop,
    mh798_csv,
    mh798_demo,
    mh798_demo_calcoli,
    mh798_e_chiller,
    mh798_e_pdc_raff,
    mh798_e_pdc_risc,
    mh798_eta,
    mh798_flussi,
    mh798_gas,
    mh798_int_pos,
    mh798_num,
    mh798_nneg,
    mh798_payback,
    mh798_pct_tolleranza,
    mh798_pct_wacc,
    mh798_pos,
    mh798_q_raff,
    mh798_q_risc,
    mh798_risparmio,
    mh798_tir,
    mh798_valida,
    mh798_van,
    mh798_verdetto,
)

_DEMO = {
    "q_risc_kwh_anno": 240000.0,
    "q_raff_kwh_anno": 120000.0,
    "gas_base_kwh_anno": 266666.6666666667,
    "e_chiller_kwh_anno": 40000.0,
    "e_pdc_risc_kwh_anno": 70588.23529411765,
    "e_pdc_raff_kwh_anno": 31578.947368421053,
    "c_base_eur_anno": 42000.0,
    "c_alt_eur_anno": 35541.79566563468,
    "risparmio_eur_anno": 6458.20433436532,
    "co2_base_t_anno": 67.33333333333334,
    "co2_alt_t_anno": 35.758513931888544,
    "co2_evitata_t_anno": 31.5748194014448,
    "van": 7033.9525314077255,
    "tir": 6.687395527965288,
    "breakeven_gas_eur_mwh": 65.78173374613004,
}


def _demo_kwargs():
    return dict(mh798_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh798_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh798_num(3, "x") == 3.0
    assert mh798_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh798_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh798_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh798_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh798_pos(0, "x")
    with pytest.raises(ValueError):
        mh798_pos(-1, "x")
    assert mh798_pos(0.5, "x") == 0.5


def test_cop_maggiore_di_uno():
    assert mh798_cop(3.4, "x") == 3.4
    assert mh798_cop(1.01, "x") == 1.01
    with pytest.raises(ValueError):
        mh798_cop(1.0, "x")
    with pytest.raises(ValueError):
        mh798_cop(0.5, "x")
    with pytest.raises(ValueError):
        mh798_cop(0, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh798_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh798_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh798_int_pos(0, "x")


def test_eta_limiti():
    assert mh798_eta(1.0, "x") == 1.0
    assert mh798_eta(0.9, "x") == 0.9
    with pytest.raises(ValueError):
        mh798_eta(0, "x")
    with pytest.raises(ValueError):
        mh798_eta(1.01, "x")


def test_pct_wacc_limiti():
    assert mh798_pct_wacc(0, "x") == 0.0
    assert mh798_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh798_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh798_pct_tolleranza(0, "x") == 0.0
    assert mh798_pct_tolleranza(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh798_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh798_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_q_risc_q_raff_stessa_superficie():
    assert mh798_q_risc(2000, 120) == 240000.0
    assert mh798_q_risc(2000, 0) == 0.0
    assert mh798_q_raff(2000, 60) == 120000.0
    assert mh798_q_raff(2000, 0) == 0.0
    assert mh798_q_raff(1000, 60) == 60000.0
    with pytest.raises(ValueError):
        mh798_q_risc(0, 120)
    with pytest.raises(ValueError):
        mh798_q_risc(2000, -1)
    with pytest.raises(ValueError):
        mh798_q_raff(2000, -10)
    with pytest.raises(ValueError):
        mh798_q_raff(0, 60)


def test_gas_e_chiller():
    assert mh798_gas(240000, 0.9) == pytest.approx(266666.6666666667)
    assert mh798_gas(0, 0.9) == 0.0
    assert mh798_e_chiller(120000, 3.0) == pytest.approx(40000.0)
    assert mh798_e_chiller(0, 3.0) == 0.0
    with pytest.raises(ValueError):
        mh798_gas(240000, 0)
    with pytest.raises(ValueError):
        mh798_gas(240000, 1.01)
    with pytest.raises(ValueError):
        mh798_e_chiller(120000, 1.0)


def test_e_pdc_risc_raff():
    assert mh798_e_pdc_risc(240000, 3.4) == pytest.approx(70588.23529411765)
    assert mh798_e_pdc_risc(0, 3.4) == 0.0
    assert mh798_e_pdc_raff(120000, 3.8) == pytest.approx(31578.947368421053)
    assert mh798_e_pdc_raff(0, 3.8) == 0.0
    with pytest.raises(ValueError):
        mh798_e_pdc_risc(240000, 1.0)
    with pytest.raises(ValueError):
        mh798_e_pdc_raff(120000, 0.5)


def test_c_base_c_alt_scomposizione():
    assert mh798_c_base(40000.0, 250,
                        266666.6666666667, 90,
                        8000) == pytest.approx(42000.0)
    assert mh798_c_base(40000.0, 250,
                        266666.6666666667, 0,
                        8000) == pytest.approx(18000.0)
    assert mh798_c_alt(70588.23529411765, 31578.947368421053, 250,
                       10000) == pytest.approx(35541.79566563468)
    assert mh798_c_alt(0, 0, 250, 10000) == pytest.approx(10000.0)
    with pytest.raises(ValueError):
        mh798_c_base(40000.0, 250,
                     266666.6666666667, -1, 8000)
    with pytest.raises(ValueError):
        mh798_c_alt(70588.23529411765, 31578.947368421053, 250, -1)


def test_risparmio_segno():
    assert mh798_risparmio(42000.0, 35541.79566563468) == pytest.approx(6458.20433436532)
    assert mh798_risparmio(35541.79566563468, 35541.79566563468) == 0.0
    assert mh798_risparmio(34000.0, 35541.79566563468) == pytest.approx(-1541.7956656346796)


def test_co2_base_alt_evitata():
    assert mh798_co2_base(266666.6666666667, 0.20, 40000.0,
                          0.35) == pytest.approx(67.33333333333334)
    assert mh798_co2_alt(70588.23529411765, 31578.947368421053,
                         0.35) == pytest.approx(35.758513931888544)
    assert mh798_co2_evitata(266666.6666666667, 0.20,
                             40000.0,
                             70588.23529411765, 31578.947368421053,
                             0.35) == pytest.approx(31.5748194014448)
    assert mh798_co2_base(0, 0.20, 0, 0.35) == pytest.approx(0.0)
    assert mh798_co2_alt(0, 0, 0.35) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh798_co2_base(266666.6666666667, -0.10, 40000.0,
                       0.35)
    with pytest.raises(ValueError):
        mh798_co2_alt(70588.23529411765, 31578.947368421053, -0.10)


def test_breakeven_gas_demo_e_varianti():
    assert mh798_breakeven_gas(35541.79566563468, 40000.0,
                               250, 8000,
                               266666.6666666667) == \
        pytest.approx(65.78173374613004)
    assert mh798_breakeven_gas(27647.058823529413, 0,
                               250, 8000,
                               266666.6666666667) == \
        pytest.approx(73.67647058823529)
    assert mh798_breakeven_gas(39323.308270676695, 40000.0,
                               250, 8000,
                               266666.6666666667) == \
        pytest.approx(79.9624060150376)
    assert mh798_breakeven_gas(35541.79566563468, 40000.0,
                               250, 8000, 0) is None
    assert mh798_breakeven_gas(200, 40000.0,
                               250, 8000,
                               266666.6666666667) is None
    with pytest.raises(ValueError):
        mh798_breakeven_gas(35541.79566563468, 40000.0,
                            250, 8000, -1)


def test_breakeven_verifica_pareggio():
    bc = _variante(p_gas_eur_mwh=65.78173374613004)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    # Al pareggio esatto il risparmio e' zero a meno di
    # arrotondamento floating point (qui 0.0 esatto,
    # quindi guard NON_CALCOLABILE; con +1e-11 la VAN
    # resterebbe circa -60.000, quindi NON_CONVIENTE):
    # in nessun caso CONVIENTE.
    assert bc["verdetto"] in ("NON_CALCOLABILE", "NON_CONVIENTE")
    sotto = _variante(p_gas_eur_mwh=65.78)
    assert sotto["risparmio_eur_anno"] == pytest.approx(-0.4623323013438494)
    assert sotto["risparmio_eur_anno"] < 0.0
    assert sotto["verdetto"] == "NON_CALCOLABILE"
    demo = mh798_demo_calcoli()
    assert (demo["c_alt_eur_anno"]
            - demo["e_chiller_kwh_anno"] / 1000.0
            * demo["p_el_eur_mwh"]
            - demo["om_base_eur_anno"]) * 1000.0 / demo["gas_base_kwh_anno"] == \
        pytest.approx(demo["breakeven_gas_eur_mwh"])


def test_breakeven_soglia_minima():
    be = mh798_demo_calcoli()["breakeven_gas_eur_mwh"]
    assert _variante(p_gas_eur_mwh=be + 1)[
        "c_alt_eur_anno"] < _variante(p_gas_eur_mwh=be + 1)[
        "c_base_eur_anno"]
    assert _variante(p_gas_eur_mwh=be - 1)[
        "c_alt_eur_anno"] > _variante(p_gas_eur_mwh=be - 1)[
        "c_base_eur_anno"]


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh798_flussi(60000, 6458.20433436532, 15)
    assert len(fl) == 16
    assert fl[0] == -60000
    assert all(f == 6458.20433436532 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh798_demo_calcoli()
    assert bc["van"] == pytest.approx(7033.9525314077255)
    assert mh798_van([-60000] + [6458.20433436532] * 15,
                     0) == pytest.approx(36873.065015479806)
    assert mh798_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh798_demo_calcoli()
    assert bc["tir"] == pytest.approx(6.687395527965288)
    assert mh798_tir([-60000] + [6458.20433436532] * 15) == \
        pytest.approx(0.06687395527965288)
    tir = mh798_tir([-60000] + [6458.20433436532] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-60000] + [6458.20433436532] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh798_payback([-60000] + [6458.20433436532] * 15) == 10
    assert mh798_payback([-60000] + [-1000.0] * 15) is None
    assert mh798_payback([0] + [6458.20433436532] * 15) == 0
    assert mh798_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh798_verdetto(6458.20433436532, 7033.9525314077255, 60000,
                          10.0) == "CONVIENTE"
    assert mh798_verdetto(6458.20433436532, 0.0, 60000, 10.0) == "MARGINALE"
    assert mh798_verdetto(6458.20433436532, -6000.0, 60000, 10.0) == "MARGINALE"
    assert mh798_verdetto(6458.20433436532, -6000.01, 60000, 10.0) == "NON_CONVIENTE"
    assert mh798_verdetto(6458.20433436532, -32216.86, 60000, 10.0) == "NON_CONVIENTE"
    assert mh798_verdetto(0.0, 7033.9525314077255, 60000,
                          10.0) == "NON_CALCOLABILE"
    assert mh798_verdetto(-1541.7956656346796, -76003.31, 60000,
                          10.0) == "NON_CALCOLABILE"
    assert mh798_verdetto(None, 7033.9525314077255, 60000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh798_verdetto(float("nan"), 7033.95, 60000, 10.0)
    with pytest.raises(ValueError):
        mh798_verdetto(6458.20433436532, 7033.95, -1, 10.0)
    with pytest.raises(ValueError):
        mh798_verdetto(6458.20433436532, 7033.95, 60000, 100.1)


def test_valida_demo_ok():
    v = mh798_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("s_sale_m2", "2000"),
                       ("s_sale_m2", float("nan")),
                       ("s_sale_m2", float("inf")),
                       ("s_sale_m2", True),
                       ("p_gas_eur_mwh", None),
                       ("q_risc_kwh_th_m2_anno", "120")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh798_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("s_sale_m2", 0),
                          ("s_sale_m2", -10),
                          ("q_risc_kwh_th_m2_anno", -0.1),
                          ("q_raff_kwh_c_m2_anno", -0.1),
                          ("eta_caldaia", 0),
                          ("eta_caldaia", 1.01),
                          ("cop_chiller", 1.0),
                          ("cop_chiller", 0.5),
                          ("cop_pdc_risc", 1.0),
                          ("cop_pdc_raff", 1.0),
                          ("cop_pdc_raff", 0.5),
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
        assert mh798_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"q_risc_kwh_th_m2_anno": 0,
              "q_raff_kwh_c_m2_anno": 0,
              "p_gas_eur_mwh": 0,
              "p_el_eur_mwh": 0,
              "om_base_eur_anno": 0, "om_alt_eur_anno": 0,
              "capex_eur": 0, "wacc_pct": 0,
              "f_gas_t_per_mwh": 0, "f_el_t_per_mwh": 0,
              "tolleranza_pct": 0})
    assert mh798_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["q_risc_kwh_th_m2_anno"] = 120
    assert mh798_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh798_demo()
    assert d["s_sale_m2"] == 2000
    assert d["q_risc_kwh_th_m2_anno"] == 120
    assert d["q_raff_kwh_c_m2_anno"] == 60
    assert d["eta_caldaia"] == 0.90
    assert d["cop_chiller"] == 3.0
    assert d["cop_pdc_risc"] == 3.4
    assert d["cop_pdc_raff"] == 3.8
    assert d["p_gas_eur_mwh"] == 90
    assert d["p_el_eur_mwh"] == 250
    assert d["om_base_eur_anno"] == 8000
    assert d["om_alt_eur_anno"] == 10000
    assert d["capex_eur"] == 60000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["f_gas_t_per_mwh"] == 0.20
    assert d["f_el_t_per_mwh"] == 0.35
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    bc = mh798_demo_calcoli()
    for chiave, atteso in _DEMO.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert got == pytest.approx(atteso, rel=1e-9), chiave
    assert bc["payback"] == 10
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True
    assert demo_calcoli()["van"] == bc["van"]


def test_demo_calcoli_fisica_economia():
    bc = mh798_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(42000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(35541.79566563468)
    assert bc["risparmio_eur_anno"] == pytest.approx(6458.20433436532)
    assert bc["co2_base_t_anno"] == pytest.approx(67.33333333333334)
    assert bc["co2_alt_t_anno"] == pytest.approx(35.758513931888544)
    assert bc["co2_evitata_t_anno"] == pytest.approx(31.5748194014448)
    assert bc["gas_base_kwh_anno"] == pytest.approx(266666.6666666667)


def test_demo_flussi_e_cumulato():
    bc = mh798_demo_calcoli()
    assert bc["flussi"][0] == -60000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(6458.20433436532) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -60000
    assert righe.iloc[9]["Cumulato (EUR)"] == pytest.approx(-1876.160990712116)
    assert righe.iloc[10]["Cumulato (EUR)"] == pytest.approx(4582.043343653204)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(36873.065015479806)


def test_demo_tabella_righe():
    bc = mh798_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Superficie sale lettura (m2)"] == pytest.approx(2000.0)
    assert mappa["Riscaldamento sale lettura (kWh_th/anno)"] == pytest.approx(240000.0)
    assert mappa["Raffrescamento sale lettura (kWh_c/anno)"] == pytest.approx(120000.0)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(266666.6666666667)
    assert mappa["Elettricita' chiller (kWh_e/anno)"] == pytest.approx(40000.0)
    assert mappa["Elettricita' pompa di calore riscaldamento (kWh_e/anno)"] == pytest.approx(70588.23529411765)
    assert mappa["Elettricita' pompa di calore raffrescamento (kWh_e/anno)"] == pytest.approx(31578.947368421053)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(42000.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(35541.79566563468)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(6458.20433436532)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(31.5748194014448)
    assert mappa["Payback (anni)"] == 10
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] == \
        pytest.approx(65.78173374613004)


def test_demo_coerenza_interna():
    bc = mh798_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["q_risc_kwh_anno"] == pytest.approx(
        bc["s_sale_m2"] * bc["q_risc_kwh_th_m2_anno"])
    assert bc["q_raff_kwh_anno"] == pytest.approx(
        bc["s_sale_m2"] * bc["q_raff_kwh_c_m2_anno"])
    assert bc["gas_base_kwh_anno"] == pytest.approx(
        bc["q_risc_kwh_anno"] / bc["eta_caldaia"])
    assert bc["e_chiller_kwh_anno"] == pytest.approx(
        bc["q_raff_kwh_anno"] / bc["cop_chiller"])
    assert bc["e_pdc_risc_kwh_anno"] == pytest.approx(
        bc["q_risc_kwh_anno"] / bc["cop_pdc_risc"])
    assert bc["e_pdc_raff_kwh_anno"] == pytest.approx(
        bc["q_raff_kwh_anno"] / bc["cop_pdc_raff"])
    assert bc["co2_evitata_t_anno"] == pytest.approx(
        bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])
    assert bc["c_base_eur_anno"] == pytest.approx(
        bc["e_chiller_kwh_anno"] / 1000.0 * bc["p_el_eur_mwh"]
        + bc["gas_base_kwh_anno"] / 1000.0 * bc["p_gas_eur_mwh"]
        + bc["om_base_eur_anno"])
    assert bc["c_alt_eur_anno"] == pytest.approx(
        (bc["e_pdc_risc_kwh_anno"] + bc["e_pdc_raff_kwh_anno"])
        / 1000.0 * bc["p_el_eur_mwh"]
        + bc["om_alt_eur_anno"])


def test_demo_contro_riconteggio_indipendente():
    s_sale = 2000
    qr_spec, qf_spec = 120, 60
    eta, copc, copr, copf = 0.90, 3.0, 3.4, 3.8
    pg, pel, omb, oma, cx = 90, 250, 8000, 10000, 60000
    fg, fel, wacc, vita = 0.20, 0.35, 5.0, 15
    qrisc = s_sale * qr_spec
    qraff = s_sale * qf_spec
    gas = qrisc / eta
    ech = qraff / copc
    epr = qrisc / copr
    epf = qraff / copf
    cb = ech / 1000.0 * pel + gas / 1000.0 * pg + omb
    ca = (epr + epf) / 1000.0 * pel + oma
    risp = cb - ca
    co2b = gas / 1000.0 * fg + ech / 1000.0 * fel
    co2a = (epr + epf) / 1000.0 * fel
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    be = (ca - ech / 1000.0 * pel - omb) * 1000.0 / gas
    bc = mh798_demo_calcoli()
    assert bc["q_risc_kwh_anno"] == pytest.approx(qrisc)
    assert bc["q_raff_kwh_anno"] == pytest.approx(qraff)
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
def test_variante_gas_60_non_calcolabile():
    bc = _variante(p_gas_eur_mwh=60)
    assert bc["risparmio_eur_anno"] == pytest.approx(-1541.7956656346796)
    assert bc["van"] == pytest.approx(-76003.31177403699)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_gas_30_non_calcolabile():
    bc = _variante(p_gas_eur_mwh=30)
    assert bc["risparmio_eur_anno"] == pytest.approx(-9541.79566563468)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_gas_zero_non_calcolabile():
    bc = _variante(p_gas_eur_mwh=0)
    assert bc["valid"] is True
    assert bc["c_base_eur_anno"] == pytest.approx(18000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-17541.79566563468)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_senza_raffrescamento_non_conviente():
    bc = _variante(q_raff_kwh_c_m2_anno=0)
    assert bc["q_raff_kwh_anno"] == 0.0
    assert bc["e_chiller_kwh_anno"] == 0.0
    assert bc["e_pdc_raff_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(4352.941176470587)
    assert bc["van"] == pytest.approx(-14817.959127919792)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(73.67647058823529)
    assert bc["payback"] == 14
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_capex_alto_marginale_e_non_conviente():
    bc = _variante(capex_eur=70000)
    assert bc["risparmio_eur_anno"] == pytest.approx(6458.20433436532)
    assert bc["van"] == pytest.approx(-2966.047468592274)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"
    bc2 = _variante(capex_eur=80000)
    assert bc2["van"] == pytest.approx(-12966.047468592275)
    assert bc2["payback"] == 13
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex_eur=0)
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(67033.95253140773, rel=1e-6)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(36873.065015479806)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(-10131.458011518565)
    assert bc2["payback"] == 10
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_el_alto_e_cop_risc_basso():
    bc = _variante(p_el_eur_mwh=400)
    assert bc["risparmio_eur_anno"] == pytest.approx(-2866.873065015483)
    assert bc["van"] == pytest.approx(-89757.16205373139)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(100.75077399380805)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CALCOLABILE"
    bc2 = _variante(cop_pdc_risc=2.8)
    assert bc2["e_pdc_risc_kwh_anno"] == pytest.approx(85714.28571428572)
    assert bc2["risparmio_eur_anno"] == pytest.approx(2676.6917293233055)
    assert bc2["van"] == pytest.approx(-32216.855175997847)
    assert bc2["breakeven_gas_eur_mwh"] == pytest.approx(79.9624060150376)
    assert bc2["payback"] is None
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_superficie_piccola_e_grande():
    bc = _variante(s_sale_m2=1000)
    assert bc["q_risc_kwh_anno"] == pytest.approx(120000.0)
    assert bc["q_raff_kwh_anno"] == pytest.approx(60000.0)
    assert bc["gas_base_kwh_anno"] == pytest.approx(133333.33333333333)
    assert bc["c_base_eur_anno"] == pytest.approx(25000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(22770.89783281734)
    assert bc["risparmio_eur_anno"] == pytest.approx(2229.10216718266)
    assert bc["van"] == pytest.approx(-36862.681772476724)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"
    bc2 = _variante(s_sale_m2=3000)
    assert bc2["q_risc_kwh_anno"] == pytest.approx(360000.0)
    assert bc2["risparmio_eur_anno"] == pytest.approx(10687.306501547988)
    assert bc2["van"] == pytest.approx(50930.586835292255)
    assert bc2["tir"] == pytest.approx(15.852794686311366)
    assert bc2["payback"] == 6
    assert bc2["verdetto"] == "CONVIENTE"


def test_monotonia_prezzo_gas_crescente():
    base = mh798_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas_eur_mwh=91)["risparmio_eur_anno"]
    basso = _variante(p_gas_eur_mwh=89)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(266.66666666666663)
    assert base - basso == pytest.approx(266.66666666666663)


def test_monotonia_superficie_crescente():
    assert _variante(s_sale_m2=1000)["risparmio_eur_anno"] < \
        mh798_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(s_sale_m2=3000)["risparmio_eur_anno"] > \
        mh798_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(s_sale_m2=3000)["q_risc_kwh_anno"] == \
        pytest.approx(360000.0)


def test_demo_deterministica_due_chiamate():
    a = mh798_demo_calcoli()
    b = mh798_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh798_demo().keys()) == {
        "s_sale_m2",
        "q_risc_kwh_th_m2_anno", "q_raff_kwh_c_m2_anno",
        "eta_caldaia", "cop_chiller",
        "cop_pdc_risc", "cop_pdc_raff",
        "p_gas_eur_mwh", "p_el_eur_mwh",
        "om_base_eur_anno", "om_alt_eur_anno",
        "capex_eur", "wacc_pct", "vita_anni",
        "f_gas_t_per_mwh", "f_el_t_per_mwh",
        "tolleranza_pct"}


# ---------------------------------------------------------------- degenere
def test_degenere_cop_uguale_uno_sollevela():
    with pytest.raises(ValueError):
        _variante(cop_pdc_risc=1.0)
    with pytest.raises(ValueError):
        _variante(cop_pdc_raff=1.0)


def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"s_sale_m2": 0},
               {"s_sale_m2": -10},
               {"q_risc_kwh_th_m2_anno": -0.1},
               {"q_raff_kwh_c_m2_anno": -0.1},
               {"eta_caldaia": 0}, {"eta_caldaia": 1.01},
               {"cop_chiller": 1.0}, {"cop_chiller": 0.5},
               {"cop_pdc_risc": 1.0}, {"cop_pdc_risc": 0.5},
               {"cop_pdc_raff": 1.0}, {"cop_pdc_raff": 0.5},
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
        assert mh798_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"s_sale_m2": "2000"},
               {"s_sale_m2": float("nan")},
               {"p_gas_eur_mwh": float("inf")},
               {"capex_eur": True},
               {"q_risc_kwh_th_m2_anno": "120"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh798_valida(**d)["valido"] is False


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    for kw in ({"p_gas_eur_mwh": 0},
               {"p_gas_eur_mwh": 65.78},
               {"p_gas_eur_mwh": 30}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] <= 0.0
        assert bc["verdetto"] == "NON_CALCOLABILE"
        assert bc["flussi"]


def test_pareggio_esatto_tolleranza_float():
    # A pareggio esatto il risparmio puo' essere +1e-11
    # (non <= 0): la guard NON scatta sul segno
    # floating point, ma la VAN resta circa -60.000
    # (oltre la tolleranza del 10 % di 60.000), quindi
    # il verdetto e' NON_CONVIENTE; se il risparmio
    # risulta esattamente <= 0 scatta invece la guard
    # NON_CALCOLABILE. In nessun caso CONVIENTE.
    bc = _variante(p_gas_eur_mwh=65.78173374613004)
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] in ("NON_CALCOLABILE", "NON_CONVIENTE")
    assert bc["verdetto"] != "CONVIENTE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh798_demo_calcoli()
    testo = mh798_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_gas_eur_mwh" in testo
    assert "co2_evitata_t_anno" in testo
    assert "q_raff_kwh_anno" in testo
    assert "s_sale_m2" in testo
    assert "e_chiller_kwh_anno" in testo
    assert "e_pdc_raff_kwh_anno" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh798_demo_calcoli()
    testo = mh798_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"q_risc_kwh_anno;{bc['q_risc_kwh_anno']}" in testo
    assert f"gas_base_kwh_anno;{bc['gas_base_kwh_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh798_demo_calcoli()
    testo = mh798_csv(bc, _demo_kwargs())
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
    return ["mh" + "79" + "7", "st" + "79" + "7",
            "tab" + "79" + "7", "w" + "79" + "8",
            "mh" + "79" + "6", "tab" + "79" + "6"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w799_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w799_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab798:")


def test_registry_chain_tail_and_count():
    """Registry della nuova scheda: il frammento UI apre la
    scheda numero 798 (la coda della catena, in append dopo
    la coda precedente che termina a 797, termina con la
    nuova scheda e il conteggio atteso delle schede e'
    798)."""
    src = _leggi("w799_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 798
    assert src.count("with tab798:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w799_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w799_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st798_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) >= 24
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w799_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 4
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w799_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def798[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w799_ui.py")
        usate = set(re.findall(r'_def798\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 17
        assert usate <= set(mh798_demo().keys())
