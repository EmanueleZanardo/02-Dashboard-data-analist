"""Test tab220 (stile pytest): Costo CBAM stimato.

Le funzioni sono pure (niente Streamlit nel corpo): estratte da app.py via
AST con tests/appfuncs.py.
"""

import re
from pathlib import Path

import pandas as pd
import pytest

from appfuncs import load

_F = load("calcola_cbam")
calcola_cbam = _F["calcola_cbam"]


class TestCbamBase:
    def test_numeri_a_mano_2026(self):
        # 1000 MWh x 0.40 tCO2/MWh = 400 tCO2; fattore 2026 = 2.5%
        # -> 10 certificati x 75.36 € = 753.60 €
        r = calcola_cbam(1000.0, 0.40, 75.36, anno=2026)
        assert r["errore"] is None and r["valido"]
        assert r["emissioni_tco2"] == pytest.approx(400.0)
        assert r["fattore_cbam"] == pytest.approx(0.025)
        assert r["certificati_lordi"] == pytest.approx(10.0)
        assert r["certificati_netti"] == pytest.approx(10.0)
        assert r["costo_annuo_eur"] == pytest.approx(753.60, abs=0.01)
        assert r["costo_unitario_eur"] == pytest.approx(0.7536, abs=1e-4)

    def test_phase_in_2034_pieno(self):
        r = calcola_cbam(1000.0, 0.40, 75.36, anno=2034)
        assert r["errore"] is None
        assert r["certificati_netti"] == pytest.approx(400.0)
        assert r["costo_annuo_eur"] == pytest.approx(400.0 * 75.36, abs=0.01)

    def test_deduzione_origine(self):
        # 10 tCO2 lorde; pagati 376.80 € all'origine = 5 tCO2 eq. a 75.36 €/t
        r = calcola_cbam(1000.0, 0.40, 75.36, anno=2026,
                         carbonio_pagato_origine_eur=376.80)
        assert r["errore"] is None
        assert r["deduzione_origine_tco2"] == pytest.approx(5.0)
        assert r["certificati_netti"] == pytest.approx(5.0)
        assert r["costo_annuo_eur"] == pytest.approx(376.80, abs=0.01)

    def test_deduzione_cappata(self):
        # deduzione superiore al lordo -> certificati netti 0, mai negativi
        r = calcola_cbam(1000.0, 0.40, 75.36, anno=2026,
                         carbonio_pagato_origine_eur=100000.0)
        assert r["errore"] is None
        assert r["certificati_netti"] == pytest.approx(0.0)
        assert r["costo_annuo_eur"] == pytest.approx(0.0)

    def test_aggravio_verdetti(self):
        # costo unitario 0.7536 €/MWh su bene da 100 €/MWh -> 0.75% -> TRASCURABILE
        r = calcola_cbam(1000.0, 0.40, 75.36, anno=2026,
                         prezzo_bene_eur_unita=100.0)
        assert r["aggravio_pct"] == pytest.approx(0.7536, abs=1e-3)
        assert r["verdetto"].startswith("🟢")
        # stesso bene, anno 2034: 30.144 €/1000 MWh = 30.14 €/MWh -> 30.1% -> CRITICO
        r2 = calcola_cbam(1000.0, 0.40, 75.36, anno=2034,
                          prezzo_bene_eur_unita=100.0)
        assert r2["aggravio_pct"] == pytest.approx(30.144, abs=1e-3)
        assert r2["verdetto"].startswith("🔴")
        # senza prezzo bene -> aggravio None, verdetto neutro
        r3 = calcola_cbam(1000.0, 0.40, 75.36, anno=2026)
        assert r3["aggravio_pct"] is None
        assert r3["verdetto"].startswith("ℹ️")

    def test_traiettoria_monotona(self):
        r = calcola_cbam(500.0, 1.40, 80.0, anno=2028,
                         carbonio_pagato_origine_eur=1000.0)
        df = r["df_traiettoria"]
        assert list(df["Anno"]) == list(range(2026, 2035))
        assert (df["Fattore CBAM (%)"].diff().dropna() > 0).all()
        assert df["Fattore CBAM (%)"].iloc[-1] == pytest.approx(100.0)
        assert (df["Costo annuo (€)"].diff().dropna() >= 0).all()
        # 2026 a mano: 500*1.4=700 tCO2 x 2.5% = 17.5 lordi; deduzione 1000/80=12.5
        # -> 5.0 netti x 80 = 400 €
        assert df.iloc[0]["Costo annuo (€)"] == pytest.approx(400.0, abs=0.01)

    def test_determinismo(self):
        a = calcola_cbam(1000.0, 0.40, 75.36, anno=2029,
                         prezzo_bene_eur_unita=90.0)
        b = calcola_cbam(1000.0, 0.40, 75.36, anno=2029,
                         prezzo_bene_eur_unita=90.0)
        assert a["costo_annuo_eur"] == b["costo_annuo_eur"]
        assert a["verdetto"] == b["verdetto"]
        assert a["df_traiettoria"].equals(b["df_traiettoria"])


class TestCbamInvalidi:
    def test_quantita_fattore_prezzo_non_validi(self):
        for bad in [0, -10.0, "x", True, None, float("nan"), float("inf")]:
            assert calcola_cbam(bad, 0.40, 75.36)["errore"], bad
            assert calcola_cbam(1000.0, bad, 75.36)["errore"], bad
            assert calcola_cbam(1000.0, 0.40, bad)["errore"], bad

    def test_anno_fuori_range(self):
        for bad in [2025, 2035, 2026.5, "2026", True, None]:
            assert calcola_cbam(1000.0, 0.40, 75.36, anno=bad)["errore"], bad

    def test_carbonio_pagato_negativo(self):
        assert calcola_cbam(1000.0, 0.40, 75.36,
                            carbonio_pagato_origine_eur=-1.0)["errore"]

    def test_prezzo_bene_negativo(self):
        assert calcola_cbam(1000.0, 0.40, 75.36,
                            prezzo_bene_eur_unita=-5.0)["errore"]


# ------------------------------------------------------- registry
class TestRegistryTab220:
    def test_tab220_dichiarata(self):
        src = Path(__file__).parent.parent.joinpath("app.py").read_text()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 305
        assert titoli[-1] == "🎯🛡 Risk budgeting: il book rispetta i target?"
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab220" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab220" in withs
        assert len(withs) == len(dvars) == 305
        keys = re.findall(r'key="(cb220_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 4
