"""Test tab221 (stile pytest): Oneri di dispacciamento.

Le funzioni sono pure (niente Streamlit nel corpo): estratte da app.py via
AST con tests/appfuncs.py.
"""

import re
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from appfuncs import load

_F = load("calcola_oneri_dispacciamento", "profilo_mensile_demo")
calcola_oneri_dispacciamento = _F["calcola_oneri_dispacciamento"]
profilo_mensile_demo = _F["profilo_mensile_demo"]


class TestOneriBase:
    def test_numeri_a_mano(self):
        # 1000 MWh x 3.50 = 3500; 2 POD x 21 = 42; 200 kW x 21 = 4200
        # totale 7742 -> 7.742 €/MWh -> RILEVANTI
        r = calcola_oneri_dispacciamento(1000.0, 3.5, 21.0, 21.0, 200.0,
                                         n_pod=2)
        assert r["errore"] is None and r["valido"]
        assert r["costo_uplift"] == pytest.approx(3500.0)
        assert r["costo_quota_fissa"] == pytest.approx(42.0)
        assert r["costo_quota_potenza"] == pytest.approx(4200.0)
        assert r["costo_totale_annuo"] == pytest.approx(7742.0)
        assert r["equivalente_eur_mwh"] == pytest.approx(7.742)
        assert "RILEVANTI" in r["verdetto"]
        assert r["quote_pct"]["uplift"] == pytest.approx(3500 / 7742 * 100)
        assert r["quote_pct"]["quota_fissa"] == pytest.approx(42 / 7742 * 100)
        assert r["quote_pct"]["quota_potenza"] == pytest.approx(4200 / 7742 * 100)
        assert sum(r["quote_pct"].values()) == pytest.approx(100.0)

    def test_solo_uplift_moderato(self):
        r = calcola_oneri_dispacciamento(500.0, 4.0, 0.0, 0.0, 0.0)
        assert r["valido"]
        assert r["costo_totale_annuo"] == pytest.approx(2000.0)
        assert r["equivalente_eur_mwh"] == pytest.approx(4.0)
        assert "MODERATI" in r["verdetto"]
        assert r["quote_pct"]["uplift"] == pytest.approx(100.0)

    def test_verdetto_trascurabile(self):
        r = calcola_oneri_dispacciamento(10000.0, 2.0, 0.0, 0.0, 0.0)
        assert r["valido"] and "TRASCURABILI" in r["verdetto"]

    def test_verdetto_significativo(self):
        # 100 MWh, 100 kW x 21 € = 2100 € -> 21 €/MWh
        r = calcola_oneri_dispacciamento(100.0, 0.0, 0.0, 21.0, 100.0)
        assert r["valido"] and "SIGNIFICATIVI" in r["verdetto"]
        assert r["equivalente_eur_mwh"] == pytest.approx(21.0)

    def test_mensile_coerente(self):
        r = calcola_oneri_dispacciamento(1200.0, 3.0, 24.0, 12.0, 100.0,
                                         n_pod=1)
        df = r["df_mensile"]
        assert list(df.columns) == ["Mese", "Energia (MWh)", "Uplift (€)",
                                    "Quota fissa (€)", "Quota potenza (€)",
                                    "Totale (€)"]
        assert len(df) == 12
        assert df["Energia (MWh)"].sum() == pytest.approx(1200.0, abs=0.1)
        assert df["Uplift (€)"].sum() == pytest.approx(3600.0, abs=0.1)
        assert np.allclose(df["Quota fissa (€)"].to_numpy(), 2.0)
        assert np.allclose(df["Quota potenza (€)"].to_numpy(), 100.0)

    def test_profilo_estivo(self):
        r = calcola_oneri_dispacciamento(1200.0, 3.0, 0.0, 0.0, 0.0,
                                         quote_mensili=profilo_mensile_demo("estivo"))
        lug = r["df_mensile"].loc[6, "Energia (MWh)"]
        gen = r["df_mensile"].loc[0, "Energia (MWh)"]
        assert lug > gen
        assert r["df_mensile"]["Energia (MWh)"].sum() == pytest.approx(1200.0, abs=0.1)

    def test_quote_non_normalizzate(self):
        # 12 quote da 2 -> normalizzate = piatto
        r = calcola_oneri_dispacciamento(1200.0, 3.0, 0.0, 0.0, 0.0,
                                         quote_mensili=[2.0] * 12)
        assert np.allclose(r["df_mensile"]["Energia (MWh)"].to_numpy(),
                           100.0, atol=0.05)

    def test_sensitivita_default(self):
        r = calcola_oneri_dispacciamento(1000.0, 4.0, 0.0, 0.0, 0.0)
        df = r["df_sensitivita"]
        assert len(df) == 5
        assert df.iloc[2]["Scenario"] == "Uplift base"
        assert df.iloc[2]["Totale annuo (€)"] == pytest.approx(4000.0)
        assert df.iloc[0]["Totale annuo (€)"] == pytest.approx(2000.0)
        assert df.iloc[4]["Totale annuo (€)"] == pytest.approx(6000.0)

    def test_sensitivita_custom(self):
        r = calcola_oneri_dispacciamento(1000.0, 4.0, 21.0, 0.0, 0.0,
                                         uplift_scenari=[1.0, 5.0])
        df = r["df_sensitivita"]
        assert len(df) == 2
        assert df.iloc[0]["Totale annuo (€)"] == pytest.approx(1021.0)
        assert df.iloc[1]["Totale annuo (€)"] == pytest.approx(5021.0)

    def test_profilo_demo(self):
        for tipo in ["piatto", "estivo", "invernale", "doppia_punta", "sconosciuto"]:
            q = profilo_mensile_demo(tipo)
            assert len(q) == 12
            assert sum(q) == pytest.approx(1.0)
            assert all(v > 0 for v in q)
        assert profilo_mensile_demo("sconosciuto") == profilo_mensile_demo("piatto")

    def test_determinismo(self):
        kw = dict(uplift_scenari=[2.0, 4.0])
        a = calcola_oneri_dispacciamento(800.0, 3.0, 10.0, 10.0, 50.0, **kw)
        b = calcola_oneri_dispacciamento(800.0, 3.0, 10.0, 10.0, 50.0, **kw)
        assert a["costo_totale_annuo"] == b["costo_totale_annuo"]
        assert a["df_mensile"].equals(b["df_mensile"])
        assert a["df_sensitivita"].equals(b["df_sensitivita"])


