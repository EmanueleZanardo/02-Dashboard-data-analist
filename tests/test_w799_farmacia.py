"""Test nuova scheda "Farmacia: pompa di
calore reversibile + recupero calore dai
frigoriferi farmaceutici batte caldaia a gas
+ chiller?"
(titolo completo nel frammento UI).
Contenuto pronto da scrivere in repo come test
della scheda farmacia.

Business case deterministico di una farmacia
guidata dalla SUPERFICIE di vendita in m2 per
riscaldamento E raffrescamento, piu' la
potenza elettrica assorbita continua dei
frigoriferi farmaceutici in kW (24/7).
Riscaldamento superficie di vendita Q_risc = S x
q_risc kWh_th/anno (q_risc kWh_th/m2/anno);
raffrescamento stessa superficie Q_raff = S x
q_raff kWh_c/anno (stessa superficie: la
superficie di vendita e' la stessa);
elettricita' frigoriferi E_frigo = P_frigo x
8760 kWh_e/anno (identica in baseline e
alternativa: il recupero non cambia il consumo
dei frighi); calore recuperato Q_rec = E_frigo x
f_rec kWh_th/anno; riscaldamento netto
Q_risc_net = max(0, Q_risc - Q_rec); gas baseline
G_base = Q_risc / eta_caldaia kWh/anno (senza
recupero: la baseline non recupera);
elettricita' chiller E_chiller = Q_raff /
COP_chiller kWh_e/anno; elettricita' pompa di
calore in riscaldamento E_pdc_risc = Q_risc_net /
COP_pdc_risc kWh_e/anno (solo il netto, dopo il
recupero); in raffrescamento E_pdc_raff = Q_raff /
COP_pdc_raff kWh_e/anno;
C_base = (E_chiller + E_frigo) / 1000 x p_el +
G_base / 1000 x p_gas + O&M_base EUR/anno; C_alt =
(E_pdc_risc + E_pdc_raff + E_frigo) / 1000 x p_el +
O&M_alt EUR/anno (prezzi EUR/MWh, energie kWh:
 / 1000 esatto); risparmio = C_base - C_alt;
CO2_base = G_base / 1000 x f_gas + (E_chiller +
E_frigo) / 1000 x f_el t/anno; CO2_alt =
(E_pdc_risc + E_pdc_raff + E_frigo) / 1000 x f_el
t/anno; CO2_evitata = CO2_base - CO2_alt; flussi
[-CAPEX, risparmio x vita]; VAN, TIR, payback
(primo anno con cumulato >= 0); breakeven gas
p_gas_be = (C_alt - (E_chiller + E_frigo) / 1000
x p_el - O&M_base) x 1000 / G_base EUR/MWh, None
se G_base <= 0 o numeratore < 0, SOGLIA MINIMA
quando esiste.
Verdetto: NON_CALCOLABILE se risparmio <= 0
(guard degenere: UI salta KPI, grafico, tabella
e CSV); altrimenti CONVIENTE se VAN > 0,
MARGINALE se VAN negativa entro tolleranza %
del CAPEX, NON_CONVIENTE se VAN negativa oltre
la tolleranza. Distinzione esplicita: distinto
dal supermercato (banchi alimentari aperti,
celle frigo alimentari, recupero sul
riscaldamento del punto vendita), dal
ristorante (coperti, ACS, celle frigo, recupero
su ACS), dalla biblioteca (sale lettura,
depositi, recupero dalla ventilazione),
dall'albergo (pernottamento, ACS docce ospiti),
dalla scuola (aule + mensa, chiusure stagionali
scolastiche), dall'ospedale (reparti 24h,
ventilazione di reparto, ACS posti letto), dalla
palestra (docce utenti) e dalla piscina (vasca
riscaldata), dal teatro/cinema (sala spettacolo,
affollamento serale) e dal centro logistico
(magazzino volumetrico in m3, uffici SOLO per
il raffrescamento): qui driver SUPERFICIE +
POTENZA FRIGHI = m2 di superficie di vendita
per riscaldamento E raffrescamento piu' kW
continui dei frigoriferi farmaceutici chiusi
2-8 gradi per il recupero; niente ACS, niente
celle frigo, niente banchi aperti.

Demo (farmacia): 300 m2 di superficie di vendita
a 130 kWh_th/m2/anno di riscaldamento e 80
kWh_c/m2/anno di raffrescamento, frigoriferi
farmaceutici 5 kW continui, f_rec 0,50, caldaia
0,90, chiller COP 3,0, pompa di calore COP
riscaldamento 3,4 e COP raffrescamento 3,8,
gas 90, el 250 EUR/MWh, O&M base 4.000, alt
5.000, CAPEX 18.000, WACC 5 %, vita 15,
f_gas 0,20, f_el 0,35, tolleranza 10 % del
CAPEX. Valori calcolati eseguendo
mh799_demo_calcoli(): Q_risc 39.000, Q_raff
24.000, E_frigo 43.800, Q_rec 21.900, Q_risc_net
17.100, G_base 43.333,333333333336, E_chiller
8.000, E_pdc_risc 5.029,411764705883, E_pdc_raff
6.315,789473684211, C_base 20.850, C_alt
18.786,300309597522, risparmio 2.063,699690402478,
CO2_base 26,796666666666667, CO2_alt
19,30082043343653, CO2_evitata
7,495846233230136, VAN 3.420,4970798768773, TIR
7,6931760513409095 %, payback 9, breakeven gas
42,37616099071204, verdetto CONVIENTE.
"""

