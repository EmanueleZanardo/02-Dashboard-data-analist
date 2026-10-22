"""Test tab454 '⚖️ Lo spread è stazionario? Test ADF': registry + funzioni pure."""

import math
import random
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh454_num", "mh454_parse_serie", "mh454_adf",
           "mh454_critico", "mh454_verdetto", "mh454_mappa",
           "_mh454_seq", "_mh454_solve", "_mh454_ols",
           "mh447_num", "mh447_eig", "mh447_rango",
           "mh447_trace", "mh447_max", "mh447_critico", "_mh447_lam_T",
           "_mh447_seq", "_mh447_solve", "_mh447_mul",
           "_mh447_transp", "_mh447_ols")

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
TITLE453 = "📊 Backtest VECM(1): il modello batte il random walk?"
TITLE455 = "🔮 Quando rientra lo spread? Forecast mean-reversion"
TITLE457 = "📐 Quanto puntare sul rientro? Sizing Kelly del trade"
TITLE452 = "📈 Previsione VECM(1): dove vanno power e gas nei prossimi H giorni?"
TITLE451 = "🌊 Spillover gas↔power: chi trasmette e chi riceve gli shock?"
TITLE450 = "📜 Scomposizione storica: cosa ha mosso davvero il prezzo power?"
TITLE449 = "💥 Risposta allo shock: di quanto uno shock del gas muove power?"
TITLE448 = "🔗 ECM: quanto in fretta power torna all'equilibrio col gas?"
TITLE447 = "⛓️ Johansen: power e gas cointegrati?"
TITLE446 = "📏 Variance ratio: il prezzo segue un random walk?"
TITLE445 = "🌀 Rolling drawdown: il peggior calo in ogni finestra"
DEMO_POWER = '115.0\n114.222584\n115.526527\n115.270435\n115.404795\n113.275972\n114.840219\n116.685764\n115.420859\n113.571058\n112.06301\n112.194403\n116.139654\n117.765956\n116.742831\n116.62762\n115.739526\n117.414453\n114.867579\n116.640701\n115.779325\n115.137451\n116.642853\n117.253244\n117.493738\n117.242796\n118.334843\n119.091227\n116.768615\n115.421416\n116.033447\n114.144567\n113.700317\n114.354433\n114.876507\n113.755332\n115.568524\n116.069102\n116.138549\n117.333173\n117.084818\n116.63492\n117.999467\n117.718767\n117.668152\n118.796536\n116.597527\n114.618757\n114.130273\n116.852609\n116.128887\n119.874946\n118.472635\n119.958398\n119.950907\n122.309881\n121.085938\n120.106701\n119.684133\n119.645704\n'
DEMO_GAS = '40.0\n39.387964\n39.576758\n40.074258\n39.817653\n39.153163\n39.120398\n39.359404\n39.908497\n39.300559\n38.654127\n39.007091\n39.244134\n40.011027\n40.502256\n40.451366\n40.314247\n41.599511\n41.45511\n41.062643\n40.493471\n40.541201\n40.613858\n40.441425\n40.410346\n40.546892\n40.893091\n41.441492\n41.5464\n40.651509\n41.002372\n40.292523\n40.206815\n39.469916\n39.470967\n39.081684\n39.188627\n40.838781\n40.814478\n41.23564\n40.573978\n40.429951\n40.761193\n40.714858\n40.899949\n40.951613\n40.448546\n40.730418\n40.324405\n41.260281\n41.00768\n41.350726\n41.351901\n41.828116\n41.527041\n42.026474\n41.964525\n42.596178\n42.908275\n42.978922\n'
BETA = 1.8286056394998358
TSTAT = -4.322632779574823
GAMMA = -0.5846318659915757
SE_GAMMA = 0.1352490243339802
HALF = 0.7889312601051977
T15 = -4.089707814792808
T_RW = -2.1658595891845627
T_AR1 = -3.5290605880941546
SPREAD_MEAN = 42.356374118813505
SPREAD_STD = 1.2939388309490982


