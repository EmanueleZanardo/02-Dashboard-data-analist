"""Test tab631 "🌱⚗️ BECCS: bioenergia con cattura CO2 (rimozione netta)".

Demo calcolata a mano: 20 MW x 8000 h x 0,85 -> 136.000 MWh/anno;
biogenica 136000 x 0,4 = 54.400 t; catturate x 0,9 = 48.960 t;
rimozione netta x 0,98 = 47.980,8 t; capex 4,5M x 20 = 90.000.000;
CRF(7 %, 25 a) = 0,0858105172206656; capitale annuo = 90M x CRF +
90M x 4 % = 11.322.946,549859904; biomassa 136000 x 1,2 = 163.200 t
x 80 = 13.056.000; T&S 48960 x 30 = 1.468.800; costi =
25.847.746,549859904; ricavi energia 136000 x 90 = 12.240.000;
costo netto = (25.847.746,549859904 - 12.240.000)/47.980,8 =
283,60816305396963 €/tCO2. Credito 120 -> NON_CONVIENTE (gap
163,61). Ricavi crediti 47.980,8 x 120 = 5.757.696; margine =
12.240.000 + 5.757.696 - 25.847.746,549859904 = -7.850.050,549859904.
"""

import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh631_num", "mh631_nneg", "mh631_pos", "mh631_frac01",
           "mh631_mwh_annui", "mh631_co2_biogenica_t",
           "mh631_co2_catturata_t", "mh631_rimozione_netta_t",
           "mh631_crf", "mh631_capex_totale",
           "mh631_costo_capitale_annuo", "mh631_biomassa_t_annue",
           "mh631_costo_biomassa", "mh631_costo_ts",
           "mh631_costi_totali", "mh631_ricavi_energia",
           "mh631_costo_netto_rimozione", "mh631_ricavi_crediti",
           "mh631_margine", "mh631_verdetto", "mh631_sensibilita",
           "mh631_demo")

TITLE631 = ("🌱⚗️ BECCS: bioenergia con cattura CO2 (rimozione netta)")

DEMO = _F["mh631_demo"]()
MWH_DEMO = 136000.0
BIO_DEMO = 54400.0
CAT_DEMO = 48960.0
NET_DEMO = 47980.799999999996
CRF_DEMO = 0.0858105172206656
CX_DEMO = 90000000.0
CAP_DEMO = 11322946.549859904
TB_DEMO = 163200.0
CB_DEMO = 13056000.0
CTS_DEMO = 1468800.0
TOT_DEMO = 25847746.549859904
REL_DEMO = 12240000.0
CN_DEMO = 283.60816305396963
RC_DEMO = 5757695.999999999
MG_DEMO = -7850050.549859904
GAP_DEMO = 163.60816305396963


class TestW631Validatori:
    def test_num(self):
        assert _F["mh631_num"](3, "x") == 3.0
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh631_num"](bad, "x")

    def test_nneg_pos_frac01(self):
        assert _F["mh631_nneg"](0, "x") == 0.0
        assert _F["mh631_pos"](0.001, "x") == 0.001
        assert _F["mh631_frac01"](1, "x") == 1.0
        for bad in (-1.0,):
            with pytest.raises(ValueError):
                _F["mh631_nneg"](bad, "x")
        for bad in (0.0, -2.0):
            with pytest.raises(ValueError):
                _F["mh631_pos"](bad, "x")
        for bad in (-0.1, 1.1):
            with pytest.raises(ValueError):
                _F["mh631_frac01"](bad, "x")


