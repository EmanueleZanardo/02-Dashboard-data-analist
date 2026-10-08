"""Test tab256 'Perdite di rete': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab256.
"""

import math
import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("_pr256_num", "pr256_perdite_standard", "pr256_energia_immessa",
          "pr256_parsa_misure", "pr256_sintesi", "pr256_confronto_livelli",
          "pr256_risparmio_cambio_livello", "pr256_curva_perdite")
pr256_perdite_standard = _F["pr256_perdite_standard"]
pr256_energia_immessa = _F["pr256_energia_immessa"]
pr256_parsa_misure = _F["pr256_parsa_misure"]
pr256_sintesi = _F["pr256_sintesi"]
pr256_confronto_livelli = _F["pr256_confronto_livelli"]
pr256_risparmio_cambio_livello = _F["pr256_risparmio_cambio_livello"]
pr256_curva_perdite = _F["pr256_curva_perdite"]

APP = Path(__file__).parent.parent / "app.py"


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab256:
    def test_tab256_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 316
        assert "⚡ Perdite di rete" in titoli
        assert "tab256" in dvars
        assert "tab256" in withs
        assert titoli[dvars.index("tab256")] == "⚡ Perdite di rete"
        assert titoli[-1] == "🌊📉 POT-GPD: il VaR dalla coda paretiana oltre soglia"
        keys = re.findall(r'key="(pr256_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 7

    def test_titoli_allineati_255_256(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab255")] == "⛽ Capacità gas giornaliera"
        assert titoli[dvars.index("tab256")] == "⚡ Perdite di rete"

    def test_helper_definiti_prima_della_ui(self):
        src = APP.read_text(encoding="utf-8")
        i_ws = src.index("if workspace ==")
        for fn in ("pr256_perdite_standard", "pr256_energia_immessa",
                   "pr256_parsa_misure", "pr256_sintesi", "pr256_confronto_livelli",
                   "pr256_risparmio_cambio_livello", "pr256_curva_perdite"):
            assert src.index(f"def {fn}(") < i_ws, fn


class TestPr256PerditeStandard:
    def test_valori(self):
        std = pr256_perdite_standard()
        assert set(std) == {"AT", "MT", "BT"}
        assert std["AT"] < std["MT"] < std["BT"]
        assert std["BT"] == 10.4


class TestPr256EnergiaImmessa:
    def test_base(self):
        r = pr256_energia_immessa(900.0, 10.0)
        assert r["energia_immessa_kwh"] == pytest.approx(1000.0)
        assert r["perdite_kwh"] == pytest.approx(100.0)
        assert r["perdite_pct_verificata"] == pytest.approx(10.0)

    def test_zero_perdite(self):
        r = pr256_energia_immessa(500.0, 0.0)
        assert r["energia_immessa_kwh"] == 500.0
        assert r["perdite_kwh"] == 0.0

    def test_errori(self):
        with pytest.raises(ValueError):
            pr256_energia_immessa(-1.0, 10.0)
        with pytest.raises(ValueError):
            pr256_energia_immessa(900.0, 100.0)
        with pytest.raises(ValueError):
            pr256_energia_immessa(900.0, -0.5)
        with pytest.raises(ValueError):
            pr256_energia_immessa(math.nan, 10.0)


class TestPr256ParsaMisure:
    def test_base_virgola(self):
        righe = pr256_parsa_misure("42100,46800\n43800,48700")
        assert righe == [{"prelevata_kwh": 42100.0, "immessa_kwh": 46800.0},
                         {"prelevata_kwh": 43800.0, "immessa_kwh": 48700.0}]

    def test_punto_e_virgola_e_decimale(self):
        righe = pr256_parsa_misure("45210,5;49800\n\n50000;55600,25")
        assert righe[0] == {"prelevata_kwh": 45210.5, "immessa_kwh": 49800.0}
        assert righe[1] == {"prelevata_kwh": 50000.0, "immessa_kwh": 55600.25}

    def test_errori(self):
        with pytest.raises(ValueError):
            pr256_parsa_misure("")
        with pytest.raises(ValueError):
            pr256_parsa_misure("   \n  ")
        with pytest.raises(ValueError) as exc:
            pr256_parsa_misure("42100,46800\nabc\n43800,48700")
        assert "riga 2" in str(exc.value)
        with pytest.raises(ValueError):
            pr256_parsa_misure("50000,40000")
        with pytest.raises(ValueError):
            pr256_parsa_misure("-100,50000")
        with pytest.raises(ValueError):
            pr256_parsa_misure("42100")


class TestPr256Sintesi:
    def test_base(self):
        misure = [{"prelevata_kwh": 900.0, "immessa_kwh": 1000.0},
                  {"prelevata_kwh": 1800.0, "immessa_kwh": 2000.0}]
        r = pr256_sintesi(misure, 10.0, 140.0)
        assert r["mesi"] == 2
        assert r["prelievo_tot_kwh"] == 2700.0
        assert r["perdite_eff_kwh"] == pytest.approx(300.0)
        assert r["perdite_eff_pct"] == pytest.approx(10.0)
        assert r["perdite_std_pct"] == 10.0
        assert r["scostamento_kwh"] == pytest.approx(0.0, abs=1e-6)
        assert r["costo_perdite_eff_eur"] == pytest.approx(42.0)
        assert len(r["per_mese"]) == 2
        assert r["per_mese"][0]["perdite_eff_pct"] == 10.0

    def test_scostamento_positivo(self):
        misure = [{"prelevata_kwh": 900.0, "immessa_kwh": 1100.0}]
        r = pr256_sintesi(misure, 5.0, 100.0)
        assert r["scostamento_kwh"] > 0
        assert r["costo_scostamento_eur"] > 0

    def test_errori(self):
        with pytest.raises(ValueError):
            pr256_sintesi([], 10.0, 140.0)
        with pytest.raises(ValueError):
            pr256_sintesi([{"prelevata_kwh": 1.0, "immessa_kwh": 2.0}], 10.0, -5.0)
        with pytest.raises(ValueError):
            pr256_sintesi([{"prelevata_kwh": 5.0, "immessa_kwh": 4.0}], 10.0, 140.0)

    def test_determinismo(self):
        misure = [{"prelevata_kwh": 900.0, "immessa_kwh": 1000.0}]
        a = pr256_sintesi(misure, 10.0, 140.0)
        b = pr256_sintesi(misure, 10.0, 140.0)
        assert a == b


class TestPr256ConfrontoLivelli:
    def test_base(self):
        righe = pr256_confronto_livelli(1_000_000.0, 140.0)
        assert [r["livello"] for r in righe] == ["AT", "MT", "BT"]
        costi = [r["costo_perdite_eur_anno"] for r in righe]
        assert costi[0] < costi[1] < costi[2]
        assert righe[2]["perdite_kwh"] == pytest.approx(
            1_000_000.0 / 0.896 - 1_000_000.0, rel=1e-9)

    def test_standard_custom(self):
        righe = pr256_confronto_livelli(1000.0, 100.0, {"X": 5.0})
        assert len(righe) == 1 and righe[0]["livello"] == "X"

    def test_errori(self):
        with pytest.raises(ValueError):
            pr256_confronto_livelli(-1.0, 140.0)
        with pytest.raises(ValueError):
            pr256_confronto_livelli(1000.0, 140.0, {})


class TestPr256RisparmioCambioLivello:
    def test_bt_mt(self):
        r = pr256_risparmio_cambio_livello(1_000_000.0, 140.0, 10.4, 5.1)
        assert r["risparmio_kwh_anno"] > 0
        assert r["risparmio_eur_anno"] == pytest.approx(
            r["risparmio_kwh_anno"] / 1000.0 * 140.0)

    def test_stesso_livello(self):
        r = pr256_risparmio_cambio_livello(1_000_000.0, 140.0, 5.1, 5.1)
        assert r["risparmio_kwh_anno"] == 0.0
        assert r["risparmio_eur_anno"] == 0.0

    def test_peggioramento_negativo(self):
        r = pr256_risparmio_cambio_livello(1_000_000.0, 140.0, 5.1, 10.4)
        assert r["risparmio_eur_anno"] < 0

    def test_errori(self):
        with pytest.raises(ValueError):
            pr256_risparmio_cambio_livello(1000.0, 140.0, 100.0, 5.0)


class TestPr256CurvaPerdite:
    def test_base(self):
        righe = pr256_curva_perdite(1_000_000.0, 140.0, [0.0, 5.0, 10.0])
        assert len(righe) == 3
        assert righe[0]["perdite_kwh_anno"] == 0.0
        costi = [r["costo_perdite_eur_anno"] for r in righe]
        assert costi[0] < costi[1] < costi[2]

    def test_errori(self):
        with pytest.raises(ValueError):
            pr256_curva_perdite(1000.0, 140.0, [])
        with pytest.raises(ValueError):
            pr256_curva_perdite(1000.0, 140.0, [101.0])

    def test_determinismo(self):
        a = pr256_curva_perdite(1000.0, 100.0, [5.0])
        b = pr256_curva_perdite(1000.0, 100.0, [5.0])
        assert a == b
