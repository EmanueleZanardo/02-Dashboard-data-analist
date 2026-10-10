"""Test tab331 '⛵ Tempo di recupero: quanto resta sott'acqua l'equity': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica del tempo di recupero: validatori,
parse equity, scomposizione in episodi di drawdown (picco/fondo/recupero),
statistiche (durata media/max, % tempo sott'acqua, conversione in mesi) e
verdetto a 3 stati (soglie 3 / 9 mesi medi).
"""
import math
import re
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh331_num", "mh331_parse_equity", "mh331_episodi",
           "mh331_statistiche", "mh331_verdetto")

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
TITLE330 = "🔍📉 Martin ratio: il Calmar che guarda tutto il dolore"
TITLE329 = "🌊📉 CDaR: il drawdown medio oltre la soglia (il VaR dei drawdown)"
TITLE328 = "🔻 Burke ratio: il drawdown penalizzato al quadrato"
SERIE_DEMO = '100\n103\n106\n109\n112\n115\n118\n119\n120\n116\n111\n106\n101\n97\n94\n100\n106\n112\n118\n124\n130\n126\n121\n117\n115\n114\n118\n123\n128\n133\n138\n142\n139\n136\n133\n130\n134\n138\n142\n146\n149\n152\n154\n156\n158\n160\n162\n164'

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N_EP = 3
PCT = 50.0
DUR_MED = 9.0
DUR_MAX = 11
MESI_MED = 9.0
MESI_MAX = 11.0
MAXDD = 21.666666666666668
EP1_PICCO = 9
EP1_PROF = 21.666666666666668
EP1_DUR = 11
STATO = "tempo di recupero MODERATO"
VERDETTO = "tempo di recupero MODERATO: in media l'equity torna al picco in 9.0 mesi (sott'acqua il 50.0% del tempo): i drawdown si chiudono ma il capitale resta bloccato per trimestri, pianificare liquidita' e margin."


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _eq_demo():
    return _F["mh331_parse_equity"](SERIE_DEMO)


