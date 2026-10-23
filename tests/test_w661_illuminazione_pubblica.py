"""Test tab661 "💡🌃 Illuminazione pubblica: LED + telecontrollo — il business case"

Demo calcolata a mano: Comune con 500 punti luce; SAP 150 W -> LED
70 W; 4.200 h/anno di accensione; dimming 25 %; energia 0,22
EUR/kWh; manutenzione 12 -> 3 EUR/punto/anno; CAPEX 450 EUR/punto;
CO2 0,35 kg/kWh; 5 %, 15 anni, tolleranza 0,10 (frazione del CAPEX).

- e_old = 500 x 150 x 4.200 / 1.000 = 315.000 kWh/anno
- e_new (con dimming) = 500 x 70 x 4.200 x 0,75 / 1.000
        = 110.250 kWh/anno
- e_new (senza dimming) = 500 x 70 x 4.200 / 1.000
        = 147.000 kWh/anno
- risp_kwh = 315.000 - 110.250 = 204.750 kWh/anno
        = 204,75 MWh/anno
- risp_energia = 204.750 x 0,22 = 45.045 EUR/anno
- risp_manut = 500 x (12 - 3) = 4.500 EUR/anno
- risp_tot = 45.045 + 4.500 = 49.545 EUR/anno
- capex = 500 x 450 = 225.000 EUR
- co2 = 204.750 x 0,35 / 1.000 = 71,6625 t/anno
- flussi [-225.000, 49.545 x 15];
  VAN(5 %) = 289.260,1575016574 EUR -> CONVIENTE
- TIR = 0,20712169417287857 (20,7122 %); payback anno 5
  (cum 4 = 4 x 49.545 - 225.000 = -26.820 < 0;
   cum 5 = +22.725 >= 0)
"""

import ast
import math
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh661_num", "mh661_nneg", "mh661_pos", "mh661_int_pos",
           "mh661_frazione", "mh661_energia_old_kwh",
           "mh661_energia_new_kwh", "mh661_risparmio_kwh",
           "mh661_risparmio_energia_eur",
           "mh661_risparmio_manut_eur", "mh661_risparmio_tot_eur",
           "mh661_capex", "mh661_co2_t", "mh661_flussi", "mh661_van",
           "mh661_tir", "mh661_payback", "mh661_verdetto",
           "mh661_demo", "mh661_demo_calcoli")

TITLE661 = "💡🌃 Illuminazione pubblica: LED + telecontrollo — il business case"

E_OLD_DEMO = 315000.0
E_NEW_DEMO = 110250.0
E_NEW_NODIM_DEMO = 147000.0
RISP_KWH_DEMO = 204750.0
RISP_EN_DEMO = 45045.0
RISP_MAN_DEMO = 4500.0
RISP_TOT_DEMO = 49545.0
CAPEX_DEMO = 225000.0
CO2_DEMO = 71.6625
VAN_DEMO = 289260.1575016574
TIR_DEMO = 0.20712169417287857
VITA_DEMO = 15
PAYBACK_DEMO = 5
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w661_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _helpers_src():
    return (_new_dir() / "w661_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w661_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh661_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh661_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh661_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh661_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh661_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh661_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh661_pos"](0.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh661_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh661_int_pos"](True, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh661_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh661_int_pos"](15.0, "x") == 15

    def test_frazione_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh661_frazione"](1.1, "x")

    def test_frazione_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh661_frazione"](-0.1, "x")

    def test_frazione_accetta_bordi(self):
        assert _F["mh661_frazione"](0.0, "x") == 0.0
        assert _F["mh661_frazione"](1.0, "x") == 1.0


