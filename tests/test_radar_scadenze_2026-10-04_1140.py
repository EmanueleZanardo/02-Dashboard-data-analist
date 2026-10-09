"""Test tab201 (stile pytest): Radar scadenze contratti di fornitura.

Le funzioni sono pure (niente Streamlit nel corpo): estratte da app.py via
AST con tests/appfuncs.py.
"""

import re
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from appfuncs import load

_F = load("calcola_radar_scadenze")
calcola_radar_scadenze = _F["calcola_radar_scadenze"]

RIF = "2026-10-04"
COLS = ["Fornitore", "Inizio", "Fine", "Volume_MWh_anno",
        "Prezzo_EUR_MWh", "Tipo"]


def _df(righe):
    return pd.DataFrame(righe, columns=COLS)


def _base():
    return _df([
        ["A", "2025-06-01", "2026-12-03", 10000.0, 80.0, "Fisso"],
        ["B", "2026-01-01", "2027-11-08", 5000.0, 120.0, "Fisso"],
        ["C", "2026-01-01", "2026-11-03", 8000.0, 0.0, "Indicizzato"],
    ])


class TestRadarScadenzeBase:
    def test_numeri_a_mano(self):
        r = calcola_radar_scadenze(_base(), 100.0, data_rif=RIF,
                                   orizzonte_mesi=6)
        assert r["errore"] is None and r["valido"]
        assert r["n_contratti"] == 3
        assert r["n_scaduti"] == 0
        assert r["n_critici"] == 2  # A (60gg) e C (30gg)
        assert r["volume_totale"] == pytest.approx(23000.0)
        assert r["volume_esposto"] == pytest.approx(18000.0)  # A + C
        assert r["quota_esposta_pct"] == pytest.approx(18000 / 230 * 1.0,
                                                      rel=1e-6)
        # repricing: solo A (fisso, esposto): 10000 * (100-80) = 200000
        assert r["repricing_totale"] == pytest.approx(200000.0)
        assert r["verdetto"].startswith("🔴 RIPREZZAMENTO IN VISTA")
        det = r["df_dettaglio"]
        ra = det[det["Fornitore"] == "A"].iloc[0]
        assert ra["Giorni rimanenti"] == 60
        assert ra["Classe"] == "🔴 Critico"
        assert ra["Repricing stimato (€/anno)"] == pytest.approx(200000.0)
        rb = det[det["Fornitore"] == "B"].iloc[0]
        assert rb["Classe"] == "🟢 Tranquillo"
        assert rb["Repricing stimato (€/anno)"] == pytest.approx(0.0)
        rc = det[det["Fornitore"] == "C"].iloc[0]
        assert rc["Repricing stimato (€/anno)"] == pytest.approx(0.0)

    def test_concentrazione_trimestri(self):
        r = calcola_radar_scadenze(_base(), 100.0, data_rif=RIF,
                                   orizzonte_mesi=6)
        assert r["trimestre_picco"] == "2026Q4"
        assert r["quota_picco_pct"] == pytest.approx(18000 / 230, rel=1e-6)
        tr = r["df_trimestri"]
        assert list(tr["Trimestre"]) == ["2026Q4", "2027Q4"]
        assert tr["Quota volume (%)"].sum() == pytest.approx(100.0)

    def test_classi_ai_bordi(self):
        righe = []
        for i, gg in enumerate([-5, 0, 90, 91, 180, 181, 365, 366]):
            fine = (pd.Timestamp(RIF) + pd.Timedelta(days=gg)).strftime(
                "%Y-%m-%d")
            righe.append(["F%d" % i, "2025-01-01", fine, 1000.0, 90.0,
                          "Fisso"])
        r = calcola_radar_scadenze(_df(righe), 90.0, data_rif=RIF,
                                   orizzonte_mesi=24)
        det = r["df_dettaglio"].set_index("Fornitore")
        attese = {0: "⛔ Scaduto", 1: "🔴 Critico", 2: "🔴 Critico",
                  3: "🟡 Attenzione", 4: "🟡 Attenzione",
                  5: "🔵 Monitoraggio", 6: "🔵 Monitoraggio",
                  7: "🟢 Tranquillo"}
        for i, cl in attese.items():
            assert det.loc["F%d" % i, "Classe"] == cl, i

    def test_verdetto_scaduti(self):
        df = _df([["X", "2025-01-01", "2026-09-20", 2000.0, 80.0, "Fisso"]])
        r = calcola_radar_scadenze(df, 100.0, data_rif=RIF, orizzonte_mesi=6)
        assert r["n_scaduti"] == 1
        assert r["verdetto"].startswith("⛔ CONTRATTI SCADUTI")
        # scaduto => esposto, repricing calcolato
        assert r["volume_esposto"] == pytest.approx(2000.0)
        assert r["repricing_totale"] == pytest.approx(40000.0)

    def test_verdetto_scadenze_ravvicinate(self):
        df = _df([["Y", "2025-01-01", "2026-11-03", 2000.0, 0.0,
                   "Indicizzato"]])
        r = calcola_radar_scadenze(df, 100.0, data_rif=RIF, orizzonte_mesi=6)
        assert r["repricing_totale"] == pytest.approx(0.0)
        assert r["n_critici"] == 1
        assert r["verdetto"].startswith("🟡 SCADENZE RAVVICINATE")

    def test_verdetto_concentrazione(self):
        df = _df([["Z", "2025-01-01", "2027-11-08", 2000.0, 100.0, "Fisso"]])
        r = calcola_radar_scadenze(df, 100.0, data_rif=RIF, orizzonte_mesi=6)
        assert r["repricing_totale"] == pytest.approx(0.0)
        assert r["n_critici"] == 0
        assert r["quota_picco_pct"] == pytest.approx(100.0)
        assert r["verdetto"].startswith("🟡 CONCENTRAZIONE SCADENZE")

    def test_verdetto_sotto_controllo(self):
        df = _df([
            ["P", "2025-01-01", "2027-11-08", 4000.0, 100.0, "Fisso"],
            ["Q", "2025-01-01", "2028-02-08", 3500.0, 100.0, "Fisso"],
            ["R", "2025-01-01", "2028-05-08", 2500.0, 100.0, "Fisso"],
        ])
        r = calcola_radar_scadenze(df, 100.0, data_rif=RIF, orizzonte_mesi=6)
        assert r["quota_picco_pct"] < 50.0
        assert r["verdetto"].startswith("🟢 SOTTO CONTROLLO")

    def test_risparmio_da_repricing(self):
        df = _df([["S", "2025-01-01", "2026-12-03", 1000.0, 80.0, "Fisso"]])
        r = calcola_radar_scadenze(df, 60.0, data_rif=RIF, orizzonte_mesi=6)
        assert r["repricing_totale"] == pytest.approx(-20000.0)

    def test_tipo_case_insensitive(self):
        df = _df([
            ["T1", "2025-01-01", "2027-01-01", 1000.0, 80.0, "fisso"],
            ["T2", "2025-01-01", "2027-01-01", 1000.0, 0.0, " INDICIZZATO "],
        ])
        r = calcola_radar_scadenze(df, 100.0, data_rif=RIF)
        assert r["errore"] is None
        det = r["df_dettaglio"].set_index("Fornitore")
        assert det.loc["T1", "Tipo"] == "Fisso"
        assert det.loc["T2", "Tipo"] == "Indicizzato"

    def test_tz_aware(self):
        df = _df([["W", "2025-06-01", "2026-12-03", 1000.0, 80.0, "Fisso"]])
        df["Inizio"] = pd.to_datetime(df["Inizio"]).dt.tz_localize(
            "Europe/Zurich")
        df["Fine"] = pd.to_datetime(df["Fine"]).dt.tz_localize(
            "Europe/Zurich")
        r = calcola_radar_scadenze(df, 100.0, data_rif=RIF)
        assert r["errore"] is None
        assert r["df_dettaglio"].iloc[0]["Giorni rimanenti"] == 60

    def test_determinismo(self):
        r1 = calcola_radar_scadenze(_base(), 100.0, data_rif=RIF)
        r2 = calcola_radar_scadenze(_base(), 100.0, data_rif=RIF)
        assert r1["repricing_totale"] == r2["repricing_totale"]
        assert r1["verdetto"] == r2["verdetto"]
        assert r1["df_dettaglio"].equals(r2["df_dettaglio"])

    def test_data_rif_default_oggi(self):
        r = calcola_radar_scadenze(_base(), 100.0)
        assert r["errore"] is None
        assert r["data_rif"].date() == pd.Timestamp.today().date()


