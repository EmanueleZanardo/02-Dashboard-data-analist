"""Test tab755 "Forno ad arco elettrico
(EAF): fondere rottame con elettricita'
batte l'altoforno?"

Nuova tab tab755 (EAF da rottame,
w756). Business case deterministico
di un forno ad arco elettrico
STANDALONE alimentato a rottame
contro la rotta BF-BOF esistente, il
cui CAPEX e' escluso perche' gia'
esistente: il confronto e' solo costo
operativo BF-BOF contro costo
variabile EAF piu' O&M fisso.
E_el = produzione x kWh per t / 1000;
costo_el = kWh per t x p_el;
costo_var_eaf = costo_el + rottame +
altri variabili; C_eaf = costo_var_eaf
x produzione + OM fisso; C_bf =
costo_bf x produzione (solo
operativo); risparmio = C_bf - C_eaf;
CO2 evitata = produzione x (f_bf -
f_eaf), segno libero (puo' essere
negativa), NON monetizzata; CRF solo
nel LCO, mai nei flussi; LCO_eaf =
(CAPEX x CRF + OM fisso) / produzione
+ costo_var_eaf; LCO_bf = costo_bf;
prezzo elettrico di pareggio =
(C_bf - OM fisso - produzione x
(rottame + altri variabili)) /
(produzione x kWh per t), None se il
denominatore <= 0, puo' essere
negativo (il solo O&M fisso piu'
rottame e altri variabili superano
gia' il costo BF-BOF); flussi
[-CAPEX, risparmio x vita]; VAN, TIR,
payback (primo anno con cumulato
>= 0). Distinta dal DRI /
Power-to-Steel (li' il DRI riduce il
minerale e l'EAF e' solo lo step a
valle), dal forno a induzione
(fusione a induzione, nessun arco)
e dal forno vetro / ceramica
(fusione di vetro o ceramica, non
di acciaio da rottame).

Demo calcolata eseguendo demo_calcoli()
(e ricontrollata a mano, riga per riga):
produzione 500.000 t/anno, 400 kWh/t,
prezzo elettrico 0,08 EUR/kWh,
rottame 350 EUR/t, altri variabili
40 EUR/t, O&M fisso 10.000.000
EUR/anno, costo BF-BOF 520 EUR/t,
CAPEX EAF 300.000.000 EUR, fattore
EAF 0,35 tCO2/t e fattore BF-BOF
1,85 tCO2/t, WACC 5 %, vita 20 anni,
tolleranza 10 % del CAPEX.

- e_el_mwh_anno = 200000.0
- costo_el_eur_t = 32.0
- costo_var_eaf_eur_t = 422.0
- c_eaf_eur_anno = 221000000.0
- c_bf_eur_anno = 260000000.0
- risparmio_eur_anno = 39000000.0
- co2_evitata_t_anno = 750000.0
- crf = 0.08024258719069129
- quota_capex_eur_anno = 24072776.157207385
- lco_eaf_eur_t = 490.1455523144148
- lco_bf_eur_t = 520
- van = 186026203.3590597
- tir = 11.535538384892973
- payback = 8
- prezzo_pareggio_eur_kwh = 0.275
- verdetto = 'CONVIENTE'

Scomposizione: E_el = 500.000 x 400 /
1000 = 200.000 MWh_e/anno; costo_el
= 400 x 0,08 = 32 EUR/t; costo
variabile EAF = 32 + 350 + 40 = 422
EUR/t; C_eaf = 422 x 500.000 +
10.000.000 = 221.000.000 EUR/anno;
C_bf = 520 x 500.000 = 260.000.000
EUR/anno (solo operativo); risparmio
= 260.000.000 - 221.000.000 =
39.000.000 EUR/anno; CO2 evitata =
500.000 x (1,85 - 0,35) = 750.000
t/anno (925.000 t del BF-BOF evitato
meno 175.000 t dell'EAF); CAPEX
300.000.000 EUR; CRF 0,05 x
1,05^20 / (1,05^20 - 1) =
0.08024258719069129; quota CAPEX
300.000.000 x 0,080243 =
24.072.776,16 EUR/anno; LCO EAF
(24.072.776,16 + 10.000.000) /
500.000 + 422 = 490,15 EUR/t contro
520 EUR/t del solo operativo BF-BOF;
flussi: anno 0 -300.000.000, anni
1-20 risparmio 39.000.000 (piatti);
VAN -300.000.000 + 39.000.000 x
12,46221034 (annuita' 20 anni al
5 %) = 186.026.203,36 EUR; TIR circa
11,54 %; payback 8 anni (il cumulato
all'anno 7 e' -27.000.000, all'anno 8
e' 12.000.000); prezzo elettrico di
pareggio (260.000.000 - 10.000.000 -
500.000 x 390) / (500.000 x 400) =
0,275 EUR/kWh; verdetto CONVIENTE
perche' VAN > 0.
NOTA: il CRF entra solo nel LCO,
mai nei flussi: il CAPEX compare una
sola volta, all'anno 0.
NOTA 2: in questo brief il risparmio
nullo o negativo NON e' degenere:
con prezzo elettrico 0,30 EUR/kWh il
risparmio e' -5.000.000 EUR/anno e
il caso resta calcolabile (valid=True,
VAN -362.311.051,71 EUR,
NON_CONVIENTE).
NOTA 3: la CO2 evitata puo' essere
negativa: con fattore EAF 2,00
tCO2/t la CO2 evitata e' -75.000
t/anno, pur restando il caso
economicamente CONVIENTE.
NOTA 4: il prezzo elettrico di
pareggio puo' essere negativo: con
O&M fisso 300.000.000 EUR/anno il
pareggio e' -1,175 EUR/kWh, perche'
il solo O&M fisso piu' rottame e
altri variabili superano gia' il
costo BF-BOF.
NOTA 5: il brief stimava la quota
CAPEX a circa 24.072.900 EUR/anno:
il ricalcolo indipendente da zero
da' 24.072.776,16 EUR/anno
(300.000.000 x 0,08024258719069129)
e il test usa il valore ricalcolato.
"""

