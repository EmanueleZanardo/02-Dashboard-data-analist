"""Test tab739 "🏭 Cemento verde: la cattura CO2 sul clinker paga?"

Nuova tab tab739 (cattura CO2 in
cementeria, w740). Business case
deterministico della cattura CO2 sul
clinker: le emissioni di processo
(calcinazione CaCO3 -> CaO + CO2, 0,52
tCO2/t clinker) non si abbattono
cambiando fuel, solo la cattura le
toglie; le emissioni da combustibile
dipendono da consumo specifico e fattore
di emissione. Emissioni totali, CO2
catturata e residua, CRF, costo annuo,
EUA evitate, netto, VAN, TIR, payback,
costo netto per tCO2, margine vs EUA e
verdetto.

Demo calcolata eseguendo demo_calcoli()
(e ricontrollata a mano, riga per riga):
clinker 1000000 t/anno; consumo 3,5 GJ/t;
fattore combustibile 95 kg/GJ; tasso
cattura 90 %; costo cattura 60 EUR/t;
costo trasporto e stoccaggio 25 EUR/t;
CAPEX 400000000 EUR; prezzo EUA 85 EUR/t;
WACC 7 %; vita 20 anni; tolleranza 10 %
del CAPEX.

- e_processo_t = 520000.0
- e_comb_t = 332500.0
- e_tot_t = 852500.0
- co2_catturata_t = 767250.0
- co2_residua_t = 85250.0
- crf = 0.09439292574325567
- costo_annuo_eur = 102973420.29730228
- evitato_eur = 65216250.0
- netto_eur_anno = 0.0
- van = -400000000.0
- tir = None
- payback = None
- costo_netto_eur_per_t = 134.21103981401404
- margine_vs_eua = -49.21103981401404
- verdetto = 'NON_CONVIENTE'

Scomposizione: processo 1000000 x 0,52 =
520000.0 tCO2/anno; combustibile 1000000
x 3,5 x 95 / 1000 = 332500.0 tCO2/anno;
totale 520000.0 + 332500.0 = 852500.0
tCO2/anno; catturata 852500.0 x 90 / 100
= 767250.0 tCO2/anno; residua 852500.0 -
767250.0 = 85250.0 tCO2/anno; CRF
0,07 x 1,07^20 / (1,07^20 - 1) =
0.09439292574325567; quota CAPEX annua
400000000.0 x 0.09439292574325567 =
37757170.29730227 EUR/anno; costo
variabile 767250.0 x (60 + 25) =
65216250.0 EUR/anno; costo annuo
37757170.29730227 + 65216250.0 =
102973420.29730228 EUR/anno; evitato
767250.0 x 85 = 65216250.0 EUR/anno;
netto cassa 65216250.0 - 65216250.0 =
0.0 EUR/anno; flussi: anno 0
-400000000.0, anni 1-20 netto 0.0
(piatti); VAN -400000000.0 + 0.0 x
10,594014245516165 (annuita' 20 anni al
7 %) = -400000000.0 EUR; TIR None
(flussi -400000000.0 poi 0, nessun cambio
di segno); payback None (il cumulato non
raggiunge mai lo zero); costo netto
102973420.29730228 / 767250.0 =
134.21103981401404 EUR/tCO2; margine 85 -
134.21103981401404 = -49.21103981401404
EUR/tCO2; verdetto NON_CONVIENTE perche'
VAN < 0 e |VAN| = 400.000.000 EUR circa >
10 % del CAPEX (40.000.000 EUR).
NOTA: il costo variabile unitario (85
EUR/t) eguaglia il prezzo EUA (85 EUR/t),
quindi l'evitato compensa esattamente il
costo variabile, il netto cassa vale 0 e
la VAN vale -CAPEX (il CAPEX compare una
sola volta, all'anno 0; il CRF entra solo
nel costo annuo livellato).
"""

import ast
import re
from pathlib import Path
import sys
import textwrap

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w740_helpers.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w740_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w740_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w740_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w740_helpers.py: {missing}")
    return out


