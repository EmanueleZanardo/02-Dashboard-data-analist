"""Test tab489 '🪓🌪️ Component Stressed VaR: quale linea tagliare sotto stress?': registry + funzioni pure."""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh489_num", "mh489_segno", "mh489_mese", "mh489_z",
           "mh489_mult", "mh489_limite",
           "mh489_dv01_linea", "mh489_sigma_mtm_linea",
           "mh489_var_stress_linea", "mh489_riga", "mh489_componenti",
           "mh489_taglio")

TITLE489 = "🪓🌪️ Component Stressed VaR: quale linea tagliare sotto stress?"
TITLE488 = "🌪️📉 Stressed VaR: il VaR sotto volatilità stressata"

Z99 = 2.3263478740408408

# Demo A: long TTF 100k MWh, scadenza 2027-01, f_fix 95.00, f_now 88.00,
# vol giornaliera 2.5%, z 99%, stress x2.
SIGMA_MTM_A = 220000.0
VAR_STRESS_A = 1023593.06457797

# Demo B: portafoglio 3 linee (TTF long 2027-01 sigma 2.5%,
# TTF short 2026-12 sigma 2.5%, Power DE long 2027-03 sigma 1.8%),
# z 99%, stress x2, limite 2'500'000 EUR.
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
VAR_STRESS_B = [1023593.06457797, 523428.2716596892, 1942965.7443985098]
VAR_STRESS_CONS_B = 3489987.080636169
PEG_B = "Power baseload DE 2027-03"
LIMITE_B = 2500000.0


def _righe_b():
    return [_F["mh489_riga"](p["commodity"], p["scadenza"], p["volume_mwh"],
                             p["segno"], p["f_fix"], p["f_now"],
                             p["sigma_pct"]) for p in POS_B]


class TestRegistry489:
    def _src(self):
        return (Path(__file__).resolve().parent.parent / "app.py"
                ).read_text(encoding="utf-8")

    def test_counts(self):
        src = self._src()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"    with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 504
        assert TITLE489 in titoli
        assert "tab491" in dvars

    def test_ui_indentata(self):
        src = self._src()
        assert "    with tab489:" in src

    def test_titolo_occorrenze(self):
        src = self._src()
        # header W489 + lista titoli + H1 nella UI
        assert src.count(TITLE489) == 3

    def test_dvar_line(self):
        src = self._src()
        assert "tab486, tab487, tab488, tab489, tab490, tab491, tab492, tab493, tab494, tab495, tab496, tab497, tab498, tab499, tab500, tab501, tab502, tab503, tab504 = st.tabs([" in src

    def test_chiavi_univoche(self):
        src = self._src()
        righe = [ln for ln in src.split("\n")
                 if "key=" in ln and "st489_" in ln]
        basi = [re.search(r"st489_[a-z]+", ln).group(0) for ln in righe]
        # ogni base compare una sola volta nel sorgente
        # (il loop for genera le 3 istanze a runtime)
        assert len(basi) == len(set(basi))
        assert len(basi) >= 10


class TestNum489:
    def test_ok(self):
        assert _F["mh489_num"](3, "x") == 3.0
        assert _F["mh489_num"](2.5, "x") == 2.5

    def test_ko(self):
        for v in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh489_num"](v, "x")


class TestSegno489:
    def test_ok(self):
        assert _F["mh489_segno"](1.0, "s") == 1.0
        assert _F["mh489_segno"](-1.0, "s") == -1.0

    def test_ko(self):
        for v in (0.0, 2.0, "long", 0):
            with pytest.raises(ValueError):
                _F["mh489_segno"](v, "s")


class TestMese489:
    def test_ok(self):
        assert _F["mh489_mese"]("2027-01", "m") == "2027-01"
        assert _F["mh489_mese"](" 2027-03 ", "m") == "2027-03"

    def test_ko(self):
        for v in ("2027", "2027-13", "2027-00", 202701, "gen-2027"):
            with pytest.raises(ValueError):
                _F["mh489_mese"](v, "m")


class TestZ489:
    def test_ok(self):
        assert _F["mh489_z"](0.99, "c") == Z99
        assert _F["mh489_z"](0.975, "c") == pytest.approx(1.959963984540054)

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh489_z"](0.95, "c")


class TestMult489:
    def test_ok(self):
        assert _F["mh489_mult"](2.0) == 2.0
        assert _F["mh489_mult"](10.0) == 10.0

    def test_ko(self):
        for v in (0.0, -1.0, 10.5):
            with pytest.raises(ValueError):
                _F["mh489_mult"](v)


class TestLimite489:
    def test_ok(self):
        assert _F["mh489_limite"](2500000.0) == 2500000.0

    def test_ko(self):
        for v in (0.0, -5.0):
            with pytest.raises(ValueError):
                _F["mh489_limite"](v)


class TestDv01489:
    def test_ok(self):
        assert _F["mh489_dv01_linea"](1.0, 100000.0) == 100000.0
        assert _F["mh489_dv01_linea"](-1.0, 50000.0) == -50000.0

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh489_dv01_linea"](1.0, -1.0)


class TestSigmaMtm489:
    def test_demo_a(self):
        assert _F["mh489_sigma_mtm_linea"](100000.0, 2.5, 88.00) == SIGMA_MTM_A

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh489_sigma_mtm_linea"](100000.0, 0.0, 88.00)
        with pytest.raises(ValueError):
            _F["mh489_sigma_mtm_linea"](100000.0, 101.0, 88.00)
        with pytest.raises(ValueError):
            _F["mh489_sigma_mtm_linea"](100000.0, 2.5, -1.0)


