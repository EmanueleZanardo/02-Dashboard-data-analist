"""Test calcola_slippage_esecuzione - tab183 (stile pytest, via appfuncs).

Copertura: caso calcolato a mano (2 giorni 100/110, 1 MW, 1 giorno di
fornitura, 2 tranche, liquidita' 2400, coeff 1.0 -> impatto sqrt(0.005),
slippage 298.19 EUR acquisto / 58.19 EUR vendita), coeff 0 -> slippage 0,
frontiera monotona decrescente su serie piatta, rischio di timing nullo su
serie piatta, prezzo di arrivo custom, clamp delle tranche ai giorni
disponibili, giudizio MODERATO calibrato, slippage negativo a mercato
favorevole, parametri non validi (mw/giorni/direzione/liquidita'/coeff/
prezzo_riferimento), serie vuota / non datetime / 1 solo giorno,
NaN/duplicati/tz, determinismo, contenuto df_slice, registry tab183.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load  # noqa: E402

fns = load("calcola_slippage_esecuzione")
se = fns["calcola_slippage_esecuzione"]


def serie_giorni(prezzi_giorno, start="2025-01-06"):
    """Serie oraria con prezzo costante per giorno (lista di prezzi)."""
    vals = []
    for p in prezzi_giorno:
        vals.extend([float(p)] * 24)
    idx = pd.date_range(start, periods=len(vals), freq="h")
    return pd.Series(np.asarray(vals, dtype=float), index=idx)


class TestSlippageBase:
    def test_a_mano_acquisto(self):
        # 2 giorni [100, 110]; 1 MW x 24h x 1gg = 24 MWh; 2 tranche da 12 MWh
        # impatto = sqrt(12/2400) = sqrt(0.005) = 0.07071068
        # eseguito = 12*100*1.07071068 + 12*110*1.07071068 = 2698.1909
        # carta = 24*100 = 2400 -> slippage 298.1909
        r = se(serie_giorni([100, 110]), mw=1.0, giorni_fornitura=1,
               giorni_esecuzione=2, direzione="acquisto",
               liquidita_giornaliera_mwh=2400.0, coeff_impatto=1.0)
        assert r["valido"] and r["errore"] is None
        assert r["n_tranche"] == 2
        assert r["totale_mwh"] == pytest.approx(24.0)
        assert r["mwh_tranche"] == pytest.approx(12.0)
        assert r["impatto"] == pytest.approx(np.sqrt(0.005))
        assert r["prezzo_arrivo"] == pytest.approx(100.0)
        assert r["costo_carta"] == pytest.approx(2400.0)
        assert r["costo_eseguito"] == pytest.approx(2698.1909, abs=1e-3)
        assert r["slippage_eur"] == pytest.approx(298.1909, abs=1e-3)
        assert r["slippage_eur_mwh"] == pytest.approx(298.1909 / 24.0, abs=1e-4)
        assert r["slippage_pct"] == pytest.approx(298.1909 / 2400.0 * 100.0, abs=1e-4)
        # rischio timing = std([100,110], ddof=1) * 24
        assert r["rischio_timing_eur"] == pytest.approx(np.std([100.0, 110.0], ddof=1) * 24.0)
        assert r["giudizio"] == "RILEVANTE"
        d = r["df_slice"]
        assert list(d.columns) == ["Data", "Prezzo medio (EUR/MWh)", "MWh",
                                   "Impatto (%)", "Prezzo eseguito (EUR/MWh)",
                                   "Controvalore (EUR)"]
        assert len(d) == 2
        assert d["Controvalore (EUR)"].sum() == pytest.approx(2698.1909, abs=1e-2)
        f = r["df_frontiera"]
        assert f["Tranche giornaliere"].tolist() == [1, 2]

    def test_a_mano_vendita(self):
        # vendita: incassato = 12*100*0.92928932 + 12*110*0.92928932 = 2341.8091
        # slippage = carta - incassato = 58.1909
        r = se(serie_giorni([100, 110]), mw=1.0, giorni_fornitura=1,
               giorni_esecuzione=2, direzione="vendita",
               liquidita_giornaliera_mwh=2400.0, coeff_impatto=1.0)
        assert r["valido"]
        assert r["costo_eseguito"] == pytest.approx(2341.8091, abs=1e-3)
        assert r["slippage_eur"] == pytest.approx(58.1909, abs=1e-3)
        assert r["giudizio"] == "RILEVANTE"  # 2.42% del nozionale

    def test_coeff_zero(self):
        r = se(serie_giorni([100, 110, 90]), mw=2.0, giorni_fornitura=7,
               giorni_esecuzione=3, coeff_impatto=0.0)
        assert r["valido"]
        assert r["impatto"] == pytest.approx(0.0)
        assert r["slippage_eur"] == pytest.approx(0.0, abs=1e-9)
        assert r["costo_eseguito"] == pytest.approx(r["costo_carta"])
        assert r["giudizio"] == "TRASCURABILE"

    def test_frontiera_monotona_piatta(self):
        # prezzo piatto 100: lo slippage e' solo impatto -> decresce con k
        r = se(serie_giorni([100] * 6), mw=1.0, giorni_fornitura=1,
               giorni_esecuzione=6, liquidita_giornaliera_mwh=2400.0,
               coeff_impatto=1.0)
        assert r["valido"]
        f = r["df_frontiera"]
        assert len(f) == 6
        vals = f["Slippage (EUR)"].to_numpy()
        assert (np.diff(vals) < -1e-9).all()
        assert (f["Rischio di timing (EUR)"].to_numpy() == 0.0).all()
        # k=1: impatto = sqrt(24/2400) = 0.1 -> slippage = 2400*0.1 = 240
        assert f["Slippage (EUR)"].iloc[0] == pytest.approx(240.0)

    def test_prezzo_riferimento_custom(self):
        r = se(serie_giorni([100, 110]), mw=1.0, giorni_fornitura=1,
               giorni_esecuzione=2, liquidita_giornaliera_mwh=2400.0,
               coeff_impatto=1.0, prezzo_riferimento=105.0)
        assert r["valido"]
        assert r["prezzo_arrivo"] == pytest.approx(105.0)
        assert r["costo_carta"] == pytest.approx(2520.0)
        assert r["slippage_eur"] == pytest.approx(2698.1909 - 2520.0, abs=1e-3)

    def test_clamp_tranche_ai_giorni(self):
        r = se(serie_giorni([100] * 5), mw=1.0, giorni_fornitura=1,
               giorni_esecuzione=90)
        assert r["valido"]
        assert r["n_tranche"] == 5 and r["n_giorni"] == 5

    def test_giudizio_moderato(self):
        # piatto 100, 1 tranche: slippage% = impatto*100; impatto = 0.5*sqrt(24/60000) = 0.01
        r = se(serie_giorni([100, 100]), mw=1.0, giorni_fornitura=1,
               giorni_esecuzione=1, liquidita_giornaliera_mwh=60000.0,
               coeff_impatto=0.5)
        assert r["valido"]
        assert r["slippage_pct"] == pytest.approx(1.0, abs=1e-9)
        assert r["giudizio"] == "MODERATO"

    def test_slippage_negativo_mercato_favorevole(self):
        # acquisto mentre i prezzi scendono, coeff 0: paghi meno dell'arrivo
        r = se(serie_giorni([110, 100]), mw=1.0, giorni_fornitura=1,
               giorni_esecuzione=2, coeff_impatto=0.0)
        assert r["valido"]
        assert r["slippage_eur"] == pytest.approx(2520.0 - 2640.0)
        assert r["giudizio"] == "TRASCURABILE"


class TestSlippageErrori:
    def test_mw_non_validi(self):
        base = serie_giorni([100, 100])
        for mw in [0, -1.0, "x", True, None, float("nan"), float("inf")]:
            r = se(base, mw=mw)
            assert not r["valido"] and r["errore"] is not None, mw

    def test_giorni_non_validi(self):
        base = serie_giorni([100, 100])
        for gf in [0, 366, 2.5, "30", True, None]:
            r = se(base, mw=1.0, giorni_fornitura=gf)
            assert not r["valido"] and r["errore"] is not None, gf
        for ge in [0, 91, 1.5, "10", True, None]:
            r = se(base, mw=1.0, giorni_esecuzione=ge)
            assert not r["valido"] and r["errore"] is not None, ge

    def test_direzione_non_valida(self):
        base = serie_giorni([100, 100])
        for d in ["long", "", None, 1]:
            r = se(base, mw=1.0, direzione=d)
            assert not r["valido"] and r["errore"] is not None, d

    def test_liquidita_coeff_non_validi(self):
        base = serie_giorni([100, 100])
        for liq in [0, -5.0, float("inf"), float("nan"), "x", True, None]:
            r = se(base, mw=1.0, liquidita_giornaliera_mwh=liq)
            assert not r["valido"] and r["errore"] is not None, liq
        for c in [-0.1, float("nan"), float("inf"), "x", True, None]:
            r = se(base, mw=1.0, coeff_impatto=c)
            assert not r["valido"] and r["errore"] is not None, c

    def test_prezzo_riferimento_non_valido(self):
        base = serie_giorni([100, 100])
        for p in [-10.0, 0.0, float("nan"), float("inf"), "x", True]:
            r = se(base, mw=1.0, prezzo_riferimento=p)
            assert not r["valido"] and r["errore"] is not None, p

    def test_serie_vuota(self):
        r = se(pd.Series(dtype=float), mw=1.0)
        assert not r["valido"] and r["errore"] is not None

    def test_indice_non_datetime(self):
        r = se(pd.Series([1.0, 2.0, 3.0]), mw=1.0)
        assert not r["valido"] and r["errore"] is not None

    def test_un_solo_giorno(self):
        r = se(serie_giorni([100]), mw=1.0)
        assert not r["valido"] and "2 giorni" in r["errore"]

    def test_nan_duplicati_tz(self):
        p = serie_giorni([100, 110, 90, 105])
        p.iloc[10] = np.nan
        p = pd.concat([p, p.iloc[[0]]])
        p = p.tz_localize("Europe/Zurich", nonexistent="shift_forward", ambiguous="NaT")
        r = se(p, mw=1.0, giorni_fornitura=1, giorni_esecuzione=4,
               liquidita_giornaliera_mwh=2400.0, coeff_impatto=1.0)
        assert r["valido"]
        assert r["n_giorni"] == 4 and r["n_tranche"] == 4

    def test_determinismo(self):
        kw = dict(mw=3.0, giorni_fornitura=10, giorni_esecuzione=7,
                  liquidita_giornaliera_mwh=40000.0, coeff_impatto=0.7)
        a = se(serie_giorni([100, 110, 90, 105, 95, 115, 102]), **kw)
        b = se(serie_giorni([100, 110, 90, 105, 95, 115, 102]), **kw)
        assert a["valido"] and b["valido"]
        pd.testing.assert_frame_equal(a["df_slice"], b["df_slice"])
        pd.testing.assert_frame_equal(a["df_frontiera"], b["df_frontiera"])
        assert a["slippage_eur"] == b["slippage_eur"]


class TestRegistryTab183:
    def test_tab183_registrata(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py").read_text(encoding="utf-8")
        m = re.search(r"tab1, tab2, .*? = st\.tabs\(\[", src, re.S)
        dvars = re.findall(r"tab\d+", m.group(0))
        assert "tab183" in dvars
        assert dvars == ["tab%d" % i for i in range(1, len(dvars) + 1)]
        withs = re.findall(r"^    with (tab\d+):", src, re.M)
        assert withs == ["tab%d" % i for i in range(1, len(withs) + 1)]
        assert "tab183" in withs
        assert len(withs) == len(dvars) >= 183
        assert '"💸 Slippage di esecuzione"' in src
        assert "calcola_slippage_esecuzione" in src
        keys = re.findall(r'key="(sl183_[^"]+)"', src)
        assert len(keys) == len(set(keys)) and len(keys) >= 7
