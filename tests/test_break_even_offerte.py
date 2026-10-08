"""Test tab217 'Break-even offerte': helper calcola_break_even_offerte —
punto di pareggio tra due offerte a parita' di profilo di consumo.

Stile pytest (vedi docs/AGGIUNGERE_TAB.md): la funzione viene estratta da
app.py via AST senza avviare Streamlit.
"""

import re
from pathlib import Path

import pandas as pd
import pytest

from appfuncs import load

_F = load("calcola_break_even_offerte", "_fmt_mwh")
calcola_break_even_offerte = _F["calcola_break_even_offerte"]

APP = Path(__file__).parent.parent / "app.py"


def _off(nome, prezzo_piatto, canone=0.0, attiv=0.0):
    return {"nome": nome, "prezzi": {"piatto": prezzo_piatto},
            "canone_eur_mese": canone, "attivazione_eur": attiv}


class TestNumeriAMano:
    # A: 120 €/MWh, canone 50/mese -> F_A = 600
    # B: 110 €/MWh, canone 120/mese -> F_B = 1440
    # V* = (1440-600)/(120-110) = 84 MWh
    def test_break_even_base(self):
        r = calcola_break_even_offerte(_off("Alfa", 120.0, 50.0),
                                       _off("Beta", 110.0, 120.0),
                                       (0.4, 0.35, 0.25))
        assert r["errore"] is None and r["valido"] is True
        assert r["volume_pareggio_mwh"] == pytest.approx(84.0)
        assert r["dominanza"] is None
        assert r["p_eff_a"] == pytest.approx(120.0)
        assert r["p_eff_b"] == pytest.approx(110.0)
        assert r["fisso_a"] == pytest.approx(600.0)
        assert r["fisso_b"] == pytest.approx(1440.0)
        assert r["vincitore_bassi_volumi"] == "A"
        assert r["vincitore_alti_volumi"] == "B"
        assert "84" in r["verdetto"] and "Alfa" in r["verdetto"]

    def test_prezzo_fasce_pesato(self):
        # p_eff_A = 0.4*135 + 0.35*118 + 0.25*95 = 119.05
        # V* = 840/(119.05-110) = 92.8176...
        a = {"nome": "Alfa", "prezzi": {"F1": 135.0, "F2": 118.0, "F3": 95.0},
             "canone_eur_mese": 50.0, "attivazione_eur": 0.0}
        r = calcola_break_even_offerte(a, _off("Beta", 110.0, 120.0),
                                       (0.4, 0.35, 0.25))
        assert r["p_eff_a"] == pytest.approx(119.05)
        assert r["volume_pareggio_mwh"] == pytest.approx(840.0 / 9.05)

    def test_attivazione_conta_nei_fissi(self):
        # A: 100 €/MWh + 5000 attivazione; B: 110 €/MWh, nessun fisso
        # V* = (0-5000)/(100-110) = 500 MWh; sotto vince B, sopra A
        r = calcola_break_even_offerte(_off("Alfa", 100.0, 0.0, 5000.0),
                                       _off("Beta", 110.0),
                                       (1.0, 0.0, 0.0))
        assert r["fisso_a"] == pytest.approx(5000.0)
        assert r["volume_pareggio_mwh"] == pytest.approx(500.0)
        assert r["vincitore_bassi_volumi"] == "B"
        assert r["vincitore_alti_volumi"] == "A"

    def test_offerte_identitche_pareggio(self):
        r = calcola_break_even_offerte(_off("Alfa", 120.0, 50.0),
                                       _off("Beta", 120.0, 50.0),
                                       (0.5, 0.3, 0.2))
        assert r["valido"] and r["dominanza"] == "pareggio"
        assert r["volume_pareggio_mwh"] is None

    def test_stesso_prezzo_vince_fissi_bassi(self):
        r = calcola_break_even_offerte(_off("Alfa", 100.0, 50.0),
                                       _off("Beta", 100.0, 120.0),
                                       (0.5, 0.3, 0.2))
        assert r["valido"] and r["dominanza"] == "A"
        assert r["volume_pareggio_mwh"] is None

    def test_dominanza_prezzo_e_fissi(self):
        # A piu' economica sia al MWh che nei fissi -> V* negativo -> domina A
        r = calcola_break_even_offerte(_off("Alfa", 100.0, 50.0),
                                       _off("Beta", 110.0, 120.0),
                                       (0.5, 0.3, 0.2))
        assert r["valido"] and r["dominanza"] == "A"
        assert r["volume_pareggio_mwh"] is None

    def test_quote_normalizzate(self):
        a = {"nome": "Alfa", "prezzi": {"F1": 135.0, "F2": 118.0, "F3": 95.0},
             "canone_eur_mese": 50.0, "attivazione_eur": 0.0}
        r1 = calcola_break_even_offerte(a, _off("Beta", 110.0, 120.0), (40, 35, 25))
        r2 = calcola_break_even_offerte(a, _off("Beta", 110.0, 120.0), (0.4, 0.35, 0.25))
        assert r1["p_eff_a"] == pytest.approx(r2["p_eff_a"])
        assert r1["volume_pareggio_mwh"] == pytest.approx(r2["volume_pareggio_mwh"])

    def test_break_even_oltre_volume_max(self):
        r = calcola_break_even_offerte(_off("Alfa", 120.0, 50.0),
                                       _off("Beta", 110.0, 120.0),
                                       (0.4, 0.35, 0.25), volume_max_mwh=50.0)
        assert r["volume_pareggio_mwh"] == pytest.approx(84.0)
        assert "oltre il volume massimo" in r["verdetto"]

    def test_curva_costi(self):
        r = calcola_break_even_offerte(_off("Alfa", 120.0, 50.0),
                                       _off("Beta", 110.0, 120.0),
                                       (0.4, 0.35, 0.25),
                                       volume_max_mwh=1000.0, n_punti=11)
        df = r["df_curva"]
        assert isinstance(df, pd.DataFrame) and len(df) == 11
        assert list(df.columns) == ["Volume MWh", "Costo «Alfa» €", "Costo «Beta» €"]
        # a volume 0 il costo e' il fisso annuo
        assert df.iloc[0]["Costo «Alfa» €"] == pytest.approx(600.0)
        assert df.iloc[0]["Costo «Beta» €"] == pytest.approx(1440.0)
        # al break-even i costi coincidono: 84*120+600 = 10680
        assert 84.0 * 120.0 + 600.0 == pytest.approx(84.0 * 110.0 + 1440.0)


