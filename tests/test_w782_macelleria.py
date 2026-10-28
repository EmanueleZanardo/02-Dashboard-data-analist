"""Test tab782 "Macelleria: il calore dei frigoriferi
scal da acqua e negozio?" (titolo completo nel
frammento UI).
(File repo: tests/test_w782_macelleria_recupero.py,
contenuto pronto da scrivere in repo.)

Business case deterministico di una macelleria
(banchi + celle): freddo Q_freddo = P x ore_eq
kWh_th/anno; elettricita' frigoriferi E_frig =
Q_freddo / COP kWh_e/anno (costo comune ai due
casi, NON entra nel confronto); scarto Q_scart =
Q_freddo + E_frig; potenziale Q_rec_pot = Q_scart
x quota; domanda Q_domanda = Q_acs + Q_risc;
recuperato Q_rec = min(Q_rec_pot, Q_domanda);
elettricita' di recupero E_rec = Q_rec x k_pompa;
C_base = Q_domanda / eta / 1000 x p_gas + O&M_base
EUR/anno; C_alt = (Q_domanda - Q_rec) / eta / 1000
x p_gas + E_rec / 1000 x p_el + O&M_alt EUR/anno
(prezzi EUR/MWh, energie kWh: / 1000 esatto);
risparmio = C_base - C_alt; CO2 evitata =
Q_rec / eta / 1000 x f_gas - E_rec / 1000 x f_el
t/anno; copertura = Q_rec / Q_domanda; flussi
[-CAPEX, risparmio x vita]; VAN, TIR, payback
(primo anno con cumulato >= 0); breakeven gas
p_gas_be = (E_rec / 1000 x p_el + O&M_alt - O&M_base)
/ ((Q_rec / eta) / 1000) EUR/MWh, None se Q_rec
<= 0 o numeratore < 0, SOGLIA MINIMA quando
esiste. Verdetto: NON_CALCOLABILE se risparmio
<= 0 (guard degenere: UI salta KPI, grafico,
tabella e CSV); altrimenti CONVIENTE se VAN > 0,
MARGINALE se VAN negativa entro tolleranza %
del CAPEX, NON_CONVIENTE se VAN negativa oltre
la tolleranza. Distinzione esplicita: macelleria
(banchi + celle) con recupero dello scarto per
ACS e riscaldamento del negozio contro caldaia
a gas; NON un confronto per singola cella tra
gruppo tradizionale e pompa di calore con
free-cooling, senza recupero per ACS e
riscaldamento di un punto vendita.

Demo (macelleria media): P 25 kW_th, 6.000 ore
eq, COP 2,5, quota 0,6, ACS 15.000, riscaldamento
20.000 kWh_th/anno, caldaia 0,9, gas 90, el 250
EUR/MWh, k_pompa 0,02, O&M base 400, alt 700,
CAPEX 12.000, WACC 5 %, vita 15, f_gas 0,20,
f_el 0,35, tolleranza 10 % del CAPEX. Valori
calcolati eseguendo mh782_demo_calcoli():
Q_freddo 150.000, E_frig 60.000, Q_scart 210.000,
Q_rec_pot 126.000, domanda 35.000, Q_rec 35.000
(cappato dalla domanda), E_rec 700, C_base
3.900, C_alt 875, risparmio 3.025, CO2 evitata
7,5327777777777785, copertura 1,0, VAN
19.398,46556549629, TIR 24,23595672910306 %,
payback 4, breakeven gas 12,214285714285714,
verdetto CONVIENTE.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w783_helpers import (
    demo_calcoli,
    mh782_breakeven_gas,
    mh782_c_alt,
    mh782_c_base,
    mh782_calcola,
    mh782_co2_evitata,
    mh782_cop,
    mh782_copertura,
    mh782_csv,
    mh782_demo,
    mh782_demo_calcoli,
    mh782_e_frig,
    mh782_e_rec,
    mh782_eta,
    mh782_flussi,
    mh782_frazione,
    mh782_int_pos,
    mh782_num,
    mh782_nneg,
    mh782_payback,
    mh782_pct_tolleranza,
    mh782_pct_wacc,
    mh782_pos,
    mh782_q_domanda,
    mh782_q_freddo,
    mh782_q_rec,
    mh782_q_rec_pot,
    mh782_q_scart,
    mh782_risparmio,
    mh782_tir,
    mh782_valida,
    mh782_van,
    mh782_verdetto,
)

_DEMO = {
    "q_freddo_kwh_anno": 150000.0,
    "e_frig_kwh_anno": 60000.0,
    "q_scart_kwh_anno": 210000.0,
    "q_rec_pot_kwh_anno": 126000.0,
    "q_domanda_kwh_anno": 35000.0,
    "q_rec_kwh_anno": 35000.0,
    "e_rec_kwh_anno": 700.0,
    "gas_risparmiato_mwh_anno": 38.88888888888889,
    "c_base_eur_anno": 3900.0,
    "c_alt_eur_anno": 875.0,
    "risparmio_eur_anno": 3025.0,
    "co2_evitata_t_anno": 7.5327777777777785,
    "copertura": 1.0,
    "van": 19398.46556549629,
    "tir": 24.23595672910306,
    "breakeven_gas_eur_mwh": 12.214285714285714,
}


def _demo_kwargs():
    return dict(mh782_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh782_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh782_num(3, "x") == 3.0
    assert mh782_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh782_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh782_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh782_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh782_pos(0, "x")
    with pytest.raises(ValueError):
        mh782_pos(-1, "x")
    assert mh782_pos(0.5, "x") == 0.5


def test_cop_maggiore_di_uno():
    assert mh782_cop(2.5, "x") == 2.5
    assert mh782_cop(1.01, "x") == 1.01
    with pytest.raises(ValueError):
        mh782_cop(1.0, "x")
    with pytest.raises(ValueError):
        mh782_cop(0.5, "x")
    with pytest.raises(ValueError):
        mh782_cop(0, "x")


def test_frazione_limiti():
    assert mh782_frazione(0, "x") == 0.0
    assert mh782_frazione(1, "x") == 1.0
    assert mh782_frazione(0.6, "x") == 0.6
    with pytest.raises(ValueError):
        mh782_frazione(-0.1, "x")
    with pytest.raises(ValueError):
        mh782_frazione(1.01, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh782_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh782_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh782_int_pos(0, "x")


def test_eta_limiti():
    assert mh782_eta(1.0, "x") == 1.0
    assert mh782_eta(0.9, "x") == 0.9
    with pytest.raises(ValueError):
        mh782_eta(0, "x")
    with pytest.raises(ValueError):
        mh782_eta(1.01, "x")


def test_pct_wacc_limiti():
    assert mh782_pct_wacc(0, "x") == 0.0
    assert mh782_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh782_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh782_pct_tolleranza(0, "x") == 0.0
    assert mh782_pct_tolleranza(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh782_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh782_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_q_freddo_e_frig_scart():
    assert mh782_q_freddo(25, 6000) == 150000.0
    assert mh782_e_frig(150000, 2.5) == pytest.approx(60000.0)
    assert mh782_q_scart(150000, 60000) == 210000.0
    with pytest.raises(ValueError):
        mh782_q_freddo(0, 6000)
    with pytest.raises(ValueError):
        mh782_e_frig(150000, 1.0)
    with pytest.raises(ValueError):
        mh782_e_frig(150000, 0.5)


def test_q_rec_pot_domanda_rec():
    assert mh782_q_rec_pot(210000, 0.6) == pytest.approx(126000.0)
    assert mh782_q_rec_pot(210000, 0) == 0.0
    assert mh782_q_domanda(15000, 20000) == 35000.0
    assert mh782_q_rec(126000, 35000) == 35000.0
    assert mh782_q_rec(21000, 35000) == 21000.0
    with pytest.raises(ValueError):
        mh782_q_rec_pot(210000, 1.5)
    with pytest.raises(ValueError):
        mh782_q_domanda(-1, 20000)


def test_e_rec():
    assert mh782_e_rec(35000, 0.02) == pytest.approx(700.0)
    assert mh782_e_rec(0, 0.02) == 0.0
    with pytest.raises(ValueError):
        mh782_e_rec(35000, -0.01)


def test_c_base_c_alt_scomposizione():
    assert mh782_c_base(35000, 0.9, 90, 400) == pytest.approx(3900.0)
    assert mh782_c_base(35000, 0.9, 0, 400) == pytest.approx(400.0)
    assert mh782_c_alt(35000, 35000, 0.9, 90, 700, 250,
                       700) == pytest.approx(875.0)
    assert mh782_c_alt(35000, 0, 0.9, 90, 0, 250,
                       700) == pytest.approx(4200.0)
    assert mh782_c_alt(35000, 21000, 0.9, 90, 420, 250,
                       700) == pytest.approx(2205.0)
    with pytest.raises(ValueError):
        mh782_c_base(35000, 0, 90, 400)
    with pytest.raises(ValueError):
        mh782_c_alt(35000, 35000, 0.9, -1, 700, 250, 700)


def test_risparmio_segno():
    assert mh782_risparmio(3900.0, 875.0) == pytest.approx(3025.0)
    assert mh782_risparmio(875.0, 875.0) == 0.0
    assert mh782_risparmio(3900.0, 4200.0) == pytest.approx(-300.0)


def test_co2_evitata():
    assert mh782_co2_evitata(35000, 0.9, 0.20, 700,
                             0.35) == pytest.approx(7.5327777777777785)
    assert mh782_co2_evitata(21000, 0.9, 0.20, 420,
                             0.35) == pytest.approx(4.519666666666667)
    assert mh782_co2_evitata(0, 0.9, 0.20, 0, 0.35) == 0.0
    # Gas risparmiato diviso per eta, non Q_rec secco.
    assert mh782_co2_evitata(35000, 0.9, 0.20, 0,
                             0.35) == pytest.approx(35000 / 0.9 / 1000.0 * 0.20)
    with pytest.raises(ValueError):
        mh782_co2_evitata(35000, 0.9, -0.10, 700, 0.35)


def test_copertura():
    assert mh782_copertura(35000, 35000) == pytest.approx(1.0)
    assert mh782_copertura(21000, 35000) == pytest.approx(0.6)
    assert mh782_copertura(0, 35000) == 0.0
    assert mh782_copertura(35000, 0) is None
    assert mh782_copertura(35000, -5) is None


def test_breakeven_gas_demo_e_varianti():
    assert mh782_breakeven_gas(700, 250, 700, 400, 35000,
                               0.9) == pytest.approx(12.214285714285714)
    assert mh782_breakeven_gas(420, 250, 700, 400, 21000,
                               0.9) == pytest.approx(17.357142857142858)
    assert mh782_breakeven_gas(0, 250, 700, 400, 0, 0.9) is None
    # Numeratore negativo: O&M alternativo sotto il base
    # e recupero elettrico nullo -> nessun pareggio.
    assert mh782_breakeven_gas(0, 250, 100, 400, 35000,
                               0.9) is None
    with pytest.raises(ValueError):
        mh782_breakeven_gas(700, 250, 700, 400, 35000, 0)


def test_breakeven_verifica_pareggio():
    """Al prezzo gas di pareggio i costi si eguagliano
    e il risparmio e' zero: scatta la guard
    NON_CALCOLABILE, non un verdetto di convenienza."""
    bc = _variante(p_gas_eur_mwh=12.214285714285714)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    demo = mh782_demo_calcoli()
    assert (demo["e_rec_kwh_anno"] / 1000.0
            * demo["p_el_eur_mwh"]
            + demo["om_alt_eur_anno"]
            - demo["om_base_eur_anno"]) == pytest.approx(
        (demo["q_rec_kwh_anno"] / demo["eta_caldaia"]) / 1000.0
        * demo["breakeven_gas_eur_mwh"])


def test_breakeven_soglia_minima():
    """Sopra la soglia il recupero vince, sotto perde."""
    be = mh782_demo_calcoli()["breakeven_gas_eur_mwh"]
    assert _variante(p_gas_eur_mwh=be + 1)[
        "c_alt_eur_anno"] < _variante(p_gas_eur_mwh=be + 1)[
        "c_base_eur_anno"]
    assert _variante(p_gas_eur_mwh=be - 1)[
        "c_alt_eur_anno"] > _variante(p_gas_eur_mwh=be - 1)[
        "c_base_eur_anno"]


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh782_flussi(12000, 3025.0, 15)
    assert len(fl) == 16
    assert fl[0] == -12000
    assert all(f == 3025.0 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh782_demo_calcoli()
    assert bc["van"] == pytest.approx(19398.46556549629)
    assert mh782_van([-12000] + [3025.0] * 15,
                     0) == pytest.approx(33375.0)
    assert mh782_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh782_demo_calcoli()
    assert bc["tir"] == pytest.approx(24.23595672910306)
    assert mh782_tir([-12000] + [3025.0] * 15) == \
        pytest.approx(0.2423595672910306)
    tir = mh782_tir([-12000] + [3025.0] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-12000] + [3025.0] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh782_payback([-12000] + [3025.0] * 15) == 4
    assert mh782_payback([-12000] + [-1000.0] * 15) is None
    assert mh782_payback([0] + [3025.0] * 15) == 0
    assert mh782_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh782_verdetto(3025.0, 19398.46556549629, 12000,
                          10.0) == "CONVIENTE"
    assert mh782_verdetto(3025.0, 0.0, 12000, 10.0) == "MARGINALE"
    assert mh782_verdetto(3025.0, -601.53, 32000, 10.0) == "MARGINALE"
    assert mh782_verdetto(3025.0, -1200.0, 12000, 10.0) == "MARGINALE"
    assert mh782_verdetto(3025.0, -1200.01, 12000, 10.0) == "NON_CONVIENTE"
    assert mh782_verdetto(3025.0, -4820.74, 12000, 10.0) == "NON_CONVIENTE"
    assert mh782_verdetto(0.0, 19398.46556549629, 12000,
                          10.0) == "NON_CALCOLABILE"
    assert mh782_verdetto(-300.0, -15113.90, 12000,
                          10.0) == "NON_CALCOLABILE"
    assert mh782_verdetto(None, 19398.46556549629, 12000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh782_verdetto(float("nan"), 19398.0, 12000, 10.0)
    with pytest.raises(ValueError):
        mh782_verdetto(3025.0, 19398.0, -1, 10.0)
    with pytest.raises(ValueError):
        mh782_verdetto(3025.0, 19398.0, 12000, 100.1)


def test_valida_demo_ok():
    v = mh782_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("p_kw", "25"),
                       ("p_kw", float("nan")),
                       ("p_kw", float("inf")),
                       ("p_kw", True),
                       ("p_gas_eur_mwh", None),
                       ("quota_rec", "0.6")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh782_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("p_kw", 0), ("p_kw", -1),
                          ("ore_eq", 0), ("ore_eq", -1),
                          ("cop_frig", 1.0), ("cop_frig", 0.5),
                          ("quota_rec", -0.1),
                          ("quota_rec", 1.01),
                          ("q_acs_kwh", -1),
                          ("q_risc_kwh", -1),
                          ("eta_caldaia", 0),
                          ("eta_caldaia", 1.01),
                          ("p_gas_eur_mwh", -1),
                          ("p_el_eur_mwh", -1),
                          ("k_pompa", -0.01),
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
        assert mh782_valida(**d)["valido"] is False


def test_valida_domanda_nulla_rifiutata():
    d = _demo_kwargs()
    d["q_acs_kwh"] = 0
    d["q_risc_kwh"] = 0
    assert mh782_valida(**d)["valido"] is False
    with pytest.raises(ValueError):
        _variante(q_acs_kwh=0, q_risc_kwh=0)


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"quota_rec": 0, "p_gas_eur_mwh": 0,
              "p_el_eur_mwh": 0, "k_pompa": 0,
              "om_base_eur_anno": 0, "om_alt_eur_anno": 0,
              "capex_eur": 0, "wacc_pct": 0,
              "f_gas_t_per_mwh": 0, "f_el_t_per_mwh": 0,
              "tolleranza_pct": 0})
    assert mh782_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["quota_rec"] = 1
    assert mh782_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh782_demo()
    assert d["p_kw"] == 25
    assert d["ore_eq"] == 6000
    assert d["cop_frig"] == 2.5
    assert d["quota_rec"] == 0.6
    assert d["q_acs_kwh"] == 15000
    assert d["q_risc_kwh"] == 20000
    assert d["eta_caldaia"] == 0.9
    assert d["p_gas_eur_mwh"] == 90
    assert d["p_el_eur_mwh"] == 250
    assert d["k_pompa"] == 0.02
    assert d["om_base_eur_anno"] == 400
    assert d["om_alt_eur_anno"] == 700
    assert d["capex_eur"] == 12000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["f_gas_t_per_mwh"] == 0.20
    assert d["f_el_t_per_mwh"] == 0.35
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    """Tutti gli output numerici demo a tolleranza
    1e-9 relativa: confronto delle costanti _DEMO
    contro mh782_demo_calcoli()."""
    bc = mh782_demo_calcoli()
    for chiave, atteso in _DEMO.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert got == pytest.approx(atteso, rel=1e-9), chiave
    assert bc["payback"] == 4
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True
    assert demo_calcoli()["van"] == bc["van"]


def test_demo_calcoli_fisica_economia():
    bc = mh782_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(3900.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(875.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(3025.0)
    assert bc["co2_evitata_t_anno"] == pytest.approx(7.5327777777777785)
    assert bc["gas_risparmiato_mwh_anno"] == pytest.approx(38.88888888888889)


def test_demo_flussi_e_cumulato():
    bc = mh782_demo_calcoli()
    assert bc["flussi"][0] == -12000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(3025.0) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -12000
    assert righe.iloc[3]["Cumulato (EUR)"] == pytest.approx(-2925.0)
    assert righe.iloc[4]["Cumulato (EUR)"] == pytest.approx(100.0)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(33375.0)


def test_demo_tabella_righe():
    bc = mh782_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Freddo prodotto (kWh_th/anno)"] == pytest.approx(150000.0)
    assert mappa["Calore di scarto (kWh_th/anno)"] == pytest.approx(210000.0)
    assert mappa["Calore recuperato (kWh_th/anno)"] == pytest.approx(35000.0)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(3900.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(875.0)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(3025.0)
    assert mappa["Payback (anni)"] == 4
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] == \
        pytest.approx(12.214285714285714)


def test_demo_coerenza_interna():
    bc = mh782_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["q_freddo_kwh_anno"] + bc["e_frig_kwh_anno"] == \
        pytest.approx(bc["q_scart_kwh_anno"])
    assert bc["q_rec_kwh_anno"] == pytest.approx(
        min(bc["q_rec_pot_kwh_anno"], bc["q_domanda_kwh_anno"]))
    assert bc["e_rec_kwh_anno"] == pytest.approx(
        bc["q_rec_kwh_anno"] * bc["k_pompa"])
    assert bc["copertura"] == pytest.approx(
        bc["q_rec_kwh_anno"] / bc["q_domanda_kwh_anno"])
    # E_frig NON entra nei costi: C_base/C_alt non la usano.
    assert bc["c_base_eur_anno"] == pytest.approx(
        bc["q_domanda_kwh_anno"] / bc["eta_caldaia"] / 1000.0
        * bc["p_gas_eur_mwh"] + bc["om_base_eur_anno"])


def test_demo_contro_riconteggio_indipendente():
    p, ore, cop, quota = 25, 6000, 2.5, 0.6
    acs, risc, eta, pg, pel, k = 15000, 20000, 0.9, 90, 250, 0.02
    omb, oma, cx = 400, 700, 12000
    fg, fel, wacc, vita = 0.20, 0.35, 5.0, 15
    qf = p * ore
    ef = qf / cop
    qs = qf + ef
    qpot = qs * quota
    qd = acs + risc
    qr = min(qpot, qd)
    er = qr * k
    cb = qd / eta / 1000.0 * pg + omb
    ca = (qd - qr) / eta / 1000.0 * pg + er / 1000.0 * pel + oma
    risp = cb - ca
    co2 = qr / eta / 1000.0 * fg - er / 1000.0 * fel
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    be = (er / 1000.0 * pel + oma - omb) / ((qr / eta) / 1000.0)
    bc = mh782_demo_calcoli()
    assert bc["q_freddo_kwh_anno"] == pytest.approx(qf)
    assert bc["e_frig_kwh_anno"] == pytest.approx(ef)
    assert bc["q_scart_kwh_anno"] == pytest.approx(qs)
    assert bc["q_rec_pot_kwh_anno"] == pytest.approx(qpot)
    assert bc["q_domanda_kwh_anno"] == pytest.approx(qd)
    assert bc["q_rec_kwh_anno"] == pytest.approx(qr)
    assert bc["e_rec_kwh_anno"] == pytest.approx(er)
    assert bc["c_base_eur_anno"] == pytest.approx(cb)
    assert bc["c_alt_eur_anno"] == pytest.approx(ca)
    assert bc["risparmio_eur_anno"] == pytest.approx(risp)
    assert bc["co2_evitata_t_anno"] == pytest.approx(co2)
    assert bc["van"] == pytest.approx(van)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(be)


# ---------------------------------------------------------------- varianti
def test_variante_quota_bassa_cappata_dalla_domanda_no():
    """Quota 0,1: potenziale 21.000 sotto la domanda
    35.000, quindi il recuperato e' 21.000, copertura
    60 %, risparmio 1.695, VAN 5.593,52, TIR 11,28 %,
    payback 8, CONVIENTE, breakeven 17,36."""
    bc = _variante(quota_rec=0.1)
    assert bc["q_rec_pot_kwh_anno"] == pytest.approx(21000.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(21000.0)
    assert bc["copertura"] == pytest.approx(0.6)
    assert bc["risparmio_eur_anno"] == pytest.approx(1695.0)
    assert bc["van"] == pytest.approx(5593.520374716104)
    assert bc["tir"] == pytest.approx(11.283721066826216)
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(17.357142857142858)


def test_variante_quota_zero_non_calcolabile():
    """Quota zero: nessun recupero, costo alternativo
    4.200 contro baseline 3.900, risparmio -300:
    verdetto NON_CALCOLABILE, ma helper calcolabili
    (flussi pieni, VAN -15.113,90, TIR None,
    payback None, breakeven None)."""
    bc = _variante(quota_rec=0.0)
    assert bc["valid"] is True
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["c_alt_eur_anno"] == pytest.approx(4200.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-300.0)
    assert bc["van"] == pytest.approx(-15113.89741145417)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_gas_basso_risparmio_positivo_ma_non_conviente():
    """Gas 30 EUR/MWh: risparmio ancora positivo
    (691,67) ma VAN -4.820,74 oltre la tolleranza
    (1.200): NON_CONVIENTE. Il verdetto guarda la
    VAN, non il solo risparmio positivo."""
    bc = _variante(p_gas_eur_mwh=30)
    assert bc["risparmio_eur_anno"] == pytest.approx(691.6666666666667)
    assert bc["van"] == pytest.approx(-4820.736523591758)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_capex_alto_non_conviente_e_marginale():
    bc = _variante(capex_eur=100000)
    assert bc["risparmio_eur_anno"] == pytest.approx(3025.0)
    assert bc["van"] == pytest.approx(-68601.53443450372)
    assert bc["verdetto"] == "NON_CONVIENTE"
    bc2 = _variante(capex_eur=32000)
    assert bc2["van"] == pytest.approx(-601.53443450371, rel=1e-6)
    assert bc2["verdetto"] == "MARGINALE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex_eur=0)
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(31398.46556549629, rel=1e-6)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(33375.0)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(11358.248160784056)
    assert bc2["payback"] == 4
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_el_alto():
    """Elettricita' 400 EUR/MWh: il recupero costa
    di piu' (E_rec 700 kWh), risparmio 2.920, VAN
    18.308,60, payback 5, CONVIENTE, breakeven gas
    14,91 (sale perche' il recupero elettrico
    costa di piu')."""
    bc = _variante(p_el_eur_mwh=400)
    assert bc["risparmio_eur_anno"] == pytest.approx(2920.0)
    assert bc["van"] == pytest.approx(18308.60147148733)
    assert bc["payback"] == 5
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(14.914285714285713)


def test_monotonia_prezzo_gas_crescente():
    base = mh782_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas_eur_mwh=91)["risparmio_eur_anno"]
    basso = _variante(p_gas_eur_mwh=89)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(38.88888888888889)
    assert base - basso == pytest.approx(38.88888888888889)


