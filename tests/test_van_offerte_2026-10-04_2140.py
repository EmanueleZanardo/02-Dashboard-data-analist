"""Test tab216 'VAN offerte pluriennali': helper calcola_van_offerte_pluriennali —
confronto in Valore Attuale Netto di offerte di fornitura con durate diverse
(le offerte corte vengono rinnovate al forward atteso oltre la scadenza).

Stile pytest (vedi docs/AGGIUNGERE_TAB.md): la funzione viene estratta da
app.py via AST senza avviare Streamlit.
"""

import re
from pathlib import Path

import pandas as pd
import pytest

from appfuncs import load

_F = load("calcola_van_offerte_pluriennali")
calcola_van_offerte_pluriennali = _F["calcola_van_offerte_pluriennali"]

APP = Path(__file__).parent.parent / "app.py"


def _offerte_base():
    return [
        {"nome": "A", "prezzo_eur_mwh": 120.0, "durata_anni": 1,
         "canone_fisso_eur_mese": 0.0, "attivazione_eur": 0.0},
        {"nome": "B", "prezzo_eur_mwh": 125.0, "durata_anni": 3,
         "canone_fisso_eur_mese": 0.0, "attivazione_eur": 0.0},
    ]


class TestNumeriAMano:
    # V=1000, r=5%, F=130, g=0, H=3.
    # A: 120000/1.05 + 130000/1.05^2 + 130000/1.05^3
    #    = 114285.714 + 117913.832 + 112298.888 = 344498.434
    # B: 125000/1.05 + 125000/1.05^2 + 125000/1.05^3
    #    = 119047.619 + 113378.685 + 107979.700 = 340406.004
    def test_van_base(self):
        r = calcola_van_offerte_pluriennali(_offerte_base(), 1000.0, 5.0, 130.0)
        assert r["errore"] is None and r["valido"] is True
        assert r["orizzonte_anni"] == 3
        assert r["van"]["A"] == pytest.approx(344498.434, abs=0.01)
        assert r["van"]["B"] == pytest.approx(340406.004, abs=0.01)
        assert r["vincitore"] == "B"
        assert r["peggiore"] == "A"
        assert r["risparmio"] == pytest.approx(4092.43, abs=0.01)
        assert r["forward_annui"] == pytest.approx([130.0, 130.0, 130.0])
        # df_anni: Anno, Forward + 2 colonne costo
        assert list(r["df_anni"].columns)[:2] == ["Anno", "Forward €/MWh"]
        assert r["df_anni"].shape == (3, 4)
        assert r["df_anni"]["Costo att. «A» €"].iloc[0] == pytest.approx(114285.71, abs=0.01)
        # riepilogo ordinato per VAN crescente: B prima
        assert list(r["df_riepilogo"]["Offerta"]) == ["B", "A"]
        assert "«B»" in r["verdetto"]

    def test_canone_e_attivazione(self):
        off = _offerte_base()
        off[0]["canone_fisso_eur_mese"] = 50.0   # +600 €/anno
        off[0]["attivazione_eur"] = 1200.0       # una tantum a t=0
        r = calcola_van_offerte_pluriennali(off, 1000.0, 5.0, 130.0)
        delta = 1200.0 + 600.0 / 1.05 + 600.0 / 1.05 ** 2 + 600.0 / 1.05 ** 3
        assert r["van"]["A"] == pytest.approx(344498.434 + delta, abs=0.01)

    def test_escalation_forward(self):
        r = calcola_van_offerte_pluriennali(_offerte_base(), 1000.0, 5.0, 130.0,
                                            escalation_annua_pct=10.0)
        assert r["forward_annui"] == pytest.approx([130.0, 143.0, 157.3])
        # A anno 2: 143000/1.05^2 ; anno 3: 157300/1.05^3
        att2 = 143000.0 / 1.05 ** 2
        att3 = 157300.0 / 1.05 ** 3
        assert r["df_anni"]["Costo att. «A» €"].iloc[1] == pytest.approx(att2, abs=0.01)
        assert r["df_anni"]["Costo att. «A» €"].iloc[2] == pytest.approx(att3, abs=0.01)

    def test_tasso_zero(self):
        off = _offerte_base()
        r = calcola_van_offerte_pluriennali(off, 1000.0, 0.0, 130.0)
        assert r["van"]["B"] == pytest.approx(375000.0)
        assert r["rata_equivalente"]["B"] == pytest.approx(375000.0 / 3)
        assert r["van"]["A"] == pytest.approx(120000.0 + 130000.0 + 130000.0)

    def test_durata_float_intera_ok(self):
        off = _offerte_base()
        off[0]["durata_anni"] = 1.0  # arriva cosi' dal data_editor
        r = calcola_van_offerte_pluriennali(off, 1000.0, 5.0, 130.0)
        assert r["errore"] is None and r["valido"] is True
        assert r["orizzonte_anni"] == 3

    def test_orizzonte_da_durata_massima(self):
        off = [
            {"nome": "X", "prezzo_eur_mwh": 100.0, "durata_anni": 2},
            {"nome": "Y", "prezzo_eur_mwh": 100.0, "durata_anni": 5},
        ]
        r = calcola_van_offerte_pluriennali(off, 500.0, 3.0, 110.0)
        assert r["errore"] is None
        assert r["orizzonte_anni"] == 5
        assert r["df_anni"].shape[0] == 5


