"""Test tab463 '🔀 Scale-out: tutto insieme o a pezzi?': registry + funzioni pure."""

import math
import random
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh463_num", "mh463_sched", "mh463_tranche", "mh463_atteso",
           "mh463_verdetto", "mh463_mappa",
           "mh462_num", "mh462_asse", "mh462_scala", "mh462_piani",
           "mh462_tempo", "mh462_verdetto", "mh462_mappa",
           "mh461_num", "mh461_asse", "mh461_ottimo", "mh461_verdetto",
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

TITLE463 = "🔀 Scale-out: tutto insieme o a pezzi?"
TITLE462 = "⏳ Time stop: uscire se non succede niente"
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
TITLE455 = "🔮 Quando rientra lo spread? Forecast mean-reversion"
TITLE454 = "⚖️ Lo spread è stazionario? Test ADF"
TITLE453 = "📊 Backtest VECM(1): il modello batte il random walk?"
TITLE452 = "📈 Previsione VECM(1): dove vanno power e gas nei prossimi H giorni?"
DEMO_POWER = '115.0\n114.222584\n115.526527\n115.270435\n115.404795\n113.275972\n114.840219\n116.685764\n115.420859\n113.571058\n112.06301\n112.194403\n116.139654\n117.765956\n116.742831\n116.62762\n115.739526\n117.414453\n114.867579\n116.640701\n115.779325\n115.137451\n116.642853\n117.253244\n117.493738\n117.242796\n118.334843\n119.091227\n116.768615\n115.421416\n116.033447\n114.144567\n113.700317\n114.354433\n114.876507\n113.755332\n115.568524\n116.069102\n116.138549\n117.333173\n117.084818\n116.63492\n117.999467\n117.718767\n117.668152\n118.796536\n116.597527\n114.618757\n114.130273\n116.852609\n116.128887\n119.874946\n118.472635\n119.958398\n119.950907\n122.309881\n121.085938\n120.106701\n119.684133\n119.645704\n'
DEMO_GAS = '40.0\n39.387964\n39.576758\n40.074258\n39.817653\n39.153163\n39.120398\n39.359404\n39.908497\n39.300559\n38.654127\n39.007091\n39.244134\n40.011027\n40.502256\n40.451366\n40.314247\n41.599511\n41.45511\n41.062643\n40.493471\n40.541201\n40.613858\n40.441425\n40.410346\n40.546892\n40.893091\n41.441492\n41.5464\n40.651509\n41.002372\n40.292523\n40.206815\n39.469916\n39.470967\n39.081684\n39.188627\n40.838781\n40.814478\n41.23564\n40.573978\n40.429951\n40.761193\n40.714858\n40.899949\n40.951613\n40.448546\n40.730418\n40.324405\n41.260281\n41.00768\n41.350726\n41.351901\n41.828116\n41.527041\n42.026474\n41.964525\n42.596178\n42.908275\n42.978922\n'
BETA = 1.8286056394998358
Z = -1.0023831726745032
H_STAR = 10
MU_PNL = 366747.52222252387
SIGMA_PNL = 444862.37867309677
TAU_STAR = 10.0
SCHED_BEST = "one-shot"
SCHED_NET = 398760.23073435295
SCHED_GAIN = 0.0
SCHED_TEMPO = 10.0
ONESHOT_NET = 398760.23073435295
BEST_K_STOP = 0.25
BEST_K_TARGET = 4.0
VERDETTO = "TUTTO INSIEME"
KAP = 1000000.0
SCHEDS = ("one-shot", "3-pari", "5-pari",
          "front-50-50", "back-25-75", "10-graduale")


def _rw(seed, n=60):
    rng = random.Random(seed)
    out = [0.0]
    for _ in range(1, n):
        out.append(out[-1] + rng.gauss(0.0, 1.0))
    return tuple(out)