def test_monotonia_quota_crescente_fino_al_cap():
    """Il risparmio cresce con la quota finche' il
    potenziale resta sotto la domanda; oltre il cap
    (quota 0,6 nel demo: potenziale 126.000 contro
    domanda 35.000) resta piatto."""
    assert _variante(quota_rec=0.1)["risparmio_eur_anno"] < \
        mh782_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(quota_rec=1.0)["risparmio_eur_anno"] == \
        pytest.approx(mh782_demo_calcoli()["risparmio_eur_anno"])


def test_demo_deterministica_due_chiamate():
    a = mh782_demo_calcoli()
    b = mh782_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh782_demo().keys()) == {
        "p_kw", "ore_eq", "cop_frig", "quota_rec",
        "q_acs_kwh", "q_risc_kwh", "eta_caldaia",
        "p_gas_eur_mwh", "p_el_eur_mwh", "k_pompa",
        "om_base_eur_anno", "om_alt_eur_anno",
        "capex_eur", "wacc_pct", "vita_anni",
        "f_gas_t_per_mwh", "f_el_t_per_mwh",
        "tolleranza_pct"}


# ---------------------------------------------------------------- degenere
def test_degenere_cop_uguale_uno_sollevela():
    with pytest.raises(ValueError):
        _variante(cop_frig=1.0)


