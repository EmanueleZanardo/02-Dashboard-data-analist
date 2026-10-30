"""Test tab461 '🧭 Ottimizza stop/target: i migliori k': registry + funzioni pure."""

import math
import random
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh461_num", "mh461_asse", "mh461_ottimo", "mh461_verdetto",
           "mh461_mappa",
           "mh460_num", "mh460_piani", "mh460_verdetto", "mh460_mappa",
           "mh459_num", "mh459_shock", "mh459_verdetto", "mh459_mappa",
           "mh458_num", "mh458_pdf", "mh458_quantile", "mh458_var_es",
           "mh458_verdetto", "mh458_mappa",
           "mh457_num", "mh457_mills", "mh457_winloss", "mh457_kelly",
           "mh457_growth", "mh457_verdetto", "mh457_mappa",
           "mh456_num", "mh456_parse_serie", "mh456_phi",
           "mh456_trade", "mh456_verdetto", "mh456_mappa", "_mh456_seq",
           "mh455_num", "mh455_ar1", "mh455_forecast",
           "mh455_verdetto", "_mh455_seq", "_mh455_solve", "_mh455_ols",
           "mh447_num", "mh447_eig", "mh447_rango",
           "mh447_trace", "mh447_max", "mh447_critico",
           "_mh447_lam_T", "_mh447_seq", "_mh447_solve",
           "_mh447_mul", "_mh447_transp", "_mh447_ols")

TITLE461 = "🧭 Ottimizza stop/target: i migliori k"
TITLE460 = "🛑 Stop & target: dove chiudere il trade"
TITLE482 = "🗓️ Ladder delle scadenze: profilo temporale di volumi, MtM e DV01"
TITLE459 = "🧪⚠️ Stress test del trade: VaR sotto shock"
TITLE458 = "⚠️ Quanto posso perdere? VaR del trade dimensionato"
TITLE475 = "💰 Costo di esecuzione: quanto costa davvero ruotare"
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
TITLE455 = "🔮 Quando rientra lo spread? Forecast mean-reversion"
TITLE454 = "⚖️ Lo spread è stazionario? Test ADF"
TITLE453 = "📊 Backtest VECM(1): il modello batte il random walk?"
TITLE452 = "📈 Previsione VECM(1): dove vanno power e gas nei prossimi H giorni?"
TITLE451 = "🌊 Spillover gas↔power: chi trasmette e chi riceve gli shock?"
DEMO_POWER = '115.0\n114.222584\n115.526527\n115.270435\n115.404795\n113.275972\n114.840219\n116.685764\n115.420859\n113.571058\n112.06301\n112.194403\n116.139654\n117.765956\n116.742831\n116.62762\n115.739526\n117.414453\n114.867579\n116.640701\n115.779325\n115.137451\n116.642853\n117.253244\n117.493738\n117.242796\n118.334843\n119.091227\n116.768615\n115.421416\n116.033447\n114.144567\n113.700317\n114.354433\n114.876507\n113.755332\n115.568524\n116.069102\n116.138549\n117.333173\n117.084818\n116.63492\n117.999467\n117.718767\n117.668152\n118.796536\n116.597527\n114.618757\n114.130273\n116.852609\n116.128887\n119.874946\n118.472635\n119.958398\n119.950907\n122.309881\n121.085938\n120.106701\n119.684133\n119.645704\n'
DEMO_GAS = '40.0\n39.387964\n39.576758\n40.074258\n39.817653\n39.153163\n39.120398\n39.359404\n39.908497\n39.300559\n38.654127\n39.007091\n39.244134\n40.011027\n40.502256\n40.451366\n40.314247\n41.599511\n41.45511\n41.062643\n40.493471\n40.541201\n40.613858\n40.441425\n40.410346\n40.546892\n40.893091\n41.441492\n41.5464\n40.651509\n41.002372\n40.292523\n40.206815\n39.469916\n39.470967\n39.081684\n39.188627\n40.838781\n40.814478\n41.23564\n40.573978\n40.429951\n40.761193\n40.714858\n40.899949\n40.951613\n40.448546\n40.730418\n40.324405\n41.260281\n41.00768\n41.350726\n41.351901\n41.828116\n41.527041\n42.026474\n41.964525\n42.596178\n42.908275\n42.978922\n'
BETA = 1.8286056394998358
Z = -1.0023831726745032
H_STAR = 10
MU_PNL = 366747.52222252387
SIGMA_PNL = 444862.37867309677
BEST_K_STOP = 0.25
BEST_K_TARGET = 4.0
BEST_CAPPED = 398760.23073435295
BEST_DELTA = 32012.708511829085
GAIN = 52275.08081373497
CONV_CAPPED = 346485.149920618
VERDETTO = "AI BORDI"
KAP = 1000000.0


