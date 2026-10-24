"""Test tab601 "🏦📊 WACC: costo del capitale per progetti energetici".

Tutti i valori attesi sono calcolati a mano nei commenti (aritmetica
indipendente dagli helper).
"""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh601_num", "mh601_nneg", "mh601_pos", "mh601_pct",
           "mh601_beta_levered", "mh601_costo_equity",
           "mh601_costo_debito", "mh601_pesi", "mh601_wacc",
           "mh601_wacc_reale", "mh601_hurdle", "mh601_curva_leva",
           "mh601_verdetto", "mh601_demo")

TITLE601 = "🏦📊 WACC: costo del capitale per progetti energetici"

DEMO = _F["mh601_demo"]()
# Demo: rf=3,5%, beta_u=0,65, mrp=5%, crp=1,2%, D/E=1,0, spread=200 bps,
#   tax=24%, infl=2%, premio=1,5%, de_max=3, passi=7.
# beta_L = 0,65*(1+0,76*1,0) = 0,65*1,76 = 1,144
# Ke = 3,5 + 1,144*5,0 + 1,2 = 3,5+5,72+1,2 = 10,42
# Kd_lordo = 3,5+2,0 = 5,5 ; Kd_netto = 5,5*0,76 = 4,18
# E/V = D/V = 0,5 ; WACC = 10,42*0,5+4,18*0,5 = 7,30
# WACC_reale = (1,073/1,02-1)*100 = 5,1961
# hurdle = 7,30+1,5 = 8,80 ; livello MEDIO, nessun flag
BETA_L = 1.144
KE = 10.42
KD_NETTO = 4.18
WACC = 7.30


