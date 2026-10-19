"""Test tab465 '📐 Correlazione: la diversificazione è reale?': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh465_num", "mh465_dspread", "mh465_corr", "mh465_alloc",
           "mh465_verdetto", "mh465_mappa", "_mh465_chol", "_mh465_S",
           "mh464_num", "mh464_serie", "mh464_coppia", "mh464_alloc",
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
TITLE455 = "🔮 Quando rientra lo spread? Forecast mean-reversion"
TITLE454 = "⚖️ Lo spread è stazionario? Test ADF"
TITLE453 = "📊 Backtest VECM(1): il modello batte il random walk?"
COPPIE = (("A", 31, 555), ("B", 345, 7), ("C", 12, 555))
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
BETA_C = 1.5621385231753926
Z_C = -1.1297286767215544
H_STAR_C = 10
MU_PNL_C = 314299.4634041563
SIGMA_PNL_C = 428966.437395976
F_APP_C = 0.25
SCHED_C = "one-shot"
MU_C = 351170.93470905913
CORR_AB = 0.09003532721259302
CORR_AC = 0.9937515935535327
CORR_BC = 0.07883309536728715
CORR_MAX = 0.9937515935535327
RAPPORTO = 1.3298684940190912
RISCHIO_VERO = 66493.42470095457
KAP = 1000000.0
RBB = 0.05
FMAX = 0.25
G_A = 0.0
G_B = 0.01982256579754679
G_C = 0.019883614787643215
EDGE_TOT = 55622.26099071126
RB_USATO = 0.049999999999999996
SHARPE = 1.1124452198142254
VERDETTO = "CORRELATI"
N_CAP = 0
N_FLOOR = 1

_DEMO = None


def _demo():
    global _DEMO
    if _DEMO is None:
        _DEMO = _F["mh465_mappa"](COPPIE, K=KAP, rb=RBB, f_max=FMAX,
                                  z_entry=1.0, costo=0.20, H=10)
    return _DEMO


class TestRegistry465:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 565
        assert "tab465" in dvars
        assert "tab465" in withs

    def test_titoli_allineati_453_454_455_456_457_458_459_460_461_462_463_464_465(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        attesi = {453: TITLE453, 454: TITLE454, 455: TITLE455,
                  456: TITLE456, 457: TITLE457, 458: TITLE458,
                  459: TITLE459, 460: TITLE460, 461: TITLE461,
                  462: TITLE462, 463: TITLE463, 464: TITLE464,
                  465: TITLE465}
        for n, att in attesi.items():
            assert titoli[dvars.index(f"tab{n}")] == att, f"tab{n}"
        assert len({titoli[dvars.index(f"tab{n}")] for n in attesi}) == 13


class TestCorrelazione465:
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
        C = m["corr"]
        assert abs(C[0][1] - CORR_AB) < 1e-12
        assert abs(C[0][2] - CORR_AC) < 1e-12
        assert abs(C[1][2] - CORR_BC) < 1e-12
        for i in range(3):
            assert C[i][i] == 1.0
        assert abs(m["corr_max"] - CORR_MAX) < 1e-12
        assert abs(m["rapporto"] - RAPPORTO) < 1e-9
        assert abs(m["rischio_vero"] - RISCHIO_VERO) < 1e-6
        a = m["alloc_corr"]
        assert a is not None
        assert a["n_capped"] == N_CAP
        assert a["n_floored"] == N_FLOOR
        gs = {"A": G_A, "B": G_B, "C": G_C}
        for r in a["righe"]:
            assert abs(r["g"] - gs[r["nome"]]) < 1e-12, r["nome"]
            assert abs(r["eur"] - r["g"] * KAP) < 1e-6
        assert a["righe"][0]["floored"] is True
        assert a["righe"][0]["g"] == 0.0
        assert abs(a["edge_tot"] - EDGE_TOT) < 1e-6
        assert abs(a["var_tot"] - (RBB * KAP) ** 2) < 1e-3
        assert abs(a["rb_usato"] - RB_USATO) < 1e-9
        assert abs(a["sharpe"] - SHARPE) < 1e-9
        # rischio vero dell'allocazione diagonale: ricalcolo indipendente
        d = m["alloc_diag"]
        gd = [r["g"] for r in d["righe"]]
        u = [r["sigma"] / r["f_app"] for r in d["righe"]]
        S = _F["_mh465_S"](u, C, 1e-6)
        rv = math.sqrt(sum(gd[i] * S[i][j] * gd[j]
                           for i in range(3) for j in range(3)))
        assert abs(rv - RISCHIO_VERO) < 1e-6
        assert m["verdetto"].startswith(VERDETTO)
        print(f"demo: corr_max={m['corr_max']:.4f} rapporto={m['rapporto']:.2f} "
              f"g={[round(r['g'], 4) for r in a['righe']]} -> {VERDETTO}")

    def test_coerenza_tab464(self):
        # con corr = I, mh465_alloc coincide con mh464_alloc (1e-12)
        att = self._coppie_attese()
        mus = [att[n][7] for n in "ABC"]
        sgs = [att[n][4] for n in "ABC"]
        fas = [att[n][5] for n in "ABC"]
        I = [[1.0 if i == j else 0.0 for j in range(3)] for i in range(3)]
        aI = _F["mh465_alloc"](mus, sgs, fas, I, KAP, RBB, FMAX)
        aD = _F["mh464_alloc"](mus, sgs, fas, KAP, RBB, FMAX)
        for r1, r2 in zip(aI["righe"], aD["righe"]):
            assert abs(r1["g"] - r2["g"]) < 1e-12
            assert r1["capped"] == r2["capped"]
        assert abs(aI["edge_tot"] / aD["edge_tot"] - 1.0) < 1e-9
        assert abs(aI["var_tot"] / aD["var_tot"] - 1.0) < 1e-9
        # coerenza anche con cap vincolante (caso diagonale di tab464)
        aIc = _F["mh465_alloc"]([1e6, 1e5], [1e5, 1e5], [0.25, 0.25],
                                [[1.0, 0.0], [0.0, 1.0]],
                                1e6, 0.05, 0.10)
        aDc = _F["mh464_alloc"]([1e6, 1e5], [1e5, 1e5], [0.25, 0.25],
                                1e6, 0.05, 0.10)
        assert aIc["righe"][0]["g"] == 0.10
        assert abs(aIc["righe"][1]["g"] - 0.075) < 1e-12
        assert abs(aIc["edge_tot"] - aDc["edge_tot"]) < 1e-6
        print("coerenza tab464 OK (I -> identico, anche con cap)")

    def test_definizione_a_mano(self):
        # 2 trade, corr 0.5: forma chiusa via aggiunta 2x2 scritta a mano
        # (indipendente da _mh465_chol), ridge incluso
        mu2 = [600000.0, 300000.0]
        sg2 = [200000.0, 200000.0]
        fa2 = [0.25, 0.25]
        rho_t = 0.5 * (1.0 - 1e-6)
        e1, e2 = mu2[0] / fa2[0], mu2[1] / fa2[1]
        S11 = (sg2[0] / fa2[0]) ** 2
        S22 = (sg2[1] / fa2[1]) ** 2
        S12 = rho_t * (sg2[0] / fa2[0]) * (sg2[1] / fa2[1])
        det = S11 * S22 - S12 ** 2
        Se1 = (S22 * e1 - S12 * e2) / det
        Se2 = (-S12 * e1 + S11 * e2) / det
        den = math.sqrt(e1 * Se1 + e2 * Se2)
        g1e = RBB * KAP * Se1 / den
        g2e = RBB * KAP * Se2 / den
        a = _F["mh465_alloc"](mu2, sg2, fa2, [[1.0, 0.5], [0.5, 1.0]],
                              KAP, RBB, FMAX)
        assert abs(a["righe"][0]["g"] - g1e) < 1e-12
        assert abs(a["righe"][1]["g"] - g2e) < 1e-12
        assert a["n_capped"] == 0 and a["n_floored"] == 0
        assert abs(a["var_tot"] / (RBB * KAP) ** 2 - 1.0) < 1e-9
        print("definizione a mano OK (chiusa 2x2, 1e-12)")

    def test_bound_patologico(self):
        # rilassato: g* = (0.1437, -0.0605) per via dell'hedge;
        # l'ottimo vero e' (0.10, g2): cap reale, floor spurio.
        # g2 a mano via completamento del quadrato (codice indipendente)
        S11 = (1e5 / 0.25) ** 2
        S12 = 0.5 * (1.0 - 1e-6) * S11
        e2 = 1e5 / 0.25
        v = S12 * 0.10
        w = v / S11
        B2p = (RBB * KAP) ** 2 - 0.01 * S11 + v * w
        Bp = math.sqrt(B2p)
        y = e2 / S11
        g2e = Bp * y / math.sqrt(e2 * y) - w
        a = _F["mh465_alloc"]([1e6, 1e5], [1e5, 1e5], [0.25, 0.25],
                              [[1.0, 0.5], [0.5, 1.0]], 1e6, 0.05, 0.10)
        assert a["righe"][0]["g"] == 0.10
        assert a["righe"][0]["capped"] is True
        assert abs(a["righe"][1]["g"] - g2e) < 1e-9
        assert a["righe"][1]["capped"] is False
        assert a["righe"][1]["floored"] is False
        assert a["n_capped"] == 1 and a["n_floored"] == 0
        assert a["var_tot"] <= (0.05 * 1e6) ** 2 * (1.0 + 1e-9)
        print("bound patologico OK (cap reale, floor spurio)")

    def test_hedge_degenere(self):
        # due asset quasi-identici: il rilassato vorrebbe un long-short
        # enorme; l'ottimo azzera il doppione -> (0, B/u2)
        mu9 = [159411.69673319787, 184455.55120546662]
        sg9 = [123658.86474157251, 124334.68100362195]
        fa9 = [0.2682332286536105, 0.31510557667951505]
        C9 = [[1.0, 0.9940972807090636], [0.9940972807090636, 1.0]]
        fm9 = 0.3048535506678764
        a = _F["mh465_alloc"](mu9, sg9, fa9, C9, 1e6, 0.05, fm9)
        u2 = sg9[1] / fa9[1]
        assert a["righe"][0]["g"] == 0.0
        assert a["righe"][0]["floored"] is True
        assert abs(a["righe"][1]["g"] - 0.05 * 1e6 / u2) < 1e-9
        assert abs(a["var_tot"] / (0.05 * 1e6) ** 2 - 1.0) < 1e-9
        print("hedge degenere OK (doppione azzerato)")

    def test_verdetti(self):
        v = _F["mh465_verdetto"]
        assert v(None).startswith("NESSUN TRADE")
        m_ns = _F["mh465_mappa"]([("N1", 136, 5555), ("N2", 91, 7777)],
                                 K=KAP, rb=RBB, f_max=FMAX)
        assert m_ns["eligibili"] == []
        assert m_ns["alloc_corr"] is None
        assert m_ns["verdetto"].startswith("NESSUN TRADE")
        assert _demo()["verdetto"].startswith("CORRELATI")
        m_ab = _F["mh465_mappa"]([("A", 31, 555), ("B", 345, 7)],
                                 K=KAP, rb=RBB, f_max=FMAX)
        assert m_ab["eligibili"] == ["A", "B"]
        assert m_ab["corr_max"] < 0.5
        assert m_ab["rapporto"] < 1.15
        assert m_ab["verdetto"].startswith("INDIPENDENTI")
        print("verdetti OK (NESSUN/CORRELATI/INDIPENDENTI)")

    def test_corr_proprieta(self):
        Cc = _F["mh465_corr"]
        assert Cc([(1.0, 2.0, 3.0), (1.0, 2.0, 3.0)])[0][1] == 1.0
        assert Cc([(1.0, 2.0, 3.0), (3.0, 2.0, 1.0)])[0][1] == -1.0
        C = _demo()["corr"]
        for i in range(3):
            assert C[i][i] == 1.0
            for j in range(3):
                assert abs(C[i][j] - C[j][i]) < 1e-15
                assert abs(C[i][j]) <= 1.0 + 1e-12
        # serie demo A e C: stesso driver -> quasi 1
        assert C[0][2] > 0.99
        for bad in (lambda: Cc([]),
                    lambda: Cc([(1.0,)]),
                    lambda: Cc([(1.0, 2.0), (5.0, 5.0)]),
                    lambda: Cc([(1.0, 2.0), (1.0,)]),
                    lambda: Cc([(1.0, "x"), (1.0, 2.0)])):
            with pytest.raises(ValueError):
                bad()

    def test_dspread_deterministica(self):
        d1 = _F["mh465_dspread"](31, 555, 1.5, "long spread (x)")
        d2 = _F["mh465_dspread"](31, 555, 1.5, "long spread (x)")
        assert d1 == d2 and len(d1) == 59
        ds = _F["mh465_dspread"](31, 555, 1.5, "short spread (x)")
        assert ds == tuple(-x for x in d1)
        for bad in (lambda: _F["mh465_dspread"](31, 555, 1.5, "flat"),
                    lambda: _F["mh465_dspread"](31, 555, 1.5, 3),
                    lambda: _F["mh465_dspread"](31, 555, float("nan"),
                                                "long x"),
                    lambda: _F["mh465_dspread"](-1, 555, 1.5, "long x")):
            with pytest.raises(ValueError):
                bad()

    def test_degeneri(self):
        for bad in (lambda: _F["mh465_num"](float("nan"), "x"),
                    lambda: _F["mh465_num"](True, "x"),
                    lambda: _F["mh465_num"]("1.5", "x"),
                    lambda: _F["_mh465_chol"]([[0.0]], [1.0]),
                    lambda: _F["_mh465_chol"]([[1.0, 2.0], [2.0, 1.0]],
                                              [1.0, 1.0]),
                    lambda: _F["mh465_alloc"]([], [], [], [], 1e6, 0.05,
                                              0.25),
                    lambda: _F["mh465_alloc"]([1.0], [1.0], [0.25],
                                              [[1.0]], 1e6, 0.05, 0.25,
                                              eps=0.0),
                    lambda: _F["mh465_alloc"]([1.0], [1.0], [0.25],
                                              [[1.0, 0.0]], 1e6, 0.05,
                                              0.25),
                    lambda: _F["mh465_alloc"]([1.0], [1.0], [0.25],
                                              [[2.0]], 1e6, 0.05, 0.25),
                    lambda: _F["mh465_alloc"]([0.0], [1.0], [0.25],
                                              [[1.0]], 1e6, 0.05, 0.25),
                    lambda: _F["mh465_alloc"]([1.0], [0.0], [0.25],
                                              [[1.0]], 1e6, 0.05, 0.25),
                    lambda: _F["mh465_alloc"]([1.0], [1.0], [0.0],
                                              [[1.0]], 1e6, 0.05, 0.25),
                    lambda: _F["mh465_alloc"]([1.0], [1.0], [0.25],
                                              [[1.0]], 0.0, 0.05, 0.25),
                    lambda: _F["mh465_alloc"]([1.0], [1.0], [0.25],
                                              [[1.0]], 1e6, 0.0, 0.25),
                    lambda: _F["mh465_alloc"]([1.0], [1.0], [0.25],
                                              [[1.0]], 1e6, 0.05, 0.0),
                    lambda: _F["mh465_alloc"]([1.0] * 11, [1.0] * 11,
                                              [0.25] * 11,
                                              [[1.0] * 11] * 11,
                                              1e6, 0.05, 0.25),
                    lambda: _F["mh465_verdetto"]([]),
                    lambda: _F["mh465_mappa"]([], K=1e6),
                    lambda: _F["mh465_mappa"]([("A", 31, 555),
                                               ("A", 345, 7)]),
                    lambda: _F["mh465_mappa"]([("A", 31)], K=1e6),
                    lambda: _F["mh465_mappa"]("A", K=1e6),
                    lambda: _F["mh465_mappa"]([("A", 31, 555)], K=0.0),
                    lambda: _F["mh465_mappa"]([("A", 31, 555)],
                                              soglia_corr=1.5),
                    lambda: _F["mh465_mappa"]([("A", 31, 555)],
                                              soglia_rischio=0.9)):
            with pytest.raises(ValueError):
                bad()
