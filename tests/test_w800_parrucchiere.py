"""Test nuova scheda "Parrucchiere: pompa di
calore + recupero calore dalle acque di
lavaggio batte caldaia a gas + chiller?"
(titolo completo nel frammento UI).
Contenuto pronto da scrivere in repo come test
della scheda parrucchiere.

Business case deterministico di un parrucchiere
guidato dalla SUPERFICIE del salone in m2 per
riscaldamento E raffrescamento, piu' i lavaggi
di capelli al giorno, i giorni di apertura
all'anno e i litri per lavaggio per l'ACS dei
lavaggi. Riscaldamento del salone Q_risc = S x
q_risc kWh_th/anno (q_risc kWh_th/m2/anno);
raffrescamento stesso salone Q_raff = S x
q_raff kWh_c/anno (stessa superficie: il salone
e' lo stesso); ACS dei lavaggi Q_acs = lavaggi
al giorno x giorni all'anno x litri per
lavaggio x 4.186 x 23 / 3600 kWh_th/anno (acqua
da 15 a 38 gradi, delta 23 K, 4.186 kJ/kgK,
1 L = 1 kg); calore recuperato dalle acque
reflue Q_rec = Q_acs x f_rec kWh_th/anno;
riscaldamento netto Q_risc_net = max(0, Q_risc -
Q_rec); gas baseline G_base = (Q_risc + Q_acs) /
eta_caldaia kWh/anno (senza recupero: la
baseline non recupera); elettricita' chiller
E_chiller = Q_raff / COP_chiller kWh_e/anno;
elettricita' pompa di calore in riscaldamento
E_pdc_risc = Q_risc_net / COP_pdc_risc
kWh_e/anno (solo il netto, dopo il recupero);
per ACS E_pdc_acs = Q_acs / COP_pdc_acs
kWh_e/anno; in raffrescamento E_pdc_raff =
Q_raff / COP_pdc_raff kWh_e/anno;
C_base = E_chiller / 1000 x p_el + G_base /
1000 x p_gas + O&M_base EUR/anno; C_alt =
(E_pdc_risc + E_pdc_acs + E_pdc_raff) / 1000 x
p_el + O&M_alt EUR/anno (prezzi EUR/MWh, energie
kWh: / 1000 esatto); risparmio = C_base - C_alt;
CO2_base = G_base / 1000 x f_gas + E_chiller /
1000 x f_el t/anno; CO2_alt = (E_pdc_risc +
E_pdc_acs + E_pdc_raff) / 1000 x f_el t/anno;
CO2_evitata = CO2_base - CO2_alt; flussi
[-CAPEX, risparmio x vita]; VAN, TIR, payback
(primo anno con cumulato >= 0); breakeven gas
p_gas_be = (C_alt - E_chiller / 1000 x p_el -
O&M_base) x 1000 / G_base EUR/MWh, None se
G_base <= 0 o numeratore < 0, SOGLIA MINIMA
quando esiste.
Verdetto: NON_CALCOLABILE se risparmio <= 0
(guard degenere: UI salta KPI, grafico, tabella
e CSV); altrimenti CONVIENTE se VAN > 0,
MARGINALE se VAN negativa entro tolleranza %
del CAPEX, NON_CONVIENTE se VAN negativa oltre
la tolleranza. Distinzione esplicita: distinto
dalla palestra (docce utenti, recupero dalle
acque delle docce), dall'albergo
(pernottamento, ACS docce ospiti),
dall'autolavaggio (veicoli lavati, acque di
lavaggio dei veicoli), dalla lavanderia
industriale (kg di biancheria, acqua di
processo per la biancheria, nessuna superficie
di salone e nessun lavaggio di capelli), dal
ristorante (coperti, ACS di cucina, celle
frigo) e dalla farmacia (superficie di vendita
piu' frigoriferi farmaceutici, recupero dai
frigoriferi, nessuna ACS dei lavaggi): qui
driver SUPERFICIE + LAVAGGI = m2 del salone
per riscaldamento E raffrescamento piu'
lavaggi al giorno, giorni all'anno e litri per
lavaggio per l'ACS e il recupero dalle acque
reflue di lavaggio; niente docce, niente
veicoli, niente biancheria, niente coperti,
niente frigoriferi farmaceutici.

Demo (parrucchiere): 120 m2 di superficie del
salone a 110 kWh_th/m2/anno di riscaldamento e
70 kWh_c/m2/anno di raffrescamento, 40 lavaggi
di capelli al giorno per 300 giorni all'anno,
12 litri per lavaggio, f_rec 0,35, caldaia
0,90, chiller COP 3,0, pompa di calore COP
riscaldamento 3,4, COP ACS 3,0 e COP
raffrescamento 3,8, gas 90, el 250 EUR/MWh,
O&M base 2.500, alt 1.500, CAPEX 15.000, WACC
5 %, vita 15, f_gas 0,20, f_el 0,35,
tolleranza 10 % del CAPEX. Valori calcolati
eseguendo mh800_demo_calcoli(): Q_risc 13.200,
Q_raff 8.400, Q_acs 3.851,12, Q_rec
1.347,892, Q_risc_net 11.852,108, G_base
18.945,688888888886, E_chiller 2.800,
E_pdc_risc 3.485,914117647059, E_pdc_acs
1.283,7066666666667, E_pdc_raff
2.210,5263157894738, C_base 4.905,112, C_alt
3.245,0367750257997, risparmio
1.660,0752249741995, CO2_base
4,769137777777777, CO2_alt 2,4430514850361194,
CO2_evitata 2,3260862927416577, VAN
2.231,0131528879024, TIR 7,126238770920787 %,
payback 10, breakeven gas 2,3771516195545925,
verdetto CONVIENTE. NOTA: il primo
suggerimento con O&M alternativo 3.500
EUR/anno dava risparmio -339,92477502580005
(NON_CALCOLABILE); la demo adotta O&M
alternativo 1.500 EUR/anno (un solo impianto
integrato contro caldaia + chiller separati).
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w801_helpers import (
    demo_calcoli,
    mh800_breakeven_gas,
    mh800_c_alt,
    mh800_c_base,
    mh800_calcola,
    mh800_co2_alt,
    mh800_co2_base,
    mh800_co2_evitata,
    mh800_cop,
    mh800_csv,
    mh800_demo,
    mh800_demo_calcoli,
    mh800_e_chiller,
    mh800_e_pdc_acs,
    mh800_e_pdc_raff,
    mh800_e_pdc_risc,
    mh800_eta,
    mh800_flussi,
    mh800_frazione,
    mh800_gas,
    mh800_int_pos,
    mh800_num,
    mh800_nneg,
    mh800_payback,
    mh800_pct_tolleranza,
    mh800_pct_wacc,
    mh800_pos,
    mh800_q_acs,
    mh800_q_raff,
    mh800_q_rec,
    mh800_q_risc,
    mh800_q_risc_net,
    mh800_risparmio,
    mh800_tir,
    mh800_valida,
    mh800_van,
    mh800_verdetto,
)

_DEMO = {
    "q_risc_kwh_anno": 13200.0,
    "q_raff_kwh_anno": 8400.0,
    "q_acs_kwh_anno": 3851.12,
    "q_rec_kwh_anno": 1347.8919999999998,
    "q_risc_net_kwh_anno": 11852.108,
    "gas_base_kwh_anno": 18945.688888888886,
    "e_chiller_kwh_anno": 2800.0,
    "e_pdc_risc_kwh_anno": 3485.914117647059,
    "e_pdc_acs_kwh_anno": 1283.7066666666667,
    "e_pdc_raff_kwh_anno": 2210.5263157894738,
    "c_base_eur_anno": 4905.111999999999,
    "c_alt_eur_anno": 3245.0367750257997,
    "risparmio_eur_anno": 1660.0752249741995,
    "co2_base_t_anno": 4.769137777777777,
    "co2_alt_t_anno": 2.4430514850361194,
    "co2_evitata_t_anno": 2.3260862927416577,
    "van": 2231.0131528879024,
    "tir": 7.126238770920787,
    "breakeven_gas_eur_mwh": 2.3771516195545925,
}


def _demo_kwargs():
    return dict(mh800_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh800_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh800_num(3, "x") == 3.0
    assert mh800_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh800_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh800_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh800_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh800_pos(0, "x")
    with pytest.raises(ValueError):
        mh800_pos(-1, "x")
    assert mh800_pos(0.5, "x") == 0.5


def test_cop_maggiore_di_uno():
    assert mh800_cop(3.4, "x") == 3.4
    assert mh800_cop(1.01, "x") == 1.01
    with pytest.raises(ValueError):
        mh800_cop(1.0, "x")
    with pytest.raises(ValueError):
        mh800_cop(0.5, "x")
    with pytest.raises(ValueError):
        mh800_cop(0, "x")


def test_frazione_limiti():
    assert mh800_frazione(0, "x") == 0.0
    assert mh800_frazione(1, "x") == 1.0
    assert mh800_frazione(0.35, "x") == 0.35
    with pytest.raises(ValueError):
        mh800_frazione(-0.01, "x")
    with pytest.raises(ValueError):
        mh800_frazione(1.01, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh800_int_pos(5.0, "x") == 5
    assert mh800_int_pos(300.0, "x") == 300
    with pytest.raises(ValueError):
        mh800_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh800_int_pos(0, "x")


def test_eta_limiti():
    assert mh800_eta(1.0, "x") == 1.0
    assert mh800_eta(0.9, "x") == 0.9
    with pytest.raises(ValueError):
        mh800_eta(0, "x")
    with pytest.raises(ValueError):
        mh800_eta(1.01, "x")


def test_pct_wacc_limiti():
    assert mh800_pct_wacc(0, "x") == 0.0
    assert mh800_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh800_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh800_pct_tolleranza(0, "x") == 0.0
    assert mh800_pct_tolleranza(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh800_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh800_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_q_risc_q_raff_stessa_superficie():
    assert mh800_q_risc(120, 110) == 13200.0
    assert mh800_q_risc(120, 0) == 0.0
    assert mh800_q_raff(120, 70) == 8400.0
    assert mh800_q_raff(120, 0) == 0.0
    assert mh800_q_raff(240, 70) == 16800.0
    with pytest.raises(ValueError):
        mh800_q_risc(0, 110)
    with pytest.raises(ValueError):
        mh800_q_risc(120, -1)
    with pytest.raises(ValueError):
        mh800_q_raff(120, -10)
    with pytest.raises(ValueError):
        mh800_q_raff(0, 70)


def test_q_acs_formula_acqua_15_38():
    assert mh800_q_acs(40, 300, 12) == pytest.approx(3851.12)
    assert mh800_q_acs(0, 300, 12) == 0.0
    assert mh800_q_acs(40, 300, 0) == 0.0
    assert mh800_q_acs(20, 300, 12) == pytest.approx(1925.56)
    assert mh800_q_acs(40, 150, 12) == pytest.approx(1925.56)
    with pytest.raises(ValueError):
        mh800_q_acs(-1, 300, 12)
    with pytest.raises(ValueError):
        mh800_q_acs(40, 0, 12)
    with pytest.raises(ValueError):
        mh800_q_acs(40, 2.5, 12)
    with pytest.raises(ValueError):
        mh800_q_acs(40, 300, -1)


def test_q_rec_e_risc_netto():
    assert mh800_q_rec(3851.12, 0.35) == pytest.approx(1347.892)
    assert mh800_q_rec(3851.12, 0) == 0.0
    assert mh800_q_rec(3851.12, 1.0) == pytest.approx(3851.12)
    with pytest.raises(ValueError):
        mh800_q_rec(3851.12, 1.01)
    with pytest.raises(ValueError):
        mh800_q_rec(3851.12, -0.1)
    assert mh800_q_risc_net(13200.0, 1347.892) == pytest.approx(11852.108)
    assert mh800_q_risc_net(3300.0, 3851.12) == 0.0
    assert mh800_q_risc_net(13200.0, 0.0) == 13200.0
    with pytest.raises(ValueError):
        mh800_q_risc_net(-1, 1347.892)
    with pytest.raises(ValueError):
        mh800_q_risc_net(13200.0, -1)


def test_gas_e_chiller():
    assert mh800_gas(13200, 3851.12, 0.9) == pytest.approx(18945.688888888886)
    assert mh800_gas(0, 0, 0.9) == 0.0
    assert mh800_gas(13200, 0, 0.9) == pytest.approx(14666.666666666666)
    assert mh800_e_chiller(8400, 3.0) == pytest.approx(2800.0)
    assert mh800_e_chiller(0, 3.0) == 0.0
    with pytest.raises(ValueError):
        mh800_gas(13200, 3851.12, 0)
    with pytest.raises(ValueError):
        mh800_gas(13200, 3851.12, 1.01)
    with pytest.raises(ValueError):
        mh800_e_chiller(8400, 1.0)


def test_e_pdc_risc_acs_raff():
    assert mh800_e_pdc_risc(11852.108, 3.4) == pytest.approx(3485.914117647059)
    assert mh800_e_pdc_risc(0, 3.4) == 0.0
    assert mh800_e_pdc_acs(3851.12, 3.0) == pytest.approx(1283.7066666666667)
    assert mh800_e_pdc_acs(0, 3.0) == 0.0
    assert mh800_e_pdc_raff(8400, 3.8) == pytest.approx(2210.5263157894738)
    assert mh800_e_pdc_raff(0, 3.8) == 0.0
    with pytest.raises(ValueError):
        mh800_e_pdc_risc(11852.108, 1.0)
    with pytest.raises(ValueError):
        mh800_e_pdc_acs(3851.12, 1.0)
    with pytest.raises(ValueError):
        mh800_e_pdc_raff(8400, 0.5)


def test_c_base_c_alt_scomposizione():
    assert mh800_c_base(2800.0, 250,
                        18945.688888888886, 90,
                        2500) == pytest.approx(4905.112)
    assert mh800_c_base(2800.0, 250,
                        18945.688888888886, 0,
                        2500) == pytest.approx(3200.0)
    assert mh800_c_alt(3485.914117647059, 1283.7066666666667,
                       2210.5263157894738,
                       250, 1500) == pytest.approx(3245.0367750257997)
    assert mh800_c_alt(0, 0, 0, 250, 1500) == pytest.approx(1500.0)
    with pytest.raises(ValueError):
        mh800_c_base(2800.0, 250,
                     18945.688888888886, -1, 2500)
    with pytest.raises(ValueError):
        mh800_c_alt(3485.914117647059, 1283.7066666666667,
                    2210.5263157894738, 250, -1)


def test_risparmio_segno():
    assert mh800_risparmio(4905.112, 3245.0367750257997) == pytest.approx(1660.0752249741995)
    assert mh800_risparmio(3245.0367750257997, 3245.0367750257997) == 0.0
    assert mh800_risparmio(4905.112, 3245.0367750257997) > 0.0


def test_co2_base_alt_evitata():
    assert mh800_co2_base(18945.688888888886, 0.20, 2800.0,
                          0.35) == pytest.approx(4.769137777777777)
    assert mh800_co2_alt(3485.914117647059, 1283.7066666666667,
                         2210.5263157894738,
                         0.35) == pytest.approx(2.4430514850361194)
    assert mh800_co2_evitata(18945.688888888886, 0.20,
                             2800.0,
                             3485.914117647059, 1283.7066666666667,
                             2210.5263157894738,
                             0.35) == pytest.approx(2.3260862927416577)
    assert mh800_co2_base(0, 0.20, 0, 0.35) == pytest.approx(0.0)
    assert mh800_co2_alt(0, 0, 0, 0.35) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh800_co2_base(18945.688888888886, -0.10, 2800.0, 0.35)
    with pytest.raises(ValueError):
        mh800_co2_alt(3485.914117647059, 1283.7066666666667,
                      2210.5263157894738, -0.10)


def test_breakeven_gas_demo_e_varianti():
    assert mh800_breakeven_gas(3245.0367750257997, 2800.0,
                               250, 2500,
                               18945.688888888886) == \
        pytest.approx(2.3771516195545925)
    assert mh800_breakeven_gas(4000.0, 2800.0,
                               250, 2500,
                               18945.688888888886) == \
        pytest.approx(42.22596521518822)
    assert mh800_breakeven_gas(3245.0367750257997, 2800.0,
                               250, 2500, 0) is None
    assert mh800_breakeven_gas(200, 2800.0, 250, 2500,
                               18945.688888888886) is None
    with pytest.raises(ValueError):
        mh800_breakeven_gas(3245.0367750257997, 2800.0,
                            250, 2500, -1)


def test_breakeven_verifica_pareggio():
    bc = _variante(p_gas_eur_mwh=2.3771516195545925)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] in ("NON_CALCOLABILE", "NON_CONVIENTE")
    arrotondato = _variante(p_gas_eur_mwh=2.38)
    assert arrotondato["risparmio_eur_anno"] > 0.0
    assert arrotondato["risparmio_eur_anno"] == pytest.approx(0.05396, abs=1e-3)
    assert arrotondato["verdetto"] == "NON_CONVIENTE"
    demo = mh800_demo_calcoli()
    assert (demo["c_alt_eur_anno"]
            - demo["e_chiller_kwh_anno"]
            / 1000.0 * demo["p_el_eur_mwh"]
            - demo["om_base_eur_anno"]) * 1000.0 / demo["gas_base_kwh_anno"] == \
        pytest.approx(demo["breakeven_gas_eur_mwh"])


def test_breakeven_soglia_minima():
    be = mh800_demo_calcoli()["breakeven_gas_eur_mwh"]
    assert _variante(p_gas_eur_mwh=be + 1)[
        "c_alt_eur_anno"] < _variante(p_gas_eur_mwh=be + 1)[
        "c_base_eur_anno"]
    assert _variante(p_gas_eur_mwh=be - 1)[
        "c_alt_eur_anno"] > _variante(p_gas_eur_mwh=be - 1)[
        "c_base_eur_anno"]


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh800_flussi(15000, 1660.0752249741995, 15)
    assert len(fl) == 16
    assert fl[0] == -15000
    assert all(f == 1660.0752249741995 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh800_demo_calcoli()
    assert bc["van"] == pytest.approx(2231.0131528879024)
    assert mh800_van([-15000] + [1660.0752249741995] * 15,
                     0) == pytest.approx(9901.128374612996)
    assert mh800_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh800_demo_calcoli()
    assert bc["tir"] == pytest.approx(7.126238770920787)
    assert mh800_tir([-15000] + [1660.0752249741995] * 15) == \
        pytest.approx(0.07126238770920787)
    tir = mh800_tir([-15000] + [1660.0752249741995] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-15000] + [1660.0752249741995] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh800_payback([-15000] + [1660.0752249741995] * 15) == 10
    assert mh800_payback([-15000] + [-1000.0] * 15) is None
    assert mh800_payback([0] + [1660.0752249741995] * 15) == 0
    assert mh800_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh800_verdetto(1660.0752249741995, 2231.0131528879024, 15000,
                          10.0) == "CONVIENTE"
    assert mh800_verdetto(1660.0752249741995, 0.0, 15000, 10.0) == "MARGINALE"
    assert mh800_verdetto(1660.0752249741995, -1500.0, 15000, 10.0) == "MARGINALE"
    assert mh800_verdetto(1660.0752249741995, -1500.01, 15000, 10.0) == "NON_CONVIENTE"
    assert mh800_verdetto(1660.0752249741995, -3668.48, 15000, 10.0) == "NON_CONVIENTE"
    assert mh800_verdetto(0.0, 2231.0131528879024, 15000,
                          10.0) == "NON_CALCOLABILE"
    assert mh800_verdetto(-45.03677502579967, -15467.47, 15000,
                          10.0) == "NON_CALCOLABILE"
    assert mh800_verdetto(None, 2231.0131528879024, 15000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh800_verdetto(float("nan"), 2231.01, 15000, 10.0)
    with pytest.raises(ValueError):
        mh800_verdetto(1660.0752249741995, 2231.01, -1, 10.0)
    with pytest.raises(ValueError):
        mh800_verdetto(1660.0752249741995, 2231.01, 15000, 100.1)


def test_valida_demo_ok():
    v = mh800_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("s_m2", "120"),
                       ("s_m2", float("nan")),
                       ("s_m2", float("inf")),
                       ("s_m2", True),
                       ("p_gas_eur_mwh", None),
                       ("q_risc_kwh_th_m2_anno", "110")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh800_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("s_m2", 0),
                          ("s_m2", -10),
                          ("q_risc_kwh_th_m2_anno", -0.1),
                          ("q_raff_kwh_c_m2_anno", -0.1),
                          ("lavaggi_giorno", -1),
                          ("giorni_anno", 0),
                          ("giorni_anno", 2.5),
                          ("litri_per_lavaggio", -1),
                          ("f_rec", -0.1),
                          ("f_rec", 1.01),
                          ("eta_caldaia", 0),
                          ("eta_caldaia", 1.01),
                          ("cop_chiller", 1.0),
                          ("cop_chiller", 0.5),
                          ("cop_pdc_risc", 1.0),
                          ("cop_pdc_acs", 1.0),
                          ("cop_pdc_raff", 1.0),
                          ("cop_pdc_raff", 0.5),
                          ("p_gas_eur_mwh", -1),
                          ("p_el_eur_mwh", -1),
                          ("om_base_eur_anno", -100),
                          ("om_alt_eur_anno", -100),
                          ("capex_eur", -1),
                          ("wacc_pct", -0.1), ("wacc_pct", 50.1),
                          ("vita_anni", 0), ("vita_anni", 2.5),
                          ("f_gas_t_per_mwh", -0.10),
                          ("f_el_t_per_mwh", -0.10),
                          ("tolleranza_pct", -1),
                          ("tolleranza_pct", 100.1)):
        d = _demo_kwargs()
        d[campo] = valore
        assert mh800_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"q_risc_kwh_th_m2_anno": 0,
              "q_raff_kwh_c_m2_anno": 0,
              "lavaggi_giorno": 0,
              "litri_per_lavaggio": 0,
              "f_rec": 0,
              "p_gas_eur_mwh": 0,
              "p_el_eur_mwh": 0,
              "om_base_eur_anno": 0, "om_alt_eur_anno": 0,
              "capex_eur": 0, "wacc_pct": 0,
              "f_gas_t_per_mwh": 0, "f_el_t_per_mwh": 0,
              "tolleranza_pct": 0})
    assert mh800_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["f_rec"] = 1.0
    d["q_risc_kwh_th_m2_anno"] = 110
    assert mh800_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh800_demo()
    assert d["s_m2"] == 120
    assert d["q_risc_kwh_th_m2_anno"] == 110
    assert d["q_raff_kwh_c_m2_anno"] == 70
    assert d["lavaggi_giorno"] == 40
    assert d["giorni_anno"] == 300
    assert d["litri_per_lavaggio"] == 12
    assert d["f_rec"] == 0.35
    assert d["eta_caldaia"] == 0.90
    assert d["cop_chiller"] == 3.0
    assert d["cop_pdc_risc"] == 3.4
    assert d["cop_pdc_acs"] == 3.0
    assert d["cop_pdc_raff"] == 3.8
    assert d["p_gas_eur_mwh"] == 90
    assert d["p_el_eur_mwh"] == 250
    assert d["om_base_eur_anno"] == 2500
    assert d["om_alt_eur_anno"] == 1500
    assert d["capex_eur"] == 15000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["f_gas_t_per_mwh"] == 0.20
    assert d["f_el_t_per_mwh"] == 0.35
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    bc = mh800_demo_calcoli()
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
    bc = mh800_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(4905.112)
    assert bc["c_alt_eur_anno"] == pytest.approx(3245.0367750257997)
    assert bc["risparmio_eur_anno"] == pytest.approx(1660.0752249741995)
    assert bc["co2_base_t_anno"] == pytest.approx(4.769137777777777)
    assert bc["co2_alt_t_anno"] == pytest.approx(2.4430514850361194)
    assert bc["co2_evitata_t_anno"] == pytest.approx(2.3260862927416577)
    assert bc["gas_base_kwh_anno"] == pytest.approx(18945.688888888886)
    assert bc["q_acs_kwh_anno"] == pytest.approx(3851.12)
    assert bc["q_rec_kwh_anno"] == pytest.approx(1347.892)
    assert bc["q_risc_net_kwh_anno"] == pytest.approx(11852.108)


def test_demo_flussi_e_cumulato():
    bc = mh800_demo_calcoli()
    assert bc["flussi"][0] == -15000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(1660.0752249741995) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -15000
    assert righe.iloc[9]["Cumulato (EUR)"] == pytest.approx(-59.32297523220177)
    assert righe.iloc[10]["Cumulato (EUR)"] == pytest.approx(1600.7522497419977)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(9901.128374612996)


def test_demo_tabella_righe():
    bc = mh800_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Superficie del salone (m2)"] == pytest.approx(120.0)
    assert mappa["Riscaldamento del salone (kWh_th/anno)"] == pytest.approx(13200.0)
    assert mappa["Raffrescamento del salone (kWh_c/anno)"] == pytest.approx(8400.0)
    assert mappa["ACS dei lavaggi di capelli (kWh_th/anno)"] == pytest.approx(3851.12)
    assert mappa["Calore recuperato dalle acque di lavaggio (kWh_th/anno)"] == pytest.approx(1347.892)
    assert mappa["Riscaldamento netto (kWh_th/anno)"] == pytest.approx(11852.108)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(18945.688888888886)
    assert mappa["Elettricita' chiller (kWh_e/anno)"] == pytest.approx(2800.0)
    assert mappa["Elettricita' pompa di calore riscaldamento (kWh_e/anno)"] == pytest.approx(3485.914117647059)
    assert mappa["Elettricita' pompa di calore ACS (kWh_e/anno)"] == pytest.approx(1283.7066666666667)
    assert mappa["Elettricita' pompa di calore raffrescamento (kWh_e/anno)"] == pytest.approx(2210.5263157894738)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(4905.112)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(3245.0367750257997)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(1660.0752249741995)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(2.3260862927416577)
    assert mappa["Payback (anni)"] == 10
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] == \
        pytest.approx(2.3771516195545925)


def test_demo_coerenza_interna():
    bc = mh800_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["q_risc_kwh_anno"] == pytest.approx(
        bc["s_m2"] * bc["q_risc_kwh_th_m2_anno"])
    assert bc["q_raff_kwh_anno"] == pytest.approx(
        bc["s_m2"] * bc["q_raff_kwh_c_m2_anno"])
    assert bc["q_acs_kwh_anno"] == pytest.approx(
        bc["lavaggi_giorno"] * bc["giorni_anno"]
        * bc["litri_per_lavaggio"] * 4.186 * 23.0 / 3600.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(
        bc["q_acs_kwh_anno"] * bc["f_rec"])
    assert bc["q_risc_net_kwh_anno"] == pytest.approx(
        max(0.0, bc["q_risc_kwh_anno"] - bc["q_rec_kwh_anno"]))
    assert bc["gas_base_kwh_anno"] == pytest.approx(
        (bc["q_risc_kwh_anno"] + bc["q_acs_kwh_anno"])
        / bc["eta_caldaia"])
    assert bc["e_chiller_kwh_anno"] == pytest.approx(
        bc["q_raff_kwh_anno"] / bc["cop_chiller"])
    assert bc["e_pdc_risc_kwh_anno"] == pytest.approx(
        bc["q_risc_net_kwh_anno"] / bc["cop_pdc_risc"])
    assert bc["e_pdc_acs_kwh_anno"] == pytest.approx(
        bc["q_acs_kwh_anno"] / bc["cop_pdc_acs"])
    assert bc["e_pdc_raff_kwh_anno"] == pytest.approx(
        bc["q_raff_kwh_anno"] / bc["cop_pdc_raff"])
    assert bc["co2_evitata_t_anno"] == pytest.approx(
        bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])
    assert bc["c_base_eur_anno"] == pytest.approx(
        bc["e_chiller_kwh_anno"] / 1000.0 * bc["p_el_eur_mwh"]
        + bc["gas_base_kwh_anno"] / 1000.0 * bc["p_gas_eur_mwh"]
        + bc["om_base_eur_anno"])
    assert bc["c_alt_eur_anno"] == pytest.approx(
        (bc["e_pdc_risc_kwh_anno"] + bc["e_pdc_acs_kwh_anno"]
         + bc["e_pdc_raff_kwh_anno"])
        / 1000.0 * bc["p_el_eur_mwh"]
        + bc["om_alt_eur_anno"])


def test_demo_contro_riconteggio_indipendente():
    s_sal = 120
    qr_spec, qf_spec = 110, 70
    lav, gg, lit = 40, 300, 12
    frec = 0.35
    eta, copc, copr, copa, copf = 0.90, 3.0, 3.4, 3.0, 3.8
    pg, pel, omb, oma, cx = 90, 250, 2500, 1500, 15000
    fg, fel, wacc, vita = 0.20, 0.35, 5.0, 15
    qrisc = s_sal * qr_spec
    qraff = s_sal * qf_spec
    qacs = lav * gg * lit * 4.186 * 23.0 / 3600.0
    qrec = qacs * frec
    qrnet = max(0.0, qrisc - qrec)
    gas = (qrisc + qacs) / eta
    ech = qraff / copc
    epr = qrnet / copr
    epa = qacs / copa
    epf = qraff / copf
    cb = ech / 1000.0 * pel + gas / 1000.0 * pg + omb
    ca = (epr + epa + epf) / 1000.0 * pel + oma
    risp = cb - ca
    co2b = gas / 1000.0 * fg + ech / 1000.0 * fel
    co2a = (epr + epa + epf) / 1000.0 * fel
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    be = (ca - ech / 1000.0 * pel - omb) * 1000.0 / gas
    bc = mh800_demo_calcoli()
    assert bc["q_risc_kwh_anno"] == pytest.approx(qrisc)
    assert bc["q_raff_kwh_anno"] == pytest.approx(qraff)
    assert bc["q_acs_kwh_anno"] == pytest.approx(qacs)
    assert bc["q_rec_kwh_anno"] == pytest.approx(qrec)
    assert bc["q_risc_net_kwh_anno"] == pytest.approx(qrnet)
    assert bc["gas_base_kwh_anno"] == pytest.approx(gas)
    assert bc["e_chiller_kwh_anno"] == pytest.approx(ech)
    assert bc["e_pdc_risc_kwh_anno"] == pytest.approx(epr)
    assert bc["e_pdc_acs_kwh_anno"] == pytest.approx(epa)
    assert bc["e_pdc_raff_kwh_anno"] == pytest.approx(epf)
    assert bc["c_base_eur_anno"] == pytest.approx(cb)
    assert bc["c_alt_eur_anno"] == pytest.approx(ca)
    assert bc["risparmio_eur_anno"] == pytest.approx(risp)
    assert bc["co2_base_t_anno"] == pytest.approx(co2b)
    assert bc["co2_alt_t_anno"] == pytest.approx(co2a)
    assert bc["co2_evitata_t_anno"] == pytest.approx(co2)
    assert bc["van"] == pytest.approx(van)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(be)


# ---------------------------------------------------------------- varianti
def test_variante_gas_60_non_conviente():
    bc = _variante(p_gas_eur_mwh=60)
    assert bc["risparmio_eur_anno"] == pytest.approx(1091.7045583075337)
    assert bc["van"] == pytest.approx(-3668.480006044817)
    assert bc["tir"] == pytest.approx(1.1173509481505417)
    assert bc["payback"] == 14
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_gas_zero_non_calcolabile():
    bc = _variante(p_gas_eur_mwh=0)
    assert bc["valid"] is True
    assert bc["c_base_eur_anno"] == pytest.approx(3200.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-45.03677502579967)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_senza_recupero_conveniente():
    bc = _variante(f_rec=0)
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["q_risc_net_kwh_anno"] == 13200.0
    assert bc["e_pdc_risc_kwh_anno"] == pytest.approx(3882.3529411764707)
    assert bc["risparmio_eur_anno"] == pytest.approx(1560.9655190918465)
    assert bc["van"] == pytest.approx(1202.2882975644231)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(7.608405360899306)
    assert bc["payback"] == 10
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_recupero_pieno_conveniente_be_none():
    bc = _variante(f_rec=1.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(3851.12)
    assert bc["q_risc_net_kwh_anno"] == pytest.approx(9348.88)
    assert bc["risparmio_eur_anno"] == pytest.approx(1844.1361073271405)
    assert bc["van"] == pytest.approx(4141.5021699172175)
    assert bc["tir"] == pytest.approx(8.847254823028203)
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["payback"] == 9
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_saloncino_satura_marginale():
    bc = _variante(s_m2=30, f_rec=1.0)
    assert bc["q_risc_kwh_anno"] == pytest.approx(3300.0)
    assert bc["q_risc_net_kwh_anno"] == 0.0
    assert bc["e_pdc_risc_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(1431.0274385964913)
    assert bc["van"] == pytest.approx(-146.42454411495112)
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"


def test_variante_senza_lavaggi_conveniente_be_none():
    bc = _variante(lavaggi_giorno=0)
    assert bc["q_acs_kwh_anno"] == 0.0
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["q_risc_net_kwh_anno"] == 13200.0
    assert bc["risparmio_eur_anno"] == pytest.approx(1496.7801857585137)
    assert bc["van"] == pytest.approx(536.0664864977939)
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_alto_marginale_e_non_conviente():
    bc = _variante(capex_eur=18000)
    assert bc["risparmio_eur_anno"] == pytest.approx(1660.0752249741995)
    assert bc["van"] == pytest.approx(-768.9868471120999)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"
    bc2 = _variante(capex_eur=20000)
    assert bc2["van"] == pytest.approx(-2768.986847112098)
    assert bc2["payback"] == 13
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex_eur=0)
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(17231.013152887903, rel=1e-6)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(9901.128374612996)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(-2181.33915024239)
    assert bc2["payback"] == 10
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_el_alto_non_conviente_e_cop_risc_basso():
    bc = _variante(p_el_eur_mwh=400)
    assert bc["risparmio_eur_anno"] == pytest.approx(1033.0531599587193)
    assert bc["van"] == pytest.approx(-4277.261464366621)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(35.47291650267853)
    assert bc["payback"] == 15
    assert bc["verdetto"] == "NON_CONVIENTE"
    bc2 = _variante(cop_pdc_risc=2.8)
    assert bc2["e_pdc_risc_kwh_anno"] == pytest.approx(4232.895714285714)
    assert bc2["risparmio_eur_anno"] == pytest.approx(1473.3298258145355)
    assert bc2["van"] == pytest.approx(292.659769407054)
    assert bc2["breakeven_gas_eur_mwh"] == pytest.approx(12.234032530820105)
    assert bc2["payback"] == 11
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_senza_riscaldamento_e_senza_lavaggi_be_none():
    bc = _variante(q_risc_kwh_th_m2_anno=0, lavaggi_giorno=0)
    assert bc["q_risc_kwh_anno"] == 0.0
    assert bc["q_acs_kwh_anno"] == 0.0
    assert bc["gas_base_kwh_anno"] == 0.0
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["risparmio_eur_anno"] == pytest.approx(1147.3684210526317)
    assert bc["van"] == pytest.approx(-3090.708145666478)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_om_alt_3500_non_calcolabile():
    bc = _variante(om_alt_eur_anno=3500)
    assert bc["risparmio_eur_anno"] == pytest.approx(-339.92477502580005)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_monotonia_prezzo_gas_crescente():
    base = mh800_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas_eur_mwh=91)["risparmio_eur_anno"]
    basso = _variante(p_gas_eur_mwh=89)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(18.945688888888886)
    assert base - basso == pytest.approx(18.945688888888886)


def test_monotonia_superficie_crescente():
    assert _variante(s_m2=60)["risparmio_eur_anno"] < \
        mh800_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(s_m2=240)["risparmio_eur_anno"] > \
        mh800_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(s_m2=240)["q_risc_kwh_anno"] == \
        pytest.approx(26400.0)


def test_demo_deterministica_due_chiamate():
    a = mh800_demo_calcoli()
    b = mh800_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh800_demo().keys()) == {
        "s_m2",
        "q_risc_kwh_th_m2_anno", "q_raff_kwh_c_m2_anno",
        "lavaggi_giorno", "giorni_anno", "litri_per_lavaggio",
        "f_rec",
        "eta_caldaia", "cop_chiller",
        "cop_pdc_risc", "cop_pdc_acs", "cop_pdc_raff",
        "p_gas_eur_mwh", "p_el_eur_mwh",
        "om_base_eur_anno", "om_alt_eur_anno",
        "capex_eur", "wacc_pct", "vita_anni",
        "f_gas_t_per_mwh", "f_el_t_per_mwh",
        "tolleranza_pct"}


# ---------------------------------------------------------------- degenere
def test_degenere_cop_uguale_uno_sollevela():
    with pytest.raises(ValueError):
        _variante(cop_pdc_risc=1.0)
    with pytest.raises(ValueError):
        _variante(cop_pdc_acs=1.0)
    with pytest.raises(ValueError):
        _variante(cop_pdc_raff=1.0)


def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"s_m2": 0},
               {"s_m2": -10},
               {"q_risc_kwh_th_m2_anno": -0.1},
               {"q_raff_kwh_c_m2_anno": -0.1},
               {"lavaggi_giorno": -1},
               {"giorni_anno": 0},
               {"giorni_anno": 2.5},
               {"litri_per_lavaggio": -1},
               {"f_rec": -0.1},
               {"f_rec": 1.01},
               {"eta_caldaia": 0}, {"eta_caldaia": 1.01},
               {"cop_chiller": 1.0}, {"cop_chiller": 0.5},
               {"cop_pdc_risc": 1.0}, {"cop_pdc_risc": 0.5},
               {"cop_pdc_acs": 1.0}, {"cop_pdc_acs": 0.5},
               {"cop_pdc_raff": 1.0}, {"cop_pdc_raff": 0.5},
               {"p_gas_eur_mwh": -1},
               {"p_el_eur_mwh": -1},
               {"om_base_eur_anno": -100},
               {"om_alt_eur_anno": -100},
               {"capex_eur": -1},
               {"wacc_pct": -1}, {"wacc_pct": 60},
               {"vita_anni": 0}, {"vita_anni": 2.5},
               {"f_gas_t_per_mwh": -0.10},
               {"f_el_t_per_mwh": -0.10},
               {"tolleranza_pct": -1},
               {"tolleranza_pct": 100.1}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh800_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"s_m2": "120"},
               {"s_m2": float("nan")},
               {"p_gas_eur_mwh": float("inf")},
               {"capex_eur": True},
               {"q_risc_kwh_th_m2_anno": "110"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh800_valida(**d)["valido"] is False


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    for kw in ({"p_gas_eur_mwh": 0},
               {"p_gas_eur_mwh": 1.38},
               {"om_alt_eur_anno": 3500}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] <= 0.0
        assert bc["verdetto"] == "NON_CALCOLABILE"
        assert bc["flussi"]


def test_pareggio_esatto_tolleranza_float():
    # A pareggio esatto il risparmio e' zero (qui
    # circa 0.0, quindi guard NON_CALCOLABILE; con
    # +0,05 a 2,38 arrotondato la VAN resta circa
    # -14.999, quindi NON_CONVIENTE): in nessun
    # caso CONVIENTE.
    bc = _variante(p_gas_eur_mwh=2.3771516195545925)
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] in ("NON_CALCOLABILE", "NON_CONVIENTE")
    assert bc["verdetto"] != "CONVIENTE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh800_demo_calcoli()
    testo = mh800_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_gas_eur_mwh" in testo
    assert "co2_evitata_t_anno" in testo
    assert "q_raff_kwh_anno" in testo
    assert "s_m2" in testo
    assert "e_chiller_kwh_anno" in testo
    assert "e_pdc_raff_kwh_anno" in testo
    assert "e_pdc_acs_kwh_anno" in testo
    assert "q_acs_kwh_anno" in testo
    assert "q_rec_kwh_anno" in testo
    assert "q_risc_net_kwh_anno" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh800_demo_calcoli()
    testo = mh800_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"q_risc_kwh_anno;{bc['q_risc_kwh_anno']}" in testo
    assert f"gas_base_kwh_anno;{bc['gas_base_kwh_anno']}" in testo
    assert f"q_acs_kwh_anno;{bc['q_acs_kwh_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh800_demo_calcoli()
    testo = mh800_csv(bc, _demo_kwargs())
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
    return ["mh" + "79" + "9", "st" + "79" + "9",
            "tab" + "79" + "9", "w" + "80" + "0",
            "mh" + "79" + "8", "tab" + "79" + "8"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w801_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w801_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab800:")


def test_registry_chain_tail_and_count():
    """Registry della nuova scheda: il frammento UI apre la
    scheda numero 800 (la coda della catena, in append dopo
    la coda precedente che termina a 799, termina con la
    nuova scheda e il conteggio atteso delle schede e'
    800)."""
    src = _leggi("w801_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 800
    assert src.count("with tab800:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w801_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w801_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st800_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) >= 28
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w801_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 4
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w801_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def800[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w801_ui.py")
        usate = set(re.findall(r'_def800\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 22
        assert usate <= set(mh800_demo().keys())
