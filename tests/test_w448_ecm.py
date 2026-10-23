"""Test tab448 '🔗 ECM: quanto in fretta power torna all'equilibrio col gas?': registry + funzioni pure."""

import math
import random
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh448_num", "mh448_parse_serie", "mh448_ecm",
           "mh448_half_life", "mh448_verdetto", "mh448_mappa",
           "_mh448_seq", "_mh448_solve", "_mh448_ols",
           "mh447_num", "mh447_eig",
           "_mh447_seq", "_mh447_solve", "_mh447_mul",
           "_mh447_transp", "_mh447_ols",
           "calcola_cointegrazione")

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
TITLE447 = "⛓️ Johansen: power e gas cointegrati?"
TITLE449 = "💥 Risposta allo shock: di quanto uno shock del gas muove power?"
TITLE451 = "🌊 Spillover gas↔power: chi trasmette e chi riceve gli shock?"
TITLE453 = "📊 Backtest VECM(1): il modello batte il random walk?"
TITLE455 = "🔮 Quando rientra lo spread? Forecast mean-reversion"
TITLE457 = "📐 Quanto puntare sul rientro? Sizing Kelly del trade"
TITLE446 = "📏 Variance ratio: il prezzo segue un random walk?"
TITLE445 = "🌀 Rolling drawdown: il peggior calo in ogni finestra"
TITLE444 = "🏞️ Lake ratio: l'area del dolore sotto il picco"
TITLE443 = "💹 Gain-to-Pain ratio: guadagni totali per ogni punto perso"
TITLE442 = "📐 Calmar geometrico: CAGR composto per unita' di peggior drawdown"
TITLE441 = "📈 Recovery Factor: profitto totale per unita' di peggior drawdown"
TITLE440 = "🎯 Drawdown-at-Risk (DaR): la soglia di drawdown superata solo nell'alpha% dei casi"
TITLE439 = "📉 CDaR ratio: rendimento per unita' di coda media (Conditional Drawdown-at-Risk)"
DEMO_POWER = '115.0\n114.222584\n115.526527\n115.270435\n115.404795\n113.275972\n114.840219\n116.685764\n115.420859\n113.571058\n112.06301\n112.194403\n116.139654\n117.765956\n116.742831\n116.62762\n115.739526\n117.414453\n114.867579\n116.640701\n115.779325\n115.137451\n116.642853\n117.253244\n117.493738\n117.242796\n118.334843\n119.091227\n116.768615\n115.421416\n116.033447\n114.144567\n113.700317\n114.354433\n114.876507\n113.755332\n115.568524\n116.069102\n116.138549\n117.333173\n117.084818\n116.63492\n117.999467\n117.718767\n117.668152\n118.796536\n116.597527\n114.618757\n114.130273\n116.852609\n116.128887\n119.874946\n118.472635\n119.958398\n119.950907\n122.309881\n121.085938\n120.106701\n119.684133\n119.645704\n'
DEMO_GAS = '40.0\n39.387964\n39.576758\n40.074258\n39.817653\n39.153163\n39.120398\n39.359404\n39.908497\n39.300559\n38.654127\n39.007091\n39.244134\n40.011027\n40.502256\n40.451366\n40.314247\n41.599511\n41.45511\n41.062643\n40.493471\n40.541201\n40.613858\n40.441425\n40.410346\n40.546892\n40.893091\n41.441492\n41.5464\n40.651509\n41.002372\n40.292523\n40.206815\n39.469916\n39.470967\n39.081684\n39.188627\n40.838781\n40.814478\n41.23564\n40.573978\n40.429951\n40.761193\n40.714858\n40.899949\n40.951613\n40.448546\n40.730418\n40.324405\n41.260281\n41.00768\n41.350726\n41.351901\n41.828116\n41.527041\n42.026474\n41.964525\n42.596178\n42.908275\n42.978922\n'
BETA = 1.8286056394998358
ALPHA_P = -0.2604753448087028
SE_P = 0.14374605784786604
T_P = -1.812052091782423
HL_P = 2.2971087410381923
R2_P = 0.054468154597616336
ALPHA_G = 0.13052976063089952
SE_G = 0.04699080215057056
T_G = 2.7777725566941536
R2_G = 0.11922890702807254
ALPHA_P15 = -0.30346693792017626
SE_P15 = 0.13851967117183878
T_P15 = -2.190785867111353
HL_P15 = 1.9166772095349338
R2_P15 = 0.07766307814974105
EG_BETA = 1.7615
EG_STAT = -3.7925691353180193
EG_HL = 1.1
RW_BETA = 0.5463200061789492
RW_ALPHA_P = -0.10642288897302919
RW_T_P = -2.72302041916675
RW_HL_P = 6.160068269402087
RW_ALPHA_G = 0.019870269598439086
RW_T_G = 0.4325307421383448
STAT_BETA = -9.897262366687045
STAT_ALPHA_P = -0.0022286221196297453
STAT_HL_P = 310.67380408768514


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
    helper): ritorna (a, c, se_a, t_a, r2)."""
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
    ym = s_y / n
    sst = sum((y - ym) ** 2 for y in ys)
    r2 = 1.0 - sum(r * r for r in resid) / sst
    return a, c, se_a, a / se_a, r2


def _eg(power, gas):
    import pandas as pd
    idx = pd.date_range("2025-01-01", periods=len(power), freq="D")
    return _F["calcola_cointegrazione"](
        pd.Series(power, index=idx), pd.Series(gas, index=idx),
        min_giorni=30)


class TestRegistry448:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 659
        assert "tab448" in dvars
        assert "tab448" in withs

    def test_titoli_allineati_439_440_441_442_443_444_445_446_447_448(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab439")] == TITLE439
        assert titoli[dvars.index("tab440")] == TITLE440
        assert titoli[dvars.index("tab441")] == TITLE441
        assert titoli[dvars.index("tab442")] == TITLE442
        assert titoli[dvars.index("tab443")] == TITLE443
        assert titoli[dvars.index("tab444")] == TITLE444
        assert titoli[dvars.index("tab445")] == TITLE445
        assert titoli[dvars.index("tab446")] == TITLE446
        assert titoli[dvars.index("tab447")] == TITLE447
        assert titoli[dvars.index("tab448")] == TITLE448

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


class TestECM448:
    def _pw(self):
        return _F["mh448_parse_serie"](DEMO_POWER)

    def _gs(self):
        return _F["mh448_parse_serie"](DEMO_GAS)

    def test_demo_valori(self):
        pw, gs = self._pw(), self._gs()
        assert len(pw) == 60 and len(gs) == 60
        assert pw[0] == 115.0 and gs[0] == 40.0
        m = _F["mh448_mappa"](pw, gs)
        assert m["n"] == 60 and m["T"] == 59
        assert abs(m["beta"] - BETA) < 1e-12
        assert abs(m["beta"] - 1.8286) < 1e-3  # Johansen tab447
        assert abs(m["alpha_power"] - ALPHA_P) < 1e-12
        assert abs(m["se_power"] - SE_P) < 1e-12
        assert abs(m["t_power"] - T_P) < 1e-12
        assert abs(m["hl_power"] - HL_P) < 1e-12
        assert abs(m["r2_power"] - R2_P) < 1e-12
        assert abs(m["alpha_gas"] - ALPHA_G) < 1e-12
        assert abs(m["se_gas"] - SE_G) < 1e-12
        assert abs(m["t_gas"] - T_G) < 1e-12
        assert abs(m["r2_gas"] - R2_G) < 1e-12
        assert len(m["ec"]) == 60
        assert abs(sum(m["ec"]) / 60) < 1e-9  # demeaned
        assert m["verdetto"].startswith("CONVERGENZA MODERATA")
        assert f"{HL_P:.2f}" in m["verdetto"]
        # demo: power corregge (alpha < 0), hl in (2, 6]
        assert ALPHA_P < 0.0
        assert 2.0 < HL_P <= 6.0
        # in QUESTO campione il gas ha t > 2 (rumore: e' un RW puro
        # per costruzione, vedi chiave 3) -> flag esogeneita' False
        assert T_G > 2.0
        assert m["gas_esogeno"] is False

    def test_definizione_a_mano(self):
        pw, gs = self._pw(), self._gs()
        n = len(pw)
        ec_raw = [y - BETA * g for y, g in zip(pw, gs)]
        mu = sum(ec_raw) / n
        ec = [v - mu for v in ec_raw]
        for nome, y, const in (("power", pw, (ALPHA_P, SE_P, T_P,
                                               R2_P)),
                               ("gas", gs, (ALPHA_G, SE_G, T_G,
                                            R2_G))):
            dy = [y[t] - y[t - 1] for t in range(1, n)]
            a, c, se_a, t_a, r2 = _ols2_mano(ec[:-1], dy)
            ea, ese, et, er2 = const
            assert abs(a - ea) < 1e-9, nome
            assert abs(se_a - ese) < 1e-9, nome
            assert abs(t_a - et) < 1e-9, nome
            assert abs(r2 - er2) < 1e-9, nome
            e = _F["mh448_ecm"](pw, gs)
            assert abs(e[f"alpha_{nome}"] - a) < 1e-12, nome
        # half-life a mano da alpha_power
        assert abs(-math.log(2.0) / math.log(1.0 + ALPHA_P)
                   - HL_P) < 1e-9
        assert abs(_F["mh448_half_life"](ALPHA_P) - HL_P) < 1e-12

    def test_chiave_beta_vera(self):
        # con la beta VERA (1.5, nota per costruzione) il segnale
        # non e' diluito: alpha piu' negativo, t significativo
        pw, gs = self._pw(), self._gs()
        e = _F["mh448_ecm"](pw, gs, beta=1.5)
        assert abs(e["beta"] - 1.5) < 1e-12
        assert abs(e["alpha_power"] - ALPHA_P15) < 1e-12
        assert abs(e["se_power"] - SE_P15) < 1e-12
        assert abs(e["t_power"] - T_P15) < 1e-12
        assert abs(e["hl_power"] - HL_P15) < 1e-12
        assert abs(e["r2_power"] - R2_P15) < 1e-12
        assert T_P15 < -2.0  # significativo al 5%
        assert e["alpha_power"] < ALPHA_P  # meno attenuato
        assert e["hl_power"] < HL_P
        m = _F["mh448_mappa"](pw, gs, beta=1.5)
        assert m["verdetto"].startswith("CONVERGENZA RAPIDA")

    def test_half_life_formula(self):
        h = _F["mh448_half_life"]
        # alpha = -(1 - phi) con phi = 0.6 -> hl teorica ESATTA
        assert abs(h(-0.4) - (-math.log(2.0) / math.log(0.6))) < 1e-12
        assert abs(h(-0.4) - 1.3569) < 1e-3
        assert h(-1.0) == 1.0
        assert h(0.0) is None
        assert h(0.1) is None
        assert h(-2.0) is None
        assert h(-2.5) is None
        for bad in (lambda: h(float("nan")),
                    lambda: h(float("inf")),
                    lambda: h("x"),
                    lambda: h(True)):
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
        # stessa beta a meno di 0.25 (due stimatori)
        assert abs(BETA - eg["beta"]) < 0.25
        # half-life stesso ordine di grandezza (metodi diversi)
        assert EG_HL < 5.0 and HL_P15 < 5.0

    def test_controlli(self):
        # RANDOM WALK INDIPENDENTI -> beta spuria, ECM senza senso:
        # hl 6.16 (LENTA) su una relazione che non esiste (tab447:
        # rango 0). Lezione: l'ECM vuole prima la cointegrazione.
        mrw = _F["mh448_mappa"](_rw(20261014), _rw(777))
        assert abs(mrw["beta"] - RW_BETA) < 1e-12
        assert abs(mrw["alpha_power"] - RW_ALPHA_P) < 1e-12
        assert abs(mrw["t_power"] - RW_T_P) < 1e-12
        assert abs(mrw["hl_power"] - RW_HL_P) < 1e-12
        assert abs(mrw["alpha_gas"] - RW_ALPHA_G) < 1e-12
        assert abs(mrw["t_gas"] - RW_T_G) < 1e-12
        assert mrw["verdetto"].startswith("CONVERGENZA LENTA")
        # AR(1) STAZIONARIE -> niente da correggere: hl 310.67
        mst = _F["mh448_mappa"](_ar1(0.5, 20261014), _ar1(0.5, 777))
        assert abs(mst["beta"] - STAT_BETA) < 1e-12
        assert abs(mst["alpha_power"] - STAT_ALPHA_P) < 1e-12
        assert abs(mst["hl_power"] - STAT_HL_P) < 1e-12
        assert mst["verdetto"].startswith("CONVERGENZA LENTA")

    def test_verdetto_soglie(self):
        v = _F["mh448_verdetto"]
        assert v(0.1, None).startswith("DIVERGENZA")
        assert v(0.0, None).startswith("DIVERGENZA")
        assert v(-2.5, None).startswith("DIVERGENZA OSCILLANTE")
        assert v(-2.0, None).startswith("DIVERGENZA OSCILLANTE")
        assert v(-0.5, 1.5).startswith("CONVERGENZA RAPIDA")
        assert v(-0.5, 2.0).startswith("CONVERGENZA RAPIDA")
        assert v(-0.2605, 2.30).startswith("CONVERGENZA MODERATA")
        assert v(-0.1, 6.0).startswith("CONVERGENZA MODERATA")
        assert v(-0.05, 6.16).startswith("CONVERGENZA LENTA")
        assert v(-0.001, 310.0).startswith("CONVERGENZA LENTA")
        for bad in (lambda: v(float("nan"), 2.0),
                    lambda: v(float("inf"), 2.0),
                    lambda: v("x", 2.0),
                    lambda: v(True, 2.0),
                    lambda: v(-0.5, None),
                    lambda: v(-0.5, float("nan")),
                    lambda: v(-0.5, float("inf")),
                    lambda: v(-0.5, -1.0),
                    lambda: v(-0.5, True)):
            with pytest.raises(ValueError):
                bad()

    def test_degeneri(self):
        pw, gs = self._pw(), self._gs()
        flat = tuple([5.0] * 40)
        for bad in (lambda: _F["mh448_mappa"](tuple([1.0] * 29),
                                              tuple([1.0] * 29)),
                    lambda: _F["mh448_mappa"](None, gs),
                    lambda: _F["mh448_mappa"](pw, None),
                    lambda: _F["mh448_mappa"](pw, gs[:50]),
                    lambda: _F["mh448_mappa"](pw, gs + (1.0,)),
                    lambda: _F["mh448_mappa"](flat, gs),
                    lambda: _F["mh448_mappa"](pw, flat),
                    lambda: _F["mh448_mappa"](pw, pw),
                    lambda: _F["mh448_ecm"](pw, gs,
                                            beta=float("nan")),
                    lambda: _F["mh448_ecm"](pw, gs,
                                            beta=float("inf")),
                    lambda: _F["mh448_ecm"](pw, gs, beta="1.5"),
                    lambda: _F["mh448_ecm"](pw, gs, beta=True),
                    lambda: _F["mh448_num"](float("nan"), "x"),
                    lambda: _F["mh448_num"](True, "x"),
                    lambda: _F["mh448_num"]("1.5", "x")):
            with pytest.raises(ValueError):
                bad()

    def test_parse_serie(self):
        xs = _F["mh448_parse_serie"]("1,5\n" + "2.5\n" * 29)
        assert len(xs) == 30
        assert xs[0] == 1.5 and xs[1] == 2.5
        with pytest.raises(ValueError):
            _F["mh448_parse_serie"]("1\n2\nabc\n" + "1\n" * 30)
        with pytest.raises(ValueError):
            _F["mh448_parse_serie"]("1\n2\n")
        with pytest.raises(ValueError):
            _F["mh448_parse_serie"](None)

    def test_solve(self):
        X = _F["_mh448_solve"]([[2.0, 1.0], [1.0, 3.0]],
                               [[5.0], [10.0]])
        assert abs(X[0][0] - 1.0) < 1e-12
        assert abs(X[1][0] - 3.0) < 1e-12
        with pytest.raises(ValueError):
            _F["_mh448_solve"]([[1.0, 2.0], [2.0, 4.0]],
                               [[1.0], [1.0]])

