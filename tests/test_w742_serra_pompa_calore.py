"""Test tab742 "🌱🔥 Serra riscaldata: la pompa di calore batte la caldaia a gas?"

Nuova tab tab742 (serra riscaldata,
w743). Business case deterministico
del riscaldamento di una serra
agricola: la caldaia a gas esistente
brucia metano, la pompa di calore
copre lo stesso fabbisogno termico
con elettricita' di rete e SCOP
stagionale. Fabbisogno termico da
superficie e fabbisogno specifico,
energia gas ed elettrica, CO2 gas ed
elettrica, costo energia piu' costo
EUA, CAPEX retrofit, VAN, TIR,
payback semplice, costo livellato,
prezzo elettrico di pareggio e
verdetto. Distinta dal forno ceramico
(li' si cuociono piastrelle in un
forno a tunnel, qui si riscalda una
serra agricola), dal teleriscaldamento
(li' il calore arriva da rete, qui e'
prodotto in loco) e dalla pompa di
calore residenziale (li' si scalda
un'abitazione, qui una serra).

Demo calcolata eseguendo demo_calcoli()
(e ricontrollata a mano, riga per riga):
superficie 10000 m2; fabbisogno 300
kWh/m2/anno; rendimento caldaia 0,90;
SCOP 3,0; prezzo gas 0,09 EUR/kWh;
fattore gas 0,20 kg/kWh; prezzo
elettricita' 220 EUR/MWh; fattore rete
150 kg/MWh; prezzo EUA 85 EUR/t; CAPEX
900000 EUR; WACC 5 %; vita 20 anni;
tolleranza 10 % del CAPEX.

- q_term_kwh = 3000000.0
- e_gas_kwh = 3333333.333333333
- e_el_kwh = 1000000.0
- e_el_MWh = 1000.0
- co2_gas_t = 666.6666666666666
- co2_el_t = 150.0
- co2_risparmiata_t = 516.6666666666666
- costo_energia_gas_eur = 299999.99999999994
- costo_energia_el_eur = 220000.0
- costo_co2_gas_eur = 56666.666666666664
- costo_co2_el_eur = 12750.0
- costo_totale_gas_eur = 356666.6666666666
- costo_totale_elettrico_eur = 232750.0
- risparmio_eur_anno = 123916.66666666663
- risparmio_eur_m2 = 12.391666666666662
- crf = 0.08024258719069129
- quota_capex_eur = 72218.32847162215
- costo_annuo_livellato_elettrico_eur = 304968.32847162214
- costo_livellato_eur_m2 = 30.496832847162214
- costo_totale_gas_eur_m2 = 35.666666666666664
- van = 644275.5649464122
- tir = 12.451538518138188
- payback = 8
- prezzo_pareggio_eur_MWh = 343.91666666666663
- verdetto = 'CONVIENTE'

Scomposizione: fabbisogno termico 10000 x 300 =
3000000.0 kWh/anno; energia gas 3000000.0 / 0,90 =
3333333.333333333 kWh/anno; energia elettrica
3000000.0 / 3,0 = 1000000.0 kWh/anno =
1000.0 MWh/anno; CO2 gas 3333333.333333333 x 0,20 /
1000 = 666.6666666666666 tCO2/anno; CO2 elettrica
1000.0 x 150 / 1000 = 150.0 tCO2/anno; risparmiata
666.6666666666666 - 150.0 = 516.6666666666666
tCO2/anno; costo energia gas 3333333.333333333 x
0,09 = 299999.99999999994 EUR/anno; costo energia
elettrica 1000.0 x 220 = 220000.0 EUR/anno; costo
CO2 gas 666.6666666666666 x 85 =
56666.666666666664 EUR/anno; costo CO2 elettrica
150.0 x 85 = 12750.0 EUR/anno; totali
299999.99999999994 + 56666.666666666664 =
356666.6666666666 EUR/anno contro 220000.0 +
12750.0 = 232750.0 EUR/anno; risparmio
356666.6666666666 - 232750.0 =
123916.66666666663 EUR/anno =
12.391666666666662 EUR/m2; CRF 0,05 x 1,05^20 /
(1,05^20 - 1) = 0.08024258719069129;
quota CAPEX 900000.0 x
0.08024258719069129 = 72218.32847162215
EUR/anno; costo livellato 232750.0 +
72218.32847162215 = 304968.32847162214
EUR/anno = 30.496832847162214 EUR/m2
contro 35.666666666666664 EUR/m2 del gas; flussi:
anno 0 -900000.0, anni 1-20 risparmio
123916.66666666663 (piatti); VAN -900000.0 +
123916.66666666663 x 12,462210342539981
(annuita' 20 anni al 5 %) =
644275.5649464122 EUR; TIR
12.451538518138188 %; payback 8 (ceil di
900000.0 / 123916.66666666663 = 7,26); prezzo
elettrico di pareggio (356666.6666666666 -
12750.0) / 1000.0 = 343.91666666666663 EUR/MWh;
verdetto CONVIENTE perche' VAN
> 0. NOTA: il CRF entra solo nel costo
annuo livellato, mai nei flussi: il
CAPEX compare una sola volta,
all'anno 0.
"""

