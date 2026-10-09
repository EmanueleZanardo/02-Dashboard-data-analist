"""Test tab323 '🔄📉 Half-life di mean reversion: lo spot torna alla media?': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica della mean reversion: validatori,
parse serie, stima OLS di beta (se, t-stat, R2), half-life, verdetto a 3 stati.
"""
import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh323_num", "mh323_parse_serie", "mh323_beta",
           "mh323_half_life", "mh323_risultato", "mh323_verdetto")

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
TITLE322 = "🎯📉 Convergenza forward: il forward indovina lo spot?"
TITLE321 = "🧪📉 Backtest VaR: il modello resiste al tempo?"
SERIE_DEMO = '79.81\n81.48\n93.40\n95.39\n90.10\n86.24\n96.97\n94.32\n87.08\n85.19\n80.96\n87.50\n90.32\n83.94\n85.56\n86.96\n93.54\n99.15\n88.03\n86.26\n88.44\n95.28\n99.54\n86.99\n89.42\n85.97\n89.25\n96.91\n102.51\n102.44\n95.33\n90.81\n85.86\n80.26\n85.01\n91.36\n103.15\n97.06\n102.36\n96.99\n89.46\n82.88\n76.32\n75.04\n75.33\n80.15\n69.20\n72.93'

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N = 48
MEDIA = 88.71770833333333
BETA = -0.2765819440306293
SE = 0.10913133936554696
TSTAT = -2.5343952125813174
R2 = 0.12440563341620703
HL = 2.14087612352128
STATO = "mean reversion RAPIDA"
VERDETTO = 'mean reversion RAPIDA: half-life 2.1 mesi (beta -0.2766, t-stat -2.53, R2 0.12): gli scostamenti dalla media si dimezzano in pochi mesi, picchi e crolli vanno colti in fretta prima del rientro.'


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _ris_demo():
    return _F["mh323_risultato"](SERIE_DEMO)


class TestRegistry323:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 336
        assert TITLE323 in titoli
        assert "tab323" in dvars
        assert "    with tab323:" in src

    def test_titoli_allineati_321_322_323(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab321")] == TITLE321
        assert titoli[dvars.index("tab322")] == TITLE322
        assert titoli[dvars.index("tab323")] == TITLE323

    def test_ultima_tab(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[-1] == TITLE336
        assert dvars[-1] == "tab336"


class TestValidatori:
    def test_num_ok(self):
        assert _F["mh323_num"](3.5, "t") == 3.5
        assert _F["mh323_num"](7, "t") == 7.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh323_num"](bad, "t")

    def test_parse_ok(self):
        vals = _F["mh323_parse_serie"](SERIE_DEMO)
        assert len(vals) == N == 48
        assert all(isinstance(v, float) for v in vals)

    def test_parse_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh323_parse_serie"]("\n".join(["90.0"] * 23))

    def test_parse_ko_numero(self):
        with pytest.raises(ValueError):
            _F["mh323_parse_serie"]("\n".join(["a"] * 24))

    def test_parse_ko_non_testo(self):
        with pytest.raises(ValueError):
            _F["mh323_parse_serie"](None)

    def test_parse_virgola(self):
        vals = _F["mh323_parse_serie"]("\n".join(["90,5"] * 24))
        assert vals[0] == 90.5

    def test_parse_righe_vuote(self):
        txt = "\n\n" + "\n".join(["90.0"] * 24) + "\n\n"
        assert len(_F["mh323_parse_serie"](txt)) == 24


class TestBeta:
    def test_beta_sintetica(self):
        # serie alternata 10/5: mu=7.5, dp = -2*(p_{t-1}-mu) esatto
        vals = _F["mh323_parse_serie"]("\n".join(["10", "5"] * 14))
        st_ = _F["mh323_beta"](vals)
        assert st_["beta"] == pytest.approx(-2.0)
        assert st_["m"] == len(vals) - 1
        assert st_["media"] == pytest.approx(7.5)

    def test_beta_pochi_ko(self):
        with pytest.raises(ValueError):
            _F["mh323_beta"]([1.0] * 23)

    def test_beta_costante_ko(self):
        with pytest.raises(ValueError):
            _F["mh323_beta"]([50.0] * 30)

    def test_beta_demo(self):
        st_ = _F["mh323_beta"](_F["mh323_parse_serie"](SERIE_DEMO))
        assert st_["beta"] == pytest.approx(BETA)
        assert st_["se_beta"] == pytest.approx(SE)
        assert st_["t_stat"] == pytest.approx(TSTAT)
        assert st_["r2"] == pytest.approx(R2)
        assert st_["media"] == pytest.approx(MEDIA)

    def test_t_stat_significativo(self):
        assert TSTAT < -2.0


class TestHalfLife:
    def test_hl_beta_mezza(self):
        assert _F["mh323_half_life"](-0.5) == pytest.approx(1.0)

    def test_hl_random_walk_none(self):
        assert _F["mh323_half_life"](0.0) is None
        assert _F["mh323_half_life"](0.1) is None

    def test_hl_beta_uno_none(self):
        assert _F["mh323_half_life"](-1.0) is None

    def test_hl_demo(self):
        hl = _F["mh323_half_life"](BETA)
        assert hl == pytest.approx(HL)
        assert 1.0 < hl < 3.0


class TestRisultato:
    def test_ris_demo(self):
        ris = _ris_demo()
        assert ris["n"] == N == 48
        assert ris["half_life"] == pytest.approx(HL)
        assert ris["beta"] == pytest.approx(BETA)
        assert ris["media"] == pytest.approx(MEDIA)

    def test_ris_keys(self):
        ris = _ris_demo()
        for k in ("beta", "se_beta", "t_stat", "r2", "m", "media",
                  "n", "half_life"):
            assert k in ris

    def test_verdetto_demo(self):
        ris = _ris_demo()
        verd = _F["mh323_verdetto"](ris)
        assert verd == VERDETTO
        assert verd.startswith(STATO)


class TestVerdetto:
    def test_verdetto_rapida(self):
        ris = {"beta": -0.27, "se_beta": 0.1, "t_stat": -2.7, "r2": 0.1,
               "half_life": 2.1, "m": 47, "media": 85.0, "n": 48}
        assert _F["mh323_verdetto"](ris).startswith("mean reversion RAPIDA")

    def test_verdetto_moderata(self):
        ris = {"beta": -0.13, "se_beta": 0.05, "t_stat": -2.6, "r2": 0.1,
               "half_life": 5.0, "m": 47, "media": 85.0, "n": 48}
        assert _F["mh323_verdetto"](ris).startswith("mean reversion MODERATA")

    def test_verdetto_assente_none(self):
        ris = {"beta": 0.05, "se_beta": 0.05, "t_stat": 1.0, "r2": 0.01,
               "half_life": None, "m": 47, "media": 85.0, "n": 48}
        assert _F["mh323_verdetto"](ris).startswith(
            "mean reversion debole o assente")

    def test_verdetto_assente_t_debole(self):
        ris = {"beta": -0.02, "se_beta": 0.05, "t_stat": -0.4, "r2": 0.01,
               "half_life": 30.0, "m": 47, "media": 85.0, "n": 48}
        assert _F["mh323_verdetto"](ris).startswith(
            "mean reversion debole o assente")
