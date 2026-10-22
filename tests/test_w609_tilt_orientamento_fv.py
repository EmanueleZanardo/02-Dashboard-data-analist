"""Test tab609 "☀️📐 Tilt & orientamento FV: l'angolo che massimizza il rendimento".

I casi speciali di fisica (declinazione, eccentricita', angolo di incidenza)
sono calcolati a mano nei commenti; i valori integrati (annuo, demo) sono
fissati dal modello e contro-verificati per plausibilita' (tilt ottimo 39°
a 46°N, simmetria est/ovest esatta, tilt batte orizzontale a 46°N).
"""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh609_num", "mh609_nneg", "mh609_pos", "mh609_lat",
           "mh609_tilt", "mh609_azimut", "mh609_frac", "mh609_posfrac",
           "mh609_giorno", "mh609_mese", "mh609_giorni_mese",
           "mh609_giorno_medio", "mh609_declinazione", "mh609_e0",
           "mh609_omega_s", "mh609_cos_incidenza",
           "mh609_irraggiamento_giornaliero", "mh609_annuo",
           "mh609_tilt_ottimale", "mh609_perdita_tilt",
           "mh609_penalita_azimut", "mh609_scansione_azimut",
           "mh609_resa_specifica", "mh609_capacity_factor",
           "mh609_verdetto", "mh609_demo")

TITLE609 = "☀️📐 Tilt & orientamento FV: l'angolo che massimizza il rendimento"

# Demo: lat 46.0, tilt 30°, azimut -45° (sud-est), tau 0.75, kd 0.12,
# rho 0.2, PR 0.85, 100 kWp
DEMO = _F["mh609_demo"]()
ANNUO_TILT = 2063.06   # kWh/m2/anno sul piano (tilt 30, gamma -45)
ORIZ = 1829.78         # kWh/m2/anno su orizzontale
OTTIMO = 39.0          # tilt ottimo verso sud a 46°N
ANNUO_OTTIMO = 2240.03  # kWh/m2/anno al tilt ottimo
PT = 0.0095            # perdita tilt 30° vs ottimo
PG = 0.0701            # penalita' azimut -45° vs sud
RESA = 1753.61         # kWh/kWp/anno = 2063.06 * 0.85
CF = 0.2002            # capacity factor = 1753.61 / 8760


