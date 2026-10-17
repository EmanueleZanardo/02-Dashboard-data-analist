"""Test tab482 '🗓️ Ladder delle scadenze: profilo temporale di volumi, MtM e DV01': registry + funzioni pure."""

import math
import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh482_num", "mh482_segno", "mh482_mese", "mh482_fine_mese",
           "mh482_giorni", "mh482_bucket", "mh482_posizione",
           "mh482_aggregazione", "mh482_verdetto")

TITLE482 = "🗓️ Ladder delle scadenze: profilo temporale di volumi, MtM e DV01"
TITLE481 = "📏 DV01 del portafoglio forward: sensibilità del MtM a uno shift parallelo della curva"

DVAL = date(2026, 10, 15)

# Demo (stesse 3 linee di tab481, data di valutazione 2026-10-15):
#   1. TTF gas 2026-11 100k long  95->92 : MtM -300'000, DV01 +100'000, 46 gg  -> "31–90 gg"
#   2. Power DE 2026-12 50k short 110->108: MtM +100'000, DV01 -50'000, 77 gg  -> "31–90 gg"
#   3. CO2 EUA 2027-01 200k long  78->80 : MtM +400'000, DV01 +200'000, 108 gg -> "91–180 gg"
# MtM totale +200'000; DV01 totale +250'000; tot_vol 350'000.
# duration_gg = 30'050'000/350'000 = 85.857142857; quota_90 = 150'000/350'000 = 0.428571.
# Dominante per |DV01|: 2027-01, concentrazione 200'000/350'000 = 0.571428571.
POS_DEMO = [
    {"commodity": "TTF gas", "scadenza": "2026-11",
     "volume_mwh": 100000.0, "segno": 1.0, "f_fix": 95.00, "f_now": 92.00},
    {"commodity": "Power baseload DE", "scadenza": "2026-12",
     "volume_mwh": 50000.0, "segno": -1.0, "f_fix": 110.00, "f_now": 108.00},
    {"commodity": "CO2 EUA", "scadenza": "2027-01",
     "volume_mwh": 200000.0, "segno": 1.0, "f_fix": 78.00, "f_now": 80.00},
]
MTM_DEMO = 200000.0
DV01_DEMO = 250000.0
DUR_GG_DEMO = 30050000.0 / 350000.0
QUOTA90_DEMO = 150000.0 / 350000.0
CONC_DEMO = 200000.0 / 350000.0


