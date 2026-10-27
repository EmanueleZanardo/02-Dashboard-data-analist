"""Test tab743 "✈️⚡ Ground power elettrico in aeroporto: l'e-GPU batte diesel + APU?"

Nuova tab tab743 (ground power
aeroporto, w744). Business case
deterministico del ground power in
aeroporto: il baseline per
turnaround usa una GPU diesel piu'
l'APU dell'aeromobile accesa a
lungo, l'alternativa usa una GPU
elettrica (e-GPU) alimentata da
rete e riduce l'APU al solo breve
avviamento. Ore GPU annue da
movimenti e ore per movimento,
diesel da consumo orario,
cherosene base e alternativo da
ore APU e consumo APU, energia
elettrica da potenza e-GPU, CO2
diesel, APU ed elettrica, costo
energia piu' costo EUA, CAPEX
e-GPU, VAN, TIR, payback
semplice, costo livellato, prezzo
elettrico di pareggio e verdetto.
Distinta dalle tab sui carburanti
SAF e bunker (li' si confrontano
carburanti per volo o nave, qui
il ground power a terra), dalla
tab sull'inferenza AI (li' GPU
significa processore grafico, qui
Ground Power Unit) e dalle tab
sui veicoli elettrici stradali
(li' si ricarica un veicolo su
strada, qui si alimenta un
aeromobile in sosta). Nessuna
altra tab e' dedicata
all'aeroporto: 0 occorrenze di
"aeroporto" in app.py prima di
questa tab.

Demo calcolata eseguendo demo_calcoli()
(e ricontrollata a mano, riga per riga):
movimenti 12000 /anno; ore GPU per
movimento 1,25 h; consumo diesel 10,0
L/h; ore APU base 1,25 h e alternativa
0,25 h; consumo APU 100,0 kg/h; potenza
e-GPU 90,0 kW; fattore diesel 2,68 kg/L;
fattore cherosene 3,16 kg/kg; prezzo
diesel 1,70 EUR/L; prezzo cherosene
950,0 EUR/t; prezzo elettricita' 220,0
EUR/MWh; fattore rete 150,0 kg/MWh;
prezzo EUA 85,0 EUR/t; CAPEX 2500000,0
EUR; WACC 6,0 %; vita 15 anni;
tolleranza 10,0 % del CAPEX.

- ore_gpu_anno = 15000.0
- diesel_L = 150000.0
- cherosene_base_kg = 1500000.0
- cherosene_base_t = 1500.0
- cherosene_alt_kg = 300000.0
- cherosene_alt_t = 300.0
- energia_el_kwh = 1350000.0
- energia_el_MWh = 1350.0
- co2_diesel_t = 402.0
- co2_apu_base_t = 4740.0
- co2_apu_alt_t = 948.0
- co2_el_t = 202.5
- co2_base_t = 5142.0
- co2_alt_t = 1150.5
- co2_risparmiata_t = 3991.5
- costo_diesel_eur = 255000.0
- costo_cherosene_base_eur = 1425000.0
- costo_cherosene_alt_eur = 285000.0
- costo_energia_el_eur = 297000.0
- costo_co2_base_eur = 437070.0
- costo_co2_alt_eur = 97792.5
- costo_totale_base_eur = 2117070.0
- costo_totale_alt_eur = 679792.5
- risparmio_eur_anno = 1437277.5
- risparmio_eur_movimento = 119.773125
- crf = 0.10296276395531265
- quota_capex_eur = 257406.90988828163
- costo_annuo_livellato_alt_eur = 937199.4098882816
- costo_livellato_eur_movimento = 78.09995082402347
- costo_totale_base_eur_movimento = 176.4225
- van = 11459196.94447789
- tir = 57.42750964672604
- payback = 2
- prezzo_pareggio_eur_MWh = 1284.65
- verdetto = 'CONVIENTE'

Scomposizione: ore GPU annue 12000 x 1,25 =
15000.0 h/anno; diesel 15000.0 x 10,0 =
150000.0 L/anno; cherosene base 12000 x 1,25 x
100,0 = 1500000.0 kg/anno = 1500.0 t/anno;
cherosene alternativo 12000 x 0,25 x 100,0 =
300000.0 kg/anno = 300.0 t/anno; energia
elettrica 15000.0 x 90,0 = 1350000.0 kWh/anno =
1350.0 MWh/anno; CO2 diesel 150000.0 x 2,68 /
1000 = 402.0 tCO2/anno; CO2 APU base 1500.0 x
3,16 = 4740.0 tCO2/anno; CO2 APU alternativa
300.0 x 3,16 = 948.0 tCO2/anno; CO2 elettrica
1350.0 x 150,0 / 1000 = 202.5 tCO2/anno; CO2 base
402.0 + 4740.0 = 5142.0 tCO2/anno; CO2
alternativa 202.5 + 948.0 = 1150.5 tCO2/anno;
risparmiata 5142.0 - 1150.5 = 3991.5
tCO2/anno; costo diesel 150000.0 x 1,70 =
255000.0 EUR/anno; costo cherosene base
1500.0 x 950,0 = 1425000.0 EUR/anno; costo
cherosene alternativo 300.0 x 950,0 =
285000.0 EUR/anno; costo energia elettrica
1350.0 x 220,0 = 297000.0 EUR/anno; costo CO2
base 5142.0 x 85,0 = 437070.0 EUR/anno; costo
CO2 alternativa 1150.5 x 85,0 = 97792.5
EUR/anno; totali 255000.0 + 1425000.0 +
437070.0 = 2117070.0 EUR/anno contro 297000.0
+ 285000.0 + 97792.5 = 679792.5 EUR/anno;
risparmio 2117070.0 - 679792.5 = 1437277.5
EUR/anno = 119.773125 EUR/movimento; CRF
0,06 x 1,06^15 / (1,06^15 - 1) =
0.10296276395531265; quota CAPEX 2500000.0 x
0.10296276395531265 = 257406.90988828163
EUR/anno; costo livellato 679792.5 +
257406.90988828163 = 937199.4098882816
EUR/anno = 78.09995082402347 EUR/movimento
contro 176.4225 EUR/movimento del baseline;
flussi: anno 0 -2500000.0, anni 1-15 risparmio
1437277.5 (piatti); VAN -2500000.0 +
1437277.5 x 9,712248987740992 (annuita' 15
anni al 6 %) = 11459196.94447789 EUR; TIR
57.42750964672604 %; payback 2 (ceil di
2500000.0 / 1437277.5 = 1,74); prezzo
elettrico di pareggio (2117070.0 - 285000.0 -
948.0 x 85,0) / 1350.0 - 150,0 x 85,0 / 1000 =
1284.65 EUR/MWh; verdetto CONVIENTE perche'
VAN > 0. NOTA: il CRF entra solo nel costo
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
    if (p / "w744_helpers.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w744_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w744_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w744_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w744_helpers.py: {missing}")
    return out


_F = _load("mh743_num", "mh743_nneg", "mh743_pos",
           "mh743_int_pos", "mh743_pct_0_100",
           "mh743_pct_wacc",
           "mh743_ore_gpu_anno", "mh743_diesel_L",
           "mh743_cherosene_kg", "mh743_cherosene_t",
           "mh743_energia_el_kwh", "mh743_energia_el_MWh",
           "mh743_co2_diesel", "mh743_co2_apu", "mh743_co2_el",
           "mh743_co2_base", "mh743_co2_alt",
           "mh743_co2_risparmiata",
           "mh743_costo_diesel", "mh743_costo_cherosene",
           "mh743_costo_energia_el", "mh743_costo_co2",
           "mh743_costo_totale_base", "mh743_costo_totale_alt",
           "mh743_risparmio", "mh743_risparmio_per_movimento",
           "mh743_crf", "mh743_quota_capex",
           "mh743_costo_livellato", "mh743_prezzo_pareggio",
           "mh743_flussi", "mh743_van", "mh743_tir",
           "mh743_payback", "mh743_verdetto",
           "mh743_valida", "_mh743_neutro",
           "mh743_calcola", "mh743_csv",
           "mh743_demo", "demo_calcoli")

TITLE743 = ("✈️⚡ Ground power elettrico in aeroporto: l'e-GPU batte diesel + APU?")

ORE_DEMO = 15000.0
DIESEL_DEMO = 150000.0
KB_KG_DEMO = 1500000.0
KB_T_DEMO = 1500.0
KA_KG_DEMO = 300000.0
KA_T_DEMO = 300.0
EE_KWH_DEMO = 1350000.0
EE_MWH_DEMO = 1350.0
CO2_DIESEL_DEMO = 402.0
CO2_APU_BASE_DEMO = 4740.0
CO2_APU_ALT_DEMO = 948.0
CO2_EL_DEMO = 202.5
CO2_BASE_DEMO = 5142.0
CO2_ALT_DEMO = 1150.5
CO2_RISP_DEMO = 3991.5
C_DIESEL_DEMO = 255000.0
C_KB_DEMO = 1425000.0
C_KA_DEMO = 285000.0
C_EL_DEMO = 297000.0
CC_BASE_DEMO = 437070.0
CC_ALT_DEMO = 97792.5
CT_BASE_DEMO = 2117070.0
CT_ALT_DEMO = 679792.5
RISP_DEMO = 1437277.5
RPM_DEMO = 119.773125
CRF_DEMO = 0.10296276395531265
QUOTA_DEMO = 257406.90988828163
LIV_DEMO = 937199.4098882816
LIVM_DEMO = 78.09995082402347
BASEM_DEMO = 176.4225
VAN_DEMO = 11459196.944477892
TIR_DEMO = 57.42750964672604
PAYBACK_DEMO = 2
PAR_DEMO = 1284.65
VERDETTO_DEMO = "CONVIENTE"

_DEMO = {
    "movimenti_anno": 12000,
    "ore_gpu_per_movimento": 1.25,
    "consumo_diesel_L_h": 10.0,
    "ore_apu_base_h": 1.25,
    "ore_apu_alt_h": 0.25,
    "consumo_apu_kg_h": 100.0,
    "potenza_egpu_kW": 90.0,
    "fattore_diesel_kg_L": 2.68,
    "fattore_cherosene_kg_kg": 3.16,
    "prezzo_diesel_EUR_L": 1.70,
    "prezzo_cherosene_EUR_t": 950.0,
    "prezzo_el_EUR_MWh": 220.0,
    "fattore_rete_kg_MWh": 150.0,
    "prezzo_eua_eur_t": 85.0,
    "capex_eur": 2500000.0,
    "wacc_pct": 6.0,
    "vita_anni": 15,
    "tolleranza_pct": 10.0,
}

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w744_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w744_ui.py").read_text(encoding="utf-8")


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh743_demo"]()
        d.update(kw)
        return _F["mh743_valida"](**d)

    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh743_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh743_num"]("500", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh743_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh743_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh743_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh743_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh743_pos"](0.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh743_int_pos"](2.5, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh743_int_pos"](15.0, "x") == 15

    def test_pct_0_100_accetta_estremi_rifiuta_fuori(self):
        assert _F["mh743_pct_0_100"](0.0, "x") == 0.0
        assert _F["mh743_pct_0_100"](100.0, "x") == 100.0
        with pytest.raises(ValueError):
            _F["mh743_pct_0_100"](-0.01, "x")
        with pytest.raises(ValueError):
            _F["mh743_pct_0_100"](100.01, "x")

    def test_pct_wacc_accetta_zero_e_50_rifiuta_oltre(self):
        assert _F["mh743_pct_wacc"](0.0, "x") == 0.0
        assert _F["mh743_pct_wacc"](50.0, "x") == 50.0
        with pytest.raises(ValueError):
            _F["mh743_pct_wacc"](-0.01, "x")
        with pytest.raises(ValueError):
            _F["mh743_pct_wacc"](50.01, "x")

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_movimenti_zero_e_negativi_non_validi(self):
        assert self._val(movimenti_anno=0)["valido"] is False
        assert self._val(movimenti_anno=-1)["valido"] is False
        assert self._val(movimenti_anno=12000.5)["valido"] is False

    def test_apu_alt_sopra_base_non_valida(self):
        assert self._val(ore_apu_alt_h=1.5)["valido"] is False
        assert self._val(ore_apu_alt_h=1.25)["valido"] is True
        assert self._val(ore_apu_alt_h=0.0)["valido"] is True

    def test_consumi_potenza_zero_non_validi(self):
        assert self._val(consumo_diesel_L_h=0.0)["valido"] is False
        assert self._val(consumo_apu_kg_h=0.0)["valido"] is False
        assert self._val(potenza_egpu_kW=0.0)["valido"] is False

    def test_negativi_non_validi(self):
        for k in ("prezzo_diesel_EUR_L",
                  "prezzo_cherosene_EUR_t",
                  "prezzo_el_EUR_MWh",
                  "fattore_diesel_kg_L",
                  "fattore_cherosene_kg_kg",
                  "fattore_rete_kg_MWh",
                  "prezzo_eua_eur_t", "capex_eur"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_vita_zero_e_frazione_non_valide(self):
        assert self._val(vita_anni=0)["valido"] is False
        assert self._val(vita_anni=15.5)["valido"] is False

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
        assert self._val(movimenti_anno=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(movimenti_anno=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(vita_anni=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(movimenti_anno="500")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(prezzo_diesel_EUR_L=0.0)["valido"] is True
        assert self._val(capex_eur=0.0)["valido"] is True
        assert self._val(prezzo_eua_eur_t=0.0)["valido"] is True
        assert self._val(tolleranza_pct=0.0)["valido"] is True
        assert self._val(ore_apu_alt_h=0.0)["valido"] is True


class TestFunzioni:
    def test_ore_gpu_anno_demo(self):
        assert _F["mh743_ore_gpu_anno"](
            12000, 1.25) == pytest.approx(ORE_DEMO, rel=REL)

    def test_ore_gpu_anno_formula_letterale(self):
        assert _F["mh743_ore_gpu_anno"](
            6000, 2.0) == pytest.approx(12000.0, rel=REL)

    def test_ore_gpu_anno_rifiuta_movimenti_zero(self):
        with pytest.raises(ValueError):
            _F["mh743_ore_gpu_anno"](0, 1.25)

    def test_diesel_demo(self):
        assert _F["mh743_diesel_L"](
            ORE_DEMO, 10.0) == pytest.approx(DIESEL_DEMO, rel=REL)

    def test_cherosene_kg_base_demo(self):
        assert _F["mh743_cherosene_kg"](
            12000, 1.25, 100.0) == pytest.approx(KB_KG_DEMO, rel=REL)

    def test_cherosene_kg_alt_demo(self):
        assert _F["mh743_cherosene_kg"](
            12000, 0.25, 100.0) == pytest.approx(KA_KG_DEMO, rel=REL)

    def test_cherosene_kg_rifiuta_consumo_zero(self):
        with pytest.raises(ValueError):
            _F["mh743_cherosene_kg"](12000, 1.25, 0.0)

    def test_cherosene_t_demo(self):
        assert _F["mh743_cherosene_t"](
            KB_KG_DEMO) == pytest.approx(KB_T_DEMO, rel=REL)

    def test_energia_el_kwh_demo(self):
        assert _F["mh743_energia_el_kwh"](
            ORE_DEMO, 90.0) == pytest.approx(EE_KWH_DEMO, rel=REL)

    def test_energia_el_MWh_demo(self):
        assert _F["mh743_energia_el_MWh"](
            EE_KWH_DEMO) == pytest.approx(EE_MWH_DEMO, rel=REL)

    def test_co2_diesel_demo(self):
        assert _F["mh743_co2_diesel"](
            DIESEL_DEMO, 2.68) == pytest.approx(CO2_DIESEL_DEMO, rel=REL)

    def test_co2_apu_base_demo(self):
        assert _F["mh743_co2_apu"](
            KB_T_DEMO, 3.16) == pytest.approx(CO2_APU_BASE_DEMO, rel=REL)

    def test_co2_apu_alt_demo(self):
        assert _F["mh743_co2_apu"](
            KA_T_DEMO, 3.16) == pytest.approx(CO2_APU_ALT_DEMO, rel=REL)

    def test_co2_el_demo(self):
        assert _F["mh743_co2_el"](
            EE_MWH_DEMO, 150.0) == pytest.approx(CO2_EL_DEMO, rel=REL)

    def test_co2_base_demo(self):
        assert _F["mh743_co2_base"](
            CO2_DIESEL_DEMO, CO2_APU_BASE_DEMO) == pytest.approx(
            CO2_BASE_DEMO, rel=REL)

    def test_co2_alt_demo(self):
        assert _F["mh743_co2_alt"](
            CO2_EL_DEMO, CO2_APU_ALT_DEMO) == pytest.approx(
            CO2_ALT_DEMO, rel=REL)

    def test_co2_risparmiata_demo(self):
        assert _F["mh743_co2_risparmiata"](
            CO2_BASE_DEMO, CO2_ALT_DEMO) == pytest.approx(
            CO2_RISP_DEMO, rel=REL)

    def test_co2_risparmiata_negativa_rete_sporca(self):
        assert _F["mh743_co2_risparmiata"](
            1000.0, 2000.0) == pytest.approx(-1000.0, rel=REL)

    def test_costo_diesel_demo(self):
        assert _F["mh743_costo_diesel"](
            DIESEL_DEMO, 1.70) == pytest.approx(C_DIESEL_DEMO, rel=REL)

    def test_costo_cherosene_demo(self):
        assert _F["mh743_costo_cherosene"](
            KB_T_DEMO, 950.0) == pytest.approx(C_KB_DEMO, rel=REL)

    def test_costo_energia_el_demo(self):
        assert _F["mh743_costo_energia_el"](
            EE_MWH_DEMO, 220.0) == pytest.approx(C_EL_DEMO, rel=REL)

    def test_costo_co2_demo(self):
        assert _F["mh743_costo_co2"](
            CO2_BASE_DEMO, 85.0) == pytest.approx(CC_BASE_DEMO, rel=REL)

    def test_costo_totale_base_demo(self):
        assert _F["mh743_costo_totale_base"](
            C_DIESEL_DEMO, C_KB_DEMO, CC_BASE_DEMO) == pytest.approx(
            CT_BASE_DEMO, rel=REL)

    def test_costo_totale_alt_demo(self):
        assert _F["mh743_costo_totale_alt"](
            C_EL_DEMO, C_KA_DEMO, CC_ALT_DEMO) == pytest.approx(
            CT_ALT_DEMO, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh743_risparmio"](
            CT_BASE_DEMO, CT_ALT_DEMO) == pytest.approx(
            RISP_DEMO, rel=REL)

    def test_risparmio_negativo_elettrico_piu_caro(self):
        assert _F["mh743_risparmio"](
            1000.0, 2000.0) == pytest.approx(-1000.0, rel=REL)

    def test_risparmio_per_movimento_demo(self):
        assert _F["mh743_risparmio_per_movimento"](
            RISP_DEMO, 12000) == pytest.approx(
            RPM_DEMO, rel=REL)

    def test_crf_demo(self):
        assert _F["mh743_crf"](
            6.0, 15) == pytest.approx(CRF_DEMO, rel=REL)

    def test_crf_wacc_zero_uno_su_n(self):
        assert _F["mh743_crf"](0.0, 15) == pytest.approx(
            1.0 / 15.0, rel=REL)

    def test_crf_formula_indipendente(self):
        r = 0.10
        n = 10
        atteso = r * (1.0 + r) ** n / ((1.0 + r) ** n - 1.0)
        assert _F["mh743_crf"](10.0, 10) == pytest.approx(
            atteso, rel=REL)

    def test_crf_rifiuta_wacc_oltre_50(self):
        with pytest.raises(ValueError):
            _F["mh743_crf"](50.01, 15)

    def test_quota_capex_demo(self):
        assert _F["mh743_quota_capex"](
            2500000.0, CRF_DEMO) == pytest.approx(
            QUOTA_DEMO, rel=REL)

    def test_costo_livellato_demo(self):
        assert _F["mh743_costo_livellato"](
            CT_ALT_DEMO, QUOTA_DEMO) == pytest.approx(
            LIV_DEMO, rel=REL)

    def test_prezzo_pareggio_demo(self):
        assert _F["mh743_prezzo_pareggio"](
            CT_BASE_DEMO, C_KA_DEMO, CO2_APU_ALT_DEMO, 85.0,
            EE_MWH_DEMO, 150.0) == pytest.approx(PAR_DEMO, rel=REL)

    def test_prezzo_pareggio_formula_letterale(self):
        # (100000 - 20000 - 100 x 50) / 500 - 200 x 50 / 1000 = 140.
        assert _F["mh743_prezzo_pareggio"](
            100000.0, 20000.0, 100.0, 50.0,
            500.0, 200.0) == pytest.approx(140.0, rel=REL)

    def test_prezzo_pareggio_rifiuta_mwh_zero(self):
        with pytest.raises(ValueError):
            _F["mh743_prezzo_pareggio"](
                CT_BASE_DEMO, C_KA_DEMO, CO2_APU_ALT_DEMO, 85.0,
                0.0, 150.0)

    def test_flussi_demo(self):
        flussi = _F["mh743_flussi"](2500000.0, RISP_DEMO, 15)
        assert len(flussi) == 16
        assert flussi[0] == pytest.approx(-2500000.0, rel=REL)
        assert all(f == pytest.approx(RISP_DEMO, rel=REL)
                   for f in flussi[1:])

    def test_van_demo(self):
        flussi = _F["mh743_flussi"](2500000.0, RISP_DEMO, 15)
        assert abs(_F["mh743_van"](
            flussi, 6.0) - VAN_DEMO) <= 1.0

    def test_van_tasso_zero(self):
        flussi = _F["mh743_flussi"](2500000.0, RISP_DEMO, 15)
        atteso = -2500000.0 + RISP_DEMO * 15
        assert _F["mh743_van"](
            flussi, 0.0) == pytest.approx(atteso, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh743_van"]([100.0, 100.0], -0.01)

    def test_tir_none_flussi_tutti_negativi(self):
        flussi = _F["mh743_flussi"](2500000.0, -1000.0, 15)
        assert _F["mh743_tir"](flussi) is None

    def test_tir_none_tutti_flussi_non_negativi(self):
        assert _F["mh743_tir"](
            [0.0] + [1000.0] * 15) is None

    def test_tir_esiste_caso_semplice_100_120(self):
        assert _F["mh743_tir"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_caso_semplice_1000_500_500_zero(self):
        assert abs(_F["mh743_tir"](
            [-1000.0, 500.0, 500.0])) <= 1e-9

    def test_tir_demo(self):
        flussi = _F["mh743_flussi"](2500000.0, RISP_DEMO, 15)
        assert _F["mh743_tir"](flussi) == pytest.approx(
            TIR_DEMO / 100.0, rel=1e-9)

    def test_payback_demo_2(self):
        assert _F["mh743_payback"](
            2500000.0, RISP_DEMO) == 2

    def test_payback_semplice_due(self):
        assert _F["mh743_payback"](1000.0, 500.0) == 2

    def test_payback_zero_capex_zero(self):
        assert _F["mh743_payback"](0.0, 1000.0) == 0

    def test_payback_none_risparmio_zero(self):
        assert _F["mh743_payback"](1000.0, 0.0) is None

    def test_payback_none_risparmio_negativo(self):
        assert _F["mh743_payback"](1000.0, -500.0) is None

    def test_payback_ceil_non_intero(self):
        assert _F["mh743_payback"](1000.0, 300.0) == 4

    def test_verdetto_demo(self):
        assert _F["mh743_verdetto"](
            VAN_DEMO, 2500000.0, 10.0,
            RISP_DEMO) == VERDETTO_DEMO

    def test_verdetto_conviente_van_positivo(self):
        assert _F["mh743_verdetto"](
            1000.0, 2500000.0, 10.0,
            RISP_DEMO) == "CONVIENTE"

    def test_verdetto_van_zero_marginale(self):
        assert _F["mh743_verdetto"](
            0.0, 2500000.0, 10.0,
            RISP_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh743_verdetto"](
            -0.10 * 2500000.0, 2500000.0, 10.0,
            RISP_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_oltre_limite(self):
        assert _F["mh743_verdetto"](
            -0.10 * 2500000.0 - 1.0, 2500000.0, 10.0,
            RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_zero(self):
        assert _F["mh743_verdetto"](
            1000.0, 2500000.0, 10.0,
            0.0) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_risparmio_negativo(self):
        assert _F["mh743_verdetto"](
            1000.0, 2500000.0, 10.0,
            -5000.0) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_risparmio_nan(self):
        assert _F["mh743_verdetto"](
            1000.0, 2500000.0, 10.0,
            float("nan")) == "NON_CALCOLABILE"


class TestDemo:
    def _bc(self, **kw):
        d = _F["mh743_demo"]()
        d.update(kw)
        return _F["mh743_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["ore_gpu_anno"] == pytest.approx(
            ORE_DEMO, rel=REL)
        assert c["diesel_L"] == pytest.approx(
            DIESEL_DEMO, rel=REL)
        assert c["cherosene_base_kg"] == pytest.approx(
            KB_KG_DEMO, rel=REL)
        assert c["cherosene_base_t"] == pytest.approx(
            KB_T_DEMO, rel=REL)
        assert c["cherosene_alt_kg"] == pytest.approx(
            KA_KG_DEMO, rel=REL)
        assert c["cherosene_alt_t"] == pytest.approx(
            KA_T_DEMO, rel=REL)
        assert c["energia_el_kwh"] == pytest.approx(
            EE_KWH_DEMO, rel=REL)
        assert c["energia_el_MWh"] == pytest.approx(
            EE_MWH_DEMO, rel=REL)
        assert c["co2_diesel_t"] == pytest.approx(
            CO2_DIESEL_DEMO, rel=REL)
        assert c["co2_apu_base_t"] == pytest.approx(
            CO2_APU_BASE_DEMO, rel=REL)
        assert c["co2_apu_alt_t"] == pytest.approx(
            CO2_APU_ALT_DEMO, rel=REL)
        assert c["co2_el_t"] == pytest.approx(
            CO2_EL_DEMO, rel=REL)
        assert c["co2_base_t"] == pytest.approx(
            CO2_BASE_DEMO, rel=REL)
        assert c["co2_alt_t"] == pytest.approx(
            CO2_ALT_DEMO, rel=REL)
        assert c["co2_risparmiata_t"] == pytest.approx(
            CO2_RISP_DEMO, rel=REL)
        assert c["costo_diesel_eur"] == pytest.approx(
            C_DIESEL_DEMO, rel=REL)
        assert c["costo_cherosene_base_eur"] == pytest.approx(
            C_KB_DEMO, rel=REL)
        assert c["costo_cherosene_alt_eur"] == pytest.approx(
            C_KA_DEMO, rel=REL)
        assert c["costo_energia_el_eur"] == pytest.approx(
            C_EL_DEMO, rel=REL)
        assert c["costo_co2_base_eur"] == pytest.approx(
            CC_BASE_DEMO, rel=REL)
        assert c["costo_co2_alt_eur"] == pytest.approx(
            CC_ALT_DEMO, rel=REL)
        assert c["costo_totale_base_eur"] == pytest.approx(
            CT_BASE_DEMO, rel=REL)
        assert c["costo_totale_alt_eur"] == pytest.approx(
            CT_ALT_DEMO, rel=REL)
        assert c["risparmio_eur_anno"] == pytest.approx(
            RISP_DEMO, rel=REL)
        assert c["risparmio_eur_movimento"] == pytest.approx(
            RPM_DEMO, rel=REL)
        assert c["crf"] == pytest.approx(CRF_DEMO, rel=REL)
        assert c["quota_capex_eur"] == pytest.approx(
            QUOTA_DEMO, rel=REL)
        assert c["costo_annuo_livellato_alt_eur"] == pytest.approx(
            LIV_DEMO, rel=REL)
        assert c["costo_livellato_eur_movimento"] == pytest.approx(
            LIVM_DEMO, rel=REL)
        assert c["costo_totale_base_eur_movimento"] == pytest.approx(
            BASEM_DEMO, rel=REL)
        assert abs(c["van"] - VAN_DEMO) <= 1.0
        assert c["tir"] == pytest.approx(TIR_DEMO, rel=REL)
        assert c["payback"] == PAYBACK_DEMO
        assert c["prezzo_pareggio_eur_MWh"] == pytest.approx(
            PAR_DEMO, rel=REL)
        assert c["verdetto"] == VERDETTO_DEMO
        assert len(c["flussi"]) == 16

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()["van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()["risparmio_eur_anno"] == \
            _F["demo_calcoli"]()["risparmio_eur_anno"]

    def test_demo_defaults_contro_costanti_test(self):
        d = _F["mh743_demo"]()
        for k, v in _DEMO.items():
            assert d[k] == v, k
        assert len(d) == 18

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("ore_gpu_anno",
                       "diesel_L",
                       "cherosene_base_kg",
                       "cherosene_base_t",
                       "cherosene_alt_kg",
                       "cherosene_alt_t",
                       "energia_el_kwh",
                       "energia_el_MWh",
                       "co2_diesel_t",
                       "co2_apu_base_t",
                       "co2_apu_alt_t",
                       "co2_el_t",
                       "co2_base_t",
                       "co2_alt_t",
                       "co2_risparmiata_t",
                       "costo_diesel_eur",
                       "costo_cherosene_base_eur",
                       "costo_cherosene_alt_eur",
                       "costo_energia_el_eur",
                       "costo_co2_base_eur",
                       "costo_co2_alt_eur",
                       "costo_totale_base_eur",
                       "costo_totale_alt_eur",
                       "risparmio_eur_anno",
                       "risparmio_eur_movimento",
                       "crf",
                       "quota_capex_eur",
                       "costo_annuo_livellato_alt_eur",
                       "costo_livellato_eur_movimento",
                       "costo_totale_base_eur_movimento",
                       "van",
                       "tir",
                       "prezzo_pareggio_eur_MWh"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 2" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_prezzo_elettrico_1300_neutro(self):
        # Prezzo elettrico 1300 EUR/MWh: risparmio
        # -20.722,5 EUR/anno -> NON_CALCOLABILE.
        n = self._bc(prezzo_el_EUR_MWh=1300.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["risparmio_eur_anno"] == 0.0

    def test_capex_20m_non_conviente(self):
        # CAPEX 20.000.000 EUR: VAN circa
        # -6.040.803,06 EUR, oltre la tolleranza
        # del 10 % del CAPEX (2.000.000 EUR) ->
        # NON_CONVIENTE.
        n = self._bc(capex_eur=20000000.0)
        assert n["valid"] is True
        assert abs(n["van"] + 6040803.06) <= 1.0
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_capex_14m_marginale(self):
        # CAPEX 14.000.000 EUR: VAN circa
        # -40.803,06 EUR, entro la tolleranza
        # del 10 % del CAPEX (1.400.000 EUR) ->
        # MARGINALE.
        n = self._bc(capex_eur=14000000.0)
        assert n["valid"] is True
        assert abs(n["van"] + 40803.06) <= 1.0
        assert n["verdetto"] == "MARGINALE"

    def test_prezzo_eua_zero_conviente(self):
        # Prezzo EUA 0: risparmio 1.098.000
        # EUR/anno, VAN circa +8.164.049,39
        # EUR -> CONVIENTE.
        n = self._bc(prezzo_eua_eur_t=0.0)
        assert n["valid"] is True
        assert n["risparmio_eur_anno"] == pytest.approx(
            1098000.0, rel=REL)
        assert abs(n["van"] - 8164049.39) <= 1.0
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_zero_payback_zero(self):
        # CAPEX zero: flussi [0, risparmio x 15],
        # VAN positiva, payback 0, TIR None
        # (nessun cambio di segno).
        n = self._bc(capex_eur=0.0)
        assert n["valid"] is True
        assert n["van"] == pytest.approx(
            RISP_DEMO * 9.712248987740992, rel=REL)
        assert n["payback"] == 0
        assert n["tir"] is None
        assert n["verdetto"] == "CONVIENTE"

    def test_wacc_zero_valido_crf_uno_su_n(self):
        n = self._bc(wacc_pct=0.0)
        assert n["valid"] is True
        assert n["crf"] == pytest.approx(
            1.0 / 15.0, rel=REL)
        assert n["van"] == pytest.approx(
            19059162.5, rel=REL)

    def test_movimenti_zero_neutro(self):
        n = self._bc(movimenti_anno=0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_ore_gpu_zero_neutro(self):
        n = self._bc(ore_gpu_per_movimento=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_apu_alt_sopra_base_neutro(self):
        n = self._bc(ore_apu_alt_h=1.5)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_potenza_zero_neutro(self):
        n = self._bc(potenza_egpu_kW=0.0)
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
        n = self._bc(movimenti_anno=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_anno"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(movimenti_anno=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(vita_anni=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_stringa_neutro(self):
        n = self._bc(movimenti_anno="500")
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzo_negativo_neutro(self):
        n = self._bc(prezzo_el_EUR_MWh=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh743_neutro"]()
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
        n = _F["_mh743_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "movimenti_anno",
                       "ore_gpu_per_movimento",
                       "consumo_diesel_L_h",
                       "ore_apu_base_h", "ore_apu_alt_h",
                       "consumo_apu_kg_h",
                       "potenza_egpu_kW",
                       "fattore_diesel_kg_L",
                       "fattore_cherosene_kg_kg",
                       "prezzo_diesel_EUR_L",
                       "prezzo_cherosene_EUR_t",
                       "prezzo_el_EUR_MWh",
                       "fattore_rete_kg_MWh",
                       "prezzo_eua_eur_t",
                       "capex_eur", "wacc_pct",
                       "vita_anni", "tolleranza_pct",
                       "ore_gpu_anno",
                       "diesel_L",
                       "cherosene_base_kg",
                       "cherosene_base_t",
                       "cherosene_alt_kg",
                       "cherosene_alt_t",
                       "energia_el_kwh",
                       "energia_el_MWh",
                       "co2_diesel_t", "co2_apu_base_t",
                       "co2_apu_alt_t", "co2_el_t",
                       "co2_base_t", "co2_alt_t",
                       "co2_risparmiata_t",
                       "costo_diesel_eur",
                       "costo_cherosene_base_eur",
                       "costo_cherosene_alt_eur",
                       "costo_energia_el_eur",
                       "costo_co2_base_eur",
                       "costo_co2_alt_eur",
                       "costo_totale_base_eur",
                       "costo_totale_alt_eur",
                       "risparmio_eur_anno",
                       "risparmio_eur_movimento",
                       "crf", "quota_capex_eur",
                       "costo_annuo_livellato_alt_eur",
                       "costo_livellato_eur_movimento",
                       "costo_totale_base_eur_movimento",
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
        assert len(b["df_tabella"]) == 53
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Ore GPU annue (h/anno)" in voci
        assert "Diesel (L/anno)" in voci
        assert "Cherosene base (t/anno)" in voci
        assert "Cherosene alternativo (t/anno)" in voci
        assert "Energia elettrica (MWh/anno)" in voci
        assert "CO2 diesel (tCO2/anno)" in voci
        assert "CO2 APU base (tCO2/anno)" in voci
        assert "CO2 alternativa (tCO2/anno)" in voci
        assert "CO2 risparmiata (tCO2/anno)" in voci
        assert "Costo totale base (EUR/anno)" in voci
        assert "Costo totale alternativo (EUR/anno)" in voci
        assert "Risparmio (EUR/anno)" in voci
        assert "CRF" in voci
        assert "VAN (EUR)" in voci
        assert "Prezzo elettrico di pareggio (EUR/MWh)" in voci
        assert "Verdetto" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (EUR/anno)",
                                               "Cumulato (EUR)"]
        assert len(b["df_flussi"]) == 16
        assert b["df_flussi"]["Flusso (EUR/anno)"].iloc[0] == \
            pytest.approx(-2500000.0, rel=REL)
        assert b["df_flussi"]["Flusso (EUR/anno)"].iloc[1] == \
            pytest.approx(RISP_DEMO, rel=REL)


class TestCsv:
    def _ing(self):
        return _F["mh743_demo"]()

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh743_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") == 54

    def test_csv_contiene_verdetti_e_costi(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh743_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "capex_eur" in txt
        assert "van_eur" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "prezzo_pareggio_eur_MWh" in txt
        assert "risparmio_eur_anno" in txt
        assert "costo_totale_base_eur" in txt
        assert "ore_gpu_anno" in txt
        assert "co2_risparmiata_t" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh743_csv"](bc, self._ing())
        assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in txt
        assert f"co2_risparmiata_t;{bc['co2_risparmiata_t']}" in txt
        assert "movimenti_anno;12000" in txt
        assert "prezzo_el_EUR_MWh;220.0" in txt
        assert f"costo_livellato_eur_movimento;{bc['costo_livellato_eur_movimento']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def743["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def743\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 18, ui_keys
        demo_keys = set(_F["mh743_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh743_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh743_demo():")
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
        ui_keys = set(re.findall(r'_def743\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W744 (27/10/2026) - tab743' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh743_num", "mh743_nneg", "mh743_pos",
                     "mh743_int_pos", "mh743_pct_0_100",
                     "mh743_pct_wacc",
                     "mh743_ore_gpu_anno", "mh743_diesel_L",
                     "mh743_cherosene_kg", "mh743_cherosene_t",
                     "mh743_energia_el_kwh", "mh743_energia_el_MWh",
                     "mh743_co2_diesel", "mh743_co2_apu",
                     "mh743_co2_el", "mh743_co2_base",
                     "mh743_co2_alt", "mh743_co2_risparmiata",
                     "mh743_costo_diesel",
                     "mh743_costo_cherosene",
                     "mh743_costo_energia_el",
                     "mh743_costo_co2",
                     "mh743_costo_totale_base",
                     "mh743_costo_totale_alt",
                     "mh743_risparmio",
                     "mh743_risparmio_per_movimento",
                     "mh743_crf", "mh743_quota_capex",
                     "mh743_costo_livellato",
                     "mh743_prezzo_pareggio",
                     "mh743_flussi", "mh743_van",
                     "mh743_tir", "mh743_payback",
                     "mh743_verdetto", "mh743_valida",
                     "_mh743_neutro",
                     "mh743_calcola", "mh743_csv",
                     "mh743_demo", "demo_calcoli"):
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
        mh_old = "mh" + "742"
        st_old = "st" + "742"
        tab_old = "tab" + "742"
        w_old = "W" + "743"
        assert mh_old not in _helpers_src()
        assert mh_old not in _ui_src()
        assert st_old not in _ui_src()
        assert tab_old not in _ui_src()
        assert w_old not in _helpers_src()
        assert w_old not in _ui_src()
        assert "mh743" in _helpers_src()
        assert "st743" in _ui_src()

    def test_helpers_parse_ast(self):
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w744_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE743) == 1

    def test_blocco_with_tab743(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab743:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE743

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st743_[A-Za-z0-9_]+)"', _ui_src())
        assert len(keys) == 26, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st743_") for k in keys)

    def test_chiavi_st_input_presenti(self):
        keys = re.findall(r'key="(st743_[A-Za-z0-9_]+)"', _ui_src())
        attese = ["st743_movimenti", "st743_ore_gpu",
                  "st743_consumo_diesel", "st743_potenza",
                  "st743_apu_base", "st743_apu_alt",
                  "st743_consumo_apu", "st743_fattore_diesel",
                  "st743_fattore_cherosene", "st743_fattore_rete",
                  "st743_prezzo_diesel", "st743_prezzo_cherosene",
                  "st743_prezzo_el", "st743_eua", "st743_capex",
                  "st743_wacc", "st743_vita", "st743_tolleranza",
                  "st743_grafico", "st743_show_flussi",
                  "st743_show_tabella", "st743_nota",
                  "st743_ipotesi", "st743_calcola",
                  "st743_csv", "st743_csv_flussi"]
        assert len(attese) == 26
        for k in attese:
            assert k in keys, k

    def test_chiavi_st_niente_fstring_dinamiche(self):
        src = _ui_src()
        assert 'key=f"' not in src
        assert "key=f'" not in src

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg743" in src
        assert "NON_CALCOLABILE" in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg743") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg743")
        assert g < src.index("st.bar_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "CO2 risparmiata (t/anno)" in src
        assert "Risparmio (EUR/anno)" in src
        assert "Costo livellato alternativo (EUR/movimento)" in src
        assert "VAN (kEUR)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON_CALCOLABILE"):
            assert v in src

    def test_distinzioni_presenti(self):
        src = _ui_src()
        assert "aeroporto" in src
        assert "Ground Power Unit" in src
        assert "SAF" in src
        assert "bunker" in src

    def test_distinzioni_in_header_helpers(self):
        src = _helpers_src()
        assert "aeroporto" in src
        assert "Ground Power Unit" in src
        assert "SAF" in src
        assert "bunker" in src

    def test_nota_didattica_presente(self):
        src = _ui_src()
        assert "NOTA DIDATTICA" in src
        assert "15.000" in src
        assert "1.350" in src

    def test_grafico_bar_chart_presente(self):
        src = _ui_src()
        assert "st.bar_chart" in src
        assert "_dati743" in src
        assert '"EUR/anno"' in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh743_csv" in src
        assert "ground_power_aeroporto.csv" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st743_show_flussi" in src
        assert "st.checkbox" in src

    def test_niente_nome(self):
        assert "Emanuele" not in _helpers_src()
        assert "Emanuele" not in _ui_src()

    def test_ancora_helper_presente(self):
        assert "# W744 (27/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab743:")
