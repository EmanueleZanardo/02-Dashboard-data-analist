"""Test tab447 '⛓️ Johansen: power e gas cointegrati?': registry + funzioni pure."""

import math
import random
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh447_num", "mh447_parse_serie", "mh447_eig",
           "mh447_critico", "mh447_trace", "mh447_max",
           "mh447_rango", "mh447_verdetto", "mh447_mappa",
           "_mh447_seq", "_mh447_solve", "_mh447_ols",
           "_mh447_mul", "_mh447_transp", "_mh447_lam_T",
           "calcola_cointegrazione")

TITLE447 = "⛓️ Johansen: power e gas cointegrati?"
TITLE449 = "💥 Risposta allo shock: di quanto uno shock del gas muove power?"
TITLE451 = "🌊 Spillover gas↔power: chi trasmette e chi riceve gli shock?"
TITLE453 = "📊 Backtest VECM(1): il modello batte il random walk?"
TITLE455 = "🔮 Quando rientra lo spread? Forecast mean-reversion"
TITLE457 = "📐 Quanto puntare sul rientro? Sizing Kelly del trade"
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
TITLE444 = "🏞️ Lake ratio: l'area del dolore sotto il picco"
TITLE443 = "💹 Gain-to-Pain ratio: guadagni totali per ogni punto perso"
TITLE442 = "📐 Calmar geometrico: CAGR composto per unita' di peggior drawdown"
TITLE441 = "📈 Recovery Factor: profitto totale per unita' di peggior drawdown"
TITLE440 = "🎯 Drawdown-at-Risk (DaR): la soglia di drawdown superata solo nell'alpha% dei casi"
TITLE439 = "📉 CDaR ratio: rendimento per unita' di coda media (Conditional Drawdown-at-Risk)"
TITLE438 = "🩹 Pain ratio: rendimento per unita' di dolore medio (Pain Index)"
DEMO_POWER = '115.0\n114.222584\n115.526527\n115.270435\n115.404795\n113.275972\n114.840219\n116.685764\n115.420859\n113.571058\n112.06301\n112.194403\n116.139654\n117.765956\n116.742831\n116.62762\n115.739526\n117.414453\n114.867579\n116.640701\n115.779325\n115.137451\n116.642853\n117.253244\n117.493738\n117.242796\n118.334843\n119.091227\n116.768615\n115.421416\n116.033447\n114.144567\n113.700317\n114.354433\n114.876507\n113.755332\n115.568524\n116.069102\n116.138549\n117.333173\n117.084818\n116.63492\n117.999467\n117.718767\n117.668152\n118.796536\n116.597527\n114.618757\n114.130273\n116.852609\n116.128887\n119.874946\n118.472635\n119.958398\n119.950907\n122.309881\n121.085938\n120.106701\n119.684133\n119.645704\n'
DEMO_GAS = '40.0\n39.387964\n39.576758\n40.074258\n39.817653\n39.153163\n39.120398\n39.359404\n39.908497\n39.300559\n38.654127\n39.007091\n39.244134\n40.011027\n40.502256\n40.451366\n40.314247\n41.599511\n41.45511\n41.062643\n40.493471\n40.541201\n40.613858\n40.441425\n40.410346\n40.546892\n40.893091\n41.441492\n41.5464\n40.651509\n41.002372\n40.292523\n40.206815\n39.469916\n39.470967\n39.081684\n39.188627\n40.838781\n40.814478\n41.23564\n40.573978\n40.429951\n40.761193\n40.714858\n40.899949\n40.951613\n40.448546\n40.730418\n40.324405\n41.260281\n41.00768\n41.350726\n41.351901\n41.828116\n41.527041\n42.026474\n41.964525\n42.596178\n42.908275\n42.978922\n'
LAM1 = 0.27191034421404076
LAM2 = 0.02949042347562858
TRACE0 = 20.141375429884956
TRACE1 = 1.736172510552007
MAX0 = 18.40520291933295
MAX1 = 1.736172510552007
BETA = 1.8286056394998358
EG_BETA = 1.7615
EG_STAT = -3.7925691353180193
EG_HL = 1.1
SPREAD_MEAN = 42.356374118813505
SPREAD_SD = 1.2939388309490982
P2_LAM1 = 0.2532331428788901
P2_LAM2 = 0.03577457090223099
P2_TRACE0 = 18.720647498622
P2_TRACE1 = 2.07651935357966
P2_MAX0 = 16.644128145042338
P2_MAX1 = 2.07651935357966
P2_BETA = 1.8185205318131592
RW_LAM1 = 0.15174315103617825
RW_LAM2 = 0.00020324441906093005
RW_TRACE0 = 9.556953839512662
RW_TRACE1 = 0.011789374408398482
RW_MAX0 = 9.545164465104262
RW_MAX1 = 0.011789374408398482
RW_BETA = 0.5463200061789492
RW_EG_STAT = -1.747519821962829
STAT_LAM1 = 0.28032873518203716
STAT_LAM2 = 0.19196568834152983
STAT_TRACE0 = 31.442467250293678
STAT_TRACE1 = 12.362743873450505
STAT_MAX0 = 19.07972337684317
STAT_MAX1 = 12.362743873450505
STAT_BETA = -9.897262366687045


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


