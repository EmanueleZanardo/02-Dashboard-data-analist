"""Test tab669 "⚡📋 Demand response: quanto rendono i servizi di flessibilità?"

Demo calcolata eseguendo mh669_demo_calcoli() (non a mano):
sito industriale con 2,0 MW di potenza flessibile in UVAM —
40 attivazioni/anno da 2 h con 90 % di successo; premio di
disponibilita' 25.000 EUR/MW/anno, prezzo attivazione
180 EUR/MWh; CAPEX 60.000 EUR, fee aggregatore 15 %,
O&M 3.000 EUR/anno, probabilita' penalita' 5 % con penale
8.000 EUR/evento; tasso 6 %, vita 10 anni, tolleranza 10 %
del CAPEX.

- E_att = 2,0 x 40 x 2,0 x 90,0/100 = 144.0 MWh/anno
- R_disp = 2,0 x 25000,0 = 50000.0 EUR/anno
- R_att = 144.0 x 180,0 = 25920.0 EUR/anno
- R = 50000.0 + 25920.0 = 75920.0 EUR/anno
- fee = 75920.0 x 15,0/100 = 11388.0 EUR/anno
- penale_attesa = 5,0/100 x 8000,0 = 400.0 EUR/anno
- C = 11388.0 + 3000.0 + 400.0 = 14788.0 EUR/anno
- M = 75920.0 - 14788.0 = 61132.0 EUR/anno
- flussi [-60000.0, 61132.0 x 10];
  VAN(6 %) = 389936.8416270836 EUR -> CONVIENTE (VAN > 0)
- TIR = 101.79567559043889 % (bisezione su [-0.99, 10])
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
    if (p / "w669_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w669_helpers.py via AST
    (stesso pattern di tests/appfuncs.py: niente Streamlit)."""
    src = (_new_dir() / "w669_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w669_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w669_helpers.py: {missing}")
    return out


_F = _load("mh669_num", "mh669_nneg", "mh669_pos", "mh669_int_pos",
           "mh669_energia_attivata_mwh",
           "mh669_ricavo_disponibilita",
           "mh669_ricavo_attivazione", "mh669_costi",
           "mh669_margine", "mh669_van", "mh669_tir",
           "mh669_payback", "mh669_verdetto", "_mh669_neutro",
           "mh669_business_case", "mh669_demo",
           "mh669_demo_calcoli")

TITLE669 = "⚡📋 Demand response: quanto rendono i servizi di flessibilità?"

E_ATT_DEMO = 144.0
RIC_DISP_DEMO = 50000.0
RIC_ATT_DEMO = 25920.0
RIC_TOT_DEMO = 75920.0
FEE_DEMO = 11388.0
PENALE_ATTESA_DEMO = 400.0
COSTI_TOT_DEMO = 14788.0
MARGINE_DEMO = 61132.0
VAN_DEMO = 389936.8416270836
TIR_PCT_DEMO = 101.79567559043889
PAYBACK_DEMO = 1
VITA_DEMO = 10
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w669_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w669_ui.py").read_text(encoding="utf-8")


