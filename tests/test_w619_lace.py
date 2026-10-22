"""Test tab619 "📐 LACE: il costo che la rete evita (il vero valore di un impianto)".

Demo calcolata a mano: FV utility-scale 100 MW, CF 14 % ->
energia annua 122.640 MWh; capex 800 eur/kW (80 Meur), opex fisso
15 eur/kW/anno, vita 25 anni, WACC 6 % -> CRF 0,07822671821227395 ->
LCOE 63,25943784231829 eur/MWh. Prezzo medio 85 eur/MWh x value
factor 0,9 = 76,5 di cattura; ELCC 15 % x 100 MW x 60.000 eur/MW/anno
/ 122.640 MWh = 7,338551859099804 eur/MWh di valore capacita' ->
LACE 83,83855185909981; netto +20,579114016781517 -> NETTO_POSITIVO.
"""

import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh619_num", "mh619_nneg", "mh619_pos", "mh619_frac01",
           "mh619_crf", "mh619_energia_annua", "mh619_lcoe",
           "mh619_prezzo_cattura", "mh619_valore_capacita_mwh",
           "mh619_lace", "mh619_valore_netto", "mh619_verdetto",
           "mh619_sensibilita", "mh619_demo")

TITLE619 = "📐 LACE: il costo che la rete evita (il vero valore di un impianto)"

DEMO = _F["mh619_demo"]()
ENERGIA = 122640.0
CRF_DEMO = 0.07822671821227395
LCOE_DEMO = 63.25943784231829
CATTURA_DEMO = 76.5
VALCAP_DEMO = 7.338551859099804
LACE_DEMO = 83.83855185909981
NETTO_DEMO = 20.579114016781517