def _rw(seed, n=60):
    rng = random.Random(seed)
    out = [0.0]
    for _ in range(1, n):
        out.append(out[-1] + rng.gauss(0.0, 1.0))
    return tuple(out)


def _ar1(phi, seed, n=60):
    rng = random.Random(seed)
    out = [0.0]
    for _ in range(1, n):
        out.append(phi * out[-1] + rng.gauss(0.0, 1.0))
    return tuple(out)


class TestRegistry454:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 643
        assert "tab454" in dvars
        assert "tab454" in withs

    def test_titoli_allineati_445_446_447_448_449_450_451_452_453_454(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab445")] == TITLE445
        assert titoli[dvars.index("tab446")] == TITLE446
        assert titoli[dvars.index("tab447")] == TITLE447
        assert titoli[dvars.index("tab448")] == TITLE448
        assert titoli[dvars.index("tab449")] == TITLE449
        assert titoli[dvars.index("tab450")] == TITLE450
        assert titoli[dvars.index("tab451")] == TITLE451
        assert titoli[dvars.index("tab452")] == TITLE452
        assert titoli[dvars.index("tab453")] == TITLE453
        assert titoli[dvars.index("tab454")] == TITLE454

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


class TestADF454:
    def _pw(self):
        return _F["mh454_parse_serie"](DEMO_POWER)

    def _gs(self):
        return _F["mh454_parse_serie"](DEMO_GAS)

    def test_demo_valori(self):
        pw, gs = self._pw(), self._gs()
        assert len(pw) == 60 and len(gs) == 60
        assert pw[0] == 115.0 and gs[0] == 40.0
        m = _F["mh454_mappa"](pw, gs, lags=1)
        assert m["n"] == 60 and m["lags"] == 1 and m["T"] == 58
        assert abs(m["beta"] - BETA) < 1e-12
        assert abs(m["beta"] - 1.8286) < 1e-3  # Johansen tab447
        assert abs(m["t_stat"] - TSTAT) < 1e-12
        assert m["t_stat"] < -3.51  # rifiuto all'1%
        assert abs(m["gamma"] - GAMMA) < 1e-12
        assert abs(m["se_gamma"] - SE_GAMMA) < 1e-12
        assert abs(m["half_life"] - HALF) < 1e-12
        assert 0.5 < m["half_life"] < 1.5  # rientro in ~0.8 giorni
        assert abs(m["spread_mean"] - SPREAD_MEAN) < 1e-9
        assert abs(m["spread_std"] - SPREAD_STD) < 1e-9
        assert len(m["spread"]) == 60
        assert m["verdetto"].startswith("STAZIONARIO")
        assert (m["cv1"], m["cv5"], m["cv10"]) == (-3.51, -2.89, -2.58)

    def test_definizione_a_mano(self):
        # ADF indipendente: demean, OLS con loop espliciti, t-stat
        # con formula indipendente
        pw, gs = self._pw(), self._gs()
        n = len(pw)
        sp = [p - BETA * g for p, g in zip(pw, gs)]
        mu = sum(sp) / n
        y = [v - mu for v in sp]
        dy = [y[t] - y[t - 1] for t in range(1, n)]
        lags = 1
        Z = [[1.0, y[t - 1], dy[t - 2]] for t in range(lags + 1, n)]
        Y = [dy[t - 1] for t in range(lags + 1, n)]
        T = len(Z)
        k = 3
        xtx = [[sum(Z[t][i] * Z[t][j] for t in range(T))
                for j in range(k)] for i in range(k)]
        xty = [sum(Z[t][i] * Y[t] for t in range(T)) for i in range(k)]
        # solve 3x3 esplicito (Cramer via Gauss-Jordan a mano)
        aug = [xtx[i][:] + [xty[i]] for i in range(k)]
        for col in range(k):
            piv = max(range(col, k), key=lambda r: abs(aug[r][col]))
            aug[col], aug[piv] = aug[piv], aug[col]
            pv = aug[col][col]
            assert abs(pv) > 1e-12
            aug[col] = [v / pv for v in aug[col]]
            for r in range(k):
                if r != col:
                    f = aug[r][col]
                    aug[r] = [v - f * w
                              for v, w in zip(aug[r], aug[col])]
        b = [row[k] for row in aug]
        resid = [Y[t] - sum(Z[t][i] * b[i] for i in range(k))
                 for t in range(T)]
        s2 = sum(r * r for r in resid) / (T - k)
        # inversa 3x3 a mano
        aug2 = [xtx[i][:] + [1.0 if i == j else 0.0 for j in range(k)]
                for i in range(k)]
        for col in range(k):
            piv = max(range(col, k), key=lambda r: abs(aug2[r][col]))
            aug2[col], aug2[piv] = aug2[piv], aug2[col]
            pv = aug2[col][col]
            aug2[col] = [v / pv for v in aug2[col]]
            for r in range(k):
                if r != col:
                    f = aug2[r][col]
                    aug2[r] = [v - f * w
                               for v, w in zip(aug2[r], aug2[col])]
        inv = [row[k:] for row in aug2]
        gamma_mano = b[1]
        se_mano = math.sqrt(s2 * inv[1][1])
        t_mano = gamma_mano / se_mano
        m = _F["mh454_mappa"](pw, gs, lags=1)
        assert abs(m["gamma"] - gamma_mano) < 1e-9
        assert abs(m["se_gamma"] - se_mano) < 1e-9
        assert abs(m["t_stat"] - t_mano) < 1e-9
        assert abs(t_mano - TSTAT) < 1e-9
        hl_mano = math.log(0.5) / math.log(1.0 + gamma_mano)
        assert abs(m["half_life"] - hl_mano) < 1e-9

    def test_chiave_coerenza_tab447(self):
        # la beta usata dall'ADF coincide con mh447_eig sul campione
        pw, gs = self._pw(), self._gs()
        m = _F["mh454_mappa"](pw, gs, lags=1)
        e = _F["mh447_eig"](pw, gs)
        assert abs(m["beta"] - e["beta"]) < 1e-12

    def test_chiave_beta_vera(self):
        # con la beta VERA (1.5) lo spread e' lo stesso AR(1) del DGP:
        # il test rifiuta comunque all'1%
        pw, gs = self._pw(), self._gs()
        m = _F["mh454_mappa"](pw, gs, beta=1.5, lags=1)
        assert abs(m["t_stat"] - T15) < 1e-12
        assert m["t_stat"] < -3.51
        assert m["verdetto"].startswith("STAZIONARIO")

    def test_controlli(self):
        # RANDOM WALK (radice unitaria): l'ADF NON deve rifiutare
        t_rw = _F["mh454_adf"](_rw(7))["t_stat"]
        assert abs(t_rw - T_RW) < 1e-12
        assert t_rw > -2.58
        assert _F["mh454_verdetto"](t_rw).startswith(
            "PROBABILMENTE NON STAZIONARIO")
        # AR(1) phi = 0.6 (stazionario): l'ADF deve rifiutare al 5%
        t_ar = _F["mh454_adf"](_ar1(0.6, 7))["t_stat"]
        assert abs(t_ar - T_AR1) < 1e-12
        assert t_ar < -2.89
        assert _F["mh454_verdetto"](t_ar).startswith("STAZIONARIO")

    def test_verdetto_soglie(self):
        v = _F["mh454_verdetto"]
        assert v(-4.32).startswith("STAZIONARIO")
        assert v(-3.52).startswith("STAZIONARIO")
        assert v(-3.51).startswith("PROBABILMENTE STAZIONARIO")
        assert v(-2.90).startswith("PROBABILMENTE STAZIONARIO")
        assert v(-2.89).startswith("DUBBIO")
        assert v(-2.59).startswith("DUBBIO")
        assert v(-2.58).startswith("PROBABILMENTE NON STAZIONARIO")
        assert v(-0.01).startswith("PROBABILMENTE NON STAZIONARIO")
        assert v(0.0).startswith("NON STAZIONARIO")
        assert v(1.5).startswith("NON STAZIONARIO")
        for bad in (lambda: v(float("nan")),
                    lambda: v(float("inf")),
                    lambda: v("x"),
                    lambda: v(True),
                    lambda: v(None)):
            with pytest.raises(ValueError):
                bad()

    def test_critico(self):
        c = _F["mh454_critico"]
        assert (c(1), c(5), c(10)) == (-3.51, -2.89, -2.58)
        for bad in (lambda: c(2), lambda: c("5"), lambda: c(None)):
            with pytest.raises(ValueError):
                bad()

    def test_degeneri(self):
        pw, gs = self._pw(), self._gs()
        flat = tuple([5.0] * 40)
        for bad in (lambda: _F["mh454_mappa"](tuple([1.0] * 29),
                                              tuple([1.0] * 29)),
                    lambda: _F["mh454_mappa"](None, gs),
                    lambda: _F["mh454_mappa"](pw, None),
                    lambda: _F["mh454_mappa"](pw, gs[:50]),
                    lambda: _F["mh454_mappa"](pw, gs + (1.0,)),
                    lambda: _F["mh454_mappa"](flat, gs),
                    lambda: _F["mh454_mappa"](pw, flat),
                    lambda: _F["mh454_mappa"](pw, pw),
                    lambda: _F["mh454_mappa"](pw, gs,
                                              beta=float("nan")),
                    lambda: _F["mh454_mappa"](pw, gs, beta="1.5"),
                    lambda: _F["mh454_mappa"](_rw(20261014),
                                              _rw(777)),
                    lambda: _F["mh454_mappa"](_ar1(0.5, 20261014),
                                              _ar1(0.5, 777)),
                    lambda: _F["mh454_adf"](flat),
                    lambda: _F["mh454_adf"](pw, lags=-1),
                    lambda: _F["mh454_adf"](pw, lags=5),
                    lambda: _F["mh454_adf"](pw, lags=1.0),
                    lambda: _F["mh454_adf"](pw, lags=True),
                    lambda: _F["mh454_num"](float("nan"), "x"),
                    lambda: _F["mh454_num"](True, "x"),
                    lambda: _F["mh454_num"]("1.5", "x")):
            with pytest.raises(ValueError):
                bad()
        # lags = 0: Dickey-Fuller semplice, funziona lo stesso
        m0 = _F["mh454_mappa"](pw, gs, lags=0)
        assert m0["T"] == 59 and m0["lags"] == 0
        assert m0["t_stat"] < -3.51

    def test_parse_serie(self):
        xs = _F["mh454_parse_serie"]("1,5\n" + "2.5\n" * 29)
        assert len(xs) == 30
        assert xs[0] == 1.5 and xs[1] == 2.5
        with pytest.raises(ValueError):
            _F["mh454_parse_serie"]("1\n2\nabc\n" + "1\n" * 30)
        with pytest.raises(ValueError):
            _F["mh454_parse_serie"]("1\n2\n")
        with pytest.raises(ValueError):
            _F["mh454_parse_serie"](None)

    def test_solve(self):
        X = _F["_mh454_solve"]([[2.0, 1.0], [1.0, 3.0]],
                               [[5.0], [10.0]])
        assert abs(X[0][0] - 1.0) < 1e-12
        assert abs(X[1][0] - 3.0) < 1e-12
        with pytest.raises(ValueError):
            _F["_mh454_solve"]([[1.0, 2.0], [2.0, 4.0]],
                               [[1.0], [1.0]])

