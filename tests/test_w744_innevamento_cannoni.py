"""Test tab744 "Innevamento artificiale: cannoni ventilatori o lance ad aria compressa?"

Nuova tab tab744 (innevamento
artificiale, w745). Business case
deterministico dell'innevamento
artificiale: per produrre un manto
target su una pista, confronta
BASE = lance ad aria compressa
contro ALT = cannoni ventilatori.
Volume da area e profondita',
acqua da volume, densita' e
perdite, energia da volume e
consumo specifico, CO2 da energia
e fattore di rete, costi da
energia, acqua, O&M e EUA, CAPEX
da numero e prezzo unitario,
VAN, TIR, payback e prezzo
elettrico di pareggio. Nessuna
altra tab e' dedicata
all'innevamento: 0 occorrenze di
"innevamento" in app.py prima di
questa tab; i 4 hit "neve"
altrove sono scioglimento nivale
in idroelettrico e albedo, non
produzione di neve.

Demo calcolata eseguendo demo_calcoli()
(e ricontrollata a mano, riga per riga):
area 30 ha; profondita' 0,50 m;
densita' 400 kg/m3; perdite 15 %;
consumo fan 1,8 kWh/m3 e lance
4,5 kWh/m3; prezzo elettricita'
240 EUR/MWh; prezzo acqua 1,20
EUR/m3; O&M fan 18000 EUR/anno e
lance 11000 EUR/anno; n_fan 50 a
25000 EUR e n_lance 90 a 6000
EUR; fattore rete 150 kg/MWh;
prezzo EUA 85 EUR/t; WACC 5 %;
vita 20 anni; tolleranza 10 % del
CAPEX delta.

- volume_neve_m3 = 150000.0
- acqua_m3 = 69000.0
- energia_fan_kwh = 270000.0
- energia_fan_MWh = 270.0
- energia_lance_kwh = 675000.0
- energia_lance_MWh = 675.0
- co2_fan_t = 40.5
- co2_lance_t = 101.25
- co2_risparmiata_t = 60.75
- costo_energia_fan_eur = 64800.0
- costo_energia_lance_eur = 162000.0
- costo_acqua_eur = 82800.0
- costo_co2_fan_eur = 3442.5
- costo_co2_lance_eur = 8606.25
- totale_fan_eur = 169042.5
- totale_lance_eur = 264406.25
- risparmio_eur_anno = 95363.75
- risparmio_eur_m3 = 0.6357583333333333
- costo_per_m3_fan_eur = 1.12695
- costo_per_m3_lance_eur = 1.7627083333333333
- capex_fan_eur = 1250000.0
- capex_lance_eur = 540000.0
- capex_delta_eur = 710000.0
- crf = 0.08024258719069129
- quota_capex_eur = 56972.23690539081
- costo_livellato_alt_eur = 226014.7369053908
- costo_livellato_eur_m3 = 1.5067649127026053
- van = 478443.11155339715
- tir = 12.051972267099071
- payback = 8
- prezzo_pareggio_eur_MWh = 593.199074074074
- verdetto = 'CONVIENTE'

Scomposizione: volume 30 x 10000 x 0,50 =
150000.0 m3; acqua 150000.0 x 400 / 1000 x
1,15 = 69000.0 m3; energia fan 150000.0 x
1,8 = 270000.0 kWh = 270.0 MWh; energia
lance 150000.0 x 4,5 = 675000.0 kWh =
675.0 MWh; CO2 fan 270.0 x 150 / 1000 =
40.5 t; CO2 lance 675.0 x 150 / 1000 =
101.25 t; risparmiata 101.25 - 40.5 =
60.75 t; costo energia fan 270.0 x 240 =
64800.0 EUR; costo energia lance 675.0 x
240 = 162000.0 EUR; costo acqua 69000.0 x
1,20 = 82800.0 EUR; costo CO2 fan 40.5 x
85 = 3442.5 EUR; costo CO2 lance 101.25 x
85 = 8606.25 EUR; totali 64800.0 + 82800.0
+ 18000 + 3442.5 = 169042.5 EUR contro
162000.0 + 82800.0 + 11000 + 8606.25 =
264406.25 EUR; risparmio 264406.25 -
169042.5 = 95363.75 EUR/anno =
0.6357583333333333 EUR/m3; costi per m3
169042.5 / 150000.0 = 1.12695 EUR/m3
contro 264406.25 / 150000.0 =
1.7627083333333333 EUR/m3; CAPEX fan 50 x
25000 = 1250000.0 EUR; CAPEX lance 90 x
6000 = 540000.0 EUR; delta 710000.0 EUR;
CRF 0,05 x 1,05^20 / (1,05^20 - 1) =
0.08024258719069129; quota CAPEX 710000.0
x 0.08024258719069129 = 56972.23690539081
EUR/anno; costo livellato 169042.5 +
56972.23690539081 = 226014.7369053908
EUR/anno = 1.5067649127026053 EUR/m3;
flussi: anno 0 -710000.0, anni 1-20
risparmio 95363.75 (piatti); VAN
-710000.0 + 95363.75 x 12.462210342539992
(annuita' 20 anni al 5 %) =
478443.11155339715 EUR; TIR
12.051972267099071 %; payback 8 (ceil di
710000.0 / 95363.75 = 7,45); prezzo
elettrico di pareggio (264406.25 -
82800.0 - 18000) / 270.0 - 150 x 85 /
1000 = 593.199074074074 EUR/MWh;
verdetto CONVIENTE perche' VAN > 0.
NOTA: il CRF entra solo nel costo
livellato, mai nei flussi: il
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
    if (p / "w745_helpers.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w745_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w745_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w745_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w745_helpers.py: {missing}")
    return out


_F = _load("mh744_num", "mh744_nneg", "mh744_pos",
           "mh744_int_pos", "mh744_int_nneg",
           "mh744_pct_0_100", "mh744_pct_wacc",
           "mh744_volume_neve", "mh744_acqua_m3",
           "mh744_energia_kwh", "mh744_energia_MWh",
           "mh744_co2", "mh744_costo_energia",
           "mh744_costo_acqua", "mh744_costo_co2",
           "mh744_costo_totale", "mh744_risparmio",
           "mh744_risparmio_per_m3", "mh744_costo_per_m3",
           "mh744_capex", "mh744_capex_delta",
           "mh744_crf", "mh744_quota_capex",
           "mh744_costo_livellato", "mh744_prezzo_pareggio",
           "mh744_flussi", "mh744_van", "mh744_tir",
           "mh744_payback", "mh744_verdetto",
           "mh744_valida", "_mh744_neutro",
           "mh744_calcola", "mh744_csv",
           "mh744_demo", "demo_calcoli")

TITLE744 = ("❄️⛷️ Innevamento artificiale: cannoni ventilatori o lance ad aria compressa?")

VOL_DEMO = 150000.0
ACQUA_DEMO = 69000.0
EF_KWH_DEMO = 270000.0
EF_MWH_DEMO = 270.0
EL_KWH_DEMO = 675000.0
EL_MWH_DEMO = 675.0
CO2_FAN_DEMO = 40.5
CO2_LANCE_DEMO = 101.25
CO2_RISP_DEMO = 60.75
CE_FAN_DEMO = 64800.0
CE_LANCE_DEMO = 162000.0
C_ACQUA_DEMO = 82800.0
CC_FAN_DEMO = 3442.5
CC_LANCE_DEMO = 8606.25
TF_DEMO = 169042.5
TL_DEMO = 264406.25
RISP_DEMO = 95363.75
RPM3_DEMO = 0.6357583333333333
PM3_FAN_DEMO = 1.12695
PM3_LANCE_DEMO = 1.7627083333333333
CX_FAN_DEMO = 1250000.0
CX_LANCE_DEMO = 540000.0
DELTA_DEMO = 710000.0
CRF_DEMO = 0.08024258719069129
QUOTA_DEMO = 56972.23690539081
LIV_DEMO = 226014.7369053908
LIVM3_DEMO = 1.5067649127026053
VAN_DEMO = 478443.11155339715
TIR_DEMO = 12.051972267099071
PAYBACK_DEMO = 8
PAR_DEMO = 593.199074074074
VERDETTO_DEMO = "CONVIENTE"

_DEMO = {
    "area_ha": 30,
    "profondita_m": 0.50,
    "densita_neve_kg_m3": 400,
    "perdite_pct": 15.0,
    "consumo_fan_kWh_m3": 1.8,
    "consumo_lance_kWh_m3": 4.5,
    "prezzo_el_EUR_MWh": 240,
    "prezzo_acqua_EUR_m3": 1.20,
    "om_fan_eur_anno": 18000,
    "om_lance_eur_anno": 11000,
    "n_fan": 50,
    "n_lance": 90,
    "prezzo_fan_EUR": 25000,
    "prezzo_lance_EUR": 6000,
    "fattore_rete_kg_MWh": 150,
    "prezzo_eua_eur_t": 85,
    "wacc_pct": 5.0,
    "vita_anni": 20,
    "tolleranza_pct": 10.0,
}

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w745_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w745_ui.py").read_text(encoding="utf-8")


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh744_demo"]()
        d.update(kw)
        return _F["mh744_valida"](**d)

    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh744_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh744_num"]("500", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh744_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh744_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh744_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh744_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh744_pos"](0.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh744_int_pos"](2.5, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh744_int_pos"](20.0, "x") == 20

    def test_int_nneg_accetta_zero_rifiuta_frazione(self):
        assert _F["mh744_int_nneg"](0.0, "x") == 0
        assert _F["mh744_int_nneg"](50.0, "x") == 50
        with pytest.raises(ValueError):
            _F["mh744_int_nneg"](2.5, "x")
        with pytest.raises(ValueError):
            _F["mh744_int_nneg"](-1.0, "x")

    def test_pct_0_100_accetta_estremi_rifiuta_fuori(self):
        assert _F["mh744_pct_0_100"](0.0, "x") == 0.0
        assert _F["mh744_pct_0_100"](100.0, "x") == 100.0
        with pytest.raises(ValueError):
            _F["mh744_pct_0_100"](-0.01, "x")
        with pytest.raises(ValueError):
            _F["mh744_pct_0_100"](100.01, "x")

    def test_pct_wacc_accetta_zero_e_50_rifiuta_oltre(self):
        assert _F["mh744_pct_wacc"](0.0, "x") == 0.0
        assert _F["mh744_pct_wacc"](50.0, "x") == 50.0
        with pytest.raises(ValueError):
            _F["mh744_pct_wacc"](-0.01, "x")
        with pytest.raises(ValueError):
            _F["mh744_pct_wacc"](50.01, "x")

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_area_profondita_zero_passano_validazione(self):
        assert self._val(area_ha=0)["valido"] is True
        assert self._val(profondita_m=0.0)["valido"] is True

    def test_area_profondita_negative_non_valide(self):
        assert self._val(area_ha=-1)["valido"] is False
        assert self._val(profondita_m=-0.1)["valido"] is False

    def test_densita_zero_non_valida(self):
        assert self._val(densita_neve_kg_m3=0)["valido"] is False

    def test_perdite_fuori_range_non_valide(self):
        assert self._val(perdite_pct=-0.01)["valido"] is False
        assert self._val(perdite_pct=100.01)["valido"] is False
        assert self._val(perdite_pct=100.0)["valido"] is True

    def test_consumi_zero_non_validi(self):
        assert self._val(consumo_fan_kWh_m3=0.0)["valido"] is False
        assert self._val(consumo_lance_kWh_m3=0.0)["valido"] is False

    def test_negativi_non_validi(self):
        for k in ("prezzo_el_EUR_MWh", "prezzo_acqua_EUR_m3",
                  "om_fan_eur_anno", "om_lance_eur_anno",
                  "prezzo_fan_EUR", "prezzo_lance_EUR",
                  "fattore_rete_kg_MWh", "prezzo_eua_eur_t"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_n_impianti_frazione_non_valida(self):
        assert self._val(n_fan=50.5)["valido"] is False
        assert self._val(n_lance=-1)["valido"] is False
        assert self._val(n_fan=0)["valido"] is True

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
        assert self._val(area_ha=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(area_ha=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(vita_anni=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(area_ha="30")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(prezzo_el_EUR_MWh=0.0)["valido"] is True
        assert self._val(prezzo_eua_eur_t=0.0)["valido"] is True
        assert self._val(tolleranza_pct=0.0)["valido"] is True
        assert self._val(n_fan=0)["valido"] is True


class TestFunzioni:
    def test_volume_neve_demo(self):
        assert _F["mh744_volume_neve"](
            30, 0.50) == pytest.approx(VOL_DEMO, rel=REL)

    def test_volume_neve_formula_letterale(self):
        assert _F["mh744_volume_neve"](
            10, 1.0) == pytest.approx(100000.0, rel=REL)

    def test_volume_neve_area_zero(self):
        assert _F["mh744_volume_neve"](0, 0.50) == 0.0

    def test_acqua_demo(self):
        assert _F["mh744_acqua_m3"](
            VOL_DEMO, 400, 15.0) == pytest.approx(
            ACQUA_DEMO, rel=REL)

    def test_acqua_senza_perdite(self):
        assert _F["mh744_acqua_m3"](
            100000.0, 400, 0.0) == pytest.approx(40000.0, rel=REL)

    def test_acqua_rifiuta_densita_zero(self):
        with pytest.raises(ValueError):
            _F["mh744_acqua_m3"](VOL_DEMO, 0, 15.0)

    def test_energia_kwh_demo(self):
        assert _F["mh744_energia_kwh"](
            VOL_DEMO, 1.8) == pytest.approx(EF_KWH_DEMO, rel=REL)
        assert _F["mh744_energia_kwh"](
            VOL_DEMO, 4.5) == pytest.approx(EL_KWH_DEMO, rel=REL)

    def test_energia_MWh_demo(self):
        assert _F["mh744_energia_MWh"](
            EF_KWH_DEMO) == pytest.approx(EF_MWH_DEMO, rel=REL)

    def test_co2_demo(self):
        assert _F["mh744_co2"](
            EF_MWH_DEMO, 150) == pytest.approx(CO2_FAN_DEMO, rel=REL)
        assert _F["mh744_co2"](
            EL_MWH_DEMO, 150) == pytest.approx(CO2_LANCE_DEMO, rel=REL)

    def test_costo_energia_demo(self):
        assert _F["mh744_costo_energia"](
            EF_MWH_DEMO, 240) == pytest.approx(CE_FAN_DEMO, rel=REL)
        assert _F["mh744_costo_energia"](
            EL_MWH_DEMO, 240) == pytest.approx(CE_LANCE_DEMO, rel=REL)

    def test_costo_acqua_demo(self):
        assert _F["mh744_costo_acqua"](
            ACQUA_DEMO, 1.20) == pytest.approx(C_ACQUA_DEMO, rel=REL)

    def test_costo_co2_demo(self):
        assert _F["mh744_costo_co2"](
            CO2_FAN_DEMO, 85) == pytest.approx(CC_FAN_DEMO, rel=REL)

    def test_costo_totale_fan_demo(self):
        assert _F["mh744_costo_totale"](
            CE_FAN_DEMO, C_ACQUA_DEMO, 18000,
            CC_FAN_DEMO) == pytest.approx(TF_DEMO, rel=REL)

    def test_costo_totale_lance_demo(self):
        assert _F["mh744_costo_totale"](
            CE_LANCE_DEMO, C_ACQUA_DEMO, 11000,
            CC_LANCE_DEMO) == pytest.approx(TL_DEMO, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh744_risparmio"](
            TL_DEMO, TF_DEMO) == pytest.approx(RISP_DEMO, rel=REL)

    def test_risparmio_negativo_ventilatori_piu_cari(self):
        assert _F["mh744_risparmio"](
            1000.0, 2000.0) == pytest.approx(-1000.0, rel=REL)

    def test_risparmio_per_m3_demo(self):
        assert _F["mh744_risparmio_per_m3"](
            RISP_DEMO, VOL_DEMO) == pytest.approx(RPM3_DEMO, rel=REL)

    def test_risparmio_per_m3_rifiuta_volume_zero(self):
        with pytest.raises(ValueError):
            _F["mh744_risparmio_per_m3"](RISP_DEMO, 0.0)

    def test_costo_per_m3_demo(self):
        assert _F["mh744_costo_per_m3"](
            TF_DEMO, VOL_DEMO) == pytest.approx(PM3_FAN_DEMO, rel=REL)
        assert _F["mh744_costo_per_m3"](
            TL_DEMO, VOL_DEMO) == pytest.approx(PM3_LANCE_DEMO, rel=REL)

    def test_capex_demo(self):
        assert _F["mh744_capex"](
            50, 25000) == pytest.approx(CX_FAN_DEMO, rel=REL)
        assert _F["mh744_capex"](
            90, 6000) == pytest.approx(CX_LANCE_DEMO, rel=REL)

    def test_capex_delta_demo(self):
        assert _F["mh744_capex_delta"](
            CX_FAN_DEMO, CX_LANCE_DEMO) == pytest.approx(
            DELTA_DEMO, rel=REL)

    def test_capex_delta_negativo(self):
        assert _F["mh744_capex_delta"](
            100.0, 200.0) == pytest.approx(-100.0, rel=REL)

    def test_crf_demo(self):
        assert _F["mh744_crf"](
            5.0, 20) == pytest.approx(CRF_DEMO, rel=REL)

    def test_crf_wacc_zero_uno_su_n(self):
        assert _F["mh744_crf"](0.0, 20) == pytest.approx(
            1.0 / 20.0, rel=REL)

    def test_crf_formula_indipendente(self):
        r = 0.10
        n = 10
        atteso = r * (1.0 + r) ** n / ((1.0 + r) ** n - 1.0)
        assert _F["mh744_crf"](10.0, 10) == pytest.approx(
            atteso, rel=REL)

    def test_crf_rifiuta_wacc_oltre_50(self):
        with pytest.raises(ValueError):
            _F["mh744_crf"](50.01, 20)

    def test_quota_capex_demo(self):
        assert _F["mh744_quota_capex"](
            DELTA_DEMO, CRF_DEMO) == pytest.approx(
            QUOTA_DEMO, rel=REL)

    def test_costo_livellato_demo(self):
        assert _F["mh744_costo_livellato"](
            TF_DEMO, QUOTA_DEMO) == pytest.approx(LIV_DEMO, rel=REL)

    def test_prezzo_pareggio_demo(self):
        assert _F["mh744_prezzo_pareggio"](
            TL_DEMO, C_ACQUA_DEMO, 18000,
            EF_MWH_DEMO, 150, 85) == pytest.approx(PAR_DEMO, rel=REL)

    def test_prezzo_pareggio_formula_letterale(self):
        # (100000 - 20000 - 5000) / 500 - 200 x 50 / 1000 = 140.
        assert _F["mh744_prezzo_pareggio"](
            100000.0, 20000.0, 5000.0, 500.0,
            200.0, 50.0) == pytest.approx(140.0, rel=REL)

    def test_prezzo_pareggio_rifiuta_mwh_zero(self):
        with pytest.raises(ValueError):
            _F["mh744_prezzo_pareggio"](
                TL_DEMO, C_ACQUA_DEMO, 18000, 0.0, 150, 85)

    def test_flussi_demo(self):
        flussi = _F["mh744_flussi"](DELTA_DEMO, RISP_DEMO, 20)
        assert len(flussi) == 21
        assert flussi[0] == pytest.approx(-DELTA_DEMO, rel=REL)
        assert all(f == pytest.approx(RISP_DEMO, rel=REL)
                   for f in flussi[1:])

    def test_van_demo(self):
        flussi = _F["mh744_flussi"](DELTA_DEMO, RISP_DEMO, 20)
        assert _F["mh744_van"](
            flussi, 5.0) == pytest.approx(VAN_DEMO, rel=REL)

    def test_van_tasso_zero(self):
        flussi = _F["mh744_flussi"](DELTA_DEMO, RISP_DEMO, 20)
        atteso = -DELTA_DEMO + RISP_DEMO * 20
        assert _F["mh744_van"](
            flussi, 0.0) == pytest.approx(atteso, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh744_van"]([100.0, 100.0], -0.01)

    def test_tir_none_flussi_tutti_negativi(self):
        flussi = _F["mh744_flussi"](DELTA_DEMO, -1000.0, 20)
        assert _F["mh744_tir"](flussi) is None

    def test_tir_none_tutti_flussi_non_negativi(self):
        assert _F["mh744_tir"](
            [0.0] + [1000.0] * 20) is None

    def test_tir_esiste_caso_semplice_100_120(self):
        assert _F["mh744_tir"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_caso_semplice_1000_500_500_zero(self):
        assert abs(_F["mh744_tir"](
            [-1000.0, 500.0, 500.0])) <= 1e-9

    def test_tir_demo(self):
        flussi = _F["mh744_flussi"](DELTA_DEMO, RISP_DEMO, 20)
        assert _F["mh744_tir"](flussi) == pytest.approx(
            TIR_DEMO / 100.0, rel=1e-9)

    def test_payback_demo_8(self):
        assert _F["mh744_payback"](
            DELTA_DEMO, RISP_DEMO) == 8

    def test_payback_semplice_due(self):
        assert _F["mh744_payback"](1000.0, 500.0) == 2

    def test_payback_zero_capex_zero(self):
        assert _F["mh744_payback"](0.0, 1000.0) == 0

    def test_payback_none_risparmio_zero(self):
        assert _F["mh744_payback"](1000.0, 0.0) is None

    def test_payback_none_risparmio_negativo(self):
        assert _F["mh744_payback"](1000.0, -500.0) is None

    def test_payback_ceil_non_intero(self):
        assert _F["mh744_payback"](1000.0, 300.0) == 4

    def test_verdetto_demo(self):
        assert _F["mh744_verdetto"](
            VAN_DEMO, DELTA_DEMO, 10.0,
            RISP_DEMO) == VERDETTO_DEMO

    def test_verdetto_conviente_van_positivo(self):
        assert _F["mh744_verdetto"](
            1000.0, DELTA_DEMO, 10.0,
            RISP_DEMO) == "CONVIENTE"

    def test_verdetto_van_zero_marginale(self):
        assert _F["mh744_verdetto"](
            0.0, DELTA_DEMO, 10.0,
            RISP_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh744_verdetto"](
            -0.10 * DELTA_DEMO, DELTA_DEMO, 10.0,
            RISP_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_oltre_limite(self):
        assert _F["mh744_verdetto"](
            -0.10 * DELTA_DEMO - 1.0, DELTA_DEMO, 10.0,
            RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_zero(self):
        assert _F["mh744_verdetto"](
            1000.0, DELTA_DEMO, 10.0,
            0.0) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_risparmio_negativo(self):
        assert _F["mh744_verdetto"](
            1000.0, DELTA_DEMO, 10.0,
            -5000.0) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_risparmio_nan(self):
        assert _F["mh744_verdetto"](
            1000.0, DELTA_DEMO, 10.0,
            float("nan")) == "NON_CALCOLABILE"


class TestDemo:
    def _bc(self, **kw):
        d = _F["mh744_demo"]()
        d.update(kw)
        return _F["mh744_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["volume_neve_m3"] == pytest.approx(VOL_DEMO, rel=REL)
        assert c["acqua_m3"] == pytest.approx(ACQUA_DEMO, rel=REL)
        assert c["energia_fan_kwh"] == pytest.approx(
            EF_KWH_DEMO, rel=REL)
        assert c["energia_fan_MWh"] == pytest.approx(
            EF_MWH_DEMO, rel=REL)
        assert c["energia_lance_kwh"] == pytest.approx(
            EL_KWH_DEMO, rel=REL)
        assert c["energia_lance_MWh"] == pytest.approx(
            EL_MWH_DEMO, rel=REL)
        assert c["co2_fan_t"] == pytest.approx(CO2_FAN_DEMO, rel=REL)
        assert c["co2_lance_t"] == pytest.approx(
            CO2_LANCE_DEMO, rel=REL)
        assert c["co2_risparmiata_t"] == pytest.approx(
            CO2_RISP_DEMO, rel=REL)
        assert c["costo_energia_fan_eur"] == pytest.approx(
            CE_FAN_DEMO, rel=REL)
        assert c["costo_energia_lance_eur"] == pytest.approx(
            CE_LANCE_DEMO, rel=REL)
        assert c["costo_acqua_eur"] == pytest.approx(
            C_ACQUA_DEMO, rel=REL)
        assert c["costo_co2_fan_eur"] == pytest.approx(
            CC_FAN_DEMO, rel=REL)
        assert c["costo_co2_lance_eur"] == pytest.approx(
            CC_LANCE_DEMO, rel=REL)
        assert c["totale_fan_eur"] == pytest.approx(TF_DEMO, rel=REL)
        assert c["totale_lance_eur"] == pytest.approx(
            TL_DEMO, rel=REL)
        assert c["risparmio_eur_anno"] == pytest.approx(
            RISP_DEMO, rel=REL)
        assert c["risparmio_eur_m3"] == pytest.approx(
            RPM3_DEMO, rel=REL)
        assert c["costo_per_m3_fan_eur"] == pytest.approx(
            PM3_FAN_DEMO, rel=REL)
        assert c["costo_per_m3_lance_eur"] == pytest.approx(
            PM3_LANCE_DEMO, rel=REL)
        assert c["capex_fan_eur"] == pytest.approx(
            CX_FAN_DEMO, rel=REL)
        assert c["capex_lance_eur"] == pytest.approx(
            CX_LANCE_DEMO, rel=REL)
        assert c["capex_delta_eur"] == pytest.approx(
            DELTA_DEMO, rel=REL)
        assert c["crf"] == pytest.approx(CRF_DEMO, rel=REL)
        assert c["quota_capex_eur"] == pytest.approx(
            QUOTA_DEMO, rel=REL)
        assert c["costo_livellato_alt_eur"] == pytest.approx(
            LIV_DEMO, rel=REL)
        assert c["costo_livellato_eur_m3"] == pytest.approx(
            LIVM3_DEMO, rel=REL)
        assert c["van"] == pytest.approx(VAN_DEMO, rel=REL)
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
        d = _F["mh744_demo"]()
        for k, v in _DEMO.items():
            assert d[k] == v, k
        assert len(d) == 19

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("volume_neve_m3",
                       "acqua_m3",
                       "energia_fan_kwh",
                       "energia_fan_MWh",
                       "energia_lance_kwh",
                       "energia_lance_MWh",
                       "co2_fan_t",
                       "co2_lance_t",
                       "co2_risparmiata_t",
                       "costo_energia_fan_eur",
                       "costo_energia_lance_eur",
                       "costo_acqua_eur",
                       "costo_co2_fan_eur",
                       "costo_co2_lance_eur",
                       "totale_fan_eur",
                       "totale_lance_eur",
                       "risparmio_eur_anno",
                       "risparmio_eur_m3",
                       "costo_per_m3_fan_eur",
                       "costo_per_m3_lance_eur",
                       "capex_fan_eur",
                       "capex_lance_eur",
                       "capex_delta_eur",
                       "crf",
                       "quota_capex_eur",
                       "costo_livellato_alt_eur",
                       "costo_livellato_eur_m3",
                       "van",
                       "tir",
                       "prezzo_pareggio_eur_MWh"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback = 8" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_prezzo_elettrico_700_conviente(self):
        # Prezzo elettrico 700 EUR/MWh: lo
        # stesso prezzo si applica anche alle
        # lance, che consumano di piu' (675
        # contro 270 MWh), quindi il risparmio
        # CRESCE: totale fan 293.242,50 EUR,
        # totale lance 574.906,25 EUR, risparmio
        # 281.663,75 EUR/anno, VAN circa
        # +2.800.152,90 EUR -> CONVIENTE.
        n = self._bc(prezzo_el_EUR_MWh=700.0)
        assert n["valid"] is True
        assert n["totale_fan_eur"] == pytest.approx(
            293242.5, rel=REL)
        assert n["totale_lance_eur"] == pytest.approx(
            574906.25, rel=REL)
        assert n["risparmio_eur_anno"] == pytest.approx(
            281663.75, rel=REL)
        assert abs(n["van"] - 2800152.90) <= 1.0
        assert n["verdetto"] == "CONVIENTE"

    def test_prezzo_pareggio_identita(self):
        # Il pareggio del brief e' definito a
        # totale lance invariato: al prezzo di
        # pareggio il totale fan (energia fan
        # al pareggio + acqua + O&M fan + CO2
        # fan) eguaglia il totale lance della
        # demo, 264.406,25 EUR/anno. Non e'
        # un punto di pareggio a prezzo
        # uniforme: lo stesso prezzo si
        # applica anche alle lance (vedi
        # test_prezzo_elettrico_700_conviente).
        assert PAR_DEMO * EF_MWH_DEMO + C_ACQUA_DEMO + 18000 + \
            CC_FAN_DEMO == pytest.approx(TL_DEMO, rel=REL)

    def test_prezzo_fan_40000_non_conviente(self):
        # Prezzo cannone 40000 EUR: CAPEX delta
        # 1.460.000 EUR, VAN circa -271.556,89
        # EUR, oltre la tolleranza del 10 %
        # del delta (146.000 EUR) ->
        # NON_CONVIENTE.
        n = self._bc(prezzo_fan_EUR=40000.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            1460000.0, rel=REL)
        assert abs(n["van"] + 271556.89) <= 1.0
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_prezzo_fan_35400_marginale(self):
        # Prezzo cannone 35400 EUR: CAPEX delta
        # 1.230.000 EUR, VAN circa -41.556,89
        # EUR, entro la tolleranza del 10 %
        # del delta (123.000 EUR) ->
        # MARGINALE.
        n = self._bc(prezzo_fan_EUR=35400.0)
        assert n["valid"] is True
        assert abs(n["van"] + 41556.89) <= 1.0
        assert n["verdetto"] == "MARGINALE"

    def test_prezzo_eua_zero_conviente(self):
        # Prezzo EUA 0: totali senza CO2,
        # fan 165.600 EUR (64.800 + 82.800 +
        # 18.000) e lance 255.800 EUR
        # (162.000 + 82.800 + 11.000),
        # risparmio 90.200 EUR/anno, VAN
        # circa +414.091,37 EUR -> CONVIENTE.
        n = self._bc(prezzo_eua_eur_t=0.0)
        assert n["valid"] is True
        assert n["risparmio_eur_anno"] == pytest.approx(
            90200.0, rel=REL)
        assert abs(n["van"] - 414091.37) <= 1.0
        assert n["verdetto"] == "CONVIENTE"

    def test_wacc_zero_valido_crf_uno_su_n(self):
        n = self._bc(wacc_pct=0.0)
        assert n["valid"] is True
        assert n["crf"] == pytest.approx(
            1.0 / 20.0, rel=REL)
        assert n["van"] == pytest.approx(
            1197275.0, rel=REL)

    def test_area_zero_neutro(self):
        n = self._bc(area_ha=0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_profondita_zero_neutro(self):
        n = self._bc(profondita_m=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_densita_zero_neutro(self):
        n = self._bc(densita_neve_kg_m3=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_consumo_fan_zero_neutro(self):
        n = self._bc(consumo_fan_kWh_m3=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_consumo_lance_zero_neutro(self):
        n = self._bc(consumo_lance_kWh_m3=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_capex_delta_zero_neutro(self):
        # Prezzo cannone 10800 EUR: CAPEX fan
        # 540.000 EUR = CAPEX lance, delta 0.
        n = self._bc(prezzo_fan_EUR=10800.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_capex_delta_negativo_n_fan_zero_neutro(self):
        n = self._bc(n_fan=0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_capex_delta_negativo_prezzo_lance_alto_neutro(self):
        n = self._bc(prezzo_lance_EUR=20000.0)
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

    def test_perdite_oltre_100_neutro(self):
        n = self._bc(perdite_pct=100.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(area_ha=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_anno"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(area_ha=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(vita_anni=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_stringa_neutro(self):
        n = self._bc(area_ha="30")
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzo_negativo_neutro(self):
        n = self._bc(prezzo_el_EUR_MWh=-1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh744_neutro"]()
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
        n = _F["_mh744_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "area_ha",
                       "profondita_m",
                       "densita_neve_kg_m3",
                       "perdite_pct",
                       "consumo_fan_kWh_m3",
                       "consumo_lance_kWh_m3",
                       "prezzo_el_EUR_MWh",
                       "prezzo_acqua_EUR_m3",
                       "om_fan_eur_anno",
                       "om_lance_eur_anno",
                       "n_fan", "n_lance",
                       "prezzo_fan_EUR",
                       "prezzo_lance_EUR",
                       "fattore_rete_kg_MWh",
                       "prezzo_eua_eur_t",
                       "wacc_pct", "vita_anni",
                       "tolleranza_pct",
                       "volume_neve_m3",
                       "acqua_m3",
                       "energia_fan_kwh",
                       "energia_fan_MWh",
                       "energia_lance_kwh",
                       "energia_lance_MWh",
                       "co2_fan_t", "co2_lance_t",
                       "co2_risparmiata_t",
                       "costo_energia_fan_eur",
                       "costo_energia_lance_eur",
                       "costo_acqua_eur",
                       "costo_co2_fan_eur",
                       "costo_co2_lance_eur",
                       "totale_fan_eur",
                       "totale_lance_eur",
                       "risparmio_eur_anno",
                       "risparmio_eur_m3",
                       "costo_per_m3_fan_eur",
                       "costo_per_m3_lance_eur",
                       "capex_fan_eur",
                       "capex_lance_eur",
                       "capex_delta_eur",
                       "crf", "quota_capex_eur",
                       "costo_livellato_alt_eur",
                       "costo_livellato_eur_m3",
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
        assert len(b["df_tabella"]) == 51
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Volume neve (m3)" in voci
        assert "Acqua (m3)" in voci
        assert "Energia fan (MWh)" in voci
        assert "Energia lance (MWh)" in voci
        assert "CO2 fan (tCO2)" in voci
        assert "CO2 lance (tCO2)" in voci
        assert "CO2 risparmiata (tCO2)" in voci
        assert "Costo totale fan (EUR/anno)" in voci
        assert "Costo totale lance (EUR/anno)" in voci
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
            pytest.approx(-DELTA_DEMO, rel=REL)
        assert b["df_flussi"]["Flusso (EUR/anno)"].iloc[1] == \
            pytest.approx(RISP_DEMO, rel=REL)


class TestCsv:
    def _ing(self):
        return _F["mh744_demo"]()

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh744_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") == 52
        assert len(txt.strip().splitlines()) == 52

    def test_csv_contiene_verdetti_e_costi(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh744_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "capex_delta_eur" in txt
        assert "van_eur" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "prezzo_pareggio_eur_MWh" in txt
        assert "risparmio_eur_anno" in txt
        assert "totale_lance_eur" in txt
        assert "volume_neve_m3" in txt
        assert "co2_risparmiata_t" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh744_csv"](bc, self._ing())
        assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in txt
        assert f"co2_risparmiata_t;{bc['co2_risparmiata_t']}" in txt
        assert "area_ha;30" in txt
        assert "prezzo_el_EUR_MWh;240" in txt
        assert f"costo_livellato_eur_m3;{bc['costo_livellato_eur_m3']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def744["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def744\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 19, ui_keys
        demo_keys = set(_F["mh744_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh744_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh744_demo():")
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
        ui_keys = set(re.findall(r'_def744\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W745 (27/10/2026) - tab744' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh744_num", "mh744_nneg", "mh744_pos",
                     "mh744_int_pos", "mh744_int_nneg",
                     "mh744_pct_0_100", "mh744_pct_wacc",
                     "mh744_volume_neve", "mh744_acqua_m3",
                     "mh744_energia_kwh", "mh744_energia_MWh",
                     "mh744_co2", "mh744_costo_energia",
                     "mh744_costo_acqua", "mh744_costo_co2",
                     "mh744_costo_totale", "mh744_risparmio",
                     "mh744_risparmio_per_m3",
                     "mh744_costo_per_m3",
                     "mh744_capex", "mh744_capex_delta",
                     "mh744_crf", "mh744_quota_capex",
                     "mh744_costo_livellato",
                     "mh744_prezzo_pareggio",
                     "mh744_flussi", "mh744_van",
                     "mh744_tir", "mh744_payback",
                     "mh744_verdetto", "mh744_valida",
                     "_mh744_neutro",
                     "mh744_calcola", "mh744_csv",
                     "mh744_demo", "demo_calcoli"):
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
        mh_old = "mh" + "743"
        st_old = "st" + "743"
        tab_old = "tab" + "743"
        w_old = "W" + "744"
        assert mh_old not in _helpers_src()
        assert mh_old not in _ui_src()
        assert st_old not in _ui_src()
        assert tab_old not in _ui_src()
        assert w_old not in _helpers_src()
        assert w_old not in _ui_src()
        assert "mh744" in _helpers_src()
        assert "st744" in _ui_src()

    def test_helpers_parse_ast(self):
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w745_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE744) == 1

    def test_blocco_with_tab744(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab744:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE744

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st744_[A-Za-z0-9_]+)"', _ui_src())
        assert len(keys) == 27, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st744_") for k in keys)

    def test_chiavi_st_input_presenti(self):
        keys = re.findall(r'key="(st744_[A-Za-z0-9_]+)"', _ui_src())
        attese = ["st744_area", "st744_profondita",
                  "st744_densita", "st744_perdite",
                  "st744_consumo_fan", "st744_consumo_lance",
                  "st744_prezzo_el", "st744_prezzo_acqua",
                  "st744_fattore_rete", "st744_eua",
                  "st744_om_fan", "st744_om_lance",
                  "st744_n_fan", "st744_prezzo_fan",
                  "st744_n_lance", "st744_prezzo_lance",
                  "st744_wacc", "st744_vita", "st744_tolleranza",
                  "st744_grafico", "st744_show_flussi",
                  "st744_show_tabella", "st744_nota",
                  "st744_ipotesi", "st744_calcola",
                  "st744_csv", "st744_csv_flussi"]
        assert len(attese) == 27
        for k in attese:
            assert k in keys, k

    def test_chiavi_st_niente_fstring_dinamiche(self):
        src = _ui_src()
        assert 'key=f"' not in src
        assert "key=f'" not in src

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg744" in src
        assert "NON_CALCOLABILE" in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg744") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg744")
        assert g < src.index("st.bar_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Risparmio (EUR/anno)" in src
        assert "VAN (kEUR)" in src
        assert "CO2 risparmiata (t/anno)" in src
        assert "Costo livellato alternativo (EUR/m3)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON_CALCOLABILE"):
            assert v in src

    def test_distinzioni_presenti(self):
        src = _ui_src()
        assert "innevamento" in src
        assert "scioglimento nivale" in src
        assert "albedo" in src

    def test_distinzioni_in_header_helpers(self):
        src = _helpers_src()
        assert "innevamento" in src
        assert "scioglimento nivale" in src
        assert "albedo" in src

    def test_nota_didattica_presente(self):
        src = _ui_src()
        assert "NOTA DIDATTICA" in src
        assert "150.000" in src
        assert "69.000" in src

    def test_grafico_bar_chart_presente(self):
        src = _ui_src()
        assert "st.bar_chart" in src
        assert "_dati744" in src
        assert '"EUR/anno"' in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh744_csv" in src
        assert "innevamento_cannoni.csv" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st744_show_flussi" in src
        assert "st.checkbox" in src

    def test_niente_nome(self):
        assert "Emanuele" not in _helpers_src()
        assert "Emanuele" not in _ui_src()

    def test_ancora_helper_presente(self):
        assert "# W745 (27/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab744:")
