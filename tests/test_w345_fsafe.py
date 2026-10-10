"""Test tab345 '🎯 Sizing anti-rovina: f massima con ROR vincolato': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica del sizing vincolato dal rischio
di rovina: validatori, Kelly pieno f* = (p*(b+1)-1)/b, coefficiente di
Lundberg theta (radice di p*(1+f*b)^(-theta) + q*(1-f)^(-theta) = 1 via
bisezione), R = barriera^theta (Cramer-Lundberg), edge per trade
e = f*(p*b-q), f_safe = unica f con R(f) = Rmax (bisezione, R monotono
crescente in f), misure (f_rec = min(half-Kelly, f_safe)) e verdetto a
3 stati (SIZING BLOCCATO / VINCOLO ROVINA ATTIVO / HALF-KELLY ENTRO RMAX).
"""
import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh345_num", "mh345_kelly", "mh345_theta", "mh345_ror",
           "mh345_edge", "mh345_f_safe", "mh345_misure", "mh345_verdetto")

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
TITLE344 = "🎲 Risk of ruin: probabilita' di toccare una barriera di drawdown"
TITLE343 = "📐 Kelly criterion: il sizing ottimale dall'edge stimato"
TITLE342 = "🎯 Volatilità target: il sizing a volatilità costante"

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
P = 0.55
WIN = 120.0
LOSS = 100.0
BAR = 0.5
RMAX = 0.05
B = 1.2
F_STAR = 0.17500000000000016
F_HALF = 0.08750000000000008
F_SAFE = 0.06588426159267208
F_REC = 0.06588426159267208
THETA = 4.321928094887394
EDGE = 0.013835694934461141
ROR = 0.04999999999999891
VERDETTO = 'VINCOLO ROVINA ATTIVO (f_safe = 6.59% < half-Kelly 8.75%): half-Kelly ha ROR oltre il limite 5%: tagliare la frazione a 6.59% (ROR = 5% al limite).'

_M = None