class TestErrori:
    def test_offerta_non_dict(self):
        r = calcola_break_even_offerte("no", _off("Beta", 110.0), (0.4, 0.35, 0.25))
        assert r["errore"] and not r["valido"]

    def test_nome_mancante(self):
        a = _off("", 120.0)
        r = calcola_break_even_offerte(a, _off("Beta", 110.0), (0.4, 0.35, 0.25))
        assert "nome mancante" in r["errore"]

    def test_nomi_duplicati(self):
        r = calcola_break_even_offerte(_off("X", 120.0), _off("X", 110.0),
                                       (0.4, 0.35, 0.25))
        assert "nomi diversi" in r["errore"]

    def test_prezzo_negativo(self):
        r = calcola_break_even_offerte(_off("Alfa", -5.0), _off("Beta", 110.0),
                                       (0.4, 0.35, 0.25))
        assert ">= 0" in r["errore"]

    def test_canone_negativo(self):
        r = calcola_break_even_offerte(_off("Alfa", 120.0, -1.0), _off("Beta", 110.0),
                                       (0.4, 0.35, 0.25))
        assert "canone" in r["errore"]

    def test_prezzi_mancanti(self):
        r = calcola_break_even_offerte({"nome": "Alfa"}, _off("Beta", 110.0),
                                       (0.4, 0.35, 0.25))
        assert "prezzi mancanti" in r["errore"]

    def test_fascia_mancante(self):
        a = {"nome": "Alfa", "prezzi": {"F1": 135.0, "F2": 118.0},
             "canone_eur_mese": 0.0, "attivazione_eur": 0.0}
        r = calcola_break_even_offerte(a, _off("Beta", 110.0), (0.4, 0.35, 0.25))
        assert "F3" in r["errore"]

    def test_quote_negative(self):
        r = calcola_break_even_offerte(_off("Alfa", 120.0), _off("Beta", 110.0),
                                       (0.5, -0.1, 0.6))
        assert "Quote fasce" in r["errore"]

    def test_quote_somma_zero(self):
        r = calcola_break_even_offerte(_off("Alfa", 120.0), _off("Beta", 110.0),
                                       (0.0, 0.0, 0.0))
        assert "Quote fasce" in r["errore"]

    def test_volume_max_non_valido(self):
        r = calcola_break_even_offerte(_off("Alfa", 120.0), _off("Beta", 110.0),
                                       (0.4, 0.35, 0.25), volume_max_mwh=-10.0)
        assert "Volume massimo" in r["errore"]

    def test_n_punti_non_valido(self):
        r = calcola_break_even_offerte(_off("Alfa", 120.0), _off("Beta", 110.0),
                                       (0.4, 0.35, 0.25), n_punti=1)
        assert "n_punti" in r["errore"]
        r2 = calcola_break_even_offerte(_off("Alfa", 120.0), _off("Beta", 110.0),
                                        (0.4, 0.35, 0.25), n_punti=True)
        assert "n_punti" in r2["errore"]


class TestDeterminismo:
    def test_due_chiamate_uguali(self):
        kw = dict(volume_max_mwh=2000.0, n_punti=51)
        r1 = calcola_break_even_offerte(_off("Alfa", 120.0, 50.0),
                                        _off("Beta", 110.0, 120.0),
                                        (0.4, 0.35, 0.25), **kw)
        r2 = calcola_break_even_offerte(_off("Alfa", 120.0, 50.0),
                                        _off("Beta", 110.0, 120.0),
                                        (0.4, 0.35, 0.25), **kw)
        assert r1["volume_pareggio_mwh"] == r2["volume_pareggio_mwh"]
        assert r1["verdetto"] == r2["verdetto"]
        pd.testing.assert_frame_equal(r1["df_curva"], r2["df_curva"])


class TestRegistry:
    def test_tab217_dichiarata(self):
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
        assert len(titoli) == 314
        assert titoli[-1] == "⏳📉 VaR multi-orizzonte: lo scaling con autocorrelazione dei rendimenti"
        m = re.search(r"((?:tab\d+, )+tab\d+) = st.tabs\(\[", src)
        assert m is not None
        vars_tab = [v.strip() for v in m.group(1).split(",")]
        assert len(vars_tab) == 314
        assert "tab216" in vars_tab
        withs = re.findall(r"^\s*with (tab\d+):", src, re.M)
        assert len(withs) == len(vars_tab) == 314
        assert "tab217" in withs
        # key widget univoche della tab217
        keys = re.findall(r'key="(be217_[^"]+)"', src)
        assert len(keys) == len(set(keys)) == 21
