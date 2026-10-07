"""Test di regressione per le tab senza copertura dedicata:
tab133 (Regimi di prezzo), tab134 (Report di periodo),
tab175 (Matrice costo giornoxora), tab229 (Valore del forecast),
tab230 (Budget di rischio).

Funzioni pure estratte da app.py via AST (tests/appfuncs), stile QA:
numeri calcolati a mano + validazione input + determinismo + registry.

Nota QA: tab230 (calcola_budget_rischio) aveva un NameError latente
(`math.sqrt` senza `import math` in scope): con input validi la funzione
sollevava NameError invece di ritornare il dict. Il fix (import math
locale, come le altre helper del file) e' coperto da questi test.
"""

import re
from pathlib import Path

import numpy as np
import pandas as pd

from appfuncs import load

_F = load(
    "calcola_regimi_prezzo",
    "calcola_riepilogo_periodo",
    "genera_csv_report",
    "calcola_matrice_costo_settimana",
    "calcola_valore_forecast",
    "calcola_budget_rischio",
    "fascia_oraria",
)
calcola_regimi_prezzo = _F["calcola_regimi_prezzo"]
calcola_riepilogo_periodo = _F["calcola_riepilogo_periodo"]
genera_csv_report = _F["genera_csv_report"]
calcola_matrice_costo_settimana = _F["calcola_matrice_costo_settimana"]
calcola_valore_forecast = _F["calcola_valore_forecast"]
calcola_budget_rischio = _F["calcola_budget_rischio"]

APP = Path(__file__).parent.parent / "app.py"


def _titoli():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    return re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])


def _serie_piatta(prezzo, giorni, inizio="2026-01-05"):
    idx = pd.date_range(inizio, periods=24 * giorni, freq="h")
    return pd.Series(float(prezzo), index=idx)


# ------------------------------------------------------- registry
class TestRegistryScoperte:
    def test_tab133_dichiarata(self):
        titoli = _titoli()
        assert len(titoli) == 290
        assert titoli[132] == "🔀 Regimi di prezzo"

    def test_tab134_dichiarata(self):
        titoli = _titoli()
        assert len(titoli) == 290
        assert titoli[133] == "📑 Report di periodo"

    def test_tab175_dichiarata(self):
        titoli = _titoli()
        assert len(titoli) == 290
        assert titoli[174] == "🎯 Matrice costo giorno×ora"

    def test_tab229_dichiarata(self):
        titoli = _titoli()
        assert len(titoli) == 290
        assert titoli[228] == "💡 Valore del forecast"

    def test_tab230_dichiarata(self):
        titoli = _titoli()
        assert len(titoli) == 290
        assert titoli[229] == "🧮 Budget di rischio"


# ------------------------------------------------------- tab133: regimi di prezzo
class TestRegimiPrezzo:
    def _serie_terzili(self):
        # 9 giorni: 3 a 50, 3 a 100, 3 a 150 EUR/MWh (piatti in giornata)
        vals = [50.0] * 72 + [100.0] * 72 + [150.0] * 72
        idx = pd.date_range("2026-01-05", periods=len(vals), freq="h")
        return pd.Series(vals, index=idx)

    def test_classificazione_terzili(self):
        r = calcola_regimi_prezzo(self._serie_terzili())
        assert r["ok"] is True
        g = r["giornaliera"]
        assert len(g) == 9
        assert list(g["Regime"]) == ["Basso"] * 3 + ["Medio"] * 3 + ["Alto"] * 3

    def test_matrice_transizione(self):
        r = calcola_regimi_prezzo(self._serie_terzili())
        m = r["matrice_conteggi"]
        assert m.loc["Basso", "Basso"] == 2
        assert m.loc["Basso", "Medio"] == 1
        assert m.loc["Medio", "Medio"] == 2
        assert m.loc["Medio", "Alto"] == 1
        assert m.loc["Alto", "Alto"] == 2
        assert m.loc["Alto", "Basso"] == 0
        # righe di probabilita' sommano a 1
        assert np.allclose(r["matrice_prob"].sum(axis=1).to_numpy(), 1.0)

    def test_regime_corrente_e_stazionaria(self):
        r = calcola_regimi_prezzo(self._serie_terzili())
        assert r["regime_corrente"] == "Alto"
        assert r["giorni_regime_corrente"] == 3
        # Alto->Alto 2 volte su 2 uscite da Alto
        assert r["prob_resta_corrente"] == 1.0
        staz = r["stazionaria"]
        assert abs(float(staz.sum()) - 1.0) < 1e-9
        assert bool((staz >= 0).all())
        # Alto e' assorbente in questa serie sintetica: la stazionaria
        # si concentra tutta su Alto
        assert list(staz.round(9)) == [0.0, 0.0, 1.0]

    def test_tabella_regimi(self):
        r = calcola_regimi_prezzo(self._serie_terzili())
        t = r["tabella_regimi"]
        assert list(t["Giorni"]) == [3, 3, 3]
        assert list(t["Regime"]) == ["Basso", "Medio", "Alto"]

    def test_pochi_giorni_non_ok(self):
        assert calcola_regimi_prezzo(_serie_piatta(100.0, 8))["ok"] is False

    def test_serie_vuota_non_ok(self):
        s = pd.Series([], dtype=float)
        assert calcola_regimi_prezzo(s)["ok"] is False

    def test_non_numerica_non_ok(self):
        assert calcola_regimi_prezzo(["a", "b", "c"])["ok"] is False