import ast
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w800_helpers import (
    demo_calcoli,
    mh799_breakeven_gas,
    mh799_c_alt,
    mh799_c_base,
    mh799_calcola,
    mh799_co2_alt,
    mh799_co2_base,
    mh799_co2_evitata,
    mh799_cop,
    mh799_csv,
    mh799_demo,
    mh799_demo_calcoli,
    mh799_e_chiller,
    mh799_e_frigo,
    mh799_e_pdc_raff,
    mh799_e_pdc_risc,
    mh799_eta,
    mh799_flussi,
    mh799_frazione,
    mh799_gas,
    mh799_int_pos,
    mh799_num,
    mh799_nneg,
    mh799_payback,
    mh799_pct_tolleranza,
    mh799_pct_wacc,
    mh799_pos,
    mh799_q_raff,
    mh799_q_rec,
    mh799_q_risc,
    mh799_q_risc_net,
    mh799_risparmio,
    mh799_tir,
    mh799_valida,
    mh799_van,
    mh799_verdetto,
)

_DEMO = {
    "q_risc_kwh_anno": 39000.0,
    "q_raff_kwh_anno": 24000.0,
    "e_frigo_kwh_anno": 43800.0,
    "q_rec_kwh_anno": 21900.0,
    "q_risc_net_kwh_anno": 17100.0,
    "gas_base_kwh_anno": 43333.333333333336,
    "e_chiller_kwh_anno": 8000.0,
    "e_pdc_risc_kwh_anno": 5029.411764705883,
    "e_pdc_raff_kwh_anno": 6315.789473684211,
    "c_base_eur_anno": 20850.0,
    "c_alt_eur_anno": 18786.300309597522,
    "risparmio_eur_anno": 2063.699690402478,
    "co2_base_t_anno": 26.796666666666667,
    "co2_alt_t_anno": 19.30082043343653,
    "co2_evitata_t_anno": 7.495846233230136,
    "van": 3420.4970798768773,
    "tir": 7.6931760513409095,
    "breakeven_gas_eur_mwh": 42.37616099071204,
}


