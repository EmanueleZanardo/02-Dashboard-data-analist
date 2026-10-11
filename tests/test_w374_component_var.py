"""Test tab374 'Component VaR: contributo al rischio per posizione': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh374_num", "mh374_z", "mh374_cov", "mh374_vol_port",
           "mh374_dot", "mh374_marginal", "mh374_component",
           "mh374_standalone", "mh374_verdetto", "mh374_analisi")

TITLE374 = "Component VaR: contributo al rischio per posizione"
TITLE373 = "Kelly con limite VaR: sizing con vincolo di perdita massima"
TITLE372 = "Monte Carlo: VaR e Expected Shortfall di una posizione power"
TITLE371 = "Kelly frazionario: frazione ottima per un budget di volatilità"
TITLE370 = "Kelly e drawdown: probabilità di toccare un max drawdown"
TITLE369 = "Kelly con costi di transazione: f* netto = (μ-c)/σ²"
E1 = 10000.0
E2 = 8000.0
E3 = 6000.0
S1 = 0.15
S2 = 0.2
S3 = 0.1
R12 = 0.6
R13 = 0.3
R23 = 0.4
ALPHA = 0.95
Z = 1.6448536269514715
V1 = 1500.0
V2 = 1600.0
V3 = 600.0
SIGMAP = 3059.0848304680926
VARP = 5031.746778547669
DOT1 = 2640.0
DOT2 = 2740.0
DOT3 = 1690.0
M1 = 0.21292709171883706
M2 = 0.2946566824796028
M3 = 0.09087040025374614
M1FC = 0.16448536269514716
SP0 = 2273.7634001804145
C1 = 2129.2709171883707
C2 = 2357.2534598368225
C3 = 545.2224015224768
SA1 = 2467.2804404272074
SA2 = 2631.7658031223546
SA3 = 986.912176170883
BENEFIT = 1054.2116411727757
BENPCT = 0.17322031608970478
TOPI = 1
TOPSHARE = 0.46847617012182097
VERDETTO = 'MODERATO: il maggior contribuente pesa tra 45% e 60%'


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry374:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 374
        assert "tab374" in dvars
        assert "tab374" in withs

    def test_titoli_allineati_369_370_371_372_373_374(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab369")] == TITLE369
        assert titoli[dvars.index("tab370")] == TITLE370
        assert titoli[dvars.index("tab371")] == TITLE371
        assert titoli[dvars.index("tab372")] == TITLE372
        assert titoli[dvars.index("tab373")] == TITLE373
        assert titoli[dvars.index("tab374")] == TITLE374

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab374"
        assert titoli[-1] == TITLE374
        assert withs[-1] == "tab374"


class TestNum:
    def test_num_ok(self):
        assert _F["mh374_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh374_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh374_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh374_num"](float("inf"), "x")


class TestZ:
    def test_demo(self):
        assert _F["mh374_z"](ALPHA) == pytest.approx(Z)

    def test_z95_noto(self):
        from statistics import NormalDist
        assert _F["mh374_z"](0.95) == pytest.approx(
            NormalDist().inv_cdf(0.95))

    def test_alpha_basso_ko(self):
        with pytest.raises(ValueError):
            _F["mh374_z"](0.5)

    def test_alpha_alto_ko(self):
        with pytest.raises(ValueError):
            _F["mh374_z"](1.0)


class TestCov:
    def test_demo_v(self):
        c = _F["mh374_cov"](E1, E2, E3, S1, S2, S3, R12, R13, R23)
        assert c["v"] == pytest.approx((V1, V2, V3))
        # v_i = E_i * s_i in forma chiusa
        assert c["v"][0] == pytest.approx(E1 * S1)
        assert c["v"][1] == pytest.approx(E2 * S2)
        assert c["v"][2] == pytest.approx(E3 * S3)

    def test_demo_c(self):
        c = _F["mh374_cov"](E1, E2, E3, S1, S2, S3, R12, R13, R23)
        assert c["c11"] == pytest.approx(V1 * V1)
        assert c["c22"] == pytest.approx(V2 * V2)
        assert c["c12"] == pytest.approx(V1 * V2 * R12)
        assert c["c13"] == pytest.approx(V1 * V3 * R13)
        assert c["c23"] == pytest.approx(V2 * V3 * R23)

    def test_posizione_singola(self):
        c = _F["mh374_cov"](15000.0, 0.0, 0.0, 0.10, 0.20, 0.10,
                            0.0, 0.0, 0.0)
        assert c["v"][0] == pytest.approx(1500.0)
        assert c["c11"] == pytest.approx(1500.0 ** 2)
        assert c["c22"] == pytest.approx(0.0)
        assert c["c12"] == pytest.approx(0.0)

    def test_corr_fuori_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh374_cov"](E1, E2, E3, S1, S2, S3, 1.5, R13, R23)
        with pytest.raises(ValueError):
            _F["mh374_cov"](E1, E2, E3, S1, S2, S3, R12, -1.01, R23)

    def test_vol_negativa_ko(self):
        with pytest.raises(ValueError):
            _F["mh374_cov"](E1, E2, E3, -0.05, S2, S3, R12, R13, R23)


class TestVol:
    def test_demo(self):
        c = _F["mh374_cov"](E1, E2, E3, S1, S2, S3, R12, R13, R23)
        assert _F["mh374_vol_port"](c) == pytest.approx(SIGMAP)

    def test_posizione_singola(self):
        c = _F["mh374_cov"](15000.0, 0.0, 0.0, 0.10, 0.20, 0.10,
                            0.0, 0.0, 0.0)
        assert _F["mh374_vol_port"](c) == pytest.approx(1500.0)

    def test_non_correlate(self):
        c = _F["mh374_cov"](E1, E2, E3, S1, S2, S3, 0.0, 0.0, 0.0)
        assert _F["mh374_vol_port"](c) == pytest.approx(SP0)
        assert SP0 == pytest.approx(math.sqrt(V1 ** 2 + V2 ** 2 + V3 ** 2))

    def test_vol_nulla_ko(self):
        c = _F["mh374_cov"](0.0, 0.0, 0.0, S1, S2, S3, R12, R13, R23)
        with pytest.raises(ValueError):
            _F["mh374_vol_port"](c)

    def test_non_psd_ko(self):
        c = _F["mh374_cov"](1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                            -1.0, -1.0, -1.0)
        with pytest.raises(ValueError):
            _F["mh374_vol_port"](c)


class TestDot:
    def test_demo(self):
        c = _F["mh374_cov"](E1, E2, E3, S1, S2, S3, R12, R13, R23)
        assert _F["mh374_dot"](c, 0) == pytest.approx(DOT1)
        assert _F["mh374_dot"](c, 1) == pytest.approx(DOT2)
        assert _F["mh374_dot"](c, 2) == pytest.approx(DOT3)
        # forma chiusa: riga 0 = v1 + r12*v2 + r13*v3
        assert _F["mh374_dot"](c, 0) == pytest.approx(
            V1 + R12 * V2 + R13 * V3)

    def test_indice_ko(self):
        c = _F["mh374_cov"](E1, E2, E3, S1, S2, S3, R12, R13, R23)
        with pytest.raises(ValueError):
            _F["mh374_dot"](c, 3)


class TestMarginal:
    def test_demo(self):
        c = _F["mh374_cov"](E1, E2, E3, S1, S2, S3, R12, R13, R23)
        sp = _F["mh374_vol_port"](c)
        assert _F["mh374_marginal"](Z, S1, DOT1, sp) == pytest.approx(M1)
        assert _F["mh374_marginal"](Z, S2, DOT2, sp) == pytest.approx(M2)
        assert _F["mh374_marginal"](Z, S3, DOT3, sp) == pytest.approx(M3)

    def test_posizione_singola(self):
        # dot = v1, sigma_p = v1 -> m = z * s1
        assert M1FC == pytest.approx(Z * 0.10)

    def test_sigma_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh374_marginal"](Z, S1, DOT1, 0.0)


class TestComponent:
    def test_demo(self):
        c = _F["mh374_cov"](E1, E2, E3, S1, S2, S3, R12, R13, R23)
        sp = _F["mh374_vol_port"](c)
        m = [_F["mh374_marginal"](Z, c["s"][i], _F["mh374_dot"](c, i), sp)
             for i in range(3)]
        cv = [_F["mh374_component"](c["e"][i], m[i]) for i in range(3)]
        assert cv == pytest.approx((C1, C2, C3))

    def test_eulero(self):
        # somma Component VaR = VaR di portafoglio
        assert C1 + C2 + C3 == pytest.approx(VARP)

    def test_esposizione_nulla(self):
        assert _F["mh374_component"](0.0, M1) == 0.0


class TestStandalone:
    def test_demo(self):
        assert _F["mh374_standalone"](Z, V1) == pytest.approx(SA1)
        assert _F["mh374_standalone"](Z, V2) == pytest.approx(SA2)
        assert _F["mh374_standalone"](Z, V3) == pytest.approx(SA3)

    def test_valore_assoluto(self):
        assert _F["mh374_standalone"](Z, -500.0) == pytest.approx(Z * 500.0)


class TestVerdetto:
    def test_demo(self):
        assert _F["mh374_verdetto"](TOPSHARE) == VERDETTO
        assert VERDETTO.startswith("MODERATO")

    def test_concentrato(self):
        assert _F["mh374_verdetto"](0.65).startswith("CONCENTRATO")
        assert _F["mh374_verdetto"](0.60).startswith("CONCENTRATO")

    def test_moderato(self):
        assert _F["mh374_verdetto"](0.59).startswith("MODERATO")
        assert _F["mh374_verdetto"](0.45).startswith("MODERATO")

    def test_bilanciato(self):
        assert _F["mh374_verdetto"](0.449).startswith("BILANCIATO")
        assert _F["mh374_verdetto"](0.10).startswith("BILANCIATO")

    def test_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh374_verdetto"](1.5)
        with pytest.raises(ValueError):
            _F["mh374_verdetto"](-0.1)


class TestAnalisi:
    def test_demo(self):
        a = _F["mh374_analisi"]((E1, E2, E3), (S1, S2, S3),
                                (R12, R13, R23), ALPHA)
        assert a["z"] == pytest.approx(Z)
        assert a["sigma_p"] == pytest.approx(SIGMAP)
        assert a["var_p"] == pytest.approx(VARP)
        assert a["marginal"] == pytest.approx((M1, M2, M3))
        assert a["cvar"] == pytest.approx((C1, C2, C3))
        assert a["standalone"] == pytest.approx((SA1, SA2, SA3))
        assert a["benefit"] == pytest.approx(BENEFIT)
        assert a["benefit_pct"] == pytest.approx(BENPCT)
        assert a["top_i"] == TOPI
        assert a["top_share"] == pytest.approx(TOPSHARE)
        assert a["verdetto"] == VERDETTO
        # Eulero + quote a somma 1
        assert sum(a["cvar"]) == pytest.approx(a["var_p"])
        assert sum(a["quote"]) == pytest.approx(1.0)
        # la demo ha correlazioni < 1: beneficio positivo, top = Power
        assert a["benefit"] > 0.0
        assert a["top_i"] == 1
        assert a["verdetto"].startswith("MODERATO")

    def test_non_correlate(self):
        a = _F["mh374_analisi"]((E1, E2, E3), (S1, S2, S3),
                                (0.0, 0.0, 0.0), ALPHA)
        assert a["benefit"] == pytest.approx(
            SA1 + SA2 + SA3 - a["var_p"])
        assert a["benefit"] > 0.0

    def test_posizione_singola(self):
        a = _F["mh374_analisi"]((10000.0, 0.0, 0.0), (0.15, 0.0, 0.0),
                                (0.0, 0.0, 0.0), ALPHA)
        assert a["benefit"] == pytest.approx(0.0)
        assert a["top_share"] == pytest.approx(1.0)
        assert a["cvar"][0] == pytest.approx(a["var_p"])
        assert a["verdetto"].startswith("CONCENTRATO")

    def test_corr_ko(self):
        with pytest.raises(ValueError):
            _F["mh374_analisi"]((E1, E2, E3), (S1, S2, S3),
                                (1.5, R13, R23), ALPHA)

    def test_lunghezze_ko(self):
        with pytest.raises(ValueError):
            _F["mh374_analisi"]((E1, E2), (S1, S2, S3),
                                (R12, R13, R23), ALPHA)

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh374_analisi"]((E1, E2, E3), (S1, S2, S3),
                                (R12, R13, R23), 1.5)
