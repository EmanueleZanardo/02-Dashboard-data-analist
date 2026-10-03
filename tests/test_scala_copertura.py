"""Test calcola_scala_copertura - tab170 (stile pytest, via appfuncs).

Copertura: numeri a mano su scenari controllati (quota 50% su 30gg piatti;
tabella mensile su 2 mesi con tranche solo a gennaio; over-hedge; nessuna
tranche; righe scartate), casi di errore, robustezza dati (NaN/tz/duplicati),
determinismo, replicazione indipendente del pipeline, registry tab170.
"""
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load  # noqa: E402

fns = load("calcola_scala_copertura", "fascia_oraria")
sc = fns["calcola_scala_copertura"]
fascia_oraria = fns["fascia_oraria"]


def serie_ore(valore=100.0, start="2025-01-01", n_ore=720):
    idx = pd.date_range(start, periods=n_ore, freq="h")
    return pd.Series(float(valore), index=idx)


def tranche(nome, mw, inizio, fine, prezzo):
    return {"Tranche": nome, "MW": mw, "Inizio": inizio,
            "Fine": fine, "Prezzo (€/MWh)": prezzo}


def quota_manuale(prezzi, mw_f1, mw_f2, mw_f3, righe, target=80.0):
    """Replica indipendente del pipeline: carico da fasce + overlap giornaliero."""
    idx = prezzi.index.tz_localize(None) if prezzi.index.tz is not None else prezzi.index
    idx = idx[~idx.duplicated(keep="first")]
    ore = idx.map(fascia_oraria).map({"F1": mw_f1, "F2": mw_f2, "F3": mw_f3}).astype(float).to_numpy()
    giorni = idx.normalize()
    hedge = np.zeros(len(idx))
    for r in righe:
        g1 = pd.to_datetime(r["Inizio"]).normalize()
        g2 = pd.to_datetime(r["Fine"]).normalize()
        m = np.asarray((giorni >= g1) & (giorni <= g2))
        hedge[m] += float(r["MW"])
    mese = idx.to_period("M")
    out = {}
    for per in mese.unique():
        mm = np.asarray(mese == per)
        car, cop = float(ore[mm].sum()), float(hedge[mm].sum())
        out[str(per)] = (car, cop, cop / car * 100.0 if car else 0.0)
    return out


