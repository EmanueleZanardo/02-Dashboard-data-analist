"""Test tab756 "Cartiera: essiccare la
carta con vapore o con pompa di
calore?"

Nuova tab tab756 (essiccazione carta,
w757). Business case deterministico
della sezione essiccamento di una
macchina continua per carta: i
cilindri essiccatori asciugano il
foglio e il calore puo' arrivare dal
vapore di una caldaia a gas
(baseline) oppure in parte da una
pompa di calore industriale di
retrofit che copre una quota del
calore di essiccazione, con il resto
che resta a vapore da caldaia a gas.
q_term = evap x calore x
0.2777777777777778 (GJ -> MWh);
Q_term = produzione x q_term;
gas_base = Q_term / eta_caldaia;
C_base = gas_base x p_gas;
co2_base = gas_base x f_gas;
Q_pdc = quota_pdc / 100 x Q_term;
E_el = Q_pdc / COP; gas_res =
(1 - quota_pdc / 100) x Q_term /
eta_caldaia; C_alt_var = gas_res x
p_gas + E_el x p_el; C_alt =
C_alt_var + OM_fisso; co2_alt =
gas_res x f_gas + E_el x f_el;
risparmio = C_base - C_alt;
CO2 evitata = co2_base - co2_alt,
segno libero (puo' essere negativa),
NON monetizzata; CRF solo nel LCO,
mai nei flussi; LCO_base = C_base /
produzione; LCO_alt = (CAPEX x CRF +
OM_fisso) / produzione + C_alt_var /
produzione; prezzo elettrico di
pareggio = (C_base - gas_res x
p_gas - OM_fisso) / E_el, None se
E_el <= 0, puo' essere negativo (il
solo O&M fisso piu' il gas residuo
superano gia' il costo baseline);
flussi [-CAPEX, risparmio x vita];
VAN, TIR, payback (primo anno con
cumulato >= 0). Distinta dalla
tab generica di essiccazione (li'
si rimuove acqua da un prodotto
qualsiasi, senza macchina continua),
dalla tab generica pompa di calore
industriale ad alta temperatura
(li' il COP di Carnot viene da
calore di scarto, senza foglio e
senza baseline caldaia per
essiccatori) e dal
teleriscaldamento / cogenerazione
(li' il calore va a una rete o a un
ciclo combinato, non ai cilindri di
una cartiera).

Demo calcolata eseguendo demo_calcoli()
(e ricontrollata a mano, riga per riga):
produzione 100.000 t/anno, evaporazione
1,3 t acqua/t carta, calore 2,7
GJ/t acqua, rendimento caldaia 0,90,
quota PdC 60 %, COP 3,5, prezzo gas
45 EUR/MWh, prezzo elettrico 110
EUR/MWh, O&M fisso 300.000 EUR/anno,
CAPEX PdC 4.000.000 EUR, fattore gas
0,20 tCO2/MWh e fattore elettrico
0,25 tCO2/MWh, WACC 5 %, vita 15
anni, tolleranza 10 % del CAPEX.

- q_term_mwh_per_t = 0.975
- q_term_mwh_anno = 97500.0
- gas_base_mwh_anno = 108333.33333333334
- c_base_eur_anno = 4875000.0
- q_pdc_mwh_anno = 58500.0
- e_el_mwh_anno = 16714.285714285717
- gas_res_mwh_anno = 43333.33333333334
- c_alt_var_eur_anno = 3788571.428571429
- c_alt_eur_anno = 4088571.428571429
- risparmio_eur_anno = 786428.5714285709
- co2_base_t_anno = 21666.66666666667
- co2_alt_gas_t_anno = 8666.66666666667
- co2_alt_el_t_anno = 4178.571428571429
- co2_alt_t_anno = 12845.238095238099
- co2_evitata_t_anno = 8821.428571428572
- crf = 0.09634228760924432
- quota_capex_eur_anno = 385369.1504369773
- lco_base_eur_t = 48.75
- lco_alt_eur_t = 44.739405790084064
- van = 4162859.6428834447
- tir = 18.023659827104836
- payback = 6
- prezzo_pareggio_eur_mwh = 157.051282051282
- verdetto = 'CONVIENTE'

Scomposizione: q_term = 1,3 x 2,7 x
0,2777777777777778 = 0,975 MWh/t;
Q_term = 100.000 x 0,975 = 97.500
MWh/anno; gas_base = 97.500 / 0,90 =
108.333,33 MWh/anno; C_base =
108.333,33 x 45 = 4.875.000 EUR/anno;
Q_pdc = 0,60 x 97.500 = 58.500
MWh/anno; E_el = 58.500 / 3,5 =
16.714,29 MWh/anno; gas_res = 0,40 x
97.500 / 0,90 = 43.333,33 MWh/anno;
C_alt_var = 43.333,33 x 45 +
16.714,29 x 110 = 1.950.000 +
1.838.571,43 = 3.788.571,43
EUR/anno; C_alt = 3.788.571,43 +
300.000 = 4.088.571,43 EUR/anno;
risparmio = 4.875.000 - 4.088.571,43
= 786.428,57 EUR/anno; CO2 base =
108.333,33 x 0,20 = 21.666,67 t/anno;
CO2 alt = 43.333,33 x 0,20 +
16.714,29 x 0,25 = 8.666,67 +
4.178,57 = 12.845,24 t/anno; CO2
evitata = 8.821,43 t/anno; CRF 0,05 x
1,05^15 / (1,05^15 - 1) =
0.09634228760924432; quota CAPEX
4.000.000 x 0,096342 = 385.369,15
EUR/anno; LCO base 4.875.000 /
100.000 = 48,75 EUR/t; LCO alt
(385.369,15 + 300.000) / 100.000 +
3.788.571,43 / 100.000 = 44,74
EUR/t; flussi: anno 0 -4.000.000,
anni 1-15 risparmio 786.428,57
(piatti); VAN -4.000.000 +
786.428,57 x 10,379658 (annuita'
15 anni al 5 %) = 4.162.859,64 EUR;
TIR circa 18,02 %; payback 6 anni
(il cumulato all'anno 5 e'
-67.857,14 EUR, all'anno 6 e'
718.571,43 EUR); prezzo elettrico di
pareggio (4.875.000 - 1.950.000 -
300.000) / 16.714,29 = 157,05
EUR/MWh; verdetto CONVIENTE perche'
VAN > 0.
NOTA: il CRF entra solo nel LCO,
mai nei flussi: il CAPEX compare una
sola volta, all'anno 0.
NOTA 2: in questo brief il risparmio
nullo o negativo NON e' degenere:
con prezzo elettrico 200 EUR/MWh il
risparmio e' -717.857,14 EUR/anno e
il caso resta calcolabile (valid=True,
VAN -11.451.111,66 EUR,
NON_CONVIENTE).
NOTA 3: la CO2 evitata puo' essere
negativa: con fattore elettrico 0,60
tCO2/MWh la CO2 evitata e'
2.971,43 t/anno (ancora positiva per
il mix demo); con fattore elettrico
1,00 tCO2/MWh la CO2 evitata diventa
-3.714,29 t/anno, pur restando il
caso economicamente CONVIENTE.
NOTA 4: il prezzo elettrico di
pareggio puo' essere negativo: con
O&M fisso 5.000.000 EUR/anno il
pareggio e' -124,15 EUR/MWh, perche'
il solo O&M fisso piu' il gas
residuo superano gia' il costo
baseline.
NOTA 5: il brief stimava C_alt_var
3.888.571,43 EUR/anno, C_alt
4.188.571,43 EUR/anno e risparmio
686.428,57 EUR/anno: il ricalcolo
indipendente da zero da' C_alt_var
3.788.571,43 EUR/anno (1.950.000 di
gas residuo + 1.838.571,43 di
elettricita'), C_alt 4.088.571,43
EUR/anno e risparmio 786.428,57
EUR/anno (la stima del brief era
sopra di 100.000 EUR sul costo
variabile). Il test usa i valori
ricalcolati, e la VAN diventa
4.162.859,64 EUR (non circa
3,13 milioni come stimato dal
brief).
NOTA 6: la quota PdC zero NON e'
degenere: con quota 0 il risparmio
e' -300.000 EUR/anno (solo O&M
fisso), la VAN -7.113.897,41 EUR e
il pareggio non e' definito
(E_el nulla).
"""

