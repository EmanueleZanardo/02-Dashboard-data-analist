"""Test tab460 '🛑 Stop & target: dove chiudere il trade': registry + funzioni pure."""

import math
import random
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh460_num", "mh460_piani", "mh460_verdetto", "mh460_mappa",
           "mh459_num", "mh459_shock", "mh459_verdetto", "mh459_mappa",
           "mh458_num", "mh458_pdf", "mh458_quantile", "mh458_var_es",
           "mh458_verdetto", "mh458_mappa",
           "mh457_num", "mh457_mills", "mh457_winloss", "mh457_kelly",
           "mh457_growth", "mh457_verdetto", "mh457_mappa",
           "mh456_num", "mh456_parse_serie", "mh456_phi",
           "mh456_trade", "mh456_verdetto", "mh456_mappa", "_mh456_seq",
           "mh455_num", "mh455_ar1", "mh455_forecast",
           "mh455_verdetto", "_mh455_seq", "_mh455_solve",
           "_mh455_ols",
           "mh447_num", "mh447_eig", "mh447_rango",
           "mh447_trace", "mh447_max", "mh447_critico",
           "_mh447_lam_T", "_mh447_seq", "_mh447_solve",
           "_mh447_mul", "_mh447_transp", "_mh447_ols")

TITLE460 = "🛑 Stop & target: dove chiudere il trade"
TITLE459 = "🧪⚠️ Stress test del trade: VaR sotto shock"
TITLE458 = "⚠️ Quanto posso perdere? VaR del trade dimensionato"
TITLE457 = "📐 Quanto puntare sul rientro? Sizing Kelly del trade"
TITLE456 = "💰 Vale la pena tradare il rientro? P&L atteso del trade"
TITLE469 = "📊 VaR per segnale: chi mangia il capitale?"
TITLE468 = "📉 VaR annuale: quanto capitale di rischio?"
TITLE467 = "📅 L'edge annualizzato: il trade si ripete?"
TITLE466 = "💸 Costi veri: l'edge sopravvive al netto?"
TITLE465 = "📐 Correlazione: la diversificazione è reale?"
TITLE464 = "🧺 Portafoglio: quanti trade insieme?"
TITLE463 = "🔀 Scale-out: tutto insieme o a pezzi?"
TITLE462 = "⏳ Time stop: uscire se non succede niente"
TITLE461 = "🧭 Ottimizza stop/target: i migliori k"
TITLE455 = "🔮 Quando rientra lo spread? Forecast mean-reversion"
TITLE454 = "⚖️ Lo spread è stazionario? Test ADF"
TITLE453 = "📊 Backtest VECM(1): il modello batte il random walk?"
TITLE452 = "📈 Previsione VECM(1): dove vanno power e gas nei prossimi H giorni?"
TITLE451 = "🌊 Spillover gas↔power: chi trasmette e chi riceve gli shock?"
TITLE450 = "📜 Scomposizione storica: cosa ha mosso davvero il prezzo power?"
DEMO_POWER = '115.0\n114.222584\n115.526527\n115.270435\n115.404795\n113.275972\n114.840219\n116.685764\n115.420859\n113.571058\n112.06301\n112.194403\n116.139654\n117.765956\n116.742831\n116.62762\n115.739526\n117.414453\n114.867579\n116.640701\n115.779325\n115.137451\n116.642853\n117.253244\n117.493738\n117.242796\n118.334843\n119.091227\n116.768615\n115.421416\n116.033447\n114.144567\n113.700317\n114.354433\n114.876507\n113.755332\n115.568524\n116.069102\n116.138549\n117.333173\n117.084818\n116.63492\n117.999467\n117.718767\n117.668152\n118.796536\n116.597527\n114.618757\n114.130273\n116.852609\n116.128887\n119.874946\n118.472635\n119.958398\n119.950907\n122.309881\n121.085938\n120.106701\n119.684133\n119.645704\n'
DEMO_GAS = '40.0\n39.387964\n39.576758\n40.074258\n39.817653\n39.153163\n39.120398\n39.359404\n39.908497\n39.300559\n38.654127\n39.007091\n39.244134\n40.011027\n40.502256\n40.451366\n40.314247\n41.599511\n41.45511\n41.062643\n40.493471\n40.541201\n40.613858\n40.441425\n40.410346\n40.546892\n40.893091\n41.441492\n41.5464\n40.651509\n41.002372\n40.292523\n40.206815\n39.469916\n39.470967\n39.081684\n39.188627\n40.838781\n40.814478\n41.23564\n40.573978\n40.429951\n40.761193\n40.714858\n40.899949\n40.951613\n40.448546\n40.730418\n40.324405\n41.260281\n41.00768\n41.350726\n41.351901\n41.828116\n41.527041\n42.026474\n41.964525\n42.596178\n42.908275\n42.978922\n'
BETA = 1.8286056394998358
Z = -1.0023831726745032
H_STAR = 10
MU_PNL = 366747.52222252387
SIGMA_PNL = 444862.37867309677
STOP = -444862.37867309677
TARGET = 889724.7573461935
P_STOP = 0.03404530548738105
P_TARGET = 0.11987871558959617
PNL_CAPPED = 346485.149920618
DELTA = -20262.37230190588
KAP = 1000000.0
K_STOP = 1.0
K_TARGET = 2.0


