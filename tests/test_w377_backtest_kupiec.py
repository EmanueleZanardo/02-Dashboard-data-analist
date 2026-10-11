"""Test tab377 'Backtest VaR di Kupiec: copertura e likelihood ratio': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh377_num", "mh377_z", "mh377_chi2_1_sf", "mh377_sim_gbm",
           "mh377_log_returns", "mh377_var_par", "mh377_kupiec",
           "mh377_basel_zone", "mh377_verdetto", "mh377_backtest")

TITLE377 = "Backtest VaR di Kupiec: copertura e likelihood ratio"
TITLE378 = "Reverse stress test: quanto shock regge il limite?"
TITLE379 = "Mappa di rottura: superficie VaR su shock congiunti vol+corr"
TITLE380 = "Liquidity-adjusted VaR: VaR + costo di liquidazione"
TITLE381 = "Component VaR: attribution del VaR per asset"
TITLE382 = "Hedge VaR: copertura ottimale con futures"
TITLE383 = "Jump VaR: VaR con salti di prezzo (Merton)"
TITLE384 = "Delta-Gamma VaR: VaR parametrico di una posizione con opzioni"
TITLE385 = "Expected Shortfall: misura di rischio coerente"
TITLE386 = "VaR ed ES con code pesanti (t-Student)"
TITLE387 = "🌈📉 Misura spettrale: l'ES pesato con l'avversione al rischio"
TITLE388 = "🧲📈 Misura entropica: rischio con avversione costante (CARA)"
TITLE376 = "Shock correlazioni: stress test sul rischio di coda"
TITLE375 = "Component ES: contributo al rischio di coda per posizione"
TITLE374 = "Component VaR: contributo al rischio per posizione"
TITLE373 = "Kelly con limite VaR: sizing con vincolo di perdita massima"
TITLE372 = "Monte Carlo: VaR e Expected Shortfall di una posizione power"
S0 = 100.0
MU = 0.05
SIG = 0.2
N = 250
SEED = 7
ALPHA = 0.99
Z = 2.3263478740408408
SIGD = 0.012906200153838396
VARF = 0.030024311289827525
T = 4
LR = 0.7691383643858458
PV = 0.380483738238954
EXP = 2.500000000000002
ZONE = 'VERDE: 4 violazioni su 250 entro la soglia (4) - modello adeguato'
VERDETTO = "ACCETTABILE: il tasso di violazioni e' compatibile con il VaR (p >= 10%)"
P0 = 100.0
PN = 119.54918615981961
RET0 = -0.003116658079341123


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry377:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 388
        assert "tab377" in dvars
        assert "tab377" in withs

    def test_titoli_allineati_372_373_374_375_376_377(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab372")] == TITLE372
        assert titoli[dvars.index("tab373")] == TITLE373
        assert titoli[dvars.index("tab374")] == TITLE374
        assert titoli[dvars.index("tab375")] == TITLE375
        assert titoli[dvars.index("tab376")] == TITLE376
        assert titoli[dvars.index("tab377")] == TITLE377

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab388"
        assert titoli[-1] == TITLE388
        assert withs[-1] == "tab388"


class TestNum:
    def test_num_ok(self):
        assert _F["mh377_num"](0.5, "x") == 0.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh377_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh377_num"](float("nan"), "x")

    def test_num_inf_ko(self):
        with pytest.raises(ValueError):
            _F["mh377_num"](float("inf"), "x")


class TestZChi2:
    def test_z_demo(self):
        assert _F["mh377_z"](ALPHA) == pytest.approx(Z)

    def test_z_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh377_z"](0.5)

    def test_chi2_sf_zero(self):
        assert _F["mh377_chi2_1_sf"](0.0) == pytest.approx(1.0)

    def test_chi2_sf_forma_chiusa(self):
        assert _F["mh377_chi2_1_sf"](1.0) == pytest.approx(
            math.erfc(math.sqrt(0.5)))

    def test_chi2_sf_decresce(self):
        assert _F["mh377_chi2_1_sf"](0.5) > _F["mh377_chi2_1_sf"](5.0)

    def test_chi2_sf_negativo_ko(self):
        with pytest.raises(ValueError):
            _F["mh377_chi2_1_sf"](-0.1)


class TestSim:
    def test_demo_struttura(self):
        p = _F["mh377_sim_gbm"](S0, MU, SIG, N, SEED)
        assert len(p) == N + 1
        assert p[0] == pytest.approx(P0)
        assert p[-1] == pytest.approx(PN)
        assert all(x > 0.0 for x in p)

    def test_riproducibile(self):
        a = _F["mh377_sim_gbm"](S0, MU, SIG, N, SEED)
        b = _F["mh377_sim_gbm"](S0, MU, SIG, N, SEED)
        assert a == b

    def test_seed_diverso_serie_diversa(self):
        a = _F["mh377_sim_gbm"](S0, MU, SIG, N, SEED)
        b = _F["mh377_sim_gbm"](S0, MU, SIG, N, SEED + 1)
        assert a != b

    def test_log_returns(self):
        p = _F["mh377_sim_gbm"](S0, MU, SIG, N, SEED)
        r = _F["mh377_log_returns"](p)
        assert len(r) == N
        assert r[0] == pytest.approx(RET0)
        assert r[0] == pytest.approx(math.log(p[1] / p[0]))

    def test_s0_ko(self):
        with pytest.raises(ValueError):
            _F["mh377_sim_gbm"](0.0, MU, SIG, N, SEED)

    def test_sigma_negativa_ko(self):
        with pytest.raises(ValueError):
            _F["mh377_sim_gbm"](S0, MU, -0.1, N, SEED)

    def test_n_troppo_piccolo_ko(self):
        with pytest.raises(ValueError):
            _F["mh377_sim_gbm"](S0, MU, SIG, 29, SEED)

    def test_seed_non_intero_ko(self):
        with pytest.raises(ValueError):
            _F["mh377_sim_gbm"](S0, MU, SIG, N, 7.5)

    def test_prezzi_non_positivi_ko(self):
        with pytest.raises(ValueError):
            _F["mh377_log_returns"]((100.0, 0.0, 101.0))


class TestKupiec:
    def test_demo(self):
        assert _F["mh377_kupiec"](N, T, 1.0 - ALPHA) == pytest.approx(LR)
        assert LR >= 0.0

    def test_forma_chiusa(self):
        p = 1.0 - ALPHA
        nn, tt = N, T
        def _lnl(nn_, tt_, pp_):
            a = tt_ * math.log(pp_) if tt_ > 0 else 0.0
            b = (nn_ - tt_) * math.log(1.0 - pp_) if tt_ < nn_ else 0.0
            return a + b
        ph = tt / nn
        ph = max(min(ph, 1.0 - 1e-12), 1e-12)
        att = max(-2.0 * (_lnl(nn, tt, p) - _lnl(nn, tt, ph)), 0.0)
        assert _F["mh377_kupiec"](nn, tt, p) == pytest.approx(att)

    def test_zero_violazioni(self):
        lr = _F["mh377_kupiec"](250, 0, 0.01)
        assert lr >= 0.0 and math.isfinite(lr)

    def test_tutte_violazioni(self):
        lr = _F["mh377_kupiec"](250, 250, 0.01)
        assert lr >= 0.0 and math.isfinite(lr)

    def test_t_sopra_n_ko(self):
        with pytest.raises(ValueError):
            _F["mh377_kupiec"](250, 251, 0.01)

    def test_p_fuori_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh377_kupiec"](250, 3, 1.0)


class TestBasel:
    def test_verde(self):
        assert _F["mh377_basel_zone"](250, 4).startswith("VERDE")
        assert _F["mh377_basel_zone"](250, 0).startswith("VERDE")

    def test_giallo(self):
        assert _F["mh377_basel_zone"](250, 5).startswith("GIALLO")
        assert _F["mh377_basel_zone"](250, 9).startswith("GIALLO")

    def test_rosso(self):
        assert _F["mh377_basel_zone"](250, 10).startswith("ROSSO")
        assert _F["mh377_basel_zone"](250, 50).startswith("ROSSO")

    def test_scaling_n(self):
        # N=500: soglie doppie (8/18)
        assert _F["mh377_basel_zone"](500, 8).startswith("VERDE")
        assert _F["mh377_basel_zone"](500, 9).startswith("GIALLO")


class TestVerdetto:
    def test_accettabile(self):
        assert _F["mh377_verdetto"](0.10).startswith("ACCETTABILE")
        assert _F["mh377_verdetto"](0.99).startswith("ACCETTABILE")

    def test_dubbio(self):
        assert _F["mh377_verdetto"](0.05).startswith("DUBBIO")
        assert _F["mh377_verdetto"](0.0999).startswith("DUBBIO")

    def test_rifiutato(self):
        assert _F["mh377_verdetto"](0.0499).startswith("RIFIUTATO")
        assert _F["mh377_verdetto"](0.0).startswith("RIFIUTATO")

    def test_fuori_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh377_verdetto"](1.5)


class TestBacktest:
    def _b(self):
        return _F["mh377_backtest"](S0, MU, SIG, N, SEED, ALPHA)

    def test_demo_completa(self):
        b = self._b()
        assert b["n"] == N
        assert b["seed"] == SEED
        assert b["alpha"] == pytest.approx(ALPHA)
        assert b["z"] == pytest.approx(Z)
        assert b["sigma_daily"] == pytest.approx(SIGD)
        assert b["var_frac"] == pytest.approx(VARF)
        assert b["T"] == T
        assert b["lr"] == pytest.approx(LR)
        assert b["pvalue"] == pytest.approx(PV)
        assert b["attese"] == pytest.approx(EXP)
        assert b["basel"] == ZONE
        assert b["verdetto"] == VERDETTO

    def test_violazioni_conteggio_manuale(self):
        b = self._b()
        att = sum(1 for r in b["rendimenti"] if r < -b["var_frac"])
        assert b["T"] == att

    def test_pvalue_forma_chiusa(self):
        b = self._b()
        assert b["pvalue"] == pytest.approx(
            math.erfc(math.sqrt(b["lr"] / 2.0)))
        assert 0.0 < b["pvalue"] <= 1.0

    def test_sigma_daily_forma_chiusa(self):
        import statistics
        b = self._b()
        assert b["sigma_daily"] == pytest.approx(
            statistics.stdev(b["rendimenti"]))
        assert b["var_frac"] == pytest.approx(b["z"] * b["sigma_daily"])

    def test_alpha_ko(self):
        with pytest.raises(ValueError):
            _F["mh377_backtest"](S0, MU, SIG, N, SEED, 0.5)

    def test_num_ok(self):
        assert _F["mh377_num"](5.0, "x") == 5.0
