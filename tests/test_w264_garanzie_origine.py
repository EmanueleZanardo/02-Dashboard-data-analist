"""Test tab264 'Garanzie di origine: costo del 100% rinnovabile': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab264.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("go264_num", "go264_parse_consumi", "go264_costo_go",
          "go264_costo_annuo", "go264_copertura_fv", "go264_confronto",
          "go264_sensibilita_prezzo")
go264_num = _F["go264_num"]
go264_parse_consumi = _F["go264_parse_consumi"]
go264_costo_go = _F["go264_costo_go"]
go264_costo_annuo = _F["go264_costo_annuo"]
go264_copertura_fv = _F["go264_copertura_fv"]
go264_confronto = _F["go264_confronto"]
go264_sensibilita_prezzo = _F["go264_sensibilita_prezzo"]

APP = Path(__file__).parent.parent / "app.py"

TITLE264 = "\U0001F4DC Garanzie di origine: costo del 100% rinnovabile"
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
TITLE263 = "\U0001F697 Flotta aziendale: TCO diesel vs elettrico"

CONSUMI_TXT = "85\n78\n82\n75\n70\n65\n60\n62\n68\n75\n82\n90"
# somma = 892 MWh; FV 120 MWh -> netto 772 MWh; copertura 13,4529%


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab264:
    def test_tab264_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 300
        assert TITLE264 in titoli
        assert "tab264" in dvars
        assert "tab264" in withs
        assert titoli[dvars.index("tab264")] == TITLE264
        assert titoli[-1] == TITLE300
        keys = re.findall(r'key="(go264_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_263_264(self):
        _, titoli, dvars, _ = _registry()
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


class TestGo264Num:
    def test_ok(self):
        assert go264_num(3, "x") == 3.0
        assert go264_num(2.5, "x") == 2.5

    def test_invalidi(self):
        for bad in (True, False, float("nan"), float("inf"), "3", None):
            with pytest.raises(ValueError):
                go264_num(bad, "x")


class TestGo264ParseConsumi:
    def test_base(self):
        c = go264_parse_consumi(CONSUMI_TXT)
        assert len(c) == 12
        assert sum(c) == pytest.approx(892.0)
        assert c[0] == pytest.approx(85.0)
        assert c[-1] == pytest.approx(90.0)

    def test_separatore_puntoevirgola_e_virgola_decimale(self):
        c = go264_parse_consumi("85,5; 78; 82; 75; 70; 65; 60; 62; 68; 75; 82; 90")
        assert c[0] == pytest.approx(85.5)

    def test_conteggio_errato(self):
        with pytest.raises(ValueError):
            go264_parse_consumi("85\n78\n82")
        with pytest.raises(ValueError):
            go264_parse_consumi("")

    def test_non_numerico_e_negativo(self):
        with pytest.raises(ValueError):
            go264_parse_consumi("85\n78\nXX\n75\n70\n65\n60\n62\n68\n75\n82\n90")
        with pytest.raises(ValueError):
            go264_parse_consumi("85\n-78\n82\n75\n70\n65\n60\n62\n68\n75\n82\n90")


class TestGo264Costo:
    def test_base(self):
        # 772 MWh * 1,20 €/MWh = 926,40 €
        assert go264_costo_go(772.0, 1.20) == pytest.approx(926.4)

    def test_annuo(self):
        c = go264_parse_consumi(CONSUMI_TXT)
        r = go264_costo_annuo(c, 1.20)
        assert r["costo_totale"] == pytest.approx(892.0 * 1.20)
        assert len(r["costi_mensili"]) == 12
        assert r["costi_mensili"][0] == pytest.approx(85.0 * 1.20)
        assert sum(r["costi_mensili"]) == pytest.approx(r["costo_totale"])

    def test_invalidi(self):
        with pytest.raises(ValueError):
            go264_costo_go(-1.0, 1.20)
        with pytest.raises(ValueError):
            go264_costo_go(772.0, -0.5)
        with pytest.raises(ValueError):
            go264_costo_annuo([1.0] * 11, 1.20)


class TestGo264CoperturaFv:
    def test_base(self):
        r = go264_copertura_fv(892.0, 120.0)
        assert r["copertura_pct"] == pytest.approx(120.0 / 892.0 * 100.0)
        assert r["consumo_netto_mwh"] == pytest.approx(772.0)

    def test_fv_copre_tutto(self):
        r = go264_copertura_fv(892.0, 1000.0)
        assert r["copertura_pct"] == pytest.approx(100.0)
        assert r["consumo_netto_mwh"] == pytest.approx(0.0)

    def test_consumo_nullo(self):
        r = go264_copertura_fv(0.0, 50.0)
        assert r["copertura_pct"] == pytest.approx(100.0)
        assert r["consumo_netto_mwh"] == pytest.approx(0.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            go264_copertura_fv(-1.0, 120.0)
        with pytest.raises(ValueError):
            go264_copertura_fv(892.0, -5.0)


class TestGo264Confronto:
    def test_conviene_go(self):
        # 772 MWh: GO 926,40 € vs verde 2316 € -> delta 1389,60 (60%)
        r = go264_confronto(772.0, 1.20, 3.00, 0.0)
        assert r["costo_go"] == pytest.approx(926.4)
        assert r["costo_verde"] == pytest.approx(2316.0)
        assert r["delta"] == pytest.approx(1389.6)
        assert r["risparmio_pct"] == pytest.approx(60.0)
        assert r["verdetto"] == "GO"

    def test_conviene_fornitore_verde(self):
        # GO a 5 €/MWh: 3860 € vs verde 2316 €
        r = go264_confronto(772.0, 5.00, 3.00, 0.0)
        assert r["verdetto"] == "fornitore verde"
        assert r["delta"] == pytest.approx(2316.0 - 3860.0)

    def test_con_fisso_verde(self):
        r = go264_confronto(772.0, 1.20, 3.00, 500.0)
        assert r["costo_verde"] == pytest.approx(2816.0)
        assert r["verdetto"] == "GO"

    def test_indifferente(self):
        # premio = prezzo GO -> costi uguali
        r = go264_confronto(772.0, 1.20, 1.20, 0.0)
        assert r["verdetto"] == "indifferente"
        assert r["delta"] == pytest.approx(0.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            go264_confronto(-1.0, 1.20, 3.00, 0.0)
        with pytest.raises(ValueError):
            go264_confronto(772.0, 1.20, -3.00, 0.0)
        with pytest.raises(ValueError):
            go264_confronto(772.0, 1.20, 3.00, -10.0)


class TestGo264Sensibilita:
    def test_lunghezza_e_chiavi(self):
        righe = go264_sensibilita_prezzo(772.0, 3.0, 1.0)
        assert len(righe) == 4
        assert righe[0]["prezzo_go"] == pytest.approx(0.0)
        assert righe[-1]["prezzo_go"] == pytest.approx(3.0)
        assert set(righe[0]) == {"prezzo_go", "costo_annuo"}

    def test_monotonia_e_coerenza(self):
        righe = go264_sensibilita_prezzo(772.0, 3.0, 1.0)
        costi = [r["costo_annuo"] for r in righe]
        assert all(b > a for a, b in zip(costi, costi[1:]))
        assert righe[2]["costo_annuo"] == pytest.approx(go264_costo_go(772.0, 2.0))

    def test_invalidi(self):
        with pytest.raises(ValueError):
            go264_sensibilita_prezzo(772.0, 0.0, 1.0)
        with pytest.raises(ValueError):
            go264_sensibilita_prezzo(772.0, 3.0, 0.0)