import ast
import math
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w756_helpers import (
    demo_calcoli,
    mh755_c_bf,
    mh755_c_eaf,
    mh755_calcola,
    mh755_co2_evitata,
    mh755_costo_el_eur_t,
    mh755_costo_var_eaf,
    mh755_crf,
    mh755_csv,
    mh755_demo,
    mh755_e_el_mwh,
    mh755_flussi,
    mh755_int_pos,
    mh755_lco_bf,
    mh755_lco_eaf,
    mh755_nneg,
    mh755_num,
    mh755_payback,
    mh755_pct_0_100,
    mh755_pct_wacc,
    mh755_pos,
    mh755_prezzo_pareggio,
    mh755_quota_capex,
    mh755_risparmio,
    mh755_tir,
    mh755_valida,
    mh755_van,
    mh755_verdetto,
)


def _demo_kwargs():
    return dict(mh755_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh755_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh755_num(3, "x") == 3.0
    assert mh755_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh755_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh755_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh755_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh755_pos(0, "x")
    with pytest.raises(ValueError):
        mh755_pos(-1, "x")
    assert mh755_pos(0.5, "x") == 0.5


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh755_int_pos(5.0, "x") == 5
    with pytest.raises(ValueError):
        mh755_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh755_int_pos(0, "x")


def test_pct_0_100_limiti():
    assert mh755_pct_0_100(0, "x") == 0.0
    assert mh755_pct_0_100(100, "x") == 100.0
    with pytest.raises(ValueError):
        mh755_pct_0_100(100.1, "x")
    with pytest.raises(ValueError):
        mh755_pct_0_100(-1, "x")


def test_pct_wacc_limiti():
    assert mh755_pct_wacc(0, "x") == 0.0
    assert mh755_pct_wacc(50, "x") == 50.0
    with pytest.raises(ValueError):
        mh755_pct_wacc(50.1, "x")


# ---------------------------------------------------------------- fisica base
def test_e_el_mwh():
    assert mh755_e_el_mwh(500000, 400) == 200000.0
    assert mh755_e_el_mwh(1000000, 400) == 400000.0
    assert mh755_e_el_mwh(500000, 300) == 150000.0
    with pytest.raises(ValueError):
        mh755_e_el_mwh(0, 400)
    with pytest.raises(ValueError):
        mh755_e_el_mwh(500000, 0)


def test_costo_el_e_costo_var():
    assert mh755_costo_el_eur_t(400, 0.08) == 32.0
    assert mh755_costo_el_eur_t(400, 0.0) == 0.0
    assert mh755_costo_var_eaf(32.0, 350, 40) == 422.0
    assert mh755_costo_var_eaf(0.0, 0, 0) == 0.0
    with pytest.raises(ValueError):
        mh755_costo_el_eur_t(400, -0.01)
    with pytest.raises(ValueError):
        mh755_costo_var_eaf(32.0, -1, 40)


def test_c_eaf_e_c_bf_solo_operativo():
    assert mh755_c_eaf(422.0, 500000, 10000000) == 221000000.0
    assert mh755_c_eaf(422.0, 500000, 0) == 211000000.0
    assert mh755_c_bf(520, 500000) == 260000000.0
    assert mh755_c_bf(520, 0) == 0.0
    with pytest.raises(ValueError):
        mh755_c_eaf(422.0, 500000, -100)
    with pytest.raises(ValueError):
        mh755_c_bf(-1, 500000)


def test_risparmio_segno():
    assert mh755_risparmio(260000000.0, 221000000.0) == 39000000.0
    assert mh755_risparmio(260000000.0, 260000000.0) == 0.0
    assert mh755_risparmio(260000000.0, 265000000.0) == -5000000.0
    assert mh755_risparmio(0.0, 0.0) == 0.0


def test_co2_evitata_segno_libero():
    assert mh755_co2_evitata(500000, 1.85, 0.35) == 750000.0
    assert mh755_co2_evitata(500000, 1.85, 2.00) == pytest.approx(-75000.0)
    assert mh755_co2_evitata(500000, 1.85, 1.85) == 0.0
    assert mh755_co2_evitata(0, 1.85, 0.35) == 0.0
    with pytest.raises(ValueError):
        mh755_co2_evitata(500000, -1.85, 0.35)


# ---------------------------------------------------------------- finanza base
def test_crf():
    assert mh755_crf(5.0, 20) == pytest.approx(0.08024258719069129)
    assert mh755_crf(0, 20) == pytest.approx(1.0 / 20.0)
    assert mh755_crf(5.0, 1) == pytest.approx(1.05)
    assert mh755_crf(5.0, 10) == pytest.approx(0.12950457496545661)


def test_quota_capex_e_lco():
    assert mh755_quota_capex(300000000, 0.08024258719069129) == pytest.approx(
        24072776.157207385)
    assert mh755_lco_eaf(300000000, 0.08024258719069129, 10000000,
                         500000, 422.0) == pytest.approx(
        490.1455523144148)
    assert mh755_lco_bf(520) == 520
    assert mh755_lco_eaf(300000000, 0.08024258719069129, 10000000,
                         0, 422.0) is None
    assert mh755_lco_eaf(0, 0.08024258719069129, 10000000,
                         500000, 422.0) == pytest.approx(442.0)


def test_prezzo_pareggio_formula_brief_negativo_e_none():
    assert mh755_prezzo_pareggio(260000000.0, 10000000, 500000, 350, 40,
                                 400) == pytest.approx(0.275)
    assert mh755_prezzo_pareggio(260000000.0, 300000000, 500000, 350, 40,
                                 400) == pytest.approx(-1.175)
    assert mh755_prezzo_pareggio(260000000.0, 65000000, 500000, 350, 40,
                                 400) == pytest.approx(0.0, abs=1e-9)
    assert mh755_prezzo_pareggio(260000000.0, 10000000, 500000, 350, 40,
                                 0) is None
    assert mh755_prezzo_pareggio(260000000.0, 10000000, 0, 350, 40,
                                 400) is None
    assert mh755_prezzo_pareggio(260000000.0, 10000000, -500000, 350, 40,
                                 400) is None
    assert mh755_prezzo_pareggio(0.0, 0, 500000, 0, 0, 400) == 0.0


def test_flussi_lunghezza_e_primo():
    fl = mh755_flussi(300000000, 39000000.0, 20)
    assert len(fl) == 21
    assert fl[0] == -300000000
    assert all(f == 39000000.0 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = demo_calcoli()
    assert bc["van"] == pytest.approx(186026203.3590597)
    assert mh755_van([-300000000] + [39000000.0] * 20,
                     0) == pytest.approx(480000000.0)
    assert mh755_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo_e_conviente():
    bc = demo_calcoli()
    assert bc["tir"] == pytest.approx(11.535538384892973)
    assert mh755_tir([-300000000] + [39000000.0] * 20) == pytest.approx(
        0.11535538384892974)
    tir = mh755_tir([-300000000] + [39000000.0] * 20)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-300000000] + [39000000.0] * 20))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback():
    assert mh755_payback([-300000000] + [39000000.0] * 20) == 8
    assert mh755_payback([-300000000] + [800.0] * 20) is None
    assert mh755_payback([0] + [39000000.0] * 20) == 0
    assert mh755_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh755_verdetto(100.0, 300000000, 10.0) == "CONVIENTE"
    assert mh755_verdetto(-29000000.0, 300000000, 10.0) == "MARGINALE"
    assert mh755_verdetto(-30000000.0, 300000000, 10.0) == "MARGINALE"
    assert mh755_verdetto(-30000000.01, 300000000, 10.0) == "NON_CONVIENTE"
    assert mh755_verdetto(-186026203.36, 300000000, 10.0) == "NON_CONVIENTE"
    assert mh755_verdetto(float("nan"), 300000000, 10.0) == "NON_CALCOLABILE"
    assert mh755_verdetto(0.0, 0, 10.0) == "MARGINALE"


