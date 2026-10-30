"""Test tab667 "🌊〰️ Moto ondoso: il business case wave energy"

Demo calcolata eseguendo mh667_demo_calcoli() (non a mano):
sito con Hs = 2,0 m e Te = 8,0 s; dispositivo da 1.500 kW
nominali, larghezza di cattura 150 m, efficienza di cattura
25 %, disponibilita' 92 %; strike 250 EUR/MWh; CAPEX specifico
6.500 EUR/kW, OPEX 180 EUR/kW/anno; fattore CO2 rete
0,35 t/MWh; tasso 6 %, vita 25 anni, tolleranza 10 % del
CAPEX.

- P_risorsa = (1025 x 9,81^2 / (64 x pi) / 1000) x 2,0^2 x 8,0
            = 15.699362294358098 kW/m
- P_media_raw = 15.699362294358098 x 150 x 0,25 x 0,92
              = 541.6279991553544 kW
- P_media = min(541.6279991553544, 1500,0)
          = 541.6279991553544 kW
- E = 541.6279991553544 x 8760 / 1000 = 4744.661272600904 MWh/anno
- CF = 4744.661272600904 x 1000 / (1500,0 x 8760)
     = 0.36108533277023624
- CAPEX = 1500,0 x 6500,0 = 9750000.0 EUR
- O&M = 1500,0 x 180,0 = 270000.0 EUR/anno
- ricavo = 4744.661272600904 x 250,0 = 1186165.318150226 EUR/anno
- utile = 1186165.318150226 - 270000,0 = 916165.318150226 EUR/anno
- CO2 evitata = 4744.661272600904 x 0,35 = 1660.6314454103165 t/anno
- flussi [-9750000.0, 916165.318150226 x 25];
  VAN(6 %) = 1961667.5617676207 EUR -> CONVIENTE (VAN > 0)
- TIR = 0.08035831825490072 (bisezione su [-0.9999, 10])
- payback = 11 (primo anno con cumulato >= 0)
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
    if (p / "w667_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w667_helpers.py via AST
    (stesso pattern di tests/appfuncs.py: niente Streamlit)."""
    src = (_new_dir() / "w667_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w667_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w667_helpers.py: {missing}")
    return out


_F = _load("mh667_num", "mh667_nneg", "mh667_pos", "mh667_int_pos",
           "mh667_frac01",
           "mh667_p_risorsa_kw_m", "mh667_p_media_raw_kw",
           "mh667_p_media_kw", "mh667_e_mwh_anno", "mh667_cf",
           "mh667_capex", "mh667_om_annuo",
           "mh667_ricavo_annuo", "mh667_utile_annuo",
           "mh667_co2_evitata_t_anno",
           "mh667_flussi", "mh667_van", "mh667_tir",
           "mh667_payback", "mh667_verdetto",
           "mh667_demo", "mh667_demo_calcoli")

TITLE667 = "🌊〰️ Moto ondoso: il business case wave energy"

P_RISORSA_DEMO = 15.699362294358098
P_MEDIA_RAW_DEMO = 541.6279991553544
P_MEDIA_DEMO = 541.6279991553544
E_DEMO = 4744.661272600904
CF_DEMO = 0.36108533277023624
CAPEX_DEMO = 9750000.0
OM_DEMO = 270000.0
RICAVO_DEMO = 1186165.318150226
UTILE_DEMO = 916165.318150226
CO2_DEMO = 1660.6314454103165
VAN_DEMO = 1961667.5617676207
TIR_DEMO = 0.08035831825490072
PAYBACK_DEMO = 11
VITA_DEMO = 25
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w667_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w667_ui.py").read_text(encoding="utf-8")


def _app_src():
    return (Path.home() / "workspace/repo-dashboard/"
            "Dashboard-data-analist/app.py").read_text(
                encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh667_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh667_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh667_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh667_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh667_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh667_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh667_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh667_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh667_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh667_int_pos"](True, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh667_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh667_int_pos"](25.0, "x") == 25

    def test_frac01_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh667_frac01"](-0.1, "x")

    def test_frac01_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh667_frac01"](1.1, "x")

    def test_frac01_accetta_bordi(self):
        assert _F["mh667_frac01"](0.0, "x") == 0.0
        assert _F["mh667_frac01"](1.0, "x") == 1.0


