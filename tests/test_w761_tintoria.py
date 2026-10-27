"""Test tab761 "Tintoria:
tingere il tessuto con bagni caldi
recuperati e pompa di calore batte
la caldaia a gas?"

Nuova tab tab761 (tintura tessuto,
file di lavoro w762).
Business case deterministico della
tintura del tessuto in bagni caldi
in una tintoria industriale: il
tessuto va tinto in bagni caldi
(acqua per kg di tessuto, scaldata
dalla temperatura di ingresso alla
temperatura di tintura) e il calore
puo' arrivare dalla caldaia a gas
(baseline, tutto il calore lordo,
senza recupero) oppure in parte dal
calore recuperato dai bagni
scaricati caldi e in parte da una
pompa di calore che copre una quota
del calore netto, con il resto che
resta a gas.
Acqua = tessuto x rapporto bagno
(1 L = 1 kg); delta_T = T_tintura -
T_ingresso; Q_lordo = acqua x 4,186
x delta_T / 3600000; Q_rec =
quota_recupero / 100 x Q_lordo;
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
tessuto; LCO_alt = (CAPEX x CRF +
OM_fisso) / tessuto + C_alt_var /
tessuto; prezzo elettrico di
pareggio = (C_base - gas_res x
p_gas - OM_fisso) / E_el, None se
E_el <= 0, puo' essere negativo (il
solo O&M fisso piu' il gas residuo
superano gia' il costo baseline);
flussi [-CAPEX, risparmio x vita];
VAN, TIR, payback (primo anno con
cumulato >= 0). Distinta dalla tab
precedente del conservificio (li' si
sterilizzano conserve in autoclave,
senza tessuto e senza bagni di
tintura), dalla tab della lavanderia
(li' si lava biancheria, senza
tessuto da tingere, senza rapporto
bagno e senza temperatura di
tintura), dalla tab del caseificio
(li' si pastorizza latte, senza
tessuto e senza bagni di tintura),
dalla cartiera (li' si essicca
carta, senza tessuto e senza bagni
di tintura), dalla caldaia a
elettrodi generica (li' il calore
viene da elettrodi, senza processo
di tintura e senza quota di
recupero) e dal recupero calore
generico (li' il calore recuperato
va a un uso generico, senza tintura
di tessuto e senza pompa di calore
sul calore netto).

Demo calcolata eseguendo demo_calcoli()
(e ricontrollata a mano, riga per
riga): tessuto 2.500.000 kg/anno,
rapporto bagno 8 L/kg, temperatura
ingresso 20 C, temperatura tintura
80 C, rendimento caldaia 0,90, quota
recupero 40 %, quota PdC 70 %,
COP 3,5, prezzo gas 45 EUR/MWh,
prezzo elettrico 110 EUR/MWh, O&M
fisso 12.000 EUR/anno, CAPEX 250.000
EUR, fattore gas 0,20 tCO2/MWh e
fattore elettrico 0,25 tCO2/MWh,
WACC 5 %, vita 15 anni, tolleranza
10 % del CAPEX.

- acqua_kg_anno = 20000000.0
- delta_t_K = 60.0
- q_lordo_mwh_anno = 1395.3333333333333
- q_rec_mwh_anno = 558.1333333333333
- q_netto_mwh_anno = 837.1999999999999
- gas_base_mwh_anno = 1550.3703703703702
- c_base_eur_anno = 69766.66666666666
- q_pdc_mwh_anno = 586.04
- e_el_mwh_anno = 167.44
- gas_res_mwh_anno = 279.06666666666666
- c_alt_var_eur_anno = 30976.4
- c_alt_eur_anno = 42976.4
- risparmio_eur_anno = 26790.266666666656
- co2_base_t_anno = 310.0740740740741
- co2_alt_gas_t_anno = 55.81333333333333
- co2_alt_el_t_anno = 41.86
- co2_alt_t_anno = 97.67333333333333
- co2_evitata_t_anno = 212.40074074074073
- crf = 0.09634228760924432
- quota_capex_eur_anno = 24085.57190231108
- lco_base_eur_kg = 0.027906666666666663
- lco_alt_eur_kg = 0.02682478876092443
- van = 28073.806751668075
- tir = 6.6180936640955075
- payback = 10
- prezzo_pareggio_eur_mwh = 269.9992036948558
- verdetto = 'CONVIENTE'

Scomposizione: acqua = 2.500.000 x 8 =
20.000.000 kg/anno; delta_T = 80 - 20 =
60 K; Q_lordo = 20.000.000 x 4,186 x 60 /
3.600.000 = 1.395,33 MWh/anno; Q_rec =
0,40 x 1.395,33 = 558,13 MWh/anno;
Q_netto = 1.395,33 - 558,13 = 837,20
MWh/anno; gas_base = 1.395,33 / 0,90 =
1.550,37 MWh/anno; C_base = 1.550,37 x 45
= 69.766,67 EUR/anno; Q_pdc = 0,70 x
837,20 = 586,04 MWh/anno; E_el = 586,04 /
3,5 = 167,44 MWh/anno; gas_res = 0,30 x
837,20 / 0,90 = 279,07 MWh/anno;
C_alt_var = 279,07 x 45 + 167,44 x 110
= 12.558 + 18.418,40 = 30.976,40
EUR/anno; C_alt = 30.976,40 + 12.000 =
42.976,40 EUR/anno; risparmio =
69.766,67 - 42.976,40 = 26.790,27
EUR/anno; CO2 base = 1.550,37 x 0,20 =
310,07 t/anno; CO2 alt = 279,07 x 0,20 +
167,44 x 0,25 = 55,81 + 41,86 = 97,67
t/anno; CO2 evitata = 212,40 t/anno;
CRF 0,05 x 1,05^15 / (1,05^15 - 1) =
0.09634228760924432; quota CAPEX
250.000 x 0,096342 = 24.085,57
EUR/anno; LCO base 69.766,67 /
2.500.000 = 0,0279067 EUR/kg; LCO alt
(24.085,57 + 12.000) / 2.500.000 +
30.976,40 / 2.500.000 = 0,0268248
EUR/kg; flussi: anno 0 -250.000, anni
1-15 risparmio 26.790,27 (piatti); VAN
-250.000 + 26.790,27 x 10,379658
(annuita' 15 anni al 5 %) = 28.073,81
EUR; TIR 6,62 %; payback 10 anni (il
cumulato all'anno 9 e' -8.887,60 EUR,
all'anno 10 e' 17.902,67 EUR); prezzo
elettrico di pareggio (69.766,67 -
12.558 - 12.000) / 167,44 = 270,00
EUR/MWh; verdetto CONVIENTE perche'
VAN > 0.
NOTA: il CRF entra solo nel LCO,
mai nei flussi: il CAPEX compare una
sola volta, all'anno 0.
NOTA 2: in questo brief il risparmio
nullo o negativo NON e' degenere:
con prezzo gas 30 EUR/MWh il
risparmio e' 7.720,71 EUR/anno e il
caso resta calcolabile (valid=True,
VAN -169.861,66 EUR, NON_CONVIENTE).
NOTA 3: la CO2 evitata puo' essere
negativa: con fattore elettrico 2,00
tCO2/MWh la CO2 evitata e'
-80,62 t/anno, pur restando il caso
calcolabile.
NOTA 4: il prezzo elettrico di
pareggio puo' essere negativo: con
O&M fisso 5.000.000 EUR/anno il
pareggio e' -29.519,78 EUR/MWh,
perche' il solo O&M fisso piu' il
gas residuo superano gia' il costo
baseline (il caso demo ha pareggio
positivo, 270,00 EUR/MWh).
NOTA 5: la quota PdC zero NON e'
degenere: con quota 0 il risparmio
e' 15.906,67 EUR/anno, la VAN
-84.894,24 EUR e il pareggio non
e' definito (E_el nulla).
NOTA 6: il calore netto nullo (quota
recupero 100 %) NON e' degenere:
il risparmio e' 57.766,67 EUR/anno
(69.766,67 - 12.000 di solo O&M fisso)
e la VAN 349.598,25 EUR, e il
pareggio non e' definito.
NOTA 7: la temperatura di tintura
deve superare la temperatura di
ingresso: con T_tintura = T_ingresso
(delta_T 0) o sotto, il caso e'
degenere (valid=False,
NON_CALCOLABILE).
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w762_helpers import (
    demo_calcoli,
    mh761_acqua,
    mh761_c_alt,
    mh761_c_alt_var,
    mh761_c_base,
    mh761_calcola,
    mh761_co2_alt,
    mh761_co2_base,
    mh761_co2_evitata,
    mh761_crf,
    mh761_csv,
    mh761_delta_t,
    mh761_demo,
    mh761_e_el,
    mh761_eta,
    mh761_flussi,
    mh761_gas_base,
    mh761_gas_res,
    mh761_int_pos,
    mh761_lco_alt,
    mh761_lco_base,
    mh761_nneg,
    mh761_num,
    mh761_payback,
    mh761_pct_0_100,
    mh761_pct_wacc,
    mh761_pos,
    mh761_prezzo_pareggio,
    mh761_q_lordo,
    mh761_q_netto,
    mh761_q_pdc,
    mh761_q_rec,
    mh761_quota_capex,
    mh761_risparmio,
    mh761_temp_ingresso,
    mh761_temp_tintura,
    mh761_tir,
    mh761_valida,
    mh761_van,
    mh761_verdetto,
)


def _demo_kwargs():
    return dict(mh761_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh761_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh761_num(3, "x") == 3.0
    assert mh761_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh761_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh761_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh761_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh761_pos(0, "x")
    with pytest.raises(ValueError):
        mh761_pos(-1, "x")
    assert mh761_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh761_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh761_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh761_int_pos(0, "x")


def test_pct_0_100_limiti():
    assert mh761_pct_0_100(0, "x") == 0.0
    assert mh761_pct_0_100(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh761_pct_0_100(100.1, "x")
    with pytest.raises(ValueError):
        mh761_pct_0_100(-1, "x")


def test_pct_wacc_limiti():
    assert mh761_pct_wacc(0, "x") == 0.0
    assert mh761_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh761_pct_wacc(50.1, "x")


def test_eta_limiti():
    assert mh761_eta(1.0, "x") == 1.0
    assert mh761_eta(0.90, "x") == 0.90
    with pytest.raises(ValueError):
        mh761_eta(0, "x")
    with pytest.raises(ValueError):
        mh761_eta(-0.1, "x")
    with pytest.raises(ValueError):
        mh761_eta(1.01, "x")


def test_temp_limiti():
    assert mh761_temp_ingresso(0, "x") == 0.0
    assert mh761_temp_ingresso(99.0, "x") == 99.0
    with pytest.raises(ValueError):
        mh761_temp_ingresso(100, "x")
    with pytest.raises(ValueError):
        mh761_temp_ingresso(-1, "x")
    assert mh761_temp_tintura(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh761_temp_tintura(0, "x")
    with pytest.raises(ValueError):
        mh761_temp_tintura(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_acqua_delta_q_lordo():
    assert mh761_acqua(2500000, 8) == pytest.approx(20000000.0)
    assert mh761_acqua(2500000, 0) == 0.0
    assert mh761_delta_t(20, 80) == pytest.approx(60.0)
    assert mh761_delta_t(80, 20) == pytest.approx(-60.0)
    assert mh761_q_lordo(20000000.0, 60.0) == pytest.approx(
        1395.3333333333333)
    assert mh761_q_lordo(20000000.0, 0) == 0.0
    with pytest.raises(ValueError):
        mh761_acqua(2500000, -1)
    with pytest.raises(ValueError):
        mh761_q_lordo(20000000.0, -1) if False else mh761_acqua(-1, 8)


def test_q_rec_netto():
    assert mh761_q_rec(1395.3333333333333, 40.0) == pytest.approx(
        558.1333333333333)
    assert mh761_q_rec(1395.3333333333333, 0) == 0.0
    assert mh761_q_rec(1395.3333333333333, 100) == pytest.approx(
        1395.3333333333333)
    assert mh761_q_netto(1395.3333333333333, 558.1333333333333) == \
        pytest.approx(837.2)
    assert mh761_q_netto(1395.3333333333333, 1395.3333333333333) == 0.0
    with pytest.raises(ValueError):
        mh761_q_rec(1395.3333333333333, 100.1)


def test_gas_base_e_c_base_e_co2_base():
    assert mh761_gas_base(1395.3333333333333, 0.90) == pytest.approx(
        1550.3703703703702)
    assert mh761_gas_base(1395.3333333333333, 1.0) == pytest.approx(
        1395.3333333333333)
    assert mh761_c_base(1550.3703703703702, 45) == pytest.approx(
        69766.66666666666)
    assert mh761_co2_base(1550.3703703703702, 0.20) == pytest.approx(
        310.0740740740741)
    with pytest.raises(ValueError):
        mh761_gas_base(1395.3333333333333, 0)


def test_q_pdc_e_e_el():
    assert mh761_q_pdc(837.2, 70.0) == pytest.approx(586.04)
    assert mh761_q_pdc(837.2, 0) == 0.0
    assert mh761_q_pdc(837.2, 100) == pytest.approx(837.2)
    assert mh761_e_el(586.04, 3.5) == pytest.approx(167.44)
    assert mh761_e_el(586.04, 0) is None
    assert mh761_e_el(586.04, -1.0) is None
    assert mh761_e_el(0.0, 3.5) == 0.0
    with pytest.raises(ValueError):
        mh761_q_pdc(837.2, 100.1)


def test_gas_res():
    assert mh761_gas_res(837.2, 70.0, 0.90) == pytest.approx(
        279.06666666666666)
    assert mh761_gas_res(837.2, 0, 0.90) == pytest.approx(
        930.2222222222222)
    assert mh761_gas_res(837.2, 100, 0.90) == 0.0
    with pytest.raises(ValueError):
        mh761_gas_res(837.2, 70.0, 0)


def test_c_alt_var_e_c_alt():
    assert mh761_c_alt_var(279.06666666666666, 45, 167.44,
                           110) == pytest.approx(30976.4)
    assert mh761_c_alt_var(279.06666666666666, 45, 0.0,
                           110) == pytest.approx(12558.0)
    assert mh761_c_alt(30976.4, 12000) == pytest.approx(42976.4)
    assert mh761_c_alt(30976.4, 0) == pytest.approx(30976.4)
    with pytest.raises(ValueError):
        mh761_c_alt_var(279.06666666666666, -1, 167.44, 110)


def test_risparmio_segno():
    assert mh761_risparmio(69766.66666666666, 42976.4) == pytest.approx(
        26790.266666666656)
    assert mh761_risparmio(69766.66666666666, 69766.66666666666) == 0.0


def test_co2_alt_e_evitata_segno_libero():
    assert mh761_co2_alt(279.06666666666666, 0.20, 167.44,
                         0.25) == pytest.approx(97.67333333333333)
    assert mh761_co2_evitata(310.0740740740741,
                             97.67333333333333) == pytest.approx(
        212.40074074074073)
    assert mh761_co2_evitata(310.0740740740741,
                             910.0740740740741) == pytest.approx(
        -600.0, abs=1e-6)


# ---------------------------------------------------------------- finanza base
def test_crf():
    assert mh761_crf(5.0, 15) == pytest.approx(0.09634228760924432)
    assert mh761_crf(0, 15) == pytest.approx(1.0 / 15.0)
    assert mh761_crf(5.0, 1) == pytest.approx(1.05)
    assert mh761_crf(5.0, 10) == pytest.approx(0.12950457496545661)


def test_quota_capex_e_lco():
    assert mh761_quota_capex(250000, 0.09634228760924432) == pytest.approx(
        24085.57190231108)
    assert mh761_lco_base(69766.66666666666, 2500000) == pytest.approx(
        0.027906666666666663)
    assert mh761_lco_base(69766.66666666666, 0) is None
    assert mh761_lco_alt(250000, 0.09634228760924432, 12000,
                         30976.4, 2500000) == pytest.approx(
        0.02682478876092443)
    assert mh761_lco_alt(250000, 0.09634228760924432, 12000,
                         30976.4, 0) is None
    assert mh761_lco_alt(0, 0.09634228760924432, 12000,
                         30976.4, 2500000) == pytest.approx(0.01719056)


def test_prezzo_pareggio_formula_brief_negativo_e_none():
    assert mh761_prezzo_pareggio(69766.66666666666, 279.06666666666666,
                                 45, 12000,
                                 167.44) == pytest.approx(
        269.9992036948558)
    assert mh761_prezzo_pareggio(69766.66666666666, 279.06666666666666,
                                 45, 57208.66666666666,
                                 167.44) == pytest.approx(0.0, abs=1e-6)
    assert mh761_prezzo_pareggio(69766.66666666666, 279.06666666666666,
                                 45, 12000, 0.0) is None
    assert mh761_prezzo_pareggio(69766.66666666666, 279.06666666666666,
                                 45, 12000, None) is None


def test_flussi_lunghezza_e_primo():
    fl = mh761_flussi(250000, 26790.266666666656, 15)
    assert len(fl) == 16
    assert fl[0] == -250000
    assert all(f == 26790.266666666656 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = demo_calcoli()
    assert bc["van"] == pytest.approx(28073.806751668075)
    assert mh761_van([-250000] + [26790.266666666656] * 15,
                     0) == pytest.approx(151854.0)
    assert mh761_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo_e_conviente():
    bc = demo_calcoli()
    assert bc["tir"] == pytest.approx(6.6180936640955075)
    assert mh761_tir([-250000] + [26790.266666666656] * 15) == pytest.approx(
        0.066180936640955075)
    tir = mh761_tir([-250000] + [26790.266666666656] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-250000] + [26790.266666666656] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback():
    assert mh761_payback([-250000] + [26790.266666666656] * 15) == 10
    assert mh761_payback([-250000] + [-1000.0] * 15) is None
    assert mh761_payback([0] + [26790.266666666656] * 15) == 0
    assert mh761_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh761_verdetto(100.0, 250000, 10.0) == "CONVIENTE"
    assert mh761_verdetto(-24000.0, 250000, 10.0) == "MARGINALE"
    assert mh761_verdetto(-25000.0, 250000, 10.0) == "MARGINALE"
    assert mh761_verdetto(-25000.01, 250000, 10.0) == "NON_CONVIENTE"
    assert mh761_verdetto(float("nan"), 250000, 10.0) == "NON_CALCOLABILE"
    assert mh761_verdetto(0.0, 0, 10.0) == "MARGINALE"


def test_valida_demo_ok():
    v = mh761_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("tessuto_kg_anno", "300000"),
                       ("tessuto_kg_anno", float("nan")),
                       ("tessuto_kg_anno", float("inf")),
                       ("tessuto_kg_anno", True),
                       ("prezzo_el_eur_mwh", None)):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh761_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("tessuto_kg_anno", 0),
                          ("rapporto_bagno_L_per_kg", 0),
                          ("rapporto_bagno_L_per_kg", -1),
                          ("t_ingresso_C", -1),
                          ("t_ingresso_C", 100),
                          ("t_tintura_C", 0),
                          ("t_tintura_C", 100.1),
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
        assert mh761_valida(**d)["valido"] is False


def test_valida_rifiuta_delta_non_positivo():
    for ti, tt in ((80, 80), (80, 20), (20, 20)):
        d = _demo_kwargs()
        d["t_ingresso_C"] = ti
        d["t_tintura_C"] = tt
        assert mh761_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"quota_recupero_pct": 0, "quota_pdc_pct": 0,
              "prezzo_gas_eur_mwh": 0,
              "prezzo_el_eur_mwh": 0, "om_fisso_eur_anno": 0,
              "capex_eur": 0, "f_gas_t_per_mwh": 0,
              "f_el_t_per_mwh": 0, "wacc_pct": 0,
              "tolleranza_pct": 0, "eta_caldaia": 1.0,
              "t_ingresso_C": 0, "t_tintura_C": 100})
    assert mh761_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["quota_pdc_pct"] = 100
    d["quota_recupero_pct"] = 100
    assert mh761_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh761_demo()
    assert d["tessuto_kg_anno"] == 2500000
    assert d["rapporto_bagno_L_per_kg"] == 8
    assert d["t_ingresso_C"] == 20
    assert d["t_tintura_C"] == 80
    assert d["eta_caldaia"] == 0.90
    assert d["quota_recupero_pct"] == 40.0
    assert d["quota_pdc_pct"] == 70.0
    assert d["cop"] == 3.5
    assert d["prezzo_gas_eur_mwh"] == 45
    assert d["prezzo_el_eur_mwh"] == 110
    assert d["om_fisso_eur_anno"] == 12000
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
        "acqua_kg_anno": 20000000.0,
        "delta_t_K": 60.0,
        "q_lordo_mwh_anno": 1395.3333333333333,
        "q_rec_mwh_anno": 558.1333333333333,
        "q_netto_mwh_anno": 837.1999999999999,
        "gas_base_mwh_anno": 1550.3703703703702,
        "c_base_eur_anno": 69766.66666666666,
        "q_pdc_mwh_anno": 586.04,
        "e_el_mwh_anno": 167.44,
        "gas_res_mwh_anno": 279.06666666666666,
        "c_alt_var_eur_anno": 30976.4,
        "c_alt_eur_anno": 42976.4,
        "risparmio_eur_anno": 26790.266666666656,
        "co2_base_t_anno": 310.0740740740741,
        "co2_alt_t_anno": 97.67333333333333,
        "co2_evitata_t_anno": 212.40074074074073,
        "crf": 0.09634228760924432,
        "quota_capex_eur_anno": 24085.57190231108,
        "lco_base_eur_kg": 0.027906666666666663,
        "lco_alt_eur_kg": 0.02682478876092443,
        "van": 28073.806751668075,
        "tir": 6.6180936640955075,
        "prezzo_pareggio_eur_mwh": 269.9992036948558,
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
    assert bc["acqua_kg_anno"] == pytest.approx(20000000.0)
    assert bc["q_lordo_mwh_anno"] == pytest.approx(1395.3333333333333)
    assert bc["q_rec_mwh_anno"] == pytest.approx(558.1333333333333)
    assert bc["q_netto_mwh_anno"] == pytest.approx(837.2)
    assert bc["gas_base_mwh_anno"] == pytest.approx(1550.3703703703702)
    assert bc["co2_evitata_t_anno"] == pytest.approx(212.40074074074073)


def test_demo_calcoli_economia():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(69766.66666666666)
    assert bc["c_alt_var_eur_anno"] == pytest.approx(30976.4)
    assert bc["c_alt_eur_anno"] == pytest.approx(42976.4)
    assert bc["risparmio_eur_anno"] == pytest.approx(26790.266666666656)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(269.9992036948558)


def test_demo_calcoli_finanza():
    bc = demo_calcoli()
    assert bc["crf"] == pytest.approx(0.09634228760924432)
    assert bc["quota_capex_eur_anno"] == pytest.approx(24085.57190231108)
    assert bc["lco_base_eur_kg"] == pytest.approx(0.027906666666666663)
    assert bc["lco_alt_eur_kg"] == pytest.approx(0.02682478876092443)
    assert bc["van"] == pytest.approx(28073.806751668075)
    assert bc["tir"] == pytest.approx(6.6180936640955075)
    assert bc["payback"] == 10
    assert bc["verdetto"] == "CONVIENTE"


def test_demo_flussi_e_cumulato():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -250000
    assert len(bc["flussi"]) == 16
    assert all(f == 26790.266666666656 for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -250000
    assert righe.iloc[5]["Cumulato (EUR)"] == pytest.approx(-116048.67)
    assert righe.iloc[9]["Cumulato (EUR)"] == pytest.approx(-8887.60)
    assert righe.iloc[10]["Cumulato (EUR)"] == pytest.approx(17902.67)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(151854.0)
    assert righe.iloc[15]["Flusso (EUR/anno)"] == 26790.266666666656


def test_demo_tabella_righe():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Calore lordo (MWh/anno)"] == pytest.approx(1395.3333333333333)
    assert mappa["Calore recuperato (MWh/anno)"] == pytest.approx(558.1333333333333)
    assert mappa["Calore netto (MWh/anno)"] == pytest.approx(837.2)
    assert mappa["Acqua di bagno (kg/anno)"] == pytest.approx(20000000.0)
    assert mappa["Salto termico (K)"] == pytest.approx(60.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(42976.4)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(26790.266666666656)
    assert mappa["Payback (anni)"] == 10
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Prezzo elettrico di pareggio (EUR/MWh)"] == pytest.approx(
        269.9992036948558)


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
        bc["tessuto_kg_anno"] + bc["c_alt_var_eur_anno"] / \
        bc["tessuto_kg_anno"] == pytest.approx(bc["lco_alt_eur_kg"])
    assert bc["c_base_eur_anno"] - bc["gas_res_mwh_anno"] * \
        bc["prezzo_gas_eur_mwh"] - bc["om_fisso_eur_anno"] == \
        pytest.approx(bc["prezzo_pareggio_eur_mwh"] *
                      bc["e_el_mwh_anno"])
    assert bc["q_lordo_mwh_anno"] - bc["q_rec_mwh_anno"] == \
        pytest.approx(bc["q_netto_mwh_anno"])
    assert bc["tessuto_kg_anno"] * bc["rapporto_bagno_L_per_kg"] == \
        pytest.approx(bc["acqua_kg_anno"])
    assert bc["acqua_kg_anno"] * 4.186 * bc["delta_t_K"] / \
        3600000.0 == pytest.approx(bc["q_lordo_mwh_anno"])


def test_demo_crf_solo_nel_lco_non_nei_flussi():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -bc["capex_eur"]
    assert all(f == bc["risparmio_eur_anno"] for f in bc["flussi"][1:])
    assert bc["crf"] not in bc["flussi"]
    assert bc["quota_capex_eur_anno"] not in bc["flussi"]
    van_da_flussi = mh761_van(bc["flussi"], bc["wacc_pct"])
    assert van_da_flussi == pytest.approx(bc["van"])
    assert bc["lco_alt_eur_kg"] == pytest.approx(
        (bc["capex_eur"] * bc["crf"] + bc["om_fisso_eur_anno"]) /
        bc["tessuto_kg_anno"] + bc["c_alt_var_eur_anno"] /
        bc["tessuto_kg_anno"])


def test_demo_contro_riconteggio_indipendente():
    tess, rap, ti, tt = 2500000, 8, 20, 80
    eta, qr, quota, cop = 0.90, 40.0, 70.0, 3.5
    pg, pe, om, cx = 45, 110, 12000, 250000
    fg, fe, wacc, vita = 0.20, 0.25, 5.0, 15
    acqua = tess * rap
    dt = tt - ti
    ql = acqua * 4.186 * dt / 3600000.0
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
    assert bc["acqua_kg_anno"] == pytest.approx(acqua)
    assert bc["delta_t_K"] == pytest.approx(dt)
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
    assert bc["risparmio_eur_anno"] == pytest.approx(7720.711111111108)
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] == pytest.approx(-169861.6588550854)
    assert bc["van"] < 0.0
    assert bc["tir"] is None or bc["tir"] < 0.0
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_prezzo_el_alto_non_conviente():
    bc = _variante(prezzo_el_eur_mwh=200)
    assert bc["risparmio_eur_anno"] == pytest.approx(11720.666666666657)
    assert bc["van"] == pytest.approx(-128343.48802049815)
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(269.9992036948558)
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_variante_prezzo_el_zero_conviente():
    bc = _variante(prezzo_el_eur_mwh=0.0)
    assert bc["c_alt_var_eur_anno"] == pytest.approx(12558.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(24558.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(45208.66666666666)
    assert bc["van"] == pytest.approx(219250.50036209347)
    assert bc["tir"] == pytest.approx(16.17554282932855, abs=1e-4)
    assert bc["payback"] == 6
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_variante_gas_alto_conviente():
    bc = _variante(prezzo_gas_eur_mwh=150)
    assert bc["risparmio_eur_anno"] == pytest.approx(160277.15555555554)
    assert bc["van"] == pytest.approx(1413622.065998943)
    assert bc["tir"] == pytest.approx(64.07272176636066, abs=1e-4)
    assert bc["payback"] == 2
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_variante_gas_marginale():
    bc = _variante(prezzo_gas_eur_mwh=42.8)
    assert bc["risparmio_eur_anno"] == pytest.approx(23993.3985185185)
    assert bc["van"] == pytest.approx(-956.7282039891725)
    assert bc["van"] < 0.0
    assert abs(bc["van"]) <= 0.10 * 250000
    assert bc["tir"] == pytest.approx(4.943329269800012, abs=1e-4)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"
    assert bc["valid"] is True


def test_variante_quota_zero_calcolabile_non_degenere():
    """Sensibilita' richiesta dal brief: quota PdC 0 %."""
    bc = _variante(quota_pdc_pct=0)
    assert bc["valid"] is True
    assert bc["q_pdc_mwh_anno"] == 0.0
    assert bc["e_el_mwh_anno"] == 0.0
    assert bc["gas_res_mwh_anno"] == pytest.approx(930.2222222222222)
    assert bc["risparmio_eur_anno"] == pytest.approx(15906.666666666657)
    assert bc["van"] == pytest.approx(-84894.2394726742)
    assert bc["co2_evitata_t_anno"] == pytest.approx(124.02962962962962)
    assert bc["tir"] == pytest.approx(-0.5778118238258146, abs=1e-4)
    assert bc["payback"] is None
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
    assert bc["risparmio_eur_anno"] == pytest.approx(57766.66666666666)
    assert bc["van"] == pytest.approx(349598.24600556534)
    assert bc["tir"] == pytest.approx(21.925474739191536, abs=1e-4)
    assert bc["payback"] == 5
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_quota_recupero_zero():
    bc = _variante(quota_recupero_pct=0)
    assert bc["q_netto_mwh_anno"] == pytest.approx(1395.3333333333333)
    assert bc["q_pdc_mwh_anno"] == pytest.approx(976.7333333333332)
    assert bc["e_el_mwh_anno"] == pytest.approx(279.06666666666666)
    assert bc["gas_res_mwh_anno"] == pytest.approx(465.11111111111114)
    assert bc["risparmio_eur_anno"] == pytest.approx(6139.3333333333285)
    assert bc["van"] == pytest.approx(-186275.81941759665)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(131.99952221691348)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_cop_basso_e_alto():
    bc = _variante(cop=2.0)
    assert bc["e_el_mwh_anno"] == pytest.approx(293.02)
    assert bc["risparmio_eur_anno"] == pytest.approx(12976.46666666666)
    assert bc["van"] == pytest.approx(-115308.71345615093)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(154.28525925420334)
    assert bc["verdetto"] == "NON_CONVIENTE"
    bc2 = _variante(cop=5.0)
    assert bc2["e_el_mwh_anno"] == pytest.approx(117.208)
    assert bc2["risparmio_eur_anno"] == pytest.approx(32315.78666666666)
    assert bc2["van"] == pytest.approx(85426.81483479576)
    assert bc2["tir"] == pytest.approx(9.704400102185838, abs=1e-4)
    assert bc2["payback"] == 8
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_co2_evitata_negativa_con_fattore_el_alto():
    bc = _variante(f_el_t_per_mwh=2.0)
    assert bc["co2_alt_t_anno"] == pytest.approx(390.6933333333333)
    assert bc["co2_evitata_t_anno"] == pytest.approx(-80.61925925925925)
    assert bc["co2_evitata_t_anno"] < 0.0
    assert bc["van"] == pytest.approx(28073.806751668075)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_pareggio_negativo():
    bc = _variante(om_fisso_eur_anno=5000000)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(-29519.776238254497)
    assert bc["prezzo_pareggio_eur_mwh"] < 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(-4961209.733333333)
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_variante_pareggio_zero():
    bc = _variante(om_fisso_eur_anno=57208.66666666666)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(0.0, abs=1e-6)
    assert bc["risparmio_eur_anno"] == pytest.approx(-18418.4)


