"""Test tab196 (stile pytest): business case accumulo (batteria merchant).

La funzione e' pura (niente Streamlit nel corpo): estratta da app.py via
AST con tests/appfuncs.py.

Modello: ricavo giornaliero da arbitraggio = max(0, E*(Pmax*eta - Pmin)) *
cicli; annualizzato sui giorni osservati; flussi annui con degrado della
capacita', piu' ricavi fissi, meno opex; NPV al tasso, IRR per bisezione,
payback interpolato.

Numeri a mano (2 giorni, 48h: giorno1 12h a 10 + 12h a 100; giorno2 12h a
20 + 12h a 60; E=20 MWh, eta=0.85, 1 ciclo/giorno):
  giorno1: 20*(100*0.85-10) = 1500.0 €; giorno2: 20*(60*0.85-20) = 620.0 €
  ric_arb_anno = 2120 * 365/2 = 386900.0 €
  capex = 20*1000*350 = 7_000_000 €; opex = 10*1000*10 = 100_000 €/anno
  flussi[t] = 386900*0.98^(t-1) - 100000, t=1..15; NPV al 6%.
"""

import re
from pathlib import Path

import numpy as np
import pandas as pd

from appfuncs import load

_F = load("calcola_business_case_accumulo")
calcola_business_case_accumulo = _F["calcola_business_case_accumulo"]

P = dict(potenza_mw=10.0, energia_mwh=20.0, capex_eur_kwh=100.0,
         opex_eur_kw_anno=10.0, efficienza_pct=85.0, cicli_giorno=1.0,
         degrado_pct=2.0, ricavi_fissi_eur_anno=0.0, tasso_pct=6.0,
         vita_anni=15, n_punti_sens=11)


def serie_2giorni():
    idx = pd.date_range("2026-01-01", periods=48, freq="h")
    vals = np.array([10.0] * 12 + [100.0] * 12 + [20.0] * 12 + [60.0] * 12)
    return pd.Series(vals, index=idx)


def attesi_manuali():
    ric_arb = 386900.0
    capex, opex = 2_000_000.0, 100_000.0
    flussi = [ric_arb * 0.98 ** (t - 1) - opex for t in range(1, 16)]
    npv = -capex + sum(cf / 1.06 ** t for t, cf in enumerate(flussi, 1))
    return ric_arb, capex, opex, flussi, npv


