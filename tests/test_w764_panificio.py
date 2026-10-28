"""Test tab764 "Panificio:
forno elettrico con recupero fumi
batte il forno a gas?"

Nuova tab tab764 (cottura pane,
file di lavoro w765).
Business case deterministico
della cottura del pane in forno in
un panificio: l'impasto va cotto
dalla temperatura dell'impasto
alla temperatura di cottura,
perdendo acqua per evaporazione
(perdita di cottura in % sul pane:
l'impasto pesa piu' del pane).
Massa impasto = pane / (1 -
perdita / 100); acqua evaporata =
massa impasto - pane; dT =
T_cottura - T_impasto; Q_evap =
acqua evaporata x 1000 x 2257 /
3600000; Q_risc = massa impasto x
1000 x 2,9 x dT / 3600000 (cp
2,9 kJ/kgK sulla MASSA IMPASTO,
non sul pane); Q_utile = Q_evap +
Q_risc; Q_rec = quota_recupero /
100 x Q_utile; Q_netto = Q_utile -
Q_rec; gas_base = Q_utile /
eta_gas; C_base = gas_base x p_gas;
co2_base = gas_base x f_gas;
E_el = Q_netto / eta_el; C_alt_var
= E_el x p_el; C_alt = C_alt_var +
OM_fisso; co2_alt = E_el x f_el;
risparmio = C_base - C_alt;
CO2 evitata = co2_base - co2_alt,
segno libero (puo' essere negativa),
NON monetizzata; fattori di emissione
in tCO2/MWh, numericamente uguali a
kg/kWh (1 kg/kWh = 1 t/MWh); CRF solo
nel LCO, mai nei flussi; LCO_base =
C_base / pane; LCO_alt = (CAPEX x
CRF + OM_fisso) / pane + C_alt_var /
pane; prezzo elettrico di pareggio =
(C_base - OM_fisso) / E_el, None se
E_el <= 0; flussi [-CAPEX, risparmio
x vita]; VAN, TIR, payback (primo
anno con cumulato STRETTAMENTE > 0).
DIFFERENZA CHIAVE RISPETTO ALLA TAB
PRECEDENTE: in questa tab il
risparmio nullo o negativo NON e'
degenere: resta calcolabile e porta
a VAN negativa (NON_CONVIENTE o
MARGINALE). Distinta dal pastificio
(li' si essicca pasta fresca, con
umidita' iniziale e finale in %
base umida, massa secca, massa
essiccata, cp 1,8 kJ/kgK sulla massa
essiccata, temperatura di
essiccazione, recupero dall'aria
esausta e pompa di calore: qui non
si essicca nulla, si cuoce pane in
forno, senza umidita' della pasta e
senza pompa di calore), dalla
torrefazione del pellet (li' si
torrefa pellet di legno, senza pane,
senza impasto, senza perdita di
cottura del pane, senza forno da
pane), dalla caldaia a elettrodi
generica (li' il calore viene da
elettrodi per un uso generico, senza
cottura del pane, senza impasto,
senza perdita di cottura, senza
recupero dai fumi di un forno da
pane) e dal recupero calore generico
(li' il calore recuperato va a un uso
generico, senza cottura del pane,
senza impasto, senza forno elettrico
da pane).

Demo calcolata eseguendo demo_calcoli()
(e ricontrollata a mano, riga per
riga): pane 2.000 t/anno, perdita di
cottura 12 %, temperatura impasto
20 C, temperatura cottura 230 C,
quota recupero fumi 40 %, rendimento
gas 0,65, rendimento elettrico 0,98,
prezzo gas 45 EUR/MWh, prezzo
elettrico 90 EUR/MWh, O&M fisso
2.000 EUR/anno, CAPEX 45.000 EUR,
fattore gas 0,20 tCO2/MWh e fattore
elettrico 0,25 tCO2/MWh, WACC 5 %,
vita 12 anni, tolleranza 10 % del
CAPEX.

- m_impasto_t_anno = 2272.7272727272725
- m_acqua_t_anno = 272.7272727272725
- delta_t_K = 210.0
- q_evap_mwh_anno = 170.98484848484838
- q_risc_mwh_anno = 384.4696969696969
- q_utile_mwh_anno = 555.4545454545453
- q_rec_mwh_anno = 222.18181818181813
- q_netto_mwh_anno = 333.27272727272714
- gas_base_mwh_anno = 854.5454545454543
- c_base_eur_anno = 38454.54545454544
- e_el_mwh_anno = 340.0742115027828
- c_alt_var_eur_anno = 30606.679035250454
- c_alt_eur_anno = 32606.679035250454
- risparmio_eur_anno = 5847.866419294987
- co2_base_t_anno = 170.90909090909088
- co2_alt_t_anno = 85.0185528756957
- co2_evitata_t_anno = 85.89053803339517
- crf = 0.11282541002081534
- quota_capex_eur_anno = 5077.14345093669
- lco_base_eur_t = 19.22727272727272
- lco_alt_eur_t = 18.841911243093573
- van = 6831.111610550321
- tir = 7.599207634733886
- payback = 8
- prezzo_pareggio_eur_mwh = 107.19585379159847
- verdetto = 'CONVIENTE'

Scomposizione: massa impasto = 2.000 /
(1 - 0,12) = 2.272,73 t/anno; acqua
evaporata = 2.272,73 - 2.000 = 272,73
t/anno; dT = 230 - 20 = 210 K; Q_evap
= 272,73 x 1000 x 2257 / 3.600.000 =
170,98 MWh/anno; Q_risc = 2.272,73 x
1000 x 2,9 x 210 / 3.600.000 = 384,47
MWh/anno (sulla massa impasto, cp
2,9); Q_utile = 170,98 + 384,47 =
555,45 MWh/anno; Q_rec = 0,40 x 555,45
= 222,18 MWh/anno; Q_netto = 555,45 -
222,18 = 333,27 MWh/anno; gas_base =
555,45 / 0,65 = 854,55 MWh/anno;
C_base = 854,55 x 45 = 38.454,55
EUR/anno; E_el = 333,27 / 0,98 =
340,07 MWh/anno; C_alt_var = 340,07 x
90 = 30.606,68 EUR/anno; C_alt =
30.606,68 + 2.000 = 32.606,68 EUR/anno;
risparmio = 38.454,55 - 32.606,68 =
5.847,87 EUR/anno; CO2 base = 854,55 x
0,20 = 170,91 t/anno; CO2 alt = 340,07
x 0,25 = 85,02 t/anno; CO2 evitata =
85,89 t/anno; CRF 0,05 x 1,05^12 /
(1,05^12 - 1) = 0.11282541002081534;
quota CAPEX 45.000 x 0,112825 =
5.077,14 EUR/anno; LCO base 38.454,55 /
2.000 = 19,23 EUR/t; LCO alt
(5.077,14 + 2.000) / 2.000 + 30.606,68
/ 2.000 = 18,84 EUR/t; flussi: anno 0
-45.000, anni 1-12 risparmio 5.847,87
(piatti); VAN -45.000 + 5.847,87 x
8,863252 (annuita' 12 anni al 5 %) =
6.831,11 EUR; TIR 7,60 %; payback 8
anni (il cumulato all'anno 7 e'
-4.064,94 EUR, all'anno 8 e'
1.782,93 EUR, strettamente positivo);
prezzo elettrico di pareggio
(38.454,55 - 2.000) / 340,07 = 107,20
EUR/MWh; verdetto CONVIENTE perche'
VAN > 0.
NOTA: il CRF entra solo nel LCO,
mai nei flussi: il CAPEX compare una
sola volta, all'anno 0.
NOTA 2: in questa tab il risparmio
nullo o negativo NON e' degenere: con
prezzo gas 30 EUR/MWh il caso e'
calcolabile (valid=True, flussi
pieni), NON_CONVIENTE con VAN
-106.779,66 EUR, non NON_CALCOLABILE.
NOTA 3: la CO2 evitata puo' essere
negativa: con fattore elettrico 2,00
tCO2/MWh la CO2 evitata e'
-509,24 t/anno, pur restando il caso
calcolabile e CONVIENTE.
NOTA 4: il prezzo elettrico di
pareggio come valore della funzione
pura puo' essere negativo: con O&M
fisso 5.000.000 il pareggio e'
-14.589,60 EUR/MWh, perche' il solo
O&M fisso supera gia' il costo
baseline (ma il caso resta
calcolabile in questa tab, con VAN
negativa, a differenza della tab
precedente).
NOTA 5: il calore netto nullo (quota
recupero 100 %) NON e' degenere:
il risparmio e' 36.454,55 EUR/anno
(38.454,55 - 2.000 di solo O&M fisso)
e la VAN 278.105,81 EUR, e il
pareggio non e' definito.
NOTA 6: il payback usa il cumulato
STRETTAMENTE positivo: con CAPEX
nullo e risparmio positivo il payback
e' 1, non 0 (all'anno 0 il cumulato
e' zero, non positivo); con flussi
[-100, 50, 50] il payback e' None
(il cumulato all'anno 2 e' zero, non
positivo).
NOTA 7: Q_risc usa la massa impasto
(cp 2,9 kJ/kgK), non il pane: con la
demo Q_risc = 384,47 MWh/anno,
mentre sul pane sarebbe 338,33
MWh/anno.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w765_helpers import (
    demo_calcoli,
    mh764_c_alt,
    mh764_c_alt_var,
    mh764_c_base,
    mh764_calcola,
    mh764_co2_alt,
    mh764_co2_base,
    mh764_co2_evitata,
    mh764_crf,
    mh764_csv,
    mh764_delta_t,
    mh764_demo,
    mh764_e_el,
    mh764_eta,
    mh764_flussi,
    mh764_gas_base,
    mh764_int_pos,
    mh764_lco_alt,
    mh764_lco_base,
    mh764_m_acqua,
    mh764_m_impasto,
    mh764_nneg,
    mh764_num,
    mh764_payback,
    mh764_pct_0_100,
    mh764_pct_wacc,
    mh764_perdita,
    mh764_pos,
    mh764_prezzo_pareggio,
    mh764_q_evap,
    mh764_q_netto,
    mh764_q_rec,
    mh764_q_risc,
    mh764_q_utile,
    mh764_quota_capex,
    mh764_risparmio,
    mh764_temp_cottura,
    mh764_temp_impasto,
    mh764_tir,
    mh764_valida,
    mh764_van,
    mh764_verdetto,
)


def _demo_kwargs():
    return dict(mh764_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh764_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh764_num(3, "x") == 3.0
    assert mh764_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh764_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh764_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh764_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh764_pos(0, "x")
    with pytest.raises(ValueError):
        mh764_pos(-1, "x")
    assert mh764_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh764_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh764_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh764_int_pos(0, "x")


def test_pct_0_100_limiti():
    assert mh764_pct_0_100(0, "x") == 0.0
    assert mh764_pct_0_100(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh764_pct_0_100(100.1, "x")
    with pytest.raises(ValueError):
        mh764_pct_0_100(-1, "x")


def test_pct_wacc_limiti():
    assert mh764_pct_wacc(0, "x") == 0.0
    assert mh764_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh764_pct_wacc(50.1, "x")


def test_eta_limiti():
    assert mh764_eta(1.0, "x") == 1.0
    assert mh764_eta(0.65, "x") == 0.65
    with pytest.raises(ValueError):
        mh764_eta(0, "x")
    with pytest.raises(ValueError):
        mh764_eta(-0.1, "x")
    with pytest.raises(ValueError):
        mh764_eta(1.01, "x")


def test_temp_limiti():
    assert mh764_temp_impasto(0, "x") == 0.0
    assert mh764_temp_impasto(99.0, "x") == 99.0
    with pytest.raises(ValueError):
        mh764_temp_impasto(100, "x")
    with pytest.raises(ValueError):
        mh764_temp_impasto(-1, "x")
    assert mh764_temp_cottura(300, "x") == 300.0
    with pytest.raises(ValueError):
        mh764_temp_cottura(0, "x")
    with pytest.raises(ValueError):
        mh764_temp_cottura(300.1, "x")


def test_perdita_limiti():
    assert mh764_perdita(12, "x") == 12.0
    assert mh764_perdita(99.9, "x") == 99.9
    with pytest.raises(ValueError):
        mh764_perdita(0, "x")
    with pytest.raises(ValueError):
        mh764_perdita(100, "x")
    with pytest.raises(ValueError):
        mh764_perdita(-1, "x")


# ---------------------------------------------------------------- fisica base
def test_masse():
    assert mh764_m_impasto(2000, 12.0) == pytest.approx(2272.7272727272725)
    assert mh764_m_impasto(2000, 50.0) == pytest.approx(4000.0)
    assert mh764_m_acqua(2272.7272727272725, 2000) == pytest.approx(
        272.7272727272725)
    assert mh764_m_acqua(2000, 2000) == 0.0
    with pytest.raises(ValueError):
        mh764_m_impasto(2000, 100)
    with pytest.raises(ValueError):
        mh764_m_impasto(2000, 0)


def test_delta_q_evap_q_risc_q_utile():
    assert mh764_delta_t(20, 230) == pytest.approx(210.0)
    assert mh764_delta_t(230, 20) == pytest.approx(-210.0)
    assert mh764_q_evap(272.7272727272725) == pytest.approx(
        170.98484848484838)
    assert mh764_q_evap(0) == 0.0
    assert mh764_q_risc(2272.7272727272725, 210.0) == pytest.approx(
        384.4696969696969)
    assert mh764_q_risc(2000, 210.0) == pytest.approx(338.3333333333333)
    assert mh764_q_risc(2272.7272727272725, 0) == 0.0
    assert mh764_q_utile(170.98484848484838, 384.4696969696969) == \
        pytest.approx(555.4545454545453)
    with pytest.raises(ValueError):
        mh764_q_evap(-1)
    with pytest.raises(ValueError):
        mh764_q_risc(-1, 210.0)


def test_q_rec_netto():
    assert mh764_q_rec(555.4545454545453, 40.0) == pytest.approx(
        222.18181818181813)
    assert mh764_q_rec(555.4545454545453, 0) == 0.0
    assert mh764_q_rec(555.4545454545453, 100) == pytest.approx(
        555.4545454545453)
    assert mh764_q_netto(555.4545454545453, 222.18181818181813) == \
        pytest.approx(333.27272727272714)
    assert mh764_q_netto(555.4545454545453, 555.4545454545453) == 0.0
    with pytest.raises(ValueError):
        mh764_q_rec(555.4545454545453, 100.1)


def test_gas_base_e_c_base_e_co2_base():
    assert mh764_gas_base(555.4545454545453, 0.65) == pytest.approx(
        854.5454545454543)
    assert mh764_gas_base(555.4545454545453, 1.0) == pytest.approx(
        555.4545454545453)
    assert mh764_c_base(854.5454545454543, 45) == pytest.approx(
        38454.54545454544)
    assert mh764_co2_base(854.5454545454543, 0.20) == pytest.approx(
        170.90909090909088)
    with pytest.raises(ValueError):
        mh764_gas_base(555.4545454545453, 0)


def test_e_el():
    assert mh764_e_el(333.27272727272714, 0.98) == pytest.approx(
        340.0742115027828)
    assert mh764_e_el(333.27272727272714, 0) is None
    assert mh764_e_el(333.27272727272714, -1.0) is None
    assert mh764_e_el(0.0, 0.98) == 0.0


def test_c_alt_var_e_c_alt():
    assert mh764_c_alt_var(340.0742115027828, 90) == pytest.approx(
        30606.679035250454)
    assert mh764_c_alt_var(0.0, 90) == 0.0
    assert mh764_c_alt(30606.679035250454, 2000) == pytest.approx(
        32606.679035250454)
    assert mh764_c_alt(30606.679035250454, 0) == pytest.approx(
        30606.679035250454)
    with pytest.raises(ValueError):
        mh764_c_alt_var(340.0742115027828, -1)


def test_risparmio_segno():
    assert mh764_risparmio(38454.54545454544, 32606.679035250454) == \
        pytest.approx(5847.866419294987)
    assert mh764_risparmio(38454.54545454544, 38454.54545454544) == 0.0
    assert mh764_risparmio(25636.36363636363, 32606.679035250454) == \
        pytest.approx(-6970.315398886825)


def test_co2_alt_e_evitata_segno_libero():
    assert mh764_co2_alt(340.0742115027828, 0.25) == pytest.approx(
        85.0185528756957)
    assert mh764_co2_evitata(170.90909090909088,
                             85.0185528756957) == pytest.approx(
        85.89053803339517)
    assert mh764_co2_evitata(170.90909090909088,
                             680.1484230303759) == pytest.approx(
        -509.23933209647475, abs=1e-6)


# ---------------------------------------------------------------- finanza base
def test_crf():
    assert mh764_crf(5.0, 12) == pytest.approx(0.11282541002081534)
    assert mh764_crf(0, 12) == pytest.approx(1.0 / 12.0)
    assert mh764_crf(5.0, 1) == pytest.approx(1.05)
    assert mh764_crf(5.0, 10) == pytest.approx(0.12950457496545661)


def test_quota_capex_e_lco():
    assert mh764_quota_capex(45000, 0.11282541002081534) == pytest.approx(
        5077.14345093669)
    assert mh764_lco_base(38454.54545454544, 2000.0) == \
        pytest.approx(19.22727272727272)
    assert mh764_lco_base(38454.54545454544, 0) is None
    assert mh764_lco_alt(45000, 0.11282541002081534, 2000,
                         30606.679035250454,
                         2000.0) == pytest.approx(
        18.841911243093573)
    assert mh764_lco_alt(45000, 0.11282541002081534, 2000,
                         30606.679035250454, 0) is None
    assert mh764_lco_alt(0, 0.11282541002081534, 2000,
                         30606.679035250454,
                         2000.0) == pytest.approx(
        16.303339517625226)


def test_prezzo_pareggio_formula_negativo_e_none():
    assert mh764_prezzo_pareggio(38454.54545454544, 2000,
                                 340.0742115027828) == pytest.approx(
        107.19585379159847)
    assert mh764_prezzo_pareggio(38454.54545454544, 2000, 0.0) is None
    assert mh764_prezzo_pareggio(38454.54545454544, 2000, None) is None


def test_prezzo_pareggio_negativo_solo_funzione_pura():
    """Il pareggio negativo esiste come valore della
    funzione pura: con O&M fisso 5.000.000 il numeratore e'
    negativo; in questa tab quel caso resta comunque
    calcolabile (VAN negativa), a differenza della tab
    precedente."""
    bc = demo_calcoli()
    assert mh764_prezzo_pareggio(bc["c_base_eur_anno"], 5000000,
                                 bc["e_el_mwh_anno"]) == pytest.approx(
        -14589.596290234591)
    assert bc["prezzo_pareggio_eur_mwh"] > 0.0


def test_flussi_lunghezza_e_primo():
    fl = mh764_flussi(45000, 5847.866419294987, 12)
    assert len(fl) == 13
    assert fl[0] == -45000
    assert all(f == 5847.866419294987 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = demo_calcoli()
    assert bc["van"] == pytest.approx(6831.111610550321)
    assert mh764_van([-45000] + [5847.866419294987] * 12,
                     0) == pytest.approx(25174.397031539847)
    assert mh764_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = demo_calcoli()
    assert bc["tir"] == pytest.approx(7.599207634733886)
    assert mh764_tir([-45000] + [5847.866419294987] * 12) == pytest.approx(
        0.07599207634733886)
    tir = mh764_tir([-45000] + [5847.866419294987] * 12)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-45000] + [5847.866419294987] * 12))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_stretto():
    """Payback STRETTAMENTE positivo: il cumulato nullo
    non basta."""
    assert mh764_payback([-45000] + [5847.866419294987] * 12) == 8
    assert mh764_payback([-45000] + [-1000.0] * 12) is None
    assert mh764_payback([0] + [5847.866419294987] * 12) == 1
    assert mh764_payback([-100] + [50] * 2) is None
    assert mh764_payback([-100] + [50] * 3) == 3


def test_verdetto():
    assert mh764_verdetto(100.0, 45000, 10.0) == "CONVIENTE"
    assert mh764_verdetto(-4000.0, 45000, 10.0) == "MARGINALE"
    assert mh764_verdetto(-4500.0, 45000, 10.0) == "MARGINALE"
    assert mh764_verdetto(-4500.01, 45000, 10.0) == "NON_CONVIENTE"
    assert mh764_verdetto(float("nan"), 45000, 10.0) == "NON_CALCOLABILE"
    assert mh764_verdetto(0.0, 0, 10.0) == "MARGINALE"


def test_valida_demo_ok():
    v = mh764_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("m_pane_t_anno", "2000"),
                       ("m_pane_t_anno", float("nan")),
                       ("m_pane_t_anno", float("inf")),
                       ("m_pane_t_anno", True),
                       ("prezzo_el_eur_mwh", None)):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh764_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("m_pane_t_anno", 0),
                          ("m_pane_t_anno", -1),
                          ("perdita_pct", 0),
                          ("perdita_pct", 100),
                          ("perdita_pct", -1),
                          ("t_impasto_C", -1),
                          ("t_impasto_C", 100),
                          ("t_cottura_C", 0),
                          ("t_cottura_C", 300.1),
                          ("eta_gas", 0),
                          ("eta_gas", 1.01),
                          ("eta_el", 0),
                          ("eta_el", 1.01),
                          ("quota_recupero_pct", -1),
                          ("quota_recupero_pct", 100.1),
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
        assert mh764_valida(**d)["valido"] is False


def test_valida_rifiuta_delta_non_valido():
    for ti, tc in ((230, 230), (230, 20), (20, 20)):
        d = _demo_kwargs()
        d["t_impasto_C"] = ti
        d["t_cottura_C"] = tc
        assert mh764_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"quota_recupero_pct": 0,
              "prezzo_gas_eur_mwh": 0,
              "prezzo_el_eur_mwh": 0, "om_fisso_eur_anno": 0,
              "capex_eur": 0, "f_gas_t_per_mwh": 0,
              "f_el_t_per_mwh": 0, "wacc_pct": 0,
              "tolleranza_pct": 0, "eta_gas": 1.0,
              "eta_el": 1.0,
              "t_impasto_C": 0, "t_cottura_C": 300,
              "perdita_pct": 99})
    assert mh764_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["quota_recupero_pct"] = 100
    assert mh764_valida(**d)["valido"] is True


def test_valida_non_controlla_risparmio_calcola_neppure():
    """La validazione input NON controlla il risparmio
    (e' un esito, non un range) e in questa tab
    nemmeno mh764_calcola lo controlla: con gas 30 il
    caso resta CALCOLABILE (differenza rispetto alla
    tab precedente)."""
    d = _demo_kwargs()
    d["prezzo_gas_eur_mwh"] = 30
    assert mh764_valida(**d)["valido"] is True
    bc = _variante(prezzo_gas_eur_mwh=30)
    assert bc["valid"] is True
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["flussi"]
    assert bc["tir"] is None
    assert bc["payback"] is None


def test_demo_dict():
    d = mh764_demo()
    assert d["m_pane_t_anno"] == 2000
    assert d["perdita_pct"] == 12.0
    assert d["t_impasto_C"] == 20
    assert d["t_cottura_C"] == 230
    assert d["eta_gas"] == 0.65
    assert d["eta_el"] == 0.98
    assert d["quota_recupero_pct"] == 40.0
    assert d["prezzo_gas_eur_mwh"] == 45
    assert d["prezzo_el_eur_mwh"] == 90
    assert d["om_fisso_eur_anno"] == 2000
    assert d["capex_eur"] == 45000
    assert d["f_gas_t_per_mwh"] == 0.20
    assert d["f_el_t_per_mwh"] == 0.25
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 12
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    """Ogni _DEMO del test contro demo_calcoli():
    scarto relativo < 1e-9 (zero atteso:
    confronto assoluto)."""
    bc = demo_calcoli()
    attesi = {
        "m_impasto_t_anno": 2272.7272727272725,
        "m_acqua_t_anno": 272.7272727272725,
        "delta_t_K": 210.0,
        "q_evap_mwh_anno": 170.98484848484838,
        "q_risc_mwh_anno": 384.4696969696969,
        "q_utile_mwh_anno": 555.4545454545453,
        "q_rec_mwh_anno": 222.18181818181813,
        "q_netto_mwh_anno": 333.27272727272714,
        "gas_base_mwh_anno": 854.5454545454543,
        "c_base_eur_anno": 38454.54545454544,
        "e_el_mwh_anno": 340.0742115027828,
        "c_alt_var_eur_anno": 30606.679035250454,
        "c_alt_eur_anno": 32606.679035250454,
        "risparmio_eur_anno": 5847.866419294987,
        "co2_base_t_anno": 170.90909090909088,
        "co2_alt_t_anno": 85.0185528756957,
        "co2_evitata_t_anno": 85.89053803339517,
        "crf": 0.11282541002081534,
        "quota_capex_eur_anno": 5077.14345093669,
        "lco_base_eur_t": 19.22727272727272,
        "lco_alt_eur_t": 18.841911243093573,
        "van": 6831.111610550321,
        "tir": 7.599207634733886,
        "prezzo_pareggio_eur_mwh": 107.19585379159847,
    }
    for chiave, atteso in attesi.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert abs(got - atteso) / abs(atteso) < 1e-9, chiave
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_demo_calcoli_fisica():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["m_impasto_t_anno"] == pytest.approx(2272.7272727272725)
    assert bc["m_acqua_t_anno"] == pytest.approx(272.7272727272725)
    assert bc["q_evap_mwh_anno"] == pytest.approx(170.98484848484838)
    assert bc["q_risc_mwh_anno"] == pytest.approx(384.4696969696969)
    assert bc["q_utile_mwh_anno"] == pytest.approx(555.4545454545453)
    assert bc["q_rec_mwh_anno"] == pytest.approx(222.18181818181813)
    assert bc["q_netto_mwh_anno"] == pytest.approx(333.27272727272714)
    assert bc["gas_base_mwh_anno"] == pytest.approx(854.5454545454543)
    assert bc["co2_evitata_t_anno"] == pytest.approx(85.89053803339517)


def test_demo_calcoli_economia():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(38454.54545454544)
    assert bc["c_alt_var_eur_anno"] == pytest.approx(30606.679035250454)
    assert bc["c_alt_eur_anno"] == pytest.approx(32606.679035250454)
    assert bc["risparmio_eur_anno"] == pytest.approx(5847.866419294987)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(107.19585379159847)


def test_demo_calcoli_finanza():
    bc = demo_calcoli()
    assert bc["crf"] == pytest.approx(0.11282541002081534)
    assert bc["quota_capex_eur_anno"] == pytest.approx(5077.14345093669)
    assert bc["lco_base_eur_t"] == pytest.approx(19.22727272727272)
    assert bc["lco_alt_eur_t"] == pytest.approx(18.841911243093573)
    assert bc["van"] == pytest.approx(6831.111610550321)
    assert bc["tir"] == pytest.approx(7.599207634733886)
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"


def test_demo_flussi_e_cumulato():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -45000
    assert len(bc["flussi"]) == 13
    assert all(f == 5847.866419294987 for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -45000
    assert righe.iloc[5]["Cumulato (EUR)"] == pytest.approx(-15760.67)
    assert righe.iloc[7]["Cumulato (EUR)"] == pytest.approx(-4064.935064935089)
    assert righe.iloc[8]["Cumulato (EUR)"] == pytest.approx(1782.93)
    assert righe.iloc[12]["Cumulato (EUR)"] == pytest.approx(25174.40)
    assert righe.iloc[12]["Flusso (EUR/anno)"] == 5847.866419294987


def test_demo_tabella_righe():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Calore utile (MWh/anno)"] == pytest.approx(555.4545454545453)
    assert mappa["Calore recuperato (MWh/anno)"] == pytest.approx(222.18181818181813)
    assert mappa["Calore netto (MWh/anno)"] == pytest.approx(333.27272727272714)
    assert mappa["Massa impasto (t/anno)"] == pytest.approx(2272.7272727272725)
    assert mappa["Acqua evaporata (t/anno)"] == pytest.approx(272.7272727272725)
    assert mappa["Salto termico (K)"] == pytest.approx(210.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(32606.679035250454)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(5847.866419294987)
    assert mappa["Payback (anni)"] == 8
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Prezzo elettrico di pareggio (EUR/MWh)"] == pytest.approx(
        107.19585379159847)


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
        bc["m_pane_t_anno"] + bc["c_alt_var_eur_anno"] / \
        bc["m_pane_t_anno"] == pytest.approx(bc["lco_alt_eur_t"])
    assert bc["c_base_eur_anno"] - bc["om_fisso_eur_anno"] == \
        pytest.approx(bc["prezzo_pareggio_eur_mwh"] *
                      bc["e_el_mwh_anno"])
    assert bc["q_utile_mwh_anno"] - bc["q_rec_mwh_anno"] == \
        pytest.approx(bc["q_netto_mwh_anno"])
    assert bc["q_evap_mwh_anno"] + bc["q_risc_mwh_anno"] == \
        pytest.approx(bc["q_utile_mwh_anno"])
    assert bc["m_pane_t_anno"] / (1.0 - bc["perdita_pct"] / 100.0) == \
        pytest.approx(bc["m_impasto_t_anno"])
    assert bc["m_impasto_t_anno"] - bc["m_pane_t_anno"] == \
        pytest.approx(bc["m_acqua_t_anno"])
    assert bc["m_acqua_t_anno"] * 1000.0 * 2257.0 / \
        3600000.0 == pytest.approx(bc["q_evap_mwh_anno"])
    assert bc["m_impasto_t_anno"] * 1000.0 * 2.9 * \
        bc["delta_t_K"] / 3600000.0 == pytest.approx(
        bc["q_risc_mwh_anno"])


def test_demo_crf_solo_nel_lco_non_nei_flussi():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -bc["capex_eur"]
    assert all(f == bc["risparmio_eur_anno"] for f in bc["flussi"][1:])
    assert bc["crf"] not in bc["flussi"]
    assert bc["quota_capex_eur_anno"] not in bc["flussi"]
    van_da_flussi = mh764_van(bc["flussi"], bc["wacc_pct"])
    assert van_da_flussi == pytest.approx(bc["van"])
    assert bc["lco_alt_eur_t"] == pytest.approx(
        (bc["capex_eur"] * bc["crf"] + bc["om_fisso_eur_anno"]) /
        bc["m_pane_t_anno"] + bc["c_alt_var_eur_anno"] /
        bc["m_pane_t_anno"])


def test_demo_contro_riconteggio_indipendente():
    mp, pe_, ti, tc = 2000, 12.0, 20, 230
    eta_g, eta_e, qr = 0.65, 0.98, 40.0
    pg, pel, om, cx = 45, 90, 2000, 45000
    fg, fe, wacc, vita = 0.20, 0.25, 5.0, 12
    mi = mp / (1 - pe_ / 100)
    ma = mi - mp
    qe = ma * 1000 * 2257 / 3600000.0
    qri = mi * 1000 * 2.9 * (tc - ti) / 3600000.0
    qu = qe + qri
    qrec = qr / 100 * qu
    qn = qu - qrec
    gb = qu / eta_g
    cb = gb * pg
    ee = qn / eta_e
    cav = ee * pel
    ca = cav + om
    risp = cb - ca
    co2b = gb * fg
    co2a = ee * fe
    r = wacc / 100.0
    crf = r * (1 + r) ** vita / ((1 + r) ** vita - 1)
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    bc = demo_calcoli()
    assert bc["m_impasto_t_anno"] == pytest.approx(mi)
    assert bc["m_acqua_t_anno"] == pytest.approx(ma)
    assert bc["q_evap_mwh_anno"] == pytest.approx(qe)
    assert bc["q_risc_mwh_anno"] == pytest.approx(qri)
    assert bc["q_utile_mwh_anno"] == pytest.approx(qu)
    assert bc["q_rec_mwh_anno"] == pytest.approx(qrec)
    assert bc["q_netto_mwh_anno"] == pytest.approx(qn)
    assert bc["gas_base_mwh_anno"] == pytest.approx(gb)
    assert bc["c_base_eur_anno"] == pytest.approx(cb)
    assert bc["e_el_mwh_anno"] == pytest.approx(ee)
    assert bc["c_alt_var_eur_anno"] == pytest.approx(cav)
    assert bc["c_alt_eur_anno"] == pytest.approx(ca)
    assert bc["risparmio_eur_anno"] == pytest.approx(risp)
    assert bc["co2_base_t_anno"] == pytest.approx(co2b)
    assert bc["co2_alt_t_anno"] == pytest.approx(co2a)
    assert bc["crf"] == pytest.approx(crf)
    assert bc["van"] == pytest.approx(van)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(
        (cb - om) / ee)


# ---------------------------------------------------------------- varianti
def test_demo_conviente():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] > 0.0
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_gas_trenta_calcolabile_non_conviente():
    """Sensibilita' richiesta dal brief: gas 30 EUR/MWh.
    In questa tab il risparmio negativo e' CALCOLABILE
    (differenza rispetto alla tab precedente)."""
    bc = _variante(prezzo_gas_eur_mwh=30)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(-6970.315398886825)
    assert bc["van"] == pytest.approx(-106779.65936574797)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(69.50354609929079)
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["flussi"]


def test_variante_gas_marginale():
    bc = _variante(prezzo_gas_eur_mwh=43.8)
    assert bc["risparmio_eur_anno"] == pytest.approx(4822.411873840443)
    assert bc["van"] == pytest.approx(-2257.7500675535284)
    assert bc["van"] < 0.0
    assert abs(bc["van"]) <= 0.10 * 45000
    assert bc["tir"] == pytest.approx(4.098931935016989, abs=1e-4)
    assert bc["payback"] == 10
    assert bc["verdetto"] == "MARGINALE"
    assert bc["valid"] is True


def test_variante_prezzo_el_alto_calcolabile_non_conviente():
    bc = _variante(prezzo_el_eur_mwh=130)
    assert bc["risparmio_eur_anno"] == pytest.approx(-7755.102040816324)
    assert bc["van"] == pytest.approx(-113735.42085409276)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(107.19585379159847)
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_variante_prezzo_el_zero_conviente():
    bc = _variante(prezzo_el_eur_mwh=0.0)
    assert bc["c_alt_var_eur_anno"] == 0.0
    assert bc["c_alt_eur_anno"] == 2000.0
    assert bc["risparmio_eur_anno"] == pytest.approx(36454.54545454544)
    assert bc["van"] == pytest.approx(278105.8096559973)
    assert bc["tir"] == pytest.approx(80.94433533619615, abs=1e-4)
    assert bc["payback"] == 2
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_variante_quota_recupero_cento_calcolabile_non_degenere():
    """Sensibilita' richiesta dal brief: recupero 100 %."""
    bc = _variante(quota_recupero_pct=100)
    assert bc["valid"] is True
    assert bc["q_netto_mwh_anno"] == 0.0
    assert bc["e_el_mwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(36454.54545454544)
    assert bc["van"] == pytest.approx(278105.8096559973)
    assert bc["tir"] == pytest.approx(80.94433533619615, abs=1e-4)
    assert bc["payback"] == 2
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_quota_recupero_zero_calcolabile_non_conviente():
    bc = _variante(quota_recupero_pct=0)
    assert bc["valid"] is True
    assert bc["q_netto_mwh_anno"] == pytest.approx(555.4545454545453)
    assert bc["e_el_mwh_anno"] == pytest.approx(566.790352504638)
    assert bc["risparmio_eur_anno"] == pytest.approx(-14556.58627087198)
    assert bc["van"] == pytest.approx(-174018.6870864143)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_co2_evitata_negativa_con_fattore_el_alto():
    bc = _variante(f_el_t_per_mwh=2.0)
    assert bc["co2_alt_t_anno"] == pytest.approx(680.1484230303759)
    assert bc["co2_evitata_t_anno"] == pytest.approx(-509.23933209647475)
    assert bc["co2_evitata_t_anno"] < 0.0
    assert bc["van"] == pytest.approx(6831.111610550321)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero():
    bc = _variante(wacc_pct=0)
    assert bc["crf"] == pytest.approx(1.0 / 12.0)
    assert bc["quota_capex_eur_anno"] == pytest.approx(3750.0)
    assert bc["van"] == pytest.approx(25174.397031539847)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_zero_payback_uno_tir_none():
    """Payback stretto: con CAPEX nullo il payback e' 1,
    non 0 (all'anno 0 il cumulato e' zero)."""
    bc = _variante(capex_eur=0)
    assert bc["capex_eur"] == 0
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 1
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(51831.11161055032)
    assert bc["lco_alt_eur_t"] == pytest.approx(16.303339517625226)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_vita_dieci():
    bc = _variante(vita_anni=10)
    assert len(bc["flussi"]) == 11
    assert bc["crf"] == pytest.approx(0.12950457496545661)
    assert bc["van"] == pytest.approx(155.67439107700875)
    assert bc["tir"] == pytest.approx(5.071176071880185, abs=1e-4)
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_fattori_zero_calcolabile():
    bc = _variante(f_gas_t_per_mwh=0, f_el_t_per_mwh=0)
    assert bc["valid"] is True
    assert bc["co2_base_t_anno"] == 0.0
    assert bc["co2_alt_t_anno"] == 0.0
    assert bc["co2_evitata_t_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(5847.866419294987)


def test_variante_perdita_venti():
    bc = _variante(perdita_pct=20.0)
    assert bc["m_impasto_t_anno"] == pytest.approx(2500.0)
    assert bc["m_acqua_t_anno"] == pytest.approx(500.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(8404.238618524338)
    assert bc["van"] == pytest.approx(29488.881688742098)
    assert bc["payback"] == 6
    assert bc["verdetto"] == "CONVIENTE"


# ---------------------------------------------------------------- degenere
def test_degenere_pane_zero():
    bc = _variante(m_pane_t_anno=0)
    assert bc["valid"] is False
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"] == []
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["lco_base_eur_t"] is None
    assert bc["lco_alt_eur_t"] is None
    assert bc["errore"]


def test_degenere_perdita_delta_eta_vita():
    for kw in ({"perdita_pct": 0},
               {"perdita_pct": 100},
               {"t_impasto_C": 230, "t_cottura_C": 230},
               {"t_impasto_C": 230, "t_cottura_C": 20},
               {"eta_gas": 0}, {"eta_el": 0},
               {"m_pane_t_anno": 0},
               {"m_pane_t_anno": -1},
               {"vita_anni": 0}, {"vita_anni": 2.5}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_eta_wacc_tolleranza_quote_prezzi_negativi():
    for kw in ({"eta_gas": 0}, {"eta_gas": 1.01},
               {"eta_el": 0}, {"eta_el": 1.01},
               {"wacc_pct": -1}, {"wacc_pct": 60},
               {"tolleranza_pct": -1}, {"tolleranza_pct": 101},
               {"quota_recupero_pct": -1}, {"quota_recupero_pct": 101},
               {"prezzo_gas_eur_mwh": -1},
               {"prezzo_el_eur_mwh": -1},
               {"om_fisso_eur_anno": -100},
               {"capex_eur": -1},
               {"perdita_pct": 0}, {"perdita_pct": 100},
               {"t_impasto_C": -1}, {"t_impasto_C": 100},
               {"t_cottura_C": 0}, {"t_cottura_C": 300.1}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_stringa_nan_inf():
    for kw in ({"m_pane_t_anno": "2000"},
               {"m_pane_t_anno": float("nan")},
               {"prezzo_el_eur_mwh": float("inf")},
               {"capex_eur": True}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_risparmio_negativo_non_degenere():
    """Differenza chiave: risparmio negativo resta
    calcolabile, con flussi pieni e VAN negativa."""
    for kw in ({"prezzo_gas_eur_mwh": 30},
               {"prezzo_gas_eur_mwh": 0},
               {"quota_recupero_pct": 0},
               {"prezzo_el_eur_mwh": 400}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] < 0.0
        assert bc["verdetto"] in ("NON_CONVIENTE", "MARGINALE")
        assert bc["flussi"]


def test_degenere_neutro_campi():
    bc = _variante(m_pane_t_anno=0)
    assert bc["q_utile_mwh_anno"] == 0.0
    assert bc["gas_base_mwh_anno"] == 0.0
    assert bc["c_base_eur_anno"] == 0.0
    assert bc["c_alt_eur_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == 0.0
    assert bc["van"] == 0.0
    assert list(bc["df_flussi"].columns) == [
        "Anno", "Flusso (EUR/anno)", "Cumulato (EUR)"]
    assert list(bc["df_tabella"].columns) == ["Voce", "Valore"]


def test_pareggio_none_quando_e_el_zero():
    assert mh764_prezzo_pareggio(38454.54545454544, 2000, 0.0) is None
    assert mh764_prezzo_pareggio(38454.54545454544, 2000, None) is None
    assert mh764_lco_base(38454.54545454544, 0) is None
    assert mh764_e_el(333.27272727272714, 0) is None
    bc = _variante(quota_recupero_pct=100)
    assert bc["prezzo_pareggio_eur_mwh"] is None


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = demo_calcoli()
    testo = mh764_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert "q_utile_mwh_anno;555.4545454545453" in testo
    assert "q_netto_mwh_anno;333.27272727272714" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "prezzo_pareggio_eur_mwh" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = demo_calcoli()
    testo = mh764_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"quota_capex_eur_anno;{bc['quota_capex_eur_anno']}" in testo
    assert f"q_utile_mwh_anno;{bc['q_utile_mwh_anno']}" in testo


def test_csv_degenere_solo_zeri():
    bc = _variante(m_pane_t_anno=0)
    testo = mh764_csv(bc, _demo_kwargs())
    assert "van_eur;0.0" in testo
    assert "q_utile_mwh_anno;0.0" in testo
    assert "verdetto;NON_CALCOLABILE" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = demo_calcoli()
    testo = mh764_csv(bc, _demo_kwargs())
    for chiave in _demo_kwargs():
        assert f"{chiave};" in testo


def test_calcola_non_sollevela_per_input_numerici():
    bc = _variante(f_gas_t_per_mwh=0, f_el_t_per_mwh=0)
    assert bc["valid"] is True
    assert bc["co2_base_t_anno"] == 0.0
    assert bc["co2_alt_t_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(5847.866419294987)


def test_monotonia_prezzo_el():
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(prezzo_el_eur_mwh=100)["risparmio_eur_anno"]
    basso = _variante(prezzo_el_eur_mwh=80)["risparmio_eur_anno"]
    assert basso > base > alto
    assert basso - base == pytest.approx(3400.742115027828)
    assert base - alto == pytest.approx(3400.742115027828)


def test_monotonia_quota_recupero():
    base = demo_calcoli()["risparmio_eur_anno"]
    alta = _variante(quota_recupero_pct=50)["risparmio_eur_anno"]
    bassa = _variante(quota_recupero_pct=30)["risparmio_eur_anno"]
    assert alta > base > bassa


def test_demo_deterministica_due_chiamate():
    a = demo_calcoli()
    b = demo_calcoli()
    assert a["van"] == b["van"]
    assert a["flussi"] == b["flussi"]
    assert a["tir"] == b["tir"]


def test_demo_chiavi_attese():
    assert set(mh764_demo().keys()) == {
        "m_pane_t_anno", "perdita_pct",
        "t_impasto_C", "t_cottura_C",
        "eta_gas", "eta_el",
        "quota_recupero_pct",
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
    return ["mh" + "76" + "3", "st" + "76" + "3",
            "tab" + "76" + "3", "w" + "76" + "4_",
            "mh" + "76" + "2", "st" + "76" + "2",
            "tab" + "76" + "2", "w" + "76" + "3_"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w765_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w765_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab764:")


def test_registry_chain_tail_and_count():
    """Registry della nuova tab: il frammento UI apre la tab
    numero 764 (la coda della catena termina con la nuova tab
    e il conteggio atteso delle tab e' 764)."""
    src = _leggi("w765_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 764
    assert src.count("with tab764:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w765_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w765_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st764_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert "key=f" not in src and 'key = f' not in src
    assert "st.stop()" in src
    # guard degenere prima di KPI / grafico / tabella / CSV
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w765_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def764[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w765_ui.py")
        usate = set(re.findall(r'_def764\["([^"]+)"\]', src))
        assert usate
        assert usate <= set(mh764_demo().keys())


def test_ui_chiavi_demo_coerenti():
    """Ogni _def764[...] letto dalla UI esiste nel dict demo:
    sweep anti-KeyError a render (lezione dello sweep chiavi demo vs UI)."""
    src = _leggi("w765_ui.py")
    usate = set(re.findall(r'_def764\["([^"]+)"\]', src))
    assert usate
    assert usate <= set(mh764_demo().keys())


def test_ui_riferisce_solo_helper_nuovi():
    src = _leggi("w765_ui.py")
    usati = set(re.findall(r'\b(mh\d+_\w+)\b', src))
    assert usati
    assert all(u.startswith("mh764_") for u in usati)


@pytest.mark.parametrize("wacc,vita,atteso", [
    (5.0, 12, 0.11282541002081534),
    (0, 12, 1.0 / 12.0),
    (10.0, 10, 0.16274539488251152),
    (5.0, 1, 1.05),
    (50.0, 5, 0.5758293838862559),
])
def test_crf_parametrizzato(wacc, vita, atteso):
    assert mh764_crf(wacc, vita) == pytest.approx(atteso)


@pytest.mark.parametrize("campo,valore", [
    ("m_pane_t_anno", 0), ("m_pane_t_anno", -3),
    ("perdita_pct", 0), ("perdita_pct", 100),
    ("t_impasto_C", -1), ("t_impasto_C", 100),
    ("t_cottura_C", 0), ("t_cottura_C", 300.1),
    ("eta_gas", 0), ("eta_gas", 1.01),
    ("eta_el", 0), ("eta_el", 1.01),
    ("quota_recupero_pct", -1), ("quota_recupero_pct", 100.1),
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
    assert mh764_valida(**d)["valido"] is False


def test_df_tabella_valori_demo_selezionati():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Pane (t/anno)"] == 2000.0
    assert mappa["Calore utile (MWh/anno)"] == pytest.approx(555.4545454545453)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(5847.866419294987)
    assert mappa["Verdetto"] == "CONVIENTE"


def test_lco_alt_minore_di_lco_base_demo():
    bc = demo_calcoli()
    assert bc["lco_alt_eur_t"] < bc["lco_base_eur_t"]
    assert bc["lco_base_eur_t"] - bc["lco_alt_eur_t"] == pytest.approx(
        0.385361484179147)
