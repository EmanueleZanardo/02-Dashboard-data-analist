"""Test tab754 "Caldaia a elettrodi: vapore
e calore industriale con elettricita' in
surplus - conviene piu' del gas?"

Nuova tab tab754 (caldaia a elettrodi,
w755). Business case deterministico di
una caldaia a elettrodi (conversione
diretta Joule, eta circa 0,99, calore
NON sollevato) contro la caldaia a gas
esistente, il cui CAPEX e' escluso
perche' gia' esistente: il confronto
e' solo combustibile gas contro
elettricita' piu' O&M. E_el = Q_dem /
eta_eb; F_gas = Q_dem / eta_gas;
P_th = Q_dem / ore_eq; P_el = P_th /
eta_eb; C_eb = E_el x p_el + OM_eb;
C_gas = F_gas x p_gas (solo
combustibile); risparmio = C_gas -
C_eb; CO2 evitata = (F_gas x f_gas
- E_el x f_el) / 1000, segno libero
(puo' essere negativa); CRF solo nel
LCOH, mai nei flussi; LCOH_eb =
(CAPEX x CRF + OM_eb) / Q_dem;
LCOH_gas = C_gas / Q_dem; prezzo
elettrico di pareggio = (C_gas -
OM_eb) / E_el, None se E_el <= 0,
puo' essere negativo (il solo O&M
supera gia' il costo del gas);
flussi [-CAPEX, risparmio x vita];
VAN, TIR, payback (primo anno con
cumulato >= 0). Distinta dal gas
(baseline), dalla pompa di calore
(calore sollevato con COP, non
conversione diretta), dai pannelli
ibridi PVT (un solo modulo, due
prodotti) e dal solare termico
solo-calore (calore da irradiazione).

Demo calcolata eseguendo demo_calcoli()
(e ricontrollata a mano, riga per riga):
domanda termica 5.000.000 kWh_th/anno,
5.000 ore equivalenti, eta elettrodi
0,99 e eta gas 0,90, prezzo elettrico
0,08 EUR/kWh (surplus) e prezzo gas
0,09 EUR/kWh, O&M elettrodi 20.000
EUR/anno, CAPEX elettrodi 500.000 EUR,
fattore elettrico 0,10 kg/kWh e
fattore gas 0,20 kg/kWh, WACC 5 %,
vita 15 anni, tolleranza 10 % del CAPEX.

- e_el_kwh_anno = 5050505.05050505
- f_gas_kwh_anno = 5555555.555555555
- p_th_kw = 1000.0
- p_el_kw = 1010.1010101010102
- c_eb_eur_anno = 424040.4040404041
- c_gas_eur_anno = 500000.0 (499999.99999999994 in float)
- risparmio_eur_anno = 75959.59595959587
- co2_evitata_t_anno = 606.060606060606
- crf = 0.09634228760924432
- quota_capex_eur_anno = 48171.14380462216
- lcoh_eb_eur_kwh = 0.013634228760924431
- lcoh_gas_eur_kwh = 0.10
- van = 288434.6307789692
- tir = 12.645721447074548
- payback = 7
- prezzo_pareggio_eur_kwh = 0.09504
- verdetto = 'CONVIENTE'

Scomposizione: E_el = 5.000.000 /
0,99 = 5.050.505,05 kWh_e/anno;
F_gas = 5.000.000 / 0,90 =
5.555.555,56 kWh PCI/anno; P_th =
5.000.000 / 5.000 = 1.000 kW_th;
P_el = 1.000 / 0,99 = 1.010,10 kW_e;
C_eb = 5.050.505,05 x 0,08 + 20.000
= 424.040,40 EUR/anno; C_gas =
5.555.555,56 x 0,09 = 500.000
EUR/anno (solo combustibile);
risparmio = 500.000 - 424.040,40 =
75.959,60 EUR/anno; CO2 evitata =
(5.555.555,56 x 0,20 - 5.050.505,05
x 0,10) / 1000 = 606,06 t/anno
(1.111,11 t dal gas evitato meno
505,05 t dall'elettricita');
CAPEX 500.000 EUR; CRF 0,05 x
1,05^15 / (1,05^15 - 1) =
0.09634228760924432; quota CAPEX
500.000 x 0,096342 = 48.171,14
EUR/anno; LCOH elettrodi
(48.171,14 + 20.000) / 5.000.000 =
0,0136 EUR/kWh_th contro 0,10
EUR/kWh_th del solo combustibile
gas; flussi: anno 0 -500.000, anni
1-15 risparmio 75.959,60 (piatti);
VAN -500.000 + 75.959,60 x
10,37965804 (annuita' 15 anni al
5 %) = 288.434,63 EUR; TIR circa
12,65 %; payback 7 anni (il cumulato
all'anno 6 e' -44.242,42, all'anno 7
e' 31.717,17); prezzo elettrico di
pareggio (500.000 - 20.000) /
5.050.505,05 = 0,09504 EUR/kWh;
verdetto CONVIENTE perche' VAN > 0.
NOTA: il CRF entra solo nel LCOH,
mai nei flussi: il CAPEX compare una
sola volta, all'anno 0.
NOTA 2: in questo brief il risparmio
nullo o negativo NON e' degenere:
con prezzo elettrico 0,12 EUR/kWh il
risparmio e' -126.060,61 EUR/anno e
il caso resta calcolabile (valid=True,
VAN -1.808.465,98 EUR, NON_CONVIENTE).
NOTA 3: la CO2 evitata puo' essere
negativa: con fattore elettrico 0,30
kg/kWh la CO2 evitata e' -404,04
t/anno, pur restando il caso
economicamente CONVIENTE.
NOTA 4: il prezzo elettrico di
pareggio puo' essere negativo: con
O&M 600.000 EUR/anno il pareggio e'
-0,0198 EUR/kWh, perche' il solo O&M
supera gia' il costo del gas.
NOTA 5: le eta sopra 1 vengono
clampate a 1 (vedi test_eta_clamp):
non e' un errore, e' la regola
del brief.
"""

