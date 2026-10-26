"""Test tab668 "❄️🏭 Refrigerazione industriale: quanto costa il freddo?"

Demo calcolata eseguendo mh668_demo_calcoli() (non a mano):
celle frigorifere di logistica alimentare — P = 500 kW_f,
h_eq = 6000 h/anno, EER baseline 2,5 -> nuovo 4,0; prezzo
elettricita' 0,22 EUR/kWh; recupero calore 40 %; gas
0,09 EUR/kWh, rendimento caldaia 0,9; CAPEX 180.000 EUR;
fattori CO2 0,35 kg/kWh (el) e 0,20 kg/kWh (gas); tasso 6 %,
vita 15 anni, tolleranza 10 % del CAPEX.

- Q_freddo = 500,0 x 6000,0 = 3000000.0 kWh_f/anno
- E_base = 3000000.0 / 2,5 = 1200000.0 kWh_el/anno
- E_new = 3000000.0 / 4,0 = 750000.0 kWh_el/anno
- dE = 1200000.0 - 750000.0 = 450000.0 kWh/anno
- C_el = 450000.0 x 0,22 = 99000.0 EUR/anno
- Q_cond = 3000000.0 x (1 + 1/4,0) = 3750000.0 kWh/anno
- Q_rec = 3750000.0 x 40,0/100 = 1500000.0 kWh/anno
- C_gas = 1500000.0 / 0,9 x 0,09 = 149999.99999999997 EUR/anno
- R = 99000.0 + 149999.99999999997 = 248999.99999999997 EUR/anno
- CO2 = (450000.0 x 0,35 + 1500000.0 / 0,9 x 0,20) / 1000
      = 490.8333333333333 t/anno
- flussi [-180000.0, 248999.99999999997 x 15];
  VAN(6 %) = 2238349.9979475066 EUR -> CONVIENTE (VAN > 0)
- TIR = 138.3330291304246 % (bisezione su [-0.99, 10])
- payback_anni = 1 (primo anno con cumulato >= 0)
- verdetto = 'CONVIENTE'
"""

