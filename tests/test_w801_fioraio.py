"""Test nuova scheda "Fioraio: pompa di
calore + recupero calore dalla cella frigo
fiori batte caldaia a gas + frigo tradizionale?"
(titolo completo nel frammento UI).
Contenuto pronto da scrivere in repo come test
della scheda fioraio.

Business case deterministico di un fioraio
guidato dalla SUPERFICIE del negozio in m2 per
il riscaldamento del negozio, piu' il VOLUME
della cella frigo fiori in m3, il carico
specifico della cella in W/m3 e le ore di
funzionamento all'anno per il carico
frigorifero della cella. Riscaldamento del
negozio Q_risc = S x q_risc kWh_th/anno
(q_risc kWh_th/m2/anno); carico frigorifero
della cella Q_frigo = V x carico_specifico x
ore / 1000 kWh_c/anno (W x h / 1000 = kWh);
elettricita' frigo E_frigo = Q_frigo / COP_frigo
kWh_e/anno (identica in baseline e in
alternativa: il frigo resta lo stesso); calore
del condensatore Q_cond = Q_frigo + E_frigo
kWh_th/anno (carico piu' lavoro del
compressore, primo principio); calore
recuperato Q_rec = min(Q_risc, Q_cond x f_rec)
kWh_th/anno (saturato al riscaldamento);
riscaldamento netto Q_risc_net = max(0, Q_risc -
Q_rec); gas baseline G_base = Q_risc /
eta_caldaia kWh/anno (senza recupero: la
baseline non recupera); elettricita' pompa di
calore in riscaldamento E_pdc_risc =
Q_risc_net / COP_pdc_risc kWh_e/anno (solo il
netto, dopo il recupero);
C_base = G_base / 1000 x p_gas + E_frigo /
1000 x p_el + O&M_base EUR/anno; C_alt =
(E_pdc_risc + E_frigo) / 1000 x p_el + O&M_alt
EUR/anno (prezzi EUR/MWh, energie kWh: / 1000
esatto); risparmio = C_base - C_alt;
CO2_base = G_base / 1000 x f_gas + E_frigo /
1000 x f_el t/anno; CO2_alt = (E_pdc_risc +
E_frigo) / 1000 x f_el t/anno;
CO2_evitata = CO2_base - CO2_alt; flussi
[-CAPEX, risparmio x vita]; VAN, TIR, payback
(primo anno con cumulato >= 0); breakeven gas
p_gas_be = (C_alt - E_frigo / 1000 x p_el -
O&M_base) x 1000 / G_base EUR/MWh, None se
G_base <= 0 o numeratore < 0, SOGLIA MINIMA
quando esiste.
Verdetto: NON_CALCOLABILE se risparmio <= 0
(guard degenere: UI salta KPI, grafico, tabella
e CSV); altrimenti CONVIENTE se VAN > 0,
MARGINALE se VAN negativa entro tolleranza %
del CAPEX, NON_CONVIENTE se VAN negativa oltre
la tolleranza. Distinzione esplicita: distinto
dal parrucchiere (lavaggi di capelli, ACS dei
lavaggi, recupero dalle acque reflue), dal
ristorante (coperti, ACS di cucina, celle frigo
di cucina), dalla farmacia (superficie di
vendita piu' frigoriferi farmaceutici, recupero
dai frigoriferi, nessuna cella fiori),
dall'albergo (pernottamento, ACS docce ospiti),
dalla palestra (docce utenti, recupero dalle
acque delle docce) e dall'autolavaggio (veicoli
lavati, acque di lavaggio dei veicoli): qui
driver SUPERFICIE + CELLA = m2 del negozio
per il riscaldamento piu' volume della cella,
carico specifico e ore per il carico
frigorifero e il recupero dal condensatore;
niente lavaggi, niente coperti, niente docce,
niente veicoli, niente frigoriferi farmaceutici.

Demo (fioraio): 80 m2 di superficie del
negozio a 120 kWh_th/m2/anno di riscaldamento,
cella frigo fiori 12 m3 a carico specifico 60
W/m3 per 8760 ore all'anno, COP frigo 2,5,
f_rec 0,60, caldaia 0,90, pompa di calore COP
riscaldamento 3,4, gas 90, el 250 EUR/MWh,
O&M base 1.500, alt 800, CAPEX 12.000, WACC
5 %, vita 15, f_gas 0,20, f_el 0,35,
tolleranza 10 % del CAPEX. Valori calcolati
eseguendo mh801_demo_calcoli(): Q_risc 9.600,
Q_frigo 6.307,2, E_frigo 2.522,88, Q_cond
8.830,08, Q_rec 5.298,048, Q_risc_net
4.301,952, G_base 10.666,666666666666,
E_pdc_risc 1.265,2800000000002, C_base
3.090,7200000000003, C_alt 1.747,04, risparmio
1.343,6800000000003, CO2_base
3,016341333333333, CO2_alt 1,3258560000000001,
CO2_evitata 1,690485333333333, VAN
1.946,9389127424977, TIR 7,312744117414975 %,
payback 9, breakeven gas None (numeratore
negativo: a prezzo gas zero l'alternativa e'
gia' piu' conveniente), verdetto CONVIENTE.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w802_helpers import (
    demo_calcoli,
    mh801_breakeven_gas,
    mh801_c_alt,
    mh801_c_base,
    mh801_calcola,
    mh801_co2_alt,
    mh801_co2_base,
    mh801_co2_evitata,
    mh801_cop,
    mh801_csv,
    mh801_demo,
    mh801_demo_calcoli,
    mh801_e_frigo,
    mh801_e_pdc_risc,
    mh801_eta,
    mh801_flussi,
    mh801_frazione,
    mh801_gas,
    mh801_int_pos,
    mh801_num,
    mh801_nneg,
    mh801_payback,
    mh801_pct_tolleranza,
    mh801_pct_wacc,
    mh801_pos,
    mh801_q_cond,
    mh801_q_frigo,
    mh801_q_rec,
    mh801_q_risc,
    mh801_q_risc_net,
    mh801_risparmio,
    mh801_tir,
    mh801_valida,
    mh801_van,
    mh801_verdetto,
)

_DEMO = {
    "q_risc_kwh_anno": 9600.0,
    "q_frigo_kwh_anno": 6307.2,
    "e_frigo_kwh_anno": 2522.88,
    "q_cond_kwh_anno": 8830.08,
    "q_rec_kwh_anno": 5298.048,
    "q_risc_net_kwh_anno": 4301.952,
    "gas_base_kwh_anno": 10666.666666666666,
    "e_pdc_risc_kwh_anno": 1265.2800000000002,
    "c_base_eur_anno": 3090.7200000000003,
    "c_alt_eur_anno": 1747.04,
    "risparmio_eur_anno": 1343.6800000000003,
    "co2_base_t_anno": 3.016341333333333,
    "co2_alt_t_anno": 1.3258560000000001,
    "co2_evitata_t_anno": 1.690485333333333,
    "van": 1946.9389127424977,
    "tir": 7.312744117414975,
}


def _demo_kwargs():
    return dict(mh801_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh801_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh801_num(3, "x") == 3.0
    assert mh801_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh801_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh801_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh801_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh801_pos(0, "x")
    with pytest.raises(ValueError):
        mh801_pos(-1, "x")
    assert mh801_pos(0.5, "x") == 0.5


def test_cop_maggiore_di_uno():
    assert mh801_cop(3.4, "x") == 3.4
    assert mh801_cop(1.01, "x") == 1.01
    with pytest.raises(ValueError):
        mh801_cop(1.0, "x")
    with pytest.raises(ValueError):
        mh801_cop(0.5, "x")
    with pytest.raises(ValueError):
        mh801_cop(0, "x")


def test_frazione_limiti():
    assert mh801_frazione(0, "x") == 0.0
    assert mh801_frazione(1, "x") == 1.0
    assert mh801_frazione(0.60, "x") == 0.60
    with pytest.raises(ValueError):
        mh801_frazione(-0.01, "x")
    with pytest.raises(ValueError):
        mh801_frazione(1.01, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh801_int_pos(5.0, "x") == 5
    assert mh801_int_pos(8760.0, "x") == 8760
    with pytest.raises(ValueError):
        mh801_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh801_int_pos(0, "x")


def test_eta_limiti():
    assert mh801_eta(1.0, "x") == 1.0
    assert mh801_eta(0.9, "x") == 0.9
    with pytest.raises(ValueError):
        mh801_eta(0, "x")
    with pytest.raises(ValueError):
        mh801_eta(1.01, "x")


def test_pct_wacc_limiti():
    assert mh801_pct_wacc(0, "x") == 0.0
    assert mh801_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh801_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh801_pct_tolleranza(0, "x") == 0.0
    assert mh801_pct_tolleranza(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh801_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh801_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_q_risc():
    assert mh801_q_risc(80, 120) == 9600.0
    assert mh801_q_risc(80, 0) == 0.0
    assert mh801_q_risc(160, 120) == 19200.0
    with pytest.raises(ValueError):
        mh801_q_risc(0, 120)
    with pytest.raises(ValueError):
        mh801_q_risc(80, -1)


def test_q_frigo_formula_volume_carico_ore():
    assert mh801_q_frigo(12, 60, 8760) == pytest.approx(6307.2)
    assert mh801_q_frigo(0, 60, 8760) == 0.0
    assert mh801_q_frigo(12, 0, 8760) == 0.0
    assert mh801_q_frigo(24, 60, 8760) == pytest.approx(12614.4)
    assert mh801_q_frigo(12, 60, 4380) == pytest.approx(3153.6)
    with pytest.raises(ValueError):
        mh801_q_frigo(-1, 60, 8760)
    with pytest.raises(ValueError):
        mh801_q_frigo(12, -1, 8760)
    with pytest.raises(ValueError):
        mh801_q_frigo(12, 60, 0)
    with pytest.raises(ValueError):
        mh801_q_frigo(12, 60, 2.5)


def test_e_frigo_q_cond():
    assert mh801_e_frigo(6307.2, 2.5) == pytest.approx(2522.88)
    assert mh801_e_frigo(0, 2.5) == 0.0
    assert mh801_q_cond(6307.2, 2522.88) == pytest.approx(8830.08)
    assert mh801_q_cond(0, 0) == 0.0
    with pytest.raises(ValueError):
        mh801_e_frigo(6307.2, 1.0)
    with pytest.raises(ValueError):
        mh801_q_cond(-1, 2522.88)
    with pytest.raises(ValueError):
        mh801_q_cond(6307.2, -1)


def test_q_rec_saturazione_e_risc_netto():
    assert mh801_q_rec(8830.08, 0.60, 9600.0) == pytest.approx(5298.048)
    assert mh801_q_rec(8830.08, 0, 9600.0) == 0.0
    assert mh801_q_rec(8830.08, 1.0, 9600.0) == pytest.approx(8830.08)
    assert mh801_q_rec(8830.08, 0.60, 4800.0) == 4800.0
    assert mh801_q_rec(8830.08, 1.0, 4800.0) == 4800.0
    with pytest.raises(ValueError):
        mh801_q_rec(8830.08, 1.01, 9600.0)
    with pytest.raises(ValueError):
        mh801_q_rec(8830.08, -0.1, 9600.0)
    assert mh801_q_risc_net(9600.0, 5298.048) == pytest.approx(4301.952)
    assert mh801_q_risc_net(4800.0, 4800.0) == 0.0
    assert mh801_q_risc_net(9600.0, 0.0) == 9600.0
    with pytest.raises(ValueError):
        mh801_q_risc_net(-1, 5298.048)
    with pytest.raises(ValueError):
        mh801_q_risc_net(9600.0, -1)


def test_gas_e_pdc_risc():
    assert mh801_gas(9600, 0.9) == pytest.approx(10666.666666666666)
    assert mh801_gas(0, 0.9) == 0.0
    assert mh801_gas(9600, 1.0) == pytest.approx(9600.0)
    assert mh801_e_pdc_risc(4301.952, 3.4) == pytest.approx(1265.2800000000002)
    assert mh801_e_pdc_risc(0, 3.4) == 0.0
    with pytest.raises(ValueError):
        mh801_gas(9600, 0)
    with pytest.raises(ValueError):
        mh801_gas(9600, 1.01)
    with pytest.raises(ValueError):
        mh801_e_pdc_risc(4301.952, 1.0)


def test_c_base_c_alt_scomposizione():
    assert mh801_c_base(2522.88, 250,
                        10666.666666666666, 90,
                        1500) == pytest.approx(3090.72)
    assert mh801_c_base(2522.88, 250,
                        10666.666666666666, 0,
                        1500) == pytest.approx(2130.72)
    assert mh801_c_alt(1265.2800000000002, 2522.88,
                       250, 800) == pytest.approx(1747.04)
    assert mh801_c_alt(0, 2522.88, 250, 800) == pytest.approx(1430.72)
    with pytest.raises(ValueError):
        mh801_c_base(2522.88, 250,
                     10666.666666666666, -1, 1500)
    with pytest.raises(ValueError):
        mh801_c_alt(1265.2800000000002, 2522.88, 250, -1)


def test_risparmio_segno():
    assert mh801_risparmio(3090.72, 1747.04) == pytest.approx(1343.68)
    assert mh801_risparmio(1747.04, 1747.04) == 0.0
    assert mh801_risparmio(3090.72, 1747.04) > 0.0


def test_co2_base_alt_evitata():
    assert mh801_co2_base(10666.666666666666, 0.20, 2522.88,
                          0.35) == pytest.approx(3.016341333333333)
    assert mh801_co2_alt(1265.2800000000002, 2522.88,
                         0.35) == pytest.approx(1.3258560000000001)
    assert mh801_co2_evitata(10666.666666666666, 0.20,
                             2522.88,
                             1265.2800000000002,
                             0.35) == pytest.approx(1.690485333333333)
    assert mh801_co2_base(0, 0.20, 0, 0.35) == pytest.approx(0.0)
    assert mh801_co2_alt(0, 0, 0.35) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh801_co2_base(10666.666666666666, -0.10, 2522.88, 0.35)
    with pytest.raises(ValueError):
        mh801_co2_alt(1265.2800000000002, 2522.88, -0.10)


def test_breakeven_demo_none_e_varianti():
    assert mh801_breakeven_gas(1747.04, 2522.88,
                               250, 1500,
                               10666.666666666666) is None
    assert mh801_breakeven_gas(2747.04, 2522.88,
                               250, 1500,
                               10666.666666666666) == \
        pytest.approx(57.78)
    assert mh801_breakeven_gas(2136.6023529411764, 2522.88,
                               250, 1500,
                               10666.666666666666) == \
        pytest.approx(0.5514705882352828)
    assert mh801_breakeven_gas(1747.04, 2522.88,
                               250, 1500, 0) is None
    with pytest.raises(ValueError):
        mh801_breakeven_gas(1747.04, 2522.88,
                            250, 1500, -1)


def test_breakeven_verifica_pareggio():
    be = _variante(om_alt_eur_anno=1800)["breakeven_gas_eur_mwh"]
    assert be == pytest.approx(57.78)
    bc = _variante(om_alt_eur_anno=1800, p_gas_eur_mwh=be)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    demo = mh801_demo_calcoli()
    assert demo["breakeven_gas_eur_mwh"] is None
    assert (demo["c_alt_eur_anno"]
            - demo["e_frigo_kwh_anno"]
            / 1000.0 * demo["p_el_eur_mwh"]
            - demo["om_base_eur_anno"]) < 0.0


def test_breakeven_soglia_minima():
    bc_alto = _variante(om_alt_eur_anno=1800, p_gas_eur_mwh=58.78)
    bc_basso = _variante(om_alt_eur_anno=1800, p_gas_eur_mwh=56.78)
    assert bc_alto["c_alt_eur_anno"] < bc_alto["c_base_eur_anno"]
    assert bc_basso["c_alt_eur_anno"] > bc_basso["c_base_eur_anno"]


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh801_flussi(12000, 1343.6800000000003, 15)
    assert len(fl) == 16
    assert fl[0] == -12000
    assert all(f == 1343.6800000000003 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh801_demo_calcoli()
    assert bc["van"] == pytest.approx(1946.9389127424977)
    assert mh801_van([-12000] + [1343.6800000000003] * 15,
                     0) == pytest.approx(8155.200000000004)
    assert mh801_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh801_demo_calcoli()
    assert bc["tir"] == pytest.approx(7.312744117414975)
    assert mh801_tir([-12000] + [1343.6800000000003] * 15) == \
        pytest.approx(0.07312744117414975)
    tir = mh801_tir([-12000] + [1343.6800000000003] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-12000] + [1343.6800000000003] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh801_payback([-12000] + [1343.6800000000003] * 15) == 9
    assert mh801_payback([-12000] + [-1000.0] * 15) is None
    assert mh801_payback([0] + [1343.6800000000003] * 15) == 0
    assert mh801_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh801_verdetto(1343.6800000000003, 1946.9389127424977, 12000,
                          10.0) == "CONVIENTE"
    assert mh801_verdetto(1343.6800000000003, 0.0, 12000, 10.0) == "MARGINALE"
    assert mh801_verdetto(1343.6800000000003, -1200.0, 12000, 10.0) == "MARGINALE"
    assert mh801_verdetto(1343.6800000000003, -1200.01, 12000, 10.0) == "NON_CONVIENTE"
    assert mh801_verdetto(1343.6800000000003, -1374.55, 12000, 10.0) == "NON_CONVIENTE"
    assert mh801_verdetto(0.0, 1946.9389127424977, 12000,
                          10.0) == "NON_CALCOLABILE"
    assert mh801_verdetto(-1356.32, -26078.14, 12000,
                          10.0) == "NON_CALCOLABILE"
    assert mh801_verdetto(None, 1946.9389127424977, 12000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh801_verdetto(float("nan"), 1946.94, 12000, 10.0)
    with pytest.raises(ValueError):
        mh801_verdetto(1343.6800000000003, 1946.94, -1, 10.0)
    with pytest.raises(ValueError):
        mh801_verdetto(1343.6800000000003, 1946.94, 12000, 100.1)


def test_valida_demo_ok():
    v = mh801_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("s_m2", "80"),
                       ("s_m2", float("nan")),
                       ("s_m2", float("inf")),
                       ("s_m2", True),
                       ("p_gas_eur_mwh", None),
                       ("q_risc_kwh_th_m2_anno", "120")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh801_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("s_m2", 0),
                          ("s_m2", -10),
                          ("q_risc_kwh_th_m2_anno", -0.1),
                          ("v_cella_m3", -1),
                          ("carico_w_m3", -1),
                          ("ore_anno", 0),
                          ("ore_anno", 2.5),
                          ("cop_frigo", 1.0),
                          ("cop_frigo", 0.5),
                          ("f_rec", -0.1),
                          ("f_rec", 1.01),
                          ("eta_caldaia", 0),
                          ("eta_caldaia", 1.01),
                          ("cop_pdc_risc", 1.0),
                          ("cop_pdc_risc", 0.5),
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
        assert mh801_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"q_risc_kwh_th_m2_anno": 0,
              "v_cella_m3": 0,
              "carico_w_m3": 0,
              "f_rec": 0,
              "p_gas_eur_mwh": 0,
              "p_el_eur_mwh": 0,
              "om_base_eur_anno": 0, "om_alt_eur_anno": 0,
              "capex_eur": 0, "wacc_pct": 0,
              "f_gas_t_per_mwh": 0, "f_el_t_per_mwh": 0,
              "tolleranza_pct": 0})
    assert mh801_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["f_rec"] = 1.0
    d["q_risc_kwh_th_m2_anno"] = 120
    assert mh801_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh801_demo()
    assert d["s_m2"] == 80
    assert d["q_risc_kwh_th_m2_anno"] == 120
    assert d["v_cella_m3"] == 12
    assert d["carico_w_m3"] == 60
    assert d["ore_anno"] == 8760
    assert d["cop_frigo"] == 2.5
    assert d["f_rec"] == 0.60
    assert d["eta_caldaia"] == 0.90
    assert d["cop_pdc_risc"] == 3.4
    assert d["p_gas_eur_mwh"] == 90
    assert d["p_el_eur_mwh"] == 250
    assert d["om_base_eur_anno"] == 1500
    assert d["om_alt_eur_anno"] == 800
    assert d["capex_eur"] == 12000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["f_gas_t_per_mwh"] == 0.20
    assert d["f_el_t_per_mwh"] == 0.35
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    bc = mh801_demo_calcoli()
    for chiave, atteso in _DEMO.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert got == pytest.approx(atteso, rel=1e-9), chiave
    assert bc["payback"] == 9
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True
    assert demo_calcoli()["van"] == bc["van"]


def test_demo_calcoli_fisica_economia():
    bc = mh801_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(3090.72)
    assert bc["c_alt_eur_anno"] == pytest.approx(1747.04)
    assert bc["risparmio_eur_anno"] == pytest.approx(1343.68)
    assert bc["co2_base_t_anno"] == pytest.approx(3.016341333333333)
    assert bc["co2_alt_t_anno"] == pytest.approx(1.3258560000000001)
    assert bc["co2_evitata_t_anno"] == pytest.approx(1.690485333333333)
    assert bc["gas_base_kwh_anno"] == pytest.approx(10666.666666666666)
    assert bc["q_frigo_kwh_anno"] == pytest.approx(6307.2)
    assert bc["q_cond_kwh_anno"] == pytest.approx(8830.08)
    assert bc["q_rec_kwh_anno"] == pytest.approx(5298.048)
    assert bc["q_risc_net_kwh_anno"] == pytest.approx(4301.952)


def test_demo_flussi_e_cumulato():
    bc = mh801_demo_calcoli()
    assert bc["flussi"][0] == -12000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(1343.6800000000003) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -12000
    assert righe.iloc[8]["Cumulato (EUR)"] == pytest.approx(-1250.56)
    assert righe.iloc[9]["Cumulato (EUR)"] == pytest.approx(93.12)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(8155.20)


def test_demo_tabella_righe():
    bc = mh801_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Superficie del negozio (m2)"] == pytest.approx(80.0)
    assert mappa["Riscaldamento del negozio (kWh_th/anno)"] == pytest.approx(9600.0)
    assert mappa["Carico frigorifero della cella (kWh_c/anno)"] == pytest.approx(6307.2)
    assert mappa["Elettricita' frigo (kWh_e/anno)"] == pytest.approx(2522.88)
    assert mappa["Calore del condensatore (kWh_th/anno)"] == pytest.approx(8830.08)
    assert mappa["Calore recuperato dal condensatore (kWh_th/anno)"] == pytest.approx(5298.048)
    assert mappa["Riscaldamento netto (kWh_th/anno)"] == pytest.approx(4301.952)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(10666.666666666666)
    assert mappa["Elettricita' pompa di calore riscaldamento (kWh_e/anno)"] == pytest.approx(1265.2800000000002)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(3090.72)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(1747.04)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(1343.68)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(1.690485333333333)
    assert mappa["Payback (anni)"] == 9
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] is None


def test_demo_coerenza_interna():
    bc = mh801_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["q_risc_kwh_anno"] == pytest.approx(
        bc["s_m2"] * bc["q_risc_kwh_th_m2_anno"])
    assert bc["q_frigo_kwh_anno"] == pytest.approx(
        bc["v_cella_m3"] * bc["carico_w_m3"]
        * bc["ore_anno"] / 1000.0)
    assert bc["e_frigo_kwh_anno"] == pytest.approx(
        bc["q_frigo_kwh_anno"] / bc["cop_frigo"])
    assert bc["q_cond_kwh_anno"] == pytest.approx(
        bc["q_frigo_kwh_anno"] + bc["e_frigo_kwh_anno"])
    assert bc["q_rec_kwh_anno"] == pytest.approx(
        min(bc["q_risc_kwh_anno"],
            bc["q_cond_kwh_anno"] * bc["f_rec"]))
    assert bc["q_risc_net_kwh_anno"] == pytest.approx(
        max(0.0, bc["q_risc_kwh_anno"] - bc["q_rec_kwh_anno"]))
    assert bc["gas_base_kwh_anno"] == pytest.approx(
        bc["q_risc_kwh_anno"] / bc["eta_caldaia"])
    assert bc["e_pdc_risc_kwh_anno"] == pytest.approx(
        bc["q_risc_net_kwh_anno"] / bc["cop_pdc_risc"])
    assert bc["co2_evitata_t_anno"] == pytest.approx(
        bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])
    assert bc["c_base_eur_anno"] == pytest.approx(
        bc["gas_base_kwh_anno"] / 1000.0 * bc["p_gas_eur_mwh"]
        + bc["e_frigo_kwh_anno"] / 1000.0 * bc["p_el_eur_mwh"]
        + bc["om_base_eur_anno"])
    assert bc["c_alt_eur_anno"] == pytest.approx(
        (bc["e_pdc_risc_kwh_anno"] + bc["e_frigo_kwh_anno"])
        / 1000.0 * bc["p_el_eur_mwh"]
        + bc["om_alt_eur_anno"])


def test_demo_contro_riconteggio_indipendente():
    s_neg = 80
    qr_spec = 120
    vol, car, ore = 12, 60, 8760
    copf, frec = 2.5, 0.60
    eta, copr = 0.90, 3.4
    pg, pel, omb, oma, cx = 90, 250, 1500, 800, 12000
    fg, fel, wacc, vita = 0.20, 0.35, 5.0, 15
    qrisc = s_neg * qr_spec
    qfrigo = vol * car * ore / 1000.0
    efr = qfrigo / copf
    qcond = qfrigo + efr
    qrec = min(qrisc, qcond * frec)
    qrnet = max(0.0, qrisc - qrec)
    gas = qrisc / eta
    epr = qrnet / copr
    cb = gas / 1000.0 * pg + efr / 1000.0 * pel + omb
    ca = (epr + efr) / 1000.0 * pel + oma
    risp = cb - ca
    co2b = gas / 1000.0 * fg + efr / 1000.0 * fel
    co2a = (epr + efr) / 1000.0 * fel
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    bc = mh801_demo_calcoli()
    assert bc["q_risc_kwh_anno"] == pytest.approx(qrisc)
    assert bc["q_frigo_kwh_anno"] == pytest.approx(qfrigo)
    assert bc["e_frigo_kwh_anno"] == pytest.approx(efr)
    assert bc["q_cond_kwh_anno"] == pytest.approx(qcond)
    assert bc["q_rec_kwh_anno"] == pytest.approx(qrec)
    assert bc["q_risc_net_kwh_anno"] == pytest.approx(qrnet)
    assert bc["gas_base_kwh_anno"] == pytest.approx(gas)
    assert bc["e_pdc_risc_kwh_anno"] == pytest.approx(epr)
    assert bc["c_base_eur_anno"] == pytest.approx(cb)
    assert bc["c_alt_eur_anno"] == pytest.approx(ca)
    assert bc["risparmio_eur_anno"] == pytest.approx(risp)
    assert bc["co2_base_t_anno"] == pytest.approx(co2b)
    assert bc["co2_alt_t_anno"] == pytest.approx(co2a)
    assert bc["co2_evitata_t_anno"] == pytest.approx(co2)
    assert bc["van"] == pytest.approx(van)
    assert bc["breakeven_gas_eur_mwh"] is None


# ---------------------------------------------------------------- varianti
def test_variante_gas_60_non_conviente():
    bc = _variante(p_gas_eur_mwh=60)
    assert bc["risparmio_eur_anno"] == pytest.approx(1023.68)
    assert bc["van"] == pytest.approx(-1374.5516594752894)
    assert bc["tir"] == pytest.approx(3.252956647100913)
    assert bc["payback"] == 12
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_gas_zero_non_conviente_be_none():
    bc = _variante(p_gas_eur_mwh=0)
    assert bc["valid"] is True
    assert bc["c_base_eur_anno"] == pytest.approx(2130.72)
    assert bc["risparmio_eur_anno"] == pytest.approx(383.68)
    assert bc["van"] == pytest.approx(-8017.532803910868)
    assert bc["payback"] is None
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_senza_recupero_non_conviente_be_piccolo():
    bc = _variante(f_rec=0)
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["q_risc_net_kwh_anno"] == 9600.0
    assert bc["e_pdc_risc_kwh_anno"] == pytest.approx(2823.529411764706)
    assert bc["risparmio_eur_anno"] == pytest.approx(954.1176470588239)
    assert bc["van"] == pytest.approx(-2096.585095335926)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(0.5514705882352828)
    assert bc["payback"] == 13
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_recupero_pieno_conveniente_be_none():
    bc = _variante(f_rec=1.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(8830.08)
    assert bc["q_risc_net_kwh_anno"] == pytest.approx(769.92)
    assert bc["risparmio_eur_anno"] == pytest.approx(1603.3882352941177)
    assert bc["van"] == pytest.approx(4642.62158479478)
    assert bc["tir"] == pytest.approx(10.284462398259787)
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_negozio_piccolo_satura_conveniente():
    bc = _variante(s_m2=40)
    assert bc["q_risc_kwh_anno"] == pytest.approx(4800.0)
    assert bc["q_rec_kwh_anno"] == 4800.0
    assert bc["q_risc_net_kwh_anno"] == 0.0
    assert bc["e_pdc_risc_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(1180.0)
    assert bc["van"] == pytest.approx(247.9964850531005)
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["payback"] == 11
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_senza_cella_non_conviente():
    bc = _variante(carico_w_m3=0)
    assert bc["q_frigo_kwh_anno"] == 0.0
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["q_risc_net_kwh_anno"] == 9600.0
    assert bc["risparmio_eur_anno"] == pytest.approx(954.1176470588234)
    assert bc["van"] == pytest.approx(-2096.585095335933)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(0.5514705882353041)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_capex_alto_marginale_e_non_conviente():
    bc = _variante(capex_eur=15000)
    assert bc["risparmio_eur_anno"] == pytest.approx(1343.68)
    assert bc["van"] == pytest.approx(-1053.061087257502)
    assert bc["payback"] == 12
    assert bc["verdetto"] == "MARGINALE"
    bc2 = _variante(capex_eur=17000)
    assert bc2["van"] == pytest.approx(-3053.0610872575025)
    assert bc2["payback"] == 13
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex_eur=0)
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(13946.938912742497, rel=1e-6)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(8155.200000000004)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(-1624.4592103529521)
    assert bc2["payback"] == 9
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_el_alto_marginale_e_cop_risc_basso():
    bc = _variante(p_el_eur_mwh=400)
    assert bc["risparmio_eur_anno"] == pytest.approx(1153.888)
    assert bc["van"] == pytest.approx(-23.03714563987546)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"
    bc2 = _variante(cop_pdc_risc=2.8)
    assert bc2["e_pdc_risc_kwh_anno"] == pytest.approx(1536.4114285714288)
    assert bc2["risparmio_eur_anno"] == pytest.approx(1275.897142857143)
    assert bc2["van"] == pytest.approx(1243.3760347487953)
    assert bc2["payback"] == 10
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_senza_riscaldamento_be_none():
    bc = _variante(q_risc_kwh_th_m2_anno=0)
    assert bc["q_risc_kwh_anno"] == 0.0
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["gas_base_kwh_anno"] == 0.0
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["risparmio_eur_anno"] == pytest.approx(700.0)
    assert bc["van"] == pytest.approx(-4734.239373273588)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_om_alt_3500_non_calcolabile():
    bc = _variante(om_alt_eur_anno=3500)
    assert bc["risparmio_eur_anno"] == pytest.approx(-1356.32)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_monotonia_prezzo_gas_crescente():
    base = mh801_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas_eur_mwh=91)["risparmio_eur_anno"]
    basso = _variante(p_gas_eur_mwh=89)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(10.666666666666666)
    assert base - basso == pytest.approx(10.666666666666666)


def test_monotonia_superficie_crescente():
    assert _variante(s_m2=40)["risparmio_eur_anno"] < \
        mh801_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(s_m2=160)["risparmio_eur_anno"] > \
        mh801_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(s_m2=160)["q_risc_kwh_anno"] == \
        pytest.approx(19200.0)


def test_demo_deterministica_due_chiamate():
    a = mh801_demo_calcoli()
    b = mh801_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh801_demo().keys()) == {
        "s_m2",
        "q_risc_kwh_th_m2_anno",
        "v_cella_m3", "carico_w_m3", "ore_anno",
        "cop_frigo", "f_rec",
        "eta_caldaia", "cop_pdc_risc",
        "p_gas_eur_mwh", "p_el_eur_mwh",
        "om_base_eur_anno", "om_alt_eur_anno",
        "capex_eur", "wacc_pct", "vita_anni",
        "f_gas_t_per_mwh", "f_el_t_per_mwh",
        "tolleranza_pct"}


# ---------------------------------------------------------------- degenere
def test_degenere_cop_uguale_uno_sollevela():
    with pytest.raises(ValueError):
        _variante(cop_frigo=1.0)
    with pytest.raises(ValueError):
        _variante(cop_pdc_risc=1.0)


def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"s_m2": 0},
               {"s_m2": -10},
               {"q_risc_kwh_th_m2_anno": -0.1},
               {"v_cella_m3": -1},
               {"carico_w_m3": -1},
               {"ore_anno": 0},
               {"ore_anno": 2.5},
               {"cop_frigo": 1.0}, {"cop_frigo": 0.5},
               {"f_rec": -0.1},
               {"f_rec": 1.01},
               {"eta_caldaia": 0}, {"eta_caldaia": 1.01},
               {"cop_pdc_risc": 1.0}, {"cop_pdc_risc": 0.5},
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
        assert mh801_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"s_m2": "80"},
               {"s_m2": float("nan")},
               {"p_gas_eur_mwh": float("inf")},
               {"capex_eur": True},
               {"q_risc_kwh_th_m2_anno": "120"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh801_valida(**d)["valido"] is False


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    for kw in ({"om_alt_eur_anno": 3500},
               {"om_alt_eur_anno": 1800,
                "p_gas_eur_mwh": 57.78}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] <= 0.0
        assert bc["verdetto"] == "NON_CALCOLABILE"
        assert bc["flussi"]


def test_pareggio_esatto_tolleranza_float():
    # A pareggio esatto (O&M alt 1.800, gas 57,78)
    # il risparmio e' zero (circa 0.0, quindi guard
    # NON_CALCOLABILE): in nessun caso CONVIENTE.
    bc = _variante(om_alt_eur_anno=1800,
                   p_gas_eur_mwh=57.78)
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["verdetto"] != "CONVIENTE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh801_demo_calcoli()
    testo = mh801_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_gas_eur_mwh" in testo
    assert "co2_evitata_t_anno" in testo
    assert "q_frigo_kwh_anno" in testo
    assert "s_m2" in testo
    assert "e_frigo_kwh_anno" in testo
    assert "e_pdc_risc_kwh_anno" in testo
    assert "q_cond_kwh_anno" in testo
    assert "q_rec_kwh_anno" in testo
    assert "q_risc_net_kwh_anno" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh801_demo_calcoli()
    testo = mh801_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"q_risc_kwh_anno;{bc['q_risc_kwh_anno']}" in testo
    assert f"gas_base_kwh_anno;{bc['gas_base_kwh_anno']}" in testo
    assert f"q_frigo_kwh_anno;{bc['q_frigo_kwh_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh801_demo_calcoli()
    testo = mh801_csv(bc, _demo_kwargs())
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
    return ["mh" + "80" + "0", "st" + "80" + "0",
            "tab" + "80" + "0", "w" + "80" + "1",
            "mh" + "79" + "9", "tab" + "79" + "9"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w802_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w802_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab801:")


def test_registry_chain_tail_and_count():
    """Registry della nuova scheda: il frammento UI apre la
    scheda numero 801 (la coda della catena, in append dopo
    la coda precedente che termina a 800, termina con la
    nuova scheda e il conteggio atteso delle schede e'
    801)."""
    src = _leggi("w802_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 801
    assert src.count("with tab801:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w802_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w802_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st801_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) >= 28
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w802_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 4
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w802_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def801[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w802_ui.py")
        usate = set(re.findall(r'_def801\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 19
        assert usate <= set(mh801_demo().keys())
