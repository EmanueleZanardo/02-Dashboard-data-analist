"""Test tab324 'Ω📊 Omega ratio: oltre Sharpe e Sortino': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica dell'Omega ratio: validatori,
parse rendimenti, omega(T) con gestione inf/degenere, statistiche di base,
curva su 21 soglie, verdetto a 3 stati.
"""
import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh324_num", "mh324_parse_serie", "mh324_omega", "mh324_stat",
           "mh324_curva", "mh324_verdetto")

TITLE324 = "Ω📊 Omega ratio: oltre Sharpe e Sortino"
TITLE325 = "📈📉 Calmar ratio: il rendimento che paga il drawdown"
TITLE326 = "🩹 Pain index e Pain ratio: il dolore medio oltre il peggio"
TITLE327 = "🛟 Sterling ratio: il Calmar mediato sui peggiori drawdown"
TITLE328 = "🔻 Burke ratio: il drawdown penalizzato al quadrato"
TITLE329 = "🌊📉 CDaR: il drawdown medio oltre la soglia (il VaR dei drawdown)"
TITLE330 = "🔍📉 Martin ratio: il Calmar che guarda tutto il dolore"
TITLE331 = "⛵ Tempo di recupero: quanto resta sott'acqua l'equity"
TITLE332 = "🎯 Information ratio: la strategia batte davvero il benchmark?"
TITLE323 = "🔄📉 Half-life di mean reversion: lo spot torna alla media?"
TITLE322 = "🎯📉 Convergenza forward: il forward indovina lo spot?"
SERIE_DEMO = '1.2\n-0.8\n2.1\n0.5\n-1.5\n3.2\n0.8\n-2.2\n1.7\n5.4\n0.3\n-1.1\n2.6\n1.1\n-0.6\n4.1\n0.9\n-1.8\n2.3\n0.4\n6.2\n-0.9\n1.5\n2.8\n-2.5\n1.0\n0.7\n-1.2\n3.6\n1.4\n-0.4\n2.0\n0.6\n-1.6\n4.8\n1.9'

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N = 36
MEDIA = 1.0694444444444444
VOL = 2.1293620029676825
SHARPE = 0.5022370282525772
OMEGA0 = 3.636986301369863
MINR = -2.5
MAXR = 6.2
PCTPOS = 69.44444444444444
STATO = "asimmetria FORTEMENTE positiva"
VERDETTO = "asimmetria FORTEMENTE positiva: Omega(0) 3.64 (Sharpe 0.50): i guadagni sopra lo zero dominano le perdite, la strategia ha code destre grasse: il rischio di coda e' contenuto rispetto al potenziale."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _rets_demo():
    return _F["mh324_parse_serie"](SERIE_DEMO)


