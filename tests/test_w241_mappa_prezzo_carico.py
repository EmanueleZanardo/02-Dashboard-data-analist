"""Test tab241 'Mappa prezzo×carico': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) con forma robusta
(i worker paralleli aggiungono tab in contemporanea) e l'allineamento
titolo-contenuto delle tab 231-241 (bug fix QA 05/10/2026: i titoli erano
disallineati dai contenuti per gli edit concorrenti sullo st.tabs).
"""

import re
from pathlib import Path

import numpy as np

from appfuncs import load

_F = load("calcola_mappa_prezzo_carico")
calcola_mappa_prezzo_carico = _F["calcola_mappa_prezzo_carico"]

APP = Path(__file__).parent.parent / "app.py"


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab241:
    def test_tab241_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) >= 231
        assert "🗺️ Mappa prezzo×carico" in titoli
        assert "tab241" in dvars
        assert "tab241" in withs
        # il titolo deve stare nella posizione della sua variabile
        assert titoli[dvars.index("tab241")] == "🗺️ Mappa prezzo×carico"
        keys = re.findall(r'key="(t241_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 10

    def test_titoli_allineati_ai_contenuti_231_241(self):
        # bug fix 05/10/2026: titoli disallineati dai with-block per edit concorrenti
        _, titoli, dvars, _ = _registry()
        attesi = {
            "tab231": "🔍 Qualità dati (gap & outlier)",
            "tab232": "🧮 Concentrazione temporale (HHI)",
            "tab234": "🎯 Score di timing",
            "tab239": "📊 Probabilità sforamento budget",
            "tab235": "🔁 Correlazione carico-prezzo",
            "tab233": "💧 Waterfall del costo",
            "tab240": "📋 Checklist gara fornitura",
            "tab238": "🌙 Baseload notturno",
            "tab241": "🗺️ Mappa prezzo×carico",
        }
        for var, tit in attesi.items():
            assert titoli[dvars.index(var)] == tit, var


class TestMappaPrezzoCarico:
    def test_caso_calcolato_a_mano(self):
        # 4 ore: prezzi [10,10,20,20] €/MWh, carichi [100,200,100,200] kW
        # costo orario € = p*c/1000 -> [1, 2, 2, 4]; bucket prezzo: P1 10-15, P2 15-20
        # bucket carico: C1 100-150, C2 150-200
        ris = calcola_mappa_prezzo_carico([10, 10, 20, 20], [100, 200, 100, 200],
                                          n_prezzo=2, n_carico=2, min_ore=4)
        assert ris["errore"] is None and ris["ok"] and ris["valido"]
        m = ris["mat_costo"]
        assert m.shape == (2, 2)
        assert m.iloc[0, 0] == 1.0 and m.iloc[0, 1] == 2.0
        assert m.iloc[1, 0] == 2.0 and m.iloc[1, 1] == 4.0
        assert (ris["mat_ore"].values == 1).all()
        k = ris["kpi"]
        assert k["ore_totali"] == 4
        assert k["costo_totale_eur"] == 9.0
        assert k["quota_dominante_pct"] == round(4.0 / 9.0 * 100, 2)
        assert k["quota_top3_pct"] == 88.88  # somma delle quote arrotondate: 44.44+22.22+22.22
        top = ris["top_celle"]
        assert top.iloc[0]["costo_eur"] == 4.0
        assert abs(top["quota_pct"].sum() - 100.0) < 0.05

    def test_serie_vuota_e_troppo_corta(self):
        r = calcola_mappa_prezzo_carico([], [])
        assert r["errore"] and not r["ok"] and not r["valido"]
        r = calcola_mappa_prezzo_carico([10.0] * 10, [100.0] * 10, min_ore=24)
        assert "almeno 24 ore" in r["errore"]

    def test_input_non_validi(self):
        r = calcola_mappa_prezzo_carico([10, 20], [100])
        assert "lunghezze diverse" in r["errore"]
        r = calcola_mappa_prezzo_carico(["a", "b"], [1, 2])
        assert r["errore"] and not r["ok"]
        r = calcola_mappa_prezzo_carico([10] * 30, [100] * 30, n_prezzo=1)
        assert "almeno 2 bucket" in r["errore"]

    def test_carico_piatto_un_solo_bucket_carico(self):
        # carico costante -> una sola colonna, nessun errore
        prezzi = list(np.linspace(10, 100, 60))
        ris = calcola_mappa_prezzo_carico(prezzi, [100.0] * 60, n_prezzo=3, n_carico=5)
        assert ris["ok"]
        assert ris["mat_costo"].shape == (3, 1)
        assert ris["kpi"]["ore_totali"] == 60

    def test_nan_vengono_scartati(self):
        prezzi = [10.0, np.nan, 20.0, 30.0] * 10
        carichi = [100.0] * 40
        ris = calcola_mappa_prezzo_carico(prezzi, carichi, min_ore=24)
        assert ris["ok"] and ris["kpi"]["ore_totali"] == 30

    def test_determinismo(self):
        rng = np.random.default_rng(7)
        p = rng.uniform(20, 200, 200)
        c = rng.uniform(50, 300, 200)
        a = calcola_mappa_prezzo_carico(p, c, n_prezzo=4, n_carico=4)
        b = calcola_mappa_prezzo_carico(p, c, n_prezzo=4, n_carico=4)
        assert a["ok"] and b["ok"]
        assert (a["mat_costo"].values == b["mat_costo"].values).all()
        assert a["kpi"] == b["kpi"]