class TestFisica:
    def test_energia_old_demo(self):
        assert _F["mh661_energia_old_kwh"](500, 150.0, 4200.0) == \
            pytest.approx(E_OLD_DEMO, rel=REL)

    def test_energia_new_demo(self):
        assert _F["mh661_energia_new_kwh"](500, 70.0, 4200.0, 0.25) == \
            pytest.approx(E_NEW_DEMO, rel=REL)

    def test_energia_new_nodim(self):
        assert _F["mh661_energia_new_kwh"](500, 70.0, 4200.0, 0.0) == \
            pytest.approx(E_NEW_NODIM_DEMO, rel=REL)

    def test_energia_new_dimming_riduce(self):
        nodim = _F["mh661_energia_new_kwh"](500, 70.0, 4200.0, 0.0)
        dim = _F["mh661_energia_new_kwh"](500, 70.0, 4200.0, 0.5)
        assert dim == pytest.approx(nodim * 0.5, rel=REL)

    def test_energia_quota_uno_zero(self):
        assert _F["mh661_energia_new_kwh"](500, 70.0, 4200.0, 1.0) == \
            pytest.approx(0.0)

    def test_energia_rifiuta_quota_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh661_energia_new_kwh"](500, 70.0, 4200.0, 1.01)

    def test_energia_rifiuta_ore_oltre_8760(self):
        with pytest.raises(ValueError):
            _F["mh661_energia_old_kwh"](500, 150.0, 9000.0)
        with pytest.raises(ValueError):
            _F["mh661_energia_new_kwh"](500, 70.0, 9000.0, 0.25)

    def test_energia_rifiuta_n_zero(self):
        with pytest.raises(ValueError):
            _F["mh661_energia_old_kwh"](0, 150.0, 4200.0)

    def test_energia_rifiuta_potenza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh661_energia_old_kwh"](500, -1.0, 4200.0)

    def test_risparmio_demo(self):
        assert _F["mh661_risparmio_kwh"](E_OLD_DEMO, E_NEW_DEMO) == \
            pytest.approx(RISP_KWH_DEMO, rel=REL)

    def test_risparmio_zero_se_uguali(self):
        assert _F["mh661_risparmio_kwh"](1000.0, 1000.0) == \
            pytest.approx(0.0)

    def test_risparmio_negativo_possibile(self):
        assert _F["mh661_risparmio_kwh"](1000.0, 1200.0) == \
            pytest.approx(-200.0)

    def test_risparmio_rifiuta_negativo_ingresso(self):
        with pytest.raises(ValueError):
            _F["mh661_risparmio_kwh"](-10.0, 100.0)

    def test_risparmio_energia_demo(self):
        assert _F["mh661_risparmio_energia_eur"](RISP_KWH_DEMO, 0.22) == \
            pytest.approx(RISP_EN_DEMO, rel=REL)

    def test_risparmio_manut_demo(self):
        assert _F["mh661_risparmio_manut_eur"](500, 12.0, 3.0) == \
            pytest.approx(RISP_MAN_DEMO, rel=REL)

    def test_risparmio_manut_negativo_possibile(self):
        assert _F["mh661_risparmio_manut_eur"](500, 3.0, 12.0) == \
            pytest.approx(-RISP_MAN_DEMO, rel=REL)

    def test_risparmio_tot_demo(self):
        assert _F["mh661_risparmio_tot_eur"](RISP_EN_DEMO,
                                             RISP_MAN_DEMO) == \
            pytest.approx(RISP_TOT_DEMO, rel=REL)

    def test_capex_demo(self):
        assert _F["mh661_capex"](500, 450.0) == \
            pytest.approx(CAPEX_DEMO, rel=REL)

    def test_co2_demo(self):
        assert _F["mh661_co2_t"](RISP_KWH_DEMO, 0.35) == \
            pytest.approx(CO2_DEMO, rel=REL)

    def test_co2_none_se_risparmio_zero(self):
        assert _F["mh661_co2_t"](0.0, 0.35) is None

    def test_co2_none_se_risparmio_negativo(self):
        assert _F["mh661_co2_t"](-100.0, 0.35) is None

    def test_co2_rifiuta_fattore_negativo(self):
        with pytest.raises(ValueError):
            _F["mh661_co2_t"](100.0, -0.1)


class TestFinanza:
    def _flussi_demo(self):
        return _F["mh661_flussi"](CAPEX_DEMO, RISP_TOT_DEMO, VITA_DEMO)

    def test_flussi_struttura(self):
        fl = self._flussi_demo()
        assert fl[0] == -CAPEX_DEMO and len(fl) == 16
        assert all(f == RISP_TOT_DEMO for f in fl[1:])

    def test_flussi_rifiuta_vita_zero(self):
        with pytest.raises(ValueError):
            _F["mh661_flussi"](100.0, 10.0, 0)

    def test_van_demo(self):
        assert _F["mh661_van"](self._flussi_demo(), 5.0) == \
            pytest.approx(VAN_DEMO, rel=REL)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh661_van"](self._flussi_demo(), -1.0)

    def test_tir_demo(self):
        assert _F["mh661_tir"](self._flussi_demo()) == \
            pytest.approx(TIR_DEMO, rel=REL)

    def test_tir_none_senza_cambio_segno(self):
        assert _F["mh661_tir"]([-100.0, -10.0, -10.0]) is None

    def test_payback_demo(self):
        assert _F["mh661_payback"](self._flussi_demo()) == PAYBACK_DEMO

    def test_payback_none_mai(self):
        assert _F["mh661_payback"]([-100.0, 1.0, 1.0]) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh661_verdetto"](VAN_DEMO, CAPEX_DEMO, RISP_TOT_DEMO,
                                    0.10) == VERDETTO_DEMO

    def test_verdetto_marginale(self):
        assert _F["mh661_verdetto"](-22500.0, 225000.0, 100.0,
                                    0.10) == "MARGINALE"

    def test_verdetto_non_conviente(self):
        assert _F["mh661_verdetto"](-50000.0, 225000.0, 100.0,
                                    0.10) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risp_zero(self):
        assert _F["mh661_verdetto"](500.0, 225000.0, 0.0,
                                    0.10) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_risp_none(self):
        assert _F["mh661_verdetto"](500.0, 225000.0, None,
                                    0.10) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_van_none(self):
        assert _F["mh661_verdetto"](None, 225000.0, 100.0,
                                    0.10) == "NON_CALCOLABILE"

    def test_verdetto_rifiuta_tolleranza_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh661_verdetto"](100.0, 225000.0, 100.0, 1.5)