import ast
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w668_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w668_helpers.py via AST
    (stesso pattern di tests/appfuncs.py: niente Streamlit)."""
    src = (_new_dir() / "w668_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w668_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w668_helpers.py: {missing}")
    return out


_F = _load("mh668_num", "mh668_nneg", "mh668_pos", "mh668_int_pos",
           "mh668_q_freddo_kwh", "mh668_e_base_kwh",
           "mh668_e_new_kwh", "mh668_risparmio",
           "mh668_recupero_calore", "mh668_co2",
           "mh668_van", "mh668_tir", "mh668_payback",
           "mh668_verdetto", "_mh668_neutro",
           "mh668_business_case", "mh668_demo",
           "mh668_demo_calcoli")

TITLE668 = "❄️🏭 Refrigerazione industriale: quanto costa il freddo?"

Q_DEMO = 3000000.0
E_BASE_DEMO = 1200000.0
E_NEW_DEMO = 750000.0
DE_DEMO = 450000.0
C_EL_DEMO = 99000.0
Q_COND_DEMO = 3750000.0
Q_REC_DEMO = 1500000.0
C_GAS_DEMO = 149999.99999999997
R_DEMO = 248999.99999999997
CO2_DEMO = 490.8333333333333
VAN_DEMO = 2238349.9979475066
TIR_PCT_DEMO = 138.3330291304246
PAYBACK_DEMO = 1
VITA_DEMO = 15
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w668_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w668_ui.py").read_text(encoding="utf-8")


def _app_src():
    return (Path.home() / "workspace/repo-dashboard/"
            "Dashboard-data-analist/app.py").read_text(
                encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh668_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh668_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh668_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh668_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh668_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh668_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh668_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh668_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh668_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh668_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh668_int_pos"](15.0, "x") == 15


class TestFisica:
    def test_q_freddo_demo(self):
        assert _F["mh668_q_freddo_kwh"](
            500.0, 6000.0) == pytest.approx(Q_DEMO, rel=REL)

    def test_q_freddo_rifiuta_potenza_zero(self):
        with pytest.raises(ValueError):
            _F["mh668_q_freddo_kwh"](0.0, 6000.0)

    def test_q_freddo_rifiuta_ore_negative(self):
        with pytest.raises(ValueError):
            _F["mh668_q_freddo_kwh"](500.0, -10.0)

    def test_e_base_demo(self):
        assert _F["mh668_e_base_kwh"](
            Q_DEMO, 2.5) == pytest.approx(E_BASE_DEMO, rel=REL)

    def test_e_new_demo(self):
        assert _F["mh668_e_new_kwh"](
            Q_DEMO, 4.0) == pytest.approx(E_NEW_DEMO, rel=REL)

    def test_e_base_rifiuta_eer_zero(self):
        with pytest.raises(ValueError):
            _F["mh668_e_base_kwh"](Q_DEMO, 0.0)

    def test_e_new_rifiuta_eer_negativo(self):
        with pytest.raises(ValueError):
            _F["mh668_e_new_kwh"](Q_DEMO, -1.0)

    def test_risparmio_dict_demo(self):
        r = _F["mh668_risparmio"](500.0, 6000.0, 2.5, 4.0,
                                  0.22)
        assert r["q_freddo_kwh"] == pytest.approx(Q_DEMO,
                                                  rel=REL)
        assert r["e_base_kwh"] == pytest.approx(E_BASE_DEMO,
                                                rel=REL)
        assert r["e_new_kwh"] == pytest.approx(E_NEW_DEMO,
                                               rel=REL)
        assert r["risparmio_kwh_el"] == pytest.approx(DE_DEMO,
                                                     rel=REL)
        assert r["risparmio_el_eur"] == pytest.approx(C_EL_DEMO,
                                                     rel=REL)

    def test_risparmio_negativo_se_eer_new_peggiore(self):
        # nuovo impianto peggiore del baseline -> dE negativo
        r = _F["mh668_risparmio"](500.0, 6000.0, 2.5, 1.0,
                                  0.22)
        assert r["risparmio_kwh_el"] == pytest.approx(
            E_BASE_DEMO - Q_DEMO / 1.0, rel=REL)
        assert r["risparmio_kwh_el"] < 0.0

    def test_recupero_calore_demo(self):
        r = _F["mh668_recupero_calore"](Q_DEMO, 4.0, 40.0,
                                        0.09, 0.9)
        assert r["q_cond_kwh"] == pytest.approx(Q_COND_DEMO,
                                                rel=REL)
        assert r["q_rec_kwh"] == pytest.approx(Q_REC_DEMO,
                                               rel=REL)
        assert r["risparmio_gas_eur"] == pytest.approx(
            C_GAS_DEMO, rel=REL)

    def test_recupero_calore_eta_zero_azzera_gas(self):
        r = _F["mh668_recupero_calore"](Q_DEMO, 4.0, 40.0,
                                        0.09, 0.0)
        assert r["risparmio_gas_eur"] == 0.0
        assert r["q_rec_kwh"] == pytest.approx(Q_REC_DEMO,
                                               rel=REL)

    def test_recupero_calore_rifiuta_quota_sopra_100(self):
        with pytest.raises(ValueError):
            _F["mh668_recupero_calore"](Q_DEMO, 4.0, 101.0,
                                        0.09, 0.9)

    def test_recupero_calore_rifiuta_quota_negativa(self):
        with pytest.raises(ValueError):
            _F["mh668_recupero_calore"](Q_DEMO, 4.0, -1.0,
                                        0.09, 0.9)

    def test_co2_demo(self):
        assert _F["mh668_co2"](
            DE_DEMO, 0.35, Q_REC_DEMO, 0.9,
            0.20) == pytest.approx(CO2_DEMO, rel=REL)

    def test_co2_eta_zero_solo_elettrico(self):
        # termine gas azzerato: solo dE x f_el / 1000
        assert _F["mh668_co2"](
            DE_DEMO, 0.35, Q_REC_DEMO, 0.0,
            0.20) == pytest.approx(DE_DEMO * 0.35 / 1000.0,
                                   rel=REL)

    def test_co2_rifiuta_fattore_negativo(self):
        with pytest.raises(ValueError):
            _F["mh668_co2"](DE_DEMO, -0.1, Q_REC_DEMO, 0.9,
                            0.20)


class TestFinanza:
    def test_van_demo(self):
        assert _F["mh668_van"](
            180000.0, R_DEMO, 0.06,
            VITA_DEMO) == pytest.approx(VAN_DEMO, rel=REL)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh668_van"](180000.0, R_DEMO, -0.01, 15)

    def test_van_tasso_zero(self):
        assert _F["mh668_van"](
            180000.0, 249000.0, 0.0, 15) == pytest.approx(
            -180000.0 + 249000.0 * 15, rel=1e-12)

    def test_tir_none_se_r_non_positivo(self):
        assert _F["mh668_tir"](180000.0, 0.0, 15) is None
        assert _F["mh668_tir"](180000.0, -100.0, 15) is None

    def test_tir_demo(self):
        assert _F["mh668_tir"](
            180000.0, R_DEMO, VITA_DEMO) * 100.0 == \
            pytest.approx(TIR_PCT_DEMO, rel=REL)

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh668_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo(self):
        assert _F["mh668_payback"](
            180000.0, R_DEMO, VITA_DEMO) == PAYBACK_DEMO

    def test_payback_none_mai(self):
        assert _F["mh668_payback"](100000.0, 1.0, 15) is None

    def test_payback_none_se_r_non_positivo(self):
        assert _F["mh668_payback"](180000.0, 0.0, 15) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh668_verdetto"](
            R_DEMO, VAN_DEMO, 180000.0,
            10.0) == VERDETTO_DEMO

    def test_verdetto_marginale_ad_hoc(self):
        # VAN negativo entro il 10 % del CAPEX
        assert _F["mh668_verdetto"](
            1000.0, -0.05 * 180000.0, 180000.0,
            10.0) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh668_verdetto"](
            1000.0, -180000.0, 180000.0,
            10.0) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_r_non_positivo(self):
        assert _F["mh668_verdetto"](
            0.0, 1000.0, 180000.0,
            10.0) == "NON_CALCOLABILE"
        assert _F["mh668_verdetto"](
            -50.0, 1000.0, 180000.0,
            10.0) == "NON_CALCOLABILE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh668_verdetto"](1000.0, 100.0, 180000.0,
                                 -1.0)


class TestGuard:
    def _bc(self, **kw):
        d = _F["mh668_demo"]()
        d.update(kw)
        return _F["mh668_business_case"](**d)

    def test_eer_base_zero_neutro(self):
        n = self._bc(eer_base=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["q_freddo_kwh"] == 0.0
        assert n["risparmio_tot_eur"] == 0.0
        assert n["tir_pct"] is None
        assert n["payback_anni"] is None

    def test_eer_new_negativo_neutro(self):
        n = self._bc(eer_new=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["van_eur"] == 0.0

    def test_potenza_zero_neutra(self):
        n = self._bc(p_kw=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_ore_zero_neutre(self):
        n = self._bc(h_eq=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(p_el=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["co2_t"] == 0.0

    def test_r_non_positivo_neutro(self):
        # nuovo impianto peggiore + nessun recupero calore
        n = self._bc(eer_new=1.0, rec_pct=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["tir_pct"] is None
        assert n["payback_anni"] is None

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh668_neutro"]()
        assert list(n["df_anno"].columns) == ["Anno", "Flusso",
                                             "Cumulato"]
        assert len(n["df_anno"]) == 0
        assert list(n["df_voci"].columns) == ["Voce",
                                             "Valore (EUR/anno)"]
        assert len(n["df_voci"]) == 0

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh668_neutro"]()
        for chiave in ("q_freddo_kwh", "e_base_kwh",
                       "e_new_kwh", "risparmio_kwh_el",
                       "risparmio_el_eur", "q_rec_kwh",
                       "risparmio_gas_eur", "risparmio_tot_eur",
                       "co2_t", "van_eur", "tir_pct",
                       "payback_anni", "verdetto", "df_anno",
                       "df_voci"):
            assert chiave in n, chiave

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert list(b["df_anno"].columns) == ["Anno", "Flusso",
                                             "Cumulato"]
        assert len(b["df_anno"]) == VITA_DEMO + 1
        assert b["df_anno"]["Anno"].tolist() == list(
            range(VITA_DEMO + 1))
        assert list(b["df_voci"].columns) == ["Voce",
                                             "Valore (EUR/anno)"]
        assert len(b["df_voci"]) == 3


class TestDemo:
    def test_demo_calcoli_end_to_end(self):
        c = _F["mh668_demo_calcoli"]()
        assert c["q_freddo_kwh"] == pytest.approx(Q_DEMO,
                                                  rel=REL)
        assert c["e_base_kwh"] == pytest.approx(E_BASE_DEMO,
                                                rel=REL)
        assert c["e_new_kwh"] == pytest.approx(E_NEW_DEMO,
                                               rel=REL)
        assert c["risparmio_kwh_el"] == pytest.approx(DE_DEMO,
                                                     rel=REL)
        assert c["risparmio_el_eur"] == pytest.approx(
            C_EL_DEMO, rel=REL)
        assert c["q_rec_kwh"] == pytest.approx(Q_REC_DEMO,
                                               rel=REL)
        assert c["risparmio_gas_eur"] == pytest.approx(
            C_GAS_DEMO, rel=REL)
        assert c["risparmio_tot_eur"] == pytest.approx(
            R_DEMO, rel=REL)
        assert c["co2_t"] == pytest.approx(CO2_DEMO, rel=REL)
        assert c["van_eur"] == pytest.approx(VAN_DEMO, rel=REL)
        assert c["tir_pct"] == pytest.approx(TIR_PCT_DEMO,
                                             rel=REL)
        assert c["payback_anni"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO

    def test_demo_calcoli_deterministico(self):
        assert _F["mh668_demo_calcoli"]()[
            "van_eur"] == _F["mh668_demo_calcoli"]()["van_eur"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        """business_case(**demo()) deve matchare le costanti
        _DEMO entro 1e-9 relativo (mismatch vietato)."""
        d = _F["mh668_demo"]()
        b = _F["mh668_business_case"](**d)
        coppie = [("q_freddo_kwh", Q_DEMO),
                  ("e_base_kwh", E_BASE_DEMO),
                  ("e_new_kwh", E_NEW_DEMO),
                  ("risparmio_kwh_el", DE_DEMO),
                  ("risparmio_el_eur", C_EL_DEMO),
                  ("q_rec_kwh", Q_REC_DEMO),
                  ("risparmio_gas_eur", C_GAS_DEMO),
                  ("risparmio_tot_eur", R_DEMO),
                  ("co2_t", CO2_DEMO),
                  ("van_eur", VAN_DEMO),
                  ("tir_pct", TIR_PCT_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert b["payback_anni"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh668_demo"]()
        assert d["p_kw"] == 500.0
        assert d["h_eq"] == 6000.0
        assert d["eer_base"] == 2.5
        assert d["eer_new"] == 4.0
        assert d["p_el"] == 0.22
        assert d["rec_pct"] == 40.0
        assert d["p_gas"] == 0.09
        assert d["eta_caldaia"] == 0.9
        assert d["capex"] == 180000.0
        assert d["f_el"] == 0.35
        assert d["f_gas"] == 0.20
        assert d["r_pct"] == 6.0
        assert d["n"] == 15
        assert d["tol_pct"] == 10.0

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        mh668_demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["mh668_demo_calcoli"]()
        doc = __doc__
        for chiave in ("q_freddo_kwh", "e_base_kwh",
                       "e_new_kwh", "risparmio_kwh_el",
                       "risparmio_el_eur", "q_rec_kwh",
                       "risparmio_gas_eur", "risparmio_tot_eur",
                       "co2_t", "van_eur", "tir_pct"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback_anni = 1" in doc
        assert "verdetto = 'CONVIENTE'" in doc


class TestUI:
    def test_header_helpers_presente(self):
        assert '# W668 (23/10/2026) - tab668' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh668_num", "mh668_nneg", "mh668_pos",
                     "mh668_int_pos",
                     "mh668_q_freddo_kwh", "mh668_e_base_kwh",
                     "mh668_e_new_kwh", "mh668_risparmio",
                     "mh668_recupero_calore", "mh668_co2",
                     "mh668_van", "mh668_tir", "mh668_payback",
                     "mh668_verdetto", "_mh668_neutro",
                     "mh668_business_case", "mh668_demo",
                     "mh668_demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE668) == 1

    def test_blocco_with_tab668(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab668:"

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st668_[a-z0-9_]+)"', _ui_src())
        assert len(keys) >= 16
        assert len(set(keys)) == len(keys)
        # nessuna collisione con le chiavi dei cicli precedenti
        assert not any(k.startswith("st667_") for k in keys)

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index('"NON_CALCOLABILE"') < src.index(
            ".metric(")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Risparmio annuo (€/anno)" in src
        assert "Energia el. risparmiata (kWh/anno)" in src
        assert "CO2 evitata (t/anno)" in src
        assert "VAN (€)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd668" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_grafico_voci_presente(self):
        src = _ui_src()
        assert "plotly.graph_objects" in src
        assert "Risparmio elettrico" in src
        assert "Risparmio gas (recupero calore)" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert 'sep=";"' in src
        assert "refrigerazione_industriale.csv" in src

    def test_differenziazione_da_feature_esistenti(self):
        src = _ui_src()
        assert "refrigerazione" in src.lower()
        assert "EER" in src

    def test_nessun_segreto_nella_sezione(self):
        assert not re.search(r'(?i)(api_key|secret|password)\s*=\s*["\']',
                             _ui_src())


class TestRegistry:
    """Verifiche sull'app.py applicato: falliscono finche' la
    tab668 non e' applicata (atteso in fase di authoring)."""

    def test_numero_tab_668(self):
        src = _app_src()
        assert len(re.findall(r"\n    with tab\d+:", src)) == 717

    def test_chain_tail_668(self):
        assert ", tab666, tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717 = st.tabs([" in _app_src()

    def test_titolo_668_in_app(self):
        assert TITLE668 in _app_src()

    def test_with_tab668_in_app(self):
        assert "\n    with tab668:" in _app_src()
