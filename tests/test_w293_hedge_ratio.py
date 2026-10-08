"""Test tab293 '🛡📉 Hedge ratio ottimale: quanto coprire con i futures?': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab293.
"""

import math
import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("hr293_num", "hr293_pos", "hr293_parse_serie", "hr293_media",
          "hr293_varianza", "hr293_covarianza", "hr293_correlazione",
          "hr293_hedge_ratio", "hr293_efficacia", "hr293_numero_contratti",
          "hr293_norm_ppf", "hr293_var", "hr293_vol_residua",
          "hr293_verdetto")
hr293_num = _F["hr293_num"]
hr293_pos = _F["hr293_pos"]
hr293_parse_serie = _F["hr293_parse_serie"]
hr293_media = _F["hr293_media"]
hr293_varianza = _F["hr293_varianza"]
hr293_covarianza = _F["hr293_covarianza"]
hr293_correlazione = _F["hr293_correlazione"]
hr293_hedge_ratio = _F["hr293_hedge_ratio"]
hr293_efficacia = _F["hr293_efficacia"]
hr293_numero_contratti = _F["hr293_numero_contratti"]
hr293_norm_ppf = _F["hr293_norm_ppf"]
hr293_var = _F["hr293_var"]
hr293_vol_residua = _F["hr293_vol_residua"]
hr293_verdetto = _F["hr293_verdetto"]

APP = Path(__file__).parent.parent / "app.py"

TITLE293 = "\U0001F6E1\U0001F4C9 Hedge ratio ottimale: quanto coprire con i futures?"
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
TITLE292 = "🪓📊 Component VaR: quale posizione tagliare per prima?"
TITLE291 = "📊💹 Sharpe & Sortino: la strategia rende davvero?"