class TestRegistry331:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 354
        assert TITLE331 in titoli
        assert "tab331" in dvars
        assert "    with tab331:" in src

    def test_titoli_allineati_328_329_330_331(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab328")] == TITLE328
        assert titoli[dvars.index("tab329")] == TITLE329
        assert titoli[dvars.index("tab330")] == TITLE330
        assert titoli[dvars.index("tab331")] == TITLE331

    def test_ultima_tab(self):
        _, titoli, dvars, withs = _registry()
        assert titoli[-1] == TITLE354
        assert dvars[-1] == "tab354"
        assert withs[-1] == "tab354"


class TestNum:
    def test_num_ok(self):
        assert _F["mh331_num"](3, "x") == 3.0
        assert _F["mh331_num"](2.5, "x") == 2.5

    def test_num_ko(self):
        for bad in (True, float("nan"), float("inf"), "x", None):
            with pytest.raises(ValueError):
                _F["mh331_num"](bad, "x")


class TestParse:
    def test_parse_ok(self):
        eq = _F["mh331_parse_equity"](SERIE_DEMO)
        assert len(eq) == 48
        assert (eq > 0).all()

    def test_parse_ko_pochi(self):
        with pytest.raises(ValueError):
            _F["mh331_parse_equity"]("\n".join(["100"] * 29))

    def test_parse_ko_non_positivo(self):
        with pytest.raises(ValueError):
            _F["mh331_parse_equity"]("\n".join(["100"] * 29 + ["0"]))

    def test_parse_ko_numero(self):
        with pytest.raises(ValueError):
            _F["mh331_parse_equity"]("\n".join(["100"] * 29 + ["abc"]))

    def test_parse_ko_non_testo(self):
        with pytest.raises(ValueError):
            _F["mh331_parse_equity"]([100.0] * 30)

    def test_parse_virgola(self):
        eq = _F["mh331_parse_equity"]("\n".join(["100,5"] * 30))
        assert eq[0] == pytest.approx(100.5)


class TestEpisodi:
    def test_un_episodio(self):
        # picco 110 (per.2), fondo 95, recupero a 110 (per.6): durata 4
        eps = _F["mh331_episodi"]([100, 110, 105, 100, 95, 110, 120] +
                                 [120.0] * 23)
        assert len(eps) == 1
        e = eps[0]
        assert e["picco"] == 2
        assert e["profondita_max"] == pytest.approx(15.0 / 110.0)
        assert e["durata"] == 4
        assert e["recuperato"] is True
        assert e["periodi_sottacqua"] == 3

    def test_due_episodi(self):
        eps = _F["mh331_episodi"]([100, 110, 105, 112, 108, 115] +
                                 [115.0] * 24)
        assert len(eps) == 2
        assert [e["picco"] for e in eps] == [2, 4]
        assert [e["durata"] for e in eps] == [2, 2]
        assert all(e["recuperato"] for e in eps)

    def test_non_recuperato(self):
        eps = _F["mh331_episodi"]([100, 110, 105, 108] + [108.0] * 26)
        assert len(eps) == 1
        e = eps[0]
        assert e["recuperato"] is False
        assert e["durata"] is None
        assert e["periodi_sottacqua"] == 28
        assert e["profondita_max"] == pytest.approx(5.0 / 110.0)

    def test_nessun_episodio(self):
        eps = _F["mh331_episodi"]([100.0 + i for i in range(30)])
        assert eps == []

    def test_partenza_in_discesa(self):
        # picco al periodo 1, poi recupero: durata 3
        eps = _F["mh331_episodi"]([100, 95, 90, 110, 115] + [115.0] * 25)
        assert len(eps) == 1
        e = eps[0]
        assert e["picco"] == 1
        assert e["profondita_max"] == pytest.approx(0.10)
        assert e["durata"] == 3
        assert e["recuperato"] is True

    def test_pochi_ko(self):
        with pytest.raises(ValueError):
            _F["mh331_episodi"]([100.0] * 29)

    def test_demo_tre_episodi(self):
        eps = _F["mh331_episodi"](_eq_demo())
        assert len(eps) == N_EP == 3
        assert eps[0]["picco"] == EP1_PICCO == 9
        assert eps[0]["profondita_max"] * 100.0 == pytest.approx(EP1_PROF)
        assert eps[0]["durata"] == EP1_DUR == 11
        assert all(e["recuperato"] for e in eps)


class TestStatistiche:
    def test_demo(self):
        s = _F["mh331_statistiche"](_eq_demo(), 12)
        assert s["n"] == N_EP == 3
        assert s["n_recuperati"] == 3
        assert s["durata_media"] == pytest.approx(DUR_MED)
        assert s["durata_max"] == DUR_MAX == 11
        assert s["pct_sottacqua"] == pytest.approx(PCT)
        assert s["max_dd"] * 100.0 == pytest.approx(MAXDD)
        assert s["mesi_medi"] == pytest.approx(MESI_MED)
        assert s["mesi_max"] == pytest.approx(MESI_MAX)
        assert s["in_corso"] is False
        assert s["sottacqua_da"] is None

    def test_chiavi(self):
        s = _F["mh331_statistiche"](_eq_demo(), 12)
        for k in ("n", "n_recuperati", "durata_media", "durata_max",
                  "pct_sottacqua", "max_dd", "mesi_medi", "mesi_max",
                  "in_corso", "sottacqua_da"):
            assert k in s

    def test_pct_invariante(self):
        eq = _eq_demo()
        s = _F["mh331_statistiche"](eq, 12)
        eps = _F["mh331_episodi"](eq)
        att = 100.0 * sum(e["periodi_sottacqua"] for e in eps) / len(eq)
        assert s["pct_sottacqua"] == pytest.approx(att)
        assert 0.0 <= s["pct_sottacqua"] <= 100.0

    def test_media_solo_recuperati(self):
        # 1 episodio chiuso (durata 2) + 1 ancora aperto: la media usa solo il chiuso
        eq = ([100, 110, 105, 112] + [112.0, 108, 105] + [105.0] * 23)
        s = _F["mh331_statistiche"](eq, 12)
        assert s["n"] == 2
        assert s["n_recuperati"] == 1
        assert s["durata_media"] == pytest.approx(2.0)
        assert s["in_corso"] is True
        assert s["sottacqua_da"] == 25
        assert s["mesi_medi"] == pytest.approx(2.0)

    def test_scaling_mesi(self):
        s = _F["mh331_statistiche"](_eq_demo(), 52)
        assert s["mesi_medi"] == pytest.approx(DUR_MED * 12.0 / 52.0)
        assert s["mesi_max"] == pytest.approx(DUR_MAX * 12.0 / 52.0)

    def test_max_dd_coerente(self):
        s = _F["mh331_statistiche"](_eq_demo(), 12)
        eps = _F["mh331_episodi"](_eq_demo())
        assert s["max_dd"] == pytest.approx(max(e["profondita_max"]
                                               for e in eps))

    def test_senza_episodi(self):
        s = _F["mh331_statistiche"]([100.0 + i for i in range(30)], 12)
        assert s["n"] == 0
        assert s["durata_media"] is None
        assert s["mesi_medi"] is None
        assert s["pct_sottacqua"] == 0.0
        assert s["in_corso"] is False

    def test_p_ko(self):
        with pytest.raises(ValueError):
            _F["mh331_statistiche"](_eq_demo(), 0)


class TestVerdetto:
    def test_verdetto_eccellente(self):
        v = _F["mh331_verdetto"](2.0, 10.0, False)
        assert v.startswith("tempo di recupero ECCELLENTE")

    def test_verdetto_soglia_eccellente(self):
        v = _F["mh331_verdetto"](3.0, 10.0, False)
        assert v.startswith("tempo di recupero ECCELLENTE")

    def test_verdetto_moderato(self):
        v = _F["mh331_verdetto"](9.0, 50.0, False)
        assert v.startswith("tempo di recupero MODERATO")

    def test_verdetto_soglia_moderato(self):
        v = _F["mh331_verdetto"](9.0, 50.0, False)
        assert v.startswith("tempo di recupero MODERATO")

    def test_verdetto_debole(self):
        v = _F["mh331_verdetto"](9.01, 50.0, False)
        assert v.startswith("tempo di recupero DEBOLE")

    def test_verdetto_nessun_episodio(self):
        v = _F["mh331_verdetto"](None, 0.0, False)
        assert v.startswith("nessun episodio di drawdown")

    def test_verdetto_mai_recuperato(self):
        v = _F["mh331_verdetto"](None, 20.0, True, 5)
        assert v.startswith("tempo di recupero NON MISURABILE")
        assert "ancora aperto" in v

    def test_verdetto_nota_in_corso(self):
        v = _F["mh331_verdetto"](2.0, 10.0, True, 4)
        assert v.startswith("tempo di recupero ECCELLENTE")
        assert "ancora aperto" in v

    def test_verdetto_ko_nan(self):
        with pytest.raises(ValueError):
            _F["mh331_verdetto"](float("nan"), 10.0, False)

    def test_verdetto_ko_tipo(self):
        with pytest.raises(ValueError):
            _F["mh331_verdetto"]("x", 10.0, False)

    def test_verdetto_demo(self):
        s = _F["mh331_statistiche"](_eq_demo(), 12)
        v = _F["mh331_verdetto"](s["mesi_medi"], s["pct_sottacqua"],
                                 s["in_corso"], s["sottacqua_da"])
        assert v == VERDETTO
        assert v.startswith(STATO)
