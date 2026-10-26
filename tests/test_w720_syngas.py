"""Test tab720 "🌿🔥 Syngas da gassificazione: la biomassa diventa gas combustibile?"

Tab precedente tab719 (torrefazione, w720);
nuova tab tab720 (syngas, w721). La tab720
replica ESATTAMENTE la semantica economica
delle tab650-719: flussi [-CAPEX_delta,
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
domanda termica 15000 MWh/a; ore equivalenti
4000 h; rendimento gas 0,90; rendimento
gassificazione 0,75; rendimento caldaia a
syngas 0,88; prezzo gas 80 EUR/MWh; prezzo
biomassa 35 EUR/MWh; costo gas 300 EUR/kW_th;
costo fisso gas 300000 EUR; costo syngas 900
EUR/kW_th; costo fisso syngas 700000 EUR;
opex gas 250000 EUR/anno; opex syngas 400000
EUR/anno; vita gas 20 anni; vita syngas 15
anni; vita di progetto 20 anni; WACC 0,05
(5 %); tolleranza 0,10 (10 % del
|CAPEX_delta|); fattore gas 0,20 t/MWh;
fattore biomassa 0,02 t/MWh.

- potenza_th_kw = 3750.0
- fuel_gas_mwh_a = 16666.666666666668
- feed_bio_mwh_a = 22727.272727272728
- costo_base_eur_a = 1583333.3333333335
- costo_alt_eur_a = 1195454.5454545454
- risparmio_eur_a = 387878.7878787881
- capex_gas_eur = 1425000.0
- capex_syn_eur = 4075000.0
- capex_delta_eur = 2650000.0
- anni_sost_gas = []
- anni_sost_syn = [15]
- co2_evitata_t_a = 2878.7878787878794
- van = 223682.36723420172
- tir = 6.84262258776374
- payback = 7
- verdetto = 'CONVIENTE'

Scomposizione: P_th 15000 x 1000 / 4000 =
3750.0 kW; fuel gas 15000 / 0,90 =
16666.666666666668 MWh/a; feedstock biomassa
15000 / (0,75 x 0,88) = 15000 / 0,66 =
22727.272727272728 MWh PCI/a; C_base
16666.666666666668 x 80 + 250000 =
1583333.3333333335 EUR/anno; C_alt
22727.272727272728 x 35 + 400000 =
1195454.5454545454 EUR/anno; risparmio
1583333.3333333335 - 1195454.5454545454 =
387878.7878787881 EUR/anno; CAPEX gas
3750.0 x 300 + 300000 = 1425000.0 EUR;
CAPEX syngas 3750.0 x 900 + 700000 =
4075000.0 EUR; CAPEX_delta 4075000.0 -
1425000.0 = 2650000.0 EUR; sostituzioni:
floor(20) = 20, nessun multiplo < 20 -> []
per il gas; floor(15) = 15, multipli
15 < 20 -> [15] per il syngas; flussi:
anno 0 -2650000.0, anni 1-14 e 16-20
risparmio 387878.7878787881, anno 15
risparmio - CAPEX syngas =
-3687121.212121212; VAN 223682.36723420172
a WACC 5 % su 20 anni; TIR
6.84262258776374 % (il tasso che azzera
il VAN dei flussi sopra); payback 7 (il
cumulato diventa positivo all'anno 7:
-2650000.0 + 7 x 387878.7878787881 =
65151.515151516534 >= 0); CO2
16666.666666666668 x 0,20 -
22727.272727272728 x 0,02 =
2878.7878787878794 t/anno (positiva e
INFORMATIVA: il gas risparmiato pesa piu'
della biomassa bruciata, il cui fattore e'
quasi nullo perche' la CO2 biogenica non
conta come fossile); VAN >= 0 -> CONVIENTE,
ma di misura (VAN = 8,4 % del CAPEX delta).

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
    if (p / "w721_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w721_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w721_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w721_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w721_helpers.py: {missing}")
    return out


_F = _load("mh720_num", "mh720_nneg", "mh720_pos",
           "mh720_int_pos", "mh720_int_nneg",
           "mh720_eta_valido", "mh720_potenza_th",
           "mh720_energia_gas", "mh720_energia_bio",
           "mh720_costo_annuo", "mh720_risparmio",
           "mh720_capex", "mh720_anni_sostituzione",
           "mh720_flussi", "mh720_van_flussi",
           "mh720_tir_flussi", "mh720_payback_flussi",
           "mh720_verdetto", "mh720_co2_evitata",
           "mh720_valida", "_mh720_neutro",
           "mh720_calcola", "mh720_sensitivita",
           "mh720_csv", "mh720_demo", "demo_calcoli")

TITLE720 = ("🌿🔥 Syngas da gassificazione: la biomassa "
            "diventa gas combustibile?")

P_TH_DEMO = 3750.0
FUEL_GAS_DEMO = 16666.666666666668
FEED_BIO_DEMO = 22727.272727272728
C_BASE_DEMO = 1583333.3333333335
C_ALT_DEMO = 1195454.5454545454
RISPARMIO_DEMO = 387878.7878787881
CAPEX_GAS_DEMO = 1425000.0
CAPEX_SYN_DEMO = 4075000.0
DELTA_DEMO = 2650000.0
CO2_DEMO = 2878.7878787878794
VAN_DEMO = 223682.3672342016
TIR_DEMO = 6.842622587763303
PAYBACK_DEMO = 7
VITA_DEMO = 20
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w721_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w721_ui.py").read_text(encoding="utf-8")


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh720_demo"]()
        d.update(kw)
        return _F["mh720_valida"](**d)

    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh720_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh720_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh720_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh720_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh720_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh720_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh720_pos"](0.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh720_int_pos"](2.5, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh720_int_pos"](20.0, "x") == 20

    def test_int_nneg_accetta_zero(self):
        assert _F["mh720_int_nneg"](0, "x") == 0

    def test_eta_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh720_eta_valido"](0.0, "x")

    def test_eta_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh720_eta_valido"](1.01, "x")

    def test_eta_accetta_uno(self):
        assert _F["mh720_eta_valido"](1.0, "x") == 1.0

    def test_eta_gassif_e_cald_syn_sopra_uno_non_validi(self):
        assert self._val(eta_gassif=1.2)["valido"] is False
        assert self._val(eta_cald_syn=1.2)["valido"] is False
        assert self._val(eta_gas=1.2)["valido"] is False

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_domanda_zero_non_valida(self):
        assert self._val(domanda_mwh_a=0.0)["valido"] is False

    def test_ore_zero_non_valide(self):
        assert self._val(ore_eq=0.0)["valido"] is False

    def test_eta_zero_non_valide(self):
        assert self._val(eta_gas=0.0)["valido"] is False
        assert self._val(eta_gassif=0.0)["valido"] is False
        assert self._val(eta_cald_syn=0.0)["valido"] is False

    def test_negativi_non_validi(self):
        for k in ("prezzo_gas_eur_mwh", "prezzo_bio_eur_mwh",
                  "costo_gas_eur_kw", "fisso_gas_eur",
                  "costo_syn_eur_kw", "fisso_syn_eur",
                  "opex_gas_eur_a", "opex_syn_eur_a",
                  "wacc_frac", "tolleranza_frac",
                  "fattore_gas_t_mwh", "fattore_bio_t_mwh"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_vite_zero_non_valide(self):
        assert self._val(vita_gas_anni=0)["valido"] is False
        assert self._val(vita_syn_anni=0)["valido"] is False

    def test_vite_non_intere_non_valide(self):
        assert self._val(vita_gas_anni=20.5)["valido"] is False
        assert self._val(vita_syn_anni=15.5)["valido"] is False

    def test_vita_progetto_zero_non_valida(self):
        assert self._val(vita_progetto_anni=0)["valido"] is False

    def test_tolleranza_sopra_uno_valida_brief(self):
        assert self._val(tolleranza_frac=1.5)["valido"] is True

    def test_wacc_senza_tetto_superiore(self):
        assert self._val(wacc_frac=1.5)["valido"] is True

    def test_nan_non_valido(self):
        assert self._val(eta_gassif=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(domanda_mwh_a=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(vita_syn_anni=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(eta_gassif="0.75")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(prezzo_gas_eur_mwh=0.0)["valido"] is True
        assert self._val(costo_syn_eur_kw=0.0)["valido"] is True
        assert self._val(fisso_syn_eur=0.0)["valido"] is True
        assert self._val(opex_syn_eur_a=0.0)["valido"] is True
        assert self._val(wacc_frac=0.0)["valido"] is True
        assert self._val(tolleranza_frac=0.0)["valido"] is True
        assert self._val(fattore_bio_t_mwh=0.0)["valido"] is True


class TestFunzioni:
    def test_potenza_th_demo(self):
        assert _F["mh720_potenza_th"](
            15000.0, 4000.0) == pytest.approx(P_TH_DEMO, rel=REL)

    def test_energia_gas_demo(self):
        assert _F["mh720_energia_gas"](
            15000.0, 0.90) == pytest.approx(
            FUEL_GAS_DEMO, rel=REL)

    def test_energia_bio_demo_prodotto_rendimenti(self):
        # 15000 / (0,75 x 0,88) = 15000 / 0,66.
        assert _F["mh720_energia_bio"](
            15000.0, 0.75, 0.88) == pytest.approx(
            FEED_BIO_DEMO, rel=REL)
        assert _F["mh720_energia_bio"](
            15000.0, 0.75, 0.88) == pytest.approx(
            15000.0 / 0.66, rel=REL)

    def test_energia_bio_cresce_con_eta_basso(self):
        assert _F["mh720_energia_bio"](
            15000.0, 0.55, 0.88) > _F["mh720_energia_bio"](
            15000.0, 0.75, 0.88)

    def test_costo_annuo_demo(self):
        assert _F["mh720_costo_annuo"](
            FUEL_GAS_DEMO, 80.0, 250000.0) == pytest.approx(
            C_BASE_DEMO, rel=REL)
        assert _F["mh720_costo_annuo"](
            FEED_BIO_DEMO, 35.0, 400000.0) == pytest.approx(
            C_ALT_DEMO, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh720_risparmio"](
            C_BASE_DEMO, C_ALT_DEMO) == pytest.approx(
            RISPARMIO_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh720_risparmio"](
            100000.0, 150000.0) == pytest.approx(-50000.0, rel=REL)

    def test_capex_demo(self):
        assert _F["mh720_capex"](
            P_TH_DEMO, 300.0, 300000.0) == pytest.approx(
            CAPEX_GAS_DEMO, rel=REL)
        assert _F["mh720_capex"](
            P_TH_DEMO, 900.0, 700000.0) == pytest.approx(
            CAPEX_SYN_DEMO, rel=REL)

    def test_capex_delta_demo_non_clampato(self):
        delta = _F["mh720_capex"](
            P_TH_DEMO, 900.0, 700000.0) - _F["mh720_capex"](
            P_TH_DEMO, 300.0, 300000.0)
        assert delta == pytest.approx(DELTA_DEMO, rel=REL)
        # Delta negativo possibile: syngas piu' economico del gas.
        assert _F["mh720_capex"](
            P_TH_DEMO, 100.0, 0.0) - _F["mh720_capex"](
            P_TH_DEMO, 300.0, 300000.0) < 0.0

    def test_anni_sostituzione_demo(self):
        assert _F["mh720_anni_sostituzione"](20, 20) == []
        assert _F["mh720_anni_sostituzione"](15, 20) == [15]

    def test_anni_sostituzione_multipli(self):
        assert _F["mh720_anni_sostituzione"](10, 20) == [10]
        assert _F["mh720_anni_sostituzione"](5, 20) == [5, 10, 15]

    def test_anni_sostituzione_floor_non_intero(self):
        assert _F["mh720_anni_sostituzione"](10.5, 20) == [10]

    def test_anni_sostituzione_sotto_anno_vuota(self):
        assert _F["mh720_anni_sostituzione"](0.5, 20) == []

    def test_anni_sostituzione_esclude_vita_progetto(self):
        assert _F["mh720_anni_sostituzione"](20, 20) == []
        assert _F["mh720_anni_sostituzione"](15, 20) == [15]

    def test_co2_evitata_demo(self):
        assert _F["mh720_co2_evitata"](
            FUEL_GAS_DEMO, FEED_BIO_DEMO, 0.20, 0.02) == \
            pytest.approx(CO2_DEMO, rel=REL)
        assert CO2_DEMO > 0.0

    def test_co2_evitata_puo_essere_negativa(self):
        assert _F["mh720_co2_evitata"](
            5000.0, 10000.0, 0.02, 0.20) == pytest.approx(
            -1900.0, rel=REL)

    def test_co2_evitata_zero_se_fattori_zero(self):
        assert _F["mh720_co2_evitata"](
            FUEL_GAS_DEMO, FEED_BIO_DEMO, 0.0, 0.0) == \
            pytest.approx(0.0, abs=1e-9)

    def test_van_flussi_demo(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 14 + \
            [RISPARMIO_DEMO - CAPEX_SYN_DEMO] + \
            [RISPARMIO_DEMO] * 5
        assert len(flussi) == 21
        assert abs(_F["mh720_van_flussi"](
            flussi, 0.05) - VAN_DEMO) <= 1.0

    def test_van_flussi_tasso_zero(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 20
        atteso = -DELTA_DEMO + RISPARMIO_DEMO * 20
        assert _F["mh720_van_flussi"](
            flussi, 0.0) == pytest.approx(atteso, rel=1e-12)

    def test_van_flussi_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh720_van_flussi"]([100.0, 100.0], -0.01)

    def test_flussi_demo_con_sostituzioni(self):
        flussi = _F["mh720_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CAPEX_GAS_DEMO, CAPEX_SYN_DEMO, [], [15], 20)
        assert len(flussi) == 21
        assert flussi[0] == pytest.approx(-DELTA_DEMO, rel=REL)
        assert flussi[1] == pytest.approx(RISPARMIO_DEMO, rel=REL)
        assert flussi[14] == pytest.approx(RISPARMIO_DEMO, rel=REL)
        assert flussi[15] == pytest.approx(
            RISPARMIO_DEMO - CAPEX_SYN_DEMO, rel=REL)
        assert flussi[20] == pytest.approx(RISPARMIO_DEMO, rel=REL)

    def test_flussi_formula_sostituzione_gas(self):
        flussi = _F["mh720_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CAPEX_GAS_DEMO, CAPEX_SYN_DEMO, [10], [], 20)
        assert flussi[10] == pytest.approx(
            RISPARMIO_DEMO + CAPEX_GAS_DEMO, rel=REL)

    def test_flussi_formula_sostituzione_entrambi(self):
        flussi = _F["mh720_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CAPEX_GAS_DEMO, CAPEX_SYN_DEMO, [10], [10], 20)
        assert flussi[10] == pytest.approx(
            RISPARMIO_DEMO - CAPEX_SYN_DEMO + CAPEX_GAS_DEMO,
            rel=REL)

    def test_tir_demo(self):
        flussi = _F["mh720_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CAPEX_GAS_DEMO, CAPEX_SYN_DEMO, [], [15], 20)
        tir = _F["mh720_tir_flussi"](flussi)
        assert tir is not None
        assert tir * 100.0 == pytest.approx(TIR_DEMO, rel=1e-9)

    def test_tir_none_tutti_flussi_non_negativi(self):
        assert _F["mh720_tir_flussi"](
            [1000.0] + [100.0] * 10) is None

    def test_tir_none_nessun_cambio_segno_negativo(self):
        # Tutti i flussi <= 0: nessun tasso azzera il VAN.
        assert _F["mh720_tir_flussi"](
            [-1000.0] + [-100.0] * 10) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh720_tir_flussi"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo_sette(self):
        flussi = _F["mh720_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CAPEX_GAS_DEMO, CAPEX_SYN_DEMO, [], [15], 20)
        assert _F["mh720_payback_flussi"](flussi) == PAYBACK_DEMO

    def test_payback_none_se_mai(self):
        assert _F["mh720_payback_flussi"](
            [-5000000000.0] + [RISPARMIO_DEMO] * 20) is None

    def test_payback_zero_se_cumulato_anno_zero_non_negativo(self):
        assert _F["mh720_payback_flussi"](
            [0.0] + [RISPARMIO_DEMO] * 20) == 0

    def test_verdetto_conviente_demo(self):
        assert _F["mh720_verdetto"](
            VAN_DEMO, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == VERDETTO_DEMO

    def test_verdetto_van_zero_conviente(self):
        assert _F["mh720_verdetto"](
            0.0, DELTA_DEMO, 0.10, RISPARMIO_DEMO) == "CONVIENTE"

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh720_verdetto"](
            -100.0, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh720_verdetto"](
            -0.10 * abs(DELTA_DEMO), DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_oltre_limite(self):
        assert _F["mh720_verdetto"](
            -0.10 * abs(DELTA_DEMO) - 1.0, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_non_positivo(
            self):
        assert _F["mh720_verdetto"](
            1000.0, DELTA_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh720_verdetto"](
            1000.0, DELTA_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_delta_zero_van_positivo_conviente(
            self):
        assert _F["mh720_verdetto"](
            1000.0, 0.0, 0.10, RISPARMIO_DEMO) == "CONVIENTE"

    def test_verdetto_capex_delta_zero_van_negativo_non_conviente(
            self):
        assert _F["mh720_verdetto"](
            -1.0, 0.0, 0.10, RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh720_verdetto"](100.0, DELTA_DEMO, -0.01, RISPARMIO_DEMO)


class TestDemo:
    def _bc(self, **kw):
        d = _F["mh720_demo"]()
        d.update(kw)
        return _F["mh720_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["potenza_th_kw"] == pytest.approx(
            P_TH_DEMO, rel=REL)
        assert c["fuel_gas_mwh_a"] == pytest.approx(
            FUEL_GAS_DEMO, rel=REL)
        assert c["feed_bio_mwh_a"] == pytest.approx(
            FEED_BIO_DEMO, rel=REL)
        assert c["costo_base_eur_a"] == pytest.approx(
            C_BASE_DEMO, rel=REL)
        assert c["costo_alt_eur_a"] == pytest.approx(
            C_ALT_DEMO, rel=REL)
        assert c["risparmio_eur_a"] == pytest.approx(
            RISPARMIO_DEMO, rel=REL)
        assert c["capex_gas_eur"] == pytest.approx(
            CAPEX_GAS_DEMO, rel=REL)
        assert c["capex_syn_eur"] == pytest.approx(
            CAPEX_SYN_DEMO, rel=REL)
        assert c["capex_delta_eur"] == pytest.approx(
            DELTA_DEMO, rel=REL)
        assert c["anni_sost_gas"] == []
        assert c["anni_sost_syn"] == [15]
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
        d = _F["mh720_demo"]()
        b = _F["mh720_calcola"](**d)
        coppie = [("potenza_th_kw", P_TH_DEMO),
                  ("fuel_gas_mwh_a", FUEL_GAS_DEMO),
                  ("feed_bio_mwh_a", FEED_BIO_DEMO),
                  ("costo_base_eur_a", C_BASE_DEMO),
                  ("costo_alt_eur_a", C_ALT_DEMO),
                  ("risparmio_eur_a", RISPARMIO_DEMO),
                  ("capex_gas_eur", CAPEX_GAS_DEMO),
                  ("capex_syn_eur", CAPEX_SYN_DEMO),
                  ("capex_delta_eur", DELTA_DEMO),
                  ("co2_evitata_t_a", CO2_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert b["anni_sost_gas"] == []
        assert b["anni_sost_syn"] == [15]
        assert abs(b["van"] - VAN_DEMO) <= 1.0
        assert abs(b["tir"] - TIR_DEMO) <= 0.01
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh720_demo"]()
        assert d["domanda_mwh_a"] == 15000.0
        assert d["ore_eq"] == 4000.0
        assert d["eta_gas"] == 0.90
        assert d["eta_gassif"] == 0.75
        assert d["eta_cald_syn"] == 0.88
        assert d["prezzo_gas_eur_mwh"] == 80.0
        assert d["prezzo_bio_eur_mwh"] == 35.0
        assert d["costo_gas_eur_kw"] == 300.0
        assert d["fisso_gas_eur"] == 300000.0
        assert d["costo_syn_eur_kw"] == 900.0
        assert d["fisso_syn_eur"] == 700000.0
        assert d["opex_gas_eur_a"] == 250000.0
        assert d["opex_syn_eur_a"] == 400000.0
        assert d["vita_gas_anni"] == 20
        assert d["vita_syn_anni"] == 15
        assert d["vita_progetto_anni"] == 20
        assert d["wacc_frac"] == 0.05
        assert d["tolleranza_frac"] == 0.10
        assert d["fattore_gas_t_mwh"] == 0.20
        assert d["fattore_bio_t_mwh"] == 0.02
        assert len(d) == 20

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("potenza_th_kw",
                       "fuel_gas_mwh_a",
                       "feed_bio_mwh_a",
                       "costo_base_eur_a",
                       "costo_alt_eur_a",
                       "risparmio_eur_a",
                       "capex_gas_eur",
                       "capex_syn_eur",
                       "capex_delta_eur",
                       "co2_evitata_t_a", "van"):
            assert repr(c[chiave]) in doc, chiave
        assert repr(c["anni_sost_gas"]) in doc
        assert repr(c["anni_sost_syn"]) in doc
        assert f"tir = {repr(c['tir'])}" in doc
        assert "payback = 7" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_prezzo_bio_alto_risparmio_negativo(self):
        # Prezzo biomassa 60 EUR/MWh: C_alt
        # 1763636,36 > C_base 1583333,33 ->
        # risparmio -180303,03 -> dict neutro
        # NON_CALCOLABILE.
        n = self._bc(prezzo_bio_eur_mwh=60.0)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_prezzo_gas_basso_risparmio_negativo(self):
        # Prezzo gas 40 EUR/MWh: C_base
        # 916666,67 < C_alt 1195454,55 ->
        # risparmio negativo -> dict neutro.
        n = self._bc(prezzo_gas_eur_mwh=40.0)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_prezzo_bio_50_non_conviente(self):
        # Prezzo biomassa 50 EUR/MWh: risparmio
        # 46969,70, VAN -4024798,43, TIR -53,60 %,
        # payback None -> NON_CONVIENTE.
        n = self._bc(prezzo_bio_eur_mwh=50.0)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            46969.69696969702, rel=REL)
        assert abs(n["van"] - (-4024798.431358976)) <= 1.0
        assert abs(n["tir"] - (-53.60174296370581)) <= 0.01
        assert n["payback"] is None
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_eta_gassif_basso_non_conviente(self):
        # Rendimento gassificazione 0,55: risparmio
        # 98622,59, VAN -3381089,22, TIR -44,02 %,
        # payback None -> NON_CONVIENTE.
        n = self._bc(eta_gassif=0.55)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            98622.58953168057, rel=REL)
        assert abs(n["van"] - (-3381089.219450918)) <= 1.0
        assert abs(n["tir"] - (-44.02057393125677)) <= 0.01
        assert n["payback"] is None
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_costo_syn_marginale(self):
        # Costo syngas 950 EUR/kW_th:
        # CAPEX_delta 2837500, VAN -54008,34 entro
        # la tolleranza 283750 -> MARGINALE.
        # (A 1000 EUR/kW_th il VAN -331699,04
        # supera la tolleranza 302500 e il caso
        # e' NON_CONVIENTE, non MARGINALE.)
        n = self._bc(costo_syn_eur_kw=950.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            2837500.0, rel=REL)
        assert abs(n["van"] - (-54008.33865785561)) <= 1.0
        assert abs(n["tir"] - 4.545357520898559) <= 0.01
        assert n["payback"] == 8
        assert n["verdetto"] == "MARGINALE"

    def test_costo_syn_alto_non_conviente(self):
        # Costo syngas 2000 EUR/kW_th:
        # CAPEX_delta 6775000, VAN -5885513,16,
        # TIR -31,68 %, payback None -> NON_CONVIENTE.
        n = self._bc(costo_syn_eur_kw=2000.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            6775000.0, rel=REL)
        assert abs(n["van"] - (-5885513.16239105)) <= 1.0
        assert abs(n["tir"] - (-31.682022685448874)) <= 0.01
        assert n["payback"] is None
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_vite_corte_sostituzioni_entrambi(self):
        # Vita 10 anni per entrambi: sost [10]
        # per entrambi; flusso anno 10 = risparmio
        # - CAPEX syngas + CAPEX gas;
        # VAN 556956,92, TIR 7,60 %, payback 7
        # -> CONVIENTE.
        n = self._bc(vita_gas_anni=10, vita_syn_anni=10)
        assert n["valid"] is True
        assert n["anni_sost_gas"] == [10]
        assert n["anni_sost_syn"] == [10]
        assert n["df_flussi"]["Flusso (€/anno)"].iloc[10] == \
            pytest.approx(-2262121.212121212, rel=REL)
        assert abs(n["van"] - 556956.9200718927) <= 1.0
        assert abs(n["tir"] - 7.60262659446801) <= 0.01
        assert n["payback"] == 7
        assert n["verdetto"] == "CONVIENTE"

    def test_vite_diverse_sostituzioni(self):
        # Vita gas 12 anni, syngas 8 anni:
        # sost gas [12], syngas [8, 16];
        # VAN -1647604,49, TIR -12,92 %,
        # payback 7 (primo cumulato >= 0 prima
        # delle sostituzioni) -> NON_CONVIENTE.
        n = self._bc(vita_gas_anni=12, vita_syn_anni=8)
        assert n["anni_sost_gas"] == [12]
        assert n["anni_sost_syn"] == [8, 16]
        assert abs(n["van"] - (-1647604.4895239284)) <= 1.0
        assert abs(n["tir"] - (-12.916055285548738)) <= 0.01
        assert n["payback"] == 7
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_domanda_zero_neutro(self):
        n = self._bc(domanda_mwh_a=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_sopra_uno_neutro(self):
        n = self._bc(eta_gassif=1.2)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_gas_zero_neutro(self):
        n = self._bc(eta_gas=0.0)
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
        n = self._bc(eta_gassif=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(domanda_mwh_a=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(vita_syn_anni=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_zero_calcolabile(self):
        # WACC 0: VAN = somma flussi =
        # -2650000 + 387878,79 x 20 - 4075000 =
        # 1032575,76.
        n = self._bc(wacc_frac=0.0)
        assert n["van"] == pytest.approx(
            1032575.7575757615, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_tir_none_caso_demo_senza_investimento(self):
        # CAPEX delta negativo e risparmio positivo:
        # tutti i flussi >= 0 -> TIR None.
        n = self._bc(costo_syn_eur_kw=100.0, fisso_syn_eur=0.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] < 0.0
        assert n["tir"] is None
        assert n["payback"] == 0
        assert n["verdetto"] == "CONVIENTE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh720_neutro"]()
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
        n = _F["_mh720_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "domanda_mwh_a", "ore_eq",
                       "eta_gas", "eta_gassif", "eta_cald_syn",
                       "potenza_th_kw",
                       "fuel_gas_mwh_a",
                       "feed_bio_mwh_a",
                       "costo_base_eur_a",
                       "costo_alt_eur_a",
                       "risparmio_eur_a",
                       "capex_gas_eur",
                       "capex_syn_eur",
                       "capex_delta_eur",
                       "anni_sost_gas",
                       "anni_sost_syn",
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
        assert len(b["df_tabella"]) == 28
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Potenza termica (kW)" in voci
        assert "Gas naturale consumato (MWh/a)" in voci
        assert "Biomassa feedstock (MWh PCI/a)" in voci
        assert "Costo annuo baseline (EUR/anno)" in voci
        assert "Costo annuo alternativa (EUR/anno)" in voci
        assert "Risparmio annuo (EUR/anno)" in voci
        assert "CAPEX syngas (EUR)" in voci
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
        assert b["df_flussi"]["Flusso (€/anno)"].iloc[15] == \
            pytest.approx(RISPARMIO_DEMO - CAPEX_SYN_DEMO,
                          rel=REL)


class TestSensitivita:
    def _ing(self):
        return _F["mh720_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh720_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.9", "x1.0", "x1.1"]
        assert list(s.index) == ["x0.9", "x1.0", "x1.1"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh720_sensitivita"](self._ing())
        assert abs(s.loc["x1.0", "x1.0"] - VAN_DEMO) <= 1.0

    def test_sensitivita_crescente_con_eta_gassif(self):
        s = _F["mh720_sensitivita"](self._ing())
        for colonna in ("x0.9", "x1.0", "x1.1"):
            assert s.loc["x0.9", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.1", colonna]

    def test_sensitivita_decrescente_con_prezzo_bio(self):
        s = _F["mh720_sensitivita"](self._ing())
        for riga in ("x0.9", "x1.0", "x1.1"):
            assert s.loc[riga, "x0.9"] > \
                s.loc[riga, "x1.0"] > \
                s.loc[riga, "x1.1"]

    def test_sensitivita_nessuna_colonna_degenere(self):
        s = _F["mh720_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_nessuna_colonna_costante(self):
        s = _F["mh720_sensitivita"](self._ing())
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3

    def test_sensitivita_angoli(self):
        s = _F["mh720_sensitivita"](self._ing())
        assert abs(s.loc["x0.9", "x0.9"] - 223682.3672342016) <= 1.0
        assert abs(s.loc["x0.9", "x1.1"] - (-1979233.6024067022)) <= 1.0
        assert abs(s.loc["x1.1", "x0.9"] - 2026068.1605767612) <= 1.0
        assert abs(s.loc["x1.1", "x1.1"] - 223682.3672342016) <= 1.0

    def test_sensitivita_diagonale_simmetrica(self):
        # Rendimento e prezzo variati dello stesso
        # fattore si compensano (feedstock x prezzo
        # invariato): la diagonale coincide col centro.
        s = _F["mh720_sensitivita"](self._ing())
        assert abs(s.loc["x0.9", "x0.9"] - VAN_DEMO) <= 1.0
        assert abs(s.loc["x1.1", "x1.1"] - VAN_DEMO) <= 1.0

    def test_sensitivita_con_sostituzioni_ricalcolate(self):
        # Con vite 10 anni per entrambi la griglia
        # deve includere la sostituzione anno 10:
        # il centro deve coincidere col VAN
        # del caso con vite 10 anni.
        ing = self._ing()
        ing["vita_gas_anni"] = 10
        ing["vita_syn_anni"] = 10
        s = _F["mh720_sensitivita"](ing)
        assert abs(s.loc["x1.0", "x1.0"] - 556956.9200718927) <= 1.0


class TestCsv:
    def _ing(self):
        return _F["mh720_demo"]()

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh720_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 34

    def test_csv_contiene_verdetto_e_risparmio(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh720_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "risparmio_eur_a" in txt
        assert "costo_base_eur_a" in txt
        assert "costo_alt_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "domanda_mwh_a" in txt
        assert "potenza_th_kw" in txt
        assert "co2_evitata_t_a" in txt
        assert "eta_gassif" in txt
        assert "eta_cald_syn" in txt
        assert "capex_delta_eur" in txt
        assert "fisso_syn_eur" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh720_csv"](bc, self._ing())
        assert f"risparmio_eur_a;{bc['risparmio_eur_a']}" in txt
        assert f"costo_base_eur_a;{bc['costo_base_eur_a']}" in txt
        assert "domanda_mwh_a;15000.0" in txt
        assert "opex_syn_eur_a;400000.0" in txt
        assert f"capex_delta_eur;{bc['capex_delta_eur']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def720["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def720\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 20, ui_keys
        demo_keys = set(_F["mh720_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh720_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh720_demo():")
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
        ui_keys = set(re.findall(r'_def720\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W721 (26/10/2026) - tab720' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh720_num", "mh720_nneg", "mh720_pos",
                     "mh720_int_pos", "mh720_int_nneg",
                     "mh720_eta_valido", "mh720_potenza_th",
                     "mh720_energia_gas", "mh720_energia_bio",
                     "mh720_costo_annuo", "mh720_risparmio",
                     "mh720_capex", "mh720_anni_sostituzione",
                     "mh720_flussi", "mh720_van_flussi",
                     "mh720_tir_flussi", "mh720_payback_flussi",
                     "mh720_verdetto", "mh720_co2_evitata",
                     "mh720_valida", "_mh720_neutro",
                     "mh720_calcola", "mh720_sensitivita",
                     "mh720_csv", "mh720_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_nessun_identificatore_futura_tab(self):
        assert "mh721" not in _helpers_src()
        assert "mh721" not in _ui_src()
        assert "st721" not in _ui_src()
        assert "tab721" not in _ui_src()

    def test_nessun_residuo_tab_precedente(self):
        # Niente residui della tab precedente
        # (mh719 / tab719 / st719) in helpers/UI:
        # il test puo' citare tab719 come tab
        # precedente, i frammenti no.
        assert "mh719" not in _helpers_src()
        assert "mh719" not in _ui_src()
        assert "st719" not in _ui_src()
        assert "tab719" not in _helpers_src()
        assert "tab719" not in _ui_src()

    def test_chain_riferimento_tab_precedente(self):
        # Questo file test fa riferimento alla
        # tab precedente tab719 (torrefazione)
        # come punto di confronto e la nuova tab
        # e' tab720.
        src = Path(__file__).read_text(encoding="utf-8")
        assert "tab719" in src
        assert "tab720" in src
        assert _ui_src().startswith("    with tab720:")

    def test_helpers_parse_ast(self):
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w721_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE720) == 1

    def test_blocco_with_tab720(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab720:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE720

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st720_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 25, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st720_") for k in keys)

    def test_chiavi_st_input_sono_21(self):
        """Le 21 chiavi di input/bottone (20 input +
        bottone calcola) sono tutte presenti; le
        altre 4 sono solo chiavi di
        visualizzazione (fig, heatmap, flussi, CSV)."""
        keys = re.findall(r'key="(st720_[a-z0-9_]+)"', _ui_src())
        attese = ["st720_domanda", "st720_ore",
                  "st720_eta_gas", "st720_eta_gassif",
                  "st720_eta_cald_syn", "st720_p_gas",
                  "st720_p_bio", "st720_c_gas",
                  "st720_fisso_gas", "st720_c_syn",
                  "st720_fisso_syn", "st720_opex_gas",
                  "st720_opex_syn", "st720_vita_gas",
                  "st720_vita_syn", "st720_vita_progetto",
                  "st720_wacc", "st720_tolleranza",
                  "st720_f_gas", "st720_f_bio",
                  "st720_calcola"]
        assert len(attese) == 21
        for k in attese:
            assert k in keys, k

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg720" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg720") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg720")
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
        assert "gassificazione" in src
        assert "syngas" in src
        assert "biomassa" in src
        assert "biogenica" in src

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Costo annuo baseline (caldaia a gas)" in src
        assert "Costo annuo alternativa (caldaia a syngas)" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh720_csv" in src
        assert "syngas_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh720_sensitivita" in src
        assert "Heatmap" in src
        assert "Rendimento gassificazione" in src
        assert "Prezzo biomassa" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st720_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W721 (26/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab720:")