import ast
import math
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w757_helpers import (
    demo_calcoli,
    mh756_c_alt,
    mh756_c_alt_var,
    mh756_c_base,
    mh756_calcola,
    mh756_co2_alt,
    mh756_co2_base,
    mh756_co2_evitata,
    mh756_crf,
    mh756_csv,
    mh756_demo,
    mh756_e_el,
    mh756_eta,
    mh756_flussi,
    mh756_gas_base,
    mh756_gas_res,
    mh756_int_pos,
    mh756_lco_alt,
    mh756_lco_base,
    mh756_nneg,
    mh756_num,
    mh756_payback,
    mh756_pct_0_100,
    mh756_pct_wacc,
    mh756_pos,
    mh756_prezzo_pareggio,
    mh756_q_pdc,
    mh756_q_term_anno,
    mh756_q_term_per_t,
    mh756_quota_capex,
    mh756_risparmio,
    mh756_tir,
    mh756_valida,
    mh756_van,
    mh756_verdetto,
)


def _demo_kwargs():
    return dict(mh756_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh756_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh756_num(3, "x") == 3.0
    assert mh756_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh756_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh756_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh756_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh756_pos(0, "x")
    with pytest.raises(ValueError):
        mh756_pos(-1, "x")
    assert mh756_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh756_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh756_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh756_int_pos(0, "x")


def test_pct_0_100_limiti():
    assert mh756_pct_0_100(0, "x") == 0.0
    assert mh756_pct_0_100(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh756_pct_0_100(100.1, "x")
    with pytest.raises(ValueError):
        mh756_pct_0_100(-1, "x")


def test_pct_wacc_limiti():
    assert mh756_pct_wacc(0, "x") == 0.0
    assert mh756_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh756_pct_wacc(50.1, "x")


def test_eta_limiti():
    assert mh756_eta(1.0, "x") == 1.0
    assert mh756_eta(0.90, "x") == 0.90
    with pytest.raises(ValueError):
        mh756_eta(0, "x")
    with pytest.raises(ValueError):
        mh756_eta(-0.1, "x")
    with pytest.raises(ValueError):
        mh756_eta(1.01, "x")


# ---------------------------------------------------------------- fisica base
def test_q_term_per_t_e_anno():
    assert mh756_q_term_per_t(1.3, 2.7) == pytest.approx(0.975)
    assert mh756_q_term_per_t(1.0, 2.7) == pytest.approx(0.75)
    assert mh756_q_term_anno(100000, 0.975) == pytest.approx(97500.0)
    assert mh756_q_term_anno(100000, 0.0) == 0.0
    with pytest.raises(ValueError):
        mh756_q_term_per_t(0, 2.7)
    with pytest.raises(ValueError):
        mh756_q_term_per_t(1.3, 0)


def test_gas_base_e_c_base_e_co2_base():
    assert mh756_gas_base(97500.0, 0.90) == pytest.approx(108333.33333333334)
    assert mh756_gas_base(97500.0, 1.0) == 97500.0
    assert mh756_c_base(108333.33333333334, 45) == pytest.approx(4875000.0)
    assert mh756_co2_base(108333.33333333334, 0.20) == pytest.approx(
        21666.66666666667)
    with pytest.raises(ValueError):
        mh756_gas_base(97500.0, 0)
    with pytest.raises(ValueError):
        mh756_c_base(108333.33333333334, -1)


def test_q_pdc_e_e_el():
    assert mh756_q_pdc(97500.0, 60.0) == pytest.approx(58500.0)
    assert mh756_q_pdc(97500.0, 0) == 0.0
    assert mh756_q_pdc(97500.0, 100) == 97500.0
    assert mh756_e_el(58500.0, 3.5) == pytest.approx(16714.285714285717)
    assert mh756_e_el(58500.0, 0) is None
    assert mh756_e_el(58500.0, -1.0) is None
    assert mh756_e_el(0.0, 3.5) == 0.0
    with pytest.raises(ValueError):
        mh756_q_pdc(97500.0, 100.1)


def test_gas_res():
    assert mh756_gas_res(97500.0, 60.0, 0.90) == pytest.approx(
        43333.33333333334)
    assert mh756_gas_res(97500.0, 0, 0.90) == pytest.approx(108333.33333333334)
    assert mh756_gas_res(97500.0, 100, 0.90) == 0.0
    with pytest.raises(ValueError):
        mh756_gas_res(97500.0, 60.0, 0)


def test_c_alt_var_e_c_alt():
    assert mh756_c_alt_var(43333.33333333334, 45, 16714.285714285717,
                           110) == pytest.approx(3788571.428571429)
    assert mh756_c_alt_var(43333.33333333334, 45, 0.0, 110) == pytest.approx(
        1950000.0)
    assert mh756_c_alt(3788571.428571429, 300000) == pytest.approx(
        4088571.428571429)
    assert mh756_c_alt(3788571.428571429, 0) == pytest.approx(
        3788571.428571429)
    with pytest.raises(ValueError):
        mh756_c_alt_var(43333.33333333334, -1, 16714.285714285717, 110)


def test_risparmio_segno():
    assert mh756_risparmio(4875000.0, 4088571.428571429) == pytest.approx(
        786428.5714285709)
    assert mh756_risparmio(4875000.0, 4875000.0) == 0.0
    assert mh756_risparmio(4875000.0, 5000000.0) == -125000.0


def test_co2_alt_e_evitata_segno_libero():
    assert mh756_co2_alt(43333.33333333334, 0.20, 16714.285714285717,
                         0.25) == pytest.approx(12845.238095238099)
    assert mh756_co2_evitata(21666.66666666667,
                             12845.238095238099) == pytest.approx(
        8821.428571428572)
    assert mh756_co2_evitata(21666.66666666667,
                             21666.66666666667) == pytest.approx(0.0)
    assert mh756_co2_evitata(21666.66666666667,
                             25666.66666666667) == pytest.approx(
        -4000.0, abs=1e-6)


# ---------------------------------------------------------------- finanza base
def test_crf():
    assert mh756_crf(5.0, 15) == pytest.approx(0.09634228760924432)
    assert mh756_crf(0, 15) == pytest.approx(1.0 / 15.0)
    assert mh756_crf(5.0, 1) == pytest.approx(1.05)
    assert mh756_crf(5.0, 10) == pytest.approx(0.12950457496545661)


def test_quota_capex_e_lco():
    assert mh756_quota_capex(4000000, 0.09634228760924432) == pytest.approx(
        385369.1504369773)
    assert mh756_lco_base(4875000.0, 100000) == pytest.approx(48.75)
    assert mh756_lco_base(4875000.0, 0) is None
    assert mh756_lco_alt(4000000, 0.09634228760924432, 300000,
                         3788571.428571429, 100000) == pytest.approx(
        44.739405790084064)
    assert mh756_lco_alt(4000000, 0.09634228760924432, 300000,
                         3788571.428571429, 0) is None
    assert mh756_lco_alt(0, 0.09634228760924432, 300000,
                         3788571.428571429, 100000) == pytest.approx(
        40.88571428571429)


def test_prezzo_pareggio_formula_brief_negativo_e_none():
    assert mh756_prezzo_pareggio(4875000.0, 43333.33333333334, 45, 300000,
                                 16714.285714285717) == pytest.approx(
        157.051282051282)
    assert mh756_prezzo_pareggio(4875000.0, 43333.33333333334, 45, 5000000,
                                 16714.285714285717) == pytest.approx(
        -124.14529914529915)
    assert mh756_prezzo_pareggio(4875000.0, 43333.33333333334, 45, 2925000,
                                 16714.285714285717) == pytest.approx(
        0.0, abs=1e-9)
    assert mh756_prezzo_pareggio(4875000.0, 43333.33333333334, 45, 300000,
                                 0.0) is None
    assert mh756_prezzo_pareggio(4875000.0, 43333.33333333334, 45, 300000,
                                 None) is None
    assert mh756_prezzo_pareggio(4875000.0, 0.0, 45, 0,
                                 16714.285714285717) == pytest.approx(
        291.6666666666667)


def test_flussi_lunghezza_e_primo():
    fl = mh756_flussi(4000000, 786428.5714285709, 15)
    assert len(fl) == 16
    assert fl[0] == -4000000
    assert all(f == 786428.5714285709 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = demo_calcoli()
    assert bc["van"] == pytest.approx(4162859.6428834447)
    assert mh756_van([-4000000] + [786428.5714285709] * 15,
                     0) == pytest.approx(7796428.571428563)
    assert mh756_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo_e_conviente():
    bc = demo_calcoli()
    assert bc["tir"] == pytest.approx(18.023659827104836)
    assert mh756_tir([-4000000] + [786428.5714285709] * 15) == pytest.approx(
        0.18023659827104836)
    tir = mh756_tir([-4000000] + [786428.5714285709] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-4000000] + [786428.5714285709] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback():
    assert mh756_payback([-4000000] + [786428.5714285709] * 15) == 6
    assert mh756_payback([-4000000] + [800.0] * 15) is None
    assert mh756_payback([0] + [786428.5714285709] * 15) == 0
    assert mh756_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh756_verdetto(100.0, 4000000, 10.0) == "CONVIENTE"
    assert mh756_verdetto(-390000.0, 4000000, 10.0) == "MARGINALE"
    assert mh756_verdetto(-400000.0, 4000000, 10.0) == "MARGINALE"
    assert mh756_verdetto(-400000.01, 4000000, 10.0) == "NON_CONVIENTE"
    assert mh756_verdetto(-4162859.64, 4000000, 10.0) == "NON_CONVIENTE"
    assert mh756_verdetto(float("nan"), 4000000, 10.0) == "NON_CALCOLABILE"
    assert mh756_verdetto(0.0, 0, 10.0) == "MARGINALE"


def test_valida_demo_ok():
    v = mh756_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("produzione_t_anno", "100000"),
                       ("produzione_t_anno", float("nan")),
                       ("produzione_t_anno", float("inf")),
                       ("produzione_t_anno", True),
                       ("prezzo_el_eur_mwh", None)):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh756_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("produzione_t_anno", 0),
                          ("evap_t_acqua_per_t", 0),
                          ("evap_t_acqua_per_t", -0.5),
                          ("calore_gj_per_t_acqua", 0),
                          ("eta_caldaia", 0),
                          ("eta_caldaia", 1.01),
                          ("quota_pdc_pct", -1),
                          ("quota_pdc_pct", 100.1),
                          ("cop", 0), ("cop", -1),
                          ("prezzo_gas_eur_mwh", -1),
                          ("prezzo_el_eur_mwh", -1),
                          ("om_fisso_eur_anno", -100),
                          ("capex_pdc_eur", -1),
                          ("f_gas_t_per_mwh", -0.10),
                          ("f_el_t_per_mwh", -0.10),
                          ("wacc_pct", -0.1), ("wacc_pct", 50.1),
                          ("vita_anni", 0), ("vita_anni", 2.5),
                          ("tolleranza_pct", -1),
                          ("tolleranza_pct", 100.1)):
        d = _demo_kwargs()
        d[campo] = valore
        assert mh756_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"quota_pdc_pct": 0, "prezzo_gas_eur_mwh": 0,
              "prezzo_el_eur_mwh": 0, "om_fisso_eur_anno": 0,
              "capex_pdc_eur": 0, "f_gas_t_per_mwh": 0,
              "f_el_t_per_mwh": 0, "wacc_pct": 0,
              "tolleranza_pct": 0, "eta_caldaia": 1.0})
    assert mh756_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["quota_pdc_pct"] = 100
    assert mh756_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh756_demo()
    assert d["produzione_t_anno"] == 100000
    assert d["evap_t_acqua_per_t"] == 1.3
    assert d["calore_gj_per_t_acqua"] == 2.7
    assert d["eta_caldaia"] == 0.90
    assert d["quota_pdc_pct"] == 60.0
    assert d["cop"] == 3.5
    assert d["prezzo_gas_eur_mwh"] == 45
    assert d["prezzo_el_eur_mwh"] == 110
    assert d["om_fisso_eur_anno"] == 300000
    assert d["capex_pdc_eur"] == 4000000
    assert d["f_gas_t_per_mwh"] == 0.20
    assert d["f_el_t_per_mwh"] == 0.25
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    """Ogni _DEMO del test contro demo_calcoli():
    scarto relativo < 1e-9 (zero atteso:
    confronto assoluto)."""
    bc = demo_calcoli()
    attesi = {
        "q_term_mwh_per_t": 0.975,
        "q_term_mwh_anno": 97500.0,
        "gas_base_mwh_anno": 108333.33333333334,
        "c_base_eur_anno": 4875000.0,
        "q_pdc_mwh_anno": 58500.0,
        "e_el_mwh_anno": 16714.285714285717,
        "gas_res_mwh_anno": 43333.33333333334,
        "c_alt_var_eur_anno": 3788571.428571429,
        "c_alt_eur_anno": 4088571.428571429,
        "risparmio_eur_anno": 786428.5714285709,
        "co2_base_t_anno": 21666.66666666667,
        "co2_alt_t_anno": 12845.238095238099,
        "co2_evitata_t_anno": 8821.428571428572,
        "crf": 0.09634228760924432,
        "quota_capex_eur_anno": 385369.1504369773,
        "lco_base_eur_t": 48.75,
        "lco_alt_eur_t": 44.739405790084064,
        "van": 4162859.6428834447,
        "tir": 18.023659827104836,
        "prezzo_pareggio_eur_mwh": 157.051282051282,
    }
    for chiave, atteso in attesi.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert abs(got - atteso) / abs(atteso) < 1e-9, chiave
    assert bc["payback"] == 6
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_demo_calcoli_fisica():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["q_term_mwh_per_t"] == pytest.approx(0.975)
    assert bc["q_term_mwh_anno"] == pytest.approx(97500.0)
    assert bc["gas_base_mwh_anno"] == pytest.approx(108333.33333333334)
    assert bc["co2_evitata_t_anno"] == pytest.approx(8821.428571428572)


