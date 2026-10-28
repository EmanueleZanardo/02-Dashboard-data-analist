"""Test tab765 "Fonderia:
fondere la ghisa a induzione con
preriscaldo della carica batte il
cubilotto a coke?"

Nuova tab tab765 (fusione ghisa,
file di lavoro w766).
Business case deterministico
della fusione di ghisa in
fonderia: la carica va portata
dalla temperatura di carica alla
temperatura di fusione e poi
fusa. dT = T_fusione - T_carica;
Q_risc = m_ghisa x 1000 x 0,70 x
dT / 3600000 (cp 0,70 kJ/kgK
sulla MASSA GHISA, non su altro);
Q_fus = m_ghisa x 1000 x 270 /
3600000 (latente di fusione 270
kJ/kg); Q_lordo = Q_risc + Q_fus;
Q_rec = quota_recupero / 100 x
Q_lordo (preriscaldo della
carica); Q_netto = Q_lordo -
Q_rec; coke_base = Q_lordo /
eta_coke; C_base = coke_base x
p_coke; co2_base = coke_base x
f_coke; E_el = Q_netto /
eta_induzione; C_alt_var = E_el x
p_el; C_alt = C_alt_var + OM_fisso;
co2_alt = E_el x f_el; risparmio =
C_base - C_alt; CO2 evitata =
co2_base - co2_alt, segno libero
(puo' essere negativa), NON
monetizzata; fattori di emissione
in tCO2/MWh, numericamente uguali
a kg/kWh (1 kg/kWh = 1 t/MWh);
CRF solo nel LCO, mai nei flussi;
LCO_base = C_base / m_ghisa;
LCO_alt = (CAPEX x CRF + OM_fisso)
/ m_ghisa + C_alt_var / m_ghisa;
prezzo elettrico di pareggio =
(C_base - OM_fisso) / E_el, None se
E_el <= 0; flussi [-CAPEX, risparmio
x vita]; VAN, TIR, payback (primo
anno con cumulato STRETTAMENTE > 0).
In questa tab il risparmio nullo o
negativo NON e' degenere: resta
calcolabile e porta a VAN negativa
(NON_CONVIENTE o MARGINALE).
Distinta dal forno ad arco elettrico
EAF (li' si fonde rottame d'acciaio
ad arco, senza ghisa, senza
cubilotto a coke, senza preriscaldo
della carica da calore recuperato,
senza cp 0,70 e senza latente 270),
dal forno fusorio del vetro (li' si
fonde vetro a 1500 C in continuo,
senza ghisa, senza cubilotto a coke,
senza preriscaldo della carica),
dal forno a induzione generico (li'
il riscaldamento per induzione e'
generico, senza fusione di ghisa,
senza cubilotto a coke, senza
preriscaldo della carica), dalla
caldaia a elettrodi generica (li' il
calore elettrico e' generico, senza
fusione di ghisa, senza cubilotto a
coke, senza preriscaldo della
carica) e dal recupero calore
generico (li' il calore recuperato va
a un uso generico, senza fusione di
ghisa, senza forno a induzione,
senza cubilotto a coke).

Demo calcolata eseguendo demo_calcoli()
(e ricontrollata a mano, riga per
riga): ghisa 5.000 t/anno,
temperatura carica 20 C, temperatura
fusione 1450 C, quota recupero
preriscaldo 30 %, rendimento coke
0,45, rendimento induzione 0,70,
prezzo coke 60 EUR/MWh, prezzo
elettrico 110 EUR/MWh, O&M fisso
20.000 EUR/anno, CAPEX 150.000 EUR,
fattore coke 0,35 tCO2/MWh e fattore
elettrico 0,25 tCO2/MWh, WACC 5 %,
vita 15 anni, tolleranza 10 % del
CAPEX.

- delta_t_K = 1430.0
- q_risc_mwh_anno = 1390.2777777777778
- q_fus_mwh_anno = 375.0
- q_lordo_mwh_anno = 1765.2777777777778
- q_rec_mwh_anno = 529.5833333333334
- q_netto_mwh_anno = 1235.6944444444443
- coke_base_mwh_anno = 3922.8395061728397
- c_base_eur_anno = 235370.3703703704
- e_el_mwh_anno = 1765.2777777777778
- c_alt_var_eur_anno = 194180.55555555556
- c_alt_eur_anno = 214180.55555555556
- risparmio_eur_anno = 21189.814814814832
- co2_base_t_anno = 1372.9938271604938
- co2_alt_t_anno = 441.31944444444446
- co2_evitata_t_anno = 931.6743827160493
- crf = 0.09634228760924432
- quota_capex_eur_anno = 14451.343141386647
- lco_base_eur_t = 47.074074074074076
- lco_alt_eur_t = 45.72637973938845
- van = 69943.0316701509
- tir = 11.285718989835509
- payback = 8
- prezzo_pareggio_eur_mwh = 122.00367164961973
- verdetto = 'CONVIENTE'

Scomposizione: dT = 1450 - 20 = 1430 K;
Q_risc = 5.000 x 1000 x 0,70 x 1430 /
3.600.000 = 1.390,28 MWh/anno (sulla
massa ghisa, cp 0,70); Q_fus = 5.000 x
1000 x 270 / 3.600.000 = 375,00
MWh/anno; Q_lordo = 1.390,28 + 375,00
= 1.765,28 MWh/anno; Q_rec = 0,30 x
1.765,28 = 529,58 MWh/anno; Q_netto =
1.765,28 - 529,58 = 1.235,69 MWh/anno;
coke_base = 1.765,28 / 0,45 = 3.922,84
MWh/anno; C_base = 3.922,84 x 60 =
235.370,37 EUR/anno; E_el = 1.235,69 /
0,70 = 1.765,28 MWh/anno; C_alt_var =
1.765,28 x 110 = 194.180,56 EUR/anno;
C_alt = 194.180,56 + 20.000 =
214.180,56 EUR/anno; risparmio =
235.370,37 - 214.180,56 = 21.189,81
EUR/anno; CO2 base = 3.922,84 x 0,35
= 1.372,99 t/anno; CO2 alt = 1.765,28
x 0,25 = 441,32 t/anno; CO2 evitata =
931,67 t/anno; CRF 0,05 x 1,05^15 /
(1,05^15 - 1) = 0.09634228760924432;
quota CAPEX 150.000 x 0,096342 =
14.451,34 EUR/anno; LCO base
235.370,37 / 5.000 = 47,07 EUR/t; LCO
alt (14.451,34 + 20.000) / 5.000 +
194.180,56 / 5.000 = 45,73 EUR/t;
flussi: anno 0 -150.000, anni 1-15
risparmio 21.189,81 (piatti); VAN
-150.000 + 21.189,81 x 10,379658
(annuita' 15 anni al 5 %) =
69.943,03 EUR; TIR 11,29 %; payback 8
anni (il cumulato all'anno 7 e'
-1.671,30 EUR, all'anno 8 e'
19.518,52 EUR, strettamente positivo);
prezzo elettrico di pareggio
(235.370,37 - 20.000) / 1.765,28 =
122,00 EUR/MWh; verdetto CONVIENTE
perche' VAN > 0.
NOTA: il CRF entra solo nel LCO,
mai nei flussi: il CAPEX compare una
sola volta, all'anno 0.
NOTA 2: in questa tab il risparmio
nullo o negativo NON e' degenere: con
prezzo elettrico 130 EUR/MWh il caso
e' calcolabile (valid=True, flussi
pieni), NON_CONVIENTE con VAN
-296.516,56 EUR, non NON_CALCOLABILE.
NOTA 3: la CO2 evitata puo' essere
negativa: con fattore elettrico 2,00
tCO2/MWh la CO2 evitata e'
-2.157,56 t/anno, pur restando il caso
calcolabile e CONVIENTE.
NOTA 4: il prezzo elettrico di
pareggio come valore della funzione
pura puo' essere negativo: con O&M
fisso 5.000.000 il pareggio e'
-2.699,08 EUR/MWh circa, perche' il
solo O&M fisso supera gia' il costo
baseline (ma il caso resta
calcolabile in questa tab, con VAN
negativa).
NOTA 5: il calore netto nullo (quota
recupero 100 %) NON e' degenere:
il risparmio e' 215.370,37 EUR/anno
(235.370,37 - 20.000 di solo O&M
fisso) e la VAN 2.085.470,80 EUR, e il
pareggio non e' definito.
NOTA 6: il payback usa il cumulato
STRETTAMENTE positivo: con CAPEX
nullo e risparmio positivo il payback
e' 1, non 0 (all'anno 0 il cumulato
e' zero, non positivo); con flussi
[-100, 50, 50] il payback e' None
(il cumulato all'anno 2 e' zero, non
positivo).
NOTA 7: Q_risc usa la massa ghisa
(cp 0,70 kJ/kgK): con la demo Q_risc
= 1.390,28 MWh/anno; sul solo calore
latente senza riscaldamento il calore
sarebbe 375,00 MWh/anno.
NOTA 8: i valori demo sono stati
ricalcolati da zero: il brief del
ciclo indicava E_el 1.765,27,
risparmio 21.190,01, CO2 evitata
931,68, quota CAPEX 14.451,35, LCO
alternativo 45,7273 e pareggio
122,03; il ricalcolo esatto (senza
arrotondamenti intermedi) da'
1.765,28, 21.189,81, 931,67,
14.451,34, 45,7264 e 122,00: i file
usano i valori esatti.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w766_helpers import (
    demo_calcoli,
    mh765_c_alt,
    mh765_c_alt_var,
    mh765_c_base,
    mh765_calcola,
    mh765_co2_alt,
    mh765_co2_base,
    mh765_co2_evitata,
    mh765_coke_base,
    mh765_crf,
    mh765_csv,
    mh765_delta_t,
    mh765_demo,
    mh765_e_el,
    mh765_eta,
    mh765_flussi,
    mh765_int_pos,
    mh765_lco_alt,
    mh765_lco_base,
    mh765_nneg,
    mh765_num,
    mh765_payback,
    mh765_pct_0_100,
    mh765_pct_wacc,
    mh765_pos,
    mh765_prezzo_pareggio,
    mh765_q_fus,
    mh765_q_lordo,
    mh765_q_netto,
    mh765_q_rec,
    mh765_q_risc,
    mh765_quota_capex,
    mh765_risparmio,
    mh765_temp_carica,
    mh765_temp_fusione,
    mh765_tir,
    mh765_valida,
    mh765_van,
    mh765_verdetto,
)


def _demo_kwargs():
    return dict(mh765_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh765_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh765_num(3, "x") == 3.0
    assert mh765_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh765_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh765_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh765_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh765_pos(0, "x")
    with pytest.raises(ValueError):
        mh765_pos(-1, "x")
    assert mh765_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh765_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh765_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh765_int_pos(0, "x")


def test_pct_0_100_limiti():
    assert mh765_pct_0_100(0, "x") == 0.0
    assert mh765_pct_0_100(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh765_pct_0_100(100.1, "x")
    with pytest.raises(ValueError):
        mh765_pct_0_100(-1, "x")


def test_pct_wacc_limiti():
    assert mh765_pct_wacc(0, "x") == 0.0
    assert mh765_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh765_pct_wacc(50.1, "x")


def test_eta_limiti():
    assert mh765_eta(1.0, "x") == 1.0
    assert mh765_eta(0.45, "x") == 0.45
    with pytest.raises(ValueError):
        mh765_eta(0, "x")
    with pytest.raises(ValueError):
        mh765_eta(-0.1, "x")
    with pytest.raises(ValueError):
        mh765_eta(1.01, "x")


def test_temp_limiti():
    assert mh765_temp_carica(0, "x") == 0.0
    assert mh765_temp_carica(999.0, "x") == 999.0
    with pytest.raises(ValueError):
        mh765_temp_carica(1000, "x")
    with pytest.raises(ValueError):
        mh765_temp_carica(-1, "x")
    assert mh765_temp_fusione(2000, "x") == 2000.0
    with pytest.raises(ValueError):
        mh765_temp_fusione(0, "x")
    with pytest.raises(ValueError):
        mh765_temp_fusione(2000.1, "x")


# ---------------------------------------------------------------- fisica base
def test_delta_q_risc_q_fus_q_lordo():
    assert mh765_delta_t(20, 1450) == pytest.approx(1430.0)
    assert mh765_delta_t(1450, 20) == pytest.approx(-1430.0)
    assert mh765_q_risc(5000, 1430.0) == pytest.approx(1390.2777777777778)
    assert mh765_q_risc(5000, 0) == 0.0
    assert mh765_q_risc(2500, 1430.0) == pytest.approx(695.1388888888889)
    assert mh765_q_fus(5000) == pytest.approx(375.0)
    assert mh765_q_fus(0) == 0.0
    assert mh765_q_lordo(1390.2777777777778, 375.0) == \
        pytest.approx(1765.2777777777778)
    with pytest.raises(ValueError):
        mh765_q_fus(-1)
    with pytest.raises(ValueError):
        mh765_q_risc(-1, 1430.0)


def test_q_rec_netto():
    assert mh765_q_rec(1765.2777777777778, 30.0) == pytest.approx(
        529.5833333333334)
    assert mh765_q_rec(1765.2777777777778, 0) == 0.0
    assert mh765_q_rec(1765.2777777777778, 100) == pytest.approx(
        1765.2777777777778)
    assert mh765_q_netto(1765.2777777777778, 529.5833333333334) == \
        pytest.approx(1235.6944444444443)
    assert mh765_q_netto(1765.2777777777778, 1765.2777777777778) == 0.0
    with pytest.raises(ValueError):
        mh765_q_rec(1765.2777777777778, 100.1)


def test_coke_base_e_c_base_e_co2_base():
    assert mh765_coke_base(1765.2777777777778, 0.45) == pytest.approx(
        3922.8395061728397)
    assert mh765_coke_base(1765.2777777777778, 1.0) == pytest.approx(
        1765.2777777777778)
    assert mh765_c_base(3922.8395061728397, 60) == pytest.approx(
        235370.3703703704)
    assert mh765_co2_base(3922.8395061728397, 0.35) == pytest.approx(
        1372.9938271604938)
    with pytest.raises(ValueError):
        mh765_coke_base(1765.2777777777778, 0)


def test_e_el():
    assert mh765_e_el(1235.6944444444443, 0.70) == pytest.approx(
        1765.2777777777778)
    assert mh765_e_el(1235.6944444444443, 0) is None
    assert mh765_e_el(1235.6944444444443, -1.0) is None
    assert mh765_e_el(0.0, 0.70) == 0.0


def test_c_alt_var_e_c_alt():
    assert mh765_c_alt_var(1765.2777777777778, 110) == pytest.approx(
        194180.55555555556)
    assert mh765_c_alt_var(0.0, 110) == 0.0
    assert mh765_c_alt(194180.55555555556, 20000) == pytest.approx(
        214180.55555555556)
    assert mh765_c_alt(194180.55555555556, 0) == pytest.approx(
        194180.55555555556)
    with pytest.raises(ValueError):
        mh765_c_alt_var(1765.2777777777778, -1)


def test_risparmio_segno():
    assert mh765_risparmio(235370.3703703704, 214180.55555555556) == \
        pytest.approx(21189.814814814832)
    assert mh765_risparmio(235370.3703703704, 235370.3703703704) == 0.0
    assert mh765_risparmio(156913.5802469136, 214180.55555555556) == \
        pytest.approx(-57266.975308641966)


def test_co2_alt_e_evitata_segno_libero():
    assert mh765_co2_alt(1765.2777777777778, 0.25) == pytest.approx(
        441.31944444444446)
    assert mh765_co2_evitata(1372.9938271604938,
                             441.31944444444446) == pytest.approx(
        931.6743827160493)
    assert mh765_co2_evitata(1372.9938271604938,
                             3530.5555555555557) == pytest.approx(
        -2157.561728395062, abs=1e-6)


# ---------------------------------------------------------------- finanza base
def test_crf():
    assert mh765_crf(5.0, 15) == pytest.approx(0.09634228760924432)
    assert mh765_crf(0, 15) == pytest.approx(1.0 / 15.0)
    assert mh765_crf(5.0, 1) == pytest.approx(1.05)
    assert mh765_crf(5.0, 10) == pytest.approx(0.12950457496545661)


def test_quota_capex_e_lco():
    assert mh765_quota_capex(150000, 0.09634228760924432) == pytest.approx(
        14451.343141386647)
    assert mh765_lco_base(235370.3703703704, 5000.0) == \
        pytest.approx(47.074074074074076)
    assert mh765_lco_base(235370.3703703704, 0) is None
    assert mh765_lco_alt(150000, 0.09634228760924432, 20000,
                         194180.55555555556,
                         5000.0) == pytest.approx(
        45.72637973938845)
    assert mh765_lco_alt(150000, 0.09634228760924432, 20000,
                         194180.55555555556, 0) is None
    assert mh765_lco_alt(0, 0.09634228760924432, 20000,
                         194180.55555555556,
                         5000.0) == pytest.approx(
        42.836111111111116)


def test_prezzo_pareggio_formula_negativo_e_none():
    assert mh765_prezzo_pareggio(235370.3703703704, 20000,
                                 1765.2777777777778) == pytest.approx(
        122.00367164961973)
    assert mh765_prezzo_pareggio(235370.3703703704, 20000, 0.0) is None
    assert mh765_prezzo_pareggio(235370.3703703704, 20000, None) is None


def test_prezzo_pareggio_negativo_solo_funzione_pura():
    """Il pareggio negativo esiste come valore della
    funzione pura: con O&M fisso 5.000.000 il numeratore e'
    negativo; in questa tab quel caso resta comunque
    calcolabile (VAN negativa)."""
    bc = demo_calcoli()
    assert mh765_prezzo_pareggio(bc["c_base_eur_anno"], 5000000,
                                 bc["e_el_mwh_anno"]) == pytest.approx(
        -2699.0820875950694, abs=1e-6)
    assert bc["prezzo_pareggio_eur_mwh"] > 0.0


def test_flussi_lunghezza_e_primo():
    fl = mh765_flussi(150000, 21189.814814814832, 15)
    assert len(fl) == 16
    assert fl[0] == -150000
    assert all(f == 21189.814814814832 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = demo_calcoli()
    assert bc["van"] == pytest.approx(69943.0316701509)
    assert mh765_van([-150000] + [21189.814814814832] * 15,
                     0) == pytest.approx(167847.22222222248)
    assert mh765_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = demo_calcoli()
    assert bc["tir"] == pytest.approx(11.285718989835509)
    assert mh765_tir([-150000] + [21189.814814814832] * 15) == pytest.approx(
        0.11285718989835509)
    tir = mh765_tir([-150000] + [21189.814814814832] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-150000] + [21189.814814814832] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_stretto():
    """Payback STRETTAMENTE positivo: il cumulato nullo
    non basta."""
    assert mh765_payback([-150000] + [21189.814814814832] * 15) == 8
    assert mh765_payback([-150000] + [-1000.0] * 15) is None
    assert mh765_payback([0] + [21189.814814814832] * 15) == 1
    assert mh765_payback([-100] + [50] * 2) is None
    assert mh765_payback([-100] + [50] * 3) == 3


def test_verdetto():
    assert mh765_verdetto(100.0, 150000, 10.0) == "CONVIENTE"
    assert mh765_verdetto(-14000.0, 150000, 10.0) == "MARGINALE"
    assert mh765_verdetto(-15000.0, 150000, 10.0) == "MARGINALE"
    assert mh765_verdetto(-15000.01, 150000, 10.0) == "NON_CONVIENTE"
    assert mh765_verdetto(float("nan"), 150000, 10.0) == "NON_CALCOLABILE"
    assert mh765_verdetto(0.0, 0, 10.0) == "MARGINALE"


def test_valida_demo_ok():
    v = mh765_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("m_ghisa_t_anno", "5000"),
                       ("m_ghisa_t_anno", float("nan")),
                       ("m_ghisa_t_anno", float("inf")),
                       ("m_ghisa_t_anno", True),
                       ("prezzo_el_eur_mwh", None)):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh765_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("m_ghisa_t_anno", 0),
                          ("m_ghisa_t_anno", -1),
                          ("t_carica_C", -1),
                          ("t_carica_C", 1000),
                          ("t_fusione_C", 0),
                          ("t_fusione_C", 2000.1),
                          ("eta_coke", 0),
                          ("eta_coke", 1.01),
                          ("eta_induzione", 0),
                          ("eta_induzione", 1.01),
                          ("quota_recupero_pct", -1),
                          ("quota_recupero_pct", 100.1),
                          ("prezzo_coke_eur_mwh", -1),
                          ("prezzo_el_eur_mwh", -1),
                          ("om_fisso_eur_anno", -100),
                          ("capex_eur", -1),
                          ("f_coke_t_per_mwh", -0.10),
                          ("f_el_t_per_mwh", -0.10),
                          ("wacc_pct", -0.1), ("wacc_pct", 50.1),
                          ("vita_anni", 0), ("vita_anni", 2.5),
                          ("tolleranza_pct", -1),
                          ("tolleranza_pct", 100.1)):
        d = _demo_kwargs()
        d[campo] = valore
        assert mh765_valida(**d)["valido"] is False


def test_valida_rifiuta_delta_non_valido():
    for ti, tc in ((1450, 1450), (1450, 20), (20, 20)):
        d = _demo_kwargs()
        d["t_carica_C"] = ti
        d["t_fusione_C"] = tc
        assert mh765_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"quota_recupero_pct": 0,
              "prezzo_coke_eur_mwh": 0,
              "prezzo_el_eur_mwh": 0, "om_fisso_eur_anno": 0,
              "capex_eur": 0, "f_coke_t_per_mwh": 0,
              "f_el_t_per_mwh": 0, "wacc_pct": 0,
              "tolleranza_pct": 0, "eta_coke": 1.0,
              "eta_induzione": 1.0,
              "t_carica_C": 0, "t_fusione_C": 2000})
    assert mh765_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["quota_recupero_pct"] = 100
    assert mh765_valida(**d)["valido"] is True


def test_valida_non_controlla_risparmio_calcola_neppure():
    """La validazione input NON controlla il risparmio
    (e' un esito, non un range) e in questa tab
    nemmeno mh765_calcola lo controlla: con prezzo
    elettrico 130 il caso resta CALCOLABILE."""
    d = _demo_kwargs()
    d["prezzo_el_eur_mwh"] = 130
    assert mh765_valida(**d)["valido"] is True
    bc = _variante(prezzo_el_eur_mwh=130)
    assert bc["valid"] is True
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["flussi"]
    assert bc["tir"] is None
    assert bc["payback"] is None


def test_demo_dict():
    d = mh765_demo()
    assert d["m_ghisa_t_anno"] == 5000
    assert d["t_carica_C"] == 20
    assert d["t_fusione_C"] == 1450
    assert d["eta_coke"] == 0.45
    assert d["eta_induzione"] == 0.70
    assert d["quota_recupero_pct"] == 30.0
    assert d["prezzo_coke_eur_mwh"] == 60
    assert d["prezzo_el_eur_mwh"] == 110
    assert d["om_fisso_eur_anno"] == 20000
    assert d["capex_eur"] == 150000
    assert d["f_coke_t_per_mwh"] == 0.35
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
        "delta_t_K": 1430.0,
        "q_risc_mwh_anno": 1390.2777777777778,
        "q_fus_mwh_anno": 375.0,
        "q_lordo_mwh_anno": 1765.2777777777778,
        "q_rec_mwh_anno": 529.5833333333334,
        "q_netto_mwh_anno": 1235.6944444444443,
        "coke_base_mwh_anno": 3922.8395061728397,
        "c_base_eur_anno": 235370.3703703704,
        "e_el_mwh_anno": 1765.2777777777778,
        "c_alt_var_eur_anno": 194180.55555555556,
        "c_alt_eur_anno": 214180.55555555556,
        "risparmio_eur_anno": 21189.814814814832,
        "co2_base_t_anno": 1372.9938271604938,
        "co2_alt_t_anno": 441.31944444444446,
        "co2_evitata_t_anno": 931.6743827160493,
        "crf": 0.09634228760924432,
        "quota_capex_eur_anno": 14451.343141386647,
        "lco_base_eur_t": 47.074074074074076,
        "lco_alt_eur_t": 45.72637973938845,
        "van": 69943.0316701509,
        "tir": 11.285718989835509,
        "prezzo_pareggio_eur_mwh": 122.00367164961973,
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
    assert bc["q_risc_mwh_anno"] == pytest.approx(1390.2777777777778)
    assert bc["q_fus_mwh_anno"] == pytest.approx(375.0)
    assert bc["q_lordo_mwh_anno"] == pytest.approx(1765.2777777777778)
    assert bc["q_rec_mwh_anno"] == pytest.approx(529.5833333333334)
    assert bc["q_netto_mwh_anno"] == pytest.approx(1235.6944444444443)
    assert bc["coke_base_mwh_anno"] == pytest.approx(3922.8395061728397)
    assert bc["co2_evitata_t_anno"] == pytest.approx(931.6743827160493)


def test_demo_calcoli_economia():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(235370.3703703704)
    assert bc["c_alt_var_eur_anno"] == pytest.approx(194180.55555555556)
    assert bc["c_alt_eur_anno"] == pytest.approx(214180.55555555556)
    assert bc["risparmio_eur_anno"] == pytest.approx(21189.814814814832)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(122.00367164961973)


def test_demo_calcoli_finanza():
    bc = demo_calcoli()
    assert bc["crf"] == pytest.approx(0.09634228760924432)
    assert bc["quota_capex_eur_anno"] == pytest.approx(14451.343141386647)
    assert bc["lco_base_eur_t"] == pytest.approx(47.074074074074076)
    assert bc["lco_alt_eur_t"] == pytest.approx(45.72637973938845)
    assert bc["van"] == pytest.approx(69943.0316701509)
    assert bc["tir"] == pytest.approx(11.285718989835509)
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"


def test_demo_flussi_e_cumulato():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -150000
    assert len(bc["flussi"]) == 16
    assert all(f == 21189.814814814832 for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -150000
    assert righe.iloc[5]["Cumulato (EUR)"] == pytest.approx(-44050.92592592584)
    assert righe.iloc[7]["Cumulato (EUR)"] == pytest.approx(-1671.2962962961756)
    assert righe.iloc[8]["Cumulato (EUR)"] == pytest.approx(19518.518518518656)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(167847.22222222248)
    assert righe.iloc[15]["Flusso (EUR/anno)"] == 21189.814814814832


def test_demo_tabella_righe():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Calore lordo (MWh/anno)"] == pytest.approx(1765.2777777777778)
    assert mappa["Calore recuperato (MWh/anno)"] == pytest.approx(529.5833333333334)
    assert mappa["Calore netto (MWh/anno)"] == pytest.approx(1235.6944444444443)
    assert mappa["Ghisa (t/anno)"] == pytest.approx(5000.0)
    assert mappa["Salto termico (K)"] == pytest.approx(1430.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(214180.55555555556)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(21189.814814814832)
    assert mappa["Payback (anni)"] == 8
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Prezzo elettrico di pareggio (EUR/MWh)"] == pytest.approx(
        122.00367164961973)


def test_demo_coerenza_interna():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["c_alt_var_eur_anno"] + bc["om_fisso_eur_anno"] == \
        pytest.approx(bc["c_alt_eur_anno"])
    assert bc["coke_base_mwh_anno"] * bc["prezzo_coke_eur_mwh"] == \
        pytest.approx(bc["c_base_eur_anno"])
    assert bc["co2_base_t_anno"] - bc["co2_alt_t_anno"] == \
        pytest.approx(bc["co2_evitata_t_anno"])
    assert bc["capex_eur"] * bc["crf"] == pytest.approx(
        bc["quota_capex_eur_anno"])
    assert (bc["quota_capex_eur_anno"] + bc["om_fisso_eur_anno"]) / \
        bc["m_ghisa_t_anno"] + bc["c_alt_var_eur_anno"] / \
        bc["m_ghisa_t_anno"] == pytest.approx(bc["lco_alt_eur_t"])
    assert bc["c_base_eur_anno"] - bc["om_fisso_eur_anno"] == \
        pytest.approx(bc["prezzo_pareggio_eur_mwh"] *
                      bc["e_el_mwh_anno"])
    assert bc["q_lordo_mwh_anno"] - bc["q_rec_mwh_anno"] == \
        pytest.approx(bc["q_netto_mwh_anno"])
    assert bc["q_risc_mwh_anno"] + bc["q_fus_mwh_anno"] == \
        pytest.approx(bc["q_lordo_mwh_anno"])
    assert bc["m_ghisa_t_anno"] * 1000.0 * 0.70 * \
        bc["delta_t_K"] / 3600000.0 == pytest.approx(
        bc["q_risc_mwh_anno"])
    assert bc["m_ghisa_t_anno"] * 1000.0 * 270.0 / \
        3600000.0 == pytest.approx(bc["q_fus_mwh_anno"])


def test_demo_crf_solo_nel_lco_non_nei_flussi():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -bc["capex_eur"]
    assert all(f == bc["risparmio_eur_anno"] for f in bc["flussi"][1:])
    assert bc["crf"] not in bc["flussi"]
    assert bc["quota_capex_eur_anno"] not in bc["flussi"]
    van_da_flussi = mh765_van(bc["flussi"], bc["wacc_pct"])
    assert van_da_flussi == pytest.approx(bc["van"])
    assert bc["lco_alt_eur_t"] == pytest.approx(
        (bc["capex_eur"] * bc["crf"] + bc["om_fisso_eur_anno"]) /
        bc["m_ghisa_t_anno"] + bc["c_alt_var_eur_anno"] /
        bc["m_ghisa_t_anno"])


def test_demo_contro_riconteggio_indipendente():
    mg, ti, tc = 5000, 20, 1450
    eta_c, eta_i, qr = 0.45, 0.70, 30.0
    pc, pel, om, cx = 60, 110, 20000, 150000
    fc, fe, wacc, vita = 0.35, 0.25, 5.0, 15
    dt = tc - ti
    qri = mg * 1000 * 0.70 * dt / 3600000.0
    qfu = mg * 1000 * 270 / 3600000.0
    ql = qri + qfu
    qrec = qr / 100 * ql
    qn = ql - qrec
    cb_coke = ql / eta_c
    cb = cb_coke * pc
    ee = qn / eta_i
    cav = ee * pel
    ca = cav + om
    risp = cb - ca
    co2b = cb_coke * fc
    co2a = ee * fe
    r = wacc / 100.0
    crf = r * (1 + r) ** vita / ((1 + r) ** vita - 1)
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    bc = demo_calcoli()
    assert bc["delta_t_K"] == pytest.approx(dt)
    assert bc["q_risc_mwh_anno"] == pytest.approx(qri)
    assert bc["q_fus_mwh_anno"] == pytest.approx(qfu)
    assert bc["q_lordo_mwh_anno"] == pytest.approx(ql)
    assert bc["q_rec_mwh_anno"] == pytest.approx(qrec)
    assert bc["q_netto_mwh_anno"] == pytest.approx(qn)
    assert bc["coke_base_mwh_anno"] == pytest.approx(cb_coke)
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


def test_variante_prezzo_el_alto_calcolabile_non_conviente():
    """Sensibilita' richiesta dal brief: prezzo elettrico
    130 EUR/MWh. In questa tab il risparmio negativo e'
    CALCOLABILE."""
    bc = _variante(prezzo_el_eur_mwh=130)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(-14115.74074074073)
    assert bc["van"] == pytest.approx(-296516.56184450275)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(122.00367164961973)
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["flussi"]


def test_variante_coke_quaranta_calcolabile_non_conviente():
    bc = _variante(prezzo_coke_eur_mwh=40)
    assert bc["risparmio_eur_anno"] == pytest.approx(-57266.975308641966)
    assert bc["van"] == pytest.approx(-744411.620584635)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_variante_coke_cinquantasette_non_conviente():
    bc = _variante(prezzo_coke_eur_mwh=57)
    assert bc["risparmio_eur_anno"] == pytest.approx(9421.296296296292)
    assert bc["van"] == pytest.approx(-52210.16616806717)
    assert bc["van"] < 0.0
    assert abs(bc["van"]) > 0.10 * 150000
    assert bc["tir"] == pytest.approx(-0.736065604140318, abs=1e-4)
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(115.33700498295305)
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_variante_coke_cinquantotto_marginale():
    bc = _variante(prezzo_coke_eur_mwh=58)
    assert bc["risparmio_eur_anno"] == pytest.approx(13344.135802469129)
    assert bc["van"] == pytest.approx(-11492.433555327909)
    assert bc["van"] < 0.0
    assert abs(bc["van"]) <= 0.10 * 150000
    assert bc["verdetto"] == "MARGINALE"
    assert bc["valid"] is True


def test_variante_prezzo_el_zero_conviente():
    bc = _variante(prezzo_el_eur_mwh=0.0)
    assert bc["c_alt_var_eur_anno"] == 0.0
    assert bc["c_alt_eur_anno"] == 20000.0
    assert bc["risparmio_eur_anno"] == pytest.approx(215370.3703703704)
    assert bc["van"] == pytest.approx(2085470.796000746)
    assert bc["tir"] == pytest.approx(143.5800191575988, abs=1e-4)
    assert bc["payback"] == 1
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_variante_quota_recupero_cento_calcolabile_non_degenere():
    """Sensibilita' richiesta dal brief: recupero 100 %."""
    bc = _variante(quota_recupero_pct=100)
    assert bc["valid"] is True
    assert bc["q_netto_mwh_anno"] == 0.0
    assert bc["e_el_mwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(215370.3703703704)
    assert bc["van"] == pytest.approx(2085470.796000746)
    assert bc["tir"] == pytest.approx(143.5800191575988, abs=1e-4)
    assert bc["payback"] == 1
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_quota_recupero_zero_calcolabile_non_conviente():
    bc = _variante(quota_recupero_pct=0)
    assert bc["valid"] is True
    assert bc["q_netto_mwh_anno"] == pytest.approx(1765.2777777777778)
    assert bc["e_el_mwh_anno"] == pytest.approx(2521.825396825397)
    assert bc["risparmio_eur_anno"] == pytest.approx(-62030.423280423274)
    assert bc["van"] == pytest.approx(-793854.5816143899)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_co2_evitata_negativa_con_fattore_el_alto():
    bc = _variante(f_el_t_per_mwh=2.0)
    assert bc["co2_alt_t_anno"] == pytest.approx(3530.5555555555557)
    assert bc["co2_evitata_t_anno"] == pytest.approx(-2157.561728395062)
    assert bc["co2_evitata_t_anno"] < 0.0
    assert bc["van"] == pytest.approx(69943.0316701509)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero():
    bc = _variante(wacc_pct=0)
    assert bc["crf"] == pytest.approx(1.0 / 15.0)
    assert bc["quota_capex_eur_anno"] == pytest.approx(10000.0)
    assert bc["van"] == pytest.approx(167847.22222222248)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_zero_payback_uno_tir_none():
    """Payback stretto: con CAPEX nullo il payback e' 1,
    non 0 (all'anno 0 il cumulato e' zero)."""
    bc = _variante(capex_eur=0)
    assert bc["capex_eur"] == 0
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 1
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(219943.03167015093)
    assert bc["lco_alt_eur_t"] == pytest.approx(42.836111111111116)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_vita_dieci():
    bc = _variante(vita_anni=10)
    assert len(bc["flussi"]) == 11
    assert bc["crf"] == pytest.approx(0.12950457496545661)
    assert bc["van"] == pytest.approx(13622.133198513475)
    assert bc["tir"] == pytest.approx(6.830717532903508, abs=1e-4)
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_fattori_zero_calcolabile():
    bc = _variante(f_coke_t_per_mwh=0, f_el_t_per_mwh=0)
    assert bc["valid"] is True
    assert bc["co2_base_t_anno"] == 0.0
    assert bc["co2_alt_t_anno"] == 0.0
    assert bc["co2_evitata_t_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(21189.814814814832)


# ---------------------------------------------------------------- degenere
def test_degenere_ghisa_zero():
    bc = _variante(m_ghisa_t_anno=0)
    assert bc["valid"] is False
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"] == []
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["lco_base_eur_t"] is None
    assert bc["lco_alt_eur_t"] is None
    assert bc["errore"]


def test_degenere_delta_eta_vita():
    for kw in ({"t_carica_C": 1450, "t_fusione_C": 1450},
               {"t_carica_C": 1450, "t_fusione_C": 20},
               {"eta_coke": 0}, {"eta_induzione": 0},
               {"m_ghisa_t_anno": 0},
               {"m_ghisa_t_anno": -1},
               {"vita_anni": 0}, {"vita_anni": 2.5}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_eta_wacc_tolleranza_quote_prezzi_negativi():
    for kw in ({"eta_coke": 0}, {"eta_coke": 1.01},
               {"eta_induzione": 0}, {"eta_induzione": 1.01},
               {"wacc_pct": -1}, {"wacc_pct": 60},
               {"tolleranza_pct": -1}, {"tolleranza_pct": 101},
               {"quota_recupero_pct": -1}, {"quota_recupero_pct": 101},
               {"prezzo_coke_eur_mwh": -1},
               {"prezzo_el_eur_mwh": -1},
               {"om_fisso_eur_anno": -100},
               {"capex_eur": -1},
               {"t_carica_C": -1}, {"t_carica_C": 1000},
               {"t_fusione_C": 0}, {"t_fusione_C": 2000.1}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_stringa_nan_inf():
    for kw in ({"m_ghisa_t_anno": "5000"},
               {"m_ghisa_t_anno": float("nan")},
               {"prezzo_el_eur_mwh": float("inf")},
               {"capex_eur": True}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_risparmio_negativo_non_degenere():
    """Differenza chiave: risparmio negativo resta
    calcolabile, con flussi pieni e VAN negativa."""
    for kw in ({"prezzo_el_eur_mwh": 130},
               {"prezzo_coke_eur_mwh": 40},
               {"quota_recupero_pct": 0},
               {"prezzo_el_eur_mwh": 400}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] < 0.0
        assert bc["verdetto"] in ("NON_CONVIENTE", "MARGINALE")
        assert bc["flussi"]


def test_degenere_neutro_campi():
    bc = _variante(m_ghisa_t_anno=0)
    assert bc["q_lordo_mwh_anno"] == 0.0
    assert bc["coke_base_mwh_anno"] == 0.0
    assert bc["c_base_eur_anno"] == 0.0
    assert bc["c_alt_eur_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == 0.0
    assert bc["van"] == 0.0
    assert list(bc["df_flussi"].columns) == [
        "Anno", "Flusso (EUR/anno)", "Cumulato (EUR)"]
    assert list(bc["df_tabella"].columns) == ["Voce", "Valore"]


def test_pareggio_none_quando_e_el_zero():
    assert mh765_prezzo_pareggio(235370.3703703704, 20000, 0.0) is None
    assert mh765_prezzo_pareggio(235370.3703703704, 20000, None) is None
    assert mh765_lco_base(235370.3703703704, 0) is None
    assert mh765_e_el(1235.6944444444443, 0) is None
    bc = _variante(quota_recupero_pct=100)
    assert bc["prezzo_pareggio_eur_mwh"] is None


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = demo_calcoli()
    testo = mh765_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert "q_lordo_mwh_anno;1765.2777777777778" in testo
    assert "q_netto_mwh_anno;1235.6944444444443" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "prezzo_pareggio_eur_mwh" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = demo_calcoli()
    testo = mh765_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"quota_capex_eur_anno;{bc['quota_capex_eur_anno']}" in testo
    assert f"q_lordo_mwh_anno;{bc['q_lordo_mwh_anno']}" in testo


def test_csv_degenere_solo_zeri():
    bc = _variante(m_ghisa_t_anno=0)
    testo = mh765_csv(bc, _demo_kwargs())
    assert "van_eur;0.0" in testo
    assert "q_lordo_mwh_anno;0.0" in testo
    assert "verdetto;NON_CALCOLABILE" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = demo_calcoli()
    testo = mh765_csv(bc, _demo_kwargs())
    for chiave in _demo_kwargs():
        assert f"{chiave};" in testo


def test_calcola_non_sollevela_per_input_numerici():
    bc = _variante(f_coke_t_per_mwh=0, f_el_t_per_mwh=0)
    assert bc["valid"] is True
    assert bc["co2_base_t_anno"] == 0.0
    assert bc["co2_alt_t_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(21189.814814814832)


def test_monotonia_prezzo_el():
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(prezzo_el_eur_mwh=120)["risparmio_eur_anno"]
    basso = _variante(prezzo_el_eur_mwh=100)["risparmio_eur_anno"]
    assert basso > base > alto
    assert basso - base == pytest.approx(17652.777777777777)
    assert base - alto == pytest.approx(17652.777777777777)


def test_monotonia_quota_recupero():
    base = demo_calcoli()["risparmio_eur_anno"]
    alta = _variante(quota_recupero_pct=40)["risparmio_eur_anno"]
    bassa = _variante(quota_recupero_pct=20)["risparmio_eur_anno"]
    assert alta > base > bassa


def test_demo_deterministica_due_chiamate():
    a = demo_calcoli()
    b = demo_calcoli()
    assert a["van"] == b["van"]
    assert a["flussi"] == b["flussi"]
    assert a["tir"] == b["tir"]


def test_demo_chiavi_attese():
    assert set(mh765_demo().keys()) == {
        "m_ghisa_t_anno",
        "t_carica_C", "t_fusione_C",
        "eta_coke", "eta_induzione",
        "quota_recupero_pct",
        "prezzo_coke_eur_mwh", "prezzo_el_eur_mwh",
        "om_fisso_eur_anno", "capex_eur",
        "f_coke_t_per_mwh", "f_el_t_per_mwh",
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
    return ["mh" + "76" + "4", "st" + "76" + "4",
            "tab" + "76" + "4", "w" + "76" + "5_",
            "mh" + "76" + "3", "st" + "76" + "3",
            "tab" + "76" + "3", "w" + "76" + "4_"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w766_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w766_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab765:")


def test_registry_chain_tail_and_count():
    """Registry della nuova tab: il frammento UI apre la tab
    numero 765 (la coda della catena termina con la nuova tab
    e il conteggio atteso delle tab e' 765)."""
    src = _leggi("w766_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 765
    assert src.count("with tab765:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w766_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w766_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st765_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert "key=f" not in src and 'key = f' not in src
    assert "st.stop()" in src
    # guard degenere prima di KPI / grafico / tabella / CSV
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w766_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def765[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w766_ui.py")
        usate = set(re.findall(r'_def765\["([^"]+)"\]', src))
        assert usate
        assert usate <= set(mh765_demo().keys())


def test_ui_chiavi_demo_coerenti():
    """Ogni _def765[...] letto dalla UI esiste nel dict demo:
    sweep anti-KeyError a render (lezione dello sweep chiavi demo vs UI)."""
    src = _leggi("w766_ui.py")
    usate = set(re.findall(r'_def765\["([^"]+)"\]', src))
    assert usate
    assert usate <= set(mh765_demo().keys())


def test_ui_riferisce_solo_helper_nuovi():
    src = _leggi("w766_ui.py")
    usati = set(re.findall(r'\b(mh\d+_\w+)\b', src))
    assert usati
    assert all(u.startswith("mh765_") for u in usati)


@pytest.mark.parametrize("wacc,vita,atteso", [
    (5.0, 15, 0.09634228760924432),
    (0, 15, 1.0 / 15.0),
    (10.0, 10, 0.16274539488251152),
    (5.0, 1, 1.05),
    (50.0, 5, 0.5758293838862559),
])
def test_crf_parametrizzato(wacc, vita, atteso):
    assert mh765_crf(wacc, vita) == pytest.approx(atteso)


@pytest.mark.parametrize("campo,valore", [
    ("m_ghisa_t_anno", 0), ("m_ghisa_t_anno", -3),
    ("t_carica_C", -1), ("t_carica_C", 1000),
    ("t_fusione_C", 0), ("t_fusione_C", 2000.1),
    ("eta_coke", 0), ("eta_coke", 1.01),
    ("eta_induzione", 0), ("eta_induzione", 1.01),
    ("quota_recupero_pct", -1), ("quota_recupero_pct", 100.1),
    ("prezzo_coke_eur_mwh", -1),
    ("prezzo_el_eur_mwh", -1),
    ("om_fisso_eur_anno", -100),
    ("capex_eur", -1),
    ("f_coke_t_per_mwh", -0.10), ("f_el_t_per_mwh", -0.10),
    ("wacc_pct", -0.1), ("wacc_pct", 50.1),
    ("vita_anni", -1), ("vita_anni", 2.5),
    ("tolleranza_pct", -1), ("tolleranza_pct", 100.1),
])
def test_valida_rifiuta_singoli_campi(campo, valore):
    d = _demo_kwargs()
    d[campo] = valore
    assert mh765_valida(**d)["valido"] is False


def test_df_tabella_valori_demo_selezionati():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Ghisa (t/anno)"] == 5000.0
    assert mappa["Calore lordo (MWh/anno)"] == pytest.approx(1765.2777777777778)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(21189.814814814832)
    assert mappa["Verdetto"] == "CONVIENTE"


def test_lco_alt_minore_di_lco_base_demo():
    bc = demo_calcoli()
    assert bc["lco_alt_eur_t"] < bc["lco_base_eur_t"]
    assert bc["lco_base_eur_t"] - bc["lco_alt_eur_t"] == pytest.approx(
        1.347694334685626)
