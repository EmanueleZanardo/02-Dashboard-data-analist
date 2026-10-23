"""Test tab663 "🌡️💨 Essiccazione industriale: quanta energia per togliere l'acqua?"

Demo calcolata a mano: 10.000 t/anno di prodotto umido (u_in 0,35,
u_out 0,12); calore latente effettivo 2.500 kJ/kg; essiccatore a
gas eta 0,55 (gas 75 EUR/MWh, O&M 40.000 EUR/anno); essiccatore a
PdC COP 3,5 (T processo 70 C <= T max 90 C; elettricita'
130 EUR/MWh, O&M 25.000 EUR/anno); CAPEX 950.000 EUR; fattori CO2
gas 0,202 / rete 0,25 t/MWh; 6 %, 15 anni, tolleranza 0,10.

- m_acqua = 10.000 x (0,35 - 0,12) / (1 - 0,12)
         = 2.613,6364 t/anno
- Q_evap = 2.613,6364 x 1.000 x 2.500 / 3.600.000
        = 1.815,0253 MWh/anno
- F_base = 1.815,0253 / 0,55 = 3.300,0459 MWh/anno (PCI)
- E_hp = 1.815,0253 / 3,5 = 518,5786 MWh/anno
- costo base = 3.300,0459 x 75 + 40.000
            = 247.503,44 + 40.000 = 287.503,44 EUR/anno
- costo PdC = 518,5786 x 130 + 25.000
           = 67.415,22 + 25.000 = 92.415,22 EUR/anno
- risparmio = 287.503,44 - 92.415,22 = 195.088,22 EUR/anno
- co2 evitata = 3.300,0459 x 0,202 - 518,5786 x 0,25
             = 666,6093 - 129,6447 = 536,9646 t/anno
- flussi [-950.000, 195.088,22 x 15];
  VAN(6 %) = 944.745,3658646739 EUR -> CONVIENTE
- TIR = 0,19030210797327318 (19,0302 %); payback anno 5
  (cum 4 = 4 x 195.088,22 - 950.000 = -169.647,12 < 0;
   cum 5 = +25.441,10 >= 0)
"""

import ast
import math
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh663_num", "mh663_nneg", "mh663_pos", "mh663_int_pos",
           "mh663_frazione", "mh663_eta",
           "mh663_acqua_t_anno", "mh663_q_evap_mwh",
           "mh663_f_base_mwh_pci", "mh663_costo_base_annuo",
           "mh663_hp_valido", "mh663_e_hp_mwh_el",
           "mh663_costo_hp_annuo", "mh663_risparmio_eur",
           "mh663_co2_evitata_t", "mh663_capex", "mh663_flussi",
           "mh663_van", "mh663_tir", "mh663_payback",
           "mh663_verdetto", "mh663_demo", "mh663_demo_calcoli")

TITLE663 = "🌡️💨 Essiccazione industriale: quanta energia per togliere l'acqua?"