def test_demo_calcoli_economia():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] == 4875000.0
    assert bc["c_alt_var_eur_anno"] == pytest.approx(3788571.428571429)
    assert bc["c_alt_eur_anno"] == pytest.approx(4088571.428571429)
    assert bc["risparmio_eur_anno"] == pytest.approx(786428.5714285709)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(157.051282051282)


def test_demo_calcoli_finanza():
    bc = demo_calcoli()
    assert bc["crf"] == pytest.approx(0.09634228760924432)
    assert bc["quota_capex_eur_anno"] == pytest.approx(385369.1504369773)
    assert bc["lco_base_eur_t"] == pytest.approx(48.75)
    assert bc["lco_alt_eur_t"] == pytest.approx(44.739405790084064)
    assert bc["van"] == pytest.approx(4162859.6428834447)
    assert bc["tir"] == pytest.approx(18.023659827104836)
    assert bc["payback"] == 6
    assert bc["verdetto"] == "CONVIENTE"


def test_demo_flussi_e_cumulato():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -4000000
    assert len(bc["flussi"]) == 16
    assert all(f == 786428.5714285709 for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -4000000
    assert righe.iloc[5]["Cumulato (EUR)"] == pytest.approx(-67857.14285714552)
    assert righe.iloc[6]["Cumulato (EUR)"] == pytest.approx(718571.4285714254)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(7796428.571428563)
    assert righe.iloc[15]["Flusso (EUR/anno)"] == 786428.5714285709


def test_demo_tabella_righe():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Calore annuo (MWh/anno)"] == pytest.approx(97500.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(
        4088571.428571429)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(786428.5714285709)
    assert mappa["Payback (anni)"] == 6
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Prezzo elettrico di pareggio (EUR/MWh)"] == pytest.approx(
        157.051282051282)


