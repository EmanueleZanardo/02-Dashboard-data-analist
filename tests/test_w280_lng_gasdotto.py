"""Test tab280 'LNG vs gasdotto: costo delivered': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab280.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("lg280_num", "lg280_perc", "lg280_costo_lng", "lg280_costo_gasdotto",
          "lg280_confronto", "lg280_breakeven_fob", "lg280_sensibilita_fob",
          "lg280_verdetto", "lg280_costo_annuo_mln")
lg280_num = _F["lg280_num"]
lg280_perc = _F["lg280_perc"]
lg280_costo_lng = _F["lg280_costo_lng"]
lg280_costo_gasdotto = _F["lg280_costo_gasdotto"]
lg280_confronto = _F["lg280_confronto"]
lg280_breakeven_fob = _F["lg280_breakeven_fob"]
lg280_sensibilita_fob = _F["lg280_sensibilita_fob"]
lg280_verdetto = _F["lg280_verdetto"]
lg280_costo_annuo_mln = _F["lg280_costo_annuo_mln"]

APP = Path(__file__).parent.parent / "app.py"

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
TITLE279 = "🌪️ Derivati meteo: pricing HDD/CDD"
TITLE278 = "🌡️ Stress climatico: domanda e prezzo"

FOB, NOLO, RIGASS, PERD_LNG = 40.0, 8.0, 3.0, 2.0
FRONT, TRASP, PERD_GAS = 45.0, 2.0, 1.0
DES_ATTESO = (FOB + NOLO) / 0.98 + RIGASS
DGAS_ATTESO = FRONT / 0.99 + TRASP


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab280:
    def test_tab280_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 308
        assert TITLE280 in titoli
        assert "tab280" in dvars
        assert "tab280" in withs
        assert titoli[dvars.index("tab280")] == TITLE280
        assert titoli[-1] == TITLE308
        keys = re.findall(r'key="(lg280_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_278_279_280(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab278")] == TITLE278
        assert titoli[dvars.index("tab279")] == TITLE279
        assert titoli[dvars.index("tab280")] == TITLE280
        assert titoli[dvars.index("tab281")] == TITLE281
        assert titoli[dvars.index("tab282")] == TITLE282
        assert titoli[dvars.index("tab283")] == TITLE283
        assert titoli[dvars.index("tab284")] == TITLE284
        assert titoli[dvars.index("tab285")] == TITLE285


class TestLg280Validatori:
    def test_num_ok(self):
        assert lg280_num(3, "x") == 3.0
        assert lg280_num(2.5, "x") == 2.5

    def test_num_ko(self):
        with pytest.raises(ValueError):
            lg280_num(True, "x")
        with pytest.raises(ValueError):
            lg280_num("3", "x")
        with pytest.raises(ValueError):
            lg280_num(float("nan"), "x")
        with pytest.raises(ValueError):
            lg280_num(float("inf"), "x")

    def test_perc_ok(self):
        assert lg280_perc(0, "x") == 0.0
        assert lg280_perc(100, "x") == 100.0
        assert lg280_perc(2.5, "x") == 2.5

    def test_perc_ko(self):
        with pytest.raises(ValueError):
            lg280_perc(-0.1, "x")
        with pytest.raises(ValueError):
            lg280_perc(100.1, "x")


class TestLg280CostoLng:
    def test_base(self):
        assert lg280_costo_lng(FOB, NOLO, RIGASS, PERD_LNG) == pytest.approx(DES_ATTESO)

    def test_zero_perdite(self):
        assert lg280_costo_lng(40.0, 8.0, 3.0, 0.0) == pytest.approx(51.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            lg280_costo_lng(-1.0, NOLO, RIGASS, PERD_LNG)
        with pytest.raises(ValueError):
            lg280_costo_lng(FOB, NOLO, RIGASS, 100.0)
        with pytest.raises(ValueError):
            lg280_costo_lng(FOB, NOLO, RIGASS, 101.0)


class TestLg280CostoGasdotto:
    def test_base(self):
        assert lg280_costo_gasdotto(FRONT, TRASP, PERD_GAS) == pytest.approx(DGAS_ATTESO)

    def test_zero_perdite(self):
        assert lg280_costo_gasdotto(45.0, 2.0, 0.0) == pytest.approx(47.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            lg280_costo_gasdotto(-1.0, TRASP, PERD_GAS)
        with pytest.raises(ValueError):
            lg280_costo_gasdotto(FRONT, TRASP, 100.0)


class TestLg280Confronto:
    def test_base_gasdotto_vince(self):
        r = lg280_confronto(FOB, NOLO, RIGASS, PERD_LNG, FRONT, TRASP, PERD_GAS)
        assert r["des_lng"] == pytest.approx(DES_ATTESO)
        assert r["delivered_gasdotto"] == pytest.approx(DGAS_ATTESO)
        assert r["delta"] == pytest.approx(DES_ATTESO - DGAS_ATTESO)
        assert r["fonte"] == "gasdotto"

    def test_lng_vince(self):
        r = lg280_confronto(30.0, 8.0, 3.0, 2.0, FRONT, TRASP, PERD_GAS)
        assert r["fonte"] == "LNG"
        assert r["delta"] < 0

    def test_pari(self):
        dgas = lg280_costo_gasdotto(FRONT, TRASP, PERD_GAS)
        be = lg280_breakeven_fob(dgas, NOLO, RIGASS, PERD_LNG)
        r = lg280_confronto(be, NOLO, RIGASS, PERD_LNG, FRONT, TRASP, PERD_GAS)
        assert r["fonte"] == "pari"
        assert abs(r["delta"]) <= 0.005


class TestLg280Breakeven:
    def test_base(self):
        be = lg280_breakeven_fob(DGAS_ATTESO, NOLO, RIGASS, PERD_LNG)
        assert be == pytest.approx((DGAS_ATTESO - RIGASS) * 0.98 - NOLO)

    def test_coerente_con_confronto(self):
        be = lg280_breakeven_fob(DGAS_ATTESO, NOLO, RIGASS, PERD_LNG)
        assert lg280_costo_lng(be, NOLO, RIGASS, PERD_LNG) == pytest.approx(DGAS_ATTESO)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            lg280_breakeven_fob(0.0, NOLO, RIGASS, PERD_LNG)
        with pytest.raises(ValueError):
            lg280_breakeven_fob(DGAS_ATTESO, NOLO, RIGASS, 100.0)


class TestLg280Sensibilita:
    def test_struttura(self):
        righe = lg280_sensibilita_fob(FOB, NOLO, RIGASS, PERD_LNG, 5)
        assert len(righe) == 5
        assert righe[0]["fob"] == pytest.approx(20.0)
        assert righe[-1]["fob"] == pytest.approx(60.0)
        assert set(righe[0]) == {"fob", "des"}

    def test_monotonia_e_centro(self):
        righe = lg280_sensibilita_fob(FOB, NOLO, RIGASS, PERD_LNG, 5)
        dess = [r["des"] for r in righe]
        assert all(b > a for a, b in zip(dess, dess[1:]))
        assert righe[2]["des"] == pytest.approx(DES_ATTESO)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            lg280_sensibilita_fob(0.0, NOLO, RIGASS, PERD_LNG)
        with pytest.raises(ValueError):
            lg280_sensibilita_fob(FOB, NOLO, RIGASS, PERD_LNG, 2)


class TestLg280Verdetto:
    def test_lng(self):
        r = lg280_verdetto(-2.0, 1.0)
        assert r["verdetto"] == "lng"

    def test_in_linea(self):
        assert lg280_verdetto(0.5, 1.0)["verdetto"] == "in_linea"
        assert lg280_verdetto(-1.0, 1.0)["verdetto"] == "in_linea"

    def test_gasdotto(self):
        r = lg280_verdetto(4.53, 1.0)
        assert r["verdetto"] == "gasdotto"
        assert r["delta"] == pytest.approx(4.53)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            lg280_verdetto(1.0, -0.5)


class TestLg280CostoAnnuo:
    def test_base(self):
        assert lg280_costo_annuo_mln(50.0, 100.0) == pytest.approx(5.0)

    def test_zero(self):
        assert lg280_costo_annuo_mln(50.0, 0.0) == pytest.approx(0.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            lg280_costo_annuo_mln(-1.0, 100.0)
        with pytest.raises(ValueError):
            lg280_costo_annuo_mln(50.0, -1.0)
