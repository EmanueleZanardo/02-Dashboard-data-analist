"""Test tab479 '🏦 Costo del margine: il capitale fermo al clearing': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh479_num", "mh479_margine_linea", "mh479_margine_totale",
           "mh479_nozionale", "mh479_costo_funding", "mh479_costo_bps",
           "mh479_sensibilita_tasso", "mh479_sensibilita_giorni",
           "mh479_verdetto")

TITLE482 = "🗓️ Ladder delle scadenze: profilo temporale di volumi, MtM e DV01"
TITLE479 = "🏦 Costo del margine: il capitale fermo al clearing"
TITLE478 = "📉 Implementation shortfall: scomponi il costo realizzato"

# Demo deterministica: portafoglio futures al clearing.
# TTF gas 250'000 MWh @ IM 4.20 EUR/MWh, prezzo 95 EUR/MWh;
# Power baseload DE 120'000 MWh @ IM 6.50 EUR/MWh, prezzo 110 EUR/MWh;
# CO2 EUA 0 t @ IM 3.00 EUR/t, prezzo 75 EUR/t.
# tasso funding 4.50% p.a., detenzione 60 giorni, soglia verdetto 5 bps.
LINEE_DEMO = [
    {"nome": "TTF gas", "qta_mwh": 250000.0, "im_eur_mwh": 4.20},
    {"nome": "Power baseload DE", "qta_mwh": 120000.0, "im_eur_mwh": 6.50},
    {"nome": "CO2 EUA", "qta_mwh": 0.0, "im_eur_mwh": 3.00},
]
PREZZI_DEMO = [95.0, 110.0, 75.0]
QTY_DEMO = [250000.0, 120000.0, 0.0]
TASSO_DEMO = 4.50
GIORNI_DEMO = 60.0
SOGLIA_DEMO = 5.0
MARGINE_DEMO = 1830000.0
NOZIONALE_DEMO = 36950000.0
COSTO_DEMO = 13536.986301369861
BPS_DEMO = 3.663595751385619
VERD_DEMO = 'RILEVANTE'


class TestRegistry481:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"    with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 555

    def test_ultima_tab(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert TITLE482 in titoli
        assert TITLE479 in titoli  # membership (non [-2]: la posizione scorre a ogni ciclo)
        assert "tab482" in dvars
        assert f"with tab482:" in src

    def test_chiavi_univoche(self):
        import re
        from collections import Counter
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        keys = re.findall(r'key="(st479_[^"]+)"', src)
        # chiavi generate via f-string nel loop linee (indici 0..2)
        for pre in re.findall(r'key=f"st479_(\w+)\{', src):
            keys += [f"st479_{pre}{i}" for i in range(3)]
        assert len(keys) == 16, f"attese 16 chiavi st479_*, trovate {len(keys)}"
        dup = [k for k, n in Counter(keys).items() if n > 1]
        assert not dup, f"chiavi duplicate: {dup}"
        allkeys = re.findall(r'key="(st\d+_[^"]+)"', src)
        dup2 = [k for k, n in Counter(allkeys).items() if n > 1]
        assert not dup2, f"chiavi duplicate in app: {dup2[:5]}"


class TestNum479:
    def test_validi(self):
        assert _F["mh479_num"](3, "x") == 3.0
        assert _F["mh479_num"](2.5, "x") == 2.5
        assert _F["mh479_num"](0, "x") == 0.0

    def test_bool_rifiutato(self):
        with pytest.raises(ValueError):
            _F["mh479_num"](True, "x")

    def test_nan_inf_rifiutati(self):
        with pytest.raises(ValueError):
            _F["mh479_num"](math.nan, "x")
        with pytest.raises(ValueError):
            _F["mh479_num"](math.inf, "x")

    def test_stringa_rifiutata(self):
        with pytest.raises(ValueError):
            _F["mh479_num"]("4.5", "x")


class TestMargineLinea479:
    def test_demo_ttf(self):
        assert _F["mh479_margine_linea"](250000.0, 4.20) == 1050000.0

    def test_demo_power(self):
        assert _F["mh479_margine_linea"](120000.0, 6.50) == 780000.0

    def test_qta_zero(self):
        assert _F["mh479_margine_linea"](0.0, 4.20) == 0.0

    def test_qta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh479_margine_linea"](-1.0, 4.20)

    def test_im_negativo(self):
        with pytest.raises(ValueError):
            _F["mh479_margine_linea"](100.0, -0.5)

    def test_non_numero(self):
        with pytest.raises(ValueError):
            _F["mh479_margine_linea"]("100", 4.2)


class TestMargineTotale479:
    def test_demo(self):
        r = _F["mh479_margine_totale"](LINEE_DEMO)
        assert r["totale"] == pytest.approx(MARGINE_DEMO)
        assert r["n_linee"] == 3
        assert r["totale"] == MARGINE_DEMO

    def test_quote_sommano_uno(self):
        r = _F["mh479_margine_totale"](LINEE_DEMO)
        assert sum(x["quota"] for x in r["righe"]) == pytest.approx(1.0)

    def test_quota_ttf(self):
        r = _F["mh479_margine_totale"](LINEE_DEMO)
        assert r["righe"][0]["quota"] == pytest.approx(1050000.0 / 1830000.0)

    def test_lista_vuota(self):
        with pytest.raises(ValueError):
            _F["mh479_margine_totale"]([])

    def test_chiave_mancante(self):
        with pytest.raises(ValueError):
            _F["mh479_margine_totale"]([{"nome": "X", "qta_mwh": 1.0}])

    def test_qta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh479_margine_totale"](
                [{"nome": "X", "qta_mwh": -5.0, "im_eur_mwh": 1.0}])


class TestNozionale479:
    def test_demo(self):
        assert _F["mh479_nozionale"](QTY_DEMO, PREZZI_DEMO) == NOZIONALE_DEMO

    def test_lunghezze_diverse(self):
        with pytest.raises(ValueError):
            _F["mh479_nozionale"]([1.0, 2.0], [10.0])

    def test_prezzo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh479_nozionale"]([100.0], [-5.0])


class TestCostoFunding479:
    def test_demo(self):
        assert _F["mh479_costo_funding"](MARGINE_DEMO, TASSO_DEMO,
                                         GIORNI_DEMO) == pytest.approx(COSTO_DEMO)

    def test_formula_a_mano(self):
        c = _F["mh479_costo_funding"](1830000.0, 4.50, 60.0)
        assert c == pytest.approx(1830000.0 * 0.045 * 60.0 / 365.0)

    def test_giorni_zero(self):
        assert _F["mh479_costo_funding"](1830000.0, 4.50, 0.0) == 0.0

    def test_tasso_zero(self):
        assert _F["mh479_costo_funding"](1830000.0, 0.0, 60.0) == 0.0

    def test_margine_negativo(self):
        with pytest.raises(ValueError):
            _F["mh479_costo_funding"](-1.0, 4.5, 60.0)

    def test_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh479_costo_funding"](100.0, -1.0, 60.0)

    def test_giorni_negativi(self):
        with pytest.raises(ValueError):
            _F["mh479_costo_funding"](100.0, 4.5, -2.0)


class TestCostoBps479:
    def test_demo(self):
        assert _F["mh479_costo_bps"](COSTO_DEMO, NOZIONALE_DEMO) == pytest.approx(BPS_DEMO)

    def test_notionale_zero(self):
        with pytest.raises(ValueError):
            _F["mh479_costo_bps"](100.0, 0.0)

    def test_notionale_negativo(self):
        with pytest.raises(ValueError):
            _F["mh479_costo_bps"](100.0, -10.0)


class TestSensibilita479:
    def test_tasso_nove_punti(self):
        s = _F["mh479_sensibilita_tasso"](MARGINE_DEMO, GIORNI_DEMO, TASSO_DEMO)
        assert len(s) == 9
        assert s[0]["tasso_pct"] == 0.0
        assert s[-1]["tasso_pct"] == pytest.approx(2.0 * TASSO_DEMO)

    def test_tasso_estremi(self):
        s = _F["mh479_sensibilita_tasso"](MARGINE_DEMO, GIORNI_DEMO, TASSO_DEMO)
        assert s[0]["costo_eur"] == 0.0
        assert s[-1]["costo_eur"] == pytest.approx(2.0 * COSTO_DEMO)

    def test_tasso_punto_centrale(self):
        s = _F["mh479_sensibilita_tasso"](MARGINE_DEMO, GIORNI_DEMO, TASSO_DEMO)
        assert s[4]["tasso_pct"] == pytest.approx(TASSO_DEMO)
        assert s[4]["costo_eur"] == pytest.approx(COSTO_DEMO)

    def test_tasso_n_minimo_due(self):
        with pytest.raises(ValueError):
            _F["mh479_sensibilita_tasso"](100.0, 60.0, 4.5, n=1)

    def test_giorni_estremi(self):
        s = _F["mh479_sensibilita_giorni"](MARGINE_DEMO, TASSO_DEMO, GIORNI_DEMO)
        assert len(s) == 9
        assert s[0]["giorni"] == pytest.approx(0.5 * GIORNI_DEMO)
        assert s[-1]["giorni"] == pytest.approx(2.0 * GIORNI_DEMO)
        assert s[0]["costo_eur"] == pytest.approx(0.5 * COSTO_DEMO)
        assert s[-1]["costo_eur"] == pytest.approx(2.0 * COSTO_DEMO)

    def test_giorni_base_zero(self):
        with pytest.raises(ValueError):
            _F["mh479_sensibilita_giorni"](100.0, 4.5, 0.0)

    def test_monotona(self):
        s = _F["mh479_sensibilita_tasso"](MARGINE_DEMO, GIORNI_DEMO, TASSO_DEMO)
        costi = [x["costo_eur"] for x in s]
        assert all(b >= a for a, b in zip(costi, costi[1:]))


class TestVerdetto479:
    def test_demo(self):
        assert _F["mh479_verdetto"](BPS_DEMO, SOGLIA_DEMO) == VERD_DEMO

    def test_trascurabile(self):
        assert _F["mh479_verdetto"](2.5, 5.0) == "TRASCURABILE"
        assert _F["mh479_verdetto"](2.4999, 5.0) == "TRASCURABILE"

    def test_rilevante_confine(self):
        assert _F["mh479_verdetto"](2.5001, 5.0) == "RILEVANTE"
        assert _F["mh479_verdetto"](5.0, 5.0) == "RILEVANTE"

    def test_critico(self):
        assert _F["mh479_verdetto"](5.0001, 5.0) == "CRITICO"
        assert _F["mh479_verdetto"](50.0, 5.0) == "CRITICO"

    def test_soglia_zero(self):
        with pytest.raises(ValueError):
            _F["mh479_verdetto"](1.0, 0.0)

    def test_costo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh479_verdetto"](-1.0, 5.0)

    def test_nan(self):
        with pytest.raises(ValueError):
            _F["mh479_verdetto"](math.nan, 5.0)
