"""Test tab202 'Concentrazione controparte': helper
calcola_concentrazione_controparte — quote volume, MtM, esposizione, HHI.

Stile pytest (vedi docs/AGGIUNGERE_TAB.md): la funzione viene estratta da
app.py via AST senza avviare Streamlit.
"""

import datetime

import numpy as np
import pandas as pd

from appfuncs import load

_F = load("calcola_concentrazione_controparte")
calcola_concentrazione_controparte = _F["calcola_concentrazione_controparte"]

OGGI = datetime.date.today()


def _df_base():
    return pd.DataFrame({
        "Fornitore": ["A", "A", "B", "C"],
        "Inizio": [OGGI - datetime.timedelta(days=400)] * 4,
        "Fine": [OGGI + datetime.timedelta(days=365)] * 4,
        "Volume_MWh_anno": [6000.0, 4000.0, 8000.0, 2000.0],
        "Prezzo_EUR_MWh": [80.0, 80.0, 0.0, 100.0],
        "Tipo": ["Fisso", "Fisso", "Indicizzato", "Fisso"]})


class TestValoriAttesi:
    def test_numeri_calcolabili_a_mano(self):
        # Volumi: A=10000 (50%), B=8000 (40%), C=2000 (10%) -> HHI = 4200.
        # Volume residuo = volume annuo (365 gg rimanenti).
        # MtM: A = 10000*(95-80) = 150000; B = 0 (indicizzato);
        #      C = 2000*(95-100) = -10000 -> esposizione solo su A.
        r = calcola_concentrazione_controparte(_df_base(), 95.0)
        assert r["errore"] is None
        assert r["valido"] is True
        assert r["n_controparti"] == 3
        assert r["n_contratti_attivi"] == 4
        assert abs(r["volume_totale"] - 20000.0) < 1e-9
        assert abs(r["hhi"] - 4200.0) < 1e-6
        assert r["classe_hhi"] == "Alta concentrazione"
        assert abs(r["cr1_pct"] - 50.0) < 1e-9
        assert abs(r["cr2_pct"] - 90.0) < 1e-9
        assert abs(r["esposizione_totale"] - 150000.0) < 1e-6
        assert abs(r["mtm_totale"] - 140000.0) < 1e-6
        g = r["df_controparti"]
        assert list(g["Fornitore"]) == ["A", "B", "C"]  # ordinato per quota
        assert list(g["Contratti"]) == [2, 1, 1]
        assert "Concentrazione ELEVATA" in r["verdetto"]

    def test_singola_controparte_hhi_10000(self):
        df = _df_base().iloc[:1].copy()
        r = calcola_concentrazione_controparte(df, 95.0)
        assert r["errore"] is None
        assert abs(r["hhi"] - 10000.0) < 1e-6
        assert abs(r["cr1_pct"] - 100.0) < 1e-9
        assert "CRITICA" in r["verdetto"]

    def test_portafoglio_diversificato(self):
        df = _df_base().copy()
        df["Fornitore"] = ["A", "B", "C", "D"]
        df["Volume_MWh_anno"] = [5000.0] * 4
        r = calcola_concentrazione_controparte(df, 95.0)
        assert r["errore"] is None
        assert abs(r["hhi"] - 2500.0) < 1e-6  # 4 x 25%^2
        assert "diversificato" in r["verdetto"]

    def test_volume_residuo_pro_rata(self):
        # Contratto che scade tra 182 giorni: volume residuo ~= meta'.
        df = _df_base().iloc[:1].copy()
        df["Fine"] = OGGI + datetime.timedelta(days=182)
        r = calcola_concentrazione_controparte(df, 95.0)
        assert r["errore"] is None
        vol_res = r["df_controparti"].loc[0, "Volume residuo (MWh)"]
        assert abs(vol_res - 6000.0 * 182 / 365) < 1e-6
        mtm = r["df_controparti"].loc[0, "MtM (€)"]
        assert abs(mtm - vol_res * (95.0 - 80.0)) < 1e-6


class TestRobustezza:
    def test_df_vuota(self):
        r = calcola_concentrazione_controparte(pd.DataFrame(), 95.0)
        assert r["errore"] is not None and r["valido"] is False

    def test_colonne_mancanti(self):
        r = calcola_concentrazione_controparte(
            _df_base().drop(columns=["Tipo"]), 95.0)
        assert r["errore"] is not None and "Colonne mancanti" in r["errore"]

    def test_tutti_scaduti(self):
        df = _df_base().copy()
        df["Fine"] = OGGI - datetime.timedelta(days=1)
        r = calcola_concentrazione_controparte(df, 95.0)
        assert r["errore"] is not None and "attivo" in r["errore"]

    def test_prezzo_mercato_non_valido(self):
        for pm in (0, -5.0, float("nan"), "95"):
            r = calcola_concentrazione_controparte(_df_base(), pm)
            assert r["errore"] is not None, pm

    def test_volume_non_positivo(self):
        df = _df_base().copy()
        df.loc[0, "Volume_MWh_anno"] = 0.0
        r = calcola_concentrazione_controparte(df, 95.0)
        assert r["errore"] is not None

    def test_tipo_non_valido(self):
        df = _df_base().copy()
        df.loc[0, "Tipo"] = "Variabile"
        r = calcola_concentrazione_controparte(df, 95.0)
        assert r["errore"] is not None

    def test_determinismo(self):
        df = _df_base()
        r1 = calcola_concentrazione_controparte(df, 95.0)
        r2 = calcola_concentrazione_controparte(df, 95.0)
        assert r1["hhi"] == r2["hhi"]
        assert r1["verdetto"] == r2["verdetto"]
        pd.testing.assert_frame_equal(r1["df_controparti"],
                                      r2["df_controparti"])

    def test_indice_tz_aware(self):
        df = _df_base().copy()
        df["Fine"] = pd.to_datetime(df["Fine"]).dt.tz_localize("Europe/Zurich")
        r = calcola_concentrazione_controparte(df, 95.0)
        assert r["errore"] is None and r["valido"] is True


# ------------------------------------------------------- registry
class TestRegistryTab202:
    def test_tab202_dichiarata(self):
        import re
        from pathlib import Path
        src = Path(__file__).parent.parent.joinpath("app.py").read_text()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 324
        assert titoli[-1] == "Ω📊 Omega ratio: oltre Sharpe e Sortino"
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab202" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab202" in withs
        assert len(withs) == len(dvars) == 324
        keys = re.findall(r'key="(cc202_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 3