class TestErrori:
    def _e(self, *a, **k):
        r = calcola_van_offerte_pluriennali(*a, **k)
        assert r["errore"] is not None and r["valido"] is False
        return r

    def test_meno_di_due_offerte(self):
        self._e([], 1000.0, 5.0, 130.0)
        self._e([_offerte_base()[0]], 1000.0, 5.0, 130.0)
        self._e("non una lista", 1000.0, 5.0, 130.0)

    def test_offerta_non_dict(self):
        self._e(["x", _offerte_base()[1]], 1000.0, 5.0, 130.0)

    def test_nome_mancante(self):
        off = _offerte_base()
        off[0] = {"prezzo_eur_mwh": 120.0, "durata_anni": 1}
        self._e(off, 1000.0, 5.0, 130.0)

    def test_nomi_duplicati(self):
        off = _offerte_base()
        off[1]["nome"] = "A"
        self._e(off, 1000.0, 5.0, 130.0)

    def test_prezzo_non_valido(self):
        for p in (0.0, -5.0, float("nan"), float("inf"), "120", None):
            off = _offerte_base()
            off[0]["prezzo_eur_mwh"] = p
            self._e(off, 1000.0, 5.0, 130.0)

    def test_durata_non_valida(self):
        for d in (0, 11, 2.5, True, "3", None, float("nan")):
            off = _offerte_base()
            off[0]["durata_anni"] = d
            self._e(off, 1000.0, 5.0, 130.0)

    def test_canone_attivazione_negativi(self):
        off = _offerte_base()
        off[0]["canone_fisso_eur_mese"] = -1.0
        self._e(off, 1000.0, 5.0, 130.0)
        off = _offerte_base()
        off[1]["attivazione_eur"] = -10.0
        self._e(off, 1000.0, 5.0, 130.0)

    def test_parametri_globali_non_validi(self):
        self._e(_offerte_base(), 0.0, 5.0, 130.0)          # volume
        self._e(_offerte_base(), -100.0, 5.0, 130.0)
        self._e(_offerte_base(), 1000.0, -1.0, 130.0)      # tasso
        self._e(_offerte_base(), 1000.0, 60.0, 130.0)
        self._e(_offerte_base(), 1000.0, 5.0, 0.0)        # forward
        self._e(_offerte_base(), 1000.0, 5.0, 130.0,
                escalation_annua_pct=150.0)               # escalation
        self._e(_offerte_base(), 1000.0, float("nan"), 130.0)


class TestDeterminismo:
    def test_due_chiamate_uguali(self):
        r1 = calcola_van_offerte_pluriennali(_offerte_base(), 1000.0, 5.0, 130.0,
                                             escalation_annua_pct=7.5)
        r2 = calcola_van_offerte_pluriennali(_offerte_base(), 1000.0, 5.0, 130.0,
                                             escalation_annua_pct=7.5)
        assert r1["van"] == r2["van"]
        assert r1["df_anni"].equals(r2["df_anni"])
        assert r1["df_riepilogo"].equals(r2["df_riepilogo"])


class TestRegistry:
    def test_tab216_dichiarata(self):
        import ast as _ast
        src = APP.read_text(encoding="utf-8")
        tree = _ast.parse(src)
        titoli = None
        for node in _ast.walk(tree):
            if (isinstance(node, _ast.Assign)
                    and isinstance(node.value, _ast.Call)
                    and getattr(getattr(node.value.func, "attr", ""),
                                "lower", lambda: "")() == "tabs"
                                and node.value.args and hasattr(node.value.args[0], "elts")):
                titoli = [t.value for t in node.value.args[0].elts]
        assert titoli is not None
        assert len(titoli) == 344
        assert titoli[-1] == "🎲 Risk of ruin: probabilita' di toccare una barriera di drawdown"
        m = re.search(r"((?:tab\d+, )+tab\d+) = st.tabs\(\[", src)
        assert m is not None
        vars_tab = [v.strip() for v in m.group(1).split(",")]
        assert len(vars_tab) == 344
        assert "tab215" in vars_tab
        withs = re.findall(r"^\s*with (tab\d+):", src, re.M)
        assert len(withs) == len(vars_tab) == 344
        assert "tab216" in withs
        # key widget univoche della tab216
        keys = re.findall(r'key="(van216_[^"]+)"', src)
        assert len(keys) == len(set(keys)) == 6