class TestBusinessCaseAccumulo:
    def test_numeri_a_mano(self):
        r = calcola_business_case_accumulo(serie_2giorni(), **P)
        ric_arb, capex, opex, flussi, npv = attesi_manuali()
        assert r["valido"] and r["errore"] is None
        assert r["n_giorni"] == 2
        assert abs(r["capex_eur"] - capex) < 1e-6
        assert abs(r["opex_annuo_eur"] - opex) < 1e-6
        assert abs(r["ricavo_arb_anno_eur"] - ric_arb) < 1e-6
        assert abs(r["npv_eur"] - npv) < 1e-3
        assert len(r["flussi"]) == 15
        for got, exp in zip(r["flussi"], flussi):
            assert abs(got - exp) < 1e-6
        # degrado: flusso anno 2 = (flusso anno 1 + opex) * 0.98 - opex
        assert abs(r["flussi"][1] - ((r["flussi"][0] + 100000) * 0.98 - 100000)) < 1e-6

    def test_irr_coerente(self):
        r = calcola_business_case_accumulo(serie_2giorni(), **P)
        irr = r["irr_pct"]
        assert irr is not None and irr > 6.0  # NPV>0 -> IRR>tasso
        # NPV valutato all'IRR deve azzerarsi (ricalcolo indipendente)
        flussi = r["flussi"]
        npv_irr = -2_000_000.0 + sum(
            cf / (1.0 + irr / 100.0) ** t for t, cf in enumerate(flussi, 1))
        assert abs(npv_irr) < 1.0

    def test_payback_coerente(self):
        r = calcola_business_case_accumulo(serie_2giorni(), **P)
        pb = r["payback_anni"]
        assert pb is not None and 0 < pb <= 15
        cum = -2_000_000.0
        for t, cf in enumerate(r["flussi"], 1):
            cum += cf
            if cum >= 0:
                assert t - 1 <= pb <= t
                break

    def test_verdetto_non_conveniente(self):
        q = dict(P, capex_eur_kwh=2000.0)
        r = calcola_business_case_accumulo(serie_2giorni(), **q)
        assert r["valido"] and r["npv_eur"] < 0
        assert "NON CONVENIENTE" in r["verdetto"]
        assert r["payback_anni"] is None

    def test_verdetto_molto_conveniente(self):
        q = dict(P, capex_eur_kwh=0.0)
        r = calcola_business_case_accumulo(serie_2giorni(), **q)
        assert r["valido"] and r["npv_eur"] > 0
        assert "MOLTO CONVENIENTE" in r["verdetto"]

    def test_spread_negativo_rende_zero(self):
        idx = pd.date_range("2026-01-01", periods=48, freq="h")
        vals = np.array([50.0] * 24 + [10.0] * 12 + [100.0] * 12)
        s = pd.Series(vals, index=idx)
        # giorno1 piatto (spread 0, con eta<1 sarebbe negativo -> 0);
        # giorno2: 20*(85-10)=1500
        r = calcola_business_case_accumulo(s, **P)
        assert r["valido"]
        assert abs(r["ricavo_arb_anno_eur"] - 1500.0 * 365.0 / 2.0) < 1e-6

    def test_ricavi_fissi_e_opex(self):
        q = dict(P, ricavi_fissi_eur_anno=50000.0)
        r = calcola_business_case_accumulo(serie_2giorni(), **q)
        _, _, _, flussi, _ = attesi_manuali()
        assert abs(r["flussi"][0] - (flussi[0] + 50000.0)) < 1e-6

    def test_cicli_giorno_scalano(self):
        q = dict(P, cicli_giorno=2.0)
        r = calcola_business_case_accumulo(serie_2giorni(), **q)
        assert abs(r["ricavo_arb_anno_eur"] - 2.0 * 386900.0) < 1e-6

    def test_sensibilita_monotona(self):
        r = calcola_business_case_accumulo(serie_2giorni(), **P)
        df = r["df_sens"]
        assert len(df) == 11
        assert list(df.columns) == ["Capex (€/kWh)", "NPV (€ mln)"]
        npvs = df["NPV (€ mln)"].to_numpy()
        assert all(npvs[i] >= npvs[i + 1] for i in range(len(npvs) - 1))
        # range 0.5x..2x del capex inserito
        assert abs(df["Capex (€/kWh)"].iloc[0] - 50.0) < 1e-9
        assert abs(df["Capex (€/kWh)"].iloc[-1] - 200.0) < 1e-9

    def test_df_flussi(self):
        r = calcola_business_case_accumulo(serie_2giorni(), **P)
        df = r["df_flussi"]
        assert len(df) == 15 and list(df["Anno"]) == list(range(1, 16))
        assert abs(df["Cumulato (€)"].iloc[-1] -
                   (-2_000_000.0 + sum(r["flussi"]))) < 1.0

    def test_parametri_invalidi(self):
        s = serie_2giorni()
        casi = [
            dict(potenza_mw=0.0), dict(potenza_mw=-1.0),
            dict(energia_mwh=0.0), dict(capex_eur_kwh=-5.0),
            dict(opex_eur_kw_anno=-1.0), dict(efficienza_pct=0.0),
            dict(efficienza_pct=101.0), dict(cicli_giorno=0.0),
            dict(cicli_giorno=4.5), dict(degrado_pct=-1.0),
            dict(degrado_pct=51.0), dict(ricavi_fissi_eur_anno=-1.0),
            dict(tasso_pct=-1.0), dict(tasso_pct=51.0),
            dict(vita_anni=0), dict(vita_anni=41), dict(vita_anni=2.5),
            dict(n_punti_sens=2), dict(n_punti_sens=102),
            dict(potenza_mw=True), dict(capex_eur_kwh=float("inf")),
            dict(tasso_pct=float("nan")),
        ]
        for kw in casi:
            q = dict(P, **kw)
            r = calcola_business_case_accumulo(s, **q)
            assert not r["valido"] and r["errore"], kw

    def test_serie_invalida(self):
        assert not calcola_business_case_accumulo(
            pd.Series([], dtype=float), **P)["valido"]
        assert not calcola_business_case_accumulo(
            pd.Series([50.0] * 23,
                      index=pd.date_range("2026-01-01", periods=23, freq="h")),
            **P)["valido"]
        assert not calcola_business_case_accumulo(
            "non una serie", **P)["valido"]

    def test_determinismo(self):
        s = serie_2giorni()
        a = calcola_business_case_accumulo(s, **P)
        b = calcola_business_case_accumulo(s, **P)
        assert a["npv_eur"] == b["npv_eur"]
        assert a["verdetto"] == b["verdetto"]
        assert a["df_sens"].equals(b["df_sens"])

    def test_tab196_dichiarata(self):
        src = Path(__file__).parent.parent.joinpath("app.py").read_text()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 307
        assert titoli[-1] == "🌊📉 Expected Shortfall: la perdita oltre il VaR"
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab196" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab196" in withs
        assert len(withs) == len(dvars) == 307
        keys = re.findall(r'key="(bac196_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 12
