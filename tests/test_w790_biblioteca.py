"""Test tab790 "Biblioteca: pompa di calore reversibile
+ recupero calore ventilazione sale lettura +
climatizzazione continua depositi batte la
caldaia a gas + chiller?"
(titolo completo nel frammento UI).
(File repo: tests/test_w790_biblioteca.py,
contenuto pronto da scrivere in repo.)

Business case deterministico di una biblioteca
guidato da due superfici in m2: sale lettura e
depositi archivio con raffrescamento continuo.
Riscaldamento sale lettura Q_risc = S_lett x
q_risc kWh_th/anno; raffrescamento sale lettura
Q_raff = S_lett x q_raff kWh_c/anno;
raffrescamento continuo depositi Q_dep_raff =
S_dep x q_dep_raff kWh_c/anno; raffrescamento
totale Q_raff_tot = Q_raff + Q_dep_raff;
calore recuperato dalla ventilazione Q_rec =
eta_rec x f_vent x Q_risc kWh_th/anno, SOLO
dalla ventilazione (per costruzione Q_rec <=
Q_risc, perche' eta_rec x f_vent <= 1);
riscaldamento residuo Q_risc_res = max(0,
Q_risc - Q_rec) kWh_th/anno (l'eccesso viene
sprecato, senza export); gas baseline G_base =
Q_risc / eta_caldaia kWh/anno; elettricita'
chiller E_chiller = Q_raff_tot / COP_chiller
kWh_e/anno; elettricita' pompa di calore in
riscaldamento E_pdc_risc = Q_risc_res / COP_risc
kWh_e/anno; in raffrescamento E_pdc_raff =
Q_raff_tot / COP_raff kWh_e/anno; C_base =
E_chiller / 1000 x p_el + G_base / 1000 x p_gas
+ O&M_base EUR/anno; C_alt = (E_pdc_risc +
E_pdc_raff) / 1000 x p_el + O&M_alt EUR/anno
(prezzi EUR/MWh, energie kWh: / 1000 esatto);
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
espositiva, senza depositi archivio e senza
raffrescamento continuo di depositi: nessun
fabbisogno di freddo continuo da coprire),
NON la scuola (aule e palestra scolastica con
orari e chiusure stagionali, senza depositi
archivio da climatizzare in continuo) e NON la
palestra (docce degli utenti con acqua calda
sanitaria + riscaldamento, recupero sulle acque
di scarico delle docce: nessun raffrescamento
continuo di depositi archivio, nessun chiller
da sostituire per depositi): qui i driver sono
DUE superfici, m2 di sale lettura + m2 di
depositi archivio con raffrescamento continuo,
e il calore recuperato viene SOLO dalla
ventilazione, come quota del fabbisogno di
riscaldamento delle sale lettura.

Demo (biblioteca): 3.000 m2 di sale lettura a
100 kWh_th/m2/anno di riscaldamento e 50
kWh_c/m2/anno di raffrescamento, depositi
archivio 800 m2 con raffrescamento continuo 80
kWh_c/m2/anno, quota ventilazione 0,40,
recupero 0,60, caldaia 0,90, chiller COP 3,0,
pompa di calore reversibile COP riscaldamento
3,8 e COP raffrescamento 3,2, gas 90, el 250
EUR/MWh, O&M base 5.000, alt 7.000, CAPEX
110.000, WACC 5 %, vita 15, f_gas 0,20, f_el
0,35, tolleranza 10 % del CAPEX. Valori
calcolati eseguendo mh790_demo_calcoli():
Q_risc 300.000, Q_raff sale 150.000, Q_dep_raff
64.000, Q_raff_tot 214.000, Q_rec 72.000,
Q_risc_res 228.000, G_base 333.333,3333333333,
E_chiller 71.333,33333333333, E_pdc_risc
60.000, E_pdc_raff 66.875, C_base
52.833,33333333333, C_alt 38.718,75, risparmio
14.114,583333333328, CO2_base 91,63333333333334,
CO2_alt 44,40625, CO2_evitata
47,22708333333334, VAN 36.504,54835140307, TIR
9,576890577667026 %, payback 8, breakeven gas
47,65625, verdetto CONVIENTE.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w791_helpers import (
    demo_calcoli,
    mh790_breakeven_gas,
    mh790_c_alt,
    mh790_c_base,
    mh790_calcola,
    mh790_co2_alt,
    mh790_co2_base,
    mh790_co2_evitata,
    mh790_cop,
    mh790_csv,
    mh790_demo,
    mh790_demo_calcoli,
    mh790_e_chiller,
    mh790_e_pdc_raff,
    mh790_e_pdc_risc,
    mh790_eta,
    mh790_eta_rec,
    mh790_f_vent,
    mh790_flussi,
    mh790_gas,
    mh790_int_pos,
    mh790_num,
    mh790_nneg,
    mh790_payback,
    mh790_pct_tolleranza,
    mh790_pct_wacc,
    mh790_pos,
    mh790_q_dep_raff,
    mh790_q_raff,
    mh790_q_rec,
    mh790_q_risc,
    mh790_q_risc_res,
    mh790_risparmio,
    mh790_tir,
    mh790_valida,
    mh790_van,
    mh790_verdetto,
)

_DEMO = {
    "q_risc_kwh_anno": 300000.0,
    "q_raff_kwh_anno": 150000.0,
    "q_dep_raff_kwh_anno": 64000.0,
    "q_raff_tot_kwh_anno": 214000.0,
    "q_rec_kwh_anno": 72000.0,
    "q_risc_res_kwh_anno": 228000.0,
    "gas_base_kwh_anno": 333333.3333333333,
    "e_chiller_kwh_anno": 71333.33333333333,
    "e_pdc_risc_kwh_anno": 60000.0,
    "e_pdc_raff_kwh_anno": 66875.0,
    "c_base_eur_anno": 52833.33333333333,
    "c_alt_eur_anno": 38718.75,
    "risparmio_eur_anno": 14114.583333333328,
    "co2_base_t_anno": 91.63333333333334,
    "co2_alt_t_anno": 44.40625,
    "co2_evitata_t_anno": 47.22708333333334,
    "van": 36504.54835140307,
    "tir": 9.576890577667026,
    "breakeven_gas_eur_mwh": 47.65625000000001,
}


def _demo_kwargs():
    return dict(mh790_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh790_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh790_num(3, "x") == 3.0
    assert mh790_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh790_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh790_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh790_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh790_pos(0, "x")
    with pytest.raises(ValueError):
        mh790_pos(-1, "x")
    assert mh790_pos(0.5, "x") == 0.5


def test_cop_maggiore_di_uno():
    assert mh790_cop(3.8, "x") == 3.8
    assert mh790_cop(1.01, "x") == 1.01
    with pytest.raises(ValueError):
        mh790_cop(1.0, "x")
    with pytest.raises(ValueError):
        mh790_cop(0.5, "x")
    with pytest.raises(ValueError):
        mh790_cop(0, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh790_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh790_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh790_int_pos(0, "x")


def test_eta_limiti():
    assert mh790_eta(1.0, "x") == 1.0
    assert mh790_eta(0.9, "x") == 0.9
    with pytest.raises(ValueError):
        mh790_eta(0, "x")
    with pytest.raises(ValueError):
        mh790_eta(1.01, "x")


def test_eta_rec_limiti():
    assert mh790_eta_rec(0.0, "x") == 0.0
    assert mh790_eta_rec(1.0, "x") == 1.0
    assert mh790_eta_rec(0.6, "x") == 0.6
    with pytest.raises(ValueError):
        mh790_eta_rec(-0.1, "x")
    with pytest.raises(ValueError):
        mh790_eta_rec(1.01, "x")


def test_f_vent_limiti():
    assert mh790_f_vent(0.0, "x") == 0.0
    assert mh790_f_vent(1.0, "x") == 1.0
    assert mh790_f_vent(0.40, "x") == 0.40
    with pytest.raises(ValueError):
        mh790_f_vent(-0.1, "x")
    with pytest.raises(ValueError):
        mh790_f_vent(1.01, "x")


def test_pct_wacc_limiti():
    assert mh790_pct_wacc(0, "x") == 0.0
    assert mh790_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh790_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh790_pct_tolleranza(0, "x") == 0.0
    assert mh790_pct_tolleranza(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh790_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh790_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_q_risc_q_raff_e_q_dep_raff():
    assert mh790_q_risc(3000, 100) == 300000.0
    assert mh790_q_risc(1500, 100) == 150000.0
    assert mh790_q_risc(3000, 0) == 0.0
    assert mh790_q_raff(3000, 50) == 150000.0
    assert mh790_q_raff(3000, 0) == 0.0
    assert mh790_q_dep_raff(800, 80) == 64000.0
    assert mh790_q_dep_raff(800, 0) == 0.0
    assert mh790_q_dep_raff(400, 80) == 32000.0
    with pytest.raises(ValueError):
        mh790_q_risc(0, 100)
    with pytest.raises(ValueError):
        mh790_q_risc(3000, -10)
    with pytest.raises(ValueError):
        mh790_q_raff(0, 50)
    with pytest.raises(ValueError):
        mh790_q_raff(3000, -10)
    with pytest.raises(ValueError):
        mh790_q_dep_raff(0, 80)
    with pytest.raises(ValueError):
        mh790_q_dep_raff(800, -10)


def test_q_rec_solo_ventilazione():
    assert mh790_q_rec(300000, 0.40, 0.60) == 72000.0
    assert mh790_q_rec(300000, 0.40, 0) == 0.0
    assert mh790_q_rec(300000, 0, 0.60) == 0.0
    assert mh790_q_rec(300000, 0.40, 1.0) == 120000.0
    # Quota e rendimento massimi: il recupero eguaglia
    # il riscaldamento, mai lo supera.
    assert mh790_q_rec(300000, 1.0, 1.0) == 300000.0
    with pytest.raises(ValueError):
        mh790_q_rec(300000, 0.40, 1.01)
    with pytest.raises(ValueError):
        mh790_q_rec(300000, 1.01, 0.60)
    with pytest.raises(ValueError):
        mh790_q_rec(300000, -0.1, 0.60)


def test_q_risc_res_con_troncamento_a_zero():
    assert mh790_q_risc_res(300000, 72000.0) == 228000.0
    assert mh790_q_risc_res(300000, 300000.0) == 0.0
    # L'eccesso recuperato viene sprecato, senza export.
    assert mh790_q_risc_res(300000, 400000.0) == 0.0
    with pytest.raises(ValueError):
        mh790_q_risc_res(300000, -1)


def test_gas_e_chiller_su_raffrescamento_totale():
    assert mh790_gas(300000, 0.9) == pytest.approx(333333.3333333333)
    assert mh790_gas(0, 0.9) == 0.0
    # Il chiller serve sale lettura + depositi: 214.000 totali.
    assert mh790_e_chiller(214000, 3.0) == pytest.approx(71333.33333333333)
    assert mh790_e_chiller(150000, 3.0) == 50000.0
    assert mh790_e_chiller(0, 3.0) == 0.0
    with pytest.raises(ValueError):
        mh790_gas(300000, 0)
    with pytest.raises(ValueError):
        mh790_gas(300000, 1.01)
    with pytest.raises(ValueError):
        mh790_e_chiller(214000, 1.0)


def test_e_pdc_risc_e_raff():
    assert mh790_e_pdc_risc(228000.0, 3.8) == pytest.approx(60000.0)
    assert mh790_e_pdc_risc(0, 3.8) == 0.0
    assert mh790_e_pdc_raff(214000, 3.2) == pytest.approx(66875.0)
    assert mh790_e_pdc_raff(0, 3.2) == 0.0
    with pytest.raises(ValueError):
        mh790_e_pdc_risc(228000.0, 1.0)
    with pytest.raises(ValueError):
        mh790_e_pdc_raff(214000, 0.5)


def test_c_base_c_alt_scomposizione():
    assert mh790_c_base(71333.33333333333, 250, 333333.3333333333, 90,
                        5000) == pytest.approx(52833.33333333333)
    assert mh790_c_base(71333.33333333333, 250, 333333.3333333333, 0,
                        5000) == pytest.approx(22833.333333333332)
    assert mh790_c_alt(60000.0, 66875.0, 250,
                       7000) == pytest.approx(38718.75)
    assert mh790_c_alt(0, 0, 250, 7000) == pytest.approx(7000.0)
    with pytest.raises(ValueError):
        mh790_c_base(71333.33333333333, 250, 333333.3333333333, -1, 5000)
    with pytest.raises(ValueError):
        mh790_c_alt(60000.0, 66875.0, 250, -1)


def test_risparmio_segno():
    assert mh790_risparmio(52833.33333333333, 38718.75) == \
        pytest.approx(14114.583333333328)
    assert mh790_risparmio(38718.75, 38718.75) == 0.0
    assert mh790_risparmio(22833.333333333332, 38718.75) == \
        pytest.approx(-15885.416666666668)


def test_co2_base_alt_evitata():
    assert mh790_co2_base(333333.3333333333, 0.20, 71333.33333333333,
                          0.35) == pytest.approx(91.63333333333334)
    assert mh790_co2_alt(60000.0, 66875.0,
                         0.35) == pytest.approx(44.40625)
    assert mh790_co2_evitata(333333.3333333333, 0.20, 71333.33333333333,
                             60000.0, 66875.0,
                             0.35) == pytest.approx(47.22708333333334)
    assert mh790_co2_base(0, 0.20, 0, 0.35) == pytest.approx(0.0)
    assert mh790_co2_alt(0, 0, 0.35) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh790_co2_base(333333.3333333333, -0.10, 71333.33333333333, 0.35)
    with pytest.raises(ValueError):
        mh790_co2_alt(60000.0, 66875.0, -0.10)


def test_breakeven_gas_demo_e_varianti():
    assert mh790_breakeven_gas(38718.75, 71333.33333333333, 250,
                               5000,
                               333333.3333333333) == \
        pytest.approx(47.65625000000001)
    assert mh790_breakeven_gas(43455.59210526316, 71333.33333333333, 250,
                               5000,
                               333333.3333333333) == \
        pytest.approx(61.86677631578949)
    assert mh790_breakeven_gas(35560.85526315789, 71333.33333333333, 250,
                               5000,
                               333333.3333333333) == \
        pytest.approx(38.182565789473685)
    assert mh790_breakeven_gas(38718.75, 71333.33333333333, 250,
                               5000, 0) is None
    # Numeratore negativo: alternativa gia' piu'
    # conveniente a prezzo gas zero -> nessun pareggio.
    assert mh790_breakeven_gas(200, 71333.33333333333, 250, 5000,
                               333333.3333333333) is None
    with pytest.raises(ValueError):
        mh790_breakeven_gas(38718.75, 71333.33333333333, 250,
                            5000, -1)


def test_breakeven_verifica_pareggio():
    """Al prezzo gas di pareggio i costi si eguagliano
    e il risparmio e' zero: scatta la guard
    NON_CALCOLABILE, non un verdetto di convenienza."""
    bc = _variante(p_gas_eur_mwh=47.65625000000001)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    demo = mh790_demo_calcoli()
    assert (demo["c_alt_eur_anno"]
            - demo["e_chiller_kwh_anno"] / 1000.0
            * demo["p_el_eur_mwh"]
            - demo["om_base_eur_anno"]) * 1000.0 / demo["gas_base_kwh_anno"] == \
        pytest.approx(demo["breakeven_gas_eur_mwh"])


def test_breakeven_soglia_minima():
    """Sopra la soglia l'alternativa vince, sotto perde."""
    be = mh790_demo_calcoli()["breakeven_gas_eur_mwh"]
    assert _variante(p_gas_eur_mwh=be + 1)[
        "c_alt_eur_anno"] < _variante(p_gas_eur_mwh=be + 1)[
        "c_base_eur_anno"]
    assert _variante(p_gas_eur_mwh=be - 1)[
        "c_alt_eur_anno"] > _variante(p_gas_eur_mwh=be - 1)[
        "c_base_eur_anno"]


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh790_flussi(110000, 14114.583333333328, 15)
    assert len(fl) == 16
    assert fl[0] == -110000
    assert all(f == 14114.583333333328 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh790_demo_calcoli()
    assert bc["van"] == pytest.approx(36504.54835140307)
    assert mh790_van([-110000] + [14114.583333333328] * 15,
                     0) == pytest.approx(101718.74999999993)
    assert mh790_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh790_demo_calcoli()
    assert bc["tir"] == pytest.approx(9.576890577667026)
    assert mh790_tir([-110000] + [14114.583333333328] * 15) == \
        pytest.approx(0.09576890577667026)
    tir = mh790_tir([-110000] + [14114.583333333328] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-110000] + [14114.583333333328] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh790_payback([-110000] + [14114.583333333328] * 15) == 8
    assert mh790_payback([-110000] + [-1000.0] * 15) is None
    assert mh790_payback([0] + [14114.583333333328] * 15) == 0
    assert mh790_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh790_verdetto(14114.583333333328, 36504.54835140307, 110000,
                          10.0) == "CONVIENTE"
    assert mh790_verdetto(14114.583333333328, 0.0, 110000, 10.0) == "MARGINALE"
    assert mh790_verdetto(14114.583333333328, -11000.0, 110000, 10.0) == "MARGINALE"
    assert mh790_verdetto(14114.583333333328, -11000.01, 110000, 10.0) == "NON_CONVIENTE"
    assert mh790_verdetto(14114.583333333328, -67292.03, 110000, 10.0) == "NON_CONVIENTE"
    assert mh790_verdetto(0.0, 36504.54835140307, 110000,
                          10.0) == "NON_CALCOLABILE"
    assert mh790_verdetto(-2552.0833333333358, -136489.75, 110000,
                          10.0) == "NON_CALCOLABILE"
    assert mh790_verdetto(None, 36504.54835140307, 110000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh790_verdetto(float("nan"), 36504.55, 110000, 10.0)
    with pytest.raises(ValueError):
        mh790_verdetto(14114.58, 36504.55, -1, 10.0)
    with pytest.raises(ValueError):
        mh790_verdetto(14114.58, 36504.55, 110000, 100.1)


def test_valida_demo_ok():
    v = mh790_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("superficie_lettura_m2", "3000"),
                       ("superficie_depositi_m2", "800"),
                       ("superficie_lettura_m2", float("nan")),
                       ("superficie_lettura_m2", float("inf")),
                       ("superficie_lettura_m2", True),
                       ("p_gas_eur_mwh", None),
                       ("q_risc_kwh_m2_anno", "100")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh790_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("superficie_lettura_m2", 0),
                          ("superficie_lettura_m2", -10),
                          ("superficie_depositi_m2", 0),
                          ("superficie_depositi_m2", -10),
                          ("q_risc_kwh_m2_anno", -0.1),
                          ("q_raff_kwh_m2_anno", -0.1),
                          ("q_dep_raff_kwh_m2_anno", -0.1),
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
        assert mh790_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"q_risc_kwh_m2_anno": 0,
              "q_raff_kwh_m2_anno": 0,
              "q_dep_raff_kwh_m2_anno": 0,
              "f_vent": 0,
              "eta_rec": 0,
              "p_gas_eur_mwh": 0,
              "p_el_eur_mwh": 0,
              "om_base_eur_anno": 0, "om_alt_eur_anno": 0,
              "capex_eur": 0, "wacc_pct": 0,
              "f_gas_t_per_mwh": 0, "f_el_t_per_mwh": 0,
              "tolleranza_pct": 0})
    assert mh790_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["eta_rec"] = 1
    d["f_vent"] = 1
    d["q_risc_kwh_m2_anno"] = 100
    assert mh790_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh790_demo()
    assert d["superficie_lettura_m2"] == 3000
    assert d["superficie_depositi_m2"] == 800
    assert d["q_risc_kwh_m2_anno"] == 100
    assert d["q_raff_kwh_m2_anno"] == 50
    assert d["q_dep_raff_kwh_m2_anno"] == 80
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
    assert d["capex_eur"] == 110000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["f_gas_t_per_mwh"] == 0.20
    assert d["f_el_t_per_mwh"] == 0.35
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    """Tutti gli output numerici demo a tolleranza
    1e-9 relativa: confronto delle costanti _DEMO
    contro mh790_demo_calcoli()."""
    bc = mh790_demo_calcoli()
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
    bc = mh790_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(52833.33333333333)
    assert bc["c_alt_eur_anno"] == pytest.approx(38718.75)
    assert bc["risparmio_eur_anno"] == pytest.approx(14114.583333333328)
    assert bc["co2_base_t_anno"] == pytest.approx(91.63333333333334)
    assert bc["co2_alt_t_anno"] == pytest.approx(44.40625)
    assert bc["co2_evitata_t_anno"] == pytest.approx(47.22708333333334)
    assert bc["gas_base_kwh_anno"] == pytest.approx(333333.3333333333)


