"""Test tab499 '🎯 Regret della copertura: fissato vs spot': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh499_num", "mh499_num_ge0", "mh499_num_pos", "mh499_mese",
           "mh499_lato", "mh499_costi", "mh499_tol", "mh499_fissazione",
           "mh499_risparmio", "mh499_linee", "mh499_verdetto",
           "mh499_riepilogo")

TITLE499 = "🎯 Regret della copertura: fissato vs spot"
TITLE498 = "📓 Blotter delle coperture: registro operazioni"


def _fix(comm, scad, lato, vol, fisso, reg, costi):
    return _F["mh499_fissazione"](comm, scad, lato, vol, fisso, reg, costi)


# Demo: acquisto TTF che risparmia, vendita TTF in regret, acquisto power in regret
FIX_BUY = _fix("TTF gas", "2027-01", "ACQUISTO", 60000.0, 88.40, 95.10, 250.0)
FIX_SELL = _fix("TTF gas", "2027-01", "VENDITA", 20000.0, 89.10, 95.10, 120.0)
FIX_PWR = _fix("Power baseload DE", "2027-03", "ACQUISTO", 49938.26, 116.20, 112.40, 400.0)


class TestW499Validatori:
    def test_num_ok(self):
        assert _F["mh499_num"](3, "x") == 3.0

    def test_num_ko(self):
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh499_num"](bad, "x")

    def test_num_pos_ko(self):
        for bad in (0.0, -1.0):
            with pytest.raises(ValueError):
                _F["mh499_num_pos"](bad, "x")

    def test_mese_ok(self):
        assert _F["mh499_mese"]("2027-01", "x") == "2027-01"

    def test_mese_ko(self):
        for bad in ("2027-13", "27-01", 202701, "2027/01"):
            with pytest.raises(ValueError):
                _F["mh499_mese"](bad, "x")

    def test_lato_ok(self):
        assert _F["mh499_lato"]("ACQUISTO", "x") == 1.0
        assert _F["mh499_lato"]("vendita", "x") == -1.0

    def test_lato_ko(self):
        with pytest.raises(ValueError):
            _F["mh499_lato"]("LONG", "x")

    def test_tol_ko(self):
        with pytest.raises(ValueError):
            _F["mh499_tol"](-1.0, "x")
        with pytest.raises(ValueError):
            _F["mh499_tol"](1e10, "x")

    def test_fissazione_ko(self):
        with pytest.raises(ValueError):
            _fix("", "2027-01", "ACQUISTO", 100.0, 80.0, 90.0, 10.0)
        with pytest.raises(ValueError):
            _fix("TTF gas", "2027-01", "ACQUISTO", 0.0, 80.0, 90.0, 10.0)
        with pytest.raises(ValueError):
            _fix("TTF gas", "2027-01", "ACQUISTO", 100.0, 80.0, 0.0, 10.0)


class TestW499Risparmio:
    def test_acquisto_risparmia_a_mano(self):
        # 60000 * (95.10 - 88.40) - 250 = 401750.0
        r = _F["mh499_risparmio"](FIX_BUY)
        assert r["risparmio_eur"] == pytest.approx(401750.0)
        assert r["riferimento_eur"] == pytest.approx(60000.0 * 95.10)
        assert r["efficacia"] == pytest.approx(401750.0 / (60000.0 * 95.10))

    def test_vendita_regret_a_mano(self):
        # -20000 * (95.10 - 89.10) - 120 = -120120.0
        r = _F["mh499_risparmio"](FIX_SELL)
        assert r["risparmio_eur"] == pytest.approx(-120120.0)

    def test_vendita_guadagna_se_fisso_sopra_regolamento(self):
        f = _fix("CO2 EUA", "2026-12", "VENDITA", 1000.0, 90.0, 80.0, 50.0)
        r = _F["mh499_risparmio"](f)
        assert r["risparmio_eur"] == pytest.approx(1000.0 * 10.0 - 50.0)

    def test_determinismo(self):
        r1 = _F["mh499_risparmio"](FIX_PWR)
        r2 = _F["mh499_risparmio"](FIX_PWR)
        assert r1 == r2


class TestW499Linee:
    def test_netting_stessa_linea(self):
        linee = _F["mh499_linee"]([FIX_BUY, FIX_SELL])
        assert len(linee) == 1
        ln = linee[0]
        assert ln["commodity"] == "TTF gas" and ln["scadenza"] == "2027-01"
        assert ln["n_righe"] == 2
        assert ln["volume_mwh"] == pytest.approx(80000.0)
        assert ln["risparmio_eur"] == pytest.approx(401750.0 - 120120.0)
        assert ln["costi_eur"] == pytest.approx(370.0)

    def test_due_linee_ordinate(self):
        linee = _F["mh499_linee"]([FIX_PWR, FIX_BUY])
        assert [ (l["commodity"], l["scadenza"]) for l in linee ] == [
            ("Power baseload DE", "2027-03"), ("TTF gas", "2027-01")]

    def test_linee_vuote_ko(self):
        with pytest.raises(ValueError):
            _F["mh499_linee"]([])


class TestW499VerdettoRiepilogo:
    def test_verdetto_rami(self):
        assert _F["mh499_verdetto"](15000.0, 10000.0) == "COPERTURA_UTILE"
        assert _F["mh499_verdetto"](-15000.0, 10000.0) == "REGRET"
        assert _F["mh499_verdetto"](5000.0, 10000.0) == "NEUTRA"
        assert _F["mh499_verdetto"](-5000.0, 10000.0) == "NEUTRA"

    def test_riepilogo_totali(self):
        rie = _F["mh499_riepilogo"]([FIX_BUY, FIX_SELL, FIX_PWR], 10000.0)
        assert rie["n_fissazioni"] == 3
        assert rie["mwh_totali"] == pytest.approx(60000.0 + 20000.0 + 49938.26)
        exp = 401750.0 - 120120.0 + (49938.26 * (112.40 - 116.20) - 400.0)
        assert rie["risparmio_totale_eur"] == pytest.approx(exp)
        assert rie["costi_totali_eur"] == pytest.approx(770.0)
        # 1 riga su 3 con risparmio > 0
        assert rie["hit_rate"] == pytest.approx(1 / 3)
        assert rie["verdetto"] in ("COPERTURA_UTILE", "REGRET", "NEUTRA")
        assert len(rie["linee"]) == 2
        assert len(rie["righe"]) == 3

    def test_riepilogo_ko(self):
        with pytest.raises(ValueError):
            _F["mh499_riepilogo"]([], 10000.0)
        with pytest.raises(ValueError):
            _F["mh499_riepilogo"]([FIX_BUY], -5.0)


def test_registry_tab499():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 528
    assert TITLE499 in titoli
    assert src.count(TITLE499) == 3
    assert "tab498, tab499, tab500, tab501, tab502, tab503, tab504, tab505, tab506, tab507, tab508, tab509, tab510, tab511, tab512, tab513, tab514, tab515, tab516, tab517, tab518, tab519, tab520, tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528 = st.tabs([" in src
    assert "    with tab499:" in src
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    assert "tab499" in dvars
    withs = re.findall(r"    with (tab\d+):", src)
    assert "tab499" in withs
    assert len(withs) == len(dvars) == 528
    # ordine: tab499 dopo tab498
    _decl499 = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    assert _decl499.index(f'"{TITLE498}"') < _decl499.index(f'"{TITLE499}"')
    assert titoli[dvars.index("tab499")] == TITLE499


def test_chiavi_st499_uniche():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    keys = re.findall(r'key="(st499_[^"]+)"', src) + re.findall(
        r'key=f"(st499_[^"]+)"', src)
    assert len(keys) == len(set(keys)) > 10
