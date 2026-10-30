"""Test nuova scheda "Tipografia:
presse efficienti + finitura servo +
recupero calore essiccazione battono
presse tradizionali + finitura
tradizionale + essiccazione a gas?"
(titolo completo nel frammento UI).

Business case deterministico di una
tipografia guidata dalle TONNELLATE DI
CARTA STAMPATA in un anno: E_stampa_base =
carta_t x e_stampa; E_fin_base = carta_t x
e_fin; E_stampa_alt = E_stampa_base x
f_stampa (le presse efficienti riducono
solo la stampa); E_fin_alt = E_fin_base x
f_fin (la finitura servo riduce solo la
finitura); E_base = E_stampa_base +
E_fin_base; E_alt = E_stampa_alt +
E_fin_alt; Q_ess = carta_t x q_ess;
gas_base = Q_ess / eta_cald; gas_alt =
Q_ess x (1 - f_rec) / eta_cald (il recupero
calore copre solo la quota f_rec del calore
di essiccazione); C_base = E_base / 1000
x p_el + gas_base / 1000 x p_gas + OM_base;
C_alt = E_alt / 1000 x p_el + gas_alt /
1000 x p_gas + OM_alt; risparmio = C_base
- C_alt; CO2 evitata = (E_base x 0,35 +
gas_base x 0,20 - E_alt x 0,35 - gas_alt x
0,20) / 1000 (fattori letterali, recupero a
zero); flussi [-CAPEX, risparmio x vita];
VAN, TIR, payback (primo anno con cumulato
>= 0); breakeven gas = (E_alt / 1000 x p_el
+ OM_alt - E_base / 1000 x p_el - OM_base)
x 1000 / (gas_base - gas_alt) EUR/MWh, None
se gas_base <= gas_alt o numeratore < 0,
SOGLIA MINIMA quando esiste. Nel demo il
breakeven e' None (numeratore -21.040,00
EUR, denominatore 320.000,00 kWh/anno):
l'alternativa vince gia' a prezzo gas zero.
Verdetto: NON_CALCOLABILE se input degenere
(carta <= 0, specifici negativi, fattori
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
helper dove previsto (carta, rendimento
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
Distinzione esplicita: distinto dalla
falegnameria (m3 di legno, lavorazioni del
legno: qui niente legno, niente segagione,
niente piallatura, niente levigatura),
dalla cartiera (produzione di carta da
pasta di legno: qui si stampa carta gia'
prodotta, niente spappolamento, niente
pasta di legno), dal frantoio (tonnellate
di olive, acqua calda di processo: qui
niente olive, niente malaxazione), dal
birrificio (ettolitri di birra, bollitura
del mosto: qui niente mosto, niente
bollitura): qui driver TONNELLATE DI CARTA
STAMPATA + PRESSE EFFICIENTI + FINITURA
SERVO + RECUPERO CALORE.

Demo (tipografia): 800 t di carta stampata,
stampa specifica 600 (480.000 kWh_e/anno),
finitura specifica 150 (120.000
kWh_e/anno), elettricita' base 600.000 e
alternativa 468.000 kWh_e/anno (fattore
presse 0,80: stampa alternativa 384.000;
fattore finitura 0,70: finitura alternativa
84.000 kWh_e/anno), calore specifico 900
(720.000 kWh_th/anno), quota recupero 0,40
(gas base 800.000 e gas alternativo 480.000
kWh/anno), rendimento caldaia 0,90, prezzi
elettricita' 220 e gas 90 EUR/MWh, O&M base
20.000 e alternativo 28.000 EUR/anno, CAPEX
300.000 EUR, WACC 5 %, vita 12 anni,
tolleranza 10 % del CAPEX. Valori
calcolati eseguendo mh819_demo_calcoli():
E_base 600.000, E_alt 468.000, C_base
224.000, C_alt 174.160, risparmio 49.840,
CO2_base 370,0, CO2_alt 259,8,
CO2_evitata 110,20, VAN 141.744,46156060853,
TIR 12,624238382300456 %, payback 7,
breakeven gas None (numeratore negativo),
verdetto CONVIENTE.
"""

