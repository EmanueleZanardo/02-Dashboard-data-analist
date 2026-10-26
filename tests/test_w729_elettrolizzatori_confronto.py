"""Test tab729 "⚗️ Elettrolizzatori a confronto: alcalino vs PEM vs SOEC — quale tecnologia paga?"

Nuova tab tab729 (elettrolizzatori a confronto,
w730). Business case di un elettrolizzatore
che produce idrogeno verde: tre tecnologie
(alcalino, PEM, SOEC) con la STESSA potenza,
le STESSE ore equivalenti/anno, lo STESSO
prezzo dell'elettricita' e lo STESSO prezzo
di vendita dell'H2; ogni tecnologia ha il
suo consumo specifico (kWh/kg), il suo
CAPEX (EUR/kW) e il suo O&M (EUR/kW/anno).
VAN, TIR, payback, LCOH, verdetto per
tecnologia, migliore per LCOH minimo e
delta LCOH.

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
potenza 10 MW; ore equivalenti 5000
ore/anno; prezzo elettricita' 70 EUR/MWh;
prezzo H2 5 EUR/kg; WACC 0,06 (6 %); vita
20 anni; tolleranza 0,10 (10 % del CAPEX);
alcalino: consumo 50 kWh/kg, CAPEX 800
EUR/kW, O&M 20 EUR/kW/anno; PEM: consumo
55 kWh/kg, CAPEX 1200 EUR/kW, O&M 25
EUR/kW/anno; SOEC: consumo 40 kWh/kg,
CAPEX 1800 EUR/kW, O&M 30 EUR/kW/anno.

- e_kwh_anno = 50000000.0
- costo_el_eur_anno = 3500000.0
- h2_alk_kg_anno = 1000000.0
- ricavo_alk_eur_anno = 5000000.0
- om_alk_eur_anno = 200000.0
- capex_alk_eur = 8000000.0
- netto_alk_eur_anno = 1300000.0
- van_alk = 6910897.584134827
- tir_alk = 15.309000968748304
- payback_alk = 7
- lcoh_alk_eur_kg = 4.1
- verdetto_alk = 'CONVIENTE'
- delta_lcoh_alk_eur_kg = 0.33999999999999986
- h2_pem_kg_anno = 909090.9090909091
- ricavo_pem_eur_anno = 4545454.545454545
- om_pem_eur_anno = 250000.0
- capex_pem_eur = 12000000.0
- netto_pem_eur_anno = 795454.545454545
- van_pem = -2876199.0306867384
- tir_pem = 2.8501414839757286
- payback_pem = 16
- lcoh_pem_eur_kg = 4.785
- verdetto_pem = 'NON_CONVIENTE'
- delta_lcoh_pem_eur_kg = 1.0250000000000004
- h2_soec_kg_anno = 1250000.0
- ricavo_soec_eur_anno = 6250000.0
- om_soec_eur_anno = 300000.0
- capex_soec_eur = 18000000.0
- netto_soec_eur_anno = 2450000.0
- van_soec = 10101306.985484866
- tir_soec = 12.26530552322236
- payback_soec = 8
- lcoh_soec_eur_kg = 3.76
- verdetto_soec = 'CONVIENTE'
- delta_lcoh_soec_eur_kg = 0.0
- migliore = 'soec'
- lcoh_migliore_eur_kg = 3.76
- van_migliore_eur = 10101306.985484866

Scomposizione: E 10 x 1000 x 5000 =
50000000,0 kWh/anno; costo elettricita'
50000000,0 / 1000 x 70 = 3500000,0
EUR/anno; H2 alcalino 50000000,0 / 50 =
1000000,0 kg/anno; ricavo alcalino
1000000,0 x 5 = 5000000,0 EUR/anno; O&M
alcalino 10 x 1000 x 20 = 200000,0
EUR/anno; netto alcalino 5000000,0 -
3500000,0 - 200000,0 = 1300000,0 EUR/anno;
CAPEX alcalino 10 x 1000 x 800 =
8000000,0 EUR; flussi alcalino: anno 0
-8000000,0, anni 1-20 netto 1300000,0
(piatti); VAN alcalino -8000000,0 +
1300000,0 x 11,469921218565263 (annuita'
20 anni al 6 %) = 6910897,584134827 EUR;
TIR alcalino 15,309000968748304 % (il
tasso che azzera il VAN dei flussi
alcalino); payback alcalino 7 (il cumulato
supera lo zero al settimo anno: -8000000,0
+ 7 x 1300000,0 = 1100000,0); LCOH
alcalino (8000000,0 / 20 + 200000,0 +
3500000,0) / 1000000,0 = 4,1 EUR/kg; H2
PEM 50000000,0 / 55 = 909090,9090909091
kg/anno; ricavo PEM 909090,9090909091 x 5
= 4545454,545454545 EUR/anno; O&M PEM 10
x 1000 x 25 = 250000,0 EUR/anno; netto PEM
4545454,545454545 - 3500000,0 - 250000,0
= 795454,545454545 EUR/anno; CAPEX PEM 10
x 1000 x 1200 = 12000000,0 EUR; VAN PEM
-12000000,0 + 795454,545454545 x
11,469921218565263 = -2876199,030686737
EUR; TIR PEM 2,8501414839757286 %;
payback PEM 16 (-12000000,0 + 16 x
795454,545454545 = 727272,727272727);
LCOH PEM (12000000,0 / 20 + 250000,0 +
3500000,0) / 909090,9090909091 = 4,785
EUR/kg; verdetto PEM NON_CONVIENTE
perche' VAN PEM < 0 e |VAN| 2876199,03 >
tolleranza 0,10 x 12000000,0 =
1200000,0 EUR; H2 SOEC 50000000,0 / 40 =
1250000,0 kg/anno; ricavo SOEC 1250000,0
x 5 = 6250000,0 EUR/anno; O&M SOEC 10 x
1000 x 30 = 300000,0 EUR/anno; netto SOEC
6250000,0 - 3500000,0 - 300000,0 =
2450000,0 EUR/anno; CAPEX SOEC 10 x 1000
x 1800 = 18000000,0 EUR; VAN SOEC
-18000000,0 + 2450000,0 x 11,469921218565263
= 10101306,985484866 EUR; TIR SOEC
12,26530552322236 %; payback SOEC 8
(-18000000,0 + 8 x 2450000,0 = 1600000,0);
LCOH SOEC (18000000,0 / 20 + 300000,0 +
3500000,0) / 1250000,0 = 3,76 EUR/kg;
migliore SOEC per LCOH minimo (3,76 <
4,1 < 4,785); delta LCOH alcalino 4,1 -
3,76 = 0,34 EUR/kg, PEM 4,785 - 3,76 =
1,025 EUR/kg, SOEC 0,0 EUR/kg.
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
    if (p / "w730_helpers.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w730_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w730_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w730_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w730_helpers.py: {missing}")
    return out


_F = _load("mh729_num", "mh729_nneg", "mh729_pos",
           "mh729_int_pos", "mh729_frac_01",
           "mh729_frac_toll",
           "mh729_e_kwh", "mh729_h2", "mh729_costo_el",
           "mh729_ricavo", "mh729_om", "mh729_capex",
           "mh729_netto", "mh729_flussi",
           "mh729_van", "mh729_tir", "mh729_payback",
           "mh729_lcoh", "mh729_verdetto",
           "mh729_tecnologia", "mh729_valida",
           "_mh729_neutro", "mh729_calcola",
           "mh729_confronto", "mh729_csv",
           "mh729_demo", "demo_calcoli")

TITLE729 = ("⚗️ Elettrolizzatori a confronto: alcalino "
            "vs PEM vs SOEC — quale tecnologia paga?")

E_DEMO = 50000000.0
COSTO_EL_DEMO = 3500000.0
H2_ALK_DEMO = 1000000.0
RIC_ALK_DEMO = 5000000.0
OM_ALK_DEMO = 200000.0
CAPEX_ALK_DEMO = 8000000.0
NETTO_ALK_DEMO = 1300000.0
VAN_ALK_DEMO = 6910897.584134827
TIR_ALK_DEMO = 15.309000968748304
PAYBACK_ALK_DEMO = 7
LCOH_ALK_DEMO = 4.1
VERDETTO_ALK_DEMO = "CONVIENTE"
DELTA_ALK_DEMO = 0.33999999999999986
H2_PEM_DEMO = 909090.9090909091
RIC_PEM_DEMO = 4545454.545454545
OM_PEM_DEMO = 250000.0
CAPEX_PEM_DEMO = 12000000.0
NETTO_PEM_DEMO = 795454.545454545
VAN_PEM_DEMO = -2876199.0306867384
TIR_PEM_DEMO = 2.8501414839757286
PAYBACK_PEM_DEMO = 16
LCOH_PEM_DEMO = 4.785
VERDETTO_PEM_DEMO = "NON_CONVIENTE"
DELTA_PEM_DEMO = 1.0250000000000004
H2_SOEC_DEMO = 1250000.0
RIC_SOEC_DEMO = 6250000.0
OM_SOEC_DEMO = 300000.0
CAPEX_SOEC_DEMO = 18000000.0
NETTO_SOEC_DEMO = 2450000.0
VAN_SOEC_DEMO = 10101306.985484866
TIR_SOEC_DEMO = 12.26530552322236
PAYBACK_SOEC_DEMO = 8
LCOH_SOEC_DEMO = 3.76
VERDETTO_SOEC_DEMO = "CONVIENTE"
DELTA_SOEC_DEMO = 0.0
MIGLIORE_DEMO = "soec"

_DEMO = {
    "potenza_mw": 10.0,
    "ore_anno": 5000,
    "prezzo_el_eur_mwh": 70.0,
    "prezzo_h2_eur_kg": 5.0,
    "wacc_frac": 0.06,
    "vita_anni": 20,
    "tolleranza_frac": 0.10,
    "consumo_alk_kwh_kg": 50.0,
    "capex_alk_eur_kw": 800.0,
    "om_alk_eur_kw_anno": 20.0,
    "consumo_pem_kwh_kg": 55.0,
    "capex_pem_eur_kw": 1200.0,
    "om_pem_eur_kw_anno": 25.0,
    "consumo_soec_kwh_kg": 40.0,
    "capex_soec_eur_kw": 1800.0,
    "om_soec_eur_kw_anno": 30.0,
}

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w730_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w730_ui.py").read_text(encoding="utf-8")


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh729_demo"]()
        d.update(kw)
        return _F["mh729_valida"](**d)

    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh729_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh729_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh729_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh729_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh729_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh729_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh729_pos"](0.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh729_int_pos"](2.5, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh729_int_pos"](20.0, "x") == 20

    def test_frac_01_rifiuta_zero_e_uno(self):
        with pytest.raises(ValueError):
            _F["mh729_frac_01"](0.0, "x")
        with pytest.raises(ValueError):
            _F["mh729_frac_01"](1.0, "x")

    def test_frac_toll_accetta_zero_rifiuta_uno(self):
        assert _F["mh729_frac_toll"](0.0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh729_frac_toll"](1.0, "x")
        with pytest.raises(ValueError):
            _F["mh729_frac_toll"](-0.01, "x")

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_potenza_zero_non_valida(self):
        assert self._val(potenza_mw=0.0)["valido"] is False

    def test_ore_zero_e_frazione_non_valide(self):
        assert self._val(ore_anno=0)["valido"] is False
        assert self._val(ore_anno=5000.5)["valido"] is False

    def test_consumi_zero_non_validi(self):
        for k in ("consumo_alk_kwh_kg", "consumo_pem_kwh_kg",
                  "consumo_soec_kwh_kg"):
            assert self._val(**{k: 0.0})["valido"] is False, k

    def test_negativi_non_validi(self):
        for k in ("prezzo_el_eur_mwh", "prezzo_h2_eur_kg",
                  "capex_alk_eur_kw", "om_alk_eur_kw_anno",
                  "capex_pem_eur_kw", "om_pem_eur_kw_anno",
                  "capex_soec_eur_kw", "om_soec_eur_kw_anno"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_vita_zero_e_frazione_non_valide(self):
        assert self._val(vita_anni=0)["valido"] is False
        assert self._val(vita_anni=20.5)["valido"] is False

    def test_wacc_zero_e_uno_non_validi(self):
        assert self._val(wacc_frac=0.0)["valido"] is False
        assert self._val(wacc_frac=1.0)["valido"] is False
        assert self._val(wacc_frac=0.06)["valido"] is True

    def test_tolleranza_uno_non_valida_zero_valida(self):
        assert self._val(tolleranza_frac=1.0)["valido"] is False
        assert self._val(tolleranza_frac=0.0)["valido"] is True

    def test_nan_non_valido(self):
        assert self._val(potenza_mw=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(potenza_mw=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(vita_anni=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(potenza_mw="10")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(prezzo_el_eur_mwh=0.0)["valido"] is True
        assert self._val(prezzo_h2_eur_kg=0.0)["valido"] is True
        assert self._val(capex_alk_eur_kw=0.0)["valido"] is True
        assert self._val(tolleranza_frac=0.0)["valido"] is True


class TestFunzioni:
    def test_e_kwh_demo(self):
        assert _F["mh729_e_kwh"](
            10.0, 5000) == pytest.approx(E_DEMO, rel=REL)

    def test_h2_alk_demo(self):
        assert _F["mh729_h2"](
            E_DEMO, 50.0) == pytest.approx(H2_ALK_DEMO, rel=REL)

    def test_h2_pem_demo(self):
        assert _F["mh729_h2"](
            E_DEMO, 55.0) == pytest.approx(H2_PEM_DEMO, rel=REL)

    def test_h2_soec_demo(self):
        assert _F["mh729_h2"](
            E_DEMO, 40.0) == pytest.approx(H2_SOEC_DEMO, rel=REL)

    def test_costo_el_demo(self):
        assert _F["mh729_costo_el"](
            E_DEMO, 70.0) == pytest.approx(
            COSTO_EL_DEMO, rel=REL)

    def test_ricavo_alk_demo(self):
        assert _F["mh729_ricavo"](
            H2_ALK_DEMO, 5.0) == pytest.approx(
            RIC_ALK_DEMO, rel=REL)

    def test_ricavo_pem_demo(self):
        assert _F["mh729_ricavo"](
            H2_PEM_DEMO, 5.0) == pytest.approx(
            RIC_PEM_DEMO, rel=REL)

    def test_om_alk_demo(self):
        assert _F["mh729_om"](
            10.0, 20.0) == pytest.approx(OM_ALK_DEMO, rel=REL)

    def test_om_pem_demo(self):
        assert _F["mh729_om"](
            10.0, 25.0) == pytest.approx(OM_PEM_DEMO, rel=REL)

    def test_om_soec_demo(self):
        assert _F["mh729_om"](
            10.0, 30.0) == pytest.approx(OM_SOEC_DEMO, rel=REL)

    def test_capex_alk_demo(self):
        assert _F["mh729_capex"](
            10.0, 800.0) == pytest.approx(
            CAPEX_ALK_DEMO, rel=REL)

    def test_capex_pem_demo(self):
        assert _F["mh729_capex"](
            10.0, 1200.0) == pytest.approx(
            CAPEX_PEM_DEMO, rel=REL)

    def test_capex_soec_demo(self):
        assert _F["mh729_capex"](
            10.0, 1800.0) == pytest.approx(
            CAPEX_SOEC_DEMO, rel=REL)

    def test_netto_alk_demo(self):
        assert _F["mh729_netto"](
            RIC_ALK_DEMO, COSTO_EL_DEMO,
            OM_ALK_DEMO) == pytest.approx(
            NETTO_ALK_DEMO, rel=REL)

    def test_netto_pem_demo(self):
        assert _F["mh729_netto"](
            RIC_PEM_DEMO, COSTO_EL_DEMO,
            OM_PEM_DEMO) == pytest.approx(
            NETTO_PEM_DEMO, rel=REL)

    def test_netto_soec_demo(self):
        assert _F["mh729_netto"](
            RIC_SOEC_DEMO, COSTO_EL_DEMO,
            OM_SOEC_DEMO) == pytest.approx(
            NETTO_SOEC_DEMO, rel=REL)

    def test_netto_puo_essere_negativo(self):
        assert _F["mh729_netto"](
            1000000.0, 3500000.0, 200000.0) == pytest.approx(
            -2700000.0, rel=REL)

    def test_flussi_demo(self):
        flussi = _F["mh729_flussi"](CAPEX_ALK_DEMO,
                                     NETTO_ALK_DEMO, 20)
        assert len(flussi) == 21
        assert flussi[0] == pytest.approx(-CAPEX_ALK_DEMO, rel=REL)
        assert all(f == pytest.approx(NETTO_ALK_DEMO, rel=REL)
                   for f in flussi[1:])

    def test_van_demo_alk(self):
        flussi = _F["mh729_flussi"](CAPEX_ALK_DEMO,
                                     NETTO_ALK_DEMO, 20)
        assert abs(_F["mh729_van"](
            flussi, 0.06) - VAN_ALK_DEMO) <= 1.0

    def test_van_demo_pem(self):
        flussi = _F["mh729_flussi"](CAPEX_PEM_DEMO,
                                     NETTO_PEM_DEMO, 20)
        assert abs(_F["mh729_van"](
            flussi, 0.06) - VAN_PEM_DEMO) <= 1.0

    def test_van_demo_soec(self):
        flussi = _F["mh729_flussi"](CAPEX_SOEC_DEMO,
                                     NETTO_SOEC_DEMO, 20)
        assert abs(_F["mh729_van"](
            flussi, 0.06) - VAN_SOEC_DEMO) <= 1.0

    def test_van_tasso_zero(self):
        flussi = _F["mh729_flussi"](CAPEX_ALK_DEMO,
                                     NETTO_ALK_DEMO, 20)
        atteso = -CAPEX_ALK_DEMO + NETTO_ALK_DEMO * 20
        assert _F["mh729_van"](
            flussi, 0.0) == pytest.approx(atteso, rel=1e-12)

    def test_van_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh729_van"]([100.0, 100.0], -0.01)

    def test_tir_none_flussi_tutti_negativi(self):
        flussi = _F["mh729_flussi"](CAPEX_ALK_DEMO,
                                     -1000.0, 20)
        assert _F["mh729_tir"](flussi) is None

    def test_tir_none_tutti_flussi_non_negativi(self):
        assert _F["mh729_tir"](
            [0.0] + [NETTO_ALK_DEMO] * 20) is None

    def test_tir_none_nessun_cambio_segno_negativo(self):
        assert _F["mh729_tir"](
            [-1000.0] + [-100.0] * 10) is None

    def test_tir_esiste_caso_semplice_100_120(self):
        assert _F["mh729_tir"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_caso_semplice_1000_500_500_zero(self):
        assert abs(_F["mh729_tir"](
            [-1000.0, 500.0, 500.0])) <= 1e-9

    def test_tir_alk_demo(self):
        flussi = _F["mh729_flussi"](CAPEX_ALK_DEMO,
                                     NETTO_ALK_DEMO, 20)
        tir = _F["mh729_tir"](flussi)
        assert tir is not None
        assert tir * 100.0 == pytest.approx(TIR_ALK_DEMO, rel=1e-9)

    def test_tir_pem_demo(self):
        flussi = _F["mh729_flussi"](CAPEX_PEM_DEMO,
                                     NETTO_PEM_DEMO, 20)
        tir = _F["mh729_tir"](flussi)
        assert tir is not None
        assert tir * 100.0 == pytest.approx(TIR_PEM_DEMO, rel=1e-9)

    def test_tir_soec_demo(self):
        flussi = _F["mh729_flussi"](CAPEX_SOEC_DEMO,
                                     NETTO_SOEC_DEMO, 20)
        tir = _F["mh729_tir"](flussi)
        assert tir is not None
        assert tir * 100.0 == pytest.approx(TIR_SOEC_DEMO, rel=1e-9)

    def test_payback_alk_demo(self):
        flussi = _F["mh729_flussi"](CAPEX_ALK_DEMO,
                                     NETTO_ALK_DEMO, 20)
        assert _F["mh729_payback"](flussi) == PAYBACK_ALK_DEMO

    def test_payback_pem_demo(self):
        flussi = _F["mh729_flussi"](CAPEX_PEM_DEMO,
                                     NETTO_PEM_DEMO, 20)
        assert _F["mh729_payback"](flussi) == PAYBACK_PEM_DEMO

    def test_payback_soec_demo(self):
        flussi = _F["mh729_flussi"](CAPEX_SOEC_DEMO,
                                     NETTO_SOEC_DEMO, 20)
        assert _F["mh729_payback"](flussi) == PAYBACK_SOEC_DEMO

    def test_payback_semplice_due(self):
        assert _F["mh729_payback"](
            [-1000.0, 500.0, 500.0, 500.0]) == 2

    def test_payback_zero_se_cumulato_anno_zero_non_negativo(self):
        assert _F["mh729_payback"](
            [0.0, 100.0]) == 0

    def test_payback_none_se_mai(self):
        assert _F["mh729_payback"](
            [-100000000.0] + [NETTO_PEM_DEMO] * 20) is None

    def test_lcoh_alk_demo(self):
        assert _F["mh729_lcoh"](
            CAPEX_ALK_DEMO, 20, OM_ALK_DEMO,
            COSTO_EL_DEMO, H2_ALK_DEMO) == pytest.approx(
            LCOH_ALK_DEMO, rel=REL)

    def test_lcoh_pem_demo(self):
        assert _F["mh729_lcoh"](
            CAPEX_PEM_DEMO, 20, OM_PEM_DEMO,
            COSTO_EL_DEMO, H2_PEM_DEMO) == pytest.approx(
            LCOH_PEM_DEMO, rel=REL)

    def test_lcoh_soec_demo(self):
        assert _F["mh729_lcoh"](
            CAPEX_SOEC_DEMO, 20, OM_SOEC_DEMO,
            COSTO_EL_DEMO, H2_SOEC_DEMO) == pytest.approx(
            LCOH_SOEC_DEMO, rel=REL)

    def test_lcoh_none_se_h2_zero(self):
        assert _F["mh729_lcoh"](
            1000.0, 10, 100.0, 50.0, 0.0) is None

    def test_lcoh_formula_indipendente(self):
        assert _F["mh729_lcoh"](
            120000.0, 10, 5000.0, 10000.0,
            100000.0) == pytest.approx(
            (12000.0 + 5000.0 + 10000.0) / 100000.0, rel=REL)

    def test_verdetto_demo(self):
        assert _F["mh729_verdetto"](
            VAN_ALK_DEMO, CAPEX_ALK_DEMO, 0.10,
            H2_ALK_DEMO, NETTO_ALK_DEMO) == VERDETTO_ALK_DEMO
        assert _F["mh729_verdetto"](
            VAN_PEM_DEMO, CAPEX_PEM_DEMO, 0.10,
            H2_PEM_DEMO, NETTO_PEM_DEMO) == VERDETTO_PEM_DEMO
        assert _F["mh729_verdetto"](
            VAN_SOEC_DEMO, CAPEX_SOEC_DEMO, 0.10,
            H2_SOEC_DEMO, NETTO_SOEC_DEMO) == VERDETTO_SOEC_DEMO

    def test_verdetto_conviente_van_positivo(self):
        assert _F["mh729_verdetto"](
            1000.0, CAPEX_ALK_DEMO, 0.10,
            H2_ALK_DEMO, NETTO_ALK_DEMO) == "CONVIENTE"

    def test_verdetto_van_zero_marginale(self):
        assert _F["mh729_verdetto"](
            0.0, CAPEX_ALK_DEMO, 0.10,
            H2_ALK_DEMO, NETTO_ALK_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh729_verdetto"](
            -0.10 * CAPEX_ALK_DEMO, CAPEX_ALK_DEMO, 0.10,
            H2_ALK_DEMO, NETTO_ALK_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_oltre_limite(self):
        assert _F["mh729_verdetto"](
            -0.10 * CAPEX_ALK_DEMO - 1.0, CAPEX_ALK_DEMO, 0.10,
            H2_ALK_DEMO, NETTO_ALK_DEMO) == "NON_CONVIENTE"

    def test_verdetto_netto_negativo_non_e_non_calcolabile(self):
        # Netto negativo ma VAN calcolabile: il
        # verdetto segue la regola VAN/tolleranza.
        assert _F["mh729_verdetto"](
            -1000.0, CAPEX_ALK_DEMO, 0.10,
            H2_ALK_DEMO, -5000.0) == "MARGINALE"

    def test_verdetto_non_calcolabile_h2_zero(self):
        assert _F["mh729_verdetto"](
            1000.0, CAPEX_ALK_DEMO, 0.10, 0.0,
            NETTO_ALK_DEMO) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_netto_nan(self):
        assert _F["mh729_verdetto"](
            1000.0, CAPEX_ALK_DEMO, 0.10, H2_ALK_DEMO,
            float("nan")) == "NON_CALCOLABILE"

    def test_tecnologia_alk_demo(self):
        r = _F["mh729_tecnologia"](
            E_DEMO, COSTO_EL_DEMO, 50.0, 800.0, 20.0,
            10.0, 5.0, 20, 0.06)
        assert r["h2_kg_anno"] == pytest.approx(
            H2_ALK_DEMO, rel=REL)
        assert r["ricavo_eur_anno"] == pytest.approx(
            RIC_ALK_DEMO, rel=REL)
        assert r["om_eur_anno"] == pytest.approx(
            OM_ALK_DEMO, rel=REL)
        assert r["capex_eur"] == pytest.approx(
            CAPEX_ALK_DEMO, rel=REL)
        assert r["netto_eur_anno"] == pytest.approx(
            NETTO_ALK_DEMO, rel=REL)
        assert abs(r["van"] - VAN_ALK_DEMO) <= 1.0
        assert r["tir"] * 100.0 == pytest.approx(
            TIR_ALK_DEMO, rel=1e-9)
        assert r["payback"] == PAYBACK_ALK_DEMO
        assert r["lcoh_eur_kg"] == pytest.approx(
            LCOH_ALK_DEMO, rel=REL)

    def test_tecnologia_pem_demo(self):
        r = _F["mh729_tecnologia"](
            E_DEMO, COSTO_EL_DEMO, 55.0, 1200.0, 25.0,
            10.0, 5.0, 20, 0.06)
        assert r["h2_kg_anno"] == pytest.approx(
            H2_PEM_DEMO, rel=REL)
        assert r["capex_eur"] == pytest.approx(
            CAPEX_PEM_DEMO, rel=REL)
        assert abs(r["van"] - VAN_PEM_DEMO) <= 1.0
        assert r["tir"] * 100.0 == pytest.approx(
            TIR_PEM_DEMO, rel=1e-9)
        assert r["payback"] == PAYBACK_PEM_DEMO

    def test_tecnologia_soec_demo(self):
        r = _F["mh729_tecnologia"](
            E_DEMO, COSTO_EL_DEMO, 40.0, 1800.0, 30.0,
            10.0, 5.0, 20, 0.06)
        assert r["h2_kg_anno"] == pytest.approx(
            H2_SOEC_DEMO, rel=REL)
        assert r["capex_eur"] == pytest.approx(
            CAPEX_SOEC_DEMO, rel=REL)
        assert abs(r["van"] - VAN_SOEC_DEMO) <= 1.0
        assert r["tir"] * 100.0 == pytest.approx(
            TIR_SOEC_DEMO, rel=1e-9)
        assert r["payback"] == PAYBACK_SOEC_DEMO

    def test_confronto_demo(self):
        ralk = _F["mh729_tecnologia"](
            E_DEMO, COSTO_EL_DEMO, 50.0, 800.0, 20.0,
            10.0, 5.0, 20, 0.06)
        rpem = _F["mh729_tecnologia"](
            E_DEMO, COSTO_EL_DEMO, 55.0, 1200.0, 25.0,
            10.0, 5.0, 20, 0.06)
        rsoec = _F["mh729_tecnologia"](
            E_DEMO, COSTO_EL_DEMO, 40.0, 1800.0, 30.0,
            10.0, 5.0, 20, 0.06)
        df = _F["mh729_confronto"](ralk, rpem, rsoec)
        assert list(df.columns) == ["Voce", "Alcalino",
                                    "PEM", "SOEC"]
        assert len(df) == 7
        riga = df[df["Voce"] == "CAPEX (EUR)"].iloc[0]
        assert riga["Alcalino"] == pytest.approx(
            CAPEX_ALK_DEMO, rel=REL)
        assert riga["PEM"] == pytest.approx(
            CAPEX_PEM_DEMO, rel=REL)
        assert riga["SOEC"] == pytest.approx(
            CAPEX_SOEC_DEMO, rel=REL)
        riga_van = df[df["Voce"] == "VAN (EUR)"].iloc[0]
        assert riga_van["SOEC"] == pytest.approx(
            VAN_SOEC_DEMO, rel=REL)
        riga_lcoh = df[df["Voce"] == "LCOH (EUR/kg)"].iloc[0]
        assert riga_lcoh["SOEC"] == pytest.approx(
            LCOH_SOEC_DEMO, rel=REL)


class TestDemo:
    def _bc(self, **kw):
        d = _F["mh729_demo"]()
        d.update(kw)
        return _F["mh729_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["e_kwh_anno"] == pytest.approx(
            E_DEMO, rel=REL)
        assert c["costo_el_eur_anno"] == pytest.approx(
            COSTO_EL_DEMO, rel=REL)
        for suf, h2, ric, om, cx, netto, van, tir, pb, lcoh, verd, dl in (
                ("alk", H2_ALK_DEMO, RIC_ALK_DEMO,
                 OM_ALK_DEMO, CAPEX_ALK_DEMO, NETTO_ALK_DEMO,
                 VAN_ALK_DEMO, TIR_ALK_DEMO, PAYBACK_ALK_DEMO,
                 LCOH_ALK_DEMO, VERDETTO_ALK_DEMO,
                 DELTA_ALK_DEMO),
                ("pem", H2_PEM_DEMO, RIC_PEM_DEMO,
                 OM_PEM_DEMO, CAPEX_PEM_DEMO, NETTO_PEM_DEMO,
                 VAN_PEM_DEMO, TIR_PEM_DEMO, PAYBACK_PEM_DEMO,
                 LCOH_PEM_DEMO, VERDETTO_PEM_DEMO,
                 DELTA_PEM_DEMO),
                ("soec", H2_SOEC_DEMO, RIC_SOEC_DEMO,
                 OM_SOEC_DEMO, CAPEX_SOEC_DEMO, NETTO_SOEC_DEMO,
                 VAN_SOEC_DEMO, TIR_SOEC_DEMO, PAYBACK_SOEC_DEMO,
                 LCOH_SOEC_DEMO, VERDETTO_SOEC_DEMO,
                 DELTA_SOEC_DEMO)):
            assert c[f"h2_{suf}_kg_anno"] == pytest.approx(
                h2, rel=REL), suf
            assert c[f"ricavo_{suf}_eur_anno"] == pytest.approx(
                ric, rel=REL), suf
            assert c[f"om_{suf}_eur_anno"] == pytest.approx(
                om, rel=REL), suf
            assert c[f"capex_{suf}_eur"] == pytest.approx(
                cx, rel=REL), suf
            assert c[f"netto_{suf}_eur_anno"] == pytest.approx(
                netto, rel=REL), suf
            assert abs(c[f"van_{suf}"] - van) <= 1.0, suf
            assert abs(c[f"tir_{suf}"] - tir) <= 0.01, suf
            assert c[f"payback_{suf}"] == pb, suf
            assert c[f"lcoh_{suf}_eur_kg"] == pytest.approx(
                lcoh, rel=REL), suf
            assert c[f"verdetto_{suf}"] == verd, suf
            assert c[f"delta_lcoh_{suf}_eur_kg"] == pytest.approx(
                dl, rel=REL), suf
            assert len(c[f"flussi_{suf}"]) == 21, suf
        assert c["migliore"] == MIGLIORE_DEMO
        assert c["lcoh_migliore_eur_kg"] == pytest.approx(
            LCOH_SOEC_DEMO, rel=REL)
        assert abs(c["van_migliore_eur"] - VAN_SOEC_DEMO) <= 1.0

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()[
            "van_alk"] == _F["demo_calcoli"]()["van_alk"]
        assert _F["demo_calcoli"]()[
            "van_soec"] == _F["demo_calcoli"]()["van_soec"]

    def test_demo_defaults_contro_costanti_test(self):
        d = _F["mh729_demo"]()
        for k, v in _DEMO.items():
            assert d[k] == v, k
        assert len(d) == 16

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("e_kwh_anno",
                       "costo_el_eur_anno",
                       "h2_alk_kg_anno",
                       "ricavo_alk_eur_anno",
                       "om_alk_eur_anno",
                       "capex_alk_eur",
                       "netto_alk_eur_anno",
                       "van_alk",
                       "tir_alk",
                       "lcoh_alk_eur_kg",
                       "h2_pem_kg_anno",
                       "ricavo_pem_eur_anno",
                       "om_pem_eur_anno",
                       "capex_pem_eur",
                       "netto_pem_eur_anno",
                       "van_pem",
                       "tir_pem",
                       "lcoh_pem_eur_kg",
                       "h2_soec_kg_anno",
                       "ricavo_soec_eur_anno",
                       "om_soec_eur_anno",
                       "capex_soec_eur",
                       "netto_soec_eur_anno",
                       "van_soec",
                       "tir_soec",
                       "lcoh_soec_eur_kg",
                       "van_migliore_eur"):
            assert repr(c[chiave]) in doc, chiave
        assert "payback_alk = 7" in doc
        assert "payback_pem = 16" in doc
        assert "payback_soec = 8" in doc
        assert "verdetto_alk = 'CONVIENTE'" in doc
        assert "verdetto_pem = 'NON_CONVIENTE'" in doc
        assert "verdetto_soec = 'CONVIENTE'" in doc
        assert "migliore = 'soec'" in doc

    def test_elettricita_economica_vince_alcalino(self):
        # Prezzo elettricita' 20 EUR/MWh: costo
        # 1.000.000 EUR/anno; LCOH alcalino
        # 1,60 EUR/kg, SOEC 1,76 EUR/kg, PEM
        # 2,035 EUR/kg -> migliore alcalino.
        n = self._bc(prezzo_el_eur_mwh=20.0)
        assert n["valid"] is True
        assert n["migliore"] == "alk"
        assert n["lcoh_alk_eur_kg"] == pytest.approx(
            1.60, rel=REL)
        assert n["lcoh_soec_eur_kg"] == pytest.approx(
            1.76, rel=REL)
        assert n["lcoh_pem_eur_kg"] == pytest.approx(
            2.035, rel=1e-9)

    def test_prezzo_h2_alto_tutti_convienti(self):
        # Prezzo H2 8 EUR/kg: netto PEM
        # 3.522.727,27 EUR/anno, VAN PEM
        # largamente positivo -> tutti CONVIENTE.
        n = self._bc(prezzo_h2_eur_kg=8.0)
        assert n["valid"] is True
        assert n["verdetto_alk"] == "CONVIENTE"
        assert n["verdetto_pem"] == "CONVIENTE"
        assert n["verdetto_soec"] == "CONVIENTE"

    def test_prezzo_h2_medio_pem_marginale(self):
        # Prezzo H2 5,20 EUR/kg: netto PEM
        # 977.272,73 EUR/anno, VAN PEM circa
        # -791.000 EUR, entro la tolleranza
        # 10 % di 12.000.000 = 1.200.000 ->
        # MARGINALE.
        n = self._bc(prezzo_h2_eur_kg=5.2)
        assert n["valid"] is True
        assert n["verdetto_pem"] == "MARGINALE"
        assert -1200000.0 < n["van_pem"] < 0.0

    def test_capex_zero_tir_none_payback_zero(self):
        # CAPEX alcalino zero e prezzo H2 8:
        # tutti i flussi alcalino >= 0 -> TIR
        # None, payback 0, VAN positivo ->
        # CONVIENTE.
        n = self._bc(capex_alk_eur_kw=0.0,
                     prezzo_h2_eur_kg=8.0)
        assert n["valid"] is True
        assert n["capex_alk_eur"] == pytest.approx(0.0, abs=1e-9)
        assert n["tir_alk"] is None
        assert n["payback_alk"] == 0
        assert n["verdetto_alk"] == "CONVIENTE"

    def test_potenza_zero_neutro(self):
        n = self._bc(potenza_mw=0.0)
        assert n["verdetto_alk"] == "NON_CALCOLABILE"
        assert n["verdetto_pem"] == "NON_CALCOLABILE"
        assert n["verdetto_soec"] == "NON_CALCOLABILE"
        assert n["valid"] is False
        assert n["migliore"] is None

    def test_consumo_zero_neutro(self):
        for k in ("consumo_alk_kwh_kg", "consumo_pem_kwh_kg",
                  "consumo_soec_kwh_kg"):
            n = self._bc(**{k: 0.0})
            assert n["verdetto_alk"] == "NON_CALCOLABILE", k
            assert n["valid"] is False, k

    def test_consumo_negativo_neutro(self):
        n = self._bc(consumo_pem_kwh_kg=-5.0)
        assert n["verdetto_pem"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_ore_zero_neutro(self):
        n = self._bc(ore_anno=0)
        assert n["verdetto_alk"] == "NON_CALCOLABILE"

    def test_wacc_zero_e_uno_neutri(self):
        assert self._bc(wacc_frac=0.0)["verdetto_alk"] == "NON_CALCOLABILE"
        assert self._bc(wacc_frac=1.0)["verdetto_alk"] == "NON_CALCOLABILE"

    def test_tolleranza_uno_neutro(self):
        n = self._bc(tolleranza_frac=1.0)
        assert n["verdetto_alk"] == "NON_CALCOLABILE"

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto_alk"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(potenza_mw=float("nan"))
        assert n["verdetto_alk"] == "NON_CALCOLABILE"
        assert n["netto_alk_eur_anno"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(potenza_mw=float("inf"))
        assert n["verdetto_alk"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(vita_anni=True)
        assert n["verdetto_alk"] == "NON_CALCOLABILE"

    def test_stringa_neutro(self):
        n = self._bc(potenza_mw="10")
        assert n["verdetto_alk"] == "NON_CALCOLABILE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh729_neutro"]()
        assert n["valid"] is False
        assert n["errore"] == ""
        assert list(n["df_confronto"].columns) == [
            "Voce", "Alcalino", "PEM", "SOEC"]
        assert len(n["df_confronto"]) == 0
        assert list(n["df_flussi"].columns) == ["Anno",
                                               "Flusso alcalino (EUR/anno)",
                                               "Cumulato alcalino (EUR)",
                                               "Flusso PEM (EUR/anno)",
                                               "Cumulato PEM (EUR)",
                                               "Flusso SOEC (EUR/anno)",
                                               "Cumulato SOEC (EUR)"]
        assert len(n["df_flussi"]) == 0
        assert list(n["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(n["df_tabella"]) == 0
        assert n["flussi_alk"] == []
        assert n["flussi_pem"] == []
        assert n["flussi_soec"] == []
        assert n["tir_alk"] is None
        assert n["tir_pem"] is None
        assert n["tir_soec"] is None
        assert n["payback_alk"] is None
        assert n["payback_pem"] is None
        assert n["payback_soec"] is None
        assert n["lcoh_alk_eur_kg"] is None
        assert n["lcoh_pem_eur_kg"] is None
        assert n["lcoh_soec_eur_kg"] is None
        assert n["migliore"] is None

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh729_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "potenza_mw", "ore_anno",
                       "prezzo_el_eur_mwh",
                       "prezzo_h2_eur_kg",
                       "wacc_frac", "vita_anni",
                       "tolleranza_frac",
                       "consumo_alk_kwh_kg",
                       "capex_alk_eur_kw",
                       "om_alk_eur_kw_anno",
                       "consumo_pem_kwh_kg",
                       "capex_pem_eur_kw",
                       "om_pem_eur_kw_anno",
                       "consumo_soec_kwh_kg",
                       "capex_soec_eur_kw",
                       "om_soec_eur_kw_anno",
                       "e_kwh_anno",
                       "costo_el_eur_anno",
                       "migliore",
                       "lcoh_migliore_eur_kg",
                       "van_migliore_eur",
                       "df_confronto", "df_flussi",
                       "df_tabella"):
            assert chiave in n, chiave
        for suf in ("alk", "pem", "soec"):
            for c in (f"h2_{suf}_kg_anno",
                      f"ricavo_{suf}_eur_anno",
                      f"om_{suf}_eur_anno",
                      f"capex_{suf}_eur",
                      f"netto_{suf}_eur_anno",
                      f"flussi_{suf}",
                      f"van_{suf}",
                      f"tir_{suf}",
                      f"payback_{suf}",
                      f"lcoh_{suf}_eur_kg",
                      f"verdetto_{suf}",
                      f"delta_lcoh_{suf}_eur_kg"):
                assert c in n, c
        assert n["errore"] == "errore di prova"
        assert n["tir_alk"] is None

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert b["valid"] is True
        assert list(b["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(b["df_tabella"]) == 41
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Energia elettrica (kWh/anno)" in voci
        assert "VAN alcalino (EUR)" in voci
        assert "VAN PEM (EUR)" in voci
        assert "VAN SOEC (EUR)" in voci
        assert "LCOH SOEC (EUR/kg)" in voci
        assert "Migliore (LCOH minimo)" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso alcalino (EUR/anno)",
                                               "Cumulato alcalino (EUR)",
                                               "Flusso PEM (EUR/anno)",
                                               "Cumulato PEM (EUR)",
                                               "Flusso SOEC (EUR/anno)",
                                               "Cumulato SOEC (EUR)"]
        assert len(b["df_flussi"]) == 21
        assert b["df_flussi"]["Flusso alcalino (EUR/anno)"].iloc[0] == \
            pytest.approx(-CAPEX_ALK_DEMO, rel=REL)
        assert b["df_flussi"]["Flusso alcalino (EUR/anno)"].iloc[1] == \
            pytest.approx(NETTO_ALK_DEMO, rel=REL)
        assert list(b["df_confronto"].columns) == [
            "Voce", "Alcalino", "PEM", "SOEC"]
        assert len(b["df_confronto"]) == 7


class TestCsv:
    def _ing(self):
        return _F["mh729_demo"]()

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh729_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") == 54

    def test_csv_contiene_verdetti_e_costi(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh729_csv"](bc, self._ing())
        assert "verdetto_alk;CONVIENTE" in txt
        assert "verdetto_pem;NON_CONVIENTE" in txt
        assert "verdetto_soec;CONVIENTE" in txt
        assert "migliore;soec" in txt
        assert "costo_el_eur_anno" in txt
        assert "van_alk_eur" in txt
        assert "van_pem_eur" in txt
        assert "van_soec_eur" in txt
        assert "tir_alk_pct" in txt
        assert "payback_alk_anni" in txt
        assert "lcoh_alk_eur_kg" in txt
        assert "lcoh_soec_eur_kg" in txt
        assert "delta_lcoh_pem_eur_kg" in txt
        assert "potenza_mw" in txt
        assert "e_kwh_anno" in txt
        assert "capex_alk_eur" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh729_csv"](bc, self._ing())
        assert f"netto_alk_eur_anno;{bc['netto_alk_eur_anno']}" in txt
        assert f"e_kwh_anno;{bc['e_kwh_anno']}" in txt
        assert "potenza_mw;10.0" in txt
        assert "capex_alk_eur_kw;800.0" in txt
        assert f"lcoh_migliore_eur_kg;{bc['lcoh_migliore_eur_kg']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def729["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def729\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 16, ui_keys
        demo_keys = set(_F["mh729_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh729_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh729_demo():")
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
        ui_keys = set(re.findall(r'_def729\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W730 (26/10/2026) - tab729' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh729_num", "mh729_nneg", "mh729_pos",
                     "mh729_int_pos", "mh729_frac_01",
                     "mh729_frac_toll",
                     "mh729_e_kwh", "mh729_h2",
                     "mh729_costo_el", "mh729_ricavo",
                     "mh729_om", "mh729_capex",
                     "mh729_netto", "mh729_flussi",
                     "mh729_van", "mh729_tir",
                     "mh729_payback", "mh729_lcoh",
                     "mh729_verdetto", "mh729_tecnologia",
                     "mh729_valida", "_mh729_neutro",
                     "mh729_calcola", "mh729_confronto",
                     "mh729_csv", "mh729_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_nessun_residuo_728(self):
        assert "mh728" not in _helpers_src()
        assert "mh728" not in _ui_src()
        assert "st728" not in _ui_src()
        assert "tab728" not in _ui_src()
        assert "mh729" in _helpers_src()
        assert "st729" in _ui_src()

    def test_helpers_parse_ast(self):
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w730_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE729) == 1

    def test_blocco_with_tab729(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab729:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE729

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st729_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 19, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st729_") for k in keys)

    def test_chiavi_st_input_presenti(self):
        keys = re.findall(r'key="(st729_[a-z0-9_]+)"', _ui_src())
        attese = ["st729_pot", "st729_ore",
                  "st729_prezzo_el", "st729_prezzo_h2",
                  "st729_consumo_alk", "st729_capex_alk",
                  "st729_om_alk",
                  "st729_consumo_pem", "st729_capex_pem",
                  "st729_om_pem",
                  "st729_consumo_soec", "st729_capex_soec",
                  "st729_om_soec",
                  "st729_vita", "st729_wacc",
                  "st729_tolleranza", "st729_calcola"]
        assert len(attese) == 17
        for k in attese:
            assert k in keys, k

    def test_chiavi_st_niente_fstring_dinamiche(self):
        src = _ui_src()
        assert 'key=f"' not in src
        assert "key=f'" not in src

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg729" in src
        assert "NON_CALCOLABILE" in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg729") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg729")
        assert g < src.index("st.bar_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "LCOH migliore (EUR/kg)" in src
        assert "VAN migliore (EUR)" in src
        assert "H2 migliore (kg/anno)" in src
        assert "Payback migliore (anni)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON_CALCOLABILE"):
            assert v in src

    def test_distinzioni_presenti(self):
        src = _ui_src()
        assert "singola tecnologia" in src
        assert "reforming" in src
        assert "compressione" in src
        assert "fuel cell" in src
        assert "power-to-X" in src

    def test_distinzioni_in_header_helpers(self):
        src = _helpers_src()
        assert "singola tecnologia" in src
        assert "reforming" in src
        assert "compressione" in src
        assert "fuel cell" in src
        assert "power-to-X" in src

    def test_nota_didattica_presente(self):
        src = _ui_src()
        assert "NOTA DIDATTICA" in src
        assert "50.000.000" in src
        assert "1.000.000" in src

    def test_grafico_bar_chart_presente(self):
        src = _ui_src()
        assert "st.bar_chart" in src
        assert "_dati729" in src
        assert '"LCOH (EUR/kg)"' in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh729_csv" in src
        assert "elettrolizzatori_confronto.csv" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st729_show_flussi" in src
        assert "st.checkbox" in src

    def test_em_dash_solo_nel_titolo_e_niente_nome(self):
        # Il trattino lungo e' ammesso SOLO nel
        # titolo della tab (richiesto dal brief):
        # 1 occorrenza nell'header helper, 2 in UI
        # (h1 + titolo edu). Niente nome altrove.
        assert _helpers_src().count("—") == 1
        assert _ui_src().count("—") == 2
        assert "Emanuele" not in _helpers_src()
        assert "Emanuele" not in _ui_src()

    def test_ancora_helper_presente(self):
        assert "# W730 (26/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab729:")
