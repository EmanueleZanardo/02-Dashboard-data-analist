"""Test tab794 "Ospedale: pompa di calore reversibile
+ recupero calore ventilazione batte la
caldaia a gas + chiller?"
(titolo completo nel frammento UI).
Contenuto pronto da scrivere in repo come test
della tab ospedale.

Business case deterministico di un ospedale
con funzionamento continuo 24h, guidato dalla
superficie complessiva in m2 (reparti + sale
operatorie) per riscaldamento e raffrescamento
e dal numero di posti letto per l'acqua calda
sanitaria. Riscaldamento ospedale Q_risc = S x
q_risc kWh_th/anno; raffrescamento ospedale
Q_raff = S x q_raff kWh_c/anno; ACS posti letto
Q_acs = N x q_acs_letto kWh_th/anno; calore
recuperato dall'aria esausta di ventilazione
Q_rec = eta_rec x f_vent x Q_risc kWh_th/anno,
SOLO dalla ventilazione (per costruzione
Q_rec <= Q_risc, perche' eta_rec x f_vent <= 1);
riscaldamento residuo Q_risc_res =
max(0, Q_risc - Q_rec) kWh_th/anno (l'eccesso
viene sprecato, senza export); gas baseline
G_base = (Q_risc + Q_acs) / eta_caldaia
kWh/anno; elettricita' chiller E_chiller =
Q_raff / COP_chiller kWh_e/anno; elettricita'
pompa di calore in riscaldamento E_pdc_risc =
Q_risc_res / COP_risc kWh_e/anno; per ACS
E_pdc_acs = Q_acs / COP_acs kWh_e/anno; in
raffrescamento E_pdc_raff = Q_raff / COP_raff
kWh_e/anno; C_base = E_chiller / 1000 x p_el
+ G_base / 1000 x p_gas + O&M_base EUR/anno;
C_alt = (E_pdc_risc + E_pdc_acs + E_pdc_raff)
/ 1000 x p_el + O&M_alt EUR/anno (prezzi
EUR/MWh, energie kWh: / 1000 esatto);
risparmio = C_base - C_alt; CO2_base =
G_base / 1000 x f_gas + E_chiller / 1000 x f_el
t/anno; CO2_alt = (E_pdc_risc + E_pdc_acs +
E_pdc_raff) / 1000 x f_el t/anno; CO2_evitata
= CO2_base - CO2_alt; flussi [-CAPEX,
risparmio x vita]; VAN, TIR, payback (primo
anno con cumulato >= 0); breakeven gas
p_gas_be = (C_alt - E_chiller / 1000 x p_el
- O&M_base) x 1000 / G_base EUR/MWh, None se
G_base <= 0 o numeratore < 0, SOGLIA MINIMA
quando esiste. Verdetto: NON_CALCOLABILE se
risparmio <= 0 (guard degenere: UI salta KPI,
grafico, tabella e CSV); altrimenti CONVIENTE
se VAN > 0, MARGINALE se VAN negativa entro
tolleranza % del CAPEX, NON_CONVIENTE se VAN
negativa oltre la tolleranza. Distinzione
esplicita: distinto dall'albergo (pernottamento
turistico, ACS docce ospiti), dalla scuola
(chiusure stagionali, aule + mensa), dalla
piscina (vasca riscaldata) e dalla palestra
(docce utenti senza degenza): qui funzionamento
24h continuo, reparti + sale operatorie con
alti ricambi d'aria; driver = m2 per
riscaldamento/raffrescamento + posti letto per
ACS; recupero SOLO da ventilazione (aria
esausta) sul riscaldamento.

Demo (ospedale): 20.000 m2 complessivi a 120
kWh_th/m2/anno di riscaldamento e 100
kWh_c/m2/anno di raffrescamento, 200 posti
letto a 4.000 kWh_th/letto/anno di ACS, quota
ventilazione 0,60, recupero 0,55, caldaia 0,90,
chiller COP 3,0, pompa di calore reversibile
COP riscaldamento 3,8, COP ACS 3,0 e COP
raffrescamento 3,4, gas 90, el 250 EUR/MWh,
O&M base 40.000, alt 60.000, CAPEX 800.000,
WACC 5 %, vita 15, f_gas 0,20, f_el 0,35,
tolleranza 10 % del CAPEX. Valori calcolati
eseguendo mh794_demo_calcoli(): Q_risc
2.400.000, Q_raff 2.000.000, Q_acs 800.000,
Q_rec 792.000, Q_risc_res 1.608.000, G_base
3.555.555,5555555555, E_chiller 666.666,6666666666,
E_pdc_risc 423.157,89473684214, E_pdc_acs
266.666,6666666667, E_pdc_raff 588.235,2941176471,
C_base 526.666,6666666666, C_alt
379.514,963880289, risparmio 147.151,70278637763,
CO2_base 944,4444444444446, CO2_alt
447,3209494324045, CO2_evitata
497,12349501204005, VAN 727.384,3546585856,
TIR 16,543085580790663 %, payback 6,
breakeven gas 48,613583591331285, verdetto
CONVIENTE.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w795_helpers import (
    demo_calcoli,
    mh794_breakeven_gas,
    mh794_c_alt,
    mh794_c_base,
    mh794_calcola,
    mh794_co2_alt,
    mh794_co2_base,
    mh794_co2_evitata,
    mh794_cop,
    mh794_csv,
    mh794_demo,
    mh794_demo_calcoli,
    mh794_e_chiller,
    mh794_e_pdc_acs,
    mh794_e_pdc_raff,
    mh794_e_pdc_risc,
    mh794_eta,
    mh794_eta_rec,
    mh794_f_vent,
    mh794_flussi,
    mh794_gas,
    mh794_int_pos,
    mh794_num,
    mh794_nneg,
    mh794_payback,
    mh794_pct_tolleranza,
    mh794_pct_wacc,
    mh794_pos,
    mh794_q_acs,
    mh794_q_raff,
    mh794_q_rec,
    mh794_q_risc,
    mh794_q_risc_res,
    mh794_risparmio,
    mh794_tir,
    mh794_valida,
    mh794_van,
    mh794_verdetto,
)

_DEMO = {
    "q_risc_kwh_anno": 2400000.0,
    "q_raff_kwh_anno": 2000000.0,
    "q_acs_kwh_anno": 800000.0,
    "q_rec_kwh_anno": 792000.0,
    "q_risc_res_kwh_anno": 1608000.0,
    "gas_base_kwh_anno": 3555555.5555555555,
    "e_chiller_kwh_anno": 666666.6666666666,
    "e_pdc_risc_kwh_anno": 423157.89473684214,
    "e_pdc_acs_kwh_anno": 266666.6666666667,
    "e_pdc_raff_kwh_anno": 588235.2941176471,
    "c_base_eur_anno": 526666.6666666666,
    "c_alt_eur_anno": 379514.963880289,
    "risparmio_eur_anno": 147151.70278637763,
    "co2_base_t_anno": 944.4444444444446,
    "co2_alt_t_anno": 447.3209494324045,
    "co2_evitata_t_anno": 497.12349501204005,
    "van": 727384.3546585856,
    "tir": 16.543085580790663,
    "breakeven_gas_eur_mwh": 48.613583591331285,
}


def _demo_kwargs():
    return dict(mh794_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh794_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh794_num(3, "x") == 3.0
    assert mh794_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh794_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh794_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh794_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh794_pos(0, "x")
    with pytest.raises(ValueError):
        mh794_pos(-1, "x")
    assert mh794_pos(0.5, "x") == 0.5


def test_cop_maggiore_di_uno():
    assert mh794_cop(3.8, "x") == 3.8
    assert mh794_cop(1.01, "x") == 1.01
    with pytest.raises(ValueError):
        mh794_cop(1.0, "x")
    with pytest.raises(ValueError):
        mh794_cop(0.5, "x")
    with pytest.raises(ValueError):
        mh794_cop(0, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh794_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh794_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh794_int_pos(0, "x")


def test_eta_limiti():
    assert mh794_eta(1.0, "x") == 1.0
    assert mh794_eta(0.9, "x") == 0.9
    with pytest.raises(ValueError):
        mh794_eta(0, "x")
    with pytest.raises(ValueError):
        mh794_eta(1.01, "x")


def test_eta_rec_limiti():
    assert mh794_eta_rec(0.0, "x") == 0.0
    assert mh794_eta_rec(1.0, "x") == 1.0
    assert mh794_eta_rec(0.55, "x") == 0.55
    with pytest.raises(ValueError):
        mh794_eta_rec(-0.1, "x")
    with pytest.raises(ValueError):
        mh794_eta_rec(1.01, "x")


def test_f_vent_limiti():
    assert mh794_f_vent(0.0, "x") == 0.0
    assert mh794_f_vent(1.0, "x") == 1.0
    assert mh794_f_vent(0.60, "x") == 0.60
    with pytest.raises(ValueError):
        mh794_f_vent(-0.1, "x")
    with pytest.raises(ValueError):
        mh794_f_vent(1.01, "x")


def test_pct_wacc_limiti():
    assert mh794_pct_wacc(0, "x") == 0.0
    assert mh794_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh794_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh794_pct_tolleranza(0, "x") == 0.0
    assert mh794_pct_tolleranza(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh794_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh794_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_q_risc_q_raff_q_acs():
    assert mh794_q_risc(20000, 120) == 2400000.0
    assert mh794_q_risc(20000, 0) == 0.0
    assert mh794_q_raff(20000, 100) == 2000000.0
    assert mh794_q_raff(20000, 0) == 0.0
    assert mh794_q_acs(200, 4000) == 800000.0
    assert mh794_q_acs(200, 0) == 0.0
    assert mh794_q_acs(100, 4000) == 400000.0
    with pytest.raises(ValueError):
        mh794_q_risc(0, 120)
    with pytest.raises(ValueError):
        mh794_q_risc(20000, -10)
    with pytest.raises(ValueError):
        mh794_q_raff(0, 100)
    with pytest.raises(ValueError):
        mh794_q_raff(20000, -10)
    with pytest.raises(ValueError):
        mh794_q_acs(0, 4000)
    with pytest.raises(ValueError):
        mh794_q_acs(200.5, 4000)
    with pytest.raises(ValueError):
        mh794_q_acs(200, -10)


def test_q_rec_solo_ventilazione():
    assert mh794_q_rec(2400000, 0.60, 0.55) == 792000.0
    assert mh794_q_rec(2400000, 0.60, 0) == 0.0
    assert mh794_q_rec(2400000, 0, 0.55) == 0.0
    assert mh794_q_rec(2400000, 0.60, 1.0) == 1440000.0
    assert mh794_q_rec(2400000, 1.0, 1.0) == 2400000.0
    with pytest.raises(ValueError):
        mh794_q_rec(2400000, 0.60, 1.01)
    with pytest.raises(ValueError):
        mh794_q_rec(2400000, 1.01, 0.55)
    with pytest.raises(ValueError):
        mh794_q_rec(2400000, -0.1, 0.55)


def test_q_risc_res_con_troncamento_a_zero():
    assert mh794_q_risc_res(2400000, 792000.0) == 1608000.0
    assert mh794_q_risc_res(2400000, 2400000.0) == 0.0
    assert mh794_q_risc_res(2400000, 3000000.0) == 0.0
    with pytest.raises(ValueError):
        mh794_q_risc_res(2400000, -1)


def test_gas_e_chiller():
    assert mh794_gas(2400000, 800000, 0.9) == pytest.approx(3555555.5555555555)
    assert mh794_gas(0, 0, 0.9) == 0.0
    assert mh794_e_chiller(2000000, 3.0) == pytest.approx(666666.6666666666)
    assert mh794_e_chiller(0, 3.0) == 0.0
    with pytest.raises(ValueError):
        mh794_gas(2400000, 800000, 0)
    with pytest.raises(ValueError):
        mh794_gas(2400000, 800000, 1.01)
    with pytest.raises(ValueError):
        mh794_e_chiller(2000000, 1.0)


def test_e_pdc_risc_acs_raff():
    assert mh794_e_pdc_risc(1608000.0, 3.8) == pytest.approx(423157.89473684214)
    assert mh794_e_pdc_risc(0, 3.8) == 0.0
    assert mh794_e_pdc_acs(800000.0, 3.0) == pytest.approx(266666.6666666667)
    assert mh794_e_pdc_acs(0, 3.0) == 0.0
    assert mh794_e_pdc_raff(2000000, 3.4) == pytest.approx(588235.2941176471)
    assert mh794_e_pdc_raff(0, 3.4) == 0.0
    with pytest.raises(ValueError):
        mh794_e_pdc_risc(1608000.0, 1.0)
    with pytest.raises(ValueError):
        mh794_e_pdc_acs(800000.0, 0.5)
    with pytest.raises(ValueError):
        mh794_e_pdc_raff(2000000, 1.0)


def test_c_base_c_alt_scomposizione():
    assert mh794_c_base(666666.6666666666, 250, 3555555.5555555555, 90,
                        40000) == pytest.approx(526666.6666666666)
    assert mh794_c_base(666666.6666666666, 250, 3555555.5555555555, 0,
                        40000) == pytest.approx(206666.66666666666)
    assert mh794_c_alt(423157.89473684214, 266666.6666666667, 588235.2941176471,
                       250, 60000) == pytest.approx(379514.963880289)
    assert mh794_c_alt(0, 0, 0, 250, 60000) == pytest.approx(60000.0)
    with pytest.raises(ValueError):
        mh794_c_base(666666.6666666666, 250, 3555555.5555555555, -1, 40000)
    with pytest.raises(ValueError):
        mh794_c_alt(423157.89473684214, 266666.6666666667, 588235.2941176471,
                    250, -1)


def test_risparmio_segno():
    assert mh794_risparmio(526666.6666666666, 379514.963880289) == pytest.approx(147151.70278637763)
    assert mh794_risparmio(379514.963880289, 379514.963880289) == 0.0
    assert mh794_risparmio(206666.66666666666, 379514.963880289) == pytest.approx(-172848.29721362234)


def test_co2_base_alt_evitata():
    assert mh794_co2_base(3555555.5555555555, 0.20, 666666.6666666666,
                          0.35) == pytest.approx(944.4444444444446)
    assert mh794_co2_alt(423157.89473684214, 266666.6666666667, 588235.2941176471,
                         0.35) == pytest.approx(447.3209494324045)
    assert mh794_co2_evitata(3555555.5555555555, 0.20, 666666.6666666666,
                             423157.89473684214, 266666.6666666667,
                             588235.2941176471,
                             0.35) == pytest.approx(497.12349501204005)
    assert mh794_co2_base(0, 0.20, 0, 0.35) == pytest.approx(0.0)
    assert mh794_co2_alt(0, 0, 0, 0.35) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh794_co2_base(3555555.5555555555, -0.10, 666666.6666666666, 0.35)
    with pytest.raises(ValueError):
        mh794_co2_alt(423157.89473684214, 266666.6666666667, 588235.2941176471,
                      -0.10)


def test_breakeven_gas_demo_e_varianti():
    assert mh794_breakeven_gas(379514.963880289, 666666.6666666666, 250,
                               40000,
                               3555555.5555555555) == \
        pytest.approx(48.613583591331285)
    assert mh794_breakeven_gas(431620.2270381837, 666666.6666666666, 250,
                               40000,
                               3555555.5555555555) == \
        pytest.approx(63.26818885448918)
    assert mh794_breakeven_gas(336883.38493292057, 666666.6666666666, 250,
                               40000,
                               3555555.5555555555) == \
        pytest.approx(36.623452012383915)
    assert mh794_breakeven_gas(379514.963880289, 666666.6666666666, 250,
                               40000, 0) is None
    assert mh794_breakeven_gas(200, 666666.6666666666, 250, 40000,
                               3555555.5555555555) is None
    with pytest.raises(ValueError):
        mh794_breakeven_gas(379514.963880289, 666666.6666666666, 250,
                            40000, -1)


def test_breakeven_verifica_pareggio():
    bc = _variante(p_gas_eur_mwh=48.613583591331285)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    demo = mh794_demo_calcoli()
    assert (demo["c_alt_eur_anno"]
            - demo["e_chiller_kwh_anno"] / 1000.0
            * demo["p_el_eur_mwh"]
            - demo["om_base_eur_anno"]) * 1000.0 / demo["gas_base_kwh_anno"] == \
        pytest.approx(demo["breakeven_gas_eur_mwh"])


def test_breakeven_soglia_minima():
    be = mh794_demo_calcoli()["breakeven_gas_eur_mwh"]
    assert _variante(p_gas_eur_mwh=be + 1)[
        "c_alt_eur_anno"] < _variante(p_gas_eur_mwh=be + 1)[
        "c_base_eur_anno"]
    assert _variante(p_gas_eur_mwh=be - 1)[
        "c_alt_eur_anno"] > _variante(p_gas_eur_mwh=be - 1)[
        "c_base_eur_anno"]


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh794_flussi(800000, 147151.70278637763, 15)
    assert len(fl) == 16
    assert fl[0] == -800000
    assert all(f == 147151.70278637763 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh794_demo_calcoli()
    assert bc["van"] == pytest.approx(727384.3546585856)
    assert mh794_van([-800000] + [147151.70278637763] * 15,
                     0) == pytest.approx(1407275.5417956645)
    assert mh794_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh794_demo_calcoli()
    assert bc["tir"] == pytest.approx(16.543085580790663)
    assert mh794_tir([-800000] + [147151.70278637763] * 15) == \
        pytest.approx(0.16543085580790663)
    tir = mh794_tir([-800000] + [147151.70278637763] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-800000] + [147151.70278637763] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh794_payback([-800000] + [147151.70278637763] * 15) == 6
    assert mh794_payback([-800000] + [-1000.0] * 15) is None
    assert mh794_payback([0] + [147151.70278637763] * 15) == 0
    assert mh794_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh794_verdetto(147151.70278637763, 727384.3546585856, 800000,
                          10.0) == "CONVIENTE"
    assert mh794_verdetto(147151.70278637763, 0.0, 800000, 10.0) == "MARGINALE"
    assert mh794_verdetto(147151.70278637763, -80000.0, 800000, 10.0) == "MARGINALE"
    assert mh794_verdetto(147151.70278637763, -80000.01, 800000, 10.0) == "NON_CONVIENTE"
    assert mh794_verdetto(147151.70278637763, -379779.17, 800000, 10.0) == "NON_CONVIENTE"
    assert mh794_verdetto(0.0, 727384.3546585856, 800000,
                          10.0) == "NON_CALCOLABILE"
    assert mh794_verdetto(-30626.07499140012, -1117888.19, 800000,
                          10.0) == "NON_CALCOLABILE"
    assert mh794_verdetto(None, 727384.3546585856, 800000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh794_verdetto(float("nan"), 727384.35, 800000, 10.0)
    with pytest.raises(ValueError):
        mh794_verdetto(147151.70278637763, 727384.35, -1, 10.0)
    with pytest.raises(ValueError):
        mh794_verdetto(147151.70278637763, 727384.35, 800000, 100.1)


def test_valida_demo_ok():
    v = mh794_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("superficie_m2", "20000"),
                       ("superficie_m2", float("nan")),
                       ("superficie_m2", float("inf")),
                       ("superficie_m2", True),
                       ("p_gas_eur_mwh", None),
                       ("q_risc_kwh_m2_anno", "120")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh794_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("superficie_m2", 0),
                          ("superficie_m2", -10),
                          ("q_risc_kwh_m2_anno", -0.1),
                          ("q_raff_kwh_m2_anno", -0.1),
                          ("n_letti", 0), ("n_letti", 200.5),
                          ("q_acs_letto_kwh_anno", -0.1),
                          ("f_vent", -0.1), ("f_vent", 1.01),
                          ("eta_rec", -0.1),
                          ("eta_rec", 1.01),
                          ("eta_caldaia", 0),
                          ("eta_caldaia", 1.01),
                          ("cop_chiller", 1.0),
                          ("cop_chiller", 0.5),
                          ("cop_risc", 1.0),
                          ("cop_acs", 1.0),
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
        assert mh794_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"q_risc_kwh_m2_anno": 0,
              "q_raff_kwh_m2_anno": 0,
              "q_acs_letto_kwh_anno": 0,
              "f_vent": 0,
              "eta_rec": 0,
              "p_gas_eur_mwh": 0,
              "p_el_eur_mwh": 0,
              "om_base_eur_anno": 0, "om_alt_eur_anno": 0,
              "capex_eur": 0, "wacc_pct": 0,
              "f_gas_t_per_mwh": 0, "f_el_t_per_mwh": 0,
              "tolleranza_pct": 0})
    assert mh794_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["eta_rec"] = 1
    d["f_vent"] = 1
    d["q_risc_kwh_m2_anno"] = 130
    assert mh794_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh794_demo()
    assert d["superficie_m2"] == 20000
    assert d["q_risc_kwh_m2_anno"] == 120
    assert d["q_raff_kwh_m2_anno"] == 100
    assert d["n_letti"] == 200
    assert d["q_acs_letto_kwh_anno"] == 4000
    assert d["f_vent"] == 0.60
    assert d["eta_rec"] == 0.55
    assert d["eta_caldaia"] == 0.90
    assert d["cop_chiller"] == 3.0
    assert d["cop_risc"] == 3.8
    assert d["cop_acs"] == 3.0
    assert d["cop_raff"] == 3.4
    assert d["p_gas_eur_mwh"] == 90
    assert d["p_el_eur_mwh"] == 250
    assert d["om_base_eur_anno"] == 40000
    assert d["om_alt_eur_anno"] == 60000
    assert d["capex_eur"] == 800000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["f_gas_t_per_mwh"] == 0.20
    assert d["f_el_t_per_mwh"] == 0.35
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    bc = mh794_demo_calcoli()
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
    bc = mh794_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(526666.6666666666)
    assert bc["c_alt_eur_anno"] == pytest.approx(379514.963880289)
    assert bc["risparmio_eur_anno"] == pytest.approx(147151.70278637763)
    assert bc["co2_base_t_anno"] == pytest.approx(944.4444444444446)
    assert bc["co2_alt_t_anno"] == pytest.approx(447.3209494324045)
    assert bc["co2_evitata_t_anno"] == pytest.approx(497.12349501204005)
    assert bc["gas_base_kwh_anno"] == pytest.approx(3555555.5555555555)


def test_demo_flussi_e_cumulato():
    bc = mh794_demo_calcoli()
    assert bc["flussi"][0] == -800000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(147151.70278637763) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -800000
    assert righe.iloc[4]["Cumulato (EUR)"] == pytest.approx(-211393.18885448948)
    assert righe.iloc[5]["Cumulato (EUR)"] == pytest.approx(-64241.486068111844)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(1407275.5417956645)


def test_demo_tabella_righe():
    bc = mh794_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Riscaldamento ospedale (kWh_th/anno)"] == pytest.approx(2400000.0)
    assert mappa["Raffrescamento ospedale (kWh_c/anno)"] == pytest.approx(2000000.0)
    assert mappa["ACS posti letto (kWh_th/anno)"] == pytest.approx(800000.0)
    assert mappa["Calore recuperato ventilazione (kWh_th/anno)"] == pytest.approx(792000.0)
    assert mappa["Riscaldamento residuo (kWh_th/anno)"] == pytest.approx(1608000.0)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(3555555.5555555555)
    assert mappa["Elettricita' chiller (kWh_e/anno)"] == pytest.approx(666666.6666666666)
    assert mappa["Elettricita' pompa di calore riscaldamento (kWh_e/anno)"] == pytest.approx(423157.89473684214)
    assert mappa["Elettricita' pompa di calore ACS (kWh_e/anno)"] == pytest.approx(266666.6666666667)
    assert mappa["Elettricita' pompa di calore raffrescamento (kWh_e/anno)"] == pytest.approx(588235.2941176471)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(526666.6666666666)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(379514.963880289)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(147151.70278637763)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(497.12349501204005)
    assert mappa["Payback (anni)"] == 6
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] == \
        pytest.approx(48.613583591331285)


def test_demo_coerenza_interna():
    bc = mh794_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["q_risc_kwh_anno"] == pytest.approx(
        bc["superficie_m2"] * bc["q_risc_kwh_m2_anno"])
    assert bc["q_raff_kwh_anno"] == pytest.approx(
        bc["superficie_m2"] * bc["q_raff_kwh_m2_anno"])
    assert bc["q_acs_kwh_anno"] == pytest.approx(
        bc["n_letti"] * bc["q_acs_letto_kwh_anno"])
    assert bc["q_rec_kwh_anno"] == pytest.approx(
        bc["eta_rec"] * bc["f_vent"] * bc["q_risc_kwh_anno"])
    assert bc["q_risc_res_kwh_anno"] == pytest.approx(
        max(0.0, bc["q_risc_kwh_anno"] - bc["q_rec_kwh_anno"]))
    assert bc["gas_base_kwh_anno"] == pytest.approx(
        (bc["q_risc_kwh_anno"] + bc["q_acs_kwh_anno"])
        / bc["eta_caldaia"])
    assert bc["e_chiller_kwh_anno"] == pytest.approx(
        bc["q_raff_kwh_anno"] / bc["cop_chiller"])
    assert bc["e_pdc_risc_kwh_anno"] == pytest.approx(
        bc["q_risc_res_kwh_anno"] / bc["cop_risc"])
    assert bc["e_pdc_acs_kwh_anno"] == pytest.approx(
        bc["q_acs_kwh_anno"] / bc["cop_acs"])
    assert bc["e_pdc_raff_kwh_anno"] == pytest.approx(
        bc["q_raff_kwh_anno"] / bc["cop_raff"])
    assert bc["co2_evitata_t_anno"] == pytest.approx(
        bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])
    assert bc["c_base_eur_anno"] == pytest.approx(
        bc["e_chiller_kwh_anno"] / 1000.0 * bc["p_el_eur_mwh"]
        + bc["gas_base_kwh_anno"] / 1000.0 * bc["p_gas_eur_mwh"]
        + bc["om_base_eur_anno"])
    assert bc["c_alt_eur_anno"] == pytest.approx(
        (bc["e_pdc_risc_kwh_anno"] + bc["e_pdc_acs_kwh_anno"]
         + bc["e_pdc_raff_kwh_anno"])
        / 1000.0 * bc["p_el_eur_mwh"]
        + bc["om_alt_eur_anno"])


def test_demo_contro_riconteggio_indipendente():
    s_osp = 20000
    qr_spec, qf_spec = 120, 100
    nletti, qa_spec = 200, 4000
    fv, erec = 0.60, 0.55
    eta, copc, copr, copa, copf = 0.90, 3.0, 3.8, 3.0, 3.4
    pg, pel, omb, oma, cx = 90, 250, 40000, 60000, 800000
    fg, fel, wacc, vita = 0.20, 0.35, 5.0, 15
    qrisc = s_osp * qr_spec
    qraff = s_osp * qf_spec
    qacs = nletti * qa_spec
    qrec = erec * fv * qrisc
    qres = max(0.0, qrisc - qrec)
    gas = (qrisc + qacs) / eta
    ech = qraff / copc
    epr = qres / copr
    epa = qacs / copa
    epf = qraff / copf
    cb = ech / 1000.0 * pel + gas / 1000.0 * pg + omb
    ca = (epr + epa + epf) / 1000.0 * pel + oma
    risp = cb - ca
    co2b = gas / 1000.0 * fg + ech / 1000.0 * fel
    co2a = (epr + epa + epf) / 1000.0 * fel
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    be = (ca - ech / 1000.0 * pel - omb) * 1000.0 / gas
    bc = mh794_demo_calcoli()
    assert bc["q_risc_kwh_anno"] == pytest.approx(qrisc)
    assert bc["q_raff_kwh_anno"] == pytest.approx(qraff)
    assert bc["q_acs_kwh_anno"] == pytest.approx(qacs)
    assert bc["q_rec_kwh_anno"] == pytest.approx(qrec)
    assert bc["q_risc_res_kwh_anno"] == pytest.approx(qres)
    assert bc["gas_base_kwh_anno"] == pytest.approx(gas)
    assert bc["e_chiller_kwh_anno"] == pytest.approx(ech)
    assert bc["e_pdc_risc_kwh_anno"] == pytest.approx(epr)
    assert bc["e_pdc_acs_kwh_anno"] == pytest.approx(epa)
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
    assert bc["risparmio_eur_anno"] == pytest.approx(40485.036119711)
    assert bc["van"] == pytest.approx(-379779.16941401013)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_gas_40_non_calcolabile():
    bc = _variante(p_gas_eur_mwh=40)
    assert bc["risparmio_eur_anno"] == pytest.approx(-30626.07499140012)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_gas_zero_non_calcolabile():
    bc = _variante(p_gas_eur_mwh=0)
    assert bc["valid"] is True
    assert bc["c_base_eur_anno"] == pytest.approx(206666.66666666666)
    assert bc["risparmio_eur_anno"] == pytest.approx(-172848.29721362234)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_senza_recupero_conviente():
    bc = _variante(eta_rec=0)
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["q_risc_res_kwh_anno"] == pytest.approx(2400000.0)
    assert bc["e_pdc_risc_kwh_anno"] == pytest.approx(631578.947368421)
    assert bc["risparmio_eur_anno"] == pytest.approx(95046.43962848291)
    assert bc["van"] == pytest.approx(186549.5410902289)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(63.26818885448918)
    assert bc["payback"] == 9
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_recupero_totale_conviente():
    bc = _variante(eta_rec=1.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(1440000.0)
    assert bc["q_risc_res_kwh_anno"] == pytest.approx(960000.0)
    assert bc["e_pdc_risc_kwh_anno"] == pytest.approx(252631.57894736842)
    assert bc["risparmio_eur_anno"] == pytest.approx(189783.28173374606)
    assert bc["van"] == pytest.approx(1169885.565759969)
    assert bc["payback"] == 5
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(36.623452012383915)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_senza_raffrescamento_conviente():
    bc = _variante(q_raff_kwh_m2_anno=0)
    assert bc["q_raff_kwh_anno"] == 0.0
    assert bc["e_chiller_kwh_anno"] == 0.0
    assert bc["e_pdc_raff_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(127543.85964912281)
    assert bc["van"] == pytest.approx(523861.64802759455)
    assert bc["payback"] == 7
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(54.12828947368421)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_alto_marginale_e_non_conviente():
    bc = _variante(capex_eur=1600000)
    assert bc["risparmio_eur_anno"] == pytest.approx(147151.70278637763)
    assert bc["van"] == pytest.approx(-72615.64534141467)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"
    bc2 = _variante(capex_eur=1800000)
    assert bc2["van"] == pytest.approx(-272615.64534141484)
    assert bc2["payback"] == 13
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex_eur=0)
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(1527384.3546585857, rel=1e-6)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(1407275.5417956645)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(336266.443294594)
    assert bc2["payback"] == 6
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_el_alto_e_cop_risc_basso():
    bc = _variante(p_el_eur_mwh=350)
    assert bc["risparmio_eur_anno"] == pytest.approx(86012.38390092872)
    assert bc["van"] == pytest.approx(92779.1319403496)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(65.80901702786379)
    assert bc["payback"] == 10
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(cop_risc=2.5)
    assert bc2["e_pdc_risc_kwh_anno"] == pytest.approx(643200.0)
    assert bc2["risparmio_eur_anno"] == pytest.approx(92141.1764705882)
    assert bc2["van"] == pytest.approx(156393.90300035704)
    assert bc2["breakeven_gas_eur_mwh"] == pytest.approx(64.08529411764707)
    assert bc2["payback"] == 9
    assert bc2["verdetto"] == "CONVIENTE"


def test_monotonia_prezzo_gas_crescente():
    base = mh794_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas_eur_mwh=91)["risparmio_eur_anno"]
    basso = _variante(p_gas_eur_mwh=89)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(3555.5555555555557)
    assert base - basso == pytest.approx(3555.5555555555557)


def test_monotonia_recupero_crescente_con_tetto():
    assert _variante(eta_rec=0)["risparmio_eur_anno"] < \
        mh794_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(eta_rec=1.0)["risparmio_eur_anno"] > \
        mh794_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(f_vent=1.0, eta_rec=1.0)["q_rec_kwh_anno"] == \
        pytest.approx(2400000.0)
    assert _variante(f_vent=1.0, eta_rec=1.0)["q_risc_res_kwh_anno"] == 0.0


def test_demo_deterministica_due_chiamate():
    a = mh794_demo_calcoli()
    b = mh794_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh794_demo().keys()) == {
        "superficie_m2",
        "q_risc_kwh_m2_anno", "q_raff_kwh_m2_anno",
        "n_letti", "q_acs_letto_kwh_anno",
        "f_vent", "eta_rec",
        "eta_caldaia", "cop_chiller", "cop_risc",
        "cop_acs", "cop_raff",
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
               {"n_letti": 0}, {"n_letti": 200.5},
               {"q_acs_letto_kwh_anno": -0.1},
               {"f_vent": -0.1}, {"f_vent": 1.01},
               {"eta_rec": -0.1}, {"eta_rec": 1.01},
               {"eta_caldaia": 0}, {"eta_caldaia": 1.01},
               {"cop_chiller": 1.0}, {"cop_chiller": 0.5},
               {"cop_risc": 1.0}, {"cop_risc": 0.5},
               {"cop_acs": 1.0}, {"cop_acs": 0.5},
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
        assert mh794_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"superficie_m2": "20000"},
               {"superficie_m2": float("nan")},
               {"p_gas_eur_mwh": float("inf")},
               {"capex_eur": True},
               {"q_risc_kwh_m2_anno": "120"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh794_valida(**d)["valido"] is False


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    for kw in ({"p_gas_eur_mwh": 0},
               {"p_gas_eur_mwh": 48.613583591331285},
               {"p_gas_eur_mwh": 40}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] <= 0.0
        assert bc["verdetto"] == "NON_CALCOLABILE"
        assert bc["flussi"]


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh794_demo_calcoli()
    testo = mh794_csv(bc, _demo_kwargs())
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
    assert "e_pdc_acs_kwh_anno" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh794_demo_calcoli()
    testo = mh794_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"q_risc_kwh_anno;{bc['q_risc_kwh_anno']}" in testo
    assert f"gas_base_kwh_anno;{bc['gas_base_kwh_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh794_demo_calcoli()
    testo = mh794_csv(bc, _demo_kwargs())
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
    return ["mh" + "79" + "3", "st" + "79" + "3",
            "tab" + "79" + "3", "w" + "79" + "4"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w795_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w795_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab794:")


def test_registry_chain_tail_and_count():
    """Registry della nuova tab: il frammento UI apre la tab
    numero 794 (la coda della catena termina con la nuova tab
    e il conteggio atteso delle tab e' 794)."""
    src = _leggi("w795_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 794
    assert src.count("with tab794:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w795_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w795_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st794_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) >= 24
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w795_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 3
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w795_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def794[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w795_ui.py")
        usate = set(re.findall(r'_def794\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 22
        assert usate <= set(mh794_demo().keys())
