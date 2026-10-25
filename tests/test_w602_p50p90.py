"""Test tab602 "📊💨 P50/P90: incertezza della producibilità rinnovabile".

Tutti i valori attesi sono calcolati a mano nei commenti (aritmetica
indipendente dagli helper).
"""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh602_num", "mh602_nneg", "mh602_pos", "mh602_pct",
           "mh602_z_eccedenza", "mh602_sigma", "mh602_pxx",
           "mh602_prob_superamento", "mh602_media", "mh602_haircut",
           "mh602_tabella", "mh602_curva", "mh602_verdetto", "mh602_demo")

TITLE602 = "📊💨 P50/P90: incertezza della producibilità rinnovabile"

DEMO = _F["mh602_demo"]()
# Demo: p50=120 GWh, p90=100 GWh, prezzo=70 €/MWh, opex=2,0 M€,
#   debt_service=4,5 M€, dscr_min=1,20, punti=9.
# z90 = Φ⁻¹(0,10) = −1,2815515655446004
# sigma = ln(120/100)/1,2815515655446004 = 0,1823215568/1,2815515655
#       = 0,1422662666846935
# media = 120·exp(0,1422662667²/2) = 120·exp(0,01011985) = 121,2205468946106
# haircut = (1−100/120)·100 = 16,666666666666664
# ricavo_p50 = 120·70/1000 = 8,4 M€ ; cfads_p50 = 8,4 − 2,0 = 6,4 M€
# ricavo_p90 = 100·70/1000 = 7,0 M€ ; cfads_p90 = 7,0 − 2,0 = 5,0 M€
#   (opex fisso: il CFADS NON scala in proporzione alla produzione)
# dscr_p90 = 5,0/4,5 = 1,1111111111111112 < 1,20 → flag
# verdetto: haircut 16,67 → MEDIA + [DSCR_P90_SOTTO_SOGLIA]
SIGMA = 0.1422662666846935
MEDIA = 121.2205468946106
HAIRCUT = 16.666666666666664
DSCR90 = 1.1111111111111112
P99 = 86.18799645684545
P95 = 94.96273562158372
P75 = 109.02035458468413
P25 = 132.08542620189758
P05 = 151.63842854509215
P01 = 167.0766300642586