def _demo_kwargs():
    return dict(mh799_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh799_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh799_num(3, "x") == 3.0
    assert mh799_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh799_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh799_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh799_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh799_pos(0, "x")
    with pytest.raises(ValueError):
        mh799_pos(-1, "x")
    assert mh799_pos(0.5, "x") == 0.5


def test_cop_maggiore_di_uno():
    assert mh799_cop(3.4, "x") == 3.4
    assert mh799_cop(1.01, "x") == 1.01
    with pytest.raises(ValueError):
        mh799_cop(1.0, "x")
    with pytest.raises(ValueError):
        mh799_cop(0.5, "x")
    with pytest.raises(ValueError):
        mh799_cop(0, "x")


def test_frazione_limiti():
    assert mh799_frazione(0, "x") == 0.0
    assert mh799_frazione(1, "x") == 1.0
    assert mh799_frazione(0.5, "x") == 0.5
    with pytest.raises(ValueError):
        mh799_frazione(-0.01, "x")
    with pytest.raises(ValueError):
        mh799_frazione(1.01, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh799_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh799_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh799_int_pos(0, "x")


def test_eta_limiti():
    assert mh799_eta(1.0, "x") == 1.0
    assert mh799_eta(0.9, "x") == 0.9
    with pytest.raises(ValueError):
        mh799_eta(0, "x")
    with pytest.raises(ValueError):
        mh799_eta(1.01, "x")


def test_pct_wacc_limiti():
    assert mh799_pct_wacc(0, "x") == 0.0
    assert mh799_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh799_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh799_pct_tolleranza(0, "x") == 0.0
    assert mh799_pct_tolleranza(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh799_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh799_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_q_risc_q_raff_stessa_superficie():
    assert mh799_q_risc(300, 130) == 39000.0
    assert mh799_q_risc(300, 0) == 0.0
    assert mh799_q_raff(300, 80) == 24000.0
    assert mh799_q_raff(300, 0) == 0.0
    assert mh799_q_raff(600, 80) == 48000.0
    with pytest.raises(ValueError):
        mh799_q_risc(0, 130)
    with pytest.raises(ValueError):
        mh799_q_risc(300, -1)
    with pytest.raises(ValueError):
        mh799_q_raff(300, -10)
    with pytest.raises(ValueError):
        mh799_q_raff(0, 80)


def test_e_frigo_continuo_8760():
    assert mh799_e_frigo(5) == 43800.0
    assert mh799_e_frigo(0) == 0.0
    assert mh799_e_frigo(2.5) == 21900.0
    with pytest.raises(ValueError):
        mh799_e_frigo(-0.5)


def test_q_rec_e_risc_netto():
    assert mh799_q_rec(43800.0, 0.5) == 21900.0
    assert mh799_q_rec(43800.0, 0) == 0.0
    assert mh799_q_rec(43800.0, 1.0) == 43800.0
    with pytest.raises(ValueError):
        mh799_q_rec(43800.0, 1.01)
    with pytest.raises(ValueError):
        mh799_q_rec(43800.0, -0.1)
    assert mh799_q_risc_net(39000.0, 21900.0) == 17100.0
    assert mh799_q_risc_net(19500.0, 21900.0) == 0.0
    assert mh799_q_risc_net(39000.0, 0.0) == 39000.0
    with pytest.raises(ValueError):
        mh799_q_risc_net(-1, 21900.0)
    with pytest.raises(ValueError):
        mh799_q_risc_net(39000.0, -1)


def test_gas_e_chiller():
    assert mh799_gas(39000, 0.9) == pytest.approx(43333.333333333336)
    assert mh799_gas(0, 0.9) == 0.0
    assert mh799_e_chiller(24000, 3.0) == pytest.approx(8000.0)
    assert mh799_e_chiller(0, 3.0) == 0.0
    with pytest.raises(ValueError):
        mh799_gas(39000, 0)
    with pytest.raises(ValueError):
        mh799_gas(39000, 1.01)
    with pytest.raises(ValueError):
        mh799_e_chiller(24000, 1.0)


def test_e_pdc_risc_raff_solo_netto():
    assert mh799_e_pdc_risc(17100, 3.4) == pytest.approx(5029.411764705883)
    assert mh799_e_pdc_risc(0, 3.4) == 0.0
    assert mh799_e_pdc_raff(24000, 3.8) == pytest.approx(6315.789473684211)
    assert mh799_e_pdc_raff(0, 3.8) == 0.0
    with pytest.raises(ValueError):
        mh799_e_pdc_risc(17100, 1.0)
    with pytest.raises(ValueError):
        mh799_e_pdc_raff(24000, 0.5)


def test_c_base_c_alt_scomposizione():
    assert mh799_c_base(8000.0, 43800.0, 250,
                        43333.333333333336, 90,
                        4000) == pytest.approx(20850.0)
    assert mh799_c_base(8000.0, 43800.0, 250,
                        43333.333333333336, 0,
                        4000) == pytest.approx(16950.0)
    assert mh799_c_alt(5029.411764705883, 6315.789473684211, 43800.0,
                       250, 5000) == pytest.approx(18786.300309597522)
    assert mh799_c_alt(0, 0, 43800.0, 250, 5000) == pytest.approx(15950.0)
    with pytest.raises(ValueError):
        mh799_c_base(8000.0, 43800.0, 250,
                     43333.333333333336, -1, 4000)
    with pytest.raises(ValueError):
        mh799_c_alt(5029.411764705883, 6315.789473684211, 43800.0,
                    250, -1)


def test_risparmio_segno():
    assert mh799_risparmio(20850.0, 18786.300309597522) == pytest.approx(2063.699690402478)
    assert mh799_risparmio(18786.300309597522, 18786.300309597522) == 0.0
    assert mh799_risparmio(20000.0, 18786.300309597522) == pytest.approx(1213.699690402478)


def test_co2_base_alt_evitata():
    assert mh799_co2_base(43333.333333333336, 0.20, 8000.0, 43800.0,
                          0.35) == pytest.approx(26.796666666666667)
    assert mh799_co2_alt(5029.411764705883, 6315.789473684211, 43800.0,
                         0.35) == pytest.approx(19.30082043343653)
    assert mh799_co2_evitata(43333.333333333336, 0.20,
                             8000.0, 43800.0,
                             5029.411764705883, 6315.789473684211,
                             0.35) == pytest.approx(7.495846233230136)
    assert mh799_co2_base(0, 0.20, 0, 0, 0.35) == pytest.approx(0.0)
    assert mh799_co2_alt(0, 0, 0, 0.35) == pytest.approx(0.0)
    with pytest.raises(ValueError):
        mh799_co2_base(43333.333333333336, -0.10, 8000.0, 43800.0,
                       0.35)
    with pytest.raises(ValueError):
        mh799_co2_alt(5029.411764705883, 6315.789473684211, 43800.0,
                      -0.10)


def test_breakeven_gas_demo_e_varianti():
    assert mh799_breakeven_gas(18786.300309597522, 8000.0, 43800.0,
                               250, 4000,
                               43333.333333333336) == \
        pytest.approx(42.37616099071204)
    assert mh799_breakeven_gas(20396.594427244583, 8000.0, 43800.0,
                               250, 4000,
                               43333.333333333336) == \
        pytest.approx(79.53679447487495)
    assert mh799_breakeven_gas(19055.733082706768, 8000.0, 43800.0,
                               250, 4000,
                               43333.333333333336) == \
        pytest.approx(48.593840370156165)
    assert mh799_breakeven_gas(18786.300309597522, 8000.0, 43800.0,
                               250, 4000, 0) is None
    assert mh799_breakeven_gas(200, 8000.0, 43800.0,
                               250, 4000,
                               43333.333333333336) is None
    with pytest.raises(ValueError):
        mh799_breakeven_gas(18786.300309597522, 8000.0, 43800.0,
                            250, 4000, -1)


def test_breakeven_verifica_pareggio():
    bc = _variante(p_gas_eur_mwh=42.37616099071204)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] in ("NON_CALCOLABILE", "NON_CONVIENTE")
    arrotondato = _variante(p_gas_eur_mwh=42.38)
    assert arrotondato["risparmio_eur_anno"] == pytest.approx(0.166357069145306)
    assert arrotondato["risparmio_eur_anno"] > 0.0
    assert arrotondato["verdetto"] == "NON_CONVIENTE"
    demo = mh799_demo_calcoli()
    assert (demo["c_alt_eur_anno"]
            - (demo["e_chiller_kwh_anno"] + demo["e_frigo_kwh_anno"])
            / 1000.0 * demo["p_el_eur_mwh"]
            - demo["om_base_eur_anno"]) * 1000.0 / demo["gas_base_kwh_anno"] == \
        pytest.approx(demo["breakeven_gas_eur_mwh"])


def test_breakeven_soglia_minima():
    be = mh799_demo_calcoli()["breakeven_gas_eur_mwh"]
    assert _variante(p_gas_eur_mwh=be + 1)[
        "c_alt_eur_anno"] < _variante(p_gas_eur_mwh=be + 1)[
        "c_base_eur_anno"]
    assert _variante(p_gas_eur_mwh=be - 1)[
        "c_alt_eur_anno"] > _variante(p_gas_eur_mwh=be - 1)[
        "c_base_eur_anno"]


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh799_flussi(18000, 2063.699690402478, 15)
    assert len(fl) == 16
    assert fl[0] == -18000
    assert all(f == 2063.699690402478 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh799_demo_calcoli()
    assert bc["van"] == pytest.approx(3420.4970798768773)
    assert mh799_van([-18000] + [2063.699690402478] * 15,
                     0) == pytest.approx(12955.495356037172)
    assert mh799_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh799_demo_calcoli()
    assert bc["tir"] == pytest.approx(7.6931760513409095)
    assert mh799_tir([-18000] + [2063.699690402478] * 15) == \
        pytest.approx(0.076931760513409095)
    tir = mh799_tir([-18000] + [2063.699690402478] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-18000] + [2063.699690402478] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh799_payback([-18000] + [2063.699690402478] * 15) == 9
    assert mh799_payback([-18000] + [-1000.0] * 15) is None
    assert mh799_payback([0] + [2063.699690402478] * 15) == 0
    assert mh799_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh799_verdetto(2063.699690402478, 3420.4970798768773, 18000,
                          10.0) == "CONVIENTE"
    assert mh799_verdetto(2063.699690402478, 0.0, 18000, 10.0) == "MARGINALE"
    assert mh799_verdetto(2063.699690402478, -1800.0, 18000, 10.0) == "MARGINALE"
    assert mh799_verdetto(2063.699690402478, -1800.01, 18000, 10.0) == "NON_CONVIENTE"
    assert mh799_verdetto(2063.699690402478, -10073.06, 18000, 10.0) == "NON_CONVIENTE"
    assert mh799_verdetto(0.0, 3420.4970798768773, 18000,
                          10.0) == "NON_CALCOLABILE"
    assert mh799_verdetto(-536.3003095975218, -23566.61, 18000,
                          10.0) == "NON_CALCOLABILE"
    assert mh799_verdetto(None, 3420.4970798768773, 18000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh799_verdetto(float("nan"), 3420.49, 18000, 10.0)
    with pytest.raises(ValueError):
        mh799_verdetto(2063.699690402478, 3420.49, -1, 10.0)
    with pytest.raises(ValueError):
        mh799_verdetto(2063.699690402478, 3420.49, 18000, 100.1)


def test_valida_demo_ok():
    v = mh799_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("s_m2", "300"),
                       ("s_m2", float("nan")),
                       ("s_m2", float("inf")),
                       ("s_m2", True),
                       ("p_gas_eur_mwh", None),
                       ("q_risc_kwh_th_m2_anno", "130")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh799_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("s_m2", 0),
                          ("s_m2", -10),
                          ("q_risc_kwh_th_m2_anno", -0.1),
                          ("q_raff_kwh_c_m2_anno", -0.1),
                          ("p_frigo_kw", -0.5),
                          ("f_rec", -0.1),
                          ("f_rec", 1.01),
                          ("eta_caldaia", 0),
                          ("eta_caldaia", 1.01),
                          ("cop_chiller", 1.0),
                          ("cop_chiller", 0.5),
                          ("cop_pdc_risc", 1.0),
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
        assert mh799_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"q_risc_kwh_th_m2_anno": 0,
              "q_raff_kwh_c_m2_anno": 0,
              "p_frigo_kw": 0,
              "f_rec": 0,
              "p_gas_eur_mwh": 0,
              "p_el_eur_mwh": 0,
              "om_base_eur_anno": 0, "om_alt_eur_anno": 0,
              "capex_eur": 0, "wacc_pct": 0,
              "f_gas_t_per_mwh": 0, "f_el_t_per_mwh": 0,
              "tolleranza_pct": 0})
    assert mh799_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["f_rec"] = 1.0
    d["q_risc_kwh_th_m2_anno"] = 130
    assert mh799_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh799_demo()
    assert d["s_m2"] == 300
    assert d["q_risc_kwh_th_m2_anno"] == 130
    assert d["q_raff_kwh_c_m2_anno"] == 80
    assert d["p_frigo_kw"] == 5
    assert d["f_rec"] == 0.50
    assert d["eta_caldaia"] == 0.90
    assert d["cop_chiller"] == 3.0
    assert d["cop_pdc_risc"] == 3.4
    assert d["cop_pdc_raff"] == 3.8
    assert d["p_gas_eur_mwh"] == 90
    assert d["p_el_eur_mwh"] == 250
    assert d["om_base_eur_anno"] == 4000
    assert d["om_alt_eur_anno"] == 5000
    assert d["capex_eur"] == 18000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["f_gas_t_per_mwh"] == 0.20
    assert d["f_el_t_per_mwh"] == 0.35
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    bc = mh799_demo_calcoli()
    for chiave, atteso in _DEMO.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert got == pytest.approx(atteso, rel=1e-9), chiave
    assert bc["payback"] == 9
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True
    assert demo_calcoli()["van"] == bc["van"]


def test_demo_calcoli_fisica_economia():
    bc = mh799_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(20850.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(18786.300309597522)
    assert bc["risparmio_eur_anno"] == pytest.approx(2063.699690402478)
    assert bc["co2_base_t_anno"] == pytest.approx(26.796666666666667)
    assert bc["co2_alt_t_anno"] == pytest.approx(19.30082043343653)
    assert bc["co2_evitata_t_anno"] == pytest.approx(7.495846233230136)
    assert bc["gas_base_kwh_anno"] == pytest.approx(43333.333333333336)
    assert bc["e_frigo_kwh_anno"] == pytest.approx(43800.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(21900.0)
    assert bc["q_risc_net_kwh_anno"] == pytest.approx(17100.0)


def test_demo_flussi_e_cumulato():
    bc = mh799_demo_calcoli()
    assert bc["flussi"][0] == -18000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(2063.699690402478) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -18000
    assert righe.iloc[8]["Cumulato (EUR)"] == pytest.approx(-1490.4024767801748)
    assert righe.iloc[9]["Cumulato (EUR)"] == pytest.approx(573.2972136223034)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(12955.495356037172)


def test_demo_tabella_righe():
    bc = mh799_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Superficie di vendita (m2)"] == pytest.approx(300.0)
    assert mappa["Riscaldamento superficie di vendita (kWh_th/anno)"] == pytest.approx(39000.0)
    assert mappa["Raffrescamento superficie di vendita (kWh_c/anno)"] == pytest.approx(24000.0)
    assert mappa["Elettricita' frigoriferi farmaceutici (kWh_e/anno)"] == pytest.approx(43800.0)
    assert mappa["Calore recuperato dai frigoriferi (kWh_th/anno)"] == pytest.approx(21900.0)
    assert mappa["Riscaldamento netto (kWh_th/anno)"] == pytest.approx(17100.0)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(43333.333333333336)
    assert mappa["Elettricita' chiller (kWh_e/anno)"] == pytest.approx(8000.0)
    assert mappa["Elettricita' pompa di calore riscaldamento (kWh_e/anno)"] == pytest.approx(5029.411764705883)
    assert mappa["Elettricita' pompa di calore raffrescamento (kWh_e/anno)"] == pytest.approx(6315.789473684211)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(20850.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(18786.300309597522)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(2063.699690402478)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(7.495846233230136)
    assert mappa["Payback (anni)"] == 9
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] == \
        pytest.approx(42.37616099071204)


def test_demo_coerenza_interna():
    bc = mh799_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["q_risc_kwh_anno"] == pytest.approx(
        bc["s_m2"] * bc["q_risc_kwh_th_m2_anno"])
    assert bc["q_raff_kwh_anno"] == pytest.approx(
        bc["s_m2"] * bc["q_raff_kwh_c_m2_anno"])
    assert bc["e_frigo_kwh_anno"] == pytest.approx(
        bc["p_frigo_kw"] * 8760.0)
    assert bc["q_rec_kwh_anno"] == pytest.approx(
        bc["e_frigo_kwh_anno"] * bc["f_rec"])
    assert bc["q_risc_net_kwh_anno"] == pytest.approx(
        max(0.0, bc["q_risc_kwh_anno"] - bc["q_rec_kwh_anno"]))
    assert bc["gas_base_kwh_anno"] == pytest.approx(
        bc["q_risc_kwh_anno"] / bc["eta_caldaia"])
    assert bc["e_chiller_kwh_anno"] == pytest.approx(
        bc["q_raff_kwh_anno"] / bc["cop_chiller"])
    assert bc["e_pdc_risc_kwh_anno"] == pytest.approx(
        bc["q_risc_net_kwh_anno"] / bc["cop_pdc_risc"])
    assert bc["e_pdc_raff_kwh_anno"] == pytest.approx(
        bc["q_raff_kwh_anno"] / bc["cop_pdc_raff"])
    assert bc["co2_evitata_t_anno"] == pytest.approx(
        bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])
    assert bc["c_base_eur_anno"] == pytest.approx(
        (bc["e_chiller_kwh_anno"] + bc["e_frigo_kwh_anno"])
        / 1000.0 * bc["p_el_eur_mwh"]
        + bc["gas_base_kwh_anno"] / 1000.0 * bc["p_gas_eur_mwh"]
        + bc["om_base_eur_anno"])
    assert bc["c_alt_eur_anno"] == pytest.approx(
        (bc["e_pdc_risc_kwh_anno"] + bc["e_pdc_raff_kwh_anno"]
         + bc["e_frigo_kwh_anno"])
        / 1000.0 * bc["p_el_eur_mwh"]
        + bc["om_alt_eur_anno"])


def test_demo_contro_riconteggio_indipendente():
    s_vend = 300
    qr_spec, qf_spec = 130, 80
    pfr, frec = 5, 0.50
    eta, copc, copr, copf = 0.90, 3.0, 3.4, 3.8
    pg, pel, omb, oma, cx = 90, 250, 4000, 5000, 18000
    fg, fel, wacc, vita = 0.20, 0.35, 5.0, 15
    qrisc = s_vend * qr_spec
    qraff = s_vend * qf_spec
    efr = pfr * 8760.0
    qrec = efr * frec
    qrnet = max(0.0, qrisc - qrec)
    gas = qrisc / eta
    ech = qraff / copc
    epr = qrnet / copr
    epf = qraff / copf
    cb = (ech + efr) / 1000.0 * pel + gas / 1000.0 * pg + omb
    ca = (epr + epf + efr) / 1000.0 * pel + oma
    risp = cb - ca
    co2b = gas / 1000.0 * fg + (ech + efr) / 1000.0 * fel
    co2a = (epr + epf + efr) / 1000.0 * fel
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    be = (ca - (ech + efr) / 1000.0 * pel - omb) * 1000.0 / gas
    bc = mh799_demo_calcoli()
    assert bc["q_risc_kwh_anno"] == pytest.approx(qrisc)
    assert bc["q_raff_kwh_anno"] == pytest.approx(qraff)
    assert bc["e_frigo_kwh_anno"] == pytest.approx(efr)
    assert bc["q_rec_kwh_anno"] == pytest.approx(qrec)
    assert bc["q_risc_net_kwh_anno"] == pytest.approx(qrnet)
    assert bc["gas_base_kwh_anno"] == pytest.approx(gas)
    assert bc["e_chiller_kwh_anno"] == pytest.approx(ech)
    assert bc["e_pdc_risc_kwh_anno"] == pytest.approx(epr)
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
    assert bc["risparmio_eur_anno"] == pytest.approx(763.6996904024782)
    assert bc["van"] == pytest.approx(-10073.05836975789)
    assert bc["tir"] == pytest.approx(-5.181239137544084)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_gas_30_non_calcolabile():
    bc = _variante(p_gas_eur_mwh=30)
    assert bc["risparmio_eur_anno"] == pytest.approx(-536.3003095975218)
    assert bc["van"] == pytest.approx(-23566.61381939266)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_gas_zero_non_calcolabile():
    bc = _variante(p_gas_eur_mwh=0)
    assert bc["valid"] is True
    assert bc["c_base_eur_anno"] == pytest.approx(16950.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(-1836.3003095975218)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_variante_senza_recupero_non_conviente():
    bc = _variante(f_rec=0)
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["q_risc_net_kwh_anno"] == 39000.0
    assert bc["e_pdc_risc_kwh_anno"] == pytest.approx(11470.588235294117)
    assert bc["risparmio_eur_anno"] == pytest.approx(453.4055727554187)
    assert bc["van"] == pytest.approx(-13293.805202193345)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(79.53679447487495)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_frighi_spenti_uguale_senza_recupero():
    bc = _variante(p_frigo_kw=0)
    assert bc["e_frigo_kwh_anno"] == 0.0
    assert bc["q_rec_kwh_anno"] == 0.0
    assert bc["q_risc_net_kwh_anno"] == 39000.0
    assert bc["risparmio_eur_anno"] == pytest.approx(453.4055727554187)
    assert bc["van"] == pytest.approx(-13293.805202193345)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_recupero_pieno_conveniente():
    bc = _variante(f_rec=1.0)
    assert bc["q_rec_kwh_anno"] == 43800.0
    assert bc["q_risc_net_kwh_anno"] == 0.0
    assert bc["e_pdc_risc_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(3321.0526315789466)
    assert bc["van"] == pytest.approx(16471.390642589216)
    assert bc["tir"] == pytest.approx(16.609558625981148)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(13.360323886639693)
    assert bc["payback"] == 6
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_alto_marginale_e_non_conviente():
    bc = _variante(capex_eur=22000)
    assert bc["risparmio_eur_anno"] == pytest.approx(2063.699690402478)
    assert bc["van"] == pytest.approx(-579.5029201231234)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"
    bc2 = _variante(capex_eur=26000)
    assert bc2["van"] == pytest.approx(-4579.5029201231255)
    assert bc2["payback"] == 13
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex_eur=0)
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(21420.49707987688, rel=1e-6)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(12955.495356037172)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(-2064.6580172713057)
    assert bc2["payback"] == 9
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_el_alto_marginale_e_cop_risc_basso():
    bc = _variante(p_el_eur_mwh=400)
    assert bc["risparmio_eur_anno"] == pytest.approx(1561.9195046439636)
    assert bc["van"] == pytest.approx(-1787.8096586312404)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(53.95570373898545)
    assert bc["payback"] == 12
    assert bc["verdetto"] == "MARGINALE"
    bc2 = _variante(cop_pdc_risc=2.8)
    assert bc2["e_pdc_risc_kwh_anno"] == pytest.approx(6107.142857142858)
    assert bc2["risparmio_eur_anno"] == pytest.approx(1794.2669172932328)
    assert bc2["van"] == pytest.approx(623.877030724214)
    assert bc2["breakeven_gas_eur_mwh"] == pytest.approx(48.593840370156165)
    assert bc2["payback"] == 11
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_superficie_piccola_satura_e_grande():
    bc = _variante(s_m2=150)
    assert bc["q_risc_kwh_anno"] == pytest.approx(19500.0)
    assert bc["q_risc_net_kwh_anno"] == 0.0
    assert bc["e_pdc_risc_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(1160.5263157894733)
    assert bc["van"] == pytest.approx(-5954.133697795684)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(36.43724696356277)
    assert bc["payback"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"
    bc2 = _variante(s_m2=600)
    assert bc2["q_risc_kwh_anno"] == pytest.approx(78000.0)
    assert bc2["q_risc_net_kwh_anno"] == pytest.approx(56100.0)
    assert bc2["e_pdc_risc_kwh_anno"] == pytest.approx(16500.0)
    assert bc2["risparmio_eur_anno"] == pytest.approx(3517.105263157893)
    assert bc2["van"] == pytest.approx(18506.349915864084)
    assert bc2["tir"] == pytest.approx(17.883190275433485)
    assert bc2["payback"] == 6
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_senza_riscaldamento_be_none():
    bc = _variante(q_risc_kwh_th_m2_anno=0)
    assert bc["q_risc_kwh_anno"] == 0.0
    assert bc["gas_base_kwh_anno"] == 0.0
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["risparmio_eur_anno"] == pytest.approx(-578.9473684210534)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_monotonia_prezzo_gas_crescente():
    base = mh799_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas_eur_mwh=91)["risparmio_eur_anno"]
    basso = _variante(p_gas_eur_mwh=89)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(43.333333333333336)
    assert base - basso == pytest.approx(43.333333333333336)


def test_monotonia_superficie_crescente():
    assert _variante(s_m2=150)["risparmio_eur_anno"] < \
        mh799_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(s_m2=600)["risparmio_eur_anno"] > \
        mh799_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(s_m2=600)["q_risc_kwh_anno"] == \
        pytest.approx(78000.0)


def test_demo_deterministica_due_chiamate():
    a = mh799_demo_calcoli()
    b = mh799_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh799_demo().keys()) == {
        "s_m2",
        "q_risc_kwh_th_m2_anno", "q_raff_kwh_c_m2_anno",
        "p_frigo_kw", "f_rec",
        "eta_caldaia", "cop_chiller",
        "cop_pdc_risc", "cop_pdc_raff",
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
        _variante(cop_pdc_raff=1.0)


def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"s_m2": 0},
               {"s_m2": -10},
               {"q_risc_kwh_th_m2_anno": -0.1},
               {"q_raff_kwh_c_m2_anno": -0.1},
               {"p_frigo_kw": -0.5},
               {"f_rec": -0.1},
               {"f_rec": 1.01},
               {"eta_caldaia": 0}, {"eta_caldaia": 1.01},
               {"cop_chiller": 1.0}, {"cop_chiller": 0.5},
               {"cop_pdc_risc": 1.0}, {"cop_pdc_risc": 0.5},
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
        assert mh799_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"s_m2": "300"},
               {"s_m2": float("nan")},
               {"p_gas_eur_mwh": float("inf")},
               {"capex_eur": True},
               {"q_risc_kwh_th_m2_anno": "130"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh799_valida(**d)["valido"] is False


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    for kw in ({"p_gas_eur_mwh": 0},
               {"p_gas_eur_mwh": 42.38 - 1},
               {"p_gas_eur_mwh": 30}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["risparmio_eur_anno"] <= 0.0
        assert bc["verdetto"] == "NON_CALCOLABILE"
        assert bc["flussi"]


def test_pareggio_esatto_tolleranza_float():
    # A pareggio esatto il risparmio e' zero (qui 0.0
    # esatto, quindi guard NON_CALCOLABILE; con +0,17
    # a 42,38 arrotondato la VAN resta circa -17.998,
    # quindi NON_CONVIENTE): in nessun caso CONVIENTE.
    bc = _variante(p_gas_eur_mwh=42.37616099071204)
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] in ("NON_CALCOLABILE", "NON_CONVIENTE")
    assert bc["verdetto"] != "CONVIENTE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh799_demo_calcoli()
    testo = mh799_csv(bc, _demo_kwargs())
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
    assert "e_frigo_kwh_anno" in testo
    assert "q_rec_kwh_anno" in testo
    assert "q_risc_net_kwh_anno" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh799_demo_calcoli()
    testo = mh799_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"q_risc_kwh_anno;{bc['q_risc_kwh_anno']}" in testo
    assert f"gas_base_kwh_anno;{bc['gas_base_kwh_anno']}" in testo
    assert f"e_frigo_kwh_anno;{bc['e_frigo_kwh_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh799_demo_calcoli()
    testo = mh799_csv(bc, _demo_kwargs())
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
    return ["mh" + "79" + "8", "st" + "79" + "8",
            "tab" + "79" + "8", "w" + "79" + "9",
            "mh" + "79" + "7", "tab" + "79" + "7"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w800_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w800_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab799:")


def test_registry_chain_tail_and_count():
    """Registry della nuova scheda: il frammento UI apre la
    scheda numero 799 (la coda della catena, in append dopo
    la coda precedente che termina a 798, termina con la
    nuova scheda e il conteggio atteso delle schede e'
    799)."""
    src = _leggi("w800_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert int(m.group(1)) == 799
    assert src.count("with tab799:") == 1


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w800_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w800_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st799_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) >= 24
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w800_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 4
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w800_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def799[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w800_ui.py")
        usate = set(re.findall(r'_def799\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 19
        assert usate <= set(mh799_demo().keys())
