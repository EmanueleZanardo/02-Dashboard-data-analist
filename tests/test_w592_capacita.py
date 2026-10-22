"""Test tab592 "⚡🏛️ Asta del mercato della capacità: clearing e de-rating": registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh592_num", "mh592_pos", "mh592_nneg", "mh592_pct",
           "mh592_str", "mh592_unita", "mh592_domanda",
           "mh592_prezzo_domanda", "mh592_clearing", "mh592_riepilogo",
           "mh592_demo")

TITLE592 = "⚡🏛️ Asta del mercato della capacità: clearing e de-rating"

DEMO_U = [_F["mh592_unita"](*_r)
          for _r in _F["mh592_demo"]()["unita"]]
DEMO_D = {"target_mw": 600.0, "pmax": 75.0}


class TestW592Validatori:
    def test_num_ok(self):
        assert _F["mh592_num"](2, "x") == 2.0
        assert _F["mh592_num"](-3.5, "x") == -3.5

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh592_num"](bad, "x")

    def test_pos_ko(self):
        for bad in (0, -1.5):
            with pytest.raises(ValueError):
                _F["mh592_pos"](bad, "x")
        assert _F["mh592_pos"](0.5, "x") == 0.5

    def test_nneg_ko(self):
        with pytest.raises(ValueError):
            _F["mh592_nneg"](-0.1, "x")
        assert _F["mh592_nneg"](0, "x") == 0.0

    def test_pct_ko(self):
        for bad in (-0.1, 100.1):
            with pytest.raises(ValueError):
                _F["mh592_pct"](bad, "x")
        assert _F["mh592_pct"](0, "x") == 0.0
        assert _F["mh592_pct"](100, "x") == 100.0

    def test_str_ok_ko(self):
        assert _F["mh592_str"]("  a ", "x") == "a"
        for bad in ("", "   ", 5, None):
            with pytest.raises(ValueError):
                _F["mh592_str"](bad, "x")

    def test_unita_ok(self):
        u = _F["mh592_unita"](" U1 ", "CCGT", 400, 90, 12)
        assert u == {"id": "U1", "descr": "CCGT", "targa_mw": 400.0,
                     "derating_pct": 90.0, "offerta": 12.0,
                     "derated_mw": 360.0}

    def test_unita_ko(self):
        with pytest.raises(ValueError):
            _F["mh592_unita"]("U1", "d", 0, 90, 12)       # targa <= 0
        with pytest.raises(ValueError):
            _F["mh592_unita"]("U1", "d", 100, 101, 12)    # derating > 100
        with pytest.raises(ValueError):
            _F["mh592_unita"]("U1", "d", 100, 90, -1)     # bid < 0
        with pytest.raises(ValueError):
            _F["mh592_unita"]("", "d", 100, 90, 12)       # id vuoto

    def test_domanda_ko(self):
        with pytest.raises(ValueError):
            _F["mh592_domanda"](0, 75)
        with pytest.raises(ValueError):
            _F["mh592_domanda"](600, 0)


class TestW592Domanda:
    def test_bordi(self):
        assert _F["mh592_prezzo_domanda"](0.0, DEMO_D) == 75.0
        assert _F["mh592_prezzo_domanda"](600.0, DEMO_D) == 0.0
        assert _F["mh592_prezzo_domanda"](1200.0, DEMO_D) == 0.0

    def test_lineare(self):
        assert _F["mh592_prezzo_domanda"](300.0, DEMO_D) == pytest.approx(37.5)
        assert _F["mh592_prezzo_domanda"](150.0, DEMO_D) == pytest.approx(56.25)


class TestW592Clearing:
    def _u(self, uid, targa, der, bid, descr="d"):
        return _F["mh592_unita"](uid, descr, targa, der, bid)

    def test_demo_hand_computed(self):
        # Ordine di merito: CC1(12,360) -> DR1(18,40) -> ST1(25,50) -> OC1(55,190)
        # Confronto a INIZIO blocco (unità marginale = scalino che incrocia
        # la domanda): CC1: P(0)=75 >= 12 ok; DR1: P(360)=30 >= 18 ok;
        # ST1: P(400)=25 >= 25 ok (marginale, fissa il prezzo);
        # OC1: P(450)=18.75 < 55 stop.
        r = _F["mh592_clearing"](DEMO_U, DEMO_D)
        assert [u["id"] for u in r["accettate"]] == ["CC1", "DR1", "ST1"]
        assert [u["id"] for u in r["rifiutate"]] == ["OC1"]
        assert r["prezzo_clearing"] == pytest.approx(25.0)
        assert r["q_accettata_mw"] == pytest.approx(450.0)
        assert r["deficit_mw"] == pytest.approx(150.0)
        assert r["verdetto"] == "COPERTURA_PARZIALE"
        assert r["costo_totale_eur_anno"] == pytest.approx(25.0 * 450 * 1000)
        assert not r["prezzo_al_cap"]
        cc1 = r["accettate"][0]
        assert cc1["margine_eur_anno"] == pytest.approx(360 * 1000 * (25 - 12))
        st1 = r["accettate"][2]
        assert st1["margine_eur_anno"] == pytest.approx(0.0)  # marginale

    def test_piena_copertura(self):
        # A fissa il prezzo (20), B chiude il fabbisogno a bid 0.
        uu = [self._u("A", 60, 100, 20), self._u("B", 50, 100, 0)]
        r = _F["mh592_clearing"](uu, _F["mh592_domanda"](100, 50))
        assert r["verdetto"] == "PIENA_COPERTURA"
        assert r["q_accettata_mw"] == pytest.approx(110.0)
        assert r["deficit_mw"] == pytest.approx(0.0)
        assert r["prezzo_clearing"] == pytest.approx(20.0)

    def test_nessuna_accettazione(self):
        uu = [self._u("A", 10, 100, 100)]
        r = _F["mh592_clearing"](uu, _F["mh592_domanda"](100, 50))
        assert r["verdetto"] == "NESSUNA_ACCETTAZIONE"
        assert r["prezzo_clearing"] == 0.0
        assert r["q_accettata_mw"] == pytest.approx(0.0)

    def test_prezzo_al_cap(self):
        # Unità a derating 0: Q cumulata resta 0, P(0) = Pmax -> bid=Pmax passa.
        uu = [self._u("A", 100, 0, 50)]
        r = _F["mh592_clearing"](uu, _F["mh592_domanda"](100, 50))
        assert r["prezzo_clearing"] == pytest.approx(50.0)
        assert r["prezzo_al_cap"] is True

    def test_tie_break_deterministico(self):
        uu = [self._u("piccola", 50, 100, 10),
              self._u("grande", 100, 100, 10)]
        r = _F["mh592_clearing"](uu, _F["mh592_domanda"](1000, 50))
        assert [u["id"] for u in r["accettate"]] == ["grande", "piccola"]

    def test_stop_al_primo_rifiuto(self):
        # B rifiutata: C ha bid maggiore e non può passare dopo.
        uu = [self._u("A", 10, 100, 5), self._u("B", 500, 100, 60),
              self._u("C", 10, 100, 61)]
        r = _F["mh592_clearing"](uu, _F["mh592_domanda"](100, 50))
        assert [u["id"] for u in r["accettate"]] == ["A"]
        assert [u["id"] for u in r["rifiutate"]] == ["B", "C"]

    def test_id_duplicati_e_vuota(self):
        uu = [self._u("A", 10, 100, 5), self._u("A", 10, 100, 6)]
        with pytest.raises(ValueError):
            _F["mh592_clearing"](uu, _F["mh592_domanda"](100, 50))
        with pytest.raises(ValueError):
            _F["mh592_clearing"]([], _F["mh592_domanda"](100, 50))

    def test_riepilogo(self):
        r = _F["mh592_clearing"](DEMO_U, DEMO_D)
        s = _F["mh592_riepilogo"](r)
        assert "COPERTURA_PARZIALE" in s
        assert "25.00" in s


class TestW592Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 628
        assert TITLE592 in titles
        assert TITLE592 in titles

    def test_chain(self):
        assert ", tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628 = st.tabs([" in self._src()
        assert "with tab592:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st592_[a-z0-9_]+", self._src()))
        assert len(keys) >= 12, keys
