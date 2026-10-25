"""Test tab696 "⚡🤝 Scambio peer-to-peer: vendere il surplus al vicino conviene?"

Demo calcolata eseguendo demo_calcoli() (non a mano):
surplus 12000 kWh/anno; domanda 10000
kWh/anno; prezzo P2P 0,18 EUR/kWh; prezzo
feed-in 0,08 EUR/kWh; prezzo retail 0,32
EUR/kWh; fee piattaforma 5 %; CAPEX 5000
EUR; OPEX annuo 120 EUR/anno; vita 10
anni; WACC 5 %; tolleranza 10 % del CAPEX.

- energia_scambiata_kwh_a = 10000.0
- ricavo_lordo_eur_a = 1800.0
- fee_eur_a = 90.0
- ricavo_netto_eur_a = 1710.0
- ricavo_alternativo_eur_a = 800.0
- extra_venditore_eur_a = 910.0
- risparmio_acquirente_eur_a = 1400.0000000000002
- beneficio_totale_eur_a = 2310.0
- margine_eur_a = 2190.0
- van = 11910.59949491475
- tir = 42.534461641143515
- payback = 3
- verdetto = 'CONVIENTE'

Scomposizione: scambiata min(12000, 10000)
= 10000; lordo 10000 x 0,18 = 1800; fee
1800 x 0,05 = 90; netto 1800 - 90 = 1710;
alternativo 10000 x 0,08 = 800; extra
1710 - 800 = 910; risparmio 10000 x
(0,32 - 0,18) = 1400; beneficio 910 + 1400
= 2310; margine 2310 - 120 = 2190; CRF 0,05
x 1,05^10 / (1,05^10 - 1) =
0,12950457496545661; VAN -5000 + 2190 x
(1 - 1,05^-10) / 0,05 = 11910,59949491475;
payback: cumulato anno 2 -620, anno 3
+1570 -> 3.
"""

import ast
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w697_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w697_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w697_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w697_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w697_helpers.py: {missing}")
    return out


_F = _load("mh696_num", "mh696_nneg", "mh696_pos",
           "mh696_int_pos", "mh696_pct_range",
           "mh696_energia_scambiata",
           "mh696_ricavo_lordo", "mh696_fee",
           "mh696_ricavo_netto",
           "mh696_ricavo_alternativo",
           "mh696_extra_venditore",
           "mh696_risparmio_acquirente",
           "mh696_beneficio", "mh696_margine",
           "mh696_crf", "mh696_van", "mh696_tir",
           "mh696_payback", "mh696_verdetto",
           "mh696_valida", "_mh696_neutro",
           "mh696_calcola", "mh696_sensitivita",
           "mh696_csv", "mh696_demo", "demo_calcoli")

TITLE696 = ("⚡🤝 Scambio peer-to-peer: "
            "vendere il surplus al vicino conviene?")

