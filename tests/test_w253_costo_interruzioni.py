"""Test tab253 'Costo interruzioni (VoLL)': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab253.
"""

import math
import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("ci253_costo_evento", "ci253_costo_atteso", "ci253_indici",
          "ci253_backup", "ci253_matrice")
ci253_costo_evento = _F["ci253_costo_evento"]
ci253_costo_atteso = _F["ci253_costo_atteso"]
ci253_indici = _F["ci253_indici"]
ci253_backup = _F["ci253_backup"]
ci253_matrice = _F["ci253_matrice"]

APP = Path(__file__).parent.parent / "app.py"


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab253:
    def test_tab253_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 324
        assert "🌑 Costo interruzioni (VoLL)" in titoli
        assert "tab253" in dvars
        assert "tab253" in withs
        assert titoli[dvars.index("tab253")] == "🌑 Costo interruzioni (VoLL)"
        assert titoli[-1] == "Ω📊 Omega ratio: oltre Sharpe e Sortino"
        keys = re.findall(r'key="(ci253_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 10

    def test_titoli_allineati_252_253(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab252")] == "⚖️ Bilancio energetico"
        assert titoli[dvars.index("tab253")] == "🌑 Costo interruzioni (VoLL)"

    def test_helper_definiti_prima_della_ui(self):
        src = APP.read_text(encoding="utf-8")
        i_ws = src.index("if workspace ==")
        for fn in ("ci253_costo_evento", "ci253_costo_atteso", "ci253_indici",
                   "ci253_backup", "ci253_matrice"):
            assert src.index(f"def {fn}(") < i_ws, fn


class TestCi253CostoEvento:
    def test_base(self):
        r = ci253_costo_evento(12.0, 500.0, 2.0)
        assert r["ens_kwh"] == 1000.0
        assert r["costo_eur"] == 12000.0
        assert r["voll_eur_kwh"] == 12.0

    def test_frazioni(self):
        r = ci253_costo_evento(8.5, 200.0, 0.5)
        assert r["ens_kwh"] == 100.0
        assert r["costo_eur"] == 850.0

    def test_voll_zero(self):
        r = ci253_costo_evento(0.0, 500.0, 2.0)
        assert r["costo_eur"] == 0.0
        assert r["ens_kwh"] == 1000.0

    def test_errori(self):
        with pytest.raises(ValueError):
            ci253_costo_evento(-1.0, 500.0, 2.0)
        with pytest.raises(ValueError):
            ci253_costo_evento(12.0, -5.0, 2.0)
        with pytest.raises(ValueError):
            ci253_costo_evento(12.0, 500.0, -1.0)
        with pytest.raises(ValueError):
            ci253_costo_evento(math.nan, 500.0, 2.0)


class TestCi253CostoAtteso:
    def test_base(self):
        r = ci253_costo_atteso(12.0, 500.0, 2.0, 3.0)
        assert r["costo_evento_eur"] == 12000.0
        assert r["ens_evento_kwh"] == 1000.0
        assert r["eventi_anno"] == 3.0
        assert r["ens_annua_kwh"] == 3000.0
        assert r["costo_atteso_annuo_eur"] == 36000.0

    def test_zero_eventi(self):
        r = ci253_costo_atteso(12.0, 500.0, 2.0, 0.0)
        assert r["costo_atteso_annuo_eur"] == 0.0

    def test_errori(self):
        with pytest.raises(ValueError):
            ci253_costo_atteso(12.0, 500.0, 2.0, -1.0)
        with pytest.raises(ValueError):
            ci253_costo_atteso(12.0, 500.0, math.nan, 2.0)


class TestCi253Indici:
    def test_base(self):
        r = ci253_indici([0.5, 2.0, 1.5])
        assert r["eventi_anno"] == 3
        assert r["saidi_ore_anno"] == 4.0
        assert r["caidi_ore_evento"] == 1.333
        assert r["disponibilita_pct"] == 99.9543

    def test_singolo_evento(self):
        r = ci253_indici([1.0])
        assert r["saidi_ore_anno"] == 1.0
        assert r["caidi_ore_evento"] == 1.0
        assert r["disponibilita_pct"] == 99.9886

    def test_errori(self):
        with pytest.raises(ValueError):
            ci253_indici([])
        with pytest.raises(ValueError):
            ci253_indici([1.0, -0.5])
        with pytest.raises(ValueError):
            ci253_indici([math.nan])


class TestCi253Backup:
    def test_conveniente(self):
        r = ci253_backup(36000.0, 90.0, 50000.0, 2000.0)
        assert r["costo_residuo_eur"] == 3600.0
        assert r["costo_con_backup_eur"] == 5600.0
        assert r["risparmio_annuo_eur"] == 30400.0
        assert r["payback_mesi"] == 19.7
        assert r["conviene"] is True

    def test_non_conviene_quota_zero(self):
        r = ci253_backup(36000.0, 0.0, 50000.0, 2000.0)
        assert r["costo_con_backup_eur"] == 38000.0
        assert r["risparmio_annuo_eur"] == -2000.0
        assert r["payback_mesi"] is None
        assert r["conviene"] is False

    def test_payback_lungo(self):
        r = ci253_backup(10000.0, 50.0, 100000.0, 1000.0)
        assert r["payback_mesi"] == 300.0
        assert r["conviene"] is False

    def test_copertura_totale(self):
        r = ci253_backup(36000.0, 100.0, 50000.0, 2000.0)
        assert r["costo_residuo_eur"] == 0.0
        assert r["risparmio_annuo_eur"] == 34000.0
        assert r["payback_mesi"] == 17.6

    def test_errori(self):
        with pytest.raises(ValueError):
            ci253_backup(36000.0, 101.0, 50000.0, 2000.0)
        with pytest.raises(ValueError):
            ci253_backup(36000.0, 90.0, -1.0, 2000.0)
        with pytest.raises(ValueError):
            ci253_backup(-5.0, 90.0, 50000.0, 2000.0)


class TestCi253Matrice:
    def test_base(self):
        righe = ci253_matrice([1.0, 2.0], [1.0, 3.0], 10.0, 100.0)
        assert len(righe) == 4
        mappa = {(r["durata_ore"], r["eventi_anno"]): r["costo_atteso_annuo_eur"]
                 for r in righe}
        assert mappa[(1.0, 1.0)] == 1000.0
        assert mappa[(1.0, 3.0)] == 3000.0
        assert mappa[(2.0, 1.0)] == 2000.0
        assert mappa[(2.0, 3.0)] == 6000.0

    def test_errori(self):
        with pytest.raises(ValueError):
            ci253_matrice([], [1.0], 10.0, 100.0)
        with pytest.raises(ValueError):
            ci253_matrice([1.0], [1.0], -10.0, 100.0)

    def test_determinismo(self):
        a = ci253_matrice([0.5, 8.0], [2.0, 5.0], 12.0, 500.0)
        b = ci253_matrice([0.5, 8.0], [2.0, 5.0], 12.0, 500.0)
        assert a == b
