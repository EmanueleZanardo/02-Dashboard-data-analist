"""Test tab446 '📏 Variance ratio: il prezzo segue un random walk?': registry + funzioni pure."""

import math
import random
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh446_num", "mh446_parse_serie", "mh446_mean",
           "mh446_sd", "mh446_autocorr", "mh446_vr", "mh446_phi",
           "mh446_phi_star", "mh446_norm_cdf", "mh446_norm_ppf",
           "mh446_smm_critico", "mh446_z", "mh446_joint",
           "mh446_verdetto", "mh446_mappa",
           "_mh446_vs", "_mh446_mu_s",
           "mh445_num", "mh445_parse_serie", "mh445_equity",
           "mh445_peaks", "mh445_drawdowns", "mh445_rolling",
           "mh445_window_dds", "mh445_worst_window",
           "mh445_verdetto", "mh445_mappa",
           "mh323_beta")

TITLE446 = "📏 Variance ratio: il prezzo segue un random walk?"
TITLE448 = "🔗 ECM: quanto in fretta power torna all'equilibrio col gas?"
TITLE450 = "📜 Scomposizione storica: cosa ha mosso davvero il prezzo power?"
TITLE452 = "📈 Previsione VECM(1): dove vanno power e gas nei prossimi H giorni?"
TITLE454 = "⚖️ Lo spread è stazionario? Test ADF"
TITLE456 = "💰 Vale la pena tradare il rientro? P&L atteso del trade"
TITLE473 = "🔁 Ribilanciare: i nuovi pesi post-shock"
TITLE474 = "⏰ Frequenza di ribilanciamento"
TITLE472 = "🔔 Drift dei budget: quando ribilanciare?"
TITLE471 = "🎯 Risk budgeting: ogni segnale si guadagna il suo capitale"
TITLE470 = "📈 Expected Shortfall: quanto perdi quando perdi?"
TITLE469 = "📊 VaR per segnale: chi mangia il capitale?"
TITLE468 = "📉 VaR annuale: quanto capitale di rischio?"
TITLE467 = "📅 L'edge annualizzato: il trade si ripete?"
TITLE466 = "💸 Costi veri: l'edge sopravvive al netto?"
TITLE465 = "📐 Correlazione: la diversificazione è reale?"
TITLE464 = "🧺 Portafoglio: quanti trade insieme?"
TITLE463 = "🔀 Scale-out: tutto insieme o a pezzi?"
TITLE462 = "⏳ Time stop: uscire se non succede niente"
TITLE461 = "🧭 Ottimizza stop/target: i migliori k"
TITLE460 = "🛑 Stop & target: dove chiudere il trade"
TITLE482 = "🗓️ Ladder delle scadenze: profilo temporale di volumi, MtM e DV01"
TITLE459 = "🧪⚠️ Stress test del trade: VaR sotto shock"
TITLE458 = "⚠️ Quanto posso perdere? VaR del trade dimensionato"
TITLE475 = "💰 Costo di esecuzione: quanto costa davvero ruotare"
TITLE445 = "🌀 Rolling drawdown: il peggior calo in ogni finestra"
TITLE447 = "⛓️ Johansen: power e gas cointegrati?"
TITLE449 = "💥 Risposta allo shock: di quanto uno shock del gas muove power?"
TITLE451 = "🌊 Spillover gas↔power: chi trasmette e chi riceve gli shock?"
TITLE453 = "📊 Backtest VECM(1): il modello batte il random walk?"
TITLE455 = "🔮 Quando rientra lo spread? Forecast mean-reversion"
TITLE457 = "📐 Quanto puntare sul rientro? Sizing Kelly del trade"
TITLE444 = "🏞️ Lake ratio: l'area del dolore sotto il picco"
TITLE443 = "💹 Gain-to-Pain ratio: guadagni totali per ogni punto perso"
TITLE442 = "📐 Calmar geometrico: CAGR composto per unita' di peggior drawdown"
TITLE441 = "📈 Recovery Factor: profitto totale per unita' di peggior drawdown"
TITLE440 = "🎯 Drawdown-at-Risk (DaR): la soglia di drawdown superata solo nell'alpha% dei casi"
TITLE439 = "📉 CDaR ratio: rendimento per unita' di coda media (Conditional Drawdown-at-Risk)"
TITLE438 = "🩹 Pain ratio: rendimento per unita' di dolore medio (Pain Index)"
TITLE437 = "📈 Sterling ratio: rendimento per unita' di drawdown medio annuo"
DEMO = '3.5\n3.9\n2.6\n4.3\n2.9\n4.8\n2.1\n3.7\n3.2\n4.5\n2.8\n2.4\n4.1\n3.6\n5.0\n2.3\n3.1\n3.8\n2.5\n4.6\n3.0\n4.2\n2.2\n3.4\n4.0\n2.7\n4.7\n3.3\n2.0\n4.4\n-9.5\n-7.2\n-14.0\n-8.3\n-6.1\n-10.2'
MEAN = 1.3416666666666666
SD = 4.898887345328755
VR2 = 1.7069227301824303
VR4 = 2.9442379519805755
VR8 = 4.107453887636591
VR16 = 4.459386895018877
Z2 = 4.2415363810945825
Z4 = 6.235433395435166
Z8 = 6.303066898820964
Z16 = 4.715519343036432
ZS2 = 2.457020416127494
ZS4 = 3.6406731017544747
ZS8 = 4.061871864925529
ZS16 = 3.728599783282759
P2 = 2.219948955706208e-05
P4 = 4.505289474820984e-10
P8 = 2.9181279614931555e-10
P16 = 2.4109498633073656e-06
PS2 = 0.014009472475297713
PS4 = 0.0002719262134180944
PS8 = 4.868079647124546e-05
PS16 = 0.0001925466661800712
ZMAX = 4.061871864925529
QMAX = 8
CRITICO = 2.4909151335179773
RHO1 = 0.7069227301824303
RHO2 = 0.658018418259689
RHO3 = 0.45167087689448193
RHO4 = 0.23059284315928805
BETA323 = -0.1642120376051979
S_DEMO = 863.9675
DN2 = 133.21006944444443
CRITICO_M1 = 1.959963986120195
CRITICO_M2 = 2.236476643336348
CRITICO_A01 = 3.0222020260312377
CRITICO_A10 = 2.226267729500008
RW_VR2 = 1.1612128034541205
RW_ZMAX = 1.4074362397610838
TREND_VR2 = 1.4337972113413393
TREND_ZMAX = 8.510667828382797
MR_VR2 = 0.6140457965871146
MR_ZMAX = 2.7384596768394682
ALT_VR2 = 0.026223421088247267
ALT_ZMAX = 7.601671826160126
TRENDFORTE_VR2 = 1.5329363882917562
TRENDFORTE_ZMAX = 10.299341843544875


