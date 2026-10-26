"""Test tab648 "🔌📉 Trasformatore: quanto costano le perdite a vuoto?".

Demo calcolata a mano: trasformatore esistente 630 kVA, P0 1,10 kW,
Pk 7,60 kW, fattore di carico 50 %, 8.760 h/anno, prezzo 0,22 €/kWh;
nuovo a basse perdite P0' 0,28 kW, Pk' 4,60 kW; CAPEX 18.000 €,
tasso 6 %, vita 20 anni.
-> E_vuoto  = 1,10 x 8.760 = 9.636 kWh/anno
-> E_carico = 7,60 x 0,50^2 x 8.760 = 16.644 kWh/anno
-> E_tot    = 26.280 kWh/anno -> 5.781,60 €/anno
-> quota a vuoto = 9.636 / 26.280 = 36,6667 %
-> E_tot'   = 0,28 x 8.760 + 4,60 x 0,25 x 8.760 = 12.526,8 kWh/anno
-> risparmio = 13.753,2 kWh/anno = 3.025,704 €/anno
-> flussi [-18.000, 3.025,704 x 20]; VAN(6 %) = 16.704,59 €
-> TIR 15,9361 %; payback anno 6 -> CONVIENTE
"""

import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh648_num", "mh648_nneg", "mh648_pos", "mh648_carico01",
           "mh648_int_pos", "mh648_energia_vuoto_kwh",
           "mh648_energia_carico_kwh", "mh648_energia_totale_kwh",
           "mh648_costo_annuo_eur", "mh648_quota_vuoto_pct",
           "mh648_risparmio_kwh", "mh648_risparmio_eur", "mh648_flussi",
           "mh648_van", "mh648_tir", "mh648_payback", "mh648_verdetto",
           "mh648_demo", "mh648_demo_calcoli")

TITLE648 = "🔌📉 Trasformatore: quanto costano le perdite a vuoto?"

E_VUOTO_DEMO = 9636.0
E_CARICO_DEMO = 16644.0
E_TOT_DEMO = 26280.0
COSTO_DEMO = 5781.6
QUOTA_VUOTO_DEMO = 36.666666666666664
E_TOT_NUOVO_DEMO = 12526.8
RISP_KWH_DEMO = 13753.2
RISP_EUR_DEMO = 3025.704
VAN_DEMO = 16704.59
TIR_DEMO = 0.159361


class TestValidatori:
    def test_num_ok(self):
        assert _F["mh648_num"](3, "x") == 3.0

    def test_num_rifiuta_bool_str_nan_inf(self):
        import math
        for bad in (True, "3", math.nan, math.inf, None):
            with pytest.raises(ValueError):
                _F["mh648_num"](bad, "x")

    def test_nneg_pos(self):
        assert _F["mh648_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh648_nneg"](-0.1, "x")
        assert _F["mh648_pos"](0.1, "x") == pytest.approx(0.1)
        with pytest.raises(ValueError):
            _F["mh648_pos"](0.0, "x")

    def test_carico01(self):
        assert _F["mh648_carico01"](0.0, "x") == 0.0
        assert _F["mh648_carico01"](1.0, "x") == 1.0
        with pytest.raises(ValueError):
            _F["mh648_carico01"](-0.01, "x")
        with pytest.raises(ValueError):
            _F["mh648_carico01"](1.01, "x")

    def test_int_pos(self):
        assert _F["mh648_int_pos"](20.0, "x") == 20
        with pytest.raises(ValueError):
            _F["mh648_int_pos"](0, "x")
        with pytest.raises(ValueError):
            _F["mh648_int_pos"](2.5, "x")


class TestPerdite:
    def test_vuoto(self):
        assert _F["mh648_energia_vuoto_kwh"](1.10, 8760.0) == \
            pytest.approx(E_VUOTO_DEMO)

    def test_vuoto_zero_ore(self):
        assert _F["mh648_energia_vuoto_kwh"](1.10, 0.0) == 0.0

    def test_carico_quadratico(self):
        # dimezzare il carico riduce le perdite a carico a 1/4
        e_pieno = _F["mh648_energia_carico_kwh"](7.60, 1.0, 8760.0)
        e_mezzo = _F["mh648_energia_carico_kwh"](7.60, 0.5, 8760.0)
        assert e_mezzo == pytest.approx(e_pieno / 4.0)
        assert e_mezzo == pytest.approx(E_CARICO_DEMO)

    def test_carico_nullo(self):
        assert _F["mh648_energia_carico_kwh"](7.60, 0.0, 8760.0) == 0.0

    def test_carico_fuori_range(self):
        with pytest.raises(ValueError):
            _F["mh648_energia_carico_kwh"](7.60, 1.5, 8760.0)

    def test_totale(self):
        assert _F["mh648_energia_totale_kwh"](E_VUOTO_DEMO,
                                             E_CARICO_DEMO) == \
            pytest.approx(E_TOT_DEMO)

    def test_costo(self):
        assert _F["mh648_costo_annuo_eur"](E_TOT_DEMO, 0.22) == \
            pytest.approx(COSTO_DEMO)

    def test_quota_vuoto(self):
        assert _F["mh648_quota_vuoto_pct"](E_VUOTO_DEMO, E_TOT_DEMO) == \
            pytest.approx(QUOTA_VUOTO_DEMO)

    def test_quota_vuoto_none_se_totale_nullo(self):
        assert _F["mh648_quota_vuoto_pct"](0.0, 0.0) is None

    def test_risparmio(self):
        assert _F["mh648_risparmio_kwh"](E_TOT_DEMO, E_TOT_NUOVO_DEMO) == \
            pytest.approx(RISP_KWH_DEMO)

    def test_risparmio_negativo_se_nuovo_peggiore(self):
        assert _F["mh648_risparmio_kwh"](1000.0, 2000.0) == -1000.0

    def test_risparmio_eur(self):
        assert _F["mh648_risparmio_eur"](RISP_KWH_DEMO, 0.22) == \
            pytest.approx(RISP_EUR_DEMO)


