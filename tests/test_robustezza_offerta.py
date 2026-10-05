"""Test tab215 'Robustezza offerta': helper calcola_robustezza_offerta —
valutazione di offerte a fasce F1/F2/F3 sul profilo di carico reale +
stress-test della classifica con spostamenti del carico.

Stile pytest (vedi docs/AGGIUNGERE_TAB.md): la funzione viene estratta da
app.py via AST senza avviare Streamlit.
"""

import re
from pathlib import Path

import pandas as pd
import pytest

from appfuncs import load

_F = load("fascia_oraria", "calcola_robustezza_offerta")
calcola_robustezza_offerta = _F["calcola_robustezza_offerta"]

APP = Path(__file__).parent.parent / "app.py"


def _lunedi_24h():
    # 2026-01-05 e' un lunedi': F1 = ore 8-18 (11h), F2 = 7,19-22 (5h),
    # F3 = 0-6,23 (8h). Con 1 MW per fascia: 11 / 5 / 8 MWh.
    idx = pd.date_range("2026-01-05", periods=24, freq="h")
    return pd.Series(100.0, index=idx)


def _offerte_base():
    return [
        {"nome": "A-piatta", "prezzo_energia": 100.0,
         "canone_fisso_eur_mese": 0.0},
        {"nome": "B-fasce", "prezzo_f1": 130.0, "prezzo_f2": 100.0,
         "prezzo_f3": 70.0, "canone_fisso_eur_mese": 0.0},
    ]


class TestNumeriAMano:
    def test_quattro_scenari(self):
        # q = 50%: scenario "picco": F1=17.5, F2=2.5, F3=4
        #   B = 17.5*130 + 2.5*100 + 4*70 = 2805 ; A = 2400 -> vince A
        # scenario "notte": F1=5.5, F2=5, F3=13.5
        #   B = 5.5*130 + 5*100 + 13.5*70 = 2160 ; A = 2400 -> vince B
        # scenario "piatto": come il base (11/5/8): A=2400, B=2490 -> vince A
        r = calcola_robustezza_offerta(_lunedi_24h(), 1.0, 1.0, 1.0,
                                       _offerte_base(), spostamento_pct=50.0)
        assert r["errore"] is None and r["valido"] is True
        assert r["n_ore"] == 24
        assert r["mwh_fasce"] == pytest.approx({"F1": 11.0, "F2": 5.0, "F3": 8.0})
        assert r["mesi_equiv"] == pytest.approx(24.0 / 730.5)
        assert r["scenari"] == ["Profilo attuale", "Verso picco (+50% F1)",
                                "Verso notte (+50% F3)", "Profilo piatto"]
        assert r["vincitore_base"] == "A-piatta"
        assert r["vincitore_robusto"] == "A-piatta"
        assert r["vittorie"] == {"A-piatta": 3, "B-fasce": 1}
        df = r["df_scenari"]
        assert list(df["Vincitore"]) == ["A-piatta", "A-piatta",
                                         "B-fasce", "A-piatta"]
        costi_b = df.set_index("Scenario").loc["Verso notte (+50% F3)"]
        assert costi_b["A-piatta"] == pytest.approx(2400.0)
        assert costi_b["B-fasce"] == pytest.approx(2160.0)
        costi_p = df.set_index("Scenario").loc["Verso picco (+50% F1)"]
        assert costi_p["B-fasce"] == pytest.approx(2805.0)
        # rimpianti: A perde 240 nello scenario notte; B perde 405 in picco
        assert r["rimpianto"]["A-piatta"] == pytest.approx(240.0)
        assert r["rimpianto"]["B-fasce"] == pytest.approx(405.0)
        assert r["rimpianto_max"] == pytest.approx(405.0)
        # df_base ordinata per costo: A prima, delta B = 90
        db = r["df_base"]
        assert list(db["Offerta"]) == ["A-piatta", "B-fasce"]
        assert list(db["Costo totale (€)"]) == pytest.approx([2400.0, 2490.0])
        assert list(db["Δ vs migliore (€)"]) == pytest.approx([0.0, 90.0])
        assert "A-piatta" in r["verdetto"]

    def test_canone_e_sconto(self):
        # C: piatto 100 con sconto 10% -> 2160 ; D: piatto 95 + canone 100/mese
        # D = 24*95 + 100*(24/730.5) = 2280 + 3.285... -> vince C
        offerte = [
            {"nome": "C", "prezzo_energia": 100.0, "sconto_pct": 10.0},
            {"nome": "D", "prezzo_energia": 95.0,
             "canone_fisso_eur_mese": 100.0},
        ]
        r = calcola_robustezza_offerta(_lunedi_24h(), 1.0, 1.0, 1.0, offerte,
                                       spostamento_pct=20.0)
        assert r["errore"] is None and r["valido"] is True
        db = r["df_base"]
        assert list(db["Offerta"]) == ["C", "D"]
        assert db["Costo totale (€)"].iloc[0] == pytest.approx(2160.0)
        assert db["Costo totale (€)"].iloc[1] == pytest.approx(
            round(2280.0 + 100.0 * 24.0 / 730.5, 2))
        assert db["Canone (€)"].iloc[1] == pytest.approx(
            round(100.0 * 24.0 / 730.5, 2))

    def test_fasce_parziali_usano_piatto(self):
        # solo F1 valorizzata (110), resto dal piatto 100: base 11*110+5*100+8*100
        offerte = [
            {"nome": "E", "prezzo_f1": 110.0, "prezzo_energia": 100.0},
            {"nome": "F", "prezzo_energia": 105.0},
        ]
        r = calcola_robustezza_offerta(_lunedi_24h(), 1.0, 1.0, 1.0, offerte)
        assert r["errore"] is None
        db = r["df_base"]
        assert db.set_index("Offerta").loc["E", "Costo totale (€)"] == pytest.approx(
            11 * 110.0 + 5 * 100.0 + 8 * 100.0)
        assert db.set_index("Offerta").loc["F", "Costo totale (€)"] == pytest.approx(
            24 * 105.0)