def _rw(seed, n=60):
    rng = random.Random(seed)
    out = [0.0]
    for _ in range(1, n):
        out.append(out[-1] + rng.gauss(0.0, 1.0))
    return tuple(out)


class TestRegistry460:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 469
        assert "tab460" in dvars
        assert "tab460" in withs

    def test_titoli_allineati_450_451_452_453_454_455_456_457_458_459_460(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab450")] == TITLE450
        assert titoli[dvars.index("tab451")] == TITLE451
        assert titoli[dvars.index("tab452")] == TITLE452
        assert titoli[dvars.index("tab453")] == TITLE453
        assert titoli[dvars.index("tab454")] == TITLE454
        assert titoli[dvars.index("tab455")] == TITLE455
        assert titoli[dvars.index("tab456")] == TITLE456
        assert titoli[dvars.index("tab457")] == TITLE457
        assert titoli[dvars.index("tab458")] == TITLE458
        assert titoli[dvars.index("tab459")] == TITLE459
        assert titoli[dvars.index("tab460")] == TITLE460

    def test_ultima_tab(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert dvars[-1] == "tab469"
        assert titoli[-1] == TITLE469
        assert withs[-1] == "tab469"


class TestStopTarget460:
    def _pw(self):
        return _F["mh456_parse_serie"](DEMO_POWER)

    def _gs(self):
        return _F["mh456_parse_serie"](DEMO_GAS)

    def _m(self, **kw):
        d = dict(z_entry=1.0, costo=0.20, H=10, capitale=KAP,
                 f_max=0.25, k_stop=K_STOP, k_target=K_TARGET)
        d.update(kw)
        return _F["mh460_mappa"](self._pw(), self._gs(), **d)

    def test_demo_valori(self):
        m = self._m()
        assert m["n"] == 60 and m["H"] == 10 and m["T"] == 59
        assert abs(m["beta"] - BETA) < 1e-12
        assert abs(m["beta"] - 1.8286) < 1e-3  # Johansen tab447
        assert abs(m["z"] - Z) < 1e-12
        assert m["segnale"] is True
        assert m["h_star"] == H_STAR == 10
        assert abs(m["mu_pnl"] - MU_PNL) < 1e-9
        assert abs(m["sigma_pnl"] - SIGMA_PNL) < 1e-6
        assert abs(m["k_stop"] - K_STOP) < 1e-12
        assert abs(m["k_target"] - K_TARGET) < 1e-12
        # stop/target: multipli di sigma
        assert abs(m["stop"] - STOP) < 1e-6
        assert abs(m["stop"] - (-K_STOP * SIGMA_PNL)) < 1e-9
        assert abs(m["stop"] - (-444862.4)) < 1.0
        assert abs(m["target"] - TARGET) < 1e-6
        assert abs(m["target"] - (K_TARGET * SIGMA_PNL)) < 1e-9
        assert abs(m["target"] - 889724.8) < 1.0
        assert m["stop"] < 0.0 < m["target"]
        # probabilita' via Phi
        assert abs(m["p_stop"] - P_STOP) < 1e-9
        assert abs(m["p_stop"] - 0.0340) < 1e-3
        assert abs(m["p_target"] - P_TARGET) < 1e-9
        assert abs(m["p_target"] - 0.1199) < 1e-3
        assert 0.0 < m["p_stop"] < 0.15  # non STOP STRETTO
        assert 0.05 < m["p_target"] < 0.5  # non TARGET LONTANO
        # P&L capped e delta
        assert abs(m["pnl_capped"] - PNL_CAPPED) < 1e-6
        assert abs(m["pnl_capped"] - 346485.1) < 1.0
        assert abs(m["delta"] - DELTA) < 1e-6
        assert abs(m["delta"] - (-20262.4)) < 1.0
        assert m["delta"] < 0.0  # la protezione costa il 5.5% dell'edge
        assert abs(m["delta"] / m["mu_pnl"] - (-0.0552)) < 1e-3
        assert m["zero_motivo"] is None
        assert m["verdetto"].startswith("BILANCIATO")
        assert "3.4%" in m["verdetto"] and "12.0%" in m["verdetto"]

    def test_definizione_a_mano(self):
        # p_stop/p_target a mano via Phi (forma indipendente)
        a = (STOP - MU_PNL) / SIGMA_PNL
        b = (TARGET - MU_PNL) / SIGMA_PNL
        assert abs(_F["mh456_phi"](a) - P_STOP) < 1e-12
        assert abs((1.0 - _F["mh456_phi"](b)) - P_TARGET) < 1e-12
        # pnl_capped a mano: integrazione numerica a trapezi
        # (indipendente dalla forma chiusa con Mills)
        N = 20000
        lo, hi = MU_PNL - 8.0 * SIGMA_PNL, MU_PNL + 8.0 * SIGMA_PNL
        dx = (hi - lo) / N
        acc = 0.0
        for i in range(N + 1):
            x = lo + i * dx
            d = (x - MU_PNL) / SIGMA_PNL
            pdf = math.exp(-0.5 * d * d) / math.sqrt(2.0 * math.pi)
            pdf /= SIGMA_PNL
            y = min(max(x, STOP), TARGET)
            w = 0.5 if i in (0, N) else 1.0
            acc += w * y * pdf
        assert abs(acc * dx - PNL_CAPPED) < 1e-1
        assert abs(acc * dx - PNL_CAPPED) < 1e-3 * abs(PNL_CAPPED)
        # forma chiusa a mano: stop*Phi(a)+target*(1-Phi(b))
        #   + mu*(Phi(b)-Phi(a)) + sigma*(phi(a)-phi(b))
        pa = math.exp(-0.5 * a * a) / math.sqrt(2.0 * math.pi)
        pb = math.exp(-0.5 * b * b) / math.sqrt(2.0 * math.pi)
        Fa, Fb = _F["mh456_phi"](a), _F["mh456_phi"](b)
        mano = (STOP * Fa + TARGET * (1.0 - Fb)
                + MU_PNL * (Fb - Fa) + SIGMA_PNL * (pa - pb))
        assert abs(mano - PNL_CAPPED) < 1e-6
        # piani diretto == mappa
        p = _F["mh460_piani"](MU_PNL, SIGMA_PNL, K_STOP, K_TARGET)
        assert abs(p["pnl_capped"] - PNL_CAPPED) < 1e-9
        assert abs(p["delta"] - DELTA) < 1e-9

    def test_chiave_coerenza_tab458(self):
        # sizing e P&L a h* identici a mh458_mappa (riuso, 1e-9)
        m = self._m()
        m458 = _F["mh458_mappa"](self._pw(), self._gs(), z_entry=1.0,
                                 costo=0.20, H=10, capitale=KAP, f_max=0.25)
        assert abs(m["mu_pnl"] - m458["mu_pnl"]) < 1e-9
        assert abs(m["sigma_pnl"] - m458["sigma_pnl"]) < 1e-9
        assert abs(m["size"] - m458["size"]) < 1e-9
        assert abs(m["h_star"] - m458["h_star"]) < 1e-12
        assert m["zero_motivo"] == m458["zero_motivo"]
        # stop/target collassano sui multipli di sigma di tab458
        assert abs(m["stop"] + m["k_stop"] * m458["sigma_pnl"]) < 1e-9
        assert abs(m["target"] - m["k_target"] * m458["sigma_pnl"]) < 1e-9

    def test_controlli(self):
        pw, gs = self._pw(), self._gs()
        # z_entry 5.0 -> nessun segnale -> NESSUN TRADE
        m_ns = self._m(z_entry=5.0)
        assert m_ns["size"] == 0.0
        assert m_ns["pnl_capped"] == 0.0 and m_ns["delta"] == 0.0
        assert m_ns["stop"] == 0.0 and m_ns["target"] == 0.0
        assert m_ns["verdetto"].startswith("NESSUN TRADE")
        # costo 10.0 -> netto negativo -> NESSUN TRADE
        m_nc = self._m(costo=10.0)
        assert m_nc["verdetto"].startswith("NESSUN TRADE")
        # k_stop 0.2 -> stop strettissimo -> STOP STRETTO
        m_st = self._m(k_stop=0.2)
        assert m_st["verdetto"].startswith("STOP STRETTO")
        assert m_st["p_stop"] >= 0.15
        # k_target 3.0 -> target quasi irraggiungibile -> TARGET LONTANO
        m_tl = self._m(k_target=3.0)
        assert m_tl["verdetto"].startswith("TARGET LONTANO")
        assert m_tl["p_target"] < 0.05
        # precedenza: STOP STRETTO batte TARGET LONTANO
        m_both = self._m(k_stop=0.2, k_target=3.0)
        assert m_both["verdetto"].startswith("STOP STRETTO")
        # monotonia: p_stop decresce con k_stop, p_target con k_target
        pss = [self._m(k_stop=k)["p_stop"] for k in (0.5, 1.0, 1.5, 2.0)]
        assert pss == sorted(pss, reverse=True)
        pts = [self._m(k_target=k)["p_target"]
               for k in (1.0, 1.5, 2.0, 2.5, 3.0)]
        assert pts == sorted(pts, reverse=True)
        # pnl_capped: decresce allargando lo stop, cresce col target
        cs = [self._m(k_stop=k)["pnl_capped"] for k in (0.5, 1.0, 2.0)]
        assert cs == sorted(cs, reverse=True)
        ct = [self._m(k_target=k)["pnl_capped"]
              for k in (1.0, 2.0, 3.0)]
        assert ct == sorted(ct)
        # RW indipendenti -> ValueError onesto (rango Johansen != 1)
        with pytest.raises(ValueError):
            _F["mh460_mappa"](_rw(20261014), _rw(777))

    def test_verdetto_soglie(self):
        v = _F["mh460_verdetto"]
        # BILANCIATO: demo-like
        b = v(0.034, 0.12, 346485.0, 366748.0)
        assert b.startswith("BILANCIATO")
        assert "3.4%" in b and "12.0%" in b
        # STOP STRETTO a p_stop = 15% (soglia inclusiva)
        assert v(0.15, 0.12, 300000.0, 366748.0).startswith("STOP STRETTO")
        assert v(0.149, 0.12, 300000.0, 366748.0).startswith("BILANCIATO")
        # TARGET LONTANO sotto il 5%
        assert v(0.03, 0.049, 300000.0, 366748.0).startswith(
            "TARGET LONTANO")
        assert v(0.03, 0.05, 300000.0, 366748.0).startswith("BILANCIATO")
        # precedenza STOP STRETTO > TARGET LONTANO
        assert v(0.20, 0.01, 300000.0, 366748.0).startswith("STOP STRETTO")
        # NESSUN TRADE
        z = v(0.0, 0.0, 0.0, 0.0, zero_motivo="NESSUN SEGNALE")
        assert z.startswith("NESSUN TRADE")
        assert "NESSUN SEGNALE" in z
        # delta positivo: lo stop taglia la coda e alza l'atteso
        bp = v(0.03, 0.12, 400000.0, 366748.0)
        assert bp.startswith("BILANCIATO")
        assert "+33,252" in bp
        for bad in (lambda: v("x", 0.1, 1.0, 1.0),
                    lambda: v(1.5, 0.1, 1.0, 1.0),
                    lambda: v(0.1, -0.1, 1.0, 1.0),
                    lambda: v(0.1, 0.1, float("nan"), 1.0),
                    lambda: v(0.1, 0.1, 1.0, True)):
            with pytest.raises(ValueError):
                bad()

    def test_degeneri(self):
        pw, gs = self._pw(), self._gs()
        for bad in (lambda: _F["mh460_mappa"](pw, gs, k_stop=0.0),
                    lambda: _F["mh460_mappa"](pw, gs, k_stop=-1.0),
                    lambda: _F["mh460_mappa"](pw, gs, k_target=0.0),
                    lambda: _F["mh460_mappa"](pw, gs, k_target=-2.0),
                    lambda: _F["mh460_mappa"](pw, gs, k_stop="1.0"),
                    lambda: _F["mh460_mappa"](pw, gs,
                                             k_stop=float("nan")),
                    lambda: _F["mh460_mappa"](pw, gs, k_stop=True),
                    lambda: _F["mh460_mappa"](pw, gs, f_max=2.0),
                    lambda: _F["mh460_mappa"]((1.0,) * 29, (1.0,) * 29),
                    lambda: _F["mh460_mappa"](None, gs),
                    lambda: _F["mh460_mappa"](pw, gs[:50]),
                    lambda: _F["mh460_piani"](1.0, 0.0, 1.0, 2.0),
                    lambda: _F["mh460_piani"](1.0, -2.0, 1.0, 2.0),
                    lambda: _F["mh460_piani"](1.0, 2.0, 0.0, 2.0),
                    lambda: _F["mh460_piani"](1.0, 2.0, 1.0, 0.0),
                    lambda: _F["mh460_piani"](float("nan"), 2.0, 1.0, 2.0),
                    lambda: _F["mh460_num"](float("nan"), "x"),
                    lambda: _F["mh460_num"](True, "x"),
                    lambda: _F["mh460_num"]("1.5", "x")):
            with pytest.raises(ValueError):
                bad()

    def test_parse_serie(self):
        # parse_serie richiede almeno 30 valori e restituisce una tupla
        assert _F["mh456_parse_serie"]("1,5\n" * 30) == (1.5,) * 30
        assert _F["mh456_parse_serie"]("2.5\n" * 30) == (2.5,) * 30
        with pytest.raises(ValueError):
            _F["mh456_parse_serie"]("1.0\n" * 30 + "abc\n")
        with pytest.raises(ValueError):
            _F["mh456_parse_serie"]("1.0\n" * 29)