def _rw(seed, n=60):
    rng = random.Random(seed)
    out = [0.0]
    for _ in range(1, n):
        out.append(out[-1] + rng.gauss(0.0, 1.0))
    return tuple(out)


class TestRegistry461:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 820
        assert "tab461" in dvars
        assert "tab461" in withs

    def test_titoli_allineati_451_452_453_454_455_456_457_458_459_460_461(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        attesi = {451: TITLE451, 452: TITLE452, 453: TITLE453,
                  454: TITLE454, 455: TITLE455, 456: TITLE456,
                  457: TITLE457, 458: TITLE458, 459: TITLE459,
                  460: TITLE460, 461: TITLE461}
        for n, att in attesi.items():
            assert titoli[dvars.index(f"tab{n}")] == att, f"tab{n}"
        assert len({titoli[dvars.index(f"tab{n}")] for n in attesi}) == 11


class TestOttimo461:
    def _pw(self):
        return _F["mh456_parse_serie"](DEMO_POWER)

    def _gs(self):
        return _F["mh456_parse_serie"](DEMO_GAS)

    def test_coerenza_demo(self):
        m = _F["mh461_mappa"](self._pw(), self._gs())
        assert m["n"] == 60 and m["H"] == 10 and m["T"] == 59
        assert abs(m["beta"] - BETA) < 1e-9
        assert abs(m["z"] - Z) < 1e-9
        assert m["h_star"] == H_STAR
        assert abs(m["mu_pnl"] - MU_PNL) < 1e-9
        assert abs(m["sigma_pnl"] - SIGMA_PNL) < 1e-9
        assert m["zero_motivo"] is None
        o = m["ottimo"]
        assert o is not None
        b = o["best"]
        assert abs(b["k_stop"] - BEST_K_STOP) < 1e-12
        assert abs(b["k_target"] - BEST_K_TARGET) < 1e-12
        assert abs(b["pnl_capped"] - BEST_CAPPED) < 1e-6
        assert abs(b["delta"] - BEST_DELTA) < 1e-6
        assert abs(o["conventional"]["pnl_capped"] - CONV_CAPPED) < 1e-6
        assert abs(o["gain"] - GAIN) < 1e-6
        assert abs(o["gain"] - (b["pnl_capped"]
                                - o["conventional"]["pnl_capped"])) < 1e-9
        assert m["verdetto"].startswith(VERDETTO)
        print(f"demo: best k=({b['k_stop']:.2f}, {b['k_target']:.2f}), "
              f"capped={b['pnl_capped']:,.0f}, gain={o['gain']:+,.0f} -> "
              f"{VERDETTO}")

    def test_coerenza_tab460(self):
        # ogni punto della griglia riusa mh460_piani (1e-12)
        o = _F["mh461_ottimo"](MU_PNL, SIGMA_PNL)
        b = o["best"]
        p = _F["mh460_piani"](MU_PNL, SIGMA_PNL,
                              b["k_stop"], b["k_target"])
        for k in ("stop", "target", "p_stop", "p_target",
                  "pnl_capped", "delta"):
            assert abs(b[k] - p[k]) < 1e-12, k
        # il best e' davvero l'argmax sulla griglia
        assert b["pnl_capped"] == max(r["pnl_capped"] for r in o["righe"])
        assert len(o["righe"]) == 21 * 21
        assert o["fattibili"] == 21 * 21

    def test_definizione_a_mano(self):
        # argmax indipendente: trapezi su E[min(max(Y,stop),target)]
        mu, sg = 366747.5, 444862.4
        ott = _F["mh461_ottimo"](mu, sg, ks_min=0.5, ks_max=2.0, n_ks=5,
                                 kt_min=1.0, kt_max=3.0, n_kt=5)
        best_i = (ott["best"]["i"], ott["best"]["j"])

        def capped_trap(ks_, kt_):
            st_ = -ks_ * sg
            tg_ = kt_ * sg
            n_ = 2001
            lo = mu - 6.0 * sg
            hi = mu + 6.0 * sg
            dx = (hi - lo) / n_
            acc = 0.0
            for i in range(n_ + 1):
                x = lo + i * dx
                d = (x - mu) / sg
                pdf = (math.exp(-0.5 * d * d) / math.sqrt(2.0 * math.pi)
                       / sg)
                y = min(max(x, st_), tg_)
                w = 0.5 if i in (0, n_) else 1.0
                acc += w * y * pdf
            return acc * dx

        mano = None
        for i, kss in enumerate(ott["ks"]):
            for j, ktt in enumerate(ott["kt"]):
                c = capped_trap(kss, ktt)
                if mano is None or c > mano[0]:
                    mano = (c, i, j)
        assert mano[1:] == best_i, (mano[1:], best_i)
        assert abs(mano[0] - ott["best"]["pnl_capped"]) < 2.0, mano[0]
        print("definizione a mano OK (argmax trapezi = argmax forma chiusa)")

    def test_monotonia_vincolo(self):
        # vincolo piu' stretto -> capped ottimo non crescente
        c_lib = _F["mh461_ottimo"](MU_PNL, SIGMA_PNL
                                   )["best"]["pnl_capped"]
        c_30 = _F["mh461_ottimo"](MU_PNL, SIGMA_PNL, p_stop_max=0.30
                                  )["best"]["pnl_capped"]
        c_10 = _F["mh461_ottimo"](MU_PNL, SIGMA_PNL, p_stop_max=0.10
                                  )["best"]["pnl_capped"]
        assert c_lib >= c_30 >= c_10
        o30 = _F["mh461_ottimo"](MU_PNL, SIGMA_PNL, p_stop_max=0.30)
        assert all(r["p_stop"] <= 0.30 + 1e-12 for r in o30["righe"])
        # vincolo impossibile -> ValueError onesto
        with pytest.raises(ValueError):
            _F["mh461_ottimo"](MU_PNL, SIGMA_PNL, p_stop_max=1e-9)

    def test_verdetti(self):
        v = _F["mh461_verdetto"]
        b = {"k_stop": 1.0, "k_target": 2.0}
        assert v(b, 0.0, False, 100.0,
                 zero_motivo="NESSUN SEGNALE").startswith("NESSUN TRADE")
        assert v(b, 5000.0, True, 100000.0).startswith("AI BORDI")
        assert v(b, 5000.0, False, 100000.0).startswith("OTTIMO TROVATO")
        assert v(b, 500.0, False, 100000.0).startswith("CONVENZIONALI OK")
        # soglia inclusiva: gain == 1% -> CONVENZIONALI OK
        assert v(b, 1000.0, False, 100000.0).startswith("CONVENZIONALI OK")
        assert v(b, 1000.01, False, 100000.0).startswith("OTTIMO TROVATO")
        # precedenza: AI BORDI prima di OTTIMO
        assert v(b, 50000.0, True, 100000.0).startswith("AI BORDI")

    def test_asse(self):
        a = _F["mh461_asse"](0.25, 3.0, 21, "k_stop")
        assert len(a) == 21
        assert abs(a[0] - 0.25) < 1e-12 and abs(a[-1] - 3.0) < 1e-12
        assert abs(a[10] - 1.625) < 1e-12
        assert a == tuple(sorted(a))
        assert _F["mh461_asse"](1.0, 2.0, 2, "k") == (1.0, 2.0)

    def test_nessun_trade(self):
        pw, gs = self._pw(), self._gs()
        m = _F["mh461_mappa"](pw, gs, z_entry=5.0)
        assert m["verdetto"].startswith("NESSUN TRADE")
        assert m["ottimo"] is None
        m2 = _F["mh461_mappa"](pw, gs, costo=10.0)
        assert m2["verdetto"].startswith("NESSUN TRADE")
        assert m2["ottimo"] is None

    def test_rw_rilevati(self):
        with pytest.raises(ValueError):
            _F["mh461_mappa"](_rw(20261014), _rw(777))

    def test_degeneri(self):
        pw, gs = self._pw(), self._gs()
        for bad in (lambda: _F["mh461_ottimo"](1.0, 0.0),
                    lambda: _F["mh461_ottimo"](1.0, -2.0),
                    lambda: _F["mh461_ottimo"](float("nan"), 1.0, 1.0, 2.0),
                    lambda: _F["mh461_ottimo"](1.0, 1.0, ks_min=0.0),
                    lambda: _F["mh461_ottimo"](1.0, 1.0, ks_min=-0.5),
                    lambda: _F["mh461_ottimo"](1.0, 1.0, ks_min=3.0,
                                              ks_max=1.0),
                    lambda: _F["mh461_ottimo"](1.0, 1.0, ks_min=1.0,
                                              ks_max=1.0),
                    lambda: _F["mh461_ottimo"](1.0, 1.0, n_ks=1),
                    lambda: _F["mh461_ottimo"](1.0, 1.0, n_ks=True),
                    lambda: _F["mh461_ottimo"](1.0, 1.0, n_ks="21"),
                    lambda: _F["mh461_ottimo"](1.0, 1.0, n_kt=0),
                    lambda: _F["mh461_ottimo"](1.0, 1.0, kt_min="0.5"),
                    lambda: _F["mh461_ottimo"](1.0, 1.0, ks_min=True),
                    lambda: _F["mh461_ottimo"](1.0, 1.0, p_stop_max=0.0),
                    lambda: _F["mh461_ottimo"](1.0, 1.0, p_stop_max=1.0),
                    lambda: _F["mh461_ottimo"](1.0, 1.0, p_stop_max=1.2),
                    lambda: _F["mh461_ottimo"](1.0, 1.0, p_stop_max=-0.1),
                    lambda: _F["mh461_ottimo"](1.0, 1.0, p_stop_max="0.15"),
                    lambda: _F["mh461_ottimo"](1.0, 1.0,
                                              p_stop_max=float("nan")),
                    lambda: _F["mh461_verdetto"]("x", 1.0, False, 1.0),
                    lambda: _F["mh461_verdetto"]({"k_stop": 1.0}, 1.0,
                                                False, 1.0),
                    lambda: _F["mh461_verdetto"]({"k_stop": 1.0,
                                                 "k_target": 2.0},
                                                "x", False, 1.0),
                    lambda: _F["mh461_verdetto"]({"k_stop": 1.0,
                                                 "k_target": 2.0},
                                                1.0, False,
                                                float("nan")),
                    lambda: _F["mh461_asse"](0.0, 1.0, 5, "k"),
                    lambda: _F["mh461_asse"](-1.0, 1.0, 5, "k"),
                    lambda: _F["mh461_asse"](2.0, 1.0, 5, "k"),
                    lambda: _F["mh461_asse"](1.0, 1.0, 5, "k"),
                    lambda: _F["mh461_asse"](0.5, 1.0, 1, "k"),
                    lambda: _F["mh461_asse"](0.5, 1.0, True, "k"),
                    lambda: _F["mh461_asse"]("0.5", 1.0, 5, "k"),
                    lambda: _F["mh461_num"](float("nan"), "x"),
                    lambda: _F["mh461_num"](True, "x"),
                    lambda: _F["mh461_num"]("1.5", "x"),
                    lambda: _F["mh461_mappa"](pw, gs, ks_min=0.0),
                    lambda: _F["mh461_mappa"](pw, gs, ks_max=0.1),
                    lambda: _F["mh461_mappa"](pw, gs, n_ks=1),
                    lambda: _F["mh461_mappa"](pw, gs, vincola_pstop="si"),
                    lambda: _F["mh461_mappa"](pw, gs, p_stop_max=0.0),
                    lambda: _F["mh461_mappa"](pw, gs, p_stop_max=1.5),
                    lambda: _F["mh461_mappa"](pw, gs, f_max=2.0),
                    lambda: _F["mh461_mappa"]((1.0,) * 29, (1.0,) * 29),
                    lambda: _F["mh461_mappa"](None, gs),
                    lambda: _F["mh461_mappa"](pw, gs[:50])):
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
