"""Test tab538 '🛡️📑 Informativa rischio di credito (IFRS 7.35)': registry + funzioni pure."""

import math
import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh538_num", "mh538_str", "mh538_int0", "mh538_aging",
           "mh538_posizione", "mh538_demo", "mh538_informativa")

TITLE538 = "🛡️📑 Informativa rischio di credito (IFRS 7.35)"


def _p(pid="P-1", d="x", exp=100000.0, ecl=1000.0, st=1, gs=0):
    return {"id": pid, "descrizione": d, "esposizione_eur": exp,
            "ecl_eur": ecl, "stadio": st, "giorni_scaduto": gs}


class TestW538Validatori:
    def test_num_ok(self):
        assert _F["mh538_num"](2, "x") == 2.0
        assert _F["mh538_num"](-1.5, "x") == -1.5

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh538_num"](bad, "x")

    def test_str_ko(self):
        for bad in ("", "   ", None, 12):
            with pytest.raises(ValueError):
                _F["mh538_str"](bad, "x")

    def test_int0_ok_ko(self):
        assert _F["mh538_int0"](0, "x") == 0
        assert _F["mh538_int0"](120, "x") == 120
        for bad in (True, 1.5, -1, "3", None):
            with pytest.raises(ValueError):
                _F["mh538_int0"](bad, "x")

    def test_aging_buckets(self):
        assert _F["mh538_aging"](0) == "non scaduto"
        assert _F["mh538_aging"](1) == "1-30 gg"
        assert _F["mh538_aging"](30) == "1-30 gg"
        assert _F["mh538_aging"](31) == "31-60 gg"
        assert _F["mh538_aging"](60) == "31-60 gg"
        assert _F["mh538_aging"](61) == "61-90 gg"
        assert _F["mh538_aging"](90) == "61-90 gg"
        assert _F["mh538_aging"](91) == ">90 gg"
        assert _F["mh538_aging"](365) == ">90 gg"

    def test_aging_ko(self):
        for bad in (-1, 1.5, True, None):
            with pytest.raises(ValueError):
                _F["mh538_aging"](bad)


class TestW538Posizione:
    def test_posizione_non_dict(self):
        with pytest.raises(ValueError):
            _F["mh538_posizione"]("x")

    def test_chiave_mancante(self):
        _d = _p()
        del _d["ecl_eur"]
        with pytest.raises(ValueError):
            _F["mh538_posizione"](_d)

    def test_degeneri(self):
        _bad_exp = _p(exp=0.0)
        with pytest.raises(ValueError):
            _F["mh538_posizione"](_bad_exp)
        _neg = _p(ecl=-5.0)
        with pytest.raises(ValueError):
            _F["mh538_posizione"](_neg)
        _over = _p(exp=1000.0, ecl=1001.0)
        with pytest.raises(ValueError):
            _F["mh538_posizione"](_over)
        _st = _p(st=4)
        with pytest.raises(ValueError):
            _F["mh538_posizione"](_st)
        _gs = _p(gs=-1)
        with pytest.raises(ValueError):
            _F["mh538_posizione"](_gs)

    def test_coverage_e_bucket(self):
        _r = _F["mh538_posizione"](_p(exp=200000.0, ecl=4000.0,
                                      st=1, gs=45))
        assert _r["coverage_pct"] == pytest.approx(2.0)
        assert _r["bucket_aging"] == "31-60 gg"
        assert _r["anomalie"] == []

    def test_anomalia_stadio_90gg(self):
        _r = _F["mh538_posizione"](_p(st=1, gs=120))
        assert any("stadio incoerente" in a for a in _r["anomalie"])

    def test_anomalia_coverage_stadio1(self):
        _r = _F["mh538_posizione"](_p(exp=1000.0, ecl=150.0,
                                      st=1, gs=0))
        assert any("stadio 1" in a for a in _r["anomalie"])

    def test_anomalia_ecl_nulla_stadio2(self):
        _r = _F["mh538_posizione"](_p(exp=1000.0, ecl=0.0,
                                      st=2, gs=40))
        assert any("ECL nulla" in a for a in _r["anomalie"])

    def test_anomalia_coverage_bassa_stadio3(self):
        _r = _F["mh538_posizione"](_p(exp=1000.0, ecl=100.0,
                                      st=3, gs=120))
        assert any("stadio 3" in a for a in _r["anomalie"])

    def test_stadio3_coerente(self):
        _r = _F["mh538_posizione"](_p(exp=1000.0, ecl=600.0,
                                      st=3, gs=120))
        assert _r["anomalie"] == []


