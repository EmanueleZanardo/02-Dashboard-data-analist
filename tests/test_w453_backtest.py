"""Test tab453 '📊 Backtest VECM(1): il modello batte il random walk?': registry + funzioni pure."""

import math
import random
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh453_num", "mh453_parse_serie", "mh453_backtest",
           "mh453_metrics", "mh453_dm", "mh453_verdetto", "mh453_mappa",
           "_mh453_seq", "_mh453_solve", "_mh453_ols", "_mh453_phi",
           "_mh453_ecm_fit",
           "mh452_num", "mh452_forecast",
           "_mh452_seq", "_mh452_solve", "_mh452_ols",
           "mh449_num", "mh449_vecm",
           "_mh449_seq", "_mh449_solve", "_mh449_ols",
           "_mh449_chol", "_mh449_matmul",
           "mh447_num", "mh447_eig", "mh447_rango",
           "mh447_trace", "mh447_max", "mh447_critico", "_mh447_lam_T",
           "_mh447_seq", "_mh447_solve", "_mh447_mul",
           "_mh447_transp", "_mh447_ols")

TITLE453 = "📊 Backtest VECM(1): il modello batte il random walk?"
TITLE455 = "🔮 Quando rientra lo spread? Forecast mean-reversion"
TITLE457 = "📐 Quanto puntare sul rientro? Sizing Kelly del trade"
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
TITLE451 = "🌊 Spillover gas↔power: chi trasmette e chi riceve gli shock?"
TITLE450 = "📜 Scomposizione storica: cosa ha mosso davvero il prezzo power?"
TITLE449 = "💥 Risposta allo shock: di quanto uno shock del gas muove power?"
TITLE448 = "🔗 ECM: quanto in fretta power torna all'equilibrio col gas?"
TITLE447 = "⛓️ Johansen: power e gas cointegrati?"
TITLE446 = "📏 Variance ratio: il prezzo segue un random walk?"
TITLE445 = "🌀 Rolling drawdown: il peggior calo in ogni finestra"
TITLE444 = "🏞️ Lake ratio: l'area del dolore sotto il picco"
DEMO_POWER = '115.0\n114.222584\n115.526527\n115.270435\n115.404795\n113.275972\n114.840219\n116.685764\n115.420859\n113.571058\n112.06301\n112.194403\n116.139654\n117.765956\n116.742831\n116.62762\n115.739526\n117.414453\n114.867579\n116.640701\n115.779325\n115.137451\n116.642853\n117.253244\n117.493738\n117.242796\n118.334843\n119.091227\n116.768615\n115.421416\n116.033447\n114.144567\n113.700317\n114.354433\n114.876507\n113.755332\n115.568524\n116.069102\n116.138549\n117.333173\n117.084818\n116.63492\n117.999467\n117.718767\n117.668152\n118.796536\n116.597527\n114.618757\n114.130273\n116.852609\n116.128887\n119.874946\n118.472635\n119.958398\n119.950907\n122.309881\n121.085938\n120.106701\n119.684133\n119.645704\n'
DEMO_GAS = '40.0\n39.387964\n39.576758\n40.074258\n39.817653\n39.153163\n39.120398\n39.359404\n39.908497\n39.300559\n38.654127\n39.007091\n39.244134\n40.011027\n40.502256\n40.451366\n40.314247\n41.599511\n41.45511\n41.062643\n40.493471\n40.541201\n40.613858\n40.441425\n40.410346\n40.546892\n40.893091\n41.441492\n41.5464\n40.651509\n41.002372\n40.292523\n40.206815\n39.469916\n39.470967\n39.081684\n39.188627\n40.838781\n40.814478\n41.23564\n40.573978\n40.429951\n40.761193\n40.714858\n40.899949\n40.951613\n40.448546\n40.730418\n40.324405\n41.260281\n41.00768\n41.350726\n41.351901\n41.828116\n41.527041\n42.026474\n41.964525\n42.596178\n42.908275\n42.978922\n'
BETA = 1.8286056394998358
W_DEMO = 40
K_DEMO = 20
RMSE_V = 1.4874363922791352
RMSE_R = 1.5299359280529845
RMSE_A = 1.5567437678362446
MAE_V = 1.1724783760516295
MAE_R = 1.1649797499999999
MAE_A = 1.1463693283819238
DM_RW = 0.6290437112930833
P_RW = 0.5293204397872708
MEAN_D_RW = 0.12823692287097768
DM_AR = 0.6643493968762331
P_AR = 0.5064667123503976
ACT_0 = 117.084818
VECM_0 = 117.4392117393406
RW_0 = 117.333173
AR1_0 = 116.71485528708737
ACT_L = 119.645704
VECM_L = 120.03557027982669
A15Y = -0.30346693792017626


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


