"""Test tab557 'Concentrazioni di rischio (IFRS 7.32)': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh557_num", "mh557_str", "mh557_ge0", "mh557_tipo",
           "mh557_concentrazione", "mh557_demo", "mh557_riepilogo")

TITLE557 = "🗂️⚠️ Concentrazioni di rischio (IFRS 7.32)"


def _mk(cid="C-1", tipo="RISCHIO_CREDITO", car="x", det="y", esp=1000000.0):
    return _F["mh557_concentrazione"](cid, tipo, car, det, esp)


class TestW557Validatori:
    def test_num_ok(self):
        assert _F["mh557_num"](2, "x") == 2.0
        assert _F["mh557_num"](0, "x") == 0.0
        assert _F["mh557_num"](2.5, "x") == 2.5

    def test_num_ko(self):
        for bad in (True, False, "1", None, math.nan, math.inf,
                    -math.inf, -1, -0.01):
            with pytest.raises(ValueError):
                _F["mh557_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh557_str"]("  abc  ", "x") == "abc"

    def test_str_ko(self):
        for bad in (None, 1, "", "   "):
            with pytest.raises(ValueError):
                _F["mh557_str"](bad, "x")

    def test_tipo_ok(self):
        assert _F["mh557_tipo"]("rischio_credito") == "RISCHIO_CREDITO"
        assert _F["mh557_tipo"]("RISCHIO_MERCATO") == "RISCHIO_MERCATO"
        assert _F["mh557_tipo"]("RISCHIO_LIQUIDITA") == "RISCHIO_LIQUIDITA"

    def test_tipo_ko(self):
        for bad in (None, "CREDITO", "", "RISCHIO_OPERATIVO"):
            with pytest.raises(ValueError):
                _F["mh557_tipo"](bad)


class TestW557Concentrazione:
    def test_ok(self):
        c = _mk("CONC-1", "RISCHIO_MERCATO", "Hub TTF", "open position",
                5e6)
        assert c == {"id": "CONC-1", "tipo": "RISCHIO_MERCATO",
                     "caratteristica": "Hub TTF",
                     "determinazione": "open position",
                     "esposizione_lorda": 5000000.0}

    def test_ko(self):
        with pytest.raises(ValueError):
            _mk(cid="  ")
        with pytest.raises(ValueError):
            _mk(tipo="ALTRO")
        with pytest.raises(ValueError):
            _mk(car="")
        with pytest.raises(ValueError):
            _mk(det="  ")
        with pytest.raises(ValueError):
            _mk(esp=-1)


class TestW557Riepilogo:
    def test_demo(self):
        cs = _F["mh557_demo"]()
        assert len(cs) == 4
        r = _F["mh557_riepilogo"](cs)
        assert r["verdetto"] == "CONCENTRAZIONE_DOMINANTE"
        assert r["esposizione_lorda_totale"] == 22700000.0
        assert r["n_concentrazioni"] == 4
        assert r["n_dominanti"] == 3
        assert r["n_anomalie"] == 0
        assert r["hhi_max"] == pytest.approx(1.0)

    def test_demo_quote_e_status(self):
        r = _F["mh557_riepilogo"](_F["mh557_demo"]())
        per_id = {o["id"]: o for o in r["analizzate"]}
        assert per_id["CONC-001"]["quota"] == pytest.approx(9600000 / 13000000)
        assert per_id["CONC-001"]["status"] == "DOMINANTE"
        assert per_id["CONC-002"]["status"] == "SIGNIFICATIVA"
        hhi_cr = r["per_tipo"]["RISCHIO_CREDITO"]["hhi"]
        assert hhi_cr == pytest.approx((9600000 / 13000000) ** 2 +
                                       (3400000 / 13000000) ** 2)

    def test_anomalia_duplicata(self):
        cs = [_mk("A", car="Offtaker X", det="d", esp=1e6),
              _mk("B", car="offtaker x", det="d", esp=2e6)]
        r = _F["mh557_riepilogo"](cs)
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 1
        assert "duplicata" in r["analizzate"][1]["anomalie"][0]

    def test_stessa_caratteristica_tipo_diverso_ok(self):
        cs = [_mk("A", tipo="RISCHIO_CREDITO", car="X", det="d", esp=1e6),
              _mk("B", tipo="RISCHIO_MERCATO", car="X", det="d", esp=1e6)]
        r = _F["mh557_riepilogo"](cs)
        assert r["n_anomalie"] == 0

    def test_anomalia_esposizione_nulla(self):
        cs = [_mk("A", esp=0.0), _mk("B", esp=2e6)]
        r = _F["mh557_riepilogo"](cs)
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert any("nulla" in a for a in r["analizzate"][0]["anomalie"])

    def test_nessuna_concentrazione(self):
        cs = [_mk("A", esp=0.0), _mk("B", esp=0.0)]
        r = _F["mh557_riepilogo"](cs)
        # esp 0 -> anomalia, ma totale 0 -> NESSUNA_CONCENTRAZIONE prevale
        assert r["verdetto"] == "NESSUNA_CONCENTRAZIONE"

    def test_lista_vuota(self):
        with pytest.raises(ValueError):
            _F["mh557_riepilogo"]([])

    def test_soglie_degeneri(self):
        cs = _F["mh557_demo"]()
        for bad in (0, 1, -0.1, 1.5, "x"):
            with pytest.raises(ValueError):
                _F["mh557_riepilogo"](cs, soglia_dominante=bad)

    def test_soglia_personalizzata(self):
        # soglia 80%: solo le concentrazioni uniche per tipo dominano
        r = _F["mh557_riepilogo"](_F["mh557_demo"](),
                                  soglia_dominante=0.80)
        assert r["n_dominanti"] == 2
        per_id = {o["id"]: o for o in r["analizzate"]}
        assert per_id["CONC-001"]["status"] == "SIGNIFICATIVA"

    def test_diffusa(self):
        cs = [_mk("A", car="offtaker X", esp=6e6),
              _mk("B", car="offtaker Y", esp=4e6)]
        r = _F["mh557_riepilogo"](cs, soglia_dominante=0.99)
        assert r["verdetto"] == "CONCENTRAZIONE_DIFFUSA"
        assert r["n_dominanti"] == 0
        assert r["per_tipo"]["RISCHIO_CREDITO"]["hhi"] == \
            pytest.approx(0.6 ** 2 + 0.4 ** 2)

    def test_boundary_dominanza(self):
        # quota esattamente sulla soglia -> DOMINANTE (>=)
        cs = [_mk("A", esp=3e6), _mk("B", esp=7e6)]
        r = _F["mh557_riepilogo"](cs, soglia_dominante=0.30)
        per_id = {o["id"]: o for o in r["analizzate"]}
        assert per_id["A"]["status"] == "DOMINANTE"


class TestW557Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_titolo_557_presente(self):
        assert self._src().count(TITLE557) == 3

    def test_counts_557(self):
        src = self._src()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        assert "\n" not in line
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"    with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 607
        assert TITLE557 in titoli
        assert "tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607 = st.tabs([" in src

    def test_chiavi_557_univoche(self):
        src = self._src()
        righe = [ln for ln in src.split("\n")
                 if "key=" in ln and "st557_" in ln]
        basi = []
        for ln in righe:
            basi.append(re.search(r"st557_[a-z]+\d*", ln).group(0))
        assert len(basi) == len(set(basi))
        assert len(basi) >= 10
