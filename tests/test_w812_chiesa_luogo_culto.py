"""Test nuova scheda "Chiesa / luogo di
culto: riscaldamento localizzato a panche +
pompa di calore batte caldaia a gas ad aria
+ illuminazione tradizionale?" (titolo
completo nel frammento UI). Contenuto pronto
da scrivere in repo come test della scheda
chiesa.

Business case deterministico di una chiesa
guidata dai M2 DI SUPERFICIE e dalle ORE DI
USO A SETTIMANA: i m2 guidano il
riscaldamento, le ore a settimana per le
settimane all'anno guidano l'anno e
l'illuminazione, la quota panche guida la
zona occupata scaldata a comfort, il resto
del volume e' mantenuto solo antigelo/fondo
con un fattore di mantenimento, i litri a
settimana guidano l'ACS, la potenza di
illuminazione di base per le ore annue guida
l'illuminazione.
Riscaldamento = S x q_risc; zona occupata =
Q_risc x quota_panche; mantenimento = Q_risc
x (1 - quota_panche) x f_mantenimento;
fabbisogno termico alternativo = zona +
mantenimento; ore annue = ore a settimana x
settimane; ACS = litri_settimana x settimane
x 4,186 x delta_T / 3600; illuminazione base
= ore annue x potenza di base e LED = base x
f_led; gas baseline = (riscaldamento + ACS)
/ 0,90 (eta_caldaia letterale, senza
localizzazione); pompa di calore =
fabbisogno alternativo / 3,2; ACS alt = ACS
/ 3,0 (COP letterali); E_base =
illuminazione base (in baseline l'unico
carico elettrico e' l'illuminazione
tradizionale); E_alt = pompa di calore + ACS
alt + illuminazione LED; C_base = gas_base /
1000 x p_gas + E_base / 1000 x p_el +
O&M_base; C_alt = E_alt / 1000 x p_el +
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
(superficie <= 0, q <= 0, quota o fattori
fuori [0, 1], ore <= 0, settimane <= 0,
litri <= 0, delta_T <= 0, potenza <= 0,
prezzi <= 0, CAPEX <= 0, vita <= 0) o se
risparmio <= 0 (guard degenere: UI salta KPI,
grafico, tabella e CSV); altrimenti CONVIENTE
se VAN > 0, MARGINALE se VAN negativa entro
tolleranza % del CAPEX, NON_CONVIENTE se VAN
negativa oltre la tolleranza. Differenze
UI-vs-helper documentate: S = 0 e' calcolabile
negli helper (risparmio -146,01 EUR/anno, VAN
-31.515,49 EUR, verdetto NON_CALCOLABILE,
breakeven 410,47 EUR/MWh) e bloccato dalla
guard UI (NON_CALCOLABILE): qui NON c'e'
divergenza di verdetto, solo guard prima
(l'ACS resta anche senza superficie, ma non
basta a rendere positivo il risparmio);
CAPEX = 0 e' CONVIENTE negli helper (VAN
positiva, TIR None, payback 0) ma bloccato
dalla guard UI; prezzi = 0 sono ammessi negli
helper ma bloccati dalla guard UI (p_el = 0
resta CONVIENTE negli helper, p_gas = 0 da'
invece risparmio NEGATIVO negli helper,
-3.469,03 EUR/anno, verdetto NON_CALCOLABILE:
per gas zero QUI NON c'e' divergenza di
verdetto helper-vs-UI, solo guard prima).
Distinzione esplicita: distinto dall'asilo
(giorni di apertura, mensa con pasti al
giorno, lavanderia con kg al giorno: qui
niente mensa, niente pasti, niente
lavanderia), dall'ospedale (posti letto e
reparti di degenza umana: qui nessun posto
letto, nessun reparto ospedaliero),
dall'albergo (pernottamenti e camere: qui
nessun pernottamento, nessuna camera), dalla
palestra (docce e spogliatoi: qui niente
docce, niente spogliatoi): qui driver M2 +
ORE + QUOTA PANCHE + ACS + ILLUMINAZIONE,
con riscaldamento intermittente di un grande
volume usato poche ore a settimana.

Demo (chiesa): superficie 600 m2, 120
kWh_th/m2 di riscaldamento (72.000
kWh_th/anno), quota panche 0,45 (32.400
kWh_th/anno) e fattore di mantenimento 0,20
(7.920 kWh_th/anno, totale alternativo
40.320 kWh_th/anno), 12 ore a settimana per
52 settimane (624 ore all'anno), ACS 200
litri a settimana con delta_T 35 K (10.400
litri all'anno, 423,251... kWh_th/anno),
illuminazione di base 8 kW (4.992 kWh_e/anno)
con fattore LED 0,35 (1.747,20 kWh_e/anno),
gas 100, el 260 EUR/MWh, O&M base 1.500, alt
2.500, CAPEX 30.000, WACC 5 %, vita 15,
tolleranza 10 % del CAPEX. Valori calcolati
eseguendo mh812_demo_calcoli():
Q_risc 72.000, Q_locale 32.400, Q_mant 7.920,
Q_alt_th 40.320, ore_anno 624, Q_acs
423,25111111111113, E_ill_base 4.992,
E_ill_alt 1.747,2, gas_base 80.470,27901234568,
E_pdc 12.600, E_acs_alt 141,08370370370372,
E_base 4.992, E_alt 14.488,283703703702,
C_base 10.844,94790123457, C_alt
6.266,953762962963, risparmio
4.577,994138271606, CO2_base
17,841255802469135, CO2_alt 5,070899296296296,
CO2_evitata 12,77035650617284, VAN
17.518,013656054503, TIR 12,731367600619304 %,
payback 7, breakeven gas 43,109503353787886
EUR/MWh (soglia minima), verdetto CONVIENTE.
"""

