"""Test tab731 "💧⚡ Mini-idroelettrico ad acqua fluente: il salto del torrente paga?"

Nuova tab tab731 (mini-idroelettrico ad
acqua fluente, w732).
Business case di un mini-impianto
idroelettrico run-of-river: potenza da
portata, salto e rendimento (9,81 kW per
m3/s per m a rendimento 1), energia
annua, CAPEX, O&M, ricavo, netto, VAN,
TIR, payback, LCOE, margine sul prezzo,
CO2 evitata e verdetto.

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
portata 2,0 m3/s; salto 12,0 m;
rendimento 0,82; ore equivalenti 4500
ore/anno; CAPEX 4500 EUR/kW; O&M 30
EUR/kW/anno; prezzo 120 EUR/MWh; fattore
rete 0,35 kg/kWh; WACC 0,05 (5 %); vita 25
anni; tolleranza 0,10 (10 % del CAPEX).

- potenza_kw = 193.0608
- energia_kwh_anno = 868773.6
- capex_eur = 868773.6
- om_eur_anno = 5791.824
- ricavo_eur_anno = 104252.832
- netto_eur_anno = 98461.008
- van = 518930.3886688888
- tir = 10.371969285039249
- payback = 9
- lcoe_eur_mwh = 46.666666666666664
- margine_eur_mwh = 73.33333333333334
- co2_evitata_t_anno = 304.07075999999995
- verdetto = 'CONVIENTE'

Scomposizione: potenza 9,81 x 2,0 x 12,0 x
0,82 = 193,0608 kW; energia 193,0608 x
4500 = 868.773,6 kWh/anno; CAPEX
193,0608 x 4500 = 868.773,6 EUR; O&M
193,0608 x 30 = 5.791,824 EUR/anno;
ricavo 868.773,6 / 1000 x 120 =
104.252,832 EUR/anno; netto 104.252,832 -
5.791,824 = 98.461,008 EUR/anno; flussi:
anno 0 -868.773,6, anni 1-25 netto
98.461,008 (piatti); VAN -868.773,6 +
98.461,008 x 14,093944568759537
(annuita' 25 anni al 5 %) =
518.930,3886688888 EUR; TIR
10,371969285039249 % (il tasso che azzera
il VAN dei flussi); payback 9 (il
cumulato supera lo zero al nono anno:
-868.773,6 + 9 x 98.461,008 =
17.375,472); LCOE (868.773,6 / 25 +
5.791,824) / 868,7736 = 46,666666666666664
EUR/MWh; margine 120 - 46,666666666666664
= 73,33333333333334 EUR/MWh; CO2 evitata
868.773,6 x 0,35 / 1000 = 304,07076
t/anno; verdetto CONVIENTE perche' VAN >
0.
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
    if (p / "w732_helpers.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w732_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w732_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w732_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w732_helpers.py: {missing}")
    return out


_F = _load("mh731_num", "mh731_nneg", "mh731_pos",
           "mh731_int_pos", "mh731_frac_01",
           "mh731_frac_toll", "mh731_pot_kw",
           "mh731_energia", "mh731_capex",
           "mh731_om", "mh731_ricavo",
           "mh731_netto", "mh731_flussi",
           "mh731_van", "mh731_tir", "mh731_payback",
           "mh731_lcoe", "mh731_margine",
           "mh731_co2_evitata", "mh731_verdetto",
           "mh731_valida", "_mh731_neutro",
           "mh731_calcola", "mh731_csv",
           "mh731_demo", "demo_calcoli")

TITLE731 = ("💧⚡ Mini-idroelettrico ad acqua fluente: "
            "il salto del torrente paga?")

POT_DEMO = 193.0608
ENE_DEMO = 868773.6
CAPEX_DEMO = 868773.6
OM_DEMO = 5791.824
RICAVO_DEMO = 104252.832
NETTO_DEMO = 98461.008
VAN_DEMO = 518930.3886688887
TIR_DEMO = 10.371969285039249
PAYBACK_DEMO = 9
LCOE_DEMO = 46.666666666666664
MARGINE_DEMO = 73.33333333333334
CO2_DEMO = 304.07075999999995
VERDETTO_DEMO = "CONVIENTE"

_DEMO = {
    "portata_m3s": 2.0,
    "salto_m": 12.0,
    "rendimento": 0.82,
    "ore_equivalenti": 4500,
    "capex_eur_kw": 4500.0,
    "om_eur_kw_anno": 30.0,
    "prezzo_eur_mwh": 120.0,
    "fattore_rete_kg_kwh": 0.35,
    "wacc_frac": 0.05,
    "vita_anni": 25,
    "tolleranza_frac": 0.10,
}

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w732_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w732_ui.py").read_text(encoding="utf-8")


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh731_demo"]()
        d.update(kw)
        return _F["mh731_valida"](**d)

    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh731_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh731_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh731_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh731_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh731_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh731_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh731_pos"](0.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh731_int_pos"](2.5, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh731_int_pos"](25.0, "x") == 25

    def test_frac_01_rifiuta_zero_e_uno(self):
        with pytest.raises(ValueError):
            _F["mh731_frac_01"](0.0, "x")
        with pytest.raises(ValueError):
            _F["mh731_frac_01"](1.0, "x")

    def test_frac_toll_accetta_zero_rifiuta_uno(self):
        assert _F["mh731_frac_toll"](0.0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh731_frac_toll"](1.0, "x")
        with pytest.raises(ValueError):
            _F["mh731_frac_toll"](-0.01, "x")

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_portata_zero_e_negativa_non_valide(self):
        assert self._val(portata_m3s=0.0)["valido"] is False
        assert self._val(portata_m3s=-1.0)["valido"] is False

    def test_salto_zero_e_negativo_non_validi(self):
        assert self._val(salto_m=0.0)["valido"] is False
        assert self._val(salto_m=-5.0)["valido"] is False

    def test_rendimento_zero_uno_e_oltre_non_validi(self):
        assert self._val(rendimento=0.0)["valido"] is False
        assert self._val(rendimento=1.0)["valido"] is False
        assert self._val(rendimento=1.2)["valido"] is False

    def test_ore_zero_frazione_e_oltre_8760_non_valide(self):
        assert self._val(ore_equivalenti=0)["valido"] is False
        assert self._val(ore_equivalenti=4500.5)["valido"] is False
        assert self._val(ore_equivalenti=8761)["valido"] is False
        assert self._val(ore_equivalenti=8760)["valido"] is True

    def test_negativi_non_validi(self):
        for k in ("capex_eur_kw", "om_eur_kw_anno",
                  "prezzo_eur_mwh", "fattore_rete_kg_kwh"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_vita_zero_e_frazione_non_valide(self):
        assert self._val(vita_anni=0)["valido"] is False
        assert self._val(vita_anni=25.5)["valido"] is False

    def test_wacc_zero_e_uno_non_validi(self):
        assert self._val(wacc_frac=0.0)["valido"] is False
        assert self._val(wacc_frac=1.0)["valido"] is False
        assert self._val(wacc_frac=0.05)["valido"] is True

    def test_tolleranza_uno_non_valida_zero_valida(self):
        assert self._val(tolleranza_frac=1.0)["valido"] is False
        assert self._val(tolleranza_frac=0.0)["valido"] is True

    def test_nan_non_valido(self):
        assert self._val(portata_m3s=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(portata_m3s=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(vita_anni=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(portata_m3s="2.0")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(prezzo_eur_mwh=0.0)["valido"] is True
        assert self._val(capex_eur_kw=0.0)["valido"] is True
        assert self._val(fattore_rete_kg_kwh=0.0)["valido"] is True
        assert self._val(tolleranza_frac=0.0)["valido"] is True


class TestFunzioni:
    def test_potenza_demo(self):
        assert _F["mh731_pot_kw"](
            2.0, 12.0, 0.82) == pytest.approx(
            POT_DEMO, rel=REL)

    def test_potenza_formula_letterale(self):
        assert _F["mh731_pot_kw"](
            1.0, 10.0, 1.0 - 0.15) == pytest.approx(
            9.81 * 1.0 * 10.0 * 0.85, rel=REL)

    def test_potenza_rifiuta_rendimento_uno(self):
        with pytest.raises(ValueError):
            _F["mh731_pot_kw"](2.0, 12.0, 1.0)

    def test_energia_demo(self):
        assert _F["mh731_energia"](
            POT_DEMO, 4500) == pytest.approx(
            ENE_DEMO, rel=REL)

    def test_energia_rifiuta_oltre_8760(self):
        with pytest.raises(ValueError):
            _F["mh731_energia"](POT_DEMO, 8761)

    def test_capex_demo(self):
        assert _F["mh731_capex"](
            POT_DEMO, 4500.0) == pytest.approx(
            CAPEX_DEMO, rel=REL)

    def test_capex_formula_indipendente(self):
        assert _F["mh731_capex"](
            1000.0, 4500.0) == pytest.approx(
            4500000.0, rel=REL)

    def test_om_demo(self):
        assert _F["mh731_om"](
            POT_DEMO, 30.0) == pytest.approx(OM_DEMO, rel=REL)

    def test_ricavo_demo(self):
        assert _F["mh731_ricavo"](
            ENE_DEMO, 120.0) == pytest.approx(
            RICAVO_DEMO, rel=REL)

    def test_netto_demo(self):
        assert _F["mh731_netto"](
            RICAVO_DEMO, OM_DEMO) == pytest.approx(
            NETTO_DEMO, rel=REL)

    def test_netto_puo_essere_negativo(self):
        assert _F["mh731_netto"](
            1000.0, 5791.824) == pytest.approx(
            -4791.824, rel=REL)

    def test_flussi_demo(self):
        flussi = _F["mh731_flussi"](CAPEX_DEMO, NETTO_DEMO, 25)
        assert len(flussi) == 26
        assert flussi[0] == pytest.approx(-CAPEX_DEMO, rel=REL)
        assert all(f == pytest.approx(NETTO_DEMO, rel=REL)
                   for f in flussi[1:])

    def test_van_demo(self):
        flussi = _F["mh731_flussi"](CAPEX_DEMO, NETTO_DEMO, 25)
        assert abs(_F["mh731_van"](
            flussi, 0.05) - VAN_DEMO) <= 1.0

    def test_van_tasso_zero(self):
        flussi = _F["mh731_flussi"](CAPEX_DEMO, NETTO_DEMO, 25)
        atteso = -CAPEX_DEMO + NETTO_DEMO * 25
        assert _F["mh731_van"](
            flussi, 0.0) == pytest.approx(atteso, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh731_van"]([100.0, 100.0], -0.01)

    def test_tir_none_flussi_tutti_negativi(self):
        flussi = _F["mh731_flussi"](CAPEX_DEMO, -1000.0, 25)
        assert _F["mh731_tir"](flussi) is None

    def test_tir_none_tutti_flussi_non_negativi(self):
        assert _F["mh731_tir"](
            [0.0] + [NETTO_DEMO] * 25) is None

    def test_tir_none_nessun_cambio_segno_negativo(self):
        assert _F["mh731_tir"](
            [-1000.0] + [-100.0] * 10) is None

    def test_tir_esiste_caso_semplice_100_120(self):
        assert _F["mh731_tir"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_caso_semplice_1000_500_500_zero(self):
        assert abs(_F["mh731_tir"](
            [-1000.0, 500.0, 500.0])) <= 1e-9

    def test_tir_demo(self):
        flussi = _F["mh731_flussi"](CAPEX_DEMO, NETTO_DEMO, 25)
        tir = _F["mh731_tir"](flussi)
        assert tir is not None
        assert tir * 100.0 == pytest.approx(TIR_DEMO, rel=1e-9)

    def test_payback_demo(self):
        flussi = _F["mh731_flussi"](CAPEX_DEMO, NETTO_DEMO, 25)
        assert _F["mh731_payback"](flussi) == PAYBACK_DEMO

    def test_payback_semplice_due(self):
        assert _F["mh731_payback"](
            [-1000.0, 500.0, 500.0, 500.0]) == 2

    def test_payback_zero_se_cumulato_anno_zero_non_negativo(self):
        assert _F["mh731_payback"](
            [0.0, 100.0]) == 0

    def test_payback_none_se_mai(self):
        assert _F["mh731_payback"](
            [-1000000000.0] + [NETTO_DEMO] * 25) is None

    def test_lcoe_demo(self):
        assert _F["mh731_lcoe"](
            CAPEX_DEMO, 25, OM_DEMO,
            ENE_DEMO) == pytest.approx(LCOE_DEMO, rel=REL)

    def test_lcoe_none_se_energia_zero(self):
        assert _F["mh731_lcoe"](
            1000.0, 10, 100.0, 0.0) is None

    def test_lcoe_formula_indipendente(self):
        assert _F["mh731_lcoe"](
            120000.0, 10, 5000.0,
            1000000.0) == pytest.approx(
            (12000.0 + 5000.0) / 1000.0, rel=REL)

    def test_margine_demo(self):
        assert _F["mh731_margine"](
            120.0, LCOE_DEMO) == pytest.approx(
            MARGINE_DEMO, rel=REL)

    def test_margine_none_se_lcoe_none(self):
        assert _F["mh731_margine"](120.0, None) is None

    def test_co2_demo(self):
        assert _F["mh731_co2_evitata"](
            ENE_DEMO, 0.35) == pytest.approx(CO2_DEMO, rel=REL)

    def test_co2_fattore_zero(self):
        assert _F["mh731_co2_evitata"](
            ENE_DEMO, 0.0) == pytest.approx(0.0, abs=1e-9)

    def test_verdetto_demo(self):
        assert _F["mh731_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10, ENE_DEMO,
            NETTO_DEMO) == VERDETTO_DEMO

    def test_verdetto_conviente_van_positivo(self):
        assert _F["mh731_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, ENE_DEMO,
            NETTO_DEMO) == "CONVIENTE"

    def test_verdetto_van_zero_marginale(self):
        assert _F["mh731_verdetto"](
            0.0, CAPEX_DEMO, 0.10, ENE_DEMO,
            NETTO_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh731_verdetto"](
            -0.10 * CAPEX_DEMO, CAPEX_DEMO, 0.10,
            ENE_DEMO, NETTO_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_oltre_limite(self):
        assert _F["mh731_verdetto"](
            -0.10 * CAPEX_DEMO - 1.0, CAPEX_DEMO, 0.10,
            ENE_DEMO, NETTO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_netto_negativo_non_e_non_calcolabile(self):
        assert _F["mh731_verdetto"](
            -1000.0, CAPEX_DEMO, 0.10, ENE_DEMO,
            -5000.0) == "MARGINALE"

    def test_verdetto_non_calcolabile_energia_zero(self):
        assert _F["mh731_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0,
            NETTO_DEMO) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_netto_nan(self):
        assert _F["mh731_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, ENE_DEMO,
            float("nan")) == "NON_CALCOLABILE"


class TestDemo:
    def _bc(self, **kw):
        d = _F["mh731_demo"]()
        d.update(kw)
        return _F["mh731_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["potenza_kw"] == pytest.approx(
            POT_DEMO, rel=REL)
        assert c["energia_kwh_anno"] == pytest.approx(
            ENE_DEMO, rel=REL)
        assert c["capex_eur"] == pytest.approx(
            CAPEX_DEMO, rel=REL)
        assert c["om_eur_anno"] == pytest.approx(
            OM_DEMO, rel=REL)
        assert c["ricavo_eur_anno"] == pytest.approx(
            RICAVO_DEMO, rel=REL)
        assert c["netto_eur_anno"] == pytest.approx(
            NETTO_DEMO, rel=REL)
        assert abs(c["van"] - VAN_DEMO) <= 1.0
        assert abs(c["tir"] - TIR_DEMO) <= 0.01
        assert c["payback"] == PAYBACK_DEMO
        assert c["lcoe_eur_mwh"] == pytest.approx(
            LCOE_DEMO, rel=REL)
        assert c["margine_eur_mwh"] == pytest.approx(
            MARGINE_DEMO, rel=REL)
        assert c["co2_evitata_t_anno"] == pytest.approx(
            CO2_DEMO, rel=REL)
        assert c["verdetto"] == VERDETTO_DEMO
        assert len(c["flussi"]) == 26

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()["van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()["lcoe_eur_mwh"] == \
            _F["demo_calcoli"]()["lcoe_eur_mwh"]

    def test_demo_defaults_contro_costanti_test(self):
        d = _F["mh731_demo"]()
        for k, v in _DEMO.items():
            assert d[k] == v, k
        assert len(d) == 11

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("potenza_kw",
                       "energia_kwh_anno",
                       "capex_eur",
                       "om_eur_anno",
                       "ricavo_eur_anno",
                       "netto_eur_anno",
                       "van",
                       "tir",
                       "lcoe_eur_mwh",
                       "margine_eur_mwh",
                       "co2_evitata_t_anno"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 9" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_prezzo_77_marginale(self):
        # Prezzo 77 EUR/MWh: netto 61.103,7432
        # EUR/anno, VAN circa -7.580,83 EUR,
        # entro la tolleranza 10 % di
        # 868.773,6 = 86.877,36 -> MARGINALE.
        n = self._bc(prezzo_eur_mwh=77.0)
        assert n["valid"] is True
        assert n["verdetto"] == "MARGINALE"
        assert -86877.36 < n["van"] < 0.0

    def test_prezzo_70_non_conviente(self):
        # Prezzo 70 EUR/MWh: netto 55.022,328
        # EUR/anno, VAN circa -93.291,96 EUR,
        # oltre la tolleranza 86.877,36 EUR
        # -> NON_CONVIENTE.
        n = self._bc(prezzo_eur_mwh=70.0)
        assert n["valid"] is True
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["van"] < -86877.36

    def test_prezzo_zero_non_conviente(self):
        # Prezzo 0: ricavo zero, netto negativo
        # pari a -O&M, VAN negativa oltre
        # tolleranza -> NON_CONVIENTE.
        n = self._bc(prezzo_eur_mwh=0.0)
        assert n["valid"] is True
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_capex_zero_tir_none_payback_zero(self):
        # CAPEX zero e prezzo 120: tutti i flussi
        # >= 0 -> TIR None, payback 0, VAN
        # positiva -> CONVIENTE.
        n = self._bc(capex_eur_kw=0.0)
        assert n["valid"] is True
        assert n["capex_eur"] == pytest.approx(0.0, abs=1e-9)
        assert n["tir"] is None
        assert n["payback"] == 0
        assert n["verdetto"] == "CONVIENTE"

    def test_portata_zero_neutro(self):
        n = self._bc(portata_m3s=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["lcoe_eur_mwh"] is None

    def test_salto_zero_neutro(self):
        n = self._bc(salto_m=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_rendimento_uno_neutro(self):
        n = self._bc(rendimento=1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_rendimento_zero_neutro(self):
        n = self._bc(rendimento=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_ore_oltre_8760_neutro(self):
        n = self._bc(ore_equivalenti=8761)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_ore_zero_neutro(self):
        n = self._bc(ore_equivalenti=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_zero_e_uno_neutri(self):
        assert self._bc(wacc_frac=0.0)["verdetto"] == "NON_CALCOLABILE"
        assert self._bc(wacc_frac=1.0)["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_uno_neutro(self):
        n = self._bc(tolleranza_frac=1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(portata_m3s=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["netto_eur_anno"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(portata_m3s=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(vita_anni=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_stringa_neutro(self):
        n = self._bc(portata_m3s="2.0")
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_capex_negativo_neutro(self):
        n = self._bc(capex_eur_kw=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh731_neutro"]()
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
        assert n["lcoe_eur_mwh"] is None
        assert n["margine_eur_mwh"] is None
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh731_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "portata_m3s", "salto_m",
                       "rendimento", "ore_equivalenti",
                       "capex_eur_kw", "om_eur_kw_anno",
                       "prezzo_eur_mwh",
                       "fattore_rete_kg_kwh",
                       "wacc_frac", "vita_anni",
                       "tolleranza_frac",
                       "potenza_kw", "energia_kwh_anno",
                       "capex_eur", "om_eur_anno",
                       "ricavo_eur_anno",
                       "netto_eur_anno", "flussi", "van",
                       "tir", "payback", "lcoe_eur_mwh",
                       "margine_eur_mwh",
                       "co2_evitata_t_anno", "verdetto",
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
        assert "Energia (kWh/anno)" in voci
        assert "VAN (EUR)" in voci
        assert "LCOE (EUR/MWh)" in voci
        assert "Margine (EUR/MWh)" in voci
        assert "CO2 evitata (t/anno)" in voci
        assert "Verdetto" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (EUR/anno)",
                                               "Cumulato (EUR)"]
        assert len(b["df_flussi"]) == 26
        assert b["df_flussi"]["Flusso (EUR/anno)"].iloc[0] == \
            pytest.approx(-CAPEX_DEMO, rel=REL)
        assert b["df_flussi"]["Flusso (EUR/anno)"].iloc[1] == \
            pytest.approx(NETTO_DEMO, rel=REL)


class TestCsv:
    def _ing(self):
        return _F["mh731_demo"]()

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh731_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") == 25

    def test_csv_contiene_verdetti_e_costi(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh731_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "capex_eur" in txt
        assert "van_eur" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "lcoe_eur_mwh" in txt
        assert "margine_eur_mwh" in txt
        assert "co2_evitata_t_anno" in txt
        assert "portata_m3s" in txt
        assert "energia_kwh_anno" in txt
        assert "potenza_kw" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh731_csv"](bc, self._ing())
        assert f"netto_eur_anno;{bc['netto_eur_anno']}" in txt
        assert f"energia_kwh_anno;{bc['energia_kwh_anno']}" in txt
        assert "portata_m3s;2.0" in txt
        assert "capex_eur_kw;4500.0" in txt
        assert f"lcoe_eur_mwh;{bc['lcoe_eur_mwh']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def731["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def731\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 11, ui_keys
        demo_keys = set(_F["mh731_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh731_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh731_demo():")
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
        ui_keys = set(re.findall(r'_def731\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W732 (26/10/2026) - tab731' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh731_num", "mh731_nneg", "mh731_pos",
                     "mh731_int_pos", "mh731_frac_01",
                     "mh731_frac_toll", "mh731_pot_kw",
                     "mh731_energia", "mh731_capex",
                     "mh731_om", "mh731_ricavo",
                     "mh731_netto", "mh731_flussi",
                     "mh731_van", "mh731_tir",
                     "mh731_payback", "mh731_lcoe",
                     "mh731_margine", "mh731_co2_evitata",
                     "mh731_verdetto", "mh731_valida",
                     "_mh731_neutro", "mh731_calcola",
                     "mh731_csv", "mh731_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_nessun_residuo_730(self):
        assert "mh730" not in _helpers_src()
        assert "mh730" not in _ui_src()
        assert "st730" not in _ui_src()
        assert "tab730" not in _ui_src()
        assert "W731" not in _helpers_src()
        assert "W731" not in _ui_src()
        assert "mh731" in _helpers_src()
        assert "st731" in _ui_src()

    def test_helpers_parse_ast(self):
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w732_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE731) == 1

    def test_blocco_with_tab731(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab731:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE731

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st731_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 14, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st731_") for k in keys)

    def test_chiavi_st_input_presenti(self):
        keys = re.findall(r'key="(st731_[a-z0-9_]+)"', _ui_src())
        attese = ["st731_portata", "st731_salto",
                  "st731_rendimento", "st731_ore",
                  "st731_capex", "st731_om",
                  "st731_prezzo", "st731_fattore",
                  "st731_vita", "st731_wacc",
                  "st731_tolleranza", "st731_calcola"]
        assert len(attese) == 12
        for k in attese:
            assert k in keys, k

    def test_chiavi_st_niente_fstring_dinamiche(self):
        src = _ui_src()
        assert 'key=f"' not in src
        assert "key=f'" not in src

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg731" in src
        assert "NON_CALCOLABILE" in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg731") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg731")
        assert g < src.index("st.bar_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "LCOE (EUR/MWh)" in src
        assert "Margine (EUR/MWh)" in src
        assert "VAN (EUR)" in src
        assert "Payback (anni)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON_CALCOLABILE"):
            assert v in src

    def test_distinzioni_presenti(self):
        src = _ui_src()
        assert "idroelettrico a bacino" in src
        assert "pompaggio" in src
        assert "eolico" in src
        assert "fotovoltaico" in src
        assert "biomasse" in src

    def test_distinzioni_in_header_helpers(self):
        src = _helpers_src()
        assert "idroelettrico a bacino" in src
        assert "pompaggio" in src
        assert "eolico" in src
        assert "fotovoltaico" in src
        assert "biomasse" in src

    def test_nota_didattica_presente(self):
        src = _ui_src()
        assert "NOTA DIDATTICA" in src
        assert "868.773,6" in src
        assert "193,0608" in src

    def test_grafico_bar_chart_presente(self):
        src = _ui_src()
        assert "st.bar_chart" in src
        assert "_dati731" in src
        assert '"EUR/MWh"' in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh731_csv" in src
        assert "mini_idroelettrico.csv" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st731_show_flussi" in src
        assert "st.checkbox" in src

    def test_niente_nome(self):
        assert "Emanuele" not in _helpers_src()
        assert "Emanuele" not in _ui_src()

    def test_ancora_helper_presente(self):
        assert "# W732 (26/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab731:")
