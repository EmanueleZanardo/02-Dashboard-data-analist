"""Test tab676 "📜💹 Trading GO: il market making sui certificati verdi paga?"

Demo calcolata eseguendo demo_calcoli() (non a mano):
trader con 50.000 MWh/anno di GO (1 GO = 1 MWh),
acquisto a 1,80 EUR/MWh e vendita a 2,60 EUR/MWh con
premio tecnologico 1,0; quota invenduta 0,10 ceduta con
haircut 0,5; fee fisse 15.000 EUR/anno e fee variabili
0,02 (2 % dei ricavi); fattore mix residuo 0,35 t
CO2/MWh; CAPEX 0 EUR (nessun impianto); tasso 0,06
(6 %), vita 5 anni, tolleranza 0,10 (10 % del CAPEX).

- ricavi_venduti = 50000.0 x 0.90 x 2.60 x 1.0 = 117000.0 EUR/anno
- ricavi_sconto = 50000.0 x 0.10 x 2.60 x 1.0 x 0.5 = 6500.0 EUR/anno
- ricavi = 123500.0 EUR/anno
- costi = 50000.0 x 1.80 + 15000.0 + 0.02 x 123500.0 = 107470.0 EUR/anno
- risp = 123500.0 - 107470.0 = 16030.0 EUR/anno
- co2_t = 50000.0 x 0.35/1000 = 17.5 t/anno (ATTRIBUITA: i GO non riducono le emissioni fisiche, sono attribuzione contrattuale)
- flussi [-0.0, 16030.0 x 5];
  VAN(0,06) = 67524.19148261844 EUR -> CONVIENTE (VAN >= 0)
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
    if (p / "w676_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w676_helpers.py via AST
    (stesso pattern di tests/appfuncs.py: niente Streamlit)."""
    src = (_new_dir() / "w676_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w676_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w676_helpers.py: {missing}")
    return out


_F = _load("mh676_num", "mh676_nneg", "mh676_pos", "mh676_int_pos",
           "mh676_quota", "mh676_ricavi", "mh676_ricavi_venduti",
           "mh676_ricavi_sconto", "mh676_costi",
           "mh676_risparmio", "mh676_co2_evitata", "mh676_van",
           "mh676_tir", "mh676_payback", "mh676_verdetto",
           "_mh676_neutro", "mh676_calcola", "mh676_demo",
           "demo_calcoli")

TITLE676 = ("📜💹 Trading GO: il market making sui "
            "certificati verdi paga?")

RICAVI_VENDUTI_DEMO = 117000.0
RICAVI_SCONTO_DEMO = 6500.0
RICAVI_DEMO = 123500.0
COSTI_DEMO = 107470.0
RISP_DEMO = 16030.0
CO2_DEMO = 17.5
VAN_DEMO = 67524.19148261844
PAYBACK_DEMO = 1
VITA_DEMO = 5
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w676_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w676_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh676_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh676_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh676_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh676_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh676_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh676_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh676_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh676_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh676_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh676_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh676_int_pos"](5.0, "x") == 5

    def test_quota_rifiuta_oltre_1(self):
        with pytest.raises(ValueError):
            _F["mh676_quota"](1.01, "x")

    def test_quota_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh676_quota"](-0.01, "x")

    def test_quota_accetta_estremi(self):
        assert _F["mh676_quota"](0.0, "x") == 0.0
        assert _F["mh676_quota"](1.0, "x") == 1.0