def _solve_mano(A, B):
    """Gauss-Jordan con pivoting parziale (implementazione
    indipendente, scritta per questo test)."""
    n = len(A)
    aug = [list(map(float, A[i])) + list(map(float, B[i]))
           for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(aug[r][col]))
        assert abs(aug[piv][col]) > 1e-12
        aug[col], aug[piv] = aug[piv], aug[col]
        pv = aug[col][col]
        aug[col] = [v / pv for v in aug[col]]
        for r in range(n):
            if r != col and aug[r][col] != 0.0:
                f = aug[r][col]
                aug[r] = [v - f * w for v, w in zip(aug[r], aug[col])]
    return [row[n:] for row in aug]


def _ols_mano(Z, Y):
    """OLS via equazioni normali (indipendente dagli helper)."""
    T = len(Z)
    k = len(Z[0])
    m = len(Y[0])
    xtx = [[sum(Z[t][i] * Z[t][j] for t in range(T))
            for j in range(k)] for i in range(k)]
    xty = [[sum(Z[t][i] * Y[t][j] for t in range(T))
            for j in range(m)] for i in range(k)]
    return _solve_mano(xtx, xty)


def _eg(power, gas):
    import pandas as pd
    idx = pd.date_range("2025-01-01", periods=len(power), freq="D")
    return _F["calcola_cointegrazione"](
        pd.Series(power, index=idx), pd.Series(gas, index=idx),
        min_giorni=30)


