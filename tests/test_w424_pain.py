
"""Test tab424 '🤕 Pain ratio: il rendimento medio contro il drawdown medio': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh424_num", "mh424_parse_serie", "mh424_equity",
           "mh424_drawdowns", "mh424_pain", "mh424_pain_ratio",
           "mh424_verdetto", "mh424_curva", "mh424_mappa",
           "mh421_num", "mh421_equity", "mh421_drawdowns",
           "mh421_ulcer", "mh421_martin")

TITLE424 = "🤕 Pain ratio: il rendimento medio contro il drawdown medio"
TITLE426 = "🔀 Sequence risk: l'ordine dei rendimenti cambia il drawdown"
TITLE423 = "🔃 MAR ratio: il rendimento composto contro il peggior drawdown"
TITLE425 = "🚀 Upside Potential ratio: il guadagno atteso contro la downside deviation"
TITLE422 = "🎯 Calmar ratio: il rendimento medio contro il peggior drawdown"
TITLE421 = "📉 Ulcer Performance Index (Martin ratio): il rischio drawdown contro il rendimento"
TITLE420 = "📈 Gain-Loss ratio: guadagno atteso contro perdita attesa"
TITLE419 = "⭐ STAR ratio: il rendimento medio contro la perdita attesa di coda"
TITLE418 = "📊 Rachev ratio: tutta la coda destra contro tutta la coda sinistra"
DEMO = '3.5\n3.9\n2.6\n4.3\n2.9\n4.8\n2.1\n3.7\n3.2\n4.5\n2.8\n2.4\n4.1\n3.6\n5.0\n2.3\n3.1\n3.8\n2.5\n4.6\n3.0\n4.2\n2.2\n3.4\n4.0\n2.7\n4.7\n3.3\n2.0\n4.4\n-9.5\n-7.2\n-14.0\n-8.3\n-6.1\n-10.2'
PAIN = 0.2857664706631636
MEAN = 1.3416666666666666
PAINIDX = 4.694975808579396
ULCER = 12.513733768880378
MAXDD = 44.15217408197824


class TestRegistry424:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 426
        assert "tab424" in dvars
        assert "tab424" in withs

    def test_titoli_allineati_418_419_420_421_422_423_424(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert titoli[dvars.index("tab418")] == TITLE418
        assert titoli[dvars.index("tab419")] == TITLE419
        assert titoli[dvars.index("tab420")] == TITLE420
        assert titoli[dvars.index("tab421")] == TITLE421
        assert titoli[dvars.index("tab422")] == TITLE422
        assert titoli[dvars.index("tab423")] == TITLE423
        assert titoli[dvars.index("tab424")] == TITLE424

    def test_ultima_tab(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"with (tab\d+):", src)
        assert dvars[-1] == "tab426"
        assert titoli[-1] == TITLE426
        assert withs[-1] == "tab426"


class TestPain424:
    def _xs(self):
        return _F["mh424_parse_serie"](DEMO)

    def test_demo_valori(self):
        xs = self._xs()
        assert len(xs) == 36
        m = _F["mh424_mappa"](xs, 0.0)
        assert abs(m["pain_ratio"] - PAIN) < 1e-12
        assert abs(m["mean"] - MEAN) < 1e-12
        assert abs(m["pain"] - PAINIDX) < 1e-12
        assert abs(m["ulcer"] - ULCER) < 1e-12
        assert abs(m["max_dd"] - MAXDD) < 1e-12
        # media 1.3417%, pain index 4.6950% < ulcer 12.5137%
        assert abs(m["mean"] - 1.3417) < 1e-3
        assert abs(m["pain"] - 4.6950) < 1e-3
        assert abs(m["ulcer"] - 12.5137) < 1e-3
        assert m["pain"] < m["ulcer"]
        assert m["n_dd"] == 6
        assert m["pain_ratio"] < 1.0
        assert m["verdetto"].startswith("NEGATIVO")
        assert 0.2 < m["pain_ratio"] < 0.4
        # definizione: pain_ratio = eccesso / pain, eccesso = media - T
        assert abs(m["pain_ratio"] - m["excess"] / m["pain"]) < 1e-12
        assert abs(m["excess"] - (m["mean"] - 0.0)) < 1e-12
        # ulcer >= pain >= 0 (RMS >= AM) e max_dd >= pain
        assert m["ulcer"] >= m["pain"] >= 0.0
        assert m["max_dd"] >= m["pain"]

    def test_definizione_a_mano(self):
        # equity composta -> running max + dd punto per punto ->
        # pain = media dei drawdown, indipendenti dall'helper
        xs = list(self._xs())
        eq, dd, peak = 100.0, [], 100.0
        for x in xs:
            eq *= 1.0 + x / 100.0
            peak = max(peak, eq)
            dd.append((peak - eq) / peak * 100.0)
        n = len(xs)
        pain_mano = sum(dd) / n
        import math as _m
        ulcer_mano = _m.sqrt(sum(d * d for d in dd) / n)
        k = _F["mh424_pain_ratio"](tuple(xs), 0.0)
        assert abs(k["pain"] - pain_mano) < 1e-12
        assert abs(k["ulcer"] - ulcer_mano) < 1e-12
        mean_mano = sum(xs) / n
        assert abs(k["pain_ratio"] - mean_mano / pain_mano) < 1e-12
        assert abs(_F["mh424_pain"](tuple(xs))["pain"]
                   - pain_mano) < 1e-12
        # i drawdown dell'helper coincidono punto per punto
        for a, b in zip(_F["mh424_drawdowns"](tuple(xs)), dd):
            assert abs(a - b) < 1e-12
        # l'equity dell'helper coincide
        e0 = 100.0
        for a, x in zip(_F["mh424_equity"](tuple(xs)), xs):
            e0 *= 1.0 + x / 100.0
            assert abs(a - e0) < 1e-9

    def test_chiave_teorica_pain_maggiore_uguale_upi(self):
        # CHIAVE TEORICA: per drawdown >= 0 vale SEMPRE
        #   Pain ratio >= UPI   (se eccesso >= 0),
        # perche' ulcer (RMS) >= pain index (media): RMS >= AM.
        # Sesto gemello: STESSO numeratore dell'UPI (media - T),
        # denominatore piu' "gentile" (media invece di RMS).
        # Sulla demo: Pain 0.2858 > UPI 0.1072 (eccesso > 0).
        xs = self._xs()
        pr = _F["mh424_pain_ratio"](xs, 0.0)["pain_ratio"]
        upi = _F["mh421_martin"](xs, 0.0)["upi"]
        assert pr > upi
        assert abs(pr - 0.2858) < 0.005
        assert abs(upi - 0.1072) < 0.005
        # rapporto dei ratio = rapporto inverso dei denominatori
        k = _F["mh424_pain_ratio"](xs, 0.0)
        assert abs(pr / upi - k["ulcer"] / k["pain"]) < 1e-9
        # con eccesso < 0 la disuguaglianza si rovescia (stessa
        # frazione, numeratore negativo): Pain < UPI
        pr_neg = _F["mh424_pain_ratio"](xs, 5.0)["pain_ratio"]
        upi_neg = _F["mh421_martin"](xs, 5.0)["upi"]
        assert pr_neg < upi_neg < 0.0
        # serie con un dip: eccesso > 0, Pain > UPI stretto
        dip = [2.0] * 20
        dip[10] = -5.0
        dip = tuple(dip)
        assert _F["mh424_pain_ratio"](dip, 0.0)["pain_ratio"] > \
            _F["mh421_martin"](dip, 0.0)["upi"]
        # drawdown COSTANTE: RMS == media -> Pain == UPI
        # (primo rendimento -5%, poi piatta: dd = 5% sempre)
        const = (-5.0,) + (0.0,) * 35
        kc = _F["mh424_pain"](const)
        assert abs(kc["pain"] - 5.0) < 1e-12
        assert abs(kc["ulcer"] - kc["pain"]) < 1e-12
        assert abs(_F["mh424_pain_ratio"](const, 0.0)["pain_ratio"]
                   - _F["mh421_martin"](const, 0.0)["upi"]) < 1e-12

    def test_crosscheck_tab421_upi(self):
        # il cross-check di famiglia: mappa["upi"] e' l'UPI vero
        # di tab421 (stesso numeratore, denominatore RMS)
        xs = self._xs()
        m = _F["mh424_mappa"](xs, 0.0)
        assert abs(m["upi"] - _F["mh421_martin"](xs, 0.0)
                   ["upi"]) < 1e-12
        assert abs(m["ulcer"] - _F["mh421_ulcer"](xs)
                   ["ulcer"]) < 1e-12
        assert abs(m["ulcer"] - 12.5137) < 1e-3
        assert m["pain_ratio"] > m["upi"] > 0.0

    def test_monotonia(self):
        F = _F
        xs = self._xs()
        base = F["mh424_pain_ratio"](xs, 0.0)["pain_ratio"]
        # alzare i rendimenti di +1: media sale -> Pain sale
        up = tuple(x + 1.0 for x in xs)
        assert F["mh424_pain_ratio"](up, 0.0)["pain_ratio"] > base
        # approfondire i crash: pain index piu' alto -> Pain scende
        dn = tuple(x - 1.0 if x < 0.0 else x for x in xs)
        assert F["mh424_pain_ratio"](dn, 0.0)["pain_ratio"] < base
        # alzare il target: numeratore cala -> Pain scende
        assert F["mh424_pain_ratio"](xs, 2.5)["pain_ratio"] < base
        assert F["mh424_pain_ratio"](xs, -2.5)["pain_ratio"] > base

    def test_non_invarianza_di_scala(self):
        # CHIAVE TEORICA (proprieta' intenzionale, non bug): il
        # drawdown e' una funzione di percorso non lineare
        # dell'equity composta, quindi Pain(2x) != Pain(x).
        # Come per UPI (tab421), Calmar (tab422), MAR (tab423).
        xs = self._xs()
        base = _F["mh424_pain_ratio"](xs, 0.0)["pain_ratio"]
        sc = tuple(2.0 * x for x in xs)
        pr2 = _F["mh424_pain_ratio"](sc, 0.0)["pain_ratio"]
        assert abs(pr2 - base) > 1e-6
        assert abs(pr2 - 0.3303) < 0.005

    def test_infinito_senza_drawdown(self):
        # solo guadagni: mai sott'acqua -> pain=0 -> +inf
        k = _F["mh424_pain_ratio"](tuple([1.0] * 25), 0.0)
        assert math.isinf(k["pain_ratio"]) and k["pain_ratio"] > 0
        assert k["pain"] == 0.0
        assert _F["mh424_verdetto"](k["pain_ratio"]).startswith(
            "MOLTO FORTE")
        # serie piatta su 0: eccesso=0, pain=0 -> non definito
        with pytest.raises(ValueError):
            _F["mh424_pain_ratio"](tuple([0.0] * 25), 0.0)
        # serie piatta a 2% con T=0: eccesso>0, pain=0 -> +inf
        k2 = _F["mh424_pain_ratio"](tuple([2.0] * 25), 0.0)
        assert math.isinf(k2["pain_ratio"]) and k2["pain_ratio"] > 0
        # serie piatta a 2% con T=5: eccesso<0, pain=0 -> -inf
        k3 = _F["mh424_pain_ratio"](tuple([2.0] * 25), 5.0)
        assert math.isinf(k3["pain_ratio"]) and k3["pain_ratio"] < 0
        assert _F["mh424_verdetto"](k3["pain_ratio"]).startswith(
            "NEGATIVO")

    def test_curva(self):
        F = _F
        xs = self._xs()
        c = F["mh424_curva"](xs, -2.0, 2.0, 1.0)
        assert len(c) == 5
        assert [t for t, _ in c] == [-2.0, -1.0, 0.0, 1.0, 2.0]
        # il punto a T=0 e' il Pain della demo
        assert abs(dict(c)[0.0] - PAIN) < 1e-12
        # monotona decrescente in T (numeratore cala, pain fisso)
        uu = [u for _, u in c]
        assert all(u is not None for u in uu)
        assert all(a > b for a, b in zip(uu, uu[1:]))
        # ogni punto coincide con pain_ratio al target T
        for t, u in c:
            mio = F["mh424_pain_ratio"](xs, t)["pain_ratio"]
            assert abs(u - mio) < 1e-12
        with pytest.raises(ValueError):
            F["mh424_curva"](None)
        with pytest.raises(ValueError):
            F["mh424_curva"](xs, 2.0, -2.0, 1.0)
        with pytest.raises(ValueError):
            F["mh424_curva"](xs, -2.0, 2.0, 0.0)

    def test_verdetto_soglie(self):
        F = _F
        assert F["mh424_verdetto"](0.99).startswith("NEGATIVO")
        assert F["mh424_verdetto"](-3.0).startswith("NEGATIVO")
        assert F["mh424_verdetto"](float("-inf")).startswith("NEGATIVO")
        assert F["mh424_verdetto"](1.0).startswith("DEBOLE")
        assert F["mh424_verdetto"](1.49).startswith("DEBOLE")
        assert F["mh424_verdetto"](1.50).startswith("ACCETTABILE")
        assert F["mh424_verdetto"](1.99).startswith("ACCETTABILE")
        assert F["mh424_verdetto"](2.0).startswith("BUONO")
        assert F["mh424_verdetto"](2.99).startswith("BUONO")
        assert F["mh424_verdetto"](3.0).startswith("FORTE")
        assert F["mh424_verdetto"](4.99).startswith("FORTE")
        assert F["mh424_verdetto"](5.0).startswith("MOLTO FORTE")
        assert F["mh424_verdetto"](float("inf")).startswith("MOLTO FORTE")
        with pytest.raises(ValueError):
            F["mh424_verdetto"](float("nan"))
        with pytest.raises(ValueError):
            F["mh424_verdetto"](True)

    def test_casi_degeneri(self):
        F = _F
        with pytest.raises(ValueError):
            F["mh424_pain_ratio"](tuple([0.0] * 25), 0.0)
        with pytest.raises(ValueError):
            F["mh424_mappa"](tuple([0.0] * 25), 0.0)
        with pytest.raises(ValueError):
            F["mh424_mappa"]((1.0,) * 19, 0.0)
        with pytest.raises(ValueError):
            F["mh424_mappa"](None, 0.0)
        with pytest.raises(ValueError):
            F["mh424_pain"]((1.0,) * 19)
        # target cattivo contro la sua funzione (lezione tab417)
        for _t in (True, "x", float("nan"), float("inf")):
            with pytest.raises(ValueError):
                F["mh424_pain_ratio"](self._xs(), _t)

    def test_validatori(self):
        for _bad in (lambda: _F["mh424_pain_ratio"](None, 0.0),
                     lambda: _F["mh424_pain_ratio"]((1.0,) * 19, 0.0),
                     lambda: _F["mh424_pain_ratio"](tuple([0.0] * 25), 0.0),
                     lambda: _F["mh424_pain_ratio"](self._xs(), True),
                     lambda: _F["mh424_pain_ratio"](self._xs(),
                                                    float("nan")),
                     lambda: _F["mh424_parse_serie"](
                         "\n".join(["1.0"] * 19)),
                     lambda: _F["mh424_parse_serie"](
                         "\n".join(["xx"] + ["1.0"] * 20)),
                     lambda: _F["mh424_parse_serie"](None),
                     lambda: _F["mh424_num"](True, "x"),
                     lambda: _F["mh424_num"](float("nan"), "x"),
                     lambda: _F["mh424_mappa"]((1.0,) * 19, 0.0),
                     lambda: _F["mh424_mappa"](None, 0.0),
                     lambda: _F["mh424_mappa"](tuple([0.0] * 25), 0.0),
                     lambda: _F["mh424_mappa"](self._xs(), True),
                     lambda: _F["mh424_curva"](None),
                     lambda: _F["mh424_curva"](self._xs(), 1.0, -1.0),
                     lambda: _F["mh424_curva"](self._xs(), 0.0, 1.0, 0.0)):
            with pytest.raises(ValueError):
                _bad()

    def test_mappa_stringa_input(self):
        # mappa accetta anche il testo grezzo della text area
        m = _F["mh424_mappa"](DEMO, 0.0)
        assert abs(m["pain_ratio"] - PAIN) < 1e-12
        assert abs(m["upi"] - _F["mh421_martin"](self._xs(), 0.0)
                   ["upi"]) < 1e-12
        assert abs(m["ulcer"] - _F["mh421_ulcer"](self._xs())
                   ["ulcer"]) < 1e-12