class TestW602Validatori:
    def test_num(self):
        assert _F["mh602_num"](2, "x") == 2.0
        assert _F["mh602_num"](-3.5, "x") == -3.5
        for bad in (True, False, "1", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh602_num"](bad, "x")

    def test_nneg_pos_pct(self):
        assert _F["mh602_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh602_nneg"](-0.1, "x")
        assert _F["mh602_pos"](0.1, "x") == 0.1
        for bad in (0, -1):
            with pytest.raises(ValueError):
                _F["mh602_pos"](bad, "x")
        assert _F["mh602_pct"](100, "x") == 100.0
        for bad in (-0.1, 100.1):
            with pytest.raises(ValueError):
                _F["mh602_pct"](bad, "x")

    def test_z_eccedenza(self):
        z = _F["mh602_z_eccedenza"]
        assert z(90) == pytest.approx(-1.2815515655446004)
        assert z(50) == pytest.approx(0.0, abs=1e-12)
        assert z(10) == pytest.approx(1.2815515655446004)
        assert z(99) == pytest.approx(-2.3263478740408408)
        assert z(1) == pytest.approx(2.3263478740408408)
        for bad in (0, 100, -5, 101):
            with pytest.raises(ValueError):
                z(bad)


class TestW602SigmaPxx:
    def test_sigma_demo(self):
        assert _F["mh602_sigma"](120.0, 100.0) == pytest.approx(
            SIGMA, rel=1e-12)

    def test_sigma_errori(self):
        with pytest.raises(ValueError):
            _F["mh602_sigma"](100.0, 100.0)  # p90 == p50
        with pytest.raises(ValueError):
            _F["mh602_sigma"](100.0, 120.0)  # p90 > p50
        with pytest.raises(ValueError):
            _F["mh602_sigma"](0, 50.0)
        with pytest.raises(ValueError):
            _F["mh602_sigma"](120.0, 0)

    def test_pxx_demo(self):
        pxx = _F["mh602_pxx"]
        # coerenza interna: P90 ricostruito == p90 di input
        assert pxx(120.0, SIGMA, 90) == pytest.approx(100.0, rel=1e-12)
        assert pxx(120.0, SIGMA, 50) == pytest.approx(120.0, rel=1e-12)
        assert pxx(120.0, SIGMA, 99) == pytest.approx(P99, rel=1e-9)
        assert pxx(120.0, SIGMA, 95) == pytest.approx(P95, rel=1e-9)
        assert pxx(120.0, SIGMA, 75) == pytest.approx(P75, rel=1e-9)
        assert pxx(120.0, SIGMA, 25) == pytest.approx(P25, rel=1e-9)
        assert pxx(120.0, SIGMA, 5) == pytest.approx(P05, rel=1e-9)
        assert pxx(120.0, SIGMA, 1) == pytest.approx(P01, rel=1e-9)

    def test_pxx_sigma_zero(self):
        # nessuna incertezza: tutti i percentili = p50
        for xx in (1, 50, 90, 99):
            assert _F["mh602_pxx"](120.0, 0.0, xx) == pytest.approx(120.0)

    def test_pxx_errori(self):
        with pytest.raises(ValueError):
            _F["mh602_pxx"](120.0, -0.1, 90)
        with pytest.raises(ValueError):
            _F["mh602_pxx"](0, SIGMA, 90)
        with pytest.raises(ValueError):
            _F["mh602_pxx"](120.0, SIGMA, 0)


class TestW602ProbMediaHaircut:
    def test_prob_superamento(self):
        p = _F["mh602_prob_superamento"]
        assert p(120.0, SIGMA, 100.0) == pytest.approx(90.0, abs=1e-9)
        assert p(120.0, SIGMA, 120.0) == pytest.approx(50.0, abs=1e-9)
        assert p(120.0, SIGMA, 110.0) == pytest.approx(
            72.96018703452864, rel=1e-9)
        assert p(120.0, SIGMA, 200.0) < 1.0
        assert p(120.0, SIGMA, 50.0) > 99.0

    def test_prob_sigma_zero(self):
        p = _F["mh602_prob_superamento"]
        assert p(120.0, 0.0, 120.0) == 100.0
        assert p(120.0, 0.0, 119.9) == 100.0
        assert p(120.0, 0.0, 120.1) == 0.0
        with pytest.raises(ValueError):
            p(120.0, SIGMA, 0)

    def test_media(self):
        assert _F["mh602_media"](120.0, SIGMA) == pytest.approx(
            MEDIA, rel=1e-12)
        # la media lognormale sta sopra la mediana
        assert _F["mh602_media"](120.0, SIGMA) > 120.0
        assert _F["mh602_media"](120.0, 0.0) == pytest.approx(120.0)

    def test_haircut(self):
        assert _F["mh602_haircut"](120.0, 100.0) == pytest.approx(
            HAIRCUT, rel=1e-12)
        assert _F["mh602_haircut"](100.0, 90.0) == pytest.approx(10.0)
        with pytest.raises(ValueError):
            _F["mh602_haircut"](100.0, 100.0)


class TestW602TabellaCurva:
    def test_tabella_demo(self):
        righe = _F["mh602_tabella"](120.0, SIGMA, 70.0, 2.0, 4.5,
                                    [50, 90])
        assert len(righe) == 2
        r50, r90 = righe
        assert r50["xx"] == 50 and r90["xx"] == 90
        assert r50["pxx_gwh"] == pytest.approx(120.0, rel=1e-12)
        assert r50["ricavo_meur"] == pytest.approx(8.4, rel=1e-12)
        assert r50["cfads_meur"] == pytest.approx(6.4, rel=1e-12)
        assert r50["dscr"] == pytest.approx(6.4 / 4.5, rel=1e-12)
        assert r90["pxx_gwh"] == pytest.approx(100.0, rel=1e-9)
        assert r90["ricavo_meur"] == pytest.approx(7.0, rel=1e-9)
        assert r90["cfads_meur"] == pytest.approx(5.0, rel=1e-9)
        assert r90["dscr"] == pytest.approx(DSCR90, rel=1e-9)

    def test_tabella_errori(self):
        with pytest.raises(ValueError):
            _F["mh602_tabella"](120.0, SIGMA, 70.0, 2.0, 0, [90])
        with pytest.raises(ValueError):
            _F["mh602_tabella"](120.0, SIGMA, 70.0, 2.0, 4.5, [])
        with pytest.raises(ValueError):
            _F["mh602_tabella"](120.0, SIGMA, -1.0, 2.0, 4.5, [90])

    def test_curva(self):
        curva = _F["mh602_curva"](120.0, SIGMA, 9)
        assert len(curva) == 9
        assert curva[0][0] == pytest.approx(99.0)
        assert curva[-1][0] == pytest.approx(1.0)
        # decrescente in xx -> crescente in produzione
        pxs = [p[1] for p in curva]
        assert all(b > a for a, b in zip(pxs, pxs[1:]))
        assert curva[0][1] == pytest.approx(P99, rel=1e-9)
        assert curva[-1][1] == pytest.approx(P01, rel=1e-9)

    def test_curva_errori(self):
        with pytest.raises(ValueError):
            _F["mh602_curva"](120.0, SIGMA, 1)
        with pytest.raises(ValueError):
            _F["mh602_curva"](120.0, SIGMA, 2.5)


class TestW602VerdettoDemo:
    def test_demo(self):
        assert DEMO["p50_gwh"] == 120.0
        assert DEMO["p90_gwh"] == 100.0
        assert DEMO["prezzo_eur_mwh"] == 70.0
        assert DEMO["ds_meur"] == 4.5
        assert DEMO["dscr_min"] == 1.20

    def test_verdetto_demo(self):
        v = _F["mh602_verdetto"](HAIRCUT, DSCR90, 1.20)
        assert v["livello"] == "MEDIA"
        assert v["flags"] == ["DSCR_P90_SOTTO_SOGLIA"]

    def test_verdetto_livelli(self):
        assert _F["mh602_verdetto"](5.0, 1.5, 1.2)["livello"] == "BASSA"
        assert _F["mh602_verdetto"](9.99, 1.5, 1.2)["livello"] == "BASSA"
        assert _F["mh602_verdetto"](10.0, 1.5, 1.2)["livello"] == "MEDIA"
        assert _F["mh602_verdetto"](19.99, 1.5, 1.2)["livello"] == "MEDIA"
        assert _F["mh602_verdetto"](20.0, 1.5, 1.2)["livello"] == "ALTA"

    def test_verdetto_flags(self):
        v = _F["mh602_verdetto"](30.0, 1.5, 1.2)
        assert v["flags"] == ["HAIRCUT_ELEVATO"]
        v = _F["mh602_verdetto"](30.0, 1.0, 1.2)
        assert v["flags"] == ["DSCR_P90_SOTTO_SOGLIA", "HAIRCUT_ELEVATO"]
        v = _F["mh602_verdetto"](5.0, 1.5, 1.2)
        assert v["flags"] == []
        with pytest.raises(ValueError):
            _F["mh602_verdetto"](HAIRCUT, DSCR90, 0)


class TestW602Registry:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 711
        assert TITLE602 in titles
        assert TITLE602 in titles

    def test_chain(self):
        assert ", tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711 = st.tabs([" in self._src()
        assert "with tab602:" in self._src()

    def test_keys(self):
        src = self._src()
        ui = src.split("with tab602:")[1].split("# Footer")[0]
        keys = set(re.findall(r"st602_[a-z0-9_]+", ui))
        attese = {"st602_p50", "st602_p90", "st602_prezzo", "st602_opex",
                  "st602_ds", "st602_dscrmin", "st602_punti", "st602_sep",
                  "st602_graf", "st602_go", "st602_tab", "st602_chart",
                  "st602_csv", "st602_csv2"}
        assert keys == attese, keys ^ attese

    def test_no_secrets(self):
        src = self._src()
        for pat in ("api_key", "apikey", "password", "secret"):
            assert pat not in src.lower().split("with tab602:")[1].split(
                "# Footer")[0], pat
