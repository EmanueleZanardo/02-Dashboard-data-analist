"""Test nuova scheda "Frantoio oleario:
pompa di calore + recupero calore acque
reflue + motori efficienti battono caldaia
a gas + motori tradizionali?" (titolo
completo nel frammento UI).

Business case deterministico di un
frantoio oleario guidato dalle TONNELLATE
DI OLIVE molite in un anno: Q_acq =
olive_t x q_acq; Q_net = Q_acq x (1 -
f_rec) (il recupero riduce solo l'acqua
calda); E_pdc = Q_net / cop_pdc;
E_mol_base = olive_t x e_mol; E_centr_base
= olive_t x e_centr; E_lav_base = olive_t x
e_lav; E_mol_alt = E_mol_base x f_eff;
E_centr_alt = E_centr_base x f_eff (i
motori efficienti riducono solo molitura
e centrifuga); E_lav_alt = E_lav_base (il
lavaggio resta invariato); E_base =
E_mol_base + E_centr_base + E_lav_base;
E_alt = E_mol_alt + E_centr_alt +
E_lav_base + E_pdc; gas_base = Q_acq /
eta_cald; gas_alt = 0 (tutta l'acqua calda
passa alla pompa di calore); C_base =
E_base / 1000 x p_el + gas_base / 1000 x
p_gas + OM_base; C_alt = E_alt / 1000 x
p_el + OM_alt; risparmio = C_base - C_alt;
CO2 evitata = (E_base x 0,35 + gas_base x
0,20 - E_alt x 0,35) / 1000 (fattori
letterali); flussi [-CAPEX, risparmio x
vita]; VAN, TIR, payback (primo anno con
cumulato >= 0); breakeven gas = (E_alt /
1000 x p_el + OM_alt - E_base / 1000 x
p_el - OM_base) x 1000 / (gas_base -
gas_alt) EUR/MWh, None se gas_base <=
gas_alt o numeratore < 0, SOGLIA MINIMA
quando esiste. Nel demo il breakeven e'
42,90 EUR/MWh (numeratore 4.576,00 EUR,
denominatore 106.666,66666666666
kWh/anno). Verdetto: NON_CALCOLABILE se
input degenere (olive <= 0, specifici
negativi, fattore motori fuori [0, 1],
acqua calda specifica negativa, recupero
fuori [0, 1], COP <= 0, rendimento caldaia
<= 0 o sopra 1, prezzi <= 0, O&M negativi,
CAPEX <= 0, WACC negativo, vita <= 0,
tolleranza negativa) o se risparmio <= 0
(guard degenere: UI salta KPI, grafico,
tabella e CSV); altrimenti CONVIENTE se
VAN > 0, MARGINALE se VAN negativa entro
tolleranza % del CAPEX, NON_CONVIENTE se
VAN negativa oltre la tolleranza. Guard UI
IDENTICA agli helper: nessuna divergenza
di verdetto. Tutti gli slider UI hanno
minimo 0, quindi i casi negativi sono NON
RAGGIUNGIBILI via slider, ma la guard li
controlla comunque; i casi = 0 raggiungibili
via slider sono bloccati in UI esattamente
come negli helper dove previsto (olive,
COP, rendimento caldaia, prezzi, CAPEX,
vita). Gli zeri ammessi in entrambi
(specifici elettrici, fattore motori 0 o 1,
acqua calda specifica, recupero 0 o 1, O&M,
WACC, tolleranza) non creano divergenza:
con acqua calda specifica zero il gas base
e' zero e il breakeven e' None, e il caso
resta calcolabile in entrambi. COP sopra 6,
WACC sopra 20 % e tolleranza sopra 100 %
sono ammessi negli helper e limitati solo
dagli slider UI (6, 20, 100): nessuna
divergenza nel range raggiungibile, perche'
la guard controlla solo gli stessi limiti
degli helper. Distinzione esplicita:
distinto dal caseificio (litri di latte,
pastorizzazione: qui niente latte, niente
pastorizzazione), dal birrificio (ettolitri
di birra, bollitura del mosto: qui niente
mosto, niente bollitura), dalla discoteca
(m2 di locale, serate: qui niente m2 di
locale, niente serate), dalla lavanderia
(kg di biancheria: qui niente biancheria,
niente capi da lavare): qui driver
TONNELLATE DI OLIVE + RECUPERO + MOTORI
EFFICIENTI.

Demo (frantoio): 800 t di olive, molitura
specifica 60 (48.000 kWh_e/anno),
centrifuga specifica 45 (36.000
kWh_e/anno), lavaggio specifico 15
(12.000 kWh_e/anno), fattore motori
efficienti 0,80 (molitura alternativa
38.400, centrifuga alternativa 28.800
kWh_e/anno), acqua calda specifica 120
(96.000 kWh_th/anno), recupero 0,30 (acqua
calda netta 67.200 kWh_th/anno), COP pompa
di calore 3,5 (19.200 kWh_e/anno),
rendimento caldaia 0,90 (gas base
106.666,66666666666 e gas alternativo 0
kWh/anno), prezzi elettricita' 240 e gas
100 EUR/MWh, O&M base 8.000 e alternativo
12.000 EUR/anno, CAPEX 45.000 EUR, WACC
5 %, vita 15 anni, tolleranza 10 % del
CAPEX. Valori calcolati eseguendo
mh817_demo_calcoli(): E_base 96.000, E_alt
98.400, C_base 41.706,666666666664, C_alt
35.616, risparmio 6.090,666666666664,
CO2_base 54,93333333333333, CO2_alt 34,44,
CO2_evitata 20,49333333333333, VAN
18.219,03722454523, TIR 10,51318938149353
%, payback 8, breakeven gas 42,90 EUR/MWh
(SOGLIA MINIMA), verdetto CONVIENTE.
"""

