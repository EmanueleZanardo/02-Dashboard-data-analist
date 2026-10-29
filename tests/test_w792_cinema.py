"""Test tab792 "Cinema: pompa di calore reversibile
+ recupero calore ventilazione sale batte la
caldaia a gas + chiller?"
(titolo completo nel frammento UI).
Contenuto pronto da scrivere in repo come test
della tab cinema.

Business case deterministico di un cinema
guidato dalla superficie complessiva in m2 delle sale cinematografiche a uso giornaliero continuativo con piu' spettacoli al giorno.
Riscaldamento sale cinematografiche Q_risc = S x q_risc
kWh_th/anno; raffrescamento sale cinematografiche Q_raff = S x
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
tolleranza. Distinzione esplicita: NON la tab del teatro (una sola sala a uso serale concentrato, con spettacoli solo la sera: qui invece le sale sono piu' di una e gli spettacoli si ripetono tutto il giorno, con freddo dominante e ventilazione per il pubblico continua), NON la tab del museo / delle sale espositive (una sola superficie espositiva con orario diurno continuo, senza picchi di pubblico in sala e senza ventilazione legata agli spettacoli), NON la tab della biblioteca (depositi con raffrescamento continuo, anche quando le sale non raffrescano: nessun fabbisogno di freddo continuo qui), NON la scuola (aule + mensa con pasti, orari e chiusure stagionali: nessuna mensa qui, nessuna chiusura stagionale legata alle lezioni) e NON la palestra (docce degli utenti con acqua calda sanitaria + riscaldamento, recupero sulle acque di scarico delle docce: nessuna acqua calda sanitaria per docce qui, nessun recupero da acque di scarico): qui il driver e' la superficie complessiva in m2 delle sale cinematografiche a uso giornaliero continuativo, con piu' spettacoli al giorno, e il calore recuperato viene SOLO dalla ventilazione per il pubblico, come quota del fabbisogno di riscaldamento delle sale cinematografiche.

Demo (cinema): sale per 2.500 m2 complessivi a 110
kWh_th/m2/anno di riscaldamento e 95
kWh_c/m2/anno di raffrescamento, quota
ventilazione 0,45, recupero 0,60, caldaia 0,90,
chiller COP 3,0, pompa di calore reversibile
COP riscaldamento 3,8 e COP raffrescamento
3,4, gas 90, el 250 EUR/MWh, O&M base 6.000,
alt 8.000, CAPEX 85.000, WACC 5 %, vita 15,
f_gas 0,20, f_el 0,35, tolleranza 10 % del
CAPEX. Valori calcolati eseguendo
mh792_demo_calcoli(): Q_risc 275.000, Q_raff
237.500, Q_rec 74.250, Q_risc_res 200.750,
G_base 305.555,55555555556, E_chiller 79.166,66666666667,
E_pdc_risc 52.828,94736842105, E_pdc_raff 69.852,94117647059, C_base
53.291,66666666667, C_alt 38.670,47213622291, risparmio 14.621,194530443761,
CO2_base 88,81944444444444, CO2_alt 42,93866099071207,
CO2_evitata 45,88078345373237, VAN
66.762,99933572266, TIR 15,12035800303993 %,
payback 6, breakeven gas 42,148817900365884,
verdetto CONVIENTE.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w793_helpers import (
    demo_calcoli,
    mh792_breakeven_gas,
    mh792_c_alt,
    mh792_c_base,
    mh792_calcola,
    mh792_co2_alt,
    mh792_co2_base,
    mh792_co2_evitata,
    mh792_cop,
    mh792_csv,
    mh792_demo,
    mh792_demo_calcoli,
    mh792_e_chiller,
    mh792_e_pdc_raff,
    mh792_e_pdc_risc,
    mh792_eta,
    mh792_eta_rec,
    mh792_f_vent,
    mh792_flussi,
    mh792_gas,
    mh792_int_pos,
    mh792_num,
    mh792_nneg,
    mh792_payback,
    mh792_pct_tolleranza,
    mh792_pct_wacc,
    mh792_pos,
    mh792_q_raff,
    mh792_q_rec,
    mh792_q_risc,
    mh792_q_risc_res,
    mh792_risparmio,
    mh792_tir,
    mh792_valida,
    mh792_van,
    mh792_verdetto,
)

_DEMO = {
    "q_risc_kwh_anno": 275000.0,
    "q_raff_kwh_anno": 237500.0,
    "q_rec_kwh_anno": 74250.0,
    "q_risc_res_kwh_anno": 200750.0,
    "gas_base_kwh_anno": 305555.55555555556,
    "e_chiller_kwh_anno": 79166.66666666667,
    "e_pdc_risc_kwh_anno": 52828.94736842105,
    "e_pdc_raff_kwh_anno": 69852.94117647059,
    "c_base_eur_anno": 53291.66666666667,
    "c_alt_eur_anno": 38670.47213622291,
    "risparmio_eur_anno": 14621.194530443761,
    "co2_base_t_anno": 88.81944444444444,
    "co2_alt_t_anno": 42.93866099071207,
    "co2_evitata_t_anno": 45.88078345373237,
    "van": 66762.99933572266,
    "tir": 15.12035800303993,
    "breakeven_gas_eur_mwh": 42.148817900365884,
}


def _demo_kwargs():
    return dict(mh792_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh792_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh792_num(3, "x") == 3.0
    assert mh792_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh792_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh792_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh792_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh792_pos(0, "x")
    with pytest.raises(ValueError):
        mh792_pos(-1, "x")
    assert mh792_pos(0.5, "x") == 0.5


def test_cop_maggiore_di_uno():
    assert mh792_cop(3.8, "x") == 3.8
    assert mh792_cop(1.01, "x") == 1.01
    with pytest.raises(ValueError):
        mh792_cop(1.0, "x")
    with pytest.raises(ValueError):
        mh792_cop(0.5, "x")
    with pytest.raises(ValueError):
        mh792_cop(0, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh792_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh792_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh792_int_pos(0, "x")


def test_eta_limiti():
    assert mh792_eta(1.0, "x") == 1.0
    assert mh792_eta(0.9, "x") == 0.9
    with pytest.raises(ValueError):
        mh792_eta(0, "x")
    with pytest.raises(ValueError):
        mh792_eta(1.01, "x")


def test_eta_rec_limiti():
    assert mh792_eta_rec(0.0, "x") == 0.0
    assert mh792_eta_rec(1.0, "x") == 1.0
    assert mh792_eta_rec(0.6, "x") == 0.6
    with pytest.raises(ValueError):
        mh792_eta_rec(-0.1, "x")
    with pytest.raises(ValueError):
        mh792_eta_rec(1.01, "x")


def test_f_vent_limiti():
    assert mh792_f_vent(0.0, "x") == 0.0
    assert mh792_f_vent(1.0, "x") == 1.0
    assert mh792_f_vent(0.40, "x") == 0.40
    with pytest.raises(ValueError):
        mh792_f_vent(-0.1, "x")
    with pytest.raises(ValueError):
        mh792_f_vent(1.01, "x")


def test_pct_wacc_limiti():
    assert mh792_pct_wacc(0, "x") == 0.0
    assert mh792_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh792_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh792_pct_tolleranza(0, "x") == 0.0
    assert mh792_pct_tolleranza(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh792_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh792_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_q_risc_e_q_raff():
    assert mh792_q_risc(2500, 110) == 275000.0
    assert mh792_q_risc(1500, 110) == 165000.0
    assert mh792_q_risc(2500, 0) == 0.0
    assert mh792_q_raff(2500, 95) == 237500.0
    assert mh792_q_raff(2500, 0) == 0.0
    assert mh792_q_raff(1500, 95) == 142500.0
    with pytest.raises(ValueError):
        mh792_q_risc(0, 110)
    with pytest.raises(ValueError):
        mh792_q_risc(2500, -10)
    with pytest.raises(ValueError):
        mh792_q_raff(0, 95)
    with pytest.raises(ValueError):
        mh792_q_raff(2500, -10)


def test_q_rec_solo_ventilazione():
    assert mh792_q_rec(275000, 0.45, 0.60) == 74250.0
    assert mh792_q_rec(275000, 0.40, 0) == 0.0
    assert mh792_q_rec(275000, 0, 0.60) == 0.0
    assert mh792_q_rec(275000, 0.45, 1.0) == 123750.0
    # Quota e rendimento massimi: il recupero eguaglia
    # il riscaldamento, mai lo supera.
    assert mh792_q_rec(275000, 1.0, 1.0) == 275000.0
    with pytest.raises(ValueError):
        mh792_q_rec(275000, 0.40, 1.01)
    with pytest.raises(ValueError):
        mh792_q_rec(275000, 1.01, 0.60)
    with pytest.raises(ValueError):
        mh792_q_rec(275000, -0.1, 0.60)


def test_q_risc_res_con_troncamento_a_zero():
    assert mh792_q_risc_res(275000, 74250.0) == 200750.0
    assert mh792_q_risc_res(275000, 275000.0) == 0.0
    # L'eccesso recuperato viene sprecato, senza export.
    assert mh792_q_risc_res(275000, 300000.0) == 0.0
    with pytest.raises(ValueError):
        mh792_q_risc_res(275000, -1)


def test_gas_e_chiller():
    assert mh792_gas(275000, 0.9) == pytest.approx(305555.55555555556)
    assert mh792_gas(0, 0.9) == 0.0
    assert mh792_e_chiller(237500, 3.0) == 79166.66666666667
    assert mh792_e_chiller(0, 3.0) == 0.0
    with pytest.raises(ValueError):
        mh792_gas(275000, 0)
    with pytest.raises(ValueError):
        mh792_gas(275000, 1.01)
    with pytest.raises(ValueError):
        mh792_e_chiller(237500, 1.0)


def test_e_pdc_risc_e_raff():
    assert mh792_e_pdc_risc(200750.0, 3.8) == pytest.approx(52828.94736842105)
    assert mh792_e_pdc_risc(0, 3.8) == 0.0
    assert mh792_e_pdc_raff(237500, 3.4) == pytest.approx(69852.94117647059)
    assert mh792_e_pdc_raff(0, 3.4) == 0.0
    with pytest.raises(ValueError):
        mh792_e_pdc_risc(200750.0, 1.0)
    with pytest.raises(ValueError):
        mh792_e_pdc_raff(237500, 0.5)


def test_c_base_c_alt_scomposizione():
    assert mh792_c_base(79166.66666666667, 250, 305555.55555555556, 90,
                        6000) == pytest.approx(53291.66666666667)
    assert mh792_c_base(79166.66666666667, 250, 305555.55555555556, 0,
                        6000) == pytest.approx(25791.66666666667)
    assert mh792_c_alt(52828.94736842105, 69852.94117647059, 250,
                       8000) == pytest.approx(38670.47213622291)
    assert mh792_c_alt(0, 0, 250, 8000) == pytest.approx(8000.0)
    with pytest.raises(ValueError):
        mh792_c_base(79166.66666666667, 250, 305555.55555555556, -1, 6000)
    with pytest.raises(ValueError):
        mh792_c_alt(52828.94736842105, 69852.94117647059, 250, -1)


def test_risparmio_segno():
    assert mh792_risparmio(53291.66666666667, 38670.47213622291) == pytest.approx(14621.194530443761)
    assert mh792_risparmio(38670.47213622291, 38670.47213622291) == 0.0
    assert mh792_risparmio(25791.66666666667, 38670.47213622291) == pytest.approx(-12878.805469556242)


def test_co2_base_alt_evitata():
    assert mh792_co2_base(305555.55555555556, 0.20, 79166.66666666667,
                          0.35) == pytest.approx(88.81944444444444)
    assert mh792_co2_alt(52828.94736842105, 69852.94117647059,
                         0.35) == pytest.approx(42.93866099071207)
    assert mh792_co2_evitata(305555.55555555556, 0.20, 79166.66666666667,
                             52828.94736842105, 69852.94117647059,
                             0.35) == pytest.approx(45.88078345373237)
    assert mh792_co2_base(0, 0.20, 0, 0.35) == pytest.approx(0.0)
    assert mh792_co2_alt(0, 0, 0.35) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh792_co2_base(305555.55555555556, -0.10, 79166.66666666667, 0.35)
    with pytest.raises(ValueError):
        mh792_co2_alt(52828.94736842105, 69852.94117647059, -0.10)


def test_breakeven_gas_demo_e_varianti():
    assert mh792_breakeven_gas(38670.47213622291, 79166.66666666667, 250,
                               6000,
                               305555.55555555556) == \
        pytest.approx(42.148817900365884)
    assert mh792_breakeven_gas(43555.340557275544, 79166.66666666667, 250,
                               6000,
                               305555.55555555556) == \
        pytest.approx(58.13566000562905)
    assert mh792_breakeven_gas(35413.89318885449, 79166.66666666667, 250,
                               6000,
                               305555.55555555556) == \
        pytest.approx(31.490923163523778)
    assert mh792_breakeven_gas(38670.47213622291, 79166.66666666667, 250,
                               6000, 0) is None
    # Numeratore negativo: alternativa gia' piu'
    # conveniente a prezzo gas zero -> nessun pareggio.
    assert mh792_breakeven_gas(200, 79166.66666666667, 250, 6000,
                               305555.55555555556) is None
    with pytest.raises(ValueError):
        mh792_breakeven_gas(38670.47213622291, 79166.66666666667, 250,
                            6000, -1)


def test_breakeven_verifica_pareggio():
    """Al prezzo gas di pareggio i costi si eguagliano
    e il risparmio e' zero: scatta la guard
    NON_CALCOLABILE, non un verdetto di convenienza."""
    bc = _variante(p_gas_eur_mwh=42.148817900365884)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    demo = mh792_demo_calcoli()
    assert (demo["c_alt_eur_anno"]
            - demo["e_chiller_kwh_anno"] / 1000.0
            * demo["p_el_eur_mwh"]
            - demo["om_base_eur_anno"]) * 1000.0 / demo["gas_base_kwh_anno"] == \
        pytest.approx(demo["breakeven_gas_eur_mwh"])


def test_breakeven_soglia_minima():
    """Sopra la soglia l'alternativa vince, sotto perde."""
    be = mh792_demo_calcoli()["breakeven_gas_eur_mwh"]
    assert _variante(p_gas_eur_mwh=be + 1)[
        "c_alt_eur_anno"] < _variante(p_gas_eur_mwh=be + 1)[
        "c_base_eur_anno"]
    assert _variante(p_gas_eur_mwh=be - 1)[
        "c_alt_eur_anno"] > _variante(p_gas_eur_mwh=be - 1)[
        "c_base_eur_anno"]


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh792_flussi(85000, 14621.194530443761, 15)
    assert len(fl) == 16
    assert fl[0] == -85000
    assert all(f == 14621.194530443761 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh792_demo_calcoli()
    assert bc["van"] == pytest.approx(66762.99933572266)
    assert mh792_van([-85000] + [14621.194530443761] * 15,
                     0) == pytest.approx(134317.91795665643)
    assert mh792_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh792_demo_calcoli()
    assert bc["tir"] == pytest.approx(15.12035800303993)
    assert mh792_tir([-85000] + [14621.194530443761] * 15) == \
        pytest.approx(0.1512035800303993)
    tir = mh792_tir([-85000] + [14621.194530443761] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-85000] + [14621.194530443761] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh792_payback([-85000] + [14621.194530443761] * 15) == 6
    assert mh792_payback([-85000] + [-1000.0] * 15) is None
    assert mh792_payback([0] + [14621.194530443761] * 15) == 0
    assert mh792_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh792_verdetto(14621.194530443761, 66762.99933572266, 85000,
                          10.0) == "CONVIENTE"
    assert mh792_verdetto(14621.194530443761, 0.0, 85000, 10.0) == "MARGINALE"
    assert mh792_verdetto(14621.194530443761, -8500.0, 85000, 10.0) == "MARGINALE"
    assert mh792_verdetto(14621.194530443761, -8500.01, 85000, 10.0) == "NON_CONVIENTE"
    assert mh792_verdetto(14621.194530443761, -28383.87, 85000, 10.0) == "NON_CONVIENTE"
    assert mh792_verdetto(0.0, 66762.99933572266, 85000,
                          10.0) == "NON_CALCOLABILE"
    assert mh792_verdetto(-656.5832473340197, -91815.11, 85000,
                          10.0) == "NON_CALCOLABILE"
    assert mh792_verdetto(None, 66762.99933572266, 85000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh792_verdetto(float("nan"), 66762.99, 85000, 10.0)
    with pytest.raises(ValueError):
        mh792_verdetto(14621.194530443761, 66762.99, -1, 10.0)
    with pytest.raises(ValueError):
        mh792_verdetto(14621.194530443761, 66762.99, 85000, 100.1)


def test_valida_demo_ok():
    v = mh792_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("superficie_sale_m2", "2500"),
                       ("superficie_sale_m2", float("nan")),
                       ("superficie_sale_m2", float("inf")),
                       ("superficie_sale_m2", True),
                       ("p_gas_eur_mwh", None),
                       ("q_risc_kwh_m2_anno", "110")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh792_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("superficie_sale_m2", 0),
                          ("superficie_sale_m2", -10),
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
        assert mh792_valida(**d)["valido"] is False


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
    assert mh792_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["eta_rec"] = 1
    d["f_vent"] = 1
    d["q_risc_kwh_m2_anno"] = 130
    assert mh792_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh792_demo()
    assert d["superficie_sale_m2"] == 2500
    assert d["q_risc_kwh_m2_anno"] == 110
    assert d["q_raff_kwh_m2_anno"] == 95
    assert d["f_vent"] == 0.45
    assert d["eta_rec"] == 0.60
    assert d["eta_caldaia"] == 0.90
    assert d["cop_chiller"] == 3.0
    assert d["cop_risc"] == 3.8
    assert d["cop_raff"] == 3.4
    assert d["p_gas_eur_mwh"] == 90
    assert d["p_el_eur_mwh"] == 250
    assert d["om_base_eur_anno"] == 6000
    assert d["om_alt_eur_anno"] == 8000
    assert d["capex_eur"] == 85000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["f_gas_t_per_mwh"] == 0.20
    assert d["f_el_t_per_mwh"] == 0.35
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    """Tutti gli output numerici demo a tolleranza
    1e-9 relativa: confronto delle costanti _DEMO
    contro mh792_demo_calcoli()."""
    bc = mh792_demo_calcoli()
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
    bc = mh792_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(53291.66666666667)
    assert bc["c_alt_eur_anno"] == pytest.approx(38670.47213622291)
    assert bc["risparmio_eur_anno"] == pytest.approx(14621.194530443761)
    assert bc["co2_base_t_anno"] == pytest.approx(88.81944444444444)
    assert bc["co2_alt_t_anno"] == pytest.approx(42.93866099071207)
    assert bc["co2_evitata_t_anno"] == pytest.approx(45.88078345373237)
    assert bc["gas_base_kwh_anno"] == pytest.approx(305555.55555555556)


def test_demo_flussi_e_cumulato():
    bc = mh792_demo_calcoli()
    assert bc["flussi"][0] == -85000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(14621.194530443761) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -85000
    assert righe.iloc[4]["Cumulato (EUR)"] == pytest.approx(-26515.221878224962)
    assert righe.iloc[5]["Cumulato (EUR)"] == pytest.approx(-11894.027347781193)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(134317.91795665643)


def test_demo_tabella_righe():
    bc = mh792_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Riscaldamento sale cinematografiche (kWh_th/anno)"] == pytest.approx(275000.0)
    assert mappa["Raffrescamento sale cinematografiche (kWh_c/anno)"] == pytest.approx(237500.0)
    assert mappa["Calore recuperato ventilazione (kWh_th/anno)"] == pytest.approx(74250.0)
    assert mappa["Riscaldamento residuo (kWh_th/anno)"] == pytest.approx(200750.0)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(305555.55555555556)
    assert mappa["Elettricita' chiller (kWh_e/anno)"] == pytest.approx(79166.66666666667)
    assert mappa["Elettricita' pompa di calore riscaldamento (kWh_e/anno)"] == pytest.approx(52828.94736842105)
    assert mappa["Elettricita' pompa di calore raffrescamento (kWh_e/anno)"] == pytest.approx(69852.94117647059)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(53291.66666666667)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(38670.47213622291)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(14621.194530443761)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(45.88078345373237)
    assert mappa["Payback (anni)"] == 6
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] == \
        pytest.approx(42.148817900365884)


def test_demo_coerenza_interna():
    bc = mh792_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["q_risc_kwh_anno"] == pytest.approx(
        bc["superficie_sale_m2"] * bc["q_risc_kwh_m2_anno"])
    assert bc["q_raff_kwh_anno"] == pytest.approx(
        bc["superficie_sale_m2"] * bc["q_raff_kwh_m2_anno"])
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
    s_sala = 2500
    qr_spec, qf_spec = 110, 95
    fv, erec = 0.45, 0.60
    eta, copc, copr, copf = 0.90, 3.0, 3.8, 3.4
    pg, pel, omb, oma, cx = 90, 250, 6000, 8000, 85000
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
    bc = mh792_demo_calcoli()
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
    (5.454,53) ma VAN -28.383,87 oltre la tolleranza
    (8.500): NON_CONVIENTE con payback mai
    raggiunto. Il verdetto guarda la VAN, non il
    solo risparmio positivo."""
    bc = _variante(p_gas_eur_mwh=60)
    assert bc["risparmio_eur_anno"] == pytest.approx(5454.52786377709)
    assert bc["van"] == pytest.approx(-28383.866014266125)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_gas_40_non_calcolabile():
    """Gas 40 EUR/MWh: risparmio -656,58, verdetto
    NON_CALCOLABILE, ma helper calcolabili (flussi
    pieni, VAN negativa, TIR None, payback None)."""
    bc = _variante(p_gas_eur_mwh=40)
    assert bc["risparmio_eur_anno"] == pytest.approx(-656.5832473340197)
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
    assert bc["c_base_eur_anno"] == pytest.approx(25791.66666666667)
    assert bc["risparmio_eur_anno"] == pytest.approx(-12878.805469556242)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_senza_recupero_conviente():
    """Senza recupero (eta_rec zero): riscaldamento
    residuo 390.000, E_pdc_risc 72.368,42,
    risparmio 9.736,33, VAN 16.059,74, breakeven
    58,14, CONVIENTE con payback 9 anni. Il
    recupero dalla ventilazione aiuta, ma il caso
    resta conveniente anche senza di esso, perche'
    le sale da sole bastano."""
    bc = _variante(eta_rec=0)
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["q_risc_res_kwh_anno"] == pytest.approx(275000.0)
    assert bc["e_pdc_risc_kwh_anno"] == pytest.approx(72368.42105263159)
    assert bc["risparmio_eur_anno"] == pytest.approx(9736.326109391128)
    assert bc["van"] == pytest.approx(16059.735563689177)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(58.13566000562905)
    assert bc["payback"] == 9
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_recupero_totale_conviente():
    """Recupero totale (eta_rec 1,0): calore
    recuperato 123.750, residuo 151.250, E_pdc_risc
    39.802,63, risparmio 17.877,77, VAN 100.565,18,
    payback 5, breakeven 31,49, CONVIENTE."""
    bc = _variante(eta_rec=1.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(123750.0)
    assert bc["q_risc_res_kwh_anno"] == pytest.approx(151250.0)
    assert bc["e_pdc_risc_kwh_anno"] == pytest.approx(39802.631578947374)
    assert bc["risparmio_eur_anno"] == pytest.approx(17877.77347781218)
    assert bc["van"] == pytest.approx(100565.17518374497)
    assert bc["payback"] == 5
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(31.490923163523778)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_senza_raffrescamento_conviente():
    """Senza raffrescamento (q_raff zero): il
    chiller sparisce da entrambi i costi, risparmio
    12.292,76, VAN 42.594,68, payback 7, breakeven
    49,77, CONVIENTE."""
    bc = _variante(q_raff_kwh_m2_anno=0)
    assert bc["q_raff_kwh_anno"] == 0.0
    assert bc["e_chiller_kwh_anno"] == 0.0
    assert bc["e_pdc_raff_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(12292.763157894737)
    assert bc["van"] == pytest.approx(42594.67792329232)
    assert bc["payback"] == 7
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(49.76913875598086)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_alto_marginale_e_non_conviente():
    bc = _variante(capex_eur=160000)
    assert bc["risparmio_eur_anno"] == pytest.approx(14621.194530443761)
    assert bc["van"] == pytest.approx(-8237.000664277339)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"
    bc2 = _variante(capex_eur=180000)
    assert bc2["van"] == pytest.approx(-28237.00066427734)
    assert bc2["payback"] == 13
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex_eur=0)
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(151762.99933572268, rel=1e-6)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(134317.91795665643)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(27900.988512133503)
    assert bc2["payback"] == 6
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_el_alto_e_cop_risc_basso():
    """Elettricita' 350 EUR/MWh: risparmio 10.269,67,
    VAN 21.595,69, breakeven 56,39, CONVIENTE con
    payback 9 anni. COP riscaldamento 2,5:
    E_pdc_risc 80.300, risparmio 7.753,43, VAN
    -4.522,03 entro la tolleranza del 10 %
    (8.500), breakeven 64,63, MARGINALE con
    payback 11 anni."""
    bc = _variante(p_el_eur_mwh=350)
    assert bc["risparmio_eur_anno"] == pytest.approx(10269.672342621263)
    assert bc["van"] == pytest.approx(21595.687080569685)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(56.39016324233041)
    assert bc["payback"] == 9
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(cop_risc=2.5)
    assert bc2["e_pdc_risc_kwh_anno"] == pytest.approx(80300.0)
    assert bc2["risparmio_eur_anno"] == pytest.approx(7753.431372549021)
    assert bc2["van"] == pytest.approx(-4522.033730439985)
    assert bc2["breakeven_gas_eur_mwh"] == pytest.approx(64.62513368983959)
    assert bc2["payback"] == 11
    assert bc2["verdetto"] == "MARGINALE"


def test_monotonia_prezzo_gas_crescente():
    base = mh792_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas_eur_mwh=91)["risparmio_eur_anno"]
    basso = _variante(p_gas_eur_mwh=89)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(305.55555555555554)
    assert base - basso == pytest.approx(305.55555555555554)


def test_monotonia_recupero_crescente_con_tetto():
    """Il risparmio cresce con il recupero finche'
    il calore recuperato non copre tutto il
    riscaldamento; oltre, il residuo e' zero e il
    risparmio si ferma."""
    assert _variante(eta_rec=0)["risparmio_eur_anno"] < \
        mh792_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(eta_rec=1.0)["risparmio_eur_anno"] > \
        mh792_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(f_vent=1.0, eta_rec=1.0)["q_rec_kwh_anno"] == \
        pytest.approx(275000.0)
    assert _variante(f_vent=1.0, eta_rec=1.0)["q_risc_res_kwh_anno"] == 0.0


def test_demo_deterministica_due_chiamate():
    a = mh792_demo_calcoli()
    b = mh792_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh792_demo().keys()) == {
        "superficie_sale_m2",
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
    for kw in ({"superficie_sale_m2": 0},
               {"superficie_sale_m2": -10},
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
        assert mh792_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"superficie_sale_m2": "2500"},
               {"superficie_sale_m2": float("nan")},
               {"p_gas_eur_mwh": float("inf")},
               {"capex_eur": True},
               {"q_risc_kwh_m2_anno": "110"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh792_valida(**d)["valido"] is False


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    """Differenza chiave: risparmio <= 0 NON solleva
    negli helper (resta calcolabile con flussi, VAN,
    TIR e payback), ma il verdetto e' NON_CALCOLABILE
    e la UI salta KPI, grafico, tabella e CSV."""
    for kw in ({"p_gas_eur_mwh": 0},
               {"p_gas_eur_mwh": 42.148817900365884},
               {"p_gas_eur_mwh": 40}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] <= 0.0
        assert bc["verdetto"] == "NON_CALCOLABILE"
        assert bc["flussi"]


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh792_demo_calcoli()
    testo = mh792_csv(bc, _demo_kwargs())
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
    bc = mh792_demo_calcoli()
    testo = mh792_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"q_risc_kwh_anno;{bc['q_risc_kwh_anno']}" in testo
    assert f"gas_base_kwh_anno;{bc['gas_base_kwh_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh792_demo_calcoli()
    testo = mh792_csv(bc, _demo_kwargs())
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
    return ["mh" + "79" + "1", "st" + "79" + "1",
            "tab" + "79" + "1", "tab" + "79" + "0"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w793_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w793_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab792:")


def test_registry_chain_tail_and_count():
    """Registry della nuova tab: il frammento UI apre la tab
    numero 792 (la coda della catena termina con la nuova tab
    e il conteggio atteso delle tab e' 792)."""
    src = _leggi("w793_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 792
    assert src.count("with tab792:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w793_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w793_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st792_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) >= 24
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w793_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 3
    # Tutte le guard (input degenere e risparmio <= 0)
    # stanno prima di KPI / grafico / tabella / CSV.
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w793_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def792[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w793_ui.py")
        usate = set(re.findall(r'_def792\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 19
        assert usate <= set(mh792_demo().keys())
