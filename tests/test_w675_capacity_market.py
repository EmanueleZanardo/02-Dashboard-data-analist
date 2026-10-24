"""Test tab675 "🏛️⚡ Mercato della capacita': la remunerazione della capacita' disponibile paga?"

Demo calcolata eseguendo demo_calcoli() (non a mano):
CCGT da 400 MW con derating 0,90 (capacita' deratata
360 MW), premio di capacita' 33.000 EUR/MW/anno e
disponibilita' effettiva 0,97; energia attivata a salire
15.000 MWh/anno a 120 EUR/MWh; 80 avviamenti/anno a
5.000 EUR l'uno; costo variabile 60 EUR/MWh; O&M
2.000.000 EUR/anno; CAPEX 0 EUR (impianto esistente);
fattore emissivo 360 kg CO2/MWh; tasso 0,06 (6 %),
vita 15 anni, tolleranza 0,10 (10 % del CAPEX).

- cap_deratata = 400.0 x 0.90 = 360.0 MW
- ricavi_premio = 360.0 x 33000.0 x 0.97 = 11523600.0 EUR/anno
- ricavi_en_up = 15000.0 x 120.0 = 1800000.0 EUR/anno
- ricavi = 13323600.0 EUR/anno
- costi_avviamenti = 80 x 5000.0 = 400000.0 EUR/anno
- costi_en_up = 15000.0 x 60.0 = 900000.0 EUR/anno
- costi = 400000.0 + 900000.0 + 2000000.0 = 3300000.0 EUR/anno
- risp = 13323600.0 - 3300000.0 = 10023600.0 EUR/anno
- co2_t = 15000.0 x 360.0/1000 = 5400.0 t/anno (extra emessa: l'energia attivata a salire emette CO2 e il premio di capacita', da solo, non la compensa)
- flussi [-0.0, 10023600.0 x 15];
  VAN(0,06) = 97351698.9535206 EUR -> CONVIENTE (VAN >= 0)
- tir = None (CAPEX = 0: nessun cambio di segno)
- payback = 1 (CAPEX = 0, primo anno con cumulato >= 0)
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
    if (p / "w675_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w675_helpers.py via AST
    (stesso pattern di tests/appfuncs.py: niente Streamlit)."""
    src = (_new_dir() / "w675_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w675_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w675_helpers.py: {missing}")
    return out


_F = _load("mh675_num", "mh675_nneg", "mh675_pos", "mh675_int_pos",
           "mh675_capacita_deratata", "mh675_ricavi_premio",
           "mh675_ricavi_en_up", "mh675_costi_avviamenti",
           "mh675_costi_en_up", "mh675_risparmio", "mh675_co2",
           "mh675_van", "mh675_tir", "mh675_payback",
           "mh675_verdetto", "_mh675_neutro", "mh675_calcola",
           "mh675_demo", "demo_calcoli")

TITLE675 = ("🏛️⚡ Mercato della capacità: la remunerazione "
            "della capacità disponibile paga?")

CAP_DERATATA_DEMO = 360.0
RICAVI_PREMIO_DEMO = 11523600.0
RICAVI_UP_DEMO = 1800000.0
RICAVI_DEMO = 13323600.0
COSTI_AVV_DEMO = 400000.0
COSTI_EN_UP_DEMO = 900000.0
COSTI_DEMO = 3300000.0
RISP_DEMO = 10023600.0
CO2_DEMO = 5400.0
VAN_DEMO = 97351698.9535206
PAYBACK_DEMO = 1
VITA_DEMO = 15
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w675_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w675_ui.py").read_text(encoding="utf-8")


def _test_src():
    return (_new_dir() / "w675_test.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh675_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh675_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh675_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh675_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh675_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh675_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh675_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh675_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh675_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh675_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh675_int_pos"](15.0, "x") == 15


