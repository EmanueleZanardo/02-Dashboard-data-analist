"""Test tab245 'Conguaglio a rate': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab245.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("r245_rata_francese", "r245_piano", "r245_taeg", "r245_sintesi")
r245_rata_francese = _F["r245_rata_francese"]
r245_piano = _F["r245_piano"]
r245_taeg = _F["r245_taeg"]
r245_sintesi = _F["r245_sintesi"]

APP = Path(__file__).parent.parent / "app.py"


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab245:
    def test_tab245_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 299
        assert "💳 Conguaglio a rate" in titoli
        assert "tab245" in dvars
        assert "tab245" in withs
        assert titoli[dvars.index("tab245")] == "💳 Conguaglio a rate"
        keys = re.findall(r'key="(t245_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_244_245(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab244")] == "🧾 Acconto & conguaglio"
        assert titoli[dvars.index("tab245")] == "💳 Conguaglio a rate"


class TestR245Rata:
    def test_tasso_zero(self):
        assert r245_rata_francese(1200.0, 0.0, 12) == pytest.approx(100.0)

    def test_francese_nota(self):
        # 1200 €, TAN 12% (i=1%/mese), 12 rate -> ~106.62 €/mese
        assert r245_rata_francese(1200.0, 12.0, 12) == pytest.approx(106.6185, rel=1e-4)

    def test_rata_unica(self):
        assert r245_rata_francese(1500.0, 6.0, 1) == pytest.approx(1507.4627, rel=1e-4)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            r245_rata_francese(0.0, 5.0, 12)
        with pytest.raises(ValueError):
            r245_rata_francese(1000.0, -1.0, 12)
        with pytest.raises(ValueError):
            r245_rata_francese(1000.0, 5.0, 0)
        with pytest.raises(ValueError):
            r245_rata_francese(1000.0, 5.0, 61)


class TestR245Piano:
    def test_lunghezza_e_azzera_residuo(self):
        p = r245_piano(1500.0, 4.5, 6)
        assert len(p) == 6
        assert p[-1]["residuo"] == pytest.approx(0.0, abs=0.01)
        assert all(r["residuo"] >= 0 for r in p)

    def test_quote_capitale_sommano(self):
        p = r245_piano(1500.0, 4.5, 6)
        assert sum(r["quota_capitale"] for r in p) == pytest.approx(1500.0, abs=0.05)

    def test_costi_solo_prima_rata(self):
        p = r245_piano(1500.0, 4.5, 6, costi_fissi=25.0)
        assert p[0]["costi"] == 25.0
        assert all(r["costi"] == 0.0 for r in p[1:])

    def test_interessi_decrescenti(self):
        p = r245_piano(1500.0, 12.0, 12)
        qi = [r["quota_interessi"] for r in p]
        assert qi[0] > qi[-1] > 0

    def test_costi_negativi_errore(self):
        with pytest.raises(ValueError):
            r245_piano(1500.0, 4.5, 6, costi_fissi=-1.0)


class TestR245Taeg:
    def test_taeg_senza_costi_uguale_tan_effettivo(self):
        # TAN 12% nominale mensile -> TAEG (1.01^12-1) = 12.6825%
        pag = [r245_rata_francese(1200.0, 12.0, 12)] * 12
        assert r245_taeg(1200.0, pag) == pytest.approx(12.6825, rel=1e-3)

    def test_taeg_zero(self):
        assert r245_taeg(1200.0, [100.0] * 12) == 0.0

    def test_taeg_cresce_con_costi(self):
        pag = [r245_rata_francese(1200.0, 12.0, 12)] * 12
        base = r245_taeg(1200.0, pag)
        con_costi = r245_taeg(1200.0, pag, costi_iniziali=30.0)
        assert con_costi > base

    def test_invalidi(self):
        with pytest.raises(ValueError):
            r245_taeg(0.0, [100.0] * 12)
        with pytest.raises(ValueError):
            r245_taeg(1200.0, [])


class TestR245Sintesi:
    def test_kpi_coerenti(self):
        s = r245_sintesi(1500.0, 4.5, 6, costi_fissi=25.0, sconto_pronta_cassa_pct=2.0)
        assert s["n_rate"] == 6
        assert s["totale_versato"] == pytest.approx(
            s["pagamento_immediato"] + s["delta_vs_immediato"], abs=0.05)
        assert s["costo_finanziario"] == pytest.approx(
            s["interessi_totali"] + 25.0, abs=0.05)
        assert s["taeg_pct"] > 4.5  # TAN 4.5% + costi -> TAEG superiore
        assert s["pagamento_immediato"] == pytest.approx(1470.0)
        assert len(s["piano"]) == 6

    def test_sconto_zero(self):
        s = r245_sintesi(1500.0, 0.0, 6, sconto_pronta_cassa_pct=0.0)
        assert s["pagamento_immediato"] == 1500.0
        assert s["taeg_pct"] == 0.0
        assert s["delta_vs_immediato"] == pytest.approx(0.0, abs=0.05)

    def test_sconto_invalido(self):
        with pytest.raises(ValueError):
            r245_sintesi(1500.0, 4.5, 6, sconto_pronta_cassa_pct=100.0)
