"""Test tab455 '🔮 Quando rientra lo spread? Forecast mean-reversion': registry + funzioni pure."""

import math
import random
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh455_num", "mh455_parse_serie", "mh455_ar1",
           "mh455_forecast", "mh455_verdetto", "mh455_mappa",
           "_mh455_seq", "_mh455_solve", "_mh455_ols",
           "mh447_num", "mh447_eig", "mh447_rango",
           "mh447_trace", "mh447_max", "mh447_critico", "_mh447_lam_T",
           "_mh447_seq", "_mh447_solve", "_mh447_mul",
           "_mh447_transp", "_mh447_ols",
           "mh454_num", "mh454_adf", "mh454_critico",
           "_mh454_seq", "_mh454_solve", "_mh454_ols")

TITLE455 = "🔮 Quando rientra lo spread? Forecast mean-reversion"
TITLE457 = "📐 Quanto puntare sul rientro? Sizing Kelly del trade"
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
TITLE452 = "📈 Previsione VECM(1): dove vanno power e gas nei prossimi H giorni?"
TITLE451 = "🌊 Spillover gas↔power: chi trasmette e chi riceve gli shock?"
TITLE450 = "📜 Scomposizione storica: cosa ha mosso davvero il prezzo power?"
TITLE449 = "💥 Risposta allo shock: di quanto uno shock del gas muove power?"
TITLE448 = "🔗 ECM: quanto in fretta power torna all'equilibrio col gas?"
TITLE447 = "⛓️ Johansen: power e gas cointegrati?"
TITLE446 = "📏 Variance ratio: il prezzo segue un random walk?"
DEMO_POWER = '115.0\n114.222584\n115.526527\n115.270435\n115.404795\n113.275972\n114.840219\n116.685764\n115.420859\n113.571058\n112.06301\n112.194403\n116.139654\n117.765956\n116.742831\n116.62762\n115.739526\n117.414453\n114.867579\n116.640701\n115.779325\n115.137451\n116.642853\n117.253244\n117.493738\n117.242796\n118.334843\n119.091227\n116.768615\n115.421416\n116.033447\n114.144567\n113.700317\n114.354433\n114.876507\n113.755332\n115.568524\n116.069102\n116.138549\n117.333173\n117.084818\n116.63492\n117.999467\n117.718767\n117.668152\n118.796536\n116.597527\n114.618757\n114.130273\n116.852609\n116.128887\n119.874946\n118.472635\n119.958398\n119.950907\n122.309881\n121.085938\n120.106701\n119.684133\n119.645704\n'
DEMO_GAS = '40.0\n39.387964\n39.576758\n40.074258\n39.817653\n39.153163\n39.120398\n39.359404\n39.908497\n39.300559\n38.654127\n39.007091\n39.244134\n40.011027\n40.502256\n40.451366\n40.314247\n41.599511\n41.45511\n41.062643\n40.493471\n40.541201\n40.613858\n40.441425\n40.410346\n40.546892\n40.893091\n41.441492\n41.5464\n40.651509\n41.002372\n40.292523\n40.206815\n39.469916\n39.470967\n39.081684\n39.188627\n40.838781\n40.814478\n41.23564\n40.573978\n40.429951\n40.761193\n40.714858\n40.899949\n40.951613\n40.448546\n40.730418\n40.324405\n41.260281\n41.00768\n41.350726\n41.351901\n41.828116\n41.527041\n42.026474\n41.964525\n42.596178\n42.908275\n42.978922\n'
BETA = 1.8286056394998358
RHO = 0.5008371987789733
MU = 42.35122736178993
SIGMA = 1.2939388309490982
S2 = 1.323438899929027
HL = 1.0024194646130267
Z = -1.0023831726745032
SPREAD_T = 41.054204851176436
FC1 = 41.701630240821
FC10 = 42.34993936941491
RIENTRO = 2
RW_RHO = 0.8686396552077983
AR_RHO = 0.6015570603503797


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