import ast
import math
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w755_helpers import (
    demo_calcoli,
    mh754_c_eb,
    mh754_c_gas,
    mh754_calcola,
    mh754_co2_evitata,
    mh754_crf,
    mh754_csv,
    mh754_demo,
    mh754_e_el,
    mh754_eta,
    mh754_f_gas,
    mh754_flussi,
    mh754_int_nneg,
    mh754_int_pos,
    mh754_lcoh_eb,
    mh754_lcoh_gas,
    mh754_nneg,
    mh754_num,
    mh754_p_el,
    mh754_p_th,
    mh754_payback,
    mh754_pct_0_100,
    mh754_pct_wacc,
    mh754_pos,
    mh754_prezzo_pareggio,
    mh754_quota_capex,
    mh754_risparmio,
    mh754_tir,
    mh754_valida,
    mh754_van,
    mh754_verdetto,
)


def _demo_kwargs():
    return dict(mh754_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh754_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh754_num(3, "x") == 3.0
    assert mh754_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh754_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh754_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh754_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh754_pos(0, "x")
    with pytest.raises(ValueError):
        mh754_pos(-1, "x")
    assert mh754_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh754_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh754_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh754_int_pos(0, "x")


def test_int_nneg_zero_ok():
    assert mh754_int_nneg(0, "x") == 0
    with pytest.raises(ValueError):
        mh754_int_nneg(-1, "x")


def test_pct_0_100_limiti():
    assert mh754_pct_0_100(0, "x") == 0.0
    assert mh754_pct_0_100(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh754_pct_0_100(100.1, "x")
    with pytest.raises(ValueError):
        mh754_pct_0_100(-1, "x")


def test_pct_wacc_limiti():
    assert mh754_pct_wacc(0, "x") == 0.0
    assert mh754_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh754_pct_wacc(50.1, "x")


def test_eta_clamp():
    assert mh754_eta(0.99, "x") == 0.99
    assert mh754_eta(1.0, "x") == 1.0
    assert mh754_eta(1.5, "x") == 1.0
    with pytest.raises(ValueError):
        mh754_eta(0, "x")
    with pytest.raises(ValueError):
        mh754_eta(-0.1, "x")


# ---------------------------------------------------------------- fisica base
def test_e_el_e_f_gas():
    assert mh754_e_el(5000000, 0.99) == pytest.approx(5050505.05050505)
    assert mh754_e_el(5000000, 1.0) == 5000000.0
    assert mh754_e_el(5000000, 1.5) == 5000000.0
    assert mh754_f_gas(5000000, 0.90) == pytest.approx(5555555.555555555)
    assert mh754_f_gas(5000000, 1.0) == 5000000.0
    assert mh754_f_gas(5000000, 1.5) == 5000000.0
    with pytest.raises(ValueError):
        mh754_e_el(0, 0.99)
    with pytest.raises(ValueError):
        mh754_e_el(5000000, 0)
    with pytest.raises(ValueError):
        mh754_f_gas(5000000, 0)


def test_p_th_e_p_el():
    assert mh754_p_th(5000000, 5000) == 1000.0
    assert mh754_p_th(5000000, 2500) == 2000.0
    assert mh754_p_el(1000.0, 0.99) == pytest.approx(1010.1010101010102)
    assert mh754_p_el(1000.0, 1.0) == 1000.0
    assert mh754_p_el(1000.0, 1.5) == 1000.0
    with pytest.raises(ValueError):
        mh754_p_th(5000000, 0)
    with pytest.raises(ValueError):
        mh754_p_th(0, 5000)
    with pytest.raises(ValueError):
        mh754_p_el(0, 0.99)


def test_c_eb_e_c_gas_solo_combustibile():
    assert mh754_c_eb(5050505.05050505, 0.08, 20000) == pytest.approx(
        424040.4040404041)
    assert mh754_c_eb(5050505.05050505, 0.0, 0) == pytest.approx(
        0.0)
    assert mh754_c_gas(5555555.555555555, 0.09) == pytest.approx(
        500000.0)
    assert mh754_c_gas(5555555.555555555, 0.0) == 0.0
    with pytest.raises(ValueError):
        mh754_c_eb(-1, 0.08, 20000)
    with pytest.raises(ValueError):
        mh754_c_gas(5555555.555555555, -0.01)


def test_risparmio_segno():
    assert mh754_risparmio(500000.0, 424040.4040404041) == pytest.approx(
        75959.59595959587)
    assert mh754_risparmio(500000.0, 500000.0) == 0.0
    assert mh754_risparmio(500000.0, 626060.6060606061) == pytest.approx(
        -126060.60606060614)
    assert mh754_risparmio(0.0, 0.0) == 0.0


def test_co2_evitata_segno_libero():
    assert mh754_co2_evitata(5555555.555555555, 5050505.05050505, 0.20,
                             0.10) == pytest.approx(606.060606060606)
    assert mh754_co2_evitata(5555555.555555555, 5050505.05050505, 0.20,
                             0.30) == pytest.approx(-404.04040404040416)
    assert mh754_co2_evitata(5555555.555555555, 5050505.05050505, 0.20,
                             0.22) == pytest.approx(0.0, abs=1e-9)
    assert mh754_co2_evitata(0.0, 0.0, 0.20, 0.10) == 0.0
    with pytest.raises(ValueError):
        mh754_co2_evitata(-1, 5050505.05050505, 0.20, 0.10)


# ---------------------------------------------------------------- finanza base
def test_crf():
    assert mh754_crf(5.0, 15) == pytest.approx(0.09634228760924432)
    assert mh754_crf(0, 15) == pytest.approx(1.0 / 15.0)
    assert mh754_crf(5.0, 1) == pytest.approx(1.05)
    assert mh754_crf(5.0, 10) == pytest.approx(0.12950457496545661)


def test_quota_capex_e_lcoh():
    assert mh754_quota_capex(500000, 0.09634228760924432) == pytest.approx(
        48171.14380462216)
    assert mh754_lcoh_eb(500000, 0.09634228760924432, 20000,
                         5000000) == pytest.approx(0.013634228760924431)
    assert mh754_lcoh_gas(500000.0, 5000000) == pytest.approx(0.10)
    assert mh754_lcoh_eb(500000, 0.09634228760924432, 20000, 0) is None
    assert mh754_lcoh_gas(500000.0, 0) is None
    assert mh754_lcoh_eb(0, 0.09634228760924432, 20000,
                         5000000) == pytest.approx(0.004)


def test_prezzo_pareggio_formula_brief_negativo_e_none():
    assert mh754_prezzo_pareggio(500000.0, 20000, 5050505.05050505) == \
        pytest.approx(0.09504)
    assert mh754_prezzo_pareggio(500000.0, 600000, 5050505.05050505) == \
        pytest.approx(-0.0198)
    assert mh754_prezzo_pareggio(500000.0, 500000, 5050505.05050505) == \
        pytest.approx(0.0, abs=1e-9)
    assert mh754_prezzo_pareggio(500000.0, 20000, 0) is None
    assert mh754_prezzo_pareggio(500000.0, 20000, -5) is None
    assert mh754_prezzo_pareggio(0.0, 0, 5050505.05050505) == 0.0


def test_flussi_lunghezza_e_primo():
    fl = mh754_flussi(500000, 75959.59595959587, 15)
    assert len(fl) == 16
    assert fl[0] == -500000
    assert all(f == 75959.59595959587 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = demo_calcoli()
    assert bc["van"] == pytest.approx(288434.6307789692)
    assert mh754_van([-500000] + [75959.59595959587] * 15,
                     0) == pytest.approx(639393.939393938)
    assert mh754_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo_e_conviente():
    bc = demo_calcoli()
    assert bc["tir"] == pytest.approx(12.645721447074548)
    assert mh754_tir([-500000] + [75959.59595959587] * 15) == pytest.approx(
        0.12645721447074548)
    tir = mh754_tir([-500000] + [75959.59595959587] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-500000] + [75959.59595959587] * 15))
    assert npv == pytest.approx(0.0, abs=1e-4)


def test_payback():
    assert mh754_payback([-500000] + [75959.59595959587] * 15) == 7
    assert mh754_payback([-500000] + [800.0] * 15) is None
    assert mh754_payback([0] + [75959.59595959587] * 15) == 0
    assert mh754_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh754_verdetto(100.0, 500000, 10.0) == "CONVIENTE"
    assert mh754_verdetto(-47000.0, 500000, 10.0) == "MARGINALE"
    assert mh754_verdetto(-50000.0, 500000, 10.0) == "MARGINALE"
    assert mh754_verdetto(-50000.01, 500000, 10.0) == "NON_CONVIENTE"
    assert mh754_verdetto(-288434.63, 500000, 10.0) == "NON_CONVIENTE"
    assert mh754_verdetto(float("nan"), 500000, 10.0) == "NON_CALCOLABILE"
    assert mh754_verdetto(0.0, 0, 10.0) == "MARGINALE"


def test_valida_demo_ok():
    v = mh754_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("q_dem_kwh_anno", "5000000"),
                       ("q_dem_kwh_anno", float("nan")),
                       ("q_dem_kwh_anno", float("inf")),
                       ("q_dem_kwh_anno", True),
                       ("prezzo_el_eur_kwh", None)):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh754_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("q_dem_kwh_anno", 0),
                          ("ore_eq_h", 0),
                          ("eta_eb", 0),
                          ("eta_eb", -0.1),
                          ("eta_gas", 0),
                          ("eta_gas", -0.1),
                          ("prezzo_el_eur_kwh", -0.01),
                          ("prezzo_gas_eur_kwh", -0.01),
                          ("om_eur_anno", -100),
                          ("capex_eur", -1),
                          ("f_el_kg_kwh", -0.10),
                          ("f_gas_kg_kwh", -0.20),
                          ("wacc_pct", -0.1), ("wacc_pct", 50.1),
                          ("vita_anni", 0), ("vita_anni", 2.5),
                          ("tolleranza_pct", -1),
                          ("tolleranza_pct", 100.1)):
        d = _demo_kwargs()
        d[campo] = valore
        assert mh754_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"prezzo_el_eur_kwh": 0, "prezzo_gas_eur_kwh": 0,
              "om_eur_anno": 0, "capex_eur": 0,
              "f_el_kg_kwh": 0, "f_gas_kg_kwh": 0,
              "wacc_pct": 0, "tolleranza_pct": 0,
              "eta_eb": 1.0, "eta_gas": 1.0})
    assert mh754_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    assert mh754_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh754_demo()
    assert d["q_dem_kwh_anno"] == 5000000
    assert d["ore_eq_h"] == 5000
    assert d["eta_eb"] == 0.99
    assert d["eta_gas"] == 0.90
    assert d["prezzo_el_eur_kwh"] == 0.08
    assert d["prezzo_gas_eur_kwh"] == 0.09
    assert d["om_eur_anno"] == 20000
    assert d["capex_eur"] == 500000
    assert d["f_el_kg_kwh"] == 0.10
    assert d["f_gas_kg_kwh"] == 0.20
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    """Ogni _DEMO del test contro demo_calcoli():
    scarto relativo < 1e-9 (zero atteso:
    confronto assoluto)."""
    bc = demo_calcoli()
    attesi = {
        "e_el_kwh_anno": 5050505.05050505,
        "f_gas_kwh_anno": 5555555.555555555,
        "p_th_kw": 1000.0,
        "p_el_kw": 1010.1010101010102,
        "c_eb_eur_anno": 424040.4040404041,
        "c_gas_eur_anno": 500000.0,
        "risparmio_eur_anno": 75959.59595959587,
        "co2_evitata_t_anno": 606.060606060606,
        "crf": 0.09634228760924432,
        "quota_capex_eur_anno": 48171.14380462216,
        "lcoh_eb_eur_kwh": 0.013634228760924431,
        "lcoh_gas_eur_kwh": 0.10,
        "van": 288434.6307789692,
        "tir": 12.645721447074548,
        "prezzo_pareggio_eur_kwh": 0.09504,
    }
    for chiave, atteso in attesi.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert abs(got - atteso) / abs(atteso) < 1e-9, chiave
    assert bc["payback"] == 7
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_demo_calcoli_fisica():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["e_el_kwh_anno"] == pytest.approx(5050505.05050505)
    assert bc["f_gas_kwh_anno"] == pytest.approx(5555555.555555555)
    assert bc["p_th_kw"] == 1000.0
    assert bc["p_el_kw"] == pytest.approx(1010.1010101010102)
    assert bc["co2_evitata_t_anno"] == pytest.approx(606.060606060606)


