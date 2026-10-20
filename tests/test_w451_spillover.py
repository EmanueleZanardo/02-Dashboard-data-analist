"""Test tab451 '🌊 Spillover gas↔power: chi trasmette e chi riceve gli shock?': registry + funzioni pure."""

import math
import random
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh451_num", "mh451_parse_serie", "mh451_spillover",
           "mh451_verdetto", "mh451_mappa",
           "_mh451_seq", "_mh451_solve", "_mh451_ols",
           "_mh451_chol", "_mh451_matmul",
           "mh449_num", "mh449_irf", "mh449_vecm",
           "_mh449_seq", "_mh449_solve", "_mh449_ols",
           "_mh449_chol", "_mh449_matmul",
           "mh447_num", "mh447_eig", "mh447_rango",
           "mh447_trace", "mh447_max", "mh447_critico", "_mh447_lam_T",
           "_mh447_seq", "_mh447_solve", "_mh447_mul",
           "_mh447_transp", "_mh447_ols")

TITLE451 = "🌊 Spillover gas↔power: chi trasmette e chi riceve gli shock?"
TITLE453 = "📊 Backtest VECM(1): il modello batte il random walk?"
TITLE455 = "🔮 Quando rientra lo spread? Forecast mean-reversion"
TITLE457 = "📐 Quanto puntare sul rientro? Sizing Kelly del trade"
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
TITLE448 = "🔗 ECM: quanto in fretta power torna all'equilibrio col gas?"
TITLE447 = "⛓️ Johansen: power e gas cointegrati?"
TITLE446 = "📏 Variance ratio: il prezzo segue un random walk?"
TITLE445 = "🌀 Rolling drawdown: il peggior calo in ogni finestra"
TITLE444 = "🏞️ Lake ratio: l'area del dolore sotto il picco"
TITLE443 = "💹 Gain-to-Pain ratio: guadagni totali per ogni punto perso"
TITLE442 = "📐 Calmar geometrico: CAGR composto per unita' di peggior drawdown"
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
G2P_01 = 0.35131220433058946
P2G_01 = 0.0
TOT_01 = 0.17565610216529473
G2P_05 = 0.5238602219498085
P2G_05 = 0.16988789475065344
TOT_05 = 0.346874058350231
G2P_20 = 0.6477976606255661
P2G_20 = 0.2659281133243112
TOT_20 = 0.45686288697493865
NET_20 = 0.3818695473012549
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


