"""Test tab674 "🔌📋 Riserva di sostituzione RR: la riserva lenta di Terna paga?"

Demo calcolata eseguendo demo_calcoli() (non a mano):
20 MW di banda RR a 3,5 EUR/MW/h per 8 ore/giorno, 330
giorni/anno, con disponibilita' effettiva 0,99; energia
attivata a salire 2.000 MWh/anno a 130 EUR/MWh;
120 avviamenti/anno a 400 EUR l'uno; costo variabile
95 EUR/MWh; O&M 40.000 EUR/anno; CAPEX 200.000 EUR
(telemetria/SCADA e adeguamento impianto); fattore
emissivo 0,55 kg CO2/MWh; tasso 0,06 (6 %), vita 10
anni, tolleranza 0,10 (10 % del CAPEX).

- ricavi_banda = 20.0 x 3.5 x 8.0 x 330 x 0.99 = 182952.0 EUR/anno
- ricavi_en_up = 2000.0 x 130.0 = 260000.0 EUR/anno
- ricavi = 442952.0 EUR/anno
- costi_avviamenti = 120 x 400.0 = 48000.0 EUR/anno
- costi_en_up = 2000.0 x 95.0 = 190000.0 EUR/anno
- costi = 48000.0 + 190000.0 + 40000.0 = 278000.0 EUR/anno
- risp = 442952.0 - 278000.0 = 164952.0 EUR/anno
- co2_t = 2000.0 x 0.55/1000 = 1.1 t/anno (extra emessa: l'energia attivata a salire emette CO2 e la banda RR, da sola, non la compensa)
- flussi [-200000.0, 164952.0 x 10];
  VAN(0,06) = 1014061.079304958 EUR -> CONVIENTE (VAN >= 0)
- TIR = 82.2722384104201 % (bisezione su [-0.99, 10])
- payback = 2 (primo anno con cumulato >= 0)
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
    if (p / "w674_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w674_helpers.py via AST
    (stesso pattern di tests/appfuncs.py: niente Streamlit)."""
    src = (_new_dir() / "w674_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w674_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w674_helpers.py: {missing}")
    return out


_F = _load("mh674_num", "mh674_nneg", "mh674_pos", "mh674_int_pos",
           "mh674_ricavi_banda", "mh674_ricavi_en_up",
           "mh674_costi_avviamenti", "mh674_costi_en_up",
           "mh674_risparmio", "mh674_co2", "mh674_van",
           "mh674_tir", "mh674_payback", "mh674_verdetto",
           "_mh674_neutro", "mh674_calcola",
           "mh674_demo", "demo_calcoli")

TITLE674 = ("🔌📋 Riserva di sostituzione RR: la riserva "
            "lenta di Terna paga?")

RICAVI_BANDA_DEMO = 182952.0
RICAVI_UP_DEMO = 260000.0
RICAVI_DEMO = 442952.0
COSTI_AVV_DEMO = 48000.0
COSTI_EN_UP_DEMO = 190000.0
COSTI_DEMO = 278000.0
RISP_DEMO = 164952.0
CO2_DEMO = 1.1
VAN_DEMO = 1014061.079304958
TIR_PCT_DEMO = 82.2722384104201
PAYBACK_DEMO = 2
VITA_DEMO = 10
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w674_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w674_ui.py").read_text(encoding="utf-8")


def _test_src():
    return (_new_dir() / "w674_test.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh674_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh674_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh674_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh674_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh674_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh674_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh674_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh674_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh674_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh674_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh674_int_pos"](10.0, "x") == 10


