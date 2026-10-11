"""Test tab247 'Voltura e subentro': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab247.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("d247_costo_pratica", "d247_confronto", "d247_sintesi")
d247_costo_pratica = _F["d247_costo_pratica"]
d247_confronto = _F["d247_confronto"]
d247_sintesi = _F["d247_sintesi"]

APP = Path(__file__).parent.parent / "app.py"


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab247:
    def test_tab247_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 373
        assert "🔄 Voltura e subentro" in titoli
        assert "tab247" in dvars
        assert "tab247" in withs
        assert titoli[dvars.index("tab247")] == "🔄 Voltura e subentro"
        keys = re.findall(r'key="(t247_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_246_247(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab246")] == "🛡️ Deposito cauzionale"
        assert titoli[dvars.index("tab247")] == "🔄 Voltura e subentro"


class TestD247CostoPratica:
    def test_voltura_valore_noto(self):
        # 23 € corrispettivo + 22% IVA + 16 € bollo = 44,06 €
        r = d247_costo_pratica(23.0, 22.0, 16.0)
        assert r == {"imponibile": 23.0, "iva": 5.06, "bollo": 16.0, "totale": 44.06}

    def test_subentro_con_riattivazione(self):
        # +30 € onere riattivazione (IVA applicata): 53 imponibile, 11,66 IVA, 80,66 totale
        r = d247_costo_pratica(23.0, 22.0, 16.0, 0.0, 30.0)
        assert r["imponibile"] == 53.0
        assert r["iva"] == pytest.approx(11.66)
        assert r["totale"] == pytest.approx(80.66)

    def test_senza_bollo(self):
        r = d247_costo_pratica(23.0, 22.0, 0.0)
        assert r["totale"] == pytest.approx(28.06)

    def test_contributo_distributore_zero_default(self):
        r = d247_costo_pratica(23.0, 0.0)
        assert r["totale"] == 23.0

    def test_errori(self):
        with pytest.raises(ValueError):
            d247_costo_pratica(-1.0, 22.0)
        with pytest.raises(ValueError):
            d247_costo_pratica(23.0, 101.0)
        with pytest.raises(ValueError):
            d247_costo_pratica(23.0, 22.0, 16.0, 0.0, -5.0)


class TestD247Confronto:
    def test_delta_e_rapporto(self):
        c = d247_confronto(44.06, 80.66)
        assert c["delta"] == pytest.approx(36.60)
        assert c["rapporto"] == pytest.approx(80.66 / 44.06, rel=1e-3)

    def test_uguali(self):
        c = d247_confronto(44.06, 44.06)
        assert c["delta"] == 0.0 and c["rapporto"] == 1.0


class TestD247Sintesi:
    def test_valori_noti_con_deposito(self):
        s = d247_sintesi(23.0, 22.0, 16.0, 30.0, 100.0)
        assert s["voltura"]["totale"] == 44.06
        assert s["subentro"]["totale"] == pytest.approx(80.66)
        assert s["esborso_voltura"] == pytest.approx(144.06)
        assert s["esborso_subentro"] == pytest.approx(180.66)
        assert s["delta"] == pytest.approx(36.60)
        assert s["deposito"] == 100.0

    def test_deposito_negativo_errore(self):
        with pytest.raises(ValueError):
            d247_sintesi(23.0, 22.0, 16.0, 0.0, -10.0)
