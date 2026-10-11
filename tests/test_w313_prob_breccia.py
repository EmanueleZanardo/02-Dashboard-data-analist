"""Test tab313 '📉💥 VaR rotto: la probabilita' di breccia con code grasse': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab di rischio precedenti, piu' la matematica della probabilita' di
breccia del VaR con code grasse: inversione della CDF corretta di
Cornish-Fisher per bisezione, neutralita' a momenti nulli, rapporto
p_vera/p_nom, breacce attese/anno, semaforo Basilea, verdetto a 5 stati.
"""
import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("be313_num", "be313_conf", "be313_corr", "be313_skew",
           "be313_kurt", "be313_giorni", "be313_parse_book",
           "be313_norm_ppf", "be313_norm_cdf", "be313_zcf", "be313_pesi",
           "be313_sigmas", "be313_cdf_cf", "be313_prob_breccia",
           "be313_risultato", "be313_verdetto")

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
TITLE337 = "📐 Treynor & Jensen: il premio per unita' di rischio sistematico"
TITLE338 = "⚖️ M² Modigliani: il rendimento a parita' di rischio col benchmark"
TITLE339 = "📉 Sortino ratio: il rendimento per unità di rischio al ribasso"
TITLE340 = "📉 Calmar ratio: il rendimento annuo per unità di max drawdown"
TITLE341 = "📐 K-ratio: la regolarità della crescita dell'equity"
TITLE342 = "🎯 Volatilità target: il sizing a volatilità costante"
TITLE343 = "📐 Kelly criterion: il sizing ottimale dall'edge stimato"
TITLE344 = "🎲 Risk of ruin: probabilita' di toccare una barriera di drawdown"
TITLE345 = "🎯 Sizing anti-rovina: f massima con ROR vincolato"
TITLE346 = "📊 Monte Carlo: distribuzione del capitale dopo N trade"
TITLE347 = "VaR & Expected Shortfall del P&L dopo N trade"
TITLE348 = "Kelly con costi di trading: sizing netto"
TITLE349 = "Frazione di Kelly: half-Kelly e trade-off crescita/volatilità"
TITLE350 = "Kelly robusto: sizing con edge incerta"
TITLE351 = "Kelly con portafoglio: due posizioni simultanee"
TITLE352 = "Kelly con correlazione: due posizioni correlate"
TITLE353 = "Kelly adattivo: win-rate rolling e size dinamica"
TITLE354 = "Kelly con controllo drawdown: sizing frazionato al drawdown"
TITLE355 = "Kelly con target di volatilità: sizing riscalato sulla vol"
TITLE356 = "Kelly bayesiano: sizing con win-rate posterior"
TITLE357 = "Kelly con lotti interi: sizing discreto e drag di arrotondamento"
TITLE358 = "Kelly con stop-loss: sizing con perdita troncata"
TITLE359 = "Kelly con take-profit: sizing con vincita troncata"
TITLE360 = "Kelly frazionario (fractional Kelly): λ·f*"
TITLE361 = "Rischio di rovina (risk of ruin): probabilita' di rovina prima del target"
TITLE362 = "Kelly con tre esiti: sizing con vincita, perdita parziale e perdita piena"
TITLE363 = "Kelly con limite di posizione: sizing con cap f_max"
TITLE364 = "Kelly con vincoli multipli: cap, lotti, stop e drawdown"
TITLE365 = "Kelly con incertezza: haircut bayesiano sulla p stimata"
TITLE366 = "Kelly su N trade: raddoppio, dimezzamento e crescita attesa"
TITLE367 = "Kelly: mappa di sensibilità f* e crescita su (p, b)"
TITLE368 = "Kelly su ritorni continui: f* = μ/σ² e volatility drag"
TITLE369 = "Kelly con costi di transazione: f* netto = (μ-c)/σ²"
TITLE370 = "Kelly e drawdown: probabilità di toccare un max drawdown"
TITLE371 = "Kelly frazionario: frazione ottima per un budget di volatilità"
TITLE372 = "Monte Carlo: VaR e Expected Shortfall di una posizione power"
TITLE312 = "📐🌊 Expected Shortfall con Cornish-Fisher: la coda oltre il VaR con code grasse"
TITLE311 = "📐📉 Cornish-Fisher: il VaR corretto per skew e code grasse"
BOOK_DEMO = ("Cal-28 Baseload power;2500000;18,5;-0,8;4,0;power\n"
             "Q3-28 Peak power;1200000;26,0;-1,2;6,0;power\n"
             "TTF Gas Cal-28;1800000;22,0;-0,5;3,0;gas\n"
             "EUA Carbon Dec-28;700000;31,0;-0,3;2,0;carbon")
