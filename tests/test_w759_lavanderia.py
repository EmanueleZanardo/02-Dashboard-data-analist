"""Test tab759 "Lavanderia industriale:
lavare a caldo con calore recuperato
e pompa di calore batte la caldaia
a gas?"

Nuova tab tab759 (lavaggio biancheria,
w760). Business case deterministico
del lavaggio a caldo della biancheria
in una lavanderia industriale: la
biancheria va lavata a caldo (calore
per 1000 kg di biancheria) e il calore
puo' arrivare dalla caldaia a gas
(baseline, tutto il calore lordo,
senza recupero) oppure in parte dal
calore recuperato dalle acque reflue
calde di lavaggio e in parte da una
pompa di calore che copre una quota
del calore netto, con il resto che
resta a gas.
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
del caseificio (li' si pastorizza
latte, senza biancheria e senza
recupero dalle acque reflue calde
di lavaggio), dalla cartiera (li'
si essicca carta, senza biancheria
e senza recupero dalle acque reflue
calde), dalla caldaia a elettrodi
generica (li' il calore viene da
elettrodi, senza processo di
lavanderia e senza quota di
recupero) e dal recupero calore
generico (li' il calore recuperato
va a un uso generico, senza
lavaggio biancheria e senza pompa
di calore sul calore netto).

Demo calcolata eseguendo demo_calcoli()
(e ricontrollata a mano, riga per
riga): biancheria 10.000.000 kg/anno,
calore 200 kWh/1000kg, rendimento
caldaia 0,90, quota recupero 40 %,
quota PdC 70 %, COP 3,0, prezzo gas
45 EUR/MWh, prezzo elettrico 110
EUR/MWh, O&M fisso 20.000 EUR/anno,
CAPEX 250.000 EUR, fattore gas 0,20
tCO2/MWh e fattore elettrico 0,25
tCO2/MWh, WACC 5 %, vita 15 anni,
tolleranza 10 % del CAPEX.

- q_lordo_mwh_anno = 2000.0
- q_rec_mwh_anno = 800.0
- q_netto_mwh_anno = 1200.0
- gas_base_mwh_anno = 2222.222222222222
- c_base_eur_anno = 100000.0
- q_pdc_mwh_anno = 840.0
- e_el_mwh_anno = 280.0
- gas_res_mwh_anno = 400.0
- c_alt_var_eur_anno = 48800.0
- c_alt_eur_anno = 68800.0
- risparmio_eur_anno = 31200.0
- co2_base_t_anno = 444.44444444444446
- co2_alt_gas_t_anno = 80.0
- co2_alt_el_t_anno = 70.0
- co2_alt_t_anno = 150.0
- co2_evitata_t_anno = 294.44444444444446
- crf = 0.09634228760924432
- quota_capex_eur_anno = 24085.57190231108
- lco_base_eur_kg = 0.01
- lco_alt_eur_kg = 0.009288557190231108
- van = 73845.33079123445
- tir = 9.101066486064207
- payback = 9
- prezzo_pareggio_eur_mwh = 221.42857142857142
- verdetto = 'CONVIENTE'

Scomposizione: Q_lordo = 10.000.000 x 200 /
1000000 = 2.000 MWh/anno; Q_rec = 0,40 x
2.000 = 800 MWh/anno; Q_netto =
2.000 - 800 = 1.200 MWh/anno;
gas_base = 2.000 / 0,90 = 2.222,22
MWh/anno; C_base = 2.222,22 x 45 =
100.000 EUR/anno; Q_pdc = 0,70 x
1.200 = 840 MWh/anno; E_el = 840 /
3,0 = 280 MWh/anno; gas_res =
0,30 x 1.200 / 0,90 = 400 MWh/anno;
C_alt_var = 400 x 45 + 280 x 110
= 18.000 + 30.800 = 48.800
EUR/anno; C_alt = 48.800 + 20.000 =
68.800 EUR/anno; risparmio = 100.000
- 68.800 = 31.200 EUR/anno; CO2 base
= 2.222,22 x 0,20 = 444,44 t/anno;
CO2 alt = 400 x 0,20 + 280 x
0,25 = 80 + 70 = 150 t/anno;
CO2 evitata = 294,44 t/anno; CRF 0,05
x 1,05^15 / (1,05^15 - 1) =
0.09634228760924432; quota CAPEX
250.000 x 0,096342 = 24.085,57
EUR/anno; LCO base 100.000 / 10.000.000 =
0,0100 EUR/kg; LCO alt (24.085,57 +
20.000) / 10.000.000 + 48.800 / 10.000.000 =
0,0092886 EUR/kg; flussi: anno 0
-250.000, anni 1-15 risparmio
31.200 (piatti); VAN -250.000 +
31.200 x 10,379658 (annuita' 15 anni
al 5 %) = 73.845,33 EUR; TIR 9,10 %;
payback 9 anni (il cumulato all'anno
8 e' -400 EUR, all'anno 9 e'
30.800 EUR); prezzo elettrico di
pareggio (100.000 - 18.000 - 20.000) /
280 = 221,43 EUR/MWh; verdetto
CONVIENTE perche' VAN > 0.
NOTA: il CRF entra solo nel LCO,
mai nei flussi: il CAPEX compare una
sola volta, all'anno 0.
NOTA 2: in questo brief il risparmio
nullo o negativo NON e' degenere:
con prezzo gas 30 EUR/MWh il
risparmio e' 3.866,67 EUR/anno e il
caso resta calcolabile (valid=True,
VAN -209.865,32 EUR, NON_CONVIENTE).
NOTA 3: la CO2 evitata puo' essere
negativa: con fattore elettrico 1,50
tCO2/MWh la CO2 evitata e'
-55,56 t/anno, pur restando il caso
calcolabile.
NOTA 4: il prezzo elettrico di
pareggio puo' essere negativo: con
O&M fisso 5.000.000 EUR/anno il
pareggio e' -17.564,29 EUR/MWh,
perche' il solo O&M fisso piu' il
gas residuo superano gia' il costo
baseline (il caso demo ha pareggio
positivo, 221,43 EUR/MWh).
NOTA 5: la quota PdC zero NON e'
degenere: con quota 0 il risparmio
e' 20.000 EUR/anno, la VAN
-42.406,84 EUR e il pareggio non
e' definito (E_el nulla).
NOTA 6: il calore netto nullo (quota
recupero 100 %) NON e' degenere:
il risparmio e' 80.000 EUR/anno
(100.000 - 20.000 di solo O&M fisso)
e la VAN 580.372,64 EUR, e il
pareggio non e' definito.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w760_helpers import (
    demo_calcoli,
    mh759_c_alt,
    mh759_c_alt_var,
    mh759_c_base,
    mh759_calcola,
    mh759_co2_alt,
    mh759_co2_base,
    mh759_co2_evitata,
    mh759_crf,
    mh759_csv,
    mh759_demo,
    mh759_e_el,
    mh759_eta,
    mh759_flussi,
    mh759_gas_base,
    mh759_gas_res,
    mh759_int_pos,
    mh759_lco_alt,
    mh759_lco_base,
    mh759_nneg,
    mh759_num,
    mh759_payback,
    mh759_pct_0_100,
    mh759_pct_wacc,
    mh759_pos,
    mh759_prezzo_pareggio,
    mh759_q_lordo,
    mh759_q_netto,
    mh759_q_pdc,
    mh759_q_rec,
    mh759_quota_capex,
    mh759_risparmio,
    mh759_tir,
    mh759_valida,
    mh759_van,
    mh759_verdetto,
)


def _demo_kwargs():
    return dict(mh759_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh759_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh759_num(3, "x") == 3.0
    assert mh759_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh759_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh759_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh759_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh759_pos(0, "x")
    with pytest.raises(ValueError):
        mh759_pos(-1, "x")
    assert mh759_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh759_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh759_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh759_int_pos(0, "x")


def test_pct_0_100_limiti():
    assert mh759_pct_0_100(0, "x") == 0.0
    assert mh759_pct_0_100(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh759_pct_0_100(100.1, "x")
    with pytest.raises(ValueError):
        mh759_pct_0_100(-1, "x")


def test_pct_wacc_limiti():
    assert mh759_pct_wacc(0, "x") == 0.0
    assert mh759_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh759_pct_wacc(50.1, "x")


def test_eta_limiti():
    assert mh759_eta(1.0, "x") == 1.0
    assert mh759_eta(0.90, "x") == 0.90
    with pytest.raises(ValueError):
        mh759_eta(0, "x")
    with pytest.raises(ValueError):
        mh759_eta(-0.1, "x")
    with pytest.raises(ValueError):
        mh759_eta(1.01, "x")


# ---------------------------------------------------------------- fisica base
def test_q_lordo_rec_netto():
    assert mh759_q_lordo(10000000, 200) == pytest.approx(2000.0)
    assert mh759_q_lordo(10000000, 0) == 0.0
    assert mh759_q_rec(2000.0, 40.0) == pytest.approx(800.0)
    assert mh759_q_rec(2000.0, 0) == 0.0
    assert mh759_q_rec(2000.0, 100) == 2000.0
    assert mh759_q_netto(2000.0, 800.0) == pytest.approx(1200.0)
    assert mh759_q_netto(2000.0, 2000.0) == 0.0
    with pytest.raises(ValueError):
        mh759_q_rec(2000.0, 100.1)
    with pytest.raises(ValueError):
        mh759_q_lordo(10000000, -1)


def test_gas_base_e_c_base_e_co2_base():
    assert mh759_gas_base(2000.0, 0.90) == pytest.approx(2222.222222222222)
    assert mh759_gas_base(2000.0, 1.0) == 2000.0
    assert mh759_c_base(2222.222222222222, 45) == pytest.approx(100000.0)
    assert mh759_co2_base(2222.222222222222, 0.20) == pytest.approx(
        444.44444444444446)
    with pytest.raises(ValueError):
        mh759_gas_base(2000.0, 0)
    with pytest.raises(ValueError):
        mh759_c_base(2222.222222222222, -1)


def test_q_pdc_e_e_el():
    assert mh759_q_pdc(1200.0, 70.0) == pytest.approx(840.0)
    assert mh759_q_pdc(1200.0, 0) == 0.0
    assert mh759_q_pdc(1200.0, 100) == 1200.0
    assert mh759_e_el(840.0, 3.0) == pytest.approx(280.0)
    assert mh759_e_el(840.0, 0) is None
    assert mh759_e_el(840.0, -1.0) is None
    assert mh759_e_el(0.0, 3.0) == 0.0
    with pytest.raises(ValueError):
        mh759_q_pdc(1200.0, 100.1)


def test_gas_res():
    assert mh759_gas_res(1200.0, 70.0, 0.90) == pytest.approx(400.0)
    assert mh759_gas_res(1200.0, 0, 0.90) == pytest.approx(1333.3333333333333)
    assert mh759_gas_res(1200.0, 100, 0.90) == 0.0
    with pytest.raises(ValueError):
        mh759_gas_res(1200.0, 70.0, 0)


def test_c_alt_var_e_c_alt():
    assert mh759_c_alt_var(400.0, 45, 280.0,
                           110) == pytest.approx(48800.0)
    assert mh759_c_alt_var(400.0, 45, 0.0, 110) == pytest.approx(18000.0)
    assert mh759_c_alt(48800.0, 20000) == pytest.approx(68800.0)
    assert mh759_c_alt(48800.0, 0) == pytest.approx(48800.0)
    with pytest.raises(ValueError):
        mh759_c_alt_var(400.0, -1, 280.0, 110)


def test_risparmio_segno():
    assert mh759_risparmio(100000.0, 68800.0) == pytest.approx(31200.0)
    assert mh759_risparmio(100000.0, 100000.0) == 0.0
    assert mh759_risparmio(100000.0, 50000.0) == 50000.0


def test_co2_alt_e_evitata_segno_libero():
    assert mh759_co2_alt(400.0, 0.20, 280.0,
                         0.25) == pytest.approx(150.0)
    assert mh759_co2_evitata(444.44444444444446,
                             150.0) == pytest.approx(
        294.44444444444446)
    assert mh759_co2_evitata(444.44444444444446,
                             444.44444444444446) == pytest.approx(0.0)
    assert mh759_co2_evitata(444.44444444444446,
                             1044.44444444444446) == pytest.approx(
        -600.0, abs=1e-6)


# ---------------------------------------------------------------- finanza base
def test_crf():
    assert mh759_crf(5.0, 15) == pytest.approx(0.09634228760924432)
    assert mh759_crf(0, 15) == pytest.approx(1.0 / 15.0)
    assert mh759_crf(5.0, 1) == pytest.approx(1.05)
    assert mh759_crf(5.0, 10) == pytest.approx(0.12950457496545661)


def test_quota_capex_e_lco():
    assert mh759_quota_capex(250000, 0.09634228760924432) == pytest.approx(
        24085.57190231108)
    assert mh759_lco_base(100000.0, 10000000) == pytest.approx(0.01)
    assert mh759_lco_base(100000.0, 0) is None
    assert mh759_lco_alt(250000, 0.09634228760924432, 20000,
                         48800.0, 10000000) == pytest.approx(
        0.009288557190231108)
    assert mh759_lco_alt(250000, 0.09634228760924432, 20000,
                         48800.0, 0) is None
    assert mh759_lco_alt(0, 0.09634228760924432, 20000,
                         48800.0, 10000000) == pytest.approx(0.00688)


def test_prezzo_pareggio_formula_brief_negativo_e_none():
    assert mh759_prezzo_pareggio(100000.0, 400.0, 45, 20000,
                                 280.0) == pytest.approx(
        221.42857142857142)
    assert mh759_prezzo_pareggio(100000.0, 400.0, 45, 82000,
                                 280.0) == pytest.approx(0.0, abs=1e-9)
    assert mh759_prezzo_pareggio(100000.0, 400.0, 45, 20000,
                                 0.0) is None
    assert mh759_prezzo_pareggio(100000.0, 400.0, 45, 20000,
                                 None) is None
    assert mh759_prezzo_pareggio(100000.0, 0.0, 45, 0,
                                 280.0) == pytest.approx(
        357.14285714285714)


def test_flussi_lunghezza_e_primo():
    fl = mh759_flussi(250000, 31200.0, 15)
    assert len(fl) == 16
    assert fl[0] == -250000
    assert all(f == 31200.0 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = demo_calcoli()
    assert bc["van"] == pytest.approx(73845.33079123445)
    assert mh759_van([-250000] + [31200.0] * 15,
                     0) == pytest.approx(218000.0)
    assert mh759_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo_e_conviente():
    bc = demo_calcoli()
    assert bc["tir"] == pytest.approx(9.101066486064207)
    assert mh759_tir([-250000] + [31200.0] * 15) == pytest.approx(
        0.09101066486064207)
    tir = mh759_tir([-250000] + [31200.0] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-250000] + [31200.0] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback():
    assert mh759_payback([-250000] + [31200.0] * 15) == 9
    assert mh759_payback([-250000] + [-1000.0] * 15) is None
    assert mh759_payback([0] + [31200.0] * 15) == 0
    assert mh759_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh759_verdetto(100.0, 250000, 10.0) == "CONVIENTE"
    assert mh759_verdetto(-24000.0, 250000, 10.0) == "MARGINALE"
    assert mh759_verdetto(-25000.0, 250000, 10.0) == "MARGINALE"
    assert mh759_verdetto(-25000.01, 250000, 10.0) == "NON_CONVIENTE"
    assert mh759_verdetto(float("nan"), 250000, 10.0) == "NON_CALCOLABILE"
    assert mh759_verdetto(0.0, 0, 10.0) == "MARGINALE"


def test_valida_demo_ok():
    v = mh759_valida(**_demo_kwargs())
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
        assert mh759_valida(**d)["valido"] is False


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
        assert mh759_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"quota_recupero_pct": 0, "quota_pdc_pct": 0,
              "prezzo_gas_eur_mwh": 0,
              "prezzo_el_eur_mwh": 0, "om_fisso_eur_anno": 0,
              "capex_eur": 0, "f_gas_t_per_mwh": 0,
              "f_el_t_per_mwh": 0, "wacc_pct": 0,
              "tolleranza_pct": 0, "eta_caldaia": 1.0})
    assert mh759_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["quota_pdc_pct"] = 100
    d["quota_recupero_pct"] = 100
    assert mh759_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh759_demo()
    assert d["kg_anno"] == 10000000
    assert d["calore_kWh_per_1000kg"] == 200
    assert d["eta_caldaia"] == 0.90
    assert d["quota_recupero_pct"] == 40.0
    assert d["quota_pdc_pct"] == 70.0
    assert d["cop"] == 3.0
    assert d["prezzo_gas_eur_mwh"] == 45
    assert d["prezzo_el_eur_mwh"] == 110
    assert d["om_fisso_eur_anno"] == 20000
    assert d["capex_eur"] == 250000
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
        "q_rec_mwh_anno": 800.0,
        "q_netto_mwh_anno": 1200.0,
        "gas_base_mwh_anno": 2222.222222222222,
        "c_base_eur_anno": 100000.0,
        "q_pdc_mwh_anno": 840.0,
        "e_el_mwh_anno": 280.0,
        "gas_res_mwh_anno": 400.0,
        "c_alt_var_eur_anno": 48800.0,
        "c_alt_eur_anno": 68800.0,
        "risparmio_eur_anno": 31200.0,
        "co2_base_t_anno": 444.44444444444446,
        "co2_alt_t_anno": 150.0,
        "co2_evitata_t_anno": 294.44444444444446,
        "crf": 0.09634228760924432,
        "quota_capex_eur_anno": 24085.57190231108,
        "lco_base_eur_kg": 0.01,
        "lco_alt_eur_kg": 0.009288557190231108,
        "van": 73845.33079123445,
        "tir": 9.101066486064207,
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
    assert bc["q_lordo_mwh_anno"] == pytest.approx(2000.0)
    assert bc["q_rec_mwh_anno"] == pytest.approx(800.0)
    assert bc["q_netto_mwh_anno"] == pytest.approx(1200.0)
    assert bc["gas_base_mwh_anno"] == pytest.approx(2222.222222222222)
    assert bc["co2_evitata_t_anno"] == pytest.approx(294.44444444444446)


def test_demo_calcoli_economia():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] == 100000.0
    assert bc["c_alt_var_eur_anno"] == pytest.approx(48800.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(68800.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(31200.0)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(221.42857142857142)


def test_demo_calcoli_finanza():
    bc = demo_calcoli()
    assert bc["crf"] == pytest.approx(0.09634228760924432)
    assert bc["quota_capex_eur_anno"] == pytest.approx(24085.57190231108)
    assert bc["lco_base_eur_kg"] == pytest.approx(0.01)
    assert bc["lco_alt_eur_kg"] == pytest.approx(0.009288557190231108)
    assert bc["van"] == pytest.approx(73845.33079123445)
    assert bc["tir"] == pytest.approx(9.101066486064207)
    assert bc["payback"] == 9
    assert bc["verdetto"] == "CONVIENTE"


def test_demo_flussi_e_cumulato():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -250000
    assert len(bc["flussi"]) == 16
    assert all(f == 31200.0 for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -250000
    assert righe.iloc[5]["Cumulato (EUR)"] == pytest.approx(-94000.0)
    assert righe.iloc[8]["Cumulato (EUR)"] == pytest.approx(-400.0)
    assert righe.iloc[9]["Cumulato (EUR)"] == pytest.approx(30800.0)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(218000.0)
    assert righe.iloc[15]["Flusso (EUR/anno)"] == 31200.0


def test_demo_tabella_righe():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Calore lordo (MWh/anno)"] == pytest.approx(2000.0)
    assert mappa["Calore recuperato (MWh/anno)"] == pytest.approx(800.0)
    assert mappa["Calore netto (MWh/anno)"] == pytest.approx(1200.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(68800.0)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(31200.0)
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
    van_da_flussi = mh759_van(bc["flussi"], bc["wacc_pct"])
    assert van_da_flussi == pytest.approx(bc["van"])
    assert bc["lco_alt_eur_kg"] == pytest.approx(
        (bc["capex_eur"] * bc["crf"] + bc["om_fisso_eur_anno"]) /
        bc["kg_anno"] + bc["c_alt_var_eur_anno"] /
        bc["kg_anno"])


def test_demo_contro_riconteggio_indipendente():
    kg, cal, eta, qr, quota, cop = 10000000, 200, 0.90, 40.0, 70.0, 3.0
    pg, pe, om, cx = 45, 110, 20000, 250000
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
    assert bc["van"] == pytest.approx(-250000 + 31200.0 * annuita)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(
        (100000.0 - 18000.0 - 20000) / 280.0)
    assert bc["flussi"][0] + 15 * bc["flussi"][1] == pytest.approx(
        218000.0)
    assert bc["flussi"][0] + 8 * bc["flussi"][1] == pytest.approx(
        -400.0)


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
    assert bc["risparmio_eur_anno"] == pytest.approx(3866.6666666666715)
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] == pytest.approx(-209865.32225236832)
    assert bc["van"] < 0.0
    assert bc["tir"] is None or bc["tir"] < 0.0
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_prezzo_el_alto_non_conviente():
    bc = _variante(prezzo_el_eur_mwh=200)
    assert bc["risparmio_eur_anno"] == pytest.approx(6000.0)
    assert bc["van"] == pytest.approx(-187722.05177091647)
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(221.42857142857142)
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_variante_prezzo_el_zero_conviente():
    bc = _variante(prezzo_el_eur_mwh=0.0)
    assert bc["c_alt_var_eur_anno"] == pytest.approx(18000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(38000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(62000.0)
    assert bc["van"] == pytest.approx(393538.7983671966)
    assert bc["tir"] == pytest.approx(23.790405707953994, abs=1e-4)
    assert bc["payback"] == 5
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_variante_gas_alto_conviente():
    bc = _variante(prezzo_gas_eur_mwh=150)
    assert bc["risparmio_eur_anno"] == pytest.approx(222533.3333333333)
    assert bc["van"] == pytest.approx(2059819.9020964536)
    assert bc["payback"] == 2
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_variante_gas_marginale():
    bc = _variante(prezzo_gas_eur_mwh=41)
    assert bc["risparmio_eur_anno"] == pytest.approx(23911.11111111111)
    assert bc["van"] == pytest.approx(-1810.8433537263045)
    assert bc["van"] < 0.0
    assert abs(bc["van"]) <= 0.10 * 250000
    assert bc["tir"] == pytest.approx(4.8926448144593975, abs=1e-4)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"
    assert bc["valid"] is True


def test_variante_quota_zero_calcolabile_non_degenere():
    """Sensibilita' richiesta dal brief: quota PdC 0 %."""
    bc = _variante(quota_pdc_pct=0)
    assert bc["valid"] is True
    assert bc["q_pdc_mwh_anno"] == 0.0
    assert bc["e_el_mwh_anno"] == 0.0
    assert bc["gas_res_mwh_anno"] == pytest.approx(1333.3333333333333)
    assert bc["risparmio_eur_anno"] == 20000.0
    assert bc["van"] == pytest.approx(-42406.839236388194)
    assert bc["co2_evitata_t_anno"] == pytest.approx(177.77777777777777)
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
    assert bc["risparmio_eur_anno"] == 80000.0
    assert bc["van"] == pytest.approx(580372.6430544471)
    assert bc["tir"] == pytest.approx(31.471977991973578, abs=1e-4)
    assert bc["payback"] == 4
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_quota_recupero_zero():
    bc = _variante(quota_recupero_pct=0)
    assert bc["q_netto_mwh_anno"] == pytest.approx(2000.0)
    assert bc["q_pdc_mwh_anno"] == pytest.approx(1400.0)
    assert bc["e_el_mwh_anno"] == pytest.approx(466.6666666666667)
    assert bc["gas_res_mwh_anno"] == pytest.approx(666.6666666666667)
    assert bc["risparmio_eur_anno"] == pytest.approx(-1333.333333333343)
    assert bc["van"] == pytest.approx(-263839.5440509076)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(107.14285714285714)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_cop_basso_e_alto():
    bc = _variante(cop=2.0)
    assert bc["e_el_mwh_anno"] == pytest.approx(420.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(15800.0)
    assert bc["van"] == pytest.approx(-86001.40299674663)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(147.61904761904762)
    assert bc["verdetto"] == "NON_CONVIENTE"
    bc2 = _variante(cop=5.0)
    assert bc2["e_el_mwh_anno"] == pytest.approx(168.0)
    assert bc2["risparmio_eur_anno"] == pytest.approx(43520.0)
    assert bc2["van"] == pytest.approx(201722.7178216193)
    assert bc2["tir"] == pytest.approx(15.369033677495903, abs=1e-4)
    assert bc2["payback"] == 6
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_co2_evitata_negativa_con_fattore_el_alto():
    bc = _variante(f_el_t_per_mwh=1.50)
    assert bc["co2_alt_t_anno"] == pytest.approx(500.0)
    assert bc["co2_evitata_t_anno"] == pytest.approx(-55.55555555555554)
    assert bc["co2_evitata_t_anno"] < 0.0
    assert bc["van"] == pytest.approx(73845.33079123445)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_pareggio_negativo():
    bc = _variante(om_fisso_eur_anno=5000000)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(-17564.285714285714)
    assert bc["prezzo_pareggio_eur_mwh"] < 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(-4948800.0)
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_variante_pareggio_zero():
    bc = _variante(om_fisso_eur_anno=82000)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(0.0, abs=1e-9)
    assert bc["risparmio_eur_anno"] == pytest.approx(-30800.0)


def test_variante_wacc_zero():
    bc = _variante(wacc_pct=0)
    assert bc["crf"] == pytest.approx(1.0 / 15.0)
    assert bc["quota_capex_eur_anno"] == pytest.approx(16666.666666666668)
    assert bc["lco_alt_eur_kg"] == pytest.approx(0.008546666666666668)
    assert bc["van"] == pytest.approx(218000.0)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex_eur=0)
    assert bc["capex_eur"] == 0
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(323845.3307912344)
    assert bc["lco_alt_eur_kg"] == pytest.approx(0.00688)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_vita_dieci():
    bc = _variante(vita_anni=10)
    assert len(bc["flussi"]) == 11
    assert bc["crf"] == pytest.approx(0.12950457496545661)
    assert bc["van"] == pytest.approx(-9081.870209433866)
    assert bc["tir"] == pytest.approx(4.245122315835656, abs=1e-4)
    assert bc["payback"] == 9
    assert bc["verdetto"] == "MARGINALE"


