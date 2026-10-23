"""Test tab664 "🔌🏝️ Microrete industriale: quanto costa staccarsi dalla rete?"

Demo calcolata eseguendo mh664_demo_calcoli() (non a mano):
carico 20.000 MWh/anno, picco 5 MW (energia 150 EUR/MWh, potenza
40.000 EUR/MW/anno); FV 8 MWp x 1.150 MWh/MWp, autoconsumo 70 %;
accumulo 4 MWh x 250 cicli/anno, eta round-trip 90 %; generatore di
backup (fuel 80 EUR/MWh, eta 40 %); CAPEX 900.000 EUR/MWp FV,
350.000 EUR/MWh accumulo, 1.000.000 EUR generatore,
300.000 EUR EMS; OPEX 150.000 EUR/anno; fattori CO2 rete 250 /
fuel 202 kg/MWh; 8 h/anno di interruzione x 3 MW critici, VoLL
5 EUR/kWh; 6 %, 20 anni, tolleranza 10 %.

- E_pv = 8 x 1.150 = 9.200 MWh/anno
- E_pv_auto = 9.200 x 70 % = 6.440 MWh/anno
- E_bess = 4 x 250 x 90 % = 900 MWh/anno
- E_backup = 20.000 - 6.440 - 900 = 12.660 MWh/anno
- autosufficienza = 100 x (6.440 + 900) / 20.000 = 36,7 %
- bolletta base = 20.000 x 150 + 5 x 40.000 = 3.200.000 EUR/anno
- costo fuel = 12.660 x 80 / 0,40 = 2.532.000 EUR/anno
- E_protetta = 8 x 3 = 24 MWh/anno
- valore affidabilita' = 24 x 5 x 1000 = 120.000 EUR/anno
- CAPEX = 8 x 900.000 + 4 x 350.000 + 1.000.000 + 300.000
        = 9.900.000 EUR
- margine = 3.200.000 + 120.000 - 150.000 - 2.532.000
         = 638.000 EUR/anno
- CO2 = (6.440 + 900) x 250 / 1000 - 12.660 x 202 / 1000
     = 1.835 - 2.557,32 = -722,32 t/anno (segno libero: il fuel
     di backup sporca piu' della rete risparmiata)
- flussi [-9.900.000, 638.000 x 20]; VAN(6 %) = -2.582.190,26 EUR
  (|VAN| = 2,58 M > tolleranza 0,10 x 9,9 M = 990.000) ->
  NON_CONVIENTE
- TIR = 0,025490046828405537 (2,5490 %); payback anno 16
  (cum 15 = 15 x 638.000 - 9.900.000 = -330.000 < 0;
   cum 16 = +308.000 >= 0)
"""

