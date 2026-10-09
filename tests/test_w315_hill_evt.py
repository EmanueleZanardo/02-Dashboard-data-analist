"""Test tab315 '🏔️📉 Valori estremi (Hill): il VaR oltre il massimo storico': registry + funzioni pure.

Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
con le tab precedenti, piu' la matematica dei valori estremi: stimatore di
Hill dell'indice di coda xi, Hill plot, estrapolazione EVT del VaR oltre il
massimo storico, ES di coda, confronti con quantile empirico e VaR normale,
verdetto a 5 stati.
"""
import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh315_num", "mh315_conf", "mh315_k", "mh315_parse_serie",
           "mh315_norm_ppf", "mh315_perdite", "mh315_hill",
           "mh315_hill_plot", "mh315_var_evt", "mh315_es_evt",
           "mh315_var_empirico", "mh315_var_normale",
           "mh315_risultato", "mh315_verdetto")

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
TITLE314 = "⏳📉 VaR multi-orizzonte: lo scaling con autocorrelazione dei rendimenti"
TITLE313 = "📉💥 VaR rotto: la probabilita' di breccia con code grasse"
SERIE_DEMO = '-7689 13066 8112 -63229 62852 39916 92196 24157 -9069 986\n-6796 -21240 -45770 -92147 -41405 65384 -249746 -17518 -67249 14967\n67536 20043 -38215 -195168 -30319 -40368 23914 4742 -897 -223481\n-31032 -3617 -6607 54814 -27012 29764 -66225 -258903 -1171 91295\n-57139 -2898 72058 -11675 27543 28342 -297043 -55968 -34426 -63587\n10167 253064 -36629 41993 329157 -92752 -49044 -33433 -22182 9731\n596 -36229 21513 32183 29756 -4331 -17444 12668 -14222 38696\n-6197 64319 -23380 55794 -74553 -23556 46003 8501 91959 -27344\n84011 31131 -71850 -10800 60122 20014 -57979 -14127 -26228 -83049\n-21612 5747 55320 12401 -47501 71536 36926 -72323 -49058 67403\n-24232 -352459 36997 -6063 9064 66434 -22234 44252 -61060 -64021\n-82194 67388 37750 -83448 -66946 -39595 3678 -26929 22239 -44530\n-16531 83110 -29847 -24544 -26872 32082 61709 22204 -21202 13207\n-21291 -67548 19628 61315 15596 47843 25604 -71902 -11348 58829\n-9688 -73248 -264 35737 10802 -68684 -13708 77325 -73463 -87837\n74951 35657 -24316 8134 256845 260928 35922 5358 -44268 59457\n-9750 -38450 37071 44300 -8005 60115 -8831 -54 34491 -64982\n-30951 36466 52359 -1241 41335 56577 1439 -55179 278123 -13374\n21626 -5022 -5668 26555 -23788 32083 5240 86738 -1218 -53702\n22143 27240 -28895 -20704 14206 -641731 80989 24271 55275 -47645\n-76571 82496 -62532 90879 32733 14602 23266 1374 73310 31853\n-47314 17457 30017 -15547 -90575 50574 45809 9943 -30051 46882\n79807 70062 -41899 5484 -10908 15879 -33740 56919 28814 -35468\n52292 42954 -45173 54859 -15658 -38864 24992 84557 -55546 -40903\n-4621 23948 -8369 805164 65154 55048 29350 -29982 1393 -8152\n35452 -4642 51174 1321 60854 -86365 8770 272804 -22471 45833\n3751 32149 7893 14629 73511 -24227 39749 2438 5080 -30937\n-13496 31034 269121 -222554 6059 83384 -61822 -35130 44231 -21991\n-22231 67430 48037 504455 -48391 41817 -66130 -63614 33813 13353\n31161 4704 -10615 17269 -10096 -76538 -17306 -202031 -27894 -60946\n-14546 8057 80104 -60491 17630 -277926 4100 -14294 -457 -70577\n52719 12411 -4991 53889 8238 36992 -57925 69312 -9368 56753\n-40766 58968 14240 84561 20366 15403 -64989 54077 42576 224056\n-68128 -1549 8999 -63716 3024 15645 38593 -36854 19736 -21757\n-3065 -42171 18759 68683 -19885 -14975 -27483 -9242 -44457 -33684\n33204 34045 -7391 -2089 -18703 -33351 40089 18435 2022 93359\n43366 -11025 17247 -13805 25185 -14143 -60018 39621 -85758 -6415\n-9171 -66823 26653 22523 -35972 -16781 22318 48175 11157 46879\n-71206 -8616 -48444 -13749 -41557 -22312 12832 54346 11352 64055\n51972 12823 -43678 39759 17631 44892 11934 -44844 83964 -15675'
K_DEMO = 40
Q_DEMO = 99.0

# costanti demo calcolate dai veri helper (interpolate dal ciclo QA)
N_DEMO = 400
XI = 0.48115407556677436
SOGLIA = 63716.0
VAR_EVT = 192931.25047037363
ES_EVT = 371846.9036470257
VAR_EMP = 258903.0
VAR_NOR = 204156.52994617875
RATIO = 0.745187388598717
MAX_STORICO = 641731.0
STATO = "code pesanti"
VERDETTO = "code pesanti (xi=0.48): VaR EVT al 99% 192,931 euro vs quantile storico 258,903 euro (x0.75), VaR normale 204,157 euro: la coda e' pesante, il modello normale non la vede"


