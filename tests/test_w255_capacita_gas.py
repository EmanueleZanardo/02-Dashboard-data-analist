"""Test tab255 'Capacità gas giornaliera': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab255.
"""

import math
import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("_cg255_num", "cg255_parsa_prelievi", "cg255_statistiche_prelievi",
          "cg255_costo_capacita", "cg255_sforamenti", "cg255_costo_totale",
          "cg255_capacita_ottimale", "cg255_curva_costo")
cg255_parsa_prelievi = _F["cg255_parsa_prelievi"]
cg255_statistiche_prelievi = _F["cg255_statistiche_prelievi"]
cg255_costo_capacita = _F["cg255_costo_capacita"]
cg255_sforamenti = _F["cg255_sforamenti"]
cg255_costo_totale = _F["cg255_costo_totale"]
cg255_capacita_ottimale = _F["cg255_capacita_ottimale"]
cg255_curva_costo = _F["cg255_curva_costo"]

APP = Path(__file__).parent.parent / "app.py"


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab255:
    def test_tab255_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 364
        assert "⛽ Capacità gas giornaliera" in titoli
        assert "tab255" in dvars
        assert "tab255" in withs
        assert titoli[dvars.index("tab255")] == "⛽ Capacità gas giornaliera"
        assert titoli[-1] == "Kelly con vincoli multipli: cap, lotti, stop e drawdown"
        keys = re.findall(r'key="(cg255_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 10

    def test_titoli_allineati_254_255(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab254")] == "♨️ Recupero calore di scarto"
        assert titoli[dvars.index("tab255")] == "⛽ Capacità gas giornaliera"

    def test_helper_definiti_prima_della_ui(self):
        src = APP.read_text(encoding="utf-8")
        i_ws = src.index("if workspace ==")
        for fn in ("cg255_parsa_prelievi", "cg255_statistiche_prelievi",
                   "cg255_costo_capacita", "cg255_sforamenti", "cg255_costo_totale",
                   "cg255_capacita_ottimale", "cg255_curva_costo"):
            assert src.index(f"def {fn}(") < i_ws, fn


class TestCg255ParsaPrelievi:
    def test_base(self):
        vals = cg255_parsa_prelievi("100\n200,5\n\n300")
        assert vals == [100.0, 200.5, 300.0]

    def test_errori(self):
        with pytest.raises(ValueError):
            cg255_parsa_prelievi("")
        with pytest.raises(ValueError):
            cg255_parsa_prelievi("   \n  ")
        with pytest.raises(ValueError) as exc:
            cg255_parsa_prelievi("100\nabc\n300")
        assert "riga 2" in str(exc.value)


class TestCg255Statistiche:
    def test_base(self):
        r = cg255_statistiche_prelievi([100.0, 200.0, 300.0])
        assert r["giorni"] == 3
        assert r["prelievo_max_smc_g"] == 300.0
        assert r["prelievo_p95_smc_g"] == 300.0
        assert r["prelievo_medio_smc_g"] == 200.0

    def test_errori(self):
        with pytest.raises(ValueError):
            cg255_statistiche_prelievi([])
        with pytest.raises(ValueError):
            cg255_statistiche_prelievi([100.0, -5.0])
        with pytest.raises(ValueError):
            cg255_statistiche_prelievi([math.nan])


class TestCg255CostoCapacita:
    def test_base(self):
        r = cg255_costo_capacita(1000.0, 0.90, 365.0)
        assert r["costo_capacita_eur_anno"] == 900.0

    def test_giorni_pro_rata(self):
        r = cg255_costo_capacita(1000.0, 0.90, 182.5)
        assert r["costo_capacita_eur_anno"] == 450.0

    def test_errori(self):
        with pytest.raises(ValueError):
            cg255_costo_capacita(-1.0, 0.90)
        with pytest.raises(ValueError):
            cg255_costo_capacita(1000.0, 0.90, 400.0)
        with pytest.raises(ValueError):
            cg255_costo_capacita(1000.0, 0.90, 0.0)


class TestCg255Sforamenti:
    def test_base(self):
        r = cg255_sforamenti([100.0, 200.0, 300.0], 150.0)
        assert r["giorni_sforamento"] == 2
        assert r["volume_eccedente_smc"] == 200.0
        assert r["sforamento_max_smc_g"] == 150.0
        assert r["quota_giorni_sforamento_pct"] == 66.67

    def test_nessuno_sforamento(self):
        r = cg255_sforamenti([100.0, 200.0], 300.0)
        assert r["giorni_sforamento"] == 0
        assert r["volume_eccedente_smc"] == 0.0

    def test_errori(self):
        with pytest.raises(ValueError):
            cg255_sforamenti([], 150.0)
        with pytest.raises(ValueError):
            cg255_sforamenti([100.0], -1.0)


class TestCg255CostoTotale:
    def test_base(self):
        r = cg255_costo_totale([100.0, 200.0, 300.0], 150.0, 0.90, 2.70)
        assert r["costo_capacita_eur_anno"] == 135.0
        assert r["penali_eur_anno"] == 540.0
        assert r["costo_totale_eur_anno"] == 675.0
        assert r["giorni_sforamento"] == 2

    def test_errori(self):
        with pytest.raises(ValueError):
            cg255_costo_totale([100.0], 150.0, 0.90, -1.0)


class TestCg255CapacitaOttimale:
    def test_penale_alta_tende_al_max(self):
        r = cg255_capacita_ottimale([100.0, 200.0, 300.0], 0.90, 1000.0, n_punti=3)
        assert r["capacita_ottimale_smc_g"] == 300.0
        assert r["penali_eur_anno"] == 0.0
        assert r["costo_totale_eur_anno"] == 270.0

    def test_penale_zero_ottimo_p50(self):
        r = cg255_capacita_ottimale([100.0, 200.0, 300.0], 0.90, 0.0, n_punti=3)
        assert r["capacita_ottimale_smc_g"] == 200.0

    def test_prelievi_nulli(self):
        r = cg255_capacita_ottimale([0.0, 0.0], 0.90, 2.70)
        assert r["capacita_ottimale_smc_g"] == 0.0
        assert r["costo_totale_eur_anno"] == 0.0

    def test_errori(self):
        with pytest.raises(ValueError):
            cg255_capacita_ottimale([], 0.90, 2.70)
        with pytest.raises(ValueError):
            cg255_capacita_ottimale([100.0], 0.90, 2.70, n_punti=1)

    def test_determinismo(self):
        a = cg255_capacita_ottimale([100.0, 200.0, 300.0], 0.90, 2.70, n_punti=11)
        b = cg255_capacita_ottimale([100.0, 200.0, 300.0], 0.90, 2.70, n_punti=11)
        assert a == b


class TestCg255CurvaCosto:
    def test_base(self):
        righe = cg255_curva_costo([100.0, 200.0, 300.0], [150.0, 250.0], 0.90, 2.70)
        assert len(righe) == 2
        assert righe[0]["capacita_smc_g"] == 150.0
        assert righe[0]["costo_totale_eur_anno"] == 675.0
        assert righe[1]["penali_eur_anno"] == 135.0
        assert righe[1]["giorni_sforamento"] == 1

    def test_errori(self):
        with pytest.raises(ValueError):
            cg255_curva_costo([100.0], [], 0.90, 2.70)

    def test_determinismo(self):
        a = cg255_curva_costo([100.0, 200.0], [150.0], 0.90, 2.70)
        b = cg255_curva_costo([100.0, 200.0], [150.0], 0.90, 2.70)
        assert a == b
