"""Test nuova scheda "Impianto di
imbottigliamento: riempitrici efficienti
+ soffiaggio efficiente + recupero calore
lavaggio battono riempitrici tradizionali
+ soffiaggio tradizionale + lavaggio a gas?"
(titolo completo nel frammento UI).

Business case deterministico di un impianto
di imbottigliamento guidato dai LITRI
IMBOTTIGLIATI in un anno: E_riemp_base =
litri x e_riemp; E_soff_base = litri x
e_soff; E_riemp_alt = E_riemp_base x
f_riemp (le riempitrici efficienti riducono
solo il riempimento); E_soff_alt =
E_soff_base x f_soff (il soffiaggio
efficiente riduce solo il soffiaggio);
E_base = E_riemp_base + E_soff_base;
E_alt = E_riemp_alt + E_soff_alt; Q_lav =
litri x q_lav; gas_base = Q_lav / eta_cald;
gas_alt = Q_lav x (1 - f_rec) / eta_cald
(il recupero calore copre solo la quota
f_rec del calore di lavaggio); C_base =
E_base / 1000 x p_el + gas_base / 1000 x
p_gas + OM_base; C_alt = E_alt / 1000 x
p_el + gas_alt / 1000 x p_gas + OM_alt;
risparmio = C_base - C_alt; CO2 evitata =
(E_base x 0,35 + gas_base x 0,20 - E_alt x
0,35 - gas_alt x 0,20) / 1000 (fattori
letterali, recupero a zero); flussi
[-CAPEX, risparmio x vita]; VAN, TIR,
payback (primo anno con cumulato >= 0);
breakeven gas = (E_alt / 1000 x p_el
+ OM_alt - E_base / 1000 x p_el - OM_base)
x 1000 / (gas_base - gas_alt) EUR/MWh, None
se gas_base <= gas_alt o numeratore < 0,
SOGLIA MINIMA quando esiste. Nel demo il
breakeven e' None (numeratore -47.200,00
EUR, denominatore 333.333,33 kWh/anno):
l'alternativa vince gia' a prezzo gas zero.
Verdetto: NON_CALCOLABILE se input degenere
(litri <= 0, specifici negativi, fattori
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
helper dove previsto (litri, rendimento
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
tipografia (tonnellate di carta stampata,
presse: qui niente carta, niente stampa,
niente finitura, niente essiccazione),
dalla falegnameria (m3 di legno, lavorazioni
del legno: qui niente legno, niente
segagione, niente piallatura, niente
levigatura), dalla cartiera (produzione di
carta da pasta di legno: qui niente pasta
di legno, niente spappolamento, niente carta
da produrre), dal frantoio (tonnellate di
olive, acqua calda di processo: qui niente
olive, niente malaxazione), dal birrificio
(ettolitri di birra, bollitura del mosto:
qui niente mosto, niente bollitura, niente
birra da produrre): qui driver LITRI
IMBOTTIGLIATI + RIEMPITRICI EFFICIENTI +
SOFFIAGGIO EFFICIENTE + RECUPERO CALORE.

Demo (impianto): 10.000.000 di litri
imbottigliati, riempimento specifico
0,030 (300.000 kWh_e/anno), soffiaggio
specifico 0,080 (800.000 kWh_e/anno),
elettricita' base 1.100.000 e alternativa
840.000 kWh_e/anno (fattore riempitrici
0,80: riempimento alternativo 240.000;
fattore soffiaggio 0,75: soffiaggio
alternativo 600.000 kWh_e/anno), calore
specifico 0,060 (600.000 kWh_th/anno),
quota recupero 0,50 (gas base 666.666,67 e
gas alternativo 333.333,33 kWh/anno),
rendimento caldaia 0,90, prezzi
elettricita' 220 e gas 90 EUR/MWh, O&M base
30.000 e alternativo 40.000 EUR/anno, CAPEX
500.000 EUR, WACC 5 %, vita 12 anni,
tolleranza 10 % del CAPEX. Valori
calcolati eseguendo mh820_demo_calcoli():
E_base 1.100.000, E_alt 840.000, C_base
332.000, C_alt 254.800, risparmio 77.200,
CO2_base 518,3333333333334, CO2_alt
360,6666666666667, CO2_evitata
157,66666666666669, VAN 184243,02633384796,
TIR 11,050768715676949 %, payback 7,
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

from w821_helpers import (
    demo_calcoli,
    mh820_breakeven_gas,
    mh820_c_alt,
    mh820_c_base,
    mh820_calcola,
    mh820_co2_alt,
    mh820_co2_base,
    mh820_co2_evitata,
    mh820_csv,
    mh820_demo,
    mh820_demo_calcoli,
    mh820_e_alt,
    mh820_e_base,
    mh820_e_riemp_alt,
    mh820_e_riemp_base,
    mh820_e_soff_alt,
    mh820_e_soff_base,
    mh820_eta,
    mh820_flussi,
    mh820_frazione,
    mh820_gas_alt,
    mh820_gas_base,
    mh820_int_pos,
    mh820_nneg,
    mh820_num,
    mh820_payback,
    mh820_pos,
    mh820_q_lav,
    mh820_risparmio,
    mh820_tir,
    mh820_valida,
    mh820_van,
    mh820_verdetto,
)

_DEMO = {
    "q_lav_kwh_th_anno": 600000.0,
    "e_riemp_base_kwh_e_anno": 300000.0,
    "e_soff_base_kwh_e_anno": 800000.0,
    "e_riemp_alt_kwh_e_anno": 240000.0,
    "e_soff_alt_kwh_e_anno": 600000.0,
    "e_base_kwh_e_anno": 1100000.0,
    "e_alt_kwh_e_anno": 840000.0,
    "gas_base_kwh_anno": 666666.6666666666,
    "gas_alt_kwh_anno": 333333.3333333333,
    "c_base_eur_anno": 332000.0,
    "c_alt_eur_anno": 254800.0,
    "risparmio_eur_anno": 77200.0,
    "co2_base_t_anno": 518.3333333333334,
    "co2_alt_t_anno": 360.6666666666667,
    "co2_evitata_t_anno": 157.66666666666669,
    "van": 184243.02633384796,
    "tir": 11.050768715676949,
}


def _demo_kwargs():
    return dict(mh820_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh820_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh820_num(3, "x") == 3.0
    assert mh820_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh820_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh820_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh820_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh820_pos(0, "x")
    with pytest.raises(ValueError):
        mh820_pos(-1, "x")
    assert mh820_pos(0.5, "x") == 0.5


def test_frazione_limiti():
    assert mh820_frazione(0, "x") == 0.0
    assert mh820_frazione(1, "x") == 1.0
    assert mh820_frazione(0.80, "x") == 0.80
    with pytest.raises(ValueError):
        mh820_frazione(-0.01, "x")
    with pytest.raises(ValueError):
        mh820_frazione(1.01, "x")


def test_eta_limiti():
    assert mh820_eta(1, "x") == 1.0
    assert mh820_eta(0.90, "x") == 0.90
    with pytest.raises(ValueError):
        mh820_eta(0, "x")
    with pytest.raises(ValueError):
        mh820_eta(-0.1, "x")
    with pytest.raises(ValueError):
        mh820_eta(1.01, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh820_int_pos(5.0, "x") == 5
    assert mh820_int_pos(12.0, "x") == 12
    with pytest.raises(ValueError):
        mh820_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh820_int_pos(0, "x")


# ---------------------------------------------------------------- fisica base
def test_q_lav():
    assert mh820_q_lav(10000000, 0.060) == 600000.0
    assert mh820_q_lav(10000000, 0) == 0.0
    with pytest.raises(ValueError):
        mh820_q_lav(0, 0.060)
    with pytest.raises(ValueError):
        mh820_q_lav(10000000, -0.01)


def test_e_riemp_soff_e_base():
    assert mh820_e_riemp_base(10000000, 0.030) == 300000.0
    assert mh820_e_soff_base(10000000, 0.080) == 800000.0
    assert mh820_e_base(300000.0, 800000.0) == 1100000.0
    with pytest.raises(ValueError):
        mh820_e_base(-1, 800000.0)
    with pytest.raises(ValueError):
        mh820_e_riemp_base(0, 0.030)


def test_e_riemp_alt_e_soff_alt():
    assert mh820_e_riemp_alt(300000.0, 0.80) == 240000.0
    assert mh820_e_riemp_alt(300000.0, 1) == 300000.0
    assert mh820_e_riemp_alt(300000.0, 0) == 0.0
    assert mh820_e_soff_alt(800000.0, 0.75) == 600000.0
    assert mh820_e_soff_alt(800000.0, 1) == 800000.0
    assert mh820_e_soff_alt(800000.0, 0) == 0.0
    with pytest.raises(ValueError):
        mh820_e_riemp_alt(300000.0, 1.01)
    with pytest.raises(ValueError):
        mh820_e_soff_alt(800000.0, 1.01)


def test_e_alt():
    assert mh820_e_alt(240000.0, 600000.0) == 840000.0
    with pytest.raises(ValueError):
        mh820_e_alt(240000.0, -1)


def test_gas_base_alt():
    assert mh820_gas_base(600000.0, 0.90) == pytest.approx(666666.6666666666)
    assert mh820_gas_base(0, 0.90) == 0.0
    assert mh820_gas_alt(600000.0, 0.50, 0.90) == pytest.approx(333333.3333333333)
    assert mh820_gas_alt(600000.0, 0, 0.90) == pytest.approx(666666.6666666666)
    assert mh820_gas_alt(600000.0, 1, 0.90) == 0.0
    with pytest.raises(ValueError):
        mh820_gas_base(600000.0, 0)
    with pytest.raises(ValueError):
        mh820_gas_base(600000.0, 1.01)
    with pytest.raises(ValueError):
        mh820_gas_alt(600000.0, 1.01, 0.90)


def test_c_base_c_alt_scomposizione():
    assert mh820_c_base(1100000.0, 220, 666666.6666666666, 90,
                        30000) == pytest.approx(332000.0)
    assert mh820_c_alt(840000.0, 220, 333333.3333333333, 90,
                       40000) == pytest.approx(254800.0)
    with pytest.raises(ValueError):
        mh820_c_base(1100000.0, 0, 666666.6666666666, 90, 30000)
    with pytest.raises(ValueError):
        mh820_c_alt(840000.0, 220, 333333.3333333333, 0, 40000)
    with pytest.raises(ValueError):
        mh820_c_base(1100000.0, 220, 666666.6666666666, 90, -1)


def test_risparmio_segno():
    assert mh820_risparmio(332000.0, 254800.0) == pytest.approx(77200.0)
    assert mh820_risparmio(254800.0, 254800.0) == pytest.approx(0.0, abs=1e-9)


def test_co2_base_alt_evitata():
    assert mh820_co2_base(1100000.0, 666666.6666666666) == pytest.approx(518.3333333333334)
    assert mh820_co2_alt(840000.0, 333333.3333333333) == pytest.approx(360.6666666666667)
    assert mh820_co2_evitata(1100000.0, 666666.6666666666,
                             840000.0, 333333.3333333333) == pytest.approx(157.66666666666669)
    assert mh820_co2_base(0, 0) == 0.0
    assert mh820_co2_alt(0, 0) == 0.0
    with pytest.raises(ValueError):
        mh820_co2_base(1100000.0, -1)
    with pytest.raises(ValueError):
        mh820_co2_alt(-1, 333333.3333333333)


def test_breakeven_demo_none_numeratore_negativo():
    bc = mh820_demo_calcoli()
    assert bc["breakeven_gas_eur_mwh"] is None
    # Numeratore: 840000/1000*220 + 40000 - 1100000/1000*220 - 30000 = -47200 < 0.
    assert mh820_breakeven_gas(840000.0, 220, 40000, 1100000.0,
                               30000, 666666.6666666666,
                               333333.3333333333) is None
    # Denominatore nullo (gas_base = gas_alt) -> None.
    assert mh820_breakeven_gas(840000.0, 220, 40000, 1100000.0,
                               30000, 0.0, 0.0) is None
    # Variante senza recupero: gas_base = gas_alt -> None.
    assert _variante(f_rec=0)["breakeven_gas_eur_mwh"] is None
    # Variante calore zero -> breakeven None.
    assert _variante(q_lav_kwh_th_litro=0)["breakeven_gas_eur_mwh"] is None
    with pytest.raises(ValueError):
        mh820_breakeven_gas(840000.0, 220, 40000, 1100000.0,
                            30000, -1, 333333.3333333333)


def test_breakeven_variante_senza_leve_valore():
    # Senza alcuna leva elettrica il numeratore
    # diventa positivo e il breakeven esiste:
    # 30,00 EUR/MWh.
    bc = _variante(f_riemp=1, f_soff=1)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(30.0)
    assert mh820_breakeven_gas(1100000.0, 220, 40000, 1100000.0,
                               30000, 666666.6666666666,
                               333333.3333333333) == pytest.approx(30.0)


def test_breakeven_verifica_pareggio_su_variante():
    be = _variante(f_riemp=1, f_soff=1)["breakeven_gas_eur_mwh"]
    bc = _variante(f_riemp=1, f_soff=1, p_gas=be)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_breakeven_soglia_minima_su_variante():
    be = _variante(f_riemp=1, f_soff=1)["breakeven_gas_eur_mwh"]
    bc_alto = _variante(f_riemp=1, f_soff=1, p_gas=be + 1)
    bc_basso = _variante(f_riemp=1, f_soff=1, p_gas=10.0)
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
    fl = mh820_flussi(500000, 77200.0, 12)
    assert len(fl) == 13
    assert fl[0] == -500000
    assert all(f == pytest.approx(77200.0) for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh820_demo_calcoli()
    assert bc["van"] == pytest.approx(184243.02633384796)
    assert mh820_van([-500000] + [77200.0] * 12,
                     0) == pytest.approx(426400.0)
    assert mh820_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh820_demo_calcoli()
    assert bc["tir"] == pytest.approx(11.050768715676949)
    assert mh820_tir([-500000] + [77200.0] * 12) == \
        pytest.approx(0.11050768715676949)
    tir = mh820_tir([-500000] + [77200.0] * 12)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-500000] + [77200.0] * 12))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh820_payback([-500000] + [77200.0] * 12) == 7
    assert mh820_payback([-500000] + [-1000.0] * 12) is None
    assert mh820_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh820_verdetto(77200.0, 184243.02633384796, 500000,
                          10.0) == "CONVIENTE"
    assert mh820_verdetto(77200.0, -1500.0, 500000,
                          10.0) == "MARGINALE"
    assert mh820_verdetto(77200.0, -50000.0, 500000, 10.0) == "MARGINALE"
    assert mh820_verdetto(77200.0, -50000.01, 500000, 10.0) == "NON_CONVIENTE"
    assert mh820_verdetto(77200.0, 0.0, 500000, 10.0) == "MARGINALE"
    assert mh820_verdetto(0.0, 184243.03, 500000,
                          10.0) == "NON_CALCOLABILE"
    assert mh820_verdetto(-12800.0, -613449.62, 500000,
                          10.0) == "NON_CALCOLABILE"
    assert mh820_verdetto(None, 184243.03, 500000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh820_verdetto(float("nan"), 184243.03, 500000, 10.0)
    with pytest.raises(ValueError):
        mh820_verdetto(77200.0, 184243.03, 0, 10.0)
    with pytest.raises(ValueError):
        mh820_verdetto(77200.0, 184243.03, 500000, -1)


def test_valida_demo_ok():
    v = mh820_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("litri", "10000000"),
                       ("litri", float("nan")),
                       ("litri", float("inf")),
                       ("litri", True),
                       ("p_gas", None),
                       ("f_rec", "0.50")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh820_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("litri", 0),
                          ("litri", -10),
                          ("e_riemp_kwh_e_litro", -0.01),
                          ("e_soff_kwh_e_litro", -0.01),
                          ("f_riemp", -0.1),
                          ("f_riemp", 1.01),
                          ("f_soff", -0.1),
                          ("f_soff", 1.01),
                          ("q_lav_kwh_th_litro", -0.01),
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
        assert mh820_valida(**d)["valido"] is False


def test_valida_accetta_limiti_e_nessun_tetto_wacc_tolleranza():
    d = _demo_kwargs()
    d.update({"e_riemp_kwh_e_litro": 0,
              "e_soff_kwh_e_litro": 0,
              "f_riemp": 0,
              "f_soff": 0,
              "q_lav_kwh_th_litro": 0,
              "f_rec": 0,
              "om_base": 0, "om_alt": 0,
              "wacc_pct": 0,
              "tolleranza_pct": 0})
    assert mh820_valida(**d)["valido"] is True
    d["f_riemp"] = 1
    d["f_soff"] = 1
    d["f_rec"] = 1
    d["eta_cald"] = 1
    # Il brief non impone tetti superiori a WACC
    # e tolleranza: gli helper li ammettono.
    d["wacc_pct"] = 60
    d["tolleranza_pct"] = 200
    assert mh820_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh820_demo()
    assert d["litri"] == 10000000
    assert d["e_riemp_kwh_e_litro"] == 0.030
    assert d["e_soff_kwh_e_litro"] == 0.080
    assert d["f_riemp"] == 0.80
    assert d["f_soff"] == 0.75
    assert d["q_lav_kwh_th_litro"] == 0.060
    assert d["f_rec"] == 0.50
    assert d["eta_cald"] == 0.90
    assert d["p_el"] == 220
    assert d["p_gas"] == 90
    assert d["om_base"] == 30000
    assert d["om_alt"] == 40000
    assert d["capex"] == 500000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 12
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    bc = mh820_demo_calcoli()
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
    bc = mh820_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(332000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(254800.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(77200.0)
    assert bc["co2_base_t_anno"] == pytest.approx(518.3333333333334)
    assert bc["co2_alt_t_anno"] == pytest.approx(360.6666666666667)
    assert bc["co2_evitata_t_anno"] == pytest.approx(157.66666666666669)
    assert bc["q_lav_kwh_th_anno"] == pytest.approx(600000.0)
    assert bc["e_riemp_base_kwh_e_anno"] == pytest.approx(300000.0)
    assert bc["e_soff_base_kwh_e_anno"] == pytest.approx(800000.0)
    assert bc["e_riemp_alt_kwh_e_anno"] == pytest.approx(240000.0)
    assert bc["e_soff_alt_kwh_e_anno"] == pytest.approx(600000.0)
    assert bc["e_base_kwh_e_anno"] == pytest.approx(1100000.0)
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(840000.0)
    assert bc["gas_base_kwh_anno"] == pytest.approx(666666.6666666666)
    assert bc["gas_alt_kwh_anno"] == pytest.approx(333333.3333333333)


def test_demo_flussi_e_cumulato():
    bc = mh820_demo_calcoli()
    assert bc["flussi"][0] == -500000
    assert len(bc["flussi"]) == 13
    assert all(f == pytest.approx(77200.0) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -500000
    assert righe.iloc[6]["Cumulato (EUR)"] == pytest.approx(-36800.0)
    assert righe.iloc[7]["Cumulato (EUR)"] == pytest.approx(40400.0)
    assert righe.iloc[12]["Cumulato (EUR)"] == pytest.approx(426400.0)


def test_demo_tabella_righe():
    bc = mh820_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Riempimento baseline (kWh_e/anno)"] == pytest.approx(300000.0)
    assert mappa["Riempimento alternativo (kWh_e/anno)"] == pytest.approx(240000.0)
    assert mappa["Soffiaggio baseline (kWh_e/anno)"] == pytest.approx(800000.0)
    assert mappa["Soffiaggio alternativo (kWh_e/anno)"] == pytest.approx(600000.0)
    assert mappa["Elettricita' base (kWh_e/anno)"] == pytest.approx(1100000.0)
    assert mappa["Elettricita' alternativa (kWh_e/anno)"] == pytest.approx(840000.0)
    assert mappa["Calore lavaggio (kWh_th/anno)"] == pytest.approx(600000.0)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(666666.6666666666)
    assert mappa["Gas alternativo (kWh/anno)"] == pytest.approx(333333.3333333333)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(332000.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(254800.0)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(77200.0)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(157.66666666666669)
    assert mappa["Payback (anni)"] == 7
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] is None


def test_demo_coerenza_interna():
    bc = mh820_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["q_lav_kwh_th_anno"] == pytest.approx(
        bc["litri"] * bc["q_lav_kwh_th_litro"])
    assert bc["e_riemp_base_kwh_e_anno"] == pytest.approx(
        bc["litri"] * bc["e_riemp_kwh_e_litro"])
    assert bc["e_soff_base_kwh_e_anno"] == pytest.approx(
        bc["litri"] * bc["e_soff_kwh_e_litro"])
    assert bc["e_riemp_alt_kwh_e_anno"] == pytest.approx(
        bc["e_riemp_base_kwh_e_anno"] * bc["f_riemp"])
    assert bc["e_soff_alt_kwh_e_anno"] == pytest.approx(
        bc["e_soff_base_kwh_e_anno"] * bc["f_soff"])
    assert bc["e_base_kwh_e_anno"] == pytest.approx(
        bc["e_riemp_base_kwh_e_anno"] + bc["e_soff_base_kwh_e_anno"])
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(
        bc["e_riemp_alt_kwh_e_anno"] + bc["e_soff_alt_kwh_e_anno"])
    assert bc["gas_base_kwh_anno"] == pytest.approx(
        bc["q_lav_kwh_th_anno"] / bc["eta_cald"])
    assert bc["gas_alt_kwh_anno"] == pytest.approx(
        bc["q_lav_kwh_th_anno"] * (1.0 - bc["f_rec"])
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
    lt, er, es, fr = 10000000, 0.030, 0.080, 0.80
    fs, ql, fre, etac = 0.75, 0.060, 0.50, 0.90
    pel, pg = 220, 90
    omb, oma, cx = 30000, 40000, 500000
    wacc, vita = 5.0, 12
    e_riemp_b = lt * er
    e_soff_b = lt * es
    e_riemp_a = e_riemp_b * fr
    e_soff_a = e_soff_b * fs
    eb = e_riemp_b + e_soff_b
    ea = e_riemp_a + e_soff_a
    q_lav = lt * ql
    gasb = q_lav / etac
    gasa = q_lav * (1 - fre) / etac
    cb = eb / 1000.0 * pel + gasb / 1000.0 * pg + omb
    ca = ea / 1000.0 * pel + gasa / 1000.0 * pg + oma
    risp = cb - ca
    co2b = (eb * 0.35 + gasb * 0.20) / 1000.0
    co2a = (ea * 0.35 + gasa * 0.20) / 1000.0
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    bc = mh820_demo_calcoli()
    assert bc["e_riemp_base_kwh_e_anno"] == pytest.approx(e_riemp_b)
    assert bc["e_soff_base_kwh_e_anno"] == pytest.approx(e_soff_b)
    assert bc["e_riemp_alt_kwh_e_anno"] == pytest.approx(e_riemp_a)
    assert bc["e_soff_alt_kwh_e_anno"] == pytest.approx(e_soff_a)
    assert bc["e_base_kwh_e_anno"] == pytest.approx(eb)
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(ea)
    assert bc["q_lav_kwh_th_anno"] == pytest.approx(q_lav)
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
    bc = mh820_demo_calcoli()
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] > 0.0
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["tir"] is not None and bc["tir"] > bc["wacc_pct"]
    assert bc["payback"] == 7


# ---------------------------------------------------------------- varianti
def test_variante_senza_recupero_non_convinte():
    # Recupero zero: il gas alternativo resta
    # 666.666,67 kWh/anno, il risparmio scende
    # a 47.200 EUR/anno e il caso diventa
    # NON_CONVIENTE.
    bc = _variante(f_rec=0)
    assert bc["gas_alt_kwh_anno"] == pytest.approx(666666.6666666666)
    assert bc["c_alt_eur_anno"] == pytest.approx(284800.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(47200.0)
    assert bc["van"] == pytest.approx(-81654.52275961635)
    assert bc["tir"] == pytest.approx(1.9725054314109771)
    assert bc["payback"] == 11
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_senza_riempitrici_convinte():
    # Fattore riempitrici 1 = niente risparmio
    # dalle riempitrici efficienti: il caso resta
    # CONVIENTE (le riempitrici valgono 13.200
    # EUR/anno, meno delle altre leve).
    bc = _variante(f_riemp=1)
    assert bc["e_riemp_alt_kwh_e_anno"] == pytest.approx(300000.0)
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(900000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(268000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(64000.0)
    assert bc["van"] == pytest.approx(67248.10473272367)
    assert bc["tir"] == pytest.approx(7.311463506480716)
    assert bc["payback"] == 8
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_senza_soffiaggio_non_convinte():
    # Fattore soffiaggio 1 = niente risparmio
    # dal soffiaggio efficiente: il caso diventa
    # NON_CONVIENTE.
    bc = _variante(f_soff=1)
    assert bc["e_soff_alt_kwh_e_anno"] == pytest.approx(800000.0)
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(1040000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(298800.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(33200.0)
    assert bc["van"] == pytest.approx(-205740.04566989953)
    assert bc["tir"] == pytest.approx(-3.332674713563677)
    assert bc["payback"] is None
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_capex_600000_convinte_e_800000_non_convinte():
    bc = _variante(capex=600000)
    assert bc["risparmio_eur_anno"] == pytest.approx(77200.0)
    assert bc["van"] == pytest.approx(84243.02633384783)
    assert bc["tir"] == pytest.approx(7.4099347825138535)
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(capex=800000)
    assert bc2["van"] == pytest.approx(-115756.97366615206)
    assert bc2["tir"] == pytest.approx(2.3323132810409644)
    assert bc2["payback"] == 11
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_om_alt_130000_non_calcolabile():
    # O&M alt 130.000: risparmio negativo negli
    # helper (calcolabile, non solleva), verdetto
    # NON_CALCOLABILE; stessa guard della UI.
    bc = _variante(om_alt=130000)
    assert bc["valid"] is True
    assert bc["c_alt_eur_anno"] == pytest.approx(344800.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-12800.0)
    assert bc["van"] == pytest.approx(-613449.6209465446)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"]
    assert bc["payback"] is None
    assert bc["tir"] is None
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(128.4)


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(426400.0)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(96117.93653306743)
    assert bc2["payback"] == 7
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_prezzo_el_alto_aumenta_risparmio_convinte():
    # Elettricita' a 350 EUR/MWh: il risparmio
    # SALE perche' l'alternativa consuma meno
    # elettricita' della base; il caso resta
    # CONVIENTE e il breakeven resta n/d.
    bc = _variante(p_el=350)
    assert bc["c_base_eur_anno"] == pytest.approx(475000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(364000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(111000.0)
    assert bc["van"] == pytest.approx(483820.93164581765)
    assert bc["tir"] == pytest.approx(19.611261961839944)
    assert bc["payback"] == 5
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_recupero_totale_convinte():
    # Recupero 100 %: gas alternativo zero, il
    # risparmio sale a 107.200 EUR/anno.
    bc = _variante(f_rec=1)
    assert bc["gas_alt_kwh_anno"] == 0.0
    assert bc["c_alt_eur_anno"] == pytest.approx(224800.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(107200.0)
    assert bc["van"] == pytest.approx(450140.5754273122)
    assert bc["tir"] == pytest.approx(18.699427554474536)
    assert bc["payback"] == 5
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_calore_zero_breakeven_none():
    # Calore specifico zero: gas base zero,
    # breakeven None, risparmio solo elettrico
    # (47.200 EUR/anno) e VAN negativa oltre la
    # tolleranza, quindi NON_CONVIENTE.
    bc = _variante(q_lav_kwh_th_litro=0)
    assert bc["q_lav_kwh_th_anno"] == 0.0
    assert bc["gas_base_kwh_anno"] == 0.0
    assert bc["gas_alt_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(47200.0)
    assert bc["van"] == pytest.approx(-81654.52275961635)
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_monotonia_prezzo_gas_crescente():
    base = mh820_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas=91)["risparmio_eur_anno"]
    basso = _variante(p_gas=89)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(333.3333333333333, abs=1e-6)
    assert base - basso == pytest.approx(333.3333333333333, abs=1e-6)


def test_monotonia_f_rec_crescente_risparmio_cresce():
    assert _variante(f_rec=1.0)["risparmio_eur_anno"] > \
        mh820_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(f_rec=0.0)["risparmio_eur_anno"] < \
        mh820_demo_calcoli()["risparmio_eur_anno"]


def test_demo_deterministica_due_chiamate():
    a = mh820_demo_calcoli()
    b = mh820_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh820_demo().keys()) == {
        "litri", "e_riemp_kwh_e_litro", "e_soff_kwh_e_litro",
        "f_riemp", "f_soff", "q_lav_kwh_th_litro", "f_rec",
        "eta_cald", "p_el", "p_gas", "om_base", "om_alt",
        "capex", "wacc_pct", "vita_anni",
        "tolleranza_pct"}


# ---------------------------------------------------------------- degenere
def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"litri": 0},
               {"litri": -10},
               {"e_riemp_kwh_e_litro": -0.01},
               {"e_soff_kwh_e_litro": -0.01},
               {"f_riemp": -0.1}, {"f_riemp": 1.01},
               {"f_soff": -0.1}, {"f_soff": 1.01},
               {"q_lav_kwh_th_litro": -0.01},
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
        assert mh820_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"litri": "10000000"},
               {"litri": float("nan")},
               {"p_gas": float("inf")},
               {"capex": True},
               {"f_rec": "0.50"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh820_valida(**d)["valido"] is False


def test_zeri_ammessi_non_sollevano_e_nessuna_divergenza():
    # Zeri ammessi in entrambi (helper e UI):
    # specifici elettrici, fattori 0 e 1,
    # calore specifico, O&M, WACC, tolleranza.
    # Qui si verifica che non sollevano e
    # restano calcolabili.
    for kw in ({"e_riemp_kwh_e_litro": 0},
               {"e_soff_kwh_e_litro": 0},
               {"f_riemp": 0},
               {"f_riemp": 1},
               {"f_soff": 0},
               {"f_soff": 1},
               {"q_lav_kwh_th_litro": 0},
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
    bc = _variante(om_alt=130000)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] <= 0.0
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"]


def test_pareggio_esatto_tolleranza_float():
    # A pareggio esatto (prezzo gas = breakeven
    # della variante senza leve elettriche) il
    # risparmio e' zero (circa 0.0, quindi guard
    # NON_CALCOLABILE): in nessun caso CONVIENTE.
    be = _variante(f_riemp=1, f_soff=1)["breakeven_gas_eur_mwh"]
    bc = _variante(f_riemp=1, f_soff=1, p_gas=be)
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["verdetto"] != "CONVIENTE"
    bc2 = _variante(f_riemp=1, f_soff=1, p_gas=be + 1)
    assert bc2["risparmio_eur_anno"] == pytest.approx(333.3333333333333, abs=1e-6)
    # Risparmio positivo ma piccolo: VAN negativa oltre
    # la tolleranza, quindi NON_CONVIENTE (non CONVIENTE).
    assert bc2["verdetto"] == "NON_CONVIENTE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh820_demo_calcoli()
    testo = mh820_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_gas_eur_mwh" in testo
    assert "co2_evitata_t_anno" in testo
    assert "q_lav_kwh_th_anno" in testo
    assert "e_soff_alt_kwh_e_anno" in testo
    assert "e_riemp_alt_kwh_e_anno" in testo
    assert "gas_alt_kwh_anno" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh820_demo_calcoli()
    testo = mh820_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"e_soff_base_kwh_e_anno;{bc['e_soff_base_kwh_e_anno']}" in testo
    assert f"gas_base_kwh_anno;{bc['gas_base_kwh_anno']}" in testo
    assert f"q_lav_kwh_th_anno;{bc['q_lav_kwh_th_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh820_demo_calcoli()
    testo = mh820_csv(bc, _demo_kwargs())
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
    return ["mh" + "81" + "9", "st" + "81" + "9",
            "tab" + "81" + "9", "w" + "82" + "0"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w821_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w821_ui.py"))
    ast.parse(src)
    assert src.startswith("# W821")
    assert "with tab820:" in src


def test_ui_apre_scheda_attesa_una_volta():
    """Il frammento UI apre la scheda attesa, una sola volta."""
    src = _leggi("w821_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert m.group(1) == "820"
    assert src.count("with tab820:") == 1
    assert src.count("    with tab820:") == 1


def test_ui_titolo_atteso():
    src = _leggi("w821_ui.py")
    titolo = ("Impianto di imbottigliamento: "
              "riempitrici efficienti + "
              "soffiaggio efficiente + recupero "
              "calore lavaggio battono riempitrici "
              "tradizionali + soffiaggio tradizionale "
              "+ lavaggio a gas?")
    assert src.count(titolo) == 2


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w821_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_helpers_senza_costanti_di_modulo():
    src = _leggi("w821_helpers.py")
    albero = ast.parse(src)
    for nodo in albero.body:
        assert not isinstance(nodo, ast.Assign), \
            "costante di modulo vietata: i fattori devono essere letterali dentro le funzioni"


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w821_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st820_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) == 26
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w821_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 4
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_ui_guard_degenere_identica_helper():
    """La guard UI della scheda dichiara NON_CALCOLABILE
    per gli stessi casi degeneri degli helper:
    litri <= 0, rendimento caldaia <= 0 o sopra 1,
    prezzi <= 0, CAPEX <= 0, vita <= 0 (nessuna
    divergenza helper-vs-UI)."""
    src = _leggi("w821_ui.py")
    assert "float(_lt820) <= 0.0" in src
    assert "float(_etac820) <= 0.0" in src
    assert "float(_etac820) > 1.0" in src
    assert "float(_pel820) <= 0.0" in src
    assert "float(_pg820) <= 0.0" in src
    assert "float(_cx820) <= 0.0" in src
    assert "int(_vita820) <= 0" in src
    assert "Verdetto: NON_CALCOLABILE" in src


def test_ui_chiamata_calcola_keyword_uguali_firma():
    """La chiamata UI a calcola usa come keyword
    esattamente i parametri della firma helper."""
    src = textwrap.dedent(_leggi("w821_ui.py"))
    albero = ast.parse(src)
    chiamate = []
    for nodo in ast.walk(albero):
        if isinstance(nodo, ast.Call):
            func = nodo.func
            if isinstance(func, ast.Name) and func.id == "mh820_calcola":
                chiamate.append({kw.arg for kw in nodo.keywords})
    assert len(chiamate) == 1
    attesi = set(inspect.signature(mh820_calcola).parameters.keys())
    assert chiamate[0] == attesi


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w821_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def820[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w821_ui.py")
        usate = set(re.findall(r'_def820\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 16
        assert usate <= set(mh820_demo().keys())
