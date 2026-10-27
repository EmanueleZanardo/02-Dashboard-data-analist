"""Test tab760 "Conservificio:
sterilizzare le conserve con calore
recuperato e pompa di calore batte
la caldaia a gas?"

Nuova tab tab760 (sterilizzazione
conserve, file di lavoro w761).
Business case deterministico della
sterilizzazione delle conserve
alimentari in autoclave in un
conservificio: le conserve vanno
sterilizzate in autoclave (calore
per 1000 kg di conserve) e il calore
puo' arrivare dalla caldaia a gas
(baseline, tutto il calore lordo,
senza recupero) oppure in parte dal
calore recuperato dalle condense e
dalle acque calde di autoclave e in
parte da una pompa di calore che
copre una quota del calore netto,
con il resto che resta a gas.
Q_lordo = kg x calore / 1000000;
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
kg; LCO_alt = (CAPEX x CRF +
OM_fisso) / kg + C_alt_var / kg;
prezzo elettrico di pareggio =
(C_base - gas_res x p_gas -
OM_fisso) / E_el, None se E_el
<= 0, puo' essere negativo (il solo
O&M fisso piu' il gas residuo
superano gia' il costo baseline);
flussi [-CAPEX, risparmio x vita];
VAN, TIR, payback (primo anno con
cumulato >= 0). Distinta dalla tab
precedente della lavanderia (li' si
lava biancheria, senza conserve e
senza recupero da condense di
autoclave), dalla tab del caseificio
(li' si pastorizza latte, senza
conserve e senza recupero da
condense di autoclave), dalla
cartiera (li' si essicca carta,
senza conserve e senza recupero da
condense di autoclave), dalla caldaia
a elettrodi generica (li' il calore
viene da elettrodi, senza processo
di sterilizzazione e senza quota di
recupero) e dal recupero calore
generico (li' il calore recuperato
va a un uso generico, senza
sterilizzazione di conserve e senza
pompa di calore sul calore netto).

Demo calcolata eseguendo demo_calcoli()
(e ricontrollata a mano, riga per
riga): conserve 8.000.000 kg/anno,
calore 250 kWh/1000kg, rendimento
caldaia 0,90, quota recupero 35 %,
quota PdC 60 %, COP 3,2, prezzo gas
45 EUR/MWh, prezzo elettrico 110
EUR/MWh, O&M fisso 15.000 EUR/anno,
CAPEX 300.000 EUR, fattore gas 0,20
tCO2/MWh e fattore elettrico 0,25
tCO2/MWh, WACC 5 %, vita 15 anni,
tolleranza 10 % del CAPEX.

- q_lordo_mwh_anno = 2000.0
- q_rec_mwh_anno = 700.0
- q_netto_mwh_anno = 1300.0
- gas_base_mwh_anno = 2222.222222222222
- c_base_eur_anno = 100000.0
- q_pdc_mwh_anno = 780.0
- e_el_mwh_anno = 243.75
- gas_res_mwh_anno = 577.7777777777777
- c_alt_var_eur_anno = 52812.5
- c_alt_eur_anno = 67812.5
- risparmio_eur_anno = 32187.5
- co2_base_t_anno = 444.44444444444446
- co2_alt_gas_t_anno = 115.55555555555554
- co2_alt_el_t_anno = 60.9375
- co2_alt_t_anno = 176.49305555555554
- co2_evitata_t_anno = 267.9513888888889
- crf = 0.09634228760924432
- quota_capex_eur_anno = 28902.686282773295
- lco_base_eur_kg = 0.0125
- lco_alt_eur_kg = 0.012089398285346662
- van = 34095.24310393778
- tir = 6.637135466991194
- payback = 10
- prezzo_pareggio_eur_mwh = 242.05128205128204
- verdetto = 'CONVIENTE'

Scomposizione: Q_lordo = 8.000.000 x 250 /
1000000 = 2.000 MWh/anno; Q_rec = 0,35 x
2.000 = 700 MWh/anno; Q_netto =
2.000 - 700 = 1.300 MWh/anno;
gas_base = 2.000 / 0,90 = 2.222,22
MWh/anno; C_base = 2.222,22 x 45 =
100.000 EUR/anno; Q_pdc = 0,60 x
1.300 = 780 MWh/anno; E_el = 780 /
3,2 = 243,75 MWh/anno; gas_res =
0,40 x 1.300 / 0,90 = 577,78 MWh/anno;
C_alt_var = 577,78 x 45 + 243,75 x 110
= 26.000 + 26.812,50 = 52.812,50
EUR/anno; C_alt = 52.812,50 + 15.000 =
67.812,50 EUR/anno; risparmio = 100.000
- 67.812,50 = 32.187,50 EUR/anno; CO2 base
= 2.222,22 x 0,20 = 444,44 t/anno;
CO2 alt = 577,78 x 0,20 + 243,75 x
0,25 = 115,56 + 60,94 = 176,49 t/anno;
CO2 evitata = 267,95 t/anno; CRF 0,05
x 1,05^15 / (1,05^15 - 1) =
0.09634228760924432; quota CAPEX
300.000 x 0,096342 = 28.902,69
EUR/anno; LCO base 100.000 / 8.000.000 =
0,0125 EUR/kg; LCO alt (28.902,69 +
15.000) / 8.000.000 + 52.812,50 / 8.000.000 =
0,0120894 EUR/kg; flussi: anno 0
-300.000, anni 1-15 risparmio
32.187,50 (piatti); VAN -300.000 +
32.187,50 x 10,379658 (annuita' 15 anni
al 5 %) = 34.095,24 EUR; TIR 6,64 %;
payback 10 anni (il cumulato all'anno
9 e' -10.312,50 EUR, all'anno 10 e'
21.875 EUR); prezzo elettrico di
pareggio (100.000 - 26.000 - 15.000) /
243,75 = 242,05 EUR/MWh; verdetto
CONVIENTE perche' VAN > 0.
NOTA: il CRF entra solo nel LCO,
mai nei flussi: il CAPEX compare una
sola volta, all'anno 0.
NOTA 2: in questo brief il risparmio
nullo o negativo NON e' degenere:
con prezzo gas 30 EUR/MWh il
risparmio e' 7.520,83 EUR/anno e il
caso resta calcolabile (valid=True,
VAN -221.936,32 EUR, NON_CONVIENTE).
NOTA 3: la CO2 evitata puo' essere
negativa: con fattore elettrico 1,50
tCO2/MWh la CO2 evitata e'
-36,74 t/anno, pur restando il caso
calcolabile.
NOTA 4: il prezzo elettrico di
pareggio puo' essere negativo: con
O&M fisso 5.000.000 EUR/anno il
pareggio e' -20.209,23 EUR/MWh,
perche' il solo O&M fisso piu' il
gas residuo superano gia' il costo
baseline (il caso demo ha pareggio
positivo, 242,05 EUR/MWh).
NOTA 5: la quota PdC zero NON e'
degenere: con quota 0 il risparmio
e' 20.000 EUR/anno, la VAN
-92.406,84 EUR e il pareggio non
e' definito (E_el nulla).
NOTA 6: il calore netto nullo (quota
recupero 100 %) NON e' degenere:
il risparmio e' 85.000 EUR/anno
(100.000 - 15.000 di solo O&M fisso)
e la VAN 582.270,93 EUR, e il
pareggio non e' definito.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w761_helpers import (
    demo_calcoli,
    mh760_c_alt,
    mh760_c_alt_var,
    mh760_c_base,
    mh760_calcola,
    mh760_co2_alt,
    mh760_co2_base,
    mh760_co2_evitata,
    mh760_crf,
    mh760_csv,
    mh760_demo,
    mh760_e_el,
    mh760_eta,
    mh760_flussi,
    mh760_gas_base,
    mh760_gas_res,
    mh760_int_pos,
    mh760_lco_alt,
    mh760_lco_base,
    mh760_nneg,
    mh760_num,
    mh760_payback,
    mh760_pct_0_100,
    mh760_pct_wacc,
    mh760_pos,
    mh760_prezzo_pareggio,
    mh760_q_lordo,
    mh760_q_netto,
    mh760_q_pdc,
    mh760_q_rec,
    mh760_quota_capex,
    mh760_risparmio,
    mh760_tir,
    mh760_valida,
    mh760_van,
    mh760_verdetto,
)


def _demo_kwargs():
    return dict(mh760_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh760_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh760_num(3, "x") == 3.0
    assert mh760_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh760_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh760_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh760_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh760_pos(0, "x")
    with pytest.raises(ValueError):
        mh760_pos(-1, "x")
    assert mh760_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh760_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh760_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh760_int_pos(0, "x")


def test_pct_0_100_limiti():
    assert mh760_pct_0_100(0, "x") == 0.0
    assert mh760_pct_0_100(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh760_pct_0_100(100.1, "x")
    with pytest.raises(ValueError):
        mh760_pct_0_100(-1, "x")


def test_pct_wacc_limiti():
    assert mh760_pct_wacc(0, "x") == 0.0
    assert mh760_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh760_pct_wacc(50.1, "x")


def test_eta_limiti():
    assert mh760_eta(1.0, "x") == 1.0
    assert mh760_eta(0.90, "x") == 0.90
    with pytest.raises(ValueError):
        mh760_eta(0, "x")
    with pytest.raises(ValueError):
        mh760_eta(-0.1, "x")
    with pytest.raises(ValueError):
        mh760_eta(1.01, "x")


# ---------------------------------------------------------------- fisica base
def test_q_lordo_rec_netto():
    assert mh760_q_lordo(8000000, 250) == pytest.approx(2000.0)
    assert mh760_q_lordo(8000000, 0) == 0.0
    assert mh760_q_rec(2000.0, 35.0) == pytest.approx(700.0)
    assert mh760_q_rec(2000.0, 0) == 0.0
    assert mh760_q_rec(2000.0, 100) == 2000.0
    assert mh760_q_netto(2000.0, 700.0) == pytest.approx(1300.0)
    assert mh760_q_netto(2000.0, 2000.0) == 0.0
    with pytest.raises(ValueError):
        mh760_q_rec(2000.0, 100.1)
    with pytest.raises(ValueError):
        mh760_q_lordo(8000000, -1)


def test_gas_base_e_c_base_e_co2_base():
    assert mh760_gas_base(2000.0, 0.90) == pytest.approx(2222.222222222222)
    assert mh760_gas_base(2000.0, 1.0) == 2000.0
    assert mh760_c_base(2222.222222222222, 45) == pytest.approx(100000.0)
    assert mh760_co2_base(2222.222222222222, 0.20) == pytest.approx(
        444.44444444444446)
    with pytest.raises(ValueError):
        mh760_gas_base(2000.0, 0)
    with pytest.raises(ValueError):
        mh760_c_base(2222.222222222222, -1)


def test_q_pdc_e_e_el():
    assert mh760_q_pdc(1300.0, 60.0) == pytest.approx(780.0)
    assert mh760_q_pdc(1300.0, 0) == 0.0
    assert mh760_q_pdc(1300.0, 100) == 1300.0
    assert mh760_e_el(780.0, 3.2) == pytest.approx(243.75)
    assert mh760_e_el(780.0, 0) is None
    assert mh760_e_el(780.0, -1.0) is None
    assert mh760_e_el(0.0, 3.2) == 0.0
    with pytest.raises(ValueError):
        mh760_q_pdc(1300.0, 100.1)


def test_gas_res():
    assert mh760_gas_res(1300.0, 60.0, 0.90) == pytest.approx(
        577.7777777777777)
    assert mh760_gas_res(1300.0, 0, 0.90) == pytest.approx(
        1444.4444444444443)
    assert mh760_gas_res(1300.0, 100, 0.90) == 0.0
    with pytest.raises(ValueError):
        mh760_gas_res(1300.0, 60.0, 0)


def test_c_alt_var_e_c_alt():
    assert mh760_c_alt_var(577.7777777777777, 45, 243.75,
                           110) == pytest.approx(52812.5)
    assert mh760_c_alt_var(577.7777777777777, 45, 0.0,
                           110) == pytest.approx(26000.0)
    assert mh760_c_alt(52812.5, 15000) == pytest.approx(67812.5)
    assert mh760_c_alt(52812.5, 0) == pytest.approx(52812.5)
    with pytest.raises(ValueError):
        mh760_c_alt_var(577.7777777777777, -1, 243.75, 110)


def test_risparmio_segno():
    assert mh760_risparmio(100000.0, 67812.5) == pytest.approx(32187.5)
    assert mh760_risparmio(100000.0, 100000.0) == 0.0
    assert mh760_risparmio(100000.0, 50000.0) == 50000.0


def test_co2_alt_e_evitata_segno_libero():
    assert mh760_co2_alt(577.7777777777777, 0.20, 243.75,
                         0.25) == pytest.approx(176.49305555555554)
    assert mh760_co2_evitata(444.44444444444446,
                             176.49305555555554) == pytest.approx(
        267.9513888888889)
    assert mh760_co2_evitata(444.44444444444446,
                             444.44444444444446) == pytest.approx(0.0)
    assert mh760_co2_evitata(444.44444444444446,
                             1044.44444444444446) == pytest.approx(
        -600.0, abs=1e-6)


# ---------------------------------------------------------------- finanza base
def test_crf():
    assert mh760_crf(5.0, 15) == pytest.approx(0.09634228760924432)
    assert mh760_crf(0, 15) == pytest.approx(1.0 / 15.0)
    assert mh760_crf(5.0, 1) == pytest.approx(1.05)
    assert mh760_crf(5.0, 10) == pytest.approx(0.12950457496545661)


def test_quota_capex_e_lco():
    assert mh760_quota_capex(300000, 0.09634228760924432) == pytest.approx(
        28902.686282773295)
    assert mh760_lco_base(100000.0, 8000000) == pytest.approx(0.0125)
    assert mh760_lco_base(100000.0, 0) is None
    assert mh760_lco_alt(300000, 0.09634228760924432, 15000,
                         52812.5, 8000000) == pytest.approx(
        0.012089398285346662)
    assert mh760_lco_alt(300000, 0.09634228760924432, 15000,
                         52812.5, 0) is None
    assert mh760_lco_alt(0, 0.09634228760924432, 15000,
                         52812.5, 8000000) == pytest.approx(0.0084765625)


def test_prezzo_pareggio_formula_brief_negativo_e_none():
    assert mh760_prezzo_pareggio(100000.0, 577.7777777777777, 45, 15000,
                                 243.75) == pytest.approx(
        242.05128205128204)
    assert mh760_prezzo_pareggio(100000.0, 577.7777777777777, 45, 74000,
                                 243.75) == pytest.approx(0.0, abs=1e-9)
    assert mh760_prezzo_pareggio(100000.0, 577.7777777777777, 45, 15000,
                                 0.0) is None
    assert mh760_prezzo_pareggio(100000.0, 577.7777777777777, 45, 15000,
                                 None) is None
    assert mh760_prezzo_pareggio(100000.0, 0.0, 45, 0,
                                 243.75) == pytest.approx(
        410.25641025641026)


def test_flussi_lunghezza_e_primo():
    fl = mh760_flussi(300000, 32187.5, 15)
    assert len(fl) == 16
    assert fl[0] == -300000
    assert all(f == 32187.5 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = demo_calcoli()
    assert bc["van"] == pytest.approx(34095.24310393778)
    assert mh760_van([-300000] + [32187.5] * 15,
                     0) == pytest.approx(182812.5)
    assert mh760_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo_e_conviente():
    bc = demo_calcoli()
    assert bc["tir"] == pytest.approx(6.637135466991194)
    assert mh760_tir([-300000] + [32187.5] * 15) == pytest.approx(
        0.06637135466991194)
    tir = mh760_tir([-300000] + [32187.5] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-300000] + [32187.5] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback():
    assert mh760_payback([-300000] + [32187.5] * 15) == 10
    assert mh760_payback([-300000] + [-1000.0] * 15) is None
    assert mh760_payback([0] + [32187.5] * 15) == 0
    assert mh760_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh760_verdetto(100.0, 300000, 10.0) == "CONVIENTE"
    assert mh760_verdetto(-29000.0, 300000, 10.0) == "MARGINALE"
    assert mh760_verdetto(-30000.0, 300000, 10.0) == "MARGINALE"
    assert mh760_verdetto(-30000.01, 300000, 10.0) == "NON_CONVIENTE"
    assert mh760_verdetto(float("nan"), 300000, 10.0) == "NON_CALCOLABILE"
    assert mh760_verdetto(0.0, 0, 10.0) == "MARGINALE"


def test_valida_demo_ok():
    v = mh760_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("kg_anno", "300000"),
                       ("kg_anno", float("nan")),
                       ("kg_anno", float("inf")),
                       ("kg_anno", True),
                       ("prezzo_el_eur_mwh", None)):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh760_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("kg_anno", 0),
                          ("calore_kWh_per_1000kg", 0),
                          ("calore_kWh_per_1000kg", -5),
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
        assert mh760_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"quota_recupero_pct": 0, "quota_pdc_pct": 0,
              "prezzo_gas_eur_mwh": 0,
              "prezzo_el_eur_mwh": 0, "om_fisso_eur_anno": 0,
              "capex_eur": 0, "f_gas_t_per_mwh": 0,
              "f_el_t_per_mwh": 0, "wacc_pct": 0,
              "tolleranza_pct": 0, "eta_caldaia": 1.0})
    assert mh760_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["quota_pdc_pct"] = 100
    d["quota_recupero_pct"] = 100
    assert mh760_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh760_demo()
    assert d["kg_anno"] == 8000000
    assert d["calore_kWh_per_1000kg"] == 250
    assert d["eta_caldaia"] == 0.90
    assert d["quota_recupero_pct"] == 35.0
    assert d["quota_pdc_pct"] == 60.0
    assert d["cop"] == 3.2
    assert d["prezzo_gas_eur_mwh"] == 45
    assert d["prezzo_el_eur_mwh"] == 110
    assert d["om_fisso_eur_anno"] == 15000
    assert d["capex_eur"] == 300000
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
        "q_lordo_mwh_anno": 2000.0,
        "q_rec_mwh_anno": 700.0,
        "q_netto_mwh_anno": 1300.0,
        "gas_base_mwh_anno": 2222.222222222222,
        "c_base_eur_anno": 100000.0,
        "q_pdc_mwh_anno": 780.0,
        "e_el_mwh_anno": 243.75,
        "gas_res_mwh_anno": 577.7777777777777,
        "c_alt_var_eur_anno": 52812.5,
        "c_alt_eur_anno": 67812.5,
        "risparmio_eur_anno": 32187.5,
        "co2_base_t_anno": 444.44444444444446,
        "co2_alt_t_anno": 176.49305555555554,
        "co2_evitata_t_anno": 267.9513888888889,
        "crf": 0.09634228760924432,
        "quota_capex_eur_anno": 28902.686282773295,
        "lco_base_eur_kg": 0.0125,
        "lco_alt_eur_kg": 0.012089398285346662,
        "van": 34095.24310393778,
        "tir": 6.637135466991194,
        "prezzo_pareggio_eur_mwh": 242.05128205128204,
    }
    for chiave, atteso in attesi.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert abs(got - atteso) / abs(atteso) < 1e-9, chiave
    assert bc["payback"] == 10
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_demo_calcoli_fisica():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["q_lordo_mwh_anno"] == pytest.approx(2000.0)
    assert bc["q_rec_mwh_anno"] == pytest.approx(700.0)
    assert bc["q_netto_mwh_anno"] == pytest.approx(1300.0)
    assert bc["gas_base_mwh_anno"] == pytest.approx(2222.222222222222)
    assert bc["co2_evitata_t_anno"] == pytest.approx(267.9513888888889)


def test_demo_calcoli_economia():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] == 100000.0
    assert bc["c_alt_var_eur_anno"] == pytest.approx(52812.5)
    assert bc["c_alt_eur_anno"] == pytest.approx(67812.5)
    assert bc["risparmio_eur_anno"] == pytest.approx(32187.5)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(242.05128205128204)


def test_demo_calcoli_finanza():
    bc = demo_calcoli()
    assert bc["crf"] == pytest.approx(0.09634228760924432)
    assert bc["quota_capex_eur_anno"] == pytest.approx(28902.686282773295)
    assert bc["lco_base_eur_kg"] == pytest.approx(0.0125)
    assert bc["lco_alt_eur_kg"] == pytest.approx(0.012089398285346662)
    assert bc["van"] == pytest.approx(34095.24310393778)
    assert bc["tir"] == pytest.approx(6.637135466991194)
    assert bc["payback"] == 10
    assert bc["verdetto"] == "CONVIENTE"


def test_demo_flussi_e_cumulato():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -300000
    assert len(bc["flussi"]) == 16
    assert all(f == 32187.5 for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -300000
    assert righe.iloc[5]["Cumulato (EUR)"] == pytest.approx(-139062.5)
    assert righe.iloc[9]["Cumulato (EUR)"] == pytest.approx(-10312.5)
    assert righe.iloc[10]["Cumulato (EUR)"] == pytest.approx(21875.0)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(182812.5)
    assert righe.iloc[15]["Flusso (EUR/anno)"] == 32187.5


def test_demo_tabella_righe():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Calore lordo (MWh/anno)"] == pytest.approx(2000.0)
    assert mappa["Calore recuperato (MWh/anno)"] == pytest.approx(700.0)
    assert mappa["Calore netto (MWh/anno)"] == pytest.approx(1300.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(67812.5)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(32187.5)
    assert mappa["Payback (anni)"] == 10
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Prezzo elettrico di pareggio (EUR/MWh)"] == pytest.approx(
        242.05128205128204)


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
        bc["kg_anno"] + bc["c_alt_var_eur_anno"] / \
        bc["kg_anno"] == pytest.approx(bc["lco_alt_eur_kg"])
    assert bc["c_base_eur_anno"] - bc["gas_res_mwh_anno"] * \
        bc["prezzo_gas_eur_mwh"] - bc["om_fisso_eur_anno"] == \
        pytest.approx(bc["prezzo_pareggio_eur_mwh"] *
                      bc["e_el_mwh_anno"])
    assert bc["q_lordo_mwh_anno"] - bc["q_rec_mwh_anno"] == \
        pytest.approx(bc["q_netto_mwh_anno"])
    assert bc["kg_anno"] * bc["calore_kWh_per_1000kg"] / \
        1000000.0 == pytest.approx(bc["q_lordo_mwh_anno"])


def test_demo_crf_solo_nel_lco_non_nei_flussi():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -bc["capex_eur"]
    assert all(f == bc["risparmio_eur_anno"] for f in bc["flussi"][1:])
    assert bc["crf"] not in bc["flussi"]
    assert bc["quota_capex_eur_anno"] not in bc["flussi"]
    van_da_flussi = mh760_van(bc["flussi"], bc["wacc_pct"])
    assert van_da_flussi == pytest.approx(bc["van"])
    assert bc["lco_alt_eur_kg"] == pytest.approx(
        (bc["capex_eur"] * bc["crf"] + bc["om_fisso_eur_anno"]) /
        bc["kg_anno"] + bc["c_alt_var_eur_anno"] /
        bc["kg_anno"])


def test_demo_contro_riconteggio_indipendente():
    kg, cal, eta, qr, quota, cop = 8000000, 250, 0.90, 35.0, 60.0, 3.2
    pg, pe, om, cx = 45, 110, 15000, 300000
    fg, fe, wacc, vita = 0.20, 0.25, 5.0, 15
    ql = kg * cal / 1000000.0
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
    assert bc["van"] == pytest.approx(-300000 + 32187.5 * annuita)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(
        (100000.0 - 26000.0 - 15000) / 243.75)
    assert bc["flussi"][0] + 15 * bc["flussi"][1] == pytest.approx(
        182812.5)
    assert bc["flussi"][0] + 9 * bc["flussi"][1] == pytest.approx(
        -10312.5)


# ---------------------------------------------------------------- varianti
def test_demo_conviente():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] > 0.0
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_gas_trenta_segno_e_verdetto():
    """Sensibilita' richiesta dal brief: gas 30 EUR/MWh."""
    bc = _variante(prezzo_gas_eur_mwh=30)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(7520.833333333343)
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] == pytest.approx(-221936.32183785015)
    assert bc["van"] < 0.0
    assert bc["tir"] is None or bc["tir"] < 0.0
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_prezzo_el_alto_non_conviente():
    bc = _variante(prezzo_el_eur_mwh=200)
    assert bc["risparmio_eur_anno"] == pytest.approx(10250.0)
    assert bc["van"] == pytest.approx(-193608.50510864897)
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(242.05128205128204)
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_variante_prezzo_el_zero_conviente():
    bc = _variante(prezzo_el_eur_mwh=0.0)
    assert bc["c_alt_var_eur_anno"] == pytest.approx(26000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(41000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(59000.0)
    assert bc["van"] == pytest.approx(312399.82425265474)
    assert bc["tir"] == pytest.approx(18.03054987949297, abs=1e-4)
    assert bc["payback"] == 6
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_variante_gas_alto_conviente():
    bc = _variante(prezzo_gas_eur_mwh=150)
    assert bc["risparmio_eur_anno"] == pytest.approx(204854.16666666666)
    assert bc["van"] == pytest.approx(1826316.1976964525)
    assert bc["tir"] == pytest.approx(68.25687825320497, abs=1e-4)
    assert bc["payback"] == 2
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_variante_gas_marginale():
    bc = _variante(prezzo_gas_eur_mwh=43)
    assert bc["risparmio_eur_anno"] == pytest.approx(28898.61111111111)
    assert bc["van"] == pytest.approx(-42.29888830067466)
    assert bc["van"] < 0.0
    assert abs(bc["van"]) <= 0.10 * 300000
    assert bc["tir"] == pytest.approx(4.997913981004384, abs=1e-4)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"
    assert bc["valid"] is True


def test_variante_quota_zero_calcolabile_non_degenere():
    """Sensibilita' richiesta dal brief: quota PdC 0 %."""
    bc = _variante(quota_pdc_pct=0)
    assert bc["valid"] is True
    assert bc["q_pdc_mwh_anno"] == 0.0
    assert bc["e_el_mwh_anno"] == 0.0
    assert bc["gas_res_mwh_anno"] == pytest.approx(1444.4444444444443)
    assert bc["risparmio_eur_anno"] == 20000.0
    assert bc["van"] == pytest.approx(-92406.8392363882)
    assert bc["co2_evitata_t_anno"] == pytest.approx(155.5555555555556)
    assert bc["tir"] == pytest.approx(0.0, abs=1e-6)
    assert bc["payback"] == 15
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_quota_recupero_cento_calcolabile_non_degenere():
    """Sensibilita' richiesta dal brief: recupero 100 %."""
    bc = _variante(quota_recupero_pct=100)
    assert bc["valid"] is True
    assert bc["q_netto_mwh_anno"] == 0.0
    assert bc["q_pdc_mwh_anno"] == 0.0
    assert bc["e_el_mwh_anno"] == 0.0
    assert bc["gas_res_mwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == 85000.0
    assert bc["van"] == pytest.approx(582270.9332453503)
    assert bc["tir"] == pytest.approx(27.601410040902742, abs=1e-4)
    assert bc["payback"] == 4
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_quota_recupero_zero():
    bc = _variante(quota_recupero_pct=0)
    assert bc["q_netto_mwh_anno"] == pytest.approx(2000.0)
    assert bc["q_pdc_mwh_anno"] == pytest.approx(1200.0)
    assert bc["e_el_mwh_anno"] == pytest.approx(375.0)
    assert bc["gas_res_mwh_anno"] == pytest.approx(888.8888888888889)
    assert bc["risparmio_eur_anno"] == pytest.approx(3750.0)
    assert bc["van"] == pytest.approx(-261076.28235682275)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(120.0)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_cop_basso_e_alto():
    bc = _variante(cop=2.0)
    assert bc["e_el_mwh_anno"] == pytest.approx(390.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(16100.0)
    assert bc["van"] == pytest.approx(-132887.50558529253)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(151.28205128205127)
    assert bc["verdetto"] == "NON_CONVIENTE"
    bc2 = _variante(cop=5.0)
    assert bc2["e_el_mwh_anno"] == pytest.approx(156.0)
    assert bc2["risparmio_eur_anno"] == pytest.approx(41840.0)
    assert bc2["van"] == pytest.approx(134284.89231747587)
    assert bc2["tir"] == pytest.approx(11.052261605989253, abs=1e-4)
    assert bc2["payback"] == 8
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_co2_evitata_negativa_con_fattore_el_alto():
    bc = _variante(f_el_t_per_mwh=1.50)
    assert bc["co2_alt_t_anno"] == pytest.approx(481.18055555555554)
    assert bc["co2_evitata_t_anno"] == pytest.approx(-36.736111111111086)
    assert bc["co2_evitata_t_anno"] < 0.0
    assert bc["van"] == pytest.approx(34095.24310393778)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_pareggio_negativo():
    bc = _variante(om_fisso_eur_anno=5000000)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(-20209.23076923077)
    assert bc["prezzo_pareggio_eur_mwh"] < 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(-4952812.5)
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_variante_pareggio_zero():
    bc = _variante(om_fisso_eur_anno=74000)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(0.0, abs=1e-9)
    assert bc["risparmio_eur_anno"] == pytest.approx(-26812.5)


def test_variante_wacc_zero():
    bc = _variante(wacc_pct=0)
    assert bc["crf"] == pytest.approx(1.0 / 15.0)
    assert bc["quota_capex_eur_anno"] == pytest.approx(20000.0)
    assert bc["lco_alt_eur_kg"] == pytest.approx(0.0109765625)
    assert bc["van"] == pytest.approx(182812.5)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex_eur=0)
    assert bc["capex_eur"] == 0
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(334095.2431039377)
    assert bc["lco_alt_eur_kg"] == pytest.approx(0.0084765625)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_vita_dieci():
    bc = _variante(vita_anni=10)
    assert len(bc["flussi"]) == 11
    assert bc["crf"] == pytest.approx(0.12950457496545661)
    assert bc["van"] == pytest.approx(-51456.65696686387)
    assert bc["tir"] == pytest.approx(1.3005565192390205, abs=1e-4)
    assert bc["payback"] == 10
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_input_nulli_calcolabile_non_degenere():
    bc = _variante(prezzo_el_eur_mwh=0.0, prezzo_gas_eur_mwh=0,
                   om_fisso_eur_anno=0)
    assert bc["valid"] is True
    assert bc["c_base_eur_anno"] == 0.0
    assert bc["c_alt_eur_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == 0.0
    assert bc["van"] == -300000.0
    assert bc["verdetto"] == "NON_CONVIENTE"


# ---------------------------------------------------------------- degenere
def test_degenere_kg_zero():
    bc = _variante(kg_anno=0)
    assert bc["valid"] is False
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"] == []
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["lco_base_eur_kg"] is None
    assert bc["lco_alt_eur_kg"] is None
    assert bc["errore"]


def test_degenere_calore_cop_vita():
    for kw in ({"calore_kWh_per_1000kg": 0}, {"calore_kWh_per_1000kg": -5},
               {"cop": 0}, {"cop": -1},
               {"kg_anno": 0},
               {"kg_anno": -1},
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
    for kw in ({"kg_anno": "300000"},
               {"kg_anno": float("nan")},
               {"prezzo_el_eur_mwh": float("inf")},
               {"capex_eur": True}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_neutro_campi():
    bc = _variante(kg_anno=0)
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
    assert mh760_prezzo_pareggio(100000.0, 577.7777777777777, 45, 15000,
                                 0.0) is None
    assert mh760_prezzo_pareggio(100000.0, 577.7777777777777, 45, 15000,
                                 None) is None
    assert mh760_lco_base(100000.0, 0) is None
    assert mh760_e_el(780.0, 0) is None
    bc = _variante(quota_pdc_pct=0)
    assert bc["prezzo_pareggio_eur_mwh"] is None


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = demo_calcoli()
    testo = mh760_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert "q_lordo_mwh_anno;2000.0" in testo
    assert "q_netto_mwh_anno;1300.0" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "prezzo_pareggio_eur_mwh" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = demo_calcoli()
    testo = mh760_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"quota_capex_eur_anno;{bc['quota_capex_eur_anno']}" in testo
    assert f"q_lordo_mwh_anno;{bc['q_lordo_mwh_anno']}" in testo


def test_csv_degenere_solo_zeri():
    bc = _variante(kg_anno=0)
    testo = mh760_csv(bc, _demo_kwargs())
    assert "van_eur;0.0" in testo
    assert "q_lordo_mwh_anno;0.0" in testo
    assert "verdetto;NON_CALCOLABILE" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = demo_calcoli()
    testo = mh760_csv(bc, _demo_kwargs())
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
    assert basso - base == pytest.approx(2437.5)
    assert base - alto == pytest.approx(2437.5)


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
    assert set(mh760_demo().keys()) == {
        "kg_anno", "calore_kWh_per_1000kg",
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


def _vietati():
    # Token della tab precedente e dei file precedenti, costruiti
    # per concatenazione: questo stesso file non li contiene
    # come sottostringhe contigue.
    return ["mh" + "75" + "9", "st" + "75" + "9",
            "tab" + "75" + "9", "w" + "76" + "0_",
            "mh" + "75" + "8", "st" + "75" + "8",
            "tab" + "75" + "8", "w" + "75" + "9_"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w761_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w761_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab760:")


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w761_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w761_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st760_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert "key=f" not in src and 'key = f' not in src
    assert "st.stop()" in src
    # guard degenere prima di KPI / grafico / tabella / CSV
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w761_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def760[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w761_ui.py")
        usate = set(re.findall(r'_def760\["([^"]+)"\]', src))
        assert usate
        assert usate <= set(mh760_demo().keys())


def test_ui_chiavi_demo_coerenti():
    """Ogni _def760[...] letto dalla UI esiste nel dict demo:
    sweep anti-KeyError a render (lezione dello sweep chiavi demo vs UI)."""
    src = _leggi("w761_ui.py")
    usate = set(re.findall(r'_def760\["([^"]+)"\]', src))
    assert usate
    assert usate <= set(mh760_demo().keys())


def test_ui_riferisce_solo_helper_nuovi():
    src = _leggi("w761_ui.py")
    usati = set(re.findall(r'\b(mh\d+_\w+)\b', src))
    assert usati
    assert all(u.startswith("mh760_") for u in usati)


@pytest.mark.parametrize("wacc,vita,atteso", [
    (5.0, 15, 0.09634228760924432),
    (0, 15, 1.0 / 15.0),
    (10.0, 10, 0.16274539488251152),
    (5.0, 1, 1.05),
    (50.0, 5, 0.5758293838862559),
])
def test_crf_parametrizzato(wacc, vita, atteso):
    assert mh760_crf(wacc, vita) == pytest.approx(atteso)


@pytest.mark.parametrize("campo,valore", [
    ("kg_anno", 0), ("kg_anno", -3),
    ("calore_kWh_per_1000kg", 0), ("calore_kWh_per_1000kg", -5),
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
    assert mh760_valida(**d)["valido"] is False


def test_df_tabella_valori_demo_selezionati():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Conserve (kg/anno)"] == 8000000.0
    assert mappa["Calore lordo (MWh/anno)"] == pytest.approx(2000.0)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(32187.5)
    assert mappa["Verdetto"] == "CONVIENTE"


def test_lco_alt_minore_di_lco_base_demo():
    bc = demo_calcoli()
    assert bc["lco_alt_eur_kg"] < bc["lco_base_eur_kg"]
    assert bc["lco_base_eur_kg"] - bc["lco_alt_eur_kg"] == pytest.approx(
        0.000410601714653338)
