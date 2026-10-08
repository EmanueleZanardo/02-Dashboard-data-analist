"""Test tab252 'Bilancio energetico di sito': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab252.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("be252_bilancio", "be252_quote", "be252_intensita",
          "be252_costo_ponderato", "be252_link_sankey")
be252_bilancio = _F["be252_bilancio"]
be252_quote = _F["be252_quote"]
be252_intensita = _F["be252_intensita"]
be252_costo_ponderato = _F["be252_costo_ponderato"]
be252_link_sankey = _F["be252_link_sankey"]

APP = Path(__file__).parent.parent / "app.py"


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab252:
    def test_tab252_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 305
        assert "⚖️ Bilancio energetico" in titoli
        assert "tab252" in dvars
        assert "tab252" in withs
        assert titoli[dvars.index("tab252")] == "⚖️ Bilancio energetico"
        assert titoli[-1] == "🎯🛡 Risk budgeting: il book rispetta i target?"
        keys = re.findall(r'key="(b252_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 10

    def test_titoli_allineati_251_252(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab251")] == "⚡ Energia reattiva & penali cosφ"
        assert titoli[dvars.index("tab252")] == "⚖️ Bilancio energetico"

    def test_helper_definiti_prima_della_ui(self):
        src = APP.read_text(encoding="utf-8")
        i_ws = src.index("if workspace ==")
        for fn in ("be252_bilancio", "be252_quote", "be252_intensita",
                   "be252_costo_ponderato", "be252_link_sankey"):
            assert src.index(f"def {fn}(") < i_ws, fn


class TestBe252Bilancio:
    def test_base(self):
        # fonti 170000, usi 165000 -> sbilancio 5000, perdite 2.94%
        r = be252_bilancio({"Rete": 120000, "FV": 30000, "Cogen": 20000},
                           {"Processo": 100000, "HVAC": 40000,
                            "Illuminazione": 15000, "Ausiliari": 10000})
        assert r["totale_fonti_kwh"] == 170000.0
        assert r["totale_usi_kwh"] == 165000.0
        assert r["sbilancio_kwh"] == 5000.0
        assert r["perdite_pct"] == pytest.approx(2.94, abs=0.01)

    def test_bilancio_chiuso(self):
        r = be252_bilancio({"Rete": 1000}, {"Uso": 1000})
        assert r["sbilancio_kwh"] == 0.0
        assert r["perdite_pct"] == 0.0

    def test_sbilancio_negativo(self):
        r = be252_bilancio({"Rete": 1000}, {"Uso": 1200})
        assert r["sbilancio_kwh"] == -200.0
        assert r["perdite_pct"] == -20.0

    def test_errori(self):
        with pytest.raises(ValueError):
            be252_bilancio({}, {"Uso": 100})
        with pytest.raises(ValueError):
            be252_bilancio({"Rete": 100}, {})
        with pytest.raises(ValueError):
            be252_bilancio({"Rete": -50}, {"Uso": 100})
        with pytest.raises(ValueError):
            be252_bilancio({"Rete": float("nan")}, {"Uso": 100})
        with pytest.raises(ValueError):
            be252_bilancio("nonsense", {"Uso": 100})


class TestBe252Quote:
    def test_base_e_ordinamento(self):
        righe = be252_quote({"Rete": 120000, "FV": 30000, "Cogen": 20000})
        assert [r["nome"] for r in righe] == ["Rete", "FV", "Cogen"]
        assert righe[0]["quota_pct"] == pytest.approx(70.59, abs=0.01)
        assert righe[1]["quota_pct"] == pytest.approx(17.65, abs=0.01)
        assert righe[2]["quota_pct"] == pytest.approx(11.76, abs=0.01)
        assert sum(r["quota_pct"] for r in righe) == pytest.approx(100.0, abs=1e-9)

    def test_singola_voce(self):
        righe = be252_quote({"Rete": 5000})
        assert righe == [{"nome": "Rete", "quota_pct": 100.0}]

    def test_errori(self):
        with pytest.raises(ValueError):
            be252_quote({})
        with pytest.raises(ValueError):
            be252_quote({"Rete": 0, "FV": 0})
        with pytest.raises(ValueError):
            be252_quote({"Rete": -10})


class TestBe252Intensita:
    def test_base(self):
        # 170000 kWh / 5000 t = 34.0 kWh/t
        assert be252_intensita(170000, 5000) == 34.0

    def test_decimale(self):
        assert be252_intensita(1000, 3) == pytest.approx(333.333, abs=1e-3)

    def test_errori(self):
        with pytest.raises(ValueError):
            be252_intensita(1000, 0)
        with pytest.raises(ValueError):
            be252_intensita(1000, -5)
        with pytest.raises(ValueError):
            be252_intensita(-100, 5000)
        with pytest.raises(ValueError):
            be252_intensita(float("nan"), 5000)


class TestBe252CostoPonderato:
    def test_base(self):
        r = be252_costo_ponderato(
            {"Rete": 120000.0, "FV": 30000.0, "Cogen": 20000.0},
            {"Rete": 0.28, "FV": 0.09, "Cogen": 0.16})
        # 33600 + 2700 + 3200 = 39500 su 170000 -> 0.2324
        assert r["costo_totale_eur"] == pytest.approx(39500.0, abs=0.01)
        assert r["costo_medio_eur_kwh"] == pytest.approx(0.2324, abs=1e-4)
        assert r["righe"][0]["fonte"] == "Rete"  # ordinato per costo desc
        assert r["righe"][0]["quota_costo_pct"] == pytest.approx(85.06, abs=0.01)
        assert sum(x["quota_costo_pct"] for x in r["righe"]) > 0

    def test_costo_zero(self):
        r = be252_costo_ponderato({"FV": 1000.0}, {"FV": 0.0})
        assert r["costo_totale_eur"] == 0.0
        assert r["costo_medio_eur_kwh"] == 0.0

    def test_errori(self):
        with pytest.raises(ValueError):
            be252_costo_ponderato({"Rete": 100.0}, {"FV": 0.09})  # chiave mancante
        with pytest.raises(ValueError):
            be252_costo_ponderato({"Rete": 100.0}, {"Rete": -0.01})
        with pytest.raises(ValueError):
            be252_costo_ponderato({"Rete": float("nan")}, {"Rete": 0.1})


class TestBe252LinkSankey:
    def test_nodi_e_link(self):
        sk = be252_link_sankey({"Rete": 1000.0, "FV": 500.0},
                               {"Processo": 1200.0, "HVAC": 200.0})
        # sbilancio 100 -> nodo perdite presente
        assert "Perdite / errori di misura" in sk["labels"]
        assert len(sk["labels"]) == 5
        assert len(sk["source"]) == len(sk["target"]) == len(sk["value"])
        # somma link verso usi = totale usi (1400), verso perdite = 100
        idx_perd = sk["labels"].index("Perdite / errori di misura")
        tot_usi = sum(v for s, t, v in zip(sk["source"], sk["target"], sk["value"])
                      if t != idx_perd)
        tot_perd = sum(v for s, t, v in zip(sk["source"], sk["target"], sk["value"])
                       if t == idx_perd)
        assert tot_usi == pytest.approx(1400.0, abs=1.0)
        assert tot_perd == pytest.approx(100.0, abs=1.0)

    def test_bilancio_chiuso_senza_nodo_perdite(self):
        sk = be252_link_sankey({"Rete": 1000.0}, {"Uso": 1000.0})
        assert "Perdite / errori di misura" not in sk["labels"]
        assert sk["labels"] == ["Rete", "Uso"]
        assert sk["value"] == [1000.0]

    def test_sbilancio_negativo_nodo_deficit(self):
        # fonti 1000 < usi 1200 -> deficit 200 come sorgente
        sk = be252_link_sankey({"Rete": 1000.0}, {"Uso": 1200.0})
        assert "Deficit (usi oltre le fonti)" in sk["labels"]
        idx_def = sk["labels"].index("Deficit (usi oltre le fonti)")
        idx_uso = sk["labels"].index("Uso")
        tot_in_uso = sum(v for s, t, v in zip(sk["source"], sk["target"], sk["value"])
                         if t == idx_uso)
        assert tot_in_uso == pytest.approx(1200.0, abs=1.0)
        tot_da_def = sum(v for s, t, v in zip(sk["source"], sk["target"], sk["value"])
                         if s == idx_def)
        assert tot_da_def == pytest.approx(200.0, abs=1.0)

    def test_errori(self):
        with pytest.raises(ValueError):
            be252_link_sankey({}, {"Uso": 100.0})