def _misure():
    global _M
    if _M is None:
        _M = _F["mh345_misure"](P, WIN, LOSS, BAR, RMAX)
    return _M


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry345:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 360
        assert "tab345" in dvars
        assert "tab345" in withs

    def test_titoli_allineati_342_343_344_345(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab342")] == TITLE342
        assert titoli[dvars.index("tab343")] == TITLE343
        assert titoli[dvars.index("tab344")] == TITLE344
        assert titoli[dvars.index("tab345")] == TITLE345

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab360"
        assert titoli[-1] == TITLE360
        assert withs[-1] == "tab360"


class TestNum:
    def test_num_ok(self):
        assert _F["mh345_num"](1.5, "x") == 1.5
        assert _F["mh345_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh345_num"](bad, "x")


class TestKelly:
    def test_demo(self):
        assert _F["mh345_kelly"](P, B) == pytest.approx(F_STAR, rel=1e-9)
        assert _F["mh345_kelly"](P, B) == pytest.approx(0.175, rel=1e-9)

    def test_formula(self):
        assert _F["mh345_kelly"](0.6, 2.0) == pytest.approx(
            max(0.0, (0.6 * 3.0 - 1.0) / 2.0), rel=1e-9)

    def test_nessun_edge_zero(self):
        assert _F["mh345_kelly"](0.4, 1.0) == 0.0

    def test_ko_p_bordi(self):
        for p in (0.0, 1.0):
            with pytest.raises(ValueError):
                _F["mh345_kelly"](p, B)

    def test_ko_b(self):
        with pytest.raises(ValueError):
            _F["mh345_kelly"](P, 0.0)


class TestTheta:
    def test_demo_radice(self):
        th = _F["mh345_theta"](P, B, F_REC)
        assert th == pytest.approx(THETA, rel=1e-9)
        assert th > 0
        up, down = 1.0 + F_REC * B, 1.0 - F_REC
        assert P * up ** (-th) + (1.0 - P) * down ** (-th) == pytest.approx(
            1.0, rel=1e-9)

    def test_nessun_edge_zero(self):
        # drift logaritmico <= 0: nessuna radice positiva
        assert _F["mh345_theta"](0.4, 1.0, 0.05) == 0.0

    def test_ko_f(self):
        with pytest.raises(ValueError):
            _F["mh345_theta"](P, B, 1.0)

    def test_ko_p(self):
        with pytest.raises(ValueError):
            _F["mh345_theta"](1.0, B, 0.05)


class TestRor:
    def test_demo(self):
        r = _F["mh345_ror"](P, B, F_REC, BAR)
        assert r == pytest.approx(ROR, rel=1e-9)
        assert r == pytest.approx(BAR ** THETA, rel=1e-9)

    def test_nessun_edge_uno(self):
        assert _F["mh345_ror"](0.4, 1.0, 0.05, 0.5) == 1.0

    def test_monotonia_f(self):
        # a parita' di edge, piu' f -> piu' rischio di rovina
        r1 = _F["mh345_ror"](P, B, 0.02, BAR)
        r2 = _F["mh345_ror"](P, B, 0.15, BAR)
        assert r1 < r2

    def test_range(self):
        for p, b, f in ((0.55, 1.2, 0.0875), (0.6, 2.0, 0.05),
                        (0.51, 1.1, 0.02)):
            r = _F["mh345_ror"](p, b, f, 0.5)
            assert 0.0 <= r <= 1.0

    def test_ko_barriera(self):
        with pytest.raises(ValueError):
            _F["mh345_ror"](P, B, 0.05, 1.0)


class TestEdge:
    def test_demo(self):
        e = _F["mh345_edge"](P, B, F_REC)
        assert e == pytest.approx(EDGE, rel=1e-9)
        assert e == pytest.approx(F_REC * (0.55 * 1.2 - 0.45), rel=1e-9)

    def test_formula(self):
        assert _F["mh345_edge"](0.6, 2.0, 0.1) == pytest.approx(
            0.1 * (0.6 * 2.0 - 0.4), rel=1e-9)

    def test_zero_f(self):
        assert _F["mh345_edge"](P, B, 0.0) == 0.0

    def test_negativo(self):
        assert _F["mh345_edge"](0.4, 1.0, 0.05) < 0.0

    def test_ko_f_uno(self):
        with pytest.raises(ValueError):
            _F["mh345_edge"](P, B, 1.0)


class TestFSafe:
    def test_demo_al_limite(self):
        fs = _F["mh345_f_safe"](P, B, BAR, RMAX)
        assert fs == pytest.approx(F_SAFE, rel=1e-9)
        # f_safe tocca il vincolo: R(f_safe) == Rmax
        assert _F["mh345_ror"](P, B, fs, BAR) == pytest.approx(
            RMAX, rel=1e-6)
        assert 0.0 < fs < F_HALF  # vincolo attivo nella demo

    def test_monotonia_rmax(self):
        # vincolo piu' severo -> f_safe piu' piccola
        assert _F["mh345_f_safe"](P, B, BAR, 0.02) < \
            _F["mh345_f_safe"](P, B, BAR, 0.10)

    def test_rmax_largo_ritorna_hi(self):
        # edge fortissimo (drift > 0 anche a f=0.99): R(0.99) <= Rmax
        assert _F["mh345_f_safe"](0.99, 12.0, 0.5, 0.99) == 0.99

    def test_nessun_edge_zero(self):
        assert _F["mh345_f_safe"](0.4, 1.0, 0.5, 0.05) == 0.0

    def test_barriera_severa_piu_piccola(self):
        # barriera piu' profonda (20% = drawdown 80%, tolleranza maggiore)
        # -> R piu' basso a parita' di theta -> f_safe piu' alta
        assert _F["mh345_f_safe"](P, B, 0.2, RMAX) > \
            _F["mh345_f_safe"](P, B, 0.8, RMAX)

    def test_ko_rmax(self):
        for rm in (0.0, 1.0, 1.5):
            with pytest.raises(ValueError):
                _F["mh345_f_safe"](P, B, BAR, rm)

    def test_ko_p(self):
        with pytest.raises(ValueError):
            _F["mh345_f_safe"](1.0, B, BAR, RMAX)


class TestMisure:
    def test_demo(self):
        m = _misure()
        assert m["p"] == pytest.approx(P)
        assert m["b"] == pytest.approx(B, rel=1e-9) == pytest.approx(1.2)
        assert m["f_star"] == pytest.approx(F_STAR, rel=1e-9)
        assert m["f_half"] == pytest.approx(F_HALF, rel=1e-9)
        assert m["f_safe"] == pytest.approx(F_SAFE, rel=1e-9)
        assert m["f_rec"] == pytest.approx(F_REC, rel=1e-9)
        assert m["vincolo_attivo"] is True
        assert m["barriera"] == pytest.approx(BAR)
        assert m["rmax"] == pytest.approx(RMAX)
        assert m["theta"] == pytest.approx(THETA, rel=1e-9)
        assert m["edge"] == pytest.approx(EDGE, rel=1e-9)
        assert m["ror"] == pytest.approx(ROR, rel=1e-9)
        assert m["verdetto"] == VERDETTO

    def test_relazioni(self):
        m = _misure()
        assert m["f_half"] == pytest.approx(m["f_star"] / 2.0, rel=1e-9)
        assert m["f_rec"] == pytest.approx(
            min(m["f_half"], m["f_safe"]), rel=1e-9)
        assert m["ror"] == pytest.approx(m["barriera"] ** THETA, rel=1e-9)

    def test_vincolo_non_attivo(self):
        m = _F["mh345_misure"](0.7, 300.0, 100.0, 0.5, 0.30)
        assert m["vincolo_attivo"] is False
        assert m["f_rec"] == pytest.approx(m["f_half"], rel=1e-12)

    def test_ko_win(self):
        with pytest.raises(ValueError):
            _F["mh345_misure"](P, 0.0, LOSS, BAR, RMAX)

    def test_ko_rmax(self):
        with pytest.raises(ValueError):
            _F["mh345_misure"](P, WIN, LOSS, BAR, 1.0)


class TestVerdetto:
    def test_bloccato(self):
        v = _F["mh345_verdetto"](0.0, 0.0, 1.0, 0.05)
        assert v.startswith("SIZING BLOCCATO")

    def test_vincolo_attivo(self):
        v = _F["mh345_verdetto"](0.05, 0.0875, 0.05, 0.05)
        assert v.startswith("VINCOLO ROVINA ATTIVO")

    def test_half_kelly_ok(self):
        v = _F["mh345_verdetto"](0.10, 0.0875, 0.03, 0.05)
        assert v.startswith("HALF-KELLY ENTRO RMAX")

    def test_verdetto_demo(self):
        assert VERDETTO.startswith("VINCOLO ROVINA ATTIVO")
        assert "5%" in VERDETTO or "5.00" in VERDETTO
