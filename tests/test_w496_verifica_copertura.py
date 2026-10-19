"""Test tab496 '📊✅ Verifica della copertura: il piano ha funzionato?': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh496_num", "mh496_segno", "mh496_mese", "mh496_z",
           "mh496_phi", "mh496_Phi", "mh496_lambda",
           "mh496_mult", "mh496_limite", "mh496_fill", "mh496_f_exec",
           "mh496_n_tranche", "mh496_spread_bps", "mh496_adv", "mh496_k_imp",
           "mh496_lato", "mh496_riga", "mh496_portafoglio",
           "mh496_hedge_frac", "mh496_piano",
           "mh496_costo_spread", "mh496_costo_impatto",
           "mh496_verdetto", "mh496_verifica")

TITLE496 = "📊✅ Verifica della copertura: il piano ha funzionato?"
TITLE495 = "🛡️📋 Esecuzione della copertura: il piano ordini"

Z99 = 2.3263478740408408
LAMBDA99 = 2.665214220345806

# Demo (stessi numeri tab491/tab492/tab493/tab494/tab495): 3 linee, z 99%,
# stress x2, limite 3M EUR, 5 tranche, k=0.10.
POS_B = [
    {"commodity": "TTF gas", "scadenza": "2027-01",
     "volume_mwh": 100000.0, "segno": 1.0, "f_fix": 95.00,
     "f_now": 88.00, "sigma_pct": 2.5},
    {"commodity": "TTF gas", "scadenza": "2026-12",
     "volume_mwh": 50000.0, "segno": -1.0, "f_fix": 91.00,
     "f_now": 90.00, "sigma_pct": 2.5},
    {"commodity": "Power baseload DE", "scadenza": "2027-03",
     "volume_mwh": 200000.0, "segno": 1.0, "f_fix": 110.00,
     "f_now": 116.00, "sigma_pct": 1.8},
]
LIMITE_B = 3000000.0
ES_STRESS_B = 3998354.3733627778
HEDGE_FRAC_B = 0.2496913180116952
PLAN_B = [24969.13180116952, 12484.56590058476, 49938.26360233904]
FEXEC_B = [88.00, 90.00, 116.00]
SPR_B = {"TTF gas": 4.0, "Power baseload DE": 6.0,
         "Power baseload IT": 10.0, "CO2 EUA": 8.0}
ADV_B = {"TTF gas": 8000000.0, "Power baseload DE": 5000000.0,
         "Power baseload IT": 2000000.0, "CO2 EUA": 1500000.0}
CS_B = 2402.0305
CI_B = 33365.2354
CTOT_B = 35767.2658
# meta' fill -> efficacia 0.5, es residuo noto
ES_RES_HALF_B = 3499177.186681389


def _righe():
    return [_F["mh496_riga"](p["commodity"], p["scadenza"], p["volume_mwh"],
                             p["segno"], p["f_fix"], p["f_now"],
                             p["sigma_pct"]) for p in POS_B]


def _verifica_full():
    return _F["mh496_verifica"](_righe(), Z99, 2.0, LIMITE_B, list(PLAN_B),
                                list(FEXEC_B), SPR_B, ADV_B, 5, 0.10, CTOT_B)


def test_registry_tab496():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text()
    assert f'"{TITLE496}"' in src
    assert src.count(TITLE496) == 3
    assert "tab496, tab497, tab498, tab499, tab500, tab501, tab502, tab503, tab504, tab505, tab506, tab507, tab508, tab509, tab510, tab511, tab512, tab513, tab514, tab515, tab516, tab517, tab518, tab519, tab520, tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562 = st.tabs([" in src
    assert "    with tab496:" in src
    # ordine: tab496 dopo tab495 nella dichiarazione delle tab
    _decl496 = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    assert _decl496.index(f'"{TITLE495}"') < _decl496.index(f'"{TITLE496}"')


def test_chiavi_st496_uniche():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text()
    import re
    keys = re.findall(r'key="(st496_[^"]+)"', src) + re.findall(
        r'key=f"(st496_[^"]+)"', src)
    assert len(keys) == len(set(keys)) > 10


def test_lambda99():
    assert _F["mh496_lambda"](Z99) == pytest.approx(LAMBDA99, rel=1e-12)


def test_portafoglio_demo():
    pf = _F["mh496_portafoglio"](_righe(), Z99, 2.0)
    assert pf["es_stress_cons"] == pytest.approx(ES_STRESS_B, rel=1e-9)
    assert pf["n"] == 3


def test_piano_demo():
    p = _F["mh496_piano"](_righe(), Z99, 2.0, LIMITE_B)
    assert p["hedge_frac"] == pytest.approx(HEDGE_FRAC_B, rel=1e-9)
    assert p["es_stress"] == pytest.approx(ES_STRESS_B, rel=1e-9)
    for got, exp in zip(p["hedge_mwh_plan"], PLAN_B):
        assert got == pytest.approx(exp, rel=1e-9)
    # piano eseguito alla lettera -> residuo = limite
    assert p["es_residuo_plan"] == pytest.approx(LIMITE_B, rel=1e-9)
    assert p["rischio_salvato_plan"] == pytest.approx(ES_STRESS_B - LIMITE_B,
                                                     rel=1e-9)


def test_verifica_fill_piene_rientro():
    v = _verifica_full()
    assert v["verdetto"]["codice"] == "RIENTRO"
    assert v["es_residuo_real"] == pytest.approx(LIMITE_B, rel=1e-9)
    assert v["gap"] == pytest.approx(0.0, abs=1e-6)
    assert v["efficacia"] == pytest.approx(1.0, rel=1e-9)
    assert v["fill_ratio_tot"] == pytest.approx(1.0, rel=1e-9)
    assert all(r["fill_ratio"] == pytest.approx(1.0, rel=1e-9)
               for r in v["righe_verifica"])
    assert [r["lato"] for r in v["righe_verifica"]] == ["vendi", "compra",
                                                       "vendi"]


def test_verifica_costi_fill_piene():
    v = _verifica_full()
    assert v["costo_spread_tot"] == pytest.approx(CS_B, rel=1e-6)
    assert v["costo_impatto_tot"] == pytest.approx(CI_B, rel=1e-6)
    assert v["costo_totale"] == pytest.approx(CTOT_B, rel=1e-6)
    assert v["aderenza_budget"] == pytest.approx(1.0, rel=1e-6)


def test_verifica_fill_meta_fuori():
    v = _F["mh496_verifica"](_righe(), Z99, 2.0, LIMITE_B,
                             [p / 2.0 for p in PLAN_B], list(FEXEC_B),
                             SPR_B, ADV_B, 5, 0.10, CTOT_B)
    assert v["verdetto"]["codice"] == "FUORI"
    assert v["es_residuo_real"] == pytest.approx(ES_RES_HALF_B, rel=1e-9)
    assert v["efficacia"] == pytest.approx(0.5, rel=1e-9)
    assert v["fill_ratio_tot"] == pytest.approx(0.5, rel=1e-9)


def test_verifica_fill_zero():
    v = _F["mh496_verifica"](_righe(), Z99, 2.0, LIMITE_B,
                             [0.0, 0.0, 0.0], list(FEXEC_B),
                             SPR_B, ADV_B, 5, 0.10, CTOT_B)
    assert v["verdetto"]["codice"] == "FUORI"
    # niente eseguito: residuo = ES stressato intero
    assert v["es_residuo_real"] == pytest.approx(ES_STRESS_B, rel=1e-9)
    assert v["costo_totale"] == 0.0
    assert v["efficacia"] == pytest.approx(0.0, rel=1e-9)


def test_verifica_sovrafill_cappata():
    # fill 150% del piano: la frazione hedge reale si capta a 1.0
    v = _F["mh496_verifica"](_righe(), Z99, 2.0, LIMITE_B,
                             [p * 1.5 for p in PLAN_B], list(FEXEC_B),
                             SPR_B, ADV_B, 5, 0.10, CTOT_B)
    for r in v["righe_verifica"]:
        assert r["hedge_frac_real"] <= 1.0
    assert v["verdetto"]["codice"] == "RIENTRO"


def test_verdetto_soglie():
    f = _F["mh496_verdetto"]
    assert f(LIMITE_B, LIMITE_B)["codice"] == "RIENTRO"
    assert f(LIMITE_B * 1.04, LIMITE_B)["codice"] == "MARGINALE"
    assert f(LIMITE_B * 1.05, LIMITE_B)["codice"] == "MARGINALE"
    assert f(LIMITE_B * 1.06, LIMITE_B)["codice"] == "FUORI"
    assert f(ES_STRESS_B, LIMITE_B)["codice"] == "FUORI"


def test_costo_impatto_scala_sqrt():
    # raddoppiare la q_giorno scala l'impatto di sqrt(2)
    c1 = _F["mh496_costo_impatto"](1e6, 1000.0, 1e6, 0.1)
    c2 = _F["mh496_costo_impatto"](1e6, 2000.0, 1e6, 0.1)
    assert c2 == pytest.approx(c1 * math.sqrt(2.0), rel=1e-12)
    assert _F["mh496_costo_impatto"](1e6, 1000.0, 1e6, 0.0) == 0.0
    assert _F["mh496_costo_spread"](1e6, 0.0) == 0.0


def test_validatori():
    f = _F
    with pytest.raises(ValueError):
        f["mh496_segno"](0.5, "segno")
    with pytest.raises(ValueError):
        f["mh496_mese"]("2027-13", "mese")
    with pytest.raises(ValueError):
        f["mh496_z"](0.9, "z")
    with pytest.raises(ValueError):
        f["mh496_mult"](11.0, "mult")
    with pytest.raises(ValueError):
        f["mh496_limite"](0.0, "limite")
    with pytest.raises(ValueError):
        f["mh496_fill"](-1.0, "fill")
    with pytest.raises(ValueError):
        f["mh496_f_exec"](-1.0, "f_exec")
    with pytest.raises(ValueError):
        f["mh496_n_tranche"](0, "n")
    with pytest.raises(ValueError):
        f["mh496_n_tranche"](2.5, "n")
    with pytest.raises(ValueError):
        f["mh496_spread_bps"](-1.0, "spread")
    with pytest.raises(ValueError):
        f["mh496_adv"](0.0, "adv")
    with pytest.raises(ValueError):
        f["mh496_k_imp"](-0.1, "k")
    with pytest.raises(ValueError):
        f["mh496_hedge_frac"](-5.0, 100.0)
    with pytest.raises(ValueError):
        f["mh496_verdetto"](-1.0, 100.0)
    with pytest.raises(ValueError):
        f["mh496_verifica"](_righe(), Z99, 2.0, LIMITE_B,
                            [1.0, 2.0], list(FEXEC_B), SPR_B, ADV_B, 5,
                            0.10, CTOT_B)
    with pytest.raises(ValueError):
        f["mh496_verifica"](_righe(), Z99, 2.0, LIMITE_B, list(PLAN_B),
                            list(FEXEC_B), SPR_B, ADV_B, 5, 0.10, -1.0)


def test_verifica_commodity_sconosciuta():
    with pytest.raises(ValueError):
        _F["mh496_verifica"](_righe(), Z99, 2.0, LIMITE_B, list(PLAN_B),
                             list(FEXEC_B), {"Altro": 4.0}, ADV_B, 5, 0.10,
                             CTOT_B)
