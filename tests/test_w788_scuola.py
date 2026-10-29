"""Test tab788 "Scuola: pompa di calore +
recupero calore dalla ventilazione batte la
caldaia a gas per aule e mensa?"
(titolo completo nel frammento UI).
(File repo: tests/test_w788_scuola.py,
contenuto pronto da scrivere in repo.)

Business case deterministico di una scuola
guidato dalla superficie delle aule in m2 e dai
pasti della mensa all'anno: il riscaldamento
delle aule piu' l'acqua calda sanitaria della
mensa e' il fabbisogno termico, e una pompa di
calore con recupero del calore dalle perdite
termiche di ventilazione copre parte di quel
fabbisogno al posto della caldaia a gas.
Riscaldamento aule Q_risc = S_aule x q_risc
kWh_th/anno; ACS mensa Q_mensa = pasti x litri
x 4,186 x (T_uso - T_in) / 3600 kWh_th/anno;
perdite ventilazione Q_vent = S_aule x q_vent
kWh_th/anno; calore recuperato Q_rec =
min(eta_rec x Q_vent, Q_risc + Q_mensa)
kWh_th/anno, SOLO dalle perdite termiche di
ventilazione (l'eccesso viene sprecato, senza
export); fabbisogno totale Q_tot = Q_risc +
Q_mensa kWh_th/anno; calore residuo Q_res =
Q_tot - Q_rec kWh_th/anno; gas baseline G_base
= Q_tot / eta_caldaia kWh/anno; elettricita'
pompa di calore E_pdc = Q_res / COP_pdc
kWh_e/anno; C_base = G_base / 1000 x p_gas +
O&M_base EUR/anno; C_alt = E_pdc / 1000 x p_el
+ O&M_alt EUR/anno (prezzi EUR/MWh, energie kWh:
/ 1000 esatto); risparmio = C_base - C_alt;
CO2_base = G_base / 1000 x f_gas t/anno;
CO2_alt = E_pdc / 1000 x f_el t/anno; CO2_evitata
= CO2_base - CO2_alt; flussi [-CAPEX, risparmio
x vita]; VAN, TIR, payback (primo anno con
cumulato >= 0); breakeven gas p_gas_be = (C_alt
- O&M_base) x 1000 / G_base EUR/MWh, None se
G_base <= 0 o numeratore < 0, SOGLIA MINIMA
quando esiste. Verdetto: NON_CALCOLABILE se
risparmio <= 0 (guard degenere: UI salta KPI,
grafico, tabella e CSV); altrimenti CONVIENTE se
VAN > 0, MARGINALE se VAN negativa entro
tolleranza % del CAPEX, NON_CONVIENTE se VAN
negativa oltre la tolleranza. Distinzione
esplicita: NON la palestra (docce degli utenti
con acqua calda sanitaria + riscaldamento,
recupero sulle acque di scarico delle docce:
nessun recupero dalla ventilazione, nessuna
mensa), NON la piscina coperta (acqua della
vasca da scaldare: nessun'aula, nessuna mensa,
nessun recupero dalla ventilazione) e NON una
tab uffici generica (superficie generica di
uffici, senza pasti mensa e senza recupero
accoppiato alle perdite di ventilazione): qui il
driver sono i m2 di aule + i pasti della mensa
all'anno, e il calore recuperato viene SOLO
dalle perdite termiche di ventilazione.

Demo (scuola): 3.000 m2 di aule a 110
kWh_th/m2/anno, mensa da 40.000 pasti all'anno
a 8 litri per pasto da 12 C a 55 C, perdite di
ventilazione 35 kWh_th/m2/anno, recupero 0,6,
caldaia 0,9, COP pompa di calore 3,5, gas 90,
el 250 EUR/MWh, O&M base 5.000, alt 7.000, CAPEX
120.000, WACC 5 %, vita 15, f_gas 0,20, f_el
0,35, tolleranza 10 % del CAPEX. Valori calcolati
eseguendo mh788_demo_calcoli(): Q_risc
330.000, Q_mensa 15.999,822222222223, Q_vent
105.000, Q_rec 63.000, Q_tot 345.999,8222222222,
Q_res 282.999,8222222222, G_base
384.444,2469135802, E_pdc 80.857,09206349206,
C_base 39.599,98222222222, C_alt
27.214,273015873016, risparmio
12.385,709206349205, CO2_base 76,88884938271605,
CO2_alt 28,29998222222222, CO2_evitata
48,58886716049383, VAN 8.559,426122249857, TIR
6,03735875867488 %, payback 10, breakeven gas
57,78282077106123, verdetto CONVIENTE.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w789_helpers import (
    demo_calcoli,
    mh788_breakeven_gas,
    mh788_c_alt,
    mh788_c_base,
    mh788_calcola,
    mh788_co2_alt,
    mh788_co2_base,
    mh788_co2_evitata,
    mh788_cop,
    mh788_csv,
    mh788_demo,
    mh788_demo_calcoli,
    mh788_e_pdc,
    mh788_eta,
    mh788_eta_rec,
    mh788_flussi,
    mh788_gas,
    mh788_int_pos,
    mh788_num,
    mh788_nneg,
    mh788_payback,
    mh788_pct_tolleranza,
    mh788_pct_wacc,
    mh788_pos,
    mh788_q_mensa,
    mh788_q_rec,
    mh788_q_res,
    mh788_q_risc,
    mh788_q_tot,
    mh788_q_vent,
    mh788_risparmio,
    mh788_tir,
    mh788_valida,
    mh788_van,
    mh788_verdetto,
)

_DEMO = {
    "q_risc_kwh_anno": 330000.0,
    "q_mensa_kwh_anno": 15999.822222222223,
    "q_vent_kwh_anno": 105000.0,
    "q_rec_kwh_anno": 63000.0,
    "q_tot_kwh_anno": 345999.8222222222,
    "q_res_kwh_anno": 282999.8222222222,
    "gas_base_kwh_anno": 384444.2469135802,
    "e_pdc_kwh_anno": 80857.09206349206,
    "c_base_eur_anno": 39599.98222222222,
    "c_alt_eur_anno": 27214.273015873016,
    "risparmio_eur_anno": 12385.709206349205,
    "co2_base_t_anno": 76.88884938271605,
    "co2_alt_t_anno": 28.29998222222222,
    "co2_evitata_t_anno": 48.58886716049383,
    "van": 8559.426122249857,
    "tir": 6.03735875867488,
    "breakeven_gas_eur_mwh": 57.78282077106123,
}


def _demo_kwargs():
    return dict(mh788_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh788_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh788_num(3, "x") == 3.0
    assert mh788_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh788_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh788_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh788_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh788_pos(0, "x")
    with pytest.raises(ValueError):
        mh788_pos(-1, "x")
    assert mh788_pos(0.5, "x") == 0.5


def test_cop_maggiore_di_uno():
    assert mh788_cop(3.5, "x") == 3.5
    assert mh788_cop(1.01, "x") == 1.01
    with pytest.raises(ValueError):
        mh788_cop(1.0, "x")
    with pytest.raises(ValueError):
        mh788_cop(0.5, "x")
    with pytest.raises(ValueError):
        mh788_cop(0, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh788_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh788_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh788_int_pos(0, "x")


def test_eta_limiti():
    assert mh788_eta(1.0, "x") == 1.0
    assert mh788_eta(0.9, "x") == 0.9
    with pytest.raises(ValueError):
        mh788_eta(0, "x")
    with pytest.raises(ValueError):
        mh788_eta(1.01, "x")


def test_eta_rec_limiti():
    assert mh788_eta_rec(0.0, "x") == 0.0
    assert mh788_eta_rec(1.0, "x") == 1.0
    assert mh788_eta_rec(0.6, "x") == 0.6
    with pytest.raises(ValueError):
        mh788_eta_rec(-0.1, "x")
    with pytest.raises(ValueError):
        mh788_eta_rec(1.01, "x")


def test_pct_wacc_limiti():
    assert mh788_pct_wacc(0, "x") == 0.0
    assert mh788_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh788_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh788_pct_tolleranza(0, "x") == 0.0
    assert mh788_pct_tolleranza(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh788_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh788_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_q_risc_e_q_vent():
    assert mh788_q_risc(3000, 110) == 330000.0
    assert mh788_q_risc(1500, 110) == 165000.0
    assert mh788_q_risc(3000, 0) == 0.0
    assert mh788_q_vent(3000, 35) == 105000.0
    assert mh788_q_vent(3000, 0) == 0.0
    with pytest.raises(ValueError):
        mh788_q_risc(0, 110)
    with pytest.raises(ValueError):
        mh788_q_risc(3000, -10)
    with pytest.raises(ValueError):
        mh788_q_vent(0, 35)
    with pytest.raises(ValueError):
        mh788_q_vent(3000, -10)


def test_q_mensa_formula_e_salto_termico():
    assert mh788_q_mensa(40000, 8, 12, 55) == pytest.approx(15999.822222222223)
    assert mh788_q_mensa(40000, 8, 12, 12 + 43) == pytest.approx(15999.822222222223)
    assert mh788_q_mensa(0, 8, 12, 55) == 0.0
    assert mh788_q_mensa(40000, 0, 12, 55) == 0.0
    assert mh788_q_mensa(20000, 8, 12, 55) == pytest.approx(7999.911111111111)
    # Il salto termico dimezzato dimezza l'ACS mensa.
    assert mh788_q_mensa(40000, 8, 12, 33.5) == pytest.approx(15999.822222222223 / 2.0)
    with pytest.raises(ValueError):
        mh788_q_mensa(40000, 8, 55, 55)
    with pytest.raises(ValueError):
        mh788_q_mensa(40000, 8, 55, 12)
    with pytest.raises(ValueError):
        mh788_q_mensa(-1, 8, 12, 55)
    with pytest.raises(ValueError):
        mh788_q_mensa(40000, -1, 12, 55)


def test_q_rec_solo_ventilazione_con_tetto():
    assert mh788_q_rec(105000, 0.6, 345999.8222222222) == 63000.0
    assert mh788_q_rec(105000, 0, 345999.8222222222) == 0.0
    assert mh788_q_rec(105000, 1.0, 345999.8222222222) == 105000.0
    # Il recupero non supera mai il fabbisogno:
    # l'eccesso viene sprecato, senza export.
    assert mh788_q_rec(105000, 1.0, 50000.0) == 50000.0
    assert mh788_q_rec(1000000, 1.0, 345999.8222222222) == 345999.8222222222
    with pytest.raises(ValueError):
        mh788_q_rec(105000, 1.01, 345999.8222222222)
    with pytest.raises(ValueError):
        mh788_q_rec(105000, -0.1, 345999.8222222222)


def test_q_tot_q_res_gas():
    assert mh788_q_tot(330000, 15999.822222222223) == pytest.approx(345999.8222222222)
    assert mh788_q_tot(330000, 0) == 330000.0
    assert mh788_q_res(345999.8222222222, 63000.0) == pytest.approx(282999.8222222222)
    assert mh788_q_res(345999.8222222222, 345999.8222222222) == 0.0
    assert mh788_gas(345999.8222222222, 0.9) == pytest.approx(384444.2469135802)
    assert mh788_gas(0, 0.9) == 0.0
    with pytest.raises(ValueError):
        mh788_q_res(345999.8222222222, 346000.0)
    with pytest.raises(ValueError):
        mh788_gas(345999.8222222222, 0)
    with pytest.raises(ValueError):
        mh788_gas(345999.8222222222, 1.01)


def test_e_pdc():
    assert mh788_e_pdc(282999.8222222222, 3.5) == pytest.approx(80857.09206349206)
    assert mh788_e_pdc(345999.8222222222, 3.5) == pytest.approx(98857.09206349206)
    assert mh788_e_pdc(0, 3.5) == 0.0
    with pytest.raises(ValueError):
        mh788_e_pdc(282999.8222222222, 1.0)
    with pytest.raises(ValueError):
        mh788_e_pdc(282999.8222222222, 0.5)


def test_c_base_c_alt_scomposizione():
    assert mh788_c_base(384444.2469135802, 90, 5000) == pytest.approx(39599.98222222222)
    assert mh788_c_base(384444.2469135802, 0, 5000) == pytest.approx(5000.0)
    assert mh788_c_alt(80857.09206349206, 250, 7000) == pytest.approx(27214.273015873016)
    assert mh788_c_alt(0, 250, 7000) == pytest.approx(7000.0)
    with pytest.raises(ValueError):
        mh788_c_base(384444.2469135802, -1, 5000)
    with pytest.raises(ValueError):
        mh788_c_alt(80857.09206349206, 250, -1)


def test_risparmio_segno():
    assert mh788_risparmio(39599.98222222222, 27214.273015873016) == \
        pytest.approx(12385.709206349205)
    assert mh788_risparmio(27214.273015873016, 27214.273015873016) == 0.0
    assert mh788_risparmio(5000.0, 27214.273015873016) == \
        pytest.approx(-22214.273015873016)


def test_co2_base_alt_evitata():
    assert mh788_co2_base(384444.2469135802, 0.20) == \
        pytest.approx(76.88884938271605)
    assert mh788_co2_alt(80857.09206349206, 0.35) == \
        pytest.approx(28.29998222222222)
    assert mh788_co2_evitata(384444.2469135802, 0.20,
                             80857.09206349206, 0.35) == \
        pytest.approx(48.58886716049383)
    assert mh788_co2_base(0, 0.20) == pytest.approx(0.0)
    assert mh788_co2_alt(0, 0.35) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh788_co2_base(384444.2469135802, -0.10)
    with pytest.raises(ValueError):
        mh788_co2_alt(80857.09206349206, -0.10)


def test_breakeven_gas_demo_e_varianti():
    assert mh788_breakeven_gas(27214.273015873016, 5000,
                               384444.2469135802) == \
        pytest.approx(57.78282077106123)
    assert mh788_breakeven_gas(31714.273015873016, 5000,
                               384444.2469135802) == \
        pytest.approx(69.48802909743674)
    assert mh788_breakeven_gas(24214.273015873016, 5000,
                               384444.2469135802) == \
        pytest.approx(49.97934855347756)
    assert mh788_breakeven_gas(27214.273015873016, 5000, 0) is None
    # Numeratore negativo: alternativa gia' piu'
    # conveniente a prezzo gas zero -> nessun pareggio.
    assert mh788_breakeven_gas(200, 5000, 384444.2469135802) is None
    with pytest.raises(ValueError):
        mh788_breakeven_gas(27214.273015873016, 5000, -1)


def test_breakeven_verifica_pareggio():
    """Al prezzo gas di pareggio i costi si eguagliano
    e il risparmio e' zero: scatta la guard
    NON_CALCOLABILE, non un verdetto di convenienza."""
    bc = _variante(p_gas_eur_mwh=57.78282077106123)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    demo = mh788_demo_calcoli()
    assert (demo["c_alt_eur_anno"]
            - demo["om_base_eur_anno"]) * 1000.0 / demo["gas_base_kwh_anno"] == \
        pytest.approx(demo["breakeven_gas_eur_mwh"])


def test_breakeven_soglia_minima():
    """Sopra la soglia l'alternativa vince, sotto perde."""
    be = mh788_demo_calcoli()["breakeven_gas_eur_mwh"]
    assert _variante(p_gas_eur_mwh=be + 1)[
        "c_alt_eur_anno"] < _variante(p_gas_eur_mwh=be + 1)[
        "c_base_eur_anno"]
    assert _variante(p_gas_eur_mwh=be - 1)[
        "c_alt_eur_anno"] > _variante(p_gas_eur_mwh=be - 1)[
        "c_base_eur_anno"]


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh788_flussi(120000, 12385.709206349205, 15)
    assert len(fl) == 16
    assert fl[0] == -120000
    assert all(f == 12385.709206349205 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh788_demo_calcoli()
    assert bc["van"] == pytest.approx(8559.426122249857)
    assert mh788_van([-120000] + [12385.709206349205] * 15,
                     0) == pytest.approx(65785.63809523806)
    assert mh788_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh788_demo_calcoli()
    assert bc["tir"] == pytest.approx(6.03735875867488)
    assert mh788_tir([-120000] + [12385.709206349205] * 15) == \
        pytest.approx(0.0603735875867488)
    tir = mh788_tir([-120000] + [12385.709206349205] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-120000] + [12385.709206349205] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh788_payback([-120000] + [12385.709206349205] * 15) == 10
    assert mh788_payback([-120000] + [-1000.0] * 15) is None
    assert mh788_payback([0] + [12385.709206349205] * 15) == 0
    assert mh788_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh788_verdetto(12385.709206349205, 8559.426122249857, 120000,
                          10.0) == "CONVIENTE"
    assert mh788_verdetto(12385.709206349205, 0.0, 120000, 10.0) == "MARGINALE"
    assert mh788_verdetto(12385.709206349205, -12000.0, 120000, 10.0) == "MARGINALE"
    assert mh788_verdetto(12385.709206349205, -12000.01, 120000, 10.0) == "NON_CONVIENTE"
    assert mh788_verdetto(12385.709206349205, -111152.57, 120000, 10.0) == "NON_CONVIENTE"
    assert mh788_verdetto(0.0, 8559.426122249857, 120000,
                          10.0) == "NON_CALCOLABILE"
    assert mh788_verdetto(-6836.503139329809, -190960.56, 120000,
                          10.0) == "NON_CALCOLABILE"
    assert mh788_verdetto(None, 8559.426122249857, 120000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh788_verdetto(float("nan"), 8559.43, 120000, 10.0)
    with pytest.raises(ValueError):
        mh788_verdetto(12385.71, 8559.43, -1, 10.0)
    with pytest.raises(ValueError):
        mh788_verdetto(12385.71, 8559.43, 120000, 100.1)


def test_valida_demo_ok():
    v = mh788_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("superficie_aule_m2", "3000"),
                       ("superficie_aule_m2", float("nan")),
                       ("superficie_aule_m2", float("inf")),
                       ("superficie_aule_m2", True),
                       ("p_gas_eur_mwh", None),
                       ("q_risc_kwh_m2_anno", "110")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh788_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("superficie_aule_m2", 0),
                          ("superficie_aule_m2", -10),
                          ("q_risc_kwh_m2_anno", -0.1),
                          ("pasti_mensa_anno", -1),
                          ("litri_pasto", -1),
                          ("t_uso_c", 12),
                          ("t_uso_c", 10),
                          ("q_vent_kwh_m2_anno", -0.1),
                          ("eta_rec", -0.1),
                          ("eta_rec", 1.01),
                          ("eta_caldaia", 0),
                          ("eta_caldaia", 1.01),
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
        assert mh788_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"q_risc_kwh_m2_anno": 0,
              "pasti_mensa_anno": 0,
              "litri_pasto": 0,
              "q_vent_kwh_m2_anno": 0,
              "eta_rec": 0,
              "p_gas_eur_mwh": 0,
              "p_el_eur_mwh": 0,
              "om_base_eur_anno": 0, "om_alt_eur_anno": 0,
              "capex_eur": 0, "wacc_pct": 0,
              "f_gas_t_per_mwh": 0, "f_el_t_per_mwh": 0,
              "tolleranza_pct": 0})
    assert mh788_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["eta_rec"] = 1
    d["q_risc_kwh_m2_anno"] = 110
    assert mh788_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh788_demo()
    assert d["superficie_aule_m2"] == 3000
    assert d["q_risc_kwh_m2_anno"] == 110
    assert d["pasti_mensa_anno"] == 40000
    assert d["litri_pasto"] == 8
    assert d["t_in_c"] == 12
    assert d["t_uso_c"] == 55
    assert d["q_vent_kwh_m2_anno"] == 35
    assert d["eta_rec"] == 0.6
    assert d["eta_caldaia"] == 0.9
    assert d["cop_pdc"] == 3.5
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
    contro mh788_demo_calcoli()."""
    bc = mh788_demo_calcoli()
    for chiave, atteso in _DEMO.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert got == pytest.approx(atteso, rel=1e-9), chiave
    assert bc["payback"] == 10
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True
    assert demo_calcoli()["van"] == bc["van"]


def test_demo_calcoli_fisica_economia():
    bc = mh788_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(39599.98222222222)
    assert bc["c_alt_eur_anno"] == pytest.approx(27214.273015873016)
    assert bc["risparmio_eur_anno"] == pytest.approx(12385.709206349205)
    assert bc["co2_base_t_anno"] == pytest.approx(76.88884938271605)
    assert bc["co2_alt_t_anno"] == pytest.approx(28.29998222222222)
    assert bc["co2_evitata_t_anno"] == pytest.approx(48.58886716049383)
    assert bc["gas_base_kwh_anno"] == pytest.approx(384444.2469135802)


def test_demo_flussi_e_cumulato():
    bc = mh788_demo_calcoli()
    assert bc["flussi"][0] == -120000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(12385.709206349205) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -120000
    assert righe.iloc[9]["Cumulato (EUR)"] == pytest.approx(-8528.617142857176)
    assert righe.iloc[10]["Cumulato (EUR)"] == pytest.approx(3857.0920634920294)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(65785.63809523806)


def test_demo_tabella_righe():
    bc = mh788_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Riscaldamento aule (kWh_th/anno)"] == pytest.approx(330000.0)
    assert mappa["ACS mensa (kWh_th/anno)"] == pytest.approx(15999.822222222223)
    assert mappa["Perdite ventilazione (kWh_th/anno)"] == pytest.approx(105000.0)
    assert mappa["Calore recuperato (kWh_th/anno)"] == pytest.approx(63000.0)
    assert mappa["Fabbisogno totale (kWh_th/anno)"] == pytest.approx(345999.8222222222)
    assert mappa["Calore residuo (kWh_th/anno)"] == pytest.approx(282999.8222222222)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(384444.2469135802)
    assert mappa["Elettricita' pompa di calore (kWh_e/anno)"] == pytest.approx(80857.09206349206)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(39599.98222222222)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(27214.273015873016)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(12385.709206349205)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(48.58886716049383)
    assert mappa["Payback (anni)"] == 10
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] == \
        pytest.approx(57.78282077106123)


def test_demo_coerenza_interna():
    bc = mh788_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["q_risc_kwh_anno"] == pytest.approx(
        bc["superficie_aule_m2"] * bc["q_risc_kwh_m2_anno"])
    assert bc["q_mensa_kwh_anno"] == pytest.approx(
        bc["pasti_mensa_anno"] * bc["litri_pasto"] * 4.186
        * (bc["t_uso_c"] - bc["t_in_c"]) / 3600.0)
    assert bc["q_vent_kwh_anno"] == pytest.approx(
        bc["superficie_aule_m2"] * bc["q_vent_kwh_m2_anno"])
    assert bc["q_rec_kwh_anno"] == pytest.approx(
        min(bc["eta_rec"] * bc["q_vent_kwh_anno"],
            bc["q_tot_kwh_anno"]))
    assert bc["q_tot_kwh_anno"] == pytest.approx(
        bc["q_risc_kwh_anno"] + bc["q_mensa_kwh_anno"])
    assert bc["q_res_kwh_anno"] == pytest.approx(
        bc["q_tot_kwh_anno"] - bc["q_rec_kwh_anno"])
    assert bc["gas_base_kwh_anno"] == pytest.approx(
        bc["q_tot_kwh_anno"] / bc["eta_caldaia"])
    assert bc["e_pdc_kwh_anno"] == pytest.approx(
        bc["q_res_kwh_anno"] / bc["cop_pdc"])
    assert bc["co2_evitata_t_anno"] == pytest.approx(
        bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])
    assert bc["c_base_eur_anno"] == pytest.approx(
        bc["gas_base_kwh_anno"] / 1000.0 * bc["p_gas_eur_mwh"]
        + bc["om_base_eur_anno"])
    assert bc["c_alt_eur_anno"] == pytest.approx(
        bc["e_pdc_kwh_anno"] / 1000.0 * bc["p_el_eur_mwh"]
        + bc["om_alt_eur_anno"])


def test_demo_contro_riconteggio_indipendente():
    sa, qr_spec = 3000, 110
    pasti, litri, ti, tu = 40000, 8, 12, 55
    qv_spec, erec = 35, 0.6
    eta, copp = 0.9, 3.5
    pg, pel, omb, oma, cx = 90, 250, 5000, 7000, 120000
    fg, fel, wacc, vita = 0.20, 0.35, 5.0, 15
    qrisc = sa * qr_spec
    qmensa = pasti * litri * 4.186 * (tu - ti) / 3600.0
    qvent = sa * qv_spec
    qtot = qrisc + qmensa
    qrec = min(erec * qvent, qtot)
    qres = qtot - qrec
    gas = qtot / eta
    ep = qres / copp
    cb = gas / 1000.0 * pg + omb
    ca = ep / 1000.0 * pel + oma
    risp = cb - ca
    co2b = gas / 1000.0 * fg
    co2a = ep / 1000.0 * fel
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    be = (ca - omb) * 1000.0 / gas
    bc = mh788_demo_calcoli()
    assert bc["q_risc_kwh_anno"] == pytest.approx(qrisc)
    assert bc["q_mensa_kwh_anno"] == pytest.approx(qmensa)
    assert bc["q_vent_kwh_anno"] == pytest.approx(qvent)
    assert bc["q_rec_kwh_anno"] == pytest.approx(qrec)
    assert bc["q_tot_kwh_anno"] == pytest.approx(qtot)
    assert bc["q_res_kwh_anno"] == pytest.approx(qres)
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
def test_variante_gas_60_non_conviente():
    """Gas 60 EUR/MWh: risparmio ancora positivo
    (852,38) ma VAN -111.152,57 oltre la tolleranza
    (12.000): NON_CONVIENTE con payback mai
    raggiunto. Il verdetto guarda la VAN, non il
    solo risparmio positivo."""
    bc = _variante(p_gas_eur_mwh=60)
    assert bc["risparmio_eur_anno"] == pytest.approx(852.3817989417985)
    assert bc["van"] == pytest.approx(-111152.56840901493)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_gas_40_non_calcolabile():
    """Gas 40 EUR/MWh: risparmio -6.836,50, verdetto
    NON_CALCOLABILE, ma helper calcolabili (flussi
    pieni, VAN negativa, TIR None, payback None)."""
    bc = _variante(p_gas_eur_mwh=40)
    assert bc["risparmio_eur_anno"] == pytest.approx(-6836.503139329809)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_gas_zero_non_calcolabile():
    """Gas zero: costo baseline 5.000 (solo O&M)
    contro 27.214,27 dell'alternativa: risparmio
    -22.214,27, verdetto NON_CALCOLABILE."""
    bc = _variante(p_gas_eur_mwh=0)
    assert bc["valid"] is True
    assert bc["c_base_eur_anno"] == pytest.approx(5000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-22214.273015873016)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_solo_mensa_non_calcolabile():
    """Senza riscaldamento aule (q_risc zero): il
    fabbisogno e' solo ACS mensa (15.999,82), il
    recupero e' troncato a 15.999,82, il residuo e'
    zero, ma il risparmio e' -400,02 (solo O&M:
    alternativa 7.000 contro base 6.599,98),
    NON_CALCOLABILE."""
    bc = _variante(q_risc_kwh_m2_anno=0)
    assert bc["q_tot_kwh_anno"] == pytest.approx(15999.822222222223)
    assert bc["q_rec_kwh_anno"] == pytest.approx(15999.822222222223)
    assert bc["q_res_kwh_anno"] == 0.0
    assert bc["e_pdc_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(-400.0177777777776)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_senza_recupero_non_conviente():
    """Senza recupero (eta_rec zero): calore residuo
    345.999,82, E_pdc 98.857,09, risparmio 7.885,71,
    VAN -38.149,04, breakeven 69,49, NON_CONVIENTE.
    Il recupero dalla ventilazione e' decisivo:
    senza di esso la pompa di calore lavora a pieno
    carico."""
    bc = _variante(eta_rec=0)
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["q_res_kwh_anno"] == pytest.approx(345999.8222222222)
    assert bc["e_pdc_kwh_anno"] == pytest.approx(98857.09206349206)
    assert bc["risparmio_eur_anno"] == pytest.approx(7885.7092063492055)
    assert bc["van"] == pytest.approx(-38149.03504956277)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(69.48802909743674)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_recupero_totale_conviente():
    """Recupero totale (eta_rec 1,0): calore
    recuperato 105.000, residuo 240.999,82, E_pdc
    68.857,09, risparmio 15.385,71, VAN 39.698,40,
    payback 8, breakeven 49,98, CONVIENTE."""
    bc = _variante(eta_rec=1.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(105000.0)
    assert bc["q_res_kwh_anno"] == pytest.approx(240999.82222222222)
    assert bc["e_pdc_kwh_anno"] == pytest.approx(68857.09206349206)
    assert bc["risparmio_eur_anno"] == pytest.approx(15385.709206349205)
    assert bc["van"] == pytest.approx(39698.400236791655)
    assert bc["payback"] == 8
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(49.97934855347756)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_senza_mensa_conviente():
    """Senza mensa (pasti zero): fabbisogno 330.000,
    residuo 267.000, E_pdc 76.285,71, risparmio
    11.928,57, VAN 3.814,49 ancora positiva,
    CONVIENTE con payback 11 e breakeven 57,47:
    la mensa pesa poco sul totale, ma il caso
    regge anche senza di essa."""
    bc = _variante(pasti_mensa_anno=0)
    assert bc["q_mensa_kwh_anno"] == 0.0
    assert bc["q_tot_kwh_anno"] == pytest.approx(330000.0)
    assert bc["q_res_kwh_anno"] == pytest.approx(267000.0)
    assert bc["e_pdc_kwh_anno"] == pytest.approx(76285.71428571429)
    assert bc["risparmio_eur_anno"] == pytest.approx(11928.571428571428)
    assert bc["van"] == pytest.approx(3814.492312582728)
    assert bc["payback"] == 11
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(57.467532467532465)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_alto_marginale_e_non_conviente():
    bc = _variante(capex_eur=140000)
    assert bc["risparmio_eur_anno"] == pytest.approx(12385.709206349205)
    assert bc["van"] == pytest.approx(-11440.573877750143)
    assert bc["payback"] == 12
    assert bc["verdetto"] == "MARGINALE"
    bc2 = _variante(capex_eur=180000)
    assert bc2["van"] == pytest.approx(-51440.57387775012)
    assert bc2["payback"] == 15
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex_eur=0)
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(128559.42612224986, rel=1e-6)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(65785.63809523806)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(-24360.83659860747)
    assert bc2["payback"] == 10
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_el_alto_e_cop_basso():
    """Elettricita' 350 EUR/MWh e COP pompa di calore
    2,5 danno lo stesso risparmio (4.300,00) per
    vie diverse: nel primo caso la pompa di calore
    costa di piu' a parita' di energia, nel secondo
    assorbe 113.199,93 kWh_e. In entrambi i casi
    VAN -75.367,47, breakeven 78,82, NON_CONVIENTE
    con payback mai raggiunto."""
    bc = _variante(p_el_eur_mwh=350)
    assert bc["risparmio_eur_anno"] == pytest.approx(4300.0)
    assert bc["van"] == pytest.approx(-75367.47043582346)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(78.81502315479673)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"
    bc2 = _variante(cop_pdc=2.5)
    assert bc2["e_pdc_kwh_anno"] == pytest.approx(113199.92888888888)
    assert bc2["risparmio_eur_anno"] == pytest.approx(4300.0)
    assert bc2["van"] == pytest.approx(-75367.47043582346)
    assert bc2["breakeven_gas_eur_mwh"] == pytest.approx(78.81502315479673)
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_monotonia_prezzo_gas_crescente():
    base = mh788_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas_eur_mwh=91)["risparmio_eur_anno"]
    basso = _variante(p_gas_eur_mwh=89)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(384.4442469135802)
    assert base - basso == pytest.approx(384.4442469135802)


def test_monotonia_recupero_crescente_con_tetto():
    """Il risparmio cresce con il recupero finche'
    il calore recuperato non copre tutto il
    fabbisogno; oltre, il residuo e' zero e il
    risparmio si ferma al gas risparmiato meno
    la differenza di O&M."""
    assert _variante(eta_rec=0)["risparmio_eur_anno"] < \
        mh788_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(eta_rec=1.0)["risparmio_eur_anno"] > \
        mh788_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(q_vent_kwh_m2_anno=200)["q_rec_kwh_anno"] == \
        pytest.approx(345999.8222222222)
    assert _variante(q_vent_kwh_m2_anno=200)["q_res_kwh_anno"] == 0.0


def test_demo_deterministica_due_chiamate():
    a = mh788_demo_calcoli()
    b = mh788_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh788_demo().keys()) == {
        "superficie_aule_m2", "q_risc_kwh_m2_anno",
        "pasti_mensa_anno", "litri_pasto",
        "t_in_c", "t_uso_c",
        "q_vent_kwh_m2_anno", "eta_rec",
        "eta_caldaia", "cop_pdc",
        "p_gas_eur_mwh", "p_el_eur_mwh",
        "om_base_eur_anno", "om_alt_eur_anno",
        "capex_eur", "wacc_pct", "vita_anni",
        "f_gas_t_per_mwh", "f_el_t_per_mwh",
        "tolleranza_pct"}


# ---------------------------------------------------------------- degenere
def test_degenere_cop_uguale_uno_sollevela():
    with pytest.raises(ValueError):
        _variante(cop_pdc=1.0)


def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"superficie_aule_m2": 0},
               {"superficie_aule_m2": -10},
               {"q_risc_kwh_m2_anno": -0.1},
               {"pasti_mensa_anno": -1},
               {"litri_pasto": -1},
               {"t_uso_c": 12},
               {"t_uso_c": 10},
               {"q_vent_kwh_m2_anno": -0.1},
               {"eta_rec": -0.1}, {"eta_rec": 1.01},
               {"eta_caldaia": 0}, {"eta_caldaia": 1.01},
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
        assert mh788_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"superficie_aule_m2": "3000"},
               {"superficie_aule_m2": float("nan")},
               {"p_gas_eur_mwh": float("inf")},
               {"capex_eur": True},
               {"q_risc_kwh_m2_anno": "110"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh788_valida(**d)["valido"] is False


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    """Differenza chiave: risparmio <= 0 NON solleva
    negli helper (resta calcolabile con flussi, VAN,
    TIR e payback), ma il verdetto e' NON_CALCOLABILE
    e la UI salta KPI, grafico, tabella e CSV."""
    for kw in ({"p_gas_eur_mwh": 0},
               {"p_gas_eur_mwh": 57.78282077106123},
               {"p_gas_eur_mwh": 40},
               {"q_risc_kwh_m2_anno": 0}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] <= 0.0
        assert bc["verdetto"] == "NON_CALCOLABILE"
        assert bc["flussi"]


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh788_demo_calcoli()
    testo = mh788_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_gas_eur_mwh" in testo
    assert "co2_evitata_t_anno" in testo
    assert "q_mensa_kwh_anno" in testo
    assert "q_vent_kwh_anno" in testo
    assert "q_res_kwh_anno" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh788_demo_calcoli()
    testo = mh788_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"q_risc_kwh_anno;{bc['q_risc_kwh_anno']}" in testo
    assert f"gas_base_kwh_anno;{bc['gas_base_kwh_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh788_demo_calcoli()
    testo = mh788_csv(bc, _demo_kwargs())
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
    return ["mh" + "78" + "7", "st" + "78" + "7",
            "tab" + "78" + "7", "tab" + "78" + "6"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w789_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w789_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab788:")


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w789_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w789_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st788_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) >= 24
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w789_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 2
    # Entrambe le guard (input degenere e risparmio <= 0)
    # stanno prima di KPI / grafico / tabella / CSV.
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w789_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def788[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w789_ui.py")
        usate = set(re.findall(r'_def788\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 20
        assert usate <= set(mh788_demo().keys())
