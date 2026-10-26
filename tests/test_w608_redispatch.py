"""Test tab608 "⚡🔀 Redispatch: costi e ottimo della congestione".

Tutti i valori attesi sono calcolati a mano nei commenti (aritmetica
indipendente dagli helper) e contro-verificati con gli helper stessi.
"""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh608_num", "mh608_nneg", "mh608_pos", "mh608_volume",
           "mh608_spread", "mh608_costo_redispatch",
           "mh608_costo_curtailment", "mh608_risparmio",
           "mh608_costo_unitario", "mh608_verdetto",
           "mh608_sensibilita_flusso", "mh608_demo")

TITLE608 = "⚡🔀 Redispatch: costi e ottimo della congestione"

DEMO = _F["mh608_demo"]()
# Demo: flusso 1000 MW, capacita' 800 MW, 6 ore -> volume = 200*6 = 1200 MWh
# spread = 60 - 40 = 20 EUR/MWh
# costo_rd = 1200 * 20 = 24000 EUR
# costo_cu = 1200 * 40 = 48000 EUR
# risparmio = 48000 - 24000 = 24000 EUR -> REDISPATCH_CONVIENE
# unitario = 24000 / 1200 = 20 EUR/MWh (= spread)
VOL = 1200.0
SPREAD = 20.0
COSTO_RD = 24000.0
COSTO_CU = 48000.0
RISPARMIO = 24000.0
UNITARIO = 20.0


class TestW608Validatori:
    def test_num(self):
        assert _F["mh608_num"](3, "x") == 3.0
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh608_num"](bad, "x")

    def test_nneg_pos(self):
        assert _F["mh608_nneg"](0, "x") == 0.0
        assert _F["mh608_pos"](0.5, "x") == 0.5
        with pytest.raises(ValueError):
            _F["mh608_nneg"](-1, "x")
        with pytest.raises(ValueError):
            _F["mh608_pos"](0, "x")


class TestW608Volume:
    def test_demo(self):
        d = DEMO
        assert _F["mh608_volume"](d["flusso"], d["capacita"], d["ore"]) \
            == pytest.approx(VOL)

    def test_nessuna_congestione(self):
        assert _F["mh608_volume"](700.0, 800.0, 6.0) == 0.0
        assert _F["mh608_volume"](800.0, 800.0, 6.0) == 0.0
        assert _F["mh608_volume"](1000.0, 800.0, 0.0) == 0.0

    def test_degeneri(self):
        with pytest.raises(ValueError):  # capacita' nulla
            _F["mh608_volume"](1000.0, 0.0, 6.0)
        with pytest.raises(ValueError):  # flusso negativo
            _F["mh608_volume"](-10.0, 800.0, 6.0)


class TestW608Costi:
    def test_spread(self):
        d = DEMO
        assert _F["mh608_spread"](d["p_monte"], d["p_valle"]) \
            == pytest.approx(SPREAD)
        # spread negativo: prezzi invertiti
        assert _F["mh608_spread"](50.0, 30.0) == pytest.approx(-20.0)

    def test_costo_redispatch(self):
        d = DEMO
        cr = _F["mh608_costo_redispatch"](VOL, d["p_monte"], d["p_valle"])
        assert cr == pytest.approx(COSTO_RD)
        # spread negativo -> il redispatch rende
        cr2 = _F["mh608_costo_redispatch"](VOL, 50.0, 30.0)
        assert cr2 == pytest.approx(-24000.0)

    def test_costo_curtailment(self):
        cc = _F["mh608_costo_curtailment"](VOL, 40.0)
        assert cc == pytest.approx(COSTO_CU)
        assert _F["mh608_costo_curtailment"](0.0, 40.0) == 0.0

    def test_risparmio(self):
        assert _F["mh608_risparmio"](COSTO_RD, COSTO_CU) \
            == pytest.approx(RISPARMIO)
        # caso dove il curtailment conviene
        assert _F["mh608_risparmio"](96000.0, 48000.0) \
            == pytest.approx(-48000.0)

    def test_costo_unitario(self):
        assert _F["mh608_costo_unitario"](COSTO_RD, VOL) \
            == pytest.approx(UNITARIO)
        with pytest.raises(ValueError):  # volume nullo
            _F["mh608_costo_unitario"](100.0, 0.0)


class TestW608Verdetto:
    def test_demo(self):
        v = _F["mh608_verdetto"](VOL, RISPARMIO)
        assert v["verdetto"] == "REDISPATCH_CONVIENE"

    def test_curtailment(self):
        v = _F["mh608_verdetto"](1200.0, -48000.0)
        assert v["verdetto"] == "CURTAILMENT_CONVIENE"

    def test_nessuna_congestione(self):
        v = _F["mh608_verdetto"](0.0, 0.0)
        assert v["verdetto"] == "NESSUNA_CONGESTIONE"

    def test_pareggio(self):
        v = _F["mh608_verdetto"](1200.0, 0.0)
        assert v["verdetto"] == "REDISPATCH_CONVIENE"

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh608_verdetto"](-5.0, 100.0)


