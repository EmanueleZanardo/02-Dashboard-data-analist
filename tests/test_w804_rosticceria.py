"""Test nuova scheda "Rosticceria: girarrosto a gas
efficiente + recupero calore girarrosto su ACS +
celle e banchi caldi efficienti batte girarrosto
vecchio + celle tradizionali + caldaia a gas?"
(titolo completo nel frammento UI).
Contenuto pronto da scrivere in repo come test
della scheda rosticceria.

Business case deterministico di una rosticceria
guidato dai KG DI POLLI ARROSTO AL GIORNO e
dai GIORNI DI APERTURA ALL'ANNO: i polli
guidano il calore di cottura del girarrosto
(kWh_th per kg di polli), i banchi caldi di
mantenimento (kWh_e per kg di polli, elettrici)
e il carico frigorifero delle celle (kWh_c per
kg di polli); i litri di ACS al giorno guidano
il lavaggio di spiedi, teglie e attrezzature.
Polli annui = kg al giorno x giorni; calore di
cottura = polli annui x kWh_th per kg; gas
girarrosto base e alt = Q_cottura / eta
(stesso calore utile, rendimento diverso);
elettricita' banchi base e alt = polli annui x
kWh_e per kg x fattore (base 1,00, alt 0,80);
carico celle = polli annui x kWh_c per kg;
elettricita' freddo base e alt = Q_celle / COP
(stesso carico, COP diverso); ACS = litri x
giorni x 4,186 x delta_T / 3600; recupero =
min(ACS, Q_cottura x f_rec) (saturato
all'ACS); ACS netta = max(0, ACS - recupero);
gas ACS baseline = ACS / eta_caldaia (senza
recupero); elettricita' PdC ACS = ACS netta /
COP_pdc_acs; C_base = (gas_girarrosto_base +
gas_acs_base) / 1000 x p_gas + (E_banchi_base
+ E_freddo_base) / 1000 x p_el + O&M_base;
C_alt = gas_girarrosto_alt / 1000 x p_gas +
(E_banchi_alt + E_freddo_alt + E_pdc_acs)
/ 1000 x p_el + O&M_alt; risparmio = C_base -
C_alt; CO2_base = (gas_girarrosto_base +
gas_acs_base) / 1000 x f_gas + (E_banchi_base
+ E_freddo_base) / 1000 x f_el; CO2_alt =
gas_girarrosto_alt / 1000 x f_gas +
(E_banchi_alt + E_freddo_alt + E_pdc_acs)
/ 1000 x f_el; CO2_evitata = CO2_base -
CO2_alt; flussi [-CAPEX, risparmio x vita];
VAN, TIR, payback (primo anno con cumulato
>= 0); breakeven gas = ((E_banchi_alt +
E_freddo_alt + E_pdc_acs) / 1000 x p_el +
O&M_alt - (E_banchi_base + E_freddo_base)
/ 1000 x p_el - O&M_base) /
((gas_girarrosto_base + gas_acs_base -
gas_girarrosto_alt) / 1000) EUR/MWh, None se
denominatore gas <= 0 o numeratore < 0,
SOGLIA MINIMA quando esiste.
Verdetto: NON_CALCOLABILE se input degenere
(kg <= 0, giorni <= 0, eta <= 0 o > 1, COP
<= 1, delta_T <= 0, f_rec fuori [0, 1],
prezzi <= 0, CAPEX <= 0, vita <= 0) o se
risparmio <= 0 (guard degenere: UI salta KPI,
grafico, tabella e CSV); altrimenti CONVIENTE
se VAN > 0, MARGINALE se VAN negativa entro
tolleranza % del CAPEX, NON_CONVIENTE se VAN
negativa oltre la tolleranza. Distinzione
esplicita: distinto dal panificio (kg di pane
per la cottura del pane, senza girarrosto e
senza polli: qui il calore e' quello del
girarrosto per i polli, con banchi caldi di
mantenimento e celle dei polli, e il recupero
va sull'ACS di lavaggio di spiedi e teglie),
dalla pasticceria (kg di dolci, abbattitore da
T_in a T_out, celle dei dolci: qui nessun
dolce, nessun abbattitore, i banchi sono caldi
di mantenimento), dalla gelateria (litri di
gelato, pastorizzazione, freddo del gelato:
qui nessuna pastorizzazione, nessun gelato, il
freddo e' quello delle celle dei polli), dalla
pescheria (kg di pesce, macchina del ghiaccio
in scaglie, recupero dai condensatori: qui
nessun pesce, nessun ghiaccio, il recupero
viene dal calore del girarrosto), dal fioraio
(superficie negozio per riscaldamento piu'
cella fiori, recupero sul riscaldamento: qui
niente riscaldamento, recupero sull'ACS di
lavaggio), dal parrucchiere (lavaggi di
capelli, ACS, recupero dalle acque reflue),
dal ristorante (coperti, ACS di cucina, celle
frigo di cucina), dalla farmacia (superficie
di vendita piu' frigoriferi farmaceutici,
recupero dai frigoriferi, nessun girarrosto),
dall'albergo (pernottamento, ACS docce
ospiti), dalla palestra (docce utenti, recupero
dalle acque delle docce), dall'autolavaggio
(veicoli lavati, acque di lavaggio dei
veicoli) e dal palaghiaccio (pista da
pattinaggio, freddo di pista verso
spogliatoi): qui driver POLLI + GIORNI + ACS
= kg di polli al giorno per cottura, banchi e
celle, giorni di apertura per l'anno, litri di
ACS per il lavaggio; niente pane, niente
dolci, niente gelato, niente pesce, niente
lavaggi, niente coperti, niente docce, niente
veicoli, niente frigoriferi farmaceutici,
niente pista.

Demo (rosticceria): 120 kg di polli arrosto al
giorno per 310 giorni di apertura all'anno
(37.200 kg all'anno), calore di cottura 1,20
kWh_th per kg di polli (44.640 kWh_th/anno),
girarrosto base 0,70 e alt 0,88, banchi caldi
0,25 kWh_e per kg di polli con fattore base
1,00 e alt 0,80, carico celle 0,30 kWh_c per kg
di polli, COP freddo base 2,2 e alt 3,2, ACS
di lavaggio 200 litri al giorno con delta_T 40
K, f_rec 0,08, caldaia 0,85, COP PdC ACS 3,2,
gas 90, el 250 EUR/MWh, O&M base 1.200, alt
2.000, CAPEX 18.000, WACC 5 %, vita 15, f_gas
0,20, f_el 0,35, tolleranza 10 % del CAPEX.
Valori calcolati eseguendo mh804_demo_calcoli():
polli annui 37.200, Q_cottura 44.640,
gas_girarrosto_base 63.771,42857142857,
gas_girarrosto_alt 50.727,27272727273,
E_banchi_base 9.300, E_banchi_alt 7.440,
Q_celle 11.160, E_freddo_base
5.072,727272727272, E_freddo_alt 3.487,5,
Q_acs 2.883,688888888889, Q_rec
2.883,688888888889 (saturato all'ACS: il
recupero grezzo 44.640 x 0,08 = 3.571,20
supera l'ACS), Q_acs_net 0,0, gas_acs_base
3.392,575163398693, E_pdc_acs 0,0, C_base
10.837,942154316272, C_alt 9.297,329545454544,
risparmio 1.540,6126088617275, CO2_base
18,463255292419998, CO2_alt
13,970079545454546, CO2_evitata
4,493175746965452, VAN -2.008,9679507060014,
TIR 3,2991625535369717 %, payback 12,
breakeven gas None (numeratore negativo: a
prezzo gas zero l'alternativa e' gia' piu'
conveniente di 61,31 EUR/anno), verdetto
NON_CONVIENTE (VAN negativa oltre la
tolleranza del 10 % = 1.800 EUR).
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w805_helpers import (
    demo_calcoli,
    mh804_breakeven_gas,
    mh804_c_alt,
    mh804_c_base,
    mh804_calcola,
    mh804_co2_alt,
    mh804_co2_base,
    mh804_co2_evitata,
    mh804_cop,
    mh804_csv,
    mh804_demo,
    mh804_demo_calcoli,
    mh804_e_banchi,
    mh804_e_freddo,
    mh804_e_pdc_acs,
    mh804_eta,
    mh804_flussi,
    mh804_frazione,
    mh804_gas_acs,
    mh804_gas_girarrosto,
    mh804_int_pos,
    mh804_kg_polli_anno,
    mh804_num,
    mh804_nneg,
    mh804_payback,
    mh804_pct_tolleranza,
    mh804_pct_wacc,
    mh804_pos,
    mh804_q_acs,
    mh804_q_acs_net,
    mh804_q_celle,
    mh804_q_cottura,
    mh804_q_rec,
    mh804_risparmio,
    mh804_tir,
    mh804_valida,
    mh804_van,
    mh804_verdetto,
)

_DEMO = {
    "kg_polli_anno": 37200.0,
    "q_cottura_kwh_anno": 44640.0,
    "gas_girarrosto_base_kwh_anno": 63771.42857142857,
    "gas_girarrosto_alt_kwh_anno": 50727.27272727273,
    "e_banchi_base_kwh_anno": 9300.0,
    "e_banchi_alt_kwh_anno": 7440.0,
    "q_celle_kwh_anno": 11160.0,
    "e_freddo_base_kwh_anno": 5072.727272727272,
    "e_freddo_alt_kwh_anno": 3487.5,
    "q_acs_kwh_anno": 2883.688888888889,
    "q_rec_kwh_anno": 2883.688888888889,
    "q_acs_net_kwh_anno": 0.0,
    "gas_acs_base_kwh_anno": 3392.575163398693,
    "e_pdc_acs_kwh_anno": 0.0,
    "c_base_eur_anno": 10837.942154316272,
    "c_alt_eur_anno": 9297.329545454544,
    "risparmio_eur_anno": 1540.6126088617275,
    "co2_base_t_anno": 18.463255292419998,
    "co2_alt_t_anno": 13.970079545454546,
    "co2_evitata_t_anno": 4.493175746965452,
    "van": -2008.9679507060014,
    "tir": 3.2991625535369717,
}


def _demo_kwargs():
    return dict(mh804_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh804_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh804_num(3, "x") == 3.0
    assert mh804_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh804_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh804_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh804_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh804_pos(0, "x")
    with pytest.raises(ValueError):
        mh804_pos(-1, "x")
    assert mh804_pos(0.5, "x") == 0.5


def test_cop_maggiore_di_uno():
    assert mh804_cop(3.2, "x") == 3.2
    assert mh804_cop(1.01, "x") == 1.01
    with pytest.raises(ValueError):
        mh804_cop(1.0, "x")
    with pytest.raises(ValueError):
        mh804_cop(0.5, "x")
    with pytest.raises(ValueError):
        mh804_cop(0, "x")


def test_frazione_limiti():
    assert mh804_frazione(0, "x") == 0.0
    assert mh804_frazione(1, "x") == 1.0
    assert mh804_frazione(0.08, "x") == 0.08
    with pytest.raises(ValueError):
        mh804_frazione(-0.01, "x")
    with pytest.raises(ValueError):
        mh804_frazione(1.01, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh804_int_pos(5.0, "x") == 5
    assert mh804_int_pos(310.0, "x") == 310
    with pytest.raises(ValueError):
        mh804_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh804_int_pos(0, "x")


def test_eta_limiti():
    assert mh804_eta(1.0, "x") == 1.0
    assert mh804_eta(0.88, "x") == 0.88
    with pytest.raises(ValueError):
        mh804_eta(0, "x")
    with pytest.raises(ValueError):
        mh804_eta(1.01, "x")


def test_pct_wacc_limiti():
    assert mh804_pct_wacc(0, "x") == 0.0
    assert mh804_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh804_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh804_pct_tolleranza(0, "x") == 0.0
    assert mh804_pct_tolleranza(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh804_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh804_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_kg_polli_anno_e_q_cottura():
    assert mh804_kg_polli_anno(120, 310) == 37200.0
    assert mh804_kg_polli_anno(0, 310) == 0.0
    assert mh804_kg_polli_anno(60, 310) == 18600.0
    assert mh804_q_cottura(37200, 1.20) == 44640.0
    assert mh804_q_cottura(37200, 0) == 0.0
    assert mh804_q_cottura(18600, 1.20) == 22320.0
    with pytest.raises(ValueError):
        mh804_kg_polli_anno(-1, 310)
    with pytest.raises(ValueError):
        mh804_kg_polli_anno(120, 0)
    with pytest.raises(ValueError):
        mh804_kg_polli_anno(120, 2.5)
    with pytest.raises(ValueError):
        mh804_q_cottura(37200, -0.1)


def test_gas_girarrosto_rendimenti():
    assert mh804_gas_girarrosto(44640.0, 0.70) == pytest.approx(63771.42857142857)
    assert mh804_gas_girarrosto(44640.0, 0.88) == pytest.approx(50727.27272727273)
    assert mh804_gas_girarrosto(44640.0, 1.0) == 44640.0
    assert mh804_gas_girarrosto(0, 0.70) == 0.0
    with pytest.raises(ValueError):
        mh804_gas_girarrosto(44640.0, 0)
    with pytest.raises(ValueError):
        mh804_gas_girarrosto(44640.0, 1.01)


def test_e_banchi_fattori():
    assert mh804_e_banchi(37200, 0.25, 1.0) == 9300.0
    assert mh804_e_banchi(37200, 0.25, 0.80) == 7440.0
    assert mh804_e_banchi(0, 0.25, 1.0) == 0.0
    assert mh804_e_banchi(37200, 0, 0.80) == 0.0
    with pytest.raises(ValueError):
        mh804_e_banchi(37200, 0.25, 0)
    with pytest.raises(ValueError):
        mh804_e_banchi(37200, 0.25, 1.01)
    with pytest.raises(ValueError):
        mh804_e_banchi(37200, -0.1, 0.80)
    with pytest.raises(ValueError):
        mh804_e_banchi(-1, 0.25, 0.80)


def test_q_celle_e_freddo():
    assert mh804_q_celle(37200, 0.30) == 11160.0
    assert mh804_q_celle(0, 0.30) == 0.0
    assert mh804_q_celle(37200, 0) == 0.0
    assert mh804_e_freddo(11160.0, 2.2) == pytest.approx(5072.727272727272)
    assert mh804_e_freddo(11160.0, 3.2) == pytest.approx(3487.5)
    assert mh804_e_freddo(0, 2.2) == 0.0
    with pytest.raises(ValueError):
        mh804_q_celle(37200, -0.1)
    with pytest.raises(ValueError):
        mh804_e_freddo(11160.0, 1.0)
    with pytest.raises(ValueError):
        mh804_e_freddo(-1, 2.2)


def test_q_acs_formula():
    assert mh804_q_acs(200, 310, 40) == pytest.approx(2883.688888888889)
    assert mh804_q_acs(0, 310, 40) == 0.0
    assert mh804_q_acs(400, 310, 40) == pytest.approx(5767.377777777778)
    assert mh804_q_acs(200, 310, 20) == pytest.approx(1441.8444444444444)
    with pytest.raises(ValueError):
        mh804_q_acs(-1, 310, 40)
    with pytest.raises(ValueError):
        mh804_q_acs(200, 0, 40)
    with pytest.raises(ValueError):
        mh804_q_acs(200, 310, 0)
    with pytest.raises(ValueError):
        mh804_q_acs(200, 2.5, 40)


def test_q_rec_saturazione_e_acs_netta():
    assert mh804_q_rec(44640.0, 0.08, 2883.688888888889) == pytest.approx(2883.688888888889)
    assert mh804_q_rec(44640.0, 0, 2883.688888888889) == 0.0
    assert mh804_q_rec(44640.0, 0.05, 2883.688888888889) == pytest.approx(2232.0)
    assert mh804_q_rec(44640.0, 1.0, 2883.688888888889) == 2883.688888888889
    with pytest.raises(ValueError):
        mh804_q_rec(44640.0, 1.01, 2883.688888888889)
    with pytest.raises(ValueError):
        mh804_q_rec(44640.0, -0.1, 2883.688888888889)
    assert mh804_q_acs_net(2883.688888888889, 2883.688888888889) == 0.0
    assert mh804_q_acs_net(2883.688888888889, 0.0) == pytest.approx(2883.688888888889)
    assert mh804_q_acs_net(2883.688888888889, 2232.0) == pytest.approx(651.688888888889)
    with pytest.raises(ValueError):
        mh804_q_acs_net(-1, 2232.0)
    with pytest.raises(ValueError):
        mh804_q_acs_net(2883.688888888889, -1)


def test_gas_acs_e_pdc_acs():
    assert mh804_gas_acs(2883.688888888889, 0.85) == pytest.approx(3392.575163398693)
    assert mh804_gas_acs(0, 0.85) == 0.0
    assert mh804_gas_acs(2883.688888888889, 1.0) == pytest.approx(2883.688888888889)
    assert mh804_e_pdc_acs(0.0, 3.2) == 0.0
    assert mh804_e_pdc_acs(651.688888888889, 3.2) == pytest.approx(203.65277777777777)
    with pytest.raises(ValueError):
        mh804_gas_acs(2883.688888888889, 0)
    with pytest.raises(ValueError):
        mh804_gas_acs(2883.688888888889, 1.01)
    with pytest.raises(ValueError):
        mh804_e_pdc_acs(651.688888888889, 1.0)


def test_c_base_c_alt_scomposizione():
    assert mh804_c_base(63771.42857142857, 3392.575163398693, 90,
                        9300.0, 5072.727272727272, 250,
                        1200) == pytest.approx(10837.942154316272)
    assert mh804_c_base(63771.42857142857, 3392.575163398693, 0,
                        9300.0, 5072.727272727272, 250,
                        1200) == pytest.approx(4793.181818181818)
    assert mh804_c_alt(50727.27272727273, 90, 7440.0,
                       3487.5, 0.0, 250,
                       2000) == pytest.approx(9297.329545454544)
    assert mh804_c_alt(50727.27272727273, 90, 7440.0,
                       3487.5, 203.65277777777777, 250,
                       2000) == pytest.approx(9348.242739898989)
    with pytest.raises(ValueError):
        mh804_c_base(63771.43, 3392.58, 90, 9300.0, 5072.73, 250, -1)
    with pytest.raises(ValueError):
        mh804_c_alt(50727.27, 90, 7440.0, 3487.5, 0.0, 250, -1)


def test_risparmio_segno():
    assert mh804_risparmio(10837.942154316272, 9297.329545454544) == pytest.approx(1540.6126088617275)
    assert mh804_risparmio(9297.33, 9297.33) == 0.0


def test_co2_base_alt_evitata():
    assert mh804_co2_base(63771.42857142857, 3392.575163398693, 0.20,
                          9300.0, 5072.727272727272,
                          0.35) == pytest.approx(18.463255292419998)
    assert mh804_co2_alt(50727.27272727273, 0.20, 7440.0,
                         3487.5, 0.0,
                         0.35) == pytest.approx(13.970079545454546)
    assert mh804_co2_evitata(63771.42857142857, 3392.575163398693, 0.20,
                             9300.0, 5072.727272727272,
                             50727.27272727273, 7440.0,
                             3487.5, 0.0,
                             0.35) == pytest.approx(4.493175746965452)
    assert mh804_co2_base(0, 0, 0.20, 0, 0, 0.35) == pytest.approx(0.0)
    assert mh804_co2_alt(0, 0.20, 0, 0, 0, 0.35) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh804_co2_base(63771.43, 3392.58, -0.10, 9300.0, 5072.73, 0.35)
    with pytest.raises(ValueError):
        mh804_co2_alt(50727.27, 0.20, 7440.0, 3487.5, 0.0, -0.10)


def test_breakeven_demo_none_e_varianti():
    # Demo: numeratore negativo -> None (a prezzo gas zero
    # l'alternativa e' gia' piu' conveniente di 61,31 EUR/anno).
    assert mh804_demo_calcoli()["breakeven_gas_eur_mwh"] is None
    assert mh804_breakeven_gas(7440.0, 3487.5, 0.0,
                               250, 2000,
                               9300.0, 5072.727272727272, 1200,
                               63771.42857142857, 3392.575163398693,
                               50727.27272727273) is None
    # Variante senza recupero: numeratore positivo -> be 9,98.
    bc = _variante(f_rec=0)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(9.976520038398048)
    # Denominatore gas nullo (stesso rendimento, niente ACS) -> None.
    assert mh804_breakeven_gas(7440.0, 3487.5, 0.0,
                               250, 2000,
                               9300.0, 5072.727272727272, 1200,
                               63771.42857142857, 0,
                               63771.42857142857) is None
    with pytest.raises(ValueError):
        mh804_breakeven_gas(7440.0, 3487.5, 0.0, 250, 2000,
                            9300.0, 5072.73, 1200,
                            63771.43, 3392.58, -1)


def test_breakeven_verifica_pareggio():
    be = _variante(f_rec=0)["breakeven_gas_eur_mwh"]
    assert be == pytest.approx(9.976520038398048)
    bc = _variante(f_rec=0, p_gas=be)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    demo = mh804_demo_calcoli()
    assert demo["breakeven_gas_eur_mwh"] is None
    assert (demo["gas_girarrosto_base_kwh_anno"]
            + demo["gas_acs_base_kwh_anno"]
            - demo["gas_girarrosto_alt_kwh_anno"]) > 0.0


def test_breakeven_soglia_minima():
    bc_alto = _variante(f_rec=0, p_gas=10.976520038398048)
    bc_basso = _variante(f_rec=0, p_gas=9.0)
    assert bc_alto["c_alt_eur_anno"] < bc_alto["c_base_eur_anno"]
    assert bc_basso["c_alt_eur_anno"] > bc_basso["c_base_eur_anno"]
    assert bc_alto["verdetto"] == "NON_CONVIENTE"
    assert bc_basso["verdetto"] == "NON_CALCOLABILE"


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh804_flussi(18000, 1540.6126088617275, 15)
    assert len(fl) == 16
    assert fl[0] == -18000
    assert all(f == 1540.6126088617275 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh804_demo_calcoli()
    assert bc["van"] == pytest.approx(-2008.9679507060014)
    assert mh804_van([-18000] + [1540.6126088617275] * 15,
                     0) == pytest.approx(5109.189132926913)
    assert mh804_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh804_demo_calcoli()
    assert bc["tir"] == pytest.approx(3.2991625535369717)
    assert mh804_tir([-18000] + [1540.6126088617275] * 15) == \
        pytest.approx(0.032991625535369717)
    tir = mh804_tir([-18000] + [1540.6126088617275] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-18000] + [1540.6126088617275] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh804_payback([-18000] + [1540.6126088617275] * 15) == 12
    assert mh804_payback([-18000] + [-1000.0] * 15) is None
    assert mh804_payback([0] + [1540.6126088617275] * 15) == 0
    assert mh804_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh804_verdetto(1540.6126088617275, -2008.9679507060014, 18000,
                          10.0) == "NON_CONVIENTE"
    assert mh804_verdetto(1540.6126088617275, 0.0, 18000, 10.0) == "MARGINALE"
    assert mh804_verdetto(1540.6126088617275, -1800.0, 18000, 10.0) == "MARGINALE"
    assert mh804_verdetto(1540.6126088617275, -1800.01, 18000, 10.0) == "NON_CONVIENTE"
    assert mh804_verdetto(1540.6126088617275, 1991.03, 18000, 10.0) == "CONVIENTE"
    assert mh804_verdetto(0.0, 1991.03, 18000,
                          10.0) == "NON_CALCOLABILE"
    assert mh804_verdetto(-719.96, -25472.90, 18000,
                          10.0) == "NON_CALCOLABILE"
    assert mh804_verdetto(None, 1991.03, 18000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh804_verdetto(float("nan"), 1991.03, 18000, 10.0)
    with pytest.raises(ValueError):
        mh804_verdetto(1540.6126088617275, 1991.03, -1, 10.0)
    with pytest.raises(ValueError):
        mh804_verdetto(1540.6126088617275, 1991.03, 18000, 100.1)


def test_valida_demo_ok():
    v = mh804_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("kg_polli_giorno", "120"),
                       ("kg_polli_giorno", float("nan")),
                       ("kg_polli_giorno", float("inf")),
                       ("kg_polli_giorno", True),
                       ("p_gas", None),
                       ("q_celle_per_kg", "0.30")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh804_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("kg_polli_giorno", -10),
                          ("giorni_anno", 0),
                          ("giorni_anno", 2.5),
                          ("q_cottura_per_kg", -0.1),
                          ("eta_girarrosto_base", 0),
                          ("eta_girarrosto_base", 1.01),
                          ("eta_girarrosto_alt", 0),
                          ("eta_girarrosto_alt", 1.01),
                          ("q_banchi_per_kg", -0.1),
                          ("fattore_banchi_alt", 0),
                          ("fattore_banchi_alt", 1.01),
                          ("q_celle_per_kg", -0.1),
                          ("cop_freddo_base", 1.0),
                          ("cop_freddo_base", 0.5),
                          ("cop_freddo_alt", 1.0),
                          ("cop_freddo_alt", 0.5),
                          ("litri_acs_giorno", -1),
                          ("delta_t_acs", 0),
                          ("delta_t_acs", -5),
                          ("f_rec", -0.1),
                          ("f_rec", 1.01),
                          ("eta_caldaia_base", 0),
                          ("eta_caldaia_base", 1.01),
                          ("cop_pdc_acs", 1.0),
                          ("cop_pdc_acs", 0.5),
                          ("p_gas", -1),
                          ("p_el", -1),
                          ("om_base", -100),
                          ("om_alt", -100),
                          ("capex", -1),
                          ("wacc_pct", -0.1), ("wacc_pct", 50.1),
                          ("vita_anni", 0), ("vita_anni", 2.5),
                          ("f_gas", -0.10),
                          ("f_el", -0.10),
                          ("tolleranza_pct", -1),
                          ("tolleranza_pct", 100.1)):
        d = _demo_kwargs()
        d[campo] = valore
        assert mh804_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"kg_polli_giorno": 0,
              "q_cottura_per_kg": 0,
              "q_banchi_per_kg": 0,
              "q_celle_per_kg": 0,
              "litri_acs_giorno": 0,
              "f_rec": 0,
              "p_gas": 0,
              "p_el": 0,
              "om_base": 0, "om_alt": 0,
              "capex": 0, "wacc_pct": 0,
              "f_gas": 0, "f_el": 0,
              "tolleranza_pct": 0})
    assert mh804_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["f_rec"] = 1.0
    d["kg_polli_giorno"] = 120
    assert mh804_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh804_demo()
    assert d["kg_polli_giorno"] == 120
    assert d["giorni_anno"] == 310
    assert d["q_cottura_per_kg"] == 1.20
    assert d["eta_girarrosto_base"] == 0.70
    assert d["eta_girarrosto_alt"] == 0.88
    assert d["q_banchi_per_kg"] == 0.25
    assert d["fattore_banchi_alt"] == 0.80
    assert d["q_celle_per_kg"] == 0.30
    assert d["cop_freddo_base"] == 2.2
    assert d["cop_freddo_alt"] == 3.2
    assert d["litri_acs_giorno"] == 200
    assert d["delta_t_acs"] == 40
    assert d["f_rec"] == 0.08
    assert d["eta_caldaia_base"] == 0.85
    assert d["cop_pdc_acs"] == 3.2
    assert d["p_gas"] == 90
    assert d["p_el"] == 250
    assert d["om_base"] == 1200
    assert d["om_alt"] == 2000
    assert d["capex"] == 18000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["f_gas"] == 0.20
    assert d["f_el"] == 0.35
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    bc = mh804_demo_calcoli()
    for chiave, atteso in _DEMO.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert got == pytest.approx(atteso, rel=1e-9), chiave
    assert bc["payback"] == 12
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True
    assert demo_calcoli()["van"] == bc["van"]


def test_demo_calcoli_fisica_economia():
    bc = mh804_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(10837.942154316272)
    assert bc["c_alt_eur_anno"] == pytest.approx(9297.329545454544)
    assert bc["risparmio_eur_anno"] == pytest.approx(1540.6126088617275)
    assert bc["co2_base_t_anno"] == pytest.approx(18.463255292419998)
    assert bc["co2_alt_t_anno"] == pytest.approx(13.970079545454546)
    assert bc["co2_evitata_t_anno"] == pytest.approx(4.493175746965452)
    assert bc["kg_polli_anno"] == pytest.approx(37200.0)
    assert bc["q_cottura_kwh_anno"] == pytest.approx(44640.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(2883.688888888889)
    assert bc["q_acs_net_kwh_anno"] == pytest.approx(0.0, abs=1e-12)


def test_demo_flussi_e_cumulato():
    bc = mh804_demo_calcoli()
    assert bc["flussi"][0] == -18000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(1540.6126088617275) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -18000
    assert righe.iloc[11]["Cumulato (EUR)"] == pytest.approx(-1053.2613025209976)
    assert righe.iloc[12]["Cumulato (EUR)"] == pytest.approx(487.35130634072993)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(5109.189132926913)


def test_demo_tabella_righe():
    bc = mh804_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Kg di polli all'anno"] == pytest.approx(37200.0)
    assert mappa["Calore di cottura (kWh_th/anno)"] == pytest.approx(44640.0)
    assert mappa["Gas girarrosto base (kWh/anno)"] == pytest.approx(63771.42857142857)
    assert mappa["Gas girarrosto alt (kWh/anno)"] == pytest.approx(50727.27272727273)
    assert mappa["Elettricita' banchi caldi base (kWh_e/anno)"] == pytest.approx(9300.0)
    assert mappa["Elettricita' banchi caldi alt (kWh_e/anno)"] == pytest.approx(7440.0)
    assert mappa["Carico celle (kWh_c/anno)"] == pytest.approx(11160.0)
    assert mappa["Elettricita' freddo base (kWh_e/anno)"] == pytest.approx(5072.727272727272)
    assert mappa["Elettricita' freddo alt (kWh_e/anno)"] == pytest.approx(3487.5)
    assert mappa["ACS di lavaggio (kWh_th/anno)"] == pytest.approx(2883.688888888889)
    assert mappa["Calore girarrosto recuperato (kWh_th/anno)"] == pytest.approx(2883.688888888889)
    assert mappa["ACS netta (kWh_th/anno)"] == pytest.approx(0.0, abs=1e-12)
    assert mappa["Gas ACS baseline (kWh/anno)"] == pytest.approx(3392.575163398693)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(10837.942154316272)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(9297.329545454544)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(1540.6126088617275)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(4.493175746965452)
    assert mappa["Payback (anni)"] == 12
    assert mappa["Verdetto"] == "NON_CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] is None


def test_demo_coerenza_interna():
    bc = mh804_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["kg_polli_anno"] == pytest.approx(
        bc["kg_polli_giorno"] * bc["giorni_anno"])
    assert bc["q_cottura_kwh_anno"] == pytest.approx(
        bc["kg_polli_anno"] * bc["q_cottura_per_kg"])
    assert bc["gas_girarrosto_base_kwh_anno"] == pytest.approx(
        bc["q_cottura_kwh_anno"] / bc["eta_girarrosto_base"])
    assert bc["gas_girarrosto_alt_kwh_anno"] == pytest.approx(
        bc["q_cottura_kwh_anno"] / bc["eta_girarrosto_alt"])
    assert bc["e_banchi_base_kwh_anno"] == pytest.approx(
        bc["kg_polli_anno"] * bc["q_banchi_per_kg"] * 1.0)
    assert bc["e_banchi_alt_kwh_anno"] == pytest.approx(
        bc["kg_polli_anno"] * bc["q_banchi_per_kg"]
        * bc["fattore_banchi_alt"])
    assert bc["q_celle_kwh_anno"] == pytest.approx(
        bc["kg_polli_anno"] * bc["q_celle_per_kg"])
    assert bc["e_freddo_base_kwh_anno"] == pytest.approx(
        bc["q_celle_kwh_anno"] / bc["cop_freddo_base"])
    assert bc["e_freddo_alt_kwh_anno"] == pytest.approx(
        bc["q_celle_kwh_anno"] / bc["cop_freddo_alt"])
    assert bc["q_acs_kwh_anno"] == pytest.approx(
        bc["litri_acs_giorno"] * bc["giorni_anno"]
        * 4.186 * bc["delta_t_acs"] / 3600.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(
        min(bc["q_acs_kwh_anno"],
            bc["q_cottura_kwh_anno"] * bc["f_rec"]))
    assert bc["q_acs_net_kwh_anno"] == pytest.approx(
        max(0.0, bc["q_acs_kwh_anno"] - bc["q_rec_kwh_anno"]))
    assert bc["gas_acs_base_kwh_anno"] == pytest.approx(
        bc["q_acs_kwh_anno"] / bc["eta_caldaia_base"])
    assert bc["e_pdc_acs_kwh_anno"] == pytest.approx(
        bc["q_acs_net_kwh_anno"] / bc["cop_pdc_acs"])
    assert bc["co2_evitata_t_anno"] == pytest.approx(
        bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])
    assert bc["c_base_eur_anno"] == pytest.approx(
        (bc["gas_girarrosto_base_kwh_anno"]
         + bc["gas_acs_base_kwh_anno"]) / 1000.0 * bc["p_gas"]
        + (bc["e_banchi_base_kwh_anno"]
           + bc["e_freddo_base_kwh_anno"]) / 1000.0 * bc["p_el"]
        + bc["om_base"])
    assert bc["c_alt_eur_anno"] == pytest.approx(
        bc["gas_girarrosto_alt_kwh_anno"] / 1000.0 * bc["p_gas"]
        + (bc["e_banchi_alt_kwh_anno"]
           + bc["e_freddo_alt_kwh_anno"]
           + bc["e_pdc_acs_kwh_anno"])
        / 1000.0 * bc["p_el"]
        + bc["om_alt"])


def test_demo_contro_riconteggio_indipendente():
    kgg, gg, qc = 120, 310, 1.20
    egb, ega = 0.70, 0.88
    qb, fba, qcel = 0.25, 0.80, 0.30
    cfb, cfa = 2.2, 3.2
    lit, dt, frec = 200, 40, 0.08
    eta, copp = 0.85, 3.2
    pg, pel = 90, 250
    omb, oma, cx = 1200, 2000, 18000
    fg, fel, wacc, vita = 0.20, 0.35, 5.0, 15
    kga = kgg * gg
    qcott = kga * qc
    ggb = qcott / egb
    gga = qcott / ega
    ebb = kga * qb * 1.0
    eba = kga * qb * fba
    qce = kga * qcel
    efbk = qce / cfb
    efak = qce / cfa
    qacs = lit * gg * 4.186 * dt / 3600.0
    qrec = min(qacs, qcott * frec)
    qnet = max(0.0, qacs - qrec)
    gasa = qacs / eta
    epdc = qnet / copp
    cb = (ggb + gasa) / 1000.0 * pg + (ebb + efbk) / 1000.0 * pel + omb
    ca = gga / 1000.0 * pg + (eba + efak + epdc) / 1000.0 * pel + oma
    risp = cb - ca
    co2b = (ggb + gasa) / 1000.0 * fg + (ebb + efbk) / 1000.0 * fel
    co2a = gga / 1000.0 * fg + (eba + efak + epdc) / 1000.0 * fel
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    bc = mh804_demo_calcoli()
    assert bc["kg_polli_anno"] == pytest.approx(kga)
    assert bc["q_cottura_kwh_anno"] == pytest.approx(qcott)
    assert bc["gas_girarrosto_base_kwh_anno"] == pytest.approx(ggb)
    assert bc["gas_girarrosto_alt_kwh_anno"] == pytest.approx(gga)
    assert bc["e_banchi_base_kwh_anno"] == pytest.approx(ebb)
    assert bc["e_banchi_alt_kwh_anno"] == pytest.approx(eba)
    assert bc["q_celle_kwh_anno"] == pytest.approx(qce)
    assert bc["e_freddo_base_kwh_anno"] == pytest.approx(efbk)
    assert bc["e_freddo_alt_kwh_anno"] == pytest.approx(efak)
    assert bc["q_acs_kwh_anno"] == pytest.approx(qacs)
    assert bc["q_rec_kwh_anno"] == pytest.approx(qrec)
    assert bc["q_acs_net_kwh_anno"] == pytest.approx(qnet)
    assert bc["gas_acs_base_kwh_anno"] == pytest.approx(gasa)
    assert bc["e_pdc_acs_kwh_anno"] == pytest.approx(epdc)
    assert bc["c_base_eur_anno"] == pytest.approx(cb)
    assert bc["c_alt_eur_anno"] == pytest.approx(ca)
    assert bc["risparmio_eur_anno"] == pytest.approx(risp)
    assert bc["co2_base_t_anno"] == pytest.approx(co2b)
    assert bc["co2_alt_t_anno"] == pytest.approx(co2a)
    assert bc["co2_evitata_t_anno"] == pytest.approx(co2)
    assert bc["van"] == pytest.approx(van)
    assert bc["breakeven_gas_eur_mwh"] is None


# ---------------------------------------------------------------- varianti
def test_variante_gas_zero_helper_calcola_ma_ui_guard():
    # Negli helper p_gas = 0 e' ammesso (non negativo) e
    # il risparmio resta positivo (61,31 EUR/anno) perche'
    # banchi e celle efficienti risparmiano elettricita':
    # verdetto NON_CONVIENTE, breakeven None. La UI pero'
    # ha la guard piu' stretta (prezzi <= 0 ->
    # NON_CALCOLABILE): vedi test_ui_guard_degenere_stretta.
    bc = _variante(p_gas=0)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(61.3068, abs=1e-2)
    assert bc["van"] == pytest.approx(-17363.66, abs=1e-2)
    assert bc["payback"] is None
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_gas_alto_conviente():
    bc = _variante(p_gas=150)
    assert bc["risparmio_eur_anno"] == pytest.approx(2526.8165, abs=1e-2)
    assert bc["van"] == pytest.approx(8227.4909, abs=1e-2)
    assert bc["tir"] == pytest.approx(11.170777996924071)
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_senza_recupero_non_conviente():
    bc = _variante(f_rec=0)
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["q_acs_net_kwh_anno"] == pytest.approx(2883.688888888889)
    assert bc["e_pdc_acs_kwh_anno"] == pytest.approx(901.1527777777778)
    assert bc["risparmio_eur_anno"] == pytest.approx(1315.3230, abs=1e-2)
    assert bc["van"] == pytest.approx(-4347.38, abs=1e-2)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(9.976520038398048)
    assert bc["payback"] == 14
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_recupero_parziale_senza_saturazione():
    bc = _variante(f_rec=0.05)
    assert bc["q_rec_kwh_anno"] == pytest.approx(2232.0)
    assert bc["q_acs_net_kwh_anno"] == pytest.approx(651.688888888889)
    assert bc["e_pdc_acs_kwh_anno"] == pytest.approx(203.65277777777777)
    assert bc["risparmio_eur_anno"] == pytest.approx(1489.70, abs=1e-2)
    assert bc["van"] == pytest.approx(-2537.43, abs=1e-2)
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["payback"] == 13
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_recupero_pieno_satura():
    bc = _variante(f_rec=1.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(2883.688888888889)
    assert bc["q_acs_net_kwh_anno"] == 0.0
    assert bc["e_pdc_acs_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(1540.6126088617275)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_acs_doppia_marginale():
    bc = _variante(litri_acs_giorno=400)
    assert bc["q_acs_kwh_anno"] == pytest.approx(5767.377777777778)
    assert bc["q_rec_kwh_anno"] == pytest.approx(3571.2)
    assert bc["q_acs_net_kwh_anno"] == pytest.approx(2196.177777777778)
    assert bc["risparmio_eur_anno"] == pytest.approx(1674.37, abs=1e-2)
    assert bc["van"] == pytest.approx(-620.63, abs=1e-2)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(5.560939437638924)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"


def test_variante_acs_zero():
    bc = _variante(litri_acs_giorno=0)
    assert bc["q_acs_kwh_anno"] == 0.0
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["gas_acs_base_kwh_anno"] == 0.0
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["risparmio_eur_anno"] == pytest.approx(1235.2808, abs=1e-2)
    assert bc["van"] == pytest.approx(-5178.21, abs=1e-2)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_polli_piccoli_e_grandi():
    bc = _variante(kg_polli_giorno=60)
    assert bc["kg_polli_anno"] == pytest.approx(18600.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(437.18, abs=1e-2)
    assert bc["van"] == pytest.approx(-13462.18, abs=1e-2)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(45.9052658151232)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"
    bc2 = _variante(kg_polli_giorno=240)
    assert bc2["risparmio_eur_anno"] == pytest.approx(3575.89, abs=1e-2)
    assert bc2["van"] == pytest.approx(19116.55, abs=1e-2)
    assert bc2["payback"] == 6
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_capex_marginale_conviente():
    bc = _variante(capex=16000)
    assert bc["risparmio_eur_anno"] == pytest.approx(1540.6126088617275)
    assert bc["van"] == pytest.approx(-8.97, abs=1e-2)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"
    bc2 = _variante(capex=14000)
    assert bc2["van"] == pytest.approx(1991.03, abs=1e-2)
    assert bc2["payback"] == 10
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex=0)
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(15991.032049293999, rel=1e-6)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(5109.189132926913)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(-6103.80, abs=1e-2)
    assert bc2["payback"] is None
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_el_alto_e_om_alt_alto():
    bc = _variante(p_el=400)
    assert bc["risparmio_eur_anno"] == pytest.approx(2057.3967, abs=1e-2)
    assert bc["van"] == pytest.approx(3355.0742, abs=1e-2)
    assert bc["payback"] == 9
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(om_alt=3000)
    assert bc2["risparmio_eur_anno"] == pytest.approx(540.61, abs=1e-2)
    assert bc2["breakeven_gas_eur_mwh"] == pytest.approx(57.10948128230282)
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_senza_celle_e_senza_banchi():
    bc = _variante(q_celle_per_kg=0)
    assert bc["q_celle_kwh_anno"] == 0.0
    assert bc["e_freddo_base_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(1144.31, abs=1e-2)
    assert bc["van"] == pytest.approx(-6122.50, abs=1e-2)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(20.38118162583726)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"
    bc2 = _variante(q_banchi_per_kg=0)
    assert bc2["e_banchi_base_kwh_anno"] == 0.0
    assert bc2["e_banchi_alt_kwh_anno"] == 0.0
    assert bc2["risparmio_eur_anno"] == pytest.approx(1075.6126, abs=1e-2)
    assert bc2["van"] == pytest.approx(-6835.51, abs=1e-2)
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_senza_polli_non_calcolabile():
    bc = _variante(kg_polli_giorno=0)
    assert bc["kg_polli_anno"] == 0.0
    assert bc["q_cottura_kwh_anno"] == 0.0
    assert bc["e_banchi_base_kwh_anno"] == 0.0
    assert bc["q_celle_kwh_anno"] == 0.0
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(302.2153217137)
    assert bc["risparmio_eur_anno"] == pytest.approx(-719.96, abs=1e-2)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_girarrosto_alt_uguale_base():
    bc = _variante(eta_girarrosto_alt=0.70)
    assert bc["gas_girarrosto_alt_kwh_anno"] == pytest.approx(63771.42857142857)
    assert bc["risparmio_eur_anno"] == pytest.approx(366.64, abs=1e-2)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_monotonia_prezzo_gas_crescente():
    base = mh804_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas=91)["risparmio_eur_anno"]
    basso = _variante(p_gas=89)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(16.4367, abs=1e-2)
    assert base - basso == pytest.approx(16.4367, abs=1e-2)


def test_monotonia_polli_crescente():
    assert _variante(kg_polli_giorno=60)["risparmio_eur_anno"] < \
        mh804_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(kg_polli_giorno=240)["risparmio_eur_anno"] > \
        mh804_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(kg_polli_giorno=240)["kg_polli_anno"] == \
        pytest.approx(74400.0)


def test_demo_deterministica_due_chiamate():
    a = mh804_demo_calcoli()
    b = mh804_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh804_demo().keys()) == {
        "kg_polli_giorno", "giorni_anno",
        "q_cottura_per_kg",
        "eta_girarrosto_base", "eta_girarrosto_alt",
        "q_banchi_per_kg", "fattore_banchi_alt",
        "q_celle_per_kg",
        "cop_freddo_base", "cop_freddo_alt",
        "litri_acs_giorno", "delta_t_acs",
        "f_rec", "eta_caldaia_base", "cop_pdc_acs",
        "p_gas", "p_el",
        "om_base", "om_alt",
        "capex", "wacc_pct", "vita_anni",
        "f_gas", "f_el",
        "tolleranza_pct"}


# ---------------------------------------------------------------- degenere
def test_degenere_cop_uguale_uno_sollevela():
    with pytest.raises(ValueError):
        _variante(cop_freddo_base=1.0)
    with pytest.raises(ValueError):
        _variante(cop_freddo_alt=1.0)
    with pytest.raises(ValueError):
        _variante(cop_pdc_acs=1.0)


def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"kg_polli_giorno": -10},
               {"giorni_anno": 0},
               {"giorni_anno": 2.5},
               {"q_cottura_per_kg": -0.1},
               {"eta_girarrosto_base": 0}, {"eta_girarrosto_base": 1.01},
               {"eta_girarrosto_alt": 0}, {"eta_girarrosto_alt": 1.01},
               {"q_banchi_per_kg": -0.1},
               {"fattore_banchi_alt": 0}, {"fattore_banchi_alt": 1.01},
               {"q_celle_per_kg": -0.1},
               {"cop_freddo_base": 1.0}, {"cop_freddo_base": 0.5},
               {"cop_freddo_alt": 1.0}, {"cop_freddo_alt": 0.5},
               {"litri_acs_giorno": -1},
               {"delta_t_acs": 0}, {"delta_t_acs": -5},
               {"f_rec": -0.1},
               {"f_rec": 1.01},
               {"eta_caldaia_base": 0}, {"eta_caldaia_base": 1.01},
               {"cop_pdc_acs": 1.0}, {"cop_pdc_acs": 0.5},
               {"p_gas": -1},
               {"p_el": -1},
               {"om_base": -100},
               {"om_alt": -100},
               {"capex": -1},
               {"wacc_pct": -1}, {"wacc_pct": 60},
               {"vita_anni": 0}, {"vita_anni": 2.5},
               {"f_gas": -0.10},
               {"f_el": -0.10},
               {"tolleranza_pct": -1},
               {"tolleranza_pct": 100.1}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh804_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"kg_polli_giorno": "120"},
               {"kg_polli_giorno": float("nan")},
               {"p_gas": float("inf")},
               {"capex": True},
               {"q_celle_per_kg": "0.30"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh804_valida(**d)["valido"] is False


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    for kw in ({"kg_polli_giorno": 0},
               {"om_alt": 5000}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] <= 0.0
        assert bc["verdetto"] == "NON_CALCOLABILE"
        assert bc["flussi"]


def test_pareggio_esatto_tolleranza_float():
    # A pareggio esatto (prezzo gas = breakeven della
    # variante senza recupero) il risparmio e' zero
    # (circa 0.0, quindi guard NON_CALCOLABILE):
    # in nessun caso CONVIENTE.
    be = _variante(f_rec=0)["breakeven_gas_eur_mwh"]
    bc = _variante(f_rec=0, p_gas=be)
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["verdetto"] != "CONVIENTE"
    bc2 = _variante(f_rec=0, p_gas=be + 1)
    assert bc2["risparmio_eur_anno"] == pytest.approx(16.4367, abs=1e-2)
    assert bc2["van"] == pytest.approx(-17829.39, abs=1e-2)
    assert bc2["verdetto"] == "NON_CONVIENTE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh804_demo_calcoli()
    testo = mh804_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;NON_CONVIENTE" in testo
    assert "breakeven_gas_eur_mwh" in testo
    assert "co2_evitata_t_anno" in testo
    assert "q_cottura_kwh_anno" in testo
    assert "kg_polli_giorno" in testo
    assert "e_freddo_alt_kwh_anno" in testo
    assert "e_banchi_alt_kwh_anno" in testo
    assert "q_rec_kwh_anno" in testo
    assert "q_acs_net_kwh_anno" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh804_demo_calcoli()
    testo = mh804_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"kg_polli_anno;{bc['kg_polli_anno']}" in testo
    assert f"gas_acs_base_kwh_anno;{bc['gas_acs_base_kwh_anno']}" in testo
    assert f"q_celle_kwh_anno;{bc['q_celle_kwh_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh804_demo_calcoli()
    testo = mh804_csv(bc, _demo_kwargs())
    for chiave in _demo_kwargs():
        assert f"{chiave};" in testo


# ------------------------------------------------------- test strutturali
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _leggi(nome):
    qui = os.path.dirname(os.path.abspath(__file__))
    p = os.path.join(qui, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    with open(p, encoding="utf-8") as f:
        return f.read()


def _vietati():
    # Token della scheda precedente, costruiti
    # per concatenazione: questo stesso file non li contiene
    # come sottostringhe contigue.
    return ["mh" + "80" + "3", "st" + "80" + "3",
            "tab" + "80" + "3", "w" + "80" + "4",
            "mh" + "80" + "2", "tab" + "80" + "2"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w805_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w805_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab804:")


def test_ui_apre_scheda_attesa_una_volta():
    """Il frammento UI apre la scheda attesa, una sola volta."""
    src = _leggi("w805_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert src.count("with tab804:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w805_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w805_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st804_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) >= 28
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w805_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 4
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_ui_guard_degenere_stretta():
    """La guard UI della scheda dichiara NON_CALCOLABILE
    anche per kg <= 0, prezzi <= 0 e CAPEX <= 0 (piu'
    stretta degli helper, che ammettono lo zero)."""
    src = _leggi("w805_ui.py")
    assert "float(_kg804) <= 0.0" in src
    assert "float(_pg804) <= 0.0" in src
    assert "float(_pel804) <= 0.0" in src
    assert "float(_cx804) <= 0.0" in src
    assert "int(_vita804) <= 0" in src
    assert "Verdetto: NON_CALCOLABILE" in src


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w805_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def804[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w805_ui.py")
        usate = set(re.findall(r'_def804\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 25
        assert usate <= set(mh804_demo().keys())
