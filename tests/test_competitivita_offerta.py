"""Test tab206 'Competitivita' offerta': helper calcola_competitivita_offerta —
sconto/premio vs prezzo di mercato, risparmio annuo, verdetto su margine
target, scenari mercato +/-10%.

Stile pytest (vedi docs/AGGIUNGERE_TAB.md): la funzione viene estratta da
app.py via AST senza avviare Streamlit.
"""

from appfuncs import load

_F = load("calcola_competitivita_offerta")
calcola_competitivita_offerta = _F["calcola_competitivita_offerta"]


class TestCasiBase:
    def test_numeri_a_mano(self):
        # mercato 100, offerta 92, consumo 1000, margine 5%
        r = calcola_competitivita_offerta(100, 92, 1000, 5)
        assert r["errore"] is None and r["valido"] is True
        assert abs(r["sconto_pct"] - 8.0) < 1e-9
        assert abs(r["risparmio_annuo"] - 8000.0) < 1e-9
        # offerta 92 <= 100 * (1 - 0.05) = 95 -> competitiva
        assert r["competitiva"] is True

    def test_non_competitiva_sul_margine(self):
        r = calcola_competitivita_offerta(100, 97, 1000, 5)
        assert r["valido"] is True
        assert r["competitiva"] is False  # 97 > 95, sconto insufficiente

    def test_competitiva_al_limite(self):
        # offerta esattamente alla soglia: competitiva (<=)
        r = calcola_competitivita_offerta(100, 95, 1000, 5)
        assert r["competitiva"] is True

    def test_premio_sopra_mercato(self):
        # offerta sopra il mercato: sconto e risparmio negativi
        r = calcola_competitivita_offerta(100, 105, 1000, 0)
        assert abs(r["sconto_pct"] - (-5.0)) < 1e-9
        assert abs(r["risparmio_annuo"] - (-5000.0)) < 1e-9
        assert r["competitiva"] is False

    def test_margine_zero(self):
        r = calcola_competitivita_offerta(100, 100, 1000, 0)
        assert r["competitiva"] is True
        assert abs(r["sconto_pct"]) < 1e-9
        assert abs(r["risparmio_annuo"]) < 1e-9

    def test_df_scenari(self):
        r = calcola_competitivita_offerta(100, 92, 1000, 5)
        df = r["df_scenari"]
        assert list(df.columns) == [
            "Scenario", "Prezzo mercato (EUR/MWh)",
            "Risparmio annuo (EUR)"]
        assert list(df["Scenario"]) == ["-10%", "-5%", "Base", "+5%", "+10%"]
        assert list(df["Prezzo mercato (EUR/MWh)"]) == [
            90.0, 95.0, 100.0, 105.0, 110.0]
        assert df["Risparmio annuo (EUR)"][0] == (90 - 92) * 1000  # -2000
        assert df["Risparmio annuo (EUR)"][2] == (100 - 92) * 1000  # 8000
        assert df["Risparmio annuo (EUR)"][4] == (110 - 92) * 1000  # 18000

    def test_input_non_validi(self):
        casi = [
            (0, 92, 1000, 5), (-1, 92, 1000, 5),        # mercato <= 0
            (100, 0, 1000, 5), (100, -3, 1000, 5),      # offerta <= 0
            (100, 92, 0, 5), (100, 92, -10, 5),         # consumo <= 0
            (100, 92, 1000, -1), (100, 92, 1000, 100),  # margine fuori [0,100)
            (float("nan"), 92, 1000, 5),                # NaN
            ("x", 92, 1000, 5), (100, None, 1000, 5),  # non numerici
        ]
        for args in casi:
            r = calcola_competitivita_offerta(*args)  # nessuna eccezione
            assert r["valido"] is False and r["errore"], args

    def test_determinismo(self):
        a = calcola_competitivita_offerta(100, 92, 1000, 5)
        b = calcola_competitivita_offerta(100, 92, 1000, 5)
        assert a["sconto_pct"] == b["sconto_pct"]
        assert a["risparmio_annuo"] == b["risparmio_annuo"]
        assert a["competitiva"] == b["competitiva"]
        assert a["df_scenari"].equals(b["df_scenari"])
