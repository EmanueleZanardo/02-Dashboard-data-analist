"""Test tab485 '🏦 Rho del portafoglio forward: il MtM sotto il tasso d'interesse': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh485_num", "mh485_segno", "mh485_mese", "mh485_data",
           "mh485_fine_mese", "mh485_tasso", "mh485_posizione", "mh485_tau",
           "mh485_df", "mh485_rho_linea", "mh485_rho_portafoglio",
           "mh485_scenario", "mh485_verdetto")

TITLE485 = "🏦 Rho del portafoglio forward: il MtM sotto il tasso d'interesse"
TITLE484 = "⏳ Theta del portafoglio forward: quanto vale il passare del tempo"

# Demo: stesse 3 righe dei default UI, data 2026-10-15, r = 3.00%.
POS = [
    {"commodity": "TTF gas", "scadenza": "2027-01",
     "volume_mwh": 100000.0, "segno": 1.0, "f_fix": 95.00, "f_now": 88.00},
    {"commodity": "TTF gas", "scadenza": "2026-12",
     "volume_mwh": 50000.0, "segno": -1.0, "f_fix": 91.00, "f_now": 90.00},
    {"commodity": "Power baseload DE", "scadenza": "2027-03",
     "volume_mwh": 200000.0, "segno": 1.0, "f_fix": 110.00, "f_now": 108.00},
]
DATA = "2026-10-15"
R = 0.03

# Riga 1: tau 108 gg -> tau_anni 108/365.25; df = exp(-0.03*tau).
TAU_G1 = 108
DF1 = 0.9911685914679053
MTM1 = -693818.0140275337
RHO_BP1 = 20.515358114982515
FUND1 = -20814.54042082601
# Riga 2: short TTF 2026-12, tau 77 gg.
TAU_G2 = 77
DF2 = 0.9936955218280477
MTM2 = 49684.77609140238
RHO_BP2 = -1.0474271756435274
# Riga 3: long Power DE 2027-03, tau 167 gg.
TAU_G3 = 167
DF3 = 0.9863770119085808
MTM3 = -394550.80476343236
RHO_BP3 = 18.039694564132297

MTM_TOT = -1038684.0426995637
RHO_BP_TOT = 37.50762550347128
FUND_TOT = -31160.52128098691
DUR = 0.3611071698568518
VERD = "RHO BREVE TERMINE"

# Scenario tassi: shift bp -> (mtm_stress, delta).
SCEN = {
    -200: (-1046213.8284455246, -7529.785745960893),
    -100: (-1042441.8611858573, -3757.8184862936614),
    -50: (-1040561.1868073115, -1877.144107747823),
    50: (-1036810.4219576502, 1873.6207419134444),
    100: (-1034940.3176906385, 3743.72500892519),
    200: (-1031210.631087561, 7473.411612002645),
}


def _approx(a, b):
    assert math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-6), f"{a} != {b}"


class TestRegistry485:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"    with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 502

    def test_ultima_tab(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert TITLE485 in titoli
        assert TITLE484 in titoli
        assert "tab485" in dvars

    def test_ui_indentata(self):
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        assert "    with tab485:" in src

    def test_titolo_occorrenze(self):
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        # header W485 + lista titoli + H1 nella UI
        assert src.count(TITLE485) == 3

    def test_dvar_line(self):
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        assert "tab485, tab486, tab487, tab488, tab489, tab490, tab491, tab492, tab493, tab494, tab495, tab496, tab497, tab498, tab499, tab500, tab501, tab502 = st.tabs([" in src


class TestNum485:
    def test_ok(self):
        assert _F["mh485_num"](3.5, "x") == 3.5
        assert _F["mh485_num"](7, "x") == 7.0

    def test_bool_rifiutato(self):
        with pytest.raises(ValueError):
            _F["mh485_num"](True, "x")

    def test_nan_inf_rifiutati(self):
        with pytest.raises(ValueError):
            _F["mh485_num"](float("nan"), "x")
        with pytest.raises(ValueError):
            _F["mh485_num"](float("inf"), "x")


class TestSegno485:
    def test_numerico(self):
        assert _F["mh485_segno"](1.0, "s") == 1.0
        assert _F["mh485_segno"](-1.0, "s") == -1.0

    def test_stringhe(self):
        assert _F["mh485_segno"]("long", "s") == 1.0
        assert _F["mh485_segno"](" Short ", "s") == -1.0

    def test_invalido(self):
        with pytest.raises(ValueError):
            _F["mh485_segno"](0.5, "s")
        with pytest.raises(ValueError):
            _F["mh485_segno"]("flat", "s")


class TestMeseData485:
    def test_mese_ok(self):
        assert _F["mh485_mese"]("2027-01", "m") == "2027-01"

    def test_mese_ko(self):
        with pytest.raises(ValueError):
            _F["mh485_mese"]("2027-13", "m")
        with pytest.raises(ValueError):
            _F["mh485_mese"]("2027-1", "m")

    def test_data_ok(self):
        import datetime
        assert _F["mh485_data"]("2026-10-15", "d") == datetime.date(2026, 10, 15)

    def test_data_ko(self):
        with pytest.raises(ValueError):
            _F["mh485_data"]("2026-13-01", "d")
        with pytest.raises(ValueError):
            _F["mh485_data"]("15/10/2026", "d")
        with pytest.raises(ValueError):
            _F["mh485_data"]("2026-02-30", "d")

    def test_fine_mese(self):
        import datetime
        assert _F["mh485_fine_mese"](2027, 1) == datetime.date(2027, 1, 31)
        assert _F["mh485_fine_mese"](2026, 12) == datetime.date(2026, 12, 31)
        assert _F["mh485_fine_mese"](2028, 2) == datetime.date(2028, 2, 29)


class TestTasso485:
    def test_ok(self):
        assert _F["mh485_tasso"](0.03, "r") == 0.03
        assert _F["mh485_tasso"](-0.10, "r") == -0.10
        assert _F["mh485_tasso"](0.50, "r") == 0.50

    def test_fuori_range(self):
        with pytest.raises(ValueError):
            _F["mh485_tasso"](0.51, "r")
        with pytest.raises(ValueError):
            _F["mh485_tasso"](-0.11, "r")


class TestTau485:
    def test_giorni(self):
        g, anni = _F["mh485_tau"]("2026-10-15", "2027-01")
        assert g == TAU_G1
        _approx(anni, 108 / 365.25)

    def test_scadenza_passata(self):
        with pytest.raises(ValueError):
            _F["mh485_tau"]("2026-10-15", "2026-09")

    def test_stesso_mese(self):
        g, _ = _F["mh485_tau"]("2026-10-15", "2026-10")
        assert g == 16


class TestDf485:
    def test_r_zero(self):
        assert _F["mh485_df"](1.5, 0.0) == 1.0

    def test_manuale(self):
        _approx(_F["mh485_df"](108 / 365.25, 0.03), DF1)

    def test_tau_negativo(self):
        with pytest.raises(ValueError):
            _F["mh485_df"](-1.0, 0.03)


class TestRhoLinea485:
    def test_demo_riga1(self):
        r = _F["mh485_rho_linea"]("TTF gas", "2027-01", 100000.0, 1.0,
                                  95.00, 88.00, DATA, R)
        assert r["tau_giorni"] == TAU_G1
        _approx(r["df"], DF1)
        _approx(r["mtm"], MTM1)
        _approx(r["rho_bp"], RHO_BP1)
        _approx(r["funding_annuo"], FUND1)

    def test_demo_riga2_short(self):
        r = _F["mh485_rho_linea"]("TTF gas", "2026-12", 50000.0, -1.0,
                                  91.00, 90.00, DATA, R)
        assert r["tau_giorni"] == TAU_G2
        _approx(r["df"], DF2)
        _approx(r["mtm"], MTM2)
        _approx(r["rho_bp"], RHO_BP2)

    def test_identita_rho(self):
        # rho = -tau * mtm ; rho_bp = rho * 1e-4 ; funding = mtm * r
        r = _F["mh485_rho_linea"]("X", "2027-03", 200000.0, 1.0,
                                  110.00, 108.00, DATA, R)
        _approx(r["rho"], -r["tau_anni"] * r["mtm"])
        _approx(r["rho_bp"], r["rho"] * 0.0001)
        _approx(r["funding_annuo"], r["mtm"] * R)
        _approx(r["mtm"], MTM3)

    def test_volume_zero_ko(self):
        with pytest.raises(ValueError):
            _F["mh485_rho_linea"]("X", "2027-01", 0.0, 1.0, 95.0, 88.0,
                                  DATA, R)


class TestRhoPortafoglio485:
    def test_totali(self):
        agg = _F["mh485_rho_portafoglio"](POS, DATA, R)
        assert agg["n_posizioni"] == 3
        _approx(agg["mtm_tot"], MTM_TOT)
        _approx(agg["rho_bp_tot"], RHO_BP_TOT)
        _approx(agg["funding_tot"], FUND_TOT)
        _approx(agg["rho_tot"], -sum(r["tau_anni"] * r["mtm"]
                                     for r in agg["righe"]))

    def test_aggregazioni(self):
        agg = _F["mh485_rho_portafoglio"](POS, DATA, R)
        _approx(agg["per_commodity"]["TTF gas"]["mtm"], MTM1 + MTM2)
        _approx(agg["per_commodity"]["TTF gas"]["rho_bp"], RHO_BP1 + RHO_BP2)
        assert agg["per_commodity"]["TTF gas"]["n"] == 2
        _approx(agg["per_scadenza"]["2027-03"]["mtm"], MTM3)

    def test_lista_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh485_rho_portafoglio"]([], DATA, R)


class TestScenario485:
    def test_costanti(self):
        sc = _F["mh485_scenario"](POS, DATA, R, [-200, -100, -50, 50, 100, 200])
        assert sc["base_r"] == R
        _approx(sc["mtm_base"], MTM_TOT)
        _approx(sc["rho_bp_tot"], RHO_BP_TOT)
        for s in sc["scenari"]:
            ms, dl = SCEN[s["shift_bp"]]
            _approx(s["mtm_stress"], ms)
            _approx(s["delta"], dl)

    def test_delta_lineare_in_rho_bp(self):
        # per piccoli shift, delta ~= rho_bp_tot * shift_bp
        sc = _F["mh485_scenario"](POS, DATA, R, [100])
        s = sc["scenari"][0]
        assert abs(s["delta"] - RHO_BP_TOT * 100) < abs(RHO_BP_TOT * 100) * 0.01

    def test_tasso_sale_mtm_negativo_sale(self):
        # MtM negativo + tassi su -> meno negativo (delta > 0)
        sc = _F["mh485_scenario"](POS, DATA, R, [200])
        assert sc["scenari"][0]["delta"] > 0

    def test_shifts_vuoti_ko(self):
        with pytest.raises(ValueError):
            _F["mh485_scenario"](POS, DATA, R, [])

    def test_shift_fuori_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh485_scenario"](POS, DATA, 0.50, [100])


class TestVerdetto485:
    def test_demo_breve(self):
        v = _F["mh485_verdetto"](POS, DATA, R)
        assert v["verdetto"] == VERD
        _approx(v["duration_anni"], DUR)
        _approx(v["rho_bp_tot"], RHO_BP_TOT)
        _approx(v["funding_annuo"], FUND_TOT)

    def test_nessuna_esposizione(self):
        p0 = [{"commodity": "X", "scadenza": "2027-01", "volume_mwh": 1000.0,
               "segno": 1.0, "f_fix": 88.0, "f_now": 88.0}]
        v = _F["mh485_verdetto"](p0, DATA, R)
        assert v["verdetto"] == "NESSUNA ESPOSIZIONE"

    def test_medio_termine(self):
        p1 = [{"commodity": "X", "scadenza": "2027-10", "volume_mwh": 1000.0,
               "segno": 1.0, "f_fix": 90.0, "f_now": 88.0}]
        v = _F["mh485_verdetto"](p1, DATA, R)
        assert v["verdetto"] == "RHO MEDIO TERMINE"

    def test_lungo_termine(self):
        p2 = [{"commodity": "X", "scadenza": "2029-01", "volume_mwh": 1000.0,
               "segno": 1.0, "f_fix": 90.0, "f_now": 88.0}]
        v = _F["mh485_verdetto"](p2, DATA, R)
        assert v["verdetto"] == "RHO LUNGO TERMINE"
