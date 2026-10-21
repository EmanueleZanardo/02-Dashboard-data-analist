"""Test tab521 '🧱 Basis adjustment (adeguamento del costo, IFRS 9 6.5.11)': registry + funzioni pure."""

import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh521_num", "mh521_str", "mh521_voce", "mh521_verifica",
           "mh521_riepilogo")

TITLE521 = "🧱 Basis adjustment (adeguamento del costo, IFRS 9 6.5.11)"
TITLE520 = "🔁 Aggregated exposure (esposizione aggregata, IFRS 9 6.3.4)"


def _v(vid="GAS-STOCC-001", t="cash_flow", nat="non_finanziario",
       st="avvenuta", p=450000.0, q=10000.0, c=28000.0,
       d="Acquisto gas per stoccaggio"):
    return {"id": vid, "tipo_copertura": t, "natura_item": nat,
            "stato_transazione": st, "prezzo_acquisto": p, "quantita": q,
            "saldo_cfhr": c, "descrizione": d}


class TestW521Validatori:
    def test_num_ok(self):
        assert _F["mh521_num"](2, "x") == 2.0
        assert _F["mh521_num"](-12000.5, "x") == -12000.5
        assert _F["mh521_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, "2", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh521_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh521_str"]("  GAS-1 ", "x") == "GAS-1"

    def test_str_ko(self):
        for bad in (None, "", "   ", 5):
            with pytest.raises(ValueError):
                _F["mh521_str"](bad, "x")


class TestW521Voce:
    def test_ok(self):
        r = _F["mh521_voce"](_v())
        assert r["id"] == "GAS-STOCC-001"
        assert r["tipo_copertura"] == "cash_flow"
        assert r["natura_item"] == "non_finanziario"
        assert r["stato_transazione"] == "avvenuta"
        assert r["prezzo_acquisto"] == pytest.approx(450000.0)
        assert r["quantita"] == pytest.approx(10000.0)
        assert r["saldo_cfhr"] == pytest.approx(28000.0)
        assert r["descrizione"] == "Acquisto gas per stoccaggio"

    def test_descrizione_default(self):
        d = _v()
        del d["descrizione"]
        assert _F["mh521_voce"](d)["descrizione"] == ""

    def test_saldo_cfhr_negativo_e_zero_ok(self):
        assert _F["mh521_voce"](_v(c=-12000.0))["saldo_cfhr"] == \
            pytest.approx(-12000.0)
        assert _F["mh521_voce"](_v(c=0.0))["saldo_cfhr"] == 0.0

    def test_tipo_ko(self):
        with pytest.raises(ValueError):
            _F["mh521_voce"](_v(t="net_investment"))
        with pytest.raises(ValueError):
            _F["mh521_voce"](_v(t="CASH_FLOW"))

    def test_natura_ko(self):
        with pytest.raises(ValueError):
            _F["mh521_voce"](_v(nat="misto"))

    def test_stato_ko(self):
        with pytest.raises(ValueError):
            _F["mh521_voce"](_v(st="pending"))

    def test_chiave_mancante(self):
        d = _v()
        del d["saldo_cfhr"]
        with pytest.raises(ValueError):
            _F["mh521_voce"](d)

    def test_non_dict(self):
        with pytest.raises(ValueError):
            _F["mh521_voce"](["id"])

    def test_id_vuoto(self):
        with pytest.raises(ValueError):
            _F["mh521_voce"](_v(vid="  "))

    def test_prezzo_qta_ko(self):
        for bad in (0, -5, True, float("nan"), "100"):
            with pytest.raises(ValueError):
                _F["mh521_voce"](_v(p=bad))
            with pytest.raises(ValueError):
                _F["mh521_voce"](_v(q=bad))

    def test_descrizione_non_str(self):
        with pytest.raises(ValueError):
            _F["mh521_voce"](_v(d=5))