class TestW608Sensibilita:
    def test_geometria_e_valori(self):
        # flusso 0..1600 passo 400, capacita' 800, 6 h, prezzi 40/60
        righe = _F["mh608_sensibilita_flusso"](0.0, 1600.0, 400.0,
                                              800.0, 6.0, 40.0, 60.0)
        assert len(righe) == 5
        # f=0: nessuna congestione
        assert righe[0]["volume_mwh"] == 0.0
        assert righe[0]["scelta"] == "NESSUNA_CONGESTIONE"
        # f=400: ancora nessuna congestione
        assert righe[1]["volume_mwh"] == 0.0
        assert righe[1]["scelta"] == "NESSUNA_CONGESTIONE"
        # f=800: flusso = capacita' -> volume 0
        assert righe[2]["flusso_mw"] == pytest.approx(800.0)
        assert righe[2]["volume_mwh"] == 0.0
        assert righe[2]["scelta"] == "NESSUNA_CONGESTIONE"
        # f=1200: vol = 400*6 = 2400; cr = 2400*20 = 48000;
        #         cc = 2400*40 = 96000; r = 48000 -> REDISPATCH
        assert righe[3]["volume_mwh"] == pytest.approx(2400.0)
        assert righe[3]["costo_redispatch_eur"] == pytest.approx(48000.0)
        assert righe[3]["costo_curtailment_eur"] == pytest.approx(96000.0)
        assert righe[3]["risparmio_eur"] == pytest.approx(48000.0)
        assert righe[3]["scelta"] == "REDISPATCH"
        # f=1600: vol = 4800; cr = 96000; cc = 192000; r = 96000
        assert righe[4]["volume_mwh"] == pytest.approx(4800.0)
        assert righe[4]["costo_redispatch_eur"] == pytest.approx(96000.0)
        assert righe[4]["scelta"] == "REDISPATCH"
        # monotonicita' del volume
        vols = [r["volume_mwh"] for r in righe]
        assert vols == sorted(vols)

    def test_scelta_curtailment(self):
        # spread 80 > p_monte 40 -> curtailment conviene
        # f=1200: vol = 2400; cr = 2400*80 = 192000; cc = 2400*40 = 96000
        righe = _F["mh608_sensibilita_flusso"](800.0, 1200.0, 400.0,
                                              800.0, 6.0, 40.0, 120.0)
        assert righe[1]["scelta"] == "CURTAILMENT"
        assert righe[1]["risparmio_eur"] == pytest.approx(-96000.0)

    def test_degeneri(self):
        with pytest.raises(ValueError):  # passo nullo
            _F["mh608_sensibilita_flusso"](0.0, 1000.0, 0.0, 800.0, 6.0,
                                          40.0, 60.0)
        with pytest.raises(ValueError):  # max < min
            _F["mh608_sensibilita_flusso"](1000.0, 500.0, 100.0, 800.0, 6.0,
                                          40.0, 60.0)
        with pytest.raises(ValueError):  # capacita' nulla
            _F["mh608_sensibilita_flusso"](0.0, 1000.0, 100.0, 0.0, 6.0,
                                          40.0, 60.0)


class TestW608Demo:
    def test_valori(self):
        d = DEMO
        assert d["flusso"] == 1000.0
        assert d["capacita"] == 800.0
        assert d["ore"] == 6.0
        assert d["p_monte"] == 40.0
        assert d["p_valle"] == 60.0

    def test_catena_completa(self):
        d = DEMO
        vol = _F["mh608_volume"](d["flusso"], d["capacita"], d["ore"])
        assert vol == pytest.approx(VOL)
        cr = _F["mh608_costo_redispatch"](vol, d["p_monte"], d["p_valle"])
        assert cr == pytest.approx(COSTO_RD)
        cc = _F["mh608_costo_curtailment"](vol, d["p_monte"])
        assert cc == pytest.approx(COSTO_CU)
        r = _F["mh608_risparmio"](cr, cc)
        assert r == pytest.approx(RISPARMIO)
        v = _F["mh608_verdetto"](vol, r)
        assert v["verdetto"] == "REDISPATCH_CONVIENE"


class TestW608Registro:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def _ui(self):
        return self._src().split("with tab608:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 724
        assert TITLE608 in titles
        assert TITLE608 in titles

    def test_chain(self):
        assert ", tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724 = st.tabs([" in self._src()
        assert "with tab608:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st608_[a-z0-9_]+", self._ui()))
        attese = {"st608_flusso", "st608_cap", "st608_ore", "st608_pmonte",
                  "st608_pvalle", "st608_passo", "st608_graf", "st608_tabc",
                  "st608_go", "st608_chart", "st608_tab", "st608_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st608_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        sec = self._src().split('# W608 (21/10/2026)')[1]
        sec = sec.split('# W607 (21/10/2026)')[0]
        for w in ("api_key", "apikey", "password", "passwd", "secret",
                  "token"):
            assert w not in sec.lower(), f"sospetto segreto: {w}"
