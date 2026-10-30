"""Test nuova scheda "Falegnameria:
motori efficienti + aspirazione con
inverter + caldaia a biomassa da scarti
battono motori tradizionali + aspirazione
sempre accesa + caldaia a gas?" (titolo
completo nel frammento UI).

Business case deterministico di una
falegnameria guidata dai METRI CUBI DI
LEGNO lavorati in un anno: E_seg_base =
legno_m3 x e_seg; E_pial_base = legno_m3 x
e_pial; E_lev_base = legno_m3 x e_lev;
E_lav_base = E_seg_base + E_pial_base +
E_lev_base; E_asp_base = legno_m3 x e_asp;
E_lav_alt = E_lav_base x f_eff (i motori
efficienti riducono solo le lavorazioni);
E_asp_alt = E_asp_base x f_asp (l'inverter
riduce solo l'aspirazione); E_base =
E_lav_base + E_asp_base; E_alt = E_lav_alt
+ E_asp_alt; Q_risc = legno_m3 x q_risc;
gas_base = Q_risc / eta_cald; gas_alt =
Q_risc x (1 - f_bio) / eta_cald (la
biomassa da scarti copre solo la quota
f_bio del calore); C_base = E_base / 1000
x p_el + gas_base / 1000 x p_gas + OM_base;
C_alt = E_alt / 1000 x p_el + gas_alt /
1000 x p_gas + OM_alt; risparmio = C_base
- C_alt; CO2 evitata = (E_base x 0,35 +
gas_base x 0,20 - E_alt x 0,35 - gas_alt x
0,20) / 1000 (fattori letterali, biomassa a
zero); flussi [-CAPEX, risparmio x vita];
VAN, TIR, payback (primo anno con cumulato
>= 0); breakeven gas = (E_alt / 1000 x p_el
+ OM_alt - E_base / 1000 x p_el - OM_base)
x 1000 / (gas_base - gas_alt) EUR/MWh, None
se gas_base <= gas_alt o numeratore < 0,
SOGLIA MINIMA quando esiste. Nel demo il
breakeven e' None (numeratore -3.128,00
EUR, denominatore 74.666,67 kWh/anno):
l'alternativa vince gia' a prezzo gas zero.
Verdetto: NON_CALCOLABILE se input degenere
(legno <= 0, specifici negativi, fattori
fuori [0, 1], calore specifico negativo,
rendimento caldaia <= 0 o sopra 1, prezzi
<= 0, O&M negativi, CAPEX <= 0, WACC
negativo, vita <= 0, tolleranza negativa)
o se risparmio <= 0 (guard degenere: UI
salta KPI, grafico, tabella e CSV);
altrimenti CONVIENTE se VAN > 0, MARGINALE
se VAN negativa entro tolleranza % del
CAPEX, NON_CONVIENTE se VAN negativa oltre
la tolleranza. Guard UI IDENTICA agli
helper: nessuna divergenza di verdetto.
Tutti gli slider UI hanno minimo 0, quindi
i casi negativi sono NON RAGGIUNGIBILI via
slider, ma la guard li controlla comunque;
i casi = 0 raggiungibili via slider sono
bloccati in UI esattamente come negli
helper dove previsto (legno, rendimento
caldaia, prezzi, CAPEX, vita). Gli zeri
ammessi in entrambi (specifici elettrici,
fattori 0 o 1, calore specifico, O&M, WACC,
tolleranza) non creano divergenza: con
calore specifico zero il gas base e' zero e
il breakeven e' None, e il caso resta
calcolabile in entrambi. WACC sopra 20 % e
tolleranza sopra 100 % sono ammessi negli
helper e limitati solo dagli slider UI (20,
100): nessuna divergenza nel range
raggiungibile, perche' la guard controlla
solo gli stessi limiti degli helper.
Distinzione esplicita: distinto dal
frantoio (tonnellate di olive, acqua calda
di processo: qui niente olive, niente
malaxazione), dal caseificio (litri di
latte, pastorizzazione: qui niente latte,
niente pastorizzazione), dal birrificio
(ettolitri di birra, bollitura del mosto:
qui niente mosto, niente bollitura), dalla
discoteca (m2 di locale, serate: qui niente
m2 di locale, niente serate), dalla
lavanderia (kg di biancheria: qui niente
biancheria, niente capi da lavare): qui
driver METRI CUBI DI LEGNO + MOTORI
EFFICIENTI + INVERTER + BIOMASSA.

Demo (falegnameria): 1200 m3 di legno,
segagione specifica 40 (48.000 kWh_e/anno),
piallatura specifica 30 (36.000
kWh_e/anno), levigatura specifica 20
(24.000 kWh_e/anno), lavorazioni base
108.000 e alternative 91.800 kWh_e/anno
(fattore motori 0,85), aspirazione
specifica 25 (base 30.000, alternativa
16.500 kWh_e/anno con fattore inverter
0,55), calore specifico 80 (96.000
kWh_th/anno), quota biomassa 0,70 (gas base
106.666,66666666666 e gas alternativo
32.000 kWh/anno), rendimento caldaia 0,90,
prezzi elettricita' 240 e gas 100 EUR/MWh,
O&M base 8.000 e alternativo 12.000
EUR/anno, CAPEX 85.000 EUR, WACC 5 %, vita
15 anni, tolleranza 10 % del CAPEX. Valori
calcolati eseguendo mh818_demo_calcoli():
E_base 138.000, E_alt 108.300, C_base
51.786,666666666664, C_alt 41.192, risparmio
10.594,666666666664, CO2_base
69,63333333333333, CO2_alt 44,305,
CO2_evitata 25,32833333333333, VAN
24.969,017028510603, TIR 9,079696533984528
%, payback 9, breakeven gas None
(numeratore negativo), verdetto CONVIENTE.
"""

