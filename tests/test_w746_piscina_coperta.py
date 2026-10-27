"""Test tab746 "Piscina coperta riscaldata: pompa di calore + copertura battono la caldaia a gas?"

Nuova tab tab746 (piscina
coperta, w747). Business case
deterministico di una piscina
COPERTA (indoor): confronta
BASE = caldaia a gas contro ALT
= pompa di calore + copertura
termica (la copertura abbatte
evaporazione e convezione, non
il rinnovo). Fabbisogno da
evaporazione (Magnus), convezione
indoor e rinnovo acqua, energia
da fabbisogno, rendimento caldaia
e COP, CO2 da energia e fattori
di emissione, costi da energia,
O&M e EUA, CAPEX delta da CAPEX
alt meno CAPEX base, VAN, TIR,
payback (primo anno con cumulato
>= 0) e prezzo elettrico di
pareggio. Nessuna altra tab e'
dedicata a una piscina coperta
riscaldata con pompa di calore e
copertura: 0 occorrenze di
"piscina coperta" in app.py
prima di questa tab.

Demo calcolata eseguendo demo_calcoli()
(e ricontrollata a mano, riga per riga):
superficie 250 m2; acqua 28 C e
aria 30 C; RH 60 %; velocita' aria
0,15 m/s; ore annue 4000 h; rinnovo
5 m3/giorno per 300 giorni;
reintegro 10 C; rendimento caldaia
0,90; COP 3,5; share copertura 50 %
con efficacia 85 %; prezzo gas 90
EUR/MWh e prezzo elettricita' 220
EUR/MWh; O&M base 8000 EUR/anno e
alt 12000 EUR/anno; fattore gas 200
kg/MWh e fattore rete 150 kg/MWh;
prezzo EUA 85 EUR/t; CAPEX base
150000 EUR e alt 320000 EUR; WACC
5 %; vita 15 anni; tolleranza 10 %
del CAPEX delta.

- q_evap_kwh = 90157.13459969063
- q_conv_kwh = 0.0
- q_rinnovo_kwh = 31395.0
- q_base_kwh = 121552.13459969063
- f_copertura = 0.575
- q_evap_alt_kwh = 51840.35239482211
- q_conv_alt_kwh = 0.0
- q_rinnovo_alt_kwh = 31395.0
- q_alt_kwh = 83235.35239482211
- e_gas_MWh = 135.05792733298958
- e_el_MWh = 23.78152925566346
- co2_base_t = 27.011585466597918
- co2_alt_t = 3.567229388349519
- co2_risparmiata_t = 23.444356078248397
- costo_energia_base_eur = 12155.213459969062
- costo_energia_alt_eur = 5231.936436245961
- costo_co2_base_eur = 2295.984764660823
- costo_co2_alt_eur = 303.21449800970913
- totale_base_eur = 22451.198224629887
- totale_alt_eur = 17535.150934255667
- risparmio_eur_anno = 4916.047290374219
- risparmio_eur_mwh_th = 40.443940425763046
- capex_delta_eur = 170000.0
- crf = 0.09634228760924432
- quota_capex_eur = 16378.188893571534
- costo_livellato_alt_eur = 33913.3398278272
- costo_livellato_eur_mwh_th = 279.00242097363804
- van = -118973.11022639135
- tir = -8.991471551523942
- payback = None
- prezzo_pareggio_eur_MWh = 426.71703814856573
- verdetto = 'NON_CONVIENTE'

Scomposizione: p_sat(28) = 3,7735 kPa e
p_sat(30) = 4,2367 kPa (Magnus);
p_aria = 0,60 x 4,2367 = 2,5420 kPa;
differenza 1,2315 kPa; m_evap = 250 x
(0,10 + 0,05 x 0,15) x 1,2315 = 33,0973
kg/h; Q_evap = 33,0973 x 0,681 x 4000 =
90157,13 kWh_th; h_conv = 3,5 W/m2K ma
Q_conv = 0 perche' l'aria (30 C) e'
piu' calda dell'acqua (28 C);
Q_rinnovo = 5 x 300 x 1000 x 4,186 x
18 / 3600 = 31395,00 kWh_th; Q_base =
121552,13 kWh_th; f_cop = 1 - 0,50 x
0,85 = 0,575; Q_evap_alt = 51840,35,
Q_conv_alt = 0, Q_rinnovo_alt = 31395,
Q_alt = 83235,35 kWh_th; E_gas =
121552,13 / 0,90 / 1000 = 135,06 MWh;
E_el = 83235,35 / 3,5 / 1000 = 23,78
MWh; CO2 base 135,06 x 200 / 1000 =
27,01 t; CO2 alt 23,78 x 150 / 1000 =
3,57 t; risparmiata 23,44 t; costo
energia base 135,06 x 90 = 12155,21
EUR; costo energia alt 23,78 x 220 =
5231,94 EUR; costo CO2 base 27,01 x
85 = 2295,98 EUR; costo CO2 alt 3,57
x 85 = 303,21 EUR; totali 12155,21 +
8000 + 2295,98 = 22451,20 EUR contro
5231,94 + 12000 + 303,21 = 17535,15
EUR; risparmio 22451,20 - 17535,15 =
4916,05 EUR/anno = 40,44 EUR/MWh_th;
CAPEX delta 320000 - 150000 = 170000
EUR; CRF 0,05 x 1,05^15 / (1,05^15 -
1) = 0.09634228760924432; quota CAPEX
170000 x 0,09634228760924432 =
16378,19 EUR/anno; costo livellato
17535,15 + 16378,19 = 33913,34
EUR/anno = 279,00 EUR/MWh_th; flussi:
anno 0 -170000, anni 1-15 risparmio
4916,05 (piatti); VAN -170000 + 4916,05
x 10,3796580381806 (annuita' 15 anni
al 5 %) = -118973,11 EUR; TIR -8,99 %
(bisezione esatta); payback None
(cumulato anno 15: -170000 + 15 x
4916,05 = -96259,29 EUR, mai >= 0);
prezzo elettrico di pareggio (12155,21
+ 8000 + 2295,98 - 12000 - 303,21) /
23,78 = 426,71703814856573 EUR/MWh;
verdetto NON_CONVIENTE perche' VAN
< 0 e |VAN| = 118973,11 > tolleranza
10 % di 170000 = 17000 EUR.
NOTA: il CRF entra solo nel costo
livellato, mai nei flussi: il
CAPEX delta compare una sola volta,
all'anno 0. NOTA 2: il CAPEX delta
negativo NON e' degenere e il
risparmio nullo o negativo NON e'
degenere: restano calcolabili.
NOTA 3: la demo di questo ciclo e'
NON_CONVIENTE (non CONVIENTE): con
questi prezzi il risparmio annuo
(4916 EUR) non ripaga un delta
CAPEX di 170000 EUR in 15 anni.
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
    if (p / "w747_helpers.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w747_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w747_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w747_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w747_helpers.py: {missing}")
    return out


_F = _load("mh746_num", "mh746_nneg", "mh746_pos",
           "mh746_int_pos", "mh746_int_nneg",
           "mh746_pct_0_100", "mh746_pct_wacc",
           "mh746_temp_acqua", "mh746_temp_aria",
           "mh746_eta", "mh746_cop", "mh746_psat",
           "mh746_p_aria", "mh746_m_evap",
           "mh746_q_evap", "mh746_h_conv",
           "mh746_q_conv", "mh746_q_rinnovo",
           "mh746_q_base", "mh746_f_copertura",
           "mh746_q_alt", "mh746_energia_gas",
           "mh746_energia_el", "mh746_co2",
           "mh746_costo_energia", "mh746_costo_co2",
           "mh746_costo_totale", "mh746_risparmio",
           "mh746_risparmio_per_mwh_th",
           "mh746_capex_delta", "mh746_crf",
           "mh746_quota_capex", "mh746_costo_livellato",
           "mh746_prezzo_pareggio", "mh746_flussi",
           "mh746_van", "mh746_tir", "mh746_payback",
           "mh746_verdetto", "mh746_valida",
           "_mh746_neutro", "mh746_calcola",
           "mh746_csv", "mh746_demo", "demo_calcoli")

TITLE746 = ("🏊♨️ Piscina coperta riscaldata: pompa di calore + copertura battono la caldaia a gas?")

PSAT28 = 3.7735188138198774
PSAT30 = 4.236650251295474
PAIR_DEMO = 2.5419901507772846
MEVAP_DEMO = 33.09733281926969
QE_DEMO = 90157.13459969063
QC_DEMO = 0.0
QR_DEMO = 31395.0
QB_DEMO = 121552.13459969063
FC_DEMO = 0.575
QEA_DEMO = 51840.35239482211
QCA_DEMO = 0.0
QA_DEMO = 83235.35239482211
EG_DEMO = 135.05792733298958
EE_DEMO = 23.78152925566346
CO2_B_DEMO = 27.011585466597918
CO2_A_DEMO = 3.567229388349519
CO2_R_DEMO = 23.444356078248397
CE_B_DEMO = 12155.213459969062
CE_A_DEMO = 5231.936436245961
CC_B_DEMO = 2295.984764660823
CC_A_DEMO = 303.21449800970913
TB_DEMO = 22451.198224629887
TA_DEMO = 17535.150934255667
RISP_DEMO = 4916.047290374219
RPMWH_DEMO = 40.443940425763046
DELTA_DEMO = 170000.0
CRF_DEMO = 0.09634228760924432
QUOTA_DEMO = 16378.188893571534
LIV_DEMO = 33913.3398278272
LIVMWH_DEMO = 279.00242097363804
VAN_DEMO = -118973.11022639135
TIR_DEMO = -8.991471551523942
PAYBACK_DEMO = None
PAR_DEMO = 426.71703814856573
VERDETTO_DEMO = "NON_CONVIENTE"

_DEMO = {
    "area_m2": 250,
    "t_acqua_c": 28,
    "t_aria_c": 30,
    "rh_pct": 60.0,
    "v_ms": 0.15,
    "ore_annue": 4000,
    "v_rinnovo_m3_giorno": 5,
    "giorni_anno": 300,
    "t_reintegro_c": 10,
    "eta_caldaia": 0.90,
    "cop": 3.5,
    "share_copertura_pct": 50.0,
    "eff_copertura_pct": 85.0,
    "p_gas_EUR_MWh": 90,
    "p_el_EUR_MWh": 220,
    "om_base_eur_anno": 8000,
    "om_alt_eur_anno": 12000,
    "f_gas_kg_MWh": 200,
    "f_rete_kg_MWh": 150,
    "prezzo_eua_eur_t": 85,
    "capex_base_eur": 150000,
    "capex_alt_eur": 320000,
    "wacc_pct": 5.0,
    "vita_anni": 15,
    "tolleranza_pct": 10.0,
}

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w747_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w747_ui.py").read_text(encoding="utf-8")


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh746_demo"]()
        d.update(kw)
        return _F["mh746_valida"](**d)

    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh746_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh746_num"]("250", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh746_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh746_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh746_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh746_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh746_pos"](0.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh746_int_pos"](2.5, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh746_int_pos"](15.0, "x") == 15

    def test_int_nneg_accetta_zero_rifiuta_frazione(self):
        assert _F["mh746_int_nneg"](0.0, "x") == 0
        assert _F["mh746_int_nneg"](15.0, "x") == 15
        with pytest.raises(ValueError):
            _F["mh746_int_nneg"](2.5, "x")
        with pytest.raises(ValueError):
            _F["mh746_int_nneg"](-1.0, "x")

    def test_pct_0_100_accetta_estremi_rifiuta_fuori(self):
        assert _F["mh746_pct_0_100"](0.0, "x") == 0.0
        assert _F["mh746_pct_0_100"](100.0, "x") == 100.0
        with pytest.raises(ValueError):
            _F["mh746_pct_0_100"](-0.01, "x")
        with pytest.raises(ValueError):
            _F["mh746_pct_0_100"](100.01, "x")

    def test_pct_wacc_accetta_zero_e_50_rifiuta_oltre(self):
        assert _F["mh746_pct_wacc"](0.0, "x") == 0.0
        assert _F["mh746_pct_wacc"](50.0, "x") == 50.0
        with pytest.raises(ValueError):
            _F["mh746_pct_wacc"](-0.01, "x")
        with pytest.raises(ValueError):
            _F["mh746_pct_wacc"](50.01, "x")

    def test_temp_acqua_range(self):
        assert _F["mh746_temp_acqua"](-10.0, "x") == -10.0
        assert _F["mh746_temp_acqua"](60.0, "x") == 60.0
        with pytest.raises(ValueError):
            _F["mh746_temp_acqua"](-10.01, "x")
        with pytest.raises(ValueError):
            _F["mh746_temp_acqua"](60.01, "x")

    def test_temp_aria_range(self):
        assert _F["mh746_temp_aria"](0.0, "x") == 0.0
        assert _F["mh746_temp_aria"](50.0, "x") == 50.0
        with pytest.raises(ValueError):
            _F["mh746_temp_aria"](-0.01, "x")
        with pytest.raises(ValueError):
            _F["mh746_temp_aria"](50.01, "x")

    def test_eta_range(self):
        assert _F["mh746_eta"](1.0, "x") == 1.0
        with pytest.raises(ValueError):
            _F["mh746_eta"](0.0, "x")
        with pytest.raises(ValueError):
            _F["mh746_eta"](1.01, "x")

    def test_cop_maggiore_di_uno(self):
        assert _F["mh746_cop"](1.01, "x") == 1.01
        with pytest.raises(ValueError):
            _F["mh746_cop"](1.0, "x")
        with pytest.raises(ValueError):
            _F["mh746_cop"](0.5, "x")

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_area_ore_giorni_zero_non_validi(self):
        assert self._val(area_m2=0)["valido"] is False
        assert self._val(ore_annue=0)["valido"] is False
        assert self._val(giorni_anno=0)["valido"] is False

    def test_area_ore_giorni_negativi_non_validi(self):
        assert self._val(area_m2=-1)["valido"] is False
        assert self._val(ore_annue=-100)["valido"] is False
        assert self._val(giorni_anno=-5)["valido"] is False

    def test_temperature_fuori_range_non_valide(self):
        assert self._val(t_acqua_c=61)["valido"] is False
        assert self._val(t_acqua_c=-11)["valido"] is False
        assert self._val(t_aria_c=51)["valido"] is False
        assert self._val(t_aria_c=-1)["valido"] is False
        assert self._val(t_reintegro_c=61)["valido"] is False

    def test_rh_share_eff_fuori_range_non_validi(self):
        assert self._val(rh_pct=100.01)["valido"] is False
        assert self._val(rh_pct=-0.01)["valido"] is False
        assert self._val(share_copertura_pct=100.01)["valido"] is False
        assert self._val(eff_copertura_pct=-0.01)["valido"] is False
        assert self._val(share_copertura_pct=100.0)["valido"] is True

    def test_eta_cop_non_validi(self):
        assert self._val(eta_caldaia=0.0)["valido"] is False
        assert self._val(eta_caldaia=1.01)["valido"] is False
        assert self._val(cop=1.0)["valido"] is False
        assert self._val(cop=0.9)["valido"] is False

    def test_negativi_non_validi(self):
        for k in ("v_ms", "p_gas_EUR_MWh", "p_el_EUR_MWh",
                  "om_base_eur_anno", "om_alt_eur_anno",
                  "f_gas_kg_MWh", "f_rete_kg_MWh",
                  "prezzo_eua_eur_t", "capex_base_eur",
                  "capex_alt_eur"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_vita_zero_e_frazione_non_valide(self):
        assert self._val(vita_anni=0)["valido"] is False
        assert self._val(vita_anni=15.5)["valido"] is False

    def test_wacc_fuori_range_non_validi(self):
        assert self._val(wacc_pct=-0.01)["valido"] is False
        assert self._val(wacc_pct=50.01)["valido"] is False
        assert self._val(wacc_pct=0.0)["valido"] is True

    def test_tolleranza_fuori_range_non_valida(self):
        assert self._val(tolleranza_pct=-0.01)["valido"] is False
        assert self._val(tolleranza_pct=100.01)["valido"] is False

    def test_nan_non_valido(self):
        assert self._val(area_m2=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(area_m2=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(vita_anni=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(area_m2="250")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(p_el_EUR_MWh=0.0)["valido"] is True
        assert self._val(prezzo_eua_eur_t=0.0)["valido"] is True
        assert self._val(tolleranza_pct=0.0)["valido"] is True
        assert self._val(capex_alt_eur=0.0)["valido"] is True
        assert self._val(v_ms=0.0)["valido"] is True
        assert self._val(v_rinnovo_m3_giorno=0.0)["valido"] is True


class TestFunzioni:
    def test_psat_demo_e_zero(self):
        assert _F["mh746_psat"](28) == pytest.approx(
            PSAT28, rel=REL)
        assert _F["mh746_psat"](30) == pytest.approx(
            PSAT30, rel=REL)
        assert _F["mh746_psat"](0) == pytest.approx(
            0.61094, rel=REL)

    def test_psat_formula_letterale(self):
        atteso = 0.61094 * math.exp(17.625 * 20 / (20 + 243.04))
        assert _F["mh746_psat"](20) == pytest.approx(
            atteso, rel=REL)

    def test_p_aria_demo(self):
        assert _F["mh746_p_aria"](
            60.0, 30) == pytest.approx(PAIR_DEMO, rel=REL)

    def test_p_aria_estremi(self):
        assert _F["mh746_p_aria"](0.0, 30) == 0.0
        assert _F["mh746_p_aria"](
            100.0, 30) == pytest.approx(PSAT30, rel=REL)

    def test_m_evap_demo(self):
        assert _F["mh746_m_evap"](
            250, 28, 30, 60.0, 0.15) == pytest.approx(
            MEVAP_DEMO, rel=REL)

    def test_m_evap_clamp_zero_aria_satura(self):
        assert _F["mh746_m_evap"](
            250, 20, 30, 100.0, 0.15) == 0.0
        assert _F["mh746_m_evap"](
            250, 28, 30, 100.0, 0.15) == 0.0

    def test_m_evap_rifiuta_area_zero_e_v_negativa(self):
        with pytest.raises(ValueError):
            _F["mh746_m_evap"](0, 28, 30, 60.0, 0.15)
        with pytest.raises(ValueError):
            _F["mh746_m_evap"](250, 28, 30, 60.0, -0.1)

    def test_q_evap_demo_e_letterale(self):
        assert _F["mh746_q_evap"](
            MEVAP_DEMO, 4000) == pytest.approx(QE_DEMO, rel=REL)
        assert _F["mh746_q_evap"](10.0, 1000) == pytest.approx(
            6810.0, rel=REL)

    def test_h_conv_demo_e_estremi(self):
        assert _F["mh746_h_conv"](0.15) == pytest.approx(
            3.5, rel=REL)
        assert _F["mh746_h_conv"](0.0) == pytest.approx(
            2.0, rel=REL)
        assert _F["mh746_h_conv"](0.2) == pytest.approx(
            4.0, rel=REL)

    def test_q_conv_demo_zero_aria_piu_calda(self):
        assert _F["mh746_q_conv"](
            250, 0.15, 28, 30, 4000) == pytest.approx(
            QC_DEMO, rel=REL)

    def test_q_conv_positiva(self):
        assert _F["mh746_q_conv"](
            250, 0.2, 30, 24, 4000) == pytest.approx(
            24000.0, rel=REL)
        assert _F["mh746_q_conv"](
            100, 0.0, 25, 20, 1000) == pytest.approx(
            1000.0, rel=REL)

    def test_q_rinnovo_demo_e_letterale(self):
        assert _F["mh746_q_rinnovo"](
            5, 300, 28, 10) == pytest.approx(QR_DEMO, rel=REL)
        assert _F["mh746_q_rinnovo"](
            10, 100, 30, 10) == pytest.approx(
            23255.555555555557, rel=REL)

    def test_q_rinnovo_zero_reintegro_caldo(self):
        assert _F["mh746_q_rinnovo"](5, 300, 28, 28) == 0.0
        assert _F["mh746_q_rinnovo"](5, 300, 28, 30) == 0.0

    def test_q_base_demo(self):
        assert _F["mh746_q_base"](
            QE_DEMO, QC_DEMO, QR_DEMO) == pytest.approx(
            QB_DEMO, rel=REL)

    def test_f_copertura_demo_e_estremi(self):
        assert _F["mh746_f_copertura"](
            50.0, 85.0) == pytest.approx(FC_DEMO, rel=REL)
        assert _F["mh746_f_copertura"](0.0, 85.0) == 1.0
        assert _F["mh746_f_copertura"](100.0, 100.0) == 0.0
        assert _F["mh746_f_copertura"](
            100.0, 85.0) == pytest.approx(0.15, rel=REL)

    def test_f_copertura_rifiuta_fuori_range(self):
        with pytest.raises(ValueError):
            _F["mh746_f_copertura"](100.01, 85.0)
        with pytest.raises(ValueError):
            _F["mh746_f_copertura"](50.0, -0.01)

    def test_q_alt_demo(self):
        assert _F["mh746_q_alt"](
            QE_DEMO, QC_DEMO, QR_DEMO, 50.0, 85.0) == pytest.approx(
            QA_DEMO, rel=REL)

    def test_q_alt_share_zero_e_copertura_perfetta(self):
        assert _F["mh746_q_alt"](
            QE_DEMO, QC_DEMO, QR_DEMO, 0.0, 85.0) == pytest.approx(
            QB_DEMO, rel=REL)
        assert _F["mh746_q_alt"](
            QE_DEMO, QC_DEMO, QR_DEMO, 100.0, 100.0) == pytest.approx(
            QR_DEMO, rel=REL)

    def test_energia_gas_demo(self):
        assert _F["mh746_energia_gas"](
            QB_DEMO, 0.90) == pytest.approx(EG_DEMO, rel=REL)

    def test_energia_gas_rifiuta_eta(self):
        with pytest.raises(ValueError):
            _F["mh746_energia_gas"](QB_DEMO, 0.0)
        with pytest.raises(ValueError):
            _F["mh746_energia_gas"](QB_DEMO, 1.01)

    def test_energia_el_demo(self):
        assert _F["mh746_energia_el"](
            QA_DEMO, 3.5) == pytest.approx(EE_DEMO, rel=REL)

    def test_energia_el_rifiuta_cop_minore_uguale_uno(self):
        with pytest.raises(ValueError):
            _F["mh746_energia_el"](QA_DEMO, 1.0)
        with pytest.raises(ValueError):
            _F["mh746_energia_el"](QA_DEMO, 0.5)

    def test_co2_demo(self):
        assert _F["mh746_co2"](
            EG_DEMO, 200) == pytest.approx(CO2_B_DEMO, rel=REL)
        assert _F["mh746_co2"](
            EE_DEMO, 150) == pytest.approx(CO2_A_DEMO, rel=REL)

    def test_costo_energia_demo(self):
        assert _F["mh746_costo_energia"](
            EG_DEMO, 90) == pytest.approx(CE_B_DEMO, rel=REL)
        assert _F["mh746_costo_energia"](
            EE_DEMO, 220) == pytest.approx(CE_A_DEMO, rel=REL)

    def test_costo_co2_demo(self):
        assert _F["mh746_costo_co2"](
            CO2_B_DEMO, 85) == pytest.approx(CC_B_DEMO, rel=REL)

    def test_costo_totale_demo(self):
        assert _F["mh746_costo_totale"](
            CE_B_DEMO, 8000, CC_B_DEMO) == pytest.approx(
            TB_DEMO, rel=REL)
        assert _F["mh746_costo_totale"](
            CE_A_DEMO, 12000, CC_A_DEMO) == pytest.approx(
            TA_DEMO, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh746_risparmio"](
            TB_DEMO, TA_DEMO) == pytest.approx(RISP_DEMO, rel=REL)

    def test_risparmio_negativo_alternativa_piu_cara(self):
        assert _F["mh746_risparmio"](
            1000.0, 2000.0) == pytest.approx(-1000.0, rel=REL)

    def test_risparmio_per_mwh_th_demo(self):
        assert _F["mh746_risparmio_per_mwh_th"](
            RISP_DEMO, QB_DEMO) == pytest.approx(
            RPMWH_DEMO, rel=REL)

    def test_risparmio_per_mwh_th_rifiuta_q_zero(self):
        with pytest.raises(ValueError):
            _F["mh746_risparmio_per_mwh_th"](RISP_DEMO, 0.0)

    def test_capex_delta_demo(self):
        assert _F["mh746_capex_delta"](
            320000, 150000) == pytest.approx(DELTA_DEMO, rel=REL)

    def test_capex_delta_negativo(self):
        assert _F["mh746_capex_delta"](
            100000.0, 150000.0) == pytest.approx(-50000.0, rel=REL)

    def test_crf_demo(self):
        assert _F["mh746_crf"](
            5.0, 15) == pytest.approx(CRF_DEMO, rel=REL)

    def test_crf_wacc_zero_uno_su_n(self):
        assert _F["mh746_crf"](0.0, 15) == pytest.approx(
            1.0 / 15.0, rel=REL)

    def test_crf_formula_indipendente(self):
        r = 0.10
        n = 10
        atteso = r * (1.0 + r) ** n / ((1.0 + r) ** n - 1.0)
        assert _F["mh746_crf"](10.0, 10) == pytest.approx(
            atteso, rel=REL)

    def test_crf_rifiuta_wacc_oltre_50(self):
        with pytest.raises(ValueError):
            _F["mh746_crf"](50.01, 15)

    def test_quota_capex_demo(self):
        assert _F["mh746_quota_capex"](
            DELTA_DEMO, CRF_DEMO) == pytest.approx(
            QUOTA_DEMO, rel=REL)

    def test_quota_capex_delta_negativo(self):
        assert _F["mh746_quota_capex"](
            -50000.0, CRF_DEMO) == pytest.approx(
            -50000.0 * CRF_DEMO, rel=REL)

    def test_costo_livellato_demo(self):
        assert _F["mh746_costo_livellato"](
            TA_DEMO, QUOTA_DEMO) == pytest.approx(LIV_DEMO, rel=REL)

    def test_prezzo_pareggio_demo(self):
        assert _F["mh746_prezzo_pareggio"](
            CE_B_DEMO, 8000, CC_B_DEMO, 12000, CC_A_DEMO,
            EE_DEMO) == pytest.approx(PAR_DEMO, rel=REL)

    def test_prezzo_pareggio_formula_letterale(self):
        # (10000 + 2000 + 1000 - 3000 - 500) / 50 = 190.
        assert _F["mh746_prezzo_pareggio"](
            10000.0, 2000.0, 1000.0, 3000.0, 500.0,
            50.0) == pytest.approx(190.0, rel=REL)

    def test_prezzo_pareggio_none_energia_zero(self):
        assert _F["mh746_prezzo_pareggio"](
            CE_B_DEMO, 8000, CC_B_DEMO, 12000, CC_A_DEMO,
            0.0) is None

    def test_flussi_demo(self):
        flussi = _F["mh746_flussi"](DELTA_DEMO, RISP_DEMO, 15)
        assert len(flussi) == 16
        assert flussi[0] == pytest.approx(-DELTA_DEMO, rel=REL)
        assert all(f == pytest.approx(RISP_DEMO, rel=REL)
                   for f in flussi[1:])

    def test_flussi_delta_negativo_primo_positivo(self):
        flussi = _F["mh746_flussi"](-50000.0, RISP_DEMO, 15)
        assert flussi[0] == pytest.approx(50000.0, rel=REL)

    def test_van_demo(self):
        flussi = _F["mh746_flussi"](DELTA_DEMO, RISP_DEMO, 15)
        assert _F["mh746_van"](
            flussi, 5.0) == pytest.approx(VAN_DEMO, rel=REL)

    def test_van_tasso_zero(self):
        flussi = _F["mh746_flussi"](DELTA_DEMO, RISP_DEMO, 15)
        atteso = -DELTA_DEMO + RISP_DEMO * 15
        assert _F["mh746_van"](
            flussi, 0.0) == pytest.approx(atteso, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh746_van"]([100.0, 100.0], -0.01)

    def test_tir_none_flussi_tutti_negativi(self):
        flussi = _F["mh746_flussi"](DELTA_DEMO, -1000.0, 15)
        assert _F["mh746_tir"](flussi) is None

    def test_tir_none_tutti_flussi_non_negativi(self):
        assert _F["mh746_tir"](
            [0.0] + [1000.0] * 15) is None

    def test_tir_esiste_caso_semplice_100_120(self):
        assert _F["mh746_tir"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_caso_semplice_1000_500_500_zero(self):
        assert abs(_F["mh746_tir"](
            [-1000.0, 500.0, 500.0])) <= 1e-9

    def test_tir_demo(self):
        flussi = _F["mh746_flussi"](DELTA_DEMO, RISP_DEMO, 15)
        assert _F["mh746_tir"](flussi) == pytest.approx(
            TIR_DEMO / 100.0, rel=1e-9)

    def test_payback_demo_none(self):
        flussi = _F["mh746_flussi"](DELTA_DEMO, RISP_DEMO, 15)
        assert _F["mh746_payback"](flussi) is None

    def test_payback_semplice_due(self):
        assert _F["mh746_payback"]([-1000.0, 500.0, 500.0]) == 2

    def test_payback_zero_delta_negativo(self):
        assert _F["mh746_payback"](
            [50000.0, 4916.047290374219]) == 0

    def test_payback_none_mai(self):
        assert _F["mh746_payback"](
            [-170000.0] + [0.0] * 15) is None
        assert _F["mh746_payback"](
            [-170000.0] + [-1000.0] * 15) is None

    def test_payback_equivale_ceil(self):
        # delta 50000, risparmio 4916,05: ceil = 11.
        flussi = _F["mh746_flussi"](50000.0, RISP_DEMO, 15)
        assert _F["mh746_payback"](flussi) == 11
        assert _F["mh746_payback"](flussi) == math.ceil(
            50000.0 / RISP_DEMO)

    def test_verdetto_demo(self):
        assert _F["mh746_verdetto"](
            VAN_DEMO, DELTA_DEMO, 10.0) == VERDETTO_DEMO

    def test_verdetto_conviente_van_positivo(self):
        assert _F["mh746_verdetto"](
            1000.0, DELTA_DEMO, 10.0) == "CONVIENTE"

    def test_verdetto_van_zero_marginale(self):
        assert _F["mh746_verdetto"](
            0.0, DELTA_DEMO, 10.0) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh746_verdetto"](
            -0.10 * DELTA_DEMO, DELTA_DEMO, 10.0) == "MARGINALE"

    def test_verdetto_non_conviente_oltre_limite(self):
        assert _F["mh746_verdetto"](
            -0.10 * DELTA_DEMO - 1.0, DELTA_DEMO,
            10.0) == "NON_CONVIENTE"

    def test_verdetto_delta_negativo_valore_assoluto(self):
        # Delta -50000: tolleranza 10 % = 5000
        # su |delta|; VAN -4000 -> MARGINALE.
        assert _F["mh746_verdetto"](
            -4000.0, -50000.0, 10.0) == "MARGINALE"
        assert _F["mh746_verdetto"](
            -50000.0, -50000.0, 10.0) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_van_nan(self):
        assert _F["mh746_verdetto"](
            float("nan"), DELTA_DEMO, 10.0) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_toll_invalida(self):
        assert _F["mh746_verdetto"](
            1000.0, DELTA_DEMO, 100.01) == "NON_CALCOLABILE"


class TestDemo:
    def _bc(self, **kw):
        d = _F["mh746_demo"]()
        d.update(kw)
        return _F["mh746_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["q_evap_kwh"] == pytest.approx(QE_DEMO, rel=REL)
        assert c["q_conv_kwh"] == pytest.approx(QC_DEMO, rel=REL)
        assert c["q_rinnovo_kwh"] == pytest.approx(QR_DEMO, rel=REL)
        assert c["q_base_kwh"] == pytest.approx(QB_DEMO, rel=REL)
        assert c["f_copertura"] == pytest.approx(FC_DEMO, rel=REL)
        assert c["q_evap_alt_kwh"] == pytest.approx(
            QEA_DEMO, rel=REL)
        assert c["q_conv_alt_kwh"] == pytest.approx(
            QCA_DEMO, rel=REL)
        assert c["q_rinnovo_alt_kwh"] == pytest.approx(
            QR_DEMO, rel=REL)
        assert c["q_alt_kwh"] == pytest.approx(QA_DEMO, rel=REL)
        assert c["e_gas_MWh"] == pytest.approx(EG_DEMO, rel=REL)
        assert c["e_el_MWh"] == pytest.approx(EE_DEMO, rel=REL)
        assert c["co2_base_t"] == pytest.approx(CO2_B_DEMO, rel=REL)
        assert c["co2_alt_t"] == pytest.approx(CO2_A_DEMO, rel=REL)
        assert c["co2_risparmiata_t"] == pytest.approx(
            CO2_R_DEMO, rel=REL)
        assert c["costo_energia_base_eur"] == pytest.approx(
            CE_B_DEMO, rel=REL)
        assert c["costo_energia_alt_eur"] == pytest.approx(
            CE_A_DEMO, rel=REL)
        assert c["costo_co2_base_eur"] == pytest.approx(
            CC_B_DEMO, rel=REL)
        assert c["costo_co2_alt_eur"] == pytest.approx(
            CC_A_DEMO, rel=REL)
        assert c["totale_base_eur"] == pytest.approx(
            TB_DEMO, rel=REL)
        assert c["totale_alt_eur"] == pytest.approx(
            TA_DEMO, rel=REL)
        assert c["risparmio_eur_anno"] == pytest.approx(
            RISP_DEMO, rel=REL)
        assert c["risparmio_eur_mwh_th"] == pytest.approx(
            RPMWH_DEMO, rel=REL)
        assert c["capex_delta_eur"] == pytest.approx(
            DELTA_DEMO, rel=REL)
        assert c["crf"] == pytest.approx(CRF_DEMO, rel=REL)
        assert c["quota_capex_eur"] == pytest.approx(
            QUOTA_DEMO, rel=REL)
        assert c["costo_livellato_alt_eur"] == pytest.approx(
            LIV_DEMO, rel=REL)
        assert c["costo_livellato_eur_mwh_th"] == pytest.approx(
            LIVMWH_DEMO, rel=REL)
        assert c["van"] == pytest.approx(VAN_DEMO, rel=REL)
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
        d = _F["mh746_demo"]()
        for k, v in _DEMO.items():
            assert d[k] == v, k
        assert len(d) == 25

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("q_evap_kwh",
                       "q_conv_kwh",
                       "q_rinnovo_kwh",
                       "q_base_kwh",
                       "f_copertura",
                       "q_evap_alt_kwh",
                       "q_conv_alt_kwh",
                       "q_rinnovo_alt_kwh",
                       "q_alt_kwh",
                       "e_gas_MWh",
                       "e_el_MWh",
                       "co2_base_t",
                       "co2_alt_t",
                       "co2_risparmiata_t",
                       "costo_energia_base_eur",
                       "costo_energia_alt_eur",
                       "costo_co2_base_eur",
                       "costo_co2_alt_eur",
                       "totale_base_eur",
                       "totale_alt_eur",
                       "risparmio_eur_anno",
                       "risparmio_eur_mwh_th",
                       "capex_delta_eur",
                       "crf",
                       "quota_capex_eur",
                       "costo_livellato_alt_eur",
                       "costo_livellato_eur_mwh_th",
                       "van",
                       "tir",
                       "prezzo_pareggio_eur_MWh"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = None" in doc
        assert "verdetto = 'NON_CONVIENTE'" in doc

    def test_prezzo_pareggio_identita(self):
        # Al prezzo di pareggio il risparmio si
        # azzera: 23,78 x 426,72 + 12000 + 303,21
        # = 22451,20 = totale base.
        n = self._bc(p_el_EUR_MWh=426.71703814856573)
        assert n["valid"] is True
        assert n["risparmio_eur_anno"] == pytest.approx(
            0.0, abs=1e-6)
        assert n["van"] == pytest.approx(-170000.0, rel=REL)
        assert n["payback"] is None

    def test_capex_alt_200000_conviente(self):
        # CAPEX alt 200000 EUR: delta 50000 EUR,
        # VAN +1026,89 EUR, payback 11 ->
        # CONVIENTE.
        n = self._bc(capex_alt_eur=200000.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            50000.0, rel=REL)
        assert abs(n["van"] - 1026.89) <= 1.0
        assert n["payback"] == 11
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_alt_205000_marginale(self):
        # CAPEX alt 205000 EUR: delta 55000 EUR,
        # VAN -3973,11 EUR, entro la tolleranza
        # del 10 % del delta (5500 EUR) ->
        # MARGINALE.
        n = self._bc(capex_alt_eur=205000.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            55000.0, rel=REL)
        assert abs(n["van"] + 3973.11) <= 1.0
        assert n["verdetto"] == "MARGINALE"

    def test_capex_alt_100000_delta_negativo_calcolabile(self):
        # CAPEX alt 100000 EUR: delta -50000 EUR
        # (alternativa piu' economica della base):
        # NON degenere, flusso anno 0 positivo,
        # VAN +101026,89 EUR, payback 0,
        # TIR n/d (flussi tutti >= 0) ->
        # CONVIENTE.
        n = self._bc(capex_alt_eur=100000.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            -50000.0, rel=REL)
        assert n["flussi"][0] == pytest.approx(
            50000.0, rel=REL)
        assert abs(n["van"] - 101026.89) <= 1.0
        assert n["payback"] == 0
        assert n["tir"] is None
        assert n["verdetto"] == "CONVIENTE"

    def test_cop_15_risparmio_negativo_calcolabile(self):
        # COP 1,5: energia alt 55,49 MWh,
        # totale alt 24915,35 EUR, risparmio
        # -2464,15 EUR/anno (NON degenere),
        # VAN -195577,08 EUR -> NON_CONVIENTE.
        n = self._bc(cop=1.5)
        assert n["valid"] is True
        assert n["e_el_MWh"] == pytest.approx(55.49, rel=1e-3)
        assert n["risparmio_eur_anno"] == pytest.approx(
            -2464.15, rel=1e-3)
        assert abs(n["van"] + 195577.08) <= 1.0
        assert n["payback"] is None
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_share_zero_e_cento_calcolabili(self):
        n0 = self._bc(share_copertura_pct=0.0)
        assert n0["valid"] is True
        assert n0["q_alt_kwh"] == pytest.approx(QB_DEMO, rel=REL)
        assert n0["e_el_MWh"] == pytest.approx(34.73, rel=1e-3)
        assert abs(n0["van"] + 145421.16) <= 1.0
        assert n0["verdetto"] == "NON_CONVIENTE"
        n100 = self._bc(share_copertura_pct=100.0)
        assert n100["valid"] is True
        assert n100["q_alt_kwh"] == pytest.approx(
            44918.57, rel=1e-3)
        assert n100["e_el_MWh"] == pytest.approx(12.83, rel=1e-3)
        assert abs(n100["van"] + 92525.06) <= 1.0
        assert n100["verdetto"] == "NON_CONVIENTE"

    def test_prezzo_eua_zero(self):
        # Prezzo EUA 0: totali senza CO2,
        # base 20155,21 EUR (12155,21 + 8000) e
        # alt 17231,94 EUR (5231,94 + 12000),
        # risparmio 2923,27 EUR/anno.
        n = self._bc(prezzo_eua_eur_t=0.0)
        assert n["valid"] is True
        assert n["risparmio_eur_anno"] == pytest.approx(
            2923.27, rel=1e-3)
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_wacc_zero_valido_crf_uno_su_n(self):
        n = self._bc(wacc_pct=0.0)
        assert n["valid"] is True
        assert n["crf"] == pytest.approx(
            1.0 / 15.0, rel=REL)
        assert n["quota_capex_eur"] == pytest.approx(
            11333.33, rel=1e-3)
        assert n["van"] == pytest.approx(
            -96259.29, rel=1e-3)

    def test_q_base_zero_neutro(self):
        # Acqua 20 C, aria 30 C satura, reintegro
        # 25 C: evaporazione clamp 0, convezione 0,
        # rinnovo 0 -> Q_base 0.
        n = self._bc(t_acqua_c=20, t_aria_c=30, rh_pct=100.0,
                     t_reintegro_c=25)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_e_el_zero_neutro(self):
        # Copertura perfetta sempre chiusa e
        # reintegro a temperatura vasca: Q_alt 0.
        n = self._bc(share_copertura_pct=100.0,
                     eff_copertura_pct=100.0, t_reintegro_c=28)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_area_zero_neutro(self):
        n = self._bc(area_m2=0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_ore_zero_neutro(self):
        n = self._bc(ore_annue=0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_giorni_zero_neutro(self):
        n = self._bc(giorni_anno=0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_eta_cop_neutri(self):
        for kw in ({"eta_caldaia": 0.0}, {"eta_caldaia": 1.01},
                   {"cop": 1.0}, {"cop": 0.5}):
            n = self._bc(**kw)
            assert n["verdetto"] == "NON_CALCOLABILE", kw
            assert n["valid"] is False

    def test_temperature_neutre(self):
        for kw in ({"t_acqua_c": 61}, {"t_acqua_c": -11},
                   {"t_aria_c": 51}, {"t_aria_c": -1},
                   {"rh_pct": 101.0}, {"v_ms": -0.1},
                   {"share_copertura_pct": 110.0}):
            n = self._bc(**kw)
            assert n["verdetto"] == "NON_CALCOLABILE", kw
            assert n["valid"] is False

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_negativo_neutro(self):
        n = self._bc(wacc_pct=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_oltre_50_neutro(self):
        n = self._bc(wacc_pct=50.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_oltre_100_neutro(self):
        n = self._bc(tolleranza_pct=100.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(area_m2=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_anno"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(area_m2=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(vita_anni=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_stringa_neutro(self):
        n = self._bc(area_m2="250")
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzo_negativo_neutro(self):
        n = self._bc(p_el_EUR_MWh=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh746_neutro"]()
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
        n = _F["_mh746_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "area_m2", "t_acqua_c",
                       "t_aria_c", "rh_pct", "v_ms",
                       "ore_annue", "v_rinnovo_m3_giorno",
                       "giorni_anno", "t_reintegro_c",
                       "eta_caldaia", "cop",
                       "share_copertura_pct",
                       "eff_copertura_pct",
                       "p_gas_EUR_MWh", "p_el_EUR_MWh",
                       "om_base_eur_anno",
                       "om_alt_eur_anno",
                       "f_gas_kg_MWh", "f_rete_kg_MWh",
                       "prezzo_eua_eur_t",
                       "capex_base_eur",
                       "capex_alt_eur",
                       "wacc_pct", "vita_anni",
                       "tolleranza_pct",
                       "q_evap_kwh", "q_conv_kwh",
                       "q_rinnovo_kwh", "q_base_kwh",
                       "f_copertura",
                       "q_evap_alt_kwh", "q_conv_alt_kwh",
                       "q_rinnovo_alt_kwh", "q_alt_kwh",
                       "e_gas_MWh", "e_el_MWh",
                       "co2_base_t", "co2_alt_t",
                       "co2_risparmiata_t",
                       "costo_energia_base_eur",
                       "costo_energia_alt_eur",
                       "costo_co2_base_eur",
                       "costo_co2_alt_eur",
                       "totale_base_eur",
                       "totale_alt_eur",
                       "risparmio_eur_anno",
                       "risparmio_eur_mwh_th",
                       "capex_delta_eur",
                       "crf", "quota_capex_eur",
                       "costo_livellato_alt_eur",
                       "costo_livellato_eur_mwh_th",
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
        assert len(b["df_tabella"]) == 57
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Evaporazione (kWh_th/anno)" in voci
        assert "Convezione (kWh_th/anno)" in voci
        assert "Rinnovo (kWh_th/anno)" in voci
        assert "Fabbisogno base (kWh_th/anno)" in voci
        assert "Fattore copertura" in voci
        assert "Energia gas base (MWh/anno)" in voci
        assert "Energia elettrica alt (MWh/anno)" in voci
        assert "CO2 base (tCO2/anno)" in voci
        assert "CO2 alt (tCO2/anno)" in voci
        assert "CO2 risparmiata (tCO2/anno)" in voci
        assert "Costo totale base (EUR/anno)" in voci
        assert "Costo totale alt (EUR/anno)" in voci
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
            pytest.approx(-DELTA_DEMO, rel=REL)
        assert b["df_flussi"]["Flusso (EUR/anno)"].iloc[1] == \
            pytest.approx(RISP_DEMO, rel=REL)

    def test_crf_solo_livellato_non_nei_flussi(self):
        # I flussi contengono solo -delta e
        # risparmio: la quota CRF non compare
        # mai nei flussi (contarla anche li'
        # conterebbe il CAPEX due volte).
        c = self._bc()
        assert c["flussi"][0] == pytest.approx(
            -DELTA_DEMO, rel=REL)
        assert all(f == pytest.approx(RISP_DEMO, rel=REL)
                   for f in c["flussi"][1:])
        assert c["quota_capex_eur"] == pytest.approx(
            QUOTA_DEMO, rel=REL)
        assert c["costo_livellato_alt_eur"] == pytest.approx(
            TA_DEMO + QUOTA_DEMO, rel=REL)


class TestCsv:
    def _ing(self):
        return _F["mh746_demo"]()

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh746_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") == 58
        assert len(txt.strip().splitlines()) == 58

    def test_csv_contiene_verdetti_e_costi(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh746_csv"](bc, self._ing())
        assert "verdetto;NON_CONVIENTE" in txt
        assert "capex_delta_eur" in txt
        assert "van_eur" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "prezzo_pareggio_eur_MWh" in txt
        assert "risparmio_eur_anno" in txt
        assert "totale_alt_eur" in txt
        assert "q_base_kwh" in txt
        assert "co2_risparmiata_t" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh746_csv"](bc, self._ing())
        assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in txt
        assert f"co2_risparmiata_t;{bc['co2_risparmiata_t']}" in txt
        assert "area_m2;250" in txt
        assert "p_el_EUR_MWh;220" in txt
        assert f"costo_livellato_eur_mwh_th;{bc['costo_livellato_eur_mwh_th']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def746["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def746\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 25, ui_keys
        demo_keys = set(_F["mh746_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh746_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh746_demo():")
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
        ui_keys = set(re.findall(r'_def746\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W747 (27/10/2026) - tab746' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh746_num", "mh746_nneg", "mh746_pos",
                     "mh746_int_pos", "mh746_int_nneg",
                     "mh746_pct_0_100", "mh746_pct_wacc",
                     "mh746_temp_acqua", "mh746_temp_aria",
                     "mh746_eta", "mh746_cop", "mh746_psat",
                     "mh746_p_aria", "mh746_m_evap",
                     "mh746_q_evap", "mh746_h_conv",
                     "mh746_q_conv", "mh746_q_rinnovo",
                     "mh746_q_base", "mh746_f_copertura",
                     "mh746_q_alt", "mh746_energia_gas",
                     "mh746_energia_el", "mh746_co2",
                     "mh746_costo_energia", "mh746_costo_co2",
                     "mh746_costo_totale", "mh746_risparmio",
                     "mh746_risparmio_per_mwh_th",
                     "mh746_capex_delta", "mh746_crf",
                     "mh746_quota_capex", "mh746_costo_livellato",
                     "mh746_prezzo_pareggio",
                     "mh746_flussi", "mh746_van",
                     "mh746_tir", "mh746_payback",
                     "mh746_verdetto", "mh746_valida",
                     "_mh746_neutro",
                     "mh746_calcola", "mh746_csv",
                     "mh746_demo", "demo_calcoli"):
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
        mh_old = "mh" + "745"
        st_old = "st" + "745"
        tab_old = "tab" + "745"
        w_old = "W" + "746"
        assert mh_old not in _helpers_src()
        assert mh_old not in _ui_src()
        assert st_old not in _ui_src()
        assert tab_old not in _ui_src()
        assert w_old not in _helpers_src()
        assert w_old not in _ui_src()
        assert "mh746" in _helpers_src()
        assert "st746" in _ui_src()

    def test_helpers_parse_ast(self):
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w747_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE746) == 1

    def test_blocco_with_tab746(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab746:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE746

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st746_[A-Za-z0-9_]+)"', _ui_src())
        assert len(keys) == 33, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st746_") for k in keys)

    def test_chiavi_st_input_presenti(self):
        keys = re.findall(r'key="(st746_[A-Za-z0-9_]+)"', _ui_src())
        attese = ["st746_area", "st746_t_acqua",
                  "st746_t_aria", "st746_rh",
                  "st746_v", "st746_ore",
                  "st746_v_rinnovo", "st746_giorni",
                  "st746_t_reintegro", "st746_eta",
                  "st746_cop", "st746_share",
                  "st746_eff", "st746_p_gas",
                  "st746_p_el", "st746_om_base",
                  "st746_om_alt", "st746_f_gas",
                  "st746_f_rete", "st746_eua",
                  "st746_capex_base", "st746_capex_alt",
                  "st746_wacc", "st746_vita",
                  "st746_tolleranza", "st746_grafico",
                  "st746_show_flussi", "st746_show_tabella",
                  "st746_nota", "st746_ipotesi",
                  "st746_calcola", "st746_csv",
                  "st746_csv_flussi"]
        assert len(attese) == 33
        for k in attese:
            assert k in keys, k

    def test_chiavi_st_niente_fstring_dinamiche(self):
        src = _ui_src()
        assert 'key=f"' not in src
        assert "key=f'" not in src

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg746" in src
        assert "NON_CALCOLABILE" in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg746") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg746")
        assert g < src.index("st.bar_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Risparmio (EUR/anno)" in src
        assert "VAN (kEUR)" in src
        assert "CO2 risparmiata (t/anno)" in src
        assert "Costo livellato alternativo (EUR/MWh_th)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON_CALCOLABILE"):
            assert v in src

    def test_distinzioni_presenti(self):
        src = _ui_src()
        assert "piscina coperta" in src
        assert "impianti termici generici" in src

    def test_distinzioni_in_header_helpers(self):
        src = _helpers_src()
        assert "piscina coperta" in src
        assert "impianti termici generici" in src

    def test_nota_didattica_presente(self):
        src = _ui_src()
        assert "NOTA DIDATTICA" in src
        assert "90.157,13" in src
        assert "33.913,34" in src

    def test_grafico_bar_chart_presente(self):
        src = _ui_src()
        assert "st.bar_chart" in src
        assert "_dati746" in src
        assert '"EUR/anno"' in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh746_csv" in src
        assert "piscina_coperta.csv" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st746_show_flussi" in src
        assert "st.checkbox" in src

    def test_niente_nome(self):
        assert "Emanuele" not in _helpers_src()
        assert "Emanuele" not in _ui_src()

    def test_ancora_helper_presente(self):
        assert "# W747 (27/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab746:")
