"""Test tab275 'Posizione vs limiti di rischio': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab275.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("pl275_num", "pl275_segno", "pl275_parse_posizioni",
          "pl275_parse_limiti", "pl275_utilizzo_pct", "pl275_stato",
          "pl275_nozionale", "pl275_aggrega", "pl275_check_limiti",
          "pl275_riepilogo")
pl275_num = _F["pl275_num"]
pl275_segno = _F["pl275_segno"]
pl275_parse_posizioni = _F["pl275_parse_posizioni"]
pl275_parse_limiti = _F["pl275_parse_limiti"]
pl275_utilizzo_pct = _F["pl275_utilizzo_pct"]
pl275_stato = _F["pl275_stato"]
pl275_nozionale = _F["pl275_nozionale"]
pl275_aggrega = _F["pl275_aggrega"]
pl275_check_limiti = _F["pl275_check_limiti"]
pl275_riepilogo = _F["pl275_riepilogo"]

APP = Path(__file__).parent.parent / "app.py"

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
TITLE302 = "✂️📉 Incremental VaR: quanto rischio togli chiudendo la posizione?"
TITLE303 = "🧱📉 Capacità VaR: quanto nozionale puoi ancora aggiungere?"
TITLE274 = "⚛️ Nucleare SMR: business case"

CSV_POS = ("prodotto,qta_mwh,direzione,prezzo_eur_mwh\n"
           "Power CAL-27 Baseload,5000,long,98.5\n"
           "Power Q2-27 Peak,2500,short,112.0\n"
           "Gas TTF CAL-27,8000,long,38.2\n")
CSV_LIM = ("prodotto,limite_mwh\n"
           "Power CAL-27 Baseload,10000\n"
           "Power Q2-27 Peak,2000\n"
           "Gas TTF CAL-27,10000\n")


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab275:
    def test_tab275_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 303
        assert TITLE275 in titoli
        assert "tab275" in dvars
        assert "tab275" in withs
        assert titoli[dvars.index("tab275")] == TITLE275
        assert titoli[-1] == TITLE303
        keys = re.findall(r'key="(pl275_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_274_275(self):
        _, titoli, dvars, _ = _registry()
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

    def test_helper_definiti_prima_della_ui(self):
        src = APP.read_text(encoding="utf-8")
        i_ws = src.index("if workspace ==")
        for fn in ("pl275_num", "pl275_segno", "pl275_parse_posizioni",
                   "pl275_parse_limiti", "pl275_utilizzo_pct", "pl275_stato",
                   "pl275_nozionale", "pl275_aggrega", "pl275_check_limiti",
                   "pl275_riepilogo"):
            assert src.index(f"def {fn}(") < i_ws
            assert src.index("    with tab275:") > i_ws


class TestPl275Num:
    def test_ok(self):
        assert pl275_num(3, "x") == 3.0
        assert pl275_num(2.5, "x") == 2.5
        assert pl275_num(-3, "x") == -3.0

    def test_invalidi(self):
        import math
        for bad in (True, False, math.nan, math.inf, -math.inf, "3", None, [1]):
            with pytest.raises(ValueError):
                pl275_num(bad, "x")


class TestPl275Segno:
    def test_long(self):
        for s in ("long", "Long", " L ", "acquisto", "+"):
            assert pl275_segno(s) == 1.0

    def test_short(self):
        for s in ("short", "SHORT", "s", "vendita", "-"):
            assert pl275_segno(s) == -1.0

    def test_invalidi(self):
        for bad in ("flat", "", None, 3):
            with pytest.raises(ValueError):
                pl275_segno(bad)


class TestPl275ParsePosizioni:
    def test_base(self):
        righe = pl275_parse_posizioni(CSV_POS)
        assert len(righe) == 3
        assert righe[0]["prodotto"] == "Power CAL-27 Baseload"
        assert righe[0]["qta_firmata_mwh"] == 5000.0
        assert righe[1]["direzione"] == "short"
        assert righe[1]["qta_firmata_mwh"] == -2500.0
        assert righe[2]["prezzo_eur_mwh"] == 38.2

    def test_senza_header(self):
        righe = pl275_parse_posizioni("A,100,long,50.0\nB,200,S,60")
        assert len(righe) == 2

    def test_righe_vuote_ignorate(self):
        righe = pl275_parse_posizioni("\nA,100,long,50.0\n\n")
        assert len(righe) == 1

    def test_invalidi(self):
        for bad in ("", "   ", "prodotto,qta\n",
                    "A,0,long,50", "A,-5,long,50",
                    "A,100,flat,50", "A,100,long,-1",
                    "A,100,long", ",100,long,50", "A,xx,long,50"):
            with pytest.raises(ValueError):
                pl275_parse_posizioni(bad)


class TestPl275ParseLimiti:
    def test_base(self):
        lim = pl275_parse_limiti(CSV_LIM)
        assert lim == {"Power CAL-27 Baseload": 10000.0,
                       "Power Q2-27 Peak": 2000.0,
                       "Gas TTF CAL-27": 10000.0}

    def test_senza_header(self):
        assert pl275_parse_limiti("A,500") == {"A": 500.0}

    def test_invalidi(self):
        for bad in ("", "prodotto\n", "A,0", "A,-10", "A,xx", "A,10,extra"):
            with pytest.raises(ValueError):
                pl275_parse_limiti(bad)


class TestPl275UtilizzoStato:
    def test_utilizzo(self):
        assert pl275_utilizzo_pct(5000, 10000) == 50.0
        assert pl275_utilizzo_pct(-5000, 10000) == 50.0
        assert pl275_utilizzo_pct(12000, 10000) == 120.0

    def test_utilizzo_limite_non_valido(self):
        assert pl275_utilizzo_pct(5000, 0) is None
        assert pl275_utilizzo_pct(5000, -3) is None

    def test_stato_soglie_default(self):
        assert pl275_stato(0) == "ok"
        assert pl275_stato(69.9) == "ok"
        assert pl275_stato(70.0) == "attenzione"
        assert pl275_stato(89.9) == "attenzione"
        assert pl275_stato(90.0) == "critico"
        assert pl275_stato(100.0) == "critico"
        assert pl275_stato(100.01) == "breach"
        assert pl275_stato(None) == "senza_limite"

    def test_stato_soglie_custom(self):
        assert pl275_stato(60, soglia_att=50.0, soglia_crit=80.0) == "attenzione"
        assert pl275_stato(85, soglia_att=50.0, soglia_crit=80.0) == "critico"

    def test_stato_invalidi(self):
        with pytest.raises(ValueError):
            pl275_stato(-1.0)
        with pytest.raises(ValueError):
            pl275_stato(50, soglia_att=90.0, soglia_crit=80.0)


class TestPl275NozionaleAggrega:
    def test_nozionale(self):
        assert pl275_nozionale(100, 50.0) == 5000.0
        assert pl275_nozionale(-100, 50.0) == 5000.0
        with pytest.raises(ValueError):
            pl275_nozionale(100, -1.0)

    def test_aggrega(self):
        pos = pl275_parse_posizioni(CSV_POS + "Power CAL-27 Baseload,1000,short,100.0\n")
        agg = pl275_aggrega(pos)
        cal = [a for a in agg if a["prodotto"] == "Power CAL-27 Baseload"][0]
        assert cal["qta_lorda_mwh"] == 6000.0
        assert cal["qta_netta_mwh"] == 4000.0
        assert cal["n_posizioni"] == 2
        assert cal["prezzo_medio_eur_mwh"] == pytest.approx(
            (5000 * 98.5 + 1000 * 100.0) / 6000.0)

    def test_check_limiti(self):
        pos = pl275_parse_posizioni(CSV_POS)
        lim = pl275_parse_limiti(CSV_LIM)
        ck = pl275_check_limiti(pos, lim)
        assert len(ck) == 3
        # ordinato per utilizzo desc
        assert ck[0]["prodotto"] == "Power Q2-27 Peak"
        assert ck[0]["utilizzo_pct"] == 125.0
        assert ck[0]["stato"] == "breach"
        assert ck[1]["stato"] == "attenzione"
        assert ck[2]["stato"] == "ok"

    def test_check_senza_limite(self):
        pos = pl275_parse_posizioni("Z,100,long,10.0")
        ck = pl275_check_limiti(pos, {})
        assert ck[0]["utilizzo_pct"] is None
        assert ck[0]["stato"] == "senza_limite"


class TestPl275Riepilogo:
    def test_base(self):
        pos = pl275_parse_posizioni(CSV_POS)
        lim = pl275_parse_limiti(CSV_LIM)
        ck = pl275_check_limiti(pos, lim)
        r = pl275_riepilogo(ck, pos)
        assert r["n_posizioni"] == 3
        assert r["n_prodotti"] == 3
        assert r["n_breach"] == 1
        assert r["n_critici"] == 0
        assert r["utilizzo_max_pct"] == 125.0
        assert r["nozionale_tot_eur"] == pytest.approx(
            5000 * 98.5 + 2500 * 112.0 + 8000 * 38.2)
        assert r["esposizione_netta_mwh"] == pytest.approx(5000 - 2500 + 8000)

    def test_vuoto(self):
        r = pl275_riepilogo([], [])
        assert r["n_posizioni"] == 0
        assert r["utilizzo_max_pct"] is None
        assert r["nozionale_tot_eur"] == 0.0