import ast
import inspect
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w819_helpers import (
    demo_calcoli,
    mh818_breakeven_gas,
    mh818_c_alt,
    mh818_c_base,
    mh818_calcola,
    mh818_co2_alt,
    mh818_co2_base,
    mh818_co2_evitata,
    mh818_csv,
    mh818_demo,
    mh818_demo_calcoli,
    mh818_e_alt,
    mh818_e_asp_alt,
    mh818_e_asp_base,
    mh818_e_base,
    mh818_e_lav_alt,
    mh818_e_lav_base,
    mh818_e_lev_base,
    mh818_e_pial_base,
    mh818_e_seg_base,
    mh818_eta,
    mh818_flussi,
    mh818_frazione,
    mh818_gas_alt,
    mh818_gas_base,
    mh818_int_pos,
    mh818_nneg,
    mh818_num,
    mh818_payback,
    mh818_pos,
    mh818_q_risc,
    mh818_risparmio,
    mh818_tir,
    mh818_valida,
    mh818_van,
    mh818_verdetto,
)

_DEMO = {
    "q_risc_kwh_th_anno": 96000.0,
    "e_seg_base_kwh_e_anno": 48000.0,
    "e_pial_base_kwh_e_anno": 36000.0,
    "e_lev_base_kwh_e_anno": 24000.0,
    "e_lav_base_kwh_e_anno": 108000.0,
    "e_lav_alt_kwh_e_anno": 91800.0,
    "e_asp_base_kwh_e_anno": 30000.0,
    "e_asp_alt_kwh_e_anno": 16500.0,
    "e_base_kwh_e_anno": 138000.0,
    "e_alt_kwh_e_anno": 108300.0,
    "gas_base_kwh_anno": 106666.66666666666,
    "gas_alt_kwh_anno": 32000.0,
    "c_base_eur_anno": 51786.666666666664,
    "c_alt_eur_anno": 41192.0,
    "risparmio_eur_anno": 10594.666666666664,
    "co2_base_t_anno": 69.63333333333333,
    "co2_alt_t_anno": 44.305,
    "co2_evitata_t_anno": 25.32833333333333,
    "van": 24969.017028510603,
    "tir": 9.079696533984528,
}


