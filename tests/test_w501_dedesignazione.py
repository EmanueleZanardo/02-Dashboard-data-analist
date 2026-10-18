"""Test tab501 '🛑 De-designazione: continuare o chiudere la copertura?': registry + funzioni pure."""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh501_num", "mh501_str", "mh501_ge0", "mh501_pct", "mh501_int",
           "mh501_relazione", "mh501_verdetto", "mh501_riepilogo")

TITLE501 = "🛑 De-designazione: continuare o chiudere la copertura?"
TITLE500 = "📑 Efficacia contabile: dollar-offset delle coperture"


def _rel(nome, verdetto, res, orig, costo, mesi):
    return _F["mh501_relazione"](nome, verdetto, res, orig, costo, mesi)


def _verd(riga, soglia=10.0, budget=5000.0):
    return _F["mh501_verdetto"](riga, soglia, budget)


# Demo: uno per ogni decisione (ordine delle regole: la prima che scatta vince)
R_CONT = _rel("TTF Q1-27 future", "EFFICACE", 8000.0, 10000.0, 2500.0, 3)
R_DES = _rel("Power Cal-27 DE", "INEFFICACE", 5000.0, 6000.0, 8000.0, 9)
R_CHI = _rel("CO2 Dec-26 EUA", "EFFICACE", 200.0, 5000.0, 400.0, 1)
R_MAN = _rel("PSV baseload IT", "MARGINALE", 3000.0, 3000.0, 12000.0, 12)
R_SCA = _rel("TTF Wk-52 swap", "EFFICACE", 1500.0, 1500.0, 900.0, 0)
R_NDV = _rel("Gas spot proxy", "NON_VALUTABILE", 2500.0, 2500.0, 1100.0, 6)


class TestW501Validatori:
    def test_num_ok(self):
        assert _F["mh501_num"](3, "x") == 3.0
        assert _F["mh501_num"](-2.5, "x") == -2.5

    def test_num_ko(self):
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh501_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh501_str"]("  TTF  ", "x") == "TTF"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5):
            with pytest.raises(ValueError):
                _F["mh501_str"](bad, "x")

    def test_ge0_ok(self):
        assert _F["mh501_ge0"](0, "x") == 0.0
        assert _F["mh501_ge0"](12.5, "x") == 12.5

    def test_ge0_ko(self):
        with pytest.raises(ValueError):
            _F["mh501_ge0"](-0.01, "x")

    def test_pct_ok(self):
        assert _F["mh501_pct"](0, "x") == 0.0
        assert _F["mh501_pct"](100, "x") == 100.0
        assert _F["mh501_pct"](10.0, "x") == 10.0

    def test_pct_ko(self):
        for bad in (-0.1, 100.1, float("nan")):
            with pytest.raises(ValueError):
                _F["mh501_pct"](bad, "x")

    def test_int_ok(self):
        assert _F["mh501_int"](0, "x") == 0
        assert _F["mh501_int"](3.0, "x") == 3

    def test_int_ko(self):
        for bad in (-1, 1.5, 2.7):
            with pytest.raises(ValueError):
                _F["mh501_int"](bad, "x")


class TestW501Relazione:
    def test_quota_residua(self):
        r = _rel("TTF", "EFFICACE", 8000.0, 10000.0, 2500.0, 3)
        assert r["quota_residua_pct"] == pytest.approx(80.0)
        assert r["verdetto_eff"] == "EFFICACE"
        assert r["mesi_residui"] == 3

    def test_verdetto_case_insensitive(self):
        r = _rel("TTF", "efficace", 8000.0, 10000.0, 2500.0, 3)
        assert r["verdetto_eff"] == "EFFICACE"

    def test_relazione_ko(self):
        with pytest.raises(ValueError):
            _rel("TTF", "BOH", 8000.0, 10000.0, 2500.0, 3)      # verdetto ignoto
        with pytest.raises(ValueError):
            _rel("TTF", "EFFICACE", 8000.0, 0.0, 2500.0, 3)      # orig nulla
        with pytest.raises(ValueError):
            _rel("TTF", "EFFICACE", 12000.0, 10000.0, 2500.0, 3)  # residua > orig
        with pytest.raises(ValueError):
            _rel("TTF", "EFFICACE", -1.0, 10000.0, 2500.0, 3)    # residua < 0
        with pytest.raises(ValueError):
            _rel("TTF", "EFFICACE", 8000.0, 10000.0, -5.0, 3)    # costo < 0
        with pytest.raises(ValueError):
            _rel("TTF", "EFFICACE", 8000.0, 10000.0, 2500.0, -1)  # mesi < 0
        with pytest.raises(ValueError):
            _rel("  ", "EFFICACE", 8000.0, 10000.0, 2500.0, 3)    # nome vuoto


