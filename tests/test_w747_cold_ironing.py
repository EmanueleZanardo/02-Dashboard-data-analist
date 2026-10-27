"""Test tab747 "Cold ironing portuale: la corrente da banchina batte i generatori diesel di bordo?"

Nuova tab tab747 (cold
ironing, w748). Business case
deterministico di una nave in
banchina: confronta BORDO =
gruppi ausiliari a gasolio marino
MGO contro BANCHINA = corrente da
banchina. Energia hotel da potenza
hotel, ore per scalo e scali annui,
energia da banchina da energia hotel
e rendimento connessione,
combustibile risparmiato da energia
hotel e rendimento generatore di
bordo, CO2 da energia e fattori di
emissione, costi da energia, O&M e
EUA, CAPEX da costo del sistema di
connessione, VAN, TIR, payback
(primo anno con cumulato >= 0) e
prezzo elettrico di pareggio.
Nessuna altra tab e' dedicata al
cold ironing portuale con confronto
tra generatori diesel di bordo a MGO
e corrente da banchina: 0 occorrenze
di "cold ironing" in app.py prima
di questa tab.

Demo calcolata eseguendo demo_calcoli()
(e ricontrollata a mano, riga per riga):
nave portacontainer con potenza hotel
800 kW, 24 ore per scalo e 100 scali
all'anno, rendimento connessione 0,95
e rendimento generatore di bordo 0,42,
prezzo MGO 120 EUR/MWh e prezzo
elettricita' 220 EUR/MWh, O&M bordo 0
EUR/anno e banchina 30000 EUR/anno,
fattore MGO 270 kg/MWh e fattore rete
150 kg/MWh, prezzo EUA 85 EUR/t,
CAPEX 1200000 EUR, WACC 5 %, vita 20
anni, tolleranza 10 % del CAPEX.

- e_hotel_mwh = 1920.0
- e_banchina_mwh = 2021.0526315789475
- e_combustibile_mwh = 4571.428571428572
- co2_bordo_t = 1234.2857142857142
- co2_banchina_t = 303.15789473684214
- co2_evitata_t = 931.1278195488721
- costo_combustibile_eur = 548571.4285714286
- costo_co2_bordo_eur = 104914.28571428571
- costo_energia_banchina_eur = 444631.5789473684
- costo_co2_banchina_eur = 25768.42105263158
- totale_bordo_eur = 653485.7142857143
- totale_banchina_eur = 500400.0
- risparmio_eur_anno = 153085.71428571432
- risparmio_eur_mwh = 79.73214285714288
- capex_eur_out = 1200000.0
- crf = 0.08024258719069129
- quota_capex_eur = 96291.10462882955
- costo_livellato_banchina_eur = 596691.1046288295
- costo_livellato_banchina_eur_mwh = 310.77661699418206
- costo_bordo_eur_mwh = 340.3571428571429
- van = 707786.3718665496
- tir = 11.242364022078561
- payback = 8
- prezzo_pareggio_eur_mwh = 295.7455357142857
- verdetto = 'CONVIENTE'

Scomposizione: E_hotel = 800 x 24 x
100 / 1000 = 1920,00 MWh; E_banchina
= 1920 / 0,95 = 2021,05 MWh;
E_combustibile = 1920 / 0,42 =
4571,43 MWh; CO2 bordo 4571,43 x
270 / 1000 = 1234,29 t; CO2 banchina
2021,05 x 150 / 1000 = 303,16 t;
evitata 931,13 t; costo combustibile
4571,43 x 120 = 548571,43 EUR; costo
CO2 bordo 1234,29 x 85 = 104914,29
EUR; totale bordo 548571,43 +
104914,29 + 0 = 653485,71 EUR; costo
energia banchina 2021,05 x 220 =
444631,58 EUR; costo CO2 banchina
303,16 x 85 = 25768,42 EUR; totale
banchina 444631,58 + 25768,42 +
30000 = 500400,00 EUR; risparmio
653485,71 - 500400,00 = 153085,71
EUR/anno = 79,73 EUR/MWh; CAPEX
1200000 EUR; CRF 0,05 x 1,05^20 /
(1,05^20 - 1) = 0.08024258719069129;
quota CAPEX 1200000 x 0,080243 =
96291,10 EUR/anno; costo livellato
500400,00 + 96291,10 = 596691,10
EUR/anno = 310,78 EUR/MWh contro
340,36 EUR/MWh del bordo; flussi:
anno 0 -1200000, anni 1-20 risparmio
153085,71 (piatti); VAN -1200000 +
153085,71 x 12,462210343296 (annuita'
20 anni al 5 %) = 707786,37 EUR; TIR
11,24 % (bisezione esatta); payback 8
(cumulato anno 7: -1200000 + 7 x
153085,71 = -128400,00 EUR, mai >= 0;
anno 8: +24685,71 EUR); prezzo
elettrico di pareggio (548571,43 +
104914,29 + 0 - 30000 - 25768,42) /
2021,05 = 295.7455357142857 EUR/MWh;
verdetto CONVIENTE perche' VAN > 0.
NOTA: il CRF entra solo nel costo
livellato, mai nei flussi: il CAPEX
compare una sola volta, all'anno 0.
NOTA 2: in questo brief il risparmio
nullo o negativo E' degenere (a
differenza di altri business case):
la banchina piu' cara del bordo non
ha senso economico da mostrare come
caso calcolabile, e al prezzo di
pareggio esatto il caso e' degenere
(risparmio 0). NOTA 3: la CO2 evitata
negativa NON e' degenere di per se':
se il risparmio resta > 0 il caso
resta calcolabile e la CO2 evitata
negativa va detta (rete 800 kg/MWh:
evitata -382,56 t, risparmio
41422,56 EUR/anno, VAN -683783,39
EUR, NON_CONVIENTE).
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
    if (p / "w748_helpers.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w748_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w748_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w748_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w748_helpers.py: {missing}")
    return out


_F = _load("mh747_num", "mh747_nneg", "mh747_pos",
           "mh747_int_pos", "mh747_int_nneg",
           "mh747_pct_0_100", "mh747_pct_wacc",
           "mh747_eta", "mh747_e_hotel",
           "mh747_e_banchina", "mh747_e_combustibile",
           "mh747_co2", "mh747_costo_energia",
           "mh747_costo_co2", "mh747_costo_totale",
           "mh747_risparmio",
           "mh747_risparmio_per_mwh",
           "mh747_co2_evitata", "mh747_crf",
           "mh747_quota_capex", "mh747_costo_livellato",
           "mh747_prezzo_pareggio", "mh747_flussi",
           "mh747_van", "mh747_tir", "mh747_payback",
           "mh747_verdetto", "mh747_valida",
           "_mh747_neutro", "mh747_calcola",
           "mh747_csv", "mh747_demo", "demo_calcoli")

TITLE747 = ("⚓🔌 Cold ironing portuale: la corrente da banchina batte i generatori diesel di bordo?")

EH_DEMO = 1920.0
EB_DEMO = 2021.0526315789475
EF_DEMO = 4571.428571428572
CO2_B_DEMO = 1234.2857142857142
CO2_A_DEMO = 303.15789473684214
CO2_E_DEMO = 931.1278195488721
CCOMB_DEMO = 548571.4285714286
CCB_DEMO = 104914.28571428571
CEN_DEMO = 444631.5789473684
CCA_DEMO = 25768.42105263158
TB_DEMO = 653485.7142857143
TA_DEMO = 500400.0
RISP_DEMO = 153085.71428571432
RPMWH_DEMO = 79.73214285714288
CAPEX_DEMO = 1200000.0
CRF_DEMO = 0.08024258719069129
QUOTA_DEMO = 96291.10462882955
LIV_DEMO = 596691.1046288295
LIVMWH_DEMO = 310.77661699418206
BORDOMWH_DEMO = 340.3571428571429
VAN_DEMO = 707786.3718665496
TIR_DEMO = 11.242364022078561
PAYBACK_DEMO = 8
PAR_DEMO = 295.7455357142857
VERDETTO_DEMO = "CONVIENTE"

_DEMO = {
    "p_hotel_kw": 800,
    "ore_per_scalo": 24,
    "scali_anno": 100,
    "eta_connessione": 0.95,
    "eta_generatore_bordo": 0.42,
    "p_mgo_eur_mwh": 120,
    "p_elettrica_eur_mwh": 220,
    "om_bordo_eur_anno": 0,
    "om_banchina_eur_anno": 30000,
    "f_mgo_kg_mwh": 270,
    "f_rete_kg_mwh": 150,
    "prezzo_eua_eur_t": 85,
    "capex_eur": 1200000,
    "wacc_pct": 5.0,
    "vita_anni": 20,
    "tolleranza_pct": 10.0,
}

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w748_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w748_ui.py").read_text(encoding="utf-8")


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh747_demo"]()
        d.update(kw)
        return _F["mh747_valida"](**d)

    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh747_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh747_num"]("800", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh747_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh747_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh747_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh747_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh747_pos"](0.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh747_int_pos"](2.5, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh747_int_pos"](20.0, "x") == 20

    def test_int_nneg_accetta_zero_rifiuta_frazione(self):
        assert _F["mh747_int_nneg"](0.0, "x") == 0
        assert _F["mh747_int_nneg"](20.0, "x") == 20
        with pytest.raises(ValueError):
            _F["mh747_int_nneg"](2.5, "x")
        with pytest.raises(ValueError):
            _F["mh747_int_nneg"](-1.0, "x")

    def test_pct_0_100_accetta_estremi_rifiuta_fuori(self):
        assert _F["mh747_pct_0_100"](0.0, "x") == 0.0
        assert _F["mh747_pct_0_100"](100.0, "x") == 100.0
        with pytest.raises(ValueError):
            _F["mh747_pct_0_100"](-0.01, "x")
        with pytest.raises(ValueError):
            _F["mh747_pct_0_100"](100.01, "x")

    def test_pct_wacc_accetta_zero_e_50_rifiuta_oltre(self):
        assert _F["mh747_pct_wacc"](0.0, "x") == 0.0
        assert _F["mh747_pct_wacc"](50.0, "x") == 50.0
        with pytest.raises(ValueError):
            _F["mh747_pct_wacc"](-0.01, "x")
        with pytest.raises(ValueError):
            _F["mh747_pct_wacc"](50.01, "x")

    def test_eta_range(self):
        assert _F["mh747_eta"](1.0, "x") == 1.0
        with pytest.raises(ValueError):
            _F["mh747_eta"](0.0, "x")
        with pytest.raises(ValueError):
            _F["mh747_eta"](1.01, "x")

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_p_ore_scali_zero_non_validi(self):
        assert self._val(p_hotel_kw=0)["valido"] is False
        assert self._val(ore_per_scalo=0)["valido"] is False
        assert self._val(scali_anno=0)["valido"] is False

    def test_p_ore_scali_negativi_non_validi(self):
        assert self._val(p_hotel_kw=-1)["valido"] is False
        assert self._val(ore_per_scalo=-1)["valido"] is False
        assert self._val(scali_anno=-5)["valido"] is False

    def test_eta_non_validi(self):
        assert self._val(eta_connessione=0.0)["valido"] is False
        assert self._val(eta_connessione=1.01)["valido"] is False
        assert self._val(eta_generatore_bordo=0.0)["valido"] is False
        assert self._val(eta_generatore_bordo=1.01)["valido"] is False

    def test_negativi_non_validi(self):
        for k in ("p_mgo_eur_mwh", "p_elettrica_eur_mwh",
                  "om_bordo_eur_anno", "om_banchina_eur_anno",
                  "f_mgo_kg_mwh", "f_rete_kg_mwh",
                  "prezzo_eua_eur_t", "capex_eur"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_vita_zero_e_frazione_non_valide(self):
        assert self._val(vita_anni=0)["valido"] is False
        assert self._val(vita_anni=20.5)["valido"] is False

    def test_wacc_fuori_range_non_validi(self):
        assert self._val(wacc_pct=-0.01)["valido"] is False
        assert self._val(wacc_pct=50.01)["valido"] is False
        assert self._val(wacc_pct=0.0)["valido"] is True

    def test_tolleranza_fuori_range_non_valida(self):
        assert self._val(tolleranza_pct=-0.01)["valido"] is False
        assert self._val(tolleranza_pct=100.01)["valido"] is False

    def test_nan_non_valido(self):
        assert self._val(p_hotel_kw=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(p_hotel_kw=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(vita_anni=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(p_hotel_kw="800")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(p_elettrica_eur_mwh=0.0)["valido"] is True
        assert self._val(prezzo_eua_eur_t=0.0)["valido"] is True
        assert self._val(tolleranza_pct=0.0)["valido"] is True
        assert self._val(capex_eur=0.0)["valido"] is True
        assert self._val(om_bordo_eur_anno=0.0)["valido"] is True


class TestFunzioni:
    def test_e_hotel_demo_e_letterale(self):
        assert _F["mh747_e_hotel"](
            800, 24, 100) == pytest.approx(EH_DEMO, rel=REL)
        assert _F["mh747_e_hotel"](
            1000, 10, 50) == pytest.approx(500.0, rel=REL)

    def test_e_hotel_rifiuta_zero_e_frazione_scali(self):
        with pytest.raises(ValueError):
            _F["mh747_e_hotel"](0, 24, 100)
        with pytest.raises(ValueError):
            _F["mh747_e_hotel"](800, 0, 100)
        with pytest.raises(ValueError):
            _F["mh747_e_hotel"](800, 24, 100.5)

    def test_e_banchina_demo(self):
        assert _F["mh747_e_banchina"](
            EH_DEMO, 0.95) == pytest.approx(EB_DEMO, rel=REL)

    def test_e_banchina_eta_uno(self):
        assert _F["mh747_e_banchina"](
            EH_DEMO, 1.0) == pytest.approx(EH_DEMO, rel=REL)

    def test_e_banchina_rifiuta_eta(self):
        with pytest.raises(ValueError):
            _F["mh747_e_banchina"](EH_DEMO, 0.0)
        with pytest.raises(ValueError):
            _F["mh747_e_banchina"](EH_DEMO, 1.01)

    def test_e_combustibile_demo(self):
        assert _F["mh747_e_combustibile"](
            EH_DEMO, 0.42) == pytest.approx(EF_DEMO, rel=REL)

    def test_co2_demo(self):
        assert _F["mh747_co2"](
            EF_DEMO, 270) == pytest.approx(CO2_B_DEMO, rel=REL)
        assert _F["mh747_co2"](
            EB_DEMO, 150) == pytest.approx(CO2_A_DEMO, rel=REL)

    def test_costo_energia_demo(self):
        assert _F["mh747_costo_energia"](
            EF_DEMO, 120) == pytest.approx(CCOMB_DEMO, rel=REL)
        assert _F["mh747_costo_energia"](
            EB_DEMO, 220) == pytest.approx(CEN_DEMO, rel=REL)

    def test_costo_co2_demo(self):
        assert _F["mh747_costo_co2"](
            CO2_B_DEMO, 85) == pytest.approx(CCB_DEMO, rel=REL)

    def test_costo_totale_demo(self):
        assert _F["mh747_costo_totale"](
            CCOMB_DEMO, 0, CCB_DEMO) == pytest.approx(
            TB_DEMO, rel=REL)
        assert _F["mh747_costo_totale"](
            CEN_DEMO, 30000, CCA_DEMO) == pytest.approx(
            TA_DEMO, rel=REL)

    def test_risparmio_demo_e_negativo_helper(self):
        assert _F["mh747_risparmio"](
            TB_DEMO, TA_DEMO) == pytest.approx(RISP_DEMO, rel=REL)
        # L'helper calcola anche un risparmio
        # negativo: e' calcola a renderlo degenere.
        assert _F["mh747_risparmio"](
            1000.0, 2000.0) == pytest.approx(-1000.0, rel=REL)

    def test_risparmio_per_mwh_demo(self):
        assert _F["mh747_risparmio_per_mwh"](
            RISP_DEMO, EH_DEMO) == pytest.approx(
            RPMWH_DEMO, rel=REL)

    def test_risparmio_per_mwh_rifiuta_e_zero(self):
        with pytest.raises(ValueError):
            _F["mh747_risparmio_per_mwh"](RISP_DEMO, 0.0)

    def test_co2_evitata_demo_e_negativa(self):
        assert _F["mh747_co2_evitata"](
            CO2_B_DEMO, CO2_A_DEMO) == pytest.approx(
            CO2_E_DEMO, rel=REL)
        assert _F["mh747_co2_evitata"](
            1000.0, 1500.0) == pytest.approx(-500.0, rel=REL)

    def test_crf_demo(self):
        assert _F["mh747_crf"](
            5.0, 20) == pytest.approx(CRF_DEMO, rel=REL)

    def test_crf_wacc_zero_uno_su_n(self):
        assert _F["mh747_crf"](0.0, 20) == pytest.approx(
            1.0 / 20.0, rel=REL)

    def test_crf_formula_indipendente(self):
        r = 0.10
        n = 10
        atteso = r * (1.0 + r) ** n / ((1.0 + r) ** n - 1.0)
        assert _F["mh747_crf"](10.0, 10) == pytest.approx(
            atteso, rel=REL)

    def test_crf_rifiuta_wacc_oltre_50(self):
        with pytest.raises(ValueError):
            _F["mh747_crf"](50.01, 20)

    def test_quota_capex_demo(self):
        assert _F["mh747_quota_capex"](
            CAPEX_DEMO, CRF_DEMO) == pytest.approx(
            QUOTA_DEMO, rel=REL)

    def test_costo_livellato_demo(self):
        assert _F["mh747_costo_livellato"](
            TA_DEMO, QUOTA_DEMO) == pytest.approx(LIV_DEMO, rel=REL)

    def test_prezzo_pareggio_demo(self):
        assert _F["mh747_prezzo_pareggio"](
            CCOMB_DEMO, CCB_DEMO, 0, 30000, CCA_DEMO,
            EB_DEMO) == pytest.approx(PAR_DEMO, rel=REL)

    def test_prezzo_pareggio_formula_letterale(self):
        # (10000 + 2000 + 1000 - 3000 - 500) / 50 = 190.
        assert _F["mh747_prezzo_pareggio"](
            10000.0, 2000.0, 1000.0, 3000.0, 500.0,
            50.0) == pytest.approx(190.0, rel=REL)

    def test_prezzo_pareggio_none_energia_zero(self):
        assert _F["mh747_prezzo_pareggio"](
            CCOMB_DEMO, CCB_DEMO, 0, 30000, CCA_DEMO,
            0.0) is None

    def test_flussi_demo(self):
        flussi = _F["mh747_flussi"](CAPEX_DEMO, RISP_DEMO, 20)
        assert len(flussi) == 21
        assert flussi[0] == pytest.approx(-CAPEX_DEMO, rel=REL)
        assert all(f == pytest.approx(RISP_DEMO, rel=REL)
                   for f in flussi[1:])

    def test_flussi_capex_zero_primo_zero(self):
        flussi = _F["mh747_flussi"](0.0, RISP_DEMO, 20)
        assert flussi[0] == pytest.approx(0.0, rel=REL)

    def test_van_demo(self):
        flussi = _F["mh747_flussi"](CAPEX_DEMO, RISP_DEMO, 20)
        assert _F["mh747_van"](
            flussi, 5.0) == pytest.approx(VAN_DEMO, rel=REL)

    def test_van_tasso_zero(self):
        flussi = _F["mh747_flussi"](CAPEX_DEMO, RISP_DEMO, 20)
        atteso = -CAPEX_DEMO + RISP_DEMO * 20
        assert _F["mh747_van"](
            flussi, 0.0) == pytest.approx(atteso, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh747_van"]([100.0, 100.0], -0.01)

    def test_tir_none_flussi_tutti_negativi(self):
        flussi = _F["mh747_flussi"](CAPEX_DEMO, -1000.0, 20)
        assert _F["mh747_tir"](flussi) is None

    def test_tir_none_tutti_flussi_non_negativi(self):
        assert _F["mh747_tir"](
            [0.0] + [1000.0] * 20) is None

    def test_tir_esiste_caso_semplice_100_120(self):
        assert _F["mh747_tir"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_caso_semplice_1000_500_500_zero(self):
        assert abs(_F["mh747_tir"](
            [-1000.0, 500.0, 500.0])) <= 1e-9

    def test_tir_demo(self):
        flussi = _F["mh747_flussi"](CAPEX_DEMO, RISP_DEMO, 20)
        assert _F["mh747_tir"](flussi) == pytest.approx(
            TIR_DEMO / 100.0, rel=1e-9)

    def test_payback_demo_otto(self):
        flussi = _F["mh747_flussi"](CAPEX_DEMO, RISP_DEMO, 20)
        assert _F["mh747_payback"](flussi) == PAYBACK_DEMO

    def test_payback_semplice_due(self):
        assert _F["mh747_payback"]([-1000.0, 500.0, 500.0]) == 2

    def test_payback_zero_capex_zero(self):
        assert _F["mh747_payback"](
            [0.0, 153085.71428571432]) == 0

    def test_payback_none_mai(self):
        assert _F["mh747_payback"](
            [-1200000.0] + [0.0] * 20) is None
        assert _F["mh747_payback"](
            [-1200000.0] + [-1000.0] * 20) is None

    def test_payback_equivale_ceil(self):
        flussi = _F["mh747_flussi"](CAPEX_DEMO, RISP_DEMO, 20)
        assert _F["mh747_payback"](flussi) == math.ceil(
            CAPEX_DEMO / RISP_DEMO)

    def test_verdetto_demo(self):
        assert _F["mh747_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 10.0) == VERDETTO_DEMO

    def test_verdetto_conviente_van_positivo(self):
        assert _F["mh747_verdetto"](
            1000.0, CAPEX_DEMO, 10.0) == "CONVIENTE"

    def test_verdetto_van_zero_marginale(self):
        assert _F["mh747_verdetto"](
            0.0, CAPEX_DEMO, 10.0) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh747_verdetto"](
            -0.10 * CAPEX_DEMO, CAPEX_DEMO, 10.0) == "MARGINALE"

    def test_verdetto_non_conviente_oltre_limite(self):
        assert _F["mh747_verdetto"](
            -0.10 * CAPEX_DEMO - 1.0, CAPEX_DEMO,
            10.0) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_van_nan(self):
        assert _F["mh747_verdetto"](
            float("nan"), CAPEX_DEMO, 10.0) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_toll_invalida(self):
        assert _F["mh747_verdetto"](
            1000.0, CAPEX_DEMO, 100.01) == "NON_CALCOLABILE"


class TestDemo:
    def _bc(self, **kw):
        d = _F["mh747_demo"]()
        d.update(kw)
        return _F["mh747_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["e_hotel_mwh"] == pytest.approx(EH_DEMO, rel=REL)
        assert c["e_banchina_mwh"] == pytest.approx(EB_DEMO, rel=REL)
        assert c["e_combustibile_mwh"] == pytest.approx(
            EF_DEMO, rel=REL)
        assert c["co2_bordo_t"] == pytest.approx(CO2_B_DEMO, rel=REL)
        assert c["co2_banchina_t"] == pytest.approx(
            CO2_A_DEMO, rel=REL)
        assert c["co2_evitata_t"] == pytest.approx(
            CO2_E_DEMO, rel=REL)
        assert c["costo_combustibile_eur"] == pytest.approx(
            CCOMB_DEMO, rel=REL)
        assert c["costo_co2_bordo_eur"] == pytest.approx(
            CCB_DEMO, rel=REL)
        assert c["costo_energia_banchina_eur"] == pytest.approx(
            CEN_DEMO, rel=REL)
        assert c["costo_co2_banchina_eur"] == pytest.approx(
            CCA_DEMO, rel=REL)
        assert c["totale_bordo_eur"] == pytest.approx(
            TB_DEMO, rel=REL)
        assert c["totale_banchina_eur"] == pytest.approx(
            TA_DEMO, rel=REL)
        assert c["risparmio_eur_anno"] == pytest.approx(
            RISP_DEMO, rel=REL)
        assert c["risparmio_eur_mwh"] == pytest.approx(
            RPMWH_DEMO, rel=REL)
        assert c["capex_eur_out"] == pytest.approx(
            CAPEX_DEMO, rel=REL)
        assert c["crf"] == pytest.approx(CRF_DEMO, rel=REL)
        assert c["quota_capex_eur"] == pytest.approx(
            QUOTA_DEMO, rel=REL)
        assert c["costo_livellato_banchina_eur"] == pytest.approx(
            LIV_DEMO, rel=REL)
        assert c["costo_livellato_banchina_eur_mwh"] == pytest.approx(
            LIVMWH_DEMO, rel=REL)
        assert c["costo_bordo_eur_mwh"] == pytest.approx(
            BORDOMWH_DEMO, rel=REL)
        assert c["van"] == pytest.approx(VAN_DEMO, rel=REL)
        assert c["tir"] == pytest.approx(TIR_DEMO, rel=REL)
        assert c["payback"] == PAYBACK_DEMO
        assert c["prezzo_pareggio_eur_mwh"] == pytest.approx(
            PAR_DEMO, rel=REL)
        assert c["verdetto"] == VERDETTO_DEMO
        assert len(c["flussi"]) == 21

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()["van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()["risparmio_eur_anno"] == \
            _F["demo_calcoli"]()["risparmio_eur_anno"]

    def test_demo_defaults_contro_costanti_test(self):
        d = _F["mh747_demo"]()
        for k, v in _DEMO.items():
            assert d[k] == v, k
        assert len(d) == 16

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("e_hotel_mwh",
                       "e_banchina_mwh",
                       "e_combustibile_mwh",
                       "co2_bordo_t",
                       "co2_banchina_t",
                       "co2_evitata_t",
                       "costo_combustibile_eur",
                       "costo_co2_bordo_eur",
                       "costo_energia_banchina_eur",
                       "costo_co2_banchina_eur",
                       "totale_bordo_eur",
                       "totale_banchina_eur",
                       "risparmio_eur_anno",
                       "risparmio_eur_mwh",
                       "capex_eur_out",
                       "crf",
                       "quota_capex_eur",
                       "costo_livellato_banchina_eur",
                       "costo_livellato_banchina_eur_mwh",
                       "costo_bordo_eur_mwh",
                       "van",
                       "tir",
                       "prezzo_pareggio_eur_mwh"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 8" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_prezzo_pareggio_identita(self):
        # Al prezzo di pareggio il risparmio si
        # azzera: pareggio x E_banchina +
        # O&M banchina + costo CO2 banchina
        # = totale bordo. (In calcola il caso
        # al pareggio esatto e' degenere per
        # il brief, perche' il risparmio e' 0:
        # qui si verifica l'identita' sui
        # valori della demo, non via calcola.)
        c = _F["demo_calcoli"]()
        lhs = c["prezzo_pareggio_eur_mwh"] * c["e_banchina_mwh"] \
            + c["om_banchina_eur_anno"] \
            + c["costo_co2_banchina_eur"]
        assert lhs == pytest.approx(
            c["totale_bordo_eur"], rel=REL)

    def test_prezzo_pareggio_esatto_degenere(self):
        # Al prezzo di pareggio esatto il
        # risparmio e' 0 -> degenere per il
        # brief tab747 (NON un caso valido).
        n = self._bc(p_elettrica_eur_mwh=295.7455357142857)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_capex_2000000_marginale(self):
        # CAPEX 2000000 EUR: VAN -92213,63 EUR,
        # entro la tolleranza del 10 % del
        # CAPEX (200000 EUR) -> MARGINALE,
        # payback 14.
        n = self._bc(capex_eur=2000000.0)
        assert n["valid"] is True
        assert abs(n["van"] + 92213.63) <= 1.0
        assert n["payback"] == 14
        assert n["verdetto"] == "MARGINALE"

    def test_capex_600000_conviente(self):
        # CAPEX 600000 EUR: VAN +1307786,37 EUR,
        # payback 4 -> CONVIENTE.
        n = self._bc(capex_eur=600000.0)
        assert n["valid"] is True
        assert abs(n["van"] - 1307786.37) <= 1.0
        assert n["payback"] == 4
        assert n["verdetto"] == "CONVIENTE"

    def test_rete_sporca_co2_negativa_calcolabile(self):
        # Fattore rete 800 kg/MWh: CO2 banchina
        # 1616,84 t, evitata -382,56 t (NEGATIVA)
        # ma risparmio 41422,56 EUR/anno > 0:
        # NON degenere, VAN -683783,39 EUR ->
        # NON_CONVIENTE.
        n = self._bc(f_rete_kg_mwh=800.0)
        assert n["valid"] is True
        assert n["co2_evitata_t"] == pytest.approx(
            -382.56, rel=1e-3)
        assert n["risparmio_eur_anno"] == pytest.approx(
            41422.56, rel=1e-3)
        assert abs(n["van"] + 683783.39) <= 1.0
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_mgo_80_risparmio_negativo_degenere(self):
        # Prezzo MGO 80 EUR/MWh: totale bordo
        # 470628,57 EUR sotto il totale
        # banchina -> risparmio negativo ->
        # degenere per il brief tab747.
        n = self._bc(p_mgo_eur_mwh=80.0)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_elettrica_400_risparmio_negativo_degenere(self):
        n = self._bc(p_elettrica_eur_mwh=400.0)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_elettrica_290_non_conviente_calcolabile(self):
        # Prezzo elettrico 290 EUR/MWh: risparmio
        # 11612,03 EUR/anno > 0 ma VAN
        # -1055288,44 EUR -> NON_CONVIENTE.
        n = self._bc(p_elettrica_eur_mwh=290.0)
        assert n["valid"] is True
        assert n["risparmio_eur_anno"] == pytest.approx(
            11612.03, rel=1e-3)
        assert abs(n["van"] + 1055288.44) <= 1.0
        assert n["payback"] is None
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_eta_conn_uno(self):
        # Rendimento connessione 1,0: energia da
        # banchina 1920 MWh, risparmio
        # 176605,71 EUR/anno, VAN +1000897,56.
        n = self._bc(eta_connessione=1.0)
        assert n["valid"] is True
        assert n["e_banchina_mwh"] == pytest.approx(
            EH_DEMO, rel=REL)
        assert abs(n["van"] - 1000897.56) <= 1.0
        assert n["verdetto"] == "CONVIENTE"

    def test_wacc_zero_valido_crf_uno_su_n(self):
        n = self._bc(wacc_pct=0.0)
        assert n["valid"] is True
        assert n["crf"] == pytest.approx(
            1.0 / 20.0, rel=REL)
        assert n["quota_capex_eur"] == pytest.approx(
            60000.0, rel=1e-3)
        assert n["van"] == pytest.approx(
            1861714.29, rel=1e-3)

    def test_p_zero_neutro(self):
        n = self._bc(p_hotel_kw=0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_ore_zero_neutro(self):
        n = self._bc(ore_per_scalo=0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_scali_zero_neutro(self):
        n = self._bc(scali_anno=0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_eta_neutri(self):
        for kw in ({"eta_connessione": 0.0},
                   {"eta_connessione": 1.01},
                   {"eta_generatore_bordo": 0.0},
                   {"eta_generatore_bordo": 1.01}):
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
        n = self._bc(p_hotel_kw=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_anno"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(p_hotel_kw=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(vita_anni=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_stringa_neutro(self):
        n = self._bc(p_hotel_kw="800")
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzo_negativo_neutro(self):
        n = self._bc(p_elettrica_eur_mwh=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh747_neutro"]()
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
        assert n["prezzo_pareggio_eur_mwh"] is None
        assert n["risparmio_eur_mwh"] is None
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh747_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "p_hotel_kw", "ore_per_scalo",
                       "scali_anno", "eta_connessione",
                       "eta_generatore_bordo",
                       "p_mgo_eur_mwh",
                       "p_elettrica_eur_mwh",
                       "om_bordo_eur_anno",
                       "om_banchina_eur_anno",
                       "f_mgo_kg_mwh", "f_rete_kg_mwh",
                       "prezzo_eua_eur_t",
                       "capex_eur",
                       "wacc_pct", "vita_anni",
                       "tolleranza_pct",
                       "e_hotel_mwh", "e_banchina_mwh",
                       "e_combustibile_mwh",
                       "co2_bordo_t", "co2_banchina_t",
                       "co2_evitata_t",
                       "costo_combustibile_eur",
                       "costo_co2_bordo_eur",
                       "costo_energia_banchina_eur",
                       "costo_co2_banchina_eur",
                       "totale_bordo_eur",
                       "totale_banchina_eur",
                       "risparmio_eur_anno",
                       "risparmio_eur_mwh",
                       "capex_eur_out",
                       "crf", "quota_capex_eur",
                       "costo_livellato_banchina_eur",
                       "costo_livellato_banchina_eur_mwh",
                       "costo_bordo_eur_mwh",
                       "flussi", "van", "tir",
                       "payback",
                       "prezzo_pareggio_eur_mwh",
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
        assert "Energia hotel (MWh/anno)" in voci
        assert "Energia da banchina (MWh/anno)" in voci
        assert "Combustibile risparmiato (MWh/anno)" in voci
        assert "CO2 bordo (tCO2/anno)" in voci
        assert "CO2 banchina (tCO2/anno)" in voci
        assert "CO2 evitata (tCO2/anno)" in voci
        assert "Costo totale bordo (EUR/anno)" in voci
        assert "Costo totale banchina (EUR/anno)" in voci
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
            pytest.approx(-CAPEX_DEMO, rel=REL)
        assert b["df_flussi"]["Flusso (EUR/anno)"].iloc[1] == \
            pytest.approx(RISP_DEMO, rel=REL)

    def test_crf_solo_livellato_non_nei_flussi(self):
        # I flussi contengono solo -CAPEX e
        # risparmio: la quota CRF non compare
        # mai nei flussi (contarla anche li'
        # conterebbe il CAPEX due volte).
        c = self._bc()
        assert c["flussi"][0] == pytest.approx(
            -CAPEX_DEMO, rel=REL)
        assert all(f == pytest.approx(RISP_DEMO, rel=REL)
                   for f in c["flussi"][1:])
        assert c["quota_capex_eur"] == pytest.approx(
            QUOTA_DEMO, rel=REL)
        assert c["costo_livellato_banchina_eur"] == pytest.approx(
            TA_DEMO + QUOTA_DEMO, rel=REL)


class TestCsv:
    def _ing(self):
        return _F["mh747_demo"]()

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh747_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") == 42
        assert len(txt.strip().splitlines()) == 42

    def test_csv_contiene_verdetti_e_costi(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh747_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "capex_eur_out" in txt
        assert "van_eur" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "prezzo_pareggio_eur_mwh" in txt
        assert "risparmio_eur_anno" in txt
        assert "totale_banchina_eur" in txt
        assert "e_hotel_mwh" in txt
        assert "co2_evitata_t" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh747_csv"](bc, self._ing())
        assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in txt
        assert f"co2_evitata_t;{bc['co2_evitata_t']}" in txt
        assert "p_hotel_kw;800" in txt
        assert "p_elettrica_eur_mwh;220" in txt
        assert f"costo_livellato_banchina_eur_mwh;{bc['costo_livellato_banchina_eur_mwh']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def747["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def747\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 16, ui_keys
        demo_keys = set(_F["mh747_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh747_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh747_demo():")
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
        ui_keys = set(re.findall(r'_def747\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W748 (27/10/2026) - tab747' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh747_num", "mh747_nneg", "mh747_pos",
                     "mh747_int_pos", "mh747_int_nneg",
                     "mh747_pct_0_100", "mh747_pct_wacc",
                     "mh747_eta", "mh747_e_hotel",
                     "mh747_e_banchina",
                     "mh747_e_combustibile",
                     "mh747_co2", "mh747_costo_energia",
                     "mh747_costo_co2",
                     "mh747_costo_totale",
                     "mh747_risparmio",
                     "mh747_risparmio_per_mwh",
                     "mh747_co2_evitata",
                     "mh747_crf", "mh747_quota_capex",
                     "mh747_costo_livellato",
                     "mh747_prezzo_pareggio",
                     "mh747_flussi", "mh747_van",
                     "mh747_tir", "mh747_payback",
                     "mh747_verdetto", "mh747_valida",
                     "_mh747_neutro",
                     "mh747_calcola", "mh747_csv",
                     "mh747_demo", "demo_calcoli"):
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
        mh_old = "mh" + "746"
        st_old = "st" + "746"
        tab_old = "tab" + "746"
        w_old = "W" + "747"
        assert mh_old not in _helpers_src()
        assert mh_old not in _ui_src()
        assert st_old not in _ui_src()
        assert tab_old not in _ui_src()
        assert w_old not in _helpers_src()
        assert w_old not in _ui_src()
        assert "mh747" in _helpers_src()
        assert "st747" in _ui_src()

    def test_helpers_parse_ast(self):
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w748_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE747) == 1

    def test_blocco_with_tab747(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab747:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE747

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st747_[A-Za-z0-9_]+)"', _ui_src())
        assert len(keys) == 24, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st747_") for k in keys)