class TestFisica:
    def test_cap_deratata_demo(self):
        assert _F["mh675_capacita_deratata"](
            400.0, 0.90) == pytest.approx(
            CAP_DERATATA_DEMO, rel=REL)

    def test_cap_deratata_rifiuta_p_zero(self):
        with pytest.raises(ValueError):
            _F["mh675_capacita_deratata"](0.0, 0.90)

    def test_cap_deratata_rifiuta_p_negativa(self):
        with pytest.raises(ValueError):
            _F["mh675_capacita_deratata"](-400.0, 0.90)

    def test_cap_deratata_rifiuta_derating_oltre_1(self):
        with pytest.raises(ValueError):
            _F["mh675_capacita_deratata"](400.0, 1.01)

    def test_cap_deratata_rifiuta_derating_negativo(self):
        with pytest.raises(ValueError):
            _F["mh675_capacita_deratata"](400.0, -0.01)

    def test_cap_deratata_zero_se_derating_zero(self):
        assert _F["mh675_capacita_deratata"](400.0, 0.0) == 0.0

    def test_ricavi_premio_demo(self):
        assert _F["mh675_ricavi_premio"](
            360.0, 33000.0, 0.97) == pytest.approx(
            RICAVI_PREMIO_DEMO, rel=REL)

    def test_ricavi_premio_rifiuta_disp_oltre_1(self):
        with pytest.raises(ValueError):
            _F["mh675_ricavi_premio"](360.0, 33000.0, 1.01)

    def test_ricavi_premio_rifiuta_disp_negativa(self):
        with pytest.raises(ValueError):
            _F["mh675_ricavi_premio"](360.0, 33000.0, -0.01)

    def test_ricavi_premio_rifiuta_premio_negativo(self):
        with pytest.raises(ValueError):
            _F["mh675_ricavi_premio"](360.0, -0.01, 0.97)

    def test_ricavi_premio_zero_se_disp_zero(self):
        assert _F["mh675_ricavi_premio"](
            360.0, 33000.0, 0.0) == 0.0

    def test_ricavi_en_up_demo(self):
        assert _F["mh675_ricavi_en_up"](
            15000.0, 120.0) == pytest.approx(RICAVI_UP_DEMO,
                                             rel=REL)

    def test_ricavi_en_up_zero_se_e_up_zero(self):
        assert _F["mh675_ricavi_en_up"](0.0, 120.0) == 0.0

    def test_ricavi_en_up_rifiuta_e_negativa(self):
        with pytest.raises(ValueError):
            _F["mh675_ricavi_en_up"](-1.0, 120.0)

    def test_ricavi_en_up_rifiuta_prezzo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh675_ricavi_en_up"](15000.0, -0.01)

    def test_costi_avviamenti_demo(self):
        assert _F["mh675_costi_avviamenti"](
            80, 5000.0) == pytest.approx(COSTI_AVV_DEMO,
                                        rel=REL)

    def test_costi_avviamenti_zero_se_n_avv_zero(self):
        assert _F["mh675_costi_avviamenti"](0, 5000.0) == 0.0

    def test_costi_avviamenti_rifiuta_n_negativo(self):
        with pytest.raises(ValueError):
            _F["mh675_costi_avviamenti"](-1, 5000.0)

    def test_costi_avviamenti_rifiuta_costo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh675_costi_avviamenti"](80, -0.01)

    def test_costi_en_up_demo(self):
        assert _F["mh675_costi_en_up"](
            15000.0, 60.0) == pytest.approx(COSTI_EN_UP_DEMO,
                                           rel=REL)

    def test_costi_en_up_zero_se_e_up_zero(self):
        assert _F["mh675_costi_en_up"](0.0, 60.0) == 0.0

    def test_costi_en_up_rifiuta_e_negativa(self):
        with pytest.raises(ValueError):
            _F["mh675_costi_en_up"](-1.0, 60.0)

    def test_costi_en_up_rifiuta_costo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh675_costi_en_up"](15000.0, -0.01)

    def test_risparmio_demo(self):
        assert _F["mh675_risparmio"](
            RICAVI_PREMIO_DEMO, RICAVI_UP_DEMO,
            COSTI_AVV_DEMO, COSTI_EN_UP_DEMO,
            2000000.0) == pytest.approx(RISP_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh675_risparmio"](
            100.0, 50.0, 90.0, 50.0, 20.0) == -10.0

    def test_risparmio_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh675_risparmio"](
                float("nan"), 0.0, 0.0, 0.0, 0.0)

    def test_co2_demo(self):
        assert _F["mh675_co2"](
            15000.0, 360.0) == pytest.approx(CO2_DEMO,
                                            rel=REL)

    def test_co2_e_zero_se_energia_zero(self):
        assert _F["mh675_co2"](0.0, 360.0) == 0.0

    def test_co2_rifiuta_fattore_negativo(self):
        with pytest.raises(ValueError):
            _F["mh675_co2"](15000.0, -0.01)


