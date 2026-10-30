"""Test nuova scheda "Centro commerciale:
pompa di calore + LED + banchi frigo chiusi
+ scale mobili con standby battono caldaia a
gas + illuminazione tradizionale + banchi frigo
aperti + scale sempre accese?" (titolo
completo nel frammento UI).

Business case deterministico di un centro
commerciale guidato dai M2 DI SUPERFICIE DI
VENDITA e dalle ORE DI APERTURA ALL'ANNO: i
m2 guidano la climatizzazione, le ore per la
potenza di illuminazione guidano
l'illuminazione, il numero di banchi frigo
per i consumi specifici guida i frigoriferi,
il numero di scale mobili per potenza e ore
guida le scale mobili. Climatizzazione = S x
q; illuminazione base = ore x P_ill e LED =
base x f_led; frigo base = n_banchi x
e_banco_aperto e chiusi = n_banchi x
e_banco_chiuso; scale base = n_scale x
P_scala x ore e standby = base x f_standby;
gas baseline = climatizzazione / eta
(rendimento in ingresso, demo 0,90); pompa di
calore = climatizzazione / COP (COP in
ingresso, demo 3,4; zero se Q_clim = 0);
E_base = illuminazione base + frigo base +
scale base; E_alt = pompa di calore + LED +
frigo chiusi + scale standby; C_base =
gas_base / 1000 x p_gas + E_base / 1000 x
p_el + O&M_base; C_alt = E_alt / 1000 x p_el
+ O&M_alt (niente gas); risparmio = C_base -
C_alt; CO2 evitata = (gas_base x 0,20 +
E_base x 0,35 - E_alt x 0,35) / 1000 (fattori
letterali, come nelle schede precedenti: il
brief indica f_gas e f_el senza fissarne i
valori); flussi [-CAPEX, risparmio x vita];
VAN, TIR, payback (primo anno con cumulato
>= 0); breakeven gas = (C_alt - O&M_base -
E_base / 1000 x p_el) x 1000 / gas_base
EUR/MWh, None se gas_base <= 0 o numeratore
< 0, SOGLIA MINIMA quando esiste. Nel demo il
breakeven e' None (non circa 15 EUR/MWh come
stimato nel brief: il numeratore e' negativo,
l'alternativa vince anche a prezzo gas zero).
Verdetto: NON_CALCOLABILE se input degenere
(superficie <= 0, ore <= 0, COP <= 0,
rendimento <= 0, fattore LED o standby fuori
[0, 1], prezzi <= 0, CAPEX <= 0, vita <= 0) o
se risparmio <= 0 (guard degenere: UI salta
KPI, grafico, tabella e CSV); per scelta
esplicita del brief, q = 0, n_banchi = 0 e
n_scale = 0 NON sono degeneri in UI (degenere
solo q, n_banchi o n_scale negativi);
altrimenti CONVIENTE se VAN > 0, MARGINALE
se VAN negativa entro tolleranza % del
CAPEX, NON_CONVIENTE se VAN negativa oltre
la tolleranza. Differenze UI-vs-helper
documentate: S = 0 e' CONVIENTE negli helper
(risparmio 161.790,00 EUR/anno, VAN
1.059.324,87 EUR, TIR 25,20 %, payback 4,
breakeven None perche' gas_base = 0) ma
bloccato dalla guard UI (NON_CALCOLABILE):
qui c'e' DIVERGENZA di verdetto, perche'
illuminazione, frigo e scale da soli
risparmiano anche senza climatizzazione;
q = 0 NON crea divergenza (stessi numeri di
S = 0, CONVIENTE anche in UI perche' la
guard non blocca q = 0); n_banchi = 0 NON
crea divergenza (risparmio 157.554,71
EUR/anno, VAN 1.015.363,97 EUR, payback 4,
CONVIENTE in entrambi); n_scale = 0 NON crea
divergenza (risparmio 183.684,71 EUR/anno,
VAN 1.286.584,43 EUR, payback 4, CONVIENTE
in entrambi); CAPEX = 0 e' CONVIENTE negli
helper (VAN 2.133.587,56 EUR, TIR None,
payback 0) ma bloccato dalla guard UI;
prezzi = 0 sono ammessi negli helper ma
bloccati dalla guard UI (p_el = 0 resta
CONVIENTE negli helper, risparmio 105.000,00
EUR/anno, VAN 469.864,09 EUR, payback 6,
breakeven 12,50 EUR/MWh; p_gas = 0 resta
CONVIENTE negli helper, risparmio 85.554,71
EUR/anno, VAN 268.028,59 EUR, payback 8,
breakeven None: per gas zero QUI C'E'
divergenza di verdetto helper-vs-UI, a
differenza della scheda officina, perche'
qui LED, frigo chiusi e standby da soli
risparmiano piu' di quanto costi
l'elettricita' della pompa di calore).
Distinzione esplicita: distinto dall'officina
(m2 di capannone, portata di aria compressa,
quota di calore recuperato dal compressore
VSD: qui niente aria compressa, niente
compressore, niente recupero calore), dalla
chiesa (m2 di navata, ore di uso a
settimana, quota panche con mantenimento
antigelo: qui niente panche, niente zona
occupata a comfort, niente mantenimento
antigelo), dall'asilo (giorni di apertura,
mensa con pasti al giorno, lavanderia con kg
al giorno: qui niente mensa, niente pasti,
niente lavanderia), dall'albergo
(pernottamenti e camere: qui nessun
pernottamento, nessuna camera): qui driver
M2 + ORE + BANCHI + SCALE, con superficie
di vendita, banchi frigo e scale mobili.

Demo (centro commerciale): superficie
12.000 m2, 90 kWh_t/m2 di climatizzazione
(1.080.000 kWh_t/anno), 4.500 ore all'anno,
potenza di illuminazione 180 kW (810.000
kWh_e/anno) con fattore LED 0,45 (364.500
kWh_e/anno), 40 banchi frigo da 12.000
kWh/anno aperti (480.000 kWh_e/anno) e 7.000
kWh/anno chiusi (280.000 kWh_e/anno), 6 scale
mobili da 7,5 kW (202.500 kWh_e/anno) con
fattore standby 0,55 (111.375 kWh_e/anno),
rendimento caldaia 0,90 (gas base 1.200.000
kWh/anno), COP 3,4 (pompa di calore
317.647,06 kWh_e/anno), gas 100, el 240
EUR/MWh, O&M base 40.000, alt 55.000, CAPEX
620.000, WACC 5 %, vita 15, tolleranza 10 %
del CAPEX. Valori calcolati eseguendo
mh814_demo_calcoli():
Q_clim 1.080.000, E_ill_base 810.000,
E_ill_alt 364.500, E_frigo_base 480.000,
E_frigo_alt 280.000, E_scale_base 202.500,
E_scale_alt 111.375, gas_base 1.200.000,
E_pdc 317.647,0588235294, E_base 1.492.500,
E_alt 1.073.522,0588235294, C_base 518.200,
C_alt 312.645,2941176471, risparmio
205.554,7058823529, CO2_base 762,375,
CO2_alt 375,7327205882352, CO2_evitata
386,6422794117648, VAN 1.513.587,5551976112,
TIR 32,676887922260946 %, payback 4,
breakeven gas None (nessun prezzo non
negativo pareggia: l'alternativa vince anche
a gas zero), verdetto CONVIENTE. NOTA: i
valori approssimati del brief (E_alt
1.173.522, C_alt 336.645, risparmio 181.555,
CO2 evitata circa 326 t, breakeven circa 15
EUR/MWh) sono ERRATI: il ricalcolo esatto
qui sopra li sostituisce (E_alt e' inferiore
di 100.000 per un errore di somma del brief).
"""

