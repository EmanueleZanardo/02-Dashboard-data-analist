"""Test tab662 "🔥⚡ Forno a induzione: elettrificare il forno industriale paga?"

Demo calcolata a mano: 5.000 t/anno di acciaio (cp 0,49 kJ/(kg K),
dT 1.200 K); forno a gas eta 0,35 (gas 75 EUR/MWh, ETS 100 EUR/t,
fattore CO2 0,202 t/MWh, manutenzione 30.000 EUR/anno); forno a
induzione eta 0,90 (elettricita' 120 EUR/MWh, fattore CO2 rete
0,25 t/MWh, manutenzione 20.000 EUR/anno); CAPEX 1.100.000 EUR;
5 %, 15 anni, tolleranza 0,10 (frazione del CAPEX).

- Q = 5.000 x 1.000 x 0,49 x 1.200 / 3.600.000 = 816,6667 MWh/anno
- F_gas = 816,6667 / 0,35 = 2.333,3333 MWh/anno (PCI)
- E_ind = 816,6667 / 0,90 = 907,4074 MWh/anno
- costo gas = 2.333,3333 x 75 + 2.333,3333 x 0,202 x 100 + 30.000
           = 175.000 + 47.133,33 + 30.000 = 252.133,33 EUR/anno
- costo induzione = 907,4074 x 120 + 20.000
                 = 108.888,89 + 20.000 = 128.888,89 EUR/anno
- risparmio = 252.133,33 - 128.888,89 = 123.244,44 EUR/anno
- co2 evitata = 2.333,3333 x 0,202 - 907,4074 x 0,25
             = 471,3333 - 226,8519 = 244,4815 t/anno
- flussi [-1.100.000, 123.244,44 x 15];
  VAN(5 %) = 179.235,18843887906 EUR -> CONVIENTE
- TIR = 0,07322327202038711 (7,3223 %); payback anno 9
  (cum 8 = 8 x 123.244,44 - 1.100.000 = -114.044,44 < 0;
   cum 9 = +9.200 >= 0)
"""

import ast
import math
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh662_num", "mh662_nneg", "mh662_pos", "mh662_int_pos",
           "mh662_frazione", "mh662_eta",
           "mh662_calore_utile_mwh", "mh662_gas_mwh_pci",
           "mh662_elettricita_mwh", "mh662_costo_gas_annuo",
           "mh662_costo_induzione_annuo", "mh662_risparmio_eur",
           "mh662_co2_evitata_t", "mh662_capex", "mh662_flussi",
           "mh662_van", "mh662_tir", "mh662_payback",
           "mh662_verdetto", "mh662_demo", "mh662_demo_calcoli")

TITLE662 = "🔥⚡ Forno a induzione: elettrificare il forno industriale paga?"

