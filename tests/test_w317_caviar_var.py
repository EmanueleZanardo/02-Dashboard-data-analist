"""Test tab317 '🧠📉 CAViaR: il VaR adattivo che impara dai rendimenti': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica CAViaR: ricorsione del quantile,
tick loss asimmetrico, stima coordinate-descent con vincoli, flag eccezioni,
hit-rate, confronto col VaR statico, forecast a 1 giorno, verdetto a 5 stati.
"""
import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh317_num", "mh317_conf", "mh317_parse_serie",
           "mh317_quantile_empirico", "mh317_var_path", "mh317_tick_loss",
           "mh317_stima", "mh317_hit", "mh317_var_statico",
           "mh317_var_domani", "mh317_risultato", "mh317_verdetto")

TITLE317 = "🧠📉 CAViaR: il VaR adattivo che impara dai rendimenti"
TITLE318 = "🌀📉 Copula t-Student: il VaR che vede le code muoversi insieme"
TITLE319 = "🎛📉 FHS: il VaR con la volatilita' di oggi"
TITLE320 = "⚙️📉 GARCH(1,1): la volatilita' che ricorda"
TITLE321 = "🧪📉 Backtest VaR: il modello resiste al tempo?"
TITLE322 = "🎯📉 Convergenza forward: il forward indovina lo spot?"
TITLE323 = "🔄📉 Half-life di mean reversion: lo spot torna alla media?"
TITLE324 = "Ω📊 Omega ratio: oltre Sharpe e Sortino"
TITLE325 = "📈📉 Calmar ratio: il rendimento che paga il drawdown"
TITLE326 = "🩹 Pain index e Pain ratio: il dolore medio oltre il peggio"
TITLE327 = "🛟 Sterling ratio: il Calmar mediato sui peggiori drawdown"
TITLE328 = "🔻 Burke ratio: il drawdown penalizzato al quadrato"
TITLE329 = "🌊📉 CDaR: il drawdown medio oltre la soglia (il VaR dei drawdown)"
TITLE330 = "🔍📉 Martin ratio: il Calmar che guarda tutto il dolore"
TITLE331 = "⛵ Tempo di recupero: quanto resta sott'acqua l'equity"
TITLE332 = "🎯 Information ratio: la strategia batte davvero il benchmark?"
TITLE333 = "📊 Capture ratio: quanto cattura la strategia nei mercati su e giù?"
TITLE334 = "🎯 Hit rate: quanto spesso la strategia batte il benchmark?"
TITLE335 = "📏 Tracking error: quanto si discosta la strategia dal benchmark?"
TITLE336 = "📉 Max drawdown relativo: quanto si scende sotto il benchmark?"
TITLE337 = "📐 Treynor & Jensen: il premio per unita' di rischio sistematico"
TITLE338 = "⚖️ M² Modigliani: il rendimento a parita' di rischio col benchmark"
TITLE339 = "📉 Sortino ratio: il rendimento per unità di rischio al ribasso"
TITLE340 = "📉 Calmar ratio: il rendimento annuo per unità di max drawdown"
TITLE341 = "📐 K-ratio: la regolarità della crescita dell'equity"
TITLE342 = "🎯 Volatilità target: il sizing a volatilità costante"
TITLE343 = "📐 Kelly criterion: il sizing ottimale dall'edge stimato"
TITLE344 = "🎲 Risk of ruin: probabilita' di toccare una barriera di drawdown"
TITLE345 = "🎯 Sizing anti-rovina: f massima con ROR vincolato"
TITLE346 = "📊 Monte Carlo: distribuzione del capitale dopo N trade"
TITLE347 = "VaR & Expected Shortfall del P&L dopo N trade"
TITLE348 = "Kelly con costi di trading: sizing netto"
TITLE349 = "Frazione di Kelly: half-Kelly e trade-off crescita/volatilità"
TITLE350 = "Kelly robusto: sizing con edge incerta"
TITLE351 = "Kelly con portafoglio: due posizioni simultanee"
TITLE352 = "Kelly con correlazione: due posizioni correlate"
TITLE353 = "Kelly adattivo: win-rate rolling e size dinamica"
TITLE354 = "Kelly con controllo drawdown: sizing frazionato al drawdown"
TITLE355 = "Kelly con target di volatilità: sizing riscalato sulla vol"
TITLE356 = "Kelly bayesiano: sizing con win-rate posterior"
TITLE357 = "Kelly con lotti interi: sizing discreto e drag di arrotondamento"
TITLE358 = "Kelly con stop-loss: sizing con perdita troncata"
TITLE359 = "Kelly con take-profit: sizing con vincita troncata"
TITLE360 = "Kelly frazionario (fractional Kelly): λ·f*"
TITLE361 = "Rischio di rovina (risk of ruin): probabilita' di rovina prima del target"
TITLE362 = "Kelly con tre esiti: sizing con vincita, perdita parziale e perdita piena"
TITLE363 = "Kelly con limite di posizione: sizing con cap f_max"
TITLE364 = "Kelly con vincoli multipli: cap, lotti, stop e drawdown"
TITLE365 = "Kelly con incertezza: haircut bayesiano sulla p stimata"
TITLE366 = "Kelly su N trade: raddoppio, dimezzamento e crescita attesa"
TITLE367 = "Kelly: mappa di sensibilità f* e crescita su (p, b)"
TITLE368 = "Kelly su ritorni continui: f* = μ/σ² e volatility drag"
TITLE369 = "Kelly con costi di transazione: f* netto = (μ-c)/σ²"
TITLE316 = "🌊📉 POT-GPD: il VaR dalla coda paretiana oltre soglia"
TITLE315 = "🏔️📉 Valori estremi (Hill): il VaR oltre il massimo storico"
SERIE_DEMO = '-85 -708 -309 119 -352 -344 39 -712 -119 -879\n-394 -326 811 -297 738 -971 138 1071 618 1165\n-872 371 -1866 -285 -494 381 264 347 -1447 -891\n-17 85 1552 -424 585 -279 1140 -810 32 -633\n257 -443 -477 -251 508 -161 -93 544 85 452\n-112 160 248 -93 -160 -172 -36 26 -146 252\n434 -73 -25 -470 276 196 81 -616 -621 -929\n-150 -913 -86 542 -313 -258 844 -887 1256 -406\n889 156 178 304 -277 48 -470 153 -218 -1412\n-402 -226 -833 115 288 10 -160 345 741 -303\n852 -74 -141 433 -622 28 -549 -374 -382 267\n81 585 -455 -372 -416 71 551 -214 745 -42\n-57 71 -674 -2 -199 430 137 154 665 83\n234 535 373 392 192 -563 888 -894 126 343\n467 1064 322 -445 131 -284 147 586 -189 348\n-600 -145 27 255 -200 516 282 328 -291 -335\n-247 181 -43 381 111 -215 -141 342 19 -286\n201 -420 -229 243 -257 125 563 556 -620 -49\n-185 196 550 -235 -258 -971 1487 1493 837 -925\n1252 647 277 -770 -84 -531 -467 400 -24 -52\n-319 277 427 -229 -41 -335 96 -85 97 139\n-30 -311 -104 66 186 21 3 447 -258 161\n-193 -671 4 282 517 174 222 -262 -127 412\n-448 214 340 -90 -137 478 85 273 80 214\n-7 109 -123 -493 307 303 282 286 -432 -600\n-206 214 -239 191 -184 108 98 -227 412 -208\n-19 -357 -261 198 336 -503 998 -642 -591 -606\n-13 216 -582 -54 -942 -264 406 -140 -296 -470\n-630 856 527 -310 -408 339 -668 98 386 82\n-112 419 555 317 292 -742 -642 71 144 416'
Q_DEMO = 99.0

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N_DEMO = 300
B0 = -536.2790368041982
B1 = 0.6201989746093748
B2 = 3.8146972652780554e-08
LOSS_CAV = 15.68459541973728
LOSS_STAT = 15.708333333333343
MIGL = 0.0015111669132772424
X_DEMO = 3
HIT_RATE = 0.01
VAR_DOMANI = -1411.9999343096817
VAR_STATICO = -975.4099999999987
STATO = "miglioramento modesto"
VERDETTO = "miglioramento modesto: tick loss -0.2% vs statico, hit-rate 1.00% (atteso 1.0%): il regime e' stabile, lo statico basta."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _ris_demo():
    return _F["mh317_risultato"](SERIE_DEMO, Q_DEMO, "accurata")


