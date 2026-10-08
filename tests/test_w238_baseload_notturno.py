"""W238 (05/10/2026): test tab238 'Baseload notturno' — registry + funzioni pure."""
import re
from pathlib import Path

APP = Path(__file__).parent.parent.joinpath("app.py")


def _extract_pure(ns_name):
    """Estrae le funzioni pure 238 da app.py senza importare streamlit: exec del solo codice def."""
    src = APP.read_text(encoding="utf-8")
    ns = {"np": __import__("numpy")}
    for fname in ["night_share238", "ghost_load238", "profilo_sintetico238"]:
        m = re.search(rf"\ndef {fname}\(.*?\n(?=\ndef |\n    with |\n# )", src, re.S)
        assert m, f"funzione {fname} non trovata in app.py"
        exec(m.group(0), ns)
    return ns


class TestRegistryTab238:
    def test_tab238_dichiarata(self):
        src = APP.read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 304
        assert "🌙 Baseload notturno" in titoli
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab238" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab238" in withs
        assert len(withs) == len(dvars) == 304
        keys = re.findall(r'key="(t238_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 10


class TestPureBaseloadNotturno:
    def _load(self):
        return [10.0] * 24, [100.0] * 24

    def test_night_share_quota(self):
        ns = _extract_pure(None)
        load, price = self._load()
        # 10 kW costanti: quota notte = 8/24
        r = ns["night_share238"](load, price)
        assert abs(r["quota"] - 8 / 24) < 1e-9
        assert abs(r["energia_notte_kwh"] - 80.0) < 1e-9
        assert abs(r["costo_notte"] - 80.0 * 100.0 / 1000.0) < 1e-9
        assert abs(r["costo_giorno"] - 160.0 * 100.0 / 1000.0) < 1e-9
        assert abs(r["rapporto"] - 1.0) < 1e-9

    def test_night_share_prezzi_diversi(self):
        ns = _extract_pure(None)
        load = [10.0] * 24
        price = [50.0 if h in (22, 23, 0, 1, 2, 3, 4, 5) else 100.0 for h in range(24)]
        r = ns["night_share238"](load, price)
        assert abs(r["prezzo_medio_notte"] - 50.0) < 1e-9
        assert abs(r["prezzo_medio_giorno"] - 100.0) < 1e-9
        assert abs(r["rapporto"] - 0.5) < 1e-9

    def test_ghost_load(self):
        ns = _extract_pure(None)
        load = [50.0] * 24
        for h in (22, 23, 0, 1, 2, 3, 4, 5):
            load[h] = 7.5
        load[3] = 5.0
        assert ns["ghost_load238"](load) == 5.0

    def test_profilo_sintetico(self):
        ns = _extract_pure(None)
        p = ns["profilo_sintetico238"](8.0, 60.0, 12, 0.35)
        assert len(p) == 24
        assert min(p) >= 8.0  # baseload mai sotto la base
        assert max(p) > 60.0  # picco sopra la sola gaussiana per la base
        # picco diurno attorno all'ora 12
        assert p.index(max(p)) in (11, 12, 13)

    def test_validazione_input(self):
        ns = _extract_pure(None)
        try:
            ns["night_share238"]([1.0] * 23, [1.0] * 24)
            raise AssertionError("doveva fallire su 23 valori")
        except ValueError:
            pass
        try:
            ns["ghost_load238"]([1.0] * 10)
            raise AssertionError("doveva fallire su 10 valori")
        except ValueError:
            pass
