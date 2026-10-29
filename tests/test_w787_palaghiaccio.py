"""Test tab787 "Palaghiaccio: il calore di scarto
del freddo pista scalda gli spogliatoi e batte
caldaia a gas + chiller tradizionale?"
(titolo completo nel frammento UI).
(File repo: tests/test_w787_palaghiaccio.py,
contenuto pronto da scrivere in repo.)

Business case deterministico di un palaghiaccio
guidato dalla superficie della pista in m2 e dalla
superficie riscaldata in m2 (spogliatoi e
ambienti): il freddo della pista produce calore di
scarto, e quel calore di scarto scalda gli
spogliatoi al posto della caldaia a gas. Freddo
pista Q_freddo = S_pista x q_freddo kWh_f/anno;
elettricita' chiller E_chiller = Q_freddo /
COP_freddo kWh_e/anno; calore di scarto Q_scart =
Q_freddo + E_chiller kWh_th/anno (primo principio);
calore recuperato Q_rec = eta_rec x Q_scart
kWh_th/anno, SOLO dal calore di scarto della
refrigerazione della pista; riscaldamento Q_risc =
S_risc x q_risc kWh_th/anno; calore residuo
Q_risc_res = max(0, Q_risc - Q_rec) kWh_th/anno
(l'eccesso recuperato viene sprecato, senza
export); gas baseline G_base = Q_risc /
eta_caldaia kWh/anno; elettricita' pompa di calore
E_pdc = Q_risc_res / COP_pdc kWh_e/anno; C_base =
E_chiller / 1000 x p_el + G_base / 1000 x p_gas +
O&M_base EUR/anno; C_alt = E_chiller / 1000 x p_el
+ E_pdc / 1000 x p_el + O&M_alt EUR/anno
(l'elettricita' del chiller e' identica nei due
casi e si elide nel risparmio, ma resta in
entrambi i costi; prezzi EUR/MWh, energie kWh:
/ 1000 esatto); risparmio = C_base - C_alt;
CO2_base = E_chiller / 1000 x f_el + G_base /
1000 x f_gas t/anno; CO2_alt = (E_chiller + E_pdc)
/ 1000 x f_el t/anno; CO2_evitata = CO2_base -
CO2_alt; flussi [-CAPEX, risparmio x vita]; VAN,
TIR, payback (primo anno con cumulato >= 0);
breakeven gas p_gas_be = (C_alt - E_chiller /
1000 x p_el - O&M_base) x 1000 / G_base EUR/MWh,
None se G_base <= 0 o numeratore < 0, SOGLIA
MINIMA quando esiste. Verdetto: NON_CALCOLABILE
se risparmio <= 0 (guard degenere: UI salta KPI,
grafico, tabella e CSV); altrimenti CONVIENTE se
VAN > 0, MARGINALE se VAN negativa entro
tolleranza % del CAPEX, NON_CONVIENTE se VAN
negativa oltre la tolleranza. Distinzione
esplicita: NON la piscina coperta (acqua della
vasca da scaldare, nessun freddo pista e nessun
calore di scarto di refrigerazione), NON la
palestra (docce degli utenti con acqua calda
sanitaria + riscaldamento, recupero sulle acque
di scarico delle docce: nessun freddo pista,
nessun calore di scarto di refrigerazione) e NON
una tab generica di chiller o cella frigorifera
(carico frigorifero generico, calore di scarto
senza uso termico accoppiato definito): qui il
driver sono la superficie della pista in m2 +
la superficie riscaldata in m2, e il calore
recuperato viene SOLO dal calore di scarto della
refrigerazione della pista.

Demo (palaghiaccio): pista 1.800 m2 a 400
kWh_f/m2/anno, COP chiller 3,0, 1.500 m2
riscaldati a 120 kWh_th/m2/anno, caldaia 0,9,
recupero 0,15, COP pompa di calore 3,5, gas 90,
el 250 EUR/MWh, O&M base 4.000, alt 6.000, CAPEX
80.000, WACC 5 %, vita 15, f_gas 0,20, f_el 0,35,
tolleranza 10 % del CAPEX. Valori calcolati
eseguendo mh787_demo_calcoli(): Q_freddo
720.000, E_chiller 240.000, Q_scart 960.000,
Q_rec 144.000, Q_risc 180.000, Q_res 36.000,
E_pdc 10.285,714285714286, G_base 200.000,
C_base 82.000, C_alt 68.571,42857142858,
risparmio 13.428,57142857142, CO2_base 124,0,
CO2_alt 87,6, CO2_evitata 36,400000000000006,
VAN 59.383,97936985355, TIR 14,616986532511362 %,
payback 6, breakeven gas 22,8571428571429,
verdetto CONVIENTE.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w788_helpers import (
    demo_calcoli,
    mh787_breakeven_gas,
    mh787_c_alt,
    mh787_c_base,
    mh787_calcola,
    mh787_co2_alt,
    mh787_co2_base,
    mh787_co2_evitata,
    mh787_cop,
    mh787_csv,
    mh787_demo,
    mh787_demo_calcoli,
    mh787_e_chiller,
    mh787_e_pdc,
    mh787_eta,
    mh787_eta_rec,
    mh787_flussi,
    mh787_gas,
    mh787_int_pos,
    mh787_num,
    mh787_nneg,
    mh787_payback,
    mh787_pct_tolleranza,
    mh787_pct_wacc,
    mh787_pos,
    mh787_q_freddo,
    mh787_q_rec,
    mh787_q_res,
    mh787_q_risc,
    mh787_q_scart,
    mh787_risparmio,
    mh787_tir,
    mh787_valida,
    mh787_van,
    mh787_verdetto,
)

_DEMO = {
    "q_freddo_kwh_anno": 720000.0,
    "e_chiller_kwh_anno": 240000.0,
    "q_scart_kwh_anno": 960000.0,
    "q_rec_kwh_anno": 144000.0,
    "q_risc_kwh_anno": 180000.0,
    "q_risc_res_kwh_anno": 36000.0,
    "gas_base_kwh_anno": 200000.0,
    "e_pdc_kwh_anno": 10285.714285714286,
    "c_base_eur_anno": 82000.0,
    "c_alt_eur_anno": 68571.42857142858,
    "risparmio_eur_anno": 13428.57142857142,
    "co2_base_t_anno": 124.0,
    "co2_alt_t_anno": 87.6,
    "co2_evitata_t_anno": 36.400000000000006,
    "van": 59383.97936985355,
    "tir": 14.616986532511362,
    "breakeven_gas_eur_mwh": 22.8571428571429,
}


def _demo_kwargs():
    return dict(mh787_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh787_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh787_num(3, "x") == 3.0
    assert mh787_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh787_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh787_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh787_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh787_pos(0, "x")
    with pytest.raises(ValueError):
        mh787_pos(-1, "x")
    assert mh787_pos(0.5, "x") == 0.5


def test_cop_maggiore_di_uno():
    assert mh787_cop(3.0, "x") == 3.0
    assert mh787_cop(1.01, "x") == 1.01
    with pytest.raises(ValueError):
        mh787_cop(1.0, "x")
    with pytest.raises(ValueError):
        mh787_cop(0.5, "x")
    with pytest.raises(ValueError):
        mh787_cop(0, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh787_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh787_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh787_int_pos(0, "x")


def test_eta_limiti():
    assert mh787_eta(1.0, "x") == 1.0
    assert mh787_eta(0.9, "x") == 0.9
    with pytest.raises(ValueError):
        mh787_eta(0, "x")
    with pytest.raises(ValueError):
        mh787_eta(1.01, "x")


def test_eta_rec_limiti():
    assert mh787_eta_rec(0.0, "x") == 0.0
    assert mh787_eta_rec(1.0, "x") == 1.0
    assert mh787_eta_rec(0.15, "x") == 0.15
    with pytest.raises(ValueError):
        mh787_eta_rec(-0.1, "x")
    with pytest.raises(ValueError):
        mh787_eta_rec(1.01, "x")


def test_pct_wacc_limiti():
    assert mh787_pct_wacc(0, "x") == 0.0
    assert mh787_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh787_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh787_pct_tolleranza(0, "x") == 0.0
    assert mh787_pct_tolleranza(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh787_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh787_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_q_freddo_e_chiller():
    assert mh787_q_freddo(1800, 400) == 720000.0
    assert mh787_q_freddo(900, 400) == 360000.0
    assert mh787_q_freddo(1800, 200) == 360000.0
    assert mh787_e_chiller(720000, 3.0) == 240000.0
    assert mh787_e_chiller(360000, 3.0) == 120000.0
    assert mh787_e_chiller(0, 3.0) == 0.0
    with pytest.raises(ValueError):
        mh787_q_freddo(0, 400)
    with pytest.raises(ValueError):
        mh787_q_freddo(1800, 0)
    with pytest.raises(ValueError):
        mh787_q_freddo(1800, -10)
    with pytest.raises(ValueError):
        mh787_e_chiller(720000, 1.0)
    with pytest.raises(ValueError):
        mh787_e_chiller(720000, 0.5)


def test_q_scart_primo_principio():
    assert mh787_q_scart(720000, 240000) == 960000.0
    assert mh787_q_scart(360000, 120000) == 480000.0
    assert mh787_q_scart(0, 0) == 0.0
    # Lo scarto supera sempre il freddo: contiene
    # anche l'elettricita' del chiller.
    assert mh787_q_scart(720000, 240000) > 720000.0
    with pytest.raises(ValueError):
        mh787_q_scart(-1, 240000)
    with pytest.raises(ValueError):
        mh787_q_scart(720000, -1)


def test_q_rec_solo_scart():
    assert mh787_q_rec(960000, 0.15) == 144000.0
    assert mh787_q_rec(960000, 0) == 0.0
    assert mh787_q_rec(960000, 1.0) == 960000.0
    assert mh787_q_rec(480000, 0.15) == 72000.0
    with pytest.raises(ValueError):
        mh787_q_rec(960000, 1.01)
    with pytest.raises(ValueError):
        mh787_q_rec(960000, -0.1)


def test_q_risc_gas():
    assert mh787_q_risc(1500, 120) == 180000.0
    assert mh787_q_risc(1500, 0) == 0.0
    assert mh787_q_risc(750, 120) == 90000.0
    assert mh787_gas(180000, 0.9) == 200000.0
    assert mh787_gas(0, 0.9) == 0.0
    with pytest.raises(ValueError):
        mh787_q_risc(0, 120)
    with pytest.raises(ValueError):
        mh787_q_risc(1500, -0.1)
    with pytest.raises(ValueError):
        mh787_gas(180000, 0)
    with pytest.raises(ValueError):
        mh787_gas(180000, 1.01)


def test_q_res_troncamento_a_zero():
    assert mh787_q_res(180000, 144000) == 36000.0
    assert mh787_q_res(180000, 0) == 180000.0
    # L'eccesso recuperato viene sprecato, senza
    # export: il residuo non va mai sotto zero.
    assert mh787_q_res(180000, 960000) == 0.0
    assert mh787_q_res(180000, 180000) == 0.0
    assert mh787_q_res(0, 144000) == 0.0
    with pytest.raises(ValueError):
        mh787_q_res(-1, 144000)
    with pytest.raises(ValueError):
        mh787_q_res(180000, -1)


def test_e_pdc():
    assert mh787_e_pdc(36000, 3.5) == pytest.approx(10285.714285714286)
    assert mh787_e_pdc(180000, 3.5) == pytest.approx(51428.57142857143)
    assert mh787_e_pdc(0, 3.5) == 0.0
    with pytest.raises(ValueError):
        mh787_e_pdc(36000, 1.0)
    with pytest.raises(ValueError):
        mh787_e_pdc(36000, 0.5)


def test_c_base_c_alt_scomposizione():
    assert mh787_c_base(240000, 250, 200000, 90,
                        4000) == pytest.approx(82000.0)
    assert mh787_c_base(240000, 250, 0, 90, 4000) == pytest.approx(64000.0)
    assert mh787_c_alt(240000, 10285.714285714286, 250,
                       6000) == pytest.approx(68571.42857142858)
    assert mh787_c_alt(240000, 0, 250, 6000) == pytest.approx(66000.0)
    # Il chiller e' identico nei due costi: a parita'
    # di gas zero e pompa di calore zero, la
    # differenza resta solo sugli O&M.
    assert mh787_c_base(240000, 250, 0, 0, 4000) - \
        mh787_c_alt(240000, 0, 250, 6000) == pytest.approx(-2000.0)
    with pytest.raises(ValueError):
        mh787_c_base(240000, -1, 200000, 90, 4000)
    with pytest.raises(ValueError):
        mh787_c_base(240000, 250, 200000, -1, 4000)
    with pytest.raises(ValueError):
        mh787_c_alt(240000, 10285.714285714286, 250, -1)


def test_risparmio_segno_e_chiller_si_elide():
    assert mh787_risparmio(82000.0, 68571.42857142858) == \
        pytest.approx(13428.57142857142)
    assert mh787_risparmio(68571.42857142858, 68571.42857142858) == 0.0
    assert mh787_risparmio(64000.0, 68571.42857142858) == \
        pytest.approx(-4571.42857142858)
    # Il risparmio dipende solo da gas, pompa di
    # calore e O&M: il chiller si elide.
    assert mh787_risparmio(
        mh787_c_base(240000, 250, 200000, 90, 4000),
        mh787_c_alt(240000, 10285.714285714286, 250, 6000)) == \
        pytest.approx(18000.0 - 2571.42857142858 - 2000.0)


def test_co2_base_alt_evitata():
    assert mh787_co2_base(240000, 0.35, 200000, 0.20) == \
        pytest.approx(124.0)
    assert mh787_co2_alt(240000, 10285.714285714286, 0.35) == \
        pytest.approx(87.6)
    assert mh787_co2_evitata(240000, 0.35, 200000, 0.20,
                             10285.714285714286) == \
        pytest.approx(36.400000000000006)
    assert mh787_co2_base(240000, 0.35, 0, 0.20) == pytest.approx(84.0)
    assert mh787_co2_alt(240000, 0, 0.35) == pytest.approx(84.0)
    assert mh787_co2_evitata(240000, 0.35, 0, 0.20, 0) == \
        pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh787_co2_base(240000, -0.10, 200000, 0.20)
    with pytest.raises(ValueError):
        mh787_co2_alt(240000, 10285.714285714286, -0.10)


def test_breakeven_gas_demo_e_varianti():
    assert mh787_breakeven_gas(68571.42857142858, 240000, 250,
                               4000, 200000) == \
        pytest.approx(22.8571428571429)
    assert mh787_breakeven_gas(78857.14285714286, 240000, 250,
                               4000, 200000) == \
        pytest.approx(74.28571428571428)
    assert mh787_breakeven_gas(69600.0, 240000, 250,
                               4000, 200000) == \
        pytest.approx(28.0)
    assert mh787_breakeven_gas(66000.0, 240000, 250,
                               4000, 200000) == \
        pytest.approx(10.0)
    assert mh787_breakeven_gas(68571.42857142858, 240000, 250,
                               4000, 0) is None
    # Numeratore negativo: alternativa gia' piu'
    # conveniente a prezzo gas zero -> nessun pareggio.
    assert mh787_breakeven_gas(200, 240000, 250, 4000, 200000) is None
    with pytest.raises(ValueError):
        mh787_breakeven_gas(68571.42857142858, 240000, 250, 4000, -1)


def test_breakeven_verifica_pareggio():
    """Al prezzo gas di pareggio i costi si eguagliano
    e il risparmio e' zero: scatta la guard
    NON_CALCOLABILE, non un verdetto di convenienza."""
    bc = _variante(p_gas_eur_mwh=22.8571428571429)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    demo = mh787_demo_calcoli()
    assert (demo["c_alt_eur_anno"]
            - demo["e_chiller_kwh_anno"] / 1000.0
            * demo["p_el_eur_mwh"]
            - demo["om_base_eur_anno"]) * 1000.0 / demo["gas_base_kwh_anno"] == \
        pytest.approx(demo["breakeven_gas_eur_mwh"])


def test_breakeven_soglia_minima():
    """Sopra la soglia l'alternativa vince, sotto perde."""
    be = mh787_demo_calcoli()["breakeven_gas_eur_mwh"]
    assert _variante(p_gas_eur_mwh=be + 1)[
        "c_alt_eur_anno"] < _variante(p_gas_eur_mwh=be + 1)[
        "c_base_eur_anno"]
    assert _variante(p_gas_eur_mwh=be - 1)[
        "c_alt_eur_anno"] > _variante(p_gas_eur_mwh=be - 1)[
        "c_base_eur_anno"]


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh787_flussi(80000, 13428.57142857142, 15)
    assert len(fl) == 16
    assert fl[0] == -80000
    assert all(f == 13428.57142857142 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh787_demo_calcoli()
    assert bc["van"] == pytest.approx(59383.97936985355)
    assert mh787_van([-80000] + [13428.57142857142] * 15,
                     0) == pytest.approx(121428.5714285713)
    assert mh787_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh787_demo_calcoli()
    assert bc["tir"] == pytest.approx(14.616986532511362)
    assert mh787_tir([-80000] + [13428.57142857142] * 15) == \
        pytest.approx(0.14616986532511362)
    tir = mh787_tir([-80000] + [13428.57142857142] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-80000] + [13428.57142857142] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh787_payback([-80000] + [13428.57142857142] * 15) == 6
    assert mh787_payback([-80000] + [-1000.0] * 15) is None
    assert mh787_payback([0] + [13428.57142857142] * 15) == 0
    assert mh787_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh787_verdetto(13428.57142857142, 59383.97936985355, 80000,
                          10.0) == "CONVIENTE"
    assert mh787_verdetto(13428.57142857142, 0.0, 80000, 10.0) == "MARGINALE"
    assert mh787_verdetto(13428.57142857142, -8000.0, 80000, 10.0) == "MARGINALE"
    assert mh787_verdetto(13428.57142857142, -8000.01, 80000, 10.0) == "NON_CONVIENTE"
    assert mh787_verdetto(13428.57142857142, -44412.60, 80000, 10.0) == "NON_CONVIENTE"
    assert mh787_verdetto(0.0, 59383.97936985355, 80000,
                          10.0) == "NON_CALCOLABILE"
    assert mh787_verdetto(-4571.42857142858, -100759.32, 80000,
                          10.0) == "NON_CALCOLABILE"
    assert mh787_verdetto(None, 59383.97936985355, 80000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh787_verdetto(float("nan"), 59383.98, 80000, 10.0)
    with pytest.raises(ValueError):
        mh787_verdetto(13428.57, 59383.98, -1, 10.0)
    with pytest.raises(ValueError):
        mh787_verdetto(13428.57, 59383.98, 80000, 100.1)


def test_valida_demo_ok():
    v = mh787_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("superficie_pista_m2", "1800"),
                       ("superficie_pista_m2", float("nan")),
                       ("superficie_pista_m2", float("inf")),
                       ("superficie_pista_m2", True),
                       ("p_gas_eur_mwh", None),
                       ("q_freddo_kwh_m2_anno", "400")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh787_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("superficie_pista_m2", 0),
                          ("superficie_pista_m2", -10),
                          ("q_freddo_kwh_m2_anno", 0),
                          ("q_freddo_kwh_m2_anno", -10),
                          ("cop_freddo", 1.0),
                          ("cop_freddo", 0.5),
                          ("superficie_risc_m2", 0),
                          ("superficie_risc_m2", -10),
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
        assert mh787_valida(**d)["valido"] is False


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
    assert mh787_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["eta_rec"] = 1
    d["q_risc_kwh_m2_anno"] = 120
    assert mh787_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh787_demo()
    assert d["superficie_pista_m2"] == 1800
    assert d["q_freddo_kwh_m2_anno"] == 400
    assert d["cop_freddo"] == 3.0
    assert d["superficie_risc_m2"] == 1500
    assert d["q_risc_kwh_m2_anno"] == 120
    assert d["eta_caldaia"] == 0.9
    assert d["eta_rec"] == 0.15
    assert d["cop_pdc"] == 3.5
    assert d["p_gas_eur_mwh"] == 90
    assert d["p_el_eur_mwh"] == 250
    assert d["om_base_eur_anno"] == 4000
    assert d["om_alt_eur_anno"] == 6000
    assert d["capex_eur"] == 80000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["f_gas_t_per_mwh"] == 0.20
    assert d["f_el_t_per_mwh"] == 0.35
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    """Tutti gli output numerici demo a tolleranza
    1e-9 relativa: confronto delle costanti _DEMO
    contro mh787_demo_calcoli()."""
    bc = mh787_demo_calcoli()
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
    bc = mh787_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(82000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(68571.42857142858)
    assert bc["risparmio_eur_anno"] == pytest.approx(13428.57142857142)
    assert bc["co2_base_t_anno"] == pytest.approx(124.0)
    assert bc["co2_alt_t_anno"] == pytest.approx(87.6)
    assert bc["co2_evitata_t_anno"] == pytest.approx(36.400000000000006)
    assert bc["gas_base_kwh_anno"] == pytest.approx(200000.0)


def test_demo_flussi_e_cumulato():
    bc = mh787_demo_calcoli()
    assert bc["flussi"][0] == -80000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(13428.57142857142) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -80000
    assert righe.iloc[5]["Cumulato (EUR)"] == pytest.approx(-12857.142857142899)
    assert righe.iloc[6]["Cumulato (EUR)"] == pytest.approx(571.4285714285215)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(121428.5714285713)


def test_demo_tabella_righe():
    bc = mh787_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Freddo pista (kWh_f/anno)"] == pytest.approx(720000.0)
    assert mappa["Elettricita' chiller (kWh_e/anno)"] == pytest.approx(240000.0)
    assert mappa["Calore di scarto (kWh_th/anno)"] == pytest.approx(960000.0)
    assert mappa["Calore recuperato (kWh_th/anno)"] == pytest.approx(144000.0)
    assert mappa["Riscaldamento spogliatoi (kWh_th/anno)"] == pytest.approx(180000.0)
    assert mappa["Calore residuo (kWh_th/anno)"] == pytest.approx(36000.0)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(200000.0)
    assert mappa["Elettricita' pompa di calore (kWh_e/anno)"] == pytest.approx(10285.714285714286)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(82000.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(68571.42857142858)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(13428.57142857142)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(36.400000000000006)
    assert mappa["Payback (anni)"] == 6
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] == \
        pytest.approx(22.8571428571429)


def test_demo_coerenza_interna():
    bc = mh787_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["q_freddo_kwh_anno"] == pytest.approx(
        bc["superficie_pista_m2"] * bc["q_freddo_kwh_m2_anno"])
    assert bc["e_chiller_kwh_anno"] == pytest.approx(
        bc["q_freddo_kwh_anno"] / bc["cop_freddo"])
    assert bc["q_scart_kwh_anno"] == pytest.approx(
        bc["q_freddo_kwh_anno"] + bc["e_chiller_kwh_anno"])
    assert bc["q_rec_kwh_anno"] == pytest.approx(
        bc["eta_rec"] * bc["q_scart_kwh_anno"])
    assert bc["q_risc_kwh_anno"] == pytest.approx(
        bc["superficie_risc_m2"] * bc["q_risc_kwh_m2_anno"])
    assert bc["q_risc_res_kwh_anno"] == pytest.approx(
        max(0.0, bc["q_risc_kwh_anno"] - bc["q_rec_kwh_anno"]))
    assert bc["gas_base_kwh_anno"] == pytest.approx(
        bc["q_risc_kwh_anno"] / bc["eta_caldaia"])
    assert bc["e_pdc_kwh_anno"] == pytest.approx(
        bc["q_risc_res_kwh_anno"] / bc["cop_pdc"])
    assert bc["co2_evitata_t_anno"] == pytest.approx(
        bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])
    assert bc["c_base_eur_anno"] == pytest.approx(
        bc["e_chiller_kwh_anno"] / 1000.0 * bc["p_el_eur_mwh"]
        + bc["gas_base_kwh_anno"] / 1000.0 * bc["p_gas_eur_mwh"]
        + bc["om_base_eur_anno"])
    assert bc["c_alt_eur_anno"] == pytest.approx(
        bc["e_chiller_kwh_anno"] / 1000.0 * bc["p_el_eur_mwh"]
        + bc["e_pdc_kwh_anno"] / 1000.0 * bc["p_el_eur_mwh"]
        + bc["om_alt_eur_anno"])


def test_demo_contro_riconteggio_indipendente():
    sp, qf_spec, copf = 1800, 400, 3.0
    sr, qr_spec = 1500, 120
    eta, erec, copp = 0.9, 0.15, 3.5
    pg, pel, omb, oma, cx = 90, 250, 4000, 6000, 80000
    fg, fel, wacc, vita = 0.20, 0.35, 5.0, 15
    qfred = sp * qf_spec
    ech = qfred / copf
    qscart = qfred + ech
    qrec = erec * qscart
    qrisc = sr * qr_spec
    qres = max(0.0, qrisc - qrec)
    gas = qrisc / eta
    ep = qres / copp
    cb = ech / 1000.0 * pel + gas / 1000.0 * pg + omb
    ca = ech / 1000.0 * pel + ep / 1000.0 * pel + oma
    risp = cb - ca
    co2b = ech / 1000.0 * fel + gas / 1000.0 * fg
    co2a = (ech + ep) / 1000.0 * fel
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    be = (ca - ech / 1000.0 * pel - omb) * 1000.0 / gas
    bc = mh787_demo_calcoli()
    assert bc["q_freddo_kwh_anno"] == pytest.approx(qfred)
    assert bc["e_chiller_kwh_anno"] == pytest.approx(ech)
    assert bc["q_scart_kwh_anno"] == pytest.approx(qscart)
    assert bc["q_rec_kwh_anno"] == pytest.approx(qrec)
    assert bc["q_risc_kwh_anno"] == pytest.approx(qrisc)
    assert bc["q_risc_res_kwh_anno"] == pytest.approx(qres)
    assert bc["gas_base_kwh_anno"] == pytest.approx(gas)
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
def test_variante_gas_60_marginale():
    """Gas 60 EUR/MWh: risparmio ancora positivo
    (7.428,57) ma VAN -2.893,97 entro la tolleranza
    (8.000): MARGINALE con payback 11. Il verdetto
    guarda la VAN, non il solo risparmio positivo."""
    bc = _variante(p_gas_eur_mwh=60)
    assert bc["risparmio_eur_anno"] == pytest.approx(7428.57142857142)
    assert bc["van"] == pytest.approx(-2893.9688592299913)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"


def test_variante_gas_40_non_conviente():
    """Gas 40 EUR/MWh: risparmio 3.428,57 ancora
    positivo ma VAN -44.412,60 oltre la tolleranza
    (8.000): NON_CONVIENTE con payback mai
    raggiunto."""
    bc = _variante(p_gas_eur_mwh=40)
    assert bc["risparmio_eur_anno"] == pytest.approx(3428.5714285714203)
    assert bc["van"] == pytest.approx(-44412.601011952356)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_gas_zero_non_calcolabile():
    """Gas zero: costo baseline 64.000 (solo chiller
    + O&M) contro 68.571,43 dell'alternativa:
    risparmio -4.571,43, verdetto NON_CALCOLABILE,
    ma helper calcolabili (flussi pieni, VAN
    negativa, TIR None, payback None)."""
    bc = _variante(p_gas_eur_mwh=0)
    assert bc["valid"] is True
    assert bc["c_base_eur_anno"] == pytest.approx(64000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-4571.42857142858)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_risc_zero_non_calcolabile_be_none():
    """Senza riscaldamento (q_risc zero): gas zero,
    breakeven None, risparmio -2.000 (solo O&M:
    alternativa 66.000 contro base 64.000),
    NON_CALCOLABILE, CO2 evitata zero."""
    bc = _variante(q_risc_kwh_m2_anno=0)
    assert bc["gas_base_kwh_anno"] == 0.0
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["risparmio_eur_anno"] == pytest.approx(-2000.0)
    assert bc["co2_evitata_t_anno"] == pytest.approx(0.0)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_senza_recupero_non_conviente():
    """Senza recupero (eta_rec zero): calore residuo
    180.000, E_pdc 51.428,57, risparmio 3.142,86,
    VAN -47.378,22, breakeven 74,29, NON_CONVIENTE.
    Il recupero del calore di scarto e' decisivo:
    senza di esso la pompa di calore lavora a pieno
    carico."""
    bc = _variante(eta_rec=0)
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["q_risc_res_kwh_anno"] == pytest.approx(180000.0)
    assert bc["e_pdc_kwh_anno"] == pytest.approx(51428.57142857143)
    assert bc["risparmio_eur_anno"] == pytest.approx(3142.857142857145)
    assert bc["van"] == pytest.approx(-47378.21759428955)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(74.28571428571428)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_recupero_totale_troncato():
    """Recupero totale (eta_rec 1,0): calore
    recuperato nominale 960.000, ma il residuo e'
    zero (troncamento max(0, ...): l'eccesso di
    780.000 viene sprecato, senza export),
    E_pdc zero, risparmio 16.000, VAN 86.074,53,
    payback 5, breakeven 10,00, CONVIENTE."""
    bc = _variante(eta_rec=1.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(960000.0)
    assert bc["q_risc_res_kwh_anno"] == 0.0
    assert bc["e_pdc_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(16000.0)
    assert bc["van"] == pytest.approx(86074.52861088944)
    assert bc["payback"] == 5
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(10.0)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_pista_dimezzata_conviente():
    """Pista 900 m2: freddo 360.000, scarto 480.000,
    recupero 72.000, residuo 108.000, E_pdc
    30.857,14, risparmio 8.285,71, VAN 6.002,88
    ancora positiva, CONVIENTE con payback 10 e
    breakeven 48,57: la pista piu' piccola produce
    meno calore di scarto e il caso si stringe, ma
    regge."""
    bc = _variante(superficie_pista_m2=900)
    assert bc["q_freddo_kwh_anno"] == pytest.approx(360000.0)
    assert bc["q_scart_kwh_anno"] == pytest.approx(480000.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(72000.0)
    assert bc["q_risc_res_kwh_anno"] == pytest.approx(108000.0)
    assert bc["e_pdc_kwh_anno"] == pytest.approx(30857.14285714286)
    assert bc["risparmio_eur_anno"] == pytest.approx(8285.714285714283)
    assert bc["van"] == pytest.approx(6002.880887782)
    assert bc["payback"] == 10
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(48.57142857142859)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_alto_marginale_e_conviente():
    bc = _variante(capex_eur=140000)
    assert bc["risparmio_eur_anno"] == pytest.approx(13428.57142857142)
    assert bc["van"] == pytest.approx(-616.0206301464632)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"
    bc2 = _variante(capex_eur=120000)
    assert bc2["van"] == pytest.approx(19383.979369853547)
    assert bc2["payback"] == 9
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex_eur=0)
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(139383.97936985357, rel=1e-6)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(121428.5714285713)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(23691.869049053108)
    assert bc2["payback"] == 6
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_el_alto_e_cop_basso():
    """Elettricita' 350 EUR/MWh e COP pompa di calore
    2,5 danno lo stesso risparmio (12.400,00) per
    vie diverse: nel primo caso il chiller costa di
    piu' in entrambi i costi (si elide) e la pompa
    di calore costa 3.600,00; nel secondo la pompa
    di calore assorbe 14.400 kWh_e. In entrambi i
    casi VAN 48.707,76, breakeven 28,00, CONVIENTE
    con payback 7."""
    bc = _variante(p_el_eur_mwh=350)
    assert bc["risparmio_eur_anno"] == pytest.approx(12400.0)
    assert bc["van"] == pytest.approx(48707.759673439345)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(28.0)
    assert bc["payback"] == 7
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(cop_pdc=2.5)
    assert bc2["e_pdc_kwh_anno"] == pytest.approx(14400.0)
    assert bc2["risparmio_eur_anno"] == pytest.approx(12400.0)
    assert bc2["van"] == pytest.approx(48707.759673439345)
    assert bc2["breakeven_gas_eur_mwh"] == pytest.approx(28.0)
    assert bc2["verdetto"] == "CONVIENTE"


def test_monotonia_prezzo_gas_crescente():
    base = mh787_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas_eur_mwh=91)["risparmio_eur_anno"]
    basso = _variante(p_gas_eur_mwh=89)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(200.0)
    assert base - basso == pytest.approx(200.0)


def test_monotonia_pista_crescente_con_tetto():
    """Il risparmio cresce con la pista finche' il
    calore recuperato non copre tutto il
    riscaldamento; oltre, il residuo e' zero e il
    risparmio si ferma a 16.000 (solo O&M e gas
    risparmiato, senza piu' elettricita' pompa di
    calore)."""
    assert _variante(superficie_pista_m2=900)["risparmio_eur_anno"] < \
        mh787_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(superficie_pista_m2=3600)["risparmio_eur_anno"] == \
        pytest.approx(16000.0)
    assert _variante(superficie_pista_m2=3600)["risparmio_eur_anno"] > \
        mh787_demo_calcoli()["risparmio_eur_anno"]


def test_demo_deterministica_due_chiamate():
    a = mh787_demo_calcoli()
    b = mh787_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh787_demo().keys()) == {
        "superficie_pista_m2", "q_freddo_kwh_m2_anno",
        "cop_freddo", "superficie_risc_m2",
        "q_risc_kwh_m2_anno",
        "eta_caldaia", "eta_rec", "cop_pdc",
        "p_gas_eur_mwh", "p_el_eur_mwh",
        "om_base_eur_anno", "om_alt_eur_anno",
        "capex_eur", "wacc_pct", "vita_anni",
        "f_gas_t_per_mwh", "f_el_t_per_mwh",
        "tolleranza_pct"}


# ---------------------------------------------------------------- degenere
def test_degenere_cop_uguale_uno_sollevela():
    with pytest.raises(ValueError):
        _variante(cop_freddo=1.0)
    with pytest.raises(ValueError):
        _variante(cop_pdc=1.0)


def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"superficie_pista_m2": 0},
               {"superficie_pista_m2": -10},
               {"q_freddo_kwh_m2_anno": 0},
               {"q_freddo_kwh_m2_anno": -10},
               {"cop_freddo": 1.0}, {"cop_freddo": 0.5},
               {"superficie_risc_m2": 0},
               {"superficie_risc_m2": -10},
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
        assert mh787_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"superficie_pista_m2": "1800"},
               {"superficie_pista_m2": float("nan")},
               {"p_gas_eur_mwh": float("inf")},
               {"capex_eur": True},
               {"q_freddo_kwh_m2_anno": "400"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh787_valida(**d)["valido"] is False


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    """Differenza chiave: risparmio <= 0 NON solleva
    negli helper (resta calcolabile con flussi, VAN,
    TIR e payback), ma il verdetto e' NON_CALCOLABILE
    e la UI salta KPI, grafico, tabella e CSV."""
    for kw in ({"p_gas_eur_mwh": 0},
               {"p_gas_eur_mwh": 22.8571428571429},
               {"q_risc_kwh_m2_anno": 0}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] <= 0.0
        assert bc["verdetto"] == "NON_CALCOLABILE"
        assert bc["flussi"]


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh787_demo_calcoli()
    testo = mh787_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_gas_eur_mwh" in testo
    assert "co2_evitata_t_anno" in testo
    assert "q_freddo_kwh_anno" in testo
    assert "q_scart_kwh_anno" in testo
    assert "q_risc_res_kwh_anno" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh787_demo_calcoli()
    testo = mh787_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"q_freddo_kwh_anno;{bc['q_freddo_kwh_anno']}" in testo
    assert f"gas_base_kwh_anno;{bc['gas_base_kwh_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh787_demo_calcoli()
    testo = mh787_csv(bc, _demo_kwargs())
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
    return ["mh" + "78" + "6", "st" + "78" + "6",
            "tab" + "78" + "6", "tab" + "78" + "5"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w788_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w788_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab787:")


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w788_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w788_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st787_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) >= 19
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w788_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 2
    # Entrambe le guard (input degenere e risparmio <= 0)
    # stanno prima di KPI / grafico / tabella / CSV.
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w788_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def787[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w788_ui.py")
        usate = set(re.findall(r'_def787\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 18
        assert usate <= set(mh787_demo().keys())
