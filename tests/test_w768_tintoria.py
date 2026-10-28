"""Test tab768 "Tintoria tessile:
recuperare calore dalle acque
reflue di tintura batte scaldare
acqua nuova in caldaia a gas?"

Nuova tab tab768 (tintoria,
file di lavoro w769).
Business case deterministico
del recupero di calore dalle
acque reflue di tintura in
tintoria tessile: volume acqua
V = P x acqua specifica m3/anno;
fabbisogno termico Q_fabbisogno
= V x 1000 x 4,186 x (T_proc -
T_in) / 3.600.000 MWh/anno
(1000 kg/m3, 4,186 kJ/kgK,
3.600.000 kJ/MWh); gas baseline
= Q_fabbisogno / eta_caldaia
MWh/anno (eta come frazione, es.
0,90); calore recuperato =
V x 1000 x 4,186 x (T_scarico -
T_in) x eta_recupero /
3.600.000 MWh/anno; calore
residuo = Q_fabbisogno -
Q_recuperato (sempre maggiore di
zero con i vincoli di validita');
gas alternativo = Q_alt /
eta_caldaia MWh/anno; costo base
= gas base x prezzo gas; costo
alternativo = gas alt x prezzo
gas + OM annuo; CO2 base = gas
base x f_gas; CO2 alt = gas alt
x f_gas; risparmio = costo base
- costo alt; CO2 evitata = CO2
base - CO2 alt, segno libero
(positiva nel caso demo), NON
monetizzata; fattore di emissione
in tCO2/MWh, numericamente uguale
a kg/kWh (1 kg/kWh = 1 t/MWh);
LCO base = costo base / P;
LCO alt = costo alt / P (il CAPEX
NON entra nel LCO di questa tab:
entra nei flussi, nella VAN,
nella TIR e nel payback); prezzo
gas di pareggio = OM / (gas base
- gas alt), None se gas base -
gas alt <= 0; flussi [-CAPEX,
risparmio x vita]; VAN, TIR,
payback (primo anno con cumulato
>= 0, regola >= del brief: con
CAPEX nullo il payback e' 0, con
divisione esatta CAPEX /
risparmio il payback e' l'anno
della divisione esatta).
Verdetto: CONVIENTE se VAN > 0,
altrimenti NON_CONVIENTE
(nessuna fascia MARGINALE in
questa tab). Regime degenere
SOLLEVA ValueError negli helper
(produzione <= 0, acqua specifica
<= 0, T_in < 0, T_proc <= T_in,
T_scarico <= T_in, T_scarico >=
T_proc, T_proc > 100, eta di
recupero fuori (0, 100] %, eta di
caldaia fuori (0, 100] %, prezzo
gas < 0, fattore gas < 0, CAPEX
< 0, OM < 0, WACC < 0 o sopra
50 %, vita <= 0 o non intera,
input non numerici o non finiti);
la UI lo intercetta PRIMA di KPI,
grafico, tabella e CSV con
st.stop(). In questa tab il
risparmio nullo o negativo NON
e' degenere: resta calcolabile e
porta a VAN negativa
(NON_CONVIENTE). La CO2 evitata
negativa NON e' degenere: e' un
numero, non una guard.
Distinta dalla fusione del vetro
o della ghisa (li' si fondono
vetro o metallo in forni, senza
bagno di tintura, senza acqua di
processo, senza scarico caldo da
cui recuperare calore),
dall'evaporazione o
concentrazione (li' si evapora
acqua da un liquido con Brix,
multi-effetto e MVR, senza bagno
di tintura, senza scarico di
tintura, senza recupero da acque
reflue), dall'essiccazione (li'
si seccano solidi togliendo acqua,
senza bagno di tintura, senza
scarico caldo, senza recupero) e
da una caldaia generica senza
processo (li' il calore e'
generico, senza bagno di tintura,
senza acqua specifica in m3/t,
senza scarico e senza recupero).

Demo calcolata eseguendo demo_calcoli()
(e ricontrollata a mano, riga per
riga): produzione tessuto 2.000
t/anno, acqua specifica 80 m3/t,
temperatura ingresso 15 gradi C,
temperatura processo 60 gradi C,
temperatura scarico 40 gradi C,
rendimento recupero 65 %,
rendimento caldaia 90 %, prezzo
gas 45 EUR/MWh, fattore gas 0,20
tCO2/MWh, CAPEX 180.000 EUR,
O&M annuo 8.000 EUR/anno, WACC
5 %, vita 12 anni.

- volume_m3_anno = 160000.0
- q_fabbisogno_mwh_anno = 8372.0
- gas_base_mwh_anno = 9302.222222222223
- q_recuperato_mwh_anno = 3023.222222222222
- q_alt_mwh_anno = 5348.777777777777
- gas_alt_mwh_anno = 5943.0864197530855
- c_base_eur_anno = 418600.0
- c_alt_eur_anno = 275438.8888888888
- co2_base_t_anno = 1860.4444444444446
- co2_alt_t_anno = 1188.617283950617
- risparmio_eur_anno = 143161.11111111118
- co2_evitata_t_anno = 671.8271604938275
- lco_base_eur_t = 209.3
- lco_alt_eur_t = 137.7194444444444
- van = 1088872.9523313858
- tir = 79.46268787362636
- payback = 2
- prezzo_pareggio_eur_mwh = 2.3815649233709424
- verdetto = 'CONVIENTE'

Scomposizione: volume = 2.000 x 80
= 160.000 m3/anno; fabbisogno =
160.000 x 1000 x 4,186 x (60 -
15) / 3.600.000 = 8.372 MWh/anno;
gas base = 8.372 / 0,90 =
9.302,222222 MWh/anno; calore
recuperato = 160.000 x 1000 x
4,186 x (40 - 15) x 0,65 /
3.600.000 = 3.023,222222 MWh/anno;
calore residuo = 8.372 -
3.023,222222 = 5.348,777778
MWh/anno; gas alt = 5.348,777778
/ 0,90 = 5.943,086420 MWh/anno;
costo base = 9.302,222222 x 45 =
418.600 EUR/anno; costo alt =
5.943,086420 x 45 + 8.000 =
275.438,888889 EUR/anno; risparmio
= 418.600 - 275.438,888889 =
143.161,111111 EUR/anno; CO2 base
= 9.302,222222 x 0,20 =
1.860,444444 t/anno; CO2 alt =
5.943,086420 x 0,20 =
1.188,617284 t/anno; CO2 evitata
= 1.860,444444 - 1.188,617284 =
671,827160 t/anno; LCO base
418.600 / 2.000 = 209,30 EUR/t;
LCO alt 275.438,888889 / 2.000 =
137,719444 EUR/t; flussi: anno 0
-180.000, anni 1-12 risparmio
143.161,111111 (piatti); VAN
-180.000 + 143.161,111111 x
8,863252 (annuita' 12 anni al
5 %) = 1.088.872,95 EUR; TIR
79,46 %; payback 2 anni (il
cumulato all'anno 2 e'
106.322,22 EUR, gia' >= 0);
prezzo gas di pareggio 8.000 /
(9.302,222222 - 5.943,086420) =
2,381565 EUR/MWh; verdetto
CONVIENTE perche' VAN > 0.
NOTA: il CAPEX non entra nel LCO
di questa tab: entra solo nei
flussi, nella VAN, nella TIR e
nel payback.
NOTA 2: in questa tab il risparmio
nullo o negativo NON e' degenere:
con prezzo gas 2 EUR/MWh il caso
e' calcolabile (valid=True,
flussi pieni), NON_CONVIENTE con
VAN -191.360,28 EUR, non un
errore.
NOTA 3: la CO2 evitata ha segno
libero in generale (NON monetizzata):
qui con i vincoli di validita'
resta positiva perche' il gas
alternativo e' sempre minore del
gas baseline; la funzione pura
resta a segno libero.
NOTA 4: il prezzo gas di pareggio
come valore della funzione pura
e' zero con O&M nullo: qualsiasi
prezzo gas positivo rende il
recupero conveniente.
NOTA 5: il payback usa il cumulato
>= 0 (regola >= del brief): con
CAPEX nullo il payback e' 0 (non
1); con flussi [-100, 50, 50] il
payback e' 2 (il cumulato all'anno
2 e' zero, e zero basta).
NOTA 6: i valori demo sono stati
ricalcolati da zero: il ricalcolo
esatto (senza arrotondamenti
intermedi) da' volume 160.000,
fabbisogno 8.372, gas base
9.302,222222, recuperato
3.023,222222, residuo
5.348,777778, gas alt
5.943,086420, costo base 418.600,
costo alt 275.438,888889,
risparmio 143.161,111111, CO2
evitata 671,827160, LCO base
209,30, LCO alt 137,719444, VAN
1.088.872,95, TIR 79,46 %,
payback 2 e pareggio 2,381565:
i file usano i valori esatti.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w769_helpers import (
    demo_calcoli,
    mh768_c_alt,
    mh768_c_base,
    mh768_calcola,
    mh768_co2_alt,
    mh768_co2_base,
    mh768_co2_evitata,
    mh768_csv,
    mh768_demo,
    mh768_flussi,
    mh768_gas_alt,
    mh768_gas_base,
    mh768_int_pos,
    mh768_lco_alt,
    mh768_lco_base,
    mh768_nneg,
    mh768_num,
    mh768_payback,
    mh768_pct_0_100_escl0,
    mh768_pct_wacc,
    mh768_pos,
    mh768_prezzo_pareggio,
    mh768_q_alt,
    mh768_q_fabbisogno,
    mh768_q_recuperato,
    mh768_risparmio,
    mh768_tir,
    mh768_valida,
    mh768_van,
    mh768_verdetto,
    mh768_volume,
)


def _demo_kwargs():
    return dict(mh768_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh768_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh768_num(3, "x") == 3.0
    assert mh768_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh768_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh768_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh768_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh768_pos(0, "x")
    with pytest.raises(ValueError):
        mh768_pos(-1, "x")
    assert mh768_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh768_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh768_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh768_int_pos(0, "x")


def test_pct_wacc_limiti():
    assert mh768_pct_wacc(0, "x") == 0.0
    assert mh768_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh768_pct_wacc(50.1, "x")


def test_pct_0_100_escl0_limiti():
    assert mh768_pct_0_100_escl0(100, "x") == 100.0
    assert mh768_pct_0_100_escl0(65.0, "x") == 65.0
    with pytest.raises(ValueError):
        mh768_pct_0_100_escl0(0, "x")
    with pytest.raises(ValueError):
        mh768_pct_0_100_escl0(100.1, "x")
    with pytest.raises(ValueError):
        mh768_pct_0_100_escl0(-1, "x")


# ---------------------------------------------------------------- fisica base
def test_volume():
    assert mh768_volume(2000, 80) == pytest.approx(160000.0)
    assert mh768_volume(2000, 120) == pytest.approx(240000.0)
    with pytest.raises(ValueError):
        mh768_volume(0, 80)
    with pytest.raises(ValueError):
        mh768_volume(2000, 0)


def test_q_fabbisogno():
    assert mh768_q_fabbisogno(160000.0, 15, 60) == pytest.approx(8372.0)
    assert mh768_q_fabbisogno(240000.0, 15, 60) == pytest.approx(12558.0)
    assert mh768_q_fabbisogno(160000.0, 15, 15) == 0.0
    with pytest.raises(ValueError):
        mh768_q_fabbisogno(-1, 15, 60)


def test_gas_base_e_alt():
    assert mh768_gas_base(8372.0, 0.90) == pytest.approx(
        9302.222222222223)
    assert mh768_gas_base(8372.0, 1.0) == pytest.approx(8372.0)
    assert mh768_gas_base(0.0, 0.90) == 0.0
    assert mh768_gas_alt(5348.777777777777, 0.90) == pytest.approx(
        5943.0864197530855)
    assert mh768_gas_alt(0.0, 0.90) == 0.0
    with pytest.raises(ValueError):
        mh768_gas_base(8372.0, 0.0)
    with pytest.raises(ValueError):
        mh768_gas_base(8372.0, 1.1)
    with pytest.raises(ValueError):
        mh768_gas_alt(5348.777777777777, 0.0)


def test_q_recuperato_e_q_alt():
    assert mh768_q_recuperato(160000.0, 15, 40,
                              0.65) == pytest.approx(3023.222222222222)
    assert mh768_q_recuperato(160000.0, 15, 40,
                              1.0) == pytest.approx(4651.111111111111)
    assert mh768_q_recuperato(160000.0, 15, 16,
                              0.65) == pytest.approx(120.92888888888889)
    assert mh768_q_alt(8372.0, 3023.222222222222) == pytest.approx(
        5348.777777777777)
    with pytest.raises(ValueError):
        mh768_q_recuperato(160000.0, 15, 40, 0.0)
    with pytest.raises(ValueError):
        mh768_q_recuperato(160000.0, 15, 40, 1.1)
    with pytest.raises(ValueError):
        mh768_q_alt(-1, 3023.222222222222)


def test_c_base_c_alt():
    assert mh768_c_base(9302.222222222223, 45) == pytest.approx(
        418600.0)
    assert mh768_c_alt(5943.0864197530855, 45,
                       8000) == pytest.approx(275438.8888888888)
    assert mh768_c_alt(5943.0864197530855, 45,
                       0) == pytest.approx(267438.8888888888)
    with pytest.raises(ValueError):
        mh768_c_base(9302.222222222223, -1)
    with pytest.raises(ValueError):
        mh768_c_alt(5943.0864197530855, 45, -1)


def test_co2_base_alt_evitata():
    assert mh768_co2_base(9302.222222222223, 0.20) == pytest.approx(
        1860.4444444444446)
    assert mh768_co2_alt(5943.0864197530855, 0.20) == pytest.approx(
        1188.617283950617)
    assert mh768_co2_evitata(1860.4444444444446,
                             1188.617283950617) == pytest.approx(
        671.8271604938275)
    assert mh768_co2_evitata(100.0, 150.0) == pytest.approx(-50.0)
    with pytest.raises(ValueError):
        mh768_co2_base(9302.222222222223, -0.10)


def test_risparmio_segno():
    assert mh768_risparmio(418600.0, 275438.8888888888) == pytest.approx(
        143161.11111111118)
    assert mh768_risparmio(418600.0, 418600.0) == 0.0
    assert mh768_risparmio(418600.0, 420553.55555555556) == pytest.approx(
        -1953.555555555562)


def test_lco():
    assert mh768_lco_base(418600.0, 2000) == pytest.approx(209.3)
    assert mh768_lco_alt(275438.8888888888, 2000) == pytest.approx(
        137.7194444444444)
    assert mh768_lco_base(418600.0, 0) is None
    assert mh768_lco_alt(275438.8888888888, 0) is None
    assert mh768_lco_alt(275438.8888888888, -5) is None


def test_prezzo_pareggio_formula_zero_e_none():
    assert mh768_prezzo_pareggio(8000, 9302.222222222223,
                                 5943.0864197530855) == pytest.approx(
        2.3815649233709424)
    assert mh768_prezzo_pareggio(0, 9302.222222222223,
                                 5943.0864197530855) == 0.0
    assert mh768_prezzo_pareggio(8000, 100.0, 100.0) is None
    assert mh768_prezzo_pareggio(8000, 50.0, 100.0) is None


def test_prezzo_pareggio_zero_con_om_nullo():
    """Il pareggio zero esiste come valore della
    funzione pura: con O&M nullo il numeratore e'
    zero; in questa tab quel caso resta comunque
    calcolabile (VAN maggiore)."""
    bc = demo_calcoli()
    assert mh768_prezzo_pareggio(0, bc["gas_base_mwh_anno"],
                                 bc["gas_alt_mwh_anno"]) == 0.0
    assert bc["prezzo_pareggio_eur_mwh"] > 0.0


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh768_flussi(180000, 143161.11111111118, 12)
    assert len(fl) == 13
    assert fl[0] == -180000
    assert all(f == 143161.11111111118 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = demo_calcoli()
    assert bc["van"] == pytest.approx(1088872.9523313858)
    assert mh768_van([-180000] + [143161.11111111118] * 12,
                     0) == pytest.approx(1537933.3333333347)
    assert mh768_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = demo_calcoli()
    assert bc["tir"] == pytest.approx(79.46268787362636)
    assert mh768_tir([-180000] + [143161.11111111118] * 12) == \
        pytest.approx(0.7946268787362636)
    tir = mh768_tir([-180000] + [143161.11111111118] * 12)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate(
                  [-180000] + [143161.11111111118] * 12))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    """Payback con cumulato >= 0: il cumulato nullo basta."""
    assert mh768_payback([-180000] + [143161.11111111118] * 12) == 2
    assert mh768_payback([-180000] + [-1000.0] * 12) is None
    assert mh768_payback([0] + [143161.11111111118] * 12) == 0
    assert mh768_payback([-100] + [50] * 2) == 2
    assert mh768_payback([-286322.22222222224] +
                         [143161.11111111118] * 2) == 2


def test_verdetto():
    assert mh768_verdetto(100.0) == "CONVIENTE"
    assert mh768_verdetto(0.0) == "NON_CONVIENTE"
    assert mh768_verdetto(-100.0) == "NON_CONVIENTE"
    with pytest.raises(ValueError):
        mh768_verdetto(float("nan"))


def test_valida_demo_ok():
    v = mh768_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("p_t_anno", "2000"),
                       ("p_t_anno", float("nan")),
                       ("p_t_anno", float("inf")),
                       ("p_t_anno", True),
                       ("prezzo_gas_eur_mwh", None)):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh768_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("p_t_anno", 0),
                          ("p_t_anno", -1),
                          ("acqua_specifica_m3_per_t", 0),
                          ("acqua_specifica_m3_per_t", -1),
                          ("t_in_c", -1),
                          ("t_proc_c", 15),
                          ("t_proc_c", 101),
                          ("t_scarico_c", 15),
                          ("t_scarico_c", 60),
                          ("eta_recupero_pct", 0),
                          ("eta_recupero_pct", 100.1),
                          ("eta_caldaia_pct", 0),
                          ("eta_caldaia_pct", 100.1),
                          ("prezzo_gas_eur_mwh", -1),
                          ("f_gas_t_per_mwh", -0.10),
                          ("capex_eur", -1),
                          ("om_eur_anno", -100),
                          ("wacc_pct", -0.1), ("wacc_pct", 50.1),
                          ("vita_anni", 0), ("vita_anni", 2.5)):
        d = _demo_kwargs()
        d[campo] = valore
        assert mh768_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"eta_recupero_pct": 100,
              "eta_caldaia_pct": 100,
              "prezzo_gas_eur_mwh": 0,
              "f_gas_t_per_mwh": 0,
              "om_eur_anno": 0,
              "capex_eur": 0, "wacc_pct": 0})
    assert mh768_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["t_scarico_c"] = 59
    assert mh768_valida(**d)["valido"] is True


def test_valida_non_controlla_risparmio_calcola_neppure():
    """La validazione input NON controlla il risparmio
    (e' un esito, non un range) e in questa tab
    nemmeno mh768_calcola lo controlla: con prezzo
    gas 2 EUR/MWh il caso resta CALCOLABILE."""
    d = _demo_kwargs()
    d["prezzo_gas_eur_mwh"] = 2
    assert mh768_valida(**d)["valido"] is True
    bc = _variante(prezzo_gas_eur_mwh=2)
    assert bc["valid"] is True
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["flussi"]
    assert bc["tir"] is None
    assert bc["payback"] is None


def test_demo_dict():
    d = mh768_demo()
    assert d["p_t_anno"] == 2000
    assert d["acqua_specifica_m3_per_t"] == 80
    assert d["t_in_c"] == 15
    assert d["t_proc_c"] == 60
    assert d["t_scarico_c"] == 40
    assert d["eta_recupero_pct"] == 65.0
    assert d["eta_caldaia_pct"] == 90.0
    assert d["prezzo_gas_eur_mwh"] == 45
    assert d["f_gas_t_per_mwh"] == 0.20
    assert d["capex_eur"] == 180000
    assert d["om_eur_anno"] == 8000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 12


def test_demo_costanti_vs_demo_calcoli():
    """Ogni _DEMO del test contro demo_calcoli():
    scarto relativo < 1e-9 (zero atteso:
    confronto assoluto)."""
    bc = demo_calcoli()
    attesi = {
        "volume_m3_anno": 160000.0,
        "q_fabbisogno_mwh_anno": 8372.0,
        "gas_base_mwh_anno": 9302.222222222223,
        "q_recuperato_mwh_anno": 3023.222222222222,
        "q_alt_mwh_anno": 5348.777777777777,
        "gas_alt_mwh_anno": 5943.0864197530855,
        "c_base_eur_anno": 418600.0,
        "c_alt_eur_anno": 275438.8888888888,
        "co2_base_t_anno": 1860.4444444444446,
        "co2_alt_t_anno": 1188.617283950617,
        "risparmio_eur_anno": 143161.11111111118,
        "co2_evitata_t_anno": 671.8271604938275,
        "lco_base_eur_t": 209.3,
        "lco_alt_eur_t": 137.7194444444444,
        "van": 1088872.9523313858,
        "tir": 79.46268787362636,
        "prezzo_pareggio_eur_mwh": 2.3815649233709424,
    }
    for chiave, atteso in attesi.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert abs(got - atteso) / abs(atteso) < 1e-9, chiave
    assert bc["payback"] == 2
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_demo_calcoli_fisica():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["volume_m3_anno"] == pytest.approx(160000.0)
    assert bc["q_fabbisogno_mwh_anno"] == pytest.approx(8372.0)
    assert bc["gas_base_mwh_anno"] == pytest.approx(9302.222222222223)
    assert bc["q_recuperato_mwh_anno"] == pytest.approx(3023.222222222222)
    assert bc["q_alt_mwh_anno"] == pytest.approx(5348.777777777777)
    assert bc["gas_alt_mwh_anno"] == pytest.approx(5943.0864197530855)
    assert bc["co2_evitata_t_anno"] == pytest.approx(671.8271604938275)


def test_demo_calcoli_economia():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(418600.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(275438.8888888888)
    assert bc["risparmio_eur_anno"] == pytest.approx(143161.11111111118)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(
        2.3815649233709424)


def test_demo_calcoli_finanza():
    bc = demo_calcoli()
    assert bc["lco_base_eur_t"] == pytest.approx(209.3)
    assert bc["lco_alt_eur_t"] == pytest.approx(137.7194444444444)
    assert bc["van"] == pytest.approx(1088872.9523313858)
    assert bc["tir"] == pytest.approx(79.46268787362636)
    assert bc["payback"] == 2
    assert bc["verdetto"] == "CONVIENTE"


def test_demo_flussi_e_cumulato():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -180000
    assert len(bc["flussi"]) == 13
    assert all(f == 143161.11111111118 for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -180000
    assert righe.iloc[1]["Cumulato (EUR)"] == pytest.approx(
        -36838.88888888882)
    assert righe.iloc[2]["Cumulato (EUR)"] == pytest.approx(
        106322.22222222236)
    assert righe.iloc[12]["Cumulato (EUR)"] == pytest.approx(
        1537933.3333333347)
    assert righe.iloc[12]["Flusso (EUR/anno)"] == 143161.11111111118


def test_demo_tabella_righe():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Produzione tessuto (t/anno)"] == pytest.approx(2000.0)
    assert mappa["Volume acqua (m3/anno)"] == pytest.approx(160000.0)
    assert mappa["Fabbisogno termico (MWh/anno)"] == pytest.approx(
        8372.0)
    assert mappa["Gas baseline (MWh/anno)"] == pytest.approx(
        9302.222222222223)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(
        275438.8888888888)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(
        143161.11111111118)
    assert mappa["Payback (anni)"] == 2
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Prezzo gas di pareggio (EUR/MWh)"] == pytest.approx(
        2.3815649233709424)


def test_demo_coerenza_interna():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["gas_alt_mwh_anno"] * bc["prezzo_gas_eur_mwh"] + \
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
        bc["q_alt_mwh_anno"])
    assert bc["q_alt_mwh_anno"] > 0.0
    assert bc["gas_alt_mwh_anno"] == pytest.approx(
        bc["q_alt_mwh_anno"] / (bc["eta_caldaia_pct"] / 100.0))
    assert bc["om_eur_anno"] / (bc["gas_base_mwh_anno"] -
                                bc["gas_alt_mwh_anno"]) == \
        pytest.approx(bc["prezzo_pareggio_eur_mwh"])
    assert bc["c_base_eur_anno"] / bc["p_t_anno"] == \
        pytest.approx(bc["lco_base_eur_t"])
    assert bc["c_alt_eur_anno"] / bc["p_t_anno"] == \
        pytest.approx(bc["lco_alt_eur_t"])


def test_demo_contro_riconteggio_indipendente():
    p, acq = 2000, 80
    ti, tp, ts = 15, 60, 40
    er, ec = 65.0, 90.0
    pg, fg, om, cx = 45, 0.20, 8000, 180000
    wacc, vita = 5.0, 12
    vol = p * acq
    qf = vol * 1000.0 * 4.186 * (tp - ti) / 3600000.0
    gb = qf / (ec / 100.0)
    qr = vol * 1000.0 * 4.186 * (ts - ti) * (er / 100.0) / 3600000.0
    qa = qf - qr
    ga = qa / (ec / 100.0)
    cb = gb * pg
    ca = ga * pg + om
    risp = cb - ca
    co2b = gb * fg
    co2a = ga * fg
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    bc = demo_calcoli()
    assert bc["volume_m3_anno"] == pytest.approx(vol)
    assert bc["q_fabbisogno_mwh_anno"] == pytest.approx(qf)
    assert bc["gas_base_mwh_anno"] == pytest.approx(gb)
    assert bc["q_recuperato_mwh_anno"] == pytest.approx(qr)
    assert bc["q_alt_mwh_anno"] == pytest.approx(qa)
    assert bc["gas_alt_mwh_anno"] == pytest.approx(ga)
    assert bc["c_base_eur_anno"] == pytest.approx(cb)
    assert bc["c_alt_eur_anno"] == pytest.approx(ca)
    assert bc["risparmio_eur_anno"] == pytest.approx(risp)
    assert bc["co2_base_t_anno"] == pytest.approx(co2b)
    assert bc["co2_alt_t_anno"] == pytest.approx(co2a)
    assert bc["van"] == pytest.approx(van)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(
        om / (gb - ga))


# ---------------------------------------------------------------- varianti
def test_demo_conviente():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] > 0.0
    assert bc["payback"] == 2
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_acqua_specifica_diversa():
    """Sensibilita' richiesta dal brief: acqua specifica
    diversa (120 m3/t)."""
    bc = _variante(acqua_specifica_m3_per_t=120)
    assert bc["valid"] is True
    assert bc["volume_m3_anno"] == pytest.approx(240000.0)
    assert bc["q_fabbisogno_mwh_anno"] == pytest.approx(12558.0)
    assert bc["gas_base_mwh_anno"] == pytest.approx(13953.333333333332)
    assert bc["q_recuperato_mwh_anno"] == pytest.approx(
        4534.833333333333)
    assert bc["gas_alt_mwh_anno"] == pytest.approx(8914.62962962963)
    assert bc["c_base_eur_anno"] == pytest.approx(627900.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(409158.3333333333)
    assert bc["risparmio_eur_anno"] == pytest.approx(218741.6666666667)
    assert bc["van"] == pytest.approx(1758762.4350428728)
    assert bc["tir"] == pytest.approx(121.51444183141305)
    assert bc["payback"] == 1
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(
        1.5877099489139626)
    assert bc["co2_evitata_t_anno"] == pytest.approx(1007.7407407407404)
    assert bc["lco_alt_eur_t"] == pytest.approx(204.57916666666665)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_scarico_vicino_a_ingresso_risparmio_piccolo():
    """Sensibilita' richiesta dal brief: scarico a 16
    gradi C, appena sopra l'ingresso a 15 gradi C:
    recupero quasi nullo, risparmio piccolo e
    negativo, caso calcolabile."""
    bc = _variante(t_scarico_c=16)
    assert bc["valid"] is True
    assert bc["q_recuperato_mwh_anno"] == pytest.approx(
        120.92888888888889)
    assert bc["q_alt_mwh_anno"] == pytest.approx(8251.07111111111)
    assert bc["gas_alt_mwh_anno"] == pytest.approx(9167.856790123456)
    assert bc["c_alt_eur_anno"] == pytest.approx(420553.55555555556)
    assert bc["risparmio_eur_anno"] == pytest.approx(-1953.555555555562)
    assert bc["van"] == pytest.approx(-197314.85447467153)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(
        59.53912308427326)
    assert bc["co2_evitata_t_anno"] == pytest.approx(26.873086419753236)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_prezzo_gas_basso_non_conviente():
    """Sensibilita' richiesta dal brief: prezzo gas
    basso (2 EUR/MWh, sotto il pareggio 2,38):
    risparmio negativo, caso calcolabile."""
    bc = _variante(prezzo_gas_eur_mwh=2)
    assert bc["valid"] is True
    assert bc["c_base_eur_anno"] == pytest.approx(18604.444444444445)
    assert bc["c_alt_eur_anno"] == pytest.approx(19886.172839506173)
    assert bc["risparmio_eur_anno"] == pytest.approx(-1281.7283950617275)
    assert bc["van"] == pytest.approx(-191360.28129501376)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["lco_alt_eur_t"] == pytest.approx(9.943086419753087)
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["flussi"]


def test_variante_wacc_zero():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(1537933.3333333347)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    """Payback regola >=: con CAPEX nullo il payback e' 0,
    non 1 (all'anno 0 il cumulato e' gia' zero)."""
    bc = _variante(capex_eur=0)
    assert bc["capex_eur"] == 0
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(1268872.9523313858)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_vita_diversa():
    bc = _variante(vita_anni=20)
    assert len(bc["flussi"]) == 21
    assert bc["van"] == pytest.approx(1604103.8795384057)
    assert bc["tir"] == pytest.approx(79.53329348534389)
    assert bc["payback"] == 2
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_om_zero_pareggio_zero():
    bc = _variante(om_eur_anno=0)
    assert bc["prezzo_pareggio_eur_mwh"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(151161.11111111118)
    assert bc["van"] == pytest.approx(1159778.9654229763)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_eta_recupero_cento():
    bc = _variante(eta_recupero_pct=100)
    assert bc["q_recuperato_mwh_anno"] == pytest.approx(
        4651.111111111111)
    assert bc["q_alt_mwh_anno"] == pytest.approx(3720.8888888888887)
    assert bc["gas_alt_mwh_anno"] == pytest.approx(4134.320987654321)
    assert bc["c_alt_eur_anno"] == pytest.approx(194044.44444444444)
    assert bc["risparmio_eur_anno"] == pytest.approx(224555.55555555556)
    assert bc["van"] == pytest.approx(1810292.395251449)
    assert bc["payback"] == 1
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_prezzo_gas_zero_calcolabile():
    bc = _variante(prezzo_gas_eur_mwh=0)
    assert bc["valid"] is True
    assert bc["c_base_eur_anno"] == 0.0
    assert bc["c_alt_eur_anno"] == 8000.0
    assert bc["risparmio_eur_anno"] == -8000.0
    assert bc["van"] == pytest.approx(-250906.01309159046)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_scarico_alto():
    bc = _variante(t_scarico_c=59)
    assert bc["q_recuperato_mwh_anno"] == pytest.approx(
        5320.8711111111115)
    assert bc["risparmio_eur_anno"] == pytest.approx(258043.5555555556)
    assert bc["van"] == pytest.approx(2107104.966052847)
    assert bc["payback"] == 1
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_fattore_gas_zero_calcolabile():
    bc = _variante(f_gas_t_per_mwh=0)
    assert bc["valid"] is True
    assert bc["co2_base_t_anno"] == 0.0
    assert bc["co2_alt_t_anno"] == 0.0
    assert bc["co2_evitata_t_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(143161.11111111118)


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
               {"t_scarico_c": 60},
               {"eta_recupero_pct": 0},
               {"eta_recupero_pct": 100.1},
               {"eta_caldaia_pct": 0},
               {"eta_caldaia_pct": 100.1},
               {"prezzo_gas_eur_mwh": -1},
               {"f_gas_t_per_mwh": -0.10},
               {"capex_eur": -1},
               {"om_eur_anno": -100},
               {"wacc_pct": -1}, {"wacc_pct": 60},
               {"vita_anni": 0}, {"vita_anni": 2.5}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh768_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"p_t_anno": "2000"},
               {"p_t_anno": float("nan")},
               {"prezzo_gas_eur_mwh": float("inf")},
               {"capex_eur": True}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh768_valida(**d)["valido"] is False


def test_risparmio_negativo_non_degenere():
    """Differenza chiave: risparmio negativo resta
    calcolabile, con flussi pieni e VAN negativa."""
    for kw in ({"prezzo_gas_eur_mwh": 2},
               {"t_scarico_c": 16},
               {"prezzo_gas_eur_mwh": 0}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] < 0.0
        assert bc["verdetto"] == "NON_CONVIENTE"
        assert bc["flussi"]


def test_co2_evitata_segno_libero_funzione_pura():
    assert mh768_co2_evitata(100.0, 150.0) == pytest.approx(-50.0)


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = demo_calcoli()
    testo = mh768_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert "volume_m3_anno;160000.0" in testo
    assert "q_fabbisogno_mwh_anno;8372.0" in testo
    assert "gas_base_mwh_anno;9302.222222222223" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "prezzo_pareggio_eur_mwh" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = demo_calcoli()
    testo = mh768_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"gas_base_mwh_anno;{bc['gas_base_mwh_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = demo_calcoli()
    testo = mh768_csv(bc, _demo_kwargs())
    for chiave in _demo_kwargs():
        assert f"{chiave};" in testo


def test_monotonia_prezzo_gas():
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(prezzo_gas_eur_mwh=50)["risparmio_eur_anno"]
    basso = _variante(prezzo_gas_eur_mwh=40)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(16795.67901234568)
    assert base - basso == pytest.approx(16795.67901234568)


def test_monotonia_scarico():
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(t_scarico_c=50)["risparmio_eur_anno"]
    basso = _variante(t_scarico_c=30)["risparmio_eur_anno"]
    assert alto > base > basso


def test_demo_deterministica_due_chiamate():
    a = demo_calcoli()
    b = demo_calcoli()
    assert a["van"] == b["van"]
    assert a["flussi"] == b["flussi"]
    assert a["tir"] == b["tir"]


def test_demo_chiavi_attese():
    assert set(mh768_demo().keys()) == {
        "p_t_anno",
        "acqua_specifica_m3_per_t",
        "t_in_c", "t_proc_c", "t_scarico_c",
        "eta_recupero_pct", "eta_caldaia_pct",
        "prezzo_gas_eur_mwh", "f_gas_t_per_mwh",
        "capex_eur", "om_eur_anno",
        "wacc_pct", "vita_anni"}


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
    return ["mh" + "76" + "7", "st" + "76" + "7",
            "tab" + "76" + "7", "w" + "76" + "8_",
            "mh" + "76" + "6", "st" + "76" + "6",
            "tab" + "76" + "6", "w" + "76" + "7_"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w769_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w769_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab768:")


def test_registry_chain_tail_and_count():
    """Registry della nuova tab: il frammento UI apre la tab
    numero 768 (la coda della catena termina con la nuova tab
    e il conteggio atteso delle tab e' 768)."""
    src = _leggi("w769_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 768
    assert src.count("with tab768:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w769_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w769_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st768_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert "key=f" not in src and 'key = f' not in src
    assert "st.stop()" in src
    # guard degenere prima di KPI / grafico / tabella / CSV
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w769_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def768[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w769_ui.py")
        usate = set(re.findall(r'_def768\["([^"]+)"\]', src))
        assert usate
        assert usate <= set(mh768_demo().keys())


def test_ui_chiavi_demo_coerenti():
    """Ogni _def768[...] letto dalla UI esiste nel dict demo:
    sweep anti-KeyError a render (lezione dello sweep chiavi demo vs UI)."""
    src = _leggi("w769_ui.py")
    usate = set(re.findall(r'_def768\["([^"]+)"\]', src))
    assert usate
    assert usate <= set(mh768_demo().keys())


def test_ui_riferisce_solo_helper_nuovi():
    src = _leggi("w769_ui.py")
    usati = set(re.findall(r'\b(mh\d+_\w+)\b', src))
    assert usati
    assert all(u.startswith("mh768_") for u in usati)


@pytest.mark.parametrize("t_scarico,atteso", [
    (16, 120.92888888888889),
    (40, 3023.222222222222),
    (59, 5320.8711111111115),
])
def test_q_recuperato_parametrizzato(t_scarico, atteso):
    assert mh768_q_recuperato(160000.0, 15, t_scarico,
                              0.65) == pytest.approx(atteso)


@pytest.mark.parametrize("campo,valore", [
    ("p_t_anno", 0), ("p_t_anno", -3),
    ("acqua_specifica_m3_per_t", 0),
    ("acqua_specifica_m3_per_t", -1),
    ("t_in_c", -1),
    ("t_proc_c", 15), ("t_proc_c", 101),
    ("t_scarico_c", 15), ("t_scarico_c", 60),
    ("eta_recupero_pct", 0), ("eta_recupero_pct", 100.1),
    ("eta_caldaia_pct", 0), ("eta_caldaia_pct", 100.1),
    ("prezzo_gas_eur_mwh", -1),
    ("f_gas_t_per_mwh", -0.10),
    ("capex_eur", -1),
    ("om_eur_anno", -100),
    ("wacc_pct", -0.1), ("wacc_pct", 50.1),
    ("vita_anni", -1), ("vita_anni", 2.5),
])
def test_valida_rifiuta_singoli_campi(campo, valore):
    d = _demo_kwargs()
    d[campo] = valore
    assert mh768_valida(**d)["valido"] is False


@pytest.mark.parametrize("campo,valore", [
    ("p_t_anno", 0), ("p_t_anno", -3),
    ("acqua_specifica_m3_per_t", 0),
    ("acqua_specifica_m3_per_t", -1),
    ("t_in_c", -1),
    ("t_proc_c", 15), ("t_proc_c", 101),
    ("t_scarico_c", 15), ("t_scarico_c", 60),
    ("eta_recupero_pct", 0), ("eta_recupero_pct", 100.1),
    ("eta_caldaia_pct", 0), ("eta_caldaia_pct", 100.1),
    ("prezzo_gas_eur_mwh", -1),
    ("f_gas_t_per_mwh", -0.10),
    ("capex_eur", -1),
    ("om_eur_anno", -100),
    ("wacc_pct", -0.1), ("wacc_pct", 50.1),
    ("vita_anni", -1), ("vita_anni", 2.5),
])
def test_calcola_sollevela_singoli_campi(campo, valore):
    d = _demo_kwargs()
    d[campo] = valore
    with pytest.raises(ValueError):
        mh768_calcola(**d)


def test_df_tabella_valori_demo_selezionati():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Produzione tessuto (t/anno)"] == 2000.0
    assert mappa["Volume acqua (m3/anno)"] == pytest.approx(160000.0)
    assert mappa["Gas baseline (MWh/anno)"] == pytest.approx(
        9302.222222222223)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(
        143161.11111111118)
    assert mappa["Verdetto"] == "CONVIENTE"


def test_lco_alt_minore_di_lco_base_demo():
    bc = demo_calcoli()
    assert bc["lco_alt_eur_t"] < bc["lco_base_eur_t"]
    assert bc["lco_base_eur_t"] - bc["lco_alt_eur_t"] == pytest.approx(
        71.5805555555556)