class TestVarStressLinea489:
    def test_demo_a(self):
        assert _F["mh489_var_stress_linea"](
            SIGMA_MTM_A, Z99, 2.0) == pytest.approx(VAR_STRESS_A, rel=1e-9)

    def test_scala_con_mult(self):
        v1 = _F["mh489_var_stress_linea"](SIGMA_MTM_A, Z99, 1.0)
        v3 = _F["mh489_var_stress_linea"](SIGMA_MTM_A, Z99, 3.0)
        assert v3 == pytest.approx(3.0 * v1)

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh489_var_stress_linea"](-1.0, Z99, 2.0)
        with pytest.raises(ValueError):
            _F["mh489_var_stress_linea"](SIGMA_MTM_A, 0.0, 2.0)
        with pytest.raises(ValueError):
            _F["mh489_var_stress_linea"](SIGMA_MTM_A, Z99, 0.0)


class TestRiga489:
    def test_demo_a(self):
        r = _F["mh489_riga"]("TTF gas", "2027-01", 100000.0, 1.0, 95.00,
                             88.00, 2.5)
        assert r["scadenza"] == "2027-01"
        assert r["dv01"] == 100000.0
        assert r["sigma_mtm"] == SIGMA_MTM_A

    def test_ko(self):
        with pytest.raises(ValueError):
            _F["mh489_riga"]("TTF gas", "2027-13", 100000.0, 1.0, 95.00,
                             88.00, 2.5)
        with pytest.raises(ValueError):
            _F["mh489_riga"]("TTF gas", "2027-01", 100000.0, 1.0, -95.00,
                             88.00, 2.5)


class TestComponenti489:
    def test_demo_b(self):
        c = _F["mh489_componenti"](_righe_b(), Z99, 2.0)
        for got, exp in zip(c["var_stress"], VAR_STRESS_B):
            assert got == pytest.approx(exp, rel=1e-9)
        assert c["var_stress_cons"] == pytest.approx(VAR_STRESS_CONS_B,
                                                    rel=1e-9)
        # conservativo = somma (attribuzione lineare, corr=1)
        assert sum(c["var_stress"]) == pytest.approx(c["var_stress_cons"])
        # indipendenza: RSS
        import math
        assert c["var_stress_ind"] == pytest.approx(
            math.sqrt(sum(v * v for v in VAR_STRESS_B)))
        assert c["var_stress_ind"] <= c["var_stress_cons"]
        # Eulero: i componenti d'indipendenza sommano al VaR indipendente
        assert sum(c["comp_ind"]) == pytest.approx(c["var_stress_ind"])
        # share conservative: sommano a 1
        assert sum(c["share_cons"]) == pytest.approx(1.0)
        # la linea C e' la peggiore
        assert c["share_cons"][2] == max(c["share_cons"])
        assert 0.0 <= c["div_benefit"] <= 1.0

    def test_riga_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh489_componenti"]([], Z99, 2.0)

    def test_volumi_nulli(self):
        r = _F["mh489_riga"]("TTF gas", "2027-01", 0.0, 1.0, 95.00, 88.00,
                             2.5)
        c = _F["mh489_componenti"]([r], Z99, 2.0)
        assert c["var_stress_cons"] == 0.0
        assert c["share_cons"] == [0.0]


class TestTaglio489:
    def test_demo_b_sfondato(self):
        t = _F["mh489_taglio"](_righe_b(), Z99, 2.0, LIMITE_B)
        assert t["peggiore"] == PEG_B
        assert t["verdetto"].startswith(f"TAGLIARE {PEG_B}:")
        assert t["verdetto"].endswith("LIMITE SFONDATO SOTTO STRESS")
        _per_mwh = VAR_STRESS_B[2] / 200000.0
        assert t["taglio_mwh"] == pytest.approx(
            (VAR_STRESS_CONS_B - LIMITE_B) / _per_mwh, rel=1e-9)
        assert 0.0 < t["taglio_mwh"] < 200000.0
        # dopo il taglio il VaR stressato torna (circa) al limite
        assert t["var_dopo_taglio"] == pytest.approx(LIMITE_B, rel=1e-9)

    def test_entro_limite(self):
        t = _F["mh489_taglio"](_righe_b(), Z99, 2.0, 10_000_000.0)
        assert t["peggiore"] is None
        assert t["taglio_mwh"] is None
        assert t["verdetto"] == ("NESSUN TAGLIO NECESSARIO — "
                                 "ENTRO IL LIMITE SOTTO STRESS")
        assert t["var_dopo_taglio"] == pytest.approx(VAR_STRESS_CONS_B,
                                                    rel=1e-9)

    def test_limite_uguale_var(self):
        t = _F["mh489_taglio"](_righe_b(), Z99, 2.0, VAR_STRESS_CONS_B)
        assert t["peggiore"] is None

    def test_limite_ko(self):
        with pytest.raises(ValueError):
            _F["mh489_taglio"](_righe_b(), Z99, 2.0, 0.0)

    def test_soglia_zero(self):
        # volume nullo -> VaR nullo -> nessun taglio, nessun errore
        r = _F["mh489_riga"]("TTF gas", "2027-01", 0.0, 1.0, 95.00, 88.00,
                             2.5)
        t = _F["mh489_taglio"]([r], Z99, 2.0, 1.0)
        assert t["peggiore"] is None
        assert t["taglio_mwh"] is None
