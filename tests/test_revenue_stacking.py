"""Test calcola_revenue_stacking - tab184 (stile pytest, via appfuncs).

Copertura: caso piatto calcolato a mano (2 giorni a 100, 2 MW / 4 MWh ->
tutto FCR a 1728 EUR, FLUSSO DOMINANTE: FCR), caso stacking calcolato a mano
(1 giorno 50/150, eff 1.0, 2 MW / 3 MWh, FCR 5 EUR/MW/h -> ottimo a
pf=0.7 MW con 344 EUR, STACKING VINCENTE che batte i flussi singoli),
caso manuale calcolato a mano (220 EUR), arbitraggio dominante, nessun
ricavo, parametri non validi (potenza/capacita'/efficienza/prezzi/ore/
headroom/modo/manuale), serie vuota / non datetime / troppo corta,
NaN/duplicati/tz, determinismo, contenuto df_giornaliero e df_griglia,
registry tab184.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load  # noqa: E402

fns = load("calcola_revenue_stacking")
rs = fns["calcola_revenue_stacking"]


def serie_giorni(prezzi_giorno, start="2025-01-06"):
    """Serie oraria con prezzo costante per giorno (lista di prezzi)."""
    vals = []
    for p in prezzi_giorno:
        vals.extend([float(p)] * 24)
    idx = pd.date_range(start, periods=len(vals), freq="h")
    return pd.Series(np.asarray(vals, dtype=float), index=idx)


def serie_spread():
    """1 giorno: 12h a 50, 12h a 150."""
    vals = [50.0] * 12 + [150.0] * 12
    idx = pd.date_range("2025-01-06", periods=24, freq="h")
    return pd.Series(np.asarray(vals, dtype=float), index=idx)


class TestRevenueStackingBase:
    def test_piatta_tutto_fcr(self):
        # 2 giorni a 100 EUR/MWh: spread netto 0 -> arbitraggio 0.
        # FCR: 2 MW x 18 EUR/MW/h x 24 h x 2 gg = 1728 EUR > aFRR (960).
        r = rs(serie_giorni([100, 100]), pot_mw=2.0, cap_mwh=4.0,
               prezzo_fcr=18.0, prezzo_afrr=10.0)
        assert r["valido"]
        assert r["p_fcr"] == pytest.approx(2.0)
        assert r["p_afrr"] == pytest.approx(0.0)
        assert r["p_arb"] == pytest.approx(0.0)
        assert r["ricavo_totale_eur"] == pytest.approx(1728.0)
        assert r["r_arb_eur"] == pytest.approx(0.0)
        assert r["giudizio"] == "FLUSSO DOMINANTE: FCR"
        assert r["ricavo_medio_giorno"] == pytest.approx(864.0)
        assert r["ricavo_per_mw_giorno"] == pytest.approx(432.0)

    def test_stacking_vincente_a_mano(self):
        # 1 giorno 50/150, eff 1.0 -> spread netto 100 EUR/MWh.
        # pot 2 MW, cap 3 MWh, FCR 5 EUR/MW/h x 24 h = 120 EUR/MW/gg.
        # Singoli: arb = 100 x min(3, 4) = 300; FCR = 240.
        # Ottimo su griglia: pf = 0.7 -> lock 0.35, cap_disp 2.65,
        # p_arb 1.3, e_ciclo = min(2.65, 2.6) = 2.6 -> arb 260 + fcr 84 = 344.
        r = rs(serie_spread(), pot_mw=2.0, cap_mwh=3.0, eff=1.0,
               prezzo_fcr=5.0, prezzo_afrr=0.0)
        assert r["valido"]
        assert r["p_fcr"] == pytest.approx(0.7)
        assert r["p_afrr"] == pytest.approx(0.0)
        assert r["p_arb"] == pytest.approx(1.3)
        assert r["ricavo_totale_eur"] == pytest.approx(344.0)
        assert r["ricavo_totale_eur"] > r["miglior_singolo_eur"]
        assert r["nome_miglior_singolo"] == "arbitraggio"
        assert r["miglior_singolo_eur"] == pytest.approx(300.0)
        assert r["giudizio"] == "STACKING VINCENTE"
        assert r["energia_lock_mwh"] == pytest.approx(0.35)
        assert r["cap_residua_mwh"] == pytest.approx(2.65)
        assert r["e_ciclo_mwh"] == pytest.approx(2.6)

    def test_manuale_a_mano(self):
        # p_fcr 1.0, p_afrr 0.5, p_arb 0.5; lock = 0.5 + 0.5 = 1.0;
        # cap_disp 2.0; e_ciclo = min(2, 1) = 1 -> arb 100;
        # fcr 1 x 5 x 24 = 120; afrr 0.5 x 0 x 24 = 0; totale 220.
        r = rs(serie_spread(), pot_mw=2.0, cap_mwh=3.0, eff=1.0,
               prezzo_fcr=5.0, prezzo_afrr=0.0,
               modo="manuale", p_fcr=1.0, p_afrr=0.5)
        assert r["valido"]
        assert r["modo"] == "manuale"
        assert r["r_arb_eur"] == pytest.approx(100.0)
        assert r["r_fcr_eur"] == pytest.approx(120.0)
        assert r["r_afrr_eur"] == pytest.approx(0.0)
        assert r["ricavo_totale_eur"] == pytest.approx(220.0)
        assert r["df_griglia"].empty

    def test_arbitraggio_dominante(self):
        # Spread 100, FCR 1 EUR/MW/h: arb 400 > fcr 48 -> tutto arbitraggio.
        r = rs(serie_spread(), pot_mw=2.0, cap_mwh=4.0, eff=1.0,
               prezzo_fcr=1.0, prezzo_afrr=0.0)
        assert r["valido"]
        assert r["p_arb"] == pytest.approx(2.0)
        assert r["ricavo_totale_eur"] == pytest.approx(400.0)
        assert r["giudizio"] == "FLUSSO DOMINANTE: ARBITRAGGIO"

    def test_nessun_ricavo(self):
        r = rs(serie_giorni([100]), prezzo_fcr=0.0, prezzo_afrr=0.0)
        assert r["valido"]
        assert r["ricavo_totale_eur"] == pytest.approx(0.0)
        assert r["giudizio"] == "NESSUN RICAVO"


class TestRevenueStackingErrori:
    @pytest.mark.parametrize("pot", [0, -1.0, "x", None, True, float("nan")])
    def test_pot_mw_invalida(self, pot):
        r = rs(serie_giorni([100]), pot_mw=pot)
        assert not r["valido"] and r["errore"]

    @pytest.mark.parametrize("cap", [0, -2.0, "x", True])
    def test_cap_mwh_invalida(self, cap):
        r = rs(serie_giorni([100]), cap_mwh=cap)
        assert not r["valido"] and r["errore"]

    @pytest.mark.parametrize("eff", [0, -0.5, 1.5, 2.0, "x", True])
    def test_eff_invalida(self, eff):
        r = rs(serie_giorni([100]), eff=eff)
        assert not r["valido"] and r["errore"]

    @pytest.mark.parametrize("kw", ["prezzo_fcr", "prezzo_afrr"])
    def test_prezzi_riserva_negativi(self, kw):
        r = rs(serie_giorni([100]), **{kw: -1.0})
        assert not r["valido"] and r["errore"]

    @pytest.mark.parametrize("kw", ["ore_fcr", "ore_afrr"])
    @pytest.mark.parametrize("ore", [-1.0, 24.5, "x", True])
    def test_ore_invalide(self, kw, ore):
        r = rs(serie_giorni([100]), **{kw: ore})
        assert not r["valido"] and r["errore"]

    @pytest.mark.parametrize("kw", ["lock_fcr_h", "lock_afrr_h"])
    def test_lock_negativi(self, kw):
        r = rs(serie_giorni([100]), **{kw: -0.5})
        assert not r["valido"] and r["errore"]

    def test_modo_invalido(self):
        r = rs(serie_giorni([100]), modo="auto")
        assert not r["valido"] and r["errore"]

    def test_manuale_somma_supera_potenza(self):
        r = rs(serie_giorni([100]), modo="manuale", p_fcr=1.5, p_afrr=1.0)
        assert not r["valido"] and "pot_mw" in r["errore"]

    def test_manuale_headroom_supera_capacita(self):
        # lock = 2 x 0.5 = 1.0 > cap 0.5 -> non fattibile
        r = rs(serie_giorni([100]), pot_mw=2.0, cap_mwh=0.5,
               modo="manuale", p_fcr=2.0, p_afrr=0.0)
        assert not r["valido"] and r["errore"]

    def test_serie_vuota(self):
        r = rs(pd.Series([], dtype=float))
        assert not r["valido"] and r["errore"]

    def test_serie_non_series(self):
        r = rs([100.0] * 24)
        assert not r["valido"] and r["errore"]

    def test_indice_non_datetime(self):
        s = pd.Series([100.0] * 24, index=["a"] * 24)
        r = rs(s)
        assert not r["valido"] and r["errore"]

    def test_giorni_troppo_corti(self):
        # 3 ore sole: nessun giorno con >= 4 ore
        idx = pd.date_range("2025-01-06", periods=3, freq="h")
        r = rs(pd.Series([100.0, 110.0, 105.0], index=idx))
        assert not r["valido"] and r["errore"]


class TestRevenueStackingRobusto:
    def test_nan_duplicati_tz(self):
        idx = pd.date_range("2025-01-06", periods=48, freq="h", tz="Europe/Zurich")
        vals = np.full(48, 100.0)
        vals[5] = np.nan
        s = pd.Series(vals, index=idx)
        s = pd.concat([s, s.iloc[[10]]])  # duplicato
        r = rs(s, prezzo_fcr=10.0)
        assert r["valido"]
        # 2 giorni, spread 0, tutto FCR: 2 x 10 x 24 x 2 = 960
        assert r["ricavo_totale_eur"] == pytest.approx(960.0)

    def test_determinismo(self):
        kw = dict(pot_mw=2.0, cap_mwh=3.0, eff=1.0, prezzo_fcr=5.0)
        r1 = rs(serie_spread(), **kw)
        r2 = rs(serie_spread(), **kw)
        assert r1["ricavo_totale_eur"] == r2["ricavo_totale_eur"]
        assert r1["p_fcr"] == r2["p_fcr"] and r1["p_arb"] == r2["p_arb"]
        assert r1["df_giornaliero"].equals(r2["df_giornaliero"])
        assert r1["giudizio"] == r2["giudizio"]

    def test_df_giornaliero(self):
        r = rs(serie_giorni([100, 110]), pot_mw=2.0, cap_mwh=4.0, prezzo_fcr=18.0)
        df = r["df_giornaliero"]
        assert list(df.columns) == ["Giorno", "Spread netto (EUR/MWh)",
                                    "Ricavo arbitraggio (EUR)", "Ricavo FCR (EUR)",
                                    "Ricavo aFRR (EUR)", "Ricavo totale (EUR)"]
        assert len(df) == 2
        assert df["Ricavo totale (EUR)"].sum() == pytest.approx(r["ricavo_totale_eur"], abs=0.02)
        assert (df["Ricavo FCR (EUR)"] == 864.0).all()  # 2 x 18 x 24

    def test_df_griglia_ottimale(self):
        r = rs(serie_giorni([100, 110]), prezzo_fcr=18.0)
        g = r["df_griglia"]
        assert not g.empty
        assert list(g.columns) == ["P FCR (MW)", "P aFRR (MW)",
                                   "P arbitraggio (MW)", "Ricavo totale (EUR)"]
        # 21x21 triangolare: 231 combinazioni
        assert len(g) == 231
        assert g["Ricavo totale (EUR)"].max() == pytest.approx(r["ricavo_totale_eur"], abs=0.02)


class TestRegistryTab184:
    def test_tab184_registrata(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(encoding="utf-8")
        m = re.search(r"tab1, tab2, .*? = st\.tabs\(\[", src, re.S)
        dvars = re.findall(r"tab\d+", m.group(0))
        assert "tab184" in dvars
        assert dvars == ["tab%d" % i for i in range(1, len(dvars) + 1)]
        withs = re.findall(r"^    with (tab\d+):", src, re.M)
        assert withs == ["tab%d" % i for i in range(1, len(withs) + 1)]
        assert "tab184" in withs
        assert len(withs) == len(dvars) >= 184
        assert '"🪙 Revenue stacking"' in src
        assert "calcola_revenue_stacking" in src
        keys = re.findall(r'key="(rs184_[^"]+)"', src)
        assert len(keys) == len(set(keys)) and len(keys) >= 10
