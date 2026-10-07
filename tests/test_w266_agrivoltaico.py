"""Test tab266 'Agrivoltaico: doppio reddito': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab266.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("av266_num", "av266_int", "av266_ler", "av266_produzione_annua",
          "av266_fattore_rendita", "av266_npv_solo_agri",
          "av266_npv_agrivoltaico", "av266_npv_fv_terra",
          "av266_confronto", "av266_anno_pareggio",
          "av266_sensibilita_prezzo")
av266_num = _F["av266_num"]
av266_int = _F["av266_int"]
av266_ler = _F["av266_ler"]
av266_produzione_annua = _F["av266_produzione_annua"]
av266_fattore_rendita = _F["av266_fattore_rendita"]
av266_npv_solo_agri = _F["av266_npv_solo_agri"]
av266_npv_agrivoltaico = _F["av266_npv_agrivoltaico"]
av266_npv_fv_terra = _F["av266_npv_fv_terra"]
av266_confronto = _F["av266_confronto"]
av266_anno_pareggio = _F["av266_anno_pareggio"]
av266_sensibilita_prezzo = _F["av266_sensibilita_prezzo"]

APP = Path(__file__).parent.parent / "app.py"

TITLE266 = "\U0001F33E\uFE0F Agrivoltaico: doppio reddito"
TITLE267 = "🟢 Biometano: business case"
TITLE268 = "🌬️ Eolico onshore: business case"
TITLE269 = "🌊 Idroelettrico run-of-river: business case"
TITLE270 = "🔥 Geotermia profonda: business case"
TITLE271 = "☀️ Solare termodinamico (CSP): business case"
TITLE272 = "🌬️ Eolico offshore: business case"
TITLE273 = "☀️ Fotovoltaico utility-scale: business case"
TITLE274 = "⚛️ Nucleare SMR: business case"
TITLE275 = "📊 Posizione vs limiti di rischio"
TITLE276 = "💧 Cash flow at risk (CFaR)"
TITLE265 = "\U0000267B\uFE0F Fine vita FV: revamping vs dismissione"

HA = 10.0
MARGINE_HA = 1200.0
PERDITA = 25.0
KWP = 1000.0
RESA = 1100.0
DEGRADO = 0.5
PREZZO = 0.10
CAPEX_AGRIV = 945000.0
CAPEX_FV = 700000.0
OEM = 12000.0
ANNI = 25
TASSO = 5.0


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab266:
    def test_tab266_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 276
        assert TITLE266 in titoli
        assert "tab266" in dvars
        assert "tab266" in withs
        assert titoli[dvars.index("tab266")] == TITLE266
        assert titoli[-1] == TITLE276
        keys = re.findall(r'key="(av266_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_265_266(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab265")] == TITLE265
        assert titoli[dvars.index("tab266")] == TITLE266
        assert titoli[dvars.index("tab267")] == TITLE267
        assert titoli[dvars.index("tab268")] == TITLE268
        assert titoli[dvars.index("tab269")] == TITLE269
        assert titoli[dvars.index("tab270")] == TITLE270
        assert titoli[dvars.index("tab271")] == TITLE271
        assert titoli[dvars.index("tab272")] == TITLE272
        assert titoli[dvars.index("tab273")] == TITLE273
        assert titoli[dvars.index("tab274")] == TITLE274
        assert titoli[dvars.index("tab275")] == TITLE275
        assert titoli[dvars.index("tab276")] == TITLE276


class TestAv266Num:
    def test_ok(self):
        assert av266_num(3, "x") == 3.0
        assert av266_num(2.5, "x") == 2.5

    def test_invalidi(self):
        for bad in (True, False, float("nan"), float("inf"), "3", None):
            with pytest.raises(ValueError):
                av266_num(bad, "x")

    def test_int(self):
        assert av266_int(25, "anni") == 25
        assert av266_int(25.0, "anni") == 25
        for bad in (0, -3, 2.5, "25"):
            with pytest.raises(ValueError):
                av266_int(bad, "anni")


class TestAv266Ler:
    def test_perdita_zero(self):
        assert av266_ler(0.0) == pytest.approx(2.0)

    def test_perdita_25(self):
        assert av266_ler(25.0) == pytest.approx(1.75)

    def test_perdita_totale(self):
        assert av266_ler(100.0) == pytest.approx(1.0)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            av266_ler(-0.1)
        with pytest.raises(ValueError):
            av266_ler(100.1)


class TestAv266ProduzioneAnnua:
    def test_anno1_e_anno2(self):
        assert av266_produzione_annua(KWP, RESA, DEGRADO, 1) == pytest.approx(KWP * RESA)
        assert av266_produzione_annua(KWP, RESA, DEGRADO, 2) == pytest.approx(KWP * RESA * 0.995)

    def test_degrado_nullo(self):
        assert av266_produzione_annua(KWP, RESA, 0.0, 9) == pytest.approx(KWP * RESA)

    def test_monotonia(self):
        prods = [av266_produzione_annua(KWP, RESA, DEGRADO, a) for a in range(1, 11)]
        assert all(b < a for a, b in zip(prods, prods[1:]))

    def test_invalidi(self):
        with pytest.raises(ValueError):
            av266_produzione_annua(-1.0, RESA, DEGRADO, 1)
        with pytest.raises(ValueError):
            av266_produzione_annua(KWP, -10.0, DEGRADO, 1)
        with pytest.raises(ValueError):
            av266_produzione_annua(KWP, RESA, 51.0, 1)
        with pytest.raises(ValueError):
            av266_produzione_annua(KWP, RESA, DEGRADO, 0)


class TestAv266FattoreRendita:
    def test_tasso_zero(self):
        assert av266_fattore_rendita(0.0, ANNI) == pytest.approx(float(ANNI))

    def test_un_anno(self):
        assert av266_fattore_rendita(5.0, 1) == pytest.approx(1 / 1.05)

    def test_formula(self):
        atteso = sum(1 / 1.05 ** t for t in range(1, 11))
        assert av266_fattore_rendita(5.0, 10) == pytest.approx(atteso)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            av266_fattore_rendita(-1.0, ANNI)
        with pytest.raises(ValueError):
            av266_fattore_rendita(5.0, 0)


class TestAv266NpvSoloAgri:
    def test_base(self):
        r = av266_npv_solo_agri(HA, MARGINE_HA, ANNI, TASSO)
        assert r["reddito_annuo"] == pytest.approx(HA * MARGINE_HA)
        assert r["npv"] == pytest.approx(HA * MARGINE_HA * av266_fattore_rendita(TASSO, ANNI))

    def test_tasso_zero(self):
        r = av266_npv_solo_agri(HA, MARGINE_HA, ANNI, 0.0)
        assert r["npv"] == pytest.approx(HA * MARGINE_HA * ANNI)

    def test_invalidi(self):
        with pytest.raises(ValueError):
            av266_npv_solo_agri(0.0, MARGINE_HA, ANNI, TASSO)
        with pytest.raises(ValueError):
            av266_npv_solo_agri(HA, MARGINE_HA, ANNI, -1.0)


class TestAv266NpvAgrivoltaico:
    def test_chiavi_e_coerenza(self):
        r = av266_npv_agrivoltaico(HA, MARGINE_HA, PERDITA, KWP, RESA, DEGRADO,
                                  PREZZO, CAPEX_AGRIV, OEM, ANNI, TASSO)
        assert set(r) == {"npv", "capex", "margine_agri_residuo", "produzioni",
                          "flussi_attualizzati", "produzione_totale_kwh"}
        assert len(r["produzioni"]) == len(r["flussi_attualizzati"]) == ANNI
        assert r["capex"] == pytest.approx(CAPEX_AGRIV)
        assert r["margine_agri_residuo"] == pytest.approx(HA * MARGINE_HA * 0.75)
        assert r["produzione_totale_kwh"] == pytest.approx(sum(r["produzioni"]))
        assert r["npv"] == pytest.approx(sum(r["flussi_attualizzati"]) - CAPEX_AGRIV)
        assert r["produzioni"][0] == pytest.approx(KWP * RESA)

    def test_capex_zero_perdita_zero_scomposizione(self):
        # senza capex e senza perdita agricola: agri + FV separati
        r = av266_npv_agrivoltaico(HA, MARGINE_HA, 0.0, KWP, RESA, DEGRADO,
                                  PREZZO, 0.0, OEM, ANNI, TASSO)
        a = av266_npv_solo_agri(HA, MARGINE_HA, ANNI, TASSO)["npv"]
        f = av266_npv_fv_terra(KWP, RESA, DEGRADO, PREZZO, 0.0, OEM, ANNI, TASSO)["npv"]
        assert r["npv"] == pytest.approx(a + f)

    def test_prezzo_alto_aumenta_npv(self):
        r1 = av266_npv_agrivoltaico(HA, MARGINE_HA, PERDITA, KWP, RESA, DEGRADO,
                                   0.05, CAPEX_AGRIV, OEM, ANNI, TASSO)
        r2 = av266_npv_agrivoltaico(HA, MARGINE_HA, PERDITA, KWP, RESA, DEGRADO,
                                   0.20, CAPEX_AGRIV, OEM, ANNI, TASSO)
        assert r2["npv"] > r1["npv"]

    def test_invalidi(self):
        with pytest.raises(ValueError):
            av266_npv_agrivoltaico(HA, MARGINE_HA, 101.0, KWP, RESA, DEGRADO,
                                  PREZZO, CAPEX_AGRIV, OEM, ANNI, TASSO)
        with pytest.raises(ValueError):
            av266_npv_agrivoltaico(HA, MARGINE_HA, PERDITA, KWP, RESA, DEGRADO,
                                  -0.1, CAPEX_AGRIV, OEM, ANNI, TASSO)
        with pytest.raises(ValueError):
            av266_npv_agrivoltaico(HA, MARGINE_HA, PERDITA, KWP, RESA, DEGRADO,
                                  PREZZO, -1.0, OEM, ANNI, TASSO)
        with pytest.raises(ValueError):
            av266_npv_agrivoltaico(0.0, MARGINE_HA, PERDITA, KWP, RESA, DEGRADO,
                                  PREZZO, CAPEX_AGRIV, OEM, ANNI, TASSO)


class TestAv266NpvFvTerra:
    def test_base(self):
        r = av266_npv_fv_terra(KWP, RESA, DEGRADO, PREZZO, CAPEX_FV, OEM, ANNI, TASSO)
        atteso = (sum(av266_produzione_annua(KWP, RESA, DEGRADO, a) * PREZZO
                      / 1.05 ** a for a in range(1, ANNI + 1))
                  - sum(OEM / 1.05 ** a for a in range(1, ANNI + 1)) - CAPEX_FV)
        assert r["npv"] == pytest.approx(atteso)
        assert r["produzione_totale_kwh"] == pytest.approx(sum(r["produzioni"]))

    def test_prezzo_zero_negativo(self):
        r = av266_npv_fv_terra(KWP, RESA, DEGRADO, 0.0, CAPEX_FV, OEM, ANNI, TASSO)
        assert r["npv"] < 0

    def test_invalidi(self):
        with pytest.raises(ValueError):
            av266_npv_fv_terra(KWP, RESA, DEGRADO, PREZZO, -5.0, OEM, ANNI, TASSO)
        with pytest.raises(ValueError):
            av266_npv_fv_terra(KWP, RESA, DEGRADO, PREZZO, CAPEX_FV, -1.0, ANNI, TASSO)


class TestAv266Confronto:
    def test_vince_agrivoltaico(self):
        r = av266_confronto(100.0, 150.0, 120.0)
        assert r["verdetto"] == "agrivoltaico"
        assert r["migliore"] == "agrivoltaico"
        assert r["secondo"] == "fv_terra"
        assert r["margine_pct"] == pytest.approx(20.0)

    def test_vince_solo_agri(self):
        r = av266_confronto(200.0, 100.0, -50.0)
        assert r["verdetto"] == "solo_agri"
        assert r["margine_pct"] == pytest.approx(50.0)

    def test_vince_fv_terra(self):
        r = av266_confronto(50.0, 80.0, 120.0)
        assert r["verdetto"] == "fv_terra"
        assert r["secondo"] == "agrivoltaico"

    def test_indifferente(self):
        r = av266_confronto(100.0, 103.0, 90.0)
        assert r["verdetto"] == "indifferente"
        assert r["migliore"] == "agrivoltaico"
        assert r["margine_pct"] == pytest.approx(3.0 / 103.0 * 100.0)

    def test_migliore_zero(self):
        r = av266_confronto(0.0, -10.0, -20.0)
        assert r["verdetto"] == "solo_agri"
        assert r["margine_pct"] is None

    def test_invalidi(self):
        with pytest.raises(ValueError):
            av266_confronto("100", 150.0, 120.0)


class TestAv266Pareggio:
    def test_capex_zero_pareggio_anno1(self):
        a = av266_anno_pareggio(HA, MARGINE_HA, 0.0, KWP, RESA, DEGRADO,
                                PREZZO, 0.0, OEM, ANNI, TASSO)
        assert a == 1

    def test_capex_enorme_mai(self):
        a = av266_anno_pareggio(HA, MARGINE_HA, PERDITA, KWP, RESA, DEGRADO,
                                PREZZO, 1e12, OEM, ANNI, TASSO)
        assert a is None

    def test_pareggio_intermedio(self):
        # prezzo alto + perdita contenuta: pareggia entro l'orizzonte
        a = av266_anno_pareggio(HA, MARGINE_HA, 10.0, KWP, RESA, DEGRADO,
                                0.30, 200000.0, OEM, ANNI, TASSO)
        assert a is not None and 1 <= a <= ANNI

    def test_invalidi(self):
        with pytest.raises(ValueError):
            av266_anno_pareggio(HA, MARGINE_HA, PERDITA, KWP, RESA, DEGRADO,
                                PREZZO, -1.0, OEM, ANNI, TASSO)


class TestAv266Sensibilita:
    def test_lunghezza_e_chiavi(self):
        righe = av266_sensibilita_prezzo(HA, MARGINE_HA, PERDITA, KWP, RESA, DEGRADO,
                                         CAPEX_AGRIV, CAPEX_FV, OEM, ANNI, TASSO,
                                         0.2, 0.1)
        assert len(righe) == 3
        assert righe[0]["prezzo_kwh"] == pytest.approx(0.0)
        assert righe[-1]["prezzo_kwh"] == pytest.approx(0.2)
        assert set(righe[0]) == {"prezzo_kwh", "npv_agri", "npv_agrivoltaico", "npv_fv"}

    def test_monotonia_e_coerenza(self):
        righe = av266_sensibilita_prezzo(HA, MARGINE_HA, PERDITA, KWP, RESA, DEGRADO,
                                         CAPEX_AGRIV, CAPEX_FV, OEM, ANNI, TASSO,
                                         0.2, 0.1)
        nv = [r["npv_agrivoltaico"] for r in righe]
        nf = [r["npv_fv"] for r in righe]
        na = [r["npv_agri"] for r in righe]
        assert all(b > a for a, b in zip(nv, nv[1:]))
        assert all(b > a for a, b in zip(nf, nf[1:]))
        assert all(x == na[0] for x in na)
        assert righe[1]["npv_agrivoltaico"] == pytest.approx(
            av266_npv_agrivoltaico(HA, MARGINE_HA, PERDITA, KWP, RESA, DEGRADO,
                                   0.1, CAPEX_AGRIV, OEM, ANNI, TASSO)["npv"])

    def test_invalidi(self):
        with pytest.raises(ValueError):
            av266_sensibilita_prezzo(HA, MARGINE_HA, PERDITA, KWP, RESA, DEGRADO,
                                     CAPEX_AGRIV, CAPEX_FV, OEM, ANNI, TASSO,
                                     0.0, 0.1)
        with pytest.raises(ValueError):
            av266_sensibilita_prezzo(HA, MARGINE_HA, PERDITA, KWP, RESA, DEGRADO,
                                     CAPEX_AGRIV, CAPEX_FV, OEM, ANNI, TASSO,
                                     0.2, 0.0)
