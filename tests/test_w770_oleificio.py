"""Test tab770 "Oleificio: la sansa
che avanza alimenta un
cogeneratore a biomassa e batte
rete + caldaia a gas?"

Nuova tab tab770 (oleificio,
file di lavoro w771).
Business case deterministico
di un oleificio: sansa prodotta
M_sansa = P x resa_sansa t/anno;
energia biomassa E_biomassa =
M_sansa x PCI MWh/anno; elettricita'
prodotta E_el = E_biomassa x
eta_el MWh/anno; calore prodotto
Q_th = E_biomassa x eta_th
MWh/anno (eta come frazioni);
domanda elettrica E_dem = P x
e_el_spec / 1000 MWh/anno
(e_el_spec in kWh/t olive);
domanda termica Q_dem = P x
q_th_spec / 1000 MWh/anno
(q_th_spec in kWh/t olive);
autoconsumo elettrico E_auto =
min(E_el, E_dem) MWh/anno;
vendita E_vend = E_el - E_auto
MWh/anno; calore autoconsumato
Q_auto = min(Q_th, Q_dem)
MWh/anno; costo base C_base =
E_dem x p_el + (Q_dem /
eta_caldaia) x p_gas EUR/anno;
costo alternativo C_alt = O&M
annuo + M_sansa x costo tratt
sansa + (E_dem - E_auto) x p_el
+ ((Q_dem - Q_auto) /
eta_caldaia) x p_gas - E_vend x
p_vendita EUR/anno; risparmio =
C_base - C_alt EUR/anno; CO2 base
= E_dem x f_el + (Q_dem /
eta_caldaia) x f_gas t/anno;
CO2 alt = - E_vend x f_el t/anno
(biomassa conteggiata a zero per
convenzione biogenica dichiarata);
CO2 evitata = CO2 base - CO2 alt,
segno libero (positiva nel caso
demo), NON monetizzata; fattore
di emissione in tCO2/MWh,
numericamente uguale a kg/kWh
(1 kg/kWh = 1 t/MWh); LCO base =
C_base / P; LCO alt = C_alt / P
(il CAPEX NON entra nel LCO di
questa tab: entra nei flussi,
nella VAN, nella TIR e nel
payback; il LCO alternativo puo'
essere negativo quando i ricavi
di vendita superano i costi
operativi); prezzo elettricita'
di pareggio NON definito in
questa tab (l'alternativa vende
anche elettricita': il pareggio
su p_el non e' univoco) -> None
sempre; prezzo vendita di
pareggio = (O&M + M_sansa x costo
tratt + (E_dem - E_auto) x p_el
+ ((Q_dem - Q_auto) /
eta_caldaia) x p_gas - C_base) /
E_vend, None se E_vend <= 0, puo'
essere negativo (in quel caso
l'impianto conviene anche a
prezzo di vendita zero); flussi
[-CAPEX, risparmio x vita]; VAN,
TIR, payback (primo anno con
cumulato >= 0, regola >= del
brief: con CAPEX nullo il payback
e' 0, con divisione esatta CAPEX
/ risparmio il payback e' l'anno
della divisione esatta).
Verdetto: CONVIENTE se VAN > 0,
MARGINALE se VAN < 0 e |VAN| <=
tolleranza % del CAPEX, altrimenti
NON_CONVIENTE; NON_CALCOLABILE e'
il verdetto del caso degenere
(VAN None: nessun calcolo
eseguibile). Regime degenere
SOLLEVA ValueError negli helper
(produzione <= 0, resa sansa
<= 0, PCI <= 0, eta elettrica
<= 0, eta termica < 0, somma dei
rendimenti > 1, eta caldaia
<= 0 o > 1, elettricita' specifica
< 0, calore specifico < 0, prezzi
< 0, costo trattamento sansa < 0,
O&M < 0, CAPEX < 0, fattori < 0,
WACC < 0 o sopra 50 %, vita <= 0
o non intera, tolleranza fuori
[0, 100] %, input non numerici o
non finiti); la UI lo intercetta
PRIMA di KPI, grafico, tabella e
CSV con st.stop(). In questa tab
il risparmio nullo o negativo NON
e' degenere: resta calcolabile e
porta a VAN negativa
(NON_CONVIENTE o MARGINALE). La
CO2 evitata negativa NON e'
degenere: e' un numero, non una
guard. Distinta dalla tintoria
(li' il processo e' il bagno di
tintura del tessuto, con acque
reflue di tintura, e l'alternativa
e' la sola caldaia a gas sul
calore residuo, senza olive,
senza sansa, senza cogeneratore,
senza vendita di elettricita'),
dalla conceria (li' si scaldano
vasche di concia con pompa di
calore e recupero dallo scarico
caldo, senza olive, senza sansa,
senza cogeneratore a biomassa,
senza vendita di elettricita'),
dalla vetreria (li' si fonde il
vetro in forni, con cullet, senza
olive, senza sansa, senza
cogeneratore), dalla fonderia
(li' si fonde la ghisa in forni,
con carica metallica, senza
olive, senza sansa, senza
cogeneratore), dall'essiccazione
(li' si seccano solidi togliendo
acqua, legno o pasta, senza
olive, senza sansa, senza
cogeneratore, senza vendita di
elettricita') e da una caldaia
generica senza processo (li' il
calore e' generico, senza olive,
senza sansa, senza cogeneratore,
senza elettricita' prodotta e
venduta).

Demo calcolata eseguendo demo_calcoli()
(e ricontrollata a mano, riga per
riga): produzione olive 2.000
t/anno, resa sansa 0,35 t/t, PCI
sansa 4,2 MWh/t, rendimento
elettrico 28 %, rendimento termico
55 %, elettricita' specifica 60
kWh/t, calore specifico 40 kWh/t,
rendimento caldaia 90 %, prezzo
elettricita' 200 EUR/MWh, prezzo
gas 60 EUR/MWh, prezzo vendita 80
EUR/MWh, costo trattamento sansa
20 EUR/t, O&M annuo 15.000
EUR/anno, CAPEX 350.000 EUR,
fattore elettricita' 0,25
tCO2/MWh, fattore gas 0,20
tCO2/MWh, WACC 5 %, vita 15 anni,
tolleranza MARGINALE 10 % del
CAPEX.

- m_sansa_t_anno = 700.0
- e_biomassa_mwh_anno = 2940.0
- e_el_mwh_anno = 823.2
- q_th_mwh_anno = 1617.0000000000002
- e_dem_mwh_anno = 120.0
- q_dem_mwh_anno = 80.0
- e_auto_mwh_anno = 120.0
- e_vend_mwh_anno = 703.2
- q_auto_mwh_anno = 80.0
- c_base_eur_anno = 29333.333333333332
- c_alt_eur_anno = -27256.0
- co2_base_t_anno = 47.77777777777778
- co2_alt_t_anno = -175.8
- risparmio_eur_anno = 56589.33333333333
- co2_evitata_t_anno = 223.57777777777778
- lco_base_eur_t = 14.666666666666666
- lco_alt_eur_t = -13.628
- van = 237377.9286086141
- tir = 13.861592810054779
- payback = 7
- prezzo_pareggio_eur_mwh = None
- prezzo_vendita_pareggio_eur_mwh = -0.47402351156617195
- verdetto = 'CONVIENTE'

Scomposizione: sansa = 2.000 x 0,35
= 700 t/anno; energia biomassa =
700 x 4,2 = 2.940 MWh/anno;
elettricita' prodotta = 2.940 x
0,28 = 823,20 MWh/anno; calore
prodotto = 2.940 x 0,55 = 1.617
MWh/anno; domanda elettrica =
2.000 x 60 / 1000 = 120 MWh/anno;
domanda termica = 2.000 x 40 /
1000 = 80 MWh/anno; autoconsumo
elettrico = min(823,20, 120) = 120
MWh/anno; vendita = 823,20 - 120 =
703,20 MWh/anno; calore
autoconsumato = min(1.617, 80) =
80 MWh/anno; costo base = 120 x
200 + (80 / 0,90) x 60 =
29.333,333333 EUR/anno; costo alt
= 15.000 + 700 x 20 + 0 + 0 -
703,20 x 80 = -27.256 EUR/anno;
risparmio = 29.333,333333 -
(-27.256) = 56.589,333333 EUR/anno;
CO2 base = 120 x 0,25 + (80 /
0,90) x 0,20 = 47,777778 t/anno;
CO2 alt = -703,20 x 0,25 = -175,80
t/anno; CO2 evitata = 47,777778 -
(-175,80) = 223,577778 t/anno;
LCO base 29.333,333333 / 2.000 =
14,666667 EUR/t; LCO alt -27.256 /
2.000 = -13,628 EUR/t; flussi:
anno 0 -350.000, anni 1-15
risparmio 56.589,333333 (piatti);
VAN -350.000 + 56.589,333333 x
10,379658 (annuita' 15 anni al
5 %) = 237.377,93 EUR; TIR 13,86 %;
payback 7 anni (il cumulato
all'anno 7 e' 46.125,33 EUR, gia'
>= 0); prezzo elettricita' di
pareggio None sempre (non definito
in questa tab); prezzo vendita di
pareggio (15.000 + 14.000 + 0 + 0 -
29.333,333333) / 703,20 =
-0,474024 EUR/MWh (negativo: il
caso conviene anche a prezzo di
vendita zero); verdetto CONVIENTE
perche' VAN > 0.
NOTA: il CAPEX non entra nel LCO
di questa tab: entra solo nei
flussi, nella VAN, nella TIR e
nel payback.
NOTA 2: in questa tab il risparmio
nullo o negativo NON e' degenere:
con prezzo vendita 0 EUR/MWh il
caso e' calcolabile (valid=True,
flussi pieni), NON_CONVIENTE con
VAN -346.540,11 EUR, non un
errore.
NOTA 3: la CO2 evitata ha segno
libero in generale (NON monetizzata):
con fattore elettricita' 0
tCO2/MWh la CO2 evitata diventa
17,78 t/anno (solo il gas evitato)
e il caso resta calcolabile e
CONVIENTE economicamente; la
funzione pura resta a segno libero.
NOTA 4: il prezzo elettricita' di
pareggio e' None sempre in questa
tab, anche nel caso demo: non e'
un valore mancante, e' una scelta
del brief (il pareggio su p_el
non e' univoco perche'
l'alternativa vende anche
elettricita').
NOTA 5: il prezzo vendita di
pareggio e' negativo nel caso demo
(-0,47 EUR/MWh): l'impianto conviene
anche a prezzo di vendita zero
(risparmio 333,33 EUR/anno con
p_vendita 0); con rendimento
termico zero il pareggio di vendita
diventa 7,11 EUR/MWh (il calore
residuo da caldaia pesa sui costi).
NOTA 6: il payback usa il cumulato
>= 0 (regola >= del brief): con
CAPEX nullo il payback e' 0 (non
1); con flussi [-100, 50, 50] il
payback e' 2 (il cumulato all'anno
2 e' zero, e zero basta).
NOTA 7: il verdetto MARGINALE
richiede VAN negativa entro la
tolleranza % del CAPEX: con CAPEX
600.000 EUR la VAN e' -12.622,07
EUR, entro 60.000 EUR (10 % di
600.000), quindi MARGINALE; con
tolleranza 0 % lo stesso caso e'
NON_CONVIENTE.
NOTA 8: i valori demo sono stati
ricalcolati da zero: il ricalcolo
esatto (senza arrotondamenti
intermedi) da' sansa 700, biomassa
2.940, elettricita' 823,20, calore
1.617, domanda elettrica 120,
domanda termica 80, autoconsumo
120, vendita 703,20, calore auto
80, costo base 29.333,333333,
costo alt -27.256, risparmio
56.589,333333, CO2 evitata
223,577778, LCO base 14,666667,
LCO alt -13,628, VAN 237.377,93,
TIR 13,86 %, payback 7 e pareggio
vendita -0,474024: i file usano i
valori esatti.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w771_helpers import (
    demo_calcoli,
    mh770_c_alt,
    mh770_c_base,
    mh770_calcola,
    mh770_co2_alt,
    mh770_co2_base,
    mh770_co2_evitata,
    mh770_csv,
    mh770_demo,
    mh770_e_auto,
    mh770_e_biomassa,
    mh770_e_dem,
    mh770_e_el,
    mh770_e_vend,
    mh770_flussi,
    mh770_int_pos,
    mh770_lco_alt,
    mh770_lco_base,
    mh770_m_sansa,
    mh770_nneg,
    mh770_num,
    mh770_payback,
    mh770_pct_0_100,
    mh770_pct_0_100_escl0,
    mh770_pct_tolleranza,
    mh770_pct_wacc,
    mh770_pos,
    mh770_prezzo_vendita_pareggio,
    mh770_q_auto,
    mh770_q_dem,
    mh770_q_th,
    mh770_risparmio,
    mh770_tir,
    mh770_valida,
    mh770_van,
    mh770_verdetto,
)


def _demo_kwargs():
    return dict(mh770_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh770_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh770_num(3, "x") == 3.0
    assert mh770_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh770_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh770_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh770_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh770_pos(0, "x")
    with pytest.raises(ValueError):
        mh770_pos(-1, "x")
    assert mh770_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh770_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh770_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh770_int_pos(0, "x")


def test_pct_wacc_limiti():
    assert mh770_pct_wacc(0, "x") == 0.0
    assert mh770_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh770_pct_wacc(50.1, "x")


def test_pct_0_100_escl0_limiti():
    assert mh770_pct_0_100_escl0(100, "x") == 100.0
    assert mh770_pct_0_100_escl0(65.0, "x") == 65.0
    with pytest.raises(ValueError):
        mh770_pct_0_100_escl0(0, "x")
    with pytest.raises(ValueError):
        mh770_pct_0_100_escl0(100.1, "x")
    with pytest.raises(ValueError):
        mh770_pct_0_100_escl0(-1, "x")


def test_pct_0_100_limiti():
    assert mh770_pct_0_100(0, "x") == 0.0
    assert mh770_pct_0_100(100, "x") == 100.0
    assert mh770_pct_0_100(55.0, "x") == 55.0
    with pytest.raises(ValueError):
        mh770_pct_0_100(-0.1, "x")
    with pytest.raises(ValueError):
        mh770_pct_0_100(100.1, "x")


def test_pct_tolleranza_limiti():
    assert mh770_pct_tolleranza(0, "x") == 0.0
    assert mh770_pct_tolleranza(100, "x") == 100.0
    assert mh770_pct_tolleranza(10.0, "x") == 10.0
    with pytest.raises(ValueError):
        mh770_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh770_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_m_sansa_e_biomassa():
    assert mh770_m_sansa(2000, 0.35) == pytest.approx(700.0)
    assert mh770_m_sansa(2000, 0.20) == pytest.approx(400.0)
    assert mh770_e_biomassa(700.0, 4.2) == pytest.approx(2940.0)
    assert mh770_e_biomassa(400.0, 4.2) == pytest.approx(1680.0)
    with pytest.raises(ValueError):
        mh770_m_sansa(0, 0.35)
    with pytest.raises(ValueError):
        mh770_m_sansa(2000, 0)
    with pytest.raises(ValueError):
        mh770_e_biomassa(700.0, 0)


def test_e_el_e_q_th():
    assert mh770_e_el(2940.0, 0.28) == pytest.approx(823.2)
    assert mh770_q_th(2940.0, 0.55) == pytest.approx(1617.0)
    assert mh770_q_th(2940.0, 0.0) == 0.0
    assert mh770_e_el(2940.0, 1.0) == pytest.approx(2940.0)
    with pytest.raises(ValueError):
        mh770_e_el(2940.0, 0.0)
    with pytest.raises(ValueError):
        mh770_e_el(2940.0, 1.1)
    with pytest.raises(ValueError):
        mh770_q_th(2940.0, -0.1)
    with pytest.raises(ValueError):
        mh770_q_th(2940.0, 1.1)


def test_e_dem_e_q_dem():
    assert mh770_e_dem(2000, 60) == pytest.approx(120.0)
    assert mh770_e_dem(2000, 400) == pytest.approx(800.0)
    assert mh770_e_dem(2000, 0) == 0.0
    assert mh770_q_dem(2000, 40) == pytest.approx(80.0)
    assert mh770_q_dem(2000, 1000) == pytest.approx(2000.0)
    with pytest.raises(ValueError):
        mh770_e_dem(2000, -1)
    with pytest.raises(ValueError):
        mh770_e_dem(0, 60)


def test_e_auto_e_vend_e_q_auto():
    assert mh770_e_auto(823.2, 120.0) == pytest.approx(120.0)
    assert mh770_e_auto(823.2, 2000.0) == pytest.approx(823.2)
    assert mh770_e_auto(823.2, 800.0) == pytest.approx(800.0)
    assert mh770_e_vend(823.2, 120.0) == pytest.approx(703.2)
    assert mh770_e_vend(823.2, 823.2) == 0.0
    assert mh770_e_vend(823.2, 800.0) == pytest.approx(23.2)
    assert mh770_q_auto(1617.0, 80.0) == pytest.approx(80.0)
    assert mh770_q_auto(1617.0, 2000.0) == pytest.approx(1617.0)
    assert mh770_q_auto(0.0, 80.0) == 0.0
    with pytest.raises(ValueError):
        mh770_e_auto(-1, 120.0)
    with pytest.raises(ValueError):
        mh770_e_vend(823.2, -1)


def test_c_base_c_alt():
    assert mh770_c_base(120.0, 80.0, 0.90, 200,
                        60) == pytest.approx(29333.333333333332)
    assert mh770_c_base(120.0, 80.0, 1.0, 200,
                        60) == pytest.approx(28800.0)
    assert mh770_c_alt(15000, 700.0, 20, 120.0, 120.0, 200, 80.0,
                       80.0, 0.90, 60, 703.2,
                       80) == pytest.approx(-27256.0)
    assert mh770_c_alt(15000, 700.0, 20, 120.0, 120.0, 200, 80.0,
                       80.0, 0.90, 60, 703.2,
                       0) == pytest.approx(29000.0)
    with pytest.raises(ValueError):
        mh770_c_base(120.0, 80.0, 0.0, 200, 60)
    with pytest.raises(ValueError):
        mh770_c_base(120.0, 80.0, 1.1, 200, 60)
    with pytest.raises(ValueError):
        mh770_c_alt(15000, 700.0, -1, 120.0, 120.0, 200, 80.0,
                    80.0, 0.90, 60, 703.2, 80)


def test_co2_base_alt_evitata():
    assert mh770_co2_base(120.0, 80.0, 0.90, 0.25,
                          0.20) == pytest.approx(47.77777777777778)
    assert mh770_co2_alt(703.2, 0.25) == pytest.approx(-175.8)
    assert mh770_co2_alt(0.0, 0.25) == 0.0
    assert mh770_co2_evitata(47.77777777777778,
                             -175.8) == pytest.approx(
        223.57777777777778)
    assert mh770_co2_evitata(100.0, 150.0) == pytest.approx(-50.0)
    with pytest.raises(ValueError):
        mh770_co2_base(120.0, 80.0, 0.90, -0.10, 0.20)


def test_risparmio_segno():
    assert mh770_risparmio(29333.333333333332, -27256.0) == \
        pytest.approx(56589.33333333333)
    assert mh770_risparmio(29333.333333333332, 29333.333333333332) == 0.0
    assert mh770_risparmio(29333.333333333332, 29000.0) == \
        pytest.approx(333.3333333333321)


def test_lco():
    assert mh770_lco_base(29333.333333333332, 2000) == pytest.approx(
        14.666666666666666)
    assert mh770_lco_alt(-27256.0, 2000) == pytest.approx(-13.628)
    assert mh770_lco_base(29333.333333333332, 0) is None
    assert mh770_lco_alt(-27256.0, 0) is None
    assert mh770_lco_alt(-27256.0, -5) is None


def test_prezzo_vendita_pareggio_formula_zero_e_none():
    assert mh770_prezzo_vendita_pareggio(
        15000, 700.0, 20, 120.0, 120.0, 200, 80.0, 80.0, 0.90, 60,
        29333.333333333332, 703.2) == pytest.approx(
        -0.47402351156617195)
    assert mh770_prezzo_vendita_pareggio(
        15000, 700.0, 20, 120.0, 120.0, 200, 80.0, 80.0, 0.90, 60,
        29333.333333333332, 0.0) is None
    assert mh770_prezzo_vendita_pareggio(
        15000, 700.0, 20, 120.0, 120.0, 200, 80.0, 80.0, 0.90, 60,
        29333.333333333332, -5.0) is None


def test_prezzo_vendita_pareggio_termico_zero():
    """Con rendimento termico zero il calore residuo va
    comprato da caldaia: il pareggio di vendita sale
    a 7,11 EUR/MWh."""
    bc = _variante(eta_th_pct=0)
    assert bc["prezzo_vendita_pareggio_eur_mwh"] == pytest.approx(
        7.11035267349261)
    assert bc["q_th_mwh_anno"] == 0.0
    assert bc["q_auto_mwh_anno"] == 0.0


def test_prezzo_elettricita_pareggio_sempre_none():
    """Il pareggio su prezzo elettricita' e' None sempre:
    non definito in questa tab, anche nel caso demo."""
    bc = demo_calcoli()
    assert bc["prezzo_pareggio_eur_mwh"] is None
    assert _variante(e_el_spec_kwh_per_t=400)[
        "prezzo_pareggio_eur_mwh"] is None
    assert _variante(e_el_spec_kwh_per_t=1000)[
        "prezzo_pareggio_eur_mwh"] is None


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh770_flussi(350000, 56589.33333333333, 15)
    assert len(fl) == 16
    assert fl[0] == -350000
    assert all(f == 56589.33333333333 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = demo_calcoli()
    assert bc["van"] == pytest.approx(237377.9286086141)
    assert mh770_van([-350000] + [56589.33333333333] * 15,
                     0) == pytest.approx(498839.9999999998)
    assert mh770_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = demo_calcoli()
    assert bc["tir"] == pytest.approx(13.861592810054779)
    assert mh770_tir([-350000] + [56589.33333333333] * 15) == \
        pytest.approx(0.13861592810054779)
    tir = mh770_tir([-350000] + [56589.33333333333] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate(
                  [-350000] + [56589.33333333333] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    """Payback con cumulato >= 0: il cumulato nullo basta."""
    assert mh770_payback([-350000] + [56589.33333333333] * 15) == 7
    assert mh770_payback([-350000] + [-1000.0] * 15) is None
    assert mh770_payback([0] + [56589.33333333333] * 15) == 0
    assert mh770_payback([-100] + [50] * 2) == 2
    assert mh770_payback([-113178.66666666666] +
                         [56589.33333333333] * 2) == 2


def test_verdetto():
    assert mh770_verdetto(100.0, 350000, 10.0) == "CONVIENTE"
    assert mh770_verdetto(0.0, 350000, 10.0) == "NON_CONVIENTE"
    assert mh770_verdetto(-12622.071391385918, 600000,
                          10.0) == "MARGINALE"
    assert mh770_verdetto(-12622.071391385918, 600000,
                          0.0) == "NON_CONVIENTE"
    assert mh770_verdetto(-212622.07139138586, 800000,
                          10.0) == "NON_CONVIENTE"
    assert mh770_verdetto(-100.0, 0, 10.0) == "NON_CONVIENTE"
    assert mh770_verdetto(None, 350000, 10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh770_verdetto(float("nan"), 350000, 10.0)
    with pytest.raises(ValueError):
        mh770_verdetto(100.0, -1, 10.0)
    with pytest.raises(ValueError):
        mh770_verdetto(100.0, 350000, 100.1)


def test_valida_demo_ok():
    v = mh770_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("p_t_anno", "2000"),
                       ("p_t_anno", float("nan")),
                       ("p_t_anno", float("inf")),
                       ("p_t_anno", True),
                       ("prezzo_gas_eur_mwh", None),
                       ("eta_el_pct", "28")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh770_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("p_t_anno", 0),
                          ("p_t_anno", -1),
                          ("resa_sansa_t_per_t", 0),
                          ("resa_sansa_t_per_t", -0.1),
                          ("pci_mwh_per_t", 0),
                          ("pci_mwh_per_t", -1),
                          ("eta_el_pct", 0),
                          ("eta_el_pct", 100.1),
                          ("eta_th_pct", -1),
                          ("eta_th_pct", 100.1),
                          ("eta_el_pct", 50),
                          ("e_el_spec_kwh_per_t", -1),
                          ("q_th_spec_kwh_per_t", -1),
                          ("eta_caldaia_pct", 0),
                          ("eta_caldaia_pct", 100.1),
                          ("prezzo_el_eur_mwh", -1),
                          ("prezzo_gas_eur_mwh", -1),
                          ("prezzo_vendita_eur_mwh", -1),
                          ("costo_tratt_sansa_eur_t", -1),
                          ("om_eur_anno", -100),
                          ("capex_eur", -1),
                          ("f_el_t_per_mwh", -0.10),
                          ("f_gas_t_per_mwh", -0.10),
                          ("wacc_pct", -0.1), ("wacc_pct", 50.1),
                          ("vita_anni", 0), ("vita_anni", 2.5),
                          ("tolleranza_pct", -1),
                          ("tolleranza_pct", 100.1)):
        d = _demo_kwargs()
        d[campo] = valore
        assert mh770_valida(**d)["valido"] is False


def test_valida_somma_rendimenti_sopra_cento():
    """Somma eta_el + eta_th > 100 %: degenere anche se i
    singoli rendimenti sono validi (45 + 60 = 105)."""
    d = _demo_kwargs()
    d.update({"eta_el_pct": 45, "eta_th_pct": 60})
    assert mh770_valida(**d)["valido"] is False
    with pytest.raises(ValueError):
        mh770_calcola(**d)
    d2 = _demo_kwargs()
    d2.update({"eta_el_pct": 45, "eta_th_pct": 55})
    assert mh770_valida(**d2)["valido"] is True


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"eta_th_pct": 0,
              "eta_caldaia_pct": 100,
              "e_el_spec_kwh_per_t": 0,
              "q_th_spec_kwh_per_t": 0,
              "prezzo_gas_eur_mwh": 0,
              "prezzo_el_eur_mwh": 0,
              "prezzo_vendita_eur_mwh": 0,
              "costo_tratt_sansa_eur_t": 0,
              "f_el_t_per_mwh": 0,
              "f_gas_t_per_mwh": 0,
              "om_eur_anno": 0,
              "capex_eur": 0, "wacc_pct": 0,
              "tolleranza_pct": 0})
    assert mh770_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["eta_el_pct"] = 100
    d["tolleranza_pct"] = 100
    assert mh770_valida(**d)["valido"] is True


def test_valida_non_controlla_risparmio_calcola_neppure():
    """La validazione input NON controlla il risparmio
    (e' un esito, non un range) e in questa tab
    nemmeno mh770_calcola lo controlla: con prezzo
    vendita 0 EUR/MWh il caso resta CALCOLABILE."""
    d = _demo_kwargs()
    d["prezzo_vendita_eur_mwh"] = 0
    assert mh770_valida(**d)["valido"] is True
    bc = _variante(prezzo_vendita_eur_mwh=0)
    assert bc["valid"] is True
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["flussi"]
    assert bc["payback"] is None


def test_demo_dict():
    d = mh770_demo()
    assert d["p_t_anno"] == 2000
    assert d["resa_sansa_t_per_t"] == 0.35
    assert d["pci_mwh_per_t"] == 4.2
    assert d["eta_el_pct"] == 28.0
    assert d["eta_th_pct"] == 55.0
    assert d["e_el_spec_kwh_per_t"] == 60
    assert d["q_th_spec_kwh_per_t"] == 40
    assert d["eta_caldaia_pct"] == 90.0
    assert d["prezzo_el_eur_mwh"] == 200
    assert d["prezzo_gas_eur_mwh"] == 60
    assert d["prezzo_vendita_eur_mwh"] == 80
    assert d["costo_tratt_sansa_eur_t"] == 20
    assert d["om_eur_anno"] == 15000
    assert d["capex_eur"] == 350000
    assert d["f_el_t_per_mwh"] == 0.25
    assert d["f_gas_t_per_mwh"] == 0.20
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    """Ogni _DEMO del test contro demo_calcoli():
    scarto relativo < 1e-9 (zero atteso:
    confronto assoluto)."""
    bc = demo_calcoli()
    attesi = {
        "m_sansa_t_anno": 700.0,
        "e_biomassa_mwh_anno": 2940.0,
        "e_el_mwh_anno": 823.2,
        "q_th_mwh_anno": 1617.0000000000002,
        "e_dem_mwh_anno": 120.0,
        "q_dem_mwh_anno": 80.0,
        "e_auto_mwh_anno": 120.0,
        "e_vend_mwh_anno": 703.2,
        "q_auto_mwh_anno": 80.0,
        "c_base_eur_anno": 29333.333333333332,
        "c_alt_eur_anno": -27256.0,
        "co2_base_t_anno": 47.77777777777778,
        "co2_alt_t_anno": -175.8,
        "risparmio_eur_anno": 56589.33333333333,
        "co2_evitata_t_anno": 223.57777777777778,
        "lco_base_eur_t": 14.666666666666666,
        "lco_alt_eur_t": -13.628,
        "van": 237377.9286086141,
        "tir": 13.861592810054779,
        "prezzo_vendita_pareggio_eur_mwh": -0.47402351156617195,
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
    assert bc["prezzo_pareggio_eur_mwh"] is None


def test_demo_calcoli_fisica():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["m_sansa_t_anno"] == pytest.approx(700.0)
    assert bc["e_biomassa_mwh_anno"] == pytest.approx(2940.0)
    assert bc["e_el_mwh_anno"] == pytest.approx(823.2)
    assert bc["q_th_mwh_anno"] == pytest.approx(1617.0)
    assert bc["e_dem_mwh_anno"] == pytest.approx(120.0)
    assert bc["q_dem_mwh_anno"] == pytest.approx(80.0)
    assert bc["e_auto_mwh_anno"] == pytest.approx(120.0)
    assert bc["e_vend_mwh_anno"] == pytest.approx(703.2)
    assert bc["q_auto_mwh_anno"] == pytest.approx(80.0)
    assert bc["co2_evitata_t_anno"] == pytest.approx(223.57777777777778)


def test_demo_calcoli_economia():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(29333.333333333332)
    assert bc["c_alt_eur_anno"] == pytest.approx(-27256.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(56589.33333333333)
    assert bc["prezzo_vendita_pareggio_eur_mwh"] == pytest.approx(
        -0.47402351156617195)
    assert bc["prezzo_pareggio_eur_mwh"] is None


def test_demo_calcoli_finanza():
    bc = demo_calcoli()
    assert bc["lco_base_eur_t"] == pytest.approx(14.666666666666666)
    assert bc["lco_alt_eur_t"] == pytest.approx(-13.628)
    assert bc["van"] == pytest.approx(237377.9286086141)
    assert bc["tir"] == pytest.approx(13.861592810054779)
    assert bc["payback"] == 7
    assert bc["verdetto"] == "CONVIENTE"


def test_demo_flussi_e_cumulato():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -350000
    assert len(bc["flussi"]) == 16
    assert all(f == 56589.33333333333 for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -350000
    assert righe.iloc[6]["Cumulato (EUR)"] == pytest.approx(
        -10464.000000000073)
    assert righe.iloc[7]["Cumulato (EUR)"] == pytest.approx(
        46125.333333333256)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(
        498839.9999999998)
    assert righe.iloc[15]["Flusso (EUR/anno)"] == 56589.33333333333


def test_demo_tabella_righe():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Produzione olive (t/anno)"] == pytest.approx(2000.0)
    assert mappa["Sansa prodotta (t/anno)"] == pytest.approx(700.0)
    assert mappa["Energia biomassa (MWh/anno)"] == pytest.approx(2940.0)
    assert mappa["Elettricita' prodotta (MWh/anno)"] == pytest.approx(
        823.2)
    assert mappa["Elettricita' venduta (MWh/anno)"] == pytest.approx(
        703.2)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(
        -27256.0)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(
        56589.33333333333)
    assert mappa["Payback (anni)"] == 7
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Prezzo vendita di pareggio (EUR/MWh)"] == \
        pytest.approx(-0.47402351156617195)
    assert mappa["Prezzo elettricita' di pareggio (EUR/MWh)"] is None


def test_demo_coerenza_interna():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["e_auto_mwh_anno"] == pytest.approx(
        min(bc["e_el_mwh_anno"], bc["e_dem_mwh_anno"]))
    assert bc["e_vend_mwh_anno"] == pytest.approx(
        bc["e_el_mwh_anno"] - bc["e_auto_mwh_anno"])
    assert bc["q_auto_mwh_anno"] == pytest.approx(
        min(bc["q_th_mwh_anno"], bc["q_dem_mwh_anno"]))
    assert bc["m_sansa_t_anno"] == pytest.approx(
        bc["p_t_anno"] * bc["resa_sansa_t_per_t"])
    assert bc["e_biomassa_mwh_anno"] == pytest.approx(
        bc["m_sansa_t_anno"] * bc["pci_mwh_per_t"])
    assert bc["e_el_mwh_anno"] == pytest.approx(
        bc["e_biomassa_mwh_anno"] * bc["eta_el_pct"] / 100.0)
    assert bc["q_th_mwh_anno"] == pytest.approx(
        bc["e_biomassa_mwh_anno"] * bc["eta_th_pct"] / 100.0)
    assert bc["e_dem_mwh_anno"] == pytest.approx(
        bc["p_t_anno"] * bc["e_el_spec_kwh_per_t"] / 1000.0)
    assert bc["q_dem_mwh_anno"] == pytest.approx(
        bc["p_t_anno"] * bc["q_th_spec_kwh_per_t"] / 1000.0)
    assert bc["co2_base_t_anno"] - bc["co2_alt_t_anno"] == \
        pytest.approx(bc["co2_evitata_t_anno"])
    assert bc["co2_alt_t_anno"] == pytest.approx(
        -bc["e_vend_mwh_anno"] * bc["f_el_t_per_mwh"])
    assert bc["c_base_eur_anno"] / bc["p_t_anno"] == \
        pytest.approx(bc["lco_base_eur_t"])
    assert bc["c_alt_eur_anno"] / bc["p_t_anno"] == \
        pytest.approx(bc["lco_alt_eur_t"])


def test_demo_contro_riconteggio_indipendente():
    p, resa, pci = 2000, 0.35, 4.2
    eel, eth, ecal = 28.0, 55.0, 90.0
    esp, qsp = 60, 40
    pel, pg, pv, ct, om, cx = 200, 60, 80, 20, 15000, 350000
    fel, fg, wacc, vita = 0.25, 0.20, 5.0, 15
    m = p * resa
    eb = m * pci
    ee = eb * (eel / 100.0)
    qt = eb * (eth / 100.0)
    ed = p * esp / 1000.0
    qd = p * qsp / 1000.0
    ea = min(ee, ed)
    ev = ee - ea
    qa = min(qt, qd)
    cb = ed * pel + (qd / (ecal / 100.0)) * pg
    ca = om + m * ct + (ed - ea) * pel + \
        ((qd - qa) / (ecal / 100.0)) * pg - ev * pv
    risp = cb - ca
    co2b = ed * fel + (qd / (ecal / 100.0)) * fg
    co2a = -ev * fel
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    par = (om + m * ct + (ed - ea) * pel +
           ((qd - qa) / (ecal / 100.0)) * pg - cb) / ev
    bc = demo_calcoli()
    assert bc["m_sansa_t_anno"] == pytest.approx(m)
    assert bc["e_biomassa_mwh_anno"] == pytest.approx(eb)
    assert bc["e_el_mwh_anno"] == pytest.approx(ee)
    assert bc["q_th_mwh_anno"] == pytest.approx(qt)
    assert bc["e_dem_mwh_anno"] == pytest.approx(ed)
    assert bc["q_dem_mwh_anno"] == pytest.approx(qd)
    assert bc["e_auto_mwh_anno"] == pytest.approx(ea)
    assert bc["e_vend_mwh_anno"] == pytest.approx(ev)
    assert bc["q_auto_mwh_anno"] == pytest.approx(qa)
    assert bc["c_base_eur_anno"] == pytest.approx(cb)
    assert bc["c_alt_eur_anno"] == pytest.approx(ca)
    assert bc["risparmio_eur_anno"] == pytest.approx(risp)
    assert bc["co2_base_t_anno"] == pytest.approx(co2b)
    assert bc["co2_alt_t_anno"] == pytest.approx(co2a)
    assert bc["van"] == pytest.approx(van)
    assert bc["prezzo_vendita_pareggio_eur_mwh"] == pytest.approx(par)
    assert bc["prezzo_pareggio_eur_mwh"] is None


# ---------------------------------------------------------------- varianti
def test_demo_conviente():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] > 0.0
    assert bc["payback"] == 7
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_autoconsumo_parziale():
    """Autoconsumo parziale: domanda elettrica 800
    MWh/anno, sotto la produzione 823,20: autoconsumo
    800, vendita residua 23,20 MWh/anno."""
    bc = _variante(e_el_spec_kwh_per_t=400)
    assert bc["valid"] is True
    assert bc["e_dem_mwh_anno"] == pytest.approx(800.0)
    assert bc["e_auto_mwh_anno"] == pytest.approx(800.0)
    assert bc["e_vend_mwh_anno"] == pytest.approx(23.2)
    assert bc["c_base_eur_anno"] == pytest.approx(165333.33333333334)
    assert bc["c_alt_eur_anno"] == pytest.approx(27143.999999999996)
    assert bc["risparmio_eur_anno"] == pytest.approx(138189.33333333334)
    assert bc["van"] == pytest.approx(1084358.0245241504)
    assert bc["tir"] == pytest.approx(39.206275428660476)
    assert bc["payback"] == 3
    assert bc["prezzo_vendita_pareggio_eur_mwh"] == pytest.approx(
        -5876.436781609184)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_vendita_zero():
    """Vendita zero: produzione minore della domanda
    (domanda 2.000 MWh/anno contro produzione 823,20):
    tutto autoconsumato, vendita 0, prezzo vendita
    di pareggio None."""
    bc = _variante(e_el_spec_kwh_per_t=1000)
    assert bc["valid"] is True
    assert bc["e_dem_mwh_anno"] == pytest.approx(2000.0)
    assert bc["e_auto_mwh_anno"] == pytest.approx(823.2)
    assert bc["e_vend_mwh_anno"] == 0.0
    assert bc["prezzo_vendita_pareggio_eur_mwh"] is None
    assert bc["c_base_eur_anno"] == pytest.approx(405333.3333333333)
    assert bc["c_alt_eur_anno"] == pytest.approx(264360.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(140973.3333333333)
    assert bc["van"] == pytest.approx(1113254.992502445)
    assert bc["tir"] == pytest.approx(40.01973226034845)
    assert bc["payback"] == 3
    assert bc["co2_evitata_t_anno"] == pytest.approx(517.7777777777778)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_domanda_termica_sopra_produzione():
    """Domanda termica 2.000 MWh/anno sopra il calore
    prodotto 1.617: calore autoconsumato 1.617, il
    residuo va comprato da caldaia a gas."""
    bc = _variante(q_th_spec_kwh_per_t=1000)
    assert bc["valid"] is True
    assert bc["q_dem_mwh_anno"] == pytest.approx(2000.0)
    assert bc["q_auto_mwh_anno"] == pytest.approx(1617.0)
    assert bc["c_base_eur_anno"] == pytest.approx(157333.33333333334)
    assert bc["c_alt_eur_anno"] == pytest.approx(-1722.666666666686)
    assert bc["risparmio_eur_anno"] == pytest.approx(159056.00000000003)
    assert bc["van"] == pytest.approx(1300946.8889208524)
    assert bc["payback"] == 3
    assert bc["co2_evitata_t_anno"] == pytest.approx(650.2444444444445)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_marginale_capex_alto():
    """Fascia MARGINALE: CAPEX 600.000 EUR, VAN
    negativa entro la tolleranza del 10 % del
    CAPEX (60.000 EUR)."""
    bc = _variante(capex_eur=600000)
    assert bc["valid"] is True
    assert bc["van"] == pytest.approx(-12622.071391385918)
    assert bc["tir"] == pytest.approx(4.687120307588484)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"
    bc0 = _variante(capex_eur=600000, tolleranza_pct=0)
    assert bc0["verdetto"] == "NON_CONVIENTE"
    assert bc0["van"] == pytest.approx(-12622.071391385918)


def test_variante_non_conviente_prezzo_vendita_zero():
    """NON_CONVIENTE: prezzo vendita zero, risparmio
    quasi nullo (333,33 EUR/anno), VAN negativa oltre
    la tolleranza, payback mai."""
    bc = _variante(prezzo_vendita_eur_mwh=0)
    assert bc["valid"] is True
    assert bc["c_alt_eur_anno"] == pytest.approx(29000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(333.3333333333321)
    assert bc["van"] == pytest.approx(-346540.1139872732)
    assert bc["tir"] == pytest.approx(-32.18515155685867)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["flussi"]


def test_variante_non_conviente_capex_altissimo():
    """NON_CONVIENTE per CAPEX: 800.000 EUR, VAN
    -212.622,07 EUR oltre la tolleranza del 10 %
    (80.000 EUR), payback all'anno 15."""
    bc = _variante(capex_eur=800000)
    assert bc["valid"] is True
    assert bc["van"] == pytest.approx(-212622.07139138586)
    assert bc["tir"] == pytest.approx(0.7500499840634204)
    assert bc["payback"] == 15
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_wacc_zero():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(498839.9999999998)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    """Payback regola >=: con CAPEX nullo il payback e' 0,
    non 1 (all'anno 0 il cumulato e' gia' zero)."""
    bc = _variante(capex_eur=0)
    assert bc["capex_eur"] == 0
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(587377.928608614)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_vita_diversa():
    bc = _variante(vita_anni=20)
    assert len(bc["flussi"]) == 21
    assert bc["van"] == pytest.approx(355228.1751441092)
    assert bc["tir"] == pytest.approx(15.217050320867598)
    assert bc["payback"] == 7
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_rendimento_termico_zero():
    bc = _variante(eta_th_pct=0)
    assert bc["q_th_mwh_anno"] == 0.0
    assert bc["q_auto_mwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(51256.0)
    assert bc["van"] == pytest.approx(182019.75240498432)
    assert bc["payback"] == 7
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_fattore_el_zero_co2_evitata_solo_gas():
    bc = _variante(f_el_t_per_mwh=0)
    assert bc["valid"] is True
    assert bc["co2_alt_t_anno"] == 0.0
    assert bc["co2_evitata_t_anno"] == pytest.approx(17.77777777777778)
    assert bc["risparmio_eur_anno"] == pytest.approx(56589.33333333333)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_resa_sansa_bassa():
    bc = _variante(resa_sansa_t_per_t=0.20)
    assert bc["m_sansa_t_anno"] == pytest.approx(400.0)
    assert bc["e_biomassa_mwh_anno"] == pytest.approx(1680.0)
    assert bc["e_el_mwh_anno"] == pytest.approx(470.4)
    assert bc["e_vend_mwh_anno"] == pytest.approx(350.4)
    assert bc["verdetto"] == "CONVIENTE"


# ---------------------------------------------------------------- degenere
def test_degenere_produzione_zero_sollevela():
    """Caso degenere richiesto dal brief: P = 0
    solleva ValueError."""
    with pytest.raises(ValueError):
        _variante(p_t_anno=0)


def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"p_t_anno": 0}, {"p_t_anno": -1},
               {"resa_sansa_t_per_t": 0},
               {"resa_sansa_t_per_t": -0.1},
               {"pci_mwh_per_t": 0},
               {"pci_mwh_per_t": -1},
               {"eta_el_pct": 0},
               {"eta_el_pct": 100.1},
               {"eta_th_pct": -1},
               {"eta_th_pct": 100.1},
               {"eta_el_pct": 50, "eta_th_pct": 60},
               {"e_el_spec_kwh_per_t": -1},
               {"q_th_spec_kwh_per_t": -1},
               {"eta_caldaia_pct": 0},
               {"eta_caldaia_pct": 100.1},
               {"prezzo_el_eur_mwh": -1},
               {"prezzo_gas_eur_mwh": -1},
               {"prezzo_vendita_eur_mwh": -1},
               {"costo_tratt_sansa_eur_t": -1},
               {"om_eur_anno": -100},
               {"capex_eur": -1},
               {"f_el_t_per_mwh": -0.10},
               {"f_gas_t_per_mwh": -0.10},
               {"wacc_pct": -1}, {"wacc_pct": 60},
               {"vita_anni": 0}, {"vita_anni": 2.5},
               {"tolleranza_pct": -1},
               {"tolleranza_pct": 100.1}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh770_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"p_t_anno": "2000"},
               {"p_t_anno": float("nan")},
               {"prezzo_gas_eur_mwh": float("inf")},
               {"capex_eur": True},
               {"eta_el_pct": "28"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh770_valida(**d)["valido"] is False


def test_risparmio_negativo_non_degenere():
    """Differenza chiave: risparmio quasi nullo o
    negativo resta calcolabile, con flussi pieni e
    VAN negativa."""
    for kw in ({"prezzo_vendita_eur_mwh": 0},
               {"capex_eur": 800000}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["verdetto"] in ("NON_CONVIENTE", "MARGINALE")
        assert bc["flussi"]


def test_co2_evitata_segno_libero_funzione_pura():
    assert mh770_co2_evitata(100.0, 150.0) == pytest.approx(-50.0)


def test_verdetto_non_calcolabile_solo_van_none():
    assert mh770_verdetto(None, 350000, 10.0) == "NON_CALCOLABILE"
    assert demo_calcoli()["verdetto"] != "NON_CALCOLABILE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = demo_calcoli()
    testo = mh770_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert "m_sansa_t_anno;700.0" in testo
    assert "e_biomassa_mwh_anno;2940.0" in testo
    assert "e_el_mwh_anno;823.2" in testo
    assert "e_vend_mwh_anno;703.2" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "prezzo_vendita_pareggio_eur_mwh" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = demo_calcoli()
    testo = mh770_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"e_el_mwh_anno;{bc['e_el_mwh_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = demo_calcoli()
    testo = mh770_csv(bc, _demo_kwargs())
    for chiave in _demo_kwargs():
        assert f"{chiave};" in testo


def test_monotonia_prezzo_gas():
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(prezzo_gas_eur_mwh=70)["risparmio_eur_anno"]
    basso = _variante(prezzo_gas_eur_mwh=50)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(888.888888888889)
    assert base - basso == pytest.approx(888.888888888889)


def test_monotonia_prezzo_vendita():
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(prezzo_vendita_eur_mwh=100)["risparmio_eur_anno"]
    basso = _variante(prezzo_vendita_eur_mwh=60)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(14064.0)
    assert base - basso == pytest.approx(14064.0)


def test_monotonia_resa_sansa():
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(resa_sansa_t_per_t=0.40)["risparmio_eur_anno"]
    basso = _variante(resa_sansa_t_per_t=0.30)["risparmio_eur_anno"]
    assert alto > base > basso


def test_demo_deterministica_due_chiamate():
    a = demo_calcoli()
    b = demo_calcoli()
    assert a["van"] == b["van"]
    assert a["flussi"] == b["flussi"]
    assert a["tir"] == b["tir"]


def test_demo_chiavi_attese():
    assert set(mh770_demo().keys()) == {
        "p_t_anno",
        "resa_sansa_t_per_t",
        "pci_mwh_per_t",
        "eta_el_pct", "eta_th_pct",
        "e_el_spec_kwh_per_t", "q_th_spec_kwh_per_t",
        "eta_caldaia_pct",
        "prezzo_el_eur_mwh", "prezzo_gas_eur_mwh",
        "prezzo_vendita_eur_mwh",
        "costo_tratt_sansa_eur_t",
        "om_eur_anno", "capex_eur",
        "f_el_t_per_mwh", "f_gas_t_per_mwh",
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
    return ["mh" + "76" + "9", "st" + "76" + "9",
            "tab" + "76" + "9", "w" + "77" + "0_",
            "mh" + "76" + "8", "st" + "76" + "8",
            "tab" + "76" + "8", "w" + "76" + "9_"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w771_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w771_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab770:")


def test_registry_chain_tail_and_count():
    """Registry della nuova tab: il frammento UI apre la tab
    numero 770 (la coda della catena termina con la nuova tab
    e il conteggio atteso delle tab e' 770)."""
    src = _leggi("w771_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 770
    assert src.count("with tab770:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w771_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w771_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st770_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert "key=f" not in src and 'key = f' not in src
    assert "st.stop()" in src
    # guard degenere prima di KPI / grafico / tabella / CSV
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w771_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def770[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w771_ui.py")
        usate = set(re.findall(r'_def770\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 19
        assert usate <= set(mh770_demo().keys())


def test_ui_chiavi_demo_coerenti():
    """Ogni _def770[...] letto dalla UI esiste nel dict demo:
    sweep anti-KeyError a render (lezione dello sweep chiavi demo vs UI)."""
    src = _leggi("w771_ui.py")
    usate = set(re.findall(r'_def770\["([^"]+)"\]', src))
    assert usate
    assert len(usate) == 19
    assert usate <= set(mh770_demo().keys())


def test_ui_riferisce_solo_helper_nuovi():
    src = _leggi("w771_ui.py")
    usati = set(re.findall(r'\b(mh\d+_\w+)\b', src))
    assert usati
    assert all(u.startswith("mh770_") for u in usati)


@pytest.mark.parametrize("e_el_spec,atteso", [
    (60, 120.0),
    (400, 800.0),
    (1000, 2000.0),
])
def test_e_dem_parametrizzato(e_el_spec, atteso):
    assert mh770_e_dem(2000, e_el_spec) == pytest.approx(atteso)


@pytest.mark.parametrize("campo,valore", [
    ("p_t_anno", 0), ("p_t_anno", -3),
    ("resa_sansa_t_per_t", 0),
    ("resa_sansa_t_per_t", -0.1),
    ("pci_mwh_per_t", 0), ("pci_mwh_per_t", -1),
    ("eta_el_pct", 0), ("eta_el_pct", 100.1),
    ("eta_th_pct", -1), ("eta_th_pct", 100.1),
    ("e_el_spec_kwh_per_t", -1),
    ("q_th_spec_kwh_per_t", -1),
    ("eta_caldaia_pct", 0), ("eta_caldaia_pct", 100.1),
    ("prezzo_el_eur_mwh", -1),
    ("prezzo_gas_eur_mwh", -1),
    ("prezzo_vendita_eur_mwh", -1),
    ("costo_tratt_sansa_eur_t", -1),
    ("om_eur_anno", -100),
    ("capex_eur", -1),
    ("f_el_t_per_mwh", -0.10),
    ("f_gas_t_per_mwh", -0.10),
    ("wacc_pct", -0.1), ("wacc_pct", 50.1),
    ("vita_anni", -1), ("vita_anni", 2.5),
    ("tolleranza_pct", -1), ("tolleranza_pct", 100.1),
])
def test_valida_rifiuta_singoli_campi(campo, valore):
    d = _demo_kwargs()
    d[campo] = valore
    assert mh770_valida(**d)["valido"] is False


@pytest.mark.parametrize("campo,valore", [
    ("p_t_anno", 0), ("p_t_anno", -3),
    ("resa_sansa_t_per_t", 0),
    ("resa_sansa_t_per_t", -0.1),
    ("pci_mwh_per_t", 0), ("pci_mwh_per_t", -1),
    ("eta_el_pct", 0), ("eta_el_pct", 100.1),
    ("eta_th_pct", -1), ("eta_th_pct", 100.1),
    ("e_el_spec_kwh_per_t", -1),
    ("q_th_spec_kwh_per_t", -1),
    ("eta_caldaia_pct", 0), ("eta_caldaia_pct", 100.1),
    ("prezzo_el_eur_mwh", -1),
    ("prezzo_gas_eur_mwh", -1),
    ("prezzo_vendita_eur_mwh", -1),
    ("costo_tratt_sansa_eur_t", -1),
    ("om_eur_anno", -100),
    ("capex_eur", -1),
    ("f_el_t_per_mwh", -0.10),
    ("f_gas_t_per_mwh", -0.10),
    ("wacc_pct", -0.1), ("wacc_pct", 50.1),
    ("vita_anni", -1), ("vita_anni", 2.5),
    ("tolleranza_pct", -1), ("tolleranza_pct", 100.1),
])
def test_calcola_sollevela_singoli_campi(campo, valore):
    d = _demo_kwargs()
    d[campo] = valore
    with pytest.raises(ValueError):
        mh770_calcola(**d)


def test_df_tabella_valori_demo_selezionati():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Produzione olive (t/anno)"] == 2000.0
    assert mappa["Sansa prodotta (t/anno)"] == pytest.approx(700.0)
    assert mappa["Elettricita' venduta (MWh/anno)"] == pytest.approx(
        703.2)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(
        56589.33333333333)
    assert mappa["Verdetto"] == "CONVIENTE"


def test_lco_alt_minore_di_lco_base_demo():
    bc = demo_calcoli()
    assert bc["lco_alt_eur_t"] < bc["lco_base_eur_t"]
    assert bc["lco_base_eur_t"] - bc["lco_alt_eur_t"] == pytest.approx(
        28.294666666666666)
