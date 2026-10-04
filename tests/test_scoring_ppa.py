"""Test tab210 'Scoring offerte PPA': helper calcola_scoring_ppa.

Stile pytest (vedi docs/AGGIUNGERE_TAB.md): la funzione viene estratta da
app.py via AST senza avviare Streamlit.
"""

from appfuncs import load

_F = load("calcola_scoring_ppa")
calcola_scoring_ppa = _F["calcola_scoring_ppa"]

OFFERTE = [
    {"nome": "A", "prezzo": 70.0, "durata": 10.0,
     "profilo": 80.0, "floor": True},
    {"nome": "B", "prezzo": 65.0, "durata": 7.0,
     "profilo": 60.0, "floor": False},
]
PESI = {"prezzo": 40.0, "durata": 25.0, "profilo": 20.0, "floor": 15.0}


class TestScoringPpa:
    def test_caso_a_mano(self):
        # pesi_norm = 0.40 / 0.25 / 0.20 / 0.15
        # prezzo: min=65 -> A=0.0, B=100.0
        # durata: max=10 -> A=100.0, B=0.0
        # profilo: A=80.0, B=60.0 ; floor: A=100.0, B=0.0
        # A: 0.40*0 + 0.25*100 + 0.20*80 + 0.15*100 = 56.0
        # B: 0.40*100 + 0.25*0 + 0.20*60 + 0.15*0 = 52.0
        r = calcola_scoring_ppa(OFFERTE, PESI)
        assert r["errore"] is None and r["valido"] is True
        assert r["classifica"] == ["A", "B"]
        df = r["df"]
        assert list(df.columns) == [
            "Offerta", "Prezzo", "Durata", "Profilo", "Floor", "Score"]
        score_a = df.loc[df["Offerta"] == "A", "Score"].iloc[0]
        score_b = df.loc[df["Offerta"] == "B", "Score"].iloc[0]
        assert score_a == 56.0
        assert score_b == 52.0
        assert abs(r["pesi_norm"]["prezzo"] - 0.40) < 1e-12
        assert abs(sum(r["pesi_norm"].values()) - 1.0) < 1e-12
        # df_criteri: score normalizzati per criterio
        dc = r["df_criteri"]
        assert dc.loc[dc["Offerta"] == "A", "Prezzo"].iloc[0] == 0.0
        assert dc.loc[dc["Offerta"] == "B", "Durata"].iloc[0] == 0.0
        assert dc.loc[dc["Offerta"] == "A", "Floor"].iloc[0] == 100.0

    def test_offerte_vuote(self):
        r = calcola_scoring_ppa([], PESI)
        assert r["valido"] is False and r["errore"]

    def test_pesi_non_validi(self):
        assert calcola_scoring_ppa(OFFERTE, None)["valido"] is False
        assert calcola_scoring_ppa(OFFERTE, "pesi")["valido"] is False
        zero = {"prezzo": 0, "durata": 0, "profilo": 0, "floor": 0}
        assert calcola_scoring_ppa(OFFERTE, zero)["valido"] is False
        bad = dict(PESI, prezzo="x")
        assert calcola_scoring_ppa(OFFERTE, bad)["valido"] is False

    def test_valori_non_numerici(self):
        bad = [{"nome": "A", "prezzo": "x", "durata": 10.0,
                "profilo": 80.0, "floor": True}]
        assert calcola_scoring_ppa(bad, PESI)["valido"] is False
        nan = [{"nome": "A", "prezzo": 70.0, "durata": 10.0,
                "profilo": float("nan"), "floor": True}]
        assert calcola_scoring_ppa(nan, PESI)["valido"] is False
        no_nome = [{"nome": " ", "prezzo": 70.0, "durata": 10.0,
                    "profilo": 80.0, "floor": True}]
        assert calcola_scoring_ppa(no_nome, PESI)["valido"] is False

    def test_max_uguale_min(self):
        # prezzo identico per tutti -> 100.0 a tutti sul criterio prezzo
        off = [
            {"nome": "A", "prezzo": 70.0, "durata": 10.0,
             "profilo": 80.0, "floor": True},
            {"nome": "B", "prezzo": 70.0, "durata": 7.0,
             "profilo": 60.0, "floor": False},
        ]
        r = calcola_scoring_ppa(off, PESI)
        assert r["valido"] is True
        assert (r["df_criteri"]["Prezzo"] == 100.0).all()

    def test_offerta_singola(self):
        # prezzo/durata/floor -> 100 (max==min, floor True); profilo = 80
        # diretto -> score = 0.40*100 + 0.25*100 + 0.20*80 + 0.15*100 = 96.0
        r = calcola_scoring_ppa(OFFERTE[:1], PESI)
        assert r["valido"] is True
        assert r["classifica"] == ["A"]
        assert r["df"]["Score"].iloc[0] == 96.0

    def test_determinismo(self):
        a = calcola_scoring_ppa(OFFERTE, PESI)
        b = calcola_scoring_ppa(OFFERTE, PESI)
        assert a["classifica"] == b["classifica"]
        assert a["df"].equals(b["df"])
        assert a["df_criteri"].equals(b["df_criteri"])
        assert a["pesi_norm"] == b["pesi_norm"]
