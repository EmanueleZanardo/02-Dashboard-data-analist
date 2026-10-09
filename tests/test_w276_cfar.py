"""Test tab276 'Cash flow at risk (CFaR)': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab276.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("cf276_num", "cf276_int", "cf276_parse_flussi", "cf276_simula",
          "cf276_totali_annui", "cf276_percentile", "cf276_cfar",
          "cf276_prob_negativo", "cf276_sintesi", "cf276_gap_budget")
cf276_num = _F["cf276_num"]
cf276_int = _F["cf276_int"]
cf276_parse_flussi = _F["cf276_parse_flussi"]
cf276_simula = _F["cf276_simula"]
cf276_totali_annui = _F["cf276_totali_annui"]
cf276_percentile = _F["cf276_percentile"]
cf276_cfar = _F["cf276_cfar"]
cf276_prob_negativo = _F["cf276_prob_negativo"]
cf276_sintesi = _F["cf276_sintesi"]
cf276_gap_budget = _F["cf276_gap_budget"]

APP = Path(__file__).parent.parent / "app.py"

TITLE276 = "💧 Cash flow at risk (CFaR)"
TITLE277 = "⚡ Aste MI: scostamenti vs MGP"
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
TITLE302 = "✂️📉 Incremental VaR: quanto rischio togli chiudendo la posizione?"
TITLE303 = "🧱📉 Capacità VaR: quanto nozionale puoi ancora aggiungere?"
TITLE304 = "🗂️📊 VaR per segmento: dove si concentra il rischio?"
TITLE305 = "🎯🛡 Risk budgeting: il book rispetta i target?"
TITLE306 = "💎📊 RAROC: il rendimento ripaga il rischio?"
TITLE307 = "🌊📉 Expected Shortfall: la perdita oltre il VaR"
TITLE308 = "💥📈 Stress di correlazione: quanto sale il VaR se si rompono?"
TITLE309 = "🎯💥 Rho critica: a quale correlazione il VaR tocca il limite?"
TITLE310 = "💧📉 LVaR: il VaR corretto per il costo di liquidazione"
TITLE311 = "📐📉 Cornish-Fisher: il VaR corretto per skew e code grasse"
TITLE312 = "📐🌊 Expected Shortfall con Cornish-Fisher: la coda oltre il VaR con code grasse"
TITLE313 = "📉💥 VaR rotto: la probabilita' di breccia con code grasse"
TITLE314 = "⏳📉 VaR multi-orizzonte: lo scaling con autocorrelazione dei rendimenti"
TITLE315 = "🏔️📉 Valori estremi (Hill): il VaR oltre il massimo storico"
TITLE316 = "🌊📉 POT-GPD: il VaR dalla coda paretiana oltre soglia"
TITLE317 = "🧠📉 CAViaR: il VaR adattivo che impara dai rendimenti"
TITLE318 = "🌀📉 Copula t-Student: il VaR che vede le code muoversi insieme"
TITLE319 = "🎛📉 FHS: il VaR con la volatilita' di oggi"
TITLE320 = "⚙️📉 GARCH(1,1): la volatilita' che ricorda"
TITLE321 = "🧪📉 Backtest VaR: il modello resiste al tempo?"
TITLE322 = "🎯📉 Convergenza forward: il forward indovina lo spot?"
TITLE323 = "🔄📉 Half-life di mean reversion: lo spot torna alla media?"
TITLE324 = "Ω📊 Omega ratio: oltre Sharpe e Sortino"
TITLE325 = "📈📉 Calmar ratio: il rendimento che paga il drawdown"
TITLE326 = "🩹 Pain index e Pain ratio: il dolore medio oltre il peggio"
TITLE327 = "🛟 Sterling ratio: il Calmar mediato sui peggiori drawdown"
TITLE328 = "🔻 Burke ratio: il drawdown penalizzato al quadrato"
TITLE329 = "🌊📉 CDaR: il drawdown medio oltre la soglia (il VaR dei drawdown)"
TITLE330 = "🔍📉 Martin ratio: il Calmar che guarda tutto il dolore"
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
TITLE275 = "📊 Posizione vs limiti di rischio"

CSV_FLUSSI = ("mese,flusso_eur\n"
              "Gen,185000\nFeb,170000\nMar,140000\n")


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab276:
    def test_tab276_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 340
        assert TITLE276 in titoli
        assert "tab276" in dvars
        assert "tab276" in withs
        assert titoli[dvars.index("tab276")] == TITLE276
        assert titoli[-1] == TITLE340
        keys = re.findall(r'key="(cf276_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_275_276(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab275")] == TITLE275
        assert titoli[dvars.index("tab276")] == TITLE276
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
        for fn in ("cf276_num", "cf276_int", "cf276_parse_flussi",
                   "cf276_simula", "cf276_totali_annui", "cf276_percentile",
                   "cf276_cfar", "cf276_prob_negativo", "cf276_sintesi",
                   "cf276_gap_budget"):
            assert src.index(f"def {fn}(") < i_ws
            assert src.index("    with tab276:") > i_ws


class TestCf276NumInt:
    def test_num_ok(self):
        assert cf276_num(3, "x") == 3.0
        assert cf276_num(-2.5, "x") == -2.5

    def test_num_invalidi(self):
        import math
        for bad in (True, math.nan, math.inf, "3", None):
            with pytest.raises(ValueError):
                cf276_num(bad, "x")

    def test_int_ok(self):
        assert cf276_int(500, "n") == 500
        assert cf276_int(500.0, "n") == 500
        assert cf276_int(0, "seed", minimo=0) == 0

    def test_int_invalidi(self):
        for bad in (True, 2.5, 0, -3, "500"):
            with pytest.raises(ValueError):
                cf276_int(bad, "n")


class TestCf276ParseFlussi:
    def test_base(self):
        righe = cf276_parse_flussi(CSV_FLUSSI)
        assert len(righe) == 3
        assert righe[0] == {"etichetta": "Gen", "flusso_eur": 185000.0}
        assert righe[2]["flusso_eur"] == 140000.0

    def test_senza_header_e_negativi(self):
        righe = cf276_parse_flussi("A,100.0\nB,-50")
        assert len(righe) == 2
        assert righe[1]["flusso_eur"] == -50.0

    def test_invalidi(self):
        for bad in ("", "etichetta\n", "A,xx", "A,10,extra", ",100",
                    "A,10\nA,20"):
            with pytest.raises(ValueError):
                cf276_parse_flussi(bad)

    def test_troppe_righe(self):
        txt = "\n".join(f"M{i},{1000}" for i in range(61))
        with pytest.raises(ValueError):
            cf276_parse_flussi(txt)


class TestCf276Simula:
    def test_forma_e_riproducibilita(self):
        s1 = cf276_simula([100.0, 200.0], 10.0, 500, 7)
        s2 = cf276_simula([100.0, 200.0], 10.0, 500, 7)
        assert len(s1) == 500 and len(s1[0]) == 2
        assert s1 == s2
        s3 = cf276_simula([100.0, 200.0], 10.0, 500, 8)
        assert s1 != s3

    def test_vol_zero_deterministica(self):
        sims = cf276_simula([100.0, 200.0], 0.0, 500, 1)
        assert all(r == [100.0, 200.0] for r in sims)

    def test_media_centrata(self):
        tot = cf276_totali_annui(cf276_simula([100000.0] * 12, 10.0, 3000, 42))
        assert abs(sum(tot) / len(tot) - 1_200_000) < 60_000

    def test_invalidi(self):
        with pytest.raises(ValueError):
            cf276_simula([], 10.0, 500, 1)
        with pytest.raises(ValueError):
            cf276_simula([100.0], -1.0, 500, 1)
        with pytest.raises(ValueError):
            cf276_simula([100.0], 10.0, 50, 1)
        with pytest.raises(ValueError):
            cf276_simula([100.0], 10.0, 500, -1)


class TestCf276PercentileCfar:
    def test_percentile(self):
        assert cf276_percentile([1, 2, 3, 4], 50) == pytest.approx(2.5)
        assert cf276_percentile([10.0], 95) == pytest.approx(10.0)
        assert cf276_percentile([1, 2, 3, 4], 25) == pytest.approx(1.75)

    def test_percentile_invalidi(self):
        with pytest.raises(ValueError):
            cf276_percentile([], 50)
        with pytest.raises(ValueError):
            cf276_percentile([1, 2], 0)
        with pytest.raises(ValueError):
            cf276_percentile([1, 2], 100)

    def test_cfar(self):
        tot = cf276_totali_annui(cf276_simula([100000.0] * 12, 10.0, 2000, 3))
        c = cf276_cfar(tot, 95.0)
        assert c["cfar_eur"] == pytest.approx(
            c["atteso_eur"] - c["percentile_basso_eur"])
        assert c["cfar_eur"] > 0
        assert c["percentile_basso_eur"] < c["atteso_eur"]

    def test_cfar_invalidi(self):
        with pytest.raises(ValueError):
            cf276_cfar([], 95.0)
        with pytest.raises(ValueError):
            cf276_cfar([1.0, 2.0], 50.0)
        with pytest.raises(ValueError):
            cf276_cfar([1.0, 2.0], 100.0)


class TestCf276ProbSintesiGap:
    def test_prob_negativo(self):
        assert cf276_prob_negativo([1.0, -2.0, 3.0, -4.0]) == pytest.approx(0.5)
        assert cf276_prob_negativo([1.0, 2.0]) == pytest.approx(0.0)
        with pytest.raises(ValueError):
            cf276_prob_negativo([])

    def test_sintesi(self):
        tot = cf276_totali_annui(cf276_simula([100000.0] * 12, 10.0, 2000, 11))
        s = cf276_sintesi(tot)
        assert s["n"] == 2000
        assert s["min_eur"] <= s["p5_eur"] <= s["mediana_eur"]
        assert s["mediana_eur"] <= s["p95_eur"] <= s["max_eur"]
        assert 0.0 <= s["prob_negativa"] <= 1.0
        assert s["media_eur"] == pytest.approx(sum(tot) / len(tot))

    def test_gap_budget(self):
        g = cf276_gap_budget(1_420_000, 1_400_000)
        assert g["diff_eur"] == pytest.approx(20_000)
        assert g["diff_pct"] == pytest.approx(20_000 / 1_400_000 * 100)
        assert g["verdetto"] == "in_linea"
        assert cf276_gap_budget(1_300_000, 1_400_000)["verdetto"] == "sotto_budget"
        assert cf276_gap_budget(1_500_000, 1_400_000)["verdetto"] == "sopra_budget"
        g0 = cf276_gap_budget(100, 0)
        assert g0["diff_pct"] is None
        assert g0["verdetto"] == "sopra_budget"
        with pytest.raises(ValueError):
            cf276_gap_budget(100, 200, tolleranza_pct=-1)
