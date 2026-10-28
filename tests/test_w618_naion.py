"""Test tab618 "🔋🧂 Batterie al sodio (Na-ion): l'accumulo senza litio conviene?".

I valori della demo sono calcolati a mano: sistema da 1 MWh utile,
300 cicli/anno, DoD 90 % (270.000 kWh/anno scaricati); Na-ion capex
170 eur/kWh, 4.000 cicli, RTE 90 % -> vita 13,33 anni, LCOS
0,1682689522975387 eur/kWh; LFP capex 220 eur/kWh, 6.000 cicli,
RTE 93 % -> vita 15 anni (calendario), LCOS 0,18213931304363584
eur/kWh; verdetto SODIO_CONVIENE (risparmio 7,6 % > 5 %).
"""

import re
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh618_num", "mh618_nneg", "mh618_pos", "mh618_frac01",
           "mh618_crf", "mh618_anni_vita", "mh618_energia_annua",
           "mh618_lcos", "mh618_verdetto", "mh618_sensibilita",
           "mh618_demo")

TITLE618 = "🔋🧂 Batterie al sodio (Na-ion): l'accumulo senza litio conviene?"

# Demo: 1 MWh, 300 cicli/anno, DoD 90 %, vita calendario 15 anni,
# ricarica 0,08 eur/kWh, tasso 6 %, opex 1,5 % capex/anno
DEMO = _F["mh618_demo"]()
ENERGIA = 270000.0                   # 1000*300*0,9
ANNI_NA = 13.333333333333334        # min(4000/300, 15)
ANNI_LFP = 15.0                     # min(6000/300, 15) -> calendario
LCOS_NA = 0.1682689522975387
LCOS_LFP = 0.18213931304363584