class TestRadarScadenzeErrori:
    def test_input_non_validi(self):
        assert calcola_radar_scadenze(None, 100.0)["errore"]
        assert calcola_radar_scadenze("x", 100.0)["errore"]
        assert calcola_radar_scadenze(
            pd.DataFrame(columns=COLS), 100.0)["errore"]

    def test_colonne_mancanti(self):
        df = _base().drop(columns=["Tipo"])
        r = calcola_radar_scadenze(df, 100.0, data_rif=RIF)
        assert r["errore"] and "Tipo" in r["errore"]

    def test_date_non_valide(self):
        df = _base()
        df.loc[0, "Fine"] = "non una data"
        assert calcola_radar_scadenze(df, 100.0, data_rif=RIF)["errore"]

    def test_fine_prima_di_inizio(self):
        df = _df([["E", "2026-06-01", "2026-01-01", 1000.0, 80.0, "Fisso"]])
        assert calcola_radar_scadenze(df, 100.0, data_rif=RIF)["errore"]

    def test_volume_non_valido(self):
        for v in [0.0, -5.0, np.nan, "x"]:
            df = _df([["E", "2025-01-01", "2027-01-01", v, 80.0, "Fisso"]])
            assert calcola_radar_scadenze(df, 100.0,
                                          data_rif=RIF)["errore"], v

    def test_tipo_non_valido(self):
        df = _df([["E", "2025-01-01", "2027-01-01", 1000.0, 80.0, "Spot"]])
        assert calcola_radar_scadenze(df, 100.0, data_rif=RIF)["errore"]

    def test_prezzo_fisso_non_valido(self):
        for p in [0.0, -10.0, np.nan]:
            df = _df([["E", "2025-01-01", "2027-01-01", 1000.0, p, "Fisso"]])
            assert calcola_radar_scadenze(df, 100.0,
                                          data_rif=RIF)["errore"], p

    def test_prezzo_mercato_non_valido(self):
        for pm in [0.0, -1.0, np.nan, np.inf, "x", True]:
            assert calcola_radar_scadenze(_base(), pm,
                                          data_rif=RIF)["errore"], pm

    def test_orizzonte_non_valido(self):
        for o in [0, 25, "sei", True, None, 6.5]:
            assert calcola_radar_scadenze(_base(), 100.0, data_rif=RIF,
                                          orizzonte_mesi=o)["errore"], o

    def test_data_rif_non_valida(self):
        assert calcola_radar_scadenze(_base(), 100.0,
                                      data_rif="non una data")["errore"]

    def test_fornitore_vuoto(self):
        df = _df([["", "2025-01-01", "2027-01-01", 1000.0, 80.0, "Fisso"]])
        assert calcola_radar_scadenze(df, 100.0, data_rif=RIF)["errore"]


# ------------------------------------------------------- registry
class TestRegistryTab201:
    def test_tab201_dichiarata(self):
        src = Path(__file__).parent.parent.joinpath("app.py").read_text()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 342
        assert titoli[-1] == "🎯 Volatilità target: il sizing a volatilità costante"
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab201" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab201" in withs
        assert len(withs) == len(dvars) == 342
        keys = re.findall(r'key="(rs201_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 4