class TestRegistry317:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 369
        assert TITLE317 in titoli
        assert "tab317" in dvars
        assert "    with tab317:" in src

    def test_titoli_allineati_315_316_317(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab315")] == TITLE315
        assert titoli[dvars.index("tab316")] == TITLE316
        assert titoli[dvars.index("tab317")] == TITLE317

    def test_ultima_tab(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[-1] == TITLE369
        assert dvars[-1] == "tab369"


class TestValidatori:
    def test_conf_ok(self):
        assert _F["mh317_conf"](95.0) == pytest.approx(0.05)
        assert _F["mh317_conf"](99.0) == pytest.approx(0.01)

    def test_conf_ko(self):
        with pytest.raises(ValueError):
            _F["mh317_conf"](97)
        with pytest.raises(ValueError):
            _F["mh317_conf"]("99")

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh317_num"](True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh317_num"](float("nan"), "x")


class TestParse:
    def test_parse_serie_ok(self):
        vals = _F["mh317_parse_serie"](" ".join(["10"] * 50))
        assert vals == [10.0] * 50

    def test_parse_serie_separators(self):
        a = _F["mh317_parse_serie"]("1;2 3\n4 " + "5 " * 50)
        b = _F["mh317_parse_serie"]("1 2 3 4 " + "5 " * 50)
        assert a == b

    def test_parse_serie_virgola_decimale(self):
        assert _F["mh317_parse_serie"](("1,5 " * 50).strip()) == [1.5] * 50

    def test_parse_serie_corta_ko(self):
        with pytest.raises(ValueError):
            _F["mh317_parse_serie"](" ".join(["1"] * 49))

    def test_parse_serie_testo_ko(self):
        with pytest.raises(ValueError):
            _F["mh317_parse_serie"](42)


class TestQuantile:
    def test_quantile_mediana(self):
        assert _F["mh317_quantile_empirico"]([1.0, 2.0, 3.0], 0.5) == 2.0

    def test_quantile_interpola(self):
        assert _F["mh317_quantile_empirico"]([0.0, 10.0], 0.25) == 2.5

    def test_quantile_bounds_ko(self):
        with pytest.raises(ValueError):
            _F["mh317_quantile_empirico"]([1.0], 0.0)


class TestVarPath:
    def test_ricorsione_manuale(self):
        r = [100.0, -200.0, 50.0, -300.0, 80.0]
        qp = _F["mh317_var_path"](r, -50.0, 0.9, 0.1)
        assert len(qp) == len(r)
        q0 = _F["mh317_quantile_empirico"](r, 0.01)
        assert qp[0] == pytest.approx(-50.0 + 0.9 * q0 + 0.1 * 100.0)
        assert qp[1] == pytest.approx(-50.0 + 0.9 * qp[0] + 0.1 * 200.0)

    def test_corta_ko(self):
        with pytest.raises(ValueError):
            _F["mh317_var_path"]([1.0], 0.0, 0.5, 0.1)


class TestTickLoss:
    def test_tick_loss_manuale(self):
        r = [10.0, -30.0]
        qp = [-20.0, -20.0]
        # u = 30 -> 30*(0.01-0) = 0.3 ; u = -10 -> -10*(0.01-1) = 9.9
        assert _F["mh317_tick_loss"](r, qp, 0.01) == pytest.approx(5.1)

    def test_tick_loss_cresce_con_distanza(self):
        r = [0.0]
        a = _F["mh317_tick_loss"](r, [-10.0], 0.01)
        b = _F["mh317_tick_loss"](r, [-100.0], 0.01)
        assert b > a

    def test_tick_loss_lunghezze_ko(self):
        with pytest.raises(ValueError):
            _F["mh317_tick_loss"]([1.0, 2.0], [-1.0], 0.01)


class TestStima:
    def test_stima_vincoli(self):
        r = _F["mh317_parse_serie"](SERIE_DEMO)
        b0, b1, b2, loss = _F["mh317_stima"](r, 0.01, sweeps=10)
        assert b0 <= 0.0
        assert 0.0 <= b1 <= 0.995
        assert b2 >= 0.0
        assert loss > 0.0

    def test_stima_batte_statico_demo(self):
        r = _F["mh317_parse_serie"](SERIE_DEMO)
        b0, b1, b2, loss = _F["mh317_stima"](r, 0.01, sweeps=60)
        qp = _F["mh317_var_path"](r, b0, b1, b2)
        assert loss == pytest.approx(LOSS_CAV)
        vs = _F["mh317_var_statico"](r, 0.01)
        loss_stat = _F["mh317_tick_loss"](r, [vs] * len(r), 0.01)
        assert loss <= loss_stat


class TestHit:
    def test_hit_manuale(self):
        assert _F["mh317_hit"]([10.0, -30.0, -20.0], [-20.0, -20.0, -20.0]) == [0, 1, 0]

    def test_hit_demo(self):
        ris = _ris_demo()
        assert ris["x"] == X_DEMO
        assert ris["hit_rate"] == HIT_RATE
        assert sum(ris["flags"]) == ris["x"]


class TestRisultato:
    def test_risultato_demo(self):
        ris = _ris_demo()
        assert ris["n"] == N_DEMO == 300
        assert ris["b0"] == B0
        assert ris["b1"] == B1
        assert ris["b2"] == B2
        assert ris["loss_cav"] == LOSS_CAV
        assert ris["loss_stat"] == LOSS_STAT
        assert ris["migl"] == MIGL
        assert ris["var_domani"] == VAR_DOMANI
        assert ris["var_statico"] == VAR_STATICO
        assert ris["var_domani"] < 0.0

    def test_var_domani_coerente(self):
        ris = _ris_demo()
        r = _F["mh317_parse_serie"](SERIE_DEMO)
        qp = _F["mh317_var_path"](r, ris["b0"], ris["b1"], ris["b2"])
        assert ris["var_domani"] == pytest.approx(
            ris["b0"] + ris["b1"] * qp[-1] + ris["b2"] * abs(r[-1]))


class TestVerdetto:
    def test_verdetto_demo(self):
        assert _F["mh317_verdetto"](_ris_demo()) == VERDETTO
        assert STATO in VERDETTO

    def _base(self, **kw):
        ris = _ris_demo()
        ris.update(kw)
        return ris

    def test_stato_sottostimato(self):
        v = _F["mh317_verdetto"](self._base(x=10, hit_rate=10 / 300,
                                            loss_cav=1.0, loss_stat=1.0,
                                            migl=0.0))
        assert v.startswith("VaR sottostimato")

    def test_stato_conservativo(self):
        v = _F["mh317_verdetto"](self._base(x=0, hit_rate=0.0))
        assert v.startswith("VaR troppo conservativo")

    def test_stato_adattivo(self):
        v = _F["mh317_verdetto"](self._base(migl=0.25, hit_rate=0.01))
        assert v.startswith("CAViaR adattivo")

    def test_stato_modesto(self):
        v = _F["mh317_verdetto"](self._base(migl=0.05, hit_rate=0.01))
        assert v.startswith("miglioramento modesto")

    def test_stato_nessuno(self):
        v = _F["mh317_verdetto"](
            self._base(migl=0.0, hit_rate=0.01, loss_cav=5.0, loss_stat=5.0))
        assert v.startswith("nessun miglioramento")