import ast
import inspect
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w818_helpers import (
    demo_calcoli,
    mh817_breakeven_gas,
    mh817_c_alt,
    mh817_c_base,
    mh817_calcola,
    mh817_co2_alt,
    mh817_co2_base,
    mh817_co2_evitata,
    mh817_csv,
    mh817_demo,
    mh817_demo_calcoli,
    mh817_e_alt,
    mh817_e_base,
    mh817_e_centr_base,
    mh817_e_lav_base,
    mh817_e_mol_base,
    mh817_e_mot_alt,
    mh817_e_pdc,
    mh817_eta,
    mh817_flussi,
    mh817_frazione,
    mh817_gas_alt,
    mh817_gas_base,
    mh817_int_pos,
    mh817_nneg,
    mh817_num,
    mh817_payback,
    mh817_pos,
    mh817_q_acq,
    mh817_q_acq_net,
    mh817_risparmio,
    mh817_tir,
    mh817_valida,
    mh817_van,
    mh817_verdetto,
)

_DEMO = {
    "q_acq_kwh_th_anno": 96000.0,
    "q_acq_net_kwh_th_anno": 67200.0,
    "e_pdc_kwh_e_anno": 19200.0,
    "e_mol_base_kwh_e_anno": 48000.0,
    "e_mol_alt_kwh_e_anno": 38400.0,
    "e_centr_base_kwh_e_anno": 36000.0,
    "e_centr_alt_kwh_e_anno": 28800.0,
    "e_lav_base_kwh_e_anno": 12000.0,
    "e_base_kwh_e_anno": 96000.0,
    "e_alt_kwh_e_anno": 98400.0,
    "gas_base_kwh_anno": 106666.66666666666,
    "gas_alt_kwh_anno": 0.0,
    "c_base_eur_anno": 41706.666666666664,
    "c_alt_eur_anno": 35616.0,
    "risparmio_eur_anno": 6090.666666666664,
    "co2_base_t_anno": 54.93333333333333,
    "co2_alt_t_anno": 34.44,
    "co2_evitata_t_anno": 20.49333333333333,
    "van": 18219.03722454523,
    "tir": 10.51318938149353,
}