class TestW631Catena:
    def test_mwh_bio_cat_net(self):
        assert _F["mh631_mwh_annui"](20.0, 8000.0, 0.85) == MWH_DEMO
        assert _F["mh631_co2_biogenica_t"](MWH_DEMO, 0.40) == BIO_DEMO
        assert _F["mh631_co2_catturata_t"](BIO_DEMO, 0.90) == CAT_DEMO
        assert _F["mh631_rimozione_netta_t"](CAT_DEMO, 0.02) == \
            pytest.approx(NET_DEMO)
        with pytest.raises(ValueError):
            _F["mh631_mwh_annui"](20.0, 8000.0, 1.5)
        with pytest.raises(ValueError):
            _F["mh631_co2_catturata_t"](-1.0, 0.9)

    def test_crf(self):
        assert _F["mh631_crf"](7.0, 25.0) == pytest.approx(CRF_DEMO)
        assert _F["mh631_crf"](0.0, 25.0) == pytest.approx(1.0 / 25.0)
        with pytest.raises(ValueError):
            _F["mh631_crf"](7.0, 0.0)

    def test_capex_e_capitale(self):
        assert _F["mh631_capex_totale"](4500000.0, 20.0) == CX_DEMO
        ca = _F["mh631_costo_capitale_annuo"](CX_DEMO, CRF_DEMO, 4.0)
        assert ca == pytest.approx(CAP_DEMO)
        with pytest.raises(ValueError):
            _F["mh631_capex_totale"](-5.0, 20.0)

    def test_biomassa_e_ts(self):
        assert _F["mh631_biomassa_t_annue"](MWH_DEMO, 1.2) == TB_DEMO
        assert _F["mh631_costo_biomassa"](TB_DEMO, 80.0) == CB_DEMO
        assert _F["mh631_costo_ts"](CAT_DEMO, 30.0) == CTS_DEMO
        assert _F["mh631_costo_biomassa"](TB_DEMO, 0.0) == 0.0

    def test_costi_ricavi(self):
        assert _F["mh631_costi_totali"](CAP_DEMO, CB_DEMO,
                                        CTS_DEMO) == pytest.approx(TOT_DEMO)
        assert _F["mh631_ricavi_energia"](MWH_DEMO, 90.0) == REL_DEMO
        assert _F["mh631_ricavi_crediti"](NET_DEMO, 120.0) == \
            pytest.approx(RC_DEMO)
        assert _F["mh631_margine"](REL_DEMO, RC_DEMO,
                                   TOT_DEMO) == pytest.approx(MG_DEMO)
        # margine positivo se il credito paga la rimozione
        assert _F["mh631_margine"](REL_DEMO,
                                   _F["mh631_ricavi_crediti"](NET_DEMO,
                                                              300.0),
                                   TOT_DEMO) > 0

    def test_costo_netto(self):
        assert _F["mh631_costo_netto_rimozione"](TOT_DEMO, REL_DEMO,
                                                 NET_DEMO) == \
            pytest.approx(CN_DEMO)
        assert _F["mh631_costo_netto_rimozione"](TOT_DEMO, REL_DEMO,
                                                 0.0) is None
        with pytest.raises(ValueError):
            _F["mh631_costo_netto_rimozione"](-1.0, REL_DEMO, NET_DEMO)

    def test_verdetto(self):
        v = _F["mh631_verdetto"](CN_DEMO, 120.0)
        assert v["verdetto"] == "NON_CONVIENTE"
        assert v["gap"] == pytest.approx(GAP_DEMO)
        assert "283.61" in v["msg"]  # pareggio citato nel msg
        v2 = _F["mh631_verdetto"](100.0, 120.0)
        assert v2["verdetto"] == "CONVIENTE"
        assert v2["gap"] == pytest.approx(-20.0)
        v3 = _F["mh631_verdetto"](130.0, 120.0)
        assert v3["verdetto"] == "MARGINALE"
        v4 = _F["mh631_verdetto"](None, 120.0)
        assert v4["verdetto"] == "NON_CALCOLABILE"
        with pytest.raises(ValueError):
            _F["mh631_verdetto"](CN_DEMO, -1.0)

    def test_sensibilita(self):
        rows = _F["mh631_sensibilita"](
            20.0, 8000.0, 0.85, 0.40, 0.9, 0.02, 4.5e6, 7.0, 25.0,
            4.0, 1.2, 30.0, 90.0, [60.0, 80.0], [100.0, 140.0])
        assert len(rows) == 4
        r00 = rows[0]
        assert r00["prezzo_biomassa_eur_t"] == 60.0
        assert r00["prezzo_credito_eur_t"] == 100.0
        # riga hand-computed: biomassa 163200 x 60 = 9.792.000
        tot60 = CAP_DEMO + 9792000.0 + CTS_DEMO
        u00 = (tot60 - REL_DEMO) / NET_DEMO
        assert r00["costo_netto_eur_t"] == pytest.approx(u00)
        assert r00["costo_netto_eur_t"] == \
            pytest.approx(215.58095216961587)
        assert r00["verdetto"] == "NON_CONVIENTE"
        r13 = rows[3]
        assert r13["prezzo_biomassa_eur_t"] == 80.0
        assert r13["prezzo_credito_eur_t"] == 140.0
        assert r13["costo_netto_eur_t"] == pytest.approx(CN_DEMO)
        assert r13["verdetto"] == "NON_CONVIENTE"

    def test_demo(self):
        d = DEMO
        assert d["potenza_mw"] == 20.0
        assert d["ore_annue"] == 8000.0
        assert d["prezzo_credito_eur_t"] == 120.0

    def test_catena_completa(self):
        d = dict(DEMO)
        mwh = _F["mh631_mwh_annui"](d["potenza_mw"], d["ore_annue"],
                                    d["fattore_capacita_pct"] / 100.0)
        bio = _F["mh631_co2_biogenica_t"](mwh, d["ef_biogenica_t_mwh"])
        cat = _F["mh631_co2_catturata_t"](bio, d["eta_cattura_pct"] / 100.0)
        net = _F["mh631_rimozione_netta_t"](cat,
                                            d["perdita_ts_pct"] / 100.0)
        crf = _F["mh631_crf"](d["tasso_pct"], d["anni"])
        cx = _F["mh631_capex_totale"](d["capex_mw_meur"] * 1e6,
                                      d["potenza_mw"])
        cap = _F["mh631_costo_capitale_annuo"](cx, crf, d["opex_pct"])
        tb = _F["mh631_biomassa_t_annue"](mwh, d["t_biomassa_per_mwh"])
        cb = _F["mh631_costo_biomassa"](tb, d["prezzo_biomassa_eur_t"])
        cts = _F["mh631_costo_ts"](cat, d["costo_ts_eur_t"])
        tot = _F["mh631_costi_totali"](cap, cb, cts)
        rel = _F["mh631_ricavi_energia"](mwh, d["prezzo_el_eur_mwh"])
        cn = _F["mh631_costo_netto_rimozione"](tot, rel, net)
        rc = _F["mh631_ricavi_crediti"](net, d["prezzo_credito_eur_t"])
        mg = _F["mh631_margine"](rel, rc, tot)
        ver = _F["mh631_verdetto"](cn, d["prezzo_credito_eur_t"])
        assert mwh == pytest.approx(MWH_DEMO)
        assert bio == pytest.approx(BIO_DEMO)
        assert cat == pytest.approx(CAT_DEMO)
        assert net == pytest.approx(NET_DEMO)
        assert crf == pytest.approx(CRF_DEMO)
        assert cx == pytest.approx(CX_DEMO)
        assert cap == pytest.approx(CAP_DEMO)
        assert tb == pytest.approx(TB_DEMO)
        assert cb == pytest.approx(CB_DEMO)
        assert cts == pytest.approx(CTS_DEMO)
        assert tot == pytest.approx(TOT_DEMO)
        assert rel == pytest.approx(REL_DEMO)
        assert cn == pytest.approx(CN_DEMO)
        assert rc == pytest.approx(RC_DEMO)
        assert mg == pytest.approx(MG_DEMO)
        assert ver["verdetto"] == "NON_CONVIENTE"


class TestW631Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def _ui(self):
        return self._src().split("with tab631:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 671
        assert TITLE631 in titles
        assert TITLE631 in titles

    def test_chain(self):
        assert ", tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671 = st.tabs([" in self._src()
        assert "with tab631:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st631_[a-z0-9_]+", self._ui()))
        attese = {"st631_pot", "st631_ore", "st631_cf", "st631_ef",
                  "st631_eta", "st631_leak", "st631_cx", "st631_tasso",
                  "st631_anni", "st631_ox", "st631_cons", "st631_pbio",
                  "st631_pts", "st631_pel", "st631_pcr", "st631_tab",
                  "st631_graf", "st631_go", "st631_fig", "st631_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st631_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        sec = self._src().split('# W631 (22/10/2026)')[1]
        sec = sec.split('# W630 (22/10/2026)')[0]
        for w in ("api_key", "apikey", "password", "passwd", "secret",
                  "token"):
            assert w not in sec.lower(), f"sospetto segreto: {w}"
