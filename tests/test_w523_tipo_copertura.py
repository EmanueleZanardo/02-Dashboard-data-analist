"""Test tab523 '🔀📊 Tipo di copertura (IFRS 9 6.5.2)': registry + funzioni pure."""

import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh523_num", "mh523_str", "mh523_copertura", "mh523_classifica",
           "mh523_riepilogo")

TITLE523 = "🔀📊 Tipo di copertura (IFRS 9 6.5.2)"
TITLE522 = "⚖️📋 Hedge ratio designato (IFRS 9 6.4.1(c)(iii))"


def _c(cid="COV-2026-001", nat="riconosciuta", prob=100.0, tipo="auto",
       d="Forward fisico"):
    return {"id": cid, "natura_item": nat, "prob_forecast": prob,
            "tipo_dichiarato": tipo, "descrizione": d}


class TestW523Validatori:
    def test_num_ok(self):
        assert _F["mh523_num"](2, "x") == 2.0
        assert _F["mh523_num"](0.0, "x") == 0.0
        assert _F["mh523_num"](100, "x") == 100.0

    def test_num_ko(self):
        for bad in (True, "2", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh523_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh523_str"]("  COV-1 ", "x") == "COV-1"

    def test_str_ko(self):
        for bad in (None, "", "   ", 5):
            with pytest.raises(ValueError):
                _F["mh523_str"](bad, "x")


class TestW523Copertura:
    def test_ok(self):
        c = _F["mh523_copertura"](_c())
        assert c["id"] == "COV-2026-001"
        assert c["natura_item"] == "riconosciuta"
        assert c["prob_forecast"] == pytest.approx(100.0)
        assert c["tipo_dichiarato"] == "auto"
        assert c["descrizione"] == "Forward fisico"

    def test_default_prob_tipo_desc(self):
        d = _c()
        del d["prob_forecast"]
        del d["tipo_dichiarato"]
        del d["descrizione"]
        c = _F["mh523_copertura"](d)
        assert c["prob_forecast"] == 100.0
        assert c["tipo_dichiarato"] == "auto"
        assert c["descrizione"] == ""

    def test_natura_ko(self):
        for bad in ("spot", "", None, 5):
            with pytest.raises(ValueError):
                _F["mh523_copertura"](_c(nat=bad))

    def test_prob_ko(self):
        for bad in (-1, 101, True, float("nan"), "90"):
            with pytest.raises(ValueError):
                _F["mh523_copertura"](_c(prob=bad))

    def test_tipo_dichiarato_ko(self):
        for bad in ("fair", "", None):
            with pytest.raises(ValueError):
                _F["mh523_copertura"](_c(tipo=bad))

    def test_chiave_mancante(self):
        d = _c()
        del d["natura_item"]
        with pytest.raises(ValueError):
            _F["mh523_copertura"](d)

    def test_non_dict(self):
        with pytest.raises(ValueError):
            _F["mh523_copertura"](["id"])

    def test_id_vuoto(self):
        with pytest.raises(ValueError):
            _F["mh523_copertura"](_c(cid="  "))

    def test_descrizione_non_str(self):
        with pytest.raises(ValueError):
            _F["mh523_copertura"](_c(d=5))


class TestW523Classifica:
    def test_riconosciuta_fair_value(self):
        r = _F["mh523_classifica"](_c(tipo="fair_value"))
        assert r["tipo_determinato"] == "fair_value"
        assert r["esito"] == "COERENTE"
        assert r["motivo"] == ""
        assert "P&L" in r["destino"]

    def test_firm_commitment_fair_value(self):
        r = _F["mh523_classifica"](_c(nat="firm_commitment", tipo="auto"))
        assert r["tipo_determinato"] == "fair_value"
        assert r["esito"] == "COERENTE"

    def test_forecast_cash_flow(self):
        r = _F["mh523_classifica"](_c(nat="forecast", prob=90.0,
                                      tipo="cash_flow"))
        assert r["tipo_determinato"] == "cash_flow"
        assert r["esito"] == "COERENTE"
        assert "OCI" in r["destino"]

    def test_net_investment(self):
        r = _F["mh523_classifica"](_c(nat="net_investment", tipo="auto"))
        assert r["tipo_determinato"] == "net_investment"
        assert r["esito"] == "COERENTE"
        assert "dismissione" in r["destino"]

    def test_mismatch(self):
        r = _F["mh523_classifica"](_c(nat="forecast", prob=90.0,
                                      tipo="fair_value"))
        assert r["tipo_determinato"] == "cash_flow"
        assert r["esito"] == "MISMATCH"
        assert "fair_value" in r["motivo"]
        assert "6.5.2" in r["motivo"]

    def test_non_designabile_prob_bassa(self):
        r = _F["mh523_classifica"](_c(nat="forecast", prob=55.0,
                                      tipo="auto"))
        assert r["tipo_determinato"] == "cash_flow"
        assert r["esito"] == "NON_DESIGNABILE"
        assert "6.3.3(c)" in r["motivo"]

    def test_prob_80_designabile(self):
        r = _F["mh523_classifica"](_c(nat="forecast", prob=80.0,
                                      tipo="auto"))
        assert r["esito"] == "COERENTE"

    def test_prob_irrilevante_non_forecast(self):
        r = _F["mh523_classifica"](_c(nat="riconosciuta", prob=10.0,
                                      tipo="auto"))
        assert r["esito"] == "COERENTE"

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh523_classifica"]("non un dict")
        with pytest.raises(ValueError):
            _F["mh523_classifica"]({"id": "X"})


class TestW523Riepilogo:
    def test_misto(self):
        a = _F["mh523_riepilogo"](
            [_c(), _c(cid="COV-2026-002", nat="forecast", prob=90.0,
                      tipo="fair_value", d="Acquisto forecast")])
        t = a["totali"]
        assert t["n_coperture"] == 2
        assert t["n_coerenti"] == 1
        assert t["n_mismatch"] == 1
        assert t["n_non_designabili"] == 0
        assert t["n_fair_value"] == 1
        assert t["n_cash_flow"] == 1
        assert t["n_net_investment"] == 0
        assert t["n_quota_oci"] == 0
        assert t["verdetto_complessivo"] == "MISTO"

    def test_tutte_coerenti(self):
        a = _F["mh523_riepilogo"](
            [_c(), _c(cid="C2", nat="forecast", prob=95.0,
                      tipo="cash_flow"),
             _c(cid="C3", nat="net_investment", tipo="auto")])
        t = a["totali"]
        assert t["verdetto_complessivo"] == "TUTTE_COERENTI"
        assert t["n_fair_value"] == 1
        assert t["n_cash_flow"] == 1
        assert t["n_net_investment"] == 1
        assert t["n_quota_oci"] == 2

    def test_nessuna_coerente(self):
        a = _F["mh523_riepilogo"](
            [_c(cid="A", nat="forecast", prob=60.0, tipo="auto"),
             _c(cid="B", nat="net_investment", tipo="fair_value")])
        t = a["totali"]
        assert t["verdetto_complessivo"] == "NESSUNA_COERENTE"
        assert t["n_coerenti"] == 0
        assert t["n_non_designabili"] == 1
        assert t["n_mismatch"] == 1

    def test_wrapper_parita_classifica(self):
        a = _F["mh523_riepilogo"]([_c()])
        v = _F["mh523_classifica"](_c())
        assert a["righe"][0]["tipo_determinato"] == v["tipo_determinato"]
        assert a["righe"][0]["esito"] == v["esito"]

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh523_riepilogo"]([])
        with pytest.raises(ValueError):
            _F["mh523_riepilogo"]("non una lista")
        with pytest.raises(ValueError):
            _F["mh523_riepilogo"]([_c(cid="A"), _c(cid="A")])


def test_registry_tab523():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(
        encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 746
    assert TITLE523 in titoli
    assert TITLE522 in titoli
    assert src.count(TITLE523) == 3
    assert ", tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746 = st.tabs([" in src