Q_DEMO = 816.6666666666666
F_GAS_DEMO = 2333.3333333333335
E_IND_DEMO = 907.4074074074074
COSTO_GAS_DEMO = 252133.33333333334
COSTO_IND_DEMO = 128888.88888888889
RISP_DEMO = 123244.44444444445
CO2_DEMO = 244.48148148148152
CAPEX_DEMO = 1100000.0
VAN_DEMO = 179235.18843887906
TIR_DEMO = 0.07322327202038711
VITA_DEMO = 15
PAYBACK_DEMO = 9
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w662_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _helpers_src():
    return (_new_dir() / "w662_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w662_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh662_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh662_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh662_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh662_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh662_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh662_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh662_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh662_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh662_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh662_int_pos"](True, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh662_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh662_int_pos"](15.0, "x") == 15

    def test_frazione_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh662_frazione"](1.1, "x")

    def test_frazione_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh662_frazione"](-0.1, "x")

    def test_frazione_accetta_bordi(self):
        assert _F["mh662_frazione"](0.0, "x") == 0.0
        assert _F["mh662_frazione"](1.0, "x") == 1.0

    def test_eta_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh662_eta"](0.0, "x")

    def test_eta_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh662_eta"](1.01, "x")

    def test_eta_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh662_eta"](-0.5, "x")

    def test_eta_accetta_uno(self):
        assert _F["mh662_eta"](1.0, "x") == 1.0


class TestFisica:
    def test_calore_utile_demo(self):
        assert _F["mh662_calore_utile_mwh"](5000.0, 0.49, 1200.0) == \
            pytest.approx(Q_DEMO, rel=REL)

    def test_calore_utile_rifiuta_massa_zero(self):
        with pytest.raises(ValueError):
            _F["mh662_calore_utile_mwh"](0.0, 0.49, 1200.0)

    def test_calore_utile_rifiuta_cp_negativo(self):
        with pytest.raises(ValueError):
            _F["mh662_calore_utile_mwh"](5000.0, -0.1, 1200.0)

    def test_calore_utile_scala_lineare(self):
        q1 = _F["mh662_calore_utile_mwh"](5000.0, 0.49, 1200.0)
        q2 = _F["mh662_calore_utile_mwh"](10000.0, 0.49, 1200.0)
        assert q2 == pytest.approx(2.0 * q1, rel=REL)

    def test_gas_demo(self):
        assert _F["mh662_gas_mwh_pci"](Q_DEMO, 0.35) == \
            pytest.approx(F_GAS_DEMO, rel=REL)

    def test_gas_eta_uno_uguale_q(self):
        assert _F["mh662_gas_mwh_pci"](800.0, 1.0) == \
            pytest.approx(800.0, rel=REL)

    def test_gas_rifiuta_eta_zero(self):
        with pytest.raises(ValueError):
            _F["mh662_gas_mwh_pci"](800.0, 0.0)

    def test_gas_rifiuta_eta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh662_gas_mwh_pci"](800.0, 1.5)

    def test_elettricita_demo(self):
        assert _F["mh662_elettricita_mwh"](Q_DEMO, 0.90) == \
            pytest.approx(E_IND_DEMO, rel=REL)

    def test_elettricita_rifiuta_eta_zero(self):
        with pytest.raises(ValueError):
            _F["mh662_elettricita_mwh"](800.0, 0.0)

    def test_elettricita_piu_efficiente_meno_mwh(self):
        e1 = _F["mh662_elettricita_mwh"](800.0, 0.5)
        e2 = _F["mh662_elettricita_mwh"](800.0, 0.9)
        assert e2 == pytest.approx(0.5 / 0.9 * e1, rel=REL)

    def test_costo_gas_demo(self):
        assert _F["mh662_costo_gas_annuo"](F_GAS_DEMO, 75.0, 100.0,
                                            0.202, 30000.0) == \
            pytest.approx(COSTO_GAS_DEMO, rel=REL)

    def test_costo_gas_senza_ets(self):
        c = _F["mh662_costo_gas_annuo"](1000.0, 75.0, 0.0, 0.202, 0.0)
        assert c == pytest.approx(75000.0, rel=REL)

    def test_costo_gas_rifiuta_fattore_negativo(self):
        with pytest.raises(ValueError):
            _F["mh662_costo_gas_annuo"](1000.0, 75.0, 100.0,
                                        -0.1, 30000.0)

    def test_costo_induzione_demo(self):
        assert _F["mh662_costo_induzione_annuo"](E_IND_DEMO, 120.0,
                                                 20000.0) == \
            pytest.approx(COSTO_IND_DEMO, rel=REL)

    def test_costo_induzione_solo_manutenzione(self):
        c = _F["mh662_costo_induzione_annuo"](0.0, 120.0, 20000.0)
        assert c == pytest.approx(20000.0, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh662_risparmio_eur"](COSTO_GAS_DEMO,
                                         COSTO_IND_DEMO) == \
            pytest.approx(RISP_DEMO, rel=REL)

    def test_risparmio_zero_se_uguali(self):
        assert _F["mh662_risparmio_eur"](100.0, 100.0) == \
            pytest.approx(0.0)

    def test_risparmio_negativo_possibile(self):
        assert _F["mh662_risparmio_eur"](100.0, 200.0) == \
            pytest.approx(-100.0)

    def test_risparmio_rifiuta_costi_negativi(self):
        with pytest.raises(ValueError):
            _F["mh662_risparmio_eur"](-10.0, 100.0)

    def test_co2_demo(self):
        assert _F["mh662_co2_evitata_t"](F_GAS_DEMO, 0.202,
                                         E_IND_DEMO, 0.25) == \
            pytest.approx(CO2_DEMO, rel=REL)

    def test_co2_segno_negativo_possibile(self):
        # rete sporca: l'elettrificazione peggiora il bilancio CO2
        c = _F["mh662_co2_evitata_t"](1000.0, 0.202, 1000.0, 1.5)
        assert c == pytest.approx(-1298.0, rel=REL)

    def test_co2_zero_se_nulla(self):
        assert _F["mh662_co2_evitata_t"](0.0, 0.202, 0.0, 0.25) == \
            pytest.approx(0.0)

    def test_co2_rifiuta_fattore_el_negativo(self):
        with pytest.raises(ValueError):
            _F["mh662_co2_evitata_t"](1000.0, 0.202, 1000.0, -0.1)

    def test_capex_demo(self):
        assert _F["mh662_capex"](1100000.0) == \
            pytest.approx(CAPEX_DEMO, rel=REL)

    def test_capex_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh662_capex"](-1.0)

    def test_capex_zero_accettato(self):
        assert _F["mh662_capex"](0.0) == 0.0


class TestFinanza:
    def _flussi_demo(self):
        return _F["mh662_flussi"](CAPEX_DEMO, RISP_DEMO, VITA_DEMO)

    def test_flussi_struttura(self):
        fl = self._flussi_demo()
        assert fl[0] == -CAPEX_DEMO and len(fl) == 16
        assert all(f == RISP_DEMO for f in fl[1:])

    def test_flussi_rifiuta_vita_zero(self):
        with pytest.raises(ValueError):
            _F["mh662_flussi"](100.0, 10.0, 0)

    def test_van_demo(self):
        assert _F["mh662_van"](self._flussi_demo(), 5.0) == \
            pytest.approx(VAN_DEMO, rel=REL)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh662_van"](self._flussi_demo(), -1.0)

    def test_tir_demo(self):
        assert _F["mh662_tir"](self._flussi_demo()) == \
            pytest.approx(TIR_DEMO, rel=REL)

    def test_tir_none_senza_cambio_segno(self):
        assert _F["mh662_tir"]([-100.0, -10.0, -10.0]) is None

    def test_payback_demo(self):
        assert _F["mh662_payback"](self._flussi_demo()) == PAYBACK_DEMO

    def test_payback_none_mai(self):
        assert _F["mh662_payback"]([-100.0, 1.0, 1.0]) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh662_verdetto"](VAN_DEMO, CAPEX_DEMO, RISP_DEMO,
                                    0.10) == VERDETTO_DEMO

    def test_verdetto_marginale(self):
        assert _F["mh662_verdetto"](-110000.0, 1100000.0, 100.0,
                                    0.10) == "MARGINALE"

    def test_verdetto_non_conviente(self):
        assert _F["mh662_verdetto"](-500000.0, 1100000.0, 100.0,
                                    0.10) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risp_zero(self):
        assert _F["mh662_verdetto"](500.0, 1100000.0, 0.0,
                                    0.10) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_risp_none(self):
        assert _F["mh662_verdetto"](500.0, 1100000.0, None,
                                    0.10) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_van_none(self):
        assert _F["mh662_verdetto"](None, 1100000.0, 100.0,
                                    0.10) == "NON_CALCOLABILE"

    def test_verdetto_rifiuta_tolleranza_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh662_verdetto"](100.0, 1100000.0, 100.0, 1.5)


