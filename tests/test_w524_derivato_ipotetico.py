"""Test tab524 '🧪📐 Derivato ipotetico (IFRS 9 B6.5.5)': registry + funzioni pure."""

import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh524_num", "mh524_str", "mh524_periodo", "mh524_misura",
           "mh524_riepilogo")

TITLE524 = "🧪📐 Derivato ipotetico (IFRS 9 B6.5.5)"
TITLE523 = "🔀📊 Tipo di copertura (IFRS 9 6.5.2)"


def _p(pid="DER-IPO-2026-Q3", qta=10000.0, dp=2.50, dreal=-20000.0,
       tipo="cash_flow", d="Acquisto forecast gas"):
    return {"id": pid, "qta_item_mwh": qta, "delta_p_item": dp,
            "delta_fv_strumento": dreal, "tipo": tipo, "descrizione": d}


class TestW524Validatori:
    def test_num_ok(self):
        assert _F["mh524_num"](2, "x") == 2.0
        assert _F["mh524_num"](-1.5, "x") == -1.5
        assert _F["mh524_num"](0.0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, "2", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh524_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh524_str"]("  DER-1 ", "x") == "DER-1"

    def test_str_ko(self):
        for bad in (None, "", "   ", 5):
            with pytest.raises(ValueError):
                _F["mh524_str"](bad, "x")


class TestW524Periodo:
    def test_ok(self):
        p = _F["mh524_periodo"](_p())
        assert p["id"] == "DER-IPO-2026-Q3"
        assert p["qta_item_mwh"] == pytest.approx(10000.0)
        assert p["delta_p_item"] == pytest.approx(2.50)
        assert p["delta_fv_strumento"] == pytest.approx(-20000.0)
        assert p["tipo"] == "cash_flow"
        assert p["descrizione"] == "Acquisto forecast gas"
        assert p["delta_fv_item"] == pytest.approx(25000.0)

    def test_default_tipo_desc(self):
        d = _p()
        del d["tipo"]
        del d["descrizione"]
        p = _F["mh524_periodo"](d)
        assert p["tipo"] == "cash_flow"
        assert p["descrizione"] == ""

    def test_qta_ko(self):
        for bad in (0, -100, True, "1000", float("nan")):
            with pytest.raises(ValueError):
                _F["mh524_periodo"](_p(qta=bad))

    def test_dp_dreal_ko(self):
        for bad in (True, "2.5", None, float("inf")):
            with pytest.raises(ValueError):
                _F["mh524_periodo"](_p(dp=bad))
            with pytest.raises(ValueError):
                _F["mh524_periodo"](_p(dreal=bad))

    def test_tipo_ko(self):
        for bad in ("fair", "", None):
            with pytest.raises(ValueError):
                _F["mh524_periodo"](_p(tipo=bad))

    def test_chiave_mancante(self):
        d = _p()
        del d["delta_p_item"]
        with pytest.raises(ValueError):
            _F["mh524_periodo"](d)

    def test_non_dict(self):
        with pytest.raises(ValueError):
            _F["mh524_periodo"](["id"])

    def test_id_vuoto(self):
        with pytest.raises(ValueError):
            _F["mh524_periodo"](_p(pid="  "))

    def test_descrizione_non_str(self):
        with pytest.raises(ValueError):
            _F["mh524_periodo"](_p(d=5))


class TestW524Misura:
    def test_efficace_80_boundary(self):
        # d_item = 25000, d_real = -20000 -> offset 0.80 EFFICACE
        r = _F["mh524_misura"](_p())
        assert r["delta_fv_item"] == pytest.approx(25000.0)
        assert r["delta_fv_ipotetico"] == pytest.approx(-25000.0)
        assert r["offset"] == pytest.approx(0.80)
        assert r["offset_pct"] == pytest.approx(80.0)
        assert r["esito"] == "EFFICACE"
        assert r["motivo"] == ""
        assert r["inefficacia"] == pytest.approx(5000.0)
        assert r["quota_efficace"] == pytest.approx(-25000.0)
        assert r["destinazione"] == "OCI (riserva CFHR)"

    def test_efficace_100(self):
        r = _F["mh524_misura"](_p(pid="A", qta=1000.0, dp=10.0,
                                  dreal=-10000.0))
        assert r["offset"] == pytest.approx(1.0)
        assert r["esito"] == "EFFICACE"
        assert r["inefficacia"] == pytest.approx(0.0)

    def test_efficace_125_boundary(self):
        r = _F["mh524_misura"](_p(pid="A", qta=1000.0, dp=10.0,
                                  dreal=-12500.0))
        assert r["offset"] == pytest.approx(1.25)
        assert r["esito"] == "EFFICACE"

    def test_inefficace_sotto_80(self):
        r = _F["mh524_misura"](_p(pid="B", qta=10000.0, dp=2.50,
                                  dreal=-12500.0))
        assert r["offset"] == pytest.approx(0.50)
        assert r["esito"] == "INEFFICACE"
        assert "sottocopertura" in r["motivo"]
        assert "50.0%" in r["motivo"]
        assert r["inefficacia"] == pytest.approx(12500.0)

    def test_inefficace_sopra_125(self):
        r = _F["mh524_misura"](_p(pid="C", qta=1000.0, dp=10.0,
                                  dreal=-13000.0))
        assert r["offset"] == pytest.approx(1.3)
        assert r["esito"] == "INEFFICACE"
        assert "sovracopertura" in r["motivo"]

    def test_inefficace_segno_opposto(self):
        # strumento si muove COME l'item: peggiora invece di compensare
        r = _F["mh524_misura"](_p(pid="D", qta=1000.0, dp=10.0,
                                  dreal=5000.0))
        assert r["offset"] == pytest.approx(-0.5)
        assert r["esito"] == "INEFFICACE"
        assert r["inefficacia"] == pytest.approx(15000.0)

    def test_fair_value_destinazione(self):
        r = _F["mh524_misura"](_p(tipo="fair_value"))
        assert r["destinazione"] == "P&L (adeguamento carrying amount)"
        assert r["esito"] == "EFFICACE"

    def test_non_misurabile(self):
        r = _F["mh524_misura"](_p(pid="E", qta=1000.0, dp=0.0,
                                  dreal=0.0))
        assert r["esito"] == "NON_MISURABILE"
        assert r["offset"] is None
        assert r["offset_pct"] is None
        assert r["inefficacia"] == pytest.approx(0.0)

    def test_item_fermo_strumento_mosso(self):
        r = _F["mh524_misura"](_p(pid="F", qta=1000.0, dp=0.0,
                                  dreal=-500.0))
        assert r["esito"] == "INEFFICACE"
        assert r["offset"] is None
        assert r["inefficacia"] == pytest.approx(-500.0)
        assert "item fermo" in r["motivo"]

    def test_delta_p_negativo(self):
        # prezzo scende: item perde, lo strumento deve guadagnare
        r = _F["mh524_misura"](_p(pid="G", qta=1000.0, dp=-10.0,
                                  dreal=8000.0))
        assert r["delta_fv_item"] == pytest.approx(-10000.0)
        assert r["offset"] == pytest.approx(0.80)
        assert r["esito"] == "EFFICACE"
        assert r["inefficacia"] == pytest.approx(-2000.0)

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh524_misura"]("non un dict")
        with pytest.raises(ValueError):
            _F["mh524_misura"]({"id": "X"})


class TestW524Riepilogo:
    def test_misto(self):
        a = _F["mh524_riepilogo"](
            [_p(), _p(pid="DER-IPO-2026-Q4", dreal=-12500.0,
                      d="Swap sottodimensionato")])
        t = a["totali"]
        assert t["n_periodi"] == 2
        assert t["n_efficaci"] == 1
        assert t["n_inefficaci"] == 1
        assert t["n_non_misurabili"] == 0
        assert t["inefficacia_totale"] == pytest.approx(17500.0)
        assert t["inefficacia_media"] == pytest.approx(8750.0)
        assert t["quota_efficace_totale"] == pytest.approx(-50000.0)
        assert t["offset_medio"] == pytest.approx(0.65)
        assert t["verdetto_complessivo"] == "MISTO"

    def test_sempre_efficace(self):
        a = _F["mh524_riepilogo"](
            [_p(), _p(pid="H2", qta=1000.0, dp=10.0, dreal=-10000.0)])
        assert a["totali"]["verdetto_complessivo"] == "SEMPRE_EFFICACE"
        assert a["totali"]["n_efficaci"] == 2
        assert a["totali"]["inefficacia_totale"] == pytest.approx(5000.0)

    def test_mai_efficace(self):
        a = _F["mh524_riepilogo"](
            [_p(pid="I1", qta=1000.0, dp=10.0, dreal=-5000.0),
             _p(pid="I2", qta=1000.0, dp=0.0, dreal=0.0)])
        t = a["totali"]
        assert t["verdetto_complessivo"] == "MAI_EFFICACE"
        assert t["n_efficaci"] == 0
        assert t["n_non_misurabili"] == 1
        # offset medio solo sul periodo misurabile
        assert t["offset_medio"] == pytest.approx(0.5)

    def test_wrapper_parita_misura(self):
        a = _F["mh524_riepilogo"]([_p()])
        v = _F["mh524_misura"](_p())
        assert a["righe"][0]["offset"] == pytest.approx(v["offset"])
        assert a["righe"][0]["esito"] == v["esito"]
        assert a["righe"][0]["inefficacia"] == pytest.approx(
            v["inefficacia"])

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh524_riepilogo"]([])
        with pytest.raises(ValueError):
            _F["mh524_riepilogo"]("non una lista")
        with pytest.raises(ValueError):
            _F["mh524_riepilogo"]([_p(pid="A"), _p(pid="A")])


def test_registry_tab524():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 527
    assert TITLE524 in titoli
    assert TITLE523 in titoli
    assert src.count(TITLE524) == 3
    assert ", tab523, tab524, tab525, tab526, tab527 = st.tabs([" in src
