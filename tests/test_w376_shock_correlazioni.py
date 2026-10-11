"""Test tab376 'Shock correlazioni: stress test sul rischio di coda': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh376_num", "mh376_z", "mh376_phi", "mh376_es_mult",
           "mh376_cov", "mh376_vol_port", "mh376_dot",
           "mh376_marginal_es", "mh376_component", "mh376_standalone_es",
           "mh376_shock_rho", "mh376_scenario", "mh376_verdetto",
           "mh376_analisi")

TITLE376 = "Shock correlazioni: stress test sul rischio di coda"
TITLE377 = "Backtest VaR di Kupiec: copertura e likelihood ratio"
TITLE378 = "Reverse stress test: quanto shock regge il limite?"
TITLE379 = "Mappa di rottura: superficie VaR su shock congiunti vol+corr"
TITLE380 = "Liquidity-adjusted VaR: VaR + costo di liquidazione"
TITLE381 = "Component VaR: attribution del VaR per asset"
TITLE382 = "Hedge VaR: copertura ottimale con futures"
TITLE383 = "Jump VaR: VaR con salti di prezzo (Merton)"
TITLE384 = "Delta-Gamma VaR: VaR parametrico di una posizione con opzioni"
TITLE375 = "Component ES: contributo al rischio di coda per posizione"
TITLE374 = "Component VaR: contributo al rischio per posizione"
TITLE373 = "Kelly con limite VaR: sizing con vincolo di perdita massima"
TITLE372 = "Monte Carlo: VaR e Expected Shortfall di una posizione power"
TITLE371 = "Kelly frazionario: frazione ottima per un budget di volatilità"
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
K = 0.5
Z = 1.6448536269514715
MULT = 2.062712807507429
V1 = 1500.0
V2 = 1600.0
V3 = 600.0
SIGMAP = 3059.0848304680926
ESP = 6310.0134590582265
VARP = 5031.746778547669
RSH1 = 0.8
RSH2 = 0.65
RSH3 = 0.7
SIGSH = 3394.701754204631
ESSH = 7002.294786065828
CB1 = 2670.1916325999764
CB2 = 2956.090938716741
CB3 = 683.7308877415092
CS1 = 2889.2668958471895
CS2 = 3130.494857498364
CS3 = 982.5330327202746
D1 = 219.07526324721312
D2 = 174.4039187816229
D3 = 298.80214497876545
CORRRISK = 692.2813270076012
CORRPCT = 0.10971154522876797
VULNI = 2
VULNDELTA = 298.80214497876545
BENEFIT = 1322.0239287192599
BENSH = 629.7426017116586
TERM0ES = 6310.0134590582265
TERM4ES = 7632.037387777486
VERDETTO = "ESPOSTO: sotto stress di correlazione l'ES cresce tra 10% e 25%"


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry376:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 384
        assert "tab376" in dvars
        assert "tab376" in withs

    def test_titoli_allineati_371_372_373_374_375_376(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab371")] == TITLE371
        assert titoli[dvars.index("tab372")] == TITLE372
        assert titoli[dvars.index("tab373")] == TITLE373
        assert titoli[dvars.index("tab374")] == TITLE374
        assert titoli[dvars.index("tab375")] == TITLE375
        assert titoli[dvars.index("tab376")] == TITLE376

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab384"
        assert titoli[-1] == TITLE384
        assert withs[-1] == "tab384"


class TestNum:
    def test_num_ok(self):
        assert _F["mh376_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh376_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh376_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh376_num"](float("inf"), "x")


class TestZPhi:
    def test_demo_z(self):
        assert _F["mh376_z"](ALPHA) == pytest.approx(Z)

    def test_phi_zero(self):
        assert _F["mh376_phi"](0.0) == pytest.approx(
            1.0 / math.sqrt(2.0 * math.pi))

    def test_es_mult_demo(self):
        assert _F["mh376_es_mult"](ALPHA) == pytest.approx(MULT)
        assert MULT == pytest.approx(_F["mh376_phi"](Z) / (1.0 - ALPHA))

    def test_es_mult_cresce_con_confidenza(self):
        assert _F["mh376_es_mult"](0.99) > _F["mh376_es_mult"](0.95)


class TestShockRho:
    def test_identita_k_zero(self):
        assert _F["mh376_shock_rho"](R12, R13, R23, 0.0) == (R12, R13, R23)

    def test_meltdown_k_uno(self):
        assert _F["mh376_shock_rho"](R12, R13, R23, 1.0) == (1.0, 1.0, 1.0)

    def test_demo_forma_chiusa(self):
        rsh = _F["mh376_shock_rho"](R12, R13, R23, K)
        assert rsh == pytest.approx((RSH1, RSH2, RSH3))
        # forma chiusa rho' = (1-k)*rho + k
        assert RSH1 == pytest.approx((1.0 - K) * R12 + K)
        assert RSH2 == pytest.approx((1.0 - K) * R13 + K)
        assert RSH3 == pytest.approx((1.0 - K) * R23 + K)

    def test_k_negativo_ko(self):
        with pytest.raises(ValueError):
            _F["mh376_shock_rho"](R12, R13, R23, -0.1)

    def test_k_sopra_uno_ko(self):
        with pytest.raises(ValueError):
            _F["mh376_shock_rho"](R12, R13, R23, 1.1)

    def test_rho_fuori_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh376_shock_rho"](1.5, R13, R23, K)


class TestScenario:
    def _b(self):
        return _F["mh376_scenario"]((E1, E2, E3), (S1, S2, S3),
                                   (R12, R13, R23), ALPHA, 0.0)

    def test_base_demo(self):
        b = self._b()
        assert b["z"] == pytest.approx(Z)
        assert b["es_mult"] == pytest.approx(MULT)
        assert b["sigma"] == pytest.approx(SIGMAP)
        assert b["es"] == pytest.approx(ESP)
        assert b["var_p"] == pytest.approx(VARP)
        assert b["v"] == pytest.approx((V1, V2, V3))
        assert b["ces"] == pytest.approx((CB1, CB2, CB3))
        assert b["benefit"] == pytest.approx(BENEFIT)
        assert b["r_sh"] == pytest.approx((R12, R13, R23))

    def test_eulero_base(self):
        b = self._b()
        assert sum(b["ces"]) == pytest.approx(b["es"])

    def test_k_uno_meltdown(self):
        s = _F["mh376_scenario"]((E1, E2, E3), (S1, S2, S3),
                                 (R12, R13, R23), ALPHA, 1.0)
        # meltdown: sigma = somma v, beneficio azzerato
        assert s["sigma"] == pytest.approx(V1 + V2 + V3)
        assert s["es"] == pytest.approx(MULT * (V1 + V2 + V3))
        assert s["benefit"] == pytest.approx(0.0, abs=1e-6)

    def test_lunghezze_ko(self):
        with pytest.raises(ValueError):
            _F["mh376_scenario"]((E1, E2), (S1, S2, S3),
                                 (R12, R13, R23), ALPHA, K)


class TestShock:
    def _a(self):
        return _F["mh376_analisi"]((E1, E2, E3), (S1, S2, S3),
                                  (R12, R13, R23), ALPHA, K)

    def test_demo_shock(self):
        a = self._a()
        assert a["r_sh"] == pytest.approx((RSH1, RSH2, RSH3))
        assert a["sigma_sh"] == pytest.approx(SIGSH)
        assert a["es_sh"] == pytest.approx(ESSH)
        assert a["ces_sh"] == pytest.approx((CS1, CS2, CS3))
        assert a["delta"] == pytest.approx((D1, D2, D3))

    def test_eulero_shock(self):
        a = self._a()
        assert sum(a["ces_sh"]) == pytest.approx(a["es_sh"])

    def test_shock_aumenta_rischio(self):
        a = self._a()
        assert a["sigma_sh"] > a["sigma_p"]
        assert a["es_sh"] > a["es_p"]

    def test_rischio_correlazione(self):
        a = self._a()
        assert a["corr_risk"] == pytest.approx(CORRRISK)
        assert a["corr_risk"] == pytest.approx(a["es_sh"] - a["es_p"])
        assert a["corr_risk"] >= 0.0
        assert a["corr_risk_pct"] == pytest.approx(CORRPCT)
        assert a["corr_risk_pct"] == pytest.approx(
            a["corr_risk"] / a["es_p"])

    def test_vulnerabile(self):
        a = self._a()
        assert a["vuln_i"] == VULNI
        assert a["vuln_delta"] == pytest.approx(VULNDELTA)
        assert a["vuln_delta"] == pytest.approx(a["delta"][a["vuln_i"]])
        # il vulnerabile e' il max dei delta
        assert a["vuln_i"] == max(range(3), key=lambda i: a["delta"][i])

    def test_benefit_residuo(self):
        a = self._a()
        assert a["benefit_sh"] == pytest.approx(BENSH)
        assert a["benefit_sh"] < a["benefit"]

    def test_termometro(self):
        a = self._a()
        tm = a["termometro"]
        assert len(tm) == 5
        assert [t["k"] for t in tm] == [0.0, 0.25, 0.5, 0.75, 1.0]
        assert tm[0]["es"] == pytest.approx(TERM0ES)
        assert tm[0]["es"] == pytest.approx(a["es_p"])
        assert tm[4]["es"] == pytest.approx(TERM4ES)
        assert tm[4]["benefit"] == pytest.approx(0.0, abs=1e-6)
        for j in range(4):
            assert tm[j + 1]["es"] > tm[j]["es"]
            assert tm[j + 1]["benefit"] < tm[j]["benefit"]

    def test_k_ko(self):
        with pytest.raises(ValueError):
            _F["mh376_analisi"]((E1, E2, E3), (S1, S2, S3),
                                (R12, R13, R23), ALPHA, 1.5)


class TestVerdetto:
    def test_resiliente(self):
        assert _F["mh376_verdetto"](0.05).startswith("RESILIENTE")
        assert _F["mh376_verdetto"](0.099).startswith("RESILIENTE")

    def test_esposto(self):
        assert _F["mh376_verdetto"](0.10).startswith("ESPOSTO")
        assert _F["mh376_verdetto"](0.249).startswith("ESPOSTO")

    def test_fragile(self):
        assert _F["mh376_verdetto"](0.25).startswith("FRAGILE")
        assert _F["mh376_verdetto"](0.90).startswith("FRAGILE")

    def test_negativo_ko(self):
        with pytest.raises(ValueError):
            _F["mh376_verdetto"](-0.01)


class TestAnalisi:
    def _a(self):
        return _F["mh376_analisi"]((E1, E2, E3), (S1, S2, S3),
                                  (R12, R13, R23), ALPHA, K)

    def test_demo_completa(self):
        a = self._a()
        assert a["k"] == pytest.approx(K)
        assert a["sigma_p"] == pytest.approx(SIGMAP)
        assert a["es_p"] == pytest.approx(ESP)
        assert a["verdetto"] == VERDETTO

    def test_demo_verdetto(self):
        a = self._a()
        # k=50% -> rischio correlazione ~10.97% -> ESPOSTO,
        # vulnerabile = EUA CO2 (indice 2)
        assert a["vuln_i"] == 2
        assert 0.10 <= a["corr_risk_pct"] < 0.25
        assert a["verdetto"].startswith("ESPOSTO")

    def test_num_ok(self):
        assert _F["mh376_num"](5.0, "x") == 5.0

    def test_lunghezze_ko(self):
        with pytest.raises(ValueError):
            _F["mh376_analisi"]((E1, E2), (S1, S2, S3),
                                (R12, R13, R23), ALPHA, K)
