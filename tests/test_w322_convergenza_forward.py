"""Test tab322 '🎯📉 Convergenza forward: il forward indovina lo spot?': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica della convergenza forward: validatori,
parse coppie, errori, bias, RMSE, MAE, hit rate, premio %, t-stat del bias,
verdetto a 3 stati.
"""
import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh322_num", "mh322_parse_coppie", "mh322_errori", "mh322_bias",
           "mh322_rmse", "mh322_mae", "mh322_hit", "mh322_premio_pct",
           "mh322_risultato", "mh322_verdetto")

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
TITLE321 = "🧪📉 Backtest VaR: il modello resiste al tempo?"
TITLE320 = "⚙️📉 GARCH(1,1): la volatilita' che ricorda"
COPPIE_DEMO = '106.93;116.98\n107.84;99.26\n101.46;97.31\n88.64;90.64\n78.61;68.61\n67.77;69.39\n70.00;69.14\n68.48;69.67\n78.87;85.82\n92.17;86.39\n104.68;98.48\n105.29;108.10\n107.33;106.83\n106.99;117.16\n98.01;90.92\n95.39;75.36\n80.48;82.50\n68.78;53.28\n67.03;47.34\n71.72;65.30\n76.58;63.33\n94.04;69.27\n100.38;106.04\n106.42;102.37'

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N = 24
BIAS = 4.3500000000000005
RMSE = 10.1952047551778
MAE = 7.889166666666665
HIT = 0.625
PREMIO = 7.321136840834128
TSTAT = 2.0902533371280003
STATO = "premio forward sistematico"
VERDETTO = 'premio forward sistematico: bias +4.35 €/MWh (t-stat 2.09 su 24 mesi): il forward quota sistematicamente sopra lo spot realizzato, il mercato paga un premio per la certezza del prezzo.'

def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _ris_demo():
    return _F["mh322_risultato"](COPPIE_DEMO)


