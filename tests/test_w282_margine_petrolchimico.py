"""Test tab282 'Margine petrolchimico: nafta -> etilene': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab282.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("pc282_num", "pc282_pos", "pc282_costo_nafta", "pc282_crediti",
          "pc282_margine", "pc282_breakdown", "pc282_breakeven_nafta",
          "pc282_sensibilita_nafta", "pc282_ricavo_annuo_mln", "pc282_verdetto")
pc282_num = _F["pc282_num"]
pc282_pos = _F["pc282_pos"]
pc282_costo_nafta = _F["pc282_costo_nafta"]
pc282_crediti = _F["pc282_crediti"]
pc282_margine = _F["pc282_margine"]
pc282_breakdown = _F["pc282_breakdown"]
pc282_breakeven_nafta = _F["pc282_breakeven_nafta"]
pc282_sensibilita_nafta = _F["pc282_sensibilita_nafta"]
pc282_ricavo_annuo_mln = _F["pc282_ricavo_annuo_mln"]
pc282_verdetto = _F["pc282_verdetto"]

APP = Path(__file__).parent.parent / "app.py"

TITLE282 = "🧪 Margine petrolchimico: nafta \u2192 etilene"
TITLE283 = "🛢️ Carry petrolio: contango & stoccaggio fisico"
TITLE284 = "🏭 Unit commitment CCGT: accendere o no?"
TITLE285 = "🛛️ Differenziali greggio: sweet vs sour"
TITLE286 = "⛽ Basis gas TTF–PSV"
TITLE287 = "🚢⚡ Rigassificazione GNL: margine terminale"
TITLE288 = "⚡🔥 Clean spark spread: margine centrale a gas"
TITLE289 = "⚫🔥 Clean dark spread: margine centrale a carbone"
TITLE290 = "🔀💰 PTR transfrontaliero: vale il prezzo d'asta?"
TITLE291 = "📊💹 Sharpe & Sortino: la strategia rende davvero?"
TITLE292 = "🪓📊 Component VaR: quale posizione tagliare per prima?"
TITLE293 = "🛡📉 Hedge ratio ottimale: quanto coprire con i futures?"
TITLE294 = "🧪📉 Backtest del VaR: il modello tiene?"
TITLE295 = "🧪🛡 Backtest dell'ES: la coda e' sottostimata?"
TITLE296 = "🪓🛡 Component ES: chi contribuisce alla coda?"
TITLE297 = "➕📊 Marginal VaR: quanto rischio aggiunge il nuovo trade?"
TITLE298 = "🚦📏 Limite VaR: quanto margine resta?"
TITLE299 = "🧪⚡ Stress test: quanto perde il book negli scenari?"
TITLE300 = "🧮📊 Rapporto di diversificazione: quanto rischio risparmia il book?"
TITLE301 = "🛡️🔍 Rischio di modello: quale VaR credere?"
TITLE302 = "✂️📉 Incremental VaR: quanto rischio togli chiudendo la posizione?"
TITLE281 = "🛢️ Crack spread: margine raffinazione 3-2-1"
TITLE280 = "🚢 LNG vs gasdotto: costo delivered"

NAFTA, RESA, ETILENE = 470.0, 3.28, 1000.0
CREDITI = 0.52 * 900.0 + 0.15 * 1100.0 + 70.0
VARCOST = 110.0
COSTO_NAFTA_ATTESO = NAFTA * RESA
MARGINE_ATTESO = ETILENE + CREDITI - COSTO_NAFTA_ATTESO - VARCOST
BE_ATTESO = (ETILENE + CREDITI - VARCOST) / RESA


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab282:
    def test_tab282_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 302
        assert TITLE282 in titoli
        assert "tab282" in dvars
        assert "tab282" in withs
        assert titoli[dvars.index("tab282")] == TITLE282
        assert titoli[-1] == TITLE302
        keys = re.findall(r'key="(pc282_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_280_281_282(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab280")] == TITLE280
        assert titoli[dvars.index("tab281")] == TITLE281
        assert titoli[dvars.index("tab282")] == TITLE282
        assert titoli[dvars.index("tab283")] == TITLE283
        assert titoli[dvars.index("tab284")] == TITLE284
        assert titoli[dvars.index("tab285")] == TITLE285


class TestPc282Validatori:
    def test_num_ok(self):
        assert pc282_num(3, "x") == 3.0
        assert pc282_num(2.5, "x") == 2.5

    def test_num_ko(self):
        with pytest.raises(ValueError):
            pc282_num(True, "x")
        with pytest.raises(ValueError):
            pc282_num("3", "x")
        with pytest.raises(ValueError):
            pc282_num(float("nan"), "x")
        with pytest.raises(ValueError):
            pc282_num(float("inf"), "x")

    def test_pos_ok(self):
        assert pc282_pos(0, "x") == 0.0
        assert pc282_pos(470, "x") == 470.0

    def test_pos_ko(self):
        with pytest.raises(ValueError):
            pc282_pos(-0.1, "x")


class TestPc282CostoNafta:
    def test_base(self):
        assert pc282_costo_nafta(NAFTA, RESA) == pytest.approx(COSTO_NAFTA_ATTESO)

    def test_lineare_resa(self):
        assert pc282_costo_nafta(NAFTA, 2 * RESA) == pytest.approx(2 * COSTO_NAFTA_ATTESO)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            pc282_costo_nafta(NAFTA, 0.0)
        with pytest.raises(ValueError):
            pc282_costo_nafta(NAFTA, -1.0)
        with pytest.raises(ValueError):
            pc282_costo_nafta(-1.0, RESA)


class TestPc282Crediti:
    def test_base(self):
        assert pc282_crediti(0.52, 900.0, 0.15, 1100.0, 70.0) == pytest.approx(CREDITI)

    def test_somma_componenti(self):
        c = pc282_crediti(0.5, 1000.0, 0.1, 1000.0, 50.0)
        assert c == pytest.approx(500.0 + 100.0 + 50.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            pc282_crediti(-0.1, 900.0, 0.15, 1100.0, 70.0)
        with pytest.raises(ValueError):
            pc282_crediti(0.52, 900.0, 0.15, 1100.0, -1.0)


class TestPc282Margine:
    def test_base(self):
        assert pc282_margine(ETILENE, COSTO_NAFTA_ATTESO, CREDITI, VARCOST) == pytest.approx(MARGINE_ATTESO)

    def test_formula(self):
        assert pc282_margine(1000.0, 1500.0, 600.0, 100.0) == pytest.approx(0.0)
        assert pc282_margine(1000.0, 2000.0, 600.0, 100.0) == pytest.approx(-500.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            pc282_margine(ETILENE, -1.0, CREDITI, VARCOST)


class TestPc282Breakdown:
    def test_somma(self):
        b = pc282_breakdown(ETILENE, COSTO_NAFTA_ATTESO, CREDITI, VARCOST)
        assert b["etilene"] == pytest.approx(ETILENE)
        assert b["crediti_coprodotti"] == pytest.approx(CREDITI)
        assert b["nafta"] == pytest.approx(-COSTO_NAFTA_ATTESO)
        assert b["costi_variabili"] == pytest.approx(-VARCOST)
        assert b["margine"] == pytest.approx(MARGINE_ATTESO)
        assert b["margine"] == pytest.approx(b["etilene"] + b["crediti_coprodotti"] + b["nafta"] + b["costi_variabili"])


class TestPc282Breakeven:
    def test_base(self):
        assert pc282_breakeven_nafta(ETILENE, CREDITI, VARCOST, RESA) == pytest.approx(BE_ATTESO)

    def test_coerente_con_margine(self):
        be = pc282_breakeven_nafta(ETILENE, CREDITI, VARCOST, RESA)
        assert pc282_margine(ETILENE, pc282_costo_nafta(be, RESA), CREDITI, VARCOST) == pytest.approx(0.0, abs=1e-9)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            pc282_breakeven_nafta(ETILENE, CREDITI, VARCOST, 0.0)
        with pytest.raises(ValueError):
            pc282_breakeven_nafta(ETILENE, CREDITI, VARCOST, -1.0)


class TestPc282Sensibilita:
    def test_struttura(self):
        righe = pc282_sensibilita_nafta(NAFTA, ETILENE, CREDITI, VARCOST, RESA, 5)
        assert len(righe) == 5
        assert righe[0]["nafta"] == pytest.approx(235.0)
        assert righe[-1]["nafta"] == pytest.approx(705.0)
        assert set(righe[0]) == {"nafta", "margine"}

    def test_decrescente_e_centro(self):
        righe = pc282_sensibilita_nafta(NAFTA, ETILENE, CREDITI, VARCOST, RESA, 5)
        margini = [r["margine"] for r in righe]
        assert all(b < a for a, b in zip(margini, margini[1:]))
        assert righe[2]["margine"] == pytest.approx(MARGINE_ATTESO)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            pc282_sensibilita_nafta(0.0, ETILENE, CREDITI, VARCOST, RESA)
        with pytest.raises(ValueError):
            pc282_sensibilita_nafta(NAFTA, ETILENE, CREDITI, VARCOST, 0.0)
        with pytest.raises(ValueError):
            pc282_sensibilita_nafta(NAFTA, ETILENE, CREDITI, VARCOST, RESA, 2)


class TestPc282RicavoAnnuo:
    def test_base(self):
        atteso = MARGINE_ATTESO * 450 * 1000 * 0.92 / 1e6
        assert pc282_ricavo_annuo_mln(MARGINE_ATTESO, 450, 92.0) == pytest.approx(atteso)

    def test_zero(self):
        assert pc282_ricavo_annuo_mln(MARGINE_ATTESO, 450, 0.0) == pytest.approx(0.0)
        assert pc282_ricavo_annuo_mln(0.0, 450, 92.0) == pytest.approx(0.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            pc282_ricavo_annuo_mln(MARGINE_ATTESO, -1.0, 92.0)
        with pytest.raises(ValueError):
            pc282_ricavo_annuo_mln(MARGINE_ATTESO, 450, 100.1)


class TestPc282Verdetto:
    def test_positivo(self):
        r = pc282_verdetto(51.4, 30.0)
        assert r["verdetto"] == "positivo"
        assert r["margine"] == pytest.approx(51.4)

    def test_in_linea(self):
        assert pc282_verdetto(10.0, 30.0)["verdetto"] == "in_linea"
        assert pc282_verdetto(-30.0, 30.0)["verdetto"] == "in_linea"

    def test_negativo(self):
        r = pc282_verdetto(-100.0, 30.0)
        assert r["verdetto"] == "negativo"

    def test_invalidi(self):
        with pytest.raises(ValueError):
            pc282_verdetto(1.0, -0.5)