def test_valida_demo_ok():
    v = mh755_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("produzione_t_anno", "500000"),
                       ("produzione_t_anno", float("nan")),
                       ("produzione_t_anno", float("inf")),
                       ("produzione_t_anno", True),
                       ("prezzo_el_eur_kwh", None)):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh755_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("produzione_t_anno", 0),
                          ("kwh_per_t", 0),
                          ("kwh_per_t", -10),
                          ("prezzo_el_eur_kwh", -0.01),
                          ("prezzo_rottame_eur_t", -1),
                          ("altri_var_eur_t", -1),
                          ("om_fisso_eur_anno", -100),
                          ("costo_bf_eur_t", -1),
                          ("capex_eur", -1),
                          ("f_eaf_t_per_t", -0.10),
                          ("f_bf_t_per_t", -0.10),
                          ("wacc_pct", -0.1), ("wacc_pct", 50.1),
                          ("vita_anni", 0), ("vita_anni", 2.5),
                          ("tolleranza_pct", -1),
                          ("tolleranza_pct", 100.1)):
        d = _demo_kwargs()
        d[campo] = valore
        assert mh755_valida(**d)["valido"] is False


def test_valida_accetta_limiti():
    d = _demo_kwargs()
    d.update({"prezzo_el_eur_kwh": 0, "prezzo_rottame_eur_t": 0,
              "altri_var_eur_t": 0, "om_fisso_eur_anno": 0,
              "costo_bf_eur_t": 0, "capex_eur": 0,
              "f_eaf_t_per_t": 0, "f_bf_t_per_t": 0,
              "wacc_pct": 0, "tolleranza_pct": 0})
    assert mh755_valida(**d)["valido"] is True
    d["wacc_pct"] = 50
    d["tolleranza_pct"] = 100
    assert mh755_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh755_demo()
    assert d["produzione_t_anno"] == 500000
    assert d["kwh_per_t"] == 400
    assert d["prezzo_el_eur_kwh"] == 0.08
    assert d["prezzo_rottame_eur_t"] == 350
    assert d["altri_var_eur_t"] == 40
    assert d["om_fisso_eur_anno"] == 10000000
    assert d["costo_bf_eur_t"] == 520
    assert d["capex_eur"] == 300000000
    assert d["f_eaf_t_per_t"] == 0.35
    assert d["f_bf_t_per_t"] == 1.85
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 20
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    """Ogni _DEMO del test contro demo_calcoli():
    scarto relativo < 1e-9 (zero atteso:
    confronto assoluto)."""
    bc = demo_calcoli()
    attesi = {
        "e_el_mwh_anno": 200000.0,
        "costo_el_eur_t": 32.0,
        "costo_var_eaf_eur_t": 422.0,
        "c_eaf_eur_anno": 221000000.0,
        "c_bf_eur_anno": 260000000.0,
        "risparmio_eur_anno": 39000000.0,
        "co2_evitata_t_anno": 750000.0,
        "crf": 0.08024258719069129,
        "quota_capex_eur_anno": 24072776.157207385,
        "lco_eaf_eur_t": 490.1455523144148,
        "lco_bf_eur_t": 520,
        "van": 186026203.3590597,
        "tir": 11.535538384892973,
        "prezzo_pareggio_eur_kwh": 0.275,
    }
    for chiave, atteso in attesi.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert abs(got - atteso) / abs(atteso) < 1e-9, chiave
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True


