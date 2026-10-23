"""Test tab580 "Flussi di cassa futuri coperti (IFRS 7.24C)": registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh580_num", "mh580_str", "mh580_tipo", "mh580_direzione",
           "mh580_fascia", "mh580_strumento", "mh580_demo",
           "mh580_riepilogo")

TITLE580 = "📊📅 Flussi di cassa futuri coperti (IFRS 7.24C)"


def _s(sid="S-1", descrizione="strumento", categoria="Prezzo power",
       tipo="FORWARD", direzione="VENDITA", nominale=50_000.0,
       prezzo=110.0, scadenza=0.25):
    return _F["mh580_strumento"](sid, descrizione, categoria, tipo,
                                 direzione, nominale, prezzo, scadenza)


class TestW580Validatori:
    def test_num_ok(self):
        assert _F["mh580_num"](2, "x") == 2.0
        assert _F["mh580_num"](-3.5, "x") == -3.5
        assert _F["mh580_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh580_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh580_str"]("  abc ", "x") == "abc"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5, b"a"):
            with pytest.raises(ValueError):
                _F["mh580_str"](bad, "x")

    def test_tipo_ok(self):
        assert _F["mh580_tipo"]("forward") == "FORWARD"
        assert _F["mh580_tipo"]("FUTURES") == "FUTURES"
        assert _F["mh580_tipo"]("swap") == "SWAP"
        assert _F["mh580_tipo"]("Option") == "OPTION"

    def test_tipo_ko(self):
        for bad in ("CFD", "", None, 5):
            with pytest.raises(ValueError):
                _F["mh580_tipo"](bad)

    def test_direzione_ok(self):
        assert _F["mh580_direzione"]("acquisto") == "ACQUISTO"
        assert _F["mh580_direzione"]("VENDITA") == "VENDITA"

    def test_direzione_ko(self):
        for bad in ("LONG", "", None, "buy"):
            with pytest.raises(ValueError):
                _F["mh580_direzione"](bad)


class TestW580Fascia:
    def test_bordi(self):
        f = _F["mh580_fascia"]
        assert f(0.1) == "fino a 6 mesi"
        assert f(0.5) == "fino a 6 mesi"
        assert f(0.5001) == "6-12 mesi"
        assert f(1.0) == "6-12 mesi"
        assert f(1.0001) == "1-2 anni"
        assert f(2.0) == "1-2 anni"
        assert f(2.0001) == "2-5 anni"
        assert f(5.0) == "2-5 anni"
        assert f(5.0001) == "oltre 5 anni"
        assert f(10.0) == "oltre 5 anni"


class TestW580Strumento:
    def test_hand_computed(self):
        s = _s()
        assert s["fascia"] == "fino a 6 mesi"
        assert s["completa"] is True
        assert s["anomalie"] == []
        assert s["tipo"] == "FORWARD"
        assert s["direzione"] == "VENDITA"

    def test_anomalia_nominale(self):
        s = _s(nominale=0.0)
        assert s["completa"] is False
        assert any("Nominale" in a for a in s["anomalie"])

    def test_anomalia_prezzo(self):
        s = _s(prezzo=-5.0)
        assert s["completa"] is False
        assert any("Prezzo" in a for a in s["anomalie"])

    def test_anomalia_scadenza(self):
        for bad in (0.0, 11.0):
            s = _s(scadenza=bad)
            assert s["completa"] is False
            assert any("Scadenza" in a for a in s["anomalie"])
        s11 = _s(scadenza=11.0)
        assert s11["fascia"] == "non classificabile"

    def test_ko_tipo_direzione(self):
        with pytest.raises(ValueError):
            _F["mh580_strumento"]("X", "d", "c", "CFD", "VENDITA",
                                  100.0, 10.0, 1.0)
        with pytest.raises(ValueError):
            _F["mh580_strumento"]("X", "d", "c", "FORWARD", "LONG",
                                  100.0, 10.0, 1.0)

    def test_demo(self):
        d = _F["mh580_demo"]()
        assert len(d) == 4
        assert [x["id"] for x in d] == ["S-001", "S-002", "S-003",
                                        "S-004"]
        assert [x["fascia"] for x in d] == ["fino a 6 mesi", "6-12 mesi",
                                            "1-2 anni", "2-5 anni"]
        assert all(x["completa"] for x in d)


class TestW580Riepilogo:
    def test_vuoto(self):
        r = _F["mh580_riepilogo"]([])
        assert r["verdetto"] == "NESSUNO_STRUMENTO"
        assert r["n_strumenti"] == 0
        assert r["fasce"] == []

    def test_demo_distribuito(self):
        r = _F["mh580_riepilogo"](_F["mh580_demo"]())
        assert r["verdetto"] == "PROFILO_DISTRIBUITO"
        assert r["n_strumenti"] == 4
        assert r["n_anomalie"] == 0
        assert r["nominale_totale"] == pytest.approx(110_000.0)
        # 50000*110 + 30000*105 + 20000*42 + 10000*120 = 10690000
        assert r["prezzo_medio_ponderato"] == pytest.approx(
            10_690_000.0 / 110_000.0)
        # 50000*0.25 + 30000*0.75 + 20000*1.5 + 10000*3 = 95000
        assert r["wal_anni"] == pytest.approx(95_000.0 / 110_000.0)
        assert r["quota_max_fascia"] == pytest.approx(
            50_000.0 / 110_000.0)
        assert r["n_acquisto"] == 2
        assert r["n_vendita"] == 2
        f0 = r["fasce"][0]
        assert f0["fascia"] == "fino a 6 mesi"
        assert f0["n_strumenti"] == 1
        assert f0["nominale_mwh"] == pytest.approx(50_000.0)
        assert f0["prezzo_medio"] == pytest.approx(110.0)
        assert f0["wal_anni"] == pytest.approx(0.25)
        assert f0["quota"] == pytest.approx(50_000.0 / 110_000.0)
        f4 = r["fasce"][4]
        assert f4["fascia"] == "oltre 5 anni"
        assert f4["n_strumenti"] == 0
        assert f4["nominale_mwh"] == pytest.approx(0.0)
        assert f4["quota"] == pytest.approx(0.0)

    def test_profilo_concentrato(self):
        r = _F["mh580_riepilogo"]([_s()])
        assert r["verdetto"] == "PROFILO_CONCENTRATO"
        assert r["quota_max_fascia"] == pytest.approx(1.0)

    def test_concentrato_soglia(self):
        # quota 0.7 su una fascia -> soglia inclusiva
        a = _s(sid="A", nominale=7_000.0, scadenza=0.25)
        b = _s(sid="B", nominale=3_000.0, scadenza=0.75)
        r = _F["mh580_riepilogo"]([a, b])
        assert r["quota_max_fascia"] == pytest.approx(0.7)
        assert r["verdetto"] == "PROFILO_CONCENTRATO"
        # quota 0.6999 < 0.7 -> distribuito
        a2 = _s(sid="A", nominale=6_999.0, scadenza=0.25)
        b2 = _s(sid="B", nominale=3_001.0, scadenza=0.75)
        r2 = _F["mh580_riepilogo"]([a2, b2])
        assert r2["quota_max_fascia"] == pytest.approx(
            6_999.0 / 10_000.0)
        assert r2["quota_max_fascia"] < 0.7
        assert r2["verdetto"] == "PROFILO_DISTRIBUITO"

    def test_anomalie_hanno_priorita(self):
        bad = _s(prezzo=-5.0)
        r = _F["mh580_riepilogo"]([bad])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        # lo strumento anomalo non entra nei totali
        assert r["nominale_totale"] == pytest.approx(0.0)

    def test_id_duplicato(self):
        r = _F["mh580_riepilogo"]([_s(), _s()])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 2


class TestW580Registry:
    def test_titolo_presente(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert f'"{TITLE580}"' in src

    def test_conteggio_tab(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", src, re.S)
        titles = re.findall(r'"((?:[^"\\\\]|\\\\.)*)"', m.group(1))
        assert len(titles) == 659
        assert TITLE580 in titles

    def test_chain_tab_var(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert ", tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659 = st.tabs([" in src
        assert "with tab580:" in src

    def test_chiavi_univoche(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        keys = set(re.findall(r"st580_[a-z0-9_]+", src))
        assert len(keys) >= 12, keys
