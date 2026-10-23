"""Test tab660 "⚖️ Sbilanciamento fasi: quanto costa la corrente nel neutro?"

Demo calcolata a mano: Va 228 V, Vb 230 V, Vc 200 V; Ia 95 A,
Ib 102 A, Ic 88 A; motore 400 kW; 7.000 h/anno; prezzo
elettricita' 0,28 EUR/kWh; O&M 800 EUR/anno; fattore CO2
0,30 kg/kWh; portata neutro 40 A; CAPEX diretto 12.000 EUR;
6 %, 15 anni, tolleranza 0,10 (frazione del CAPEX).

Con a = -0,5 + j0,8660254 (exp(j120°)), a^2 = -0,5 - j0,8660254:

- V1 = (228 + 230 + 200)/3 = 658/3 = 219,3333 V (reale)
- V2 = (228 + 230*a + 200*a^2)/3
     = (228 - 115 - 100 + j(199,1858 - 173,2051))/3
     = (13 + j25,9808)/3 = 4,3333 + j8,6603
  |V2| = sqrt(4,3333^2 + 8,6603^2) = sqrt(93,7778) = 9,6844
- VUF = 9,6844/219,3333 x 100 = 4,41515 %
- IN = |95 + 102*a^2 + 88*a|
     = |95 - 51 - 44 + j(-88,3346 + 76,2102)| = 12,1244 A
- allarme neutro: 12,1244 > 0,30 x 40 = 12,0 -> True
- derating NEMA (interp. tra (4, 0,87) e (5, 0,81)):
  0,87 - 0,06 x (4,4151486 - 4) = 0,8450911
- P_extra = 400 x 2 x (4,4151486/100)^2 = 800 x 0,0019493538
        = 1,559483 kW  (stima: aumento termico % = 2 x (VUF%)^2)
- E_extra = 1,559483 x 7.000 = 10.916,381 kWh/anno
- lordo = 10.916,381 x 0,28 = 3.056,5867 EUR/anno
- netto = 3.056,5867 - 800 = 2.256,5867 EUR/anno
- CO2 extra = 10.916,381 x 0,30 / 1.000 = 3,27491 t/anno
- flussi [-12.000, 2.256,5867 x 15];
  VAN(6 %) = 9.916,53180357225 EUR -> CONVIENTE
- TIR = 0,17026602127436274 (17,0266 %); payback anno 6
  (cum 5 = 5 x 2.256,5867 - 12.000 = -717,07 < 0;
   cum 6 = +1.539,52 >= 0)
"""

import math
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh660_num", "mh660_nneg", "mh660_pos", "mh660_int_pos",
           "mh660_frazione", "mh660_vuf_pct",
           "mh660_corrente_neutro", "mh660_derating",
           "mh660_perdite_extra_kw", "mh660_energia_extra_kwh",
           "mh660_risparmio_lordo_eur", "mh660_risparmio_netto_eur",
           "mh660_co2_t", "mh660_capex_da_specifico", "mh660_flussi",
           "mh660_van", "mh660_tir", "mh660_payback",
           "mh660_verdetto", "mh660_neutro_allarme", "mh660_demo",
           "mh660_demo_calcoli")

TITLE660 = "⚖️ Sbilanciamento fasi: quanto costa la corrente nel neutro?"

VUF_DEMO = 4.415148646302107
IN_DEMO = 12.124355652982132
DERATING_DEMO = 0.8450910812218736
P_EXTRA_DEMO = 1.5594830055154663
E_EXTRA_DEMO = 10916.381038608264
LORDO_DEMO = 3056.5866908103144
NETTO_DEMO = 2256.5866908103144
CO2_DEMO = 3.2749143115824793
CAPEX_DEMO = 12000.0
VAN_DEMO = 9916.53180357225
TIR_DEMO = 0.17026602127436274
VITA_DEMO = 15
PAYBACK_DEMO = 6
VERDETTO_DEMO = "CONVIENTE"


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w660_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _helpers_src():
    return (_new_dir() / "w660_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w660_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh660_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh660_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh660_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh660_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh660_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh660_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh660_pos"](0.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh660_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh660_int_pos"](True, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh660_int_pos"](15.0, "x") == 15

    def test_frazione_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh660_frazione"](1.1, "x")

    def test_frazione_accetta_bordi(self):
        assert _F["mh660_frazione"](0.0, "x") == 0.0
        assert _F["mh660_frazione"](1.0, "x") == 1.0


