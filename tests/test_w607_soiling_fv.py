"""Test tab607 "☀️🧹 Soiling & degrado FV: quanto perdi senza pulire i pannelli".

Tutti i valori attesi sono calcolati a mano nei commenti (aritmetica
indipendente dagli helper) e contro-verificati con gli helper stessi.
"""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh607_num", "mh607_nneg", "mh607_pos", "mh607_pct",
           "mh607_int", "mh607_fattore_degrado", "mh607_profilo_soiling",
           "mh607_perdita_media", "mh607_aep0", "mh607_aep_effettiva",
           "mh607_mwh_persi_soiling", "mh607_valore_perso",
           "mh607_giorni_pioggia", "mh607_profilo_con_pulizie",
           "mh607_n_pulizie", "mh607_costo_pulizie_annuo",
           "mh607_costo_totale", "mh607_ottimo", "mh607_verdetto",
           "mh607_sensibilita_tasso", "mh607_demo")

TITLE607 = "☀️🧹 Soiling & degrado FV: quanto perdi senza pulire i pannelli"

DEMO = _F["mh607_demo"]()
# Demo: FV 10 MW, 1200 ore eq -> AEP0 = 12000 MWh; prezzo 80 EUR/MWh;
# soiling 0,1 %/giorno, 0 piogge; anno 5, degrado 0,5 %/anno;
# pulizia 1500 EUR/MW/intervento -> 15000 EUR/intervento (10 MW).
# f_degrado(5) = 1 - 0,5*5/100 = 0,975 ; AEP_degradata = 11700 MWh
# profilo 365 gg senza pioggia: [0,1; 0,2; ...; 36,5]
#   perdita media = 0,1 * 366/2 = 18,3 %
# AEP_eff = 11700 * (1 - 0,183) = 11700 * 0,817 = 9558,9 MWh
# MWh persi = 11700 - 9558,9 = 2141,1 MWh
# valore perso = 2141,1 * 80 = 171288,0 EUR
# ottimo (scansione k=7..730, costo_intervento 15000):
#   k=122: reset d=122,244; giorno d -> 0,1*(d+1) tra un reset e l'altro
#     segmenti: [0..121] (122 gg): 0,1*122*123/2 = 750,3
#               [123..243] (121 gg): 0,1*121*122/2 = 738,1
#               [245..364] (120 gg): 0,1*120*121/2 = 726,0
#     somma = 2214,4 ; pm = 2214,4/365 = 6,066849315068485 %
#     MWh = 11700*0,06066849315068485 = 709,8213698630127
#     valore = 709,8213698630127*80 = 56785,70958904101
#     pulizie = 364//122 = 2 -> 30000 ; totale = 86785,70958904101
#   vicini: k=121 -> 101165,12876712321 ; k=123 -> 86801,09589041087 ;
#           k=92 -> 87481,57808219173 ; k=183 -> 100411,92328767109
#   -> k* = 122 minimo globale
# risparmio = 171288,00000000047 - 86785,70958904101 = 84502,29041145946
#   > 2% * 171288 = 3425,76 -> PULIRE_CONVIENE
AEP0 = 12000.0
F_DEGR = 0.975
AEP_DEGR = 11700.0
PM_MEDIA = 18.3
AEP_EFF = 9558.9
MWH_PERSI = 2141.1
VALORE_PERSO = 171288.0
K_OTT = 122
N_PULIZIE_OTT = 2
PM_OTT = 6.066849315068485
MWH_OTT = 709.8213698630127
VALORE_OTT = 56785.70958904101
COSTO_PUL_OTT = 30000.0
TOT_OTT = 86785.70958904101
RISPARMIO = 84502.29041145946


class TestW607Validatori:
    def test_num(self):
        assert _F["mh607_num"](3, "x") == 3.0
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh607_num"](bad, "x")

    def test_nneg_pos_pct(self):
        assert _F["mh607_nneg"](0, "x") == 0.0
        assert _F["mh607_pos"](0.5, "x") == 0.5
        assert _F["mh607_pct"](100, "x") == 100.0
        for bad in (-1,):
            with pytest.raises(ValueError):
                _F["mh607_nneg"](bad, "x")
        with pytest.raises(ValueError):
            _F["mh607_pos"](0, "x")
        for bad in (-0.1, 100.1):
            with pytest.raises(ValueError):
                _F["mh607_pct"](bad, "x")

    def test_int(self):
        assert _F["mh607_int"](5, "x") == 5
        assert _F["mh607_int"](0, "x", minimo=0) == 0
        for bad in (True, 5.0, "5", -1):
            with pytest.raises(ValueError):
                _F["mh607_int"](bad, "x", minimo=0)