class TestW538Demo:
    def test_demo_verdetto(self):
        _demo = _F["mh538_demo"]()
        assert len(_demo) == 3
        _an = [_F["mh538_posizione"](_p) for _p in _demo]
        _esiti = [_r["stadio"] for _r in _an]
        assert _esiti == [1, 2, 3]
        assert [p["id"] for p in _demo] == ["PPA-OFF-001", "GO-BRK-002",
                                            "RET-AGG-003"]
        _ri = _F["mh538_informativa"](_an)
        assert _ri["esposizione_totale"] == pytest.approx(1170000.0)
        assert _ri["ecl_totale"] == pytest.approx(82500.0)
        assert _ri["coverage_pct"] == pytest.approx(7.0512820, rel=1e-6)
        assert _ri["esposizione_massima"] == pytest.approx(800000.0)
        assert _ri["quota_max_pct"] == pytest.approx(68.3760683, rel=1e-6)
        assert _ri["quota_stadio3_pct"] == pytest.approx(10.2564102,
                                                        rel=1e-6)
        assert _ri["verdetto"] == "RISCHIO_MEDIO"
        assert _ri["aging"]["non scaduto"] == pytest.approx(800000.0)
        assert _ri["aging"][">90 gg"] == pytest.approx(120000.0)
        assert _ri["n_anomalie"] == 0


class TestW538Informativa:
    def test_verdetto_elevato(self):
        _an = [_F["mh538_posizione"](_p("A", "a", 1000.0, 500.0, 3, 120)),
               _F["mh538_posizione"](_p("B", "b", 3000.0, 10.0, 1, 0))]
        _ri = _F["mh538_informativa"](_an)
        assert _ri["verdetto"] == "RISCHIO_ELEVATO"
        assert _ri["per_stadio"][3]["n"] == 1
        assert _ri["per_stadio"][3]["esposizione"] == pytest.approx(1000.0)

    def test_verdetto_basso(self):
        _an = [_F["mh538_posizione"](_p("A", "a", 5000.0, 50.0, 1, 0))]
        _ri = _F["mh538_informativa"](_an)
        assert _ri["verdetto"] == "RISCHIO_BASSO"

    def test_verdetto_medio_da_anomalia(self):
        _an = [_F["mh538_posizione"](_p("A", "a", 5000.0, 50.0, 1, 100))]
        _ri = _F["mh538_informativa"](_an)
        assert _ri["verdetto"] == "RISCHIO_MEDIO"
        assert _ri["n_anomalie"] == 1

    def test_informativa_ko(self):
        with pytest.raises(ValueError):
            _F["mh538_informativa"]([])
        with pytest.raises(ValueError):
            _F["mh538_informativa"]("x")
        with pytest.raises(ValueError):
            _F["mh538_informativa"]([{"stadio": 9,
                                     "esposizione_eur": 1.0,
                                     "ecl_eur": 0.0,
                                     "bucket_aging": "non scaduto",
                                     "anomalie": []}])


class TestW538Registry:
    def test_titolo_538_presente(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert src.count(TITLE538) == 3

    def test_registry_tab_count_538(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        assert len(re.findall(r"tab\d+", line.split("= st.tabs([")[0])) == 616
        assert len(re.findall(r"^\s*with (tab\d+):", src, re.M)) == 616

    def test_tab538_chain(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        assert ", tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616 = st.tabs([" in src
        assert "with tab538:" in src

    def test_chiavi_st538_uniche(self):
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(
            encoding="utf-8")
        keys = re.findall(r'key=f?"(st538_[^\"]+)"', src)
        assert len(set(keys)) == len(keys) >= 10