M_ACQUA_DEMO = 2613.6363636363635
Q_EVAP_DEMO = 1815.0252525252522
F_BASE_DEMO = 3300.0459136822765
COSTO_BASE_DEMO = 287503.44352617074
E_HP_DEMO = 518.5786435786434
COSTO_HP_DEMO = 92415.22366522365
RISP_DEMO = 195088.2198609471
CO2_DEMO = 536.964613669159
CAPEX_DEMO = 950000.0
VAN_DEMO = 944745.3658646739
TIR_DEMO = 0.19030210797327318
VITA_DEMO = 15
PAYBACK_DEMO = 5
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w663_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _helpers_src():
    return (_new_dir() / "w663_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w663_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh663_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh663_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh663_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh663_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh663_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh663_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh663_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh663_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh663_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh663_int_pos"](True, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh663_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh663_int_pos"](15.0, "x") == 15

    def test_frazione_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh663_frazione"](1.1, "x")

    def test_frazione_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh663_frazione"](-0.1, "x")

    def test_frazione_accetta_bordi(self):
        assert _F["mh663_frazione"](0.0, "x") == 0.0
        assert _F["mh663_frazione"](1.0, "x") == 1.0

    def test_eta_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh663_eta"](0.0, "x")

    def test_eta_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh663_eta"](1.01, "x")

    def test_eta_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh663_eta"](-0.5, "x")

    def test_eta_accetta_uno(self):
        assert _F["mh663_eta"](1.0, "x") == 1.0


class TestFisica:
    def test_acqua_demo(self):
        assert _F["mh663_acqua_t_anno"](10000.0, 0.35,
                                        0.12) == pytest.approx(
            M_ACQUA_DEMO, rel=REL)

    def test_acqua_zero_se_stessa_umidita(self):
        assert _F["mh663_acqua_t_anno"](10000.0, 0.2,
                                        0.2) == pytest.approx(0.0)

    def test_acqua_negativa_se_u_out_maggiore(self):
        # regime degenere: la UI deve fermarsi prima dei KPI
        a = _F["mh663_acqua_t_anno"](10000.0, 0.10, 0.20)
        assert a < 0.0

    def test_acqua_rifiuta_u_out_uguale_uno(self):
        with pytest.raises(ValueError):
            _F["mh663_acqua_t_anno"](10000.0, 0.35, 1.0)

    def test_acqua_rifiuta_u_in_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh663_acqua_t_anno"](10000.0, 1.5, 0.12)

    def test_q_evap_demo(self):
        assert _F["mh663_q_evap_mwh"](M_ACQUA_DEMO,
                                      2500.0) == pytest.approx(
            Q_EVAP_DEMO, rel=REL)

    def test_q_evap_scala_lineare(self):
        q1 = _F["mh663_q_evap_mwh"](1000.0, 2500.0)
        q2 = _F["mh663_q_evap_mwh"](2000.0, 2500.0)
        assert q2 == pytest.approx(2.0 * q1, rel=REL)

    def test_q_evap_rifiuta_h_fg_zero(self):
        with pytest.raises(ValueError):
            _F["mh663_q_evap_mwh"](1000.0, 0.0)

    def test_f_base_demo(self):
        assert _F["mh663_f_base_mwh_pci"](Q_EVAP_DEMO,
                                          0.55) == pytest.approx(
            F_BASE_DEMO, rel=REL)

    def test_f_base_eta_uno_uguale_q(self):
        assert _F["mh663_f_base_mwh_pci"](800.0, 1.0) == \
            pytest.approx(800.0, rel=REL)

    def test_f_base_rifiuta_eta_zero(self):
        with pytest.raises(ValueError):
            _F["mh663_f_base_mwh_pci"](800.0, 0.0)

    def test_costo_base_demo(self):
        assert _F["mh663_costo_base_annuo"](F_BASE_DEMO, 75.0,
                                            40000.0) == pytest.approx(
            COSTO_BASE_DEMO, rel=REL)

    def test_costo_base_solo_om(self):
        c = _F["mh663_costo_base_annuo"](0.0, 75.0, 40000.0)
        assert c == pytest.approx(40000.0, rel=REL)

    def test_hp_valido_uguale(self):
        assert _F["mh663_hp_valido"](90.0, 90.0) is True

    def test_hp_valido_demo(self):
        assert _F["mh663_hp_valido"](70.0, 90.0) is True

    def test_hp_non_valido_t_processo_maggiore(self):
        assert _F["mh663_hp_valido"](100.0, 90.0) is False

    def test_e_hp_demo(self):
        assert _F["mh663_e_hp_mwh_el"](Q_EVAP_DEMO,
                                       3.5) == pytest.approx(
            E_HP_DEMO, rel=REL)

    def test_e_hp_cop_maggiore_meno_mwh(self):
        e1 = _F["mh663_e_hp_mwh_el"](800.0, 2.0)
        e2 = _F["mh663_e_hp_mwh_el"](800.0, 4.0)
        assert e2 == pytest.approx(0.5 * e1, rel=REL)

    def test_e_hp_rifiuta_cop_zero(self):
        with pytest.raises(ValueError):
            _F["mh663_e_hp_mwh_el"](800.0, 0.0)

    def test_costo_hp_demo(self):
        assert _F["mh663_costo_hp_annuo"](E_HP_DEMO, 130.0,
                                          25000.0) == pytest.approx(
            COSTO_HP_DEMO, rel=REL)

    def test_costo_hp_solo_om(self):
        c = _F["mh663_costo_hp_annuo"](0.0, 130.0, 25000.0)
        assert c == pytest.approx(25000.0, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh663_risparmio_eur"](COSTO_BASE_DEMO,
                                        COSTO_HP_DEMO) == \
            pytest.approx(RISP_DEMO, rel=REL)

    def test_risparmio_zero_se_uguali(self):
        assert _F["mh663_risparmio_eur"](100.0, 100.0) == \
            pytest.approx(0.0)

    def test_risparmio_negativo_possibile(self):
        assert _F["mh663_risparmio_eur"](100.0, 200.0) == \
            pytest.approx(-100.0)

    def test_co2_demo(self):
        assert _F["mh663_co2_evitata_t"](F_BASE_DEMO, 0.202,
                                         E_HP_DEMO,
                                         0.25) == pytest.approx(
            CO2_DEMO, rel=REL)

    def test_co2_segno_negativo_possibile(self):
        # rete sporca: la PdC peggiora il bilancio CO2
        c = _F["mh663_co2_evitata_t"](1000.0, 0.202, 1000.0, 1.5)
        assert c == pytest.approx(-1298.0, rel=REL)

    def test_co2_zero_se_nulla(self):
        assert _F["mh663_co2_evitata_t"](0.0, 0.202, 0.0, 0.25) == \
            pytest.approx(0.0)

    def test_capex_demo(self):
        assert _F["mh663_capex"](950000.0) == pytest.approx(
            CAPEX_DEMO, rel=REL)

    def test_capex_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh663_capex"](-1.0)


class TestFinanza:
    def _flussi_demo(self):
        return _F["mh663_flussi"](CAPEX_DEMO, RISP_DEMO, VITA_DEMO)

    def test_flussi_struttura(self):
        fl = self._flussi_demo()
        assert fl[0] == -CAPEX_DEMO and len(fl) == 16
        assert all(f == RISP_DEMO for f in fl[1:])

    def test_flussi_rifiuta_vita_zero(self):
        with pytest.raises(ValueError):
            _F["mh663_flussi"](100.0, 10.0, 0)

    def test_van_demo(self):
        assert _F["mh663_van"](self._flussi_demo(),
                               0.06) == pytest.approx(VAN_DEMO,
                                                      rel=REL)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh663_van"](self._flussi_demo(), -0.01)

    def test_van_tasso_zero(self):
        fl = [-100.0, 30.0, 30.0]
        assert _F["mh663_van"](fl, 0.0) == pytest.approx(-40.0)

    def test_tir_demo(self):
        assert _F["mh663_tir"](self._flussi_demo()) == pytest.approx(
            TIR_DEMO, rel=REL)

    def test_tir_none_senza_cambio_segno(self):
        assert _F["mh663_tir"]([-100.0, -10.0, -10.0]) is None

    def test_payback_demo(self):
        assert _F["mh663_payback"](self._flussi_demo()) == PAYBACK_DEMO

    def test_payback_none_mai(self):
        assert _F["mh663_payback"]([-100.0, 1.0, 1.0]) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh663_verdetto"](VAN_DEMO, CAPEX_DEMO, RISP_DEMO,
                                    0.10) == VERDETTO_DEMO

    def test_verdetto_marginale(self):
        assert _F["mh663_verdetto"](-95000.0, 950000.0, 100.0,
                                    0.10) == "MARGINALE"

    def test_verdetto_non_conviente(self):
        assert _F["mh663_verdetto"](-500000.0, 950000.0, 100.0,
                                    0.10) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risp_zero(self):
        assert _F["mh663_verdetto"](500.0, 950000.0, 0.0,
                                    0.10) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_risp_none(self):
        assert _F["mh663_verdetto"](500.0, 950000.0, None,
                                    0.10) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_van_none(self):
        assert _F["mh663_verdetto"](None, 950000.0, 100.0,
                                    0.10) == "NON_CALCOLABILE"

    def test_verdetto_rifiuta_tolleranza_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh663_verdetto"](100.0, 950000.0, 100.0, 1.5)