class TestFisica:
    def test_p_risorsa_demo(self):
        assert _F["mh667_p_risorsa_kw_m"](
            2.0, 8.0) == pytest.approx(P_RISORSA_DEMO, rel=REL)

    def test_p_risorsa_quadratica_in_hs(self):
        # raddoppio Hs -> x4 potenza
        assert _F["mh667_p_risorsa_kw_m"](
            4.0, 8.0) == pytest.approx(4.0 * P_RISORSA_DEMO,
                                       rel=REL)

    def test_p_risorsa_lineare_in_te(self):
        assert _F["mh667_p_risorsa_kw_m"](
            2.0, 4.0) == pytest.approx(P_RISORSA_DEMO / 2.0,
                                       rel=REL)

    def test_p_risorsa_rifiuta_hs_negativo(self):
        with pytest.raises(ValueError):
            _F["mh667_p_risorsa_kw_m"](-1.0, 8.0)

    def test_p_risorsa_rifiuta_te_zero(self):
        with pytest.raises(ValueError):
            _F["mh667_p_risorsa_kw_m"](2.0, 0.0)

    def test_p_media_raw_demo(self):
        assert _F["mh667_p_media_raw_kw"](
            P_RISORSA_DEMO, 150.0, 0.25,
            0.92) == pytest.approx(P_MEDIA_RAW_DEMO, rel=REL)

    def test_p_media_raw_rifiuta_eta_fuori_01(self):
        with pytest.raises(ValueError):
            _F["mh667_p_media_raw_kw"](P_RISORSA_DEMO, 150.0,
                                       1.5, 0.92)

    def test_p_media_raw_rifiuta_larghezza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh667_p_media_raw_kw"](P_RISORSA_DEMO, -10.0,
                                       0.25, 0.92)

    def test_p_media_demo_non_satura(self):
        # 541.6 kW < 1500 kW nominali -> nessun clipping
        assert _F["mh667_p_media_kw"](
            P_MEDIA_RAW_DEMO, 1500.0) == pytest.approx(
            P_MEDIA_DEMO, rel=REL)

    def test_p_media_satura_alla_nominale(self):
        assert _F["mh667_p_media_kw"](
            5000.0, 1500.0) == pytest.approx(1500.0, rel=REL)

    def test_p_media_zero_con_nominale_zero(self):
        assert _F["mh667_p_media_kw"](
            P_MEDIA_RAW_DEMO, 0.0) == pytest.approx(0.0)

    def test_e_mwh_demo(self):
        assert _F["mh667_e_mwh_anno"](
            P_MEDIA_DEMO) == pytest.approx(E_DEMO, rel=REL)

    def test_e_mwh_8760_ore(self):
        assert _F["mh667_e_mwh_anno"](1000.0) == pytest.approx(
            8760.0, rel=REL)

    def test_cf_demo(self):
        assert _F["mh667_cf"](
            E_DEMO, 1500.0) == pytest.approx(CF_DEMO, rel=REL)

    def test_cf_none_con_nominale_zero(self):
        assert _F["mh667_cf"](E_DEMO, 0.0) is None

    def test_cf_uno_a_piena_nominale(self):
        # P_media = P_rated per tutte le 8760 h -> CF = 1
        assert _F["mh667_cf"](8760.0, 1000.0) == pytest.approx(
            1.0, rel=REL)

    def test_capex_demo(self):
        assert _F["mh667_capex"](
            1500.0, 6500.0) == pytest.approx(CAPEX_DEMO,
                                             rel=REL)

    def test_capex_rifiuta_specifico_negativo(self):
        with pytest.raises(ValueError):
            _F["mh667_capex"](1500.0, -10.0)

    def test_om_demo(self):
        assert _F["mh667_om_annuo"](
            1500.0, 180.0) == pytest.approx(OM_DEMO, rel=REL)

    def test_ricavo_demo(self):
        assert _F["mh667_ricavo_annuo"](
            E_DEMO, 250.0) == pytest.approx(RICAVO_DEMO,
                                            rel=REL)

    def test_ricavo_rifiuta_strike_negativo(self):
        with pytest.raises(ValueError):
            _F["mh667_ricavo_annuo"](E_DEMO, -1.0)

    def test_utile_demo(self):
        assert _F["mh667_utile_annuo"](
            RICAVO_DEMO, OM_DEMO) == pytest.approx(UTILE_DEMO,
                                                  rel=REL)

    def test_utile_negativo_possibile(self):
        assert _F["mh667_utile_annuo"](100000.0,
                                       270000.0) == pytest.approx(
            -170000.0)

    def test_co2_evitata_demo(self):
        assert _F["mh667_co2_evitata_t_anno"](
            E_DEMO, 0.35) == pytest.approx(CO2_DEMO, rel=REL)

    def test_co2_evitata_rifiuta_fattore_negativo(self):
        with pytest.raises(ValueError):
            _F["mh667_co2_evitata_t_anno"](E_DEMO, -0.1)