def _demo_kwargs():
    return dict(mh818_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh818_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh818_num(3, "x") == 3.0
    assert mh818_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh818_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh818_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh818_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh818_pos(0, "x")
    with pytest.raises(ValueError):
        mh818_pos(-1, "x")
    assert mh818_pos(0.5, "x") == 0.5


def test_frazione_limiti():
    assert mh818_frazione(0, "x") == 0.0
    assert mh818_frazione(1, "x") == 1.0
    assert mh818_frazione(0.85, "x") == 0.85
    with pytest.raises(ValueError):
        mh818_frazione(-0.01, "x")
    with pytest.raises(ValueError):
        mh818_frazione(1.01, "x")


def test_eta_limiti():
    assert mh818_eta(1, "x") == 1.0
    assert mh818_eta(0.90, "x") == 0.90
    with pytest.raises(ValueError):
        mh818_eta(0, "x")
    with pytest.raises(ValueError):
        mh818_eta(-0.1, "x")
    with pytest.raises(ValueError):
        mh818_eta(1.01, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh818_int_pos(5.0, "x") == 5
    assert mh818_int_pos(15.0, "x") == 15
    with pytest.raises(ValueError):
        mh818_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh818_int_pos(0, "x")


# ---------------------------------------------------------------- fisica base
def test_q_risc():
    assert mh818_q_risc(1200, 80) == 96000.0
    assert mh818_q_risc(1200, 0) == 0.0
    with pytest.raises(ValueError):
        mh818_q_risc(0, 80)
    with pytest.raises(ValueError):
        mh818_q_risc(1200, -1)


def test_e_seg_pial_lev_e_lav_base():
    assert mh818_e_seg_base(1200, 40) == 48000.0
    assert mh818_e_pial_base(1200, 30) == 36000.0
    assert mh818_e_lev_base(1200, 20) == 24000.0
    assert mh818_e_lav_base(48000.0, 36000.0, 24000.0) == 108000.0
    with pytest.raises(ValueError):
        mh818_e_lav_base(-1, 36000.0, 24000.0)
    with pytest.raises(ValueError):
        mh818_e_seg_base(0, 40)


def test_e_lav_alt_e_asp_base_alt():
    assert mh818_e_lav_alt(108000.0, 0.85) == 91800.0
    assert mh818_e_lav_alt(108000.0, 1) == 108000.0
    assert mh818_e_lav_alt(108000.0, 0) == 0.0
    assert mh818_e_asp_base(1200, 25) == 30000.0
    assert mh818_e_asp_alt(30000.0, 0.55) == 16500.0
    assert mh818_e_asp_alt(30000.0, 1) == 30000.0
    assert mh818_e_asp_alt(30000.0, 0) == 0.0
    with pytest.raises(ValueError):
        mh818_e_lav_alt(108000.0, 1.01)
    with pytest.raises(ValueError):
        mh818_e_asp_alt(30000.0, 1.01)
    with pytest.raises(ValueError):
        mh818_e_asp_base(0, 25)


def test_e_base_e_alt():
    assert mh818_e_base(108000.0, 30000.0) == 138000.0
    assert mh818_e_alt(91800.0, 16500.0) == 108300.0
    with pytest.raises(ValueError):
        mh818_e_base(-1, 30000.0)
    with pytest.raises(ValueError):
        mh818_e_alt(91800.0, -1)


def test_gas_base_alt():
    assert mh818_gas_base(96000.0, 0.90) == pytest.approx(106666.66666666666)
    assert mh818_gas_base(0, 0.90) == 0.0
    assert mh818_gas_alt(96000.0, 0.70, 0.90) == pytest.approx(32000.0)
    assert mh818_gas_alt(96000.0, 0, 0.90) == pytest.approx(106666.66666666666)
    assert mh818_gas_alt(96000.0, 1, 0.90) == 0.0
    with pytest.raises(ValueError):
        mh818_gas_base(96000.0, 0)
    with pytest.raises(ValueError):
        mh818_gas_base(96000.0, 1.01)
    with pytest.raises(ValueError):
        mh818_gas_alt(96000.0, 1.01, 0.90)


def test_c_base_c_alt_scomposizione():
    assert mh818_c_base(138000.0, 240, 106666.66666666666, 100,
                        8000) == pytest.approx(51786.666666666664)
    assert mh818_c_alt(108300.0, 240, 32000.0, 100,
                       12000) == pytest.approx(41192.0)
    with pytest.raises(ValueError):
        mh818_c_base(138000.0, 0, 106666.66666666666, 100, 8000)
    with pytest.raises(ValueError):
        mh818_c_alt(108300.0, 240, 32000.0, 0, 12000)
    with pytest.raises(ValueError):
        mh818_c_base(138000.0, 240, 106666.66666666666, 100, -1)


def test_risparmio_segno():
    assert mh818_risparmio(51786.666666666664, 41192.0) == pytest.approx(10594.666666666664)
    assert mh818_risparmio(41192.0, 41192.0) == pytest.approx(0.0, abs=1e-9)


def test_co2_base_alt_evitata():
    assert mh818_co2_base(138000.0, 106666.66666666666) == pytest.approx(69.63333333333333)
    assert mh818_co2_alt(108300.0, 32000.0) == pytest.approx(44.305)
    assert mh818_co2_evitata(138000.0, 106666.66666666666,
                             108300.0, 32000.0) == pytest.approx(25.32833333333333)
    assert mh818_co2_base(0, 0) == 0.0
    assert mh818_co2_alt(0, 0) == 0.0
    with pytest.raises(ValueError):
        mh818_co2_base(138000.0, -1)
    with pytest.raises(ValueError):
        mh818_co2_alt(-1, 32000.0)


def test_breakeven_demo_none_numeratore_negativo():
    bc = mh818_demo_calcoli()
    assert bc["breakeven_gas_eur_mwh"] is None
    # Numeratore: 108300/1000*240 + 12000 - 138000/1000*240 - 8000 = -3128 < 0.
    assert mh818_breakeven_gas(108300.0, 240, 12000, 138000.0,
                               8000, 106666.66666666666,
                               32000.0) is None
    # Denominatore nullo (gas_base = gas_alt) -> None.
    assert mh818_breakeven_gas(108300.0, 240, 12000, 138000.0,
                               8000, 0.0, 0.0) is None
    # Variante senza biomassa: gas_base = gas_alt -> None.
    assert _variante(f_bio=0)["breakeven_gas_eur_mwh"] is None
    # Variante calore zero -> breakeven None.
    assert _variante(q_risc_kwh_th_m3=0)["breakeven_gas_eur_mwh"] is None
    with pytest.raises(ValueError):
        mh818_breakeven_gas(108300.0, 240, 12000, 138000.0,
                            8000, -1, 32000.0)


def test_breakeven_variante_senza_motori_valore():
    # Senza motori efficienti il numeratore diventa
    # positivo e il breakeven esiste: 10,18 EUR/MWh.
    bc = _variante(f_eff=1)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(10.17857142857143)
    assert mh818_breakeven_gas(124500.0, 240, 12000, 138000.0,
                               8000, 106666.66666666666,
                               32000.0) == pytest.approx(10.17857142857143)


def test_breakeven_verifica_pareggio_su_variante():
    be = _variante(f_eff=1)["breakeven_gas_eur_mwh"]
    bc = _variante(f_eff=1, p_gas=be)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_breakeven_soglia_minima_su_variante():
    be = _variante(f_eff=1)["breakeven_gas_eur_mwh"]
    bc_alto = _variante(f_eff=1, p_gas=be + 1)
    bc_basso = _variante(f_eff=1, p_gas=be - 1)
    assert bc_alto["c_alt_eur_anno"] < bc_alto["c_base_eur_anno"]
    assert bc_basso["c_alt_eur_anno"] > bc_basso["c_base_eur_anno"]
    assert bc_alto["risparmio_eur_anno"] > 0.0
    assert bc_basso["verdetto"] == "NON_CALCOLABILE"
    # Sopra la soglia il risparmio e' positivo ma
    # piccolo: VAN ancora negativa oltre la
    # tolleranza, quindi NON_CONVIENTE.
    assert bc_alto["verdetto"] == "NON_CONVIENTE"


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh818_flussi(85000, 10594.666666666664, 15)
    assert len(fl) == 16
    assert fl[0] == -85000
    assert all(f == pytest.approx(10594.666666666664) for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh818_demo_calcoli()
    assert bc["van"] == pytest.approx(24969.017028510603)
    assert mh818_van([-85000] + [10594.666666666664] * 15,
                     0) == pytest.approx(73920.0)
    assert mh818_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh818_demo_calcoli()
    assert bc["tir"] == pytest.approx(9.079696533984528)
    assert mh818_tir([-85000] + [10594.666666666664] * 15) == \
        pytest.approx(0.09079696533984528)
    tir = mh818_tir([-85000] + [10594.666666666664] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-85000] + [10594.666666666664] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh818_payback([-85000] + [10594.666666666664] * 15) == 9
    assert mh818_payback([-85000] + [-1000.0] * 15) is None
    assert mh818_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh818_verdetto(10594.666666666664, 24969.017028510603, 85000,
                          10.0) == "CONVIENTE"
    assert mh818_verdetto(10594.666666666664, -1500.0, 85000,
                          10.0) == "MARGINALE"
    assert mh818_verdetto(10594.666666666664, -8500.0, 85000, 10.0) == "MARGINALE"
    assert mh818_verdetto(10594.666666666664, -8500.01, 85000, 10.0) == "NON_CONVIENTE"
    assert mh818_verdetto(10594.666666666664, 0.0, 85000, 10.0) == "MARGINALE"
    assert mh818_verdetto(0.0, 24969.02, 85000,
                          10.0) == "NON_CALCOLABILE"
    assert mh818_verdetto(-7405.33, -161864.83, 85000,
                          10.0) == "NON_CALCOLABILE"
    assert mh818_verdetto(None, 24969.02, 85000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh818_verdetto(float("nan"), 24969.02, 85000, 10.0)
    with pytest.raises(ValueError):
        mh818_verdetto(10594.666666666664, 24969.02, 0, 10.0)
    with pytest.raises(ValueError):
        mh818_verdetto(10594.666666666664, 24969.02, 85000, -1)


def test_valida_demo_ok():
    v = mh818_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("legno_m3", "1200"),
                       ("legno_m3", float("nan")),
                       ("legno_m3", float("inf")),
                       ("legno_m3", True),
                       ("p_gas", None),
                       ("f_bio", "0.70")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh818_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("legno_m3", 0),
                          ("legno_m3", -10),
                          ("e_seg_kwh_e_m3", -0.1),
                          ("e_pial_kwh_e_m3", -0.1),
                          ("e_lev_kwh_e_m3", -0.1),
                          ("f_eff", -0.1),
                          ("f_eff", 1.01),
                          ("e_asp_kwh_e_m3", -0.1),
                          ("f_asp", -0.1),
                          ("f_asp", 1.01),
                          ("q_risc_kwh_th_m3", -0.1),
                          ("f_bio", -0.1),
                          ("f_bio", 1.01),
                          ("eta_cald", 0),
                          ("eta_cald", 1.01),
                          ("p_el", 0),
                          ("p_el", -1),
                          ("p_gas", 0),
                          ("p_gas", -1),
                          ("om_base", -100),
                          ("om_alt", -100),
                          ("capex", 0),
                          ("capex", -1),
                          ("wacc_pct", -0.1),
                          ("vita_anni", 0), ("vita_anni", 2.5),
                          ("tolleranza_pct", -1)):
        d = _demo_kwargs()
        d.update({campo: valore})
        assert mh818_valida(**d)["valido"] is False


def test_valida_accetta_limiti_e_nessun_tetto_wacc_tolleranza():
    d = _demo_kwargs()
    d.update({"e_seg_kwh_e_m3": 0,
              "e_pial_kwh_e_m3": 0,
              "e_lev_kwh_e_m3": 0,
              "f_eff": 0,
              "e_asp_kwh_e_m3": 0,
              "f_asp": 0,
              "q_risc_kwh_th_m3": 0,
              "f_bio": 0,
              "om_base": 0, "om_alt": 0,
              "wacc_pct": 0,
              "tolleranza_pct": 0})
    assert mh818_valida(**d)["valido"] is True
    d["f_eff"] = 1
    d["f_asp"] = 1
    d["f_bio"] = 1
    d["eta_cald"] = 1
    # Il brief non impone tetti superiori a WACC
    # e tolleranza: gli helper li ammettono.
    d["wacc_pct"] = 60
    d["tolleranza_pct"] = 200
    assert mh818_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh818_demo()
    assert d["legno_m3"] == 1200
    assert d["e_seg_kwh_e_m3"] == 40
    assert d["e_pial_kwh_e_m3"] == 30
    assert d["e_lev_kwh_e_m3"] == 20
    assert d["f_eff"] == 0.85
    assert d["e_asp_kwh_e_m3"] == 25
    assert d["f_asp"] == 0.55
    assert d["q_risc_kwh_th_m3"] == 80
    assert d["f_bio"] == 0.70
    assert d["eta_cald"] == 0.90
    assert d["p_el"] == 240
    assert d["p_gas"] == 100
    assert d["om_base"] == 8000
    assert d["om_alt"] == 12000
    assert d["capex"] == 85000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    bc = mh818_demo_calcoli()
    for chiave, atteso in _DEMO.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert got == pytest.approx(atteso, rel=1e-9), chiave
    assert bc["payback"] == 9
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True
    assert bc["breakeven_gas_eur_mwh"] is None
    assert demo_calcoli()["van"] == bc["van"]


def test_demo_calcoli_fisica_economia():
    bc = mh818_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(51786.666666666664)
    assert bc["c_alt_eur_anno"] == pytest.approx(41192.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(10594.666666666664)
    assert bc["co2_base_t_anno"] == pytest.approx(69.63333333333333)
    assert bc["co2_alt_t_anno"] == pytest.approx(44.305)
    assert bc["co2_evitata_t_anno"] == pytest.approx(25.32833333333333)
    assert bc["q_risc_kwh_th_anno"] == pytest.approx(96000.0)
    assert bc["e_seg_base_kwh_e_anno"] == pytest.approx(48000.0)
    assert bc["e_pial_base_kwh_e_anno"] == pytest.approx(36000.0)
    assert bc["e_lev_base_kwh_e_anno"] == pytest.approx(24000.0)
    assert bc["e_lav_base_kwh_e_anno"] == pytest.approx(108000.0)
    assert bc["e_lav_alt_kwh_e_anno"] == pytest.approx(91800.0)
    assert bc["e_asp_base_kwh_e_anno"] == pytest.approx(30000.0)
    assert bc["e_asp_alt_kwh_e_anno"] == pytest.approx(16500.0)
    assert bc["e_base_kwh_e_anno"] == pytest.approx(138000.0)
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(108300.0)
    assert bc["gas_base_kwh_anno"] == pytest.approx(106666.66666666666)
    assert bc["gas_alt_kwh_anno"] == pytest.approx(32000.0)


def test_demo_flussi_e_cumulato():
    bc = mh818_demo_calcoli()
    assert bc["flussi"][0] == -85000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(10594.666666666664) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -85000
    assert righe.iloc[8]["Cumulato (EUR)"] == pytest.approx(-242.66666666669335)
    assert righe.iloc[9]["Cumulato (EUR)"] == pytest.approx(10352.0)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(73920.0)


def test_demo_tabella_righe():
    bc = mh818_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Segagione baseline (kWh_e/anno)"] == pytest.approx(48000.0)
    assert mappa["Piallatura baseline (kWh_e/anno)"] == pytest.approx(36000.0)
    assert mappa["Levigatura baseline (kWh_e/anno)"] == pytest.approx(24000.0)
    assert mappa["Lavorazioni baseline (kWh_e/anno)"] == pytest.approx(108000.0)
    assert mappa["Lavorazioni alternative (kWh_e/anno)"] == pytest.approx(91800.0)
    assert mappa["Aspirazione baseline (kWh_e/anno)"] == pytest.approx(30000.0)
    assert mappa["Aspirazione alternativa (kWh_e/anno)"] == pytest.approx(16500.0)
    assert mappa["Elettricita' base (kWh_e/anno)"] == pytest.approx(138000.0)
    assert mappa["Elettricita' alternativa (kWh_e/anno)"] == pytest.approx(108300.0)
    assert mappa["Calore capannone (kWh_th/anno)"] == pytest.approx(96000.0)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(106666.66666666666)
    assert mappa["Gas alternativo (kWh/anno)"] == pytest.approx(32000.0)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(51786.666666666664)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(41192.0)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(10594.666666666664)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(25.32833333333333)
    assert mappa["Payback (anni)"] == 9
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] is None


def test_demo_coerenza_interna():
    bc = mh818_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["q_risc_kwh_th_anno"] == pytest.approx(
        bc["legno_m3"] * bc["q_risc_kwh_th_m3"])
    assert bc["e_seg_base_kwh_e_anno"] == pytest.approx(
        bc["legno_m3"] * bc["e_seg_kwh_e_m3"])
    assert bc["e_pial_base_kwh_e_anno"] == pytest.approx(
        bc["legno_m3"] * bc["e_pial_kwh_e_m3"])
    assert bc["e_lev_base_kwh_e_anno"] == pytest.approx(
        bc["legno_m3"] * bc["e_lev_kwh_e_m3"])
    assert bc["e_lav_base_kwh_e_anno"] == pytest.approx(
        bc["e_seg_base_kwh_e_anno"] + bc["e_pial_base_kwh_e_anno"]
        + bc["e_lev_base_kwh_e_anno"])
    assert bc["e_lav_alt_kwh_e_anno"] == pytest.approx(
        bc["e_lav_base_kwh_e_anno"] * bc["f_eff"])
    assert bc["e_asp_base_kwh_e_anno"] == pytest.approx(
        bc["legno_m3"] * bc["e_asp_kwh_e_m3"])
    assert bc["e_asp_alt_kwh_e_anno"] == pytest.approx(
        bc["e_asp_base_kwh_e_anno"] * bc["f_asp"])
    assert bc["e_base_kwh_e_anno"] == pytest.approx(
        bc["e_lav_base_kwh_e_anno"] + bc["e_asp_base_kwh_e_anno"])
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(
        bc["e_lav_alt_kwh_e_anno"] + bc["e_asp_alt_kwh_e_anno"])
    assert bc["gas_base_kwh_anno"] == pytest.approx(
        bc["q_risc_kwh_th_anno"] / bc["eta_cald"])
    assert bc["gas_alt_kwh_anno"] == pytest.approx(
        bc["q_risc_kwh_th_anno"] * (1.0 - bc["f_bio"])
        / bc["eta_cald"])
    assert bc["co2_evitata_t_anno"] == pytest.approx(
        bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])
    assert bc["c_base_eur_anno"] == pytest.approx(
        bc["e_base_kwh_e_anno"] / 1000.0 * bc["p_el"]
        + bc["gas_base_kwh_anno"] / 1000.0 * bc["p_gas"]
        + bc["om_base"])
    assert bc["c_alt_eur_anno"] == pytest.approx(
        bc["e_alt_kwh_e_anno"] / 1000.0 * bc["p_el"]
        + bc["gas_alt_kwh_anno"] / 1000.0 * bc["p_gas"]
        + bc["om_alt"])


def test_demo_contro_riconteggio_indipendente():
    lg, es, ep, el, fe = 1200, 40, 30, 20, 0.85
    ea_sp, fa, qr, fb, etac = 25, 0.55, 80, 0.70, 0.90
    pel, pg = 240, 100
    omb, oma, cx = 8000, 12000, 85000
    wacc, vita = 5.0, 15
    e_seg_b = lg * es
    e_pial_b = lg * ep
    e_lev_b = lg * el
    e_lav_b = e_seg_b + e_pial_b + e_lev_b
    e_lav_a = e_lav_b * fe
    e_asp_b = lg * ea_sp
    e_asp_a = e_asp_b * fa
    eb = e_lav_b + e_asp_b
    ea = e_lav_a + e_asp_a
    q_risc = lg * qr
    gasb = q_risc / etac
    gasa = q_risc * (1 - fb) / etac
    cb = eb / 1000.0 * pel + gasb / 1000.0 * pg + omb
    ca = ea / 1000.0 * pel + gasa / 1000.0 * pg + oma
    risp = cb - ca
    co2b = (eb * 0.35 + gasb * 0.20) / 1000.0
    co2a = (ea * 0.35 + gasa * 0.20) / 1000.0
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    bc = mh818_demo_calcoli()
    assert bc["e_seg_base_kwh_e_anno"] == pytest.approx(e_seg_b)
    assert bc["e_pial_base_kwh_e_anno"] == pytest.approx(e_pial_b)
    assert bc["e_lev_base_kwh_e_anno"] == pytest.approx(e_lev_b)
    assert bc["e_lav_base_kwh_e_anno"] == pytest.approx(e_lav_b)
    assert bc["e_lav_alt_kwh_e_anno"] == pytest.approx(e_lav_a)
    assert bc["e_asp_base_kwh_e_anno"] == pytest.approx(e_asp_b)
    assert bc["e_asp_alt_kwh_e_anno"] == pytest.approx(e_asp_a)
    assert bc["e_base_kwh_e_anno"] == pytest.approx(eb)
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(ea)
    assert bc["q_risc_kwh_th_anno"] == pytest.approx(q_risc)
    assert bc["gas_base_kwh_anno"] == pytest.approx(gasb)
    assert bc["gas_alt_kwh_anno"] == pytest.approx(gasa)
    assert bc["c_base_eur_anno"] == pytest.approx(cb)
    assert bc["c_alt_eur_anno"] == pytest.approx(ca)
    assert bc["risparmio_eur_anno"] == pytest.approx(risp)
    assert bc["co2_base_t_anno"] == pytest.approx(co2b)
    assert bc["co2_alt_t_anno"] == pytest.approx(co2a)
    assert bc["co2_evitata_t_anno"] == pytest.approx(co2)
    assert bc["van"] == pytest.approx(van)
    assert bc["breakeven_gas_eur_mwh"] is None


def test_demo_verdetto_coerente_con_risparmio_e_van():
    bc = mh818_demo_calcoli()
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] > 0.0
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["tir"] is not None and bc["tir"] > bc["wacc_pct"]
    assert bc["payback"] == 9


# ---------------------------------------------------------------- varianti
def test_variante_senza_biomassa_non_convinte():
    # Biomassa zero: il gas alternativo resta
    # 106.666,67 kWh/anno, il risparmio scende
    # a 3.128,00 EUR/anno (solo elettricita') e
    # il caso diventa NON_CONVIENTE.
    bc = _variante(f_bio=0)
    assert bc["gas_alt_kwh_anno"] == pytest.approx(106666.66666666666)
    assert bc["c_alt_eur_anno"] == pytest.approx(48658.666666666664)
    assert bc["risparmio_eur_anno"] == pytest.approx(3128.0)
    assert bc["van"] == pytest.approx(-52532.42965657114)
    assert bc["tir"] == pytest.approx(-6.648822533728384)
    assert bc["payback"] is None
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_senza_motori_non_convinte():
    # Fattore motori 1 = niente risparmio dai
    # motori efficienti: il caso diventa
    # NON_CONVIENTE.
    bc = _variante(f_eff=1)
    assert bc["e_lav_alt_kwh_e_anno"] == pytest.approx(108000.0)
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(124500.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(45080.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(6706.666666666664)
    assert bc["van"] == pytest.approx(-15387.093423935528)
    assert bc["tir"] == pytest.approx(2.184192780149768)
    assert bc["payback"] == 13
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(10.17857142857143)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_senza_inverter_non_convinte():
    # Fattore inverter 1 = niente risparmio
    # dall'aspirazione: il caso diventa
    # NON_CONVIENTE.
    bc = _variante(f_asp=1)
    assert bc["e_asp_alt_kwh_e_anno"] == pytest.approx(30000.0)
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(121800.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(44432.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(7354.666666666664)
    assert bc["van"] == pytest.approx(-8661.075015194507)
    assert bc["tir"] == pytest.approx(3.4514396210841443)
    assert bc["payback"] == 12
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(1.5000000000000002)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_capex_marginale_e_non_convinte():
    bc = _variante(capex=120000)
    assert bc["risparmio_eur_anno"] == pytest.approx(10594.666666666664)
    assert bc["van"] == pytest.approx(-10030.982971489408)
    assert bc["tir"] == pytest.approx(3.7360274767017336)
    assert bc["payback"] == 12
    assert bc["verdetto"] == "MARGINALE"
    bc2 = _variante(capex=150000)
    assert bc2["van"] == pytest.approx(-40030.9829714894)
    assert bc2["tir"] == pytest.approx(0.7309156048444805)
    assert bc2["payback"] == 15
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_om_alt_30000_non_calcolabile():
    # O&M alt 30.000: risparmio negativo negli
    # helper (calcolabile, non solleva), verdetto
    # NON_CALCOLABILE; stessa guard della UI.
    bc = _variante(om_alt=30000)
    assert bc["valid"] is True
    assert bc["c_alt_eur_anno"] == pytest.approx(59192.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-7405.333333333336)
    assert bc["van"] == pytest.approx(-161864.82765874002)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"]
    assert bc["payback"] is None
    assert bc["tir"] is None
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(199.17857142857144)


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(73920.0)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(-3190.792336930007)
    assert bc2["payback"] == 9
    assert bc2["verdetto"] == "MARGINALE"


def test_variante_prezzo_el_alto_aumenta_risparmio_convinte():
    # Elettricita' a 400 EUR/MWh: il risparmio
    # SALE perche' l'alternativa consuma meno
    # elettricita' della base; il caso resta
    # CONVIENTE e il breakeven resta n/d.
    bc = _variante(p_el=400)
    assert bc["c_base_eur_anno"] == pytest.approx(73866.66666666667)
    assert bc["c_alt_eur_anno"] == pytest.approx(58520.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(15346.666666666672)
    assert bc["van"] == pytest.approx(74293.15202594484)
    assert bc["tir"] == pytest.approx(16.141631905547055)
    assert bc["payback"] == 6
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_biomassa_totale_convinte():
    # Biomassa 100 %: gas alternativo zero, il
    # risparmio sale a 13.794,67 EUR/anno.
    bc = _variante(f_bio=1)
    assert bc["gas_alt_kwh_anno"] == 0.0
    assert bc["c_alt_eur_anno"] == pytest.approx(37992.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(13794.666666666664)
    assert bc["van"] == pytest.approx(58183.9227506885)
    assert bc["tir"] == pytest.approx(13.936226948833497)
    assert bc["payback"] == 7
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_calore_zero_breakeven_none():
    # Calore specifico zero: gas base zero,
    # breakeven None, risparmio solo elettrico
    # (3.128,00 EUR/anno) e VAN negativa oltre la
    # tolleranza, quindi NON_CONVIENTE.
    bc = _variante(q_risc_kwh_th_m3=0)
    assert bc["q_risc_kwh_th_anno"] == 0.0
    assert bc["gas_base_kwh_anno"] == 0.0
    assert bc["gas_alt_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(3128.0)
    assert bc["van"] == pytest.approx(-52532.42965657114)
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_monotonia_prezzo_gas_crescente():
    base = mh818_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas=101)["risparmio_eur_anno"]
    basso = _variante(p_gas=99)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(74.66666666666424, abs=1e-2)
    assert base - basso == pytest.approx(74.66666666666424, abs=1e-2)


def test_monotonia_f_bio_crescente_risparmio_cresce():
    assert _variante(f_bio=1.0)["risparmio_eur_anno"] > \
        mh818_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(f_bio=0.0)["risparmio_eur_anno"] < \
        mh818_demo_calcoli()["risparmio_eur_anno"]


def test_demo_deterministica_due_chiamate():
    a = mh818_demo_calcoli()
    b = mh818_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh818_demo().keys()) == {
        "legno_m3", "e_seg_kwh_e_m3", "e_pial_kwh_e_m3",
        "e_lev_kwh_e_m3", "f_eff", "e_asp_kwh_e_m3", "f_asp",
        "q_risc_kwh_th_m3", "f_bio", "eta_cald",
        "p_el", "p_gas", "om_base", "om_alt",
        "capex", "wacc_pct", "vita_anni",
        "tolleranza_pct"}


# ---------------------------------------------------------------- degenere
def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"legno_m3": 0},
               {"legno_m3": -10},
               {"e_seg_kwh_e_m3": -0.1},
               {"e_pial_kwh_e_m3": -0.1},
               {"e_lev_kwh_e_m3": -0.1},
               {"f_eff": -0.1}, {"f_eff": 1.01},
               {"e_asp_kwh_e_m3": -0.1},
               {"f_asp": -0.1}, {"f_asp": 1.01},
               {"q_risc_kwh_th_m3": -0.1},
               {"f_bio": -0.1}, {"f_bio": 1.01},
               {"eta_cald": 0}, {"eta_cald": 1.01},
               {"p_el": 0}, {"p_el": -1},
               {"p_gas": 0}, {"p_gas": -1},
               {"om_base": -100},
               {"om_alt": -100},
               {"capex": 0}, {"capex": -1},
               {"wacc_pct": -1},
               {"vita_anni": 0}, {"vita_anni": 2.5},
               {"tolleranza_pct": -1}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh818_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"legno_m3": "1200"},
               {"legno_m3": float("nan")},
               {"p_gas": float("inf")},
               {"capex": True},
               {"f_bio": "0.70"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh818_valida(**d)["valido"] is False


def test_zeri_ammessi_non_sollevano_e_nessuna_divergenza():
    # Zeri ammessi in entrambi (helper e UI):
    # specifici elettrici, fattori 0 e 1,
    # calore specifico, O&M, WACC, tolleranza.
    # Qui si verifica che non sollevano e
    # restano calcolabili.
    for kw in ({"e_seg_kwh_e_m3": 0},
               {"e_pial_kwh_e_m3": 0},
               {"e_lev_kwh_e_m3": 0},
               {"f_eff": 0},
               {"f_eff": 1},
               {"e_asp_kwh_e_m3": 0},
               {"f_asp": 0},
               {"f_asp": 1},
               {"q_risc_kwh_th_m3": 0},
               {"f_bio": 0},
               {"f_bio": 1},
               {"om_base": 0},
               {"om_alt": 0},
               {"wacc_pct": 0},
               {"tolleranza_pct": 0}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["verdetto"] in ("CONVIENTE", "MARGINALE",
                                  "NON_CONVIENTE", "NON_CALCOLABILE")


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    bc = _variante(om_alt=30000)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] <= 0.0
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"]


def test_pareggio_esatto_tolleranza_float():
    # A pareggio esatto (prezzo gas = breakeven
    # della variante senza motori) il risparmio
    # e' zero (circa 0.0, quindi guard
    # NON_CALCOLABILE): in nessun caso CONVIENTE.
    be = _variante(f_eff=1)["breakeven_gas_eur_mwh"]
    bc = _variante(f_eff=1, p_gas=be)
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["verdetto"] != "CONVIENTE"
    bc2 = _variante(f_eff=1, p_gas=be + 1)
    assert bc2["risparmio_eur_anno"] == pytest.approx(74.66666666666424, abs=1e-2)
    # Risparmio positivo ma piccolo: VAN negativa oltre
    # la tolleranza, quindi NON_CONVIENTE (non CONVIENTE).
    assert bc2["verdetto"] == "NON_CONVIENTE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh818_demo_calcoli()
    testo = mh818_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_gas_eur_mwh" in testo
    assert "co2_evitata_t_anno" in testo
    assert "q_risc_kwh_th_anno" in testo
    assert "e_asp_alt_kwh_e_anno" in testo
    assert "e_lav_alt_kwh_e_anno" in testo
    assert "gas_alt_kwh_anno" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh818_demo_calcoli()
    testo = mh818_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"e_asp_base_kwh_e_anno;{bc['e_asp_base_kwh_e_anno']}" in testo
    assert f"gas_base_kwh_anno;{bc['gas_base_kwh_anno']}" in testo
    assert f"q_risc_kwh_th_anno;{bc['q_risc_kwh_th_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh818_demo_calcoli()
    testo = mh818_csv(bc, _demo_kwargs())
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
    return ["mh" + "81" + "7", "st" + "81" + "7",
            "tab" + "81" + "7", "w" + "81" + "8"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w819_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w819_ui.py"))
    ast.parse(src)
    assert src.startswith("# W819")
    assert "with tab818:" in src


def test_ui_apre_scheda_attesa_una_volta():
    """Il frammento UI apre la scheda attesa, una sola volta."""
    src = _leggi("w819_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert m.group(1) == "818"
    assert src.count("with tab818:") == 1
    assert src.count("    with tab818:") == 1


def test_ui_titolo_atteso():
    src = _leggi("w819_ui.py")
    titolo = ("Falegnameria: motori efficienti + "
              "aspirazione con inverter + caldaia a "
              "biomassa da scarti battono motori "
              "tradizionali + aspirazione sempre accesa "
              "+ caldaia a gas?")
    assert src.count(titolo) == 2


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w819_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_helpers_senza_costanti_di_modulo():
    src = _leggi("w819_helpers.py")
    albero = ast.parse(src)
    for nodo in albero.body:
        assert not isinstance(nodo, ast.Assign), \
            "costante di modulo vietata: i fattori devono essere letterali dentro le funzioni"


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w819_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st818_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) == 28
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w819_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 4
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_ui_guard_degenere_identica_helper():
    """La guard UI della scheda dichiara NON_CALCOLABILE
    per gli stessi casi degeneri degli helper:
    legno <= 0, rendimento caldaia <= 0 o sopra 1,
    prezzi <= 0, CAPEX <= 0, vita <= 0 (nessuna
    divergenza helper-vs-UI)."""
    src = _leggi("w819_ui.py")
    assert "float(_lg818) <= 0.0" in src
    assert "float(_etac818) <= 0.0" in src
    assert "float(_etac818) > 1.0" in src
    assert "float(_pel818) <= 0.0" in src
    assert "float(_pg818) <= 0.0" in src
    assert "float(_cx818) <= 0.0" in src
    assert "int(_vita818) <= 0" in src
    assert "Verdetto: NON_CALCOLABILE" in src


def test_ui_chiamata_calcola_keyword_uguali_firma():
    """La chiamata UI a calcola usa come keyword
    esattamente i parametri della firma helper."""
    src = textwrap.dedent(_leggi("w819_ui.py"))
    albero = ast.parse(src)
    chiamate = []
    for nodo in ast.walk(albero):
        if isinstance(nodo, ast.Call):
            func = nodo.func
            if isinstance(func, ast.Name) and func.id == "mh818_calcola":
                chiamate.append({kw.arg for kw in nodo.keywords})
    assert len(chiamate) == 1
    attesi = set(inspect.signature(mh818_calcola).parameters.keys())
    assert chiamate[0] == attesi


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w819_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def818[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w819_ui.py")
        usate = set(re.findall(r'_def818\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 18
        assert usate <= set(mh818_demo().keys())
