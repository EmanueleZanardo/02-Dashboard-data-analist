"""Test tab284 'Unit commitment CCGT: accendere o no?': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab284.
"""

import math
import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("uc284_num", "uc284_pos", "uc284_costo_marginale",
          "uc284_clean_spark", "uc284_costo_avviamento_tot",
          "uc284_ore_breakeven", "uc284_prezzo_breakeven", "uc284_pnl",
          "uc284_verdetto", "uc284_sensibilita_prezzo")
uc284_num = _F["uc284_num"]
uc284_pos = _F["uc284_pos"]
uc284_costo_marginale = _F["uc284_costo_marginale"]
uc284_clean_spark = _F["uc284_clean_spark"]
uc284_costo_avviamento_tot = _F["uc284_costo_avviamento_tot"]
uc284_ore_breakeven = _F["uc284_ore_breakeven"]
uc284_prezzo_breakeven = _F["uc284_prezzo_breakeven"]
uc284_pnl = _F["uc284_pnl"]
uc284_verdetto = _F["uc284_verdetto"]
uc284_sensibilita_prezzo = _F["uc284_sensibilita_prezzo"]

APP = Path(__file__).parent.parent / "app.py"

TITLE284 = "\U0001F3ED Unit commitment CCGT: accendere o no?"
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
TITLE283 = "\U0001F6E2\uFE0F Carry petrolio: contango & stoccaggio fisico"
TITLE282 = "\U0001F9EA Margine petrolchimico: nafta \u2192 etilene"

