"""Test tab531 '⚖️📶 Gerarchia fair value (IFRS 13)': registry + funzioni pure."""

import math
import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh531_num", "mh531_str", "mh531_bool", "mh531_strumento",
           "mh531_livello", "mh531_riepilogo")

TITLE531 = "⚖️📶 Gerarchia fair value (IFRS 13)"
TITLE530 = "🔗📄 Derivati incorporati (IFRS 9 4.3)"


def _s(cid="S-1", tipo="future_quotato", ma=True, io=True, oriz=1.0,
       fv=1000.0, tec="market", d="x"):
    return {"id": cid, "tipo_strumento": tipo, "mercato_attivo": ma,
            "input_osservabili": io, "orizzonte_anni": oriz,
            "fair_value_eur": fv, "tecnica_valutazione": tec,
            "descrizione": d}


class TestW531Validatori:
    def test_num_ok(self):
        assert _F["mh531_num"](2, "x") == 2.0
        assert _F["mh531_num"](-1.5, "x") == -1.5
        assert _F["mh531_num"](0.0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, False, "1", None, math.nan, math.inf, -math.inf):
            with pytest.raises(ValueError):
                _F["mh531_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh531_str"]("  S-1 ", "x") == "S-1"

    def test_str_ko(self):
        for bad in ("", "   ", None, 12):
            with pytest.raises(ValueError):
                _F["mh531_str"](bad, "x")

    def test_bool_ok(self):
        assert _F["mh531_bool"](True, "x") is True
        assert _F["mh531_bool"](False, "x") is False

    def test_bool_ko(self):
        for bad in (1, 0, "true", None):
            with pytest.raises(ValueError):
                _F["mh531_bool"](bad, "x")


class TestW531Strumento:
    def test_strumento_ok(self):
        s = _F["mh531_strumento"](_s(cid=" FUT-1 "))
        assert s["id"] == "FUT-1"
        assert s["orizzonte_anni"] == 1.0
        assert s["fair_value_eur"] == 1000.0

    def test_strumento_chiave_mancante(self):
        v = _s()
        del v["orizzonte_anni"]
        with pytest.raises(ValueError):
            _F["mh531_strumento"](v)

    def test_strumento_ko(self):
        with pytest.raises(ValueError):
            _F["mh531_strumento"]("no")
        with pytest.raises(ValueError):
            _F["mh531_strumento"](_s(tipo="bond"))
        with pytest.raises(ValueError):
            _F["mh531_strumento"](_s(tec="dcf"))
        with pytest.raises(ValueError):
            _F["mh531_strumento"](_s(oriz=-1.0))
        with pytest.raises(ValueError):
            _F["mh531_strumento"](_s(ma=1))
        with pytest.raises(ValueError):
            _F["mh531_strumento"](_s(cid=""))


class TestW531Livello:
    def test_livello_1(self):
        r = _F["mh531_livello"](_s(tipo="future_quotato", ma=True))
        assert r["livello"] == 1
        assert "13.76" in r["motivo"]

    def test_livello_1_richiede_future_quotato(self):
        # opzione vanilla con mercato attivo ma non future -> non L1
        r = _F["mh531_livello"](_s(tipo="opzione_vanilla", ma=True, io=True))
        assert r["livello"] == 2

    def test_livello_2(self):
        r = _F["mh531_livello"](_s(tipo="forward_otc", ma=False, io=True,
                                  oriz=2.5))
        assert r["livello"] == 2
        assert "13.81" in r["motivo"]

    def test_livello_3_no_input_osservabili(self):
        r = _F["mh531_livello"](_s(tipo="ppa_lungo_termine", ma=False,
                                  io=False, oriz=8.0, fv=-80000.0))
        assert r["livello"] == 3
        assert "13.86" in r["motivo"]

    def test_livello_3_oltre_soglia(self):
        r = _F["mh531_livello"](_s(tipo="tolling", ma=False, io=True,
                                  oriz=5.0), 3.0)
        assert r["livello"] == 3
        assert "13.87" in r["motivo"]

    def test_livello_boundary_soglia(self):
        # orizzonte == soglia -> resta L2
        r = _F["mh531_livello"](_s(tipo="forward_otc", ma=False, io=True,
                                  oriz=3.0), 3.0)
        assert r["livello"] == 2

    def test_livello_soglia_degenere(self):
        with pytest.raises(ValueError):
            _F["mh531_livello"](_s(), 0.0)
        with pytest.raises(ValueError):
            _F["mh531_livello"](_s(), -2.0)


class TestW531Riepilogo:
    def test_riepilogo_misto(self):
        rows = [_s("A", "future_quotato", True, True, 1.0, 120000.0),
                _s("B", "forward_otc", False, True, 2.5, 35000.0),
                _s("C", "ppa_lungo_termine", False, False, 8.0, -80000.0)]
        an = _F["mh531_riepilogo"](rows, 3.0)
        t = an["totali"]
        assert t["n_strumenti"] == 3
        assert (t["n_l1"], t["n_l2"], t["n_l3"]) == (1, 1, 1)
        assert t["fv_l1_eur"] == 120000.0
        assert t["fv_l2_eur"] == 35000.0
        assert t["fv_l3_eur"] == -80000.0
        assert t["fv_totale_eur"] == 75000.0
        assert t["pct_fv_l3"] == pytest.approx(106.6666666)
        assert t["verdetto"] == "CON_LIVELLO_3"
        assert [r["id"] for r in an["righe"]] == ["A", "B", "C"]

    def test_riepilogo_verdetti(self):
        assert _F["mh531_riepilogo"](
            [_s("A", "future_quotato", True, True, 1.0, 1.0)],
            3.0)["totali"]["verdetto"] == "TUTTO_LIVELLO_1"
        assert _F["mh531_riepilogo"](
            [_s("A", "forward_otc", False, True, 1.0, 1.0)],
            3.0)["totali"]["verdetto"] == "NESSUN_LIVELLO_3"

    def test_riepilogo_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh531_riepilogo"]([], 3.0)
        with pytest.raises(ValueError):
            _F["mh531_riepilogo"](
                [_s("D"), _s("D")], 3.0)


class TestW531Registry:
    def test_titolo_531_presente(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert src.count(TITLE531) == 3

    def test_registry_tab_count_531(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        assert len(re.findall(r"tab\d+", line.split("= st.tabs([")[0])) == 580
        assert len(re.findall(r"^\s*with (tab\d+):", src, re.M)) == 580

    def test_tab531_chain(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert ", tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580 = st.tabs([" in src
        assert "with tab531:" in src

    def test_chiavi_st531_uniche(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        keys = re.findall(r'key=f?"(st531_[^"]+)"', src)
        assert len(set(keys)) == len(keys) >= 10
