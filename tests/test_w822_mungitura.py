"""Test nuova scheda "Sala mungitura:
pompa del vuoto a velocita' variabile +
refrigerazione latte efficiente + recupero
calore acqua lavaggio battono pompa fissa
+ refrigerazione tradizionale + acqua
calda a gas?" (titolo completo nel
frammento UI).

Business case deterministico di una sala
mungitura guidata dai LITRI DI LATTE
MUNTO in un anno: E_vu_base = litri x
e_vu_base; E_vu_alt = litri x e_vu_alt
(la pompa a velocita' variabile riduce
solo il vuoto); E_ref_base = litri x
e_ref_base; E_ref_alt = litri x e_ref_alt
(la refrigerazione efficiente riduce solo
la refrigerazione); E_base = E_vu_base +
E_ref_base; E_alt = E_vu_alt + E_ref_alt;
gas_base = litri x g_acs_base; gas_alt =
litri x g_acs_alt (il recupero calore
RIDUCE il gas, non lo azzera: gas_alt
resta positivo nel demo); C_base = E_base
x p_el + gas_base x p_gas + OM_base;
C_alt = E_alt x p_el + gas_alt x p_gas
+ OM_alt (prezzi in EUR/kWh, nessuna
conversione / 1000); risparmio =
C_base - C_alt; CO2 evitata = (E_base x
0,25 + gas_base x 0,202 - E_alt x 0,25
- gas_alt x 0,202) / 1000 (fattori
letterali); flussi [-CAPEX, risparmio x
vita]; VAN, TIR, payback (primo anno con
cumulato >= 0); breakeven gas = (E_alt x
p_el + OM_alt - E_base x p_el - OM_base)
/ (gas_base - gas_alt) EUR/kWh, None se
gas_base <= gas_alt o numeratore < 0,
SOGLIA MINIMA quando esiste. Nel demo il
breakeven e' 0,0167 EUR/kWh (numeratore
1.000 EUR, denominatore 60.000 kWh/anno).
Verdetto: NON_CALCOLABILE se input degenere
(litri <= 0, specifici negativi,
prezzi <= 0, O&M negativi, CAPEX <= 0, WACC
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
helper dove previsto (litri, prezzi,
CAPEX, vita). Gli zeri ammessi in entrambi
(specifici elettrici e gas, O&M, WACC,
tolleranza) non creano divergenza: con gas
specifico base uguale a gas specifico
alternativo il breakeven e' None, e il
caso resta calcolabile in entrambi. WACC
sopra 20 % e tolleranza sopra 100 % sono
ammessi negli helper e limitati solo dagli
slider UI (20, 100): nessuna divergenza
nel range raggiungibile, perche' la guard
controlla solo gli stessi limiti degli
helper.
Distinzione esplicita: distinta dal
caseificio (litri di latte, pastorizzazione:
qui niente pastorizzazione, niente latte
pastorizzato), dal mulino (tonnellate di
cereale, macinazione, pneumatico: qui
niente cereali, niente macinazione, niente
pneumatico), dall'imbottigliamento (litri
imbottigliati, riempitrici: qui niente
bottiglie, niente riempimento, niente
riempitrici): qui driver LITRO DI LATTE
MUNTO + POMPA DEL VUOTO A VELOCITA'
VARIABILE + REFRIGERAZIONE EFFICIENTE +
RECUPERO CALORE ACQUA LAVAGGIO.

Demo (sala mungitura): 1.500.000 litri di
latte munto, vuoto specifico base 0,015
(22.500 kWh_e/anno) e alternativo 0,008
(12.000 kWh_e/anno), refrigerazione
specifica base 0,022 (33.000 kWh_e/anno)
e alternativa 0,013 (19.500 kWh_e/anno),
elettricita' base 55.500 e alternativa
31.500 kWh_e/anno, gas specifico acqua
lavaggio base 0,05 (75.000 kWh/anno) e
alternativo 0,01 (15.000 kWh/anno, il
recupero riduce il gas dell'80 %, non lo
azzera), prezzi elettricita' 0,25 e gas
0,10 EUR/kWh, O&M base 12.000 e alternativo
19.000 EUR/anno, CAPEX 45.000 EUR, WACC
5 %, vita 15 anni, tolleranza 10 % del
CAPEX. Valori calcolati eseguendo
mh822_demo_calcoli(): E_base 55.500,
E_alt 31.500, gas_base 75.000, gas_alt
15.000, C_base 33.375, C_alt 28.375,
risparmio 5.000, CO2_base 29,025, CO2_alt
10,905, CO2_evitata 18,12, VAN
6898,290190902959, TIR 7,189314082292121 %,
payback 9, breakeven gas
0,016666666666666666 EUR/kWh, verdetto
CONVIENTE.
"""