E_DEMO = 10000.0
LORDO_DEMO = 1800.0
FEE_DEMO = 90.0
NETTO_DEMO = 1710.0
ALT_DEMO = 800.0
EXTRA_DEMO = 910.0
RISP_DEMO = 1400.0000000000002
BEN_DEMO = 2310.0
MARG_DEMO = 2190.0
VAN_DEMO = 11910.59949491475
TIR_DEMO = 42.534461641143515
PAYBACK_DEMO = 3
VITA_DEMO = 10
VERDETTO_DEMO = "CONVIENTE"
CRF_DEMO = 0.12950457496545661

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w697_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w697_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh696_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh696_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh696_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh696_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh696_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh696_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh696_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh696_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh696_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh696_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh696_int_pos"](10.0, "x") == 10

    def test_pct_range_rifiuta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh696_pct_range"](-0.01, "x")

    def test_pct_range_rifiuta_cento(self):
        with pytest.raises(ValueError):
            _F["mh696_pct_range"](100.0, "x")

    def test_pct_range_accetta_zero(self):
        assert _F["mh696_pct_range"](0.0, "x") == 0.0

    def test_pct_range_accetta_99(self):
        assert _F["mh696_pct_range"](99.9, "x") == 99.9


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh696_demo"]()
        d.update(kw)
        return _F["mh696_valida"](**d)

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_surplus_zero_non_valido(self):
        v = self._val(surplus_venditore_kwh=0.0)
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_surplus_negativo_non_valido(self):
        v = self._val(surplus_venditore_kwh=-1.0)
        assert v["valido"] is False

    def test_domanda_zero_non_valido(self):
        v = self._val(domanda_acquirente_kwh=0.0)
        assert v["valido"] is False

    def test_domanda_negativa_non_valido(self):
        v = self._val(domanda_acquirente_kwh=-5.0)
        assert v["valido"] is False

    def test_prezzo_p2p_zero_non_valido(self):
        v = self._val(prezzo_p2p=0.0)
        assert v["valido"] is False

    def test_prezzo_feedin_zero_non_valido(self):
        v = self._val(prezzo_feedin=0.0)
        assert v["valido"] is False

    def test_prezzo_retail_zero_non_valido(self):
        v = self._val(prezzo_retail=0.0)
        assert v["valido"] is False

    def test_prezzi_negativi_non_validi(self):
        for k in ("prezzo_p2p", "prezzo_feedin", "prezzo_retail"):
            assert self._val(**{k: -0.01})["valido"] is False

    def test_fee_cento_non_valida(self):
        v = self._val(fee_piattaforma_pct=100.0)
        assert v["valido"] is False

    def test_fee_negativa_non_valida(self):
        v = self._val(fee_piattaforma_pct=-1.0)
        assert v["valido"] is False

    def test_wacc_cento_non_valido(self):
        v = self._val(wacc_pct=100.0)
        assert v["valido"] is False

    def test_tolleranza_cento_non_valida(self):
        v = self._val(tolleranza_pct=100.0)
        assert v["valido"] is False

    def test_vita_zero_non_valida(self):
        v = self._val(vita_anni=0)
        assert v["valido"] is False

    def test_vita_non_intera_non_valida(self):
        v = self._val(vita_anni=9.5)
        assert v["valido"] is False

    def test_capex_negativo_non_valido(self):
        v = self._val(capex_eur=-1.0)
        assert v["valido"] is False

    def test_opex_negativo_non_valido(self):
        v = self._val(opex_annuo_eur=-1.0)
        assert v["valido"] is False

    def test_nan_non_valido(self):
        v = self._val(prezzo_p2p=float("nan"))
        assert v["valido"] is False

    def test_inf_non_valido(self):
        v = self._val(surplus_venditore_kwh=float("inf"))
        assert v["valido"] is False

    def test_bool_non_valido(self):
        v = self._val(surplus_venditore_kwh=True)
        assert v["valido"] is False


