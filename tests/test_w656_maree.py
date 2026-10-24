"""Test tab656 "🌊 Energia delle maree: il business case tidal".

Demo calcolata a mano: sbarramento tipo Severn, bacino 10 km2,
escursione di marea 8 m, 705 maree/anno, rendimento 0,85, prezzo
energia 0,15 EUR/kWh, O&M 15.000.000 EUR/anno, CAPEX 800.000.000 EUR,
CO2 elettricita' 0,30 kg/kWh, 6 %, 25 anni, escalation 2 %/anno,
tolleranza 10 %.

- E_ciclo_J = 0,5 x 1025 x 9,81 x 10e6 x 8^2 = 3.217.680.000.000 J
- E_anno = 3.21768e12 x 705 x 0,85 / 3,6e6 = 535.609.650,0 kWh/anno
- E_teorica = 535.609.650 / 0,85 = 630.129.000,0 kWh/anno
- ricavi = 535.609.650 x 0,15 = 80.341.447,5 EUR/anno
- risparmio anno 1 = 80.341.447,5 - 15.000.000 = 65.341.447,5 EUR/anno
- CO2 evitata = 535.609.650 x 0,30 / 1.000 = 160.682,895 t/anno
- P_media = 535.609.650 / 8760 = 61.142,65410958904 kW
- CRF(6 %, 25) = 0,07822671821227395
- LCOE = (800.000.000 x 0,07822671821227395 + 15.000.000) / 535.609.650
  = 0,14484685735184039 EUR/kWh = 144,85 EUR/MWh
- flussi [-800.000.000, 65.341.447,5 x 1,02^i per i=1..25]; VAN(6 %) =
  229.284.407,0281824 EUR; TIR 0,08588995838557728 (8,5890 %);
  payback anno 11; VAN > 0 -> CONVIENTE

Ramo stream (mano): rotore d = 20 m -> A = pi x 400 / 4 =
314,1592653589793 m2; v = 2,5 m/s; Cp = 0,35 ->
P = 0,5 x 1025 x 314,1592653589793 x 15,625 x 0,35 / 1000 =
880,5049722463581 kW/turbina; E = 880,5049722463581 x 4000 x 10 =
35.220.198,88985432 kWh/anno.
"""

import math
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh656_num", "mh656_nneg", "mh656_pos", "mh656_int_pos",
           "mh656_frazione", "mh656_cp", "mh656_energia_barrage",
           "mh656_area_rotore", "mh656_potenza_stream",
           "mh656_energia_stream", "mh656_energia_teorica_stream",
           "mh656_ricavi", "mh656_risparmio", "mh656_crf", "mh656_lcoe",
           "mh656_co2_t", "mh656_potenza_media_kw",
           "mh656_capex_da_specifico", "mh656_flussi",
           "mh656_flussi_esc", "mh656_van", "mh656_tir",
           "mh656_payback", "mh656_verdetto", "mh656_demo",
           "mh656_demo_calcoli")

TITLE656 = "🌊 Energia delle maree: il business case tidal"

E_ANNO_DEMO = 535609650.0
E_TEORICA_DEMO = 630129000.0
RICAVI_DEMO = 80341447.5
RISP_DEMO = 65341447.5
CO2_DEMO = 160682.895
P_MEDIA_DEMO = 61142.65410958904
LCOE_DEMO = 0.14484685735184039
CAPEX_DEMO = 800000000.0
VAN_DEMO = 229284407.0281824
TIR_DEMO = 0.08588995838557728
AREA_STREAM_DEMO = 314.1592653589793
P_STREAM_DEMO = 880.5049722463581
E_STREAM_DEMO = 35220198.88985432