def test_demo_coerenza_interna():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["c_alt_var_eur_anno"] + bc["om_fisso_eur_anno"] == \
        pytest.approx(bc["c_alt_eur_anno"])
    assert bc["gas_base_mwh_anno"] * bc["prezzo_gas_eur_mwh"] == \
        pytest.approx(bc["c_base_eur_anno"])
    assert bc["co2_base_t_anno"] - bc["co2_alt_t_anno"] == \
        pytest.approx(bc["co2_evitata_t_anno"])
    assert bc["capex_pdc_eur"] * bc["crf"] == pytest.approx(
        bc["quota_capex_eur_anno"])
    assert (bc["quota_capex_eur_anno"] + bc["om_fisso_eur_anno"]) / \
        bc["produzione_t_anno"] + bc["c_alt_var_eur_anno"] / \
        bc["produzione_t_anno"] == pytest.approx(bc["lco_alt_eur_t"])
    assert bc["c_base_eur_anno"] - bc["gas_res_mwh_anno"] * \
        bc["prezzo_gas_eur_mwh"] - bc["om_fisso_eur_anno"] == \
        pytest.approx(bc["prezzo_pareggio_eur_mwh"] *
                      bc["e_el_mwh_anno"])
    assert bc["produzione_t_anno"] * bc["evap_t_acqua_per_t"] * \
        bc["calore_gj_per_t_acqua"] * 0.2777777777777778 == \
        pytest.approx(bc["q_term_mwh_anno"])


