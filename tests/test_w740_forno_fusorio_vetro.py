"""Test tab740 "🔥🪟 Forno fusorio del vetro: l'elettrificazione paga?"

Nuova tab tab740 (forno fusorio del
vetro, w741). Business case
deterministico dell'elettrificazione
del forno fusorio: il forno a gas
fonde con calore da combustione
(rendimento basso), il forno elettrico
fonde con resistenze ed elettrodi
immersi nel bagno fuso (rendimento
piu' alto). Energia di fusione per
tonnellata, rendimento forno, costo
energia, CO2 gas ed elettrica,
CAPEX retrofit, VAN, TIR, payback,
costo livellato e verdetto.

Demo calcolata eseguendo demo_calcoli()
(e ricontrollata a mano, riga per riga):
produzione 100000 t/anno; consumo gas
4,5 GJ/t; prezzo gas 15 EUR/GJ; fattore
gas 56 kg/GJ; consumo elettrico 950
kWh/t; prezzo elettricita' 60 EUR/MWh;
fattore rete 150 kg/MWh; prezzo EUA 85
EUR/t; CAPEX 12000000 EUR; WACC 7 %;
vita 15 anni; tolleranza 10 % del CAPEX.

- energia_gas_GJ = 450000.0
- energia_elettrica_MWh = 95000.0
- energia_elettrica_GJ = 342000.0
- rendimento_gas_pct = 60.00000000000001
- rendimento_elettrico_pct = 78.94736842105264
- e_gas_t = 25200.0
- e_elettrica_t = 14250.0
- e_risparmiata_t = 10950.0
- costo_gas_eur = 6750000.0
- costo_elettrico_eur = 5700000.0
- costo_co2_gas_eur = 2142000.0
- costo_co2_elettrica_eur = 1211250.0
- costo_totale_gas_eur = 8892000.0
- costo_totale_elettrico_eur = 6911250.0
- risparmio_eur_anno = 1980750.0
- risparmio_eur_per_t = 19.8075
- crf = 0.1097946247010065
- quota_capex_eur = 1317535.496412078
- costo_annuo_livellato_elettrico_eur = 8228785.496412078
- costo_livellato_eur_per_t = 82.28785496412078
- van = 6040500.665619936
- tir = 14.2762220615063
- payback = 7
- verdetto = 'CONVIENTE'

Scomposizione: energia gas 100000 x 4,5 =
450000.0 GJ/anno; energia elettrica
100000 x 950 / 1000 = 95000.0 MWh/anno
= 342000.0 GJ/anno (95000.0 x 3,6);
rendimento gas 2,7 / 4,5 x 100 =
60.00000000000001 %; rendimento
elettrico 2,7 / 3,42 x 100 =
78.94736842105264 % (950 kWh/t = 3,42
GJ/t); CO2 gas 450000.0 x 56 / 1000 =
25200.0 tCO2/anno; CO2 elettrica
95000.0 x 150 / 1000 = 14250.0
tCO2/anno; risparmiata 25200.0 -
14250.0 = 10950.0 tCO2/anno; costo gas
450000.0 x 15 = 6750000.0 EUR/anno;
costo elettrico 95000.0 x 60 =
5700000.0 EUR/anno; costo CO2 gas
25200.0 x 85 = 2142000.0 EUR/anno;
costo CO2 elettrica 14250.0 x 85 =
1211250.0 EUR/anno; totali 6750000.0 +
2142000.0 = 8892000.0 EUR/anno contro
5700000.0 + 1211250.0 = 6911250.0
EUR/anno; risparmio 8892000.0 -
6911250.0 = 1980750.0 EUR/anno =
19.8075 EUR/t; CRF 0,07 x 1,07^15 /
(1,07^15 - 1) = 0.1097946247010065;
quota CAPEX 12000000.0 x
0.1097946247010065 = 1317535.496412078
EUR/anno; costo livellato 6911250.0 +
1317535.496412078 = 8228785.496412078
EUR/anno = 82.28785496412078 EUR/t
contro 88,92 EUR/t del gas; flussi:
anno 0 -12000000.0, anni 1-15 risparmio
1980750.0 (piatti); VAN -12000000.0 +
1980750.0 x 9,107914005109144
(annuita' 15 anni al 7 %) =
6040500.665619936 EUR; TIR
14.2762220615063 %; payback 7 (il
cumulato -12000000.0 + 1980750.0 x 7 =
1865250.0 diventa positivo al settimo
anno); verdetto CONVIENTE perche' VAN
> 0. NOTA: il CRF entra solo nel costo
annuo livellato, mai nei flussi: il
CAPEX compare una sola volta,
all'anno 0.
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
    if (p / "w741_helpers.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w741_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w741_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w741_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w741_helpers.py: {missing}")
    return out


_F = _load("mh740_num", "mh740_nneg", "mh740_pos",
           "mh740_int_pos", "mh740_pct_0_100",
           "mh740_pct_wacc",
           "mh740_energia_gas", "mh740_energia_elettrica",
           "mh740_energia_elettrica_GJ", "mh740_rendimento",
           "mh740_e_gas", "mh740_e_elettrica",
           "mh740_e_risparmiata", "mh740_costo_gas",
           "mh740_costo_elettrico", "mh740_costo_co2",
           "mh740_costo_totale", "mh740_risparmio",
           "mh740_risparmio_per_t", "mh740_crf",
           "mh740_quota_capex", "mh740_costo_livellato",
           "mh740_flussi", "mh740_van", "mh740_tir",
           "mh740_payback", "mh740_verdetto",
           "mh740_valida", "_mh740_neutro",
           "mh740_calcola", "mh740_csv",
           "mh740_demo", "demo_calcoli")

TITLE740 = ("🔥🪟 Forno fusorio del vetro: l'elettrificazione paga?")

EG_DEMO = 450000.0
MWH_DEMO = 95000.0
EGJ_DEMO = 342000.0
RG_DEMO = 60.00000000000001
RE_DEMO = 78.94736842105264
E_GAS_DEMO = 25200.0
E_EL_DEMO = 14250.0
E_RISP_DEMO = 10950.0
C_GAS_DEMO = 6750000.0
C_EL_DEMO = 5700000.0
CC_GAS_DEMO = 2142000.0
CC_EL_DEMO = 1211250.0
CT_GAS_DEMO = 8892000.0
CT_EL_DEMO = 6911250.0
RISP_DEMO = 1980750.0
RPT_DEMO = 19.8075
CRF_DEMO = 0.1097946247010065
QUOTA_DEMO = 1317535.496412078
LIV_DEMO = 8228785.496412078
LIVT_DEMO = 82.28785496412078
VAN_DEMO = 6040500.665619936
TIR_DEMO = 14.2762220615063
PAYBACK_DEMO = 7
VERDETTO_DEMO = "CONVIENTE"

_DEMO = {
    "produzione_t_anno": 100000.0,
    "consumo_gas_GJ_per_t": 4.5,
    "prezzo_gas_eur_per_GJ": 15.0,
    "fattore_gas_kg_per_GJ": 56.0,
    "consumo_elettrico_kWh_per_t": 950.0,
    "prezzo_elettricita_eur_per_MWh": 60.0,
    "fattore_rete_kg_per_MWh": 150.0,
    "prezzo_eua_eur_t": 85.0,
    "capex_eur": 12000000.0,
    "wacc_pct": 7.0,
    "vita_anni": 15,
    "tolleranza_pct": 10.0,
}

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w741_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w741_ui.py").read_text(encoding="utf-8")


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh740_demo"]()
        d.update(kw)
        return _F["mh740_valida"](**d)

    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh740_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh740_num"]("500", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh740_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh740_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh740_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh740_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh740_pos"](0.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh740_int_pos"](2.5, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh740_int_pos"](15.0, "x") == 15

    def test_pct_0_100_accetta_estremi_rifiuta_fuori(self):
        assert _F["mh740_pct_0_100"](0.0, "x") == 0.0
        assert _F["mh740_pct_0_100"](100.0, "x") == 100.0
        with pytest.raises(ValueError):
            _F["mh740_pct_0_100"](-0.01, "x")
        with pytest.raises(ValueError):
            _F["mh740_pct_0_100"](100.01, "x")

    def test_pct_wacc_accetta_zero_e_50_rifiuta_oltre(self):
        assert _F["mh740_pct_wacc"](0.0, "x") == 0.0
        assert _F["mh740_pct_wacc"](50.0, "x") == 50.0
        with pytest.raises(ValueError):
            _F["mh740_pct_wacc"](-0.01, "x")
        with pytest.raises(ValueError):
            _F["mh740_pct_wacc"](50.01, "x")

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_produzione_zero_e_negativa_non_valide(self):
        assert self._val(produzione_t_anno=0.0)["valido"] is False
        assert self._val(produzione_t_anno=-1.0)["valido"] is False

    def test_negativi_non_validi(self):
        for k in ("consumo_gas_GJ_per_t",
                  "prezzo_gas_eur_per_GJ",
                  "fattore_gas_kg_per_GJ",
                  "consumo_elettrico_kWh_per_t",
                  "prezzo_elettricita_eur_per_MWh",
                  "fattore_rete_kg_per_MWh",
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
        assert self._val(produzione_t_anno=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(produzione_t_anno=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(vita_anni=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(produzione_t_anno="500")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(consumo_gas_GJ_per_t=0.0)["valido"] is True
        assert self._val(capex_eur=0.0)["valido"] is True
        assert self._val(prezzo_eua_eur_t=0.0)["valido"] is True
        assert self._val(tolleranza_pct=0.0)["valido"] is True


class TestFunzioni:
    def test_energia_gas_demo(self):
        assert _F["mh740_energia_gas"](
            100000.0, 4.5) == pytest.approx(EG_DEMO, rel=REL)

    def test_energia_gas_formula_letterale(self):
        assert _F["mh740_energia_gas"](
            50000.0, 4.0) == pytest.approx(200000.0, rel=REL)

    def test_energia_gas_rifiuta_produzione_zero(self):
        with pytest.raises(ValueError):
            _F["mh740_energia_gas"](0.0, 4.5)

    def test_energia_elettrica_demo(self):
        assert _F["mh740_energia_elettrica"](
            100000.0, 950.0) == pytest.approx(MWH_DEMO, rel=REL)

    def test_energia_elettrica_formula_letterale(self):
        assert _F["mh740_energia_elettrica"](
            200000.0, 1000.0) == pytest.approx(200000.0, rel=REL)

    def test_energia_elettrica_GJ_demo(self):
        assert _F["mh740_energia_elettrica_GJ"](
            MWH_DEMO) == pytest.approx(EGJ_DEMO, rel=REL)

    def test_energia_elettrica_GJ_fattore_3_6(self):
        assert _F["mh740_energia_elettrica_GJ"](
            1000.0) == pytest.approx(3600.0, rel=REL)

    def test_rendimento_gas_demo(self):
        assert _F["mh740_rendimento"](
            2.7, 4.5) == pytest.approx(RG_DEMO, rel=REL)

    def test_rendimento_elettrico_demo(self):
        assert _F["mh740_rendimento"](
            2.7, 3.42) == pytest.approx(RE_DEMO, rel=REL)

    def test_rendimento_rifiuta_consumo_zero(self):
        with pytest.raises(ValueError):
            _F["mh740_rendimento"](2.7, 0.0)

    def test_e_gas_demo(self):
        assert _F["mh740_e_gas"](
            EG_DEMO, 56.0) == pytest.approx(E_GAS_DEMO, rel=REL)

    def test_e_elettrica_demo(self):
        assert _F["mh740_e_elettrica"](
            MWH_DEMO, 150.0) == pytest.approx(E_EL_DEMO, rel=REL)

    def test_e_risparmiata_demo(self):
        assert _F["mh740_e_risparmiata"](
            E_GAS_DEMO, E_EL_DEMO) == pytest.approx(
            E_RISP_DEMO, rel=REL)

    def test_e_risparmiata_negativa_rete_sporca(self):
        assert _F["mh740_e_risparmiata"](
            1000.0, 2000.0) == pytest.approx(-1000.0, rel=REL)

    def test_costo_gas_demo(self):
        assert _F["mh740_costo_gas"](
            EG_DEMO, 15.0) == pytest.approx(C_GAS_DEMO, rel=REL)

    def test_costo_elettrico_demo(self):
        assert _F["mh740_costo_elettrico"](
            MWH_DEMO, 60.0) == pytest.approx(C_EL_DEMO, rel=REL)

    def test_costo_co2_demo(self):
        assert _F["mh740_costo_co2"](
            E_GAS_DEMO, 85.0) == pytest.approx(CC_GAS_DEMO, rel=REL)

    def test_costo_totale_demo(self):
        assert _F["mh740_costo_totale"](
            C_GAS_DEMO, CC_GAS_DEMO) == pytest.approx(
            CT_GAS_DEMO, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh740_risparmio"](
            CT_GAS_DEMO, CT_EL_DEMO) == pytest.approx(
            RISP_DEMO, rel=REL)

    def test_risparmio_negativo_elettrico_piu_caro(self):
        assert _F["mh740_risparmio"](
            1000.0, 2000.0) == pytest.approx(-1000.0, rel=REL)

    def test_risparmio_per_t_demo(self):
        assert _F["mh740_risparmio_per_t"](
            RISP_DEMO, 100000.0) == pytest.approx(
            RPT_DEMO, rel=REL)

    def test_crf_demo(self):
        assert _F["mh740_crf"](
            7.0, 15) == pytest.approx(CRF_DEMO, rel=REL)

    def test_crf_wacc_zero_uno_su_n(self):
        assert _F["mh740_crf"](0.0, 15) == pytest.approx(
            1.0 / 15.0, rel=REL)

    def test_crf_formula_indipendente(self):
        r = 0.10
        n = 10
        atteso = r * (1.0 + r) ** n / ((1.0 + r) ** n - 1.0)
        assert _F["mh740_crf"](10.0, 10) == pytest.approx(
            atteso, rel=REL)

    def test_crf_rifiuta_wacc_oltre_50(self):
        with pytest.raises(ValueError):
            _F["mh740_crf"](50.01, 15)

    def test_quota_capex_demo(self):
        assert _F["mh740_quota_capex"](
            12000000.0, CRF_DEMO) == pytest.approx(
            QUOTA_DEMO, rel=REL)

    def test_costo_livellato_demo(self):
        assert _F["mh740_costo_livellato"](
            CT_EL_DEMO, QUOTA_DEMO) == pytest.approx(
            LIV_DEMO, rel=REL)

    def test_flussi_demo(self):
        flussi = _F["mh740_flussi"](12000000.0, RISP_DEMO, 15)
        assert len(flussi) == 16
        assert flussi[0] == pytest.approx(-12000000.0, rel=REL)
        assert all(f == pytest.approx(RISP_DEMO, rel=REL)
                   for f in flussi[1:])

    def test_van_demo(self):
        flussi = _F["mh740_flussi"](12000000.0, RISP_DEMO, 15)
        assert abs(_F["mh740_van"](
            flussi, 7.0) - VAN_DEMO) <= 1.0

    def test_van_tasso_zero(self):
        flussi = _F["mh740_flussi"](12000000.0, RISP_DEMO, 15)
        atteso = -12000000.0 + RISP_DEMO * 15
        assert _F["mh740_van"](
            flussi, 0.0) == pytest.approx(atteso, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh740_van"]([100.0, 100.0], -0.01)

    def test_tir_none_flussi_tutti_negativi(self):
        flussi = _F["mh740_flussi"](12000000.0, -1000.0, 15)
        assert _F["mh740_tir"](flussi) is None

    def test_tir_none_tutti_flussi_non_negativi(self):
        assert _F["mh740_tir"](
            [0.0] + [1000.0] * 15) is None

    def test_tir_esiste_caso_semplice_100_120(self):
        assert _F["mh740_tir"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_caso_semplice_1000_500_500_zero(self):
        assert abs(_F["mh740_tir"](
            [-1000.0, 500.0, 500.0])) <= 1e-9

    def test_tir_demo(self):
        flussi = _F["mh740_flussi"](12000000.0, RISP_DEMO, 15)
        assert _F["mh740_tir"](flussi) == pytest.approx(
            TIR_DEMO / 100.0, rel=1e-9)

    def test_payback_demo_7(self):
        flussi = _F["mh740_flussi"](12000000.0, RISP_DEMO, 15)
        assert _F["mh740_payback"](flussi) == 7

    def test_payback_semplice_due(self):
        assert _F["mh740_payback"](
            [-1000.0, 500.0, 500.0, 500.0]) == 2

    def test_payback_zero_se_cumulato_anno_zero_non_negativo(self):
        assert _F["mh740_payback"](
            [0.0, 100.0]) == 0

    def test_payback_none_se_mai(self):
        assert _F["mh740_payback"](
            [-10000000000.0] + [1000.0] * 15) is None

    def test_verdetto_demo(self):
        assert _F["mh740_verdetto"](
            VAN_DEMO, 12000000.0, 10.0,
            RISP_DEMO) == VERDETTO_DEMO

    def test_verdetto_conviente_van_positivo(self):
        assert _F["mh740_verdetto"](
            1000.0, 12000000.0, 10.0,
            RISP_DEMO) == "CONVIENTE"

    def test_verdetto_van_zero_marginale(self):
        assert _F["mh740_verdetto"](
            0.0, 12000000.0, 10.0,
            RISP_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh740_verdetto"](
            -0.10 * 12000000.0, 12000000.0, 10.0,
            RISP_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_oltre_limite(self):
        assert _F["mh740_verdetto"](
            -0.10 * 12000000.0 - 1.0, 12000000.0, 10.0,
            RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_zero(self):
        assert _F["mh740_verdetto"](
            1000.0, 12000000.0, 10.0,
            0.0) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_risparmio_negativo(self):
        assert _F["mh740_verdetto"](
            1000.0, 12000000.0, 10.0,
            -5000.0) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_risparmio_nan(self):
        assert _F["mh740_verdetto"](
            1000.0, 12000000.0, 10.0,
            float("nan")) == "NON_CALCOLABILE"


class TestDemo:
    def _bc(self, **kw):
        d = _F["mh740_demo"]()
        d.update(kw)
        return _F["mh740_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["energia_gas_GJ"] == pytest.approx(
            EG_DEMO, rel=REL)
        assert c["energia_elettrica_MWh"] == pytest.approx(
            MWH_DEMO, rel=REL)
        assert c["energia_elettrica_GJ"] == pytest.approx(
            EGJ_DEMO, rel=REL)
        assert c["rendimento_gas_pct"] == pytest.approx(
            RG_DEMO, rel=REL)
        assert c["rendimento_elettrico_pct"] == pytest.approx(
            RE_DEMO, rel=REL)
        assert c["e_gas_t"] == pytest.approx(
            E_GAS_DEMO, rel=REL)
        assert c["e_elettrica_t"] == pytest.approx(
            E_EL_DEMO, rel=REL)
        assert c["e_risparmiata_t"] == pytest.approx(
            E_RISP_DEMO, rel=REL)
        assert c["costo_gas_eur"] == pytest.approx(
            C_GAS_DEMO, rel=REL)
        assert c["costo_elettrico_eur"] == pytest.approx(
            C_EL_DEMO, rel=REL)
        assert c["costo_co2_gas_eur"] == pytest.approx(
            CC_GAS_DEMO, rel=REL)
        assert c["costo_co2_elettrica_eur"] == pytest.approx(
            CC_EL_DEMO, rel=REL)
        assert c["costo_totale_gas_eur"] == pytest.approx(
            CT_GAS_DEMO, rel=REL)
        assert c["costo_totale_elettrico_eur"] == pytest.approx(
            CT_EL_DEMO, rel=REL)
        assert c["risparmio_eur_anno"] == pytest.approx(
            RISP_DEMO, rel=REL)
        assert c["risparmio_eur_per_t"] == pytest.approx(
            RPT_DEMO, rel=REL)
        assert c["crf"] == pytest.approx(CRF_DEMO, rel=REL)
        assert c["quota_capex_eur"] == pytest.approx(
            QUOTA_DEMO, rel=REL)
        assert c["costo_annuo_livellato_elettrico_eur"] == pytest.approx(
            LIV_DEMO, rel=REL)
        assert c["costo_livellato_eur_per_t"] == pytest.approx(
            LIVT_DEMO, rel=REL)
        assert abs(c["van"] - VAN_DEMO) <= 1.0
        assert c["tir"] == pytest.approx(TIR_DEMO, rel=REL)
        assert c["payback"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO
        assert len(c["flussi"]) == 16

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()["van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()["risparmio_eur_anno"] == \
            _F["demo_calcoli"]()["risparmio_eur_anno"]

    def test_demo_defaults_contro_costanti_test(self):
        d = _F["mh740_demo"]()
        for k, v in _DEMO.items():
            assert d[k] == v, k
        assert len(d) == 12

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("energia_gas_GJ",
                       "energia_elettrica_MWh",
                       "energia_elettrica_GJ",
                       "rendimento_gas_pct",
                       "rendimento_elettrico_pct",
                       "e_gas_t",
                       "e_elettrica_t",
                       "e_risparmiata_t",
                       "costo_gas_eur",
                       "costo_elettrico_eur",
                       "costo_co2_gas_eur",
                       "costo_co2_elettrica_eur",
                       "costo_totale_gas_eur",
                       "costo_totale_elettrico_eur",
                       "risparmio_eur_anno",
                       "risparmio_eur_per_t",
                       "crf",
                       "quota_capex_eur",
                       "costo_annuo_livellato_elettrico_eur",
                       "costo_livellato_eur_per_t",
                       "van",
                       "tir"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 7" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_prezzo_pareggio_80_85_neutro(self):
        # Prezzo elettrico 80,85 EUR/MWh: totale
        # elettrico = totale gas, risparmio 0 ->
        # guard degenere -> NON_CALCOLABILE.
        n = self._bc(prezzo_elettricita_eur_per_MWh=80.85)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["risparmio_eur_anno"] == 0.0

    def test_prezzo_elettrico_120_neutro(self):
        # Prezzo elettrico 120 EUR/MWh: risparmio
        # -3.719.250 EUR/anno -> NON_CALCOLABILE.
        n = self._bc(prezzo_elettricita_eur_per_MWh=120.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["risparmio_eur_anno"] == 0.0

    def test_prezzo_gas_10_neutro(self):
        # Prezzo gas 10 EUR/GJ: risparmio
        # -269.250 EUR/anno -> NON_CALCOLABILE.
        n = self._bc(prezzo_gas_eur_per_GJ=10.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_prezzo_eua_150_conviente(self):
        # Prezzo EUA 150 EUR/t: risparmio
        # 2.692.500 EUR/anno -> CONVIENTE.
        n = self._bc(prezzo_eua_eur_t=150.0)
        assert n["valid"] is True
        assert n["risparmio_eur_anno"] == pytest.approx(
            2692500.0, rel=REL)
        assert n["verdetto"] == "CONVIENTE"
        assert n["van"] > 0.0

    def test_prezzo_eua_zero_non_conviente(self):
        # Prezzo EUA 0: risparmio 1.050.000
        # EUR/anno (solo energia), VAN
        # -2.436.690,29 EUR, oltre la
        # tolleranza del 10 % del CAPEX
        # (1.200.000 EUR) -> NON_CONVIENTE:
        # senza EUA la sola leva energia non
        # basta a ripagare il CAPEX.
        n = self._bc(prezzo_eua_eur_t=0.0)
        assert n["valid"] is True
        assert n["risparmio_eur_anno"] == pytest.approx(
            1050000.0, rel=REL)
        assert n["van"] == pytest.approx(
            -2436690.2946353983, rel=REL)
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_capex_20m_marginale(self):
        # CAPEX 20.000.000 EUR: VAN -1.959.499,33
        # EUR, entro la tolleranza del 10 %
        # (2.000.000 EUR) -> MARGINALE.
        n = self._bc(capex_eur=20000000.0)
        assert n["valid"] is True
        assert n["van"] == pytest.approx(
            -1959499.334380065, rel=REL)
        assert n["verdetto"] == "MARGINALE"

    def test_capex_30m_non_conviente(self):
        # CAPEX 30.000.000 EUR: VAN
        # -11.959.499,33 EUR, oltre tolleranza
        # -> NON_CONVIENTE.
        n = self._bc(capex_eur=30000000.0)
        assert n["valid"] is True
        assert n["van"] == pytest.approx(
            -11959499.334380064, rel=REL)
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_capex_zero_payback_zero(self):
        # CAPEX zero: flussi [0, risparmio x 15],
        # VAN positiva, payback 0 (cumulato
        # anno 0 = 0), TIR None (nessun cambio
        # di segno).
        n = self._bc(capex_eur=0.0)
        assert n["valid"] is True
        assert n["van"] == pytest.approx(
            RISP_DEMO * 9.107914005109144, rel=REL)
        assert n["payback"] == 0
        assert n["tir"] is None
        assert n["verdetto"] == "CONVIENTE"

    def test_wacc_zero_valido_crf_uno_su_n(self):
        n = self._bc(wacc_pct=0.0)
        assert n["valid"] is True
        assert n["crf"] == pytest.approx(
            1.0 / 15.0, rel=REL)
        assert n["van"] == pytest.approx(
            17711250.0, rel=REL)

    def test_produzione_zero_neutro(self):
        n = self._bc(produzione_t_anno=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

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
        n = self._bc(produzione_t_anno=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_anno"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(produzione_t_anno=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(vita_anni=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_stringa_neutro(self):
        n = self._bc(produzione_t_anno="500")
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_costo_negativo_neutro(self):
        n = self._bc(prezzo_elettricita_eur_per_MWh=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh740_neutro"]()
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
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh740_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "produzione_t_anno",
                       "consumo_gas_GJ_per_t",
                       "prezzo_gas_eur_per_GJ",
                       "fattore_gas_kg_per_GJ",
                       "consumo_elettrico_kWh_per_t",
                       "prezzo_elettricita_eur_per_MWh",
                       "fattore_rete_kg_per_MWh",
                       "prezzo_eua_eur_t",
                       "capex_eur", "wacc_pct",
                       "vita_anni", "tolleranza_pct",
                       "energia_gas_GJ",
                       "energia_elettrica_MWh",
                       "energia_elettrica_GJ",
                       "rendimento_gas_pct",
                       "rendimento_elettrico_pct",
                       "e_gas_t", "e_elettrica_t",
                       "e_risparmiata_t",
                       "costo_gas_eur",
                       "costo_elettrico_eur",
                       "costo_co2_gas_eur",
                       "costo_co2_elettrica_eur",
                       "costo_totale_gas_eur",
                       "costo_totale_elettrico_eur",
                       "risparmio_eur_anno",
                       "risparmio_eur_per_t",
                       "crf", "quota_capex_eur",
                       "costo_annuo_livellato_elettrico_eur",
                       "costo_livellato_eur_per_t",
                       "flussi", "van", "tir",
                       "payback", "verdetto",
                       "df_flussi", "df_tabella"):
            assert chiave in n, chiave
        assert n["errore"] == "errore di prova"
        assert n["tir"] is None

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert b["valid"] is True
        assert list(b["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(b["df_tabella"]) == 36
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Energia gas (GJ/anno)" in voci
        assert "Energia elettrica (MWh/anno)" in voci
        assert "Rendimento gas (%)" in voci
        assert "Rendimento elettrico (%)" in voci
        assert "CO2 gas (tCO2/anno)" in voci
        assert "CO2 elettrica (tCO2/anno)" in voci
        assert "CO2 risparmiata (tCO2/anno)" in voci
        assert "Costo totale gas (EUR/anno)" in voci
        assert "Costo totale elettrico (EUR/anno)" in voci
        assert "Risparmio (EUR/anno)" in voci
        assert "CRF" in voci
        assert "VAN (EUR)" in voci
        assert "Verdetto" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (EUR/anno)",
                                               "Cumulato (EUR)"]
        assert len(b["df_flussi"]) == 16
        assert b["df_flussi"]["Flusso (EUR/anno)"].iloc[0] == \
            pytest.approx(-12000000.0, rel=REL)
        assert b["df_flussi"]["Flusso (EUR/anno)"].iloc[1] == \
            pytest.approx(RISP_DEMO, rel=REL)


class TestCsv:
    def _ing(self):
        return _F["mh740_demo"]()

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh740_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") == 37

    def test_csv_contiene_verdetti_e_costi(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh740_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "capex_eur" in txt
        assert "van_eur" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "risparmio_eur_anno" in txt
        assert "costo_totale_gas_eur" in txt
        assert "energia_gas_GJ" in txt
        assert "e_risparmiata_t" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh740_csv"](bc, self._ing())
        assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in txt
        assert f"e_risparmiata_t;{bc['e_risparmiata_t']}" in txt
        assert "produzione_t_anno;100000.0" in txt
        assert "prezzo_elettricita_eur_per_MWh;60.0" in txt
        assert f"costo_livellato_eur_per_t;{bc['costo_livellato_eur_per_t']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def740["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def740\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 12, ui_keys
        demo_keys = set(_F["mh740_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh740_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh740_demo():")
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
        ui_keys = set(re.findall(r'_def740\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W741 (27/10/2026) - tab740' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh740_num", "mh740_nneg", "mh740_pos",
                     "mh740_int_pos", "mh740_pct_0_100",
                     "mh740_pct_wacc",
                     "mh740_energia_gas",
                     "mh740_energia_elettrica",
                     "mh740_energia_elettrica_GJ",
                     "mh740_rendimento",
                     "mh740_e_gas", "mh740_e_elettrica",
                     "mh740_e_risparmiata",
                     "mh740_costo_gas",
                     "mh740_costo_elettrico",
                     "mh740_costo_co2",
                     "mh740_costo_totale",
                     "mh740_risparmio",
                     "mh740_risparmio_per_t",
                     "mh740_crf", "mh740_quota_capex",
                     "mh740_costo_livellato",
                     "mh740_flussi", "mh740_van",
                     "mh740_tir", "mh740_payback",
                     "mh740_verdetto", "mh740_valida",
                     "_mh740_neutro",
                     "mh740_calcola", "mh740_csv",
                     "mh740_demo", "demo_calcoli"):
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
        mh_old = "mh" + "739"
        st_old = "st" + "739"
        tab_old = "tab" + "739"
        w_old = "W" + "740"
        assert mh_old not in _helpers_src()
        assert mh_old not in _ui_src()
        assert st_old not in _ui_src()
        assert tab_old not in _ui_src()
        assert w_old not in _helpers_src()
        assert w_old not in _ui_src()
        assert "mh740" in _helpers_src()
        assert "st740" in _ui_src()

    def test_helpers_parse_ast(self):
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w741_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE740) == 1

    def test_blocco_with_tab740(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab740:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE740

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st740_[A-Za-z0-9_]+)"', _ui_src())
        assert len(keys) == 20, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st740_") for k in keys)

    def test_chiavi_st_input_presenti(self):
        keys = re.findall(r'key="(st740_[A-Za-z0-9_]+)"', _ui_src())
        attese = ["st740_produzione", "st740_consumo_gas",
                  "st740_prezzo_gas", "st740_fattore_gas",
                  "st740_consumo_el", "st740_prezzo_el",
                  "st740_fattore_rete", "st740_eua",
                  "st740_capex", "st740_wacc", "st740_vita",
                  "st740_tolleranza", "st740_grafico",
                  "st740_show_flussi", "st740_show_tabella",
                  "st740_nota", "st740_ipotesi",
                  "st740_calcola", "st740_csv",
                  "st740_csv_flussi"]
        assert len(attese) == 20
        for k in attese:
            assert k in keys, k

    def test_chiavi_st_niente_fstring_dinamiche(self):
        src = _ui_src()
        assert 'key=f"' not in src
        assert "key=f'" not in src

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg740" in src
        assert "NON_CALCOLABILE" in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg740") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg740")
        assert g < src.index("st.bar_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "CO2 risparmiata (t/anno)" in src
        assert "Risparmio (EUR/anno)" in src
        assert "Costo livellato elettrico (EUR/t)" in src
        assert "VAN (kEUR)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON_CALCOLABILE"):
            assert v in src

    def test_distinzioni_presenti(self):
        src = _ui_src()
        assert "induzione" in src
        assert "essiccazione" in src
        assert "vetro" in src
        assert "CCS" in src

    def test_distinzioni_in_header_helpers(self):
        src = _helpers_src()
        assert "induzione" in src
        assert "essiccazione" in src
        assert "vetro" in src
        assert "CCS" in src

    def test_nota_didattica_presente(self):
        src = _ui_src()
        assert "NOTA DIDATTICA" in src
        assert "450.000" in src
        assert "95.000" in src

    def test_grafico_bar_chart_presente(self):
        src = _ui_src()
        assert "st.bar_chart" in src
        assert "_dati740" in src
        assert '"EUR/anno"' in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh740_csv" in src
        assert "forno_vetro.csv" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st740_show_flussi" in src
        assert "st.checkbox" in src

    def test_niente_nome(self):
        assert "Emanuele" not in _helpers_src()
        assert "Emanuele" not in _ui_src()

    def test_ancora_helper_presente(self):
        assert "# W741 (27/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab740:")
