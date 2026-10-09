
"""Test tab339 '📉 Sortino ratio: il rendimento per unità di rischio al ribasso': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica del Sortino ratio: validatori, parse
della serie di rendimenti %, misure (exp_ann, mar_ann, premio, dd, dd_ann,
vol_ann, sortino, n_down, sharpe_vs_mar; MAR parametrizzabile) e verdetto a 4
stati (ECCELLENTE / BUONO / MODERATO / DEBOLE + NON MISURABILE), con note su
asimmetria (downside vs vol totale) e quota di periodi sotto il target.
"""
import re
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh339_num", "mh339_parse_serie", "mh339_misure", "mh339_verdetto")

TITLE339 = "📉 Sortino ratio: il rendimento per unità di rischio al ribasso"
TITLE340 = "📉 Calmar ratio: il rendimento annuo per unità di max drawdown"
TITLE341 = "📐 K-ratio: la regolarità della crescita dell'equity"
TITLE342 = "🎯 Volatilità target: il sizing a volatilità costante"
TITLE343 = "📐 Kelly criterion: il sizing ottimale dall'edge stimato"
TITLE344 = "🎲 Risk of ruin: probabilita' di toccare una barriera di drawdown"
TITLE338 = "⚖️ M² Modigliani: il rendimento a parita' di rischio col benchmark"
TITLE337 = "📐 Treynor & Jensen: il premio per unita' di rischio sistematico"
TITLE336 = "📉 Max drawdown relativo: quanto si scende sotto il benchmark?"
SERIE_DEMO = '1.1\n0.6\n1.8\n-2.8\n0.9\n1.2\n-0.7\n1.6\n0.8\n0.4\n-1.5\n1.3\n0.7\n1.0\n-2.2\n1.4\n0.5\n0.9\n-1.8\n1.1\n2.0\n0.3\n-0.9\n1.2\n0.8\n0.6\n1.5\n-2.5\n1.0\n0.7\n0.5\n1.9\n-1.2\n0.9\n0.6\n1.3'

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N_PER = 36
EXP_ANN = 5.000000000000001
MAR_ANN = 0.0
PREMIO = 5.000000000000001
DD = 0.8685876147196923
DD_ANN = 3.0088757590391353
VOL_ANN = 4.371204476048743
SORTINO = 1.6617502351099793
N_DOWN = 8
SHARPE = 1.14384948757182
STATO = "Sortino ratio BUONO"
VERDETTO = "Sortino ratio BUONO (1.66): il premio sul target (+5.00 pp/anno) ripaga bene il rischio al ribasso: l'upside conta piu' dei ribassi. Profilo asimmetrico favorevole: il rischio al ribasso (3.01 pp) pesa meno della volatilita' totale (4.37 pp): l'upside non e' penalizzato. (8 periodi su 36 sotto il target)."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _demo():
    return _F["mh339_parse_serie"](SERIE_DEMO, "strategia")


