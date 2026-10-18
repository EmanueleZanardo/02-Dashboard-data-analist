"""Test tab515 '🛑 Cessazione della copertura (hedge discontinuation)': registry + funzioni pure."""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh515_num", "mh515_str", "mh515_data",
           "mh515_evento", "mh515_cessazione", "mh515_riepilogo")

TITLE515 = "🛑 Cessazione della copertura (hedge discontinuation)"
TITLE514 = "📅 Piano di recycling futuro (proiezione release OCI→P&L)"


def _e(rid="HR-2026-001", data="2026-09-30", motivo="operazione_non_piu_probabile",
       ris=15000.0, prob=False):
    return {"id": rid, "data": data, "motivo": motivo,
            "riserva_residua": ris, "operazione_probabile": prob}


class TestW515Validatori:
    def test_num_ok(self):
        assert _F["mh515_num"](2, "x") == 2.0

    def test_num_ko(self):
        for bad in (True, "2", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh515_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh515_str"]("  HR-1 ", "x") == "HR-1"

    def test_str_ko(self):
        for bad in (None, "", "   ", 5):
            with pytest.raises(ValueError):
                _F["mh515_str"](bad, "x")

    def test_data_ok(self):
        assert _F["mh515_data"]("2026-09-30") == "2026-09-30"

    def test_data_formato_ko(self):
        for bad in ("30/09/2026", "2026-9-30", "2026-13-01", "no-data", None):
            with pytest.raises(ValueError):
                _F["mh515_data"](bad)

    def test_data_futura_ko(self):
        with pytest.raises(ValueError):
            _F["mh515_data"]("2999-01-01")


class TestW515Evento:
    def test_ok(self):
        r = _F["mh515_evento"](_e())
        assert r["id"] == "HR-2026-001"
        assert r["data"] == "2026-09-30"
        assert r["motivo"] == "operazione_non_piu_probabile"
        assert r["operazione_probabile"] is False

    def test_motivo_ko(self):
        with pytest.raises(ValueError):
            _F["mh515_evento"](_e(motivo="venduta_a_mio_cugino"))

    def test_chiave_mancante_ko(self):
        d = _e()
        del d["riserva_residua"]
        with pytest.raises(ValueError):
            _F["mh515_evento"](d)

    def test_prob_non_bool_ko(self):
        with pytest.raises(ValueError):
            _F["mh515_evento"](_e(prob="si"))


class TestW515Cessazione:
    def test_riciclo_immediato_da_motivo(self):
        a = _F["mh515_cessazione"]([_e()])
        o = a["righe"][0]
        assert o["verdetto"] == "RICICLO_IMMEDIATO"
        assert o["riciclo_immediato"] == pytest.approx(15000.0)
        assert o["accantonato_oci"] == pytest.approx(0.0)

    def test_riciclo_immediato_da_prob_false(self):
        # motivo innocuo ma operazione non più probabile -> immediato
        a = _F["mh515_cessazione"](
            [_e(rid="A", motivo="scadenza_strumento", ris=9500.0, prob=False)])
        o = a["righe"][0]
        assert o["verdetto"] == "RICICLO_IMMEDIATO"
        assert o["riciclo_immediato"] == pytest.approx(9500.0)

    def test_riserva_accantonata(self):
        a = _F["mh515_cessazione"](
            [_e(rid="A", motivo="revoca_volontaria", ris=4200.0, prob=True)])
        o = a["righe"][0]
        assert o["verdetto"] == "RISERVA_ACCANTONATA"
        assert o["riciclo_immediato"] == pytest.approx(0.0)
        assert o["accantonato_oci"] == pytest.approx(4200.0)

    def test_totali_demo(self):
        a = _F["mh515_cessazione"]([
            _e("HR-2026-001", "2026-09-30", "operazione_non_piu_probabile",
               15000.0, False),
            _e("HR-2026-002", "2026-10-15", "scadenza_strumento",
               9500.0, True),
            _e("HR-2026-003", "2026-10-10", "revoca_volontaria",
               4200.0, False)])
        tt = a["totali"]
        assert tt["n_eventi"] == 3
        assert tt["n_immediati"] == 2
        assert tt["riserva_totale"] == pytest.approx(28700.0)
        assert tt["riciclo_immediato_totale"] == pytest.approx(19200.0)
        assert tt["accantonato_totale"] == pytest.approx(9500.0)
        assert tt["verdetto_complessivo"] == "IMPATTO_IMMEDIATO"

    def test_complessivo_accantonate(self):
        a = _F["mh515_cessazione"](
            [_e("A", motivo="altro", ris=100.0, prob=True)])
        assert a["totali"]["verdetto_complessivo"] == "RISERVE_ACCANTONATE"

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh515_cessazione"]([])
        with pytest.raises(ValueError):
            _F["mh515_cessazione"]("non una lista")
        with pytest.raises(ValueError):
            _F["mh515_cessazione"]([_e(rid="A"), _e(rid="A")])
        with pytest.raises(ValueError):
            _F["mh515_cessazione"]([_e(ris=float("nan"))])

    def test_riepilogo_wrapper(self):
        a = _F["mh515_riepilogo"]([_e()])
        assert a["totali"]["n_eventi"] == 1
        assert a["righe"][0]["verdetto"] == "RICICLO_IMMEDIATO"


def test_registry_tab515():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 555
    assert TITLE515 in titoli
    assert src.count(TITLE515) == 3
    assert ", tab514, tab515, tab516, tab517, tab518, tab519, tab520, tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555 = st.tabs([" in src
    assert "    with tab515:" in src
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    assert "tab515" in dvars
    withs = re.findall(r"    with (tab\d+):", src)
    assert "tab515" in withs
    assert len(withs) == len(dvars) == 555
    # ordine: tab515 dopo tab514
    _decl515 = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    assert _decl515.index(f'"{TITLE514}"') < _decl515.index(f'"{TITLE515}"')
    assert titoli[dvars.index("tab515")] == TITLE515


def test_chiavi_st515_uniche():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    keys = re.findall(r'key="(st515_[^"]+)"', src) + re.findall(
        r'key=f"(st515_[^"]+)"', src)
    assert len(keys) == len(set(keys)) > 5
