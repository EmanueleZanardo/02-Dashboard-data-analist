"""Test tab495 '🛡️📋 Esecuzione della copertura: il piano ordini': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh495_num", "mh495_segno", "mh495_mese", "mh495_z",
           "mh495_phi", "mh495_Phi", "mh495_lambda",
           "mh495_mult", "mh495_limite",
           "mh495_mtm_linea", "mh495_sigma_mtm_linea",
           "mh495_es_linea", "mh495_riga", "mh495_portafoglio",
           "mh495_hedge_frac", "mh495_pesi", "mh495_n_tranche",
           "mh495_spread_bps", "mh495_adv", "mh495_k_imp",
           "mh495_lato", "mh495_q_giorno",
           "mh495_costo_spread", "mh495_costo_impatto",
           "mh495_es_residuo", "mh495_piano", "mh495_verdetto")

TITLE495 = "🛡️📋 Esecuzione della copertura: il piano ordini"
TITLE494 = "🚨⏳ Monitoraggio dell'attesa: il trigger di escalation"

Z99 = 2.3263478740408408
LAMBDA99 = 2.665214220345806

# Demo (stessi numeri tab491/tab492/tab493/tab494): 3 linee, z 99%,
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
ES_BASE_B = 1999177.1866813889
ES_STRESS_B = 3998354.3733627778
HEDGE_FRAC_B = 0.2496913180116952
PESI_B = [0.2932942274363418, 0.14998000266631115, 0.556725769897347]
SPR_B = {"TTF gas": 4.0, "Power baseload DE": 6.0,
         "Power baseload IT": 10.0, "CO2 EUA": 8.0}
ADV_B = {"TTF gas": 8000000.0, "Power baseload DE": 5000000.0,
         "Power baseload IT": 2000000.0, "CO2 EUA": 1500000.0}
# per linea: (hedge_mwh, nozionale, q_giorno, costo_spread, costo_impatto)
LINEE_B = [
    (24969.1318, 2197283.5985, 4993.8264, 439.4567, 5489.8166),
    (12484.5659, 1123610.9311, 2496.9132, 224.7222, 1985.0556),
    (49938.2636, 5792838.5779, 9987.6527, 1737.8516, 25890.3631),
]
CS_B = 2402.0305
CI_B = 33365.2354
CTOT_B = 35767.2658
RS_B = 998354.3734
RC_B = 0.03582622


def _righe():
    return [_F["mh495_riga"](p["commodity"], p["scadenza"], p["volume_mwh"],
                             p["segno"], p["f_fix"], p["f_now"],
                             p["sigma_pct"]) for p in POS_B]


def _piano():
    return _F["mh495_piano"](_righe(), Z99, 2.0, LIMITE_B, 5,
                             SPR_B, ADV_B, 0.10)


def test_registry_tab495():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text()
    assert f'"{TITLE495}"' in src
    assert "tab494, tab495, tab496, tab497, tab498, tab499, tab500, tab501, tab502, tab503, tab504, tab505, tab506, tab507, tab508, tab509, tab510, tab511, tab512, tab513, tab514, tab515, tab516, tab517, tab518, tab519, tab520, tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561 = st.tabs([" in src
    assert "    with tab495:" in src
    # ordine: tab495 dopo tab494 nella dichiarazione delle tab
    # (confronto dentro la riga st.tabs, non nel file: i titoli compaiono
    # anche negli header dei blocchi helper W494/W495)
    _decl495 = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    assert _decl495.index(f'"{TITLE494}"') < _decl495.index(f'"{TITLE495}"')


def test_lambda99():
    assert _F["mh495_lambda"](Z99) == pytest.approx(LAMBDA99, rel=1e-12)


def test_portafoglio_demo():
    pf = _F["mh495_portafoglio"](_righe(), Z99, 2.0)
    assert pf["es_base_cons"] == pytest.approx(ES_BASE_B, rel=1e-9)
    assert pf["es_stress_cons"] == pytest.approx(ES_STRESS_B, rel=1e-9)
    assert pf["n"] == 3


def test_hedge_frac_demo():
    h = _F["mh495_hedge_frac"](ES_STRESS_B, LIMITE_B)
    assert h == pytest.approx(HEDGE_FRAC_B, rel=1e-9)
    # sotto il limite: nessun hedge
    assert _F["mh495_hedge_frac"](ES_STRESS_B, 5000000.0) == 0.0


def test_pesi_demo():
    pf = _F["mh495_portafoglio"](_righe(), Z99, 2.0)
    w = _F["mh495_pesi"](pf["es_linee_stress"])
    assert sum(w) == pytest.approx(1.0, rel=1e-12)
    for got, exp in zip(w, PESI_B):
        assert got == pytest.approx(exp, rel=1e-9)


def test_piano_demo_linee():
    p = _piano()
    assert p["hedge_frac"] == pytest.approx(HEDGE_FRAC_B, rel=1e-9)
    assert p["n_tranche"] == 5
    assert len(p["righe_piano"]) == 3
    for rp, exp in zip(p["righe_piano"], LINEE_B):
        assert rp["hedge_mwh"] == pytest.approx(exp[0], rel=1e-6)
        assert rp["nozionale_eur"] == pytest.approx(exp[1], rel=1e-6)
        assert rp["q_giorno_mwh"] == pytest.approx(exp[2], rel=1e-6)
        assert rp["costo_spread"] == pytest.approx(exp[3], rel=1e-6)
        assert rp["costo_impatto"] == pytest.approx(exp[4], rel=1e-6)
    assert [rp["lato"] for rp in p["righe_piano"]] == ["vendi", "compra",
                                                      "vendi"]


def test_piano_demo_totali():
    p = _piano()
    assert p["costo_spread_tot"] == pytest.approx(CS_B, rel=1e-6)
    assert p["costo_impatto_tot"] == pytest.approx(CI_B, rel=1e-6)
    assert p["costo_totale"] == pytest.approx(CTOT_B, rel=1e-6)
    assert p["rischio_salvato"] == pytest.approx(RS_B, rel=1e-9)
    assert p["rapporto_costo"] == pytest.approx(RC_B, rel=1e-6)
    # l'ES residuo coincide col limite (linearita', corr=1)
    assert p["es_residuo"] == pytest.approx(LIMITE_B, rel=1e-9)
    # tranche: 5 giorni x 3 linee, ogni giorno = q_giorno della linea
    assert len(p["tranche"]) == 5 and all(len(t) == 3 for t in p["tranche"])
    for t in p["tranche"]:
        for q, rp in zip(t, p["righe_piano"]):
            assert q == pytest.approx(rp["q_giorno_mwh"])


def test_verdetto_demo_sostenibile():
    v = _F["mh495_verdetto"](ES_STRESS_B, LIMITE_B, CTOT_B, RS_B)
    assert v["codice"] == "SOSTENIBILE"


def test_verdetto_soglie():
    f = _F["mh495_verdetto"]
    assert f(4000000.0, 3000000.0, 40000.0, 1000000.0)["codice"] == "SOSTENIBILE"
    assert f(4000000.0, 3000000.0, 100000.0, 1000000.0)["codice"] == "ELEVATO"
    assert f(4000000.0, 3000000.0, 200000.0, 1000000.0)["codice"] == "PROIBITIVO"
    assert f(2000000.0, 3000000.0, 0.0, 0.0)["codice"] == "NON_NECESSARIA"


def test_costo_impatto_scala_sqrt():
    # raddoppiare la q_giorno scala l'impatto di sqrt(2)
    c1 = _F["mh495_costo_impatto"](1e6, 1000.0, 1e6, 0.1)
    c2 = _F["mh495_costo_impatto"](1e6, 2000.0, 1e6, 0.1)
    assert c2 == pytest.approx(c1 * math.sqrt(2.0), rel=1e-12)
    # k=0 -> impatto nullo; spread nullo -> costo nullo
    assert _F["mh495_costo_impatto"](1e6, 1000.0, 1e6, 0.0) == 0.0
    assert _F["mh495_costo_spread"](1e6, 0.0) == 0.0


def test_validatori():
    f = _F
    with pytest.raises(ValueError):
        f["mh495_segno"](0.5, "segno")
    with pytest.raises(ValueError):
        f["mh495_mese"]("2027-13", "mese")
    with pytest.raises(ValueError):
        f["mh495_z"](0.9, "z")
    with pytest.raises(ValueError):
        f["mh495_mult"](11.0, "mult")
    with pytest.raises(ValueError):
        f["mh495_limite"](0.0, "limite")
    with pytest.raises(ValueError):
        f["mh495_n_tranche"](0, "n")
    with pytest.raises(ValueError):
        f["mh495_n_tranche"](2.5, "n")
    with pytest.raises(ValueError):
        f["mh495_spread_bps"](-1.0, "spread")
    with pytest.raises(ValueError):
        f["mh495_adv"](0.0, "adv")
    with pytest.raises(ValueError):
        f["mh495_k_imp"](-0.1, "k")
    with pytest.raises(ValueError):
        f["mh495_pesi"]([0.0, 0.0])
    with pytest.raises(ValueError):
        f["mh495_hedge_frac"](-5.0, 100.0)
    with pytest.raises(ValueError):
        f["mh495_es_residuo"](100.0, 1.5)
    with pytest.raises(ValueError):
        f["mh495_verdetto"](4000000.0, 3000000.0, -1.0, 1000000.0)


def test_piano_commodity_sconosciuta():
    righe = _righe()
    with pytest.raises(ValueError):
        _F["mh495_piano"](righe, Z99, 2.0, LIMITE_B, 5,
                          {"Altro": 4.0}, ADV_B, 0.10)