def test_demo_crf_solo_nel_lco_non_nei_flussi():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -bc["capex_pdc_eur"]
    assert all(f == bc["risparmio_eur_anno"] for f in bc["flussi"][1:])
    assert bc["crf"] not in bc["flussi"]
    assert bc["quota_capex_eur_anno"] not in bc["flussi"]
    van_da_flussi = mh756_van(bc["flussi"], bc["wacc_pct"])
    assert van_da_flussi == pytest.approx(bc["van"])
    assert bc["lco_alt_eur_t"] == pytest.approx(
        (bc["capex_pdc_eur"] * bc["crf"] + bc["om_fisso_eur_anno"]) /
        bc["produzione_t_anno"] + bc["c_alt_var_eur_anno"] /
        bc["produzione_t_anno"])


def test_demo_contro_riconteggio_indipendente():
    prod, evap, cal, eta, quota, cop = 100000, 1.3, 2.7, 0.90, 60.0, 3.5
    pg, pe, om, cx = 45, 110, 300000, 4000000
    fg, fe, wacc, vita = 0.20, 0.25, 5.0, 15
    qpt = evap * cal * 0.2777777777777778
    qt = prod * qpt
    gb = qt / eta
    cb = gb * pg
    qp = quota / 100 * qt
    ee = qp / cop
    gr = (1 - quota / 100) * qt / eta
    cav = gr * pg + ee * pe
    ca = cav + om
    risp = cb - ca
    co2b = gb * fg
    co2a = gr * fg + ee * fe
    r = wacc / 100.0
    crf = r * (1 + r) ** vita / ((1 + r) ** vita - 1)
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    bc = demo_calcoli()
    assert bc["q_term_mwh_per_t"] == pytest.approx(qpt)
    assert bc["q_term_mwh_anno"] == pytest.approx(qt)
    assert bc["gas_base_mwh_anno"] == pytest.approx(gb)
    assert bc["c_base_eur_anno"] == pytest.approx(cb)
    assert bc["q_pdc_mwh_anno"] == pytest.approx(qp)
    assert bc["e_el_mwh_anno"] == pytest.approx(ee)
    assert bc["gas_res_mwh_anno"] == pytest.approx(gr)
    assert bc["c_alt_var_eur_anno"] == pytest.approx(cav)
    assert bc["c_alt_eur_anno"] == pytest.approx(ca)
    assert bc["risparmio_eur_anno"] == pytest.approx(risp)
    assert bc["co2_base_t_anno"] == pytest.approx(co2b)
    assert bc["co2_alt_t_anno"] == pytest.approx(co2a)
    assert bc["crf"] == pytest.approx(crf)
    assert bc["van"] == pytest.approx(van)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(
        (cb - gr * pg - om) / ee)


def test_demo_riconteggio_crf_van_payback_pareggio_a_mano():
    bc = demo_calcoli()
    r = 0.05
    annuita = (1 - (1 + r) ** -15) / r
    assert annuita == pytest.approx(10.379658038800514)
    assert bc["van"] == pytest.approx(-4000000 + 786428.5714285709 * annuita)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(
        (4875000.0 - 1950000.0 - 300000) / 16714.285714285717)
    assert bc["flussi"][0] + 15 * bc["flussi"][1] == pytest.approx(
        7796428.571428563)
    assert bc["flussi"][0] + 6 * bc["flussi"][1] == pytest.approx(
        718571.4285714254)