import ast
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w664_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w664_helpers.py via AST
    (stesso pattern di tests/appfuncs.py: niente Streamlit)."""
    src = (_new_dir() / "w664_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w664_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w664_helpers.py: {missing}")
    return out


_F = _load("mh664_num", "mh664_nneg", "mh664_pos", "mh664_int_pos",
           "mh664_pct100",
           "mh664_e_pv", "mh664_e_pv_auto", "mh664_e_bess",
           "mh664_e_backup", "mh664_autosufficienza_pct",
           "mh664_bolletta_base", "mh664_costo_fuel",
           "mh664_e_protetta", "mh664_valore_affidabilita",
           "mh664_capex", "mh664_margine_annuo", "mh664_co2_t_anno",
           "mh664_flussi", "mh664_van", "mh664_tir",
           "mh664_payback", "mh664_verdetto",
           "mh664_demo", "mh664_demo_calcoli")

TITLE664 = "🔌🏝️ Microrete industriale: quanto costa staccarsi dalla rete?"

E_PV_DEMO = 9200.0
E_PV_AUTO_DEMO = 6440.0
E_BESS_DEMO = 900.0
E_BACKUP_DEMO = 12660.0
AUTOSUFF_DEMO = 36.7
BOLLETTA_DEMO = 3200000.0
COSTO_FUEL_DEMO = 2532000.0
E_PROTETTA_DEMO = 24.0
VAFF_DEMO = 120000.0
CAPEX_DEMO = 9900000.0
MARGINE_DEMO = 638000.0
CO2_DEMO = -722.3200000000002
VAN_DEMO = -2582190.262555369
TIR_DEMO = 0.025490046828405537
VITA_DEMO = 20
PAYBACK_DEMO = 16
VERDETTO_DEMO = "NON_CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w664_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w664_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh664_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh664_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh664_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh664_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh664_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh664_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh664_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh664_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh664_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh664_int_pos"](True, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh664_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh664_int_pos"](20.0, "x") == 20

    def test_pct100_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh664_pct100"](-0.1, "x")

    def test_pct100_rifiuta_sopra_100(self):
        with pytest.raises(ValueError):
            _F["mh664_pct100"](100.1, "x")

    def test_pct100_accetta_bordi(self):
        assert _F["mh664_pct100"](0.0, "x") == 0.0
        assert _F["mh664_pct100"](100.0, "x") == 100.0


class TestFisica:
    def test_e_pv_demo(self):
        assert _F["mh664_e_pv"](8.0, 1150.0) == pytest.approx(
            E_PV_DEMO, rel=REL)

    def test_e_pv_zero_se_no_pv(self):
        assert _F["mh664_e_pv"](0.0, 1150.0) == pytest.approx(0.0)

    def test_e_pv_rifiuta_potenza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh664_e_pv"](-1.0, 1150.0)

    def test_e_pv_auto_demo(self):
        assert _F["mh664_e_pv_auto"](E_PV_DEMO, 70.0) == \
            pytest.approx(E_PV_AUTO_DEMO, rel=REL)

    def test_e_pv_auto_zero_a_quota_zero(self):
        assert _F["mh664_e_pv_auto"](9200.0, 0.0) == \
            pytest.approx(0.0)

    def test_e_pv_auto_rifiuta_quota_sopra_100(self):
        with pytest.raises(ValueError):
            _F["mh664_e_pv_auto"](9200.0, 101.0)

    def test_e_bess_demo(self):
        assert _F["mh664_e_bess"](4.0, 250.0, 90.0) == pytest.approx(
            E_BESS_DEMO, rel=REL)

    def test_e_bess_scala_lineare(self):
        b1 = _F["mh664_e_bess"](2.0, 250.0, 90.0)
        b2 = _F["mh664_e_bess"](4.0, 250.0, 90.0)
        assert b2 == pytest.approx(2.0 * b1, rel=REL)

    def test_e_backup_demo(self):
        assert _F["mh664_e_backup"](20000.0, E_PV_AUTO_DEMO,
                                    E_BESS_DEMO) == pytest.approx(
            E_BACKUP_DEMO, rel=REL)

    def test_e_backup_clamp_a_zero(self):
        # rinnovabili che coprono tutto il carico: niente backup
        assert _F["mh664_e_backup"](5000.0, 4000.0,
                                    2000.0) == pytest.approx(0.0)

    def test_e_backup_rifiuta_carico_zero(self):
        with pytest.raises(ValueError):
            _F["mh664_e_backup"](0.0, 100.0, 100.0)

    def test_autosufficienza_demo(self):
        assert _F["mh664_autosufficienza_pct"](
            E_PV_AUTO_DEMO, E_BESS_DEMO, 20000.0) == pytest.approx(
            AUTOSUFF_DEMO, rel=REL)

    def test_autosufficienza_100_pct(self):
        assert _F["mh664_autosufficienza_pct"](7000.0, 3000.0,
                                               10000.0) == \
            pytest.approx(100.0, rel=REL)

    def test_bolletta_demo(self):
        assert _F["mh664_bolletta_base"](20000.0, 150.0, 5.0,
                                         40000.0) == pytest.approx(
            BOLLETTA_DEMO, rel=REL)

    def test_bolletta_solo_potenza(self):
        b = _F["mh664_bolletta_base"](20000.0, 0.0, 5.0, 40000.0)
        assert b == pytest.approx(200000.0, rel=REL)

    def test_costo_fuel_demo(self):
        assert _F["mh664_costo_fuel"](E_BACKUP_DEMO, 80.0,
                                      40.0) == pytest.approx(
            COSTO_FUEL_DEMO, rel=REL)

    def test_costo_fuel_zero_a_backup_zero(self):
        assert _F["mh664_costo_fuel"](0.0, 80.0,
                                      40.0) == pytest.approx(0.0)

    def test_costo_fuel_rifiuta_eta_zero(self):
        with pytest.raises(ValueError):
            _F["mh664_costo_fuel"](1000.0, 80.0, 0.0)

    def test_e_protetta_demo(self):
        assert _F["mh664_e_protetta"](8.0, 3.0) == pytest.approx(
            E_PROTETTA_DEMO, rel=REL)

    def test_valore_affidabilita_demo(self):
        assert _F["mh664_valore_affidabilita"](
            E_PROTETTA_DEMO, 5.0) == pytest.approx(VAFF_DEMO,
                                                   rel=REL)

    def test_capex_demo(self):
        assert _F["mh664_capex"](8.0, 900000.0, 4.0, 350000.0,
                                 1000000.0, 300000.0) == \
            pytest.approx(CAPEX_DEMO, rel=REL)

    def test_capex_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh664_capex"](8.0, -1.0, 4.0, 350000.0, 1000000.0,
                              300000.0)

    def test_margine_demo(self):
        assert _F["mh664_margine_annuo"](BOLLETTA_DEMO, VAFF_DEMO,
                                         150000.0,
                                         COSTO_FUEL_DEMO) == \
            pytest.approx(MARGINE_DEMO, rel=REL)

    def test_margine_negativo_possibile(self):
        assert _F["mh664_margine_annuo"](100.0, 0.0, 500.0,
                                         200.0) == pytest.approx(
            -600.0)

    def test_co2_demo(self):
        assert _F["mh664_co2_t_anno"](E_PV_AUTO_DEMO, E_BESS_DEMO,
                                      250.0, E_BACKUP_DEMO,
                                      202.0) == pytest.approx(
            CO2_DEMO, rel=REL)

    def test_co2_segno_negativo_possibile(self):
        # backup a fuel piu' sporco della rete risparmiata
        c = _F["mh664_co2_t_anno"](6440.0, 900.0, 50.0, 12660.0,
                                   202.0)
        assert c < 0.0

    def test_co2_zero_se_nulla(self):
        assert _F["mh664_co2_t_anno"](0.0, 0.0, 250.0, 0.0,
                                      202.0) == pytest.approx(0.0)


class TestFinanza:
    def _flussi_demo(self):
        return _F["mh664_flussi"](CAPEX_DEMO, MARGINE_DEMO,
                                  VITA_DEMO)

    def test_flussi_struttura(self):
        fl = self._flussi_demo()
        assert fl[0] == -CAPEX_DEMO and len(fl) == 21
        assert all(f == MARGINE_DEMO for f in fl[1:])

    def test_flussi_rifiuta_vita_zero(self):
        with pytest.raises(ValueError):
            _F["mh664_flussi"](100.0, 10.0, 0)

    def test_van_demo(self):
        assert _F["mh664_van"](self._flussi_demo(),
                               0.06) == pytest.approx(VAN_DEMO,
                                                      rel=REL)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh664_van"](self._flussi_demo(), -0.01)

    def test_van_tasso_zero(self):
        fl = [-100.0, 30.0, 30.0]
        assert _F["mh664_van"](fl, 0.0) == pytest.approx(-40.0)

    def test_tir_demo(self):
        assert _F["mh664_tir"](self._flussi_demo()) == pytest.approx(
            TIR_DEMO, rel=REL)

    def test_tir_none_senza_cambio_segno(self):
        assert _F["mh664_tir"]([-100.0, -10.0, -10.0]) is None

    def test_payback_demo(self):
        assert _F["mh664_payback"](self._flussi_demo()) == \
            PAYBACK_DEMO

    def test_payback_none_mai(self):
        assert _F["mh664_payback"]([-100.0, 1.0, 1.0]) is None

    def test_verdetto_conviente_p_el_alto(self):
        # prezzo energia raddoppiato -> bolletta e margine salgono,
        # VAN diventa positivo
        bol = _F["mh664_bolletta_base"](20000.0, 300.0, 5.0,
                                        40000.0)
        m = _F["mh664_margine_annuo"](bol, VAFF_DEMO, 150000.0,
                                       COSTO_FUEL_DEMO)
        fl = _F["mh664_flussi"](CAPEX_DEMO, m, VITA_DEMO)
        v = _F["mh664_van"](fl, 0.06)
        assert v > 0.0
        assert _F["mh664_verdetto"](v, CAPEX_DEMO, m, 0.10) == \
            "CONVIENTE"

    def test_verdetto_marginale_tolleranza_ampia(self):
        assert _F["mh664_verdetto"](VAN_DEMO, CAPEX_DEMO,
                                    MARGINE_DEMO, 0.50) == \
            "MARGINALE"

    def test_verdetto_non_conviente_demo(self):
        assert _F["mh664_verdetto"](VAN_DEMO, CAPEX_DEMO,
                                    MARGINE_DEMO, 0.10) == \
            VERDETTO_DEMO

    def test_verdetto_non_calcolabile_margine_zero(self):
        assert _F["mh664_verdetto"](500.0, CAPEX_DEMO, 0.0,
                                    0.10) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_margine_negativo(self):
        assert _F["mh664_verdetto"](500.0, CAPEX_DEMO, -100.0,
                                    0.10) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_van_none(self):
        assert _F["mh664_verdetto"](None, CAPEX_DEMO, 100.0,
                                    0.10) == "NON_CALCOLABILE"

    def test_verdetto_rifiuta_tolleranza_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh664_verdetto"](100.0, CAPEX_DEMO, 100.0, 1.5)


class TestDemo:
    def test_demo_calcoli_end_to_end(self):
        c = _F["mh664_demo_calcoli"]()
        assert c["e_pv_mwh_anno"] == pytest.approx(E_PV_DEMO,
                                                   rel=REL)
        assert c["e_pv_auto_mwh_anno"] == pytest.approx(
            E_PV_AUTO_DEMO, rel=REL)
        assert c["e_bess_mwh_anno"] == pytest.approx(
            E_BESS_DEMO, rel=REL)
        assert c["e_backup_mwh_anno"] == pytest.approx(
            E_BACKUP_DEMO, rel=REL)
        assert c["autosufficienza_pct"] == pytest.approx(
            AUTOSUFF_DEMO, rel=REL)
        assert c["bolletta_base_eur_anno"] == pytest.approx(
            BOLLETTA_DEMO, rel=REL)
        assert c["costo_fuel_eur_anno"] == pytest.approx(
            COSTO_FUEL_DEMO, rel=REL)
        assert c["e_protetta_mwh_anno"] == pytest.approx(
            E_PROTETTA_DEMO, rel=REL)
        assert c["valore_affidabilita_eur_anno"] == pytest.approx(
            VAFF_DEMO, rel=REL)
        assert c["capex_eur"] == pytest.approx(CAPEX_DEMO, rel=REL)
        assert c["margine_annuo_eur"] == pytest.approx(
            MARGINE_DEMO, rel=REL)
        assert c["co2_t_anno"] == pytest.approx(CO2_DEMO, rel=REL)
        assert c["van_eur"] == pytest.approx(VAN_DEMO, rel=REL)
        assert c["tir"] == pytest.approx(TIR_DEMO, rel=REL)
        assert c["payback_anni"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO

    def test_demo_calcoli_deterministico(self):
        assert _F["mh664_demo_calcoli"]() == _F["mh664_demo_calcoli"]()

    def test_demo_calcoli_contro_demo(self):
        # i default della UI riproducono la demo: mismatch < 1e-9 rel
        d = _F["mh664_demo"]()
        c = _F["mh664_demo_calcoli"]()
        e_pv = _F["mh664_e_pv"](d["potenza_mwp"],
                                d["producibilita_mwh_mwp"])
        assert e_pv == pytest.approx(c["e_pv_mwh_anno"], rel=REL)

    def test_demo_defaults(self):
        d = _F["mh664_demo"]()
        assert d["e_carico_mwh_anno"] == 20000.0
        assert d["p_picco_mw"] == 5.0
        assert d["p_el_eur_mwh"] == 150.0
        assert d["p_potenza_eur_mw_anno"] == 40000.0
        assert d["potenza_mwp"] == 8.0
        assert d["producibilita_mwh_mwp"] == 1150.0
        assert d["quota_autoconsumo_pct"] == 70.0
        assert d["capacita_mwh"] == 4.0
        assert d["cicli_eq_anno"] == 250.0
        assert d["eta_rt_pct"] == 90.0
        assert d["p_fuel_eur_mwh"] == 80.0
        assert d["eta_gen_pct"] == 40.0
        assert d["capex_pv_eur_mwp"] == 900000.0
        assert d["capex_bess_eur_mwh"] == 350000.0
        assert d["capex_gen_fisso_eur"] == 1000000.0
        assert d["capex_ems_fisso_eur"] == 300000.0
        assert d["opex_annuo_eur"] == 150000.0
        assert d["f_grid_kg_mwh"] == 250.0
        assert d["f_fuel_kg_mwh"] == 202.0
        assert d["ore_interruzione_anno"] == 8.0
        assert d["potenza_critica_mw"] == 3.0
        assert d["voll_eur_kwh"] == 5.0
        assert d["tasso_pct"] == 6.0
        assert d["vita_anni"] == 20
        assert d["tolleranza_pct"] == 10.0


class TestUI:
    def test_header_helpers_presente(self):
        assert '# W664 (23/10/2026) - tab664' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh664_num", "mh664_nneg", "mh664_pos",
                     "mh664_int_pos", "mh664_pct100",
                     "mh664_e_pv", "mh664_e_pv_auto",
                     "mh664_e_bess", "mh664_e_backup",
                     "mh664_autosufficienza_pct",
                     "mh664_bolletta_base", "mh664_costo_fuel",
                     "mh664_e_protetta",
                     "mh664_valore_affidabilita", "mh664_capex",
                     "mh664_margine_annuo", "mh664_co2_t_anno",
                     "mh664_flussi", "mh664_van", "mh664_tir",
                     "mh664_payback", "mh664_verdetto",
                     "mh664_demo", "mh664_demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE664) == 1

    def test_blocco_with_tab664(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab664:"

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st664_[a-z0-9_]+)"', _ui_src())
        assert len(keys) >= 20
        assert len(set(keys)) == len(keys)
        # nessuna collisione con le chiavi del ciclo precedente
        assert not any(k.startswith("st663_") for k in keys)

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_mar664 <= 0.0" in src
        assert "NON_CALCOLABILE" in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_mar664 <= 0.0") < src.index(".metric(")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Autosufficienza (%)" in src
        assert "Margine (€/anno)" in src
        assert "CO2 netta (t/anno)" in src
        assert "Payback (anni)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd664" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_grafico_costi_presente(self):
        src = _ui_src()
        assert "plotly.graph_objects" in src
        assert "Bolletta evitata" in src
        assert "Fuel backup" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert 'sep=";"' in src
        assert "microrete_industriale.csv" in src

    def test_differenziazione_da_feature_esistenti(self):
        src = _ui_src()
        assert "VoLL" in src
        assert "autoconsumo FV" in src.lower() or \
            "Autoconsumo FV" in src

    def test_nessun_segreto_nella_sezione(self):
        assert not re.search(r'(?i)(api_key|secret|password)\s*=\s*["\']',
                             _ui_src())
