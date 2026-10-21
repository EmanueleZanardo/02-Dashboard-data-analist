"""Test tab459 '🧪⚠️ Stress test del trade: VaR sotto shock': registry + funzioni pure."""

import math
import random
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh459_num", "mh459_shock", "mh459_verdetto", "mh459_mappa",
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
           "mh447_trace", "mh447_max", "mh447_critico", "_mh447_lam_T",
           "_mh447_seq", "_mh447_solve", "_mh447_mul",
           "_mh447_transp", "_mh447_ols")

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
TITLE461 = "🧭 Ottimizza stop/target: i migliori k"
TITLE460 = "🛑 Stop & target: dove chiudere il trade"
TITLE482 = "🗓️ Ladder delle scadenze: profilo temporale di volumi, MtM e DV01"
TITLE455 = "🔮 Quando rientra lo spread? Forecast mean-reversion"
TITLE454 = "⚖️ Lo spread è stazionario? Test ADF"
TITLE453 = "📊 Backtest VECM(1): il modello batte il random walk?"
TITLE452 = "📈 Previsione VECM(1): dove vanno power e gas nei prossimi H giorni?"
TITLE451 = "🌊 Spillover gas↔power: chi trasmette e chi riceve gli shock?"
TITLE450 = "📜 Scomposizione storica: cosa ha mosso davvero il prezzo power?"
TITLE449 = "💥 Risposta allo shock: di quanto uno shock del gas muove power?"
DEMO_POWER = '115.0\n114.222584\n115.526527\n115.270435\n115.404795\n113.275972\n114.840219\n116.685764\n115.420859\n113.571058\n112.06301\n112.194403\n116.139654\n117.765956\n116.742831\n116.62762\n115.739526\n117.414453\n114.867579\n116.640701\n115.779325\n115.137451\n116.642853\n117.253244\n117.493738\n117.242796\n118.334843\n119.091227\n116.768615\n115.421416\n116.033447\n114.144567\n113.700317\n114.354433\n114.876507\n113.755332\n115.568524\n116.069102\n116.138549\n117.333173\n117.084818\n116.63492\n117.999467\n117.718767\n117.668152\n118.796536\n116.597527\n114.618757\n114.130273\n116.852609\n116.128887\n119.874946\n118.472635\n119.958398\n119.950907\n122.309881\n121.085938\n120.106701\n119.684133\n119.645704\n'
DEMO_GAS = '40.0\n39.387964\n39.576758\n40.074258\n39.817653\n39.153163\n39.120398\n39.359404\n39.908497\n39.300559\n38.654127\n39.007091\n39.244134\n40.011027\n40.502256\n40.451366\n40.314247\n41.599511\n41.45511\n41.062643\n40.493471\n40.541201\n40.613858\n40.441425\n40.410346\n40.546892\n40.893091\n41.441492\n41.5464\n40.651509\n41.002372\n40.292523\n40.206815\n39.469916\n39.470967\n39.081684\n39.188627\n40.838781\n40.814478\n41.23564\n40.573978\n40.429951\n40.761193\n40.714858\n40.899949\n40.951613\n40.448546\n40.730418\n40.324405\n41.260281\n41.00768\n41.350726\n41.351901\n41.828116\n41.527041\n42.026474\n41.964525\n42.596178\n42.908275\n42.978922\n'
BETA = 1.8286056394998358
Z = -1.0023831726745032
H_STAR = 10
MU_PNL = 366747.52222252387
SIGMA_PNL = 444862.37867309677
VAR_BASE = 364985.97483217873
ES_BASE = 550875.8038446917
VAR_VOL = 730852.7233595301
ES_VOL = 1009687.4668782994
VAR_DRIFT = 587417.1641687271
ES_DRIFT = 773306.99318124
VAR_WORST = 953283.9126960784
ES_WORST = 1232118.6562148477
P_PERDITA_WORST = 0.4143882063795459
VAR_UNIT_WORST = 2.8481340037213614
SIZE_MAX_STRESS = 140442.83010467957
F_LIM_STRESS = 0.10490054292134227
KAP = 1000000.0
LIMITE = 400000.0
K_VOL = 1.5
DRIFT = 0.5


def _rw(seed, n=60):
    rng = random.Random(seed)
    out = [0.0]
    for _ in range(1, n):
        out.append(out[-1] + rng.gauss(0.0, 1.0))
    return tuple(out)


