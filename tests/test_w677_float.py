"""Test tab677 "🌊💨 Eolico offshore flottante: il vento in mare aperto paga?"

Demo calcolata eseguendo demo_calcoli() (non a mano):
parco flottante da 500 MW con capacity factor 52 %,
CAPEX 4500 EUR/kW, OPEX fisso 110 EUR/kW/anno e OPEX
variabile 3 EUR/MWh; prezzo CfD/PPA 95 EUR/MWh; vita
30 anni; WACC 0,06 (6 %); tolleranza 0,10 (10 % del
CAPEX).

- produzione_mwh = 500.0 x 0.52 x 8760.0 = 2277600.0 MWh/anno
- ricavi = 2277600.0 x 95.0 = 216372000.0 EUR/anno
- opex_fisso = 110.0 x 500.0 x 1000.0 = 55000000.0 EUR/anno
- opex_variabile = 3.0 x 2277600.0 = 6832800.0 EUR/anno
- opex = 61832800.0 EUR/anno
- margine = 216372000.0 - 61832800.0 = 154539200.0 EUR/anno
- capex_tot = 4500.0 x 500.0 x 1000.0 = 2250000000.0 EUR
- crf = 0.07264891149004721
- lcoe = 98.91677680567537 EUR/MWh (sopra il prezzo CfD: margine per MWh negativo)
- van = -122794005.71374488 EUR
- tir = 5.484031229849188 % (in uscita: percentuale)
- payback = 15
- verdetto = 'MARGINALE' (|VAN| = 122794005.71374488 <= 0.10 x 2250000000.0)
"""