class TestRegistry451:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 602
        assert "tab451" in dvars
        assert "tab451" in withs

    def test_titoli_allineati_442_443_444_445_446_447_448_449_450_451(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab442")] == TITLE442
        assert titoli[dvars.index("tab443")] == TITLE443
        assert titoli[dvars.index("tab444")] == TITLE444
        assert titoli[dvars.index("tab445")] == TITLE445
        assert titoli[dvars.index("tab446")] == TITLE446
        assert titoli[dvars.index("tab447")] == TITLE447
        assert titoli[dvars.index("tab448")] == TITLE448
        assert titoli[dvars.index("tab449")] == TITLE449
        assert titoli[dvars.index("tab450")] == TITLE450
        assert titoli[dvars.index("tab451")] == TITLE451

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


class TestSpillover451:
    def _pw(self):
        return _F["mh451_parse_serie"](DEMO_POWER)

    def _gs(self):
        return _F["mh451_parse_serie"](DEMO_GAS)

    def test_demo_valori(self):
        pw, gs = self._pw(), self._gs()
        assert len(pw) == 60 and len(gs) == 60
        assert pw[0] == 115.0 and gs[0] == 40.0
        m = _F["mh451_mappa"](pw, gs)
        assert m["n"] == 60 and m["T"] == 59 and m["H"] == 20
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
        assert len(m["S_pg"]) == 20 and len(m["S_gp"]) == 20
        assert len(m["S_pp"]) == 20 and len(m["S_gg"]) == 20
        assert len(m["tot"]) == 20 and len(m["net"]) == 20
        assert abs(m["S_pg"][0] - G2P_01) < 1e-12
        assert m["S_gp"][0] == P2G_01 == 0.0
        assert abs(m["tot"][0] - TOT_01) < 1e-12
        assert abs(m["S_pg"][4] - G2P_05) < 1e-12
        assert abs(m["S_gp"][4] - P2G_05) < 1e-12
        assert abs(m["tot"][4] - TOT_05) < 1e-12
        assert abs(m["S_pg"][19] - G2P_20) < 1e-12
        assert abs(m["S_pg"][19] - 0.6478) < 1e-3
        assert abs(m["S_gp"][19] - P2G_20) < 1e-12
        assert abs(m["S_gp"][19] - 0.2659) < 1e-3
        assert abs(m["tot"][19] - TOT_20) < 1e-12
        assert abs(m["net"][19] - NET_20) < 1e-12
        assert abs(m["g2p"] - G2P_20) < 1e-12
        assert abs(m["p2g"] - P2G_20) < 1e-12
        assert abs(m["spill"] - TOT_20) < 1e-12
        assert abs(m["spill_net"] - NET_20) < 1e-12
        assert m["verdetto"].startswith("FORTEMENTE CONNESSI")
        assert "45.7%" in m["verdetto"]
        # in QUESTO campione il gas ha t > 2 (stesso rumore di
        # tab448/449/450) -> flag False
        assert T_G > 2.0
        assert m["gas_esogeno"] is False

    def test_definizione_a_mano(self):
        # ec demeaned -> OLS 2x2 per equazione -> Sigma/Cholesky/A ->
        # Phi ricorsivo -> somme cumulative dei quadrati per riga,
        # tutto con loop espliciti
        pw, gs = self._pw(), self._gs()
        n = len(pw)
        T = n - 1
        H = 20
        ec_raw = [y - BETA * g for y, g in zip(pw, gs)]
        mu = sum(ec_raw) / n
        ec = [v - mu for v in ec_raw]
        assert abs(sum(ec) / n) < 1e-9
        al, rs = {}, {}
        for nome, y in (("power", pw), ("gas", gs)):
            dy = [y[t] - y[t - 1] for t in range(1, n)]
            a, c, se_a, t_a = _ols2_mano(ec[:-1], dy)
            al[nome] = a
            rs[nome] = [yv - (a * xv + c)
                        for xv, yv in zip(ec[:-1], dy)]
            h = _F["mh451_spillover"](pw, gs, H=H)
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
        A = [[1.0 - al["gas"] * BETA, al["gas"]],
             [-al["power"] * BETA, 1.0 + al["power"]]]
        Phi = [[1.0, 0.0], [0.0, 1.0]]
        c_pg = c_pp = c_gp = c_gg = 0.0
        e_pg, e_gp, e_tot, e_net = [], [], [], []
        for _ in range(H):
            r_pg = Phi[1][0] * l00 + Phi[1][1] * l10
            r_pp = Phi[1][1] * l11
            r_gg = Phi[0][0] * l00 + Phi[0][1] * l10
            r_gp = Phi[0][1] * l11
            c_pg += r_pg * r_pg
            c_pp += r_pp * r_pp
            c_gg += r_gg * r_gg
            c_gp += r_gp * r_gp
            v_pg = c_pg / (c_pg + c_pp)
            v_gp = c_gp / (c_gg + c_gp)
            e_pg.append(v_pg)
            e_gp.append(v_gp)
            e_tot.append((v_pg + v_gp) / 2.0)
            e_net.append(v_pg - v_gp)
            Phi = [[A[0][0] * Phi[0][0] + A[0][1] * Phi[1][0],
                    A[0][0] * Phi[0][1] + A[0][1] * Phi[1][1]],
                   [A[1][0] * Phi[0][0] + A[1][1] * Phi[1][0],
                    A[1][0] * Phi[0][1] + A[1][1] * Phi[1][1]]]
        h = _F["mh451_spillover"](pw, gs, H=H)
        for i in range(H):
            assert abs(h["S_pg"][i] - e_pg[i]) < 1e-9, i
            assert abs(h["S_gp"][i] - e_gp[i]) < 1e-9, i
            assert abs(h["tot"][i] - e_tot[i]) < 1e-9, i
            assert abs(h["net"][i] - e_net[i]) < 1e-9, i
        assert abs(e_pg[0] - G2P_01) < 1e-9
        assert e_gp[0] == 0.0
        assert abs(e_tot[19] - TOT_20) < 1e-9

    def test_chiave_righe_a_uno(self):
        # OGNI riga della tabella somma a 1 a OGNI orizzonte
        pw, gs = self._pw(), self._gs()
        m = _F["mh451_mappa"](pw, gs, H=30)
        for h in range(30):
            assert abs(m["S_pg"][h] + m["S_pp"][h] - 1.0) < 1e-12, h
            assert abs(m["S_gp"][h] + m["S_gg"][h] - 1.0) < 1e-12, h

    def test_chiave_coerenza_tab449(self):
        # la riga power E' la FEVD di tab449 (1e-9)
        pw, gs = self._pw(), self._gs()
        m = _F["mh451_mappa"](pw, gs, H=20)
        r = _F["mh449_irf"](pw, gs, H=20)
        assert len(r["fevd"]) == 20
        for h in range(20):
            assert abs(m["S_pg"][h] - r["fevd"][h]) < 1e-9, h

    def test_chiave_h1(self):
        # h = 1: valori esatti di Cholesky
        pw, gs = self._pw(), self._gs()
        m = _F["mh451_mappa"](pw, gs, H=1)
        assert m["S_gp"][0] == 0.0
        assert m["S_gg"][0] == 1.0
        assert abs(m["S_pg"][0] - m["corr_resid"] ** 2) < 1e-12
        assert abs(m["tot"][0] - m["corr_resid"] ** 2 / 2.0) < 1e-12
        assert abs(m["S_pg"][0] - 0.3513) < 1e-3  # corr^2

    def test_chiave_beta_vera(self):
        # con la beta VERA (1.5) le righe restano a 1 e il modello
        # ritrova il DGP (cross-check tab448 chiave 1)
        pw, gs = self._pw(), self._gs()
        m = _F["mh451_mappa"](pw, gs, beta=1.5, H=20)
        assert abs(m["beta"] - 1.5) < 1e-12
        assert abs(m["alpha_power"] - A15Y) < 1e-12
        assert abs(A15Y - (-0.3035)) < 1e-3
        for h in range(20):
            assert abs(m["S_pg"][h] + m["S_pp"][h] - 1.0) < 1e-9, h
            assert abs(m["S_gp"][h] + m["S_gg"][h] - 1.0) < 1e-9, h

    def test_controlli(self):
        # RANDOM WALK INDIPENDENTI (Johansen rango 0): niente spillover
        with pytest.raises(ValueError, match="cointegrazione"):
            _F["mh451_mappa"](_rw(20261014), _rw(777))
        # AR(1) STAZIONARIE (Johansen rango 2): niente VECM
        with pytest.raises(ValueError, match="stazionarie"):
            _F["mh451_mappa"](_ar1(0.5, 20261014), _ar1(0.5, 777))

    def test_verdetto_soglie(self):
        v = _F["mh451_verdetto"]
        assert v(0.75).startswith("MERCATI FUSI")
        assert v(0.60).startswith("MERCATI FUSI")
        assert v(0.4569).startswith("FORTEMENTE CONNESSI")
        assert v(0.5999).startswith("FORTEMENTE CONNESSI")
        assert v(0.40).startswith("FORTEMENTE CONNESSI")
        assert v(0.3999).startswith("CONNESSI")
        assert v(0.25).startswith("CONNESSI")
        assert v(0.2499).startswith("DEBOLMENTE CONNESSI")
        assert v(0.10).startswith("DEBOLMENTE CONNESSI")
        assert v(0.0999).startswith("SCOLLEGATI")
        assert v(0.0).startswith("SCOLLEGATI")
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
        _trend = tuple(100.0 + 0.3 * t for t in range(60))
        for bad in (lambda: _F["mh451_mappa"](tuple([1.0] * 29),
                                              tuple([1.0] * 29)),
                    lambda: _F["mh451_mappa"](None, gs),
                    lambda: _F["mh451_mappa"](pw, None),
                    lambda: _F["mh451_mappa"](pw, gs[:50]),
                    lambda: _F["mh451_mappa"](pw, gs + (1.0,)),
                    lambda: _F["mh451_mappa"](flat, gs),
                    lambda: _F["mh451_mappa"](pw, flat),
                    lambda: _F["mh451_mappa"](pw, pw),
                    lambda: _F["mh451_mappa"](_trend, gs),
                    lambda: _F["mh451_spillover"](pw, gs,
                                                 beta=float("nan")),
                    lambda: _F["mh451_spillover"](pw, gs,
                                                 beta=float("inf")),
                    lambda: _F["mh451_spillover"](pw, gs, beta="1.5"),
                    lambda: _F["mh451_spillover"](pw, gs, beta=True),
                    lambda: _F["mh451_spillover"](pw, gs, H=0),
                    lambda: _F["mh451_spillover"](pw, gs, H=121),
                    lambda: _F["mh451_spillover"](pw, gs, H="20"),
                    lambda: _F["mh451_spillover"](pw, gs, H=True),
                    lambda: _F["mh451_num"](float("nan"), "x"),
                    lambda: _F["mh451_num"](True, "x"),
                    lambda: _F["mh451_num"]("1.5", "x")):
            with pytest.raises(ValueError):
                bad()

    def test_parse_serie(self):
        xs = _F["mh451_parse_serie"]("1,5\n" + "2.5\n" * 29)
        assert len(xs) == 30
        assert xs[0] == 1.5 and xs[1] == 2.5
        with pytest.raises(ValueError):
            _F["mh451_parse_serie"]("1\n2\nabc\n" + "1\n" * 30)
        with pytest.raises(ValueError):
            _F["mh451_parse_serie"]("1\n2\n")
        with pytest.raises(ValueError):
            _F["mh451_parse_serie"](None)

    def test_solve(self):
        X = _F["_mh451_solve"]([[2.0, 1.0], [1.0, 3.0]],
                               [[5.0], [10.0]])
        assert abs(X[0][0] - 1.0) < 1e-12
        assert abs(X[1][0] - 3.0) < 1e-12
        with pytest.raises(ValueError):
            _F["_mh451_solve"]([[1.0, 2.0], [2.0, 4.0]],
                               [[1.0], [1.0]])

