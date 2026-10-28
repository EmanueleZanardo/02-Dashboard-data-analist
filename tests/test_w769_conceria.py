"""Test tab769 "Conceria: scaldare
le vasche di concia con pompa di
calore + recupero calore batte la
caldaia a gas?"

Nuova tab tab769 (conceria,
file di lavoro w770).
Business case deterministico
del riscaldamento delle vasche
di concia in conceria: volume
acqua V = P x acqua specifica
m3/anno; fabbisogno termico
Q_fabbisogno = V x 1000 x 4,186
x (T_proc - T_in) / 3.600.000
MWh/anno (1000 kg/m3, 4,186
kJ/kgK, 3.600.000 kJ/MWh); calore
recuperato = V x 1000 x 4,186 x
(T_scarico - T_in) x eta_recupero
/ 3.600.000 MWh/anno; calore
residuo = Q_fabbisogno -
Q_recuperato (sempre maggiore di
zero con i vincoli di validita');
gas baseline = Q_fabbisogno /
eta_caldaia MWh/anno (eta come
frazione, es. 0,90); elettricita'
alternativa = Q_residuo / COP
MWh/anno (COP > 1); costo base =
gas base x prezzo gas; costo
alternativo = elettricita' alt x
prezzo elettricita' + OM annuo;
CO2 base = gas base x f_gas;
CO2 alt = elettricita' alt x
f_el; risparmio = costo base -
costo alt; CO2 evitata = CO2 base
- CO2 alt, segno libero
(positiva nel caso demo), NON
monetizzata; fattore di emissione
in tCO2/MWh, numericamente uguale
a kg/kWh (1 kg/kWh = 1 t/MWh);
LCO base = costo base / P;
LCO alt = costo alt / P (il CAPEX
NON entra nel LCO di questa tab:
entra nei flussi, nella VAN,
nella TIR e nel payback); prezzo
elettricita' di pareggio =
(C_base - OM) / E_alt, None se
E_alt <= 0; flussi [-CAPEX,
risparmio x vita]; VAN, TIR,
payback (primo anno con cumulato
>= 0, regola >= del brief: con
CAPEX nullo il payback e' 0, con
divisione esatta CAPEX /
risparmio il payback e' l'anno
della divisione esatta).
Verdetto: CONVIENTE se VAN > 0,
MARGINALE se VAN < 0 e |VAN| <=
tolleranza % del CAPEX, altrimenti
NON_CONVIENTE; NON_CALCOLABILE e'
il verdetto del caso degenere
(VAN None: nessun calcolo
eseguibile). Regime degenere
SOLLEVA ValueError negli helper
(produzione <= 0, acqua specifica
<= 0, T_in < 0, T_proc <= T_in,
T_scarico <= T_in, T_scarico >=
T_proc, T_proc > 100, eta di
recupero fuori (0, 100] %, COP
<= 1, eta di caldaia fuori
(0, 100] %, prezzo gas < 0, prezzo
elettricita' < 0, fattore gas < 0,
fattore elettricita' < 0, CAPEX
< 0, OM < 0, WACC < 0 o sopra
50 %, vita <= 0 o non intera,
tolleranza fuori [0, 100] %,
input non numerici o non finiti);
la UI lo intercetta PRIMA di KPI,
grafico, tabella e CSV con
st.stop(). In questa tab il
risparmio nullo o negativo NON
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
calore residuo, senza pompa di
calore), dalla vetreria (li' si
fonde il vetro in forni, con
cullet, senza vasche di concia,
senza acqua di processo, senza
scarico caldo da cui recuperare
calore, senza pompa di calore),
dalla fonderia (li' si fonde la
ghisa in forni, con carica
metallica, senza vasche di concia,
senza acqua di processo, senza
scarico caldo, senza pompa di
calore), dall'essiccazione (li'
si seccano solidi togliendo acqua,
legno o pasta, senza vasche di
concia, senza bagno di concia,
senza scarico caldo, senza pompa
di calore) e da una caldaia
generica senza processo (li' il
calore e' generico, senza vasche
di concia, senza pellame, senza
acqua specifica in m3/t, senza
scarico e senza recupero, senza
pompa di calore).

Demo calcolata eseguendo demo_calcoli()
(e ricontrollata a mano, riga per
riga): produzione pellame 4.000
t/anno, acqua specifica 25 m3/t,
temperatura ingresso 15 gradi C,
temperatura processo 38 gradi C,
temperatura scarico 30 gradi C,
rendimento recupero 60 %, COP
pompa di calore 3,5, rendimento
caldaia 90 %, prezzo gas 45
EUR/MWh, prezzo elettricita' 150
EUR/MWh, fattore gas 0,20
tCO2/MWh, fattore elettricita'
0,25 tCO2/MWh, CAPEX 400.000 EUR,
O&M annuo 12.000 EUR/anno, WACC
5 %, vita 15 anni, tolleranza
MARGINALE 10 % del CAPEX.

- volume_m3_anno = 100000.0
- q_fabbisogno_mwh_anno = 2674.3888888888887
- gas_base_mwh_anno = 2971.5432098765427
- q_recuperato_mwh_anno = 1046.5
- q_residuo_mwh_anno = 1627.8888888888887
- e_alt_mwh_anno = 465.11111111111103
- c_base_eur_anno = 133719.4444444444
- c_alt_eur_anno = 81766.66666666666
- co2_base_t_anno = 594.3086419753085
- co2_alt_t_anno = 116.27777777777776
- risparmio_eur_anno = 51952.77777777775
- co2_evitata_t_anno = 478.0308641975308
- lco_base_eur_t = 33.4298611111111
- lco_alt_eur_t = 20.441666666666663
- van = 139252.0674669208
- tir = 9.787354228586363
- payback = 8
- prezzo_pareggio_eur_mwh = 261.6997133301481
- verdetto = 'CONVIENTE'

Scomposizione: volume = 4.000 x 25
= 100.000 m3/anno; fabbisogno =
100.000 x 1000 x 4,186 x (38 -
15) / 3.600.000 = 2.674,388889
MWh/anno; gas base = 2.674,388889
/ 0,90 = 2.971,543210 MWh/anno;
calore recuperato = 100.000 x
1000 x 4,186 x (30 - 15) x 0,60 /
3.600.000 = 1.046,50 MWh/anno;
calore residuo = 2.674,388889 -
1.046,50 = 1.627,888889 MWh/anno;
elettricita' alt = 1.627,888889 /
3,5 = 465,111111 MWh/anno; costo
base = 2.971,543210 x 45 =
133.719,444444 EUR/anno; costo alt
= 465,111111 x 150 + 12.000 =
81.766,666667 EUR/anno; risparmio
= 133.719,444444 - 81.766,666667 =
51.952,777778 EUR/anno; CO2 base =
2.971,543210 x 0,20 = 594,308642
t/anno; CO2 alt = 465,111111 x
0,25 = 116,277778 t/anno; CO2
evitata = 594,308642 - 116,277778 =
478,030864 t/anno; LCO base
133.719,444444 / 4.000 = 33,429861
EUR/t; LCO alt 81.766,666667 /
4.000 = 20,441667 EUR/t; flussi:
anno 0 -400.000, anni 1-15
risparmio 51.952,777778 (piatti);
VAN -400.000 + 51.952,777778 x
10,379658 (annuita' 15 anni al
5 %) = 139.252,07 EUR; TIR 9,79 %;
payback 8 anni (il cumulato
all'anno 8 e' 15.622,22 EUR, gia'
>= 0); prezzo elettricita' di
pareggio (133.719,444444 - 12.000)
/ 465,111111 = 261,699713 EUR/MWh;
verdetto CONVIENTE perche' VAN > 0.
NOTA: il CAPEX non entra nel LCO
di questa tab: entra solo nei
flussi, nella VAN, nella TIR e
nel payback.
NOTA 2: in questa tab il risparmio
nullo o negativo NON e' degenere:
con prezzo gas 0 EUR/MWh il caso
e' calcolabile (valid=True,
flussi pieni), NON_CONVIENTE con
VAN -1.248.710,04 EUR, non un
errore.
NOTA 3: la CO2 evitata ha segno
libero in generale (NON monetizzata):
con fattore elettricita' 1,50
tCO2/MWh la CO2 evitata diventa
-103,36 t/anno e il caso resta
calcolabile e CONVIENTE
economicamente; la funzione pura
resta a segno libero.
NOTA 4: il prezzo elettricita' di
pareggio come valore della
funzione pura e' zero solo se
C_base = OM; con O&M nullo il
pareggio e' 287,50 EUR/MWh
(133.719,444444 / 465,111111).
NOTA 5: il payback usa il cumulato
>= 0 (regola >= del brief): con
CAPEX nullo il payback e' 0 (non
1); con flussi [-100, 50, 50] il
payback e' 2 (il cumulato all'anno
2 e' zero, e zero basta).
NOTA 6: il verdetto MARGINALE
richiede VAN negativa entro la
tolleranza % del CAPEX: con prezzo
elettricita' 183 EUR/MWh la VAN e'
-20.061,84 EUR, entro 40.000 EUR
(10 % di 400.000), quindi
MARGINALE; con tolleranza 0 % lo
stesso caso e' NON_CONVIENTE.
NOTA 7: i valori demo sono stati
ricalcolati da zero: il ricalcolo
esatto (senza arrotondamenti
intermedi) da' volume 100.000,
fabbisogno 2.674,388889, gas base
2.971,543210, recuperato 1.046,50,
residuo 1.627,888889, elettricita'
465,111111, costo base
133.719,444444, costo alt
81.766,666667, risparmio
51.952,777778, CO2 evitata
478,030864, LCO base 33,429861,
LCO alt 20,441667, VAN 139.252,07,
TIR 9,79 %, payback 8 e pareggio
261,699713: i file usano i valori
esatti.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w770_helpers import (
    demo_calcoli,
    mh769_c_alt,
    mh769_c_base,
    mh769_calcola,
    mh769_co2_alt,
    mh769_co2_base,
    mh769_co2_evitata,
    mh769_cop,
    mh769_csv,
    mh769_demo,
    mh769_e_alt,
    mh769_flussi,
    mh769_gas_base,
    mh769_int_pos,
    mh769_lco_alt,
    mh769_lco_base,
    mh769_nneg,
    mh769_num,
    mh769_payback,
    mh769_pct_0_100_escl0,
    mh769_pct_tolleranza,
    mh769_pct_wacc,
    mh769_pos,
    mh769_prezzo_pareggio,
    mh769_q_fabbisogno,
    mh769_q_recuperato,
    mh769_q_residuo,
    mh769_risparmio,
    mh769_tir,
    mh769_valida,
    mh769_van,
    mh769_verdetto,
    mh769_volume,
)


def _demo_kwargs():
    return dict(mh769_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh769_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh769_num(3, "x") == 3.0
    assert mh769_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh769_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh769_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh769_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh769_pos(0, "x")
    with pytest.raises(ValueError):
        mh769_pos(-1, "x")
    assert mh769_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh769_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh769_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh769_int_pos(0, "x")


def test_pct_wacc_limiti():
    assert mh769_pct_wacc(0, "x") == 0.0
    assert mh769_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh769_pct_wacc(50.1, "x")


def test_pct_0_100_escl0_limiti():
    assert mh769_pct_0_100_escl0(100, "x") == 100.0
    assert mh769_pct_0_100_escl0(65.0, "x") == 65.0
    with pytest.raises(ValueError):
        mh769_pct_0_100_escl0(0, "x")
    with pytest.raises(ValueError):
        mh769_pct_0_100_escl0(100.1, "x")
    with pytest.raises(ValueError):
        mh769_pct_0_100_escl0(-1, "x")


def test_pct_tolleranza_limiti():
    assert mh769_pct_tolleranza(0, "x") == 0.0
    assert mh769_pct_tolleranza(100, "x") == 100.0
    assert mh769_pct_tolleranza(10.0, "x") == 10.0
    with pytest.raises(ValueError):
        mh769_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh769_pct_tolleranza(100.1, "x")


def test_cop_limiti():
    assert mh769_cop(3.5, "x") == 3.5
    assert mh769_cop(1.01, "x") == 1.01
    with pytest.raises(ValueError):
        mh769_cop(1.0, "x")
    with pytest.raises(ValueError):
        mh769_cop(0.9, "x")
    with pytest.raises(ValueError):
        mh769_cop(-2.0, "x")


# ---------------------------------------------------------------- fisica base
def test_volume():
    assert mh769_volume(4000, 25) == pytest.approx(100000.0)
    assert mh769_volume(4000, 40) == pytest.approx(160000.0)
    with pytest.raises(ValueError):
        mh769_volume(0, 25)
    with pytest.raises(ValueError):
        mh769_volume(4000, 0)


def test_q_fabbisogno():
    assert mh769_q_fabbisogno(100000.0, 15, 38) == pytest.approx(
        2674.3888888888887)
    assert mh769_q_fabbisogno(160000.0, 15, 38) == pytest.approx(
        4279.022222222222)
    assert mh769_q_fabbisogno(100000.0, 15, 15) == 0.0
    with pytest.raises(ValueError):
        mh769_q_fabbisogno(-1, 15, 38)


def test_gas_base_e_alt():
    assert mh769_gas_base(2674.3888888888887, 0.90) == pytest.approx(
        2971.5432098765427)
    assert mh769_gas_base(2674.3888888888887, 1.0) == pytest.approx(
        2674.3888888888887)
    assert mh769_gas_base(0.0, 0.90) == 0.0
    assert mh769_e_alt(1627.8888888888887, 3.5) == pytest.approx(
        465.11111111111103)
    assert mh769_e_alt(0.0, 3.5) == 0.0
    with pytest.raises(ValueError):
        mh769_gas_base(2674.3888888888887, 0.0)
    with pytest.raises(ValueError):
        mh769_gas_base(2674.3888888888887, 1.1)
    with pytest.raises(ValueError):
        mh769_e_alt(1627.8888888888887, 1.0)


def test_q_recuperato_e_q_residuo():
    assert mh769_q_recuperato(100000.0, 15, 30,
                              0.60) == pytest.approx(1046.5)
    assert mh769_q_recuperato(100000.0, 15, 30,
                              1.0) == pytest.approx(1744.1666666666667)
    assert mh769_q_recuperato(100000.0, 15, 16,
                              0.60) == pytest.approx(69.76666666666667)
    assert mh769_q_residuo(2674.3888888888887, 1046.5) == pytest.approx(
        1627.8888888888887)
    with pytest.raises(ValueError):
        mh769_q_recuperato(100000.0, 15, 30, 0.0)
    with pytest.raises(ValueError):
        mh769_q_recuperato(100000.0, 15, 30, 1.1)
    with pytest.raises(ValueError):
        mh769_q_residuo(-1, 1046.5)


def test_c_base_c_alt():
    assert mh769_c_base(2971.5432098765427, 45) == pytest.approx(
        133719.4444444444)
    assert mh769_c_alt(465.11111111111103, 150,
                       12000) == pytest.approx(81766.66666666666)
    assert mh769_c_alt(465.11111111111103, 150,
                       0) == pytest.approx(69766.66666666666)
    with pytest.raises(ValueError):
        mh769_c_base(2971.5432098765427, -1)
    with pytest.raises(ValueError):
        mh769_c_alt(465.11111111111103, 150, -1)


def test_co2_base_alt_evitata():
    assert mh769_co2_base(2971.5432098765427, 0.20) == pytest.approx(
        594.3086419753085)
    assert mh769_co2_alt(465.11111111111103, 0.25) == pytest.approx(
        116.27777777777776)
    assert mh769_co2_evitata(594.3086419753085,
                             116.27777777777776) == pytest.approx(
        478.0308641975308)
    assert mh769_co2_evitata(100.0, 150.0) == pytest.approx(-50.0)
    with pytest.raises(ValueError):
        mh769_co2_base(2971.5432098765427, -0.10)


def test_risparmio_segno():
    assert mh769_risparmio(133719.4444444444, 81766.66666666666) == \
        pytest.approx(51952.77777777775)
    assert mh769_risparmio(133719.4444444444, 133719.4444444444) == 0.0
    assert mh769_risparmio(133719.4444444444, 174788.88888888888) == \
        pytest.approx(-41069.44444444447)


def test_lco():
    assert mh769_lco_base(133719.4444444444, 4000) == pytest.approx(
        33.4298611111111)
    assert mh769_lco_alt(81766.66666666666, 4000) == pytest.approx(
        20.441666666666663)
    assert mh769_lco_base(133719.4444444444, 0) is None
    assert mh769_lco_alt(81766.66666666666, 0) is None
    assert mh769_lco_alt(81766.66666666666, -5) is None


def test_prezzo_pareggio_formula_zero_e_none():
    assert mh769_prezzo_pareggio(133719.4444444444, 12000,
                                 465.11111111111103) == pytest.approx(
        261.6997133301481)
    assert mh769_prezzo_pareggio(133719.4444444444, 12000,
                                 0.0) is None
    assert mh769_prezzo_pareggio(133719.4444444444, 12000,
                                 -5.0) is None
    assert mh769_prezzo_pareggio(0.0, 12000,
                                 465.11111111111103) == pytest.approx(
        -25.800286669851893)


def test_prezzo_pareggio_om_nullo():
    """Il pareggio con O&M nullo e' C_base / E_alt:
    287,50 EUR/MWh nel caso demo."""
    bc = demo_calcoli()
    assert mh769_prezzo_pareggio(bc["c_base_eur_anno"], 0,
                                 bc["e_alt_mwh_anno"]) == pytest.approx(
        287.5)
    assert bc["prezzo_pareggio_eur_mwh"] > 0.0


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh769_flussi(400000, 51952.77777777775, 15)
    assert len(fl) == 16
    assert fl[0] == -400000
    assert all(f == 51952.77777777775 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = demo_calcoli()
    assert bc["van"] == pytest.approx(139252.0674669208)
    assert mh769_van([-400000] + [51952.77777777775] * 15,
                     0) == pytest.approx(379291.6666666663)
    assert mh769_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = demo_calcoli()
    assert bc["tir"] == pytest.approx(9.787354228586363)
    assert mh769_tir([-400000] + [51952.77777777775] * 15) == \
        pytest.approx(0.09787354228586363)
    tir = mh769_tir([-400000] + [51952.77777777775] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate(
                  [-400000] + [51952.77777777775] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    """Payback con cumulato >= 0: il cumulato nullo basta."""
    assert mh769_payback([-400000] + [51952.77777777775] * 15) == 8
    assert mh769_payback([-400000] + [-1000.0] * 15) is None
    assert mh769_payback([0] + [51952.77777777775] * 15) == 0
    assert mh769_payback([-100] + [50] * 2) == 2
    assert mh769_payback([-103905.5555555555] +
                         [51952.77777777775] * 2) == 2


def test_verdetto():
    assert mh769_verdetto(100.0, 400000, 10.0) == "CONVIENTE"
    assert mh769_verdetto(0.0, 400000, 10.0) == "NON_CONVIENTE"
    assert mh769_verdetto(-20061.843875100265, 400000,
                          10.0) == "MARGINALE"
    assert mh769_verdetto(-20061.843875100265, 400000,
                          0.0) == "NON_CONVIENTE"
    assert mh769_verdetto(-50000.0, 400000, 10.0) == "NON_CONVIENTE"
    assert mh769_verdetto(-100.0, 0, 10.0) == "NON_CONVIENTE"
    assert mh769_verdetto(None, 400000, 10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh769_verdetto(float("nan"), 400000, 10.0)
    with pytest.raises(ValueError):
        mh769_verdetto(100.0, -1, 10.0)
    with pytest.raises(ValueError):
        mh769_verdetto(100.0, 400000, 100.1)


def test_valida_demo_ok():
    v = mh769_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("p_t_anno", "4000"),
                       ("p_t_anno", float("nan")),
                       ("p_t_anno", float("inf")),
                       ("p_t_anno", True),
                       ("prezzo_gas_eur_mwh", None),
                       ("cop", "3,5")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh769_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("p_t_anno", 0),
                          ("p_t_anno", -1),
                          ("acqua_specifica_m3_per_t", 0),
                          ("acqua_specifica_m3_per_t", -1),
                          ("t_in_c", -1),
                          ("t_proc_c", 15),
                          ("t_proc_c", 101),
                          ("t_scarico_c", 15),
                          ("t_scarico_c", 38),
                          ("eta_recupero_pct", 0),
                          ("eta_recupero_pct", 100.1),
                          ("cop", 1.0),
                          ("cop", 0.9),
                          ("eta_caldaia_pct", 0),
                          ("eta_caldaia_pct", 100.1),
                          ("prezzo_gas_eur_mwh", -1),
                          ("prezzo_el_eur_mwh", -1),
                          ("f_gas_t_per_mwh", -0.10),
                          ("f_el_t_per_mwh", -0.10),
                          ("capex_eur", -1),
                          ("om_eur_anno", -100),
                          ("wacc_pct", -0.1), ("wacc_pct", 50.1),
                          ("vita_anni", 0), ("vita_anni", 2.5),
                          ("tolleranza_pct", -1),
                          ("tolleranza_pct", 100.1)):
        d = _demo_kwargs()
        d[campo] = valore
        assert mh769_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"eta_recupero_pct": 100,
              "eta_caldaia_pct": 100,
              "prezzo_gas_eur_mwh": 0,
              "prezzo_el_eur_mwh": 0,
              "f_gas_t_per_mwh": 0,
              "f_el_t_per_mwh": 0,
              "om_eur_anno": 0,
              "capex_eur": 0, "wacc_pct": 0,
              "tolleranza_pct": 0})
    assert mh769_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["t_scarico_c"] = 37
    d["tolleranza_pct"] = 100
    d["cop"] = 8.0
    assert mh769_valida(**d)["valido"] is True


def test_valida_non_controlla_risparmio_calcola_neppure():
    """La validazione input NON controlla il risparmio
    (e' un esito, non un range) e in questa tab
    nemmeno mh769_calcola lo controlla: con prezzo
    gas 0 EUR/MWh il caso resta CALCOLABILE."""
    d = _demo_kwargs()
    d["prezzo_gas_eur_mwh"] = 0
    assert mh769_valida(**d)["valido"] is True
    bc = _variante(prezzo_gas_eur_mwh=0)
    assert bc["valid"] is True
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["flussi"]
    assert bc["tir"] is None
    assert bc["payback"] is None


def test_demo_dict():
    d = mh769_demo()
    assert d["p_t_anno"] == 4000
    assert d["acqua_specifica_m3_per_t"] == 25
    assert d["t_in_c"] == 15
    assert d["t_proc_c"] == 38
    assert d["t_scarico_c"] == 30
    assert d["eta_recupero_pct"] == 60.0
    assert d["cop"] == 3.5
    assert d["eta_caldaia_pct"] == 90.0
    assert d["prezzo_gas_eur_mwh"] == 45
    assert d["prezzo_el_eur_mwh"] == 150
    assert d["f_gas_t_per_mwh"] == 0.20
    assert d["f_el_t_per_mwh"] == 0.25
    assert d["capex_eur"] == 400000
    assert d["om_eur_anno"] == 12000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    """Ogni _DEMO del test contro demo_calcoli():
    scarto relativo < 1e-9 (zero atteso:
    confronto assoluto)."""
    bc = demo_calcoli()
    attesi = {
        "volume_m3_anno": 100000.0,
        "q_fabbisogno_mwh_anno": 2674.3888888888887,
        "gas_base_mwh_anno": 2971.5432098765427,
        "q_recuperato_mwh_anno": 1046.5,
        "q_residuo_mwh_anno": 1627.8888888888887,
        "e_alt_mwh_anno": 465.11111111111103,
        "c_base_eur_anno": 133719.4444444444,
        "c_alt_eur_anno": 81766.66666666666,
        "co2_base_t_anno": 594.3086419753085,
        "co2_alt_t_anno": 116.27777777777776,
        "risparmio_eur_anno": 51952.77777777775,
        "co2_evitata_t_anno": 478.0308641975308,
        "lco_base_eur_t": 33.4298611111111,
        "lco_alt_eur_t": 20.441666666666663,
        "van": 139252.0674669208,
        "tir": 9.787354228586363,
        "prezzo_pareggio_eur_mwh": 261.6997133301481,
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
    assert bc["volume_m3_anno"] == pytest.approx(100000.0)
    assert bc["q_fabbisogno_mwh_anno"] == pytest.approx(2674.3888888888887)
    assert bc["gas_base_mwh_anno"] == pytest.approx(2971.5432098765427)
    assert bc["q_recuperato_mwh_anno"] == pytest.approx(1046.5)
    assert bc["q_residuo_mwh_anno"] == pytest.approx(1627.8888888888887)
    assert bc["e_alt_mwh_anno"] == pytest.approx(465.11111111111103)
    assert bc["co2_evitata_t_anno"] == pytest.approx(478.0308641975308)


def test_demo_calcoli_economia():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(133719.4444444444)
    assert bc["c_alt_eur_anno"] == pytest.approx(81766.66666666666)
    assert bc["risparmio_eur_anno"] == pytest.approx(51952.77777777775)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(
        261.6997133301481)


def test_demo_calcoli_finanza():
    bc = demo_calcoli()
    assert bc["lco_base_eur_t"] == pytest.approx(33.4298611111111)
    assert bc["lco_alt_eur_t"] == pytest.approx(20.441666666666663)
    assert bc["van"] == pytest.approx(139252.0674669208)
    assert bc["tir"] == pytest.approx(9.787354228586363)
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"


def test_demo_flussi_e_cumulato():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -400000
    assert len(bc["flussi"]) == 16
    assert all(f == 51952.77777777775 for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -400000
    assert righe.iloc[7]["Cumulato (EUR)"] == pytest.approx(
        -36330.55555555575)
    assert righe.iloc[8]["Cumulato (EUR)"] == pytest.approx(
        15622.222222222285)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(
        379291.6666666663)
    assert righe.iloc[15]["Flusso (EUR/anno)"] == 51952.77777777775


def test_demo_tabella_righe():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Produzione pellame (t/anno)"] == pytest.approx(4000.0)
    assert mappa["Volume acqua (m3/anno)"] == pytest.approx(100000.0)
    assert mappa["Fabbisogno termico (MWh/anno)"] == pytest.approx(
        2674.3888888888887)
    assert mappa["Gas baseline (MWh/anno)"] == pytest.approx(
        2971.5432098765427)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(
        81766.66666666666)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(
        51952.77777777775)
    assert mappa["Payback (anni)"] == 8
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Prezzo elettricita' di pareggio (EUR/MWh)"] == \
        pytest.approx(261.6997133301481)


def test_demo_coerenza_interna():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["e_alt_mwh_anno"] * bc["prezzo_el_eur_mwh"] + \
        bc["om_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["gas_base_mwh_anno"] * bc["prezzo_gas_eur_mwh"] == \
        pytest.approx(bc["c_base_eur_anno"])
    assert bc["co2_base_t_anno"] - bc["co2_alt_t_anno"] == \
        pytest.approx(bc["co2_evitata_t_anno"])
    assert bc["volume_m3_anno"] == pytest.approx(
        bc["p_t_anno"] * bc["acqua_specifica_m3_per_t"])
    assert bc["q_fabbisogno_mwh_anno"] == pytest.approx(
        bc["volume_m3_anno"] * 1000.0 * 4.186 *
        (bc["t_proc_c"] - bc["t_in_c"]) / 3600000.0)
    assert bc["q_recuperato_mwh_anno"] == pytest.approx(
        bc["volume_m3_anno"] * 1000.0 * 4.186 *
        (bc["t_scarico_c"] - bc["t_in_c"]) *
        bc["eta_recupero_pct"] / 100.0 / 3600000.0)
    assert bc["q_fabbisogno_mwh_anno"] - \
        bc["q_recuperato_mwh_anno"] == pytest.approx(
        bc["q_residuo_mwh_anno"])
    assert bc["q_residuo_mwh_anno"] > 0.0
    assert bc["e_alt_mwh_anno"] == pytest.approx(
        bc["q_residuo_mwh_anno"] / bc["cop"])
    assert bc["gas_base_mwh_anno"] == pytest.approx(
        bc["q_fabbisogno_mwh_anno"] / (bc["eta_caldaia_pct"] / 100.0))
    assert (bc["c_base_eur_anno"] - bc["om_eur_anno"]) / \
        bc["e_alt_mwh_anno"] == \
        pytest.approx(bc["prezzo_pareggio_eur_mwh"])
    assert bc["c_base_eur_anno"] / bc["p_t_anno"] == \
        pytest.approx(bc["lco_base_eur_t"])
    assert bc["c_alt_eur_anno"] / bc["p_t_anno"] == \
        pytest.approx(bc["lco_alt_eur_t"])


def test_demo_contro_riconteggio_indipendente():
    p, acq = 4000, 25
    ti, tp, ts = 15, 38, 30
    er, cop, ec = 60.0, 3.5, 90.0
    pg, pel, fg, fel, om, cx = 45, 150, 0.20, 0.25, 12000, 400000
    wacc, vita = 5.0, 15
    vol = p * acq
    qf = vol * 1000.0 * 4.186 * (tp - ti) / 3600000.0
    gb = qf / (ec / 100.0)
    qr = vol * 1000.0 * 4.186 * (ts - ti) * (er / 100.0) / 3600000.0
    qres = qf - qr
    ea = qres / cop
    cb = gb * pg
    ca = ea * pel + om
    risp = cb - ca
    co2b = gb * fg
    co2a = ea * fel
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    bc = demo_calcoli()
    assert bc["volume_m3_anno"] == pytest.approx(vol)
    assert bc["q_fabbisogno_mwh_anno"] == pytest.approx(qf)
    assert bc["gas_base_mwh_anno"] == pytest.approx(gb)
    assert bc["q_recuperato_mwh_anno"] == pytest.approx(qr)
    assert bc["q_residuo_mwh_anno"] == pytest.approx(qres)
    assert bc["e_alt_mwh_anno"] == pytest.approx(ea)
    assert bc["c_base_eur_anno"] == pytest.approx(cb)
    assert bc["c_alt_eur_anno"] == pytest.approx(ca)
    assert bc["risparmio_eur_anno"] == pytest.approx(risp)
    assert bc["co2_base_t_anno"] == pytest.approx(co2b)
    assert bc["co2_alt_t_anno"] == pytest.approx(co2a)
    assert bc["van"] == pytest.approx(van)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(
        (cb - om) / ea)


# ---------------------------------------------------------------- varianti
def test_demo_conviente():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] > 0.0
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_acqua_specifica_diversa():
    """Sensibilita' richiesta dal brief: acqua specifica
    diversa (40 m3/t)."""
    bc = _variante(acqua_specifica_m3_per_t=40)
    assert bc["valid"] is True
    assert bc["volume_m3_anno"] == pytest.approx(160000.0)
    assert bc["q_fabbisogno_mwh_anno"] == pytest.approx(4279.022222222222)
    assert bc["gas_base_mwh_anno"] == pytest.approx(4754.469135802468)
    assert bc["q_recuperato_mwh_anno"] == pytest.approx(1674.4)
    assert bc["e_alt_mwh_anno"] == pytest.approx(744.1777777777777)
    assert bc["c_base_eur_anno"] == pytest.approx(213951.11111111107)
    assert bc["c_alt_eur_anno"] == pytest.approx(123626.66666666666)
    assert bc["risparmio_eur_anno"] == pytest.approx(90324.44444444441)
    assert bc["van"] == pytest.approx(537536.8458219736)
    assert bc["tir"] == pytest.approx(21.340422600888186)
    assert bc["payback"] == 5
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(
        271.37482083134256)
    assert bc["co2_evitata_t_anno"] == pytest.approx(764.8493827160494)
    assert bc["lco_alt_eur_t"] == pytest.approx(30.906666666666666)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_scarico_vicino_a_ingresso():
    """Sensibilita' richiesta dal brief: scarico a 16
    gradi C, appena sopra l'ingresso a 15 gradi C:
    recupero quasi nullo, risparmio piccolo ma
    positivo, VAN negativa, caso calcolabile."""
    bc = _variante(t_scarico_c=16)
    assert bc["valid"] is True
    assert bc["q_recuperato_mwh_anno"] == pytest.approx(
        69.76666666666667)
    assert bc["q_residuo_mwh_anno"] == pytest.approx(2604.622222222222)
    assert bc["e_alt_mwh_anno"] == pytest.approx(744.1777777777777)
    assert bc["c_alt_eur_anno"] == pytest.approx(123626.66666666666)
    assert bc["risparmio_eur_anno"] == pytest.approx(10092.777777777752)
    assert bc["van"] == pytest.approx(-295240.4180113187)
    assert bc["tir"] == pytest.approx(-10.246517725020057)
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(
        163.56232083134253)
    assert bc["co2_evitata_t_anno"] == pytest.approx(408.2641975308641)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_prezzo_el_marginale():
    """Fascia MARGINALE: prezzo elettricita' 183
    EUR/MWh, VAN negativa entro la tolleranza
    del 10 % del CAPEX."""
    bc = _variante(prezzo_el_eur_mwh=183)
    assert bc["valid"] is True
    assert bc["c_alt_eur_anno"] == pytest.approx(97115.33333333331)
    assert bc["risparmio_eur_anno"] == pytest.approx(36604.111111111095)
    assert bc["van"] == pytest.approx(-20061.843875100265)
    assert bc["tir"] == pytest.approx(4.248400780523124)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"
    bc0 = _variante(prezzo_el_eur_mwh=183, tolleranza_pct=0)
    assert bc0["verdetto"] == "NON_CONVIENTE"
    assert bc0["van"] == pytest.approx(-20061.843875100265)


def test_variante_prezzo_el_alto_non_conviente():
    """Sensibilita' richiesta dal brief: prezzo
    elettricita' alto (250 EUR/MWh, sotto il
    pareggio 261,70 ma con CAPEX alto): VAN
    negativa oltre la tolleranza."""
    bc = _variante(prezzo_el_eur_mwh=250)
    assert bc["valid"] is True
    assert bc["c_alt_eur_anno"] == pytest.approx(128277.77777777775)
    assert bc["risparmio_eur_anno"] == pytest.approx(5441.666666666657)
    assert bc["van"] == pytest.approx(-343517.36084223405)
    assert bc["tir"] == pytest.approx(-15.42285489609554)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["flussi"]


def test_variante_wacc_zero():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(379291.6666666663)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    """Payback regola >=: con CAPEX nullo il payback e' 0,
    non 1 (all'anno 0 il cumulato e' gia' zero)."""
    bc = _variante(capex_eur=0)
    assert bc["capex_eur"] == 0
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(539252.0674669208)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_vita_diversa():
    bc = _variante(vita_anni=20)
    assert len(bc["flussi"]) == 21
    assert bc["van"] == pytest.approx(247446.44454590318)
    assert bc["tir"] == pytest.approx(11.521330015363613)
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_om_zero_pareggio():
    bc = _variante(om_eur_anno=0)
    assert bc["prezzo_pareggio_eur_mwh"] == 287.5
    assert bc["risparmio_eur_anno"] == pytest.approx(63952.77777777775)
    assert bc["van"] == pytest.approx(263807.9639250879)
    assert bc["payback"] == 7
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_eta_recupero_cento():
    bc = _variante(eta_recupero_pct=100)
    assert bc["q_recuperato_mwh_anno"] == pytest.approx(
        1744.1666666666667)
    assert bc["q_residuo_mwh_anno"] == pytest.approx(930.222222222222)
    assert bc["e_alt_mwh_anno"] == pytest.approx(265.7777777777777)
    assert bc["c_alt_eur_anno"] == pytest.approx(51866.66666666666)
    assert bc["risparmio_eur_anno"] == pytest.approx(81852.77777777775)
    assert bc["van"] == pytest.approx(449603.8428085204)
    assert bc["payback"] == 5
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_prezzo_gas_zero_calcolabile():
    bc = _variante(prezzo_gas_eur_mwh=0)
    assert bc["valid"] is True
    assert bc["c_base_eur_anno"] == 0.0
    assert bc["c_alt_eur_anno"] == 81766.66666666666
    assert bc["risparmio_eur_anno"] == -81766.66666666666
    assert bc["van"] == pytest.approx(-1248710.0389218994)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(
        -25.800286669851893)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_scarico_alto():
    bc = _variante(t_scarico_c=37)
    assert bc["q_recuperato_mwh_anno"] == pytest.approx(
        1534.8666666666666)
    assert bc["risparmio_eur_anno"] == pytest.approx(72882.77777777775)
    assert bc["van"] == pytest.approx(356498.31020604057)
    assert bc["tir"] == pytest.approx(16.338222201669222)
    assert bc["payback"] == 6
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_fattore_el_alto_co2_negativa_calcolabile():
    bc = _variante(f_el_t_per_mwh=1.5)
    assert bc["valid"] is True
    assert bc["co2_alt_t_anno"] == pytest.approx(697.6666666666666)
    assert bc["co2_evitata_t_anno"] == pytest.approx(-103.35802469135797)
    assert bc["risparmio_eur_anno"] == pytest.approx(51952.77777777775)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_cop_basso_non_conviente():
    bc = _variante(cop=1.5)
    assert bc["valid"] is True
    assert bc["e_alt_mwh_anno"] == pytest.approx(1085.2592592592591)
    assert bc["c_alt_eur_anno"] == pytest.approx(174788.88888888888)
    assert bc["risparmio_eur_anno"] == pytest.approx(-41069.44444444447)
    assert bc["van"] == pytest.approx(-826286.7891513892)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(
        112.15701999863488)
    assert bc["verdetto"] == "NON_CONVIENTE"


# ---------------------------------------------------------------- degenere
def test_degenere_produzione_zero_sollevela():
    """Caso degenere richiesto dal brief: P = 0
    solleva ValueError."""
    with pytest.raises(ValueError):
        _variante(p_t_anno=0)


def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"p_t_anno": 0}, {"p_t_anno": -1},
               {"acqua_specifica_m3_per_t": 0},
               {"acqua_specifica_m3_per_t": -1},
               {"t_in_c": -1},
               {"t_proc_c": 15},
               {"t_proc_c": 101},
               {"t_scarico_c": 15},
               {"t_scarico_c": 38},
               {"eta_recupero_pct": 0},
               {"eta_recupero_pct": 100.1},
               {"cop": 1.0},
               {"cop": 0.9},
               {"eta_caldaia_pct": 0},
               {"eta_caldaia_pct": 100.1},
               {"prezzo_gas_eur_mwh": -1},
               {"prezzo_el_eur_mwh": -1},
               {"f_gas_t_per_mwh": -0.10},
               {"f_el_t_per_mwh": -0.10},
               {"capex_eur": -1},
               {"om_eur_anno": -100},
               {"wacc_pct": -1}, {"wacc_pct": 60},
               {"vita_anni": 0}, {"vita_anni": 2.5},
               {"tolleranza_pct": -1},
               {"tolleranza_pct": 100.1}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh769_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"p_t_anno": "4000"},
               {"p_t_anno": float("nan")},
               {"prezzo_gas_eur_mwh": float("inf")},
               {"capex_eur": True},
               {"cop": "3,5"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh769_valida(**d)["valido"] is False


def test_risparmio_negativo_non_degenere():
    """Differenza chiave: risparmio negativo resta
    calcolabile, con flussi pieni e VAN negativa."""
    for kw in ({"prezzo_gas_eur_mwh": 0},
               {"cop": 1.5},
               {"prezzo_el_eur_mwh": 250}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] < 0.0 or \
            bc["verdetto"] in ("NON_CONVIENTE", "MARGINALE")
        assert bc["flussi"]


def test_co2_evitata_segno_libero_funzione_pura():
    assert mh769_co2_evitata(100.0, 150.0) == pytest.approx(-50.0)


def test_verdetto_non_calcolabile_solo_van_none():
    assert mh769_verdetto(None, 400000, 10.0) == "NON_CALCOLABILE"
    assert demo_calcoli()["verdetto"] != "NON_CALCOLABILE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = demo_calcoli()
    testo = mh769_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert "volume_m3_anno;100000.0" in testo
    assert "q_fabbisogno_mwh_anno;2674.3888888888887" in testo
    assert "gas_base_mwh_anno;2971.5432098765427" in testo
    assert "e_alt_mwh_anno;465.11111111111103" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "prezzo_pareggio_eur_mwh" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = demo_calcoli()
    testo = mh769_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"gas_base_mwh_anno;{bc['gas_base_mwh_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = demo_calcoli()
    testo = mh769_csv(bc, _demo_kwargs())
    for chiave in _demo_kwargs():
        assert f"{chiave};" in testo


def test_monotonia_prezzo_gas():
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(prezzo_gas_eur_mwh=50)["risparmio_eur_anno"]
    basso = _variante(prezzo_gas_eur_mwh=40)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(14857.716049382713)
    assert base - basso == pytest.approx(14857.716049382713)


def test_monotonia_scarico():
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(t_scarico_c=37)["risparmio_eur_anno"]
    basso = _variante(t_scarico_c=20)["risparmio_eur_anno"]
    assert alto > base > basso


def test_monotonia_cop():
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(cop=5.0)["risparmio_eur_anno"]
    basso = _variante(cop=2.0)["risparmio_eur_anno"]
    assert alto > base > basso


def test_demo_deterministica_due_chiamate():
    a = demo_calcoli()
    b = demo_calcoli()
    assert a["van"] == b["van"]
    assert a["flussi"] == b["flussi"]
    assert a["tir"] == b["tir"]


def test_demo_chiavi_attese():
    assert set(mh769_demo().keys()) == {
        "p_t_anno",
        "acqua_specifica_m3_per_t",
        "t_in_c", "t_proc_c", "t_scarico_c",
        "eta_recupero_pct", "cop", "eta_caldaia_pct",
        "prezzo_gas_eur_mwh", "prezzo_el_eur_mwh",
        "f_gas_t_per_mwh", "f_el_t_per_mwh",
        "capex_eur", "om_eur_anno",
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
    return ["mh" + "76" + "8", "st" + "76" + "8",
            "tab" + "76" + "8", "w" + "76" + "9_",
            "mh" + "76" + "7", "st" + "76" + "7",
            "tab" + "76" + "7", "w" + "76" + "8_"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w770_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w770_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab769:")


def test_registry_chain_tail_and_count():
    """Registry della nuova tab: il frammento UI apre la tab
    numero 769 (la coda della catena termina con la nuova tab
    e il conteggio atteso delle tab e' 769)."""
    src = _leggi("w770_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 769
    assert src.count("with tab769:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w770_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w770_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st769_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert "key=f" not in src and 'key = f' not in src
    assert "st.stop()" in src
    # guard degenere prima di KPI / grafico / tabella / CSV
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w770_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def769[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w770_ui.py")
        usate = set(re.findall(r'_def769\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 17
        assert usate <= set(mh769_demo().keys())


def test_ui_chiavi_demo_coerenti():
    """Ogni _def769[...] letto dalla UI esiste nel dict demo:
    sweep anti-KeyError a render (lezione dello sweep chiavi demo vs UI)."""
    src = _leggi("w770_ui.py")
    usate = set(re.findall(r'_def769\["([^"]+)"\]', src))
    assert usate
    assert len(usate) == 17
    assert usate <= set(mh769_demo().keys())


def test_ui_riferisce_solo_helper_nuovi():
    src = _leggi("w770_ui.py")
    usati = set(re.findall(r'\b(mh\d+_\w+)\b', src))
    assert usati
    assert all(u.startswith("mh769_") for u in usati)


@pytest.mark.parametrize("t_scarico,atteso", [
    (16, 69.76666666666667),
    (30, 1046.5),
    (37, 1534.8666666666666),
])
def test_q_recuperato_parametrizzato(t_scarico, atteso):
    assert mh769_q_recuperato(100000.0, 15, t_scarico,
                              0.60) == pytest.approx(atteso)


@pytest.mark.parametrize("campo,valore", [
    ("p_t_anno", 0), ("p_t_anno", -3),
    ("acqua_specifica_m3_per_t", 0),
    ("acqua_specifica_m3_per_t", -1),
    ("t_in_c", -1),
    ("t_proc_c", 15), ("t_proc_c", 101),
    ("t_scarico_c", 15), ("t_scarico_c", 38),
    ("eta_recupero_pct", 0), ("eta_recupero_pct", 100.1),
    ("cop", 1.0), ("cop", 0.9),
    ("eta_caldaia_pct", 0), ("eta_caldaia_pct", 100.1),
    ("prezzo_gas_eur_mwh", -1),
    ("prezzo_el_eur_mwh", -1),
    ("f_gas_t_per_mwh", -0.10),
    ("f_el_t_per_mwh", -0.10),
    ("capex_eur", -1),
    ("om_eur_anno", -100),
    ("wacc_pct", -0.1), ("wacc_pct", 50.1),
    ("vita_anni", -1), ("vita_anni", 2.5),
    ("tolleranza_pct", -1), ("tolleranza_pct", 100.1),
])
def test_valida_rifiuta_singoli_campi(campo, valore):
    d = _demo_kwargs()
    d[campo] = valore
    assert mh769_valida(**d)["valido"] is False


@pytest.mark.parametrize("campo,valore", [
    ("p_t_anno", 0), ("p_t_anno", -3),
    ("acqua_specifica_m3_per_t", 0),
    ("acqua_specifica_m3_per_t", -1),
    ("t_in_c", -1),
    ("t_proc_c", 15), ("t_proc_c", 101),
    ("t_scarico_c", 15), ("t_scarico_c", 38),
    ("eta_recupero_pct", 0), ("eta_recupero_pct", 100.1),
    ("cop", 1.0), ("cop", 0.9),
    ("eta_caldaia_pct", 0), ("eta_caldaia_pct", 100.1),
    ("prezzo_gas_eur_mwh", -1),
    ("prezzo_el_eur_mwh", -1),
    ("f_gas_t_per_mwh", -0.10),
    ("f_el_t_per_mwh", -0.10),
    ("capex_eur", -1),
    ("om_eur_anno", -100),
    ("wacc_pct", -0.1), ("wacc_pct", 50.1),
    ("vita_anni", -1), ("vita_anni", 2.5),
    ("tolleranza_pct", -1), ("tolleranza_pct", 100.1),
])
def test_calcola_sollevela_singoli_campi(campo, valore):
    d = _demo_kwargs()
    d[campo] = valore
    with pytest.raises(ValueError):
        mh769_calcola(**d)


def test_df_tabella_valori_demo_selezionati():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Produzione pellame (t/anno)"] == 4000.0
    assert mappa["Volume acqua (m3/anno)"] == pytest.approx(100000.0)
    assert mappa["Gas baseline (MWh/anno)"] == pytest.approx(
        2971.5432098765427)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(
        51952.77777777775)
    assert mappa["Verdetto"] == "CONVIENTE"


def test_lco_alt_minore_di_lco_base_demo():
    bc = demo_calcoli()
    assert bc["lco_alt_eur_t"] < bc["lco_base_eur_t"]
    assert bc["lco_base_eur_t"] - bc["lco_alt_eur_t"] == pytest.approx(
        12.988194444444437)
