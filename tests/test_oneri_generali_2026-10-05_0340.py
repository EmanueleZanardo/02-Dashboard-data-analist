"""Test tab222 (stile pytest): Oneri generali di sistema.

Le funzioni sono pure (niente Streamlit nel corpo): estratte da app.py via
AST con tests/appfuncs.py.
"""

import pytest

from appfuncs import load

_F = load("calcola_oneri_generali", "profilo_mensile_demo")
calcola_oneri_generali = _F["calcola_oneri_generali"]
profilo_mensile_demo = _F["profilo_mensile_demo"]


class TestOneriGeneraliBase:
    def test_numeri_a_mano(self):
        # 1000 MWh x 27 = 27000; 2 POD x 0 = 0; 200 kW x 21 = 4200
        # totale 31200 -> 31.2 €/MWh -> RILEVANTI; ASOS 85% = 26520
        r = calcola_oneri_generali(1000.0, 0.0, 21.0, 27.0, 200.0, n_pod=2)
        assert r["errore"] is None and r["valido"]
        assert r["costo_quota_energia"] == pytest.approx(27000.0)
        assert r["costo_quota_fissa"] == pytest.approx(0.0)
        assert r["costo_quota_potenza"] == pytest.approx(4200.0)
        assert r["costo_totale_annuo"] == pytest.approx(31200.0)
        assert r["quota_asos_eur"] == pytest.approx(26520.0)
        assert r["quota_arim_eur"] == pytest.approx(4680.0)
        assert r["equivalente_eur_mwh"] == pytest.approx(31.2)
        assert "RILEVANTI" in r["verdetto"]
        assert r["quote_pct"]["quota_energia"] == pytest.approx(27000 / 31200 * 100)
        assert sum(r["quote_pct"].values()) == pytest.approx(100.0)

    def test_moderati_e_trascurabili(self):
        r = calcola_oneri_generali(1000.0, 0.0, 0.0, 15.0, 0.0)
        assert "MODERATI" in r["verdetto"]
        r = calcola_oneri_generali(1000.0, 0.0, 0.0, 5.0, 0.0)
        assert "TRASCURABILI" in r["verdetto"]

    def test_quota_asos_personalizzata(self):
        r = calcola_oneri_generali(500.0, 0.0, 0.0, 20.0, 0.0,
                                   quota_asos_pct=50.0)
        assert r["quota_asos_eur"] == pytest.approx(5000.0)
        assert r["quota_arim_eur"] == pytest.approx(5000.0)

    def test_mensile_e_sensitivita(self):
        quote = profilo_mensile_demo("estivo")
        r = calcola_oneri_generali(1200.0, 10.0, 21.0, 27.0, 100.0,
                                   quote_mensili=quote)
        assert len(r["df_mensile"]) == 12
        assert r["df_mensile"]["Totale (€)"].sum() == pytest.approx(
            r["costo_totale_annuo"], rel=1e-3)
        assert r["df_mensile"]["Energia (MWh)"].sum() == pytest.approx(
            1200.0, rel=1e-3)
        assert len(r["df_sensitivita"]) == 5
        base = r["df_sensitivita"].set_index("Scenario").loc["base"]
        assert base["Totale annuo (€)"] == pytest.approx(
            r["costo_totale_annuo"], rel=1e-6)

    def test_input_non_validi(self):
        for args in [
            (0.0, 0.0, 21.0, 27.0, 100.0),          # energia zero
            (-5.0, 0.0, 21.0, 27.0, 100.0),         # energia negativa
            (1000.0, 0.0, 21.0, -1.0, 100.0),       # quota negativa
            (1000.0, 0.0, 21.0, 27.0, 100.0, 0),    # n_pod zero
            (1000.0, 0.0, 21.0, 27.0, 100.0, 1, 101.0),  # asos > 100
            ("x", 0.0, 21.0, 27.0, 100.0),          # non numerico
        ]:
            r = calcola_oneri_generali(*args)
            assert r["errore"] is not None and not r["valido"]

    def test_determinismo(self):
        kw = dict(n_pod=2, quota_asos_pct=80.0)
        a = calcola_oneri_generali(1000.0, 5.0, 21.0, 27.0, 200.0, **kw)
        b = calcola_oneri_generali(1000.0, 5.0, 21.0, 27.0, 200.0, **kw)
        assert a["costo_totale_annuo"] == b["costo_totale_annuo"]
        assert a["verdetto"] == b["verdetto"]
