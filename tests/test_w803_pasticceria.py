"""Test nuova scheda "Pasticceria: forno a gas
efficiente + recupero calore forno su ACS +
freddo efficiente batte forno a gas vecchio +
celle tradizionali + caldaia a gas?"
(titolo completo nel frammento UI).
Contenuto pronto da scrivere in repo come test
della scheda pasticceria.

Business case deterministico di una pasticceria
guidato dai KG DI DOLCI PRODOTTI AL GIORNO e
dai GIORNI DI APERTURA ALL'ANNO: i dolci
guidano il calore di cottura del forno (kWh_th
per kg di dolci), il freddo dell'abbattitore
(raffreddamento dei dolci caldi da T_in a
T_out) e il carico frigorifero delle celle
(kWh_c per kg di dolci); i litri di ACS al
giorno guidano il lavaggio di teglie e
attrezzature. Dolci annui = kg al giorno x
giorni; calore di cottura = dolci annui x
kWh_th per kg; gas forno base e alt =
Q_cottura / eta (stesso calore utile,
rendimento diverso); freddo abbattitore =
kg annui x cp x (T_in - T_out) / 3600
kWh_c/anno (cp in kJ/kg/K; serve T_in > T_out
>= 0); carico celle = dolci annui x kWh_c per
kg; freddo totale = abbattitore + celle;
elettricita' freddo base e alt = Q_freddo /
COP (stesso carico, COP diverso); ACS = litri
x giorni x 4,186 x delta_T / 3600; recupero =
min(ACS, Q_cottura x f_rec) (saturato
all'ACS); ACS netta = max(0, ACS - recupero);
gas ACS baseline = ACS / eta_caldaia (senza
recupero); elettricita' PdC ACS = ACS netta /
COP_pdc_acs; C_base = (gas_forno_base +
gas_acs_base) / 1000 x p_gas + E_freddo_base
/ 1000 x p_el + O&M_base; C_alt =
gas_forno_alt / 1000 x p_gas + (E_freddo_alt
+ E_pdc_acs) / 1000 x p_el + O&M_alt;
risparmio = C_base - C_alt; CO2_base =
(gas_forno_base + gas_acs_base) / 1000 x f_gas
+ E_freddo_base / 1000 x f_el; CO2_alt =
gas_forno_alt / 1000 x f_gas + (E_freddo_alt
+ E_pdc_acs) / 1000 x f_el; CO2_evitata =
CO2_base - CO2_alt; flussi [-CAPEX, risparmio
x vita]; VAN, TIR, payback (primo anno con
cumulato >= 0); breakeven gas =
((E_freddo_alt + E_pdc_acs) / 1000 x p_el +
O&M_alt - E_freddo_base / 1000 x p_el -
O&M_base) / ((gas_forno_base + gas_acs_base -
gas_forno_alt) / 1000) EUR/MWh, None se
denominatore gas <= 0 o numeratore < 0,
SOGLIA MINIMA quando esiste.
Verdetto: NON_CALCOLABILE se risparmio <= 0
(guard degenere: UI salta KPI, grafico, tabella
e CSV); altrimenti CONVIENTE se VAN > 0,
MARGINALE se VAN negativa entro tolleranza %
del CAPEX, NON_CONVIENTE se VAN negativa oltre
la tolleranza. Distinzione esplicita: distinto
dal panificio (kg di pane per la cottura del
pane, senza abbattitore e senza dolci: qui i
dolci passano dall'abbattitore da T_in a T_out
e il recupero va sull'ACS di lavaggio di teglie),
dalla gelateria (litri di gelato,
pastorizzazione, freddo del gelato: qui nessuna
pastorizzazione, nessun gelato, il freddo e'
quello dell'abbattitore dei dolci piu' le celle
dei dolci), dalla pescheria (kg di pesce,
macchina del ghiaccio in scaglie, recupero dai
condensatori: qui nessun pesce, nessun ghiaccio,
il recupero viene dal calore del forno), dal
fioraio (superficie negozio per riscaldamento
piu' cella fiori, recupero sul riscaldamento:
qui niente riscaldamento, recupero sull'ACS di
lavaggio), dal parrucchiere (lavaggi di capelli,
ACS, recupero dalle acque reflue), dal
ristorante (coperti, ACS di cucina, celle frigo
di cucina), dalla farmacia (superficie di
vendita piu' frigoriferi farmaceutici, recupero
dai frigoriferi, nessun forno), dall'albergo
(pernottamento, ACS docce ospiti), dalla
palestra (docce utenti, recupero dalle acque
delle docce), dall'autolavaggio (veicoli lavati,
acque di lavaggio dei veicoli) e dal
palaghiaccio (pista da pattinaggio, freddo di
pista verso spogliatoi): qui driver DOLCI +
GIORNI + TEMPERATURE + ACS = kg di dolci al
giorno per cottura e freddo, giorni di apertura
per l'anno, temperature di abbattimento per il
freddo, litri di ACS per il lavaggio; niente
pane, niente gelato, niente pesce, niente
lavaggi, niente coperti, niente docce, niente
veicoli, niente frigoriferi farmaceutici,
niente pista.

Demo (pasticceria): 400 kg di dolci al giorno
per 300 giorni di apertura all'anno (120.000 kg
all'anno), calore di cottura 0,60 kWh_th per kg
di dolci (72.000 kWh_th/anno), forno base 0,75
e alt 0,92, calore specifico dolci 3,0 kJ/kg/K,
abbattimento da 85 C a 3 C, carico celle 0,20
kWh_c per kg di dolci, COP freddo base 2,2 e
alt 3,2, ACS di lavaggio 400 litri al giorno
con delta_T 40 K, f_rec 0,05, caldaia 0,90,
COP PdC ACS 3,2, gas 90, el 250 EUR/MWh, O&M
base 1.500, alt 2.500, CAPEX 20.000, WACC 5 %,
vita 15, f_gas 0,20, f_el 0,35, tolleranza 10 %
del CAPEX. Valori calcolati eseguendo
mh803_demo_calcoli(): dolci annui 120.000,
Q_cottura 72.000, gas_forno_base 96.000,
gas_forno_alt 78.260,86956521739,
Q_abbattitore 8.200, Q_celle 24.000,
Q_freddo 32.200, E_freddo_base
14.636,363636363636, E_freddo_alt 10.062,5,
Q_acs 5.581,333333333333, Q_rec 3.600,
Q_acs_net 1.981,333333333333, gas_acs_base
6.201,481481481481, E_pdc_acs
619,1666666666665, C_base 14.357,224242424243,
C_alt 12.213,894927536232, risparmio
2.143,329314888011, CO2_base
25,563023569023567, CO2_alt 19,39075724637681,
CO2_evitata 6,172266322646756, VAN
2.247,025351745442, TIR 6,6188810791093395 %,
payback 10, breakeven gas
0,47307719683066607 EUR/MWh (soglia minima),
verdetto CONVIENTE.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w804_helpers import (
    demo_calcoli,
    mh803_breakeven_gas,
    mh803_c_alt,
    mh803_c_base,
    mh803_calcola,
    mh803_co2_alt,
    mh803_co2_base,
    mh803_co2_evitata,
    mh803_cop,
    mh803_csv,
    mh803_demo,
    mh803_demo_calcoli,
    mh803_e_freddo,
    mh803_e_pdc_acs,
    mh803_eta,
    mh803_flussi,
    mh803_frazione,
    mh803_gas_acs,
    mh803_gas_forno,
    mh803_int_pos,
    mh803_kg_dolci_anno,
    mh803_num,
    mh803_nneg,
    mh803_payback,
    mh803_pct_tolleranza,
    mh803_pct_wacc,
    mh803_pos,
    mh803_q_abbattitore,
    mh803_q_acs,
    mh803_q_acs_net,
    mh803_q_celle,
    mh803_q_cottura,
    mh803_q_freddo,
    mh803_q_rec,
    mh803_risparmio,
    mh803_tir,
    mh803_valida,
    mh803_van,
    mh803_verdetto,
)

_DEMO = {
    "kg_dolci_anno": 120000.0,
    "q_cottura_kwh_anno": 72000.0,
    "gas_forno_base_kwh_anno": 96000.0,
    "gas_forno_alt_kwh_anno": 78260.86956521739,
    "q_abbattitore_kwh_anno": 8200.0,
    "q_celle_kwh_anno": 24000.0,
    "q_freddo_kwh_anno": 32200.0,
    "e_freddo_base_kwh_anno": 14636.363636363636,
    "e_freddo_alt_kwh_anno": 10062.5,
    "q_acs_kwh_anno": 5581.333333333333,
    "q_rec_kwh_anno": 3600.0,
    "q_acs_net_kwh_anno": 1981.333333333333,
    "gas_acs_base_kwh_anno": 6201.481481481481,
    "e_pdc_acs_kwh_anno": 619.1666666666665,
    "c_base_eur_anno": 14357.224242424243,
    "c_alt_eur_anno": 12213.894927536232,
    "risparmio_eur_anno": 2143.329314888011,
    "co2_base_t_anno": 25.563023569023567,
    "co2_alt_t_anno": 19.39075724637681,
    "co2_evitata_t_anno": 6.172266322646756,
    "van": 2247.025351745442,
    "tir": 6.6188810791093395,
}


def _demo_kwargs():
    return dict(mh803_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh803_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh803_num(3, "x") == 3.0
    assert mh803_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh803_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh803_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh803_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh803_pos(0, "x")
    with pytest.raises(ValueError):
        mh803_pos(-1, "x")
    assert mh803_pos(0.5, "x") == 0.5


def test_cop_maggiore_di_uno():
    assert mh803_cop(3.2, "x") == 3.2
    assert mh803_cop(1.01, "x") == 1.01
    with pytest.raises(ValueError):
        mh803_cop(1.0, "x")
    with pytest.raises(ValueError):
        mh803_cop(0.5, "x")
    with pytest.raises(ValueError):
        mh803_cop(0, "x")


def test_frazione_limiti():
    assert mh803_frazione(0, "x") == 0.0
    assert mh803_frazione(1, "x") == 1.0
    assert mh803_frazione(0.05, "x") == 0.05
    with pytest.raises(ValueError):
        mh803_frazione(-0.01, "x")
    with pytest.raises(ValueError):
        mh803_frazione(1.01, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh803_int_pos(5.0, "x") == 5
    assert mh803_int_pos(300.0, "x") == 300
    with pytest.raises(ValueError):
        mh803_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh803_int_pos(0, "x")


def test_eta_limiti():
    assert mh803_eta(1.0, "x") == 1.0
    assert mh803_eta(0.9, "x") == 0.9
    with pytest.raises(ValueError):
        mh803_eta(0, "x")
    with pytest.raises(ValueError):
        mh803_eta(1.01, "x")


def test_pct_wacc_limiti():
    assert mh803_pct_wacc(0, "x") == 0.0
    assert mh803_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh803_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh803_pct_tolleranza(0, "x") == 0.0
    assert mh803_pct_tolleranza(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh803_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh803_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_kg_dolci_anno_e_q_cottura():
    assert mh803_kg_dolci_anno(400, 300) == 120000.0
    assert mh803_kg_dolci_anno(0, 300) == 0.0
    assert mh803_kg_dolci_anno(200, 300) == 60000.0
    assert mh803_q_cottura(120000, 0.60) == 72000.0
    assert mh803_q_cottura(120000, 0) == 0.0
    assert mh803_q_cottura(60000, 0.60) == 36000.0
    with pytest.raises(ValueError):
        mh803_kg_dolci_anno(-1, 300)
    with pytest.raises(ValueError):
        mh803_kg_dolci_anno(400, 0)
    with pytest.raises(ValueError):
        mh803_kg_dolci_anno(400, 2.5)
    with pytest.raises(ValueError):
        mh803_q_cottura(120000, -0.1)


def test_gas_forno_rendimenti():
    assert mh803_gas_forno(72000.0, 0.75) == 96000.0
    assert mh803_gas_forno(72000.0, 0.92) == pytest.approx(78260.86956521739)
    assert mh803_gas_forno(72000.0, 1.0) == 72000.0
    assert mh803_gas_forno(0, 0.75) == 0.0
    with pytest.raises(ValueError):
        mh803_gas_forno(72000.0, 0)
    with pytest.raises(ValueError):
        mh803_gas_forno(72000.0, 1.01)


def test_q_abbattitore_formula_e_vincolo_temperature():
    assert mh803_q_abbattitore(120000, 3.0, 85, 3) == pytest.approx(8200.0)
    assert mh803_q_abbattitore(0, 3.0, 85, 3) == 0.0
    assert mh803_q_abbattitore(120000, 2.0, 85, 3) == pytest.approx(5466.666666666667)
    assert mh803_q_abbattitore(120000, 3.0, 60, 3) == pytest.approx(5700.0)
    assert mh803_q_abbattitore(120000, 3.0, 85, 0) == pytest.approx(8500.0)
    with pytest.raises(ValueError):
        mh803_q_abbattitore(120000, 3.0, 3, 3)
    with pytest.raises(ValueError):
        mh803_q_abbattitore(120000, 3.0, 3, 85)
    with pytest.raises(ValueError):
        mh803_q_abbattitore(120000, 3.0, 85, -1)
    with pytest.raises(ValueError):
        mh803_q_abbattitore(120000, 0, 85, 3)
    with pytest.raises(ValueError):
        mh803_q_abbattitore(-1, 3.0, 85, 3)


def test_q_celle_q_freddo_e_freddo():
    assert mh803_q_celle(120000, 0.20) == 24000.0
    assert mh803_q_celle(0, 0.20) == 0.0
    assert mh803_q_celle(120000, 0) == 0.0
    assert mh803_q_freddo(8200.0, 24000.0) == 32200.0
    assert mh803_q_freddo(0, 0) == 0.0
    assert mh803_e_freddo(32200.0, 2.2) == pytest.approx(14636.363636363636)
    assert mh803_e_freddo(32200.0, 3.2) == pytest.approx(10062.5)
    assert mh803_e_freddo(0, 2.2) == 0.0
    with pytest.raises(ValueError):
        mh803_q_celle(120000, -0.1)
    with pytest.raises(ValueError):
        mh803_e_freddo(32200.0, 1.0)
    with pytest.raises(ValueError):
        mh803_q_freddo(-1, 24000.0)


def test_q_acs_formula():
    assert mh803_q_acs(400, 300, 40) == pytest.approx(5581.333333333333)
    assert mh803_q_acs(0, 300, 40) == 0.0
    assert mh803_q_acs(100, 300, 40) == pytest.approx(1395.3333333333333)
    assert mh803_q_acs(400, 300, 20) == pytest.approx(2790.6666666666665)
    with pytest.raises(ValueError):
        mh803_q_acs(-1, 300, 40)
    with pytest.raises(ValueError):
        mh803_q_acs(400, 0, 40)
    with pytest.raises(ValueError):
        mh803_q_acs(400, 300, 0)
    with pytest.raises(ValueError):
        mh803_q_acs(400, 2.5, 40)


def test_q_rec_saturazione_e_acs_netta():
    assert mh803_q_rec(72000.0, 0.05, 5581.333333333333) == pytest.approx(3600.0)
    assert mh803_q_rec(72000.0, 0, 5581.333333333333) == 0.0
    assert mh803_q_rec(72000.0, 1.0, 5581.333333333333) == 5581.333333333333
    assert mh803_q_rec(72000.0, 0.05, 1395.3333333333333) == 1395.3333333333333
    assert mh803_q_rec(72000.0, 1.0, 1395.3333333333333) == 1395.3333333333333
    with pytest.raises(ValueError):
        mh803_q_rec(72000.0, 1.01, 5581.333333333333)
    with pytest.raises(ValueError):
        mh803_q_rec(72000.0, -0.1, 5581.333333333333)
    assert mh803_q_acs_net(5581.333333333333, 3600.0) == pytest.approx(1981.333333333333)
    assert mh803_q_acs_net(1395.3333333333333, 1395.3333333333333) == 0.0
    assert mh803_q_acs_net(5581.333333333333, 0.0) == 5581.333333333333
    with pytest.raises(ValueError):
        mh803_q_acs_net(-1, 3600.0)
    with pytest.raises(ValueError):
        mh803_q_acs_net(5581.333333333333, -1)


def test_gas_acs_e_pdc_acs():
    assert mh803_gas_acs(5581.333333333333, 0.9) == pytest.approx(6201.481481481481)
    assert mh803_gas_acs(0, 0.9) == 0.0
    assert mh803_gas_acs(5581.333333333333, 1.0) == pytest.approx(5581.333333333333)
    assert mh803_e_pdc_acs(1981.333333333333, 3.2) == pytest.approx(619.1666666666665)
    assert mh803_e_pdc_acs(0, 3.2) == 0.0
    with pytest.raises(ValueError):
        mh803_gas_acs(5581.333333333333, 0)
    with pytest.raises(ValueError):
        mh803_gas_acs(5581.333333333333, 1.01)
    with pytest.raises(ValueError):
        mh803_e_pdc_acs(1981.333333333333, 1.0)


def test_c_base_c_alt_scomposizione():
    assert mh803_c_base(96000.0, 6201.481481481481, 90,
                        14636.363636363636, 250,
                        1500) == pytest.approx(14357.224242424243)
    assert mh803_c_base(96000.0, 6201.481481481481, 0,
                        14636.363636363636, 250,
                        1500) == pytest.approx(5159.090909090909)
    assert mh803_c_alt(78260.86956521739, 90, 10062.5,
                       619.1666666666665, 250,
                       2500) == pytest.approx(12213.894927536232)
    assert mh803_c_alt(78260.86956521739, 90, 10062.5, 0, 250,
                       2500) == pytest.approx(12059.103260869565)
    with pytest.raises(ValueError):
        mh803_c_base(96000.0, 6201.48, 90, 14636.36, 250, -1)
    with pytest.raises(ValueError):
        mh803_c_alt(78260.87, 90, 10062.5, 619.17, 250, -1)


def test_risparmio_segno():
    assert mh803_risparmio(14357.224242424243, 12213.894927536232) == pytest.approx(2143.329314888011)
    assert mh803_risparmio(12213.89, 12213.89) == 0.0


def test_co2_base_alt_evitata():
    assert mh803_co2_base(96000.0, 6201.481481481481, 0.20,
                          14636.363636363636,
                          0.35) == pytest.approx(25.563023569023567)
    assert mh803_co2_alt(78260.86956521739, 0.20, 10062.5,
                         619.1666666666665,
                         0.35) == pytest.approx(19.39075724637681)
    assert mh803_co2_evitata(96000.0, 6201.481481481481, 0.20,
                             14636.363636363636,
                             78260.86956521739, 10062.5,
                             619.1666666666665,
                             0.35) == pytest.approx(6.172266322646756)
    assert mh803_co2_base(0, 0, 0.20, 0, 0.35) == pytest.approx(0.0)
    assert mh803_co2_alt(0, 0.20, 0, 0, 0.35) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh803_co2_base(96000.0, 6201.48, -0.10, 14636.36, 0.35)
    with pytest.raises(ValueError):
        mh803_co2_alt(78260.87, 0.20, 10062.5, 619.17, -0.10)


def test_breakeven_demo_e_varianti():
    assert mh803_breakeven_gas(10062.5, 619.1666666666665,
                               250, 2500,
                               14636.363636363636, 1500,
                               96000.0, 6201.481481481481,
                               78260.86956521739) == \
        pytest.approx(0.47307719683066607)
    assert mh803_breakeven_gas(10062.5, 619.1666666666665,
                               250, 2500,
                               14636.363636363636, 1500,
                               78260.86956521739, 0,
                               78260.86956521739) is None
    assert mh803_breakeven_gas(10062.5, 619.1666666666665,
                               250, 1500,
                               14636.363636363636, 1500,
                               96000.0, 6201.481481481481,
                               78260.86956521739) is None
    with pytest.raises(ValueError):
        mh803_breakeven_gas(10062.5, 619.17, 250, 2500,
                            14636.36, 1500,
                            96000.0, 6201.48, -1)


def test_breakeven_verifica_pareggio():
    be = mh803_demo_calcoli()["breakeven_gas_eur_mwh"]
    assert be == pytest.approx(0.47307719683066607)
    bc = _variante(p_gas=be)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    demo = mh803_demo_calcoli()
    assert demo["breakeven_gas_eur_mwh"] is not None
    assert (demo["gas_forno_base_kwh_anno"]
            + demo["gas_acs_base_kwh_anno"]
            - demo["gas_forno_alt_kwh_anno"]) > 0.0


def test_breakeven_soglia_minima():
    bc_alto = _variante(p_gas=1.473077196830666)
    bc_basso = _variante(p_gas=0.0)
    assert bc_alto["c_alt_eur_anno"] < bc_alto["c_base_eur_anno"]
    assert bc_basso["c_alt_eur_anno"] > bc_basso["c_base_eur_anno"]
    assert bc_alto["verdetto"] == "NON_CONVIENTE"
    assert bc_basso["verdetto"] == "NON_CALCOLABILE"


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh803_flussi(20000, 2143.329314888011, 15)
    assert len(fl) == 16
    assert fl[0] == -20000
    assert all(f == 2143.329314888011 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh803_demo_calcoli()
    assert bc["van"] == pytest.approx(2247.025351745442)
    assert mh803_van([-20000] + [2143.329314888011] * 15,
                     0) == pytest.approx(12149.939723320165)
    assert mh803_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh803_demo_calcoli()
    assert bc["tir"] == pytest.approx(6.6188810791093395)
    assert mh803_tir([-20000] + [2143.329314888011] * 15) == \
        pytest.approx(0.066188810791093395)
    tir = mh803_tir([-20000] + [2143.329314888011] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-20000] + [2143.329314888011] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh803_payback([-20000] + [2143.329314888011] * 15) == 10
    assert mh803_payback([-20000] + [-1000.0] * 15) is None
    assert mh803_payback([0] + [2143.329314888011] * 15) == 0
    assert mh803_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh803_verdetto(2143.329314888011, 2247.025351745442, 20000,
                          10.0) == "CONVIENTE"
    assert mh803_verdetto(2143.329314888011, 0.0, 20000, 10.0) == "MARGINALE"
    assert mh803_verdetto(2143.329314888011, -2000.0, 20000, 10.0) == "MARGINALE"
    assert mh803_verdetto(2143.329314888011, -2000.01, 20000, 10.0) == "NON_CONVIENTE"
    assert mh803_verdetto(2143.329314888011, -6599.27, 20000, 10.0) == "NON_CONVIENTE"
    assert mh803_verdetto(0.0, 2247.025351745442, 20000,
                          10.0) == "NON_CALCOLABILE"
    assert mh803_verdetto(-877.91, -29112.39, 20000,
                          10.0) == "NON_CALCOLABILE"
    assert mh803_verdetto(None, 2247.025351745442, 20000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh803_verdetto(float("nan"), 2247.03, 20000, 10.0)
    with pytest.raises(ValueError):
        mh803_verdetto(2143.329314888011, 2247.03, -1, 10.0)
    with pytest.raises(ValueError):
        mh803_verdetto(2143.329314888011, 2247.03, 20000, 100.1)


def test_valida_demo_ok():
    v = mh803_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("kg_dolci_giorno", "400"),
                       ("kg_dolci_giorno", float("nan")),
                       ("kg_dolci_giorno", float("inf")),
                       ("kg_dolci_giorno", True),
                       ("p_gas", None),
                       ("q_celle_per_kg", "0.20")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh803_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("kg_dolci_giorno", -10),
                          ("giorni_anno", 0),
                          ("giorni_anno", 2.5),
                          ("q_cottura_per_kg", -0.1),
                          ("eta_forno_base", 0),
                          ("eta_forno_base", 1.01),
                          ("eta_forno_alt", 0),
                          ("eta_forno_alt", 1.01),
                          ("cp_dolci", 0),
                          ("cp_dolci", -1),
                          ("t_in", 3),
                          ("t_out", -1),
                          ("t_out", 85),
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
        assert mh803_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"kg_dolci_giorno": 0,
              "q_cottura_per_kg": 0,
              "q_celle_per_kg": 0,
              "litri_acs_giorno": 0,
              "f_rec": 0,
              "p_gas": 0,
              "p_el": 0,
              "om_base": 0, "om_alt": 0,
              "capex": 0, "wacc_pct": 0,
              "f_gas": 0, "f_el": 0,
              "tolleranza_pct": 0})
    assert mh803_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["f_rec"] = 1.0
    d["kg_dolci_giorno"] = 400
    assert mh803_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh803_demo()
    assert d["kg_dolci_giorno"] == 400
    assert d["giorni_anno"] == 300
    assert d["q_cottura_per_kg"] == 0.60
    assert d["eta_forno_base"] == 0.75
    assert d["eta_forno_alt"] == 0.92
    assert d["cp_dolci"] == 3.0
    assert d["t_in"] == 85
    assert d["t_out"] == 3
    assert d["q_celle_per_kg"] == 0.20
    assert d["cop_freddo_base"] == 2.2
    assert d["cop_freddo_alt"] == 3.2
    assert d["litri_acs_giorno"] == 400
    assert d["delta_t_acs"] == 40
    assert d["f_rec"] == 0.05
    assert d["eta_caldaia_base"] == 0.90
    assert d["cop_pdc_acs"] == 3.2
    assert d["p_gas"] == 90
    assert d["p_el"] == 250
    assert d["om_base"] == 1500
    assert d["om_alt"] == 2500
    assert d["capex"] == 20000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["f_gas"] == 0.20
    assert d["f_el"] == 0.35
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    bc = mh803_demo_calcoli()
    for chiave, atteso in _DEMO.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert got == pytest.approx(atteso, rel=1e-9), chiave
    assert bc["payback"] == 10
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(0.47307719683066607)
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True
    assert demo_calcoli()["van"] == bc["van"]


def test_demo_calcoli_fisica_economia():
    bc = mh803_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(14357.224242424243)
    assert bc["c_alt_eur_anno"] == pytest.approx(12213.894927536232)
    assert bc["risparmio_eur_anno"] == pytest.approx(2143.329314888011)
    assert bc["co2_base_t_anno"] == pytest.approx(25.563023569023567)
    assert bc["co2_alt_t_anno"] == pytest.approx(19.39075724637681)
    assert bc["co2_evitata_t_anno"] == pytest.approx(6.172266322646756)
    assert bc["kg_dolci_anno"] == pytest.approx(120000.0)
    assert bc["q_cottura_kwh_anno"] == pytest.approx(72000.0)
    assert bc["q_freddo_kwh_anno"] == pytest.approx(32200.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(3600.0)
    assert bc["q_acs_net_kwh_anno"] == pytest.approx(1981.333333333333)


def test_demo_flussi_e_cumulato():
    bc = mh803_demo_calcoli()
    assert bc["flussi"][0] == -20000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(2143.329314888011) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -20000
    assert righe.iloc[9]["Cumulato (EUR)"] == pytest.approx(-710.0361660078997)
    assert righe.iloc[10]["Cumulato (EUR)"] == pytest.approx(1433.2931488801114)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(12149.939723320165)


def test_demo_tabella_righe():
    bc = mh803_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Kg di dolci all'anno"] == pytest.approx(120000.0)
    assert mappa["Calore di cottura (kWh_th/anno)"] == pytest.approx(72000.0)
    assert mappa["Gas forno base (kWh/anno)"] == pytest.approx(96000.0)
    assert mappa["Gas forno alt (kWh/anno)"] == pytest.approx(78260.86956521739)
    assert mappa["Freddo abbattitore (kWh_c/anno)"] == pytest.approx(8200.0)
    assert mappa["Carico celle (kWh_c/anno)"] == pytest.approx(24000.0)
    assert mappa["Freddo totale (kWh_c/anno)"] == pytest.approx(32200.0)
    assert mappa["Elettricita' freddo base (kWh_e/anno)"] == pytest.approx(14636.363636363636)
    assert mappa["Elettricita' freddo alt (kWh_e/anno)"] == pytest.approx(10062.5)
    assert mappa["ACS di lavaggio (kWh_th/anno)"] == pytest.approx(5581.333333333333)
    assert mappa["Calore forno recuperato (kWh_th/anno)"] == pytest.approx(3600.0)
    assert mappa["ACS netta (kWh_th/anno)"] == pytest.approx(1981.333333333333)
    assert mappa["Gas ACS baseline (kWh/anno)"] == pytest.approx(6201.481481481481)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(14357.224242424243)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(12213.894927536232)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(2143.329314888011)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(6.172266322646756)
    assert mappa["Payback (anni)"] == 10
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] == pytest.approx(0.47307719683066607)


def test_demo_coerenza_interna():
    bc = mh803_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["kg_dolci_anno"] == pytest.approx(
        bc["kg_dolci_giorno"] * bc["giorni_anno"])
    assert bc["q_cottura_kwh_anno"] == pytest.approx(
        bc["kg_dolci_anno"] * bc["q_cottura_per_kg"])
    assert bc["gas_forno_base_kwh_anno"] == pytest.approx(
        bc["q_cottura_kwh_anno"] / bc["eta_forno_base"])
    assert bc["gas_forno_alt_kwh_anno"] == pytest.approx(
        bc["q_cottura_kwh_anno"] / bc["eta_forno_alt"])
    assert bc["q_abbattitore_kwh_anno"] == pytest.approx(
        bc["kg_dolci_anno"] * bc["cp_dolci"]
        * (bc["t_in"] - bc["t_out"]) / 3600.0)
    assert bc["q_celle_kwh_anno"] == pytest.approx(
        bc["kg_dolci_anno"] * bc["q_celle_per_kg"])
    assert bc["q_freddo_kwh_anno"] == pytest.approx(
        bc["q_abbattitore_kwh_anno"] + bc["q_celle_kwh_anno"])
    assert bc["e_freddo_base_kwh_anno"] == pytest.approx(
        bc["q_freddo_kwh_anno"] / bc["cop_freddo_base"])
    assert bc["e_freddo_alt_kwh_anno"] == pytest.approx(
        bc["q_freddo_kwh_anno"] / bc["cop_freddo_alt"])
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
        (bc["gas_forno_base_kwh_anno"]
         + bc["gas_acs_base_kwh_anno"]) / 1000.0 * bc["p_gas"]
        + bc["e_freddo_base_kwh_anno"] / 1000.0 * bc["p_el"]
        + bc["om_base"])
    assert bc["c_alt_eur_anno"] == pytest.approx(
        bc["gas_forno_alt_kwh_anno"] / 1000.0 * bc["p_gas"]
        + (bc["e_freddo_alt_kwh_anno"]
           + bc["e_pdc_acs_kwh_anno"])
        / 1000.0 * bc["p_el"]
        + bc["om_alt"])


def test_demo_contro_riconteggio_indipendente():
    kgg, gg, qc = 400, 300, 0.60
    efb, efa, cp = 0.75, 0.92, 3.0
    tin, tout, qcel = 85, 3, 0.20
    cfb, cfa = 2.2, 3.2
    lit, dt, frec = 400, 40, 0.05
    eta, copp = 0.90, 3.2
    pg, pel = 90, 250
    omb, oma, cx = 1500, 2500, 20000
    fg, fel, wacc, vita = 0.20, 0.35, 5.0, 15
    kga = kgg * gg
    qcott = kga * qc
    gfb = qcott / efb
    gfa = qcott / efa
    qabb = kga * cp * (tin - tout) / 3600.0
    qce = kga * qcel
    qfr = qabb + qce
    efbk = qfr / cfb
    efak = qfr / cfa
    qacs = lit * gg * 4.186 * dt / 3600.0
    qrec = min(qacs, qcott * frec)
    qnet = max(0.0, qacs - qrec)
    gasa = qacs / eta
    epdc = qnet / copp
    cb = (gfb + gasa) / 1000.0 * pg + efbk / 1000.0 * pel + omb
    ca = gfa / 1000.0 * pg + (efak + epdc) / 1000.0 * pel + oma
    risp = cb - ca
    co2b = (gfb + gasa) / 1000.0 * fg + efbk / 1000.0 * fel
    co2a = gfa / 1000.0 * fg + (efak + epdc) / 1000.0 * fel
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    bc = mh803_demo_calcoli()
    assert bc["kg_dolci_anno"] == pytest.approx(kga)
    assert bc["q_cottura_kwh_anno"] == pytest.approx(qcott)
    assert bc["gas_forno_base_kwh_anno"] == pytest.approx(gfb)
    assert bc["gas_forno_alt_kwh_anno"] == pytest.approx(gfa)
    assert bc["q_abbattitore_kwh_anno"] == pytest.approx(qabb)
    assert bc["q_celle_kwh_anno"] == pytest.approx(qce)
    assert bc["q_freddo_kwh_anno"] == pytest.approx(qfr)
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
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(
        ((efak + epdc) / 1000.0 * pel + oma
         - efbk / 1000.0 * pel - omb)
        / ((gfb + gasa - gfa) / 1000.0))


# ---------------------------------------------------------------- varianti
def test_variante_gas_zero_non_calcolabile():
    bc = _variante(p_gas=0)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(-11.3258, abs=1e-2)
    assert bc["van"] == pytest.approx(-20117.56, abs=1e-2)
    assert bc["payback"] is None
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(0.47307719683066607)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_gas_alto_conviente():
    bc = _variante(p_gas=150)
    assert bc["risparmio_eur_anno"] == pytest.approx(3579.7660, abs=1e-2)
    assert bc["van"] == pytest.approx(17156.7472, abs=1e-2)
    assert bc["tir"] == pytest.approx(15.956051214882338)
    assert bc["payback"] == 6
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_senza_recupero_marginale():
    bc = _variante(f_rec=0)
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["q_acs_net_kwh_anno"] == pytest.approx(5581.333333333333)
    assert bc["risparmio_eur_anno"] == pytest.approx(1862.0793148880111)
    assert bc["van"] == pytest.approx(-672.2534714928487)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(12.220897218462298)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"


def test_variante_recupero_pieno_satura_conviente():
    bc = _variante(f_rec=1.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(5581.333333333333)
    assert bc["q_acs_net_kwh_anno"] == 0.0
    assert bc["e_pdc_acs_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(2298.120981554679)
    assert bc["van"] == pytest.approx(3853.709918905492)
    assert bc["payback"] == 9
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_acs_piccola_satura_marginale():
    bc = _variante(litri_acs_giorno=100)
    assert bc["q_acs_kwh_anno"] == pytest.approx(1395.3333333333333)
    assert bc["q_rec_kwh_anno"] == pytest.approx(1395.3333333333333)
    assert bc["q_acs_net_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(1879.5209815546768)
    assert bc["van"] == pytest.approx(-491.21493587692555)
    assert bc["verdetto"] == "MARGINALE"


def test_variante_dolci_piccoli_e_grandi():
    bc = _variante(kg_dolci_giorno=200)
    assert bc["kg_dolci_anno"] == pytest.approx(60000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(632.7104907773382)
    assert bc["van"] == pytest.approx(-13432.681468561816)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"
    bc2 = _variante(kg_dolci_giorno=800)
    assert bc2["risparmio_eur_anno"] == pytest.approx(5038.108629776027)
    assert bc2["van"] == pytest.approx(32293.844736281735)
    assert bc2["payback"] == 4
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_capex_conviente_marginale_non_conviente():
    bc = _variante(capex=22000)
    assert bc["risparmio_eur_anno"] == pytest.approx(2143.329314888011)
    assert bc["van"] == pytest.approx(247.025351745442)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(capex=23000)
    assert bc2["van"] == pytest.approx(-752.974648254558)
    assert bc2["payback"] == 11
    assert bc2["verdetto"] == "MARGINALE"
    bc3 = _variante(capex=30000)
    assert bc3["van"] == pytest.approx(-7752.974648254558)
    assert bc3["payback"] == 14
    assert bc3["verdetto"] == "NON_CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex=0)
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(22247.025351745444, rel=1e-6)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(12149.939723320165)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(-3449.7792, abs=1e-2)
    assert bc2["payback"] == 10
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_el_alto_e_om_alt_alto():
    bc = _variante(p_el=400)
    assert bc["risparmio_eur_anno"] == pytest.approx(2736.5338603425553)
    assert bc["van"] == pytest.approx(8404.285680257964)
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(om_alt=5000)
    assert bc2["risparmio_eur_anno"] == pytest.approx(-356.67068511198886)
    assert bc2["verdetto"] == "NON_CALCOLABILE"


def test_variante_senza_acs_e_senza_celle():
    bc = _variante(litri_acs_giorno=0)
    assert bc["q_acs_kwh_anno"] == 0.0
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["gas_acs_base_kwh_anno"] == 0.0
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["risparmio_eur_anno"] == pytest.approx(1739.9876, abs=1e-2)
    assert bc["van"] == pytest.approx(-1939.5232, abs=1e-2)
    assert bc["payback"] == 12
    assert bc["verdetto"] == "MARGINALE"
    bc2 = _variante(q_celle_per_kg=0)
    assert bc2["q_celle_kwh_anno"] == 0.0
    assert bc2["q_freddo_kwh_anno"] == pytest.approx(8200.0)
    assert bc2["risparmio_eur_anno"] == pytest.approx(1291.0566, abs=1e-2)
    assert bc2["van"] == pytest.approx(-6599.2741, abs=1e-2)
    assert bc2["breakeven_gas_eur_mwh"] == pytest.approx(36.07253180783564)
    assert bc2["payback"] is None
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_om_alt_basso_be_none():
    bc = _variante(om_alt=1500)
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["risparmio_eur_anno"] == pytest.approx(3143.329314888011)
    assert bc["van"] == pytest.approx(12626.6834, abs=1e-2)
    assert bc["payback"] == 7
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_senza_dolci_non_calcolabile():
    bc = _variante(kg_dolci_giorno=0)
    assert bc["kg_dolci_anno"] == 0.0
    assert bc["q_cottura_kwh_anno"] == 0.0
    assert bc["q_freddo_kwh_anno"] == 0.0
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(231.5642916865743)
    assert bc["risparmio_eur_anno"] == pytest.approx(-877.9083, abs=1e-2)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_forno_alt_uguale_base_e_cp_basso():
    bc = _variante(eta_forno_alt=0.75)
    assert bc["gas_forno_alt_kwh_anno"] == pytest.approx(96000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(546.8076, abs=1e-2)
    assert bc["van"] == pytest.approx(-14324.3244, abs=1e-2)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(1.826298701298619)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"
    bc2 = _variante(cp_dolci=2.0)
    assert bc2["q_freddo_kwh_anno"] == pytest.approx(29466.666666666668)
    assert bc2["risparmio_eur_anno"] == pytest.approx(2046.2649, abs=1e-2)
    assert bc2["van"] == pytest.approx(1239.5301, abs=1e-2)
    assert bc2["payback"] == 10
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_t_in_basso_conviente():
    bc = _variante(t_in=60)
    assert bc["q_abbattitore_kwh_anno"] == pytest.approx(5700.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(2054.5509, abs=1e-2)
    assert bc["van"] == pytest.approx(1325.5358, abs=1e-2)
    assert bc["payback"] == 10
    assert bc["verdetto"] == "CONVIENTE"


def test_monotonia_prezzo_gas_crescente():
    base = mh803_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas=91)["risparmio_eur_anno"]
    basso = _variante(p_gas=89)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(23.9406, abs=1e-2)
    assert base - basso == pytest.approx(23.9406, abs=1e-2)


def test_monotonia_dolci_crescente():
    assert _variante(kg_dolci_giorno=200)["risparmio_eur_anno"] < \
        mh803_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(kg_dolci_giorno=800)["risparmio_eur_anno"] > \
        mh803_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(kg_dolci_giorno=800)["kg_dolci_anno"] == \
        pytest.approx(240000.0)


def test_demo_deterministica_due_chiamate():
    a = mh803_demo_calcoli()
    b = mh803_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh803_demo().keys()) == {
        "kg_dolci_giorno", "giorni_anno",
        "q_cottura_per_kg",
        "eta_forno_base", "eta_forno_alt",
        "cp_dolci", "t_in", "t_out",
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


def test_degenere_temperature_sollevano():
    with pytest.raises(ValueError):
        _variante(t_in=3)
    with pytest.raises(ValueError):
        _variante(t_out=85)
    with pytest.raises(ValueError):
        _variante(t_out=-1)
    with pytest.raises(ValueError):
        _variante(t_in=85, t_out=85)


def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"kg_dolci_giorno": -10},
               {"giorni_anno": 0},
               {"giorni_anno": 2.5},
               {"q_cottura_per_kg": -0.1},
               {"eta_forno_base": 0}, {"eta_forno_base": 1.01},
               {"eta_forno_alt": 0}, {"eta_forno_alt": 1.01},
               {"cp_dolci": 0}, {"cp_dolci": -1},
               {"t_in": 3},
               {"t_out": -1}, {"t_out": 85},
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
        assert mh803_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"kg_dolci_giorno": "400"},
               {"kg_dolci_giorno": float("nan")},
               {"p_gas": float("inf")},
               {"capex": True},
               {"q_celle_per_kg": "0.20"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh803_valida(**d)["valido"] is False


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    for kw in ({"p_gas": 0},
               {"kg_dolci_giorno": 0},
               {"om_alt": 5000}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] <= 0.0
        assert bc["verdetto"] == "NON_CALCOLABILE"
        assert bc["flussi"]


def test_pareggio_esatto_tolleranza_float():
    # A pareggio esatto (prezzo gas = breakeven)
    # il risparmio e' zero (circa 0.0, quindi guard
    # NON_CALCOLABILE): in nessun caso CONVIENTE.
    be = mh803_demo_calcoli()["breakeven_gas_eur_mwh"]
    bc = _variante(p_gas=be)
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["verdetto"] != "CONVIENTE"
    bc2 = _variante(p_gas=be + 1)
    assert bc2["risparmio_eur_anno"] == pytest.approx(23.9406, abs=1e-2)
    assert bc2["van"] == pytest.approx(-19751.51, abs=1e-2)
    assert bc2["verdetto"] == "NON_CONVIENTE"
    bc3 = _variante(p_gas=be - 0.4)
    assert bc3["risparmio_eur_anno"] == pytest.approx(-9.5762, abs=1e-2)
    assert bc3["verdetto"] == "NON_CALCOLABILE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh803_demo_calcoli()
    testo = mh803_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_gas_eur_mwh" in testo
    assert "co2_evitata_t_anno" in testo
    assert "q_cottura_kwh_anno" in testo
    assert "kg_dolci_giorno" in testo
    assert "e_freddo_alt_kwh_anno" in testo
    assert "q_abbattitore_kwh_anno" in testo
    assert "q_rec_kwh_anno" in testo
    assert "q_acs_net_kwh_anno" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh803_demo_calcoli()
    testo = mh803_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"kg_dolci_anno;{bc['kg_dolci_anno']}" in testo
    assert f"gas_acs_base_kwh_anno;{bc['gas_acs_base_kwh_anno']}" in testo
    assert f"q_celle_kwh_anno;{bc['q_celle_kwh_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh803_demo_calcoli()
    testo = mh803_csv(bc, _demo_kwargs())
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
    return ["mh" + "80" + "2", "st" + "80" + "2",
            "tab" + "80" + "2", "w" + "80" + "3",
            "mh" + "80" + "1", "tab" + "80" + "1"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w804_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w804_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab803:")


def test_ui_apre_scheda_attesa_una_volta():
    """Il frammento UI apre la scheda attesa, una sola volta."""
    src = _leggi("w804_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert src.count("with tab803:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w804_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w804_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st803_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) >= 28
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w804_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 4
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w804_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def803[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w804_ui.py")
        usate = set(re.findall(r'_def803\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 26
        assert usate <= set(mh803_demo().keys())