class TestW601Validatori:
    def test_num(self):
        assert _F["mh601_num"](2, "x") == 2.0
        assert _F["mh601_num"](-3.5, "x") == -3.5
        # rf e inflazione possono essere negativi: num li ammette
        assert _F["mh601_num"](-0.5, "rf") == -0.5
        for bad in (True, False, "1", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh601_num"](bad, "x")

    def test_nneg_pos_pct(self):
        assert _F["mh601_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh601_nneg"](-0.1, "x")
        assert _F["mh601_pos"](0.1, "x") == 0.1
        for bad in (0, -1):
            with pytest.raises(ValueError):
                _F["mh601_pos"](bad, "x")
        assert _F["mh601_pct"](100, "x") == 100.0
        for bad in (-0.1, 100.1):
            with pytest.raises(ValueError):
                _F["mh601_pct"](bad, "x")


class TestW601BetaEquity:
    def test_beta_levered_demo(self):
        assert _F["mh601_beta_levered"](0.65, 1.0, 24.0) == pytest.approx(
            BETA_L, abs=1e-9)

    def test_beta_levered_senza_debito(self):
        # D/E = 0 -> beta levered = beta unlevered
        assert _F["mh601_beta_levered"](0.65, 0.0, 24.0) == pytest.approx(
            0.65)

    def test_beta_levered_errori(self):
        with pytest.raises(ValueError):
            _F["mh601_beta_levered"](-0.5, 1.0, 24.0)
        with pytest.raises(ValueError):
            _F["mh601_beta_levered"](0.65, -1.0, 24.0)
        with pytest.raises(ValueError):
            _F["mh601_beta_levered"](0.65, 1.0, 101.0)

    def test_costo_equity_demo(self):
        assert _F["mh601_costo_equity"](3.5, BETA_L, 5.0, 1.2) == \
            pytest.approx(KE, abs=1e-9)

    def test_costo_equity_senza_crp(self):
        # 3,5 + 1,0*5,0 + 0 = 8,5
        assert _F["mh601_costo_equity"](3.5, 1.0, 5.0, 0.0) == \
            pytest.approx(8.5)


class TestW601DebitoPesi:
    def test_costo_debito_demo(self):
        kd = _F["mh601_costo_debito"](3.5, 200.0, 24.0)
        assert kd["kd_lordo_pct"] == pytest.approx(5.5)
        assert kd["kd_netto_pct"] == pytest.approx(KD_NETTO, abs=1e-9)

    def test_costo_debito_senza_tasse(self):
        kd = _F["mh601_costo_debito"](3.5, 200.0, 0.0)
        assert kd["kd_netto_pct"] == pytest.approx(5.5)

    def test_pesi(self):
        p = _F["mh601_pesi"](1.0)
        assert p["e_su_v"] == pytest.approx(0.5)
        assert p["d_su_v"] == pytest.approx(0.5)
        p0 = _F["mh601_pesi"](0.0)
        assert p0["e_su_v"] == pytest.approx(1.0)
        assert p0["d_su_v"] == pytest.approx(0.0)
        with pytest.raises(ValueError):
            _F["mh601_pesi"](-0.5)


class TestW601Wacc:
    def test_wacc_demo(self):
        assert _F["mh601_wacc"](KE, KD_NETTO, 1.0) == pytest.approx(
            WACC, abs=1e-9)

    def test_wacc_all_equity(self):
        # D/E = 0 -> WACC = Ke
        assert _F["mh601_wacc"](KE, KD_NETTO, 0.0) == pytest.approx(KE)

    def test_wacc_reale_demo(self):
        assert _F["mh601_wacc_reale"](WACC, 2.0) == pytest.approx(
            5.1961, abs=1e-3)

    def test_wacc_reale_senza_inflazione(self):
        assert _F["mh601_wacc_reale"](WACC, 0.0) == pytest.approx(WACC)

    def test_wacc_reale_deflazione_estrema(self):
        with pytest.raises(ValueError):
            _F["mh601_wacc_reale"](5.0, -100.0)

    def test_hurdle(self):
        assert _F["mh601_hurdle"](WACC, 1.5) == pytest.approx(8.80)
        with pytest.raises(ValueError):
            _F["mh601_hurdle"](WACC, -1.0)


class TestW601CurvaLeva:
    def _curva(self):
        return _F["mh601_curva_leva"](3.5, 0.65, 5.0, 1.2, 200.0,
                                      24.0, 3.0, 7)

    def test_struttura(self):
        c = self._curva()
        assert len(c) == 7
        assert c[0]["d_su_e"] == pytest.approx(0.0)
        assert c[-1]["d_su_e"] == pytest.approx(3.0)

    def test_primo_punto_all_equity(self):
        # D/E=0: beta_L=0,65 -> Ke = 3,5+0,65*5+1,2 = 7,95 = WACC
        c = self._curva()
        assert c[0]["ke_pct"] == pytest.approx(7.95)
        assert c[0]["wacc_pct"] == pytest.approx(7.95)

    def test_monotona_decrescente(self):
        # Kd costante: lo scudo fiscale abbassa il WACC con la leva
        c = self._curva()
        for a, b in zip(c, c[1:]):
            assert b["wacc_pct"] <= a["wacc_pct"] + 1e-9

    def test_ultimo_punto(self):
        # D/E=3: beta_L = 0,65*(1+0,76*3) = 2,132
        # Ke = 3,5+2,132*5+1,2 = 15,36 ; E/V=0,25 D/V=0,75
        # WACC = 15,36*0,25+4,18*0,75 = 6,975
        c = self._curva()
        assert c[-1]["ke_pct"] == pytest.approx(15.36, abs=1e-9)
        assert c[-1]["wacc_pct"] == pytest.approx(6.975, abs=1e-9)

    def test_passi_minimi(self):
        with pytest.raises(ValueError):
            _F["mh601_curva_leva"](3.5, 0.65, 5.0, 1.2, 200.0, 24.0,
                                   3.0, 1)


class TestW601VerdettoDemo:
    def _pipeline_demo(self):
        d = DEMO
        bl = _F["mh601_beta_levered"](d["beta_u"], d["d_su_e"],
                                      d["aliquota_pct"])
        ke = _F["mh601_costo_equity"](d["rf_pct"], bl, d["mrp_pct"],
                                      d["crp_pct"])
        kd = _F["mh601_costo_debito"](d["rf_pct"], d["spread_bps"],
                                      d["aliquota_pct"])["kd_netto_pct"]
        w = _F["mh601_wacc"](ke, kd, d["d_su_e"])
        wr = _F["mh601_wacc_reale"](w, d["infl_pct"])
        h = _F["mh601_hurdle"](w, d["premio_pct"])
        return bl, ke, kd, w, wr, h

    def test_pipeline_demo(self):
        bl, ke, kd, w, wr, h = self._pipeline_demo()
        assert bl == pytest.approx(BETA_L, abs=1e-9)
        assert ke == pytest.approx(KE, abs=1e-9)
        assert kd == pytest.approx(KD_NETTO, abs=1e-9)
        assert w == pytest.approx(WACC, abs=1e-9)
        assert wr == pytest.approx(5.1961, abs=1e-3)
        assert h == pytest.approx(8.80, abs=1e-9)

    def test_verdetto_demo(self):
        v = _F["mh601_verdetto"](WACC, 5.1961, 8.80, 1.0, BETA_L)
        assert v["livello"] == "MEDIO"
        assert v["flags"] == []

    def test_verdetto_livelli(self):
        assert _F["mh601_verdetto"](4.9, 3.0, 6.0, 1.0,
                                    1.0)["livello"] == "BASSO"
        assert _F["mh601_verdetto"](9.0, 7.0, 10.0, 1.0,
                                    1.0)["livello"] == "ALTO"

    def test_verdetto_flags(self):
        v = _F["mh601_verdetto"](WACC, 5.1961, 8.80, 2.5, BETA_L)
        assert "LEVA_ELEVATA" in v["flags"]
        v = _F["mh601_verdetto"](WACC, 5.1961, 8.80, 1.0, 1.6)
        assert "BETA_ELEVATO" in v["flags"]
        v = _F["mh601_verdetto"](1.0, -1.94, 2.0, 1.0, 1.0)
        assert "WACC_REALE_NEGATIVO" in v["flags"]

    def test_demo(self):
        assert DEMO["rf_pct"] == 3.5
        assert DEMO["beta_u"] == 0.65
        assert DEMO["spread_bps"] == 200.0
        assert DEMO["aliquota_pct"] == 24.0


class TestW601Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 685
        assert TITLE601 in titles
        assert TITLE601 in titles

    def test_chain(self):
        assert ", tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685 = st.tabs([" in self._src()
        assert "with tab601:" in self._src()

    def test_keys(self):
        src = self._src()
        ui = src.split("with tab601:")[1].split("# Footer")[0]
        keys = set(re.findall(r"st601_[a-z0-9_]+", ui))
        attese = {"st601_rf", "st601_betau", "st601_mrp", "st601_crp",
                  "st601_de", "st601_spread", "st601_tax", "st601_infl",
                  "st601_premio", "st601_demax", "st601_passi", "st601_sep",
                  "st601_graf", "st601_go", "st601_tab", "st601_chart",
                  "st601_csv"}
        assert keys == attese, keys ^ attese

    def test_no_secrets(self):
        src = self._src()
        for pat in ("api_key", "apikey", "password", "secret"):
            assert pat not in src.lower().split("with tab601:")[1].split(
                "# Footer")[0], pat
