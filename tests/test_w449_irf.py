"""Test tab449 '💥 Risposta allo shock: di quanto uno shock del gas muove power?': registry + funzioni pure."""

import math
import random
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh449_num", "mh449_parse_serie", "mh449_vecm",
           "mh449_irf", "mh449_verdetto", "mh449_mappa",
           "_mh449_seq", "_mh449_solve", "_mh449_ols",
           "_mh449_chol", "_mh449_matmul",
           "mh447_num", "mh447_eig", "mh447_rango",
           "mh447_trace", "mh447_max", "mh447_critico", "_mh447_lam_T",
           "_mh447_seq", "_mh447_solve", "_mh447_mul",
           "_mh447_transp", "_mh447_ols")

TITLE449 = "💥 Risposta allo shock: di quanto uno shock del gas muove power?"
TITLE451 = "🌊 Spillover gas↔power: chi trasmette e chi riceve gli shock?"
TITLE453 = "📊 Backtest VECM(1): il modello batte il random walk?"
TITLE455 = "🔮 Quando rientra lo spread? Forecast mean-reversion"
TITLE457 = "📐 Quanto puntare sul rientro? Sizing Kelly del trade"
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
TITLE446 = "📏 Variance ratio: il prezzo segue un random walk?"
TITLE445 = "🌀 Rolling drawdown: il peggior calo in ogni finestra"
TITLE444 = "🏞️ Lake ratio: l'area del dolore sotto il picco"
TITLE443 = "💹 Gain-to-Pain ratio: guadagni totali per ogni punto perso"
TITLE442 = "📐 Calmar geometrico: CAGR composto per unita' di peggior drawdown"
TITLE441 = "📈 Recovery Factor: profitto totale per unita' di peggior drawdown"
TITLE440 = "🎯 Drawdown-at-Risk (DaR): la soglia di drawdown superata solo nell'alpha% dei casi"
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
IRF0 = 0.8465880600888026
LR = 0.8503579309287612
LR_GAS = 0.46503079316836893
FEVD_06 = 0.5458922653435432
FEVD_12 = 0.6145289320327393
FEVD_24 = 0.6566828113367581
FEVD_36 = 0.6720395661735236
T50 = 0
A15Y = -0.30346693792017626
PT15 = 1.7654993601763673
LR15 = 0.7563966915854989
OLS_DIRETTA = 1.3590310703598587


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