def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"p_kw": 0}, {"p_kw": -1},
               {"ore_eq": 0}, {"ore_eq": -1},
               {"cop_frig": 1.0}, {"cop_frig": 0.5},
               {"quota_rec": -0.1}, {"quota_rec": 1.01},
               {"q_acs_kwh": -1}, {"q_risc_kwh": -1},
               {"eta_caldaia": 0}, {"eta_caldaia": 1.01},
               {"p_gas_eur_mwh": -1},
               {"p_el_eur_mwh": -1},
               {"k_pompa": -0.01},
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
        assert mh782_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"p_kw": "25"},
               {"p_kw": float("nan")},
               {"p_gas_eur_mwh": float("inf")},
               {"capex_eur": True},
               {"quota_rec": "0.6"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh782_valida(**d)["valido"] is False


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    """Differenza chiave: risparmio <= 0 NON solleva
    negli helper (resta calcolabile con flussi, VAN,
    TIR e payback), ma il verdetto e' NON_CALCOLABILE
    e la UI salta KPI, grafico, tabella e CSV."""
    for kw in ({"quota_rec": 0.0},
               {"p_gas_eur_mwh": 12.214285714285714}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] <= 0.0
        assert bc["verdetto"] == "NON_CALCOLABILE"
        assert bc["flussi"]


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh782_demo_calcoli()
    testo = mh782_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_gas_eur_mwh" in testo
    assert "copertura" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh782_demo_calcoli()
    testo = mh782_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"q_rec_kwh_anno;{bc['q_rec_kwh_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh782_demo_calcoli()
    testo = mh782_csv(bc, _demo_kwargs())
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
    return ["mh" + "78" + "1", "st" + "78" + "1",
            "tab" + "78" + "1"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w783_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w783_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab782:")


def test_registry_chain_tail_and_count():
    """Registry della nuova tab: il frammento UI apre la tab
    numero 782 (la coda della catena termina con la nuova tab
    e il conteggio atteso delle tab e' 782)."""
    src = _leggi("w783_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 782
    assert src.count("with tab782:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w783_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w783_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st782_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) >= 19
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w783_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 2
    # Entrambe le guard (input degenere e risparmio <= 0)
    # stanno prima di KPI / grafico / tabella / CSV.
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w783_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def782[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w783_ui.py")
        usate = set(re.findall(r'_def782\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 18
        assert usate <= set(mh782_demo().keys())