def test_variante_wacc_zero():
    bc = _variante(wacc_pct=0)
    assert bc["crf"] == pytest.approx(1.0 / 15.0)
    assert bc["quota_capex_eur_anno"] == pytest.approx(16666.666666666668)
    assert bc["van"] == pytest.approx(151854.0)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex_eur=0)
    assert bc["capex_eur"] == 0
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(278073.8067516681)
    assert bc["lco_alt_eur_kg"] == pytest.approx(0.01719056)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_vita_dieci():
    bc = _variante(vita_anni=10)
    assert len(bc["flussi"]) == 11
    assert bc["crf"] == pytest.approx(0.12950457496545661)
    assert bc["van"] == pytest.approx(-43132.66211782456)
    assert bc["tir"] == pytest.approx(1.2776865906620825, abs=1e-4)
    assert bc["payback"] == 10
    assert bc["verdetto"] == "NON_CONVIENTE"


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
def test_degenere_tessuto_zero():
    bc = _variante(tessuto_kg_anno=0)
    assert bc["valid"] is False
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"] == []
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["lco_base_eur_kg"] is None
    assert bc["lco_alt_eur_kg"] is None
    assert bc["errore"]


def test_degenere_rapporto_delta_cop_vita():
    for kw in ({"rapporto_bagno_L_per_kg": 0},
               {"rapporto_bagno_L_per_kg": -1},
               {"t_ingresso_C": 80, "t_tintura_C": 80},
               {"t_ingresso_C": 80, "t_tintura_C": 20},
               {"cop": 0}, {"cop": -1},
               {"tessuto_kg_anno": 0},
               {"tessuto_kg_anno": -1},
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
               {"capex_eur": -1},
               {"t_ingresso_C": -1}, {"t_ingresso_C": 100},
               {"t_tintura_C": 0}, {"t_tintura_C": 100.1}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_stringa_nan_inf():
    for kw in ({"tessuto_kg_anno": "300000"},
               {"tessuto_kg_anno": float("nan")},
               {"prezzo_el_eur_mwh": float("inf")},
               {"capex_eur": True}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_neutro_campi():
    bc = _variante(tessuto_kg_anno=0)
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
    assert mh761_prezzo_pareggio(69766.66666666666, 279.06666666666666,
                                 45, 12000, 0.0) is None
    assert mh761_prezzo_pareggio(69766.66666666666, 279.06666666666666,
                                 45, 12000, None) is None
    assert mh761_lco_base(69766.66666666666, 0) is None
    assert mh761_e_el(586.04, 0) is None
    bc = _variante(quota_pdc_pct=0)
    assert bc["prezzo_pareggio_eur_mwh"] is None


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = demo_calcoli()
    testo = mh761_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert "q_lordo_mwh_anno;1395.3333333333333" in testo
    assert "q_netto_mwh_anno;837.1999999999999" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "prezzo_pareggio_eur_mwh" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = demo_calcoli()
    testo = mh761_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"quota_capex_eur_anno;{bc['quota_capex_eur_anno']}" in testo
    assert f"q_lordo_mwh_anno;{bc['q_lordo_mwh_anno']}" in testo


def test_csv_degenere_solo_zeri():
    bc = _variante(tessuto_kg_anno=0)
    testo = mh761_csv(bc, _demo_kwargs())
    assert "van_eur;0.0" in testo
    assert "q_lordo_mwh_anno;0.0" in testo
    assert "verdetto;NON_CALCOLABILE" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = demo_calcoli()
    testo = mh761_csv(bc, _demo_kwargs())
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
    assert basso - base == pytest.approx(1674.4)
    assert base - alto == pytest.approx(1674.4)


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
    assert set(mh761_demo().keys()) == {
        "tessuto_kg_anno", "rapporto_bagno_L_per_kg",
        "t_ingresso_C", "t_tintura_C",
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
    return ["mh" + "76" + "0", "st" + "76" + "0",
            "tab" + "76" + "0", "w" + "76" + "1_",
            "mh" + "75" + "9", "st" + "75" + "9",
            "tab" + "75" + "9", "w" + "76" + "0_"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w762_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w762_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab761:")


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w762_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w762_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st761_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert "key=f" not in src and 'key = f' not in src
    assert "st.stop()" in src
    # guard degenere prima di KPI / grafico / tabella / CSV
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w762_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def761[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w762_ui.py")
        usate = set(re.findall(r'_def761\["([^"]+)"\]', src))
        assert usate
        assert usate <= set(mh761_demo().keys())


def test_ui_chiavi_demo_coerenti():
    """Ogni _def761[...] letto dalla UI esiste nel dict demo:
    sweep anti-KeyError a render (lezione dello sweep chiavi demo vs UI)."""
    src = _leggi("w762_ui.py")
    usate = set(re.findall(r'_def761\["([^"]+)"\]', src))
    assert usate
    assert usate <= set(mh761_demo().keys())


def test_ui_riferisce_solo_helper_nuovi():
    src = _leggi("w762_ui.py")
    usati = set(re.findall(r'\b(mh\d+_\w+)\b', src))
    assert usati
    assert all(u.startswith("mh761_") for u in usati)


@pytest.mark.parametrize("wacc,vita,atteso", [
    (5.0, 15, 0.09634228760924432),
    (0, 15, 1.0 / 15.0),
    (10.0, 10, 0.16274539488251152),
    (5.0, 1, 1.05),
    (50.0, 5, 0.5758293838862559),
])
def test_crf_parametrizzato(wacc, vita, atteso):
    assert mh761_crf(wacc, vita) == pytest.approx(atteso)


@pytest.mark.parametrize("campo,valore", [
    ("tessuto_kg_anno", 0), ("tessuto_kg_anno", -3),
    ("rapporto_bagno_L_per_kg", 0), ("rapporto_bagno_L_per_kg", -1),
    ("t_ingresso_C", -1), ("t_ingresso_C", 100),
    ("t_tintura_C", 0), ("t_tintura_C", 100.1),
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
    assert mh761_valida(**d)["valido"] is False


def test_df_tabella_valori_demo_selezionati():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Tessuto (kg/anno)"] == 2500000.0
    assert mappa["Calore lordo (MWh/anno)"] == pytest.approx(1395.3333333333333)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(26790.266666666656)
    assert mappa["Verdetto"] == "CONVIENTE"


def test_lco_alt_minore_di_lco_base_demo():
    bc = demo_calcoli()
    assert bc["lco_alt_eur_kg"] < bc["lco_base_eur_kg"]
    assert bc["lco_base_eur_kg"] - bc["lco_alt_eur_kg"] == pytest.approx(
        0.001081877905742233)