class TestW609Validatori:
    def test_num(self):
        assert _F["mh609_num"](3, "x") == 3.0
        for bad in (True, "3", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh609_num"](bad, "x")

    def test_range(self):
        assert _F["mh609_lat"](-90) == -90.0
        assert _F["mh609_lat"](90) == 90.0
        assert _F["mh609_tilt"](0) == 0.0
        assert _F["mh609_tilt"](90) == 90.0
        assert _F["mh609_azimut"](-180) == -180.0
        assert _F["mh609_azimut"](180) == 180.0
        assert _F["mh609_frac"](0, "x") == 0.0
        assert _F["mh609_frac"](1, "x") == 1.0
        assert _F["mh609_posfrac"](1, "x") == 1.0
        for fn, bad in (("mh609_lat", 91), ("mh609_lat", -91),
                        ("mh609_tilt", -1), ("mh609_tilt", 91),
                        ("mh609_azimut", 181), ("mh609_azimut", -181)):
            with pytest.raises(ValueError):
                _F[fn](bad)
        for fn, bad in (("mh609_frac", -0.1), ("mh609_frac", 1.1),
                        ("mh609_posfrac", 0), ("mh609_posfrac", 1.1)):
            with pytest.raises(ValueError):
                _F[fn](bad, "x")

    def test_giorno_mese(self):
        assert _F["mh609_giorno"](1) == 1
        assert _F["mh609_giorno"](365) == 365
        assert _F["mh609_giorni_mese"](1) == 31
        assert _F["mh609_giorni_mese"](2) == 28
        assert _F["mh609_giorni_mese"](12) == 31
        assert _F["mh609_giorno_medio"](1) == 15
        assert _F["mh609_giorno_medio"](2) == 46
        assert _F["mh609_giorno_medio"](12) == 349
        for bad_fn, bad in (("mh609_giorno", 0), ("mh609_giorno", 366),
                            ("mh609_giorno", 1.5), ("mh609_mese", 0),
                            ("mh609_mese", 13)):
            with pytest.raises(ValueError):
                _F[bad_fn](bad)


class TestW609Fisica:
    def test_declinazione(self):
        # equinozio di primavera (n=81): ~0°; solstizio d'estate (n=172): ~+23.45°
        assert abs(_F["mh609_declinazione"](81)) < 0.5
        assert _F["mh609_declinazione"](172) == pytest.approx(23.45, abs=0.01)
        assert _F["mh609_declinazione"](355) == pytest.approx(-23.45,
                                                             abs=0.01)

    def test_e0(self):
        # perielio ~3 gennaio: E0 ~ 1.033; afelio ~luglio: ~0.967
        assert _F["mh609_e0"](3) == pytest.approx(1.0330, abs=0.001)
        assert _F["mh609_e0"](185) == pytest.approx(0.9670, abs=0.001)

    def test_omega_s(self):
        assert _F["mh609_omega_s"](0, 0) == 90.0
        assert _F["mh609_omega_s"](45, 0) == 90.0
        # polo nord: giorno polare d'estate, notte polare d'inverno
        assert _F["mh609_omega_s"](90, 23.44) == 180.0
        assert _F["mh609_omega_s"](90, -23.44) == 0.0

    def test_cos_incidenza_speciali(self):
        ci = _F["mh609_cos_incidenza"]
        # mezzogiorno, equatore, equinozio, tilt 30°: cos(30°) = 0.8660
        assert ci(0, 0, 30, 0, 0) == pytest.approx(0.8660, abs=1e-4)
        # orizzontale = coseno dell'angolo zenitale
        tz = (math.sin(math.radians(10)) * math.sin(math.radians(45))
              + math.cos(math.radians(10)) * math.cos(math.radians(45))
              * math.cos(math.radians(30)))
        assert ci(10, 45, 0, 0, 30) == pytest.approx(tz, abs=1e-9)
        # 45°N, mezzogiorno, equinozio, tilt 45° verso sud: sole in asse = 1
        assert ci(0, 45, 45, 0, 0) == pytest.approx(1.0, abs=1e-9)
        # stesso ma verso nord: sole radente al piano = 0
        assert ci(0, 45, 45, 180, 0) == pytest.approx(0.0, abs=1e-9)
        # alba all'equatore su orizzontale: sole all'orizzonte = 0
        assert ci(0, 0, 0, 0, 90) == pytest.approx(0.0, abs=1e-9)


class TestW609Giornaliero:
    def test_notte_polare(self):
        g = _F["mh609_irraggiamento_giornaliero"](75, 30, 0, 355, 0.75,
                                                  0.12, 0.2)
        assert g["tilt_wh"] == 0.0
        assert g["oriz_wh"] == 0.0
        assert g["ore_sole"] == 0.0

    def test_equatore_equinozio(self):
        g = _F["mh609_irraggiamento_giornaliero"](0, 0, 0, 81, 0.75,
                                                  0.12, 0.2)
        assert g["tilt_wh"] > 0.0
        assert g["ore_sole"] == pytest.approx(12.0, abs=0.01)

    def test_verticale_meno_di_orizzontale_equatore(self):
        # a mezzogiorno all'equatore il beam e' perpendicolare all'orizzontale:
        # un piano verticale prende solo diffusa+riflessa
        v = _F["mh609_irraggiamento_giornaliero"](0, 90, 0, 81, 0.75,
                                                  0.12, 0.2)["tilt_wh"]
        o = _F["mh609_irraggiamento_giornaliero"](0, 0, 0, 81, 0.75,
                                                  0.12, 0.2)["tilt_wh"]
        assert 0.0 < v < o

    def test_degeneri(self):
        with pytest.raises(ValueError):
            _F["mh609_irraggiamento_giornaliero"](46, 30, 0, 81, 0, 0.12,
                                                  0.2)  # tau = 0
        with pytest.raises(ValueError):
            _F["mh609_irraggiamento_giornaliero"](46, 30, 0, 81, 0.75,
                                                  1.5, 0.2)  # kd > 1


class TestW609Annuo:
    def test_struttura_e_somma(self):
        a = _F["mh609_annuo"](46.0, 30, 0, 0.75, 0.12, 0.2)
        assert len(a["mensile"]) == 12
        assert sum(r["tilt_kwh_m2"] for r in a["mensile"]) == \
            pytest.approx(a["annuo_kwh_m2"], rel=1e-9)
        assert sum(r["giorni"] for r in a["mensile"]) == 365

    def test_tilt_batte_orizzontale_46N(self):
        a = _F["mh609_annuo"](46.0, 30, 0, 0.75, 0.12, 0.2)
        assert a["annuo_kwh_m2"] > a["oriz_kwh_m2"]

    def test_simmetria_est_ovest(self):
        # la griglia oraria e' simmetrica: est e ovest rendono uguale
        e = _F["mh609_annuo"](46.0, 30, -45, 0.75, 0.12, 0.2)
        o = _F["mh609_annuo"](46.0, 30, 45, 0.75, 0.12, 0.2)
        assert e["annuo_kwh_m2"] == o["annuo_kwh_m2"]

    def test_stagionalita_46N(self):
        a = _F["mh609_annuo"](46.0, 30, 0, 0.75, 0.12, 0.2)
        luglio = a["mensile"][6]["tilt_kwh_m2"]
        gennaio = a["mensile"][0]["tilt_kwh_m2"]
        assert luglio > 2.5 * gennaio


class TestW609Ottimo:
    def test_46N(self):
        ott = _F["mh609_tilt_ottimale"](46.0, 0.75, 0.12, 0.2)
        assert ott["tilt_ottimo"] == pytest.approx(OTTIMO, abs=2.0)
        assert ott["guadagno_vs_oriz"] > 0.15

    def test_equatore_quasi_piatto(self):
        ott = _F["mh609_tilt_ottimale"](0.0, 0.75, 0.12, 0.2)
        assert ott["tilt_ottimo"] <= 5.0

    def test_sud_batte_nord(self):
        s = _F["mh609_annuo"](46.0, 30, 0, 0.75, 0.12, 0.2)["annuo_kwh_m2"]
        n = _F["mh609_annuo"](46.0, 30, 180, 0.75, 0.12, 0.2)["annuo_kwh_m2"]
        assert s > 1.5 * n


class TestW609Perdite:
    def test_all_ottimo_zero(self):
        assert _F["mh609_perdita_tilt"](46.0, 39.0, 0.75, 0.12,
                                        0.2) == pytest.approx(0.0, abs=1e-9)
        assert _F["mh609_penalita_azimut"](46.0, 30, 0, 0.75, 0.12,
                                           0.2) == pytest.approx(0.0,
                                                                 abs=1e-9)

    def test_monotonia_azimut(self):
        p45 = _F["mh609_penalita_azimut"](46.0, 30, 45, 0.75, 0.12, 0.2)
        p90 = _F["mh609_penalita_azimut"](46.0, 30, 90, 0.75, 0.12, 0.2)
        assert 0.0 < p45 < p90 < 0.5

    def test_scansione(self):
        righe = _F["mh609_scansione_azimut"](46.0, 30, 0.75, 0.12, 0.2)
        assert len(righe) == 13  # -90..+90 passo 15
        assert righe[6]["gamma"] == 0.0
        assert righe[6]["penalita"] == pytest.approx(0.0, abs=1e-9)
        assert max(r["penalita"] for r in righe) < 0.5


class TestW609Resa:
    def test_resa_e_cf(self):
        assert _F["mh609_resa_specifica"](2063.06, 0.85) == \
            pytest.approx(1753.61, rel=1e-3)
        assert _F["mh609_capacity_factor"](1753.61) == \
            pytest.approx(0.2002, rel=1e-3)
        with pytest.raises(ValueError):
            _F["mh609_resa_specifica"](1000, 1.5)


class TestW609Verdetto:
    def test_soglie(self):
        assert _F["mh609_verdetto"](0.01)["verdetto"] == "OTTIMALE"
        assert _F["mh609_verdetto"](0.05)["verdetto"] == "MIGLIORABILE"
        assert _F["mh609_verdetto"](0.20)["verdetto"] == "DA_RIVEDERE"
        with pytest.raises(ValueError):
            _F["mh609_verdetto"](-0.1)


class TestW609Demo:
    def test_valori(self):
        ann = _F["mh609_annuo"](DEMO["lat"], DEMO["beta"], DEMO["gamma"],
                                DEMO["tau"], DEMO["kd"], DEMO["rho"])
        assert ann["annuo_kwh_m2"] == pytest.approx(ANNUO_TILT, rel=1e-3)
        assert ann["oriz_kwh_m2"] == pytest.approx(ORIZ, rel=1e-3)
        ott = _F["mh609_tilt_ottimale"](DEMO["lat"], DEMO["tau"],
                                        DEMO["kd"], DEMO["rho"])
        assert ott["tilt_ottimo"] == pytest.approx(OTTIMO, abs=2.0)
        assert ott["annuo_kwh_m2"] == pytest.approx(ANNUO_OTTIMO, rel=1e-3)

    def test_catena_completa(self):
        pt = _F["mh609_perdita_tilt"](DEMO["lat"], DEMO["beta"],
                                      DEMO["tau"], DEMO["kd"], DEMO["rho"])
        pg = _F["mh609_penalita_azimut"](DEMO["lat"], DEMO["beta"],
                                         DEMO["gamma"], DEMO["tau"],
                                         DEMO["kd"], DEMO["rho"])
        assert pt == pytest.approx(PT, rel=1e-2)
        assert pg == pytest.approx(PG, rel=1e-2)
        resa = _F["mh609_resa_specifica"](ANNUO_TILT, DEMO["pr"])
        assert resa == pytest.approx(RESA, rel=1e-3)
        assert _F["mh609_capacity_factor"](resa) == \
            pytest.approx(CF, rel=1e-3)
        ptot = 1.0 - (1.0 - pt) * (1.0 - pg)
        assert _F["mh609_verdetto"](ptot)["verdetto"] == "MIGLIORABILE"


class TestW609Registro:
    def _src(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def _ui(self):
        return self._src().split("with tab609:")[1].split("# Footer")[0]

    def test_tab_count(self):
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", self._src(), re.S)
        titles = re.findall(r'"([^"]+)"', m.group(1))
        assert len(titles) == 647
        assert TITLE609 in titles
        assert TITLE609 in titles

    def test_chain(self):
        assert ", tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644, tab645, tab646, tab647 = st.tabs([" in self._src()
        assert "with tab609:" in self._src()

    def test_keys(self):
        keys = set(re.findall(r"st609_[a-z0-9_]+", self._ui()))
        attese = {"st609_lat", "st609_tilt", "st609_gamma", "st609_tau",
                  "st609_kd", "st609_rho", "st609_pr", "st609_kwp",
                  "st609_graf", "st609_tabz", "st609_go", "st609_chart",
                  "st609_tab", "st609_csv"}
        assert keys == attese, f"chiavi extra/mancanti: {keys ^ attese}"
        # unicita' globale nel file
        tutte = re.findall(r"st609_[a-z0-9_]+", self._src())
        assert len(tutte) == len(set(tutte))

    def test_no_secrets(self):
        sec = self._src().split('# W609 (21/10/2026)')[1]
        sec = sec.split('# W608 (21/10/2026)')[0]
        for w in ("api_key", "apikey", "password", "passwd", "secret",
                  "token"):
            assert w not in sec.lower(), f"sospetto segreto: {w}"