class TestFinanza:
    def _flussi_demo(self):
        return _F["mh667_flussi"](CAPEX_DEMO, UTILE_DEMO,
                                  VITA_DEMO)

    def test_flussi_struttura(self):
        fl = self._flussi_demo()
        assert fl[0] == -CAPEX_DEMO and len(fl) == 26
        assert all(f == UTILE_DEMO for f in fl[1:])

    def test_flussi_rifiuta_vita_zero(self):
        with pytest.raises(ValueError):
            _F["mh667_flussi"](9750000.0, 100.0, 0)

    def test_van_demo(self):
        assert _F["mh667_van"](self._flussi_demo(),
                               0.06) == pytest.approx(VAN_DEMO,
                                                      rel=REL)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh667_van"](self._flussi_demo(), -0.01)

    def test_van_tasso_zero(self):
        fl = [-9750000.0, 916165.32, 916165.32]
        assert _F["mh667_van"](fl, 0.0) == pytest.approx(
            -7917669.36, rel=1e-6)

    def test_tir_demo(self):
        assert _F["mh667_tir"](self._flussi_demo()) == \
            pytest.approx(TIR_DEMO, rel=REL)

    def test_tir_none_senza_cambio_segno(self):
        assert _F["mh667_tir"]([-100.0, -10.0, -10.0]) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh667_tir"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo(self):
        assert _F["mh667_payback"](self._flussi_demo()) == \
            PAYBACK_DEMO

    def test_payback_none_mai(self):
        assert _F["mh667_payback"]([-100.0, 1.0, 1.0]) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh667_verdetto"](E_DEMO, UTILE_DEMO,
                                    VAN_DEMO, CAPEX_DEMO,
                                    0.10) == VERDETTO_DEMO

    def test_verdetto_marginale_tolleranza_ampia(self):
        assert _F["mh667_verdetto"](E_DEMO, UTILE_DEMO,
                                    -0.05 * CAPEX_DEMO,
                                    CAPEX_DEMO,
                                    0.10) == "MARGINALE"

    def test_verdetto_non_conviente_van_oltre_tolleranza(self):
        assert _F["mh667_verdetto"](E_DEMO, UTILE_DEMO,
                                    -CAPEX_DEMO, CAPEX_DEMO,
                                    0.10) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_energia_zero(self):
        assert _F["mh667_verdetto"](0.0, UTILE_DEMO, VAN_DEMO,
                                    CAPEX_DEMO,
                                    0.10) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_utile_zero(self):
        assert _F["mh667_verdetto"](E_DEMO, 0.0, 500.0,
                                    CAPEX_DEMO,
                                    0.10) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_utile_negativo(self):
        assert _F["mh667_verdetto"](E_DEMO, -100.0, 500.0,
                                    CAPEX_DEMO,
                                    0.10) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_van_none(self):
        assert _F["mh667_verdetto"](E_DEMO, UTILE_DEMO, None,
                                    CAPEX_DEMO,
                                    0.10) == "NON_CALCOLABILE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh667_verdetto"](E_DEMO, UTILE_DEMO, 100.0,
                                 CAPEX_DEMO, -0.1)


