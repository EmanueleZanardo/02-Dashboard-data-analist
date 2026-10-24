"""Test tab672 "⚡🔄 Riserva secondaria aFRR: la banda automatica di ripristino frequenza paga?"

Demo calcolata eseguendo demo_calcoli() (non a mano):
5 MW di banda aFRR simmetrica a 8 EUR/MW/h per 20
ore/giorno, 350 giorni/anno, con tasso di disponibilita'
effettiva 0,98; energia attivata a salire 400 MWh/anno a
90 EUR/MWh; energia attivata a scendere 350 MWh/anno a
60 EUR/MWh; spread netto di attivazione 15 EUR/MWh; O&M
20.000 EUR/anno; CAPEX 150.000 EUR (telemetria/
SCADA/controller); fattori emissivi 0,35 kg CO2/MWh a
salire e a scendere; tasso 6 %, vita 10 anni, tolleranza
10 % del CAPEX.

- ricavi_potenza = 5.0 x 8.0 x 20.0 x 350 x 0.98 = 274400.0 EUR/anno
- ricavi_en_up = 400.0 x 90.0 = 36000.0 EUR/anno
- costi_en_down = 350.0 x 60.0 = 21000.0 EUR/anno
- costi_att = (400.0 + 350.0) x 15.0 = 11250.0 EUR/anno
- risp = 274400.0 + 36000.0 - (21000.0 + 11250.0 + 20000.0) = 258150.0 EUR/anno
- co2_netta = (400.0 x 0.35 - 350.0 x 0.35)/1000 = 0.017500000000000016 t/anno (extra emessa: l'energia attivata a salire emette CO2 e la banda aFRR, da sola, non la compensa)
- flussi [-150000.0, 258150.0 x 10];
  VAN(6 %) = 1750006.4723227054 EUR -> CONVIENTE (VAN >= 0)
- TIR = 172.09226217408468 % (bisezione su [-0.99, 10])
- payback = 1 (primo anno con cumulato >= 0)
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
    if (p / "w672_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w672_helpers.py via AST
    (stesso pattern di tests/appfuncs.py: niente Streamlit)."""
    src = (_new_dir() / "w672_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w672_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w672_helpers.py: {missing}")
    return out


_F = _load("mh672_num", "mh672_nneg", "mh672_pos", "mh672_int_pos",
           "mh672_ricavi_potenza", "mh672_ricavi_en_up",
           "mh672_costi_en_down", "mh672_costi_attivazione",
           "mh672_risparmio", "mh672_co2", "mh672_van",
           "mh672_tir", "mh672_payback", "mh672_verdetto",
           "_mh672_neutro", "mh672_calcola",
           "mh672_demo", "demo_calcoli")

TITLE672 = ("⚡🔄 Riserva secondaria aFRR: la banda automatica "
            "di ripristino frequenza paga?")

RICAVI_POT_DEMO = 274400.0
RICAVI_UP_DEMO = 36000.0
COSTI_DOWN_DEMO = 21000.0
COSTI_ATT_DEMO = 11250.0
RISP_DEMO = 258150.0
CO2_NETTA_DEMO = 0.017500000000000016
VAN_DEMO = 1750006.4723227054
TIR_PCT_DEMO = 172.09226217408468
PAYBACK_DEMO = 1
VITA_DEMO = 10
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w672_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w672_ui.py").read_text(encoding="utf-8")


def _test_src():
    return (_new_dir() / "w672_test.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh672_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh672_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh672_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh672_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh672_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh672_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh672_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh672_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh672_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh672_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh672_int_pos"](10.0, "x") == 10


