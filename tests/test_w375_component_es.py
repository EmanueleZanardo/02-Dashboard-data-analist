"""Test tab375 'Component ES: contributo al rischio di coda per posizione': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh375_num", "mh375_z", "mh375_phi", "mh375_es_mult",
           "mh375_cov", "mh375_vol_port", "mh375_dot", "mh375_marginal_es",
           "mh375_component", "mh375_standalone_es", "mh375_verdetto",
           "mh375_analisi")

TITLE375 = "Component ES: contributo al rischio di coda per posizione"
TITLE374 = "Component VaR: contributo al rischio per posizione"
TITLE373 = "Kelly con limite VaR: sizing con vincolo di perdita massima"
TITLE372 = "Monte Carlo: VaR e Expected Shortfall di una posizione power"
TITLE371 = "Kelly frazionario: frazione ottima per un budget di volatilità"
TITLE370 = "Kelly e drawdown: probabilità di toccare un max drawdown"
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
MULT = 2.062712807507429
V1 = 1500.0
V2 = 1600.0
V3 = 600.0
SIGMAP = 3059.0848304680926
ESP = 6310.0134590582265
VARP = 5031.746778547669
DOT1 = 2640.0
DOT2 = 2740.0
DOT3 = 1690.0
M1 = 0.26701916325999764
M2 = 0.36951136733959267
M3 = 0.11395514795691819
M1FC = 0.2062712807507429
SP0 = 2273.7634001804145
C1 = 2670.1916325999764
C2 = 2956.090938716741
C3 = 683.7308877415092
SA1 = 3094.069211261143
SA2 = 3300.340492011886
SA3 = 1237.6276845044572
ES1FC = 3094.069211261143
BENEFIT = 1322.0239287192599
BENPCT = 0.17322031608970465
TOPI = 1
TOPSHARE = 0.4684761701218209
VERDETTO = 'MODERATO: il maggior contribuente di coda pesa tra 45% e 60%'


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry375:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 375
        assert "tab375" in dvars
        assert "tab375" in withs

    def test_titoli_allineati_370_371_372_373_374_375(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab370")] == TITLE370
        assert titoli[dvars.index("tab371")] == TITLE371
        assert titoli[dvars.index("tab372")] == TITLE372
        assert titoli[dvars.index("tab373")] == TITLE373
        assert titoli[dvars.index("tab374")] == TITLE374
        assert titoli[dvars.index("tab375")] == TITLE375

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab375"
        assert titoli[-1] == TITLE375
        assert withs[-1] == "tab375"


class TestNum:
    def test_num_ok(self):
        assert _F["mh375_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh375_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh375_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh375_num"](float("inf"), "x")


class TestZPhi:
    def test_demo_z(self):
        assert _F["mh375_z"](ALPHA) == pytest.approx(Z)

    def test_z95_noto(self):
        from statistics import NormalDist
        assert _F["mh375_z"](0.95) == pytest.approx(
            NormalDist().inv_cdf(0.95))

    def test_alpha_basso_ko(self):
        with pytest.raises(ValueError):
            _F["mh375_z"](0.5)

    def test_phi_zero(self):
        assert _F["mh375_phi"](0.0) == pytest.approx(
            1.0 / math.sqrt(2.0 * math.pi))

    def test_phi_simmetria(self):
        assert _F["mh375_phi"](1.5) == pytest.approx(_F["mh375_phi"](-1.5))

    def test_es_mult_demo(self):
        assert _F["mh375_es_mult"](ALPHA) == pytest.approx(MULT)
        # forma chiusa: ES = sigma * phi(z)/p
        assert MULT == pytest.approx(_F["mh375_phi"](Z) / (1.0 - ALPHA))

    def test_es_mult_cresce_con_confidenza(self):
        assert _F["mh375_es_mult"](0.99) > _F["mh375_es_mult"](0.95)


class TestCov:
    def test_demo_v(self):
        c = _F["mh375_cov"](E1, E2, E3, S1, S2, S3, R12, R13, R23)
        assert c["v"] == pytest.approx((V1, V2, V3))
        # v_i = E_i * s_i in forma chiusa
        assert c["v"][0] == pytest.approx(E1 * S1)
        assert c["v"][1] == pytest.approx(E2 * S2)
        assert c["v"][2] == pytest.approx(E3 * S3)

    def test_demo_c(self):
        c = _F["mh375_cov"](E1, E2, E3, S1, S2, S3, R12, R13, R23)
        assert c["c11"] == pytest.approx(V1 * V1)
        assert c["c22"] == pytest.approx(V2 * V2)
        assert c["c12"] == pytest.approx(V1 * V2 * R12)
        assert c["c13"] == pytest.approx(V1 * V3 * R13)
        assert c["c23"] == pytest.approx(V2 * V3 * R23)

    def test_posizione_singola(self):
        c = _F["mh375_cov"](15000.0, 0.0, 0.0, 0.10, 0.20, 0.10,
                            0.0, 0.0, 0.0)
        assert c["v"][0] == pytest.approx(1500.0)
        assert c["v"][1] == pytest.approx(0.0)

    def test_corr_fuori_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh375_cov"](E1, E2, E3, S1, S2, S3, 1.5, R13, R23)

    def test_vol_negativa_ko(self):
        with pytest.raises(ValueError):
            _F["mh375_cov"](E1, E2, E3, -0.05, S2, S3, R12, R13, R23)


class TestVolPort:
    def test_demo(self):
        c = _F["mh375_cov"](E1, E2, E3, S1, S2, S3, R12, R13, R23)
        assert _F["mh375_vol_port"](c) == pytest.approx(SIGMAP)

    def test_corr_nulle_euclidea(self):
        c = _F["mh375_cov"](E1, E2, E3, S1, S2, S3, 0.0, 0.0, 0.0)
        assert _F["mh375_vol_port"](c) == pytest.approx(SP0)
        assert SP0 == pytest.approx(math.sqrt(V1 * V1 + V2 * V2 + V3 * V3))

    def test_non_psd_ko(self):
        c = _F["mh375_cov"](1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0, -1.0, -1.0)
        with pytest.raises(ValueError):
            _F["mh375_vol_port"](c)

    def test_vol_nulla_ko(self):
        c = _F["mh375_cov"](0.0, 0.0, 0.0, S1, S2, S3, R12, R13, R23)
        with pytest.raises(ValueError):
            _F["mh375_vol_port"](c)


class TestDot:
    def test_demo(self):
        c = _F["mh375_cov"](E1, E2, E3, S1, S2, S3, R12, R13, R23)
        assert _F["mh375_dot"](c, 0) == pytest.approx(DOT1)
        assert _F["mh375_dot"](c, 1) == pytest.approx(DOT2)
        assert _F["mh375_dot"](c, 2) == pytest.approx(DOT3)
        # forma chiusa riga 0
        assert DOT1 == pytest.approx(V1 + R12 * V2 + R13 * V3)

    def test_indice_ko(self):
        c = _F["mh375_cov"](E1, E2, E3, S1, S2, S3, R12, R13, R23)
        with pytest.raises(ValueError):
            _F["mh375_dot"](c, 3)


class TestMarginalES:
    def test_demo(self):
        assert _F["mh375_marginal_es"](MULT, S1, DOT1, SIGMAP) == \
            pytest.approx(M1)
        assert _F["mh375_marginal_es"](MULT, S2, DOT2, SIGMAP) == \
            pytest.approx(M2)
        assert _F["mh375_marginal_es"](MULT, S3, DOT3, SIGMAP) == \
            pytest.approx(M3)
        # forma chiusa
        assert M1 == pytest.approx(MULT * S1 * DOT1 / SIGMAP)

    def test_posizione_singola_forma_chiusa(self):
        c = _F["mh375_cov"](15000.0, 0.0, 0.0, 0.10, 0.20, 0.10,
                            0.0, 0.0, 0.0)
        sp = _F["mh375_vol_port"](c)
        m = _F["mh375_marginal_es"](MULT, 0.10, _F["mh375_dot"](c, 0), sp)
        assert m == pytest.approx(M1FC)
        assert M1FC == pytest.approx(MULT * 0.10)

    def test_mult_non_positivo_ko(self):
        with pytest.raises(ValueError):
            _F["mh375_marginal_es"](0.0, S1, DOT1, SIGMAP)

    def test_sigma_non_positivo_ko(self):
        with pytest.raises(ValueError):
            _F["mh375_marginal_es"](MULT, S1, DOT1, 0.0)


class TestComponent:
    def test_demo(self):
        assert _F["mh375_component"](E1, M1) == pytest.approx(C1)
        assert _F["mh375_component"](E2, M2) == pytest.approx(C2)
        assert _F["mh375_component"](E3, M3) == pytest.approx(C3)

    def test_eulero(self):
        # somma Component ES = ES di portafoglio
        assert C1 + C2 + C3 == pytest.approx(ESP)


class TestStandalone:
    def test_demo(self):
        assert _F["mh375_standalone_es"](MULT, V1) == pytest.approx(SA1)
        assert _F["mh375_standalone_es"](MULT, V2) == pytest.approx(SA2)
        assert _F["mh375_standalone_es"](MULT, V3) == pytest.approx(SA3)
        # forma chiusa
        assert SA1 == pytest.approx(MULT * abs(V1))

    def test_posizione_singola(self):
        c = _F["mh375_cov"](15000.0, 0.0, 0.0, 0.10, 0.20, 0.10,
                            0.0, 0.0, 0.0)
        sa = _F["mh375_standalone_es"](MULT, c["v"][0])
        assert sa == pytest.approx(ES1FC)
        assert ES1FC == pytest.approx(MULT * 1500.0)

    def test_mult_ko(self):
        with pytest.raises(ValueError):
            _F["mh375_standalone_es"](-1.0, V1)


class TestVerdetto:
    def test_concentrato(self):
        assert _F["mh375_verdetto"](0.65).startswith("CONCENTRATO")
        assert _F["mh375_verdetto"](0.60).startswith("CONCENTRATO")

    def test_moderato(self):
        assert _F["mh375_verdetto"](0.59).startswith("MODERATO")
        assert _F["mh375_verdetto"](0.45).startswith("MODERATO")

    def test_bilanciato(self):
        assert _F["mh375_verdetto"](0.449).startswith("BILANCIATO")

    def test_fuori_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh375_verdetto"](1.5)


class TestAnalisi:
    def _a(self):
        return _F["mh375_analisi"]((E1, E2, E3), (S1, S2, S3),
                                  (R12, R13, R23), ALPHA)

    def test_demo(self):
        a = self._a()
        assert a["z"] == pytest.approx(Z)
        assert a["es_mult"] == pytest.approx(MULT)
        assert a["sigma_p"] == pytest.approx(SIGMAP)
        assert a["es_p"] == pytest.approx(ESP)
        assert a["var_p"] == pytest.approx(VARP)
        assert a["v"] == pytest.approx((V1, V2, V3))
        assert a["dot"] == pytest.approx((DOT1, DOT2, DOT3))
        assert a["marginal"] == pytest.approx((M1, M2, M3))
        assert a["ces"] == pytest.approx((C1, C2, C3))
        assert a["standalone"] == pytest.approx((SA1, SA2, SA3))
        assert a["benefit"] == pytest.approx(BENEFIT)
        assert a["benefit_pct"] == pytest.approx(BENPCT)
        assert a["top_i"] == TOPI
        assert a["top_share"] == pytest.approx(TOPSHARE)
        assert a["verdetto"] == VERDETTO

    def test_eulero_esatto(self):
        a = self._a()
        assert sum(a["ces"]) == pytest.approx(a["es_p"])
        assert sum(a["quote"]) == pytest.approx(1.0)

    def test_es_sopra_var(self):
        a = self._a()
        # l'ES di coda sta sempre sopra il VaR
        assert a["es_p"] > a["var_p"]

    def test_benefit_positivo(self):
        a = self._a()
        assert a["benefit"] == pytest.approx(
            sum(a["standalone"]) - a["es_p"])
        assert a["benefit"] > 0.0

    def test_demo_verdetto(self):
        a = self._a()
        # top = Power DE (indice 1), quota 45-60% -> MODERATO
        assert a["top_i"] == 1
        assert 0.45 <= a["top_share"] < 0.60
        assert a["verdetto"].startswith("MODERATO")

    def test_num_ok(self):
        assert _F["mh375_num"](5.0, "x") == 5.0

    def test_lunghezze_ko(self):
        with pytest.raises(ValueError):
            _F["mh375_analisi"]((E1, E2), (S1, S2, S3),
                                (R12, R13, R23), ALPHA)