def _ols2_mano(xs, ys):
    """OLS y = a*x + c con loop espliciti (indipendente dagli
    helper): ritorna (a, c, se_a, t_a)."""
    n = len(xs)
    s_x = sum(xs)
    s_xx = sum(x * x for x in xs)
    s_xy = sum(x * y for x, y in zip(xs, ys))
    s_y = sum(ys)
    det = s_xx * n - s_x * s_x
    assert abs(det) > 1e-12
    a = (s_xy * n - s_x * s_y) / det
    c = (s_xx * s_y - s_x * s_xy) / det
    resid = [y - (a * x + c) for x, y in zip(xs, ys)]
    s2 = sum(r * r for r in resid) / (n - 2)
    se_a = math.sqrt(s2 * n / det)
    return a, c, se_a, a / se_a


class TestRegistry453:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 727
        assert "tab453" in dvars
        assert "tab453" in withs

    def test_titoli_allineati_444_445_446_447_448_449_450_451_452_453(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab444")] == TITLE444
        assert titoli[dvars.index("tab445")] == TITLE445
        assert titoli[dvars.index("tab446")] == TITLE446
        assert titoli[dvars.index("tab447")] == TITLE447
        assert titoli[dvars.index("tab448")] == TITLE448
        assert titoli[dvars.index("tab449")] == TITLE449
        assert titoli[dvars.index("tab450")] == TITLE450
        assert titoli[dvars.index("tab451")] == TITLE451
        assert titoli[dvars.index("tab452")] == TITLE452
        assert titoli[dvars.index("tab453")] == TITLE453

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


class TestBacktest453:
    def _pw(self):
        return _F["mh453_parse_serie"](DEMO_POWER)

    def _gs(self):
        return _F["mh453_parse_serie"](DEMO_GAS)

    def test_demo_valori(self):
        pw, gs = self._pw(), self._gs()
        assert len(pw) == 60 and len(gs) == 60
        assert pw[0] == 115.0 and gs[0] == 40.0
        m = _F["mh453_mappa"](pw, gs, W=40)
        assert m["n"] == 60 and m["W"] == W_DEMO and m["K"] == K_DEMO
        assert abs(m["beta"] - BETA) < 1e-12
        assert abs(m["beta"] - 1.8286) < 1e-3  # Johansen tab447
        assert len(m["actual"]) == 20 and len(m["fc_vecm"]) == 20
        assert len(m["fc_rw"]) == 20 and len(m["fc_ar1"]) == 20
        assert abs(m["actual"][0] - ACT_0) < 1e-9
        assert abs(m["fc_vecm"][0] - VECM_0) < 1e-9
        assert abs(m["fc_rw"][0] - RW_0) < 1e-9
        assert abs(m["fc_rw"][0] - pw[39]) < 1e-12  # RW = ultimo oss.
        assert abs(m["fc_ar1"][0] - AR1_0) < 1e-9
        assert abs(m["actual"][-1] - ACT_L) < 1e-9
        assert abs(m["fc_vecm"][-1] - VECM_L) < 1e-9
        assert abs(m["rmse_vecm"] - RMSE_V) < 1e-12
        assert abs(m["rmse_rw"] - RMSE_R) < 1e-12
        assert abs(m["rmse_ar1"] - RMSE_A) < 1e-12
        assert m["rmse_vecm"] < m["rmse_rw"] < m["rmse_ar1"]
        assert abs(m["mae_vecm"] - MAE_V) < 1e-12
        assert abs(m["mae_rw"] - MAE_R) < 1e-12
        assert abs(m["mae_ar1"] - MAE_A) < 1e-12
        dm_rw, dm_ar = m["dm_rw"], m["dm_ar1"]
        assert abs(dm_rw["dm"] - DM_RW) < 1e-12
        assert abs(dm_rw["p"] - P_RW) < 1e-12
        assert abs(dm_rw["mean_d"] - MEAN_D_RW) < 1e-12
        assert dm_rw["dm"] > 0.0  # sulla demo il VECM e' di poco meglio
        assert dm_rw["p"] > 0.05  # ...ma non significativamente
        assert abs(dm_ar["dm"] - DM_AR) < 1e-12
        assert abs(dm_ar["p"] - P_AR) < 1e-12
        assert m["verdetto_rw"].startswith("PARI")
        assert m["verdetto_ar1"].startswith("PARI")

    def test_definizione_a_mano(self):
        # rolling loop indipendente: OLS 2x2 per equazione su ogni
        # finestra (loop espliciti), costante corretta -alpha*mu,
        # forecast, metriche e DM con formule indipendenti
        pw, gs = self._pw(), self._gs()
        n = len(pw)
        W = 40
        e_actual, e_v, e_r, e_a = [], [], [], []
        A_last_mano = None
        for i in range(W, n):
            yw = pw[i - W:i]
            gw = gs[i - W:i]
            er = [y - BETA * g for y, g in zip(yw, gw)]
            mu = sum(er) / W
            ec = [v - mu for v in er]
            al, cs = {}, {}
            for nome, y in (("power", yw), ("gas", gw)):
                dy = [y[t] - y[t - 1] for t in range(1, W)]
                a, c, _, _ = _ols2_mano(ec[:-1], dy)
                al[nome] = a
                cs[nome] = c
            A = [[1.0 - al["gas"] * BETA, al["gas"]],
                 [-al["power"] * BETA, 1.0 + al["power"]]]
            c = [cs["gas"] - al["gas"] * mu,
                 cs["power"] - al["power"] * mu]
            A_last_mano = A
            e_actual.append(pw[i])
            e_v.append(A[1][0] * gs[i - 1] + A[1][1] * pw[i - 1] + c[1])
            e_r.append(pw[i - 1])
            a_ar, c_ar, _, _ = _ols2_mano(yw[:-1], yw[1:])
            e_a.append(a_ar * pw[i - 1] + c_ar)
        m = _F["mh453_mappa"](pw, gs, W=W)
        K = n - W
        for j in range(K):
            assert abs(m["actual"][j] - e_actual[j]) < 1e-9, j
            assert abs(m["fc_vecm"][j] - e_v[j]) < 1e-9, j
            assert abs(m["fc_rw"][j] - e_r[j]) < 1e-9, j
            assert abs(m["fc_ar1"][j] - e_a[j]) < 1e-9, j
        assert abs(e_actual[0] - ACT_0) < 1e-9
        assert abs(e_v[0] - VECM_0) < 1e-9
        # metriche indipendenti
        rv = math.sqrt(sum((a - f) ** 2
                           for a, f in zip(e_actual, e_v)) / K)
        assert abs(m["rmse_vecm"] - rv) < 1e-9
        assert abs(rv - RMSE_V) < 1e-9
        # DM indipendente: d = e_b^2 - e_v^2, t-stat, normale
        evv = [a - f for a, f in zip(e_actual, e_v)]
        erb = [a - f for a, f in zip(e_actual, e_r)]
        d = [b * b - v * v for v, b in zip(evv, erb)]
        md = sum(d) / K
        vd = sum((x - md) ** 2 for x in d) / (K - 1)
        dm_mano = md / math.sqrt(vd / K)
        p_mano = 2.0 * (1.0 - 0.5 * (1.0 + math.erf(abs(dm_mano)
                                                   / math.sqrt(2.0))))
        assert abs(m["dm_rw"]["dm"] - dm_mano) < 1e-9
        assert abs(m["dm_rw"]["p"] - p_mano) < 1e-9
        assert abs(dm_mano - DM_RW) < 1e-9
        # A_last coincide col fit manuale dell'ultima finestra
        for ii in (0, 1):
            for jj in (0, 1):
                assert abs(m["A_last"][ii][jj]
                           - A_last_mano[ii][jj]) < 1e-9, (ii, jj)

    def test_chiave_coerenza_tab449(self):
        # il fit dell'ultima finestra [n-W, n-1) coincide con
        # mh449_vecm sulla stessa finestra e stessa beta (stessa stima)
        pw, gs = self._pw(), self._gs()
        m = _F["mh453_mappa"](pw, gs, W=40)
        v = _F["mh449_vecm"](pw[19:59], gs[19:59], beta=m["beta"])
        for i in (0, 1):
            for j in (0, 1):
                assert abs(m["A_last"][i][j] - v["A"][i][j]) < 1e-9, (i, j)

    def test_chiave_beta_vera(self):
        # con la beta VERA (1.5) il modello ritrova il DGP
        # (cross-check tab448 chiave 1)
        pw, gs = self._pw(), self._gs()
        A, c, a_p, a_g = _F["_mh453_ecm_fit"](pw, gs, 1.5)
        assert abs(a_p - A15Y) < 1e-12
        assert abs(A15Y - (-0.3035)) < 1e-3

    def test_controlli(self):
        # RANDOM WALK INDIPENDENTI (Johansen rango 0): niente VECM
        with pytest.raises(ValueError, match="cointegrazione"):
            _F["mh453_mappa"](_rw(20261014), _rw(777))
        # AR(1) STAZIONARIE (Johansen rango 2): niente VECM
        with pytest.raises(ValueError, match="stazionarie"):
            _F["mh453_mappa"](_ar1(0.5, 20261014), _ar1(0.5, 777))

    def test_verdetto_soglie(self):
        v = _F["mh453_verdetto"]
        assert v(2.5, 0.005).startswith("BATTE NETTAMENTE")
        assert v(2.5, 0.01).startswith("BATTE")
        assert v(2.5, 0.049).startswith("BATTE")
        assert v(2.5, 0.05).startswith("PARI")
        assert v(0.629, 0.529).startswith("PARI")
        assert v(-0.5, 0.7).startswith("PARI")
        assert v(-2.5, 0.049).startswith("PEGGIORE")
        assert v(-2.5, 0.005).startswith("PEGGIORE NETTAMENTE")
        assert v(0.0, 1.0).startswith("PARI")
        for bad in (lambda: v(float("nan"), 0.5),
                    lambda: v(1.0, float("inf")),
                    lambda: v("x", 0.5),
                    lambda: v(True, 0.5),
                    lambda: v(1.0, None)):
            with pytest.raises(ValueError):
                bad()

    def test_dm(self):
        # DM indipendente su errori noti: benchmark sempre peggiore
        ev = [0.1, -0.2, 0.15, -0.1, 0.05]
        eb = [1.0, -1.2, 0.9, -1.1, 1.05]
        r = _F["mh453_dm"](ev, eb)
        d = [b * b - v * v for v, b in zip(ev, eb)]
        md = sum(d) / 5
        vd = sum((x - md) ** 2 for x in d) / 4
        assert abs(r["mean_d"] - md) < 1e-12
        assert abs(r["dm"] - md / math.sqrt(vd / 5)) < 1e-12
        assert r["dm"] > 0 and r["p"] < 0.05
        # varianza nulla -> indistinguibili
        r0 = _F["mh453_dm"]([0.5, 0.5], [0.5, 0.5])
        assert r0["dm"] == 0.0 and r0["p"] == 1.0
        for bad in (lambda: _F["mh453_dm"]([0.1], [0.2]),
                    lambda: _F["mh453_dm"](None, [0.2, 0.3]),
                    lambda: _F["mh453_dm"]([0.1, 0.2], [0.1])):
            with pytest.raises(ValueError):
                bad()

    def test_metrics(self):
        r = _F["mh453_metrics"]([1.0, 2.0, 3.0], [1.5, 1.5, 3.5])
        assert r["n"] == 3
        assert abs(r["rmse"] - 0.5) < 1e-12
        assert abs(r["mae"] - 0.5) < 1e-12
        for bad in (lambda: _F["mh453_metrics"](None, [1.0]),
                    lambda: _F["mh453_metrics"]([1.0], [1.0, 2.0]),
                    lambda: _F["mh453_metrics"]([], [])):
            with pytest.raises(ValueError):
                bad()

    def test_degeneri(self):
        pw, gs = self._pw(), self._gs()
        flat = tuple([5.0] * 40)
        _trend = tuple(100.0 + 0.3 * t for t in range(60))
        for bad in (lambda: _F["mh453_mappa"](tuple([1.0] * 29),
                                              tuple([1.0] * 29)),
                    lambda: _F["mh453_mappa"](None, gs),
                    lambda: _F["mh453_mappa"](pw, None),
                    lambda: _F["mh453_mappa"](pw, gs[:50]),
                    lambda: _F["mh453_mappa"](pw, gs + (1.0,)),
                    lambda: _F["mh453_mappa"](flat, gs),
                    lambda: _F["mh453_mappa"](pw, flat),
                    lambda: _F["mh453_mappa"](pw, pw),
                    lambda: _F["mh453_mappa"](_trend, gs),
                    lambda: _F["mh453_backtest"](pw, gs,
                                                 beta=float("nan")),
                    lambda: _F["mh453_backtest"](pw, gs, beta="1.5"),
                    lambda: _F["mh453_backtest"](pw, gs, W=29),
                    lambda: _F["mh453_backtest"](pw, gs, W=60),
                    lambda: _F["mh453_backtest"](pw, gs, W=59.0),
                    lambda: _F["mh453_backtest"](pw, gs, W=True),
                    lambda: _F["mh453_num"](float("nan"), "x"),
                    lambda: _F["mh453_num"](True, "x"),
                    lambda: _F["mh453_num"]("1.5", "x")):
            with pytest.raises(ValueError):
                bad()
        # K = 1 (W = n-1): metriche ok, DM non calcolabile
        m1 = _F["mh453_mappa"](pw, gs, W=59)
        assert m1["K"] == 1
        assert m1["dm_rw"] is None and m1["verdetto_rw"] is None

    def test_parse_serie(self):
        xs = _F["mh453_parse_serie"]("1,5\n" + "2.5\n" * 29)
        assert len(xs) == 30
        assert xs[0] == 1.5 and xs[1] == 2.5
        with pytest.raises(ValueError):
            _F["mh453_parse_serie"]("1\n2\nabc\n" + "1\n" * 30)
        with pytest.raises(ValueError):
            _F["mh453_parse_serie"]("1\n2\n")
        with pytest.raises(ValueError):
            _F["mh453_parse_serie"](None)

    def test_solve(self):
        X = _F["_mh453_solve"]([[2.0, 1.0], [1.0, 3.0]],
                               [[5.0], [10.0]])
        assert abs(X[0][0] - 1.0) < 1e-12
        assert abs(X[1][0] - 3.0) < 1e-12
        with pytest.raises(ValueError):
            _F["_mh453_solve"]([[1.0, 2.0], [2.0, 4.0]],
                               [[1.0], [1.0]])

    def test_phi(self):
        assert abs(_F["_mh453_phi"](0.0) - 0.5) < 1e-12
        assert abs(_F["_mh453_phi"](1.96) - 0.9750021048517795) < 1e-9