import ast
import inspect
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w820_helpers import (
    demo_calcoli,
    mh819_breakeven_gas,
    mh819_c_alt,
    mh819_c_base,
    mh819_calcola,
    mh819_co2_alt,
    mh819_co2_base,
    mh819_co2_evitata,
    mh819_csv,
    mh819_demo,
    mh819_demo_calcoli,
    mh819_e_alt,
    mh819_e_base,
    mh819_e_fin_alt,
    mh819_e_fin_base,
    mh819_e_stampa_alt,
    mh819_e_stampa_base,
    mh819_eta,
    mh819_flussi,
    mh819_frazione,
    mh819_gas_alt,
    mh819_gas_base,
    mh819_int_pos,
    mh819_nneg,
    mh819_num,
    mh819_payback,
    mh819_pos,
    mh819_q_ess,
    mh819_risparmio,
    mh819_tir,
    mh819_valida,
    mh819_van,
    mh819_verdetto,
)

_DEMO = {
    "q_ess_kwh_th_anno": 720000.0,
    "e_stampa_base_kwh_e_anno": 480000.0,
    "e_fin_base_kwh_e_anno": 120000.0,
    "e_stampa_alt_kwh_e_anno": 384000.0,
    "e_fin_alt_kwh_e_anno": 84000.0,
    "e_base_kwh_e_anno": 600000.0,
    "e_alt_kwh_e_anno": 468000.0,
    "gas_base_kwh_anno": 800000.0,
    "gas_alt_kwh_anno": 480000.0,
    "c_base_eur_anno": 224000.0,
    "c_alt_eur_anno": 174160.0,
    "risparmio_eur_anno": 49840.0,
    "co2_base_t_anno": 370.0,
    "co2_alt_t_anno": 259.8,
    "co2_evitata_t_anno": 110.2,
    "van": 141744.46156060853,
    "tir": 12.624238382300456,
}


