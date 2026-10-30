"""Test nuova scheda "Clinica veterinaria: pompa
di calore + recupero calore ventilazione sale
operatorie batte caldaia a gas + chiller +
autoclave tradizionale?" (titolo completo nel
frammento UI). Contenuto pronto da scrivere in
repo come test della scheda clinica veterinaria.

Business case deterministico di una clinica
veterinaria guidato dai M2 DI SUPERFICIE e dai
GIORNI DI APERTURA ALL'ANNO: i m2 guidano
riscaldamento e raffrescamento, i giorni
guidano l'anno, eta_rec e f_vent guidano il
recupero di calore dalla ventilazione delle
sale operatorie e della degenza, cicli al
giorno x kWh per ciclo x giorni guidano
l'autoclave, numero x kWh all'anno guidano i
frigoriferi farmaci, kg al giorno x giorni x
kWh per kg guidano la lavanderia, litri al
giorno x giorni x 4,186 x delta_T / 3600
guidano l'ACS.
Riscaldamento = S x q_risc; raffrescamento =
S x q_raff; recupero ventilazione = eta_rec x
f_vent x Q_risc; riscaldamento netto = Q_risc
- recupero; ACS = litri_giorno x giorni x
4,186 x delta_T / 3600; autoclave base =
cicli x giorni x kWh ciclo e alt = base x
0,85 (letterale); frigoriferi base = n_frigo x
kWh base e alt = n_frigo x kWh alt; lavanderia
base = kg x giorni x kWh per kg e alt = base x
0,55 (letterale); gas baseline = (riscaldamento
+ ACS) / 0,90 (eta_caldaia letterale, senza
recupero); chiller = raffrescamento / 3,0;
E_base = chiller + autoclave base + frigoriferi
base + lavanderia base; E_pdc = riscaldamento
netto / 3,4 + raffrescamento / 3,2 + ACS / 3,0
(COP letterali); E_alt = E_pdc + autoclave alt
+ frigoriferi alt + lavanderia alt; C_base =
gas_base / 1000 x p_gas + E_base / 1000 x p_el
+ O&M_base; C_alt = E_alt / 1000 x p_el +
O&M_alt (niente gas: l'alternativa non ha
caldaia); risparmio = C_base - C_alt; CO2
evitata = (gas_base x 0,20 + E_base x 0,35 -
E_alt x 0,35) / 1000 (fattori letterali);
flussi [-CAPEX, risparmio x vita]; VAN, TIR,
payback (primo anno con cumulato >= 0);
breakeven gas = (C_alt - O&M_base - E_base /
1000 x p_el) x 1000 / gas_base EUR/MWh, None
se gas_base <= 0 o numeratore < 0, SOGLIA
MINIMA quando esiste.
Verdetto: NON_CALCOLABILE se input degenere
(superficie <= 0, giorni <= 0, carichi <= 0,
eta_rec o f_vent fuori [0, 1], delta_T <= 0,
litri, cicli, kWh ciclo, frigoriferi, kWh
frigorifero, kg o energia per kg negativi,
prezzi <= 0, CAPEX <= 0, vita <= 0) o se
risparmio <= 0 (guard degenere: UI salta KPI,
grafico, tabella e CSV); altrimenti CONVIENTE
se VAN > 0, MARGINALE se VAN negativa entro
tolleranza % del CAPEX, NON_CONVIENTE se VAN
negativa oltre la tolleranza. Differenze
UI-vs-helper documentate: S = 0 e' calcolabile
negli helper (risparmio 864,26 EUR/anno, VAN
-21.029,31 EUR, verdetto NON_CONVIENTE,
breakeven 20,36 EUR/MWh) ma bloccato dalla
guard UI (NON_CALCOLABILE): DIVERGENZA di
verdetto; CAPEX = 0 e' CONVIENTE negli helper
(VAN positiva, TIR None, payback 0) ma bloccato
dalla guard UI; prezzi = 0 sono ammessi negli
helper ma bloccati dalla guard UI (p_el = 0
resta CONVIENTE negli helper, p_gas = 0 da'
invece risparmio NEGATIVO negli helper,
-2.648,18 EUR/anno, verdetto NON_CALCOLABILE:
per gas zero QUI NON c'e' divergenza di
verdetto helper-vs-UI, solo guard prima);
carichi = 0 sono calcolabili negli helper
(stessi KPI di S = 0) ma bloccati dalla guard
UI.
Distinzione esplicita: distinto dal centro
estetico / SPA (cabine, saune, hammam, vasca
idromassaggio e docce: qui nessuna cabina,
nessuna sauna, nessuno hammam, nessuna vasca,
l'ACS e' quella di lavaggi, pulizie e servizi
della clinica, con autoclave, frigoriferi
farmaci e lavanderia lettiere), dall'ospedale
(posti letto e reparti di degenza umana: qui
nessun posto letto umano, nessun reparto
ospedaliero, il recupero e' quello della
ventilazione delle sale operatorie veterinarie
e della degenza animali), dal laboratorio
(cappe e strumenti analitici: qui nessuna
cappa, nessuno strumento analitico, il carico
caratteristico e' autoclave + frigoriferi
farmaci + lavanderia lettiere): qui driver M2
+ GIORNI + VENTILAZIONE + AUTOCLAVE +
FRIGORIFERI + LAVANDERIA + ACS.

Demo (clinica veterinaria): superficie 400 m2
per 300 giorni di apertura all'anno, 110
kWh_th/m2 di riscaldamento (44.000
kWh_th/anno) e 60 kWh_th/m2 di raffrescamento
(24.000 kWh_th/anno), rendimento di recupero
0,60 e frazione di ventilazione 0,40 (recupero
10.560 kWh_th/anno, riscaldamento netto 33.440
kWh_th/anno), ACS 800 litri al giorno con
delta_T 35 K (240.000 litri all'anno,
9.767,333... kWh_th/anno), autoclave 5 cicli al
giorno da 3,0 kWh per ciclo (4.500 kWh_e/anno
base, 3.825 alt con fattore 0,85), 3 frigoriferi
farmaci da 2.500 kWh all'anno base (7.500
kWh_e/anno base, 5.400 alt da 1.800 kWh
all'anno), lavanderia 40 kg al giorno da 1,0
kWh_e/kg (12.000 kg all'anno, 12.000
kWh_e/anno base, 6.600 alt con fattore 0,55),
gas 100, el 260 EUR/MWh, O&M base 4.000, alt
5.500, CAPEX 30.000, WACC 5 %, vita 15,
tolleranza 10 % del CAPEX. Valori calcolati
eseguendo mh810_demo_calcoli():
Q_risc 44.000, Q_raff 24.000, Q_vent_rec
10.560, Q_risc_net 33.440, Q_acs
9.767,333333333334, E_auto_base 4.500,
E_auto_alt 3.825, E_frigo_base 7.500,
E_frigo_alt 5.400, E_lav_base 12.000,
E_lav_alt 6.600, gas_base 59.741,48148148148,
E_chiller 8.000, E_pdc 20.591,071895424837,
E_base 32.000, E_alt 36.416,07189542484,
C_base 18.294,148148148146, C_alt
14.968,178692810458, risparmio
3.325,9694553376885, CO2_base
23,148296296296298, CO2_alt 12,745625163398692,
CO2_evitata 10,402671132897607, VAN
4.522,425591838961, TIR 7,154094804690368 %,
payback 10, breakeven gas 44,32730202098074
EUR/MWh (soglia minima), verdetto CONVIENTE.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w811_helpers import (
    demo_calcoli,
    mh810_breakeven_gas,
    mh810_c_alt,
    mh810_c_base,
    mh810_calcola,
    mh810_co2_alt,
    mh810_co2_base,
    mh810_co2_evitata,
    mh810_cop,
    mh810_csv,
    mh810_demo,
    mh810_demo_calcoli,
    mh810_e_alt,
    mh810_e_auto_alt,
    mh810_e_auto_base,
    mh810_e_base,
    mh810_e_chiller,
    mh810_e_frigo_alt,
    mh810_e_frigo_base,
    mh810_e_lav_alt,
    mh810_e_lav_base,
    mh810_e_pdc,
    mh810_flussi,
    mh810_frazione,
    mh810_gas_base,
    mh810_int_pos,
    mh810_num,
    mh810_nneg,
    mh810_payback,
    mh810_pct_tolleranza,
    mh810_pos,
    mh810_pct_wacc,
    mh810_q_acs,
    mh810_q_raff,
    mh810_q_risc,
    mh810_q_risc_net,
    mh810_q_vent_rec,
    mh810_risparmio,
    mh810_tir,
    mh810_valida,
    mh810_van,
    mh810_verdetto,
)

_DEMO = {
    "q_risc_kwh_anno": 44000.0,
    "q_raff_kwh_anno": 24000.0,
    "q_vent_rec_kwh_anno": 10560.0,
    "q_risc_net_kwh_anno": 33440.0,
    "q_acs_kwh_anno": 9767.333333333334,
    "e_auto_base_kwh_anno": 4500.0,
    "e_auto_alt_kwh_anno": 3825.0,
    "e_frigo_base_kwh_anno": 7500.0,
    "e_frigo_alt_kwh_anno": 5400.0,
    "e_lav_base_kwh_anno": 12000.0,
    "e_lav_alt_kwh_anno": 6600.000000000001,
    "gas_base_kwh_anno": 59741.48148148148,
    "e_chiller_kwh_anno": 8000.0,
    "e_pdc_kwh_anno": 20591.071895424837,
    "e_base_kwh_anno": 32000.0,
    "e_alt_kwh_anno": 36416.07189542484,
    "c_base_eur_anno": 18294.148148148146,
    "c_alt_eur_anno": 14968.178692810458,
    "risparmio_eur_anno": 3325.9694553376885,
    "co2_base_t_anno": 23.148296296296298,
    "co2_alt_t_anno": 12.745625163398692,
    "co2_evitata_t_anno": 10.402671132897607,
    "van": 4522.425591838961,
    "tir": 7.154094804690368,
    "breakeven_gas_eur_mwh": 44.32730202098074,
}


def _demo_kwargs():
    return dict(mh810_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh810_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh810_num(3, "x") == 3.0
    assert mh810_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh810_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh810_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh810_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh810_pos(0, "x")
    with pytest.raises(ValueError):
        mh810_pos(-1, "x")
    assert mh810_pos(0.5, "x") == 0.5


def test_cop_maggiore_di_uno():
    assert mh810_cop(3.0, "x") == 3.0
    with pytest.raises(ValueError):
        mh810_cop(1.0, "x")
    with pytest.raises(ValueError):
        mh810_cop(0.5, "x")


def test_frazione_limiti():
    assert mh810_frazione(0, "x") == 0.0
    assert mh810_frazione(1, "x") == 1.0
    assert mh810_frazione(0.60, "x") == 0.60
    assert mh810_frazione(0.40, "x") == 0.40
    with pytest.raises(ValueError):
        mh810_frazione(-0.01, "x")
    with pytest.raises(ValueError):
        mh810_frazione(1.01, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh810_int_pos(5.0, "x") == 5
    assert mh810_int_pos(300.0, "x") == 300
    with pytest.raises(ValueError):
        mh810_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh810_int_pos(0, "x")


def test_pct_wacc_limiti():
    assert mh810_pct_wacc(0, "x") == 0.0
    assert mh810_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh810_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh810_pct_tolleranza(0, "x") == 0.0
    assert mh810_pct_tolleranza(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh810_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh810_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_q_risc_raff_vent_rec_net():
    assert mh810_q_risc(400, 110) == 44000.0
    assert mh810_q_raff(400, 60) == 24000.0
    assert mh810_q_risc(0, 110) == 0.0
    with pytest.raises(ValueError):
        mh810_q_risc(-1, 110)
    assert mh810_q_vent_rec(44000.0, 0.60, 0.40) == pytest.approx(10560.0)
    assert mh810_q_vent_rec(44000.0, 0, 0.40) == 0.0
    assert mh810_q_vent_rec(44000.0, 1, 1) == pytest.approx(44000.0)
    assert mh810_q_risc_net(44000.0, 10560.0) == pytest.approx(33440.0)
    assert mh810_q_risc_net(44000.0, 44000.0) == 0.0
    with pytest.raises(ValueError):
        mh810_q_vent_rec(44000.0, 1.01, 0.40)
    with pytest.raises(ValueError):
        mh810_q_vent_rec(44000.0, 0.60, -0.1)


def test_q_acs():
    assert mh810_q_acs(800, 300, 35) == pytest.approx(9767.333333333334)
    assert mh810_q_acs(0, 300, 35) == 0.0
    with pytest.raises(ValueError):
        mh810_q_acs(-1, 300, 35)
    with pytest.raises(ValueError):
        mh810_q_acs(800, 300, 0)
    with pytest.raises(ValueError):
        mh810_q_acs(800, 0, 35)


def test_autoclave_frigo_lavanderia():
    assert mh810_e_auto_base(5, 300, 3.0) == 4500.0
    assert mh810_e_auto_base(0, 300, 3.0) == 0.0
    assert mh810_e_auto_alt(4500.0) == pytest.approx(3825.0)
    assert mh810_e_auto_alt(0.0) == 0.0
    with pytest.raises(ValueError):
        mh810_e_auto_base(-1, 300, 3.0)
    assert mh810_e_frigo_base(3, 2500) == 7500.0
    assert mh810_e_frigo_alt(3, 1800) == 5400.0
    assert mh810_e_frigo_base(0, 2500) == 0.0
    with pytest.raises(ValueError):
        mh810_e_frigo_base(3, -1)
    assert mh810_e_lav_base(40, 300, 1.0) == 12000.0
    assert mh810_e_lav_alt(12000.0) == pytest.approx(6600.0)
    with pytest.raises(ValueError):
        mh810_e_lav_base(-1, 300, 1.0)


def test_gas_chiller_pdc_e_totali():
    assert mh810_gas_base(44000.0, 9767.333333333334) == pytest.approx(59741.48148148148)
    assert mh810_gas_base(0, 0) == 0.0
    with pytest.raises(ValueError):
        mh810_gas_base(-1, 9767.33)
    assert mh810_e_chiller(24000.0) == pytest.approx(8000.0)
    assert mh810_e_pdc(33440.0, 24000.0, 9767.333333333334) == pytest.approx(20591.071895424837)
    assert mh810_e_pdc(0.0, 0.0, 0.0) == 0.0
    assert mh810_e_base(8000.0, 4500.0, 7500.0, 12000.0) == pytest.approx(32000.0)
    assert mh810_e_alt(20591.071895424837, 3825.0, 5400.0,
                       6600.000000000001) == pytest.approx(36416.07189542484)


def test_c_base_c_alt_scomposizione():
    assert mh810_c_base(59741.48148148148, 100, 32000.0, 260,
                        4000) == pytest.approx(18294.148148148146)
    assert mh810_c_base(59741.48148148148, 0, 32000.0, 260,
                        4000) == pytest.approx(12320.0)
    assert mh810_c_alt(36416.07189542484, 260,
                       5500) == pytest.approx(14968.178692810458)
    with pytest.raises(ValueError):
        mh810_c_base(59741.48, 100, 32000.0, 260, -1)
    with pytest.raises(ValueError):
        mh810_c_alt(36416.07, 260, -1)


def test_risparmio_segno():
    assert mh810_risparmio(18294.148148148146, 14968.178692810458) == pytest.approx(3325.9694553376885)
    assert mh810_risparmio(14968.18, 14968.18) == pytest.approx(0.0, abs=1e-9)


def test_co2_base_alt_evitata():
    assert mh810_co2_base(59741.48148148148, 32000.0) == pytest.approx(23.148296296296298)
    assert mh810_co2_alt(36416.07189542484) == pytest.approx(12.745625163398692)
    assert mh810_co2_evitata(59741.48148148148, 32000.0,
                             36416.07189542484) == pytest.approx(10.402671132897607)
    assert mh810_co2_base(0, 0) == 0.0
    assert mh810_co2_alt(0) == 0.0
    with pytest.raises(ValueError):
        mh810_co2_base(59741.48, -1)
    with pytest.raises(ValueError):
        mh810_co2_alt(-1)


def test_breakeven_demo_e_varianti():
    assert mh810_demo_calcoli()["breakeven_gas_eur_mwh"] == pytest.approx(44.32730202098074)
    assert mh810_breakeven_gas(36416.07189542484,
                               260, 5500,
                               32000.0,
                               4000,
                               59741.48148148148) == pytest.approx(44.32730202098074)
    bc = _variante(om_alt=10000)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(119.65184852381391)
    assert _variante(superficie_m2=0)["breakeven_gas_eur_mwh"] == pytest.approx(20.364002457170088)
    assert _variante(superficie_m2=0, litri_giorno=0)["breakeven_gas_eur_mwh"] is None
    assert mh810_breakeven_gas(36416.07189542484,
                               260, 5500,
                               32000.0,
                               4000,
                               0) is None
    with pytest.raises(ValueError):
        mh810_breakeven_gas(36416.07, 260, 5500, 32000.0, 4000, -1)


def test_breakeven_verifica_pareggio():
    be = mh810_demo_calcoli()["breakeven_gas_eur_mwh"]
    assert be == pytest.approx(44.32730202098074)
    bc = _variante(p_gas=be)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert mh810_demo_calcoli()["gas_base_kwh_anno"] > 0.0


def test_breakeven_soglia_minima():
    bc_alto = _variante(p_gas=45.32730202098074)
    bc_basso = _variante(p_gas=43.0)
    assert bc_alto["c_alt_eur_anno"] < bc_alto["c_base_eur_anno"]
    assert bc_basso["c_alt_eur_anno"] > bc_basso["c_base_eur_anno"]
    assert bc_alto["risparmio_eur_anno"] > 0.0
    assert bc_alto["verdetto"] == "NON_CONVIENTE"
    assert bc_basso["verdetto"] == "NON_CALCOLABILE"


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh810_flussi(30000, 3325.9694553376885, 15)
    assert len(fl) == 16
    assert fl[0] == -30000
    assert all(f == 3325.9694553376885 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh810_demo_calcoli()
    assert bc["van"] == pytest.approx(4522.425591838961)
    assert mh810_van([-30000] + [3325.9694553376885] * 15,
                     0) == pytest.approx(19889.541830065333)
    assert mh810_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh810_demo_calcoli()
    assert bc["tir"] == pytest.approx(7.154094804690368)
    assert mh810_tir([-30000] + [3325.9694553376885] * 15) == \
        pytest.approx(0.07154094804690368)
    tir = mh810_tir([-30000] + [3325.9694553376885] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-30000] + [3325.9694553376885] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh810_payback([-30000] + [3325.9694553376885] * 15) == 10
    assert mh810_payback([-30000] + [-1000.0] * 15) is None
    assert mh810_payback([0] + [3325.9694553376885] * 15) == 0
    assert mh810_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh810_verdetto(3325.9694553376885, 4522.425591838961, 30000,
                          10.0) == "CONVIENTE"
    assert mh810_verdetto(3325.9694553376885, -1500.0, 30000,
                          10.0) == "MARGINALE"
    assert mh810_verdetto(3325.9694553376885, -3000.0, 30000, 10.0) == "MARGINALE"
    assert mh810_verdetto(3325.9694553376885, -3000.01, 30000, 10.0) == "NON_CONVIENTE"
    assert mh810_verdetto(3325.9694553376885, 0.0, 30000, 10.0) == "MARGINALE"
    assert mh810_verdetto(0.0, 4522.43, 30000,
                          10.0) == "NON_CALCOLABILE"
    assert mh810_verdetto(-2648.1786928104575, -57487.19, 30000,
                          10.0) == "NON_CALCOLABILE"
    assert mh810_verdetto(None, 4522.43, 30000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh810_verdetto(float("nan"), 4522.43, 30000, 10.0)
    with pytest.raises(ValueError):
        mh810_verdetto(3325.9694553376885, 4522.43, -1, 10.0)
    with pytest.raises(ValueError):
        mh810_verdetto(3325.9694553376885, 4522.43, 30000, 100.1)


def test_valida_demo_ok():
    v = mh810_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("superficie_m2", "400"),
                       ("superficie_m2", float("nan")),
                       ("superficie_m2", float("inf")),
                       ("superficie_m2", True),
                       ("p_gas", None),
                       ("q_risc_per_m2", "110")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh810_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("superficie_m2", -10),
                          ("q_risc_per_m2", -10),
                          ("q_raff_per_m2", -10),
                          ("giorni_anno", 0),
                          ("giorni_anno", 2.5),
                          ("eta_rec", -0.1),
                          ("eta_rec", 1.01),
                          ("f_vent", -0.1),
                          ("f_vent", 1.01),
                          ("litri_giorno", -1),
                          ("delta_t", 0),
                          ("delta_t", -5),
                          ("cicli_giorno", -1),
                          ("kwh_ciclo", -0.5),
                          ("n_frigo", -1),
                          ("kwh_frigo_base", -1),
                          ("kwh_frigo_alt", -1),
                          ("kg_giorno", -1),
                          ("e_per_kg", -0.1),
                          ("p_gas", -1),
                          ("p_el", -1),
                          ("om_base", -100),
                          ("om_alt", -100),
                          ("capex", -1),
                          ("wacc_pct", -0.1), ("wacc_pct", 50.1),
                          ("vita_anni", 0), ("vita_anni", 2.5),
                          ("tolleranza_pct", -1),
                          ("tolleranza_pct", 100.1)):
        d = _demo_kwargs()
        d[campo] = valore
        assert mh810_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"superficie_m2": 0,
              "q_risc_per_m2": 0,
              "q_raff_per_m2": 0,
              "eta_rec": 0,
              "f_vent": 0,
              "litri_giorno": 0,
              "cicli_giorno": 0,
              "kwh_ciclo": 0,
              "n_frigo": 0,
              "kwh_frigo_base": 0,
              "kwh_frigo_alt": 0,
              "kg_giorno": 0,
              "e_per_kg": 0,
              "p_gas": 0,
              "p_el": 0,
              "om_base": 0, "om_alt": 0,
              "capex": 0, "wacc_pct": 0,
              "tolleranza_pct": 0})
    assert mh810_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["eta_rec"] = 1
    d["f_vent"] = 1
    assert mh810_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh810_demo()
    assert d["superficie_m2"] == 400
    assert d["giorni_anno"] == 300
    assert d["q_risc_per_m2"] == 110
    assert d["q_raff_per_m2"] == 60
    assert d["eta_rec"] == 0.60
    assert d["f_vent"] == 0.40
    assert d["litri_giorno"] == 800
    assert d["delta_t"] == 35
    assert d["cicli_giorno"] == 5
    assert d["kwh_ciclo"] == 3.0
    assert d["n_frigo"] == 3
    assert d["kwh_frigo_base"] == 2500
    assert d["kwh_frigo_alt"] == 1800
    assert d["kg_giorno"] == 40
    assert d["e_per_kg"] == 1.0
    assert d["p_gas"] == 100
    assert d["p_el"] == 260
    assert d["om_base"] == 4000
    assert d["om_alt"] == 5500
    assert d["capex"] == 30000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    bc = mh810_demo_calcoli()
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
    bc = mh810_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(18294.148148148146)
    assert bc["c_alt_eur_anno"] == pytest.approx(14968.178692810458)
    assert bc["risparmio_eur_anno"] == pytest.approx(3325.9694553376885)
    assert bc["co2_base_t_anno"] == pytest.approx(23.148296296296298)
    assert bc["co2_alt_t_anno"] == pytest.approx(12.745625163398692)
    assert bc["co2_evitata_t_anno"] == pytest.approx(10.402671132897607)
    assert bc["q_risc_kwh_anno"] == pytest.approx(44000.0)
    assert bc["q_raff_kwh_anno"] == pytest.approx(24000.0)
    assert bc["q_vent_rec_kwh_anno"] == pytest.approx(10560.0)
    assert bc["q_risc_net_kwh_anno"] == pytest.approx(33440.0)


def test_demo_flussi_e_cumulato():
    bc = mh810_demo_calcoli()
    assert bc["flussi"][0] == -30000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(3325.9694553376885) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -30000
    assert righe.iloc[9]["Cumulato (EUR)"] == pytest.approx(-66.27490704381356)
    assert righe.iloc[10]["Cumulato (EUR)"] == pytest.approx(3259.694548293875)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(19889.541830065333)


def test_demo_tabella_righe():
    bc = mh810_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Riscaldamento (kWh_th/anno)"] == pytest.approx(44000.0)
    assert mappa["Raffrescamento (kWh_th/anno)"] == pytest.approx(24000.0)
    assert mappa["Recupero calore ventilazione (kWh_th/anno)"] == pytest.approx(10560.0)
    assert mappa["Riscaldamento netto (kWh_th/anno)"] == pytest.approx(33440.0)
    assert mappa["ACS (kWh_th/anno)"] == pytest.approx(9767.333333333334)
    assert mappa["Elettricita' autoclave base (kWh_e/anno)"] == pytest.approx(4500.0)
    assert mappa["Elettricita' autoclave alt (kWh_e/anno)"] == pytest.approx(3825.0)
    assert mappa["Elettricita' frigoriferi base (kWh_e/anno)"] == pytest.approx(7500.0)
    assert mappa["Elettricita' frigoriferi alt (kWh_e/anno)"] == pytest.approx(5400.0)
    assert mappa["Elettricita' lavanderia base (kWh_e/anno)"] == pytest.approx(12000.0)
    assert mappa["Elettricita' lavanderia alt (kWh_e/anno)"] == pytest.approx(6600.0)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(59741.48148148148)
    assert mappa["Elettricita' totale base (kWh_e/anno)"] == pytest.approx(32000.0)
    assert mappa["Elettricita' totale alternativa (kWh_e/anno)"] == pytest.approx(36416.07189542484)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(18294.148148148146)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(14968.178692810458)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(3325.9694553376885)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(10.402671132897607)
    assert mappa["Payback (anni)"] == 10
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] == pytest.approx(44.32730202098074)


def test_demo_coerenza_interna():
    bc = mh810_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["q_risc_kwh_anno"] == pytest.approx(
        bc["superficie_m2"] * bc["q_risc_per_m2"])
    assert bc["q_raff_kwh_anno"] == pytest.approx(
        bc["superficie_m2"] * bc["q_raff_per_m2"])
    assert bc["q_vent_rec_kwh_anno"] == pytest.approx(
        bc["eta_rec"] * bc["f_vent"] * bc["q_risc_kwh_anno"])
    assert bc["q_risc_net_kwh_anno"] == pytest.approx(
        bc["q_risc_kwh_anno"] - bc["q_vent_rec_kwh_anno"])
    assert bc["q_acs_kwh_anno"] == pytest.approx(
        bc["litri_giorno"] * bc["giorni_anno"] * 4.186
        * bc["delta_t"] / 3600.0)
    assert bc["e_auto_base_kwh_anno"] == pytest.approx(
        bc["cicli_giorno"] * bc["giorni_anno"] * bc["kwh_ciclo"])
    assert bc["e_auto_alt_kwh_anno"] == pytest.approx(
        bc["e_auto_base_kwh_anno"] * 0.85)
    assert bc["e_frigo_base_kwh_anno"] == pytest.approx(
        bc["n_frigo"] * bc["kwh_frigo_base"])
    assert bc["e_frigo_alt_kwh_anno"] == pytest.approx(
        bc["n_frigo"] * bc["kwh_frigo_alt"])
    assert bc["e_lav_base_kwh_anno"] == pytest.approx(
        bc["kg_giorno"] * bc["giorni_anno"] * bc["e_per_kg"])
    assert bc["e_lav_alt_kwh_anno"] == pytest.approx(
        bc["e_lav_base_kwh_anno"] * 0.55)
    assert bc["gas_base_kwh_anno"] == pytest.approx(
        (bc["q_risc_kwh_anno"] + bc["q_acs_kwh_anno"]) / 0.90)
    assert bc["e_chiller_kwh_anno"] == pytest.approx(
        bc["q_raff_kwh_anno"] / 3.0)
    assert bc["e_pdc_kwh_anno"] == pytest.approx(
        bc["q_risc_net_kwh_anno"] / 3.4 + bc["q_raff_kwh_anno"] / 3.2
        + bc["q_acs_kwh_anno"] / 3.0)
    assert bc["e_base_kwh_anno"] == pytest.approx(
        bc["e_chiller_kwh_anno"] + bc["e_auto_base_kwh_anno"]
        + bc["e_frigo_base_kwh_anno"] + bc["e_lav_base_kwh_anno"])
    assert bc["e_alt_kwh_anno"] == pytest.approx(
        bc["e_pdc_kwh_anno"] + bc["e_auto_alt_kwh_anno"]
        + bc["e_frigo_alt_kwh_anno"] + bc["e_lav_alt_kwh_anno"])
    assert bc["co2_evitata_t_anno"] == pytest.approx(
        bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])
    assert bc["c_base_eur_anno"] == pytest.approx(
        bc["gas_base_kwh_anno"] / 1000.0 * bc["p_gas"]
        + bc["e_base_kwh_anno"] / 1000.0 * bc["p_el"]
        + bc["om_base"])
    assert bc["c_alt_eur_anno"] == pytest.approx(
        bc["e_alt_kwh_anno"] / 1000.0 * bc["p_el"]
        + bc["om_alt"])


def test_demo_contro_riconteggio_indipendente():
    sup, qri, qra = 400, 110, 60
    gg = 300
    ere, fve = 0.60, 0.40
    lit, dta = 800, 35
    cic, kwc = 5, 3.0
    nfr, kwb, kwa = 3, 2500, 1800
    kgg, epk = 40, 1.0
    pg, pel = 100, 260
    omb, oma, cx = 4000, 5500, 30000
    wacc, vita = 5.0, 15
    qrisc = sup * qri
    qraff = sup * qra
    qven = ere * fve * qrisc
    qnet = qrisc - qven
    qacs = lit * gg * 4.186 * dta / 3600.0
    eab = cic * gg * kwc
    eaa = eab * 0.85
    efb = nfr * kwb
    efa = nfr * kwa
    elb = kgg * gg * epk
    ela = elb * 0.55
    gasb = (qrisc + qacs) / 0.90
    ech = qraff / 3.0
    epdc = qnet / 3.4 + qraff / 3.2 + qacs / 3.0
    eb = ech + eab + efb + elb
    ea = epdc + eaa + efa + ela
    cb = gasb / 1000.0 * pg + eb / 1000.0 * pel + omb
    ca = ea / 1000.0 * pel + oma
    risp = cb - ca
    co2b = (gasb * 0.20 + eb * 0.35) / 1000.0
    co2a = ea * 0.35 / 1000.0
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    be = ((ca - omb - eb / 1000.0 * pel) * 1000.0 / gasb)
    bc = mh810_demo_calcoli()
    assert bc["q_risc_kwh_anno"] == pytest.approx(qrisc)
    assert bc["q_raff_kwh_anno"] == pytest.approx(qraff)
    assert bc["q_vent_rec_kwh_anno"] == pytest.approx(qven)
    assert bc["q_risc_net_kwh_anno"] == pytest.approx(qnet)
    assert bc["q_acs_kwh_anno"] == pytest.approx(qacs)
    assert bc["e_auto_base_kwh_anno"] == pytest.approx(eab)
    assert bc["e_auto_alt_kwh_anno"] == pytest.approx(eaa)
    assert bc["e_frigo_base_kwh_anno"] == pytest.approx(efb)
    assert bc["e_frigo_alt_kwh_anno"] == pytest.approx(efa)
    assert bc["e_lav_base_kwh_anno"] == pytest.approx(elb)
    assert bc["e_lav_alt_kwh_anno"] == pytest.approx(ela)
    assert bc["gas_base_kwh_anno"] == pytest.approx(gasb)
    assert bc["e_chiller_kwh_anno"] == pytest.approx(ech)
    assert bc["e_pdc_kwh_anno"] == pytest.approx(epdc)
    assert bc["e_base_kwh_anno"] == pytest.approx(eb)
    assert bc["e_alt_kwh_anno"] == pytest.approx(ea)
    assert bc["c_base_eur_anno"] == pytest.approx(cb)
    assert bc["c_alt_eur_anno"] == pytest.approx(ca)
    assert bc["risparmio_eur_anno"] == pytest.approx(risp)
    assert bc["co2_base_t_anno"] == pytest.approx(co2b)
    assert bc["co2_alt_t_anno"] == pytest.approx(co2a)
    assert bc["co2_evitata_t_anno"] == pytest.approx(co2)
    assert bc["van"] == pytest.approx(van)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(be)


def test_demo_verdetto_coerente_con_risparmio_e_van():
    bc = mh810_demo_calcoli()
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] > 0.0
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["tir"] is not None and bc["tir"] > bc["wacc_pct"]
    assert bc["payback"] == 10


# ---------------------------------------------------------------- varianti
def test_variante_senza_recupero_non_convinte():
    # eta_rec zero: il recupero e' nullo, il caso
    # NON regge piu' (il recupero e' decisivo).
    bc0 = _variante(eta_rec=0)
    assert bc0["q_vent_rec_kwh_anno"] == 0.0
    assert bc0["q_risc_net_kwh_anno"] == pytest.approx(44000.0)
    assert bc0["risparmio_eur_anno"] == pytest.approx(2518.4400435729804)
    assert bc0["van"] == pytest.approx(-3859.453558051843)
    assert bc0["breakeven_gas_eur_mwh"] == pytest.approx(57.844365738508806)
    assert bc0["payback"] == 12
    assert bc0["verdetto"] == "NON_CONVIENTE"


def test_variante_recupero_massimo():
    # eta_rec 1,00 e f_vent 1,00: recupero pari
    # all'intero riscaldamento, netto zero.
    bc = _variante(eta_rec=1, f_vent=1)
    assert bc["q_vent_rec_kwh_anno"] == pytest.approx(44000.0)
    assert bc["q_risc_net_kwh_anno"] == pytest.approx(0.0, abs=1e-12)
    assert bc["risparmio_eur_anno"] == pytest.approx(5883.1459259259245)
    assert bc["van"] == pytest.approx(31065.042899826418)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(1.523266915475307)
    assert bc["payback"] == 6
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_risparmio_nonpositivo_non_calcolabile():
    # Prezzo gas zero: risparmio negativo negli
    # helper (calcolabile, non solleva), verdetto
    # NON_CALCOLABILE; stessa guard della UI.
    for kw in ({"p_gas": 0}, {"om_alt": 10000}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] <= 0.0
        assert bc["verdetto"] == "NON_CALCOLABILE"
        assert bc["flussi"]
    bc = _variante(p_gas=0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-2648.1786928104575)
    assert bc["van"] == pytest.approx(-57487.189255368634)
    assert bc["payback"] is None
    bc2 = _variante(om_alt=10000)
    assert bc2["risparmio_eur_anno"] == pytest.approx(-1174.0305446623097)
    assert bc2["breakeven_gas_eur_mwh"] == pytest.approx(119.65184852381391)


def test_variante_prezzo_el_zero_helper_convinte():
    # Negli helper p_el = 0 e' ammesso e resta
    # CONVIENTE; in UI e' guard degenere:
    # divergenza documentata.
    bc = _variante(p_el=0)
    assert bc["risparmio_eur_anno"] == pytest.approx(4474.148148148148)
    assert bc["van"] == pytest.approx(16440.127789936727)
    assert bc["payback"] == 7
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_superficie_zero_helper_non_convinte():
    # Negli helper S = 0 resta calcolabile
    # (risparmio positivo, VAN negativa, verdetto
    # NON_CONVIENTE, breakeven 20,36); in UI e'
    # guard degenere (S <= 0): divergenza
    # documentata.
    bc = _variante(superficie_m2=0)
    assert bc["q_risc_kwh_anno"] == 0.0
    assert bc["q_raff_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(864.2570370370377)
    assert bc["van"] == pytest.approx(-21029.307498464368)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(20.364002457170088)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_carichi_zero_come_superficie_zero():
    bc = _variante(q_risc_per_m2=0, q_raff_per_m2=0)
    demo_s0 = _variante(superficie_m2=0)
    assert bc["risparmio_eur_anno"] == pytest.approx(demo_s0["risparmio_eur_anno"])
    assert bc["van"] == pytest.approx(demo_s0["van"])
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_capex_conviente_e_zero():
    bc = _variante(capex=60000)
    assert bc["risparmio_eur_anno"] == pytest.approx(3325.9694553376885)
    assert bc["van"] == pytest.approx(-25477.574408161046)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"
    bc0 = _variante(capex=0)
    assert bc0["flussi"][0] == 0
    assert bc0["payback"] == 0
    assert bc0["tir"] is None
    assert bc0["van"] == pytest.approx(34522.42559183895, rel=1e-6)
    assert bc0["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(19889.541830065333)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(-4317.745483317188)
    assert bc2["payback"] == 10
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_el_alto_marginale():
    # Elettricita' cara penalizza (l'alternativa
    # consuma piu' elettricita' della base):
    # VAN negativa entro il 10 % del CAPEX.
    bc = _variante(p_el=400)
    assert bc["risparmio_eur_anno"] == pytest.approx(2707.719389978214)
    assert bc["van"] == pytest.approx(-1894.7986686751901)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(54.676058865102824)
    assert bc["payback"] == 12
    assert bc["verdetto"] == "MARGINALE"


def test_monotonia_prezzo_gas_crescente():
    base = mh810_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas=101)["risparmio_eur_anno"]
    basso = _variante(p_gas=99)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(59.74148148148148, abs=1e-2)
    assert base - basso == pytest.approx(59.74148148148148, abs=1e-2)


def test_monotonia_recupero_crescente():
    assert _variante(eta_rec=0.30)["risparmio_eur_anno"] < \
        mh810_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(eta_rec=0.90)["risparmio_eur_anno"] > \
        mh810_demo_calcoli()["risparmio_eur_anno"]


def test_demo_deterministica_due_chiamate():
    a = mh810_demo_calcoli()
    b = mh810_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh810_demo().keys()) == {
        "superficie_m2", "giorni_anno",
        "q_risc_per_m2", "q_raff_per_m2",
        "eta_rec", "f_vent",
        "litri_giorno", "delta_t",
        "cicli_giorno", "kwh_ciclo",
        "n_frigo", "kwh_frigo_base", "kwh_frigo_alt",
        "kg_giorno", "e_per_kg",
        "p_gas", "p_el",
        "om_base", "om_alt",
        "capex", "wacc_pct", "vita_anni",
        "tolleranza_pct"}


# ---------------------------------------------------------------- degenere
def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"superficie_m2": -10},
               {"q_risc_per_m2": -10},
               {"q_raff_per_m2": -10},
               {"giorni_anno": 0},
               {"giorni_anno": 2.5},
               {"eta_rec": -0.1}, {"eta_rec": 1.01},
               {"f_vent": -0.1}, {"f_vent": 1.01},
               {"litri_giorno": -1},
               {"delta_t": 0}, {"delta_t": -5},
               {"cicli_giorno": -1},
               {"kwh_ciclo": -0.5},
               {"n_frigo": -1},
               {"kwh_frigo_base": -1},
               {"kwh_frigo_alt": -1},
               {"kg_giorno": -1},
               {"e_per_kg": -0.1},
               {"p_gas": -1},
               {"p_el": -1},
               {"om_base": -100},
               {"om_alt": -100},
               {"capex": -1},
               {"wacc_pct": -1}, {"wacc_pct": 60},
               {"vita_anni": 0}, {"vita_anni": 2.5},
               {"tolleranza_pct": -1},
               {"tolleranza_pct": 100.1}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh810_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"superficie_m2": "400"},
               {"superficie_m2": float("nan")},
               {"p_gas": float("inf")},
               {"capex": True},
               {"q_risc_per_m2": "110"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh810_valida(**d)["valido"] is False


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    for kw in ({"p_gas": 0}, {"om_alt": 10000}):
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
    be = mh810_demo_calcoli()["breakeven_gas_eur_mwh"]
    bc = _variante(p_gas=be)
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["verdetto"] != "CONVIENTE"
    bc2 = _variante(p_gas=be + 1)
    assert bc2["risparmio_eur_anno"] == pytest.approx(59.74148148148148, abs=1e-2)
    # Risparmio positivo ma piccolo: VAN negativa oltre
    # la tolleranza, quindi NON_CONVIENTE (non CONVIENTE).
    assert bc2["verdetto"] == "NON_CONVIENTE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh810_demo_calcoli()
    testo = mh810_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_gas_eur_mwh" in testo
    assert "co2_evitata_t_anno" in testo
    assert "q_vent_rec_kwh_anno" in testo
    assert "q_risc_net_kwh_anno" in testo
    assert "e_auto_alt_kwh_anno" in testo
    assert "e_frigo_alt_kwh_anno" in testo
    assert "e_lav_alt_kwh_anno" in testo
    assert "e_pdc_kwh_anno" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh810_demo_calcoli()
    testo = mh810_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"q_vent_rec_kwh_anno;{bc['q_vent_rec_kwh_anno']}" in testo
    assert f"gas_base_kwh_anno;{bc['gas_base_kwh_anno']}" in testo
    assert f"q_risc_kwh_anno;{bc['q_risc_kwh_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh810_demo_calcoli()
    testo = mh810_csv(bc, _demo_kwargs())
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
    return ["mh" + "80" + "9", "st" + "80" + "9",
            "tab" + "80" + "9", "w" + "81" + "0",
            "mh" + "80" + "8", "tab" + "80" + "8"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w811_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w811_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab810:")


def test_ui_apre_scheda_attesa_una_volta():
    """Il frammento UI apre la scheda attesa, una sola volta."""
    src = _leggi("w811_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert m.group(1) == "810"
    assert src.count("with tab810:") == 1


def test_ui_titolo_atteso():
    src = _leggi("w811_ui.py")
    titolo = ("Clinica veterinaria: pompa di calore + recupero "
              "calore ventilazione sale operatorie batte caldaia "
              "a gas + chiller + autoclave tradizionale?")
    assert src.count(titolo) == 2


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w811_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w811_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st810_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) >= 30
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w811_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 4
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_ui_guard_degenere_stretta():
    """La guard UI della scheda dichiara NON_CALCOLABILE
    anche per superficie <= 0, carichi <= 0, prezzi
    <= 0 e CAPEX <= 0 (piu' stretta degli helper,
    che ammettono lo zero)."""
    src = _leggi("w811_ui.py")
    assert "float(_sup810) <= 0.0" in src
    assert "float(_qri810) <= 0.0" in src
    assert "float(_qra810) <= 0.0" in src
    assert "float(_pg810) <= 0.0" in src
    assert "float(_pel810) <= 0.0" in src
    assert "float(_cx810) <= 0.0" in src
    assert "int(_vita810) <= 0" in src
    assert "Verdetto: NON_CALCOLABILE" in src


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w811_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def810[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w811_ui.py")
        usate = set(re.findall(r'_def810\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 23
        assert usate <= set(mh810_demo().keys())
