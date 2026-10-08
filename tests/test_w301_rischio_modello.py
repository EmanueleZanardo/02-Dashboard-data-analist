"""Test tab301 '🛡️🔍 Rischio di modello: quale VaR credere?': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab301. Rischio di modello sul VaR: stesso P&L,
tre modelli (normale, storico, Cornish-Fisher), dispersione tra modelli,
capitale prudente con buffer e verdetto sul disaccordo (follow-up del filone
rischio tab292/294/295/297/298/299/300).
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("mr301_num", "mr301_conf", "mr301_parse_pl", "mr301_serie_demo",
          "mr301_media", "mr301_dev_std", "mr301_skew", "mr301_kurt_eccesso",
          "mr301_norm_cdf", "mr301_norm_ppf", "mr301_quantile",
          "mr301_var_normale", "mr301_var_storico", "mr301_var_cornish_fisher",
          "mr301_tre_var", "mr301_dispersione", "mr301_capitale_prudente",
          "mr301_verdetto")
mr301_num = _F["mr301_num"]
mr301_conf = _F["mr301_conf"]
mr301_parse_pl = _F["mr301_parse_pl"]
mr301_serie_demo = _F["mr301_serie_demo"]
mr301_media = _F["mr301_media"]
mr301_dev_std = _F["mr301_dev_std"]
mr301_skew = _F["mr301_skew"]
mr301_kurt_eccesso = _F["mr301_kurt_eccesso"]
mr301_norm_cdf = _F["mr301_norm_cdf"]
mr301_norm_ppf = _F["mr301_norm_ppf"]
mr301_quantile = _F["mr301_quantile"]
mr301_var_normale = _F["mr301_var_normale"]
mr301_var_storico = _F["mr301_var_storico"]
mr301_var_cornish_fisher = _F["mr301_var_cornish_fisher"]
mr301_tre_var = _F["mr301_tre_var"]
mr301_dispersione = _F["mr301_dispersione"]
mr301_capitale_prudente = _F["mr301_capitale_prudente"]
mr301_verdetto = _F["mr301_verdetto"]

APP = Path(__file__).parent.parent / "app.py"

TITLE301 = "🛡️🔍 Rischio di modello: quale VaR credere?"
TITLE300 = "🧮📊 Rapporto di diversificazione: quanto rischio risparmia il book?"
TITLE299 = "🧪⚡ Stress test: quanto perde il book negli scenari?"

# demo: 120 P&L con shock di coda (seed 7)
N_DEMO = 120
SYN = [-2000.0, -500.0, 1000.0, 3000.0, -1500.0, 2500.0, -800.0, 1200.0]


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab301:
    def test_tab301_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 301
        assert TITLE301 in titoli
        assert "tab301" in dvars
        assert "tab301" in withs
        assert titoli[dvars.index("tab301")] == TITLE301
        assert titoli[-1] == TITLE301
        keys = re.findall(r'key="(st301_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_299_300_301(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab299")] == TITLE299
        assert titoli[dvars.index("tab300")] == TITLE300
        assert titoli[dvars.index("tab301")] == TITLE301


class TestMr301Validatori:
    def test_num_ok(self):
        assert mr301_num(2.5, "x") == 2.5

    def test_num_bool_ko(self):
        with pytest.raises(ValueError):
            mr301_num(True, "x")

    def test_num_nan_ko(self):
        with pytest.raises(ValueError):
            mr301_num(float("nan"), "x")

    def test_conf_ok(self):
        assert mr301_conf(95) == 95

    def test_conf_ko(self):
        with pytest.raises(ValueError):
            mr301_conf(97)


class TestMr301ParsePl:
    def test_ok(self):
        p = mr301_parse_pl("# cmt\n\n" + "\n".join(["1,5"] * 19 + ["2.5"]))
        assert len(p) == 20
        assert p[0] == 1.5

    def test_poche_osservazioni_ko(self):
        with pytest.raises(ValueError):
            mr301_parse_pl("\n".join(["1"] * 19))

    def test_non_numerico_ko(self):
        with pytest.raises(ValueError):
            mr301_parse_pl("\n".join(["xx"] * 20))


class TestMr301Demo:
    def test_deterministica(self):
        assert mr301_serie_demo(7) == mr301_serie_demo(7)

    def test_dimensione(self):
        assert len(mr301_serie_demo(7)) == N_DEMO

    def test_code_pesanti(self):
        assert mr301_skew(mr301_serie_demo(7)) < 0.0
        assert mr301_kurt_eccesso(mr301_serie_demo(7)) > 0.0


class TestMr301Statistiche:
    def test_media(self):
        assert mr301_media(SYN) == pytest.approx(362.5)

    def test_dev_std(self):
        assert mr301_dev_std(SYN) == pytest.approx(1843.085534020135)

    def test_skew_simmetrica_zero(self):
        assert mr301_skew([-2.0, -1.0, 0.0, 1.0, 2.0]) == pytest.approx(0.0)

    def test_skew_demo(self):
        assert mr301_skew(mr301_serie_demo(7)) == pytest.approx(-1.0956811663608865)

    def test_kurt_demo(self):
        assert mr301_kurt_eccesso(mr301_serie_demo(7)) == pytest.approx(1.9468916036671624)

    def test_una_osservazione_ko(self):
        with pytest.raises(ValueError):
            mr301_dev_std([5.0])


class TestMr301NormPpf:
    def test_mediana_zero(self):
        assert mr301_norm_ppf(0.5) == pytest.approx(0.0, abs=1e-9)

    def test_0975(self):
        assert mr301_norm_ppf(0.975) == pytest.approx(1.9599639845400536)

    def test_simmetria(self):
        assert mr301_norm_ppf(0.025) == pytest.approx(-1.9599639845400536)

    def test_fuori_range_ko(self):
        with pytest.raises(ValueError):
            mr301_norm_ppf(1.0)


class TestMr301Var:
    def test_tre_chiavi(self):
        tre = mr301_tre_var(mr301_serie_demo(7), 95)
        assert set(tre) == {"normale", "storico", "cornish_fisher"}
        assert all(v >= 0.0 for v in tre.values())

    def test_valori_demo(self):
        tre = mr301_tre_var(mr301_serie_demo(7), 95)
        assert tre["normale"] == pytest.approx(8804.343053705083)
        assert tre["storico"] == pytest.approx(8313.99)
        assert tre["cornish_fisher"] == pytest.approx(10082.058415788386)

    def test_modelli_in_disaccordo_demo(self):
        tre = mr301_tre_var(mr301_serie_demo(7), 95)
        assert len({round(v, 6) for v in tre.values()}) == 3

    def test_quantile_storico_noto(self):
        assert mr301_quantile([1.0, 2.0, 3.0, 4.0], 0.5) == pytest.approx(2.5)


class TestMr301Dispersione:
    def test_nota(self):
        d = mr301_dispersione({"a": 100.0, "b": 150.0})
        assert d["min"] == pytest.approx(100.0)
        assert d["max"] == pytest.approx(150.0)
        assert d["range_eur"] == pytest.approx(50.0)
        assert d["range_pct"] == pytest.approx(100.0 * 50.0 / 150.0)

    def test_demo(self):
        tre = mr301_tre_var(mr301_serie_demo(7), 95)
        d = mr301_dispersione(tre)
        assert d["range_pct"] == pytest.approx(17.536780118429103)
        assert d["range_eur"] == pytest.approx(1768.0684157883861)


class TestMr301Capitale:
    def test_noto(self):
        assert mr301_capitale_prudente({"a": 100.0, "b": 150.0},
                                       10.0) == pytest.approx(165.0)

    def test_buffer_zero(self):
        assert mr301_capitale_prudente({"a": 100.0},
                                       0.0) == pytest.approx(100.0)

    def test_buffer_negativo_ko(self):
        with pytest.raises(ValueError):
            mr301_capitale_prudente({"a": 100.0}, -5.0)

    def test_demo(self):
        tre = mr301_tre_var(mr301_serie_demo(7), 95)
        assert mr301_capitale_prudente(tre, 10.0) == pytest.approx(11090.264257367226)


class TestMr301Verdetto:
    def test_concordi(self):
        assert mr301_verdetto(5.0).startswith("modelli concordi")
        assert mr301_verdetto(9.99).startswith("modelli concordi")

    def test_moderato(self):
        assert mr301_verdetto(10.0).startswith("disaccordo moderato")
        assert mr301_verdetto(24.99).startswith("disaccordo moderato")

    def test_forte(self):
        assert mr301_verdetto(25.0).startswith("disaccordo forte")
        assert mr301_verdetto(60.0).startswith("disaccordo forte")

    def test_demo(self):
        tre = mr301_tre_var(mr301_serie_demo(7), 95)
        d = mr301_dispersione(tre)
        assert mr301_verdetto(d["range_pct"]) == "disaccordo moderato: le code sono piu' pesanti di quanto dice la normale"


class TestMr301Integrazione:
    def test_catena_demo(self):
        pl = mr301_serie_demo(7)
        assert len(pl) == N_DEMO
        tre = mr301_tre_var(pl, 95)
        d = mr301_dispersione(tre)
        cap = mr301_capitale_prudente(tre, 10.0)
        assert cap == pytest.approx(d["max"] * 1.10)
        assert mr301_verdetto(d["range_pct"]) == "disaccordo moderato: le code sono piu' pesanti di quanto dice la normale"
        assert cap >= d["max"] >= d["min"] >= 0.0
