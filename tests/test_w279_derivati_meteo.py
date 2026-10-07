"""Test tab279 'Derivati meteo: pricing HDD/CDD': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab279.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("wd279_num", "wd279_tipo_indice", "wd279_lato",
          "wd279_gradi_giorno", "wd279_indice_periodo", "wd279_payoff",
          "wd279_burn", "wd279_intervallo_confidenza",
          "wd279_prob_in_the_money", "wd279_sensibilita_strike",
          "wd279_verdetto", "wd279_parse_serie")
wd279_num = _F["wd279_num"]
wd279_tipo_indice = _F["wd279_tipo_indice"]
wd279_lato = _F["wd279_lato"]
wd279_gradi_giorno = _F["wd279_gradi_giorno"]
wd279_indice_periodo = _F["wd279_indice_periodo"]
wd279_payoff = _F["wd279_payoff"]
wd279_burn = _F["wd279_burn"]
wd279_intervallo_confidenza = _F["wd279_intervallo_confidenza"]
wd279_prob_in_the_money = _F["wd279_prob_in_the_money"]
wd279_sensibilita_strike = _F["wd279_sensibilita_strike"]
wd279_verdetto = _F["wd279_verdetto"]
wd279_parse_serie = _F["wd279_parse_serie"]

APP = Path(__file__).parent.parent / "app.py"

TITLE279 = "\U0001f32a\ufe0f Derivati meteo: pricing HDD/CDD"
TITLE280 = "🚢 LNG vs gasdotto: costo delivered"
TITLE281 = "🛢️ Crack spread: margine raffinazione 3-2-1"
TITLE282 = "🧪 Margine petrolchimico: nafta → etilene"
TITLE283 = "🛢️ Carry petrolio: contango & stoccaggio fisico"
TITLE278 = "\U0001f321\ufe0f Stress climatico: domanda e prezzo"
TITLE277 = "\u26a1 Aste MI: scostamenti vs MGP"

INDICI = [300.0, 400.0]
STRIKE = 300.0
TICK = 10.0


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab279:
    def test_tab279_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 283
        assert TITLE279 in titoli
        assert "tab279" in dvars
        assert "tab279" in withs
        assert titoli[dvars.index("tab279")] == TITLE279
        assert titoli[-1] == TITLE283
        keys = re.findall(r'key="(wd279_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_277_278_279(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab277")] == TITLE277
        assert titoli[dvars.index("tab278")] == TITLE278
        assert titoli[dvars.index("tab279")] == TITLE279
        assert titoli[dvars.index("tab280")] == TITLE280
        assert titoli[dvars.index("tab281")] == TITLE281
        assert titoli[dvars.index("tab282")] == TITLE282
        assert titoli[dvars.index("tab283")] == TITLE283


class TestWd279Validatori:
    def test_num_ok(self):
        assert wd279_num(3, "x") == 3.0
        assert wd279_num(2.5, "x") == 2.5

    def test_num_invalidi(self):
        for bad in (True, False, float("nan"), float("inf"), "3", None):
            with pytest.raises(ValueError):
                wd279_num(bad, "x")

    def test_tipo(self):
        assert wd279_tipo_indice("hdd") == "HDD"
        assert wd279_tipo_indice(" CDD ") == "CDD"
        for bad in ("X", "", 3, None):
            with pytest.raises(ValueError):
                wd279_tipo_indice(bad)

    def test_lato(self):
        assert wd279_lato("Call") == "call"
        assert wd279_lato("PUT") == "put"
        for bad in ("x", "", 1, None):
            with pytest.raises(ValueError):
                wd279_lato(bad)


class TestWd279GradiGiorno:
    def test_hdd(self):
        assert wd279_gradi_giorno(10.0, 18.0, "HDD") == pytest.approx(8.0)
        assert wd279_gradi_giorno(20.0, 18.0, "HDD") == pytest.approx(0.0)

    def test_cdd(self):
        assert wd279_gradi_giorno(25.0, 18.0, "CDD") == pytest.approx(7.0)
        assert wd279_gradi_giorno(15.0, 18.0, "CDD") == pytest.approx(0.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            wd279_gradi_giorno(10.0, 18.0, "X")
        with pytest.raises(ValueError):
            wd279_gradi_giorno("10", 18.0, "HDD")


class TestWd279IndicePeriodo:
    def test_base(self):
        assert wd279_indice_periodo([10.0, 20.0], 18.0, "HDD") == pytest.approx(8.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            wd279_indice_periodo([], 18.0, "HDD")
        with pytest.raises(ValueError):
            wd279_indice_periodo(None, 18.0, "HDD")
        with pytest.raises(ValueError):
            wd279_indice_periodo([10.0, "x"], 18.0, "HDD")


class TestWd279Payoff:
    def test_call(self):
        assert wd279_payoff(350.0, STRIKE, TICK, "call") == pytest.approx(500.0)
        assert wd279_payoff(250.0, STRIKE, TICK, "call") == pytest.approx(0.0)

    def test_put(self):
        assert wd279_payoff(250.0, STRIKE, TICK, "put") == pytest.approx(500.0)
        assert wd279_payoff(350.0, STRIKE, TICK, "put") == pytest.approx(0.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            wd279_payoff(350.0, STRIKE, 0.0, "call")
        with pytest.raises(ValueError):
            wd279_payoff(-1.0, STRIKE, TICK, "call")
        with pytest.raises(ValueError):
            wd279_payoff(350.0, -1.0, TICK, "call")
        with pytest.raises(ValueError):
            wd279_payoff(350.0, STRIKE, TICK, "x")


class TestWd279Burn:
    def test_base(self):
        b = wd279_burn(INDICI, STRIKE, TICK, "call")
        assert b["n_anni"] == 2
        assert b["premio"] == pytest.approx(500.0)
        assert b["dev_std"] == pytest.approx(500.0)
        assert b["payoff_min"] == pytest.approx(0.0)
        assert b["payoff_max"] == pytest.approx(1000.0)
        assert b["payoff_anni"] == pytest.approx([0.0, 1000.0])

    def test_un_anno(self):
        b = wd279_burn([350.0], STRIKE, TICK, "call")
        assert b["premio"] == pytest.approx(500.0)
        assert b["dev_std"] == pytest.approx(0.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            wd279_burn([], STRIKE, TICK, "call")
        with pytest.raises(ValueError):
            wd279_burn([-5.0, 300.0], STRIKE, TICK, "call")


class TestWd279Intervallo:
    def test_base(self):
        ic = wd279_intervallo_confidenza(500.0, 500.0, 2)
        assert ic["inf"] == pytest.approx(0.0)
        assert ic["sup"] == pytest.approx(500.0 + 1.96 * 500.0 / 2 ** 0.5)

    def test_zero_sd(self):
        ic = wd279_intervallo_confidenza(500.0, 0.0, 10)
        assert ic["inf"] == pytest.approx(500.0)
        assert ic["sup"] == pytest.approx(500.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            wd279_intervallo_confidenza(-1.0, 500.0, 2)
        with pytest.raises(ValueError):
            wd279_intervallo_confidenza(500.0, -1.0, 2)
        with pytest.raises(ValueError):
            wd279_intervallo_confidenza(500.0, 500.0, 0)


class TestWd279ProbItm:
    def test_base(self):
        assert wd279_prob_in_the_money(INDICI, STRIKE, TICK, "call") == pytest.approx(0.5)

    def test_sempre_itm(self):
        assert wd279_prob_in_the_money([400.0, 500.0], STRIKE, TICK, "call") == pytest.approx(1.0)


class TestWd279Sensibilita:
    def test_struttura(self):
        righe = wd279_sensibilita_strike(INDICI, STRIKE, TICK, "call", 5)
        assert len(righe) == 5
        assert righe[0]["strike"] == pytest.approx(60.0)
        assert righe[-1]["strike"] == pytest.approx(540.0)
        assert set(righe[0]) == {"strike", "premio"}

    def test_monotonia_call(self):
        # il premio burn e' non-crescente nello strike (0 quando strike >= max storico)
        righe = wd279_sensibilita_strike(INDICI, STRIKE, TICK, "call", 5)
        premi = [r["premio"] for r in righe]
        assert all(b <= a for a, b in zip(premi, premi[1:]))
        assert righe[2]["premio"] == pytest.approx(500.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            wd279_sensibilita_strike(INDICI, 0.0, TICK, "call")
        with pytest.raises(ValueError):
            wd279_sensibilita_strike(INDICI, STRIKE, TICK, "call", 2)


class TestWd279Verdetto:
    def test_conveniente(self):
        r = wd279_verdetto(500.0, 1000.0)
        assert r["verdetto"] == "conveniente"
        assert r["rapporto"] == pytest.approx(0.5)
        assert r["scostamento_eur"] == pytest.approx(-500.0)

    def test_in_linea(self):
        r = wd279_verdetto(1050.0, 1000.0)
        assert r["verdetto"] == "in_linea"

    def test_sopra_budget(self):
        r = wd279_verdetto(1500.0, 1000.0)
        assert r["verdetto"] == "sopra_budget"
        assert r["scostamento_eur"] == pytest.approx(500.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            wd279_verdetto(500.0, 0.0)
        with pytest.raises(ValueError):
            wd279_verdetto(-1.0, 1000.0)


class TestWd279ParseSerie:
    def test_misto(self):
        assert wd279_parse_serie("1, 2\n3;4") == [1.0, 2.0, 3.0, 4.0]

    def test_invalidi(self):
        with pytest.raises(ValueError):
            wd279_parse_serie("")
        with pytest.raises(ValueError):
            wd279_parse_serie("   ")
        with pytest.raises(ValueError):
            wd279_parse_serie("1, x")
