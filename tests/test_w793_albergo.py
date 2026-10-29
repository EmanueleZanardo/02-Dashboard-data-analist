"""Test tab793 "Albergo: pompa di calore reversibile
+ recupero calore docce su ACS batte la
caldaia a gas + chiller?"
(titolo completo nel frammento UI).
Contenuto pronto da scrivere in repo come test
della tab albergo.

Business case deterministico di un albergo
guidato dalla superficie complessiva in m2 (camere + spazi comuni) per riscaldamento e raffrescamento e dal numero di camere per l'acqua calda sanitaria, con occupazione continuativa annuale.
Riscaldamento albergo Q_risc = S x q_risc
kWh_th/anno; raffrescamento albergo Q_raff = S x
q_raff kWh_c/anno; ACS camere Q_acs = N x
q_acs_camera kWh_th/anno; calore recuperato
dalle acque reflue delle docce degli ospiti
Q_rec = eta_rec x f_docce x Q_acs kWh_th/anno,
SOLO dalle docce (per costruzione Q_rec <= Q_acs,
perche' eta_rec x f_docce <= 1); ACS residua
Q_acs_res = max(0, Q_acs - Q_rec)
kWh_th/anno (l'eccesso viene sprecato, senza
export); gas baseline G_base = (Q_risc + Q_acs) /
eta_caldaia kWh/anno; elettricita' chiller
E_chiller = Q_raff / COP_chiller kWh_e/anno;
elettricita' pompa di calore in riscaldamento
E_pdc_risc = Q_risc / COP_risc kWh_e/anno;
per ACS E_pdc_acs = Q_acs_res / COP_acs
kWh_e/anno; in raffrescamento E_pdc_raff =
Q_raff / COP_raff kWh_e/anno; C_base =
E_chiller / 1000 x p_el + G_base / 1000 x p_gas
+ O&M_base EUR/anno; C_alt = (E_pdc_risc +
E_pdc_acs + E_pdc_raff) / 1000 x p_el + O&M_alt
EUR/anno (prezzi EUR/MWh, energie kWh: / 1000
esatto); risparmio = C_base - C_alt;
CO2_base = G_base / 1000 x f_gas + E_chiller /
1000 x f_el t/anno; CO2_alt = (E_pdc_risc +
E_pdc_acs + E_pdc_raff) / 1000 x f_el t/anno;
CO2_evitata = CO2_base - CO2_alt;
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
tolleranza. Distinzione esplicita: NON la tab della palestra (docce degli utenti senza pernottamento ne' ACS camere: qui invece le docce sono quelle degli ospiti pernottanti e l'ACS delle camere e' il fabbisogno dominante del recupero, con occupazione continuativa annuale), NON la tab del cinema / del teatro / del museo / della biblioteca (nessuna ACS dominante e nessun pernottamento: qui invece le camere con docce ospiti generano l'ACS e il recupero), NON la scuola (aule + mensa con pasti, orari e chiusure stagionali: nessuna mensa qui, nessuna chiusura stagionale legata alle lezioni, qui l'occupazione e' continuativa annuale) e NON la piscina (vasca riscaldata: nessuna vasca qui): qui il driver e' la superficie in m2 (camere + spazi comuni) per riscaldamento e raffrescamento, il numero di camere per l'ACS, e il calore recuperato viene SOLO dalle acque reflue delle docce degli ospiti, come quota dell'ACS delle camere.

Demo (albergo): 4.000 m2 complessivi a 100
kWh_th/m2/anno di riscaldamento e 90
kWh_c/m2/anno di raffrescamento, 60 camere a
2.500 kWh_th/camera/anno di ACS, quota
docce 0,70, recupero 0,50, caldaia 0,90,
chiller COP 3,0, pompa di calore reversibile
COP riscaldamento 3,8, COP ACS 3,0 e COP
raffrescamento 3,4, gas 90, el 250 EUR/MWh,
O&M base 8.000, alt 12.000, CAPEX 150.000,
WACC 5 %, vita 15, f_gas 0,20, f_el 0,35,
tolleranza 10 % del CAPEX. Valori calcolati
eseguendo mh793_demo_calcoli(): Q_risc 400.000,
Q_raff 360.000, Q_acs 150.000, Q_rec 52.500,
Q_acs_res 97.500, G_base 611.111,1111111111,
E_chiller 120.000, E_pdc_risc 105.263,15789473684,
E_pdc_acs 32.500, E_pdc_raff 105.882,35294117648,
C_base 93.000, C_alt 72.911,37770897834,
risparmio 20.088,62229102166, CO2_base
164,22222222222223, CO2_alt 85,27592879256966,
CO2_evitata 78,94629342965257, VAN
58.513,02983897676, TIR 10,325274586288796 %,
payback 8, breakeven gas 57,127708978328194,
verdetto CONVIENTE.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w794_helpers import (
    demo_calcoli,
    mh793_breakeven_gas,
    mh793_c_alt,
    mh793_c_base,
    mh793_calcola,
    mh793_co2_alt,
    mh793_co2_base,
    mh793_co2_evitata,
    mh793_cop,
    mh793_csv,
    mh793_demo,
    mh793_demo_calcoli,
    mh793_e_chiller,
    mh793_e_pdc_acs,
    mh793_e_pdc_raff,
    mh793_e_pdc_risc,
    mh793_eta,
    mh793_eta_rec,
    mh793_f_docce,
    mh793_flussi,
    mh793_gas,
    mh793_int_pos,
    mh793_num,
    mh793_nneg,
    mh793_payback,
    mh793_pct_tolleranza,
    mh793_pct_wacc,
    mh793_pos,
    mh793_q_acs,
    mh793_q_acs_res,
    mh793_q_raff,
    mh793_q_rec,
    mh793_q_risc,
    mh793_risparmio,
    mh793_tir,
    mh793_valida,
    mh793_van,
    mh793_verdetto,
)

_DEMO = {
    "q_risc_kwh_anno": 400000.0,
    "q_raff_kwh_anno": 360000.0,
    "q_acs_kwh_anno": 150000.0,
    "q_rec_kwh_anno": 52500.0,
    "q_acs_res_kwh_anno": 97500.0,
    "gas_base_kwh_anno": 611111.1111111111,
    "e_chiller_kwh_anno": 120000.0,
    "e_pdc_risc_kwh_anno": 105263.15789473684,
    "e_pdc_acs_kwh_anno": 32500.0,
    "e_pdc_raff_kwh_anno": 105882.35294117648,
    "c_base_eur_anno": 93000.0,
    "c_alt_eur_anno": 72911.37770897834,
    "risparmio_eur_anno": 20088.62229102166,
    "co2_base_t_anno": 164.22222222222223,
    "co2_alt_t_anno": 85.27592879256966,
    "co2_evitata_t_anno": 78.94629342965257,
    "van": 58513.02983897676,
    "tir": 10.325274586288796,
    "breakeven_gas_eur_mwh": 57.127708978328194,
}


def _demo_kwargs():
    return dict(mh793_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh793_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh793_num(3, "x") == 3.0
    assert mh793_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh793_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh793_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh793_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh793_pos(0, "x")
    with pytest.raises(ValueError):
        mh793_pos(-1, "x")
    assert mh793_pos(0.5, "x") == 0.5


def test_cop_maggiore_di_uno():
    assert mh793_cop(3.8, "x") == 3.8
    assert mh793_cop(1.01, "x") == 1.01
    with pytest.raises(ValueError):
        mh793_cop(1.0, "x")
    with pytest.raises(ValueError):
        mh793_cop(0.5, "x")
    with pytest.raises(ValueError):
        mh793_cop(0, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh793_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh793_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh793_int_pos(0, "x")


def test_eta_limiti():
    assert mh793_eta(1.0, "x") == 1.0
    assert mh793_eta(0.9, "x") == 0.9
    with pytest.raises(ValueError):
        mh793_eta(0, "x")
    with pytest.raises(ValueError):
        mh793_eta(1.01, "x")


def test_eta_rec_limiti():
    assert mh793_eta_rec(0.0, "x") == 0.0
    assert mh793_eta_rec(1.0, "x") == 1.0
    assert mh793_eta_rec(0.5, "x") == 0.5
    with pytest.raises(ValueError):
        mh793_eta_rec(-0.1, "x")
    with pytest.raises(ValueError):
        mh793_eta_rec(1.01, "x")


def test_f_docce_limiti():
    assert mh793_f_docce(0.0, "x") == 0.0
    assert mh793_f_docce(1.0, "x") == 1.0
    assert mh793_f_docce(0.70, "x") == 0.70
    with pytest.raises(ValueError):
        mh793_f_docce(-0.1, "x")
    with pytest.raises(ValueError):
        mh793_f_docce(1.01, "x")


def test_pct_wacc_limiti():
    assert mh793_pct_wacc(0, "x") == 0.0
    assert mh793_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh793_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh793_pct_tolleranza(0, "x") == 0.0
    assert mh793_pct_tolleranza(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh793_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh793_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_q_risc_q_raff_q_acs():
    assert mh793_q_risc(4000, 100) == 400000.0
    assert mh793_q_risc(2500, 100) == 250000.0
    assert mh793_q_risc(4000, 0) == 0.0
    assert mh793_q_raff(4000, 90) == 360000.0
    assert mh793_q_raff(4000, 0) == 0.0
    assert mh793_q_raff(2500, 90) == 225000.0
    assert mh793_q_acs(60, 2500) == 150000.0
    assert mh793_q_acs(60, 0) == 0.0
    assert mh793_q_acs(40, 2500) == 100000.0
    with pytest.raises(ValueError):
        mh793_q_risc(0, 100)
    with pytest.raises(ValueError):
        mh793_q_risc(4000, -10)
    with pytest.raises(ValueError):
        mh793_q_raff(0, 90)
    with pytest.raises(ValueError):
        mh793_q_raff(4000, -10)
    with pytest.raises(ValueError):
        mh793_q_acs(0, 2500)
    with pytest.raises(ValueError):
        mh793_q_acs(60.5, 2500)
    with pytest.raises(ValueError):
        mh793_q_acs(60, -10)


def test_q_rec_solo_docce():
    assert mh793_q_rec(150000, 0.70, 0.50) == 52500.0
    assert mh793_q_rec(150000, 0.70, 0) == 0.0
    assert mh793_q_rec(150000, 0, 0.50) == 0.0
    assert mh793_q_rec(150000, 0.70, 1.0) == 105000.0
    # Quota e rendimento massimi: il recupero eguaglia
    # l'ACS, mai la supera.
    assert mh793_q_rec(150000, 1.0, 1.0) == 150000.0
    with pytest.raises(ValueError):
        mh793_q_rec(150000, 0.70, 1.01)
    with pytest.raises(ValueError):
        mh793_q_rec(150000, 1.01, 0.50)
    with pytest.raises(ValueError):
        mh793_q_rec(150000, -0.1, 0.50)


def test_q_acs_res_con_troncamento_a_zero():
    assert mh793_q_acs_res(150000, 52500.0) == 97500.0
    assert mh793_q_acs_res(150000, 150000.0) == 0.0
    # L'eccesso recuperato viene sprecato, senza export.
    assert mh793_q_acs_res(150000, 200000.0) == 0.0
    with pytest.raises(ValueError):
        mh793_q_acs_res(150000, -1)


def test_gas_e_chiller():
    assert mh793_gas(400000, 150000, 0.9) == pytest.approx(611111.1111111111)
    assert mh793_gas(0, 0, 0.9) == 0.0
    assert mh793_e_chiller(360000, 3.0) == 120000.0
    assert mh793_e_chiller(0, 3.0) == 0.0
    with pytest.raises(ValueError):
        mh793_gas(400000, 150000, 0)
    with pytest.raises(ValueError):
        mh793_gas(400000, 150000, 1.01)
    with pytest.raises(ValueError):
        mh793_e_chiller(360000, 1.0)


def test_e_pdc_risc_acs_raff():
    assert mh793_e_pdc_risc(400000.0, 3.8) == pytest.approx(105263.15789473684)
    assert mh793_e_pdc_risc(0, 3.8) == 0.0
    assert mh793_e_pdc_acs(97500.0, 3.0) == 32500.0
    assert mh793_e_pdc_acs(0, 3.0) == 0.0
    assert mh793_e_pdc_raff(360000, 3.4) == pytest.approx(105882.35294117648)
    assert mh793_e_pdc_raff(0, 3.4) == 0.0
    with pytest.raises(ValueError):
        mh793_e_pdc_risc(400000.0, 1.0)
    with pytest.raises(ValueError):
        mh793_e_pdc_acs(97500.0, 0.5)
    with pytest.raises(ValueError):
        mh793_e_pdc_raff(360000, 1.0)


def test_c_base_c_alt_scomposizione():
    assert mh793_c_base(120000.0, 250, 611111.1111111111, 90,
                        8000) == pytest.approx(93000.0)
    assert mh793_c_base(120000.0, 250, 611111.1111111111, 0,
                        8000) == pytest.approx(38000.0)
    assert mh793_c_alt(105263.15789473684, 32500.0, 105882.35294117648,
                       250, 12000) == pytest.approx(72911.37770897834)
    assert mh793_c_alt(0, 0, 0, 250, 12000) == pytest.approx(12000.0)
    with pytest.raises(ValueError):
        mh793_c_base(120000.0, 250, 611111.1111111111, -1, 8000)
    with pytest.raises(ValueError):
        mh793_c_alt(105263.15789473684, 32500.0, 105882.35294117648,
                    250, -1)


def test_risparmio_segno():
    assert mh793_risparmio(93000.0, 72911.37770897834) == pytest.approx(20088.62229102166)
    assert mh793_risparmio(72911.37770897834, 72911.37770897834) == 0.0
    assert mh793_risparmio(38000.0, 72911.37770897834) == pytest.approx(-34911.37770897834)


def test_co2_base_alt_evitata():
    assert mh793_co2_base(611111.1111111111, 0.20, 120000.0,
                          0.35) == pytest.approx(164.22222222222223)
    assert mh793_co2_alt(105263.15789473684, 32500.0, 105882.35294117648,
                         0.35) == pytest.approx(85.27592879256966)
    assert mh793_co2_evitata(611111.1111111111, 0.20, 120000.0,
                             105263.15789473684, 32500.0,
                             105882.35294117648,
                             0.35) == pytest.approx(78.94629342965257)
    assert mh793_co2_base(0, 0.20, 0, 0.35) == pytest.approx(0.0)
    assert mh793_co2_alt(0, 0, 0, 0.35) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh793_co2_base(611111.1111111111, -0.10, 120000.0, 0.35)
    with pytest.raises(ValueError):
        mh793_co2_alt(105263.15789473684, 32500.0, 105882.35294117648,
                      -0.10)


def test_breakeven_gas_demo_e_varianti():
    assert mh793_breakeven_gas(72911.37770897834, 120000.0, 250,
                               8000,
                               611111.1111111111) == \
        pytest.approx(57.127708978328194)
    assert mh793_breakeven_gas(77286.37770897834, 120000.0, 250,
                               8000,
                               611111.1111111111) == \
        pytest.approx(64.28679988741911)
    assert mh793_breakeven_gas(68536.37770897833, 120000.0, 250,
                               8000,
                               611111.1111111111) == \
        pytest.approx(49.96861806923726)
    assert mh793_breakeven_gas(72911.37770897834, 120000.0, 250,
                               8000, 0) is None
    # Numeratore negativo: alternativa gia' piu'
    # conveniente a prezzo gas zero -> nessun pareggio.
    assert mh793_breakeven_gas(200, 120000.0, 250, 8000,
                               611111.1111111111) is None
    with pytest.raises(ValueError):
        mh793_breakeven_gas(72911.37770897834, 120000.0, 250,
                            8000, -1)


def test_breakeven_verifica_pareggio():
    """Al prezzo gas di pareggio i costi si eguagliano
    e il risparmio e' zero: scatta la guard
    NON_CALCOLABILE, non un verdetto di convenienza."""
    bc = _variante(p_gas_eur_mwh=57.127708978328194)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    demo = mh793_demo_calcoli()
    assert (demo["c_alt_eur_anno"]
            - demo["e_chiller_kwh_anno"] / 1000.0
            * demo["p_el_eur_mwh"]
            - demo["om_base_eur_anno"]) * 1000.0 / demo["gas_base_kwh_anno"] == \
        pytest.approx(demo["breakeven_gas_eur_mwh"])


def test_breakeven_soglia_minima():
    """Sopra la soglia l'alternativa vince, sotto perde."""
    be = mh793_demo_calcoli()["breakeven_gas_eur_mwh"]
    assert _variante(p_gas_eur_mwh=be + 1)[
        "c_alt_eur_anno"] < _variante(p_gas_eur_mwh=be + 1)[
        "c_base_eur_anno"]
    assert _variante(p_gas_eur_mwh=be - 1)[
        "c_alt_eur_anno"] > _variante(p_gas_eur_mwh=be - 1)[
        "c_base_eur_anno"]


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh793_flussi(150000, 20088.62229102166, 15)
    assert len(fl) == 16
    assert fl[0] == -150000
    assert all(f == 20088.62229102166 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh793_demo_calcoli()
    assert bc["van"] == pytest.approx(58513.02983897676)
    assert mh793_van([-150000] + [20088.62229102166] * 15,
                     0) == pytest.approx(151329.3343653249)
    assert mh793_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh793_demo_calcoli()
    assert bc["tir"] == pytest.approx(10.325274586288796)
    assert mh793_tir([-150000] + [20088.62229102166] * 15) == \
        pytest.approx(0.10325274586288796)
    tir = mh793_tir([-150000] + [20088.62229102166] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-150000] + [20088.62229102166] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh793_payback([-150000] + [20088.62229102166] * 15) == 8
    assert mh793_payback([-150000] + [-1000.0] * 15) is None
    assert mh793_payback([0] + [20088.62229102166] * 15) == 0
    assert mh793_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh793_verdetto(20088.62229102166, 58513.02983897676, 150000,
                          10.0) == "CONVIENTE"
    assert mh793_verdetto(20088.62229102166, 0.0, 150000, 10.0) == "MARGINALE"
    assert mh793_verdetto(20088.62229102166, -15000.0, 150000, 10.0) == "MARGINALE"
    assert mh793_verdetto(20088.62229102166, -15000.01, 150000, 10.0) == "NON_CONVIENTE"
    assert mh793_verdetto(20088.62229102166, -131780.70, 150000, 10.0) == "NON_CONVIENTE"
    assert mh793_verdetto(0.0, 58513.02983897676, 150000,
                          10.0) == "NON_CALCOLABILE"
    assert mh793_verdetto(-10466.933264533895, -258643.19, 150000,
                          10.0) == "NON_CALCOLABILE"
    assert mh793_verdetto(None, 58513.02983897676, 150000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh793_verdetto(float("nan"), 58513.03, 150000, 10.0)
    with pytest.raises(ValueError):
        mh793_verdetto(20088.62229102166, 58513.03, -1, 10.0)
    with pytest.raises(ValueError):
        mh793_verdetto(20088.62229102166, 58513.03, 150000, 100.1)


def test_valida_demo_ok():
    v = mh793_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("superficie_m2", "4000"),
                       ("superficie_m2", float("nan")),
                       ("superficie_m2", float("inf")),
                       ("superficie_m2", True),
                       ("p_gas_eur_mwh", None),
                       ("q_risc_kwh_m2_anno", "100")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh793_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("superficie_m2", 0),
                          ("superficie_m2", -10),
                          ("q_risc_kwh_m2_anno", -0.1),
                          ("q_raff_kwh_m2_anno", -0.1),
                          ("n_camere", 0), ("n_camere", 60.5),
                          ("q_acs_camera_kwh_anno", -0.1),
                          ("f_docce", -0.1), ("f_docce", 1.01),
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
        assert mh793_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"q_risc_kwh_m2_anno": 0,
              "q_raff_kwh_m2_anno": 0,
              "q_acs_camera_kwh_anno": 0,
              "f_docce": 0,
              "eta_rec": 0,
              "p_gas_eur_mwh": 0,
              "p_el_eur_mwh": 0,
              "om_base_eur_anno": 0, "om_alt_eur_anno": 0,
              "capex_eur": 0, "wacc_pct": 0,
              "f_gas_t_per_mwh": 0, "f_el_t_per_mwh": 0,
              "tolleranza_pct": 0})
    assert mh793_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["eta_rec"] = 1
    d["f_docce"] = 1
    d["q_risc_kwh_m2_anno"] = 130
    assert mh793_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh793_demo()
    assert d["superficie_m2"] == 4000
    assert d["q_risc_kwh_m2_anno"] == 100
    assert d["q_raff_kwh_m2_anno"] == 90
    assert d["n_camere"] == 60
    assert d["q_acs_camera_kwh_anno"] == 2500
    assert d["f_docce"] == 0.70
    assert d["eta_rec"] == 0.50
    assert d["eta_caldaia"] == 0.90
    assert d["cop_chiller"] == 3.0
    assert d["cop_risc"] == 3.8
    assert d["cop_acs"] == 3.0
    assert d["cop_raff"] == 3.4
    assert d["p_gas_eur_mwh"] == 90
    assert d["p_el_eur_mwh"] == 250
    assert d["om_base_eur_anno"] == 8000
    assert d["om_alt_eur_anno"] == 12000
    assert d["capex_eur"] == 150000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["f_gas_t_per_mwh"] == 0.20
    assert d["f_el_t_per_mwh"] == 0.35
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    """Tutti gli output numerici demo a tolleranza
    1e-9 relativa: confronto delle costanti _DEMO
    contro mh793_demo_calcoli()."""
    bc = mh793_demo_calcoli()
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
    bc = mh793_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(93000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(72911.37770897834)
    assert bc["risparmio_eur_anno"] == pytest.approx(20088.62229102166)
    assert bc["co2_base_t_anno"] == pytest.approx(164.22222222222223)
    assert bc["co2_alt_t_anno"] == pytest.approx(85.27592879256966)
    assert bc["co2_evitata_t_anno"] == pytest.approx(78.94629342965257)
    assert bc["gas_base_kwh_anno"] == pytest.approx(611111.1111111111)


def test_demo_flussi_e_cumulato():
    bc = mh793_demo_calcoli()
    assert bc["flussi"][0] == -150000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(20088.62229102166) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -150000
    assert righe.iloc[4]["Cumulato (EUR)"] == pytest.approx(-69645.51083591336)
    assert righe.iloc[7]["Cumulato (EUR)"] == pytest.approx(-9379.64396284838)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(151329.3343653249)


def test_demo_tabella_righe():
    bc = mh793_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Riscaldamento albergo (kWh_th/anno)"] == pytest.approx(400000.0)
    assert mappa["Raffrescamento albergo (kWh_c/anno)"] == pytest.approx(360000.0)
    assert mappa["ACS camere (kWh_th/anno)"] == pytest.approx(150000.0)
    assert mappa["Calore recuperato docce (kWh_th/anno)"] == pytest.approx(52500.0)
    assert mappa["ACS residua (kWh_th/anno)"] == pytest.approx(97500.0)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(611111.1111111111)
    assert mappa["Elettricita' chiller (kWh_e/anno)"] == pytest.approx(120000.0)
    assert mappa["Elettricita' pompa di calore riscaldamento (kWh_e/anno)"] == pytest.approx(105263.15789473684)
    assert mappa["Elettricita' pompa di calore ACS (kWh_e/anno)"] == pytest.approx(32500.0)
    assert mappa["Elettricita' pompa di calore raffrescamento (kWh_e/anno)"] == pytest.approx(105882.35294117648)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(93000.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(72911.37770897834)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(20088.62229102166)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(78.94629342965257)
    assert mappa["Payback (anni)"] == 8
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] == \
        pytest.approx(57.127708978328194)


def test_demo_coerenza_interna():
    bc = mh793_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["q_risc_kwh_anno"] == pytest.approx(
        bc["superficie_m2"] * bc["q_risc_kwh_m2_anno"])
    assert bc["q_raff_kwh_anno"] == pytest.approx(
        bc["superficie_m2"] * bc["q_raff_kwh_m2_anno"])
    assert bc["q_acs_kwh_anno"] == pytest.approx(
        bc["n_camere"] * bc["q_acs_camera_kwh_anno"])
    assert bc["q_rec_kwh_anno"] == pytest.approx(
        bc["eta_rec"] * bc["f_docce"] * bc["q_acs_kwh_anno"])
    assert bc["q_acs_res_kwh_anno"] == pytest.approx(
        max(0.0, bc["q_acs_kwh_anno"] - bc["q_rec_kwh_anno"]))
    assert bc["gas_base_kwh_anno"] == pytest.approx(
        (bc["q_risc_kwh_anno"] + bc["q_acs_kwh_anno"])
        / bc["eta_caldaia"])
    assert bc["e_chiller_kwh_anno"] == pytest.approx(
        bc["q_raff_kwh_anno"] / bc["cop_chiller"])
    assert bc["e_pdc_risc_kwh_anno"] == pytest.approx(
        bc["q_risc_kwh_anno"] / bc["cop_risc"])
    assert bc["e_pdc_acs_kwh_anno"] == pytest.approx(
        bc["q_acs_res_kwh_anno"] / bc["cop_acs"])
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
    s_alb = 4000
    qr_spec, qf_spec = 100, 90
    ncam, qa_spec = 60, 2500
    fd, erec = 0.70, 0.50
    eta, copc, copr, copa, copf = 0.90, 3.0, 3.8, 3.0, 3.4
    pg, pel, omb, oma, cx = 90, 250, 8000, 12000, 150000
    fg, fel, wacc, vita = 0.20, 0.35, 5.0, 15
    qrisc = s_alb * qr_spec
    qraff = s_alb * qf_spec
    qacs = ncam * qa_spec
    qrec = erec * fd * qacs
    qres = max(0.0, qacs - qrec)
    gas = (qrisc + qacs) / eta
    ech = qraff / copc
    epr = qrisc / copr
    epa = qres / copa
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
    bc = mh793_demo_calcoli()
    assert bc["q_risc_kwh_anno"] == pytest.approx(qrisc)
    assert bc["q_raff_kwh_anno"] == pytest.approx(qraff)
    assert bc["q_acs_kwh_anno"] == pytest.approx(qacs)
    assert bc["q_rec_kwh_anno"] == pytest.approx(qrec)
    assert bc["q_acs_res_kwh_anno"] == pytest.approx(qres)
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
    """Gas 60 EUR/MWh: risparmio ancora positivo
    (1.755,29) ma VAN -131.780,70 oltre la tolleranza
    (15.000): NON_CONVIENTE con payback mai
    raggiunto. Il verdetto guarda la VAN, non il
    solo risparmio positivo."""
    bc = _variante(p_gas_eur_mwh=60)
    assert bc["risparmio_eur_anno"] == pytest.approx(1755.2889576883172)
    assert bc["van"] == pytest.approx(-131780.70086100083)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_gas_40_non_calcolabile():
    """Gas 40 EUR/MWh: risparmio -10.466,93, verdetto
    NON_CALCOLABILE, ma helper calcolabili (flussi
    pieni, VAN negativa, TIR None, payback None)."""
    bc = _variante(p_gas_eur_mwh=40)
    assert bc["risparmio_eur_anno"] == pytest.approx(-10466.933264533895)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_gas_zero_non_calcolabile():
    """Gas zero: costo baseline 38.000 (chiller
    30.000 + O&M 8.000, zero gas) contro 72.911,38
    dell'alternativa: risparmio -34.911,38,
    verdetto NON_CALCOLABILE."""
    bc = _variante(p_gas_eur_mwh=0)
    assert bc["valid"] is True
    assert bc["c_base_eur_anno"] == pytest.approx(38000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-34911.37770897834)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_senza_recupero_conviente():
    """Senza recupero (eta_rec zero): ACS residua
    150.000, E_pdc_acs 50.000, risparmio 15.713,62,
    VAN 13.102,03, breakeven 64,29, CONVIENTE con
    payback 10 anni. Il recupero dalle docce
    aiuta, ma il caso resta conveniente anche
    senza di esso, perche' superfici e camere da
    sole bastano."""
    bc = _variante(eta_rec=0)
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["q_acs_res_kwh_anno"] == pytest.approx(150000.0)
    assert bc["e_pdc_acs_kwh_anno"] == pytest.approx(50000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(15713.62229102166)
    assert bc["van"] == pytest.approx(13102.025921936665)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(64.28679988741911)
    assert bc["payback"] == 10
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_recupero_totale_conviente():
    """Recupero totale (eta_rec 1,0): calore
    recuperato 105.000, ACS residua 45.000,
    E_pdc_acs 15.000, risparmio 24.463,62, VAN
    103.924,03, payback 7, breakeven 49,97,
    CONVIENTE."""
    bc = _variante(eta_rec=1.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(105000.0)
    assert bc["q_acs_res_kwh_anno"] == pytest.approx(45000.0)
    assert bc["e_pdc_acs_kwh_anno"] == pytest.approx(15000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(24463.622291021675)
    assert bc["van"] == pytest.approx(103924.033756017)
    assert bc["payback"] == 7
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(49.96861806923726)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_senza_raffrescamento_conviente():
    """Senza raffrescamento (q_raff zero): il
    chiller sparisce da entrambi i costi, risparmio
    16.559,21, VAN 21.878,94, payback 10, breakeven
    62,90, CONVIENTE."""
    bc = _variante(q_raff_kwh_m2_anno=0)
    assert bc["q_raff_kwh_anno"] == 0.0
    assert bc["e_chiller_kwh_anno"] == 0.0
    assert bc["e_pdc_raff_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(16559.210526315786)
    assert bc["van"] == pytest.approx(21878.942645398274)
    assert bc["payback"] == 10
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(62.903110047846894)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_alto_marginale_e_non_conviente():
    bc = _variante(capex_eur=230000)
    assert bc["risparmio_eur_anno"] == pytest.approx(20088.62229102166)
    assert bc["van"] == pytest.approx(-21486.970161023273)
    assert bc["payback"] == 12
    assert bc["verdetto"] == "MARGINALE"
    bc2 = _variante(capex_eur=260000)
    assert bc2["van"] == pytest.approx(-51486.970161023266)
    assert bc2["payback"] == 13
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex_eur=0)
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(208513.0298389768, rel=1e-6)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(151329.3343653249)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(5119.01642378255)
    assert bc2["payback"] == 8
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_el_alto_e_cop_risc_basso():
    """Elettricita' 350 EUR/MWh: risparmio 7.724,07,
    VAN -69.826,78, breakeven 77,36, NON_CONVIENTE
    con payback mai raggiunto. COP riscaldamento
    2,5: E_pdc_risc 160.000, risparmio 6.404,41,
    VAN -83.524,40, breakeven 79,52, NON_CONVIENTE
    con payback mai raggiunto."""
    bc = _variante(p_el_eur_mwh=350)
    assert bc["risparmio_eur_anno"] == pytest.approx(7724.07120743033)
    assert bc["van"] == pytest.approx(-69826.78220431654)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(77.36061075147764)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"
    bc2 = _variante(cop_risc=2.5)
    assert bc2["e_pdc_risc_kwh_anno"] == pytest.approx(160000.0)
    assert bc2["risparmio_eur_anno"] == pytest.approx(6404.411764705874)
    assert bc2["van"] == pytest.approx(-83524.39594665234)
    assert bc2["breakeven_gas_eur_mwh"] == pytest.approx(79.52005347593584)
    assert bc2["payback"] is None
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_monotonia_prezzo_gas_crescente():
    base = mh793_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas_eur_mwh=91)["risparmio_eur_anno"]
    basso = _variante(p_gas_eur_mwh=89)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(611.1111111111111)
    assert base - basso == pytest.approx(611.1111111111111)


def test_monotonia_recupero_crescente_con_tetto():
    """Il risparmio cresce con il recupero finche'
    il calore recuperato non copre tutta l'ACS;
    oltre, la residua e' zero e il risparmio si
    ferma."""
    assert _variante(eta_rec=0)["risparmio_eur_anno"] < \
        mh793_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(eta_rec=1.0)["risparmio_eur_anno"] > \
        mh793_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(f_docce=1.0, eta_rec=1.0)["q_rec_kwh_anno"] == \
        pytest.approx(150000.0)
    assert _variante(f_docce=1.0, eta_rec=1.0)["q_acs_res_kwh_anno"] == 0.0


def test_demo_deterministica_due_chiamate():
    a = mh793_demo_calcoli()
    b = mh793_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh793_demo().keys()) == {
        "superficie_m2",
        "q_risc_kwh_m2_anno", "q_raff_kwh_m2_anno",
        "n_camere", "q_acs_camera_kwh_anno",
        "f_docce", "eta_rec",
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
               {"n_camere": 0}, {"n_camere": 60.5},
               {"q_acs_camera_kwh_anno": -0.1},
               {"f_docce": -0.1}, {"f_docce": 1.01},
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
        assert mh793_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"superficie_m2": "4000"},
               {"superficie_m2": float("nan")},
               {"p_gas_eur_mwh": float("inf")},
               {"capex_eur": True},
               {"q_risc_kwh_m2_anno": "100"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh793_valida(**d)["valido"] is False


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    """Differenza chiave: risparmio <= 0 NON solleva
    negli helper (resta calcolabile con flussi, VAN,
    TIR e payback), ma il verdetto e' NON_CALCOLABILE
    e la UI salta KPI, grafico, tabella e CSV."""
    for kw in ({"p_gas_eur_mwh": 0},
               {"p_gas_eur_mwh": 57.127708978328194},
               {"p_gas_eur_mwh": 40}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] <= 0.0
        assert bc["verdetto"] == "NON_CALCOLABILE"
        assert bc["flussi"]


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh793_demo_calcoli()
    testo = mh793_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_gas_eur_mwh" in testo
    assert "co2_evitata_t_anno" in testo
    assert "q_raff_kwh_anno" in testo
    assert "q_acs_res_kwh_anno" in testo
    assert "e_chiller_kwh_anno" in testo
    assert "e_pdc_acs_kwh_anno" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh793_demo_calcoli()
    testo = mh793_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"q_risc_kwh_anno;{bc['q_risc_kwh_anno']}" in testo
    assert f"gas_base_kwh_anno;{bc['gas_base_kwh_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh793_demo_calcoli()
    testo = mh793_csv(bc, _demo_kwargs())
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
    return ["mh" + "79" + "2", "st" + "79" + "2",
            "tab" + "79" + "2", "tab" + "79" + "1"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w794_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w794_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab793:")


def test_registry_chain_tail_and_count():
    """Registry della nuova tab: il frammento UI apre la tab
    numero 793 (la coda della catena termina con la nuova tab
    e il conteggio atteso delle tab e' 793)."""
    src = _leggi("w794_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 793
    assert src.count("with tab793:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w794_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w794_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st793_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) >= 24
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w794_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 3
    # Tutte le guard (input degenere e risparmio <= 0)
    # stanno prima di KPI / grafico / tabella / CSV.
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w794_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def793[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w794_ui.py")
        usate = set(re.findall(r'_def793\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 22
        assert usate <= set(mh793_demo().keys())
