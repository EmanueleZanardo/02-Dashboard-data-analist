"""Test tab758 "Caseificio: bollire il
latte con calore recuperato e pompa
di calore batte la caldaia a gas?"

Nuova tab tab758 (pastorizzazione latte,
w759). Business case deterministico
della pastorizzazione del latte in un
caseificio: il latte va bollito
(calore per litri di latte) e il calore
puo' arrivare dalla caldaia a gas
(baseline, tutto il calore lordo,
senza recupero) oppure in parte dal
calore recuperato dal raffreddamento
del latte e in parte da una pompa di
calore ad alta temperatura che copre
una quota del calore netto, con il
resto che resta a gas.
Q_lordo = produzione x calore / 1000;
Q_rec = quota_recupero / 100 x Q_lordo;
Q_netto = Q_lordo - Q_rec;
gas_base = Q_lordo / eta_caldaia;
C_base = gas_base x p_gas;
co2_base = gas_base x f_gas;
Q_pdc = quota_pdc / 100 x Q_netto;
E_el = Q_pdc / COP; gas_res =
(1 - quota_pdc / 100) x Q_netto /
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
cartiera (li' si essicca carta,
senza latte e senza recupero dal
rigenerazione del pastorizzatore), dalla
caldaia a elettrodi
generica (li' il calore viene da
elettrodi, senza processo latte e
senza quota di recupero) e dal
recupero calore generico (li' il
calore recuperato va a un uso
generico, senza pastorizzazione latte e
senza pompa di calore ad alta
temperatura sul calore netto).

Demo calcolata eseguendo demo_calcoli()
(e ricontrollata a mano, riga per riga):
produzione 50.000.000 L/anno, calore
60 kWh/1000L, rendimento caldaia 0,90,
quota recupero 40 %, quota PdC 70 %,
COP 3,0, prezzo gas 45 EUR/MWh,
prezzo elettrico 110 EUR/MWh, O&M
fisso 30.000 EUR/anno, CAPEX
400.000 EUR, fattore gas 0,20
tCO2/MWh e fattore elettrico 0,25
tCO2/MWh, WACC 5 %, vita 15 anni,
tolleranza 10 % del CAPEX.

- q_lordo_mwh_anno = 3000.0
- q_rec_mwh_anno = 1200.0
- q_netto_mwh_anno = 1800.0
- gas_base_mwh_anno = 3333.333333333333
- c_base_eur_anno = 150000.0
- q_pdc_mwh_anno = 1260.0
- e_el_mwh_anno = 420.0
- gas_res_mwh_anno = 600.0000000000001
- c_alt_var_eur_anno = 73200.0
- c_alt_eur_anno = 103200.0
- risparmio_eur_anno = 46800.0
- co2_base_t_anno = 666.6666666666666
- co2_alt_gas_t_anno = 120.00000000000003
- co2_alt_el_t_anno = 105.0
- co2_alt_t_anno = 225.00000000000003
- co2_evitata_t_anno = 441.66666666666663
- crf = 0.09634228760924432
- quota_capex_eur_anno = 38536.91504369773
- lco_base_eur_L = 0.003
- lco_alt_eur_L = 0.0028347383008739545
- van = 85767.99618685164
- tir = 8.023886934285711
- payback = 9
- prezzo_pareggio_eur_mwh = 221.42857142857142
- verdetto = 'CONVIENTE'

Scomposizione: Q_lordo = 50.000.000 x 60 /
1000000 = 3.000 MWh/anno; Q_rec = 0,40 x
3.000 = 1.200 MWh/anno; Q_netto =
3.000 - 1.200 = 1.800 MWh/anno;
gas_base = 3.000 / 0,90 = 3.333,33
MWh/anno; C_base = 3.333,33 x 45 =
150.000 EUR/anno; Q_pdc = 0,70 x
1.800 = 1.260 MWh/anno; E_el = 1.260 /
3,0 = 420 MWh/anno; gas_res =
0,30 x 1.800 / 0,90 = 600 MWh/anno;
C_alt_var = 600 x 45 + 420 x 110
= 27.000 + 46.200 = 73.200
EUR/anno; C_alt = 73.200 + 30.000 =
103.200 EUR/anno; risparmio = 150.000
- 103.200 = 46.800 EUR/anno; CO2 base
= 3.333,33 x 0,20 = 666,67 t/anno;
CO2 alt = 600 x 0,20 + 420 x
0,25 = 120 + 105 = 225 t/anno;
CO2 evitata = 441,67 t/anno; CRF 0,05
x 1,05^15 / (1,05^15 - 1) =
0.09634228760924432; quota CAPEX
400.000 x 0,096342 = 38.536,92
EUR/anno; LCO base 150.000 / 50.000.000 =
0,0030 EUR/L; LCO alt (38.536,92 +
30.000) / 50.000.000 + 73.200 / 50.000.000 =
0,0028 EUR/L; flussi: anno 0
-400.000, anni 1-15 risparmio
46.800 (piatti); VAN -400.000 +
46.800 x 10,379658 (annuita' 15 anni
al 5 %) = 85.767,99 EUR; TIR 8,02 %;
payback 9 anni (il cumulato all'anno
8 e' -25.600 EUR, all'anno 9 e'
21.200 EUR); prezzo elettrico di
pareggio (150.000 - 27.000 - 30.000) /
420 = 221,43 EUR/MWh; verdetto
CONVIENTE perche' VAN > 0.
NOTA: il CRF entra solo nel LCO,
mai nei flussi: il CAPEX compare una
sola volta, all'anno 0.
NOTA 2: in questo brief il risparmio
nullo o negativo NON e' degenere:
con prezzo gas 30 EUR/MWh il
risparmio e' 5.800 EUR/anno e il
caso resta calcolabile (valid=True,
VAN -339.797,98 EUR, NON_CONVIENTE).
NOTA 3: la CO2 evitata puo' essere
negativa: con fattore elettrico 1,50
tCO2/MWh la CO2 evitata e'
-83,33 t/anno, pur restando il caso
calcolabile.
NOTA 4: il prezzo elettrico di
pareggio puo' essere negativo: con
O&M fisso 5.000.000 EUR/anno il
pareggio e' -11.611,90 EUR/MWh,
perche' il solo O&M fisso piu' il
gas residuo superano gia' il costo
baseline (il caso demo ha pareggio
positivo, 221,43 EUR/MWh).
NOTA 5: la quota PdC zero NON e'
degenere: con quota 0 il risparmio
e' 30.000 EUR/anno, la VAN
-88.610,26 EUR e il pareggio non
e' definito (E_el nulla).
NOTA 6: il calore netto nullo (quota
recupero 100 %) NON e' degenere:
il risparmio e' 120.000 EUR/anno
(150.000 - 30.000 di solo O&M fisso)
e la VAN 845.558,96 EUR, e il
pareggio non e' definito.
"""

