"""Test tab527 '⚖️📉 Ammortamento adeguamento FV hedge (IFRS 9 6.5.10)': registry + funzioni pure."""

import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh527_num", "mh527_str", "mh527_voce", "mh527_misura",
           "mh527_riepilogo")

TITLE527 = "⚖️📉 Ammortamento adeguamento FV hedge (IFRS 9 6.5.10)"
TITLE526 = "⚖️🧺 Posizione netta (IFRS 9 6.6)"


def _v(vid="VOCE-1", adg=120000.0, vc=5000000.0, vita=5.0, eir=4.0,
       voce="amortised", d="x"):
    return {"id": vid, "adeguamento_eur": adg,
            "valore_contabile_eur": vc, "vita_residua_anni": vita,
            "eir_pct": eir, "voce": voce, "descrizione": d}


class TestW527Validatori:
    def test_num_ok(self):
        assert _F["mh527_num"](2, "x") == 2.0
        assert _F["mh527_num"](-1.5, "x") == -1.5
        assert _F["mh527_num"](0.0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, "2", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh527_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh527_str"]("  VOCE-1 ", "x") == "VOCE-1"

    def test_str_ko(self):
        for bad in (None, "", "   ", 5):
            with pytest.raises(ValueError):
                _F["mh527_str"](bad, "x")


class TestW527Voce:
    def test_ok(self):
        r = _F["mh527_voce"](_v())
        assert r["id"] == "VOCE-1"
        assert r["nuovo_valore_contabile"] == pytest.approx(5120000.0)
        assert r["n_anni"] == 5
        assert r["eir_annuo"] == pytest.approx(0.04)

    def test_default_descrizione(self):
        v = _v()
        del v["descrizione"]
        r = _F["mh527_voce"](v)
        assert r["descrizione"] == ""

    def test_vita_arrotondata(self):
        r = _F["mh527_voce"](_v(vita=4.6))
        assert r["n_anni"] == 5

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh527_voce"]("non un dict")
        with pytest.raises(ValueError):
            _F["mh527_voce"]({"id": "X"})
        with pytest.raises(ValueError):
            _F["mh527_voce"](_v(vid="  "))
        with pytest.raises(ValueError):
            _F["mh527_voce"](_v(vc=-1.0))
        with pytest.raises(ValueError):
            _F["mh527_voce"](_v(vita=0.0))
        with pytest.raises(ValueError):
            _F["mh527_voce"](_v(vita=0.4))
        with pytest.raises(ValueError):
            _F["mh527_voce"](_v(eir=-0.1))
        with pytest.raises(ValueError):
            _F["mh527_voce"](_v(eir=100.1))
        with pytest.raises(ValueError):
            _F["mh527_voce"](_v(voce="altro"))
        with pytest.raises(ValueError):
            _F["mh527_voce"](_v(d=5))
        with pytest.raises(ValueError):
            _F["mh527_voce"](_v(adg=float("nan")))


class TestW527Misura:
    def test_nessun_adeguamento(self):
        r = _F["mh527_misura"](_v(adg=0.0))
        assert r["esito"] == "NESSUN_ADEGUAMENTO"
        assert r["piano"] == []
        assert r["importo_pnl_immediato"] == 0.0

    def test_rileva_subito(self):
        r = _F["mh527_misura"](_v(adg=-45000.0, voce="non_amortised"))
        assert r["esito"] == "RILEVA_SUBITO"
        assert r["importo_pnl_immediato"] == pytest.approx(-45000.0)
        assert r["piano"] == []

    def test_ammortizza_piano(self):
        r = _F["mh527_misura"](_v())
        assert r["esito"] == "AMMORTIZZA"
        p = r["piano"]
        assert len(p) == 5
        assert [q["anno"] for q in p] == [1, 2, 3, 4, 5]
        # somma quote = adeguamento esatto
        assert sum(q["ammortamento"] for q in p) == pytest.approx(120000.0)
        # concatenamento apertura/chiusura
        assert p[0]["apertura"] == pytest.approx(120000.0)
        for a, b in zip(p, p[1:]):
            assert a["chiusura"] == pytest.approx(b["apertura"])
        assert abs(p[-1]["chiusura"]) < 1e-6
        assert r["ammortamento_anno1"] == pytest.approx(p[0]["ammortamento"])
        # quote decrescenti con EIR > 0
        assert all(p[i]["ammortamento"] > p[i + 1]["ammortamento"]
                   for i in range(4))

    def test_ammortizza_eir_zero_quote_costanti(self):
        r = _F["mh527_misura"](_v(adg=10000.0, eir=0.0, vita=4.0))
        p = r["piano"]
        assert len(p) == 4
        assert all(q["ammortamento"] == pytest.approx(2500.0) for q in p)

    def test_ammortizza_adeguamento_negativo(self):
        r = _F["mh527_misura"](_v(adg=-50000.0, eir=5.0, vita=2.0))
        p = r["piano"]
        assert sum(q["ammortamento"] for q in p) == pytest.approx(-50000.0)
        assert all(q["ammortamento"] < 0.0 for q in p)

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh527_misura"](_v(voce="bogus"))
        with pytest.raises(ValueError):
            _F["mh527_misura"](_v(vita=-2.0))


class TestW527Riepilogo:
    def _misto(self):
        return [_v("A"), _v("B", adg=-45000.0, voce="non_amortised",
                           vc=800000.0, vita=2.0, eir=0.0)]

    def test_misto(self):
        r = _F["mh527_riepilogo"](self._misto())
        t = r["totali"]
        assert t["n_voci"] == 2
        assert t["n_ammortizza"] == 1
        assert t["n_rileva_subito"] == 1
        assert t["verdetto_complessivo"] == "MISTO"
        assert t["adeguamento_totale_eur"] == pytest.approx(75000.0)
        assert t["pnl_immediato_totale_eur"] == pytest.approx(-45000.0)
        assert t["ammortamento_anno1_totale_eur"] == pytest.approx(
            r["righe"][0]["ammortamento_anno1"])

    def test_tutti_ammortizza(self):
        r = _F["mh527_riepilogo"]([_v("A"), _v("B", adg=5000.0)])
        assert r["totali"]["verdetto_complessivo"] == "TUTTI_AMMORTIZZA"

    def test_tutti_pnl_subito(self):
        r = _F["mh527_riepilogo"](
            [_v("A", adg=1000.0, voce="non_amortised"),
             _v("B", adg=-2000.0, voce="non_amortised")])
        assert r["totali"]["verdetto_complessivo"] == "TUTTI_PNL_SUBITO"
        assert r["totali"]["pnl_immediato_totale_eur"] == pytest.approx(
            -1000.0)

    def test_nessun_adeguamento(self):
        r = _F["mh527_riepilogo"]([_v("A", adg=0.0), _v("B", adg=0.0)])
        assert r["totali"]["verdetto_complessivo"] == "NESSUN_ADEGUAMENTO"

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh527_riepilogo"]([])
        with pytest.raises(ValueError):
            _F["mh527_riepilogo"]("non una lista")
        with pytest.raises(ValueError):
            _F["mh527_riepilogo"]([_v("A"), _v("A")])


def test_registry_tab527():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 607
    assert TITLE527 in titoli
    assert TITLE526 in titoli
    assert src.count(TITLE527) == 3
    assert ", tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607 = st.tabs([" in src
    # chiavi widget st527_* univoche (11 pattern attesi)
    keys = re.findall(r'key=f?"(st527_[^"]+)"', src)
    assert len(set(keys)) == len(keys) >= 11