class TestValidatori:
    def test_num_ok(self):
        assert _F["mh656_num"](3, "x") == 3.0

    def test_num_rifiuta_bool_str_nan_inf(self):
        for bad in (True, "3", math.nan, math.inf, None):
            with pytest.raises(ValueError):
                _F["mh656_num"](bad, "x")

    def test_nneg_pos(self):
        assert _F["mh656_nneg"](0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh656_nneg"](-0.1, "x")

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh656_pos"](0, "x")
        assert _F["mh656_pos"](0.5, "x") == 0.5

    def test_int_pos(self):
        assert _F["mh656_int_pos"](705.0, "x") == 705
        with pytest.raises(ValueError):
            _F["mh656_int_pos"](705.5, "x")

    def test_frazione_bordi(self):
        assert _F["mh656_frazione"](0, "x") == 0.0
        assert _F["mh656_frazione"](1, "x") == 1.0
        with pytest.raises(ValueError):
            _F["mh656_frazione"](1.1, "x")

    def test_cp_bordi(self):
        assert _F["mh656_cp"](0.35, "x") == 0.35
        assert _F["mh656_cp"](0.593, "x") == 0.593
        with pytest.raises(ValueError):
            _F["mh656_cp"](0.594, "x")
        with pytest.raises(ValueError):
            _F["mh656_cp"](0.0, "x")


class TestBarrage:
    def test_energia_demo(self):
        assert _F["mh656_energia_barrage"](10.0, 8.0, 705, 0.85) == \
            pytest.approx(E_ANNO_DEMO)

    def test_energia_scala_con_r_quadrato(self):
        # R dimezzato -> energia / 4
        e1 = _F["mh656_energia_barrage"](10.0, 8.0, 705, 0.85)
        e2 = _F["mh656_energia_barrage"](10.0, 4.0, 705, 0.85)
        assert e2 == pytest.approx(e1 / 4.0)

    def test_energia_scala_con_area(self):
        e1 = _F["mh656_energia_barrage"](10.0, 8.0, 705, 0.85)
        e2 = _F["mh656_energia_barrage"](5.0, 8.0, 705, 0.85)
        assert e2 == pytest.approx(e1 / 2.0)

    def test_energia_eta_zero(self):
        assert _F["mh656_energia_barrage"](10.0, 8.0, 705, 0.0) == 0.0

    def test_energia_rifiuta_input(self):
        with pytest.raises(ValueError):
            _F["mh656_energia_barrage"](0.0, 8.0, 705, 0.85)
        with pytest.raises(ValueError):
            _F["mh656_energia_barrage"](10.0, -1.0, 705, 0.85)
        with pytest.raises(ValueError):
            _F["mh656_energia_barrage"](10.0, 8.0, 0, 0.85)


class TestStream:
    def test_area_rotore_demo(self):
        assert _F["mh656_area_rotore"](20.0) == \
            pytest.approx(AREA_STREAM_DEMO)

    def test_potenza_demo(self):
        assert _F["mh656_potenza_stream"](AREA_STREAM_DEMO, 2.5, 0.35) == \
            pytest.approx(P_STREAM_DEMO)

    def test_potenza_scala_con_v_cubo(self):
        p1 = _F["mh656_potenza_stream"](AREA_STREAM_DEMO, 2.5, 0.35)
        p2 = _F["mh656_potenza_stream"](AREA_STREAM_DEMO, 5.0, 0.35)
        assert p2 == pytest.approx(p1 * 8.0)

    def test_potenza_zero_con_v_zero(self):
        assert _F["mh656_potenza_stream"](AREA_STREAM_DEMO, 0.0, 0.35) == 0.0

    def test_potenza_rifiuta_cp_betz(self):
        with pytest.raises(ValueError):
            _F["mh656_potenza_stream"](AREA_STREAM_DEMO, 2.5, 0.60)

    def test_energia_stream_demo(self):
        assert _F["mh656_energia_stream"](P_STREAM_DEMO, 4000.0, 10) == \
            pytest.approx(E_STREAM_DEMO)

    def test_energia_teorica_maggiore(self):
        # con Cp = 1 l'energia disponibile supera quella elettrica
        et = _F["mh656_energia_teorica_stream"](AREA_STREAM_DEMO, 2.5,
                                                4000.0, 10)
        assert et == pytest.approx(E_STREAM_DEMO / 0.35)


class TestEconomia:
    def test_ricavi_demo(self):
        assert _F["mh656_ricavi"](E_ANNO_DEMO, 0.15) == \
            pytest.approx(RICAVI_DEMO)

    def test_risparmio_demo(self):
        assert _F["mh656_risparmio"](RICAVI_DEMO, 15000000.0) == \
            pytest.approx(RISP_DEMO)

    def test_risparmio_negativo_possibile(self):
        assert _F["mh656_risparmio"](100.0, 300.0) == pytest.approx(-200.0)

    def test_crf_demo(self):
        assert _F["mh656_crf"](6.0, 25) == \
            pytest.approx(0.07822671821227395)

    def test_crf_tasso_zero(self):
        assert _F["mh656_crf"](0.0, 25) == pytest.approx(1.0 / 25.0)

    def test_lcoe_demo(self):
        assert _F["mh656_lcoe"](CAPEX_DEMO, 15000000.0, E_ANNO_DEMO, 6.0,
                                25) == pytest.approx(LCOE_DEMO)

    def test_lcoe_none_senza_energia(self):
        assert _F["mh656_lcoe"](CAPEX_DEMO, 15000000.0, 0.0, 6.0,
                                25) is None

    def test_co2_demo(self):
        assert _F["mh656_co2_t"](E_ANNO_DEMO, 0.30) == \
            pytest.approx(CO2_DEMO)

    def test_potenza_media_demo(self):
        assert _F["mh656_potenza_media_kw"](E_ANNO_DEMO) == \
            pytest.approx(P_MEDIA_DEMO)

    def test_capex_da_specifico(self):
        assert _F["mh656_capex_da_specifico"](P_MEDIA_DEMO, 13000.0) == \
            pytest.approx(P_MEDIA_DEMO * 13000.0)


class TestFinanza:
    def _flussi_demo(self):
        return _F["mh656_flussi_esc"](CAPEX_DEMO, RISP_DEMO, 25, 2.0)

    def test_flussi_struttura(self):
        fl = _F["mh656_flussi"](CAPEX_DEMO, RISP_DEMO, 25)
        assert fl[0] == -CAPEX_DEMO and len(fl) == 26
        assert all(f == RISP_DEMO for f in fl[1:])

    def test_flussi_esc_struttura(self):
        fl = _F["mh656_flussi_esc"](1000.0, 100.0, 3, 10.0)
        assert fl[0] == -1000.0
        assert fl[1:] == pytest.approx([110.0, 121.0, 133.1])

    def test_flussi_esc_rifiuta(self):
        with pytest.raises(ValueError):
            _F["mh656_flussi_esc"](1000.0, 100.0, 3, 31.0)
        with pytest.raises(ValueError):
            _F["mh656_flussi_esc"](1000.0, 100.0, 3, -1.0)

    def test_van_demo(self):
        assert _F["mh656_van"](self._flussi_demo(), 6.0) == \
            pytest.approx(VAN_DEMO)

    def test_tir_demo(self):
        assert _F["mh656_tir"](self._flussi_demo()) == \
            pytest.approx(TIR_DEMO)

    def test_tir_none_senza_cambio_segno(self):
        assert _F["mh656_tir"]([-100.0, -10.0, -10.0]) is None

    def test_payback_demo(self):
        assert _F["mh656_payback"](self._flussi_demo()) == 11

    def test_payback_none_mai(self):
        assert _F["mh656_payback"]([-100.0, 1.0, 1.0]) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh656_verdetto"](RISP_DEMO, VAN_DEMO, CAPEX_DEMO,
                                    10.0) == "CONVIENTE"

    def test_verdetto_marginale(self):
        assert _F["mh656_verdetto"](1000.0, -1500.0, 24000.0,
                                    10.0) == "MARGINALE"

    def test_verdetto_non_conviente(self):
        assert _F["mh656_verdetto"](100.0, -5000.0, 24000.0,
                                    10.0) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile(self):
        assert _F["mh656_verdetto"](0.0, 1.0, 24000.0,
                                    10.0) == "NON_CALCOLABILE"
        assert _F["mh656_verdetto"](-50.0, 1.0, 24000.0,
                                    10.0) == "NON_CALCOLABILE"