class TestRegistry339:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 344
        assert "tab339" in dvars
        assert "tab339" in withs

    def test_titoli_allineati_336_337_338_339(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab336")] == TITLE336
        assert titoli[dvars.index("tab337")] == TITLE337
        assert titoli[dvars.index("tab338")] == TITLE338
        assert titoli[dvars.index("tab339")] == TITLE339

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab344"
        assert titoli[-1] == TITLE344
        assert withs[-1] == "tab344"


class TestNum:
    def test_num_ok(self):
        assert _F["mh339_num"](1.5, "x") == 1.5
        assert _F["mh339_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh339_num"](bad, "x")


class TestParse:
    def test_parse_ok(self):
        a = _F["mh339_parse_serie"](SERIE_DEMO, "strategia")
        assert len(a) == N_PER == 36
        assert a[0] == pytest.approx(1.1)

    def test_parse_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh339_parse_serie"]("\n".join(["1.0"] * 11), "strategia")

    def test_parse_ko_numero(self):
        righe = SERIE_DEMO.split("\n")
        righe[5] = "abc"
        with pytest.raises(ValueError):
            _F["mh339_parse_serie"]("\n".join(righe), "strategia")

    def test_parse_ko_non_testo(self):
        with pytest.raises(ValueError):
            _F["mh339_parse_serie"]([1.0] * 36, "strategia")

    def test_parse_virgola(self):
        a = _F["mh339_parse_serie"]("\n".join(["1,5"] * 36), "x")
        assert a[0] == pytest.approx(1.5)


class TestMisure:
    def test_demo(self):
        r = _demo()
        m = _F["mh339_misure"](r)
        assert m["n"] == N_PER == 36
        assert m["exp_ann"] == pytest.approx(EXP_ANN, rel=1e-9)
        assert m["mar_ann"] == pytest.approx(MAR_ANN, rel=1e-9)
        assert m["premio"] == pytest.approx(PREMIO, rel=1e-9)
        assert m["dd"] == pytest.approx(DD, rel=1e-9)
        assert m["dd_ann"] == pytest.approx(DD_ANN, rel=1e-9)
        assert m["vol_ann"] == pytest.approx(VOL_ANN, rel=1e-9)
        assert m["sortino"] == pytest.approx(SORTINO, rel=1e-9)
        assert m["n_down"] == N_DOWN == 8
        assert m["sharpe_vs_mar"] == pytest.approx(SHARPE, rel=1e-9)
        assert m["dd_ann"] < m["vol_ann"]
        assert m["sortino"] > m["sharpe_vs_mar"] > 0

    def test_relazioni(self):
        r = _demo()
        m = _F["mh339_misure"](r)
        assert m["premio"] == pytest.approx(m["exp_ann"] - m["mar_ann"],
                                            rel=1e-9)
        assert m["sortino"] == pytest.approx(m["premio"] / m["dd_ann"],
                                             rel=1e-9)
        assert m["dd_ann"] == pytest.approx(m["dd"] * (12 ** 0.5), rel=1e-9)
        assert m["sharpe_vs_mar"] == pytest.approx(
            m["premio"] / m["vol_ann"], rel=1e-9)

    def test_mar_sposta_target(self):
        r = _demo()
        m0 = _F["mh339_misure"](r, 12, 0.0)
        m1 = _F["mh339_misure"](r, 12, 0.5)
        assert m1["mar_ann"] == pytest.approx(6.0, rel=1e-9)
        assert m1["premio"] == pytest.approx(m0["premio"] - 6.0, rel=1e-9)
        assert m1["n_down"] > m0["n_down"]
        assert m1["dd_ann"] > m0["dd_ann"]
        assert m1["sortino"] < m0["sortino"]

    def test_ko_nessun_ribasso(self):
        with pytest.raises(ValueError):
            _F["mh339_misure"](np.full(36, 1.0))

    def test_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh339_misure"](np.ones(11))

    def test_ko_periodi_annuo(self):
        r = _demo()
        with pytest.raises(ValueError):
            _F["mh339_misure"](r, 0)
        with pytest.raises(ValueError):
            _F["mh339_misure"](r, -4)


class TestVerdetto:
    def test_verdetto_buono_demo(self):
        v = _F["mh339_verdetto"](1.66, 5.0, 3.01, 4.37, 8, 36)
        assert v.startswith("Sortino ratio BUONO")
        assert "asimmetrico" in v

    def test_verdetto_soglia_2(self):
        v = _F["mh339_verdetto"](2.0, 6.0, 3.0, 4.0, 5, 36)
        assert v.startswith("Sortino ratio ECCELLENTE")

    def test_verdetto_soglia_1(self):
        v = _F["mh339_verdetto"](1.0, 3.0, 3.0, 4.0, 5, 36)
        assert v.startswith("Sortino ratio BUONO")

    def test_verdetto_moderato(self):
        v = _F["mh339_verdetto"](0.7, 2.0, 2.86, 4.0, 5, 36)
        assert v.startswith("Sortino ratio MODERATO")

    def test_verdetto_soglia_05(self):
        v = _F["mh339_verdetto"](0.5, 1.5, 3.0, 4.0, 5, 36)
        assert v.startswith("Sortino ratio MODERATO")

    def test_verdetto_debole(self):
        v = _F["mh339_verdetto"](0.3, 1.0, 3.33, 4.0, 5, 36)
        assert v.startswith("Sortino ratio DEBOLE")

    def test_verdetto_simmetrico(self):
        v = _F["mh339_verdetto"](1.5, 4.5, 3.9, 4.0, 5, 36)
        assert "simmetrico" in v
        assert "asimmetrico favorevole" not in v

    def test_verdetto_none(self):
        v = _F["mh339_verdetto"](None, 5.0, 3.0, 4.0, 8, 36)
        assert v.startswith("Sortino ratio NON MISURABILE")
        v2 = _F["mh339_verdetto"](1.66, None, 3.0, 4.0, 8, 36)
        assert v2.startswith("Sortino ratio NON MISURABILE")

    def test_verdetto_demo(self):
        v = _F["mh339_verdetto"](SORTINO, PREMIO, DD_ANN, VOL_ANN,
                                 N_DOWN, N_PER)
        assert v == VERDETTO
        assert v.startswith(STATO)

    def test_verdetto_ko_tipo(self):
        with pytest.raises(ValueError):
            _F["mh339_verdetto"]("x", 5.0, 3.0, 4.0, 8, 36)
