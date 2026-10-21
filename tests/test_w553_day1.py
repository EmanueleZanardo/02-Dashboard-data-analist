"""Test tab553 'Day-1 P&L differito (IFRS 7.27)': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh553_num", "mh553_str", "mh553_classe", "mh553_voce",
           "mh553_demo", "mh553_riepilogo")

TITLE553 = "📊🕐 Day-1 P&L differito (IFRS 7.27)"


def _v(vid="D-1", d="x", cl="ATTIVITA", ap=1000000.0, nu=200000.0,
       rc=600000.0, es=100000.0):
    return {"id": vid, "descrizione": d, "classe": cl, "apertura": ap,
            "nuovi_differimenti": nu, "riconosciuti_pl": rc,
            "estinzioni": es}


class TestW553Validatori:
    def test_num_ok(self):
        assert _F["mh553_num"](2, "x") == 2.0
        assert _F["mh553_num"](0, "x") == 0.0
        assert _F["mh553_num"](2.5, "x") == 2.5

    def test_num_ko(self):
        for bad in (True, False, "1", None, math.nan, math.inf,
                    -math.inf, -1, -0.01):
            with pytest.raises(ValueError):
                _F["mh553_num"](bad, "x")

    def test_str_ok_ko(self):
        assert _F["mh553_str"]("  abc  ", "x") == "abc"
        for bad in ("", "   ", None, 5, True):
            with pytest.raises(ValueError):
                _F["mh553_str"](bad, "x")

    def test_classe_ok_ko(self):
        for ok in ("ATTIVITA", "PASSIVITA"):
            assert _F["mh553_classe"](ok) == ok
        for bad in ("ATTIVO", "", None, 3, True):
            with pytest.raises(ValueError):
                _F["mh553_classe"](bad)


class TestW553Voce:
    def test_voce_ok(self):
        o = _F["mh553_voce"](_v())
        assert o["chiusura"] == pytest.approx(500000.0)
        assert o["quota_riconosciuta"] == pytest.approx(0.5)
        assert o["anomalie"] == []

    def test_chiusura_zero_den_zero(self):
        o = _F["mh553_voce"](_v(ap=0.0, nu=0.0, rc=0.0, es=0.0))
        assert o["chiusura"] == 0.0
        assert o["quota_riconosciuta"] == 0.0

    def test_voce_ko_struttura(self):
        with pytest.raises(ValueError):
            _F["mh553_voce"]("non-dict")
        with pytest.raises(ValueError):
            _F["mh553_voce"]({"id": "x"})
        with pytest.raises(ValueError):
            _F["mh553_voce"](_v(ap=-1))
        with pytest.raises(ValueError):
            _F["mh553_voce"](_v(nu=math.nan))
        with pytest.raises(ValueError):
            _F["mh553_voce"](_v(cl="ALTRO"))
        with pytest.raises(ValueError):
            _F["mh553_voce"](_v(vid="  "))

    def test_anomalia_chiusura_negativa(self):
        o = _F["mh553_voce"](_v(ap=100000.0, nu=0.0, rc=200000.0,
                                es=50000.0))
        assert any("Chiusura negativa" in a for a in o["anomalie"])
        # riconosciuti oltre il differibile -> anche seconda anomalia
        assert any("oltre il differibile" in a for a in o["anomalie"])

    def test_anomalia_estinzioni_senza_differimento(self):
        o = _F["mh553_voce"](_v(ap=0.0, nu=0.0, rc=0.0, es=100000.0))
        assert any("Estinzioni senza differimento" in a
                   for a in o["anomalie"])

    def test_anomalia_voce_ferma(self):
        o = _F["mh553_voce"](_v(ap=500000.0, nu=0.0, rc=0.0, es=0.0))
        assert any("Voce ferma" in a for a in o["anomalie"])

    def test_nessuna_anomalia_movimenti_normali(self):
        o = _F["mh553_voce"](_v(ap=1000000.0, nu=200000.0, rc=600000.0,
                                es=100000.0))
        assert o["anomalie"] == []


class TestW553Demo:
    def test_demo_struttura(self):
        d = _F["mh553_demo"]()
        assert len(d) == 3
        assert {x["id"] for x in d} == {"DER-PWR-001", "FX-UK-002",
                                       "EQO-DE-003"}

    def test_demo_anomalie_zero(self):
        for v in _F["mh553_demo"]():
            assert _F["mh553_voce"](v)["anomalie"] == []

    def test_demo_riconciliazione(self):
        # apertura 4.3M + nuovi 0.9M - riconosciuti 2.5M - estinzioni 0.4M
        r = _F["mh553_riepilogo"](_F["mh553_demo"]())
        assert r["apertura_tot"] == pytest.approx(4300000.0)
        assert r["nuovi_tot"] == pytest.approx(900000.0)
        assert r["riconosciuti_tot"] == pytest.approx(2500000.0)
        assert r["estinzioni_tot"] == pytest.approx(400000.0)
        assert r["chiusura_tot"] == pytest.approx(2300000.0)
        assert r["quota_riconosciuta"] == pytest.approx(2500000.0 /
                                                      5200000.0)
        assert r["verdetto"] == "DIFFERIMENTI_IN_CONSUMO"
        assert r["n_anomalie"] == 0
        assert r["per_classe"]["ATTIVITA"]["chiusura"] == \
            pytest.approx(1500000.0)
        assert r["per_classe"]["PASSIVITA"]["n"] == 1


class TestW553Riepilogo:
    def test_verdetto_teso(self):
        r = _F["mh553_riepilogo"]([_v(ap=1000000.0, nu=0.0, rc=800000.0,
                                      es=0.0)], 0.70, 0.40)
        assert r["verdetto"] == "RICONOSCIMENTI_TESI"
        assert r["quota_riconosciuta"] == pytest.approx(0.8)

    def test_verdetto_stabile(self):
        r = _F["mh553_riepilogo"]([_v(ap=1000000.0, nu=0.0, rc=100000.0,
                                      es=0.0)], 0.70, 0.40)
        assert r["verdetto"] == "DIFFERIMENTI_STABILI"

    def test_verdetto_soglie_custom(self):
        r = _F["mh553_riepilogo"]([_v(ap=1000000.0, nu=0.0, rc=500000.0,
                                      es=0.0)], 0.40, 0.30)
        assert r["verdetto"] == "RICONOSCIMENTI_TESI"

    def test_verdetto_nessuna(self):
        r = _F["mh553_riepilogo"]([_v(ap=0.0, nu=0.0, rc=0.0, es=0.0)])
        assert r["verdetto"] == "NESSUNA_VOCE"

    def test_verdetto_anomalie(self):
        r = _F["mh553_riepilogo"]([_v(ap=100000.0, nu=0.0, rc=200000.0,
                                      es=50000.0)])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] >= 1

    def test_riepilogo_ko(self):
        for bad in ([], "x", None):
            with pytest.raises(ValueError):
                _F["mh553_riepilogo"](bad)
        for st_, sv_ in ((0.0, 0.40), (1.5, 0.40), (-0.1, 0.40),
                         (0.40, 0.40), (0.30, 0.40), ("0.7", 0.40),
                         (True, 0.40), (math.nan, 0.40)):
            with pytest.raises(ValueError):
                _F["mh553_riepilogo"]([_v()], st_, sv_)


class TestW553Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_titolo_553_presente(self):
        assert self._src().count(TITLE553) == 3

    def test_counts_553(self):
        src = self._src()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        assert "\n" not in line
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"    with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 613
        assert TITLE553 in titoli
        assert "tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613 = st.tabs([" in src

    def test_chiavi_553_univoche(self):
        src = self._src()
        righe = [ln for ln in src.split("\n")
                 if "key=" in ln and "st553_" in ln]
        # le f-string st553_id_{_i553} generano istanze a runtime: la base
        # e' fino al suffisso numerico; csv1/csv2 sono chiavi distinte
        basi = []
        for ln in righe:
            basi.append(re.search(r"st553_[a-z]+\d*", ln).group(0))
        assert len(basi) == len(set(basi))
        assert len(basi) >= 13
