"""Test tab250 'Capitale circolante': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab250.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("cc250_ciclo_cassa", "cc250_fabbisogno",
          "cc250_costo_finanziario", "cc250_costo_per_mwh",
          "cc250_confronto_scenari", "cc250_sensibilita")
cc250_ciclo_cassa = _F["cc250_ciclo_cassa"]
cc250_fabbisogno = _F["cc250_fabbisogno"]
cc250_costo_finanziario = _F["cc250_costo_finanziario"]
cc250_costo_per_mwh = _F["cc250_costo_per_mwh"]
cc250_confronto_scenari = _F["cc250_confronto_scenari"]
cc250_sensibilita = _F["cc250_sensibilita"]

APP = Path(__file__).parent.parent / "app.py"


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab250:
    def test_tab250_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 343
        assert "💸 Capitale circolante" in titoli
        assert "tab250" in dvars
        assert "tab250" in withs
        assert titoli[dvars.index("tab250")] == "💸 Capitale circolante"
        assert titoli[-1] == "📐 Kelly criterion: il sizing ottimale dall'edge stimato"
        keys = re.findall(r'key="(t250_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_249_250(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab249")] == "🔌 Preventivo allacciamento"
        assert titoli[dvars.index("tab250")] == "💸 Capitale circolante"

    def test_helper_definiti_prima_della_ui(self):
        src = APP.read_text(encoding="utf-8")
        i_ws = src.index("if workspace ==")
        for fn in ("cc250_ciclo_cassa", "cc250_fabbisogno",
                   "cc250_costo_finanziario", "cc250_costo_per_mwh",
                   "cc250_confronto_scenari", "cc250_sensibilita"):
            assert src.index(f"def {fn}(") < i_ws, fn


class TestCc250CicloCassa:
    def test_base(self):
        # 45 + 0 - 30 = 15 giorni
        r = cc250_ciclo_cassa(45, 30)
        assert r == {"dso_gg": 45.0, "dpo_gg": 30.0, "dio_gg": 0.0,
                     "ciclo_gg": 15.0}

    def test_negativo_finanziato_dai_fornitori(self):
        r = cc250_ciclo_cassa(20, 60, 5)
        assert r["ciclo_gg"] == -35.0

    def test_errori(self):
        with pytest.raises(ValueError):
            cc250_ciclo_cassa(-1, 30)
        with pytest.raises(ValueError):
            cc250_ciclo_cassa(45, -5)
        with pytest.raises(ValueError):
            cc250_ciclo_cassa(45, 30, -2)


class TestCc250Fabbisogno:
    def test_base(self):
        # 2_000_000 * 15 / 365 = 82191.78
        r = cc250_fabbisogno(2_000_000, 15)
        assert r["fabbisogno_medio_eur"] == pytest.approx(82191.78, abs=0.01)

    def test_ciclo_negativo(self):
        r = cc250_fabbisogno(2_000_000, -35)
        assert r["fabbisogno_medio_eur"] == pytest.approx(-191780.82, abs=0.01)

    def test_costo_zero(self):
        assert cc250_fabbisogno(0, 15)["fabbisogno_medio_eur"] == 0.0

    def test_errori(self):
        with pytest.raises(ValueError):
            cc250_fabbisogno(-100, 15)


class TestCc250CostoFinanziario:
    def test_base(self):
        # 82191.78 * 6% = 4931.51
        r = cc250_costo_finanziario(82191.78, 6.0)
        assert r["costo_annuo_eur"] == pytest.approx(4931.51, abs=0.01)

    def test_wacc_zero(self):
        assert cc250_costo_finanziario(82191.78, 0.0)["costo_annuo_eur"] == 0.0

    def test_fabbisogno_negativo_beneficio(self):
        # ciclo negativo: i fornitori finanziano -> costo negativo = beneficio
        r = cc250_costo_finanziario(-164383.56, 6.0)
        assert r["costo_annuo_eur"] == pytest.approx(-9863.01, abs=0.01)

    def test_errori(self):
        with pytest.raises(ValueError):
            cc250_costo_finanziario(1000, -1.0)
        with pytest.raises(ValueError):
            cc250_costo_finanziario(1000, 101.0)


class TestCc250CostoPerMwh:
    def test_base(self):
        # 4931.51 / 20000 = 0.247
        r = cc250_costo_per_mwh(4931.51, 20000)
        assert r["costo_per_mwh"] == pytest.approx(0.247, abs=0.001)

    def test_costo_negativo_beneficio(self):
        # beneficio da ciclo negativo -> ricarico negativo
        r = cc250_costo_per_mwh(-9863.01, 20000)
        assert r["costo_per_mwh"] == pytest.approx(-0.493, abs=0.001)

    def test_errori(self):
        with pytest.raises(ValueError):
            cc250_costo_per_mwh(100, 0)
        with pytest.raises(ValueError):
            cc250_costo_per_mwh(100, -50)


class TestCc250ConfrontoScenari:
    _SCEN = [
        {"nome": "Base", "dso": 45.0, "dpo": 30.0, "wacc_pct": 6.0},
        {"nome": "Incasso rapido", "dso": 30.0, "dpo": 30.0, "wacc_pct": 6.0},
    ]

    def test_due_scenari(self):
        righe = cc250_confronto_scenari(2_000_000, 20000, self._SCEN)
        assert len(righe) == 2
        base, rapido = righe
        assert base["ciclo_gg"] == 15.0
        assert rapido["ciclo_gg"] == 0.0
        assert rapido["fabbisogno_eur"] == 0.0
        assert rapido["costo_annuo_eur"] == 0.0
        assert rapido["costo_per_mwh"] == 0.0
        assert base["fabbisogno_eur"] == pytest.approx(82191.78, abs=0.01)
        assert base["costo_annuo_eur"] == pytest.approx(4931.51, abs=0.05)
        assert base["costo_per_mwh"] == pytest.approx(0.247, abs=0.001)

    def test_errori(self):
        with pytest.raises(ValueError):
            cc250_confronto_scenari(2_000_000, 20000, [])
        with pytest.raises(ValueError):
            cc250_confronto_scenari(-1, 20000, self._SCEN)
        with pytest.raises(ValueError):
            cc250_confronto_scenari(2_000_000, 0, self._SCEN)
        with pytest.raises(ValueError):
            cc250_confronto_scenari(2_000_000, 20000, [{"nome": "x"}])
        with pytest.raises(ValueError):
            cc250_confronto_scenari(2_000_000, 20000, "nonsense")


class TestCc250Sensibilita:
    def test_matrice(self):
        righe = cc250_sensibilita([0.0, 45.0], [2.0, 6.0], 2_000_000, 30.0,
                                  20000)
        assert len(righe) == 4
        d = {(r["dso_gg"], r["wacc_pct"]): r for r in righe}
        # DSO 0, DPO 30 -> ciclo -30 -> fabbisogno -164383.56 -> costo 2% negativo
        assert d[(0.0, 2.0)]["costo_annuo_eur"] == pytest.approx(
            -164383.56 * 0.02, abs=0.05)
        # DSO 45, WACC 6% -> 4931.51
        assert d[(45.0, 6.0)]["costo_annuo_eur"] == pytest.approx(
            4931.51, abs=0.05)
        assert d[(45.0, 6.0)]["costo_per_mwh"] == pytest.approx(
            0.247, abs=0.001)

    def test_errori(self):
        with pytest.raises(ValueError):
            cc250_sensibilita([], [6.0], 2_000_000, 30.0, 20000)
        with pytest.raises(ValueError):
            cc250_sensibilita([45.0], [], 2_000_000, 30.0, 20000)
        with pytest.raises(ValueError):
            cc250_sensibilita([-5.0], [6.0], 2_000_000, 30.0, 20000)
        with pytest.raises(ValueError):
            cc250_sensibilita([45.0], [150.0], 2_000_000, 30.0, 20000)
        with pytest.raises(ValueError):
            cc250_sensibilita([45.0], [6.0], 2_000_000, -30.0, 20000)
        with pytest.raises(ValueError):
            cc250_sensibilita([45.0], [6.0], -1, 30.0, 20000)
        with pytest.raises(ValueError):
            cc250_sensibilita([45.0], [6.0], 2_000_000, 30.0, 0)