RHO_DEMO = 0.35
CONF_DEMO = 99
GIORNI_DEMO = 250
SOGLIA_DEMO = 3.0

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
VAR = 2336394.1500722347
VAR_VERITIERO = 3583686.0773059446
VAR_GAP_EUR = 1247291.92723371
VAR_GAP_PCT = 0.5338533856520515
P_NOM = 0.010000000000000009
P_VERA = 0.029163111139973275
RATIO = 2.916311113997325
ATTESE_NOM = 2.500000000000002
ATTESE_VERE = 7.290777784993319
Z = 2.326347874040838
ZCF = 3.5682765628019917
SKEW = -0.7338709677419355
KURT = 3.870967741935484
ZONA = "gialla (5-9 breacce attese)"
STATO = "breacce materiali"
VERDETTO = 'breacce materiali (x2.9): 7.3 superamenti attesi/anno contro 2.5 nominali: valutare un add-on di 1,247,292 euro al limite'


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistry313:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 372
        assert TITLE313 in titoli
        assert "tab313" in dvars
        assert "    with tab313:" in src

    def test_titoli_allineati_311_312_313(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab311")] == TITLE311
        assert titoli[dvars.index("tab312")] == TITLE312
        assert titoli[dvars.index("tab313")] == TITLE313

    def test_ultima_tab(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[-1] == TITLE372
        assert dvars[-1] == "tab372"


class TestValidatori:
    def test_conf_ok(self):
        assert _F["be313_conf"](99) == 99

    def test_conf_ko(self):
        with pytest.raises(ValueError):
            _F["be313_conf"](97)

    def test_skew_ok(self):
        assert _F["be313_skew"](-5.0) == -5.0
        assert _F["be313_skew"](5.0) == 5.0

    def test_skew_fuori_range(self):
        with pytest.raises(ValueError):
            _F["be313_skew"](5.1)
        with pytest.raises(ValueError):
            _F["be313_skew"](-5.1)

    def test_kurt_ok(self):
        assert _F["be313_kurt"](30.0) == 30.0
        assert _F["be313_kurt"](-1.5) == -1.5

    def test_kurt_fuori_range(self):
        with pytest.raises(ValueError):
            _F["be313_kurt"](30.1)
        with pytest.raises(ValueError):
            _F["be313_kurt"](-1.6)

    def test_giorni_ok(self):
        assert _F["be313_giorni"](250) == 250
        assert _F["be313_giorni"](250.0) == 250

    def test_giorni_ko(self):
        with pytest.raises(ValueError):
            _F["be313_giorni"](4)
        with pytest.raises(ValueError):
            _F["be313_giorni"](501)
        with pytest.raises(ValueError):
            _F["be313_giorni"](250.5)
        with pytest.raises(ValueError):
            _F["be313_giorni"](True)

    def test_corr_ko(self):
        with pytest.raises(ValueError):
            _F["be313_corr"](1.1)

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["be313_num"](True, "x")

    def test_parse_book_ok(self):
        book = _F["be313_parse_book"](BOOK_DEMO)
        assert len(book) == 4
        assert book[0] == ("Cal-28 Baseload power", 2500000.0, 0.185,
                           -0.8, 4.0, "power")

    def test_parse_book_5campi_ko(self):
        with pytest.raises(ValueError):
            _F["be313_parse_book"]("nome;1000;20,0;-0,5;2,0")

    def test_parse_book_skew_testo_ko(self):
        with pytest.raises(ValueError):
            _F["be313_parse_book"]("nome;1000;20,0;alta;2,0;power")

    def test_parse_book_vuoto_ko(self):
        with pytest.raises(ValueError):
            _F["be313_parse_book"]("   \n  ")


class TestMatematica:
    def test_ppf_99(self):
        assert abs(_F["be313_norm_ppf"](0.99) - 2.32634787404084) < 1e-3

    def test_cdf_inversa_ppf(self):
        for q in (0.90, 0.95, 0.99):
            assert _F["be313_norm_cdf"](_F["be313_norm_ppf"](q)) == \
                pytest.approx(q, rel=1e-6)

    def test_cdf_0(self):
        assert _F["be313_norm_cdf"](0.0) == pytest.approx(0.5)

    def test_zcf_neutro(self):
        z = 1.6448536269514722
        assert _F["be313_zcf"](z, 0.0, 0.0) == pytest.approx(z)

    def test_zcf_skew_neg_aumenta(self):
        # skew rendimenti negativa = coda perdite grassa -> quantile sale
        z = 1.6448536269514722
        assert _F["be313_zcf"](z, -1.0, 0.0) > z

    def test_cdf_cf_neutra(self):
        # a momenti nulli la CDF corretta ridiventa quella normale
        for z in (-2.0, -0.5, 0.0, 1.0, 2.326):
            assert _F["be313_cdf_cf"](z, 0.0, 0.0) == pytest.approx(
                _F["be313_norm_cdf"](z), rel=1e-6)

    def test_prob_breccia_neutra(self):
        # senza correzione la breccia vera e' quella nominale
        p = 0.99
        z = _F["be313_norm_ppf"](p)
        assert _F["be313_prob_breccia"](0.0, 0.0, z) == pytest.approx(
            1.0 - p, rel=1e-4)

    def test_prob_breccia_code_grasse(self):
        # skew negativa / curtosi alta -> piu' buchi del nominale
        p = 0.99
        z = _F["be313_norm_ppf"](p)
        assert _F["be313_prob_breccia"](-1.0, 4.0, z) > 1.0 - p

    def test_prob_breccia_clamp(self):
        assert 0.0 <= _F["be313_prob_breccia"](-5.0, 30.0, 0.0) <= 1.0

    def test_risultato_coerente(self):
        book = _F["be313_parse_book"](BOOK_DEMO)
        ris = _F["be313_risultato"](book, RHO_DEMO, CONF_DEMO, GIORNI_DEMO)
        assert ris["p_nom"] == pytest.approx(1.0 - CONF_DEMO / 100.0)
        assert ris["p_vera"] == pytest.approx(
            _F["be313_prob_breccia"](ris["skew"], ris["kurt"], ris["z"]),
            rel=1e-12)
        assert ris["ratio"] == pytest.approx(ris["p_vera"] / ris["p_nom"])
        assert ris["attese_nom"] == pytest.approx(GIORNI_DEMO * ris["p_nom"])
        assert ris["attese_vere"] == pytest.approx(GIORNI_DEMO * ris["p_vera"])
        assert ris["var_veritiero"] - ris["var"] == pytest.approx(
            ris["var_gap_eur"])
        assert ris["var_gap_pct"] == pytest.approx(
            ris["var_gap_eur"] / ris["var"])
        assert len(ris["dettaglio"]) == 4

    def test_dettaglio_standalone(self):
        book = _F["be313_parse_book"](BOOK_DEMO)
        ris = _F["be313_risultato"](book, RHO_DEMO, CONF_DEMO, GIORNI_DEMO)
        z = _F["be313_norm_ppf"](CONF_DEMO / 100.0)
        for (n, seg, vp, pv, av), (_, noz, vol, sk, ku, _) in zip(
                ris["dettaglio"], book):
            assert vp == pytest.approx(z * noz * vol, rel=1e-12)
            assert pv == pytest.approx(_F["be313_prob_breccia"](sk, ku, z),
                                       rel=1e-12)
            assert av == pytest.approx(GIORNI_DEMO * pv)
            assert 0.0 <= pv <= 1.0

    def test_zona_basilea(self):
        book = _F["be313_parse_book"](BOOK_DEMO)
        ris = _F["be313_risultato"](book, RHO_DEMO, 99, GIORNI_DEMO)
        if ris["attese_vere"] < 5.0:
            assert ris["zona"].startswith("verde")
        elif ris["attese_vere"] < 10.0:
            assert ris["zona"].startswith("gialla")
        else:
            assert ris["zona"].startswith("rossa")

    def test_zona_nd_senza_99(self):
        book = _F["be313_parse_book"](BOOK_DEMO)
        ris = _F["be313_risultato"](book, RHO_DEMO, 95, GIORNI_DEMO)
        assert ris["zona"].startswith("n.d.")

    def test_demo(self):
        book = _F["be313_parse_book"](BOOK_DEMO)
        ris = _F["be313_risultato"](book, RHO_DEMO, CONF_DEMO, GIORNI_DEMO)
        assert ris["var"] == pytest.approx(VAR, rel=1e-9)
        assert ris["var_veritiero"] == pytest.approx(VAR_VERITIERO, rel=1e-9)
        assert ris["var_gap_eur"] == pytest.approx(VAR_GAP_EUR, rel=1e-9)
        assert ris["var_gap_pct"] == pytest.approx(VAR_GAP_PCT, rel=1e-9)
        assert ris["p_nom"] == pytest.approx(P_NOM, rel=1e-9)
        assert ris["p_vera"] == pytest.approx(P_VERA, rel=1e-9)
        assert ris["ratio"] == pytest.approx(RATIO, rel=1e-9)
        assert ris["attese_nom"] == pytest.approx(ATTESE_NOM, rel=1e-9)
        assert ris["attese_vere"] == pytest.approx(ATTESE_VERE, rel=1e-9)
        assert ris["z"] == pytest.approx(Z, rel=1e-9)
        assert ris["zcf"] == pytest.approx(ZCF, rel=1e-9)
        assert ris["skew"] == pytest.approx(SKEW, rel=1e-9)
        assert ris["kurt"] == pytest.approx(KURT, rel=1e-9)
        assert ris["zona"] == ZONA
        assert ris["p_vera"] > ris["p_nom"]
        assert ris["ratio"] >= SOGLIA_DEMO / 2.0


def _ris(ratio=4.0, att_vere=10.0, att_nom=2.5,
         var_ver=3000000.0, gap_eur=800000.0, gap_pct=0.36):
    return {"ratio": ratio, "attese_vere": att_vere, "attese_nom": att_nom,
            "var_veritiero": var_ver, "var_gap_eur": gap_eur,
            "var_gap_pct": gap_pct}


class TestVerdetto:
    def test_severa(self):
        assert _F["be313_verdetto"](
            _ris(ratio=10.0), SOGLIA_DEMO).startswith("breacce severe")

    def test_materiale(self):
        # soglia 3.0 -> materiale da ratio >= 2.0
        assert _F["be313_verdetto"](
            _ris(ratio=2.5), SOGLIA_DEMO).startswith("breacce materiali")

    def test_moderata(self):
        assert _F["be313_verdetto"](
            _ris(ratio=1.4), SOGLIA_DEMO).startswith("breacce moderate")

    def test_in_linea(self):
        assert _F["be313_verdetto"](
            _ris(ratio=1.0), SOGLIA_DEMO).startswith("in linea")

    def test_prudente(self):
        assert _F["be313_verdetto"](
            _ris(ratio=0.5), SOGLIA_DEMO).startswith("VaR prudente")

    def test_verdetto_demo(self):
        assert VERDETTO.startswith(STATO)

    def test_soglia_ko(self):
        with pytest.raises(ValueError):
            _F["be313_verdetto"](_ris(), 1.9)
        with pytest.raises(ValueError):
            _F["be313_verdetto"](_ris(), 10.1)