class TestOneriErrori:
    def test_energia_non_valida(self):
        for bad in [0, -10.0, "x", True, None, float("nan"), float("inf")]:
            assert calcola_oneri_dispacciamento(bad, 3.5, 21.0, 21.0, 200.0)["errore"], bad

    def test_uplift_negativo(self):
        assert calcola_oneri_dispacciamento(1000.0, -0.5, 21.0, 21.0, 200.0)["errore"]

    def test_quote_negative(self):
        assert calcola_oneri_dispacciamento(1000.0, 3.5, -1.0, 0.0, 0.0)["errore"]
        assert calcola_oneri_dispacciamento(1000.0, 3.5, 21.0, -1.0, 200.0)["errore"]
        assert calcola_oneri_dispacciamento(1000.0, 3.5, 21.0, 21.0, -5.0)["errore"]

    def test_npod_non_valido(self):
        for bad in [0, -1, 1.5, "2", True, None]:
            assert calcola_oneri_dispacciamento(1000.0, 3.5, 21.0, 21.0, 200.0,
                                                n_pod=bad)["errore"], bad

    def test_quote_mensili_non_valide(self):
        assert calcola_oneri_dispacciamento(1000.0, 3.5, 0.0, 0.0, 0.0,
                                            quote_mensili=[1.0] * 11)["errore"]
        assert calcola_oneri_dispacciamento(1000.0, 3.5, 0.0, 0.0, 0.0,
                                            quote_mensili=[-1.0] + [1.0] * 11)["errore"]
        assert calcola_oneri_dispacciamento(1000.0, 3.5, 0.0, 0.0, 0.0,
                                            quote_mensili=[0.0] * 12)["errore"]

    def test_scenari_non_validi(self):
        assert calcola_oneri_dispacciamento(1000.0, 3.5, 0.0, 0.0, 0.0,
                                            uplift_scenari=[])["errore"]
        assert calcola_oneri_dispacciamento(1000.0, 3.5, 0.0, 0.0, 0.0,
                                            uplift_scenari=[-1.0])["errore"]


# ------------------------------------------------------- registry
class TestRegistryTab221:
    def test_tab221_dichiarata(self):
        src = Path(__file__).parent.parent.joinpath("app.py").read_text()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 316
        assert titoli[-1] == "🌊📉 POT-GPD: il VaR dalla coda paretiana oltre soglia"
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab221" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab221" in withs
        assert len(withs) == len(dvars) == 316
        keys = re.findall(r'key="(od221_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 4