class TestFisica:
    def test_vuf_demo(self):
        assert _F["mh660_vuf_pct"](228.0, 230.0, 200.0) == \
            pytest.approx(VUF_DEMO)

    def test_vuf_zero_bilanciato(self):
        assert _F["mh660_vuf_pct"](230.0, 230.0, 230.0) == \
            pytest.approx(0.0)

    def test_vuf_cinquanta_fase_mancante(self):
        assert _F["mh660_vuf_pct"](230.0, 230.0, 1e-9) == \
            pytest.approx(50.0)

    def test_vuf_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh660_vuf_pct"](230.0, 230.0, 0.0)

    def test_vuf_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh660_vuf_pct"](-230.0, 230.0, 230.0)

    def test_neutro_demo(self):
        assert _F["mh660_corrente_neutro"](95.0, 102.0, 88.0) == \
            pytest.approx(IN_DEMO)

    def test_neutro_zero_bilanciato(self):
        assert _F["mh660_corrente_neutro"](100.0, 100.0, 100.0) == \
            pytest.approx(0.0)

    def test_neutro_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh660_corrente_neutro"](-1.0, 100.0, 100.0)

    def test_derating_demo(self):
        assert _F["mh660_derating"](VUF_DEMO) == \
            pytest.approx(DERATING_DEMO)

    def test_derating_punti_tabella(self):
        pts = [(0.0, 1.0), (1.0, 1.0), (2.0, 0.96), (3.0, 0.92),
               (4.0, 0.87), (5.0, 0.81)]
        for v, atteso in pts:
            assert _F["mh660_derating"](v) == pytest.approx(atteso)

    def test_derating_interpolazione(self):
        assert _F["mh660_derating"](1.5) == pytest.approx(0.98)
        assert _F["mh660_derating"](2.5) == pytest.approx(0.94)

    def test_derating_none_oltre_cinque(self):
        assert _F["mh660_derating"](5.0001) is None
        assert _F["mh660_derating"](10.0) is None

    def test_derating_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh660_derating"](-1.0)

    def test_perdite_extra_demo(self):
        assert _F["mh660_perdite_extra_kw"](400.0, VUF_DEMO) == \
            pytest.approx(P_EXTRA_DEMO)

    def test_perdite_extra_zero_se_vuf_zero(self):
        assert _F["mh660_perdite_extra_kw"](400.0, 0.0) == \
            pytest.approx(0.0)

    def test_perdite_extra_cresce_con_vuf(self):
        assert _F["mh660_perdite_extra_kw"](400.0, 4.0) > \
            _F["mh660_perdite_extra_kw"](400.0, 2.0)

    def test_energia_extra_demo(self):
        assert _F["mh660_energia_extra_kwh"](P_EXTRA_DEMO, 7000.0) == \
            pytest.approx(E_EXTRA_DEMO)

    def test_energia_extra_rifiuta_ore_oltre_8760(self):
        with pytest.raises(ValueError):
            _F["mh660_energia_extra_kwh"](1.0, 9000.0)

    def test_risparmio_lordo_demo(self):
        assert _F["mh660_risparmio_lordo_eur"](E_EXTRA_DEMO, 0.28) == \
            pytest.approx(LORDO_DEMO)

    def test_risparmio_netto_demo(self):
        assert _F["mh660_risparmio_netto_eur"](LORDO_DEMO, 800.0) == \
            pytest.approx(NETTO_DEMO)

    def test_risparmio_netto_negativo_possibile(self):
        assert _F["mh660_risparmio_netto_eur"](100.0, 800.0) == \
            pytest.approx(-700.0)

    def test_co2_demo(self):
        assert _F["mh660_co2_t"](E_EXTRA_DEMO, 0.30) == \
            pytest.approx(CO2_DEMO)

    def test_co2_none_se_non_positiva(self):
        assert _F["mh660_co2_t"](0.0, 0.30) is None
        assert _F["mh660_co2_t"](-5.0, 0.30) is None

    def test_capex_da_specifico(self):
        assert _F["mh660_capex_da_specifico"](400.0, 40.0) == \
            pytest.approx(16000.0)

    def test_neutro_allarme_true_demo(self):
        assert _F["mh660_neutro_allarme"](IN_DEMO, 40.0) is True

    def test_neutro_allarme_false(self):
        assert _F["mh660_neutro_allarme"](IN_DEMO, 100.0) is False

    def test_neutro_allarme_bordo_strict(self):
        # 30 A NON e' > 30 % di 100 A -> False (disuguaglianza stretta)
        assert _F["mh660_neutro_allarme"](30.0, 100.0) is False
        assert _F["mh660_neutro_allarme"](30.0001, 100.0) is True

    def test_neutro_allarme_rifiuta_portata_zero(self):
        with pytest.raises(ValueError):
            _F["mh660_neutro_allarme"](10.0, 0.0)