def test_demo_calcoli_economia():
    bc = demo_calcoli()
    assert bc["c_eb_eur_anno"] == pytest.approx(424040.4040404041)
    assert bc["c_gas_eur_anno"] == pytest.approx(500000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(75959.59595959587)
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx(0.09504)


def test_demo_calcoli_finanza():
    bc = demo_calcoli()
    assert bc["crf"] == pytest.approx(0.09634228760924432)
    assert bc["quota_capex_eur_anno"] == pytest.approx(48171.14380462216)
    assert bc["lcoh_eb_eur_kwh"] == pytest.approx(0.013634228760924431)
    assert bc["lcoh_gas_eur_kwh"] == pytest.approx(0.10)
    assert bc["van"] == pytest.approx(288434.6307789692)
    assert bc["tir"] == pytest.approx(12.645721447074548)
    assert bc["payback"] == 7
    assert bc["verdetto"] == "CONVIENTE"


def test_demo_flussi_e_cumulato():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -500000
    assert len(bc["flussi"]) == 16
    assert all(f == 75959.59595959587 for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -500000
    assert righe.iloc[6]["Cumulato (EUR)"] == pytest.approx(
        -44242.42424242478)
    assert righe.iloc[7]["Cumulato (EUR)"] == pytest.approx(
        31717.17171717109)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(
        639393.939393938)
    assert righe.iloc[15]["Flusso (EUR/anno)"] == 75959.59595959587


def test_demo_tabella_righe():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Energia elettrica (kWh_e/anno)"] == pytest.approx(
        5050505.05050505)
    assert mappa["Potenza termica (kW_th)"] == 1000.0
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(
        75959.59595959587)
    assert mappa["Payback (anni)"] == 7
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Prezzo elettrico di pareggio (EUR/kWh)"] == pytest.approx(
        0.09504)