_F = _load("mh739_num", "mh739_nneg", "mh739_pos",
           "mh739_int_pos", "mh739_pct_0_100",
           "mh739_pct_wacc",
           "mh739_e_processo", "mh739_e_comb",
           "mh739_e_tot", "mh739_catturata",
           "mh739_residua", "mh739_crf",
           "mh739_costo_annuo", "mh739_costo_variabile",
           "mh739_evitato",
           "mh739_netto", "mh739_flussi",
           "mh739_van", "mh739_tir",
           "mh739_payback", "mh739_costo_netto",
           "mh739_margine", "mh739_verdetto",
           "mh739_valida", "_mh739_neutro",
           "mh739_calcola", "mh739_csv",
           "mh739_demo", "demo_calcoli")

TITLE739 = ("🏭 Cemento verde: la cattura CO2 sul clinker paga?")

EP_DEMO = 520000.0
EC_DEMO = 332500.0
ET_DEMO = 852500.0
CATT_DEMO = 767250.0
RES_DEMO = 85250.0
CRF_DEMO = 0.09439292574325567
COSTO_DEMO = 102973420.29730228
EV_DEMO = 65216250.0
NETTO_DEMO = 0.0
VAN_DEMO = -400000000.0
COSTO_VAR_DEMO = 65216250.0
CN_DEMO = 134.21103981401404
MARG_DEMO = -49.21103981401404
VERDETTO_DEMO = "NON_CONVIENTE"

