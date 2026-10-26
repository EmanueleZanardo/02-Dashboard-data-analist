"""Test tab726 "🚚💧 Camion pesante a idrogeno: il fuel-cell paga contro il diesel?"

Nuova tab tab726 (fuel-cell, w727).
Business case INCREMENTALE per-mezzo di un
camion pesante fuel-cell contro il diesel:
tutta l'economia di investimento (flussi,
VAN, TIR, payback, verdetto) e' sul risparmio
annuo per mezzo (costo totale diesel meno
costo totale H2), con scala di flotta.
Fisica: litri_diesel = km / 100 x cons_diesel;
kg_h2 = km / 100 x cons_h2; costi totali =
carburante + manutenzione; TCO/km = costo
totale / km; capex_incr = acquisto_h2 -
acquisto_diesel. CO2 evitata INFORMATIVA, mai
nel conto economico (H2 zero emissioni allo
scarico, upstream fuori perimetro).

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
km annui 120000; consumo diesel 32 L/100km;
prezzo diesel 1,70 EUR/L; consumo H2 8
kg/100km; prezzo H2 4 EUR/kg; manutenzione
diesel 0,15 EUR/km; manutenzione H2 0,12
EUR/km; prezzo acquisto diesel 120000 EUR;
prezzo acquisto H2 280000 EUR; numero mezzi
10; vita 8 anni; WACC 0,06 (6 %); tolleranza
0,10 (10 % del CAPEX incrementale).

- litri_diesel_anno = 38400.0
- costo_carb_diesel_eur_anno = 65280.0
- costo_manut_diesel_eur_anno = 18000.0
- costo_tot_diesel_eur_anno = 83280.0
- kg_h2_anno = 9600.0
- costo_carb_h2_eur_anno = 38400.0
- costo_manut_h2_eur_anno = 14400.0
- costo_tot_h2_eur_anno = 52800.0
- risparmio_annuo_mezzo_eur_anno = 30480.0
- tco_km_diesel_eur_km = 0.694
- tco_km_h2_eur_km = 0.44
- capex_incr_eur = 160000.0
- co2_diesel_t_anno = 102.912
- co2_evitata_t_anno = 102.912
- risparmio_annuo_flotta_eur_anno = 304800.0
- co2_evitata_flotta_t_anno = 1029.1200000000001
- van = 29274.51535835196
- van_flotta_eur = 292745.1535835196
- tir = 10.446281589206759
- payback = 6
- verdetto = 'CONVIENTE'

Scomposizione: litri diesel 120000 / 100 x 32
= 38400,0 L/anno; carburante diesel 38400,0 x
1,70 = 65280,0 EUR/anno; manutenzione diesel
120000 x 0,15 = 18000,0 EUR/anno; costo
totale diesel 65280,0 + 18000,0 = 83280,0
EUR/anno; kg H2 120000 / 100 x 8 = 9600,0
kg/anno; carburante H2 9600,0 x 4 = 38400,0
EUR/anno; manutenzione H2 120000 x 0,12 =
14400,0 EUR/anno; costo totale H2 38400,0 +
14400,0 = 52800,0 EUR/anno; risparmio annuo
per mezzo 83280,0 - 52800,0 = 30480,0
EUR/anno; TCO diesel 83280,0 / 120000 =
0,694 EUR/km; TCO H2 52800,0 / 120000 = 0,44
EUR/km; CAPEX incrementale 280000,0 -
120000,0 = 160000,0 EUR; flussi: anno 0
-160000,0, anni 1-8 risparmio 30480,0
(piatti); VAN 29274,51535835196 a WACC 6 %
su 8 anni; TIR 10,446281589206759 % (il tasso
che azzera il VAN dei flussi sopra); payback
6 (il cumulato diventa positivo all'anno 6:
-160000,0 + 5 x 30480,0 = -7600,0 all'anno 5,
poi + 30480,0 = 22880,0 all'anno 6); CO2
diesel 38400,0 x 0,00268 = 102,912 t/anno;
CO2 evitata 102,912 t/anno per mezzo
(INFORMATIVA: non entra nel conto economico)
e 1029,1200000000001 t/anno di flotta (x 10
mezzi); risparmio flotta 30480,0 x 10 =
304800,0 EUR/anno; VAN flotta
29274,51535835196 x 10 = 292745,1535835196
EUR; VAN >= 0 -> CONVIENTE.
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
    if (p / "w727_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w727_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w727_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w727_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w727_helpers.py: {missing}")
    return out


_F = _load("mh726_num", "mh726_nneg", "mh726_pos",
           "mh726_int_pos", "mh726_litri_diesel",
           "mh726_kg_h2", "mh726_costo_carb",
           "mh726_costo_manut", "mh726_costo_tot",
           "mh726_risparmio", "mh726_tco_km",
           "mh726_capex_incr", "mh726_co2_diesel",
           "mh726_co2_evitata", "mh726_flussi",
           "mh726_van_flussi", "mh726_tir_flussi",
           "mh726_payback_flussi", "mh726_verdetto",
           "mh726_confronto", "mh726_valida",
           "_mh726_neutro", "mh726_calcola",
           "mh726_sensitivita", "mh726_csv",
           "mh726_demo", "demo_calcoli")

TITLE726 = ("🚚💧 Camion pesante a idrogeno: "
            "il fuel-cell paga contro il diesel?")

LITRI_DEMO = 38400.0
CC_DIESEL_DEMO = 65280.0
CM_DIESEL_DEMO = 18000.0
CT_DIESEL_DEMO = 83280.0
KG_DEMO = 9600.0
CC_H2_DEMO = 38400.0
CM_H2_DEMO = 14400.0
CT_H2_DEMO = 52800.0
RISP_DEMO = 30480.0
TCO_DIESEL_DEMO = 0.694
TCO_H2_DEMO = 0.44
CAPEX_DEMO = 160000.0
CO2_DEMO = 102.912
RISP_FLOTTA_DEMO = 304800.0
CO2_FLOTTA_DEMO = 1029.1200000000001
VAN_DEMO = 29274.51535835196
VAN_FLOTTA_DEMO = 292745.1535835196
TIR_DEMO = 10.446281589206759
PAYBACK_DEMO = 6
VITA_DEMO = 8
N_MEZZI_DEMO = 10
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w727_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w727_ui.py").read_text(encoding="utf-8")


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh726_demo"]()
        d.update(kw)
        return _F["mh726_valida"](**d)

    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh726_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh726_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh726_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh726_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh726_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh726_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh726_pos"](0.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh726_int_pos"](2.5, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh726_int_pos"](8.0, "x") == 8

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_km_zero_non_valido(self):
        assert self._val(km_annui=0.0)["valido"] is False

    def test_consumi_zero_non_validi(self):
        assert self._val(cons_diesel_l_100km=0.0)["valido"] is False
        assert self._val(cons_h2_kg_100km=0.0)["valido"] is False

    def test_negativi_non_validi(self):
        for k in ("prezzo_diesel_eur_l",
                  "prezzo_h2_eur_kg",
                  "manut_diesel_eur_km",
                  "manut_h2_eur_km",
                  "prezzo_acquisto_diesel_eur",
                  "prezzo_acquisto_h2_eur",
                  "wacc_frac", "tolleranza_frac"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_n_mezzi_zero_non_valido(self):
        assert self._val(n_mezzi=0)["valido"] is False

    def test_n_mezzi_non_intero_non_valido(self):
        assert self._val(n_mezzi=2.5)["valido"] is False

    def test_vita_zero_non_valida(self):
        assert self._val(vita_anni=0)["valido"] is False

    def test_vita_non_intera_non_valida(self):
        assert self._val(vita_anni=8.5)["valido"] is False

    def test_tolleranza_sopra_uno_valida_brief(self):
        assert self._val(tolleranza_frac=1.5)["valido"] is True

    def test_wacc_senza_tetto_superiore(self):
        assert self._val(wacc_frac=1.5)["valido"] is True

    def test_nan_non_valido(self):
        assert self._val(km_annui=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(km_annui=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(vita_anni=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(km_annui="120000")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(prezzo_diesel_eur_l=0.0)["valido"] is True
        assert self._val(prezzo_h2_eur_kg=0.0)["valido"] is True
        assert self._val(manut_diesel_eur_km=0.0)["valido"] is True
        assert self._val(manut_h2_eur_km=0.0)["valido"] is True
        assert self._val(prezzo_acquisto_diesel_eur=0.0)["valido"] is True
        assert self._val(prezzo_acquisto_h2_eur=0.0)["valido"] is True
        assert self._val(wacc_frac=0.0)["valido"] is True
        assert self._val(tolleranza_frac=0.0)["valido"] is True


class TestFunzioni:
    def test_litri_demo(self):
        assert _F["mh726_litri_diesel"](
            120000.0, 32.0) == pytest.approx(
            LITRI_DEMO, rel=REL)

    def test_kg_demo(self):
        assert _F["mh726_kg_h2"](
            120000.0, 8.0) == pytest.approx(
            KG_DEMO, rel=REL)

    def test_costo_carb_diesel_demo(self):
        assert _F["mh726_costo_carb"](
            LITRI_DEMO, 1.70) == pytest.approx(
            CC_DIESEL_DEMO, rel=REL)

    def test_costo_carb_h2_demo(self):
        assert _F["mh726_costo_carb"](
            KG_DEMO, 4.0) == pytest.approx(
            CC_H2_DEMO, rel=REL)

    def test_costo_manut_diesel_demo(self):
        assert _F["mh726_costo_manut"](
            120000.0, 0.15) == pytest.approx(
            CM_DIESEL_DEMO, rel=REL)

    def test_costo_manut_h2_demo(self):
        assert _F["mh726_costo_manut"](
            120000.0, 0.12) == pytest.approx(
            CM_H2_DEMO, rel=REL)

    def test_costo_tot_diesel_demo(self):
        assert _F["mh726_costo_tot"](
            CC_DIESEL_DEMO, CM_DIESEL_DEMO) == pytest.approx(
            CT_DIESEL_DEMO, rel=REL)

    def test_costo_tot_h2_demo(self):
        assert _F["mh726_costo_tot"](
            CC_H2_DEMO, CM_H2_DEMO) == pytest.approx(
            CT_H2_DEMO, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh726_risparmio"](
            CT_DIESEL_DEMO, CT_H2_DEMO) == pytest.approx(
            RISP_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh726_risparmio"](
            50000.0, 60000.0) == pytest.approx(
            -10000.0, rel=REL)

    def test_tco_km_diesel_demo(self):
        assert _F["mh726_tco_km"](
            CT_DIESEL_DEMO, 120000.0) == pytest.approx(
            TCO_DIESEL_DEMO, rel=REL)

    def test_tco_km_h2_demo(self):
        assert _F["mh726_tco_km"](
            CT_H2_DEMO, 120000.0) == pytest.approx(
            TCO_H2_DEMO, rel=REL)

    def test_capex_incr_demo(self):
        assert _F["mh726_capex_incr"](
            280000.0, 120000.0) == pytest.approx(
            CAPEX_DEMO, rel=REL)

    def test_capex_incr_negativo(self):
        assert _F["mh726_capex_incr"](
            100000.0, 120000.0) == pytest.approx(
            -20000.0, rel=REL)

    def test_co2_diesel_demo(self):
        assert _F["mh726_co2_diesel"](
            LITRI_DEMO) == pytest.approx(
            CO2_DEMO, rel=REL)

    def test_co2_diesel_fattore_letterale(self):
        assert _F["mh726_co2_diesel"](
            1000.0) == pytest.approx(2.68, rel=REL)

    def test_co2_evitata_uguale_diesel(self):
        assert _F["mh726_co2_evitata"](
            CO2_DEMO) == pytest.approx(CO2_DEMO, rel=REL)

    def test_co2_evitata_zero_se_diesel_zero(self):
        assert _F["mh726_co2_evitata"](
            0.0) == pytest.approx(0.0, abs=1e-9)

    def test_flussi_demo_incrementali(self):
        flussi = _F["mh726_flussi"](CAPEX_DEMO, RISP_DEMO,
                                     VITA_DEMO)
        assert len(flussi) == VITA_DEMO + 1
        assert flussi[0] == pytest.approx(-CAPEX_DEMO, rel=REL)
        assert all(f == pytest.approx(RISP_DEMO, rel=REL)
                   for f in flussi[1:])

    def test_van_flussi_demo(self):
        flussi = _F["mh726_flussi"](CAPEX_DEMO, RISP_DEMO,
                                     VITA_DEMO)
        assert abs(_F["mh726_van_flussi"](
            flussi, 0.06) - VAN_DEMO) <= 1.0

    def test_van_flussi_tasso_zero(self):
        flussi = _F["mh726_flussi"](CAPEX_DEMO, RISP_DEMO,
                                     VITA_DEMO)
        atteso = -CAPEX_DEMO + RISP_DEMO * VITA_DEMO
        assert _F["mh726_van_flussi"](
            flussi, 0.0) == pytest.approx(atteso, rel=1e-12)

    def test_van_flussi_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh726_van_flussi"]([100.0, 100.0], -0.01)

    def test_tir_demo(self):
        flussi = _F["mh726_flussi"](CAPEX_DEMO, RISP_DEMO,
                                     VITA_DEMO)
        tir = _F["mh726_tir_flussi"](flussi)
        assert tir is not None
        assert tir * 100.0 == pytest.approx(TIR_DEMO, rel=1e-9)

    def test_tir_none_tutti_flussi_non_negativi(self):
        assert _F["mh726_tir_flussi"](
            [0.0] + [RISP_DEMO] * 8) is None

    def test_tir_none_nessun_cambio_segno_negativo(self):
        assert _F["mh726_tir_flussi"](
            [-1000.0] + [-100.0] * 10) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh726_tir_flussi"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo_sei(self):
        flussi = _F["mh726_flussi"](CAPEX_DEMO, RISP_DEMO,
                                     VITA_DEMO)
        assert _F["mh726_payback_flussi"](flussi) == PAYBACK_DEMO

    def test_payback_none_se_mai(self):
        assert _F["mh726_payback_flussi"](
            [-1000000.0] + [RISP_DEMO] * 8) is None

    def test_payback_zero_se_cumulato_anno_zero_non_negativo(self):
        assert _F["mh726_payback_flussi"](
            [0.0] + [RISP_DEMO] * 8) == 0

    def test_verdetto_conviente_demo(self):
        assert _F["mh726_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10,
            RISP_DEMO) == VERDETTO_DEMO

    def test_verdetto_van_zero_conviente(self):
        assert _F["mh726_verdetto"](
            0.0, CAPEX_DEMO, 0.10, RISP_DEMO) == "CONVIENTE"

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh726_verdetto"](
            -100.0, CAPEX_DEMO, 0.10,
            RISP_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh726_verdetto"](
            -0.10 * CAPEX_DEMO, CAPEX_DEMO, 0.10,
            RISP_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_oltre_limite(self):
        assert _F["mh726_verdetto"](
            -0.10 * CAPEX_DEMO - 1.0, CAPEX_DEMO, 0.10,
            RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risp_non_positivo(self):
        assert _F["mh726_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh726_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_positivo_conviente(self):
        assert _F["mh726_verdetto"](
            1000.0, 0.0, 0.10, RISP_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(self):
        assert _F["mh726_verdetto"](
            -1.0, 0.0, 0.10, RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_capex_zero_mai_marginale(self):
        for van in (-1.0, -100.0, -1000000.0):
            assert _F["mh726_verdetto"](
                van, 0.0, 0.10, RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_capex_negativo_mai_marginale(self):
        assert _F["mh726_verdetto"](
            -1.0, -20000.0, 0.10, RISP_DEMO) == "NON_CONVIENTE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh726_verdetto"](100.0, CAPEX_DEMO, -0.01,
                                 RISP_DEMO)

    def test_confronto_demo(self):
        df = _F["mh726_confronto"](
            LITRI_DEMO, KG_DEMO, CC_DIESEL_DEMO,
            CM_DIESEL_DEMO, CT_DIESEL_DEMO, CC_H2_DEMO,
            CM_H2_DEMO, CT_H2_DEMO, RISP_DEMO,
            TCO_DIESEL_DEMO, TCO_H2_DEMO, CO2_DEMO, CO2_DEMO)
        assert list(df.columns) == ["Voce", "Diesel",
                                    "H2", "Risparmio"]
        assert len(df) == 7
        voci = df["Voce"].tolist()
        assert "Costo totale (EUR/anno)" in voci
        assert "CO2 evitata (t/anno, informativa)" in voci
        riga_tot = df[df["Voce"] == "Costo totale (EUR/anno)"].iloc[0]
        assert riga_tot["Risparmio"] == pytest.approx(
            RISP_DEMO, rel=REL)
        riga_co2 = df[df["Voce"] == "CO2 allo scarico (t/anno)"].iloc[0]
        assert riga_co2["H2"] == pytest.approx(0.0, abs=1e-9)
        assert riga_co2["Risparmio"] == pytest.approx(
            CO2_DEMO, rel=REL)
        riga_tco = df[df["Voce"] == "TCO (EUR/km)"].iloc[0]
        assert riga_tco["Risparmio"] == pytest.approx(
            TCO_DIESEL_DEMO - TCO_H2_DEMO, rel=REL)


class TestDemo:
    def _bc(self, **kw):
        d = _F["mh726_demo"]()
        d.update(kw)
        return _F["mh726_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["litri_diesel_anno"] == pytest.approx(
            LITRI_DEMO, rel=REL)
        assert c["costo_carb_diesel_eur_anno"] == pytest.approx(
            CC_DIESEL_DEMO, rel=REL)
        assert c["costo_manut_diesel_eur_anno"] == pytest.approx(
            CM_DIESEL_DEMO, rel=REL)
        assert c["costo_tot_diesel_eur_anno"] == pytest.approx(
            CT_DIESEL_DEMO, rel=REL)
        assert c["kg_h2_anno"] == pytest.approx(KG_DEMO, rel=REL)
        assert c["costo_carb_h2_eur_anno"] == pytest.approx(
            CC_H2_DEMO, rel=REL)
        assert c["costo_manut_h2_eur_anno"] == pytest.approx(
            CM_H2_DEMO, rel=REL)
        assert c["costo_tot_h2_eur_anno"] == pytest.approx(
            CT_H2_DEMO, rel=REL)
        assert c["risparmio_annuo_mezzo_eur_anno"] == pytest.approx(
            RISP_DEMO, rel=REL)
        assert c["tco_km_diesel_eur_km"] == pytest.approx(
            TCO_DIESEL_DEMO, rel=REL)
        assert c["tco_km_h2_eur_km"] == pytest.approx(
            TCO_H2_DEMO, rel=REL)
        assert c["capex_incr_eur"] == pytest.approx(
            CAPEX_DEMO, rel=REL)
        assert c["co2_diesel_t_anno"] == pytest.approx(
            CO2_DEMO, rel=REL)
        assert c["co2_evitata_t_anno"] == pytest.approx(
            CO2_DEMO, rel=REL)
        assert c["risparmio_annuo_flotta_eur_anno"] == pytest.approx(
            RISP_FLOTTA_DEMO, rel=REL)
        assert c["co2_evitata_flotta_t_anno"] == pytest.approx(
            CO2_FLOTTA_DEMO, rel=REL)
        assert abs(c["van"] - VAN_DEMO) <= 1.0
        assert abs(c["van_flotta_eur"] - VAN_FLOTTA_DEMO) <= 1.0
        assert abs(c["tir"] - TIR_DEMO) <= 0.01
        assert c["payback"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO
        assert c["flussi"][0] == pytest.approx(-CAPEX_DEMO, rel=REL)
        assert all(f == pytest.approx(RISP_DEMO, rel=REL)
                   for f in c["flussi"][1:])
        assert len(c["flussi"]) == VITA_DEMO + 1

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()[
            "van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()[
            "risparmio_annuo_mezzo_eur_anno"] == _F["demo_calcoli"]()[
            "risparmio_annuo_mezzo_eur_anno"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        d = _F["mh726_demo"]()
        b = _F["mh726_calcola"](**d)
        coppie = [("litri_diesel_anno", LITRI_DEMO),
                  ("costo_carb_diesel_eur_anno", CC_DIESEL_DEMO),
                  ("costo_manut_diesel_eur_anno", CM_DIESEL_DEMO),
                  ("costo_tot_diesel_eur_anno", CT_DIESEL_DEMO),
                  ("kg_h2_anno", KG_DEMO),
                  ("costo_carb_h2_eur_anno", CC_H2_DEMO),
                  ("costo_manut_h2_eur_anno", CM_H2_DEMO),
                  ("costo_tot_h2_eur_anno", CT_H2_DEMO),
                  ("risparmio_annuo_mezzo_eur_anno", RISP_DEMO),
                  ("tco_km_diesel_eur_km", TCO_DIESEL_DEMO),
                  ("tco_km_h2_eur_km", TCO_H2_DEMO),
                  ("capex_incr_eur", CAPEX_DEMO),
                  ("co2_diesel_t_anno", CO2_DEMO),
                  ("co2_evitata_t_anno", CO2_DEMO),
                  ("risparmio_annuo_flotta_eur_anno",
                   RISP_FLOTTA_DEMO),
                  ("co2_evitata_flotta_t_anno", CO2_FLOTTA_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert abs(b["van"] - VAN_DEMO) <= 1.0
        assert abs(b["tir"] - TIR_DEMO) <= 0.01
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh726_demo"]()
        assert d["km_annui"] == 120000.0
        assert d["cons_diesel_l_100km"] == 32.0
        assert d["prezzo_diesel_eur_l"] == 1.70
        assert d["cons_h2_kg_100km"] == 8.0
        assert d["prezzo_h2_eur_kg"] == 4.0
        assert d["manut_diesel_eur_km"] == 0.15
        assert d["manut_h2_eur_km"] == 0.12
        assert d["prezzo_acquisto_diesel_eur"] == 120000.0
        assert d["prezzo_acquisto_h2_eur"] == 280000.0
        assert d["n_mezzi"] == 10
        assert d["vita_anni"] == 8
        assert d["wacc_frac"] == 0.06
        assert d["tolleranza_frac"] == 0.10
        assert len(d) == 13

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("litri_diesel_anno",
                       "costo_carb_diesel_eur_anno",
                       "costo_manut_diesel_eur_anno",
                       "costo_tot_diesel_eur_anno",
                       "kg_h2_anno",
                       "costo_carb_h2_eur_anno",
                       "costo_manut_h2_eur_anno",
                       "costo_tot_h2_eur_anno",
                       "risparmio_annuo_mezzo_eur_anno",
                       "tco_km_diesel_eur_km",
                       "tco_km_h2_eur_km",
                       "capex_incr_eur",
                       "co2_diesel_t_anno",
                       "co2_evitata_t_anno",
                       "risparmio_annuo_flotta_eur_anno",
                       "co2_evitata_flotta_t_anno",
                       "van", "van_flotta_eur"):
            assert repr(c[chiave]) in doc, chiave
        assert f"tir = {repr(c['tir'])}" in doc
        assert "payback = 6" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_prezzo_h2_5_5_non_conviente(self):
        # Prezzo H2 5,50 EUR/kg: risparmio
        # 16080, VAN -60146,52, TIR -4,61 %,
        # payback mai -> NON_CONVIENTE (fuori
        # tolleranza: 10 % di 160000 = 16000).
        n = self._bc(prezzo_h2_eur_kg=5.5)
        assert n["valid"] is True
        assert n["risparmio_annuo_mezzo_eur_anno"] == pytest.approx(
            16080.0, rel=REL)
        assert abs(n["van"] - (-60146.51551960959)) <= 1.0
        assert abs(n["tir"] - (-4.6086314882217625)) <= 0.01
        assert n["payback"] is None
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_prezzo_h2_7_5_risp_negativo_neutro(self):
        # Prezzo H2 7,50: costo H2 86400 > costo
        # diesel 83280 -> risparmio negativo ->
        # dict neutro NON_CALCOLABILE.
        n = self._bc(prezzo_h2_eur_kg=7.5)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_annuo_mezzo_eur_anno"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_manut_h2_alta_risp_negativo_neutro(self):
        # Manutenzione H2 0,50 EUR/km: costo H2
        # 98400 > costo diesel 83280 -> neutro.
        n = self._bc(manut_h2_eur_km=0.5)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_acq_h2_310k_marginale(self):
        # Acquisto H2 310000: CAPEX incrementale
        # 190000, VAN -725,48, TIR 5,90 %,
        # payback 7 -> MARGINALE (|VAN| <= 10 %
        # di 190000 = 19000).
        n = self._bc(prezzo_acquisto_h2_eur=310000.0)
        assert n["valid"] is True
        assert n["capex_incr_eur"] == pytest.approx(
            190000.0, rel=REL)
        assert abs(n["van"] - (-725.4846416480432)) <= 1.0
        assert abs(n["tir"] - 5.903436125638957) <= 0.01
        assert n["payback"] == 7
        assert n["verdetto"] == "MARGINALE"

    def test_acq_h2_400k_non_conviente(self):
        # Acquisto H2 400000: CAPEX incrementale
        # 280000, VAN -90725,48, TIR -2,97 %,
        # payback mai -> NON_CONVIENTE.
        n = self._bc(prezzo_acquisto_h2_eur=400000.0)
        assert n["valid"] is True
        assert abs(n["van"] - (-90725.48464164806)) <= 1.0
        assert abs(n["tir"] - (-2.9745288490817665)) <= 0.01
        assert n["payback"] is None
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_acq_uguali_tir_none_payback_zero(self):
        # Acquisti uguali: CAPEX incrementale 0,
        # tutti i flussi >= 0 -> TIR None,
        # payback 0, VAN 189274,52 -> CONVIENTE.
        n = self._bc(prezzo_acquisto_h2_eur=120000.0)
        assert n["valid"] is True
        assert n["capex_incr_eur"] == pytest.approx(0.0, abs=1e-9)
        assert n["tir"] is None
        assert n["payback"] == 0
        assert abs(n["van"] - 189274.51535835193) <= 1.0
        assert n["verdetto"] == "CONVIENTE"

    def test_acq_h2_minore_tir_none_payback_zero(self):
        # Acquisto H2 100000 < diesel 120000:
        # CAPEX incrementale -20000, flusso anno
        # 0 positivo, TIR None, payback 0, VAN
        # 209274,52 -> CONVIENTE.
        n = self._bc(prezzo_acquisto_h2_eur=100000.0)
        assert n["valid"] is True
        assert n["capex_incr_eur"] == pytest.approx(
            -20000.0, rel=REL)
        assert n["tir"] is None
        assert n["payback"] == 0
        assert abs(n["van"] - 209274.51535835193) <= 1.0
        assert n["verdetto"] == "CONVIENTE"

    def test_km_60000_non_conviente(self):
        # Soli 60000 km/anno: risparmio dimezza
        # a 15240, CAPEX fisso -> VAN -65362,74,
        # TIR -5,67 %, payback mai ->
        # NON_CONVIENTE.
        n = self._bc(km_annui=60000.0)
        assert n["valid"] is True
        assert n["risparmio_annuo_mezzo_eur_anno"] == pytest.approx(
            15240.0, rel=REL)
        assert abs(n["van"] - (-65362.74232082404)) <= 1.0
        assert abs(n["tir"] - (-5.674166508012663)) <= 0.01
        assert n["payback"] is None
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_vita_5_non_conviente(self):
        # Vita 5 anni: VAN -31607,15, TIR
        # -1,60 %, payback mai -> NON_CONVIENTE.
        n = self._bc(vita_anni=5)
        assert n["valid"] is True
        assert abs(n["van"] - (-31607.151815957055)) <= 1.0
        assert abs(n["tir"] - (-1.6005478982670553)) <= 0.01
        assert n["payback"] is None
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_km_zero_neutro(self):
        n = self._bc(km_annui=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_cons_zero_neutro(self):
        assert self._bc(cons_diesel_l_100km=0.0)["verdetto"] == \
            "NON_CALCOLABILE"
        assert self._bc(cons_h2_kg_100km=0.0)["verdetto"] == \
            "NON_CALCOLABILE"

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_n_mezzi_zero_neutro(self):
        n = self._bc(n_mezzi=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_negativo_neutro(self):
        n = self._bc(wacc_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_negativa_neutro(self):
        n = self._bc(tolleranza_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(km_annui=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_annuo_mezzo_eur_anno"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(km_annui=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(vita_anni=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_zero_calcolabile(self):
        # WACC 0: VAN = somma flussi =
        # -160000 + 30480 x 8 = 83840.
        n = self._bc(wacc_frac=0.0)
        assert n["van"] == pytest.approx(83840.0, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh726_neutro"]()
        assert n["valid"] is False
        assert n["errore"] == ""
        assert list(n["df_confronto"].columns) == ["Voce", "Diesel",
                                                  "H2", "Risparmio"]
        assert len(n["df_confronto"]) == 0
        assert list(n["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(n["df_flussi"]) == 0
        assert list(n["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(n["df_tabella"]) == 0
        assert n["flussi"] == []
        assert n["tir"] is None
        assert n["payback"] is None

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh726_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "km_annui", "cons_diesel_l_100km",
                       "prezzo_diesel_eur_l",
                       "cons_h2_kg_100km",
                       "prezzo_h2_eur_kg",
                       "manut_diesel_eur_km",
                       "manut_h2_eur_km",
                       "prezzo_acquisto_diesel_eur",
                       "prezzo_acquisto_h2_eur",
                       "n_mezzi", "vita_anni",
                       "wacc_frac", "tolleranza_frac",
                       "litri_diesel_anno",
                       "costo_carb_diesel_eur_anno",
                       "costo_manut_diesel_eur_anno",
                       "costo_tot_diesel_eur_anno",
                       "kg_h2_anno",
                       "costo_carb_h2_eur_anno",
                       "costo_manut_h2_eur_anno",
                       "costo_tot_h2_eur_anno",
                       "risparmio_annuo_mezzo_eur_anno",
                       "tco_km_diesel_eur_km",
                       "tco_km_h2_eur_km",
                       "capex_incr_eur",
                       "co2_diesel_t_anno",
                       "co2_evitata_t_anno",
                       "risparmio_annuo_flotta_eur_anno",
                       "co2_evitata_flotta_t_anno",
                       "van_flotta_eur", "flussi",
                       "van", "tir", "payback",
                       "verdetto", "df_confronto",
                       "df_flussi", "df_tabella"):
            assert chiave in n, chiave
        assert n["errore"] == "errore di prova"
        assert n["tir"] is None

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert b["valid"] is True
        assert list(b["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(b["df_tabella"]) == 31
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Km annui (km/anno)" in voci
        assert "Kg H2 (kg/anno)" in voci
        assert "Risparmio annuo per mezzo (EUR/anno)" in voci
        assert "TCO diesel (EUR/km)" in voci
        assert "CO2 evitata per mezzo (t/anno)" in voci
        assert "VAN incrementale flotta (EUR)" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(b["df_flussi"]) == VITA_DEMO + 1
        assert b["df_flussi"]["Flusso (€/anno)"].iloc[0] == \
            pytest.approx(-CAPEX_DEMO, rel=REL)
        assert b["df_flussi"]["Flusso (€/anno)"].iloc[1] == \
            pytest.approx(RISP_DEMO, rel=REL)
        assert b["df_flussi"]["Flusso (€/anno)"].iloc[8] == \
            pytest.approx(RISP_DEMO, rel=REL)
        assert list(b["df_confronto"].columns) == ["Voce", "Diesel",
                                                  "H2", "Risparmio"]
        assert len(b["df_confronto"]) == 7


class TestSensitivita:
    def _ing(self):
        return _F["mh726_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh726_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.9", "x1.0", "x1.1"]
        assert list(s.index) == ["x0.9", "x1.0", "x1.1"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh726_sensitivita"](self._ing())
        assert abs(s.loc["x1.0", "x1.0"] - VAN_DEMO) <= 1.0

    def test_sensitivita_crescente_con_km(self):
        s = _F["mh726_sensitivita"](self._ing())
        for riga in ("x0.9", "x1.0", "x1.1"):
            assert s.loc[riga, "x0.9"] < \
                s.loc[riga, "x1.0"] < \
                s.loc[riga, "x1.1"]

    def test_sensitivita_decrescente_con_prezzo_h2(self):
        s = _F["mh726_sensitivita"](self._ing())
        for colonna in ("x0.9", "x1.0", "x1.1"):
            assert s.loc["x0.9", colonna] > \
                s.loc["x1.0", colonna] > \
                s.loc["x1.1", colonna]

    def test_sensitivita_nessuna_colonna_degenere(self):
        s = _F["mh726_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_nessuna_colonna_costante(self):
        s = _F["mh726_sensitivita"](self._ing())
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3

    def test_sensitivita_angoli(self):
        s = _F["mh726_sensitivita"](self._ing())
        assert abs(s.loc["x0.9", "x0.9"] - 31808.111233227522) <= 1.0
        assert abs(s.loc["x0.9", "x1.1"] - 74432.13595172255) <= 1.0
        assert abs(s.loc["x1.1", "x0.9"] - (-11113.983588194009)) <= 1.0
        assert abs(s.loc["x1.1", "x1.1"] - 21971.7978366517) <= 1.0

    def test_sensitivita_centro_con_vita_corta(self):
        # Con vita 5 anni il centro deve
        # coincidere col VAN del caso con vita
        # 5 anni (flussi incrementali piatti,
        # nessun altro effetto).
        ing = self._ing()
        ing["vita_anni"] = 5
        s = _F["mh726_sensitivita"](ing)
        b = _F["mh726_calcola"](**ing)
        assert abs(s.loc["x1.0", "x1.0"] - b["van"]) <= 1.0


class TestCsv:
    def _ing(self):
        return _F["mh726_demo"]()

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh726_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") == 35

    def test_csv_contiene_verdetto_e_costi(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh726_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "risparmio_annuo_mezzo_eur_anno" in txt
        assert "costo_tot_diesel_eur_anno" in txt
        assert "costo_tot_h2_eur_anno" in txt
        assert "tco_km_diesel_eur_km" in txt
        assert "tco_km_h2_eur_km" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "km_annui" in txt
        assert "kg_h2_anno" in txt
        assert "co2_evitata_t_anno" in txt
        assert "capex_incr_eur" in txt
        assert "van_flotta_eur" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh726_csv"](bc, self._ing())
        assert f"risparmio_annuo_mezzo_eur_anno;{bc['risparmio_annuo_mezzo_eur_anno']}" in txt
        assert f"litri_diesel_anno;{bc['litri_diesel_anno']}" in txt
        assert "km_annui;120000.0" in txt
        assert "prezzo_acquisto_h2_eur;280000.0" in txt
        assert f"kg_h2_anno;{bc['kg_h2_anno']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def726["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def726\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 13, ui_keys
        demo_keys = set(_F["mh726_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh726_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh726_demo():")
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
        ui_keys = set(re.findall(r'_def726\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W727 (26/10/2026) - tab726' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh726_num", "mh726_nneg", "mh726_pos",
                     "mh726_int_pos", "mh726_litri_diesel",
                     "mh726_kg_h2", "mh726_costo_carb",
                     "mh726_costo_manut", "mh726_costo_tot",
                     "mh726_risparmio", "mh726_tco_km",
                     "mh726_capex_incr", "mh726_co2_diesel",
                     "mh726_co2_evitata", "mh726_flussi",
                     "mh726_van_flussi", "mh726_tir_flussi",
                     "mh726_payback_flussi", "mh726_verdetto",
                     "mh726_confronto", "mh726_valida",
                     "_mh726_neutro", "mh726_calcola",
                     "mh726_sensitivita", "mh726_csv",
                     "mh726_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_nessun_identificatore_futura_tab(self):
        assert "mh727" not in _helpers_src()
        assert "mh727" not in _ui_src()
        assert "st727" not in _ui_src()
        assert "tab727" not in _ui_src()

    def test_helpers_parse_ast(self):
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w727_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE726) == 1

    def test_blocco_with_tab726(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab726:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE726

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st726_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 18, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st726_") for k in keys)

    def test_chiavi_st_input_sono_14(self):
        """Le 14 chiavi di input/bottone (13 input +
        bottone calcola) sono tutte presenti; le
        altre 4 sono solo chiavi di
        visualizzazione (fig, heatmap, flussi, CSV)."""
        keys = re.findall(r'key="(st726_[a-z0-9_]+)"', _ui_src())
        attese = ["st726_km", "st726_cons_diesel",
                  "st726_prezzo_diesel", "st726_cons_h2",
                  "st726_prezzo_h2", "st726_manut_diesel",
                  "st726_manut_h2", "st726_acq_diesel",
                  "st726_acq_h2", "st726_n_mezzi",
                  "st726_vita", "st726_wacc",
                  "st726_tolleranza", "st726_calcola"]
        assert len(attese) == 14
        for k in attese:
            assert k in keys, k

    def test_chiavi_st_niente_fstring_dinamiche(self):
        src = _ui_src()
        assert 'key=f"' not in src
        assert "key=f'" not in src

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg726" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg726") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg726")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "TCO diesel (€/km)" in src
        assert "TCO H2 (€/km)" in src
        assert "Risparmio annuo per mezzo (€/anno)" in src
        assert "VAN incrementale per mezzo (€)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_presente(self):
        src = _ui_src().lower()
        assert "bev" in src
        assert "pipeline" in src
        assert "v2g" in src
        assert "incrementale" in src
        assert "upstream" in src

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert '"Costo carburante"' in src
        assert '"Costo manutenzione"' in src
        assert '"Costo totale"' in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh726_csv" in src
        assert "camion_h2_tco.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN incrementale per mezzo" in src
        assert "mh726_sensitivita" in src
        assert "Heatmap" in src
        assert "Fattore prezzo H2" in src
        assert "Fattore km annui" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st726_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W727 (26/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab726:")