# ------------------------------------------------------- tab134: report di periodo
class TestRiepilogoPeriodo:
    def test_kpi_serie_piatta(self):
        # 48h piatte a 100 EUR/MWh (gio 2026-01-01 + ven 2026-01-02)
        r = calcola_riepilogo_periodo(_serie_piatta(100.0, 2, inizio="2026-01-01"))
        assert r["ok"] is True
        k = r["kpi"]
        assert k["ore"] == 48
        assert k["giorni"] == 2
        assert k["medio"] == 100.0
        assert k["mediano"] == 100.0
        assert k["std"] == 0.0
        assert k["min"] == 100.0 and k["max"] == 100.0
        assert k["p5"] == 100.0 and k["p95"] == 100.0
        assert k["quota_negativi"] == 0.0
        assert k["baseload_1MW"] == 4800.0

    def test_fasce_ore(self):
        r = calcola_riepilogo_periodo(_serie_piatta(100.0, 2, inizio="2026-01-01"))
        f = r["fasce"].set_index("Fascia")["Ore"].to_dict()
        # gio+ven: F1 11h/gg, F2 5h/gg, F3 8h/gg
        assert f == {"F1": 22, "F2": 10, "F3": 16}

    def test_settimanale_e_giorni(self):
        r = calcola_riepilogo_periodo(_serie_piatta(100.0, 2, inizio="2026-01-01"))
        assert len(r["giorni"]) == 2
        assert list(r["settimanale"]["Giorno settimana"]) == ["Gio", "Ven"]
        assert len(r["mensile"]) == 1

    def test_csv_report(self):
        r = calcola_riepilogo_periodo(_serie_piatta(100.0, 2, inizio="2026-01-01"))
        csv = genera_csv_report(r, "2026-01-01", "2026-01-02")
        assert csv.startswith("# Report di periodo")
        assert "# SEZIONE;KPI" in csv
        assert "# SEZIONE;MENSILE" in csv
        assert "# SEZIONE;FASCE" in csv
        assert "# SEZIONE;GIORNI" in csv
        assert "Prezzo medio (€/MWh);100.0" in csv
        assert csv.endswith("\n")

    def test_serie_vuota_non_ok(self):
        r = calcola_riepilogo_periodo(pd.Series([], dtype=float))
        assert r["ok"] is False and r["kpi"] == {}


# ------------------------------------------------------- tab175: matrice costo settimana
class TestMatriceCostoSettimana:
    def test_costo_totale_a_mano(self):
        # settimana intera da lun 2026-01-05, prezzo piatto 100
        # F1: 11h x 5gg = 55h | F2: 5h x 5gg + 16h sab = 41h | F3: 72h
        s = _serie_piatta(100.0, 7, inizio="2026-01-05")
        r = calcola_matrice_costo_settimana(s, 10.0, 5.0, 2.0)
        assert r["valido"] is True
        assert r["n_ore"] == 168
        assert abs(r["energia_totale"] - 899.0) < 1e-9  # 55*10+41*5+72*2
        assert abs(r["costo_totale"] - 89900.0) < 1e-6
        assert r["mat_costo"].shape == (7, 24)
        assert r["mat_prezzo"].shape == (7, 24)

    def test_giorno_peggiore_e_top(self):
        s = _serie_piatta(100.0, 7, inizio="2026-01-05")
        r = calcola_matrice_costo_settimana(s, 10.0, 5.0, 2.0)
        assert r["giorno_peggiore"] in ("Lun", "Mar", "Mer", "Gio", "Ven")
        # top-10 celle: tutte F1 feriali da 1000 EUR -> 10000/89900
        assert abs(r["quota_top_n"] - 10000.0 / 89900.0 * 100) < 1e-9
        assert len(r["df_top"]) == 10

    def test_carico_nullo_invalido(self):
        s = _serie_piatta(100.0, 7, inizio="2026-01-05")
        r = calcola_matrice_costo_settimana(s, 0.0, 0.0, 0.0)
        assert r["valido"] is False

    def test_serie_vuota_invalida(self):
        r = calcola_matrice_costo_settimana(pd.Series([], dtype=float), 10, 5, 2)
        assert r["valido"] is False