def _serie_rw():
    rng = random.Random(20261014)
    return tuple(rng.gauss(0.0, 1.0) for _ in range(60))


def _serie_trend(seed):
    rng = random.Random(seed)
    return tuple(0.02 * t + rng.gauss(0.0, 0.3) for t in range(60))


def _serie_ar1(phi, seed):
    rng = random.Random(seed)
    out = [0.0]
    for _i in range(1, 60):
        out.append(phi * out[-1] + rng.gauss(0.0, 1.0))
    return tuple(out)


def _serie_alt():
    rng = random.Random(41)
    return tuple((1.0 if i % 2 == 0 else -1.0) + rng.gauss(0.0, 0.1)
                 for i in range(60))


class TestRegistry446:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 813
        assert "tab446" in dvars
        assert "tab446" in withs

    def test_titoli_allineati_437_438_439_440_441_442_443_444_445_446(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab437")] == TITLE437
        assert titoli[dvars.index("tab438")] == TITLE438
        assert titoli[dvars.index("tab439")] == TITLE439
        assert titoli[dvars.index("tab440")] == TITLE440
        assert titoli[dvars.index("tab441")] == TITLE441
        assert titoli[dvars.index("tab442")] == TITLE442
        assert titoli[dvars.index("tab443")] == TITLE443
        assert titoli[dvars.index("tab444")] == TITLE444
        assert titoli[dvars.index("tab445")] == TITLE445
        assert titoli[dvars.index("tab446")] == TITLE446

    def test_ultima_tab(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert "tab482" in dvars
        assert TITLE482 in titoli
        assert "tab478" in withs  # il blocco UI esiste (non deve essere l'ultimo: le tab si accumulano)


class TestVarianceRatio446:
    def _xs(self):
        return _F["mh446_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh446_mappa"](xs)
        assert abs(m["mean"] - MEAN) < 1e-12
        assert abs(m["sd"] - SD) < 1e-12
        assert m["n"] == 36
        assert m["qs"] == (2, 4, 8, 16)
        assert abs(m["vr2"] - VR2) < 1e-12
        assert abs(m["zmax"] - ZMAX) < 1e-12
        assert m["qmax"] == QMAX
        assert abs(m["critico"] - CRITICO) < 1e-12
        assert m["rifiuta"] is True
        assert m["verdetto"].startswith("TRENDING FORTE")
        assert len(m["rows"]) == 4
        for r, vr, z, zs, p, ps in zip(
                m["rows"],
                (VR2, VR4, VR8, VR16),
                (Z2, Z4, Z8, Z16),
                (ZS2, ZS4, ZS8, ZS16),
                (P2, P4, P8, P16),
                (PS2, PS4, PS8, PS16)):
            assert abs(r["vr"] - vr) < 1e-12
            assert abs(r["z"] - z) < 1e-12
            assert abs(r["z_star"] - zs) < 1e-12
            assert abs(r["p"] - p) < 1e-12
            assert abs(r["p_star"] - ps) < 1e-12
        assert [r["q"] for r in m["rows"]] == [2, 4, 8, 16]
        # demo: VR(2) = 1 + rho_1 = 1.7069 > 1.5, rifiuta ->
        # TRENDING FORTE; il massimo |z*| e' a q=8, non a q=2
        assert VR2 > 1.5
        assert QMAX == 8
        # VR crescente con q sulla demo (due regimi: 30 guadagni,
        # poi 6 perdite in fila)
        vrs = [r["vr"] for r in m["rows"]]
        for a, b in zip(vrs, vrs[1:]):
            assert b > a

    def test_identita_vr(self):
        xs = self._xs()
        n = len(xs)
        mu = sum(xs) / n
        d = [x - mu for x in xs]
        s = sum(v * v for v in d)
        # autocorrelazioni a mano (denominatore S)
        for k, rho in ((1, RHO1), (2, RHO2), (3, RHO3), (4, RHO4)):
            ck = sum(d[t] * d[t - k] for t in range(k, n))
            assert abs(ck / s - rho) < 1e-12
            assert abs(_F["mh446_autocorr"](xs, k) - rho) < 1e-12
        # VR a mano dalla forma autocorrelazioni: VR(2) = 1 + rho_1
        assert abs(_F["mh446_vr"](xs, 2) - (1.0 + RHO1)) < 1e-12
        assert abs(_F["mh446_vr"](xs, 4)
                   - (1.0 + 2.0 * ((1.0 - 1.0 / 4.0) * RHO1
                                   + (1.0 - 2.0 / 4.0) * RHO2
                                   + (1.0 - 3.0 / 4.0) * RHO3))) < 1e-12
        assert abs(_F["mh446_vr"](xs, 8) - VR8) < 1e-12
        assert abs(_F["mh446_vr"](xs, 16) - VR16) < 1e-12
        # VR(1) = 1.0 per costruzione
        assert _F["mh446_vr"](xs, 1) == 1.0
        # phi a mano: phi(q) = 2(2q-1)(q-1)/(3qN)
        for q in (2, 4, 8, 16):
            assert abs(_F["mh446_phi"](q, n)
                         - 2.0 * (2 * q - 1) * (q - 1)
                         / (3.0 * q * n)) < 1e-15
        # phi* a mano per q=2: [2(2-1)/2]^2 * delta_1 = delta_1
        d1 = sum(d[t] ** 2 * d[t - 1] ** 2 for t in range(1, n)) / (s * s)
        assert abs(_F["mh446_phi_star"](xs, 2) - d1) < 1e-15
        # z e z* a mano per q=2
        vr2 = _F["mh446_vr"](xs, 2)
        z2 = (vr2 - 1.0) / math.sqrt(_F["mh446_phi"](2, n))
        zs2 = (vr2 - 1.0) / math.sqrt(_F["mh446_phi_star"](xs, 2))
        assert abs(z2 - Z2) < 1e-12
        assert abs(zs2 - ZS2) < 1e-12
        # p-value a mano via erf
        assert abs(2.0 * (1.0 - 0.5 * (1.0 + math.erf(abs(z2)
                   / math.sqrt(2.0)))) - P2) < 1e-12
        # norm_cdf / norm_ppf: valori noti
        assert abs(_F["mh446_norm_cdf"](0.0) - 0.5) < 1e-15
        assert abs(_F["mh446_norm_cdf"](1.96) - 0.975) < 1e-3
        assert abs(_F["mh446_norm_ppf"](0.5) - 0.0) < 1e-12
        assert abs(_F["mh446_norm_ppf"](0.975) - 1.96) < 1e-4
        assert abs(_F["mh446_norm_ppf"](0.995) - 2.5758) < 1e-4
        # round-trip ppf(cdf(x)) = x
        for xv in (-2.5, -1.0, 0.3, 1.5, 2.8):
            assert abs(_F["mh446_norm_ppf"](
                _F["mh446_norm_cdf"](xv)) - xv) < 1e-6

    def test_z_robusto_vs_omoschedastico(self):
        xs = self._xs()
        # sulla demo (eteroschedastica: crash finale) lo z
        # omoschedastico sopravvaluta SEMPRE la significativita':
        # |z| > |z*| e p < p* per ogni q
        for q in (2, 4, 8, 16):
            r = _F["mh446_z"](xs, q)
            assert abs(r["z"]) > abs(r["z_star"]) + 1e-9
            assert r["p"] < r["p_star"]
            assert r["p_star"] < 0.05  # tutti i q rifiutano da soli
        # ma il test congiunto decide sul massimo, col critico SMM
        j = _F["mh446_joint"](xs)
        assert j["zmax"] == max(abs(_F["mh446_z"](xs, q)["z_star"])
                                for q in (2, 4, 8, 16))
        assert j["critico"] > 1.96  # correzione famiglia

    def test_joint_chow_denning(self):
        xs = self._xs()
        j = _F["mh446_joint"](xs)
        assert abs(j["zmax"] - ZMAX) < 1e-12
        assert j["qmax"] == QMAX
        assert abs(j["critico"] - CRITICO) < 1e-12
        assert j["rifiuta"] is True
        assert j["m"] == 4
        assert j["alpha"] == 0.05
        # critico SMM: m=1 -> 1.96 (normale), m=2 e m=4 piu' alti
        assert abs(_F["mh446_smm_critico"](1, 0.05) - CRITICO_M1) < 1e-9
        assert abs(_F["mh446_smm_critico"](2, 0.05) - CRITICO_M2) < 1e-9
        assert abs(_F["mh446_smm_critico"](4, 0.05) - CRITICO) < 1e-9
        assert CRITICO_M1 < CRITICO_M2 < CRITICO
        # alpha piu' basso = critico piu' alto
        assert abs(_F["mh446_smm_critico"](4, 0.01) - CRITICO_A01) < 1e-9
        assert abs(_F["mh446_smm_critico"](4, 0.10) - CRITICO_A10) < 1e-9
        assert CRITICO_A10 < CRITICO < CRITICO_A01
        # alpha cambia la decisione? sulla demo no (z*max 4.06
        # supera anche il critico all'1%)
        assert _F["mh446_joint"](xs, alpha=0.01)["rifiuta"] is True
        assert _F["mh446_joint"](xs, alpha=0.10)["rifiuta"] is True
        # griglia ridotta: il massimo resta, il critico scende
        j2 = _F["mh446_joint"](xs, qs=(2, 4))
        assert j2["m"] == 2
        assert j2["critico"] < CRITICO
        # griglia con duplicati: deduplicata
        jd = _F["mh446_joint"](xs, qs=(2, 2, 4, 8, 16, 16))
        assert jd["m"] == 4
        assert abs(jd["zmax"] - ZMAX) < 1e-12

    def test_crosscheck_445_323(self):
        xs = self._xs()
        m = _F["mh446_mappa"](xs)
        # stessa demo di tab445: media identica
        m445 = _F["mh445_mappa"](xs)
        assert abs(m445["mean"] - m["mean"]) < 1e-12
        assert abs(m445["mean"] - MEAN) < 1e-12
        # tab323: beta OLS a mano sui rendimenti == mh323_beta
        n = len(xs)
        mu = sum(xs) / n
        xsl = [v - mu for v in xs[:-1]]
        ys = [xs[t] - xs[t - 1] for t in range(1, n)]
        sxx = sum(v * v for v in xsl)
        beta_mano = sum(x * y for x, y in zip(xsl, ys)) / sxx
        assert abs(_F["mh323_beta"](xs)["beta"] - beta_mano) < 1e-12
        assert abs(beta_mano - BETA323) < 1e-12
        # identita' ESATTA: 1 + beta = rho_1 * S / (S - d_N^2)
        # (il denominatore OLS esclude l'ultimo termine)
        d = [v - mu for v in xs]
        s = sum(v * v for v in d)
        assert abs(s - S_DEMO) < 1e-9
        assert abs(d[-1] ** 2 - DN2) < 1e-9
        assert abs((1.0 + beta_mano)
                   - RHO1 * s / (s - d[-1] ** 2)) < 1e-12
        # la differenza tra 1+beta e rho_1 e' TUTTA nel
        # denominatore OLS (il crollo finale pesa 133.2 su S=864)
        assert abs((1.0 + beta_mano) - RHO1) > 0.1

    def test_verdetto_soglie(self):
        v = _F["mh446_verdetto"]
        assert v(1.1612, False).startswith("RANDOM WALK")
        assert v(0.5, False).startswith("RANDOM WALK")
        assert v(2.0, False).startswith("RANDOM WALK")
        assert v(1.2, True).startswith("TRENDING —")
        assert v(1.4999, True).startswith("TRENDING —")
        assert v(1.5, True).startswith("TRENDING FORTE")
        assert v(3.0, True).startswith("TRENDING FORTE")
        assert v(0.9, True).startswith("MEAN REVERSION —")
        assert v(0.6001, True).startswith("MEAN REVERSION —")
        assert v(0.6, True).startswith("MEAN REVERSION FORTE")
        assert v(0.1, True).startswith("MEAN REVERSION FORTE")
        assert v(1.0, True).startswith("MISTO")
        assert v(float("inf"), True).startswith("TRENDING FORTE")
        assert v(float("-inf"), True).startswith("MEAN REVERSION FORTE")
        assert v(float("inf"), False).startswith("RANDOM WALK")
        with pytest.raises(ValueError):
            v(float("nan"), True)
        with pytest.raises(ValueError):
            v("1.2", True)
        with pytest.raises(ValueError):
            v(1.2, 1)

    def test_degeneri(self):
        flat = tuple([0.0] * 25)
        gains = tuple([1.0] * 25)
        xs = self._xs()
        for bad in (lambda: _F["mh446_mappa"](flat),
                    lambda: _F["mh446_mappa"](gains),
                    lambda: _F["mh446_mappa"](tuple([2.5] * 30)),
                    lambda: _F["mh446_mappa"]((1.0,) * 19),
                    lambda: _F["mh446_mappa"](None),
                    lambda: _F["mh446_vr"](xs, 0),
                    lambda: _F["mh446_vr"](xs, 37),
                    lambda: _F["mh446_vr"](xs, "2"),
                    lambda: _F["mh446_vr"](xs, 2.5),
                    lambda: _F["mh446_z"](xs, 1),
                    lambda: _F["mh446_z"](xs, 37),
                    lambda: _F["mh446_joint"](xs, ()),
                    lambda: _F["mh446_joint"](xs, (1,)),
                    lambda: _F["mh446_joint"](xs, (37,)),
                    lambda: _F["mh446_joint"](xs, (2.5,)),
                    lambda: _F["mh446_autocorr"](xs, 0),
                    lambda: _F["mh446_autocorr"](xs, 36),
                    lambda: _F["mh446_phi"](1, 36),
                    lambda: _F["mh446_phi"](2, 19),
                    lambda: _F["mh446_phi_star"](xs, 1),
                    lambda: _F["mh446_norm_ppf"](0.0),
                    lambda: _F["mh446_norm_ppf"](1.0),
                    lambda: _F["mh446_norm_ppf"](-0.1),
                    lambda: _F["mh446_smm_critico"](0),
                    lambda: _F["mh446_smm_critico"](4, 0.0),
                    lambda: _F["mh446_smm_critico"](4, 1.0),
                    lambda: _F["mh446_verdetto"](float("nan"), True)):
            with pytest.raises(ValueError):
                bad()

    def test_serie_controllo(self):
        # RANDOM WALK: white noise gaussiano (seed 20261014) —
        # il test NON rifiuta
        mrw = _F["mh446_mappa"](_serie_rw())
        assert abs(mrw["vr2"] - RW_VR2) < 1e-9
        assert abs(mrw["zmax"] - RW_ZMAX) < 1e-9
        assert mrw["rifiuta"] is False
        assert mrw["verdetto"].startswith("RANDOM WALK")
        # TRENDING: drift + rumore (seed 783) — rifiuta,
        # VR(2) in (1, 1.5)
        mtr = _F["mh446_mappa"](_serie_trend(783))
        assert abs(mtr["vr2"] - TREND_VR2) < 1e-9
        assert abs(mtr["zmax"] - TREND_ZMAX) < 1e-9
        assert mtr["rifiuta"] is True
        assert mtr["verdetto"].startswith("TRENDING —")
        # TRENDING FORTE: drift + rumore (seed 777) — rifiuta,
        # VR(2) >= 1.5
        mtf = _F["mh446_mappa"](_serie_trend(777))
        assert abs(mtf["vr2"] - TRENDFORTE_VR2) < 1e-9
        assert abs(mtf["zmax"] - TRENDFORTE_ZMAX) < 1e-9
        assert mtf["rifiuta"] is True
        assert mtf["verdetto"].startswith("TRENDING FORTE")
        # MEAN REVERSION: AR(1) phi=-0.6 (seed 552) — rifiuta,
        # VR(2) in (0.6, 1)
        mmr = _F["mh446_mappa"](_serie_ar1(-0.6, 552))
        assert abs(mmr["vr2"] - MR_VR2) < 1e-9
        assert abs(mmr["zmax"] - MR_ZMAX) < 1e-9
        assert mmr["rifiuta"] is True
        assert mmr["verdetto"].startswith("MEAN REVERSION —")
        # MEAN REVERSION FORTE: alternata + rumore (seed 41) —
        # rifiuta, VR(2) <= 0.6
        malt = _F["mh446_mappa"](_serie_alt())
        assert abs(malt["vr2"] - ALT_VR2) < 1e-9
        assert abs(malt["zmax"] - ALT_ZMAX) < 1e-9
        assert malt["rifiuta"] is True
        assert malt["verdetto"].startswith("MEAN REVERSION FORTE")

    def test_parse_serie(self):
        xs = _F["mh446_parse_serie"]("1,5\n" + "2.5\n" * 19)
        assert len(xs) == 20
        assert xs[0] == 1.5 and xs[1] == 2.5
        with pytest.raises(ValueError):
            _F["mh446_parse_serie"]("1\n2\nabc\n" + "1\n" * 20)
        with pytest.raises(ValueError):
            _F["mh446_parse_serie"]("1\n2\n")