def test_demo_coerenza_interna():
    bc = demo_calcoli()
    assert bc["c_gas_eur_anno"] - bc["c_eb_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["e_el_kwh_anno"] * bc["prezzo_el_eur_kwh"] + \
        bc["om_eur_anno"] == pytest.approx(bc["c_eb_eur_anno"])
    assert bc["f_gas_kwh_anno"] * bc["prezzo_gas_eur_kwh"] == \
        pytest.approx(bc["c_gas_eur_anno"])
    assert (bc["f_gas_kwh_anno"] * bc["f_gas_kg_kwh"] -
            bc["e_el_kwh_anno"] * bc["f_el_kg_kwh"]) / 1000.0 == \
        pytest.approx(bc["co2_evitata_t_anno"])
    assert bc["capex_eur"] * bc["crf"] == pytest.approx(
        bc["quota_capex_eur_anno"])
    assert (bc["quota_capex_eur_anno"] + bc["om_eur_anno"]) / \
        bc["q_dem_kwh_anno"] == pytest.approx(bc["lcoh_eb_eur_kwh"])
    assert bc["c_gas_eur_anno"] / bc["q_dem_kwh_anno"] == \
        pytest.approx(bc["lcoh_gas_eur_kwh"])
    assert bc["c_gas_eur_anno"] - bc["om_eur_anno"] == pytest.approx(
        bc["prezzo_pareggio_eur_kwh"] * bc["e_el_kwh_anno"])
    assert bc["p_th_kw"] / bc["eta_eb"] == pytest.approx(bc["p_el_kw"])


def test_demo_crf_solo_nel_lcoh_non_nei_flussi():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -bc["capex_eur"]
    assert all(f == bc["risparmio_eur_anno"] for f in bc["flussi"][1:])
    assert bc["crf"] not in bc["flussi"]
    assert bc["quota_capex_eur_anno"] not in bc["flussi"]
    van_da_flussi = mh754_van(bc["flussi"], bc["wacc_pct"])
    assert van_da_flussi == pytest.approx(bc["van"])
    assert bc["lcoh_eb_eur_kwh"] == pytest.approx(
        (bc["capex_eur"] * bc["crf"] + bc["om_eur_anno"]) /
        bc["q_dem_kwh_anno"])


def test_demo_contro_riconteggio_indipendente():
    qd, ore = 5000000, 5000
    ee, eg = 0.99, 0.90
    pe, pg = 0.08, 0.09
    om, cx = 20000, 500000
    fe, fg = 0.10, 0.20
    wacc, vita = 5.0, 15
    e_el = qd / ee
    f_gas = qd / eg
    p_th = qd / ore
    p_el = p_th / ee
    c_eb = e_el * pe + om
    c_gas = f_gas * pg
    risp = c_gas - c_eb
    co2 = (f_gas * fg - e_el * fe) / 1000.0
    r = wacc / 100.0
    crf = r * (1 + r) ** vita / ((1 + r) ** vita - 1)
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    bc = demo_calcoli()
    assert bc["e_el_kwh_anno"] == e_el
    assert bc["f_gas_kwh_anno"] == f_gas
    assert bc["p_th_kw"] == p_th
    assert bc["p_el_kw"] == p_el
    assert bc["c_eb_eur_anno"] == c_eb
    assert bc["c_gas_eur_anno"] == c_gas
    assert bc["risparmio_eur_anno"] == risp
    assert bc["co2_evitata_t_anno"] == co2
    assert bc["crf"] == pytest.approx(crf)
    assert bc["van"] == pytest.approx(van)
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx((c_gas - om) / e_el)


def test_demo_riconteggio_crf_van_payback_pareggio_a_mano():
    bc = demo_calcoli()
    r = 0.05
    annuita = (1 - (1 + r) ** -15) / r
    assert annuita == pytest.approx(10.3796580381806)
    assert bc["van"] == pytest.approx(-500000 + 75959.59595959587 * annuita)
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx(
        (500000.0 - 20000) / 5050505.05050505)
    assert bc["flussi"][0] + 15 * bc["flussi"][1] == pytest.approx(
        639393.939393938)
    assert bc["flussi"][0] + 7 * bc["flussi"][1] == pytest.approx(
        31717.17171717109)


# ---------------------------------------------------------------- varianti
def test_variante_prezzo_el_alto_non_conviente():
    bc = _variante(prezzo_el_eur_kwh=0.12)
    assert bc["risparmio_eur_anno"] == pytest.approx(
        -126060.60606060614)
    assert bc["van"] == pytest.approx(-1808465.9829948873)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx(0.09504)
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_variante_prezzo_el_marginale():
    bc = _variante(prezzo_el_eur_kwh=0.0864)
    assert bc["risparmio_eur_anno"] == pytest.approx(43636.36363636364)
    assert bc["van"] < 0.0
    assert abs(bc["van"]) <= 0.10 * 500000
    assert bc["verdetto"] == "MARGINALE"
    assert bc["valid"] is True


def test_variante_prezzo_el_vicino_pareggio_non_conviente():
    bc = _variante(prezzo_el_eur_kwh=0.094)
    assert bc["risparmio_eur_anno"] == pytest.approx(5252.525252525171)
    assert bc["van"] == pytest.approx(-445480.58404188056)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_risparmio_azzerato_calcolabile():
    bc = _variante(prezzo_el_eur_kwh=0.09504)
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["van"] == pytest.approx(-500000.0)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx(0.09504)
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_variante_co2_negativa():
    bc = _variante(f_el_kg_kwh=0.30)
    assert bc["co2_evitata_t_anno"] == pytest.approx(-404.04040404040416)
    assert bc["co2_evitata_t_anno"] < 0.0
    assert bc["van"] == pytest.approx(288434.6307789692)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_co2_zero():
    bc = _variante(f_el_kg_kwh=0.22)
    assert bc["co2_evitata_t_anno"] == pytest.approx(0.0, abs=1e-9)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_pareggio_negativo():
    bc = _variante(om_eur_anno=600000)
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx(-0.0198)
    assert bc["prezzo_pareggio_eur_kwh"] < 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(-504040.4040404042)
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_variante_pareggio_zero():
    bc = _variante(om_eur_anno=500000)
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx(0.0, abs=1e-9)
    assert bc["lcoh_eb_eur_kwh"] == pytest.approx(0.10963422876092442)


def test_variante_eta_eb_clamp_sopra_uno():
    bc = _variante(eta_eb=1.5)
    assert bc["valid"] is True
    assert bc["eta_eb"] == 1.0
    assert bc["e_el_kwh_anno"] == 5000000.0
    assert bc["p_el_kw"] == 1000.0
    assert bc["risparmio_eur_anno"] == pytest.approx(80000.0)
    assert bc["van"] == pytest.approx(330372.6430544465)
    assert bc["payback"] == 7
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_eta_gas_clamp_sopra_uno():
    bc = _variante(eta_gas=1.5)
    assert bc["valid"] is True
    assert bc["eta_gas"] == 1.0
    assert bc["f_gas_kwh_anno"] == 5000000.0
    assert bc["c_gas_eur_anno"] == 450000.0
    assert bc["lcoh_gas_eur_kwh"] == pytest.approx(0.09)
    assert bc["risparmio_eur_anno"] == pytest.approx(25959.59595959593)
    assert bc["van"] == pytest.approx(-230548.27113005976)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_domanda_doppia():
    bc = _variante(q_dem_kwh_anno=10000000)
    assert bc["e_el_kwh_anno"] == pytest.approx(10101010.1010101)
    assert bc["p_th_kw"] == 2000.0
    assert bc["p_el_kw"] == pytest.approx(2020.2020202020203)
    assert bc["risparmio_eur_anno"] == pytest.approx(171919.19191919174)
    assert bc["van"] == pytest.approx(1284462.42232155)
    assert bc["payback"] == 3
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_ore_dimezzate_solo_potenze():
    bc = _variante(ore_eq_h=2500)
    assert bc["p_th_kw"] == 2000.0
    assert bc["p_el_kw"] == pytest.approx(2020.2020202020203)
    assert bc["e_el_kwh_anno"] == pytest.approx(5050505.05050505)
    assert bc["risparmio_eur_anno"] == pytest.approx(75959.59595959587)
    assert bc["van"] == pytest.approx(288434.6307789692)


def test_variante_wacc_zero():
    bc = _variante(wacc_pct=0)
    assert bc["crf"] == pytest.approx(1.0 / 15.0)
    assert bc["quota_capex_eur_anno"] == pytest.approx(33333.333333333336)
    assert bc["lcoh_eb_eur_kwh"] == pytest.approx(0.010666666666666666)
    assert bc["van"] == pytest.approx(639393.939393938)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex_eur=0)
    assert bc["capex_eur"] == 0
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(788434.6307789691)
    assert bc["lcoh_eb_eur_kwh"] == pytest.approx(0.004)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_vita_dieci():
    bc = _variante(vita_anni=10)
    assert len(bc["flussi"]) == 11
    assert bc["crf"] == pytest.approx(0.12950457496545661)
    assert bc["van"] == pytest.approx(86539.86532797689)
    assert bc["tir"] == pytest.approx(8.428009929869683)
    assert bc["payback"] == 7
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_prezzo_gas_basso_non_conviente():
    bc = _variante(prezzo_gas_eur_kwh=0.05)
    assert bc["c_gas_eur_anno"] == pytest.approx(277777.77777777775)
    assert bc["lcoh_gas_eur_kwh"] == pytest.approx(0.05555555555555555)
    assert bc["risparmio_eur_anno"] == pytest.approx(-146262.62626262632)
    assert bc["van"] == pytest.approx(-2018156.0443722731)
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx(0.05104)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_prezzi_nulli_calcolabile_non_degenere():
    bc = _variante(prezzo_el_eur_kwh=0.0, prezzo_gas_eur_kwh=0.0)
    assert bc["valid"] is True
    assert bc["c_eb_eur_anno"] == 20000.0
    assert bc["c_gas_eur_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == -20000.0
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_pareggio_negativo_demo_no():
    bc = demo_calcoli()
    assert bc["prezzo_pareggio_eur_kwh"] > 0.0
    assert bc["valid"] is True
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["risparmio_eur_anno"] > 0.0


# ---------------------------------------------------------------- degenere
def test_degenere_q_dem_zero():
    bc = _variante(q_dem_kwh_anno=0)
    assert bc["valid"] is False
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"] == []
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_kwh"] is None
    assert bc["lcoh_eb_eur_kwh"] is None
    assert bc["lcoh_gas_eur_kwh"] is None
    assert bc["errore"]


def test_degenere_ore_eta_vita():
    for kw in ({"ore_eq_h": 0}, {"eta_eb": 0},
               {"eta_eb": -0.1}, {"eta_gas": 0},
               {"eta_gas": -0.1}, {"vita_anni": 0},
               {"vita_anni": 2.5}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_wacc_tolleranza_prezzi_negativi():
    for kw in ({"wacc_pct": -1}, {"wacc_pct": 60},
               {"tolleranza_pct": -1}, {"tolleranza_pct": 101},
               {"prezzo_el_eur_kwh": -0.01},
               {"prezzo_gas_eur_kwh": -0.01},
               {"om_eur_anno": -100}, {"capex_eur": -1},
               {"q_dem_kwh_anno": -1}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_stringa_nan_inf():
    for kw in ({"q_dem_kwh_anno": "5000000"},
               {"q_dem_kwh_anno": float("nan")},
               {"prezzo_el_eur_kwh": float("inf")},
               {"capex_eur": True}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_neutro_campi():
    bc = _variante(q_dem_kwh_anno=0)
    assert bc["e_el_kwh_anno"] == 0.0
    assert bc["f_gas_kwh_anno"] == 0.0
    assert bc["p_th_kw"] == 0.0
    assert bc["p_el_kw"] == 0.0
    assert bc["c_eb_eur_anno"] == 0.0
    assert bc["c_gas_eur_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == 0.0
    assert bc["van"] == 0.0
    assert list(bc["df_flussi"].columns) == [
        "Anno", "Flusso (EUR/anno)", "Cumulato (EUR)"]
    assert list(bc["df_tabella"].columns) == ["Voce", "Valore"]


def test_pareggio_none_quando_e_el_zero():
    assert mh754_prezzo_pareggio(500000.0, 20000, 0) is None
    assert mh754_lcoh_eb(500000, 0.09634228760924432, 20000, 0) is None
    assert mh754_lcoh_gas(500000.0, 0) is None


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = demo_calcoli()
    testo = mh754_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert "e_el_kwh_anno;5050505.05050505" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "prezzo_pareggio_eur_kwh" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = demo_calcoli()
    testo = mh754_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"quota_capex_eur_anno;{bc['quota_capex_eur_anno']}" in testo
    assert f"e_el_kwh_anno;{bc['e_el_kwh_anno']}" in testo


def test_csv_degenere_solo_zeri():
    bc = _variante(q_dem_kwh_anno=0)
    testo = mh754_csv(bc, _demo_kwargs())
    assert "van_eur;0.0" in testo
    assert "e_el_kwh_anno;0.0" in testo
    assert "verdetto;NON_CALCOLABILE" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = demo_calcoli()
    testo = mh754_csv(bc, _demo_kwargs())
    for chiave in _demo_kwargs():
        assert f"{chiave};" in testo


def test_calcola_non_sollevela_per_input_numerici():
    bc = _variante(prezzo_el_eur_kwh=0, prezzo_gas_eur_kwh=0,
                   om_eur_anno=0, f_el_kg_kwh=0, f_gas_kg_kwh=0)
    assert bc["valid"] is True
    assert bc["c_eb_eur_anno"] == 0.0
    assert bc["c_gas_eur_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == 0.0


def test_monotonia_prezzo_el():
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(prezzo_el_eur_kwh=0.10)["risparmio_eur_anno"]
    basso = _variante(prezzo_el_eur_kwh=0.05)["risparmio_eur_anno"]
    assert basso > base > alto
    assert basso - base == pytest.approx(151515.15151515152)
    assert base - alto == pytest.approx(101010.10101010102)


def test_monotonia_prezzo_gas():
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(prezzo_gas_eur_kwh=0.12)["risparmio_eur_anno"]
    assert alto > base
    assert alto - base == pytest.approx(166666.66666666666)


def test_demo_deterministica_due_chiamate():
    a = demo_calcoli()
    b = demo_calcoli()
    assert a["van"] == b["van"]
    assert a["flussi"] == b["flussi"]
    assert a["tir"] == b["tir"]


def test_demo_chiavi_attese():
    assert set(mh754_demo().keys()) == {
        "q_dem_kwh_anno", "ore_eq_h", "eta_eb", "eta_gas",
        "prezzo_el_eur_kwh", "prezzo_gas_eur_kwh",
        "om_eur_anno", "capex_eur",
        "f_el_kg_kwh", "f_gas_kg_kwh",
        "wacc_pct", "vita_anni", "tolleranza_pct"}


# ---------------------------------------------------------------- AST / regole dure
_HF_FALLBACK = os.path.expanduser("~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files")


def _leggi(nome):
    qui = os.path.dirname(os.path.abspath(__file__))
    p = os.path.join(qui, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    with open(p, encoding="utf-8") as f:
        return f.read()


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w755_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w755_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab754:")


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    # token vietati costruiti per concatenazione, cosi' questo
    # stesso file non li contiene come sottostringhe contigue.
    src = _leggi("w755_helpers.py")
    vietati = ["mh" + "75" + "3", "st" + "75" + "3",
               "tab" + "75" + "3", "75" + "3"]
    assert "streamlit" not in src
    assert all(t not in src for t in vietati)


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w755_ui.py")
    vietati = ["mh" + "75" + "3", "st" + "75" + "3",
               "tab" + "75" + "3", "75" + "3"]
    assert all(t not in src for t in vietati)
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st754_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert "key=f" not in src and 'key = f' not in src
    assert "st.stop()" in src
    # guard degenere prima di KPI / grafico / tabella / CSV
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")


def test_test_senza_residui_vecchia_tab():
    # token costruiti per concatenazione: il sorgente di questo
    # stesso test non deve contenere i token vietati come
    # sottostringhe contigue (altrimenti il test sarebbe
    # autoreferenziale e fallirebbe sempre).
    src = _leggi("w755_test.py")
    vietati = ["mh" + "75" + "3", "st" + "75" + "3",
               "tab" + "75" + "3", "75" + "3"]
    assert all(t not in src for t in vietati)


def test_ui_chiavi_demo_coerenti():
    """Ogni _def754[...] letto dalla UI esiste nel dict demo:
    sweep anti-KeyError a render (lezione dello sweep chiavi demo vs UI)."""
    src = _leggi("w755_ui.py")
    usate = set(re.findall(r'_def754\["([^"]+)"\]', src))
    assert usate
    assert usate <= set(mh754_demo().keys())


def test_ui_riferisce_solo_helper_nuovi():
    src = _leggi("w755_ui.py")
    usati = set(re.findall(r'\b(mh\d+_\w+)\b', src))
    assert usati
    assert all(u.startswith("mh754_") for u in usati)


@pytest.mark.parametrize("wacc,vita,atteso", [
    (5.0, 15, 0.09634228760924432),
    (0, 15, 0.06666666666666667),
    (10.0, 10, 0.16274539488251152),
    (5.0, 1, 1.05),
    (50.0, 5, 0.5758293838862559),
])
def test_crf_parametrizzato(wacc, vita, atteso):
    assert mh754_crf(wacc, vita) == pytest.approx(atteso)


@pytest.mark.parametrize("campo,valore", [
    ("q_dem_kwh_anno", 0), ("q_dem_kwh_anno", -3),
    ("ore_eq_h", 0), ("ore_eq_h", -100),
    ("eta_eb", 0), ("eta_eb", -0.5),
    ("eta_gas", 0), ("eta_gas", -0.5),
    ("prezzo_el_eur_kwh", -0.01),
    ("prezzo_gas_eur_kwh", -0.01),
    ("om_eur_anno", -100), ("capex_eur", -1),
    ("f_el_kg_kwh", -0.10), ("f_gas_kg_kwh", -0.20),
    ("wacc_pct", -0.1), ("wacc_pct", 50.1),
    ("vita_anni", -1), ("vita_anni", 2.5),
    ("tolleranza_pct", -1), ("tolleranza_pct", 100.1),
])
def test_valida_rifiuta_singoli_campi(campo, valore):
    d = _demo_kwargs()
    d[campo] = valore
    assert mh754_valida(**d)["valido"] is False


def test_df_tabella_valori_demo_selezionati():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Domanda termica (kWh_th/anno)"] == 5000000.0
    assert mappa["Energia elettrica (kWh_e/anno)"] == pytest.approx(
        5050505.05050505)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(
        75959.59595959587)
    assert mappa["Payback (anni)"] == 7
    assert mappa["Verdetto"] == "CONVIENTE"


def test_lcoh_eb_minore_di_lcoh_gas_demo():
    bc = demo_calcoli()
    assert bc["lcoh_eb_eur_kwh"] < bc["lcoh_gas_eur_kwh"]
    assert bc["lcoh_gas_eur_kwh"] - bc["lcoh_eb_eur_kwh"] == pytest.approx(
        0.08636577123907557)
