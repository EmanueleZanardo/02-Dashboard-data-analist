"""Test tab791 "Teatro: pompa di calore reversibile
+ recupero calore ventilazione sala batte la
caldaia a gas + chiller?"
(titolo completo nel frammento UI).
Contenuto pronto da scrivere in repo come test
della tab teatro.

Business case deterministico di un teatro
guidato da una sola superficie in m2: la sala
teatrale a uso serale concentrato.
Riscaldamento sala Q_risc = S x q_risc
kWh_th/anno; raffrescamento sala Q_raff = S x
q_raff kWh_c/anno; calore recuperato dalla
ventilazione per il pubblico Q_rec = eta_rec x
f_vent x Q_risc kWh_th/anno, SOLO dalla
ventilazione (per costruzione Q_rec <= Q_risc,
perche' eta_rec x f_vent <= 1); riscaldamento
residuo Q_risc_res = max(0, Q_risc - Q_rec)
kWh_th/anno (l'eccesso viene sprecato, senza
export); gas baseline G_base = Q_risc /
eta_caldaia kWh/anno; elettricita' chiller
E_chiller = Q_raff / COP_chiller kWh_e/anno;
elettricita' pompa di calore in riscaldamento
E_pdc_risc = Q_risc_res / COP_risc kWh_e/anno;
in raffrescamento E_pdc_raff = Q_raff /
COP_raff kWh_e/anno; C_base = E_chiller / 1000
x p_el + G_base / 1000 x p_gas + O&M_base
EUR/anno; C_alt = (E_pdc_risc + E_pdc_raff) /
1000 x p_el + O&M_alt EUR/anno (prezzi
EUR/MWh, energie kWh: / 1000 esatto);
risparmio = C_base - C_alt; CO2_base = G_base /
1000 x f_gas + E_chiller / 1000 x f_el t/anno;
CO2_alt = (E_pdc_risc + E_pdc_raff) / 1000 x
f_el t/anno; CO2_evitata = CO2_base - CO2_alt;
flussi [-CAPEX, risparmio x vita]; VAN, TIR,
payback (primo anno con cumulato >= 0);
breakeven gas p_gas_be = (C_alt - E_chiller /
1000 x p_el - O&M_base) x 1000 / G_base
EUR/MWh, None se G_base <= 0 o numeratore < 0,
SOGLIA MINIMA quando esiste. Verdetto:
NON_CALCOLABILE se risparmio <= 0 (guard
degenere: UI salta KPI, grafico, tabella e CSV);
altrimenti CONVIENTE se VAN > 0, MARGINALE se
VAN negativa entro tolleranza % del CAPEX,
NON_CONVIENTE se VAN negativa oltre la
tolleranza. Distinzione esplicita: NON la tab
delle sale espositive (una sola superficie
espositiva con orario diurno continuo, senza
ventilazione per il pubblico serale e senza uso
serale concentrato), NON la tab dei depositi
archivio (depositi con raffrescamento continuo,
anche quando le sale non raffrescano: nessun
fabbisogno di freddo continuo qui), NON la
scuola (aule + mensa con pasti, orari e
chiusure stagionali: nessuna mensa qui, nessuna
chiusura stagionale legata alle lezioni) e NON
la palestra (docce degli utenti con acqua calda
sanitaria + riscaldamento, recupero sulle acque
di scarico delle docce: nessuna acqua calda
sanitaria per docce qui, nessun recupero da
acque di scarico): qui il driver e' UNA sola
superficie, m2 di sala teatrale a uso serale
concentrato, e il calore recuperato viene SOLO
dalla ventilazione per il pubblico, come quota
del fabbisogno di riscaldamento della sala.

Demo (teatro): sala 3.000 m2 a 130
kWh_th/m2/anno di riscaldamento e 80
kWh_c/m2/anno di raffrescamento, quota
ventilazione 0,40, recupero 0,60, caldaia 0,90,
chiller COP 3,0, pompa di calore reversibile
COP riscaldamento 3,8 e COP raffrescamento
3,2, gas 90, el 250 EUR/MWh, O&M base 5.000,
alt 7.000, CAPEX 90.000, WACC 5 %, vita 15,
f_gas 0,20, f_el 0,35, tolleranza 10 % del
CAPEX. Valori calcolati eseguendo
mh791_demo_calcoli(): Q_risc 390.000, Q_raff
240.000, Q_rec 93.600, Q_risc_res 296.400,
G_base 433.333,3333333333, E_chiller 80.000,
E_pdc_risc 78.000, E_pdc_raff 75.000, C_base
64.000, C_alt 45.250, risparmio 18.750,
CO2_base 114,66666666666667, CO2_alt 53,55,
CO2_evitata 61,116666666666674, VAN
104.618,58821588605, TIR 19,37005123885597 %,
payback 5, breakeven gas 46,73076923076923,
verdetto CONVIENTE.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w792_helpers import (
    demo_calcoli,
    mh791_breakeven_gas,
    mh791_c_alt,
    mh791_c_base,
    mh791_calcola,
    mh791_co2_alt,
    mh791_co2_base,
    mh791_co2_evitata,
    mh791_cop,
    mh791_csv,
    mh791_demo,
    mh791_demo_calcoli,
    mh791_e_chiller,
    mh791_e_pdc_raff,
    mh791_e_pdc_risc,
    mh791_eta,
    mh791_eta_rec,
    mh791_f_vent,
    mh791_flussi,
    mh791_gas,
    mh791_int_pos,
    mh791_num,
    mh791_nneg,
    mh791_payback,
    mh791_pct_tolleranza,
    mh791_pct_wacc,
    mh791_pos,
    mh791_q_raff,
    mh791_q_rec,
    mh791_q_risc,
    mh791_q_risc_res,
    mh791_risparmio,
    mh791_tir,
    mh791_valida,
    mh791_van,
    mh791_verdetto,
)

_DEMO = {
    "q_risc_kwh_anno": 390000.0,
    "q_raff_kwh_anno": 240000.0,
    "q_rec_kwh_anno": 93600.0,
    "q_risc_res_kwh_anno": 296400.0,
    "gas_base_kwh_anno": 433333.3333333333,
    "e_chiller_kwh_anno": 80000.0,
    "e_pdc_risc_kwh_anno": 78000.0,
    "e_pdc_raff_kwh_anno": 75000.0,
    "c_base_eur_anno": 64000.0,
    "c_alt_eur_anno": 45250.0,
    "risparmio_eur_anno": 18750.0,
    "co2_base_t_anno": 114.66666666666667,
    "co2_alt_t_anno": 53.55,
    "co2_evitata_t_anno": 61.116666666666674,
    "van": 104618.58821588605,
    "tir": 19.37005123885597,
    "breakeven_gas_eur_mwh": 46.73076923076923,
}


def _demo_kwargs():
    return dict(mh791_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh791_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh791_num(3, "x") == 3.0
    assert mh791_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh791_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh791_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh791_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh791_pos(0, "x")
    with pytest.raises(ValueError):
        mh791_pos(-1, "x")
    assert mh791_pos(0.5, "x") == 0.5


def test_cop_maggiore_di_uno():
    assert mh791_cop(3.8, "x") == 3.8
    assert mh791_cop(1.01, "x") == 1.01
    with pytest.raises(ValueError):
        mh791_cop(1.0, "x")
    with pytest.raises(ValueError):
        mh791_cop(0.5, "x")
    with pytest.raises(ValueError):
        mh791_cop(0, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh791_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh791_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh791_int_pos(0, "x")


def test_eta_limiti():
    assert mh791_eta(1.0, "x") == 1.0
    assert mh791_eta(0.9, "x") == 0.9
    with pytest.raises(ValueError):
        mh791_eta(0, "x")
    with pytest.raises(ValueError):
        mh791_eta(1.01, "x")


def test_eta_rec_limiti():
    assert mh791_eta_rec(0.0, "x") == 0.0
    assert mh791_eta_rec(1.0, "x") == 1.0
    assert mh791_eta_rec(0.6, "x") == 0.6
    with pytest.raises(ValueError):
        mh791_eta_rec(-0.1, "x")
    with pytest.raises(ValueError):
        mh791_eta_rec(1.01, "x")


def test_f_vent_limiti():
    assert mh791_f_vent(0.0, "x") == 0.0
    assert mh791_f_vent(1.0, "x") == 1.0
    assert mh791_f_vent(0.40, "x") == 0.40
    with pytest.raises(ValueError):
        mh791_f_vent(-0.1, "x")
    with pytest.raises(ValueError):
        mh791_f_vent(1.01, "x")


def test_pct_wacc_limiti():
    assert mh791_pct_wacc(0, "x") == 0.0
    assert mh791_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh791_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh791_pct_tolleranza(0, "x") == 0.0
    assert mh791_pct_tolleranza(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh791_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh791_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_q_risc_e_q_raff():
    assert mh791_q_risc(3000, 130) == 390000.0
    assert mh791_q_risc(1500, 130) == 195000.0
    assert mh791_q_risc(3000, 0) == 0.0
    assert mh791_q_raff(3000, 80) == 240000.0
    assert mh791_q_raff(3000, 0) == 0.0
    assert mh791_q_raff(1500, 80) == 120000.0
    with pytest.raises(ValueError):
        mh791_q_risc(0, 130)
    with pytest.raises(ValueError):
        mh791_q_risc(3000, -10)
    with pytest.raises(ValueError):
        mh791_q_raff(0, 80)
    with pytest.raises(ValueError):
        mh791_q_raff(3000, -10)


def test_q_rec_solo_ventilazione():
    assert mh791_q_rec(390000, 0.40, 0.60) == 93600.0
    assert mh791_q_rec(390000, 0.40, 0) == 0.0
    assert mh791_q_rec(390000, 0, 0.60) == 0.0
    assert mh791_q_rec(390000, 0.40, 1.0) == 156000.0
    # Quota e rendimento massimi: il recupero eguaglia
    # il riscaldamento, mai lo supera.
    assert mh791_q_rec(390000, 1.0, 1.0) == 390000.0
    with pytest.raises(ValueError):
        mh791_q_rec(390000, 0.40, 1.01)
    with pytest.raises(ValueError):
        mh791_q_rec(390000, 1.01, 0.60)
    with pytest.raises(ValueError):
        mh791_q_rec(390000, -0.1, 0.60)


def test_q_risc_res_con_troncamento_a_zero():
    assert mh791_q_risc_res(390000, 93600.0) == 296400.0
    assert mh791_q_risc_res(390000, 390000.0) == 0.0
    # L'eccesso recuperato viene sprecato, senza export.
    assert mh791_q_risc_res(390000, 400000.0) == 0.0
    with pytest.raises(ValueError):
        mh791_q_risc_res(390000, -1)


def test_gas_e_chiller():
    assert mh791_gas(390000, 0.9) == pytest.approx(433333.3333333333)
    assert mh791_gas(0, 0.9) == 0.0
    assert mh791_e_chiller(240000, 3.0) == 80000.0
    assert mh791_e_chiller(0, 3.0) == 0.0
    with pytest.raises(ValueError):
        mh791_gas(390000, 0)
    with pytest.raises(ValueError):
        mh791_gas(390000, 1.01)
    with pytest.raises(ValueError):
        mh791_e_chiller(240000, 1.0)


def test_e_pdc_risc_e_raff():
    assert mh791_e_pdc_risc(296400.0, 3.8) == pytest.approx(78000.0)
    assert mh791_e_pdc_risc(0, 3.8) == 0.0
    assert mh791_e_pdc_raff(240000, 3.2) == pytest.approx(75000.0)
    assert mh791_e_pdc_raff(0, 3.2) == 0.0
    with pytest.raises(ValueError):
        mh791_e_pdc_risc(296400.0, 1.0)
    with pytest.raises(ValueError):
        mh791_e_pdc_raff(240000, 0.5)


def test_c_base_c_alt_scomposizione():
    assert mh791_c_base(80000.0, 250, 433333.3333333333, 90,
                        5000) == pytest.approx(64000.0)
    assert mh791_c_base(80000.0, 250, 433333.3333333333, 0,
                        5000) == pytest.approx(25000.0)
    assert mh791_c_alt(78000.0, 75000.0, 250,
                       7000) == pytest.approx(45250.0)
    assert mh791_c_alt(0, 0, 250, 7000) == pytest.approx(7000.0)
    with pytest.raises(ValueError):
        mh791_c_base(80000.0, 250, 433333.3333333333, -1, 5000)
    with pytest.raises(ValueError):
        mh791_c_alt(78000.0, 75000.0, 250, -1)


def test_risparmio_segno():
    assert mh791_risparmio(64000.0, 45250.0) == pytest.approx(18750.0)
    assert mh791_risparmio(45250.0, 45250.0) == 0.0
    assert mh791_risparmio(25000.0, 45250.0) == pytest.approx(-20250.0)


def test_co2_base_alt_evitata():
    assert mh791_co2_base(433333.3333333333, 0.20, 80000.0,
                          0.35) == pytest.approx(114.66666666666667)
    assert mh791_co2_alt(78000.0, 75000.0,
                         0.35) == pytest.approx(53.55)
    assert mh791_co2_evitata(433333.3333333333, 0.20, 80000.0,
                             78000.0, 75000.0,
                             0.35) == pytest.approx(61.116666666666674)
    assert mh791_co2_base(0, 0.20, 0, 0.35) == pytest.approx(0.0)
    assert mh791_co2_alt(0, 0, 0.35) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh791_co2_base(433333.3333333333, -0.10, 80000.0, 0.35)
    with pytest.raises(ValueError):
        mh791_co2_alt(78000.0, 75000.0, -0.10)


def test_breakeven_gas_demo_e_varianti():
    assert mh791_breakeven_gas(45250.0, 80000.0, 250,
                               5000,
                               433333.3333333333) == \
        pytest.approx(46.73076923076923)
    assert mh791_breakeven_gas(51407.89473684211, 80000.0, 250,
                               5000,
                               433333.3333333333) == \
        pytest.approx(60.94129554655871)
    assert mh791_breakeven_gas(41144.73684210527, 80000.0, 250,
                               5000,
                               433333.3333333333) == \
        pytest.approx(37.257085020242926)
    assert mh791_breakeven_gas(45250.0, 80000.0, 250,
                               5000, 0) is None
    # Numeratore negativo: alternativa gia' piu'
    # conveniente a prezzo gas zero -> nessun pareggio.
    assert mh791_breakeven_gas(200, 80000.0, 250, 5000,
                               433333.3333333333) is None
    with pytest.raises(ValueError):
        mh791_breakeven_gas(45250.0, 80000.0, 250,
                            5000, -1)


def test_breakeven_verifica_pareggio():
    """Al prezzo gas di pareggio i costi si eguagliano
    e il risparmio e' zero: scatta la guard
    NON_CALCOLABILE, non un verdetto di convenienza."""
    bc = _variante(p_gas_eur_mwh=46.73076923076923)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    demo = mh791_demo_calcoli()
    assert (demo["c_alt_eur_anno"]
            - demo["e_chiller_kwh_anno"] / 1000.0
            * demo["p_el_eur_mwh"]
            - demo["om_base_eur_anno"]) * 1000.0 / demo["gas_base_kwh_anno"] == \
        pytest.approx(demo["breakeven_gas_eur_mwh"])


def test_breakeven_soglia_minima():
    """Sopra la soglia l'alternativa vince, sotto perde."""
    be = mh791_demo_calcoli()["breakeven_gas_eur_mwh"]
    assert _variante(p_gas_eur_mwh=be + 1)[
        "c_alt_eur_anno"] < _variante(p_gas_eur_mwh=be + 1)[
        "c_base_eur_anno"]
    assert _variante(p_gas_eur_mwh=be - 1)[
        "c_alt_eur_anno"] > _variante(p_gas_eur_mwh=be - 1)[
        "c_base_eur_anno"]


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh791_flussi(90000, 18750.0, 15)
    assert len(fl) == 16
    assert fl[0] == -90000
    assert all(f == 18750.0 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh791_demo_calcoli()
    assert bc["van"] == pytest.approx(104618.58821588605)
    assert mh791_van([-90000] + [18750.0] * 15,
                     0) == pytest.approx(191250.0)
    assert mh791_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh791_demo_calcoli()
    assert bc["tir"] == pytest.approx(19.37005123885597)
    assert mh791_tir([-90000] + [18750.0] * 15) == \
        pytest.approx(0.1937005123885597)
    tir = mh791_tir([-90000] + [18750.0] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-90000] + [18750.0] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh791_payback([-90000] + [18750.0] * 15) == 5
    assert mh791_payback([-90000] + [-1000.0] * 15) is None
    assert mh791_payback([0] + [18750.0] * 15) == 0
    assert mh791_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh791_verdetto(18750.0, 104618.58821588605, 90000,
                          10.0) == "CONVIENTE"
    assert mh791_verdetto(18750.0, 0.0, 90000, 10.0) == "MARGINALE"
    assert mh791_verdetto(18750.0, -9000.0, 90000, 10.0) == "MARGINALE"
    assert mh791_verdetto(18750.0, -9000.01, 90000, 10.0) == "NON_CONVIENTE"
    assert mh791_verdetto(18750.0, -30316.97, 90000, 10.0) == "NON_CONVIENTE"
    assert mh791_verdetto(0.0, 104618.58821588605, 90000,
                          10.0) == "NON_CALCOLABILE"
    assert mh791_verdetto(-2916.6666666666715, -120274.0, 90000,
                          10.0) == "NON_CALCOLABILE"
    assert mh791_verdetto(None, 104618.58821588605, 90000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh791_verdetto(float("nan"), 104618.59, 90000, 10.0)
    with pytest.raises(ValueError):
        mh791_verdetto(18750.0, 104618.59, -1, 10.0)
    with pytest.raises(ValueError):
        mh791_verdetto(18750.0, 104618.59, 90000, 100.1)


def test_valida_demo_ok():
    v = mh791_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("superficie_sala_m2", "3000"),
                       ("superficie_sala_m2", float("nan")),
                       ("superficie_sala_m2", float("inf")),
                       ("superficie_sala_m2", True),
                       ("p_gas_eur_mwh", None),
                       ("q_risc_kwh_m2_anno", "130")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh791_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("superficie_sala_m2", 0),
                          ("superficie_sala_m2", -10),
                          ("q_risc_kwh_m2_anno", -0.1),
                          ("q_raff_kwh_m2_anno", -0.1),
                          ("f_vent", -0.1), ("f_vent", 1.01),
                          ("eta_rec", -0.1),
                          ("eta_rec", 1.01),
                          ("eta_caldaia", 0),
                          ("eta_caldaia", 1.01),
                          ("cop_chiller", 1.0),
                          ("cop_chiller", 0.5),
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
        assert mh791_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"q_risc_kwh_m2_anno": 0,
              "q_raff_kwh_m2_anno": 0,
              "f_vent": 0,
              "eta_rec": 0,
              "p_gas_eur_mwh": 0,
              "p_el_eur_mwh": 0,
              "om_base_eur_anno": 0, "om_alt_eur_anno": 0,
              "capex_eur": 0, "wacc_pct": 0,
              "f_gas_t_per_mwh": 0, "f_el_t_per_mwh": 0,
              "tolleranza_pct": 0})
    assert mh791_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["eta_rec"] = 1
    d["f_vent"] = 1
    d["q_risc_kwh_m2_anno"] = 130
    assert mh791_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh791_demo()
    assert d["superficie_sala_m2"] == 3000
    assert d["q_risc_kwh_m2_anno"] == 130
    assert d["q_raff_kwh_m2_anno"] == 80
    assert d["f_vent"] == 0.40
    assert d["eta_rec"] == 0.60
    assert d["eta_caldaia"] == 0.90
    assert d["cop_chiller"] == 3.0
    assert d["cop_risc"] == 3.8
    assert d["cop_raff"] == 3.2
    assert d["p_gas_eur_mwh"] == 90
    assert d["p_el_eur_mwh"] == 250
    assert d["om_base_eur_anno"] == 5000
    assert d["om_alt_eur_anno"] == 7000
    assert d["capex_eur"] == 90000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["f_gas_t_per_mwh"] == 0.20
    assert d["f_el_t_per_mwh"] == 0.35
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    """Tutti gli output numerici demo a tolleranza
    1e-9 relativa: confronto delle costanti _DEMO
    contro mh791_demo_calcoli()."""
    bc = mh791_demo_calcoli()
    for chiave, atteso in _DEMO.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert got == pytest.approx(atteso, rel=1e-9), chiave
    assert bc["payback"] == 5
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True
    assert demo_calcoli()["van"] == bc["van"]