class TestW521Verifica:
    def test_demo_applicabile(self):
        r = _F["mh521_verifica"](_v())
        assert r["id"] == "GAS-STOCC-001"
        assert r["esito"] == "APPLICABILE"
        assert r["motivo"] == ""
        # utile in CFHR 28'000 -> rettifica -28'000, costo 422'000
        assert r["rettifica"] == pytest.approx(-28000.0)
        assert r["costo_rettificato"] == pytest.approx(422000.0)
        assert r["costo_unitario"] == pytest.approx(42.2)

    def test_perdita_cfhr_aumenta_costo(self):
        r = _F["mh521_verifica"](_v(vid="GAS-2", c=-12000.0))
        assert r["esito"] == "APPLICABILE"
        assert r["rettifica"] == pytest.approx(12000.0)
        assert r["costo_rettificato"] == pytest.approx(462000.0)
        assert r["costo_unitario"] == pytest.approx(46.2)

    def test_saldo_zero(self):
        r = _F["mh521_verifica"](_v(vid="GAS-3", c=0.0))
        assert r["esito"] == "APPLICABILE"
        assert r["rettifica"] == 0.0
        assert r["costo_rettificato"] == pytest.approx(450000.0)

    def test_non_applicabile_fair_value(self):
        r = _F["mh521_verifica"](_v(vid="SWP-EL-002", t="fair_value",
                                   nat="finanziario", c=-12000.0))
        assert r["esito"] == "NON_APPLICABILE"
        assert "P&L" in r["motivo"]
        assert r["rettifica"] == 0.0
        assert r["costo_rettificato"] == pytest.approx(450000.0)

    def test_non_applicabile_finanziario(self):
        r = _F["mh521_verifica"](_v(vid="BOND-1", nat="finanziario"))
        assert r["esito"] == "NON_APPLICABILE"
        assert "ricicla" in r["motivo"]

    def test_non_applicabile_forecast(self):
        r = _F["mh521_verifica"](_v(vid="GAS-F", st="forecast"))
        assert r["esito"] == "NON_APPLICABILE"
        assert "forecast" in r["motivo"]

    def test_priorita_motivo(self):
        # fair value + finanziario + forecast -> vince il motivo fair value
        r = _F["mh521_verifica"](_v(vid="X", t="fair_value",
                                   nat="finanziario", st="forecast"))
        assert "P&L" in r["motivo"]

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh521_verifica"]("non un dict")
        with pytest.raises(ValueError):
            _F["mh521_verifica"]({"id": "X"})


class TestW521Riepilogo:
    def test_misto(self):
        a = _F["mh521_riepilogo"](
            [_v(), _v(vid="SWP-EL-002", t="fair_value",
                      nat="finanziario", p=300000.0, q=5000.0,
                      c=-12000.0, d="Swap power in fair value hedge")])
        t = a["totali"]
        assert t["n_voci"] == 2
        assert t["n_applicabili"] == 1
        assert t["n_non_applicabili"] == 1
        # totali solo sulle applicabili
        assert t["totale_prezzi"] == pytest.approx(450000.0)
        assert t["totale_rettifiche"] == pytest.approx(-28000.0)
        assert t["totale_costo_rettificato"] == pytest.approx(422000.0)
        assert t["verdetto_complessivo"] == "MISTO"

    def test_tutte_applicabili(self):
        a = _F["mh521_riepilogo"]([_v(), _v(vid="GAS-2", c=-12000.0)])
        t = a["totali"]
        assert t["verdetto_complessivo"] == "TUTTE_APPLICABILI"
        assert t["n_applicabili"] == 2
        assert t["totale_rettifiche"] == pytest.approx(-28000.0 + 12000.0)
        assert t["totale_costo_rettificato"] == pytest.approx(
            422000.0 + 462000.0)

    def test_nessuna_applicabile(self):
        a = _F["mh521_riepilogo"](
            [_v(vid="A", t="fair_value"), _v(vid="B", st="forecast")])
        t = a["totali"]
        assert t["verdetto_complessivo"] == "NESSUNA_APPLICABILE"
        assert t["totale_costo_rettificato"] == 0.0

    def test_wrapper_parita_verifica(self):
        a = _F["mh521_riepilogo"]([_v()])
        v = _F["mh521_verifica"](_v())
        assert a["righe"][0]["costo_rettificato"] == pytest.approx(
            v["costo_rettificato"])
        assert a["righe"][0]["esito"] == v["esito"]

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh521_riepilogo"]([])
        with pytest.raises(ValueError):
            _F["mh521_riepilogo"]("non una lista")
        with pytest.raises(ValueError):
            _F["mh521_riepilogo"]([_v(vid="A"), _v(vid="A")])


def test_registry_tab521():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 605
    assert TITLE521 in titoli
    assert src.count(TITLE521) == 3
    assert ", tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605 = st.tabs([" in src
    assert "    with tab521:" in src
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    assert "tab521" in dvars
    withs = re.findall(r"    with (tab\d+):", src)
    assert "tab521" in withs
    assert len(withs) == len(dvars) == 605
    # ordine: tab521 dopo tab520
    _decl521 = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    assert _decl521.index(f'"{TITLE520}"') < _decl521.index(f'"{TITLE521}"')
    assert titoli[dvars.index("tab521")] == TITLE521


def test_chiavi_st521_uniche():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(
        encoding="utf-8")
    keys = re.findall(r'key="(st521_[^"]+)"', src) + re.findall(
        r'key=f"(st521_[^"]+)"', src)
    assert len(keys) == len(set(keys)) > 5
