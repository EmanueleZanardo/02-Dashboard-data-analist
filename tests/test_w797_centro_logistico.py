"""Test tab797 "Centro logistico: pompa di calore
per riscaldare un magazzino alto batte caldaia
a gas + chiller uffici?"
(titolo completo nel frammento UI).
Contenuto pronto da scrivere in repo come test
della tab centro logistico.

Business case deterministico di un centro
logistico guidato dal VOLUME del magazzino per
il riscaldamento e dalla superficie degli uffici
SOLO per il raffrescamento. Volume magazzino
V = S_magazzino x H_altezza m3; riscaldamento
magazzino Q_risc = V x q_risc kWh_th/anno
(q_risc kWh_th/m3/anno); raffrescamento uffici
Q_raff = S_uffici x q_raff kWh_c/anno (SOLO
uffici: il magazzino non viene raffrescato);
gas baseline G_base = Q_risc / eta_caldaia
kWh/anno; elettricita' chiller E_chiller =
Q_raff / COP_chiller kWh_e/anno; elettricita'
pompa di calore in riscaldamento magazzino
E_pdc_risc = Q_risc / COP_pdc_risc kWh_e/anno;
in raffrescamento uffici E_pdc_raff = Q_raff /
COP_pdc_raff kWh_e/anno; C_base = E_chiller /
1000 x p_el + G_base / 1000 x p_gas + O&M_base
EUR/anno; C_alt = (E_pdc_risc + E_pdc_raff) /
1000 x p_el + O&M_alt EUR/anno (prezzi EUR/MWh,
energie kWh: / 1000 esatto); risparmio = C_base
- C_alt; CO2_base = G_base / 1000 x f_gas +
E_chiller / 1000 x f_el t/anno; CO2_alt =
(E_pdc_risc + E_pdc_raff) / 1000 x f_el t/anno;
CO2_evitata = CO2_base - CO2_alt; flussi
[-CAPEX, risparmio x vita]; VAN, TIR, payback
(primo anno con cumulato >= 0); breakeven gas
p_gas_be = (C_alt - E_chiller / 1000 x p_el -
O&M_base) x 1000 / G_base EUR/MWh, None se
G_base <= 0 o numeratore < 0, SOGLIA MINIMA
quando esiste. Verdetto: NON_CALCOLABILE se
risparmio <= 0 (guard degenere: UI salta KPI,
grafico, tabella e CSV); altrimenti CONVIENTE
se VAN > 0, MARGINALE se VAN negativa entro
tolleranza % del CAPEX, NON_CONVIENTE se VAN
negativa oltre la tolleranza. Distinzione
esplicita: distinto dal supermercato
(superficie di vendita, banchi frigo, recupero
sul riscaldamento), dal ristorante (coperti,
ACS, celle frigo, recupero su ACS),
dall'albergo (pernottamento, ACS docce ospiti),
dalla scuola (aule + mensa, chiusure
stagionali), dall'ospedale (reparti 24h,
ventilazione aria esausta, ACS posti letto),
dalla palestra (docce utenti) e dalla piscina
(vasca riscaldata): qui driver VOLUMETRICO =
m3 di magazzino per il riscaldamento + m2 di
uffici SOLO per il raffrescamento; niente ACS,
niente celle frigo, niente recupero di calore.

Demo (centro logistico): 5000 m2 di magazzino
alto 10 m (volume 50.000 m3) a 15 kWh_th/m3/anno
di riscaldamento, uffici 500 m2 a 80
kWh_c/m2/anno di raffrescamento, caldaia 0,90,
chiller COP 3,0, pompa di calore COP
riscaldamento 3,2 e COP raffrescamento 3,5,
gas 90, el 250 EUR/MWh, O&M base 12.000, alt
15.000, CAPEX 120.000, WACC 5 %, vita 15,
f_gas 0,20, f_el 0,35, tolleranza 10 % del
CAPEX. Valori calcolati eseguendo
mh797_demo_calcoli(): volume 50.000, Q_risc
750.000, Q_raff 40.000, G_base
833.333,3333333333, E_chiller
13.333,333333333334, E_pdc_risc 234.375,
E_pdc_raff 11.428,57142857143, C_base
90.333,33333333333, C_alt 76.450,89285714286,
risparmio 13.882,440476190473, CO2_base
171,33333333333331, CO2_alt 86,03124999999999,
CO2_evitata 85,30208333333333, VAN
24.094,98487825402, TIR 7,839484504665902 %,
payback 9, breakeven gas 73,34107142857144,
verdetto CONVIENTE.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w798_helpers import (
    demo_calcoli,
    mh797_breakeven_gas,
    mh797_c_alt,
    mh797_c_base,
    mh797_calcola,
    mh797_co2_alt,
    mh797_co2_base,
    mh797_co2_evitata,
    mh797_cop,
    mh797_csv,
    mh797_demo,
    mh797_demo_calcoli,
    mh797_e_chiller,
    mh797_e_pdc_raff,
    mh797_e_pdc_risc,
    mh797_eta,
    mh797_flussi,
    mh797_gas,
    mh797_int_pos,
    mh797_num,
    mh797_nneg,
    mh797_payback,
    mh797_pct_tolleranza,
    mh797_pct_wacc,
    mh797_pos,
    mh797_q_raff,
    mh797_q_risc,
    mh797_risparmio,
    mh797_tir,
    mh797_valida,
    mh797_van,
    mh797_verdetto,
    mh797_volume,
)

_DEMO = {
    "volume_m3": 50000.0,
    "q_risc_kwh_anno": 750000.0,
    "q_raff_kwh_anno": 40000.0,
    "gas_base_kwh_anno": 833333.3333333333,
    "e_chiller_kwh_anno": 13333.333333333334,
    "e_pdc_risc_kwh_anno": 234375.0,
    "e_pdc_raff_kwh_anno": 11428.57142857143,
    "c_base_eur_anno": 90333.33333333333,
    "c_alt_eur_anno": 76450.89285714286,
    "risparmio_eur_anno": 13882.440476190473,
    "co2_base_t_anno": 171.33333333333331,
    "co2_alt_t_anno": 86.03124999999999,
    "co2_evitata_t_anno": 85.30208333333333,
    "van": 24094.98487825402,
    "tir": 7.839484504665902,
    "breakeven_gas_eur_mwh": 73.34107142857144,
}


def _demo_kwargs():
    return dict(mh797_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh797_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh797_num(3, "x") == 3.0
    assert mh797_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh797_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh797_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh797_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh797_pos(0, "x")
    with pytest.raises(ValueError):
        mh797_pos(-1, "x")
    assert mh797_pos(0.5, "x") == 0.5


def test_cop_maggiore_di_uno():
    assert mh797_cop(3.2, "x") == 3.2
    assert mh797_cop(1.01, "x") == 1.01
    with pytest.raises(ValueError):
        mh797_cop(1.0, "x")
    with pytest.raises(ValueError):
        mh797_cop(0.5, "x")
    with pytest.raises(ValueError):
        mh797_cop(0, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh797_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh797_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh797_int_pos(0, "x")


def test_eta_limiti():
    assert mh797_eta(1.0, "x") == 1.0
    assert mh797_eta(0.9, "x") == 0.9
    with pytest.raises(ValueError):
        mh797_eta(0, "x")
    with pytest.raises(ValueError):
        mh797_eta(1.01, "x")


def test_pct_wacc_limiti():
    assert mh797_pct_wacc(0, "x") == 0.0
    assert mh797_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh797_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh797_pct_tolleranza(0, "x") == 0.0
    assert mh797_pct_tolleranza(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh797_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh797_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_volume_q_risc_q_raff():
    assert mh797_volume(5000, 10) == 50000.0
    assert mh797_volume(5000, 6) == 30000.0
    assert mh797_q_risc(50000, 15) == 750000.0
    assert mh797_q_risc(50000, 0) == 0.0
    assert mh797_q_raff(500, 80) == 40000.0
    assert mh797_q_raff(500, 0) == 0.0
    assert mh797_q_raff(0, 80) == 0.0
    with pytest.raises(ValueError):
        mh797_volume(0, 10)
    with pytest.raises(ValueError):
        mh797_volume(5000, 0)
    with pytest.raises(ValueError):
        mh797_volume(5000, -1)
    with pytest.raises(ValueError):
        mh797_q_risc(50000, -1)
    with pytest.raises(ValueError):
        mh797_q_raff(500, -10)
    with pytest.raises(ValueError):
        mh797_q_raff(-10, 80)


def test_gas_e_chiller():
    assert mh797_gas(750000, 0.9) == pytest.approx(833333.3333333333)
    assert mh797_gas(0, 0.9) == 0.0
    assert mh797_e_chiller(40000, 3.0) == pytest.approx(13333.333333333334)
    assert mh797_e_chiller(0, 3.0) == 0.0
    with pytest.raises(ValueError):
        mh797_gas(750000, 0)
    with pytest.raises(ValueError):
        mh797_gas(750000, 1.01)
    with pytest.raises(ValueError):
        mh797_e_chiller(40000, 1.0)


def test_e_pdc_risc_raff():
    assert mh797_e_pdc_risc(750000, 3.2) == 234375.0
    assert mh797_e_pdc_risc(0, 3.2) == 0.0
    assert mh797_e_pdc_raff(40000, 3.5) == pytest.approx(11428.57142857143)
    assert mh797_e_pdc_raff(0, 3.5) == 0.0
    with pytest.raises(ValueError):
        mh797_e_pdc_risc(750000, 1.0)
    with pytest.raises(ValueError):
        mh797_e_pdc_raff(40000, 0.5)


def test_c_base_c_alt_scomposizione():
    assert mh797_c_base(13333.333333333334, 250,
                        833333.3333333333, 90,
                        12000) == pytest.approx(90333.33333333333)
    assert mh797_c_base(13333.333333333334, 250,
                        833333.3333333333, 0,
                        12000) == pytest.approx(15333.333333333334)
    assert mh797_c_alt(234375.0, 11428.57142857143, 250,
                       15000) == pytest.approx(76450.89285714286)
    assert mh797_c_alt(0, 0, 250, 15000) == pytest.approx(15000.0)
    with pytest.raises(ValueError):
        mh797_c_base(13333.333333333334, 250,
                     833333.3333333333, -1, 12000)
    with pytest.raises(ValueError):
        mh797_c_alt(234375.0, 11428.57142857143, 250, -1)


def test_risparmio_segno():
    assert mh797_risparmio(90333.33333333333, 76450.89285714286) == pytest.approx(13882.440476190473)
    assert mh797_risparmio(76450.89285714286, 76450.89285714286) == 0.0
    assert mh797_risparmio(65333.33333333333, 76450.89285714286) == pytest.approx(-11117.559523809527)


def test_co2_base_alt_evitata():
    assert mh797_co2_base(833333.3333333333, 0.20, 13333.333333333334,
                          0.35) == pytest.approx(171.33333333333331)
    assert mh797_co2_alt(234375.0, 11428.57142857143,
                         0.35) == pytest.approx(86.03124999999999)
    assert mh797_co2_evitata(833333.3333333333, 0.20,
                             13333.333333333334,
                             234375.0, 11428.57142857143,
                             0.35) == pytest.approx(85.30208333333333)
    assert mh797_co2_base(0, 0.20, 0, 0.35) == pytest.approx(0.0)
    assert mh797_co2_alt(0, 0, 0.35) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh797_co2_base(833333.3333333333, -0.10, 13333.333333333334,
                       0.35)
    with pytest.raises(ValueError):
        mh797_co2_alt(234375.0, 11428.57142857143, -0.10)


def test_breakeven_gas_demo_e_varianti():
    assert mh797_breakeven_gas(76450.89285714286, 13333.333333333334,
                               250, 12000,
                               833333.3333333333) == \
        pytest.approx(73.34107142857144)
    assert mh797_breakeven_gas(73593.75, 0,
                               250, 12000,
                               833333.3333333333) == \
        pytest.approx(73.9125)
    assert mh797_breakeven_gas(84821.42857142858, 13333.333333333334,
                               250, 12000,
                               833333.3333333333) == \
        pytest.approx(83.38571428571431)
    assert mh797_breakeven_gas(76450.89285714286, 13333.333333333334,
                               250, 12000, 0) is None
    assert mh797_breakeven_gas(200, 13333.333333333334,
                               250, 12000,
                               833333.3333333333) is None
    with pytest.raises(ValueError):
        mh797_breakeven_gas(76450.89285714286, 13333.333333333334,
                            250, 12000, -1)


def test_breakeven_verifica_pareggio():
    bc = _variante(p_gas_eur_mwh=73.34107142857144)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    # Al pareggio esatto il risparmio e' zero a meno di
    # arrotondamento floating point (qui +1,45e-11, quindi
    # verdetto NON_CONVIENTE per VAN negativa): la guard
    # NON_CALCOLABILE scatta appena sotto il pareggio.
    sotto = _variante(p_gas_eur_mwh=73.34)
    assert sotto["risparmio_eur_anno"] < 0.0
    assert sotto["verdetto"] == "NON_CALCOLABILE"
    demo = mh797_demo_calcoli()
    assert (demo["c_alt_eur_anno"]
            - demo["e_chiller_kwh_anno"] / 1000.0
            * demo["p_el_eur_mwh"]
            - demo["om_base_eur_anno"]) * 1000.0 / demo["gas_base_kwh_anno"] == \
        pytest.approx(demo["breakeven_gas_eur_mwh"])


def test_breakeven_soglia_minima():
    be = mh797_demo_calcoli()["breakeven_gas_eur_mwh"]
    assert _variante(p_gas_eur_mwh=be + 1)[
        "c_alt_eur_anno"] < _variante(p_gas_eur_mwh=be + 1)[
        "c_base_eur_anno"]
    assert _variante(p_gas_eur_mwh=be - 1)[
        "c_alt_eur_anno"] > _variante(p_gas_eur_mwh=be - 1)[
        "c_base_eur_anno"]


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh797_flussi(120000, 13882.440476190473, 15)
    assert len(fl) == 16
    assert fl[0] == -120000
    assert all(f == 13882.440476190473 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh797_demo_calcoli()
    assert bc["van"] == pytest.approx(24094.98487825402)
    assert mh797_van([-120000] + [13882.440476190473] * 15,
                     0) == pytest.approx(88236.6071428571)
    assert mh797_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh797_demo_calcoli()
    assert bc["tir"] == pytest.approx(7.839484504665902)
    assert mh797_tir([-120000] + [13882.440476190473] * 15) == \
        pytest.approx(0.07839484504665901)
    tir = mh797_tir([-120000] + [13882.440476190473] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-120000] + [13882.440476190473] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh797_payback([-120000] + [13882.440476190473] * 15) == 9
    assert mh797_payback([-120000] + [-1000.0] * 15) is None
    assert mh797_payback([0] + [13882.440476190473] * 15) == 0
    assert mh797_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh797_verdetto(13882.440476190473, 24094.98487825402, 120000,
                          10.0) == "CONVIENTE"
    assert mh797_verdetto(13882.440476190473, 0.0, 120000, 10.0) == "MARGINALE"
    assert mh797_verdetto(13882.440476190473, -12000.0, 120000, 10.0) == "MARGINALE"
    assert mh797_verdetto(13882.440476190473, -12000.01, 120000, 10.0) == "NON_CONVIENTE"
    assert mh797_verdetto(13882.440476190473, -62788.31, 120000, 10.0) == "NON_CONVIENTE"
    assert mh797_verdetto(0.0, 24094.98487825402, 120000,
                          10.0) == "NON_CALCOLABILE"
    assert mh797_verdetto(-11117.559523809527, -235396.47, 120000,
                          10.0) == "NON_CALCOLABILE"
    assert mh797_verdetto(None, 24094.98487825402, 120000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh797_verdetto(float("nan"), 24094.98, 120000, 10.0)
    with pytest.raises(ValueError):
        mh797_verdetto(13882.440476190473, 24094.98, -1, 10.0)
    with pytest.raises(ValueError):
        mh797_verdetto(13882.440476190473, 24094.98, 120000, 100.1)


def test_valida_demo_ok():
    v = mh797_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("s_magazzino_m2", "5000"),
                       ("s_magazzino_m2", float("nan")),
                       ("s_magazzino_m2", float("inf")),
                       ("s_magazzino_m2", True),
                       ("p_gas_eur_mwh", None),
                       ("q_risc_kwh_th_m3_anno", "15")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh797_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("s_magazzino_m2", 0),
                          ("s_magazzino_m2", -10),
                          ("h_altezza_m", 0),
                          ("h_altezza_m", -1),
                          ("q_risc_kwh_th_m3_anno", -0.1),
                          ("s_uffici_m2", -10),
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
        assert mh797_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"q_risc_kwh_th_m3_anno": 0,
              "s_uffici_m2": 0,
              "q_raff_kwh_c_m2_anno": 0,
              "p_gas_eur_mwh": 0,
              "p_el_eur_mwh": 0,
              "om_base_eur_anno": 0, "om_alt_eur_anno": 0,
              "capex_eur": 0, "wacc_pct": 0,
              "f_gas_t_per_mwh": 0, "f_el_t_per_mwh": 0,
              "tolleranza_pct": 0})
    assert mh797_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["q_risc_kwh_th_m3_anno"] = 15
    assert mh797_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh797_demo()
    assert d["s_magazzino_m2"] == 5000
    assert d["h_altezza_m"] == 10
    assert d["q_risc_kwh_th_m3_anno"] == 15
    assert d["s_uffici_m2"] == 500
    assert d["q_raff_kwh_c_m2_anno"] == 80
    assert d["eta_caldaia"] == 0.90
    assert d["cop_chiller"] == 3.0
    assert d["cop_pdc_risc"] == 3.2
    assert d["cop_pdc_raff"] == 3.5
    assert d["p_gas_eur_mwh"] == 90
    assert d["p_el_eur_mwh"] == 250
    assert d["om_base_eur_anno"] == 12000
    assert d["om_alt_eur_anno"] == 15000
    assert d["capex_eur"] == 120000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["f_gas_t_per_mwh"] == 0.20
    assert d["f_el_t_per_mwh"] == 0.35
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    bc = mh797_demo_calcoli()
    for chiave, atteso in _DEMO.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert got == pytest.approx(atteso, rel=1e-9), chiave
    assert bc["payback"] == 9
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True
    assert demo_calcoli()["van"] == bc["van"]


def test_demo_calcoli_fisica_economia():
    bc = mh797_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(90333.33333333333)
    assert bc["c_alt_eur_anno"] == pytest.approx(76450.89285714286)
    assert bc["risparmio_eur_anno"] == pytest.approx(13882.440476190473)
    assert bc["co2_base_t_anno"] == pytest.approx(171.33333333333331)
    assert bc["co2_alt_t_anno"] == pytest.approx(86.03124999999999)
    assert bc["co2_evitata_t_anno"] == pytest.approx(85.30208333333333)
    assert bc["gas_base_kwh_anno"] == pytest.approx(833333.3333333333)


def test_demo_flussi_e_cumulato():
    bc = mh797_demo_calcoli()
    assert bc["flussi"][0] == -120000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(13882.440476190473) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -120000
    assert righe.iloc[8]["Cumulato (EUR)"] == pytest.approx(-8940.476190476213)
    assert righe.iloc[9]["Cumulato (EUR)"] == pytest.approx(4941.964285714261)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(88236.6071428571)


def test_demo_tabella_righe():
    bc = mh797_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Volume magazzino (m3)"] == pytest.approx(50000.0)
    assert mappa["Riscaldamento magazzino (kWh_th/anno)"] == pytest.approx(750000.0)
    assert mappa["Raffrescamento uffici (kWh_c/anno)"] == pytest.approx(40000.0)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(833333.3333333333)
    assert mappa["Elettricita' chiller (kWh_e/anno)"] == pytest.approx(13333.333333333334)
    assert mappa["Elettricita' pompa di calore riscaldamento (kWh_e/anno)"] == pytest.approx(234375.0)
    assert mappa["Elettricita' pompa di calore raffrescamento (kWh_e/anno)"] == pytest.approx(11428.57142857143)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(90333.33333333333)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(76450.89285714286)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(13882.440476190473)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(85.30208333333333)
    assert mappa["Payback (anni)"] == 9
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] == \
        pytest.approx(73.34107142857144)


def test_demo_coerenza_interna():
    bc = mh797_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["volume_m3"] == pytest.approx(
        bc["s_magazzino_m2"] * bc["h_altezza_m"])
    assert bc["q_risc_kwh_anno"] == pytest.approx(
        bc["volume_m3"] * bc["q_risc_kwh_th_m3_anno"])
    assert bc["q_raff_kwh_anno"] == pytest.approx(
        bc["s_uffici_m2"] * bc["q_raff_kwh_c_m2_anno"])
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
    s_mag, halt = 5000, 10
    qr_spec, s_uff, qf_spec = 15, 500, 80
    eta, copc, copr, copf = 0.90, 3.0, 3.2, 3.5
    pg, pel, omb, oma, cx = 90, 250, 12000, 15000, 120000
    fg, fel, wacc, vita = 0.20, 0.35, 5.0, 15
    vol = s_mag * halt
    qrisc = vol * qr_spec
    qraff = s_uff * qf_spec
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
    bc = mh797_demo_calcoli()
    assert bc["volume_m3"] == pytest.approx(vol)
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
    assert bc["risparmio_eur_anno"] == pytest.approx(-11117.559523809527)
    assert bc["van"] == pytest.approx(-235396.46607626072)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_gas_30_non_calcolabile():
    bc = _variante(p_gas_eur_mwh=30)
    assert bc["risparmio_eur_anno"] == pytest.approx(-36117.559523809527)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_gas_zero_non_calcolabile():
    bc = _variante(p_gas_eur_mwh=0)
    assert bc["valid"] is True
    assert bc["c_base_eur_anno"] == pytest.approx(15333.333333333334)
    assert bc["risparmio_eur_anno"] == pytest.approx(-61117.559523809527)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_senza_raffrescamento_conviente():
    bc = _variante(q_raff_kwh_c_m2_anno=0)
    assert bc["q_raff_kwh_anno"] == 0.0
    assert bc["e_chiller_kwh_anno"] == 0.0
    assert bc["e_pdc_raff_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(13406.25)
    assert bc["van"] == pytest.approx(19152.290574358536)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(73.9125)
    assert bc["payback"] == 9
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_alto_marginale_e_non_conviente():
    bc = _variante(capex_eur=150000)
    assert bc["risparmio_eur_anno"] == pytest.approx(13882.440476190473)
    assert bc["van"] == pytest.approx(-5905.01512174596)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"
    bc2 = _variante(capex_eur=200000)
    assert bc2["van"] == pytest.approx(-55905.01512174598)
    assert bc2["payback"] == 15
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex_eur=0)
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(144094.98487825402, rel=1e-6)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(88236.6071428571)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(-12803.474472671012)
    assert bc2["payback"] == 9
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_el_alto_e_cop_risc_basso():
    bc = _variante(p_el_eur_mwh=350)
    assert bc["risparmio_eur_anno"] == pytest.approx(-9364.583333333328)
    assert bc["van"] == pytest.approx(-217201.17267004526)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(101.2375)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CALCOLABILE"
    bc2 = _variante(cop_pdc_risc=2.8)
    assert bc2["e_pdc_risc_kwh_anno"] == pytest.approx(267857.1428571429)
    assert bc2["risparmio_eur_anno"] == pytest.approx(5511.904761904749)
    assert bc2["van"] == pytest.approx(-62788.313432409515)
    assert bc2["breakeven_gas_eur_mwh"] == pytest.approx(83.38571428571431)
    assert bc2["payback"] is None
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_altezza_bassa_non_conviente():
    bc = _variante(h_altezza_m=6)
    assert bc["volume_m3"] == pytest.approx(30000.0)
    assert bc["q_risc_kwh_anno"] == pytest.approx(450000.0)
    assert bc["gas_base_kwh_anno"] == pytest.approx(500000.0)
    assert bc["c_base_eur_anno"] == pytest.approx(60333.333333333336)
    assert bc["c_alt_eur_anno"] == pytest.approx(53013.392857142855)
    assert bc["risparmio_eur_anno"] == pytest.approx(7319.940476190481)
    assert bc["van"] == pytest.approx(-44021.52099730604)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(75.36011904761905)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_monotonia_prezzo_gas_crescente():
    base = mh797_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas_eur_mwh=91)["risparmio_eur_anno"]
    basso = _variante(p_gas_eur_mwh=89)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(833.3333333333333)
    assert base - basso == pytest.approx(833.3333333333333)


def test_monotonia_volume_crescente():
    assert _variante(h_altezza_m=6)["risparmio_eur_anno"] < \
        mh797_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(h_altezza_m=12)["risparmio_eur_anno"] > \
        mh797_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(h_altezza_m=12)["volume_m3"] == \
        pytest.approx(60000.0)


def test_demo_deterministica_due_chiamate():
    a = mh797_demo_calcoli()
    b = mh797_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh797_demo().keys()) == {
        "s_magazzino_m2", "h_altezza_m",
        "q_risc_kwh_th_m3_anno",
        "s_uffici_m2", "q_raff_kwh_c_m2_anno",
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
    for kw in ({"s_magazzino_m2": 0},
               {"s_magazzino_m2": -10},
               {"h_altezza_m": 0},
               {"h_altezza_m": -1},
               {"q_risc_kwh_th_m3_anno": -0.1},
               {"s_uffici_m2": -10},
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
        assert mh797_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"s_magazzino_m2": "5000"},
               {"s_magazzino_m2": float("nan")},
               {"p_gas_eur_mwh": float("inf")},
               {"capex_eur": True},
               {"q_risc_kwh_th_m3_anno": "15"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh797_valida(**d)["valido"] is False


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    for kw in ({"p_gas_eur_mwh": 0},
               {"p_gas_eur_mwh": 73.34},
               {"p_gas_eur_mwh": 30}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] <= 0.0
        assert bc["verdetto"] == "NON_CALCOLABILE"
        assert bc["flussi"]


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh797_demo_calcoli()
    testo = mh797_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_gas_eur_mwh" in testo
    assert "co2_evitata_t_anno" in testo
    assert "q_raff_kwh_anno" in testo
    assert "volume_m3" in testo
    assert "e_chiller_kwh_anno" in testo
    assert "e_pdc_raff_kwh_anno" in testo
    assert "s_magazzino_m2" in testo
    assert "h_altezza_m" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh797_demo_calcoli()
    testo = mh797_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"q_risc_kwh_anno;{bc['q_risc_kwh_anno']}" in testo
    assert f"gas_base_kwh_anno;{bc['gas_base_kwh_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh797_demo_calcoli()
    testo = mh797_csv(bc, _demo_kwargs())
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
    return ["mh" + "79" + "6", "st" + "79" + "6",
            "tab" + "79" + "6", "w" + "79" + "7",
            "mh" + "79" + "5", "tab" + "79" + "5"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w798_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w798_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab797:")


def test_registry_chain_tail_and_count():
    """Registry della nuova tab: il frammento UI apre la tab
    numero 797 (la coda della catena, in append dopo la
    coda precedente che termina a 796, termina con la
    nuova tab e il conteggio atteso delle tab e' 797)."""
    src = _leggi("w798_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 797
    assert src.count("with tab797:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w798_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w798_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st797_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) >= 24
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w798_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 4
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w798_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def797[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w798_ui.py")
        usate = set(re.findall(r'_def797\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 19
        assert usate <= set(mh797_demo().keys())