def test_demo_calcoli_fisica_economia():
    bc = mh791_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(64000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(45250.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(18750.0)
    assert bc["co2_base_t_anno"] == pytest.approx(114.66666666666667)
    assert bc["co2_alt_t_anno"] == pytest.approx(53.55)
    assert bc["co2_evitata_t_anno"] == pytest.approx(61.116666666666674)
    assert bc["gas_base_kwh_anno"] == pytest.approx(433333.3333333333)


def test_demo_flussi_e_cumulato():
    bc = mh791_demo_calcoli()
    assert bc["flussi"][0] == -90000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(18750.0) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -90000
    assert righe.iloc[4]["Cumulato (EUR)"] == pytest.approx(-15000.0)
    assert righe.iloc[5]["Cumulato (EUR)"] == pytest.approx(3750.0)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(191250.0)


def test_demo_tabella_righe():
    bc = mh791_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Riscaldamento sala (kWh_th/anno)"] == pytest.approx(390000.0)
    assert mappa["Raffrescamento sala (kWh_c/anno)"] == pytest.approx(240000.0)
    assert mappa["Calore recuperato ventilazione (kWh_th/anno)"] == pytest.approx(93600.0)
    assert mappa["Riscaldamento residuo (kWh_th/anno)"] == pytest.approx(296400.0)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(433333.3333333333)
    assert mappa["Elettricita' chiller (kWh_e/anno)"] == pytest.approx(80000.0)
    assert mappa["Elettricita' pompa di calore riscaldamento (kWh_e/anno)"] == pytest.approx(78000.0)
    assert mappa["Elettricita' pompa di calore raffrescamento (kWh_e/anno)"] == pytest.approx(75000.0)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(64000.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(45250.0)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(18750.0)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(61.116666666666674)
    assert mappa["Payback (anni)"] == 5
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] == \
        pytest.approx(46.73076923076923)


def test_demo_coerenza_interna():
    bc = mh791_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["q_risc_kwh_anno"] == pytest.approx(
        bc["superficie_sala_m2"] * bc["q_risc_kwh_m2_anno"])
    assert bc["q_raff_kwh_anno"] == pytest.approx(
        bc["superficie_sala_m2"] * bc["q_raff_kwh_m2_anno"])
    assert bc["q_rec_kwh_anno"] == pytest.approx(
        bc["eta_rec"] * bc["f_vent"] * bc["q_risc_kwh_anno"])
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
        bc["e_chiller_kwh_anno"] / 1000.0 * bc["p_el_eur_mwh"]
        + bc["gas_base_kwh_anno"] / 1000.0 * bc["p_gas_eur_mwh"]
        + bc["om_base_eur_anno"])
    assert bc["c_alt_eur_anno"] == pytest.approx(
        (bc["e_pdc_risc_kwh_anno"] + bc["e_pdc_raff_kwh_anno"])
        / 1000.0 * bc["p_el_eur_mwh"]
        + bc["om_alt_eur_anno"])


def test_demo_contro_riconteggio_indipendente():
    s_sala = 3000
    qr_spec, qf_spec = 130, 80
    fv, erec = 0.40, 0.60
    eta, copc, copr, copf = 0.90, 3.0, 3.8, 3.2
    pg, pel, omb, oma, cx = 90, 250, 5000, 7000, 90000
    fg, fel, wacc, vita = 0.20, 0.35, 5.0, 15
    qrisc = s_sala * qr_spec
    qraff = s_sala * qf_spec
    qrec = erec * fv * qrisc
    qres = max(0.0, qrisc - qrec)
    gas = qrisc / eta
    ech = qraff / copc
    epr = qres / copr
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
    bc = mh791_demo_calcoli()
    assert bc["q_risc_kwh_anno"] == pytest.approx(qrisc)
    assert bc["q_raff_kwh_anno"] == pytest.approx(qraff)
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
    """Gas 60 EUR/MWh: risparmio ancora positivo
    (5.750) ma VAN -30.316,97 oltre la tolleranza
    (9.000): NON_CONVIENTE con payback mai
    raggiunto. Il verdetto guarda la VAN, non il
    solo risparmio positivo."""
    bc = _variante(p_gas_eur_mwh=60)
    assert bc["risparmio_eur_anno"] == pytest.approx(5750.0)
    assert bc["van"] == pytest.approx(-30316.96628046162)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_gas_40_non_calcolabile():
    """Gas 40 EUR/MWh: risparmio -2.916,67, verdetto
    NON_CALCOLABILE, ma helper calcolabili (flussi
    pieni, VAN negativa, TIR None, payback None)."""
    bc = _variante(p_gas_eur_mwh=40)
    assert bc["risparmio_eur_anno"] == pytest.approx(-2916.6666666666715)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_gas_zero_non_calcolabile():
    """Gas zero: costo baseline 25.000 (chiller
    20.000 + O&M 5.000, zero gas) contro 45.250
    dell'alternativa: risparmio -20.250,
    verdetto NON_CALCOLABILE."""
    bc = _variante(p_gas_eur_mwh=0)
    assert bc["valid"] is True
    assert bc["c_base_eur_anno"] == pytest.approx(25000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-20250.0)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_senza_recupero_conviente():
    """Senza recupero (eta_rec zero): riscaldamento
    residuo 390.000, E_pdc_risc 102.631,58,
    risparmio 12.592,11, VAN 40.701,75, breakeven
    60,94, CONVIENTE con payback 8 anni. Il
    recupero dalla ventilazione aiuta, ma il caso
    resta conveniente anche senza di esso, perche'
    la sala da sola basta."""
    bc = _variante(eta_rec=0)
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["q_risc_res_kwh_anno"] == pytest.approx(390000.0)
    assert bc["e_pdc_risc_kwh_anno"] == pytest.approx(102631.57894736843)
    assert bc["risparmio_eur_anno"] == pytest.approx(12592.105263157893)
    assert bc["van"] == pytest.approx(40701.746612352945)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(60.94129554655871)
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_recupero_totale_conviente():
    """Recupero totale (eta_rec 1,0): calore
    recuperato 156.000, residuo 234.000, E_pdc_risc
    61.578,95, risparmio 22.855,26, VAN 147.229,82,
    payback 4, breakeven 37,26, CONVIENTE."""
    bc = _variante(eta_rec=1.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(156000.0)
    assert bc["q_risc_res_kwh_anno"] == pytest.approx(234000.0)
    assert bc["e_pdc_risc_kwh_anno"] == pytest.approx(61578.94736842105)
    assert bc["risparmio_eur_anno"] == pytest.approx(22855.263157894733)
    assert bc["van"] == pytest.approx(147229.81595157477)
    assert bc["payback"] == 4
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(37.257085020242926)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_senza_raffrescamento_conviente():
    """Senza raffrescamento (q_raff zero): il
    chiller sparisce da entrambi i costi, risparmio
    17.500, VAN 91.644,02, payback 6, breakeven
    49,62, CONVIENTE."""
    bc = _variante(q_raff_kwh_m2_anno=0)
    assert bc["q_raff_kwh_anno"] == 0.0
    assert bc["e_chiller_kwh_anno"] == 0.0
    assert bc["e_pdc_raff_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(17500.0)
    assert bc["van"] == pytest.approx(91644.01566816033)
    assert bc["payback"] == 6
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(49.61538461538462)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_alto_marginale_e_non_conviente():
    bc = _variante(capex_eur=200000)
    assert bc["risparmio_eur_anno"] == pytest.approx(18750.0)
    assert bc["van"] == pytest.approx(-5381.411784113972)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"
    bc2 = _variante(capex_eur=220000)
    assert bc2["van"] == pytest.approx(-25381.41178411399)
    assert bc2["payback"] == 12
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex_eur=0)
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(194618.5882158861, rel=1e-6)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(191250.0)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(54782.529922215195)
    assert bc2["payback"] == 5
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_el_alto_e_cop_risc_basso():
    """Elettricita' 350 EUR/MWh: risparmio 11.450,
    VAN 28.847,08, breakeven 63,58, CONVIENTE con
    payback 8 anni. COP riscaldamento 2,5:
    E_pdc_risc 118.560, risparmio 8.610, VAN
    -631,14 entro la tolleranza del 10 %
    (9.000), breakeven 70,13, MARGINALE con
    payback 11 anni."""
    bc = _variante(p_el_eur_mwh=350)
    assert bc["risparmio_eur_anno"] == pytest.approx(11450.0)
    assert bc["van"] == pytest.approx(28847.084537167757)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(63.57692307692308)
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(cop_risc=2.5)
    assert bc2["e_pdc_risc_kwh_anno"] == pytest.approx(118560.0)
    assert bc2["risparmio_eur_anno"] == pytest.approx(8610.0)
    assert bc2["van"] == pytest.approx(-631.144291265111)
    assert bc2["breakeven_gas_eur_mwh"] == pytest.approx(70.13076923076923)
    assert bc2["payback"] == 11
    assert bc2["verdetto"] == "MARGINALE"


def test_monotonia_prezzo_gas_crescente():
    base = mh791_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas_eur_mwh=91)["risparmio_eur_anno"]
    basso = _variante(p_gas_eur_mwh=89)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(433.3333333333333)
    assert base - basso == pytest.approx(433.3333333333333)


def test_monotonia_recupero_crescente_con_tetto():
    """Il risparmio cresce con il recupero finche'
    il calore recuperato non copre tutto il
    riscaldamento; oltre, il residuo e' zero e il
    risparmio si ferma."""
    assert _variante(eta_rec=0)["risparmio_eur_anno"] < \
        mh791_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(eta_rec=1.0)["risparmio_eur_anno"] > \
        mh791_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(f_vent=1.0, eta_rec=1.0)["q_rec_kwh_anno"] == \
        pytest.approx(390000.0)
    assert _variante(f_vent=1.0, eta_rec=1.0)["q_risc_res_kwh_anno"] == 0.0


def test_demo_deterministica_due_chiamate():
    a = mh791_demo_calcoli()
    b = mh791_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh791_demo().keys()) == {
        "superficie_sala_m2",
        "q_risc_kwh_m2_anno", "q_raff_kwh_m2_anno",
        "f_vent", "eta_rec",
        "eta_caldaia", "cop_chiller", "cop_risc",
        "cop_raff",
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
    for kw in ({"superficie_sala_m2": 0},
               {"superficie_sala_m2": -10},
               {"q_risc_kwh_m2_anno": -0.1},
               {"q_raff_kwh_m2_anno": -0.1},
               {"f_vent": -0.1}, {"f_vent": 1.01},
               {"eta_rec": -0.1}, {"eta_rec": 1.01},
               {"eta_caldaia": 0}, {"eta_caldaia": 1.01},
               {"cop_chiller": 1.0}, {"cop_chiller": 0.5},
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
        assert mh791_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"superficie_sala_m2": "3000"},
               {"superficie_sala_m2": float("nan")},
               {"p_gas_eur_mwh": float("inf")},
               {"capex_eur": True},
               {"q_risc_kwh_m2_anno": "130"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh791_valida(**d)["valido"] is False


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    """Differenza chiave: risparmio <= 0 NON solleva
    negli helper (resta calcolabile con flussi, VAN,
    TIR e payback), ma il verdetto e' NON_CALCOLABILE
    e la UI salta KPI, grafico, tabella e CSV."""
    for kw in ({"p_gas_eur_mwh": 0},
               {"p_gas_eur_mwh": 46.73076923076923},
               {"p_gas_eur_mwh": 40}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] <= 0.0
        assert bc["verdetto"] == "NON_CALCOLABILE"
        assert bc["flussi"]


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh791_demo_calcoli()
    testo = mh791_csv(bc, _demo_kwargs())
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


def test_csv_valori_coerenti_con_calcola():
    bc = mh791_demo_calcoli()
    testo = mh791_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"q_risc_kwh_anno;{bc['q_risc_kwh_anno']}" in testo
    assert f"gas_base_kwh_anno;{bc['gas_base_kwh_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh791_demo_calcoli()
    testo = mh791_csv(bc, _demo_kwargs())
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
    return ["mh" + "79" + "0", "st" + "79" + "0",
            "tab" + "79" + "0", "tab" + "78" + "9"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w792_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w792_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab791:")


def test_registry_chain_tail_and_count():
    """Registry della nuova tab: il frammento UI apre la tab
    numero 791 (la coda della catena termina con la nuova tab
    e il conteggio atteso delle tab e' 791)."""
    src = _leggi("w792_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 791
    assert src.count("with tab791:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w792_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w792_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st791_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) >= 24
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w792_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 3
    # Tutte le guard (input degenere e risparmio <= 0)
    # stanno prima di KPI / grafico / tabella / CSV.
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w792_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def791[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w792_ui.py")
        usate = set(re.findall(r'_def791\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 19
        assert usate <= set(mh791_demo().keys())
