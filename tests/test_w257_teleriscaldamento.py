"""Test tab257 'Teleriscaldamento vs caldaia': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab257.
"""

import math
import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("_tl257_num", "tl257_quote_mensili_default", "tl257_costo_caldaia",
          "tl257_costo_tlr", "tl257_confronto", "tl257_break_even_gas",
          "tl257_profilo_mensile", "tl257_cashflow_allaccio")
tl257_quote_mensili_default = _F["tl257_quote_mensili_default"]
tl257_costo_caldaia = _F["tl257_costo_caldaia"]
tl257_costo_tlr = _F["tl257_costo_tlr"]
tl257_confronto = _F["tl257_confronto"]
tl257_break_even_gas = _F["tl257_break_even_gas"]
tl257_profilo_mensile = _F["tl257_profilo_mensile"]
tl257_cashflow_allaccio = _F["tl257_cashflow_allaccio"]

APP = Path(__file__).parent.parent / "app.py"


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab257:
    def test_tab257_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 274
        assert "🔥 Teleriscaldamento vs caldaia" in titoli
        assert "tab257" in dvars
        assert "tab257" in withs
        assert titoli[dvars.index("tab257")] == "🔥 Teleriscaldamento vs caldaia"
        assert titoli[-1] == "⚛️ Nucleare SMR: business case"
        keys = re.findall(r'key="(tl257_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 8

    def test_titoli_allineati_256_257(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab256")] == "⚡ Perdite di rete"
        assert titoli[dvars.index("tab257")] == "🔥 Teleriscaldamento vs caldaia"

    def test_helper_definiti_prima_della_ui(self):
        src = APP.read_text(encoding="utf-8")
        i_ws = src.index("if workspace ==")
        for fn in ("tl257_quote_mensili_default", "tl257_costo_caldaia",
                   "tl257_costo_tlr", "tl257_confronto",
                   "tl257_break_even_gas", "tl257_profilo_mensile",
                   "tl257_cashflow_allaccio"):
            assert src.index(f"def {fn}(") < i_ws, fn


class TestTl257QuoteDefault:
    def test_somma_uno_e_dodici_mesi(self):
        q = tl257_quote_mensili_default()
        assert len(q) == 12
        assert sum(q) == pytest.approx(1.0)
        assert all(v >= 0 for v in q)
        assert q[0] == 0.19 and q[5] == 0.0


class TestTl257CostoCaldaia:
    def test_base(self):
        r = tl257_costo_caldaia(100000.0, 0.10, 90.0, 500.0)
        assert r["gas_kwh_anno"] == pytest.approx(111111.111111, rel=1e-9)
        assert r["costo_gas_eur"] == pytest.approx(11111.111111, rel=1e-9)
        assert r["manutenzione_eur"] == 500.0
        assert r["costo_totale_eur"] == pytest.approx(11611.111111, rel=1e-9)
        assert r["costo_eur_kwh_termico"] == pytest.approx(0.1161111111, rel=1e-9)

    def test_rendimento_cento(self):
        r = tl257_costo_caldaia(50000.0, 0.12, 100.0, 0.0)
        assert r["gas_kwh_anno"] == 50000.0
        assert r["costo_totale_eur"] == pytest.approx(6000.0)

    def test_fabbisogno_zero(self):
        r = tl257_costo_caldaia(0.0, 0.10, 90.0, 500.0)
        assert r["costo_totale_eur"] == 500.0
        assert r["costo_eur_kwh_termico"] == 0.0

    def test_errori(self):
        with pytest.raises(ValueError):
            tl257_costo_caldaia(-1.0, 0.10, 90.0, 500.0)
        with pytest.raises(ValueError):
            tl257_costo_caldaia(100000.0, -0.01, 90.0, 500.0)
        with pytest.raises(ValueError):
            tl257_costo_caldaia(100000.0, 0.10, 0.0, 500.0)
        with pytest.raises(ValueError):
            tl257_costo_caldaia(100000.0, 0.10, 101.0, 500.0)
        with pytest.raises(ValueError):
            tl257_costo_caldaia(100000.0, 0.10, 90.0, -5.0)
        with pytest.raises(ValueError):
            tl257_costo_caldaia(math.nan, 0.10, 90.0, 500.0)


class TestTl257CostoTlr:
    def test_base(self):
        r = tl257_costo_tlr(100000.0, 2000.0, 0.08)
        assert r["quota_fissa_eur"] == 2000.0
        assert r["costo_variabile_eur"] == pytest.approx(8000.0)
        assert r["costo_totale_eur"] == pytest.approx(10000.0)
        assert r["costo_eur_kwh_termico"] == pytest.approx(0.10)

    def test_errori(self):
        with pytest.raises(ValueError):
            tl257_costo_tlr(-1.0, 2000.0, 0.08)
        with pytest.raises(ValueError):
            tl257_costo_tlr(100000.0, -1.0, 0.08)
        with pytest.raises(ValueError):
            tl257_costo_tlr(100000.0, 2000.0, -0.01)
        with pytest.raises(ValueError):
            tl257_costo_tlr(True, 2000.0, 0.08)


class TestTl257Confronto:
    def test_tlr_conviene(self):
        r = tl257_confronto(100000.0, 0.10, 90.0, 500.0, 2000.0, 0.08)
        assert r["costo_caldaia_eur"] == pytest.approx(11611.111111, rel=1e-9)
        assert r["costo_tlr_eur"] == pytest.approx(10000.0)
        assert r["risparmio_eur_anno"] == pytest.approx(1611.111111, rel=1e-9)
        assert r["risparmio_pct"] == pytest.approx(13.875598086124402, rel=1e-9)
        assert r["conveniente"] == "tlr"

    def test_caldaia_conviene(self):
        r = tl257_confronto(100000.0, 0.05, 95.0, 500.0, 2000.0, 0.12)
        assert r["conveniente"] == "caldaia"
        assert r["risparmio_eur_anno"] < 0

    def test_pari(self):
        r = tl257_confronto(100000.0, 0.0855, 90.0, 500.0, 2000.0, 0.08)
        assert r["conveniente"] == "pari"
        assert r["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)

    def test_determinismo(self):
        a = tl257_confronto(200000.0, 0.10, 92.0, 800.0, 2500.0, 0.085)
        b = tl257_confronto(200000.0, 0.10, 92.0, 800.0, 2500.0, 0.085)
        assert a == b


class TestTl257BreakEvenGas:
    def test_base(self):
        be = tl257_break_even_gas(100000.0, 90.0, 500.0, 2000.0, 0.08)
        assert be == pytest.approx(0.0855, rel=1e-9)

    def test_coerenza_con_confronto(self):
        be = tl257_break_even_gas(200000.0, 92.0, 800.0, 2500.0, 0.085)
        r = tl257_confronto(200000.0, be, 92.0, 800.0, 2500.0, 0.085)
        assert r["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-4)

    def test_negativo_se_tlr_sempre_conveniente(self):
        be = tl257_break_even_gas(100000.0, 90.0, 50000.0, 1000.0, 0.01)
        assert be < 0

    def test_errori(self):
        with pytest.raises(ValueError):
            tl257_break_even_gas(0.0, 90.0, 500.0, 2000.0, 0.08)
        with pytest.raises(ValueError):
            tl257_break_even_gas(100000.0, 0.0, 500.0, 2000.0, 0.08)


class TestTl257ProfiloMensile:
    def test_base(self):
        righe = tl257_profilo_mensile(120000.0)
        assert len(righe) == 12
        assert righe[0] == {"mese": 1, "quota": 0.19, "fabbisogno_kwh": 22800.0}
        assert righe[5]["fabbisogno_kwh"] == 0.0
        assert sum(r["fabbisogno_kwh"] for r in righe) == pytest.approx(120000.0)

    def test_quote_custom(self):
        q = [1 / 12.0] * 12
        righe = tl257_profilo_mensile(12000.0, q)
        assert all(r["fabbisogno_kwh"] == pytest.approx(1000.0) for r in righe)

    def test_errori(self):
        with pytest.raises(ValueError):
            tl257_profilo_mensile(-1.0)
        with pytest.raises(ValueError):
            tl257_profilo_mensile(120000.0, [0.5, 0.5])
        with pytest.raises(ValueError):
            tl257_profilo_mensile(120000.0, [0.1] * 12)
        with pytest.raises(ValueError):
            tl257_profilo_mensile(120000.0, [-0.1] + [0.1] * 10 + [0.2])


class TestTl257CashflowAllaccio:
    def test_base(self):
        r = tl257_cashflow_allaccio(15000.0, 1611.11, 15, 4.0)
        assert r["flussi"][0] == -15000.0
        assert r["flussi"][1] == 1611.11
        assert len(r["flussi"]) == 16
        assert r["payback_anni"] == pytest.approx(15000.0 / 1611.11, rel=1e-9)
        atteso_van = sum(1611.11 / 1.04 ** n for n in range(1, 16)) - 15000.0
        assert r["van_eur"] == pytest.approx(atteso_van, rel=1e-9)
        assert r["van_eur"] > 0
        assert r["risparmio_totale_eur"] == pytest.approx(24166.65)

    def test_payback_mai(self):
        r = tl257_cashflow_allaccio(100000.0, 1000.0, 10, 4.0)
        assert r["payback_anni"] is None
        assert r["van_eur"] < 0

    def test_risparmio_negativo(self):
        r = tl257_cashflow_allaccio(15000.0, -500.0, 15, 4.0)
        assert r["payback_anni"] is None
        assert r["van_eur"] < -15000.0

    def test_tasso_zero(self):
        r = tl257_cashflow_allaccio(10000.0, 3000.0, 5, 0.0)
        assert r["van_eur"] == pytest.approx(5000.0)
        assert r["payback_anni"] == pytest.approx(10000.0 / 3000.0)

    def test_errori(self):
        with pytest.raises(ValueError):
            tl257_cashflow_allaccio(-1.0, 1000.0, 15, 4.0)
        with pytest.raises(ValueError):
            tl257_cashflow_allaccio(15000.0, 1000.0, 0, 4.0)
        with pytest.raises(ValueError):
            tl257_cashflow_allaccio(15000.0, 1000.0, 15, 100.0)
        with pytest.raises(ValueError):
            tl257_cashflow_allaccio(15000.0, 1000.0, 7.5, 4.0)

    def test_determinismo(self):
        a = tl257_cashflow_allaccio(15000.0, 1611.11, 15, 4.0)
        b = tl257_cashflow_allaccio(15000.0, 1611.11, 15, 4.0)
        assert a == b