class TestRegistry459:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 626
        assert "tab459" in dvars
        assert "tab459" in withs

    def test_titoli_allineati_449_450_451_452_453_454_455_456_457_458_459(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab449")] == TITLE449
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


class TestStressTrade459:
    def _pw(self):
        return _F["mh456_parse_serie"](DEMO_POWER)

    def _gs(self):
        return _F["mh456_parse_serie"](DEMO_GAS)

    def _m(self, **kw):
        d = dict(z_entry=1.0, costo=0.20, H=10, capitale=KAP,
                 f_max=0.25, alpha=0.05, limite=LIMITE,
                 k_vol=K_VOL, drift=DRIFT)
        d.update(kw)
        return _F["mh459_mappa"](self._pw(), self._gs(), **d)

    def _sc(self, m, nome):
        return [s for s in m["scenari"] if s["nome"] == nome][0]

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
        assert abs(m["k_vol"] - K_VOL) < 1e-12
        assert abs(m["drift"] - DRIFT) < 1e-12
        assert abs(m["limite"] - LIMITE) < 1e-12
        assert [s["nome"] for s in m["scenari"]] == [
            "BASE", "VOL SHOCK", "DRIFT SHOCK", "COMBINATO"]
        base, vol, drf, cmb = (self._sc(m, n) for n in
                               ("BASE", "VOL SHOCK", "DRIFT SHOCK",
                                "COMBINATO"))
        assert abs(base["var"] - VAR_BASE) < 1e-6
        assert abs(base["es"] - ES_BASE) < 1e-6
        assert abs(base["var"] - 364986.0) < 1.0  # tab458, 1e-9
        assert abs(vol["var"] - VAR_VOL) < 1e-6
        assert abs(vol["var"] - 730852.7) < 1.0
        assert abs(drf["var"] - VAR_DRIFT) < 1e-6
        assert abs(drf["var"] - 587417.2) < 1.0
        assert abs(cmb["var"] - VAR_WORST) < 1e-6
        assert abs(cmb["var"] - 953283.9) < 1.0
        assert abs(cmb["es"] - ES_WORST) < 1e-6
        assert abs(cmb["es"] - 1232118.7) < 1.0
        assert cmb["es"] > cmb["var"] > 0.0  # coda oltre il VaR
        assert m["worst"] == "COMBINATO"
        assert abs(m["var_worst"] - VAR_WORST) < 1e-6
        assert abs(m["es_worst"] - ES_WORST) < 1e-6
        assert abs(m["p_perdita_worst"] - P_PERDITA_WORST) < 1e-9
        assert abs(m["p_perdita_worst"] - 0.4144) < 1e-3
        # shock batte il base su entrambi gli assi
        assert vol["var"] > base["var"] and drf["var"] > base["var"]
        assert cmb["var"] > vol["var"] and cmb["var"] > drf["var"]
        assert m["zero_motivo"] is None
        assert m["verdetto"].startswith("VULNERABILE")
        assert "953" in m["verdetto"]
        # size massima compatibile col limite nello scenario peggiore
        assert abs(m["var_unit_worst"] - VAR_UNIT_WORST) < 1e-9
        assert abs(m["var_unit_worst"] - 2.8481) < 1e-3
        assert abs(m["size_max_stress"] - SIZE_MAX_STRESS) < 1e-3
        assert abs(m["size_max_stress"] - 140442.8) < 1.0
        assert m["size_max_stress"] < m["size"]
        assert abs(m["f_lim_stress"] - F_LIM_STRESS) < 1e-9
        assert abs(m["f_lim_stress"] - 0.1049) < 1e-3
        assert m["f_lim_stress"] < m["f_app"]

    def test_definizione_a_mano(self):
        # shock: trasformazione parametrica a mano
        sh = _F["mh459_shock"](MU_PNL, SIGMA_PNL, K_VOL, DRIFT)
        assert abs(sh["mu_s"] - (MU_PNL - DRIFT * SIGMA_PNL)) < 1e-9
        assert abs(sh["sigma_s"] - K_VOL * SIGMA_PNL) < 1e-9
        sh0 = _F["mh459_shock"](MU_PNL, SIGMA_PNL, 1.0, 0.0)
        assert abs(sh0["mu_s"] - MU_PNL) < 1e-12
        assert abs(sh0["sigma_s"] - SIGMA_PNL) < 1e-12
        # var/es del COMBINATO a mano: formula indipendente con z noto
        z5 = -1.6448536269514729
        pdf5 = math.exp(-0.5 * z5 * z5) / math.sqrt(2.0 * math.pi)
        mu_c = MU_PNL - DRIFT * SIGMA_PNL
        sg_c = K_VOL * SIGMA_PNL
        var_mano = -(mu_c + z5 * sg_c)
        es_mano = -mu_c + sg_c * pdf5 / 0.05
        ve = _F["mh458_var_es"](mu_c, sg_c, 0.05)
        assert abs(ve["var"] - var_mano) < 1e-6
        assert abs(ve["es"] - es_mano) < 1e-6
        assert abs(ve["var"] - VAR_WORST) < 1e-6
        assert abs(ve["es"] - ES_WORST) < 1e-6
        # P(perdita) a mano via Phi
        assert abs((1.0 - _F["mh456_phi"](mu_c / sg_c)) -
                   P_PERDITA_WORST) < 1e-9
        # var_unit_worst a mano: per unita' di spread sotto shock
        m = self._m()
        z95 = 1.6448536269514729
        se_star = m["se_star"]
        netto_star = m["netto_star"]
        vuw = -(netto_star - DRIFT * se_star) + z95 * K_VOL * se_star
        assert abs(vuw - VAR_UNIT_WORST) < 1e-9

    def test_chiave_coerenza_tab458(self):
        # scenario BASE == mappa tab458 (1e-9); riuso, nessun duplicato
        m = self._m()
        m458 = _F["mh458_mappa"](self._pw(), self._gs(), z_entry=1.0,
                                 costo=0.20, H=10, capitale=KAP, f_max=0.25,
                                 alpha=0.05, limite=LIMITE)
        base = self._sc(m, "BASE")
        assert abs(base["var"] - m458["var"]) < 1e-9
        assert abs(base["es"] - m458["es"]) < 1e-9
        assert abs(base["p_perdita"] - m458["p_perdita"]) < 1e-12
        assert abs(base["mu_s"] - m458["mu_pnl"]) < 1e-12
        assert abs(base["sigma_s"] - m458["sigma_pnl"]) < 1e-12
        assert abs(m["var"] - m458["var"]) < 1e-12
        # k=1, drift=0 -> tutti gli scenari coincidono col base
        m0 = self._m(k_vol=1.0, drift=0.0)
        assert all(abs(s["var"] - m0["var"]) < 1e-9
                   for s in m0["scenari"])
        assert all(abs(s["es"] - m0["es"]) < 1e-9
                   for s in m0["scenari"])
        assert m0["worst"] == "BASE"
        assert m0["verdetto"].startswith("RESILIENTE")
        assert m0["size_max_stress"] == m0["size"]
        assert m0["f_lim_stress"] == m0["f_app"]

    def test_controlli(self):
        pw, gs = self._pw(), self._gs()
        # z_entry 5.0 -> nessun segnale -> SIZING ZERO, scenari vuoti
        m_ns = self._m(z_entry=5.0)
        assert m_ns["size"] == 0.0
        assert m_ns["scenari"] == [] and m_ns["worst"] is None
        assert m_ns["var_worst"] == 0.0 and m_ns["es_worst"] == 0.0
        assert m_ns["size_max_stress"] == 0.0
        assert m_ns["verdetto"].startswith("SIZING ZERO")
        # costo 10.0 -> netto negativo -> SIZING ZERO
        m_nc = self._m(costo=10.0)
        assert m_nc["verdetto"].startswith("SIZING ZERO")
        # limite enorme -> RESILIENTE, size invariata
        m_ok = self._m(limite=1e9)
        assert m_ok["verdetto"].startswith("RESILIENTE")
        assert m_ok["size_max_stress"] == m_ok["size"]
        assert m_ok["f_lim_stress"] == m_ok["f_app"]
        # limite minuscolo -> OLTRE LIMITE (base gia' oltre), size ridotta
        m_ko = self._m(limite=1000.0)
        assert m_ko["verdetto"].startswith("OLTRE LIMITE")
        assert m_ko["size_max_stress"] < m_ko["size"]
        assert m_ko["f_lim_stress"] < m_ko["f_app"]
        # limite None -> default 2% del capitale
        m_def = _F["mh459_mappa"](pw, gs, limite=None, k_vol=K_VOL,
                                  drift=DRIFT)
        assert abs(m_def["limite"] - 0.02 * KAP) < 1e-9
        # alpha 1% -> VaR/ES peggiori maggiori
        m99 = self._m(alpha=0.01)
        m95 = self._m(alpha=0.05)
        assert m99["var_worst"] > m95["var_worst"]
        assert m99["es_worst"] > m95["es_worst"]
        # monotonia: var_worst cresce con k_vol e con drift
        vs = [self._m(k_vol=k)["var_worst"] for k in (1.0, 1.5, 2.0, 3.0)]
        assert vs == sorted(vs)
        vs2 = [self._m(drift=d)["var_worst"] for d in (0.0, 0.5, 1.0, 2.0)]
        assert vs2 == sorted(vs2)
        # RW indipendenti -> ValueError onesto (rango Johansen != 1)
        with pytest.raises(ValueError):
            _F["mh459_mappa"](_rw(20261014), _rw(777), k_vol=K_VOL,
                              drift=DRIFT)

    def test_verdetto_soglie(self):
        v = _F["mh459_verdetto"]
        assert v(100.0, 100.0, 200.0, 0.05).startswith("RESILIENTE")
        assert v(300.0, 150.0, 200.0, 0.05).startswith("VULNERABILE")
        assert "150" in v(300.0, 150.0, 200.0, 0.05)
        s_ko = v(300.0, 250.0, 200.0, 0.05,
                 size_max_stress=1000.0, f_lim_stress=0.02)
        assert s_ko.startswith("OLTRE LIMITE")
        assert "1,000" in s_ko and "2.00%" in s_ko
        s_ko2 = v(300.0, 250.0, 200.0, 0.01)
        assert s_ko2.startswith("OLTRE LIMITE")
        assert "VaR 99%" in s_ko2
        s_zero = v(0.0, 0.0, 200.0, 0.05, zero_motivo="NESSUN SEGNALE")
        assert s_zero.startswith("SIZING ZERO")
        assert "NESSUN SEGNALE" in s_zero
        # var_worst == limite -> RESILIENTE (soglia inclusiva)
        assert v(200.0, 100.0, 200.0, 0.05).startswith("RESILIENTE")
        # var_base == limite -> VULNERABILE solo se worst oltre
        assert v(250.0, 200.0, 200.0, 0.05).startswith("VULNERABILE")
        for bad in (lambda: v("x", 100.0, 200.0, 0.05),
                    lambda: v(100.0, 100.0, -5.0, 0.05),
                    lambda: v(100.0, 100.0, 0.0, 0.05),
                    lambda: v(100.0, 100.0, 200.0, 0.0),
                    lambda: v(100.0, 100.0, 200.0, 1.0),
                    lambda: v(float("nan"), 100.0, 200.0, 0.05)):
            with pytest.raises(ValueError):
                bad()

    def test_degeneri(self):
        pw, gs = self._pw(), self._gs()
        flat = tuple([5.0] * 40)
        for bad in (lambda: _F["mh459_mappa"](pw, gs, alpha=0.0),
                    lambda: _F["mh459_mappa"](pw, gs, alpha=1.0),
                    lambda: _F["mh459_mappa"](pw, gs, alpha="0.05"),
                    lambda: _F["mh459_mappa"](pw, gs, limite=0.0),
                    lambda: _F["mh459_mappa"](pw, gs, limite=-5.0),
                    lambda: _F["mh459_mappa"](pw, gs, capitale=0.0),
                    lambda: _F["mh459_mappa"](pw, gs, f_max=2.0),
                    lambda: _F["mh459_mappa"](pw, gs, k_vol=0.9),
                    lambda: _F["mh459_mappa"](pw, gs, k_vol=1.0,
                                              drift=-0.1),
                    lambda: _F["mh459_mappa"](pw, gs, k_vol="1.5"),
                    lambda: _F["mh459_mappa"]((1.0,) * 29, (1.0,) * 29),
                    lambda: _F["mh459_mappa"](None, gs),
                    lambda: _F["mh459_mappa"](pw, gs[:50]),
                    lambda: _F["mh459_mappa"](flat, gs),
                    lambda: _F["mh459_mappa"](pw, flat),
                    lambda: _F["mh459_mappa"](pw, gs, beta=float("nan")),
                    lambda: _F["mh459_shock"](1.0, 0.0, 1.5, 0.5),
                    lambda: _F["mh459_shock"](1.0, -2.0, 1.5, 0.5),
                    lambda: _F["mh459_shock"](1.0, 2.0, 0.99, 0.5),
                    lambda: _F["mh459_shock"](1.0, 2.0, 1.5, -0.01),
                    lambda: _F["mh459_num"](float("nan"), "x"),
                    lambda: _F["mh459_num"](True, "x"),
                    lambda: _F["mh459_num"]("1.5", "x")):
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