import ast
import math
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w759_helpers import (
    demo_calcoli,
    mh758_c_alt,
    mh758_c_alt_var,
    mh758_c_base,
    mh758_calcola,
    mh758_co2_alt,
    mh758_co2_base,
    mh758_co2_evitata,
    mh758_crf,
    mh758_csv,
    mh758_demo,
    mh758_e_el,
    mh758_eta,
    mh758_flussi,
    mh758_gas_base,
    mh758_gas_res,
    mh758_int_pos,
    mh758_lco_alt,
    mh758_lco_base,
    mh758_nneg,
    mh758_num,
    mh758_payback,
    mh758_pct_0_100,
    mh758_pct_wacc,
    mh758_pos,
    mh758_prezzo_pareggio,
    mh758_q_lordo,
    mh758_q_netto,
    mh758_q_pdc,
    mh758_q_rec,
    mh758_quota_capex,
    mh758_risparmio,
    mh758_tir,
    mh758_valida,
    mh758_van,
    mh758_verdetto,
)


def _demo_kwargs():
    return dict(mh758_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh758_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh758_num(3, "x") == 3.0
    assert mh758_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh758_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh758_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh758_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh758_pos(0, "x")
    with pytest.raises(ValueError):
        mh758_pos(-1, "x")
    assert mh758_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh758_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh758_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh758_int_pos(0, "x")


def test_pct_0_100_limiti():
    assert mh758_pct_0_100(0, "x") == 0.0
    assert mh758_pct_0_100(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh758_pct_0_100(100.1, "x")
    with pytest.raises(ValueError):
        mh758_pct_0_100(-1, "x")


def test_pct_wacc_limiti():
    assert mh758_pct_wacc(0, "x") == 0.0
    assert mh758_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh758_pct_wacc(50.1, "x")


def test_eta_limiti():
    assert mh758_eta(1.0, "x") == 1.0
    assert mh758_eta(0.90, "x") == 0.90
    with pytest.raises(ValueError):
        mh758_eta(0, "x")
    with pytest.raises(ValueError):
        mh758_eta(-0.1, "x")
    with pytest.raises(ValueError):
        mh758_eta(1.01, "x")


# ---------------------------------------------------------------- fisica base
def test_q_lordo_rec_netto():
    assert mh758_q_lordo(50000000, 60) == pytest.approx(3000.0)
    assert mh758_q_lordo(50000000, 0) == 0.0
    assert mh758_q_rec(3000.0, 40.0) == pytest.approx(1200.0)
    assert mh758_q_rec(3000.0, 0) == 0.0
    assert mh758_q_rec(3000.0, 100) == 3000.0
    assert mh758_q_netto(3000.0, 1200.0) == pytest.approx(1800.0)
    assert mh758_q_netto(3000.0, 3000.0) == 0.0
    with pytest.raises(ValueError):
        mh758_q_rec(3000.0, 100.1)
    with pytest.raises(ValueError):
        mh758_q_lordo(50000000, -1)


def test_gas_base_e_c_base_e_co2_base():
    assert mh758_gas_base(3000.0, 0.90) == pytest.approx(3333.333333333333)
    assert mh758_gas_base(3000.0, 1.0) == 3000.0
    assert mh758_c_base(3333.333333333333, 45) == pytest.approx(150000.0)
    assert mh758_co2_base(3333.333333333333, 0.20) == pytest.approx(
        666.6666666666666)
    with pytest.raises(ValueError):
        mh758_gas_base(3000.0, 0)
    with pytest.raises(ValueError):
        mh758_c_base(3333.333333333333, -1)


def test_q_pdc_e_e_el():
    assert mh758_q_pdc(1800.0, 70.0) == pytest.approx(1260.0)
    assert mh758_q_pdc(1800.0, 0) == 0.0
    assert mh758_q_pdc(1800.0, 100) == 1800.0
    assert mh758_e_el(1260.0, 3.0) == pytest.approx(420.0)
    assert mh758_e_el(1260.0, 0) is None
    assert mh758_e_el(1260.0, -1.0) is None
    assert mh758_e_el(0.0, 3.0) == 0.0
    with pytest.raises(ValueError):
        mh758_q_pdc(1800.0, 100.1)


def test_gas_res():
    assert mh758_gas_res(1800.0, 70.0, 0.90) == pytest.approx(600.0)
    assert mh758_gas_res(1800.0, 0, 0.90) == pytest.approx(2000.0)
    assert mh758_gas_res(1800.0, 100, 0.90) == 0.0
    with pytest.raises(ValueError):
        mh758_gas_res(1800.0, 70.0, 0)


def test_c_alt_var_e_c_alt():
    assert mh758_c_alt_var(600.0, 45, 420.0,
                           110) == pytest.approx(73200.0)
    assert mh758_c_alt_var(600.0, 45, 0.0, 110) == pytest.approx(27000.0)
    assert mh758_c_alt(73200.0, 30000) == pytest.approx(103200.0)
    assert mh758_c_alt(73200.0, 0) == pytest.approx(73200.0)
    with pytest.raises(ValueError):
        mh758_c_alt_var(600.0, -1, 420.0, 110)


def test_risparmio_segno():
    assert mh758_risparmio(150000.0, 103200.0) == pytest.approx(46800.0)
    assert mh758_risparmio(150000.0, 150000.0) == 0.0
    assert mh758_risparmio(150000.0, 100000.0) == 50000.0


def test_co2_alt_e_evitata_segno_libero():
    assert mh758_co2_alt(600.0, 0.20, 420.0,
                         0.25) == pytest.approx(225.0)
    assert mh758_co2_evitata(666.6666666666666,
                             225.0) == pytest.approx(
        441.66666666666663)
    assert mh758_co2_evitata(666.6666666666666,
                             666.6666666666666) == pytest.approx(0.0)
    assert mh758_co2_evitata(666.6666666666666,
                             1266.6666666666666) == pytest.approx(
        -600.0, abs=1e-6)


# ---------------------------------------------------------------- finanza base
def test_crf():
    assert mh758_crf(5.0, 15) == pytest.approx(0.09634228760924432)
    assert mh758_crf(0, 15) == pytest.approx(1.0 / 15.0)
    assert mh758_crf(5.0, 1) == pytest.approx(1.05)
    assert mh758_crf(5.0, 10) == pytest.approx(0.12950457496545661)


def test_quota_capex_e_lco():
    assert mh758_quota_capex(400000, 0.09634228760924432) == pytest.approx(
        38536.91504369773)
    assert mh758_lco_base(150000.0, 50000000) == pytest.approx(0.003)
    assert mh758_lco_base(150000.0, 0) is None
    assert mh758_lco_alt(400000, 0.09634228760924432, 30000,
                         73200.0, 50000000) == pytest.approx(
        0.0028347383008739545)
    assert mh758_lco_alt(400000, 0.09634228760924432, 30000,
                         73200.0, 0) is None
    assert mh758_lco_alt(0, 0.09634228760924432, 30000,
                         73200.0, 50000000) == pytest.approx(0.002064)


def test_prezzo_pareggio_formula_brief_negativo_e_none():
    assert mh758_prezzo_pareggio(150000.0, 600.0, 45, 30000,
                                 420.0) == pytest.approx(
        221.42857142857142)
    assert mh758_prezzo_pareggio(150000.0, 600.0, 45, 123000,
                                 420.0) == pytest.approx(0.0, abs=1e-9)
    assert mh758_prezzo_pareggio(150000.0, 600.0, 45, 30000,
                                 0.0) is None
    assert mh758_prezzo_pareggio(150000.0, 600.0, 45, 30000,
                                 None) is None
    assert mh758_prezzo_pareggio(150000.0, 0.0, 45, 0,
                                 420.0) == pytest.approx(
        357.14285714285714)


def test_flussi_lunghezza_e_primo():
    fl = mh758_flussi(400000, 46800.0, 15)
    assert len(fl) == 16
    assert fl[0] == -400000
    assert all(f == 46800.0 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = demo_calcoli()
    assert bc["van"] == pytest.approx(85767.99618685164)
    assert mh758_van([-400000] + [46800.0] * 15,
                     0) == pytest.approx(302000.0)
    assert mh758_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo_e_conviente():
    bc = demo_calcoli()
    assert bc["tir"] == pytest.approx(8.023886934285711)
    assert mh758_tir([-400000] + [46800.0] * 15) == pytest.approx(
        0.08023886934285711)
    tir = mh758_tir([-400000] + [46800.0] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-400000] + [46800.0] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback():
    assert mh758_payback([-400000] + [46800.0] * 15) == 9
    assert mh758_payback([-400000] + [-1000.0] * 15) is None
    assert mh758_payback([0] + [46800.0] * 15) == 0
    assert mh758_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh758_verdetto(100.0, 1200000, 10.0) == "CONVIENTE"
    assert mh758_verdetto(-119000.0, 1200000, 10.0) == "MARGINALE"
    assert mh758_verdetto(-120000.0, 1200000, 10.0) == "MARGINALE"
    assert mh758_verdetto(-120000.01, 1200000, 10.0) == "NON_CONVIENTE"
    assert mh758_verdetto(-791596.89, 1200000, 10.0) == "NON_CONVIENTE"
    assert mh758_verdetto(float("nan"), 1200000, 10.0) == "NON_CALCOLABILE"
    assert mh758_verdetto(0.0, 0, 10.0) == "MARGINALE"


def test_valida_demo_ok():
    v = mh758_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("produzione_L_anno", "300000"),
                       ("produzione_L_anno", float("nan")),
                       ("produzione_L_anno", float("inf")),
                       ("produzione_L_anno", True),
                       ("prezzo_el_eur_mwh", None)):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh758_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("produzione_L_anno", 0),
                          ("calore_kWh_per_1000L", 0),
                          ("calore_kWh_per_1000L", -5),
                          ("eta_caldaia", 0),
                          ("eta_caldaia", 1.01),
                          ("quota_recupero_pct", -1),
                          ("quota_recupero_pct", 100.1),
                          ("quota_pdc_pct", -1),
                          ("quota_pdc_pct", 100.1),
                          ("cop", 0), ("cop", -1),
                          ("prezzo_gas_eur_mwh", -1),
                          ("prezzo_el_eur_mwh", -1),
                          ("om_fisso_eur_anno", -100),
                          ("capex_eur", -1),
                          ("f_gas_t_per_mwh", -0.10),
                          ("f_el_t_per_mwh", -0.10),
                          ("wacc_pct", -0.1), ("wacc_pct", 50.1),
                          ("vita_anni", 0), ("vita_anni", 2.5),
                          ("tolleranza_pct", -1),
                          ("tolleranza_pct", 100.1)):
        d = _demo_kwargs()
        d[campo] = valore
        assert mh758_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"quota_recupero_pct": 0, "quota_pdc_pct": 0,
              "prezzo_gas_eur_mwh": 0,
              "prezzo_el_eur_mwh": 0, "om_fisso_eur_anno": 0,
              "capex_eur": 0, "f_gas_t_per_mwh": 0,
              "f_el_t_per_mwh": 0, "wacc_pct": 0,
              "tolleranza_pct": 0, "eta_caldaia": 1.0})
    assert mh758_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["quota_pdc_pct"] = 100
    d["quota_recupero_pct"] = 100
    assert mh758_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh758_demo()
    assert d["produzione_L_anno"] == 50000000
    assert d["calore_kWh_per_1000L"] == 60
    assert d["eta_caldaia"] == 0.90
    assert d["quota_recupero_pct"] == 40.0
    assert d["quota_pdc_pct"] == 70.0
    assert d["cop"] == 3.0
    assert d["prezzo_gas_eur_mwh"] == 45
    assert d["prezzo_el_eur_mwh"] == 110
    assert d["om_fisso_eur_anno"] == 30000
    assert d["capex_eur"] == 400000
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
        "q_lordo_mwh_anno": 3000.0,
        "q_rec_mwh_anno": 1200.0,
        "q_netto_mwh_anno": 1800.0,
        "gas_base_mwh_anno": 3333.333333333333,
        "c_base_eur_anno": 150000.0,
        "q_pdc_mwh_anno": 1260.0,
        "e_el_mwh_anno": 420.0,
        "gas_res_mwh_anno": 600.0,
        "c_alt_var_eur_anno": 73200.0,
        "c_alt_eur_anno": 103200.0,
        "risparmio_eur_anno": 46800.0,
        "co2_base_t_anno": 666.6666666666666,
        "co2_alt_t_anno": 225.0,
        "co2_evitata_t_anno": 441.66666666666663,
        "crf": 0.09634228760924432,
        "quota_capex_eur_anno": 38536.91504369773,
        "lco_base_eur_L": 0.003,
        "lco_alt_eur_L": 0.0028347383008739545,
        "van": 85767.99618685164,
        "tir": 8.023886934285711,
        "prezzo_pareggio_eur_mwh": 221.42857142857142,
    }
    for chiave, atteso in attesi.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert abs(got - atteso) / abs(atteso) < 1e-9, chiave
    assert bc["payback"] == 9
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_demo_calcoli_fisica():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["q_lordo_mwh_anno"] == pytest.approx(3000.0)
    assert bc["q_rec_mwh_anno"] == pytest.approx(1200.0)
    assert bc["q_netto_mwh_anno"] == pytest.approx(1800.0)
    assert bc["gas_base_mwh_anno"] == pytest.approx(3333.333333333333)
    assert bc["co2_evitata_t_anno"] == pytest.approx(441.66666666666663)