class TestDemo:
    def test_demo_calcoli_end_to_end(self):
        c = _F["mh662_demo_calcoli"]()
        assert c["calore_utile_mwh"] == pytest.approx(Q_DEMO,
                                                     rel=REL)
        assert c["f_gas_mwh_anno"] == pytest.approx(F_GAS_DEMO,
                                                   rel=REL)
        assert c["e_ind_mwh_anno"] == pytest.approx(E_IND_DEMO,
                                                   rel=REL)
        assert c["costo_gas_eur_anno"] == pytest.approx(
            COSTO_GAS_DEMO, rel=REL)
        assert c["costo_ind_eur_anno"] == pytest.approx(
            COSTO_IND_DEMO, rel=REL)
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
        assert _F["mh662_demo_calcoli"]() == _F["mh662_demo_calcoli"]()

    def test_demo_calcoli_contro_demo(self):
        # i default della UI riproducono la demo: mismatch < 1e-9 rel
        d = _F["mh662_demo"]()
        c = _F["mh662_demo_calcoli"]()
        q = _F["mh662_calore_utile_mwh"](d["massa_t_anno"],
                                         d["cp_kj_kgk"],
                                         d["delta_t_k"])
        assert q == pytest.approx(c["calore_utile_mwh"], rel=REL)

    def test_demo_defaults(self):
        d = _F["mh662_demo"]()
        assert d["massa_t_anno"] == 5000.0
        assert d["cp_kj_kgk"] == 0.49
        assert d["delta_t_k"] == 1200.0
        assert d["eta_gas"] == 0.35
        assert d["p_gas"] == 75.0
        assert d["p_ets"] == 100.0
        assert d["f_co2_gas"] == 0.202
        assert d["manut_gas"] == 30000.0
        assert d["eta_ind"] == 0.90
        assert d["p_el"] == 120.0
        assert d["f_co2_el"] == 0.25
        assert d["manut_ind"] == 20000.0
        assert d["capex"] == 1100000.0
        assert d["tasso_pct"] == 5.0
        assert d["vita_anni"] == 15
        assert d["tolleranza"] == 0.10


