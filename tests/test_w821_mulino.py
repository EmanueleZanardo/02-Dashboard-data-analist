"""Test nuova scheda "Mulino / molitura
cereali: motori efficienti + trasporto
pneumatico ottimizzato + recupero calore
essiccazione battono motori tradizionali
+ trasporto tradizionale + essiccazione
a gas?" (titolo completo nel frammento UI).

Business case deterministico di un mulino
guidato dalle TONNELLATE DI CEREALE MOLITO
in un anno: E_mac_base = tonnellate x
e_mac_base; E_mac_alt = tonnellate x
e_mac_alt (i motori IE4 + inverter riducono
solo la macinazione); E_pn_base = tonnellate
x e_pn_base; E_pn_alt = tonnellate x
e_pn_alt (il pneumatico ottimizzato riduce
solo il trasporto); E_base = E_mac_base +
E_pn_base; E_pdc = tonnellate x e_pdc (pompa
di calore con recupero, COP implicito
g_ess / e_pdc = 3 nel demo); E_alt =
E_mac_alt + E_pn_alt + E_pdc; gas_base =
tonnellate x g_ess (g_ess gia' consumo di
gas per tonnellata, nessun rendimento
caldaia inventato); gas_alt = 0 (la pompa
di calore sostituisce del tutto il gas);
C_base = E_base x p_el + gas_base x p_gas
+ OM_base; C_alt = E_alt x p_el + gas_alt
x p_gas + OM_alt (prezzi in EUR/kWh,
nessuna conversione / 1000); risparmio =
C_base - C_alt; CO2 evitata = (E_base x
0,25 + gas_base x 0,202 - E_alt x 0,25
- gas_alt x 0,202) / 1000 (fattori
letterali); flussi [-CAPEX, risparmio x
vita]; VAN, TIR, payback (primo anno con
cumulato >= 0); breakeven gas = (E_alt x
p_el + OM_alt - E_base x p_el - OM_base)
/ gas_base EUR/kWh, None se gas_base <=
gas_alt (qui gas_alt = 0) o numeratore < 0,
SOGLIA MINIMA quando esiste. Nel demo il
breakeven e' None (numeratore -80.000 EUR,
denominatore 2.250.000 kWh/anno):
l'alternativa vince gia' a prezzo gas zero.
Verdetto: NON_CALCOLABILE se input degenere
(tonnellate <= 0, specifici negativi,
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
helper dove previsto (tonnellate, prezzi,
CAPEX, vita). Gli zeri ammessi in entrambi
(specifici elettrici e gas, O&M, WACC,
tolleranza) non creano divergenza: con gas
specifico zero il gas base e' zero e il
breakeven e' None, e il caso resta
calcolabile in entrambi. WACC sopra 20 % e
tolleranza sopra 100 % sono ammessi negli
helper e limitati solo dagli slider UI (20,
100): nessuna divergenza nel range
raggiungibile, perche' la guard controlla
solo gli stessi limiti degli helper.
Distinzione esplicita: distinto
dall'impianto di imbottigliamento (litri
imbottigliati, riempitrici: qui niente
litri, niente bottiglie, niente riempimento,
niente soffiaggio, niente lavaggio), dal
frantoio (tonnellate di olive, acqua calda
di processo: qui niente olive, niente
malaxazione), dal birrificio (ettolitri di
birra, bollitura del mosto: qui niente
mosto, niente bollitura, niente birra da
produrre): qui driver TONNELLATE DI CEREALE
MOLITO + MOTORI IE4 + PNEUMATICO
OTTIMIZZATO + POMPA DI CALORE CON RECUPERO.

Demo (mulino): 50.000 tonnellate di cereale
molito, macinazione specifica base 65
(3.250.000 kWh_e/anno) e alternativa 48
(2.400.000 kWh_e/anno), pneumatico
specifico base 18 (900.000 kWh_e/anno) e
alternativo 12 (600.000 kWh_e/anno),
elettricita' base 4.150.000 e alternativa
3.750.000 kWh_e/anno (pompa di calore
750.000 kWh_e/anno, 15 kWh_e/t), gas
specifico 45 (2.250.000 kWh/anno, gas
alternativo 0), prezzi elettricita' 0,22 e
gas 0,055 EUR/kWh, O&M base 0 e alternativo
8.000 EUR/anno, CAPEX 420.000 EUR, WACC
5 %, vita 15 anni, tolleranza 10 % del
CAPEX. Valori calcolati eseguendo
mh821_demo_calcoli(): E_base 4.150.000,
E_alt 3.750.000, C_base 1.036.750, C_alt
833.000, risparmio 203.750, CO2_base
1.492,0, CO2_alt 937,5, CO2_evitata 554,5,
VAN 1694855,3252792954, TIR
48,38154304216884 %, payback 3, breakeven
gas None (numeratore negativo), verdetto
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

from w822_helpers import (
    demo_calcoli,
    mh821_breakeven_gas,
    mh821_c_alt,
    mh821_c_base,
    mh821_calcola,
    mh821_co2_alt,
    mh821_co2_base,
    mh821_co2_evitata,
    mh821_csv,
    mh821_demo,
    mh821_demo_calcoli,
    mh821_e_alt,
    mh821_e_base,
    mh821_e_mac_alt,
    mh821_e_mac_base,
    mh821_e_pdc,
    mh821_e_pn_alt,
    mh821_e_pn_base,
    mh821_flussi,
    mh821_gas_alt,
    mh821_gas_base,
    mh821_int_pos,
    mh821_nneg,
    mh821_num,
    mh821_payback,
    mh821_pos,
    mh821_risparmio,
    mh821_tir,
    mh821_valida,
    mh821_van,
    mh821_verdetto,
)

_DEMO = {
    "e_mac_base_kwh_e_anno": 3250000.0,
    "e_mac_alt_kwh_e_anno": 2400000.0,
    "e_pn_base_kwh_e_anno": 900000.0,
    "e_pn_alt_kwh_e_anno": 600000.0,
    "e_pdc_kwh_e_anno": 750000.0,
    "e_base_kwh_e_anno": 4150000.0,
    "e_alt_kwh_e_anno": 3750000.0,
    "gas_base_kwh_anno": 2250000.0,
    "gas_alt_kwh_anno": 0.0,
    "c_base_eur_anno": 1036750.0,
    "c_alt_eur_anno": 833000.0,
    "risparmio_eur_anno": 203750.0,
    "co2_base_t_anno": 1492.0,
    "co2_alt_t_anno": 937.5,
    "co2_evitata_t_anno": 554.5,
    "van": 1694855.3252792954,
    "tir": 48.38154304216884,
}


def _demo_kwargs():
    return dict(mh821_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh821_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh821_num(3, "x") == 3.0
    assert mh821_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh821_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh821_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh821_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh821_pos(0, "x")
    with pytest.raises(ValueError):
        mh821_pos(-1, "x")
    assert mh821_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh821_int_pos(5.0, "x") == 5
    assert mh821_int_pos(15.0, "x") == 15
    with pytest.raises(ValueError):
        mh821_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh821_int_pos(0, "x")


# ---------------------------------------------------------------- fisica base
def test_e_mac_e_pn_e_base():
    assert mh821_e_mac_base(50000, 65) == 3250000.0
    assert mh821_e_mac_alt(50000, 48) == 2400000.0
    assert mh821_e_pn_base(50000, 18) == 900000.0
    assert mh821_e_pn_alt(50000, 12) == 600000.0
    assert mh821_e_base(3250000.0, 900000.0) == 4150000.0
    with pytest.raises(ValueError):
        mh821_e_base(-1, 900000.0)
    with pytest.raises(ValueError):
        mh821_e_mac_base(0, 65)


def test_e_pdc_e_alt():
    assert mh821_e_pdc(50000, 15) == 750000.0
    assert mh821_e_pdc(50000, 0) == 0.0
    assert mh821_e_alt(2400000.0, 600000.0, 750000.0) == 3750000.0
    with pytest.raises(ValueError):
        mh821_e_alt(2400000.0, 600000.0, -1)
    with pytest.raises(ValueError):
        mh821_e_pdc(0, 15)


def test_gas_base_alt():
    assert mh821_gas_base(50000, 45) == 2250000.0
    assert mh821_gas_base(50000, 0) == 0.0
    assert mh821_gas_alt() == 0.0
    with pytest.raises(ValueError):
        mh821_gas_base(50000, -0.01)
    with pytest.raises(ValueError):
        mh821_gas_base(0, 45)


def test_c_base_c_alt_scomposizione():
    assert mh821_c_base(4150000.0, 0.22, 2250000.0, 0.055,
                        0) == pytest.approx(1036750.0)
    assert mh821_c_alt(3750000.0, 0.22, 0.0, 0.055,
                       8000) == pytest.approx(833000.0)
    with pytest.raises(ValueError):
        mh821_c_base(4150000.0, 0, 2250000.0, 0.055, 0)
    with pytest.raises(ValueError):
        mh821_c_alt(3750000.0, 0.22, 0.0, 0, 8000)
    with pytest.raises(ValueError):
        mh821_c_base(4150000.0, 0.22, 2250000.0, 0.055, -1)


def test_risparmio_segno():
    assert mh821_risparmio(1036750.0, 833000.0) == pytest.approx(203750.0)
    assert mh821_risparmio(833000.0, 833000.0) == pytest.approx(0.0, abs=1e-9)


def test_co2_base_alt_evitata():
    assert mh821_co2_base(4150000.0, 2250000.0) == pytest.approx(1492.0)
    assert mh821_co2_alt(3750000.0, 0.0) == pytest.approx(937.5)
    assert mh821_co2_evitata(4150000.0, 2250000.0,
                             3750000.0, 0.0) == pytest.approx(554.5)
    assert mh821_co2_base(0, 0) == 0.0
    assert mh821_co2_alt(0, 0) == 0.0
    with pytest.raises(ValueError):
        mh821_co2_base(4150000.0, -1)
    with pytest.raises(ValueError):
        mh821_co2_alt(-1, 0.0)


def test_breakeven_demo_none_numeratore_negativo():
    bc = mh821_demo_calcoli()
    assert bc["breakeven_gas_eur_kwh"] is None
    # Numeratore: 3750000*0,22 + 8000 - 4150000*0,22 - 0 = -80000 < 0.
    assert mh821_breakeven_gas(3750000.0, 0.22, 8000, 4150000.0,
                               0, 2250000.0,
                               0.0) is None
    # Denominatore nullo (gas_base = 0) -> None.
    assert mh821_breakeven_gas(3750000.0, 0.22, 8000, 4150000.0,
                               0, 0.0, 0.0) is None
    # Variante gas specifico zero -> breakeven None.
    assert _variante(g_ess_kwh_t=0)["breakeven_gas_eur_kwh"] is None
    with pytest.raises(ValueError):
        mh821_breakeven_gas(3750000.0, 0.22, 8000, 4150000.0,
                            0, -1, 0.0)


def test_breakeven_variante_om_alt_valore():
    # Con O&M alternativo 100.000 il numeratore
    # diventa positivo e il breakeven esiste:
    # 12.000 / 2.250.000 = 0,005333... EUR/kWh.
    bc = _variante(om_alt=100000)
    assert bc["breakeven_gas_eur_kwh"] == pytest.approx(0.005333333333333333)
    assert mh821_breakeven_gas(3750000.0, 0.22, 100000, 4150000.0,
                               0, 2250000.0,
                               0.0) == pytest.approx(0.005333333333333333)


def test_breakeven_verifica_pareggio_su_variante():
    be = _variante(om_alt=100000)["breakeven_gas_eur_kwh"]
    bc = _variante(om_alt=100000, p_gas=be)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_breakeven_soglia_minima_su_variante():
    be = _variante(om_alt=100000)["breakeven_gas_eur_kwh"]
    bc_alto = _variante(om_alt=100000, p_gas=0.055)
    bc_basso = _variante(om_alt=100000, p_gas=0.001)
    assert bc_alto["c_alt_eur_anno"] < bc_alto["c_base_eur_anno"]
    assert bc_basso["c_alt_eur_anno"] > bc_basso["c_base_eur_anno"]
    assert bc_alto["risparmio_eur_anno"] > 0.0
    assert bc_basso["verdetto"] == "NON_CALCOLABILE"
    assert bc_alto["risparmio_eur_anno"] == pytest.approx(111750.0)
    assert bc_alto["verdetto"] == "CONVIENTE"


def test_breakeven_variante_senza_motori():
    # Senza motori efficienti il numeratore
    # diventa positivo: 107.000 / 2.250.000.
    bc = _variante(e_mac_alt_kwh_e_t=65)
    assert bc["breakeven_gas_eur_kwh"] == pytest.approx(0.04755555555555555)


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh821_flussi(420000, 203750.0, 15)
    assert len(fl) == 16
    assert fl[0] == -420000
    assert all(f == pytest.approx(203750.0) for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh821_demo_calcoli()
    assert bc["van"] == pytest.approx(1694855.3252792954)
    assert mh821_van([-420000] + [203750.0] * 15,
                     0) == pytest.approx(2636250.0)
    assert mh821_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh821_demo_calcoli()
    assert bc["tir"] == pytest.approx(48.38154304216884)
    assert mh821_tir([-420000] + [203750.0] * 15) == \
        pytest.approx(0.4838154304216884)
    tir = mh821_tir([-420000] + [203750.0] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-420000] + [203750.0] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh821_payback([-420000] + [203750.0] * 15) == 3
    assert mh821_payback([-420000] + [-1000.0] * 15) is None
    assert mh821_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh821_verdetto(203750.0, 1694855.3252792954, 420000,
                          10.0) == "CONVIENTE"
    assert mh821_verdetto(203750.0, -1500.0, 420000,
                          10.0) == "MARGINALE"
    assert mh821_verdetto(203750.0, -42000.0, 420000, 10.0) == "MARGINALE"
    assert mh821_verdetto(203750.0, -42000.01, 420000, 10.0) == "NON_CONVIENTE"
    assert mh821_verdetto(203750.0, 0.0, 420000, 10.0) == "MARGINALE"
    assert mh821_verdetto(0.0, 1694855.33, 420000,
                          10.0) == "NON_CALCOLABILE"
    assert mh821_verdetto(-38250.0, -817021.92, 420000,
                          10.0) == "NON_CALCOLABILE"
    assert mh821_verdetto(None, 1694855.33, 420000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh821_verdetto(float("nan"), 1694855.33, 420000, 10.0)
    with pytest.raises(ValueError):
        mh821_verdetto(203750.0, 1694855.33, 0, 10.0)
    with pytest.raises(ValueError):
        mh821_verdetto(203750.0, 1694855.33, 420000, -1)


def test_valida_demo_ok():
    v = mh821_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("tonnellate", "50000"),
                       ("tonnellate", float("nan")),
                       ("tonnellate", float("inf")),
                       ("tonnellate", True),
                       ("p_gas", None),
                       ("g_ess_kwh_t", "45")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh821_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("tonnellate", 0),
                          ("tonnellate", -10),
                          ("e_mac_base_kwh_e_t", -1),
                          ("e_mac_alt_kwh_e_t", -1),
                          ("e_pn_base_kwh_e_t", -1),
                          ("e_pn_alt_kwh_e_t", -1),
                          ("g_ess_kwh_t", -1),
                          ("e_pdc_kwh_e_t", -1),
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
        assert mh821_valida(**d)["valido"] is False


def test_valida_accetta_limiti_e_nessun_tetto_wacc_tolleranza():
    d = _demo_kwargs()
    d.update({"e_mac_base_kwh_e_t": 0,
              "e_mac_alt_kwh_e_t": 0,
              "e_pn_base_kwh_e_t": 0,
              "e_pn_alt_kwh_e_t": 0,
              "g_ess_kwh_t": 0,
              "e_pdc_kwh_e_t": 0,
              "om_base": 0, "om_alt": 0,
              "wacc_pct": 0,
              "tolleranza_pct": 0})
    assert mh821_valida(**d)["valido"] is True
    # Il brief non impone tetti superiori a WACC
    # e tolleranza: gli helper li ammettono.
    d["wacc_pct"] = 60
    d["tolleranza_pct"] = 200
    assert mh821_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh821_demo()
    assert d["tonnellate"] == 50000
    assert d["e_mac_base_kwh_e_t"] == 65
    assert d["e_mac_alt_kwh_e_t"] == 48
    assert d["e_pn_base_kwh_e_t"] == 18
    assert d["e_pn_alt_kwh_e_t"] == 12
    assert d["g_ess_kwh_t"] == 45
    assert d["e_pdc_kwh_e_t"] == 15
    assert d["p_el"] == 0.22
    assert d["p_gas"] == 0.055
    assert d["om_base"] == 0
    assert d["om_alt"] == 8000
    assert d["capex"] == 420000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    bc = mh821_demo_calcoli()
    for chiave, atteso in _DEMO.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert got == pytest.approx(atteso, rel=1e-9), chiave
    assert bc["payback"] == 3
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True
    assert bc["breakeven_gas_eur_kwh"] is None
    assert demo_calcoli()["van"] == bc["van"]


def test_demo_calcoli_fisica_economia():
    bc = mh821_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(1036750.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(833000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(203750.0)
    assert bc["co2_base_t_anno"] == pytest.approx(1492.0)
    assert bc["co2_alt_t_anno"] == pytest.approx(937.5)
    assert bc["co2_evitata_t_anno"] == pytest.approx(554.5)
    assert bc["gas_base_kwh_anno"] == pytest.approx(2250000.0)
    assert bc["gas_alt_kwh_anno"] == 0.0
    assert bc["e_mac_base_kwh_e_anno"] == pytest.approx(3250000.0)
    assert bc["e_mac_alt_kwh_e_anno"] == pytest.approx(2400000.0)
    assert bc["e_pn_base_kwh_e_anno"] == pytest.approx(900000.0)
    assert bc["e_pn_alt_kwh_e_anno"] == pytest.approx(600000.0)
    assert bc["e_pdc_kwh_e_anno"] == pytest.approx(750000.0)
    assert bc["e_base_kwh_e_anno"] == pytest.approx(4150000.0)
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(3750000.0)


def test_demo_flussi_e_cumulato():
    bc = mh821_demo_calcoli()
    assert bc["flussi"][0] == -420000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(203750.0) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -420000
    assert righe.iloc[2]["Cumulato (EUR)"] == pytest.approx(-12500.0)
    assert righe.iloc[3]["Cumulato (EUR)"] == pytest.approx(191250.0)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(2636250.0)


def test_demo_tabella_righe():
    bc = mh821_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Macinazione baseline (kWh_e/anno)"] == pytest.approx(3250000.0)
    assert mappa["Macinazione alternativa (kWh_e/anno)"] == pytest.approx(2400000.0)
    assert mappa["Pneumatico baseline (kWh_e/anno)"] == pytest.approx(900000.0)
    assert mappa["Pneumatico alternativo (kWh_e/anno)"] == pytest.approx(600000.0)
    assert mappa["Pompa di calore (kWh_e/anno)"] == pytest.approx(750000.0)
    assert mappa["Elettricita' base (kWh_e/anno)"] == pytest.approx(4150000.0)
    assert mappa["Elettricita' alternativa (kWh_e/anno)"] == pytest.approx(3750000.0)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(2250000.0)
    assert mappa["Gas alternativo (kWh/anno)"] == 0.0
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(1036750.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(833000.0)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(203750.0)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(554.5)
    assert mappa["Payback (anni)"] == 3
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/kWh)"] is None


def test_demo_coerenza_interna():
    bc = mh821_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["gas_base_kwh_anno"] == pytest.approx(
        bc["tonnellate"] * bc["g_ess_kwh_t"])
    assert bc["e_mac_base_kwh_e_anno"] == pytest.approx(
        bc["tonnellate"] * bc["e_mac_base_kwh_e_t"])
    assert bc["e_mac_alt_kwh_e_anno"] == pytest.approx(
        bc["tonnellate"] * bc["e_mac_alt_kwh_e_t"])
    assert bc["e_pn_base_kwh_e_anno"] == pytest.approx(
        bc["tonnellate"] * bc["e_pn_base_kwh_e_t"])
    assert bc["e_pn_alt_kwh_e_anno"] == pytest.approx(
        bc["tonnellate"] * bc["e_pn_alt_kwh_e_t"])
    assert bc["e_pdc_kwh_e_anno"] == pytest.approx(
        bc["tonnellate"] * bc["e_pdc_kwh_e_t"])
    assert bc["e_base_kwh_e_anno"] == pytest.approx(
        bc["e_mac_base_kwh_e_anno"] + bc["e_pn_base_kwh_e_anno"])
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(
        bc["e_mac_alt_kwh_e_anno"] + bc["e_pn_alt_kwh_e_anno"]
        + bc["e_pdc_kwh_e_anno"])
    assert bc["gas_alt_kwh_anno"] == 0.0
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
    tn, emb, ema = 50000, 65, 48
    epb, epa, ges, epd = 18, 12, 45, 15
    pel, pg = 0.22, 0.055
    omb, oma, cx = 0, 8000, 420000
    wacc, vita = 5.0, 15
    e_mac_b = tn * emb
    e_mac_a = tn * ema
    e_pn_b = tn * epb
    e_pn_a = tn * epa
    e_pdc = tn * epd
    eb = e_mac_b + e_pn_b
    ea = e_mac_a + e_pn_a + e_pdc
    gasb = tn * ges
    gasa = 0.0
    cb = eb * pel + gasb * pg + omb
    ca = ea * pel + gasa * pg + oma
    risp = cb - ca
    co2b = (eb * 0.25 + gasb * 0.202) / 1000.0
    co2a = (ea * 0.25 + gasa * 0.202) / 1000.0
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    bc = mh821_demo_calcoli()
    assert bc["e_mac_base_kwh_e_anno"] == pytest.approx(e_mac_b)
    assert bc["e_mac_alt_kwh_e_anno"] == pytest.approx(e_mac_a)
    assert bc["e_pn_base_kwh_e_anno"] == pytest.approx(e_pn_b)
    assert bc["e_pn_alt_kwh_e_anno"] == pytest.approx(e_pn_a)
    assert bc["e_pdc_kwh_e_anno"] == pytest.approx(e_pdc)
    assert bc["e_base_kwh_e_anno"] == pytest.approx(eb)
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(ea)
    assert bc["gas_base_kwh_anno"] == pytest.approx(gasb)
    assert bc["gas_alt_kwh_anno"] == gasa
    assert bc["c_base_eur_anno"] == pytest.approx(cb)
    assert bc["c_alt_eur_anno"] == pytest.approx(ca)
    assert bc["risparmio_eur_anno"] == pytest.approx(risp)
    assert bc["co2_base_t_anno"] == pytest.approx(co2b)
    assert bc["co2_alt_t_anno"] == pytest.approx(co2a)
    assert bc["co2_evitata_t_anno"] == pytest.approx(co2)
    assert bc["van"] == pytest.approx(van)
    assert bc["breakeven_gas_eur_kwh"] is None


def test_demo_verdetto_coerente_con_risparmio_e_van():
    bc = mh821_demo_calcoli()
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] > 0.0
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["tir"] is not None and bc["tir"] > bc["wacc_pct"]
    assert bc["payback"] == 3


# ---------------------------------------------------------------- varianti
def test_variante_senza_motori_non_convinte():
    # Macinazione alternativa 65 = niente
    # risparmio dai motori efficienti: il caso
    # diventa NON_CONVIENTE.
    bc = _variante(e_mac_alt_kwh_e_t=65)
    assert bc["e_mac_alt_kwh_e_anno"] == pytest.approx(3250000.0)
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(4600000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(1020000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(16750.0)
    assert bc["van"] == pytest.approx(-246140.72786047508)
    assert bc["tir"] == pytest.approx(-5.828006081384447)
    assert bc["payback"] is None
    assert bc["breakeven_gas_eur_kwh"] == pytest.approx(0.04755555555555555)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_senza_pneumatico_convinte():
    # Pneumatico alternativo 18 = niente
    # risparmio dal pneumatico ottimizzato:
    # il caso resta CONVIENTE.
    bc = _variante(e_pn_alt_kwh_e_t=18)
    assert bc["e_pn_alt_kwh_e_anno"] == pytest.approx(900000.0)
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(4050000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(899000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(137750.0)
    assert bc["van"] == pytest.approx(1009797.8947593761)
    assert bc["tir"] == pytest.approx(32.30537557270172)
    assert bc["payback"] == 4
    assert bc["breakeven_gas_eur_kwh"] is None
    assert bc["verdetto"] == "CONVIENTE"


def test_pdc_zero_non_e_scenario_senza_gas():
    # ATTENZIONE STRUTTURALE: il modello pone
    # gas_alt = 0 per costruzione (la pompa di
    # calore sostituisce del tutto il gas).
    # Porre e_pdc = 0 NON torna al gas: toglie
    # solo l'elettricita' della pompa di calore
    # e lascia gas_alt = 0, cioe' essiccare
    # gratis. Il controfattuale "gas che resta"
    # (c_alt 791.750, risparmio 245.000, VAN
    # 2.123.016,22, CO2 evitata 287,50) vive
    # fuori dal modello ed e' documentato solo
    # nelle note UI, mai come variante helper.
    bc = _variante(e_pdc_kwh_e_t=0)
    assert bc["gas_alt_kwh_anno"] == 0.0
    assert bc["e_pdc_kwh_e_anno"] == 0.0
    assert bc["e_alt_kwh_e_anno"] == pytest.approx(3000000.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(668000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(368750.0)
    assert bc["van"] == pytest.approx(3407498.9015790923)
    assert bc["tir"] == pytest.approx(87.79072664555557)
    assert bc["payback"] == 2
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_600000_convinte():
    bc = _variante(capex=600000)
    assert bc["risparmio_eur_anno"] == pytest.approx(203750.0)
    assert bc["van"] == pytest.approx(1514855.3252792954)
    assert bc["tir"] == pytest.approx(33.51363870241919)
    assert bc["payback"] == 3
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_om_alt_250000_non_calcolabile():
    # O&M alt 250.000: risparmio negativo negli
    # helper (calcolabile, non solleva), verdetto
    # NON_CALCOLABILE; stessa guard della UI.
    bc = _variante(om_alt=250000)
    assert bc["valid"] is True
    assert bc["c_alt_eur_anno"] == pytest.approx(1075000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-38250.0)
    assert bc["van"] == pytest.approx(-817021.9199604079)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"]
    assert bc["payback"] is None
    assert bc["tir"] is None
    assert bc["breakeven_gas_eur_kwh"] == pytest.approx(0.072)


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(2636250.0)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(1153303.4918214052)
    assert bc2["tir"] == pytest.approx(47.51786895753292)
    assert bc2["payback"] == 3
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_gas_zero_breakeven_none():
    # Gas specifico zero: gas base zero,
    # breakeven None, risparmio solo elettrico
    # (80.000 EUR/anno) e VAN positiva, quindi
    # CONVIENTE con payback 6 anni.
    bc = _variante(g_ess_kwh_t=0)
    assert bc["gas_base_kwh_anno"] == 0.0
    assert bc["gas_alt_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(80000.0)
    assert bc["van"] == pytest.approx(410372.6430544473)
    assert bc["tir"] == pytest.approx(17.31071683794203)
    assert bc["payback"] == 6
    assert bc["breakeven_gas_eur_kwh"] is None
    assert bc["verdetto"] == "CONVIENTE"


def test_monotonia_prezzo_gas_crescente():
    base = mh821_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas=0.056)["risparmio_eur_anno"]
    basso = _variante(p_gas=0.054)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(2250.0, abs=1e-6)
    assert base - basso == pytest.approx(2250.0, abs=1e-6)


def test_monotonia_pdc_crescente_risparmio_cala():
    # Piu' elettricita' di pompa di calore, meno
    # risparmio: la pompa di calore costa piu'
    # del gas che sostituisce a questi prezzi.
    assert _variante(e_pdc_kwh_e_t=20)["risparmio_eur_anno"] < \
        mh821_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(e_pdc_kwh_e_t=10)["risparmio_eur_anno"] > \
        mh821_demo_calcoli()["risparmio_eur_anno"]


def test_demo_deterministica_due_chiamate():
    a = mh821_demo_calcoli()
    b = mh821_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh821_demo().keys()) == {
        "tonnellate", "e_mac_base_kwh_e_t", "e_mac_alt_kwh_e_t",
        "e_pn_base_kwh_e_t", "e_pn_alt_kwh_e_t",
        "g_ess_kwh_t", "e_pdc_kwh_e_t",
        "p_el", "p_gas", "om_base", "om_alt",
        "capex", "wacc_pct", "vita_anni",
        "tolleranza_pct"}


# ---------------------------------------------------------------- degenere
def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"tonnellate": 0},
               {"tonnellate": -10},
               {"e_mac_base_kwh_e_t": -1},
               {"e_mac_alt_kwh_e_t": -1},
               {"e_pn_base_kwh_e_t": -1},
               {"e_pn_alt_kwh_e_t": -1},
               {"g_ess_kwh_t": -1},
               {"e_pdc_kwh_e_t": -1},
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
        assert mh821_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"tonnellate": "50000"},
               {"tonnellate": float("nan")},
               {"p_gas": float("inf")},
               {"capex": True},
               {"g_ess_kwh_t": "45"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh821_valida(**d)["valido"] is False


def test_zeri_ammessi_non_sollevano_e_nessuna_divergenza():
    # Zeri ammessi in entrambi (helper e UI):
    # specifici elettrici e gas, O&M, WACC,
    # tolleranza. Qui si verifica che non
    # sollevano e restano calcolabili.
    for kw in ({"e_mac_base_kwh_e_t": 0},
               {"e_mac_alt_kwh_e_t": 0},
               {"e_pn_base_kwh_e_t": 0},
               {"e_pn_alt_kwh_e_t": 0},
               {"g_ess_kwh_t": 0},
               {"e_pdc_kwh_e_t": 0},
               {"om_base": 0},
               {"om_alt": 0},
               {"wacc_pct": 0},
               {"tolleranza_pct": 0}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["verdetto"] in ("CONVIENTE", "MARGINALE",
                                  "NON_CONVIENTE", "NON_CALCOLABILE")


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    bc = _variante(om_alt=250000)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] <= 0.0
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"]


def test_pareggio_esatto_tolleranza_float():
    # A pareggio esatto (prezzo gas = breakeven
    # della variante con O&M alternativo 100.000)
    # il risparmio e' zero (circa 0.0, quindi
    # guard NON_CALCOLABILE): in nessun caso
    # CONVIENTE.
    be = _variante(om_alt=100000)["breakeven_gas_eur_kwh"]
    bc = _variante(om_alt=100000, p_gas=be)
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["verdetto"] != "CONVIENTE"
    bc2 = _variante(om_alt=100000, p_gas=0.055)
    assert bc2["risparmio_eur_anno"] == pytest.approx(111750.0, abs=1e-6)
    assert bc2["verdetto"] == "CONVIENTE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh821_demo_calcoli()
    testo = mh821_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_gas_eur_kwh" in testo
    assert "co2_evitata_t_anno" in testo
    assert "gas_base_kwh_anno" in testo
    assert "e_pn_alt_kwh_e_anno" in testo
    assert "e_mac_alt_kwh_e_anno" in testo
    assert "e_pdc_kwh_e_anno" in testo
    assert "gas_alt_kwh_anno" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh821_demo_calcoli()
    testo = mh821_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"e_pn_base_kwh_e_anno;{bc['e_pn_base_kwh_e_anno']}" in testo
    assert f"gas_base_kwh_anno;{bc['gas_base_kwh_anno']}" in testo
    assert f"e_mac_base_kwh_e_anno;{bc['e_mac_base_kwh_e_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh821_demo_calcoli()
    testo = mh821_csv(bc, _demo_kwargs())
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
    return ["mh" + "82" + "0", "st" + "82" + "0",
            "tab" + "82" + "0", "w" + "82" + "1"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w822_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w822_ui.py"))
    ast.parse(src)
    assert src.startswith("# W822")
    assert "with tab821:" in src


def test_ui_apre_scheda_attesa_una_volta():
    """Il frammento UI apre la scheda attesa, una sola volta."""
    src = _leggi("w822_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert m.group(1) == "821"
    assert src.count("with tab821:") == 1
    assert src.count("    with tab821:") == 1


def test_ui_titolo_atteso():
    src = _leggi("w822_ui.py")
    titolo = ("🌾 Mulino / molitura cereali: "
              "motori efficienti + "
              "trasporto pneumatico ottimizzato + "
              "recupero calore essiccazione battono "
              "motori tradizionali + trasporto "
              "tradizionale + essiccazione a gas?")
    assert src.count(titolo) == 2


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w822_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_helpers_senza_costanti_di_modulo():
    src = _leggi("w822_helpers.py")
    albero = ast.parse(src)
    for nodo in albero.body:
        assert not isinstance(nodo, ast.Assign), \
            "costante di modulo vietata: i fattori devono essere letterali dentro le funzioni"


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w822_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st821_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) == 25
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w822_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 4
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_ui_guard_degenere_identica_helper():
    """La guard UI della scheda dichiara NON_CALCOLABILE
    per gli stessi casi degeneri degli helper:
    tonnellate <= 0, prezzi <= 0, CAPEX <= 0,
    vita <= 0 (nessuna divergenza helper-vs-UI)."""
    src = _leggi("w822_ui.py")
    assert "float(_tn821) <= 0.0" in src
    assert "float(_pel821) <= 0.0" in src
    assert "float(_pg821) <= 0.0" in src
    assert "float(_cx821) <= 0.0" in src
    assert "int(_vita821) <= 0" in src
    assert "Verdetto: NON_CALCOLABILE" in src


def test_ui_chiamata_calcola_keyword_uguali_firma():
    """La chiamata UI a calcola usa come keyword
    esattamente i parametri della firma helper."""
    src = textwrap.dedent(_leggi("w822_ui.py"))
    albero = ast.parse(src)
    chiamate = []
    for nodo in ast.walk(albero):
        if isinstance(nodo, ast.Call):
            func = nodo.func
            if isinstance(func, ast.Name) and func.id == "mh821_calcola":
                chiamate.append({kw.arg for kw in nodo.keywords})
    assert len(chiamate) == 1
    attesi = set(inspect.signature(mh821_calcola).parameters.keys())
    assert chiamate[0] == attesi


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w822_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def821[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w822_ui.py")
        usate = set(re.findall(r'_def821\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 15
        assert usate <= set(mh821_demo().keys())
