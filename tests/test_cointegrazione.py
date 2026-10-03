"""Test pytest per tab172 - Cointegrazione (Engle-Granger) tra spot e gas TTF."""
import ast
import math

import numpy as np
import pandas as pd
import pytest

from appfuncs import load

_F = load("calcola_cointegrazione")
calcola_cointegrazione = _F["calcola_cointegrazione"]
_APP_SRC = open("/home/hatch/workspace/dashboard-qa/app.py").read()


def _giorni(n, start="2025-01-01"):
    return pd.date_range(start=start, periods=n, freq="D")


def _rw(n, seed, sigma=1.0):
    rng = np.random.default_rng(seed)
    return np.cumsum(rng.normal(0, sigma, n))


def _coppia_cointegrata(n=500, seed=7):
    """Gas = random walk; power = 2 + 2.5*gas + AR(1) stazionario."""
    rng = np.random.default_rng(seed)
    gas = 40 + _rw(n, seed + 1, sigma=0.4)
    ar = np.zeros(n)
    for t in range(1, n):
        ar[t] = 0.6 * ar[t - 1] + rng.normal(0, 1.0)
    power = 2.0 + 2.5 * gas + ar
    idx = _giorni(n)
    return (pd.Series(power, index=idx, name="power"),
            pd.Series(gas, index=idx, name="gas"))


