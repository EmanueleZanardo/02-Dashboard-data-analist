"""Test tab627 "💧🗄️ Stoccaggio H2: lo storage idrogeno rende? (caverna salina)".

Demo calcolata a mano: 100 kg/h x 4000 h -> 400.000 kg H2/anno;
caverna 100 t x 4 cicli/anno -> throughput 400.000 kg, kg stoccati
= 400.000 (min, non limitato). CRF(8 %, 20 a) = 0,1018522088231506;
capex 100.000 kg x 1,5 = 150.000; storage = 150.000 x CRF +
150.000 x 4 % = 21.277,8313234726; compressione 400.000 x 0,35 =
140.000; logistica = 161.277,8313234726; LCoHS = 0,4031945783086814
€/kg. LCOH 5,13 -> H2 2.052.000. Ricavi vendita 7,20 -> 2.880.000;
ricavi base 5,60 -> 2.240.000; margine storage 666.722,1686765274;
margine diretto 188.000; valore storage 478.722,1686765274 ->
CONVIENTE.
"""

import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh627_num", "mh627_nneg", "mh627_pos", "mh627_frac01",
           "mh627_kg_h2_annui", "mh627_kg_stoccati_annui",
           "mh627_crf", "mh627_capex_totale",
           "mh627_costo_storage_annuo", "mh627_costo_compressione",
           "mh627_costo_h2", "mh627_lcohs", "mh627_ricavi",
           "mh627_margine_storage", "mh627_margine_diretto",
           "mh627_valore_storage", "mh627_verdetto",
           "mh627_sensibilita", "mh627_demo")

TITLE627 = ("💧🗄️ Stoccaggio H2: lo storage idrogeno rende? "
            "(caverna salina)")

DEMO = _F["mh627_demo"]()
KG_DEMO = 400000.0
KS_DEMO = 400000.0
CRF_DEMO = 0.1018522088231506
CAPEX_DEMO = 150000.0
CSTOR_DEMO = 21277.8313234726
CCOMPR_DEMO = 140000.0
LOG_DEMO = 161277.8313234726
LCOHS_DEMO = 0.4031945783086814
CH2_DEMO = 2052000.0
MS_DEMO = 666722.1686765274
MD_DEMO = 188000.0
VS_DEMO = 478722.1686765274


class TestW627Validatori:
    def test_num(self):
        assert _F["mh627_num"](3, "x") == 3.0
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh627_num"](bad, "x")

    def test_nneg_pos_frac01(self):
        assert _F["mh627_nneg"](0, "x") == 0.0
        assert _F["mh627_pos"](0.001, "x") == 0.001
        assert _F["mh627_frac01"](1, "x") == 1.0
        for bad in (-1.0,):
            with pytest.raises(ValueError):
                _F["mh627_nneg"](bad, "x")
        for bad in (0.0, -2.0):
            with pytest.raises(ValueError):
                _F["mh627_pos"](bad, "x")
        for bad in (-0.1, 1.1):
            with pytest.raises(ValueError):
                _F["mh627_frac01"](bad, "x")


class TestW627Catena:
    def test_kg_e_stoccati(self):
        assert _F["mh627_kg_h2_annui"](100.0, 4000.0) == KG_DEMO
        assert _F["mh627_kg_stoccati_annui"](KG_DEMO, 100.0, 4.0) \
            == KS_DEMO
        # throughput < produzione: limita lo stoccato
        assert _F["mh627_kg_stoccati_annui"](400000.0, 50.0, 4.0) \
            == 200000.0
        with pytest.raises(ValueError):
            _F["mh627_kg_h2_annui"](-1.0, 4000.0)

    def test_crf(self):
        assert _F["mh627_crf"](8.0, 20.0) == pytest.approx(CRF_DEMO)
        assert _F["mh627_crf"](0.0, 20.0) == pytest.approx(1.0 / 20.0)
        with pytest.raises(ValueError):
            _F["mh627_crf"](8.0, 0.0)

    def test_costi(self):
        assert _F["mh627_capex_totale"](100.0, 1.5) == CAPEX_DEMO
        assert _F["mh627_costo_storage_annuo"](CAPEX_DEMO, 4.0,
                                               CRF_DEMO) == \
            pytest.approx(CSTOR_DEMO)
        assert _F["mh627_costo_compressione"](KS_DEMO, 0.35) == \
            CCOMPR_DEMO
        assert _F["mh627_costo_h2"](KG_DEMO, 5.13) == CH2_DEMO

    def test_lcohs(self):
        assert _F["mh627_lcohs"](CSTOR_DEMO, CCOMPR_DEMO,
                                 KS_DEMO) == pytest.approx(LCOHS_DEMO)
        assert _F["mh627_lcohs"](100.0, 50.0, 0.0) is None

    def test_margini_valore(self):
        ms = _F["mh627_margine_storage"](2880000.0, CH2_DEMO,
                                         CSTOR_DEMO, CCOMPR_DEMO)
        assert ms == pytest.approx(MS_DEMO)
        md = _F["mh627_margine_diretto"](2240000.0, CH2_DEMO)
        assert md == MD_DEMO
        assert _F["mh627_valore_storage"](ms, md) == \
            pytest.approx(VS_DEMO)
        # valore = kg x premio - logistica
        assert _F["mh627_valore_storage"](ms, md) == \
            pytest.approx(KG_DEMO * 1.6 - LOG_DEMO)

    def test_verdetto_stati(self):
        assert _F["mh627_verdetto"](VS_DEMO, LOG_DEMO,
                                   KS_DEMO)["verdetto"] == "CONVIENTE"
        assert _F["mh627_verdetto"](0.0, LOG_DEMO,
                                   KS_DEMO)["verdetto"] == "CONVIENTE"
        assert _F["mh627_verdetto"](-0.10 * LOG_DEMO, LOG_DEMO,
                                   KS_DEMO)["verdetto"] == "MARGINALE"
        assert _F["mh627_verdetto"](-0.16 * LOG_DEMO, LOG_DEMO,
                                   KS_DEMO)["verdetto"] == \
            "NON_CONVIENTE"
        assert _F["mh627_verdetto"](10.0, LOG_DEMO,
                                   0.0)["verdetto"] == "NON_CALCOLABILE"