def test_demo_calcoli_economia():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] == 150000.0
    assert bc["c_alt_var_eur_anno"] == pytest.approx(73200.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(103200.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(46800.0)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(221.42857142857142)


def test_demo_calcoli_finanza():
    bc = demo_calcoli()
    assert bc["crf"] == pytest.approx(0.09634228760924432)
    assert bc["quota_capex_eur_anno"] == pytest.approx(38536.91504369773)
    assert bc["lco_base_eur_L"] == pytest.approx(0.003)
    assert bc["lco_alt_eur_L"] == pytest.approx(0.0028347383008739545)
    assert bc["van"] == pytest.approx(85767.99618685164)
    assert bc["tir"] == pytest.approx(8.023886934285711)
    assert bc["payback"] == 9
    assert bc["verdetto"] == "CONVIENTE"


def test_demo_flussi_e_cumulato():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -400000
    assert len(bc["flussi"]) == 16
    assert all(f == 46800.0 for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -400000
    assert righe.iloc[5]["Cumulato (EUR)"] == pytest.approx(-166000.0)
    assert righe.iloc[8]["Cumulato (EUR)"] == pytest.approx(-25600.0)
    assert righe.iloc[9]["Cumulato (EUR)"] == pytest.approx(21200.0)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(302000.0)
    assert righe.iloc[15]["Flusso (EUR/anno)"] == 46800.0


def test_demo_tabella_righe():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Calore lordo (MWh/anno)"] == pytest.approx(3000.0)
    assert mappa["Calore recuperato (MWh/anno)"] == pytest.approx(1200.0)
    assert mappa["Calore netto (MWh/anno)"] == pytest.approx(1800.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(103200.0)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(46800.0)
    assert mappa["Payback (anni)"] == 9
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Prezzo elettrico di pareggio (EUR/MWh)"] == pytest.approx(
        221.42857142857142)


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
    assert bc["capex_eur"] * bc["crf"] == pytest.approx(
        bc["quota_capex_eur_anno"])
    assert (bc["quota_capex_eur_anno"] + bc["om_fisso_eur_anno"]) / \
        bc["produzione_L_anno"] + bc["c_alt_var_eur_anno"] / \
        bc["produzione_L_anno"] == pytest.approx(bc["lco_alt_eur_L"])
    assert bc["c_base_eur_anno"] - bc["gas_res_mwh_anno"] * \
        bc["prezzo_gas_eur_mwh"] - bc["om_fisso_eur_anno"] == \
        pytest.approx(bc["prezzo_pareggio_eur_mwh"] *
                      bc["e_el_mwh_anno"])
    assert bc["q_lordo_mwh_anno"] - bc["q_rec_mwh_anno"] == \
        pytest.approx(bc["q_netto_mwh_anno"])
    assert bc["produzione_L_anno"] * bc["calore_kWh_per_1000L"] / \
        1000000.0 == pytest.approx(bc["q_lordo_mwh_anno"])


def test_demo_crf_solo_nel_lco_non_nei_flussi():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -bc["capex_eur"]
    assert all(f == bc["risparmio_eur_anno"] for f in bc["flussi"][1:])
    assert bc["crf"] not in bc["flussi"]
    assert bc["quota_capex_eur_anno"] not in bc["flussi"]
    van_da_flussi = mh758_van(bc["flussi"], bc["wacc_pct"])
    assert van_da_flussi == pytest.approx(bc["van"])
    assert bc["lco_alt_eur_L"] == pytest.approx(
        (bc["capex_eur"] * bc["crf"] + bc["om_fisso_eur_anno"]) /
        bc["produzione_L_anno"] + bc["c_alt_var_eur_anno"] /
        bc["produzione_L_anno"])


def test_demo_contro_riconteggio_indipendente():
    prod, cal, eta, qr, quota, cop = 50000000, 60, 0.90, 40.0, 70.0, 3.0
    pg, pe, om, cx = 45, 110, 30000, 400000
    fg, fe, wacc, vita = 0.20, 0.25, 5.0, 15
    ql = prod * cal / 1000000.0
    qrec = qr / 100 * ql
    qn = ql - qrec
    gb = ql / eta
    cb = gb * pg
    qp = quota / 100 * qn
    ee = qp / cop
    gr = (1 - quota / 100) * qn / eta
    cav = gr * pg + ee * pe
    ca = cav + om
    risp = cb - ca
    co2b = gb * fg
    co2a = gr * fg + ee * fe
    r = wacc / 100.0
    crf = r * (1 + r) ** vita / ((1 + r) ** vita - 1)
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    bc = demo_calcoli()
    assert bc["q_lordo_mwh_anno"] == pytest.approx(ql)
    assert bc["q_rec_mwh_anno"] == pytest.approx(qrec)
    assert bc["q_netto_mwh_anno"] == pytest.approx(qn)
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


def test_demo_riconteggio_crf_van_pareggio_a_mano():
    bc = demo_calcoli()
    r = 0.05
    annuita = (1 - (1 + r) ** -15) / r
    assert annuita == pytest.approx(10.379658038800514)
    assert bc["van"] == pytest.approx(-400000 + 46800.0 * annuita)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(
        (150000.0 - 27000.0 - 30000) / 420.0)
    assert bc["flussi"][0] + 15 * bc["flussi"][1] == pytest.approx(
        302000.0)
    assert bc["flussi"][0] + 8 * bc["flussi"][1] == pytest.approx(
        -25600.0)


# ---------------------------------------------------------------- varianti
def test_demo_conviente():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] > 0.0
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_risparmio_negativo_calcolabile_non_degenere():
    bc = _variante(prezzo_gas_eur_mwh=30)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(5800.0)
    assert bc["van"] == pytest.approx(-339797.9833785527)
    assert bc["tir"] is None or bc["tir"] < 0.0
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_prezzo_el_alto_non_conviente():
    bc = _variante(prezzo_el_eur_mwh=200)
    assert bc["risparmio_eur_anno"] == pytest.approx(9000.0)
    assert bc["van"] == pytest.approx(-306583.0776563748)
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(221.42857142857142)
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_variante_prezzo_el_zero_conviente():
    bc = _variante(prezzo_el_eur_mwh=0.0)
    assert bc["c_alt_var_eur_anno"] == pytest.approx(27000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(57000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(93000.0)
    assert bc["van"] == pytest.approx(565308.1975507949)
    assert bc["tir"] == pytest.approx(22.0844913982649, abs=1e-4)
    assert bc["payback"] == 5
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_variante_gas_alto_conviente():
    bc = _variante(prezzo_gas_eur_mwh=150)
    assert bc["risparmio_eur_anno"] == pytest.approx(333800.0)
    assert bc["van"] == pytest.approx(3064729.85314468)
    assert bc["payback"] == 2
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_variante_gas_marginale():
    bc = _variante(prezzo_gas_eur_mwh=41)
    assert bc["risparmio_eur_anno"] == pytest.approx(35866.66666666666)
    assert bc["van"] == pytest.approx(-27716.265030589562)
    assert bc["van"] < 0.0
    assert abs(bc["van"]) <= 0.10 * 400000
    assert bc["tir"] == pytest.approx(3.9563287463225225, abs=1e-4)
    assert bc["payback"] == 12
    assert bc["verdetto"] == "MARGINALE"
    assert bc["valid"] is True


def test_variante_quota_zero_calcolabile_non_degenere():
    bc = _variante(quota_pdc_pct=0)
    assert bc["valid"] is True
    assert bc["q_pdc_mwh_anno"] == 0.0
    assert bc["e_el_mwh_anno"] == 0.0
    assert bc["gas_res_mwh_anno"] == pytest.approx(2000.0)
    assert bc["risparmio_eur_anno"] == 30000.0
    assert bc["van"] == pytest.approx(-88610.25885458228)
    assert bc["co2_evitata_t_anno"] == pytest.approx(266.66666666666663)
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_quota_recupero_cento_calcolabile_non_degenere():
    bc = _variante(quota_recupero_pct=100)
    assert bc["valid"] is True
    assert bc["q_netto_mwh_anno"] == 0.0
    assert bc["q_pdc_mwh_anno"] == 0.0
    assert bc["e_el_mwh_anno"] == 0.0
    assert bc["gas_res_mwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == 120000.0
    assert bc["van"] == pytest.approx(845558.9645816708)
    assert bc["tir"] == pytest.approx(29.36956629840659, abs=1e-4)
    assert bc["payback"] == 4
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_quota_recupero_zero():
    bc = _variante(quota_recupero_pct=0)
    assert bc["q_netto_mwh_anno"] == pytest.approx(3000.0)
    assert bc["q_pdc_mwh_anno"] == pytest.approx(2100.0)
    assert bc["e_el_mwh_anno"] == pytest.approx(700.0)
    assert bc["gas_res_mwh_anno"] == pytest.approx(1000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-2000.0)
    assert bc["van"] == pytest.approx(-420759.31607636117)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(107.14285714285714)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_cop_basso_e_alto():
    bc = _variante(cop=2.0)
    assert bc["e_el_mwh_anno"] == pytest.approx(630.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(23700.0)
    assert bc["van"] == pytest.approx(-154002.10449512)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(147.61904761904762)
    assert bc["verdetto"] == "NON_CONVIENTE"
    bc2 = _variante(cop=5.0)
    assert bc2["e_el_mwh_anno"] == pytest.approx(252.0)
    assert bc2["risparmio_eur_anno"] == pytest.approx(65280.0)
    assert bc2["van"] == pytest.approx(277584.0767324289)
    assert bc2["tir"] == pytest.approx(14.0480244560851, abs=1e-4)
    assert bc2["payback"] == 7
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_co2_evitata_negativa_con_fattore_el_alto():
    bc = _variante(f_el_t_per_mwh=1.50)
    assert bc["co2_alt_t_anno"] == pytest.approx(750.0)
    assert bc["co2_evitata_t_anno"] == pytest.approx(-83.33333333333337)
    assert bc["co2_evitata_t_anno"] < 0.0
    assert bc["van"] == pytest.approx(85767.99618685164)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_pareggio_negativo():
    bc = _variante(om_fisso_eur_anno=5000000)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(-11611.904761904761)
    assert bc["prezzo_pareggio_eur_mwh"] < 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(-4923200.0)
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_variante_pareggio_zero():
    bc = _variante(om_fisso_eur_anno=123000)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(0.0, abs=1e-9)
    assert bc["risparmio_eur_anno"] == pytest.approx(-46200.0)


def test_variante_wacc_zero():
    bc = _variante(wacc_pct=0)
    assert bc["crf"] == pytest.approx(1.0 / 15.0)
    assert bc["quota_capex_eur_anno"] == pytest.approx(26666.666666666668)
    assert bc["lco_alt_eur_L"] == pytest.approx(0.0025973333333333334)
    assert bc["van"] == pytest.approx(302000.0)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex_eur=0)
    assert bc["capex_eur"] == 0
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(485767.99618685164)
    assert bc["lco_alt_eur_L"] == pytest.approx(0.002064)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_vita_dieci():
    bc = _variante(vita_anni=10)
    assert len(bc["flussi"]) == 11
    assert bc["crf"] == pytest.approx(0.12950457496545661)
    assert bc["van"] == pytest.approx(-38622.80531415084)
    assert bc["tir"] == pytest.approx(2.961451941278992, abs=1e-4)
    assert bc["payback"] == 9
    assert bc["verdetto"] == "MARGINALE"


def test_variante_input_nulli_calcolabile_non_degenere():
    bc = _variante(prezzo_el_eur_mwh=0.0, prezzo_gas_eur_mwh=0,
                   om_fisso_eur_anno=0)
    assert bc["valid"] is True
    assert bc["c_base_eur_anno"] == 0.0
    assert bc["c_alt_eur_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == 0.0
    assert bc["van"] == -400000.0
    assert bc["verdetto"] == "NON_CONVIENTE"


# ---------------------------------------------------------------- degenere
def test_degenere_produzione_zero():
    bc = _variante(produzione_L_anno=0)
    assert bc["valid"] is False
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"] == []
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["lco_base_eur_L"] is None
    assert bc["lco_alt_eur_L"] is None
    assert bc["errore"]


def test_degenere_calore_cop_vita():
    for kw in ({"calore_kWh_per_1000L": 0}, {"calore_kWh_per_1000L": -5},
               {"cop": 0}, {"cop": -1},
               {"produzione_L_anno": 0},
               {"produzione_L_anno": -1},
               {"vita_anni": 0}, {"vita_anni": 2.5}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_eta_wacc_tolleranza_quote_prezzi_negativi():
    for kw in ({"eta_caldaia": 0}, {"eta_caldaia": 1.01},
               {"wacc_pct": -1}, {"wacc_pct": 60},
               {"tolleranza_pct": -1}, {"tolleranza_pct": 101},
               {"quota_recupero_pct": -1}, {"quota_recupero_pct": 101},
               {"quota_pdc_pct": -1}, {"quota_pdc_pct": 101},
               {"prezzo_gas_eur_mwh": -1},
               {"prezzo_el_eur_mwh": -1},
               {"om_fisso_eur_anno": -100},
               {"capex_eur": -1}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_stringa_nan_inf():
    for kw in ({"produzione_L_anno": "300000"},
               {"produzione_L_anno": float("nan")},
               {"prezzo_el_eur_mwh": float("inf")},
               {"capex_eur": True}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_neutro_campi():
    bc = _variante(produzione_L_anno=0)
    assert bc["q_lordo_mwh_anno"] == 0.0
    assert bc["gas_base_mwh_anno"] == 0.0
    assert bc["c_base_eur_anno"] == 0.0
    assert bc["c_alt_eur_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == 0.0
    assert bc["van"] == 0.0
    assert list(bc["df_flussi"].columns) == [
        "Anno", "Flusso (EUR/anno)", "Cumulato (EUR)"]
    assert list(bc["df_tabella"].columns) == ["Voce", "Valore"]


def test_pareggio_none_quando_e_el_zero():
    assert mh758_prezzo_pareggio(600000.0, 2800.0, 45, 80000,
                                 0.0) is None
    assert mh758_prezzo_pareggio(600000.0, 2800.0, 45, 80000,
                                 None) is None
    assert mh758_lco_base(600000.0, 0) is None
    assert mh758_e_el(5880.0, 0) is None
    bc = _variante(quota_pdc_pct=0)
    assert bc["prezzo_pareggio_eur_mwh"] is None


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = demo_calcoli()
    testo = mh758_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert "q_lordo_mwh_anno;3000.0" in testo
    assert "q_netto_mwh_anno;1800.0" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "prezzo_pareggio_eur_mwh" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = demo_calcoli()
    testo = mh758_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"quota_capex_eur_anno;{bc['quota_capex_eur_anno']}" in testo
    assert f"q_lordo_mwh_anno;{bc['q_lordo_mwh_anno']}" in testo


def test_csv_degenere_solo_zeri():
    bc = _variante(produzione_L_anno=0)
    testo = mh758_csv(bc, _demo_kwargs())
    assert "van_eur;0.0" in testo
    assert "q_lordo_mwh_anno;0.0" in testo
    assert "verdetto;NON_CALCOLABILE" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = demo_calcoli()
    testo = mh758_csv(bc, _demo_kwargs())
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
    assert basso - base == pytest.approx(4200.0)
    assert base - alto == pytest.approx(4200.0)


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
    assert set(mh758_demo().keys()) == {
        "produzione_L_anno", "calore_kWh_per_1000L",
        "eta_caldaia", "quota_recupero_pct",
        "quota_pdc_pct", "cop",
        "prezzo_gas_eur_mwh", "prezzo_el_eur_mwh",
        "om_fisso_eur_anno", "capex_eur",
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
    ast.parse(_leggi("w759_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w759_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab758:")


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    # token vietati costruiti per concatenazione, cosi' questo
    # stesso file non li contiene come sottostringhe contigue.
    src = _leggi("w759_helpers.py")
    vietati = ["mh" + "75" + "7", "st" + "75" + "7",
               "tab" + "75" + "7", "w" + "75" + "8",
               "mh" + "75" + "6", "tab" + "75" + "6", "st" + "75" + "6",
               "st" + "75" + "6"]
    assert "streamlit" not in src
    assert all(t not in src for t in vietati)
    assert "macchina " + "continua" not in src
    assert "foglio " + "di carta" not in src


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w759_ui.py")
    vietati = ["mh" + "75" + "7", "st" + "75" + "7",
               "tab" + "75" + "7", "w" + "75" + "8",
               "mh" + "75" + "6", "tab" + "75" + "6", "st" + "75" + "6",
               "st" + "75" + "6"]
    assert all(t not in src for t in vietati)
    assert "essiccare " + "la carta" not in src
    assert "cilindri " + "essiccatori" not in src
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st758_") for c in chiavi)
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
    src = _leggi("w759_test.py")
    vietati = ["mh" + "75" + "7", "st" + "75" + "7",
               "tab" + "75" + "7", "w" + "75" + "8",
               "mh" + "75" + "6", "tab" + "75" + "6", "st" + "75" + "6",
               "st" + "75" + "6"]
    assert all(t not in src for t in vietati)
    assert "essiccare " + "la carta" not in src
    assert "cilindri " + "essiccatori" not in src


def test_ui_chiavi_demo_coerenti():
    """Ogni _def758[...] letto dalla UI esiste nel dict demo:
    sweep anti-KeyError a render (lezione dello sweep chiavi demo vs UI)."""
    src = _leggi("w759_ui.py")
    usate = set(re.findall(r'_def758\["([^"]+)"\]', src))
    assert usate
    assert usate <= set(mh758_demo().keys())


def test_ui_riferisce_solo_helper_nuovi():
    src = _leggi("w759_ui.py")
    usati = set(re.findall(r'\b(mh\d+_\w+)\b', src))
    assert usati
    assert all(u.startswith("mh758_") for u in usati)


@pytest.mark.parametrize("wacc,vita,atteso", [
    (5.0, 15, 0.09634228760924432),
    (0, 15, 1.0 / 15.0),
    (10.0, 10, 0.16274539488251152),
    (5.0, 1, 1.05),
    (50.0, 5, 0.5758293838862559),
])
def test_crf_parametrizzato(wacc, vita, atteso):
    assert mh758_crf(wacc, vita) == pytest.approx(atteso)


@pytest.mark.parametrize("campo,valore", [
    ("produzione_L_anno", 0), ("produzione_L_anno", -3),
    ("calore_kWh_per_1000L", 0), ("calore_kWh_per_1000L", -5),
    ("eta_caldaia", 0), ("eta_caldaia", 1.01),
    ("quota_recupero_pct", -1), ("quota_recupero_pct", 100.1),
    ("quota_pdc_pct", -1), ("quota_pdc_pct", 100.1),
    ("cop", 0), ("cop", -1),
    ("prezzo_gas_eur_mwh", -1),
    ("prezzo_el_eur_mwh", -1),
    ("om_fisso_eur_anno", -100),
    ("capex_eur", -1),
    ("f_gas_t_per_mwh", -0.10), ("f_el_t_per_mwh", -0.10),
    ("wacc_pct", -0.1), ("wacc_pct", 50.1),
    ("vita_anni", -1), ("vita_anni", 2.5),
    ("tolleranza_pct", -1), ("tolleranza_pct", 100.1),
])
def test_valida_rifiuta_singoli_campi(campo, valore):
    d = _demo_kwargs()
    d[campo] = valore
    assert mh758_valida(**d)["valido"] is False


def test_df_tabella_valori_demo_selezionati():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Produzione (L/anno)"] == 50000000.0
    assert mappa["Calore lordo (MWh/anno)"] == pytest.approx(3000.0)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(46800.0)
    assert mappa["Verdetto"] == "CONVIENTE"


def test_lco_alt_minore_di_lco_base_demo():
    bc = demo_calcoli()
    assert bc["lco_alt_eur_L"] < bc["lco_base_eur_L"]
    assert bc["lco_base_eur_L"] - bc["lco_alt_eur_L"] == pytest.approx(
        0.00016526169912604556)