def test_variante_input_nulli_calcolabile_non_degenere():
    bc = _variante(prezzo_el_eur_mwh=0.0, prezzo_gas_eur_mwh=0,
                   om_fisso_eur_anno=0)
    assert bc["valid"] is True
    assert bc["c_base_eur_anno"] == 0.0
    assert bc["c_alt_eur_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == 0.0
    assert bc["van"] == -250000.0
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
    assert mh759_prezzo_pareggio(100000.0, 400.0, 45, 20000,
                                 0.0) is None
    assert mh759_prezzo_pareggio(100000.0, 400.0, 45, 20000,
                                 None) is None
    assert mh759_lco_base(100000.0, 0) is None
    assert mh759_e_el(840.0, 0) is None
    bc = _variante(quota_pdc_pct=0)
    assert bc["prezzo_pareggio_eur_mwh"] is None


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = demo_calcoli()
    testo = mh759_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert "q_lordo_mwh_anno;2000.0" in testo
    assert "q_netto_mwh_anno;1200.0" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "prezzo_pareggio_eur_mwh" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = demo_calcoli()
    testo = mh759_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"quota_capex_eur_anno;{bc['quota_capex_eur_anno']}" in testo
    assert f"q_lordo_mwh_anno;{bc['q_lordo_mwh_anno']}" in testo


def test_csv_degenere_solo_zeri():
    bc = _variante(kg_anno=0)
    testo = mh759_csv(bc, _demo_kwargs())
    assert "van_eur;0.0" in testo
    assert "q_lordo_mwh_anno;0.0" in testo
    assert "verdetto;NON_CALCOLABILE" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = demo_calcoli()
    testo = mh759_csv(bc, _demo_kwargs())
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
    assert basso - base == pytest.approx(2800.0)
    assert base - alto == pytest.approx(2800.0)


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
    assert set(mh759_demo().keys()) == {
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


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w760_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w760_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab759:")


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    # token vietati costruiti per concatenazione, cosi' questo
    # stesso file non li contiene come sottostringhe contigue.
    src = _leggi("w760_helpers.py")
    vietati = ["mh" + "75" + "8", "st" + "75" + "8",
               "tab" + "75" + "8", "w" + "75" + "9",
               "mh" + "75" + "7", "tab" + "75" + "7", "st" + "75" + "7"]
    assert "streamlit" not in src
    assert all(t not in src for t in vietati)


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w760_ui.py")
    vietati = ["mh" + "75" + "8", "st" + "75" + "8",
               "tab" + "75" + "8", "w" + "75" + "9",
               "mh" + "75" + "7", "tab" + "75" + "7", "st" + "75" + "7"]
    assert all(t not in src for t in vietati)
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st759_") for c in chiavi)
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
    src = _leggi("w760_test.py")
    vietati = ["mh" + "75" + "8", "st" + "75" + "8",
               "tab" + "75" + "8", "w" + "75" + "9",
               "mh" + "75" + "7", "tab" + "75" + "7", "st" + "75" + "7"]
    assert all(t not in src for t in vietati)


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def759[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w760_ui.py")
        usate = set(re.findall(r'_def759\["([^"]+)"\]', src))
        assert usate
        assert usate <= set(mh759_demo().keys())


def test_ui_chiavi_demo_coerenti():
    """Ogni _def759[...] letto dalla UI esiste nel dict demo:
    sweep anti-KeyError a render (lezione dello sweep chiavi demo vs UI)."""
    src = _leggi("w760_ui.py")
    usate = set(re.findall(r'_def759\["([^"]+)"\]', src))
    assert usate
    assert usate <= set(mh759_demo().keys())


def test_ui_riferisce_solo_helper_nuovi():
    src = _leggi("w760_ui.py")
    usati = set(re.findall(r'\b(mh\d+_\w+)\b', src))
    assert usati
    assert all(u.startswith("mh759_") for u in usati)


@pytest.mark.parametrize("wacc,vita,atteso", [
    (5.0, 15, 0.09634228760924432),
    (0, 15, 1.0 / 15.0),
    (10.0, 10, 0.16274539488251152),
    (5.0, 1, 1.05),
    (50.0, 5, 0.5758293838862559),
])
def test_crf_parametrizzato(wacc, vita, atteso):
    assert mh759_crf(wacc, vita) == pytest.approx(atteso)


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
    assert mh759_valida(**d)["valido"] is False


def test_df_tabella_valori_demo_selezionati():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Biancheria (kg/anno)"] == 10000000.0
    assert mappa["Calore lordo (MWh/anno)"] == pytest.approx(2000.0)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(31200.0)
    assert mappa["Verdetto"] == "CONVIENTE"


def test_lco_alt_minore_di_lco_base_demo():
    bc = demo_calcoli()
    assert bc["lco_alt_eur_kg"] < bc["lco_base_eur_kg"]
    assert bc["lco_base_eur_kg"] - bc["lco_alt_eur_kg"] == pytest.approx(
        0.000711442809768892)
