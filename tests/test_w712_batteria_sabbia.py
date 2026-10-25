"""Test tab712 "🏜️🔥 Batteria a sabbia: il calore rinnovabile stoccato paga?"

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
calore utile 100 MWh_th/ciclo; cicli
200/anno; rendimento di carica 0,95;
frazione utilizzabile 0,90; rendimento
caldaia 0,90; prezzo del gas 80 EUR/MWh;
prezzo elettrico 30 EUR/MWh; costo sabbia
30000 EUR/MWh_th; costo fisso sabbia
200000 EUR; costo fisso caldaia 300000 EUR;
opex sabbia 40000 EUR/anno; opex caldaia
50000 EUR/anno; vita in cicli sabbia 10000;
vita in cicli caldaia 4000; vita di
progetto 20 anni; WACC 0,05 (5 %);
tolleranza 0,10 (10 % del |CAPEX delta|);
fattore gas 0,20 t/MWh; fattore elettrico
0,05 t/MWh.

- cap_nom_mwh = 111.11111111111111
- e_carica_mwh_ciclo = 105.26315789473685
- e_caldaia_mwh_ciclo = 111.11111111111111
- costo_base_eur_a = 1827777.7777777778
- costo_alt_eur_a = 671578.9473684211
- risparmio_eur_a = 1156198.8304093566
- capex_sabbia_eur = 3533333.3333333335
- capex_caldaia_eur = 300000.0
- capex_delta_eur = 3233333.3333333335
- anni_vita_sabbia = 50.0
- anni_vita_caldaia = 20.0
- anni_sost_sabbia = []
- anni_sost_caldaia = []
- co2_evitata_t_a = 3391.8128654970765
- van = 11175459.689026782
- tir = 35.67871611138963
- payback = 3
- verdetto = 'CONVIENTE'

Scomposizione: Cap 100 / 0,90 =
111.11111111111111 MWh_th; CAPEX sabbia
111.11111111111111 x 30000 + 200000 =
3533333.3333333335; CAPEX caldaia 300000;
CAPEX delta 3533333.3333333335 - 300000 =
3233333.3333333335; E_carica 100 / 0,95 =
105.26315789473685 MWh_e/ciclo; E_caldaia
100 / 0,90 = 111.11111111111111 MWh/ciclo;
C_base 200 x 111.11111111111111 x 80 +
50000 = 1827777.7777777778; C_alt 200 x
105.26315789473685 x 30 + 40000 =
671578.9473684211; risparmio
1827777.7777777778 - 671578.9473684211 =
1156198.8304093566; vite 10000 / 200 = 50.0
anni e 4000 / 200 = 20.0 anni: nessuna
sostituzione entro 20 anni (floor 50 e 20,
nessun multiplo sotto 20 per la sabbia e
il multiplo 20 della caldaia e' escluso
perche' uguale alla vita di progetto);
flussi [-3233333.3333333335,
1156198.8304093566 x 20]; VAN
-3233333.3333333335 + 1156198.8304093566
x (1 - 1,05^-20) / 0,05 =
11175459.689026782; TIR 35.67871611138963 %
(il VAN si azzera a quel tasso); payback 3
(cumulato anno 2 = -920935,67 < 0, cumulato
anno 3 = 235263,16 >= 0); VAN >= 0 ->
CONVIENTE. CO2: 200 x (111.11111111111111
x 0,20 - 105.26315789473685 x 0,05) =
3391.8128654970765 t/anno (positiva: il
gas evitato pesa piu' dell'elettricita'
di carica, ma puo' diventare negativa con
elettricita' sporca).
"""

import ast
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w713_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w713_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w713_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w713_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w713_helpers.py: {missing}")
    return out


_F = _load("mh712_num", "mh712_nneg", "mh712_pos",
           "mh712_int_pos", "mh712_int_nneg",
           "mh712_quota_valida", "mh712_eta_valido",
           "mh712_cap_nom", "mh712_capex",
           "mh712_e_carica", "mh712_costo_annuo",
           "mh712_risparmio", "mh712_anni_vita",
           "mh712_anni_sostituzione", "mh712_flussi",
           "mh712_van_flussi", "mh712_tir_flussi",
           "mh712_payback_flussi", "mh712_verdetto",
           "mh712_co2_evitata", "mh712_valida",
           "_mh712_neutro", "mh712_calcola",
           "mh712_sensitivita", "mh712_csv",
           "mh712_demo", "demo_calcoli")

TITLE712 = ("🏜️🔥 Batteria a sabbia: il calore "
            "rinnovabile stoccato paga?")