def test_demo_calcoli_fisica():
    bc = demo_calcoli()
    assert bc["valid"] is True
    assert bc["e_el_mwh_anno"] == 200000.0
    assert bc["costo_el_eur_t"] == 32.0
    assert bc["costo_var_eaf_eur_t"] == 422.0
    assert bc["co2_evitata_t_anno"] == 750000.0


def test_demo_calcoli_economia():
    bc = demo_calcoli()
    assert bc["c_eaf_eur_anno"] == 221000000.0
    assert bc["c_bf_eur_anno"] == 260000000.0
    assert bc["risparmio_eur_anno"] == 39000000.0
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx(0.275)


def test_demo_calcoli_finanza():
    bc = demo_calcoli()
    assert bc["crf"] == pytest.approx(0.08024258719069129)
    assert bc["quota_capex_eur_anno"] == pytest.approx(24072776.157207385)
    assert bc["lco_eaf_eur_t"] == pytest.approx(490.1455523144148)
    assert bc["lco_bf_eur_t"] == 520
    assert bc["van"] == pytest.approx(186026203.3590597)
    assert bc["tir"] == pytest.approx(11.535538384892973)
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"


def test_demo_flussi_e_cumulato():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -300000000
    assert len(bc["flussi"]) == 21
    assert all(f == 39000000.0 for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -300000000
    assert righe.iloc[7]["Cumulato (EUR)"] == -27000000.0
    assert righe.iloc[8]["Cumulato (EUR)"] == 12000000.0
    assert righe.iloc[20]["Cumulato (EUR)"] == 480000000.0
    assert righe.iloc[20]["Flusso (EUR/anno)"] == 39000000.0


def test_demo_tabella_righe():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Energia elettrica (MWh_e/anno)"] == 200000.0
    assert mappa["Costo variabile EAF (EUR/t)"] == 422.0
    assert mappa["Risparmio (EUR/anno)"] == 39000000.0
    assert mappa["Payback (anni)"] == 8
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Prezzo elettrico di pareggio (EUR/kWh)"] == pytest.approx(
        0.275)