class TestFinanza:
    def test_flussi(self):
        f = _F["mh648_flussi"](18000.0, RISP_EUR_DEMO, 20)
        assert f[0] == -18000.0 and len(f) == 21
        assert all(x == pytest.approx(RISP_EUR_DEMO) for x in f[1:])

    def test_van_demo(self):
        f = _F["mh648_flussi"](18000.0, RISP_EUR_DEMO, 20)
        assert _F["mh648_van"](f, 6.0) == pytest.approx(VAN_DEMO, abs=0.05)

    def test_tir_demo(self):
        f = _F["mh648_flussi"](18000.0, RISP_EUR_DEMO, 20)
        assert _F["mh648_tir"](f) == pytest.approx(TIR_DEMO, abs=1e-4)

    def test_tir_none_senza_cambio_segno(self):
        assert _F["mh648_tir"]([100.0, 50.0, 50.0]) is None
        assert _F["mh648_tir"]([-100.0, -50.0]) is None

    def test_payback_demo(self):
        f = _F["mh648_flussi"](18000.0, RISP_EUR_DEMO, 20)
        assert _F["mh648_payback"](f) == 6

    def test_payback_none_se_mai(self):
        assert _F["mh648_payback"]([-100.0, 1.0, 1.0]) is None

    def test_verdetto_conviene(self):
        assert _F["mh648_verdetto"](3025.704, 16704.59, 18000.0,
                                    10.0) == "CONVIENTE"

    def test_verdetto_marginale(self):
        assert _F["mh648_verdetto"](100.0, -900.0, 18000.0,
                                    10.0) == "MARGINALE"

    def test_verdetto_non_conviene(self):
        assert _F["mh648_verdetto"](100.0, -5000.0, 18000.0,
                                    10.0) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile(self):
        assert _F["mh648_verdetto"](0.0, 10.0, 18000.0,
                                    10.0) == "NON_CALCOLABILE"
        assert _F["mh648_verdetto"](-50.0, 10.0, 18000.0,
                                    10.0) == "NON_CALCOLABILE"


class TestDemo:
    def test_demo_calcoli(self):
        c = _F["mh648_demo_calcoli"]()
        assert c["e_vuoto"] == pytest.approx(E_VUOTO_DEMO)
        assert c["e_carico"] == pytest.approx(E_CARICO_DEMO)
        assert c["e_tot"] == pytest.approx(E_TOT_DEMO)
        assert c["costo_eur"] == pytest.approx(COSTO_DEMO)
        assert c["quota_vuoto_pct"] == pytest.approx(QUOTA_VUOTO_DEMO)
        assert c["e_tot_nuovo"] == pytest.approx(E_TOT_NUOVO_DEMO)
        assert c["risp_kwh"] == pytest.approx(RISP_KWH_DEMO)
        assert c["risp_eur"] == pytest.approx(RISP_EUR_DEMO)
        assert c["van"] == pytest.approx(VAN_DEMO, abs=0.05)
        assert c["tir"] == pytest.approx(TIR_DEMO, abs=1e-4)
        assert c["payback"] == 6
        assert c["verdetto"] == "CONVIENTE"


class TestUI:
    def _app(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_label_presente(self):
        assert TITLE648 in self._app()

    def test_helpers_presenti(self):
        assert "# W648 (23/10/2026) - tab648" in self._app()

    def test_chain_bumpata(self):
        assert ", tab647, tab648, tab649, tab650, tab651, tab652, tab653, tab654, tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735 = st.tabs([" in self._app()

    def test_tab_count_648(self):
        src = self._app()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 735
        assert TITLE648 in titoli
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab648" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab648" in withs

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st648_[a-z0-9]+)"', self._app())
        assert len(keys) >= 10
        assert len(set(keys)) == len(keys)
        # nessuna collisione con le chiavi del ciclo precedente
        assert not any(k.startswith("st647_") for k in keys)

    def test_csv_filename(self):
        assert "trasformatore_perdite.csv" in self._app()
