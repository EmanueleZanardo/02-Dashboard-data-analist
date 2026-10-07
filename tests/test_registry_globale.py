"""Test trasversali sul registry delle tab di app.py.

A differenza dei test per-tab (che asseriscono il conteggio hardcoded e
vengono bumpati a ogni nuova tab), questi check sono DINAMICI: derivano il
numero di tab atteso dal registry stesso e restano verdi a ogni aggiunta.
"""

import re
from collections import Counter
from pathlib import Path

APP = Path(__file__).parent.parent / "app.py"


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryGlobale:
    def test_conteggi_coerenti(self):
        _, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) >= 1

    def test_numerazione_consecutiva(self):
        _, _, dvars, _ = _registry()
        attesi = ["tab%d" % i for i in range(1, len(dvars) + 1)]
        assert dvars == attesi

    def test_titoli_unici(self):
        _, titoli, _, _ = _registry()
        dup = sorted(t for t, c in Counter(titoli).items() if c > 1)
        assert not dup, "titoli duplicati: %s" % dup[:5]

    def test_titoli_non_vuoti(self):
        _, titoli, _, _ = _registry()
        assert all(t.strip() for t in titoli)

    def test_with_allineati_a_dvars(self):
        _, _, dvars, withs = _registry()
        assert withs == dvars


class TestChiaviWidgetGlobali:
    def test_key_uniche_in_tutta_app(self):
        src = APP.read_text(encoding="utf-8")
        keys = re.findall(r'key="([^"]+)"', src)
        assert len(keys) >= 100
        dup = sorted(k for k, c in Counter(keys).items() if c > 1)
        assert not dup, "chiavi widget duplicate: %s" % dup[:10]