import ast
import inspect
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w823_helpers import (
    demo_calcoli,
    mh822_breakeven_gas,
    mh822_c_alt,
    mh822_c_base,
    mh822_calcola,
    mh822_co2_alt,
    mh822_co2_base,
    mh822_co2_evitata,
    mh822_csv,
    mh822_demo,
    mh822_demo_calcoli,
    mh822_e_alt,
    mh822_e_base,
    mh822_e_ref_alt,
    mh822_e_ref_base,
    mh822_e_vu_alt,
    mh822_e_vu_base,
    mh822_flussi,
    mh822_gas_alt,
    mh822_gas_base,
    mh822_int_pos,
    mh822_nneg,
    mh822_num,
    mh822_payback,
    mh822_pos,
    mh822_risparmio,
    mh822_tir,
    mh822_valida,
    mh822_van,
    mh822_verdetto,
)

_DEMO = {
    "e_vu_base_kwh_e_anno": 22500.0,
    "e_vu_alt_kwh_e_anno": 12000.0,
    "e_ref_base_kwh_e_anno": 33000.0,
    "e_ref_alt_kwh_e_anno": 19500.0,
    "e_base_kwh_e_anno": 55500.0,
    "e_alt_kwh_e_anno": 31500.0,
    "gas_base_kwh_anno": 75000.0,
    "gas_alt_kwh_anno": 15000.0,
    "c_base_eur_anno": 33375.0,
    "c_alt_eur_anno": 28375.0,
    "risparmio_eur_anno": 5000.0,
    "co2_base_t_anno": 29.025,
    "co2_alt_t_anno": 10.905,
    "co2_evitata_t_anno": 18.12,
    "van": 6898.290190902959,
    "tir": 7.189314082292121,
}


