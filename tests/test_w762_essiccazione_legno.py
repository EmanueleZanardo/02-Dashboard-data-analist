"""Test tab762 "Essiccazione del legno:
essiccare il legname con pompa di calore batte
l'essiccatore a gas?"

Nuova tab tab762 (essiccazione legname,
file di lavoro w763).
Business case deterministico
dell'essiccazione del legname in un
essiccatoio industriale: il legname verde
va essiccato dal contenuto di umidita'
iniziale al contenuto di umidita' finale
(base umida), scaldato dalla temperatura
di ingresso alla temperatura di
essiccazione, e il calore puo' arrivare
dall'essiccatore a gas (baseline, tutto
il calore lordo, senza recupero) oppure
in parte dal calore recuperato dall'aria
esausta calda e in parte da una pompa di
calore che copre una quota del calore
netto, con il resto che resta a gas.
Massa secca = legname verde x (1 - u_i /
100); massa essiccata = massa secca /
(1 - u_f / 100); acqua evaporata =
legname verde - massa essiccata;
delta_T = T_ess - T_ingresso; Q_evap =
acqua evaporata x 1000 x 2257 /
3600000; Q_risc = legname verde x 1000
x 2,0 x delta_T / 3600000; Q_lordo =
Q_evap + Q_risc; Q_rec =
quota_recupero / 100 x Q_lordo;
Q_netto = Q_lordo - Q_rec;
gas_base = Q_lordo / eta_essiccatore;
C_base = gas_base x p_gas;
co2_base = gas_base x f_gas;
Q_pdc = quota_pdc / 100 x Q_netto;
E_el = Q_pdc / COP; gas_res =
(1 - quota_pdc / 100) x Q_netto /
eta_essiccatore; C_alt_var = gas_res x
p_gas + E_el x p_el; C_alt =
C_alt_var + OM_fisso; co2_alt =
gas_res x f_gas + E_el x f_el;
risparmio = C_base - C_alt;
CO2 evitata = co2_base - co2_alt,
segno libero (puo' essere negativa),
NON monetizzata; CRF solo nel LCO,
mai nei flussi; LCO_base = C_base /
massa essiccata; LCO_alt = (CAPEX x CRF +
OM_fisso) / massa essiccata + C_alt_var /
massa essiccata; prezzo elettrico di
pareggio = (C_base - gas_res x
p_gas - OM_fisso) / E_el, None se
E_el <= 0, puo' essere negativo (il
solo O&M fisso piu' il gas residuo
superano gia' il costo baseline);
flussi [-CAPEX, risparmio x vita];
VAN, TIR, payback (primo anno con
cumulato >= 0). Distinta dalla tab
della cartiera (li' si essicca carta,
senza legname, senza umidita' del legno
in % base umida, senza massa secca di
legname, senza acqua evaporata dal
legname), dalla tab della tintoria (li'
si tinge tessuto in bagni caldi, senza
legname, senza umidita' del legno, senza
acqua evaporata, senza calore latente di
evaporazione), dalla tab del caseificio
(li' si pastorizza latte, senza legname
e senza essiccazione), dalla tab del
birrificio (li' si produce birra, senza
legname e senza essiccazione), dalla tab
del conservificio (li' si sterilizzano
conserve in autoclave, senza legname e
senza essiccazione), dalla tab della
lavanderia (li' si lava biancheria,
senza legname, senza umidita' del legno,
senza acqua evaporata), dalla caldaia a
elettrodi generica (li' il calore viene
da elettrodi, senza processo di
essiccazione del legno e senza quota di
recupero) e dal recupero calore generico
(li' il calore recuperato va a un uso
generico, senza essiccazione del legname
e senza pompa di calore sul calore
netto).

Demo calcolata eseguendo demo_calcoli()
(e ricontrollata a mano, riga per
riga): legname verde 2.000 t/anno,
umidita' iniziale 50 % (base umida),
umidita' finale 12 %, temperatura
ingresso 20 C, temperatura essiccazione
70 C, rendimento essiccatore 0,85, quota
recupero 40 %, quota PdC 70 %,
COP 3,2, prezzo gas 45 EUR/MWh,
prezzo elettrico 110 EUR/MWh, O&M
fisso 10.000 EUR/anno, CAPEX 220.000
EUR, fattore gas 0,20 tCO2/MWh e
fattore elettrico 0,25 tCO2/MWh,
WACC 5 %, vita 15 anni, tolleranza
10 % del CAPEX.

- m_secca_t_anno = 1000.0
- m_finale_t_anno = 1136.3636363636363
- m_acqua_t_anno = 863.6363636363637
- delta_t_K = 50.0
- q_evap_mwh_anno = 541.4520202020203
- q_risc_mwh_anno = 55.55555555555556
- q_lordo_mwh_anno = 597.0075757575759
- q_rec_mwh_anno = 238.80303030303037
- q_netto_mwh_anno = 358.2045454545455
- gas_base_mwh_anno = 702.3618538324422
- c_base_eur_anno = 31606.2834224599
- q_pdc_mwh_anno = 250.74318181818182
- e_el_mwh_anno = 78.35724431818181
- gas_res_mwh_anno = 126.42513368983961
- c_alt_var_eur_anno = 14308.427891042782
- c_alt_eur_anno = 24308.427891042782
- risparmio_eur_anno = 7297.855531417117
- co2_base_t_anno = 140.47237076648844
- co2_alt_gas_t_anno = 25.285026737967925
- co2_alt_el_t_anno = 19.589311079545453
- co2_alt_t_anno = 44.87433781751338
- co2_evitata_t_anno = 95.59803294897506
- crf = 0.09634228760924432
- quota_capex_eur_anno = 21195.30327403375
- lco_base_eur_t = 27.813529411764712
- lco_alt_eur_t = 40.043283425267354
- van = -144250.75517184564
- tir = -7.678286308146144
- payback = None
- prezzo_pareggio_eur_mwh = 203.13568381479877
- verdetto = 'NON_CONVIENTE'

Scomposizione: massa secca = 2.000 x
(1 - 0,50) = 1.000 t/anno; massa
essiccata = 1.000 / (1 - 0,12) =
1.136,36 t/anno; acqua evaporata =
2.000 - 1.136,36 = 863,64 t/anno;
delta_T = 70 - 20 = 50 K; Q_evap =
863,64 x 1000 x 2257 / 3.600.000 =
541,45 MWh/anno; Q_risc = 2.000 x 1000
x 2,0 x 50 / 3.600.000 = 55,56 MWh/anno;
Q_lordo = 541,45 + 55,56 = 597,01
MWh/anno; Q_rec = 0,40 x 597,01 =
238,80 MWh/anno; Q_netto = 597,01 -
238,80 = 358,20 MWh/anno; gas_base =
597,01 / 0,85 = 702,36 MWh/anno;
C_base = 702,36 x 45 = 31.606,28
EUR/anno; Q_pdc = 0,70 x 358,20 =
250,74 MWh/anno; E_el = 250,74 / 3,2 =
78,36 MWh/anno; gas_res = 0,30 x 358,20
/ 0,85 = 126,43 MWh/anno;
C_alt_var = 126,43 x 45 + 78,36 x 110
= 5.689,13 + 8.619,30 = 14.308,43
EUR/anno; C_alt = 14.308,43 + 10.000 =
24.308,43 EUR/anno; risparmio =
31.606,28 - 24.308,43 = 7.297,86
EUR/anno; CO2 base = 702,36 x 0,20 =
140,47 t/anno; CO2 alt = 126,43 x 0,20 +
78,36 x 0,25 = 25,29 + 19,59 = 44,87
t/anno; CO2 evitata = 95,60 t/anno;
CRF 0,05 x 1,05^15 / (1,05^15 - 1) =
0.09634228760924432; quota CAPEX
220.000 x 0,096342 = 21.195,30
EUR/anno; LCO base 31.606,28 /
1.136,36 = 27,81 EUR/t; LCO alt
(21.195,30 + 10.000) / 1.136,36 +
14.308,43 / 1.136,36 = 40,04 EUR/t;
flussi: anno 0 -220.000, anni 1-15
risparmio 7.297,86 (piatti); VAN
-220.000 + 7.297,86 x 10,379658
(annuita' 15 anni al 5 %) =
-144.250,76 EUR; TIR -7,68 %; nessun
payback (il cumulato all'anno 15 e'
-110.532,17 EUR); prezzo elettrico di
pareggio (31.606,28 - 5.689,13 -
10.000) / 78,36 = 203,14 EUR/MWh;
verdetto NON_CONVIENTE perche' VAN < 0
e |VAN| = 144.250,76 > 10 % del CAPEX
(22.000): il risparmio annuo positivo
NON basta a ripagare il CAPEX in 15
anni al 5 %.
NOTA: il CRF entra solo nel LCO,
mai nei flussi: il CAPEX compare una
sola volta, all'anno 0.
NOTA 2: in questo brief il risparmio
nullo o negativo NON e' degenere:
con prezzo gas 30 EUR/MWh il
risparmio e' -1.341,20 EUR/anno e il
caso resta calcolabile (valid=True,
VAN -233.921,15 EUR, NON_CONVIENTE).
NOTA 3: la CO2 evitata puo' essere
negativa: con fattore elettrico 2,00
tCO2/MWh la CO2 evitata e'
-41,53 t/anno, pur restando il caso
calcolabile.
NOTA 4: il prezzo elettrico di
pareggio puo' essere negativo: con
O&M fisso 5.000.000 EUR/anno il
pareggio e' -63.479,55 EUR/MWh,
perche' il solo O&M fisso piu' il
gas residuo superano gia' il costo
baseline (il caso demo ha pareggio
positivo, 203,14 EUR/MWh).
NOTA 5: la quota PdC zero NON e'
degenere: con quota 0 il risparmio
e' 2.642,51 EUR/anno, la VAN
-192.571,61 EUR e il pareggio non
e' definito (E_el nulla).
NOTA 6: il calore netto nullo (quota
recupero 100 %) NON e' degenere:
il risparmio e' 21.606,28 EUR/anno
(31.606,28 - 10.000 di solo O&M fisso)
e la VAN 4.265,83 EUR, e il
pareggio non e' definito.
NOTA 7: l'umidita' iniziale deve
superare l'umidita' finale e la
temperatura di essiccazione deve
superare la temperatura di ingresso:
con u_i = u_f (nessuna acqua da
evaporare) o con T_ess = T_ingresso
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

from w763_helpers import (
    demo_calcoli,
    mh762_c_alt,
    mh762_c_alt_var,
    mh762_c_base,
    mh762_calcola,
    mh762_co2_alt,
    mh762_co2_base,
    mh762_co2_evitata,
    mh762_crf,
    mh762_csv,
    mh762_delta_t,
    mh762_demo,
    mh762_e_el,
    mh762_eta,
    mh762_flussi,
    mh762_gas_base,
    mh762_gas_res,
    mh762_int_pos,
    mh762_lco_alt,
    mh762_lco_base,
    mh762_m_acqua,
    mh762_m_finale,
    mh762_m_secca,
    mh762_nneg,
    mh762_num,
    mh762_payback,
    mh762_pct_0_100,
    mh762_pct_wacc,
    mh762_pos,
    mh762_prezzo_pareggio,
    mh762_q_evap,
    mh762_q_lordo,
    mh762_q_netto,
    mh762_q_pdc,
    mh762_q_rec,
    mh762_q_risc,
    mh762_quota_capex,
    mh762_risparmio,
    mh762_temp_ess,
    mh762_temp_ingresso,
    mh762_tir,
    mh762_u_finale,
    mh762_u_iniziale,
    mh762_valida,
    mh762_van,
    mh762_verdetto,
)


def _demo_kwargs():
    return dict(mh762_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh762_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh762_num(3, "x") == 3.0
    assert mh762_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh762_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh762_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh762_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh762_pos(0, "x")
    with pytest.raises(ValueError):
        mh762_pos(-1, "x")
    assert mh762_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh762_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh762_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh762_int_pos(0, "x")


def test_pct_0_100_limiti():
    assert mh762_pct_0_100(0, "x") == 0.0
    assert mh762_pct_0_100(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh762_pct_0_100(100.1, "x")
    with pytest.raises(ValueError):
        mh762_pct_0_100(-1, "x")


def test_pct_wacc_limiti():
    assert mh762_pct_wacc(0, "x") == 0.0
    assert mh762_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh762_pct_wacc(50.1, "x")


def test_eta_limiti():
    assert mh762_eta(1.0, "x") == 1.0
    assert mh762_eta(0.85, "x") == 0.85
    with pytest.raises(ValueError):
        mh762_eta(0, "x")
    with pytest.raises(ValueError):
        mh762_eta(-0.1, "x")
    with pytest.raises(ValueError):
        mh762_eta(1.01, "x")


def test_temp_limiti():
    assert mh762_temp_ingresso(0, "x") == 0.0
    assert mh762_temp_ingresso(99.0, "x") == 99.0
    with pytest.raises(ValueError):
        mh762_temp_ingresso(100, "x")
    with pytest.raises(ValueError):
        mh762_temp_ingresso(-1, "x")
    assert mh762_temp_ess(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh762_temp_ess(0, "x")
    with pytest.raises(ValueError):
        mh762_temp_ess(100.1, "x")


def test_umidita_limiti():
    assert mh762_u_iniziale(50, "x") == 50.0
    assert mh762_u_iniziale(99.9, "x") == 99.9
    with pytest.raises(ValueError):
        mh762_u_iniziale(0, "x")
    with pytest.raises(ValueError):
        mh762_u_iniziale(100, "x")
    with pytest.raises(ValueError):
        mh762_u_iniziale(-1, "x")
    assert mh762_u_finale(0, "x") == 0.0
    assert mh762_u_finale(12, "x") == 12.0
    with pytest.raises(ValueError):
        mh762_u_finale(100, "x")
    with pytest.raises(ValueError):
        mh762_u_finale(-1, "x")


# ---------------------------------------------------------------- fisica base
def test_masse():
    assert mh762_m_secca(2000, 50.0) == pytest.approx(1000.0)
    assert mh762_m_secca(2000, 0) == pytest.approx(2000.0)
    assert mh762_m_secca(2000, 100) == pytest.approx(0.0)
    assert mh762_m_finale(1000.0, 12.0) == pytest.approx(1136.3636363636363)
    assert mh762_m_finale(1000.0, 0) == pytest.approx(1000.0)
    assert mh762_m_acqua(2000, 1136.3636363636363) == pytest.approx(
        863.6363636363637)
    assert mh762_m_acqua(2000, 2000) == 0.0
    with pytest.raises(ValueError):
        mh762_m_finale(1000.0, 100)
    with pytest.raises(ValueError):
        mh762_m_secca(2000, 100.1)


def test_delta_q_evap_q_risc_q_lordo():
    assert mh762_delta_t(20, 70) == pytest.approx(50.0)
    assert mh762_delta_t(70, 20) == pytest.approx(-50.0)
    assert mh762_q_evap(863.6363636363637) == pytest.approx(541.4520202020203)
    assert mh762_q_evap(0) == 0.0
    assert mh762_q_risc(2000, 50.0) == pytest.approx(55.55555555555556)
    assert mh762_q_risc(2000, 0) == 0.0
    assert mh762_q_lordo(541.4520202020203, 55.55555555555556) == \
        pytest.approx(597.0075757575759)
    with pytest.raises(ValueError):
        mh762_q_evap(-1)
    with pytest.raises(ValueError):
        mh762_q_risc(-1, 50.0)


def test_q_rec_netto():
    assert mh762_q_rec(597.0075757575759, 40.0) == pytest.approx(
        238.80303030303037)
    assert mh762_q_rec(597.0075757575759, 0) == 0.0
    assert mh762_q_rec(597.0075757575759, 100) == pytest.approx(
        597.0075757575759)
    assert mh762_q_netto(597.0075757575759, 238.80303030303037) == \
        pytest.approx(358.2045454545455)
    assert mh762_q_netto(597.0075757575759, 597.0075757575759) == 0.0
    with pytest.raises(ValueError):
        mh762_q_rec(597.0075757575759, 100.1)


def test_gas_base_e_c_base_e_co2_base():
    assert mh762_gas_base(597.0075757575759, 0.85) == pytest.approx(
        702.3618538324422)
    assert mh762_gas_base(597.0075757575759, 1.0) == pytest.approx(
        597.0075757575759)
    assert mh762_c_base(702.3618538324422, 45) == pytest.approx(
        31606.2834224599)
    assert mh762_co2_base(702.3618538324422, 0.20) == pytest.approx(
        140.47237076648844)
    with pytest.raises(ValueError):
        mh762_gas_base(597.0075757575759, 0)


def test_q_pdc_e_e_el():
    assert mh762_q_pdc(358.2045454545455, 70.0) == pytest.approx(
        250.74318181818182)
    assert mh762_q_pdc(358.2045454545455, 0) == 0.0
    assert mh762_q_pdc(358.2045454545455, 100) == pytest.approx(
        358.2045454545455)
    assert mh762_e_el(250.74318181818182, 3.2) == pytest.approx(
        78.35724431818181)
    assert mh762_e_el(250.74318181818182, 0) is None
    assert mh762_e_el(250.74318181818182, -1.0) is None
    assert mh762_e_el(0.0, 3.2) == 0.0
    with pytest.raises(ValueError):
        mh762_q_pdc(358.2045454545455, 100.1)


def test_gas_res():
    assert mh762_gas_res(358.2045454545455, 70.0, 0.85) == pytest.approx(
        126.42513368983961)
    assert mh762_gas_res(358.2045454545455, 0, 0.85) == pytest.approx(
        421.4171122994653)
    assert mh762_gas_res(358.2045454545455, 100, 0.85) == 0.0
    with pytest.raises(ValueError):
        mh762_gas_res(358.2045454545455, 70.0, 0)


def test_c_alt_var_e_c_alt():
    assert mh762_c_alt_var(126.42513368983961, 45, 78.35724431818181,
                           110) == pytest.approx(14308.427891042782)
    assert mh762_c_alt_var(126.42513368983961, 45, 0.0,
                           110) == pytest.approx(5689.131016042783)
    assert mh762_c_alt(14308.427891042782, 10000) == pytest.approx(
        24308.427891042782)
    assert mh762_c_alt(14308.427891042782, 0) == pytest.approx(
        14308.427891042782)
    with pytest.raises(ValueError):
        mh762_c_alt_var(126.42513368983961, -1, 78.35724431818181, 110)


def test_risparmio_segno():
    assert mh762_risparmio(31606.2834224599, 24308.427891042782) == \
        pytest.approx(7297.855531417117)
    assert mh762_risparmio(31606.2834224599, 31606.2834224599) == 0.0


def test_co2_alt_e_evitata_segno_libero():
    assert mh762_co2_alt(126.42513368983961, 0.20, 78.35724431818181,
                         0.25) == pytest.approx(44.87433781751338)
    assert mh762_co2_evitata(140.47237076648844,
                             44.87433781751338) == pytest.approx(
        95.59803294897506)
    assert mh762_co2_evitata(140.47237076648844,
                             740.47237076648844) == pytest.approx(
        -600.0, abs=1e-6)


# ---------------------------------------------------------------- finanza base
def test_crf():
    assert mh762_crf(5.0, 15) == pytest.approx(0.09634228760924432)
    assert mh762_crf(0, 15) == pytest.approx(1.0 / 15.0)
    assert mh762_crf(5.0, 1) == pytest.approx(1.05)
    assert mh762_crf(5.0, 10) == pytest.approx(0.12950457496545661)


def test_quota_capex_e_lco():
    assert mh762_quota_capex(220000, 0.09634228760924432) == pytest.approx(
        21195.30327403375)
    assert mh762_lco_base(31606.2834224599, 1136.3636363636363) == \
        pytest.approx(27.813529411764712)
    assert mh762_lco_base(31606.2834224599, 0) is None
    assert mh762_lco_alt(220000, 0.09634228760924432, 10000,
                         14308.427891042782,
                         1136.3636363636363) == pytest.approx(
        40.043283425267354)
    assert mh762_lco_alt(220000, 0.09634228760924432, 10000,
                         14308.427891042782, 0) is None
    assert mh762_lco_alt(0, 0.09634228760924432, 10000,
                         14308.427891042782,
                         1136.3636363636363) == pytest.approx(
        21.39141654411765)


def test_prezzo_pareggio_formula_brief_negativo_e_none():
    assert mh762_prezzo_pareggio(31606.2834224599, 126.42513368983961,
                                 45, 10000,
                                 78.35724431818181) == pytest.approx(
        203.13568381479877)
    assert mh762_prezzo_pareggio(31606.2834224599, 126.42513368983961,
                                 45, 25917.152406417117,
                                 78.35724431818181) == pytest.approx(
        0.0, abs=1e-6)
    assert mh762_prezzo_pareggio(31606.2834224599, 126.42513368983961,
                                 45, 10000, 0.0) is None
    assert mh762_prezzo_pareggio(31606.2834224599, 126.42513368983961,
                                 45, 10000, None) is None


def test_flussi_lunghezza_e_primo():
    fl = mh762_flussi(220000, 7297.855531417117, 15)
    assert len(fl) == 16
    assert fl[0] == -220000
    assert all(f == 7297.855531417117 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = demo_calcoli()
    assert bc["van"] == pytest.approx(-144250.75517184564)
    assert mh762_van([-220000] + [7297.855531417117] * 15,
                     0) == pytest.approx(-110532.16702874325)
    assert mh762_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo_e_negativa():
    bc = demo_calcoli()
    assert bc["tir"] == pytest.approx(-7.678286308146144)
    assert mh762_tir([-220000] + [7297.855531417117] * 15) == pytest.approx(
        -0.07678286308146144)
    tir = mh762_tir([-220000] + [7297.855531417117] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-220000] + [7297.855531417117] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback():
    assert mh762_payback([-220000] + [7297.855531417117] * 15) is None
    assert mh762_payback([-220000] + [-1000.0] * 15) is None
    assert mh762_payback([0] + [7297.855531417117] * 15) == 0
    assert mh762_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh762_verdetto(100.0, 220000, 10.0) == "CONVIENTE"
    assert mh762_verdetto(-21000.0, 220000, 10.0) == "MARGINALE"
    assert mh762_verdetto(-22000.0, 220000, 10.0) == "MARGINALE"
    assert mh762_verdetto(-22000.01, 220000, 10.0) == "NON_CONVIENTE"
    assert mh762_verdetto(float("nan"), 220000, 10.0) == "NON_CALCOLABILE"
    assert mh762_verdetto(0.0, 0, 10.0) == "MARGINALE"


def test_valida_demo_ok():
    v = mh762_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("m_verde_t_anno", "3000"),
                       ("m_verde_t_anno", float("nan")),
                       ("m_verde_t_anno", float("inf")),
                       ("m_verde_t_anno", True),
                       ("prezzo_el_eur_mwh", None)):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh762_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("m_verde_t_anno", 0),
                          ("m_verde_t_anno", -1),
                          ("u_i_pct", 0),
                          ("u_i_pct", 100),
                          ("u_i_pct", -1),
                          ("u_f_pct", -1),
                          ("u_f_pct", 100),
                          ("t_ingresso_C", -1),
                          ("t_ingresso_C", 100),
                          ("t_ess_C", 0),
                          ("t_ess_C", 100.1),
                          ("eta_essiccatore", 0),
                          ("eta_essiccatore", 1.01),
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
        assert mh762_valida(**d)["valido"] is False


def test_valida_rifiuta_delta_e_umidita_non_validi():
    for ti, te in ((70, 70), (70, 20), (20, 20)):
        d = _demo_kwargs()
        d["t_ingresso_C"] = ti
        d["t_ess_C"] = te
        assert mh762_valida(**d)["valido"] is False
    for ui, uf in ((12, 12), (12, 50), (5, 12)):
        d = _demo_kwargs()
        d["u_i_pct"] = ui
        d["u_f_pct"] = uf
        assert mh762_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"quota_recupero_pct": 0, "quota_pdc_pct": 0,
              "prezzo_gas_eur_mwh": 0,
              "prezzo_el_eur_mwh": 0, "om_fisso_eur_anno": 0,
              "capex_eur": 0, "f_gas_t_per_mwh": 0,
              "f_el_t_per_mwh": 0, "wacc_pct": 0,
              "tolleranza_pct": 0, "eta_essiccatore": 1.0,
              "t_ingresso_C": 0, "t_ess_C": 100,
              "u_i_pct": 99, "u_f_pct": 0})
    assert mh762_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["quota_pdc_pct"] = 100
    d["quota_recupero_pct"] = 100
    assert mh762_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh762_demo()
    assert d["m_verde_t_anno"] == 2000
    assert d["u_i_pct"] == 50.0
    assert d["u_f_pct"] == 12.0
    assert d["t_ingresso_C"] == 20
    assert d["t_ess_C"] == 70
    assert d["eta_essiccatore"] == 0.85
    assert d["quota_recupero_pct"] == 40.0
    assert d["quota_pdc_pct"] == 70.0
    assert d["cop"] == 3.2
    assert d["prezzo_gas_eur_mwh"] == 45
    assert d["prezzo_el_eur_mwh"] == 110
    assert d["om_fisso_eur_anno"] == 10000
    assert d["capex_eur"] == 220000
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
        "m_secca_t_anno": 1000.0,
        "m_finale_t_anno": 1136.3636363636363,
        "m_acqua_t_anno": 863.6363636363637,
        "delta_t_K": 50.0,
        "q_evap_mwh_anno": 541.4520202020203,
        "q_risc_mwh_anno": 55.55555555555556,
        "q_lordo_mwh_anno": 597.0075757575759,
        "q_rec_mwh_anno": 238.80303030303037,
        "q_netto_mwh_anno": 358.2045454545455,
        "gas_base_mwh_anno": 702.3618538324422,
        "c_base_eur_anno": 31606.2834224599,
        "q_pdc_mwh_anno": 250.74318181818182,
        "e_el_mwh_anno": 78.35724431818181,
        "gas_res_mwh_anno": 126.42513368983961,
        "c_alt_var_eur_anno": 14308.427891042782,
        "c_alt_eur_anno": 24308.427891042782,
        "risparmio_eur_anno": 7297.855531417117,
        "co2_base_t_anno": 140.47237076648844,
        "co2_alt_t_anno": 44.87433781751338,
        "co2_evitata_t_anno": 95.59803294897506,
        "crf": 0.09634228760924432,
        "quota_capex_eur_anno": 21195.30327403375,
        "lco_base_eur_t": 27.813529411764712,
        "lco_alt_eur_t": 40.043283425267354,
        "van": -144250.75517184564,
        "tir": -7.678286308146144,
        "prezzo_pareggio_eur_mwh": 203.13568381479877,
    }
    for chiave, atteso in attesi.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert abs(got - atteso) / abs(atteso) < 1e-9, chiave
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_demo_calcoli_fisica():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["m_secca_t_anno"] == pytest.approx(1000.0)
    assert bc["m_finale_t_anno"] == pytest.approx(1136.3636363636363)
    assert bc["m_acqua_t_anno"] == pytest.approx(863.6363636363637)
    assert bc["q_evap_mwh_anno"] == pytest.approx(541.4520202020203)
    assert bc["q_risc_mwh_anno"] == pytest.approx(55.55555555555556)
    assert bc["q_lordo_mwh_anno"] == pytest.approx(597.0075757575759)
    assert bc["q_rec_mwh_anno"] == pytest.approx(238.80303030303037)
    assert bc["q_netto_mwh_anno"] == pytest.approx(358.2045454545455)
    assert bc["gas_base_mwh_anno"] == pytest.approx(702.3618538324422)
    assert bc["co2_evitata_t_anno"] == pytest.approx(95.59803294897506)


def test_demo_calcoli_economia():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(31606.2834224599)
    assert bc["c_alt_var_eur_anno"] == pytest.approx(14308.427891042782)
    assert bc["c_alt_eur_anno"] == pytest.approx(24308.427891042782)
    assert bc["risparmio_eur_anno"] == pytest.approx(7297.855531417117)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(203.13568381479877)


def test_demo_calcoli_finanza():
    bc = demo_calcoli()
    assert bc["crf"] == pytest.approx(0.09634228760924432)
    assert bc["quota_capex_eur_anno"] == pytest.approx(21195.30327403375)
    assert bc["lco_base_eur_t"] == pytest.approx(27.813529411764712)
    assert bc["lco_alt_eur_t"] == pytest.approx(40.043283425267354)
    assert bc["van"] == pytest.approx(-144250.75517184564)
    assert bc["tir"] == pytest.approx(-7.678286308146144)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_demo_flussi_e_cumulato():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -220000
    assert len(bc["flussi"]) == 16
    assert all(f == 7297.855531417117 for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -220000
    assert righe.iloc[5]["Cumulato (EUR)"] == pytest.approx(-183510.72)
    assert righe.iloc[9]["Cumulato (EUR)"] == pytest.approx(-154319.30)
    assert righe.iloc[10]["Cumulato (EUR)"] == pytest.approx(-147021.44)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(-110532.17)
    assert righe.iloc[15]["Flusso (EUR/anno)"] == 7297.855531417117


def test_demo_tabella_righe():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Calore lordo (MWh/anno)"] == pytest.approx(597.0075757575759)
    assert mappa["Calore recuperato (MWh/anno)"] == pytest.approx(238.80303030303037)
    assert mappa["Calore netto (MWh/anno)"] == pytest.approx(358.2045454545455)
    assert mappa["Massa essiccata (t/anno)"] == pytest.approx(1136.3636363636363)
    assert mappa["Acqua evaporata (t/anno)"] == pytest.approx(863.6363636363637)
    assert mappa["Salto termico (K)"] == pytest.approx(50.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(24308.427891042782)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(7297.855531417117)
    assert mappa["Payback (anni)"] is None
    assert mappa["Verdetto"] == "NON_CONVIENTE"
    assert mappa["Prezzo elettrico di pareggio (EUR/MWh)"] == pytest.approx(
        203.13568381479877)


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
        bc["m_finale_t_anno"] + bc["c_alt_var_eur_anno"] / \
        bc["m_finale_t_anno"] == pytest.approx(bc["lco_alt_eur_t"])
    assert bc["c_base_eur_anno"] - bc["gas_res_mwh_anno"] * \
        bc["prezzo_gas_eur_mwh"] - bc["om_fisso_eur_anno"] == \
        pytest.approx(bc["prezzo_pareggio_eur_mwh"] *
                      bc["e_el_mwh_anno"])
    assert bc["q_lordo_mwh_anno"] - bc["q_rec_mwh_anno"] == \
        pytest.approx(bc["q_netto_mwh_anno"])
    assert bc["q_evap_mwh_anno"] + bc["q_risc_mwh_anno"] == \
        pytest.approx(bc["q_lordo_mwh_anno"])
    assert bc["m_verde_t_anno"] * (1.0 - bc["u_i_pct"] / 100.0) == \
        pytest.approx(bc["m_secca_t_anno"])
    assert bc["m_secca_t_anno"] / (1.0 - bc["u_f_pct"] / 100.0) == \
        pytest.approx(bc["m_finale_t_anno"])
    assert bc["m_verde_t_anno"] - bc["m_finale_t_anno"] == \
        pytest.approx(bc["m_acqua_t_anno"])
    assert bc["m_acqua_t_anno"] * 1000.0 * 2257.0 / \
        3600000.0 == pytest.approx(bc["q_evap_mwh_anno"])


def test_demo_crf_solo_nel_lco_non_nei_flussi():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -bc["capex_eur"]
    assert all(f == bc["risparmio_eur_anno"] for f in bc["flussi"][1:])
    assert bc["crf"] not in bc["flussi"]
    assert bc["quota_capex_eur_anno"] not in bc["flussi"]
    van_da_flussi = mh762_van(bc["flussi"], bc["wacc_pct"])
    assert van_da_flussi == pytest.approx(bc["van"])
    assert bc["lco_alt_eur_t"] == pytest.approx(
        (bc["capex_eur"] * bc["crf"] + bc["om_fisso_eur_anno"]) /
        bc["m_finale_t_anno"] + bc["c_alt_var_eur_anno"] /
        bc["m_finale_t_anno"])


def test_demo_contro_riconteggio_indipendente():
    mv, ui, uf, ti, te = 2000, 50.0, 12.0, 20, 70
    eta, qr, quota, cop = 0.85, 40.0, 70.0, 3.2
    pg, pe, om, cx = 45, 110, 10000, 220000
    fg, fe, wacc, vita = 0.20, 0.25, 5.0, 15
    ms = mv * (1 - ui / 100)
    mf = ms / (1 - uf / 100)
    ma = mv - mf
    qe = ma * 1000 * 2257 / 3600000.0
    qri = mv * 1000 * 2.0 * (te - ti) / 3600000.0
    ql = qe + qri
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
    assert bc["m_secca_t_anno"] == pytest.approx(ms)
    assert bc["m_finale_t_anno"] == pytest.approx(mf)
    assert bc["m_acqua_t_anno"] == pytest.approx(ma)
    assert bc["q_evap_mwh_anno"] == pytest.approx(qe)
    assert bc["q_risc_mwh_anno"] == pytest.approx(qri)
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
def test_demo_non_conviente():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] < 0.0
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_gas_trenta_segno_e_verdetto():
    """Sensibilita' richiesta dal brief: gas 30 EUR/MWh."""
    bc = _variante(prezzo_gas_eur_mwh=30)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(-1341.1952707219243)
    assert bc["risparmio_eur_anno"] < 0.0
    assert bc["van"] == pytest.approx(-233921.14827251862)
    assert bc["van"] < 0.0
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_prezzo_el_alto_non_conviente():
    bc = _variante(prezzo_el_eur_mwh=200)
    assert bc["risparmio_eur_anno"] == pytest.approx(245.7035427807532)
    assert bc["van"] == pytest.approx(-217449.6812471663)
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(203.13568381479877)
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_variante_prezzo_el_zero_non_conviente():
    bc = _variante(prezzo_el_eur_mwh=0.0)
    assert bc["c_alt_var_eur_anno"] == pytest.approx(5689.131016042783)
    assert bc["c_alt_eur_anno"] == pytest.approx(15689.131016042782)
    assert bc["risparmio_eur_anno"] == pytest.approx(15917.152406417117)
    assert bc["van"] == pytest.approx(-54785.40107978704)
    assert bc["tir"] == pytest.approx(1.040627789341155, abs=1e-4)
    assert bc["payback"] == 14
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_variante_gas_alto_conviente():
    bc = _variante(prezzo_gas_eur_mwh=150)
    assert bc["risparmio_eur_anno"] == pytest.approx(67771.21114639039)
    assert bc["van"] == pytest.approx(483441.996532865)
    assert bc["tir"] == pytest.approx(30.218220120582995, abs=1e-4)
    assert bc["payback"] == 4
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_variante_gas_marginale():
    bc = _variante(prezzo_gas_eur_mwh=69.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(21120.336814839575)
    assert bc["van"] == pytest.approx(-778.126210768969)
    assert bc["van"] < 0.0
    assert abs(bc["van"]) <= 0.10 * 220000
    assert bc["tir"] == pytest.approx(4.947627162800752, abs=1e-4)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"
    assert bc["valid"] is True


def test_variante_quota_zero_calcolabile_non_degenere():
    """Sensibilita' richiesta dal brief: quota PdC 0 %."""
    bc = _variante(quota_pdc_pct=0)
    assert bc["valid"] is True
    assert bc["q_pdc_mwh_anno"] == 0.0
    assert bc["e_el_mwh_anno"] == 0.0
    assert bc["gas_res_mwh_anno"] == pytest.approx(421.4171122994653)
    assert bc["risparmio_eur_anno"] == pytest.approx(2642.5133689839604)
    assert bc["van"] == pytest.approx(-192571.61486862597)
    assert bc["co2_evitata_t_anno"] == pytest.approx(56.188948306595364)
    assert bc["tir"] == pytest.approx(-16.38197403187797, abs=1e-4)
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
    assert bc["risparmio_eur_anno"] == pytest.approx(21606.2834224599)
    assert bc["van"] == pytest.approx(4265.833401143927)
    assert bc["tir"] == pytest.approx(5.285496261659485, abs=1e-4)
    assert bc["payback"] == 11
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_quota_recupero_zero():
    bc = _variante(quota_recupero_pct=0)
    assert bc["q_netto_mwh_anno"] == pytest.approx(597.0075757575759)
    assert bc["q_pdc_mwh_anno"] == pytest.approx(417.90530303030306)
    assert bc["e_el_mwh_anno"] == pytest.approx(130.5954071969697)
    assert bc["gas_res_mwh_anno"] == pytest.approx(210.7085561497327)
    assert bc["risparmio_eur_anno"] == pytest.approx(-2241.09639594474)
    assert bc["van"] == pytest.approx(-243261.81422050536)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(92.83939348215655)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_cop_basso_e_alto():
    bc = _variante(cop=2.0)
    assert bc["e_el_mwh_anno"] == pytest.approx(125.37159090909091)
    assert bc["risparmio_eur_anno"] == pytest.approx(2126.277406417117)
    assert bc["van"] == pytest.approx(-197929.9676270808)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(126.95980238424922)
    assert bc["verdetto"] == "NON_CONVIENTE"
    bc2 = _variante(cop=5.0)
    assert bc2["e_el_mwh_anno"] == pytest.approx(50.14863636363636)
    assert bc2["risparmio_eur_anno"] == pytest.approx(10400.802406417115)
    assert bc2["van"] == pytest.approx(-112043.22769870456)
    assert bc2["tir"] == pytest.approx(-4.0176833369154705, abs=1e-4)
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_co2_evitata_negativa_con_fattore_el_alto():
    bc = _variante(f_el_t_per_mwh=2.0)
    assert bc["co2_alt_t_anno"] == pytest.approx(181.99951537433157)
    assert bc["co2_evitata_t_anno"] == pytest.approx(-41.52714460784313)
    assert bc["co2_evitata_t_anno"] < 0.0
    assert bc["van"] == pytest.approx(-144250.75517184564)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_pareggio_negativo():
    bc = _variante(om_fisso_eur_anno=5000000)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(-63479.55305058386)
    assert bc["prezzo_pareggio_eur_mwh"] < 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(-4982702.144468583)
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_variante_pareggio_zero():
    bc = _variante(om_fisso_eur_anno=25917.152406417117)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(0.0, abs=1e-6)
    assert bc["risparmio_eur_anno"] == pytest.approx(-8619.296875)


def test_variante_wacc_zero():
    bc = _variante(wacc_pct=0)
    assert bc["crf"] == pytest.approx(1.0 / 15.0)
    assert bc["quota_capex_eur_anno"] == pytest.approx(14666.666666666666)
    assert bc["van"] == pytest.approx(-110532.16702874325)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex_eur=0)
    assert bc["capex_eur"] == 0
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(75749.24482815436)
    assert bc["lco_alt_eur_t"] == pytest.approx(21.39141654411765)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_vita_dieci():
    bc = _variante(vita_anni=10)
    assert len(bc["flussi"]) == 11
    assert bc["crf"] == pytest.approx(0.12950457496545661)
    assert bc["van"] == pytest.approx(-163647.89403491188)
    assert bc["tir"] == pytest.approx(-16.270365210763487, abs=1e-4)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_input_nulli_calcolabile_non_degenere():
    bc = _variante(prezzo_el_eur_mwh=0.0, prezzo_gas_eur_mwh=0,
                   om_fisso_eur_anno=0)
    assert bc["valid"] is True
    assert bc["c_base_eur_anno"] == 0.0
    assert bc["c_alt_eur_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == 0.0
    assert bc["van"] == -220000.0
    assert bc["verdetto"] == "NON_CONVIENTE"


# ---------------------------------------------------------------- degenere
def test_degenere_legname_zero():
    bc = _variante(m_verde_t_anno=0)
    assert bc["valid"] is False
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"] == []
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["lco_base_eur_t"] is None
    assert bc["lco_alt_eur_t"] is None
    assert bc["errore"]


def test_degenere_umidita_delta_cop_vita():
    for kw in ({"u_i_pct": 12},
               {"u_i_pct": 5},
               {"u_f_pct": 100},
               {"t_ingresso_C": 70, "t_ess_C": 70},
               {"t_ingresso_C": 70, "t_ess_C": 20},
               {"cop": 0}, {"cop": -1},
               {"m_verde_t_anno": 0},
               {"m_verde_t_anno": -1},
               {"vita_anni": 0}, {"vita_anni": 2.5}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_eta_wacc_tolleranza_quote_prezzi_negativi():
    for kw in ({"eta_essiccatore": 0}, {"eta_essiccatore": 1.01},
               {"wacc_pct": -1}, {"wacc_pct": 60},
               {"tolleranza_pct": -1}, {"tolleranza_pct": 101},
               {"quota_recupero_pct": -1}, {"quota_recupero_pct": 101},
               {"quota_pdc_pct": -1}, {"quota_pdc_pct": 101},
               {"prezzo_gas_eur_mwh": -1},
               {"prezzo_el_eur_mwh": -1},
               {"om_fisso_eur_anno": -100},
               {"capex_eur": -1},
               {"u_i_pct": 0}, {"u_i_pct": 100},
               {"u_f_pct": -1},
               {"t_ingresso_C": -1}, {"t_ingresso_C": 100},
               {"t_ess_C": 0}, {"t_ess_C": 100.1}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_stringa_nan_inf():
    for kw in ({"m_verde_t_anno": "3000"},
               {"m_verde_t_anno": float("nan")},
               {"prezzo_el_eur_mwh": float("inf")},
               {"capex_eur": True}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_neutro_campi():
    bc = _variante(m_verde_t_anno=0)
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
    assert mh762_prezzo_pareggio(31606.2834224599, 126.42513368983961,
                                 45, 10000, 0.0) is None
    assert mh762_prezzo_pareggio(31606.2834224599, 126.42513368983961,
                                 45, 10000, None) is None
    assert mh762_lco_base(31606.2834224599, 0) is None
    assert mh762_e_el(250.74318181818182, 0) is None
    bc = _variante(quota_pdc_pct=0)
    assert bc["prezzo_pareggio_eur_mwh"] is None


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = demo_calcoli()
    testo = mh762_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert "q_lordo_mwh_anno;597.0075757575759" in testo
    assert "q_netto_mwh_anno;358.2045454545455" in testo
    assert "verdetto;NON_CONVIENTE" in testo
    assert "prezzo_pareggio_eur_mwh" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = demo_calcoli()
    testo = mh762_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"quota_capex_eur_anno;{bc['quota_capex_eur_anno']}" in testo
    assert f"q_lordo_mwh_anno;{bc['q_lordo_mwh_anno']}" in testo


def test_csv_degenere_solo_zeri():
    bc = _variante(m_verde_t_anno=0)
    testo = mh762_csv(bc, _demo_kwargs())
    assert "van_eur;0.0" in testo
    assert "q_lordo_mwh_anno;0.0" in testo
    assert "verdetto;NON_CALCOLABILE" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = demo_calcoli()
    testo = mh762_csv(bc, _demo_kwargs())
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
    assert basso - base == pytest.approx(783.5724431818181)
    assert base - alto == pytest.approx(783.5724431818181)


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
    assert set(mh762_demo().keys()) == {
        "m_verde_t_anno", "u_i_pct",
        "u_f_pct", "t_ingresso_C", "t_ess_C",
        "eta_essiccatore", "quota_recupero_pct",
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
    return ["mh" + "76" + "1", "st" + "76" + "1",
            "tab" + "76" + "1", "w" + "76" + "2_",
            "mh" + "76" + "0", "st" + "76" + "0",
            "tab" + "76" + "0", "w" + "76" + "1_"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w763_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w763_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab762:")


def test_registry_chain_tail_and_count():
    """Registry della nuova tab: il frammento UI apre la tab
    numero 762 (la coda della catena termina con la nuova tab
    e il conteggio atteso delle tab e' 762)."""
    src = _leggi("w763_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 762
    assert src.count("with tab762:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w763_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w763_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st762_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert "key=f" not in src and 'key = f' not in src
    assert "st.stop()" in src
    # guard degenere prima di KPI / grafico / tabella / CSV
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w763_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def762[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w763_ui.py")
        usate = set(re.findall(r'_def762\["([^"]+)"\]', src))
        assert usate
        assert usate <= set(mh762_demo().keys())


def test_ui_chiavi_demo_coerenti():
    """Ogni _def762[...] letto dalla UI esiste nel dict demo:
    sweep anti-KeyError a render (lezione dello sweep chiavi demo vs UI)."""
    src = _leggi("w763_ui.py")
    usate = set(re.findall(r'_def762\["([^"]+)"\]', src))
    assert usate
    assert usate <= set(mh762_demo().keys())


def test_ui_riferisce_solo_helper_nuovi():
    src = _leggi("w763_ui.py")
    usati = set(re.findall(r'\b(mh\d+_\w+)\b', src))
    assert usati
    assert all(u.startswith("mh762_") for u in usati)


@pytest.mark.parametrize("wacc,vita,atteso", [
    (5.0, 15, 0.09634228760924432),
    (0, 15, 1.0 / 15.0),
    (10.0, 10, 0.16274539488251152),
    (5.0, 1, 1.05),
    (50.0, 5, 0.5758293838862559),
])
def test_crf_parametrizzato(wacc, vita, atteso):
    assert mh762_crf(wacc, vita) == pytest.approx(atteso)


@pytest.mark.parametrize("campo,valore", [
    ("m_verde_t_anno", 0), ("m_verde_t_anno", -3),
    ("u_i_pct", 0), ("u_i_pct", 100),
    ("u_f_pct", -1), ("u_f_pct", 100),
    ("t_ingresso_C", -1), ("t_ingresso_C", 100),
    ("t_ess_C", 0), ("t_ess_C", 100.1),
    ("eta_essiccatore", 0), ("eta_essiccatore", 1.01),
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
    assert mh762_valida(**d)["valido"] is False


def test_df_tabella_valori_demo_selezionati():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Legname verde (t/anno)"] == 2000.0
    assert mappa["Calore lordo (MWh/anno)"] == pytest.approx(597.0075757575759)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(7297.855531417117)
    assert mappa["Verdetto"] == "NON_CONVIENTE"


def test_lco_alt_maggiore_di_lco_base_demo():
    bc = demo_calcoli()
    assert bc["lco_alt_eur_t"] > bc["lco_base_eur_t"]
    assert bc["lco_alt_eur_t"] - bc["lco_base_eur_t"] == pytest.approx(
        12.229754013502642)
