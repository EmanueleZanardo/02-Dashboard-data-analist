"""Test tab227 (stile pytest): Duck curve / carico netto residuo.

Funzione pura calcola_duck_curve estratta da app.py via AST (tests/appfuncs).
Stile QA: numeri calcolati a mano + validazione input + determinismo +
registry tab227.
"""

import re
from pathlib import Path

from appfuncs import load

_F = load("calcola_duck_curve")
calcola_duck_curve = _F["calcola_duck_curve"]


# ------------------------------------------------------- numeri a mano
class TestNumeriAMano:
    def test_senza_rinnovabili(self):
        # netto == profilo carico: min 0.60*1000=600 alle ore 0-4 (argmin -> 0)
        # pancia = 1000-600 = 400, indice = 0.40
        # rampa serale max: 17->18 = (0.93-0.85)*1000 = 80 MW/h
        # rampa mattutina max in discesa: 9->10 = (0.88-0.80)*1000 = 80 MW/h
        r = calcola_duck_curve(1000.0, 0.0, 0.0, "estate", 0.35)
        assert r["valido"] and r["errore"] is None
        assert r["carico_netto_min_MW"] == 600.0
        assert r["ora_minimo"] == 0
        assert r["profondita_pancia_MW"] == 400.0
        assert r["indice_duck"] == 0.40
        assert r["rampa_serale_max_MW_h"] == 80.0
        assert r["rampa_mattutina_max_MW_h"] == 80.0
        assert r["ore_overgeneration"] == 0

    def test_solare_forma_pancia(self):
        # estate: sole 6-20, cf picco 0.90; h=13 -> sin(pi/2)=1 -> 500*0.9=450
        # netto(13) = 0.80*1000 - 450 = 350 (minimo); pancia = 650, idx 0.65
        r = calcola_duck_curve(1000.0, 500.0, 0.0, "estate")
        assert r["valido"]
        assert r["carico_netto_min_MW"] == 350.0
        assert r["ora_minimo"] == 13
        assert r["profondita_pancia_MW"] == 650.0
        assert r["indice_duck"] == 0.65
        assert r["ore_overgeneration"] == 0

    def test_overgeneration(self):
        # FV 3000 estate: netto<0 <=> sin(pi(h-6)/14) > carico/2.7
        # carico<=0.88 tra le 6 e le 16 -> h in {8..18} = 11 ore
        r = calcola_duck_curve(1000.0, 3000.0, 0.0, "estate")
        assert r["valido"]
        assert r["carico_netto_min_MW"] == -1900.0
        assert r["ora_minimo"] == 13
        assert r["ore_overgeneration"] == 11

    def test_inverno_pancia_ridotta(self):
        # inverno: sole 8-16, cf 0.60; h=12 -> 500*0.6*1 = 300
        # netto(12) = 800-300 = 500 (minimo)
        r = calcola_duck_curve(1000.0, 500.0, 0.0, "inverno")
        assert r["valido"]
        assert r["carico_netto_min_MW"] == 500.0
        assert r["ora_minimo"] == 12
        assert r["stagione_usata"] == "inverno"

    def test_eolico_piatto(self):
        # eolico 1000 MW a fattore 0.35 = 350 MW costanti -> min netto 600-350=250
        r = calcola_duck_curve(1000.0, 0.0, 1000.0, "estate", 0.35)
        assert r["valido"]
        assert r["carico_netto_min_MW"] == 250.0
        df = r["df_orario"]
        assert (df["eolico_MW"] == 350.0).all()
        assert len(df) == 24
        assert list(df.columns) == ["ora", "carico_MW", "solare_MW",
                                    "eolico_MW", "carico_netto_MW"]


# ------------------------------------------------------- validazione
class TestValidazione:
    def test_picco_non_positivo(self):
        for bad in (0.0, -5.0):
            r = calcola_duck_curve(bad)
            assert not r["valido"] and r["errore"] is not None

    def test_capacita_negative(self):
        assert not calcola_duck_curve(1000.0, -1.0)["valido"]
        assert not calcola_duck_curve(1000.0, 0.0, -1.0)["valido"]

    def test_fattore_eolico_fuori_range(self):
        assert not calcola_duck_curve(1000.0, 0.0, 100.0, "estate",
                                      1.5)["valido"]

    def test_stagione_sconosciuta(self):
        r = calcola_duck_curve(1000.0, 500.0, 0.0, "primavera")
        assert not r["valido"]

    def test_input_non_numerici(self):
        r = calcola_duck_curve("tanto")
        assert not r["valido"]


# ------------------------------------------------------- determinismo
class TestDeterminismo:
    def test_stesso_input_stesso_output(self):
        kw = dict(capacita_fv_mw=3000.0, capacita_eolico_mw=1000.0,
                  stagione="estate", fattore_eolico=0.35)
        r1 = calcola_duck_curve(5000.0, **kw)
        r2 = calcola_duck_curve(5000.0, **kw)
        assert r1["carico_netto_min_MW"] == r2["carico_netto_min_MW"]
        assert r1["rampa_serale_max_MW_h"] == r2["rampa_serale_max_MW_h"]
        assert (r1["df_orario"]["carico_netto_MW"]
                == r2["df_orario"]["carico_netto_MW"]).all()


# ------------------------------------------------------- registry
class TestRegistryTab227:
    def test_tab227_dichiarata(self):
        src = Path(__file__).parent.parent.joinpath("app.py").read_text(
            encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 365
        assert titoli[-1] == "Kelly con incertezza: haircut bayesiano sulla p stimata"
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab227" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab227" in withs
        assert len(withs) == len(dvars) == 365
        keys = re.findall(r'key="(ai227_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 6
