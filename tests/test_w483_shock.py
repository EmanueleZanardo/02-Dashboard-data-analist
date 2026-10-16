"""Test tab483 '🧪💥 Shock di curva: P&L del portafoglio sotto scenari di prezzo'.

Demo (stesse 3 linee di tab481/tab482, data di valutazione 2026-10-15):
  1. TTF gas 2026-11 100k long  95->92 : MtM -300'000, DV01 +100'000, 46 gg  -> "31–90 gg"
  2. Power baseload DE 2026-12 50k short 110->108: MtM +100'000, DV01 -50'000, 77 gg -> "31–90 gg"
  3. CO2 EUA 2027-01 200k long  78->80 : MtM +400'000, DV01 +200'000, 108 gg -> "91–180 gg"
MtM tot +200'000; DV01 tot +250'000.
Parallelo +10: delta_tot +2'500'000; stress_tot +2'700'000.
  bucket "31–90 gg": mtm -200'000, dv01 +50'000, delta +500'000, stress +300'000.
  bucket "91–180 gg": mtm +400'000, dv01 +200'000, delta +2'000'000, stress +2'400'000.
Ripida: delta = 50'000*5 + 200'000*0 = +250'000. Inversione: -250'000.
Stress gas +25: delta = +6'250'000.
Verdetto demo (parallelo +10): ratio 2.5M/200k = 12.5 -> CRITICO, peggiore "91–180 gg".
"""

import math
import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh483_num", "mh483_segno", "mh483_mese", "mh483_fine_mese",
           "mh483_giorni", "mh483_bucket", "mh483_posizione",
           "mh483_preset_shock", "mh483_scenario", "mh483_verdetto",
           "_mh483_buckets")

BUCKETS = ["≤30 gg", "31–90 gg", "91–180 gg", "181–365 gg", ">365 gg"]

TITLE483 = "🧪💥 Shock di curva: P&L del portafoglio sotto scenari di prezzo"

DVAL = date(2026, 10, 15)

POS_DEMO = [
    {"commodity": "TTF gas", "scadenza": "2026-11",
     "volume_mwh": 100000.0, "segno": 1.0, "f_fix": 95.00, "f_now": 92.00},
    {"commodity": "Power baseload DE", "scadenza": "2026-12",
     "volume_mwh": 50000.0, "segno": -1.0, "f_fix": 110.00, "f_now": 108.00},
    {"commodity": "CO2 EUA", "scadenza": "2027-01",
     "volume_mwh": 200000.0, "segno": 1.0, "f_fix": 78.00, "f_now": 80.00},
]


def _approx(a, b):
    assert math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-6), f"{a} != {b}"


# ---------- mh483_num ----------

def test_num_ok():
    assert _F["mh483_num"](3, "x") == 3.0
    assert _F["mh483_num"](-2.5, "x") == -2.5


@pytest.mark.parametrize("bad", [True, "5", None, float("nan"), float("inf")])
def test_num_ko(bad):
    with pytest.raises(ValueError):
        _F["mh483_num"](bad, "x")


# ---------- mh483_segno ----------

def test_segno():
    assert _F["mh483_segno"]("long") == 1.0
    assert _F["mh483_segno"]("SHORT") == -1.0
    assert _F["mh483_segno"](1.0) == 1.0
    assert _F["mh483_segno"](-1.0) == -1.0


@pytest.mark.parametrize("bad", [0.0, 2.0, "x", "", None])
def test_segno_ko(bad):
    with pytest.raises(ValueError):
        _F["mh483_segno"](bad)


# ---------- mese / fine_mese / giorni / bucket ----------

def test_mese():
    assert _F["mh483_mese"]("2026-11") == (2026, 11)
    assert _F["mh483_mese"](" 2027-01 ") == (2027, 1)


@pytest.mark.parametrize("bad", ["2026-13", "2026-00", "2026", "11-2026",
                                 "2026-1", "", None])
def test_mese_ko(bad):
    with pytest.raises(ValueError):
        _F["mh483_mese"](bad)


def test_fine_mese():
    assert _F["mh483_fine_mese"](2026, 2) == date(2026, 2, 28)
    assert _F["mh483_fine_mese"](2024, 2) == date(2024, 2, 29)  # bisestile
    assert _F["mh483_fine_mese"](2026, 11) == date(2026, 11, 30)
    with pytest.raises(ValueError):
        _F["mh483_fine_mese"](2026, 13)