class TestRegistry324:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 332
        assert TITLE324 in titoli
        assert "tab324" in dvars
        assert "    with tab324:" in src

    def test_titoli_allineati_322_323_324(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab322")] == TITLE322
        assert titoli[dvars.index("tab323")] == TITLE323
        assert titoli[dvars.index("tab324")] == TITLE324

    def test_ultima_tab(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[-1] == TITLE332
        assert dvars[-1] == "tab332"


class TestValidatori:
    def test_num_ok(self):
        assert _F["mh324_num"](3.5, "t") == 3.5
        assert _F["mh324_num"](0, "t") == 0.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh324_num"](bad, "t")

    def test_parse_ok(self):
        vals = _F["mh324_parse_serie"](SERIE_DEMO)
        assert len(vals) == N == 36
        assert all(isinstance(v, float) for v in vals)

    def test_parse_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh324_parse_serie"]("\n".join(["1.0"] * 19))

    def test_parse_ko_numero(self):
        with pytest.raises(ValueError):
            _F["mh324_parse_serie"]("\n".join(["a"] * 20))

    def test_parse_ko_non_testo(self):
        with pytest.raises(ValueError):
            _F["mh324_parse_serie"](None)

    def test_parse_virgola(self):
        vals = _F["mh324_parse_serie"]("\n".join(["1,5"] * 20))
        assert vals[0] == 1.5

    def test_parse_righe_vuote(self):
        txt = "\n\n" + "\n".join(["1.0"] * 20) + "\n\n"
        assert len(_F["mh324_parse_serie"](txt)) == 20


class TestOmega:
    def test_omega_simmetrico(self):
        assert _F["mh324_omega"]([-2.0, -1.0, 1.0, 2.0], 0.0) == pytest.approx(1.0)

    def test_omega_tutti_positivi_inf(self):
        assert math.isinf(_F["mh324_omega"]([1.0, 2.0, 3.0], 0.0))

    def test_omega_degenere_ko(self):
        with pytest.raises(ValueError):
            _F["mh324_omega"]([0.0] * 20, 0.0)

    def test_omega_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh324_omega"]([], 0.0)

    def test_omega_non_crescente_in_soglia(self):
        rets = _rets_demo()
        o1 = _F["mh324_omega"](rets, -2.0)
        o2 = _F["mh324_omega"](rets, 0.0)
        o3 = _F["mh324_omega"](rets, 2.0)
        assert o1 >= o2 >= o3

    def test_omega_demo(self):
        assert _F["mh324_omega"](_rets_demo(), 0.0) == pytest.approx(OMEGA0)
        assert OMEGA0 > 1.0
        assert not math.isinf(OMEGA0)


class TestStat:
    def test_stat_demo(self):
        st_ = _F["mh324_stat"](_rets_demo())
        assert st_["n"] == N == 36
        assert st_["media"] == pytest.approx(MEDIA)
        assert st_["vol"] == pytest.approx(VOL)
        assert st_["sharpe"] == pytest.approx(SHARPE)
        assert st_["min"] == pytest.approx(MINR)
        assert st_["max"] == pytest.approx(MAXR)
        assert st_["pct_pos"] == pytest.approx(PCTPOS)
        assert st_["omega0"] == pytest.approx(OMEGA0)

    def test_stat_keys(self):
        st_ = _F["mh324_stat"](_rets_demo())
        for k in ("n", "media", "vol", "sharpe", "min", "max",
                  "pct_pos", "omega0"):
            assert k in st_

    def test_stat_pochi_ko(self):
        with pytest.raises(ValueError):
            _F["mh324_stat"]([1.0] * 19)

    def test_pct_pos_range(self):
        assert 0.0 < PCTPOS < 100.0


class TestCurva:
    def test_curva_punti(self):
        cur = _F["mh324_curva"](_rets_demo())
        assert len(cur) == 21
        assert cur[0][0] == pytest.approx(MINR)
        assert cur[-1][0] == pytest.approx(MAXR)

    def test_curva_estremi(self):
        cur = _F["mh324_curva"](_rets_demo())
        assert math.isinf(cur[0][1])
        assert cur[-1][1] == pytest.approx(0.0)

    def test_curva_non_crescente(self):
        cur = _F["mh324_curva"](_rets_demo())
        vals = [v for _, v in cur if not math.isinf(v)]
        assert all(b <= a + 1e-12 for a, b in zip(vals, vals[1:]))

    def test_curva_costante_ko(self):
        with pytest.raises(ValueError):
            _F["mh324_curva"]([2.0] * 20)

    def test_curva_pochi_punti_ko(self):
        with pytest.raises(ValueError):
            _F["mh324_curva"](_rets_demo(), n_punti=2)


class TestVerdetto:
    def test_verdetto_forte(self):
        v = _F["mh324_verdetto"](3.6, 0.5)
        assert v.startswith("asimmetria FORTEMENTE positiva")

    def test_verdetto_inf(self):
        v = _F["mh324_verdetto"](float("inf"), 1.2)
        assert v.startswith("asimmetria FORTEMENTE positiva")

    def test_verdetto_moderata(self):
        v = _F["mh324_verdetto"](1.2, 0.3)
        assert v.startswith("asimmetria positiva MODERATA")

    def test_verdetto_negativa(self):
        v = _F["mh324_verdetto"](0.7, -0.2)
        assert v.startswith("coda negativa DOMINANTE")

    def test_verdetto_demo(self):
        st_ = _F["mh324_stat"](_rets_demo())
        v = _F["mh324_verdetto"](st_["omega0"], st_["sharpe"])
        assert v == VERDETTO
        assert v.startswith(STATO)