import ast
import inspect
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w815_helpers import (
    demo_calcoli,
    mh814_breakeven_gas,
    mh814_c_alt,
    mh814_c_base,
    mh814_calcola,
    mh814_co2_alt,
    mh814_co2_base,
    mh814_co2_evitata,
    mh814_csv,
    mh814_demo,
    mh814_demo_calcoli,
    mh814_e_alt,
    mh814_e_base,
    mh814_e_frigo_alt,
    mh814_e_frigo_base,
    mh814_e_ill_alt,
    mh814_e_ill_base,
    mh814_e_pdc,
    mh814_e_scale_alt,
    mh814_e_scale_base,
    mh814_flussi,
    mh814_frazione,
    mh814_gas_base,
    mh814_int_nneg,
    mh814_int_pos,
    mh814_num,
    mh814_nneg,
    mh814_payback,
    mh814_pct_tolleranza,
    mh814_pos,
    mh814_pct_wacc,
    mh814_q_clim,
    mh814_risparmio,
    mh814_tir,
    mh814_valida,
    mh814_van,
    mh814_verdetto,
)

_DEMO = {
    "q_clim_kwh_anno": 1080000.0,
    "e_ill_base_kwh_anno": 810000.0,
    "e_ill_alt_kwh_anno": 364500.0,
    "e_frigo_base_kwh_anno": 480000.0,
    "e_frigo_alt_kwh_anno": 280000.0,
    "e_scale_base_kwh_anno": 202500.0,
    "e_scale_alt_kwh_anno": 111375.00000000001,
    "gas_base_kwh_anno": 1200000.0,
    "e_pdc_kwh_anno": 317647.0588235294,
    "e_base_kwh_anno": 1492500.0,
    "e_alt_kwh_anno": 1073522.0588235294,
    "c_base_eur_anno": 518200.0,
    "c_alt_eur_anno": 312645.2941176471,
    "risparmio_eur_anno": 205554.7058823529,
    "co2_base_t_anno": 762.375,
    "co2_alt_t_anno": 375.7327205882352,
    "co2_evitata_t_anno": 386.6422794117648,
    "van": 1513587.5551976112,
    "tir": 32.676887922260946,
}