class TestUI:
    def test_header_helpers_presente(self):
        assert '# W662 (23/10/2026) - tab662' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh662_num", "mh662_nneg", "mh662_pos",
                     "mh662_int_pos", "mh662_frazione", "mh662_eta",
                     "mh662_calore_utile_mwh", "mh662_gas_mwh_pci",
                     "mh662_elettricita_mwh", "mh662_costo_gas_annuo",
                     "mh662_costo_induzione_annuo",
                     "mh662_risparmio_eur", "mh662_co2_evitata_t",
                     "mh662_capex", "mh662_flussi", "mh662_van",
                     "mh662_tir", "mh662_payback", "mh662_verdetto",
                     "mh662_demo", "mh662_demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE662) == 1

    def test_blocco_with_tab662(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab662:"

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st662_[a-z0-9_]+)"', _ui_src())
        assert len(keys) >= 15
        assert len(set(keys)) == len(keys)
        # nessuna collisione con le chiavi del ciclo precedente
        assert not any(k.startswith("st661_") for k in keys)

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg662" in src
        assert "(_rs662 <= 0.0)" in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg662") < src.index(".metric(")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Gas evitato (MWh/anno)" in src
        assert "Risparmio (€/anno)" in src
        assert "CO2 evitata (t/anno)" in src
        assert "Payback (anni)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd662" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_grafico_costi_presente(self):
        src = _ui_src()
        assert "plotly.graph_objects" in src
        assert "barmode" in src
        assert "Forno a gas" in src
        assert "Forno a induzione" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert 'sep=";"' in src
        assert "forno_induzione.csv" in _ui_src()

    def test_differenziazione_da_tab659(self):
        src = _ui_src()
        assert "tab659" in src
        assert "Economizzatore fumi" in src

    def test_nessun_segreto_nella_sezione(self):
        assert not re.search(r'(?i)(api_key|secret|password)\s*=\s*["\']',
                             _ui_src())