class TestFisica:
    def test_ricavi_demo(self):
        assert _F["mh676_ricavi"](
            50000.0, 2.60, 1.0, 0.10,
            0.5) == pytest.approx(RICAVI_DEMO, rel=REL)

    def test_ricavi_venduti_demo(self):
        assert _F["mh676_ricavi_venduti"](
            50000.0, 2.60, 1.0,
            0.10) == pytest.approx(RICAVI_VENDUTI_DEMO,
                                   rel=REL)

    def test_ricavi_sconto_demo(self):
        assert _F["mh676_ricavi_sconto"](
            50000.0, 2.60, 1.0, 0.10,
            0.5) == pytest.approx(RICAVI_SCONTO_DEMO,
                                  rel=REL)

    def test_ricavi_somma_componenti(self):
        r = _F["mh676_ricavi"](50000.0, 2.60, 1.0, 0.10, 0.5)
        rv = _F["mh676_ricavi_venduti"](50000.0, 2.60, 1.0,
                                        0.10)
        rs = _F["mh676_ricavi_sconto"](50000.0, 2.60, 1.0,
                                       0.10, 0.5)
        assert r == pytest.approx(rv + rs, rel=REL)

    def test_ricavi_zero_se_prezzo_vendita_zero(self):
        assert _F["mh676_ricavi"](
            50000.0, 0.0, 1.0, 0.10, 0.5) == 0.0

    def test_ricavi_zero_se_premio_zero(self):
        assert _F["mh676_ricavi"](
            50000.0, 2.60, 0.0, 0.10, 0.5) == 0.0

    def test_ricavi_rifiuta_volume_zero(self):
        with pytest.raises(ValueError):
            _F["mh676_ricavi"](0.0, 2.60, 1.0, 0.10, 0.5)

    def test_ricavi_rifiuta_quota_oltre_1(self):
        with pytest.raises(ValueError):
            _F["mh676_ricavi"](50000.0, 2.60, 1.0, 1.01, 0.5)

    def test_ricavi_rifiuta_haircut_negativo(self):
        with pytest.raises(ValueError):
            _F["mh676_ricavi"](50000.0, 2.60, 1.0, 0.10, -0.01)

    def test_ricavi_rifiuta_premio_negativo(self):
        with pytest.raises(ValueError):
            _F["mh676_ricavi"](50000.0, 2.60, -0.1, 0.10,
                               0.5)

    def test_ricavi_venduti_zero_se_unsold_1(self):
        assert _F["mh676_ricavi_venduti"](
            50000.0, 2.60, 1.0, 1.0) == 0.0

    def test_ricavi_sconto_zero_se_unsold_zero(self):
        assert _F["mh676_ricavi_sconto"](
            50000.0, 2.60, 1.0, 0.0, 0.5) == 0.0

    def test_ricavi_sconto_zero_se_haircut_zero(self):
        assert _F["mh676_ricavi_sconto"](
            50000.0, 2.60, 1.0, 0.10, 0.0) == 0.0

    def test_costi_demo(self):
        assert _F["mh676_costi"](
            50000.0, 1.80, 15000.0, 0.02,
            RICAVI_DEMO) == pytest.approx(COSTI_DEMO,
                                          rel=REL)

    def test_costi_rifiuta_prezzo_acquisto_negativo(self):
        with pytest.raises(ValueError):
            _F["mh676_costi"](50000.0, -0.01, 15000.0, 0.02,
                             RICAVI_DEMO)

    def test_costi_rifiuta_fee_fisse_negative(self):
        with pytest.raises(ValueError):
            _F["mh676_costi"](50000.0, 1.80, -1.0, 0.02,
                             RICAVI_DEMO)

    def test_costi_rifiuta_fee_var_oltre_1(self):
        with pytest.raises(ValueError):
            _F["mh676_costi"](50000.0, 1.80, 15000.0, 1.01,
                             RICAVI_DEMO)

    def test_costi_rifiuta_volume_zero(self):
        with pytest.raises(ValueError):
            _F["mh676_costi"](0.0, 1.80, 15000.0, 0.02,
                             RICAVI_DEMO)

    def test_risparmio_demo(self):
        assert _F["mh676_risparmio"](
            RICAVI_DEMO, COSTI_DEMO) == pytest.approx(
            RISP_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh676_risparmio"](100.0, 150.0) == -50.0

    def test_risparmio_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh676_risparmio"](float("nan"), 0.0)

    def test_co2_demo(self):
        assert _F["mh676_co2_evitata"](
            50000.0, 0.35) == pytest.approx(CO2_DEMO,
                                            rel=REL)

    def test_co2_zero_se_fattore_zero(self):
        assert _F["mh676_co2_evitata"](50000.0, 0.0) == 0.0

    def test_co2_rifiuta_volume_zero(self):
        with pytest.raises(ValueError):
            _F["mh676_co2_evitata"](0.0, 0.35)

    def test_co2_rifiuta_fattore_negativo(self):
        with pytest.raises(ValueError):
            _F["mh676_co2_evitata"](50000.0, -0.01)


class TestFinanza:
    def test_van_demo(self):
        assert _F["mh676_van"](
            RISP_DEMO, 0.0, 0.06,
            VITA_DEMO) == pytest.approx(VAN_DEMO, rel=REL)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh676_van"](RISP_DEMO, 0.0, -0.01, 5)

    def test_van_tasso_zero(self):
        assert _F["mh676_van"](
            RISP_DEMO, 50000.0, 0.0, 5) == pytest.approx(
            -50000.0 + RISP_DEMO * 5, rel=1e-12)

    def test_tir_none_se_risp_non_positivo(self):
        assert _F["mh676_tir"](50000.0, 0.0, 5) is None
        assert _F["mh676_tir"](50000.0, -100.0, 5) is None

    def test_tir_none_se_capex_zero_demo(self):
        # CAPEX = 0: nessun cambio di segno -> None
        assert _F["mh676_tir"](
            0.0, RISP_DEMO, VITA_DEMO) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh676_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo(self):
        assert _F["mh676_payback"](
            0.0, RISP_DEMO, VITA_DEMO) == PAYBACK_DEMO

    def test_payback_none_mai(self):
        assert _F["mh676_payback"](50000.0, 1.0, 5) is None

    def test_payback_none_se_risp_non_positivo(self):
        assert _F["mh676_payback"](50000.0, 0.0, 5) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh676_verdetto"](
            VAN_DEMO, 0.0, 0.10,
            RISP_DEMO) == VERDETTO_DEMO

    def test_verdetto_marginale_ad_hoc(self):
        # VAN negativo entro la tolleranza x CAPEX
        assert _F["mh676_verdetto"](
            -0.05 * 1000000.0, 1000000.0, 0.10,
            RISP_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh676_verdetto"](
            -500000.0, 1000000.0, 0.10,
            RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risp_non_positivo(self):
        assert _F["mh676_verdetto"](
            1000.0, 1000000.0, 0.10,
            0.0) == "NON_CALCOLABILE"
        assert _F["mh676_verdetto"](
            1000.0, 1000000.0, 0.10,
            -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_non_negativo_conviente(self):
        assert _F["mh676_verdetto"](
            0.0, 0.0, 0.10, RISP_DEMO) == "CONVIENTE"
        assert _F["mh676_verdetto"](
            1000.0, 0.0, 0.10, RISP_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(self):
        # CAPEX == 0: tolleranza zero, mai MARGINALE
        assert _F["mh676_verdetto"](
            -1.0, 0.0, 0.10, RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh676_verdetto"](100.0, 1000000.0, -0.01,
                                 RISP_DEMO)


class TestGuard:
    def _bc(self, **kw):
        d = _F["mh676_demo"]()
        d.update(kw)
        return _F["mh676_calcola"](**d)

    def test_volume_zero_neutro(self):
        n = self._bc(volume=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["ricavi"] == 0.0
        assert n["risp"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_volume_negativo_neutro(self):
        n = self._bc(volume=-100.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_quota_invenduta_oltre_1_neutro(self):
        n = self._bc(quota_invenduta=1.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_quota_invenduta_negativa_neutro(self):
        n = self._bc(quota_invenduta=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_haircut_oltre_1_neutro(self):
        n = self._bc(haircut=1.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_haircut_negativo_neutro(self):
        n = self._bc(haircut=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzo_acquisto_negativo_neutro(self):
        n = self._bc(prezzo_acquisto=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzo_vendita_negativo_neutro(self):
        n = self._bc(prezzo_vendita=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_fee_fisse_negative_neutro(self):
        n = self._bc(fee_fisse=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_fee_var_oltre_1_neutro(self):
        n = self._bc(fee_var=1.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_premio_tecnologico_negativo_neutro(self):
        n = self._bc(premio_tecnologico=-0.1)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_fattore_mix_negativo_neutro(self):
        n = self._bc(fattore_mix_co2=-0.01)
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
        n = self._bc(prezzo_vendita=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["ricavi"] == 0.0

    def test_bool_neutro(self):
        n = self._bc(volume=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_risp_non_positivo_neutro(self):
        # prezzo di vendita nullo mentre costo di
        # acquisto e fee pesano: lo spread GO non paga
        n = self._bc(prezzo_vendita=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risp"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh676_neutro"]()
        assert list(n["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(n["df_flussi"]) == 0
        assert list(n["df_tabella"].columns) == ["Voce",
                                                 "Valore (EUR/anno)"]
        assert len(n["df_tabella"]) == 0

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh676_neutro"]()
        for chiave in ("ricavi", "ricavi_venduti",
                       "ricavi_sconto", "costi", "risp",
                       "co2_t", "van", "tir", "payback",
                       "verdetto", "df_flussi",
                       "df_tabella"):
            assert chiave in n, chiave

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert list(b["df_tabella"].columns) == ["Voce",
                                                 "Valore (EUR/anno)"]
        assert len(b["df_tabella"]) == 6
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Ricavi GO a prezzo pieno" in voci
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
        assert c["ricavi_venduti"] == pytest.approx(
            RICAVI_VENDUTI_DEMO, rel=REL)
        assert c["ricavi_sconto"] == pytest.approx(
            RICAVI_SCONTO_DEMO, rel=REL)
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
        """mh676_calcola(**mh676_demo()) deve matchare le
        costanti _DEMO entro 1e-9 relativo (mismatch
        vietato), chiave per chiave."""
        d = _F["mh676_demo"]()
        b = _F["mh676_calcola"](**d)
        coppie = [("ricavi_venduti", RICAVI_VENDUTI_DEMO),
                  ("ricavi_sconto", RICAVI_SCONTO_DEMO),
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
        d = _F["mh676_demo"]()
        assert d["volume"] == 50000.0
        assert d["prezzo_acquisto"] == 1.80
        assert d["prezzo_vendita"] == 2.60
        assert d["quota_invenduta"] == 0.10
        assert d["haircut"] == 0.5
        assert d["fee_fisse"] == 15000.0
        assert d["fee_var"] == 0.02
        assert d["premio_tecnologico"] == 1.0
        assert d["fattore_mix_co2"] == 0.35
        assert d["capex"] == 0.0
        assert d["tasso"] == 0.06
        assert d["vita_anni"] == 5
        assert d["tolleranza"] == 0.10

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("ricavi_venduti", "ricavi_sconto",
                       "ricavi", "costi", "risp", "co2_t",
                       "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 1" in doc
        assert "verdetto = 'CONVIENTE'" in doc


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def676["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def676\["([a-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) >= 13, ui_keys
        demo_keys = set(_F["mh676_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestUI:
    def test_header_helpers_presente(self):
        assert '# W676 (24/10/2026) - tab676' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh676_num", "mh676_nneg", "mh676_pos",
                     "mh676_int_pos", "mh676_quota",
                     "mh676_ricavi", "mh676_ricavi_venduti",
                     "mh676_ricavi_sconto", "mh676_costi",
                     "mh676_risparmio", "mh676_co2_evitata",
                     "mh676_van", "mh676_tir",
                     "mh676_payback", "mh676_verdetto",
                     "_mh676_neutro", "mh676_calcola",
                     "mh676_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE676) == 1

    def test_blocco_with_tab676(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab676:"

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st676_[a-z0-9_]+)"', _ui_src())
        assert len(keys) >= 16
        assert len(set(keys)) == len(keys)
        # nessuna collisione con le chiavi dei cicli precedenti
        assert not any(k.startswith("st675_") for k in keys)
        assert not any(k.startswith("st674_") for k in keys)
        assert not any(k.startswith("st673_") for k in keys)

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg676" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg676") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg676")
        assert g < src.index("st.bar_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Ricavi totali (€/anno)" in src
        assert "Costi totali (€/anno)" in src
        assert "Risparmio netto (€/anno)" in src
        assert "CO2 attribuita (t/anno)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd676" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_onesta_co2_presente(self):
        src = _ui_src()
        assert "co2_t" in src
        assert "NON riducono le emissioni fisiche" in src
        assert "attribuzione contrattuale" in src

    def test_nota_go_vs_ppa_presente(self):
        src = _ui_src()
        assert "GO vs PPA" in src
        assert "Power Purchase Agreement" in src

    def test_grafico_presente(self):
        src = _ui_src()
        assert "st.bar_chart" in src
        assert "Ricavi GO a prezzo pieno" in src
        assert "Risparmio netto" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert 'sep=";"' in src
        assert "go_business_case.csv" in src

    def test_sensitivita_presente(self):
        src = _ui_src()
        assert "Sensitiv" in src
        assert "mh676_calcola" in src
        assert "Prezzo vendita" in src
        assert "Volume x" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st676_show_flussi" in src
        assert "st.checkbox" in src

    def test_differenziazione_da_feature_esistenti(self):
        src = _ui_src()
        assert "GO" in src
        assert "tab671" in src
        assert "tab675" in src
        assert "EEX" in src


class TestSegreti:
    def test_nessun_segreto_nei_file(self):
        for fn in ("w676_helpers.py", "w676_ui.py",
                   "w676_test.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            assert not re.search(
                r"(?i)(api[_-]?key|secret|password|passwd|token)"
                r"\s*=\s*[\"']",
                src), fn
