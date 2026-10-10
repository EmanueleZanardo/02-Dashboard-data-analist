"""Test tab212 'Costo di uscita contratto': helper calcola_costo_uscita —
VAN di uscita anticipata da un contratto a prezzo fisso vs forward,
forward di pareggio, tabella mensile.

Stile pytest (vedi docs/AGGIUNGERE_TAB.md): la funzione viene estratta da
app.py via AST senza avviare Streamlit.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("calcola_costo_uscita")
calcola_costo_uscita = _F["calcola_costo_uscita"]

APP = Path(__file__).parent.parent / "app.py"

# P=100, V=50 MWh/mese, N=6 mesi, F=80, r=0, penale=0
BASE = dict(prezzo_fisso_eur_mwh=100.0, volume_mensile_mwh=50.0,
            mesi_residui=6, forward_eur_mwh=80.0,
            tasso_annuo_pct=0.0, penale_eur=0.0)


class TestCasiBase:
    def test_numeri_a_mano(self):
        r = calcola_costo_uscita(**BASE)
        assert r["errore"] is None and r["valido"] is True
        assert r["risparmio_unitario"] == pytest.approx(20.0)
        assert r["risparmio_mensile"] == pytest.approx(1000.0)
        assert r["risparmio_totale"] == pytest.approx(6000.0)
        assert r["van_uscita"] == pytest.approx(6000.0)
        assert r["forward_pareggio"] == pytest.approx(100.0)
        assert r["verdetto"] == "CONVIENE USCIRE"

    def test_tabella_mensile(self):
        r = calcola_costo_uscita(**BASE)
        df = r["df"]
        assert len(df) == 6
        assert list(df["Mese"]) == [1, 2, 3, 4, 5, 6]
        assert (df["Risparmio mensile (€)"] == 1000.0).all()
        assert df["Cumulato attualizzato (€)"].iloc[-1] == pytest.approx(6000.0)
        # cumulato crescente di 1000 al mese
        assert list(df["Cumulato attualizzato (€)"]) == \
            [pytest.approx(1000.0 * k) for k in range(1, 7)]

    def test_penale_riduce_van(self):
        r = calcola_costo_uscita(**dict(BASE, penale_eur=1200.0))
        assert r["van_uscita"] == pytest.approx(4800.0)
        # F* = P - penale / (V * A), A = 6 a tasso 0 -> 100 - 1200/300 = 96
        assert r["forward_pareggio"] == pytest.approx(96.0)
        assert r["verdetto"] == "CONVIENE USCIRE"

    def test_penale_alta_rende_antieconomico(self):
        r = calcola_costo_uscita(**dict(BASE, penale_eur=7000.0))
        assert r["van_uscita"] == pytest.approx(-1000.0)
        assert r["verdetto"] == "RESTA NEL CONTRATTO"

    def test_forward_sopra_fisso_resta(self):
        r = calcola_costo_uscita(**dict(BASE, forward_eur_mwh=110.0))
        assert r["risparmio_unitario"] == pytest.approx(-10.0)
        assert r["van_uscita"] == pytest.approx(-3000.0)
        assert r["verdetto"] == "RESTA NEL CONTRATTO"

    def test_forward_uguale_fisso_indifferente(self):
        r = calcola_costo_uscita(**dict(BASE, forward_eur_mwh=100.0))
        assert r["van_uscita"] == pytest.approx(0.0)
        assert r["verdetto"] == "INDIFFERENTE"

    def test_tasso_attualizza(self):
        # replica indipendente: 1000 / 1.12^(k/12)
        att = sum(1000.0 / 1.12 ** (k / 12.0) for k in range(1, 7))
        r = calcola_costo_uscita(**dict(BASE, tasso_annuo_pct=12.0))
        assert r["van_uscita"] == pytest.approx(att)
        assert r["van_uscita"] < 6000.0
        # pareggio con penale e tasso: F* = P - penale/(V*A)
        r2 = calcola_costo_uscita(**dict(BASE, tasso_annuo_pct=12.0,
                                        penale_eur=600.0))
        a = sum(1.0 / 1.12 ** (k / 12.0) for k in range(1, 7))
        assert r2["forward_pareggio"] == pytest.approx(100.0 - 600.0 / (50.0 * a))

    def test_mesi_1(self):
        r = calcola_costo_uscita(**dict(BASE, mesi_residui=1))
        assert len(r["df"]) == 1
        assert r["van_uscita"] == pytest.approx(1000.0)


class TestErrori:
    @pytest.mark.parametrize("kw", [
        dict(prezzo_fisso_eur_mwh=0.0),
        dict(prezzo_fisso_eur_mwh=-5.0),
        dict(volume_mensile_mwh=0.0),
        dict(volume_mensile_mwh=-1.0),
        dict(mesi_residui=0),
        dict(mesi_residui=61),
        dict(mesi_residui=2.5),
        dict(forward_eur_mwh=0.0),
        dict(forward_eur_mwh=-3.0),
        dict(tasso_annuo_pct=-1.0),
        dict(penale_eur=-10.0),
        dict(prezzo_fisso_eur_mwh="abc"),
        dict(forward_eur_mwh=None),
    ])
    def test_input_non_validi(self, kw):
        p = dict(BASE)
        p.update(kw)
        r = calcola_costo_uscita(**p)
        assert r["valido"] is False
        assert isinstance(r["errore"], str) and r["errore"]


class TestRobustezza:
    def test_determinismo(self):
        r1 = calcola_costo_uscita(**BASE)
        r2 = calcola_costo_uscita(**BASE)
        assert r1["van_uscita"] == r2["van_uscita"]
        assert r1["df"].equals(r2["df"])

    def test_mesi_massimi(self):
        r = calcola_costo_uscita(**dict(BASE, mesi_residui=60))
        assert r["valido"] is True and len(r["df"]) == 60

    def test_penale_default_zero(self):
        p = dict(BASE)
        del p["penale_eur"]
        r = calcola_costo_uscita(**p)
        assert r["valido"] is True
        assert r["van_uscita"] == pytest.approx(6000.0)


# ------------------------------------------------------- registry
class TestRegistryTab212:
    def test_tab212_dichiarata(self):
        src = APP.read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 357
        assert titoli[-1] == "Kelly con lotti interi: sizing discreto e drag di arrotondamento"
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab212" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab212" in withs
        assert len(withs) == len(dvars) == 357
        keys = re.findall(r'key="(usc212_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 7
