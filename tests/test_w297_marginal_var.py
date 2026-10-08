"""Test tab297 '➕📊 Marginal VaR: quanto rischio aggiunge il nuovo trade?': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab297. Marginal/incremental VaR parametrico:
decision tool pre-trade (follow-up di tab292 Component VaR).
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("mv297_num", "mv297_conf", "mv297_corr",
          "mv297_parse_posizioni", "mv297_norm_cdf", "mv297_norm_ppf",
          "mv297_sigma_port", "mv297_componenti", "mv297_incrementale",
          "mv297_verdetto")
mv297_num = _F["mv297_num"]
mv297_conf = _F["mv297_conf"]
mv297_corr = _F["mv297_corr"]
mv297_parse_posizioni = _F["mv297_parse_posizioni"]
mv297_norm_cdf = _F["mv297_norm_cdf"]
mv297_norm_ppf = _F["mv297_norm_ppf"]
mv297_sigma_port = _F["mv297_sigma_port"]
mv297_componenti = _F["mv297_componenti"]
mv297_incrementale = _F["mv297_incrementale"]
mv297_verdetto = _F["mv297_verdetto"]

APP = Path(__file__).parent.parent / "app.py"

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
TITLE296 = "🪓🛡 Component ES: chi contribuisce alla coda?"
TITLE295 = "🧪🛡 Backtest dell'ES: la coda e' sottostimata?"

# book sintetico 2 posizioni a valori noti
SYN_POS = [("A", 1_000_000.0, 0.02), ("B", 500_000.0, 0.03)]
SYN_CAND = ("C", 200_000.0, 0.04, 0.5)

DEMO_TXT = """# book demo: nome;nozionale eur;vol % giornaliera
Gas TTF;2500000;3,2
Power DE;1800000;2,6
CO2 EUA;900000;2,1
Spark spread;1200000;4,0"""


def _demo_pos():
    return mv297_parse_posizioni(DEMO_TXT)


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab297:
    def test_tab297_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 310
        assert TITLE297 in titoli
        assert "tab297" in dvars
        assert "tab297" in withs
        assert titoli[dvars.index("tab297")] == TITLE297
        assert titoli[-1] == TITLE310
        keys = re.findall(r'key="(mv297_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_295_296_297(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab295")] == TITLE295
        assert titoli[dvars.index("tab296")] == TITLE296
        assert titoli[dvars.index("tab297")] == TITLE297


class TestMv297Validatori:
    def test_num_ok(self):
        assert mv297_num(2.5, "x") == 2.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            mv297_num(True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            mv297_num(float("nan"), "x")

    def test_conf_ok(self):
        assert mv297_conf(0.99) == 0.99

    def test_conf_bordi_ko(self):
        with pytest.raises(ValueError):
            mv297_conf(1.0)

    def test_corr_ok(self):
        assert mv297_corr(-1.0, "r") == -1.0
        assert mv297_corr(0.5, "r") == 0.5

    def test_corr_fuori_ko(self):
        with pytest.raises(ValueError):
            mv297_corr(1.5, "r")


class TestMv297Parse:
    def test_ok(self):
        t = "# cmt\n\n" + "\n".join(["Gas;1000000;2,5"] * 2)
        p = mv297_parse_posizioni(t)
        assert len(p) == 2 and p[0][0] == "Gas"
        assert p[0][1] == pytest.approx(1_000_000.0)
        assert p[0][2] == pytest.approx(0.025)

    def test_una_posizione_ko(self):
        with pytest.raises(ValueError):
            mv297_parse_posizioni("Gas;1000000;2,5")

    def test_colonne_sbagliate_ko(self):
        with pytest.raises(ValueError):
            mv297_parse_posizioni("Gas;1000000\nPower;2000000")

    def test_nozionale_ko(self):
        with pytest.raises(ValueError):
            mv297_parse_posizioni("Gas;-5;2,5\nPower;2000000;2")

    def test_non_numerico_ko(self):
        with pytest.raises(ValueError):
            mv297_parse_posizioni("Gas;xx;2,5\nPower;2000000;2")


class TestMv297Norm:
    def test_cdf_nota(self):
        assert mv297_norm_cdf(0.0) == pytest.approx(0.5)
        assert mv297_norm_cdf(1.959963984540054) == pytest.approx(0.975, abs=1e-6)

    def test_ppf_noti(self):
        assert mv297_norm_ppf(0.5) == pytest.approx(0.0, abs=1e-9)
        assert mv297_norm_ppf(0.975) == pytest.approx(1.959963984540054,
                                                     rel=1e-6)
        assert mv297_norm_ppf(0.99) == pytest.approx(2.3263478740408408,
                                                     rel=1e-6)

    def test_ppf_bordi_ko(self):
        with pytest.raises(ValueError):
            mv297_norm_ppf(0.0)
        with pytest.raises(ValueError):
            mv297_norm_ppf(1.0)


class TestMv297Sigma:
    def test_sintetico(self):
        # v = [20000, 15000], rho=0.5:
        # var = 20000^2+15000^2+2*0.5*20000*15000
        assert mv297_sigma_port(SYN_POS, 0.5) == pytest.approx(30413.8126514911)

    def test_rho_zero(self):
        assert mv297_sigma_port(SYN_POS, 0.0) == pytest.approx(25000.0)

    def test_una_posizione_ko(self):
        with pytest.raises(ValueError):
            mv297_sigma_port([SYN_POS[0]], 0.5)


class TestMv297Componenti:
    def test_somma_eulero(self):
        r = mv297_componenti(SYN_POS, 0.5, 0.99)
        assert r["somma"] == pytest.approx(r["var"])
        assert r["var"] == pytest.approx(70753.1084032727)
        assert r["componenti"][0] == pytest.approx(42069.415807351324)
        assert r["componenti"][1] == pytest.approx(28683.69259592136)

    def test_nomi(self):
        r = mv297_componenti(SYN_POS, 0.5, 0.99)
        assert r["nomi"] == ["A", "B"]


class TestMv297Incrementale:
    def test_valori_noti(self):
        r = mv297_incrementale(SYN_POS, 0.5, 0.99, SYN_CAND)
        assert r["var_old"] == pytest.approx(70753.1084032727)
        assert r["var_new"] == pytest.approx(82871.55140944295)
        assert r["incrementale"] == pytest.approx(12118.443006170259)
        assert r["incrementale"] == pytest.approx(r["var_new"] - r["var_old"])
        assert r["componente_candidato"] == pytest.approx(13322.140652109032)
        assert r["standalone_candidato"] == pytest.approx(18610.782992326713)
        assert r["diversificazione"] == pytest.approx(5288.642340217681)
        assert r["quota"] == pytest.approx(r["incrementale"] / r["var_old"])

    def test_nozionale_c_ko(self):
        with pytest.raises(ValueError):
            mv297_incrementale(SYN_POS, 0.5, 0.99, ("C", -1.0, 0.04, 0.5))


class TestMv297Verdetto:
    def test_trascurabile(self):
        assert mv297_verdetto(100.0, 10000.0).startswith("impatto trascurabile")

    def test_contenuto(self):
        assert mv297_verdetto(1000.0, 10000.0).startswith("impatto contenuto")

    def test_rilevante(self):
        assert mv297_verdetto(3000.0, 10000.0).startswith("impatto rilevante")

    def test_soglie(self):
        assert mv297_verdetto(500.0, 10000.0).startswith("impatto contenuto")
        assert mv297_verdetto(2000.0, 10000.0).startswith("impatto rilevante")

    def test_var_old_ko(self):
        with pytest.raises(ValueError):
            mv297_verdetto(100.0, 0.0)


class TestMv297Integrazione:
    def test_catena_demo(self):
        pos = _demo_pos()
        assert len(pos) == 4
        r = mv297_incrementale(pos, 0.35, 0.99,
                               ("Coal API2", 800000.0, 0.028, 0.45))
        assert r["var_old"] == pytest.approx(332637.92510122136)
        assert r["var_new"] == pytest.approx(366738.14339864254)
        assert r["incrementale"] == pytest.approx(34100.218297421176)
        assert r["componente_candidato"] == pytest.approx(36217.051915279015)
        assert r["diversificazione"] == pytest.approx(15893.14046323578)
        assert mv297_verdetto(r["incrementale"],
                              r["var_old"]) == 'impatto contenuto: il trade alza il VaR in misura gestibile'
        # parse round-trip della demo come appare nella UI
        p2 = mv297_parse_posizioni(DEMO_TXT)
        assert len(p2) == 4