class TestFisicaEconomia:
    def test_energia_scambiata_min_domanda(self):
        assert _F["mh696_energia_scambiata"](
            12000.0, 10000.0) == pytest.approx(E_DEMO, rel=REL)

    def test_energia_scambiata_min_surplus(self):
        assert _F["mh696_energia_scambiata"](
            8000.0, 10000.0) == 8000.0

    def test_energia_scambiata_uguali(self):
        assert _F["mh696_energia_scambiata"](
            5000.0, 5000.0) == 5000.0

    def test_energia_scambiata_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh696_energia_scambiata"](0.0, 10000.0)
        with pytest.raises(ValueError):
            _F["mh696_energia_scambiata"](12000.0, 0.0)

    def test_ricavo_lordo_demo(self):
        assert _F["mh696_ricavo_lordo"](
            E_DEMO, 0.18) == pytest.approx(LORDO_DEMO, rel=REL)

    def test_fee_demo(self):
        assert _F["mh696_fee"](
            LORDO_DEMO, 5.0) == pytest.approx(FEE_DEMO, rel=REL)

    def test_fee_zero(self):
        assert _F["mh696_fee"](LORDO_DEMO, 0.0) == 0.0

    def test_fee_rifiuta_cento(self):
        with pytest.raises(ValueError):
            _F["mh696_fee"](LORDO_DEMO, 100.0)

    def test_ricavo_netto_demo(self):
        assert _F["mh696_ricavo_netto"](
            LORDO_DEMO, FEE_DEMO) == pytest.approx(
            NETTO_DEMO, rel=REL)

    def test_ricavo_alternativo_demo(self):
        assert _F["mh696_ricavo_alternativo"](
            E_DEMO, 0.08) == pytest.approx(ALT_DEMO, rel=REL)

    def test_extra_demo(self):
        assert _F["mh696_extra_venditore"](
            NETTO_DEMO, ALT_DEMO) == pytest.approx(
            EXTRA_DEMO, rel=REL)

    def test_extra_puo_essere_negativo(self):
        assert _F["mh696_extra_venditore"](
            700.0, 800.0) == -100.0

    def test_risparmio_demo(self):
        assert _F["mh696_risparmio_acquirente"](
            E_DEMO, 0.32, 0.18) == pytest.approx(
            RISP_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh696_risparmio_acquirente"](
            E_DEMO, 0.10, 0.18) == pytest.approx(-800.0, rel=REL)

    def test_beneficio_demo(self):
        assert _F["mh696_beneficio"](
            EXTRA_DEMO, RISP_DEMO) == pytest.approx(
            BEN_DEMO, rel=REL)

    def test_margine_demo(self):
        assert _F["mh696_margine"](
            BEN_DEMO, 120.0) == pytest.approx(MARG_DEMO, rel=REL)

    def test_margine_puo_essere_negativo(self):
        assert _F["mh696_margine"](100.0, 500.0) == -400.0

    def test_crf_demo(self):
        assert _F["mh696_crf"](
            0.05, 10) == pytest.approx(CRF_DEMO, rel=REL)

    def test_crf_wacc_zero(self):
        assert _F["mh696_crf"](0.0, 10) == pytest.approx(
            0.1, rel=1e-12)

    def test_crf_formula_chiusa(self):
        atteso = 0.05 * 1.05 ** 10 / (1.05 ** 10 - 1.0)
        assert _F["mh696_crf"](0.05, 10) == pytest.approx(
            atteso, rel=1e-12)