class TestW607Degrado:
    def test_fattore(self):
        assert _F["mh607_fattore_degrado"](0, 0.5) == 1.0
        assert _F["mh607_fattore_degrado"](5, 0.5) == pytest.approx(F_DEGR)
        assert _F["mh607_fattore_degrado"](10, 1.0) == pytest.approx(0.9)

    def test_degeneri(self):
        with pytest.raises(ValueError):  # anno negativo
            _F["mh607_fattore_degrado"](-1, 0.5)
        with pytest.raises(ValueError):  # tasso oltre 100%
            _F["mh607_fattore_degrado"](3, 40.0)
        with pytest.raises(ValueError):  # anno non intero
            _F["mh607_fattore_degrado"](2.5, 0.5)


class TestW607Profilo:
    def test_lineare(self):
        p = _F["mh607_profilo_soiling"](10, 1.0, [])
        assert p == [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]

    def test_pioggia_reset(self):
        # pioggia il giorno 4 (0-based): [1,2,3,4,0,1,2,3,4,5]
        p = _F["mh607_profilo_soiling"](10, 1.0, [4])
        assert p == [1.0, 2.0, 3.0, 4.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
        assert _F["mh607_perdita_media"](p) == pytest.approx(2.5)

    def test_cap_100(self):
        p = _F["mh607_profilo_soiling"](5, 30.0, [])
        assert p[-1] == 100.0

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh607_profilo_soiling"](0, 1.0, [])
        with pytest.raises(ValueError):
            _F["mh607_profilo_soiling"](10, -1.0, [])
        with pytest.raises(ValueError):  # giorno fuori orizzonte
            _F["mh607_profilo_soiling"](10, 1.0, [10])
        with pytest.raises(ValueError):  # profilo vuoto
            _F["mh607_perdita_media"]([])

    def test_giorni_pioggia(self):
        assert _F["mh607_giorni_pioggia"](0) == []
        g12 = _F["mh607_giorni_pioggia"](12)
        assert len(g12) == 12 == len(set(g12))
        assert all(0 <= g < 365 for g in g12)
        # uniformita': distanza media ~365/13
        assert g12 == sorted(g12)
        with pytest.raises(ValueError):
            _F["mh607_giorni_pioggia"](-1)
        with pytest.raises(ValueError):
            _F["mh607_giorni_pioggia"](366)


class TestW607Energia:
    def test_aep0(self):
        assert _F["mh607_aep0"](10.0, 1200.0) == pytest.approx(AEP0)
        with pytest.raises(ValueError):
            _F["mh607_aep0"](0, 1200.0)

    def test_demo_completa(self):
        d = DEMO
        aep0 = _F["mh607_aep0"](d["p_mw"], d["ore_eq"])
        assert aep0 == pytest.approx(AEP0)
        prof = _F["mh607_profilo_soiling"](
            365, d["tasso_soiling"], _F["mh607_giorni_pioggia"](d["n_pioggia"]))
        pm = _F["mh607_perdita_media"](prof)
        assert pm == pytest.approx(PM_MEDIA)
        eff = _F["mh607_aep_effettiva"](aep0, d["anno"], d["tasso_degrado"], pm)
        assert eff == pytest.approx(AEP_EFF)
        persi = _F["mh607_mwh_persi_soiling"](aep0, d["anno"],
                                             d["tasso_degrado"], pm)
        assert persi == pytest.approx(MWH_PERSI)
        val = _F["mh607_valore_perso"](persi, d["prezzo"])
        assert val == pytest.approx(VALORE_PERSO)

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh607_aep_effettiva"](100.0, 1, 0.5, 101.0)
        with pytest.raises(ValueError):
            _F["mh607_valore_perso"](-5.0, 80.0)


class TestW607Pulizie:
    def test_profilo_con_pulizie(self):
        # k=3 su 10 gg: reset d=3,6,9 -> [1,2,3,0,1,2,0,1,2,0]
        p = _F["mh607_profilo_con_pulizie"](10, 1.0, [], 3)
        assert p == [1.0, 2.0, 3.0, 0.0, 1.0, 2.0, 0.0, 1.0, 2.0, 0.0]

    def test_n_pulizie(self):
        assert _F["mh607_n_pulizie"](3) == 121       # 364//3
        assert _F["mh607_n_pulizie"](122) == 2       # 364//122
        assert _F["mh607_n_pulizie"](365) == 0       # mai pulire
        assert _F["mh607_n_pulizie"](730) == 0
        assert _F["mh607_costo_pulizie_annuo"](15000.0, 122) == 30000.0
        with pytest.raises(ValueError):
            _F["mh607_n_pulizie"](0)

    def test_ottimo_demo(self):
        d = DEMO
        ott = _F["mh607_ottimo"](AEP_DEGR, d["prezzo"], d["tasso_soiling"],
                                 [], d["costo_pulizia_mw"] * d["p_mw"])
        assert ott["k_ott"] == K_OTT
        assert ott["n_pulizie"] == N_PULIZIE_OTT
        assert ott["perdita_media_pct"] == pytest.approx(PM_OTT)
        assert ott["mwh_persi"] == pytest.approx(MWH_OTT)
        assert ott["valore_perso"] == pytest.approx(VALORE_OTT)
        assert ott["costo_pulizie"] == pytest.approx(COSTO_PUL_OTT)
        assert ott["costo_totale"] == pytest.approx(TOT_OTT)

    def test_ottimo_vicini(self):
        # k* = 122 e' minimo locale: i vicini costano di piu'
        d = DEMO
        c = d["costo_pulizia_mw"] * d["p_mw"]
        tot = lambda k: _F["mh607_costo_totale"](AEP_DEGR, d["prezzo"],
                                                d["tasso_soiling"], [], c, k)
        t122 = tot(122)
        assert t122 == pytest.approx(TOT_OTT)
        assert tot(121) > t122
        assert tot(123) > t122
        assert tot(92) > t122
        assert tot(183) > t122

    def test_ottimo_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh607_ottimo"](100.0, 80.0, 0.1, [], 15000.0,
                               k_min=100, k_max=7)
        with pytest.raises(ValueError):
            _F["mh607_ottimo"](100.0, 80.0, 0.1, [], 15000.0, k_min=0)


