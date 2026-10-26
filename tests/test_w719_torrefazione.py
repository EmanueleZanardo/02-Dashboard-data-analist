"""Test tab719 "🪵🔥 Torrefazione: i pellet torrefatti sostituiscono il carbone?"

Tab precedente tab718 (acqua di mare, w719);
nuova tab tab719 (torrefazione, w720). La tab719
replica ESATTAMENTE la semantica economica
delle tab650-718: flussi [-CAPEX_delta,
risparmio con sostituzioni], VAN/TIR (bisezione
[-99 %, +500 %], None se risparmio <= 0 o nessun
cambio di segno incl. tutti flussi >= 0)/payback
(0 se cumulato anno 0 >= 0), verdetto CONVIENTE
(VAN >= 0)/MARGINALE (VAN < 0 entro toll % di
|CAPEX_delta|; CAPEX_delta == 0 mai MARGINALE)/
NON_CONVIENTE/NON_CALCOLABILE (validazione
fallita o risparmio <= 0), sostituzioni multipli
interi di floor(vita_anni) con 1 <= anno < vita
progetto, flusso anno sostituzione = risparmio -
CAPEX_alt + CAPEX_base.

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
domanda termica 20000 MWh/a; ore equivalenti
4000 h; rendimento carbone 0,88; rendimento
torrefatti 0,90; prezzo carbone 90 EUR/MWh;
prezzo torrefatti 55 EUR/MWh; costo carbone 400
EUR/kW_th; costo fisso carbone 500000 EUR;
costo torrefatti 650 EUR/kW_th; costo fisso
torrefatti 800000 EUR; opex carbone 400000
EUR/anno; opex torrefatti 500000 EUR/anno; vita
carbone 25 anni; vita torrefatti 20 anni;
vita di progetto 25 anni; WACC 0,05 (5 %);
tolleranza 0,10 (10 % del |CAPEX_delta|);
fattore carbone 0,34 t/MWh; fattore torrefatti
0,02 t/MWh.

- potenza_th_kw = 5000.0
- fuel_carbone_mwh_a = 22727.272727272728
- fuel_torr_mwh_a = 22222.222222222223
- costo_base_eur_a = 2445454.5454545454
- costo_alt_eur_a = 1722222.2222222222
- risparmio_eur_a = 723232.3232323232
- capex_carbone_eur = 2500000.0
- capex_torr_eur = 4050000.0
- capex_delta_eur = 1550000.0
- anni_sost_carbone = []
- anni_sost_torr = [20]
- co2_evitata_t_a = 7282.828282828284
- van = 7116793.866372468
- tir = 46.598944184859235
- payback = 3
- verdetto = 'CONVIENTE'

Scomposizione: P_th 20000 x 1000 / 4000 =
5000.0 kW; fuel carbone 20000 / 0,88 =
22727.272727272728 MWh/a; fuel torrefatti
20000 / 0,90 = 22222.222222222223 MWh/a;
C_base 22727.272727272728 x 90 + 400000 =
2445454.5454545454 EUR/anno; C_alt
22222.222222222223 x 55 + 500000 =
1722222.2222222222 EUR/anno; risparmio
2445454.5454545454 - 1722222.2222222222 =
723232.3232323232 EUR/anno; CAPEX carbone
5000.0 x 400 + 500000 = 2500000.0 EUR;
CAPEX torrefatti 5000.0 x 650 + 800000 =
4050000.0 EUR; CAPEX_delta 4050000.0 -
2500000.0 = 1550000.0 EUR; sostituzioni:
floor(25) = 25, nessun multiplo < 25 -> []
per il carbone; floor(20) = 20, multipli
20 < 25 -> [20] per i torrefatti; flussi:
anno 0 -1550000.0, anni 1-19 e 21-25
risparmio 723232.3232323232, anno 20
risparmio - CAPEX torrefatti =
-3326767.676767677; VAN 7116793.866372468
a WACC 5 % su 25 anni; TIR
46.598944184859235 % (il tasso che azzera
il VAN dei flussi sopra); payback 3 (il
cumulato diventa positivo all'anno 3:
-1550000.0 + 3 x 723232.3232323232 =
619696.9696969697 >= 0); CO2
22727.272727272728 x 0,34 -
22222.222222222223 x 0,02 =
7282.828282828284 t/anno (positiva e
INFORMATIVA: il carbone risparmiato pesa
molto piu' dei torrefatti bruciati, il cui
fattore e' quasi nullo perche' la CO2
biogenica non conta come fossile); VAN >= 0
-> CONVIENTE.

Formula flussi negli anni di sostituzione
(ESATTA delle tab precedenti, copiata):
flusso_0 = -CAPEX_delta; flusso_t (t >= 1) =
risparmio - (CAPEX_alt se t e' anno di
sostituzione alt) + (CAPEX_base se t e' anno
di sostituzione base).
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
    if (p / "w720_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w720_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w720_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w720_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w720_helpers.py: {missing}")
    return out


_F = _load("mh719_num", "mh719_nneg", "mh719_pos",
           "mh719_int_pos", "mh719_int_nneg",
           "mh719_eta_valido", "mh719_potenza_th",
           "mh719_energia_carbone", "mh719_energia_torr",
           "mh719_costo_annuo", "mh719_risparmio",
           "mh719_capex", "mh719_anni_sostituzione",
           "mh719_flussi", "mh719_van_flussi",
           "mh719_tir_flussi", "mh719_payback_flussi",
           "mh719_verdetto", "mh719_co2_evitata",
           "mh719_valida", "_mh719_neutro",
           "mh719_calcola", "mh719_sensitivita",
           "mh719_csv", "mh719_demo", "demo_calcoli")

TITLE719 = ("🪵🔥 Torrefazione: i pellet torrefatti "
            "sostituiscono il carbone?")

P_TH_DEMO = 5000.0
FUEL_CARBONE_DEMO = 22727.272727272728
FUEL_TORR_DEMO = 22222.222222222223
C_BASE_DEMO = 2445454.5454545454
C_ALT_DEMO = 1722222.2222222222
RISPARMIO_DEMO = 723232.3232323232
CAPEX_CARBONE_DEMO = 2500000.0
CAPEX_TORR_DEMO = 4050000.0
DELTA_DEMO = 1550000.0
CO2_DEMO = 7282.828282828284
VAN_DEMO = 7116793.866372468
TIR_DEMO = 46.598944184859235
PAYBACK_DEMO = 3
VITA_DEMO = 25
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w720_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w720_ui.py").read_text(encoding="utf-8")


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh719_demo"]()
        d.update(kw)
        return _F["mh719_valida"](**d)

    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh719_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh719_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh719_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh719_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh719_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh719_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh719_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh719_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh719_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh719_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh719_int_pos"](20.0, "x") == 20

    def test_int_nneg_accetta_zero(self):
        assert _F["mh719_int_nneg"](0, "x") == 0

    def test_int_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh719_int_nneg"](-1, "x")

    def test_eta_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh719_eta_valido"](0.0, "x")

    def test_eta_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh719_eta_valido"](1.01, "x")

    def test_eta_accetta_uno(self):
        assert _F["mh719_eta_valido"](1.0, "x") == 1.0

    def test_eta_accetta_valore_interno(self):
        assert _F["mh719_eta_valido"](0.90, "x") == 0.90

    def test_eta_torr_sopra_uno_non_valida(self):
        # Brief tab719: anche l'eta dei
        # torrefatti e' un rendimento di caldaia
        # (primo principio), non uno SCOP.
        assert self._val(eta_torr=1.2)["valido"] is False
        assert self._val(eta_carbone=1.2)["valido"] is False

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_domanda_zero_non_valida(self):
        assert self._val(domanda_mwh_a=0.0)["valido"] is False

    def test_domanda_negativa_non_valida(self):
        assert self._val(domanda_mwh_a=-1.0)["valido"] is False

    def test_ore_zero_non_valide(self):
        assert self._val(ore_eq=0.0)["valido"] is False

    def test_eta_zero_non_valide(self):
        assert self._val(eta_carbone=0.0)["valido"] is False
        assert self._val(eta_torr=0.0)["valido"] is False

    def test_eta_negative_non_valide(self):
        assert self._val(eta_carbone=-0.5)["valido"] is False
        assert self._val(eta_torr=-0.5)["valido"] is False

    def test_negativi_non_validi(self):
        for k in ("prezzo_carbone_eur_mwh", "prezzo_torr_eur_mwh",
                  "costo_carbone_eur_kw", "fisso_carbone_eur",
                  "costo_torr_eur_kw", "fisso_torr_eur",
                  "opex_carbone_eur_a", "opex_torr_eur_a",
                  "wacc_frac", "tolleranza_frac",
                  "fattore_carbone_t_mwh", "fattore_torr_t_mwh"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_vite_zero_non_valide(self):
        assert self._val(vita_carbone_anni=0)["valido"] is False
        assert self._val(vita_torr_anni=0)["valido"] is False

    def test_vite_non_intere_non_valide(self):
        assert self._val(vita_carbone_anni=25.5)["valido"] is False
        assert self._val(vita_torr_anni=20.5)["valido"] is False

    def test_vita_progetto_zero_non_valida(self):
        assert self._val(vita_progetto_anni=0)["valido"] is False

    def test_vita_progetto_non_intera_non_valida(self):
        assert self._val(vita_progetto_anni=24.5)["valido"] is False

    def test_tolleranza_negativa_non_valida(self):
        assert self._val(tolleranza_frac=-0.01)["valido"] is False

    def test_tolleranza_sopra_uno_valida_brief(self):
        # Brief tab719: toll >= 0 senza tetto
        # superiore (come le tab precedenti).
        assert self._val(tolleranza_frac=1.5)["valido"] is True

    def test_wacc_senza_tetto_superiore(self):
        assert self._val(wacc_frac=1.5)["valido"] is True

    def test_nan_non_valido(self):
        assert self._val(eta_torr=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(domanda_mwh_a=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(vita_torr_anni=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(eta_torr="0.90")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(prezzo_carbone_eur_mwh=0.0)["valido"] is True
        assert self._val(costo_torr_eur_kw=0.0)["valido"] is True
        assert self._val(fisso_torr_eur=0.0)["valido"] is True
        assert self._val(opex_torr_eur_a=0.0)["valido"] is True
        assert self._val(wacc_frac=0.0)["valido"] is True
        assert self._val(tolleranza_frac=0.0)["valido"] is True
        assert self._val(fattore_torr_t_mwh=0.0)["valido"] is True


class TestFunzioni:
    def test_potenza_th_demo(self):
        assert _F["mh719_potenza_th"](
            20000.0, 4000.0) == pytest.approx(P_TH_DEMO, rel=REL)

    def test_potenza_th_cresce_con_domanda(self):
        assert _F["mh719_potenza_th"](
            40000.0, 4000.0) == pytest.approx(10000.0, rel=REL)

    def test_energia_carbone_demo(self):
        assert _F["mh719_energia_carbone"](
            20000.0, 0.88) == pytest.approx(
            FUEL_CARBONE_DEMO, rel=REL)

    def test_energia_torr_demo(self):
        assert _F["mh719_energia_torr"](
            20000.0, 0.90) == pytest.approx(
            FUEL_TORR_DEMO, rel=REL)

    def test_energia_torr_cresce_con_eta_basso(self):
        assert _F["mh719_energia_torr"](
            20000.0, 0.75) > _F["mh719_energia_torr"](
            20000.0, 0.90)

    def test_costo_annuo_demo(self):
        assert _F["mh719_costo_annuo"](
            FUEL_CARBONE_DEMO, 90.0, 400000.0) == pytest.approx(
            C_BASE_DEMO, rel=REL)
        assert _F["mh719_costo_annuo"](
            FUEL_TORR_DEMO, 55.0, 500000.0) == pytest.approx(
            C_ALT_DEMO, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh719_risparmio"](
            C_BASE_DEMO, C_ALT_DEMO) == pytest.approx(
            RISPARMIO_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh719_risparmio"](
            100000.0, 150000.0) == pytest.approx(-50000.0, rel=REL)

    def test_capex_demo(self):
        assert _F["mh719_capex"](
            P_TH_DEMO, 400.0, 500000.0) == pytest.approx(
            CAPEX_CARBONE_DEMO, rel=REL)
        assert _F["mh719_capex"](
            P_TH_DEMO, 650.0, 800000.0) == pytest.approx(
            CAPEX_TORR_DEMO, rel=REL)

    def test_capex_delta_demo(self):
        delta = _F["mh719_capex"](
            P_TH_DEMO, 650.0, 800000.0) - _F["mh719_capex"](
            P_TH_DEMO, 400.0, 500000.0)
        assert delta == pytest.approx(DELTA_DEMO, rel=REL)

    def test_anni_sostituzione_demo(self):
        assert _F["mh719_anni_sostituzione"](25, 25) == []
        assert _F["mh719_anni_sostituzione"](20, 25) == [20]

    def test_anni_sostituzione_multipli(self):
        assert _F["mh719_anni_sostituzione"](10, 25) == [10, 20]
        assert _F["mh719_anni_sostituzione"](5, 25) == [5, 10, 15, 20]

    def test_anni_sostituzione_floor_non_intero(self):
        # Vita 10,5 anni -> floor 10: anni 10, 20.
        assert _F["mh719_anni_sostituzione"](10.5, 25) == [10, 20]

    def test_anni_sostituzione_sotto_anno_vuota(self):
        assert _F["mh719_anni_sostituzione"](0.5, 25) == []

    def test_anni_sostituzione_esclude_vita_progetto(self):
        assert _F["mh719_anni_sostituzione"](25, 25) == []
        assert _F["mh719_anni_sostituzione"](20, 25) == [20]

    def test_co2_evitata_demo(self):
        assert _F["mh719_co2_evitata"](
            FUEL_CARBONE_DEMO, FUEL_TORR_DEMO, 0.34, 0.02) == \
            pytest.approx(CO2_DEMO, rel=REL)
        assert CO2_DEMO > 0.0

    def test_co2_evitata_puo_essere_negativa(self):
        assert _F["mh719_co2_evitata"](
            5000.0, 10000.0, 0.34, 0.02) == pytest.approx(
            1500.0, rel=REL)
        assert _F["mh719_co2_evitata"](
            5000.0, 10000.0, 0.02, 0.34) == pytest.approx(
            -3300.0, rel=REL)

    def test_co2_evitata_zero_se_fattori_zero(self):
        assert _F["mh719_co2_evitata"](
            FUEL_CARBONE_DEMO, FUEL_TORR_DEMO, 0.0, 0.0) == \
            pytest.approx(0.0, abs=1e-9)

    def test_van_flussi_demo(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 19 + \
            [RISPARMIO_DEMO - CAPEX_TORR_DEMO] + \
            [RISPARMIO_DEMO] * 5
        assert len(flussi) == 26
        assert abs(_F["mh719_van_flussi"](
            flussi, 0.05) - VAN_DEMO) <= 1.0

    def test_van_flussi_tasso_zero(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 25
        atteso = -DELTA_DEMO + RISPARMIO_DEMO * 25
        assert _F["mh719_van_flussi"](
            flussi, 0.0) == pytest.approx(atteso, rel=1e-12)

    def test_van_flussi_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh719_van_flussi"]([100.0, 100.0], -0.01)

    def test_flussi_demo_con_sostituzioni(self):
        flussi = _F["mh719_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CAPEX_CARBONE_DEMO, CAPEX_TORR_DEMO, [], [20], 25)
        assert len(flussi) == 26
        assert flussi[0] == pytest.approx(-DELTA_DEMO, rel=REL)
        assert flussi[1] == pytest.approx(RISPARMIO_DEMO, rel=REL)
        assert flussi[19] == pytest.approx(RISPARMIO_DEMO, rel=REL)
        assert flussi[20] == pytest.approx(
            RISPARMIO_DEMO - CAPEX_TORR_DEMO, rel=REL)
        assert flussi[25] == pytest.approx(RISPARMIO_DEMO, rel=REL)

    def test_flussi_formula_sostituzione_torr(self):
        # Anno di sostituzione torrefatti ->
        # risparmio - CAPEX torrefatti.
        flussi = _F["mh719_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CAPEX_CARBONE_DEMO, CAPEX_TORR_DEMO, [], [20], 25)
        assert flussi[20] == pytest.approx(
            RISPARMIO_DEMO - CAPEX_TORR_DEMO, rel=REL)
        assert flussi[19] == pytest.approx(RISPARMIO_DEMO, rel=REL)

    def test_flussi_formula_sostituzione_carbone(self):
        # Anno di sostituzione carbone ->
        # risparmio + CAPEX carbone.
        flussi = _F["mh719_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CAPEX_CARBONE_DEMO, CAPEX_TORR_DEMO, [10], [], 25)
        assert flussi[10] == pytest.approx(
            RISPARMIO_DEMO + CAPEX_CARBONE_DEMO, rel=REL)

    def test_flussi_formula_sostituzione_entrambi(self):
        # Stesso anno per entrambi i rami: i due
        # termini si sommano.
        flussi = _F["mh719_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CAPEX_CARBONE_DEMO, CAPEX_TORR_DEMO, [10], [10], 25)
        assert flussi[10] == pytest.approx(
            RISPARMIO_DEMO - CAPEX_TORR_DEMO + CAPEX_CARBONE_DEMO,
            rel=REL)

    def test_tir_demo(self):
        flussi = _F["mh719_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CAPEX_CARBONE_DEMO, CAPEX_TORR_DEMO, [], [20], 25)
        tir = _F["mh719_tir_flussi"](flussi)
        assert tir is not None
        assert tir * 100.0 == pytest.approx(TIR_DEMO, rel=1e-9)

    def test_tir_none_tutti_flussi_non_negativi(self):
        assert _F["mh719_tir_flussi"](
            [1000.0] + [100.0] * 10) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh719_tir_flussi"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo_tre(self):
        flussi = _F["mh719_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CAPEX_CARBONE_DEMO, CAPEX_TORR_DEMO, [], [20], 25)
        assert _F["mh719_payback_flussi"](flussi) == PAYBACK_DEMO

    def test_payback_primo_anno_cumulato_non_negativo(self):
        assert _F["mh719_payback_flussi"](
            [-1000.0, 300.0, 300.0, 300.0, 300.0]) == 4

    def test_payback_none_se_mai(self):
        assert _F["mh719_payback_flussi"](
            [-5000000000.0] + [RISPARMIO_DEMO] * 25) is None

    def test_payback_zero_se_cumulato_anno_zero_non_negativo(self):
        assert _F["mh719_payback_flussi"](
            [0.0] + [RISPARMIO_DEMO] * 25) == 0

    def test_verdetto_conviente_demo(self):
        assert _F["mh719_verdetto"](
            VAN_DEMO, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == VERDETTO_DEMO

    def test_verdetto_van_zero_conviente(self):
        assert _F["mh719_verdetto"](
            0.0, DELTA_DEMO, 0.10, RISPARMIO_DEMO) == "CONVIENTE"

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh719_verdetto"](
            -100.0, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh719_verdetto"](
            -0.10 * abs(DELTA_DEMO), DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_oltre_limite(self):
        assert _F["mh719_verdetto"](
            -0.10 * abs(DELTA_DEMO) - 1.0, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_non_positivo(
            self):
        assert _F["mh719_verdetto"](
            1000.0, DELTA_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh719_verdetto"](
            1000.0, DELTA_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_delta_zero_van_positivo_conviente(
            self):
        assert _F["mh719_verdetto"](
            1000.0, 0.0, 0.10, RISPARMIO_DEMO) == "CONVIENTE"

    def test_verdetto_capex_delta_zero_van_negativo_non_conviente(
            self):
        assert _F["mh719_verdetto"](
            -1.0, 0.0, 0.10, RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh719_verdetto"](100.0, DELTA_DEMO, -0.01, RISPARMIO_DEMO)

    def test_verdetto_accetta_tolleranza_sopra_uno(self):
        assert _F["mh719_verdetto"](
            -100.0, DELTA_DEMO, 1.5,
            RISPARMIO_DEMO) == "MARGINALE"


class TestDemo:
    def _bc(self, **kw):
        d = _F["mh719_demo"]()
        d.update(kw)
        return _F["mh719_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["potenza_th_kw"] == pytest.approx(
            P_TH_DEMO, rel=REL)
        assert c["fuel_carbone_mwh_a"] == pytest.approx(
            FUEL_CARBONE_DEMO, rel=REL)
        assert c["fuel_torr_mwh_a"] == pytest.approx(
            FUEL_TORR_DEMO, rel=REL)
        assert c["costo_base_eur_a"] == pytest.approx(
            C_BASE_DEMO, rel=REL)
        assert c["costo_alt_eur_a"] == pytest.approx(
            C_ALT_DEMO, rel=REL)
        assert c["risparmio_eur_a"] == pytest.approx(
            RISPARMIO_DEMO, rel=REL)
        assert c["capex_carbone_eur"] == pytest.approx(
            CAPEX_CARBONE_DEMO, rel=REL)
        assert c["capex_torr_eur"] == pytest.approx(
            CAPEX_TORR_DEMO, rel=REL)
        assert c["capex_delta_eur"] == pytest.approx(
            DELTA_DEMO, rel=REL)
        assert c["anni_sost_carbone"] == []
        assert c["anni_sost_torr"] == [20]
        assert c["co2_evitata_t_a"] == pytest.approx(
            CO2_DEMO, rel=REL)
        assert abs(c["van"] - VAN_DEMO) <= 1.0
        assert abs(c["tir"] - TIR_DEMO) <= 0.01
        assert c["payback"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()[
            "van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()[
            "risparmio_eur_a"] == _F["demo_calcoli"]()[
            "risparmio_eur_a"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        d = _F["mh719_demo"]()
        b = _F["mh719_calcola"](**d)
        coppie = [("potenza_th_kw", P_TH_DEMO),
                  ("fuel_carbone_mwh_a", FUEL_CARBONE_DEMO),
                  ("fuel_torr_mwh_a", FUEL_TORR_DEMO),
                  ("costo_base_eur_a", C_BASE_DEMO),
                  ("costo_alt_eur_a", C_ALT_DEMO),
                  ("risparmio_eur_a", RISPARMIO_DEMO),
                  ("capex_carbone_eur", CAPEX_CARBONE_DEMO),
                  ("capex_torr_eur", CAPEX_TORR_DEMO),
                  ("capex_delta_eur", DELTA_DEMO),
                  ("co2_evitata_t_a", CO2_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert b["anni_sost_carbone"] == []
        assert b["anni_sost_torr"] == [20]
        assert abs(b["van"] - VAN_DEMO) <= 1.0
        assert abs(b["tir"] - TIR_DEMO) <= 0.01
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh719_demo"]()
        assert d["domanda_mwh_a"] == 20000.0
        assert d["ore_eq"] == 4000.0
        assert d["eta_carbone"] == 0.88
        assert d["eta_torr"] == 0.90
        assert d["prezzo_carbone_eur_mwh"] == 90.0
        assert d["prezzo_torr_eur_mwh"] == 55.0
        assert d["costo_carbone_eur_kw"] == 400.0
        assert d["fisso_carbone_eur"] == 500000.0
        assert d["costo_torr_eur_kw"] == 650.0
        assert d["fisso_torr_eur"] == 800000.0
        assert d["opex_carbone_eur_a"] == 400000.0
        assert d["opex_torr_eur_a"] == 500000.0
        assert d["vita_carbone_anni"] == 25
        assert d["vita_torr_anni"] == 20
        assert d["vita_progetto_anni"] == 25
        assert d["wacc_frac"] == 0.05
        assert d["tolleranza_frac"] == 0.10
        assert d["fattore_carbone_t_mwh"] == 0.34
        assert d["fattore_torr_t_mwh"] == 0.02
        assert len(d) == 19

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("potenza_th_kw",
                       "fuel_carbone_mwh_a",
                       "fuel_torr_mwh_a",
                       "costo_base_eur_a",
                       "costo_alt_eur_a",
                       "risparmio_eur_a",
                       "capex_carbone_eur",
                       "capex_torr_eur",
                       "capex_delta_eur",
                       "co2_evitata_t_a", "van"):
            assert repr(c[chiave]) in doc, chiave
        assert repr(c["anni_sost_carbone"]) in doc
        assert repr(c["anni_sost_torr"]) in doc
        assert f"tir = {repr(c['tir'])}" in doc
        assert "payback = 3" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_prezzo_torr_alto_risparmio_negativo(self):
        # Prezzo torrefatti 100 EUR/MWh: C_alt
        # 2722222,22 > C_base 2445454,55 ->
        # risparmio negativo -> dict neutro
        # NON_CALCOLABILE.
        n = self._bc(prezzo_torr_eur_mwh=100.0)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_prezzo_carbone_basso_risparmio_negativo(self):
        # Prezzo carbone 40 EUR/MWh: C_base
        # 1309090,91 < C_alt 1722222,22 ->
        # risparmio negativo -> dict neutro
        # NON_CALCOLABILE.
        n = self._bc(prezzo_carbone_eur_mwh=40.0)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzo_torr_80_non_conviente(self):
        # Prezzo torrefatti 80 EUR/MWh: risparmio
        # 167676,77, VAN -713175,34, TIR -34,60 %,
        # payback 10 -> NON_CONVIENTE.
        n = self._bc(prezzo_torr_eur_mwh=80.0)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            167676.76767676743, rel=REL)
        assert abs(n["van"] - (-713175.3369857273)) <= 1.0
        assert abs(n["tir"] - (-34.59959709201195)) <= 0.01
        assert n["payback"] == 10
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_eta_torr_basso_non_conviente(self):
        # Rendimento torrefatti 0,60: risparmio
        # 112121,21, VAN -1496172,26, TIR -41,93 %,
        # payback 14 -> NON_CONVIENTE.
        n = self._bc(eta_torr=0.60)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            112121.21212121192, rel=REL)
        assert abs(n["van"] - (-1496172.2573215466)) <= 1.0
        assert abs(n["tir"] - (-41.93203178974459)) <= 0.01
        assert n["payback"] == 14
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_costo_torr_marginale(self):
        # Costo torrefatti 1700 EUR/kW_th:
        # CAPEX_delta 6800000, VAN -111875,92 entro
        # la tolleranza 680000 -> MARGINALE.
        n = self._bc(costo_torr_eur_kw=1700.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            6800000.0, rel=REL)
        assert abs(n["van"] - (-111875.91871078161)) <= 1.0
        assert abs(n["tir"] - 4.687200134730627) <= 0.01
        assert n["payback"] == 10
        assert n["verdetto"] == "MARGINALE"

    def test_costo_torr_alto_non_conviente(self):
        # Costo torrefatti 2000 EUR/kW_th:
        # CAPEX_delta 8300000, VAN -2177210,14,
        # TIR -19,41 %, payback 12 -> NON_CONVIENTE.
        n = self._bc(costo_torr_eur_kw=2000.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            8300000.0, rel=REL)
        assert abs(n["van"] - (-2177210.1430202825)) <= 1.0
        assert abs(n["tir"] - (-19.40805433155225)) <= 0.01
        assert n["payback"] == 12
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_eta_torr_medio_conviente(self):
        # Rendimento torrefatti 0,75: risparmio
        # 478787,88, VAN 3671607,42, TIR 30,46 %,
        # payback 4 -> CONVIENTE.
        n = self._bc(eta_torr=0.75)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            478787.87878787867, rel=REL)
        assert abs(n["van"] - 3671607.4168948624) <= 1.0
        assert abs(n["tir"] - 30.459205166234206) <= 0.01
        assert n["payback"] == 4
        assert n["verdetto"] == "CONVIENTE"

    def test_vite_corte_sostituzioni_entrambi(self):
        # Vita 10 anni per entrambi: sost [10, 20]
        # per entrambi; flusso anno 10 = risparmio
        # - CAPEX torrefatti + CAPEX carbone;
        # VAN 7107452,03, TIR 45,56 %, payback 3
        # -> CONVIENTE.
        n = self._bc(vita_carbone_anni=10, vita_torr_anni=10)
        assert n["valid"] is True
        assert n["anni_sost_carbone"] == [10, 20]
        assert n["anni_sost_torr"] == [10, 20]
        assert n["df_flussi"]["Flusso (€/anno)"].iloc[10] == \
            pytest.approx(-826767.6767676771, rel=REL)
        assert abs(n["van"] - 7107452.030566792) <= 1.0
        assert abs(n["tir"] - 45.56448743234812) <= 0.01
        assert n["payback"] == 3
        assert n["verdetto"] == "CONVIENTE"

    def test_vite_diverse_sostituzioni(self):
        # Vita carbone 12 anni, torrefatti 8 anni:
        # sost carbone [12, 24], torrefatti
        # [8, 16, 24]; VAN 4958133,48 -> CONVIENTE.
        n = self._bc(vita_carbone_anni=12, vita_torr_anni=8)
        assert n["anni_sost_carbone"] == [12, 24]
        assert n["anni_sost_torr"] == [8, 16, 24]
        assert abs(n["van"] - 4958133.476232559) <= 1.0
        assert n["verdetto"] == "CONVIENTE"

    def test_domanda_zero_neutro(self):
        n = self._bc(domanda_mwh_a=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_sopra_uno_neutro(self):
        n = self._bc(eta_torr=1.2)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_carbone_zero_neutro(self):
        n = self._bc(eta_carbone=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_progetto_zero_neutro(self):
        n = self._bc(vita_progetto_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_negativo_neutro(self):
        n = self._bc(wacc_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_negativa_neutro(self):
        n = self._bc(tolleranza_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(eta_torr=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(domanda_mwh_a=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(vita_torr_anni=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_zero_calcolabile(self):
        # WACC 0: VAN = somma flussi =
        # -1550000 + 723232,32 x 25 - 4050000 =
        # 12480808,08.
        n = self._bc(wacc_frac=0.0)
        assert n["van"] == pytest.approx(
            12480808.080808075, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh719_neutro"]()
        assert n["valid"] is False
        assert n["errore"] == ""
        assert list(n["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(n["df_flussi"]) == 0
        assert list(n["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(n["df_tabella"]) == 0

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh719_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "domanda_mwh_a", "ore_eq",
                       "eta_carbone", "eta_torr",
                       "potenza_th_kw",
                       "fuel_carbone_mwh_a",
                       "fuel_torr_mwh_a",
                       "costo_base_eur_a",
                       "costo_alt_eur_a",
                       "risparmio_eur_a",
                       "capex_carbone_eur",
                       "capex_torr_eur",
                       "capex_delta_eur",
                       "anni_sost_carbone",
                       "anni_sost_torr",
                       "co2_evitata_t_a",
                       "van", "tir", "payback",
                       "verdetto", "df_flussi",
                       "df_tabella"):
            assert chiave in n, chiave
        assert n["errore"] == "errore di prova"
        assert n["tir"] is None

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert b["valid"] is True
        assert list(b["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(b["df_tabella"]) == 27
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Potenza termica (kW)" in voci
        assert "Carbone consumato (MWh/a)" in voci
        assert "Torrefatti consumati (MWh/a)" in voci
        assert "Costo annuo baseline (EUR/anno)" in voci
        assert "Costo annuo alternativa (EUR/anno)" in voci
        assert "Risparmio annuo (EUR/anno)" in voci
        assert "CAPEX torrefatti (EUR)" in voci
        assert "CAPEX delta (EUR)" in voci
        assert "CO2 evitata (t/anno)" in voci
        assert "VAN (EUR)" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(b["df_flussi"]) == VITA_DEMO + 1
        assert b["df_flussi"]["Flusso (€/anno)"].iloc[0] == \
            pytest.approx(-DELTA_DEMO, rel=REL)
        assert b["df_flussi"]["Flusso (€/anno)"].iloc[1] == \
            pytest.approx(RISPARMIO_DEMO, rel=REL)
        assert b["df_flussi"]["Flusso (€/anno)"].iloc[20] == \
            pytest.approx(RISPARMIO_DEMO - CAPEX_TORR_DEMO,
                          rel=REL)


class TestSensitivita:
    def _ing(self):
        return _F["mh719_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh719_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.9", "x1.0", "x1.1"]
        assert list(s.index) == ["x0.9", "x1.0", "x1.1"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh719_sensitivita"](self._ing())
        assert abs(s.loc["x1.0", "x1.0"] - VAN_DEMO) <= 1.0

    def test_sensitivita_crescente_con_eta_torr(self):
        s = _F["mh719_sensitivita"](self._ing())
        for colonna in ("x0.9", "x1.0", "x1.1"):
            assert s.loc["x0.9", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.1", colonna]

    def test_sensitivita_decrescente_con_prezzo_torr(self):
        # Un prezzo dei torrefatti piu' alto
        # alza il costo dell'alternativa e
        # riduce il risparmio.
        s = _F["mh719_sensitivita"](self._ing())
        for riga in ("x0.9", "x1.0", "x1.1"):
            assert s.loc[riga, "x0.9"] > \
                s.loc[riga, "x1.0"] > \
                s.loc[riga, "x1.1"]

    def test_sensitivita_nessuna_colonna_degenere(self):
        s = _F["mh719_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_nessuna_colonna_costante(self):
        s = _F["mh719_sensitivita"](self._ing())
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3

    def test_sensitivita_angoli(self):
        s = _F["mh719_sensitivita"](self._ing())
        assert abs(s.loc["x0.9", "x0.9"] - 7116793.866372472) <= 1.0
        assert abs(s.loc["x0.9", "x1.1"] - 3288808.9225084633) <= 1.0
        assert abs(s.loc["x1.1", "x0.9"] - 10248781.547715748) <= 1.0
        assert abs(s.loc["x1.1", "x1.1"] - 7116793.866372468) <= 1.0

    def test_sensitivita_diagonale_simmetrica(self):
        # Rendimento e prezzo variati dello stesso
        # fattore si compensano (fuel x prezzo
        # invariato): la diagonale x0.9/x0.9 e
        # x1.1/x1.1 coincide col centro.
        s = _F["mh719_sensitivita"](self._ing())
        assert abs(s.loc["x0.9", "x0.9"] - VAN_DEMO) <= 1.0
        assert abs(s.loc["x1.1", "x1.1"] - VAN_DEMO) <= 1.0

    def test_sensitivita_con_sostituzioni_ricalcolate(self):
        # Con vite 10 anni per entrambi la griglia
        # deve includere le sostituzioni anni 10
        # e 20: il centro deve coincidere col VAN
        # del caso con vite 10 anni.
        ing = self._ing()
        ing["vita_carbone_anni"] = 10
        ing["vita_torr_anni"] = 10
        s = _F["mh719_sensitivita"](ing)
        assert abs(s.loc["x1.0", "x1.0"] - 7107452.030566792) <= 1.0


class TestCsv:
    def _ing(self):
        return _F["mh719_demo"]()

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh719_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 33

    def test_csv_contiene_verdetto_e_risparmio(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh719_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "risparmio_eur_a" in txt
        assert "costo_base_eur_a" in txt
        assert "costo_alt_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "domanda_mwh_a" in txt
        assert "potenza_th_kw" in txt
        assert "co2_evitata_t_a" in txt
        assert "eta_torr" in txt
        assert "capex_delta_eur" in txt
        assert "fisso_torr_eur" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh719_csv"](bc, self._ing())
        assert f"risparmio_eur_a;{bc['risparmio_eur_a']}" in txt
        assert f"costo_base_eur_a;{bc['costo_base_eur_a']}" in txt
        assert "domanda_mwh_a;20000.0" in txt
        assert "opex_torr_eur_a;500000.0" in txt
        assert f"capex_delta_eur;{bc['capex_delta_eur']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def719["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def719\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 19, ui_keys
        demo_keys = set(_F["mh719_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh719_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh719_demo():")
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
        ui_keys = set(re.findall(r'_def719\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W720 (26/10/2026) - tab719' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh719_num", "mh719_nneg", "mh719_pos",
                     "mh719_int_pos", "mh719_int_nneg",
                     "mh719_eta_valido", "mh719_potenza_th",
                     "mh719_energia_carbone", "mh719_energia_torr",
                     "mh719_costo_annuo", "mh719_risparmio",
                     "mh719_capex", "mh719_anni_sostituzione",
                     "mh719_flussi", "mh719_van_flussi",
                     "mh719_tir_flussi", "mh719_payback_flussi",
                     "mh719_verdetto", "mh719_co2_evitata",
                     "mh719_valida", "_mh719_neutro",
                     "mh719_calcola", "mh719_sensitivita",
                     "mh719_csv", "mh719_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_nessun_identificatore_futura_tab(self):
        # I frammenti nuovi usano solo mh719 /
        # tab719 / st719: nessun identificatore
        # della numerazione successiva.
        assert "mh720" not in _helpers_src()
        assert "mh720" not in _ui_src()
        assert "st720" not in _ui_src()
        assert "tab720" not in _ui_src()

    def test_nessun_residuo_tab_precedente(self):
        # Niente residui della tab precedente
        # (mh718 / tab718 / st718) in helpers/UI:
        # il test puo' citare tab718 come tab
        # precedente, i frammenti no.
        assert "mh718" not in _helpers_src()
        assert "mh718" not in _ui_src()
        assert "st718" not in _ui_src()
        assert "tab718" not in _helpers_src()
        assert "tab718" not in _ui_src()

    def test_chain_riferimento_tab_precedente(self):
        # Questo file test fa riferimento alla
        # tab precedente tab718 (acqua di mare)
        # come punto di confronto e la nuova tab
        # e' tab719.
        src = Path(__file__).read_text(encoding="utf-8")
        assert "tab718" in src
        assert "tab719" in src
        assert _ui_src().startswith("    with tab719:")

    def test_helpers_parse_ast(self):
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w720_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE719) == 1

    def test_blocco_with_tab719(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab719:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE719

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st719_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 24, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st719_") for k in keys)

    def test_chiavi_st_input_sono_20(self):
        """Le 20 chiavi di input/bottone (19 input +
        bottone calcola) sono tutte presenti; le
        altre 4 sono solo chiavi di
        visualizzazione (fig, heatmap, flussi, CSV)."""
        keys = re.findall(r'key="(st719_[a-z0-9_]+)"', _ui_src())
        attese = ["st719_domanda", "st719_ore",
                  "st719_eta_carbone", "st719_eta_torr",
                  "st719_p_carbone", "st719_p_torr",
                  "st719_c_carbone", "st719_fisso_carbone",
                  "st719_c_torr", "st719_fisso_torr",
                  "st719_opex_carbone", "st719_opex_torr",
                  "st719_vita_carbone", "st719_vita_torr",
                  "st719_vita_progetto", "st719_wacc",
                  "st719_tolleranza", "st719_f_carbone",
                  "st719_f_torr", "st719_calcola"]
        assert len(attese) == 20
        for k in attese:
            assert k in keys, k

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg719" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg719") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg719")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Potenza termica (kW)" in src
        assert "Risparmio annuo (€/anno)" in src
        assert "VAN (€)" in src
        assert "CO2 evitata (t/anno)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_presente(self):
        src = _ui_src().lower()
        assert "torrefazione" in src
        assert "torrefatti" in src
        assert "carbone" in src
        assert "idrofob" in src
        assert "biogenica" in src

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Costo annuo baseline (caldaia a carbone)" in src
        assert "Costo annuo alternativa (caldaia a torrefatti)" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh719_csv" in src
        assert "torrefazione_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh719_sensitivita" in src
        assert "Heatmap" in src
        assert "Rendimento torrefatti" in src
        assert "Prezzo torrefatti" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st719_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W720 (26/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab719:")