class TestW501Verdetto:
    def test_inefficace_de_designare(self):
        assert _verd(R_DES) == "DE-DESIGNARE"

    def test_non_valutabile_non_designabile(self):
        assert _verd(R_NDV) == "NON_DESIGNABILE"

    def test_residuo_immateriale_chiudere(self):
        assert _verd(R_CHI) == "CHIUDERE"
        # quota 4%: sopra la soglia 3% invece continua
        assert _verd(R_CHI, soglia=3.0) == "CONTINUARE"

    def test_scaduta(self):
        assert _verd(R_SCA) == "SCADUTA"

    def test_costo_oltre_budget_mantenere(self):
        assert _verd(R_MAN) == "MANTENERE"
        # con budget 20000 il costo 12000 rientra: continua
        assert _verd(R_MAN, budget=20000.0) == "CONTINUARE"

    def test_efficace_continuare(self):
        assert _verd(R_CONT) == "CONTINUARE"

    def test_ordine_regole_inefficace_vince_su_scaduta(self):
        r = _rel("X", "INEFFICACE", 100.0, 10000.0, 100.0, 0)
        assert _verd(r) == "DE-DESIGNARE"  # regola 1 prima della 4

    def test_verdetto_ko(self):
        with pytest.raises(ValueError):
            _F["mh501_verdetto"](R_CONT, 150.0, 5000.0)
        with pytest.raises(ValueError):
            _F["mh501_verdetto"](R_CONT, 10.0, -5.0)


class TestW501Riepilogo:
    def test_riepilogo_conteggi(self):
        rie = _F["mh501_riepilogo"](
            [R_CONT, R_DES, R_CHI, R_MAN, R_SCA, R_NDV], 10.0, 5000.0)
        assert rie["n_relazioni"] == 6
        c = rie["conteggi"]
        assert c == {"DE-DESIGNARE": 1, "NON_DESIGNABILE": 1, "CHIUDERE": 1,
                     "SCADUTA": 1, "MANTENERE": 1, "CONTINUARE": 1}
        assert [r["verdetto"] for r in rie["righe"]] == [
            "CONTINUARE", "DE-DESIGNARE", "CHIUDERE", "MANTENERE", "SCADUTA",
            "NON_DESIGNABILE"]

    def test_riepilogo_costo_chiusure(self):
        # solo le righe CHIUDERE contano nel costo di chiusura
        rie = _F["mh501_riepilogo"]([R_CONT, R_CHI], 10.0, 5000.0)
        assert rie["costo_chiusura_totale_eur"] == pytest.approx(400.0)

    def test_riepilogo_complessivo_il_peggiore(self):
        rie = _F["mh501_riepilogo"](
            [R_CONT, R_DES, R_CHI, R_MAN, R_SCA, R_NDV], 10.0, 5000.0)
        assert rie["verdetto_complessivo"] == "DE-DESIGNARE"
        rie2 = _F["mh501_riepilogo"]([R_CONT, R_SCA], 10.0, 5000.0)
        assert rie2["verdetto_complessivo"] == "SCADUTA"
        rie3 = _F["mh501_riepilogo"]([R_CONT], 10.0, 5000.0)
        assert rie3["verdetto_complessivo"] == "CONTINUARE"

    def test_riepilogo_ko(self):
        with pytest.raises(ValueError):
            _F["mh501_riepilogo"]([], 10.0, 5000.0)
        with pytest.raises(ValueError):
            _F["mh501_riepilogo"]([R_CONT], 150.0, 5000.0)
        with pytest.raises(ValueError):
            _F["mh501_riepilogo"]([R_CONT], 10.0, -5.0)


def test_registry_tab501():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 544
    assert TITLE501 in titoli
    assert src.count(TITLE501) == 3
    assert "tab498, tab499, tab500, tab501, tab502, tab503, tab504, tab505, tab506, tab507, tab508, tab509, tab510, tab511, tab512, tab513, tab514, tab515, tab516, tab517, tab518, tab519, tab520, tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544 = st.tabs([" in src
    assert "    with tab501:" in src
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    assert "tab501" in dvars
    withs = re.findall(r"    with (tab\d+):", src)
    assert "tab501" in withs
    assert len(withs) == len(dvars) == 544
    # ordine: tab501 dopo tab500
    _decl501 = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    assert _decl501.index(f'"{TITLE500}"') < _decl501.index(f'"{TITLE501}"')
    assert titoli[dvars.index("tab501")] == TITLE501


def test_chiavi_st501_uniche():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    keys = re.findall(r'key="(st501_[^"]+)"', src) + re.findall(
        r'key=f"(st501_[^"]+)"', src)
    assert len(keys) == len(set(keys)) > 10
