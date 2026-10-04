"""Test tab209 'Sconto pronta cassa': helper calcola_sconto_pronta_cassa —
tasso implicito annualizzato dello sconto per pagamento anticipato vs WACC.

Stile pytest (vedi docs/AGGIUNGERE_TAB.md): la funzione viene estratta da
app.py via AST senza avviare Streamlit.
"""

import numpy as np  # noqa: F401

from appfuncs import load

_F = load("calcola_sconto_pronta_cassa")
calcola_sconto_pronta_cassa = _F["calcola_sconto_pronta_cassa"]


class TestCasiBase:
    def test_numeri_a_mano(self):
        # importo 100000, sconto 2%, 30 gg, WACC 5%
        # tasso = (0.02/0.98) * (365/30) * 100 = 24.83 % circa
        r = calcola_sconto_pronta_cassa(100000, 2.0, 30, 5.0)
        assert r["errore"] is None and r["valido"] is True
        assert abs(r["tasso_implicito_pct"] - 24.83) < 0.01
        assert abs(r["costo_sconto_eur"] - 2000.0) < 1e-9
        assert abs(r["costo_wacc_eur"] - 100000 * 0.05 * 30 / 365) < 1e-9
        assert r["conviene"] is True
        assert isinstance(r["conviene"], bool)
        assert abs(r["risparmio_vs_wacc_eur"]
                   - (2000.0 - 100000 * 0.05 * 30 / 365)) < 1e-9

    def test_sensibilita(self):
        r = calcola_sconto_pronta_cassa(100000, 2.0, 30, 5.0)
        df = r["df_sensibilita"]
        assert len(df) == 84
        assert list(df.columns) == ["Giorni anticipo",
                                    "Tasso implicito (%/anno)"]
        assert df["Giorni anticipo"].iloc[0] == 7
        assert df["Giorni anticipo"].iloc[-1] == 90
        # riga a 30 gg coerente con lo scalare
        t30 = df[df["Giorni anticipo"] == 30][
            "Tasso implicito (%/anno)"].iloc[0]
        assert abs(t30 - r["tasso_implicito_pct"]) < 1e-9
        # il tasso implicito cala al crescere dei giorni
        t = df["Tasso implicito (%/anno)"].values
        assert all(t[i] > t[i + 1] for i in range(len(t) - 1))

    def test_non_conviene(self):
        # sconto piccolo e anticipo lungo -> tasso implicito sotto il WACC
        r = calcola_sconto_pronta_cassa(100000, 1.0, 90, 5.0)
        assert r["errore"] is None
        assert r["conviene"] is False
        assert r["tasso_implicito_pct"] < 5.0

    def test_sconto_zero_errore(self):
        # sconto 0 (e fuori range) -> errore, nessuna eccezione
        r = calcola_sconto_pronta_cassa(100000, 0.0, 30, 5.0)
        assert r["valido"] is False and r["errore"]

    def test_input_non_validi(self):
        base = [100000, 2.0, 30, 5.0]
        for i, bad in [(0, 0.0), (0, -1.0),
                       (1, 0.0), (1, 100.0), (1, 101.0), (1, -2.0),
                       (2, 0.0), (2, -5.0), (3, -1.0)]:
            args = list(base)
            args[i] = bad
            r = calcola_sconto_pronta_cassa(*args)
            assert r["valido"] is False and r["errore"], (i, bad)
        # non numerico e NaN: errore, nessuna eccezione
        assert calcola_sconto_pronta_cassa(
            "x", 2.0, 30, 5.0)["valido"] is False
        assert calcola_sconto_pronta_cassa(
            float("nan"), 2.0, 30, 5.0)["valido"] is False
        assert calcola_sconto_pronta_cassa(
            100000, 2.0, 30, float("nan"))["valido"] is False

    def test_determinismo(self):
        a = calcola_sconto_pronta_cassa(100000, 2.0, 30, 5.0)
        b = calcola_sconto_pronta_cassa(100000, 2.0, 30, 5.0)
        assert a["tasso_implicito_pct"] == b["tasso_implicito_pct"]
        assert a["costo_sconto_eur"] == b["costo_sconto_eur"]
        assert a["costo_wacc_eur"] == b["costo_wacc_eur"]
        assert a["risparmio_vs_wacc_eur"] == b["risparmio_vs_wacc_eur"]
        assert a["conviene"] == b["conviene"]
        assert a["df_sensibilita"].equals(b["df_sensibilita"])

    def test_chiavi_risultato(self):
        r = calcola_sconto_pronta_cassa(100000, 2.0, 30, 5.0)
        for k in ("errore", "tasso_implicito_pct", "costo_sconto_eur",
                  "costo_wacc_eur", "conviene", "df_sensibilita"):
            assert k in r