class TestNumeriAMano:
    def test_quota_50_su_30gg_piatti(self):
        p = serie_ore(100.0, n_ore=30 * 24)
        t = [tranche("T", 1.0, "2025-01-01", "2025-01-30", 90.0)]
        r = sc(p, 2.0, 2.0, 2.0, t, 80.0)
        assert r["valido"] and r["errore"] is None
        # carico = 30*24*2 = 1440 MWh; coperto = 30*24*1 = 720 MWh
        assert r["mwh_carico_tot"] == pytest.approx(1440.0)
        assert r["mwh_coperti_tot"] == pytest.approx(720.0)
        assert r["quota_media_pct"] == pytest.approx(50.0)
        assert r["prezzo_medio_coperture"] == pytest.approx(90.0)
        assert r["mwh_scoperti"] == pytest.approx(720.0)
        assert r["n_mesi_sotto_target"] == 1
        assert r["mesi_sotto_target"] == ["2025-01"]
        assert r["giudizio"] == "ATTENZIONE"
        assert r["n_tranche_valide"] == 1 and r["n_tranche_scartate"] == 0
        assert len(r["tabella_mensile"]) == 1
        assert r["tabella_mensile"].iloc[0]["Stato"] == "SOTTO TARGET"

    def test_tabella_mensile_due_mesi_tranche_solo_gennaio(self):
        # gen 31gg + feb 28gg = 1416 ore; MW 1/1/1 -> 1416 MWh
        p = serie_ore(100.0, start="2025-01-01", n_ore=(31 + 28) * 24)
        t = [tranche("Gen", 1.0, "2025-01-01", "2025-01-31", 95.0)]
        r = sc(p, 1.0, 1.0, 1.0, t, 80.0)
        assert r["valido"]
        tm = r["tabella_mensile"]
        assert list(tm["Mese"]) == ["2025-01", "2025-02"]
        assert tm.iloc[0]["Carico (MWh)"] == pytest.approx(31 * 24.0)
        assert tm.iloc[0]["Coperto (MWh)"] == pytest.approx(31 * 24.0)
        assert tm.iloc[0]["Quota (%)"] == pytest.approx(100.0)
        assert tm.iloc[0]["Prezzo medio coperture (€/MWh)"] == pytest.approx(95.0)
        assert tm.iloc[0]["Stato"] == "OK"
        assert tm.iloc[1]["Quota (%)"] == pytest.approx(0.0)
        assert tm.iloc[1]["Stato"] == "SOTTO TARGET"
        assert pd.isna(tm.iloc[1]["Prezzo medio coperture (€/MWh)"])
        assert r["n_mesi_sotto_target"] == 1
        assert r["mesi_sotto_target"] == ["2025-02"]

    def test_prezzo_medio_ponderato_due_tranche(self):
        p = serie_ore(100.0, n_ore=30 * 24)
        t = [tranche("A", 1.0, "2025-01-01", "2025-01-30", 80.0),
             tranche("B", 1.0, "2025-01-01", "2025-01-30", 100.0)]
        r = sc(p, 2.0, 2.0, 2.0, t, 80.0)
        assert r["valido"]
        assert r["quota_media_pct"] == pytest.approx(100.0)
        assert r["prezzo_medio_coperture"] == pytest.approx(90.0)
        assert r["mwh_scoperti"] == pytest.approx(0.0)
        assert r["giudizio"] == "COPERTURA OK"

    def test_over_hedge(self):
        p = serie_ore(100.0, n_ore=30 * 24)
        t = [tranche("Big", 5.0, "2025-01-01", "2025-01-30", 90.0)]
        r = sc(p, 2.0, 2.0, 2.0, t, 80.0)
        assert r["valido"]
        assert r["quota_media_pct"] == pytest.approx(250.0)
        assert r["mesi_over_hedge"] == ["2025-01"]
        assert r["n_mesi_sotto_target"] == 0
        assert r["tabella_mensile"].iloc[0]["Stato"] == "OVER-HEDGE"
        assert r["giudizio"] == "COPERTURA OK"
        assert "over-hedge" in r["verdetto"]

    def test_nessuna_tranche(self):
        p = serie_ore(100.0, n_ore=30 * 24)
        r = sc(p, 2.0, 2.0, 2.0, [], 80.0)
        assert r["valido"]
        assert r["quota_media_pct"] == pytest.approx(0.0)
        assert r["prezzo_medio_coperture"] is None
        assert r["giudizio"] == "NESSUNA COPERTURA"
        assert r["mwh_scoperti"] == pytest.approx(r["mwh_carico_tot"])

    def test_replica_indipendente(self):
        p = serie_ore(100.0, start="2025-01-15", n_ore=60 * 24)
        t = [tranche("A", 1.2, "2025-01-20", "2025-02-10", 88.5),
             tranche("B", 0.7, "2025-02-01", "2025-03-05", 92.0)]
        r = sc(p, 3.0, 2.0, 1.0, t, 70.0)
        man = quota_manuale(p, 3.0, 2.0, 1.0, t)
        assert r["valido"]
        for _, row in r["tabella_mensile"].iterrows():
            car, cop, q = man[row["Mese"]]
            assert row["Carico (MWh)"] == pytest.approx(car, abs=0.15)
            assert row["Coperto (MWh)"] == pytest.approx(cop, abs=0.15)
            assert row["Quota (%)"] == pytest.approx(q, abs=0.15)
        assert r["quota_media_pct"] == pytest.approx(
            sum(cop for _, cop, _ in man.values())
            / sum(car for car, _, _ in man.values()) * 100.0, abs=0.01)

    def test_tranche_dataframe_da_data_editor(self):
        p = serie_ore(100.0, n_ore=30 * 24)
        df = pd.DataFrame([tranche("T", 1.0, "2025-01-01", "2025-01-30", 90.0)])
        r = sc(p, 2.0, 2.0, 2.0, df, 80.0)
        assert r["valido"] and r["quota_media_pct"] == pytest.approx(50.0)
        assert r["tranche_valide"][0]["Inizio"] == "2025-01-01"


class TestTrancheScartate:
    def test_righe_non_valide_scartate_e_contate(self):
        p = serie_ore(100.0, n_ore=30 * 24)
        t = [tranche("ok", 1.0, "2025-01-01", "2025-01-30", 90.0),
             tranche("inizio>fine", 1.0, "2025-02-01", "2025-01-01", 90.0),
             tranche("mw0", 0.0, "2025-01-01", "2025-01-30", 90.0),
             tranche("mw-neg", -2.0, "2025-01-01", "2025-01-30", 90.0),
             tranche("data-ko", 1.0, "non-una-data", "2025-01-30", 90.0),
             tranche("prezzo-nan", 1.0, "2025-01-01", "2025-01-30", float("nan")),
             {"Tranche": "vuota", "MW": "", "Inizio": "", "Fine": "", "Prezzo (€/MWh)": ""},
             "non-un-dict"]
        r = sc(p, 2.0, 2.0, 2.0, t, 80.0)
        assert r["valido"]
        assert r["n_tranche_valide"] == 1
        assert r["n_tranche_scartate"] == 7
        assert r["quota_media_pct"] == pytest.approx(50.0)

    def test_formato_tranche_non_valido(self):
        p = serie_ore(100.0, n_ore=48)
        r = sc(p, 1.0, 1.0, 1.0, "stringa", 80.0)
        assert not r["valido"] and r["errore"]