POWER, GAS, EFF = 110.0, 38.0, 58.0
CO2, EMIS, VOM = 75.0, 0.202, 2.5
AVV_MW, POT, ORE = 60.0, 400.0, 12.0
CM_ATTESO = GAS / (EFF / 100.0) + CO2 * EMIS / (EFF / 100.0) + VOM
SPARK_ATTESO = POWER - CM_ATTESO
AVVTOT_ATTESO = AVV_MW * POT
OREBE_ATTESA = AVVTOT_ATTESO / (SPARK_ATTESO * POT)
PBE_ATTESO = CM_ATTESO + AVVTOT_ATTESO / (POT * ORE)
PNL_ATTESO = SPARK_ATTESO * POT * ORE - AVVTOT_ATTESO


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab284:
    def test_tab284_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 317
        assert TITLE284 in titoli
        assert "tab284" in dvars
        assert "tab284" in withs
        assert titoli[dvars.index("tab284")] == TITLE284
        assert titoli[-1] == TITLE317
        keys = re.findall(r'key="(uc284_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_282_283_284(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab282")] == TITLE282
        assert titoli[dvars.index("tab283")] == TITLE283
        assert titoli[dvars.index("tab284")] == TITLE284
        assert titoli[dvars.index("tab285")] == TITLE285


class TestUc284Validatori:
    def test_num_ok(self):
        assert uc284_num(3, "x") == 3.0
        assert uc284_num(-2.5, "x") == -2.5

    def test_num_ko(self):
        with pytest.raises(ValueError):
            uc284_num(True, "x")
        with pytest.raises(ValueError):
            uc284_num("3", "x")
        with pytest.raises(ValueError):
            uc284_num(float("nan"), "x")
        with pytest.raises(ValueError):
            uc284_num(float("inf"), "x")

    def test_pos_ok(self):
        assert uc284_pos(0, "x") == 0.0
        assert uc284_pos(38, "x") == 38.0

    def test_pos_ko(self):
        with pytest.raises(ValueError):
            uc284_pos(-0.1, "x")


class TestUc284CostoMarginale:
    def test_base(self):
        assert uc284_costo_marginale(GAS, EFF, CO2, EMIS, VOM) == pytest.approx(CM_ATTESO)

    def test_scomposizione(self):
        assert uc284_costo_marginale(GAS, EFF, CO2, EMIS, VOM) == pytest.approx(
            GAS / (EFF / 100.0) + CO2 * EMIS / (EFF / 100.0) + VOM)

    def test_senza_co2(self):
        assert uc284_costo_marginale(GAS, EFF, 0.0, EMIS, VOM) == pytest.approx(
            GAS / (EFF / 100.0) + VOM)

    def test_efficienza_maggiore_costo_minore(self):
        assert uc284_costo_marginale(GAS, 62.0, CO2, EMIS, VOM) < \
            uc284_costo_marginale(GAS, EFF, CO2, EMIS, VOM)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            uc284_costo_marginale(GAS, 0.0, CO2, EMIS, VOM)
        with pytest.raises(ValueError):
            uc284_costo_marginale(GAS, 101.0, CO2, EMIS, VOM)
        with pytest.raises(ValueError):
            uc284_costo_marginale(-1.0, EFF, CO2, EMIS, VOM)


class TestUc284CleanSpark:
    def test_base(self):
        assert uc284_clean_spark(POWER, CM_ATTESO) == pytest.approx(SPARK_ATTESO)

    def test_formula(self):
        assert uc284_clean_spark(110.0, 94.14) == pytest.approx(15.86)
        assert uc284_clean_spark(80.0, 94.14) == pytest.approx(-14.14)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            uc284_clean_spark(POWER, -1.0)


class TestUc284Avviamento:
    def test_base(self):
        assert uc284_costo_avviamento_tot(AVV_MW, POT) == pytest.approx(AVVTOT_ATTESO)

    def test_zero(self):
        assert uc284_costo_avviamento_tot(0.0, POT) == pytest.approx(0.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            uc284_costo_avviamento_tot(AVV_MW, 0.0)
        with pytest.raises(ValueError):
            uc284_costo_avviamento_tot(-1.0, POT)


class TestUc284OreBreakeven:
    def test_base(self):
        assert uc284_ore_breakeven(AVVTOT_ATTESO, SPARK_ATTESO, POT) == pytest.approx(OREBE_ATTESA)

    def test_coerente_con_pnl(self):
        h = uc284_ore_breakeven(AVVTOT_ATTESO, SPARK_ATTESO, POT)
        assert uc284_pnl(POT, h, POWER, CM_ATTESO, AVVTOT_ATTESO) == pytest.approx(0.0, abs=1e-6)

    def test_spark_non_positivo_inf(self):
        assert uc284_ore_breakeven(AVVTOT_ATTESO, 0.0, POT) == float("inf")
        assert uc284_ore_breakeven(AVVTOT_ATTESO, -2.0, POT) == float("inf")

    def test_invalidi(self):
        with pytest.raises(ValueError):
            uc284_ore_breakeven(AVVTOT_ATTESO, SPARK_ATTESO, 0.0)


class TestUc284PrezzoBreakeven:
    def test_base(self):
        assert uc284_prezzo_breakeven(CM_ATTESO, AVVTOT_ATTESO, POT, ORE) == pytest.approx(PBE_ATTESO)

    def test_coerente_con_pnl(self):
        pbe = uc284_prezzo_breakeven(CM_ATTESO, AVVTOT_ATTESO, POT, ORE)
        assert uc284_pnl(POT, ORE, pbe, CM_ATTESO, AVVTOT_ATTESO) == pytest.approx(0.0, abs=1e-6)

    def test_piu_ore_piu_basso(self):
        assert uc284_prezzo_breakeven(CM_ATTESO, AVVTOT_ATTESO, POT, 24.0) < \
            uc284_prezzo_breakeven(CM_ATTESO, AVVTOT_ATTESO, POT, ORE)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            uc284_prezzo_breakeven(CM_ATTESO, AVVTOT_ATTESO, POT, 0.0)
        with pytest.raises(ValueError):
            uc284_prezzo_breakeven(CM_ATTESO, AVVTOT_ATTESO, 0.0, ORE)


class TestUc284Pnl:
    def test_base(self):
        assert uc284_pnl(POT, ORE, POWER, CM_ATTESO, AVVTOT_ATTESO) == pytest.approx(PNL_ATTESO)
        assert PNL_ATTESO > 0

    def test_formula(self):
        assert uc284_pnl(400.0, 12.0, 110.0, 94.14, 24000.0) == pytest.approx(
            (110.0 - 94.14) * 400.0 * 12.0 - 24000.0)

    def test_prezzi_negativi_ammessi(self):
        assert uc284_pnl(POT, ORE, -5.0, CM_ATTESO, AVVTOT_ATTESO) == pytest.approx(
            (-5.0 - CM_ATTESO) * POT * ORE - AVVTOT_ATTESO)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            uc284_pnl(0.0, ORE, POWER, CM_ATTESO, AVVTOT_ATTESO)
        with pytest.raises(ValueError):
            uc284_pnl(POT, -1.0, POWER, CM_ATTESO, AVVTOT_ATTESO)


class TestUc284Verdetto:
    def test_positivo(self):
        r = uc284_verdetto(52128.0, 5000.0)
        assert r["verdetto"] == "positivo"
        assert r["pnl_eur"] == pytest.approx(52128.0)

    def test_in_linea(self):
        assert uc284_verdetto(1000.0, 5000.0)["verdetto"] == "in_linea"
        assert uc284_verdetto(-5000.0, 5000.0)["verdetto"] == "in_linea"

    def test_negativo(self):
        assert uc284_verdetto(-19872.0, 5000.0)["verdetto"] == "negativo"

    def test_invalidi(self):
        with pytest.raises(ValueError):
            uc284_verdetto(1.0, -0.5)


class TestUc284Sensibilita:
    def test_struttura(self):
        righe = uc284_sensibilita_prezzo(POWER, CM_ATTESO, AVVTOT_ATTESO, POT, ORE, 5)
        assert len(righe) == 5
        assert righe[0]["prezzo_power"] == pytest.approx(0.7 * POWER)
        assert righe[-1]["prezzo_power"] == pytest.approx(1.3 * POWER)
        assert set(righe[0]) == {"prezzo_power", "pnl_eur"}

    def test_crescente_e_centro(self):
        righe = uc284_sensibilita_prezzo(POWER, CM_ATTESO, AVVTOT_ATTESO, POT, ORE, 5)
        pnl = [r["pnl_eur"] for r in righe]
        assert all(b > a for a, b in zip(pnl, pnl[1:]))
        assert righe[2]["pnl_eur"] == pytest.approx(PNL_ATTESO)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            uc284_sensibilita_prezzo(POWER, CM_ATTESO, AVVTOT_ATTESO, POT, ORE, 2)
        with pytest.raises(ValueError):
            uc284_sensibilita_prezzo(POWER, CM_ATTESO, AVVTOT_ATTESO, 0.0, ORE)
        with pytest.raises(ValueError):
            uc284_sensibilita_prezzo(POWER, CM_ATTESO, AVVTOT_ATTESO, POT, 0.0)
