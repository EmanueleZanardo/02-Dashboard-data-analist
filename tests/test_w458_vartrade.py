"""Test tab458 '⚠️ Quanto posso perdere? VaR del trade dimensionato': registry + funzioni pure."""

import math
import random
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh458_num", "mh458_pdf", "mh458_quantile", "mh458_var_es",
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
TITLE459 = "🧪⚠️ Stress test del trade: VaR sotto shock"
TITLE455 = "🔮 Quando rientra lo spread? Forecast mean-reversion"
TITLE454 = "⚖️ Lo spread è stazionario? Test ADF"
TITLE453 = "📊 Backtest VECM(1): il modello batte il random walk?"
TITLE452 = "📈 Previsione VECM(1): dove vanno power e gas nei prossimi H giorni?"
TITLE451 = "🌊 Spillover gas↔power: chi trasmette e chi riceve gli shock?"
TITLE450 = "📜 Scomposizione storica: cosa ha mosso davvero il prezzo power?"
TITLE449 = "💥 Risposta allo shock: di quanto uno shock del gas muove power?"
TITLE448 = "🔗 ECM: quanto in fretta power torna all'equilibrio col gas?"
DEMO_POWER = '115.0\n114.222584\n115.526527\n115.270435\n115.404795\n113.275972\n114.840219\n116.685764\n115.420859\n113.571058\n112.06301\n112.194403\n116.139654\n117.765956\n116.742831\n116.62762\n115.739526\n117.414453\n114.867579\n116.640701\n115.779325\n115.137451\n116.642853\n117.253244\n117.493738\n117.242796\n118.334843\n119.091227\n116.768615\n115.421416\n116.033447\n114.144567\n113.700317\n114.354433\n114.876507\n113.755332\n115.568524\n116.069102\n116.138549\n117.333173\n117.084818\n116.63492\n117.999467\n117.718767\n117.668152\n118.796536\n116.597527\n114.618757\n114.130273\n116.852609\n116.128887\n119.874946\n118.472635\n119.958398\n119.950907\n122.309881\n121.085938\n120.106701\n119.684133\n119.645704\n'
DEMO_GAS = '40.0\n39.387964\n39.576758\n40.074258\n39.817653\n39.153163\n39.120398\n39.359404\n39.908497\n39.300559\n38.654127\n39.007091\n39.244134\n40.011027\n40.502256\n40.451366\n40.314247\n41.599511\n41.45511\n41.062643\n40.493471\n40.541201\n40.613858\n40.441425\n40.410346\n40.546892\n40.893091\n41.441492\n41.5464\n40.651509\n41.002372\n40.292523\n40.206815\n39.469916\n39.470967\n39.081684\n39.188627\n40.838781\n40.814478\n41.23564\n40.573978\n40.429951\n40.761193\n40.714858\n40.899949\n40.951613\n40.448546\n40.730418\n40.324405\n41.260281\n41.00768\n41.350726\n41.351901\n41.828116\n41.527041\n42.026474\n41.964525\n42.596178\n42.908275\n42.978922\n'
BETA = 1.8286056394998358
Z = -1.0023831726745032
H_STAR = 10
LORDO_STAR = 1.2957345182384756
NETTO_STAR = 1.0957345182384757
PROB_STAR = 0.7951457432835478
F_STAR = 0.6977150281277623
F_APP = 0.25
SIZE = 334704.7264807486
PNL_ATTESO = 366747.52222252387
SE_STAR = 1.3291189023549213
MU_PNL = 366747.52222252387
SIGMA_PNL = 444862.37867309677
VAR = 364985.97483217873
ES = 550875.8038446917
P_PERDITA = 0.2048542567164522
VAR_PCT = 0.36498597483217876
VAR_UNIT = 1.0904715289497753
SIZE_MAX = 18340.68975579935
F_LIM = 0.013699156528683098
KAP = 1000000.0
LIMITE = 20000.0


def _rw(seed, n=60):
    rng = random.Random(seed)
    out = [0.0]
    for _ in range(1, n):
        out.append(out[-1] + rng.gauss(0.0, 1.0))
    return tuple(out)