class TestDemo:
    def test_demo_calcoli_end_to_end(self):
        r = _F["mh656_demo_calcoli"]()
        assert r["e_anno"] == pytest.approx(E_ANNO_DEMO)
        assert r["e_teorica"] == pytest.approx(E_TEORICA_DEMO)
        assert r["ricavi"] == pytest.approx(RICAVI_DEMO)
        assert r["risparmio"] == pytest.approx(RISP_DEMO)
        assert r["co2_t"] == pytest.approx(CO2_DEMO)
        assert r["p_media_kw"] == pytest.approx(P_MEDIA_DEMO)
        assert r["lcoe"] == pytest.approx(LCOE_DEMO)
        assert r["van"] == pytest.approx(VAN_DEMO)
        assert r["tir"] == pytest.approx(TIR_DEMO)
        assert r["payback"] == 11
        assert r["verdetto"] == "CONVIENTE"


class TestUI:
    def _app(self):
        return Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")

    def test_label_presente(self):
        assert TITLE656 in self._app()

    def test_helpers_presenti(self):
        assert "# W656 (23/10/2026) - tab656" in self._app()

    def test_chain_bumpata(self):
        assert ", tab655, tab656, tab657, tab658, tab659, tab660, tab661, tab662, tab663, tab664, tab665, tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682 = st.tabs([" in self._app()

    def test_tab_count_656(self):
        src = self._app()
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 682
        assert TITLE656 in titoli
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab656" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab656" in withs

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st656_[a-z0-9_]+)"', self._app())
        assert len(keys) >= 20
        assert len(set(keys)) == len(keys)
        # nessuna collisione con le chiavi del ciclo precedente
        assert not any(k.startswith("st655_") for k in keys)

    def test_csv_filename(self):
        assert "maree.csv" in self._app()

    def test_nessun_segreto_nella_sezione(self):
        src = self._app()
        sez = src.split("# W656 (23/10/2026)")[1].split("# W655 (23/10/2026)")[0]
        assert not re.search(r'(?i)(api_key|secret|password)\s*=\s*["\']',
                             sez)
