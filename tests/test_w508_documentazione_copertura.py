"""Test tab508 '📝 Documentazione della copertura (IFRS 9)': registry + funzioni pure."""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh508_num", "mh508_data", "mh508_campo",
           "mh508_doc", "mh508_riepilogo")

TITLE508 = "📝 Documentazione della copertura (IFRS 9)"
TITLE507 = "🔭 Test prospettico di efficacia (scenari forward)"


def _completa(**kw):
    base = dict(relazione_id="HR-2026-001",
                data_designazione="2026-10-10",
                obiettivo_gestione_rischio="Stabilizzare margine Cal-27",
                elemento_coperto="Vendite baseload 50 MW Cal-27",
                strumento_copertura="Future baseload Cal-27 x50",
                natura_rischio="prezzo commodity",
                hedge_ratio=1.0,
                metodo_valutazione_efficacia="scenari forward 80-125%")
    base.update(kw)
    return _F["mh508_doc"](**base)


class TestW508Validatori:
    def test_num_ok(self):
        assert _F["mh508_num"](2, "x") == 2.0

    def test_num_ko(self):
        for bad in (True, "2", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh508_num"](bad, "x")

    def test_data_ok(self):
        assert str(_F["mh508_data"]("2026-10-10")) == "2026-10-10"
        assert _F["mh508_data"](None) is None
        assert _F["mh508_data"]("") is None

    def test_data_ko(self):
        for bad in ("10/10/2026", "2026-13-01", "2026-02-30", "ieri",
                    "2026-10-10 " * 3):
            with pytest.raises(ValueError):
                _F["mh508_data"](bad)
        with pytest.raises(ValueError):
            _F["mh508_data"]("2099-01-01")  # futura


class TestW508Campo:
    def test_testo_presente(self):
        c = _F["mh508_campo"]("natura_rischio", "prezzo commodity", True)
        assert c["presente"] and c["valore"] == "prezzo commodity"

    def test_testo_mancante(self):
        for v in (None, "", "   "):
            c = _F["mh508_campo"]("obiettivo_gestione_rischio", v, True)
            assert not c["presente"]

    def test_ratio_ok(self):
        c = _F["mh508_campo"]("hedge_ratio", 0.98, True)
        assert c["presente"] and c["valore"] == "0.9800"

    def test_ratio_ko(self):
        with pytest.raises(ValueError):
            _F["mh508_campo"]("hedge_ratio", 0, True)
        with pytest.raises(ValueError):
            _F["mh508_campo"]("hedge_ratio", "x", True)
        c = _F["mh508_campo"]("hedge_ratio", None, True)
        assert not c["presente"]

    def test_scenari_ok(self):
        c = _F["mh508_campo"]("n_scenari_allegati", 6, False)
        assert c["presente"] and c["valore"] == "6"
        c = _F["mh508_campo"]("n_scenari_allegati", None, False)
        assert not c["presente"]

    def test_scenari_ko(self):
        for bad in (-1, 1.5, True, "sei"):
            with pytest.raises(ValueError):
                _F["mh508_campo"]("n_scenari_allegati", bad, False)

    def test_campo_sconosciuto(self):
        with pytest.raises(ValueError):
            _F["mh508_campo"]("foo", "bar", True)


class TestW508Doc:
    def test_completa(self):
        r = _completa(periodicita_rivalutazione="mensile",
                      n_scenari_allegati=6)
        assert r["verdetto"] == "DOCUMENTAZIONE_COMPLETA"
        assert r["punteggio_critici"] == 1.0
        assert r["punteggio_totale"] == 1.0
        assert len(r["campi"]) == 10

    def test_parziale(self):
        r = _completa()
        assert r["verdetto"] == "DOCUMENTAZIONE_PARZIALE"
        assert r["mancanti_critici"] == 0
        assert r["mancanti_opzionali"] == 2
        assert r["punteggio_critici"] == 1.0

    def test_non_designabile(self):
        r = _completa(obiettivo_gestione_rischio="")
        assert r["verdetto"] == "NON_DESIGNABILE"
        assert r["mancanti_critici"] == 1

    def test_non_designabile_data(self):
        r = _completa(data_designazione=None)
        assert r["verdetto"] == "NON_DESIGNABILE"

    def test_demo_ciclo(self):
        r = _F["mh508_riepilogo"](
            "HR-2026-042", "2026-10-10",
            "Stabilizzare il margine sulle vendite baseload Cal-27",
            "Vendite baseload 50 MW Cal-27 zona DE",
            "Future baseload Cal-27 x 50 contratti",
            "Rischio prezzo commodity (power baseload)", 1.0,
            "Scenari forward, banda 80-125% (tab507)",
            periodicita_rivalutazione="Mensile", n_scenari_allegati=6)
        assert r["verdetto"] == "DOCUMENTAZIONE_COMPLETA"

    def test_degenere(self):
        with pytest.raises(ValueError):
            _completa(data_designazione="2099-12-31")
        with pytest.raises(ValueError):
            _completa(hedge_ratio=0)
        with pytest.raises(ValueError):
            _completa(data_designazione="10-10-2026")
        with pytest.raises(ValueError):
            _completa(n_scenari_allegati=-2)


def test_registry_tab508():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 519
    assert TITLE508 in titoli
    assert src.count(TITLE508) == 3
    assert ", tab507, tab508, tab509, tab510, tab511, tab512, tab513, tab514, tab515, tab516, tab517, tab518, tab519 = st.tabs([" in src
    assert "    with tab508:" in src
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    assert "tab508" in dvars
    withs = re.findall(r"    with (tab\d+):", src)
    assert "tab508" in withs
    assert len(withs) == len(dvars) == 519
    # ordine: tab508 dopo tab507
    _decl508 = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    assert _decl508.index(f'"{TITLE507}"') < _decl508.index(f'"{TITLE508}"')
    assert titoli[dvars.index("tab508")] == TITLE508


def test_chiavi_st508_uniche():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    keys = re.findall(r'key="(st508_[^"]+)"', src) + re.findall(
        r'key=f"(st508_[^"]+)"', src)
    assert len(keys) == len(set(keys)) > 5