def _demo_kwargs():
    return dict(mh819_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh819_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh819_num(3, "x") == 3.0
    assert mh819_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh819_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh819_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh819_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh819_pos(0, "x")
    with pytest.raises(ValueError):
        mh819_pos(-1, "x")
    assert mh819_pos(0.5, "x") == 0.5


def test_frazione_limiti():
    assert mh819_frazione(0, "x") == 0.0
    assert mh819_frazione(1, "x") == 1.0
    assert mh819_frazione(0.80, "x") == 0.80
    with pytest.raises(ValueError):
        mh819_frazione(-0.01, "x")
    with pytest.raises(ValueError):
        mh819_frazione(1.01, "x")


def test_eta_limiti():
    assert mh819_eta(1, "x") == 1.0
    assert mh819_eta(0.90, "x") == 0.90
    with pytest.raises(ValueError):
        mh819_eta(0, "x")
    with pytest.raises(ValueError):
        mh819_eta(-0.1, "x")
    with pytest.raises(ValueError):
        mh819_eta(1.01, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh819_int_pos(5.0, "x") == 5
    assert mh819_int_pos(12.0, "x") == 12
    with pytest.raises(ValueError):
        mh819_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh819_int_pos(0, "x")


# ---------------------------------------------------------------- fisica base
def test_q_ess():
    assert mh819_q_ess(800, 900) == 720000.0
    assert mh819_q_ess(800, 0) == 0.0
    with pytest.raises(ValueError):
        mh819_q_ess(0, 900)
    with pytest.raises(ValueError):
        mh819_q_ess(800, -1)


def test_e_stampa_fin_e_base():
    assert mh819_e_stampa_base(800, 600) == 480000.0
    assert mh819_e_fin_base(800, 150) == 120000.0
    assert mh819_e_base(480000.0, 120000.0) == 600000.0
    with pytest.raises(ValueError):
        mh819_e_base(-1, 120000.0)
    with pytest.raises(ValueError):
        mh819_e_stampa_base(0, 600)


def test_e_stampa_alt_e_fin_alt():
    assert mh819_e_stampa_alt(480000.0, 0.80) == 384000.0
    assert mh819_e_stampa_alt(480000.0, 1) == 480000.0
    assert mh819_e_stampa_alt(480000.0, 0) == 0.0
    assert mh819_e_fin_alt(120000.0, 0.70) == 84000.0
    assert mh819_e_fin_alt(120000.0, 1) == 120000.0
    assert mh819_e_fin_alt(120000.0, 0) == 0.0
    with pytest.raises(ValueError):
        mh819_e_stampa_alt(480000.0, 1.01)
    with pytest.raises(ValueError):
        mh819_e_fin_alt(120000.0, 1.01)


def test_e_alt():
    assert mh819_e_alt(384000.0, 84000.0) == 468000.0
    with pytest.raises(ValueError):
        mh819_e_alt(384000.0, -1)


def test_gas_base_alt():
    assert mh819_gas_base(720000.0, 0.90) == pytest.approx(800000.0)
    assert mh819_gas_base(0, 0.90) == 0.0
    assert mh819_gas_alt(720000.0, 0.40, 0.90) == pytest.approx(480000.0)
    assert mh819_gas_alt(720000.0, 0, 0.90) == pytest.approx(800000.0)
    assert mh819_gas_alt(720000.0, 1, 0.90) == 0.0
    with pytest.raises(ValueError):
        mh819_gas_base(720000.0, 0)
    with pytest.raises(ValueError):
        mh819_gas_base(720000.0, 1.01)
    with pytest.raises(ValueError):
        mh819_gas_alt(720000.0, 1.01, 0.90)


def test_c_base_c_alt_scomposizione():
    assert mh819_c_base(600000.0, 220, 800000.0, 90,
                        20000) == pytest.approx(224000.0)
    assert mh819_c_alt(468000.0, 220, 480000.0, 90,
                       28000) == pytest.approx(174160.0)
    with pytest.raises(ValueError):
        mh819_c_base(600000.0, 0, 800000.0, 90, 20000)
    with pytest.raises(ValueError):
        mh819_c_alt(468000.0, 220, 480000.0, 0, 28000)
    with pytest.raises(ValueError):
        mh819_c_base(600000.0, 220, 800000.0, 90, -1)


def test_risparmio_segno():
    assert mh819_risparmio(224000.0, 174160.0) == pytest.approx(49840.0)
    assert mh819_risparmio(174160.0, 174160.0) == pytest.approx(0.0, abs=1e-9)


def test_co2_base_alt_evitata():
    assert mh819_co2_base(600000.0, 800000.0) == pytest.approx(370.0)
    assert mh819_co2_alt(468000.0, 480000.0) == pytest.approx(259.8)
    assert mh819_co2_evitata(600000.0, 800000.0,
                             468000.0, 480000.0) == pytest.approx(110.2)
    assert mh819_co2_base(0, 0) == 0.0
    assert mh819_co2_alt(0, 0) == 0.0
    with pytest.raises(ValueError):
        mh819_co2_base(600000.0, -1)
    with pytest.raises(ValueError):
        mh819_co2_alt(-1, 480000.0)


def test_breakeven_demo_none_numeratore_negativo():
    bc = mh819_demo_calcoli()
    assert bc["breakeven_gas_eur_mwh"] is None
    # Numeratore: 468000/1000*220 + 28000 - 600000/1000*220 - 20000 = -21040 < 0.
    assert mh819_breakeven_gas(468000.0, 220, 28000, 600000.0,
                               20000, 800000.0,
                               480000.0) is None
    # Denominatore nullo (gas_base = gas_alt) -> None.
    assert mh819_breakeven_gas(468000.0, 220, 28000, 600000.0,
                               20000, 0.0, 0.0) is None
    # Variante senza recupero: gas_base = gas_alt -> None.
    assert _variante(f_rec=0)["breakeven_gas_eur_mwh"] is None
    # Variante calore zero -> breakeven None.
    assert _variante(q_ess_kwh_th_t=0)["breakeven_gas_eur_mwh"] is None
    with pytest.raises(ValueError):
        mh819_breakeven_gas(468000.0, 220, 28000, 600000.0,
                            20000, -1, 480000.0)


def test_breakeven_variante_senza_presse_valore():
    # Senza presse efficienti il numeratore diventa
    # positivo e il breakeven esiste: 0,25 EUR/MWh.
    bc = _variante(f_stampa=1)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(0.25)
    assert mh819_breakeven_gas(564000.0, 220, 28000, 600000.0,
                               20000, 800000.0,
                               480000.0) == pytest.approx(0.25)


def test_breakeven_verifica_pareggio_su_variante():
    be = _variante(f_stampa=1)["breakeven_gas_eur_mwh"]
    bc = _variante(f_stampa=1, p_gas=be)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_breakeven_soglia_minima_su_variante():
    be = _variante(f_stampa=1)["breakeven_gas_eur_mwh"]
    bc_alto = _variante(f_stampa=1, p_gas=be + 1)
    bc_basso = _variante(f_stampa=1, p_gas=0.10)
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
    fl = mh819_flussi(300000, 49840.0, 12)
    assert len(fl) == 13
    assert fl[0] == -300000
    assert all(f == pytest.approx(49840.0) for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh819_demo_calcoli()
    assert bc["van"] == pytest.approx(141744.46156060853)
    assert mh819_van([-300000] + [49840.0] * 12,
                     0) == pytest.approx(298080.0)
    assert mh819_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh819_demo_calcoli()
    assert bc["tir"] == pytest.approx(12.624238382300456)
    assert mh819_tir([-300000] + [49840.0] * 12) == \
        pytest.approx(0.12624238382300456)
    tir = mh819_tir([-300000] + [49840.0] * 12)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-300000] + [49840.0] * 12))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh819_payback([-300000] + [49840.0] * 12) == 7
    assert mh819_payback([-300000] + [-1000.0] * 12) is None
    assert mh819_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh819_verdetto(49840.0, 141744.46156060853, 300000,
                          10.0) == "CONVIENTE"
    assert mh819_verdetto(49840.0, -1500.0, 300000,
                          10.0) == "MARGINALE"
    assert mh819_verdetto(49840.0, -30000.0, 300000, 10.0) == "MARGINALE"
    assert mh819_verdetto(49840.0, -30000.01, 300000, 10.0) == "NON_CONVIENTE"
    assert mh819_verdetto(49840.0, 0.0, 300000, 10.0) == "MARGINALE"
    assert mh819_verdetto(0.0, 141744.46, 300000,
                          10.0) == "NON_CALCOLABILE"
    assert mh819_verdetto(-12160.0, -407777.14, 300000,
                          10.0) == "NON_CALCOLABILE"
    assert mh819_verdetto(None, 141744.46, 300000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh819_verdetto(float("nan"), 141744.46, 300000, 10.0)
    with pytest.raises(ValueError):
        mh819_verdetto(49840.0, 141744.46, 0, 10.0)
    with pytest.raises(ValueError):
        mh819_verdetto(49840.0, 141744.46, 300000, -1)


def test_valida_demo_ok():
    v = mh819_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("carta_t", "800"),
                       ("carta_t", float("nan")),
                       ("carta_t", float("inf")),
                       ("carta_t", True),
                       ("p_gas", None),
                       ("f_rec", "0.40")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh819_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("carta_t", 0),
                          ("carta_t", -10),
                          ("e_stampa_kwh_e_t", -0.1),
                          ("e_fin_kwh_e_t", -0.1),
                          ("f_stampa", -0.1),
                          ("f_stampa", 1.01),
                          ("f_fin", -0.1),
                          ("f_fin", 1.01),
                          ("q_ess_kwh_th_t", -0.1),
                          ("f_rec", -0.1),
                          ("f_rec", 1.01),
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
        assert mh819_valida(**d)["valido"] is False


def test_valida_accetta_limiti_e_nessun_tetto_wacc_tolleranza():
    d = _demo_kwargs()
    d.update({"e_stampa_kwh_e_t": 0,
              "e_fin_kwh_e_t": 0,
              "f_stampa": 0,
              "f_fin": 0,
              "q_ess_kwh_th_t": 0,
              "f_rec": 0,
              "om_base": 0, "om_alt": 0,
              "wacc_pct": 0,
              "tolleranza_pct": 0})
    assert mh819_valida(**d)["valido"] is True
    d["f_stampa"] = 1
    d["f_fin"] = 1
    d["f_rec"] = 1
    d["eta_cald"] = 1
    # Il brief non impone tetti superiori a WACC
    # e tolleranza: gli helper li ammettono.
    d["wacc_pct"] = 60
    d["tolleranza_pct"] = 200
    assert mh819_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh819_demo()
    assert d["carta_t"] == 800
    assert d["e_stampa_kwh_e_t"] == 600
    assert d["e_fin_kwh_e_t"] == 150
    assert d["f_stampa"] == 0.80
    assert d["f_fin"] == 0.70
    assert d["q_ess_kwh_th_t"] == 900
    assert d["f_rec"] == 0.40
    assert d["eta_cald"] == 0.90
    assert d["p_el"] == 220
    assert d["p_gas"] == 90
    assert d["om_base"] == 20000
    assert d["om_alt"] == 28000
    assert d["capex"] == 300000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 12
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    bc = mh819_demo_calcoli()
    for chiave, atteso in _DEMO.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert got == pytest.approx(atteso, rel=1e-9), chiave
    assert bc["payback"] == 7
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True
    assert bc["breakeven_gas_eur_mwh"] is None
    assert demo_calcoli()["van"] == bc["van"]


def test_demo_calcoli_fisica_economia():
    bc = mh819_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(224000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(174160.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(49840.0)
    assert bc["co2_base_t_anno"] == pytest.approx(370.0)
    assert bc["co2_alt_t_anno"] == pytest.approx(259.8)
    assert bc["co2_evitata_t_anno"] == pytest.approx(110.2)
    assert bc["q_ess_kwh_th_anno"] == pytest.approx(720000.0)
    assert bc["e_stampa_base_kwh_e_anno"] == pytest.approx(480000.0)
    assert bc["e_fin_base_kwh_e_anno"] == pytest.approx(120000.0)
    assert bc["e_stampa_alt_kwh_e_anno"] == pytest.approx(384000.0)
    assert bc["e_fin_alt_kwh_e_anno"] == pytest.approx(84000.0)
    assert bc["e_base_kwh_e_anno"] == pytest.approx(600000.0)
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(468000.0)
    assert bc["gas_base_kwh_anno"] == pytest.approx(800000.0)
    assert bc["gas_alt_kwh_anno"] == pytest.approx(480000.0)


def test_demo_flussi_e_cumulato():
    bc = mh819_demo_calcoli()
    assert bc["flussi"][0] == -300000
    assert len(bc["flussi"]) == 13
    assert all(f == pytest.approx(49840.0) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -300000
    assert righe.iloc[6]["Cumulato (EUR)"] == pytest.approx(-960.0)
    assert righe.iloc[7]["Cumulato (EUR)"] == pytest.approx(48880.0)
    assert righe.iloc[12]["Cumulato (EUR)"] == pytest.approx(298080.0)


def test_demo_tabella_righe():
    bc = mh819_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Stampa baseline (kWh_e/anno)"] == pytest.approx(480000.0)
    assert mappa["Stampa alternativa (kWh_e/anno)"] == pytest.approx(384000.0)
    assert mappa["Finitura baseline (kWh_e/anno)"] == pytest.approx(120000.0)
    assert mappa["Finitura alternativa (kWh_e/anno)"] == pytest.approx(84000.0)
    assert mappa["Elettricita' base (kWh_e/anno)"] == pytest.approx(600000.0)
    assert mappa["Elettricita' alternativa (kWh_e/anno)"] == pytest.approx(468000.0)
    assert mappa["Calore essiccazione (kWh_th/anno)"] == pytest.approx(720000.0)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(800000.0)
    assert mappa["Gas alternativo (kWh/anno)"] == pytest.approx(480000.0)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(224000.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(174160.0)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(49840.0)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(110.2)
    assert mappa["Payback (anni)"] == 7
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] is None


def test_demo_coerenza_interna():
    bc = mh819_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["q_ess_kwh_th_anno"] == pytest.approx(
        bc["carta_t"] * bc["q_ess_kwh_th_t"])
    assert bc["e_stampa_base_kwh_e_anno"] == pytest.approx(
        bc["carta_t"] * bc["e_stampa_kwh_e_t"])
    assert bc["e_fin_base_kwh_e_anno"] == pytest.approx(
        bc["carta_t"] * bc["e_fin_kwh_e_t"])
    assert bc["e_stampa_alt_kwh_e_anno"] == pytest.approx(
        bc["e_stampa_base_kwh_e_anno"] * bc["f_stampa"])
    assert bc["e_fin_alt_kwh_e_anno"] == pytest.approx(
        bc["e_fin_base_kwh_e_anno"] * bc["f_fin"])
    assert bc["e_base_kwh_e_anno"] == pytest.approx(
        bc["e_stampa_base_kwh_e_anno"] + bc["e_fin_base_kwh_e_anno"])
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(
        bc["e_stampa_alt_kwh_e_anno"] + bc["e_fin_alt_kwh_e_anno"])
    assert bc["gas_base_kwh_anno"] == pytest.approx(
        bc["q_ess_kwh_th_anno"] / bc["eta_cald"])
    assert bc["gas_alt_kwh_anno"] == pytest.approx(
        bc["q_ess_kwh_th_anno"] * (1.0 - bc["f_rec"])
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
    ct, es, ef, fs = 800, 600, 150, 0.80
    ff, qe, fr, etac = 0.70, 900, 0.40, 0.90
    pel, pg = 220, 90
    omb, oma, cx = 20000, 28000, 300000
    wacc, vita = 5.0, 12
    e_stampa_b = ct * es
    e_fin_b = ct * ef
    e_stampa_a = e_stampa_b * fs
    e_fin_a = e_fin_b * ff
    eb = e_stampa_b + e_fin_b
    ea = e_stampa_a + e_fin_a
    q_ess = ct * qe
    gasb = q_ess / etac
    gasa = q_ess * (1 - fr) / etac
    cb = eb / 1000.0 * pel + gasb / 1000.0 * pg + omb
    ca = ea / 1000.0 * pel + gasa / 1000.0 * pg + oma
    risp = cb - ca
    co2b = (eb * 0.35 + gasb * 0.20) / 1000.0
    co2a = (ea * 0.35 + gasa * 0.20) / 1000.0
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    bc = mh819_demo_calcoli()
    assert bc["e_stampa_base_kwh_e_anno"] == pytest.approx(e_stampa_b)
    assert bc["e_fin_base_kwh_e_anno"] == pytest.approx(e_fin_b)
    assert bc["e_stampa_alt_kwh_e_anno"] == pytest.approx(e_stampa_a)
    assert bc["e_fin_alt_kwh_e_anno"] == pytest.approx(e_fin_a)
    assert bc["e_base_kwh_e_anno"] == pytest.approx(eb)
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(ea)
    assert bc["q_ess_kwh_th_anno"] == pytest.approx(q_ess)
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
    bc = mh819_demo_calcoli()
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] > 0.0
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["tir"] is not None and bc["tir"] > bc["wacc_pct"]
    assert bc["payback"] == 7


# ---------------------------------------------------------------- varianti
def test_variante_senza_recupero_non_convinte():
    # Recupero zero: il gas alternativo resta
    # 800.000 kWh/anno, il risparmio scende
    # a 21.040 EUR/anno e il caso diventa
    # NON_CONVIENTE.
    bc = _variante(f_rec=0)
    assert bc["gas_alt_kwh_anno"] == pytest.approx(800000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(202960.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(21040.0)
    assert bc["van"] == pytest.approx(-113517.18556911708)
    assert bc["tir"] == pytest.approx(-2.558275229025585)
    assert bc["payback"] is None
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_senza_presse_non_convinte():
    # Fattore presse 1 = niente risparmio dalle
    # presse efficienti: il caso diventa
    # NON_CONVIENTE.
    bc = _variante(f_stampa=1)
    assert bc["e_stampa_alt_kwh_e_anno"] == pytest.approx(480000.0)
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(564000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(195280.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(28720.0)
    assert bc["van"] == pytest.approx(-45447.41300119026)
    assert bc["tir"] == pytest.approx(2.2014452343836957)
    assert bc["payback"] == 11
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(0.25)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_senza_finitura_convinte():
    # Fattore finitura 1 = niente risparmio
    # dalla finitura servo: il caso resta
    # CONVIENTE (la finitura vale 7.920
    # EUR/anno, meno delle altre leve).
    bc = _variante(f_fin=1)
    assert bc["e_fin_alt_kwh_e_anno"] == pytest.approx(120000.0)
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(504000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(182080.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(41920.0)
    assert bc["van"] == pytest.approx(71547.508599934)
    assert bc["tir"] == pytest.approx(9.011750240924977)
    assert bc["payback"] == 8
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_400000_convinte_e_500000_non_convinte():
    bc = _variante(capex=400000)
    assert bc["risparmio_eur_anno"] == pytest.approx(49840.0)
    assert bc["van"] == pytest.approx(41744.46156060853)
    assert bc["tir"] == pytest.approx(6.805484852487946)
    assert bc["payback"] == 9
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(capex=500000)
    assert bc2["van"] == pytest.approx(-58255.53843939147)
    assert bc2["tir"] == pytest.approx(2.8693198101668114)
    assert bc2["payback"] == 11
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_om_alt_90000_non_calcolabile():
    # O&M alt 90.000: risparmio negativo negli
    # helper (calcolabile, non solleva), verdetto
    # NON_CALCOLABILE; stessa guard della UI.
    bc = _variante(om_alt=90000)
    assert bc["valid"] is True
    assert bc["c_alt_eur_anno"] == pytest.approx(236160.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-12160.0)
    assert bc["van"] == pytest.approx(-407777.1398992175)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"]
    assert bc["payback"] is None
    assert bc["tir"] is None
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(128.0)


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(298080.0)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(84851.26887057099)
    assert bc2["payback"] == 7
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_prezzo_el_alto_aumenta_risparmio_convinte():
    # Elettricita' a 350 EUR/MWh: il risparmio
    # SALE perche' l'alternativa consuma meno
    # elettricita' della base; il caso resta
    # CONVIENTE e il breakeven resta n/d.
    bc = _variante(p_el=350)
    assert bc["c_base_eur_anno"] == pytest.approx(302000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(235000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(67000.0)
    assert bc["van"] == pytest.approx(293837.85964207014)
    assert bc["tir"] == pytest.approx(19.770223409373607)
    assert bc["payback"] == 5
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_recupero_totale_convinte():
    # Recupero 100 %: gas alternativo zero, il
    # risparmio sale a 93.040 EUR/anno.
    bc = _variante(f_rec=1)
    assert bc["gas_alt_kwh_anno"] == 0.0
    assert bc["c_alt_eur_anno"] == pytest.approx(130960.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(93040.0)
    assert bc["van"] == pytest.approx(524636.932255197)
    assert bc["tir"] == pytest.approx(29.63671976445341)
    assert bc["payback"] == 4
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_calore_zero_breakeven_none():
    # Calore specifico zero: gas base zero,
    # breakeven None, risparmio solo elettrico
    # (21.040 EUR/anno) e VAN negativa oltre la
    # tolleranza, quindi NON_CONVIENTE.
    bc = _variante(q_ess_kwh_th_t=0)
    assert bc["q_ess_kwh_th_anno"] == 0.0
    assert bc["gas_base_kwh_anno"] == 0.0
    assert bc["gas_alt_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(21040.0)
    assert bc["van"] == pytest.approx(-113517.18556911708)
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_monotonia_prezzo_gas_crescente():
    base = mh819_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas=91)["risparmio_eur_anno"]
    basso = _variante(p_gas=89)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(320.0, abs=1e-6)
    assert base - basso == pytest.approx(320.0, abs=1e-6)


def test_monotonia_f_rec_crescente_risparmio_cresce():
    assert _variante(f_rec=1.0)["risparmio_eur_anno"] > \
        mh819_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(f_rec=0.0)["risparmio_eur_anno"] < \
        mh819_demo_calcoli()["risparmio_eur_anno"]


def test_demo_deterministica_due_chiamate():
    a = mh819_demo_calcoli()
    b = mh819_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh819_demo().keys()) == {
        "carta_t", "e_stampa_kwh_e_t", "e_fin_kwh_e_t",
        "f_stampa", "f_fin", "q_ess_kwh_th_t", "f_rec",
        "eta_cald", "p_el", "p_gas", "om_base", "om_alt",
        "capex", "wacc_pct", "vita_anni",
        "tolleranza_pct"}


# ---------------------------------------------------------------- degenere
def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"carta_t": 0},
               {"carta_t": -10},
               {"e_stampa_kwh_e_t": -0.1},
               {"e_fin_kwh_e_t": -0.1},
               {"f_stampa": -0.1}, {"f_stampa": 1.01},
               {"f_fin": -0.1}, {"f_fin": 1.01},
               {"q_ess_kwh_th_t": -0.1},
               {"f_rec": -0.1}, {"f_rec": 1.01},
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
        assert mh819_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"carta_t": "800"},
               {"carta_t": float("nan")},
               {"p_gas": float("inf")},
               {"capex": True},
               {"f_rec": "0.40"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh819_valida(**d)["valido"] is False


def test_zeri_ammessi_non_sollevano_e_nessuna_divergenza():
    # Zeri ammessi in entrambi (helper e UI):
    # specifici elettrici, fattori 0 e 1,
    # calore specifico, O&M, WACC, tolleranza.
    # Qui si verifica che non sollevano e
    # restano calcolabili.
    for kw in ({"e_stampa_kwh_e_t": 0},
               {"e_fin_kwh_e_t": 0},
               {"f_stampa": 0},
               {"f_stampa": 1},
               {"f_fin": 0},
               {"f_fin": 1},
               {"q_ess_kwh_th_t": 0},
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
    bc = _variante(om_alt=90000)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] <= 0.0
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"]


def test_pareggio_esatto_tolleranza_float():
    # A pareggio esatto (prezzo gas = breakeven
    # della variante senza presse) il risparmio
    # e' zero (circa 0.0, quindi guard
    # NON_CALCOLABILE): in nessun caso CONVIENTE.
    be = _variante(f_stampa=1)["breakeven_gas_eur_mwh"]
    bc = _variante(f_stampa=1, p_gas=be)
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["verdetto"] != "CONVIENTE"
    bc2 = _variante(f_stampa=1, p_gas=be + 1)
    assert bc2["risparmio_eur_anno"] == pytest.approx(320.0, abs=1e-6)
    # Risparmio positivo ma piccolo: VAN negativa oltre
    # la tolleranza, quindi NON_CONVIENTE (non CONVIENTE).
    assert bc2["verdetto"] == "NON_CONVIENTE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh819_demo_calcoli()
    testo = mh819_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_gas_eur_mwh" in testo
    assert "co2_evitata_t_anno" in testo
    assert "q_ess_kwh_th_anno" in testo
    assert "e_fin_alt_kwh_e_anno" in testo
    assert "e_stampa_alt_kwh_e_anno" in testo
    assert "gas_alt_kwh_anno" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh819_demo_calcoli()
    testo = mh819_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"e_fin_base_kwh_e_anno;{bc['e_fin_base_kwh_e_anno']}" in testo
    assert f"gas_base_kwh_anno;{bc['gas_base_kwh_anno']}" in testo
    assert f"q_ess_kwh_th_anno;{bc['q_ess_kwh_th_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh819_demo_calcoli()
    testo = mh819_csv(bc, _demo_kwargs())
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
    return ["mh" + "81" + "8", "st" + "81" + "8",
            "tab" + "81" + "8", "w" + "81" + "9"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w820_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w820_ui.py"))
    ast.parse(src)
    assert src.startswith("# W820")
    assert "with tab819:" in src


def test_ui_apre_scheda_attesa_una_volta():
    """Il frammento UI apre la scheda attesa, una sola volta."""
    src = _leggi("w820_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert m.group(1) == "819"
    assert src.count("with tab819:") == 1
    assert src.count("    with tab819:") == 1


def test_ui_titolo_atteso():
    src = _leggi("w820_ui.py")
    titolo = ("Tipografia: presse efficienti + "
              "finitura servo + recupero calore "
              "essiccazione battono presse "
              "tradizionali + finitura tradizionale "
              "+ essiccazione a gas?")
    assert src.count(titolo) == 2


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w820_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_helpers_senza_costanti_di_modulo():
    src = _leggi("w820_helpers.py")
    albero = ast.parse(src)
    for nodo in albero.body:
        assert not isinstance(nodo, ast.Assign), \
            "costante di modulo vietata: i fattori devono essere letterali dentro le funzioni"


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w820_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st819_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) == 26
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w820_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 4
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_ui_guard_degenere_identica_helper():
    """La guard UI della scheda dichiara NON_CALCOLABILE
    per gli stessi casi degeneri degli helper:
    carta <= 0, rendimento caldaia <= 0 o sopra 1,
    prezzi <= 0, CAPEX <= 0, vita <= 0 (nessuna
    divergenza helper-vs-UI)."""
    src = _leggi("w820_ui.py")
    assert "float(_ct819) <= 0.0" in src
    assert "float(_etac819) <= 0.0" in src
    assert "float(_etac819) > 1.0" in src
    assert "float(_pel819) <= 0.0" in src
    assert "float(_pg819) <= 0.0" in src
    assert "float(_cx819) <= 0.0" in src
    assert "int(_vita819) <= 0" in src
    assert "Verdetto: NON_CALCOLABILE" in src


def test_ui_chiamata_calcola_keyword_uguali_firma():
    """La chiamata UI a calcola usa come keyword
    esattamente i parametri della firma helper."""
    src = textwrap.dedent(_leggi("w820_ui.py"))
    albero = ast.parse(src)
    chiamate = []
    for nodo in ast.walk(albero):
        if isinstance(nodo, ast.Call):
            func = nodo.func
            if isinstance(func, ast.Name) and func.id == "mh819_calcola":
                chiamate.append({kw.arg for kw in nodo.keywords})
    assert len(chiamate) == 1
    attesi = set(inspect.signature(mh819_calcola).parameters.keys())
    assert chiamate[0] == attesi


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w820_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def819[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w820_ui.py")
        usate = set(re.findall(r'_def819\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 16
        assert usate <= set(mh819_demo().keys())
