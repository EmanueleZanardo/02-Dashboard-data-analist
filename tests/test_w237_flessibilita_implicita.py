"""W237 (05/10/2026): test tab237 'Flessibilita' implicita' — registry + funzioni pure."""
import re
from pathlib import Path

import pytest

APP = Path(__file__).parent.parent.joinpath("app.py")

FUNCS237 = ["flx237_top_bottom", "flx237_shifting_saving",
            "flx237_profilo_sintetico", "flx237_prezzo_sintetico"]


def _extract_pure():
    """Estrae le funzioni pure 237 da app.py senza importare streamlit."""
    src = APP.read_text(encoding="utf-8")
    ns = {"np": __import__("numpy")}
    for fname in FUNCS237:
        m = re.search(rf"\ndef {fname}\(.*?\n(?=\ndef |\n    with |\n# )", src, re.S)
        assert m, f"funzione {fname} non trovata in app.py"
        exec(m.group(0), ns)
    return ns


class TestRegistryTab237:
    def test_tab237_dichiarata(self):
        src = APP.read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 277
        assert "⚡ Flessibilità implicita" in titoli
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab237" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab237" in withs
        assert len(withs) == len(dvars) == 277
        keys = re.findall(r'key="(t237_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 10

    def test_titoli_ultimo(self):
        src = APP.read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert titoli[-1] == "⚡ Aste MI: scostamenti vs MGP"


class TestPureFlessibilitaImplicita:
    def test_top_bottom_base(self):
        ns = _extract_pure()
        top, bottom = ns["flx237_top_bottom"]([1, 1, 1, 1], [10, 40, 20, 30], quota_top=0.5)
        assert sorted(top) == [1, 3]
        assert sorted(bottom) == [0, 2]

    def test_top_bottom_quota_minima(self):
        ns = _extract_pure()
        top, bottom = ns["flx237_top_bottom"]([1] * 24, list(range(24)), quota_top=0.01)
        assert len(top) == 1 and len(bottom) == 1
        assert top[0] == 23 and bottom[0] == 0

    def test_shifting_saving_hand(self):
        ns = _extract_pure()
        r = ns["flx237_shifting_saving"]([10, 10, 10, 10], [10, 40, 20, 30], pct_shift=0.5, quota_top=0.5)
        assert r["energia_spostabile_kwh"] == 10.0
        assert r["risparmio_eur"] == pytest.approx(0.20)
        assert r["prezzo_medio_top"] == 35.0
        assert r["prezzo_medio_bottom"] == 15.0
        assert r["costo_base_eur"] == pytest.approx(1.0)

    def test_shifting_saving_mismatch(self):
        ns = _extract_pure()
        with pytest.raises(ValueError):
            ns["flx237_shifting_saving"]([1, 2], [1])

    def test_shifting_zero_quando_prezzi_piatti(self):
        ns = _extract_pure()
        r = ns["flx237_shifting_saving"]([10] * 24, [50] * 24, pct_shift=0.5, quota_top=0.1)
        assert r["risparmio_eur"] == 0.0

    def test_profilo_sintetico_24h(self):
        ns = _extract_pure()
        p = ns["flx237_profilo_sintetico"](6, 15, 19, seed=3)
        assert len(p) == 24
        assert all(x >= 0 for x in p)

    def test_prezzo_sintetico_24h(self):
        ns = _extract_pure()
        p = ns["flx237_prezzo_sintetico"](70, 60, 18, seed=3)
        assert len(p) == 24
        assert all(x >= 1.0 for x in p)
        assert p[18] > p[3]

    def test_ripetibilita_seed(self):
        ns = _extract_pure()
        a = ns["flx237_profilo_sintetico"](6, 15, 19, seed=42)
        b = ns["flx237_profilo_sintetico"](6, 15, 19, seed=42)
        assert a == b