import ast
import math
import re
from pathlib import Path
import sys
import textwrap

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w743_helpers.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w743_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w743_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w743_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w743_helpers.py: {missing}")
    return out


_F = _load("mh742_num", "mh742_nneg", "mh742_pos",
           "mh742_int_pos", "mh742_pct_0_100",
           "mh742_pct_wacc",
           "mh742_q_term", "mh742_e_gas", "mh742_e_el",
           "mh742_e_el_MWh",
           "mh742_co2_gas", "mh742_co2_el",
           "mh742_co2_risparmiata",
           "mh742_costo_energia_gas",
           "mh742_costo_energia_el", "mh742_costo_co2",
           "mh742_costo_totale", "mh742_risparmio",
           "mh742_risparmio_per_m2", "mh742_crf",
           "mh742_quota_capex", "mh742_costo_livellato",
           "mh742_prezzo_pareggio",
           "mh742_flussi", "mh742_van", "mh742_tir",
           "mh742_payback", "mh742_verdetto",
           "mh742_valida", "_mh742_neutro",
           "mh742_calcola", "mh742_csv",
           "mh742_demo", "demo_calcoli")

TITLE742 = ("🌱🔥 Serra riscaldata: la pompa di calore batte la caldaia a gas?")

Q_DEMO = 3000000.0
EG_DEMO = 3333333.333333333
EE_KWH_DEMO = 1000000.0
EE_MWH_DEMO = 1000.0
CO2_GAS_DEMO = 666.6666666666666
CO2_EL_DEMO = 150.0
CO2_RISP_DEMO = 516.6666666666666
C_EN_GAS_DEMO = 299999.99999999994
C_EN_EL_DEMO = 220000.0
CC_GAS_DEMO = 56666.666666666664
CC_EL_DEMO = 12750.0
CT_GAS_DEMO = 356666.6666666666
CT_EL_DEMO = 232750.0
RISP_DEMO = 123916.66666666663
RM2_DEMO = 12.391666666666662
CRF_DEMO = 0.08024258719069129
QUOTA_DEMO = 72218.32847162215
LIV_DEMO = 304968.32847162214
LIVM2_DEMO = 30.496832847162214
GASM2_DEMO = 35.666666666666664
VAN_DEMO = 644275.5649464122
TIR_DEMO = 12.451538518138188
PAYBACK_DEMO = 8
PAR_DEMO = 343.91666666666663
VERDETTO_DEMO = "CONVIENTE"