_DEMO = {
    "clinker_t_anno": 1000000.0,
    "consumo_GJ_per_t": 3.5,
    "fattore_comb_kg_per_GJ": 95.0,
    "tasso_cattura_pct": 90.0,
    "costo_cattura_eur_t": 60.0,
    "costo_trasporto_stoccaggio_eur_t": 25.0,
    "capex_eur": 400000000.0,
    "prezzo_eua_eur_t": 85.0,
    "wacc_pct": 7.0,
    "vita_anni": 20,
    "tolleranza_pct": 10.0,
}

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w740_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w740_ui.py").read_text(encoding="utf-8")


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh739_demo"]()
        d.update(kw)
        return _F["mh739_valida"](**d)

    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh739_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh739_num"]("500", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh739_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh739_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh739_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh739_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh739_pos"](0.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh739_int_pos"](2.5, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh739_int_pos"](20.0, "x") == 20

    def test_pct_0_100_accetta_estremi_rifiuta_fuori(self):
        assert _F["mh739_pct_0_100"](0.0, "x") == 0.0
        assert _F["mh739_pct_0_100"](100.0, "x") == 100.0
        with pytest.raises(ValueError):
            _F["mh739_pct_0_100"](-0.01, "x")
        with pytest.raises(ValueError):
            _F["mh739_pct_0_100"](100.01, "x")

    def test_pct_wacc_accetta_zero_e_50_rifiuta_oltre(self):
        assert _F["mh739_pct_wacc"](0.0, "x") == 0.0
        assert _F["mh739_pct_wacc"](50.0, "x") == 50.0
        with pytest.raises(ValueError):
            _F["mh739_pct_wacc"](-0.01, "x")
        with pytest.raises(ValueError):
            _F["mh739_pct_wacc"](50.01, "x")

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_clinker_zero_e_negativo_non_validi(self):
        assert self._val(clinker_t_anno=0.0)["valido"] is False
        assert self._val(clinker_t_anno=-1.0)["valido"] is False

    def test_tasso_zero_valido_in_validazione(self):
        # Range [0, 100]: 0 e' valido qui, ma la
        # guard di calcola lo rende NON_CALCOLABILE.
        assert self._val(tasso_cattura_pct=0.0)["valido"] is True
        assert self._val(tasso_cattura_pct=100.0)["valido"] is True
        assert self._val(tasso_cattura_pct=100.01)["valido"] is False
        assert self._val(tasso_cattura_pct=-0.01)["valido"] is False

    def test_negativi_non_validi(self):
        for k in ("consumo_GJ_per_t",
                  "fattore_comb_kg_per_GJ",
                  "costo_cattura_eur_t",
                  "costo_trasporto_stoccaggio_eur_t",
                  "capex_eur", "prezzo_eua_eur_t"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_vita_zero_e_frazione_non_valide(self):
        assert self._val(vita_anni=0)["valido"] is False
        assert self._val(vita_anni=20.5)["valido"] is False

    def test_wacc_fuori_range_non_validi(self):
        assert self._val(wacc_pct=-0.01)["valido"] is False
        assert self._val(wacc_pct=50.01)["valido"] is False
        assert self._val(wacc_pct=0.0)["valido"] is True
        assert self._val(wacc_pct=50.0)["valido"] is True

    def test_tolleranza_fuori_range_non_valida(self):
        assert self._val(tolleranza_pct=-0.01)["valido"] is False
        assert self._val(tolleranza_pct=100.01)["valido"] is False
        assert self._val(tolleranza_pct=0.0)["valido"] is True
        assert self._val(tolleranza_pct=100.0)["valido"] is True

    def test_nan_non_valido(self):
        assert self._val(clinker_t_anno=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(clinker_t_anno=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(vita_anni=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(clinker_t_anno="500")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(consumo_GJ_per_t=0.0)["valido"] is True
        assert self._val(capex_eur=0.0)["valido"] is True
        assert self._val(prezzo_eua_eur_t=0.0)["valido"] is True
        assert self._val(tolleranza_pct=0.0)["valido"] is True


class TestFunzioni:
    def test_e_processo_demo(self):
        assert _F["mh739_e_processo"](
            1000000.0) == pytest.approx(EP_DEMO, rel=REL)

    def test_e_processo_formula_letterale(self):
        assert _F["mh739_e_processo"](
            500000.0) == pytest.approx(260000.0, rel=REL)

    def test_e_processo_rifiuta_clinker_zero(self):
        with pytest.raises(ValueError):
            _F["mh739_e_processo"](0.0)

    def test_e_comb_demo(self):
        assert _F["mh739_e_comb"](
            1000000.0, 3.5, 95.0) == pytest.approx(
            EC_DEMO, rel=REL)

    def test_e_comb_formula_letterale(self):
        assert _F["mh739_e_comb"](
            200000.0, 4.0, 100.0) == pytest.approx(
            80000.0, rel=REL)

    def test_e_tot_demo(self):
        assert _F["mh739_e_tot"](
            EP_DEMO, EC_DEMO) == pytest.approx(ET_DEMO, rel=REL)

    def test_catturata_demo(self):
        assert _F["mh739_catturata"](
            ET_DEMO, 90.0) == pytest.approx(CATT_DEMO, rel=REL)

    def test_catturata_zero_e_cento(self):
        assert _F["mh739_catturata"](ET_DEMO, 0.0) == 0.0
        assert _F["mh739_catturata"](
            ET_DEMO, 100.0) == pytest.approx(ET_DEMO, rel=REL)

    def test_catturata_rifiuta_tasso_oltre_100(self):
        with pytest.raises(ValueError):
            _F["mh739_catturata"](ET_DEMO, 100.01)

    def test_residua_demo(self):
        assert _F["mh739_residua"](
            ET_DEMO, CATT_DEMO) == pytest.approx(RES_DEMO, rel=REL)

    def test_residua_rifiuta_catturata_oltre_totale(self):
        with pytest.raises(ValueError):
            _F["mh739_residua"](100.0, 101.0)

    def test_crf_demo(self):
        assert _F["mh739_crf"](
            7.0, 20) == pytest.approx(CRF_DEMO, rel=REL)

    def test_crf_wacc_zero_uno_su_n(self):
        assert _F["mh739_crf"](0.0, 20) == pytest.approx(
            0.05, rel=REL)

    def test_crf_formula_indipendente(self):
        r = 0.10
        n = 10
        atteso = r * (1.0 + r) ** n / ((1.0 + r) ** n - 1.0)
        assert _F["mh739_crf"](10.0, 10) == pytest.approx(
            atteso, rel=REL)

    def test_crf_rifiuta_wacc_oltre_50(self):
        with pytest.raises(ValueError):
            _F["mh739_crf"](50.01, 20)

    def test_costo_annuo_demo(self):
        assert _F["mh739_costo_annuo"](
            400000000.0, CRF_DEMO, CATT_DEMO, 60.0,
            25.0) == pytest.approx(COSTO_DEMO, rel=REL)

    def test_evitato_demo(self):
        assert _F["mh739_evitato"](
            CATT_DEMO, 85.0) == pytest.approx(EV_DEMO, rel=REL)

    def test_costo_variabile_demo(self):
        assert _F["mh739_costo_variabile"](
            CATT_DEMO, 60.0, 25.0) == pytest.approx(
            COSTO_VAR_DEMO, rel=REL)

    def test_netto_demo(self):
        # Netto CASSA della demo: evitato -
        # costo variabile (senza CRF) = 0.
        assert _F["mh739_netto"](
            EV_DEMO, COSTO_VAR_DEMO) == pytest.approx(
            NETTO_DEMO, rel=REL)

    def test_netto_puo_essere_negativo(self):
        assert _F["mh739_netto"](
            1000.0, COSTO_DEMO) == pytest.approx(
            1000.0 - COSTO_DEMO, rel=REL)

    def test_flussi_demo(self):
        flussi = _F["mh739_flussi"](400000000.0, NETTO_DEMO, 20)
        assert len(flussi) == 21
        assert flussi[0] == pytest.approx(-400000000.0, rel=REL)
        assert all(f == pytest.approx(NETTO_DEMO, rel=REL)
                   for f in flussi[1:])

    def test_van_demo(self):
        flussi = _F["mh739_flussi"](400000000.0, NETTO_DEMO, 20)
        assert abs(_F["mh739_van"](
            flussi, 7.0) - VAN_DEMO) <= 1.0

    def test_van_tasso_zero(self):
        flussi = _F["mh739_flussi"](400000000.0, NETTO_DEMO, 20)
        atteso = -400000000.0 + NETTO_DEMO * 20
        assert _F["mh739_van"](
            flussi, 0.0) == pytest.approx(atteso, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh739_van"]([100.0, 100.0], -0.01)

    def test_tir_none_flussi_tutti_negativi(self):
        flussi = _F["mh739_flussi"](400000000.0, -1000.0, 20)
        assert _F["mh739_tir"](flussi) is None

    def test_tir_none_tutti_flussi_non_negativi(self):
        assert _F["mh739_tir"](
            [0.0] + [1000.0] * 20) is None

    def test_tir_esiste_caso_semplice_100_120(self):
        assert _F["mh739_tir"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_caso_semplice_1000_500_500_zero(self):
        assert abs(_F["mh739_tir"](
            [-1000.0, 500.0, 500.0])) <= 1e-9

    def test_tir_demo_none(self):
        flussi = _F["mh739_flussi"](400000000.0, NETTO_DEMO, 20)
        assert _F["mh739_tir"](flussi) is None

    def test_payback_demo_none(self):
        flussi = _F["mh739_flussi"](400000000.0, NETTO_DEMO, 20)
        assert _F["mh739_payback"](flussi) is None

    def test_payback_semplice_due(self):
        assert _F["mh739_payback"](
            [-1000.0, 500.0, 500.0, 500.0]) == 2

    def test_payback_zero_se_cumulato_anno_zero_non_negativo(self):
        assert _F["mh739_payback"](
            [0.0, 100.0]) == 0

    def test_payback_none_se_mai(self):
        assert _F["mh739_payback"](
            [-10000000000.0] + [1000.0] * 20) is None

    def test_costo_netto_demo(self):
        assert _F["mh739_costo_netto"](
            COSTO_DEMO, CATT_DEMO) == pytest.approx(
            CN_DEMO, rel=REL)

    def test_costo_netto_none_se_catturata_zero(self):
        assert _F["mh739_costo_netto"](
            COSTO_DEMO, 0.0) is None

    def test_costo_netto_formula_indipendente(self):
        assert _F["mh739_costo_netto"](
            100000.0, 1000.0) == pytest.approx(100.0, rel=REL)

    def test_margine_demo(self):
        assert _F["mh739_margine"](
            85.0, CN_DEMO) == pytest.approx(MARG_DEMO, rel=REL)

    def test_margine_none_se_costo_netto_none(self):
        assert _F["mh739_margine"](85.0, None) is None

    def test_verdetto_demo(self):
        assert _F["mh739_verdetto"](
            VAN_DEMO, 400000000.0, 10.0, CATT_DEMO,
            NETTO_DEMO) == VERDETTO_DEMO

    def test_verdetto_conviente_van_positivo(self):
        assert _F["mh739_verdetto"](
            1000.0, 400000000.0, 10.0, CATT_DEMO,
            NETTO_DEMO) == "CONVIENTE"

    def test_verdetto_van_zero_marginale(self):
        assert _F["mh739_verdetto"](
            0.0, 400000000.0, 10.0, CATT_DEMO,
            NETTO_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh739_verdetto"](
            -0.10 * 400000000.0, 400000000.0, 10.0,
            CATT_DEMO, NETTO_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_oltre_limite(self):
        assert _F["mh739_verdetto"](
            -0.10 * 400000000.0 - 1.0, 400000000.0, 10.0,
            CATT_DEMO, NETTO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_netto_negativo_non_e_non_calcolabile(self):
        assert _F["mh739_verdetto"](
            -1000.0, 400000000.0, 10.0, CATT_DEMO,
            -5000.0) == "MARGINALE"

    def test_verdetto_non_calcolabile_catturata_zero(self):
        assert _F["mh739_verdetto"](
            1000.0, 400000000.0, 10.0, 0.0,
            NETTO_DEMO) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_netto_nan(self):
        assert _F["mh739_verdetto"](
            1000.0, 400000000.0, 10.0, CATT_DEMO,
            float("nan")) == "NON_CALCOLABILE"


class TestDemo:
    def _bc(self, **kw):
        d = _F["mh739_demo"]()
        d.update(kw)
        return _F["mh739_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["e_processo_t"] == pytest.approx(
            EP_DEMO, rel=REL)
        assert c["e_comb_t"] == pytest.approx(
            EC_DEMO, rel=REL)
        assert c["e_tot_t"] == pytest.approx(
            ET_DEMO, rel=REL)
        assert c["co2_catturata_t"] == pytest.approx(
            CATT_DEMO, rel=REL)
        assert c["co2_residua_t"] == pytest.approx(
            RES_DEMO, rel=REL)
        assert c["crf"] == pytest.approx(CRF_DEMO, rel=REL)
        assert c["costo_annuo_eur"] == pytest.approx(
            COSTO_DEMO, rel=REL)
        assert c["evitato_eur"] == pytest.approx(
            EV_DEMO, rel=REL)
        assert c["netto_eur_anno"] == pytest.approx(
            NETTO_DEMO, rel=REL)
        assert abs(c["van"] - VAN_DEMO) <= 1.0
        assert c["tir"] is None
        assert c["payback"] is None
        assert c["costo_netto_eur_per_t"] == pytest.approx(
            CN_DEMO, rel=REL)
        assert c["margine_vs_eua"] == pytest.approx(
            MARG_DEMO, rel=REL)
        assert c["verdetto"] == VERDETTO_DEMO
        assert len(c["flussi"]) == 21

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()["van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()["costo_netto_eur_per_t"] == \
            _F["demo_calcoli"]()["costo_netto_eur_per_t"]

    def test_demo_defaults_contro_costanti_test(self):
        d = _F["mh739_demo"]()
        for k, v in _DEMO.items():
            assert d[k] == v, k
        assert len(d) == 11

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("e_processo_t",
                       "e_comb_t",
                       "e_tot_t",
                       "co2_catturata_t",
                       "co2_residua_t",
                       "crf",
                       "costo_annuo_eur",
                       "evitato_eur",
                       "netto_eur_anno",
                       "van",
                       "tir",
                       "costo_netto_eur_per_t",
                       "margine_vs_eua"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = None" in doc
        assert "verdetto = 'NON_CONVIENTE'" in doc

    def test_prezzo_al_costo_netto_pareggio_van(self):
        # Prezzo EUA = costo netto 134,21103981
        # EUR/t: il netto cassa vale CAPEX x
        # CRF (37.757.170,30 EUR/anno) e la VAN
        # si azzera -> MARGINALE. Il pareggio
        # VAN coincide con il costo netto: il
        # CAPEX compare una sola volta.
        n = self._bc(prezzo_eua_eur_t=CN_DEMO)
        assert n["valid"] is True
        assert n["netto_eur_anno"] == pytest.approx(
            37757170.29730227, rel=REL)
        assert abs(n["van"]) <= 1.0
        assert n["verdetto"] == "MARGINALE"

    def test_prezzo_eua_150_conviente(self):
        # Prezzo EUA 150 EUR/t: netto cassa
        # 49.871.250 EUR/anno, VAN circa
        # +128.336.732,94 EUR -> CONVIENTE.
        n = self._bc(prezzo_eua_eur_t=150.0)
        assert n["valid"] is True
        assert n["netto_eur_anno"] == pytest.approx(
            49871250.0, rel=REL)
        assert n["verdetto"] == "CONVIENTE"
        assert n["van"] > 0.0

    def test_prezzo_eua_200_conviente(self):
        # Prezzo EUA 200 EUR/t: netto cassa
        # 88.233.750 EUR/anno, VAN circa
        # +534.749.604,44 EUR -> CONVIENTE.
        n = self._bc(prezzo_eua_eur_t=200.0)
        assert n["valid"] is True
        assert n["netto_eur_anno"] == pytest.approx(
            88233750.0, rel=REL)
        assert n["verdetto"] == "CONVIENTE"
        assert n["van"] > 0.0

    def test_prezzo_eua_zero_non_conviente(self):
        # Prezzo EUA 0: evitato zero, netto
        # cassa negativo pari a -costo
        # variabile (65.216.250 EUR/anno), VAN
        # negativa oltre tolleranza ->
        # NON_CONVIENTE.
        n = self._bc(prezzo_eua_eur_t=0.0)
        assert n["valid"] is True
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_tasso_50_stesso_netto_costo_netto_piu_alto(self):
        # Tasso 50 %: catturata 426.250 t, costo
        # netto 173,58 EUR/t, ma netto cassa
        # invariato (0): costo variabile = EUA.
        n = self._bc(tasso_cattura_pct=50.0)
        assert n["valid"] is True
        assert n["co2_catturata_t"] == pytest.approx(
            426250.0, rel=REL)
        assert n["costo_netto_eur_per_t"] == pytest.approx(
            173.57987166522528, rel=REL)
        assert n["netto_eur_anno"] == pytest.approx(
            NETTO_DEMO, rel=REL)
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_tasso_100_valido_residua_zero(self):
        n = self._bc(tasso_cattura_pct=100.0)
        assert n["valid"] is True
        assert n["co2_residua_t"] == pytest.approx(
            0.0, abs=1e-9)
        assert n["co2_catturata_t"] == pytest.approx(
            ET_DEMO, rel=REL)

    def test_wacc_zero_valido_crf_uno_su_n(self):
        n = self._bc(wacc_pct=0.0)
        assert n["valid"] is True
        assert n["crf"] == pytest.approx(0.05, rel=REL)

    def test_capex_zero_flussi_nulli(self):
        # CAPEX zero: costo variabile
        # (65.216.250) = evitato, quindi
        # netto 0 e flussi tutti zero. La TIR per
        # bisezione restituisce l'estremo -0,99
        # (NPV identicamente zero all'estremo),
        # il payback vale 0 (cumulato anno 0 = 0),
        # la VAN vale 0 -> MARGINALE (tolleranza
        # 10 % di 0 = 0, |0| <= 0).
        n = self._bc(capex_eur=0.0)
        assert n["valid"] is True
        assert n["capex_eur"] == pytest.approx(0.0, abs=1e-9)
        assert n["netto_eur_anno"] == pytest.approx(
            0.0, abs=1e-9)
        assert n["van"] == pytest.approx(0.0, abs=1e-9)
        assert n["tir"] == pytest.approx(-99.0, rel=REL)
        assert n["payback"] == 0
        assert n["verdetto"] == "MARGINALE"

    def test_clinker_zero_neutro(self):
        n = self._bc(clinker_t_anno=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["costo_netto_eur_per_t"] is None

    def test_tasso_zero_neutro(self):
        n = self._bc(tasso_cattura_pct=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["co2_catturata_t"] == 0.0

    def test_consumo_zero_valido_solo_processo(self):
        n = self._bc(consumo_GJ_per_t=0.0)
        assert n["valid"] is True
        assert n["e_comb_t"] == pytest.approx(0.0, abs=1e-9)
        assert n["e_tot_t"] == pytest.approx(
            EP_DEMO, rel=REL)

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_oltre_50_neutro(self):
        n = self._bc(wacc_pct=50.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_oltre_100_neutro(self):
        n = self._bc(tolleranza_pct=100.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(clinker_t_anno=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["netto_eur_anno"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(clinker_t_anno=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(vita_anni=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_stringa_neutro(self):
        n = self._bc(clinker_t_anno="500")
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_costo_negativo_neutro(self):
        n = self._bc(costo_cattura_eur_t=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh739_neutro"]()
        assert n["valid"] is False
        assert n["errore"] == ""
        assert list(n["df_flussi"].columns) == ["Anno",
                                               "Flusso (EUR/anno)",
                                               "Cumulato (EUR)"]
        assert len(n["df_flussi"]) == 0
        assert list(n["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(n["df_tabella"]) == 0
        assert n["flussi"] == []
        assert n["tir"] is None
        assert n["payback"] is None
        assert n["costo_netto_eur_per_t"] is None
        assert n["margine_vs_eua"] is None
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh739_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "clinker_t_anno",
                       "consumo_GJ_per_t",
                       "fattore_comb_kg_per_GJ",
                       "tasso_cattura_pct",
                       "costo_cattura_eur_t",
                       "costo_trasporto_stoccaggio_eur_t",
                       "capex_eur", "prezzo_eua_eur_t",
                       "wacc_pct", "vita_anni",
                       "tolleranza_pct",
                       "e_processo_t", "e_comb_t",
                       "e_tot_t", "co2_catturata_t",
                       "co2_residua_t", "crf",
                       "costo_annuo_eur", "costo_variabile_eur",
                       "evitato_eur",
                       "netto_eur_anno", "flussi", "van",
                       "tir", "payback",
                       "costo_netto_eur_per_t",
                       "margine_vs_eua", "verdetto",
                       "df_flussi", "df_tabella"):
            assert chiave in n, chiave
        assert n["errore"] == "errore di prova"
        assert n["tir"] is None

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert b["valid"] is True
        assert list(b["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(b["df_tabella"]) == 27
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Emissioni processo (tCO2/anno)" in voci
        assert "Emissioni combustibile (tCO2/anno)" in voci
        assert "Emissioni totali (tCO2/anno)" in voci
        assert "CO2 catturata (tCO2/anno)" in voci
        assert "CO2 residua (tCO2/anno)" in voci
        assert "CRF" in voci
        assert "Costo annuo (EUR/anno)" in voci
        assert "EUA evitate (EUR/anno)" in voci
        assert "VAN (EUR)" in voci
        assert "Costo netto (EUR/tCO2)" in voci
        assert "Margine vs EUA (EUR/tCO2)" in voci
        assert "Verdetto" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (EUR/anno)",
                                               "Cumulato (EUR)"]
        assert len(b["df_flussi"]) == 21
        assert b["df_flussi"]["Flusso (EUR/anno)"].iloc[0] == \
            pytest.approx(-400000000.0, rel=REL)
        assert b["df_flussi"]["Flusso (EUR/anno)"].iloc[1] == \
            pytest.approx(NETTO_DEMO, rel=REL)


class TestCsv:
    def _ing(self):
        return _F["mh739_demo"]()

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh739_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") == 28

    def test_csv_contiene_verdetti_e_costi(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh739_csv"](bc, self._ing())
        assert "verdetto;NON_CONVIENTE" in txt
        assert "capex_eur" in txt
        assert "van_eur" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "costo_netto_eur_per_t" in txt
        assert "margine_vs_eua" in txt
        assert "co2_catturata_t" in txt
        assert "clinker_t_anno" in txt
        assert "costo_annuo_eur" in txt
        assert "e_processo_t" in txt
        assert "e_comb_t" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh739_csv"](bc, self._ing())
        assert f"netto_eur_anno;{bc['netto_eur_anno']}" in txt
        assert f"co2_catturata_t;{bc['co2_catturata_t']}" in txt
        assert "clinker_t_anno;1000000.0" in txt
        assert "costo_cattura_eur_t;60.0" in txt
        assert f"costo_netto_eur_per_t;{bc['costo_netto_eur_per_t']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def739["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def739\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 11, ui_keys
        demo_keys = set(_F["mh739_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh739_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh739_demo():")
        depth = 0
        body = ""
        started = False
        for ch in src[start:]:
            body += ch
            if ch == "{":
                depth += 1
                started = True
            elif ch == "}":
                depth -= 1
                if started and depth == 0:
                    break
        demo_keys = set(re.findall(r'"([A-Za-z0-9_]+)":', body))
        ui_keys = set(re.findall(r'_def739\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W740 (27/10/2026) - tab739' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh739_num", "mh739_nneg", "mh739_pos",
                     "mh739_int_pos", "mh739_pct_0_100",
                     "mh739_pct_wacc",
                     "mh739_e_processo", "mh739_e_comb",
                     "mh739_e_tot", "mh739_catturata",
                     "mh739_residua", "mh739_crf",
                     "mh739_costo_annuo", "mh739_costo_variabile",
                     "mh739_evitato",
                     "mh739_netto", "mh739_flussi",
                     "mh739_van", "mh739_tir",
                     "mh739_payback", "mh739_costo_netto",
                     "mh739_margine", "mh739_verdetto",
                     "mh739_valida", "_mh739_neutro",
                     "mh739_calcola", "mh739_csv",
                     "mh739_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_nessun_residuo_precedente(self):
        # Token del ciclo precedente costruiti per
        # concatenazione, cosi' questo file non li
        # contiene come letterali.
        mh_old = "mh" + "738"
        st_old = "st" + "738"
        tab_old = "tab" + "738"
        w_old = "W" + "739"
        assert mh_old not in _helpers_src()
        assert mh_old not in _ui_src()
        assert st_old not in _ui_src()
        assert tab_old not in _ui_src()
        assert w_old not in _helpers_src()
        assert w_old not in _ui_src()
        assert "mh739" in _helpers_src()
        assert "st739" in _ui_src()

    def test_helpers_parse_ast(self):
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w740_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE739) == 1

    def test_blocco_with_tab739(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab739:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE739

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st739_[A-Za-z0-9_]+)"', _ui_src())
        assert len(keys) == 19, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st739_") for k in keys)

    def test_chiavi_st_input_presenti(self):
        keys = re.findall(r'key="(st739_[A-Za-z0-9_]+)"', _ui_src())
        attese = ["st739_clinker", "st739_consumo",
                  "st739_fattore", "st739_tasso",
                  "st739_costo_cattura", "st739_costo_trasp",
                  "st739_capex", "st739_eua",
                  "st739_wacc", "st739_vita",
                  "st739_tolleranza", "st739_grafico",
                  "st739_show_flussi", "st739_show_tabella",
                  "st739_nota", "st739_ipotesi",
                  "st739_calcola", "st739_csv",
                  "st739_csv_flussi"]
        assert len(attese) == 19
        for k in attese:
            assert k in keys, k

    def test_chiavi_st_niente_fstring_dinamiche(self):
        src = _ui_src()
        assert 'key=f"' not in src
        assert "key=f'" not in src

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg739" in src
        assert "NON_CALCOLABILE" in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg739") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg739")
        assert g < src.index("st.bar_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "CO2 catturata (t/anno)" in src
        assert "Netto (EUR/anno)" in src
        assert "Costo netto (EUR/tCO2)" in src
        assert "VAN (kEUR)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON_CALCOLABILE"):
            assert v in src

    def test_distinzioni_presenti(self):
        src = _ui_src()
        assert "CCS" in src
        assert "clinker" in src
        assert "cemento" in src
        assert "mineralizzazione" in src

    def test_distinzioni_in_header_helpers(self):
        src = _helpers_src()
        assert "CCS" in src
        assert "clinker" in src
        assert "cemento" in src
        assert "mineralizzazione" in src

    def test_nota_didattica_presente(self):
        src = _ui_src()
        assert "NOTA DIDATTICA" in src
        assert "520.000" in src
        assert "767.250" in src

    def test_grafico_bar_chart_presente(self):
        src = _ui_src()
        assert "st.bar_chart" in src
        assert "_dati739" in src
        assert '"EUR/tCO2"' in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh739_csv" in src
        assert "cemento_verde.csv" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st739_show_flussi" in src
        assert "st.checkbox" in src

    def test_niente_nome(self):
        assert "Emanuele" not in _helpers_src()
        assert "Emanuele" not in _ui_src()

    def test_ancora_helper_presente(self):
        assert "# W740 (27/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab739:")
