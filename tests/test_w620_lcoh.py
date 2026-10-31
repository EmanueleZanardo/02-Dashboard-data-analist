"""Test tab620 "🧪 LCOH: il costo dell'idrogeno verde (quando l'elettrolisi conviene)".

Demo calcolata a mano: PEM 10 MW, 5000 ore/anno, consumo 55 kWh/kg ->
909.090,9091 kg/anno, 50.000 MWh/anno; capex 1200 eur/kW (12 Meur) x
CRF(7 %, 20 a) 0,09439292574325567 = 1.132.715,1089 eur/anno; stack 400
eur/kW (4 Meur) x CRF(7 %, 12 a) 0,12590198865502042 = 503.607,9546
eur/anno; opex fisso 4 % = 480.000; energia 50 eur/MWh = 2.500.000;
acqua 0,05 eur/kg = 45.454,5455; totale 4.661.777,6090 eur/anno ->
LCOH 5,127955369893065 eur/kg, quota energia 53,62761181865252 %.
Contro H2 grigio 2,2 eur/kg -> NON_CONVIENTE (diff +2,927955369893065);
prezzo di pareggio dell'energia -3,235552179873902 eur/MWh
(irraggiungibile con questi capex).
"""

import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh620_num", "mh620_nneg", "mh620_pos", "mh620_frac01",
           "mh620_crf", "mh620_energia_annua_mwh", "mh620_kg_annui",
           "mh620_lcoh", "mh620_prezzo_pareggio_energia",
           "mh620_verdetto", "mh620_sensibilita", "mh620_demo")

TITLE620 = ("🧪 LCOH: il costo dell'idrogeno verde "
            "(quando l'elettrolisi conviene)")

DEMO = _F["mh620_demo"]()
KG_DEMO = 909090.9090909091
ENERGIA_DEMO = 50000.0
CRF_DEMO = 0.09439292574325567
CRF_STACK_DEMO = 0.12590198865502042
CAPEX_ANN_DEMO = 1132715.108918068
STACK_ANN_DEMO = 503607.9546200817
OPEX_F_DEMO = 480000.0
C_EN_DEMO = 2500000.0
C_AQ_DEMO = 45454.545454545456
TOT_DEMO = 4661777.608992695
LCOH_DEMO = 5.127955369893065
QUOTA_EN_DEMO = 53.62761181865252
PAREGGIO_DEMO = -3.235552179873902


def _args_demo():
    d = DEMO
    return (d["potenza_mw"], d["ore_annue"], d["consumo_kwh_kg"],
            d["capex_eur_kw"], d["opex_fisso_pct"],
            d["costo_stack_eur_kw"], d["vita_stack_ore"],
            d["prezzo_energia_eur_mwh"], d["costo_acqua_eur_kg"],
            d["vita_anni"], d["wacc"])


