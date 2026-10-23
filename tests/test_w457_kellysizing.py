"""Test tab457 '📐 Quanto puntare sul rientro? Sizing Kelly del trade': registry + funzioni pure."""

import math
import random
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh457_num", "mh457_mills", "mh457_winloss", "mh457_kelly",
           "mh457_growth", "mh457_verdetto", "mh457_mappa",
           "mh456_num", "mh456_parse_serie", "mh456_phi",
           "mh456_trade", "mh456_verdetto", "mh456_mappa", "_mh456_seq",
           "mh455_num", "mh455_ar1", "mh455_forecast",
           "mh455_verdetto", "_mh455_seq", "_mh455_solve",
           "_mh455_ols",
           "mh447_num", "mh447_eig", "mh447_rango",
           "mh447_trace", "mh447_max", "mh447_critico", "_mh447_lam_T",
           "_mh447_seq", "_mh447_solve", "_mh447_mul",
           "_mh447_transp", "_mh447_ols")

TITLE457 = "📐 Quanto puntare sul rientro? Sizing Kelly del trade"
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
TITLE455 = "🔮 Quando rientra lo spread? Forecast mean-reversion"
TITLE454 = "⚖️ Lo spread è stazionario? Test ADF"
TITLE453 = "📊 Backtest VECM(1): il modello batte il random walk?"
TITLE452 = "📈 Previsione VECM(1): dove vanno power e gas nei prossimi H giorni?"
TITLE451 = "🌊 Spillover gas↔power: chi trasmette e chi riceve gli shock?"
TITLE450 = "📜 Scomposizione storica: cosa ha mosso davvero il prezzo power?"
TITLE449 = "💥 Risposta allo shock: di quanto uno shock del gas muove power?"
TITLE448 = "🔗 ECM: quanto in fretta power torna all'equilibrio col gas?"
TITLE447 = "⛓️ Johansen: power e gas cointegrati?"
DEMO_POWER = '115.0\n114.222584\n115.526527\n115.270435\n115.404795\n113.275972\n114.840219\n116.685764\n115.420859\n113.571058\n112.06301\n112.194403\n116.139654\n117.765956\n116.742831\n116.62762\n115.739526\n117.414453\n114.867579\n116.640701\n115.779325\n115.137451\n116.642853\n117.253244\n117.493738\n117.242796\n118.334843\n119.091227\n116.768615\n115.421416\n116.033447\n114.144567\n113.700317\n114.354433\n114.876507\n113.755332\n115.568524\n116.069102\n116.138549\n117.333173\n117.084818\n116.63492\n117.999467\n117.718767\n117.668152\n118.796536\n116.597527\n114.618757\n114.130273\n116.852609\n116.128887\n119.874946\n118.472635\n119.958398\n119.950907\n122.309881\n121.085938\n120.106701\n119.684133\n119.645704\n'
DEMO_GAS = '40.0\n39.387964\n39.576758\n40.074258\n39.817653\n39.153163\n39.120398\n39.359404\n39.908497\n39.300559\n38.654127\n39.007091\n39.244134\n40.011027\n40.502256\n40.451366\n40.314247\n41.599511\n41.45511\n41.062643\n40.493471\n40.541201\n40.613858\n40.441425\n40.410346\n40.546892\n40.893091\n41.441492\n41.5464\n40.651509\n41.002372\n40.292523\n40.206815\n39.469916\n39.470967\n39.081684\n39.188627\n40.838781\n40.814478\n41.23564\n40.573978\n40.429951\n40.761193\n40.714858\n40.899949\n40.951613\n40.448546\n40.730418\n40.324405\n41.260281\n41.00768\n41.350726\n41.351901\n41.828116\n41.527041\n42.026474\n41.964525\n42.596178\n42.908275\n42.978922\n'
BETA = 1.8286056394998358
Z = -1.0023831726745032
H_STAR = 10
LORDO_STAR = 1.2957345182384756
NETTO_STAR = 1.0957345182384757
PROB_STAR = 0.7951457432835478
SE_STAR = 1.3291189023549213
P = 0.7951457432835478
W = 1.570461397655075
L = 0.7469270082577677
B = 2.102563410202864
F_STAR = 0.6977150281277623
F_HALF = 0.34885751406388116
F_APP = 0.25
SIZE = 334704.7264807486
GAMBA_POWER = 334704.7264807486
GAMBA_GAS = -612042.950409947
RISCHIO = 250000.0
PNL = 366747.52222252387
G_KELLY = 0.47293108938832495
G_HALF = 0.34955321913817883
G_APP = 0.2769482365705938


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