class TestFinanza:
    def test_van_demo(self):
        assert _F["mh675_van"](
            RISP_DEMO, 0.0, 0.06,
            VITA_DEMO) == pytest.approx(VAN_DEMO, rel=REL)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh675_van"](RISP_DEMO, 0.0, -0.01, 15)

    def test_van_tasso_zero(self):
        assert _F["mh675_van"](
            RISP_DEMO, 1000000.0, 0.0, 15) == pytest.approx(
            -1000000.0 + RISP_DEMO * 15, rel=1e-12)

    def test_tir_none_se_risp_non_positivo(self):
        assert _F["mh675_tir"](1000000.0, 0.0, 15) is None
        assert _F["mh675_tir"](1000000.0, -100.0, 15) is None

    def test_tir_none_se_capex_zero_demo(self):
        # CAPEX = 0: nessun cambio di segno -> None
        assert _F["mh675_tir"](
            0.0, RISP_DEMO, VITA_DEMO) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh675_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo(self):
        assert _F["mh675_payback"](
            0.0, RISP_DEMO, VITA_DEMO) == PAYBACK_DEMO

    def test_payback_none_mai(self):
        assert _F["mh675_payback"](1000000.0, 1.0, 15) is None

    def test_payback_none_se_risp_non_positivo(self):
        assert _F["mh675_payback"](1000000.0, 0.0, 15) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh675_verdetto"](
            VAN_DEMO, 0.0, 0.10,
            RISP_DEMO) == VERDETTO_DEMO

    def test_verdetto_marginale_ad_hoc(self):
        # VAN negativo entro la tolleranza x CAPEX
        assert _F["mh675_verdetto"](
            -0.05 * 1000000.0, 1000000.0, 0.10,
            RISP_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh675_verdetto"](
            -500000.0, 1000000.0, 0.10,
            RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risp_non_positivo(self):
        assert _F["mh675_verdetto"](
            1000.0, 1000000.0, 0.10,
            0.0) == "NON_CALCOLABILE"
        assert _F["mh675_verdetto"](
            1000.0, 1000000.0, 0.10,
            -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_non_negativo_conviente(self):
        assert _F["mh675_verdetto"](
            0.0, 0.0, 0.10, RISP_DEMO) == "CONVIENTE"
        assert _F["mh675_verdetto"](
            1000.0, 0.0, 0.10, RISP_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(self):
        # CAPEX == 0: tolleranza zero, mai MARGINALE
        assert _F["mh675_verdetto"](
            -1.0, 0.0, 0.10, RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh675_verdetto"](100.0, 1000000.0, -0.01,
                                 RISP_DEMO)


class TestGuard:
    def _bc(self, **kw):
        d = _F["mh675_demo"]()
        d.update(kw)
        return _F["mh675_calcola"](**d)

    def test_p_nom_zero_neutro(self):
        n = self._bc(p_nom=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["ricavi"] == 0.0
        assert n["risp"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_p_nom_negativo_neutro(self):
        n = self._bc(p_nom=-400.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_derating_oltre_1_neutro(self):
        n = self._bc(derating=1.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_derating_negativo_neutro(self):
        n = self._bc(derating=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_disp_oltre_1_neutro(self):
        n = self._bc(disponibilita=1.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_disp_negativa_neutro(self):
        n = self._bc(disponibilita=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_e_up_negativo_neutro(self):
        n = self._bc(energia_up_mwh=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_n_avviamenti_negativo_neutro(self):
        n = self._bc(n_avviamenti=-1)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_costo_avviamento_negativo_neutro(self):
        n = self._bc(costo_avviamento=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_p_up_negativo_neutro(self):
        n = self._bc(prezzo_up=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_costo_variabile_negativo_neutro(self):
        n = self._bc(costo_variabile=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_om_negativo_neutro(self):
        n = self._bc(opex_om=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_fattore_co2_negativo_neutro(self):
        n = self._bc(fattore_co2=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tasso_negativo_neutro(self):
        n = self._bc(tasso=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_negativa_neutro(self):
        n = self._bc(tolleranza=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(premio=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["ricavi"] == 0.0

    def test_bool_neutro(self):
        n = self._bc(p_nom=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_risp_non_positivo_neutro(self):
        # premio nullo (derating zero) mentre avviamenti,
        # costo variabile e O&M pesano: la capacita' non
        # paga
        n = self._bc(derating=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risp"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh675_neutro"]()
        assert list(n["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(n["df_flussi"]) == 0
        assert list(n["df_tabella"].columns) == ["Voce",
                                                 "Valore (EUR/anno)"]
        assert len(n["df_tabella"]) == 0

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh675_neutro"]()
        for chiave in ("cap_deratata", "ricavi", "costi",
                       "risp", "co2_t", "van", "tir",
                       "payback", "verdetto", "df_flussi",
                       "df_tabella"):
            assert chiave in n, chiave

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert list(b["df_tabella"].columns) == ["Voce",
                                                 "Valore (EUR/anno)"]
        assert len(b["df_tabella"]) == 6
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Ricavi premio capacita'" in voci
        assert "Risparmio netto" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(b["df_flussi"]) == VITA_DEMO + 1
        assert b["df_flussi"]["Cumulato (€)"].iloc[-1] == \
            pytest.approx(RISP_DEMO * VITA_DEMO, rel=REL)


class TestDemo:
    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["cap_deratata"] == pytest.approx(
            CAP_DERATATA_DEMO, rel=REL)
        assert c["ricavi"] == pytest.approx(
            RICAVI_DEMO, rel=REL)
        assert c["costi"] == pytest.approx(
            COSTI_DEMO, rel=REL)
        assert c["risp"] == pytest.approx(RISP_DEMO, rel=REL)
        assert c["co2_t"] == pytest.approx(
            CO2_DEMO, rel=REL)
        assert c["van"] == pytest.approx(VAN_DEMO, rel=REL)
        assert c["tir"] is None
        assert c["payback"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()[
            "van"] == _F["demo_calcoli"]()["van"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        """mh675_calcola(**mh675_demo()) deve matchare le
        costanti _DEMO entro 1e-9 relativo (mismatch
        vietato), chiave per chiave."""
        d = _F["mh675_demo"]()
        b = _F["mh675_calcola"](**d)
        coppie = [("cap_deratata", CAP_DERATATA_DEMO),
                  ("ricavi", RICAVI_DEMO),
                  ("costi", COSTI_DEMO),
                  ("risp", RISP_DEMO),
                  ("co2_t", CO2_DEMO),
                  ("van", VAN_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert b["tir"] is None
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh675_demo"]()
        assert d["p_nom"] == 400.0
        assert d["derating"] == 0.90
        assert d["premio"] == 33000.0
        assert d["disponibilita"] == 0.97
        assert d["energia_up_mwh"] == 15000.0
        assert d["prezzo_up"] == 120.0
        assert d["n_avviamenti"] == 80
        assert d["costo_avviamento"] == 5000.0
        assert d["costo_variabile"] == 60.0
        assert d["opex_om"] == 2000000.0
        assert d["capex"] == 0.0
        assert d["fattore_co2"] == 360.0
        assert d["tasso"] == 0.06
        assert d["vita_anni"] == 15
        assert d["tolleranza"] == 0.10

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("cap_deratata", "ricavi", "costi",
                       "risp", "co2_t", "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 1" in doc
        assert "verdetto = 'CONVIENTE'" in doc


class TestUI:
    def test_header_helpers_presente(self):
        assert '# W675 (24/10/2026) - tab675' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh675_num", "mh675_nneg", "mh675_pos",
                     "mh675_int_pos",
                     "mh675_capacita_deratata",
                     "mh675_ricavi_premio", "mh675_ricavi_en_up",
                     "mh675_costi_avviamenti",
                     "mh675_costi_en_up", "mh675_risparmio",
                     "mh675_co2", "mh675_van", "mh675_tir",
                     "mh675_payback", "mh675_verdetto",
                     "_mh675_neutro", "mh675_calcola",
                     "mh675_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE675) == 1

    def test_blocco_with_tab675(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab675:"

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st675_[a-z0-9_]+)"', _ui_src())
        assert len(keys) >= 16
        assert len(set(keys)) == len(keys)
        # nessuna collisione con le chiavi dei cicli precedenti
        assert not any(k.startswith("st674_") for k in keys)
        assert not any(k.startswith("st673_") for k in keys)
        assert not any(k.startswith("st672_") for k in keys)

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg675" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg675") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg675")
        assert g < src.index("st.bar_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Ricavi totali (€/anno)" in src
        assert "Costi totali (€/anno)" in src
        assert "Risparmio netto (€/anno)" in src
        assert "CO2 extra (t/anno)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd675" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_co2_presente(self):
        src = _ui_src()
        assert "co2_t" in src
        assert "extra CO2 emessa" in src

    def test_grafico_presente(self):
        src = _ui_src()
        assert "st.bar_chart" in src
        assert "Ricavi premio capacità" in src
        assert "Risparmio netto" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert 'sep=";"' in src
        assert "capacity_market_business_case.csv" in src

    def test_sensitivita_presente(self):
        src = _ui_src()
        assert "Sensitiv" in src
        assert "mh675_calcola" in src

    def test_differenziazione_da_feature_esistenti(self):
        src = _ui_src()
        assert "capacit" in src
        assert "tab674" in src
        assert "tab673" in src
        assert "tab672" in src


class TestSegreti:
    def test_nessun_segreto_nei_file(self):
        for fn in ("w675_helpers.py", "w675_ui.py",
                   "w675_test.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            assert not re.search(
                r"(?i)(api[_-]?key|secret|password|passwd|token)"
                r"\s*=\s*[\"']",
                src), fn
