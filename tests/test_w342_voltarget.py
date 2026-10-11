
"""Test tab342 '🎯 Volatilità target: il sizing a volatilità costante': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica del volatility targeting:
validatori, parse della serie di rendimenti %, volatilita' annualizzata
(std campionaria * sqrt(periodi/anno)), misure (vol realizzata, m grezzo,
m cappato, flag capped, equity 1x e con leva; m None se vol ~ 0) e verdetto
a 5 stati (IN LINEA / AUMENTA ESPOSIZIONE / RIDUCI ESPOSIZIONE /
LEVA AL MASSIMO / NON MISURABILE).
"""
import re
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh342_num", "mh342_parse_serie", "mh342_vol_ann",
           "mh342_misure", "mh342_verdetto")

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
TITLE370 = "Kelly e drawdown: probabilità di toccare un max drawdown"
TITLE371 = "Kelly frazionario: frazione ottima per un budget di volatilità"
TITLE372 = "Monte Carlo: VaR e Expected Shortfall di una posizione power"
TITLE373 = "Kelly con limite VaR: sizing con vincolo di perdita massima"
TITLE374 = "Component VaR: contributo al rischio per posizione"
TITLE341 = "📐 K-ratio: la regolarità della crescita dell'equity"
TITLE340 = "📉 Calmar ratio: il rendimento annuo per unità di max drawdown"
TITLE339 = "📉 Sortino ratio: il rendimento per unità di rischio al ribasso"
SERIE_DEMO = '1.2\n0.8\n1.5\n-0.6\n0.9\n1.1\n-4.8\n-2.5\n1.6\n0.7\n-0.9\n1.3\n0.8\n1.0\n1.4\n-1.2\n0.6\n0.9\n1.7\n-0.5\n1.1\n0.4\n-0.7\n1.2\n0.9\n0.5\n1.6\n-1.4\n0.8\n1.0\n0.6\n1.3\n-0.8\n0.9\n0.7\n1.2'

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N_PER = 36
PPY = 12
TGT = 10.0
LEVMAX = 3.0
VOL_REAL = 4.579571616480759
M_RAW = 2.183610354298739
M = 2.183610354298739
CAPPED = False
STATO = "AUMENTA ESPOSIZIONE"
VERDETTO = "AUMENTA ESPOSIZIONE (2.18x): la strategia e' meno volatile del target: si puo' scalare su restando nel budget di rischio. Vol realizzata 4.58% annua contro target 10.00%."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _demo():
    return _F["mh342_parse_serie"](SERIE_DEMO, "strategia")