class TestDemo:
    def test_demo_calcoli_end_to_end(self):
        c = _F["mh661_demo_calcoli"]()
        assert c["e_old_kwh_anno"] == pytest.approx(E_OLD_DEMO,
                                                    rel=REL)
        assert c["e_new_kwh_anno"] == pytest.approx(E_NEW_DEMO,
                                                   rel=REL)
        assert c["e_new_nodim_kwh_anno"] == pytest.approx(
            E_NEW_NODIM_DEMO, rel=REL)
        assert c["risp_kwh_anno"] == pytest.approx(RISP_KWH_DEMO,
                                                  rel=REL)
        assert c["risp_energia_eur_anno"] == pytest.approx(
            RISP_EN_DEMO, rel=REL)
        assert c["risp_manut_eur_anno"] == pytest.approx(
            RISP_MAN_DEMO, rel=REL)
        assert c["risp_tot_eur_anno"] == pytest.approx(RISP_TOT_DEMO,
                                                      rel=REL)
        assert c["capex_eur"] == pytest.approx(CAPEX_DEMO, rel=REL)
        assert c["co2_t_anno"] == pytest.approx(CO2_DEMO, rel=REL)
        assert c["van_eur"] == pytest.approx(VAN_DEMO, rel=REL)
        assert c["tir"] == pytest.approx(TIR_DEMO, rel=REL)
        assert c["payback_anni"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO

    def test_demo_calcoli_deterministico(self):
        assert _F["mh661_demo_calcoli"]() == _F["mh661_demo_calcoli"]()

    def test_demo_calcoli_contro_demo(self):
        # i default della UI riproducono la demo: mismatch < 1e-9 rel
        d = _F["mh661_demo"]()
        c = _F["mh661_demo_calcoli"]()
        e_old = _F["mh661_energia_old_kwh"](d["n_punti"], d["p_old_w"],
                                            d["ore_anno"])
        assert e_old == pytest.approx(c["e_old_kwh_anno"], rel=REL)

    def test_demo_defaults(self):
        d = _F["mh661_demo"]()
        assert d["n_punti"] == 500
        assert d["p_old_w"] == 150.0
        assert d["p_new_w"] == 70.0
        assert d["ore_anno"] == 4200.0
        assert d["quota_dimming"] == 0.25
        assert d["prezzo_el"] == 0.22
        assert d["manut_old"] == 12.0
        assert d["manut_new"] == 3.0
        assert d["capex_punto"] == 450.0
        assert d["f_co2"] == 0.35
        assert d["tasso_pct"] == 5.0
        assert d["vita_anni"] == 15
        assert d["tolleranza"] == 0.10


class TestUI:
    def test_header_helpers_presente(self):
        assert '# W661 (23/10/2026) - tab661' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh661_num", "mh661_nneg", "mh661_pos",
                     "mh661_int_pos", "mh661_frazione",
                     "mh661_energia_old_kwh", "mh661_energia_new_kwh",
                     "mh661_risparmio_kwh",
                     "mh661_risparmio_energia_eur",
                     "mh661_risparmio_manut_eur",
                     "mh661_risparmio_tot_eur", "mh661_capex",
                     "mh661_co2_t", "mh661_flussi", "mh661_van",
                     "mh661_tir", "mh661_payback", "mh661_verdetto",
                     "mh661_demo", "mh661_demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE661) == 1

    def test_blocco_with_tab661(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab661:"

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st661_[a-z0-9_]+)"', _ui_src())
        assert len(keys) >= 15
        assert len(set(keys)) == len(keys)
        # nessuna collisione con le chiavi del ciclo precedente
        assert not any(k.startswith("st660_") for k in keys)

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg661" in src
        assert "(_rk661 <= 0.0)" in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg661") < src.index(".metric(")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Risparmio energia (MWh/anno)" in src
        assert "Risparmio economico" in src
        assert "CO2 evitata (t/anno)" in src
        assert "Payback (anni)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd661" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_grafico_consumi_presente(self):
        src = _ui_src()
        assert "plotly.graph_objects" in src
        assert "LED senza dimming" in src
        assert "LED con dimming" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert 'sep=";"' in src
        assert "illuminazione_pubblica.csv" in _ui_src()

    def test_differenziazione_da_tab649(self):
        src = _ui_src()
        assert "tab649" in src
        assert "telecontrollo" in src

    def test_nessun_segreto_nella_sezione(self):
        assert not re.search(r'(?i)(api_key|secret|password)\s*=\s*["\']',
                             _ui_src())
