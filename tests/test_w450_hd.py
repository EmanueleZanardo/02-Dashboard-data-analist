"""Test tab450 '📜 Scomposizione storica: cosa ha mosso davvero il prezzo power?': registry + funzioni pure."""

import math
import random
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh450_num", "mh450_parse_serie", "mh450_hd",
           "mh450_verdetto", "mh450_mappa",
           "_mh450_seq", "_mh450_solve", "_mh450_ols",
           "_mh450_chol", "_mh450_matmul",
           "mh449_num", "mh449_irf", "mh449_vecm",
           "_mh449_seq", "_mh449_solve", "_mh449_ols",
           "_mh449_chol", "_mh449_matmul",
           "mh447_num", "mh447_eig", "mh447_rango",
           "mh447_trace", "mh447_max", "mh447_critico", "_mh447_lam_T",
           "_mh447_seq", "_mh447_solve", "_mh447_mul",
           "_mh447_transp", "_mh447_ols")

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
TITLE449 = "💥 Risposta allo shock: di quanto uno shock del gas muove power?"
TITLE451 = "🌊 Spillover gas↔power: chi trasmette e chi riceve gli shock?"
TITLE453 = "📊 Backtest VECM(1): il modello batte il random walk?"
TITLE455 = "🔮 Quando rientra lo spread? Forecast mean-reversion"
TITLE457 = "📐 Quanto puntare sul rientro? Sizing Kelly del trade"
TITLE448 = "🔗 ECM: quanto in fretta power torna all'equilibrio col gas?"
TITLE447 = "⛓️ Johansen: power e gas cointegrati?"
TITLE446 = "📏 Variance ratio: il prezzo segue un random walk?"
TITLE445 = "🌀 Rolling drawdown: il peggior calo in ogni finestra"
TITLE444 = "🏞️ Lake ratio: l'area del dolore sotto il picco"
TITLE443 = "💹 Gain-to-Pain ratio: guadagni totali per ogni punto perso"
TITLE442 = "📐 Calmar geometrico: CAGR composto per unita' di peggior drawdown"
TITLE441 = "📈 Recovery Factor: profitto totale per unita' di peggior drawdown"
DEMO_POWER = '115.0\n114.222584\n115.526527\n115.270435\n115.404795\n113.275972\n114.840219\n116.685764\n115.420859\n113.571058\n112.06301\n112.194403\n116.139654\n117.765956\n116.742831\n116.62762\n115.739526\n117.414453\n114.867579\n116.640701\n115.779325\n115.137451\n116.642853\n117.253244\n117.493738\n117.242796\n118.334843\n119.091227\n116.768615\n115.421416\n116.033447\n114.144567\n113.700317\n114.354433\n114.876507\n113.755332\n115.568524\n116.069102\n116.138549\n117.333173\n117.084818\n116.63492\n117.999467\n117.718767\n117.668152\n118.796536\n116.597527\n114.618757\n114.130273\n116.852609\n116.128887\n119.874946\n118.472635\n119.958398\n119.950907\n122.309881\n121.085938\n120.106701\n119.684133\n119.645704\n'
DEMO_GAS = '40.0\n39.387964\n39.576758\n40.074258\n39.817653\n39.153163\n39.120398\n39.359404\n39.908497\n39.300559\n38.654127\n39.007091\n39.244134\n40.011027\n40.502256\n40.451366\n40.314247\n41.599511\n41.45511\n41.062643\n40.493471\n40.541201\n40.613858\n40.441425\n40.410346\n40.546892\n40.893091\n41.441492\n41.5464\n40.651509\n41.002372\n40.292523\n40.206815\n39.469916\n39.470967\n39.081684\n39.188627\n40.838781\n40.814478\n41.23564\n40.573978\n40.429951\n40.761193\n40.714858\n40.899949\n40.951613\n40.448546\n40.730418\n40.324405\n41.260281\n41.00768\n41.350726\n41.351901\n41.828116\n41.527041\n42.026474\n41.964525\n42.596178\n42.908275\n42.978922\n'
BETA = 1.8286056394998358
ALPHA_P = -0.2604753448087028
SE_P = 0.14374605784786604
T_P = -1.812052091782423
ALPHA_G = 0.13052976063089952
SE_G = 0.04699080215057056
T_G = 2.7777725566941536
SIG_G = 0.4669199559937824
SIG_P = 1.1503854605768775
CORR = 0.5927159558596256
G_T = -0.002700825775886928
O_T = -0.6741172080406349
DRIFT = 5.322522033816526
SHARE_GAS = 0.3318879429361659
SHARE_OWN = 0.6670634958220797
TMAX = 37
DG_MAX = 2.5373988643190186
G_05 = -1.972201663140267
O_05 = -0.43136962786836097
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