class TestFisica:
    def test_ricavi_banda_demo(self):
        assert _F["mh674_ricavi_banda"](
            20.0, 3.5, 8.0, 330, 0.99) == pytest.approx(
            RICAVI_BANDA_DEMO, rel=REL)

    def test_ricavi_banda_rifiuta_banda_zero(self):
        with pytest.raises(ValueError):
            _F["mh674_ricavi_banda"](0.0, 3.5, 8.0, 330, 0.99)

    def test_ricavi_banda_rifiuta_banda_negativa(self):
        with pytest.raises(ValueError):
            _F["mh674_ricavi_banda"](-20.0, 3.5, 8.0, 330, 0.99)

    def test_ricavi_banda_rifiuta_ore_oltre_24(self):
        with pytest.raises(ValueError):
            _F["mh674_ricavi_banda"](20.0, 3.5, 24.1, 330, 0.99)

    def test_ricavi_banda_rifiuta_ore_negative(self):
        with pytest.raises(ValueError):
            _F["mh674_ricavi_banda"](20.0, 3.5, -0.1, 330, 0.99)

    def test_ricavi_banda_rifiuta_giorni_oltre_366(self):
        with pytest.raises(ValueError):
            _F["mh674_ricavi_banda"](20.0, 3.5, 8.0, 367, 0.99)

    def test_ricavi_banda_rifiuta_giorni_zero(self):
        with pytest.raises(ValueError):
            _F["mh674_ricavi_banda"](20.0, 3.5, 8.0, 0, 0.99)

    def test_ricavi_banda_rifiuta_disp_oltre_1(self):
        with pytest.raises(ValueError):
            _F["mh674_ricavi_banda"](20.0, 3.5, 8.0, 330, 1.01)

    def test_ricavi_banda_rifiuta_disp_negativa(self):
        with pytest.raises(ValueError):
            _F["mh674_ricavi_banda"](20.0, 3.5, 8.0, 330, -0.01)

    def test_ricavi_banda_rifiuta_prezzo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh674_ricavi_banda"](20.0, -0.01, 8.0, 330, 0.99)

    def test_ricavi_banda_disp_zero_ricavi_zero(self):
        assert _F["mh674_ricavi_banda"](
            20.0, 3.5, 8.0, 330, 0.0) == 0.0

    def test_ricavi_en_up_demo(self):
        assert _F["mh674_ricavi_en_up"](
            2000.0, 130.0) == pytest.approx(RICAVI_UP_DEMO,
                                            rel=REL)

    def test_ricavi_en_up_zero_se_e_up_zero(self):
        assert _F["mh674_ricavi_en_up"](0.0, 130.0) == 0.0

    def test_ricavi_en_up_rifiuta_e_negativa(self):
        with pytest.raises(ValueError):
            _F["mh674_ricavi_en_up"](-1.0, 130.0)

    def test_ricavi_en_up_rifiuta_prezzo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh674_ricavi_en_up"](2000.0, -0.01)

    def test_costi_avviamenti_demo(self):
        assert _F["mh674_costi_avviamenti"](
            120, 400.0) == pytest.approx(COSTI_AVV_DEMO,
                                         rel=REL)

    def test_costi_avviamenti_zero_se_n_avv_zero(self):
        assert _F["mh674_costi_avviamenti"](0, 400.0) == 0.0

    def test_costi_avviamenti_rifiuta_n_negativo(self):
        with pytest.raises(ValueError):
            _F["mh674_costi_avviamenti"](-1, 400.0)

    def test_costi_avviamenti_rifiuta_costo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh674_costi_avviamenti"](120, -0.01)

    def test_costi_en_up_demo(self):
        assert _F["mh674_costi_en_up"](
            2000.0, 95.0) == pytest.approx(COSTI_EN_UP_DEMO,
                                           rel=REL)

    def test_costi_en_up_zero_se_e_up_zero(self):
        assert _F["mh674_costi_en_up"](0.0, 95.0) == 0.0

    def test_costi_en_up_rifiuta_e_negativa(self):
        with pytest.raises(ValueError):
            _F["mh674_costi_en_up"](-1.0, 95.0)

    def test_costi_en_up_rifiuta_costo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh674_costi_en_up"](2000.0, -0.01)

    def test_risparmio_demo(self):
        assert _F["mh674_risparmio"](
            RICAVI_BANDA_DEMO, RICAVI_UP_DEMO,
            COSTI_AVV_DEMO, COSTI_EN_UP_DEMO,
            40000.0) == pytest.approx(RISP_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh674_risparmio"](
            100.0, 50.0, 90.0, 50.0, 20.0) == -10.0

    def test_risparmio_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh674_risparmio"](
                float("nan"), 0.0, 0.0, 0.0, 0.0)

    def test_co2_demo(self):
        assert _F["mh674_co2"](
            2000.0, 0.55) == pytest.approx(CO2_DEMO, rel=REL)

    def test_co2_e_zero_se_energia_zero(self):
        assert _F["mh674_co2"](0.0, 0.55) == 0.0

    def test_co2_rifiuta_fattore_negativo(self):
        with pytest.raises(ValueError):
            _F["mh674_co2"](2000.0, -0.01)