class TestDemo:
    def test_demo_calcoli_end_to_end(self):
        c = _F["mh667_demo_calcoli"]()
        assert c["p_risorsa_kw_m"] == pytest.approx(
            P_RISORSA_DEMO, rel=REL)
        assert c["p_media_raw_kw"] == pytest.approx(
            P_MEDIA_RAW_DEMO, rel=REL)
        assert c["p_media_kw"] == pytest.approx(P_MEDIA_DEMO,
                                                rel=REL)
        assert c["e_mwh_anno"] == pytest.approx(E_DEMO, rel=REL)
        assert c["cf"] == pytest.approx(CF_DEMO, rel=REL)
        assert c["capex_eur"] == pytest.approx(CAPEX_DEMO,
                                               rel=REL)
        assert c["om_eur_anno"] == pytest.approx(OM_DEMO,
                                                 rel=REL)
        assert c["ricavo_eur_anno"] == pytest.approx(
            RICAVO_DEMO, rel=REL)
        assert c["utile_eur_anno"] == pytest.approx(UTILE_DEMO,
                                                   rel=REL)
        assert c["co2_evitata_t_anno"] == pytest.approx(
            CO2_DEMO, rel=REL)
        assert c["van_eur"] == pytest.approx(VAN_DEMO, rel=REL)
        assert c["tir"] == pytest.approx(TIR_DEMO, rel=REL)
        assert c["payback_anni"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO

    def test_demo_calcoli_deterministico(self):
        assert _F["mh667_demo_calcoli"]() == _F["mh667_demo_calcoli"]()

    def test_demo_defaults(self):
        d = _F["mh667_demo"]()
        assert d["Hs"] == 2.0
        assert d["Te"] == 8.0
        assert d["larghezza_m"] == 150.0
        assert d["eta_cattura"] == 0.25
        assert d["disponibilita"] == 0.92
        assert d["P_rated_kW"] == 1500.0
        assert d["strike_eur_mwh"] == 250.0
        assert d["capex_eur_kw"] == 6500.0
        assert d["opex_eur_kw_anno"] == 180.0
        assert d["f_co2_rete_t_mwh"] == 0.35
        assert d["tasso"] == 0.06
        assert d["vita_anni"] == 25
        assert d["toll_frac"] == 0.10

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        mh667_demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["mh667_demo_calcoli"]()
        doc = __doc__
        for chiave in ("p_risorsa_kw_m", "p_media_raw_kw",
                       "p_media_kw", "e_mwh_anno", "cf",
                       "capex_eur", "om_eur_anno",
                       "ricavo_eur_anno", "utile_eur_anno",
                       "co2_evitata_t_anno", "van_eur", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 11" in doc
        assert "verdetto = 'CONVIENTE'" in doc


class TestUI:
    def test_header_helpers_presente(self):
        assert '# W667 (23/10/2026) - tab667' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh667_num", "mh667_nneg", "mh667_pos",
                     "mh667_int_pos", "mh667_frac01",
                     "mh667_p_risorsa_kw_m",
                     "mh667_p_media_raw_kw", "mh667_p_media_kw",
                     "mh667_e_mwh_anno", "mh667_cf",
                     "mh667_capex", "mh667_om_annuo",
                     "mh667_ricavo_annuo", "mh667_utile_annuo",
                     "mh667_co2_evitata_t_anno",
                     "mh667_flussi", "mh667_van", "mh667_tir",
                     "mh667_payback", "mh667_verdetto",
                     "mh667_demo", "mh667_demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE667) == 1

    def test_blocco_with_tab667(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab667:"

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st667_[a-z0-9_]+)"', _ui_src())
        assert len(keys) >= 16
        assert len(set(keys)) == len(keys)
        # nessuna collisione con le chiavi del ciclo precedente
        assert not any(k.startswith("st666_") for k in keys)

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_ut667 <= 0.0" in src
        assert "NON_CALCOLABILE" in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_ut667 <= 0.0") < src.index(".metric(")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Potenza d'onda (kW/m)" in src
        assert "Energia (MWh/anno)" in src
        assert "Utile (€/anno)" in src
        assert "Payback (anni)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd667" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_grafico_ricavo_vs_om_presente(self):
        src = _ui_src()
        assert "plotly.graph_objects" in src
        assert "Ricavo a strike (scenario)" in src
        assert "O&M (scenario)" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert 'sep=";"' in src
        assert "moto_ondoso_wave_energy.csv" in src

    def test_differenziazione_da_feature_esistenti(self):
        src = _ui_src()
        assert "wave energy" in src
        assert "ondoso" in src.lower()

    def test_nessun_segreto_nella_sezione(self):
        assert not re.search(r'(?i)(api_key|secret|password)\s*=\s*["\']',
                             _ui_src())


class TestRegistry:
    """Verifiche sull'app.py applicato: falliscono finche' la
    tab667 non e' applicata (atteso in fase di authoring)."""

    def test_numero_tab_667(self):
        src = _app_src()
        assert len(re.findall(r"\n    with tab\d+:", src)) == 820

    def test_chain_tail_667(self):
        # APPEND boundary-safe: tab671 appeso in coda alla catena
        assert "tab818, tab819, tab820 = st.tabs" in _app_src()

    def test_titolo_667_in_app(self):
        assert TITLE667 in _app_src()

    def test_with_tab667_in_app(self):
        assert "\n    with tab667:" in _app_src()