class TestRegistry450:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 820
        assert "tab450" in dvars
        assert "tab450" in withs

    def test_titoli_allineati_441_442_443_444_445_446_447_448_449_450(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab441")] == TITLE441
        assert titoli[dvars.index("tab442")] == TITLE442
        assert titoli[dvars.index("tab443")] == TITLE443
        assert titoli[dvars.index("tab444")] == TITLE444
        assert titoli[dvars.index("tab445")] == TITLE445
        assert titoli[dvars.index("tab446")] == TITLE446
        assert titoli[dvars.index("tab447")] == TITLE447
        assert titoli[dvars.index("tab448")] == TITLE448
        assert titoli[dvars.index("tab449")] == TITLE449
        assert titoli[dvars.index("tab450")] == TITLE450

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


class TestHD450:
    def _pw(self):
        return _F["mh450_parse_serie"](DEMO_POWER)

    def _gs(self):
        return _F["mh450_parse_serie"](DEMO_GAS)

    def test_demo_valori(self):
        pw, gs = self._pw(), self._gs()
        assert len(pw) == 60 and len(gs) == 60
        assert pw[0] == 115.0 and gs[0] == 40.0
        m = _F["mh450_mappa"](pw, gs)
        assert m["n"] == 60 and m["T"] == 59
        assert abs(m["beta"] - BETA) < 1e-12
        assert abs(m["beta"] - 1.8286) < 1e-3  # Johansen tab447
        assert abs(m["alpha_power"] - ALPHA_P) < 1e-12
        assert abs(m["se_power"] - SE_P) < 1e-12
        assert abs(m["t_power"] - T_P) < 1e-12
        assert abs(m["alpha_gas"] - ALPHA_G) < 1e-12
        assert abs(m["t_gas"] - T_G) < 1e-12
        assert abs(m["sigma_g"] - SIG_G) < 1e-12
        assert abs(m["sigma_p"] - SIG_P) < 1e-12
        assert abs(m["corr_resid"] - CORR) < 1e-12
        assert abs(m["g_T"] - G_T) < 1e-12
        assert abs(m["g_T"] - (-0.0027)) < 1e-3  # netto quasi nullo
        assert abs(m["o_T"] - O_T) < 1e-12
        assert abs(m["drift"] - DRIFT) < 1e-12
        assert abs(m["share_gas"] - SHARE_GAS) < 1e-12
        assert abs(m["share_gas"] - 0.3319) < 1e-3
        assert abs(m["share_own"] - SHARE_OWN) < 1e-12
        assert m["tmax"] == TMAX == 37
        assert abs(m["dg_max"] - DG_MAX) < 1e-12
        assert abs(m["dg_max"] - 2.5374) < 1e-3
        assert abs(m["g"][5] - G_05) < 1e-12
        assert abs(m["o"][5] - O_05) < 1e-12
        assert len(m["g"]) == 60 and len(m["o"]) == 60
        assert len(m["base"]) == 60
        assert len(m["dg"]) == 59 and len(m["dpower"]) == 59
        assert m["g"][0] == 0.0 and m["o"][0] == 0.0
        assert m["base"][0] == pw[0]
        assert m["verdetto"].startswith("STORIA A TRAZIONE GAS")
        assert "33.2%" in m["verdetto"]
        # in QUESTO campione il gas ha t > 2 (stesso rumore di
        # tab448/449) -> flag False
        assert T_G > 2.0
        assert m["gas_esogeno"] is False

    def test_definizione_a_mano(self):
        # ec demeaned -> OLS 2x2 per equazione -> Sigma/Cholesky/A ->
        # Phi ricorsivo -> sostituzione in avanti per u_t ->
        # convoluzione -> identita' contabile, tutto con loop espliciti
        pw, gs = self._pw(), self._gs()
        n = len(pw)
        T = n - 1
        ec_raw = [y - BETA * g for y, g in zip(pw, gs)]
        mu = sum(ec_raw) / n
        ec = [v - mu for v in ec_raw]
        assert abs(sum(ec) / n) < 1e-9
        al, co, rs = {}, {}, {}
        for nome, y in (("power", pw), ("gas", gs)):
            dy = [y[t] - y[t - 1] for t in range(1, n)]
            a, c, se_a, t_a = _ols2_mano(ec[:-1], dy)
            al[nome] = a
            co[nome] = c
            rs[nome] = [yv - (a * xv + c)
                        for xv, yv in zip(ec[:-1], dy)]
            h = _F["mh450_hd"](pw, gs)
            assert abs(h[f"alpha_{nome}"] - a) < 1e-9, nome
            assert abs(h[f"se_{nome}"] - se_a) < 1e-9, nome
            assert abs(h[f"t_{nome}"] - t_a) < 1e-9, nome
        assert abs(al["power"] - ALPHA_P) < 1e-9
        assert abs(al["gas"] - ALPHA_G) < 1e-9
        rx, ry = rs["gas"], rs["power"]
        dof = T - 2
        s00 = sum(v * v for v in rx) / dof
        s11 = sum(v * v for v in ry) / dof
        s01 = sum(a * b for a, b in zip(rx, ry)) / dof
        l00 = math.sqrt(s00)
        l10 = s01 / l00
        l11 = math.sqrt(s11 - l10 * l10)
        assert abs(l00 - SIG_G) < 1e-9
        assert abs(l11 - SIG_P) < 1e-9
        # shock strutturali: sostituzione in avanti esplicita
        ug = [v / l00 for v in rx]
        up = [(v - l10 * w) / l11 for v, w in zip(ry, ug)]
        for t in range(T):
            assert abs(l00 * ug[t] - rx[t]) < 1e-9, t
            assert abs(l10 * ug[t] + l11 * up[t] - ry[t]) < 1e-9, t
        A = [[1.0 - al["gas"] * BETA, al["gas"]],
             [-al["power"] * BETA, 1.0 + al["power"]]]
        Phi = [[1.0, 0.0], [0.0, 1.0]]
        pl10, pl11 = [], []
        for _ in range(T):
            pl10.append(Phi[1][0] * l00 + Phi[1][1] * l10)
            pl11.append(Phi[1][1] * l11)
            Phi = [[A[0][0] * Phi[0][0] + A[0][1] * Phi[1][0],
                    A[0][0] * Phi[0][1] + A[0][1] * Phi[1][1]],
                   [A[1][0] * Phi[0][0] + A[1][1] * Phi[1][0],
                    A[1][0] * Phi[0][1] + A[1][1] * Phi[1][1]]]
        g = [0.0] * n
        o = [0.0] * n
        for t in range(1, n):
            g[t] = sum(pl10[j] * ug[t - 1 - j] for j in range(t))
            o[t] = sum(pl11[j] * up[t - 1 - j] for j in range(t))
        h = _F["mh450_hd"](pw, gs)
        for t in range(n):
            assert abs(h["g"][t] - g[t]) < 1e-9, t
            assert abs(h["o"][t] - o[t]) < 1e-9, t
            assert abs(h["base"][t] - (pw[t] - g[t] - o[t])) < 1e-9, t
        assert abs(h["g"][5] - G_05) < 1e-9
        assert abs(h["o"][5] - O_05) < 1e-9
        # identita' contabile: livelli e differenze
        for t in range(n):
            assert abs(g[t] + o[t] + h["base"][t] - pw[t]) < 1e-9, t
        dpw = [pw[t + 1] - pw[t] for t in range(T)]
        for t in range(T):
            assert abs(h["dg"][t] + h["do"][t] + h["db"][t]
                       - dpw[t]) < 1e-9, t
        # quote di varianza
        def _var(xs):
            mu = sum(xs) / len(xs)
            return sum((v - mu) ** 2 for v in xs) / len(xs)
        dg = [g[t + 1] - g[t] for t in range(T)]
        do = [o[t + 1] - o[t] for t in range(T)]
        assert abs(_var(dg) / _var(dpw) - SHARE_GAS) < 1e-9
        assert abs(_var(do) / _var(dpw) - SHARE_OWN) < 1e-9

    def test_chiave_identita_contabile(self):
        # la base chiude il conto ESATTAMENTE: sul netto
        # g_T + o_T + drift = power_T - power_0
        pw, gs = self._pw(), self._gs()
        m = _F["mh450_mappa"](pw, gs)
        assert abs(m["g_T"] + m["o_T"] + m["drift"]
                   - (pw[-1] - pw[0])) < 1e-9
        assert abs(m["g_T"] - G_T) < 1e-12
        assert abs(m["o_T"] - O_T) < 1e-12
        assert abs(m["drift"] - DRIFT) < 1e-12

    def test_chiave_coerenza_irf(self):
        # la HD e' la convoluzione dell'IRF di tab449 con gli shock
        # realizzati: avanti e indietro sono lo stesso modello.
        # Ricostruisco gli shock gas per deconvoluzione triangolare
        # (irf[0] = l10 != 0: lo shock gas tocca la power subito) e
        # verifico che la convoluzione con l'IRF di tab449 torni g.
        pw, gs = self._pw(), self._gs()
        n = len(pw)
        T = n - 1
        m = _F["mh450_mappa"](pw, gs)
        r = _F["mh449_irf"](pw, gs, H=T)
        assert len(r["irf"]) == T + 1
        irf = r["irf"]
        assert abs(irf[0]) > 1e-12
        ug = [0.0] * T
        for t in range(1, n):
            s = m["g"][t]
            for j in range(1, t):
                s -= irf[j] * ug[t - 1 - j]
            ug[t - 1] = s / irf[0]
        for t in range(1, n):
            conv = sum(irf[j] * ug[t - 1 - j] for j in range(t))
            assert abs(conv - m["g"][t]) < 1e-9, t

    def test_chiave_beta_vera(self):
        # con la beta VERA (1.5) l'identita' resta esatta e il
        # modello ritrova il DGP (cross-check tab448 chiave 1)
        pw, gs = self._pw(), self._gs()
        m = _F["mh450_mappa"](pw, gs, beta=1.5)
        assert abs(m["beta"] - 1.5) < 1e-12
        assert abs(m["alpha_power"] - A15Y) < 1e-12
        assert abs(A15Y - (-0.3035)) < 1e-3
        assert abs(m["g_T"] + m["o_T"] + m["drift"]
                   - (pw[-1] - pw[0])) < 1e-9
        for t in range(m["n"]):
            assert abs(m["g"][t] + m["o"][t] + m["base"][t]
                       - pw[t]) < 1e-9, t

    def test_controlli(self):
        # RANDOM WALK INDIPENDENTI (Johansen rango 0): niente HD
        with pytest.raises(ValueError, match="cointegrazione"):
            _F["mh450_mappa"](_rw(20261014), _rw(777))
        # AR(1) STAZIONARIE (Johansen rango 2): niente VECM
        with pytest.raises(ValueError, match="stazionarie"):
            _F["mh450_mappa"](_ar1(0.5, 20261014), _ar1(0.5, 777))

    def test_verdetto_soglie(self):
        v = _F["mh450_verdetto"]
        assert v(0.75).startswith("IL GAS HA DETTATO LA STORIA")
        assert v(0.50).startswith("IL GAS HA DETTATO LA STORIA")
        assert v(1.5).startswith("IL GAS HA DETTATO LA STORIA")
        assert v(0.3319).startswith("STORIA A TRAZIONE GAS")
        assert v(0.4999).startswith("STORIA A TRAZIONE GAS")
        assert v(0.25).startswith("STORIA A TRAZIONE GAS")
        assert v(0.2499).startswith("GAS PARZIALE")
        assert v(0.10).startswith("GAS PARZIALE")
        assert v(0.0999).startswith("STORIA QUASI DOMESTICA")
        assert v(0.02).startswith("STORIA QUASI DOMESTICA")
        assert v(0.0199).startswith("STORIA DOMESTICA")
        assert v(0.0).startswith("STORIA DOMESTICA")
        for bad in (lambda: v(float("nan")),
                    lambda: v(float("inf")),
                    lambda: v(-0.1),
                    lambda: v("x"),
                    lambda: v(True),
                    lambda: v(None)):
            with pytest.raises(ValueError):
                bad()

    def test_degeneri(self):
        pw, gs = self._pw(), self._gs()
        flat = tuple([5.0] * 40)
        trend = tuple(100.0 + 0.3 * t for t in range(60))
        for bad in (lambda: _F["mh450_mappa"](tuple([1.0] * 29),
                                              tuple([1.0] * 29)),
                    lambda: _F["mh450_mappa"](None, gs),
                    lambda: _F["mh450_mappa"](pw, None),
                    lambda: _F["mh450_mappa"](pw, gs[:50]),
                    lambda: _F["mh450_mappa"](pw, gs + (1.0,)),
                    lambda: _F["mh450_mappa"](flat, gs),
                    lambda: _F["mh450_mappa"](pw, flat),
                    lambda: _F["mh450_mappa"](pw, pw),
                    lambda: _F["mh450_mappa"](trend, gs),
                    lambda: _F["mh450_hd"](pw, gs,
                                           beta=float("nan")),
                    lambda: _F["mh450_hd"](pw, gs,
                                           beta=float("inf")),
                    lambda: _F["mh450_hd"](pw, gs, beta="1.5"),
                    lambda: _F["mh450_hd"](pw, gs, beta=True),
                    lambda: _F["mh450_num"](float("nan"), "x"),
                    lambda: _F["mh450_num"](True, "x"),
                    lambda: _F["mh450_num"]("1.5", "x")):
            with pytest.raises(ValueError):
                bad()

    def test_parse_serie(self):
        xs = _F["mh450_parse_serie"]("1,5\n" + "2.5\n" * 29)
        assert len(xs) == 30
        assert xs[0] == 1.5 and xs[1] == 2.5
        with pytest.raises(ValueError):
            _F["mh450_parse_serie"]("1\n2\nabc\n" + "1\n" * 30)
        with pytest.raises(ValueError):
            _F["mh450_parse_serie"]("1\n2\n")
        with pytest.raises(ValueError):
            _F["mh450_parse_serie"](None)

    def test_solve(self):
        X = _F["_mh450_solve"]([[2.0, 1.0], [1.0, 3.0]],
                               [[5.0], [10.0]])
        assert abs(X[0][0] - 1.0) < 1e-12
        assert abs(X[1][0] - 3.0) < 1e-12
        with pytest.raises(ValueError):
            _F["_mh450_solve"]([[1.0, 2.0], [2.0, 4.0]],
                               [[1.0], [1.0]])