class TestErrori:
    def test_serie_vuota(self):
        s = pd.Series(dtype=float)
        r = calcola_robustezza_offerta(s, 1.0, 1.0, 1.0, _offerte_base())
        assert r["valido"] is False and r["errore"]

    def test_indice_non_datetime(self):
        s = pd.Series([100.0, 100.0], index=[0, 1])
        r = calcola_robustezza_offerta(s, 1.0, 1.0, 1.0, _offerte_base())
        assert r["valido"] is False and r["errore"]

    def test_una_sola_offerta(self):
        r = calcola_robustezza_offerta(_lunedi_24h(), 1.0, 1.0, 1.0,
                                       [_offerte_base()[0]])
        assert r["valido"] is False and "2 offerte" in r["errore"]

    def test_prezzo_negativo(self):
        off = [{"nome": "X", "prezzo_energia": -5.0},
               {"nome": "Y", "prezzo_energia": 100.0}]
        r = calcola_robustezza_offerta(_lunedi_24h(), 1.0, 1.0, 1.0, off)
        assert r["valido"] is False and r["errore"]

    def test_senza_prezzi(self):
        off = [{"nome": "X"}, {"nome": "Y", "prezzo_energia": 100.0}]
        r = calcola_robustezza_offerta(_lunedi_24h(), 1.0, 1.0, 1.0, off)
        assert r["valido"] is False and r["errore"]

    def test_canone_negativo(self):
        off = [{"nome": "X", "prezzo_energia": 100.0,
                "canone_fisso_eur_mese": -10.0},
               {"nome": "Y", "prezzo_energia": 100.0}]
        r = calcola_robustezza_offerta(_lunedi_24h(), 1.0, 1.0, 1.0, off)
        assert r["valido"] is False and r["errore"]

    def test_sconto_fuori_range(self):
        off = [{"nome": "X", "prezzo_energia": 100.0, "sconto_pct": 150.0},
               {"nome": "Y", "prezzo_energia": 100.0}]
        r = calcola_robustezza_offerta(_lunedi_24h(), 1.0, 1.0, 1.0, off)
        assert r["valido"] is False and r["errore"]

    def test_nomi_duplicati(self):
        off = [{"nome": "X", "prezzo_energia": 100.0},
               {"nome": "X", "prezzo_energia": 90.0}]
        r = calcola_robustezza_offerta(_lunedi_24h(), 1.0, 1.0, 1.0, off)
        assert r["valido"] is False and "univoci" in r["errore"]

    def test_profilo_nullo(self):
        r = calcola_robustezza_offerta(_lunedi_24h(), 0.0, 0.0, 0.0,
                                       _offerte_base())
        assert r["valido"] is False and r["errore"]

    def test_mw_negativo(self):
        r = calcola_robustezza_offerta(_lunedi_24h(), 1.0, -1.0, 1.0,
                                       _offerte_base())
        assert r["valido"] is False and r["errore"]