def _demo_kwargs():
    return dict(mh817_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh817_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh817_num(3, "x") == 3.0
    assert mh817_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh817_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh817_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh817_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh817_pos(0, "x")
    with pytest.raises(ValueError):
        mh817_pos(-1, "x")
    assert mh817_pos(0.5, "x") == 0.5


def test_frazione_limiti():
    assert mh817_frazione(0, "x") == 0.0
    assert mh817_frazione(1, "x") == 1.0
    assert mh817_frazione(0.80, "x") == 0.80
    with pytest.raises(ValueError):
        mh817_frazione(-0.01, "x")
    with pytest.raises(ValueError):
        mh817_frazione(1.01, "x")


def test_eta_limiti():
    assert mh817_eta(1, "x") == 1.0
    assert mh817_eta(0.90, "x") == 0.90
    with pytest.raises(ValueError):
        mh817_eta(0, "x")
    with pytest.raises(ValueError):
        mh817_eta(-0.1, "x")
    with pytest.raises(ValueError):
        mh817_eta(1.01, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh817_int_pos(5.0, "x") == 5
    assert mh817_int_pos(15.0, "x") == 15
    with pytest.raises(ValueError):
        mh817_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh817_int_pos(0, "x")


# ---------------------------------------------------------------- fisica base
def test_q_acq_e_q_net_e_pdc():
    assert mh817_q_acq(800, 120) == 96000.0
    assert mh817_q_acq_net(96000.0, 0.30) == 67200.0
    assert mh817_q_acq_net(96000.0, 0) == 96000.0
    assert mh817_q_acq_net(96000.0, 1) == 0.0
    with pytest.raises(ValueError):
        mh817_q_acq_net(96000.0, 1.01)
    assert mh817_e_pdc(67200.0, 3.5) == 19200.0
    with pytest.raises(ValueError):
        mh817_e_pdc(67200.0, 0)
    # COP sopra 6 ammessi negli helper (slider li limita a 6).
    assert mh817_e_pdc(67200.0, 7.0) == pytest.approx(9600.0)
    with pytest.raises(ValueError):
        mh817_q_acq(0, 120)
    with pytest.raises(ValueError):
        mh817_q_acq(800, -1)


def test_e_mol_centr_lav_e_mot_alt():
    assert mh817_e_mol_base(800, 60) == 48000.0
    assert mh817_e_centr_base(800, 45) == 36000.0
    assert mh817_e_lav_base(800, 15) == 12000.0
    assert mh817_e_mot_alt(48000.0, 0.80) == 38400.0
    assert mh817_e_mot_alt(36000.0, 0.80) == 28800.0
    assert mh817_e_mot_alt(48000.0, 1) == 48000.0
    assert mh817_e_mot_alt(48000.0, 0) == 0.0
    with pytest.raises(ValueError):
        mh817_e_mot_alt(48000.0, 1.01)
    with pytest.raises(ValueError):
        mh817_e_mol_base(0, 60)


def test_e_base_e_alt_lavaggio_invariato():
    assert mh817_e_base(48000.0, 36000.0, 12000.0) == 96000.0
    assert mh817_e_alt(38400.0, 28800.0, 12000.0,
                       19200.0) == 98400.0
    with pytest.raises(ValueError):
        mh817_e_base(-1, 36000.0, 12000.0)
    with pytest.raises(ValueError):
        mh817_e_alt(38400.0, 28800.0, 12000.0, -1)


def test_gas_base_alt_zero():
    assert mh817_gas_base(96000.0, 0.90) == pytest.approx(106666.66666666666)
    assert mh817_gas_base(0, 0.90) == 0.0
    assert mh817_gas_alt() == 0.0
    with pytest.raises(ValueError):
        mh817_gas_base(96000.0, 0)
    with pytest.raises(ValueError):
        mh817_gas_base(96000.0, 1.01)


def test_c_base_c_alt_scomposizione():
    assert mh817_c_base(96000.0, 240, 106666.66666666666, 100,
                        8000) == pytest.approx(41706.666666666664)
    assert mh817_c_alt(98400.0, 240, 12000) == pytest.approx(35616.0)
    with pytest.raises(ValueError):
        mh817_c_base(96000.0, 0, 106666.66666666666, 100, 8000)
    with pytest.raises(ValueError):
        mh817_c_alt(98400.0, 0, 12000)
    with pytest.raises(ValueError):
        mh817_c_base(96000.0, 240, 106666.66666666666, 100, -1)


def test_risparmio_segno():
    assert mh817_risparmio(41706.666666666664, 35616.0) == pytest.approx(6090.666666666664)
    assert mh817_risparmio(35616.0, 35616.0) == pytest.approx(0.0, abs=1e-9)


def test_co2_base_alt_evitata():
    assert mh817_co2_base(96000.0, 106666.66666666666) == pytest.approx(54.93333333333333)
    assert mh817_co2_alt(98400.0) == pytest.approx(34.44)
    assert mh817_co2_evitata(96000.0, 106666.66666666666,
                             98400.0) == pytest.approx(20.49333333333333)
    assert mh817_co2_base(0, 0) == 0.0
    assert mh817_co2_alt(0) == 0.0
    with pytest.raises(ValueError):
        mh817_co2_base(96000.0, -1)
    with pytest.raises(ValueError):
        mh817_co2_alt(-1)


def test_breakeven_demo_e_varianti():
    bc = mh817_demo_calcoli()
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(42.90)
    assert mh817_breakeven_gas(98400.0, 240, 12000, 96000.0,
                               8000, 106666.66666666666,
                               0.0) == pytest.approx(42.90)
    # Denominatore nullo (gas_base = gas_alt = 0) -> None.
    assert mh817_breakeven_gas(98400.0, 240, 12000, 96000.0,
                               8000, 0.0, 0.0) is None
    # Variante acqua calda zero -> breakeven None.
    assert _variante(q_acq_kwh_th_t=0)["breakeven_gas_eur_mwh"] is None
    with pytest.raises(ValueError):
        mh817_breakeven_gas(98400.0, 240, 12000, 96000.0,
                            8000, -1, 0.0)


def test_breakeven_verifica_pareggio_su_demo():
    be = mh817_demo_calcoli()["breakeven_gas_eur_mwh"]
    bc = _variante(p_gas=be)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_breakeven_soglia_minima_su_demo():
    be = mh817_demo_calcoli()["breakeven_gas_eur_mwh"]
    bc_alto = _variante(p_gas=be + 1)
    bc_basso = _variante(p_gas=be - 1)
    assert bc_alto["c_alt_eur_anno"] < bc_alto["c_base_eur_anno"]
    assert bc_basso["c_alt_eur_anno"] > bc_basso["c_base_eur_anno"]
    assert bc_alto["risparmio_eur_anno"] > 0.0
    assert bc_basso["verdetto"] == "NON_CALCOLABILE"


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh817_flussi(45000, 6090.666666666664, 15)
    assert len(fl) == 16
    assert fl[0] == -45000
    assert all(f == pytest.approx(6090.666666666664) for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh817_demo_calcoli()
    assert bc["van"] == pytest.approx(18219.03722454523)
    assert mh817_van([-45000] + [6090.666666666664] * 15,
                     0) == pytest.approx(46360.0)
    assert mh817_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh817_demo_calcoli()
    assert bc["tir"] == pytest.approx(10.51318938149353)
    assert mh817_tir([-45000] + [6090.666666666664] * 15) == \
        pytest.approx(0.1051318938149353)
    tir = mh817_tir([-45000] + [6090.666666666664] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-45000] + [6090.666666666664] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh817_payback([-45000] + [6090.666666666664] * 15) == 8
    assert mh817_payback([-45000] + [-1000.0] * 15) is None
    assert mh817_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh817_verdetto(6090.666666666664, 18219.03722454523, 45000,
                          10.0) == "CONVIENTE"
    assert mh817_verdetto(6090.666666666664, -1500.0, 45000,
                          10.0) == "MARGINALE"
    assert mh817_verdetto(6090.666666666664, -4500.0, 45000, 10.0) == "MARGINALE"
    assert mh817_verdetto(6090.666666666664, -4500.01, 45000, 10.0) == "NON_CONVIENTE"
    assert mh817_verdetto(6090.666666666664, 0.0, 45000, 10.0) == "MARGINALE"
    assert mh817_verdetto(0.0, 18219.04, 45000,
                          10.0) == "NON_CALCOLABILE"
    assert mh817_verdetto(-1909.33, -64818.23, 45000,
                          10.0) == "NON_CALCOLABILE"
    assert mh817_verdetto(None, 18219.04, 45000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh817_verdetto(float("nan"), 18219.04, 45000, 10.0)
    with pytest.raises(ValueError):
        mh817_verdetto(6090.666666666664, 18219.04, 0, 10.0)
    with pytest.raises(ValueError):
        mh817_verdetto(6090.666666666664, 18219.04, 45000, -1)


def test_valida_demo_ok():
    v = mh817_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("olive_t", "800"),
                       ("olive_t", float("nan")),
                       ("olive_t", float("inf")),
                       ("olive_t", True),
                       ("p_gas", None),
                       ("f_rec", "0.30")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh817_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("olive_t", 0),
                          ("olive_t", -10),
                          ("e_mol_kwh_e_t", -0.1),
                          ("e_centr_kwh_e_t", -0.1),
                          ("e_lav_kwh_e_t", -0.1),
                          ("f_eff", -0.1),
                          ("f_eff", 1.01),
                          ("q_acq_kwh_th_t", -0.1),
                          ("f_rec", -0.1),
                          ("f_rec", 1.01),
                          ("cop_pdc", 0),
                          ("cop_pdc", -1),
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
        assert mh817_valida(**d)["valido"] is False


def test_valida_accetta_limiti_e_nessun_tetto_cop_wacc_tolleranza():
    d = _demo_kwargs()
    d.update({"e_mol_kwh_e_t": 0,
              "e_centr_kwh_e_t": 0,
              "e_lav_kwh_e_t": 0,
              "f_eff": 0,
              "q_acq_kwh_th_t": 0,
              "f_rec": 0,
              "om_base": 0, "om_alt": 0,
              "wacc_pct": 0,
              "tolleranza_pct": 0})
    assert mh817_valida(**d)["valido"] is True
    d["f_eff"] = 1
    d["f_rec"] = 1
    d["eta_cald"] = 1
    # Il brief non impone tetti superiori a COP,
    # WACC e tolleranza: gli helper li ammettono.
    d["cop_pdc"] = 7.0
    d["wacc_pct"] = 60
    d["tolleranza_pct"] = 200
    assert mh817_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh817_demo()
    assert d["olive_t"] == 800
    assert d["e_mol_kwh_e_t"] == 60
    assert d["e_centr_kwh_e_t"] == 45
    assert d["e_lav_kwh_e_t"] == 15
    assert d["f_eff"] == 0.80
    assert d["q_acq_kwh_th_t"] == 120
    assert d["f_rec"] == 0.30
    assert d["cop_pdc"] == 3.5
    assert d["eta_cald"] == 0.90
    assert d["p_el"] == 240
    assert d["p_gas"] == 100
    assert d["om_base"] == 8000
    assert d["om_alt"] == 12000
    assert d["capex"] == 45000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    bc = mh817_demo_calcoli()
    for chiave, atteso in _DEMO.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert got == pytest.approx(atteso, rel=1e-9), chiave
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(42.90)
    assert demo_calcoli()["van"] == bc["van"]


def test_demo_calcoli_fisica_economia():
    bc = mh817_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(41706.666666666664)
    assert bc["c_alt_eur_anno"] == pytest.approx(35616.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(6090.666666666664)
    assert bc["co2_base_t_anno"] == pytest.approx(54.93333333333333)
    assert bc["co2_alt_t_anno"] == pytest.approx(34.44)
    assert bc["co2_evitata_t_anno"] == pytest.approx(20.49333333333333)
    assert bc["q_acq_kwh_th_anno"] == pytest.approx(96000.0)
    assert bc["q_acq_net_kwh_th_anno"] == pytest.approx(67200.0)
    assert bc["e_pdc_kwh_e_anno"] == pytest.approx(19200.0)
    assert bc["e_mol_base_kwh_e_anno"] == pytest.approx(48000.0)
    assert bc["e_mol_alt_kwh_e_anno"] == pytest.approx(38400.0)
    assert bc["e_centr_base_kwh_e_anno"] == pytest.approx(36000.0)
    assert bc["e_centr_alt_kwh_e_anno"] == pytest.approx(28800.0)
    assert bc["e_lav_base_kwh_e_anno"] == pytest.approx(12000.0)
    assert bc["e_base_kwh_e_anno"] == pytest.approx(96000.0)
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(98400.0)
    assert bc["gas_base_kwh_anno"] == pytest.approx(106666.66666666666)
    assert bc["gas_alt_kwh_anno"] == 0.0


def test_demo_flussi_e_cumulato():
    bc = mh817_demo_calcoli()
    assert bc["flussi"][0] == -45000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(6090.666666666664) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -45000
    assert righe.iloc[7]["Cumulato (EUR)"] == pytest.approx(-2365.3333333333503)
    assert righe.iloc[8]["Cumulato (EUR)"] == pytest.approx(3725.333333333314)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(46360.0)


def test_demo_tabella_righe():
    bc = mh817_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Acqua calda di processo (kWh_th/anno)"] == pytest.approx(96000.0)
    assert mappa["Acqua calda netta (kWh_th/anno)"] == pytest.approx(67200.0)
    assert mappa["Elettricita' pompa di calore (kWh_e/anno)"] == pytest.approx(19200.0)
    assert mappa["Molitura baseline (kWh_e/anno)"] == pytest.approx(48000.0)
    assert mappa["Molitura alternativa (kWh_e/anno)"] == pytest.approx(38400.0)
    assert mappa["Centrifuga baseline (kWh_e/anno)"] == pytest.approx(36000.0)
    assert mappa["Centrifuga alternativa (kWh_e/anno)"] == pytest.approx(28800.0)
    assert mappa["Lavaggio (kWh_e/anno)"] == pytest.approx(12000.0)
    assert mappa["Elettricita' base (kWh_e/anno)"] == pytest.approx(96000.0)
    assert mappa["Elettricita' alternativa (kWh_e/anno)"] == pytest.approx(98400.0)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(106666.66666666666)
    assert mappa["Gas alternativo (kWh/anno)"] == 0.0
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(41706.666666666664)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(35616.0)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(6090.666666666664)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(20.49333333333333)
    assert mappa["Payback (anni)"] == 8
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] == pytest.approx(42.90)


def test_demo_coerenza_interna():
    bc = mh817_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["q_acq_kwh_th_anno"] == pytest.approx(
        bc["olive_t"] * bc["q_acq_kwh_th_t"])
    assert bc["q_acq_net_kwh_th_anno"] == pytest.approx(
        bc["q_acq_kwh_th_anno"] * (1.0 - bc["f_rec"]))
    assert bc["e_pdc_kwh_e_anno"] == pytest.approx(
        bc["q_acq_net_kwh_th_anno"] / bc["cop_pdc"])
    assert bc["e_mol_base_kwh_e_anno"] == pytest.approx(
        bc["olive_t"] * bc["e_mol_kwh_e_t"])
    assert bc["e_centr_base_kwh_e_anno"] == pytest.approx(
        bc["olive_t"] * bc["e_centr_kwh_e_t"])
    assert bc["e_lav_base_kwh_e_anno"] == pytest.approx(
        bc["olive_t"] * bc["e_lav_kwh_e_t"])
    assert bc["e_mol_alt_kwh_e_anno"] == pytest.approx(
        bc["e_mol_base_kwh_e_anno"] * bc["f_eff"])
    assert bc["e_centr_alt_kwh_e_anno"] == pytest.approx(
        bc["e_centr_base_kwh_e_anno"] * bc["f_eff"])
    assert bc["e_base_kwh_e_anno"] == pytest.approx(
        bc["e_mol_base_kwh_e_anno"] + bc["e_centr_base_kwh_e_anno"]
        + bc["e_lav_base_kwh_e_anno"])
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(
        bc["e_mol_alt_kwh_e_anno"] + bc["e_centr_alt_kwh_e_anno"]
        + bc["e_lav_base_kwh_e_anno"] + bc["e_pdc_kwh_e_anno"])
    assert bc["gas_base_kwh_anno"] == pytest.approx(
        bc["q_acq_kwh_th_anno"] / bc["eta_cald"])
    assert bc["gas_alt_kwh_anno"] == 0.0
    assert bc["co2_evitata_t_anno"] == pytest.approx(
        bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])
    assert bc["c_base_eur_anno"] == pytest.approx(
        bc["e_base_kwh_e_anno"] / 1000.0 * bc["p_el"]
        + bc["gas_base_kwh_anno"] / 1000.0 * bc["p_gas"]
        + bc["om_base"])
    assert bc["c_alt_eur_anno"] == pytest.approx(
        bc["e_alt_kwh_e_anno"] / 1000.0 * bc["p_el"]
        + bc["om_alt"])


def test_demo_contro_riconteggio_indipendente():
    ol, em, ec, el, fe = 800, 60, 45, 15, 0.80
    qa, fr, cop, etac = 120, 0.30, 3.5, 0.90
    pel, pg = 240, 100
    omb, oma, cx = 8000, 12000, 45000
    wacc, vita = 5.0, 15
    q_acq = ol * qa
    q_net = q_acq * (1 - fr)
    e_pdc = q_net / cop
    e_mol_b = ol * em
    e_centr_b = ol * ec
    e_lav_b = ol * el
    e_mol_a = e_mol_b * fe
    e_centr_a = e_centr_b * fe
    eb = e_mol_b + e_centr_b + e_lav_b
    ea = e_mol_a + e_centr_a + e_lav_b + e_pdc
    gasb = q_acq / etac
    cb = eb / 1000.0 * pel + gasb / 1000.0 * pg + omb
    ca = ea / 1000.0 * pel + oma
    risp = cb - ca
    co2b = (eb * 0.35 + gasb * 0.20) / 1000.0
    co2a = ea * 0.35 / 1000.0
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    be = (ea / 1000.0 * pel + oma - eb / 1000.0 * pel - omb) * 1000.0 / gasb
    bc = mh817_demo_calcoli()
    assert bc["q_acq_kwh_th_anno"] == pytest.approx(q_acq)
    assert bc["q_acq_net_kwh_th_anno"] == pytest.approx(q_net)
    assert bc["e_pdc_kwh_e_anno"] == pytest.approx(e_pdc)
    assert bc["e_mol_base_kwh_e_anno"] == pytest.approx(e_mol_b)
    assert bc["e_mol_alt_kwh_e_anno"] == pytest.approx(e_mol_a)
    assert bc["e_centr_base_kwh_e_anno"] == pytest.approx(e_centr_b)
    assert bc["e_centr_alt_kwh_e_anno"] == pytest.approx(e_centr_a)
    assert bc["e_lav_base_kwh_e_anno"] == pytest.approx(e_lav_b)
    assert bc["e_base_kwh_e_anno"] == pytest.approx(eb)
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(ea)
    assert bc["gas_base_kwh_anno"] == pytest.approx(gasb)
    assert bc["gas_alt_kwh_anno"] == 0.0
    assert bc["c_base_eur_anno"] == pytest.approx(cb)
    assert bc["c_alt_eur_anno"] == pytest.approx(ca)
    assert bc["risparmio_eur_anno"] == pytest.approx(risp)
    assert bc["co2_base_t_anno"] == pytest.approx(co2b)
    assert bc["co2_alt_t_anno"] == pytest.approx(co2a)
    assert bc["co2_evitata_t_anno"] == pytest.approx(co2)
    assert bc["van"] == pytest.approx(van)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(be)


def test_demo_verdetto_coerente_con_risparmio_e_van():
    bc = mh817_demo_calcoli()
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] > 0.0
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["tir"] is not None and bc["tir"] > bc["wacc_pct"]
    assert bc["payback"] == 8


# ---------------------------------------------------------------- varianti
def test_variante_senza_recupero_marginale():
    # Recupero zero: la pompa di calore assorbe
    # 27.428,57 kWh_e/anno, il caso diventa
    # MARGINALE (VAN negativa entro il 10 %
    # del CAPEX).
    bc = _variante(f_rec=0)
    assert bc["q_acq_net_kwh_th_anno"] == pytest.approx(96000.0)
    assert bc["e_pdc_kwh_e_anno"] == pytest.approx(27428.571428571428)
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(106628.57142857142)
    assert bc["c_alt_eur_anno"] == pytest.approx(37590.857142857145)
    assert bc["risparmio_eur_anno"] == pytest.approx(4115.809523809519)
    assert bc["van"] == pytest.approx(-2279.304592570287)
    assert bc["tir"] == pytest.approx(4.240859516127725)
    assert bc["payback"] == 11
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(61.41428571428574)
    assert bc["verdetto"] == "MARGINALE"


def test_variante_senza_motori_non_convinte():
    # Fattore motori 1 = niente risparmio dai
    # motori efficienti: il caso diventa
    # NON_CONVIENTE.
    bc = _variante(f_eff=1)
    assert bc["e_mol_alt_kwh_e_anno"] == pytest.approx(48000.0)
    assert bc["e_centr_alt_kwh_e_anno"] == pytest.approx(36000.0)
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(115200.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(39648.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(2058.6666666666642)
    assert bc["van"] == pytest.approx(-23631.743985398924)
    assert bc["tir"] == pytest.approx(-4.375625110104751)
    assert bc["payback"] is None
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(80.7)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_capex_marginale_e_non_convinte():
    bc = _variante(capex=70000)
    assert bc["risparmio_eur_anno"] == pytest.approx(6090.666666666664)
    assert bc["van"] == pytest.approx(-6780.962775454771)
    assert bc["tir"] == pytest.approx(3.529855516651817)
    assert bc["payback"] == 12
    assert bc["verdetto"] == "MARGINALE"
    bc2 = _variante(capex=90000)
    assert bc2["van"] == pytest.approx(-26780.96277545477)
    assert bc2["payback"] == 15
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_om_alt_20000_non_calcolabile():
    # O&M alt 20.000: risparmio negativo negli
    # helper (calcolabile, non solleva), verdetto
    # NON_CALCOLABILE; stessa guard della UI.
    bc = _variante(om_alt=20000)
    assert bc["valid"] is True
    assert bc["c_alt_eur_anno"] == pytest.approx(43616.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-1909.3333333333358)
    assert bc["van"] == pytest.approx(-64818.2270808995)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"]
    assert bc["payback"] is None
    assert bc["tir"] is None
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(117.9)


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(46360.0)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(2030.5135420216066)
    assert bc2["payback"] == 8
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_prezzo_el_alto_riduce_risparmio_ma_convinte():
    # Elettricita' a 400 EUR/MWh: il risparmio
    # cala perche' l'alternativa consuma piu'
    # elettricita' della base, ma il caso resta
    # CONVIENTE; il breakeven sale a 46,50.
    bc = _variante(p_el=400)
    assert bc["c_base_eur_anno"] == pytest.approx(57066.666666666664)
    assert bc["c_alt_eur_anno"] == pytest.approx(51360.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(5706.666666666664)
    assert bc["van"] == pytest.approx(14233.24853788388)
    assert bc["tir"] == pytest.approx(9.374541541464676)
    assert bc["payback"] == 8
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(46.50000000000001)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_acqua_calda_zero_breakeven_none():
    # Acqua calda specifica zero: gas base zero,
    # breakeven None, risparmio solo dai motori
    # (32,00 EUR/anno) e VAN negativa oltre la
    # tolleranza, quindi NON_CONVIENTE.
    bc = _variante(q_acq_kwh_th_t=0)
    assert bc["q_acq_kwh_th_anno"] == 0.0
    assert bc["gas_base_kwh_anno"] == 0.0
    assert bc["gas_alt_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(32.0)
    assert bc["van"] == pytest.approx(-44667.850942778234)
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_monotonia_prezzo_gas_crescente():
    base = mh817_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas=101)["risparmio_eur_anno"]
    basso = _variante(p_gas=99)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(106.66666666666666, abs=1e-2)
    assert base - basso == pytest.approx(106.66666666666666, abs=1e-2)


def test_monotonia_f_rec_crescente_risparmio_cresce():
    assert _variante(f_rec=0.50)["risparmio_eur_anno"] > \
        mh817_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(f_rec=0.0)["risparmio_eur_anno"] < \
        mh817_demo_calcoli()["risparmio_eur_anno"]


def test_demo_deterministica_due_chiamate():
    a = mh817_demo_calcoli()
    b = mh817_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh817_demo().keys()) == {
        "olive_t", "e_mol_kwh_e_t", "e_centr_kwh_e_t",
        "e_lav_kwh_e_t", "f_eff", "q_acq_kwh_th_t", "f_rec",
        "cop_pdc", "eta_cald",
        "p_el", "p_gas", "om_base", "om_alt",
        "capex", "wacc_pct", "vita_anni",
        "tolleranza_pct"}


# ---------------------------------------------------------------- degenere
def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"olive_t": 0},
               {"olive_t": -10},
               {"e_mol_kwh_e_t": -0.1},
               {"e_centr_kwh_e_t": -0.1},
               {"e_lav_kwh_e_t": -0.1},
               {"f_eff": -0.1}, {"f_eff": 1.01},
               {"q_acq_kwh_th_t": -0.1},
               {"f_rec": -0.1}, {"f_rec": 1.01},
               {"cop_pdc": 0}, {"cop_pdc": -1},
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
        assert mh817_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"olive_t": "800"},
               {"olive_t": float("nan")},
               {"p_gas": float("inf")},
               {"capex": True},
               {"f_rec": "0.30"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh817_valida(**d)["valido"] is False


def test_zeri_ammessi_non_sollevano_e_nessuna_divergenza():
    # Zeri ammessi in entrambi (helper e UI):
    # specifici elettrici, fattore motori 0 e 1,
    # acqua calda specifica, recupero 0 e 1,
    # O&M, WACC, tolleranza. Qui si verifica
    # che non sollevano e restano calcolabili.
    for kw in ({"e_mol_kwh_e_t": 0},
               {"e_centr_kwh_e_t": 0},
               {"e_lav_kwh_e_t": 0},
               {"f_eff": 0},
               {"f_eff": 1},
               {"q_acq_kwh_th_t": 0},
               {"f_rec": 0},
               {"f_rec": 1},
               {"om_base": 0},
               {"om_alt": 0},
               {"wacc_pct": 0},
               {"tolleranza_pct": 0}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["verdetto"] in ("CONVIENTE", "MARGINALE",
                                  "NON_CONVIENTE", "NON_CALCOLABILE")


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    bc = _variante(om_alt=20000)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] <= 0.0
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"]


def test_pareggio_esatto_tolleranza_float():
    # A pareggio esatto (prezzo gas = breakeven
    # demo) il risparmio e' zero (circa 0.0,
    # quindi guard NON_CALCOLABILE): in nessun
    # caso CONVIENTE.
    be = mh817_demo_calcoli()["breakeven_gas_eur_mwh"]
    bc = _variante(p_gas=be)
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["verdetto"] != "CONVIENTE"
    bc2 = _variante(p_gas=be + 1)
    assert bc2["risparmio_eur_anno"] == pytest.approx(106.66666666666666, abs=1e-2)
    # Risparmio positivo ma piccolo: VAN negativa oltre
    # la tolleranza, quindi NON_CONVIENTE (non CONVIENTE).
    assert bc2["verdetto"] == "NON_CONVIENTE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh817_demo_calcoli()
    testo = mh817_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_gas_eur_mwh" in testo
    assert "co2_evitata_t_anno" in testo
    assert "q_acq_kwh_th_anno" in testo
    assert "e_pdc_kwh_e_anno" in testo
    assert "e_mol_alt_kwh_e_anno" in testo
    assert "e_centr_alt_kwh_e_anno" in testo
    assert "gas_alt_kwh_anno" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh817_demo_calcoli()
    testo = mh817_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"e_pdc_kwh_e_anno;{bc['e_pdc_kwh_e_anno']}" in testo
    assert f"gas_base_kwh_anno;{bc['gas_base_kwh_anno']}" in testo
    assert f"q_acq_kwh_th_anno;{bc['q_acq_kwh_th_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh817_demo_calcoli()
    testo = mh817_csv(bc, _demo_kwargs())
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
    return ["mh" + "81" + "6", "st" + "81" + "6",
            "tab" + "81" + "6", "w" + "81" + "7"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w818_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w818_ui.py"))
    ast.parse(src)
    assert src.startswith("# W818")
    assert "with tab817:" in src


def test_ui_apre_scheda_attesa_una_volta():
    """Il frammento UI apre la scheda attesa, una sola volta."""
    src = _leggi("w818_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert m.group(1) == "817"
    assert src.count("with tab817:") == 1
    assert src.count("    with tab817:") == 1


def test_ui_titolo_atteso():
    src = _leggi("w818_ui.py")
    titolo = ("Frantoio oleario: pompa di calore + "
              "recupero calore acque reflue + motori "
              "efficienti battono caldaia a gas + "
              "motori tradizionali?")
    assert src.count(titolo) == 2


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w818_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w818_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st817_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) == 27
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w818_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 4
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_ui_guard_degenere_identica_helper():
    """La guard UI della scheda dichiara NON_CALCOLABILE
    per gli stessi casi degeneri degli helper:
    olive <= 0, COP <= 0, rendimento caldaia
    <= 0 o sopra 1, prezzi <= 0, CAPEX <= 0,
    vita <= 0 (nessuna divergenza helper-vs-UI)."""
    src = _leggi("w818_ui.py")
    assert "float(_ol817) <= 0.0" in src
    assert "float(_cop817) <= 0.0" in src
    assert "float(_etac817) <= 0.0" in src
    assert "float(_etac817) > 1.0" in src
    assert "float(_pel817) <= 0.0" in src
    assert "float(_pg817) <= 0.0" in src
    assert "float(_cx817) <= 0.0" in src
    assert "int(_vita817) <= 0" in src
    assert "Verdetto: NON_CALCOLABILE" in src


def test_ui_chiamata_calcola_keyword_uguali_firma():
    """La chiamata UI a calcola usa come keyword
    esattamente i parametri della firma helper."""
    src = textwrap.dedent(_leggi("w818_ui.py"))
    albero = ast.parse(src)
    chiamate = []
    for nodo in ast.walk(albero):
        if isinstance(nodo, ast.Call):
            func = nodo.func
            if isinstance(func, ast.Name) and func.id == "mh817_calcola":
                chiamate.append({kw.arg for kw in nodo.keywords})
    assert len(chiamate) == 1
    attesi = set(inspect.signature(mh817_calcola).parameters.keys())
    assert chiamate[0] == attesi


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w818_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def817[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w818_ui.py")
        usate = set(re.findall(r'_def817\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 17
        assert usate <= set(mh817_demo().keys())