class TestRegistry458:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 592
        assert "tab458" in dvars
        assert "tab458" in withs

    def test_titoli_allineati_448_449_450_451_452_453_454_455_456_457_458(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
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
        assert titoli[dvars.index("tab458")] == TITLE458

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


class TestVarTrade458:
    def _pw(self):
        return _F["mh456_parse_serie"](DEMO_POWER)

    def _gs(self):
        return _F["mh456_parse_serie"](DEMO_GAS)

    def _m(self, **kw):
        d = dict(z_entry=1.0, costo=0.20, H=10, capitale=KAP,
                 f_max=0.25, alpha=0.05, limite=LIMITE)
        d.update(kw)
        return _F["mh458_mappa"](self._pw(), self._gs(), **d)

    def test_demo_valori(self):
        m = self._m()
        assert m["n"] == 60 and m["H"] == 10 and m["T"] == 59
        assert abs(m["beta"] - BETA) < 1e-12
        assert abs(m["beta"] - 1.8286) < 1e-3  # Johansen tab447
        assert abs(m["z"] - Z) < 1e-12
        assert m["segnale"] is True
        assert m["h_star"] == H_STAR == 10
        assert abs(m["lordo_star"] - LORDO_STAR) < 1e-9
        assert abs(m["netto_star"] - NETTO_STAR) < 1e-9
        assert abs(m["netto_star"] - 1.0957) < 1e-3
        assert abs(m["prob_star"] - PROB_STAR) < 1e-9
        assert abs(m["f_star"] - F_STAR) < 1e-9
        assert abs(m["f_star"] - 0.6977) < 1e-3
        assert abs(m["f_app"] - F_APP) < 1e-12
        assert m["f_app"] == 0.25  # Kelly 69.77% cappato a 25%
        assert abs(m["size"] - SIZE) < 1e-6
        assert abs(m["size"] - 334704.7) < 1.0
        assert abs(m["pnl_atteso"] - PNL_ATTESO) < 1e-6
        assert abs(m["se_star"] - SE_STAR) < 1e-9
        assert abs(m["se_star"] - 1.3291) < 1e-3
        assert abs(m["mu_pnl"] - MU_PNL) < 1e-9
        assert abs(m["sigma_pnl"] - SIGMA_PNL) < 1e-6
        assert abs(m["var"] - VAR) < 1e-6
        assert abs(m["var"] - 364986.0) < 1.0
        assert abs(m["es"] - ES) < 1e-6
        assert abs(m["es"] - 550876.0) < 1.0
        assert m["es"] > m["var"] > 0.0  # coda oltre il VaR
        assert abs(m["p_perdita"] - P_PERDITA) < 1e-9
        assert abs(m["p_perdita"] - 0.2049) < 1e-3
        assert abs(m["var_pct"] - VAR_PCT) < 1e-9
        assert abs(m["var_pct"] - 0.3650) < 1e-3
        assert abs(m["var_unit"] - VAR_UNIT) < 1e-9
        assert abs(m["var_unit"] - 1.0905) < 1e-3
        assert abs(m["limite"] - LIMITE) < 1e-12
        assert abs(m["alpha"] - 0.05) < 1e-12
        assert m["zero_motivo"] is None
        assert m["verdetto"].startswith("OLTRE LIMITE")
        # size massima compatibile col limite: molto sotto la Kelly
        assert abs(m["size_max"] - SIZE_MAX) < 1e-3
        assert abs(m["size_max"] - 18340.7) < 1.0
        assert m["size_max"] < m["size"]
        assert abs(m["f_lim"] - F_LIM) < 1e-9
        assert abs(m["f_lim"] - 0.0137) < 1e-3
        assert m["f_lim"] < m["f_app"]
        assert len(m["var_h"]) == len(m["es_h"]) == \
            len(m["pnl_h"]) == 10
        # VaR/ES DECRESCONO con h sulla demo: l'edge (lordo_h -> |mu-last|)
        # cresce piu' in fretta dell'incertezza di forecast se_h
        assert all(b <= a for a, b in
                   zip(m["var_h"], m["var_h"][1:]))
        assert all(b <= a for a, b in
                   zip(m["es_h"], m["es_h"][1:]))
        assert "18,341" in m["verdetto"] or "18341" in m["verdetto"]

    def test_definizione_a_mano(self):
        # quantile: valori noti della normale standard
        q = _F["mh458_quantile"]
        assert abs(q(0.5) - 0.0) < 1e-12
        assert abs(q(0.05) - (-1.6448536269514729)) < 1e-12
        assert abs(q(0.975) - 1.959963984540054) < 1e-12
        assert abs(q(0.01) - (-2.32634787404084)) < 1e-12
        # pdf: valore noto + simmetria
        assert abs(_F["mh458_pdf"](0.0) - 0.3989422804014327) < 1e-12
        assert abs(_F["mh458_pdf"](1.0) - _F["mh458_pdf"](-1.0)) < 1e-15
        assert _F["mh458_pdf"](2.0) < _F["mh458_pdf"](1.0)
        # var/es a mano: formula indipendente con z noto
        z5 = -1.6448536269514729
        pdf5 = math.exp(-0.5 * z5 * z5) / math.sqrt(2.0 * math.pi)
        var_mano = -(MU_PNL + z5 * SIGMA_PNL)
        es_mano = -MU_PNL + SIGMA_PNL * pdf5 / 0.05
        ve = _F["mh458_var_es"](MU_PNL, SIGMA_PNL, 0.05)
        assert abs(ve["var"] - var_mano) < 1e-6
        assert abs(ve["es"] - es_mano) < 1e-6
        assert abs(ve["z"] - z5) < 1e-9
        # se_star a mano: forecast tab455 sulla spread ricostruita
        pw, gs = self._pw(), self._gs()
        sp = tuple(p - BETA * g for p, g in zip(pw, gs))
        fc = _F["mh455_forecast"](sp, H=10)
        assert abs(fc["se_h"][H_STAR - 1] - SE_STAR) < 1e-9
        # var per unita' a mano
        z95 = 1.6448536269514729
        assert abs((-NETTO_STAR + z95 * SE_STAR) - VAR_UNIT) < 1e-9

    def test_chiave_coerenza_tab457(self):
        # mu_pnl = pnl_atteso, sigma_pnl = size * se_star (stessa spread)
        m = self._m()
        m457 = _F["mh457_mappa"](self._pw(), self._gs(), z_entry=1.0,
                                 costo=0.20, H=10, capitale=KAP, f_max=0.25)
        assert abs(m["mu_pnl"] - m457["pnl_atteso"]) < 1e-12
        assert abs(m["mu_pnl"] - MU_PNL) < 1e-9
        pw, gs = self._pw(), self._gs()
        sp = tuple(p - m457["beta"] * g for p, g in zip(pw, gs))
        fc = _F["mh455_forecast"](sp, H=10)
        assert abs(m["sigma_pnl"] -
                   m457["size"] * fc["se_h"][m457["h_star"] - 1]) < 1e-9
        assert abs(m["p_perdita"] - (1.0 - m457["p"])) < 1e-12
        assert abs(m["var_pct"] - m["var"] / KAP) < 1e-15
        # var/es identici alla formula diretta su (mu_pnl, sigma_pnl)
        ve = _F["mh458_var_es"](m["mu_pnl"], m["sigma_pnl"], 0.05)
        assert abs(m["var"] - ve["var"]) < 1e-9
        assert abs(m["es"] - ve["es"]) < 1e-9

    def test_controlli(self):
        pw, gs = self._pw(), self._gs()
        # z_entry 5.0 -> nessun segnale -> SIZING ZERO
        m_ns = _F["mh458_mappa"](pw, gs, z_entry=5.0, costo=0.20, H=10,
                                 capitale=KAP, f_max=0.25, alpha=0.05,
                                 limite=LIMITE)
        assert m_ns["size"] == 0.0
        assert m_ns["var"] == 0.0 and m_ns["es"] == 0.0
        assert m_ns["verdetto"].startswith("SIZING ZERO")
        # costo 10.0 -> netto negativo -> SIZING ZERO
        m_nc = _F["mh458_mappa"](pw, gs, z_entry=1.0, costo=10.0, H=10,
                                 capitale=KAP, f_max=0.25, alpha=0.05,
                                 limite=LIMITE)
        assert m_nc["verdetto"].startswith("SIZING ZERO")
        # limite enorme -> ENTRO LIMITE, size invariata
        m_ok = _F["mh458_mappa"](pw, gs, limite=1e9)
        assert m_ok["verdetto"].startswith("ENTRO LIMITE")
        assert m_ok["size_max"] == m_ok["size"]
        assert m_ok["f_lim"] == m_ok["f_app"]
        # limite minuscolo -> OLTRE LIMITE, size ridotta
        m_ko = _F["mh458_mappa"](pw, gs, limite=1000.0)
        assert m_ko["verdetto"].startswith("OLTRE LIMITE")
        assert m_ko["size_max"] < m_ko["size"]
        assert m_ko["f_lim"] < m_ko["f_app"]
        # limite None -> default 2% del capitale
        m_def = _F["mh458_mappa"](pw, gs, limite=None)
        assert abs(m_def["limite"] - 0.02 * KAP) < 1e-9
        # alpha 1% -> VaR/ES maggiori dell'alpha 5%
        m99 = self._m(alpha=0.01)
        m95 = self._m(alpha=0.05)
        assert m99["var"] > m95["var"]
        assert m99["es"] > m95["es"]
        assert m99["verdetto"].startswith("OLTRE LIMITE")
        # RW indipendenti -> ValueError onesto (rango Johansen != 1)
        with pytest.raises(ValueError):
            _F["mh458_mappa"](_rw(20261014), _rw(777))

    def test_verdetto_soglie(self):
        v = _F["mh458_verdetto"]
        assert v(100.0, 200.0, 0.05).startswith("ENTRO LIMITE")
        assert "100" in v(100.0, 200.0, 0.05)
        s_ko = v(300.0, 200.0, 0.05, size_max=1000.0, f_lim=0.02)
        assert s_ko.startswith("OLTRE LIMITE")
        assert "1,000" in s_ko and "2.00%" in s_ko
        s_ko2 = v(300.0, 200.0, 0.01)
        assert s_ko2.startswith("OLTRE LIMITE")
        assert "VaR 99%" in s_ko2
        s_zero = v(0.0, 200.0, 0.05, zero_motivo="NESSUN SEGNALE")
        assert s_zero.startswith("SIZING ZERO")
        assert "NESSUN SEGNALE" in s_zero
        # var == limite -> ENTRO LIMITE (soglia inclusiva)
        assert v(200.0, 200.0, 0.05).startswith("ENTRO LIMITE")
        for bad in (lambda: v("x", 200.0, 0.05),
                    lambda: v(100.0, -5.0, 0.05),
                    lambda: v(100.0, 0.0, 0.05),
                    lambda: v(100.0, 200.0, 0.0),
                    lambda: v(100.0, 200.0, 1.0),
                    lambda: v(float("nan"), 200.0, 0.05)):
            with pytest.raises(ValueError):
                bad()

    def test_degeneri(self):
        pw, gs = self._pw(), self._gs()
        flat = tuple([5.0] * 40)
        for bad in (lambda: _F["mh458_mappa"](pw, gs, alpha=0.0),
                    lambda: _F["mh458_mappa"](pw, gs, alpha=1.0),
                    lambda: _F["mh458_mappa"](pw, gs, alpha=-0.05),
                    lambda: _F["mh458_mappa"](pw, gs, alpha="0.05"),
                    lambda: _F["mh458_mappa"](pw, gs, limite=0.0),
                    lambda: _F["mh458_mappa"](pw, gs, limite=-5.0),
                    lambda: _F["mh458_mappa"](pw, gs, limite="x"),
                    lambda: _F["mh458_mappa"](pw, gs, capitale=0.0),
                    lambda: _F["mh458_mappa"](pw, gs, f_max=2.0),
                    lambda: _F["mh458_mappa"]((1.0,) * 29, (1.0,) * 29),
                    lambda: _F["mh458_mappa"](None, gs),
                    lambda: _F["mh458_mappa"](pw, gs[:50]),
                    lambda: _F["mh458_mappa"](flat, gs),
                    lambda: _F["mh458_mappa"](pw, flat),
                    lambda: _F["mh458_mappa"](pw, gs, beta=float("nan")),
                    lambda: _F["mh458_quantile"](0.0),
                    lambda: _F["mh458_quantile"](1.0),
                    lambda: _F["mh458_quantile"]("0.5"),
                    lambda: _F["mh458_var_es"](1.0, 0.0, 0.05),
                    lambda: _F["mh458_var_es"](1.0, -2.0, 0.05),
                    lambda: _F["mh458_var_es"](1.0, 2.0, 0.0),
                    lambda: _F["mh458_num"](float("nan"), "x"),
                    lambda: _F["mh458_num"](True, "x"),
                    lambda: _F["mh458_num"]("1.5", "x")):
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
