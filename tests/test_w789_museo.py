"""Test tab789 "Museo: pompa di calore reversibile
+ recupero calore dalla ventilazione batte la
caldaia a gas + chiller per sale espositive?"
(titolo completo nel frammento UI).
(File repo: tests/test_w789_museo.py,
contenuto pronto da scrivere in repo.)

Business case deterministico di un museo
guidato dalla superficie espositiva in m2: il
riscaldamento delle sale piu' il raffrescamento
delle sale e' il fabbisogno, e una pompa di
calore reversibile con recupero del calore dalla
ventilazione copre il riscaldamento residuo e il
raffrescamento al posto della caldaia a gas +
chiller. Riscaldamento sale Q_risc = S x q_risc
kWh_th/anno; raffrescamento sale Q_raff = S x
q_raff kWh_c/anno; calore recuperato dalla
ventilazione Q_rec = eta_rec x f_vent x Q_risc
kWh_th/anno, SOLO dalla ventilazione (per
costruzione Q_rec <= Q_risc, perche' eta_rec x
f_vent <= 1); riscaldamento residuo Q_risc_res =
max(0, Q_risc - Q_rec) kWh_th/anno (l'eccesso
viene sprecato, senza export); gas baseline
G_base = Q_risc / eta_caldaia kWh/anno;
elettricita' chiller E_chiller = Q_raff /
COP_chiller kWh_e/anno; elettricita' pompa di
calore in riscaldamento E_pdc_risc = Q_risc_res
/ COP_risc kWh_e/anno; in raffrescamento
E_pdc_raff = Q_raff / COP_raff kWh_e/anno;
C_base = E_chiller / 1000 x p_el + G_base /
1000 x p_gas + O&M_base EUR/anno; C_alt =
(E_pdc_risc + E_pdc_raff) / 1000 x p_el +
O&M_alt EUR/anno (prezzi EUR/MWh, energie kWh:
/ 1000 esatto); risparmio = C_base - C_alt;
CO2_base = G_base / 1000 x f_gas + E_chiller /
1000 x f_el t/anno; CO2_alt = (E_pdc_risc +
E_pdc_raff) / 1000 x f_el t/anno; CO2_evitata =
CO2_base - CO2_alt; flussi [-CAPEX, risparmio
x vita]; VAN, TIR, payback (primo anno con
cumulato >= 0); breakeven gas p_gas_be = (C_alt
- E_chiller / 1000 x p_el - O&M_base) x 1000 /
G_base EUR/MWh, None se G_base <= 0 o numeratore
< 0, SOGLIA MINIMA quando esiste. Verdetto:
NON_CALCOLABILE se risparmio <= 0 (guard
degenere: UI salta KPI, grafico, tabella e CSV);
altrimenti CONVIENTE se VAN > 0, MARGINALE se
VAN negativa entro tolleranza % del CAPEX,
NON_CONVIENTE se VAN negativa oltre la
tolleranza. Distinzione esplicita: NON la
palestra (docce degli utenti con acqua calda
sanitaria + riscaldamento, recupero sulle acque
di scarico delle docce: nessun raffrescamento
di sale espositive, nessun chiller da
sostituire), NON il palaghiaccio (freddo della
pista, recupero sul calore di scarto della
refrigerazione della pista: nessun riscaldamento
di sale espositive da coprire con recupero dalla
ventilazione) e NON una tab uffici generica
(superficie generica di uffici, senza
raffrescamento di sale espositive con vincoli di
conservazione e senza chiller dedicato da
sostituire): qui il driver e' la superficie
espositiva in m2, e il calore recuperato viene
SOLO dalla ventilazione, come quota del
fabbisogno di riscaldamento.

Demo (museo): 2.500 m2 espositivi a 110
kWh_th/m2/anno di riscaldamento e 60
kWh_c/m2/anno di raffrescamento, quota
ventilazione 0,35, recupero 0,6, caldaia 0,9,
chiller COP 3,0, pompa di calore reversibile COP
riscaldamento 3,8 e COP raffrescamento 3,2, gas
90, el 250 EUR/MWh, O&M base 5.000, alt 7.000,
CAPEX 120.000, WACC 5 %, vita 15, f_gas 0,20,
f_el 0,35, tolleranza 10 % del CAPEX. Con circa
2.000 m2 la VAN sarebbe negativa (-24.602,75
EUR), per questo il demo usa 2.500 m2. Valori
calcolati eseguendo mh789_demo_calcoli():
Q_risc 275.000, Q_raff 150.000, Q_rec 57.750,
Q_risc_res 217.250, G_base 305.555,55555555556,
E_chiller 50.000, E_pdc_risc 57.171,05263157895,
E_pdc_raff 46.875, C_base 45.000, C_alt
33.011,51315789473, risparmio
11.988,486842105267, CO2_base 78,61111111111111,
CO2_alt 36,41611842105263, CO2_evitata
42,194992690058484, VAN 4.436,393816280177, TIR
5,542029508322739 %, payback 11, breakeven gas
50,76495215311003, verdetto CONVIENTE.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w790_helpers import (
    demo_calcoli,
    mh789_breakeven_gas,
    mh789_c_alt,
    mh789_c_base,
    mh789_calcola,
    mh789_co2_alt,
    mh789_co2_base,
    mh789_co2_evitata,
    mh789_cop,
    mh789_csv,
    mh789_demo,
    mh789_demo_calcoli,
    mh789_e_chiller,
    mh789_e_pdc_raff,
    mh789_e_pdc_risc,
    mh789_eta,
    mh789_eta_rec,
    mh789_f_vent,
    mh789_flussi,
    mh789_gas,
    mh789_int_pos,
    mh789_num,
    mh789_nneg,
    mh789_payback,
    mh789_pct_tolleranza,
    mh789_pct_wacc,
    mh789_pos,
    mh789_q_raff,
    mh789_q_rec,
    mh789_q_risc,
    mh789_q_risc_res,
    mh789_risparmio,
    mh789_tir,
    mh789_valida,
    mh789_van,
    mh789_verdetto,
)

_DEMO = {
    "q_risc_kwh_anno": 275000.0,
    "q_raff_kwh_anno": 150000.0,
    "q_rec_kwh_anno": 57750.0,
    "q_risc_res_kwh_anno": 217250.0,
    "gas_base_kwh_anno": 305555.55555555556,
    "e_chiller_kwh_anno": 50000.0,
    "e_pdc_risc_kwh_anno": 57171.05263157895,
    "e_pdc_raff_kwh_anno": 46875.0,
    "c_base_eur_anno": 45000.0,
    "c_alt_eur_anno": 33011.51315789473,
    "risparmio_eur_anno": 11988.486842105267,
    "co2_base_t_anno": 78.61111111111111,
    "co2_alt_t_anno": 36.41611842105263,
    "co2_evitata_t_anno": 42.194992690058484,
    "van": 4436.393816280177,
    "tir": 5.542029508322739,
    "breakeven_gas_eur_mwh": 50.76495215311003,
}


def _demo_kwargs():
    return dict(mh789_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh789_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh789_num(3, "x") == 3.0
    assert mh789_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh789_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh789_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh789_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh789_pos(0, "x")
    with pytest.raises(ValueError):
        mh789_pos(-1, "x")
    assert mh789_pos(0.5, "x") == 0.5


def test_cop_maggiore_di_uno():
    assert mh789_cop(3.8, "x") == 3.8
    assert mh789_cop(1.01, "x") == 1.01
    with pytest.raises(ValueError):
        mh789_cop(1.0, "x")
    with pytest.raises(ValueError):
        mh789_cop(0.5, "x")
    with pytest.raises(ValueError):
        mh789_cop(0, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh789_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh789_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh789_int_pos(0, "x")


def test_eta_limiti():
    assert mh789_eta(1.0, "x") == 1.0
    assert mh789_eta(0.9, "x") == 0.9
    with pytest.raises(ValueError):
        mh789_eta(0, "x")
    with pytest.raises(ValueError):
        mh789_eta(1.01, "x")


def test_eta_rec_limiti():
    assert mh789_eta_rec(0.0, "x") == 0.0
    assert mh789_eta_rec(1.0, "x") == 1.0
    assert mh789_eta_rec(0.6, "x") == 0.6
    with pytest.raises(ValueError):
        mh789_eta_rec(-0.1, "x")
    with pytest.raises(ValueError):
        mh789_eta_rec(1.01, "x")


def test_f_vent_limiti():
    assert mh789_f_vent(0.0, "x") == 0.0
    assert mh789_f_vent(1.0, "x") == 1.0
    assert mh789_f_vent(0.35, "x") == 0.35
    with pytest.raises(ValueError):
        mh789_f_vent(-0.1, "x")
    with pytest.raises(ValueError):
        mh789_f_vent(1.01, "x")


def test_pct_wacc_limiti():
    assert mh789_pct_wacc(0, "x") == 0.0
    assert mh789_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh789_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh789_pct_tolleranza(0, "x") == 0.0
    assert mh789_pct_tolleranza(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh789_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh789_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_q_risc_e_q_raff():
    assert mh789_q_risc(2500, 110) == 275000.0
    assert mh789_q_risc(1250, 110) == 137500.0
    assert mh789_q_risc(2500, 0) == 0.0
    assert mh789_q_raff(2500, 60) == 150000.0
    assert mh789_q_raff(2500, 0) == 0.0
    with pytest.raises(ValueError):
        mh789_q_risc(0, 110)
    with pytest.raises(ValueError):
        mh789_q_risc(2500, -10)
    with pytest.raises(ValueError):
        mh789_q_raff(0, 60)
    with pytest.raises(ValueError):
        mh789_q_raff(2500, -10)


def test_q_rec_solo_ventilazione():
    assert mh789_q_rec(275000, 0.35, 0.6) == 57750.0
    assert mh789_q_rec(275000, 0.35, 0) == 0.0
    assert mh789_q_rec(275000, 0, 0.6) == 0.0
    assert mh789_q_rec(275000, 0.35, 1.0) == 96250.0
    # Quota e rendimento massimi: il recupero eguaglia
    # il riscaldamento, mai lo supera.
    assert mh789_q_rec(275000, 1.0, 1.0) == 275000.0
    with pytest.raises(ValueError):
        mh789_q_rec(275000, 0.35, 1.01)
    with pytest.raises(ValueError):
        mh789_q_rec(275000, 1.01, 0.6)
    with pytest.raises(ValueError):
        mh789_q_rec(275000, -0.1, 0.6)


def test_q_risc_res_con_troncamento_a_zero():
    assert mh789_q_risc_res(275000, 57750.0) == 217250.0
    assert mh789_q_risc_res(275000, 275000.0) == 0.0
    # L'eccesso recuperato viene sprecato, senza export.
    assert mh789_q_risc_res(275000, 300000.0) == 0.0
    with pytest.raises(ValueError):
        mh789_q_risc_res(275000, -1)


def test_gas_e_chiller():
    assert mh789_gas(275000, 0.9) == pytest.approx(305555.55555555556)
    assert mh789_gas(0, 0.9) == 0.0
    assert mh789_e_chiller(150000, 3.0) == 50000.0
    assert mh789_e_chiller(0, 3.0) == 0.0
    with pytest.raises(ValueError):
        mh789_gas(275000, 0)
    with pytest.raises(ValueError):
        mh789_gas(275000, 1.01)
    with pytest.raises(ValueError):
        mh789_e_chiller(150000, 1.0)


def test_e_pdc_risc_e_raff():
    assert mh789_e_pdc_risc(217250.0, 3.8) == pytest.approx(57171.05263157895)
    assert mh789_e_pdc_risc(0, 3.8) == 0.0
    assert mh789_e_pdc_raff(150000, 3.2) == 46875.0
    assert mh789_e_pdc_raff(0, 3.2) == 0.0
    with pytest.raises(ValueError):
        mh789_e_pdc_risc(217250.0, 1.0)
    with pytest.raises(ValueError):
        mh789_e_pdc_raff(150000, 0.5)


def test_c_base_c_alt_scomposizione():
    assert mh789_c_base(50000, 250, 305555.55555555556, 90,
                        5000) == pytest.approx(45000.0)
    assert mh789_c_base(50000, 250, 305555.55555555556, 0,
                        5000) == pytest.approx(17500.0)
    assert mh789_c_alt(57171.05263157895, 46875.0, 250,
                       7000) == pytest.approx(33011.51315789473)
    assert mh789_c_alt(0, 0, 250, 7000) == pytest.approx(7000.0)
    with pytest.raises(ValueError):
        mh789_c_base(50000, 250, 305555.55555555556, -1, 5000)
    with pytest.raises(ValueError):
        mh789_c_alt(57171.05263157895, 46875.0, 250, -1)


def test_risparmio_segno():
    assert mh789_risparmio(45000.0, 33011.51315789473) == \
        pytest.approx(11988.486842105267)
    assert mh789_risparmio(33011.51315789473, 33011.51315789473) == 0.0
    assert mh789_risparmio(17500.0, 33011.51315789473) == \
        pytest.approx(-15511.513157894733)


def test_co2_base_alt_evitata():
    assert mh789_co2_base(305555.55555555556, 0.20, 50000,
                          0.35) == pytest.approx(78.61111111111111)
    assert mh789_co2_alt(57171.05263157895, 46875.0,
                         0.35) == pytest.approx(36.41611842105263)
    assert mh789_co2_evitata(305555.55555555556, 0.20, 50000,
                             57171.05263157895, 46875.0,
                             0.35) == pytest.approx(42.194992690058484)
    assert mh789_co2_base(0, 0.20, 0, 0.35) == pytest.approx(0.0)
    assert mh789_co2_alt(0, 0, 0.35) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh789_co2_base(305555.55555555556, -0.10, 50000, 0.35)
    with pytest.raises(ValueError):
        mh789_co2_alt(57171.05263157895, 46875.0, -0.10)


def test_breakeven_gas_demo_e_varianti():
    assert mh789_breakeven_gas(33011.51315789473, 50000, 250,
                               5000,
                               305555.55555555556) == \
        pytest.approx(50.76495215311003)
    assert mh789_breakeven_gas(36810.85526315789, 50000, 250,
                               5000,
                               305555.55555555556) == \
        pytest.approx(63.19916267942583)
    assert mh789_breakeven_gas(30478.618421052633, 50000, 250,
                               5000,
                               305555.55555555556) == \
        pytest.approx(42.475478468899524)
    assert mh789_breakeven_gas(33011.51315789473, 50000, 250,
                               5000, 0) is None
    # Numeratore negativo: alternativa gia' piu'
    # conveniente a prezzo gas zero -> nessun pareggio.
    assert mh789_breakeven_gas(200, 50000, 250, 5000,
                               305555.55555555556) is None
    with pytest.raises(ValueError):
        mh789_breakeven_gas(33011.51315789473, 50000, 250,
                            5000, -1)


def test_breakeven_verifica_pareggio():
    """Al prezzo gas di pareggio i costi si eguagliano
    e il risparmio e' zero: scatta la guard
    NON_CALCOLABILE, non un verdetto di convenienza."""
    bc = _variante(p_gas_eur_mwh=50.76495215311003)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    demo = mh789_demo_calcoli()
    assert (demo["c_alt_eur_anno"]
            - demo["e_chiller_kwh_anno"] / 1000.0
            * demo["p_el_eur_mwh"]
            - demo["om_base_eur_anno"]) * 1000.0 / demo["gas_base_kwh_anno"] == \
        pytest.approx(demo["breakeven_gas_eur_mwh"])


def test_breakeven_soglia_minima():
    """Sopra la soglia l'alternativa vince, sotto perde."""
    be = mh789_demo_calcoli()["breakeven_gas_eur_mwh"]
    assert _variante(p_gas_eur_mwh=be + 1)[
        "c_alt_eur_anno"] < _variante(p_gas_eur_mwh=be + 1)[
        "c_base_eur_anno"]
    assert _variante(p_gas_eur_mwh=be - 1)[
        "c_alt_eur_anno"] > _variante(p_gas_eur_mwh=be - 1)[
        "c_base_eur_anno"]


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh789_flussi(120000, 11988.486842105267, 15)
    assert len(fl) == 16
    assert fl[0] == -120000
    assert all(f == 11988.486842105267 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh789_demo_calcoli()
    assert bc["van"] == pytest.approx(4436.393816280177)
    assert mh789_van([-120000] + [11988.486842105267] * 15,
                     0) == pytest.approx(59827.30263157899)
    assert mh789_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh789_demo_calcoli()
    assert bc["tir"] == pytest.approx(5.542029508322739)
    assert mh789_tir([-120000] + [11988.486842105267] * 15) == \
        pytest.approx(0.05542029508322739)
    tir = mh789_tir([-120000] + [11988.486842105267] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-120000] + [11988.486842105267] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh789_payback([-120000] + [11988.486842105267] * 15) == 11
    assert mh789_payback([-120000] + [-1000.0] * 15) is None
    assert mh789_payback([0] + [11988.486842105267] * 15) == 0
    assert mh789_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh789_verdetto(11988.486842105267, 4436.393816280177, 120000,
                          10.0) == "CONVIENTE"
    assert mh789_verdetto(11988.486842105267, 0.0, 120000, 10.0) == "MARGINALE"
    assert mh789_verdetto(11988.486842105267, -12000.0, 120000, 10.0) == "MARGINALE"
    assert mh789_verdetto(11988.486842105267, -12000.01, 120000, 10.0) == "NON_CONVIENTE"
    assert mh789_verdetto(11988.486842105267, -90710.47, 120000, 10.0) == "NON_CONVIENTE"
    assert mh789_verdetto(0.0, 4436.393816280177, 120000,
                          10.0) == "NON_CALCOLABILE"
    assert mh789_verdetto(-3289.2909356725104, -154141.72, 120000,
                          10.0) == "NON_CALCOLABILE"
    assert mh789_verdetto(None, 4436.393816280177, 120000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh789_verdetto(float("nan"), 4436.39, 120000, 10.0)
    with pytest.raises(ValueError):
        mh789_verdetto(11988.49, 4436.39, -1, 10.0)
    with pytest.raises(ValueError):
        mh789_verdetto(11988.49, 4436.39, 120000, 100.1)


def test_valida_demo_ok():
    v = mh789_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("superficie_m2", "2500"),
                       ("superficie_m2", float("nan")),
                       ("superficie_m2", float("inf")),
                       ("superficie_m2", True),
                       ("p_gas_eur_mwh", None),
                       ("q_risc_kwh_m2_anno", "110")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh789_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("superficie_m2", 0),
                          ("superficie_m2", -10),
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
        assert mh789_valida(**d)["valido"] is False


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
    assert mh789_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["eta_rec"] = 1
    d["f_vent"] = 1
    d["q_risc_kwh_m2_anno"] = 110
    assert mh789_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh789_demo()
    assert d["superficie_m2"] == 2500
    assert d["q_risc_kwh_m2_anno"] == 110
    assert d["q_raff_kwh_m2_anno"] == 60
    assert d["f_vent"] == 0.35
    assert d["eta_rec"] == 0.6
    assert d["eta_caldaia"] == 0.9
    assert d["cop_chiller"] == 3.0
    assert d["cop_risc"] == 3.8
    assert d["cop_raff"] == 3.2
    assert d["p_gas_eur_mwh"] == 90
    assert d["p_el_eur_mwh"] == 250
    assert d["om_base_eur_anno"] == 5000
    assert d["om_alt_eur_anno"] == 7000
    assert d["capex_eur"] == 120000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["f_gas_t_per_mwh"] == 0.20
    assert d["f_el_t_per_mwh"] == 0.35
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    """Tutti gli output numerici demo a tolleranza
    1e-9 relativa: confronto delle costanti _DEMO
    contro mh789_demo_calcoli()."""
    bc = mh789_demo_calcoli()
    for chiave, atteso in _DEMO.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert got == pytest.approx(atteso, rel=1e-9), chiave
    assert bc["payback"] == 11
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True
    assert demo_calcoli()["van"] == bc["van"]


def test_demo_calcoli_fisica_economia():
    bc = mh789_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(45000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(33011.51315789473)
    assert bc["risparmio_eur_anno"] == pytest.approx(11988.486842105267)
    assert bc["co2_base_t_anno"] == pytest.approx(78.61111111111111)
    assert bc["co2_alt_t_anno"] == pytest.approx(36.41611842105263)
    assert bc["co2_evitata_t_anno"] == pytest.approx(42.194992690058484)
    assert bc["gas_base_kwh_anno"] == pytest.approx(305555.55555555556)


def test_demo_flussi_e_cumulato():
    bc = mh789_demo_calcoli()
    assert bc["flussi"][0] == -120000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(11988.486842105267) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -120000
    assert righe.iloc[9]["Cumulato (EUR)"] == pytest.approx(-12103.618421052597)
    assert righe.iloc[10]["Cumulato (EUR)"] == pytest.approx(-115.13157894733013)
    assert righe.iloc[11]["Cumulato (EUR)"] == pytest.approx(11873.355263157937)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(59827.30263157899)


def test_demo_tabella_righe():
    bc = mh789_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Riscaldamento sale (kWh_th/anno)"] == pytest.approx(275000.0)
    assert mappa["Raffrescamento sale (kWh_c/anno)"] == pytest.approx(150000.0)
    assert mappa["Calore recuperato ventilazione (kWh_th/anno)"] == pytest.approx(57750.0)
    assert mappa["Riscaldamento residuo (kWh_th/anno)"] == pytest.approx(217250.0)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(305555.55555555556)
    assert mappa["Elettricita' chiller (kWh_e/anno)"] == pytest.approx(50000.0)
    assert mappa["Elettricita' pompa di calore riscaldamento (kWh_e/anno)"] == pytest.approx(57171.05263157895)
    assert mappa["Elettricita' pompa di calore raffrescamento (kWh_e/anno)"] == pytest.approx(46875.0)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(45000.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(33011.51315789473)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(11988.486842105267)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(42.194992690058484)
    assert mappa["Payback (anni)"] == 11
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] == \
        pytest.approx(50.76495215311003)


def test_demo_coerenza_interna():
    bc = mh789_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["q_risc_kwh_anno"] == pytest.approx(
        bc["superficie_m2"] * bc["q_risc_kwh_m2_anno"])
    assert bc["q_raff_kwh_anno"] == pytest.approx(
        bc["superficie_m2"] * bc["q_raff_kwh_m2_anno"])
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
    s, qr_spec, qf_spec = 2500, 110, 60
    fv, erec = 0.35, 0.6
    eta, copc, copr, copf = 0.9, 3.0, 3.8, 3.2
    pg, pel, omb, oma, cx = 90, 250, 5000, 7000, 120000
    fg, fel, wacc, vita = 0.20, 0.35, 5.0, 15
    qrisc = s * qr_spec
    qraff = s * qf_spec
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
    bc = mh789_demo_calcoli()
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
    (2.821,82) ma VAN -90.710,47 oltre la tolleranza
    (12.000): NON_CONVIENTE con payback mai
    raggiunto. Il verdetto guarda la VAN, non il
    solo risparmio positivo."""
    bc = _variante(p_gas_eur_mwh=60)
    assert bc["risparmio_eur_anno"] == pytest.approx(2821.8201754385955)
    assert bc["van"] == pytest.approx(-90710.47153370862)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_gas_40_non_calcolabile():
    """Gas 40 EUR/MWh: risparmio -3.289,29, verdetto
    NON_CALCOLABILE, ma helper calcolabili (flussi
    pieni, VAN negativa, TIR None, payback None)."""
    bc = _variante(p_gas_eur_mwh=40)
    assert bc["risparmio_eur_anno"] == pytest.approx(-3289.2909356725104)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_gas_zero_non_calcolabile():
    """Gas zero: costo baseline 17.500 (chiller
    12.500 + O&M 5.000, zero gas) contro 33.011,51
    dell'alternativa: risparmio -15.511,51,
    verdetto NON_CALCOLABILE."""
    bc = _variante(p_gas_eur_mwh=0)
    assert bc["valid"] is True
    assert bc["c_base_eur_anno"] == pytest.approx(17500.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-15511.513157894733)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_senza_recupero_non_conviente():
    """Senza recupero (eta_rec zero): riscaldamento
    residuo 275.000, E_pdc_risc 72.368,42, risparmio
    8.189,14, VAN -34.999,48, breakeven 63,20,
    NON_CONVIENTE con payback 15 anni. Il recupero
    dalla ventilazione e' decisivo: senza di esso
    la pompa di calore lavora a pieno carico in
    riscaldamento."""
    bc = _variante(eta_rec=0)
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["q_risc_res_kwh_anno"] == pytest.approx(275000.0)
    assert bc["e_pdc_risc_kwh_anno"] == pytest.approx(72368.42105263159)
    assert bc["risparmio_eur_anno"] == pytest.approx(8189.144736842107)
    assert bc["van"] == pytest.approx(-34999.47800641255)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(63.19916267942583)
    assert bc["payback"] == 15
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_recupero_totale_conviente():
    """Recupero totale (eta_rec 1,0): calore
    recuperato 96.250, residuo 178.750, E_pdc_risc
    47.039,47, risparmio 14.521,38, VAN 30.726,98,
    payback 9, breakeven 42,48, CONVIENTE."""
    bc = _variante(eta_rec=1.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(96250.0)
    assert bc["q_risc_res_kwh_anno"] == pytest.approx(178750.0)
    assert bc["e_pdc_risc_kwh_anno"] == pytest.approx(47039.47368421053)
    assert bc["risparmio_eur_anno"] == pytest.approx(14521.381578947367)
    assert bc["van"] == pytest.approx(30726.975031408598)
    assert bc["payback"] == 9
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(42.475478468899524)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_senza_raffrescamento_marginale():
    """Senza raffrescamento (q_raff zero): il chiller
    sparisce da entrambi i costi, risparmio
    11.207,24, VAN -3.672,71 entro la tolleranza
    (12.000), quindi MARGINALE con payback 11 e
    breakeven 53,32: il raffrescamento con pompa di
    calore reversibile contribuisce al caso."""
    bc = _variante(q_raff_kwh_m2_anno=0)
    assert bc["q_raff_kwh_anno"] == 0.0
    assert bc["e_chiller_kwh_anno"] == 0.0
    assert bc["e_pdc_raff_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(11207.236842105263)
    assert bc["van"] == pytest.approx(-3672.714026048445)
    assert bc["payback"] == 11
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(53.321770334928225)
    assert bc["verdetto"] == "MARGINALE"


def test_variante_capex_alto_marginale_e_non_conviente():
    bc = _variante(capex_eur=130000)
    assert bc["risparmio_eur_anno"] == pytest.approx(11988.486842105267)
    assert bc["van"] == pytest.approx(-5563.606183719822)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"
    bc2 = _variante(capex_eur=140000)
    assert bc2["van"] == pytest.approx(-15563.606183719821)
    assert bc2["payback"] == 12
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex_eur=0)
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(124436.39381628018, rel=1e-6)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(59827.30263157899)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(-27428.082403243257)
    assert bc2["payback"] is None
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_el_alto_e_cop_risc_basso():
    """Elettricita' 350 EUR/MWh: risparmio 6.583,88,
    VAN -51.661,56, breakeven 68,45, NON_CONVIENTE.
    COP riscaldamento 2,5: E_pdc_risc 86.900,
    risparmio 4.556,25, VAN -72.707,68, breakeven
    75,09, NON_CONVIENTE."""
    bc = _variante(p_el_eur_mwh=350)
    assert bc["risparmio_eur_anno"] == pytest.approx(6583.8815789473665)
    assert bc["van"] == pytest.approx(-51661.56064664986)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(68.45275119617226)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"
    bc2 = _variante(cop_risc=2.5)
    assert bc2["e_pdc_risc_kwh_anno"] == pytest.approx(86900.0)
    assert bc2["risparmio_eur_anno"] == pytest.approx(4556.25)
    assert bc2["van"] == pytest.approx(-72707.68306353968)
    assert bc2["breakeven_gas_eur_mwh"] == pytest.approx(75.08863636363637)
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_monotonia_prezzo_gas_crescente():
    base = mh789_demo_calcoli()["risparmio_eur_anno"]
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
        mh789_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(eta_rec=1.0)["risparmio_eur_anno"] > \
        mh789_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(f_vent=1.0, eta_rec=1.0)["q_rec_kwh_anno"] == \
        pytest.approx(275000.0)
    assert _variante(f_vent=1.0, eta_rec=1.0)["q_risc_res_kwh_anno"] == 0.0


def test_demo_deterministica_due_chiamate():
    a = mh789_demo_calcoli()
    b = mh789_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh789_demo().keys()) == {
        "superficie_m2", "q_risc_kwh_m2_anno",
        "q_raff_kwh_m2_anno", "f_vent", "eta_rec",
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
    for kw in ({"superficie_m2": 0},
               {"superficie_m2": -10},
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
        assert mh789_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"superficie_m2": "2500"},
               {"superficie_m2": float("nan")},
               {"p_gas_eur_mwh": float("inf")},
               {"capex_eur": True},
               {"q_risc_kwh_m2_anno": "110"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh789_valida(**d)["valido"] is False


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    """Differenza chiave: risparmio <= 0 NON solleva
    negli helper (resta calcolabile con flussi, VAN,
    TIR e payback), ma il verdetto e' NON_CALCOLABILE
    e la UI salta KPI, grafico, tabella e CSV."""
    for kw in ({"p_gas_eur_mwh": 0},
               {"p_gas_eur_mwh": 50.76495215311003},
               {"p_gas_eur_mwh": 40}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] <= 0.0
        assert bc["verdetto"] == "NON_CALCOLABILE"
        assert bc["flussi"]


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh789_demo_calcoli()
    testo = mh789_csv(bc, _demo_kwargs())
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
    bc = mh789_demo_calcoli()
    testo = mh789_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"q_risc_kwh_anno;{bc['q_risc_kwh_anno']}" in testo
    assert f"gas_base_kwh_anno;{bc['gas_base_kwh_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh789_demo_calcoli()
    testo = mh789_csv(bc, _demo_kwargs())
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
    return ["mh" + "78" + "8", "st" + "78" + "8",
            "tab" + "78" + "8", "tab" + "78" + "7"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w790_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w790_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab789:")


def test_registry_chain_tail_and_count():
    """Registry della nuova tab: il frammento UI apre la tab
    numero 789 (la coda della catena termina con la nuova tab
    e il conteggio atteso delle tab e' 789)."""
    src = _leggi("w790_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 789
    assert src.count("with tab789:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w790_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w790_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st789_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) >= 24
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w790_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 2
    # Entrambe le guard (input degenere e risparmio <= 0)
    # stanno prima di KPI / grafico / tabella / CSV.
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w790_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def789[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w790_ui.py")
        usate = set(re.findall(r'_def789\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 19
        assert usate <= set(mh789_demo().keys())