# relazione lineare quasi perfetta: fut = spot * 0.98 + 0.3 + rumore
SPOT = [35.2, 35.8, 34.6, 36.1, 36.7, 35.4, 37.1, 37.6, 36.9, 38.2, 38.8, 37.5]
FUT = [s * 0.98 + 0.3 for s in SPOT]


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab293:
    def test_tab293_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 319
        assert TITLE293 in titoli
        assert "tab293" in dvars
        assert "tab293" in withs
        assert titoli[dvars.index("tab293")] == TITLE293
        assert titoli[-1] == TITLE319
        keys = re.findall(r'key="(hr293_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_291_292_293(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab291")] == TITLE291
        assert titoli[dvars.index("tab292")] == TITLE292
        assert titoli[dvars.index("tab293")] == TITLE293


class TestHr293Validatori:
    def test_num_ok(self):
        assert hr293_num(2.5, "x") == 2.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            hr293_num(True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            hr293_num(float("nan"), "x")

    def test_pos_zero_ko(self):
        with pytest.raises(ValueError):
            hr293_pos(0.0, "x")

    def test_media(self):
        assert hr293_media([1.0, 2.0, 3.0]) == pytest.approx(2.0)

    def test_media_vuota_ko(self):
        with pytest.raises(ValueError):
            hr293_media([])


class TestHr293Parse:
    def test_ok(self):
        s, f = hr293_parse_serie("35,2;34,9\n# cmt\n\n36.1;35,90")
        assert s == pytest.approx([35.2, 36.1])
        assert f == pytest.approx([34.9, 35.9])

    def test_riga_malformata_ko(self):
        with pytest.raises(ValueError):
            hr293_parse_serie("35.2")

    def test_non_numerico_ko(self):
        with pytest.raises(ValueError):
            hr293_parse_serie("35.2;abc\n36.1;35.9")

    def test_una_sola_coppia_ko(self):
        with pytest.raises(ValueError):
            hr293_parse_serie("35.2;34.9")


class TestHr293Stat:
    def test_varianza_nota(self):
        # varianza campionaria di [2,4,4,4,5,5,7,9] = 32/7
        assert hr293_varianza([2, 4, 4, 4, 5, 5, 7, 9]) == \
            pytest.approx(32.0 / 7.0)

    def test_varianza_una_ko(self):
        with pytest.raises(ValueError):
            hr293_varianza([3.0])

    def test_covarianza_simmetrica(self):
        xs = [1.0, 2.0, 3.0, 4.0]
        ys = [2.0, 4.0, 5.0, 4.0]
        assert hr293_covarianza(xs, ys) == pytest.approx(
            hr293_covarianza(ys, xs))

    def test_covarianza_lunghezze_ko(self):
        with pytest.raises(ValueError):
            hr293_covarianza([1.0, 2.0], [1.0])

    def test_correlazione_perfetta(self):
        assert hr293_correlazione([1.0, 2.0, 3.0],
                                  [2.0, 4.0, 6.0]) == pytest.approx(1.0)

    def test_correlazione_costante_ko(self):
        with pytest.raises(ValueError):
            hr293_correlazione([5.0, 5.0, 5.0], [1.0, 2.0, 3.0])


class TestHr293Hedge:
    def test_hedge_ratio_lineare(self):
        # fut = 0.98 * spot + 0.3 -> h* = cov(spot,fut)/var(fut)
        # = 0.98*var(spot) / 0.98**2*var(spot) = 1/0.98
        h = hr293_hedge_ratio(SPOT, FUT)
        assert h == pytest.approx(1.0 / 0.98, rel=1e-9)

    def test_hedge_ratio_fut_costante_ko(self):
        with pytest.raises(ValueError):
            hr293_hedge_ratio([1.0, 2.0, 3.0], [4.0, 4.0, 4.0])

    def test_efficacia_quasi_uno(self):
        assert hr293_efficacia(SPOT, FUT) == pytest.approx(1.0, abs=1e-6)

    def test_efficacia_uguale_rho_quadro(self):
        eff = hr293_efficacia(SPOT, [s * 0.5 + 1.0 + (i % 2) * 0.01
                                     for i, s in enumerate(SPOT)])
        rho = hr293_correlazione(SPOT, [s * 0.5 + 1.0 + (i % 2) * 0.01
                                        for i, s in enumerate(SPOT)])
        assert eff == pytest.approx(rho ** 2, rel=1e-6)

    def test_efficacia_spot_costante_ko(self):
        with pytest.raises(ValueError):
            hr293_efficacia([3.0, 3.0, 3.0], [1.0, 2.0, 3.0])

    def test_numero_contratti(self):
        assert hr293_numero_contratti(2_000_000.0, 0.98, 50_000.0) == \
            pytest.approx(39.2)

    def test_numero_contratti_size_ko(self):
        with pytest.raises(ValueError):
            hr293_numero_contratti(100.0, 1.0, 0.0)


class TestHr293Var:
    def test_ppf_95(self):
        assert hr293_norm_ppf(0.95) == pytest.approx(1.64485362, rel=1e-6)

    def test_ppf_bordi_ko(self):
        with pytest.raises(ValueError):
            hr293_norm_ppf(1.0)

    def test_var_formula(self):
        att = 1_000_000.0 * 0.02 * math.sqrt(10.0) * 1.64485362
        assert hr293_var(1_000_000.0, 0.02, 10, 0.95) == \
            pytest.approx(att, rel=1e-6)

    def test_var_conf_ko(self):
        with pytest.raises(ValueError):
            hr293_var(100.0, 0.01, 5, 1.5)

    def test_copertura_riduce_var(self):
        vol = 0.02
        eff = hr293_efficacia(SPOT, FUT)
        vres = hr293_vol_residua(vol, eff)
        assert hr293_var(1e6, vres, 10, 0.95) < hr293_var(1e6, vol, 10, 0.95)

    def test_vol_residua_zero_con_efficacia_uno(self):
        assert hr293_vol_residua(0.02, 1.0) == pytest.approx(0.0)

    def test_vol_residua_fuori_range_ko(self):
        with pytest.raises(ValueError):
            hr293_vol_residua(0.02, 1.5)

    def test_verdetto(self):
        assert hr293_verdetto(0.8, 0.7)["verdetto"] == "copertura efficace"
        assert hr293_verdetto(0.5, 0.7)["verdetto"] == "copertura debole"
        assert hr293_verdetto(0.8, 0.7)["efficacia"] == pytest.approx(0.8)