CAP_DEMO = 111.11111111111111
E_CARICA_DEMO = 105.26315789473685
E_CALDAIA_DEMO = 111.11111111111111
C_BASE_DEMO = 1827777.7777777778
C_ALT_DEMO = 671578.9473684211
RISPARMIO_DEMO = 1156198.8304093566
CX_SABBIA_DEMO = 3533333.3333333335
CX_CALDAIA_DEMO = 300000.0
DELTA_DEMO = 3233333.3333333335
ANNI_VITA_SABBIA_DEMO = 50.0
ANNI_VITA_CALDAIA_DEMO = 20.0
CO2_EV_DEMO = 3391.8128654970765
VAN_DEMO = 11175459.689026782
TIR_DEMO = 35.67871611138963
PAYBACK_DEMO = 3
VITA_DEMO = 20
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w713_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w713_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh712_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh712_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh712_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh712_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh712_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh712_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh712_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh712_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh712_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh712_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh712_int_pos"](200.0, "x") == 200

    def test_int_nneg_accetta_zero(self):
        assert _F["mh712_int_nneg"](0, "x") == 0

    def test_int_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh712_int_nneg"](-1, "x")

    def test_quota_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh712_quota_valida"](-0.1, "x")

    def test_quota_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh712_quota_valida"](1.1, "x")

    def test_quota_accetta_zeri_e_uno(self):
        assert _F["mh712_quota_valida"](0.0, "x") == 0.0
        assert _F["mh712_quota_valida"](1.0, "x") == 1.0

    def test_eta_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh712_eta_valido"](0.0, "x")

    def test_eta_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh712_eta_valido"](1.1, "x")

    def test_eta_accetta_uno(self):
        assert _F["mh712_eta_valido"](1.0, "x") == 1.0


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh712_demo"]()
        d.update(kw)
        return _F["mh712_valida"](**d)

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_q_zero_non_valido(self):
        assert self._val(q_ciclo_mwh_ciclo=0.0)["valido"] is False

    def test_q_negativo_non_valido(self):
        assert self._val(q_ciclo_mwh_ciclo=-1.0)["valido"] is False

    def test_cicli_zero_non_validi(self):
        assert self._val(cicli_anno=0)["valido"] is False

    def test_cicli_non_interi_non_validi(self):
        assert self._val(cicli_anno=199.5)["valido"] is False

    def test_eta_carica_zero_non_valido(self):
        assert self._val(eta_carica=0.0)["valido"] is False

    def test_eta_carica_sopra_uno_non_valido(self):
        assert self._val(eta_carica=1.1)["valido"] is False

    def test_eta_carica_uno_valida(self):
        assert self._val(eta_carica=1.0)["valido"] is True

    def test_f_utilizzo_zero_non_valido(self):
        assert self._val(f_utilizzo=0.0)["valido"] is False

    def test_f_utilizzo_sopra_uno_non_valido(self):
        assert self._val(f_utilizzo=1.1)["valido"] is False

    def test_f_utilizzo_uno_valido(self):
        assert self._val(f_utilizzo=1.0)["valido"] is True

    def test_eta_caldaia_zero_non_valido(self):
        assert self._val(eta_caldaia=0.0)["valido"] is False

    def test_eta_caldaia_sopra_uno_non_valido(self):
        assert self._val(eta_caldaia=1.1)["valido"] is False

    def test_negativi_non_validi(self):
        for k in ("p_gas_eur_mwh", "p_elettrica_eur_mwh",
                  "c_sabbia_eur_mwh", "fisso_sabbia_eur",
                  "fisso_caldaia_eur",
                  "opex_sabbia_eur_a", "opex_caldaia_eur_a",
                  "wacc_frac", "f_gas_t_mwh",
                  "f_elettrica_t_mwh"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_vita_cicli_zero_non_valida(self):
        assert self._val(vita_cicli_sabbia=0)["valido"] is False
        assert self._val(vita_cicli_caldaia=0)["valido"] is False

    def test_vita_cicli_non_intera_non_valida(self):
        assert self._val(vita_cicli_sabbia=9999.5)["valido"] is False

    def test_vita_progetto_zero_non_valida(self):
        assert self._val(vita_progetto_anni=0)["valido"] is False

    def test_vita_progetto_non_intera_non_valida(self):
        assert self._val(vita_progetto_anni=19.5)["valido"] is False

    def test_tolleranza_negativa_non_valida(self):
        assert self._val(tolleranza_frac=-0.01)["valido"] is False

    def test_tolleranza_sopra_uno_non_valida(self):
        assert self._val(tolleranza_frac=1.5)["valido"] is False

    def test_tolleranza_uno_valida(self):
        assert self._val(tolleranza_frac=1.0)["valido"] is True

    def test_wacc_senza_tetto_superiore(self):
        assert self._val(wacc_frac=1.5)["valido"] is True

    def test_nan_non_valido(self):
        assert self._val(eta_carica=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(q_ciclo_mwh_ciclo=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(q_ciclo_mwh_ciclo=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(eta_carica="0.95")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(p_elettrica_eur_mwh=0.0)["valido"] is True
        assert self._val(c_sabbia_eur_mwh=0.0)["valido"] is True
        assert self._val(opex_sabbia_eur_a=0.0)["valido"] is True
        assert self._val(fisso_sabbia_eur=0.0)["valido"] is True


class TestFisicaEconomia:
    def test_cap_nom_demo(self):
        assert _F["mh712_cap_nom"](
            100.0, 0.90) == pytest.approx(CAP_DEMO, rel=REL)

    def test_cap_nom_rifiuta_f_utilizzo_zero(self):
        with pytest.raises(ValueError):
            _F["mh712_cap_nom"](100.0, 0.0)

    def test_capex_sabbia_demo(self):
        assert _F["mh712_capex"](
            CAP_DEMO, 30000.0, 200000.0) == pytest.approx(
            CX_SABBIA_DEMO, rel=REL)

    def test_e_carica_demo(self):
        assert _F["mh712_e_carica"](
            100.0, 0.95) == pytest.approx(E_CARICA_DEMO, rel=REL)

    def test_e_carica_rifiuta_eta_zero(self):
        with pytest.raises(ValueError):
            _F["mh712_e_carica"](100.0, 0.0)

    def test_costo_base_demo(self):
        assert _F["mh712_costo_annuo"](
            200, E_CALDAIA_DEMO, 80.0, 50000.0) == pytest.approx(
            C_BASE_DEMO, rel=REL)

    def test_costo_alt_demo(self):
        assert _F["mh712_costo_annuo"](
            200, E_CARICA_DEMO, 30.0, 40000.0) == pytest.approx(
            C_ALT_DEMO, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh712_risparmio"](
            C_BASE_DEMO, C_ALT_DEMO) == pytest.approx(
            RISPARMIO_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh712_risparmio"](
            10000.0, 15000.0) == pytest.approx(
            -5000.0, rel=REL)

    def test_anni_vita_demo(self):
        assert _F["mh712_anni_vita"](10000, 200) == pytest.approx(
            ANNI_VITA_SABBIA_DEMO, rel=REL)
        assert _F["mh712_anni_vita"](4000, 200) == pytest.approx(
            ANNI_VITA_CALDAIA_DEMO, rel=REL)

    def test_anni_sostituzione_demo_vuoti(self):
        assert _F["mh712_anni_sostituzione"](50.0, 20) == []
        assert _F["mh712_anni_sostituzione"](20.0, 20) == []

    def test_anni_sostituzione_multipli(self):
        assert _F["mh712_anni_sostituzione"](
            1000 / 200, 20) == [5, 10, 15]
        assert _F["mh712_anni_sostituzione"](5.0, 20) == [5, 10, 15]

    def test_anni_sostituzione_sotto_anno_vuota(self):
        assert _F["mh712_anni_sostituzione"](0.5, 20) == []

    def test_anni_sostituzione_esclude_vita_progetto(self):
        assert _F["mh712_anni_sostituzione"](5.0, 20) == [5, 10, 15]

    def test_co2_evitata_demo_positiva(self):
        assert _F["mh712_co2_evitata"](
            200, E_CALDAIA_DEMO, E_CARICA_DEMO,
            0.20, 0.05) == pytest.approx(CO2_EV_DEMO, rel=REL)
        assert CO2_EV_DEMO > 0.0

    def test_co2_evitata_negativa_se_elettricita_sporca(self):
        assert _F["mh712_co2_evitata"](
            200, E_CALDAIA_DEMO, E_CARICA_DEMO,
            0.20, 0.50) == pytest.approx(-6081.87134502924, rel=REL)


class TestFinanza:
    def test_van_flussi_demo(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 20
        assert abs(_F["mh712_van_flussi"](
            flussi, 0.05) - VAN_DEMO) <= 1.0

    def test_van_flussi_formula_chiusa(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 20
        atteso = -DELTA_DEMO + RISPARMIO_DEMO * (
            1.0 - 1.05 ** (-20)) / 0.05
        assert _F["mh712_van_flussi"](
            flussi, 0.05) == pytest.approx(atteso, rel=1e-12)

    def test_van_flussi_tasso_zero(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 20
        assert _F["mh712_van_flussi"](
            flussi, 0.0) == pytest.approx(
            -DELTA_DEMO + RISPARMIO_DEMO * 20, rel=1e-12)

    def test_van_flussi_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh712_van_flussi"]([100.0, 100.0], -0.01)

    def test_flussi_demo_senza_sostituzioni(self):
        flussi = _F["mh712_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CX_CALDAIA_DEMO, CX_SABBIA_DEMO, [], [], 20)
        assert len(flussi) == 21
        assert flussi[0] == pytest.approx(-DELTA_DEMO, rel=REL)
        assert all(f == pytest.approx(RISPARMIO_DEMO, rel=REL)
                   for f in flussi[1:])

    def test_flussi_con_sostituzione_base(self):
        flussi = _F["mh712_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CX_CALDAIA_DEMO, CX_SABBIA_DEMO, [5, 10, 15], [], 20)
        assert flussi[5] == pytest.approx(
            1456198.8304093566, rel=REL)
        assert flussi[10] == pytest.approx(
            1456198.8304093566, rel=REL)
        assert flussi[1] == pytest.approx(RISPARMIO_DEMO, rel=REL)

    def test_flussi_con_sostituzione_entrambi(self):
        flussi = _F["mh712_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CX_CALDAIA_DEMO, CX_SABBIA_DEMO, [5, 10, 15], [10], 20)
        assert flussi[10] == pytest.approx(
            -2077134.5029239766, rel=REL)

    def test_tir_demo_verifica_npv_zero(self):
        tir = _F["mh712_tir_flussi"](
            [-DELTA_DEMO] + [RISPARMIO_DEMO] * 20)
        assert tir is not None
        assert tir * 100.0 == pytest.approx(TIR_DEMO, rel=1e-9)
        npv = -DELTA_DEMO + sum(
            RISPARMIO_DEMO / (1.0 + tir) ** i
            for i in range(1, 21))
        assert abs(npv) <= 1e-6 * DELTA_DEMO

    def test_tir_none_tutti_flussi_non_negativi(self):
        assert _F["mh712_tir_flussi"](
            [0.0] + [RISPARMIO_DEMO] * 20) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh712_tir_flussi"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo_tre(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 20
        assert _F["mh712_payback_flussi"](flussi) == PAYBACK_DEMO

    def test_payback_primo_anno_cumulato_non_negativo(self):
        assert _F["mh712_payback_flussi"](
            [-1000.0, 300.0, 300.0, 300.0, 300.0]) == 4
        assert -1000.0 + 300.0 * 3 < 0.0
        assert -1000.0 + 300.0 * 4 >= 0.0

    def test_payback_none_se_mai(self):
        assert _F["mh712_payback_flussi"](
            [-50000000.0] + [RISPARMIO_DEMO] * 20) is None

    def test_payback_zero_se_cumulato_anno_zero_non_negativo(self):
        assert _F["mh712_payback_flussi"](
            [0.0] + [RISPARMIO_DEMO] * 20) == 0

    def test_verdetto_conviente_demo(self):
        assert _F["mh712_verdetto"](
            VAN_DEMO, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == VERDETTO_DEMO

    def test_verdetto_van_zero_conviente(self):
        assert _F["mh712_verdetto"](
            0.0, DELTA_DEMO, 0.10, RISPARMIO_DEMO) == "CONVIENTE"

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh712_verdetto"](
            -100.0, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh712_verdetto"](
            -323333.0, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh712_verdetto"](
            -323334.0, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_non_positivo(
            self):
        assert _F["mh712_verdetto"](
            1000.0, DELTA_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh712_verdetto"](
            1000.0, DELTA_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_delta_zero_van_positivo_conviente(
            self):
        assert _F["mh712_verdetto"](
            1000.0, 0.0, 0.10, RISPARMIO_DEMO) == "CONVIENTE"

    def test_verdetto_delta_zero_van_negativo_non_conviente(
            self):
        assert _F["mh712_verdetto"](
            -1.0, 0.0, 0.10, RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_delta_zero_mai_marginale(self):
        assert _F["mh712_verdetto"](
            -1.0, 0.0, 0.10, RISPARMIO_DEMO) != "MARGINALE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh712_verdetto"](100.0, DELTA_DEMO, -0.01, RISPARMIO_DEMO)

    def test_verdetto_rifiuta_tolleranza_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh712_verdetto"](100.0, DELTA_DEMO, 1.5, RISPARMIO_DEMO)


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh712_demo"]()
        d.update(kw)
        return _F["mh712_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["cap_nom_mwh"] == pytest.approx(
            CAP_DEMO, rel=REL)
        assert c["e_carica_mwh_ciclo"] == pytest.approx(
            E_CARICA_DEMO, rel=REL)
        assert c["e_caldaia_mwh_ciclo"] == pytest.approx(
            E_CALDAIA_DEMO, rel=REL)
        assert c["costo_base_eur_a"] == pytest.approx(
            C_BASE_DEMO, rel=REL)
        assert c["costo_alt_eur_a"] == pytest.approx(
            C_ALT_DEMO, rel=REL)
        assert c["risparmio_eur_a"] == pytest.approx(
            RISPARMIO_DEMO, rel=REL)
        assert c["capex_sabbia_eur"] == pytest.approx(
            CX_SABBIA_DEMO, rel=REL)
        assert c["capex_caldaia_eur"] == pytest.approx(
            CX_CALDAIA_DEMO, rel=REL)
        assert c["capex_delta_eur"] == pytest.approx(
            DELTA_DEMO, rel=REL)
        assert c["anni_vita_sabbia"] == pytest.approx(
            ANNI_VITA_SABBIA_DEMO, rel=REL)
        assert c["anni_vita_caldaia"] == pytest.approx(
            ANNI_VITA_CALDAIA_DEMO, rel=REL)
        assert c["anni_sost_sabbia"] == []
        assert c["anni_sost_caldaia"] == []
        assert c["co2_evitata_t_a"] == pytest.approx(
            CO2_EV_DEMO, rel=REL)
        assert abs(c["van"] - VAN_DEMO) <= 1.0
        assert c["tir"] == pytest.approx(TIR_DEMO, rel=1e-9)
        assert c["payback"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()[
            "van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()[
            "risparmio_eur_a"] == _F["demo_calcoli"]()[
            "risparmio_eur_a"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        d = _F["mh712_demo"]()
        b = _F["mh712_calcola"](**d)
        coppie = [("cap_nom_mwh", CAP_DEMO),
                  ("e_carica_mwh_ciclo", E_CARICA_DEMO),
                  ("e_caldaia_mwh_ciclo", E_CALDAIA_DEMO),
                  ("costo_base_eur_a", C_BASE_DEMO),
                  ("costo_alt_eur_a", C_ALT_DEMO),
                  ("risparmio_eur_a", RISPARMIO_DEMO),
                  ("capex_sabbia_eur", CX_SABBIA_DEMO),
                  ("capex_caldaia_eur", CX_CALDAIA_DEMO),
                  ("capex_delta_eur", DELTA_DEMO),
                  ("co2_evitata_t_a", CO2_EV_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert abs(b["van"] - VAN_DEMO) <= 1.0
        assert b["tir"] == pytest.approx(TIR_DEMO, rel=1e-9)
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh712_demo"]()
        assert d["q_ciclo_mwh_ciclo"] == 100.0
        assert d["cicli_anno"] == 200
        assert d["eta_carica"] == 0.95
        assert d["f_utilizzo"] == 0.90
        assert d["eta_caldaia"] == 0.90
        assert d["p_gas_eur_mwh"] == 80.0
        assert d["p_elettrica_eur_mwh"] == 30.0
        assert d["c_sabbia_eur_mwh"] == 30000.0
        assert d["fisso_sabbia_eur"] == 200000.0
        assert d["fisso_caldaia_eur"] == 300000.0
        assert d["opex_sabbia_eur_a"] == 40000.0
        assert d["opex_caldaia_eur_a"] == 50000.0
        assert d["vita_cicli_sabbia"] == 10000
        assert d["vita_cicli_caldaia"] == 4000
        assert d["vita_progetto_anni"] == 20
        assert d["wacc_frac"] == 0.05
        assert d["tolleranza_frac"] == 0.10
        assert d["f_gas_t_mwh"] == 0.20
        assert d["f_elettrica_t_mwh"] == 0.05

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("cap_nom_mwh",
                       "e_carica_mwh_ciclo",
                       "e_caldaia_mwh_ciclo",
                       "costo_base_eur_a", "costo_alt_eur_a",
                       "risparmio_eur_a", "capex_sabbia_eur",
                       "capex_caldaia_eur", "capex_delta_eur",
                       "co2_evitata_t_a", "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 3" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_eta_carica_bassa_neutro_risparmio_negativo(self):
        # Eta carica 0,30: E_carica 333,33,
        # C_alt 2040000 > C_base 1827777,78 ->
        # risparmio negativo
        n = self._bc(eta_carica=0.30)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_prezzo_elettrico_alto_neutro(self):
        # Prezzo elettrico 100: C_alt 2095263,16
        # > C_base -> risparmio negativo
        n = self._bc(p_elettrica_eur_mwh=100.0)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_opex_sabbia_alto_riduce_risparmio(self):
        # Opex sabbia 1000000: risparmio
        # 196198,83; VAN -788262,24 ->
        # NON_CONVIENTE; payback 17
        n = self._bc(opex_sabbia_eur_a=1000000.0)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            196198.83040935663, rel=REL)
        assert abs(n["van"] - (-788262.2398116014)) <= 1.0
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["payback"] == 17

    def test_capex_delta_zero_mai_marginale(self):
        # Tutti i costi CAPEX a zero -> delta 0
        n = self._bc(c_sabbia_eur_mwh=0.0, fisso_sabbia_eur=0.0,
                     fisso_caldaia_eur=0.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            0.0, abs=1e-6)
        assert n["verdetto"] == "CONVIENTE"
        assert n["verdetto"] != "MARGINALE"
        assert n["payback"] == 0
        assert n["tir"] is None

    def test_sostituzione_base_solo_caldaia(self):
        # Vita cicli caldaia 1000: 5,0 anni ->
        # sostituzioni 5, 10, 15; sabbia 10000:
        # nessuna. Flusso anno 5 = 1456198,83;
        # VAN 11738996,64 circa
        n = self._bc(vita_cicli_caldaia=1000)
        assert n["valid"] is True
        assert n["anni_sost_caldaia"] == [5, 10, 15]
        assert n["anni_sost_sabbia"] == []
        assert n["df_flussi"]["Flusso (€/anno)"].iloc[5] == \
            pytest.approx(1456198.8304093566, rel=REL)
        assert abs(n["van"] - 11738996.644456837) <= 1.0
        assert n["verdetto"] == "CONVIENTE"

    def test_sostituzione_entrambi(self):
        # Vita cicli sabbia 2000: 10,0 anni ->
        # sostituzione 10; caldaia 1000: 5, 10,
        # 15; flusso anno 10 = -2077134,50;
        # VAN 9569836,48 circa
        n = self._bc(vita_cicli_sabbia=2000, vita_cicli_caldaia=1000)
        assert n["valid"] is True
        assert n["anni_sost_sabbia"] == [10]
        assert n["anni_sost_caldaia"] == [5, 10, 15]
        assert n["df_flussi"]["Flusso (€/anno)"].iloc[10] == \
            pytest.approx(-2077134.5029239766, rel=REL)
        assert abs(n["van"] - 9569836.481946155) <= 1.0

    def test_marginale_orchestratore(self):
        # Costo sabbia 132000 EUR/MWh_th: delta
        # 14566666,67; VAN -157873,64 entro
        # tolleranza 1456666,67 -> MARGINALE;
        # payback 13
        n = self._bc(c_sabbia_eur_mwh=132000.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            14566666.666666668, rel=REL)
        assert abs(n["van"] - (-157873.64430655597)) <= 1.0
        assert n["verdetto"] == "MARGINALE"
        assert n["payback"] == 13

    def test_non_conviente_orchestratore(self):
        # Costo sabbia 150000 EUR/MWh_th: delta
        # 16566666,67; VAN -2157873,64 oltre
        # tolleranza -> NON_CONVIENTE; payback 15
        n = self._bc(c_sabbia_eur_mwh=150000.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            16566666.666666668, rel=REL)
        assert abs(n["van"] - (-2157873.644306553)) <= 1.0
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["payback"] == 15

    def test_f_utilizzo_alto_riduce_cap_nom(self):
        # Frazione 1,0: Cap 100, CAPEX sabbia
        # 3200000, delta 2900000
        n = self._bc(f_utilizzo=1.0)
        assert n["valid"] is True
        assert n["cap_nom_mwh"] == pytest.approx(
            100.0, rel=REL)
        assert n["capex_delta_eur"] == pytest.approx(
            2900000.0, rel=REL)

    def test_eta_zero_neutro(self):
        n = self._bc(eta_carica=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_sopra_uno_neutro(self):
        n = self._bc(eta_carica=1.1)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_q_zero_neutro(self):
        n = self._bc(q_ciclo_mwh_ciclo=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_cicli_non_interi_neutro(self):
        n = self._bc(cicli_anno=199.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_progetto_zero_neutro(self):
        n = self._bc(vita_progetto_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_cicli_zero_neutro(self):
        n = self._bc(vita_cicli_sabbia=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_negativo_neutro(self):
        n = self._bc(wacc_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_sopra_uno_neutro(self):
        n = self._bc(tolleranza_frac=1.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(eta_carica=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(q_ciclo_mwh_ciclo=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(q_ciclo_mwh_ciclo=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_zero_calcolabile_conviente(self):
        # WACC 0: VAN -3233333,33 + 1156198,83
        # x 20 = 19906397,61
        n = self._bc(wacc_frac=0.0)
        assert n["van"] == pytest.approx(
            -DELTA_DEMO + RISPARMIO_DEMO * 20, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh712_neutro"]()
        assert n["valid"] is False
        assert n["errore"] == ""
        assert list(n["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(n["df_flussi"]) == 0
        assert list(n["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(n["df_tabella"]) == 0

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh712_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "q_ciclo_mwh_ciclo", "cicli_anno",
                       "eta_carica", "f_utilizzo",
                       "eta_caldaia",
                       "cap_nom_mwh",
                       "e_carica_mwh_ciclo",
                       "e_caldaia_mwh_ciclo",
                       "costo_base_eur_a",
                       "costo_alt_eur_a",
                       "risparmio_eur_a",
                       "capex_sabbia_eur",
                       "capex_caldaia_eur",
                       "capex_delta_eur",
                       "anni_vita_sabbia",
                       "anni_vita_caldaia",
                       "anni_sost_sabbia",
                       "anni_sost_caldaia",
                       "co2_evitata_t_a",
                       "van", "tir", "payback",
                       "verdetto", "df_flussi",
                       "df_tabella"):
            assert chiave in n, chiave
        assert n["errore"] == "errore di prova"
        assert n["tir"] is None

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert b["valid"] is True
        assert list(b["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(b["df_tabella"]) == 29
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Capacita' nominale sabbia (MWh_th)" in voci
        assert "Energia di carica (MWh_e/ciclo)" in voci
        assert "Energia caldaia (MWh/ciclo)" in voci
        assert "Costo annuo baseline (EUR/anno)" in voci
        assert "Costo annuo alternativa (EUR/anno)" in voci
        assert "Risparmio annuo (EUR/anno)" in voci
        assert "CAPEX delta (EUR)" in voci
        assert "CO2 evitata (t/anno)" in voci
        assert "VAN (EUR)" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(b["df_flussi"]) == VITA_DEMO + 1
        assert b["df_flussi"]["Cumulato (€)"].iloc[-1] == \
            pytest.approx(-DELTA_DEMO + RISPARMIO_DEMO * VITA_DEMO,
                          rel=REL)
        assert b["df_flussi"]["Flusso (€/anno)"].iloc[0] == \
            pytest.approx(-DELTA_DEMO, rel=REL)


class TestSensitivitaCsv:
    def _ing(self):
        return _F["mh712_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh712_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.9", "x1.0", "x1.1"]
        assert list(s.index) == ["x0.9", "x1.0", "x1.1"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh712_sensitivita"](self._ing())
        assert abs(s.loc["x1.0", "x1.0"] - VAN_DEMO) <= 1.0

    def test_sensitivita_crescente_con_rendimento_carica(self):
        s = _F["mh712_sensitivita"](self._ing())
        for colonna in ("x0.9", "x1.0", "x1.1"):
            assert s.loc["x0.9", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.1", colonna]

    def test_sensitivita_decrescente_con_prezzo_elettrico(self):
        s = _F["mh712_sensitivita"](self._ing())
        for riga in ("x0.9", "x1.0", "x1.1"):
            assert s.loc[riga, "x0.9"] > \
                s.loc[riga, "x1.0"] > \
                s.loc[riga, "x1.1"]

    def test_sensitivita_diagonale_uguale_centro(self):
        # Il VAN dipende dal prodotto E_carica x
        # prezzo: sulla diagonale (fattore eta =
        # fattore prezzo) il prodotto e' invariato
        # e il VAN resta quello del centro.
        s = _F["mh712_sensitivita"](self._ing())
        assert abs(s.loc["x0.9", "x0.9"] - VAN_DEMO) <= 1.0
        assert abs(s.loc["x1.1", "x1.1"] - VAN_DEMO) <= 1.0

    def test_sensitivita_nessuna_colonna_degenere(self):
        s = _F["mh712_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_nessuna_colonna_costante(self):
        s = _F["mh712_sensitivita"](self._ing())
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3

    def test_sensitivita_angoli(self):
        s = _F["mh712_sensitivita"](self._ing())
        assert abs(s.loc["x0.9", "x0.9"] - 11175459.689026782) <= 1.0
        assert abs(s.loc["x0.9", "x1.1"] - 9426377.535687836) <= 1.0
        assert abs(s.loc["x1.1", "x0.9"] - 12606526.905395009) <= 1.0
        assert abs(s.loc["x1.1", "x1.1"] - 11175459.689026782) <= 1.0

    def test_sensitivita_con_sostituzioni_ricalcolate(self):
        # Con vita cicli caldaia 1000 la griglia
        # deve includere le sostituzioni: il
        # centro deve coincidere col VAN del
        # caso con sostituzione caldaia
        ing = self._ing()
        ing["vita_cicli_caldaia"] = 1000
        s = _F["mh712_sensitivita"](ing)
        assert abs(s.loc["x1.0", "x1.0"] - 11738996.644456837) <= 1.0

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh712_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 34

    def test_csv_contiene_verdetto_e_risparmio(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh712_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "risparmio_eur_a" in txt
        assert "costo_base_eur_a" in txt
        assert "costo_alt_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "q_ciclo_mwh_ciclo" in txt
        assert "cap_nom_mwh" in txt
        assert "co2_evitata_t_a" in txt
        assert "eta_carica" in txt
        assert "capex_sabbia_eur" in txt
        assert "capex_delta_eur" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh712_csv"](bc, self._ing())
        assert f"risparmio_eur_a;{bc['risparmio_eur_a']}" in txt
        assert f"costo_base_eur_a;{bc['costo_base_eur_a']}" in txt
        assert "q_ciclo_mwh_ciclo;100.0" in txt
        assert "opex_sabbia_eur_a;40000.0" in txt
        assert f"capex_delta_eur;{bc['capex_delta_eur']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def712["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def712\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 19, ui_keys
        demo_keys = set(_F["mh712_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh712_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh712_demo():")
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
        ui_keys = set(re.findall(r'_def712\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W713 (25/10/2026) - tab712' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh712_num", "mh712_nneg", "mh712_pos",
                     "mh712_int_pos", "mh712_int_nneg",
                     "mh712_quota_valida", "mh712_eta_valido",
                     "mh712_cap_nom", "mh712_capex",
                     "mh712_e_carica", "mh712_costo_annuo",
                     "mh712_risparmio", "mh712_anni_vita",
                     "mh712_anni_sostituzione", "mh712_flussi",
                     "mh712_van_flussi", "mh712_tir_flussi",
                     "mh712_payback_flussi", "mh712_verdetto",
                     "mh712_co2_evitata", "mh712_valida",
                     "_mh712_neutro", "mh712_calcola",
                     "mh712_sensitivita", "mh712_csv",
                     "mh712_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_helpers_nessun_residuo_tab_precedente(self):
        # La tab precedente e' la tab711 (sodio-ione):
        # i frammenti nuovi non devono contenere
        # i suoi identificatori.
        assert "mh711" not in _helpers_src()
        assert "tab711" not in _helpers_src()
        assert "mh711" not in _ui_src()
        assert "tab711" not in _ui_src()

    def test_chain_riferimento_tab_precedente(self):
        # Catena: questo file test fa riferimento
        # alla tab precedente tab711 come punto di
        # confronto (test residuo sopra) e la
        # nuova tab e' tab712.
        src = Path(__file__).read_text(encoding="utf-8")
        assert "tab711" in src
        assert "tab712" in src
        assert _ui_src().startswith("    with tab712:")

    def test_helpers_parse_ast(self):
        import textwrap
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w713_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE712) == 1

    def test_blocco_with_tab712(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab712:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE712

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st712_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 24, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st712_") for k in keys)

    def test_chiavi_st_input_sono_20(self):
        """Le 20 chiavi di input/bottone (19 input +
        bottone calcola) sono tutte presenti; le
        altre 4 sono solo chiavi di
        visualizzazione (fig, heatmap, flussi, CSV)."""
        keys = re.findall(r'key="(st712_[a-z0-9_]+)"', _ui_src())
        attese = ["st712_q_ciclo", "st712_cicli",
                  "st712_eta_carica", "st712_f_utilizzo",
                  "st712_eta_caldaia", "st712_p_gas",
                  "st712_p_elettrica", "st712_c_sabbia",
                  "st712_fisso_sabbia", "st712_fisso_caldaia",
                  "st712_opex_sabbia", "st712_opex_caldaia",
                  "st712_vita_cicli_sabbia",
                  "st712_vita_cicli_caldaia", "st712_vita_progetto",
                  "st712_wacc", "st712_tolleranza",
                  "st712_f_gas", "st712_f_elettrica",
                  "st712_calcola"]
        assert len(attese) == 20
        for k in attese:
            assert k in keys, k

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg712" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg712") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg712")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Capacità sabbia (MWh_th)" in src
        assert "Risparmio annuo (€/anno)" in src
        assert "VAN (€)" in src
        assert "CO2 evitata (t/anno)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_ver712" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_distinzioni_presente(self):
        src = _ui_src().lower()
        assert "pcm" in src
        assert "stagionale" in src
        assert "sodio-ione" in src
        assert "negativa" in src
        assert "capex" in src
        assert "surplus" in src

    def test_distinzione_altre_tab_in_helpers(self):
        src = _helpers_src()
        assert "pcm" in src.lower()
        assert "stagionale" in src.lower()
        assert "sodio-ione" in src.lower()

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Costo annuo baseline" in src
        assert "Costo annuo alternativa" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh712_csv" in src
        assert "batteria_sabbia_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh712_sensitivita" in src
        assert "Heatmap" in src
        assert "Rendimento carica" in src
        assert "Prezzo elettrico" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st712_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W713 (25/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab712:")