import ast
import inspect
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w813_helpers import (
    demo_calcoli,
    mh812_breakeven_gas,
    mh812_c_alt,
    mh812_c_base,
    mh812_calcola,
    mh812_co2_alt,
    mh812_co2_base,
    mh812_co2_evitata,
    mh812_csv,
    mh812_demo,
    mh812_demo_calcoli,
    mh812_e_acs_alt,
    mh812_e_alt,
    mh812_e_base,
    mh812_e_ill_alt,
    mh812_e_ill_base,
    mh812_e_pdc,
    mh812_flussi,
    mh812_frazione,
    mh812_gas_base,
    mh812_int_pos,
    mh812_num,
    mh812_nneg,
    mh812_ore_anno,
    mh812_payback,
    mh812_pct_tolleranza,
    mh812_pos,
    mh812_pct_wacc,
    mh812_q_acs,
    mh812_q_alt_th,
    mh812_q_locale,
    mh812_q_mant,
    mh812_q_risc,
    mh812_risparmio,
    mh812_tir,
    mh812_valida,
    mh812_van,
    mh812_verdetto,
)

_DEMO = {
    "q_risc_kwh_anno": 72000.0,
    "q_locale_kwh_anno": 32400.0,
    "q_mant_kwh_anno": 7920.0,
    "q_alt_th_kwh_anno": 40320.0,
    "ore_anno": 624,
    "q_acs_kwh_anno": 423.25111111111113,
    "e_ill_base_kwh_anno": 4992.0,
    "e_ill_alt_kwh_anno": 1747.1999999999998,
    "gas_base_kwh_anno": 80470.27901234568,
    "e_pdc_kwh_anno": 12600.0,
    "e_acs_alt_kwh_anno": 141.08370370370372,
    "e_base_kwh_anno": 4992.0,
    "e_alt_kwh_anno": 14488.283703703702,
    "c_base_eur_anno": 10844.94790123457,
    "c_alt_eur_anno": 6266.953762962963,
    "risparmio_eur_anno": 4577.994138271606,
    "co2_base_t_anno": 17.841255802469135,
    "co2_alt_t_anno": 5.070899296296296,
    "co2_evitata_t_anno": 12.77035650617284,
    "van": 17518.013656054503,
    "tir": 12.731367600619304,
    "breakeven_gas_eur_mwh": 43.109503353787886,
}