class TestErrori:
    @pytest.mark.parametrize("prezzi", [
        pd.Series([], dtype=float),
        pd.Series([100.0, 110.0], index=["a", "b"]),
        pd.Series([], dtype=float, index=pd.DatetimeIndex([])),
    ])
    def test_input_non_validi(self, prezzi):
        assert not sc(prezzi, 1.0, 1.0, 1.0, [], 80.0)["valido"]

    def test_mw_tutti_zero(self):
        assert not sc(serie_ore(n_ore=48), 0.0, 0.0, 0.0, [], 80.0)["valido"]

    def test_mw_negativo(self):
        assert not sc(serie_ore(n_ore=48), -1.0, 1.0, 1.0, [], 80.0)["valido"]

    @pytest.mark.parametrize("target", [0.0, -5.0, 100.5, 150.0, float("nan"), "x"])
    def test_target_fuori_range(self, target):
        assert not sc(serie_ore(n_ore=48), 1.0, 1.0, 1.0, [], target)["valido"]

    def test_target_100_valido(self):
        r = sc(serie_ore(n_ore=48), 1.0, 1.0, 1.0, [], 100.0)
        assert r["valido"] and r["target_pct"] == 100.0


class TestRobustezza:
    def test_nan_scartati_e_contati(self):
        p = serie_ore(100.0, n_ore=72)
        p.iloc[5] = np.nan
        p.iloc[40] = np.nan
        r = sc(p, 1.0, 1.0, 1.0, [], 80.0)
        assert r["valido"] and r["n_nan_prezzi"] == 2
        assert r["mwh_carico_tot"] == pytest.approx(70.0)

    def test_tz_aware_reso_naive(self):
        idx = pd.date_range("2025-01-01", periods=48, freq="h", tz="Europe/Zurich")
        p = pd.Series(100.0, index=idx)
        r = sc(p, 1.0, 1.0, 1.0,
               [tranche("T", 1.0, "2025-01-01", "2025-01-02", 90.0)], 80.0)
        assert r["valido"] and r["quota_media_pct"] == pytest.approx(100.0)

    def test_duplicati_keep_first(self):
        p = serie_ore(100.0, n_ore=48)
        p2 = pd.concat([p, p.iloc[[10]]])
        r = sc(p2, 1.0, 1.0, 1.0, [], 80.0)
        assert r["valido"] and r["mwh_carico_tot"] == pytest.approx(48.0)

    def test_tranche_tz_aware(self):
        p = serie_ore(100.0, n_ore=48)
        t = [{"Tranche": "T", "MW": 1.0,
              "Inizio": pd.Timestamp("2025-01-01", tz="Europe/Zurich"),
              "Fine": pd.Timestamp("2025-01-02", tz="Europe/Zurich"),
              "Prezzo (€/MWh)": 90.0}]
        r = sc(p, 1.0, 1.0, 1.0, t, 80.0)
        assert r["valido"] and r["n_tranche_valide"] == 1

    def test_determinismo(self):
        p = serie_ore(100.0, n_ore=72)
        t = [tranche("T", 1.0, "2025-01-01", "2025-01-03", 90.0)]
        r1 = sc(p, 2.0, 1.5, 1.0, t, 75.0)
        r2 = sc(p, 2.0, 1.5, 1.0, t, 75.0)
        assert r1["verdetto"] == r2["verdetto"]
        assert r1["quota_media_pct"] == r2["quota_media_pct"]
        assert r1["tabella_mensile"].equals(r2["tabella_mensile"])
        assert r1["serie_quota"].equals(r2["serie_quota"])

    def test_serie_quota_coerente_con_tabella(self):
        p = serie_ore(100.0, start="2025-01-01", n_ore=(31 + 28) * 24)
        t = [tranche("T", 1.0, "2025-01-01", "2025-02-28", 90.0)]
        r = sc(p, 2.0, 2.0, 2.0, t, 80.0)
        assert r["valido"]
        assert len(r["serie_quota"]) == 2
        for (_, row), (_, q) in zip(r["tabella_mensile"].iterrows(),
                                    r["serie_quota"].items()):
            assert row["Quota (%)"] == pytest.approx(q, abs=0.05)


# -------------------------------------------------------------------- registry
class TestRegistry:
    def test_tab170_registrata(self):
        src = open("app.py", encoding="utf-8").read()
        m = re.search(r"tab1, tab2, .*? = st\.tabs\(\[", src, re.S)
        dvars = re.findall(r"tab\d+", m.group(0))
        # appartenenza + sequenza senza buchi (non conteggio esatto)
        assert "tab170" in dvars
        assert dvars == ["tab%d" % i for i in range(1, len(dvars) + 1)]
        withs = re.findall(r"^    with (tab\d+):", src, re.M)
        assert withs == ["tab%d" % i for i in range(1, len(withs) + 1)]
        assert "tab170" in withs
        assert len(withs) == len(dvars) >= 170
        assert '"🪜 Scala di copertura"' in src
        keys = re.findall(r'key="(sc170_[^"]+)"', src)
        assert len(keys) == len(set(keys)) and len(keys) >= 7
        assert re.search(r"^def calcola_scala_copertura\(", src, re.M) is not None
