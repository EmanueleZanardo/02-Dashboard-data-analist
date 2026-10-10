
"""Test tab340 '📉 Calmar ratio: il rendimento annuo per unità di max drawdown': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica del Calmar ratio: validatori, parse
della serie di rendimenti %, equity curve, misure (exp_ann, picco/minimo
1-based, max_dd %, recupero periodi o None, calmar) e verdetto a 4 stati
(ECCELLENTE / BUONO / MODERATO / DEBOLE + NON MISURABILE), con note su
profondita' del drawdown e tempo di recupero.
"""
import re
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh340_num", "mh340_parse_serie", "mh340_equity",
           "mh340_misure", "mh340_verdetto")

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
TITLE339 = "📉 Sortino ratio: il rendimento per unità di rischio al ribasso"
TITLE338 = "⚖️ M² Modigliani: il rendimento a parita' di rischio col benchmark"
TITLE337 = "📐 Treynor & Jensen: il premio per unita' di rischio sistematico"
SERIE_DEMO = '1.2\n0.8\n1.5\n-0.6\n0.9\n1.1\n-4.8\n-2.5\n1.6\n0.7\n-0.9\n1.3\n0.8\n1.0\n1.4\n-1.2\n0.6\n0.9\n1.7\n-0.5\n1.1\n0.4\n-0.7\n1.2\n0.9\n0.5\n1.6\n-1.4\n0.8\n1.0\n0.6\n1.3\n-0.8\n0.9\n0.7\n1.2'

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N_PER = 36
EXP_ANN = 4.766666666666667
PICCO = 6
MINIMO = 8
MAX_DD = -7.179999999999998
RECUPERO = 11
CALMAR = 0.6638811513463326
STATO = "Calmar ratio MODERATO"
VERDETTO = "Calmar ratio MODERATO (0.66): il rendimento annuo (+4.77 pp) copre a malapena il peggior ribasso: il sizing deve restare contenuto. Il peggior ribasso vissuto e' stato -7.2%: e' il dolore massimo che il capitale deve reggere (36 periodi). Recupero in 11 periodi."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _demo():
    return _F["mh340_parse_serie"](SERIE_DEMO, "strategia")