def _demo_kwargs():
    return dict(mh812_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh812_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh812_num(3, "x") == 3.0
    assert mh812_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh812_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh812_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh812_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh812_pos(0, "x")
    with pytest.raises(ValueError):
        mh812_pos(-1, "x")
    assert mh812_pos(0.5, "x") == 0.5


def test_frazione_limiti():
    assert mh812_frazione(0, "x") == 0.0
    assert mh812_frazione(1, "x") == 1.0
    assert mh812_frazione(0.45, "x") == 0.45
    assert mh812_frazione(0.20, "x") == 0.20
    assert mh812_frazione(0.35, "x") == 0.35
    with pytest.raises(ValueError):
        mh812_frazione(-0.01, "x")
    with pytest.raises(ValueError):
        mh812_frazione(1.01, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh812_int_pos(5.0, "x") == 5
    assert mh812_int_pos(52.0, "x") == 52
    with pytest.raises(ValueError):
        mh812_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh812_int_pos(0, "x")


def test_pct_wacc_limiti():
    assert mh812_pct_wacc(0, "x") == 0.0
    assert mh812_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh812_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh812_pct_tolleranza(0, "x") == 0.0
    assert mh812_pct_tolleranza(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh812_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh812_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_q_risc_locale_mant_alt():
    assert mh812_q_risc(600, 120) == 72000.0
    assert mh812_q_risc(0, 120) == 0.0
    with pytest.raises(ValueError):
        mh812_q_risc(-1, 120)
    assert mh812_q_locale(72000.0, 0.45) == pytest.approx(32400.0)
    assert mh812_q_locale(72000.0, 0) == 0.0
    assert mh812_q_locale(72000.0, 1) == pytest.approx(72000.0)
    with pytest.raises(ValueError):
        mh812_q_locale(72000.0, 1.01)
    assert mh812_q_mant(72000.0, 0.45, 0.20) == pytest.approx(7920.0)
    assert mh812_q_mant(72000.0, 0.45, 0) == 0.0
    assert mh812_q_mant(72000.0, 0.45, 1) == pytest.approx(39600.0)
    assert mh812_q_mant(72000.0, 0, 0.20) == pytest.approx(14400.0)
    assert mh812_q_mant(72000.0, 1, 0.20) == 0.0
    with pytest.raises(ValueError):
        mh812_q_mant(72000.0, 0.45, -0.1)
    assert mh812_q_alt_th(32400.0, 7920.0) == pytest.approx(40320.0)
    assert mh812_q_alt_th(0.0, 0.0) == 0.0
    assert mh812_q_alt_th(72000.0, 0.0) == pytest.approx(72000.0)


def test_ore_anno_e_q_acs():
    assert mh812_ore_anno(12, 52) == 624
    assert mh812_ore_anno(12.0, 52.0) == 624
    with pytest.raises(ValueError):
        mh812_ore_anno(0, 52)
    with pytest.raises(ValueError):
        mh812_ore_anno(12.5, 52)
    assert mh812_q_acs(200, 52, 35) == pytest.approx(423.25111111111113)
    assert mh812_q_acs(0, 52, 35) == 0.0
    with pytest.raises(ValueError):
        mh812_q_acs(-1, 52, 35)
    with pytest.raises(ValueError):
        mh812_q_acs(200, 52, 0)
    with pytest.raises(ValueError):
        mh812_q_acs(200, 0, 35)


def test_illuminazione():
    assert mh812_e_ill_base(624, 8) == 4992.0
    assert mh812_e_ill_base(624, 0) == 0.0
    with pytest.raises(ValueError):
        mh812_e_ill_base(624, -1)
    assert mh812_e_ill_alt(4992.0, 0.35) == pytest.approx(1747.2)
    assert mh812_e_ill_alt(4992.0, 0) == 0.0
    assert mh812_e_ill_alt(4992.0, 1) == pytest.approx(4992.0)
    with pytest.raises(ValueError):
        mh812_e_ill_alt(4992.0, 1.01)


def test_gas_pdc_acs_alt_e_totali():
    assert mh812_gas_base(72000.0, 423.25111111111113) == pytest.approx(80470.27901234568)
    assert mh812_gas_base(0, 0) == 0.0
    with pytest.raises(ValueError):
        mh812_gas_base(-1, 423.25)
    assert mh812_e_pdc(40320.0) == pytest.approx(12600.0)
    assert mh812_e_pdc(0.0) == 0.0
    assert mh812_e_acs_alt(423.25111111111113) == pytest.approx(141.08370370370372)
    assert mh812_e_base(4992.0) == 4992.0
    assert mh812_e_alt(12600.0, 141.08370370370372,
                       1747.1999999999998) == pytest.approx(14488.283703703702)


def test_c_base_c_alt_scomposizione():
    assert mh812_c_base(80470.27901234568, 100, 4992.0, 260,
                        1500) == pytest.approx(10844.94790123457)
    assert mh812_c_base(80470.27901234568, 0, 4992.0, 260,
                        1500) == pytest.approx(2797.92)
    assert mh812_c_alt(14488.283703703702, 260,
                       2500) == pytest.approx(6266.953762962963)
    with pytest.raises(ValueError):
        mh812_c_base(80470.28, 100, 4992.0, 260, -1)
    with pytest.raises(ValueError):
        mh812_c_alt(14488.28, 260, -1)


def test_risparmio_segno():
    assert mh812_risparmio(10844.94790123457, 6266.953762962963) == pytest.approx(4577.994138271606)
    assert mh812_risparmio(6266.95, 6266.95) == pytest.approx(0.0, abs=1e-9)


def test_co2_base_alt_evitata():
    assert mh812_co2_base(80470.27901234568, 4992.0) == pytest.approx(17.841255802469135)
    assert mh812_co2_alt(14488.283703703702) == pytest.approx(5.070899296296296)
    assert mh812_co2_evitata(80470.27901234568, 4992.0,
                             14488.283703703702) == pytest.approx(12.77035650617284)
    assert mh812_co2_base(0, 0) == 0.0
    assert mh812_co2_alt(0) == 0.0
    with pytest.raises(ValueError):
        mh812_co2_base(80470.28, -1)
    with pytest.raises(ValueError):
        mh812_co2_alt(-1)


def test_breakeven_demo_e_varianti():
    assert mh812_demo_calcoli()["breakeven_gas_eur_mwh"] == pytest.approx(43.109503353787886)
    assert mh812_breakeven_gas(6266.953762962963,
                               1500, 4992.0, 260,
                               80470.27901234568) == pytest.approx(43.109503353787886)
    bc = _variante(om_alt=10000)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(136.31161588591118)
    assert _variante(superficie_m2=0)["breakeven_gas_eur_mwh"] == pytest.approx(410.46646330258386)
    assert mh812_breakeven_gas(6266.953762962963,
                               1500, 4992.0, 260,
                               0) is None
    assert mh812_breakeven_gas(1000, 1500, 4992.0, 260,
                               80470.27901234568) is None
    with pytest.raises(ValueError):
        mh812_breakeven_gas(6266.95, 1500, 4992.0, 260, -1)


def test_breakeven_verifica_pareggio():
    be = mh812_demo_calcoli()["breakeven_gas_eur_mwh"]
    assert be == pytest.approx(43.109503353787886)
    bc = _variante(p_gas=be)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert mh812_demo_calcoli()["gas_base_kwh_anno"] > 0.0


def test_breakeven_soglia_minima():
    bc_alto = _variante(p_gas=44.109503353787886)
    bc_basso = _variante(p_gas=42.0)
    assert bc_alto["c_alt_eur_anno"] < bc_alto["c_base_eur_anno"]
    assert bc_basso["c_alt_eur_anno"] > bc_basso["c_base_eur_anno"]
    assert bc_alto["risparmio_eur_anno"] > 0.0
    assert bc_alto["verdetto"] == "NON_CONVIENTE"
    assert bc_basso["verdetto"] == "NON_CALCOLABILE"


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh812_flussi(30000, 4577.994138271606, 15)
    assert len(fl) == 16
    assert fl[0] == -30000
    assert all(f == 4577.994138271606 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh812_demo_calcoli()
    assert bc["van"] == pytest.approx(17518.013656054503)
    assert mh812_van([-30000] + [4577.994138271606] * 15,
                     0) == pytest.approx(38669.91207407409)
    assert mh812_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh812_demo_calcoli()
    assert bc["tir"] == pytest.approx(12.731367600619304)
    assert mh812_tir([-30000] + [4577.994138271606] * 15) == \
        pytest.approx(0.12731367600619304)
    tir = mh812_tir([-30000] + [4577.994138271606] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-30000] + [4577.994138271606] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh812_payback([-30000] + [4577.994138271606] * 15) == 7
    assert mh812_payback([-30000] + [-1000.0] * 15) is None
    assert mh812_payback([0] + [4577.994138271606] * 15) == 0
    assert mh812_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh812_verdetto(4577.994138271606, 17518.013656054503, 30000,
                          10.0) == "CONVIENTE"
    assert mh812_verdetto(4577.994138271606, -1500.0, 30000,
                          10.0) == "MARGINALE"
    assert mh812_verdetto(4577.994138271606, -3000.0, 30000, 10.0) == "MARGINALE"
    assert mh812_verdetto(4577.994138271606, -3000.01, 30000, 10.0) == "NON_CONVIENTE"
    assert mh812_verdetto(4577.994138271606, 0.0, 30000, 10.0) == "MARGINALE"
    assert mh812_verdetto(0.0, 17518.01, 30000,
                          10.0) == "NON_CALCOLABILE"
    assert mh812_verdetto(-3469.033762962963, -66007.38, 30000,
                          10.0) == "NON_CALCOLABILE"
    assert mh812_verdetto(None, 17518.01, 30000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh812_verdetto(float("nan"), 17518.01, 30000, 10.0)
    with pytest.raises(ValueError):
        mh812_verdetto(4577.994138271606, 17518.01, -1, 10.0)
    with pytest.raises(ValueError):
        mh812_verdetto(4577.994138271606, 17518.01, 30000, 100.1)


def test_valida_demo_ok():
    v = mh812_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("superficie_m2", "600"),
                       ("superficie_m2", float("nan")),
                       ("superficie_m2", float("inf")),
                       ("superficie_m2", True),
                       ("p_gas", None),
                       ("q_risc_per_m2", "120")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh812_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("superficie_m2", -10),
                          ("q_risc_per_m2", -10),
                          ("quota_panche", -0.1),
                          ("quota_panche", 1.01),
                          ("f_mantenimento", -0.1),
                          ("f_mantenimento", 1.01),
                          ("ore_settimana", 0),
                          ("ore_settimana", 2.5),
                          ("settimane_anno", 0),
                          ("settimane_anno", 2.5),
                          ("litri_settimana", -1),
                          ("delta_t", 0),
                          ("delta_t", -5),
                          ("p_ill_base_kw", -1),
                          ("f_led", -0.1),
                          ("f_led", 1.01),
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
        assert mh812_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"superficie_m2": 0,
              "q_risc_per_m2": 0,
              "quota_panche": 0,
              "f_mantenimento": 0,
              "litri_settimana": 0,
              "p_ill_base_kw": 0,
              "f_led": 0,
              "p_gas": 0,
              "p_el": 0,
              "om_base": 0, "om_alt": 0,
              "capex": 0, "wacc_pct": 0,
              "tolleranza_pct": 0})
    assert mh812_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["quota_panche"] = 1
    d["f_mantenimento"] = 1
    d["f_led"] = 1
    assert mh812_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh812_demo()
    assert d["superficie_m2"] == 600
    assert d["q_risc_per_m2"] == 120
    assert d["quota_panche"] == 0.45
    assert d["f_mantenimento"] == 0.20
    assert d["ore_settimana"] == 12
    assert d["settimane_anno"] == 52
    assert d["litri_settimana"] == 200
    assert d["delta_t"] == 35
    assert d["p_ill_base_kw"] == 8
    assert d["f_led"] == 0.35
    assert d["p_gas"] == 100
    assert d["p_el"] == 260
    assert d["om_base"] == 1500
    assert d["om_alt"] == 2500
    assert d["capex"] == 30000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    bc = mh812_demo_calcoli()
    for chiave, atteso in _DEMO.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert got == pytest.approx(atteso, rel=1e-9), chiave
    assert bc["payback"] == 7
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True
    assert demo_calcoli()["van"] == bc["van"]


def test_demo_calcoli_fisica_economia():
    bc = mh812_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(10844.94790123457)
    assert bc["c_alt_eur_anno"] == pytest.approx(6266.953762962963)
    assert bc["risparmio_eur_anno"] == pytest.approx(4577.994138271606)
    assert bc["co2_base_t_anno"] == pytest.approx(17.841255802469135)
    assert bc["co2_alt_t_anno"] == pytest.approx(5.070899296296296)
    assert bc["co2_evitata_t_anno"] == pytest.approx(12.77035650617284)
    assert bc["q_risc_kwh_anno"] == pytest.approx(72000.0)
    assert bc["q_locale_kwh_anno"] == pytest.approx(32400.0)
    assert bc["q_mant_kwh_anno"] == pytest.approx(7920.0)
    assert bc["q_alt_th_kwh_anno"] == pytest.approx(40320.0)


def test_demo_flussi_e_cumulato():
    bc = mh812_demo_calcoli()
    assert bc["flussi"][0] == -30000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(4577.994138271606) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -30000
    assert righe.iloc[6]["Cumulato (EUR)"] == pytest.approx(-2532.0351703703636)
    assert righe.iloc[7]["Cumulato (EUR)"] == pytest.approx(2045.9589679012424)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(38669.91207407409)


def test_demo_tabella_righe():
    bc = mh812_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Riscaldamento (kWh_th/anno)"] == pytest.approx(72000.0)
    assert mappa["Zona occupata panche (kWh_th/anno)"] == pytest.approx(32400.0)
    assert mappa["Mantenimento resto volume (kWh_th/anno)"] == pytest.approx(7920.0)
    assert mappa["Fabbisogno termico alternativo (kWh_th/anno)"] == pytest.approx(40320.0)
    assert mappa["Ore di uso all'anno"] == pytest.approx(624)
    assert mappa["ACS (kWh_th/anno)"] == pytest.approx(423.25111111111113)
    assert mappa["Illuminazione base (kWh_e/anno)"] == pytest.approx(4992.0)
    assert mappa["Illuminazione LED (kWh_e/anno)"] == pytest.approx(1747.2)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(80470.27901234568)
    assert mappa["Elettricita' totale base (kWh_e/anno)"] == pytest.approx(4992.0)
    assert mappa["Elettricita' totale alternativa (kWh_e/anno)"] == pytest.approx(14488.283703703702)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(10844.94790123457)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(6266.953762962963)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(4577.994138271606)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(12.77035650617284)
    assert mappa["Payback (anni)"] == 7
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] == pytest.approx(43.109503353787886)


def test_demo_coerenza_interna():
    bc = mh812_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["q_risc_kwh_anno"] == pytest.approx(
        bc["superficie_m2"] * bc["q_risc_per_m2"])
    assert bc["q_locale_kwh_anno"] == pytest.approx(
        bc["q_risc_kwh_anno"] * bc["quota_panche"])
    assert bc["q_mant_kwh_anno"] == pytest.approx(
        bc["q_risc_kwh_anno"] * (1.0 - bc["quota_panche"])
        * bc["f_mantenimento"])
    assert bc["q_alt_th_kwh_anno"] == pytest.approx(
        bc["q_locale_kwh_anno"] + bc["q_mant_kwh_anno"])
    assert bc["ore_anno"] == pytest.approx(
        bc["ore_settimana"] * bc["settimane_anno"])
    assert bc["q_acs_kwh_anno"] == pytest.approx(
        bc["litri_settimana"] * bc["settimane_anno"] * 4.186
        * bc["delta_t"] / 3600.0)
    assert bc["e_ill_base_kwh_anno"] == pytest.approx(
        bc["ore_anno"] * bc["p_ill_base_kw"])
    assert bc["e_ill_alt_kwh_anno"] == pytest.approx(
        bc["e_ill_base_kwh_anno"] * bc["f_led"])
    assert bc["gas_base_kwh_anno"] == pytest.approx(
        (bc["q_risc_kwh_anno"] + bc["q_acs_kwh_anno"]) / 0.90)
    assert bc["e_pdc_kwh_anno"] == pytest.approx(
        bc["q_alt_th_kwh_anno"] / 3.2)
    assert bc["e_acs_alt_kwh_anno"] == pytest.approx(
        bc["q_acs_kwh_anno"] / 3.0)
    assert bc["e_base_kwh_anno"] == pytest.approx(
        bc["e_ill_base_kwh_anno"])
    assert bc["e_alt_kwh_anno"] == pytest.approx(
        bc["e_pdc_kwh_anno"] + bc["e_acs_alt_kwh_anno"]
        + bc["e_ill_alt_kwh_anno"])
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
    sup, qri = 600, 120
    quo, fma = 0.45, 0.20
    ore, sett = 12, 52
    lit, dta = 200, 35
    pil, fle = 8, 0.35
    pg, pel = 100, 260
    omb, oma, cx = 1500, 2500, 30000
    wacc, vita = 5.0, 15
    qrisc = sup * qri
    qloc = qrisc * quo
    qman = qrisc * (1.0 - quo) * fma
    qalt = qloc + qman
    oann = ore * sett
    qacs = lit * sett * 4.186 * dta / 3600.0
    eib = oann * pil
    eia = eib * fle
    gasb = (qrisc + qacs) / 0.90
    epdc = qalt / 3.2
    eacs = qacs / 3.0
    eb = eib
    ea = epdc + eacs + eia
    cb = gasb / 1000.0 * pg + eb / 1000.0 * pel + omb
    ca = ea / 1000.0 * pel + oma
    risp = cb - ca
    co2b = (gasb * 0.20 + eb * 0.35) / 1000.0
    co2a = ea * 0.35 / 1000.0
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    be = ((ca - omb - eb / 1000.0 * pel) * 1000.0 / gasb)
    bc = mh812_demo_calcoli()
    assert bc["q_risc_kwh_anno"] == pytest.approx(qrisc)
    assert bc["q_locale_kwh_anno"] == pytest.approx(qloc)
    assert bc["q_mant_kwh_anno"] == pytest.approx(qman)
    assert bc["q_alt_th_kwh_anno"] == pytest.approx(qalt)
    assert bc["ore_anno"] == pytest.approx(oann)
    assert bc["q_acs_kwh_anno"] == pytest.approx(qacs)
    assert bc["e_ill_base_kwh_anno"] == pytest.approx(eib)
    assert bc["e_ill_alt_kwh_anno"] == pytest.approx(eia)
    assert bc["gas_base_kwh_anno"] == pytest.approx(gasb)
    assert bc["e_pdc_kwh_anno"] == pytest.approx(epdc)
    assert bc["e_acs_alt_kwh_anno"] == pytest.approx(eacs)
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
    bc = mh812_demo_calcoli()
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] > 0.0
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["tir"] is not None and bc["tir"] > bc["wacc_pct"]
    assert bc["payback"] == 7


# ---------------------------------------------------------------- varianti
def test_variante_solo_mantenimento():
    # Quota 0 = solo mantenimento: il calore
    # alternativo e' minimo, il caso migliora.
    bc = _variante(quota_panche=0)
    assert bc["q_locale_kwh_anno"] == 0.0
    assert bc["q_mant_kwh_anno"] == pytest.approx(14400.0)
    assert bc["q_alt_th_kwh_anno"] == pytest.approx(14400.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(6683.994138271606)
    assert bc["van"] == pytest.approx(39377.57348446283)
    assert bc["tir"] == pytest.approx(21.0037386376228)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(16.93835015476767)
    assert bc["payback"] == 5
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_senza_localizzazione_non_convinte():
    # Quota 1 = tutto a comfort: localizzare e'
    # decisivo, senza di essa il caso non regge.
    bc = _variante(quota_panche=1)
    assert bc["q_locale_kwh_anno"] == pytest.approx(72000.0)
    assert bc["q_mant_kwh_anno"] == 0.0
    assert bc["q_alt_th_kwh_anno"] == pytest.approx(72000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(2003.994138271606)
    assert bc["van"] == pytest.approx(-9199.22613422234)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(75.0964683748126)
    assert bc["payback"] == 15
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_mantenimento_estremi():
    # Fattore 0: solo zona panche, caso migliore.
    bc0 = _variante(f_mantenimento=0)
    assert bc0["q_mant_kwh_anno"] == 0.0
    assert bc0["q_alt_th_kwh_anno"] == pytest.approx(32400.0)
    assert bc0["risparmio_eur_anno"] == pytest.approx(5221.494138271606)
    assert bc0["van"] == pytest.approx(24197.323603623707)
    assert bc0["breakeven_gas_eur_mwh"] == pytest.approx(35.11276209853171)
    assert bc0["payback"] == 6
    assert bc0["verdetto"] == "CONVIENTE"
    # Fattore 1: tutto il resto a comfort, coincide
    # con quota 1 (stesso fabbisogno alternativo).
    bc1 = _variante(f_mantenimento=1)
    assert bc1["q_alt_th_kwh_anno"] == pytest.approx(72000.0)
    assert bc1["risparmio_eur_anno"] == pytest.approx(2003.994138271606)
    assert bc1["van"] == pytest.approx(-9199.22613422234)
    assert bc1["verdetto"] == "NON_CONVIENTE"


def test_variante_risparmio_nonpositivo_non_calcolabile():
    # Prezzo gas zero e O&M alt alto: risparmio
    # negativo negli helper (calcolabile, non
    # solleva), verdetto NON_CALCOLABILE; stessa
    # guard della UI.
    for kw in ({"p_gas": 0}, {"om_alt": 10000}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] <= 0.0
        assert bc["verdetto"] == "NON_CALCOLABILE"
        assert bc["flussi"]
    bc = _variante(p_gas=0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-3469.033762962963)
    assert bc["van"] == pytest.approx(-66007.38418245838)
    assert bc["payback"] is None
    bc2 = _variante(om_alt=10000)
    assert bc2["risparmio_eur_anno"] == pytest.approx(-2922.005861728394)
    assert bc2["breakeven_gas_eur_mwh"] == pytest.approx(136.31161588591118)


def test_variante_prezzo_el_zero_helper_convinte():
    # Negli helper p_el = 0 e' ammesso e resta
    # CONVIENTE; in UI e' guard degenere:
    # divergenza documentata.
    bc = _variante(p_el=0)
    assert bc["risparmio_eur_anno"] == pytest.approx(7047.027901234567)
    assert bc["van"] == pytest.approx(43145.739800332274)
    assert bc["payback"] == 5
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_superficie_zero_helper_non_calcolabile():
    # Negli helper S = 0 resta calcolabile ma il
    # risparmio e' negativo (l'ACS resta, ma non
    # basta): verdetto NON_CALCOLABILE con
    # breakeven 410,47; in UI e' guard degenere
    # (S <= 0): qui NON c'e' divergenza di
    # verdetto, solo guard prima.
    bc = _variante(superficie_m2=0)
    assert bc["q_risc_kwh_anno"] == 0.0
    assert bc["q_alt_th_kwh_anno"] == 0.0
    assert bc["gas_base_kwh_anno"] == pytest.approx(470.279012345679)
    assert bc["risparmio_eur_anno"] == pytest.approx(-146.00586172839485)
    assert bc["van"] == pytest.approx(-31515.490916310617)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(410.46646330258386)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_capex_conviente_e_zero():
    bc = _variante(capex=60000)
    assert bc["risparmio_eur_anno"] == pytest.approx(4577.994138271606)
    assert bc["van"] == pytest.approx(-12481.9863439455)
    assert bc["payback"] == 14
    assert bc["verdetto"] == "NON_CONVIENTE"
    bc0 = _variante(capex=0)
    assert bc0["flussi"][0] == 0
    assert bc0["payback"] == 0
    assert bc0["tir"] is None
    assert bc0["van"] == pytest.approx(47518.0136560545, rel=1e-6)
    assert bc0["verdetto"] == "CONVIENTE"


def test_variante_capex_marginale():
    # CAPEX 50.000: VAN negativa entro il 10 %
    # del CAPEX (5.000 EUR), quindi MARGINALE.
    bc = _variante(capex=50000)
    assert bc["van"] == pytest.approx(-2481.9863439455003)
    assert bc["verdetto"] == "MARGINALE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(38669.91207407409)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(5350.05724309518)
    assert bc2["payback"] == 7
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_el_alto_resta_convinte():
    # Elettricita' cara NON uccide questo caso
    # (la base elettrica e' piccola: solo
    # illuminazione): risparmio e VAN restano
    # positivi, diversamente dalla scheda
    # precedente.
    bc = _variante(p_el=400)
    assert bc["risparmio_eur_anno"] == pytest.approx(3248.514419753088)
    assert bc["van"] == pytest.approx(3718.4688091356948)
    assert bc["tir"] == pytest.approx(6.781439354170228)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(59.630879131726346)
    assert bc["payback"] == 10
    assert bc["verdetto"] == "CONVIENTE"


def test_monotonia_prezzo_gas_crescente():
    base = mh812_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas=101)["risparmio_eur_anno"]
    basso = _variante(p_gas=99)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(80.47027901234568, abs=1e-2)
    assert base - basso == pytest.approx(80.47027901234568, abs=1e-2)


def test_monotonia_quota_crescente_risparmio_cala():
    assert _variante(quota_panche=0.20)["risparmio_eur_anno"] > \
        mh812_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(quota_panche=0.70)["risparmio_eur_anno"] < \
        mh812_demo_calcoli()["risparmio_eur_anno"]


def test_demo_deterministica_due_chiamate():
    a = mh812_demo_calcoli()
    b = mh812_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh812_demo().keys()) == {
        "superficie_m2", "q_risc_per_m2",
        "quota_panche", "f_mantenimento",
        "ore_settimana", "settimane_anno",
        "litri_settimana", "delta_t",
        "p_ill_base_kw", "f_led",
        "p_gas", "p_el",
        "om_base", "om_alt",
        "capex", "wacc_pct", "vita_anni",
        "tolleranza_pct"}


# ---------------------------------------------------------------- degenere
def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"superficie_m2": -10},
               {"q_risc_per_m2": -10},
               {"quota_panche": -0.1}, {"quota_panche": 1.01},
               {"f_mantenimento": -0.1}, {"f_mantenimento": 1.01},
               {"ore_settimana": 0}, {"ore_settimana": 2.5},
               {"settimane_anno": 0}, {"settimane_anno": 2.5},
               {"litri_settimana": -1},
               {"delta_t": 0}, {"delta_t": -5},
               {"p_ill_base_kw": -1},
               {"f_led": -0.1}, {"f_led": 1.01},
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
        assert mh812_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"superficie_m2": "600"},
               {"superficie_m2": float("nan")},
               {"p_gas": float("inf")},
               {"capex": True},
               {"q_risc_per_m2": "120"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh812_valida(**d)["valido"] is False


def test_degenere_superficie_zero_e_gas_zero():
    # Superficie 0: calcolabile negli helper ma
    # risparmio negativo, quindi NON_CALCOLABILE
    # (non solleva); gas 0: stessa guard.
    for kw in ({"superficie_m2": 0}, {"p_gas": 0}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] <= 0.0
        assert bc["verdetto"] == "NON_CALCOLABILE"


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
    be = mh812_demo_calcoli()["breakeven_gas_eur_mwh"]
    bc = _variante(p_gas=be)
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["verdetto"] != "CONVIENTE"
    bc2 = _variante(p_gas=be + 1)
    assert bc2["risparmio_eur_anno"] == pytest.approx(80.47027901234568, abs=1e-2)
    # Risparmio positivo ma piccolo: VAN negativa oltre
    # la tolleranza, quindi NON_CONVIENTE (non CONVIENTE).
    assert bc2["verdetto"] == "NON_CONVIENTE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh812_demo_calcoli()
    testo = mh812_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_gas_eur_mwh" in testo
    assert "co2_evitata_t_anno" in testo
    assert "q_locale_kwh_anno" in testo
    assert "q_mant_kwh_anno" in testo
    assert "q_alt_th_kwh_anno" in testo
    assert "e_ill_alt_kwh_anno" in testo
    assert "e_pdc_kwh_anno" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh812_demo_calcoli()
    testo = mh812_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"q_locale_kwh_anno;{bc['q_locale_kwh_anno']}" in testo
    assert f"gas_base_kwh_anno;{bc['gas_base_kwh_anno']}" in testo
    assert f"q_risc_kwh_anno;{bc['q_risc_kwh_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh812_demo_calcoli()
    testo = mh812_csv(bc, _demo_kwargs())
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
    return ["mh" + "81" + "1", "st" + "81" + "1",
            "tab" + "81" + "1", "w" + "81" + "2",
            "mh" + "81" + "0", "tab" + "81" + "0"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w813_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w813_ui.py"))
    ast.parse(src)
    assert src.startswith("# W813")
    assert "with tab812:" in src


def test_ui_apre_scheda_attesa_una_volta():
    """Il frammento UI apre la scheda attesa, una sola volta."""
    src = _leggi("w813_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert m.group(1) == "812"
    assert src.count("with tab812:") == 1


def test_ui_titolo_atteso():
    src = _leggi("w813_ui.py")
    titolo = ("Chiesa / luogo di culto: riscaldamento "
              "localizzato a panche + pompa di calore "
              "batte caldaia a gas ad aria + "
              "illuminazione tradizionale?")
    assert src.count(titolo) == 2


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w813_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w813_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st812_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) == 28
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w813_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 4
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_ui_guard_degenere_stretta():
    """La guard UI della scheda dichiara NON_CALCOLABILE
    anche per superficie <= 0, carico <= 0, litri <= 0,
    potenza <= 0, prezzi <= 0 e CAPEX <= 0
    (piu' stretta degli helper, che ammettono lo
    zero)."""
    src = _leggi("w813_ui.py")
    assert "float(_sup812) <= 0.0" in src
    assert "float(_qri812) <= 0.0" in src
    assert "float(_quo812) < 0.0" in src
    assert "float(_quo812) > 1.0" in src
    assert "float(_fma812) < 0.0" in src
    assert "int(_ore812) <= 0" in src
    assert "int(_set812) <= 0" in src
    assert "float(_lit812) <= 0.0" in src
    assert "float(_pil812) <= 0.0" in src
    assert "float(_pg812) <= 0.0" in src
    assert "float(_pel812) <= 0.0" in src
    assert "float(_cx812) <= 0.0" in src
    assert "int(_vita812) <= 0" in src
    assert "Verdetto: NON_CALCOLABILE" in src


def test_ui_chiamata_calcola_keyword_uguali_firma():
    """La chiamata UI a calcola usa come keyword
    esattamente i parametri della firma helper."""
    src = textwrap.dedent(_leggi("w813_ui.py"))
    albero = ast.parse(src)
    chiamate = []
    for nodo in ast.walk(albero):
        if isinstance(nodo, ast.Call):
            func = nodo.func
            if isinstance(func, ast.Name) and func.id == "mh812_calcola":
                chiamate.append({kw.arg for kw in nodo.keywords})
    assert len(chiamate) == 1
    attesi = set(inspect.signature(mh812_calcola).parameters.keys())
    assert chiamate[0] == attesi


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w813_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def812[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w813_ui.py")
        usate = set(re.findall(r'_def812\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 18
        assert usate <= set(mh812_demo().keys())