class TestRegistry455:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 761
        assert "tab455" in dvars
        assert "tab455" in withs

    def test_titoli_allineati_446_447_448_449_450_451_452_453_454_455(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab446")] == TITLE446
        assert titoli[dvars.index("tab447")] == TITLE447
        assert titoli[dvars.index("tab448")] == TITLE448
        assert titoli[dvars.index("tab449")] == TITLE449
        assert titoli[dvars.index("tab450")] == TITLE450
        assert titoli[dvars.index("tab451")] == TITLE451
        assert titoli[dvars.index("tab452")] == TITLE452
        assert titoli[dvars.index("tab453")] == TITLE453
        assert titoli[dvars.index("tab454")] == TITLE454
        assert titoli[dvars.index("tab455")] == TITLE455

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


class TestSpreadForecast455:
    def _pw(self):
        return _F["mh455_parse_serie"](DEMO_POWER)

    def _gs(self):
        return _F["mh455_parse_serie"](DEMO_GAS)

    def _spread(self):
        pw, gs = self._pw(), self._gs()
        return tuple(p - BETA * g for p, g in zip(pw, gs))

    def test_demo_valori(self):
        pw, gs = self._pw(), self._gs()
        assert len(pw) == 60 and len(gs) == 60
        assert pw[0] == 115.0 and gs[0] == 40.0
        m = _F["mh455_mappa"](pw, gs, H=10)
        assert m["n"] == 60 and m["H"] == 10 and m["T"] == 59
        assert abs(m["beta"] - BETA) < 1e-12
        assert abs(m["beta"] - 1.8286) < 1e-3  # Johansen tab447
        assert abs(m["rho"] - RHO) < 1e-12
        assert abs(m["rho"] - 0.5008) < 1e-3
        assert abs(m["mu"] - MU) < 1e-12
        assert abs(m["sigma"] - SIGMA) < 1e-12
        assert abs(m["s2"] - S2) < 1e-12
        assert abs(m["half_life"] - HL) < 1e-12
        assert abs(m["half_life"] - 1.0024) < 1e-3
        assert abs(m["spread_last"] - SPREAD_T) < 1e-9
        assert abs(m["z"] - Z) < 1e-12
        assert abs(m["z"] - (-1.0024)) < 1e-3
        assert m["rientro"] == RIENTRO == 2
        assert abs(m["forecast"][0] - FC1) < 1e-9
        assert abs(m["forecast"][-1] - FC10) < 1e-9
        assert len(m["forecast"]) == 10
        assert len(m["spread"]) == 60
        assert m["verdetto"].startswith("SPREAD BASSO")
        # bande coerenti: ampiezza crescente con h
        assert m["hi95"][0] - m["lo95"][0] > 0
        assert m["hi95"][-1] - m["lo95"][-1] > \
            m["hi95"][0] - m["lo95"][0]
        assert m["hi68"][0] - m["lo68"][0] < \
            m["hi95"][0] - m["lo95"][0]

    def test_definizione_a_mano(self):
        # AR(1) indipendente: OLS 2x2 con loop espliciti, forecast
        # ricorsivo e bande con formula indipendente
        sp = self._spread()
        n = len(sp)
        T = n - 1
        s00, s01, s11 = float(T), 0.0, 0.0
        t0, t1 = 0.0, 0.0
        for t in range(1, n):
            s01 += sp[t - 1]
            s11 += sp[t - 1] ** 2
            t0 += sp[t]
            t1 += sp[t - 1] * sp[t]
        det = s00 * s11 - s01 ** 2
        c_mano = (t0 * s11 - t1 * s01) / det
        rho_mano = (s00 * t1 - s01 * t0) / det
        m = _F["mh455_mappa"](self._pw(), self._gs(), H=10)
        assert abs(m["rho"] - rho_mano) < 1e-9
        assert abs(m["c"] - c_mano) < 1e-9
        mu_mano = c_mano / (1.0 - rho_mano)
        for h in range(1, 11):
            f_mano = mu_mano + (rho_mano ** h) * (sp[-1] - mu_mano)
            assert abs(m["forecast"][h - 1] - f_mano) < 1e-9
        hl_mano = math.log(0.5) / math.log(rho_mano)
        assert abs(m["half_life"] - hl_mano) < 1e-9
        assert abs(m["forecast"][0] - FC1) < 1e-9

    def test_chiave_coerenza_tab454(self):
        # rho == 1 + gamma dell'ADF(0) sullo stesso spread
        sp = self._spread()
        a0 = _F["mh454_adf"](sp, lags=0)
        m = _F["mh455_mappa"](self._pw(), self._gs(), H=10)
        assert abs(m["rho"] - (1.0 + a0["gamma"])) < 1e-9
        assert abs(m["half_life"] - a0["half_life"]) < 1e-9

    def test_chiave_beta_vera(self):
        # con la beta VERA (1.5) il forecast gira comunque
        pw, gs = self._pw(), self._gs()
        m = _F["mh455_mappa"](pw, gs, beta=1.5, H=10)
        assert 0.3 < m["rho"] < 0.8
        assert m["rientro"] is not None
        assert m["verdetto"].split(" — ")[0] in (
            "SPREAD MOLTO ALTO", "SPREAD ALTO", "IN EQUILIBRIO",
            "SPREAD BASSO", "SPREAD MOLTO BASSO")

    def test_controlli(self):
        # RANDOM WALK: rientro lento e onesto (rho vicino a 1)
        f_rw = _F["mh455_forecast"](_rw(7), H=10)
        assert abs(f_rw["rho"] - RW_RHO) < 1e-12
        assert 0.8 < f_rw["rho"] < 1.0
        assert f_rw["half_life"] > 4.0
        # AR(1) phi = 0.6: rho stimato bene
        f_ar = _F["mh455_forecast"](_ar1(0.6, 7), H=10)
        assert abs(f_ar["rho"] - AR_RHO) < 1e-12
        assert abs(f_ar["rho"] - 0.6) < 0.05

    def test_verdetto_soglie(self):
        v = _F["mh455_verdetto"]
        assert v(2.5, 3, 10).startswith("SPREAD MOLTO ALTO")
        assert v(2.0, None, 10).startswith("SPREAD MOLTO ALTO")
        assert v(1.99, 3, 10).startswith("SPREAD ALTO")
        assert v(1.0, 1, 10).startswith("SPREAD ALTO")
        assert v(0.99, 2, 10).startswith("IN EQUILIBRIO")
        assert v(0.0, None, 10).startswith("IN EQUILIBRIO")
        assert v(-0.99, 2, 10).startswith("IN EQUILIBRIO")
        assert v(-1.0, 2, 10).startswith("SPREAD BASSO")
        assert v(-1.99, 2, 10).startswith("SPREAD BASSO")
        assert v(-2.0, 5, 10).startswith("SPREAD MOLTO BASSO")
        assert v(-3.0, None, 10).startswith("SPREAD MOLTO BASSO")
        assert "oltre l'orizzonte" in v(2.5, None, 10)
        assert "in 1 giorno" in v(1.5, 1, 10)
        assert "in 2 giorni" in v(-1.0, 2, 10)
        for bad in (lambda: v(float("nan"), 2),
                    lambda: v(float("inf"), 2),
                    lambda: v("x", 2),
                    lambda: v(True, 2),
                    lambda: v(None, 2),
                    lambda: v(1.5, 0),
                    lambda: v(1.5, "2")):
            with pytest.raises(ValueError):
                bad()

    def test_degeneri(self):
        pw, gs = self._pw(), self._gs()
        flat = tuple([5.0] * 40)
        expl = tuple([1.1 ** i for i in range(60)])
        for bad in (lambda: _F["mh455_mappa"](tuple([1.0] * 29),
                                              tuple([1.0] * 29)),
                    lambda: _F["mh455_mappa"](None, gs),
                    lambda: _F["mh455_mappa"](pw, None),
                    lambda: _F["mh455_mappa"](pw, gs[:50]),
                    lambda: _F["mh455_mappa"](pw, gs + (1.0,)),
                    lambda: _F["mh455_mappa"](flat, gs),
                    lambda: _F["mh455_mappa"](pw, flat),
                    lambda: _F["mh455_mappa"](pw, pw),
                    lambda: _F["mh455_mappa"](pw, gs,
                                              beta=float("nan")),
                    lambda: _F["mh455_mappa"](pw, gs, beta="1.5"),
                    lambda: _F["mh455_mappa"](_rw(20261014),
                                              _rw(777)),
                    lambda: _F["mh455_mappa"](_ar1(0.5, 20261014),
                                              _ar1(0.5, 777)),
                    lambda: _F["mh455_forecast"](pw, H=0),
                    lambda: _F["mh455_forecast"](pw, H=31),
                    lambda: _F["mh455_forecast"](pw, H="10"),
                    lambda: _F["mh455_forecast"](pw, H=True),
                    lambda: _F["mh455_ar1"](flat),
                    lambda: _F["mh455_ar1"](expl),
                    lambda: _F["mh455_num"](float("nan"), "x"),
                    lambda: _F["mh455_num"](True, "x"),
                    lambda: _F["mh455_num"]("1.5", "x")):
            with pytest.raises(ValueError):
                bad()
        # H = 1: forecast a un passo, funziona lo stesso
        m1 = _F["mh455_mappa"](pw, gs, H=1)
        assert len(m1["forecast"]) == 1
        assert abs(m1["forecast"][0] - FC1) < 1e-9

    def test_parse_serie(self):
        xs = _F["mh455_parse_serie"]("1,5\n" + "2.5\n" * 29)
        assert len(xs) == 30
        assert xs[0] == 1.5 and xs[1] == 2.5
        with pytest.raises(ValueError):
            _F["mh455_parse_serie"]("1\n2\nabc\n" + "1\n" * 30)
        with pytest.raises(ValueError):
            _F["mh455_parse_serie"]("1\n2\n")
        with pytest.raises(ValueError):
            _F["mh455_parse_serie"](None)

    def test_solve(self):
        X = _F["_mh455_solve"]([[2.0, 1.0], [1.0, 3.0]],
                               [[5.0], [10.0]])
        assert abs(X[0][0] - 1.0) < 1e-12
        assert abs(X[1][0] - 3.0) < 1e-12
        with pytest.raises(ValueError):
            _F["_mh455_solve"]([[1.0, 2.0], [2.0, 4.0]],
                               [[1.0], [1.0]])