def test_demo_flussi_e_cumulato():
    bc = mh790_demo_calcoli()
    assert bc["flussi"][0] == -110000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(14114.583333333328) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -110000
    assert righe.iloc[7]["Cumulato (EUR)"] == pytest.approx(-11197.9166666667)
    assert righe.iloc[8]["Cumulato (EUR)"] == pytest.approx(2916.666666666628)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(101718.74999999993)


def test_demo_tabella_righe():
    bc = mh790_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Riscaldamento sale lettura (kWh_th/anno)"] == pytest.approx(300000.0)
    assert mappa["Raffrescamento sale lettura (kWh_c/anno)"] == pytest.approx(150000.0)
    assert mappa["Raffrescamento continuo depositi (kWh_c/anno)"] == pytest.approx(64000.0)
    assert mappa["Raffrescamento totale (kWh_c/anno)"] == pytest.approx(214000.0)
    assert mappa["Calore recuperato ventilazione (kWh_th/anno)"] == pytest.approx(72000.0)
    assert mappa["Riscaldamento residuo (kWh_th/anno)"] == pytest.approx(228000.0)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(333333.3333333333)
    assert mappa["Elettricita' chiller (kWh_e/anno)"] == pytest.approx(71333.33333333333)
    assert mappa["Elettricita' pompa di calore riscaldamento (kWh_e/anno)"] == pytest.approx(60000.0)
    assert mappa["Elettricita' pompa di calore raffrescamento (kWh_e/anno)"] == pytest.approx(66875.0)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(52833.33333333333)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(38718.75)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(14114.583333333328)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(47.22708333333334)
    assert mappa["Payback (anni)"] == 8
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] == \
        pytest.approx(47.65625000000001)


