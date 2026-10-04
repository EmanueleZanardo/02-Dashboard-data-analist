"""Test tab208 'Confronto fornitori': helper calcola_confronto_fornitori —
confronto offerte di fornitura energia su un consumo annuo dato.

Stile pytest (vedi docs/AGGIUNGERE_TAB.md): la funzione viene estratta da
app.py via AST senza avviare Streamlit.
"""

from appfuncs import load

_F = load("calcola_confronto_fornitori")
calcola_confronto_fornitori = _F["calcola_confronto_fornitori"]


def _offerte():
    return [
        {"nome": "A", "quota_energia": 90.0, "quota_fissa": 120.0,
         "quota_potenza": 0.0, "kw": 0.0},
        {"nome": "B", "quota_energia": 85.0, "quota_fissa": 600.0,
         "quota_potenza": 0.0, "kw": 0.0},
    ]


class TestCasiBase:
    def test_numeri_a_mano(self):
        # A: 90*100 + 120 = 9120 ; B: 85*100 + 600 = 9100 -> migliore B
        r = calcola_confronto_fornitori(100, _offerte())
        assert r["errore"] is None and r["valido"] is True
        tot = dict(zip(r["df"]["Fornitore"], r["df"]["Totale €"]))
        assert tot["A"] == 9120.0
        assert tot["B"] == 9100.0
        assert r["migliore"] == "B"
        assert r["delta"]["A"] == 20.0
        assert r["delta"]["B"] == 0.0

    def test_colonne_df(self):
        r = calcola_confronto_fornitori(100, _offerte())
        assert list(r["df"].columns) == [
            "Fornitore", "Quota energia €", "Quota fissa €",
            "Quota potenza €", "Totale €"]
        assert len(r["df"]) == 2

    def test_quota_potenza(self):
        offerte = [
            {"nome": "X", "quota_energia": 90.0, "quota_fissa": 0.0,
             "quota_potenza": 10.0, "kw": 50.0},   # 9000 + 500 = 9500
            {"nome": "Y", "quota_energia": 95.0, "quota_fissa": 0.0,
             "quota_potenza": 0.0, "kw": 0.0},      # 9500
        ]
        r = calcola_confronto_fornitori(100, offerte)
        tot = dict(zip(r["df"]["Fornitore"], r["df"]["Totale €"]))
        assert tot["X"] == 9500.0
        assert tot["Y"] == 9500.0
        assert r["delta"]["X"] == 0.0 and r["delta"]["Y"] == 0.0

    def test_offerte_vuote(self):
        for bad in ([], (), None, "no"):
            r = calcola_confronto_fornitori(100, bad)
            assert r["errore"], bad
            assert r["valido"] is False
            assert r["df"] is None and r["migliore"] is None

    def test_consumo_non_positivo(self):
        for bad in (0, -5, float("nan"), "x", None):
            r = calcola_confronto_fornitori(bad, _offerte())
            assert r["errore"], bad
            assert r["valido"] is False

    def test_input_strani_senza_eccezioni(self):
        r = calcola_confronto_fornitori(100, [{"nome": "A"}])
        assert r["errore"]
        r = calcola_confronto_fornitori(
            100, [{"nome": "A", "quota_energia": -1.0,
                   "quota_fissa": 0.0, "quota_potenza": 0.0, "kw": 0.0}])
        assert r["errore"]
        r = calcola_confronto_fornitori(100, [{"no_dict": True}])
        assert r["errore"]
        r = calcola_confronto_fornitori(100, ["A"])
        assert r["errore"]

    def test_determinismo(self):
        a = calcola_confronto_fornitori(100, _offerte())
        b = calcola_confronto_fornitori(100, _offerte())
        assert a["migliore"] == b["migliore"]
        assert a["delta"] == b["delta"]
        assert a["df"].equals(b["df"])