def _demo_kwargs():
    return dict(mh822_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh822_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh822_num(3, "x") == 3.0
    assert mh822_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh822_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh822_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh822_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh822_pos(0, "x")
    with pytest.raises(ValueError):
        mh822_pos(-1, "x")
    assert mh822_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh822_int_pos(5.0, "x") == 5
    assert mh822_int_pos(15.0, "x") == 15
    with pytest.raises(ValueError):
        mh822_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh822_int_pos(0, "x")


# ---------------------------------------------------------------- fisica base
def test_e_vu_e_ref_e_base():
    assert mh822_e_vu_base(1500000, 0.015) == 22500.0
    assert mh822_e_vu_alt(1500000, 0.008) == 12000.0
    assert mh822_e_ref_base(1500000, 0.022) == 33000.0
    assert mh822_e_ref_alt(1500000, 0.013) == 19500.0
    assert mh822_e_base(22500.0, 33000.0) == 55500.0
    with pytest.raises(ValueError):
        mh822_e_base(-1, 33000.0)
    with pytest.raises(ValueError):
        mh822_e_vu_base(0, 0.015)


def test_e_alt():
    assert mh822_e_alt(12000.0, 19500.0) == 31500.0
    with pytest.raises(ValueError):
        mh822_e_alt(12000.0, -1)
    with pytest.raises(ValueError):
        mh822_e_vu_alt(0, 0.008)


def test_gas_base_alt():
    assert mh822_gas_base(1500000, 0.05) == 75000.0
    assert mh822_gas_alt(1500000, 0.01) == 15000.0
    assert mh822_gas_alt(1500000, 0) == 0.0
    with pytest.raises(ValueError):
        mh822_gas_base(1500000, -0.01)
    with pytest.raises(ValueError):
        mh822_gas_base(0, 0.05)


def test_c_base_c_alt_scomposizione():
    assert mh822_c_base(55500.0, 0.25, 75000.0, 0.10,
                        12000) == pytest.approx(33375.0)
    assert mh822_c_alt(31500.0, 0.25, 15000.0, 0.10,
                       19000) == pytest.approx(28375.0)
    with pytest.raises(ValueError):
        mh822_c_base(55500.0, 0, 75000.0, 0.10, 12000)
    with pytest.raises(ValueError):
        mh822_c_alt(31500.0, 0.25, 15000.0, 0, 19000)
    with pytest.raises(ValueError):
        mh822_c_base(55500.0, 0.25, 75000.0, 0.10, -1)


def test_risparmio_segno():
    assert mh822_risparmio(33375.0, 28375.0) == pytest.approx(5000.0)
    assert mh822_risparmio(28375.0, 28375.0) == pytest.approx(0.0, abs=1e-9)


def test_co2_base_alt_evitata():
    assert mh822_co2_base(55500.0, 75000.0) == pytest.approx(29.025)
    assert mh822_co2_alt(31500.0, 15000.0) == pytest.approx(10.905)
    assert mh822_co2_evitata(55500.0, 75000.0,
                             31500.0, 15000.0) == pytest.approx(18.12)
    assert mh822_co2_base(0, 0) == 0.0
    assert mh822_co2_alt(0, 0) == 0.0
    with pytest.raises(ValueError):
        mh822_co2_base(55500.0, -1)
    with pytest.raises(ValueError):
        mh822_co2_alt(-1, 0.0)


def test_breakeven_demo_valore():
    bc = mh822_demo_calcoli()
    assert bc["breakeven_gas_eur_kwh"] == pytest.approx(0.016666666666666666)
    # Numeratore: 31500*0,25 + 19000 - 55500*0,25 - 12000 = 1000;
    # denominatore: 75000 - 15000 = 60000.
    assert mh822_breakeven_gas(31500.0, 0.25, 19000, 55500.0,
                               12000, 75000.0,
                               15000.0) == pytest.approx(0.016666666666666666)
    # Gas base uguale a gas alternativo -> None.
    assert mh822_breakeven_gas(31500.0, 0.25, 19000, 55500.0,
                               12000, 75000.0, 75000.0) is None
    # Gas base minore di gas alternativo -> None.
    assert mh822_breakeven_gas(31500.0, 0.25, 19000, 55500.0,
                               12000, 10000.0, 15000.0) is None
    # Variante gas alternativo uguale al base -> breakeven None.
    assert _variante(g_acs_alt_kwh_l=0.05)["breakeven_gas_eur_kwh"] is None
    with pytest.raises(ValueError):
        mh822_breakeven_gas(31500.0, 0.25, 19000, 55500.0,
                            12000, -1, 15000.0)


def test_breakeven_numeratore_negativo_none():
    # Con O&M alternativo 0 il numeratore
    # diventa negativo: 31500*0,25 + 0 - 55500*0,25 - 12000 < 0.
    assert mh822_breakeven_gas(31500.0, 0.25, 0, 55500.0,
                               12000, 75000.0,
                               15000.0) is None
    assert _variante(om_alt=0)["breakeven_gas_eur_kwh"] is None


def test_breakeven_verifica_pareggio_su_demo():
    be = mh822_demo_calcoli()["breakeven_gas_eur_kwh"]
    bc = _variante(p_gas=be)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_breakeven_soglia_minima_su_demo():
    be = mh822_demo_calcoli()["breakeven_gas_eur_kwh"]
    bc_alto = _variante(p_gas=0.10)
    bc_basso = _variante(p_gas=0.01)
    assert bc_alto["c_alt_eur_anno"] < bc_alto["c_base_eur_anno"]
    assert bc_basso["c_alt_eur_anno"] > bc_basso["c_base_eur_anno"]
    assert bc_alto["risparmio_eur_anno"] > 0.0
    assert bc_basso["verdetto"] == "NON_CALCOLABILE"
    assert bc_alto["risparmio_eur_anno"] == pytest.approx(5000.0)
    assert bc_basso["risparmio_eur_anno"] == pytest.approx(-400.0)
    assert bc_alto["verdetto"] == "CONVIENTE"
    assert be < 0.10


def test_breakeven_variante_senza_vuoto():
    # Senza vuoto variabile il numeratore
    # sale: 3625 / 60000 = 0,060416...
    bc = _variante(e_vu_alt_kwh_e_l=0.015)
    assert bc["breakeven_gas_eur_kwh"] == pytest.approx(0.06041666666666667)


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh822_flussi(45000, 5000.0, 15)
    assert len(fl) == 16
    assert fl[0] == -45000
    assert all(f == pytest.approx(5000.0) for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh822_demo_calcoli()
    assert bc["van"] == pytest.approx(6898.290190902959)
    assert mh822_van([-45000] + [5000.0] * 15,
                     0) == pytest.approx(30000.0)
    assert mh822_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh822_demo_calcoli()
    assert bc["tir"] == pytest.approx(7.189314082292121)
    assert mh822_tir([-45000] + [5000.0] * 15) == \
        pytest.approx(0.07189314082292121)
    tir = mh822_tir([-45000] + [5000.0] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-45000] + [5000.0] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh822_payback([-45000] + [5000.0] * 15) == 9
    assert mh822_payback([-45000] + [-1000.0] * 15) is None
    assert mh822_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh822_verdetto(5000.0, 6898.290190902959, 45000,
                          10.0) == "CONVIENTE"
    assert mh822_verdetto(5000.0, -1500.0, 45000,
                          10.0) == "MARGINALE"
    assert mh822_verdetto(5000.0, -4500.0, 45000, 10.0) == "MARGINALE"
    assert mh822_verdetto(5000.0, -4500.01, 45000, 10.0) == "NON_CONVIENTE"
    assert mh822_verdetto(5000.0, 0.0, 45000, 10.0) == "MARGINALE"
    assert mh822_verdetto(0.0, 6898.29, 45000,
                          10.0) == "NON_CALCOLABILE"
    assert mh822_verdetto(-1000.0, -55379.66, 45000,
                          10.0) == "NON_CALCOLABILE"
    assert mh822_verdetto(None, 6898.29, 45000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh822_verdetto(float("nan"), 6898.29, 45000, 10.0)
    with pytest.raises(ValueError):
        mh822_verdetto(5000.0, 6898.29, 0, 10.0)
    with pytest.raises(ValueError):
        mh822_verdetto(5000.0, 6898.29, 45000, -1)


def test_valida_demo_ok():
    v = mh822_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("litri", "1500000"),
                       ("litri", float("nan")),
                       ("litri", float("inf")),
                       ("litri", True),
                       ("p_gas", None),
                       ("g_acs_base_kwh_l", "0.05")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh822_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("litri", 0),
                          ("litri", -10),
                          ("e_vu_base_kwh_e_l", -1),
                          ("e_vu_alt_kwh_e_l", -1),
                          ("e_ref_base_kwh_e_l", -1),
                          ("e_ref_alt_kwh_e_l", -1),
                          ("g_acs_base_kwh_l", -1),
                          ("g_acs_alt_kwh_l", -1),
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
        assert mh822_valida(**d)["valido"] is False


def test_valida_accetta_limiti_e_nessun_tetto_wacc_tolleranza():
    d = _demo_kwargs()
    d.update({"e_vu_base_kwh_e_l": 0,
              "e_vu_alt_kwh_e_l": 0,
              "e_ref_base_kwh_e_l": 0,
              "e_ref_alt_kwh_e_l": 0,
              "g_acs_base_kwh_l": 0,
              "g_acs_alt_kwh_l": 0,
              "om_base": 0, "om_alt": 0,
              "wacc_pct": 0,
              "tolleranza_pct": 0})
    assert mh822_valida(**d)["valido"] is True
    # Il brief non impone tetti superiori a WACC
    # e tolleranza: gli helper li ammettono.
    d["wacc_pct"] = 60
    d["tolleranza_pct"] = 200
    assert mh822_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh822_demo()
    assert d["litri"] == 1500000
    assert d["e_vu_base_kwh_e_l"] == 0.015
    assert d["e_vu_alt_kwh_e_l"] == 0.008
    assert d["e_ref_base_kwh_e_l"] == 0.022
    assert d["e_ref_alt_kwh_e_l"] == 0.013
    assert d["g_acs_base_kwh_l"] == 0.05
    assert d["g_acs_alt_kwh_l"] == 0.01
    assert d["p_el"] == 0.25
    assert d["p_gas"] == 0.10
    assert d["om_base"] == 12000
    assert d["om_alt"] == 19000
    assert d["capex"] == 45000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    bc = mh822_demo_calcoli()
    for chiave, atteso in _DEMO.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert got == pytest.approx(atteso, rel=1e-9), chiave
    assert bc["payback"] == 9
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True
    assert bc["breakeven_gas_eur_kwh"] == pytest.approx(0.016666666666666666)
    assert demo_calcoli()["van"] == bc["van"]


def test_demo_calcoli_fisica_economia():
    bc = mh822_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(33375.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(28375.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(5000.0)
    assert bc["co2_base_t_anno"] == pytest.approx(29.025)
    assert bc["co2_alt_t_anno"] == pytest.approx(10.905)
    assert bc["co2_evitata_t_anno"] == pytest.approx(18.12)
    assert bc["gas_base_kwh_anno"] == pytest.approx(75000.0)
    assert bc["gas_alt_kwh_anno"] == pytest.approx(15000.0)
    assert bc["e_vu_base_kwh_e_anno"] == pytest.approx(22500.0)
    assert bc["e_vu_alt_kwh_e_anno"] == pytest.approx(12000.0)
    assert bc["e_ref_base_kwh_e_anno"] == pytest.approx(33000.0)
    assert bc["e_ref_alt_kwh_e_anno"] == pytest.approx(19500.0)
    assert bc["e_base_kwh_e_anno"] == pytest.approx(55500.0)
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(31500.0)


def test_demo_flussi_e_cumulato():
    bc = mh822_demo_calcoli()
    assert bc["flussi"][0] == -45000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(5000.0) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -45000
    assert righe.iloc[8]["Cumulato (EUR)"] == pytest.approx(-5000.0)
    assert righe.iloc[9]["Cumulato (EUR)"] == pytest.approx(0.0)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(30000.0)


def test_demo_tabella_righe():
    bc = mh822_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Vuoto baseline (kWh_e/anno)"] == pytest.approx(22500.0)
    assert mappa["Vuoto alternativo (kWh_e/anno)"] == pytest.approx(12000.0)
    assert mappa["Refrigerazione baseline (kWh_e/anno)"] == pytest.approx(33000.0)
    assert mappa["Refrigerazione alternativa (kWh_e/anno)"] == pytest.approx(19500.0)
    assert mappa["Elettricita' base (kWh_e/anno)"] == pytest.approx(55500.0)
    assert mappa["Elettricita' alternativa (kWh_e/anno)"] == pytest.approx(31500.0)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(75000.0)
    assert mappa["Gas alternativo (kWh/anno)"] == pytest.approx(15000.0)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(33375.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(28375.0)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(5000.0)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(18.12)
    assert mappa["Payback (anni)"] == 9
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/kWh)"] == pytest.approx(0.016666666666666666)


def test_demo_coerenza_interna():
    bc = mh822_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["gas_base_kwh_anno"] == pytest.approx(
        bc["litri"] * bc["g_acs_base_kwh_l"])
    assert bc["gas_alt_kwh_anno"] == pytest.approx(
        bc["litri"] * bc["g_acs_alt_kwh_l"])
    assert bc["e_vu_base_kwh_e_anno"] == pytest.approx(
        bc["litri"] * bc["e_vu_base_kwh_e_l"])
    assert bc["e_vu_alt_kwh_e_anno"] == pytest.approx(
        bc["litri"] * bc["e_vu_alt_kwh_e_l"])
    assert bc["e_ref_base_kwh_e_anno"] == pytest.approx(
        bc["litri"] * bc["e_ref_base_kwh_e_l"])
    assert bc["e_ref_alt_kwh_e_anno"] == pytest.approx(
        bc["litri"] * bc["e_ref_alt_kwh_e_l"])
    assert bc["e_base_kwh_e_anno"] == pytest.approx(
        bc["e_vu_base_kwh_e_anno"] + bc["e_ref_base_kwh_e_anno"])
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(
        bc["e_vu_alt_kwh_e_anno"] + bc["e_ref_alt_kwh_e_anno"])
    assert bc["co2_evitata_t_anno"] == pytest.approx(
        bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])
    assert bc["c_base_eur_anno"] == pytest.approx(
        bc["e_base_kwh_e_anno"] * bc["p_el"]
        + bc["gas_base_kwh_anno"] * bc["p_gas"]
        + bc["om_base"])
    assert bc["c_alt_eur_anno"] == pytest.approx(
        bc["e_alt_kwh_e_anno"] * bc["p_el"]
        + bc["gas_alt_kwh_anno"] * bc["p_gas"]
        + bc["om_alt"])


def test_demo_contro_riconteggio_indipendente():
    lt, evb, eva = 1500000, 0.015, 0.008
    erb, era, gab, gaa = 0.022, 0.013, 0.05, 0.01
    pel, pg = 0.25, 0.10
    omb, oma, cx = 12000, 19000, 45000
    wacc, vita = 5.0, 15
    e_vu_b = lt * evb
    e_vu_a = lt * eva
    e_ref_b = lt * erb
    e_ref_a = lt * era
    eb = e_vu_b + e_ref_b
    ea = e_vu_a + e_ref_a
    gasb = lt * gab
    gasa = lt * gaa
    cb = eb * pel + gasb * pg + omb
    ca = ea * pel + gasa * pg + oma
    risp = cb - ca
    co2b = (eb * 0.25 + gasb * 0.202) / 1000.0
    co2a = (ea * 0.25 + gasa * 0.202) / 1000.0
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    bc = mh822_demo_calcoli()
    assert bc["e_vu_base_kwh_e_anno"] == pytest.approx(e_vu_b)
    assert bc["e_vu_alt_kwh_e_anno"] == pytest.approx(e_vu_a)
    assert bc["e_ref_base_kwh_e_anno"] == pytest.approx(e_ref_b)
    assert bc["e_ref_alt_kwh_e_anno"] == pytest.approx(e_ref_a)
    assert bc["e_base_kwh_e_anno"] == pytest.approx(eb)
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(ea)
    assert bc["gas_base_kwh_anno"] == pytest.approx(gasb)
    assert bc["gas_alt_kwh_anno"] == pytest.approx(gasa)
    assert bc["c_base_eur_anno"] == pytest.approx(cb)
    assert bc["c_alt_eur_anno"] == pytest.approx(ca)
    assert bc["risparmio_eur_anno"] == pytest.approx(risp)
    assert bc["co2_base_t_anno"] == pytest.approx(co2b)
    assert bc["co2_alt_t_anno"] == pytest.approx(co2a)
    assert bc["co2_evitata_t_anno"] == pytest.approx(co2)
    assert bc["van"] == pytest.approx(van)
    assert bc["breakeven_gas_eur_kwh"] == pytest.approx(1000.0 / 60000.0)


def test_demo_verdetto_coerente_con_risparmio_e_van():
    bc = mh822_demo_calcoli()
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] > 0.0
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["tir"] is not None and bc["tir"] > bc["wacc_pct"]
    assert bc["payback"] == 9


# ---------------------------------------------------------------- varianti
def test_variante_senza_vuoto_non_convinte():
    # Vuoto alternativo 0,015 = niente
    # risparmio dalla pompa a velocita'
    # variabile: il caso diventa NON_CONVIENTE.
    bc = _variante(e_vu_alt_kwh_e_l=0.015)
    assert bc["e_vu_alt_kwh_e_anno"] == pytest.approx(22500.0)
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(42000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(31000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(2375.0)
    assert bc["van"] == pytest.approx(-20348.3121593211)
    assert bc["tir"] == pytest.approx(-2.7874930772171105)
    assert bc["payback"] is None
    assert bc["breakeven_gas_eur_kwh"] == pytest.approx(0.06041666666666667)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_senza_refrigerazione_non_convinte():
    # Refrigerazione alternativa 0,022 =
    # niente risparmio dalla refrigerazione
    # efficiente: il caso diventa NON_CONVIENTE.
    bc = _variante(e_ref_alt_kwh_e_l=0.022)
    assert bc["e_ref_alt_kwh_e_anno"] == pytest.approx(33000.0)
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(45000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(31750.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(1625.0)
    assert bc["van"] == pytest.approx(-28133.055687956537)
    assert bc["tir"] == pytest.approx(-6.838724374241965)
    assert bc["payback"] is None
    assert bc["breakeven_gas_eur_kwh"] == pytest.approx(0.07291666666666667)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_senza_recupero_non_calcolabile():
    # Gas alternativo 0,05 = niente recupero
    # calore: il risparmio diventa negativo
    # negli helper (calcolabile, non solleva),
    # verdetto NON_CALCOLABILE; stessa guard
    # della UI. Il breakeven e' None perche'
    # gas base uguale a gas alternativo.
    bc = _variante(g_acs_alt_kwh_l=0.05)
    assert bc["valid"] is True
    assert bc["gas_alt_kwh_anno"] == pytest.approx(75000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(34375.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-1000.0)
    assert bc["van"] == pytest.approx(-55379.65803818059)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"]
    assert bc["payback"] is None
    assert bc["tir"] is None
    assert bc["breakeven_gas_eur_kwh"] is None


def test_variante_capex_60000_non_convinte():
    bc = _variante(capex=60000)
    assert bc["risparmio_eur_anno"] == pytest.approx(5000.0)
    assert bc["van"] == pytest.approx(-8101.7098090970485)
    assert bc["tir"] == pytest.approx(2.9283950062936666)
    assert bc["payback"] == 12
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_om_alt_20000_marginale():
    # O&M alternativo 20.000: risparmio 4.000,
    # VAN negativa entro il 10 % del CAPEX
    # (4.500 EUR), quindi MARGINALE.
    bc = _variante(om_alt=20000)
    assert bc["c_alt_eur_anno"] == pytest.approx(29375.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(4000.0)
    assert bc["van"] == pytest.approx(-3481.3678472776446)
    assert bc["tir"] == pytest.approx(3.8321825634713464)
    assert bc["payback"] == 12
    assert bc["breakeven_gas_eur_kwh"] == pytest.approx(0.03333333333333333)
    assert bc["verdetto"] == "MARGINALE"


def test_variante_om_alt_30000_non_calcolabile():
    # O&M alt 30.000: risparmio negativo negli
    # helper (calcolabile, non solleva), verdetto
    # NON_CALCOLABILE; stessa guard della UI.
    bc = _variante(om_alt=30000)
    assert bc["valid"] is True
    assert bc["c_alt_eur_anno"] == pytest.approx(39375.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-6000.0)
    assert bc["van"] == pytest.approx(-107277.94822908353)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"]
    assert bc["payback"] is None
    assert bc["tir"] is None
    assert bc["breakeven_gas_eur_kwh"] == pytest.approx(0.2)


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(30000.0)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(-6391.32535407594)
    assert bc2["tir"] == pytest.approx(1.9629979784128262)
    assert bc2["payback"] == 9
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_gas_alto_convinte():
    # Prezzo gas 0,20: risparmio 11.000,
    # VAN positiva, payback 5 anni.
    bc = _variante(p_gas=0.20)
    assert bc["risparmio_eur_anno"] == pytest.approx(11000.0)
    assert bc["van"] == pytest.approx(69176.2384199865)
    assert bc["tir"] == pytest.approx(23.401190794198158)
    assert bc["payback"] == 5
    assert bc["verdetto"] == "CONVIENTE"


def test_monotonia_prezzo_gas_crescente():
    base = mh822_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas=0.101)["risparmio_eur_anno"]
    basso = _variante(p_gas=0.099)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(60.0, abs=1e-6)
    assert base - basso == pytest.approx(60.0, abs=1e-6)


def test_monotonia_vuoto_e_recupero():
    # Piu' elettricita' di vuoto alternativo,
    # meno risparmio; piu' gas alternativo
    # (meno recupero), meno risparmio.
    assert _variante(e_vu_alt_kwh_e_l=0.012)["risparmio_eur_anno"] < \
        mh822_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(g_acs_alt_kwh_l=0.02)["risparmio_eur_anno"] < \
        mh822_demo_calcoli()["risparmio_eur_anno"]


def test_demo_deterministica_due_chiamate():
    a = mh822_demo_calcoli()
    b = mh822_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh822_demo().keys()) == {
        "litri", "e_vu_base_kwh_e_l", "e_vu_alt_kwh_e_l",
        "e_ref_base_kwh_e_l", "e_ref_alt_kwh_e_l",
        "g_acs_base_kwh_l", "g_acs_alt_kwh_l",
        "p_el", "p_gas", "om_base", "om_alt",
        "capex", "wacc_pct", "vita_anni",
        "tolleranza_pct"}


# ---------------------------------------------------------------- degenere
def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"litri": 0},
               {"litri": -10},
               {"e_vu_base_kwh_e_l": -1},
               {"e_vu_alt_kwh_e_l": -1},
               {"e_ref_base_kwh_e_l": -1},
               {"e_ref_alt_kwh_e_l": -1},
               {"g_acs_base_kwh_l": -1},
               {"g_acs_alt_kwh_l": -1},
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
        assert mh822_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"litri": "1500000"},
               {"litri": float("nan")},
               {"p_gas": float("inf")},
               {"capex": True},
               {"g_acs_base_kwh_l": "0.05"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh822_valida(**d)["valido"] is False


def test_zeri_ammessi_non_sollevano_e_nessuna_divergenza():
    # Zeri ammessi in entrambi (helper e UI):
    # specifici elettrici e gas, O&M, WACC,
    # tolleranza. Qui si verifica che non
    # sollevano e restano calcolabili.
    for kw in ({"e_vu_base_kwh_e_l": 0},
               {"e_vu_alt_kwh_e_l": 0},
               {"e_ref_base_kwh_e_l": 0},
               {"e_ref_alt_kwh_e_l": 0},
               {"g_acs_base_kwh_l": 0},
               {"g_acs_alt_kwh_e_l": 0} if False else {"g_acs_alt_kwh_l": 0},
               {"om_base": 0},
               {"om_alt": 0},
               {"wacc_pct": 0},
               {"tolleranza_pct": 0}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["verdetto"] in ("CONVIENTE", "MARGINALE",
                                  "NON_CONVIENTE", "NON_CALCOLABILE")


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    bc = _variante(g_acs_alt_kwh_l=0.05)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] <= 0.0
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"]


def test_pareggio_esatto_tolleranza_float():
    # A pareggio esatto (prezzo gas = breakeven
    # del demo) il risparmio e' zero (circa
    # 0.0, quindi guard NON_CALCOLABILE): in
    # nessun caso CONVIENTE.
    be = mh822_demo_calcoli()["breakeven_gas_eur_kwh"]
    bc = _variante(p_gas=be)
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["verdetto"] != "CONVIENTE"
    bc2 = _variante(p_gas=0.10)
    assert bc2["risparmio_eur_anno"] == pytest.approx(5000.0, abs=1e-6)
    assert bc2["verdetto"] == "CONVIENTE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh822_demo_calcoli()
    testo = mh822_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_gas_eur_kwh" in testo
    assert "co2_evitata_t_anno" in testo
    assert "gas_base_kwh_anno" in testo
    assert "e_ref_alt_kwh_e_anno" in testo
    assert "e_vu_alt_kwh_e_anno" in testo
    assert "gas_alt_kwh_anno" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh822_demo_calcoli()
    testo = mh822_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"e_ref_base_kwh_e_anno;{bc['e_ref_base_kwh_e_anno']}" in testo
    assert f"gas_base_kwh_anno;{bc['gas_base_kwh_anno']}" in testo
    assert f"e_vu_base_kwh_e_anno;{bc['e_vu_base_kwh_e_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh822_demo_calcoli()
    testo = mh822_csv(bc, _demo_kwargs())
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
    return ["mh" + "82" + "1", "st" + "82" + "1",
            "tab" + "82" + "1", "w" + "82" + "2"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w823_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w823_ui.py"))
    ast.parse(src)
    assert src.startswith("# W823")
    assert "with tab822:" in src


def test_ui_apre_scheda_attesa_una_volta():
    """Il frammento UI apre la scheda attesa, una sola volta."""
    src = _leggi("w823_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert m.group(1) == "822"
    assert src.count("with tab822:") == 1
    assert src.count("    with tab822:") == 1


def test_ui_titolo_atteso():
    src = _leggi("w823_ui.py")
    titolo = ("🐄 Sala mungitura: "
              "pompa del vuoto a velocita' variabile + "
              "refrigerazione latte efficiente + "
              "recupero calore acqua lavaggio battono "
              "pompa fissa + refrigerazione tradizionale + "
              "acqua calda a gas?")
    assert src.count(titolo) == 2


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w823_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_helpers_senza_costanti_di_modulo():
    src = _leggi("w823_helpers.py")
    albero = ast.parse(src)
    for nodo in albero.body:
        assert not isinstance(nodo, ast.Assign), \
            "costante di modulo vietata: i fattori devono essere letterali dentro le funzioni"


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w823_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st822_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) == 25
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w823_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 4
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_ui_guard_degenere_identica_helper():
    """La guard UI della scheda dichiara NON_CALCOLABILE
    per gli stessi casi degeneri degli helper:
    litri <= 0, prezzi <= 0, CAPEX <= 0,
    vita <= 0 (nessuna divergenza helper-vs-UI)."""
    src = _leggi("w823_ui.py")
    assert "float(_lt822) <= 0.0" in src
    assert "float(_pel822) <= 0.0" in src
    assert "float(_pg822) <= 0.0" in src
    assert "float(_cx822) <= 0.0" in src
    assert "int(_vita822) <= 0" in src
    assert "Verdetto: NON_CALCOLABILE" in src


def test_ui_chiamata_calcola_keyword_uguali_firma():
    """La chiamata UI a calcola usa come keyword
    esattamente i parametri della firma helper."""
    src = textwrap.dedent(_leggi("w823_ui.py"))
    albero = ast.parse(src)
    chiamate = []
    for nodo in ast.walk(albero):
        if isinstance(nodo, ast.Call):
            func = nodo.func
            if isinstance(func, ast.Name) and func.id == "mh822_calcola":
                chiamate.append({kw.arg for kw in nodo.keywords})
    assert len(chiamate) == 1
    attesi = set(inspect.signature(mh822_calcola).parameters.keys())
    assert chiamate[0] == attesi


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w823_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def822[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w823_ui.py")
        usate = set(re.findall(r'_def822\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 15
        assert usate <= set(mh822_demo().keys())
