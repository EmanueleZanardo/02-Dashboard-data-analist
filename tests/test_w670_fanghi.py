"""Test tab670 "🧱💧 Essiccazione fanghi: togliere l'acqua dai fanghi paga?"

Demo calcolata eseguendo mh670_demo_calcoli() (non a mano):
depuratore da 12.000 t/anno di fango umido al 22 % di
sostanza secca, essiccato al 90 % con rendimento 0,78 e
42 kWh/t_acqua di ausiliari elettrici; gas a 0,085
EUR/kWh, elettricita' a 0,21 EUR/kWh; smaltimento tal
quale 130 EUR/t contro 45 EUR/t da essiccato, O&M
90.000 EUR/anno; CAPEX 2.200.000 EUR; fattori emissivi
0,20 kg/kWh (gas), 0,35 kg/kWh (elettrico), 55 kg/t
(smaltimento); tasso 6 %, vita 15 anni, tolleranza 10 %
del CAPEX.

- m_ds = 12000.0 x 22.0/100 = 2640.0 t/anno
- m_out = 2640.0 / (90.0/100) = 2933.3333333333335 t/anno
- m_acqua = 12000.0 - 2933.3333333333335 = 9066.666666666666 t/anno
- Q_evap = 9066.666666666666 x 1000 x 2257 / 3600 = 5684296.296296296 kWh/anno
- Q_th = 5684296.296296296 / 0.78 = 7287559.35422602 kWh/anno
- E_el = 9066.666666666666 x 42.0 = 380800.0 kWh/anno
- C_therm = 7287559.35422602 x 0.085 = 619442.5451092118 EUR/anno
- C_el = 380800.0 x 0.21 = 79968.0 EUR/anno
- C_essicc = 619442.5451092118 + 79968.0 + 90000.0 = 789410.5451092118 EUR/anno
- C_base = 12000.0 x 130.0 = 1560000.0 EUR/anno
- C_disp_new = 2933.3333333333335 x 45.0 = 132000.0 EUR/anno
- risp_smalt = 1560000.0 - 132000.0 = 1428000.0 EUR/anno
- risp = 1428000.0 - 789410.5451092118 = 638589.4548907882 EUR/anno
- CO2_base = 12000.0 x 55.0/1000 = 660.0 t/anno
- CO2_new = 2933.3333333333335 x 55.0/1000 + 7287559.35422602 x 0.20/1000 + 380800.0 x 0.35/1000 = 1752.1252041785374 t/anno
- CO2 evitata = 660.0 - 1752.1252041785374 = -1092.1252041785374 t/anno (extra emessa: l'essiccatore a gas emette piu' di quanto evita lo smaltimento)
- flussi [-2200000.0, 638589.4548907882 x 15];
  VAN(6 %) = 4002139.78684513 EUR -> CONVIENTE (VAN > 0)
- TIR = 28.339066660379466 % (bisezione su [-0.99, 10])
- payback_anni = 4 (primo anno con cumulato >= 0)
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
    if (p / "w670_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w670_helpers.py via AST
    (stesso pattern di tests/appfuncs.py: niente Streamlit)."""
    src = (_new_dir() / "w670_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w670_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w670_helpers.py: {missing}")
    return out


_F = _load("mh670_num", "mh670_nneg", "mh670_pos", "mh670_int_pos",
           "mh670_massa_secca", "mh670_massa_uscita",
           "mh670_acqua_evaporata", "mh670_q_evap",
           "mh670_q_termica", "mh670_costi_essiccazione",
           "mh670_smaltimento", "mh670_risparmio",
           "mh670_co2", "mh670_van", "mh670_tir",
           "mh670_payback", "mh670_verdetto", "_mh670_neutro",
           "mh670_business_case", "mh670_demo",
           "mh670_demo_calcoli")

TITLE670 = "🧱💧 Essiccazione fanghi: togliere l'acqua dai fanghi paga?"

