"""Test tab464 '🧺 Portafoglio: quanti trade insieme?': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh464_num", "mh464_serie", "mh464_coppia", "mh464_alloc",
           "mh464_verdetto", "mh464_mappa",
           "mh463_num", "mh463_sched", "mh463_tranche", "mh463_atteso",
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

TITLE464 = "🧺 Portafoglio: quanti trade insieme?"
TITLE463 = "🔀 Scale-out: tutto insieme o a pezzi?"
TITLE462 = "⏳ Time stop: uscire se non succede niente"
TITLE461 = "🧭 Ottimizza stop/target: i migliori k"
TITLE460 = "🛑 Stop & target: dove chiudere il trade"
TITLE477 = "⏳ Scheduling di esecuzione"
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
TITLE455 = "🔮 Quando rientra lo spread? Forecast mean-reversion"
TITLE454 = "⚖️ Lo spread è stazionario? Test ADF"
TITLE453 = "📊 Backtest VECM(1): il modello batte il random walk?"
COPPIE = (("A", 31, 555), ("B", 345, 7), ("C", 360, 777))
BETA_A = 1.595385304059687
Z_A = -1.088207736928303
H_STAR_A = 10
MU_PNL_A = 294391.7367220217
SIGMA_PNL_A = 422751.51796652994
F_APP_A = 0.25
SCHED_A = "one-shot"
MU_A = 333307.16100542794
BETA_B = 1.5027432202914142
Z_B = 1.144633039215061
H_STAR_B = 10
MU_PNL_B = 312164.2080941347
SIGMA_PNL_B = 428304.84271582006
F_APP_B = 0.25
SCHED_B = "one-shot"
MU_B = 349249.3216071483
BETA_C = 1.382638618226789
Z_C = -1.1355565691468332
H_STAR_C = 10
MU_PNL_C = 353678.6002328501
SIGMA_PNL_C = 440963.0343583507
F_APP_C = 0.25
SCHED_C = "one-shot"
MU_C = 386835.2688279841
KAP = 1000000.0
RBB = 0.05
FMAX = 0.25
G_A = 0.01625783828009099
G_B = 0.016596561042656926
G_C = 0.01734243999195105
EDGE_TOT = 71695.43617120649
RB_USATO = 0.05
SHARPE = 1.4339087234241297
VERDETTO = "DIVERSIFICATO"
N_CAP = 0

_DEMO = None


def _demo():
    global _DEMO
    if _DEMO is None:
        _DEMO = _F["mh464_mappa"](COPPIE, K=KAP, rb=RBB, f_max=FMAX,
                                  z_entry=1.0, costo=0.20, H=10)
    return _DEMO


class TestRegistry464:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 477
        assert "tab464" in dvars
        assert "tab464" in withs

    def test_titoli_allineati_453_454_455_456_457_458_459_460_461_462_463_464(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        attesi = {453: TITLE453, 454: TITLE454, 455: TITLE455,
                  456: TITLE456, 457: TITLE457, 458: TITLE458,
                  459: TITLE459, 460: TITLE460, 461: TITLE461,
                  462: TITLE462, 463: TITLE463, 464: TITLE464}
        for n, att in attesi.items():
            assert titoli[dvars.index(f"tab{n}")] == att, f"tab{n}"
        assert len({titoli[dvars.index(f"tab{n}")] for n in attesi}) == 12


class TestPortafoglio464:
    def _coppie_attese(self):
        return {"A": (BETA_A, Z_A, H_STAR_A, MU_PNL_A, SIGMA_PNL_A,
                      F_APP_A, SCHED_A, MU_A),
                "B": (BETA_B, Z_B, H_STAR_B, MU_PNL_B, SIGMA_PNL_B,
                      F_APP_B, SCHED_B, MU_B),
                "C": (BETA_C, Z_C, H_STAR_C, MU_PNL_C, SIGMA_PNL_C,
                      F_APP_C, SCHED_C, MU_C)}

    def test_coerenza_demo(self):
        m = _demo()
        assert m["eligibili"] == ["A", "B", "C"]
        assert len(m["coppie"]) == 3
        att = self._coppie_attese()
        for c in m["coppie"]:
            be, z, hs, mup, sgp, fa, sc, mu = att[c["nome"]]
            assert c["eligibile"] is True, c["nome"]
            assert c["motivo"] is None
            assert abs(c["beta"] - be) < 1e-9
            assert abs(c["z"] - z) < 1e-9
            assert c["h_star"] == hs
            assert abs(c["mu_pnl"] - mup) < 1e-9
            assert abs(c["sigma_pnl"] - sgp) < 1e-9
            assert abs(c["f_app"] - fa) < 1e-12
            assert c["sched_best"] == sc
            assert abs(c["mu"] - mu) < 1e-6
            assert abs(c["netto_best"] - mu) < 1e-9
        a = m["alloc"]
        assert a is not None
        assert a["n_capped"] == N_CAP
        gs = {"A": G_A, "B": G_B, "C": G_C}
        for r in a["righe"]:
            assert abs(r["g"] - gs[r["nome"]]) < 1e-12, r["nome"]
            assert r["capped"] is False
            assert abs(r["eur"] - r["g"] * KAP) < 1e-6
            assert abs(r["edge"] - r["g"] * r["rho"] * KAP) < 1e-6
            assert abs(r["risk"] - r["g"] * r["s"] * KAP) < 1e-6
        assert abs(a["edge_tot"] - EDGE_TOT) < 1e-6
        assert abs(a["var_tot"] - (RBB * KAP) ** 2) < 1e-3
        assert abs(a["rb_usato"] - RB_USATO) < 1e-12
        assert abs(a["sharpe"] - SHARPE) < 1e-9
        assert m["verdetto"].startswith(VERDETTO)
        print(f"demo: 3 coppie eligibili, g={[round(r['g'], 4) for r in a['righe']]} "
              f"edge={a['edge_tot']:,.0f} rb_usato={a['rb_usato']:.2%} "
              f"-> {VERDETTO}")

    def test_coerenza_tab463(self):
        # mu di coppia = netto del miglior schedule tab463 (1e-9);
        # mu_pnl/sigma_pnl/f_app riusati dalla pipeline (1e-9/1e-12)
        att = self._coppie_attese()
        for nm, sg, ss in COPPIE:
            pw, gs = _F["mh464_serie"](sg, ss)
            t = _F["mh463_mappa"](pw, gs, z_entry=1.0, costo=0.20, H=10,
                                  capitale=KAP, f_max=FMAX,
                                  ks_min=0.25, ks_max=3.0, n_ks=21,
                                  kt_min=0.5, kt_max=4.0, n_kt=21,
                                  vincola_pstop=False, p_stop_max=0.15,
                                  tau_min=1.0, tau_max=10.0, n_tau=10,
                                  costo_tempo=0.0)
            be, z, hs, mup, sgp, fa, sc, mu = att[nm]
            assert abs(t["mu_pnl"] - mup) < 1e-9, nm
            assert abs(t["sigma_pnl"] - sgp) < 1e-9, nm
            assert abs(t["f_app"] - fa) < 1e-12, nm
            assert t["scala"]["best"]["sched"] == sc, nm
            assert abs(t["scala"]["best"]["netto"] - mu) < 1e-9, nm

    def test_definizione_a_mano(self):
        # soluzione chiusa su A,B: g_i = rb·a_i/S', a_i = mu·f_app·K/sg²,
        # S' = sqrt(Σ(mu/sg)²) — ricalcolata a mano (1e-12)
        mus = [MU_A, MU_B]
        sgs = [SIGMA_PNL_A, SIGMA_PNL_B]
        fas = [F_APP_A, F_APP_B]
        aA = mus[0] * fas[0] * KAP / sgs[0] ** 2
        aB = mus[1] * fas[1] * KAP / sgs[1] ** 2
        Sp = math.sqrt((mus[0] / sgs[0]) ** 2 + (mus[1] / sgs[1]) ** 2)
        gA_exp = RBB * aA / Sp
        gB_exp = RBB * aB / Sp
        a = _F["mh464_alloc"](mus, sgs, fas, KAP, RBB, FMAX)
        assert abs(a["righe"][0]["g"] - gA_exp) < 1e-12
        assert abs(a["righe"][1]["g"] - gB_exp) < 1e-12
        assert a["n_capped"] == 0
        # varianza = budget² per costruzione (1e-6 relativo)
        assert abs(a["var_tot"] / (RBB * KAP) ** 2 - 1.0) < 1e-9
        print("definizione a mano OK (chiusa A,B, 1e-12)")

    def test_monotonia_rb(self):
        # senza cap vincolanti l'allocazione scala linearmente col budget:
        # raddoppiare rb raddoppia edge e g (Topkis discreto -> lineare)
        a2 = _F["mh464_alloc"]([MU_A, MU_B, MU_C],
                               [SIGMA_PNL_A, SIGMA_PNL_B, SIGMA_PNL_C],
                               [F_APP_A, F_APP_B, F_APP_C],
                               KAP, 2.0 * RBB, FMAX)
        assert a2["n_capped"] == 0
        assert abs(a2["edge_tot"] / EDGE_TOT - 2.0) < 1e-9
        g_att = [G_A, G_B, G_C]
        for r, g0 in zip(a2["righe"], g_att):
            assert abs(r["g"] / g0 - 2.0) < 1e-9
        print("monotonia rb OK: edge(2·rb) = 2·edge(rb)")

    def test_cap_vincolante(self):
        # trade 1 dominante -> cappato a f_max, trade 2 riottimizzato
        # sul budget residuo (water-filling): valori chiusi a mano
        a = _F["mh464_alloc"]([1e6, 1e5], [1e5, 1e5], [0.25, 0.25],
                               1e6, 0.05, 0.10)
        r1, r2 = a["righe"]
        assert r1["g"] == 0.10 and r1["capped"] is True
        assert abs(r2["g"] - 0.075) < 1e-12 and r2["capped"] is False
        assert a["n_capped"] == 1
        assert abs(a["var_tot"] - (0.05 * 1e6) ** 2) < 1e-3
        assert abs(a["edge_tot"] - 430000.0) < 1e-6
        v = _F["mh464_verdetto"](a, ["X", "Y"])
        assert "Cap f_max vincolante su: X" in v
        print("cap vincolante OK (water-filling, 1e-12)")

    def test_verdetti(self):
        v = _F["mh464_verdetto"]
        assert v(None, []).startswith("NESSUN TRADE")
        # concentrato: un trade con il 99.8% del capitale impiegato
        ac = _F["mh464_alloc"]([1e6, 1e3, 1e3], [1e5, 1e5, 1e5],
                               [0.25, 0.25, 0.25], 1e6, 0.05, 0.25)
        for r, nm in zip(ac["righe"], ["X", "Y", "Z"]):
            r["nome"] = nm
        vc = v(ac, ["X", "Y", "Z"])
        assert vc.startswith("CONCENTRATO"), vc
        assert "'X'" in vc
        # soglia inclusiva: 50% esatto -> DIVERSIFICATO
        ae = _F["mh464_alloc"]([1e6, 1e6], [1e5, 1e5], [0.25, 0.25],
                               1e6, 0.05, 0.25)
        for r, nm in zip(ae["righe"], ["P", "Q"]):
            r["nome"] = nm
        ve = v(ae, ["P", "Q"])
        assert ve.startswith("DIVERSIFICATO"), ve
        # demo reale -> DIVERSIFICATO
        assert _demo()["verdetto"].startswith("DIVERSIFICATO")

    def test_nessun_trade(self):
        # seed senza segnale (z=0.58 / z=-0.82): coppie non eligibili
        m = _F["mh464_mappa"]([("N1", 136, 5555), ("N2", 91, 7777)],
                              K=KAP, rb=RBB, f_max=FMAX)
        assert m["eligibili"] == []
        assert m["alloc"] is None
        assert m["verdetto"].startswith("NESSUN TRADE")
        for c in m["coppie"]:
            assert c["eligibile"] is False

    def test_serie_deterministica(self):
        p1, g1 = _F["mh464_serie"](31, 555)
        p2, g2 = _F["mh464_serie"](31, 555)
        assert p1 == p2 and g1 == g2
        p3, g3 = _F["mh464_serie"](31, 556)
        assert p3 != p1
        assert len(p1) == 60 and len(g1) == 60
        assert abs(g1[0] - 40.0) < 1e-12
        for bad in (lambda: _F["mh464_serie"](-1, 555),
                    lambda: _F["mh464_serie"](31.5, 555),
                    lambda: _F["mh464_serie"](True, 555),
                    lambda: _F["mh464_serie"](31, 555, n=29),
                    lambda: _F["mh464_serie"](31, 555, n="60")):
            with pytest.raises(ValueError):
                bad()

    def test_degeneri(self):
        pw, gs = _F["mh464_serie"](31, 555)
        for bad in (lambda: _F["mh464_num"](float("nan"), "x"),
                    lambda: _F["mh464_num"](True, "x"),
                    lambda: _F["mh464_num"]("1.5", "x"),
                    lambda: _F["mh464_coppia"]("", 31, 555),
                    lambda: _F["mh464_coppia"]("A", -1, 555),
                    lambda: _F["mh464_coppia"]("A", 31, 555, K=0.0),
                    lambda: _F["mh464_alloc"]([], [], [], 1e6, 0.05, 0.25),
                    lambda: _F["mh464_alloc"]([1.0], [1.0, 2.0], [0.25],
                                              1e6, 0.05, 0.25),
                    lambda: _F["mh464_alloc"]([1.0], [1.0], [0.25],
                                              0.0, 0.05, 0.25),
                    lambda: _F["mh464_alloc"]([1.0], [1.0], [0.25],
                                              1e6, 0.0, 0.25),
                    lambda: _F["mh464_alloc"]([1.0], [1.0], [0.25],
                                              1e6, 1.5, 0.25),
                    lambda: _F["mh464_alloc"]([1.0], [1.0], [0.25],
                                              1e6, 0.05, 0.0),
                    lambda: _F["mh464_alloc"]([1.0], [1.0], [0.25],
                                              1e6, 0.05, 1.5),
                    lambda: _F["mh464_alloc"]([0.0], [1.0], [0.25],
                                              1e6, 0.05, 0.25),
                    lambda: _F["mh464_alloc"]([-5.0], [1.0], [0.25],
                                              1e6, 0.05, 0.25),
                    lambda: _F["mh464_alloc"]([1.0], [0.0], [0.25],
                                              1e6, 0.05, 0.25),
                    lambda: _F["mh464_alloc"]([1.0], [1.0], [0.0],
                                              1e6, 0.05, 0.25),
                    lambda: _F["mh464_verdetto"]({"righe": []}, ["X", "Y"]),
                    lambda: _F["mh464_verdetto"]({"x": 1}, ["X"]),
                    lambda: _F["mh464_mappa"]([], K=1e6),
                    lambda: _F["mh464_mappa"]([("A", 31, 555),
                                               ("A", 345, 7)]),
                    lambda: _F["mh464_mappa"]([("A", 31, 555),
                                               ("", 345, 7)]),
                    lambda: _F["mh464_mappa"]([("A", 31)], K=1e6),
                    lambda: _F["mh464_mappa"]("A", K=1e6),
                    lambda: _F["mh464_mappa"]([("A", 31, 555)], K=0.0),
                    lambda: _F["mh464_mappa"]([("A", 31, 555)], rb=0.0),
                    lambda: _F["mh464_mappa"]([("A", 31, 555)],
                                              f_max=2.0)):
            with pytest.raises(ValueError):
                bad()