import ast
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w677_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w677_helpers.py via AST
    (stesso pattern di tests/appfuncs.py: niente Streamlit)."""
    src = (_new_dir() / "w677_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w677_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w677_helpers.py: {missing}")
    return out


_F = _load("mh677_num", "mh677_nneg", "mh677_pos",
           "mh677_int_pos", "mh677_quota", "mh677_pct",
           "mh677_produzione", "mh677_ricavi",
           "mh677_opex", "mh677_opex_fisso",
           "mh677_opex_variabile", "mh677_margine",
           "mh677_capex_tot", "mh677_crf", "mh677_lcoe",
           "mh677_van", "mh677_tir", "mh677_payback",
           "mh677_verdetto", "_mh677_neutro",
           "mh677_calcola", "mh677_sensitivita",
           "mh677_csv", "mh677_demo", "demo_calcoli")

TITLE677 = ("🌊💨 Eolico offshore flottante: il vento in "
            "mare aperto paga?")

PROD_DEMO = 2277600.0
RICAVI_DEMO = 216372000.0
OPEX_FISSO_DEMO = 55000000.0
OPEX_VAR_DEMO = 6832800.0
OPEX_DEMO = 61832800.0
MARG_DEMO = 154539200.0
CAPEX_DEMO = 2250000000.0
CRF_DEMO = 0.07264891149004721
LCOE_DEMO = 98.91677680567537
VAN_DEMO = -122794005.71374488
TIR_DEMO = 5.484031229849188
PAYBACK_DEMO = 15
VITA_DEMO = 30
VERDETTO_DEMO = "MARGINALE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w677_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w677_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh677_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh677_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh677_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh677_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh677_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh677_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh677_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh677_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh677_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh677_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh677_int_pos"](30.0, "x") == 30

    def test_quota_rifiuta_oltre_1(self):
        with pytest.raises(ValueError):
            _F["mh677_quota"](1.01, "x")

    def test_quota_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh677_quota"](-0.01, "x")

    def test_pct_rifiuta_oltre_100(self):
        with pytest.raises(ValueError):
            _F["mh677_pct"](100.01, "x")

    def test_pct_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh677_pct"](-0.01, "x")

    def test_pct_accetta_estremi(self):
        assert _F["mh677_pct"](0.0, "x") == 0.0
        assert _F["mh677_pct"](100.0, "x") == 100.0
        assert _F["mh677_pct"](52.0, "x") == 52.0


class TestFisica:
    def test_produzione_demo(self):
        assert _F["mh677_produzione"](
            500.0, 52.0) == pytest.approx(PROD_DEMO, rel=REL)

    def test_produzione_formula(self):
        assert _F["mh677_produzione"](
            100.0, 50.0) == pytest.approx(
            100.0 * 0.50 * 8760.0, rel=1e-12)

    def test_produzione_zero_se_cf_zero(self):
        assert _F["mh677_produzione"](500.0, 0.0) == 0.0

    def test_produzione_rifiuta_potenza_zero(self):
        with pytest.raises(ValueError):
            _F["mh677_produzione"](0.0, 52.0)

    def test_produzione_rifiuta_potenza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh677_produzione"](-10.0, 52.0)

    def test_produzione_rifiuta_cf_oltre_100(self):
        with pytest.raises(ValueError):
            _F["mh677_produzione"](500.0, 100.01)

    def test_ricavi_demo(self):
        assert _F["mh677_ricavi"](
            PROD_DEMO, 95.0) == pytest.approx(RICAVI_DEMO,
                                              rel=REL)

    def test_ricavi_zero_se_prezzo_zero(self):
        assert _F["mh677_ricavi"](PROD_DEMO, 0.0) == 0.0

    def test_ricavi_rifiuta_produzione_negativa(self):
        with pytest.raises(ValueError):
            _F["mh677_ricavi"](-1.0, 95.0)

    def test_ricavi_rifiuta_prezzo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh677_ricavi"](PROD_DEMO, -0.01)

    def test_opex_demo(self):
        assert _F["mh677_opex"](
            500.0, 110.0, PROD_DEMO,
            3.0) == pytest.approx(OPEX_DEMO, rel=REL)

    def test_opex_somma_componenti(self):
        o = _F["mh677_opex"](500.0, 110.0, PROD_DEMO, 3.0)
        of = _F["mh677_opex_fisso"](500.0, 110.0)
        ov = _F["mh677_opex_variabile"](PROD_DEMO, 3.0)
        assert of == pytest.approx(OPEX_FISSO_DEMO, rel=REL)
        assert ov == pytest.approx(OPEX_VAR_DEMO, rel=REL)
        assert o == pytest.approx(of + ov, rel=REL)

    def test_opex_rifiuta_opex_fisso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh677_opex"](500.0, -1.0, PROD_DEMO, 3.0)

    def test_opex_rifiuta_opex_var_negativo(self):
        with pytest.raises(ValueError):
            _F["mh677_opex"](500.0, 110.0, PROD_DEMO, -0.01)

    def test_opex_rifiuta_potenza_zero(self):
        with pytest.raises(ValueError):
            _F["mh677_opex"](0.0, 110.0, PROD_DEMO, 3.0)

    def test_margine_demo(self):
        assert _F["mh677_margine"](
            RICAVI_DEMO, OPEX_DEMO) == pytest.approx(
            MARG_DEMO, rel=REL)

    def test_margine_puo_essere_negativo(self):
        assert _F["mh677_margine"](100.0, 150.0) == -50.0

    def test_margine_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh677_margine"](float("nan"), 0.0)

    def test_capex_tot_demo(self):
        assert _F["mh677_capex_tot"](
            4500.0, 500.0) == pytest.approx(CAPEX_DEMO,
                                            rel=REL)

    def test_capex_tot_zero_se_unitario_zero(self):
        assert _F["mh677_capex_tot"](0.0, 500.0) == 0.0

    def test_capex_tot_rifiuta_unitario_negativo(self):
        with pytest.raises(ValueError):
            _F["mh677_capex_tot"](-1.0, 500.0)

    def test_capex_tot_rifiuta_potenza_zero(self):
        with pytest.raises(ValueError):
            _F["mh677_capex_tot"](4500.0, 0.0)

    def test_crf_demo(self):
        assert _F["mh677_crf"](
            0.06, 30) == pytest.approx(CRF_DEMO, rel=REL)

    def test_crf_wacc_zero(self):
        assert _F["mh677_crf"](
            0.0, 30) == pytest.approx(1.0 / 30.0, rel=1e-12)

    def test_crf_rifiuta_wacc_negativo(self):
        with pytest.raises(ValueError):
            _F["mh677_crf"](-0.01, 30)

    def test_crf_rifiuta_vita_zero(self):
        with pytest.raises(ValueError):
            _F["mh677_crf"](0.06, 0)

    def test_lcoe_demo(self):
        assert _F["mh677_lcoe"](
            CAPEX_DEMO, CRF_DEMO, OPEX_DEMO,
            PROD_DEMO) == pytest.approx(LCOE_DEMO, rel=REL)

    def test_lcoe_formula(self):
        c, f, o, e = 1e9, 0.08, 5e7, 2e6
        assert _F["mh677_lcoe"](
            c, f, o, e) == pytest.approx((c * f + o) / e,
                                        rel=1e-12)

    def test_lcoe_sopra_prezzo_cfd_demo(self):
        # margine per MWh negativo nella demo: il
        # progetto distrugge valore a ogni MWh
        assert LCOE_DEMO > 95.0
        assert 95.0 - LCOE_DEMO == pytest.approx(
            -3.91677680567537, rel=1e-9)

    def test_lcoe_rifiuta_produzione_zero(self):
        with pytest.raises(ValueError):
            _F["mh677_lcoe"](CAPEX_DEMO, CRF_DEMO,
                             OPEX_DEMO, 0.0)


class TestFinanza:
    def test_van_demo(self):
        assert _F["mh677_van"](
            MARG_DEMO, CAPEX_DEMO, 0.06,
            VITA_DEMO) == pytest.approx(VAN_DEMO, rel=REL)

    def test_van_tasso_zero(self):
        assert _F["mh677_van"](
            MARG_DEMO, CAPEX_DEMO, 0.0,
            30) == pytest.approx(
            -CAPEX_DEMO + MARG_DEMO * 30, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh677_van"](MARG_DEMO, CAPEX_DEMO, -0.01, 30)

    def test_van_rifiuta_capex_negativo(self):
        with pytest.raises(ValueError):
            _F["mh677_van"](MARG_DEMO, -1.0, 0.06, 30)

    def test_tir_demo(self):
        # mh677_tir ritorna la frazione; il calcola la
        # converte in percentuale
        assert _F["mh677_tir"](
            CAPEX_DEMO, MARG_DEMO,
            VITA_DEMO) == pytest.approx(TIR_DEMO / 100.0,
                                       rel=1e-9)

    def test_tir_none_se_margine_non_positivo(self):
        assert _F["mh677_tir"](CAPEX_DEMO, 0.0, 30) is None
        assert _F["mh677_tir"](CAPEX_DEMO, -100.0, 30) is None

    def test_tir_none_se_capex_zero(self):
        # CAPEX = 0 con margine positivo: nessun cambio
        # di segno nei flussi -> None
        assert _F["mh677_tir"](0.0, MARG_DEMO, 30) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh677_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo(self):
        assert _F["mh677_payback"](
            CAPEX_DEMO, MARG_DEMO,
            VITA_DEMO) == PAYBACK_DEMO

    def test_payback_anno_1_se_margine_ge_capex(self):
        assert _F["mh677_payback"](1000.0, 1000.0, 30) == 1
        assert _F["mh677_payback"](1000.0, 2000.0, 30) == 1

    def test_payback_none_mai(self):
        assert _F["mh677_payback"](CAPEX_DEMO, 1.0, 30) is None

    def test_payback_none_se_margine_non_positivo(self):
        assert _F["mh677_payback"](CAPEX_DEMO, 0.0, 30) is None

    def test_verdetto_marginale_demo(self):
        assert _F["mh677_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10,
            MARG_DEMO) == VERDETTO_DEMO

    def test_verdetto_conviente_ad_hoc(self):
        assert _F["mh677_verdetto"](
            1000.0, CAPEX_DEMO, 0.10,
            MARG_DEMO) == "CONVIENTE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh677_verdetto"](
            -500000000.0, CAPEX_DEMO, 0.10,
            MARG_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_margine_non_positivo(
            self):
        assert _F["mh677_verdetto"](
            1000.0, CAPEX_DEMO, 0.10,
            0.0) == "NON_CALCOLABILE"
        assert _F["mh677_verdetto"](
            1000.0, CAPEX_DEMO, 0.10,
            -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_non_negativo_conviente(
            self):
        assert _F["mh677_verdetto"](
            0.0, 0.0, 0.10, MARG_DEMO) == "CONVIENTE"
        assert _F["mh677_verdetto"](
            1000.0, 0.0, 0.10, MARG_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(
            self):
        # CAPEX == 0: tolleranza zero, mai MARGINALE
        assert _F["mh677_verdetto"](
            -1.0, 0.0, 0.10, MARG_DEMO) == "NON_CONVIENTE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh677_verdetto"](100.0, CAPEX_DEMO, -0.01,
                                 MARG_DEMO)


class TestGuard:
    def _bc(self, **kw):
        d = _F["mh677_demo"]()
        d.update(kw)
        return _F["mh677_calcola"](**d)

    def test_potenza_zero_neutro(self):
        n = self._bc(potenza_mw=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["produzione_mwh"] == 0.0
        assert n["margine"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_potenza_negativa_neutro(self):
        n = self._bc(potenza_mw=-100.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_cf_oltre_100_neutro(self):
        n = self._bc(cf_pct=101.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_cf_negativo_neutro(self):
        n = self._bc(cf_pct=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_cf_zero_produzione_nulla_neutro(self):
        # cf = 0 -> produzione 0 -> LCOE non
        # definibile -> neutro
        n = self._bc(cf_pct=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["produzione_mwh"] == 0.0
        assert n["lcoe"] == 0.0

    def test_capex_negativo_neutro(self):
        n = self._bc(capex_eur_kw=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_opex_fisso_negativo_neutro(self):
        n = self._bc(opex_fisso_eur_kw_anno=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_opex_var_negativo_neutro(self):
        n = self._bc(opex_var_eur_mwh=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzo_negativo_neutro(self):
        n = self._bc(prezzo_energia_eur_mwh=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_negativo_neutro(self):
        n = self._bc(wacc=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_negativa_neutro(self):
        n = self._bc(tolleranza=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(prezzo_energia_eur_mwh=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["ricavi"] == 0.0

    def test_bool_neutro(self):
        n = self._bc(potenza_mw=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzo_zero_margine_negativo_neutro(self):
        # prezzo nullo: ricavi 0, OPEX positivo ->
        # margine < 0 -> neutro
        n = self._bc(prezzo_energia_eur_mwh=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["margine"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_prezzo_basso_margine_non_positivo_neutro(self):
        # 20 EUR/MWh: ricavi 45,6 M < OPEX 61,8 M
        n = self._bc(prezzo_energia_eur_mwh=20.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh677_neutro"]()
        assert list(n["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(n["df_flussi"]) == 0
        assert list(n["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(n["df_tabella"]) == 0

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh677_neutro"]()
        for chiave in ("produzione_mwh", "ricavi",
                       "opex_fisso", "opex_variabile",
                       "opex", "margine", "capex_tot",
                       "crf", "lcoe", "van", "tir",
                       "payback", "verdetto", "df_flussi",
                       "df_tabella"):
            assert chiave in n, chiave

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert list(b["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(b["df_tabella"]) == 10
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Produzione annua (MWh/anno)" in voci
        assert "LCOE (EUR/MWh)" in voci
        assert "Margine operativo (EUR/anno)" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(b["df_flussi"]) == VITA_DEMO + 1
        assert b["df_flussi"]["Cumulato (€)"].iloc[-1] == \
            pytest.approx(-CAPEX_DEMO + MARG_DEMO * VITA_DEMO,
                          rel=REL)


class TestSensitivitaCsv:
    def _ing(self):
        return _F["mh677_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh677_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["CF x0.8", "CF x1.0",
                                   "CF x1.2"]
        assert list(s.index) == ["x0.8", "x1.0", "x1.2"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh677_sensitivita"](self._ing())
        assert s.loc["x1.0", "CF x1.0"] == pytest.approx(
            VAN_DEMO, rel=REL)

    def test_sensitivita_monotona(self):
        # VAN cresce con prezzo e con capacity factor
        s = _F["mh677_sensitivita"](self._ing())
        assert s.loc["x1.2", "CF x1.2"] > s.loc["x1.0",
                                                "CF x1.0"]
        assert s.loc["x0.8", "CF x0.8"] < s.loc["x1.0",
                                                "CF x1.0"]

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh677_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 22

    def test_csv_contiene_verdetto_e_lcoe(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh677_csv"](bc, self._ing())
        assert "verdetto;MARGINALE" in txt
        assert "lcoe_eur_mwh" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh677_csv"](bc, self._ing())
        assert f"produzione_mwh_anno;{PROD_DEMO}" in txt
        assert f"margine_eur_anno;{MARG_DEMO}" in txt


class TestDemo:
    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["produzione_mwh"] == pytest.approx(
            PROD_DEMO, rel=REL)
        assert c["ricavi"] == pytest.approx(
            RICAVI_DEMO, rel=REL)
        assert c["opex_fisso"] == pytest.approx(
            OPEX_FISSO_DEMO, rel=REL)
        assert c["opex_variabile"] == pytest.approx(
            OPEX_VAR_DEMO, rel=REL)
        assert c["opex"] == pytest.approx(
            OPEX_DEMO, rel=REL)
        assert c["margine"] == pytest.approx(
            MARG_DEMO, rel=REL)
        assert c["capex_tot"] == pytest.approx(
            CAPEX_DEMO, rel=REL)
        assert c["crf"] == pytest.approx(CRF_DEMO, rel=REL)
        assert c["lcoe"] == pytest.approx(
            LCOE_DEMO, rel=REL)
        assert c["van"] == pytest.approx(VAN_DEMO, rel=REL)
        assert c["tir"] == pytest.approx(TIR_DEMO, rel=REL)
        assert c["payback"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()[
            "van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()[
            "lcoe"] == _F["demo_calcoli"]()["lcoe"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        """mh677_calcola(**mh677_demo()) deve matchare le
        costanti _DEMO entro 1e-9 relativo (mismatch
        vietato), chiave per chiave."""
        d = _F["mh677_demo"]()
        b = _F["mh677_calcola"](**d)
        coppie = [("produzione_mwh", PROD_DEMO),
                  ("ricavi", RICAVI_DEMO),
                  ("opex_fisso", OPEX_FISSO_DEMO),
                  ("opex_variabile", OPEX_VAR_DEMO),
                  ("opex", OPEX_DEMO),
                  ("margine", MARG_DEMO),
                  ("capex_tot", CAPEX_DEMO),
                  ("crf", CRF_DEMO),
                  ("lcoe", LCOE_DEMO),
                  ("van", VAN_DEMO),
                  ("tir", TIR_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh677_demo"]()
        assert d["potenza_mw"] == 500.0
        assert d["cf_pct"] == 52.0
        assert d["capex_eur_kw"] == 4500.0
        assert d["opex_fisso_eur_kw_anno"] == 110.0
        assert d["opex_var_eur_mwh"] == 3.0
        assert d["prezzo_energia_eur_mwh"] == 95.0
        assert d["vita_anni"] == 30
        assert d["wacc"] == 0.06
        assert d["tolleranza"] == 0.10

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("produzione_mwh", "ricavi",
                       "opex_fisso", "opex_variabile",
                       "opex", "margine", "capex_tot",
                       "crf", "lcoe", "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 15" in doc
        assert "verdetto = 'MARGINALE'" in doc


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def677["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def677\["([a-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) >= 9, ui_keys
        demo_keys = set(_F["mh677_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestUI:
    def test_header_helpers_presente(self):
        assert '# W677 (24/10/2026) - tab677' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh677_num", "mh677_nneg", "mh677_pos",
                     "mh677_int_pos", "mh677_quota",
                     "mh677_pct", "mh677_produzione",
                     "mh677_ricavi", "mh677_opex",
                     "mh677_opex_fisso",
                     "mh677_opex_variabile",
                     "mh677_margine", "mh677_capex_tot",
                     "mh677_crf", "mh677_lcoe",
                     "mh677_van", "mh677_tir",
                     "mh677_payback", "mh677_verdetto",
                     "_mh677_neutro", "mh677_calcola",
                     "mh677_sensitivita", "mh677_csv",
                     "mh677_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE677) == 1

    def test_blocco_with_tab677(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab677:"

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st677_[a-z0-9_]+)"', _ui_src())
        assert len(keys) >= 14
        assert len(set(keys)) == len(keys)
        # nessuna collisione con le chiavi dei cicli precedenti
        assert not any(k.startswith("st676_") for k in keys)
        assert not any(k.startswith("st675_") for k in keys)
        assert not any(k.startswith("st674_") for k in keys)

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg677" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg677") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg677")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Produzione (GWh/anno)" in src
        assert "LCOE (€/MWh)" in src
        assert "VAN (€)" in src
        assert "TIR / Payback" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd677" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_lcoe_vs_cfd_presente(self):
        src = _ui_src()
        assert "LCOE vs prezzo CfD" in src
        assert "margine per MWh" in src
        assert "prezzo CfD" in src

    def test_nota_flottante_vs_fisso_presente(self):
        src = _ui_src()
        assert "60 m" in src
        assert "monopali" in src
        assert "capacity factor" in src.lower() or \
            "CAPACITY FACTOR" in src

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Ricavi CfD/PPA" in src
        assert "Margine operativo" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert 'sep=";"' in src or "mh677_csv" in src
        assert "eolico_flottante_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitiv" in src
        assert "mh677_sensitivita" in src
        assert "Heatmap" in src
        assert "Prezzo energia" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st677_show_flussi" in src
        assert "st.checkbox" in src

    def test_differenziazione_da_feature_esistenti(self):
        src = _ui_src()
        assert "flottante" in src
        assert "CfD" in src
        assert "spar" in src


class TestApplyContract:
    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE677

    def test_ancora_helper_presente(self):
        assert "# W677 (24/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab677:")
        assert "mh677_calcola" in _helpers_src()
        assert "demo_calcoli" in _helpers_src()
        assert "import streamlit" not in _helpers_src()
        assert "tab677" in (_new_dir() / "w677_test.py")\
            .read_text(encoding="utf-8")


class TestSegreti:
    def test_nessun_segreto_nei_file(self):
        for fn in ("w677_helpers.py", "w677_ui.py",
                   "w677_test.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            assert not re.search(
                r"(?i)(api[_-]?key|secret|password|passwd|token)"
                r"\s*=\s*[\"']",
                src), fn