def test_demo_coerenza_interna():
    bc = demo_calcoli()
    assert bc["c_bf_eur_anno"] - bc["c_eaf_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["costo_var_eaf_eur_t"] * bc["produzione_t_anno"] + \
        bc["om_fisso_eur_anno"] == pytest.approx(bc["c_eaf_eur_anno"])
    assert bc["costo_bf_eur_t"] * bc["produzione_t_anno"] == \
        pytest.approx(bc["c_bf_eur_anno"])
    assert bc["produzione_t_anno"] * (bc["f_bf_t_per_t"] -
                                      bc["f_eaf_t_per_t"]) == \
        pytest.approx(bc["co2_evitata_t_anno"])
    assert bc["capex_eur"] * bc["crf"] == pytest.approx(
        bc["quota_capex_eur_anno"])
    assert (bc["quota_capex_eur_anno"] + bc["om_fisso_eur_anno"]) / \
        bc["produzione_t_anno"] + bc["costo_var_eaf_eur_t"] == \
        pytest.approx(bc["lco_eaf_eur_t"])
    assert bc["c_bf_eur_anno"] - bc["om_fisso_eur_anno"] - \
        bc["produzione_t_anno"] * (bc["prezzo_rottame_eur_t"] +
                                   bc["altri_var_eur_t"]) == \
        pytest.approx(bc["prezzo_pareggio_eur_kwh"] *
                      bc["produzione_t_anno"] * bc["kwh_per_t"])
    assert bc["produzione_t_anno"] * bc["kwh_per_t"] / 1000.0 == \
        pytest.approx(bc["e_el_mwh_anno"])


def test_demo_crf_solo_nel_lco_non_nei_flussi():
    bc = demo_calcoli()
    assert bc["flussi"][0] == -bc["capex_eur"]
    assert all(f == bc["risparmio_eur_anno"] for f in bc["flussi"][1:])
    assert bc["crf"] not in bc["flussi"]
    assert bc["quota_capex_eur_anno"] not in bc["flussi"]
    van_da_flussi = mh755_van(bc["flussi"], bc["wacc_pct"])
    assert van_da_flussi == pytest.approx(bc["van"])
    assert bc["lco_eaf_eur_t"] == pytest.approx(
        (bc["capex_eur"] * bc["crf"] + bc["om_fisso_eur_anno"]) /
        bc["produzione_t_anno"] + bc["costo_var_eaf_eur_t"])


def test_demo_contro_riconteggio_indipendente():
    prod, kwh = 500000, 400
    pe, rott, altri = 0.08, 350, 40
    om, cbf_t, cx = 10000000, 520, 300000000
    fe, fb = 0.35, 1.85
    wacc, vita = 5.0, 20
    e_el = prod * kwh / 1000.0
    c_el = kwh * pe
    var = c_el + rott + altri
    c_eaf = var * prod + om
    c_bf = cbf_t * prod
    risp = c_bf - c_eaf
    co2 = prod * (fb - fe)
    r = wacc / 100.0
    crf = r * (1 + r) ** vita / ((1 + r) ** vita - 1)
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    bc = demo_calcoli()
    assert bc["e_el_mwh_anno"] == e_el
    assert bc["costo_el_eur_t"] == c_el
    assert bc["costo_var_eaf_eur_t"] == var
    assert bc["c_eaf_eur_anno"] == c_eaf
    assert bc["c_bf_eur_anno"] == c_bf
    assert bc["risparmio_eur_anno"] == risp
    assert bc["co2_evitata_t_anno"] == co2
    assert bc["crf"] == pytest.approx(crf)
    assert bc["van"] == pytest.approx(van)
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx(
        (c_bf - om - prod * (rott + altri)) / (prod * kwh))


def test_demo_riconteggio_crf_van_payback_pareggio_a_mano():
    bc = demo_calcoli()
    r = 0.05
    annuita = (1 - (1 + r) ** -20) / r
    assert annuita == pytest.approx(12.462210342539992)
    assert bc["van"] == pytest.approx(-300000000 + 39000000 * annuita)
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx(
        (260000000.0 - 10000000 - 500000 * 390) / (500000 * 400))
    assert bc["flussi"][0] + 20 * bc["flussi"][1] == pytest.approx(
        480000000.0)
    assert bc["flussi"][0] + 8 * bc["flussi"][1] == pytest.approx(
        12000000.0)


# ---------------------------------------------------------------- varianti
def test_variante_prezzo_el_alto_non_conviente():
    bc = _variante(prezzo_el_eur_kwh=0.30)
    assert bc["risparmio_eur_anno"] == -5000000.0
    assert bc["van"] == pytest.approx(-362311051.7127)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx(0.275)
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_variante_prezzo_el_marginale():
    bc = _variante(prezzo_el_eur_kwh=0.16)
    assert bc["risparmio_eur_anno"] == 23000000.0
    assert bc["van"] < 0.0
    assert abs(bc["van"]) <= 0.10 * 300000000
    assert bc["tir"] == pytest.approx(4.468532, abs=1e-4)
    assert bc["payback"] == 14
    assert bc["verdetto"] == "MARGINALE"
    assert bc["valid"] is True


def test_variante_prezzo_el_vicino_pareggio_non_conviente():
    bc = _variante(prezzo_el_eur_kwh=0.20)
    assert bc["risparmio_eur_anno"] == 15000000.0
    assert bc["van"] == pytest.approx(-113066844.8619)
    assert bc["tir"] == pytest.approx(0.0, abs=1e-6)
    assert bc["payback"] == 20
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_risparmio_azzerato_calcolabile():
    bc = _variante(prezzo_el_eur_kwh=0.275)
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["van"] == pytest.approx(-300000000.0)
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx(0.275)
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_variante_co2_negativa():
    bc = _variante(f_eaf_t_per_t=2.00)
    assert bc["co2_evitata_t_anno"] == pytest.approx(-75000.0)
    assert bc["co2_evitata_t_anno"] < 0.0
    assert bc["van"] == pytest.approx(186026203.3590597)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_co2_zero():
    bc = _variante(f_eaf_t_per_t=1.85)
    assert bc["co2_evitata_t_anno"] == 0.0
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_pareggio_negativo():
    bc = _variante(om_fisso_eur_anno=300000000)
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx(-1.175)
    assert bc["prezzo_pareggio_eur_kwh"] < 0.0
    assert bc["risparmio_eur_anno"] == -251000000.0
    assert bc["verdetto"] == "NON_CONVIENTE"
    assert bc["valid"] is True


def test_variante_pareggio_zero():
    bc = _variante(om_fisso_eur_anno=65000000)
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx(0.0, abs=1e-9)
    assert bc["lco_eaf_eur_t"] == pytest.approx(600.1455523144148)


def test_variante_rottame_caro_non_conviente():
    bc = _variante(prezzo_rottame_eur_t=450)
    assert bc["costo_var_eaf_eur_t"] == 522.0
    assert bc["risparmio_eur_anno"] == -11000000.0
    assert bc["van"] == pytest.approx(-437084313.76794)
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx(0.025)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_wacc_zero():
    bc = _variante(wacc_pct=0)
    assert bc["crf"] == pytest.approx(1.0 / 20.0)
    assert bc["quota_capex_eur_anno"] == pytest.approx(15000000.0)
    assert bc["lco_eaf_eur_t"] == pytest.approx(472.0)
    assert bc["van"] == pytest.approx(480000000.0)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_zero_payback_zero_tir_none():
    bc = _variante(capex_eur=0)
    assert bc["capex_eur"] == 0
    assert bc["flussi"][0] == 0
    assert bc["payback"] == 0
    assert bc["tir"] is None
    assert bc["van"] == pytest.approx(486026203.35906)
    assert bc["lco_eaf_eur_t"] == pytest.approx(442.0)
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_vita_dieci():
    bc = _variante(vita_anni=10)
    assert len(bc["flussi"]) == 11
    assert bc["crf"] == pytest.approx(0.12950457496545661)
    assert bc["van"] == pytest.approx(1147662.238208)
    assert bc["tir"] == pytest.approx(5.078702, abs=1e-4)
    assert bc["payback"] == 8
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_produzione_doppia():
    bc = _variante(produzione_t_anno=1000000)
    assert bc["e_el_mwh_anno"] == 400000.0
    assert bc["risparmio_eur_anno"] == 88000000.0
    assert bc["co2_evitata_t_anno"] == 1500000.0
    assert bc["van"] == pytest.approx(796674510.143519)
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx(0.3)
    assert bc["payback"] == 4
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_kwh_ridotti():
    bc = _variante(kwh_per_t=300)
    assert bc["e_el_mwh_anno"] == 150000.0
    assert bc["costo_el_eur_t"] == 24.0
    assert bc["costo_var_eaf_eur_t"] == 414.0
    assert bc["risparmio_eur_anno"] == 43000000.0
    assert bc["van"] == pytest.approx(235875044.72922)
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx(0.3666666666666667)
    assert bc["payback"] == 7
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_costo_bf_basso_non_conviente():
    bc = _variante(costo_bf_eur_t=400)
    assert bc["c_bf_eur_anno"] == 200000000.0
    assert bc["risparmio_eur_anno"] == -21000000.0
    assert bc["van"] == pytest.approx(-561706417.19334)
    assert bc["prezzo_pareggio_eur_kwh"] == pytest.approx(-0.025)
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_prezzo_el_nullo():
    bc = _variante(prezzo_el_eur_kwh=0.0)
    assert bc["valid"] is True
    assert bc["costo_el_eur_t"] == 0.0
    assert bc["costo_var_eaf_eur_t"] == 390.0
    assert bc["c_eaf_eur_anno"] == 205000000.0
    assert bc["risparmio_eur_anno"] == 55000000.0
    assert bc["van"] == pytest.approx(385421568.8397)
    assert bc["payback"] == 6
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_input_nulli_calcolabile_non_degenere():
    bc = _variante(prezzo_el_eur_kwh=0.0, prezzo_rottame_eur_t=0,
                   altri_var_eur_t=0)
    assert bc["valid"] is True
    assert bc["c_eaf_eur_anno"] == 10000000.0
    assert bc["c_bf_eur_anno"] == 260000000.0
    assert bc["risparmio_eur_anno"] == 250000000.0
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_pareggio_negativo_demo_no():
    bc = demo_calcoli()
    assert bc["prezzo_pareggio_eur_kwh"] > 0.0
    assert bc["valid"] is True
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["risparmio_eur_anno"] > 0.0


# ---------------------------------------------------------------- degenere
def test_degenere_produzione_zero():
    bc = _variante(produzione_t_anno=0)
    assert bc["valid"] is False
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"] == []
    assert bc["tir"] is None
    assert bc["payback"] is None
    assert bc["prezzo_pareggio_eur_kwh"] is None
    assert bc["lco_eaf_eur_t"] is None
    assert bc["lco_bf_eur_t"] is None
    assert bc["errore"]


def test_degenere_kwh_produzione_vita():
    for kw in ({"kwh_per_t": 0}, {"kwh_per_t": -10},
               {"produzione_t_anno": 0},
               {"produzione_t_anno": -1},
               {"vita_anni": 0}, {"vita_anni": 2.5}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_wacc_tolleranza_prezzi_negativi():
    for kw in ({"wacc_pct": -1}, {"wacc_pct": 60},
               {"tolleranza_pct": -1}, {"tolleranza_pct": 101},
               {"prezzo_el_eur_kwh": -0.01},
               {"prezzo_rottame_eur_t": -1},
               {"altri_var_eur_t": -1},
               {"om_fisso_eur_anno": -100},
               {"costo_bf_eur_t": -1}, {"capex_eur": -1}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_stringa_nan_inf():
    for kw in ({"produzione_t_anno": "500000"},
               {"produzione_t_anno": float("nan")},
               {"prezzo_el_eur_kwh": float("inf")},
               {"capex_eur": True}):
        bc = _variante(**kw)
        assert bc["valid"] is False
        assert bc["verdetto"] == "NON_CALCOLABILE"


def test_degenere_neutro_campi():
    bc = _variante(produzione_t_anno=0)
    assert bc["e_el_mwh_anno"] == 0.0
    assert bc["costo_el_eur_t"] == 0.0
    assert bc["costo_var_eaf_eur_t"] == 0.0
    assert bc["c_eaf_eur_anno"] == 0.0
    assert bc["c_bf_eur_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == 0.0
    assert bc["van"] == 0.0
    assert list(bc["df_flussi"].columns) == [
        "Anno", "Flusso (EUR/anno)", "Cumulato (EUR)"]
    assert list(bc["df_tabella"].columns) == ["Voce", "Valore"]


def test_pareggio_none_quando_denominatore_zero():
    assert mh755_prezzo_pareggio(260000000.0, 10000000, 500000, 350, 40,
                                 0) is None
    assert mh755_prezzo_pareggio(260000000.0, 10000000, 0, 350, 40,
                                 400) is None
    assert mh755_lco_eaf(300000000, 0.08024258719069129, 10000000,
                         0, 422.0) is None


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = demo_calcoli()
    testo = mh755_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert "e_el_mwh_anno;200000.0" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "prezzo_pareggio_eur_kwh" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = demo_calcoli()
    testo = mh755_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"quota_capex_eur_anno;{bc['quota_capex_eur_anno']}" in testo
    assert f"e_el_mwh_anno;{bc['e_el_mwh_anno']}" in testo


def test_csv_degenere_solo_zeri():
    bc = _variante(produzione_t_anno=0)
    testo = mh755_csv(bc, _demo_kwargs())
    assert "van_eur;0.0" in testo
    assert "e_el_mwh_anno;0.0" in testo
    assert "verdetto;NON_CALCOLABILE" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = demo_calcoli()
    testo = mh755_csv(bc, _demo_kwargs())
    for chiave in _demo_kwargs():
        assert f"{chiave};" in testo


def test_calcola_non_sollevela_per_input_numerici():
    bc = _variante(prezzo_el_eur_kwh=0, prezzo_rottame_eur_t=0,
                   altri_var_eur_t=0, f_eaf_t_per_t=0, f_bf_t_per_t=0)
    assert bc["valid"] is True
    assert bc["c_eaf_eur_anno"] == 10000000.0
    assert bc["c_bf_eur_anno"] == 260000000.0
    assert bc["risparmio_eur_anno"] == 250000000.0


def test_monotonia_prezzo_el():
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(prezzo_el_eur_kwh=0.10)["risparmio_eur_anno"]
    basso = _variante(prezzo_el_eur_kwh=0.05)["risparmio_eur_anno"]
    assert basso > base > alto
    assert basso - base == pytest.approx(6000000.0)
    assert base - alto == pytest.approx(4000000.0)


def test_monotonia_prezzo_rottame():
    base = demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(prezzo_rottame_eur_t=400)["risparmio_eur_anno"]
    assert alto < base
    assert base - alto == pytest.approx(25000000.0)


def test_demo_deterministica_due_chiamate():
    a = demo_calcoli()
    b = demo_calcoli()
    assert a["van"] == b["van"]
    assert a["flussi"] == b["flussi"]
    assert a["tir"] == b["tir"]


def test_demo_chiavi_attese():
    assert set(mh755_demo().keys()) == {
        "produzione_t_anno", "kwh_per_t",
        "prezzo_el_eur_kwh", "prezzo_rottame_eur_t",
        "altri_var_eur_t", "om_fisso_eur_anno",
        "costo_bf_eur_t", "capex_eur",
        "f_eaf_t_per_t", "f_bf_t_per_t",
        "wacc_pct", "vita_anni", "tolleranza_pct"}


# ---------------------------------------------------------------- AST / regole dure
_HF_FALLBACK = os.path.expanduser("~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files")


def _leggi(nome):
    qui = os.path.dirname(os.path.abspath(__file__))
    p = os.path.join(qui, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    with open(p, encoding="utf-8") as f:
        return f.read()


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w756_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w756_ui.py"))
    ast.parse(src)
    assert src.startswith("with tab755:")


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    # token vietati costruiti per concatenazione, cosi' questo
    # stesso file non li contiene come sottostringhe contigue.
    src = _leggi("w756_helpers.py")
    vietati = ["mh" + "75" + "4", "st" + "75" + "4",
               "tab" + "75" + "4", "w" + "75" + "5",
               "mh" + "75" + "3", "tab" + "75" + "3"]
    assert "streamlit" not in src
    assert all(t not in src for t in vietati)


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w756_ui.py")
    vietati = ["mh" + "75" + "4", "st" + "75" + "4",
               "tab" + "75" + "4", "w" + "75" + "5",
               "mh" + "75" + "3", "tab" + "75" + "3"]
    assert all(t not in src for t in vietati)
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st755_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert "key=f" not in src and 'key = f' not in src
    assert "st.stop()" in src
    # guard degenere prima di KPI / grafico / tabella / CSV
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")


def test_test_senza_residui_vecchia_tab():
    # token costruiti per concatenazione: il sorgente di questo
    # stesso test non deve contenere i token vietati come
    # sottostringhe contigue (altrimenti il test sarebbe
    # autoreferenziale e fallirebbe sempre).
    src = _leggi("w756_test.py")
    vietati = ["mh" + "75" + "4", "st" + "75" + "4",
               "tab" + "75" + "4", "w" + "75" + "5",
               "mh" + "75" + "3", "tab" + "75" + "3"]
    assert all(t not in src for t in vietati)


def test_ui_chiavi_demo_coerenti():
    """Ogni _def755[...] letto dalla UI esiste nel dict demo:
    sweep anti-KeyError a render (lezione dello sweep chiavi demo vs UI)."""
    src = _leggi("w756_ui.py")
    usate = set(re.findall(r'_def755\["([^"]+)"\]', src))
    assert usate
    assert usate <= set(mh755_demo().keys())


def test_ui_riferisce_solo_helper_nuovi():
    src = _leggi("w756_ui.py")
    usati = set(re.findall(r'\b(mh\d+_\w+)\b', src))
    assert usati
    assert all(u.startswith("mh755_") for u in usati)


@pytest.mark.parametrize("wacc,vita,atteso", [
    (5.0, 20, 0.08024258719069129),
    (0, 20, 0.05),
    (10.0, 10, 0.16274539488251152),
    (5.0, 1, 1.05),
    (50.0, 5, 0.5758293838862559),
])
def test_crf_parametrizzato(wacc, vita, atteso):
    assert mh755_crf(wacc, vita) == pytest.approx(atteso)


@pytest.mark.parametrize("campo,valore", [
    ("produzione_t_anno", 0), ("produzione_t_anno", -3),
    ("kwh_per_t", 0), ("kwh_per_t", -10),
    ("prezzo_el_eur_kwh", -0.01),
    ("prezzo_rottame_eur_t", -1),
    ("altri_var_eur_t", -1),
    ("om_fisso_eur_anno", -100),
    ("costo_bf_eur_t", -1), ("capex_eur", -1),
    ("f_eaf_t_per_t", -0.10), ("f_bf_t_per_t", -0.10),
    ("wacc_pct", -0.1), ("wacc_pct", 50.1),
    ("vita_anni", -1), ("vita_anni", 2.5),
    ("tolleranza_pct", -1), ("tolleranza_pct", 100.1),
])
def test_valida_rifiuta_singoli_campi(campo, valore):
    d = _demo_kwargs()
    d[campo] = valore
    assert mh755_valida(**d)["valido"] is False


def test_df_tabella_valori_demo_selezionati():
    bc = demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Produzione (t/anno)"] == 500000.0
    assert mappa["Energia elettrica (MWh_e/anno)"] == 200000.0
    assert mappa["Risparmio (EUR/anno)"] == 39000000.0
    assert mappa["Payback (anni)"] == 8
    assert mappa["Verdetto"] == "CONVIENTE"


def test_lco_eaf_minore_di_lco_bf_demo():
    bc = demo_calcoli()
    assert bc["lco_eaf_eur_t"] < bc["lco_bf_eur_t"]
    assert bc["lco_bf_eur_t"] - bc["lco_eaf_eur_t"] == pytest.approx(
        29.8544476855852)