class TestDemo:
    def test_demo_calcoli_end_to_end(self):
        c = _F["mh663_demo_calcoli"]()
        assert c["m_acqua_t_anno"] == pytest.approx(M_ACQUA_DEMO,
                                                   rel=REL)
        assert c["q_evap_mwh_anno"] == pytest.approx(Q_EVAP_DEMO,
                                                    rel=REL)
        assert c["f_base_mwh_anno"] == pytest.approx(F_BASE_DEMO,
                                                     rel=REL)
        assert c["e_hp_mwh_anno"] == pytest.approx(E_HP_DEMO,
                                                  rel=REL)
        assert c["costo_base_eur_anno"] == pytest.approx(
            COSTO_BASE_DEMO, rel=REL)
        assert c["costo_hp_eur_anno"] == pytest.approx(
            COSTO_HP_DEMO, rel=REL)
        assert c["risparmio_eur_anno"] == pytest.approx(
            RISP_DEMO, rel=REL)
        assert c["co2_evitata_t_anno"] == pytest.approx(
            CO2_DEMO, rel=REL)
        assert c["capex_eur"] == pytest.approx(CAPEX_DEMO, rel=REL)
        assert c["van_eur"] == pytest.approx(VAN_DEMO, rel=REL)
        assert c["tir"] == pytest.approx(TIR_DEMO, rel=REL)
        assert c["payback_anni"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO

    def test_demo_calcoli_deterministico(self):
        assert _F["mh663_demo_calcoli"]() == _F["mh663_demo_calcoli"]()

    def test_demo_calcoli_contro_demo(self):
        # i default della UI riproducono la demo: mismatch < 1e-9 rel
        d = _F["mh663_demo"]()
        c = _F["mh663_demo_calcoli"]()
        m = _F["mh663_acqua_t_anno"](d["m_prodotto_umido_t_anno"],
                                     d["u_in"], d["u_out"])
        assert m == pytest.approx(c["m_acqua_t_anno"], rel=REL)

    def test_demo_defaults(self):
        d = _F["mh663_demo"]()
        assert d["m_prodotto_umido_t_anno"] == 10000.0
        assert d["u_in"] == 0.35
        assert d["u_out"] == 0.12
        assert d["h_fg_eff_kj_kg"] == 2500.0
        assert d["eta_base"] == 0.55
        assert d["p_gas"] == 75.0
        assert d["om_base"] == 40000.0
        assert d["cop"] == 3.5
        assert d["t_processo_c"] == 70.0
        assert d["t_max_hp_c"] == 90.0
        assert d["p_el"] == 130.0
        assert d["om_hp"] == 25000.0
        assert d["capex"] == 950000.0
        assert d["f_co2_gas"] == 0.202
        assert d["f_co2_el"] == 0.25
        assert d["tasso"] == 0.06
        assert d["vita_anni"] == 15
        assert d["tolleranza"] == 0.10


class TestUI:
    def test_header_helpers_presente(self):
        assert '# W663 (23/10/2026) - tab663' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh663_num", "mh663_nneg", "mh663_pos",
                     "mh663_int_pos", "mh663_frazione", "mh663_eta",
                     "mh663_acqua_t_anno", "mh663_q_evap_mwh",
                     "mh663_f_base_mwh_pci",
                     "mh663_costo_base_annuo", "mh663_hp_valido",
                     "mh663_e_hp_mwh_el", "mh663_costo_hp_annuo",
                     "mh663_risparmio_eur", "mh663_co2_evitata_t",
                     "mh663_capex", "mh663_flussi", "mh663_van",
                     "mh663_tir", "mh663_payback", "mh663_verdetto",
                     "mh663_demo", "mh663_demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE663) == 1

    def test_blocco_with_tab663(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab663:"

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st663_[a-z0-9_]+)"', _ui_src())
        assert len(keys) >= 20
        assert len(set(keys)) == len(keys)
        # nessuna collisione con le chiavi del ciclo precedente
        assert not any(k.startswith("st662_") for k in keys)

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg663" in src
        assert "(_macc663 <= 0.0)" in src
        assert "_rs663 <= 0.0" in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg663") < src.index(".metric(")
        assert src.index("_rs663 <= 0.0") < src.index(".metric(")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Acqua evaporata (t/anno)" in src
        assert "Risparmio (€/anno)" in src
        assert "CO2 evitata (t/anno)" in src
        assert "Payback (anni)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd663" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_guard_hp_non_valida_presente(self):
        src = _ui_src()
        assert "mh663_hp_valido" in src
        assert src.index("mh663_hp_valido") < src.index(".metric(")

    def test_grafico_costi_presente(self):
        src = _ui_src()
        assert "plotly.graph_objects" in src
        assert "barmode" in src
        assert "Essiccatore a gas" in src
        assert "Essiccatore a pompa di calore" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert 'sep=";"' in src
        assert "essiccazione_industriale.csv" in src

    def test_differenziazione_da_tab662(self):
        src = _ui_src()
        assert "tab662" in src
        assert "Forno a induzione" in src

    def test_nessun_segreto_nella_sezione(self):
        assert not re.search(r'(?i)(api_key|secret|password)\s*=\s*["\']',
                             _ui_src())