class TestW619Validatori:
    def test_num(self):
        assert _F["mh619_num"](3, "x") == 3.0
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh619_num"](bad, "x")

    def test_nneg(self):
        assert _F["mh619_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh619_nneg"](-1.0, "x")

    def test_pos(self):
        with pytest.raises(ValueError):
            _F["mh619_pos"](0.0, "x")
        with pytest.raises(ValueError):
            _F["mh619_pos"](-2.0, "x")

    def test_frac01(self):
        assert _F["mh619_frac01"](1.0, "x") == 1.0
        assert _F["mh619_frac01"](0.0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh619_frac01"](1.5, "x")


class TestW619Calcoli:
    def test_crf(self):
        assert _F["mh619_crf"](0.0, 10.0) == pytest.approx(0.1)
        assert _F["mh619_crf"](0.06, 25.0) == pytest.approx(CRF_DEMO)
        with pytest.raises(ValueError):
            _F["mh619_crf"](-0.01, 10.0)
        with pytest.raises(ValueError):
            _F["mh619_crf"](0.06, 0.0)

    def test_energia_annua(self):
        assert _F["mh619_energia_annua"](100.0, 0.14) == pytest.approx(ENERGIA)
        assert _F["mh619_energia_annua"](100.0, 0.0) == 0.0
        with pytest.raises(ValueError):
            _F["mh619_energia_annua"](100.0, 1.2)
        with pytest.raises(ValueError):
            _F["mh619_energia_annua"](0.0, 0.14)

    def test_lcoe_demo(self):
        d = DEMO
        lc = _F["mh619_lcoe"](d["potenza_mw"], d["cf"],
                              d["capex_eur_kw"],
                              d["opex_fisso_eur_kw_anno"],
                              d["opex_var_eur_mwh"], d["vita_anni"],
                              d["wacc"])
        assert lc == pytest.approx(LCOE_DEMO)

    def test_lcoe_errori(self):
        d = DEMO

        def lcoe(**kw):
            kw2 = dict(potenza_mw=d["potenza_mw"], cf=d["cf"],
                       capex_eur_kw=d["capex_eur_kw"],
                       opex_fisso_eur_kw_anno=d["opex_fisso_eur_kw_anno"],
                       opex_var_eur_mwh=d["opex_var_eur_mwh"],
                       vita_anni=d["vita_anni"], wacc=d["wacc"])
            kw2.update(kw)
            return _F["mh619_lcoe"](**kw2)

        # CF = 0 -> energia nulla -> errore esplicito
        with pytest.raises(ValueError):
            lcoe(cf=0.0)
        with pytest.raises(ValueError):
            lcoe(capex_eur_kw=-1.0)
        with pytest.raises(ValueError):
            lcoe(wacc=-0.01)
        # capex piu' alto -> LCOE piu' alto
        assert lcoe(capex_eur_kw=1200.0) > lcoe(capex_eur_kw=800.0)
        # CF piu' alto -> LCOE piu' basso
        assert lcoe(cf=0.20) < lcoe(cf=0.14)
        # opex variabile si somma 1:1
        assert lcoe(opex_var_eur_mwh=10.0) == \
            pytest.approx(lcoe() + 10.0)

    def test_prezzo_cattura(self):
        assert _F["mh619_prezzo_cattura"](85.0, 0.9) == CATTURA_DEMO
        assert _F["mh619_prezzo_cattura"](85.0, 0.0) == 0.0
        with pytest.raises(ValueError):
            _F["mh619_prezzo_cattura"](-1.0, 0.9)

    def test_valore_capacita(self):
        vc = _F["mh619_valore_capacita_mwh"](100.0, 0.15, 60000.0, ENERGIA)
        assert vc == pytest.approx(VALCAP_DEMO)
        # ELCC 0 -> nessun valore di capacita'
        assert _F["mh619_valore_capacita_mwh"](100.0, 0.0, 60000.0,
                                              ENERGIA) == 0.0
        # energia nulla -> errore (non divisione per zero)
        with pytest.raises(ValueError):
            _F["mh619_valore_capacita_mwh"](100.0, 0.15, 60000.0, 0.0)
        with pytest.raises(ValueError):
            _F["mh619_valore_capacita_mwh"](100.0, 1.5, 60000.0, ENERGIA)

    def test_lace_e_netto(self):
        la = _F["mh619_lace"](CATTURA_DEMO, VALCAP_DEMO)
        assert la == pytest.approx(LACE_DEMO)
        nt = _F["mh619_valore_netto"](la, LCOE_DEMO)
        assert nt == pytest.approx(NETTO_DEMO)
        assert nt > 0
        with pytest.raises(ValueError):
            _F["mh619_lace"](-1.0, VALCAP_DEMO)


class TestW619Verdetto:
    def test_demo_netto_positivo(self):
        v = _F["mh619_verdetto"](LACE_DEMO, LCOE_DEMO)
        assert v["verdetto"] == "NETTO_POSITIVO"
        assert v["netto"] == pytest.approx(NETTO_DEMO)
        assert "msg" in v and v["msg"]

    def test_distrugge_valore(self):
        v = _F["mh619_verdetto"](60.0, 80.0)
        assert v["verdetto"] == "DISTRUGGE_VALORE"
        assert v["netto"] == pytest.approx(-20.0)

    def test_marginale(self):
        v = _F["mh619_verdetto"](70.0, 72.0)
        assert v["verdetto"] == "MARGINALE"
        # bordi della soglia di materialita' (evita i bordi float)
        assert _F["mh619_verdetto"](75.0, 70.0)["verdetto"] == \
            "NETTO_POSITIVO"
        assert _F["mh619_verdetto"](65.0, 70.0)["verdetto"] == \
            "DISTRUGGE_VALORE"
        # soglia custom
        v2 = _F["mh619_verdetto"](70.0, 72.0, soglia=1.0)
        assert v2["verdetto"] == "DISTRUGGE_VALORE"
        with pytest.raises(ValueError):
            _F["mh619_verdetto"](70.0, 72.0, soglia=0.0)

    def test_verdetto_errori(self):
        with pytest.raises(ValueError):
            _F["mh619_verdetto"](-1.0, LCOE_DEMO)


class TestW619Demo:
    def test_demo_end_to_end(self):
        d = DEMO
        e = _F["mh619_energia_annua"](d["potenza_mw"], d["cf"])
        lc = _F["mh619_lcoe"](d["potenza_mw"], d["cf"],
                              d["capex_eur_kw"],
                              d["opex_fisso_eur_kw_anno"],
                              d["opex_var_eur_mwh"], d["vita_anni"],
                              d["wacc"])
        pc = _F["mh619_prezzo_cattura"](d["prezzo_medio"],
                                       d["value_factor"])
        vc = _F["mh619_valore_capacita_mwh"](d["potenza_mw"], d["elcc"],
                                            d["costo_cap_eur_mw_anno"], e)
        la = _F["mh619_lace"](pc, vc)
        nt = _F["mh619_valore_netto"](la, lc)
        v = _F["mh619_verdetto"](la, lc)
        assert e == pytest.approx(ENERGIA)
        assert lc == pytest.approx(LCOE_DEMO)
        assert pc == CATTURA_DEMO
        assert vc == pytest.approx(VALCAP_DEMO)
        assert la == pytest.approx(LACE_DEMO)
        assert nt == pytest.approx(NETTO_DEMO)
        assert v["verdetto"] == "NETTO_POSITIVO"


class TestW619Sensitivita:
    def _args(self):
        d = DEMO
        return (d["potenza_mw"], d["cf"], d["capex_eur_kw"],
                d["opex_fisso_eur_kw_anno"], d["opex_var_eur_mwh"],
                d["vita_anni"], d["wacc"], d["value_factor"], d["elcc"],
                d["costo_cap_eur_mw_anno"])

    def test_griglia(self):
        rows = _F["mh619_sensibilita"](*self._args(), [85.0])
        assert len(rows) == 1
        r = rows[0]
        assert r["prezzo_medio_eur_mwh"] == 85.0
        assert r["lace"] == pytest.approx(LACE_DEMO)
        assert r["lcoe"] == pytest.approx(LCOE_DEMO)
        assert r["valore_netto"] == pytest.approx(NETTO_DEMO)
        assert r["giudizio"] == "OK"

    def test_giudizio_cambia_col_prezzo(self):
        rows = _F["mh619_sensibilita"](*self._args(), [40.0, 85.0, 140.0])
        # a 40 eur/MWh il LACE crolla sotto il LCOE
        assert rows[0]["giudizio"] == "KO"
        assert rows[0]["lace"] < rows[0]["lcoe"]
        assert rows[1]["giudizio"] == "OK"
        assert rows[2]["giudizio"] == "OK"
        assert rows[2]["lace"] > rows[1]["lace"] > rows[0]["lace"]
        # il LCOE e' piatto: non dipende dal prezzo
        assert rows[0]["lcoe"] == rows[1]["lcoe"] == rows[2]["lcoe"]

    def test_lista_vuota(self):
        with pytest.raises(ValueError):
            _F["mh619_sensibilita"](*self._args(), [])


class TestW619Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def _ui(self):
        return self._src().split("with tab619:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 637
        assert TITLE619 in titles
        assert TITLE619 in titles

    def test_chain(self):
        assert ", tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637 = st.tabs([" in self._src()
        assert "with tab619:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st619_[a-z0-9_]+", self._ui()))
        attese = {"st619_pot", "st619_cf", "st619_ck", "st619_of",
                  "st619_ov", "st619_vita", "st619_wacc", "st619_pm",
                  "st619_vf", "st619_elcc", "st619_cc", "st619_tab",
                  "st619_graf", "st619_go", "st619_fig", "st619_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st619_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        sec = self._src().split('# W619 (21/10/2026)')[1]
        sec = sec.split('# W618 (21/10/2026)')[0]
        for w in ("api_key", "apikey", "password", "passwd", "secret",
                  "token"):
            assert w not in sec.lower(), f"sospetto segreto: {w}"
