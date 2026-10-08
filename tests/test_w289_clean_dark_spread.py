"""Test tab289 '⚫🔥 Clean dark spread: margine centrale a carbone': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab289.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("cds289_num", "cds289_pos", "cds289_frac", "cds289_carbone_mwh",
          "cds289_costo_carbone_el", "cds289_emissioni", "cds289_costo_co2",
          "cds289_dark", "cds289_clean_dark", "cds289_fissi_unitari",
          "cds289_margine_ora", "cds289_pnl", "cds289_be_power",
          "cds289_be_carbone", "cds289_breakdown", "cds289_sensibilita_carbone",
          "cds289_verdetto")
cds289_num = _F["cds289_num"]
cds289_pos = _F["cds289_pos"]
cds289_frac = _F["cds289_frac"]
cds289_carbone_mwh = _F["cds289_carbone_mwh"]
cds289_costo_carbone_el = _F["cds289_costo_carbone_el"]
cds289_emissioni = _F["cds289_emissioni"]
cds289_costo_co2 = _F["cds289_costo_co2"]
cds289_dark = _F["cds289_dark"]
cds289_clean_dark = _F["cds289_clean_dark"]
cds289_fissi_unitari = _F["cds289_fissi_unitari"]
cds289_margine_ora = _F["cds289_margine_ora"]
cds289_pnl = _F["cds289_pnl"]
cds289_be_power = _F["cds289_be_power"]
cds289_be_carbone = _F["cds289_be_carbone"]
cds289_breakdown = _F["cds289_breakdown"]
cds289_sensibilita_carbone = _F["cds289_sensibilita_carbone"]
cds289_verdetto = _F["cds289_verdetto"]

APP = Path(__file__).parent.parent / "app.py"

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
TITLE288 = "⚡🔥 Clean spark spread: margine centrale a gas"
TITLE287 = "🚢⚡ Rigassificazione GNL: margine terminale"
TITLE286 = "⛽ Basis gas TTF–PSV"

POWER, COAL, CAMBIO, PCI = 105.0, 115.0, 1.08, 6.8
EFF, CO2P, CO2F = 0.42, 85.0, 0.341
ORE, CAP, FISSI, SOGLIA = 7000.0, 750.0, 25000000.0, 5.0

COAL_TERM_ATT = COAL / PCI / CAMBIO
COAL_EL_ATT = COAL_TERM_ATT / EFF
EMIS_ATT = CO2F / EFF
CO2C_ATT = CO2P * EMIS_ATT
DARK_ATT = POWER - COAL_EL_ATT
CLEAN_ATT = DARK_ATT - CO2C_ATT
FU_ATT = FISSI / (ORE * CAP)
MARG_ATT = CLEAN_ATT - FU_ATT
PNL_ATT = CLEAN_ATT * ORE * CAP - FISSI
BEPOW_ATT = COAL_EL_ATT + CO2C_ATT + FU_ATT
BECOAL_ATT = (POWER - CO2C_ATT - FU_ATT) * EFF * CAMBIO * PCI


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab289:
    def test_tab289_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 312
        assert TITLE289 in titoli
        assert "tab289" in dvars
        assert "tab289" in withs
        assert titoli[dvars.index("tab289")] == TITLE289
        assert titoli[-1] == TITLE312
        keys = re.findall(r'key="(cds289_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_287_288_289(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab287")] == TITLE287
        assert titoli[dvars.index("tab288")] == TITLE288
        assert titoli[dvars.index("tab289")] == TITLE289


class TestCds289Validatori:
    def test_num_ok(self):
        assert cds289_num(1.5, "x") == 1.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            cds289_num(True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            cds289_num(float("nan"), "x")

    def test_pos_negativo_ko(self):
        with pytest.raises(ValueError):
            cds289_pos(-0.1, "x")

    def test_frac_ok(self):
        assert cds289_frac(0.42, "e") == pytest.approx(0.42)

    def test_frac_zero_ko(self):
        with pytest.raises(ValueError):
            cds289_frac(0.0, "e")

    def test_frac_sopra_uno_ko(self):
        with pytest.raises(ValueError):
            cds289_frac(1.2, "e")


class TestCds289Conversione:
    def test_carbone_mwh(self):
        assert cds289_carbone_mwh(COAL, CAMBIO, PCI) == pytest.approx(
            COAL_TERM_ATT)

    def test_carbone_mwh_cambio_zero_ko(self):
        with pytest.raises(ValueError):
            cds289_carbone_mwh(COAL, 0.0, PCI)

    def test_carbone_mwh_pci_zero_ko(self):
        with pytest.raises(ValueError):
            cds289_carbone_mwh(COAL, CAMBIO, 0.0)

    def test_costo_carbone_el(self):
        assert cds289_costo_carbone_el(COAL_TERM_ATT,
                                       EFF) == pytest.approx(COAL_EL_ATT)

    def test_emissioni(self):
        assert cds289_emissioni(CO2F, EFF) == pytest.approx(EMIS_ATT)

    def test_costo_co2(self):
        assert cds289_costo_co2(CO2P, EMIS_ATT) == pytest.approx(CO2C_ATT)


class TestCds289Dark:
    def test_dark(self):
        assert cds289_dark(POWER, COAL_EL_ATT) == pytest.approx(DARK_ATT)

    def test_clean_dark(self):
        assert cds289_clean_dark(POWER, COAL, CAMBIO, PCI, EFF, CO2P,
                                  CO2F) == pytest.approx(CLEAN_ATT)

    def test_clean_dark_coerenza(self):
        assert cds289_clean_dark(POWER, COAL, CAMBIO, PCI, EFF, CO2P,
                                  CO2F) == pytest.approx(
            cds289_dark(POWER, cds289_costo_carbone_el(
                cds289_carbone_mwh(COAL, CAMBIO, PCI), EFF)) -
            cds289_costo_co2(CO2P, cds289_emissioni(CO2F, EFF)))


class TestCds289MarginePnl:
    def test_fissi_unitari(self):
        assert cds289_fissi_unitari(FISSI, ORE, CAP) == pytest.approx(FU_ATT)

    def test_fissi_unitari_ore_zero_ko(self):
        with pytest.raises(ValueError):
            cds289_fissi_unitari(FISSI, 0.0, CAP)

    def test_margine_ora(self):
        assert cds289_margine_ora(CLEAN_ATT, FU_ATT) == pytest.approx(MARG_ATT)

    def test_pnl(self):
        assert cds289_pnl(CLEAN_ATT, ORE, CAP,
                         FISSI) == pytest.approx(PNL_ATT)

    def test_be_power(self):
        assert cds289_be_power(COAL, CAMBIO, PCI, EFF, CO2P, CO2F,
                               FU_ATT) == pytest.approx(BEPOW_ATT)

    def test_be_power_annulla_margine(self):
        assert cds289_margine_ora(
            cds289_clean_dark(BEPOW_ATT, COAL, CAMBIO, PCI, EFF, CO2P,
                              CO2F), FU_ATT) == pytest.approx(0.0)

    def test_be_carbone(self):
        assert cds289_be_carbone(POWER, CAMBIO, PCI, EFF, CO2P, CO2F,
                                 FU_ATT) == pytest.approx(BECOAL_ATT)

    def test_be_carbone_annulla_margine(self):
        assert cds289_margine_ora(
            cds289_clean_dark(POWER, BECOAL_ATT, CAMBIO, PCI, EFF, CO2P,
                              CO2F), FU_ATT) == pytest.approx(0.0)

    def test_be_carbone_none_quando_power_basso(self):
        assert cds289_be_carbone(10.0, CAMBIO, PCI, EFF, CO2P, CO2F,
                                 FU_ATT) is None

    def test_be_carbone_cambio_zero_ko(self):
        with pytest.raises(ValueError):
            cds289_be_carbone(POWER, 0.0, PCI, EFF, CO2P, CO2F, FU_ATT)


class TestCds289Breakdown:
    def test_chiavi_e_somma(self):
        b = cds289_breakdown(POWER, COAL_EL_ATT, CO2C_ATT, FU_ATT, MARG_ATT)
        assert set(b) == {"prezzo_power", "costo_carbone", "costo_co2",
                          "quota_fissa", "margine_ora"}
        assert b["prezzo_power"] - b["costo_carbone"] - b["costo_co2"] - \
            b["quota_fissa"] == pytest.approx(b["margine_ora"])

    def test_breakdown_costo_negativo_ko(self):
        with pytest.raises(ValueError):
            cds289_breakdown(POWER, -1.0, CO2C_ATT, FU_ATT, MARG_ATT)


class TestCds289Sensibilita:
    def test_struttura(self):
        righe = cds289_sensibilita_carbone(COAL, CAMBIO, PCI, EFF, CO2P,
                                           CO2F, POWER, FU_ATT)
        assert len(righe) == 9
        assert righe[4]["coal_usd_t"] == pytest.approx(COAL)
        assert righe[4]["margine"] == pytest.approx(MARG_ATT)
        assert righe[0]["coal_usd_t"] == pytest.approx(COAL * 0.85)
        assert righe[-1]["coal_usd_t"] == pytest.approx(COAL * 1.15)
        for r in righe:
            assert r["margine"] == pytest.approx(r["clean_dark"] - FU_ATT)

    def test_n_punti_ko(self):
        with pytest.raises(ValueError):
            cds289_sensibilita_carbone(COAL, CAMBIO, PCI, EFF, CO2P, CO2F,
                                      POWER, FU_ATT, n_punti=2)

    def test_ampiezza_ko(self):
        with pytest.raises(ValueError):
            cds289_sensibilita_carbone(COAL, CAMBIO, PCI, EFF, CO2P, CO2F,
                                      POWER, FU_ATT, ampiezza=0.0)


class TestCds289Verdetto:
    def test_profittevole(self):
        assert cds289_verdetto(8.0, SOGLIA)["verdetto"] == "profittevole"

    def test_copre_i_costi(self):
        assert cds289_verdetto(2.0, SOGLIA)["verdetto"] == "copre_i_costi"

    def test_in_perdita(self):
        assert cds289_verdetto(-0.5, SOGLIA)["verdetto"] == "in_perdita"

    def test_soglia_negativa_ko(self):
        with pytest.raises(ValueError):
            cds289_verdetto(2.0, -1.0)