# ---------------------------------------------------------------- varianti
def test_variante_prezzo_el_alto_non_conviente():
    bc = _variante(prezzo_el_eur_mwh=200)
    assert bc["risparmio_eur_anno"] == pytest.approx(-717857.1428571437)
    assert bc["van"] == pytest.approx(-11451111.663122501)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(157.051282051282)
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_variante_prezzo_el_marginale():
    bc = _variante(prezzo_el_eur_mwh=135)
    assert bc["risparmio_eur_anno"] == pytest.approx(368571.42857142724)
    assert bc["van"] < 0.0
    assert abs(bc["van"]) <= 0.10 * 4000000
    assert bc["tir"] == pytest.approx(4.347920649990949, abs=1e-4)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"
    assert bc["valid"] is True


def test_variante_risparmio_azzerato_calcolabile():
    bc = _variante(prezzo_el_eur_mwh=157.051282051282)
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1.0)
    assert bc["van"] == pytest.approx(-4000000.0, abs=10.0)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(157.051282051282)
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_variante_quota_zero_calcolabile_non_degenere():
    bc = _variante(quota_pdc_pct=0)
    assert bc["valid"] is True
    assert bc["q_pdc_mwh_anno"] == 0.0
    assert bc["e_el_mwh_anno"] == 0.0
    assert bc["gas_res_mwh_anno"] == pytest.approx(108333.33333333334)
    assert bc["risparmio_eur_anno"] == -300000.0
    assert bc["van"] == pytest.approx(-7113897.411454178)
    assert bc["co2_evitata_t_anno"] == 0.0
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["lco_alt_eur_t"] == pytest.approx(55.60369150436977)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_quota_cento():
    bc = _variante(quota_pdc_pct=100)
    assert bc["q_pdc_mwh_anno"] == pytest.approx(97500.0)
    assert bc["e_el_mwh_anno"] == pytest.approx(27857.14285714286)
    assert bc["gas_res_mwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(1510714.285714285)
    assert bc["van"] == pytest.approx(11680697.679108528)
    assert bc["tir"] == pytest.approx(37.447931372056296, abs=1e-4)
    assert bc["payback"] == 3
    assert bc["co2_evitata_t_anno"] == pytest.approx(14702.380952380956)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(164.2307692307692)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_cop_basso_non_conviente():
    bc = _variante(cop=2.0)
    assert bc["e_el_mwh_anno"] == pytest.approx(29250.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-592500.0)
    assert bc["van"] == pytest.approx(-10149947.38762201)
    assert bc["co2_evitata_t_anno"] == pytest.approx(5687.5)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(89.74358974358972)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_cop_alto():
    bc = _variante(cop=5.0)
    assert bc["e_el_mwh_anno"] == pytest.approx(11700.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(1338000.0)
    assert bc["van"] == pytest.approx(9887982.45508562)
    assert bc["tir"] == pytest.approx(32.98510924891064, abs=1e-4)
    assert bc["payback"] == 3
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(224.35897435897428)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_co2_evitata_negativa_con_fattore_el_alto():
    bc = _variante(f_el_t_per_mwh=1.00)
    assert bc["co2_alt_t_anno"] == pytest.approx(25380.95238095238)
    assert bc["co2_evitata_t_anno"] == pytest.approx(-3714.2857142857)
    assert bc["co2_evitata_t_anno"] < 0.0
    assert bc["van"] == pytest.approx(4162859.6428834447)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_co2_evitata_zero():
    bc = _variante(f_el_t_per_mwh=0.80)
    assert bc["co2_alt_t_anno"] == pytest.approx(22038.09523809524)
    assert bc["co2_evitata_t_anno"] == pytest.approx(-371.4285714286)
    bc2 = _variante(f_gas_t_per_mwh=0.0, f_el_t_per_mwh=0.0)
    assert bc2["co2_evitata_t_anno"] == 0.0
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_pareggio_negativo():
    bc = _variante(om_fisso_eur_anno=5000000)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(-124.14529914529915)
    assert bc["prezzo_pareggio_eur_mwh"] < 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(-3913571.428571429)
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_variante_pareggio_zero():
    bc = _variante(om_fisso_eur_anno=2925000)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(0.0, abs=1e-9)
    assert bc["risparmio_eur_anno"] == pytest.approx(-1838571.428571429)


def test_variante_gas_basso_non_conviente():
    bc = _variante(prezzo_gas_eur_mwh=30)
    assert bc["c_base_eur_anno"] == pytest.approx(3250000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-188571.42857142864)
    assert bc["van"] == pytest.approx(-5957306.944342624)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_gas_alto():
    bc = _variante(prezzo_gas_eur_mwh=80)
    assert bc["c_base_eur_anno"] == pytest.approx(8666666.666666667)
    assert bc["risparmio_eur_anno"] == pytest.approx(3061428.571428572)
    assert bc["van"] == pytest.approx(27776581.679744296)
    assert bc["payback"] == 2
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero():
    bc = _variante(wacc_pct=0)
    assert bc["crf"] == pytest.approx(1.0 / 15.0)
    assert bc["quota_capex_eur_anno"] == pytest.approx(266666.6666666667)
    assert bc["lco_alt_eur_t"] == pytest.approx(43.55238095238096)
    assert bc["van"] == pytest.approx(7796428.571428563)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex_pdc_eur=0)
    assert bc["capex_pdc_eur"] == 0
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(8162859.642883446)
    assert bc["lco_alt_eur_t"] == pytest.approx(40.88571428571429)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_vita_dieci():
    bc = _variante(vita_anni=10)
    assert len(bc["flussi"]) == 11
    assert bc["crf"] == pytest.approx(0.12950457496545661)
    assert bc["van"] == pytest.approx(2072592.969308908)
    assert bc["tir"] == pytest.approx(14.65083889199576, abs=1e-4)
    assert bc["payback"] == 6
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_produzione_doppia():
    bc = _variante(produzione_t_anno=200000)
    assert bc["q_term_mwh_anno"] == pytest.approx(195000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(1872857.1428571418)
    assert bc["co2_evitata_t_anno"] == pytest.approx(17642.857142857145)
    assert bc["van"] == pytest.approx(15439616.697221063)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(166.02564102564097)
    assert bc["payback"] == 3
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_eta_uno():
    bc = _variante(eta_caldaia=1.0)
    assert bc["gas_base_mwh_anno"] == pytest.approx(97500.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(493928.5714285718)
    assert bc["van"] == pytest.approx(1126809.666715631)
    assert bc["tir"] == pytest.approx(8.92117038201178, abs=1e-4)
    assert bc["payback"] == 9
    assert bc["lco_base_eur_t"] == pytest.approx(43.875)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_prezzo_el_nullo():
    bc = _variante(prezzo_el_eur_mwh=0.0)
    assert bc["valid"] is True
    assert bc["c_alt_var_eur_anno"] == pytest.approx(1950000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(2250000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(2625000.0)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_input_nulli_calcolabile_non_degenere():
    bc = _variante(prezzo_el_eur_mwh=0.0, prezzo_gas_eur_mwh=0,
                   om_fisso_eur_anno=0)
    assert bc["valid"] is True
    assert bc["c_base_eur_anno"] == 0.0
    assert bc["c_alt_eur_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == 0.0
    assert bc["van"] == -4000000.0
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_pareggio_negativo_demo_no():
    bc = demo_calcoli()
    assert bc["prezzo_pareggio_eur_mwh"] > 0.0
    assert bc["valid"] is True
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["risparmio_eur_anno"] > 0.0


# ---------------------------------------------------------------- degenere
def test_degenere_produzione_zero():
    bc = _variante(produzione_t_anno=0)
    assert bc["valid"] is False
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"] == []
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["lco_base_eur_t"] is None
    assert bc["lco_alt_eur_t"] is None
    assert bc["errore"]


def test_degenere_evap_calore_cop_vita():
    for kw in ({"evap_t_acqua_per_t": 0}, {"evap_t_acqua_per_t": -0.5},
               {"calore_gj_per_t_acqua": 0},
               {"cop": 0}, {"cop": -1},
               {"produzione_t_anno": 0},
               {"produzione_t_anno": -1},
               {"vita_anni": 0}, {"vita_anni": 2.5}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_eta_wacc_tolleranza_prezzi_negativi():
    for kw in ({"eta_caldaia": 0}, {"eta_caldaia": 1.01},
               {"wacc_pct": -1}, {"wacc_pct": 60},
               {"tolleranza_pct": -1}, {"tolleranza_pct": 101},
               {"quota_pdc_pct": -1}, {"quota_pdc_pct": 101},
               {"prezzo_gas_eur_mwh": -1},
               {"prezzo_el_eur_mwh": -1},
               {"om_fisso_eur_anno": -100},
               {"capex_pdc_eur": -1}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_stringa_nan_inf():
    for kw in ({"produzione_t_anno": "100000"},
               {"produzione_t_anno": float("nan")},
               {"prezzo_el_eur_mwh": float("inf")},
               {"capex_pdc_eur": True}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_neutro_campi():
    bc = _variante(produzione_t_anno=0)
    assert bc["q_term_mwh_anno"] == 0.0
    assert bc["gas_base_mwh_anno"] == 0.0
    assert bc["c_base_eur_anno"] == 0.0
    assert bc["c_alt_eur_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == 0.0
    assert bc["van"] == 0.0
    assert list(bc["df_flussi"].columns) == [
        "Anno", "Flusso (EUR/anno)", "Cumulato (EUR)"]
    assert list(bc["df_tabella"].columns) == ["Voce", "Valore"]


def test_pareggio_none_quando_e_el_zero():
    assert mh756_prezzo_pareggio(4875000.0, 43333.33333333334, 45, 300000,
                                 0.0) is None
    assert mh756_prezzo_pareggio(4875000.0, 43333.33333333334, 45, 300000,
                                 None) is None
    assert mh756_lco_base(4875000.0, 0) is None
    assert mh756_e_el(58500.0, 0) is None


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = demo_calcoli()
    testo = mh756_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert "q_term_mwh_anno;97500.0" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "prezzo_pareggio_eur_mwh" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = demo_calcoli()
    testo = mh756_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"quota_capex_eur_anno;{bc['quota_capex_eur_anno']}" in testo
    assert f"q_term_mwh_anno;{bc['q_term_mwh_anno']}" in testo


def test_csv_degenere_solo_zeri():
    bc = _variante(produzione_t_anno=0)
    testo = mh756_csv(bc, _demo_kwargs())
    assert "van_eur;0.0" in testo
    assert "q_term_mwh_anno;0.0" in testo
    assert "verdetto;NON_CALCOLABILE" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = demo_calcoli()
    testo = mh756_csv(bc, _demo_kwargs())
    for chiave in _demo_kwargs():
        assert f"{chiave};" in testo


def test_calcola_non_sollevela_per_input_numerici():
    bc = _variante(prezzo_el_eur_mwh=0.0, prezzo_gas_eur_mwh=0,
                   om_fisso_eur_anno=0, f_gas_t_per_mwh=0,
                   f_el_t_per_mwh=0)
    assert bc["valid"] is True
    assert bc["c_base_eur_anno"] == 0.0
    assert bc["c_alt_eur_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == 0.0


def test_monotonia_prezzo_el():
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(prezzo_el_eur_mwh=120)["risparmio_eur_anno"]
    basso = _variante(prezzo_el_eur_mwh=100)["risparmio_eur_anno"]
    assert basso > base > alto
    assert basso - base == pytest.approx(167142.857142857)
    assert base - alto == pytest.approx(167142.857142857)


def test_monotonia_quota_pdc():
    base = demo_calcoli()["risparmio_eur_anno"]
    alta = _variante(quota_pdc_pct=80)["risparmio_eur_anno"]
    bassa = _variante(quota_pdc_pct=40)["risparmio_eur_anno"]
    assert alta > base > bassa


def test_demo_deterministica_due_chiamate():
    a = demo_calcoli()
    b = demo_calcoli()
    assert a["van"] == b["van"]
    assert a["flussi"] == b["flussi"]
    assert a["tir"] == b["tir"]


def test_demo_chiavi_attese():
    assert set(mh756_demo().keys()) == {
        "produzione_t_anno", "evap_t_acqua_per_t",
        "calore_gj_per_t_acqua", "eta_caldaia",
        "quota_pdc_pct", "cop",
        "prezzo_gas_eur_mwh", "prezzo_el_eur_mwh",
        "om_fisso_eur_anno", "capex_pdc_eur",
        "f_gas_t_per_mwh", "f_el_t_per_mwh",
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
    ast.parse(_leggi("w757_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w757_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab756:")


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    # token vietati costruiti per concatenazione, cosi' questo
    # stesso file non li contiene come sottostringhe contigue.
    src = _leggi("w757_helpers.py")
    vietati = ["mh" + "75" + "5", "st" + "75" + "5",
               "tab" + "75" + "5", "w" + "75" + "6",
               "mh" + "75" + "4", "tab" + "75" + "4"]
    assert "streamlit" not in src
    assert all(t not in src for t in vietati)
    assert "arco " + "elettrico" not in src
    assert "BF-" + "BOF" not in src


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w757_ui.py")
    vietati = ["mh" + "75" + "5", "st" + "75" + "5",
               "tab" + "75" + "5", "w" + "75" + "6",
               "mh" + "75" + "4", "tab" + "75" + "4"]
    assert all(t not in src for t in vietati)
    assert "arco " + "elettrico" not in src
    assert "BF-" + "BOF" not in src
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st756_") for c in chiavi)
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
    src = _leggi("w757_test.py")
    vietati = ["mh" + "75" + "5", "st" + "75" + "5",
               "tab" + "75" + "5", "w" + "75" + "6",
               "mh" + "75" + "4", "tab" + "75" + "4"]
    assert all(t not in src for t in vietati)
    assert "arco " + "elettrico" not in src
    assert "BF-" + "BOF" not in src


def test_ui_chiavi_demo_coerenti():
    """Ogni _def756[...] letto dalla UI esiste nel dict demo:
    sweep anti-KeyError a render (lezione dello sweep chiavi demo vs UI)."""
    src = _leggi("w757_ui.py")
    usate = set(re.findall(r'_def756\["([^"]+)"\]', src))
    assert usate
    assert usate <= set(mh756_demo().keys())


def test_ui_riferisce_solo_helper_nuovi():
    src = _leggi("w757_ui.py")
    usati = set(re.findall(r'\b(mh\d+_\w+)\b', src))
    assert usati
    assert all(u.startswith("mh756_") for u in usati)


@pytest.mark.parametrize("wacc,vita,atteso", [
    (5.0, 15, 0.09634228760924432),
    (0, 15, 1.0 / 15.0),
    (10.0, 10, 0.16274539488251152),
    (5.0, 1, 1.05),
    (50.0, 5, 0.5758293838862559),
])
def test_crf_parametrizzato(wacc, vita, atteso):
    assert mh756_crf(wacc, vita) == pytest.approx(atteso)


@pytest.mark.parametrize("campo,valore", [
    ("produzione_t_anno", 0), ("produzione_t_anno", -3),
    ("evap_t_acqua_per_t", 0), ("evap_t_acqua_per_t", -0.5),
    ("calore_gj_per_t_acqua", 0),
    ("eta_caldaia", 0), ("eta_caldaia", 1.01),
    ("quota_pdc_pct", -1), ("quota_pdc_pct", 100.1),
    ("cop", 0), ("cop", -1),
    ("prezzo_gas_eur_mwh", -1),
    ("prezzo_el_eur_mwh", -1),
    ("om_fisso_eur_anno", -100),
    ("capex_pdc_eur", -1),
    ("f_gas_t_per_mwh", -0.10), ("f_el_t_per_mwh", -0.10),
    ("wacc_pct", -0.1), ("wacc_pct", 50.1),
    ("vita_anni", -1), ("vita_anni", 2.5),
    ("tolleranza_pct", -1), ("tolleranza_pct", 100.1),
])
def test_valida_rifiuta_singoli_campi(campo, valore):
    d = _demo_kwargs()
    d[campo] = valore
    assert mh756_valida(**d)["valido"] is False


def test_df_tabella_valori_demo_selezionati():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Produzione (t/anno)"] == 100000.0
    assert mappa["Calore annuo (MWh/anno)"] == pytest.approx(97500.0)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(786428.5714285709)
    assert mappa["Payback (anni)"] == 6
    assert mappa["Verdetto"] == "CONVIENTE"


def test_lco_alt_minore_di_lco_base_demo():
    bc = demo_calcoli()
    assert bc["lco_alt_eur_t"] < bc["lco_base_eur_t"]
    assert bc["lco_base_eur_t"] - bc["lco_alt_eur_t"] == pytest.approx(
        4.010594209915936)