class TestRegistry447:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 756
        assert "tab447" in dvars
        assert "tab447" in withs

    def test_titoli_allineati_438_439_440_441_442_443_444_445_446_447(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab438")] == TITLE438
        assert titoli[dvars.index("tab439")] == TITLE439
        assert titoli[dvars.index("tab440")] == TITLE440
        assert titoli[dvars.index("tab441")] == TITLE441
        assert titoli[dvars.index("tab442")] == TITLE442
        assert titoli[dvars.index("tab443")] == TITLE443
        assert titoli[dvars.index("tab444")] == TITLE444
        assert titoli[dvars.index("tab445")] == TITLE445
        assert titoli[dvars.index("tab446")] == TITLE446
        assert titoli[dvars.index("tab447")] == TITLE447

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


class TestJohansen447:
    def _pw(self):
        return _F["mh447_parse_serie"](DEMO_POWER)

    def _gs(self):
        return _F["mh447_parse_serie"](DEMO_GAS)

    def test_demo_valori(self):
        pw, gs = self._pw(), self._gs()
        assert len(pw) == 60 and len(gs) == 60
        assert pw[0] == 115.0 and gs[0] == 40.0
        m = _F["mh447_mappa"](pw, gs)
        assert m["n"] == 60 and m["T"] == 58 and m["p"] == 1
        assert abs(m["lam1"] - LAM1) < 1e-12
        assert abs(m["lam2"] - LAM2) < 1e-12
        assert abs(m["trace0"] - TRACE0) < 1e-12
        assert abs(m["trace1"] - TRACE1) < 1e-12
        assert abs(m["max0"] - MAX0) < 1e-12
        assert abs(m["max1"] - MAX1) < 1e-12
        assert abs(m["beta"] - BETA) < 1e-12
        assert m["crit_trace0"] == 15.41
        assert m["crit_trace1"] == 3.76
        assert m["crit_max0"] == 14.07
        assert m["crit_max1"] == 3.76
        assert m["r_trace"] == 1 and m["r_max"] == 1
        assert m["verdetto"].startswith("COINTEGRAZIONE")
        assert f"{BETA:.4f}" in m["verdetto"]
        assert abs(m["spread_mean"] - SPREAD_MEAN) < 1e-12
        assert abs(m["spread_sd"] - SPREAD_SD) < 1e-12
        assert len(m["spread"]) == 60
        # demo: traccia(0) > critico, traccia(1) < critico;
        # max(0) > critico, max(1) < critico -> rango 1 netto
        assert TRACE0 > 15.41 and TRACE1 < 3.76
        assert MAX0 > 14.07 and MAX1 < 3.76
        assert LAM1 > 0.25 and LAM2 < 0.05

    def test_definizione_a_mano(self):
        pw, gs = self._pw(), self._gs()
        n = len(pw)
        p = 1
        T = n - p - 1
        D, L, Z = [], [], []
        for t in range(p + 1, n):
            D.append([pw[t] - pw[t - 1], gs[t] - gs[t - 1]])
            L.append([pw[t - 1], gs[t - 1]])
            Z.append([pw[t - 1] - pw[t - 2], gs[t - 1] - gs[t - 2],
                      1.0])
        k = 3
        b0 = _ols_mano(Z, D)
        b1 = _ols_mano(Z, L)
        R0 = [[D[t][j] - sum(Z[t][i] * b0[i][j] for i in range(k))
               for j in range(2)] for t in range(T)]
        R1 = [[L[t][j] - sum(Z[t][i] * b1[i][j] for i in range(k))
               for j in range(2)] for t in range(T)]
        S00 = [[sum(R0[t][i] * R0[t][j] for t in range(T)) / T
                for j in range(2)] for i in range(2)]
        S11 = [[sum(R1[t][i] * R1[t][j] for t in range(T)) / T
                for j in range(2)] for i in range(2)]
        S01 = [[sum(R0[t][i] * R1[t][j] for t in range(T)) / T
                for j in range(2)] for i in range(2)]
        S10 = [[S01[j][i] for j in range(2)] for i in range(2)]
        M = [[sum(a * b for a, b in zip(row, col))
              for col in zip(*_solve_mano(S00, S01))]
             for row in _solve_mano(S11, S10)]
        e = _F["mh447_eig"](pw, gs)
        for A, B in ((S00, e["S00"]), (S11, e["S11"]),
                     (S01, e["S01"]), (M, e["M"])):
            for i in range(2):
                for j in range(2):
                    assert abs(A[i][j] - B[i][j]) < 1e-9
        # autovalori a mano da traccia/determinante di M
        tr = M[0][0] + M[1][1]
        det = M[0][0] * M[1][1] - M[0][1] * M[1][0]
        sq = math.sqrt(tr * tr - 4.0 * det)
        assert abs((tr + sq) / 2.0 - e["lam1"]) < 1e-12
        assert abs((tr - sq) / 2.0 - e["lam2"]) < 1e-12
        assert abs((tr + sq) / 2.0 - LAM1) < 1e-12
        # traccia/max a mano dagli autovalori
        assert abs(-T * (math.log(1 - LAM1) + math.log(1 - LAM2))
                   - TRACE0) < 1e-9
        assert abs(-T * math.log(1 - LAM2) - TRACE1) < 1e-9
        assert abs(-T * math.log(1 - LAM1) - MAX0) < 1e-9
        assert abs(-T * math.log(1 - LAM2) - MAX1) < 1e-9
        # beta a mano: autovettore (M01, lam1 - M00), norm. power=1
        v = [M[0][1], LAM1 - M[0][0]]
        assert abs(-v[1] / v[0] - BETA) < 1e-9
        # spread a mano
        sp = [pw[t] - BETA * gs[t] for t in range(n)]
        mu = sum(sp) / n
        assert abs(mu - SPREAD_MEAN) < 1e-9

    def test_identita_trace_max(self):
        # traccia(0) = max(0) + max(1); traccia(1) = max(1) ESATTI
        lam = (LAM1, LAM2)
        assert abs(_F["mh447_trace"](lam, 58, 0)
                   - (_F["mh447_max"](lam, 58, 0)
                      + _F["mh447_max"](lam, 58, 1))) < 1e-12
        assert abs(_F["mh447_trace"](lam, 58, 1)
                   - _F["mh447_max"](lam, 58, 1)) < 1e-12
        # traccia crescente in lam, decrescente in r
        assert _F["mh447_trace"]((0.5, 0.1), 58, 0) > \
            _F["mh447_trace"]((0.5, 0.1), 58, 1)
        assert _F["mh447_max"]((0.5, 0.1), 58, 0) > \
            _F["mh447_max"]((0.5, 0.1), 58, 1)
        # lam = (0, 0) -> statistiche nulle
        assert _F["mh447_trace"]((0.0, 0.0), 58, 0) == 0.0
        assert _F["mh447_max"]((0.0, 0.0), 58, 1) == 0.0

    def test_critici(self):
        c = _F["mh447_critico"]
        assert c(0, "trace") == 15.41
        assert c(1, "trace") == 3.76
        assert c(0, "max") == 14.07
        assert c(1, "max") == 3.76
        for bad in (lambda: c(2, "trace"),
                    lambda: c(-1, "trace"),
                    lambda: c(0.5, "trace"),
                    lambda: c("0", "trace"),
                    lambda: c(0, "foo"),
                    lambda: c(0, None)):
            with pytest.raises(ValueError):
                bad()

    def test_rango_sequenziale(self):
        r = _F["mh447_rango"]
        assert r((LAM1, LAM2), 58, "trace") == 1
        assert r((LAM1, LAM2), 58, "max") == 1
        assert r((RW_LAM1, RW_LAM2), 58, "trace") == 0
        assert r((RW_LAM1, RW_LAM2), 58, "max") == 0
        assert r((STAT_LAM1, STAT_LAM2), 58, "trace") == 2
        assert r((STAT_LAM1, STAT_LAM2), 58, "max") == 2
        assert r((0.0, 0.0), 58, "trace") == 0
        assert r((0.9, 0.9), 58, "trace") == 2
        assert r((0.9, 0.9), 58, "max") == 2
        with pytest.raises(ValueError):
            r((LAM1, LAM2), 58, "foo")

    def test_verdetto_soglie(self):
        v = _F["mh447_verdetto"]
        assert v(0, 0, 1.5).startswith("NESSUNA COINTEGRAZIONE")
        assert v(1, 1, 1.8286).startswith("COINTEGRAZIONE")
        assert "1.8286" in v(1, 1, 1.8286)
        assert v(2, 2, 1.5).startswith("ENTRAMBE STAZIONARIE")
        assert v(1, 0, 1.5).startswith("DISACCORDO")
        assert v(0, 1, 1.5).startswith("DISACCORDO")
        assert v(2, 1, 1.5).startswith("DISACCORDO")
        assert v(1, 2, 1.5).startswith("DISACCORDO")
        for bad in (lambda: v(3, 1, 1.5),
                    lambda: v(-1, 1, 1.5),
                    lambda: v(1.0, 1, 1.5),
                    lambda: v("1", 1, 1.5),
                    lambda: v(1, 1, float("nan")),
                    lambda: v(1, 1, float("inf")),
                    lambda: v(1, 1, "1.5")):
            with pytest.raises(ValueError):
                bad()

    def test_crosscheck_eg(self):
        pw, gs = self._pw(), self._gs()
        eg = _eg(pw, gs)
        assert eg["valido"] is True
        assert eg["cointegrata"] is True
        assert abs(eg["beta"] - EG_BETA) < 1e-9
        assert abs(eg["stat"] - EG_STAT) < 1e-9
        assert abs(eg["half_life_giorni"] - EG_HL) < 1e-9
        # stessa beta (due stimatori dello stesso vettore)
        assert abs(BETA - eg["beta"]) < 0.25
        # sui RW indipendenti EG NON trova cointegrazione
        eg_rw = _eg(_rw(20261014), _rw(777))
        assert eg_rw["cointegrata"] is False
        assert abs(eg_rw["stat"] - RW_EG_STAT) < 1e-9

    def test_p2_robustezza(self):
        pw, gs = self._pw(), self._gs()
        m2 = _F["mh447_mappa"](pw, gs, p=2)
        assert m2["T"] == 57 and m2["p"] == 2
        assert abs(m2["lam1"] - P2_LAM1) < 1e-12
        assert abs(m2["lam2"] - P2_LAM2) < 1e-12
        assert abs(m2["trace0"] - P2_TRACE0) < 1e-12
        assert abs(m2["trace1"] - P2_TRACE1) < 1e-12
        assert abs(m2["max0"] - P2_MAX0) < 1e-12
        assert abs(m2["max1"] - P2_MAX1) < 1e-12
        assert abs(m2["beta"] - P2_BETA) < 1e-12
        assert m2["r_trace"] == 1 and m2["r_max"] == 1
        assert m2["verdetto"].startswith("COINTEGRAZIONE")
        # beta quasi invariante al lag
        assert abs(P2_BETA - BETA) < 0.05

    def test_controlli(self):
        # RANDOM WALK INDIPENDENTI -> rango 0, EG concorda (no)
        mrw = _F["mh447_mappa"](_rw(20261014), _rw(777))
        assert abs(mrw["lam1"] - RW_LAM1) < 1e-12
        assert abs(mrw["lam2"] - RW_LAM2) < 1e-12
        assert abs(mrw["trace0"] - RW_TRACE0) < 1e-12
        assert abs(mrw["trace1"] - RW_TRACE1) < 1e-12
        assert abs(mrw["max0"] - RW_MAX0) < 1e-12
        assert abs(mrw["max1"] - RW_MAX1) < 1e-12
        assert abs(mrw["beta"] - RW_BETA) < 1e-12
        assert mrw["r_trace"] == 0 and mrw["r_max"] == 0
        assert mrw["verdetto"].startswith("NESSUNA COINTEGRAZIONE")
        assert mrw["trace0"] < 15.41 and mrw["max0"] < 14.07
        # AR(1) STAZIONARIE -> rango 2 (il test riconosce le I(0))
        mst = _F["mh447_mappa"](_ar1(0.5, 20261014), _ar1(0.5, 777))
        assert abs(mst["lam1"] - STAT_LAM1) < 1e-12
        assert abs(mst["lam2"] - STAT_LAM2) < 1e-12
        assert abs(mst["trace0"] - STAT_TRACE0) < 1e-12
        assert abs(mst["trace1"] - STAT_TRACE1) < 1e-12
        assert abs(mst["max0"] - STAT_MAX0) < 1e-12
        assert abs(mst["max1"] - STAT_MAX1) < 1e-12
        assert abs(mst["beta"] - STAT_BETA) < 1e-12
        assert mst["r_trace"] == 2 and mst["r_max"] == 2
        assert mst["verdetto"].startswith("ENTRAMBE STAZIONARIE")
        assert mst["trace1"] > 3.76 and mst["max1"] > 3.76

    def test_degeneri(self):
        pw, gs = self._pw(), self._gs()
        flat = tuple([5.0] * 40)
        for bad in (lambda: _F["mh447_mappa"](tuple([1.0] * 29),
                                              tuple([1.0] * 29)),
                    lambda: _F["mh447_mappa"](None, gs),
                    lambda: _F["mh447_mappa"](pw, None),
                    lambda: _F["mh447_mappa"](pw, gs[:50]),
                    lambda: _F["mh447_mappa"](pw, gs + (1.0,)),
                    lambda: _F["mh447_mappa"](flat, gs),
                    lambda: _F["mh447_mappa"](pw, flat),
                    lambda: _F["mh447_mappa"](pw, pw),
                    lambda: _F["mh447_mappa"](pw, gs, p=0),
                    lambda: _F["mh447_mappa"](pw, gs, p=5),
                    lambda: _F["mh447_mappa"](pw, gs, p=2.5),
                    lambda: _F["mh447_mappa"](pw, gs, p="1"),
                    lambda: _F["mh447_eig"](pw, gs, p=0),
                    lambda: _F["mh447_trace"]((1.0, 0.5), 58, 0),
                    lambda: _F["mh447_trace"]((0.5, 1.2), 58, 0),
                    lambda: _F["mh447_trace"]((-0.1, 0.2), 58, 0),
                    lambda: _F["mh447_trace"]((0.2, 0.5), 58, 0),
                    lambda: _F["mh447_trace"]((LAM1, LAM2), 19, 0),
                    lambda: _F["mh447_trace"]((LAM1, LAM2), 58.5, 0),
                    lambda: _F["mh447_trace"]((LAM1, LAM2), 58, 2),
                    lambda: _F["mh447_max"]((LAM1, LAM2), 58, -1),
                    lambda: _F["mh447_rango"]((LAM1, LAM2), 58, "foo"),
                    lambda: _F["mh447_num"](float("nan"), "x"),
                    lambda: _F["mh447_num"](True, "x"),
                    lambda: _F["mh447_num"]("1.5", "x")):
            with pytest.raises(ValueError):
                bad()

    def test_parse_serie(self):
        xs = _F["mh447_parse_serie"]("1,5\n" + "2.5\n" * 29)
        assert len(xs) == 30
        assert xs[0] == 1.5 and xs[1] == 2.5
        with pytest.raises(ValueError):
            _F["mh447_parse_serie"]("1\n2\nabc\n" + "1\n" * 30)
        with pytest.raises(ValueError):
            _F["mh447_parse_serie"]("1\n2\n")
        with pytest.raises(ValueError):
            _F["mh447_parse_serie"](None)

    def test_solve(self):
        X = _F["_mh447_solve"]([[2.0, 1.0], [1.0, 3.0]],
                               [[5.0], [10.0]])
        assert abs(X[0][0] - 1.0) < 1e-12
        assert abs(X[1][0] - 3.0) < 1e-12
        with pytest.raises(ValueError):
            _F["_mh447_solve"]([[1.0, 2.0], [2.0, 4.0]],
                               [[1.0], [1.0]])

