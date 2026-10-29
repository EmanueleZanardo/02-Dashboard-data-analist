"""Test nuova scheda "Tavola calda: forno combinato
efficiente + banchi caldi efficienti + celle
efficienti + recupero calore cucina su ACS batte
cucina a gas vecchia + banchi e celle tradizionali
+ caldaia a gas?" (titolo completo nel frammento UI).
Contenuto pronto da scrivere in repo come test
della scheda tavola calda.

Business case deterministico di una tavola calda
guidato dalle PORZIONI AL GIORNO e dai GIORNI DI
APERTURA ALL'ANNO: le porzioni guidano il calore
di cottura della cucina (kWh_th per porzione), i
banchi caldi di mantenimento (kWh_e per porzione,
elettrici) e il carico frigorifero delle celle
(kWh_c per porzione); i litri di ACS al giorno
guidano il lavaggio di stoviglie e attrezzature.
Porzioni annue = porzioni al giorno x giorni;
calore di cottura = porzioni annue x kWh_th per
porzione; gas cucina base e alt = Q_cottura / eta
(stesso calore utile, rendimento diverso: cucina
vecchia contro forno combinato efficiente);
elettricita' banchi base e alt = porzioni annue x
kWh_e per porzione x fattore (base 1,00, alt
0,75); carico celle = porzioni annue x kWh_c per
porzione; elettricita' freddo base e alt =
Q_celle / COP (stesso carico, COP diverso);
ACS = litri x giorni x 4,186 x delta_T / 3600;
recupero = min(ACS, Q_cottura x f_rec) (saturato
all'ACS; nel demo NON satura: il recupero grezzo
3.797,50 e' sotto l'ACS 4.325,53); ACS netta =
max(0, ACS - recupero); gas ACS baseline = ACS /
eta_caldaia (senza recupero); elettricita' PdC
ACS = ACS netta / COP_pdc_acs; C_base =
(gas_cucina_base + gas_acs_base) / 1000 x p_gas +
(E_banchi_base + E_freddo_base) / 1000 x p_el +
O&M_base; C_alt = gas_cucina_alt / 1000 x p_gas +
(E_banchi_alt + E_freddo_alt + E_pdc_acs)
/ 1000 x p_el + O&M_alt; risparmio = C_base -
C_alt; CO2_base = (gas_cucina_base +
gas_acs_base) / 1000 x f_gas + (E_banchi_base
+ E_freddo_base) / 1000 x f_el; CO2_alt =
gas_cucina_alt / 1000 x f_gas +
(E_banchi_alt + E_freddo_alt + E_pdc_acs)
/ 1000 x f_el; CO2_evitata = CO2_base -
CO2_alt; flussi [-CAPEX, risparmio x vita];
VAN, TIR, payback (primo anno con cumulato
>= 0); breakeven gas = ((E_banchi_alt +
E_freddo_alt + E_pdc_acs) / 1000 x p_el +
O&M_alt - (E_banchi_base + E_freddo_base)
/ 1000 x p_el - O&M_base) /
((gas_cucina_base + gas_acs_base -
gas_cucina_alt) / 1000) EUR/MWh, None se
denominatore gas <= 0 o numeratore < 0,
SOGLIA MINIMA quando esiste.
Verdetto: NON_CALCOLABILE se input degenere
(porzioni <= 0, giorni <= 0, eta <= 0 o > 1, COP
<= 1, delta_T <= 0, f_rec fuori [0, 1],
prezzi <= 0, CAPEX <= 0, vita <= 0) o se
risparmio <= 0 (guard degenere: UI salta KPI,
grafico, tabella e CSV); altrimenti CONVIENTE
se VAN > 0, MARGINALE se VAN negativa entro
tolleranza % del CAPEX, NON_CONVIENTE se VAN
negativa oltre la tolleranza. Distinzione
esplicita: distinto dalla rosticceria (prodotto
arrosto pesato in kg al giorno, non porzioni:
qui il driver sono le porzioni servite al
giorno e la cottura e' quella del forno
combinato della tavola calda, con banchi caldi
di mantenimento delle porzioni e celle delle
porzioni, e il recupero va sull'ACS di lavaggio
di stoviglie e attrezzature), dalla pasticceria
(kg di dolci, abbattitore da T_in a T_out, celle
dei dolci: qui nessun dolce, nessun abbattitore,
i banchi sono caldi di mantenimento), dal
ristorante (coperti, ACS di cucina, celle frigo
di cucina: qui niente coperti, niente ACS di
cucina, il freddo segue le porzioni), dal
panificio (kg di pane per la cottura del pane:
qui nessun pane), dalla gelateria (litri di
gelato, pastorizzazione, freddo del gelato:
qui nessuna pastorizzazione, nessun gelato, il
freddo e' quello delle celle delle porzioni),
dalla pescheria (kg di pesce, macchina del
ghiaccio in scaglie, recupero dai condensatori:
qui nessun pesce, nessun ghiaccio, il recupero
viene dal calore della cucina), dal fioraio
(superficie negozio per riscaldamento piu'
cella fiori, recupero sul riscaldamento: qui
niente riscaldamento, recupero sull'ACS di
lavaggio), dal parrucchiere (lavaggi di capelli,
ACS, recupero dalle acque reflue), dalla
farmacia (superficie di vendita piu'
frigoriferi farmaceutici, recupero dai
frigoriferi, nessuna cucina), dall'albergo
(pernottamento, ACS docce ospiti), dalla
palestra (docce utenti, recupero dalle acque
delle docce), dall'autolavaggio (veicoli lavati,
acque di lavaggio dei veicoli) e dal
palaghiaccio (pista da pattinaggio, freddo di
pista verso spogliatoi): qui driver PORZIONI +
GIORNI + ACS = porzioni al giorno per cottura,
banchi e celle, giorni di apertura per l'anno,
litri di ACS per il lavaggio; niente kg di
prodotto arrosto, niente dolci, niente gelato,
niente pesce, niente lavaggi, niente coperti,
niente docce, niente veicoli, niente frigoriferi
farmaceutici, niente pista.

Demo (tavola calda): 350 porzioni al giorno per
310 giorni di apertura all'anno (108.500
porzioni all'anno), calore di cottura 0,35
kWh_th per porzione (37.975 kWh_th/anno),
cucina base 0,60 e alt 0,85, banchi caldi 0,08
kWh_e per porzione con fattore base 1,00 e alt
0,75, carico celle 0,12 kWh_c per porzione, COP
freddo base 2,2 e alt 3,1, ACS di lavaggio 300
litri al giorno con delta_T 40 K, f_rec 0,10,
caldaia 0,85, COP PdC ACS 3,0, gas 90, el 250
EUR/MWh, O&M base 1.500, alt 2.600, CAPEX
22.000, WACC 5 %, vita 15, f_gas 0,20, f_el
0,35, tolleranza 10 % del CAPEX.
Valori calcolati eseguendo mh805_demo_calcoli():
porzioni annue 108.500, Q_cottura 37.975,
gas_cucina_base 63.291,66666666667,
gas_cucina_alt 44.676,470588235294,
E_banchi_base 8.680, E_banchi_alt 6.510,
Q_celle 13.020, E_freddo_base
5.918,181818181818, E_freddo_alt 4.200,
Q_acs 4.325,533333333334, Q_rec 3.797,5 (NON
saturato: il recupero grezzo 37.975 x 0,10 =
3.797,50 e' sotto l'ACS), Q_acs_net
528,0333333333338, gas_acs_base
5.088,86274509804, E_pdc_acs
176,01111111111126, C_base
11.303,793101604278, C_alt 9.342,385130718954,
risparmio 1.961,4079708853242, CO2_base
18,785469518716578, CO2_alt
12,745398006535947, CO2_evitata
6,040071512180631, VAN -1.641,2559888486612,
TIR 3,874706593609684 %, payback 12,
breakeven gas 7,254340892102108 EUR/MWh
(soglia minima: sopra vince, sotto perde),
verdetto MARGINALE (VAN negativa entro la
tolleranza del 10 % = 2.200 EUR).
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w806_helpers import (
    demo_calcoli,
    mh805_breakeven_gas,
    mh805_c_alt,
    mh805_c_base,
    mh805_calcola,
    mh805_co2_alt,
    mh805_co2_base,
    mh805_co2_evitata,
    mh805_cop,
    mh805_csv,
    mh805_demo,
    mh805_demo_calcoli,
    mh805_e_banchi,
    mh805_e_freddo,
    mh805_e_pdc_acs,
    mh805_eta,
    mh805_flussi,
    mh805_frazione,
    mh805_gas_acs,
    mh805_gas_cucina,
    mh805_int_pos,
    mh805_num,
    mh805_nneg,
    mh805_payback,
    mh805_pct_tolleranza,
    mh805_pct_wacc,
    mh805_porzioni_anno,
    mh805_pos,
    mh805_q_acs,
    mh805_q_acs_net,
    mh805_q_celle,
    mh805_q_cottura,
    mh805_q_rec,
    mh805_risparmio,
    mh805_tir,
    mh805_valida,
    mh805_van,
    mh805_verdetto,
)

_DEMO = {
    "porzioni_anno": 108500.0,
    "q_cottura_kwh_anno": 37975.0,
    "gas_cucina_base_kwh_anno": 63291.66666666667,
    "gas_cucina_alt_kwh_anno": 44676.470588235294,
    "e_banchi_base_kwh_anno": 8680.0,
    "e_banchi_alt_kwh_anno": 6510.0,
    "q_celle_kwh_anno": 13020.0,
    "e_freddo_base_kwh_anno": 5918.181818181818,
    "e_freddo_alt_kwh_anno": 4200.0,
    "q_acs_kwh_anno": 4325.533333333334,
    "q_rec_kwh_anno": 3797.5,
    "q_acs_net_kwh_anno": 528.0333333333338,
    "gas_acs_base_kwh_anno": 5088.86274509804,
    "e_pdc_acs_kwh_anno": 176.01111111111126,
    "c_base_eur_anno": 11303.793101604278,
    "c_alt_eur_anno": 9342.385130718954,
    "risparmio_eur_anno": 1961.4079708853242,
    "co2_base_t_anno": 18.785469518716578,
    "co2_alt_t_anno": 12.745398006535947,
    "co2_evitata_t_anno": 6.040071512180631,
    "van": -1641.2559888486612,
    "tir": 3.874706593609684,
}


def _demo_kwargs():
    return dict(mh805_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh805_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh805_num(3, "x") == 3.0
    assert mh805_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh805_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh805_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh805_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh805_pos(0, "x")
    with pytest.raises(ValueError):
        mh805_pos(-1, "x")
    assert mh805_pos(0.5, "x") == 0.5


def test_cop_maggiore_di_uno():
    assert mh805_cop(3.0, "x") == 3.0
    assert mh805_cop(1.01, "x") == 1.01
    with pytest.raises(ValueError):
        mh805_cop(1.0, "x")
    with pytest.raises(ValueError):
        mh805_cop(0.5, "x")
    with pytest.raises(ValueError):
        mh805_cop(0, "x")


def test_frazione_limiti():
    assert mh805_frazione(0, "x") == 0.0
    assert mh805_frazione(1, "x") == 1.0
    assert mh805_frazione(0.10, "x") == 0.10
    with pytest.raises(ValueError):
        mh805_frazione(-0.01, "x")
    with pytest.raises(ValueError):
        mh805_frazione(1.01, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh805_int_pos(5.0, "x") == 5
    assert mh805_int_pos(310.0, "x") == 310
    with pytest.raises(ValueError):
        mh805_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh805_int_pos(0, "x")


def test_eta_limiti():
    assert mh805_eta(1.0, "x") == 1.0
    assert mh805_eta(0.85, "x") == 0.85
    with pytest.raises(ValueError):
        mh805_eta(0, "x")
    with pytest.raises(ValueError):
        mh805_eta(1.01, "x")


def test_pct_wacc_limiti():
    assert mh805_pct_wacc(0, "x") == 0.0
    assert mh805_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh805_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh805_pct_tolleranza(0, "x") == 0.0
    assert mh805_pct_tolleranza(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh805_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh805_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_porzioni_anno_e_q_cottura():
    assert mh805_porzioni_anno(350, 310) == 108500.0
    assert mh805_porzioni_anno(0, 310) == 0.0
    assert mh805_porzioni_anno(175, 310) == 54250.0
    assert mh805_q_cottura(108500, 0.35) == 37975.0
    assert mh805_q_cottura(108500, 0) == 0.0
    assert mh805_q_cottura(54250, 0.35) == 18987.5
    with pytest.raises(ValueError):
        mh805_porzioni_anno(-1, 310)
    with pytest.raises(ValueError):
        mh805_porzioni_anno(350, 0)
    with pytest.raises(ValueError):
        mh805_porzioni_anno(350, 2.5)
    with pytest.raises(ValueError):
        mh805_q_cottura(108500, -0.1)


def test_gas_cucina_rendimenti():
    assert mh805_gas_cucina(37975.0, 0.60) == pytest.approx(63291.66666666667)
    assert mh805_gas_cucina(37975.0, 0.85) == pytest.approx(44676.470588235294)
    assert mh805_gas_cucina(37975.0, 1.0) == 37975.0
    assert mh805_gas_cucina(0, 0.60) == 0.0
    with pytest.raises(ValueError):
        mh805_gas_cucina(37975.0, 0)
    with pytest.raises(ValueError):
        mh805_gas_cucina(37975.0, 1.01)


def test_e_banchi_fattori():
    assert mh805_e_banchi(108500, 0.08, 1.0) == 8680.0
    assert mh805_e_banchi(108500, 0.08, 0.75) == 6510.0
    assert mh805_e_banchi(0, 0.08, 1.0) == 0.0
    assert mh805_e_banchi(108500, 0, 0.75) == 0.0
    with pytest.raises(ValueError):
        mh805_e_banchi(108500, 0.08, 0)
    with pytest.raises(ValueError):
        mh805_e_banchi(108500, 0.08, 1.01)
    with pytest.raises(ValueError):
        mh805_e_banchi(108500, -0.1, 0.75)
    with pytest.raises(ValueError):
        mh805_e_banchi(-1, 0.08, 0.75)


def test_q_celle_e_freddo():
    assert mh805_q_celle(108500, 0.12) == 13020.0
    assert mh805_q_celle(0, 0.12) == 0.0
    assert mh805_q_celle(108500, 0) == 0.0
    assert mh805_e_freddo(13020.0, 2.2) == pytest.approx(5918.181818181818)
    assert mh805_e_freddo(13020.0, 3.1) == pytest.approx(4200.0)
    assert mh805_e_freddo(0, 2.2) == 0.0
    with pytest.raises(ValueError):
        mh805_q_celle(108500, -0.1)
    with pytest.raises(ValueError):
        mh805_e_freddo(13020.0, 1.0)
    with pytest.raises(ValueError):
        mh805_e_freddo(-1, 2.2)


def test_q_acs_formula():
    assert mh805_q_acs(300, 310, 40) == pytest.approx(4325.533333333334)
    assert mh805_q_acs(0, 310, 40) == 0.0
    assert mh805_q_acs(600, 310, 40) == pytest.approx(8651.066666666668)
    assert mh805_q_acs(300, 310, 20) == pytest.approx(2162.766666666667)
    with pytest.raises(ValueError):
        mh805_q_acs(-1, 310, 40)
    with pytest.raises(ValueError):
        mh805_q_acs(300, 0, 40)
    with pytest.raises(ValueError):
        mh805_q_acs(300, 310, 0)
    with pytest.raises(ValueError):
        mh805_q_acs(300, 2.5, 40)


def test_q_rec_saturazione_e_acs_netta():
    # Demo: recupero grezzo 3.797,50 sotto l'ACS -> NON satura.
    assert mh805_q_rec(37975.0, 0.10, 4325.533333333334) == pytest.approx(3797.5)
    assert mh805_q_rec(37975.0, 0, 4325.533333333334) == 0.0
    assert mh805_q_rec(37975.0, 0.05, 4325.533333333334) == pytest.approx(1898.75)
    # Con f_rec 1,0 il recupero satura all'ACS.
    assert mh805_q_rec(37975.0, 1.0, 4325.533333333334) == 4325.533333333334
    with pytest.raises(ValueError):
        mh805_q_rec(37975.0, 1.01, 4325.533333333334)
    with pytest.raises(ValueError):
        mh805_q_rec(37975.0, -0.1, 4325.533333333334)
    assert mh805_q_acs_net(4325.533333333334, 3797.5) == pytest.approx(528.0333333333338)
    assert mh805_q_acs_net(4325.533333333334, 0.0) == pytest.approx(4325.533333333334)
    assert mh805_q_acs_net(4325.533333333334, 4325.533333333334) == 0.0
    with pytest.raises(ValueError):
        mh805_q_acs_net(-1, 3797.5)
    with pytest.raises(ValueError):
        mh805_q_acs_net(4325.533333333334, -1)


def test_gas_acs_e_pdc_acs():
    assert mh805_gas_acs(4325.533333333334, 0.85) == pytest.approx(5088.86274509804)
    assert mh805_gas_acs(0, 0.85) == 0.0
    assert mh805_gas_acs(4325.533333333334, 1.0) == pytest.approx(4325.533333333334)
    assert mh805_e_pdc_acs(528.0333333333338, 3.0) == pytest.approx(176.01111111111126)
    assert mh805_e_pdc_acs(0.0, 3.0) == 0.0
    with pytest.raises(ValueError):
        mh805_gas_acs(4325.533333333334, 0)
    with pytest.raises(ValueError):
        mh805_gas_acs(4325.533333333334, 1.01)
    with pytest.raises(ValueError):
        mh805_e_pdc_acs(528.0333333333338, 1.0)


def test_c_base_c_alt_scomposizione():
    assert mh805_c_base(63291.66666666667, 5088.86274509804, 90,
                        8680.0, 5918.181818181818, 250,
                        1500) == pytest.approx(11303.793101604278)
    assert mh805_c_base(63291.66666666667, 5088.86274509804, 0,
                        8680.0, 5918.181818181818, 250,
                        1500) == pytest.approx(5149.545454545455)
    assert mh805_c_alt(44676.470588235294, 90, 6510.0,
                       4200.0, 176.01111111111126, 250,
                       2600) == pytest.approx(9342.385130718954)
    assert mh805_c_alt(44676.470588235294, 90, 6510.0,
                       4200.0, 0.0, 250,
                       2600) == pytest.approx(9298.382352941176)
    with pytest.raises(ValueError):
        mh805_c_base(63291.67, 5088.86, 90, 8680.0, 5918.18, 250, -1)
    with pytest.raises(ValueError):
        mh805_c_alt(44676.47, 90, 6510.0, 4200.0, 176.01, 250, -1)


def test_risparmio_segno():
    assert mh805_risparmio(11303.793101604278, 9342.385130718954) == pytest.approx(1961.4079708853242)
    assert mh805_risparmio(9342.39, 9342.39) == 0.0


def test_co2_base_alt_evitata():
    assert mh805_co2_base(63291.66666666667, 5088.86274509804, 0.20,
                          8680.0, 5918.181818181818,
                          0.35) == pytest.approx(18.785469518716578)
    assert mh805_co2_alt(44676.470588235294, 0.20, 6510.0,
                         4200.0, 176.01111111111126,
                         0.35) == pytest.approx(12.745398006535947)
    assert mh805_co2_evitata(63291.66666666667, 5088.86274509804, 0.20,
                             8680.0, 5918.181818181818,
                             44676.470588235294, 6510.0,
                             4200.0, 176.01111111111126,
                             0.35) == pytest.approx(6.040071512180631)
    assert mh805_co2_base(0, 0, 0.20, 0, 0, 0.35) == pytest.approx(0.0)
    assert mh805_co2_alt(0, 0.20, 0, 0, 0, 0.35) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh805_co2_base(63291.67, 5088.86, -0.10, 8680.0, 5918.18, 0.35)
    with pytest.raises(ValueError):
        mh805_co2_alt(44676.47, 0.20, 6510.0, 4200.0, 176.01, -0.10)


def test_breakeven_demo_e_varianti():
    # Demo: breakeven 7,25 EUR/MWh (soglia minima, non None).
    assert mh805_demo_calcoli()["breakeven_gas_eur_mwh"] == pytest.approx(7.254340892102108)
    assert mh805_breakeven_gas(6510.0, 4200.0, 176.01111111111126,
                               250, 2600,
                               8680.0, 5918.181818181818, 1500,
                               63291.66666666667, 5088.86274509804,
                               44676.470588235294) == pytest.approx(7.254340892102108)
    # Variante senza recupero: be 20,60.
    bc = _variante(f_rec=0)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(20.604726819224727)
    # Variante 700 porzioni: numeratore negativo -> None.
    assert _variante(porzioni_giorno=700)["breakeven_gas_eur_mwh"] is None
    # Denominatore gas nullo (stesso rendimento, niente ACS) -> None.
    assert mh805_breakeven_gas(6510.0, 4200.0, 176.01111111111126,
                               250, 2600,
                               8680.0, 5918.181818181818, 1500,
                               63291.66666666667, 0,
                               63291.66666666667) is None
    with pytest.raises(ValueError):
        mh805_breakeven_gas(6510.0, 4200.0, 176.01, 250, 2600,
                            8680.0, 5918.18, 1500,
                            63291.67, 5088.86, -1)


def test_breakeven_verifica_pareggio():
    be = _variante(f_rec=0)["breakeven_gas_eur_mwh"]
    assert be == pytest.approx(20.604726819224727)
    bc = _variante(f_rec=0, p_gas=be)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    demo = mh805_demo_calcoli()
    assert demo["breakeven_gas_eur_mwh"] == pytest.approx(7.254340892102108)
    assert (demo["gas_cucina_base_kwh_anno"]
            + demo["gas_acs_base_kwh_anno"]
            - demo["gas_cucina_alt_kwh_anno"]) > 0.0


def test_breakeven_soglia_minima():
    bc_alto = _variante(f_rec=0, p_gas=21.604726819224727)
    bc_basso = _variante(f_rec=0, p_gas=19.0)
    assert bc_alto["c_alt_eur_anno"] < bc_alto["c_base_eur_anno"]
    assert bc_basso["c_alt_eur_anno"] > bc_basso["c_base_eur_anno"]
    assert bc_alto["verdetto"] == "NON_CONVIENTE"
    assert bc_basso["verdetto"] == "NON_CALCOLABILE"


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh805_flussi(22000, 1961.4079708853242, 15)
    assert len(fl) == 16
    assert fl[0] == -22000
    assert all(f == 1961.4079708853242 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh805_demo_calcoli()
    assert bc["van"] == pytest.approx(-1641.2559888486612)
    assert mh805_van([-22000] + [1961.4079708853242] * 15,
                     0) == pytest.approx(7421.119563279863)
    assert mh805_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh805_demo_calcoli()
    assert bc["tir"] == pytest.approx(3.874706593609684)
    assert mh805_tir([-22000] + [1961.4079708853242] * 15) == \
        pytest.approx(0.03874706593609684)
    tir = mh805_tir([-22000] + [1961.4079708853242] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-22000] + [1961.4079708853242] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh805_payback([-22000] + [1961.4079708853242] * 15) == 12
    assert mh805_payback([-22000] + [-1000.0] * 15) is None
    assert mh805_payback([0] + [1961.4079708853242] * 15) == 0
    assert mh805_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh805_verdetto(1961.4079708853242, -1641.2559888486612, 22000,
                          10.0) == "MARGINALE"
    assert mh805_verdetto(1961.4079708853242, 0.0, 22000, 10.0) == "MARGINALE"
    assert mh805_verdetto(1961.4079708853242, -2200.0, 22000, 10.0) == "MARGINALE"
    assert mh805_verdetto(1961.4079708853242, -2200.01, 22000, 10.0) == "NON_CONVIENTE"
    assert mh805_verdetto(1961.4079708853242, 358.74, 22000, 10.0) == "CONVIENTE"
    assert mh805_verdetto(0.0, 358.74, 22000,
                          10.0) == "NON_CALCOLABILE"
    assert mh805_verdetto(-1002.46, -32405.23, 22000,
                          10.0) == "NON_CALCOLABILE"
    assert mh805_verdetto(None, 358.74, 22000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh805_verdetto(float("nan"), 358.74, 22000, 10.0)
    with pytest.raises(ValueError):
        mh805_verdetto(1961.4079708853242, 358.74, -1, 10.0)
    with pytest.raises(ValueError):
        mh805_verdetto(1961.4079708853242, 358.74, 22000, 100.1)


def test_valida_demo_ok():
    v = mh805_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("porzioni_giorno", "350"),
                       ("porzioni_giorno", float("nan")),
                       ("porzioni_giorno", float("inf")),
                       ("porzioni_giorno", True),
                       ("p_gas", None),
                       ("q_celle_per_porzione", "0.12")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh805_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("porzioni_giorno", -10),
                          ("giorni_anno", 0),
                          ("giorni_anno", 2.5),
                          ("q_cottura_per_porzione", -0.1),
                          ("eta_cucina_base", 0),
                          ("eta_cucina_base", 1.01),
                          ("eta_cucina_alt", 0),
                          ("eta_cucina_alt", 1.01),
                          ("q_banchi_per_porzione", -0.1),
                          ("fattore_banchi_alt", 0),
                          ("fattore_banchi_alt", 1.01),
                          ("q_celle_per_porzione", -0.1),
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
        assert mh805_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"porzioni_giorno": 0,
              "q_cottura_per_porzione": 0,
              "q_banchi_per_porzione": 0,
              "q_celle_per_porzione": 0,
              "litri_acs_giorno": 0,
              "f_rec": 0,
              "p_gas": 0,
              "p_el": 0,
              "om_base": 0, "om_alt": 0,
              "capex": 0, "wacc_pct": 0,
              "f_gas": 0, "f_el": 0,
              "tolleranza_pct": 0})
    assert mh805_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["f_rec"] = 1.0
    d["porzioni_giorno"] = 350
    assert mh805_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh805_demo()
    assert d["porzioni_giorno"] == 350
    assert d["giorni_anno"] == 310
    assert d["q_cottura_per_porzione"] == 0.35
    assert d["eta_cucina_base"] == 0.60
    assert d["eta_cucina_alt"] == 0.85
    assert d["q_banchi_per_porzione"] == 0.08
    assert d["fattore_banchi_alt"] == 0.75
    assert d["q_celle_per_porzione"] == 0.12
    assert d["cop_freddo_base"] == 2.2
    assert d["cop_freddo_alt"] == 3.1
    assert d["litri_acs_giorno"] == 300
    assert d["delta_t_acs"] == 40
    assert d["f_rec"] == 0.10
    assert d["eta_caldaia_base"] == 0.85
    assert d["cop_pdc_acs"] == 3.0
    assert d["p_gas"] == 90
    assert d["p_el"] == 250
    assert d["om_base"] == 1500
    assert d["om_alt"] == 2600
    assert d["capex"] == 22000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["f_gas"] == 0.20
    assert d["f_el"] == 0.35
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    bc = mh805_demo_calcoli()
    for chiave, atteso in _DEMO.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert got == pytest.approx(atteso, rel=1e-9), chiave
    assert bc["payback"] == 12
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(7.254340892102108)
    assert bc["verdetto"] == "MARGINALE"
    assert bc["valid"] is True
    assert demo_calcoli()["van"] == bc["van"]


def test_demo_calcoli_fisica_economia():
    bc = mh805_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(11303.793101604278)
    assert bc["c_alt_eur_anno"] == pytest.approx(9342.385130718954)
    assert bc["risparmio_eur_anno"] == pytest.approx(1961.4079708853242)
    assert bc["co2_base_t_anno"] == pytest.approx(18.785469518716578)
    assert bc["co2_alt_t_anno"] == pytest.approx(12.745398006535947)
    assert bc["co2_evitata_t_anno"] == pytest.approx(6.040071512180631)
    assert bc["porzioni_anno"] == pytest.approx(108500.0)
    assert bc["q_cottura_kwh_anno"] == pytest.approx(37975.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(3797.5)
    assert bc["q_acs_net_kwh_anno"] == pytest.approx(528.0333333333338)


def test_demo_flussi_e_cumulato():
    bc = mh805_demo_calcoli()
    assert bc["flussi"][0] == -22000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(1961.4079708853242) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -22000
    assert righe.iloc[11]["Cumulato (EUR)"] == pytest.approx(-424.51232026143407)
    assert righe.iloc[12]["Cumulato (EUR)"] == pytest.approx(1536.89565062389)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(7421.119563279863)


def test_demo_tabella_righe():
    bc = mh805_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Porzioni all'anno"] == pytest.approx(108500.0)
    assert mappa["Calore di cottura (kWh_th/anno)"] == pytest.approx(37975.0)
    assert mappa["Gas cucina base (kWh/anno)"] == pytest.approx(63291.66666666667)
    assert mappa["Gas cucina alt (kWh/anno)"] == pytest.approx(44676.470588235294)
    assert mappa["Elettricita' banchi caldi base (kWh_e/anno)"] == pytest.approx(8680.0)
    assert mappa["Elettricita' banchi caldi alt (kWh_e/anno)"] == pytest.approx(6510.0)
    assert mappa["Carico celle (kWh_c/anno)"] == pytest.approx(13020.0)
    assert mappa["Elettricita' freddo base (kWh_e/anno)"] == pytest.approx(5918.181818181818)
    assert mappa["Elettricita' freddo alt (kWh_e/anno)"] == pytest.approx(4200.0)
    assert mappa["ACS di lavaggio (kWh_th/anno)"] == pytest.approx(4325.533333333334)
    assert mappa["Calore cucina recuperato (kWh_th/anno)"] == pytest.approx(3797.5)
    assert mappa["ACS netta (kWh_th/anno)"] == pytest.approx(528.0333333333338)
    assert mappa["Gas ACS baseline (kWh/anno)"] == pytest.approx(5088.86274509804)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(11303.793101604278)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(9342.385130718954)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(1961.4079708853242)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(6.040071512180631)
    assert mappa["Payback (anni)"] == 12
    assert mappa["Verdetto"] == "MARGINALE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] == pytest.approx(7.254340892102108)


def test_demo_coerenza_interna():
    bc = mh805_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["porzioni_anno"] == pytest.approx(
        bc["porzioni_giorno"] * bc["giorni_anno"])
    assert bc["q_cottura_kwh_anno"] == pytest.approx(
        bc["porzioni_anno"] * bc["q_cottura_per_porzione"])
    assert bc["gas_cucina_base_kwh_anno"] == pytest.approx(
        bc["q_cottura_kwh_anno"] / bc["eta_cucina_base"])
    assert bc["gas_cucina_alt_kwh_anno"] == pytest.approx(
        bc["q_cottura_kwh_anno"] / bc["eta_cucina_alt"])
    assert bc["e_banchi_base_kwh_anno"] == pytest.approx(
        bc["porzioni_anno"] * bc["q_banchi_per_porzione"] * 1.0)
    assert bc["e_banchi_alt_kwh_anno"] == pytest.approx(
        bc["porzioni_anno"] * bc["q_banchi_per_porzione"]
        * bc["fattore_banchi_alt"])
    assert bc["q_celle_kwh_anno"] == pytest.approx(
        bc["porzioni_anno"] * bc["q_celle_per_porzione"])
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
        (bc["gas_cucina_base_kwh_anno"]
         + bc["gas_acs_base_kwh_anno"]) / 1000.0 * bc["p_gas"]
        + (bc["e_banchi_base_kwh_anno"]
           + bc["e_freddo_base_kwh_anno"]) / 1000.0 * bc["p_el"]
        + bc["om_base"])
    assert bc["c_alt_eur_anno"] == pytest.approx(
        bc["gas_cucina_alt_kwh_anno"] / 1000.0 * bc["p_gas"]
        + (bc["e_banchi_alt_kwh_anno"]
           + bc["e_freddo_alt_kwh_anno"]
           + bc["e_pdc_acs_kwh_anno"])
        / 1000.0 * bc["p_el"]
        + bc["om_alt"])


def test_demo_contro_riconteggio_indipendente():
    porz, gg, qc = 350, 310, 0.35
    egb, ega = 0.60, 0.85
    qb, fba, qcel = 0.08, 0.75, 0.12
    cfb, cfa = 2.2, 3.1
    lit, dt, frec = 300, 40, 0.10
    eta, copp = 0.85, 3.0
    pg, pel = 90, 250
    omb, oma, cx = 1500, 2600, 22000
    fg, fel, wacc, vita = 0.20, 0.35, 5.0, 15
    pa = porz * gg
    qcott = pa * qc
    ggb = qcott / egb
    gga = qcott / ega
    ebb = pa * qb * 1.0
    eba = pa * qb * fba
    qce = pa * qcel
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
    bc = mh805_demo_calcoli()
    assert bc["porzioni_anno"] == pytest.approx(pa)
    assert bc["q_cottura_kwh_anno"] == pytest.approx(qcott)
    assert bc["gas_cucina_base_kwh_anno"] == pytest.approx(ggb)
    assert bc["gas_cucina_alt_kwh_anno"] == pytest.approx(gga)
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
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(7.254340892102108)


# ---------------------------------------------------------------- varianti
def test_variante_gas_zero_helper_calcola_ma_ui_guard():
    # Negli helper p_gas = 0 e' ammesso (non negativo)
    # ma qui, a differenza della scheda precedente,
    # il risparmio va in negativo (-171,96 EUR/anno):
    # verdetto NON_CALCOLABILE anche negli helper.
    # La UI ha comunque la guard piu' stretta
    # (prezzi <= 0 -> NON_CALCOLABILE): vedi
    # test_ui_guard_degenere_stretta.
    bc = _variante(p_gas=0)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(-171.9573232323237)
    assert bc["van"] == pytest.approx(-23784.858212312407)
    assert bc["payback"] is None
    assert bc["tir"] is None
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(7.254340892102108)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_gas_alto_conviente():
    bc = _variante(p_gas=150)
    assert bc["risparmio_eur_anno"] == pytest.approx(3383.651500297088)
    assert bc["van"] == pytest.approx(13121.145493460483)
    assert bc["tir"] == pytest.approx(12.88234971774881)
    assert bc["payback"] == 7
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_senza_recupero_non_conviente():
    bc = _variante(f_rec=0)
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["q_acs_net_kwh_anno"] == pytest.approx(4325.533333333334)
    assert bc["e_pdc_acs_kwh_anno"] == pytest.approx(1441.8444444444447)
    assert bc["risparmio_eur_anno"] == pytest.approx(1644.9496375519902)
    assert bc["van"] == pytest.approx(-4925.985272181232)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(20.604726819224727)
    assert bc["payback"] == 14
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_recupero_parziale_senza_saturazione():
    bc = _variante(f_rec=0.05)
    assert bc["q_rec_kwh_anno"] == pytest.approx(1898.75)
    assert bc["q_acs_net_kwh_anno"] == pytest.approx(2426.7833333333338)
    assert bc["e_pdc_acs_kwh_anno"] == pytest.approx(808.9277777777779)
    assert bc["risparmio_eur_anno"] == pytest.approx(1803.1788042186563)
    assert bc["van"] == pytest.approx(-3283.6206305149562)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(13.929533855663419)
    assert bc["payback"] == 13
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_recupero_pieno_satura():
    bc = _variante(f_rec=1.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(4325.533333333334)
    assert bc["q_acs_net_kwh_anno"] == 0.0
    assert bc["e_pdc_acs_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(2005.410748663102)
    assert bc["van"] == pytest.approx(-1184.5222027852824)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(5.398001515568872)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"


def test_variante_acs_doppia_marginale():
    bc = _variante(litri_acs_giorno=600)
    assert bc["q_acs_kwh_anno"] == pytest.approx(8651.066666666668)
    assert bc["q_rec_kwh_anno"] == pytest.approx(3797.5)
    assert bc["q_acs_net_kwh_anno"] == pytest.approx(4853.5666666666675)
    assert bc["risparmio_eur_anno"] == pytest.approx(2058.944506833037)
    assert bc["van"] == pytest.approx(-628.8600994826932)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(18.49129596225323)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"


def test_variante_acs_zero():
    bc = _variante(litri_acs_giorno=0)
    assert bc["q_acs_kwh_anno"] == 0.0
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["gas_acs_base_kwh_anno"] == 0.0
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(6.8736609013106715)
    assert bc["risparmio_eur_anno"] == pytest.approx(1547.4131016042775)
    assert bc["van"] == pytest.approx(-5938.381161547203)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_porzioni_piccole_e_grandi():
    bc = _variante(porzioni_giorno=175)
    assert bc["porzioni_anno"] == pytest.approx(54250.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(479.47225341651847)
    assert bc["van"] == pytest.approx(-17023.241970740677)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(56.695130101771454)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"
    bc2 = _variante(porzioni_giorno=700)
    assert bc2["risparmio_eur_anno"] == pytest.approx(4652.823850267381)
    assert bc2["van"] == pytest.approx(26294.72047766619)
    assert bc2["breakeven_gas_eur_mwh"] is None
    assert bc2["payback"] == 5
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_capex_conviente():
    bc = _variante(capex=20000)
    assert bc["risparmio_eur_anno"] == pytest.approx(1961.4079708853242)
    assert bc["van"] == pytest.approx(358.74401115133924)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(capex=18000)
    assert bc2["van"] == pytest.approx(2358.744011151336)
    assert bc2["payback"] == 10
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex=0)
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(20358.744011151335, rel=1e-6)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(7421.119563279863)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(-6854.527560833285)
    assert bc2["payback"] is None
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_el_alto_e_om_alt_alto():
    bc = _variante(p_el=400)
    assert bc["risparmio_eur_anno"] == pytest.approx(2518.2335769459296)
    assert bc["van"] == pytest.approx(4138.403388963077)
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["payback"] == 9
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(om_alt=3600)
    assert bc2["risparmio_eur_anno"] == pytest.approx(961.4079708853242)
    assert bc2["breakeven_gas_eur_mwh"] == pytest.approx(49.4412088645764)
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_senza_celle_e_senza_banchi():
    bc = _variante(q_celle_per_porzione=0)
    assert bc["q_celle_kwh_anno"] == 0.0
    assert bc["e_freddo_base_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(1531.8625163398701)
    assert bc["van"] == pytest.approx(-6099.790918885322)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(25.375518271187655)
    assert bc["payback"] == 15
    assert bc["verdetto"] == "NON_CONVIENTE"
    bc2 = _variante(q_banchi_per_porzione=0)
    assert bc2["e_banchi_base_kwh_anno"] == 0.0
    assert bc2["e_banchi_alt_kwh_anno"] == 0.0
    assert bc2["risparmio_eur_anno"] == pytest.approx(1418.9079708853242)
    assert bc2["van"] == pytest.approx(-7272.220474561628)
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_senza_porzioni_non_calcolabile():
    bc = _variante(porzioni_giorno=0)
    assert bc["porzioni_anno"] == 0.0
    assert bc["q_cottura_kwh_anno"] == 0.0
    assert bc["e_banchi_base_kwh_anno"] == 0.0
    assert bc["q_celle_kwh_anno"] == 0.0
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(286.9916490708917)
    assert bc["risparmio_eur_anno"] == pytest.approx(-1002.4634640522877)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_cucina_alt_uguale_base():
    bc = _variante(eta_cucina_alt=0.60)
    assert bc["gas_cucina_alt_kwh_anno"] == pytest.approx(63291.66666666667)
    assert bc["risparmio_eur_anno"] == pytest.approx(286.04032382650075)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(33.79091397148899)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_monotonia_prezzo_gas_crescente():
    base = mh805_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas=91)["risparmio_eur_anno"]
    basso = _variante(p_gas=89)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(23.70405882352952, abs=1e-2)
    assert base - basso == pytest.approx(23.70405882352952, abs=1e-2)


def test_monotonia_porzioni_crescente():
    assert _variante(porzioni_giorno=175)["risparmio_eur_anno"] < \
        mh805_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(porzioni_giorno=700)["risparmio_eur_anno"] > \
        mh805_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(porzioni_giorno=700)["porzioni_anno"] == \
        pytest.approx(217000.0)


def test_demo_deterministica_due_chiamate():
    a = mh805_demo_calcoli()
    b = mh805_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh805_demo().keys()) == {
        "porzioni_giorno", "giorni_anno",
        "q_cottura_per_porzione",
        "eta_cucina_base", "eta_cucina_alt",
        "q_banchi_per_porzione", "fattore_banchi_alt",
        "q_celle_per_porzione",
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
    for kw in ({"porzioni_giorno": -10},
               {"giorni_anno": 0},
               {"giorni_anno": 2.5},
               {"q_cottura_per_porzione": -0.1},
               {"eta_cucina_base": 0}, {"eta_cucina_base": 1.01},
               {"eta_cucina_alt": 0}, {"eta_cucina_alt": 1.01},
               {"q_banchi_per_porzione": -0.1},
               {"fattore_banchi_alt": 0}, {"fattore_banchi_alt": 1.01},
               {"q_celle_per_porzione": -0.1},
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
        assert mh805_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"porzioni_giorno": "350"},
               {"porzioni_giorno": float("nan")},
               {"p_gas": float("inf")},
               {"capex": True},
               {"q_celle_per_porzione": "0.12"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh805_valida(**d)["valido"] is False


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    for kw in ({"porzioni_giorno": 0},
               {"p_gas": 0},
               {"om_alt": 6000}):
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
    assert bc2["risparmio_eur_anno"] == pytest.approx(23.70405882352952, abs=1e-2)
    assert bc2["van"] == pytest.approx(-21753.959975294845, abs=1e-2)
    assert bc2["verdetto"] == "NON_CONVIENTE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh805_demo_calcoli()
    testo = mh805_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;MARGINALE" in testo
    assert "breakeven_gas_eur_mwh" in testo
    assert "co2_evitata_t_anno" in testo
    assert "q_cottura_kwh_anno" in testo
    assert "porzioni_giorno" in testo
    assert "e_freddo_alt_kwh_anno" in testo
    assert "e_banchi_alt_kwh_anno" in testo
    assert "q_rec_kwh_anno" in testo
    assert "q_acs_net_kwh_anno" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh805_demo_calcoli()
    testo = mh805_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"porzioni_anno;{bc['porzioni_anno']}" in testo
    assert f"gas_acs_base_kwh_anno;{bc['gas_acs_base_kwh_anno']}" in testo
    assert f"q_celle_kwh_anno;{bc['q_celle_kwh_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh805_demo_calcoli()
    testo = mh805_csv(bc, _demo_kwargs())
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
    return ["mh" + "80" + "4", "st" + "80" + "4",
            "tab" + "80" + "4", "w" + "80" + "5",
            "mh" + "80" + "3", "tab" + "80" + "3"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w806_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w806_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab805:")


def test_ui_apre_scheda_attesa_una_volta():
    """Il frammento UI apre la scheda attesa, una sola volta."""
    src = _leggi("w806_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert m.group(1) == "805"
    assert src.count("with tab805:") == 1


def test_ui_titolo_atteso():
    src = _leggi("w806_ui.py")
    titolo = ("Tavola calda: forno combinato efficiente + banchi "
              "caldi efficienti + celle efficienti + recupero "
              "calore cucina su ACS batte cucina a gas vecchia + "
              "banchi e celle tradizionali + caldaia a gas?")
    assert src.count(titolo) == 2


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w806_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w806_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st805_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) >= 28
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w806_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 4
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_ui_guard_degenere_stretta():
    """La guard UI della scheda dichiara NON_CALCOLABILE
    anche per porzioni <= 0, prezzi <= 0 e CAPEX <= 0 (piu'
    stretta degli helper, che ammettono lo zero)."""
    src = _leggi("w806_ui.py")
    assert "float(_porz805) <= 0.0" in src
    assert "float(_pg805) <= 0.0" in src
    assert "float(_pel805) <= 0.0" in src
    assert "float(_cx805) <= 0.0" in src
    assert "int(_vita805) <= 0" in src
    assert "Verdetto: NON_CALCOLABILE" in src


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w806_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def805[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w806_ui.py")
        usate = set(re.findall(r'_def805\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 25
        assert usate <= set(mh805_demo().keys())