class TestW607Verdetto:
    def test_demo(self):
        v = _F["mh607_verdetto"](RISPARMIO, VALORE_PERSO)
        assert v["verdetto"] == "PULIRE_CONVIENE"

    def test_marginale(self):
        v = _F["mh607_verdetto"](100.0, 100000.0)  # 0,1% -> MARGINALE
        assert v["verdetto"] == "MARGINALE"

    def test_indifferente(self):
        v = _F["mh607_verdetto"](0.0, 50000.0)
        assert v["verdetto"] == "INDIFFERENTE"


class TestW607Sensibilita:
    def test_righe(self):
        righe = _F["mh607_sensibilita_tasso"](AEP_DEGR, 80.0,
                                             [0.02, 0.05, 0.1, 0.2, 0.3])
        assert len(righe) == 5
        # pm = tasso*366/2 (365 gg, senza pioggia)
        assert righe[0]["perdita_media_pct"] == pytest.approx(3.66)
        assert righe[2]["perdita_media_pct"] == pytest.approx(18.3)
        assert righe[2]["mwh_persi"] == pytest.approx(MWH_PERSI)
        assert righe[2]["valore_perso"] == pytest.approx(VALORE_PERSO)
        # monotonicita'
        vps = [r["valore_perso"] for r in righe]
        assert vps == sorted(vps)
        with pytest.raises(ValueError):
            _F["mh607_sensibilita_tasso"](AEP_DEGR, 80.0, [])

    def test_demo(self):
        d = DEMO
        assert d["p_mw"] == 10.0
        assert d["tasso_soiling"] == 0.1
        assert d["costo_pulizia_mw"] == 1500.0


class TestW607Registro:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def _ui(self):
        return self._src().split("with tab607:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 656
        assert TITLE607 in titles
        assert TITLE607 in titles

    def test_chain(self):
        assert ", tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656 = st.tabs([" in self._src()
        assert "with tab607:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st607_[a-z0-9_]+", self._ui()))
        attese = {"st607_pmw", "st607_oreeq", "st607_prezzo",
                  "st607_tasso", "st607_pioggia", "st607_anno",
                  "st607_degrado", "st607_costopul", "st607_graf",
                  "st607_tabc", "st607_go", "st607_chart", "st607_tab",
                  "st607_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st607_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))
