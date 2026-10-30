"""Test nuova scheda "Studio dentistico: pompa
di calore + recupero calore compressore su ACS
+ autoclave efficiente batte caldaia a gas +
chiller + autoclave tradizionale?" (titolo
completo nel frammento UI).
Contenuto pronto da scrivere in repo come test
della scheda studio dentistico.

Business case deterministico di uno studio
dentistico guidato dai RIUNITI ODONTOIATRICI,
dai M2 DI AMBULATORI e dai GIORNI DI APERTURA
ALL'ANNO: i riuniti guidano i cicli di
autoclave (cicli al giorno per riunito) e i
litri di ACS al giorno per riunito, i m2
guidano riscaldamento e raffrescamento, i
giorni guidano l'anno e il compressore aria
dentale (ore al giorno x potenza).
Cicli annui = riuniti x cicli al giorno per
riunito x giorni; riscaldamento = S x q_risc;
raffrescamento = S x q_raff; litri annui =
riuniti x litri al giorno per riunito x
giorni; ACS = litri annui x 4,186 x delta_T /
3600; elettricita' compressore base = giorni x
ore x potenza e alt = base x fattore (0,80);
calore di scarto = base x f_scart; recupero
potenziale = scarto x eta_rec; recupero =
min(ACS, potenziale) (saturato all'ACS; nel
demo SATURA: il potenziale 4.675,00 supera
l'ACS 2.441,83); ACS netta = max(0, ACS -
recupero) (nel demo zero); elettricita'
autoclave base = cicli annui x kWh_e per ciclo
e alt = base x fattore (0,75); gas baseline =
(riscaldamento + ACS) / eta_caldaia (senza
recupero); chiller = raffrescamento /
COP_chiller; pompa di calore riscaldamento =
riscaldamento / COP_risc, raffrescamento =
raffrescamento / COP_raff, ACS = ACS netta /
COP_acs; C_base = gas_base / 1000 x p_gas +
(comp_base + aut_base + chiller) / 1000 x p_el
+ O&M_base; C_alt = (comp_alt + aut_alt +
pdc_risc + pdc_raff + pdc_acs) / 1000 x p_el +
O&M_alt (niente gas: l'alternativa non ha
caldaia); risparmio = C_base - C_alt;
CO2_base = gas_base / 1000 x f_gas +
(comp_base + aut_base + chiller) / 1000 x f_el;
CO2_alt = (comp_alt + aut_alt + pdc_risc +
pdc_raff + pdc_acs) / 1000 x f_el; CO2_evitata =
CO2_base - CO2_alt; flussi [-CAPEX, risparmio
x vita]; VAN, TIR, payback (primo anno con
cumulato >= 0); breakeven gas =
((comp_alt + aut_alt + pdc_risc + pdc_raff +
pdc_acs) / 1000 x p_el + O&M_alt -
(comp_base + aut_base + chiller) / 1000 x p_el
- O&M_base) / (gas_base / 1000) EUR/MWh, None
se denominatore gas <= 0 o numeratore < 0,
SOGLIA MINIMA quando esiste.
Verdetto: NON_CALCOLABILE se input degenere
(riuniti <= 0, giorni <= 0, S <= 0, eta
<= 0 o > 1, COP <= 1, delta_T <= 0, eta_rec
< 0 o > 1, f_scart < 0 o > 1, fattori <= 0 o
> 1, prezzi <= 0, CAPEX <= 0, vita <= 0) o
se risparmio <= 0 (guard degenere: UI salta
KPI, grafico, tabella e CSV); altrimenti
CONVIENTE se VAN > 0, MARGINALE se VAN
negativa entro tolleranza % del CAPEX,
NON_CONVIENTE se VAN negativa oltre la
tolleranza. Differenze UI-vs-helper
documentate: riuniti = 0 e' calcolabile negli
helper (risparmio positivo, VAN negativa,
verdetto NON_CONVIENTE) ma bloccato dalla
guard UI (NON_CALCOLABILE): DIVERGENZA di
verdetto; CAPEX = 0 e' CONVIENTE negli helper
(VAN positiva, TIR None, payback 0) ma
bloccato dalla guard UI; prezzi = 0 sono
ammessi negli helper ma bloccati dalla guard
UI; p_gas = 0 da' risparmio NEGATIVO negli
helper (-1.886,78 EUR/anno, verdetto
NON_CALCOLABILE: l'elettricita' alternativa
supera la base), quindi QUI NON c'e'
divergenza di verdetto helper-vs-UI per gas
zero (stesso verdetto, solo guard prima);
S = 0 e' calcolabile negli helper ma bloccato
dalla guard UI.
Distinzione esplicita: distinto dal
conservificio (autoclave per conserve
alimentari in produzione alimentare: qui
nessuna conserva, nessun processo di
produzione, l'autoclave sterilizza strumenti
odontoiatrici in cicli per riunito),
dall'ospedale (reparti e posti letto 24 ore
su 24, degenze: qui nessun reparto, nessun
posto letto, nessuna degenza, driver riuniti
e m2 di ambulatori con apertura diurna),
dall'albergo (pernottamento, ACS docce
ospiti: qui nessun ospite, nessuna doccia,
l'ACS segue i litri al giorno per riunito),
dalla palestra (docce utenti, ACS delle
docce: qui nessuna doccia, nessun utente che
fa sport, l'ACS segue i litri al giorno per
riunito), dalla lavanderia (cicli di lavaggio
dei panni, kg per ciclo, asciugatura, recupero
dalle acque reflue: qui nessun panno, nessuna
asciugatura, nessun lavaggio, il recupero
viene dal calore di scarto del compressore
aria dentale): qui driver RIUNITI + M2 +
GIORNI + CICLI + COMPRESSORE = riuniti per
autoclave e ACS, m2 per riscaldamento e
raffrescamento, giorni per l'anno e il
compressore, cicli per riunito per la
sterilizzazione, ore e potenza per il
compressore; niente conserve, niente reparti,
niente pernottamenti, niente docce, niente
panni.

Demo (studio dentistico): 4 riuniti per 250
giorni di apertura all'anno, 6 cicli di
autoclave al giorno per riunito (6.000 cicli
all'anno), superficie 300 m2 con 110
kWh_th/m2 di riscaldamento (33.000
kWh_th/anno) e 70 kWh_th/m2 di raffrescamento
(21.000 kWh_th/anno), ACS 60 litri al giorno
per riunito (60.000 litri all'anno) con
delta_T 35 K (2.441,83 kWh_th/anno),
compressore 8 ore al giorno da 5,5 kW
(11.000 kWh_e/anno base, 8.800 alt con
fattore 0,80), frazione di scarto 0,85
(9.350 kWh_th/anno), rendimento di recupero
0,50 (potenziale 4.675,00, SATURATO all'ACS
2.441,83, ACS netta zero), autoclave 1,5
kWh_e per ciclo (9.000 kWh_e/anno base,
6.750 alt con fattore 0,75), caldaia 0,90,
chiller COP 3,0, pompa di calore COP
riscaldamento 3,8 / raffrescamento 3,4 / ACS
3,0, gas 100, el 260 EUR/MWh, O&M base 3.000,
alt 4.000, CAPEX 20.000, WACC 5 %, vita 15,
f_gas 0,20, f_el 0,35, tolleranza 10 % del
CAPEX. Valori calcolati eseguendo
mh808_demo_calcoli(): cicli annui 6.000,
Q_risc 33.000, Q_raff 21.000, litri annui
60.000, Q_acs 2.441,8333333333335,
E_comp_base 11.000, E_comp_alt 8.800,
Q_scart 9.350, Q_rec_pot 4.675, Q_rec
2.441,8333333333335 (SATURATO: il potenziale
4.675,00 supera l'ACS), Q_acs_net 0,0,
E_aut_base 9.000, E_aut_alt 6.750, gas_base
39.379,81481481482, E_chiller 7.000,
E_pdc_risc 8.684,21052631579, E_pdc_raff
6.176,470588235295, E_pdc_acs 0,0, C_base
13.957,981481481482, C_alt
11.906,777089783282, risparmio
2.051,2043916982, CO2_base
17,32596296296296, CO2_alt
10,64373839009288, CO2_evitata
6,682224572870082, VAN 1.290,8001522415523,
TIR 5,940108156482945 %, payback 10,
breakeven gas 47,91228954874287 EUR/MWh
(soglia minima), verdetto CONVIENTE.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w809_helpers import (
    demo_calcoli,
    mh808_breakeven_gas,
    mh808_c_alt,
    mh808_c_base,
    mh808_calcola,
    mh808_cicli_anno,
    mh808_co2_alt,
    mh808_co2_base,
    mh808_co2_evitata,
    mh808_cop,
    mh808_csv,
    mh808_demo,
    mh808_demo_calcoli,
    mh808_e_aut_alt,
    mh808_e_aut_base,
    mh808_e_chiller,
    mh808_e_comp_alt,
    mh808_e_comp_base,
    mh808_e_pdc,
    mh808_eta,
    mh808_fattore_alt,
    mh808_flussi,
    mh808_frazione,
    mh808_gas_base,
    mh808_int_pos,
    mh808_litri_anno,
    mh808_num,
    mh808_nneg,
    mh808_payback,
    mh808_pct_tolleranza,
    mh808_pos,
    mh808_pct_wacc,
    mh808_q_acs,
    mh808_q_acs_net,
    mh808_q_raff,
    mh808_q_rec,
    mh808_q_rec_pot,
    mh808_q_risc,
    mh808_q_scart_comp,
    mh808_risparmio,
    mh808_tir,
    mh808_valida,
    mh808_van,
    mh808_verdetto,
)

_DEMO = {
    "cicli_anno": 6000.0,
    "q_risc_kwh_anno": 33000.0,
    "q_raff_kwh_anno": 21000.0,
    "litri_anno": 60000.0,
    "q_acs_kwh_anno": 2441.8333333333335,
    "e_comp_base_kwh_anno": 11000.0,
    "e_comp_alt_kwh_anno": 8800.0,
    "q_scart_comp_kwh_anno": 9350.0,
    "q_rec_pot_kwh_anno": 4675.0,
    "q_rec_kwh_anno": 2441.8333333333335,
    "q_acs_net_kwh_anno": 0.0,
    "e_aut_base_kwh_anno": 9000.0,
    "e_aut_alt_kwh_anno": 6750.0,
    "gas_base_kwh_anno": 39379.81481481482,
    "e_chiller_kwh_anno": 7000.0,
    "e_pdc_risc_kwh_anno": 8684.21052631579,
    "e_pdc_raff_kwh_anno": 6176.470588235295,
    "e_pdc_acs_kwh_anno": 0.0,
    "c_base_eur_anno": 13957.981481481482,
    "c_alt_eur_anno": 11906.777089783282,
    "risparmio_eur_anno": 2051.2043916982,
    "co2_base_t_anno": 17.32596296296296,
    "co2_alt_t_anno": 10.64373839009288,
    "co2_evitata_t_anno": 6.682224572870082,
    "van": 1290.8001522415523,
    "tir": 5.940108156482945,
    "breakeven_gas_eur_mwh": 47.91228954874287,
}


def _demo_kwargs():
    return dict(mh808_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh808_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh808_num(3, "x") == 3.0
    assert mh808_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh808_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh808_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh808_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh808_pos(0, "x")
    with pytest.raises(ValueError):
        mh808_pos(-1, "x")
    assert mh808_pos(0.5, "x") == 0.5


def test_cop_maggiore_di_uno():
    assert mh808_cop(3.0, "x") == 3.0
    assert mh808_cop(3.8, "x") == 3.8
    with pytest.raises(ValueError):
        mh808_cop(1.0, "x")
    with pytest.raises(ValueError):
        mh808_cop(0.5, "x")
    with pytest.raises(ValueError):
        mh808_cop(0, "x")


def test_frazione_limiti():
    assert mh808_frazione(0, "x") == 0.0
    assert mh808_frazione(1, "x") == 1.0
    assert mh808_frazione(0.85, "x") == 0.85
    assert mh808_frazione(0.50, "x") == 0.50
    with pytest.raises(ValueError):
        mh808_frazione(-0.01, "x")
    with pytest.raises(ValueError):
        mh808_frazione(1.01, "x")


def test_fattore_alt_limiti():
    assert mh808_fattore_alt(0.80, "x") == 0.80
    assert mh808_fattore_alt(1.0, "x") == 1.0
    with pytest.raises(ValueError):
        mh808_fattore_alt(0, "x")
    with pytest.raises(ValueError):
        mh808_fattore_alt(1.01, "x")
    with pytest.raises(ValueError):
        mh808_fattore_alt(-0.1, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh808_int_pos(5.0, "x") == 5
    assert mh808_int_pos(250.0, "x") == 250
    with pytest.raises(ValueError):
        mh808_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh808_int_pos(0, "x")


def test_eta_limiti():
    assert mh808_eta(1.0, "x") == 1.0
    assert mh808_eta(0.90, "x") == 0.90
    with pytest.raises(ValueError):
        mh808_eta(0, "x")
    with pytest.raises(ValueError):
        mh808_eta(1.01, "x")


def test_pct_wacc_limiti():
    assert mh808_pct_wacc(0, "x") == 0.0
    assert mh808_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh808_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh808_pct_tolleranza(0, "x") == 0.0
    assert mh808_pct_tolleranza(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh808_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh808_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_cicli_anno_litri_anno_q_risc_raff():
    assert mh808_cicli_anno(4, 6, 250) == 6000.0
    assert mh808_cicli_anno(0, 6, 250) == 0.0
    assert mh808_cicli_anno(2, 6, 250) == 3000.0
    assert mh808_litri_anno(4, 60, 250) == 60000.0
    assert mh808_litri_anno(0, 60, 250) == 0.0
    assert mh808_q_risc(300, 110) == 33000.0
    assert mh808_q_raff(300, 70) == 21000.0
    assert mh808_q_risc(0, 110) == 0.0
    with pytest.raises(ValueError):
        mh808_cicli_anno(-1, 6, 250)
    with pytest.raises(ValueError):
        mh808_cicli_anno(4, 6, 0)
    with pytest.raises(ValueError):
        mh808_cicli_anno(4, 6, 2.5)
    with pytest.raises(ValueError):
        mh808_litri_anno(-1, 60, 250)
    with pytest.raises(ValueError):
        mh808_q_risc(-1, 110)


def test_q_acs_formula():
    assert mh808_q_acs(60000, 35) == pytest.approx(2441.8333333333335)
    assert mh808_q_acs(0, 35) == 0.0
    assert mh808_q_acs(120000, 35) == pytest.approx(4883.666666666667)
    assert mh808_q_acs(60000, 17.5) == pytest.approx(1220.9166666666667)
    with pytest.raises(ValueError):
        mh808_q_acs(-1, 35)
    with pytest.raises(ValueError):
        mh808_q_acs(60000, 0)


def test_comp_scart_recupero_saturazione_e_acs_netta():
    assert mh808_e_comp_base(250, 8, 5.5) == 11000.0
    assert mh808_e_comp_base(250, 0, 5.5) == 0.0
    assert mh808_e_comp_alt(11000.0, 0.80) == 8800.0
    assert mh808_e_comp_alt(11000.0, 1.0) == 11000.0
    with pytest.raises(ValueError):
        mh808_e_comp_alt(11000.0, 0)
    with pytest.raises(ValueError):
        mh808_e_comp_alt(11000.0, 1.01)
    assert mh808_q_scart_comp(11000.0, 0.85) == 9350.0
    assert mh808_q_scart_comp(11000.0, 0) == 0.0
    assert mh808_q_rec_pot(9350.0, 0.50) == 4675.0
    assert mh808_q_rec_pot(9350.0, 0.05) == 467.5
    # Demo: potenziale 4.675,00 sopra l'ACS -> SATURA.
    assert mh808_q_rec(2441.8333333333335, 4675.0) == pytest.approx(2441.8333333333335)
    # Recupero NON saturato con eta_rec bassa.
    assert mh808_q_rec(2441.8333333333335, 467.5) == 467.5
    assert mh808_q_rec(2441.8333333333335, 0.0) == 0.0
    with pytest.raises(ValueError):
        mh808_q_rec(-1, 4675.0)
    with pytest.raises(ValueError):
        mh808_q_rec(2441.83, -1)
    assert mh808_q_acs_net(2441.8333333333335, 2441.8333333333335) == 0.0
    assert mh808_q_acs_net(2441.8333333333335, 467.5) == pytest.approx(1974.3333333333335)
    assert mh808_q_acs_net(2441.8333333333335, 0.0) == pytest.approx(2441.8333333333335)
    with pytest.raises(ValueError):
        mh808_q_acs_net(-1, 467.5)
    with pytest.raises(ValueError):
        mh808_q_acs_net(2441.83, -1)


def test_aut_chiller_pdc():
    assert mh808_e_aut_base(6000, 1.5) == 9000.0
    assert mh808_e_aut_base(0, 1.5) == 0.0
    assert mh808_e_aut_alt(9000.0, 0.75) == 6750.0
    assert mh808_e_aut_alt(9000.0, 1.0) == 9000.0
    with pytest.raises(ValueError):
        mh808_e_aut_alt(9000.0, 0)
    assert mh808_gas_base(33000.0, 2441.8333333333335, 0.90) == pytest.approx(39379.81481481482)
    assert mh808_gas_base(0, 0, 0.90) == 0.0
    assert mh808_e_chiller(21000.0, 3.0) == 7000.0
    assert mh808_e_pdc(33000.0, 3.8) == pytest.approx(8684.21052631579)
    assert mh808_e_pdc(21000.0, 3.4) == pytest.approx(6176.470588235295)
    assert mh808_e_pdc(0.0, 3.0) == 0.0
    with pytest.raises(ValueError):
        mh808_gas_base(33000.0, 2441.83, 0)
    with pytest.raises(ValueError):
        mh808_gas_base(33000.0, 2441.83, 1.01)
    with pytest.raises(ValueError):
        mh808_e_chiller(21000.0, 1.0)
    with pytest.raises(ValueError):
        mh808_e_pdc(33000.0, 1.0)


def test_c_base_c_alt_scomposizione():
    assert mh808_c_base(39379.81481481482, 100, 11000.0, 9000.0,
                        7000.0, 260,
                        3000) == pytest.approx(13957.981481481482)
    assert mh808_c_base(39379.81481481482, 0, 11000.0, 9000.0,
                        7000.0, 260,
                        3000) == pytest.approx(10020.0)
    assert mh808_c_alt(8800.0, 6750.0, 8684.21052631579,
                       6176.470588235295, 0.0, 260,
                       4000) == pytest.approx(11906.777089783282)
    assert mh808_c_alt(8800.0, 6750.0, 8684.21052631579,
                       6176.470588235295, 813.9444444444445, 260,
                       4000) == pytest.approx(12118.402645215927)
    with pytest.raises(ValueError):
        mh808_c_base(39379.81, 100, 11000.0, 9000.0, 7000.0, 260, -1)
    with pytest.raises(ValueError):
        mh808_c_alt(8800.0, 6750.0, 8684.21, 6176.47, 0.0, 260, -1)


def test_risparmio_segno():
    assert mh808_risparmio(13957.981481481482, 11906.777089783282) == pytest.approx(2051.2043916982)
    assert mh808_risparmio(11906.78, 11906.78) == 0.0


def test_co2_base_alt_evitata():
    assert mh808_co2_base(39379.81481481482, 0.20, 11000.0,
                          9000.0, 7000.0,
                          0.35) == pytest.approx(17.32596296296296)
    assert mh808_co2_alt(8800.0, 6750.0, 8684.21052631579,
                         6176.470588235295, 0.0,
                         0.35) == pytest.approx(10.64373839009288)
    assert mh808_co2_evitata(39379.81481481482, 0.20, 11000.0,
                             9000.0, 7000.0, 8800.0,
                             6750.0, 8684.21052631579,
                             6176.470588235295, 0.0,
                             0.35) == pytest.approx(6.682224572870082)
    assert mh808_co2_base(0, 0.20, 0, 0, 0, 0.35) == pytest.approx(0.0)
    assert mh808_co2_alt(0, 0, 0, 0, 0, 0.35) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh808_co2_base(39379.81, -0.10, 11000.0, 9000.0, 7000.0, 0.35)
    with pytest.raises(ValueError):
        mh808_co2_alt(8800.0, 6750.0, 8684.21, 6176.47, 0.0, -0.10)


def test_breakeven_demo_e_varianti():
    # Demo: 47,91 EUR/MWh (soglia minima, esiste).
    assert mh808_demo_calcoli()["breakeven_gas_eur_mwh"] == pytest.approx(47.91228954874287)
    assert mh808_breakeven_gas(8800.0, 6750.0, 8684.21052631579,
                               6176.470588235295, 0.0,
                               260, 4000,
                               11000.0, 9000.0, 7000.0,
                               3000,
                               39379.81481481482) == pytest.approx(47.91228954874287)
    # Variante O&M alternativo 8.000: be 149,49 (soglia minima).
    bc = _variante(om_alt=8000)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(149.48717045689756)
    # Variante senza riuniti: be 67,41.
    assert _variante(riuniti=0)["breakeven_gas_eur_mwh"] == pytest.approx(67.41210244863495)
    # Variante senza superficie ne' litri: denominatore gas nullo -> None.
    assert _variante(superficie_m2=0, litri_giorno_per_riunito=0)["breakeven_gas_eur_mwh"] is None
    # Variante numeratore negativo (elettricita' bassa, O&M alt zero): None.
    assert _variante(p_el=50, om_alt=0)["breakeven_gas_eur_mwh"] is None
    # Denominatore gas nullo diretto -> None.
    assert mh808_breakeven_gas(8800.0, 6750.0, 8684.21052631579,
                               6176.470588235295, 0.0,
                               260, 4000,
                               11000.0, 9000.0, 7000.0,
                               3000,
                               0) is None
    with pytest.raises(ValueError):
        mh808_breakeven_gas(8800.0, 6750.0, 8684.21, 6176.47, 0.0,
                            260, 4000,
                            11000.0, 9000.0, 7000.0,
                            3000,
                            -1)


def test_breakeven_verifica_pareggio():
    be = mh808_demo_calcoli()["breakeven_gas_eur_mwh"]
    assert be == pytest.approx(47.91228954874287)
    bc = _variante(p_gas=be)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert mh808_demo_calcoli()["gas_base_kwh_anno"] > 0.0


def test_breakeven_soglia_minima():
    bc_alto = _variante(p_gas=48.91228954874287)
    bc_basso = _variante(p_gas=46.0)
    assert bc_alto["c_alt_eur_anno"] < bc_alto["c_base_eur_anno"]
    assert bc_basso["c_alt_eur_anno"] > bc_basso["c_base_eur_anno"]
    # Sopra il breakeven il risparmio e' positivo ma
    # piccolo (39,38 EUR/anno): la VAN resta negativa
    # oltre la tolleranza, quindi NON_CONVIENTE
    # (il breakeven pareggia i costi, non la finanza).
    assert bc_alto["risparmio_eur_anno"] > 0.0
    assert bc_alto["verdetto"] == "NON_CONVIENTE"
    assert bc_basso["verdetto"] == "NON_CALCOLABILE"


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh808_flussi(20000, 2051.2043916982, 15)
    assert len(fl) == 16
    assert fl[0] == -20000
    assert all(f == 2051.2043916982 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh808_demo_calcoli()
    assert bc["van"] == pytest.approx(1290.8001522415523)
    assert mh808_van([-20000] + [2051.2043916982] * 15,
                     0) == pytest.approx(10768.065875473003)
    assert mh808_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh808_demo_calcoli()
    assert bc["tir"] == pytest.approx(5.940108156482945)
    assert mh808_tir([-20000] + [2051.2043916982] * 15) == \
        pytest.approx(0.05940108156482945)
    tir = mh808_tir([-20000] + [2051.2043916982] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-20000] + [2051.2043916982] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh808_payback([-20000] + [2051.2043916982] * 15) == 10
    assert mh808_payback([-20000] + [-1000.0] * 15) is None
    assert mh808_payback([0] + [2051.2043916982] * 15) == 0
    assert mh808_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh808_verdetto(2051.2043916982, 1290.8001522415523, 20000,
                          10.0) == "CONVIENTE"
    assert mh808_verdetto(1839.578836142644, -905.8007465651142, 20000,
                          10.0) == "MARGINALE"
    assert mh808_verdetto(1839.578836142644, -2000.0, 20000, 10.0) == "MARGINALE"
    assert mh808_verdetto(1839.578836142644, -2000.01, 20000, 10.0) == "NON_CONVIENTE"
    assert mh808_verdetto(2051.2043916982, 0.0, 20000, 10.0) == "MARGINALE"
    assert mh808_verdetto(0.0, 1290.80, 20000,
                          10.0) == "NON_CALCOLABILE"
    assert mh808_verdetto(-1948.7956083017998, -40227.83, 20000,
                          10.0) == "NON_CALCOLABILE"
    assert mh808_verdetto(None, 1290.80, 20000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh808_verdetto(float("nan"), 1290.80, 20000, 10.0)
    with pytest.raises(ValueError):
        mh808_verdetto(2051.2043916982, 1290.80, -1, 10.0)
    with pytest.raises(ValueError):
        mh808_verdetto(2051.2043916982, 1290.80, 20000, 100.1)


def test_valida_demo_ok():
    v = mh808_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("riuniti", "4"),
                       ("riuniti", float("nan")),
                       ("riuniti", float("inf")),
                       ("riuniti", True),
                       ("p_gas", None),
                       ("q_risc_per_m2", "110")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh808_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("superficie_m2", -10),
                          ("q_risc_per_m2", -10),
                          ("q_raff_per_m2", -10),
                          ("riuniti", -1),
                          ("giorni_anno", 0),
                          ("giorni_anno", 2.5),
                          ("litri_giorno_per_riunito", -1),
                          ("delta_t", 0),
                          ("delta_t", -5),
                          ("ore_giorno", -1),
                          ("p_comp_kw", -0.5),
                          ("f_scart", -0.1),
                          ("f_scart", 1.01),
                          ("eta_rec", -0.1),
                          ("eta_rec", 1.01),
                          ("cicli_giorno_per_riunito", -1),
                          ("e_aut_per_ciclo", -0.1),
                          ("fattore_comp_alt", 0),
                          ("fattore_comp_alt", 1.01),
                          ("fattore_aut_alt", 0),
                          ("fattore_aut_alt", 1.01),
                          ("eta_caldaia", 0),
                          ("eta_caldaia", 1.01),
                          ("cop_chiller", 1.0),
                          ("cop_chiller", 0.5),
                          ("cop_risc", 1.0),
                          ("cop_raff", 1.0),
                          ("cop_acs", 1.0),
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
        assert mh808_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"superficie_m2": 0,
              "q_risc_per_m2": 0,
              "q_raff_per_m2": 0,
              "riuniti": 0,
              "litri_giorno_per_riunito": 0,
              "ore_giorno": 0,
              "p_comp_kw": 0,
              "f_scart": 0,
              "eta_rec": 0,
              "cicli_giorno_per_riunito": 0,
              "e_aut_per_ciclo": 0,
              "p_gas": 0,
              "p_el": 0,
              "om_base": 0, "om_alt": 0,
              "capex": 0, "wacc_pct": 0,
              "f_gas": 0, "f_el": 0,
              "tolleranza_pct": 0})
    assert mh808_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["eta_rec"] = 1
    d["f_scart"] = 1
    d["riuniti"] = 4
    assert mh808_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh808_demo()
    assert d["superficie_m2"] == 300
    assert d["q_risc_per_m2"] == 110
    assert d["q_raff_per_m2"] == 70
    assert d["riuniti"] == 4
    assert d["giorni_anno"] == 250
    assert d["litri_giorno_per_riunito"] == 60
    assert d["delta_t"] == 35
    assert d["ore_giorno"] == 8
    assert d["p_comp_kw"] == 5.5
    assert d["f_scart"] == 0.85
    assert d["eta_rec"] == 0.50
    assert d["cicli_giorno_per_riunito"] == 6
    assert d["e_aut_per_ciclo"] == 1.5
    assert d["fattore_comp_alt"] == 0.80
    assert d["fattore_aut_alt"] == 0.75
    assert d["eta_caldaia"] == 0.90
    assert d["cop_chiller"] == 3.0
    assert d["cop_risc"] == 3.8
    assert d["cop_raff"] == 3.4
    assert d["cop_acs"] == 3.0
    assert d["p_gas"] == 100
    assert d["p_el"] == 260
    assert d["om_base"] == 3000
    assert d["om_alt"] == 4000
    assert d["capex"] == 20000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["f_gas"] == 0.20
    assert d["f_el"] == 0.35
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    bc = mh808_demo_calcoli()
    for chiave, atteso in _DEMO.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert got == pytest.approx(atteso, rel=1e-9), chiave
    assert bc["payback"] == 10
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True
    assert demo_calcoli()["van"] == bc["van"]


def test_demo_calcoli_fisica_economia():
    bc = mh808_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(13957.981481481482)
    assert bc["c_alt_eur_anno"] == pytest.approx(11906.777089783282)
    assert bc["risparmio_eur_anno"] == pytest.approx(2051.2043916982)
    assert bc["co2_base_t_anno"] == pytest.approx(17.32596296296296)
    assert bc["co2_alt_t_anno"] == pytest.approx(10.64373839009288)
    assert bc["co2_evitata_t_anno"] == pytest.approx(6.682224572870082)
    assert bc["cicli_anno"] == pytest.approx(6000.0)
    assert bc["q_risc_kwh_anno"] == pytest.approx(33000.0)
    assert bc["q_raff_kwh_anno"] == pytest.approx(21000.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(2441.8333333333335)
    assert bc["q_rec_pot_kwh_anno"] == pytest.approx(4675.0)
    assert bc["q_acs_net_kwh_anno"] == pytest.approx(0.0, abs=1e-12)


def test_demo_flussi_e_cumulato():
    bc = mh808_demo_calcoli()
    assert bc["flussi"][0] == -20000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(2051.2043916982) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -20000
    assert righe.iloc[9]["Cumulato (EUR)"] == pytest.approx(-1539.1604747161982)
    assert righe.iloc[10]["Cumulato (EUR)"] == pytest.approx(512.043916982002)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(10768.065875473003)


def test_demo_tabella_righe():
    bc = mh808_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Cicli autoclave all'anno"] == pytest.approx(6000.0)
    assert mappa["Riscaldamento (kWh_th/anno)"] == pytest.approx(33000.0)
    assert mappa["Raffrescamento (kWh_th/anno)"] == pytest.approx(21000.0)
    assert mappa["ACS (kWh_th/anno)"] == pytest.approx(2441.8333333333335)
    assert mappa["Elettricita' compressore base (kWh_e/anno)"] == pytest.approx(11000.0)
    assert mappa["Elettricita' compressore alt (kWh_e/anno)"] == pytest.approx(8800.0)
    assert mappa["Calore di scarto compressore (kWh_th/anno)"] == pytest.approx(9350.0)
    assert mappa["Recupero potenziale (kWh_th/anno)"] == pytest.approx(4675.0)
    assert mappa["Calore recuperato su ACS (kWh_th/anno)"] == pytest.approx(2441.8333333333335)
    assert mappa["ACS netta (kWh_th/anno)"] == pytest.approx(0.0, abs=1e-12)
    assert mappa["Elettricita' autoclave base (kWh_e/anno)"] == pytest.approx(9000.0)
    assert mappa["Elettricita' autoclave alt (kWh_e/anno)"] == pytest.approx(6750.0)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(39379.81481481482)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(13957.981481481482)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(11906.777089783282)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(2051.2043916982)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(6.682224572870082)
    assert mappa["Payback (anni)"] == 10
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] == pytest.approx(47.91228954874287)


def test_demo_coerenza_interna():
    bc = mh808_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["cicli_anno"] == pytest.approx(
        bc["riuniti"] * bc["cicli_giorno_per_riunito"]
        * bc["giorni_anno"])
    assert bc["litri_anno"] == pytest.approx(
        bc["riuniti"] * bc["litri_giorno_per_riunito"]
        * bc["giorni_anno"])
    assert bc["q_risc_kwh_anno"] == pytest.approx(
        bc["superficie_m2"] * bc["q_risc_per_m2"])
    assert bc["q_raff_kwh_anno"] == pytest.approx(
        bc["superficie_m2"] * bc["q_raff_per_m2"])
    assert bc["q_acs_kwh_anno"] == pytest.approx(
        bc["litri_anno"] * 4.186 * bc["delta_t"] / 3600.0)
    assert bc["e_comp_base_kwh_anno"] == pytest.approx(
        bc["giorni_anno"] * bc["ore_giorno"] * bc["p_comp_kw"])
    assert bc["e_comp_alt_kwh_anno"] == pytest.approx(
        bc["e_comp_base_kwh_anno"] * bc["fattore_comp_alt"])
    assert bc["q_scart_comp_kwh_anno"] == pytest.approx(
        bc["e_comp_base_kwh_anno"] * bc["f_scart"])
    assert bc["q_rec_pot_kwh_anno"] == pytest.approx(
        bc["q_scart_comp_kwh_anno"] * bc["eta_rec"])
    assert bc["q_rec_kwh_anno"] == pytest.approx(
        min(bc["q_acs_kwh_anno"], bc["q_rec_pot_kwh_anno"]))
    assert bc["q_acs_net_kwh_anno"] == pytest.approx(
        max(0.0, bc["q_acs_kwh_anno"] - bc["q_rec_kwh_anno"]))
    assert bc["e_aut_base_kwh_anno"] == pytest.approx(
        bc["cicli_anno"] * bc["e_aut_per_ciclo"])
    assert bc["e_aut_alt_kwh_anno"] == pytest.approx(
        bc["e_aut_base_kwh_anno"] * bc["fattore_aut_alt"])
    assert bc["gas_base_kwh_anno"] == pytest.approx(
        (bc["q_risc_kwh_anno"] + bc["q_acs_kwh_anno"])
        / bc["eta_caldaia"])
    assert bc["e_chiller_kwh_anno"] == pytest.approx(
        bc["q_raff_kwh_anno"] / bc["cop_chiller"])
    assert bc["e_pdc_risc_kwh_anno"] == pytest.approx(
        bc["q_risc_kwh_anno"] / bc["cop_risc"])
    assert bc["e_pdc_raff_kwh_anno"] == pytest.approx(
        bc["q_raff_kwh_anno"] / bc["cop_raff"])
    assert bc["e_pdc_acs_kwh_anno"] == pytest.approx(
        bc["q_acs_net_kwh_anno"] / bc["cop_acs"])
    assert bc["co2_evitata_t_anno"] == pytest.approx(
        bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])
    assert bc["c_base_eur_anno"] == pytest.approx(
        bc["gas_base_kwh_anno"] / 1000.0 * bc["p_gas"]
        + (bc["e_comp_base_kwh_anno"]
           + bc["e_aut_base_kwh_anno"]
           + bc["e_chiller_kwh_anno"]) / 1000.0 * bc["p_el"]
        + bc["om_base"])
    assert bc["c_alt_eur_anno"] == pytest.approx(
        (bc["e_comp_alt_kwh_anno"]
         + bc["e_aut_alt_kwh_anno"]
         + bc["e_pdc_risc_kwh_anno"]
         + bc["e_pdc_raff_kwh_anno"]
         + bc["e_pdc_acs_kwh_anno"])
        / 1000.0 * bc["p_el"]
        + bc["om_alt"])


def test_demo_contro_riconteggio_indipendente():
    sup, qri, qra = 300, 110, 70
    riu, gg, litg, dt = 4, 250, 60, 35
    ore, pco, fsc, ere = 8, 5.5, 0.85, 0.50
    cig, eau, fco, fau = 6, 1.5, 0.80, 0.75
    eta, copc, copr, copf, copa = 0.90, 3.0, 3.8, 3.4, 3.0
    pg, pel = 100, 260
    omb, oma, cx = 3000, 4000, 20000
    fg, fel, wacc, vita = 0.20, 0.35, 5.0, 15
    cia = riu * cig * gg
    qrisc = sup * qri
    qraff = sup * qra
    lita = riu * litg * gg
    qacs = lita * 4.186 * dt / 3600.0
    ecb = gg * ore * pco
    eca = ecb * fco
    qsca = ecb * fsc
    qrpo = qsca * ere
    qrec = min(qacs, qrpo)
    qnet = max(0.0, qacs - qrec)
    eab = cia * eau
    eaa = eab * fau
    gasb = (qrisc + qacs) / eta
    ech = qraff / copc
    epr = qrisc / copr
    epf = qraff / copf
    epa = qnet / copa
    cb = gasb / 1000.0 * pg + (ecb + eab + ech) / 1000.0 * pel + omb
    ca = (eca + eaa + epr + epf + epa) / 1000.0 * pel + oma
    risp = cb - ca
    co2b = gasb / 1000.0 * fg + (ecb + eab + ech) / 1000.0 * fel
    co2a = (eca + eaa + epr + epf + epa) / 1000.0 * fel
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    be = (((eca + eaa + epr + epf + epa) / 1000.0 * pel + oma
           - (ecb + eab + ech) / 1000.0 * pel - omb)
          / (gasb / 1000.0))
    bc = mh808_demo_calcoli()
    assert bc["cicli_anno"] == pytest.approx(cia)
    assert bc["q_risc_kwh_anno"] == pytest.approx(qrisc)
    assert bc["q_raff_kwh_anno"] == pytest.approx(qraff)
    assert bc["litri_anno"] == pytest.approx(lita)
    assert bc["q_acs_kwh_anno"] == pytest.approx(qacs)
    assert bc["e_comp_base_kwh_anno"] == pytest.approx(ecb)
    assert bc["e_comp_alt_kwh_anno"] == pytest.approx(eca)
    assert bc["q_scart_comp_kwh_anno"] == pytest.approx(qsca)
    assert bc["q_rec_pot_kwh_anno"] == pytest.approx(qrpo)
    assert bc["q_rec_kwh_anno"] == pytest.approx(qrec)
    assert bc["q_acs_net_kwh_anno"] == pytest.approx(qnet)
    assert bc["e_aut_base_kwh_anno"] == pytest.approx(eab)
    assert bc["e_aut_alt_kwh_anno"] == pytest.approx(eaa)
    assert bc["gas_base_kwh_anno"] == pytest.approx(gasb)
    assert bc["e_chiller_kwh_anno"] == pytest.approx(ech)
    assert bc["e_pdc_risc_kwh_anno"] == pytest.approx(epr)
    assert bc["e_pdc_raff_kwh_anno"] == pytest.approx(epf)
    assert bc["e_pdc_acs_kwh_anno"] == pytest.approx(epa)
    assert bc["c_base_eur_anno"] == pytest.approx(cb)
    assert bc["c_alt_eur_anno"] == pytest.approx(ca)
    assert bc["risparmio_eur_anno"] == pytest.approx(risp)
    assert bc["co2_base_t_anno"] == pytest.approx(co2b)
    assert bc["co2_alt_t_anno"] == pytest.approx(co2a)
    assert bc["co2_evitata_t_anno"] == pytest.approx(co2)
    assert bc["van"] == pytest.approx(van)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(be)


# ---------------------------------------------------------------- varianti
def test_variante_recupero_non_saturato():
    # eta_rec 0,05: potenziale 467,50 sotto l'ACS
    # -> NON satura, ACS netta positiva, MARGINALE.
    bc = _variante(eta_rec=0.05)
    assert bc["q_rec_pot_kwh_anno"] == pytest.approx(467.5)
    assert bc["q_rec_kwh_anno"] == pytest.approx(467.5)
    assert bc["q_acs_net_kwh_anno"] == pytest.approx(1974.3333333333335)
    assert bc["e_pdc_acs_kwh_anno"] == pytest.approx(658.1111111111112)
    assert bc["risparmio_eur_anno"] == pytest.approx(1880.0955028093122)
    assert bc["van"] == pytest.approx(-485.25160171814434)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(52.25738080154674)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"


def test_variante_recupero_parziale_e_senza():
    bc = _variante(eta_rec=0.10)
    assert bc["q_rec_kwh_anno"] == pytest.approx(935.0)
    assert bc["q_acs_net_kwh_anno"] == pytest.approx(1506.8333333333335)
    assert bc["e_pdc_acs_kwh_anno"] == pytest.approx(502.2777777777778)
    assert bc["risparmio_eur_anno"] == pytest.approx(1920.6121694759786)
    assert bc["van"] == pytest.approx(-64.702456871197)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"
    bc0 = _variante(eta_rec=0)
    assert bc0["q_rec_kwh_anno"] == 0.0
    assert bc0["q_acs_net_kwh_anno"] == pytest.approx(2441.8333333333335)
    assert bc0["e_pdc_acs_kwh_anno"] == pytest.approx(813.9444444444445)
    assert bc0["risparmio_eur_anno"] == pytest.approx(1839.578836142644)
    assert bc0["van"] == pytest.approx(-905.8007465651142)
    assert bc0["breakeven_gas_eur_mwh"] == pytest.approx(53.286249699412295)
    assert bc0["payback"] == 11
    assert bc0["verdetto"] == "MARGINALE"


def test_variante_gas_zero_helper_non_calcolabile_come_ui():
    # Negli helper p_gas = 0 e' ammesso e qui il
    # risparmio e' NEGATIVO (-1.886,78 EUR/anno):
    # verdetto NON_CALCOLABILE anche negli helper,
    # quindi NESSUNA divergenza di verdetto con
    # la guard UI (prezzi <= 0), che lo
    # intercetta prima (diversa dalla scheda
    # lavanderia, dove gas zero restava
    # CONVIENTE negli helper).
    bc = _variante(p_gas=0)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(-1886.7770897832816)
    assert bc["van"] == pytest.approx(-39584.10098622402)
    assert bc["payback"] is None
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(47.91228954874287)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_breakeven_none_numeratore_negativo():
    # p_el 50 e O&M alt zero: numeratore negativo
    # -> breakeven None (a prezzo gas zero
    # l'alternativa e' gia' piu' conveniente).
    bc = _variante(p_el=50, om_alt=0)
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["risparmio_eur_anno"] == pytest.approx(6767.447425753928)
    assert bc["van"] == pytest.approx(50243.7900706913)
    assert bc["payback"] == 3
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_breakeven_none_denominatore_nullo():
    # S = 0 e litri = 0: nessun gas baseline ->
    # breakeven None.
    bc = _variante(superficie_m2=0, litri_giorno_per_riunito=0)
    assert bc["gas_base_kwh_anno"] == 0.0
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["risparmio_eur_anno"] == pytest.approx(157.0)
    assert bc["van"] == pytest.approx(-18370.39368800565)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_riuniti_piccoli_e_grandi():
    bc = _variante(riuniti=2)
    assert bc["cicli_anno"] == pytest.approx(3000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(1623.0469842907914)
    assert bc["van"] == pytest.approx(-3153.3273231613202)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(57.31434373631001)
    assert bc["payback"] == 13
    assert bc["verdetto"] == "NON_CONVIENTE"
    bc2 = _variante(riuniti=8)
    assert bc2["risparmio_eur_anno"] == pytest.approx(2889.4347620685694)
    assert bc2["van"] == pytest.approx(9991.344753903448)
    assert bc2["breakeven_gas_eur_mwh"] == pytest.approx(31.355871417012267)
    assert bc2["payback"] == 7
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_capex_conviente():
    bc = _variante(capex=40000)
    assert bc["risparmio_eur_anno"] == pytest.approx(2051.2043916982)
    assert bc["van"] == pytest.approx(-18709.199847758453)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    # Negli helper CAPEX = 0 e' CONVIENTE (VAN
    # positiva, TIR None, payback 0); in UI e'
    # guard degenere (NON_CALCOLABILE): divergenza
    # documentata, vedi test_ui_guard_degenere_stretta.
    bc = _variante(capex=0)
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(21290.80015224155, rel=1e-6)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(10768.065875473003)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(-4161.143401726725)
    assert bc2["payback"] == 10
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_el_alto_e_om_alt_alto():
    bc = _variante(p_el=400)
    assert bc["risparmio_eur_anno"] == pytest.approx(1573.709035661048)
    assert bc["van"] == pytest.approx(-3665.438358243377)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(60.03767302966054)
    assert bc["payback"] == 13
    assert bc["verdetto"] == "NON_CONVIENTE"
    bc2 = _variante(om_alt=8000)
    assert bc2["risparmio_eur_anno"] == pytest.approx(-1948.7956083017998)
    assert bc2["breakeven_gas_eur_mwh"] == pytest.approx(149.48717045689756)
    assert bc2["payback"] is None
    assert bc2["verdetto"] == "NON_CALCOLABILE"


def test_variante_senza_riuniti_non_convinte_helper():
    # Negli helper riuniti = 0 resta calcolabile
    # (risparmio positivo, VAN negativa, verdetto
    # NON_CONVIENTE); in UI e' guard degenere
    # (riuniti <= 0): divergenza documentata.
    bc = _variante(riuniti=0)
    assert bc["cicli_anno"] == 0.0
    assert bc["e_aut_base_kwh_anno"] == 0.0
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(1194.8895768833845)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(67.41210244863495)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_cop_risc_basso():
    bc = _variante(cop_risc=2.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(19.099128540305173)
    assert bc["van"] == pytest.approx(-19801.75757692438)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(99.51500207326725)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_monotonia_prezzo_gas_crescente():
    base = mh808_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas=101)["risparmio_eur_anno"]
    basso = _variante(p_gas=99)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(39.37981481481482, abs=1e-2)
    assert base - basso == pytest.approx(39.37981481481482, abs=1e-2)


def test_monotonia_riuniti_crescente():
    assert _variante(riuniti=2)["risparmio_eur_anno"] < \
        mh808_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(riuniti=8)["risparmio_eur_anno"] > \
        mh808_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(riuniti=8)["cicli_anno"] == \
        pytest.approx(12000.0)


def test_demo_deterministica_due_chiamate():
    a = mh808_demo_calcoli()
    b = mh808_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh808_demo().keys()) == {
        "superficie_m2", "q_risc_per_m2", "q_raff_per_m2",
        "riuniti", "giorni_anno",
        "litri_giorno_per_riunito", "delta_t",
        "ore_giorno", "p_comp_kw", "f_scart", "eta_rec",
        "cicli_giorno_per_riunito", "e_aut_per_ciclo",
        "fattore_comp_alt", "fattore_aut_alt",
        "eta_caldaia", "cop_chiller", "cop_risc",
        "cop_raff", "cop_acs",
        "p_gas", "p_el",
        "om_base", "om_alt",
        "capex", "wacc_pct", "vita_anni",
        "f_gas", "f_el",
        "tolleranza_pct"}


# ---------------------------------------------------------------- degenere
def test_degenere_cop_uguale_uno_sollevela():
    with pytest.raises(ValueError):
        _variante(cop_chiller=1.0)
    with pytest.raises(ValueError):
        _variante(cop_risc=1.0)
    with pytest.raises(ValueError):
        _variante(cop_raff=1.0)
    with pytest.raises(ValueError):
        _variante(cop_acs=1.0)


def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"superficie_m2": -10},
               {"q_risc_per_m2": -10},
               {"q_raff_per_m2": -10},
               {"riuniti": -1},
               {"giorni_anno": 0},
               {"giorni_anno": 2.5},
               {"litri_giorno_per_riunito": -1},
               {"delta_t": 0}, {"delta_t": -5},
               {"ore_giorno": -1},
               {"p_comp_kw": -0.5},
               {"f_scart": -0.1}, {"f_scart": 1.01},
               {"eta_rec": -0.1}, {"eta_rec": 1.01},
               {"cicli_giorno_per_riunito": -1},
               {"e_aut_per_ciclo": -0.1},
               {"fattore_comp_alt": 0}, {"fattore_comp_alt": 1.01},
               {"fattore_aut_alt": 0}, {"fattore_aut_alt": 1.01},
               {"eta_caldaia": 0}, {"eta_caldaia": 1.01},
               {"cop_chiller": 1.0}, {"cop_chiller": 0.5},
               {"cop_risc": 1.0}, {"cop_risc": 0.5},
               {"cop_raff": 1.0},
               {"cop_acs": 1.0},
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
        assert mh808_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"riuniti": "4"},
               {"riuniti": float("nan")},
               {"p_gas": float("inf")},
               {"capex": True},
               {"q_risc_per_m2": "110"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh808_valida(**d)["valido"] is False


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    for kw in ({"om_alt": 8000},
               {"p_gas": 0}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] <= 0.0
        assert bc["verdetto"] == "NON_CALCOLABILE"
        assert bc["flussi"]


def test_pareggio_esatto_tolleranza_float():
    # A pareggio esatto (prezzo gas = breakeven
    # demo) il risparmio e' zero (circa 0.0,
    # quindi guard NON_CALCOLABILE): in nessun
    # caso CONVIENTE.
    be = mh808_demo_calcoli()["breakeven_gas_eur_mwh"]
    bc = _variante(p_gas=be)
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["verdetto"] != "CONVIENTE"
    bc2 = _variante(p_gas=be + 1)
    assert bc2["risparmio_eur_anno"] == pytest.approx(39.37981481481482, abs=1e-2)
    # Risparmio positivo ma piccolo: VAN negativa oltre
    # la tolleranza, quindi NON_CONVIENTE (non CONVIENTE).
    assert bc2["verdetto"] == "NON_CONVIENTE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh808_demo_calcoli()
    testo = mh808_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_gas_eur_mwh" in testo
    assert "co2_evitata_t_anno" in testo
    assert "q_rec_kwh_anno" in testo
    assert "q_rec_pot_kwh_anno" in testo
    assert "riuniti" in testo
    assert "cicli_giorno_per_riunito" in testo
    assert "e_aut_alt_kwh_anno" in testo
    assert "e_comp_alt_kwh_anno" in testo
    assert "q_acs_net_kwh_anno" in testo
    assert "e_pdc_risc_kwh_anno" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh808_demo_calcoli()
    testo = mh808_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"cicli_anno;{bc['cicli_anno']}" in testo
    assert f"gas_base_kwh_anno;{bc['gas_base_kwh_anno']}" in testo
    assert f"q_risc_kwh_anno;{bc['q_risc_kwh_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh808_demo_calcoli()
    testo = mh808_csv(bc, _demo_kwargs())
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
    return ["mh" + "80" + "7", "st" + "80" + "7",
            "tab" + "80" + "7", "w" + "80" + "8",
            "mh" + "80" + "6", "tab" + "80" + "6"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w809_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w809_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab808:")


def test_ui_apre_scheda_attesa_una_volta():
    """Il frammento UI apre la scheda attesa, una sola volta."""
    src = _leggi("w809_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert m.group(1) == "808"
    assert src.count("with tab808:") == 1


def test_ui_titolo_atteso():
    src = _leggi("w809_ui.py")
    titolo = ("Studio dentistico: pompa di calore + recupero "
              "calore compressore su ACS + autoclave "
              "efficiente batte caldaia a gas + chiller + "
              "autoclave tradizionale?")
    assert src.count(titolo) == 2


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w809_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w809_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st808_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) >= 28
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w809_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 4
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_ui_guard_degenere_stretta():
    """La guard UI della scheda dichiara NON_CALCOLABILE
    anche per riuniti <= 0, superficie <= 0, prezzi
    <= 0 e CAPEX <= 0 (piu' stretta degli helper,
    che ammettono lo zero)."""
    src = _leggi("w809_ui.py")
    assert "float(_riu808) <= 0.0" in src
    assert "float(_sup808) <= 0.0" in src
    assert "float(_pg808) <= 0.0" in src
    assert "float(_pel808) <= 0.0" in src
    assert "float(_cx808) <= 0.0" in src
    assert "int(_vita808) <= 0" in src
    assert "Verdetto: NON_CALCOLABILE" in src


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w809_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def808[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w809_ui.py")
        usate = set(re.findall(r'_def808\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 30
        assert usate <= set(mh808_demo().keys())