# ------------------------------------------------------- tab229: valore del forecast
class TestValoreForecast:
    def test_determinismo_stesso_seed(self):
        a = calcola_valore_forecast(100.0, n_sim=2000, seed=7)
        b = calcola_valore_forecast(100.0, n_sim=2000, seed=7)
        assert a["valido"] and b["valido"]
        assert a["valore_forecast_eur_mwh"] == b["valore_forecast_eur_mwh"]
        assert a["evpi_eur_mwh"] == b["evpi_eur_mwh"]

    def test_proprieta_strutturali(self):
        r = calcola_valore_forecast(100.0, n_sim=2000, seed=7)
        assert r["valore_forecast_eur_mwh"] >= 0.0
        assert r["evpi_eur_mwh"] >= r["valore_forecast_eur_mwh"]
        assert 0.0 <= r["pct_evpi_catturata"] <= 100.0
        assert abs(r["valore_forecast_eur_tot"]
                   - r["valore_forecast_eur_mwh"] * 100.0) < 1e-9

    def test_forecast_perfetto_cattura_100(self):
        r = calcola_valore_forecast(100.0, n_sim=2000, seed=7, sigma_forecast=0.0)
        assert r["valido"] is True
        assert abs(r["pct_evpi_catturata"] - 100.0) < 1e-9
        assert abs(r["valore_forecast_eur_mwh"] - r["evpi_eur_mwh"]) < 1e-9

    def test_input_invalidi(self):
        assert calcola_valore_forecast(0.0)["valido"] is False
        assert calcola_valore_forecast(-5.0)["valido"] is False
        assert calcola_valore_forecast(100.0, n_giorni=1)["valido"] is False


# ------------------------------------------------------- tab230: budget di rischio
class TestBudgetRischio:
    def test_happy_path_non_sollevava_nameerror(self):
        # regressione: prima del fix `import math` questa chiamata
        # sollevava NameError: name 'math' is not defined
        r = calcola_budget_rischio(["A", "B", "C"], [1e6, 2e6, 1.5e6],
                                   [25.0, 30.0, 20.0])
        assert r["valido"] is True
        assert r["errore"] is None
        assert r["var_portafoglio_eur"] > 0

    def test_eulero_somma_componenti(self):
        r = calcola_budget_rischio(["A", "B"], [1e6, 1e6], [20.0, 20.0],
                                   correlazione_media=0.0)
        assert r["valido"] is True
        # la colonna df e' arrotondata all'euro: tolleranza = n*0.5 EUR
        comp = r["df"]["Component VaR (eur)"].to_numpy()
        assert abs(comp.sum() - r["var_portafoglio_eur"]) <= 1.0 + 1e-6

    def test_correlazione_uno_nessuna_diversificazione(self):
        r = calcola_budget_rischio(["A", "B"], [1e6, 2e6], [20.0, 30.0],
                                   correlazione_media=1.0)
        assert r["valido"] is True
        assert abs(r["benefit_diversificazione_eur"]) < 1e-6 * r["var_standalone_somma_eur"]
        assert abs(r["var_portafoglio_eur"] - r["var_standalone_somma_eur"]) < 1e-6

    def test_correlazione_zero_diversificazione_positiva(self):
        r = calcola_budget_rischio(["A", "B"], [1e6, 1e6], [20.0, 20.0],
                                   correlazione_media=0.0)
        assert r["benefit_diversificazione_eur"] > 0
        assert r["var_portafoglio_eur"] < r["var_standalone_somma_eur"]

    def test_input_invalidi(self):
        assert calcola_budget_rischio(["A"], [1e6], [20.0])["valido"] is False
        assert calcola_budget_rischio(["A", "B"], [1e6, -2.0], [20.0, 20.0])["valido"] is False
        assert calcola_budget_rischio(["A", "B"], [1e6, 1e6], [20.0, 0.0])["valido"] is False
        assert calcola_budget_rischio(["A", "B"], [1e6, 1e6], [20.0, 20.0],
                                      correlazione_media=1.5)["valido"] is False
        assert calcola_budget_rischio(["A", "B"], [1e6, 1e6], [20.0, 20.0],
                                      confidenza=1.2)["valido"] is False
        assert calcola_budget_rischio(["A", "A"], [1e6, 1e6], [20.0, 20.0])["valido"] is False
        assert calcola_budget_rischio(["A", "B"], [1e6], [20.0, 20.0])["valido"] is False
