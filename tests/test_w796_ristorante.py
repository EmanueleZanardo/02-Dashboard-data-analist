"""Test tab796 "Ristorante: pompa di calore +
recupero calore celle frigo su ACS batte
caldaia a gas + chiller?"
(titolo completo nel frammento UI).
Contenuto pronto da scrivere in repo come test
della tab ristorante.

Business case deterministico di un ristorante
guidato dai m2 di sala per riscaldamento e
raffrescamento e dai coperti annui per ACS e
carico termico delle celle frigo, sempre
accese. Riscaldamento sala Q_risc = S x q_risc
kWh_th/anno; raffrescamento sala Q_raff =
S x q_raff kWh_c/anno; ACS Q_acs = N x q_acs
kWh_th/anno (N coperti/anno, q_acs
kWh_th/coperto); carico termico celle frigo
Q_frigo = N x q_frigo kWh_th/anno;
elettricita' frigo E_frigo = Q_frigo /
COP_frigo kWh_e/anno (uguale in baseline e
alternativa); calore di scarto celle
Q_scartato = Q_frigo + E_frigo kWh_th/anno;
calore recuperato SOLO sull'ACS Q_rec =
eta_rec x Q_scartato kWh_th/anno (puo'
superare Q_acs, perche' lo scarto e'
indipendente dall'ACS); ACS residua
Q_acs_res = max(0, Q_acs - Q_rec)
kWh_th/anno (l'eccesso viene sprecato, senza
export); gas baseline G_base = (Q_risc +
Q_acs) / eta_caldaia kWh/anno (cucina a gas
ESCLUSA: invariata in entrambi gli scenari);
elettricita' chiller E_chiller = Q_raff /
COP_chiller kWh_e/anno; elettricita' pompa di
calore in riscaldamento sala E_pdc_risc =
Q_risc / COP_risc kWh_e/anno; in
raffrescamento sala E_pdc_raff = Q_raff /
COP_raff kWh_e/anno; in ACS residua
E_pdc_acs = Q_acs_res / COP_acs kWh_e/anno;
C_base = (E_chiller + E_frigo) / 1000 x p_el
+ G_base / 1000 x p_gas + O&M_base EUR/anno;
C_alt = (E_pdc_risc + E_pdc_raff + E_pdc_acs
+ E_frigo) / 1000 x p_el + O&M_alt EUR/anno
(prezzi EUR/MWh, energie kWh: / 1000 esatto);
risparmio = C_base - C_alt; CO2_base =
G_base / 1000 x f_gas + (E_chiller + E_frigo)
/ 1000 x f_el t/anno; CO2_alt = (E_pdc_risc
+ E_pdc_raff + E_pdc_acs + E_frigo) / 1000 x
f_el t/anno; CO2_evitata = CO2_base - CO2_alt;
flussi [-CAPEX, risparmio x vita]; VAN, TIR,
payback (primo anno con cumulato >= 0);
breakeven gas p_gas_be = (C_alt - (E_chiller
+ E_frigo) / 1000 x p_el - O&M_base) x 1000 /
G_base EUR/MWh, None se G_base <= 0 o
numeratore < 0, SOGLIA MINIMA quando esiste.
Verdetto: NON_CALCOLABILE se risparmio <= 0
(guard degenere: UI salta KPI, grafico,
tabella e CSV); altrimenti CONVIENTE se VAN >
0, MARGINALE se VAN negativa entro tolleranza
% del CAPEX, NON_CONVIENTE se VAN negativa
oltre la tolleranza. Distinzione esplicita:
distinto dal supermercato (superficie di
vendita, banchi frigo, recupero sul
riscaldamento), dall'ospedale (reparti 24h,
ventilazione aria esausta, ACS posti letto),
dall'albergo (pernottamento, ACS docce
ospiti), dalla scuola (aule + mensa, chiusure
stagionali), dalla piscina (vasca riscaldata)
e dalla palestra (docce utenti): qui driver =
m2 di sala per riscaldamento/raffrescamento +
coperti annui per ACS/carico frigo; celle
frigo sempre accese; recupero SOLO da calore
di scarto delle celle frigo SOLO su ACS;
cucina a gas esclusa dal confronto.

Demo (ristorante): 400 m2 di sala a 140
kWh_th/m2/anno di riscaldamento e 100
kWh_c/m2/anno di raffrescamento, 40.000
coperti/anno a 2,5 kWh_th/coperto di ACS e
1,2 kWh_th/coperto di carico termico frigo,
recupero 0,30, caldaia 0,90, chiller COP 3,0,
frigo COP 2,2, pompa di calore COP
riscaldamento 3,6, COP raffrescamento 3,2 e
COP ACS 3,0, gas 90, el 250 EUR/MWh, O&M base
8.000, alt 10.000, CAPEX 25.000, WACC 5 %,
vita 12, f_gas 0,20, f_el 0,35, tolleranza 10 %
del CAPEX. Valori calcolati eseguendo
mh796_demo_calcoli(): Q_risc 56.000, Q_raff
40.000, Q_acs 100.000, Q_frigo 48.000,
E_frigo 21.818,181818181816, Q_scartato
69.818,18181818182, Q_rec 20.945,454545454548,
Q_acs_res 79.054,54545454546, G_base
173.333,33333333334, E_chiller
13.333,333333333334, E_pdc_risc
15.555,555555555555, E_pdc_raff 12.500,
E_pdc_acs 26.351,515151515152, C_base
32.387,878787878788, C_alt 29.056,31313131313,
risparmio 3.331,5656565656573, CO2_base
46,96969696969697, CO2_alt 26,678838383838382,
CO2_evitata 20,290858585858587, VAN
4.528,504757492208, TIR 8,082477888842897 %,
payback 8, breakeven gas 70,7794289044289,
verdetto CONVIENTE.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w797_helpers import (
    demo_calcoli,
    mh796_breakeven_gas,
    mh796_c_alt,
    mh796_c_base,
    mh796_calcola,
    mh796_co2_alt,
    mh796_co2_base,
    mh796_co2_evitata,
    mh796_cop,
    mh796_csv,
    mh796_demo,
    mh796_demo_calcoli,
    mh796_e_chiller,
    mh796_e_frigo,
    mh796_e_pdc_acs,
    mh796_e_pdc_raff,
    mh796_e_pdc_risc,
    mh796_eta,
    mh796_eta_rec,
    mh796_flussi,
    mh796_gas,
    mh796_int_pos,
    mh796_num,
    mh796_nneg,
    mh796_payback,
    mh796_pct_tolleranza,
    mh796_pct_wacc,
    mh796_pos,
    mh796_q_acs,
    mh796_q_acs_res,
    mh796_q_frigo,
    mh796_q_raff,
    mh796_q_rec,
    mh796_q_risc,
    mh796_q_scartato,
    mh796_risparmio,
    mh796_tir,
    mh796_valida,
    mh796_van,
    mh796_verdetto,
)

_DEMO = {
    "q_risc_kwh_anno": 56000.0,
    "q_raff_kwh_anno": 40000.0,
    "q_acs_kwh_anno": 100000.0,
    "q_frigo_kwh_anno": 48000.0,
    "e_frigo_kwh_anno": 21818.181818181816,
    "q_scartato_kwh_anno": 69818.18181818182,
    "q_rec_kwh_anno": 20945.454545454548,
    "q_acs_res_kwh_anno": 79054.54545454546,
    "gas_base_kwh_anno": 173333.33333333334,
    "e_chiller_kwh_anno": 13333.333333333334,
    "e_pdc_risc_kwh_anno": 15555.555555555555,
    "e_pdc_raff_kwh_anno": 12500.0,
    "e_pdc_acs_kwh_anno": 26351.515151515152,
    "c_base_eur_anno": 32387.878787878788,
    "c_alt_eur_anno": 29056.31313131313,
    "risparmio_eur_anno": 3331.5656565656573,
    "co2_base_t_anno": 46.96969696969697,
    "co2_alt_t_anno": 26.678838383838382,
    "co2_evitata_t_anno": 20.290858585858587,
    "van": 4528.504757492208,
    "tir": 8.082477888842897,
    "breakeven_gas_eur_mwh": 70.7794289044289,
}


def _demo_kwargs():
    return dict(mh796_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh796_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh796_num(3, "x") == 3.0
    assert mh796_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh796_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh796_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh796_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh796_pos(0, "x")
    with pytest.raises(ValueError):
        mh796_pos(-1, "x")
    assert mh796_pos(0.5, "x") == 0.5


def test_cop_maggiore_di_uno():
    assert mh796_cop(3.6, "x") == 3.6
    assert mh796_cop(1.01, "x") == 1.01
    with pytest.raises(ValueError):
        mh796_cop(1.0, "x")
    with pytest.raises(ValueError):
        mh796_cop(0.5, "x")
    with pytest.raises(ValueError):
        mh796_cop(0, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh796_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh796_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh796_int_pos(0, "x")


def test_eta_limiti():
    assert mh796_eta(1.0, "x") == 1.0
    assert mh796_eta(0.9, "x") == 0.9
    with pytest.raises(ValueError):
        mh796_eta(0, "x")
    with pytest.raises(ValueError):
        mh796_eta(1.01, "x")


def test_eta_rec_limiti():
    assert mh796_eta_rec(0.0, "x") == 0.0
    assert mh796_eta_rec(1.0, "x") == 1.0
    assert mh796_eta_rec(0.30, "x") == 0.30
    with pytest.raises(ValueError):
        mh796_eta_rec(-0.1, "x")
    with pytest.raises(ValueError):
        mh796_eta_rec(1.01, "x")


def test_pct_wacc_limiti():
    assert mh796_pct_wacc(0, "x") == 0.0
    assert mh796_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh796_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh796_pct_tolleranza(0, "x") == 0.0
    assert mh796_pct_tolleranza(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh796_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh796_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_q_risc_q_raff_q_acs_q_frigo():
    assert mh796_q_risc(400, 140) == 56000.0
    assert mh796_q_risc(400, 0) == 0.0
    assert mh796_q_raff(400, 100) == 40000.0
    assert mh796_q_raff(400, 0) == 0.0
    assert mh796_q_acs(40000, 2.5) == 100000.0
    assert mh796_q_acs(40000, 0) == 0.0
    assert mh796_q_frigo(40000, 1.2) == 48000.0
    assert mh796_q_frigo(40000, 0) == 0.0
    with pytest.raises(ValueError):
        mh796_q_risc(0, 140)
    with pytest.raises(ValueError):
        mh796_q_risc(400, -10)
    with pytest.raises(ValueError):
        mh796_q_raff(0, 100)
    with pytest.raises(ValueError):
        mh796_q_raff(400, -10)
    with pytest.raises(ValueError):
        mh796_q_acs(0, 2.5)
    with pytest.raises(ValueError):
        mh796_q_acs(40000, -0.1)
    with pytest.raises(ValueError):
        mh796_q_frigo(0, 1.2)
    with pytest.raises(ValueError):
        mh796_q_frigo(40000, -0.1)


def test_e_frigo_e_scartato():
    assert mh796_e_frigo(48000, 2.2) == 21818.181818181816
    assert mh796_e_frigo(0, 2.2) == 0.0
    assert mh796_q_scartato(48000, 21818.181818181816) == pytest.approx(69818.18181818182)
    assert mh796_q_scartato(0, 0) == 0.0
    assert mh796_q_scartato(48000, 0) == 48000.0
    with pytest.raises(ValueError):
        mh796_e_frigo(48000, 1.0)
    with pytest.raises(ValueError):
        mh796_q_scartato(48000, -1)


def test_q_rec_solo_scartato_celle_su_acs():
    assert mh796_q_rec(69818.18181818182, 0.30) == pytest.approx(20945.454545454548)
    assert mh796_q_rec(69818.18181818182, 0) == 0.0
    assert mh796_q_rec(69818.18181818182, 1.0) == pytest.approx(69818.18181818182)
    assert mh796_q_rec(0, 0.30) == 0.0
    with pytest.raises(ValueError):
        mh796_q_rec(69818.18181818182, 1.01)
    with pytest.raises(ValueError):
        mh796_q_rec(69818.18181818182, -0.1)
    with pytest.raises(ValueError):
        mh796_q_rec(-1, 0.30)


def test_q_acs_res_con_troncamento_a_zero():
    assert mh796_q_acs_res(100000, 20945.454545454548) == pytest.approx(79054.54545454546)
    assert mh796_q_acs_res(100000, 100000.0) == 0.0
    assert mh796_q_acs_res(100000, 120000.0) == 0.0
    with pytest.raises(ValueError):
        mh796_q_acs_res(100000, -1)


def test_gas_e_chiller():
    assert mh796_gas(156000, 0.9) == pytest.approx(173333.33333333334)
    assert mh796_gas(0, 0.9) == 0.0
    assert mh796_e_chiller(40000, 3.0) == pytest.approx(13333.333333333334)
    assert mh796_e_chiller(0, 3.0) == 0.0
    with pytest.raises(ValueError):
        mh796_gas(156000, 0)
    with pytest.raises(ValueError):
        mh796_gas(156000, 1.01)
    with pytest.raises(ValueError):
        mh796_e_chiller(40000, 1.0)


def test_e_pdc_risc_raff_acs():
    assert mh796_e_pdc_risc(56000, 3.6) == pytest.approx(15555.555555555555)
    assert mh796_e_pdc_risc(0, 3.6) == 0.0
    assert mh796_e_pdc_raff(40000, 3.2) == 12500.0
    assert mh796_e_pdc_raff(0, 3.2) == 0.0
    assert mh796_e_pdc_acs(79054.54545454546, 3.0) == pytest.approx(26351.515151515152)
    assert mh796_e_pdc_acs(0, 3.0) == 0.0
    with pytest.raises(ValueError):
        mh796_e_pdc_risc(56000, 1.0)
    with pytest.raises(ValueError):
        mh796_e_pdc_raff(40000, 0.5)
    with pytest.raises(ValueError):
        mh796_e_pdc_acs(79054.54545454546, 1.0)


def test_c_base_c_alt_scomposizione():
    assert mh796_c_base(13333.333333333334, 21818.181818181816, 250,
                        173333.33333333334, 90,
                        8000) == pytest.approx(32387.878787878788)
    assert mh796_c_base(13333.333333333334, 21818.181818181816, 250,
                        173333.33333333334, 0,
                        8000) == pytest.approx(16787.878787878788)
    assert mh796_c_alt(15555.555555555555, 12500.0, 26351.515151515152,
                       21818.181818181816, 250,
                       10000) == pytest.approx(29056.31313131313)
    assert mh796_c_alt(0, 0, 0, 0, 250, 10000) == pytest.approx(10000.0)
    with pytest.raises(ValueError):
        mh796_c_base(13333.333333333334, 21818.181818181816, 250,
                     173333.33333333334, -1, 8000)
    with pytest.raises(ValueError):
        mh796_c_alt(15555.555555555555, 12500.0, 26351.515151515152,
                    21818.181818181816, 250, -1)


def test_risparmio_segno():
    assert mh796_risparmio(32387.878787878788, 29056.31313131313) == pytest.approx(3331.5656565656573)
    assert mh796_risparmio(29056.31313131313, 29056.31313131313) == 0.0
    assert mh796_risparmio(27187.878787878788, 29056.31313131313) == pytest.approx(-1868.4343434343427)


def test_co2_base_alt_evitata():
    assert mh796_co2_base(173333.33333333334, 0.20, 13333.333333333334,
                          21818.181818181816,
                          0.35) == pytest.approx(46.96969696969697)
    assert mh796_co2_alt(15555.555555555555, 12500.0, 26351.515151515152,
                         21818.181818181816,
                         0.35) == pytest.approx(26.678838383838382)
    assert mh796_co2_evitata(173333.33333333334, 0.20,
                             13333.333333333334, 21818.181818181816,
                             15555.555555555555, 12500.0,
                             26351.515151515152,
                             0.35) == pytest.approx(20.290858585858587)
    assert mh796_co2_base(0, 0.20, 0, 0, 0.35) == pytest.approx(0.0)
    assert mh796_co2_alt(0, 0, 0, 0, 0.35) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh796_co2_base(173333.33333333334, -0.10, 13333.333333333334,
                       21818.181818181816, 0.35)
    with pytest.raises(ValueError):
        mh796_co2_alt(15555.555555555555, 12500.0, 26351.515151515152,
                      21818.181818181816, -0.10)


def test_breakeven_gas_demo_e_varianti():
    assert mh796_breakeven_gas(29056.31313131313, 13333.333333333334,
                               21818.181818181816, 250, 8000,
                               173333.33333333334) == \
        pytest.approx(70.7794289044289)
    assert mh796_breakeven_gas(30801.767676767675, 13333.333333333334,
                               21818.181818181816, 250, 8000,
                               173333.33333333334) == \
        pytest.approx(80.84935897435895)
    assert mh796_breakeven_gas(24983.58585858586, 13333.333333333334,
                               21818.181818181816, 250, 8000,
                               173333.33333333334) == \
        pytest.approx(47.282925407925404)
    assert mh796_breakeven_gas(29056.31313131313, 13333.333333333334,
                               21818.181818181816, 250, 8000, 0) is None
    assert mh796_breakeven_gas(200, 13333.333333333334,
                               21818.181818181816, 250, 8000,
                               173333.33333333334) is None
    with pytest.raises(ValueError):
        mh796_breakeven_gas(29056.31313131313, 13333.333333333334,
                            21818.181818181816, 250, 8000, -1)


def test_breakeven_verifica_pareggio():
    bc = _variante(p_gas_eur_mwh=70.7794289044289)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    demo = mh796_demo_calcoli()
    assert (demo["c_alt_eur_anno"]
            - (demo["e_chiller_kwh_anno"] + demo["e_frigo_kwh_anno"])
            / 1000.0
            * demo["p_el_eur_mwh"]
            - demo["om_base_eur_anno"]) * 1000.0 / demo["gas_base_kwh_anno"] == \
        pytest.approx(demo["breakeven_gas_eur_mwh"])


def test_breakeven_soglia_minima():
    be = mh796_demo_calcoli()["breakeven_gas_eur_mwh"]
    assert _variante(p_gas_eur_mwh=be + 1)[
        "c_alt_eur_anno"] < _variante(p_gas_eur_mwh=be + 1)[
        "c_base_eur_anno"]
    assert _variante(p_gas_eur_mwh=be - 1)[
        "c_alt_eur_anno"] > _variante(p_gas_eur_mwh=be - 1)[
        "c_base_eur_anno"]


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh796_flussi(25000, 3331.5656565656573, 12)
    assert len(fl) == 13
    assert fl[0] == -25000
    assert all(f == 3331.5656565656573 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh796_demo_calcoli()
    assert bc["van"] == pytest.approx(4528.504757492208)
    assert mh796_van([-25000] + [3331.5656565656573] * 12,
                     0) == pytest.approx(14978.787878787887)
    assert mh796_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh796_demo_calcoli()
    assert bc["tir"] == pytest.approx(8.082477888842897)
    assert mh796_tir([-25000] + [3331.5656565656573] * 12) == \
        pytest.approx(0.08082477888842897)
    tir = mh796_tir([-25000] + [3331.5656565656573] * 12)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-25000] + [3331.5656565656573] * 12))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh796_payback([-25000] + [3331.5656565656573] * 12) == 8
    assert mh796_payback([-25000] + [-1000.0] * 12) is None
    assert mh796_payback([0] + [3331.5656565656573] * 12) == 0
    assert mh796_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh796_verdetto(3331.5656565656573, 4528.504757492208, 25000,
                          10.0) == "CONVIENTE"
    assert mh796_verdetto(3331.5656565656573, 0.0, 25000, 10.0) == "MARGINALE"
    assert mh796_verdetto(3331.5656565656573, -2500.0, 25000, 10.0) == "MARGINALE"
    assert mh796_verdetto(3331.5656565656573, -2500.01, 25000, 10.0) == "NON_CONVIENTE"
    assert mh796_verdetto(3331.5656565656573, -10941.90, 25000, 10.0) == "NON_CONVIENTE"
    assert mh796_verdetto(0.0, 4528.504757492208, 25000,
                          10.0) == "NON_CALCOLABILE"
    assert mh796_verdetto(-1868.4343434343427, -41560.40, 25000,
                          10.0) == "NON_CALCOLABILE"
    assert mh796_verdetto(None, 4528.504757492208, 25000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh796_verdetto(float("nan"), 4528.50, 25000, 10.0)
    with pytest.raises(ValueError):
        mh796_verdetto(3331.5656565656573, 4528.50, -1, 10.0)
    with pytest.raises(ValueError):
        mh796_verdetto(3331.5656565656573, 4528.50, 25000, 100.1)


def test_valida_demo_ok():
    v = mh796_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("superficie_sala_m2", "400"),
                       ("superficie_sala_m2", float("nan")),
                       ("superficie_sala_m2", float("inf")),
                       ("superficie_sala_m2", True),
                       ("p_gas_eur_mwh", None),
                       ("q_risc_kwh_m2_anno", "140")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh796_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("superficie_sala_m2", 0),
                          ("superficie_sala_m2", -10),
                          ("q_risc_kwh_m2_anno", -0.1),
                          ("q_raff_kwh_m2_anno", -0.1),
                          ("coperti_annui", 0),
                          ("coperti_annui", -10),
                          ("q_acs_kwh_th_coperto", -0.1),
                          ("q_frigo_kwh_th_coperto", -0.1),
                          ("eta_rec", -0.1),
                          ("eta_rec", 1.01),
                          ("eta_caldaia", 0),
                          ("eta_caldaia", 1.01),
                          ("cop_chiller", 1.0),
                          ("cop_chiller", 0.5),
                          ("cop_frigo", 1.0),
                          ("cop_frigo", 0.5),
                          ("cop_risc", 1.0),
                          ("cop_raff", 1.0),
                          ("cop_acs", 1.0),
                          ("cop_acs", 0.5),
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
        assert mh796_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"q_risc_kwh_m2_anno": 0,
              "q_raff_kwh_m2_anno": 0,
              "q_acs_kwh_th_coperto": 0,
              "q_frigo_kwh_th_coperto": 0,
              "eta_rec": 0,
              "p_gas_eur_mwh": 0,
              "p_el_eur_mwh": 0,
              "om_base_eur_anno": 0, "om_alt_eur_anno": 0,
              "capex_eur": 0, "wacc_pct": 0,
              "f_gas_t_per_mwh": 0, "f_el_t_per_mwh": 0,
              "tolleranza_pct": 0})
    assert mh796_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["eta_rec"] = 1
    d["q_risc_kwh_m2_anno"] = 140
    assert mh796_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh796_demo()
    assert d["superficie_sala_m2"] == 400
    assert d["q_risc_kwh_m2_anno"] == 140
    assert d["q_raff_kwh_m2_anno"] == 100
    assert d["coperti_annui"] == 40000
    assert d["q_acs_kwh_th_coperto"] == 2.5
    assert d["q_frigo_kwh_th_coperto"] == 1.2
    assert d["eta_rec"] == 0.30
    assert d["eta_caldaia"] == 0.90
    assert d["cop_chiller"] == 3.0
    assert d["cop_frigo"] == 2.2
    assert d["cop_risc"] == 3.6
    assert d["cop_raff"] == 3.2
    assert d["cop_acs"] == 3.0
    assert d["p_gas_eur_mwh"] == 90
    assert d["p_el_eur_mwh"] == 250
    assert d["om_base_eur_anno"] == 8000
    assert d["om_alt_eur_anno"] == 10000
    assert d["capex_eur"] == 25000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 12
    assert d["f_gas_t_per_mwh"] == 0.20
    assert d["f_el_t_per_mwh"] == 0.35
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    bc = mh796_demo_calcoli()
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
    bc = mh796_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(32387.878787878788)
    assert bc["c_alt_eur_anno"] == pytest.approx(29056.31313131313)
    assert bc["risparmio_eur_anno"] == pytest.approx(3331.5656565656573)
    assert bc["co2_base_t_anno"] == pytest.approx(46.96969696969697)
    assert bc["co2_alt_t_anno"] == pytest.approx(26.678838383838382)
    assert bc["co2_evitata_t_anno"] == pytest.approx(20.290858585858587)
    assert bc["gas_base_kwh_anno"] == pytest.approx(173333.33333333334)


def test_demo_flussi_e_cumulato():
    bc = mh796_demo_calcoli()
    assert bc["flussi"][0] == -25000
    assert len(bc["flussi"]) == 13
    assert all(f == pytest.approx(3331.5656565656573) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -25000
    assert righe.iloc[4]["Cumulato (EUR)"] == pytest.approx(-11673.737373737371)
    assert righe.iloc[7]["Cumulato (EUR)"] == pytest.approx(-1679.0404040403992)
    assert righe.iloc[8]["Cumulato (EUR)"] == pytest.approx(1652.525252525258)
    assert righe.iloc[12]["Cumulato (EUR)"] == pytest.approx(14978.787878787887)


def test_demo_tabella_righe():
    bc = mh796_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Riscaldamento sala (kWh_th/anno)"] == pytest.approx(56000.0)
    assert mappa["Raffrescamento sala (kWh_c/anno)"] == pytest.approx(40000.0)
    assert mappa["ACS ristorante (kWh_th/anno)"] == pytest.approx(100000.0)
    assert mappa["Carico termico frigo (kWh_th/anno)"] == pytest.approx(48000.0)
    assert mappa["Elettricita' frigo (kWh_e/anno)"] == pytest.approx(21818.181818181816)
    assert mappa["Calore di scarto celle frigo (kWh_th/anno)"] == pytest.approx(69818.18181818182)
    assert mappa["Calore recuperato celle frigo su ACS (kWh_th/anno)"] == pytest.approx(20945.454545454548)
    assert mappa["ACS residua (kWh_th/anno)"] == pytest.approx(79054.54545454546)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(173333.33333333334)
    assert mappa["Elettricita' chiller (kWh_e/anno)"] == pytest.approx(13333.333333333334)
    assert mappa["Elettricita' pompa di calore riscaldamento (kWh_e/anno)"] == pytest.approx(15555.555555555555)
    assert mappa["Elettricita' pompa di calore raffrescamento (kWh_e/anno)"] == pytest.approx(12500.0)
    assert mappa["Elettricita' pompa di calore ACS (kWh_e/anno)"] == pytest.approx(26351.515151515152)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(32387.878787878788)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(29056.31313131313)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(3331.5656565656573)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(20.290858585858587)
    assert mappa["Payback (anni)"] == 8
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] == \
        pytest.approx(70.7794289044289)


def test_demo_coerenza_interna():
    bc = mh796_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["q_risc_kwh_anno"] == pytest.approx(
        bc["superficie_sala_m2"] * bc["q_risc_kwh_m2_anno"])
    assert bc["q_raff_kwh_anno"] == pytest.approx(
        bc["superficie_sala_m2"] * bc["q_raff_kwh_m2_anno"])
    assert bc["q_acs_kwh_anno"] == pytest.approx(
        bc["coperti_annui"] * bc["q_acs_kwh_th_coperto"])
    assert bc["q_frigo_kwh_anno"] == pytest.approx(
        bc["coperti_annui"] * bc["q_frigo_kwh_th_coperto"])
    assert bc["e_frigo_kwh_anno"] == pytest.approx(
        bc["q_frigo_kwh_anno"] / bc["cop_frigo"])
    assert bc["q_scartato_kwh_anno"] == pytest.approx(
        bc["q_frigo_kwh_anno"] + bc["e_frigo_kwh_anno"])
    assert bc["q_rec_kwh_anno"] == pytest.approx(
        bc["eta_rec"] * bc["q_scartato_kwh_anno"])
    assert bc["q_acs_res_kwh_anno"] == pytest.approx(
        max(0.0, bc["q_acs_kwh_anno"] - bc["q_rec_kwh_anno"]))
    assert bc["gas_base_kwh_anno"] == pytest.approx(
        (bc["q_risc_kwh_anno"] + bc["q_acs_kwh_anno"])
        / bc["eta_caldaia"])
    assert bc["e_chiller_kwh_anno"] == pytest.approx(
        bc["q_raff_kwh_anno"] / bc["cop_chiller"])
    assert bc["e_pdc_risc_kwh_anno"] == pytest.approx(
        bc["q_risc_kwh_anno"] / bc["cop_risc"])
    assert bc["e_pdc_raff_kwh_anno"] == pytest.approx(
        bc["q_raff_kwh_anno"] / bc["cop_raff"])
    assert bc["e_pdc_acs_kwh_anno"] == pytest.approx(
        bc["q_acs_res_kwh_anno"] / bc["cop_acs"])
    assert bc["co2_evitata_t_anno"] == pytest.approx(
        bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])
    assert bc["c_base_eur_anno"] == pytest.approx(
        (bc["e_chiller_kwh_anno"] + bc["e_frigo_kwh_anno"])
        / 1000.0 * bc["p_el_eur_mwh"]
        + bc["gas_base_kwh_anno"] / 1000.0 * bc["p_gas_eur_mwh"]
        + bc["om_base_eur_anno"])
    assert bc["c_alt_eur_anno"] == pytest.approx(
        (bc["e_pdc_risc_kwh_anno"] + bc["e_pdc_raff_kwh_anno"]
         + bc["e_pdc_acs_kwh_anno"] + bc["e_frigo_kwh_anno"])
        / 1000.0 * bc["p_el_eur_mwh"]
        + bc["om_alt_eur_anno"])


def test_demo_contro_riconteggio_indipendente():
    s_sala = 400
    qr_spec, qf_spec = 140, 100
    n_cop = 40000
    qa_spec, qfr_spec = 2.5, 1.2
    erec = 0.30
    eta, copc, copfr, copr, copf, copa = 0.90, 3.0, 2.2, 3.6, 3.2, 3.0
    pg, pel, omb, oma, cx = 90, 250, 8000, 10000, 25000
    fg, fel, wacc, vita = 0.20, 0.35, 5.0, 12
    qrisc = s_sala * qr_spec
    qraff = s_sala * qf_spec
    qacs = n_cop * qa_spec
    qfrigo = n_cop * qfr_spec
    efrigo = qfrigo / copfr
    qscart = qfrigo + efrigo
    qrec = erec * qscart
    qares = max(0.0, qacs - qrec)
    gas = (qrisc + qacs) / eta
    ech = qraff / copc
    epr = qrisc / copr
    epf = qraff / copf
    epa = qares / copa
    cb = (ech + efrigo) / 1000.0 * pel + gas / 1000.0 * pg + omb
    ca = (epr + epf + epa + efrigo) / 1000.0 * pel + oma
    risp = cb - ca
    co2b = gas / 1000.0 * fg + (ech + efrigo) / 1000.0 * fel
    co2a = (epr + epf + epa + efrigo) / 1000.0 * fel
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    be = (ca - (ech + efrigo) / 1000.0 * pel - omb) * 1000.0 / gas
    bc = mh796_demo_calcoli()
    assert bc["q_risc_kwh_anno"] == pytest.approx(qrisc)
    assert bc["q_raff_kwh_anno"] == pytest.approx(qraff)
    assert bc["q_acs_kwh_anno"] == pytest.approx(qacs)
    assert bc["q_frigo_kwh_anno"] == pytest.approx(qfrigo)
    assert bc["e_frigo_kwh_anno"] == pytest.approx(efrigo)
    assert bc["q_scartato_kwh_anno"] == pytest.approx(qscart)
    assert bc["q_rec_kwh_anno"] == pytest.approx(qrec)
    assert bc["q_acs_res_kwh_anno"] == pytest.approx(qares)
    assert bc["gas_base_kwh_anno"] == pytest.approx(gas)
    assert bc["e_chiller_kwh_anno"] == pytest.approx(ech)
    assert bc["e_pdc_risc_kwh_anno"] == pytest.approx(epr)
    assert bc["e_pdc_raff_kwh_anno"] == pytest.approx(epf)
    assert bc["e_pdc_acs_kwh_anno"] == pytest.approx(epa)
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
    assert bc["risparmio_eur_anno"] == pytest.approx(-1868.4343434343427)
    assert bc["van"] == pytest.approx(-41560.40375204159)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_gas_30_non_calcolabile():
    bc = _variante(p_gas_eur_mwh=30)
    assert bc["risparmio_eur_anno"] == pytest.approx(-7068.434343434343)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_gas_zero_non_calcolabile():
    bc = _variante(p_gas_eur_mwh=0)
    assert bc["valid"] is True
    assert bc["c_base_eur_anno"] == pytest.approx(16787.878787878788)
    assert bc["risparmio_eur_anno"] == pytest.approx(-12268.434343434343)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_senza_recupero_non_conviente():
    bc = _variante(eta_rec=0)
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["q_acs_res_kwh_anno"] == pytest.approx(100000.0)
    assert bc["e_pdc_acs_kwh_anno"] == pytest.approx(33333.333333333336)
    assert bc["risparmio_eur_anno"] == pytest.approx(1586.1111111111131)
    assert bc["van"] == pytest.approx(-10941.89809885479)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(80.84935897435895)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_recupero_totale_conviente():
    bc = _variante(eta_rec=1.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(69818.18181818182)
    assert bc["q_acs_res_kwh_anno"] == pytest.approx(30181.818181818177)
    assert bc["e_pdc_acs_kwh_anno"] == pytest.approx(10060.606060606058)
    assert bc["risparmio_eur_anno"] == pytest.approx(7404.292929292929)
    assert bc["van"] == pytest.approx(40626.11142230188)
    assert bc["payback"] == 4
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(47.282925407925404)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_senza_raffrescamento_conviente():
    bc = _variante(q_raff_kwh_m2_anno=0)
    assert bc["q_raff_kwh_anno"] == 0.0
    assert bc["e_chiller_kwh_anno"] == 0.0
    assert bc["e_pdc_raff_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(3123.232323232325)
    assert bc["van"] == pytest.approx(2681.9939998987174)
    assert bc["payback"] == 9
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(71.98135198135196)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_alto_marginale_e_non_conviente():
    bc = _variante(capex_eur=30000)
    assert bc["risparmio_eur_anno"] == pytest.approx(3331.5656565656573)
    assert bc["van"] == pytest.approx(-471.4952425077911)
    assert bc["payback"] == 10
    assert bc["verdetto"] == "MARGINALE"
    bc2 = _variante(capex_eur=40000)
    assert bc2["van"] == pytest.approx(-10471.495242507799)
    assert bc2["payback"] is None
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex_eur=0)
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(29528.504757492206, rel=1e-6)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(14978.787878787887)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=8)
    assert len(bc2["flussi"]) == 9
    assert bc2["van"] == pytest.approx(-3467.3823396185358)
    assert bc2["payback"] == 8
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_el_alto_e_cop_risc_basso():
    bc = _variante(p_el_eur_mwh=350)
    assert bc["risparmio_eur_anno"] == pytest.approx(-775.8080808080849)
    assert bc["van"] == pytest.approx(-31876.18224179247)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(94.47581585081586)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CALCOLABILE"
    bc2 = _variante(cop_risc=2.5)
    assert bc2["e_pdc_risc_kwh_anno"] == pytest.approx(22400.0)
    assert bc2["risparmio_eur_anno"] == pytest.approx(1620.4545454545478)
    assert bc2["van"] == pytest.approx(-10637.503598209067)
    assert bc2["breakeven_gas_eur_mwh"] == pytest.approx(80.65122377622376)
    assert bc2["payback"] is None
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_monotonia_prezzo_gas_crescente():
    base = mh796_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas_eur_mwh=91)["risparmio_eur_anno"]
    basso = _variante(p_gas_eur_mwh=89)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(173.33333333333334)
    assert base - basso == pytest.approx(173.33333333333334)


def test_monotonia_recupero_crescente_con_tetto():
    assert _variante(eta_rec=0)["risparmio_eur_anno"] < \
        mh796_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(eta_rec=1.0)["risparmio_eur_anno"] > \
        mh796_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(eta_rec=1.0)["q_rec_kwh_anno"] == \
        pytest.approx(69818.18181818182)
    assert _variante(eta_rec=1.0)["q_acs_res_kwh_anno"] == \
        pytest.approx(30181.818181818177)


def test_demo_deterministica_due_chiamate():
    a = mh796_demo_calcoli()
    b = mh796_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh796_demo().keys()) == {
        "superficie_sala_m2",
        "q_risc_kwh_m2_anno", "q_raff_kwh_m2_anno",
        "coperti_annui",
        "q_acs_kwh_th_coperto", "q_frigo_kwh_th_coperto",
        "eta_rec",
        "eta_caldaia", "cop_chiller", "cop_frigo",
        "cop_risc", "cop_raff", "cop_acs",
        "p_gas_eur_mwh", "p_el_eur_mwh",
        "om_base_eur_anno", "om_alt_eur_anno",
        "capex_eur", "wacc_pct", "vita_anni",
        "f_gas_t_per_mwh", "f_el_t_per_mwh",
        "tolleranza_pct"}


# ---------------------------------------------------------------- degenere
def test_degenere_cop_uguale_uno_sollevela():
    with pytest.raises(ValueError):
        _variante(cop_risc=1.0)
    with pytest.raises(ValueError):
        _variante(cop_acs=1.0)


def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"superficie_sala_m2": 0},
               {"superficie_sala_m2": -10},
               {"q_risc_kwh_m2_anno": -0.1},
               {"q_raff_kwh_m2_anno": -0.1},
               {"coperti_annui": 0},
               {"coperti_annui": -10},
               {"q_acs_kwh_th_coperto": -0.1},
               {"q_frigo_kwh_th_coperto": -0.1},
               {"eta_rec": -0.1}, {"eta_rec": 1.01},
               {"eta_caldaia": 0}, {"eta_caldaia": 1.01},
               {"cop_chiller": 1.0}, {"cop_chiller": 0.5},
               {"cop_frigo": 1.0}, {"cop_frigo": 0.5},
               {"cop_risc": 1.0}, {"cop_risc": 0.5},
               {"cop_raff": 1.0}, {"cop_raff": 0.5},
               {"cop_acs": 1.0}, {"cop_acs": 0.5},
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
        assert mh796_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"superficie_sala_m2": "400"},
               {"superficie_sala_m2": float("nan")},
               {"p_gas_eur_mwh": float("inf")},
               {"capex_eur": True},
               {"q_risc_kwh_m2_anno": "140"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh796_valida(**d)["valido"] is False


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    for kw in ({"p_gas_eur_mwh": 0},
               {"p_gas_eur_mwh": 70.7794289044289},
               {"p_gas_eur_mwh": 30}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] <= 0.0
        assert bc["verdetto"] == "NON_CALCOLABILE"
        assert bc["flussi"]


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh796_demo_calcoli()
    testo = mh796_csv(bc, _demo_kwargs())
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
    assert "e_frigo_kwh_anno" in testo
    assert "e_pdc_acs_kwh_anno" in testo
    assert "coperti_annui" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh796_demo_calcoli()
    testo = mh796_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"q_risc_kwh_anno;{bc['q_risc_kwh_anno']}" in testo
    assert f"gas_base_kwh_anno;{bc['gas_base_kwh_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh796_demo_calcoli()
    testo = mh796_csv(bc, _demo_kwargs())
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
    return ["mh" + "79" + "5", "st" + "79" + "5",
            "tab" + "79" + "5", "w" + "79" + "6",
            "mh" + "79" + "4", "tab" + "79" + "4"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w797_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w797_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab796:")


def test_registry_chain_tail_and_count():
    """Registry della nuova tab: il frammento UI apre la tab
    numero 796 (la coda della catena, in append dopo la
    coda precedente che termina a 795, termina con la nuova
    tab e il conteggio atteso delle tab e' 796)."""
    src = _leggi("w797_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 796
    assert src.count("with tab796:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w797_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w797_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st796_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) >= 24
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w797_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 4
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w797_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def796[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w797_ui.py")
        usate = set(re.findall(r'_def796\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 23
        assert usate <= set(mh796_demo().keys())
