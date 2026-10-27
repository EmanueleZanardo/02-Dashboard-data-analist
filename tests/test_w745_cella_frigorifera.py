"""Test tab745 "Cella frigorifera: free-cooling e pompa di calore battono il gruppo tradizionale?"

Nuova tab tab745 (cella
frigorifera, w746). Business case
deterministico di una cella /
magazzino frigorifero: confronta
BASE = gruppo frigorifero
tradizionale contro ALT = pompa
di calore + free-cooling (quota
di ore in free-cooling con COP da
soli ventilatori). Fabbisogno da
potenza e ore equivalenti,
energia da fabbisogno e COP, CO2
da energia e fattore di rete,
costi da energia, O&M e EUA,
CAPEX delta da CAPEX alt meno
CAPEX base, VAN, TIR, payback
(primo anno con cumulato >= 0) e
prezzo elettrico di pareggio.
Nessuna altra tab e' dedicata a
una cella o magazzino frigorifero
con free-cooling: 0 occorrenze di
"cella frigorifera" e 0 di
"magazzino frigorifero" in app.py
prima di questa tab; la tab sulla
centrale frigorifera riguarda la
produzione centralizzata di
freddo per una rete, non una
singola cella con free-cooling.

Demo calcolata eseguendo demo_calcoli()
(e ricontrollata a mano, riga per riga):
potenza 200 kW; ore equivalenti
6000 h/anno; COP base 2,5; COP
alternativa 4,0; quota free-cooling
30 %; COP free-cooling 12; prezzo
elettricita' 220 EUR/MWh; O&M base
12000 EUR/anno e alt 18000 EUR/anno;
fattore rete 150 kg/MWh; prezzo EUA
85 EUR/t; CAPEX base 300000 EUR e
alt 520000 EUR; WACC 5 %; vita 15
anni; tolleranza 10 % del CAPEX delta.

- q_frig_kwh = 1200000.0
- e_base_MWh = 480.0
- e_alt_MWh = 239.99999999999997
- co2_base_t = 72.0
- co2_alt_t = 35.99999999999999
- co2_risparmiata_t = 36.00000000000001
- costo_energia_base_eur = 105600.0
- costo_energia_alt_eur = 52799.99999999999
- costo_co2_base_eur = 6120.0
- costo_co2_alt_eur = 3059.9999999999995
- totale_base_eur = 123720.0
- totale_alt_eur = 73860.0
- risparmio_eur_anno = 49860.0
- risparmio_eur_mwh_f = 41.55
- capex_delta_eur = 220000.0
- crf = 0.09634228760924432
- quota_capex_eur = 21195.30327403375
- costo_livellato_alt_eur = 95055.30327403375
- costo_livellato_eur_mwh_f = 79.21275272836147
- van = 297529.7497836842
- tir = 21.4325020340413
- payback = 5
- prezzo_pareggio_eur_MWh = 12.249999999999996
- verdetto = 'CONVIENTE'

Scomposizione: fabbisogno 200 x 6000 =
1200000.0 kWh_f; energia base
1200000.0 / 2,5 / 1000 = 480.0 MWh;
energia alt 1200000.0 x (0,70 / 4,0 +
0,30 / 12) / 1000 = 240.0 MWh; CO2 base
480.0 x 150 / 1000 = 72.0 t; CO2 alt
240.0 x 150 / 1000 = 36.0 t; risparmiata
72.0 - 36.0 = 36.0 t; costo energia base
480.0 x 220 = 105600.0 EUR; costo energia
alt 240.0 x 220 = 52800.0 EUR; costo CO2
base 72.0 x 85 = 6120.0 EUR; costo CO2
alt 36.0 x 85 = 3060.0 EUR; totali
105600.0 + 12000 + 6120.0 = 123720.0 EUR
contro 52800.0 + 18000 + 3060.0 = 73860.0
EUR; risparmio 123720.0 - 73860.0 =
49860.0 EUR/anno = 41.55 EUR/MWh_f;
CAPEX delta 520000.0 - 300000.0 =
220000.0 EUR; CRF 0,05 x 1,05^15 /
(1,05^15 - 1) = 0.09634228760924432;
quota CAPEX 220000.0 x 0.09634228760924432
= 21195.30327403375 EUR/anno; costo
livellato 73860.0 + 21195.30327403375 =
95055.30327403375 EUR/anno =
79.21275272836147 EUR/MWh_f; flussi:
anno 0 -220000.0, anni 1-15 risparmio
49860.0 (piatti); VAN -220000.0 +
49860.0 x 10.3796580381806 (annuita'
15 anni al 5 %) = 297529.7497836842 EUR;
TIR 21.4325020340413 % (bisezione esatta:
la stima 20,5 % del brief era
approssimata); payback 5 (cumulato
anno 4 -20560.0, anno 5 +29300.0);
prezzo elettrico di pareggio (18000 -
12000) / (480.0 - 240.0) - 150 x 85 /
1000 = 12.249999999999996 EUR/MWh;
verdetto CONVIENTE perche' VAN > 0.
NOTA: il CRF entra solo nel costo
livellato, mai nei flussi: il
CAPEX delta compare una sola volta,
all'anno 0. NOTA 2: il CAPEX delta
negativo NON e' degenere e il
risparmio nullo o negativo NON e'
degenere: restano calcolabili.
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
    if (p / "w746_helpers.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w746_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w746_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w746_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w746_helpers.py: {missing}")
    return out


_F = _load("mh745_num", "mh745_nneg", "mh745_pos",
           "mh745_int_pos", "mh745_int_nneg",
           "mh745_pct_0_100", "mh745_pct_wacc",
           "mh745_q_frig", "mh745_energia_base",
           "mh745_energia_alt", "mh745_co2",
           "mh745_costo_energia", "mh745_costo_co2",
           "mh745_costo_totale", "mh745_risparmio",
           "mh745_risparmio_per_mwh_f",
           "mh745_capex_delta", "mh745_crf",
           "mh745_quota_capex", "mh745_costo_livellato",
           "mh745_prezzo_pareggio", "mh745_flussi",
           "mh745_van", "mh745_tir", "mh745_payback",
           "mh745_verdetto", "mh745_valida",
           "_mh745_neutro", "mh745_calcola",
           "mh745_csv", "mh745_demo", "demo_calcoli")

TITLE745 = ("❄️🏭 Cella frigorifera: free-cooling e pompa di calore battono il gruppo tradizionale?")

Q_DEMO = 1200000.0
EB_DEMO = 480.0
EA_DEMO = 240.0
CO2_B_DEMO = 72.0
CO2_A_DEMO = 36.0
CO2_R_DEMO = 36.0
CE_B_DEMO = 105600.0
CE_A_DEMO = 52800.0
CC_B_DEMO = 6120.0
CC_A_DEMO = 3060.0
TB_DEMO = 123720.0
TA_DEMO = 73860.0
RISP_DEMO = 49860.0
RPMWH_DEMO = 41.55
DELTA_DEMO = 220000.0
CRF_DEMO = 0.09634228760924432
QUOTA_DEMO = 21195.30327403375
LIV_DEMO = 95055.30327403375
LIVMWH_DEMO = 79.21275272836147
VAN_DEMO = 297529.7497836842
TIR_DEMO = 21.4325020340413
PAYBACK_DEMO = 5
PAR_DEMO = 12.249999999999996
VERDETTO_DEMO = "CONVIENTE"

_DEMO = {
    "p_frig_kw": 200,
    "ore_eq_anno": 6000,
    "cop_base": 2.5,
    "cop_alt": 4.0,
    "share_fc_pct": 30.0,
    "cop_fc": 12,
    "prezzo_el_EUR_MWh": 220,
    "om_base_eur_anno": 12000,
    "om_alt_eur_anno": 18000,
    "fattore_rete_kg_MWh": 150,
    "prezzo_eua_eur_t": 85,
    "capex_base_eur": 300000,
    "capex_alt_eur": 520000,
    "wacc_pct": 5.0,
    "vita_anni": 15,
    "tolleranza_pct": 10.0,
}

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w746_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w746_ui.py").read_text(encoding="utf-8")


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh745_demo"]()
        d.update(kw)
        return _F["mh745_valida"](**d)

    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh745_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh745_num"]("500", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh745_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh745_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh745_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh745_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh745_pos"](0.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh745_int_pos"](2.5, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh745_int_pos"](15.0, "x") == 15

    def test_int_nneg_accetta_zero_rifiuta_frazione(self):
        assert _F["mh745_int_nneg"](0.0, "x") == 0
        assert _F["mh745_int_nneg"](15.0, "x") == 15
        with pytest.raises(ValueError):
            _F["mh745_int_nneg"](2.5, "x")
        with pytest.raises(ValueError):
            _F["mh745_int_nneg"](-1.0, "x")

    def test_pct_0_100_accetta_estremi_rifiuta_fuori(self):
        assert _F["mh745_pct_0_100"](0.0, "x") == 0.0
        assert _F["mh745_pct_0_100"](100.0, "x") == 100.0
        with pytest.raises(ValueError):
            _F["mh745_pct_0_100"](-0.01, "x")
        with pytest.raises(ValueError):
            _F["mh745_pct_0_100"](100.01, "x")

    def test_pct_wacc_accetta_zero_e_50_rifiuta_oltre(self):
        assert _F["mh745_pct_wacc"](0.0, "x") == 0.0
        assert _F["mh745_pct_wacc"](50.0, "x") == 50.0
        with pytest.raises(ValueError):
            _F["mh745_pct_wacc"](-0.01, "x")
        with pytest.raises(ValueError):
            _F["mh745_pct_wacc"](50.01, "x")

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_potenza_ore_zero_passano_validazione(self):
        assert self._val(p_frig_kw=0)["valido"] is True
        assert self._val(ore_eq_anno=0)["valido"] is True

    def test_potenza_ore_negative_non_valide(self):
        assert self._val(p_frig_kw=-1)["valido"] is False
        assert self._val(ore_eq_anno=-100)["valido"] is False

    def test_cop_zero_non_validi(self):
        assert self._val(cop_base=0.0)["valido"] is False
        assert self._val(cop_alt=0.0)["valido"] is False
        assert self._val(cop_fc=0.0)["valido"] is False

    def test_share_fuori_range_non_valida(self):
        assert self._val(share_fc_pct=-0.01)["valido"] is False
        assert self._val(share_fc_pct=100.01)["valido"] is False
        assert self._val(share_fc_pct=100.0)["valido"] is True

    def test_negativi_non_validi(self):
        for k in ("prezzo_el_EUR_MWh", "om_base_eur_anno",
                  "om_alt_eur_anno", "fattore_rete_kg_MWh",
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
        assert self._val(p_frig_kw=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(p_frig_kw=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(vita_anni=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(p_frig_kw="200")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(prezzo_el_EUR_MWh=0.0)["valido"] is True
        assert self._val(prezzo_eua_eur_t=0.0)["valido"] is True
        assert self._val(tolleranza_pct=0.0)["valido"] is True
        assert self._val(capex_alt_eur=0.0)["valido"] is True


class TestFunzioni:
    def test_q_frig_demo(self):
        assert _F["mh745_q_frig"](
            200, 6000) == pytest.approx(Q_DEMO, rel=REL)

    def test_q_frig_formula_letterale(self):
        assert _F["mh745_q_frig"](
            100, 1000) == pytest.approx(100000.0, rel=REL)

    def test_q_frig_zero(self):
        assert _F["mh745_q_frig"](0, 6000) == 0.0

    def test_energia_base_demo(self):
        assert _F["mh745_energia_base"](
            Q_DEMO, 2.5) == pytest.approx(EB_DEMO, rel=REL)

    def test_energia_alt_demo(self):
        assert _F["mh745_energia_alt"](
            Q_DEMO, 4.0, 30.0, 12) == pytest.approx(
            EA_DEMO, rel=REL)

    def test_energia_alt_share_zero(self):
        assert _F["mh745_energia_alt"](
            Q_DEMO, 4.0, 0.0, 12) == pytest.approx(
            300.0, rel=REL)

    def test_energia_alt_share_cento(self):
        assert _F["mh745_energia_alt"](
            Q_DEMO, 4.0, 100.0, 12) == pytest.approx(
            100.0, rel=REL)

    def test_energia_alt_rifiuta_cop_zero(self):
        with pytest.raises(ValueError):
            _F["mh745_energia_alt"](Q_DEMO, 0.0, 30.0, 12)
        with pytest.raises(ValueError):
            _F["mh745_energia_alt"](Q_DEMO, 4.0, 30.0, 0.0)

    def test_energia_alt_rifiuta_share_fuori(self):
        with pytest.raises(ValueError):
            _F["mh745_energia_alt"](Q_DEMO, 4.0, 100.01, 12)

    def test_co2_demo(self):
        assert _F["mh745_co2"](
            EB_DEMO, 150) == pytest.approx(CO2_B_DEMO, rel=REL)
        assert _F["mh745_co2"](
            EA_DEMO, 150) == pytest.approx(CO2_A_DEMO, rel=REL)

    def test_costo_energia_demo(self):
        assert _F["mh745_costo_energia"](
            EB_DEMO, 220) == pytest.approx(CE_B_DEMO, rel=REL)
        assert _F["mh745_costo_energia"](
            EA_DEMO, 220) == pytest.approx(CE_A_DEMO, rel=REL)

    def test_costo_co2_demo(self):
        assert _F["mh745_costo_co2"](
            CO2_B_DEMO, 85) == pytest.approx(CC_B_DEMO, rel=REL)

    def test_costo_totale_demo(self):
        assert _F["mh745_costo_totale"](
            CE_B_DEMO, 12000, CC_B_DEMO) == pytest.approx(
            TB_DEMO, rel=REL)
        assert _F["mh745_costo_totale"](
            CE_A_DEMO, 18000, CC_A_DEMO) == pytest.approx(
            TA_DEMO, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh745_risparmio"](
            TB_DEMO, TA_DEMO) == pytest.approx(RISP_DEMO, rel=REL)

    def test_risparmio_negativo_alternativa_piu_cara(self):
        assert _F["mh745_risparmio"](
            1000.0, 2000.0) == pytest.approx(-1000.0, rel=REL)

    def test_risparmio_per_mwh_f_demo(self):
        assert _F["mh745_risparmio_per_mwh_f"](
            RISP_DEMO, Q_DEMO) == pytest.approx(
            RPMWH_DEMO, rel=REL)

    def test_risparmio_per_mwh_f_rifiuta_q_zero(self):
        with pytest.raises(ValueError):
            _F["mh745_risparmio_per_mwh_f"](RISP_DEMO, 0.0)

    def test_capex_delta_demo(self):
        assert _F["mh745_capex_delta"](
            520000, 300000) == pytest.approx(DELTA_DEMO, rel=REL)

    def test_capex_delta_negativo(self):
        assert _F["mh745_capex_delta"](
            200000.0, 300000.0) == pytest.approx(-100000.0, rel=REL)

    def test_crf_demo(self):
        assert _F["mh745_crf"](
            5.0, 15) == pytest.approx(CRF_DEMO, rel=REL)

    def test_crf_wacc_zero_uno_su_n(self):
        assert _F["mh745_crf"](0.0, 15) == pytest.approx(
            1.0 / 15.0, rel=REL)

    def test_crf_formula_indipendente(self):
        r = 0.10
        n = 10
        atteso = r * (1.0 + r) ** n / ((1.0 + r) ** n - 1.0)
        assert _F["mh745_crf"](10.0, 10) == pytest.approx(
            atteso, rel=REL)

    def test_crf_rifiuta_wacc_oltre_50(self):
        with pytest.raises(ValueError):
            _F["mh745_crf"](50.01, 15)

    def test_quota_capex_demo(self):
        assert _F["mh745_quota_capex"](
            DELTA_DEMO, CRF_DEMO) == pytest.approx(
            QUOTA_DEMO, rel=REL)

    def test_quota_capex_delta_negativo(self):
        assert _F["mh745_quota_capex"](
            -100000.0, CRF_DEMO) == pytest.approx(
            -100000.0 * CRF_DEMO, rel=REL)

    def test_costo_livellato_demo(self):
        assert _F["mh745_costo_livellato"](
            TA_DEMO, QUOTA_DEMO) == pytest.approx(LIV_DEMO, rel=REL)

    def test_prezzo_pareggio_demo(self):
        assert _F["mh745_prezzo_pareggio"](
            18000, 12000, EB_DEMO, EA_DEMO, 150,
            85) == pytest.approx(PAR_DEMO, rel=REL)

    def test_prezzo_pareggio_formula_letterale(self):
        # (20000 - 10000) / (500 - 250) - 200 x 50 / 1000 = 30.
        assert _F["mh745_prezzo_pareggio"](
            20000.0, 10000.0, 500.0, 250.0,
            200.0, 50.0) == pytest.approx(30.0, rel=REL)

    def test_prezzo_pareggio_none_base_minore_uguale_alt(self):
        assert _F["mh745_prezzo_pareggio"](
            18000, 12000, 240.0, 240.0, 150, 85) is None
        assert _F["mh745_prezzo_pareggio"](
            18000, 12000, 240.0, 590.0, 150, 85) is None

    def test_flussi_demo(self):
        flussi = _F["mh745_flussi"](DELTA_DEMO, RISP_DEMO, 15)
        assert len(flussi) == 16
        assert flussi[0] == pytest.approx(-DELTA_DEMO, rel=REL)
        assert all(f == pytest.approx(RISP_DEMO, rel=REL)
                   for f in flussi[1:])

    def test_flussi_delta_negativo_primo_positivo(self):
        flussi = _F["mh745_flussi"](-100000.0, RISP_DEMO, 15)
        assert flussi[0] == pytest.approx(100000.0, rel=REL)

    def test_van_demo(self):
        flussi = _F["mh745_flussi"](DELTA_DEMO, RISP_DEMO, 15)
        assert _F["mh745_van"](
            flussi, 5.0) == pytest.approx(VAN_DEMO, rel=REL)

    def test_van_tasso_zero(self):
        flussi = _F["mh745_flussi"](DELTA_DEMO, RISP_DEMO, 15)
        atteso = -DELTA_DEMO + RISP_DEMO * 15
        assert _F["mh745_van"](
            flussi, 0.0) == pytest.approx(atteso, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh745_van"]([100.0, 100.0], -0.01)

    def test_tir_none_flussi_tutti_negativi(self):
        flussi = _F["mh745_flussi"](DELTA_DEMO, -1000.0, 15)
        assert _F["mh745_tir"](flussi) is None

    def test_tir_none_tutti_flussi_non_negativi(self):
        assert _F["mh745_tir"](
            [0.0] + [1000.0] * 15) is None

    def test_tir_esiste_caso_semplice_100_120(self):
        assert _F["mh745_tir"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_caso_semplice_1000_500_500_zero(self):
        assert abs(_F["mh745_tir"](
            [-1000.0, 500.0, 500.0])) <= 1e-9

    def test_tir_demo(self):
        flussi = _F["mh745_flussi"](DELTA_DEMO, RISP_DEMO, 15)
        assert _F["mh745_tir"](flussi) == pytest.approx(
            TIR_DEMO / 100.0, rel=1e-9)

    def test_payback_demo_5_da_cumulato(self):
        flussi = _F["mh745_flussi"](DELTA_DEMO, RISP_DEMO, 15)
        assert _F["mh745_payback"](flussi) == 5

    def test_payback_semplice_due(self):
        assert _F["mh745_payback"]([-1000.0, 500.0, 500.0]) == 2

    def test_payback_zero_delta_negativo(self):
        assert _F["mh745_payback"](
            [100000.0, 49860.0]) == 0

    def test_payback_none_mai(self):
        assert _F["mh745_payback"](
            [-220000.0] + [0.0] * 15) is None
        assert _F["mh745_payback"](
            [-220000.0] + [-1000.0] * 15) is None

    def test_verdetto_demo(self):
        assert _F["mh745_verdetto"](
            VAN_DEMO, DELTA_DEMO, 10.0) == VERDETTO_DEMO

    def test_verdetto_conviente_van_positivo(self):
        assert _F["mh745_verdetto"](
            1000.0, DELTA_DEMO, 10.0) == "CONVIENTE"

    def test_verdetto_van_zero_marginale(self):
        assert _F["mh745_verdetto"](
            0.0, DELTA_DEMO, 10.0) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh745_verdetto"](
            -0.10 * DELTA_DEMO, DELTA_DEMO, 10.0) == "MARGINALE"

    def test_verdetto_non_conviente_oltre_limite(self):
        assert _F["mh745_verdetto"](
            -0.10 * DELTA_DEMO - 1.0, DELTA_DEMO,
            10.0) == "NON_CONVIENTE"

    def test_verdetto_delta_negativo_valore_assoluto(self):
        # Delta -100000: tolleranza 10 % = 10000
        # su |delta|; VAN -5000 -> MARGINALE.
        assert _F["mh745_verdetto"](
            -5000.0, -100000.0, 10.0) == "MARGINALE"
        assert _F["mh745_verdetto"](
            -50000.0, -100000.0, 10.0) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_van_nan(self):
        assert _F["mh745_verdetto"](
            float("nan"), DELTA_DEMO, 10.0) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_toll_invalida(self):
        assert _F["mh745_verdetto"](
            1000.0, DELTA_DEMO, 100.01) == "NON_CALCOLABILE"


class TestDemo:
    def _bc(self, **kw):
        d = _F["mh745_demo"]()
        d.update(kw)
        return _F["mh745_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["q_frig_kwh"] == pytest.approx(Q_DEMO, rel=REL)
        assert c["e_base_MWh"] == pytest.approx(EB_DEMO, rel=REL)
        assert c["e_alt_MWh"] == pytest.approx(EA_DEMO, rel=REL)
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
        assert c["risparmio_eur_mwh_f"] == pytest.approx(
            RPMWH_DEMO, rel=REL)
        assert c["capex_delta_eur"] == pytest.approx(
            DELTA_DEMO, rel=REL)
        assert c["crf"] == pytest.approx(CRF_DEMO, rel=REL)
        assert c["quota_capex_eur"] == pytest.approx(
            QUOTA_DEMO, rel=REL)
        assert c["costo_livellato_alt_eur"] == pytest.approx(
            LIV_DEMO, rel=REL)
        assert c["costo_livellato_eur_mwh_f"] == pytest.approx(
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
        d = _F["mh745_demo"]()
        for k, v in _DEMO.items():
            assert d[k] == v, k
        assert len(d) == 16

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("q_frig_kwh",
                       "e_base_MWh",
                       "e_alt_MWh",
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
                       "risparmio_eur_mwh_f",
                       "capex_delta_eur",
                       "crf",
                       "quota_capex_eur",
                       "costo_livellato_alt_eur",
                       "costo_livellato_eur_mwh_f",
                       "van",
                       "tir",
                       "prezzo_pareggio_eur_MWh"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 5" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_prezzo_pareggio_identita(self):
        # Al prezzo di pareggio il risparmio si
        # azzera: 240 x (12,25 + 150 x 85 / 1000)
        # + (12000 - 18000) = 240 x 25 - 6000 = 0.
        n = self._bc(prezzo_el_EUR_MWh=12.25)
        assert n["valid"] is True
        assert n["risparmio_eur_anno"] == pytest.approx(
            0.0, abs=1e-6)
        assert n["payback"] is None

    def test_capex_alt_830000_marginale(self):
        # CAPEX alt 830000 EUR: delta 530000 EUR,
        # VAN -12470,25 EUR, entro la tolleranza
        # del 10 % del delta (53000 EUR) ->
        # MARGINALE.
        n = self._bc(capex_alt_eur=830000.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            530000.0, rel=REL)
        assert abs(n["van"] + 12470.25) <= 1.0
        assert n["verdetto"] == "MARGINALE"

    def test_capex_alt_1000000_non_conviente(self):
        # CAPEX alt 1000000 EUR: delta 700000 EUR,
        # VAN -182470,25 EUR, oltre la tolleranza
        # del 10 % del delta (70000 EUR) ->
        # NON_CONVIENTE.
        n = self._bc(capex_alt_eur=1000000.0)
        assert n["valid"] is True
        assert abs(n["van"] + 182470.25) <= 1.0
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_capex_alt_200000_delta_negativo_calcolabile(self):
        # CAPEX alt 200000 EUR: delta -100000 EUR
        # (alternativa piu' economica della base):
        # NON degenere, flusso anno 0 positivo,
        # VAN +617529,75 EUR, payback 0 ->
        # CONVIENTE.
        n = self._bc(capex_alt_eur=200000.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            -100000.0, rel=REL)
        assert n["flussi"][0] == pytest.approx(
            100000.0, rel=REL)
        assert abs(n["van"] - 617529.75) <= 1.0
        assert n["payback"] == 0
        assert n["verdetto"] == "CONVIENTE"

    def test_cop_alt_15_risparmio_negativo_calcolabile(self):
        # COP alt 1,5: energia alt 590 MWh,
        # totale alt 155322,50 EUR, risparmio
        # -31602,50 EUR/anno (NON degenere),
        # VAN -548023,14 EUR -> NON_CONVIENTE,
        # pareggio None, payback None.
        n = self._bc(cop_alt=1.5)
        assert n["valid"] is True
        assert n["e_alt_MWh"] == pytest.approx(590.0, rel=REL)
        assert n["risparmio_eur_anno"] == pytest.approx(
            -31602.5, rel=REL)
        assert abs(n["van"] + 548023.14) <= 1.0
        assert n["prezzo_pareggio_eur_MWh"] is None
        assert n["payback"] is None
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_share_zero_e_cento_calcolabili(self):
        n0 = self._bc(share_fc_pct=0.0)
        assert n0["valid"] is True
        assert n0["e_alt_MWh"] == pytest.approx(300.0, rel=REL)
        assert n0["verdetto"] == "CONVIENTE"
        n100 = self._bc(share_fc_pct=100.0)
        assert n100["valid"] is True
        assert n100["e_alt_MWh"] == pytest.approx(100.0, rel=REL)
        assert n100["verdetto"] == "CONVIENTE"

    def test_prezzo_eua_zero_conviente(self):
        # Prezzo EUA 0: totali senza CO2,
        # base 117600 EUR (105600 + 12000) e
        # alt 70800 EUR (52800 + 18000),
        # risparmio 46800 EUR/anno, VAN
        # 265768,00 EUR -> CONVIENTE.
        n = self._bc(prezzo_eua_eur_t=0.0)
        assert n["valid"] is True
        assert n["risparmio_eur_anno"] == pytest.approx(
            46800.0, rel=REL)
        assert abs(n["van"] - 265768.0) <= 1.0
        assert n["verdetto"] == "CONVIENTE"

    def test_wacc_zero_valido_crf_uno_su_n(self):
        n = self._bc(wacc_pct=0.0)
        assert n["valid"] is True
        assert n["crf"] == pytest.approx(
            1.0 / 15.0, rel=REL)
        assert n["van"] == pytest.approx(
            527900.0, rel=REL)

    def test_potenza_zero_neutro(self):
        n = self._bc(p_frig_kw=0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_ore_zero_neutro(self):
        n = self._bc(ore_eq_anno=0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_cop_zero_neutro(self):
        for kw in ({"cop_base": 0.0}, {"cop_alt": 0.0},
                   {"cop_fc": 0.0}):
            n = self._bc(**kw)
            assert n["verdetto"] == "NON_CALCOLABILE", kw
            assert n["valid"] is False

    def test_share_fuori_range_neutro(self):
        # 110 % = 1,1 in frazione: fuori [0, 1].
        n = self._bc(share_fc_pct=110.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
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
        n = self._bc(p_frig_kw=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_anno"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(p_frig_kw=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(vita_anni=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_stringa_neutro(self):
        n = self._bc(p_frig_kw="200")
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzo_negativo_neutro(self):
        n = self._bc(prezzo_el_EUR_MWh=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh745_neutro"]()
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
        n = _F["_mh745_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "p_frig_kw",
                       "ore_eq_anno",
                       "cop_base", "cop_alt",
                       "share_fc_pct", "cop_fc",
                       "prezzo_el_EUR_MWh",
                       "om_base_eur_anno",
                       "om_alt_eur_anno",
                       "fattore_rete_kg_MWh",
                       "prezzo_eua_eur_t",
                       "capex_base_eur",
                       "capex_alt_eur",
                       "wacc_pct", "vita_anni",
                       "tolleranza_pct",
                       "q_frig_kwh",
                       "e_base_MWh", "e_alt_MWh",
                       "co2_base_t", "co2_alt_t",
                       "co2_risparmiata_t",
                       "costo_energia_base_eur",
                       "costo_energia_alt_eur",
                       "costo_co2_base_eur",
                       "costo_co2_alt_eur",
                       "totale_base_eur",
                       "totale_alt_eur",
                       "risparmio_eur_anno",
                       "risparmio_eur_mwh_f",
                       "capex_delta_eur",
                       "crf", "quota_capex_eur",
                       "costo_livellato_alt_eur",
                       "costo_livellato_eur_mwh_f",
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
        assert len(b["df_tabella"]) == 40
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Fabbisogno frigorifero (kWh_f/anno)" in voci
        assert "Energia elettrica base (MWh/anno)" in voci
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


class TestCsv:
    def _ing(self):
        return _F["mh745_demo"]()

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh745_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") == 41
        assert len(txt.strip().splitlines()) == 41

    def test_csv_contiene_verdetti_e_costi(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh745_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "capex_delta_eur" in txt
        assert "van_eur" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "prezzo_pareggio_eur_MWh" in txt
        assert "risparmio_eur_anno" in txt
        assert "totale_alt_eur" in txt
        assert "q_frig_kwh" in txt
        assert "co2_risparmiata_t" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh745_csv"](bc, self._ing())
        assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in txt
        assert f"co2_risparmiata_t;{bc['co2_risparmiata_t']}" in txt
        assert "p_frig_kw;200" in txt
        assert "prezzo_el_EUR_MWh;220" in txt
        assert f"costo_livellato_eur_mwh_f;{bc['costo_livellato_eur_mwh_f']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def745["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def745\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 16, ui_keys
        demo_keys = set(_F["mh745_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh745_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh745_demo():")
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
        ui_keys = set(re.findall(r'_def745\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W746 (27/10/2026) - tab745' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh745_num", "mh745_nneg", "mh745_pos",
                     "mh745_int_pos", "mh745_int_nneg",
                     "mh745_pct_0_100", "mh745_pct_wacc",
                     "mh745_q_frig", "mh745_energia_base",
                     "mh745_energia_alt", "mh745_co2",
                     "mh745_costo_energia", "mh745_costo_co2",
                     "mh745_costo_totale", "mh745_risparmio",
                     "mh745_risparmio_per_mwh_f",
                     "mh745_capex_delta", "mh745_crf",
                     "mh745_quota_capex", "mh745_costo_livellato",
                     "mh745_prezzo_pareggio",
                     "mh745_flussi", "mh745_van",
                     "mh745_tir", "mh745_payback",
                     "mh745_verdetto", "mh745_valida",
                     "_mh745_neutro",
                     "mh745_calcola", "mh745_csv",
                     "mh745_demo", "demo_calcoli"):
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
        mh_old = "mh" + "744"
        st_old = "st" + "744"
        tab_old = "tab" + "744"
        w_old = "W" + "745"
        assert mh_old not in _helpers_src()
        assert mh_old not in _ui_src()
        assert st_old not in _ui_src()
        assert tab_old not in _ui_src()
        assert w_old not in _helpers_src()
        assert w_old not in _ui_src()
        assert "mh745" in _helpers_src()
        assert "st745" in _ui_src()

    def test_helpers_parse_ast(self):
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w746_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE745) == 1

    def test_blocco_with_tab745(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab745:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE745

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st745_[A-Za-z0-9_]+)"', _ui_src())
        assert len(keys) == 24, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st745_") for k in keys)

    def test_chiavi_st_input_presenti(self):
        keys = re.findall(r'key="(st745_[A-Za-z0-9_]+)"', _ui_src())
        attese = ["st745_p_frig", "st745_ore",
                  "st745_cop_base", "st745_cop_alt",
                  "st745_share_fc", "st745_cop_fc",
                  "st745_prezzo_el", "st745_fattore_rete",
                  "st745_om_base", "st745_om_alt",
                  "st745_eua", "st745_capex_base",
                  "st745_capex_alt", "st745_wacc",
                  "st745_vita", "st745_tolleranza",
                  "st745_grafico", "st745_show_flussi",
                  "st745_show_tabella", "st745_nota",
                  "st745_ipotesi", "st745_calcola",
                  "st745_csv", "st745_csv_flussi"]
        assert len(attese) == 24
        for k in attese:
            assert k in keys, k

    def test_chiavi_st_niente_fstring_dinamiche(self):
        src = _ui_src()
        assert 'key=f"' not in src
        assert "key=f'" not in src

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg745" in src
        assert "NON_CALCOLABILE" in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg745") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg745")
        assert g < src.index("st.bar_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Risparmio (EUR/anno)" in src
        assert "VAN (kEUR)" in src
        assert "CO2 risparmiata (t/anno)" in src
        assert "Costo livellato alternativo (EUR/MWh_f)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON_CALCOLABILE"):
            assert v in src

    def test_distinzioni_presenti(self):
        src = _ui_src()
        assert "cella frigorifera" in src
        assert "centrale frigorifera" in src

    def test_distinzioni_in_header_helpers(self):
        src = _helpers_src()
        assert "cella frigorifera" in src
        assert "centrale frigorifera" in src

    def test_nota_didattica_presente(self):
        src = _ui_src()
        assert "NOTA DIDATTICA" in src
        assert "1.200.000" in src
        assert "95.055,30" in src

    def test_grafico_bar_chart_presente(self):
        src = _ui_src()
        assert "st.bar_chart" in src
        assert "_dati745" in src
        assert '"EUR/anno"' in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh745_csv" in src
        assert "cella_frigorifera.csv" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st745_show_flussi" in src
        assert "st.checkbox" in src

    def test_niente_nome(self):
        assert "Emanuele" not in _helpers_src()
        assert "Emanuele" not in _ui_src()

    def test_ancora_helper_presente(self):
        assert "# W746 (27/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab745:")