class TestFisica:
    def test_ricavi_potenza_demo(self):
        assert _F["mh672_ricavi_potenza"](
            5.0, 8.0, 20.0, 350, 0.98) == pytest.approx(
            RICAVI_POT_DEMO, rel=REL)

    def test_ricavi_potenza_rifiuta_banda_zero(self):
        with pytest.raises(ValueError):
            _F["mh672_ricavi_potenza"](0.0, 8.0, 20.0, 350, 0.98)

    def test_ricavi_potenza_rifiuta_banda_negativa(self):
        with pytest.raises(ValueError):
            _F["mh672_ricavi_potenza"](-5.0, 8.0, 20.0, 350, 0.98)

    def test_ricavi_potenza_rifiuta_ore_oltre_24(self):
        with pytest.raises(ValueError):
            _F["mh672_ricavi_potenza"](5.0, 8.0, 24.1, 350, 0.98)

    def test_ricavi_potenza_rifiuta_ore_negative(self):
        with pytest.raises(ValueError):
            _F["mh672_ricavi_potenza"](5.0, 8.0, -0.1, 350, 0.98)

    def test_ricavi_potenza_rifiuta_giorni_oltre_366(self):
        with pytest.raises(ValueError):
            _F["mh672_ricavi_potenza"](5.0, 8.0, 20.0, 367, 0.98)

    def test_ricavi_potenza_rifiuta_giorni_zero(self):
        with pytest.raises(ValueError):
            _F["mh672_ricavi_potenza"](5.0, 8.0, 20.0, 0, 0.98)

    def test_ricavi_potenza_rifiuta_disp_oltre_1(self):
        with pytest.raises(ValueError):
            _F["mh672_ricavi_potenza"](5.0, 8.0, 20.0, 350, 1.01)

    def test_ricavi_potenza_rifiuta_disp_negativa(self):
        with pytest.raises(ValueError):
            _F["mh672_ricavi_potenza"](5.0, 8.0, 20.0, 350, -0.01)

    def test_ricavi_potenza_rifiuta_prezzo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh672_ricavi_potenza"](5.0, -0.01, 20.0, 350, 0.98)

    def test_ricavi_potenza_disp_zero_ricavi_zero(self):
        assert _F["mh672_ricavi_potenza"](
            5.0, 8.0, 20.0, 350, 0.0) == 0.0

    def test_ricavi_en_up_demo(self):
        assert _F["mh672_ricavi_en_up"](
            400.0, 90.0) == pytest.approx(RICAVI_UP_DEMO,
                                           rel=REL)

    def test_ricavi_en_up_zero_se_e_up_zero(self):
        assert _F["mh672_ricavi_en_up"](0.0, 90.0) == 0.0

    def test_ricavi_en_up_rifiuta_e_negativa(self):
        with pytest.raises(ValueError):
            _F["mh672_ricavi_en_up"](-1.0, 90.0)

    def test_ricavi_en_up_rifiuta_prezzo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh672_ricavi_en_up"](400.0, -0.01)

    def test_costi_en_down_demo(self):
        assert _F["mh672_costi_en_down"](
            350.0, 60.0) == pytest.approx(COSTI_DOWN_DEMO,
                                           rel=REL)

    def test_costi_en_down_zero_se_e_down_zero(self):
        assert _F["mh672_costi_en_down"](0.0, 60.0) == 0.0

    def test_costi_en_down_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh672_costi_en_down"](-1.0, 60.0)

    def test_costi_en_down_rifiuta_prezzo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh672_costi_en_down"](350.0, -0.01)

    def test_costi_attivazione_demo(self):
        assert _F["mh672_costi_attivazione"](
            400.0, 350.0, 15.0) == pytest.approx(
            COSTI_ATT_DEMO, rel=REL)

    def test_costi_attivazione_zero_se_energie_zero(self):
        assert _F["mh672_costi_attivazione"](
            0.0, 0.0, 15.0) == 0.0

    def test_costi_attivazione_rifiuta_energia_negativa(self):
        with pytest.raises(ValueError):
            _F["mh672_costi_attivazione"](-1.0, 350.0, 15.0)
        with pytest.raises(ValueError):
            _F["mh672_costi_attivazione"](400.0, -1.0, 15.0)

    def test_costi_attivazione_rifiuta_spread_negativo(self):
        with pytest.raises(ValueError):
            _F["mh672_costi_attivazione"](400.0, 350.0, -1.0)

    def test_risparmio_demo(self):
        assert _F["mh672_risparmio"](
            RICAVI_POT_DEMO, RICAVI_UP_DEMO, COSTI_DOWN_DEMO,
            COSTI_ATT_DEMO, 20000.0) == pytest.approx(
            RISP_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh672_risparmio"](
            100.0, 50.0, 90.0, 50.0, 20.0) == -10.0

    def test_risparmio_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh672_risparmio"](
                float("nan"), 0.0, 0.0, 0.0, 0.0)

    def test_co2_demo(self):
        assert _F["mh672_co2"](
            400.0, 0.35, 350.0, 0.35) == pytest.approx(
            CO2_NETTA_DEMO, rel=REL)

    def test_co2_e_zero_se_energie_zero(self):
        assert _F["mh672_co2"](0.0, 0.35, 0.0, 0.35) == 0.0

    def test_co2_negativa_se_down_domina(self):
        assert _F["mh672_co2"](100.0, 0.35, 400.0, 0.35) < 0.0

    def test_co2_rifiuta_fattore_negativo(self):
        with pytest.raises(ValueError):
            _F["mh672_co2"](400.0, -0.01, 350.0, 0.35)