def test_giorni_demo():
    g = _F["mh483_giorni"]
    assert g(DVAL, "2026-11") == 46
    assert g(DVAL, "2026-12") == 77
    assert g(DVAL, "2027-01") == 108


def test_giorni_scorso():
    with pytest.raises(ValueError):
        _F["mh483_giorni"](DVAL, "2026-09")


@pytest.mark.parametrize("gg,exp", [(0, "≤30 gg"), (30, "≤30 gg"),
                                    (31, "31–90 gg"), (90, "31–90 gg"),
                                    (91, "91–180 gg"), (180, "91–180 gg"),
                                    (181, "181–365 gg"), (365, "181–365 gg"),
                                    (366, ">365 gg"), (730, ">365 gg")])
def test_bucket_confini(gg, exp):
    assert _F["mh483_bucket"](gg) == exp


def test_bucket_ko():
    with pytest.raises(ValueError):
        _F["mh483_bucket"](-1)


# ---------- mh483_posizione ----------

def test_posizione_demo():
    p = _F["mh483_posizione"]("TTF gas", "2026-11", 100000.0, 1.0, 95.0, 92.0)
    _approx(p["mtm"], -300000.0)
    _approx(p["dv01"], 100000.0)
    p2 = _F["mh483_posizione"]("Power", "2026-12", 50000.0, -1.0, 110.0, 108.0)
    _approx(p2["mtm"], 100000.0)
    _approx(p2["dv01"], -50000.0)


@pytest.mark.parametrize("kw", [{"volume_mwh": -1.0}, {"f_fix": -1.0},
                                {"f_now": -1.0}, {"segno": 0.0},
                                {"scadenza": "2026-13"}])
def test_posizione_ko(kw):
    base = {"commodity": "X", "scadenza": "2026-11", "volume_mwh": 1.0,
            "segno": 1.0, "f_fix": 1.0, "f_now": 1.0}
    base.update(kw)
    with pytest.raises(ValueError):
        _F["mh483_posizione"](**base)


# ---------- preset ----------

def test_preset_parallelo():
    p = _F["mh483_preset_shock"]("📐 Parallelo +10 €/MWh")
    assert set(p) == set(BUCKETS)
    assert all(v == 10.0 for v in p.values())
    n = _F["mh483_preset_shock"]("📐 Parallelo −10 €/MWh")
    assert all(v == -10.0 for v in n.values())


def test_preset_ripida_inversione():
    r = _F["mh483_preset_shock"]("📈 Ripida (front +10, back −10)")
    assert r == {"≤30 gg": 10.0, "31–90 gg": 5.0, "91–180 gg": 0.0,
                 "181–365 gg": -5.0, ">365 gg": -10.0}
    i = _F["mh483_preset_shock"]("📉 Inversione (front −10, back +10)")
    assert i["≤30 gg"] == -10.0 and i[">365 gg"] == 10.0
    assert i["31–90 gg"] == -r["31–90 gg"]


def test_preset_stress_gas():
    g = _F["mh483_preset_shock"]("🔥 Stress gas +25 €/MWh")
    assert all(v == 25.0 for v in g.values())


def test_preset_ko():
    with pytest.raises(ValueError):
        _F["mh483_preset_shock"]("boh")


# ---------- mh483_scenario ----------

def test_scenario_parallelo_demo():
    s = _F["mh483_scenario"](POS_DEMO, DVAL,
                             _F["mh483_preset_shock"]("📐 Parallelo +10 €/MWh"))
    _approx(s["mtm_tot"], 200000.0)
    _approx(s["delta_tot"], 2500000.0)
    _approx(s["mtm_stress_tot"], 2700000.0)
    _approx(s["dv01_tot"], 250000.0)
    pb = s["per_bucket"]
    _approx(pb["31–90 gg"]["mtm"], -200000.0)
    _approx(pb["31–90 gg"]["dv01"], 50000.0)
    _approx(pb["31–90 gg"]["delta"], 500000.0)
    _approx(pb["31–90 gg"]["mtm_stress"], 300000.0)
    _approx(pb["91–180 gg"]["delta"], 2000000.0)
    _approx(pb["91–180 gg"]["mtm_stress"], 2400000.0)
    assert pb["≤30 gg"]["n"] == 0
    _approx(pb["≤30 gg"]["delta"], 0.0)
    # coerenza riga per riga
    for r in s["righe"]:
        _approx(r["delta"], r["dv01"] * r["shift"])
        _approx(r["mtm_stress"], r["mtm"] + r["delta"])