class TestRegistry340:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 355
        assert "tab340" in dvars
        assert "tab340" in withs

    def test_titoli_allineati_337_338_339_340(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab337")] == TITLE337
        assert titoli[dvars.index("tab338")] == TITLE338
        assert titoli[dvars.index("tab339")] == TITLE339
        assert titoli[dvars.index("tab340")] == TITLE340

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab355"
        assert titoli[-1] == TITLE355
        assert withs[-1] == "tab355"


class TestNum:
    def test_num_ok(self):
        assert _F["mh340_num"](1.5, "x") == 1.5
        assert _F["mh340_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh340_num"](bad, "x")


class TestParse:
    def test_parse_ok(self):
        a = _F["mh340_parse_serie"](SERIE_DEMO, "strategia")
        assert len(a) == N_PER == 36
        assert a[0] == pytest.approx(1.2)

    def test_parse_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh340_parse_serie"]("\n".join(["1.0"] * 11), "strategia")

    def test_parse_ko_numero(self):
        righe = SERIE_DEMO.split("\n")
        righe[5] = "abc"
        with pytest.raises(ValueError):
            _F["mh340_parse_serie"]("\n".join(righe), "strategia")

    def test_parse_ko_non_testo(self):
        with pytest.raises(ValueError):
            _F["mh340_parse_serie"]([1.0] * 36, "strategia")

    def test_parse_virgola(self):
        a = _F["mh340_parse_serie"]("\n".join(["1,5"] * 36), "x")
        assert a[0] == pytest.approx(1.5)


class TestEquity:
    def test_equity_base(self):
        eq = _F["mh340_equity"](_demo())
        assert eq[0] == pytest.approx(100.0)
        assert len(eq) == N_PER + 1

    def test_equity_compound(self):
        eq = _F["mh340_equity"](np.array([10.0, -10.0]))
        assert eq[1] == pytest.approx(110.0)
        assert eq[2] == pytest.approx(99.0)


class TestMisure:
    def test_demo(self):
        r = _demo()
        m = _F["mh340_misure"](r)
        assert m["n"] == N_PER == 36
        assert m["exp_ann"] == pytest.approx(EXP_ANN, rel=1e-9)
        assert m["picco"] == PICCO
        assert m["minimo"] == MINIMO
        assert m["minimo"] > m["picco"]
        assert m["max_dd"] == pytest.approx(MAX_DD, rel=1e-9)
        assert m["max_dd"] < 0
        assert m["recupero"] == RECUPERO
        assert m["calmar"] == pytest.approx(CALMAR, rel=1e-9)
        assert m["calmar"] > 0

    def test_relazioni(self):
        r = _demo()
        m = _F["mh340_misure"](r)
        assert m["exp_ann"] == pytest.approx(float(r.mean()) * 12, rel=1e-9)
        assert m["calmar"] == pytest.approx(
            m["exp_ann"] / abs(m["max_dd"]), rel=1e-9)
        assert m["dd_pct"][m["minimo"]] == pytest.approx(m["max_dd"],
                                                         rel=1e-9)
        assert min(m["dd_pct"]) == pytest.approx(m["max_dd"], rel=1e-9)

    def test_recupero_none(self):
        r = np.array([-1.0] * 11 + [1.0])
        assert len(r) == 12
        m = _F["mh340_misure"](r)
        assert m["max_dd"] < 0
        assert m["recupero"] is None

    def test_ko_monotona(self):
        with pytest.raises(ValueError):
            _F["mh340_misure"](np.full(36, 1.0))

    def test_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh340_misure"](np.ones(11))

    def test_ko_periodi_annuo(self):
        r = _demo()
        with pytest.raises(ValueError):
            _F["mh340_misure"](r, 0)
        with pytest.raises(ValueError):
            _F["mh340_misure"](r, -4)


class TestVerdetto:
    def test_verdetto_buono_demo(self):
        v = _F["mh340_verdetto"](1.8, 7.2, -4.0, 6, 36)
        assert v.startswith("Calmar ratio BUONO")
        assert "-4.0%" in v

    def test_verdetto_soglia_3(self):
        v = _F["mh340_verdetto"](3.0, 9.0, -3.0, 4, 36)
        assert v.startswith("Calmar ratio ECCELLENTE")

    def test_verdetto_soglia_15(self):
        v = _F["mh340_verdetto"](1.5, 6.0, -4.0, 4, 36)
        assert v.startswith("Calmar ratio BUONO")

    def test_verdetto_moderato(self):
        v = _F["mh340_verdetto"](0.8, 4.0, -5.0, 8, 36)
        assert v.startswith("Calmar ratio MODERATO")

    def test_verdetto_soglia_05(self):
        v = _F["mh340_verdetto"](0.5, 2.5, -5.0, 8, 36)
        assert v.startswith("Calmar ratio MODERATO")

    def test_verdetto_debole(self):
        v = _F["mh340_verdetto"](0.3, 1.5, -5.0, 10, 36)
        assert v.startswith("Calmar ratio DEBOLE")

    def test_verdetto_recupero_lento(self):
        v = _F["mh340_verdetto"](1.6, 6.4, -4.0, 12, 36)
        assert "12 periodi" in v

    def test_verdetto_non_recuperato(self):
        v = _F["mh340_verdetto"](1.6, 6.4, -4.0, None, 36)
        assert "NON MISURABILE" in v

    def test_verdetto_none(self):
        v = _F["mh340_verdetto"](None, 6.4, -4.0, 6, 36)
        assert v.startswith("Calmar ratio NON MISURABILE")
        v2 = _F["mh340_verdetto"](1.6, None, -4.0, 6, 36)
        assert v2.startswith("Calmar ratio NON MISURABILE")

    def test_verdetto_demo(self):
        v = _F["mh340_verdetto"](CALMAR, EXP_ANN, MAX_DD, RECUPERO, N_PER)
        assert v == VERDETTO
        assert v.startswith(STATO)

    def test_verdetto_ko_tipo(self):
        with pytest.raises(ValueError):
            _F["mh340_verdetto"]("x", 6.4, -4.0, 6, 36)