class TestW618Validatori:
    def test_num(self):
        assert _F["mh618_num"](3, "x") == 3.0
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh618_num"](bad, "x")

    def test_nneg(self):
        assert _F["mh618_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh618_nneg"](-1.0, "x")

    def test_pos(self):
        with pytest.raises(ValueError):
            _F["mh618_pos"](0.0, "x")
        with pytest.raises(ValueError):
            _F["mh618_pos"](-2.0, "x")

    def test_frac01(self):
        assert _F["mh618_frac01"](1.0, "x") == 1.0
        assert _F["mh618_frac01"](0.0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh618_frac01"](1.5, "x")


class TestW618Calcoli:
    def test_crf(self):
        assert _F["mh618_crf"](0.0, 10.0) == pytest.approx(0.1)
        # 6 % su 13,333 anni (vita Na-ion demo)
        assert _F["mh618_crf"](0.06, ANNI_NA) == \
            pytest.approx(0.11107421835491436)
        # 6 % su 15 anni (vita LFP demo)
        assert _F["mh618_crf"](0.06, 15.0) == \
            pytest.approx(0.10296276395531265)
        with pytest.raises(ValueError):
            _F["mh618_crf"](-0.01, 10.0)
        with pytest.raises(ValueError):
            _F["mh618_crf"](0.06, 0.0)

    def test_anni_vita(self):
        # limitato dai cicli
        assert _F["mh618_anni_vita"](4000.0, 300.0, 15.0) == \
            pytest.approx(ANNI_NA)
        # limitato dal calendario
        assert _F["mh618_anni_vita"](6000.0, 300.0, 15.0) == ANNI_LFP
        assert _F["mh618_anni_vita"](9000.0, 300.0, 15.0) == ANNI_LFP
        with pytest.raises(ValueError):
            _F["mh618_anni_vita"](4000.0, 0.0, 15.0)

    def test_energia_annua(self):
        assert _F["mh618_energia_annua"](1000.0, 300.0, 0.9) == ENERGIA
        assert _F["mh618_energia_annua"](1000.0, 300.0, 0.0) == 0.0
        with pytest.raises(ValueError):
            _F["mh618_energia_annua"](1000.0, -5.0, 0.9)

    def test_lcos_demo(self):
        d = DEMO
        na = _F["mh618_lcos"](d["capacita_kwh"], d["cicli_anno"], d["dod"],
                              d["capex_na_eur_kwh"], d["cicli_vita_na"],
                              d["vita_calendario"], d["rte_na"],
                              d["prezzo_ricarica_eur_kwh"], d["tasso"],
                              d["opex_frac"])
        lfp = _F["mh618_lcos"](d["capacita_kwh"], d["cicli_anno"], d["dod"],
                               d["capex_lfp_eur_kwh"], d["cicli_vita_lfp"],
                               d["vita_calendario"], d["rte_lfp"],
                               d["prezzo_ricarica_eur_kwh"], d["tasso"],
                               d["opex_frac"])
        assert na == pytest.approx(LCOS_NA)
        assert lfp == pytest.approx(LCOS_LFP)
        assert na < lfp

    def test_lcos_errori(self):
        d = DEMO
        base = dict(capacita_kwh=d["capacita_kwh"], cicli_anno=d["cicli_anno"],
                    dod=d["dod"], capex_eur_kwh=d["capex_na_eur_kwh"],
                    cicli_vita=d["cicli_vita_na"],
                    vita_calendario=d["vita_calendario"], rte=d["rte_na"],
                    prezzo_ricarica_eur_kwh=d["prezzo_ricarica_eur_kwh"],
                    tasso=d["tasso"], opex_frac=d["opex_frac"])

        def lcos(**kw):
            kw2 = dict(base)
            kw2.update(kw)
            return _F["mh618_lcos"](**kw2)

        # RTE 0 o > 1 -> errore (non divisione per zero)
        with pytest.raises(ValueError):
            lcos(rte=0.0)
        with pytest.raises(ValueError):
            lcos(rte=1.5)
        # energia annua nulla -> errore esplicito
        with pytest.raises(ValueError):
            lcos(dod=0.0)
        with pytest.raises(ValueError):
            lcos(capex_eur_kwh=-1.0)
        # piu' cicli/anno -> LCOS piu' basso (stesso capex spalmato)
        assert lcos(cicli_anno=400.0) < lcos(cicli_anno=200.0)


class TestW618Verdetto:
    def test_demo_sodio_conviene(self):
        v = _F["mh618_verdetto"](LCOS_NA, LCOS_LFP)
        assert v["verdetto"] == "SODIO_CONVIENE"
        assert v["risparmio_pct"] == pytest.approx(7.615248193438711)
        assert v["lcos_na"] == pytest.approx(LCOS_NA)

    def test_litio_conviene(self):
        v = _F["mh618_verdetto"](0.20, 0.18)
        assert v["verdetto"] == "LITIO_CONVIENE"
        assert v["risparmio_pct"] < 0

    def test_parita(self):
        v = _F["mh618_verdetto"](0.18, 0.182)
        assert v["verdetto"] == "PARITA"
        # appena dentro le soglie del 5 % (evita i bordi float)
        v2 = _F["mh618_verdetto"](0.189, 0.20)
        assert v2["verdetto"] == "SODIO_CONVIENE"
        v3 = _F["mh618_verdetto"](0.211, 0.20)
        assert v3["verdetto"] == "LITIO_CONVIENE"
        with pytest.raises(ValueError):
            _F["mh618_verdetto"](0.0, 0.18)


class TestW618Demo:
    def test_demo_end_to_end(self):
        d = DEMO
        e = _F["mh618_energia_annua"](d["capacita_kwh"], d["cicli_anno"],
                                      d["dod"])
        an = _F["mh618_anni_vita"](d["cicli_vita_na"], d["cicli_anno"],
                                    d["vita_calendario"])
        al = _F["mh618_anni_vita"](d["cicli_vita_lfp"], d["cicli_anno"],
                                    d["vita_calendario"])
        na = _F["mh618_lcos"](d["capacita_kwh"], d["cicli_anno"], d["dod"],
                              d["capex_na_eur_kwh"], d["cicli_vita_na"],
                              d["vita_calendario"], d["rte_na"],
                              d["prezzo_ricarica_eur_kwh"], d["tasso"],
                              d["opex_frac"])
        lfp = _F["mh618_lcos"](d["capacita_kwh"], d["cicli_anno"], d["dod"],
                               d["capex_lfp_eur_kwh"], d["cicli_vita_lfp"],
                               d["vita_calendario"], d["rte_lfp"],
                               d["prezzo_ricarica_eur_kwh"], d["tasso"],
                               d["opex_frac"])
        assert e == ENERGIA
        assert an == pytest.approx(ANNI_NA)
        assert al == ANNI_LFP
        assert na == pytest.approx(LCOS_NA)
        assert lfp == pytest.approx(LCOS_LFP)
        v = _F["mh618_verdetto"](na, lfp)
        assert v["verdetto"] == "SODIO_CONVIENE"


class TestW618Sensitivita:
    def _args(self):
        d = DEMO
        return (d["capacita_kwh"], d["cicli_anno"], d["dod"],
                d["capex_lfp_eur_kwh"], d["cicli_vita_lfp"], d["rte_lfp"],
                d["vita_calendario"], d["prezzo_ricarica_eur_kwh"],
                d["tasso"], d["opex_frac"],
                d["cicli_vita_na"], d["rte_na"])

    def test_griglia(self):
        (cap, ca, dod, ckl, cvl, rl, vc, pr, t, op, cvn,
         rn) = self._args()
        rows = _F["mh618_sensibilita"](cap, ca, dod, ckl, cvl, rl, vc,
                                       pr, t, op, [170.0], [300.0],
                                       cvn, rn)
        assert len(rows) == 1
        r = rows[0]
        assert r["capex_na_eur_kwh"] == 170.0
        assert r["cicli_anno"] == 300.0
        assert r["lcos_na"] == pytest.approx(LCOS_NA)
        assert r["lcos_lfp"] == pytest.approx(LCOS_LFP)
        assert r["vincitore"] == "Na-ion"

    def test_vincitore_cambia_col_capex(self):
        (cap, ca, dod, ckl, cvl, rl, vc, pr, t, op, cvn,
         rn) = self._args()
        rows = _F["mh618_sensibilita"](cap, ca, dod, ckl, cvl, rl, vc,
                                       pr, t, op, [120.0, 500.0],
                                       [300.0], cvn, rn)
        assert rows[0]["vincitore"] == "Na-ion"
        assert rows[1]["vincitore"] == "LFP"
        assert rows[1]["lcos_na"] > rows[1]["lcos_lfp"]

    def test_piu_cicli_lcos_piu_basso(self):
        (cap, ca, dod, ckl, cvl, rl, vc, pr, t, op, cvn,
         rn) = self._args()
        rows = _F["mh618_sensibilita"](cap, ca, dod, ckl, cvl, rl, vc,
                                       pr, t, op, [170.0],
                                       [200.0, 400.0], cvn, rn)
        assert rows[1]["lcos_na"] < rows[0]["lcos_na"]

    def test_liste_vuote(self):
        (cap, ca, dod, ckl, cvl, rl, vc, pr, t, op, cvn,
         rn) = self._args()
        with pytest.raises(ValueError):
            _F["mh618_sensibilita"](cap, ca, dod, ckl, cvl, rl, vc, pr,
                                    t, op, [], [300.0], cvn, rn)
        with pytest.raises(ValueError):
            _F["mh618_sensibilita"](cap, ca, dod, ckl, cvl, rl, vc, pr,
                                    t, op, [170.0], [], cvn, rn)


class TestW618Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def _ui(self):
        return self._src().split("with tab618:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 762
        assert TITLE618 in titles
        assert TITLE618 in titles

    def test_chain(self):
        assert ", tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762 = st.tabs([" in self._src()
        assert "with tab618:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st618_[a-z0-9_]+", self._ui()))
        attese = {"st618_cap", "st618_cic", "st618_dod", "st618_ckna",
                  "st618_cvna", "st618_rtna", "st618_cklf", "st618_cvlf",
                  "st618_rtlf", "st618_vc", "st618_pr", "st618_tasso",
                  "st618_opex", "st618_tab", "st618_graf", "st618_go",
                  "st618_fig", "st618_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st618_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        sec = self._src().split('# W618 (21/10/2026)')[1]
        sec = sec.split('# W617 (21/10/2026)')[0]
        for w in ("api_key", "apikey", "password", "passwd", "secret",
                  "token"):
            assert w not in sec.lower(), f"sospetto segreto: {w}"