class TestCointegrazione:
    def test_coppia_cointegrata(self):
        pw, gs = _coppia_cointegrata()
        r = calcola_cointegrazione(pw, gs)
        assert r["valido"] and r["errore"] is None
        assert r["cointegrata"] is True
        assert r["rifiuta_5"] is True
        assert abs(r["beta"] - 2.5) < 0.15
        assert r["r2"] is not None and r["r2"] > 0.95
        assert r["half_life_giorni"] is not None and r["half_life_giorni"] > 0
        assert r["n_giorni"] == 500
        assert "COINTEGRATE" in r["giudizio"]

    def test_half_life_coerente(self):
        pw, gs = _coppia_cointegrata()
        r = calcola_cointegrazione(pw, gs)
        # AR(1) con phi=0.6 -> half-life teorica -ln2/ln(0.6) = 1.357 gg
        assert abs(r["half_life_giorni"] - 1.357) < 0.6

    def test_random_walk_indipendenti_non_cointegrate(self):
        idx = _giorni(500)
        gs = pd.Series(40 + _rw(500, 21, sigma=0.4), index=idx)
        pw = pd.Series(60 + _rw(500, 22, sigma=1.5), index=idx)
        r = calcola_cointegrazione(pw, gs)
        assert r["valido"]
        assert r["cointegrata"] is False
        assert r["rifiuta_5"] is False
        assert "SPURIA" in r["giudizio"]

    def test_residui_costanti_cointegrata(self):
        idx = _giorni(120)
        gs = pd.Series(30.0 + np.arange(120), index=idx)
        pw = pd.Series(1.0 + 2.0 * (30.0 + np.arange(120)), index=idx)
        r = calcola_cointegrazione(pw, gs)
        assert r["valido"]
        assert abs(r["beta"] - 2.0) < 1e-9
        assert abs(r["alpha"] - 1.0) < 1e-9
        assert r["cointegrata"] is True
        assert r["stat"] == -np.inf

    def test_replicazione_ols_indipendente(self):
        pw, gs = _coppia_cointegrata(n=200, seed=99)
        r = calcola_cointegrazione(pw, gs)
        x = gs.to_numpy()
        y = pw.to_numpy()
        b_ref = float(np.cov(x, y, ddof=0)[0, 1] / np.var(x))
        a_ref = float(np.mean(y) - b_ref * np.mean(x))
        # l'helper arrotonda a 4 decimali
        assert r["beta"] == round(b_ref, 4)
        assert r["alpha"] == round(a_ref, 4)

    def test_z_score_segno(self):
        pw, gs = _coppia_cointegrata(n=200, seed=5)
        r = calcola_cointegrazione(pw, gs)
        assert r["z_score"] is not None
        assert (r["z_score"] > 0) == (r["spread_eur"] > 0)

    def test_tabella_mensile(self):
        idx = _giorni(400, start="2025-01-15")
        gs = pd.Series(40 + _rw(400, 31, sigma=0.4), index=idx)
        pw = pd.Series(2 + 2.5 * gs.to_numpy(), index=idx)
        r = calcola_cointegrazione(pw, gs)
        assert r["valido"]
        mesi_attesi = len(pd.period_range("2025-01", "2026-02", freq="M"))
        assert len(r["df_mesi"]) == mesi_attesi
        assert list(r["df_mesi"].columns) == ["Mese", "Giorni",
                                              "Residuo medio (€/MWh)",
                                              "Z-score medio"]

    def test_serie_output(self):
        pw, gs = _coppia_cointegrata(n=150, seed=8)
        r = calcola_cointegrazione(pw, gs)
        df = r["df_serie"]
        assert list(df.columns) == ["Giorno", "Gas (€/MWh)", "Power (€/MWh)",
                                    "Residuo (€/MWh)", "Z-score"]
        assert len(df) == 150
        assert df["Giorno"].iloc[0] == pd.Timestamp("2025-01-01").date()

    def test_lag_fisso(self):
        pw, gs = _coppia_cointegrata(n=200, seed=12)
        r = calcola_cointegrazione(pw, gs, lags=4)
        assert r["valido"] and r["lags"] == 4 and r["lags_auto"] is False
        assert r["cointegrata"] is True

    def test_regression_trend(self):
        pw, gs = _coppia_cointegrata(n=300, seed=13)
        r = calcola_cointegrazione(pw, gs, regression="ct")
        assert r["valido"] and r["cointegrata"] is True

    def test_nan_scartati_contati(self):
        pw, gs = _coppia_cointegrata(n=200, seed=14)
        pw2 = pw.copy()
        pw2.iloc[10] = np.nan
        pw2.iloc[50] = np.nan
        r = calcola_cointegrazione(pw2, gs)
        assert r["valido"]
        assert r["n_scartate"] == 2
        assert r["n_giorni"] == 198

    def test_tz_aware(self):
        pw, gs = _coppia_cointegrata(n=120, seed=15)
        pw.index = pw.index.tz_localize("Europe/Zurich")
        r = calcola_cointegrazione(pw, gs)
        assert r["valido"] and r["n_giorni"] == 120

    def test_duplicati_keep_first(self):
        pw, gs = _coppia_cointegrata(n=120, seed=16)
        pw2 = pd.concat([pw, pw.iloc[[0]] * 999.0])
        r = calcola_cointegrazione(pw2, gs)
        assert r["valido"] and r["n_giorni"] == 120

    def test_determinismo(self):
        pw, gs = _coppia_cointegrata(n=200, seed=17)
        r1 = calcola_cointegrazione(pw, gs)
        r2 = calcola_cointegrazione(pw, gs)
        assert r1["stat"] == r2["stat"]
        assert r1["beta"] == r2["beta"]
        assert r1["giudizio"] == r2["giudizio"]

    def test_serie_vuota(self):
        r = calcola_cointegrazione(pd.Series(dtype=float), pd.Series(dtype=float))
        assert not r["valido"] and r["errore"]

    def test_indice_non_datetime(self):
        r = calcola_cointegrazione(pd.Series([1.0, 2.0]), pd.Series([1.0, 2.0]))
        assert not r["valido"] and r["errore"]

    def test_troppo_corta(self):
        idx = _giorni(40)
        r = calcola_cointegrazione(pd.Series(np.ones(40), index=idx),
                                   pd.Series(np.ones(40) * 2, index=idx))
        assert not r["valido"] and "40" in r["errore"]

    def test_gas_costante(self):
        idx = _giorni(120)
        r = calcola_cointegrazione(pd.Series(_rw(120, 41), index=idx),
                                   pd.Series(np.full(120, 38.0), index=idx))
        assert not r["valido"] and "costante" in r["errore"]

    def test_regression_invalida(self):
        pw, gs = _coppia_cointegrata(n=120, seed=18)
        r = calcola_cointegrazione(pw, gs, regression="xx")
        assert not r["valido"] and r["errore"]

    def test_lags_invalido(self):
        pw, gs = _coppia_cointegrata(n=120, seed=19)
        assert not calcola_cointegrazione(pw, gs, lags=-1)["valido"]
        assert not calcola_cointegrazione(pw, gs, lags="x")["valido"]

    def test_allineamento_intersezione(self):
        idx1 = _giorni(200, start="2025-01-01")
        idx2 = _giorni(200, start="2025-02-01")
        pw = pd.Series(_rw(200, 51), index=idx1)
        gs = pd.Series(_rw(200, 52), index=idx2)
        r = calcola_cointegrazione(pw, gs)
        assert r["valido"]
        assert r["n_giorni"] == 200 - 31  # sovrapposizione feb->lug

    def test_registry_tab172(self):
        tree = ast.parse(_APP_SRC)
        # tab172 dichiarata nella chiamata st.tabs (unpacking di tupla)
        trovata = False
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for t in node.targets:
                    nomi = ([e.id for e in t.elts if isinstance(e, ast.Name)]
                            if isinstance(t, ast.Tuple)
                            else ([t.id] if isinstance(t, ast.Name) else []))
                    if "tab172" in nomi:
                        trovata = True
        assert trovata, "tab172 non dichiarata"
        # titolo presente nella lista dei titoli
        assert '"⛓️ Cointegrazione"' in _APP_SRC
        # blocco with tab172 presente
        assert "with tab172:" in _APP_SRC
        # helper a livello modulo
        assert "\ndef calcola_cointegrazione(" in _APP_SRC
        # chiavi widget uniche
        keys = []
        for m in ast.walk(tree):
            if isinstance(m, ast.Call) and getattr(m.func, "attr", "") in (
                    "selectbox", "radio", "number_input", "file_uploader",
                    "download_button", "slider", "text_input", "date_input"):
                for kw in m.keywords:
                    if kw.arg == "key" and isinstance(kw.value, ast.Constant):
                        keys.append(kw.value.value)
        cg_keys = [k for k in keys if str(k).startswith("cg172_")]
        assert len(cg_keys) == len(set(cg_keys)) and len(cg_keys) >= 8
        # conteggio titoli == variabili (robusto: non dipende dal numero totale)
        import re
        m = re.search(r"((?:tab\d+, )+tab\d+) = st\.tabs\(\[(.*?)\]\)",
                      _APP_SRC, re.S)
        assert m, "dichiarazione st.tabs non trovata"
        variabili = [v.strip() for v in m.group(1).split(",")]
        n_titoli = len(re.findall(r'"[^"]+"', m.group(2)))
        assert n_titoli == len(variabili), (n_titoli, len(variabili))
        # sequenza senza buchi: tab1..tabN tutte presenti
        numeri = sorted(int(v[3:]) for v in variabili)
        assert numeri == list(range(1, numeri[-1] + 1))
        assert "tab172" in variabili

    def test_nessun_segreto(self):
        src_fn = _APP_SRC.split("def calcola_cointegrazione(")[1].split(
            "\n\n\n")[0]
        for parola in ("api_key", "apikey", "password", "token", "secret"):
            assert parola not in src_fn.lower()
