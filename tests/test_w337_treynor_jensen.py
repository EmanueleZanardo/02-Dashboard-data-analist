"""Test tab337 '📐 Treynor & Jensen: il premio per unita' di rischio sistematico': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica di Treynor & Jensen: validatori,
parse delle due serie di rendimenti %, regressione OLS (n, beta, alpha,
r2, corr, var_bm, cov), misure (exp_ann, jensen_ann, treynor, te_ann,
appraisal; risk-free parametrizzabile) e verdetto a 4 stati (ECCELLENTE /
BUONO / MODERATO / DEBOLE + NON MISURABILE), con note su segno dell'alpha,
affidabilita' R2 e profilo beta.
"""
import re
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh337_num", "mh337_parse_serie", "mh337_regressione",
           "mh337_misure", "mh337_verdetto")

TITLE337 = "📐 Treynor & Jensen: il premio per unita' di rischio sistematico"
TITLE338 = "⚖️ M² Modigliani: il rendimento a parita' di rischio col benchmark"
TITLE339 = "📉 Sortino ratio: il rendimento per unità di rischio al ribasso"
TITLE340 = "📉 Calmar ratio: il rendimento annuo per unità di max drawdown"
TITLE341 = "📐 K-ratio: la regolarità della crescita dell'equity"
TITLE336 = "📉 Max drawdown relativo: quanto si scende sotto il benchmark?"
TITLE335 = "📏 Tracking error: quanto si discosta la strategia dal benchmark?"
TITLE334 = "🎯 Hit rate: quanto spesso la strategia batte il benchmark?"
SERIE_ST_DEMO = '1.43\n0.02\n2.44\n2.61\n-1.28\n-0.76\n0.81\n0.2\n0.73\n-0.03\n2.45\n2.47\n1.51\n2.61\n1.46\n-0.45\n1.07\n-0.45\n2.17\n1.28\n1.26\n0.56\n2.72\n0.67\n0.1\n0.15\n1.45\n1.52\n1.86\n2.03\n4.13\n0.65\n0.22\n-0.4\n1.38\n2.2'
SERIE_BM_DEMO = '0.94\n-0.54\n1.43\n1.63\n-1.55\n-0.83\n0.74\n0.25\n0.58\n-0.34\n1.57\n1.46\n0.67\n1.84\n1.11\n-0.35\n1.01\n-0.45\n1.57\n0.55\n0.4\n-0.15\n1.94\n0.43\n0.13\n0.21\n1.19\n1.0\n1.05\n1.07\n2.96\n0.15\n0.04\n-0.3\n1.28\n1.84'

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N_PER = 36
BETA = 1.2425221215094588
ALPHA_M = 0.28641478776036067
R2 = 0.9314501530842647
CORR = 0.9651166525784667
TREYNOR = 10.942796455123846
JENSEN_ANN = 3.436977453124328
EXP_ANN = 13.596666666666668
TE_ANN = 1.328376022496212
APPRAISAL = 2.587352823988607
STATO = "Treynor & Jensen ECCELLENTE"
VERDETTO = "Treynor & Jensen ECCELLENTE (Treynor +10.94 pp/anno): il premio per unita' di rischio sistematico e' molto alto. La strategia e' pagata bene per il rischio di mercato che si assume. L'alpha di Jensen e' positiva (+3.44 pp/anno): la strategia crea valore oltre quanto spiegato dal beta. La regressione e' molto affidabile (R2 = 0.931): beta e alpha sono stimati con precisione. Profilo in linea col benchmark (beta = 1.24)."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _demo():
    return (_F["mh337_parse_serie"](SERIE_ST_DEMO, "strategia"),
            _F["mh337_parse_serie"](SERIE_BM_DEMO, "benchmark"))


