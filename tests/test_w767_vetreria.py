"""Test tab767 "Vetreria:
fondere il vetro con forno
ossi-combustibile + boost
elettrico batte il forno
rigenerativo a gas?"

Nuova tab tab767 (vetreria,
file di lavoro w768).
Business case deterministico
della fusione del vetro in
vetreria: consumo specifico
baseline e_base = 5,0 x
(1 - 0,0025 x cullet%) GJ/t
(a cullet 0 %: 5,0 GJ/t; a
cullet 100 %: 3,75 GJ/t);
gas baseline = P x e_base /
3,6 MWh/anno (1 MWh = 3,6 GJ);
gas alternativo = 0,65 x gas
baseline (ossi-combustibile);
elettricita' boost = 0,08 x P
MWh/anno (80 kWh/t); costo
base = gas base x prezzo gas;
costo variabile alternativo =
gas alt x prezzo gas + el alt x
prezzo elettrico; costo
alternativo = costo variabile
alternativo + OM annuo; CO2
base = gas base x f_gas; CO2
alt = gas alt x f_gas + el alt
x f_el; risparmio = costo base
- costo alt; CO2 evitata = CO2
base - CO2 alt, segno libero
(puo' essere negativa), NON
monetizzata; fattori di emissione
in tCO2/MWh, numericamente uguali
a kg/kWh (1 kg/kWh = 1 t/MWh);
LCO base = costo base / P;
LCO alt = costo alt / P (il CAPEX
NON entra nel LCO di questa tab:
entra nei flussi, nella VAN,
nella TIR e nel payback); prezzo
elettrico di pareggio =
(costo base - gas alt x prezzo
gas - OM) / el alt, None se
el alt <= 0; flussi [-CAPEX,
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
(produzione <= 0, cullet fuori
[0, 100], prezzi negativi,
CAPEX < 0, OM < 0, WACC < 0 o
sopra 50 %, vita <= 0 o non
intera, fattori negativi, input
non numerici o non finiti); la
UI lo intercetta PRIMA di KPI,
grafico, tabella e CSV con
st.stop(). In questa tab il
risparmio nullo o negativo NON
e' degenere: resta calcolabile e
porta a VAN negativa
(NON_CONVIENTE). La CO2 evitata
negativa NON e' degenere: e' un
numero, non una guard.
Distinta dalla fusione della
ghisa (li' si fonde metallo,
senza vetro, senza cullet, senza
forno ossi-combustibile, senza
boost elettrico in MWh/t), dalla
concentrazione del succo (li' si
evapora acqua da succo con Brix,
multi-effetto e MVR, senza vetro,
senza cullet, senza forno),
dall'essiccazione (li' si seccano
solidi, senza fusione di vetro,
senza cullet, senza forno
ossi-combustibile) e da una
caldaia generica (li' il calore
e' generico, senza vetro, senza
cullet, senza fusione).

Demo calcolata eseguendo demo_calcoli()
(e ricontrollata a mano, riga per
riga): produzione vetro 30.000
t/anno, cullet 40 %, prezzo gas
45 EUR/MWh, prezzo elettrico 110
EUR/MWh, CAPEX 1.000.000 EUR,
O&M annuo 60.000 EUR/anno, WACC
5 %, vita 15 anni, fattore gas
0,20 tCO2/MWh e fattore elettrico
0,25 tCO2/MWh.

- e_base_gj_per_t = 4.5
- gas_base_mwh_anno = 37500.0
- gas_alt_mwh_anno = 24375.0
- el_alt_mwh_anno = 2400.0
- c_base_eur_anno = 1687500.0
- c_alt_var_eur_anno = 1360875.0
- c_alt_eur_anno = 1420875.0
- co2_base_t_anno = 7500.0
- co2_alt_t_anno = 5475.0
- risparmio_eur_anno = 266625.0
- co2_evitata_t_anno = 2025.0
- lco_base_eur_t = 56.25
- lco_alt_eur_t = 47.3625
- van = 1767476.3244299
- tir = 25.81113746280782
- payback = 4
- prezzo_pareggio_eur_mwh = 221.09375
- verdetto = 'CONVIENTE'

Scomposizione: e_base = 5,0 x
(1 - 0,0025 x 40) = 5,0 x 0,90 =
4,5 GJ/t; gas base = 30.000 x 4,5
/ 3,6 = 37.500 MWh/anno; gas alt
= 0,65 x 37.500 = 24.375 MWh/anno;
el alt = 0,08 x 30.000 = 2.400
MWh/anno; costo base = 37.500 x
45 = 1.687.500 EUR/anno; costo
variabile alt = 24.375 x 45 +
2.400 x 110 = 1.096.875 + 264.000
= 1.360.875 EUR/anno; costo alt =
1.360.875 + 60.000 = 1.420.875
EUR/anno; risparmio = 1.687.500 -
1.420.875 = 266.625 EUR/anno;
CO2 base = 37.500 x 0,20 = 7.500
t/anno; CO2 alt = 24.375 x 0,20 +
2.400 x 0,25 = 4.875 + 600 =
5.475 t/anno; CO2 evitata = 7.500
- 5.475 = 2.025 t/anno; LCO base
1.687.500 / 30.000 = 56,25 EUR/t;
LCO alt 1.420.875 / 30.000 =
47,3625 EUR/t; flussi: anno 0
-1.000.000, anni 1-15 risparmio
266.625 (piatti); VAN -1.000.000
+ 266.625 x 10,379658 (annuita'
15 anni al 5 %) = 1.767.476,32
EUR; TIR 25,81 %; payback 4 anni
(il cumulato all'anno 4 e'
66.500 EUR, gia' >= 0); prezzo
elettrico di pareggio (1.687.500
- 24.375 x 45 - 60.000) / 2.400 =
221,09375 EUR/MWh; verdetto
CONVIENTE perche' VAN > 0.
NOTA: il CAPEX non entra nel LCO
di questa tab: entra solo nei
flussi, nella VAN, nella TIR e
nel payback.
NOTA 2: in questa tab il risparmio
nullo o negativo NON e' degenere:
con prezzo elettrico 400 EUR/MWh
il caso e' calcolabile (valid=True,
flussi pieni), NON_CONVIENTE con
VAN -5.456.765,67 EUR, non un
errore.
NOTA 3: la CO2 evitata puo' essere
negativa in generale (segno libero,
NON monetizzata): con fattore
elettrico 2,00 tCO2/MWh la CO2
evitata e' -2.175 t/anno pur
restando il caso calcolabile e
CONVIENTE.
NOTA 4: il prezzo elettrico di
pareggio come valore della funzione
pura puo' essere negativo: con O&M
annuo 5.000.000 il pareggio e'
-1.837,24 EUR/MWh circa, perche'
il solo costo gas residuo piu' O&M
supera gia' il costo baseline
(ma il caso resta calcolabile in
questa tab, con VAN negativa).
NOTA 5: il payback usa il cumulato
>= 0 (regola >= del brief): con
CAPEX nullo il payback e' 0 (non
1); con flussi [-100, 50, 50] il
payback e' 2 (il cumulato all'anno
2 e' zero, e zero basta).
NOTA 6: i valori demo sono stati
ricalcolati da zero: il ricalcolo
esatto (senza arrotondamenti
intermedi) da' e_base 4,5, gas
base 37.500, gas alt 24.375, el
alt 2.400, costo base 1.687.500,
costo alt 1.420.875, risparmio
266.625, CO2 evitata 2.025, LCO
base 56,25, LCO alt 47,3625, VAN
1.767.476,32, TIR 25,81 %,
payback 4 e pareggio 221,09375:
i file usano i valori esatti.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w768_helpers import (
    demo_calcoli,
    mh767_c_alt,
    mh767_c_alt_var,
    mh767_c_base,
    mh767_calcola,
    mh767_co2_alt,
    mh767_co2_base,
    mh767_co2_evitata,
    mh767_csv,
    mh767_demo,
    mh767_e_base,
    mh767_el_alt,
    mh767_flussi,
    mh767_gas_alt,
    mh767_gas_base,
    mh767_int_pos,
    mh767_lco_alt,
    mh767_lco_base,
    mh767_nneg,
    mh767_num,
    mh767_payback,
    mh767_pct_0_100,
    mh767_pct_wacc,
    mh767_pos,
    mh767_prezzo_pareggio,
    mh767_risparmio,
    mh767_tir,
    mh767_valida,
    mh767_van,
    mh767_verdetto,
)


def _demo_kwargs():
    return dict(mh767_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh767_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh767_num(3, "x") == 3.0
    assert mh767_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh767_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh767_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh767_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh767_pos(0, "x")
    with pytest.raises(ValueError):
        mh767_pos(-1, "x")
    assert mh767_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh767_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh767_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh767_int_pos(0, "x")


def test_pct_0_100_limiti():
    assert mh767_pct_0_100(0, "x") == 0.0
    assert mh767_pct_0_100(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh767_pct_0_100(100.1, "x")
    with pytest.raises(ValueError):
        mh767_pct_0_100(-1, "x")


def test_pct_wacc_limiti():
    assert mh767_pct_wacc(0, "x") == 0.0
    assert mh767_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh767_pct_wacc(50.1, "x")


# ---------------------------------------------------------------- fisica base
def test_e_base():
    assert mh767_e_base(40.0) == pytest.approx(4.5)
    assert mh767_e_base(0) == pytest.approx(5.0)
    assert mh767_e_base(100) == pytest.approx(3.75)
    assert mh767_e_base(50.0) == pytest.approx(4.375)
    with pytest.raises(ValueError):
        mh767_e_base(-1)
    with pytest.raises(ValueError):
        mh767_e_base(100.1)


def test_gas_base_gas_alt_el_alt():
    assert mh767_gas_base(30000, 4.5) == pytest.approx(37500.0)
    assert mh767_gas_base(30000, 5.0) == pytest.approx(41666.666666666664)
    assert mh767_gas_base(30000, 3.75) == pytest.approx(31250.0)
    assert mh767_gas_base(0, 4.5) == 0.0
    assert mh767_gas_alt(37500.0) == pytest.approx(24375.0)
    assert mh767_gas_alt(0.0) == 0.0
    assert mh767_el_alt(30000) == pytest.approx(2400.0)
    assert mh767_el_alt(0) == 0.0
    with pytest.raises(ValueError):
        mh767_gas_base(-1, 4.5)
    with pytest.raises(ValueError):
        mh767_gas_alt(-1)
    with pytest.raises(ValueError):
        mh767_el_alt(-1)


def test_c_base_c_alt_var_c_alt():
    assert mh767_c_base(37500.0, 45) == pytest.approx(1687500.0)
    assert mh767_c_alt_var(24375.0, 45, 2400.0, 110) == pytest.approx(
        1360875.0)
    assert mh767_c_alt_var(0.0, 45, 0.0, 110) == 0.0
    assert mh767_c_alt(1360875.0, 60000) == pytest.approx(1420875.0)
    assert mh767_c_alt(1360875.0, 0) == pytest.approx(1360875.0)
    with pytest.raises(ValueError):
        mh767_c_base(37500.0, -1)
    with pytest.raises(ValueError):
        mh767_c_alt_var(24375.0, 45, 2400.0, -1)
    with pytest.raises(ValueError):
        mh767_c_alt(1360875.0, -1)


def test_co2_base_alt_evitata_segno_libero():
    assert mh767_co2_base(37500.0, 0.20) == pytest.approx(7500.0)
    assert mh767_co2_alt(24375.0, 0.20, 2400.0, 0.25) == pytest.approx(
        5475.0)
    assert mh767_co2_evitata(7500.0, 5475.0) == pytest.approx(2025.0)
    assert mh767_co2_alt(24375.0, 0.20, 2400.0, 2.0) == pytest.approx(
        9675.0)
    assert mh767_co2_evitata(7500.0, 9675.0) == pytest.approx(-2175.0)
    with pytest.raises(ValueError):
        mh767_co2_base(37500.0, -0.10)


def test_risparmio_segno():
    assert mh767_risparmio(1687500.0, 1420875.0) == pytest.approx(
        266625.0)
    assert mh767_risparmio(1687500.0, 1687500.0) == 0.0
    assert mh767_risparmio(1687500.0, 2116875.0) == pytest.approx(
        -429375.0)


def test_lco():
    assert mh767_lco_base(1687500.0, 30000) == pytest.approx(56.25)
    assert mh767_lco_alt(1420875.0, 30000) == pytest.approx(47.3625)
    assert mh767_lco_base(1687500.0, 0) is None
    assert mh767_lco_alt(1420875.0, 0) is None
    assert mh767_lco_alt(1420875.0, -5) is None


def test_prezzo_pareggio_formula_negativo_e_none():
    assert mh767_prezzo_pareggio(1687500.0, 24375.0, 45, 60000,
                                 2400.0) == pytest.approx(221.09375)
    assert mh767_prezzo_pareggio(1687500.0, 24375.0, 45, 60000,
                                 0.0) is None
    assert mh767_prezzo_pareggio(1687500.0, 24375.0, 45, 60000,
                                 None) is None


def test_prezzo_pareggio_negativo_solo_funzione_pura():
    """Il pareggio negativo esiste come valore della
    funzione pura: con O&M annuo 5.000.000 il numeratore e'
    negativo; in questa tab quel caso resta comunque
    calcolabile (VAN negativa)."""
    bc = demo_calcoli()
    assert mh767_prezzo_pareggio(bc["c_base_eur_anno"],
                                 bc["gas_alt_mwh_anno"], 45, 5000000,
                                 bc["el_alt_mwh_anno"]) == pytest.approx(
        -1837.2395833333333)
    assert bc["prezzo_pareggio_eur_mwh"] > 0.0


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh767_flussi(1000000, 266625.0, 15)
    assert len(fl) == 16
    assert fl[0] == -1000000
    assert all(f == 266625.0 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = demo_calcoli()
    assert bc["van"] == pytest.approx(1767476.3244299)
    assert mh767_van([-1000000] + [266625.0] * 15,
                     0) == pytest.approx(2999375.0)
    assert mh767_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = demo_calcoli()
    assert bc["tir"] == pytest.approx(25.81113746280782)
    assert mh767_tir([-1000000] + [266625.0] * 15) == pytest.approx(
        0.2581113746280782)
    tir = mh767_tir([-1000000] + [266625.0] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-1000000] + [266625.0] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    """Payback con cumulato >= 0: il cumulato nullo basta."""
    assert mh767_payback([-1000000] + [266625.0] * 15) == 4
    assert mh767_payback([-1000000] + [-1000.0] * 15) is None
    assert mh767_payback([0] + [266625.0] * 15) == 0
    assert mh767_payback([-100] + [50] * 2) == 2
    assert mh767_payback([-1066500] + [266625.0] * 4) == 4


def test_verdetto():
    assert mh767_verdetto(100.0) == "CONVIENTE"
    assert mh767_verdetto(0.0) == "NON_CONVIENTE"
    assert mh767_verdetto(-100.0) == "NON_CONVIENTE"
    with pytest.raises(ValueError):
        mh767_verdetto(float("nan"))


def test_valida_demo_ok():
    v = mh767_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("p_t_anno", "30000"),
                       ("p_t_anno", float("nan")),
                       ("p_t_anno", float("inf")),
                       ("p_t_anno", True),
                       ("prezzo_el_eur_mwh", None)):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh767_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("p_t_anno", 0),
                          ("p_t_anno", -1),
                          ("cullet_pct", -1),
                          ("cullet_pct", 100.1),
                          ("prezzo_gas_eur_mwh", -1),
                          ("prezzo_el_eur_mwh", -1),
                          ("capex_eur", -1),
                          ("om_eur_anno", -100),
                          ("f_gas_t_per_mwh", -0.10),
                          ("f_el_t_per_mwh", -0.10),
                          ("wacc_pct", -0.1), ("wacc_pct", 50.1),
                          ("vita_anni", 0), ("vita_anni", 2.5)):
        d = _demo_kwargs()
        d[campo] = valore
        assert mh767_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"cullet_pct": 0,
              "prezzo_gas_eur_mwh": 0,
              "prezzo_el_eur_mwh": 0, "om_eur_anno": 0,
              "capex_eur": 0, "f_gas_t_per_mwh": 0,
              "f_el_t_per_mwh": 0, "wacc_pct": 0})
    assert mh767_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["cullet_pct"] = 100
    assert mh767_valida(**d)["valido"] is True


def test_valida_non_controlla_risparmio_calcola_neppure():
    """La validazione input NON controlla il risparmio
    (e' un esito, non un range) e in questa tab
    nemmeno mh767_calcola lo controlla: con prezzo
    elettrico 400 EUR/MWh il caso resta CALCOLABILE."""
    d = _demo_kwargs()
    d["prezzo_el_eur_mwh"] = 400
    assert mh767_valida(**d)["valido"] is True
    bc = _variante(prezzo_el_eur_mwh=400)
    assert bc["valid"] is True
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["flussi"]
    assert bc["tir"] is None
    assert bc["payback"] is None


def test_demo_dict():
    d = mh767_demo()
    assert d["p_t_anno"] == 30000
    assert d["cullet_pct"] == 40.0
    assert d["prezzo_gas_eur_mwh"] == 45
    assert d["prezzo_el_eur_mwh"] == 110
    assert d["capex_eur"] == 1000000
    assert d["om_eur_anno"] == 60000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["f_gas_t_per_mwh"] == 0.20
    assert d["f_el_t_per_mwh"] == 0.25


def test_demo_costanti_vs_demo_calcoli():
    """Ogni _DEMO del test contro demo_calcoli():
    scarto relativo < 1e-9 (zero atteso:
    confronto assoluto)."""
    bc = demo_calcoli()
    attesi = {
        "e_base_gj_per_t": 4.5,
        "gas_base_mwh_anno": 37500.0,
        "gas_alt_mwh_anno": 24375.0,
        "el_alt_mwh_anno": 2400.0,
        "c_base_eur_anno": 1687500.0,
        "c_alt_var_eur_anno": 1360875.0,
        "c_alt_eur_anno": 1420875.0,
        "co2_base_t_anno": 7500.0,
        "co2_alt_t_anno": 5475.0,
        "risparmio_eur_anno": 266625.0,
        "co2_evitata_t_anno": 2025.0,
        "lco_base_eur_t": 56.25,
        "lco_alt_eur_t": 47.3625,
        "van": 1767476.3244299,
        "tir": 25.81113746280782,
        "prezzo_pareggio_eur_mwh": 221.09375,
    }
    for chiave, atteso in attesi.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert abs(got - atteso) / abs(atteso) < 1e-9, chiave
    assert bc["payback"] == 4
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_demo_calcoli_fisica():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["e_base_gj_per_t"] == pytest.approx(4.5)
    assert bc["gas_base_mwh_anno"] == pytest.approx(37500.0)
    assert bc["gas_alt_mwh_anno"] == pytest.approx(24375.0)
    assert bc["el_alt_mwh_anno"] == pytest.approx(2400.0)
    assert bc["co2_evitata_t_anno"] == pytest.approx(2025.0)


def test_demo_calcoli_economia():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(1687500.0)
    assert bc["c_alt_var_eur_anno"] == pytest.approx(1360875.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(1420875.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(266625.0)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(221.09375)


def test_demo_calcoli_finanza():
    bc = demo_calcoli()
    assert bc["lco_base_eur_t"] == pytest.approx(56.25)
    assert bc["lco_alt_eur_t"] == pytest.approx(47.3625)
    assert bc["van"] == pytest.approx(1767476.3244299)
    assert bc["tir"] == pytest.approx(25.81113746280782)
    assert bc["payback"] == 4
    assert bc["verdetto"] == "CONVIENTE"


def test_demo_flussi_e_cumulato():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -1000000
    assert len(bc["flussi"]) == 16
    assert all(f == 266625.0 for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -1000000
    assert righe.iloc[1]["Cumulato (EUR)"] == pytest.approx(-733375.0)
    assert righe.iloc[4]["Cumulato (EUR)"] == pytest.approx(66500.0)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(2999375.0)
    assert righe.iloc[15]["Flusso (EUR/anno)"] == 266625.0


def test_demo_tabella_righe():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Produzione vetro (t/anno)"] == pytest.approx(30000.0)
    assert mappa["Consumo specifico baseline (GJ/t)"] == pytest.approx(4.5)
    assert mappa["Gas baseline (MWh/anno)"] == pytest.approx(37500.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(
        1420875.0)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(266625.0)
    assert mappa["Payback (anni)"] == 4
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Prezzo elettrico di pareggio (EUR/MWh)"] == pytest.approx(
        221.09375)


def test_demo_coerenza_interna():
    bc = demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["c_alt_var_eur_anno"] + bc["om_eur_anno"] == \
        pytest.approx(bc["c_alt_eur_anno"])
    assert bc["gas_base_mwh_anno"] * bc["prezzo_gas_eur_mwh"] == \
        pytest.approx(bc["c_base_eur_anno"])
    assert bc["co2_base_t_anno"] - bc["co2_alt_t_anno"] == \
        pytest.approx(bc["co2_evitata_t_anno"])
    assert bc["gas_alt_mwh_anno"] == pytest.approx(
        0.65 * bc["gas_base_mwh_anno"])
    assert bc["el_alt_mwh_anno"] == pytest.approx(
        0.08 * bc["p_t_anno"])
    assert bc["e_base_gj_per_t"] == pytest.approx(
        5.0 * (1.0 - 0.0025 * bc["cullet_pct"]))
    assert bc["gas_base_mwh_anno"] == pytest.approx(
        bc["p_t_anno"] * bc["e_base_gj_per_t"] / 3.6)
    assert bc["c_base_eur_anno"] - bc["gas_alt_mwh_anno"] * \
        bc["prezzo_gas_eur_mwh"] - bc["om_eur_anno"] == \
        pytest.approx(bc["prezzo_pareggio_eur_mwh"] *
                      bc["el_alt_mwh_anno"])
    assert bc["c_base_eur_anno"] / bc["p_t_anno"] == \
        pytest.approx(bc["lco_base_eur_t"])
    assert bc["c_alt_eur_anno"] / bc["p_t_anno"] == \
        pytest.approx(bc["lco_alt_eur_t"])


def test_demo_contro_riconteggio_indipendente():
    p, cu = 30000, 40.0
    pg, pel, om, cx = 45, 110, 60000, 1000000
    fg, fe, wacc, vita = 0.20, 0.25, 5.0, 15
    eb = 5.0 * (1.0 - 0.0025 * cu)
    gb = p * eb / 3.6
    ga = 0.65 * gb
    ea = 0.08 * p
    cb = gb * pg
    cav = ga * pg + ea * pel
    ca = cav + om
    risp = cb - ca
    co2b = gb * fg
    co2a = ga * fg + ea * fe
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    bc = demo_calcoli()
    assert bc["e_base_gj_per_t"] == pytest.approx(eb)
    assert bc["gas_base_mwh_anno"] == pytest.approx(gb)
    assert bc["gas_alt_mwh_anno"] == pytest.approx(ga)
    assert bc["el_alt_mwh_anno"] == pytest.approx(ea)
    assert bc["c_base_eur_anno"] == pytest.approx(cb)
    assert bc["c_alt_var_eur_anno"] == pytest.approx(cav)
    assert bc["c_alt_eur_anno"] == pytest.approx(ca)
    assert bc["risparmio_eur_anno"] == pytest.approx(risp)
    assert bc["co2_base_t_anno"] == pytest.approx(co2b)
    assert bc["co2_alt_t_anno"] == pytest.approx(co2a)
    assert bc["van"] == pytest.approx(van)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(
        (cb - ga * pg - om) / ea)


# ---------------------------------------------------------------- varianti
def test_demo_conviente():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] > 0.0
    assert bc["payback"] == 4
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_cullet_zero():
    """Sensibilita' richiesta dal brief: cullet 0 %."""
    bc = _variante(cullet_pct=0)
    assert bc["valid"] is True
    assert bc["e_base_gj_per_t"] == pytest.approx(5.0)
    assert bc["gas_base_mwh_anno"] == pytest.approx(41666.666666666664)
    assert bc["gas_alt_mwh_anno"] == pytest.approx(27083.333333333332)
    assert bc["c_base_eur_anno"] == pytest.approx(1875000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(1542750.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(332250.0)
    assert bc["van"] == pytest.approx(2448641.383185501)
    assert bc["tir"] == pytest.approx(32.75086202395443)
    assert bc["payback"] == 4
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(248.4375)
    assert bc["co2_evitata_t_anno"] == pytest.approx(2316.666666666667)
    assert bc["lco_alt_eur_t"] == pytest.approx(51.425)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_cullet_cento():
    """Sensibilita' richiesta dal brief: cullet 100 %."""
    bc = _variante(cullet_pct=100)
    assert bc["valid"] is True
    assert bc["e_base_gj_per_t"] == pytest.approx(3.75)
    assert bc["gas_base_mwh_anno"] == pytest.approx(31250.0)
    assert bc["gas_alt_mwh_anno"] == pytest.approx(20312.5)
    assert bc["c_base_eur_anno"] == pytest.approx(1406250.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(1238062.5)
    assert bc["risparmio_eur_anno"] == pytest.approx(168187.5)
    assert bc["van"] == pytest.approx(745728.736296498)
    assert bc["tir"] == pytest.approx(14.657141347192743)
    assert bc["payback"] == 6
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(180.078125)
    assert bc["co2_evitata_t_anno"] == pytest.approx(1587.5)
    assert bc["lco_alt_eur_t"] == pytest.approx(41.26875)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_prezzo_el_alto_calcolabile_non_conviente():
    """Sensibilita' richiesta dal brief: risparmio
    negativo resta CALCOLABILE."""
    bc = _variante(prezzo_el_eur_mwh=400)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(-429375.0)
    assert bc["van"] == pytest.approx(-5456765.67014379)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["lco_alt_eur_t"] == pytest.approx(70.5625)
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["flussi"]


def test_variante_fattore_el_alto_co2_evitata_negativa():
    bc = _variante(f_el_t_per_mwh=2.0)
    assert bc["co2_alt_t_anno"] == pytest.approx(9675.0)
    assert bc["co2_evitata_t_anno"] == pytest.approx(-2175.0)
    assert bc["van"] == pytest.approx(1767476.3244299)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(2999375.0)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    """Payback regola >=: con CAPEX nullo il payback e' 0,
    non 1 (all'anno 0 il cumulato e' gia' zero)."""
    bc = _variante(capex_eur=0)
    assert bc["capex_eur"] == 0
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(2767476.3244299)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_vita_dieci():
    bc = _variante(vita_anni=10)
    assert len(bc["flussi"]) == 11
    assert bc["van"] == pytest.approx(1058807.5754939)
    assert bc["tir"] == pytest.approx(23.408168413113394)
    assert bc["payback"] == 4
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_alto_non_conviente():
    bc = _variante(capex_eur=5000000)
    assert bc["risparmio_eur_anno"] == pytest.approx(266625.0)
    assert bc["van"] == pytest.approx(-2232523.675570099)
    assert bc["tir"] == pytest.approx(-2.669657927511768)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_variante_gas_economico_non_conviente():
    bc = _variante(prezzo_gas_eur_mwh=10)
    assert bc["c_base_eur_anno"] == pytest.approx(375000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(567750.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-192750.0)
    assert bc["van"] == pytest.approx(-3000679.0868593086)
    assert bc["prezzo_pareggio_eur_mwh"] == pytest.approx(29.6875)
    assert bc["lco_alt_eur_t"] == pytest.approx(18.925)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_fattori_zero_calcolabile():
    bc = _variante(f_gas_t_per_mwh=0, f_el_t_per_mwh=0)
    assert bc["valid"] is True
    assert bc["co2_base_t_anno"] == 0.0
    assert bc["co2_alt_t_anno"] == 0.0
    assert bc["co2_evitata_t_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(266625.0)


# ---------------------------------------------------------------- degenere
def test_degenere_produzione_zero_sollevela():
    """Caso degenere richiesto dal brief: P = 0
    solleva ValueError."""
    with pytest.raises(ValueError):
        _variante(p_t_anno=0)


def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"p_t_anno": 0}, {"p_t_anno": -1},
               {"cullet_pct": -1}, {"cullet_pct": 100.1},
               {"prezzo_gas_eur_mwh": -1},
               {"prezzo_el_eur_mwh": -1},
               {"capex_eur": -1},
               {"om_eur_anno": -100},
               {"f_gas_t_per_mwh": -0.10},
               {"f_el_t_per_mwh": -0.10},
               {"wacc_pct": -1}, {"wacc_pct": 60},
               {"vita_anni": 0}, {"vita_anni": 2.5}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh767_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"p_t_anno": "30000"},
               {"p_t_anno": float("nan")},
               {"prezzo_el_eur_mwh": float("inf")},
               {"capex_eur": True}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh767_valida(**d)["valido"] is False


def test_risparmio_negativo_non_degenere():
    """Differenza chiave: risparmio negativo resta
    calcolabile, con flussi pieni e VAN negativa."""
    for kw in ({"prezzo_el_eur_mwh": 400},
               {"prezzo_gas_eur_mwh": 10},
               {"capex_eur": 5000000}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] < 0.0 or bc["van"] < 0.0
        assert bc["verdetto"] == "NON_CONVIENTE"
        assert bc["flussi"]


def test_co2_evitata_negativa_non_degenere():
    bc = _variante(f_el_t_per_mwh=2.0)
    assert bc["valid"] is True
    assert bc["co2_evitata_t_anno"] < 0.0
    assert bc["verdetto"] == "CONVIENTE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = demo_calcoli()
    testo = mh767_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert "e_base_gj_per_t;4.5" in testo
    assert "gas_base_mwh_anno;37500.0" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "prezzo_pareggio_eur_mwh" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = demo_calcoli()
    testo = mh767_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"gas_base_mwh_anno;{bc['gas_base_mwh_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = demo_calcoli()
    testo = mh767_csv(bc, _demo_kwargs())
    for chiave in _demo_kwargs():
        assert f"{chiave};" in testo


def test_monotonia_prezzo_el():
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(prezzo_el_eur_mwh=120)["risparmio_eur_anno"]
    basso = _variante(prezzo_el_eur_mwh=100)["risparmio_eur_anno"]
    assert basso > base > alto
    assert basso - base == pytest.approx(24000.0)
    assert base - alto == pytest.approx(24000.0)


def test_monotonia_cullet():
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(cullet_pct=50)["risparmio_eur_anno"]
    basso = _variante(cullet_pct=30)["risparmio_eur_anno"]
    assert basso > base > alto


def test_demo_deterministica_due_chiamate():
    a = demo_calcoli()
    b = demo_calcoli()
    assert a["van"] == b["van"]
    assert a["flussi"] == b["flussi"]
    assert a["tir"] == b["tir"]


def test_demo_chiavi_attese():
    assert set(mh767_demo().keys()) == {
        "p_t_anno",
        "cullet_pct",
        "prezzo_gas_eur_mwh", "prezzo_el_eur_mwh",
        "capex_eur", "om_eur_anno",
        "wacc_pct", "vita_anni",
        "f_gas_t_per_mwh", "f_el_t_per_mwh"}


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
    return ["mh" + "76" + "6", "st" + "76" + "6",
            "tab" + "76" + "6", "w" + "76" + "7_",
            "mh" + "76" + "5", "st" + "76" + "5",
            "tab" + "76" + "5", "w" + "76" + "6_"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w768_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w768_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab767:")


def test_registry_chain_tail_and_count():
    """Registry della nuova tab: il frammento UI apre la tab
    numero 767 (la coda della catena termina con la nuova tab
    e il conteggio atteso delle tab e' 767)."""
    src = _leggi("w768_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 767
    assert src.count("with tab767:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w768_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w768_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st767_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert "key=f" not in src and 'key = f' not in src
    assert "st.stop()" in src
    # guard degenere prima di KPI / grafico / tabella / CSV
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w768_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def767[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w768_ui.py")
        usate = set(re.findall(r'_def767\["([^"]+)"\]', src))
        assert usate
        assert usate <= set(mh767_demo().keys())


def test_ui_chiavi_demo_coerenti():
    """Ogni _def767[...] letto dalla UI esiste nel dict demo:
    sweep anti-KeyError a render (lezione dello sweep chiavi demo vs UI)."""
    src = _leggi("w768_ui.py")
    usate = set(re.findall(r'_def767\["([^"]+)"\]', src))
    assert usate
    assert usate <= set(mh767_demo().keys())


def test_ui_riferisce_solo_helper_nuovi():
    src = _leggi("w768_ui.py")
    usati = set(re.findall(r'\b(mh\d+_\w+)\b', src))
    assert usati
    assert all(u.startswith("mh767_") for u in usati)


@pytest.mark.parametrize("cullet,atteso", [
    (0, 5.0),
    (40.0, 4.5),
    (50.0, 4.375),
    (100, 3.75),
])
def test_e_base_parametrizzato(cullet, atteso):
    assert mh767_e_base(cullet) == pytest.approx(atteso)


@pytest.mark.parametrize("campo,valore", [
    ("p_t_anno", 0), ("p_t_anno", -3),
    ("cullet_pct", -1), ("cullet_pct", 100.1),
    ("prezzo_gas_eur_mwh", -1),
    ("prezzo_el_eur_mwh", -1),
    ("capex_eur", -1),
    ("om_eur_anno", -100),
    ("f_gas_t_per_mwh", -0.10), ("f_el_t_per_mwh", -0.10),
    ("wacc_pct", -0.1), ("wacc_pct", 50.1),
    ("vita_anni", -1), ("vita_anni", 2.5),
])
def test_valida_rifiuta_singoli_campi(campo, valore):
    d = _demo_kwargs()
    d[campo] = valore
    assert mh767_valida(**d)["valido"] is False


@pytest.mark.parametrize("campo,valore", [
    ("p_t_anno", 0), ("p_t_anno", -3),
    ("cullet_pct", -1), ("cullet_pct", 100.1),
    ("prezzo_gas_eur_mwh", -1),
    ("prezzo_el_eur_mwh", -1),
    ("capex_eur", -1),
    ("om_eur_anno", -100),
    ("f_gas_t_per_mwh", -0.10), ("f_el_t_per_mwh", -0.10),
    ("wacc_pct", -0.1), ("wacc_pct", 50.1),
    ("vita_anni", -1), ("vita_anni", 2.5),
])
def test_calcola_sollevela_singoli_campi(campo, valore):
    d = _demo_kwargs()
    d[campo] = valore
    with pytest.raises(ValueError):
        mh767_calcola(**d)


def test_df_tabella_valori_demo_selezionati():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Produzione vetro (t/anno)"] == 30000.0
    assert mappa["Gas baseline (MWh/anno)"] == pytest.approx(37500.0)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(266625.0)
    assert mappa["Verdetto"] == "CONVIENTE"


def test_lco_alt_minore_di_lco_base_demo():
    bc = demo_calcoli()
    assert bc["lco_alt_eur_t"] < bc["lco_base_eur_t"]
    assert bc["lco_base_eur_t"] - bc["lco_alt_eur_t"] == pytest.approx(
        8.8875)