class TestRobustezza:
    def test_determinismo(self):
        kw = dict(mw_f1=2.0, mw_f2=1.5, mw_f3=1.0,
                  offerte=_offerte_base(), spostamento_pct=20.0)
        r1 = calcola_robustezza_offerta(_lunedi_24h(), **kw)
        r2 = calcola_robustezza_offerta(_lunedi_24h(), **kw)
        pd.testing.assert_frame_equal(r1["df_base"], r2["df_base"])
        pd.testing.assert_frame_equal(r1["df_scenari"], r2["df_scenari"])
        assert r1["verdetto"] == r2["verdetto"]

    def test_q_zero_tutti_uguali(self):
        # con spostamento 0 gli scenari coincidono: 4 vittorie al vincitore base
        r = calcola_robustezza_offerta(_lunedi_24h(), 1.0, 1.0, 1.0,
                                       _offerte_base(), spostamento_pct=0.0)
        assert r["errore"] is None
        assert r["vittorie"][r["vincitore_base"]] == 4
        assert r["rimpianto_max"] == pytest.approx(
            abs(r["df_base"]["Costo totale (€)"].iloc[0]
                - r["df_base"]["Costo totale (€)"].iloc[1]))

    def test_tz_aware(self):
        idx = pd.date_range("2026-01-05", periods=24, freq="h", tz="Europe/Zurich")
        s = pd.Series(100.0, index=idx)
        r = calcola_robustezza_offerta(s, 1.0, 1.0, 1.0, _offerte_base())
        assert r["errore"] is None and r["valido"] is True


class TestRegistry:
    def test_tab215_dichiarata(self):
        import ast as _ast
        src = APP.read_text(encoding="utf-8")
        tree = _ast.parse(src)
        titoli = None
        for node in _ast.walk(tree):
            if (isinstance(node, _ast.Assign)
                    and isinstance(node.value, _ast.Call)
                    and getattr(getattr(node.value.func, "attr", ""),
                                "lower", lambda: "")() == "tabs"):
                titoli = [t.value for t in node.value.args[0].elts]
        assert titoli is not None
        assert len(titoli) == 220
        assert titoli[-1] == "🌍 Costo CBAM stimato"
        m = re.search(r"((?:tab\d+, )+tab220) = st\.tabs\(\[", src)
        assert m is not None
        vars_tab = [v.strip() for v in m.group(1).split(",")]
        assert len(vars_tab) == 220
        assert "tab214" in vars_tab
        withs = re.findall(r"^\s*with (tab\d+):", src, re.M)
        assert len(withs) == len(vars_tab) == 220
        assert "tab215" in withs
        # key widget univoche della tab215
        keys = re.findall(r'key="(rob215_[^"]+)"', src)
        assert len(keys) == len(set(keys)) == 6