class TestFinanza:
    def test_van_demo_tolleranza_1_eur(self):
        assert abs(_F["mh696_van"](
            MARG_DEMO, 5000.0, 0.05,
            VITA_DEMO) - VAN_DEMO) <= 1.0

    def test_van_formula_chiusa(self):
        atteso = -5000.0 + MARG_DEMO * (
            1.0 - 1.05 ** (-10)) / 0.05
        assert _F["mh696_van"](
            MARG_DEMO, 5000.0, 0.05,
            VITA_DEMO) == pytest.approx(atteso, rel=1e-12)

    def test_van_tasso_zero(self):
        assert _F["mh696_van"](
            MARG_DEMO, 5000.0, 0.0,
            10) == pytest.approx(
            -5000.0 + MARG_DEMO * 10, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh696_van"](MARG_DEMO, 5000.0, -0.01, 10)

    def test_van_rifiuta_capex_negativo(self):
        with pytest.raises(ValueError):
            _F["mh696_van"](MARG_DEMO, -1.0, 0.05, 10)

    def test_tir_demo_tolleranza_005_punti(self):
        tir_pct = _F["mh696_tir"](
            5000.0, MARG_DEMO, VITA_DEMO) * 100.0
        assert abs(tir_pct - TIR_DEMO) <= 0.05

    def test_tir_none_se_margine_non_positivo(self):
        assert _F["mh696_tir"](5000.0, 0.0, 10) is None
        assert _F["mh696_tir"](5000.0, -100.0, 10) is None

    def test_tir_none_se_capex_zero(self):
        assert _F["mh696_tir"](0.0, MARG_DEMO, 10) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh696_tir"](100.0, 120.0, 1) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_verifica_npv_zero(self):
        tir = _F["mh696_tir"](5000.0, MARG_DEMO, VITA_DEMO)
        npv = -5000.0 + sum(
            MARG_DEMO / (1.0 + tir) ** i
            for i in range(1, 11))
        assert abs(npv) <= 1e-6 * 5000.0

    def test_payback_demo(self):
        assert _F["mh696_payback"](
            5000.0, MARG_DEMO, VITA_DEMO) == PAYBACK_DEMO

    def test_payback_primo_anno_cumulato_non_negativo(self):
        assert -5000.0 + MARG_DEMO * 2 < 0.0
        assert -5000.0 + MARG_DEMO * 3 >= 0.0

    def test_payback_ceil_coerente(self):
        assert _F["mh696_payback"](1000.0, 300.0, 10) == 4

    def test_payback_anno_1_se_margine_ge_capex(self):
        assert _F["mh696_payback"](1000.0, 1000.0, 10) == 1
        assert _F["mh696_payback"](1000.0, 2000.0, 10) == 1

    def test_payback_none_se_mai_entro_vita(self):
        assert _F["mh696_payback"](
            50000000.0, MARG_DEMO, 10) is None

    def test_payback_zero_se_capex_zero(self):
        assert _F["mh696_payback"](0.0, MARG_DEMO, 10) == 0

    def test_payback_none_se_margine_non_positivo(self):
        assert _F["mh696_payback"](5000.0, 0.0, 10) is None

    def test_verdetto_conviente_demo(self):
        assert _F["mh696_verdetto"](
            VAN_DEMO, 5000.0, 0.10,
            MARG_DEMO) == VERDETTO_DEMO

    def test_verdetto_van_zero_conviente(self):
        assert _F["mh696_verdetto"](
            0.0, 5000.0, 0.10, MARG_DEMO) == "CONVIENTE"

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh696_verdetto"](
            -100.0, 5000.0, 0.10, MARG_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh696_verdetto"](
            -500.0, 5000.0, 0.10, MARG_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh696_verdetto"](
            -501.0, 5000.0, 0.10, MARG_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_margine_non_positivo(
            self):
        assert _F["mh696_verdetto"](
            1000.0, 5000.0, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh696_verdetto"](
            1000.0, 5000.0, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_positivo_conviente(
            self):
        assert _F["mh696_verdetto"](
            1000.0, 0.0, 0.10, MARG_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(
            self):
        assert _F["mh696_verdetto"](
            -1.0, 0.0, 0.10, MARG_DEMO) == "NON_CONVIENTE"

    def test_verdetto_capex_zero_mai_marginale(self):
        assert _F["mh696_verdetto"](
            -1.0, 0.0, 0.10, MARG_DEMO) != "MARGINALE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh696_verdetto"](100.0, 5000.0, -0.01, MARG_DEMO)


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh696_demo"]()
        d.update(kw)
        return _F["mh696_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["energia_scambiata_kwh_a"] == pytest.approx(
            E_DEMO, rel=REL)
        assert c["ricavo_lordo_eur_a"] == pytest.approx(
            LORDO_DEMO, rel=REL)
        assert c["fee_eur_a"] == pytest.approx(
            FEE_DEMO, rel=REL)
        assert c["ricavo_netto_eur_a"] == pytest.approx(
            NETTO_DEMO, rel=REL)
        assert c["ricavo_alternativo_eur_a"] == pytest.approx(
            ALT_DEMO, rel=REL)
        assert c["extra_venditore_eur_a"] == pytest.approx(
            EXTRA_DEMO, rel=REL)
        assert c["risparmio_acquirente_eur_a"] == pytest.approx(
            RISP_DEMO, rel=REL)
        assert c["beneficio_totale_eur_a"] == pytest.approx(
            BEN_DEMO, rel=REL)
        assert c["margine_eur_a"] == pytest.approx(
            MARG_DEMO, rel=REL)
        assert abs(c["van"] - VAN_DEMO) <= 1.0
        assert abs(c["tir"] - TIR_DEMO) <= 0.05
        assert c["payback"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()[
            "van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()[
            "margine_eur_a"] == _F["demo_calcoli"]()[
            "margine_eur_a"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        """mh696_calcola(**mh696_demo()) deve matchare le
        costanti _DEMO entro 1e-9 relativo (VAN ±1 EUR,
        TIR ±0,05 punti), chiave per chiave."""
        d = _F["mh696_demo"]()
        b = _F["mh696_calcola"](**d)
        coppie = [("energia_scambiata_kwh_a", E_DEMO),
                  ("ricavo_lordo_eur_a", LORDO_DEMO),
                  ("fee_eur_a", FEE_DEMO),
                  ("ricavo_netto_eur_a", NETTO_DEMO),
                  ("ricavo_alternativo_eur_a", ALT_DEMO),
                  ("extra_venditore_eur_a", EXTRA_DEMO),
                  ("risparmio_acquirente_eur_a", RISP_DEMO),
                  ("beneficio_totale_eur_a", BEN_DEMO),
                  ("margine_eur_a", MARG_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert abs(b["van"] - VAN_DEMO) <= 1.0
        assert abs(b["tir"] - TIR_DEMO) <= 0.05
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh696_demo"]()
        assert d["surplus_venditore_kwh"] == 12000.0
        assert d["domanda_acquirente_kwh"] == 10000.0
        assert d["prezzo_p2p"] == 0.18
        assert d["prezzo_feedin"] == 0.08
        assert d["prezzo_retail"] == 0.32
        assert d["fee_piattaforma_pct"] == 5.0
        assert d["capex_eur"] == 5000.0
        assert d["opex_annuo_eur"] == 120.0
        assert d["vita_anni"] == 10
        assert d["wacc_pct"] == 5.0
        assert d["tolleranza_pct"] == 10.0

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("energia_scambiata_kwh_a",
                       "ricavo_lordo_eur_a",
                       "fee_eur_a",
                       "ricavo_netto_eur_a",
                       "ricavo_alternativo_eur_a",
                       "extra_venditore_eur_a",
                       "risparmio_acquirente_eur_a",
                       "beneficio_totale_eur_a",
                       "margine_eur_a",
                       "van", "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 3" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_surplus_minore_domanda(self):
        # Surplus 8000, domanda 10000: E 8000,
        # lordo 1440, fee 72, netto 1368,
        # alternativo 640, extra 728, risparmio
        # 1120, beneficio 1848, margine 1728
        n = self._bc(surplus_venditore_kwh=8000.0)
        assert n["valid"] is True
        assert n["energia_scambiata_kwh_a"] == pytest.approx(
            8000.0, rel=REL)
        assert n["ricavo_lordo_eur_a"] == pytest.approx(
            1440.0, rel=REL)
        assert n["fee_eur_a"] == pytest.approx(
            72.0, rel=REL)
        assert n["extra_venditore_eur_a"] == pytest.approx(
            728.0, rel=REL)
        assert n["risparmio_acquirente_eur_a"] == pytest.approx(
            1120.0, rel=REL)
        assert n["margine_eur_a"] == pytest.approx(
            1728.0, rel=REL)

    def test_surplus_zero_neutro(self):
        n = self._bc(surplus_venditore_kwh=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["errore"] != ""
        assert n["tir"] is None
        assert n["payback"] is None

    def test_domanda_zero_neutro(self):
        n = self._bc(domanda_acquirente_kwh=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzo_p2p_zero_neutro(self):
        n = self._bc(prezzo_p2p=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_fee_cento_neutro(self):
        n = self._bc(fee_piattaforma_pct=100.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_non_intera_neutro(self):
        n = self._bc(vita_anni=9.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_uno_non_conviente(self):
        # VAN -5000 + 2190 / 1,05 < 0, oltre
        # tolleranza; payback mai
        n = self._bc(vita_anni=1)
        assert n["valid"] is True
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["payback"] is None

    def test_wacc_cento_neutro(self):
        n = self._bc(wacc_pct=100.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_cento_neutro(self):
        n = self._bc(tolleranza_pct=100.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(prezzo_p2p=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["margine_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(surplus_venditore_kwh=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(surplus_venditore_kwh=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_margine_negativo_neutro(self):
        # OPEX annuo enorme: 2310 - 5000 < 0
        n = self._bc(opex_annuo_eur=5000.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["margine_eur_a"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_wacc_zero_calcolabile_conviente(self):
        n = self._bc(wacc_pct=0.0)
        assert n["van"] == pytest.approx(
            -5000.0 + MARG_DEMO * 10, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_zero_conviente_non_marginale(self):
        n = self._bc(capex_eur=0.0)
        assert n["verdetto"] == "CONVIENTE"
        assert n["verdetto"] != "MARGINALE"
        assert n["payback"] == 0
        assert n["tir"] is None

    def test_verdetto_marginale_end_to_end(self):
        # CAPEX 17000: VAN circa -89,40, entro
        # il 10 % di 17000
        n = self._bc(capex_eur=17000.0)
        assert n["van"] == pytest.approx(
            -89.40050508525019, rel=1e-9)
        assert n["van"] < 0.0
        assert abs(n["van"]) <= 0.10 * 17000.0
        assert n["verdetto"] == "MARGINALE"

    def test_verdetto_non_conviente_end_to_end(self):
        # CAPEX 20000: VAN circa -3089,40,
        # oltre il 10 % di 20000
        n = self._bc(capex_eur=20000.0)
        assert n["van"] == pytest.approx(
            -3089.4005050852502, rel=1e-9)
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh696_neutro"]()
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
        n = _F["_mh696_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "energia_scambiata_kwh_a",
                       "ricavo_lordo_eur_a",
                       "fee_eur_a",
                       "ricavo_netto_eur_a",
                       "ricavo_alternativo_eur_a",
                       "extra_venditore_eur_a",
                       "risparmio_acquirente_eur_a",
                       "beneficio_totale_eur_a",
                       "margine_eur_a",
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
        assert len(b["df_tabella"]) == 17
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Energia scambiata (kWh/anno)" in voci
        assert "Ricavo lordo venditore (EUR/anno)" in voci
        assert "Fee piattaforma (EUR/anno)" in voci
        assert "Extra venditore (EUR/anno)" in voci
        assert "Risparmio acquirente (EUR/anno)" in voci
        assert "Beneficio totale (EUR/anno)" in voci
        assert "Margine annuo (EUR/anno)" in voci
        assert "VAN (EUR)" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(b["df_flussi"]) == VITA_DEMO + 1
        assert b["df_flussi"]["Cumulato (€)"].iloc[-1] == \
            pytest.approx(-5000.0 + MARG_DEMO * VITA_DEMO,
                          rel=REL)


class TestSensitivitaCsv:
    def _ing(self):
        return _F["mh696_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh696_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.8", "x1.0", "x1.2"]
        assert list(s.index) == ["x0.8", "x1.0", "x1.2"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh696_sensitivita"](self._ing())
        assert abs(s.loc["x1.0", "x1.0"] - VAN_DEMO) <= 1.0

    def test_sensitivita_decrescente_con_prezzo_p2p(self):
        # VAN CALA con il prezzo P2P: la fee
        # trattiene una fetta del ricavo lordo,
        # quindi l'extra cresce meno di quanto
        # cala il risparmio
        s = _F["mh696_sensitivita"](self._ing())
        for colonna in ("x0.8", "x1.0", "x1.2"):
            assert s.loc["x0.8", colonna] > \
                s.loc["x1.0", colonna] > \
                s.loc["x1.2", colonna]

    def test_sensitivita_crescente_con_energia(self):
        # VAN cresce con l'energia scambiata
        s = _F["mh696_sensitivita"](self._ing())
        for riga in ("x0.8", "x1.0", "x1.2"):
            assert s.loc[riga, "x0.8"] < \
                s.loc[riga, "x1.0"] < \
                s.loc[riga, "x1.2"]

    def test_sensitivita_nessuna_colonna_degenere(self):
        # Il margine resta positivo su tutta la
        # griglia demo, nessuna cella puo' essere
        # 0,0 per regime degenere
        s = _F["mh696_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_assi_variano_davvero(self):
        s = _F["mh696_sensitivita"](self._ing())
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh696_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 24

    def test_csv_contiene_verdetto_e_margine(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh696_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "margine_eur_a" in txt
        assert "extra_venditore_eur_a" in txt
        assert "risparmio_acquirente_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "prezzo_p2p" in txt
        assert "surplus_venditore_kwh" in txt
        assert "energia_scambiata_kwh_a" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh696_csv"](bc, self._ing())
        assert f"ricavo_lordo_eur_a;{LORDO_DEMO}" in txt
        assert f"margine_eur_a;{MARG_DEMO}" in txt
        assert f"fee_eur_a;{FEE_DEMO}" in txt
        assert f"energia_scambiata_kwh_a;{E_DEMO}" in txt
        assert "opex_annuo_eur;120.0" in txt


class TestStruttura:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def696["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def696\["([a-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 11, ui_keys
        demo_keys = set(_F["mh696_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh696_demo
        (mai regex \\{[^}]*\\} sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh696_demo():")
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
        demo_keys = set(re.findall(r'"([a-z0-9_]+)":', body))
        ui_keys = set(re.findall(r'_def696\["([a-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys

    def test_header_helpers_presente(self):
        assert '# W697 (25/10/2026) - tab696' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh696_num", "mh696_nneg", "mh696_pos",
                     "mh696_int_pos", "mh696_pct_range",
                     "mh696_energia_scambiata",
                     "mh696_ricavo_lordo", "mh696_fee",
                     "mh696_ricavo_netto",
                     "mh696_ricavo_alternativo",
                     "mh696_extra_venditore",
                     "mh696_risparmio_acquirente",
                     "mh696_beneficio", "mh696_margine",
                     "mh696_crf", "mh696_van", "mh696_tir",
                     "mh696_payback", "mh696_verdetto",
                     "mh696_valida", "_mh696_neutro",
                     "mh696_calcola", "mh696_sensitivita",
                     "mh696_csv", "mh696_demo",
                     "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_helpers_parse_ast(self):
        import textwrap
        ast.parse(_helpers_src())
        # il frammento UI e' indentato di 4 spazi per
        # l'apply: si dedenta prima del parse,
        # come farebbe l'apply
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w697_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE696) == 1

    def test_blocco_with_tab696(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab696:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE696

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st696_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 16, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st696_") for k in keys)

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg696" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg696") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg696")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Energia scambiata (kWh/anno)" in src
        assert "Extra venditore (€/anno)" in src
        assert "Risparmio acquirente (€/anno)" in src
        assert "VAN (€)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_vd696" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_p2p_presente(self):
        src = _ui_src()
        assert "CER" in src
        assert "scambio sul posto" in src.lower()
        assert "GSE" in src
        assert "fee" in src.lower()
        assert "bilaterale" in src.lower()
        assert "chiuso alle nuove attivazioni" in src

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Extra venditore" in src
        assert "Risparmio acquirente" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh696_csv" in src
        assert "scambio_peer_to_peer_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh696_sensitivita" in src
        assert "Heatmap" in src
        assert "Prezzo P2P" in src
        assert "Energia scambiata" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st696_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W697 (25/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab696:")
        assert "mh696_calcola" in _helpers_src()
        assert "demo_calcoli" in _helpers_src()
        assert "import streamlit" not in _helpers_src()
        assert "tab696" in (_new_dir() / "w697_test.py")\
            .read_text(encoding="utf-8")

    def test_nessun_segreto_nei_file(self):
        for fn in ("w697_helpers.py", "w697_ui.py",
                   "w697_test.py"):
            src = (_new_dir() / fn).read_text(encoding="utf-8")
            assert not re.search(
                r"(?i)(api[_-]?key|secret|password|passwd|token)"
                r"\s*=\s*[\"']",
                src), fn

    def test_nessun_riferimento_alle_tab_precedenti(self):
        src = _ui_src()
        tabs = set(re.findall(r"tab\d+", src))
        assert tabs == {"tab696"}, tabs

    def test_topic_p2p_non_cer(self):
        # Topic corretto: il titolo e' scambio
        # peer-to-peer, non CER
        assert "peer-to-peer" in TITLE696.lower()
        assert "surplus" in TITLE696.lower()