M_DS_DEMO = 2640.0
M_OUT_DEMO = 2933.3333333333335
M_ACQUA_DEMO = 9066.666666666666
Q_EVAP_DEMO = 5684296.296296296
Q_TH_DEMO = 7287559.35422602
E_EL_DEMO = 380800.0
C_THERM_DEMO = 619442.5451092118
C_EL_DEMO = 79968.0
C_ESSICC_DEMO = 789410.5451092118
C_BASE_DEMO = 1560000.0
C_DISP_NEW_DEMO = 132000.0
RISP_SMALT_DEMO = 1428000.0
RISP_DEMO = 638589.4548907882
CO2_BASE_DEMO = 660.0
CO2_NEW_DEMO = 1752.1252041785374
CO2_EVITATA_DEMO = -1092.1252041785374
VAN_DEMO = 4002139.78684513
TIR_PCT_DEMO = 28.339066660379466
PAYBACK_DEMO = 4
VITA_DEMO = 15
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w670_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w670_ui.py").read_text(encoding="utf-8")


def _app_src():
    return (Path.home() / "workspace/repo-dashboard/"
            "Dashboard-data-analist/app.py").read_text(
                encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh670_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh670_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh670_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh670_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh670_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh670_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh670_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh670_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh670_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh670_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh670_int_pos"](10.0, "x") == 10


class TestFisica:
    def test_massa_secca_demo(self):
        assert _F["mh670_massa_secca"](
            12000.0, 22.0) == pytest.approx(M_DS_DEMO,
                                             rel=REL)

    def test_massa_secca_rifiuta_ds_zero(self):
        with pytest.raises(ValueError):
            _F["mh670_massa_secca"](12000.0, 0.0)

    def test_massa_secca_rifiuta_ds_100(self):
        with pytest.raises(ValueError):
            _F["mh670_massa_secca"](12000.0, 100.0)

    def test_massa_secca_rifiuta_fango_zero(self):
        with pytest.raises(ValueError):
            _F["mh670_massa_secca"](0.0, 22.0)

    def test_massa_uscita_demo(self):
        assert _F["mh670_massa_uscita"](
            M_DS_DEMO, 90.0) == pytest.approx(M_OUT_DEMO,
                                              rel=REL)

    def test_massa_uscita_rifiuta_ds_100(self):
        with pytest.raises(ValueError):
            _F["mh670_massa_uscita"](M_DS_DEMO, 100.0)

    def test_acqua_evaporata_demo(self):
        assert _F["mh670_acqua_evaporata"](
            12000.0, M_OUT_DEMO) == pytest.approx(
            M_ACQUA_DEMO, rel=REL)

    def test_acqua_evaporata_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh670_acqua_evaporata"](1000.0, 1500.0)

    def test_q_evap_demo(self):
        assert _F["mh670_q_evap"](
            M_ACQUA_DEMO) == pytest.approx(Q_EVAP_DEMO,
                                           rel=REL)

    def test_q_evap_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh670_q_evap"](-1.0)

    def test_q_termica_demo(self):
        assert _F["mh670_q_termica"](
            Q_EVAP_DEMO, 0.78) == pytest.approx(Q_TH_DEMO,
                                                rel=REL)

    def test_q_termica_rifiuta_rendimento_1(self):
        with pytest.raises(ValueError):
            _F["mh670_q_termica"](Q_EVAP_DEMO, 1.0)

    def test_q_termica_rifiuta_rendimento_zero(self):
        with pytest.raises(ValueError):
            _F["mh670_q_termica"](Q_EVAP_DEMO, 0.0)

    def test_costi_essiccazione_dict_demo(self):
        c = _F["mh670_costi_essiccazione"](
            Q_TH_DEMO, 0.085, M_ACQUA_DEMO, 42.0, 0.21,
            90000.0)
        assert c["c_therm"] == pytest.approx(C_THERM_DEMO,
                                             rel=REL)
        assert c["e_el"] == pytest.approx(E_EL_DEMO,
                                         rel=REL)
        assert c["c_el"] == pytest.approx(C_EL_DEMO,
                                          rel=REL)
        assert c["totale"] == pytest.approx(C_ESSICC_DEMO,
                                            rel=REL)

    def test_costi_essiccazione_rifiuta_prezzo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh670_costi_essiccazione"](
                Q_TH_DEMO, -0.01, M_ACQUA_DEMO, 42.0, 0.21,
                90000.0)

    def test_costi_essiccazione_rifiuta_e_spec_negativo(self):
        with pytest.raises(ValueError):
            _F["mh670_costi_essiccazione"](
                Q_TH_DEMO, 0.085, M_ACQUA_DEMO, -1.0, 0.21,
                90000.0)

    def test_smaltimento_dict_demo(self):
        s = _F["mh670_smaltimento"](12000.0, M_OUT_DEMO,
                                    130.0, 45.0)
        assert s["c_base"] == pytest.approx(C_BASE_DEMO,
                                            rel=REL)
        assert s["c_disp_new"] == pytest.approx(
            C_DISP_NEW_DEMO, rel=REL)
        assert s["risp_smalt"] == pytest.approx(
            RISP_SMALT_DEMO, rel=REL)

    def test_smaltimento_rifiuta_fango_zero(self):
        with pytest.raises(ValueError):
            _F["mh670_smaltimento"](0.0, M_OUT_DEMO, 130.0,
                                    45.0)

    def test_smaltimento_rifiuta_costo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh670_smaltimento"](12000.0, M_OUT_DEMO,
                                    -1.0, 45.0)

    def test_risparmio_demo(self):
        assert _F["mh670_risparmio"](
            RISP_SMALT_DEMO, C_ESSICC_DEMO) == pytest.approx(
            RISP_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh670_risparmio"](100.0, 200.0) == -100.0

    def test_co2_dict_demo(self):
        c = _F["mh670_co2"](12000.0, M_OUT_DEMO, 55.0,
                            Q_TH_DEMO, 0.20, E_EL_DEMO,
                            0.35)
        assert c["co2_base"] == pytest.approx(CO2_BASE_DEMO,
                                             rel=REL)
        assert c["co2_new"] == pytest.approx(CO2_NEW_DEMO,
                                            rel=REL)
        assert c["co2_evitata"] == pytest.approx(
            CO2_EVITATA_DEMO, rel=REL)

    def test_co2_puo_essere_negativa_extra_emessa(self):
        # rendimento pessimo e combustibile pesante: il
        # bilancio CO2 peggiora (extra emessa)
        c = _F["mh670_co2"](100.0, 99.0, 55.0, 5000.0,
                            0.40, 10000.0, 0.35)
        assert c["co2_evitata"] < 0.0

    def test_co2_rifiuta_fattore_negativo(self):
        with pytest.raises(ValueError):
            _F["mh670_co2"](12000.0, M_OUT_DEMO, -1.0,
                            Q_TH_DEMO, 0.20, E_EL_DEMO,
                            0.35)


class TestFinanza:
    def test_van_demo(self):
        assert _F["mh670_van"](
            RISP_DEMO, 2200000.0, 6.0,
            VITA_DEMO) == pytest.approx(VAN_DEMO, rel=REL)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh670_van"](RISP_DEMO, 2200000.0, -0.01, 15)

    def test_van_tasso_zero(self):
        assert _F["mh670_van"](
            RISP_DEMO, 2200000.0, 0.0, 15) == pytest.approx(
            -2200000.0 + RISP_DEMO * 15, rel=1e-12)

    def test_tir_none_se_risp_non_positivo(self):
        assert _F["mh670_tir"](2200000.0, 0.0, 15) is None
        assert _F["mh670_tir"](2200000.0, -100.0, 15) is None

    def test_tir_demo(self):
        assert _F["mh670_tir"](
            2200000.0, RISP_DEMO, VITA_DEMO) * 100.0 == \
            pytest.approx(TIR_PCT_DEMO, rel=REL)

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh670_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo(self):
        assert _F["mh670_payback"](
            2200000.0, RISP_DEMO, VITA_DEMO) == PAYBACK_DEMO

    def test_payback_none_mai(self):
        assert _F["mh670_payback"](100000.0, 1.0, 15) is None

    def test_payback_none_se_risp_non_positivo(self):
        assert _F["mh670_payback"](2200000.0, 0.0, 15) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh670_verdetto"](
            VAN_DEMO, 2200000.0, 10.0,
            RISP_DEMO) == VERDETTO_DEMO

    def test_verdetto_marginale_ad_hoc(self):
        # VAN negativo entro il 10 % del CAPEX
        assert _F["mh670_verdetto"](
            -0.05 * 2200000.0, 2200000.0, 10.0,
            RISP_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh670_verdetto"](
            -500000.0, 2200000.0, 10.0,
            RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risp_non_positivo(self):
        assert _F["mh670_verdetto"](
            1000.0, 2200000.0, 10.0,
            0.0) == "NON_CALCOLABILE"
        assert _F["mh670_verdetto"](
            1000.0, 2200000.0, 10.0,
            -50.0) == "NON_CALCOLABILE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh670_verdetto"](100.0, 2200000.0, -1.0,
                                 RISP_DEMO)