class TestRegistry482:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"    with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 526

    def test_ultima_tab(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert TITLE482 in titoli
        assert TITLE481 in titoli
        assert "tab482" in dvars

    def test_ui_indentata(self):
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        assert "    with tab482:" in src


class TestNum482:
    def test_ok(self):
        assert _F["mh482_num"](3.5, "x") == 3.5
        assert _F["mh482_num"](7, "x") == 7.0

    def test_bool_rifiutato(self):
        with pytest.raises(ValueError):
            _F["mh482_num"](True, "x")

    def test_nan_inf_rifiutati(self):
        with pytest.raises(ValueError):
            _F["mh482_num"](float("nan"), "x")
        with pytest.raises(ValueError):
            _F["mh482_num"](float("inf"), "x")

    def test_stringa_rifiutata(self):
        with pytest.raises(ValueError):
            _F["mh482_num"]("3.5", "x")


class TestSegnoMese482:
    def test_segno_ok(self):
        assert _F["mh482_segno"](1.0, "s") == 1.0
        assert _F["mh482_segno"](-1.0, "s") == -1.0

    def test_segno_invalido(self):
        with pytest.raises(ValueError):
            _F["mh482_segno"](0.0, "s")
        with pytest.raises(ValueError):
            _F["mh482_segno"](2.0, "s")

    def test_mese_ok(self):
        assert _F["mh482_mese"]("2026-11", "m") == "2026-11"
        assert _F["mh482_mese"]("2030-01", "m") == "2030-01"

    def test_mese_invalido(self):
        for bad in ["2026-13", "2026-00", "26-11", "2026/11", "2026-1", 202611, None]:
            with pytest.raises(ValueError):
                _F["mh482_mese"](bad, "m")


class TestFineMeseGiorni482:
    def test_fine_mese(self):
        assert _F["mh482_fine_mese"]("2026-11") == date(2026, 11, 30)
        assert _F["mh482_fine_mese"]("2026-12") == date(2026, 12, 31)
        assert _F["mh482_fine_mese"]("2027-02") == date(2027, 2, 28)

    def test_fine_mese_bisestile(self):
        assert _F["mh482_fine_mese"]("2028-02") == date(2028, 2, 29)

    def test_fine_mese_invalido(self):
        with pytest.raises(ValueError):
            _F["mh482_fine_mese"]("2026-13")

    def test_giorni(self):
        assert _F["mh482_giorni"]("2026-11", DVAL) == 46
        assert _F["mh482_giorni"]("2026-12", DVAL) == 77
        assert _F["mh482_giorni"]("2027-01", DVAL) == 108
        assert _F["mh482_giorni"]("2026-10", DVAL) == 16

    def test_giorni_passata(self):
        with pytest.raises(ValueError):
            _F["mh482_giorni"]("2026-09", DVAL)

    def test_giorni_data_invalida(self):
        with pytest.raises(ValueError):
            _F["mh482_giorni"]("2026-11", "2026-10-15")
        with pytest.raises(ValueError):
            _F["mh482_giorni"]("2026-11", None)


class TestBucket482:
    @pytest.mark.parametrize("g,atteso", [
        (0, "≤ 30 gg"), (30, "≤ 30 gg"),
        (31, "31–90 gg"), (90, "31–90 gg"),
        (91, "91–180 gg"), (180, "91–180 gg"),
        (181, "181–365 gg"), (365, "181–365 gg"),
        (366, "> 365 gg"), (1000, "> 365 gg"),
    ])
    def test_soglie(self, g, atteso):
        assert _F["mh482_bucket"](g) == atteso

    def test_rifiuti(self):
        for bad in [-1, 30.5, True, "90", None]:
            with pytest.raises(ValueError):
                _F["mh482_bucket"](bad)


class TestPosizione482:
    def test_arricchimento(self):
        r = _F["mh482_posizione"](POS_DEMO[0], 0, DVAL)
        assert r["giorni"] == 46
        assert r["bucket"] == "31–90 gg"
        assert r["mtm"] == -300000.0
        assert r["dv01"] == 100000.0
        assert r["commodity"] == "TTF gas"

    def test_errori(self):
        base = dict(POS_DEMO[0])
        for k, v in [("volume_mwh", -1.0), ("segno", 0.0),
                     ("f_fix", "x"), ("scadenza", "2026-13"),
                     ("scadenza", "2026-09")]:
            bad = dict(base)
            bad[k] = v
            with pytest.raises(ValueError):
                _F["mh482_posizione"](bad, 0, DVAL)


class TestAggregazione482:
    def test_demo(self):
        a = _F["mh482_aggregazione"](POS_DEMO, DVAL)
        assert a["n_posizioni"] == 3
        assert abs(a["mtm_totale"] - MTM_DEMO) < 1e-9
        assert abs(a["dv01_totale"] - DV01_DEMO) < 1e-9
        assert abs(a["tot_vol"] - 350000.0) < 1e-9
        assert abs(a["duration_gg"] - DUR_GG_DEMO) < 1e-9
        assert abs(a["duration_mesi"] - DUR_GG_DEMO / 30.44) < 1e-9
        assert abs(a["quota_90"] - QUOTA90_DEMO) < 1e-12
        assert a["quota_365"] == 0.0
        assert a["scadenza_dominante"] == "2027-01"

    def test_bucket(self):
        a = _F["mh482_aggregazione"](POS_DEMO, DVAL)
        pb = a["per_bucket"]
        b = pb["31–90 gg"]
        assert b["vol_long"] == 100000.0
        assert b["vol_short"] == 50000.0
        assert b["vol_net"] == 50000.0
        assert abs(b["mtm"] - (-200000.0)) < 1e-9
        assert abs(b["dv01"] - 50000.0) < 1e-9
        b2 = pb["91–180 gg"]
        assert b2["vol_long"] == 200000.0
        assert b2["vol_short"] == 0.0
        assert abs(b2["mtm"] - 400000.0) < 1e-9
        assert abs(b2["dv01"] - 200000.0) < 1e-9
        for vuoto in ("≤ 30 gg", "181–365 gg", "> 365 gg"):
            assert pb[vuoto]["vol_long"] == 0.0
            assert pb[vuoto]["mtm"] == 0.0

    def test_ordine_bucket(self):
        a = _F["mh482_aggregazione"](POS_DEMO, DVAL)
        assert list(a["per_bucket"].keys()) == [
            "≤ 30 gg", "31–90 gg", "91–180 gg", "181–365 gg", "> 365 gg"]

    def test_vuota(self):
        with pytest.raises(ValueError):
            _F["mh482_aggregazione"]([], DVAL)

    def test_volumi_nulli(self):
        z = [dict(POS_DEMO[0], volume_mwh=0.0)]
        with pytest.raises(ValueError):
            _F["mh482_aggregazione"](z, DVAL)

    def test_singola_riga(self):
        a = _F["mh482_aggregazione"]([POS_DEMO[2]], DVAL)
        assert a["duration_gg"] == 108.0
        assert a["quota_90"] == 0.0
        assert abs(a["mtm_totale"] - 400000.0) < 1e-9


class TestVerdetto482:
    def test_demo_distribuito(self):
        a = _F["mh482_aggregazione"](POS_DEMO, DVAL)
        v = _F["mh482_verdetto"](a)
        assert v["verdetto"] == "DISTRIBUITO"
        assert abs(v["quota_90"] - QUOTA90_DEMO) < 1e-12
        assert v["quota_365"] == 0.0
        assert v["scadenza_dominante"] == "2027-01"
        assert abs(v["concentrazione"] - CONC_DEMO) < 1e-12

    def test_front_loaded(self):
        pos = [
            {"commodity": "TTF gas", "scadenza": "2026-11",
             "volume_mwh": 80000.0, "segno": 1.0, "f_fix": 90.0, "f_now": 90.0},
            {"commodity": "TTF gas", "scadenza": "2027-06",
             "volume_mwh": 20000.0, "segno": 1.0, "f_fix": 90.0, "f_now": 90.0},
        ]
        a = _F["mh482_aggregazione"](pos, DVAL)
        assert abs(a["quota_90"] - 0.8) < 1e-12
        assert _F["mh482_verdetto"](a)["verdetto"] == "FRONT-LOADED"

    def test_back_loaded(self):
        pos = [
            {"commodity": "TTF gas", "scadenza": "2028-06",
             "volume_mwh": 70000.0, "segno": 1.0, "f_fix": 90.0, "f_now": 90.0},
            {"commodity": "TTF gas", "scadenza": "2026-11",
             "volume_mwh": 30000.0, "segno": 1.0, "f_fix": 90.0, "f_now": 90.0},
        ]
        a = _F["mh482_aggregazione"](pos, DVAL)
        assert abs(a["quota_365"] - 0.7) < 1e-12
        assert _F["mh482_verdetto"](a)["verdetto"] == "BACK-LOADED"

    def test_soglia_inclusiva_front(self):
        pos = [
            {"commodity": "TTF gas", "scadenza": "2026-11",
             "volume_mwh": 60000.0, "segno": 1.0, "f_fix": 90.0, "f_now": 90.0},
            {"commodity": "TTF gas", "scadenza": "2027-06",
             "volume_mwh": 40000.0, "segno": 1.0, "f_fix": 90.0, "f_now": 90.0},
        ]
        a = _F["mh482_aggregazione"](pos, DVAL)
        assert abs(a["quota_90"] - 0.6) < 1e-12
        assert _F["mh482_verdetto"](a)["verdetto"] == "FRONT-LOADED"

    def test_malformato(self):
        with pytest.raises(ValueError):
            _F["mh482_verdetto"]({})
        with pytest.raises(ValueError):
            _F["mh482_verdetto"](None)


class TestUi482:
    def test_chiavi_482(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        fkeys = re.findall(r'key=f"st482_\w+\{', src)
        assert len(fkeys) == 6, fkeys
        expl = re.findall(r'key="st482_[^"]+"', src)
        assert expl == ['key="st482_data"', 'key="st482_csv"'], expl

    def test_chiavi_univoche(self):
        import re
        from collections import Counter
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        keys = re.findall(r'key=(f?"st482_[^"]+")', src)
        # le f-string con {_i482} generano 3 chiavi distinte a runtime:
        # verifico solo che i template non si ripetano
        assert len(keys) == len(set(keys)) == 8, keys