class TestFinanza:
    def test_van_demo(self):
        assert _F["mh672_van"](
            RISP_DEMO, 150000.0, 6.0,
            VITA_DEMO) == pytest.approx(VAN_DEMO, rel=REL)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh672_van"](RISP_DEMO, 150000.0, -0.01, 10)

    def test_van_tasso_zero(self):
        assert _F["mh672_van"](
            RISP_DEMO, 150000.0, 0.0, 10) == pytest.approx(
            -150000.0 + RISP_DEMO * 10, rel=1e-12)

    def test_tir_none_se_risp_non_positivo(self):
        assert _F["mh672_tir"](150000.0, 0.0, 10) is None
        assert _F["mh672_tir"](150000.0, -100.0, 10) is None

    def test_tir_demo(self):
        assert _F["mh672_tir"](
            150000.0, RISP_DEMO, VITA_DEMO) * 100.0 == \
            pytest.approx(TIR_PCT_DEMO, rel=REL)

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh672_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo(self):
        assert _F["mh672_payback"](
            150000.0, RISP_DEMO, VITA_DEMO) == PAYBACK_DEMO

    def test_payback_none_mai(self):
        assert _F["mh672_payback"](100000.0, 1.0, 10) is None

    def test_payback_none_se_risp_non_positivo(self):
        assert _F["mh672_payback"](150000.0, 0.0, 10) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh672_verdetto"](
            VAN_DEMO, 150000.0, 10.0,
            RISP_DEMO) == VERDETTO_DEMO

    def test_verdetto_marginale_ad_hoc(self):
        # VAN negativo entro il 10 % del CAPEX
        assert _F["mh672_verdetto"](
            -0.05 * 150000.0, 150000.0, 10.0,
            RISP_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh672_verdetto"](
            -50000.0, 150000.0, 10.0,
            RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risp_non_positivo(self):
        assert _F["mh672_verdetto"](
            1000.0, 150000.0, 10.0,
            0.0) == "NON_CALCOLABILE"
        assert _F["mh672_verdetto"](
            1000.0, 150000.0, 10.0,
            -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_non_negativo_conviente(self):
        assert _F["mh672_verdetto"](
            0.0, 0.0, 10.0, RISP_DEMO) == "CONVIENTE"
        assert _F["mh672_verdetto"](
            1000.0, 0.0, 10.0, RISP_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(self):
        # CAPEX == 0: tolleranza zero, mai MARGINALE
        assert _F["mh672_verdetto"](
            -1.0, 0.0, 10.0, RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh672_verdetto"](100.0, 150000.0, -1.0,
                                 RISP_DEMO)


class TestGuard:
    def _bc(self, **kw):
        d = _F["mh672_demo"]()
        d.update(kw)
        return _F["mh672_calcola"](**d)

    def test_banda_zero_neutro(self):
        n = self._bc(p_banda=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["ricavi_potenza"] == 0.0
        assert n["risp"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_banda_negativa_neutro(self):
        n = self._bc(p_banda=-5.0)
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
        n = self._bc(disp_frac=1.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_e_up_negativo_neutro(self):
        n = self._bc(e_up=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_e_down_negativo_neutro(self):
        n = self._bc(e_down=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_p_up_negativo_neutro(self):
        n = self._bc(p_up=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_p_down_negativo_neutro(self):
        n = self._bc(p_down=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_spread_negativo_neutro(self):
        n = self._bc(spread_att=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_om_negativo_neutro(self):
        n = self._bc(om=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_zero_neutro(self):
        n = self._bc(vita=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tasso_negativo_neutro(self):
        n = self._bc(r_pct=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(prezzo_pot=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["ricavi_potenza"] == 0.0

    def test_bool_neutro(self):
        n = self._bc(p_banda=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_risp_non_positivo_neutro(self):
        # ricavi potenza nulli (disponibilita' zero) mentre
        # energia a scendere, attivazione e O&M pesano: la
        # banda non paga
        n = self._bc(disp_frac=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risp"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh672_neutro"]()
        assert list(n["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(n["df_flussi"]) == 0
        assert list(n["df_tabella"].columns) == ["Voce",
                                                "Valore (EUR/anno)"]
        assert len(n["df_tabella"]) == 0

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh672_neutro"]()
        for chiave in ("ricavi_potenza", "ricavi_en_up",
                       "costi_en_down", "costi_att", "risp",
                       "co2_netta", "van", "tir", "payback",
                       "verdetto", "df_flussi", "df_tabella"):
            assert chiave in n, chiave

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert list(b["df_tabella"].columns) == ["Voce",
                                                 "Valore (EUR/anno)"]
        assert len(b["df_tabella"]) == 6
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Ricavi potenza aFRR" in voci
        assert "Risparmio netto" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(b["df_flussi"]) == VITA_DEMO + 1
        assert b["df_flussi"]["Cumulato (€)"].iloc[-1] == \
            pytest.approx(-150000.0 + RISP_DEMO * VITA_DEMO,
                          rel=REL)


class TestDemo:
    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["ricavi_potenza"] == pytest.approx(
            RICAVI_POT_DEMO, rel=REL)
        assert c["ricavi_en_up"] == pytest.approx(
            RICAVI_UP_DEMO, rel=REL)
        assert c["costi_en_down"] == pytest.approx(
            COSTI_DOWN_DEMO, rel=REL)
        assert c["costi_att"] == pytest.approx(
            COSTI_ATT_DEMO, rel=REL)
        assert c["risp"] == pytest.approx(RISP_DEMO, rel=REL)
        assert c["co2_netta"] == pytest.approx(
            CO2_NETTA_DEMO, rel=REL)
        assert c["van"] == pytest.approx(VAN_DEMO, rel=REL)
        assert c["tir"] == pytest.approx(TIR_PCT_DEMO, rel=REL)
        assert c["payback"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()[
            "van"] == _F["demo_calcoli"]()["van"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        """mh672_calcola(**mh672_demo()) deve matchare le
        costanti _DEMO entro 1e-9 relativo (mismatch
        vietato), chiave per chiave."""
        d = _F["mh672_demo"]()
        b = _F["mh672_calcola"](**d)
        coppie = [("ricavi_potenza", RICAVI_POT_DEMO),
                  ("ricavi_en_up", RICAVI_UP_DEMO),
                  ("costi_en_down", COSTI_DOWN_DEMO),
                  ("costi_att", COSTI_ATT_DEMO),
                  ("risp", RISP_DEMO),
                  ("co2_netta", CO2_NETTA_DEMO),
                  ("van", VAN_DEMO),
                  ("tir", TIR_PCT_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh672_demo"]()
        assert d["p_banda"] == 5.0
        assert d["prezzo_pot"] == 8.0
        assert d["ore_giorno"] == 20.0
        assert d["giorni_anno"] == 350
        assert d["disp_frac"] == 0.98
        assert d["e_up"] == 400.0
        assert d["p_up"] == 90.0
        assert d["e_down"] == 350.0
        assert d["p_down"] == 60.0
        assert d["spread_att"] == 15.0
        assert d["om"] == 20000.0
        assert d["capex"] == 150000.0
        assert d["f_co2_up"] == 0.35
        assert d["f_co2_down"] == 0.35
        assert d["r_pct"] == 6.0
        assert d["vita"] == 10
        assert d["toll_pct"] == 10.0

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("ricavi_potenza", "ricavi_en_up",
                       "costi_en_down", "costi_att", "risp",
                       "co2_netta", "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 1" in doc
        assert "verdetto = 'CONVIENTE'" in doc


class TestUI:
    def test_header_helpers_presente(self):
        assert '# W672 (24/10/2026) - tab672' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh672_num", "mh672_nneg", "mh672_pos",
                     "mh672_int_pos", "mh672_ricavi_potenza",
                     "mh672_ricavi_en_up", "mh672_costi_en_down",
                     "mh672_costi_attivazione",
                     "mh672_risparmio", "mh672_co2",
                     "mh672_van", "mh672_tir", "mh672_payback",
                     "mh672_verdetto", "_mh672_neutro",
                     "mh672_calcola", "mh672_demo",
                     "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE672) == 1

    def test_blocco_with_tab672(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab672:"

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st672_[a-z0-9_]+)"', _ui_src())
        assert len(keys) >= 16
        assert len(set(keys)) == len(keys)
        # nessuna collisione con le chiavi dei cicli precedenti
        assert not any(k.startswith("st671_") for k in keys)
        assert not any(k.startswith("st670_") for k in keys)

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg672" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg672") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg672")
        assert g < src.index("st.bar_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Ricavi totali (€/anno)" in src
        assert "Costi totali (€/anno)" in src
        assert "Risparmio netto (€/anno)" in src
        assert "VAN (k€)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd672" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_co2_presente(self):
        src = _ui_src()
        assert "co2_netta" in src
        assert "extra CO2 emessa" in src

    def test_grafico_presente(self):
        src = _ui_src()
        assert "st.bar_chart" in src
        assert "Ricavi potenza aFRR" in src
        assert "Risparmio netto" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert 'sep=";"' in src
        assert "afrr_banda_business_case.csv" in src

    def test_sensitivita_presente(self):
        src = _ui_src()
        assert "Sensitiv" in src
        assert "mh672_calcola" in src

    def test_differenziazione_da_feature_esistenti(self):
        src = _ui_src()
        assert "aFRR" in src
        assert "tab663" in src
        assert "tab671" in src


class TestSegreti:
    def test_nessun_segreto_nei_file(self):
        for fn in ("w672_helpers.py", "w672_ui.py",
                   "w672_test.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            assert not re.search(
                r"(?i)(api[_-]?key|secret|password|passwd|token)"
                r"\s*=\s*[\"']",
                src), fn