class TestW627Sensibilita:
    def _args(self):
        return (100.0, 4000.0, 100.0, 4.0, 1.5, 4.0, 0.35, 8.0, 20.0,
                5.60)

    def test_geometria(self):
        rows = _F["mh627_sensibilita"](*self._args(), [2.0, 5.0],
                                       [0.5, 1.0])
        assert len(rows) == 4
        assert rows[0]["lcoh_eur_kg"] == 2.0
        assert rows[0]["premio_eur_kg"] == 0.5

    def test_riga_estrema_hand_computed(self):
        # LCOH 2, premio 0,5: margine storage 1.478.722,17;
        # diretto 1.440.000; valore 38.722,17 -> CONVIENTE
        rows = _F["mh627_sensibilita"](*self._args(), [2.0], [0.5])
        r = rows[0]
        assert r["margine_storage"] == \
            pytest.approx(1478722.1686765274)
        assert r["margine_diretto"] == pytest.approx(1440000.0)
        assert r["valore_storage"] == pytest.approx(38722.16867652745)
        assert r["giudizio"] == "CONVIENTE"

    def test_monotonia_margine(self):
        rows = _F["mh627_sensibilita"](*self._args(),
                                       [2.0, 5.0, 8.0], [1.0])
        ms = [r["margine_storage"] for r in rows]
        assert ms == sorted(ms, reverse=True)

    def test_non_conviente_estremo(self):
        # LCOH 8, premio 0,2: valore -81.277,83 < -15 % logistica
        rows = _F["mh627_sensibilita"](*self._args(), [8.0], [0.2])
        r = rows[0]
        assert r["valore_storage"] == \
            pytest.approx(-81277.8313234726)
        assert r["giudizio"] == "NON_CONVIENTE"

    def test_liste_vuote(self):
        assert _F["mh627_sensibilita"](*self._args(), [], [1.0]) == []
        assert _F["mh627_sensibilita"](*self._args(), [5.0], []) == []

    def test_demo_catena_completa(self):
        d = DEMO
        kg = _F["mh627_kg_h2_annui"](d["portata_kg_h"], d["ore_annue"])
        ks = _F["mh627_kg_stoccati_annui"](kg, d["capacita_t"],
                                           d["cicli_anno"])
        crf = _F["mh627_crf"](d["tasso_pct"], d["anni"])
        cx = _F["mh627_capex_totale"](d["capacita_t"],
                                      d["capex_eur_kg"])
        cs = _F["mh627_costo_storage_annuo"](cx, d["opex_pct"], crf)
        cc = _F["mh627_costo_compressione"](ks,
                                            d["costo_compr_eur_kg"])
        ch2 = _F["mh627_costo_h2"](kg, d["lcoh_eur_kg"])
        lcohs = _F["mh627_lcohs"](cs, cc, ks)
        rv = _F["mh627_ricavi"](kg, d["prezzo_vendita_eur_kg"])
        rb = _F["mh627_ricavi"](kg, d["prezzo_base_eur_kg"])
        ms = _F["mh627_margine_storage"](rv, ch2, cs, cc)
        md = _F["mh627_margine_diretto"](rb, ch2)
        vs = _F["mh627_valore_storage"](ms, md)
        ver = _F["mh627_verdetto"](vs, cs + cc, ks)
        assert kg == pytest.approx(KG_DEMO)
        assert ks == pytest.approx(KS_DEMO)
        assert crf == pytest.approx(CRF_DEMO)
        assert cx == pytest.approx(CAPEX_DEMO)
        assert cs == pytest.approx(CSTOR_DEMO)
        assert cc == pytest.approx(CCOMPR_DEMO)
        assert ch2 == pytest.approx(CH2_DEMO)
        assert lcohs == pytest.approx(LCOHS_DEMO)
        assert ms == pytest.approx(MS_DEMO)
        assert md == pytest.approx(MD_DEMO)
        assert vs == pytest.approx(VS_DEMO)
        assert ver["verdetto"] == "CONVIENTE"


class TestW627Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def _ui(self):
        return self._src().split("with tab627:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 656
        assert TITLE627 in titles
        assert TITLE627 in titles

    def test_chain(self):
        assert ", tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656 = st.tabs([" in self._src()
        assert "with tab627:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st627_[a-z0-9_]+", self._ui()))
        attese = {"st627_port", "st627_ore", "st627_lcoh",
                  "st627_cap", "st627_cic", "st627_cx",
                  "st627_opex", "st627_comp", "st627_tasso",
                  "st627_anni", "st627_pv", "st627_pb",
                  "st627_tab", "st627_graf", "st627_go",
                  "st627_fig", "st627_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st627_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        sec = self._src().split('# W627 (22/10/2026)')[1]
        sec = sec.split('# W626 (21/10/2026)')[0]
        for w in ("api_key", "apikey", "password", "passwd", "secret",
                  "token"):
            assert w not in sec.lower(), f"sospetto segreto: {w}"