class TestRegistry322:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 362
        assert TITLE322 in titoli
        assert "tab322" in dvars
        assert "    with tab322:" in src

    def test_titoli_allineati_320_321_322(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab320")] == TITLE320
        assert titoli[dvars.index("tab321")] == TITLE321
        assert titoli[dvars.index("tab322")] == TITLE322

    def test_ultima_tab(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[-1] == TITLE362
        assert dvars[-1] == "tab362"


class TestValidatori:
    def test_num_ok(self):
        assert _F["mh322_num"](3.5, "t") == 3.5
        assert _F["mh322_num"](7, "t") == 7.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh322_num"](bad, "t")

    def test_parse_ok(self):
        coppie = _F["mh322_parse_coppie"](COPPIE_DEMO)
        assert len(coppie) == N == 24
        assert all(isinstance(f, float) and isinstance(s, float)
                   for f, s in coppie)

    def test_parse_ko_poche(self):
        with pytest.raises(ValueError):
            _F["mh322_parse_coppie"]("\n".join(["90.0;80.0"] * 11))

    def test_parse_ko_campi(self):
        with pytest.raises(ValueError):
            _F["mh322_parse_coppie"]("\n".join(["90.0"] * 12))
        with pytest.raises(ValueError):
            _F["mh322_parse_coppie"]("\n".join(["90.0;80.0;70.0"] * 12))

    def test_parse_ko_numero(self):
        with pytest.raises(ValueError):
            _F["mh322_parse_coppie"]("\n".join(["a;b"] * 12))

    def test_parse_ko_non_testo(self):
        with pytest.raises(ValueError):
            _F["mh322_parse_coppie"](None)

    def test_parse_virgola(self):
        coppie = _F["mh322_parse_coppie"]("\n".join(["90,5;80,25"] * 12))
        assert coppie[0] == (90.5, 80.25)

    def test_parse_righe_vuote(self):
        txt = "\n\n" + "\n".join(["90.0;80.0"] * 12) + "\n\n"
        assert len(_F["mh322_parse_coppie"](txt)) == 12


class TestErrori:
    def test_errori_noti(self):
        assert _F["mh322_errori"]([(100.0, 90.0), (80.0, 85.0)]) == [10.0, -5.0]

    def test_errori_vuoti_ko(self):
        with pytest.raises(ValueError):
            _F["mh322_errori"]([])

    def test_bias_noto(self):
        assert _F["mh322_bias"]([10.0, -5.0, 4.0]) == pytest.approx(3.0)

    def test_bias_vuoto_ko(self):
        with pytest.raises(ValueError):
            _F["mh322_bias"]([])

    def test_rmse_noto(self):
        assert _F["mh322_rmse"]([3.0, 4.0]) == pytest.approx(math.sqrt(12.5))

    def test_rmse_zero(self):
        assert _F["mh322_rmse"]([0.0, 0.0]) == 0.0

    def test_rmse_vuoto_ko(self):
        with pytest.raises(ValueError):
            _F["mh322_rmse"]([])

    def test_mae_noto(self):
        assert _F["mh322_mae"]([3.0, -4.0]) == pytest.approx(3.5)

    def test_mae_vuoto_ko(self):
        with pytest.raises(ValueError):
            _F["mh322_mae"]([])

    def test_hit_noto(self):
        assert _F["mh322_hit"]([(100.0, 90.0), (80.0, 80.0),
                                (70.0, 75.0)]) == pytest.approx(1.0 / 3.0)

    def test_hit_estremi(self):
        assert _F["mh322_hit"]([(2.0, 1.0)] * 12) == 1.0
        assert _F["mh322_hit"]([(1.0, 2.0)] * 12) == 0.0

    def test_hit_vuoto_ko(self):
        with pytest.raises(ValueError):
            _F["mh322_hit"]([])

    def test_premio_pct_noto(self):
        assert _F["mh322_premio_pct"]([(110.0, 100.0),
                                       (90.0, 100.0)]) == pytest.approx(0.0)

    def test_premio_vuoto_ko(self):
        with pytest.raises(ValueError):
            _F["mh322_premio_pct"]([])


class TestRisultato:
    def _ris_demo(self):
        return _F["mh322_risultato"](COPPIE_DEMO)

    def test_risultato_demo(self):
        ris = self._ris_demo()
        assert ris["n"] == N == 24
        assert ris["bias"] == BIAS
        assert ris["rmse"] == RMSE
        assert ris["mae"] == MAE
        assert ris["hit"] == HIT
        assert ris["premio_pct"] == PREMIO
        assert ris["t_stat"] == TSTAT
        assert len(ris["errori"]) == N
        assert len(ris["coppie"]) == N

    def test_coerenza_interna(self):
        ris = self._ris_demo()
        assert sum(ris["errori"]) == pytest.approx(ris["n"] * ris["bias"])
        assert ris["rmse"] >= ris["mae"] >= 0.0
        assert 0.0 <= ris["hit"] <= 1.0
        assert ris["t_stat"] == pytest.approx(
            ris["bias"] / (ris["rmse"] / math.sqrt(ris["n"])))

    def test_demo_bias_positivo_significativo(self):
        assert BIAS > 0.0
        assert TSTAT > 2.0
        assert HIT > 0.5
        assert PREMIO > 0.0


class TestVerdetto:
    def _base(self, **kw):
        return {"n": 24, "bias": 5.0, "t_stat": 3.0, **kw}

    def test_verdetto_demo(self):
        ris = _F["mh322_risultato"](COPPIE_DEMO)
        assert _F["mh322_verdetto"](ris) == VERDETTO
        assert STATO in VERDETTO

    def test_stato_premio(self):
        v = _F["mh322_verdetto"](self._base())
        assert v.startswith("premio forward sistematico")

    def test_stato_sconto(self):
        v = _F["mh322_verdetto"](self._base(bias=-4.0, t_stat=-3.0))
        assert v.startswith("sconto forward sistematico")

    def test_stato_imparziale(self):
        v = _F["mh322_verdetto"](self._base(bias=0.5, t_stat=0.4))
        assert v.startswith("forward imparziale")

    def test_verdetto_bordi(self):
        assert _F["mh322_verdetto"](
            self._base(bias=3.0, t_stat=2.0)).startswith("forward imparziale")
        assert _F["mh322_verdetto"](
            self._base(bias=3.0, t_stat=2.01)).startswith(
            "premio forward sistematico")
        assert _F["mh322_verdetto"](
            self._base(bias=-3.0, t_stat=-2.0)).startswith("forward imparziale")