class TestRegistry449:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 793
        assert "tab449" in dvars
        assert "tab449" in withs

    def test_titoli_allineati_440_441_442_443_444_445_446_447_448_449(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab440")] == TITLE440
        assert titoli[dvars.index("tab441")] == TITLE441
        assert titoli[dvars.index("tab442")] == TITLE442
        assert titoli[dvars.index("tab443")] == TITLE443
        assert titoli[dvars.index("tab444")] == TITLE444
        assert titoli[dvars.index("tab445")] == TITLE445
        assert titoli[dvars.index("tab446")] == TITLE446
        assert titoli[dvars.index("tab447")] == TITLE447
        assert titoli[dvars.index("tab448")] == TITLE448
        assert titoli[dvars.index("tab449")] == TITLE449

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


class TestIRF449:
    def _pw(self):
        return _F["mh449_parse_serie"](DEMO_POWER)

    def _gs(self):
        return _F["mh449_parse_serie"](DEMO_GAS)

    def test_demo_valori(self):
        pw, gs = self._pw(), self._gs()
        assert len(pw) == 60 and len(gs) == 60
        assert pw[0] == 115.0 and gs[0] == 40.0
        m = _F["mh449_mappa"](pw, gs, H=24)
        assert m["n"] == 60 and m["T"] == 59 and m["H"] == 24
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
        assert abs(m["irf0"] - IRF0) < 1e-12
        assert abs(m["lr"] - LR) < 1e-12
        assert abs(m["lr_gas"] - LR_GAS) < 1e-12
        assert abs(m["share_H"] - FEVD_24) < 1e-12
        assert m["t50"] == T50 == 0  # trasmissione istantanea
        assert len(m["irf"]) == 25 and len(m["gen"]) == 25
        assert len(m["fevd"]) == 24 and len(m["irf_gas"]) == 25
        assert m["verdetto"].startswith("IL GAS GUIDA IL POWER")
        assert "65.7%" in m["verdetto"]
        # in QUESTO campione il gas ha t > 2 (rumore: e' un RW puro
        # per costruzione, vedi tab448 chiave 3) -> flag False
        assert T_G > 2.0
        assert m["gas_esogeno"] is False

    def test_definizione_a_mano(self):
        # ec demeaned -> OLS 2x2 per equazione -> Sigma/Cholesky/A ->
        # Phi ricorsivo -> IRF/FEVD/LR, tutto con loop espliciti
        pw, gs = self._pw(), self._gs()
        n = len(pw)
        ec_raw = [y - BETA * g for y, g in zip(pw, gs)]
        mu = sum(ec_raw) / n
        ec = [v - mu for v in ec_raw]
        assert abs(sum(ec) / n) < 1e-9
        al, rs = {}, {}
        for nome, y in (("power", pw), ("gas", gs)):
            dy = [y[t] - y[t - 1] for t in range(1, n)]
            a, _c, se_a, t_a = _ols2_mano(ec[:-1], dy)
            al[nome] = a
            rs[nome] = (a, se_a, t_a)
            e = _F["mh449_vecm"](pw, gs)
            assert abs(e[f"alpha_{nome}"] - a) < 1e-9, nome
            assert abs(e[f"se_{nome}"] - se_a) < 1e-9, nome
            assert abs(e[f"t_{nome}"] - t_a) < 1e-9, nome
        assert abs(al["power"] - ALPHA_P) < 1e-9
        assert abs(al["gas"] - ALPHA_G) < 1e-9
        # residui -> Sigma -> Cholesky -> A -> Phi -> IRF
        dy_p = [pw[t] - pw[t - 1] for t in range(1, n)]
        dy_g = [gs[t] - gs[t - 1] for t in range(1, n)]
        xs = ec[:-1]
        rx = [y - (al["gas"] * x + _ols2_mano(xs, dy_g)[1])
              for x, y in zip(xs, dy_g)]
        ry = [y - (al["power"] * x + _ols2_mano(xs, dy_p)[1])
              for x, y in zip(xs, dy_p)]
        dof = n - 3
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
        r = _F["mh449_irf"](pw, gs, H=24)
        irf_mano, own_mano = [], []
        for h in range(25):
            irf_mano.append(Phi[1][0] * l00 + Phi[1][1] * l10)
            own_mano.append(Phi[1][1] * l11)
            assert abs(irf_mano[h] - r["irf"][h]) < 1e-9, h
            Phi = [[A[0][0] * Phi[0][0] + A[0][1] * Phi[1][0],
                    A[0][0] * Phi[0][1] + A[0][1] * Phi[1][1]],
                   [A[1][0] * Phi[0][0] + A[1][1] * Phi[1][0],
                    A[1][0] * Phi[0][1] + A[1][1] * Phi[1][1]]]
        # FEVD a mano a h = 24
        num = sum(irf_mano[k] ** 2 for k in range(24))
        den = num + sum(own_mano[k] ** 2 for k in range(24))
        assert abs(num / den - r["fevd"][-1]) < 1e-9
        assert abs(num / den - FEVD_24) < 1e-9
        # LR a mano: Phi a 200 periodi
        P = [[1.0, 0.0], [0.0, 1.0]]
        for _ in range(200):
            P = [[A[0][0] * P[0][0] + A[0][1] * P[1][0],
                  A[0][0] * P[0][1] + A[0][1] * P[1][1]],
                 [A[1][0] * P[0][0] + A[1][1] * P[1][0],
                  A[1][0] * P[0][1] + A[1][1] * P[1][1]]]
        assert abs(P[1][0] * l00 + P[1][1] * l10 - LR) < 1e-9
        assert abs(P[0][0] * l00 + P[0][1] * l10 - LR_GAS) < 1e-9

    def test_chiave_lr_su_lrg_uguale_beta(self):
        # IDENTITA' ESATTA: gli shift permanenti stanno nel rapporto
        # del vettore cointegrante (ec torna a media nulla)
        pw, gs = self._pw(), self._gs()
        r = _F["mh449_irf"](pw, gs, H=24)
        assert abs(r["lr"] / r["lr_gas"] - r["beta"]) < 1e-9
        assert abs(r["lr"] / r["lr_gas"] - BETA) < 1e-9

    def test_chiave_gen_uguale_cholesky(self):
        # GIRF (Pesaran-Shin) per lo shock ordinato primo = Cholesky
        # ESATTO: stessa colonna di Sigma normalizzata
        pw, gs = self._pw(), self._gs()
        r = _F["mh449_irf"](pw, gs, H=24)
        for h in range(25):
            assert abs(r["gen"][h] - r["irf"][h]) < 1e-12, h

    def test_chiave_ordinamento(self):
        # Ordinamento [power, gas] a mano: lo shock gas non tocca la
        # power in contemporanea (impatto 0.0 ESATTO), ma il rapporto
        # LR/LR_gas resta beta (il lungo non dipende dall'ordinamento)
        pw, gs = self._pw(), self._gs()
        v = _F["mh449_vecm"](pw, gs)
        S = v["Sigma"]
        A = v["A"]
        Sr = [[S[1][1], S[1][0]], [S[1][0], S[0][0]]]
        rl00 = math.sqrt(Sr[0][0])
        rl10 = Sr[0][1] / rl00
        rl11 = math.sqrt(Sr[1][1] - rl10 * rl10)
        Ar = [[A[1][1], A[1][0]], [A[0][1], A[0][0]]]
        # impatto contemporaneo della power (indice 0) allo shock gas
        # (colonna 1): (I @ Lr)[0,1] = 0 ESATTO
        assert 1.0 * 0.0 + 0.0 * rl11 == 0.0
        P = [[1.0, 0.0], [0.0, 1.0]]
        for _ in range(200):
            P = [[Ar[0][0] * P[0][0] + Ar[0][1] * P[1][0],
                  Ar[0][0] * P[0][1] + Ar[0][1] * P[1][1]],
                 [Ar[1][0] * P[0][0] + Ar[1][1] * P[1][0],
                  Ar[1][0] * P[0][1] + Ar[1][1] * P[1][1]]]
        lrr = P[0][0] * 0.0 + P[0][1] * rl11
        lrgr = P[1][0] * 0.0 + P[1][1] * rl11
        assert abs(lrr / lrgr - BETA) < 1e-9

    def test_chiave_beta_vera(self):
        # Con la beta VERA (1.5, nota per costruzione) il modello
        # ritrova il DGP: LR/LR_gas = 1.5 ESATTO
        pw, gs = self._pw(), self._gs()
        r = _F["mh449_irf"](pw, gs, H=24, beta=1.5)
        assert abs(r["beta"] - 1.5) < 1e-12
        assert abs(r["lr"] / r["lr_gas"] - 1.5) < 1e-9
        assert abs(r["lr"] - LR15) < 1e-12
        # cross-check tab448 chiave 1: alpha_power con beta vera
        assert abs(r["alpha_power"] - A15Y) < 1e-12
        assert abs(A15Y - (-0.3035)) < 1e-3
        # pass-through contemporaneo di Cholesky: sovrastima l'OLS
        # diretta per la corr in-sample 0.30 (stesso rumore tab448)
        assert abs(r["irf"][0] / r["sigma_g"] - PT15) < 1e-12
        assert abs(PT15 - 1.7655) < 1e-3
        assert abs(OLS_DIRETTA - 1.3590) < 1e-3
        assert PT15 > OLS_DIRETTA  # Cholesky gonfiato dal rumore

    def test_fevd_monotona_e_limitata(self):
        pw, gs = self._pw(), self._gs()
        for H, att in ((6, FEVD_06), (12, FEVD_12), (24, FEVD_24),
                       (36, FEVD_36)):
            r = _F["mh449_irf"](pw, gs, H=H)
            assert len(r["fevd"]) == H
            assert all(0.0 < v < 1.0 for v in r["fevd"])
            assert all(b >= a for a, b in zip(r["fevd"], r["fevd"][1:]))
            assert abs(r["fevd"][-1] - att) < 1e-12
        assert FEVD_06 < FEVD_12 < FEVD_24 < FEVD_36  # cresce, plateau

    def test_controlli(self):
        # RANDOM WALK INDIPENDENTI (Johansen rango 0): niente IRF,
        # l'IRF di lungo periodo non e' identificata
        with pytest.raises(ValueError, match="cointegrazione"):
            _F["mh449_mappa"](_rw(20261014), _rw(777))
        # AR(1) STAZIONARIE (Johansen rango 2): niente VECM
        with pytest.raises(ValueError, match="stazionarie"):
            _F["mh449_mappa"](_ar1(0.5, 20261014), _ar1(0.5, 777))

    def test_verdetto_soglie(self):
        v = _F["mh449_verdetto"]
        assert v(0.75).startswith("IL GAS GUIDA IL POWER")
        assert v(0.50).startswith("IL GAS GUIDA IL POWER")
        assert v(0.6567).startswith("IL GAS GUIDA IL POWER")
        assert v(0.4999).startswith("TRASMISSIONE FORTE")
        assert v(0.25).startswith("TRASMISSIONE FORTE")
        assert v(0.2499).startswith("TRASMISSIONE MODERATA")
        assert v(0.10).startswith("TRASMISSIONE MODERATA")
        assert v(0.0999).startswith("TRASMISSIONE DEBOLE")
        assert v(0.02).startswith("TRASMISSIONE DEBOLE")
        assert v(0.0199).startswith("NESSUNA TRASMISSIONE")
        assert v(0.0).startswith("NESSUNA TRASMISSIONE")
        assert v(1.0).startswith("IL GAS GUIDA IL POWER")
        for bad in (lambda: v(float("nan")),
                    lambda: v(float("inf")),
                    lambda: v(-0.1),
                    lambda: v(1.1),
                    lambda: v("x"),
                    lambda: v(True),
                    lambda: v(None)):
            with pytest.raises(ValueError):
                bad()

    def test_degeneri(self):
        pw, gs = self._pw(), self._gs()
        flat = tuple([5.0] * 40)
        for bad in (lambda: _F["mh449_mappa"](tuple([1.0] * 29),
                                              tuple([1.0] * 29)),
                    lambda: _F["mh449_mappa"](None, gs),
                    lambda: _F["mh449_mappa"](pw, None),
                    lambda: _F["mh449_mappa"](pw, gs[:50]),
                    lambda: _F["mh449_mappa"](pw, gs + (1.0,)),
                    lambda: _F["mh449_mappa"](flat, gs),
                    lambda: _F["mh449_mappa"](pw, flat),
                    lambda: _F["mh449_mappa"](pw, pw),
                    lambda: _F["mh449_vecm"](pw, gs,
                                             beta=float("nan")),
                    lambda: _F["mh449_vecm"](pw, gs,
                                             beta=float("inf")),
                    lambda: _F["mh449_vecm"](pw, gs, beta="1.5"),
                    lambda: _F["mh449_vecm"](pw, gs, beta=True),
                    lambda: _F["mh449_irf"](pw, gs, H=0),
                    lambda: _F["mh449_irf"](pw, gs, H=121),
                    lambda: _F["mh449_irf"](pw, gs, H="24"),
                    lambda: _F["mh449_irf"](pw, gs, H=True),
                    lambda: _F["mh449_num"](float("nan"), "x"),
                    lambda: _F["mh449_num"](True, "x"),
                    lambda: _F["mh449_num"]("1.5", "x")):
            with pytest.raises(ValueError):
                bad()

    def test_parse_serie(self):
        xs = _F["mh449_parse_serie"]("1,5\n" + "2.5\n" * 29)
        assert len(xs) == 30
        assert xs[0] == 1.5 and xs[1] == 2.5
        with pytest.raises(ValueError):
            _F["mh449_parse_serie"]("1\n2\nabc\n" + "1\n" * 30)
        with pytest.raises(ValueError):
            _F["mh449_parse_serie"]("1\n2\n")
        with pytest.raises(ValueError):
            _F["mh449_parse_serie"](None)

    def test_solve_e_chol(self):
        X = _F["_mh449_solve"]([[2.0, 1.0], [1.0, 3.0]],
                               [[5.0], [10.0]])
        assert abs(X[0][0] - 1.0) < 1e-12
        assert abs(X[1][0] - 3.0) < 1e-12
        with pytest.raises(ValueError):
            _F["_mh449_solve"]([[1.0, 2.0], [2.0, 4.0]],
                               [[1.0], [1.0]])
        l00, l10, l11 = _F["_mh449_chol"](4.0, 2.0, 2.0)
        assert abs(l00 - 2.0) < 1e-12
        assert abs(l10 - 1.0) < 1e-12
        assert abs(l11 - 1.0) < 1e-12
        with pytest.raises(ValueError):
            _F["_mh449_chol"](0.0, 0.0, 1.0)
        with pytest.raises(ValueError):
            _F["_mh449_chol"](1.0, 1.0, 1.0)  # singolare