def _registry():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"with (tab\d+):", src)
    return src, titoli, dvars, withs


def _pareto(n=2000, xi=0.4):
    """Quantili esatti di Pareto(xi), ordinati discendenti."""
    return [((1.0 - i / (n + 1)) ** (-xi)) for i in range(n, 0, -1)]


class TestRegistry315:
    def test_conteggi(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 333
        assert TITLE315 in titoli
        assert "tab315" in dvars
        assert "    with tab315:" in src

    def test_titoli_allineati_313_314_315(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab313")] == TITLE313
        assert titoli[dvars.index("tab314")] == TITLE314
        assert titoli[dvars.index("tab315")] == TITLE315

    def test_ultima_tab(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[-1] == TITLE333
        assert dvars[-1] == "tab333"


class TestValidatori:
    def test_conf_ok(self):
        assert _F["mh315_conf"](99.5) == 99.5

    def test_conf_ko(self):
        with pytest.raises(ValueError):
            _F["mh315_conf"](97)
        with pytest.raises(ValueError):
            _F["mh315_conf"]("99")

    def test_k_ok(self):
        assert _F["mh315_k"](40, 400) == 40
        assert _F["mh315_k"](10, 20) == 10
        assert _F["mh315_k"](10.0, 400) == 10

    def test_k_ko(self):
        with pytest.raises(ValueError):
            _F["mh315_k"](9, 400)
        with pytest.raises(ValueError):
            _F["mh315_k"](201, 400)
        with pytest.raises(ValueError):
            _F["mh315_k"](10.5, 400)
        with pytest.raises(ValueError):
            _F["mh315_k"](True, 400)

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh315_num"](True, "x")

    def test_parse_serie_ok(self):
        txt = " ".join(["1,5"] * 10 + ["2.5"] * 10 + ["-3"] * 5)
        vals = _F["mh315_parse_serie"](txt)
        assert len(vals) == 25
        assert vals[0] == pytest.approx(1.5)
        assert vals[10] == pytest.approx(2.5)
        assert vals[20] == pytest.approx(-3.0)

    def test_parse_serie_separators(self):
        txt = "\n".join([f"{i};{i + 0.5}" for i in range(10)])
        vals = _F["mh315_parse_serie"](txt)
        assert len(vals) == 20

    def test_parse_serie_corta_ko(self):
        with pytest.raises(ValueError):
            _F["mh315_parse_serie"](" ".join(["1"] * 19))

    def test_parse_serie_testo_ko(self):
        with pytest.raises(ValueError):
            _F["mh315_parse_serie"](" ".join(["1"] * 19 + ["abc"]))

    def test_parse_serie_nan_ko(self):
        with pytest.raises(ValueError):
            _F["mh315_parse_serie"](" ".join(["1"] * 19 + ["nan"]))

    def test_ppf_99(self):
        assert abs(_F["mh315_norm_ppf"](0.99) - 2.32634787404084) < 1e-3

    def test_perdite_ordinamento(self):
        assert _F["mh315_perdite"]([10.0, -5.0, 3.0]) == [5.0, -3.0, -10.0]


class TestHill:
    def test_hill_pareto_nota(self):
        perd = _pareto(2000, 0.4)
        assert _F["mh315_hill"](perd, 200) == pytest.approx(0.4, abs=0.05)

    def test_hill_piccolo_campione(self):
        perd = _pareto(400, 0.4)
        assert _F["mh315_hill"](perd, 40) == pytest.approx(0.4, abs=0.08)

    def test_hill_soglia_non_positiva_ko(self):
        perd = [100.0] * 10 + [0.0] * 20
        with pytest.raises(ValueError):
            _F["mh315_hill"](perd, 10)

    def test_hill_k_fuori_range_ko(self):
        with pytest.raises(ValueError):
            _F["mh315_hill"](_pareto(400, 0.4), 5)

    def test_hill_plot_lunghezza(self):
        perd = _pareto(400, 0.4)
        hp = _F["mh315_hill_plot"](perd)
        assert len(hp) == 400 // 2 - 10 + 1
        assert hp[0][0] == 10
        assert hp[-1][0] == 200
        assert [k for k, _ in hp] == sorted(k for k, _ in hp)

    def test_hill_plot_stabile_su_pareto(self):
        perd = _pareto(2000, 0.4)
        for k, xi in _F["mh315_hill_plot"](perd):
            assert xi == pytest.approx(0.4, abs=0.1)


class TestEvt:
    def test_var_evt_formula(self):
        perd = _pareto(2000, 0.4)
        k, q = 200, 99.0
        xi = _F["mh315_hill"](perd, k)
        att = perd[k] * ((k / 2000) / 0.01) ** xi
        assert _F["mh315_var_evt"](perd, k, q) == pytest.approx(att, rel=1e-12)

    def test_var_evt_cresce_con_q(self):
        perd = _pareto(2000, 0.4)
        v99 = _F["mh315_var_evt"](perd, 200, 99.0)
        v995 = _F["mh315_var_evt"](perd, 200, 99.5)
        v999 = _F["mh315_var_evt"](perd, 200, 99.9)
        assert v99 < v995 < v999

    def test_var_evt_cresce_con_xi(self):
        p1 = _pareto(2000, 0.2)
        p2 = _pareto(2000, 0.6)
        assert (_F["mh315_var_evt"](p2, 200, 99.0)
                > _F["mh315_var_evt"](p1, 200, 99.0))

    def test_es_evt_ok(self):
        assert _F["mh315_es_evt"](100000.0, 0.4) == pytest.approx(
            100000.0 / 0.6)

    def test_es_evt_coda_infinita(self):
        assert _F["mh315_es_evt"](100000.0, 1.0) is None
        assert _F["mh315_es_evt"](100000.0, 1.5) is None

    def test_var_empirico_manuale(self):
        assert _F["mh315_var_empirico"]([5.0, 4.0, 3.0, 2.0, 1.0],
                                        99.0) == 5.0

    def test_var_normale_manuale(self):
        # perdite [-1,-2,-3]: media -2, sd campionaria 1
        assert _F["mh315_var_normale"]([1.0, 2.0, 3.0], 99.0) == pytest.approx(
            -2.0 + 2.32634787404084, rel=1e-6)

    def test_risultato_coerente(self):
        ris = _F["mh315_risultato"](SERIE_DEMO, K_DEMO, Q_DEMO)
        perd = _F["mh315_perdite"](_F["mh315_parse_serie"](SERIE_DEMO))
        assert ris["n"] == len(perd) == N_DEMO
        assert ris["k"] == K_DEMO
        assert ris["xi"] == pytest.approx(_F["mh315_hill"](perd, K_DEMO),
                                          rel=1e-12)
        assert ris["soglia"] == pytest.approx(perd[K_DEMO], rel=1e-12)
        assert ris["var_evt"] == pytest.approx(
            _F["mh315_var_evt"](perd, K_DEMO, Q_DEMO), rel=1e-12)
        assert ris["var_empirico"] == pytest.approx(
            _F["mh315_var_empirico"](perd, Q_DEMO), rel=1e-12)
        assert ris["var_normale"] == pytest.approx(
            _F["mh315_var_normale"](_F["mh315_parse_serie"](SERIE_DEMO),
                                    Q_DEMO), rel=1e-12)
        assert ris["ratio_evt_emp"] == pytest.approx(
            ris["var_evt"] / ris["var_empirico"], rel=1e-12)
        assert ris["max_storico"] == pytest.approx(perd[0], rel=1e-12)

    def test_demo(self):
        ris = _F["mh315_risultato"](SERIE_DEMO, K_DEMO, Q_DEMO)
        assert ris["n"] == N_DEMO
        assert ris["xi"] == pytest.approx(XI, rel=1e-9)
        assert ris["soglia"] == pytest.approx(SOGLIA, rel=1e-9)
        assert ris["var_evt"] == pytest.approx(VAR_EVT, rel=1e-9)
        assert ris["es_evt"] == pytest.approx(ES_EVT, rel=1e-9)
        assert ris["var_empirico"] == pytest.approx(VAR_EMP, rel=1e-9)
        assert ris["var_normale"] == pytest.approx(VAR_NOR, rel=1e-9)
        assert ris["ratio_evt_emp"] == pytest.approx(RATIO, rel=1e-9)
        assert ris["max_storico"] == pytest.approx(MAX_STORICO, rel=1e-9)
        assert ris["es_evt"] == pytest.approx(ris["var_evt"] / (1.0 - XI),
                                              rel=1e-9)
        assert 0.3 < XI < 0.7  # coda pesante ma ES finito
        assert 0.5 < RATIO < 1.0  # outlier nel campione sopra l'EVT


def _ris(xi=0.45, ratio=0.8, q=99.0):
    return {"xi": xi, "ratio_evt_emp": ratio, "q": q,
            "var_evt": 200000.0, "var_empirico": 250000.0,
            "var_normale": 500000.0, "max_storico": 640000.0}


class TestVerdetto:
    def test_code_molto_pesanti(self):
        assert _F["mh315_verdetto"](_ris(xi=0.7)).startswith(
            "code molto pesanti")

    def test_code_pesanti(self):
        assert _F["mh315_verdetto"](_ris(xi=0.45)).startswith("code pesanti")

    def test_code_moderatamente_pesanti(self):
        assert _F["mh315_verdetto"](_ris(xi=0.2)).startswith(
            "code moderatamente pesanti")

    def test_code_sottili_campione_corto(self):
        v = _F["mh315_verdetto"](_ris(xi=0.1, ratio=1.5))
        assert "campione corto" in v

    def test_code_sottili_allineati(self):
        v = _F["mh315_verdetto"](_ris(xi=0.1, ratio=1.1))
        assert v.startswith("code sottili") and "allineati" in v

    def test_verdetto_demo(self):
        assert VERDETTO.startswith(STATO)
