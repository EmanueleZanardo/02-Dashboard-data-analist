"""Test tab757 "Birrificio: bollire il
mosto con calore recuperato e pompa
di calore batte la caldaia a gas?"

Nuova tab tab757 (bollitura mosto,
w758). Business case deterministico
della bollitura del mosto in un
birrificio: il mosto va bollito
(calore per hl di birra) e il calore
puo' arrivare dalla caldaia a gas
(baseline, tutto il calore lordo,
senza recupero) oppure in parte dal
calore recuperato dal raffreddamento
del mosto e in parte da una pompa di
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
senza mosto e senza recupero dal
raffreddamento del mosto), dalla
caldaia a elettrodi
generica (li' il calore viene da
elettrodi, senza processo birra e
senza quota di recupero) e dal
recupero calore generico (li' il
calore recuperato va a un uso
generico, senza bollitura mosto e
senza pompa di calore ad alta
temperatura sul calore netto).

Demo calcolata eseguendo demo_calcoli()
(e ricontrollata a mano, riga per riga):
produzione 300.000 hl/anno, calore
40 kWh/hl, rendimento caldaia 0,90,
quota recupero 30 %, quota PdC 70 %,
COP 3,2, prezzo gas 45 EUR/MWh,
prezzo elettrico 110 EUR/MWh, O&M
fisso 80.000 EUR/anno, CAPEX
1.200.000 EUR, fattore gas 0,20
tCO2/MWh e fattore elettrico 0,25
tCO2/MWh, WACC 5 %, vita 15 anni,
tolleranza 10 % del CAPEX.

- q_lordo_mwh_anno = 12000.0
- q_rec_mwh_anno = 3600.0
- q_netto_mwh_anno = 8400.0
- gas_base_mwh_anno = 13333.333333333332
- c_base_eur_anno = 600000.0
- q_pdc_mwh_anno = 5880.0
- e_el_mwh_anno = 1837.5
- gas_res_mwh_anno = 2800.0
- c_alt_var_eur_anno = 328125.0
- c_alt_eur_anno = 408125.0
- risparmio_eur_anno = 191875.0
- co2_base_t_anno = 2666.6666666666665
- co2_alt_gas_t_anno = 560.0
- co2_alt_el_t_anno = 459.375
- co2_alt_t_anno = 1019.375
- co2_evitata_t_anno = 1647.2916666666665
- crf = 0.09634228760924432
- quota_capex_eur_anno = 115610.74513109318
- lco_base_eur_hl = 2.0
- lco_alt_eur_hl = 1.745785817103644
- van = 791596.8860759008
- tir = 13.64095711599196
- payback = 7
- prezzo_pareggio_eur_mwh = 214.42176870748298
- verdetto = 'CONVIENTE'

Scomposizione: Q_lordo = 300.000 x 40 /
1000 = 12.000 MWh/anno; Q_rec = 0,30 x
12.000 = 3.600 MWh/anno; Q_netto =
12.000 - 3.600 = 8.400 MWh/anno;
gas_base = 12.000 / 0,90 = 13.333,33
MWh/anno; C_base = 13.333,33 x 45 =
600.000 EUR/anno; Q_pdc = 0,70 x
8.400 = 5.880 MWh/anno; E_el = 5.880 /
3,2 = 1.837,50 MWh/anno; gas_res =
0,30 x 8.400 / 0,90 = 2.800 MWh/anno;
C_alt_var = 2.800 x 45 + 1.837,50 x 110
= 126.000 + 202.125 = 328.125
EUR/anno; C_alt = 328.125 + 80.000 =
408.125 EUR/anno; risparmio = 600.000
- 408.125 = 191.875 EUR/anno; CO2 base
= 13.333,33 x 0,20 = 2.666,67 t/anno;
CO2 alt = 2.800 x 0,20 + 1.837,50 x
0,25 = 560 + 459,38 = 1.019,38 t/anno;
CO2 evitata = 1.647,29 t/anno; CRF 0,05
x 1,05^15 / (1,05^15 - 1) =
0.09634228760924432; quota CAPEX
1.200.000 x 0,096342 = 115.610,75
EUR/anno; LCO base 600.000 / 300.000 =
2,00 EUR/hl; LCO alt (115.610,75 +
80.000) / 300.000 + 328.125 / 300.000 =
1,75 EUR/hl; flussi: anno 0
-1.200.000, anni 1-15 risparmio
191.875 (piatti); VAN -1.200.000 +
191.875 x 10,379658 (annuita' 15 anni
al 5 %) = 791.596,89 EUR; TIR 13,64 %;
payback 7 anni (il cumulato all'anno
6 e' -48.750 EUR, all'anno 7 e'
143.125 EUR); prezzo elettrico di
pareggio (600.000 - 126.000 - 80.000) /
1.837,50 = 214,42 EUR/MWh; verdetto
CONVIENTE perche' VAN > 0.
NOTA: il CRF entra solo nel LCO,
mai nei flussi: il CAPEX compare una
sola volta, all'anno 0.
NOTA 2: in questo brief il risparmio
nullo o negativo NON e' degenere:
con prezzo gas 30 EUR/MWh il
risparmio e' 33.875 EUR/anno e il
caso resta calcolabile (valid=True,
VAN -848.389,08 EUR, NON_CONVIENTE).
NOTA 3: la CO2 evitata puo' essere
negativa: con fattore elettrico 1,50
tCO2/MWh la CO2 evitata e'
-649,58 t/anno, pur restando il caso
calcolabile.
NOTA 4: il prezzo elettrico di
pareggio puo' essere negativo: con
O&M fisso 5.000.000 EUR/anno il
pareggio e' -2.463,13 EUR/MWh,
perche' il solo O&M fisso piu' il
gas residuo superano gia' il costo
baseline (il caso demo ha pareggio
positivo, 214,42 EUR/MWh).
NOTA 5: la quota PdC zero NON e'
degenere: con quota 0 il risparmio
e' 100.000 EUR/anno, la VAN
-162.034,20 EUR e il pareggio non
e' definito (E_el nulla).
NOTA 6: il calore netto nullo (quota
recupero 100 %) NON e' degenere:
il risparmio e' 520.000 EUR/anno
(600.000 - 80.000 di solo O&M fisso)
e la VAN 4.197.422,18 EUR, e il
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

from w758_helpers import (
    demo_calcoli,
    mh757_c_alt,
    mh757_c_alt_var,
    mh757_c_base,
    mh757_calcola,
    mh757_co2_alt,
    mh757_co2_base,
    mh757_co2_evitata,
    mh757_crf,
    mh757_csv,
    mh757_demo,
    mh757_e_el,
    mh757_eta,
    mh757_flussi,
    mh757_gas_base,
    mh757_gas_res,
    mh757_int_pos,
    mh757_lco_alt,
    mh757_lco_base,
    mh757_nneg,
    mh757_num,
    mh757_payback,
    mh757_pct_0_100,
    mh757_pct_wacc,
    mh757_pos,
    mh757_prezzo_pareggio,
    mh757_q_lordo,
    mh757_q_netto,
    mh757_q_pdc,
    mh757_q_rec,
    mh757_quota_capex,
    mh757_risparmio,
    mh757_tir,
    mh757_valida,
    mh757_van,
    mh757_verdetto,
)


def _demo_kwargs():
    return dict(mh757_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh757_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh757_num(3, "x") == 3.0
    assert mh757_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh757_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh757_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh757_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh757_pos(0, "x")
    with pytest.raises(ValueError):
        mh757_pos(-1, "x")
    assert mh757_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh757_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh757_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh757_int_pos(0, "x")


def test_pct_0_100_limiti():
    assert mh757_pct_0_100(0, "x") == 0.0
    assert mh757_pct_0_100(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh757_pct_0_100(100.1, "x")
    with pytest.raises(ValueError):
        mh757_pct_0_100(-1, "x")


def test_pct_wacc_limiti():
    assert mh757_pct_wacc(0, "x") == 0.0
    assert mh757_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh757_pct_wacc(50.1, "x")


def test_eta_limiti():
    assert mh757_eta(1.0, "x") == 1.0
    assert mh757_eta(0.90, "x") == 0.90
    with pytest.raises(ValueError):
        mh757_eta(0, "x")
    with pytest.raises(ValueError):
        mh757_eta(-0.1, "x")
    with pytest.raises(ValueError):
        mh757_eta(1.01, "x")


# ---------------------------------------------------------------- fisica base
def test_q_lordo_rec_netto():
    assert mh757_q_lordo(300000, 40) == pytest.approx(12000.0)
    assert mh757_q_lordo(300000, 0) == 0.0
    assert mh757_q_rec(12000.0, 30.0) == pytest.approx(3600.0)
    assert mh757_q_rec(12000.0, 0) == 0.0
    assert mh757_q_rec(12000.0, 100) == 12000.0
    assert mh757_q_netto(12000.0, 3600.0) == pytest.approx(8400.0)
    assert mh757_q_netto(12000.0, 12000.0) == 0.0
    with pytest.raises(ValueError):
        mh757_q_rec(12000.0, 100.1)
    with pytest.raises(ValueError):
        mh757_q_lordo(300000, -1)


def test_gas_base_e_c_base_e_co2_base():
    assert mh757_gas_base(12000.0, 0.90) == pytest.approx(13333.333333333332)
    assert mh757_gas_base(12000.0, 1.0) == 12000.0
    assert mh757_c_base(13333.333333333332, 45) == pytest.approx(600000.0)
    assert mh757_co2_base(13333.333333333332, 0.20) == pytest.approx(
        2666.6666666666665)
    with pytest.raises(ValueError):
        mh757_gas_base(12000.0, 0)
    with pytest.raises(ValueError):
        mh757_c_base(13333.333333333332, -1)


def test_q_pdc_e_e_el():
    assert mh757_q_pdc(8400.0, 70.0) == pytest.approx(5880.0)
    assert mh757_q_pdc(8400.0, 0) == 0.0
    assert mh757_q_pdc(8400.0, 100) == 8400.0
    assert mh757_e_el(5880.0, 3.2) == pytest.approx(1837.5)
    assert mh757_e_el(5880.0, 0) is None
    assert mh757_e_el(5880.0, -1.0) is None
    assert mh757_e_el(0.0, 3.2) == 0.0
    with pytest.raises(ValueError):
        mh757_q_pdc(8400.0, 100.1)


def test_gas_res():
    assert mh757_gas_res(8400.0, 70.0, 0.90) == pytest.approx(2800.0)
    assert mh757_gas_res(8400.0, 0, 0.90) == pytest.approx(9333.333333333334)
    assert mh757_gas_res(8400.0, 100, 0.90) == 0.0
    with pytest.raises(ValueError):
        mh757_gas_res(8400.0, 70.0, 0)


def test_c_alt_var_e_c_alt():
    assert mh757_c_alt_var(2800.0, 45, 1837.5,
                           110) == pytest.approx(328125.0)
    assert mh757_c_alt_var(2800.0, 45, 0.0, 110) == pytest.approx(126000.0)
    assert mh757_c_alt(328125.0, 80000) == pytest.approx(408125.0)
    assert mh757_c_alt(328125.0, 0) == pytest.approx(328125.0)
    with pytest.raises(ValueError):
        mh757_c_alt_var(2800.0, -1, 1837.5, 110)


def test_risparmio_segno():
    assert mh757_risparmio(600000.0, 408125.0) == pytest.approx(191875.0)
    assert mh757_risparmio(600000.0, 600000.0) == 0.0
    assert mh757_risparmio(600000.0, 500000.0) == 100000.0


def test_co2_alt_e_evitata_segno_libero():
    assert mh757_co2_alt(2800.0, 0.20, 1837.5,
                         0.25) == pytest.approx(1019.375)
    assert mh757_co2_evitata(2666.6666666666665,
                             1019.375) == pytest.approx(
        1647.2916666666665)
    assert mh757_co2_evitata(2666.6666666666665,
                             2666.6666666666665) == pytest.approx(0.0)
    assert mh757_co2_evitata(2666.6666666666665,
                             3266.6666666666665) == pytest.approx(
        -600.0, abs=1e-6)


# ---------------------------------------------------------------- finanza base
def test_crf():
    assert mh757_crf(5.0, 15) == pytest.approx(0.09634228760924432)
    assert mh757_crf(0, 15) == pytest.approx(1.0 / 15.0)
    assert mh757_crf(5.0, 1) == pytest.approx(1.05)
    assert mh757_crf(5.0, 10) == pytest.approx(0.12950457496545661)


def test_quota_capex_e_lco():
    assert mh757_quota_capex(1200000, 0.09634228760924432) == pytest.approx(
        115610.74513109318)
    assert mh757_lco_base(600000.0, 300000) == pytest.approx(2.0)
    assert mh757_lco_base(600000.0, 0) is None
    assert mh757_lco_alt(1200000, 0.09634228760924432, 80000,
                         328125.0, 300000) == pytest.approx(
        1.745785817103644)
    assert mh757_lco_alt(1200000, 0.09634228760924432, 80000,
                         328125.0, 0) is None
    assert mh757_lco_alt(0, 0.09634228760924432, 80000,
                         328125.0, 300000) == pytest.approx(1.3604166666666666)


def test_prezzo_pareggio_formula_brief_negativo_e_none():
    assert mh757_prezzo_pareggio(600000.0, 2800.0, 45, 80000,
                                 1837.5) == pytest.approx(
        214.42176870748298)
    assert mh757_prezzo_pareggio(600000.0, 2800.0, 45, 474000,
                                 1837.5) == pytest.approx(0.0, abs=1e-9)
    assert mh757_prezzo_pareggio(600000.0, 2800.0, 45, 80000,
                                 0.0) is None
    assert mh757_prezzo_pareggio(600000.0, 2800.0, 45, 80000,
                                 None) is None
    assert mh757_prezzo_pareggio(600000.0, 0.0, 45, 0,
                                 1837.5) == pytest.approx(
        326.53061224489795)


def test_flussi_lunghezza_e_primo():
    fl = mh757_flussi(1200000, 191875.0, 15)
    assert len(fl) == 16
    assert fl[0] == -1200000
    assert all(f == 191875.0 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = demo_calcoli()
    assert bc["van"] == pytest.approx(791596.8860759008)
    assert mh757_van([-1200000] + [191875.0] * 15,
                     0) == pytest.approx(1678125.0)
    assert mh757_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo_e_conviente():
    bc = demo_calcoli()
    assert bc["tir"] == pytest.approx(13.64095711599196)
    assert mh757_tir([-1200000] + [191875.0] * 15) == pytest.approx(
        0.1364095711599196)
    tir = mh757_tir([-1200000] + [191875.0] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-1200000] + [191875.0] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback():
    assert mh757_payback([-1200000] + [191875.0] * 15) == 7
    assert mh757_payback([-1200000] + [-34687.5] * 15) is None
    assert mh757_payback([0] + [191875.0] * 15) == 0
    assert mh757_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh757_verdetto(100.0, 1200000, 10.0) == "CONVIENTE"
    assert mh757_verdetto(-119000.0, 1200000, 10.0) == "MARGINALE"
    assert mh757_verdetto(-120000.0, 1200000, 10.0) == "MARGINALE"
    assert mh757_verdetto(-120000.01, 1200000, 10.0) == "NON_CONVIENTE"
    assert mh757_verdetto(-791596.89, 1200000, 10.0) == "NON_CONVIENTE"
    assert mh757_verdetto(float("nan"), 1200000, 10.0) == "NON_CALCOLABILE"
    assert mh757_verdetto(0.0, 0, 10.0) == "MARGINALE"


def test_valida_demo_ok():
    v = mh757_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("produzione_hl_anno", "300000"),
                       ("produzione_hl_anno", float("nan")),
                       ("produzione_hl_anno", float("inf")),
                       ("produzione_hl_anno", True),
                       ("prezzo_el_eur_mwh", None)):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh757_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("produzione_hl_anno", 0),
                          ("calore_kwh_per_hl", 0),
                          ("calore_kwh_per_hl", -5),
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
        assert mh757_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"quota_recupero_pct": 0, "quota_pdc_pct": 0,
              "prezzo_gas_eur_mwh": 0,
              "prezzo_el_eur_mwh": 0, "om_fisso_eur_anno": 0,
              "capex_eur": 0, "f_gas_t_per_mwh": 0,
              "f_el_t_per_mwh": 0, "wacc_pct": 0,
              "tolleranza_pct": 0, "eta_caldaia": 1.0})
    assert mh757_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["quota_pdc_pct"] = 100
    d["quota_recupero_pct"] = 100
    assert mh757_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh757_demo()
    assert d["produzione_hl_anno"] == 300000
    assert d["calore_kwh_per_hl"] == 40
    assert d["eta_caldaia"] == 0.90
    assert d["quota_recupero_pct"] == 30.0
    assert d["quota_pdc_pct"] == 70.0
    assert d["cop"] == 3.2
    assert d["prezzo_gas_eur_mwh"] == 45
    assert d["prezzo_el_eur_mwh"] == 110
    assert d["om_fisso_eur_anno"] == 80000
    assert d["capex_eur"] == 1200000
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
        "q_lordo_mwh_anno": 12000.0,
        "q_rec_mwh_anno": 3600.0,
        "q_netto_mwh_anno": 8400.0,
        "gas_base_mwh_anno": 13333.333333333332,
        "c_base_eur_anno": 600000.0,
        "q_pdc_mwh_anno": 5880.0,
        "e_el_mwh_anno": 1837.5,
        "gas_res_mwh_anno": 2800.0,
        "c_alt_var_eur_anno": 328125.0,
        "c_alt_eur_anno": 408125.0,
        "risparmio_eur_anno": 191875.0,
        "co2_base_t_anno": 2666.6666666666665,
        "co2_alt_t_anno": 1019.375,
        "co2_evitata_t_anno": 1647.2916666666665,
        "crf": 0.09634228760924432,
        "quota_capex_eur_anno": 115610.74513109318,
        "lco_base_eur_hl": 2.0,
        "lco_alt_eur_hl": 1.745785817103644,
        "van": 791596.8860759008,
        "tir": 13.64095711599196,
        "prezzo_pareggio_eur_mwh": 214.42176870748298,
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
    assert bc["q_lordo_mwh_anno"] == pytest.approx(12000.0)
    assert bc["q_rec_mwh_anno"] == pytest.approx(3600.0)
    assert bc["q_netto_mwh_anno"] == pytest.approx(8400.0)
    assert bc["gas_base_mwh_anno"] == pytest.approx(13333.333333333332)
    assert bc["co2_evitata_t_anno"] == pytest.approx(1647.2916666666665)


def test_demo_calcoli_economia():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] == 600000.0
    assert bc["c_alt_var_eur_anno"] == pytest.approx(328125.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(408125.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(191875.0)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(214.42176870748298)


def test_demo_calcoli_finanza():
    bc = demo_calcoli()
    assert bc["crf"] == pytest.approx(0.09634228760924432)
    assert bc["quota_capex_eur_anno"] == pytest.approx(115610.74513109318)
    assert bc["lco_base_eur_hl"] == pytest.approx(2.0)
    assert bc["lco_alt_eur_hl"] == pytest.approx(1.745785817103644)
    assert bc["van"] == pytest.approx(791596.8860759008)
    assert bc["tir"] == pytest.approx(13.64095711599196)
    assert bc["payback"] == 7
    assert bc["verdetto"] == "CONVIENTE"


def test_demo_flussi_e_cumulato():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -1200000
    assert len(bc["flussi"]) == 16
    assert all(f == 191875.0 for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -1200000
    assert righe.iloc[5]["Cumulato (EUR)"] == pytest.approx(-240625.0)
    assert righe.iloc[6]["Cumulato (EUR)"] == pytest.approx(-48750.0)
    assert righe.iloc[7]["Cumulato (EUR)"] == pytest.approx(143125.0)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(1678125.0)
    assert righe.iloc[15]["Flusso (EUR/anno)"] == 191875.0


def test_demo_tabella_righe():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Calore lordo (MWh/anno)"] == pytest.approx(12000.0)
    assert mappa["Calore recuperato (MWh/anno)"] == pytest.approx(3600.0)
    assert mappa["Calore netto (MWh/anno)"] == pytest.approx(8400.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(408125.0)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(191875.0)
    assert mappa["Payback (anni)"] == 7
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Prezzo elettrico di pareggio (EUR/MWh)"] == pytest.approx(
        214.42176870748298)


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
        bc["produzione_hl_anno"] + bc["c_alt_var_eur_anno"] / \
        bc["produzione_hl_anno"] == pytest.approx(bc["lco_alt_eur_hl"])
    assert bc["c_base_eur_anno"] - bc["gas_res_mwh_anno"] * \
        bc["prezzo_gas_eur_mwh"] - bc["om_fisso_eur_anno"] == \
        pytest.approx(bc["prezzo_pareggio_eur_mwh"] *
                      bc["e_el_mwh_anno"])
    assert bc["q_lordo_mwh_anno"] - bc["q_rec_mwh_anno"] == \
        pytest.approx(bc["q_netto_mwh_anno"])
    assert bc["produzione_hl_anno"] * bc["calore_kwh_per_hl"] / \
        1000.0 == pytest.approx(bc["q_lordo_mwh_anno"])


def test_demo_crf_solo_nel_lco_non_nei_flussi():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -bc["capex_eur"]
    assert all(f == bc["risparmio_eur_anno"] for f in bc["flussi"][1:])
    assert bc["crf"] not in bc["flussi"]
    assert bc["quota_capex_eur_anno"] not in bc["flussi"]
    van_da_flussi = mh757_van(bc["flussi"], bc["wacc_pct"])
    assert van_da_flussi == pytest.approx(bc["van"])
    assert bc["lco_alt_eur_hl"] == pytest.approx(
        (bc["capex_eur"] * bc["crf"] + bc["om_fisso_eur_anno"]) /
        bc["produzione_hl_anno"] + bc["c_alt_var_eur_anno"] /
        bc["produzione_hl_anno"])


def test_demo_contro_riconteggio_indipendente():
    prod, cal, eta, qr, quota, cop = 300000, 40, 0.90, 30.0, 70.0, 3.2
    pg, pe, om, cx = 45, 110, 80000, 1200000
    fg, fe, wacc, vita = 0.20, 0.25, 5.0, 15
    ql = prod * cal / 1000.0
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
    assert bc["van"] == pytest.approx(-1200000 + 191875.0 * annuita)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(
        (600000.0 - 126000.0 - 80000) / 1837.5)
    assert bc["flussi"][0] + 15 * bc["flussi"][1] == pytest.approx(
        1678125.0)
    assert bc["flussi"][0] + 6 * bc["flussi"][1] == pytest.approx(
        -48750.0)


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
    assert bc["risparmio_eur_anno"] == pytest.approx(33875.0)
    assert bc["van"] == pytest.approx(-848389.0839566331)
    assert bc["tir"] is None or bc["tir"] < 0.0
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_prezzo_el_alto_non_conviente():
    bc = _variante(prezzo_el_eur_mwh=200)
    assert bc["risparmio_eur_anno"] == pytest.approx(26500.0)
    assert bc["van"] == pytest.approx(-924939.0619882144)
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(214.42176870748298)
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_variante_prezzo_el_zero_conviente():
    bc = _variante(prezzo_el_eur_mwh=0.0)
    assert bc["c_alt_var_eur_anno"] == pytest.approx(126000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(206000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(394000.0)
    assert bc["van"] == pytest.approx(2889585.2670431524)
    assert bc["tir"] == pytest.approx(32.34263053483771, abs=1e-4)
    assert bc["payback"] == 4
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_variante_gas_alto_conviente():
    bc = _variante(prezzo_gas_eur_mwh=150)
    assert bc["risparmio_eur_anno"] == pytest.approx(1297875.0)
    assert bc["van"] == pytest.approx(12271498.67630363)
    assert bc["payback"] == 1
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_variante_gas_marginale():
    bc = _variante(prezzo_gas_eur_mwh=37)
    assert bc["risparmio_eur_anno"] == pytest.approx(107608.33333333331)
    assert bc["van"] == pytest.approx(-83062.29794145052)
    assert bc["van"] < 0.0
    assert abs(bc["van"]) <= 0.10 * 1200000
    assert bc["tir"] == pytest.approx(3.9574346813472494, abs=1e-4)
    assert bc["payback"] == 12
    assert bc["verdetto"] == "MARGINALE"
    assert bc["valid"] is True


def test_variante_quota_zero_calcolabile_non_degenere():
    bc = _variante(quota_pdc_pct=0)
    assert bc["valid"] is True
    assert bc["q_pdc_mwh_anno"] == 0.0
    assert bc["e_el_mwh_anno"] == 0.0
    assert bc["gas_res_mwh_anno"] == pytest.approx(9333.333333333334)
    assert bc["risparmio_eur_anno"] == 100000.0
    assert bc["van"] == pytest.approx(-162034.19618194096)
    assert bc["co2_evitata_t_anno"] == pytest.approx(800.0)
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_quota_recupero_cento_calcolabile_non_degenere():
    bc = _variante(quota_recupero_pct=100)
    assert bc["valid"] is True
    assert bc["q_netto_mwh_anno"] == 0.0
    assert bc["q_pdc_mwh_anno"] == 0.0
    assert bc["e_el_mwh_anno"] == 0.0
    assert bc["gas_res_mwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == 520000.0
    assert bc["van"] == pytest.approx(4197422.179853907)
    assert bc["tir"] == pytest.approx(43.13348364481708, abs=1e-4)
    assert bc["payback"] == 3
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_quota_recupero_zero():
    bc = _variante(quota_recupero_pct=0)
    assert bc["q_netto_mwh_anno"] == pytest.approx(12000.0)
    assert bc["q_pdc_mwh_anno"] == pytest.approx(8400.0)
    assert bc["e_el_mwh_anno"] == pytest.approx(2625.0)
    assert bc["gas_res_mwh_anno"] == pytest.approx(4000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(51250.0)
    assert bc["van"] == pytest.approx(-668042.5255432448)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(129.52380952380952)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_cop_basso_e_alto():
    bc = _variante(cop=2.0)
    assert bc["e_el_mwh_anno"] == pytest.approx(2940.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(70600.0)
    assert bc["van"] == pytest.approx(-467196.14250445034)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(134.01360544217687)
    assert bc["verdetto"] == "NON_CONVIENTE"
    bc2 = _variante(cop=5.0)
    assert bc2["e_el_mwh_anno"] == pytest.approx(1176.0)
    assert bc2["risparmio_eur_anno"] == pytest.approx(264640.0)
    assert bc2["van"] == pytest.approx(1546872.7032241113)
    assert bc2["tir"] == pytest.approx(20.749600140326084, abs=1e-4)
    assert bc2["payback"] == 5
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_co2_evitata_negativa_con_fattore_el_alto():
    bc = _variante(f_el_t_per_mwh=1.50)
    assert bc["co2_alt_t_anno"] == pytest.approx(3316.25)
    assert bc["co2_evitata_t_anno"] == pytest.approx(-649.5833333333335)
    assert bc["co2_evitata_t_anno"] < 0.0
    assert bc["van"] == pytest.approx(791596.8860759008)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_pareggio_negativo():
    bc = _variante(om_fisso_eur_anno=5000000)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(-2463.1292517006805)
    assert bc["prezzo_pareggio_eur_mwh"] < 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(-4728125.0)
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_variante_pareggio_zero():
    bc = _variante(om_fisso_eur_anno=474000)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(0.0, abs=1e-9)
    assert bc["risparmio_eur_anno"] == pytest.approx(-202125.0)


def test_variante_wacc_zero():
    bc = _variante(wacc_pct=0)
    assert bc["crf"] == pytest.approx(1.0 / 15.0)
    assert bc["quota_capex_eur_anno"] == pytest.approx(80000.0)
    assert bc["lco_alt_eur_hl"] == pytest.approx(1.6270833333333332)
    assert bc["van"] == pytest.approx(1678125.0)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex_eur=0)
    assert bc["capex_eur"] == 0
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(1991596.8860759009)
    assert bc["lco_alt_eur_hl"] == pytest.approx(1.3604166666666666)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_vita_dieci():
    bc = _variante(vita_anni=10)
    assert len(bc["flussi"]) == 11
    assert bc["crf"] == pytest.approx(0.12950457496545661)
    assert bc["van"] == pytest.approx(281607.8895373356)
    assert bc["tir"] == pytest.approx(9.590843571654712, abs=1e-4)
    assert bc["payback"] == 7
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_input_nulli_calcolabile_non_degenere():
    bc = _variante(prezzo_el_eur_mwh=0.0, prezzo_gas_eur_mwh=0,
                   om_fisso_eur_anno=0)
    assert bc["valid"] is True
    assert bc["c_base_eur_anno"] == 0.0
    assert bc["c_alt_eur_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == 0.0
    assert bc["van"] == -1200000.0
    assert bc["verdetto"] == "NON_CONVIENTE"


# ---------------------------------------------------------------- degenere
def test_degenere_produzione_zero():
    bc = _variante(produzione_hl_anno=0)
    assert bc["valid"] is False
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"] == []
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["lco_base_eur_hl"] is None
    assert bc["lco_alt_eur_hl"] is None
    assert bc["errore"]


def test_degenere_calore_cop_vita():
    for kw in ({"calore_kwh_per_hl": 0}, {"calore_kwh_per_hl": -5},
               {"cop": 0}, {"cop": -1},
               {"produzione_hl_anno": 0},
               {"produzione_hl_anno": -1},
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
    for kw in ({"produzione_hl_anno": "300000"},
               {"produzione_hl_anno": float("nan")},
               {"prezzo_el_eur_mwh": float("inf")},
               {"capex_eur": True}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_neutro_campi():
    bc = _variante(produzione_hl_anno=0)
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
    assert mh757_prezzo_pareggio(600000.0, 2800.0, 45, 80000,
                                 0.0) is None
    assert mh757_prezzo_pareggio(600000.0, 2800.0, 45, 80000,
                                 None) is None
    assert mh757_lco_base(600000.0, 0) is None
    assert mh757_e_el(5880.0, 0) is None
    bc = _variante(quota_pdc_pct=0)
    assert bc["prezzo_pareggio_eur_mwh"] is None


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = demo_calcoli()
    testo = mh757_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert "q_lordo_mwh_anno;12000.0" in testo
    assert "q_netto_mwh_anno;8400.0" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "prezzo_pareggio_eur_mwh" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = demo_calcoli()
    testo = mh757_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"quota_capex_eur_anno;{bc['quota_capex_eur_anno']}" in testo
    assert f"q_lordo_mwh_anno;{bc['q_lordo_mwh_anno']}" in testo


def test_csv_degenere_solo_zeri():
    bc = _variante(produzione_hl_anno=0)
    testo = mh757_csv(bc, _demo_kwargs())
    assert "van_eur;0.0" in testo
    assert "q_lordo_mwh_anno;0.0" in testo
    assert "verdetto;NON_CALCOLABILE" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = demo_calcoli()
    testo = mh757_csv(bc, _demo_kwargs())
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
    assert basso - base == pytest.approx(18375.0)
    assert base - alto == pytest.approx(18375.0)


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
    assert set(mh757_demo().keys()) == {
        "produzione_hl_anno", "calore_kwh_per_hl",
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
    ast.parse(_leggi("w758_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w758_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab757:")


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    # token vietati costruiti per concatenazione, cosi' questo
    # stesso file non li contiene come sottostringhe contigue.
    src = _leggi("w758_helpers.py")
    vietati = ["mh" + "75" + "6", "st" + "75" + "6",
               "tab" + "75" + "6", "w" + "75" + "7",
               "mh" + "75" + "5", "tab" + "75" + "5"]
    assert "streamlit" not in src
    assert all(t not in src for t in vietati)
    assert "macchina " + "continua" not in src
    assert "foglio " + "di carta" not in src


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w758_ui.py")
    vietati = ["mh" + "75" + "6", "st" + "75" + "6",
               "tab" + "75" + "6", "w" + "75" + "7",
               "mh" + "75" + "5", "tab" + "75" + "5"]
    assert all(t not in src for t in vietati)
    assert "essiccare " + "la carta" not in src
    assert "cilindri " + "essiccatori" not in src
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st757_") for c in chiavi)
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
    src = _leggi("w758_test.py")
    vietati = ["mh" + "75" + "6", "st" + "75" + "6",
               "tab" + "75" + "6", "w" + "75" + "7",
               "mh" + "75" + "5", "tab" + "75" + "5"]
    assert all(t not in src for t in vietati)
    assert "essiccare " + "la carta" not in src
    assert "cilindri " + "essiccatori" not in src


def test_ui_chiavi_demo_coerenti():
    """Ogni _def757[...] letto dalla UI esiste nel dict demo:
    sweep anti-KeyError a render (lezione dello sweep chiavi demo vs UI)."""
    src = _leggi("w758_ui.py")
    usate = set(re.findall(r'_def757\["([^"]+)"\]', src))
    assert usate
    assert usate <= set(mh757_demo().keys())


def test_ui_riferisce_solo_helper_nuovi():
    src = _leggi("w758_ui.py")
    usati = set(re.findall(r'\b(mh\d+_\w+)\b', src))
    assert usati
    assert all(u.startswith("mh757_") for u in usati)


@pytest.mark.parametrize("wacc,vita,atteso", [
    (5.0, 15, 0.09634228760924432),
    (0, 15, 1.0 / 15.0),
    (10.0, 10, 0.16274539488251152),
    (5.0, 1, 1.05),
    (50.0, 5, 0.5758293838862559),
])
def test_crf_parametrizzato(wacc, vita, atteso):
    assert mh757_crf(wacc, vita) == pytest.approx(atteso)


@pytest.mark.parametrize("campo,valore", [
    ("produzione_hl_anno", 0), ("produzione_hl_anno", -3),
    ("calore_kwh_per_hl", 0), ("calore_kwh_per_hl", -5),
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
    assert mh757_valida(**d)["valido"] is False


def test_df_tabella_valori_demo_selezionati():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Produzione (hl/anno)"] == 300000.0
    assert mappa["Calore lordo (MWh/anno)"] == pytest.approx(12000.0)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(191875.0)
    assert mappa["Verdetto"] == "CONVIENTE"


def test_lco_alt_minore_di_lco_base_demo():
    bc = demo_calcoli()
    assert bc["lco_alt_eur_hl"] < bc["lco_base_eur_hl"]
    assert bc["lco_base_eur_hl"] - bc["lco_alt_eur_hl"] == pytest.approx(
        0.254214182896356)