def _app_src():
    return (Path.home() / "workspace/repo-dashboard/"
            "Dashboard-data-analist/app.py").read_text(
                encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh669_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh669_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh669_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh669_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh669_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh669_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh669_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh669_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh669_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh669_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh669_int_pos"](10.0, "x") == 10


class TestFisica:
    def test_energia_demo(self):
        assert _F["mh669_energia_attivata_mwh"](
            2.0, 40, 2.0, 90.0) == pytest.approx(E_ATT_DEMO,
                                                 rel=REL)

    def test_energia_rifiuta_potenza_zero(self):
        with pytest.raises(ValueError):
            _F["mh669_energia_attivata_mwh"](0.0, 40, 2.0,
                                             90.0)

    def test_energia_rifiuta_durata_zero(self):
        with pytest.raises(ValueError):
            _F["mh669_energia_attivata_mwh"](2.0, 40, 0.0,
                                             90.0)

    def test_energia_rifiuta_successo_sopra_100(self):
        with pytest.raises(ValueError):
            _F["mh669_energia_attivata_mwh"](2.0, 40, 2.0,
                                             101.0)

    def test_energia_rifiuta_successo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh669_energia_attivata_mwh"](2.0, 40, 2.0,
                                             -1.0)

    def test_energia_rifiuta_attivazioni_negative(self):
        with pytest.raises(ValueError):
            _F["mh669_energia_attivata_mwh"](2.0, -1, 2.0,
                                             90.0)

    def test_ricavo_disponibilita_demo(self):
        assert _F["mh669_ricavo_disponibilita"](
            2.0, 25000.0) == pytest.approx(RIC_DISP_DEMO,
                                           rel=REL)

    def test_ricavo_disponibilita_rifiuta_potenza_zero(self):
        with pytest.raises(ValueError):
            _F["mh669_ricavo_disponibilita"](0.0, 25000.0)

    def test_ricavo_attivazione_demo(self):
        assert _F["mh669_ricavo_attivazione"](
            E_ATT_DEMO, 180.0) == pytest.approx(RIC_ATT_DEMO,
                                                rel=REL)

    def test_ricavo_attivazione_rifiuta_prezzo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh669_ricavo_attivazione"](E_ATT_DEMO, -1.0)

    def test_costi_dict_demo(self):
        c = _F["mh669_costi"](RIC_TOT_DEMO, 15.0, 3000.0,
                              5.0, 8000.0)
        assert c["fee"] == pytest.approx(FEE_DEMO, rel=REL)
        assert c["penale_attesa"] == pytest.approx(
            PENALE_ATTESA_DEMO, rel=REL)
        assert c["totale"] == pytest.approx(COSTI_TOT_DEMO,
                                            rel=REL)

    def test_costi_rifiuta_fee_sopra_100(self):
        with pytest.raises(ValueError):
            _F["mh669_costi"](RIC_TOT_DEMO, 101.0, 3000.0,
                              5.0, 8000.0)

    def test_costi_rifiuta_prob_sopra_100(self):
        with pytest.raises(ValueError):
            _F["mh669_costi"](RIC_TOT_DEMO, 15.0, 3000.0,
                              101.0, 8000.0)

    def test_costi_rifiuta_om_negativo(self):
        with pytest.raises(ValueError):
            _F["mh669_costi"](RIC_TOT_DEMO, 15.0, -1.0, 5.0,
                              8000.0)

    def test_margine_demo(self):
        assert _F["mh669_margine"](
            RIC_TOT_DEMO, COSTI_TOT_DEMO) == pytest.approx(
            MARGINE_DEMO, rel=REL)

    def test_margine_puo_essere_negativo(self):
        assert _F["mh669_margine"](100.0, 200.0) == -100.0


class TestFinanza:
    def test_van_demo(self):
        assert _F["mh669_van"](
            MARGINE_DEMO, 60000.0, 6.0,
            VITA_DEMO) == pytest.approx(VAN_DEMO, rel=REL)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh669_van"](MARGINE_DEMO, 60000.0, -0.01,
                            10)

    def test_van_tasso_zero(self):
        assert _F["mh669_van"](
            MARGINE_DEMO, 60000.0, 0.0, 10) == pytest.approx(
            -60000.0 + MARGINE_DEMO * 10, rel=1e-12)

    def test_tir_none_se_margine_non_positivo(self):
        assert _F["mh669_tir"](60000.0, 0.0, 10) is None
        assert _F["mh669_tir"](60000.0, -100.0, 10) is None

    def test_tir_demo(self):
        assert _F["mh669_tir"](
            60000.0, MARGINE_DEMO, VITA_DEMO) * 100.0 == \
            pytest.approx(TIR_PCT_DEMO, rel=REL)

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh669_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo(self):
        assert _F["mh669_payback"](
            60000.0, MARGINE_DEMO, VITA_DEMO) == PAYBACK_DEMO

    def test_payback_none_mai(self):
        assert _F["mh669_payback"](100000.0, 1.0, 10) is None

    def test_payback_none_se_margine_non_positivo(self):
        assert _F["mh669_payback"](60000.0, 0.0, 10) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh669_verdetto"](
            VAN_DEMO, 60000.0, 10.0,
            MARGINE_DEMO) == VERDETTO_DEMO

    def test_verdetto_marginale_ad_hoc(self):
        # VAN negativo entro il 10 % del CAPEX
        assert _F["mh669_verdetto"](
            -0.05 * 60000.0, 60000.0, 10.0,
            MARGINE_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh669_verdetto"](
            -30000.0, 60000.0, 10.0,
            MARGINE_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_margine_non_positivo(
            self):
        assert _F["mh669_verdetto"](
            1000.0, 60000.0, 10.0,
            0.0) == "NON_CALCOLABILE"
        assert _F["mh669_verdetto"](
            1000.0, 60000.0, 10.0,
            -50.0) == "NON_CALCOLABILE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh669_verdetto"](100.0, 60000.0, -1.0,
                                 MARGINE_DEMO)


