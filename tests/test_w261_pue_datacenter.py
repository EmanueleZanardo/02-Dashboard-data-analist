"""Test tab261 'PUE & costo data center': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab261.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("pue261_num", "pue261_potenza_totale_kw",
          "pue261_energia_annua_mwh", "pue261_overhead_pct",
          "pue261_costo_annuo_energia", "pue261_costo_totale_annuo",
          "pue261_risparmio_miglioramento", "pue261_emissioni_tco2",
          "pue261_giudizio", "pue261_sensibilita")
pue261_num = _F["pue261_num"]
pue261_potenza_totale_kw = _F["pue261_potenza_totale_kw"]
pue261_energia_annua_mwh = _F["pue261_energia_annua_mwh"]
pue261_overhead_pct = _F["pue261_overhead_pct"]
pue261_costo_annuo_energia = _F["pue261_costo_annuo_energia"]
pue261_costo_totale_annuo = _F["pue261_costo_totale_annuo"]
pue261_risparmio_miglioramento = _F["pue261_risparmio_miglioramento"]
pue261_emissioni_tco2 = _F["pue261_emissioni_tco2"]
pue261_giudizio = _F["pue261_giudizio"]
pue261_sensibilita = _F["pue261_sensibilita"]

APP = Path(__file__).parent.parent / "app.py"

TITLE261 = "🏢 PUE & costo data center"
TITLE262 = "🔌 Gruppo elettrogeno vs blackout"
TITLE263 = "🚗 Flotta aziendale: TCO diesel vs elettrico"
TITLE264 = "📜 Garanzie di origine: costo del 100% rinnovabile"
TITLE265 = "♻️ Fine vita FV: revamping vs dismissione"
TITLE266 = "🌾️ Agrivoltaico: doppio reddito"
TITLE267 = "🟢 Biometano: business case"
TITLE268 = "🌬️ Eolico onshore: business case"
TITLE269 = "🌊 Idroelettrico run-of-river: business case"
TITLE270 = "🔥 Geotermia profonda: business case"
TITLE271 = "☀️ Solare termodinamico (CSP): business case"
TITLE272 = "🌬️ Eolico offshore: business case"
TITLE273 = "☀️ Fotovoltaico utility-scale: business case"
TITLE274 = "⚛️ Nucleare SMR: business case"
TITLE275 = "📊 Posizione vs limiti di rischio"
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
TITLE260 = "❄️ Pompa di calore vs caldaia"


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab261:
    def test_tab261_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 301
        assert TITLE261 in titoli
        assert "tab261" in dvars
        assert "tab261" in withs
        assert titoli[dvars.index("tab261")] == TITLE261
        assert titoli[-1] == TITLE301
        keys = re.findall(r'key="(pue261_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 8

    def test_titoli_allineati_260_261(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab260")] == TITLE260
        assert titoli[dvars.index("tab261")] == TITLE261
        assert titoli[dvars.index("tab262")] == TITLE262
        assert titoli[dvars.index("tab263")] == TITLE263
        assert titoli[dvars.index("tab264")] == TITLE264
        assert titoli[dvars.index("tab265")] == TITLE265
        assert titoli[dvars.index("tab266")] == TITLE266
        assert titoli[dvars.index("tab267")] == TITLE267
        assert titoli[dvars.index("tab268")] == TITLE268
        assert titoli[dvars.index("tab269")] == TITLE269
        assert titoli[dvars.index("tab270")] == TITLE270
        assert titoli[dvars.index("tab271")] == TITLE271
        assert titoli[dvars.index("tab272")] == TITLE272
        assert titoli[dvars.index("tab273")] == TITLE273
        assert titoli[dvars.index("tab274")] == TITLE274
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


class TestPue261Num:
    def test_ok(self):
        assert pue261_num(3, "x") == 3.0
        assert pue261_num(2.5, "x") == 2.5

    def test_invalidi(self):
        for bad in (True, False, float("nan"), float("inf"), "3", None):
            with pytest.raises(ValueError):
                pue261_num(bad, "x")


class TestPue261Potenza:
    def test_base(self):
        assert pue261_potenza_totale_kw(500.0, 1.5) == pytest.approx(750.0)

    def test_pue_uno(self):
        assert pue261_potenza_totale_kw(100.0, 1.0) == pytest.approx(100.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            pue261_potenza_totale_kw(100.0, 0.9)
        with pytest.raises(ValueError):
            pue261_potenza_totale_kw(-10.0, 1.5)


class TestPue261Energia:
    def test_annua(self):
        # 750 kW * 8760 h / 1000 = 6570 MWh
        assert pue261_energia_annua_mwh(500.0, 1.5) == pytest.approx(6570.0)

    def test_ore_custom(self):
        assert pue261_energia_annua_mwh(500.0, 1.5, 4000.0) == pytest.approx(3000.0)

    def test_ore_zero_errore(self):
        with pytest.raises(ValueError):
            pue261_energia_annua_mwh(500.0, 1.5, 0.0)


class TestPue261Overhead:
    def test_base(self):
        assert pue261_overhead_pct(1.5) == pytest.approx(33.333333)

    def test_pue_uno_zero(self):
        assert pue261_overhead_pct(1.0) == pytest.approx(0.0)

    def test_pue_sotto_uno_errore(self):
        with pytest.raises(ValueError):
            pue261_overhead_pct(0.99)


class TestPue261Costi:
    def test_costo_energia(self):
        assert pue261_costo_annuo_energia(6570.0, 180.0) == pytest.approx(1182600.0)

    def test_costo_totale_con_potenza(self):
        # 6570*180 = 1.182.600 + 750 kW * 50 = 37.500
        assert pue261_costo_totale_annuo(500.0, 1.5, 180.0, 8760.0, 50.0) == pytest.approx(1220100.0)

    def test_costo_totale_senza_potenza(self):
        e = pue261_energia_annua_mwh(500.0, 1.5)
        assert pue261_costo_totale_annuo(500.0, 1.5, 180.0) == pytest.approx(
            pue261_costo_annuo_energia(e, 180.0))

    def test_costo_potenza_negativo_errore(self):
        with pytest.raises(ValueError):
            pue261_costo_totale_annuo(500.0, 1.5, 180.0, 8760.0, -1.0)


class TestPue261Risparmio:
    def test_base(self):
        r = pue261_risparmio_miglioramento(500.0, 1.5, 1.3, 180.0)
        assert r["risparmio_mwh"] == pytest.approx(876.0)
        assert r["risparmio_eur"] == pytest.approx(157680.0)
        assert r["risparmio_pct"] == pytest.approx(876.0 / 6570.0 * 100.0)

    def test_target_uguale_zero(self):
        r = pue261_risparmio_miglioramento(500.0, 1.5, 1.5, 180.0)
        assert r["risparmio_mwh"] == pytest.approx(0.0)
        assert r["risparmio_eur"] == pytest.approx(0.0)

    def test_target_peggiore_errore(self):
        with pytest.raises(ValueError):
            pue261_risparmio_miglioramento(500.0, 1.3, 1.5, 180.0)


class TestPue261EmissioniGiudizio:
    def test_emissioni(self):
        assert pue261_emissioni_tco2(6570.0, 0.35) == pytest.approx(2299.5)

    def test_giudizio_soglie(self):
        assert pue261_giudizio(1.2) == "ottimo"
        assert pue261_giudizio(1.3) == "buono"
        assert pue261_giudizio(1.59) == "buono"
        assert pue261_giudizio(1.6) == "medio"
        assert pue261_giudizio(1.99) == "medio"
        assert pue261_giudizio(2.0) == "critico"
        assert pue261_giudizio(2.5) == "critico"

    def test_giudizio_pue_sotto_uno_errore(self):
        with pytest.raises(ValueError):
            pue261_giudizio(0.9)


class TestPue261Sensibilita:
    def test_lunghezza_e_monotonia(self):
        righe = pue261_sensibilita(500.0, 1.0, 2.0, 0.25, 180.0)
        assert len(righe) == 5
        assert righe[0]["pue"] == pytest.approx(1.0)
        assert righe[-1]["pue"] == pytest.approx(2.0)
        costi = [r["costo_eur"] for r in righe]
        assert all(b > a for a, b in zip(costi, costi[1:]))

    def test_chiavi_e_valore(self):
        r = pue261_sensibilita(500.0, 1.5, 1.5, 0.5, 180.0)[0]
        assert set(r) == {"pue", "energia_mwh", "costo_eur"}
        assert r["energia_mwh"] == pytest.approx(6570.0)
        assert r["costo_eur"] == pytest.approx(6570.0 * 180.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            pue261_sensibilita(500.0, 0.9, 2.0, 0.25, 180.0)
        with pytest.raises(ValueError):
            pue261_sensibilita(500.0, 2.0, 1.0, 0.25, 180.0)
        with pytest.raises(ValueError):
            pue261_sensibilita(500.0, 1.0, 2.0, 0.0, 180.0)
