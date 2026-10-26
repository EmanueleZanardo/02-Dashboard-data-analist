"""Test tab724 "☀️🗼 Solare a concentrazione (CSP) a torre: l'elettricità dispacciabile dal sole paga?"

Nuova tab tab724 (CSP a torre, w725).
La tab724 replica la semantica economica
delle tab precedenti: flussi [-CAPEX,
margine annuo] piatti, VAN/TIR (bisezione
[-99 %, +500 %], None se margine <= 0 o
nessun cambio di segno incl. tutti flussi
>= 0)/payback (0 se cumulato anno 0 >= 0),
verdetto CONVIENTE (VAN >= 0)/MARGINALE
(VAN < 0 entro toll % del CAPEX;
CAPEX == 0 mai MARGINALE)/NON_CONVIENTE/
NON_CALCOLABILE (validazione fallita o
margine <= 0). Fisica CSP a torre: Q_campo
= A x DNI x eta_ott / 1000; Q_utile =
Q_campo x eta_rec; E_lorda = Q_utile x
eta_ciclo; E_el = min(E_lorda, P_nom x
8760); CF = E_el / (P_nom x 8760).

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
area specchi 500000 m2; DNI 2000
kWh/m2/anno; rendimento ottico 0,70;
rendimento ricevitore 0,85; rendimento
ciclo 0,40; potenza nominale 100 MW;
prezzo 200 EUR/MWh; opex fisso 3000000
EUR/anno; opex variabile 5 EUR/MWh; CAPEX
500000000 EUR; vita 25 anni; WACC 0,06
(6 %); tolleranza 0,10 (10 % del CAPEX);
fattore CO2 0,35 t/MWh.

- q_campo_mwh = 700000.0
- q_utile_mwh = 595000.0
- e_lorda_mwh = 238000.0
- e_el_mwh = 238000.0
- cf_frac = 0.271689497716895
- ricavi_eur_anno = 47600000.0
- costo_annuo_eur_anno = 4190000.0
- margine_annuo_eur_anno = 43410000.0
- co2_evitata_t_anno = 83300.0
- van = 54925490.8304313
- tir = 7.13027762694542
- payback = 12
- verdetto = 'CONVIENTE'

Scomposizione: Q_campo 500000 x 2000 x 0,70
/ 1000 = 700000,0 MWh/anno; Q_utile 700000 x
0,85 = 595000,0 MWh/anno; E_lorda 595000 x
0,40 = 238000,0 MWh/anno; cap 100 x 8760 =
876000,0 MWh/anno (non vincolante: E_el =
238000,0 MWh/anno); CF 238000 / 876000 =
0.271689497716895; ricavi 238000 x 200 =
47600000,0 EUR/anno; costo annuo 3000000 +
5 x 238000 = 4190000,0 EUR/anno; margine
47600000,0 - 4190000,0 = 43410000,0
EUR/anno; flussi: anno 0 -500000000,0, anni
1-25 margine 43410000,0 (piatti); VAN
54925490.8304313 a WACC 6 % su 25 anni;
TIR 7.13027762694542 % (il tasso che azzera
il VAN dei flussi sopra); payback 12 (il
cumulato diventa positivo all'anno 12:
-500000000,0 + 11 x 43410000,0 =
-22510000,0 all'anno 11, poi + 43410000,0 =
20900000,0 all'anno 12); CO2 238000 x 0,35 =
83300,0 t/anno (INFORMATIVA: non entra nel
conto economico); VAN >= 0 -> CONVIENTE.
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
    if (p / "w725_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w725_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w725_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w725_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w725_helpers.py: {missing}")
    return out


_F = _load("mh724_num", "mh724_nneg", "mh724_pos",
           "mh724_int_pos", "mh724_eta_valida",
           "mh724_q_campo", "mh724_q_utile",
           "mh724_e_lorda", "mh724_e_el", "mh724_cf",
           "mh724_ricavi", "mh724_costo_annuo",
           "mh724_margine", "mh724_flussi",
           "mh724_van_flussi", "mh724_tir_flussi",
           "mh724_payback_flussi", "mh724_verdetto",
           "mh724_co2_evitata", "mh724_bilancio",
           "mh724_valida", "_mh724_neutro",
           "mh724_calcola", "mh724_sensitivita",
           "mh724_csv", "mh724_demo", "demo_calcoli")

TITLE724 = ("☀️🗼 Solare a concentrazione (CSP) a torre: "
            "l'elettricità dispacciabile dal sole paga?")

Q_CAMPO_DEMO = 700000.0
Q_UTILE_DEMO = 595000.0
E_LORDA_DEMO = 238000.0
E_EL_DEMO = 238000.0
CF_DEMO = 0.271689497716895
RIC_DEMO = 47600000.0
COSTO_DEMO = 4190000.0
MARGINE_DEMO = 43410000.0
CO2_DEMO = 83300.0
VAN_DEMO = 54925490.8304313
TIR_DEMO = 7.13027762694542
PAYBACK_DEMO = 12
CAPEX_DEMO = 500000000.0
VITA_DEMO = 25
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w725_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w725_ui.py").read_text(encoding="utf-8")


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh724_demo"]()
        d.update(kw)
        return _F["mh724_valida"](**d)

    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh724_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh724_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh724_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh724_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh724_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh724_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh724_pos"](0.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh724_int_pos"](2.5, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh724_int_pos"](25.0, "x") == 25

    def test_eta_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh724_eta_valida"](0.0, "x")

    def test_eta_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh724_eta_valida"](-0.1, "x")

    def test_eta_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh724_eta_valida"](1.01, "x")

    def test_eta_accetta_uno(self):
        assert _F["mh724_eta_valida"](1.0, "x") == 1.0

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_area_zero_non_valida(self):
        assert self._val(area_specchi_m2=0.0)["valido"] is False

    def test_dni_zero_non_valido(self):
        assert self._val(dni_kwh_m2_anno=0.0)["valido"] is False

    def test_eta_zero_non_valide(self):
        for k in ("eta_ottica", "eta_ricevitore", "eta_ciclo"):
            assert self._val(**{k: 0.0})["valido"] is False, k

    def test_eta_sopra_uno_non_valide(self):
        for k in ("eta_ottica", "eta_ricevitore", "eta_ciclo"):
            assert self._val(**{k: 1.5})["valido"] is False, k

    def test_eta_uno_valida(self):
        for k in ("eta_ottica", "eta_ricevitore", "eta_ciclo"):
            assert self._val(**{k: 1.0})["valido"] is True, k

    def test_negativi_non_validi(self):
        for k in ("opex_fisso_eur_anno", "opex_var_eur_mwh",
                  "capex_eur", "wacc_frac", "tolleranza_frac",
                  "fattore_co2_t_mwh"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_p_nom_zero_non_valido(self):
        assert self._val(p_nom_mw=0.0)["valido"] is False

    def test_prezzo_zero_non_valido(self):
        assert self._val(prezzo_eur_mwh=0.0)["valido"] is False

    def test_vita_zero_non_valida(self):
        assert self._val(vita_anni=0)["valido"] is False

    def test_vita_non_intera_non_valida(self):
        assert self._val(vita_anni=25.5)["valido"] is False

    def test_tolleranza_sopra_uno_valida_brief(self):
        assert self._val(tolleranza_frac=1.5)["valido"] is True

    def test_wacc_senza_tetto_superiore(self):
        assert self._val(wacc_frac=1.5)["valido"] is True

    def test_nan_non_valido(self):
        assert self._val(eta_ciclo=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(area_specchi_m2=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(vita_anni=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(eta_ottica="0.70")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(opex_fisso_eur_anno=0.0)["valido"] is True
        assert self._val(opex_var_eur_mwh=0.0)["valido"] is True
        assert self._val(capex_eur=0.0)["valido"] is True
        assert self._val(wacc_frac=0.0)["valido"] is True
        assert self._val(tolleranza_frac=0.0)["valido"] is True
        assert self._val(fattore_co2_t_mwh=0.0)["valido"] is True


class TestFunzioni:
    def test_q_campo_demo(self):
        assert _F["mh724_q_campo"](
            500000.0, 2000.0, 0.70) == pytest.approx(
            Q_CAMPO_DEMO, rel=REL)

    def test_q_utile_demo(self):
        assert _F["mh724_q_utile"](
            Q_CAMPO_DEMO, 0.85) == pytest.approx(
            Q_UTILE_DEMO, rel=REL)

    def test_e_lorda_demo(self):
        assert _F["mh724_e_lorda"](
            Q_UTILE_DEMO, 0.40) == pytest.approx(
            E_LORDA_DEMO, rel=REL)

    def test_e_el_demo_senza_cap(self):
        assert _F["mh724_e_el"](
            E_LORDA_DEMO, 100.0) == pytest.approx(
            E_EL_DEMO, rel=REL)

    def test_e_el_cap_a_p_nom_per_8760(self):
        # Campo 10x: E_lorda 2380000 > cap 876000.
        assert _F["mh724_e_el"](
            2380000.0, 100.0) == pytest.approx(
            876000.0, rel=REL)

    def test_cf_demo(self):
        assert _F["mh724_cf"](
            E_EL_DEMO, 100.0) == pytest.approx(
            CF_DEMO, rel=REL)

    def test_cf_uno_al_cap(self):
        assert _F["mh724_cf"](
            876000.0, 100.0) == pytest.approx(1.0, rel=REL)

    def test_ricavi_demo(self):
        assert _F["mh724_ricavi"](
            E_EL_DEMO, 200.0) == pytest.approx(
            RIC_DEMO, rel=REL)

    def test_costo_annuo_demo(self):
        assert _F["mh724_costo_annuo"](
            3000000.0, 5.0, E_EL_DEMO) == pytest.approx(
            COSTO_DEMO, rel=REL)

    def test_margine_demo(self):
        assert _F["mh724_margine"](
            RIC_DEMO, COSTO_DEMO) == pytest.approx(
            MARGINE_DEMO, rel=REL)

    def test_margine_puo_essere_negativo(self):
        assert _F["mh724_margine"](
            1000000.0, 2000000.0) == pytest.approx(
            -1000000.0, rel=REL)

    def test_flussi_demo_piatti(self):
        flussi = _F["mh724_flussi"](CAPEX_DEMO, MARGINE_DEMO,
                                     VITA_DEMO)
        assert len(flussi) == VITA_DEMO + 1
        assert flussi[0] == pytest.approx(-CAPEX_DEMO, rel=REL)
        assert all(f == pytest.approx(MARGINE_DEMO, rel=REL)
                   for f in flussi[1:])

    def test_van_flussi_demo(self):
        flussi = _F["mh724_flussi"](CAPEX_DEMO, MARGINE_DEMO,
                                     VITA_DEMO)
        assert abs(_F["mh724_van_flussi"](
            flussi, 0.06) - VAN_DEMO) <= 1.0

    def test_van_flussi_tasso_zero(self):
        flussi = _F["mh724_flussi"](CAPEX_DEMO, MARGINE_DEMO,
                                     VITA_DEMO)
        atteso = -CAPEX_DEMO + MARGINE_DEMO * VITA_DEMO
        assert _F["mh724_van_flussi"](
            flussi, 0.0) == pytest.approx(atteso, rel=1e-12)

    def test_van_flussi_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh724_van_flussi"]([100.0, 100.0], -0.01)

    def test_tir_demo(self):
        flussi = _F["mh724_flussi"](CAPEX_DEMO, MARGINE_DEMO,
                                     VITA_DEMO)
        tir = _F["mh724_tir_flussi"](flussi)
        assert tir is not None
        assert tir * 100.0 == pytest.approx(TIR_DEMO, rel=1e-9)

    def test_tir_none_tutti_flussi_non_negativi(self):
        assert _F["mh724_tir_flussi"](
            [0.0] + [MARGINE_DEMO] * 25) is None

    def test_tir_none_nessun_cambio_segno_negativo(self):
        assert _F["mh724_tir_flussi"](
            [-1000.0] + [-100.0] * 10) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh724_tir_flussi"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo_dodici(self):
        flussi = _F["mh724_flussi"](CAPEX_DEMO, MARGINE_DEMO,
                                     VITA_DEMO)
        assert _F["mh724_payback_flussi"](flussi) == PAYBACK_DEMO

    def test_payback_none_se_mai(self):
        assert _F["mh724_payback_flussi"](
            [-2000000000.0] + [MARGINE_DEMO] * 25) is None

    def test_payback_zero_se_cumulato_anno_zero_non_negativo(self):
        assert _F["mh724_payback_flussi"](
            [0.0] + [MARGINE_DEMO] * 25) == 0

    def test_verdetto_conviente_demo(self):
        assert _F["mh724_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10,
            MARGINE_DEMO) == VERDETTO_DEMO

    def test_verdetto_van_zero_conviente(self):
        assert _F["mh724_verdetto"](
            0.0, CAPEX_DEMO, 0.10, MARGINE_DEMO) == "CONVIENTE"

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh724_verdetto"](
            -100.0, CAPEX_DEMO, 0.10,
            MARGINE_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh724_verdetto"](
            -0.10 * CAPEX_DEMO, CAPEX_DEMO, 0.10,
            MARGINE_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_oltre_limite(self):
        assert _F["mh724_verdetto"](
            -0.10 * CAPEX_DEMO - 1.0, CAPEX_DEMO, 0.10,
            MARGINE_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_margine_non_positivo(self):
        assert _F["mh724_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh724_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_positivo_conviente(self):
        assert _F["mh724_verdetto"](
            1000.0, 0.0, 0.10, MARGINE_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(self):
        assert _F["mh724_verdetto"](
            -1.0, 0.0, 0.10, MARGINE_DEMO) == "NON_CONVIENTE"

    def test_verdetto_capex_zero_mai_marginale(self):
        # Con CAPEX == 0 la tolleranza vale zero:
        # nessun VAN < 0 puo' essere MARGINALE.
        for van in (-1.0, -100.0, -1000000.0):
            assert _F["mh724_verdetto"](
                van, 0.0, 0.10, MARGINE_DEMO) == "NON_CONVIENTE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh724_verdetto"](100.0, CAPEX_DEMO, -0.01, MARGINE_DEMO)

    def test_co2_evitata_demo(self):
        assert _F["mh724_co2_evitata"](
            E_EL_DEMO, 0.35) == pytest.approx(CO2_DEMO, rel=REL)

    def test_co2_evitata_zero_se_fattore_zero(self):
        assert _F["mh724_co2_evitata"](
            E_EL_DEMO, 0.0) == pytest.approx(0.0, abs=1e-9)

    def test_bilancio_demo(self):
        df = _F["mh724_bilancio"](Q_CAMPO_DEMO, Q_UTILE_DEMO,
                                   E_LORDA_DEMO, E_EL_DEMO)
        assert list(df.columns) == ["Fase", "Energia (MWh/anno)"]
        assert len(df) == 4
        assert df["Energia (MWh/anno)"].tolist() == pytest.approx(
            [Q_CAMPO_DEMO, Q_UTILE_DEMO, E_LORDA_DEMO,
             E_EL_DEMO], rel=REL)


class TestDemo:
    def _bc(self, **kw):
        d = _F["mh724_demo"]()
        d.update(kw)
        return _F["mh724_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["q_campo_mwh"] == pytest.approx(
            Q_CAMPO_DEMO, rel=REL)
        assert c["q_utile_mwh"] == pytest.approx(
            Q_UTILE_DEMO, rel=REL)
        assert c["e_lorda_mwh"] == pytest.approx(
            E_LORDA_DEMO, rel=REL)
        assert c["e_el_mwh"] == pytest.approx(
            E_EL_DEMO, rel=REL)
        assert c["cf_frac"] == pytest.approx(CF_DEMO, rel=REL)
        assert c["ricavi_eur_anno"] == pytest.approx(
            RIC_DEMO, rel=REL)
        assert c["costo_annuo_eur_anno"] == pytest.approx(
            COSTO_DEMO, rel=REL)
        assert c["margine_annuo_eur_anno"] == pytest.approx(
            MARGINE_DEMO, rel=REL)
        assert c["co2_evitata_t_anno"] == pytest.approx(
            CO2_DEMO, rel=REL)
        assert abs(c["van"] - VAN_DEMO) <= 1.0
        assert abs(c["tir"] - TIR_DEMO) <= 0.01
        assert c["payback"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO
        assert c["flussi"][0] == pytest.approx(-CAPEX_DEMO, rel=REL)
        assert all(f == pytest.approx(MARGINE_DEMO, rel=REL)
                   for f in c["flussi"][1:])
        assert len(c["flussi"]) == VITA_DEMO + 1

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()[
            "van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()[
            "margine_annuo_eur_anno"] == _F["demo_calcoli"]()[
            "margine_annuo_eur_anno"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        d = _F["mh724_demo"]()
        b = _F["mh724_calcola"](**d)
        coppie = [("q_campo_mwh", Q_CAMPO_DEMO),
                  ("q_utile_mwh", Q_UTILE_DEMO),
                  ("e_lorda_mwh", E_LORDA_DEMO),
                  ("e_el_mwh", E_EL_DEMO),
                  ("cf_frac", CF_DEMO),
                  ("ricavi_eur_anno", RIC_DEMO),
                  ("costo_annuo_eur_anno", COSTO_DEMO),
                  ("margine_annuo_eur_anno", MARGINE_DEMO),
                  ("co2_evitata_t_anno", CO2_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert abs(b["van"] - VAN_DEMO) <= 1.0
        assert abs(b["tir"] - TIR_DEMO) <= 0.01
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh724_demo"]()
        assert d["area_specchi_m2"] == 500000.0
        assert d["dni_kwh_m2_anno"] == 2000.0
        assert d["eta_ottica"] == 0.70
        assert d["eta_ricevitore"] == 0.85
        assert d["eta_ciclo"] == 0.40
        assert d["p_nom_mw"] == 100.0
        assert d["prezzo_eur_mwh"] == 200.0
        assert d["opex_fisso_eur_anno"] == 3000000.0
        assert d["opex_var_eur_mwh"] == 5.0
        assert d["capex_eur"] == 500000000.0
        assert d["vita_anni"] == 25
        assert d["wacc_frac"] == 0.06
        assert d["tolleranza_frac"] == 0.10
        assert d["fattore_co2_t_mwh"] == 0.35
        assert len(d) == 14

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("q_campo_mwh", "q_utile_mwh",
                       "e_lorda_mwh", "e_el_mwh", "cf_frac",
                       "ricavi_eur_anno",
                       "costo_annuo_eur_anno",
                       "margine_annuo_eur_anno",
                       "co2_evitata_t_anno", "van"):
            assert repr(c[chiave]) in doc, chiave
        assert f"tir = {repr(c['tir'])}" in doc
        assert "payback = 12" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_prezzo_180_marginale(self):
        # Prezzo 180 EUR/MWh: margine 38650000,
        # VAN -5923284,48, TIR 5,88 %, payback 13
        # -> MARGINALE (|VAN| <= 10 % di CAPEX).
        n = self._bc(prezzo_eur_mwh=180.0)
        assert n["valid"] is True
        assert n["margine_annuo_eur_anno"] == pytest.approx(
            38650000.0, rel=REL)
        assert abs(n["van"] - (-5923284.4829263035)) <= 1.0
        assert abs(n["tir"] - 5.8750000266354006) <= 0.01
        assert n["payback"] == 13
        assert n["verdetto"] == "MARGINALE"

    def test_prezzo_150_non_conviente(self):
        # Prezzo 150 EUR/MWh: margine 31510000,
        # VAN -97196447,45, TIR 3,85 %, payback 16
        # -> NON_CONVIENTE (fuori tolleranza).
        n = self._bc(prezzo_eur_mwh=150.0)
        assert n["valid"] is True
        assert n["margine_annuo_eur_anno"] == pytest.approx(
            31510000.0, rel=REL)
        assert abs(n["van"] - (-97196447.45296268)) <= 1.0
        assert abs(n["tir"] - 3.852815191394539) <= 0.01
        assert n["payback"] == 16
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_prezzo_10_margine_negativo_neutro(self):
        # Prezzo 10 EUR/MWh: ricavi 2380000 <
        # costo 4190000 -> margine negativo ->
        # dict neutro NON_CALCOLABILE.
        n = self._bc(prezzo_eur_mwh=10.0)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["margine_annuo_eur_anno"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_capex_zero_tir_none_payback_zero(self):
        # CAPEX 0: tutti i flussi >= 0 -> TIR None,
        # payback 0, VAN 554925490,83 -> CONVIENTE.
        n = self._bc(capex_eur=0.0)
        assert n["valid"] is True
        assert n["tir"] is None
        assert n["payback"] == 0
        assert abs(n["van"] - 554925490.8304312) <= 1.0
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_enorme_payback_none(self):
        # CAPEX 2000000000: margine x 25 anni =
        # 1085250000 < CAPEX -> payback None, VAN
        # -1445074509,17, TIR -4,24 % ->
        # NON_CONVIENTE.
        n = self._bc(capex_eur=2000000000.0)
        assert n["valid"] is True
        assert n["payback"] is None
        assert abs(n["van"] - (-1445074509.1695688)) <= 1.0
        assert abs(n["tir"] - (-4.2385873915808965)) <= 0.01
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_cap_vincolante_con_campo_grande(self):
        # Area 5000000 m2: E_lorda 2380000 >
        # cap 876000 -> E_el 876000, CF 1,0.
        n = self._bc(area_specchi_m2=5000000.0)
        assert n["valid"] is True
        assert n["e_el_mwh"] == pytest.approx(
            876000.0, rel=REL)
        assert n["cf_frac"] == pytest.approx(1.0, rel=REL)
        assert n["e_lorda_mwh"] == pytest.approx(
            2380000.0, rel=REL)

    def test_area_zero_neutro(self):
        n = self._bc(area_specchi_m2=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_sopra_uno_neutro(self):
        n = self._bc(eta_ciclo=1.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_zero_neutro(self):
        n = self._bc(eta_ottica=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_negativo_neutro(self):
        n = self._bc(wacc_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_negativa_neutro(self):
        n = self._bc(tolleranza_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(eta_ottica=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["margine_annuo_eur_anno"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(area_specchi_m2=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(vita_anni=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_zero_calcolabile(self):
        # WACC 0: VAN = somma flussi =
        # -500000000 + 43410000 x 25 = 585250000.
        n = self._bc(wacc_frac=0.0)
        assert n["van"] == pytest.approx(
            585250000.0, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh724_neutro"]()
        assert n["valid"] is False
        assert n["errore"] == ""
        assert list(n["df_bilancio"].columns) == ["Fase",
                                                 "Energia (MWh/anno)"]
        assert len(n["df_bilancio"]) == 0
        assert list(n["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(n["df_flussi"]) == 0
        assert list(n["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(n["df_tabella"]) == 0
        assert n["flussi"] == []
        assert n["tir"] is None
        assert n["payback"] is None

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh724_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "area_specchi_m2",
                       "dni_kwh_m2_anno", "eta_ottica",
                       "eta_ricevitore", "eta_ciclo",
                       "p_nom_mw", "prezzo_eur_mwh",
                       "opex_fisso_eur_anno",
                       "opex_var_eur_mwh", "capex_eur",
                       "vita_anni", "wacc_frac",
                       "tolleranza_frac",
                       "fattore_co2_t_mwh",
                       "q_campo_mwh", "q_utile_mwh",
                       "e_lorda_mwh", "e_el_mwh",
                       "cf_frac", "ricavi_eur_anno",
                       "costo_annuo_eur_anno",
                       "margine_annuo_eur_anno",
                       "co2_evitata_t_anno", "flussi",
                       "van", "tir", "payback",
                       "verdetto", "df_bilancio",
                       "df_flussi", "df_tabella"):
            assert chiave in n, chiave
        assert n["errore"] == "errore di prova"
        assert n["tir"] is None

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert b["valid"] is True
        assert list(b["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(b["df_tabella"]) == 24
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Area specchi (m2)" in voci
        assert "Q campo (MWh/anno)" in voci
        assert "E elettrica (MWh/anno)" in voci
        assert "Capacity factor" in voci
        assert "Ricavi (EUR/anno)" in voci
        assert "Costo annuo (EUR/anno)" in voci
        assert "Margine annuo (EUR/anno)" in voci
        assert "CO2 evitata (t/anno)" in voci
        assert "VAN (EUR)" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(b["df_flussi"]) == VITA_DEMO + 1
        assert b["df_flussi"]["Flusso (€/anno)"].iloc[0] == \
            pytest.approx(-CAPEX_DEMO, rel=REL)
        assert b["df_flussi"]["Flusso (€/anno)"].iloc[1] == \
            pytest.approx(MARGINE_DEMO, rel=REL)
        assert b["df_flussi"]["Flusso (€/anno)"].iloc[25] == \
            pytest.approx(MARGINE_DEMO, rel=REL)
        assert list(b["df_bilancio"].columns) == ["Fase",
                                                 "Energia (MWh/anno)"]
        assert len(b["df_bilancio"]) == 4


class TestSensitivita:
    def _ing(self):
        return _F["mh724_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh724_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.9", "x1.0", "x1.1"]
        assert list(s.index) == ["x0.9", "x1.0", "x1.1"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh724_sensitivita"](self._ing())
        assert abs(s.loc["x1.0", "x1.0"] - VAN_DEMO) <= 1.0

    def test_sensitivita_crescente_con_prezzo(self):
        s = _F["mh724_sensitivita"](self._ing())
        for riga in ("x0.9", "x1.0", "x1.1"):
            assert s.loc[riga, "x0.9"] < \
                s.loc[riga, "x1.0"] < \
                s.loc[riga, "x1.1"]

    def test_sensitivita_crescente_con_dni(self):
        s = _F["mh724_sensitivita"](self._ing())
        for colonna in ("x0.9", "x1.0", "x1.1"):
            assert s.loc["x0.9", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.1", colonna]

    def test_sensitivita_nessuna_colonna_degenere(self):
        s = _F["mh724_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_nessuna_colonna_costante(self):
        s = _F["mh724_sensitivita"](self._ing())
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3

    def test_sensitivita_angoli(self):
        s = _F["mh724_sensitivita"](self._ing())
        assert abs(s.loc["x0.9", "x0.9"] - (-59165962.88211417)) <= 1.0
        assert abs(s.loc["x0.9", "x1.1"] - 50361832.68192959) <= 1.0
        assert abs(s.loc["x1.1", "x0.9"] - 47319393.91626167) <= 1.0
        assert abs(s.loc["x1.1", "x1.1"] - 181186699.60564852) <= 1.0

    def test_sensitivita_centro_con_vita_corta(self):
        # Con vita 10 anni il centro deve
        # coincidere col VAN del caso con vita
        # 10 anni (flussi piatti, nessun altro
        # effetto).
        ing = self._ing()
        ing["vita_anni"] = 10
        s = _F["mh724_sensitivita"](ing)
        b = _F["mh724_calcola"](**ing)
        assert abs(s.loc["x1.0", "x1.0"] - b["van"]) <= 1.0


class TestCsv:
    def _ing(self):
        return _F["mh724_demo"]()

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh724_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") == 28

    def test_csv_contiene_verdetto_e_margine(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh724_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "margine_annuo_eur_anno" in txt
        assert "ricavi_eur_anno" in txt
        assert "costo_annuo_eur_anno" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "area_specchi_m2" in txt
        assert "q_campo_mwh" in txt
        assert "e_el_mwh" in txt
        assert "co2_evitata_t_anno" in txt
        assert "capex_eur" in txt
        assert "fattore_co2_t_mwh" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh724_csv"](bc, self._ing())
        assert f"margine_annuo_eur_anno;{bc['margine_annuo_eur_anno']}" in txt
        assert f"ricavi_eur_anno;{bc['ricavi_eur_anno']}" in txt
        assert "area_specchi_m2;500000.0" in txt
        assert "opex_fisso_eur_anno;3000000.0" in txt
        assert f"q_campo_mwh;{bc['q_campo_mwh']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def724["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def724\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 14, ui_keys
        demo_keys = set(_F["mh724_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh724_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh724_demo():")
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
        ui_keys = set(re.findall(r'_def724\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W725 (26/10/2026) - tab724' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh724_num", "mh724_nneg", "mh724_pos",
                     "mh724_int_pos", "mh724_eta_valida",
                     "mh724_q_campo", "mh724_q_utile",
                     "mh724_e_lorda", "mh724_e_el", "mh724_cf",
                     "mh724_ricavi", "mh724_costo_annuo",
                     "mh724_margine", "mh724_flussi",
                     "mh724_van_flussi", "mh724_tir_flussi",
                     "mh724_payback_flussi", "mh724_verdetto",
                     "mh724_co2_evitata", "mh724_bilancio",
                     "mh724_valida", "_mh724_neutro",
                     "mh724_calcola", "mh724_sensitivita",
                     "mh724_csv", "mh724_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_nessun_identificatore_futura_tab(self):
        assert "mh725" not in _helpers_src()
        assert "mh725" not in _ui_src()
        assert "st725" not in _ui_src()
        assert "tab725" not in _ui_src()

    def test_helpers_parse_ast(self):
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w725_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE724) == 1

    def test_blocco_with_tab724(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab724:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE724

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st724_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 19, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st724_") for k in keys)

    def test_chiavi_st_input_sono_15(self):
        """Le 15 chiavi di input/bottone (14 input +
        bottone calcola) sono tutte presenti; le
        altre 4 sono solo chiavi di
        visualizzazione (fig, heatmap, flussi, CSV)."""
        keys = re.findall(r'key="(st724_[a-z0-9_]+)"', _ui_src())
        attese = ["st724_area", "st724_dni",
                  "st724_eta_ottica", "st724_eta_ricevitore",
                  "st724_eta_ciclo", "st724_p_nom",
                  "st724_prezzo", "st724_opex_fisso",
                  "st724_opex_var", "st724_capex",
                  "st724_vita", "st724_wacc",
                  "st724_tolleranza", "st724_fattore_co2",
                  "st724_calcola"]
        assert len(attese) == 15
        for k in attese:
            assert k in keys, k

    def test_chiavi_st_niente_fstring_dinamiche(self):
        src = _ui_src()
        assert 'key=f"' not in src
        assert "key=f'" not in src

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg724" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg724") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg724")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Energia annua (MWh/anno)" in src
        assert "Margine annuo (€/anno)" in src
        assert "VAN (€)" in src
        assert "CO2 evitata (t/anno)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_presente(self):
        src = _ui_src().lower()
        assert "fotovoltaico" in src
        assert "acs" in src
        assert "tes" in src
        assert "sali fusi" in src
        assert "dispacciabile" in src

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert '"Campo specchi"' in src
        assert '"Ricevitore"' in src
        assert '"Ciclo"' in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh724_csv" in src
        assert "csp_torre_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh724_sensitivita" in src
        assert "Heatmap" in src
        assert "Fattore DNI" in src
        assert "Fattore prezzo" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st724_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W725 (26/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab724:")