class TestFinanza:
    def test_van_demo(self):
        assert _F["mh674_van"](
            RISP_DEMO, 200000.0, 0.06,
            VITA_DEMO) == pytest.approx(VAN_DEMO, rel=REL)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh674_van"](RISP_DEMO, 200000.0, -0.01, 10)

    def test_van_tasso_zero(self):
        assert _F["mh674_van"](
            RISP_DEMO, 200000.0, 0.0, 10) == pytest.approx(
            -200000.0 + RISP_DEMO * 10, rel=1e-12)

    def test_tir_none_se_risp_non_positivo(self):
        assert _F["mh674_tir"](200000.0, 0.0, 10) is None
        assert _F["mh674_tir"](200000.0, -100.0, 10) is None

    def test_tir_demo(self):
        assert _F["mh674_tir"](
            200000.0, RISP_DEMO, VITA_DEMO) * 100.0 == \
            pytest.approx(TIR_PCT_DEMO, rel=REL)

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh674_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo(self):
        assert _F["mh674_payback"](
            200000.0, RISP_DEMO, VITA_DEMO) == PAYBACK_DEMO

    def test_payback_none_mai(self):
        assert _F["mh674_payback"](100000.0, 1.0, 10) is None

    def test_payback_none_se_risp_non_positivo(self):
        assert _F["mh674_payback"](200000.0, 0.0, 10) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh674_verdetto"](
            VAN_DEMO, 200000.0, 0.10,
            RISP_DEMO) == VERDETTO_DEMO

    def test_verdetto_marginale_ad_hoc(self):
        # VAN negativo entro la tolleranza x CAPEX
        assert _F["mh674_verdetto"](
            -0.05 * 200000.0, 200000.0, 0.10,
            RISP_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh674_verdetto"](
            -50000.0, 200000.0, 0.10,
            RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risp_non_positivo(self):
        assert _F["mh674_verdetto"](
            1000.0, 200000.0, 0.10,
            0.0) == "NON_CALCOLABILE"
        assert _F["mh674_verdetto"](
            1000.0, 200000.0, 0.10,
            -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_non_negativo_conviente(self):
        assert _F["mh674_verdetto"](
            0.0, 0.0, 0.10, RISP_DEMO) == "CONVIENTE"
        assert _F["mh674_verdetto"](
            1000.0, 0.0, 0.10, RISP_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(self):
        # CAPEX == 0: tolleranza zero, mai MARGINALE
        assert _F["mh674_verdetto"](
            -1.0, 0.0, 0.10, RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh674_verdetto"](100.0, 200000.0, -0.01,
                                 RISP_DEMO)


class TestGuard:
    def _bc(self, **kw):
        d = _F["mh674_demo"]()
        d.update(kw)
        return _F["mh674_calcola"](**d)

    def test_banda_zero_neutro(self):
        n = self._bc(banda_mw=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["ricavi"] == 0.0
        assert n["risp"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_banda_negativa_neutro(self):
        n = self._bc(banda_mw=-20.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_ore_oltre_24_neutro(self):
        n = self._bc(ore_giorno=25.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_ore_negative_neutro(self):
        n = self._bc(ore_giorno=-0.1)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_giorni_oltre_366_neutro(self):
        n = self._bc(giorni_anno=367)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_giorni_zero_neutro(self):
        n = self._bc(giorni_anno=0)
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
        n = self._bc(prezzo_banda=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["ricavi"] == 0.0

    def test_bool_neutro(self):
        n = self._bc(banda_mw=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_risp_non_positivo_neutro(self):
        # ricavi banda nulli (disponibilita' zero) mentre
        # avviamenti, costo variabile e O&M pesano: la
        # banda non paga
        n = self._bc(disponibilita=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risp"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh674_neutro"]()
        assert list(n["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(n["df_flussi"]) == 0
        assert list(n["df_tabella"].columns) == ["Voce",
                                                 "Valore (EUR/anno)"]
        assert len(n["df_tabella"]) == 0

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh674_neutro"]()
        for chiave in ("ricavi", "costi", "risp", "co2_t",
                       "van", "tir", "payback", "verdetto",
                       "df_flussi", "df_tabella"):
            assert chiave in n, chiave

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert list(b["df_tabella"].columns) == ["Voce",
                                                 "Valore (EUR/anno)"]
        assert len(b["df_tabella"]) == 6
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Ricavi banda RR" in voci
        assert "Risparmio netto" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(b["df_flussi"]) == VITA_DEMO + 1
        assert b["df_flussi"]["Cumulato (€)"].iloc[-1] == \
            pytest.approx(-200000.0 + RISP_DEMO * VITA_DEMO,
                          rel=REL)


class TestDemo:
    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["ricavi"] == pytest.approx(
            RICAVI_DEMO, rel=REL)
        assert c["costi"] == pytest.approx(
            COSTI_DEMO, rel=REL)
        assert c["risp"] == pytest.approx(RISP_DEMO, rel=REL)
        assert c["co2_t"] == pytest.approx(
            CO2_DEMO, rel=REL)
        assert c["van"] == pytest.approx(VAN_DEMO, rel=REL)
        assert c["tir"] == pytest.approx(TIR_PCT_DEMO, rel=REL)
        assert c["payback"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()[
            "van"] == _F["demo_calcoli"]()["van"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        """mh674_calcola(**mh674_demo()) deve matchare le
        costanti _DEMO entro 1e-9 relativo (mismatch
        vietato), chiave per chiave."""
        d = _F["mh674_demo"]()
        b = _F["mh674_calcola"](**d)
        coppie = [("ricavi", RICAVI_DEMO),
                  ("costi", COSTI_DEMO),
                  ("risp", RISP_DEMO),
                  ("co2_t", CO2_DEMO),
                  ("van", VAN_DEMO),
                  ("tir", TIR_PCT_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh674_demo"]()
        assert d["banda_mw"] == 20.0
        assert d["prezzo_banda"] == 3.5
        assert d["ore_giorno"] == 8.0
        assert d["giorni_anno"] == 330
        assert d["disponibilita"] == 0.99
        assert d["energia_up_mwh"] == 2000.0
        assert d["prezzo_up"] == 130.0
        assert d["n_avviamenti"] == 120
        assert d["costo_avviamento"] == 400.0
        assert d["costo_variabile"] == 95.0
        assert d["opex_om"] == 40000.0
        assert d["capex"] == 200000.0
        assert d["fattore_co2"] == 0.55
        assert d["tasso"] == 0.06
        assert d["vita_anni"] == 10
        assert d["tolleranza"] == 0.10

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("ricavi", "costi", "risp", "co2_t",
                       "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 2" in doc
        assert "verdetto = 'CONVIENTE'" in doc


class TestUI:
    def test_header_helpers_presente(self):
        assert '# W674 (24/10/2026) - tab674' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh674_num", "mh674_nneg", "mh674_pos",
                     "mh674_int_pos", "mh674_ricavi_banda",
                     "mh674_ricavi_en_up",
                     "mh674_costi_avviamenti",
                     "mh674_costi_en_up", "mh674_risparmio",
                     "mh674_co2", "mh674_van", "mh674_tir",
                     "mh674_payback", "mh674_verdetto",
                     "_mh674_neutro", "mh674_calcola",
                     "mh674_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE674) == 1

    def test_blocco_with_tab674(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab674:"

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st674_[a-z0-9_]+)"', _ui_src())
        assert len(keys) >= 16
        assert len(set(keys)) == len(keys)
        # nessuna collisione con le chiavi dei cicli precedenti
        assert not any(k.startswith("st673_") for k in keys)
        assert not any(k.startswith("st672_") for k in keys)
        assert not any(k.startswith("st671_") for k in keys)

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg674" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg674") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg674")
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
        assert "_vd674" in src
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
        assert "Ricavi banda RR" in src
        assert "Risparmio netto" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert 'sep=";"' in src
        assert "rr_banda_business_case.csv" in src

    def test_sensitivita_presente(self):
        src = _ui_src()
        assert "Sensitiv" in src
        assert "mh674_calcola" in src

    def test_differenziazione_da_feature_esistenti(self):
        src = _ui_src()
        assert "RR" in src
        assert "tab673" in src
        assert "tab672" in src


class TestSegreti:
    def test_nessun_segreto_nei_file(self):
        for fn in ("w674_helpers.py", "w674_ui.py",
                   "w674_test.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            assert not re.search(
                r"(?i)(api[_-]?key|secret|password|passwd|token)"
                r"\s*=\s*[\"']",
                src), fn


class TestDemoUiKeysRegression:
    """Regressione 24/10/2026 ciclo ~06:39: la UI usava _def674["om"]
    mentre mh674_demo() definisce "opex_om" -> KeyError a render.
    Ogni chiave letta dal frammento UI deve esistere nel demo dict."""

    def test_ui_keys_subset_di_demo_keys(self):
        ui = _ui_src()
        demo_keys = set(_F["mh674_demo"]().keys())
        used = set(re.findall(r'_def674\["([a-z_0-9]+)"\]', ui))
        assert used, "nessuna chiave _def674 trovata nella UI"
        mancanti = sorted(used - demo_keys)
        assert not mancanti, f"chiavi UI non nel demo dict: {mancanti}"

    def test_om_rinominato_opex_om(self):
        ui = _ui_src()
        assert '_def674["om"]' not in ui
        assert '_def674["opex_om"]' in ui