class TestRegistry337:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 341
        assert "tab337" in dvars
        assert "tab337" in withs

    def test_titoli_allineati_334_335_336_337(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab334")] == TITLE334
        assert titoli[dvars.index("tab335")] == TITLE335
        assert titoli[dvars.index("tab336")] == TITLE336
        assert titoli[dvars.index("tab337")] == TITLE337

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab341"
        assert titoli[-1] == TITLE341
        assert withs[-1] == "tab341"


class TestNum:
    def test_num_ok(self):
        assert _F["mh337_num"](1.5, "x") == 1.5
        assert _F["mh337_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh337_num"](bad, "x")


class TestParse:
    def test_parse_ok(self):
        a = _F["mh337_parse_serie"](SERIE_ST_DEMO, "strategia")
        assert len(a) == N_PER == 36
        assert a[0] == pytest.approx(1.43)

    def test_parse_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh337_parse_serie"]("\n".join(["1.0"] * 11), "strategia")

    def test_parse_ko_numero(self):
        righe = SERIE_ST_DEMO.split("\n")
        righe[5] = "abc"
        with pytest.raises(ValueError):
            _F["mh337_parse_serie"]("\n".join(righe), "strategia")

    def test_parse_ko_non_testo(self):
        with pytest.raises(ValueError):
            _F["mh337_parse_serie"]([1.0] * 36, "strategia")

    def test_parse_virgola(self):
        a = _F["mh337_parse_serie"]("\n".join(["1,5"] * 36), "x")
        assert a[0] == pytest.approx(1.5)


class TestRegressione:
    def test_demo(self):
        rs, rb = _demo()
        r = _F["mh337_regressione"](rs, rb)
        assert r["n"] == N_PER == 36
        assert r["beta"] == pytest.approx(BETA, rel=1e-9)
        assert r["alpha"] == pytest.approx(ALPHA_M, rel=1e-9)
        assert r["r2"] == pytest.approx(R2, rel=1e-9)
        assert r["corr"] == pytest.approx(CORR, rel=1e-9)
        assert 0.0 <= r["r2"] <= 1.0
        assert r["var_bm"] > 0.0

    def test_identita_ols(self):
        rs, rb = _demo()
        r = _F["mh337_regressione"](rs, rb)
        assert r["alpha"] + r["beta"] * rb.mean() == pytest.approx(
            rs.mean(), rel=1e-9)

    def test_beta_uno(self):
        rb = np.arange(36, dtype=float)
        rs = 0.5 + 2.0 * rb
        r = _F["mh337_regressione"](rs, rb)
        assert r["beta"] == pytest.approx(2.0, rel=1e-9)
        assert r["alpha"] == pytest.approx(0.5, rel=1e-9)
        assert r["r2"] == pytest.approx(1.0, rel=1e-9)

    def test_ko_benchmark_piatto(self):
        rs = np.arange(36, dtype=float)
        with pytest.raises(ValueError):
            _F["mh337_regressione"](rs, np.ones(36))

    def test_ko_lunghezze_diverse(self):
        rs, rb = _demo()
        with pytest.raises(ValueError):
            _F["mh337_regressione"](rs, rb[:20])

    def test_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh337_regressione"](np.ones(11), np.ones(11))


class TestMisure:
    def test_demo(self):
        rs, rb = _demo()
        m = _F["mh337_misure"](rs, rb)
        assert m["n"] == N_PER == 36
        assert m["beta"] == pytest.approx(BETA, rel=1e-9)
        assert m["treynor"] == pytest.approx(TREYNOR, rel=1e-9)
        assert m["jensen_ann"] == pytest.approx(JENSEN_ANN, rel=1e-9)
        assert m["exp_ann"] == pytest.approx(EXP_ANN, rel=1e-9)
        assert m["te_ann"] == pytest.approx(TE_ANN, rel=1e-9)
        assert m["appraisal"] == pytest.approx(APPRAISAL, rel=1e-9)

    def test_relazioni(self):
        rs, rb = _demo()
        m = _F["mh337_misure"](rs, rb)
        assert m["treynor"] == pytest.approx(m["exp_ann"] / m["beta"],
                                             rel=1e-9)
        assert m["jensen_ann"] == pytest.approx(m["alpha"] * 12, rel=1e-9)
        assert m["appraisal"] == pytest.approx(m["jensen_ann"] / m["te_ann"],
                                               rel=1e-9)
        assert m["te_ann"] > 0

    def test_riskfree_sposta_excess(self):
        rs, rb = _demo()
        m0 = _F["mh337_misure"](rs, rb, 12, 0.0)
        m1 = _F["mh337_misure"](rs, rb, 12, 1.0)
        assert m1["exp_ann"] == pytest.approx(m0["exp_ann"] - 12.0, rel=1e-9)
        assert m1["beta"] == pytest.approx(m0["beta"], rel=1e-9)
        assert m1["jensen_ann"] == pytest.approx(m0["jensen_ann"] - 12.0
                                                 * (1.0 - m0["beta"]),
                                                 rel=1e-9)

    def test_treynor_none_beta_non_positivo(self):
        rb = np.linspace(0.1, 3.6, 36)
        rs = -rb
        m = _F["mh337_misure"](rs, rb)
        assert m["beta"] < 0
        assert m["treynor"] is None

    def test_ko_periodi_annuo(self):
        rs, rb = _demo()
        with pytest.raises(ValueError):
            _F["mh337_misure"](rs, rb, 0)
        with pytest.raises(ValueError):
            _F["mh337_misure"](rs, rb, -4)


class TestVerdetto:
    def test_verdetto_eccellente(self):
        v = _F["mh337_verdetto"](10.94, 3.44, 1.24, 0.93)
        assert v.startswith("Treynor & Jensen ECCELLENTE")
        assert "positiva" in v
        assert "molto affidabile" in v
        assert "in linea" in v

    def test_verdetto_soglia_8(self):
        v = _F["mh337_verdetto"](8.0, 1.0, 1.0, 0.8)
        assert v.startswith("Treynor & Jensen ECCELLENTE")

    def test_verdetto_buono(self):
        v = _F["mh337_verdetto"](7.99, 1.0, 1.0, 0.8)
        assert v.startswith("Treynor & Jensen BUONO")
        assert "accettabile" in v

    def test_verdetto_soglia_3(self):
        v = _F["mh337_verdetto"](3.0, 1.0, 1.0, 0.8)
        assert v.startswith("Treynor & Jensen BUONO")

    def test_verdetto_moderato(self):
        v = _F["mh337_verdetto"](2.99, -1.0, 1.0, 0.8)
        assert v.startswith("Treynor & Jensen MODERATO")
        assert "non e' positiva" in v

    def test_verdetto_debole(self):
        v = _F["mh337_verdetto"](0.0, -1.0, 1.0, 0.8)
        assert v.startswith("Treynor & Jensen DEBOLE")
        v2 = _F["mh337_verdetto"](-2.0, -1.0, 1.0, 0.8)
        assert v2.startswith("Treynor & Jensen DEBOLE")

    def test_verdetto_beta_non_positivo(self):
        v = _F["mh337_verdetto"](None, 1.0, 0.0, 0.9)
        assert "NON MISURABILE" in v
        assert "beta non positivo" in v
        v2 = _F["mh337_verdetto"](-5.0, 1.0, -0.5, 0.9)
        assert "NON MISURABILE" in v2

    def test_verdetto_none(self):
        v = _F["mh337_verdetto"](None, 1.0, 1.0, 0.9)
        assert v.startswith("Treynor & Jensen NON MISURABILE")
        v2 = _F["mh337_verdetto"](5.0, None, 1.0, 0.9)
        assert v2.startswith("Treynor & Jensen NON MISURABILE")
        v3 = _F["mh337_verdetto"](5.0, 1.0, None, 0.9)
        assert v3.startswith("Treynor & Jensen NON MISURABILE")
        v4 = _F["mh337_verdetto"](5.0, 1.0, 1.0, None)
        assert v4.startswith("Treynor & Jensen NON MISURABILE")

    def test_verdetto_r2_basso(self):
        v = _F["mh337_verdetto"](10.0, 2.0, 1.0, 0.3)
        assert "poco affidabile" in v

    def test_verdetto_beta_aggressivo(self):
        v = _F["mh337_verdetto"](10.0, 2.0, 1.6, 0.9)
        assert "aggressivo" in v

    def test_verdetto_beta_difensivo(self):
        v = _F["mh337_verdetto"](10.0, 2.0, 0.5, 0.9)
        assert "difensivo" in v

    def test_verdetto_demo(self):
        v = _F["mh337_verdetto"](TREYNOR, JENSEN_ANN, BETA, R2)
        assert v == VERDETTO
        assert v.startswith(STATO)

    def test_verdetto_ko_tipo(self):
        with pytest.raises(ValueError):
            _F["mh337_verdetto"]("x", 1.0, 1.0, 0.9)