def test_scenario_altri_preset():
    r = _F["mh483_scenario"](POS_DEMO, DVAL,
                             _F["mh483_preset_shock"]("📈 Ripida (front +10, back −10)"))
    _approx(r["delta_tot"], 250000.0)
    i = _F["mh483_scenario"](POS_DEMO, DVAL,
                             _F["mh483_preset_shock"]("📉 Inversione (front −10, back +10)"))
    _approx(i["delta_tot"], -250000.0)
    g = _F["mh483_scenario"](POS_DEMO, DVAL,
                             _F["mh483_preset_shock"]("🔥 Stress gas +25 €/MWh"))
    _approx(g["delta_tot"], 6250000.0)


def test_scenario_shift_mancanti_zero():
    s = _F["mh483_scenario"](POS_DEMO, DVAL, {})
    _approx(s["delta_tot"], 0.0)
    _approx(s["mtm_stress_tot"], s["mtm_tot"])


def test_scenario_ko():
    with pytest.raises(ValueError):
        _F["mh483_scenario"]([], DVAL, {})
    with pytest.raises(ValueError):
        _F["mh483_scenario"](POS_DEMO, DVAL, "non-dict")


# ---------- mh483_verdetto ----------

def _pb(delta_b):
    pb = {b: {"mtm": 0.0, "dv01": 0.0, "delta": 0.0,
              "mtm_stress": 0.0, "n": 0} for b in BUCKETS}
    for b, d in delta_b.items():
        pb[b]["delta"] = d
    return pb


def test_verdetto_demo_critico():
    s = _F["mh483_scenario"](POS_DEMO, DVAL,
                             _F["mh483_preset_shock"]("📐 Parallelo +10 €/MWh"))
    v = _F["mh483_verdetto"](s["delta_tot"], s["per_bucket"], s["mtm_tot"])
    assert v["verdetto"] == "CRITICO"
    _approx(v["ratio"], 12.5)
    assert v["bucket_peggiore"] == "91–180 gg"
    _approx(v["delta_peggiore"], 2000000.0)


def test_verdetto_rami():
    v = _F["mh483_verdetto"](10000.0, _pb({"≤30 gg": 10000.0}), 200000.0)
    assert v["verdetto"] == "RESILIENTE"  # 5% esatto -> RESILIENTE
    v = _F["mh483_verdetto"](40000.0, _pb({"31–90 gg": 40000.0}), 200000.0)
    assert v["verdetto"] == "DA GESTIRE"  # 20%
    v = _F["mh483_verdetto"](-60000.0, _pb({">365 gg": -60000.0}), 200000.0)
    assert v["verdetto"] == "CRITICO"  # 30%


def test_verdetto_base_dv01_se_mtm_zero():
    # posizione con f_fix == f_now: MtM 0, DV01 +100k, shift +10 -> delta 1M
    s = _F["mh483_scenario"](
        [{"commodity": "X", "scadenza": "2026-11", "volume_mwh": 100000.0,
          "segno": 1.0, "f_fix": 90.0, "f_now": 90.0}], DVAL,
        {"≤30 gg": 0.0, "31–90 gg": 10.0, "91–180 gg": 0.0,
         "181–365 gg": 0.0, ">365 gg": 0.0})
    _approx(s["mtm_tot"], 0.0)
    v = _F["mh483_verdetto"](s["delta_tot"], s["per_bucket"], s["mtm_tot"])
    _approx(v["base"], 100000.0)
    assert v["verdetto"] == "CRITICO"


def test_verdetto_portafoglio_vuoto():
    with pytest.raises(ValueError):
        _F["mh483_verdetto"](0.0, _pb({}), 0.0)


# ---------- registry ----------

def test_registry_titolo_e_tab():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(
        encoding="utf-8")
    assert TITLE483 in src
    # commento header W483 + lista titoli + H1 nella UI
    assert src.count(TITLE483) == 3
    assert "tab482, tab483, tab484, tab485, tab486, tab487, tab488, tab489, tab490, tab491, tab492, tab493, tab494, tab495, tab496, tab497, tab498, tab499, tab500, tab501, tab502, tab503 = st.tabs([" in src
    assert "    with tab483:" in src


def test_chiavi_st483_uniche():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(
        encoding="utf-8")
    import re
    keys = re.findall(r'key="(st483_[^"]+)"', src) + re.findall(
        r'key=f"(st483_[^"]+)"', src)
    assert len(keys) >= 10
    assert len(keys) == len(set(keys)), "chiavi st483_* duplicate"
