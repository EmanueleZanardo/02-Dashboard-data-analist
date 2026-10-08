"""Test tab278 'Stress climatico: domanda e prezzo': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab278.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("sc278_num", "sc278_domanda_mw", "sc278_prezzo_shock",
          "sc278_energia_mwh", "sc278_costo", "sc278_scenario",
          "sc278_confronto", "sc278_extra", "sc278_sensibilita_temp")
sc278_num = _F["sc278_num"]
sc278_domanda_mw = _F["sc278_domanda_mw"]
sc278_prezzo_shock = _F["sc278_prezzo_shock"]
sc278_energia_mwh = _F["sc278_energia_mwh"]
sc278_costo = _F["sc278_costo"]
sc278_scenario = _F["sc278_scenario"]
sc278_confronto = _F["sc278_confronto"]
sc278_extra = _F["sc278_extra"]
sc278_sensibilita_temp = _F["sc278_sensibilita_temp"]

APP = Path(__file__).parent.parent / "app.py"

TITLE278 = "🌡️ Stress climatico: domanda e prezzo"
TITLE279 = "🌪️ Derivati meteo: pricing HDD/CDD"
TITLE280 = "🚢 LNG vs gasdotto: costo delivered"
TITLE281 = "🛢️ Crack spread: margine raffinazione 3-2-1"
TITLE282 = "🧪 Margine petrolchimico: nafta → etilene"
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
TITLE277 = "⚡ Aste MI: scostamenti vs MGP"


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab278:
    def test_tab278_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 301
        assert TITLE278 in titoli
        assert "tab278" in dvars
        assert "tab278" in withs
        assert titoli[dvars.index("tab278")] == TITLE278
        assert titoli[-1] == TITLE301
        keys = re.findall(r'key="(sc278_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_277_278(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab277")] == TITLE277
        assert titoli[dvars.index("tab278")] == TITLE278
        assert titoli[dvars.index("tab279")] == TITLE279
        assert titoli[dvars.index("tab280")] == TITLE280
        assert titoli[dvars.index("tab281")] == TITLE281
        assert titoli[dvars.index("tab282")] == TITLE282
        assert titoli[dvars.index("tab283")] == TITLE283
        assert titoli[dvars.index("tab284")] == TITLE284
        assert titoli[dvars.index("tab285")] == TITLE285

    def test_helper_definiti_prima_della_ui(self):
        src = APP.read_text(encoding="utf-8")
        i_ws = src.index("if workspace ==")
        for fn in ("sc278_num", "sc278_domanda_mw", "sc278_prezzo_shock",
                   "sc278_energia_mwh", "sc278_costo", "sc278_scenario",
                   "sc278_confronto", "sc278_extra", "sc278_sensibilita_temp"):
            assert src.index(f"def {fn}(") < i_ws
            assert src.index("    with tab278:") > i_ws


class TestSc278Num:
    def test_ok(self):
        assert sc278_num(1000, "x") == 1000.0

    def test_invalidi(self):
        import math
        for bad in (True, math.nan, math.inf, "1000", None):
            with pytest.raises(ValueError):
                sc278_num(bad, "x")


class TestSc278DomandaPrezzo:
    def test_domanda(self):
        assert sc278_domanda_mw(1000, 5, 40) == 1200.0
        assert sc278_domanda_mw(1000, -8, 60) == 520.0
        assert sc278_domanda_mw(1000, 0, 40) == 1000.0

    def test_domanda_invalidi(self):
        with pytest.raises(ValueError):
            sc278_domanda_mw(0, 5, 40)
        with pytest.raises(ValueError):
            sc278_domanda_mw(1000, 5, -1)
        with pytest.raises(ValueError):
            sc278_domanda_mw(100, -10, 40)  # domanda non positiva

    def test_prezzo_shock(self):
        assert sc278_prezzo_shock(100, 1000, 1200, 0.5) == pytest.approx(110.0)
        assert sc278_prezzo_shock(100, 1000, 1000, 0.5) == pytest.approx(100.0)
        assert sc278_prezzo_shock(100, 1000, 800, 0.5) == pytest.approx(90.0)

    def test_prezzo_invalidi(self):
        with pytest.raises(ValueError):
            sc278_prezzo_shock(-5, 1000, 1200, 0.5)
        with pytest.raises(ValueError):
            sc278_prezzo_shock(100, 0, 1200, 0.5)
        with pytest.raises(ValueError):
            sc278_prezzo_shock(100, 1000, 1200, -0.5)


class TestSc278EnergiaCosto:
    def test_energia(self):
        assert sc278_energia_mwh(1200, 72) == 86400.0
        with pytest.raises(ValueError):
            sc278_energia_mwh(1200, 0)
        with pytest.raises(ValueError):
            sc278_energia_mwh(-5, 72)

    def test_costo(self):
        assert sc278_costo(86400, 110.0) == pytest.approx(9504000.0)
        assert sc278_costo(0, 110.0) == 0.0
        with pytest.raises(ValueError):
            sc278_costo(100, -1.0)


class TestSc278ScenarioConfronto:
    def test_scenario(self):
        s = sc278_scenario("caldo", 1000, 100, 5, 40, 0.5, 72)
        assert s["domanda_mw"] == 1200.0
        assert s["prezzo_eur_mwh"] == pytest.approx(110.0)
        assert s["energia_mwh"] == 86400.0
        assert s["costo_eur"] == pytest.approx(86400.0 * 110.0)
        assert s["delta_temp_c"] == 5.0

    def test_confronto(self):
        sce = sc278_confronto(1000, 100, 5, 8, 40, 60, 0.5, 3)
        assert len(sce) == 3
        base, caldo, freddo = sce
        assert base["delta_temp_c"] == 0.0
        assert caldo["delta_temp_c"] == 5.0
        assert freddo["delta_temp_c"] == 8.0
        assert caldo["domanda_mw"] == 1200.0
        assert freddo["domanda_mw"] == 1480.0
        assert caldo["costo_eur"] > base["costo_eur"]
        assert freddo["costo_eur"] > base["costo_eur"]

    def test_confronto_invalidi(self):
        with pytest.raises(ValueError):
            sc278_confronto(1000, 100, 5, 8, 40, 60, 0.5, 0)

    def test_extra(self):
        sce = sc278_confronto(1000, 100, 5, 8, 40, 60, 0.5, 3)
        ex = sc278_extra(sce[1], sce[0])
        assert ex["extra_eur"] == pytest.approx(sce[1]["costo_eur"] - sce[0]["costo_eur"])
        assert ex["extra_pct"] == pytest.approx(
            ex["extra_eur"] / sce[0]["costo_eur"] * 100.0)
        assert ex["extra_eur"] > 0


class TestSc278Sensibilita:
    def test_base(self):
        righe = sc278_sensibilita_temp(1000, 100, 40, 0.5, 72, 10, 5)
        assert len(righe) == 3
        assert righe[0]["delta_temp_c"] == 0.0
        assert righe[0]["extra_eur"] == 0.0
        assert righe[-1]["delta_temp_c"] == 10.0
        ext = [r["extra_eur"] for r in righe]
        assert all(b >= a for a, b in zip(ext, ext[1:]))
        assert set(righe[0]) == {"delta_temp_c", "domanda_mw",
                                 "prezzo_eur_mwh", "extra_eur"}

    def test_monotonia(self):
        righe = sc278_sensibilita_temp(1000, 100, 40, 0.5, 72, 12, 3)
        assert len(righe) == 5
        ext = [r["extra_eur"] for r in righe]
        assert all(b > a for a, b in zip(ext, ext[1:]))

    def test_invalidi(self):
        with pytest.raises(ValueError):
            sc278_sensibilita_temp(1000, 100, 40, 0.5, 72, 0, 5)
        with pytest.raises(ValueError):
            sc278_sensibilita_temp(1000, 100, 40, 0.5, 72, 10, 0)
