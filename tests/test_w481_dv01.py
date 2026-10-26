"""Test tab481 '📏 DV01 del portafoglio forward: sensibilità del MtM a uno shift parallelo della curva': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh481_num", "mh481_segno", "mh481_mese", "mh481_posizione",
           "mh481_mtm_linea", "mh481_dv01_linea", "mh481_aggregazione",
           "mh481_scenario", "mh481_verdetto")

TITLE481 = "📏 DV01 del portafoglio forward: sensibilità del MtM a uno shift parallelo della curva"
TITLE482 = "🗓️ Ladder delle scadenze: profilo temporale di volumi, MtM e DV01"
TITLE480 = "📞 Margin call: variazione margine e buffer di liquidità"

# Demo A (singola): TTF gas 100'000 MWh long, 95.00 -> 92.00
#   MtM = 1 * (92-95) * 100'000 = -300'000 ; DV01 = +100'000
POS_A = {"commodity": "TTF gas", "scadenza": "2026-11",
         "volume_mwh": 100000.0, "segno": 1.0, "f_fix": 95.00, "f_now": 92.00}
MTM_A = -300000.0
DV01_A = 100000.0

# Demo B (portafoglio 3 linee, usato per aggregazione/scenario/verdetto):
#   1. TTF gas 2026-11 100k long  95->92 : MtM -300'000, DV01 +100'000
#   2. Power DE 2026-12 50k short 110->108: MtM +100'000, DV01  -50'000
#   3. TTF gas 2026-11  20k long  90->94 : MtM  +80'000, DV01  +20'000
# MtM totale -120'000; DV01 totale +70'000 (net LONG); dominanza 2026-11.
POS_B = [
    {"commodity": "TTF gas", "scadenza": "2026-11",
     "volume_mwh": 100000.0, "segno": 1.0, "f_fix": 95.00, "f_now": 92.00},
    {"commodity": "Power baseload DE", "scadenza": "2026-12",
     "volume_mwh": 50000.0, "segno": -1.0, "f_fix": 110.00, "f_now": 108.00},
    {"commodity": "TTF gas", "scadenza": "2026-11",
     "volume_mwh": 20000.0, "segno": 1.0, "f_fix": 90.00, "f_now": 94.00},
]
MTM_B = -120000.0
DV01_B = 70000.0
VERD_B = 'CONCENTRATO'
CONC_B = 0.7058823529411765
SCEN_B = [-820000.0, -470000.0, -190000.0, -50000.0, 230000.0, 580000.0]

# Demo C (ESPOSTO NETTO): due scadenze long, netto 100%, dominanza 0.588 < 0.6.
POS_C = [
    {"commodity": "TTF gas", "scadenza": "2026-11",
     "volume_mwh": 100000.0, "segno": 1.0, "f_fix": 95.00, "f_now": 92.00},
    {"commodity": "TTF gas", "scadenza": "2027-01",
     "volume_mwh": 70000.0, "segno": 1.0, "f_fix": 100.00, "f_now": 94.00},
]
VERD_C = 'ESPOSTO NETTO'
CONC_C = 0.5882352941176471

# Demo D (BILANCIATO): 100k long vs 95k short stessa scadenza.
POS_D = [
    {"commodity": "TTF gas", "scadenza": "2026-11",
     "volume_mwh": 100000.0, "segno": 1.0, "f_fix": 95.00, "f_now": 92.00},
    {"commodity": "TTF gas", "scadenza": "2026-11",
     "volume_mwh": 95000.0, "segno": -1.0, "f_fix": 95.00, "f_now": 92.00},
]
VERD_D = 'BILANCIATO'
MTM_D = -15000.0


class TestRegistry481:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"    with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 736

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


class TestNum481:
    def test_ok(self):
        assert _F["mh481_num"](3.5, "x") == 3.5
        assert _F["mh481_num"](7, "x") == 7.0

    def test_bool_rifiutato(self):
        with pytest.raises(ValueError):
            _F["mh481_num"](True, "x")

    def test_nan_inf_rifiutati(self):
        with pytest.raises(ValueError):
            _F["mh481_num"](float("nan"), "x")
        with pytest.raises(ValueError):
            _F["mh481_num"](float("inf"), "x")

    def test_stringa_rifiutata(self):
        with pytest.raises(ValueError):
            _F["mh481_num"]("3.5", "x")


class TestSegnoMese481:
    def test_segno_ok(self):
        assert _F["mh481_segno"](1.0, "s") == 1.0
        assert _F["mh481_segno"](-1.0, "s") == -1.0

    def test_segno_invalido(self):
        with pytest.raises(ValueError):
            _F["mh481_segno"](0.5, "s")
        with pytest.raises(ValueError):
            _F["mh481_segno"](2, "s")

    def test_mese_ok(self):
        assert _F["mh481_mese"]("2026-11", "m") == "2026-11"

    def test_mese_formato_errato(self):
        with pytest.raises(ValueError):
            _F["mh481_mese"]("2026-13", "m")
        with pytest.raises(ValueError):
            _F["mh481_mese"]("11-2026", "m")
        with pytest.raises(ValueError):
            _F["mh481_mese"](202611, "m")


class TestMtmLinea481:
    def test_demo_singola(self):
        assert _F["mh481_mtm_linea"](
            "TTF gas", "2026-11", 100000.0, 1.0, 95.00, 92.00) == MTM_A

    def test_demo_short_profitto(self):
        assert _F["mh481_mtm_linea"](
            "Power baseload DE", "2026-12", 50000.0, -1.0, 110.00,
            108.00) == 100000.0

    def test_demo_long_profitto(self):
        assert _F["mh481_mtm_linea"](
            "TTF gas", "2026-11", 20000.0, 1.0, 90.00, 94.00) == 80000.0

    def test_prezzo_invariato(self):
        assert _F["mh481_mtm_linea"](
            "TTF gas", "2026-11", 1000.0, 1.0, 50.0, 50.0) == 0.0

    def test_segno_invalido(self):
        with pytest.raises(ValueError):
            _F["mh481_mtm_linea"](
                "TTF gas", "2026-11", 1000.0, 0.5, 50.0, 51.0)

    def test_volume_zero(self):
        with pytest.raises(ValueError):
            _F["mh481_mtm_linea"](
                "TTF gas", "2026-11", 0.0, 1.0, 50.0, 51.0)

    def test_volume_negativo(self):
        with pytest.raises(ValueError):
            _F["mh481_mtm_linea"](
                "TTF gas", "2026-11", -10.0, 1.0, 50.0, 51.0)

    def test_prezzo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh481_mtm_linea"](
                "TTF gas", "2026-11", 1000.0, 1.0, -50.0, 51.0)

    def test_scadenza_formato_errato(self):
        with pytest.raises(ValueError):
            _F["mh481_mtm_linea"](
                "TTF gas", "nov-2026", 1000.0, 1.0, 50.0, 51.0)


class TestDv01481:
    def test_demo_singola(self):
        assert _F["mh481_dv01_linea"](
            "TTF gas", "2026-11", 100000.0, 1.0, 95.00, 92.00) == DV01_A

    def test_short_negativo(self):
        assert _F["mh481_dv01_linea"](
            "Power baseload DE", "2026-12", 50000.0, -1.0, 110.00,
            108.00) == -50000.0

    def test_indipendente_dai_prezzi(self):
        a = _F["mh481_dv01_linea"](
            "TTF gas", "2026-11", 100000.0, 1.0, 10.0, 200.0)
        assert a == _F["mh481_dv01_linea"](
            "TTF gas", "2026-11", 100000.0, 1.0, 95.00, 92.00)

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh481_dv01_linea"](
                "TTF gas", "2026-11", 0.0, 1.0, 50.0, 51.0)
        with pytest.raises(ValueError):
            _F["mh481_dv01_linea"](
                "TTF gas", "2026-11", 1000.0, 3.0, 50.0, 51.0)


class TestAggregazione481:
    def test_demo(self):
        agg = _F["mh481_aggregazione"](POS_B)
        assert agg["mtm_totale"] == MTM_B
        assert agg["dv01_totale"] == DV01_B
        assert agg["n_posizioni"] == 3

    def test_per_commodity(self):
        agg = _F["mh481_aggregazione"](POS_B)
        ttf = agg["per_commodity"]["TTF gas"]
        assert ttf["mtm"] == -220000.0
        assert ttf["dv01"] == 120000.0
        assert ttf["n"] == 2
        pde = agg["per_commodity"]["Power baseload DE"]
        assert pde["mtm"] == 100000.0
        assert pde["dv01"] == -50000.0

    def test_per_scadenza(self):
        agg = _F["mh481_aggregazione"](POS_B)
        nov = agg["per_scadenza"]["2026-11"]
        assert nov["mtm"] == -220000.0 and nov["dv01"] == 120000.0
        dic = agg["per_scadenza"]["2026-12"]
        assert dic["mtm"] == 100000.0 and dic["dv01"] == -50000.0

    def test_net_e_dominante(self):
        agg = _F["mh481_aggregazione"](POS_B)
        assert agg["net"] == "LONG"
        assert agg["scadenza_dominante"] == "2026-11"

    def test_net_short(self):
        agg = _F["mh481_aggregazione"]([dict(POS_B[1])])
        assert agg["net"] == "SHORT"

    def test_vuota(self):
        with pytest.raises(ValueError):
            _F["mh481_aggregazione"]([])

    def test_chiave_mancante(self):
        with pytest.raises(ValueError):
            _F["mh481_aggregazione"]([{"commodity": "x"}])

    def test_segno_invalido(self):
        bad = [dict(POS_B[0])]
        bad[0]["segno"] = 0.0
        with pytest.raises(ValueError):
            _F["mh481_aggregazione"](bad)


class TestScenario481:
    def test_demo(self):
        righe = _F["mh481_scenario"](MTM_B, DV01_B)
        assert [r["shift_eur_mwh"] for r in righe] == [-10.0, -5.0, -1.0,
                                                      1.0, 5.0, 10.0]
        assert [r["mtm_eur"] for r in righe] == SCEN_B

    def test_lineare_nel_dv01(self):
        righe = _F["mh481_scenario"](-120000.0, 70000.0)
        up = [r for r in righe if r["shift_eur_mwh"] == 10.0][0]
        down = [r for r in righe if r["shift_eur_mwh"] == -10.0][0]
        assert up["mtm_eur"] == -120000.0 + 700000.0
        assert down["mtm_eur"] == -120000.0 - 700000.0

    def test_custom_delta(self):
        righe = _F["mh481_scenario"](0.0, 1000.0, delta=(2.0,))
        assert [r["shift_eur_mwh"] for r in righe] == [-2.0, 2.0]
        assert [r["mtm_eur"] for r in righe] == [-2000.0, 2000.0]

    def test_dv01_zero(self):
        righe = _F["mh481_scenario"](500.0, 0.0)
        assert all(r["mtm_eur"] == 500.0 for r in righe)


class TestVerdetto481:
    def test_demo_concentrato(self):
        v = _F["mh481_verdetto"](POS_B)
        assert v["verdetto"] == VERD_B
        assert v["net"] == "LONG"
        assert abs(v["concentrazione"] - CONC_B) < 1e-12
        assert v["scadenza_dominante"] == "2026-11"

    def test_bilanciato(self):
        v = _F["mh481_verdetto"](POS_D)
        assert v["verdetto"] == VERD_D
        assert _F["mh481_aggregazione"](POS_D)["mtm_totale"] == MTM_D

    def test_esposto_netto(self):
        v = _F["mh481_verdetto"](POS_C)
        assert v["verdetto"] == VERD_C
        assert v["net"] == "LONG"
        assert abs(v["concentrazione"] - CONC_C) < 1e-12
        assert v["concentrazione"] < 0.6

    def test_boundary_concentrazione(self):
        pos = [
            {"commodity": "TTF gas", "scadenza": "2026-11",
             "volume_mwh": 60000.0, "segno": 1.0, "f_fix": 90.0,
             "f_now": 90.0},
            {"commodity": "TTF gas", "scadenza": "2026-12",
             "volume_mwh": 40000.0, "segno": 1.0, "f_fix": 90.0,
             "f_now": 90.0},
        ]
        v = _F["mh481_verdetto"](pos)
        assert abs(v["concentrazione"] - 0.6) < 1e-12
        assert v["verdetto"] == "CONCENTRATO"

    def test_vuota(self):
        with pytest.raises(ValueError):
            _F["mh481_verdetto"]([])


class TestUi481:
    def test_chiavi_481(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        fkeys = re.findall(r'key=f"st481_\w+\{', src)
        assert len(fkeys) == 6, fkeys
        expl = re.findall(r'key="st481_[^"]+"', src)
        assert expl == ['key="st481_csv"'], expl