class TestRegistry457:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 662
        assert "tab457" in dvars
        assert "tab457" in withs

    def test_titoli_allineati_447_448_449_450_451_452_453_454_455_456_457(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab447")] == TITLE447
        assert titoli[dvars.index("tab448")] == TITLE448
        assert titoli[dvars.index("tab449")] == TITLE449
        assert titoli[dvars.index("tab450")] == TITLE450
        assert titoli[dvars.index("tab451")] == TITLE451
        assert titoli[dvars.index("tab452")] == TITLE452
        assert titoli[dvars.index("tab453")] == TITLE453
        assert titoli[dvars.index("tab454")] == TITLE454
        assert titoli[dvars.index("tab455")] == TITLE455
        assert titoli[dvars.index("tab456")] == TITLE456
        assert titoli[dvars.index("tab457")] == TITLE457

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


class TestKellySizing457:
    def _pw(self):
        return _F["mh456_parse_serie"](DEMO_POWER)

    def _gs(self):
        return _F["mh456_parse_serie"](DEMO_GAS)

    def _mappa(self, **kw):
        d = dict(z_entry=1.0, costo=0.20, H=10,
                 capitale=1000000.0, f_max=0.25)
        d.update(kw)
        return _F["mh457_mappa"](self._pw(), self._gs(), **d)

    def test_demo_valori(self):
        m = self._mappa()
        assert m["n"] == 60 and m["H"] == 10 and m["T"] == 59
        assert abs(m["beta"] - BETA) < 1e-12
        assert abs(m["z"] - Z) < 1e-12
        assert m["segnale"] is True
        assert m["h_star"] == H_STAR == 10
        assert abs(m["lordo_star"] - LORDO_STAR) < 1e-9
        assert abs(m["netto_star"] - NETTO_STAR) < 1e-9
        assert abs(m["prob_star"] - PROB_STAR) < 1e-9
        assert abs(m["p"] - P) < 1e-12
        assert abs(m["p"] - 0.7951) < 1e-3
        assert abs(m["q"] - (1.0 - P)) < 1e-12
        assert abs(m["W"] - W) < 1e-9
        assert abs(m["W"] - 1.5705) < 1e-3
        assert abs(m["L"] - L) < 1e-9
        assert abs(m["L"] - 0.7469) < 1e-3
        assert abs(m["b"] - B) < 1e-9
        assert abs(m["b"] - 2.1026) < 1e-3
        assert abs(m["f_star"] - F_STAR) < 1e-9
        assert abs(m["f_star"] - 0.6977) < 1e-3
        assert abs(m["f_half"] - F_HALF) < 1e-9
        assert abs(m["f_half"] - m["f_star"] / 2.0) < 1e-12
        assert m["f_app"] == F_APP == 0.25
        assert m["capped"] is True
        assert abs(m["size"] - SIZE) < 1e-6
        assert abs(m["size"] - m["f_app"] * 1000000.0 / m["L"]) < 1e-9
        assert abs(m["gamba_power"] - GAMBA_POWER) < 1e-6
        assert abs(m["gamba_gas"] - GAMBA_GAS) < 1e-6
        assert abs(m["gamba_gas"] + m["size"] * m["beta"]) < 1e-6
        assert m["direzione"].startswith("long spread")
        assert abs(m["rischio"] - RISCHIO) < 1e-6
        assert abs(m["rischio"] - m["size"] * m["L"]) < 1e-9
        assert abs(m["pnl_atteso"] - PNL) < 1e-6
        assert abs(m["pnl_atteso"] - m["size"] * m["netto_star"]) < 1e-9
        assert abs(m["g_kelly"] - G_KELLY) < 1e-9
        assert abs(m["g_half"] - G_HALF) < 1e-9
        assert abs(m["g_app"] - G_APP) < 1e-9
        # Kelly massimizza g(f): i vicini stanno sotto
        assert m["g_kelly"] > m["g_half"] > m["g_app"] > 0.0
        assert m["verdetto"].startswith("CAPPATO")
        assert m["verdetto_456"].startswith("CONVIENE")
        assert m["zero_motivo"] is None

    def test_definizione_a_mano(self):
        # Momenti della normale troncata per integrazione numerica
        # (trapezi), indipendente dalla formula chiusa di Mills;
        # Phi/phi implementati a mano con math.erf.
        mu, se, co = LORDO_STAR, SE_STAR, 0.20

        def phi(x):
            return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)

        def Phi(x):
            return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

        def dens(x):
            return phi((x - mu) / se) / se

        n = 200000
        # W: integrale da co a mu+12*se di (x - co) * dens(x)
        a, b_ = co, mu + 12.0 * se
        h = (b_ - a) / n
        s = 0.5 * ((a - co) * dens(a) + (b_ - co) * dens(b_))
        x = a + h
        for _ in range(1, n):
            s += (x - co) * dens(x)
            x += h
        e_pos = s * h
        p = Phi((mu - co) / se)
        W_mano = e_pos / p
        # L: integrale da mu-12*se a co di (co - x) * dens(x)
        a2, b2 = mu - 12.0 * se, co
        h2 = (b2 - a2) / n
        s2 = 0.5 * ((co - a2) * dens(a2) + (co - b2) * dens(b2))
        x = a2 + h2
        for _ in range(1, n):
            s2 += (co - x) * dens(x)
            x += h2
        e_neg = s2 * h2
        L_mano = e_neg / (1.0 - p)
        wl = _F["mh457_winloss"](mu, se, co)
        assert abs(wl["W"] - W_mano) < 1e-6
        assert abs(wl["L"] - L_mano) < 1e-6
        assert abs(wl["p"] - p) < 1e-12
        # Kelly a mano
        f_mano = p - (1.0 - p) / (W_mano / L_mano)
        assert abs(_F["mh457_kelly"](p, W_mano, L_mano) - f_mano) < 1e-12
        assert abs(_F["mh457_kelly"](wl["p"], wl["W"], wl["L"])
                   - F_STAR) < 1e-9
        # crescita a mano
        g_mano = (p * math.log(1.0 + F_STAR * (W_mano / L_mano))
                  + (1.0 - p) * math.log(1.0 - F_STAR))
        assert abs(_F["mh457_growth"](p, W_mano / L_mano, F_STAR)
                   - g_mano) < 1e-12
        # Mills a mano: phi(0)/Phi(0) = sqrt(2/pi)
        assert abs(_F["mh457_mills"](0.0) - math.sqrt(2.0 / math.pi)) < 1e-12

    def test_chiave_coerenza_tab456(self):
        m = self._mappa()
        m456 = _F["mh456_mappa"](self._pw(), self._gs(),
                                 z_entry=1.0, costo=0.20, H=10)
        assert abs(m["lordo_star"] - m456["lordo_star"]) < 1e-9
        assert abs(m["prob_star"] - m456["prob_star"]) < 1e-9
        assert abs(m["p"] - m456["prob_star"]) < 1e-12  # p = Phi(d)
        se_star = m456["se_h"][m456["h_star"] - 1]
        assert abs(se_star - SE_STAR) < 1e-12
        d = (m456["lordo_star"] - 0.20) / se_star
        assert abs(m["p"] - _F["mh456_phi"](d)) < 1e-12

    def test_chiave_beta_vera(self):
        # con la beta vera (1.5) il trade gira comunque
        m = _F["mh457_mappa"](self._pw(), self._gs(), beta=1.5,
                              z_entry=1.0, costo=0.20, H=10)
        assert m["verdetto"].split(" — ")[0] in (
            "SIZING ZERO", "NESSUN EDGE", "CAPPATO", "OK")
        assert m["size"] >= 0.0

    def test_controlli(self):
        # RW indipendenti: Johansen non trova cointegrazione ->
        # ValueError onesto (niente spread identificato, niente sizing)
        with pytest.raises(ValueError):
            _F["mh457_mappa"](tuple(35.0 + v for v in _rw(7)),
                              tuple(20.0 + v for v in _rw(99)))
        # gas RW + spread AR(1) stazionario (seed demo: cointegrazione
        # rilevata) -> verdetto in uno dei 5 stati
        gs_c = tuple(35.0 + v for v in _rw(11))
        sp_c = _ar1(0.6, 777)
        pw_c = tuple(1.5 * g + s + 55.0 for g, s in zip(gs_c, sp_c))
        m = _F["mh457_mappa"](pw_c, gs_c)
        assert m["verdetto"].split(" — ")[0] in (
            "SIZING ZERO", "NESSUN EDGE", "CAPPATO", "OK")
        # z_entry alta -> nessun segnale -> sizing zero
        m2 = self._mappa(z_entry=5.0)
        assert m2["verdetto"].startswith("SIZING ZERO")
        assert m2["size"] == 0.0 and m2["f_app"] == 0.0
        assert m2["zero_motivo"] is not None
        # costo alto -> non conviene -> sizing zero
        m3 = self._mappa(costo=10.0)
        assert m3["verdetto"].startswith("SIZING ZERO")
        assert m3["size"] == 0.0
        # AR(1) mean-reverting cointegrate (seed demo): sizing non negativo
        gs_a = tuple(35.0 + v for v in _rw(11))
        sp_a = _ar1(0.6, 777)
        pw_a = tuple(1.5 * g + s + 55.0 for g, s in zip(gs_a, sp_a))
        m4 = _F["mh457_mappa"](pw_a, gs_a)
        assert m4["size"] >= 0.0
        # cap stretto -> CAPPATO con f_app = f_max
        m5 = self._mappa(f_max=0.05)
        assert m5["verdetto"].startswith("CAPPATO")
        assert m5["f_app"] == 0.05
        assert abs(m5["size"] - 0.05 * 1000000.0 / m5["L"]) < 1e-9
        # cap largo oltre f* -> OK
        m6 = self._mappa(f_max=1.0)
        assert m6["verdetto"].startswith("OK")
        assert abs(m6["f_app"] - m6["f_star"]) < 1e-12

    def test_verdetto_soglie(self):
        v = _F["mh457_verdetto"]
        assert v(0.0, 0.0, False,
                 zero_motivo="NESSUN SEGNALE — test").startswith(
                     "SIZING ZERO")
        assert v(-0.05, 0.0, False).startswith("NESSUN EDGE")
        assert v(0.0, 0.0, False).startswith("NESSUN EDGE")
        assert v(0.6977, 0.25, True).startswith("CAPPATO")
        assert v(0.20, 0.20, False).startswith("OK")
        with pytest.raises(ValueError):
            v(0.2, 0.2, "si")
        with pytest.raises(ValueError):
            v(0.2, 1.5, False)

    def test_degeneri(self):
        pw, gs = self._pw(), self._gs()
        with pytest.raises(ValueError):
            _F["mh457_mappa"](pw[:20], gs)  # < 30
        with pytest.raises(ValueError):
            _F["mh457_mappa"](pw, gs[:50])  # lunghezze diverse
        with pytest.raises(ValueError):
            _F["mh457_mappa"]((100.0,) * 60, gs)  # costante
        with pytest.raises(ValueError):
            _F["mh457_mappa"](pw, gs, beta=float("nan"))
        with pytest.raises(ValueError):
            self._mappa(H=0)
        with pytest.raises(ValueError):
            self._mappa(capitale=0.0)
        with pytest.raises(ValueError):
            self._mappa(capitale=-5.0)
        with pytest.raises(ValueError):
            self._mappa(capitale="x")
        with pytest.raises(ValueError):
            self._mappa(f_max=0.0)
        with pytest.raises(ValueError):
            self._mappa(f_max=1.5)
        with pytest.raises(ValueError):
            self._mappa(f_max="x")
        wl = _F["mh457_winloss"]
        with pytest.raises(ValueError):
            wl(1.0, 0.0, 0.2)  # se <= 0
        with pytest.raises(ValueError):
            wl(1.0, -1.0, 0.2)
        with pytest.raises(ValueError):
            wl("x", 1.0, 0.2)
        k = _F["mh457_kelly"]
        with pytest.raises(ValueError):
            k(1.5, 1.0, 1.0)  # p fuori [0, 1]
        with pytest.raises(ValueError):
            k(0.5, -1.0, 1.0)  # W <= 0
        with pytest.raises(ValueError):
            k(0.5, 1.0, 0.0)  # L <= 0
        g = _F["mh457_growth"]
        with pytest.raises(ValueError):
            g(0.5, 2.0, 1.0)  # f >= 1
        with pytest.raises(ValueError):
            g(0.5, 2.0, -0.1)
        with pytest.raises(ValueError):
            g(0.5, 0.0, 0.1)  # b <= 0
        with pytest.raises(ValueError):
            g(1.2, 2.0, 0.1)
        with pytest.raises(ValueError):
            _F["mh457_mills"]("x")
        with pytest.raises(ValueError):
            _F["mh457_num"](True, "x")
        with pytest.raises(ValueError):
            _F["mh457_num"](float("nan"), "x")
        # crescita nulla a f = 0, Kelly interiorizza il massimo
        assert _F["mh457_growth"](P, B, 0.0) == 0.0
        assert _F["mh457_growth"](P, B, F_STAR - 0.01) < G_KELLY
        assert _F["mh457_growth"](P, B, F_STAR + 0.01) < G_KELLY

    def test_parse_serie(self):
        p = _F["mh456_parse_serie"]
        xs = p("1,5\n" + "2.5\n" * 29)
        assert len(xs) == 30
        assert xs[0] == 1.5 and xs[1] == 2.5
        with pytest.raises(ValueError):
            p("1\n2\nabc\n" + "1\n" * 30)
        with pytest.raises(ValueError):
            p("1\n2\n")
