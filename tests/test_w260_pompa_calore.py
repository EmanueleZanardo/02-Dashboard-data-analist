"""Test tab260 'Pompa di calore vs caldaia': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab260.
"""

import math
import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("pc260_num", "pc260_costo_termico_pdc",
          "pc260_costo_termico_caldaia", "pc260_confronto",
          "pc260_break_even_elettricita", "pc260_break_even_gas",
          "pc260_sensibilita_scop", "pc260_cashflow")
pc260_num = _F["pc260_num"]
pc260_costo_termico_pdc = _F["pc260_costo_termico_pdc"]
pc260_costo_termico_caldaia = _F["pc260_costo_termico_caldaia"]
pc260_confronto = _F["pc260_confronto"]
pc260_break_even_elettricita = _F["pc260_break_even_elettricita"]
pc260_break_even_gas = _F["pc260_break_even_gas"]
pc260_sensibilita_scop = _F["pc260_sensibilita_scop"]
pc260_cashflow = _F["pc260_cashflow"]

APP = Path(__file__).parent.parent / "app.py"

TITLE260 = "❄️ Pompa di calore vs caldaia"
TITLE259 = "🇮🇹 PUN da prezzi zonali"


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab260:
    def test_tab260_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 261
        assert TITLE260 in titoli
        assert "tab260" in dvars
        assert "tab260" in withs
        assert titoli[dvars.index("tab260")] == TITLE260
        assert titoli[-1] == "🏢 PUE & costo data center"
        keys = re.findall(r'key="(pc260_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 8

    def test_titoli_allineati_259_260(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab259")] == TITLE259
        assert titoli[dvars.index("tab260")] == TITLE260


class TestPc260Num:
    def test_ok(self):
        assert pc260_num(3, "x") == 3.0
        assert pc260_num(2.5, "x") == 2.5

    def test_invalidi(self):
        for bad in (True, False, float("nan"), float("inf"), "3", None):
            with pytest.raises(ValueError):
                pc260_num(bad, "x")


class TestPc260CostoTermico:
    def test_pdc_base(self):
        assert pc260_costo_termico_pdc(180.0, 3.0) == pytest.approx(60.0)

    def test_pdc_con_manutenzione(self):
        # 180/3 + 150/20 = 60 + 7.5
        assert pc260_costo_termico_pdc(180.0, 3.0, 150.0, 20.0) == pytest.approx(67.5)

    def test_pdc_invalidi(self):
        with pytest.raises(ValueError):
            pc260_costo_termico_pdc(180.0, 0.0)
        with pytest.raises(ValueError):
            pc260_costo_termico_pdc(-1.0, 3.0)
        with pytest.raises(ValueError):
            pc260_costo_termico_pdc(180.0, 3.0, 0.0, 0.0)

    def test_caldaia_base(self):
        assert pc260_costo_termico_caldaia(55.0, 0.92) == pytest.approx(55.0 / 0.92)

    def test_caldaia_con_co2(self):
        # 55/0.92 + 80*0.202/0.92
        atteso = 55.0 / 0.92 + 80.0 * 0.202 / 0.92
        assert pc260_costo_termico_caldaia(55.0, 0.92, 0.0, 1.0, 80.0) == pytest.approx(atteso)

    def test_caldaia_invalidi(self):
        with pytest.raises(ValueError):
            pc260_costo_termico_caldaia(55.0, 0.0)
        with pytest.raises(ValueError):
            pc260_costo_termico_caldaia(55.0, 1.5)
        with pytest.raises(ValueError):
            pc260_costo_termico_caldaia(55.0, 0.92, 0.0, 1.0, -5.0)


class TestPc260Confronto:
    def test_verdetto_pdc(self):
        r = pc260_confronto(180.0, 3.0, 55.0, 0.92, 20.0,
                            manut_pdc_eur=150.0, manut_caldaia_eur=120.0,
                            prezzo_co2_eur_t=80.0)
        assert r["verdetto"] == "pompa di calore"
        assert r["costo_pdc_eur_mwh"] == pytest.approx(67.5)
        assert r["costo_caldaia_eur_mwh"] == pytest.approx(
            55.0 / 0.92 + 80.0 * 0.202 / 0.92 + 120.0 / 20.0)
        assert r["risparmio_annuo_eur"] == pytest.approx(
            r["risparmio_eur_mwh"] * 20.0)
        assert r["risparmio_pct"] == pytest.approx(
            r["risparmio_eur_mwh"] / r["costo_caldaia_eur_mwh"] * 100.0)

    def test_verdetto_caldaia(self):
        # elettricita' cara, gas economico, niente CO2: vince la caldaia
        r = pc260_confronto(400.0, 2.0, 30.0, 0.95, 20.0)
        assert r["verdetto"] == "caldaia"
        assert r["risparmio_eur_mwh"] < 0

    def test_pareggio(self):
        r = pc260_confronto(0.0, 3.0, 0.0, 0.9, 10.0)
        assert r["verdetto"] == "pareggio"
        assert r["risparmio_eur_mwh"] == pytest.approx(0.0)


class TestPc260BreakEven:
    def test_coerenza_elettricita(self):
        # al prezzo di break-even il confronto deve dare ~pareggio
        be = pc260_break_even_elettricita(55.0, 0.92, 3.0, 150.0, 120.0,
                                          20.0, 80.0)
        r = pc260_confronto(be, 3.0, 55.0, 0.92, 20.0, 150.0, 120.0, 80.0)
        assert r["risparmio_eur_mwh"] == pytest.approx(0.0, abs=1e-9)
        assert be > 180.0  # con questi default la PDC conviene a 180

    def test_coerenza_gas(self):
        be = pc260_break_even_gas(180.0, 3.0, 0.92, 150.0, 120.0, 20.0, 80.0)
        r = pc260_confronto(180.0, 3.0, be, 0.92, 20.0, 150.0, 120.0, 80.0)
        assert r["risparmio_eur_mwh"] == pytest.approx(0.0, abs=1e-9)
        assert be < 55.0


class TestPc260Sensibilita:
    def test_monotona_decrescente(self):
        righe = pc260_sensibilita_scop(180.0, 2.0, 5.0, 0.5)
        assert len(righe) == 7
        assert righe[0]["scop"] == pytest.approx(2.0)
        assert righe[-1]["scop"] == pytest.approx(5.0)
        costi = [r["costo_termico"] for r in righe]
        assert all(a > b for a, b in zip(costi, costi[1:]))
        assert righe[0]["costo_termico"] == pytest.approx(90.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            pc260_sensibilita_scop(180.0, 0.0, 5.0, 0.5)
        with pytest.raises(ValueError):
            pc260_sensibilita_scop(180.0, 5.0, 2.0, 0.5)
        with pytest.raises(ValueError):
            pc260_sensibilita_scop(180.0, 2.0, 5.0, 0.0)


class TestPc260Cashflow:
    def test_payback_e_van(self):
        # capex 12000, risparmio 2000/anno, 15 anni, 4%
        cw = pc260_cashflow(12000.0, 2000.0, 15, 4.0)
        assert cw["payback_anni"] == 6
        assert len(cw["righe"]) == 15
        assert cw["righe"][0]["cumulato"] == pytest.approx(-10000.0)
        att = sum(2000.0 / 1.04 ** a for a in range(1, 16))
        assert cw["van_eur"] == pytest.approx(-12000.0 + att)
        assert cw["righe"][5]["cumulato_attualizzato"] == pytest.approx(
            -12000.0 + sum(2000.0 / 1.04 ** a for a in range(1, 7)))

    def test_mai_payback(self):
        cw = pc260_cashflow(12000.0, 100.0, 10, 4.0)
        assert cw["payback_anni"] is None
        assert cw["van_eur"] < 0

    def test_invalidi(self):
        with pytest.raises(ValueError):
            pc260_cashflow(12000.0, 2000.0, 0, 4.0)
        with pytest.raises(ValueError):
            pc260_cashflow(12000.0, 2000.0, 15, -1.0)
        with pytest.raises(ValueError):
            pc260_cashflow(-5.0, 2000.0, 15, 4.0)
        with pytest.raises(ValueError):
            pc260_cashflow(12000.0, 2000.0, 15.5, 4.0)