class TestRegistry463:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 816
        assert "tab463" in dvars
        assert "tab463" in withs

    def test_titoli_allineati_452_453_454_455_456_457_458_459_460_461_462_463(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        attesi = {452: TITLE452, 453: TITLE453, 454: TITLE454,
                  455: TITLE455, 456: TITLE456, 457: TITLE457,
                  458: TITLE458, 459: TITLE459, 460: TITLE460,
                  461: TITLE461, 462: TITLE462, 463: TITLE463}
        for n, att in attesi.items():
            assert titoli[dvars.index(f"tab{n}")] == att, f"tab{n}"
        assert len({titoli[dvars.index(f"tab{n}")] for n in attesi}) == 12


class TestScaleOut463:
    def _pw(self):
        return _F["mh456_parse_serie"](DEMO_POWER)

    def _gs(self):
        return _F["mh456_parse_serie"](DEMO_GAS)

    def _mappa(self):
        return _F["mh463_mappa"](self._pw(), self._gs(),
                                tau_min=1.0, tau_max=10.0, n_tau=10,
                                costo_tempo=0.0)

    def _b461(self):
        return _F["mh461_ottimo"](MU_PNL, SIGMA_PNL)["best"]

    def test_coerenza_demo(self):
        m = self._mappa()
        assert m["n"] == 60 and m["H"] == 10 and m["T"] == 59
        assert abs(m["beta"] - BETA) < 1e-9
        assert abs(m["z"] - Z) < 1e-9
        assert m["h_star"] == H_STAR
        assert abs(m["mu_pnl"] - MU_PNL) < 1e-9
        assert abs(m["sigma_pnl"] - SIGMA_PNL) < 1e-9
        assert m["zero_motivo"] is None
        assert m["scheds"] == SCHEDS
        s = m["scala"]
        assert s is not None
        assert abs(s["tau_star"] - TAU_STAR) < 1e-12
        assert len(s["righe"]) == 6
        assert [r["sched"] for r in s["righe"]] == list(SCHEDS)
        b = s["best"]
        assert b["sched"] == SCHED_BEST
        assert abs(b["netto"] - SCHED_NET) < 1e-6
        assert abs(b["tempo_medio"] - SCHED_TEMPO) < 1e-9
        assert abs(s["gain"] - SCHED_GAIN) < 1e-6
        assert abs(s["gain"] - (b["netto"]
                                - s["one_shot"]["netto"])) < 1e-9
        assert abs(s["one_shot"]["netto"] - ONESHOT_NET) < 1e-6
        assert abs(s["one_shot"]["tempo_medio"] - TAU_STAR) < 1e-9
        assert m["verdetto"].startswith(VERDETTO)
        print(f"demo: tau*={s['tau_star']:.1f} g, best='{b['sched']}' "
              f"netto={b['netto']:,.0f}, gain={s['gain']:+,.0f} "
              f"vs one-shot -> {VERDETTO}")

    def test_coerenza_tab462(self):
        # one-shot = best netto del time-stop di tab462 (1e-9); i k ottimi
        # di tab461 sono riusati (1e-12)
        m = self._mappa()
        b461 = self._b461()
        assert abs(b461["k_stop"] - BEST_K_STOP) < 1e-12
        assert abs(b461["k_target"] - BEST_K_TARGET) < 1e-12
        t = _F["mh462_tempo"](MU_PNL, SIGMA_PNL, H_STAR,
                              b461["stop"], b461["target"],
                              tau_min=1.0, tau_max=10.0, n_tau=10,
                              costo_tempo=0.0)
        assert abs(t["best"]["tau"] - TAU_STAR) < 1e-12
        assert abs(m["scala"]["one_shot"]["netto"]
                   - t["best"]["net"]) < 1e-9
        # una tranche singola (1.0, tau) coincide con mh463_tranche
        tr = _F["mh463_tranche"](MU_PNL, SIGMA_PNL, H_STAR, 4.0,
                                 b461["stop"], b461["target"],
                                 costo_tempo=0.0)
        a = _F["mh463_atteso"]([(1.0, 4.0)], MU_PNL, SIGMA_PNL, H_STAR,
                               b461["stop"], b461["target"],
                               costo_tempo=0.0)
        assert abs(a["netto"] - tr["net"]) < 1e-12
        assert abs(a["tempo_medio"] - 4.0) < 1e-12
        assert a["n_tranche"] == 1

    def test_definizione_a_mano(self):
        # capped della prima tranche di "3-pari" via trapezi indipendenti
        b461 = self._b461()
        f0, tau0 = _F["mh463_sched"]("3-pari", 10.0)[0]
        assert abs(f0 - 1.0 / 3.0) < 1e-12
        mut = MU_PNL * tau0 / 10.0
        sgt = SIGMA_PNL * math.sqrt(tau0 / 10.0)
        n_ = 2001
        lo = mut - 6.0 * sgt
        hi = mut + 6.0 * sgt
        dx = (hi - lo) / n_
        acc = 0.0
        for i in range(n_ + 1):
            x = lo + i * dx
            d = (x - mut) / sgt
            pdf = (math.exp(-0.5 * d * d) / math.sqrt(2.0 * math.pi)
                   / sgt)
            y = min(max(x, b461["stop"]), b461["target"])
            w = 0.5 if i in (0, n_) else 1.0
            acc += w * y * pdf
        tr = _F["mh463_tranche"](MU_PNL, SIGMA_PNL, H_STAR, tau0,
                                 b461["stop"], b461["target"],
                                 costo_tempo=0.0)
        assert abs(acc * dx - tr["pnl_capped"]) < 0.5, acc * dx
        print("definizione a mano OK (trapezi prima tranche 3-pari)")

    def test_sched(self):
        sc = _F["mh463_sched"]
        ts = 10.0
        one = sc("one-shot", ts)
        assert one == ((1.0, 10.0),)
        t3 = sc("3-pari", ts)
        assert len(t3) == 3
        assert [t for _, t in t3] == [ts / 3.0, 2.0 * ts / 3.0, ts]
        t5 = sc("5-pari", ts)
        assert len(t5) == 5 and t5[-1] == (0.2, ts)
        t10 = sc("10-graduale", ts)
        assert len(t10) == 10 and t10[-1] == (0.1, ts)
        assert sc("front-50-50", ts) == ((0.5, 5.0), (0.5, 10.0))
        assert sc("back-25-75", ts) == ((0.25, 5.0), (0.75, 10.0))
        for nome in SCHEDS:
            tr = sc(nome, ts)
            assert abs(sum(f for f, _ in tr) - 1.0) < 1e-12, nome
            taus = [t for _, t in tr]
            assert all(0.0 < t <= ts for t in taus), nome
            assert taus == sorted(taus), nome
        for bad in (lambda: sc("sconosciuto", ts),
                    lambda: sc("one-shot", 0.0),
                    lambda: sc("one-shot", -2.0),
                    lambda: sc("one-shot", float("nan")),
                    lambda: sc(123, ts),
                    lambda: sc(None, ts)):
            with pytest.raises(ValueError):
                bad()

    def test_tempo_medio(self):
        # tempo_medio = somma f_i*tau_i: valori esatti per costruzione
        a3 = _F["mh463_atteso"](_F["mh463_sched"]("3-pari", 9.0),
                                MU_PNL, SIGMA_PNL, H_STAR,
                                *self._st_tg(), costo_tempo=0.0)
        assert abs(a3["tempo_medio"] - 6.0) < 1e-9
        a1 = _F["mh463_atteso"](_F["mh463_sched"]("one-shot", 9.0),
                                MU_PNL, SIGMA_PNL, H_STAR,
                                *self._st_tg(), costo_tempo=0.0)
        assert abs(a1["tempo_medio"] - 9.0) < 1e-12
        af = _F["mh463_atteso"](_F["mh463_sched"]("front-50-50", 8.0),
                                MU_PNL, SIGMA_PNL, H_STAR,
                                *self._st_tg(), costo_tempo=0.0)
        assert abs(af["tempo_medio"] - 6.0) < 1e-9

    def _st_tg(self):
        b461 = self._b461()
        return (b461["stop"], b461["target"])

    def test_monotonia_costo(self):
        # a tau_star fissato, piu' funding -> il miglior schedule ha
        # tempo_medio non crescente (Topkis su insieme discreto)
        st_, tg_ = self._st_tg()

        def best_tm(ct):
            bn, bt = None, None
            for nm in SCHEDS:
                a = _F["mh463_atteso"](
                    _F["mh463_sched"](nm, 10.0), MU_PNL, SIGMA_PNL,
                    H_STAR, st_, tg_, costo_tempo=ct)
                if bn is None or a["netto"] > bn:
                    bn, bt = a["netto"], a["tempo_medio"]
            return bt

        tm0 = best_tm(0.0)
        tm1 = best_tm(5000.0)
        assert tm1 <= tm0, (tm1, tm0)
        print(f"monotonia costo OK: tempo_medio(0)={tm0:.1f} >= "
              f"tempo_medio(5000)={tm1:.1f}")

    def test_verdetti(self):
        v = _F["mh463_verdetto"]
        assert v({"sched": "3-pari"}, 0.0, 100000.0,
                 zero_motivo="NESSUN SEGNALE").startswith("NESSUN TRADE")
        assert v({"sched": "3-pari"}, 5000.0,
                 100000.0).startswith("A PEZZI CONVIENE")
        assert v({"sched": "one-shot"}, 0.0,
                 100000.0).startswith("TUTTO INSIEME")
        assert v({"sched": "5-pari"}, 500.0,
                 100000.0).startswith("TUTTO INSIEME")
        # soglia inclusiva: gain == 1% -> TUTTO INSIEME
        assert v({"sched": "3-pari"}, 1000.0,
                 100000.0).startswith("TUTTO INSIEME")
        assert v({"sched": "3-pari"}, 1000.01,
                 100000.0).startswith("A PEZZI CONVIENE")

    def test_nessun_trade(self):
        pw, gs = self._pw(), self._gs()
        m = _F["mh463_mappa"](pw, gs, z_entry=5.0)
        assert m["verdetto"].startswith("NESSUN TRADE")
        assert m["scala"] is None
        m2 = _F["mh463_mappa"](pw, gs, costo=10.0)
        assert m2["verdetto"].startswith("NESSUN TRADE")
        assert m2["scala"] is None

    def test_rw_rilevati(self):
        with pytest.raises(ValueError):
            _F["mh463_mappa"](_rw(20261015), _rw(777))

    def test_degeneri(self):
        pw, gs = self._pw(), self._gs()
        st_, tg_ = self._st_tg()
        for bad in (lambda: _F["mh463_sched"]("sconosciuto", 10.0),
                    lambda: _F["mh463_sched"]("one-shot", 0.0),
                    lambda: _F["mh463_sched"](123, 10.0),
                    lambda: _F["mh463_tranche"](1.0, 0.0, 10.0, 5.0,
                                                -1.0, 2.0),
                    lambda: _F["mh463_tranche"](1.0, 1.0, 10.0, 0.0,
                                                -1.0, 2.0),
                    lambda: _F["mh463_tranche"](1.0, 1.0, 10.0, 11.0,
                                                -1.0, 2.0),
                    lambda: _F["mh463_tranche"](1.0, 1.0, 10.0, 5.0,
                                                1.0, 2.0),
                    lambda: _F["mh463_tranche"](1.0, 1.0, 10.0, 5.0,
                                                -1.0, -2.0),
                    lambda: _F["mh463_tranche"](1.0, 1.0, 10.0, 5.0,
                                                -1.0, 2.0, costo_tempo=-1.0),
                    lambda: _F["mh463_tranche"](1.0, 1.0, 0.0, 5.0,
                                                -1.0, 2.0),
                    lambda: _F["mh463_atteso"]([], 1.0, 1.0, 10.0,
                                               -1.0, 2.0),
                    lambda: _F["mh463_atteso"]([(0.5, 5.0)], 1.0, 1.0,
                                               10.0, -1.0, 2.0),
                    lambda: _F["mh463_atteso"]([(0.6, 5.0), (0.6, 8.0)],
                                               1.0, 1.0, 10.0, -1.0, 2.0),
                    lambda: _F["mh463_atteso"]([(0.0, 5.0), (1.0, 8.0)],
                                               1.0, 1.0, 10.0, -1.0, 2.0),
                    lambda: _F["mh463_atteso"]([(1.5, 5.0)], 1.0, 1.0,
                                               10.0, -1.0, 2.0),
                    lambda: _F["mh463_atteso"]([(1.0, 11.0)], 1.0, 1.0,
                                               10.0, -1.0, 2.0),
                    lambda: _F["mh463_atteso"](["x"], 1.0, 1.0,
                                               10.0, -1.0, 2.0),
                    lambda: _F["mh463_atteso"]("one-shot", 1.0, 1.0,
                                               10.0, -1.0, 2.0),
                    lambda: _F["mh463_atteso"]([(1.0, 5.0)], 1.0, 0.0,
                                               10.0, -1.0, 2.0),
                    lambda: _F["mh463_verdetto"]("x", 1.0, 1.0),
                    lambda: _F["mh463_verdetto"]({"k": 1.0}, 1.0, 1.0),
                    lambda: _F["mh463_verdetto"]({"sched": "3-pari"}, "x",
                                               1.0),
                    lambda: _F["mh463_verdetto"]({"sched": "3-pari"}, 1.0,
                                               float("nan")),
                    lambda: _F["mh463_num"](float("nan"), "x"),
                    lambda: _F["mh463_num"](True, "x"),
                    lambda: _F["mh463_num"]("1.5", "x"),
                    lambda: _F["mh463_mappa"](pw, gs, scheds=()),
                    lambda: _F["mh463_mappa"](pw, gs,
                                              scheds=("3-pari",)),
                    lambda: _F["mh463_mappa"](pw, gs,
                                              scheds=("one-shot",
                                                      "one-shot")),
                    lambda: _F["mh463_mappa"](pw, gs,
                                              scheds=("sconosciuto",
                                                      "one-shot")),
                    lambda: _F["mh463_mappa"](pw, gs, scheds="one-shot"),
                    lambda: _F["mh463_mappa"](pw, gs[:50])):
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
