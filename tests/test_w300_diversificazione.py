"""Test tab300 '🧮📊 Rapporto di diversificazione: quanto rischio risparmia il book?': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab300. Diversification Ratio del book:
sigma euro per posizione, sigma di portafoglio equicorrelato, rapporto,
beneficio %, VaR normale e risparmio VaR (follow-up del filone rischio
tab292/295/297/298/299).
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("dr300_num", "dr300_parse_book", "dr300_sigma_euro",
          "dr300_sigma_portafoglio", "dr300_rapporto", "dr300_beneficio_pct",
          "dr300_var_eur", "dr300_risparmio_var", "dr300_componenti",
          "dr300_verdetto")
dr300_num = _F["dr300_num"]
dr300_parse_book = _F["dr300_parse_book"]
dr300_sigma_euro = _F["dr300_sigma_euro"]
dr300_sigma_portafoglio = _F["dr300_sigma_portafoglio"]
dr300_rapporto = _F["dr300_rapporto"]
dr300_beneficio_pct = _F["dr300_beneficio_pct"]
dr300_var_eur = _F["dr300_var_eur"]
dr300_risparmio_var = _F["dr300_risparmio_var"]
dr300_componenti = _F["dr300_componenti"]
dr300_verdetto = _F["dr300_verdetto"]

APP = Path(__file__).parent.parent / "app.py"

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
TITLE299 = "🧪⚡ Stress test: quanto perde il book negli scenari?"
TITLE298 = "🚦📏 Limite VaR: quanto margine resta?"

# sigma sintetiche: A=1000, B=500
SYN_SIG = [1000.0, 500.0]
SYN_RHO = 0.5

DEMO_TXT = """# book demo: nome;nozionale eur;vol % giornaliera
Gas TTF;2500000;3,2
Power DE;1800000;2,6
CO2 EUA;900000;2,1
Spark spread;1200000;4,0"""


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab300:
    def test_tab300_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 326
        assert TITLE300 in titoli
        assert "tab300" in dvars
        assert "tab300" in withs
        assert titoli[dvars.index("tab300")] == TITLE300
        assert titoli[-1] == TITLE326
        keys = re.findall(r'key="(st300_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_298_299_300(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab298")] == TITLE298
        assert titoli[dvars.index("tab299")] == TITLE299
        assert titoli[dvars.index("tab300")] == TITLE300


class TestDr300Num:
    def test_ok(self):
        assert dr300_num(2.5, "x") == 2.5

    def test_bool_ko(self):
        with pytest.raises(ValueError):
            dr300_num(True, "x")

    def test_nan_ko(self):
        with pytest.raises(ValueError):
            dr300_num(float("nan"), "x")

    def test_inf_ko(self):
        with pytest.raises(ValueError):
            dr300_num(float("inf"), "x")


class TestDr300ParseBook:
    def test_ok(self):
        p = dr300_parse_book("Gas;1000000;2,5\nPower;2000000;3")
        assert p == [("Gas", 1_000_000.0, 2.5), ("Power", 2_000_000.0, 3.0)]

    def test_commenti_e_vuote(self):
        p = dr300_parse_book("# cmt\n\n" + "\n".join(["X;100;1"] * 2))
        assert len(p) == 2

    def test_una_posizione_ko(self):
        with pytest.raises(ValueError):
            dr300_parse_book("Gas;1000000;2,5")

    def test_colonne_sbagliate_ko(self):
        with pytest.raises(ValueError):
            dr300_parse_book("Gas;1000000\nPower;2000000")

    def test_nozionale_ko(self):
        with pytest.raises(ValueError):
            dr300_parse_book("Gas;-5;2\nPower;2000000;2")

    def test_vol_negativa_ko(self):
        with pytest.raises(ValueError):
            dr300_parse_book("Gas;1000000;-2\nPower;2000000;2")

    def test_non_numerico_ko(self):
        with pytest.raises(ValueError):
            dr300_parse_book("Gas;xx;2\nPower;2000000;2")


class TestDr300Sigma:
    def test_sigma_euro(self):
        assert dr300_sigma_euro([("A", 1_000_000.0, 2.5),
                                 ("B", 500_000.0, 4.0)]) == [
            ("A", 25_000.0), ("B", 20_000.0)]

    def test_portafoglio_rho1(self):
        assert dr300_sigma_portafoglio(SYN_SIG, 1.0) == pytest.approx(1500.0)

    def test_portafoglio_rho0(self):
        assert dr300_sigma_portafoglio(SYN_SIG, 0.0) == pytest.approx(
            1118.033988749895)

    def test_portafoglio_rho05(self):
        assert dr300_sigma_portafoglio(SYN_SIG, SYN_RHO) == pytest.approx(
            1322.8756555322952)

    def test_rho_fuori_range_ko(self):
        with pytest.raises(ValueError):
            dr300_sigma_portafoglio(SYN_SIG, 1.5)
        with pytest.raises(ValueError):
            dr300_sigma_portafoglio(SYN_SIG, -0.1)

    def test_sigma_tutte_zero_ko(self):
        with pytest.raises(ValueError):
            dr300_sigma_portafoglio([0.0, 0.0], 0.5)


class TestDr300Rapporto:
    def test_rho1_uno(self):
        assert dr300_rapporto(SYN_SIG, 1.0) == pytest.approx(1.0)

    def test_sintetico(self):
        assert dr300_rapporto(SYN_SIG, SYN_RHO) == pytest.approx(1.1338934190276817)

    def test_maggiore_di_uno(self):
        assert dr300_rapporto(SYN_SIG, 0.0) > 1.0

    def test_beneficio(self):
        assert dr300_beneficio_pct(1.0) == pytest.approx(0.0)
        assert dr300_beneficio_pct(2.0) == pytest.approx(50.0)
        assert dr300_beneficio_pct(1.1338934190276817) == pytest.approx(11.808289631180314)

    def test_beneficio_ko(self):
        with pytest.raises(ValueError):
            dr300_beneficio_pct(0.9)


class TestDr300Var:
    def test_var95(self):
        assert dr300_var_eur(1000.0, 95) == pytest.approx(1644.8536269514722)

    def test_var99_maggiore(self):
        assert dr300_var_eur(1000.0, 99) > dr300_var_eur(1000.0, 95)

    def test_conf_ko(self):
        with pytest.raises(ValueError):
            dr300_var_eur(1000.0, 97)

    def test_risparmio(self):
        assert dr300_risparmio_var(SYN_SIG, SYN_RHO, 95) == pytest.approx(
            291.3436204191062)

    def test_risparmio_rho1_zero(self):
        assert dr300_risparmio_var(SYN_SIG, 1.0, 95) == pytest.approx(0.0)


class TestDr300Componenti:
    def test_pesi_sommano_dr(self):
        comp = dr300_componenti(["A", "B"], SYN_SIG, SYN_RHO)
        assert sum(p for _, _, p in comp) == pytest.approx(1.1338934190276817)

    def test_ordine_decrescente(self):
        comp = dr300_componenti(["A", "B"], SYN_SIG, SYN_RHO)
        assert comp[0][0] == "A"
        assert comp[0][2] > comp[1][2]

    def test_lunghezze_ko(self):
        with pytest.raises(ValueError):
            dr300_componenti(["A"], SYN_SIG, SYN_RHO)


class TestDr300Verdetto:
    def test_eccellente(self):
        assert dr300_verdetto(1.4).startswith("eccellente")
        assert dr300_verdetto(2.0).startswith("eccellente")

    def test_buona(self):
        assert dr300_verdetto(1.2).startswith("buona")
        assert dr300_verdetto(1.39).startswith("buona")

    def test_limitata(self):
        assert dr300_verdetto(1.05).startswith("limitata")
        assert dr300_verdetto(1.19).startswith("limitata")

    def test_nessuna(self):
        assert dr300_verdetto(1.0).startswith("nessuna")
        assert dr300_verdetto(1.049).startswith("nessuna")


class TestDr300Integrazione:
    def test_catena_demo(self):
        pos = dr300_parse_book(DEMO_TXT)
        assert len(pos) == 4
        sig = [s for _, s in dr300_sigma_euro(pos)]
        assert sig == pytest.approx([80000.0, 46800.0, 18900.0, 48000.0])
        sp = dr300_sigma_portafoglio(sig, 0.45)
        assert sp == pytest.approx(151895.22046463477)
        dr = dr300_rapporto(sig, 0.45)
        assert dr == pytest.approx(1.2752211650076146)
        ben = dr300_beneficio_pct(dr)
        assert ben == pytest.approx(21.582230013095117)
        risp = dr300_risparmio_var(sig, 0.45, 95)
        assert risp == pytest.approx(68762.74324265218)
        comp = dr300_componenti([n for n, _, _ in pos], sig, 0.45)
        assert comp[0][0] == 'Gas TTF'
        assert sum(p for _, _, p in comp) == pytest.approx(dr)
        assert dr300_verdetto(dr) == 'buona: diversificazione efficace del book'
