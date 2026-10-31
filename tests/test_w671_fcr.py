"""Test tab671 "⚡📡 Riserva primaria FCR: vendere banda di regolazione di frequenza paga?"

Demo calcolata eseguendo mh671_demo_calcoli() (non a mano):
5 MW di banda FCR offerti a 12 EUR/MW/h per 20
ore/giorno, 350 giorni/anno, con tasso di disponibilita'
effettiva 0,98; energia attivata stimata 260 MWh/anno a
spread netto 25 EUR/MWh; O&M 18.000 EUR/anno; CAPEX
120.000 EUR (telemetria/SCADA/controller); fattore
emissivo attivazione 0,35 kg CO2/MWh; tasso 6 %, vita
10 anni, tolleranza 10 % del CAPEX.

- ricavi = 5.0 x 12.0 x 20.0 x 350 x 0.98 = 411600.0 EUR/anno
- costi_att = 260.0 x 25.0 = 6500.0 EUR/anno
- risp = 411600.0 - (6500.0 + 18000.0) = 387100.0 EUR/anno
- CO2 evitata = -260.0 x 0.35/1000 = -0.091 t/anno (extra emessa: l'energia attivata emette CO2 e la banda FCR, da sola, non la compensa)
- flussi [-120000.0, 387100.0 x 10];
  VAN(6 %) = 2729089.6976026315 EUR -> CONVIENTE (VAN >= 0)
- TIR = 322.58315570179985 % (bisezione su [-0.99, 10])
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
    if (p / "w671_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w671_helpers.py via AST
    (stesso pattern di tests/appfuncs.py: niente Streamlit)."""
    src = (_new_dir() / "w671_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w671_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w671_helpers.py: {missing}")
    return out


_F = _load("mh671_num", "mh671_nneg", "mh671_pos", "mh671_int_pos",
           "mh671_ricavi", "mh671_costi_attivazione",
           "mh671_risparmio", "mh671_co2", "mh671_van",
           "mh671_tir", "mh671_payback", "mh671_verdetto",
           "_mh671_neutro", "mh671_business_case",
           "mh671_demo", "mh671_demo_calcoli")

TITLE671 = ("⚡📡 Riserva primaria FCR: vendere banda di "
            "regolazione di frequenza paga?")

RICAVI_DEMO = 411600.0
C_ATT_DEMO = 6500.0
RISP_DEMO = 387100.0
CO2_EVITATA_DEMO = -0.091
VAN_DEMO = 2729089.6976026315
TIR_PCT_DEMO = 322.58315570179985
PAYBACK_DEMO = 1
VITA_DEMO = 10
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w671_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w671_ui.py").read_text(encoding="utf-8")