class TestGuard:
    def _bc(self, **kw):
        d = _F["mh669_demo"]()
        d.update(kw)
        return _F["mh669_business_case"](**d)

    def test_potenza_zero_neutra(self):
        n = self._bc(p_flex_mw=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["e_att_mwh"] == 0.0
        assert n["margine_eur"] == 0.0
        assert n["tir_pct"] is None
        assert n["payback_anni"] is None

    def test_successo_sopra_100_neutro(self):
        n = self._bc(succ_pct=101.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["van_eur"] == 0.0

    def test_nan_neutro(self):
        n = self._bc(r_pct=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["ric_tot"] == 0.0

    def test_bool_neutro(self):
        n = self._bc(p_flex_mw=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_margine_non_positivo_neutro(self):
        # nessun premio e fee al 100 %: i costi mangiano i
        # ricavi
        n = self._bc(premio_disp=0.0, fee_agg_pct=100.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["margine_eur"] == 0.0
        assert n["tir_pct"] is None
        assert n["payback_anni"] is None

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh669_neutro"]()
        assert list(n["df_voci"].columns) == ["Voce",
                                             "Valore (EUR/anno)"]
        assert len(n["df_voci"]) == 0

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh669_neutro"]()
        for chiave in ("e_att_mwh", "ric_disp", "ric_att",
                       "ric_tot", "fee", "penale_attesa",
                       "costi_tot", "margine_eur", "van_eur",
                       "tir_pct", "payback_anni", "verdetto",
                       "df_voci"):
            assert chiave in n, chiave

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert list(b["df_voci"].columns) == ["Voce",
                                             "Valore (EUR/anno)"]
        assert len(b["df_voci"]) == 8
        voci = b["df_voci"]["Voce"].tolist()
        assert "Margine netto" in voci
        assert "Premio di disponibilita'" in voci


class TestDemo:
    def test_demo_calcoli_end_to_end(self):
        c = _F["mh669_demo_calcoli"]()
        assert c["e_att_mwh"] == pytest.approx(E_ATT_DEMO,
                                               rel=REL)
        assert c["ric_disp"] == pytest.approx(RIC_DISP_DEMO,
                                              rel=REL)
        assert c["ric_att"] == pytest.approx(RIC_ATT_DEMO,
                                             rel=REL)
        assert c["ric_tot"] == pytest.approx(RIC_TOT_DEMO,
                                              rel=REL)
        assert c["fee"] == pytest.approx(FEE_DEMO, rel=REL)
        assert c["penale_attesa"] == pytest.approx(
            PENALE_ATTESA_DEMO, rel=REL)
        assert c["costi_tot"] == pytest.approx(COSTI_TOT_DEMO,
                                               rel=REL)
        assert c["margine_eur"] == pytest.approx(
            MARGINE_DEMO, rel=REL)
        assert c["van_eur"] == pytest.approx(VAN_DEMO, rel=REL)
        assert c["tir_pct"] == pytest.approx(TIR_PCT_DEMO,
                                             rel=REL)
        assert c["payback_anni"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO

    def test_demo_calcoli_deterministico(self):
        assert _F["mh669_demo_calcoli"]()[
            "van_eur"] == _F["mh669_demo_calcoli"]()["van_eur"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        """business_case(**demo()) deve matchare le costanti
        _DEMO entro 1e-9 relativo (mismatch vietato)."""
        d = _F["mh669_demo"]()
        b = _F["mh669_business_case"](**d)
        coppie = [("e_att_mwh", E_ATT_DEMO),
                  ("ric_disp", RIC_DISP_DEMO),
                  ("ric_att", RIC_ATT_DEMO),
                  ("ric_tot", RIC_TOT_DEMO),
                  ("fee", FEE_DEMO),
                  ("penale_attesa", PENALE_ATTESA_DEMO),
                  ("costi_tot", COSTI_TOT_DEMO),
                  ("margine_eur", MARGINE_DEMO),
                  ("van_eur", VAN_DEMO),
                  ("tir_pct", TIR_PCT_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert b["payback_anni"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh669_demo"]()
        assert d["p_flex_mw"] == 2.0
        assert d["n_att"] == 40
        assert d["h_att"] == 2.0
        assert d["succ_pct"] == 90.0
        assert d["premio_disp"] == 25000.0
        assert d["p_att"] == 180.0
        assert d["capex"] == 60000.0
        assert d["fee_agg_pct"] == 15.0
        assert d["om"] == 3000.0
        assert d["prob_pen_pct"] == 5.0
        assert d["penale_evento"] == 8000.0
        assert d["r_pct"] == 6.0
        assert d["n"] == 10
        assert d["tol_pct"] == 10.0

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        mh669_demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["mh669_demo_calcoli"]()
        doc = __doc__
        for chiave in ("e_att_mwh", "ric_disp", "ric_att",
                       "ric_tot", "fee", "penale_attesa",
                       "costi_tot", "margine_eur", "van_eur",
                       "tir_pct"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback_anni = 1" in doc
        assert "verdetto = 'CONVIENTE'" in doc


class TestUI:
    def test_header_helpers_presente(self):
        assert '# W669 (23/10/2026) - tab669' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh669_num", "mh669_nneg", "mh669_pos",
                     "mh669_int_pos",
                     "mh669_energia_attivata_mwh",
                     "mh669_ricavo_disponibilita",
                     "mh669_ricavo_attivazione", "mh669_costi",
                     "mh669_margine", "mh669_van", "mh669_tir",
                     "mh669_payback", "mh669_verdetto",
                     "_mh669_neutro", "mh669_business_case",
                     "mh669_demo", "mh669_demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE669) == 1

    def test_blocco_with_tab669(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab669:"

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st669_[a-z0-9_]+)"', _ui_src())
        assert len(keys) >= 16
        assert len(set(keys)) == len(keys)
        # nessuna collisione con le chiavi dei cicli precedenti
        assert not any(k.startswith("st668_") for k in keys)

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
        assert "Margine annuo (€/anno)" in src
        assert "Energia attivata (MWh/anno)" in src
        assert "VAN (€)" in src
        assert "Payback (anni)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd669" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_grafico_ricavi_costi_presente(self):
        src = _ui_src()
        assert "plotly.graph_objects" in src
        assert "Premio disponibilita'" in src
        assert "Ricavi attivazioni" in src
        assert "Margine netto" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert 'sep=";"' in src
        assert "demand_response.csv" in src

    def test_sensitivita_presente(self):
        src = _ui_src()
        assert "Sensitiv" in src
        assert "mh669_business_case" in src

    def test_differenziazione_da_feature_esistenti(self):
        src = _ui_src()
        assert "demand response" in src.lower()
        assert "UVAM" in src

    def test_nessun_segreto_nella_sezione(self):
        assert not re.search(r'(?i)(api_key|secret|password)\s*=\s*["\']',
                             _ui_src())


class TestRegistry:
    """Verifiche sull'app.py applicato: falliscono finche' la
    tab669 non e' applicata (atteso in fase di authoring)."""

    def test_numero_tab_669(self):
        src = _app_src()
        assert len(re.findall(r"\n    with tab\d+:", src)) == 684

    def test_chain_tail_669(self):
        assert ", tab667, tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684 = st.tabs([" in _app_src()

    def test_titolo_669_in_app(self):
        assert TITLE669 in _app_src()

    def test_with_tab669_in_app(self):
        assert "\n    with tab669:" in _app_src()
