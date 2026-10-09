"""Test tab296 '🪓🛡 Component ES: chi contribuisce alla coda?': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab296. Allocazione di Eulero dell'ES:
CES_i = E[L_i | L_tot > VaR], somma_i CES_i = ES.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("ce296_num", "ce296_conf", "ce296_parse_matrice",
          "ce296_quantile", "ce296_componenti", "ce296_verdetto")
ce296_num = _F["ce296_num"]
ce296_conf = _F["ce296_conf"]
ce296_parse_matrice = _F["ce296_parse_matrice"]
ce296_quantile = _F["ce296_quantile"]
ce296_componenti = _F["ce296_componenti"]
ce296_verdetto = _F["ce296_verdetto"]

APP = Path(__file__).parent.parent / "app.py"

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
TITLE320 = "⚙️📉 GARCH(1,1): la volatilita' che ricorda"
TITLE321 = "🧪📉 Backtest VaR: il modello resiste al tempo?"
TITLE322 = "🎯📉 Convergenza forward: il forward indovina lo spot?"
TITLE323 = "🔄📉 Half-life di mean reversion: lo spot torna alla media?"
TITLE324 = "Ω📊 Omega ratio: oltre Sharpe e Sortino"
TITLE325 = "📈📉 Calmar ratio: il rendimento che paga il drawdown"
TITLE326 = "🩹 Pain index e Pain ratio: il dolore medio oltre il peggio"
TITLE327 = "🛟 Sterling ratio: il Calmar mediato sui peggiori drawdown"
TITLE328 = "🔻 Burke ratio: il drawdown penalizzato al quadrato"
TITLE329 = "🌊📉 CDaR: il drawdown medio oltre la soglia (il VaR dei drawdown)"
TITLE330 = "🔍📉 Martin ratio: il Calmar che guarda tutto il dolore"
TITLE331 = "⛵ Tempo di recupero: quanto resta sott'acqua l'equity"
TITLE332 = "🎯 Information ratio: la strategia batte davvero il benchmark?"
TITLE333 = "📊 Capture ratio: quanto cattura la strategia nei mercati su e giù?"
TITLE334 = "🎯 Hit rate: quanto spesso la strategia batte il benchmark?"
TITLE335 = "📏 Tracking error: quanto si discosta la strategia dal benchmark?"
TITLE336 = "📉 Max drawdown relativo: quanto si scende sotto il benchmark?"
TITLE295 = "🧪🛡 Backtest dell'ES: la coda e' sottostimata?"
TITLE294 = "🧪📉 Backtest del VaR: il modello tiene?"

# matrice sintetica 20x2 a valori noti: A=[100]*5+[0]*15, B=[50]*5+[0]*15
SYN_MATRICE = [[100.0, 50.0]] * 5 + [[0.0, 0.0]] * 15

DEMO_TXT = """88,66;-126,32;-68,09
-144,61;527,22;539,76
148,57;-134,88;74,99
722,39;-148,75;-149,99
-96,02;-97,44;89,49
1674,31;-60,09;638,81
70,4;-96,72;134,4
-137,05;663,18;-144,07
621,44;451,64;-148,11
-145,41;-100,42;152,36
2504,37;154,86;-131,85
-135,66;473,31;126,38
-148,49;-140,71;-120,04
-149,79;-70,31;-7,06
146,15;-149,13;-110,02
1145,85;42,18;-76,79
-126,57;-67,55;732,16
-147,98;-13,51;-79,43
79,45;-124,92;1715,81
321,97;-148,72;-149,68
-54,55;-121,78;-78,18
-131,57;494,93;-149,84
-149,88;-134,73;-124,72
538,52;643,16;933,61
-81,8;-102,37;-101,25
-149,97;-148,77;69,25
-81,25;-129,89;269,72
130,37;440,08;366,81
-135,35;-149,92;2644,91
-115,64;667,79;-109,58
-137,47;334,22;-117,0
-146,6;-110,21;-142,05
-104,15;521,38;-115,29
286,64;-149,99;-58,32
-150,0;-90,23;-111,37
-145,6;266,98;144,33
-105,25;-15,57;-148,86
-108,49;-141,35;-143,56
330,32;-149,5;16,01
25,11;-149,66;521,29
-149,84;464,71;187,2
-47,73;-86,08;-98,97
-149,72;-48,82;-123,74
181,61;-53,74;348,51
564,28;-139,33;153,81
-149,94;52,52;-141,82
344,07;-112,8;559,82
-137,48;-51,73;80,06"""


def _demo_matrice():
    righe = []
    for ln in DEMO_TXT.split("\n"):
        s = ln.strip()
        if not s:
            continue
        righe.append([float(c.replace(",", ".")) for c in s.split(";")])
    return righe


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab296:
    def test_tab296_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 336
        assert TITLE296 in titoli
        assert "tab296" in dvars
        assert "tab296" in withs
        assert titoli[dvars.index("tab296")] == TITLE296
        assert titoli[-1] == TITLE336
        keys = re.findall(r'key="(ce296_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_294_295_296(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab294")] == TITLE294
        assert titoli[dvars.index("tab295")] == TITLE295
        assert titoli[dvars.index("tab296")] == TITLE296


class TestCe296Validatori:
    def test_num_ok(self):
        assert ce296_num(2.5, "x") == 2.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            ce296_num(True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            ce296_num(float("nan"), "x")

    def test_conf_ok(self):
        assert ce296_conf(0.975) == 0.975

    def test_conf_bordi_ko(self):
        with pytest.raises(ValueError):
            ce296_conf(1.0)
        with pytest.raises(ValueError):
            ce296_conf(0.0)


class TestCe296Parse:
    def test_ok(self):
        t = "# cmt\n\n" + "\n".join(["1,5;2"] * 20)
        m = ce296_parse_matrice(t)
        assert len(m) == 20 and len(m[0]) == 2
        assert m[0][0] == pytest.approx(1.5)

    def test_una_colonna_ko(self):
        with pytest.raises(ValueError):
            ce296_parse_matrice("\n".join(["1"] * 20))

    def test_troppo_poche_righe_ko(self):
        with pytest.raises(ValueError):
            ce296_parse_matrice("\n".join(["1;2"] * 19))

    def test_righe_disallineate_ko(self):
        with pytest.raises(ValueError):
            ce296_parse_matrice("\n".join(["1;2"] * 19 + ["1;2;3"]))

    def test_non_numerico_ko(self):
        with pytest.raises(ValueError):
            ce296_parse_matrice("\n".join(["1;2"] * 19 + ["1;xx"]))


class TestCe296Quantile:
    def test_mediana(self):
        assert ce296_quantile([3.0, 1.0, 2.0], 0.5) == pytest.approx(2.0)

    def test_interpolazione(self):
        # type-7: pos = 0.25*3 = 0.75 -> 1 + 3*0.75 = 3.25
        assert ce296_quantile([1.0, 2.0, 3.0, 4.0], 0.25) == pytest.approx(1.75)

    def test_bordi(self):
        assert ce296_quantile([5.0, 6.0], 0.0) == pytest.approx(5.0)
        assert ce296_quantile([5.0, 6.0], 1.0) == pytest.approx(6.0)

    def test_singolo(self):
        assert ce296_quantile([7.0], 0.9) == pytest.approx(7.0)

    def test_q_fuori_range_ko(self):
        with pytest.raises(ValueError):
            ce296_quantile([1.0, 2.0], 1.5)

    def test_vuota_ko(self):
        with pytest.raises(ValueError):
            ce296_quantile([], 0.5)


class TestCe296Componenti:
    def test_sintetico_valori_noti(self):
        # totali = [150]*5 + [0]*15, conf 0.75 -> VaR = 37.5, 5 superamenti
        r = ce296_componenti(SYN_MATRICE, 0.75)
        assert r["n"] == 20
        assert r["m"] == 2
        assert r["var"] == pytest.approx(37.5)
        assert r["superamenti"] == 5
        assert r["es"] == pytest.approx(150.0)
        assert r["componenti"][0] == pytest.approx(100.0)
        assert r["componenti"][1] == pytest.approx(50.0)
        assert sum(r["componenti"]) == pytest.approx(r["es"])
        assert r["quote"][0] == pytest.approx(0.6666666666666666)
        assert r["standalone"][0] == pytest.approx(100.0)
        assert r["standalone"][1] == pytest.approx(50.0)
        assert r["diversificazione"] == pytest.approx(0.0)

    def test_nessun_superamento_ko(self):
        with pytest.raises(ValueError):
            ce296_componenti([[1.0, 1.0]] * 20, 0.999)

    def test_righe_disallineate_ko(self):
        with pytest.raises(ValueError):
            ce296_componenti([[1.0, 2.0], [1.0]], 0.9)

    def test_conf_ko(self):
        with pytest.raises(ValueError):
            ce296_componenti(SYN_MATRICE, 1.0)


class TestCe296Verdetto:
    def test_diversificata(self):
        assert ce296_verdetto(0.3) == "coda diversificata: nessuna posizione domina"

    def test_elevata(self):
        assert ce296_verdetto(0.6).startswith("concentrazione elevata")

    def test_critica(self):
        assert ce296_verdetto(0.8).startswith("concentrazione critica")

    def test_soglie(self):
        assert ce296_verdetto(0.5).startswith("concentrazione elevata")
        assert ce296_verdetto(0.7).startswith("concentrazione critica")

    def test_fuori_range_ko(self):
        with pytest.raises(ValueError):
            ce296_verdetto(1.2)


class TestCe296Integrazione:
    def test_catena_demo(self):
        m = _demo_matrice()
        assert len(m) == 48
        assert len(m[0]) == 3
        r = ce296_componenti(m, 0.975)
        assert r["n"] == 48
        assert r["superamenti"] == 2
        assert r["var"] == pytest.approx(2340.9832499999993)
        assert r["es"] == pytest.approx(2443.51)
        assert sum(r["componenti"]) == pytest.approx(r["es"])
        assert r["componenti"][0] == pytest.approx(1184.51)
        assert max(r["quote"]) == pytest.approx(0.5142315767072776)
        assert ce296_verdetto(max(r["quote"])) == 'concentrazione elevata: la coda dipende da poche posizioni'
        # parse round-trip della demo come appare nella UI
        m2 = ce296_parse_matrice(DEMO_TXT)
        assert len(m2) == 48