def _app_src():
    return (Path.home() / "workspace/repo-dashboard/"
            "Dashboard-data-analist/app.py").read_text(
                encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh671_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh671_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh671_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh671_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh671_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh671_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh671_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh671_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh671_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh671_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh671_int_pos"](10.0, "x") == 10


class TestFisica:
    def test_ricavi_demo(self):
        assert _F["mh671_ricavi"](
            5.0, 12.0, 20.0, 350, 0.98) == pytest.approx(
            RICAVI_DEMO, rel=REL)

    def test_ricavi_rifiuta_banda_zero(self):
        with pytest.raises(ValueError):
            _F["mh671_ricavi"](0.0, 12.0, 20.0, 350, 0.98)

    def test_ricavi_rifiuta_banda_negativa(self):
        with pytest.raises(ValueError):
            _F["mh671_ricavi"](-5.0, 12.0, 20.0, 350, 0.98)

    def test_ricavi_rifiuta_ore_oltre_24(self):
        with pytest.raises(ValueError):
            _F["mh671_ricavi"](5.0, 12.0, 24.1, 350, 0.98)

    def test_ricavi_rifiuta_ore_negative(self):
        with pytest.raises(ValueError):
            _F["mh671_ricavi"](5.0, 12.0, -0.1, 350, 0.98)

    def test_ricavi_rifiuta_giorni_oltre_366(self):
        with pytest.raises(ValueError):
            _F["mh671_ricavi"](5.0, 12.0, 20.0, 367, 0.98)

    def test_ricavi_rifiuta_giorni_zero(self):
        with pytest.raises(ValueError):
            _F["mh671_ricavi"](5.0, 12.0, 20.0, 0, 0.98)

    def test_ricavi_rifiuta_disp_oltre_1(self):
        with pytest.raises(ValueError):
            _F["mh671_ricavi"](5.0, 12.0, 20.0, 350, 1.01)

    def test_ricavi_rifiuta_disp_negativa(self):
        with pytest.raises(ValueError):
            _F["mh671_ricavi"](5.0, 12.0, 20.0, 350, -0.01)

    def test_ricavi_rifiuta_prezzo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh671_ricavi"](5.0, -0.01, 20.0, 350, 0.98)

    def test_ricavi_disp_zero_ricavi_zero(self):
        assert _F["mh671_ricavi"](
            5.0, 12.0, 20.0, 350, 0.0) == 0.0

    def test_costi_attivazione_demo(self):
        assert _F["mh671_costi_attivazione"](
            260.0, 25.0) == pytest.approx(C_ATT_DEMO,
                                          rel=REL)

    def test_costi_attivazione_zero_se_e_zero(self):
        assert _F["mh671_costi_attivazione"](0.0, 25.0) == 0.0

    def test_costi_attivazione_rifiuta_e_negativa(self):
        with pytest.raises(ValueError):
            _F["mh671_costi_attivazione"](-1.0, 25.0)

    def test_costi_attivazione_rifiuta_spread_negativo(self):
        with pytest.raises(ValueError):
            _F["mh671_costi_attivazione"](260.0, -1.0)

    def test_risparmio_demo(self):
        assert _F["mh671_risparmio"](
            RICAVI_DEMO, C_ATT_DEMO, 18000.0) == \
            pytest.approx(RISP_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh671_risparmio"](100.0, 90.0, 20.0) == -10.0

    def test_risparmio_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh671_risparmio"](float("nan"), 0.0, 0.0)

    def test_co2_demo(self):
        assert _F["mh671_co2"](
            260.0, 0.35) == pytest.approx(CO2_EVITATA_DEMO,
                                          rel=REL)

    def test_co2_e_zero_se_e_zero(self):
        assert _F["mh671_co2"](0.0, 0.35) == 0.0

    def test_co2_rifiuta_fattore_negativo(self):
        with pytest.raises(ValueError):
            _F["mh671_co2"](260.0, -0.01)


class TestFinanza:
    def test_van_demo(self):
        assert _F["mh671_van"](
            RISP_DEMO, 120000.0, 6.0,
            VITA_DEMO) == pytest.approx(VAN_DEMO, rel=REL)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh671_van"](RISP_DEMO, 120000.0, -0.01, 10)

    def test_van_tasso_zero(self):
        assert _F["mh671_van"](
            RISP_DEMO, 120000.0, 0.0, 10) == pytest.approx(
            -120000.0 + RISP_DEMO * 10, rel=1e-12)

    def test_tir_none_se_risp_non_positivo(self):
        assert _F["mh671_tir"](120000.0, 0.0, 10) is None
        assert _F["mh671_tir"](120000.0, -100.0, 10) is None

    def test_tir_demo(self):
        assert _F["mh671_tir"](
            120000.0, RISP_DEMO, VITA_DEMO) * 100.0 == \
            pytest.approx(TIR_PCT_DEMO, rel=REL)

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh671_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo(self):
        assert _F["mh671_payback"](
            120000.0, RISP_DEMO, VITA_DEMO) == PAYBACK_DEMO

    def test_payback_none_mai(self):
        assert _F["mh671_payback"](100000.0, 1.0, 10) is None

    def test_payback_none_se_risp_non_positivo(self):
        assert _F["mh671_payback"](120000.0, 0.0, 10) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh671_verdetto"](
            VAN_DEMO, 120000.0, 10.0,
            RISP_DEMO) == VERDETTO_DEMO

    def test_verdetto_marginale_ad_hoc(self):
        # VAN negativo entro il 10 % del CAPEX
        assert _F["mh671_verdetto"](
            -0.05 * 120000.0, 120000.0, 10.0,
            RISP_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh671_verdetto"](
            -50000.0, 120000.0, 10.0,
            RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risp_non_positivo(self):
        assert _F["mh671_verdetto"](
            1000.0, 120000.0, 10.0,
            0.0) == "NON_CALCOLABILE"
        assert _F["mh671_verdetto"](
            1000.0, 120000.0, 10.0,
            -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_non_negativo_conviente(self):
        assert _F["mh671_verdetto"](
            0.0, 0.0, 10.0, RISP_DEMO) == "CONVIENTE"
        assert _F["mh671_verdetto"](
            1000.0, 0.0, 10.0, RISP_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(self):
        # CAPEX == 0: tolleranza zero, mai MARGINALE
        assert _F["mh671_verdetto"](
            -1.0, 0.0, 10.0, RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh671_verdetto"](100.0, 120000.0, -1.0,
                                 RISP_DEMO)


class TestGuard:
    def _bc(self, **kw):
        d = _F["mh671_demo"]()
        d.update(kw)
        return _F["mh671_business_case"](**d)

    def test_banda_zero_neutro(self):
        n = self._bc(p_banda=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["ricavi_eur"] == 0.0
        assert n["risp_eur"] == 0.0
        assert n["tir_pct"] is None
        assert n["payback_anni"] is None

    def test_banda_negativa_neutro(self):
        n = self._bc(p_banda=-5.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_ore_oltre_24_neutro(self):
        n = self._bc(ore_giorno=25.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_giorni_oltre_366_neutro(self):
        n = self._bc(giorni_anno=367)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_disp_oltre_1_neutro(self):
        n = self._bc(disp_frac=1.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_e_attivata_negativa_neutro(self):
        n = self._bc(e_attivata=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_spread_negativo_neutro(self):
        n = self._bc(spread_att=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_om_negativo_neutro(self):
        n = self._bc(om=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_zero_neutro(self):
        n = self._bc(n=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tasso_negativo_neutro(self):
        n = self._bc(r_pct=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(prezzo=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["ricavi_eur"] == 0.0

    def test_bool_neutro(self):
        n = self._bc(p_banda=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_risp_non_positivo_neutro(self):
        # ricavi quasi zero (disponibilita' nulla) ma O&M
        # positivi: la banda non paga
        n = self._bc(disp_frac=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risp_eur"] == 0.0
        assert n["tir_pct"] is None
        assert n["payback_anni"] is None

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh671_neutro"]()
        assert list(n["df_voci"].columns) == ["Voce",
                                             "Valore (EUR/anno)"]
        assert len(n["df_voci"]) == 0

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh671_neutro"]()
        for chiave in ("ricavi_eur", "costi_att_eur", "om",
                       "risp_eur", "co2_evitata", "van_eur",
                       "tir_pct", "payback_anni", "verdetto",
                       "df_voci"):
            assert chiave in n, chiave

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert list(b["df_voci"].columns) == ["Voce",
                                             "Valore (EUR/anno)"]
        assert len(b["df_voci"]) == 4
        voci = b["df_voci"]["Voce"].tolist()
        assert "Ricavi banda FCR" in voci
        assert "Risparmio netto" in voci


class TestDemo:
    def test_demo_calcoli_end_to_end(self):
        c = _F["mh671_demo_calcoli"]()
        assert c["ricavi_eur"] == pytest.approx(RICAVI_DEMO,
                                                rel=REL)
        assert c["costi_att_eur"] == pytest.approx(
            C_ATT_DEMO, rel=REL)
        assert c["om"] == 18000.0
        assert c["risp_eur"] == pytest.approx(RISP_DEMO,
                                              rel=REL)
        assert c["co2_evitata"] == pytest.approx(
            CO2_EVITATA_DEMO, rel=REL)
        assert c["van_eur"] == pytest.approx(VAN_DEMO, rel=REL)
        assert c["tir_pct"] == pytest.approx(TIR_PCT_DEMO,
                                             rel=REL)
        assert c["payback_anni"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO

    def test_demo_calcoli_deterministico(self):
        assert _F["mh671_demo_calcoli"]()[
            "van_eur"] == _F["mh671_demo_calcoli"]()["van_eur"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        """business_case(**demo()) deve matchare le costanti
        _DEMO entro 1e-9 relativo (mismatch vietato)."""
        d = _F["mh671_demo"]()
        b = _F["mh671_business_case"](**d)
        coppie = [("ricavi_eur", RICAVI_DEMO),
                  ("costi_att_eur", C_ATT_DEMO),
                  ("risp_eur", RISP_DEMO),
                  ("co2_evitata", CO2_EVITATA_DEMO),
                  ("van_eur", VAN_DEMO),
                  ("tir_pct", TIR_PCT_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert b["payback_anni"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh671_demo"]()
        assert d["p_banda"] == 5.0
        assert d["prezzo"] == 12.0
        assert d["ore_giorno"] == 20.0
        assert d["giorni_anno"] == 350
        assert d["disp_frac"] == 0.98
        assert d["e_attivata"] == 260.0
        assert d["spread_att"] == 25.0
        assert d["om"] == 18000.0
        assert d["capex"] == 120000.0
        assert d["f_co2"] == 0.35
        assert d["r_pct"] == 6.0
        assert d["n"] == 10
        assert d["tol_pct"] == 10.0

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        mh671_demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["mh671_demo_calcoli"]()
        doc = __doc__
        for chiave in ("ricavi_eur", "costi_att_eur",
                       "risp_eur", "co2_evitata", "van_eur",
                       "tir_pct"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback_anni = 1" in doc
        assert "verdetto = 'CONVIENTE'" in doc


class TestUI:
    def test_header_helpers_presente(self):
        assert '# W671 (23/10/2026) - tab671' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh671_num", "mh671_nneg", "mh671_pos",
                     "mh671_int_pos", "mh671_ricavi",
                     "mh671_costi_attivazione",
                     "mh671_risparmio", "mh671_co2",
                     "mh671_van", "mh671_tir", "mh671_payback",
                     "mh671_verdetto", "_mh671_neutro",
                     "mh671_business_case", "mh671_demo",
                     "mh671_demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE671) == 1

    def test_blocco_with_tab671(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab671:"

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st671_[a-z0-9_]+)"', _ui_src())
        assert len(keys) >= 16
        assert len(set(keys)) == len(keys)
        # nessuna collisione con le chiavi dei cicli precedenti
        assert not any(k.startswith("st670_") for k in keys)
        assert not any(k.startswith("st669_") for k in keys)

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
        assert "Ricavi banda (€/anno)" in src
        assert "Costo attivazione (€/anno)" in src
        assert "Risparmio netto (€/anno)" in src
        assert "VAN (k€)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd671" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_co2_presente(self):
        src = _ui_src()
        assert "CO2 evitata" in src
        assert "extra CO2 emessa" in src

    def test_grafico_presente(self):
        src = _ui_src()
        assert "plotly.graph_objects" in src
        assert "Ricavi banda FCR" in src
        assert "Risparmio netto" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert 'sep=";"' in src
        assert "fcr_banda_business_case.csv" in src

    def test_sensitivita_presente(self):
        src = _ui_src()
        assert "Sensitiv" in src
        assert "mh671_business_case" in src

    def test_differenziazione_da_feature_esistenti(self):
        src = _ui_src()
        assert "FCR" in src
        assert "tab663" in src

    def test_nessun_segreto_nella_sezione(self):
        assert not re.search(r'(?i)(api_key|secret|password)\s*=\s*["\']',
                             _ui_src())


class TestRegistry:
    """Verifiche sull'app.py applicato: falliscono finche' la
    tab671 non e' applicata (atteso in fase di authoring)."""

    def test_numero_tab_671(self):
        src = _app_src()
        assert len(re.findall(r"\n    with tab\d+:", src)) == 833

    def test_bump_catena_solo_append(self):
        src = _app_src()
        assert ", tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706, tab707, tab708, tab709, tab710, tab711, tab712, tab713, tab714, tab715, tab716, tab717, tab718, tab719, tab720, tab721, tab722, tab723, tab724, tab725, tab726, tab727, tab728, tab729, tab730, tab731, tab732, tab733, tab734, tab735, tab736, tab737, tab738, tab739, tab740, tab741, tab742, tab743, tab744, tab745, tab746, tab747, tab748, tab749, tab750, tab751, tab752, tab753, tab754, tab755, tab756, tab757, tab758, tab759, tab760, tab761, tab762, tab763, tab764, tab765, tab766, tab767, tab768, tab769, tab770, tab771, tab772, tab773, tab774, tab775, tab776, tab777, tab778, tab779, tab780, tab781, tab782, tab783, tab784, tab785, tab786, tab787, tab788, tab789, tab790, tab791, tab792, tab793, tab794, tab795, tab796, tab797, tab798, tab799, tab800, tab801, tab802, tab803, tab804, tab805, tab806, tab807, tab808, tab809, tab810, tab811, tab812, tab813, tab814, tab815, tab816, tab817, tab818, tab819, tab820, tab821, tab822, tab823, tab824, tab825, tab826, tab827, tab828, tab829, tab830, tab831, tab832, tab833 = st.tabs([" in src

    def test_titolo_671_in_app(self):
        assert TITLE671 in _app_src()

    def test_with_tab671_in_app(self):
        assert "\n    with tab671:" in _app_src()
