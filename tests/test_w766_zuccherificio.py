"""Test tab766 "Zuccherificio:
concentrare il succo con
multi-effetto e MVR batte
l'evaporatore a singolo effetto
a gas?"

Nuova tab tab766 (zuccherificio,
file di lavoro w767).
Business case deterministico
della concentrazione del succo di
barbabietola per evaporazione: i
solidi si conservano, quindi
P = F x Bx_in / Bx_out e l'acqua
evaporata e' W = F - P; calore
latente di evaporazione
dell'acqua 2257 kJ/kg (letterale
dentro le funzioni, 1 MWh =
3600000 kJ); baseline singolo
effetto a gas con economia
econ_base: V_base = W / econ_base,
Q_base = V_base x 1000 x 2257 /
3600000, Gas_base = Q_base /
eta_caldaia, C_base = Gas_base x
p_gas, CO2_base = Gas_base x
f_gas; alternativa multi-effetto
(economia n_effetti x 0,85) piu'
MVR su una quota di W:
W_mvr = q_mvr / 100 x W,
E_mvr = W_mvr x consumo_mvr /
1000, W_me = W - W_mvr,
V_alt = W_me / econ_me,
Q_alt = V_alt x 1000 x 2257 /
3600000, Gas_alt = Q_alt /
eta_caldaia, C_alt_var =
Gas_alt x p_gas + E_mvr x p_el,
C_alt = C_alt_var + OM_fisso,
CO2_alt = Gas_alt x f_gas +
E_mvr x f_el; risparmio =
C_base - C_alt; CO2 evitata =
CO2_base - CO2_alt, segno libero
(puo' essere negativa), NON
monetizzata; fattori di emissione
in tCO2/MWh, numericamente uguali
a kg/kWh (1 kg/kWh = 1 t/MWh);
CRF solo nel LCO, mai nei flussi;
LCO_base = C_base / P;
LCO_alt = (CAPEX x CRF + OM_fisso)
/ P + C_alt_var / P; prezzo
elettrico di pareggio =
(C_base - Gas_alt x p_gas -
OM_fisso) / E_mvr, None se
E_mvr <= 0; flussi [-CAPEX,
risparmio x vita]; VAN, TIR,
payback (primo anno con cumulato
STRETTAMENTE > 0). In questa tab
il risparmio nullo o negativo NON
e' degenere: resta calcolabile e
porta a VAN negativa
(NON_CONVIENTE o MARGINALE).
q_mvr = 100 % NON e' degenere:
Gas_alt = 0. q_mvr = 0 % NON e'
degenere: E_mvr = 0 e il pareggio
non e' definito.
Distinta dal recupero calore
generico (li' il calore recuperato
va a un uso generico, senza Brix,
senza acqua evaporata da succo,
senza multi-effetto, senza MVR),
da una caldaia generica (li' il
calore e' generico, senza succo,
senza Brix, senza evaporazione di
acqua di succo), dall'essiccazione
(pastificio e legno: li' si seccano
solidi, senza Brix, senza
evaporazione di acqua di succo,
senza multi-effetto, senza MVR),
dalla distillazione (li' si separano
miscele volatili, senza Brix, senza
succo di barbabietola, senza
multi-effetto per succo) e dalla
tab fonderia fusione (li' si fonde
ghisa, senza succo, senza Brix,
senza acqua evaporata, senza
multi-effetto, senza MVR).

Demo calcolata eseguendo demo_calcoli()
(e ricontrollata a mano, riga per
riga): succo in ingresso 50.000
t/anno, Brix ingresso 15 %,
Brix uscita 65 %, economia
baseline 1,0, 3 effetti, quota MVR
40 %, consumo MVR 30 kWh/t
evaporata, rendimento caldaia
0,90, prezzo gas 45 EUR/MWh,
prezzo elettrico 110 EUR/MWh,
O&M fisso 50.000 EUR/anno, CAPEX
800.000 EUR, fattore gas 0,20
tCO2/MWh e fattore elettrico 0,25
tCO2/MWh, WACC 5 %, vita 15 anni,
tolleranza 10 % del CAPEX.

- p_concentrato_t_anno = 11538.461538461539
- w_evaporata_t_anno = 38461.53846153846
- econ_me = 2.55
- v_base_t_anno = 38461.53846153846
- q_base_mwh_anno = 24113.247863247863
- gas_base_mwh_anno = 26792.497625830958
- c_base_eur_anno = 1205662.393162393
- co2_base_t_anno = 5358.499525166192
- w_mvr_t_anno = 15384.615384615385
- e_mvr_mwh_anno = 461.53846153846155
- w_me_t_anno = 23076.923076923078
- v_alt_t_anno = 9049.77375565611
- q_alt_mwh_anno = 5673.705379587734
- gas_alt_mwh_anno = 6304.117088430815
- c_alt_var_eur_anno = 334454.4997486174
- c_alt_eur_anno = 384454.4997486174
- risparmio_eur_anno = 821207.8934137756
- co2_alt_t_anno = 1376.2080330707786
- co2_evitata_t_anno = 3982.2914920954136
- crf = 0.09634228760924432
- quota_capex_eur_anno = 77073.83008739546
- lco_base_eur_t = 104.49074074074072
- lco_alt_eur_t = 39.999121919121116
- van = 7723857.111889645
- tir = 102.64841500840065
- payback = 1
- prezzo_pareggio_eur_mwh = 1889.2837690631804
- verdetto = 'CONVIENTE'

Scomposizione: P = 50.000 x 15 / 65
= 11.538,46 t/anno (solidi
conservati); W = 50.000 - 11.538,46
= 38.461,54 t/anno; econ_me =
3 x 0,85 = 2,55 kg/kg; V_base =
38.461,54 / 1,0 = 38.461,54 t/anno;
Q_base = 38.461,54 x 1000 x 2257 /
3.600.000 = 24.113,25 MWh/anno;
Gas_base = 24.113,25 / 0,90 =
26.792,50 MWh/anno; C_base =
26.792,50 x 45 = 1.205.662,39
EUR/anno; W_mvr = 0,40 x 38.461,54
= 15.384,62 t/anno; E_mvr =
15.384,62 x 30 / 1000 = 461,54
MWh/anno; W_me = 38.461,54 -
15.384,62 = 23.076,92 t/anno;
V_alt = 23.076,92 / 2,55 = 9.049,77
t/anno; Q_alt = 9.049,77 x 1000 x
2257 / 3.600.000 = 5.673,71
MWh/anno; Gas_alt = 5.673,71 / 0,90
= 6.304,12 MWh/anno; C_alt_var =
6.304,12 x 45 + 461,54 x 110 =
334.454,50 EUR/anno; C_alt =
334.454,50 + 50.000 = 384.454,50
EUR/anno; risparmio = 1.205.662,39
- 384.454,50 = 821.207,89 EUR/anno;
CO2 base = 26.792,50 x 0,20 =
5.358,50 t/anno; CO2 alt =
6.304,12 x 0,20 + 461,54 x 0,25 =
1.376,21 t/anno; CO2 evitata =
3.982,29 t/anno; CRF 0,05 x 1,05^15
/ (1,05^15 - 1) = 0.09634228760924432;
quota CAPEX 800.000 x 0,096342 =
77.073,83 EUR/anno; LCO base
1.205.662,39 / 11.538,46 = 104,49
EUR/t; LCO alt (77.073,83 + 50.000)
/ 11.538,46 + 334.454,50 / 11.538,46
= 40,00 EUR/t; flussi: anno 0
-800.000, anni 1-15 risparmio
821.207,89 (piatti); VAN -800.000 +
821.207,89 x 10,379658 (annuita'
15 anni al 5 %) = 7.723.857,11 EUR;
TIR 102,65 %; payback 1 anno (il
cumulato all'anno 1 e' 21.207,89
EUR, gia' strettamente positivo);
prezzo elettrico di pareggio
(1.205.662,39 - 6.304,12 x 45 -
50.000) / 461,54 = 1.889,28
EUR/MWh; verdetto CONVIENTE
perche' VAN > 0.
NOTA: il CRF entra solo nel LCO,
mai nei flussi: il CAPEX compare una
sola volta, all'anno 0.
NOTA 2: in questa tab il risparmio
nullo o negativo NON e' degenere: con
1 effetto e quota MVR 0 % il caso e'
calcolabile (valid=True, flussi
pieni), NON_CONVIENTE con VAN
-3.527.399,96 EUR, non
NON_CALCOLABILE.
NOTA 3: la CO2 evitata puo' essere
negativa in generale (segno libero,
NON monetizzata): con fattore
elettrico 2,00 tCO2/MWh la CO2
evitata scende a 3.174,60 t/anno
pur restando il caso calcolabile e
CONVIENTE.
NOTA 4: il prezzo elettrico di
pareggio come valore della funzione
pura puo' essere negativo: con O&M
fisso 5.000.000 il pareggio e'
-8.835,72 EUR/MWh circa, perche' il
solo costo gas residuo piu' O&M
fisso supera gia' il costo baseline
(ma il caso resta calcolabile in
questa tab, con VAN negativa).
NOTA 5: la quota MVR 100 % NON e'
degenere: il gas alternativo e'
zero, il risparmio e' 1.028.739,32
EUR/anno e la VAN 9.877.962,31 EUR,
e il pareggio e' 1.001,57 EUR/MWh.
NOTA 6: la quota MVR 0 % NON e'
degenere: E_mvr e' zero, il
risparmio e' 682.853,61 EUR/anno e
la VAN 6.287.786,98 EUR, e il
pareggio non e' definito.
NOTA 7: il payback usa il cumulato
STRETTAMENTE positivo: con CAPEX
nullo e risparmio positivo il payback
e' 1, non 0 (all'anno 0 il cumulato
e' zero, non positivo); con flussi
[-100, 50, 50] il payback e' None
(il cumulato all'anno 2 e' zero, non
positivo).
NOTA 8: il consumo MVR nullo NON e'
degenere: E_mvr e' zero, il risparmio
e' 871.977,12 EUR/anno e il pareggio
non e' definito.
NOTA 9: i valori demo sono stati
ricalcolati da zero: il ricalcolo
esatto (senza arrotondamenti
intermedi) da' P 11.538,46, W
38.461,54, Q_base 24.113,25, C_base
1.205.662,39, E_mvr 461,54, C_alt
384.454,50, risparmio 821.207,89,
CO2 evitata 3.982,29, quota CAPEX
77.073,83, LCO alt 39,9991 e
pareggio 1.889,28: i file usano i
valori esatti.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w767_helpers import (
    demo_calcoli,
    mh766_bx_in,
    mh766_bx_out,
    mh766_c_alt,
    mh766_c_alt_var,
    mh766_c_base,
    mh766_calcola,
    mh766_co2_alt,
    mh766_co2_base,
    mh766_co2_evitata,
    mh766_crf,
    mh766_csv,
    mh766_demo,
    mh766_e_mvr,
    mh766_econ_me,
    mh766_eta,
    mh766_flussi,
    mh766_gas,
    mh766_int_pos,
    mh766_lco_alt,
    mh766_lco_base,
    mh766_nneg,
    mh766_num,
    mh766_p_concentrato,
    mh766_payback,
    mh766_pct_0_100,
    mh766_pct_wacc,
    mh766_pos,
    mh766_prezzo_pareggio,
    mh766_q_vapore,
    mh766_quota_capex,
    mh766_risparmio,
    mh766_tir,
    mh766_valida,
    mh766_van,
    mh766_vapore_alt,
    mh766_vapore_base,
    mh766_verdetto,
    mh766_w_evaporata,
    mh766_w_me,
    mh766_w_mvr,
)


def _demo_kwargs():
    return dict(mh766_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh766_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh766_num(3, "x") == 3.0
    assert mh766_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh766_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh766_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh766_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh766_pos(0, "x")
    with pytest.raises(ValueError):
        mh766_pos(-1, "x")
    assert mh766_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh766_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh766_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh766_int_pos(0, "x")


def test_pct_0_100_limiti():
    assert mh766_pct_0_100(0, "x") == 0.0
    assert mh766_pct_0_100(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh766_pct_0_100(100.1, "x")
    with pytest.raises(ValueError):
        mh766_pct_0_100(-1, "x")


def test_pct_wacc_limiti():
    assert mh766_pct_wacc(0, "x") == 0.0
    assert mh766_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh766_pct_wacc(50.1, "x")


def test_eta_limiti():
    assert mh766_eta(1.0, "x") == 1.0
    assert mh766_eta(0.90, "x") == 0.90
    with pytest.raises(ValueError):
        mh766_eta(0, "x")
    with pytest.raises(ValueError):
        mh766_eta(-0.1, "x")
    with pytest.raises(ValueError):
        mh766_eta(1.01, "x")


def test_bx_limiti():
    assert mh766_bx_in(15.0, "x") == 15.0
    with pytest.raises(ValueError):
        mh766_bx_in(0, "x")
    with pytest.raises(ValueError):
        mh766_bx_in(-1, "x")
    assert mh766_bx_out(100, "x") == 100.0
    assert mh766_bx_out(65.0, "x") == 65.0
    with pytest.raises(ValueError):
        mh766_bx_out(0, "x")
    with pytest.raises(ValueError):
        mh766_bx_out(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_p_concentrato_e_w_evaporata():
    assert mh766_p_concentrato(50000, 15.0, 65.0) == pytest.approx(
        11538.461538461539)
    assert mh766_p_concentrato(50000, 65.0, 65.0) == pytest.approx(50000.0)
    assert mh766_p_concentrato(0, 15.0, 65.0) == 0.0
    assert mh766_w_evaporata(50000, 11538.461538461539) == pytest.approx(
        38461.53846153846)
    assert mh766_w_evaporata(50000, 50000.0) == 0.0
    with pytest.raises(ValueError):
        mh766_p_concentrato(50000, 15.0, 0)
    with pytest.raises(ValueError):
        mh766_p_concentrato(-1, 15.0, 65.0)


def test_econ_me():
    assert mh766_econ_me(3) == pytest.approx(2.55)
    assert mh766_econ_me(1) == pytest.approx(0.85)
    assert mh766_econ_me(5) == pytest.approx(4.25)
    with pytest.raises(ValueError):
        mh766_econ_me(0)
    with pytest.raises(ValueError):
        mh766_econ_me(2.5)


def test_vapore_base_q_vapore_gas():
    assert mh766_vapore_base(38461.53846153846, 1.0) == pytest.approx(
        38461.53846153846)
    assert mh766_vapore_base(38461.53846153846, 2.0) == pytest.approx(
        19230.76923076923)
    assert mh766_q_vapore(38461.53846153846) == pytest.approx(
        24113.247863247863)
    assert mh766_q_vapore(0) == 0.0
    assert mh766_gas(24113.247863247863, 0.90) == pytest.approx(
        26792.497625830958)
    assert mh766_gas(24113.247863247863, 1.0) == pytest.approx(
        24113.247863247863)
    with pytest.raises(ValueError):
        mh766_vapore_base(38461.53846153846, 0)
    with pytest.raises(ValueError):
        mh766_gas(24113.247863247863, 0)


def test_c_base_e_co2_base():
    assert mh766_c_base(26792.497625830958, 45) == pytest.approx(
        1205662.393162393)
    assert mh766_co2_base(26792.497625830958, 0.20) == pytest.approx(
        5358.499525166192)
    with pytest.raises(ValueError):
        mh766_c_base(26792.497625830958, -1)


def test_w_mvr_e_mvr_w_me():
    assert mh766_w_mvr(38461.53846153846, 40.0) == pytest.approx(
        15384.615384615385)
    assert mh766_w_mvr(38461.53846153846, 0) == 0.0
    assert mh766_w_mvr(38461.53846153846, 100) == pytest.approx(
        38461.53846153846)
    assert mh766_e_mvr(15384.615384615385, 30) == pytest.approx(
        461.53846153846155)
    assert mh766_e_mvr(15384.615384615385, 0) == 0.0
    assert mh766_w_me(38461.53846153846, 15384.615384615385) == \
        pytest.approx(23076.923076923078)
    assert mh766_w_me(38461.53846153846, 38461.53846153846) == 0.0
    with pytest.raises(ValueError):
        mh766_w_mvr(38461.53846153846, 100.1)
    with pytest.raises(ValueError):
        mh766_e_mvr(15384.615384615385, -1)


def test_vapore_alt():
    assert mh766_vapore_alt(23076.923076923078, 2.55) == pytest.approx(
        9049.77375565611)
    assert mh766_vapore_alt(0.0, 2.55) == 0.0
    with pytest.raises(ValueError):
        mh766_vapore_alt(23076.923076923078, 0)


def test_c_alt_var_e_c_alt():
    assert mh766_c_alt_var(6304.117088430815, 45,
                           461.53846153846155, 110) == pytest.approx(
        334454.4997486174)
    assert mh766_c_alt_var(0.0, 45, 0.0, 110) == 0.0
    assert mh766_c_alt(334454.4997486174, 50000) == pytest.approx(
        384454.4997486174)
    assert mh766_c_alt(334454.4997486174, 0) == pytest.approx(
        334454.4997486174)
    with pytest.raises(ValueError):
        mh766_c_alt_var(6304.117088430815, 45,
                        461.53846153846155, -1)


def test_risparmio_segno():
    assert mh766_risparmio(1205662.393162393, 384454.4997486174) == \
        pytest.approx(821207.8934137756)
    assert mh766_risparmio(1205662.393162393, 1205662.393162393) == 0.0
    assert mh766_risparmio(1205662.393162393, 1468426.3448969328) == \
        pytest.approx(-262763.9517345398)


def test_co2_alt_e_evitata_segno_libero():
    assert mh766_co2_alt(6304.117088430815, 0.20,
                         461.53846153846155, 0.25) == pytest.approx(
        1376.2080330707786)
    assert mh766_co2_evitata(5358.499525166192,
                             1376.2080330707786) == pytest.approx(
        3982.2914920954136)
    assert mh766_co2_evitata(5358.499525166192,
                             2183.900340763086) == pytest.approx(
        3174.599184403106)


# ---------------------------------------------------------------- finanza base
def test_crf():
    assert mh766_crf(5.0, 15) == pytest.approx(0.09634228760924432)
    assert mh766_crf(0, 15) == pytest.approx(1.0 / 15.0)
    assert mh766_crf(5.0, 1) == pytest.approx(1.05)
    assert mh766_crf(5.0, 10) == pytest.approx(0.12950457496545661)


def test_quota_capex_e_lco():
    assert mh766_quota_capex(800000, 0.09634228760924432) == pytest.approx(
        77073.83008739546)
    assert mh766_lco_base(1205662.393162393, 11538.461538461539) == \
        pytest.approx(104.49074074074072)
    assert mh766_lco_base(1205662.393162393, 0) is None
    assert mh766_lco_alt(800000, 0.09634228760924432, 50000,
                         334454.4997486174,
                         11538.461538461539) == pytest.approx(
        39.999121919121116)
    assert mh766_lco_alt(800000, 0.09634228760924432, 50000,
                         334454.4997486174, 0) is None
    assert mh766_lco_alt(0, 0.09634228760924432, 50000,
                         334454.4997486174,
                         11538.461538461539) == pytest.approx(
        33.31938997821351)


def test_prezzo_pareggio_formula_negativo_e_none():
    assert mh766_prezzo_pareggio(1205662.393162393, 6304.117088430815,
                                 45, 50000,
                                 461.53846153846155) == pytest.approx(
        1889.2837690631804)
    assert mh766_prezzo_pareggio(1205662.393162393, 6304.117088430815,
                                 45, 50000, 0.0) is None
    assert mh766_prezzo_pareggio(1205662.393162393, 6304.117088430815,
                                 45, 50000, None) is None


def test_prezzo_pareggio_negativo_solo_funzione_pura():
    """Il pareggio negativo esiste come valore della
    funzione pura: con O&M fisso 5.000.000 il numeratore e'
    negativo; in questa tab quel caso resta comunque
    calcolabile (VAN negativa)."""
    bc = demo_calcoli()
    assert mh766_prezzo_pareggio(bc["c_base_eur_anno"],
                                 bc["gas_alt_mwh_anno"], 45, 5000000,
                                 bc["e_mvr_mwh_anno"]) == pytest.approx(
        -8835.71623093682, abs=1e-6)
    assert bc["prezzo_pareggio_eur_mwh"] > 0.0


def test_flussi_lunghezza_e_primo():
    fl = mh766_flussi(800000, 821207.8934137756, 15)
    assert len(fl) == 16
    assert fl[0] == -800000
    assert all(f == 821207.8934137756 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = demo_calcoli()
    assert bc["van"] == pytest.approx(7723857.111889645)
    assert mh766_van([-800000] + [821207.8934137756] * 15,
                     0) == pytest.approx(11518118.401206631)
    assert mh766_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = demo_calcoli()
    assert bc["tir"] == pytest.approx(102.64841500840065)
    assert mh766_tir([-800000] + [821207.8934137756] * 15) == pytest.approx(
        1.0264841500840065)
    tir = mh766_tir([-800000] + [821207.8934137756] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-800000] + [821207.8934137756] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_stretto():
    """Payback STRETTAMENTE positivo: il cumulato nullo
    non basta."""
    assert mh766_payback([-800000] + [821207.8934137756] * 15) == 1
    assert mh766_payback([-800000] + [-1000.0] * 15) is None
    assert mh766_payback([0] + [821207.8934137756] * 15) == 1
    assert mh766_payback([-100] + [50] * 2) is None
    assert mh766_payback([-100] + [50] * 3) == 3


def test_verdetto():
    assert mh766_verdetto(100.0, 800000, 10.0) == "CONVIENTE"
    assert mh766_verdetto(-70000.0, 800000, 10.0) == "MARGINALE"
    assert mh766_verdetto(-80000.0, 800000, 10.0) == "MARGINALE"
    assert mh766_verdetto(-80000.01, 800000, 10.0) == "NON_CONVIENTE"
    assert mh766_verdetto(float("nan"), 800000, 10.0) == "NON_CALCOLABILE"
    assert mh766_verdetto(0.0, 0, 10.0) == "MARGINALE"


def test_valida_demo_ok():
    v = mh766_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("f_t_anno", "50000"),
                       ("f_t_anno", float("nan")),
                       ("f_t_anno", float("inf")),
                       ("f_t_anno", True),
                       ("prezzo_el_eur_mwh", None)):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh766_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("f_t_anno", 0),
                          ("f_t_anno", -1),
                          ("bx_in_pct", 0),
                          ("bx_in_pct", -1),
                          ("bx_out_pct", 0),
                          ("bx_out_pct", 100.1),
                          ("bx_out_pct", 15.0),
                          ("bx_out_pct", 10.0),
                          ("econ_base", 0),
                          ("econ_base", -0.5),
                          ("n_effetti", 0),
                          ("n_effetti", 2.5),
                          ("q_mvr_pct", -1),
                          ("q_mvr_pct", 100.1),
                          ("consumo_mvr_kwh_per_t", -1),
                          ("eta_caldaia", 0),
                          ("eta_caldaia", 1.01),
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
        assert mh766_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"q_mvr_pct": 0,
              "consumo_mvr_kwh_per_t": 0,
              "prezzo_gas_eur_mwh": 0,
              "prezzo_el_eur_mwh": 0, "om_fisso_eur_anno": 0,
              "capex_eur": 0, "f_gas_t_per_mwh": 0,
              "f_el_t_per_mwh": 0, "wacc_pct": 0,
              "tolleranza_pct": 0, "eta_caldaia": 1.0,
              "econ_base": 2.0, "n_effetti": 1,
              "bx_in_pct": 10.0, "bx_out_pct": 100.0})
    assert mh766_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["q_mvr_pct"] = 100
    assert mh766_valida(**d)["valido"] is True


def test_valida_non_controlla_risparmio_calcola_neppure():
    """La validazione input NON controlla il risparmio
    (e' un esito, non un range) e in questa tab
    nemmeno mh766_calcola lo controlla: con 1 effetto
    e quota MVR 0 % il caso resta CALCOLABILE."""
    d = _demo_kwargs()
    d["n_effetti"] = 1
    d["q_mvr_pct"] = 0
    assert mh766_valida(**d)["valido"] is True
    bc = _variante(n_effetti=1, q_mvr_pct=0)
    assert bc["valid"] is True
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["flussi"]
    assert bc["tir"] is None
    assert bc["payback"] is None


def test_demo_dict():
    d = mh766_demo()
    assert d["f_t_anno"] == 50000
    assert d["bx_in_pct"] == 15.0
    assert d["bx_out_pct"] == 65.0
    assert d["econ_base"] == 1.0
    assert d["n_effetti"] == 3
    assert d["q_mvr_pct"] == 40.0
    assert d["consumo_mvr_kwh_per_t"] == 30
    assert d["eta_caldaia"] == 0.90
    assert d["prezzo_gas_eur_mwh"] == 45
    assert d["prezzo_el_eur_mwh"] == 110
    assert d["om_fisso_eur_anno"] == 50000
    assert d["capex_eur"] == 800000
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
        "p_concentrato_t_anno": 11538.461538461539,
        "w_evaporata_t_anno": 38461.53846153846,
        "econ_me": 2.55,
        "v_base_t_anno": 38461.53846153846,
        "q_base_mwh_anno": 24113.247863247863,
        "gas_base_mwh_anno": 26792.497625830958,
        "c_base_eur_anno": 1205662.393162393,
        "co2_base_t_anno": 5358.499525166192,
        "w_mvr_t_anno": 15384.615384615385,
        "e_mvr_mwh_anno": 461.53846153846155,
        "w_me_t_anno": 23076.923076923078,
        "v_alt_t_anno": 9049.77375565611,
        "q_alt_mwh_anno": 5673.705379587734,
        "gas_alt_mwh_anno": 6304.117088430815,
        "c_alt_var_eur_anno": 334454.4997486174,
        "c_alt_eur_anno": 384454.4997486174,
        "risparmio_eur_anno": 821207.8934137756,
        "co2_alt_t_anno": 1376.2080330707786,
        "co2_evitata_t_anno": 3982.2914920954136,
        "crf": 0.09634228760924432,
        "quota_capex_eur_anno": 77073.83008739546,
        "lco_base_eur_t": 104.49074074074072,
        "lco_alt_eur_t": 39.999121919121116,
        "van": 7723857.111889645,
        "tir": 102.64841500840065,
        "prezzo_pareggio_eur_mwh": 1889.2837690631804,
    }
    for chiave, atteso in attesi.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert abs(got - atteso) / abs(atteso) < 1e-9, chiave
    assert bc["payback"] == 1
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_demo_calcoli_fisica():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["p_concentrato_t_anno"] == pytest.approx(11538.461538461539)
    assert bc["w_evaporata_t_anno"] == pytest.approx(38461.53846153846)
    assert bc["econ_me"] == pytest.approx(2.55)
    assert bc["v_base_t_anno"] == pytest.approx(38461.53846153846)
    assert bc["q_base_mwh_anno"] == pytest.approx(24113.247863247863)
    assert bc["gas_base_mwh_anno"] == pytest.approx(26792.497625830958)
    assert bc["w_mvr_t_anno"] == pytest.approx(15384.615384615385)
    assert bc["e_mvr_mwh_anno"] == pytest.approx(461.53846153846155)
    assert bc["w_me_t_anno"] == pytest.approx(23076.923076923078)
    assert bc["v_alt_t_anno"] == pytest.approx(9049.77375565611)
    assert bc["q_alt_mwh_anno"] == pytest.approx(5673.705379587734)
    assert bc["gas_alt_mwh_anno"] == pytest.approx(6304.117088430815)
    assert bc["co2_evitata_t_anno"] == pytest.approx(3982.2914920954136)


def test_demo_calcoli_economia():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(1205662.393162393)
    assert bc["c_alt_var_eur_anno"] == pytest.approx(334454.4997486174)
    assert bc["c_alt_eur_anno"] == pytest.approx(384454.4997486174)
    assert bc["risparmio_eur_anno"] == pytest.approx(821207.8934137756)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(1889.2837690631804)


def test_demo_calcoli_finanza():
    bc = demo_calcoli()
    assert bc["crf"] == pytest.approx(0.09634228760924432)
    assert bc["quota_capex_eur_anno"] == pytest.approx(77073.83008739546)
    assert bc["lco_base_eur_t"] == pytest.approx(104.49074074074072)
    assert bc["lco_alt_eur_t"] == pytest.approx(39.999121919121116)
    assert bc["van"] == pytest.approx(7723857.111889645)
    assert bc["tir"] == pytest.approx(102.64841500840065)
    assert bc["payback"] == 1
    assert bc["verdetto"] == "CONVIENTE"


def test_demo_flussi_e_cumulato():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -800000
    assert len(bc["flussi"]) == 16
    assert all(f == 821207.8934137756 for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -800000
    assert righe.iloc[1]["Cumulato (EUR)"] == pytest.approx(21207.8934137756)
    assert righe.iloc[2]["Cumulato (EUR)"] == pytest.approx(842415.7868275512)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(11518118.401206631)
    assert righe.iloc[15]["Flusso (EUR/anno)"] == 821207.8934137756


def test_demo_tabella_righe():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Succo concentrato (t/anno)"] == pytest.approx(
        11538.461538461539)
    assert mappa["Acqua evaporata (t/anno)"] == pytest.approx(
        38461.53846153846)
    assert mappa["Economia multi-effetto (kg/kg)"] == pytest.approx(2.55)
    assert mappa["Succo in ingresso (t/anno)"] == pytest.approx(50000.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(
        384454.4997486174)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(821207.8934137756)
    assert mappa["Payback (anni)"] == 1
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Prezzo elettrico di pareggio (EUR/MWh)"] == pytest.approx(
        1889.2837690631804)


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
        bc["p_concentrato_t_anno"] + bc["c_alt_var_eur_anno"] / \
        bc["p_concentrato_t_anno"] == pytest.approx(bc["lco_alt_eur_t"])
    assert bc["c_base_eur_anno"] - bc["gas_alt_mwh_anno"] * \
        bc["prezzo_gas_eur_mwh"] - bc["om_fisso_eur_anno"] == \
        pytest.approx(bc["prezzo_pareggio_eur_mwh"] *
                      bc["e_mvr_mwh_anno"])
    assert bc["w_mvr_t_anno"] + bc["w_me_t_anno"] == \
        pytest.approx(bc["w_evaporata_t_anno"])
    assert bc["f_t_anno"] - bc["p_concentrato_t_anno"] == \
        pytest.approx(bc["w_evaporata_t_anno"])
    assert bc["f_t_anno"] * bc["bx_in_pct"] / \
        bc["bx_out_pct"] == pytest.approx(bc["p_concentrato_t_anno"])
    assert bc["v_base_t_anno"] * 1000.0 * 2257.0 / \
        3600000.0 == pytest.approx(bc["q_base_mwh_anno"])
    assert bc["v_alt_t_anno"] * 1000.0 * 2257.0 / \
        3600000.0 == pytest.approx(bc["q_alt_mwh_anno"])


def test_demo_crf_solo_nel_lco_non_nei_flussi():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -bc["capex_eur"]
    assert all(f == bc["risparmio_eur_anno"] for f in bc["flussi"][1:])
    assert bc["crf"] not in bc["flussi"]
    assert bc["quota_capex_eur_anno"] not in bc["flussi"]
    van_da_flussi = mh766_van(bc["flussi"], bc["wacc_pct"])
    assert van_da_flussi == pytest.approx(bc["van"])
    assert bc["lco_alt_eur_t"] == pytest.approx(
        (bc["capex_eur"] * bc["crf"] + bc["om_fisso_eur_anno"]) /
        bc["p_concentrato_t_anno"] + bc["c_alt_var_eur_anno"] /
        bc["p_concentrato_t_anno"])


def test_demo_contro_riconteggio_indipendente():
    f, bi, bo = 50000, 15.0, 65.0
    eb, n, q, cons = 1.0, 3, 40.0, 30
    eta, pg, pel, om, cx = 0.90, 45, 110, 50000, 800000
    fg, fe, wacc, vita = 0.20, 0.25, 5.0, 15
    p = f * bi / bo
    w = f - p
    eme = n * 0.85
    vb = w / eb
    qb = vb * 1000 * 2257 / 3600000.0
    gb = qb / eta
    cb = gb * pg
    wm = q / 100 * w
    em = wm * cons / 1000.0
    wme = w - wm
    va = wme / eme
    qa = va * 1000 * 2257 / 3600000.0
    ga = qa / eta
    cav = ga * pg + em * pel
    ca = cav + om
    risp = cb - ca
    co2b = gb * fg
    co2a = ga * fg + em * fe
    r = wacc / 100.0
    crf = r * (1 + r) ** vita / ((1 + r) ** vita - 1)
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    bc = demo_calcoli()
    assert bc["p_concentrato_t_anno"] == pytest.approx(p)
    assert bc["w_evaporata_t_anno"] == pytest.approx(w)
    assert bc["econ_me"] == pytest.approx(eme)
    assert bc["v_base_t_anno"] == pytest.approx(vb)
    assert bc["q_base_mwh_anno"] == pytest.approx(qb)
    assert bc["gas_base_mwh_anno"] == pytest.approx(gb)
    assert bc["c_base_eur_anno"] == pytest.approx(cb)
    assert bc["w_mvr_t_anno"] == pytest.approx(wm)
    assert bc["e_mvr_mwh_anno"] == pytest.approx(em)
    assert bc["w_me_t_anno"] == pytest.approx(wme)
    assert bc["v_alt_t_anno"] == pytest.approx(va)
    assert bc["q_alt_mwh_anno"] == pytest.approx(qa)
    assert bc["gas_alt_mwh_anno"] == pytest.approx(ga)
    assert bc["c_alt_var_eur_anno"] == pytest.approx(cav)
    assert bc["c_alt_eur_anno"] == pytest.approx(ca)
    assert bc["risparmio_eur_anno"] == pytest.approx(risp)
    assert bc["co2_base_t_anno"] == pytest.approx(co2b)
    assert bc["co2_alt_t_anno"] == pytest.approx(co2a)
    assert bc["crf"] == pytest.approx(crf)
    assert bc["van"] == pytest.approx(van)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(
        (cb - ga * pg - om) / em)


# ---------------------------------------------------------------- varianti
def test_demo_conviente():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] > 0.0
    assert bc["payback"] == 1
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_quota_mvr_zero_calcolabile_pareggio_none():
    """Sensibilita' richiesta dal brief: quota MVR 0 %."""
    bc = _variante(q_mvr_pct=0)
    assert bc["valid"] is True
    assert bc["w_mvr_t_anno"] == 0.0
    assert bc["e_mvr_mwh_anno"] == 0.0
    assert bc["gas_alt_mwh_anno"] == pytest.approx(10506.861814051357)
    assert bc["risparmio_eur_anno"] == pytest.approx(682853.611530082)
    assert bc["van"] == pytest.approx(6287786.977818862)
    assert bc["payback"] == 2
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["lco_alt_eur_t"] == pytest.approx(51.98982634904122)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_quota_mvr_cento_calcolabile_gas_zero():
    """Sensibilita' richiesta dal brief: quota MVR 100 %."""
    bc = _variante(q_mvr_pct=100)
    assert bc["valid"] is True
    assert bc["w_me_t_anno"] == 0.0
    assert bc["gas_alt_mwh_anno"] == 0.0
    assert bc["e_mvr_mwh_anno"] == pytest.approx(1153.8461538461538)
    assert bc["risparmio_eur_anno"] == pytest.approx(1028739.316239316)
    assert bc["van"] == pytest.approx(9877962.312995821)
    assert bc["payback"] == 1
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(1001.574074074074)
    assert bc["lco_alt_eur_t"] == pytest.approx(22.013065274240937)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_un_effetto_senza_mvr_calcolabile_non_conviente():
    """Sensibilita' richiesta dal brief: 1 effetto, quota
    MVR 0 %. In questa tab il risparmio negativo e'
    CALCOLABILE."""
    bc = _variante(n_effetti=1, q_mvr_pct=0)
    assert bc["valid"] is True
    assert bc["econ_me"] == pytest.approx(0.85)
    assert bc["v_alt_t_anno"] == pytest.approx(45248.86877828054)
    assert bc["gas_alt_mwh_anno"] == pytest.approx(31520.585442154064)
    assert bc["risparmio_eur_anno"] == pytest.approx(-262763.9517345398)
    assert bc["van"] == pytest.approx(-3527399.9637655127)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["lco_alt_eur_t"] == pytest.approx(133.94334849864177)
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["flussi"]


def test_variante_capex_alto_marginale():
    bc = _variante(capex_eur=8600000)
    assert bc["risparmio_eur_anno"] == pytest.approx(821207.8934137756)
    assert bc["van"] == pytest.approx(-76142.88811035472)
    assert bc["van"] < 0.0
    assert abs(bc["van"]) <= 0.10 * 8600000
    assert bc["payback"] == 11
    assert bc["lco_alt_eur_t"] == pytest.approx(105.12650834297028)
    assert bc["verdetto"] == "MARGINALE"
    assert bc["valid"] is True


def test_variante_capex_altissimo_non_conviente():
    bc = _variante(capex_eur=20000000)
    assert bc["van"] == pytest.approx(-11476142.888110355)
    assert abs(bc["van"]) > 0.10 * 20000000
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_variante_consumo_mvr_zero_pareggio_none():
    bc = _variante(consumo_mvr_kwh_per_t=0)
    assert bc["valid"] is True
    assert bc["e_mvr_mwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(871977.1241830064)
    assert bc["van"] == pytest.approx(8250824.366135737)
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_fattore_el_alto_co2_evitata_minore():
    bc = _variante(f_el_t_per_mwh=2.0)
    assert bc["co2_alt_t_anno"] == pytest.approx(2183.900340763086)
    assert bc["co2_evitata_t_anno"] == pytest.approx(3174.599184403106)
    assert bc["van"] == pytest.approx(7723857.111889645)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero():
    bc = _variante(wacc_pct=0)
    assert bc["crf"] == pytest.approx(1.0 / 15.0)
    assert bc["quota_capex_eur_anno"] == pytest.approx(53333.333333333336)
    assert bc["van"] == pytest.approx(11518118.401206631)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_zero_payback_uno_tir_none():
    """Payback stretto: con CAPEX nullo il payback e' 1,
    non 0 (all'anno 0 il cumulato e' zero)."""
    bc = _variante(capex_eur=0)
    assert bc["capex_eur"] == 0
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 1
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(8523857.111889645)
    assert bc["lco_alt_eur_t"] == pytest.approx(33.31938997821351)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_vita_dieci():
    bc = _variante(vita_anni=10)
    assert len(bc["flussi"]) == 11
    assert bc["crf"] == pytest.approx(0.12950457496545661)
    assert bc["van"] == pytest.approx(5541149.674695428)
    assert bc["payback"] == 1
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_fattori_zero_calcolabile():
    bc = _variante(f_gas_t_per_mwh=0, f_el_t_per_mwh=0)
    assert bc["valid"] is True
    assert bc["co2_base_t_anno"] == 0.0
    assert bc["co2_alt_t_anno"] == 0.0
    assert bc["co2_evitata_t_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(821207.8934137756)


# ---------------------------------------------------------------- degenere
def test_degenere_succo_zero():
    bc = _variante(f_t_anno=0)
    assert bc["valid"] is False
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"] == []
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert bc["lco_base_eur_t"] is None
    assert bc["lco_alt_eur_t"] is None
    assert bc["errore"]


def test_degenere_brix_eta_econ_effetti_vita():
    for kw in ({"bx_in_pct": 0}, {"bx_in_pct": -1},
               {"bx_out_pct": 15.0}, {"bx_out_pct": 10.0},
               {"bx_out_pct": 100.1}, {"bx_out_pct": 0},
               {"eta_caldaia": 0}, {"eta_caldaia": 1.01},
               {"econ_base": 0}, {"econ_base": -0.5},
               {"n_effetti": 0}, {"n_effetti": 2.5},
               {"consumo_mvr_kwh_per_t": -1},
               {"q_mvr_pct": -1}, {"q_mvr_pct": 100.1},
               {"f_t_anno": 0}, {"f_t_anno": -1},
               {"vita_anni": 0}, {"vita_anni": 2.5}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_wacc_tolleranza_prezzi_negativi():
    for kw in ({"wacc_pct": -1}, {"wacc_pct": 60},
               {"tolleranza_pct": -1}, {"tolleranza_pct": 101},
               {"prezzo_gas_eur_mwh": -1},
               {"prezzo_el_eur_mwh": -1},
               {"om_fisso_eur_anno": -100},
               {"capex_eur": -1},
               {"f_gas_t_per_mwh": -0.10},
               {"f_el_t_per_mwh": -0.10}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_stringa_nan_inf():
    for kw in ({"f_t_anno": "50000"},
               {"f_t_anno": float("nan")},
               {"prezzo_el_eur_mwh": float("inf")},
               {"capex_eur": True}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_risparmio_negativo_non_degenere():
    """Differenza chiave: risparmio negativo resta
    calcolabile, con flussi pieni e VAN negativa."""
    for kw in ({"n_effetti": 1, "q_mvr_pct": 0},
               {"n_effetti": 1, "q_mvr_pct": 0,
                "prezzo_gas_eur_mwh": 10},
               {"capex_eur": 20000000}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] < 0.0 or bc["van"] < 0.0
        assert bc["verdetto"] in ("NON_CONVIENTE", "MARGINALE")
        assert bc["flussi"]


def test_degenere_neutro_campi():
    bc = _variante(f_t_anno=0)
    assert bc["w_evaporata_t_anno"] == 0.0
    assert bc["gas_base_mwh_anno"] == 0.0
    assert bc["c_base_eur_anno"] == 0.0
    assert bc["c_alt_eur_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == 0.0
    assert bc["van"] == 0.0
    assert list(bc["df_flussi"].columns) == [
        "Anno", "Flusso (EUR/anno)", "Cumulato (EUR)"]
    assert list(bc["df_tabella"].columns) == ["Voce", "Valore"]


def test_pareggio_none_quando_e_mvr_zero():
    assert mh766_prezzo_pareggio(1205662.393162393, 6304.117088430815,
                                 45, 50000, 0.0) is None
    assert mh766_prezzo_pareggio(1205662.393162393, 6304.117088430815,
                                 45, 50000, None) is None
    assert mh766_lco_base(1205662.393162393, 0) is None
    bc = _variante(q_mvr_pct=0)
    assert bc["prezzo_pareggio_eur_mwh"] is None
    bc = _variante(consumo_mvr_kwh_per_t=0)
    assert bc["prezzo_pareggio_eur_mwh"] is None


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = demo_calcoli()
    testo = mh766_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert "w_evaporata_t_anno;38461.53846153846" in testo
    assert "q_base_mwh_anno;24113.247863247863" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "prezzo_pareggio_eur_mwh" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = demo_calcoli()
    testo = mh766_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"quota_capex_eur_anno;{bc['quota_capex_eur_anno']}" in testo
    assert f"w_evaporata_t_anno;{bc['w_evaporata_t_anno']}" in testo


def test_csv_degenere_solo_zeri():
    bc = _variante(f_t_anno=0)
    testo = mh766_csv(bc, _demo_kwargs())
    assert "van_eur;0.0" in testo
    assert "w_evaporata_t_anno;0.0" in testo
    assert "verdetto;NON_CALCOLABILE" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = demo_calcoli()
    testo = mh766_csv(bc, _demo_kwargs())
    for chiave in _demo_kwargs():
        assert f"{chiave};" in testo


def test_calcola_non_sollevela_per_input_numerici():
    bc = _variante(f_gas_t_per_mwh=0, f_el_t_per_mwh=0)
    assert bc["valid"] is True
    assert bc["co2_base_t_anno"] == 0.0
    assert bc["co2_alt_t_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(821207.8934137756)


def test_monotonia_prezzo_el():
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(prezzo_el_eur_mwh=120)["risparmio_eur_anno"]
    basso = _variante(prezzo_el_eur_mwh=100)["risparmio_eur_anno"]
    assert basso > base > alto
    assert basso - base == pytest.approx(4615.384615384615)
    assert base - alto == pytest.approx(4615.384615384615)


def test_monotonia_quota_mvr():
    base = demo_calcoli()["risparmio_eur_anno"]
    alta = _variante(q_mvr_pct=50)["risparmio_eur_anno"]
    bassa = _variante(q_mvr_pct=30)["risparmio_eur_anno"]
    assert alta > base > bassa


def test_demo_deterministica_due_chiamate():
    a = demo_calcoli()
    b = demo_calcoli()
    assert a["van"] == b["van"]
    assert a["flussi"] == b["flussi"]
    assert a["tir"] == b["tir"]


def test_demo_chiavi_attese():
    assert set(mh766_demo().keys()) == {
        "f_t_anno",
        "bx_in_pct", "bx_out_pct",
        "econ_base", "n_effetti",
        "q_mvr_pct", "consumo_mvr_kwh_per_t",
        "eta_caldaia",
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
    return ["mh" + "76" + "5", "st" + "76" + "5",
            "tab" + "76" + "5", "w" + "76" + "6_",
            "mh" + "76" + "4", "st" + "76" + "4",
            "tab" + "76" + "4", "w" + "76" + "5_"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w767_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w767_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab766:")


def test_registry_chain_tail_and_count():
    """Registry della nuova tab: il frammento UI apre la tab
    numero 766 (la coda della catena termina con la nuova tab
    e il conteggio atteso delle tab e' 766)."""
    src = _leggi("w767_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 766
    assert src.count("with tab766:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w767_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w767_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st766_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert "key=f" not in src and 'key = f' not in src
    assert "st.stop()" in src
    # guard degenere prima di KPI / grafico / tabella / CSV
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w767_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def766[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w767_ui.py")
        usate = set(re.findall(r'_def766\["([^"]+)"\]', src))
        assert usate
        assert usate <= set(mh766_demo().keys())


def test_ui_chiavi_demo_coerenti():
    """Ogni _def766[...] letto dalla UI esiste nel dict demo:
    sweep anti-KeyError a render (lezione dello sweep chiavi demo vs UI)."""
    src = _leggi("w767_ui.py")
    usate = set(re.findall(r'_def766\["([^"]+)"\]', src))
    assert usate
    assert usate <= set(mh766_demo().keys())


def test_ui_riferisce_solo_helper_nuovi():
    src = _leggi("w767_ui.py")
    usati = set(re.findall(r'\b(mh\d+_\w+)\b', src))
    assert usati
    assert all(u.startswith("mh766_") for u in usati)


@pytest.mark.parametrize("wacc,vita,atteso", [
    (5.0, 15, 0.09634228760924432),
    (0, 15, 1.0 / 15.0),
    (10.0, 10, 0.16274539488251152),
    (5.0, 1, 1.05),
    (50.0, 5, 0.5758293838862559),
])
def test_crf_parametrizzato(wacc, vita, atteso):
    assert mh766_crf(wacc, vita) == pytest.approx(atteso)


@pytest.mark.parametrize("campo,valore", [
    ("f_t_anno", 0), ("f_t_anno", -3),
    ("bx_in_pct", 0), ("bx_in_pct", -1),
    ("bx_out_pct", 0), ("bx_out_pct", 100.1),
    ("bx_out_pct", 15.0), ("bx_out_pct", 10.0),
    ("econ_base", 0), ("econ_base", -0.5),
    ("n_effetti", 0), ("n_effetti", 2.5),
    ("q_mvr_pct", -1), ("q_mvr_pct", 100.1),
    ("consumo_mvr_kwh_per_t", -1),
    ("eta_caldaia", 0), ("eta_caldaia", 1.01),
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
    assert mh766_valida(**d)["valido"] is False


def test_df_tabella_valori_demo_selezionati():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Succo in ingresso (t/anno)"] == 50000.0
    assert mappa["Acqua evaporata (t/anno)"] == pytest.approx(38461.53846153846)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(821207.8934137756)
    assert mappa["Verdetto"] == "CONVIENTE"


def test_lco_alt_minore_di_lco_base_demo():
    bc = demo_calcoli()
    assert bc["lco_alt_eur_t"] < bc["lco_base_eur_t"]
    assert bc["lco_base_eur_t"] - bc["lco_alt_eur_t"] == pytest.approx(
        64.49161882161961)