class TestRegistry342:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 374
        assert "tab342" in dvars
        assert "tab342" in withs

    def test_titoli_allineati_339_340_341_342(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab339")] == TITLE339
        assert titoli[dvars.index("tab340")] == TITLE340
        assert titoli[dvars.index("tab341")] == TITLE341
        assert titoli[dvars.index("tab342")] == TITLE342

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert dvars[-1] == "tab374"
        assert titoli[-1] == TITLE374
        assert withs[-1] == "tab374"


class TestNum:
    def test_num_ok(self):
        assert _F["mh342_num"](1.5, "x") == 1.5
        assert _F["mh342_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh342_num"](bad, "x")


class TestParse:
    def test_parse_ok(self):
        a = _F["mh342_parse_serie"](SERIE_DEMO, "strategia")
        assert len(a) == N_PER == 36
        assert a[0] == pytest.approx(1.2)

    def test_parse_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh342_parse_serie"]("\n".join(["1.0"] * 11), "strategia")

    def test_parse_ko_numero(self):
        righe = SERIE_DEMO.split("\n")
        righe[5] = "abc"
        with pytest.raises(ValueError):
            _F["mh342_parse_serie"]("\n".join(righe), "strategia")

    def test_parse_ko_non_testo(self):
        with pytest.raises(ValueError):
            _F["mh342_parse_serie"]([1.0] * 36, "strategia")

    def test_parse_virgola(self):
        a = _F["mh342_parse_serie"]("\n".join(["1,5"] * 36), "x")
        assert a[0] == pytest.approx(1.5)


class TestVolAnn:
    def test_demo(self):
        v = _F["mh342_vol_ann"](_demo(), PPY)
        assert v == pytest.approx(VOL_REAL, rel=1e-9)
        assert v > 0

    def test_formula(self):
        import math
        r = np.array([1.0, -1.0, 2.0, -2.0] * 9)
        v = _F["mh342_vol_ann"](r, 12)
        assert v == pytest.approx(r.std(ddof=1) * math.sqrt(12), rel=1e-9)

    def test_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh342_vol_ann"](np.array([1.0]), 12)

    def test_ko_ppy(self):
        with pytest.raises(ValueError):
            _F["mh342_vol_ann"](_demo(), 0)


class TestMisure:
    def _m(self):
        return _F["mh342_misure"](_demo(), PPY, TGT, LEVMAX)

    def test_demo(self):
        m = self._m()
        assert m["n"] == N_PER == 36
        assert m["ppy"] == PPY == 12
        assert m["vol_real"] == pytest.approx(VOL_REAL, rel=1e-9)
        assert m["m_raw"] == pytest.approx(M_RAW, rel=1e-9)
        assert m["m"] == pytest.approx(M, rel=1e-9)
        assert m["capped"] == CAPPED is False
        assert len(m["eq_1x"]) == len(m["eq_lev"]) == N_PER + 1
        assert m["eq_1x"][0] == pytest.approx(100.0)
        assert m["eq_lev"][0] == pytest.approx(100.0)

    def test_relazione_m(self):
        m = self._m()
        assert m["m_raw"] == pytest.approx(m["vol_target"] / m["vol_real"],
                                           rel=1e-9)
        assert m["m"] == pytest.approx(min(m["m_raw"], m["lev_max"]),
                                       rel=1e-9)

    def test_capped(self):
        # vol piccola ma non nulla: m_raw oltre la leva max -> cappato
        r = np.array([0.05, -0.05] * 18)
        m = _F["mh342_misure"](r, 12, 10.0, 3.0)
        assert m["capped"] is True
        assert m["m"] == pytest.approx(3.0)
        assert m["m_raw"] > 3.0

    def test_vol_nulla(self):
        r = np.zeros(36)
        m = _F["mh342_misure"](r, 12, 10.0, 3.0)
        assert m["m_raw"] is None
        assert m["m"] is None
        assert m["eq_lev"] is None

    def test_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh342_misure"](np.ones(11), 12, 10.0, 3.0)

    def test_ko_target(self):
        with pytest.raises(ValueError):
            _F["mh342_misure"](_demo(), 12, 0.0, 3.0)

    def test_ko_levmax(self):
        with pytest.raises(ValueError):
            _F["mh342_misure"](_demo(), 12, 10.0, 0.5)


class TestVerdetto:
    def test_in_linea(self):
        v = _F["mh342_verdetto"](1.0, 1.0, False, 10.0, 10.0)
        assert v.startswith("SIZING IN LINEA")

    def test_in_linea_soglia_09(self):
        v = _F["mh342_verdetto"](0.9, 0.9, False, 11.1, 10.0)
        assert v.startswith("SIZING IN LINEA")

    def test_in_linea_soglia_11(self):
        v = _F["mh342_verdetto"](1.1, 1.1, False, 9.1, 10.0)
        assert v.startswith("SIZING IN LINEA")

    def test_aumenta(self):
        v = _F["mh342_verdetto"](2.2, 2.2, False, 4.5, 10.0)
        assert v.startswith("AUMENTA ESPOSIZIONE")

    def test_riduci(self):
        v = _F["mh342_verdetto"](0.5, 0.5, False, 20.0, 10.0)
        assert v.startswith("RIDUCI ESPOSIZIONE")

    def test_leva_max(self):
        v = _F["mh342_verdetto"](4.0, 3.0, True, 2.5, 10.0)
        assert v.startswith("SIZING LEVA AL MASSIMO")

    def test_non_misurabile(self):
        v = _F["mh342_verdetto"](None, None, False, 0.0, 10.0)
        assert v.startswith("SIZING NON MISURABILE")

    def test_verdetto_demo(self):
        v = _F["mh342_verdetto"](M_RAW, M, CAPPED, VOL_REAL, TGT)
        assert v == VERDETTO
        assert v.startswith(STATO)

    def test_verdetto_ko_tipo(self):
        with pytest.raises(ValueError):
            _F["mh342_verdetto"]("x", 1.0, False, 10.0, 10.0)