_DEMO = {
    "superficie_m2": 10000.0,
    "fabbisogno_kWh_m2_anno": 300.0,
    "eta_caldaia": 0.90,
    "scop": 3.0,
    "prezzo_gas_eur_kWh": 0.09,
    "fattore_gas_kg_kWh": 0.20,
    "prezzo_elettricita_eur_MWh": 220.0,
    "fattore_rete_kg_MWh": 150.0,
    "prezzo_eua_eur_t": 85.0,
    "capex_eur": 900000.0,
    "wacc_pct": 5.0,
    "vita_anni": 20,
    "tolleranza_pct": 10.0,
}

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w743_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w743_ui.py").read_text(encoding="utf-8")


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh742_demo"]()
        d.update(kw)
        return _F["mh742_valida"](**d)

    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh742_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh742_num"]("500", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh742_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh742_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh742_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh742_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh742_pos"](0.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh742_int_pos"](2.5, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh742_int_pos"](20.0, "x") == 20

    def test_pct_0_100_accetta_estremi_rifiuta_fuori(self):
        assert _F["mh742_pct_0_100"](0.0, "x") == 0.0
        assert _F["mh742_pct_0_100"](100.0, "x") == 100.0
        with pytest.raises(ValueError):
            _F["mh742_pct_0_100"](-0.01, "x")
        with pytest.raises(ValueError):
            _F["mh742_pct_0_100"](100.01, "x")

    def test_pct_wacc_accetta_zero_e_50_rifiuta_oltre(self):
        assert _F["mh742_pct_wacc"](0.0, "x") == 0.0
        assert _F["mh742_pct_wacc"](50.0, "x") == 50.0
        with pytest.raises(ValueError):
            _F["mh742_pct_wacc"](-0.01, "x")
        with pytest.raises(ValueError):
            _F["mh742_pct_wacc"](50.01, "x")

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_superficie_zero_e_negativa_non_valide(self):
        assert self._val(superficie_m2=0.0)["valido"] is False
        assert self._val(superficie_m2=-1.0)["valido"] is False

    def test_fabbisogno_eta_scop_zero_non_validi(self):
        assert self._val(fabbisogno_kWh_m2_anno=0.0)["valido"] is False
        assert self._val(eta_caldaia=0.0)["valido"] is False
        assert self._val(scop=0.0)["valido"] is False

    def test_negativi_non_validi(self):
        for k in ("prezzo_gas_eur_kWh",
                  "fattore_gas_kg_kWh",
                  "prezzo_elettricita_eur_MWh",
                  "fattore_rete_kg_MWh",
                  "prezzo_eua_eur_t", "capex_eur"):
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
        assert self._val(superficie_m2=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(superficie_m2=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(vita_anni=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(superficie_m2="500")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(prezzo_gas_eur_kWh=0.0)["valido"] is True
        assert self._val(capex_eur=0.0)["valido"] is True
        assert self._val(prezzo_eua_eur_t=0.0)["valido"] is True
        assert self._val(tolleranza_pct=0.0)["valido"] is True


class TestFunzioni:
    def test_q_term_demo(self):
        assert _F["mh742_q_term"](
            10000.0, 300.0) == pytest.approx(Q_DEMO, rel=REL)

    def test_q_term_formula_letterale(self):
        assert _F["mh742_q_term"](
            5000.0, 200.0) == pytest.approx(1000000.0, rel=REL)

    def test_q_term_rifiuta_superficie_zero(self):
        with pytest.raises(ValueError):
            _F["mh742_q_term"](0.0, 300.0)

    def test_e_gas_demo(self):
        assert _F["mh742_e_gas"](
            Q_DEMO, 0.90) == pytest.approx(EG_DEMO, rel=REL)

    def test_e_gas_rifiuta_eta_zero(self):
        with pytest.raises(ValueError):
            _F["mh742_e_gas"](Q_DEMO, 0.0)

    def test_e_el_demo(self):
        assert _F["mh742_e_el"](
            Q_DEMO, 3.0) == pytest.approx(EE_KWH_DEMO, rel=REL)

    def test_e_el_rifiuta_scop_zero(self):
        with pytest.raises(ValueError):
            _F["mh742_e_el"](Q_DEMO, 0.0)

    def test_e_el_MWh_demo(self):
        assert _F["mh742_e_el_MWh"](
            EE_KWH_DEMO) == pytest.approx(EE_MWH_DEMO, rel=REL)

    def test_co2_gas_demo(self):
        assert _F["mh742_co2_gas"](
            EG_DEMO, 0.20) == pytest.approx(CO2_GAS_DEMO, rel=REL)

    def test_co2_el_demo(self):
        assert _F["mh742_co2_el"](
            EE_MWH_DEMO, 150.0) == pytest.approx(CO2_EL_DEMO, rel=REL)

    def test_co2_risparmiata_demo(self):
        assert _F["mh742_co2_risparmiata"](
            CO2_GAS_DEMO, CO2_EL_DEMO) == pytest.approx(
            CO2_RISP_DEMO, rel=REL)

    def test_co2_risparmiata_negativa_rete_sporca(self):
        assert _F["mh742_co2_risparmiata"](
            1000.0, 2000.0) == pytest.approx(-1000.0, rel=REL)

    def test_costo_energia_gas_demo(self):
        assert _F["mh742_costo_energia_gas"](
            EG_DEMO, 0.09) == pytest.approx(C_EN_GAS_DEMO, rel=REL)

    def test_costo_energia_el_demo(self):
        assert _F["mh742_costo_energia_el"](
            EE_MWH_DEMO, 220.0) == pytest.approx(C_EN_EL_DEMO, rel=REL)

    def test_costo_co2_demo(self):
        assert _F["mh742_costo_co2"](
            CO2_GAS_DEMO, 85.0) == pytest.approx(CC_GAS_DEMO, rel=REL)

    def test_costo_totale_demo(self):
        assert _F["mh742_costo_totale"](
            C_EN_GAS_DEMO, CC_GAS_DEMO) == pytest.approx(
            CT_GAS_DEMO, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh742_risparmio"](
            CT_GAS_DEMO, CT_EL_DEMO) == pytest.approx(
            RISP_DEMO, rel=REL)

    def test_risparmio_negativo_elettrico_piu_caro(self):
        assert _F["mh742_risparmio"](
            1000.0, 2000.0) == pytest.approx(-1000.0, rel=REL)

    def test_risparmio_per_m2_demo(self):
        assert _F["mh742_risparmio_per_m2"](
            RISP_DEMO, 10000.0) == pytest.approx(
            RM2_DEMO, rel=REL)

    def test_crf_demo(self):
        assert _F["mh742_crf"](
            5.0, 20) == pytest.approx(CRF_DEMO, rel=REL)

    def test_crf_wacc_zero_uno_su_n(self):
        assert _F["mh742_crf"](0.0, 20) == pytest.approx(
            1.0 / 20.0, rel=REL)

    def test_crf_formula_indipendente(self):
        r = 0.10
        n = 10
        atteso = r * (1.0 + r) ** n / ((1.0 + r) ** n - 1.0)
        assert _F["mh742_crf"](10.0, 10) == pytest.approx(
            atteso, rel=REL)

    def test_crf_rifiuta_wacc_oltre_50(self):
        with pytest.raises(ValueError):
            _F["mh742_crf"](50.01, 20)

    def test_quota_capex_demo(self):
        assert _F["mh742_quota_capex"](
            900000.0, CRF_DEMO) == pytest.approx(
            QUOTA_DEMO, rel=REL)

    def test_costo_livellato_demo(self):
        assert _F["mh742_costo_livellato"](
            CT_EL_DEMO, QUOTA_DEMO) == pytest.approx(
            LIV_DEMO, rel=REL)

    def test_prezzo_pareggio_demo(self):
        assert _F["mh742_prezzo_pareggio"](
            CT_GAS_DEMO, CO2_EL_DEMO, 85.0,
            EE_MWH_DEMO) == pytest.approx(PAR_DEMO, rel=REL)

    def test_prezzo_pareggio_formula_letterale(self):
        assert _F["mh742_prezzo_pareggio"](
            100000.0, 100.0, 50.0,
            500.0) == pytest.approx(190.0, rel=REL)

    def test_prezzo_pareggio_rifiuta_mwh_zero(self):
        with pytest.raises(ValueError):
            _F["mh742_prezzo_pareggio"](
                CT_GAS_DEMO, CO2_EL_DEMO, 85.0, 0.0)

    def test_flussi_demo(self):
        flussi = _F["mh742_flussi"](900000.0, RISP_DEMO, 20)
        assert len(flussi) == 21
        assert flussi[0] == pytest.approx(-900000.0, rel=REL)
        assert all(f == pytest.approx(RISP_DEMO, rel=REL)
                   for f in flussi[1:])

    def test_van_demo(self):
        flussi = _F["mh742_flussi"](900000.0, RISP_DEMO, 20)
        assert abs(_F["mh742_van"](
            flussi, 5.0) - VAN_DEMO) <= 1.0

    def test_van_tasso_zero(self):
        flussi = _F["mh742_flussi"](900000.0, RISP_DEMO, 20)
        atteso = -900000.0 + RISP_DEMO * 20
        assert _F["mh742_van"](
            flussi, 0.0) == pytest.approx(atteso, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh742_van"]([100.0, 100.0], -0.01)

    def test_tir_none_flussi_tutti_negativi(self):
        flussi = _F["mh742_flussi"](900000.0, -1000.0, 20)
        assert _F["mh742_tir"](flussi) is None

    def test_tir_none_tutti_flussi_non_negativi(self):
        assert _F["mh742_tir"](
            [0.0] + [1000.0] * 20) is None

    def test_tir_esiste_caso_semplice_100_120(self):
        assert _F["mh742_tir"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_caso_semplice_1000_500_500_zero(self):
        assert abs(_F["mh742_tir"](
            [-1000.0, 500.0, 500.0])) <= 1e-9

    def test_tir_demo(self):
        flussi = _F["mh742_flussi"](900000.0, RISP_DEMO, 20)
        assert _F["mh742_tir"](flussi) == pytest.approx(
            TIR_DEMO / 100.0, rel=1e-9)

    def test_payback_demo_8(self):
        assert _F["mh742_payback"](
            900000.0, RISP_DEMO) == 8

    def test_payback_semplice_due(self):
        assert _F["mh742_payback"](1000.0, 500.0) == 2

    def test_payback_zero_capex_zero(self):
        assert _F["mh742_payback"](0.0, 1000.0) == 0

    def test_payback_none_risparmio_zero(self):
        assert _F["mh742_payback"](1000.0, 0.0) is None

    def test_payback_none_risparmio_negativo(self):
        assert _F["mh742_payback"](1000.0, -500.0) is None

    def test_payback_ceil_non_intero(self):
        assert _F["mh742_payback"](1000.0, 300.0) == 4

    def test_verdetto_demo(self):
        assert _F["mh742_verdetto"](
            VAN_DEMO, 900000.0, 10.0,
            RISP_DEMO) == VERDETTO_DEMO

    def test_verdetto_conviente_van_positivo(self):
        assert _F["mh742_verdetto"](
            1000.0, 900000.0, 10.0,
            RISP_DEMO) == "CONVIENTE"

    def test_verdetto_van_zero_marginale(self):
        assert _F["mh742_verdetto"](
            0.0, 900000.0, 10.0,
            RISP_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh742_verdetto"](
            -0.10 * 900000.0, 900000.0, 10.0,
            RISP_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_oltre_limite(self):
        assert _F["mh742_verdetto"](
            -0.10 * 900000.0 - 1.0, 900000.0, 10.0,
            RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_zero(self):
        assert _F["mh742_verdetto"](
            1000.0, 900000.0, 10.0,
            0.0) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_risparmio_negativo(self):
        assert _F["mh742_verdetto"](
            1000.0, 900000.0, 10.0,
            -5000.0) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_risparmio_nan(self):
        assert _F["mh742_verdetto"](
            1000.0, 900000.0, 10.0,
            float("nan")) == "NON_CALCOLABILE"


class TestDemo:
    def _bc(self, **kw):
        d = _F["mh742_demo"]()
        d.update(kw)
        return _F["mh742_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["q_term_kwh"] == pytest.approx(
            Q_DEMO, rel=REL)
        assert c["e_gas_kwh"] == pytest.approx(
            EG_DEMO, rel=REL)
        assert c["e_el_kwh"] == pytest.approx(
            EE_KWH_DEMO, rel=REL)
        assert c["e_el_MWh"] == pytest.approx(
            EE_MWH_DEMO, rel=REL)
        assert c["co2_gas_t"] == pytest.approx(
            CO2_GAS_DEMO, rel=REL)
        assert c["co2_el_t"] == pytest.approx(
            CO2_EL_DEMO, rel=REL)
        assert c["co2_risparmiata_t"] == pytest.approx(
            CO2_RISP_DEMO, rel=REL)
        assert c["costo_energia_gas_eur"] == pytest.approx(
            C_EN_GAS_DEMO, rel=REL)
        assert c["costo_energia_el_eur"] == pytest.approx(
            C_EN_EL_DEMO, rel=REL)
        assert c["costo_co2_gas_eur"] == pytest.approx(
            CC_GAS_DEMO, rel=REL)
        assert c["costo_co2_el_eur"] == pytest.approx(
            CC_EL_DEMO, rel=REL)
        assert c["costo_totale_gas_eur"] == pytest.approx(
            CT_GAS_DEMO, rel=REL)
        assert c["costo_totale_elettrico_eur"] == pytest.approx(
            CT_EL_DEMO, rel=REL)
        assert c["risparmio_eur_anno"] == pytest.approx(
            RISP_DEMO, rel=REL)
        assert c["risparmio_eur_m2"] == pytest.approx(
            RM2_DEMO, rel=REL)
        assert c["crf"] == pytest.approx(CRF_DEMO, rel=REL)
        assert c["quota_capex_eur"] == pytest.approx(
            QUOTA_DEMO, rel=REL)
        assert c["costo_annuo_livellato_elettrico_eur"] == pytest.approx(
            LIV_DEMO, rel=REL)
        assert c["costo_livellato_eur_m2"] == pytest.approx(
            LIVM2_DEMO, rel=REL)
        assert c["costo_totale_gas_eur_m2"] == pytest.approx(
            GASM2_DEMO, rel=REL)
        assert abs(c["van"] - VAN_DEMO) <= 1.0
        assert c["tir"] == pytest.approx(TIR_DEMO, rel=REL)
        assert c["payback"] == PAYBACK_DEMO
        assert c["prezzo_pareggio_eur_MWh"] == pytest.approx(
            PAR_DEMO, rel=REL)
        assert c["verdetto"] == VERDETTO_DEMO
        assert len(c["flussi"]) == 21

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()["van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()["risparmio_eur_anno"] == \
            _F["demo_calcoli"]()["risparmio_eur_anno"]

    def test_demo_defaults_contro_costanti_test(self):
        d = _F["mh742_demo"]()
        for k, v in _DEMO.items():
            assert d[k] == v, k
        assert len(d) == 13

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("q_term_kwh",
                       "e_gas_kwh",
                       "e_el_kwh",
                       "e_el_MWh",
                       "co2_gas_t",
                       "co2_el_t",
                       "co2_risparmiata_t",
                       "costo_energia_gas_eur",
                       "costo_energia_el_eur",
                       "costo_co2_gas_eur",
                       "costo_co2_el_eur",
                       "costo_totale_gas_eur",
                       "costo_totale_elettrico_eur",
                       "risparmio_eur_anno",
                       "risparmio_eur_m2",
                       "crf",
                       "quota_capex_eur",
                       "costo_annuo_livellato_elettrico_eur",
                       "costo_livellato_eur_m2",
                       "costo_totale_gas_eur_m2",
                       "van",
                       "tir",
                       "prezzo_pareggio_eur_MWh"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 8" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_prezzo_elettrico_344_neutro(self):
        # Prezzo elettrico 344 EUR/MWh: risparmio
        # -83,33 EUR/anno -> NON_CALCOLABILE.
        n = self._bc(prezzo_elettricita_eur_MWh=344.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["risparmio_eur_anno"] == 0.0

    def test_prezzo_elettrico_400_neutro(self):
        # Prezzo elettrico 400 EUR/MWh: risparmio
        # -56.083,33 EUR/anno -> NON_CALCOLABILE.
        n = self._bc(prezzo_elettricita_eur_MWh=400.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["risparmio_eur_anno"] == 0.0

    def test_scop_2_non_conviente(self):
        # SCOP 2,0: risparmio 7.541,67
        # EUR/anno, VAN circa -806.014,16
        # EUR, oltre la tolleranza del 10 %
        # del CAPEX (90.000 EUR) ->
        # NON_CONVIENTE.
        n = self._bc(scop=2.0)
        assert n["valid"] is True
        assert n["risparmio_eur_anno"] == pytest.approx(
            7541.666666666667, rel=REL)
        assert abs(n["van"] + 806014.16) <= 1.0
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_prezzo_eua_zero_conviente(self):
        # Prezzo EUA 0: risparmio 80.000
        # EUR/anno, VAN circa +96.976,83
        # EUR -> CONVIENTE.
        n = self._bc(prezzo_eua_eur_t=0.0)
        assert n["valid"] is True
        assert n["risparmio_eur_anno"] == pytest.approx(
            80000.0, rel=REL)
        assert abs(n["van"] - 96976.83) <= 1.0
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_1_5m_conviente(self):
        # CAPEX 1.500.000 EUR: VAN circa
        # +44.275,56 EUR -> CONVIENTE.
        n = self._bc(capex_eur=1500000.0)
        assert n["valid"] is True
        assert abs(n["van"] - 44275.56) <= 1.0
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_1_6m_marginale(self):
        # CAPEX 1.600.000 EUR: VAN circa
        # -55.724,44 EUR, entro la tolleranza
        # del 10 % del CAPEX (90.000 EUR) ->
        # MARGINALE.
        n = self._bc(capex_eur=1600000.0)
        assert n["valid"] is True
        assert abs(n["van"] + 55724.44) <= 1.0
        assert n["verdetto"] == "MARGINALE"

    def test_capex_zero_payback_zero(self):
        # CAPEX zero: flussi [0, risparmio x 20],
        # VAN positiva, payback 0, TIR None
        # (nessun cambio di segno).
        n = self._bc(capex_eur=0.0)
        assert n["valid"] is True
        assert n["van"] == pytest.approx(
            RISP_DEMO * 12.462210342539981, rel=REL)
        assert n["payback"] == 0
        assert n["tir"] is None
        assert n["verdetto"] == "CONVIENTE"

    def test_wacc_zero_valido_crf_uno_su_n(self):
        n = self._bc(wacc_pct=0.0)
        assert n["valid"] is True
        assert n["crf"] == pytest.approx(
            1.0 / 20.0, rel=REL)
        assert n["van"] == pytest.approx(
            1578333.3333333333, rel=REL)

    def test_superficie_zero_neutro(self):
        n = self._bc(superficie_m2=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_fabbisogno_zero_neutro(self):
        n = self._bc(fabbisogno_kWh_m2_anno=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_zero_neutro(self):
        n = self._bc(eta_caldaia=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_scop_zero_neutro(self):
        n = self._bc(scop=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

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
        n = self._bc(superficie_m2=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_anno"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(superficie_m2=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(vita_anni=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_stringa_neutro(self):
        n = self._bc(superficie_m2="500")
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_costo_negativo_neutro(self):
        n = self._bc(prezzo_elettricita_eur_MWh=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh742_neutro"]()
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
        assert n["prezzo_pareggio_eur_MWh"] is None
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh742_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "superficie_m2",
                       "fabbisogno_kWh_m2_anno",
                       "eta_caldaia", "scop",
                       "prezzo_gas_eur_kWh",
                       "fattore_gas_kg_kWh",
                       "prezzo_elettricita_eur_MWh",
                       "fattore_rete_kg_MWh",
                       "prezzo_eua_eur_t",
                       "capex_eur", "wacc_pct",
                       "vita_anni", "tolleranza_pct",
                       "q_term_kwh",
                       "e_gas_kwh",
                       "e_el_kwh",
                       "e_el_MWh",
                       "co2_gas_t", "co2_el_t",
                       "co2_risparmiata_t",
                       "costo_energia_gas_eur",
                       "costo_energia_el_eur",
                       "costo_co2_gas_eur",
                       "costo_co2_el_eur",
                       "costo_totale_gas_eur",
                       "costo_totale_elettrico_eur",
                       "risparmio_eur_anno",
                       "risparmio_eur_m2",
                       "crf", "quota_capex_eur",
                       "costo_annuo_livellato_elettrico_eur",
                       "costo_livellato_eur_m2",
                       "costo_totale_gas_eur_m2",
                       "flussi", "van", "tir",
                       "payback",
                       "prezzo_pareggio_eur_MWh",
                       "verdetto",
                       "df_flussi", "df_tabella"):
            assert chiave in n, chiave
        assert n["errore"] == "errore di prova"
        assert n["tir"] is None

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert b["valid"] is True
        assert list(b["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(b["df_tabella"]) == 38
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Fabbisogno termico (kWh/anno)" in voci
        assert "Energia gas (kWh/anno)" in voci
        assert "Energia elettrica (MWh/anno)" in voci
        assert "CO2 gas (tCO2/anno)" in voci
        assert "CO2 elettrica (tCO2/anno)" in voci
        assert "CO2 risparmiata (tCO2/anno)" in voci
        assert "Costo totale gas (EUR/anno)" in voci
        assert "Costo totale elettrico (EUR/anno)" in voci
        assert "Risparmio (EUR/anno)" in voci
        assert "CRF" in voci
        assert "VAN (EUR)" in voci
        assert "Prezzo elettrico di pareggio (EUR/MWh)" in voci
        assert "Verdetto" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (EUR/anno)",
                                               "Cumulato (EUR)"]
        assert len(b["df_flussi"]) == 21
        assert b["df_flussi"]["Flusso (EUR/anno)"].iloc[0] == \
            pytest.approx(-900000.0, rel=REL)
        assert b["df_flussi"]["Flusso (EUR/anno)"].iloc[1] == \
            pytest.approx(RISP_DEMO, rel=REL)


class TestCsv:
    def _ing(self):
        return _F["mh742_demo"]()

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh742_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") == 39

    def test_csv_contiene_verdetti_e_costi(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh742_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "capex_eur" in txt
        assert "van_eur" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "prezzo_pareggio_eur_MWh" in txt
        assert "risparmio_eur_anno" in txt
        assert "costo_totale_gas_eur" in txt
        assert "q_term_kwh" in txt
        assert "co2_risparmiata_t" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh742_csv"](bc, self._ing())
        assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in txt
        assert f"co2_risparmiata_t;{bc['co2_risparmiata_t']}" in txt
        assert "superficie_m2;10000.0" in txt
        assert "prezzo_elettricita_eur_MWh;220.0" in txt
        assert f"costo_livellato_eur_m2;{bc['costo_livellato_eur_m2']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def742["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def742\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 13, ui_keys
        demo_keys = set(_F["mh742_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh742_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh742_demo():")
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
        ui_keys = set(re.findall(r'_def742\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W743 (27/10/2026) - tab742' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh742_num", "mh742_nneg", "mh742_pos",
                     "mh742_int_pos", "mh742_pct_0_100",
                     "mh742_pct_wacc",
                     "mh742_q_term", "mh742_e_gas",
                     "mh742_e_el", "mh742_e_el_MWh",
                     "mh742_co2_gas", "mh742_co2_el",
                     "mh742_co2_risparmiata",
                     "mh742_costo_energia_gas",
                     "mh742_costo_energia_el",
                     "mh742_costo_co2",
                     "mh742_costo_totale",
                     "mh742_risparmio",
                     "mh742_risparmio_per_m2",
                     "mh742_crf", "mh742_quota_capex",
                     "mh742_costo_livellato",
                     "mh742_prezzo_pareggio",
                     "mh742_flussi", "mh742_van",
                     "mh742_tir", "mh742_payback",
                     "mh742_verdetto", "mh742_valida",
                     "_mh742_neutro",
                     "mh742_calcola", "mh742_csv",
                     "mh742_demo", "demo_calcoli"):
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
        mh_old = "mh" + "741"
        st_old = "st" + "741"
        tab_old = "tab" + "741"
        w_old = "W" + "742"
        assert mh_old not in _helpers_src()
        assert mh_old not in _ui_src()
        assert st_old not in _ui_src()
        assert tab_old not in _ui_src()
        assert w_old not in _helpers_src()
        assert w_old not in _ui_src()
        assert "mh742" in _helpers_src()
        assert "st742" in _ui_src()

    def test_helpers_parse_ast(self):
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w743_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE742) == 1

    def test_blocco_with_tab742(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab742:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE742

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st742_[A-Za-z0-9_]+)"', _ui_src())
        assert len(keys) == 21, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st742_") for k in keys)

    def test_chiavi_st_input_presenti(self):
        keys = re.findall(r'key="(st742_[A-Za-z0-9_]+)"', _ui_src())
        attese = ["st742_superficie", "st742_fabbisogno",
                  "st742_eta", "st742_scop",
                  "st742_prezzo_gas", "st742_fattore_gas",
                  "st742_prezzo_el", "st742_fattore_rete",
                  "st742_eua", "st742_capex", "st742_wacc",
                  "st742_vita", "st742_tolleranza",
                  "st742_grafico", "st742_show_flussi",
                  "st742_show_tabella", "st742_nota",
                  "st742_ipotesi", "st742_calcola",
                  "st742_csv", "st742_csv_flussi"]
        assert len(attese) == 21
        for k in attese:
            assert k in keys, k

    def test_chiavi_st_niente_fstring_dinamiche(self):
        src = _ui_src()
        assert 'key=f"' not in src
        assert "key=f'" not in src

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg742" in src
        assert "NON_CALCOLABILE" in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg742") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg742")
        assert g < src.index("st.bar_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "CO2 risparmiata (t/anno)" in src
        assert "Risparmio (EUR/anno)" in src
        assert "Costo livellato elettrico (EUR/m2)" in src
        assert "VAN (kEUR)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON_CALCOLABILE"):
            assert v in src

    def test_distinzioni_presenti(self):
        src = _ui_src()
        assert "biomassa" in src
        assert "teleriscaldamento" in src
        assert "residenziale" in src
        assert "ceramico" in src

    def test_distinzioni_in_header_helpers(self):
        src = _helpers_src()
        assert "biomassa" in src
        assert "teleriscaldamento" in src
        assert "residenziale" in src
        assert "ceramico" in src

    def test_nota_didattica_presente(self):
        src = _ui_src()
        assert "NOTA DIDATTICA" in src
        assert "3.000.000" in src
        assert "1.000.000" in src

    def test_grafico_bar_chart_presente(self):
        src = _ui_src()
        assert "st.bar_chart" in src
        assert "_dati742" in src
        assert '"EUR/anno"' in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh742_csv" in src
        assert "serra_pompa_calore.csv" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st742_show_flussi" in src
        assert "st.checkbox" in src

    def test_niente_nome(self):
        assert "Emanuele" not in _helpers_src()
        assert "Emanuele" not in _ui_src()

    def test_ancora_helper_presente(self):
        assert "# W743 (27/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab742:")
