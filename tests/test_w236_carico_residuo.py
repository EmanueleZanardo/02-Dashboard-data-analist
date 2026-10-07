"""W236 (05/10/2026): test tab236 'Curva di carico residua' — registry + funzioni pure."""
import re
from pathlib import Path

import pytest

APP = Path(__file__).parent.parent.joinpath("app.py")

FUNCS236 = ["clc236_carico_residuo", "clc236_duration_curve", "clc236_kpi_anno",
            "clc236_profilo_giornaliero", "clc236_fv_giornaliero"]


def _extract_pure():
    """Estrae le funzioni pure 236 da app.py senza importare streamlit."""
    src = APP.read_text(encoding="utf-8")
    ns = {"np": __import__("numpy")}
    for fname in FUNCS236:
        m = re.search(rf"\ndef {fname}\(.*?\n(?=\ndef |\n    with |\n# )", src, re.S)
        assert m, f"funzione {fname} non trovata in app.py"
        exec(m.group(0), ns)
    return ns


class TestRegistryTab236:
    def test_tab236_dichiarata(self):
        src = APP.read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 291
        assert "📊 Curva di carico residua" in titoli
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab236" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab236" in withs
        assert len(withs) == len(dvars) == 291
        keys = re.findall(r'key="(t236_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 10

    def test_titoli_ultimo(self):
        src = APP.read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert titoli[-1] == "📊💹 Sharpe & Sortino: la strategia rende davvero?"


class TestPureCaricoResiduo:
    def test_carico_residuo_base(self):
        ns = _extract_pure()
        r = ns["clc236_carico_residuo"]([10, 10, 10], [4, 12, 0])
        assert list(r) == [6, -2, 10]

    def test_carico_residuo_mismatch(self):
        ns = _extract_pure()
        with pytest.raises(ValueError):
            ns["clc236_carico_residuo"]([1, 2], [1])

    def test_duration_curve_ordinata(self):
        ns = _extract_pure()
        d = ns["clc236_duration_curve"]([3, 1, 2])
        assert list(d) == [3, 2, 1]

    def test_kpi_anno_hand(self):
        ns = _extract_pure()
        k = ns["clc236_kpi_anno"]([10, 10, 10], [4, 12, 0])
        assert k["ore_surplus"] == 1
        assert k["energia_surplus_kwh"] == 2.0
        assert k["energia_residua_kwh"] == 16.0
        assert k["picco_residuo_kw"] == 10.0
        assert k["picco_lordo_kw"] == 10.0
        assert k["autoconsumo_pct"] == pytest.approx(87.5)

    def test_kpi_fv_zero(self):
        ns = _extract_pure()
        k = ns["clc236_kpi_anno"]([5, 5], [0, 0])
        assert k["ore_surplus"] == 0
        assert k["autoconsumo_pct"] == 100.0

    def test_profilo_24h(self):
        ns = _extract_pure()
        p = ns["clc236_profilo_giornaliero"](8, 12, 8, 18, 19)
        assert len(p) == 24
        assert p[8] > p[3]

    def test_fv_24h_notte_zero(self):
        ns = _extract_pure()
        f = ns["clc236_fv_giornaliero"](30, 13, 0.0)
        assert len(f) == 24
        assert all(x >= 0.0 for x in f)
        assert f[13] == pytest.approx(30.0)  # picco a mezzogiorno
        assert f[13] > f[10] > f[6]  # cresce al mattino
        assert f[0] < 0.01 * f[13] and f[3] < 0.05 * f[13]  # notte trascurabile vs picco