class TestGuard:
    def _bc(self, **kw):
        d = _F["mh670_demo"]()
        d.update(kw)
        return _F["mh670_business_case"](**d)

    def test_fango_zero_neutro(self):
        n = self._bc(m_wet=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["m_acqua"] == 0.0
        assert n["risp_eur"] == 0.0
        assert n["tir_pct"] is None
        assert n["payback_anni"] is None

    def test_ds_out_non_maggiore_ds_in_neutro(self):
        n = self._bc(ds_out=22.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["van_eur"] == 0.0

    def test_ds_in_100_neutro(self):
        n = self._bc(ds_in=100.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_rendimento_fuori_intervallo_neutro(self):
        n = self._bc(eta_dryer=1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        n2 = self._bc(eta_dryer=0.0)
        assert n2["verdetto"] == "NON_CALCOLABILE"

    def test_e_spec_negativo_neutro(self):
        n = self._bc(e_spec=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzo_combustibile_negativo_neutro(self):
        n = self._bc(p_fuel=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_fattore_emissivo_negativo_neutro(self):
        n = self._bc(f_fuel=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(r_pct=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["c_base"] == 0.0

    def test_bool_neutro(self):
        n = self._bc(m_wet=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_risp_non_positivo_neutro(self):
        # smaltimento tal quale uguale all'essiccato e O&M
        # altissimo: essiccare non paga
        n = self._bc(c_smalt_in=45.0, om=2000000.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risp_eur"] == 0.0
        assert n["tir_pct"] is None
        assert n["payback_anni"] is None

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh670_neutro"]()
        assert list(n["df_voci"].columns) == ["Voce",
                                             "Valore (EUR/anno)"]
        assert len(n["df_voci"]) == 0

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh670_neutro"]()
        for chiave in ("m_ds", "m_out", "m_acqua",
                       "q_evap_kwh", "q_th_kwh", "e_el_kwh",
                       "c_therm", "c_el", "om",
                       "costi_essicc_tot", "c_base",
                       "c_disp_new", "risp_smalt", "risp_eur",
                       "co2_base", "co2_new", "co2_evitata",
                       "van_eur", "tir_pct", "payback_anni",
                       "verdetto", "df_voci"):
            assert chiave in n, chiave

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert list(b["df_voci"].columns) == ["Voce",
                                             "Valore (EUR/anno)"]
        assert len(b["df_voci"]) == 8
        voci = b["df_voci"]["Voce"].tolist()
        assert "Risparmio netto" in voci
        assert "Risparmio smaltimento" in voci


class TestDemo:
    def test_demo_calcoli_end_to_end(self):
        c = _F["mh670_demo_calcoli"]()
        assert c["m_ds"] == pytest.approx(M_DS_DEMO, rel=REL)
        assert c["m_out"] == pytest.approx(M_OUT_DEMO, rel=REL)
        assert c["m_acqua"] == pytest.approx(M_ACQUA_DEMO,
                                             rel=REL)
        assert c["q_evap_kwh"] == pytest.approx(Q_EVAP_DEMO,
                                                rel=REL)
        assert c["q_th_kwh"] == pytest.approx(Q_TH_DEMO,
                                              rel=REL)
        assert c["e_el_kwh"] == pytest.approx(E_EL_DEMO,
                                             rel=REL)
        assert c["c_therm"] == pytest.approx(C_THERM_DEMO,
                                            rel=REL)
        assert c["c_el"] == pytest.approx(C_EL_DEMO, rel=REL)
        assert c["costi_essicc_tot"] == pytest.approx(
            C_ESSICC_DEMO, rel=REL)
        assert c["c_base"] == pytest.approx(C_BASE_DEMO,
                                           rel=REL)
        assert c["c_disp_new"] == pytest.approx(
            C_DISP_NEW_DEMO, rel=REL)
        assert c["risp_smalt"] == pytest.approx(
            RISP_SMALT_DEMO, rel=REL)
        assert c["risp_eur"] == pytest.approx(RISP_DEMO,
                                             rel=REL)
        assert c["co2_base"] == pytest.approx(CO2_BASE_DEMO,
                                             rel=REL)
        assert c["co2_new"] == pytest.approx(CO2_NEW_DEMO,
                                            rel=REL)
        assert c["co2_evitata"] == pytest.approx(
            CO2_EVITATA_DEMO, rel=REL)
        assert c["van_eur"] == pytest.approx(VAN_DEMO, rel=REL)
        assert c["tir_pct"] == pytest.approx(TIR_PCT_DEMO,
                                             rel=REL)
        assert c["payback_anni"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO

    def test_demo_calcoli_deterministico(self):
        assert _F["mh670_demo_calcoli"]()[
            "van_eur"] == _F["mh670_demo_calcoli"]()["van_eur"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        """business_case(**demo()) deve matchare le costanti
        _DEMO entro 1e-9 relativo (mismatch vietato)."""
        d = _F["mh670_demo"]()
        b = _F["mh670_business_case"](**d)
        coppie = [("m_ds", M_DS_DEMO),
                  ("m_out", M_OUT_DEMO),
                  ("m_acqua", M_ACQUA_DEMO),
                  ("q_evap_kwh", Q_EVAP_DEMO),
                  ("q_th_kwh", Q_TH_DEMO),
                  ("e_el_kwh", E_EL_DEMO),
                  ("c_therm", C_THERM_DEMO),
                  ("c_el", C_EL_DEMO),
                  ("costi_essicc_tot", C_ESSICC_DEMO),
                  ("c_base", C_BASE_DEMO),
                  ("c_disp_new", C_DISP_NEW_DEMO),
                  ("risp_smalt", RISP_SMALT_DEMO),
                  ("risp_eur", RISP_DEMO),
                  ("co2_base", CO2_BASE_DEMO),
                  ("co2_new", CO2_NEW_DEMO),
                  ("co2_evitata", CO2_EVITATA_DEMO),
                  ("van_eur", VAN_DEMO),
                  ("tir_pct", TIR_PCT_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert b["payback_anni"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh670_demo"]()
        assert d["m_wet"] == 12000.0
        assert d["ds_in"] == 22.0
        assert d["ds_out"] == 90.0
        assert d["eta_dryer"] == 0.78
        assert d["e_spec"] == 42.0
        assert d["p_fuel"] == 0.085
        assert d["p_el"] == 0.21
        assert d["c_smalt_in"] == 130.0
        assert d["c_smalt_out"] == 45.0
        assert d["om"] == 90000.0
        assert d["capex"] == 2200000.0
        assert d["f_fuel"] == 0.20
        assert d["f_el"] == 0.35
        assert d["f_smalt"] == 55.0
        assert d["r_pct"] == 6.0
        assert d["n"] == 15
        assert d["tol_pct"] == 10.0

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        mh670_demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["mh670_demo_calcoli"]()
        doc = __doc__
        for chiave in ("m_ds", "m_out", "m_acqua",
                       "q_evap_kwh", "q_th_kwh", "e_el_kwh",
                       "c_therm", "c_el", "costi_essicc_tot",
                       "c_base", "c_disp_new", "risp_smalt",
                       "risp_eur", "co2_base", "co2_new",
                       "co2_evitata", "van_eur", "tir_pct"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback_anni = 4" in doc
        assert "verdetto = 'CONVIENTE'" in doc


class TestUI:
    def test_header_helpers_presente(self):
        assert '# W670 (23/10/2026) - tab670' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh670_num", "mh670_nneg", "mh670_pos",
                     "mh670_int_pos", "mh670_massa_secca",
                     "mh670_massa_uscita",
                     "mh670_acqua_evaporata", "mh670_q_evap",
                     "mh670_q_termica",
                     "mh670_costi_essiccazione",
                     "mh670_smaltimento", "mh670_risparmio",
                     "mh670_co2", "mh670_van", "mh670_tir",
                     "mh670_payback", "mh670_verdetto",
                     "_mh670_neutro", "mh670_business_case",
                     "mh670_demo", "mh670_demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE670) == 1

    def test_blocco_with_tab670(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab670:"

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st670_[a-z0-9_]+)"', _ui_src())
        assert len(keys) >= 16
        assert len(set(keys)) == len(keys)
        # nessuna collisione con le chiavi dei cicli precedenti
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
        assert "Acqua evaporata (t/anno)" in src
        assert "Costo essiccazione (€/anno)" in src
        assert "Risparmio netto (€/anno)" in src
        assert "VAN (k€)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd670" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_co2_presente(self):
        src = _ui_src()
        assert "CO2 evitata" in src
        assert "extra CO2 emessa" in src

    def test_grafico_costi_presente(self):
        src = _ui_src()
        assert "plotly.graph_objects" in src
        assert "Smaltimento base (tal quale)" in src
        assert "Risparmio netto" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert 'sep=";"' in src
        assert "fanghi_essiccazione.csv" in src

    def test_sensitivita_presente(self):
        src = _ui_src()
        assert "Sensitiv" in src
        assert "mh670_business_case" in src

    def test_differenziazione_da_feature_esistenti(self):
        src = _ui_src()
        assert "fanghi" in src.lower()
        assert "tab663" in src

    def test_nessun_segreto_nella_sezione(self):
        assert not re.search(r'(?i)(api_key|secret|password)\s*=\s*["\']',
                             _ui_src())


class TestRegistry:
    """Verifiche sull'app.py applicato: falliscono finche' la
    tab670 non e' applicata (atteso in fase di authoring)."""

    def test_numero_tab_670(self):
        src = _app_src()
        assert len(re.findall(r"\n    with tab\d+:", src)) == 706

    def test_bump_catena_solo_append(self):
        src = _app_src()
        assert ", tab668, tab669, tab670, tab671, tab672, tab673, tab674, tab675, tab676, tab677, tab678, tab679, tab680, tab681, tab682, tab683, tab684, tab685, tab686, tab687, tab688, tab689, tab690, tab691, tab692, tab693, tab694, tab695, tab696, tab697, tab698, tab699, tab700, tab701, tab702, tab703, tab704, tab705, tab706 = st.tabs([" in src

    def test_titolo_670_in_app(self):
        assert TITLE670 in _app_src()

    def test_with_tab670_in_app(self):
        assert "\n    with tab670:" in _app_src()