def _demo_kwargs():
    return dict(mh814_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh814_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh814_num(3, "x") == 3.0
    assert mh814_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh814_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh814_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh814_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh814_pos(0, "x")
    with pytest.raises(ValueError):
        mh814_pos(-1, "x")
    assert mh814_pos(0.5, "x") == 0.5


def test_frazione_limiti():
    assert mh814_frazione(0, "x") == 0.0
    assert mh814_frazione(1, "x") == 1.0
    assert mh814_frazione(0.45, "x") == 0.45
    assert mh814_frazione(0.55, "x") == 0.55
    with pytest.raises(ValueError):
        mh814_frazione(-0.01, "x")
    with pytest.raises(ValueError):
        mh814_frazione(1.01, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh814_int_pos(5.0, "x") == 5
    assert mh814_int_pos(4500.0, "x") == 4500
    with pytest.raises(ValueError):
        mh814_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh814_int_pos(0, "x")


def test_int_nneg_zero_ok_frazionario_no_negativo_no():
    assert mh814_int_nneg(0, "x") == 0
    assert mh814_int_nneg(40.0, "x") == 40
    assert mh814_int_nneg(6, "x") == 6
    with pytest.raises(ValueError):
        mh814_int_nneg(5.5, "x")
    with pytest.raises(ValueError):
        mh814_int_nneg(-1, "x")


def test_pct_wacc_limiti():
    assert mh814_pct_wacc(0, "x") == 0.0
    assert mh814_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh814_pct_wacc(50.1, "x")


def test_pct_tolleranza_limiti():
    assert mh814_pct_tolleranza(0, "x") == 0.0
    assert mh814_pct_tolleranza(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh814_pct_tolleranza(-0.1, "x")
    with pytest.raises(ValueError):
        mh814_pct_tolleranza(100.1, "x")


# ---------------------------------------------------------------- fisica base
def test_q_clim_ill_frigo_scale():
    assert mh814_q_clim(12000, 90) == 1080000.0
    assert mh814_q_clim(0, 90) == 0.0
    with pytest.raises(ValueError):
        mh814_q_clim(-1, 90)
    assert mh814_e_ill_base(4500, 180) == 810000.0
    assert mh814_e_ill_base(4500, 0) == 0.0
    with pytest.raises(ValueError):
        mh814_e_ill_base(4500, -1)
    with pytest.raises(ValueError):
        mh814_e_ill_base(0, 180)
    assert mh814_e_ill_alt(810000.0, 0.45) == pytest.approx(364500.0)
    assert mh814_e_ill_alt(810000.0, 0) == 0.0
    assert mh814_e_ill_alt(810000.0, 1) == pytest.approx(810000.0)
    with pytest.raises(ValueError):
        mh814_e_ill_alt(810000.0, 1.01)
    assert mh814_e_frigo_base(40, 12000) == 480000.0
    assert mh814_e_frigo_base(0, 12000) == 0.0
    with pytest.raises(ValueError):
        mh814_e_frigo_base(-1, 12000)
    with pytest.raises(ValueError):
        mh814_e_frigo_base(40.5, 12000)
    assert mh814_e_frigo_alt(40, 7000) == 280000.0
    assert mh814_e_frigo_alt(0, 7000) == 0.0
    assert mh814_e_scale_base(6, 7.5, 4500) == 202500.0
    assert mh814_e_scale_base(0, 7.5, 4500) == 0.0
    with pytest.raises(ValueError):
        mh814_e_scale_base(6, -1, 4500)
    with pytest.raises(ValueError):
        mh814_e_scale_base(6, 7.5, 0)
    assert mh814_e_scale_alt(202500.0, 0.55) == pytest.approx(111375.0)
    assert mh814_e_scale_alt(202500.0, 0) == 0.0
    assert mh814_e_scale_alt(202500.0, 1) == pytest.approx(202500.0)
    with pytest.raises(ValueError):
        mh814_e_scale_alt(202500.0, 1.01)


def test_gas_pdc_totali():
    assert mh814_gas_base(1080000.0, 0.90) == pytest.approx(1200000.0)
    assert mh814_gas_base(0, 0.90) == 0.0
    with pytest.raises(ValueError):
        mh814_gas_base(1080000.0, 0)
    with pytest.raises(ValueError):
        mh814_gas_base(-1, 0.90)
    assert mh814_e_pdc(1080000.0, 3.4) == pytest.approx(317647.0588235294)
    assert mh814_e_pdc(0.0, 3.4) == 0.0
    with pytest.raises(ValueError):
        mh814_e_pdc(1080000.0, 0)
    assert mh814_e_base(810000.0, 480000.0,
                        202500.0) == pytest.approx(1492500.0)
    assert mh814_e_alt(317647.0588235294, 364500.0, 280000.0,
                       111375.0) == pytest.approx(1073522.0588235294)


def test_c_base_c_alt_scomposizione():
    assert mh814_c_base(1200000.0, 100, 1492500.0, 240,
                        40000) == pytest.approx(518200.0)
    assert mh814_c_base(1200000.0, 0, 1492500.0, 240,
                        40000) == pytest.approx(398200.0)
    assert mh814_c_alt(1073522.0588235294, 240,
                       55000) == pytest.approx(312645.2941176471)
    with pytest.raises(ValueError):
        mh814_c_base(1200000.0, 100, 1492500.0, 240, -1)
    with pytest.raises(ValueError):
        mh814_c_alt(1073522.0588235294, 240, -1)


def test_risparmio_segno():
    assert mh814_risparmio(518200.0, 312645.2941176471) == pytest.approx(205554.7058823529)
    assert mh814_risparmio(312645.2941176471, 312645.2941176471) == pytest.approx(0.0, abs=1e-9)


def test_co2_base_alt_evitata():
    assert mh814_co2_base(1200000.0, 1492500.0) == pytest.approx(762.375)
    assert mh814_co2_alt(1073522.0588235294) == pytest.approx(375.7327205882352)
    assert mh814_co2_evitata(1200000.0, 1492500.0,
                             1073522.0588235294) == pytest.approx(386.6422794117648)
    assert mh814_co2_base(0, 0) == 0.0
    assert mh814_co2_alt(0) == 0.0
    with pytest.raises(ValueError):
        mh814_co2_base(1200000.0, -1)
    with pytest.raises(ValueError):
        mh814_co2_alt(-1)


def test_breakeven_demo_none_e_varianti():
    # Demo: numeratore negativo -> None (non ~15):
    # l'alternativa vince anche a gas zero.
    assert mh814_demo_calcoli()["breakeven_gas_eur_mwh"] is None
    assert mh814_breakeven_gas(312645.2941176471,
                               40000, 1492500.0, 240,
                               1200000.0) is None
    bc = _variante(om_alt=300000)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(132.87107843137258)
    assert _variante(superficie_m2=0)["breakeven_gas_eur_mwh"] is None
    assert mh814_breakeven_gas(312645.2941176471,
                               40000, 1492500.0, 240,
                               0) is None
    assert mh814_breakeven_gas(1000, 40000, 1492500.0, 240,
                               1200000.0) is None
    with pytest.raises(ValueError):
        mh814_breakeven_gas(312645.2941176471, 40000, 1492500.0, 240, -1)


def test_breakeven_verifica_pareggio_su_variante():
    # Sul demo il pareggio non esiste (None), quindi
    # la verifica di pareggio usa la variante con
    # O&M alt 300.000, dove il breakeven esiste.
    be = _variante(om_alt=300000)["breakeven_gas_eur_mwh"]
    assert be == pytest.approx(132.87107843137258)
    bc = _variante(om_alt=300000, p_gas=be)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_breakeven_soglia_minima_su_variante():
    be = _variante(om_alt=300000)["breakeven_gas_eur_mwh"]
    bc_alto = _variante(om_alt=300000, p_gas=be + 1)
    bc_basso = _variante(om_alt=300000, p_gas=be - 1)
    assert bc_alto["c_alt_eur_anno"] < bc_alto["c_base_eur_anno"]
    assert bc_basso["c_alt_eur_anno"] > bc_basso["c_base_eur_anno"]
    assert bc_alto["risparmio_eur_anno"] > 0.0
    assert bc_alto["verdetto"] == "NON_CONVIENTE"
    assert bc_basso["verdetto"] == "NON_CALCOLABILE"


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh814_flussi(620000, 205554.7058823529, 15)
    assert len(fl) == 16
    assert fl[0] == -620000
    assert all(f == 205554.7058823529 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh814_demo_calcoli()
    assert bc["van"] == pytest.approx(1513587.5551976112)
    assert mh814_van([-620000] + [205554.7058823529] * 15,
                     0) == pytest.approx(2463320.5882352926)
    assert mh814_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh814_demo_calcoli()
    assert bc["tir"] == pytest.approx(32.676887922260946)
    assert mh814_tir([-620000] + [205554.7058823529] * 15) == \
        pytest.approx(0.32676887922260946)
    tir = mh814_tir([-620000] + [205554.7058823529] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-620000] + [205554.7058823529] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh814_payback([-620000] + [205554.7058823529] * 15) == 4
    assert mh814_payback([-620000] + [-1000.0] * 15) is None
    assert mh814_payback([0] + [205554.7058823529] * 15) == 0
    assert mh814_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh814_verdetto(205554.7058823529, 1513587.5551976112, 620000,
                          10.0) == "CONVIENTE"
    assert mh814_verdetto(205554.7058823529, -1500.0, 620000,
                          10.0) == "MARGINALE"
    assert mh814_verdetto(205554.7058823529, -62000.0, 620000, 10.0) == "MARGINALE"
    assert mh814_verdetto(205554.7058823529, -62000.01, 620000, 10.0) == "NON_CONVIENTE"
    assert mh814_verdetto(205554.7058823529, 0.0, 620000, 10.0) == "MARGINALE"
    assert mh814_verdetto(0.0, 1513587.56, 620000,
                          10.0) == "NON_CALCOLABILE"
    assert mh814_verdetto(-39445.29, -1029428.66, 620000,
                          10.0) == "NON_CALCOLABILE"
    assert mh814_verdetto(None, 1513587.56, 620000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh814_verdetto(float("nan"), 1513587.56, 620000, 10.0)
    with pytest.raises(ValueError):
        mh814_verdetto(205554.7058823529, 1513587.56, -1, 10.0)
    with pytest.raises(ValueError):
        mh814_verdetto(205554.7058823529, 1513587.56, 620000, 100.1)


def test_valida_demo_ok():
    v = mh814_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("superficie_m2", "12000"),
                       ("superficie_m2", float("nan")),
                       ("superficie_m2", float("inf")),
                       ("superficie_m2", True),
                       ("p_gas", None),
                       ("q_clim_per_m2", "90")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh814_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("superficie_m2", -10),
                          ("q_clim_per_m2", -10),
                          ("ore_anno", 0),
                          ("ore_anno", 2.5),
                          ("p_ill_kw", -1),
                          ("f_led", -0.1),
                          ("f_led", 1.01),
                          ("n_banchi", -1),
                          ("n_banchi", 2.5),
                          ("e_banco_aperto_kwh", -1),
                          ("e_banco_chiuso_kwh", -1),
                          ("n_scale", -1),
                          ("n_scale", 2.5),
                          ("p_scala_kw", -1),
                          ("f_standby", -0.1),
                          ("f_standby", 1.01),
                          ("eta_caldaia", 0),
                          ("eta_caldaia", -0.1),
                          ("cop_pdc", 0),
                          ("cop_pdc", -1),
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
        d.update({campo: valore})
        assert mh814_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"superficie_m2": 0,
              "q_clim_per_m2": 0,
              "p_ill_kw": 0,
              "f_led": 0,
              "n_banchi": 0,
              "e_banco_aperto_kwh": 0,
              "e_banco_chiuso_kwh": 0,
              "n_scale": 0,
              "p_scala_kw": 0,
              "f_standby": 0,
              "p_gas": 0,
              "p_el": 0,
              "om_base": 0, "om_alt": 0,
              "capex": 0, "wacc_pct": 0,
              "tolleranza_pct": 0})
    assert mh814_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    d["f_led"] = 1
    d["f_standby"] = 1
    assert mh814_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh814_demo()
    assert d["superficie_m2"] == 12000
    assert d["q_clim_per_m2"] == 90
    assert d["ore_anno"] == 4500
    assert d["p_ill_kw"] == 180
    assert d["f_led"] == 0.45
    assert d["n_banchi"] == 40
    assert d["e_banco_aperto_kwh"] == 12000
    assert d["e_banco_chiuso_kwh"] == 7000
    assert d["n_scale"] == 6
    assert d["p_scala_kw"] == 7.5
    assert d["f_standby"] == 0.55
    assert d["eta_caldaia"] == 0.90
    assert d["cop_pdc"] == 3.4
    assert d["p_gas"] == 100
    assert d["p_el"] == 240
    assert d["om_base"] == 40000
    assert d["om_alt"] == 55000
    assert d["capex"] == 620000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    bc = mh814_demo_calcoli()
    for chiave, atteso in _DEMO.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert got == pytest.approx(atteso, rel=1e-9), chiave
    assert bc["payback"] == 4
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True
    assert bc["breakeven_gas_eur_mwh"] is None
    assert demo_calcoli()["van"] == bc["van"]


def test_demo_calcoli_fisica_economia():
    bc = mh814_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(518200.0)
    assert bc["c_alt_eur_anno"] == pytest.approx(312645.2941176471)
    assert bc["risparmio_eur_anno"] == pytest.approx(205554.7058823529)
    assert bc["co2_base_t_anno"] == pytest.approx(762.375)
    assert bc["co2_alt_t_anno"] == pytest.approx(375.7327205882352)
    assert bc["co2_evitata_t_anno"] == pytest.approx(386.6422794117648)
    assert bc["q_clim_kwh_anno"] == pytest.approx(1080000.0)
    assert bc["e_ill_base_kwh_anno"] == pytest.approx(810000.0)
    assert bc["e_ill_alt_kwh_anno"] == pytest.approx(364500.0)
    assert bc["e_frigo_base_kwh_anno"] == pytest.approx(480000.0)
    assert bc["e_frigo_alt_kwh_anno"] == pytest.approx(280000.0)
    assert bc["e_scale_base_kwh_anno"] == pytest.approx(202500.0)
    assert bc["e_scale_alt_kwh_anno"] == pytest.approx(111375.0)
    assert bc["gas_base_kwh_anno"] == pytest.approx(1200000.0)
    assert bc["e_pdc_kwh_anno"] == pytest.approx(317647.0588235294)


def test_demo_flussi_e_cumulato():
    bc = mh814_demo_calcoli()
    assert bc["flussi"][0] == -620000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(205554.7058823529) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -620000
    assert righe.iloc[3]["Cumulato (EUR)"] == pytest.approx(-3335.8823529413203)
    assert righe.iloc[4]["Cumulato (EUR)"] == pytest.approx(202218.82352941157)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(2463320.5882352926)


def test_demo_tabella_righe():
    bc = mh814_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Climatizzazione (kWh_t/anno)"] == pytest.approx(1080000.0)
    assert mappa["Illuminazione base (kWh_e/anno)"] == pytest.approx(810000.0)
    assert mappa["Illuminazione LED (kWh_e/anno)"] == pytest.approx(364500.0)
    assert mappa["Frigo base banchi aperti (kWh_e/anno)"] == pytest.approx(480000.0)
    assert mappa["Frigo alternativo banchi chiusi (kWh_e/anno)"] == pytest.approx(280000.0)
    assert mappa["Scale base sempre accese (kWh_e/anno)"] == pytest.approx(202500.0)
    assert mappa["Scale alternative standby (kWh_e/anno)"] == pytest.approx(111375.0)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(1200000.0)
    assert mappa["Elettricita' pompa di calore (kWh_e/anno)"] == pytest.approx(317647.0588235294)
    assert mappa["Elettricita' totale base (kWh_e/anno)"] == pytest.approx(1492500.0)
    assert mappa["Elettricita' totale alternativa (kWh_e/anno)"] == pytest.approx(1073522.0588235294)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(518200.0)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(312645.2941176471)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(205554.7058823529)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(386.6422794117648)
    assert mappa["Payback (anni)"] == 4
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] is None


def test_demo_coerenza_interna():
    bc = mh814_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["q_clim_kwh_anno"] == pytest.approx(
        bc["superficie_m2"] * bc["q_clim_per_m2"])
    assert bc["e_ill_base_kwh_anno"] == pytest.approx(
        bc["ore_anno"] * bc["p_ill_kw"])
    assert bc["e_ill_alt_kwh_anno"] == pytest.approx(
        bc["e_ill_base_kwh_anno"] * bc["f_led"])
    assert bc["e_frigo_base_kwh_anno"] == pytest.approx(
        bc["n_banchi"] * bc["e_banco_aperto_kwh"])
    assert bc["e_frigo_alt_kwh_anno"] == pytest.approx(
        bc["n_banchi"] * bc["e_banco_chiuso_kwh"])
    assert bc["e_scale_base_kwh_anno"] == pytest.approx(
        bc["n_scale"] * bc["p_scala_kw"] * bc["ore_anno"])
    assert bc["e_scale_alt_kwh_anno"] == pytest.approx(
        bc["e_scale_base_kwh_anno"] * bc["f_standby"])
    assert bc["gas_base_kwh_anno"] == pytest.approx(
        bc["q_clim_kwh_anno"] / bc["eta_caldaia"])
    assert bc["e_pdc_kwh_anno"] == pytest.approx(
        bc["q_clim_kwh_anno"] / bc["cop_pdc"])
    assert bc["e_base_kwh_anno"] == pytest.approx(
        bc["e_ill_base_kwh_anno"] + bc["e_frigo_base_kwh_anno"]
        + bc["e_scale_base_kwh_anno"])
    assert bc["e_alt_kwh_anno"] == pytest.approx(
        bc["e_pdc_kwh_anno"] + bc["e_ill_alt_kwh_anno"]
        + bc["e_frigo_alt_kwh_anno"] + bc["e_scale_alt_kwh_anno"])
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
    sup, qcl = 12000, 90
    ore, pil, fle = 4500, 180, 0.45
    nba, eap, ech = 40, 12000, 7000
    nsc, psc, fst = 6, 7.5, 0.55
    eta, cop = 0.90, 3.4
    pg, pel = 100, 240
    omb, oma, cx = 40000, 55000, 620000
    wacc, vita = 5.0, 15
    qclim = sup * qcl
    eib = ore * pil
    eia = eib * fle
    efb = nba * eap
    efa = nba * ech
    esb = nsc * psc * ore
    esa = esb * fst
    gasb = qclim / eta
    epdc = qclim / cop
    eb = eib + efb + esb
    ea = epdc + eia + efa + esa
    cb = gasb / 1000.0 * pg + eb / 1000.0 * pel + omb
    ca = ea / 1000.0 * pel + oma
    risp = cb - ca
    co2b = (gasb * 0.20 + eb * 0.35) / 1000.0
    co2a = ea * 0.35 / 1000.0
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    bc = mh814_demo_calcoli()
    assert bc["q_clim_kwh_anno"] == pytest.approx(qclim)
    assert bc["e_ill_base_kwh_anno"] == pytest.approx(eib)
    assert bc["e_ill_alt_kwh_anno"] == pytest.approx(eia)
    assert bc["e_frigo_base_kwh_anno"] == pytest.approx(efb)
    assert bc["e_frigo_alt_kwh_anno"] == pytest.approx(efa)
    assert bc["e_scale_base_kwh_anno"] == pytest.approx(esb)
    assert bc["e_scale_alt_kwh_anno"] == pytest.approx(esa)
    assert bc["gas_base_kwh_anno"] == pytest.approx(gasb)
    assert bc["e_pdc_kwh_anno"] == pytest.approx(epdc)
    assert bc["e_base_kwh_anno"] == pytest.approx(eb)
    assert bc["e_alt_kwh_anno"] == pytest.approx(ea)
    assert bc["c_base_eur_anno"] == pytest.approx(cb)
    assert bc["c_alt_eur_anno"] == pytest.approx(ca)
    assert bc["risparmio_eur_anno"] == pytest.approx(risp)
    assert bc["co2_base_t_anno"] == pytest.approx(co2b)
    assert bc["co2_alt_t_anno"] == pytest.approx(co2a)
    assert bc["co2_evitata_t_anno"] == pytest.approx(co2)
    assert bc["van"] == pytest.approx(van)
    assert bc["breakeven_gas_eur_mwh"] is None


def test_demo_verdetto_coerente_con_risparmio_e_van():
    bc = mh814_demo_calcoli()
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] > 0.0
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["tir"] is not None and bc["tir"] > bc["wacc_pct"]
    assert bc["payback"] == 4


# ---------------------------------------------------------------- varianti
def test_variante_senza_led_resta_convinte_con_breakeven():
    # Fattore LED 1 = nessun risparmio dal LED: il
    # caso peggiora ma resta CONVIENTE, e qui il
    # breakeven ESISTE (17,80 EUR/MWh).
    bc = _variante(f_led=1)
    assert bc["e_ill_alt_kwh_anno"] == pytest.approx(810000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(98634.7058823529)
    assert bc["van"] == pytest.approx(403794.5177553426)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(17.80441176470592)
    assert bc["payback"] == 7
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_senza_frigo_chiusi_resta_convinte():
    # Consumo chiuso uguale all'aperto: niente
    # risparmio dai frigo, ma il resto basta.
    bc = _variante(e_banco_chiuso_kwh=12000)
    assert bc["e_frigo_alt_kwh_anno"] == pytest.approx(480000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(157554.7058823529)
    assert bc["van"] == pytest.approx(1015363.9693649429)
    assert bc["payback"] == 4
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_senza_standby_resta_convinte():
    # Fattore standby 1 = scale sempre accese anche
    # nell'alternativa: il caso peggiora ma resta
    # CONVIENTE.
    bc = _variante(f_standby=1)
    assert bc["e_scale_alt_kwh_anno"] == pytest.approx(202500.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(183684.7058823529)
    assert bc["van"] == pytest.approx(1286584.4339026017)
    assert bc["payback"] == 4
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_risparmio_nonpositivo_non_calcolabile():
    # O&M alt 300.000: risparmio negativo negli
    # helper (calcolabile, non solleva), verdetto
    # NON_CALCOLABILE; stessa guard della UI.
    bc = _variante(om_alt=300000)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(-39445.2941176471)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"]
    assert bc["payback"] is None
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(132.87107843137258)


def test_variante_prezzo_el_zero_helper_convinte_divergenza():
    # Negli helper p_el = 0 e' ammesso e resta
    # CONVIENTE; in UI e' guard degenere:
    # divergenza documentata.
    bc = _variante(p_el=0)
    assert bc["risparmio_eur_anno"] == pytest.approx(105000.0)
    assert bc["van"] == pytest.approx(469864.0940089620)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(12.5)
    assert bc["payback"] == 6
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_prezzo_gas_zero_helper_convinte_divergenza():
    # Negli helper p_gas = 0 e' ammesso e resta
    # CONVIENTE (LED, frigo chiusi e standby da
    # soli risparmiano piu' di quanto costi
    # l'elettricita' della pompa di calore); in UI
    # e' guard degenere (NON_CALCOLABILE): qui
    # c'e' DIVERGENZA di verdetto helper-vs-UI, a
    # differenza della scheda officina.
    bc = _variante(p_gas=0)
    assert bc["risparmio_eur_anno"] == pytest.approx(85554.7058823529)
    assert bc["van"] == pytest.approx(268028.5906159405)
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_superficie_zero_helper_convinte_divergenza():
    # Negli helper S = 0 resta calcolabile e il
    # risparmio resta POSITIVO (illuminazione,
    # frigo e scale da soli risparmiano): verdetto
    # CONVIENTE con breakeven None (gas_base
    # nullo); in UI e' guard degenere
    # (NON_CALCOLABILE): qui c'e' DIVERGENZA di
    # verdetto helper-vs-UI.
    bc = _variante(superficie_m2=0)
    assert bc["q_clim_kwh_anno"] == 0.0
    assert bc["e_pdc_kwh_anno"] == 0.0
    assert bc["gas_base_kwh_anno"] == 0.0
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["risparmio_eur_anno"] == pytest.approx(161790.0)
    assert bc["van"] == pytest.approx(1059324.8739972378)
    assert bc["tir"] == pytest.approx(25.198627953161623)
    assert bc["payback"] == 4
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_carico_zero_nessuna_divergenza():
    # q = 0 coincide con S = 0 negli helper, ma
    # in UI NON e' guard degenere (la guard
    # blocca solo q negativo): qui NON c'e'
    # divergenza di verdetto.
    bc = _variante(q_clim_per_m2=0)
    assert bc["q_clim_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(161790.0)
    assert bc["van"] == pytest.approx(1059324.8739972378)
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_banchi_zero_nessuna_divergenza():
    # n_banchi = 0 resta calcolabile e CONVIENTE
    # negli helper, e in UI NON e' guard degenere:
    # qui NON c'e' divergenza.
    bc = _variante(n_banchi=0)
    assert bc["e_frigo_base_kwh_anno"] == 0.0
    assert bc["e_frigo_alt_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(157554.7058823529)
    assert bc["van"] == pytest.approx(1015363.9693649437)
    assert bc["payback"] == 4
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_scale_zero_nessuna_divergenza():
    # n_scale = 0 resta calcolabile e CONVIENTE
    # negli helper, e in UI NON e' guard degenere:
    # qui NON c'e' divergenza.
    bc = _variante(n_scale=0)
    assert bc["e_scale_base_kwh_anno"] == 0.0
    assert bc["e_scale_alt_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(183684.7058823529)
    assert bc["van"] == pytest.approx(1286584.4339026022)
    assert bc["payback"] == 4
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_marginale_non_convinte_e_zero():
    bc = _variante(capex=2200000)
    assert bc["risparmio_eur_anno"] == pytest.approx(205554.7058823529)
    assert bc["van"] == pytest.approx(-66412.4448023886)
    assert bc["payback"] == 11
    assert bc["verdetto"] == "MARGINALE"
    bc2 = _variante(capex=2500000)
    assert bc2["van"] == pytest.approx(-366412.4448023888)
    assert bc2["payback"] == 13
    assert bc2["verdetto"] == "NON_CONVIENTE"
    bc0 = _variante(capex=0)
    assert bc0["flussi"][0] == 0
    assert bc0["payback"] == 0
    assert bc0["tir"] is None
    assert bc0["van"] == pytest.approx(2133587.5551976115, rel=1e-6)
    assert bc0["verdetto"] == "CONVIENTE"


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(2463320.5882352926)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(967238.9522700747)
    assert bc2["payback"] == 4
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_gas_basso_resta_convinte():
    # Gas a 50 EUR/MWh: il risparmio cala di
    # 60.000 EUR/anno (50 x 1.200 MWh) ma resta
    # CONVIENTE con payback 5 anni.
    bc = _variante(p_gas=50)
    assert bc["risparmio_eur_anno"] == pytest.approx(145554.7058823529)
    assert bc["van"] == pytest.approx(890808.0729067759)
    assert bc["payback"] == 5
    assert bc["verdetto"] == "CONVIENTE"


def test_monotonia_prezzo_gas_crescente():
    base = mh814_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas=101)["risparmio_eur_anno"]
    basso = _variante(p_gas=99)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(1200.0, abs=1e-2)
    assert base - basso == pytest.approx(1200.0, abs=1e-2)


def test_monotonia_led_decrescente_risparmio_cresce():
    assert _variante(f_led=0.20)["risparmio_eur_anno"] > \
        mh814_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(f_led=0.60)["risparmio_eur_anno"] < \
        mh814_demo_calcoli()["risparmio_eur_anno"]


def test_demo_deterministica_due_chiamate():
    a = mh814_demo_calcoli()
    b = mh814_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh814_demo().keys()) == {
        "superficie_m2", "q_clim_per_m2",
        "ore_anno",
        "p_ill_kw", "f_led",
        "n_banchi", "e_banco_aperto_kwh",
        "e_banco_chiuso_kwh",
        "n_scale", "p_scala_kw", "f_standby",
        "eta_caldaia", "cop_pdc",
        "p_gas", "p_el",
        "om_base", "om_alt",
        "capex", "wacc_pct", "vita_anni",
        "tolleranza_pct"}


# ---------------------------------------------------------------- degenere
def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"superficie_m2": -10},
               {"q_clim_per_m2": -10},
               {"ore_anno": 0}, {"ore_anno": 2.5},
               {"p_ill_kw": -1},
               {"f_led": -0.1}, {"f_led": 1.01},
               {"n_banchi": -1}, {"n_banchi": 2.5},
               {"e_banco_aperto_kwh": -1},
               {"e_banco_chiuso_kwh": -1},
               {"n_scale": -1}, {"n_scale": 2.5},
               {"p_scala_kw": -1},
               {"f_standby": -0.1}, {"f_standby": 1.01},
               {"eta_caldaia": 0}, {"eta_caldaia": -0.1},
               {"cop_pdc": 0}, {"cop_pdc": -1},
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
        assert mh814_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"superficie_m2": "12000"},
               {"superficie_m2": float("nan")},
               {"p_gas": float("inf")},
               {"capex": True},
               {"q_clim_per_m2": "90"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh814_valida(**d)["valido"] is False


def test_degenere_superficie_zero_o_gas_zero_non_sollevano():
    # Superficie 0: calcolabile negli helper,
    # risparmio positivo qui (divergenza
    # documentata); gas 0: risparmio ancora
    # positivo qui (divergenza documentata,
    # diversa dalla scheda officina).
    bc = _variante(superficie_m2=0)
    assert bc["valid"] is True
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(p_gas=0)
    assert bc2["valid"] is True
    assert bc2["risparmio_eur_anno"] > 0.0
    assert bc2["verdetto"] == "CONVIENTE"


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    bc = _variante(om_alt=300000)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] <= 0.0
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"]


def test_pareggio_esatto_tolleranza_float():
    # A pareggio esatto (prezzo gas = breakeven
    # della variante OM_alt 300.000) il risparmio
    # e' zero (circa 0.0, quindi guard
    # NON_CALCOLABILE): in nessun caso
    # CONVIENTE.
    be = _variante(om_alt=300000)["breakeven_gas_eur_mwh"]
    bc = _variante(om_alt=300000, p_gas=be)
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["verdetto"] != "CONVIENTE"
    bc2 = _variante(om_alt=300000, p_gas=be + 1)
    assert bc2["risparmio_eur_anno"] == pytest.approx(1200.0, abs=1e-2)
    # Risparmio positivo ma piccolo: VAN negativa oltre
    # la tolleranza, quindi NON_CONVIENTE (non CONVIENTE).
    assert bc2["verdetto"] == "NON_CONVIENTE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh814_demo_calcoli()
    testo = mh814_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_gas_eur_mwh" in testo
    assert "co2_evitata_t_anno" in testo
    assert "q_clim_kwh_anno" in testo
    assert "e_frigo_alt_kwh_anno" in testo
    assert "e_scale_alt_kwh_anno" in testo
    assert "e_pdc_kwh_anno" in testo
    assert "n_banchi" in testo
    assert "n_scale" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh814_demo_calcoli()
    testo = mh814_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"e_frigo_base_kwh_anno;{bc['e_frigo_base_kwh_anno']}" in testo
    assert f"gas_base_kwh_anno;{bc['gas_base_kwh_anno']}" in testo
    assert f"q_clim_kwh_anno;{bc['q_clim_kwh_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh814_demo_calcoli()
    testo = mh814_csv(bc, _demo_kwargs())
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
    return ["mh" + "81" + "3", "st" + "81" + "3",
            "tab" + "81" + "3", "w" + "81" + "4",
            "mh" + "81" + "2", "tab" + "81" + "2"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w815_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w815_ui.py"))
    ast.parse(src)
    assert src.startswith("# W815")
    assert "with tab814:" in src


def test_ui_apre_scheda_attesa_una_volta():
    """Il frammento UI apre la scheda attesa, una sola volta."""
    src = _leggi("w815_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert m.group(1) == "814"
    assert src.count("with tab814:") == 1


def test_ui_titolo_atteso():
    src = _leggi("w815_ui.py")
    titolo = ("Centro commerciale: pompa di calore + "
              "LED + banchi frigo chiusi + scale "
              "mobili con standby battono caldaia a "
              "gas + illuminazione tradizionale + "
              "banchi frigo aperti + scale sempre accese?")
    assert src.count(titolo) == 2


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w815_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w815_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st814_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) == 31
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w815_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 4
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_ui_guard_degenere_stretta():
    """La guard UI della scheda dichiara NON_CALCOLABILE
    anche per superficie <= 0, ore <= 0, COP <= 0,
    rendimento <= 0, prezzi <= 0 e CAPEX <= 0
    (piu' stretta degli helper, che ammettono lo
    zero per prezzi e CAPEX)."""
    src = _leggi("w815_ui.py")
    assert "float(_sup814) <= 0.0" in src
    assert "int(_ore814) <= 0" in src
    assert "float(_cop814) <= 0.0" in src
    assert "float(_eta814) <= 0.0" in src
    assert "float(_pg814) <= 0.0" in src
    assert "float(_pel814) <= 0.0" in src
    assert "float(_cx814) <= 0.0" in src
    assert "int(_vita814) <= 0" in src
    assert "Verdetto: NON_CALCOLABILE" in src


def test_ui_chiamata_calcola_keyword_uguali_firma():
    """La chiamata UI a calcola usa come keyword
    esattamente i parametri della firma helper."""
    src = textwrap.dedent(_leggi("w815_ui.py"))
    albero = ast.parse(src)
    chiamate = []
    for nodo in ast.walk(albero):
        if isinstance(nodo, ast.Call):
            func = nodo.func
            if isinstance(func, ast.Name) and func.id == "mh814_calcola":
                chiamate.append({kw.arg for kw in nodo.keywords})
    assert len(chiamate) == 1
    attesi = set(inspect.signature(mh814_calcola).parameters.keys())
    assert chiamate[0] == attesi


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w815_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def814[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w815_ui.py")
        usate = set(re.findall(r'_def814\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 21
        assert usate <= set(mh814_demo().keys())
