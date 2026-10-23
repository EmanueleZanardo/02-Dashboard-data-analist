"""Test tab520 '🔁 Aggregated exposure (esposizione aggregata, IFRS 9 6.3.4)': registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh520_num", "mh520_str", "mh520_componente", "mh520_verifica",
           "mh520_riepilogo")

TITLE520 = "🔁 Aggregated exposure (esposizione aggregata, IFRS 9 6.3.4)"
TITLE519 = "⚠️💳 Rischio di credito che domina (IFRS 9)"


def _c(cid="BASE-TTF-Q1", t="base", v=1250000.0, dv=42000.0,
        d="Acquisto forecast TTF Q1 2027"):
    return {"id": cid, "tipo": t, "valore": v, "variazione": dv,
            "descrizione": d}


def _e(eid="ESP-2026-001", comps=None):
    if comps is None:
        comps = [_c(),
                 _c(cid="SWP-TTF-Q1", t="derivato", v=-8200.0,
                     dv=-39500.0, d="Swap TTF Q1, prima relazione")]
    return {"id": eid, "componenti": comps}


class TestW520Validatori:
    def test_num_ok(self):
        assert _F["mh520_num"](2, "x") == 2.0
        assert _F["mh520_num"](-8200.5, "x") == -8200.5

    def test_num_ko(self):
        for bad in (True, "2", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh520_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh520_str"]("  ESP-1 ", "x") == "ESP-1"

    def test_str_ko(self):
        for bad in (None, "", "   ", 5):
            with pytest.raises(ValueError):
                _F["mh520_str"](bad, "x")


class TestW520Componente:
    def test_ok_base(self):
        r = _F["mh520_componente"](_c())
        assert r["id"] == "BASE-TTF-Q1"
        assert r["tipo"] == "base"
        assert r["contributo"] == pytest.approx(42000.0)
        assert r["descrizione"] == "Acquisto forecast TTF Q1 2027"

    def test_ok_derivato_senza_descrizione(self):
        r = _F["mh520_componente"](_c(cid="SWP-1", t="derivato",
                                       v=-8200.0, dv=-39500.0, d=""))
        assert r["tipo"] == "derivato"
        assert r["descrizione"] == ""
        assert r["contributo"] == pytest.approx(39500.0)

    def test_descrizione_default(self):
        d = _c()
        del d["descrizione"]
        r = _F["mh520_componente"](d)
        assert r["descrizione"] == ""

    def test_tipo_ko(self):
        with pytest.raises(ValueError):
            _F["mh520_componente"](_c(t="hedge"))
        with pytest.raises(ValueError):
            _F["mh520_componente"](_c(t="BASE"))

    def test_chiave_mancante(self):
        d = _c()
        del d["valore"]
        with pytest.raises(ValueError):
            _F["mh520_componente"](d)

    def test_non_dict(self):
        with pytest.raises(ValueError):
            _F["mh520_componente"](["id"])

    def test_id_vuoto(self):
        with pytest.raises(ValueError):
            _F["mh520_componente"](_c(cid="  "))

    def test_valori_ko(self):
        for bad in (True, float("nan"), float("inf"), "42000"):
            with pytest.raises(ValueError):
                _F["mh520_componente"](_c(dv=bad))

    def test_descrizione_non_str(self):
        with pytest.raises(ValueError):
            _F["mh520_componente"](_c(d=5))


class TestW520Verifica:
    def test_demo_eleggibile(self):
        r = _F["mh520_verifica"](_e())
        assert r["id"] == "ESP-2026-001"
        assert r["n_base"] == 1
        assert r["n_derivati"] == 1
        assert r["valore_aggregato"] == pytest.approx(1241800.0)
        assert r["variazione_aggregata"] == pytest.approx(2500.0)
        assert r["contributo_derivati"] == pytest.approx(
            39500.0 / 81500.0)
        assert r["verdetto"] == "ELEGGIBILE"
        assert r["motivo"] == ""
        assert len(r["righe"]) == 2

    def test_non_eleggibile_solo_derivati(self):
        r = _F["mh520_verifica"](
            _e(eid="ESP-2026-002",
               comps=[_c(cid="FWD-TTF-01", t="derivato", v=12000.0,
                          dv=1500.0, d="Forward TTF"),
                      _c(cid="OPT-TTF-01", t="derivato", v=-3400.0,
                          dv=-900.0, d="Opzione TTF")]))
        assert r["verdetto"] == "NON_ELEGGIBILE"
        assert r["motivo"] == "nessuna componente di base"
        assert r["contributo_derivati"] == pytest.approx(1.0)

    def test_non_eleggibile_solo_base(self):
        r = _F["mh520_verifica"](
            _e(eid="X", comps=[_c(cid="A"), _c(cid="B", t="base")]))
        assert r["verdetto"] == "NON_ELEGGIBILE"
        assert "derivato" in r["motivo"]

    def test_non_eleggibile_una_sola_componente(self):
        r = _F["mh520_verifica"](_e(eid="X", comps=[_c()]))
        assert r["verdetto"] == "NON_ELEGGIBILE"
        assert r["motivo"] != ""

    def test_denominatore_zero(self):
        r = _F["mh520_verifica"](
            _e(eid="X",
               comps=[_c(cid="A", dv=0.0),
                      _c(cid="D", t="derivato", v=0.0, dv=0.0)]))
        assert r["verdetto"] == "ELEGGIBILE"
        assert r["contributo_derivati"] == 0.0

    def test_id_componente_duplicato(self):
        with pytest.raises(ValueError):
            _F["mh520_verifica"](_e(eid="X",
                                   comps=[_c(cid="A"), _c(cid="A",
                                                           t="derivato")]))

    def test_componenti_vuota(self):
        with pytest.raises(ValueError):
            _F["mh520_verifica"](_e(eid="X", comps=[]))

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh520_verifica"]("non un dict")
        with pytest.raises(ValueError):
            _F["mh520_verifica"]({"id": "X"})
        with pytest.raises(ValueError):
            _F["mh520_verifica"]({"id": "  ",
                                  "componenti": [_c(), _c(cid="B",
                                                          t="derivato")]})
        with pytest.raises(ValueError):
            _F["mh520_verifica"]({"id": "X", "componenti": "no"})
        with pytest.raises(ValueError):
            _F["mh520_verifica"](
                {"id": "X",
                 "componenti": [{"id": "A", "tipo": "base"}]})


class TestW520Riepilogo:
    def test_misto(self):
        a = _F["mh520_riepilogo"](
            [_e(),
             _e(eid="ESP-2026-002",
                comps=[_c(cid="FWD", t="derivato", v=12000.0,
                           dv=1500.0, d="Forward TTF"),
                       _c(cid="OPT", t="derivato", v=-3400.0,
                           dv=-900.0, d="Opzione TTF")])])
        t = a["totali"]
        assert t["n_esposizioni"] == 2
        assert t["n_eleggibili"] == 1
        assert t["n_non_eleggibili"] == 1
        assert t["valore_aggregato_totale"] == pytest.approx(
            1241800.0 + 8600.0)
        assert t["variazione_aggregata_totale"] == pytest.approx(
            2500.0 + 600.0)
        assert t["verdetto_complessivo"] == "MISTO"

    def test_tutte_eleggibili(self):
        a = _F["mh520_riepilogo"]([_e(), _e(eid="Y")])
        assert a["totali"]["verdetto_complessivo"] == "TUTTE_ELEGGIBILI"
        assert a["totali"]["n_eleggibili"] == 2

    def test_nessuna_eleggibile(self):
        solo_d = _e(eid="Z",
                    comps=[_c(cid="F", t="derivato", dv=1500.0),
                           _c(cid="O", t="derivato", dv=-900.0)])
        a = _F["mh520_riepilogo"]([solo_d])
        assert a["totali"]["verdetto_complessivo"] == "NESSUNA_ELEGGIBILE"

    def test_contributo_derivati_totale(self):
        a = _F["mh520_riepilogo"]([_e()])
        assert a["totali"]["contributo_derivati_totale"] == pytest.approx(
            39500.0 / 81500.0)

    def test_wrapper_parita_verifica(self):
        a = _F["mh520_riepilogo"]([_e()])
        v = _F["mh520_verifica"](_e())
        assert a["righe"][0]["valore_aggregato"] == pytest.approx(
            v["valore_aggregato"])
        assert a["righe"][0]["verdetto"] == v["verdetto"]

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh520_riepilogo"]([])
        with pytest.raises(ValueError):
            _F["mh520_riepilogo"]("non una lista")
        with pytest.raises(ValueError):
            _F["mh520_riepilogo"]([_e(eid="A"), _e(eid="A")])


def test_registry_tab520():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 654
    assert TITLE520 in titoli
    assert src.count(TITLE520) == 3
    assert ", tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654 = st.tabs([" in src
    assert "    with tab520:" in src
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    assert "tab520" in dvars
    withs = re.findall(r"    with (tab\d+):", src)
    assert "tab520" in withs
    assert len(withs) == len(dvars) == 654
    # ordine: tab520 dopo tab519
    _decl520 = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    assert _decl520.index(f'"{TITLE519}"') < _decl520.index(f'"{TITLE520}"')
    assert titoli[dvars.index("tab520")] == TITLE520


def test_chiavi_st520_uniche():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(
        encoding="utf-8")
    keys = re.findall(r'key="(st520_[^"]+)"', src) + re.findall(
        r'key=f"(st520_[^"]+)"', src)
    assert len(keys) == len(set(keys)) > 5
