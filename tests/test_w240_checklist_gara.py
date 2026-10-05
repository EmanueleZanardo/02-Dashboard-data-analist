"""Test tab240 'Checklist gara fornitura': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Il test verifica consistenza del registry (titoli/dvar/with coerenti) e presenza
di tab240, invece di un conteggio assoluto (i worker paralleli aggiungono tab
in contemporanea).
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("checklist_score", "rank_offers")
checklist_score = _F["checklist_score"]
rank_offers = _F["rank_offers"]

APP = Path(__file__).parent.parent / "app.py"


class TestRegistryTab240:
    def test_tab240_dichiarata(self):
        src = APP.read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"    with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) >= 231
        assert "📋 Checklist gara fornitura" in titoli
        assert "tab240" in dvars
        assert "tab240" in withs
        keys = re.findall(r'key="(t240_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 10

    def test_chiavi_t240_uniche_e_sufficienti(self):
        src = APP.read_text(encoding="utf-8")
        keys = re.findall(r'key="(t240_[^"]+)"', src)
        assert len(set(keys)) == len(keys) >= 10
        # 8 pesi + 24 slider (3 offerte x 8 voci) + 1 csv
        assert sum(1 for k in keys if k.startswith("t240_w_")) == 8
        assert sum(1 for k in keys if k.startswith("t240_s_")) == 24


class TestChecklistScore:
    def test_score_ponderato_base(self):
        items = [("A", 50.0, 4), ("B", 50.0, 2)]
        r = checklist_score(items)
        assert r["totale_ponderato"] == pytest.approx(3.0)
        assert r["somma_pesi"] == pytest.approx(100.0)
        assert r["pesi_validi"] is True
        assert len(r["dettaglio"]) == 2

    def test_pesi_non_normalizzati(self):
        items = [("A", 30.0, 5), ("B", 10.0, 1)]
        r = checklist_score(items)
        assert r["totale_ponderato"] == pytest.approx(4.0)
        assert r["somma_pesi"] == pytest.approx(40.0)
        assert r["pesi_validi"] is True

    def test_clamp_punteggio_e_peso(self):
        items = [("A", 100.0, 9), ("B", -5.0, 3)]
        r = checklist_score(items)
        # score clampato a 5, peso negativo a 0
        assert r["totale_ponderato"] == pytest.approx(5.0)
        assert r["somma_pesi"] == pytest.approx(100.0)

    def test_pesi_zero(self):
        r = checklist_score([("A", 0.0, 5)])
        assert r["totale_ponderato"] == 0.0
        assert r["pesi_validi"] is False

    def test_input_non_numerici(self):
        r = checklist_score([("A", "x", None)])
        assert r["totale_ponderato"] == 0.0


class TestRankOffers:
    def _items(self, score_fisso):
        return [("V%d" % i, 100.0 / 8, score_fisso) for i in range(8)]

    def test_ordine_decrescente(self):
        offerte = [("Offerta A", self._items(5)),
                   ("Offerta B", self._items(2)),
                   ("Offerta C", self._items(4))]
        c = rank_offers(offerte)
        assert [r["offerta"] for r in c] == ["Offerta A", "Offerta C", "Offerta B"]
        assert [r["posizione"] for r in c] == [1, 2, 3]
        assert c[0]["score"] == pytest.approx(5.0)
        assert c[2]["score"] == pytest.approx(2.0)

    def test_pareggio(self):
        offerte = [("A", self._items(3)), ("B", self._items(3))]
        c = rank_offers(offerte)
        assert c[0]["score"] == c[1]["score"] == pytest.approx(3.0)