class TestFinanza:
    def _flussi_demo(self):
        return _F["mh660_flussi"](CAPEX_DEMO, NETTO_DEMO, VITA_DEMO)

    def test_flussi_struttura(self):
        fl = _F["mh660_flussi"](CAPEX_DEMO, NETTO_DEMO, VITA_DEMO)
        assert fl[0] == -CAPEX_DEMO and len(fl) == 16
        assert all(f == NETTO_DEMO for f in fl[1:])

    def test_van_demo(self):
        assert _F["mh660_van"](self._flussi_demo(), 6.0) == \
            pytest.approx(VAN_DEMO)

    def test_tir_demo(self):
        assert _F["mh660_tir"](self._flussi_demo()) == \
            pytest.approx(TIR_DEMO)

    def test_tir_none_senza_cambio_segno(self):
        assert _F["mh660_tir"]([-100.0, -10.0, -10.0]) is None

    def test_payback_demo(self):
        assert _F["mh660_payback"](self._flussi_demo()) == PAYBACK_DEMO

    def test_payback_none_mai(self):
        assert _F["mh660_payback"]([-100.0, 1.0, 1.0]) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh660_verdetto"](VAN_DEMO, CAPEX_DEMO, NETTO_DEMO,
                                    0.10) == VERDETTO_DEMO

    def test_verdetto_marginale(self):
        assert _F["mh660_verdetto"](-600.0, 12000.0, 100.0,
                                    0.10) == "MARGINALE"

    def test_verdetto_non_conviente(self):
        assert _F["mh660_verdetto"](-9000.0, 12000.0, 100.0,
                                    0.10) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile(self):
        assert _F["mh660_verdetto"](500.0, 12000.0, 0.0,
                                    0.10) == "NON_CALCOLABILE"
        assert _F["mh660_verdetto"](500.0, 12000.0, None,
                                    0.10) == "NON_CALCOLABILE"
        assert _F["mh660_verdetto"](None, 12000.0, 100.0,
                                    0.10) == "NON_CALCOLABILE"

    def test_verdetto_rifiuta_tolleranza_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh660_verdetto"](100.0, 12000.0, 100.0, 1.5)


class TestDemo:
    def test_demo_calcoli_end_to_end(self):
        c = _F["mh660_demo_calcoli"]()
        assert c["vuf_pct"] == pytest.approx(VUF_DEMO)
        assert c["in_a"] == pytest.approx(IN_DEMO)
        assert c["derating"] == pytest.approx(DERATING_DEMO)
        assert c["p_extra_kw"] == pytest.approx(P_EXTRA_DEMO)
        assert c["e_extra_kwh_anno"] == pytest.approx(E_EXTRA_DEMO)
        assert c["risparmio_lordo_eur_anno"] == \
            pytest.approx(LORDO_DEMO)
        assert c["risparmio_netto_eur_anno"] == \
            pytest.approx(NETTO_DEMO)
        assert c["co2_t_anno"] == pytest.approx(CO2_DEMO)
        assert c["capex_eur"] == CAPEX_DEMO
        assert c["van_eur"] == pytest.approx(VAN_DEMO)
        assert c["tir"] == pytest.approx(TIR_DEMO)
        assert c["payback_anni"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO
        assert c["neutro_allarme"] is True

    def test_demo_calcoli_deterministico(self):
        assert _F["mh660_demo_calcoli"]() == _F["mh660_demo_calcoli"]()

    def test_demo_defaults(self):
        d = _F["mh660_demo"]()
        assert d["va"] == 228.0
        assert d["vb"] == 230.0
        assert d["vc"] == 200.0
        assert d["ia"] == 95.0
        assert d["ib"] == 102.0
        assert d["ic"] == 88.0
        assert d["p_mot_kw"] == 400.0
        assert d["modo_capex"] == "CAPEX diretto (€)"
        assert d["capex_eur"] == 12000.0
        assert d["vita_anni"] == 15


class TestUI:
    def test_header_helpers_presente(self):
        assert '# W660 (23/10/2026) - tab660' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh660_num", "mh660_nneg", "mh660_pos",
                     "mh660_int_pos", "mh660_frazione",
                     "mh660_vuf_pct", "mh660_corrente_neutro",
                     "mh660_derating", "mh660_perdite_extra_kw",
                     "mh660_energia_extra_kwh",
                     "mh660_risparmio_lordo_eur",
                     "mh660_risparmio_netto_eur", "mh660_co2_t",
                     "mh660_capex_da_specifico", "mh660_flussi",
                     "mh660_van", "mh660_tir", "mh660_payback",
                     "mh660_verdetto", "mh660_neutro_allarme",
                     "mh660_demo", "mh660_demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE660) == 1

    def test_blocco_with_tab660(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab660:"

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st660_[a-z0-9_]+)"', _ui_src())
        assert len(keys) >= 20
        assert len(set(keys)) == len(keys)
        # nessuna collisione con le chiavi dei cicli precedenti
        assert not any(k.startswith("st659_") for k in keys)

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg660" in src
        assert "(_vuf660 <= 1.0) or (_rs660 <= 0.0)" in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg660") < src.index(".metric(")

    def test_note_derating_e_allarme_presenti(self):
        src = _ui_src()
        assert "_der660" in src
        assert "_al660" in src
        assert "30 %" in src

    def test_grafico_plotly_presente(self):
        assert "plotly.graph_objects" in _ui_src()

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert 'sep=";"' in src
        assert "sbilanciamento.csv" in _ui_src()

    def test_nessun_segreto_nella_sezione(self):
        assert not re.search(r'(?i)(api_key|secret|password)\s*=\s*["\']',
                             _ui_src())
