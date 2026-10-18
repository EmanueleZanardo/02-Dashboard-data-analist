"""Test tab484 '⏳ Theta del portafoglio forward: quanto vale il passare del tempo': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh484_num", "mh484_segno", "mh484_mese", "mh484_mese_ord",
           "mh484_ord_mese", "mh484_curva", "mh484_posizione",
           "mh484_prezzo", "mh484_theta_linea", "mh484_theta_portafoglio",
           "mh484_roll_path", "mh484_verdetto")

TITLE484 = "⏳ Theta del portafoglio forward: quanto vale il passare del tempo"
TITLE483 = "🧪💥 Shock di curva: P&L del portafoglio sotto scenari di prezzo"

# Curva TTF in backwardation (prezzi calanti con la scadenza)
CURVA_TTF = {"2026-11": 92.0, "2026-12": 90.0, "2027-01": 88.0,
             "2027-02": 87.0, "2027-03": 86.0, "2027-04": 85.0}
# Curva Power DE in contango (prezzi crescenti con la scadenza)
CURVA_DE = {"2026-11": 100.0, "2026-12": 104.0, "2027-01": 108.0,
            "2027-02": 112.0, "2027-03": 116.0, "2027-04": 120.0}
GIORNI = 30

# Demo A: long TTF 100k MWh, scadenza 2027-01, f_fix 95.00, 30 giorni.
# In backwardation il long rolla verso l'alto: theta positiva.
F0_A = 88.0
F1_A = 89.97125256673462
THETA_A = 197125.256673462
MTM_A = -700000.0
TG_A = 6570.8418891154

# Demo B: portafoglio 3 linee (TTF long 2027-01, TTF short 2026-12,
# Power DE long 2027-03) con le due curve sopra, 30 giorni.
POS_B = [
    {"commodity": "TTF gas", "scadenza": "2027-01",
     "volume_mwh": 100000.0, "segno": 1.0, "f_fix": 95.00, "f_now": 88.00},
    {"commodity": "TTF gas", "scadenza": "2026-12",
     "volume_mwh": 50000.0, "segno": -1.0, "f_fix": 91.00, "f_now": 90.00},
    {"commodity": "Power baseload DE", "scadenza": "2027-03",
     "volume_mwh": 200000.0, "segno": 1.0, "f_fix": 110.00, "f_now": 108.00},
]
CURVE_B = {"TTF gas": CURVA_TTF, "Power baseload DE": CURVA_DE}
THETA_B = -689938.398357117
MTM_B = 550000.0
TG_B = -22997.9466119039
VERD_B = 'THETA NEGATIVA'
RY_B = -0.229979466119039

# Demo C: curva piatta -> theta esattamente 0 -> NEUTRA.
CURVA_PIATTA = {"2026-11": 88.0, "2026-12": 88.0}
THETA_C = 0.0

# Demo D: long 200k in contango (Power DE, scadenza 2027-03) -> theta < 0.
THETA_D = -788501.026693848
VERD_D = 'THETA NEGATIVA'

# Demo E/F: boundary della soglia (mtm = 0 -> soglia = 100 EUR).
# curva {"2026-11": 90.0, "2026-12": 92.0}, scadenza 2026-12,
# giorni = 30.4375 -> tau1 = tau0 - 1 mese esatto -> f1 = 90.0 esatto.
CURVA_EF = {"2026-11": 90.0, "2026-12": 92.0}
GIORNI_EF = 30.4375
THETA_E = -100.0      # vol 50 -> -100.0 esatto == -soglia -> NEUTRA
THETA_F = -102.0      # vol 51 -> -102.0 esatto < -soglia -> NEGATIVA


def _approx(a, b):
    assert math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-6), f"{a} != {b}"


class TestRegistry484:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"    with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 538

    def test_ultima_tab(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert TITLE484 in titoli
        assert TITLE483 in titoli
        assert "tab484" in dvars

    def test_ui_indentata(self):
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        assert "    with tab484:" in src

    def test_titolo_occorrenze(self):
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        # header W484 + lista titoli + H1 nella UI
        assert src.count(TITLE484) == 3

    def test_dvar_line(self):
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        assert "tab484, tab485, tab486, tab487, tab488, tab489, tab490, tab491, tab492, tab493, tab494, tab495, tab496, tab497, tab498, tab499, tab500, tab501, tab502, tab503, tab504, tab505, tab506, tab507, tab508, tab509, tab510, tab511, tab512, tab513, tab514, tab515, tab516, tab517, tab518, tab519, tab520, tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538 = st.tabs([" in src


class TestNum484:
    def test_ok(self):
        assert _F["mh484_num"](3.5, "x") == 3.5
        assert _F["mh484_num"](7, "x") == 7.0

    def test_bool_rifiutato(self):
        with pytest.raises(ValueError):
            _F["mh484_num"](True, "x")

    def test_nan_inf_rifiutati(self):
        with pytest.raises(ValueError):
            _F["mh484_num"](float("nan"), "x")
        with pytest.raises(ValueError):
            _F["mh484_num"](float("inf"), "x")

    def test_stringa_rifiutata(self):
        with pytest.raises(ValueError):
            _F["mh484_num"]("3.5", "x")


class TestSegno484:
    def test_ok(self):
        assert _F["mh484_segno"](1.0, "s") == 1.0
        assert _F["mh484_segno"](-1.0, "s") == -1.0

    def test_invalido(self):
        with pytest.raises(ValueError):
            _F["mh484_segno"](0.5, "s")
        with pytest.raises(ValueError):
            _F["mh484_segno"](2, "s")


class TestMeseOrd484:
    def test_mese_ord(self):
        assert _F["mh484_mese_ord"]("2026-11") == 2026 * 12 + 11
        assert _F["mh484_mese_ord"]("2027-01") == 2027 * 12 + 1

    def test_ord_mese(self):
        assert _F["mh484_ord_mese"](2026 * 12 + 11) == "2026-11"
        assert _F["mh484_ord_mese"](2027 * 12 + 1) == "2027-01"

    def test_roundtrip(self):
        for m in ("2026-11", "2027-03", "2030-12"):
            assert _F["mh484_ord_mese"](_F["mh484_mese_ord"](m)) == m

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh484_mese_ord"]("2026-13")
        with pytest.raises(ValueError):
            _F["mh484_ord_mese"](1.5)
        with pytest.raises(ValueError):
            _F["mh484_ord_mese"](0)


class TestCurva484:
    def test_ok_ordinata(self):
        punti = _F["mh484_curva"](
            {"2027-01": 88.0, "2026-11": 92.0}, "c")
        assert punti == [(2026 * 12 + 11, 92.0), (2027 * 12 + 1, 88.0)]

    def test_vuota(self):
        with pytest.raises(ValueError):
            _F["mh484_curva"]({}, "c")

    def test_mese_errato(self):
        with pytest.raises(ValueError):
            _F["mh484_curva"]({"nov-2026": 90.0}, "c")

    def test_prezzo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh484_curva"]({"2026-11": -1.0}, "c")


class TestPrezzo484:
    def test_punto_esatto(self):
        punti = _F["mh484_curva"](CURVA_TTF, "c")
        assert _F["mh484_prezzo"](punti, 2027 * 12 + 1) == 88.0

    def test_punto_medio(self):
        punti = _F["mh484_curva"]({"2026-11": 90.0, "2026-12": 92.0}, "c")
        _approx(_F["mh484_prezzo"](punti, (2026 * 12 + 11) + 0.5), 91.0)

    def test_clamp_basso(self):
        punti = _F["mh484_curva"](CURVA_TTF, "c")
        assert _F["mh484_prezzo"](punti, 2020 * 12 + 1) == 92.0

    def test_clamp_alto(self):
        punti = _F["mh484_curva"](CURVA_TTF, "c")
        assert _F["mh484_prezzo"](punti, 2030 * 12 + 6) == 85.0


class TestPosizione484:
    def test_ok(self):
        p = _F["mh484_posizione"](
            {"commodity": "TTF gas", "scadenza": "2027-01",
             "volume_mwh": 100000.0, "segno": 1.0, "f_fix": 95.0,
             "f_now": 88.0}, 0)
        assert p["commodity"] == "TTF gas" and p["volume_mwh"] == 100000.0

    def test_volume_zero(self):
        with pytest.raises(ValueError):
            _F["mh484_posizione"](
                {"commodity": "x", "scadenza": "2027-01", "volume_mwh": 0.0,
                 "segno": 1.0, "f_fix": 95.0, "f_now": 88.0}, 0)

    def test_segno_invalido(self):
        with pytest.raises(ValueError):
            _F["mh484_posizione"](
                {"commodity": "x", "scadenza": "2027-01", "volume_mwh": 10.0,
                 "segno": 0.0, "f_fix": 95.0, "f_now": 88.0}, 0)

    def test_chiave_mancante(self):
        with pytest.raises(ValueError):
            _F["mh484_posizione"]({"commodity": "x"}, 3)


class TestThetaLinea484:
    def test_demo_backwardation_long(self):
        r = _F["mh484_theta_linea"](
            "TTF gas", "2027-01", 100000.0, 1.0, 95.00, 88.00,
            CURVA_TTF, GIORNI)
        _approx(r["f_oggi"], F0_A)
        _approx(r["f_futura"], F1_A)
        _approx(r["theta"], THETA_A)
        _approx(r["mtm"], MTM_A)
        _approx(r["theta_giorno"], TG_A)
        assert r["theta"] > 0  # long in backwardation: rolla verso l'alto

    def test_short_contango_segno(self):
        r = _F["mh484_theta_linea"](
            "Power baseload DE", "2027-03", 200000.0, -1.0, 110.00, 108.00,
            CURVA_DE, GIORNI)
        _approx(r["theta"], -THETA_D)
        assert r["theta"] > 0  # short in contango: guadagna dal roll-down

    def test_f_oggi_da_curva(self):
        # f_oggi viene dalla curva, non da f_now: qui la curva dice 100
        r = _F["mh484_theta_linea"](
            "TTF gas", "2026-11", 1000.0, 1.0, 90.0, 77.77,
            {"2026-11": 100.0}, GIORNI)
        assert r["f_oggi"] == 100.0
        assert r["f_futura"] == 100.0  # clamp: curva a un punto
        assert r["theta"] == 0.0

    def test_giorni_zero(self):
        with pytest.raises(ValueError):
            _F["mh484_theta_linea"](
                "TTF gas", "2027-01", 1000.0, 1.0, 95.0, 88.0,
                CURVA_TTF, 0)

    def test_giorni_negativi(self):
        with pytest.raises(ValueError):
            _F["mh484_theta_linea"](
                "TTF gas", "2027-01", 1000.0, 1.0, 95.0, 88.0,
                CURVA_TTF, -5)

    def test_curva_non_dict(self):
        with pytest.raises(ValueError):
            _F["mh484_theta_linea"](
                "TTF gas", "2027-01", 1000.0, 1.0, 95.0, 88.0,
                [], GIORNI)


class TestPortafoglio484:
    def test_demo(self):
        agg = _F["mh484_theta_portafoglio"](POS_B, CURVE_B, GIORNI)
        _approx(agg["theta_tot"], THETA_B)
        _approx(agg["mtm_tot"], MTM_B)
        _approx(agg["theta_giorno_tot"], TG_B)
        assert agg["n_posizioni"] == 3

    def test_per_commodity(self):
        agg = _F["mh484_theta_portafoglio"](POS_B, CURVE_B, GIORNI)
        ttf = agg["per_commodity"]["TTF gas"]
        _approx(ttf["theta"], THETA_A + (
            _F["mh484_theta_linea"](
                "TTF gas", "2026-12", 50000.0, -1.0, 91.00, 90.00,
                CURVA_TTF, GIORNI)["theta"]))
        assert ttf["n"] == 2
        pde = agg["per_commodity"]["Power baseload DE"]
        _approx(pde["theta"], THETA_D)
        assert pde["n"] == 1

    def test_per_scadenza(self):
        agg = _F["mh484_theta_portafoglio"](POS_B, CURVE_B, GIORNI)
        assert set(agg["per_scadenza"]) == {"2027-01", "2026-12", "2027-03"}
        gen = agg["per_scadenza"]["2027-01"]
        _approx(gen["theta"], THETA_A)

    def test_curva_mancante(self):
        with pytest.raises(ValueError):
            _F["mh484_theta_portafoglio"](
                [dict(POS_B[0])], {"Power baseload DE": CURVA_DE}, GIORNI)

    def test_vuota(self):
        with pytest.raises(ValueError):
            _F["mh484_theta_portafoglio"]([], CURVE_B, GIORNI)

    def test_chiave_mancante(self):
        with pytest.raises(ValueError):
            _F["mh484_theta_portafoglio"]([{"commodity": "x"}], CURVE_B,
                                          GIORNI)


class TestRollPath484:
    def test_lunghezza(self):
        path = _F["mh484_roll_path"](
            "TTF gas", "2027-01", 100000.0, 1.0, 95.00, 88.00,
            CURVA_TTF, GIORNI)
        assert len(path) == GIORNI + 1
        assert [q["giorno"] for q in path] == list(range(GIORNI + 1))

    def test_giorno_zero(self):
        path = _F["mh484_roll_path"](
            "TTF gas", "2027-01", 100000.0, 1.0, 95.00, 88.00,
            CURVA_TTF, GIORNI)
        _approx(path[0]["prezzo"], F0_A)
        _approx(path[0]["mtm"], MTM_A)

    def test_ultimo_uguale_f_futura(self):
        path = _F["mh484_roll_path"](
            "TTF gas", "2027-01", 100000.0, 1.0, 95.00, 88.00,
            CURVA_TTF, GIORNI)
        _approx(path[-1]["prezzo"], F1_A)
        _approx(path[-1]["mtm"], MTM_A + THETA_A)

    def test_giorni_non_intero(self):
        with pytest.raises(ValueError):
            _F["mh484_roll_path"](
                "TTF gas", "2027-01", 1000.0, 1.0, 95.0, 88.0,
                CURVA_TTF, 7.5)


class TestVerdetto484:
    def test_demo_negativa(self):
        v = _F["mh484_verdetto"](POS_B, CURVE_B, GIORNI)
        assert v["verdetto"] == VERD_B
        _approx(v["theta_tot"], THETA_B)
        _approx(v["roll_yield_annuo"], RY_B)

    def test_neutra_curva_piatta(self):
        v = _F["mh484_verdetto"](
            [{"commodity": "TTF gas", "scadenza": "2026-12",
              "volume_mwh": 100000.0, "segno": 1.0, "f_fix": 88.0,
              "f_now": 88.0}],
            {"TTF gas": CURVA_PIATTA}, GIORNI)
        assert v["verdetto"] == "NEUTRA"
        assert v["theta_tot"] == THETA_C == 0.0

    def test_negativa_contango(self):
        v = _F["mh484_verdetto"](
            [{"commodity": "Power baseload DE", "scadenza": "2027-03",
              "volume_mwh": 200000.0, "segno": 1.0, "f_fix": 116.0,
              "f_now": 116.0}],
            {"Power baseload DE": CURVA_DE}, GIORNI)
        assert v["verdetto"] == VERD_D
        _approx(v["theta_tot"], THETA_D)
        assert v["theta_tot"] < 0

    def test_boundary_neutra(self):
        # theta = -100.0 esatto == -soglia (mtm = 0) -> NEUTRA
        r = _F["mh484_theta_linea"](
            "TTF gas", "2026-12", 50.0, 1.0, 92.0, 92.0,
            CURVA_EF, GIORNI_EF)
        assert r["theta"] == THETA_E == -100.0
        v = _F["mh484_verdetto"](
            [{"commodity": "TTF gas", "scadenza": "2026-12",
              "volume_mwh": 50.0, "segno": 1.0, "f_fix": 92.0,
              "f_now": 92.0}],
            {"TTF gas": CURVA_EF}, GIORNI_EF)
        assert v["verdetto"] == "NEUTRA"

    def test_oltre_soglia_negativa(self):
        # theta = -102.0 esatto < -soglia -> THETA NEGATIVA
        v = _F["mh484_verdetto"](
            [{"commodity": "TTF gas", "scadenza": "2026-12",
              "volume_mwh": 51.0, "segno": 1.0, "f_fix": 92.0,
              "f_now": 92.0}],
            {"TTF gas": CURVA_EF}, GIORNI_EF)
        assert v["theta_tot"] == THETA_F == -102.0
        assert v["verdetto"] == "THETA NEGATIVA"

    def test_chiavi(self):
        v = _F["mh484_verdetto"](POS_B, CURVE_B, GIORNI)
        assert set(v) == {"verdetto", "theta_tot", "mtm_tot",
                          "theta_giorno", "roll_yield_annuo", "giorni"}
        assert v["giorni"] == float(GIORNI)


class TestUi484:
    def test_chiavi_484(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        fkeys = re.findall(r'key=f"st484_\w+', src)
        # 6 pattern riga-posizione + 1 pattern curva
        assert len(fkeys) == 7, fkeys
        expl = sorted(re.findall(r'key="(st484_[^"]+)"', src))
        assert expl == ["st484_csv", "st484_giorni"], expl