def test_demo_coerenza_interna():
    bc = mh790_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["q_risc_kwh_anno"] == pytest.approx(
        bc["superficie_lettura_m2"] * bc["q_risc_kwh_m2_anno"])
    assert bc["q_raff_kwh_anno"] == pytest.approx(
        bc["superficie_lettura_m2"] * bc["q_raff_kwh_m2_anno"])
    assert bc["q_dep_raff_kwh_anno"] == pytest.approx(
        bc["superficie_depositi_m2"] * bc["q_dep_raff_kwh_m2_anno"])
    assert bc["q_raff_tot_kwh_anno"] == pytest.approx(
        bc["q_raff_kwh_anno"] + bc["q_dep_raff_kwh_anno"])
    assert bc["q_rec_kwh_anno"] == pytest.approx(
        bc["eta_rec"] * bc["f_vent"] * bc["q_risc_kwh_anno"])
    assert bc["q_risc_res_kwh_anno"] == pytest.approx(
        max(0.0, bc["q_risc_kwh_anno"] - bc["q_rec_kwh_anno"]))
    assert bc["gas_base_kwh_anno"] == pytest.approx(
        bc["q_risc_kwh_anno"] / bc["eta_caldaia"])
    assert bc["e_chiller_kwh_anno"] == pytest.approx(
        bc["q_raff_tot_kwh_anno"] / bc["cop_chiller"])
    assert bc["e_pdc_risc_kwh_anno"] == pytest.approx(
        bc["q_risc_res_kwh_anno"] / bc["cop_risc"])
    assert bc["e_pdc_raff_kwh_anno"] == pytest.approx(
        bc["q_raff_tot_kwh_anno"] / bc["cop_raff"])
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
    s_lett, s_dep = 3000, 800
    qr_spec, qf_spec, qd_spec = 100, 50, 80
    fv, erec = 0.40, 0.60
    eta, copc, copr, copf = 0.90, 3.0, 3.8, 3.2
    pg, pel, omb, oma, cx = 90, 250, 5000, 7000, 110000
    fg, fel, wacc, vita = 0.20, 0.35, 5.0, 15
    qrisc = s_lett * qr_spec
    qraff = s_lett * qf_spec
    qdep = s_dep * qd_spec
    qtot = qraff + qdep
    qrec = erec * fv * qrisc
    qres = max(0.0, qrisc - qrec)
    gas = qrisc / eta
    ech = qtot / copc
    epr = qres / copr
    epf = qtot / copf
    cb = ech / 1000.0 * pel + gas / 1000.0 * pg + omb
    ca = (epr + epf) / 1000.0 * pel + oma
    risp = cb - ca
    co2b = gas / 1000.0 * fg + ech / 1000.0 * fel
    co2a = (epr + epf) / 1000.0 * fel
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    be = (ca - ech / 1000.0 * pel - omb) * 1000.0 / gas
    bc = mh790_demo_calcoli()
    assert bc["q_risc_kwh_anno"] == pytest.approx(qrisc)
    assert bc["q_raff_kwh_anno"] == pytest.approx(qraff)
    assert bc["q_dep_raff_kwh_anno"] == pytest.approx(qdep)
    assert bc["q_raff_tot_kwh_anno"] == pytest.approx(qtot)
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
    (4.114,58) ma VAN -67.292,03 oltre la tolleranza
    (11.000): NON_CONVIENTE con payback mai
    raggiunto. Il verdetto guarda la VAN, non il
    solo risparmio positivo."""
    bc = _variante(p_gas_eur_mwh=60)
    assert bc["risparmio_eur_anno"] == pytest.approx(4114.5833333333285)
    assert bc["van"] == pytest.approx(-67292.03203040283)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_gas_40_non_calcolabile():
    """Gas 40 EUR/MWh: risparmio -2.552,08, verdetto
    NON_CALCOLABILE, ma helper calcolabili (flussi
    pieni, VAN negativa, TIR None, payback None)."""
    bc = _variante(p_gas_eur_mwh=40)
    assert bc["risparmio_eur_anno"] == pytest.approx(-2552.0833333333358)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_gas_zero_non_calcolabile():
    """Gas zero: costo baseline 22.833,33 (chiller
    17.833,33 + O&M 5.000, zero gas) contro 38.718,75
    dell'alternativa: risparmio -15.885,42,
    verdetto NON_CALCOLABILE."""
    bc = _variante(p_gas_eur_mwh=0)
    assert bc["valid"] is True
    assert bc["c_base_eur_anno"] == pytest.approx(22833.333333333332)
    assert bc["risparmio_eur_anno"] == pytest.approx(-15885.416666666668)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_senza_recupero_non_conviente():
    """Senza recupero (eta_rec zero): riscaldamento
    residuo 300.000, E_pdc_risc 78.947,37, risparmio
    9.377,74, VAN -12.662,25 oltre la tolleranza
    (11.000), breakeven 61,87, NON_CONVIENTE con
    payback 12 anni. Il recupero dalla
    ventilazione e' decisivo: senza di esso la
    pompa di calore lavora a pieno carico in
    riscaldamento."""
    bc = _variante(eta_rec=0)
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["q_risc_res_kwh_anno"] == pytest.approx(300000.0)
    assert bc["e_pdc_risc_kwh_anno"] == pytest.approx(78947.36842105264)
    assert bc["risparmio_eur_anno"] == pytest.approx(9377.741228070168)
    assert bc["van"] == pytest.approx(-12662.252882083943)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(61.86677631578949)
    assert bc["payback"] == 12
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_recupero_totale_conviente():
    """Recupero totale (eta_rec 1,0): calore
    recuperato 120.000, residuo 180.000, E_pdc_risc
    47.368,42, risparmio 17.272,48, VAN 69.282,42,
    payback 7, breakeven 38,18, CONVIENTE."""
    bc = _variante(eta_rec=1.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(120000.0)
    assert bc["q_risc_res_kwh_anno"] == pytest.approx(180000.0)
    assert bc["e_pdc_risc_kwh_anno"] == pytest.approx(47368.42105263158)
    assert bc["risparmio_eur_anno"] == pytest.approx(17272.478070175435)
    assert bc["van"] == pytest.approx(69282.41584039443)
    assert bc["payback"] == 7
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(38.182565789473685)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_senza_depositi_conviente():
    """Senza raffrescamento depositi (q_dep_raff
    zero): raffrescamento totale 150.000, risparmio
    13.781,25, VAN 33.044,66, payback 8, breakeven
    48,66, CONVIENTE: i depositi in continuo
    contribuiscono, ma le sale lettura da sole
    bastano a tenere il caso conveniente."""
    bc = _variante(q_dep_raff_kwh_m2_anno=0)
    assert bc["q_dep_raff_kwh_anno"] == 0.0
    assert bc["q_raff_tot_kwh_anno"] == pytest.approx(150000.0)
    assert bc["e_chiller_kwh_anno"] == pytest.approx(50000.0)
    assert bc["e_pdc_raff_kwh_anno"] == pytest.approx(46875.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(13781.25)
    assert bc["van"] == pytest.approx(33044.66233867626)
    assert bc["payback"] == 8
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(48.65625)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_senza_raffrescamento_conviente():
    """Senza raffrescamento (q_raff e q_dep_raff
    zero): il chiller sparisce da entrambi i costi,
    risparmio 13.000, VAN 24.935,55, payback 9,
    breakeven 51,00, CONVIENTE."""
    bc = _variante(q_raff_kwh_m2_anno=0, q_dep_raff_kwh_m2_anno=0)
    assert bc["q_raff_tot_kwh_anno"] == 0.0
    assert bc["e_chiller_kwh_anno"] == 0.0
    assert bc["e_pdc_raff_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(13000.0)
    assert bc["van"] == pytest.approx(24935.55449634766)
    assert bc["payback"] == 9
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(51.0)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_alto_marginale_e_non_conviente():
    bc = _variante(capex_eur=150000)
    assert bc["risparmio_eur_anno"] == pytest.approx(14114.583333333328)
    assert bc["van"] == pytest.approx(-3495.4516485969)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"
    bc2 = _variante(capex_eur=170000)
    assert bc2["van"] == pytest.approx(-23495.4516485969)
    assert bc2["payback"] == 13
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex_eur=0)
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(146504.5483514031, rel=1e-6)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(101718.74999999993)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(-1010.9288641102612)
    assert bc2["payback"] == 8
    assert bc2["verdetto"] == "MARGINALE"


def test_variante_el_alto_e_cop_risc_basso():
    """Elettricita' 350 EUR/MWh: risparmio 8.560,42,
    VAN -21.145,80, breakeven 64,32, NON_CONVIENTE.
    COP riscaldamento 2,5: E_pdc_risc 91.200,
    risparmio 6.314,58, VAN -44.456,78, breakeven
    71,06, NON_CONVIENTE."""
    bc = _variante(p_el_eur_mwh=350)
    assert bc["risparmio_eur_anno"] == pytest.approx(8560.416666666664)
    assert bc["van"] == pytest.approx(-21145.802335658267)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(64.31875000000001)
    assert bc["payback"] == 13
    assert bc["verdetto"] == "NON_CONVIENTE"
    bc2 = _variante(cop_risc=2.5)
    assert bc2["e_pdc_risc_kwh_anno"] == pytest.approx(91200.0)
    assert bc2["risparmio_eur_anno"] == pytest.approx(6314.5833333333285)
    assert bc2["van"] == pytest.approx(-44456.78434640552)
    assert bc2["breakeven_gas_eur_mwh"] == pytest.approx(71.05625)
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_monotonia_prezzo_gas_crescente():
    base = mh790_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas_eur_mwh=91)["risparmio_eur_anno"]
    basso = _variante(p_gas_eur_mwh=89)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(333.3333333333333)
    assert base - basso == pytest.approx(333.3333333333333)


def test_monotonia_recupero_crescente_con_tetto():
    """Il risparmio cresce con il recupero finche'
    il calore recuperato non copre tutto il
    riscaldamento; oltre, il residuo e' zero e il
    risparmio si ferma."""
    assert _variante(eta_rec=0)["risparmio_eur_anno"] < \
        mh790_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(eta_rec=1.0)["risparmio_eur_anno"] > \
        mh790_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(f_vent=1.0, eta_rec=1.0)["q_rec_kwh_anno"] == \
        pytest.approx(300000.0)
    assert _variante(f_vent=1.0, eta_rec=1.0)["q_risc_res_kwh_anno"] == 0.0


def test_demo_deterministica_due_chiamate():
    a = mh790_demo_calcoli()
    b = mh790_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh790_demo().keys()) == {
        "superficie_lettura_m2", "superficie_depositi_m2",
        "q_risc_kwh_m2_anno", "q_raff_kwh_m2_anno",
        "q_dep_raff_kwh_m2_anno", "f_vent", "eta_rec",
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
    for kw in ({"superficie_lettura_m2": 0},
               {"superficie_lettura_m2": -10},
               {"superficie_depositi_m2": 0},
               {"superficie_depositi_m2": -10},
               {"q_risc_kwh_m2_anno": -0.1},
               {"q_raff_kwh_m2_anno": -0.1},
               {"q_dep_raff_kwh_m2_anno": -0.1},
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
        assert mh790_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"superficie_lettura_m2": "3000"},
               {"superficie_depositi_m2": "800"},
               {"superficie_lettura_m2": float("nan")},
               {"p_gas_eur_mwh": float("inf")},
               {"capex_eur": True},
               {"q_risc_kwh_m2_anno": "100"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh790_valida(**d)["valido"] is False


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    """Differenza chiave: risparmio <= 0 NON solleva
    negli helper (resta calcolabile con flussi, VAN,
    TIR e payback), ma il verdetto e' NON_CALCOLABILE
    e la UI salta KPI, grafico, tabella e CSV."""
    for kw in ({"p_gas_eur_mwh": 0},
               {"p_gas_eur_mwh": 47.65625000000001},
               {"p_gas_eur_mwh": 40}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] <= 0.0
        assert bc["verdetto"] == "NON_CALCOLABILE"
        assert bc["flussi"]


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh790_demo_calcoli()
    testo = mh790_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_gas_eur_mwh" in testo
    assert "co2_evitata_t_anno" in testo
    assert "q_raff_kwh_anno" in testo
    assert "q_dep_raff_kwh_anno" in testo
    assert "q_raff_tot_kwh_anno" in testo
    assert "q_risc_res_kwh_anno" in testo
    assert "e_chiller_kwh_anno" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh790_demo_calcoli()
    testo = mh790_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"q_risc_kwh_anno;{bc['q_risc_kwh_anno']}" in testo
    assert f"gas_base_kwh_anno;{bc['gas_base_kwh_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh790_demo_calcoli()
    testo = mh790_csv(bc, _demo_kwargs())
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
    return ["mh" + "78" + "9", "st" + "78" + "9",
            "tab" + "78" + "9", "tab" + "78" + "8"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w791_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w791_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab790:")


def test_registry_chain_tail_and_count():
    """Registry della nuova tab: il frammento UI apre la tab
    numero 790 (la coda della catena termina con la nuova tab
    e il conteggio atteso delle tab e' 790)."""
    src = _leggi("w791_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 790
    assert src.count("with tab790:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w791_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w791_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st790_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) >= 24
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w791_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 2
    # Entrambe le guard (input degenere e risparmio <= 0)
    # stanno prima di KPI / grafico / tabella / CSV.
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w791_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def790[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w791_ui.py")
        usate = set(re.findall(r'_def790\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 21
        assert usate <= set(mh790_demo().keys())