class TestW620Validatori:
    def test_num(self):
        assert _F["mh620_num"](3, "x") == 3.0
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh620_num"](bad, "x")

    def test_nneg(self):
        assert _F["mh620_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh620_nneg"](-1.0, "x")

    def test_pos(self):
        with pytest.raises(ValueError):
            _F["mh620_pos"](0.0, "x")
        with pytest.raises(ValueError):
            _F["mh620_pos"](-2.0, "x")

    def test_frac01(self):
        assert _F["mh620_frac01"](1.0, "x") == 1.0
        assert _F["mh620_frac01"](0.0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh620_frac01"](1.5, "x")


class TestW620Calcoli:
    def test_crf(self):
        assert _F["mh620_crf"](0.0, 10.0) == pytest.approx(0.1)
        assert _F["mh620_crf"](0.07, 20.0) == pytest.approx(CRF_DEMO)
        assert _F["mh620_crf"](0.07, 12.0) == pytest.approx(
            CRF_STACK_DEMO)
        with pytest.raises(ValueError):
            _F["mh620_crf"](-0.01, 10.0)
        with pytest.raises(ValueError):
            _F["mh620_crf"](0.07, 0.0)

    def test_energia_annua(self):
        assert _F["mh620_energia_annua_mwh"](10.0, 5000.0) == \
            pytest.approx(ENERGIA_DEMO)
        with pytest.raises(ValueError):
            _F["mh620_energia_annua_mwh"](10.0, 9000.0)
        with pytest.raises(ValueError):
            _F["mh620_energia_annua_mwh"](0.0, 5000.0)

    def test_kg_annui(self):
        assert _F["mh620_kg_annui"](10.0, 5000.0, 55.0) == \
            pytest.approx(KG_DEMO)
        # consumo piu' alto = meno kg
        assert _F["mh620_kg_annui"](10.0, 5000.0, 65.0) < KG_DEMO
        with pytest.raises(ValueError):
            _F["mh620_kg_annui"](10.0, 5000.0, 0.0)
        with pytest.raises(ValueError):
            _F["mh620_kg_annui"](10.0, 9000.0, 55.0)

    def test_lcoh_demo(self):
        det = _F["mh620_lcoh"](*_args_demo())
        assert det["kg_annui"] == pytest.approx(KG_DEMO)
        assert det["energia_annua_mwh"] == pytest.approx(ENERGIA_DEMO)
        assert det["capex_ann"] == pytest.approx(CAPEX_ANN_DEMO)
        assert det["stack_ann"] == pytest.approx(STACK_ANN_DEMO)
        assert det["opex_fisso_ann"] == pytest.approx(OPEX_F_DEMO)
        assert det["costo_energia_ann"] == pytest.approx(C_EN_DEMO)
        assert det["costo_acqua_ann"] == pytest.approx(C_AQ_DEMO)
        assert det["totale_ann"] == pytest.approx(TOT_DEMO)
        assert det["lcoh"] == pytest.approx(LCOH_DEMO)
        assert det["quota_energia_pct"] == pytest.approx(QUOTA_EN_DEMO)

    def test_lcoh_energia_gratis(self):
        # con energia gratis il LCOH scende ma resta > 0
        det = _F["mh620_lcoh"](*_args_demo()[:7], 0.0,
                               *_args_demo()[8:])
        assert det["lcoh"] < LCOH_DEMO
        assert det["lcoh"] > 0.0
        assert det["quota_energia_pct"] == 0.0

    def test_lcoh_stack_zero(self):
        # stack a costo zero = niente quota sostituzione
        det = _F["mh620_lcoh"](*_args_demo()[:5], 0.0,
                               *_args_demo()[6:])
        assert det["stack_ann"] == 0.0
        assert det["lcoh"] < LCOH_DEMO

    def test_pareggio_demo(self):
        # pareggio NON prende il prezzo energia: args senza [7] + rif
        p = _F["mh620_prezzo_pareggio_energia"](
            *_args_demo()[:7], *_args_demo()[8:],
            DEMO["prezzo_riferimento_eur_kg"])
        assert p == pytest.approx(PAREGGIO_DEMO)
        assert p < 0.0  # irraggiungibile con questi capex

    def test_pareggio_raggiungibile(self):
        # capex dimezzato e stack piu' economico -> pareggio positivo
        args = list(_args_demo())
        args[3] = 500.0   # capex eur/kW
        args[5] = 150.0   # stack eur/kW
        p = _F["mh620_prezzo_pareggio_energia"](
            *args[:7], *args[8:], DEMO["prezzo_riferimento_eur_kg"])
        assert p > 0.0

    def test_verdetto(self):
        v = _F["mh620_verdetto"](LCOH_DEMO, 2.2)
        assert v["verdetto"] == "NON_CONVIENTE"
        assert v["diff"] == pytest.approx(LCOH_DEMO - 2.2)
        v2 = _F["mh620_verdetto"](2.0, 2.2)
        assert v2["verdetto"] == "CONVIENTE"
        v3 = _F["mh620_verdetto"](2.9, 2.2)
        assert v3["verdetto"] == "MARGINALE"
        v4 = _F["mh620_verdetto"](3.21, 2.2)
        assert v4["verdetto"] == "NON_CONVIENTE"
        with pytest.raises(ValueError):
            _F["mh620_verdetto"](-1.0, 2.2)

    def test_demo_keys(self):
        attese = {"potenza_mw", "ore_annue", "consumo_kwh_kg",
                  "capex_eur_kw", "opex_fisso_pct",
                  "costo_stack_eur_kw", "vita_stack_ore",
                  "prezzo_energia_eur_mwh", "costo_acqua_eur_kg",
                  "vita_anni", "wacc", "prezzo_riferimento_eur_kg"}
        assert set(DEMO.keys()) == attese


class TestW620Sensibilita:
    def _args(self):
        d = DEMO
        return (d["potenza_mw"], d["consumo_kwh_kg"], d["capex_eur_kw"],
                d["opex_fisso_pct"], d["costo_stack_eur_kw"],
                d["vita_stack_ore"], d["costo_acqua_eur_kg"],
                d["vita_anni"], d["wacc"],
                d["prezzo_riferimento_eur_kg"])

    def test_griglia(self):
        rows = _F["mh620_sensibilita"](*self._args(),
                                       [20.0, 50.0, 80.0],
                                       [3000.0, 5000.0])
        assert len(rows) == 6
        # a parita' di ore, piu' prezzo energia = LCOH piu' alto
        r3000 = [r for r in rows if r["ore_annue"] == 3000.0]
        assert r3000[2]["lcoh"] > r3000[1]["lcoh"] > r3000[0]["lcoh"]
        # a parita' di prezzo, piu' ore = LCOH piu' basso
        r50 = [r for r in rows if r["prezzo_energia_eur_mwh"] == 50.0]
        assert r50[0]["lcoh"] > r50[1]["lcoh"]
        assert set(r["giudizio"] for r in rows) <= \
            {"CONVIENTE", "MARGINALE", "NON_CONVIENTE"}

    def test_demo_in_griglia(self):
        rows = _F["mh620_sensibilita"](*self._args(), [50.0], [5000.0])
        assert rows[0]["lcoh"] == pytest.approx(LCOH_DEMO)
        assert rows[0]["giudizio"] == "NON_CONVIENTE"

    def test_liste_vuote(self):
        with pytest.raises(ValueError):
            _F["mh620_sensibilita"](*self._args(), [], [5000.0])
        with pytest.raises(ValueError):
            _F["mh620_sensibilita"](*self._args(), [50.0], [])


class TestW620Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def _ui(self):
        return self._src().split("with tab620:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 830
        assert TITLE620 in titles
        assert TITLE620 in titles

    def test_chain(self):
        assert ", tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790, tab791, tab792, tab793, tab794, tab795, tab796, tab797, tab798, tab799, tab800, tab801, tab802, tab803, tab804, tab805, tab806, tab807, tab808, tab809, tab810, tab811, tab812, tab813, tab814, tab815, tab816, tab817, tab818, tab819, tab820, tab821, tab822, tab823, tab824, tab825, tab826, tab827, tab828, tab829, tab830 = st.tabs([" in self._src()
        assert "with tab620:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st620_[a-z0-9_]+", self._ui()))
        attese = {"st620_pot", "st620_ore", "st620_cons", "st620_ck",
                  "st620_of", "st620_cs", "st620_vs", "st620_vita",
                  "st620_wacc", "st620_pe", "st620_acq", "st620_rif",
                  "st620_tab", "st620_graf", "st620_go", "st620_fig",
                  "st620_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st620_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        sec = self._src().split('# W620 (21/10/2026)')[1]
        sec = sec.split('# W619 (21/10/2026)')[0]
        for w in ("api_key", "apikey", "password", "passwd", "secret",
                  "token"):
            assert w not in sec.lower(), f"sospetto segreto: {w}"
