"""Test tab721 "☀️❄️ Raffrescamento solare: il sole fa freddo con l'assorbitore?"

Tab precedente tab720 (syngas, w721);
nuova tab tab721 (raffrescamento solare,
w722). La tab721 replica ESATTAMENTE la
semantica economica delle tab650-720:
flussi [-CAPEX_delta, risparmio con
sostituzioni], VAN/TIR (bisezione [-99 %,
+500 %], None se risparmio <= 0 o nessun
cambio di segno incl. tutti flussi >= 0)/
payback (0 se cumulato anno 0 >= 0),
verdetto CONVIENTE (VAN >= 0)/MARGINALE
(VAN < 0 entro toll % di |CAPEX_delta|;
CAPEX_delta == 0 mai MARGINALE)/
NON_CONVIENTE/NON_CALCOLABILE (validazione
fallita o risparmio <= 0), sostituzioni
multipli interi di floor(vita_anni) con
1 <= anno < vita progetto, flusso anno
sostituzione = risparmio - CAPEX_alt +
CAPEX_base.

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
domanda frigorifera 2000 MWh/a; ore
equivalenti 2000 h; EER chiller 4,0; COP
assorbitore 0,80; superficie collettori
3000 m2; irraggiamento 1200 kWh/m2/a;
rendimento collettori 0,50; rendimento
caldaia backup 0,90; prezzo elettricita'
300 EUR/MWh; prezzo gas 80 EUR/MWh; opex
chiller 20000 EUR/anno; opex assorbitore
15000 EUR/anno; opex solare 10000
EUR/anno; costo chiller 400 EUR/kW; costo
fisso chiller 50000 EUR; costo collettori
300 EUR/m2; costo fisso collettori 100000
EUR; costo assorbitore 600 EUR/kW; costo
fisso assorbitore 100000 EUR; vita
chiller 15 anni; vita assorbitore 20 anni;
vita di progetto 20 anni; WACC 0,05
(5 %); tolleranza 0,10 (10 % del
|CAPEX_delta|); fattore elettrico 0,35
t/MWh; fattore gas 0,20 t/MWh.

- potenza_freddo_kw = 1000.0
- energia_el_mwh_a = 500.0
- calore_motore_mwh_a = 2500.0
- calore_solare_mwh_a = 1800.0
- calore_backup_mwh_a = 700.0
- gas_backup_mwh_a = 777.7777777777777
- costo_base_eur_a = 170000.0
- costo_alt_eur_a = 87222.22222222222
- risparmio_eur_a = 82777.77777777778
- capex_chiller_eur = 450000.0
- capex_alt_eur = 1700000.0
- capex_delta_eur = 1250000.0
- anni_sost_chiller = [15]
- anni_sost_ass = []
- co2_evitata_t_a = 19.444444444444457
- van = -1948.2275043651935
- tir = 4.983562392892675
- payback = 15
- verdetto = 'MARGINALE'

Scomposizione: P_freddo 2000 x 1000 / 2000 =
1000.0 kW; E_el 2000 / 4,0 = 500.0 MWh/a;
Q_th 2000 / 0,80 = 2500.0 MWh/a; Q_sol
grezzo 3000 x 1200 x 0,50 / 1000 = 1800.0
MWh/a (< Q_th, quindi utile intero);
Q_backup 2500.0 - 1800.0 = 700.0 MWh/a;
gas backup 700.0 / 0,90 = 777.7777777777777
MWh/a; C_base 500.0 x 300 + 20000 =
170000.0 EUR/anno; C_alt 777.7777777777777
x 80 + 15000 + 10000 = 87222.22222222222
EUR/anno; risparmio 170000.0 -
87222.22222222222 = 82777.77777777778
EUR/anno; CAPEX chiller 1000.0 x 400 +
50000 = 450000.0 EUR; CAPEX alternativa
3000 x 300 + 100000 + 1000.0 x 600 +
100000 = 1700000.0 EUR; CAPEX_delta
1700000.0 - 450000.0 = 1250000.0 EUR;
sostituzioni: floor(15) = 15, multiplo 15
< 20 -> [15] per il chiller; floor(20) =
20, nessun multiplo < 20 -> [] per
l'assorbitore; flussi: anno 0 -1250000.0,
anni 1-14 e 16-20 risparmio
82777.77777777778, anno 15 risparmio +
CAPEX chiller = 532777.7777777778; VAN
-1948.2275043651935 a WACC 5 % su 20 anni;
TIR 4.983562392892675 % (il tasso che
azzera il VAN dei flussi sopra); payback
15 (il cumulato diventa positivo solo
all'anno 15 grazie alla sostituzione del
chiller: -1250000.0 + 14 x 82777.77777777778
= -91111.11111111113 all'anno 14, poi +
532777.7777777778 = 441666.6666666667
all'anno 15); CO2 500.0 x 0,35 -
777.7777777777777 x 0,20 =
19.444444444444457 t/anno (positiva ma
piccola e INFORMATIVA: il backup a gas
mangia quasi tutta la CO2 risparmiata
sull'elettricita'); VAN < 0 ma |VAN| =
1948.2275043651935 <= 0,10 x 1250000.0 =
125000.0 -> MARGINALE, di misura (VAN =
-0,2 % del CAPEX delta).

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
    if (p / "w722_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w722_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w722_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w722_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w722_helpers.py: {missing}")
    return out


_F = _load("mh721_num", "mh721_nneg", "mh721_pos",
           "mh721_int_pos", "mh721_int_nneg",
           "mh721_eta_valido", "mh721_potenza_freddo",
           "mh721_energia_el", "mh721_calore_motore",
           "mh721_calore_solare", "mh721_calore_backup",
           "mh721_energia_gas_backup",
           "mh721_costo_annuo", "mh721_risparmio",
           "mh721_capex_chiller", "mh721_capex_alt",
           "mh721_anni_sostituzione",
           "mh721_flussi", "mh721_van_flussi",
           "mh721_tir_flussi", "mh721_payback_flussi",
           "mh721_verdetto", "mh721_co2_evitata",
           "mh721_valida", "_mh721_neutro",
           "mh721_calcola", "mh721_sensitivita",
           "mh721_csv", "mh721_demo", "demo_calcoli")

TITLE721 = ("☀️❄️ Raffrescamento solare: il sole fa freddo "
            "con l'assorbitore?")

P_FR_DEMO = 1000.0
E_EL_DEMO = 500.0
Q_TH_DEMO = 2500.0
Q_SOL_DEMO = 1800.0
Q_BK_DEMO = 700.0
GAS_BK_DEMO = 777.7777777777777
C_BASE_DEMO = 170000.0
C_ALT_DEMO = 87222.22222222222
RISPARMIO_DEMO = 82777.77777777778
CAPEX_CHILLER_DEMO = 450000.0
CAPEX_ALT_DEMO = 1700000.0
DELTA_DEMO = 1250000.0
CO2_DEMO = 19.444444444444457
VAN_DEMO = -1948.2275043651935
TIR_DEMO = 4.983562392892675
PAYBACK_DEMO = 15
VITA_DEMO = 20
VERDETTO_DEMO = "MARGINALE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w722_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w722_ui.py").read_text(encoding="utf-8")


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh721_demo"]()
        d.update(kw)
        return _F["mh721_valida"](**d)

    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh721_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh721_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh721_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh721_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh721_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh721_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh721_pos"](0.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh721_int_pos"](2.5, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh721_int_pos"](20.0, "x") == 20

    def test_int_nneg_accetta_zero(self):
        assert _F["mh721_int_nneg"](0, "x") == 0

    def test_eta_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh721_eta_valido"](0.0, "x")

    def test_eta_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh721_eta_valido"](1.01, "x")

    def test_eta_accetta_uno(self):
        assert _F["mh721_eta_valido"](1.0, "x") == 1.0

    def test_eta_coll_e_cald_sopra_uno_non_validi(self):
        assert self._val(eta_coll=1.2)["valido"] is False
        assert self._val(eta_cald=1.2)["valido"] is False

    def test_eer_e_cop_sopra_uno_validi(self):
        # EER e COP sono coefficienti di
        # prestazione, non rendimenti: possono
        # superare 1 (EER 4,0 gia' nella demo).
        assert self._val(eer=6.0)["valido"] is True
        assert self._val(cop_ass=1.2)["valido"] is True

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_domanda_zero_non_valida(self):
        assert self._val(domanda_freddo_mwh_a=0.0)["valido"] is False

    def test_ore_zero_non_valide(self):
        assert self._val(ore_eq=0.0)["valido"] is False

    def test_eer_e_cop_zero_non_validi(self):
        assert self._val(eer=0.0)["valido"] is False
        assert self._val(cop_ass=0.0)["valido"] is False

    def test_eta_zero_non_valide(self):
        assert self._val(eta_coll=0.0)["valido"] is False
        assert self._val(eta_cald=0.0)["valido"] is False

    def test_negativi_non_validi(self):
        for k in ("area_mq", "irraggiamento_kwh_mq_a",
                  "prezzo_el_eur_mwh", "prezzo_gas_eur_mwh",
                  "opex_chiller_eur_a",
                  "opex_assorbitore_eur_a",
                  "opex_solare_eur_a",
                  "costo_chiller_eur_kw", "fisso_chiller_eur",
                  "costo_coll_eur_mq", "fisso_coll_eur",
                  "costo_ass_eur_kw", "fisso_ass_eur",
                  "wacc_frac", "tolleranza_frac",
                  "fattore_el_t_mwh", "fattore_gas_t_mwh"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_vite_zero_non_valide(self):
        assert self._val(vita_chiller_anni=0)["valido"] is False
        assert self._val(vita_ass_anni=0)["valido"] is False

    def test_vite_non_intere_non_valide(self):
        assert self._val(vita_chiller_anni=15.5)["valido"] is False
        assert self._val(vita_ass_anni=20.5)["valido"] is False

    def test_vita_progetto_zero_non_valida(self):
        assert self._val(vita_progetto_anni=0)["valido"] is False

    def test_tolleranza_sopra_uno_valida_brief(self):
        assert self._val(tolleranza_frac=1.5)["valido"] is True

    def test_wacc_senza_tetto_superiore(self):
        assert self._val(wacc_frac=1.5)["valido"] is True

    def test_nan_non_valido(self):
        assert self._val(eta_coll=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(domanda_freddo_mwh_a=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(vita_ass_anni=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(eta_coll="0.50")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(prezzo_el_eur_mwh=0.0)["valido"] is True
        assert self._val(area_mq=0.0)["valido"] is True
        assert self._val(irraggiamento_kwh_mq_a=0.0)["valido"] is True
        assert self._val(costo_coll_eur_mq=0.0)["valido"] is True
        assert self._val(fisso_ass_eur=0.0)["valido"] is True
        assert self._val(opex_solare_eur_a=0.0)["valido"] is True
        assert self._val(wacc_frac=0.0)["valido"] is True
        assert self._val(tolleranza_frac=0.0)["valido"] is True
        assert self._val(fattore_gas_t_mwh=0.0)["valido"] is True


class TestFunzioni:
    def test_potenza_freddo_demo(self):
        assert _F["mh721_potenza_freddo"](
            2000.0, 2000.0) == pytest.approx(P_FR_DEMO, rel=REL)

    def test_energia_el_demo(self):
        assert _F["mh721_energia_el"](
            2000.0, 4.0) == pytest.approx(E_EL_DEMO, rel=REL)

    def test_energia_el_cresce_con_eer_basso(self):
        assert _F["mh721_energia_el"](
            2000.0, 2.0) > _F["mh721_energia_el"](
            2000.0, 4.0)

    def test_calore_motore_demo(self):
        assert _F["mh721_calore_motore"](
            2000.0, 0.80) == pytest.approx(Q_TH_DEMO, rel=REL)

    def test_calore_solare_demo(self):
        # 3000 x 1200 x 0,50 / 1000 = 1800.
        assert _F["mh721_calore_solare"](
            3000.0, 1200.0, 0.50) == pytest.approx(
            Q_SOL_DEMO, rel=REL)

    def test_calore_solare_conversione_kwh_mwh(self):
        assert _F["mh721_calore_solare"](
            1000.0, 1000.0, 1.0) == pytest.approx(
            1000.0, rel=REL)

    def test_calore_backup_demo(self):
        assert _F["mh721_calore_backup"](
            Q_TH_DEMO, Q_SOL_DEMO) == pytest.approx(
            Q_BK_DEMO, rel=REL)

    def test_energia_gas_backup_demo(self):
        assert _F["mh721_energia_gas_backup"](
            Q_BK_DEMO, 0.90) == pytest.approx(
            GAS_BK_DEMO, rel=REL)

    def test_costo_annuo_demo(self):
        assert _F["mh721_costo_annuo"](
            E_EL_DEMO, 300.0, 20000.0) == pytest.approx(
            C_BASE_DEMO, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh721_risparmio"](
            C_BASE_DEMO, C_ALT_DEMO) == pytest.approx(
            RISPARMIO_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh721_risparmio"](
            100000.0, 150000.0) == pytest.approx(-50000.0, rel=REL)

    def test_capex_chiller_demo(self):
        assert _F["mh721_capex_chiller"](
            P_FR_DEMO, 400.0, 50000.0) == pytest.approx(
            CAPEX_CHILLER_DEMO, rel=REL)

    def test_capex_alt_demo(self):
        assert _F["mh721_capex_alt"](
            3000.0, 300.0, 100000.0,
            P_FR_DEMO, 600.0, 100000.0) == pytest.approx(
            CAPEX_ALT_DEMO, rel=REL)

    def test_capex_delta_demo_non_clampato(self):
        delta = _F["mh721_capex_alt"](
            3000.0, 300.0, 100000.0,
            P_FR_DEMO, 600.0, 100000.0) - _F["mh721_capex_chiller"](
            P_FR_DEMO, 400.0, 50000.0)
        assert delta == pytest.approx(DELTA_DEMO, rel=REL)
        # Delta negativo possibile: solare piu'
        # economico del chiller.
        assert _F["mh721_capex_alt"](
            3000.0, 50.0, 0.0,
            P_FR_DEMO, 100.0, 0.0) - _F["mh721_capex_chiller"](
            P_FR_DEMO, 400.0, 50000.0) < 0.0

    def test_anni_sostituzione_demo(self):
        assert _F["mh721_anni_sostituzione"](15, 20) == [15]
        assert _F["mh721_anni_sostituzione"](20, 20) == []

    def test_anni_sostituzione_multipli(self):
        assert _F["mh721_anni_sostituzione"](10, 20) == [10]
        assert _F["mh721_anni_sostituzione"](5, 20) == [5, 10, 15]

    def test_anni_sostituzione_floor_non_intero(self):
        assert _F["mh721_anni_sostituzione"](10.5, 20) == [10]

    def test_anni_sostituzione_sotto_anno_vuota(self):
        assert _F["mh721_anni_sostituzione"](0.5, 20) == []

    def test_anni_sostituzione_esclude_vita_progetto(self):
        assert _F["mh721_anni_sostituzione"](20, 20) == []
        assert _F["mh721_anni_sostituzione"](15, 20) == [15]

    def test_co2_evitata_demo(self):
        assert _F["mh721_co2_evitata"](
            E_EL_DEMO, GAS_BK_DEMO, 0.35, 0.20) == \
            pytest.approx(CO2_DEMO, rel=REL)
        assert CO2_DEMO > 0.0

    def test_co2_evitata_puo_essere_negativa(self):
        assert _F["mh721_co2_evitata"](
            500.0, 2000.0, 0.20, 0.20) == pytest.approx(
            -300.0, rel=REL)

    def test_co2_evitata_zero_se_fattori_zero(self):
        assert _F["mh721_co2_evitata"](
            E_EL_DEMO, GAS_BK_DEMO, 0.0, 0.0) == \
            pytest.approx(0.0, abs=1e-9)

    def test_van_flussi_demo(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 14 + \
            [RISPARMIO_DEMO + CAPEX_CHILLER_DEMO] + \
            [RISPARMIO_DEMO] * 5
        assert len(flussi) == 21
        assert abs(_F["mh721_van_flussi"](
            flussi, 0.05) - VAN_DEMO) <= 1.0

    def test_van_flussi_tasso_zero(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 20
        atteso = -DELTA_DEMO + RISPARMIO_DEMO * 20
        assert _F["mh721_van_flussi"](
            flussi, 0.0) == pytest.approx(atteso, rel=1e-12)

    def test_van_flussi_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh721_van_flussi"]([100.0, 100.0], -0.01)

    def test_flussi_demo_con_sostituzioni(self):
        flussi = _F["mh721_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CAPEX_CHILLER_DEMO, CAPEX_ALT_DEMO, [15], [], 20)
        assert len(flussi) == 21
        assert flussi[0] == pytest.approx(-DELTA_DEMO, rel=REL)
        assert flussi[1] == pytest.approx(RISPARMIO_DEMO, rel=REL)
        assert flussi[14] == pytest.approx(RISPARMIO_DEMO, rel=REL)
        assert flussi[15] == pytest.approx(
            RISPARMIO_DEMO + CAPEX_CHILLER_DEMO, rel=REL)
        assert flussi[20] == pytest.approx(RISPARMIO_DEMO, rel=REL)

    def test_flussi_formula_sostituzione_ass(self):
        flussi = _F["mh721_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CAPEX_CHILLER_DEMO, CAPEX_ALT_DEMO, [], [10], 20)
        assert flussi[10] == pytest.approx(
            RISPARMIO_DEMO - CAPEX_ALT_DEMO, rel=REL)

    def test_flussi_formula_sostituzione_entrambi(self):
        flussi = _F["mh721_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CAPEX_CHILLER_DEMO, CAPEX_ALT_DEMO, [10], [10], 20)
        assert flussi[10] == pytest.approx(
            RISPARMIO_DEMO - CAPEX_ALT_DEMO + CAPEX_CHILLER_DEMO,
            rel=REL)

    def test_tir_demo(self):
        flussi = _F["mh721_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CAPEX_CHILLER_DEMO, CAPEX_ALT_DEMO, [15], [], 20)
        tir = _F["mh721_tir_flussi"](flussi)
        assert tir is not None
        assert tir * 100.0 == pytest.approx(TIR_DEMO, rel=1e-9)

    def test_tir_none_tutti_flussi_non_negativi(self):
        assert _F["mh721_tir_flussi"](
            [1000.0] + [100.0] * 10) is None

    def test_tir_none_nessun_cambio_segno_negativo(self):
        # Tutti i flussi <= 0: nessun tasso azzera il VAN.
        assert _F["mh721_tir_flussi"](
            [-1000.0] + [-100.0] * 10) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh721_tir_flussi"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo_quindici(self):
        flussi = _F["mh721_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CAPEX_CHILLER_DEMO, CAPEX_ALT_DEMO, [15], [], 20)
        assert _F["mh721_payback_flussi"](flussi) == PAYBACK_DEMO

    def test_payback_none_se_mai(self):
        assert _F["mh721_payback_flussi"](
            [-5000000000.0] + [RISPARMIO_DEMO] * 20) is None

    def test_payback_zero_se_cumulato_anno_zero_non_negativo(self):
        assert _F["mh721_payback_flussi"](
            [0.0] + [RISPARMIO_DEMO] * 20) == 0

    def test_verdetto_marginale_demo(self):
        assert _F["mh721_verdetto"](
            VAN_DEMO, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == VERDETTO_DEMO

    def test_verdetto_van_zero_conviente(self):
        assert _F["mh721_verdetto"](
            0.0, DELTA_DEMO, 0.10, RISPARMIO_DEMO) == "CONVIENTE"

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh721_verdetto"](
            -100.0, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh721_verdetto"](
            -0.10 * abs(DELTA_DEMO), DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_oltre_limite(self):
        assert _F["mh721_verdetto"](
            -0.10 * abs(DELTA_DEMO) - 1.0, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_non_positivo(
            self):
        assert _F["mh721_verdetto"](
            1000.0, DELTA_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh721_verdetto"](
            1000.0, DELTA_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_delta_zero_van_positivo_conviente(
            self):
        assert _F["mh721_verdetto"](
            1000.0, 0.0, 0.10, RISPARMIO_DEMO) == "CONVIENTE"

    def test_verdetto_capex_delta_zero_van_negativo_non_conviente(
            self):
        assert _F["mh721_verdetto"](
            -1.0, 0.0, 0.10, RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh721_verdetto"](100.0, DELTA_DEMO, -0.01, RISPARMIO_DEMO)


class TestDemo:
    def _bc(self, **kw):
        d = _F["mh721_demo"]()
        d.update(kw)
        return _F["mh721_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["potenza_freddo_kw"] == pytest.approx(
            P_FR_DEMO, rel=REL)
        assert c["energia_el_mwh_a"] == pytest.approx(
            E_EL_DEMO, rel=REL)
        assert c["calore_motore_mwh_a"] == pytest.approx(
            Q_TH_DEMO, rel=REL)
        assert c["calore_solare_mwh_a"] == pytest.approx(
            Q_SOL_DEMO, rel=REL)
        assert c["calore_backup_mwh_a"] == pytest.approx(
            Q_BK_DEMO, rel=REL)
        assert c["gas_backup_mwh_a"] == pytest.approx(
            GAS_BK_DEMO, rel=REL)
        assert c["costo_base_eur_a"] == pytest.approx(
            C_BASE_DEMO, rel=REL)
        assert c["costo_alt_eur_a"] == pytest.approx(
            C_ALT_DEMO, rel=REL)
        assert c["risparmio_eur_a"] == pytest.approx(
            RISPARMIO_DEMO, rel=REL)
        assert c["capex_chiller_eur"] == pytest.approx(
            CAPEX_CHILLER_DEMO, rel=REL)
        assert c["capex_alt_eur"] == pytest.approx(
            CAPEX_ALT_DEMO, rel=REL)
        assert c["capex_delta_eur"] == pytest.approx(
            DELTA_DEMO, rel=REL)
        assert c["anni_sost_chiller"] == [15]
        assert c["anni_sost_ass"] == []
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
        d = _F["mh721_demo"]()
        b = _F["mh721_calcola"](**d)
        coppie = [("potenza_freddo_kw", P_FR_DEMO),
                  ("energia_el_mwh_a", E_EL_DEMO),
                  ("calore_motore_mwh_a", Q_TH_DEMO),
                  ("calore_solare_mwh_a", Q_SOL_DEMO),
                  ("calore_backup_mwh_a", Q_BK_DEMO),
                  ("gas_backup_mwh_a", GAS_BK_DEMO),
                  ("costo_base_eur_a", C_BASE_DEMO),
                  ("costo_alt_eur_a", C_ALT_DEMO),
                  ("risparmio_eur_a", RISPARMIO_DEMO),
                  ("capex_chiller_eur", CAPEX_CHILLER_DEMO),
                  ("capex_alt_eur", CAPEX_ALT_DEMO),
                  ("capex_delta_eur", DELTA_DEMO),
                  ("co2_evitata_t_a", CO2_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert b["anni_sost_chiller"] == [15]
        assert b["anni_sost_ass"] == []
        assert abs(b["van"] - VAN_DEMO) <= 1.0
        assert abs(b["tir"] - TIR_DEMO) <= 0.01
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh721_demo"]()
        assert d["domanda_freddo_mwh_a"] == 2000.0
        assert d["ore_eq"] == 2000.0
        assert d["eer"] == 4.0
        assert d["cop_ass"] == 0.80
        assert d["area_mq"] == 3000.0
        assert d["irraggiamento_kwh_mq_a"] == 1200.0
        assert d["eta_coll"] == 0.50
        assert d["eta_cald"] == 0.90
        assert d["prezzo_el_eur_mwh"] == 300.0
        assert d["prezzo_gas_eur_mwh"] == 80.0
        assert d["opex_chiller_eur_a"] == 20000.0
        assert d["opex_assorbitore_eur_a"] == 15000.0
        assert d["opex_solare_eur_a"] == 10000.0
        assert d["costo_chiller_eur_kw"] == 400.0
        assert d["fisso_chiller_eur"] == 50000.0
        assert d["costo_coll_eur_mq"] == 300.0
        assert d["fisso_coll_eur"] == 100000.0
        assert d["costo_ass_eur_kw"] == 600.0
        assert d["fisso_ass_eur"] == 100000.0
        assert d["vita_chiller_anni"] == 15
        assert d["vita_ass_anni"] == 20
        assert d["vita_progetto_anni"] == 20
        assert d["wacc_frac"] == 0.05
        assert d["tolleranza_frac"] == 0.10
        assert d["fattore_el_t_mwh"] == 0.35
        assert d["fattore_gas_t_mwh"] == 0.20
        assert len(d) == 26

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("potenza_freddo_kw",
                       "energia_el_mwh_a",
                       "calore_motore_mwh_a",
                       "calore_solare_mwh_a",
                       "calore_backup_mwh_a",
                       "gas_backup_mwh_a",
                       "costo_base_eur_a",
                       "costo_alt_eur_a",
                       "risparmio_eur_a",
                       "capex_chiller_eur",
                       "capex_alt_eur",
                       "capex_delta_eur",
                       "co2_evitata_t_a", "van"):
            assert repr(c[chiave]) in doc, chiave
        assert repr(c["anni_sost_chiller"]) in doc
        assert repr(c["anni_sost_ass"]) in doc
        assert f"tir = {repr(c['tir'])}" in doc
        assert "payback = 15" in doc
        assert "verdetto = 'MARGINALE'" in doc

    def test_prezzo_el_basso_non_conviente(self):
        # Prezzo elettricita' 200 EUR/MWh: C_base
        # 120000, risparmio 32777,78, VAN
        # -625058,74, TIR -0,98 %, payback None
        # -> NON_CONVIENTE.
        n = self._bc(prezzo_el_eur_mwh=200.0)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            32777.77777777778, rel=REL)
        assert abs(n["van"] - (-625058.7446313641)) <= 1.0
        assert abs(n["tir"] - (-0.9813612161025876)) <= 0.01
        assert n["payback"] is None
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_prezzo_gas_alto_risparmio_negativo(self):
        # Prezzo gas 200 EUR/MWh: C_alt
        # 180555,56 > C_base 170000 ->
        # risparmio negativo -> dict neutro
        # NON_CALCOLABILE.
        n = self._bc(prezzo_gas_eur_mwh=200.0)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_eta_coll_basso_non_conviente(self):
        # Rendimento collettori 0,40: Q_sol
        # 1440, backup 1060, gas 1177,78,
        # risparmio 50777,78, VAN -400738,96,
        # TIR 1,37 %, payback 16 -> NON_CONVIENTE.
        n = self._bc(eta_coll=0.40)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            50777.77777777778, rel=REL)
        assert abs(n["van"] - (-400738.9584656448)) <= 1.0
        assert abs(n["tir"] - 1.3698595097289938) <= 0.01
        assert n["payback"] == 16
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_cop_ass_basso_non_conviente(self):
        # COP assorbitore 0,60: Q_th 3333,33,
        # Q_sol 1800, backup 1533,33, gas
        # 1703,70, risparmio 8703,70, VAN
        # -925074,92 -> NON_CONVIENTE.
        n = self._bc(cop_ass=0.6)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            8703.703703703679, rel=REL)
        assert abs(n["van"] - (-925074.919544364)) <= 1.0
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_costo_coll_basso_conviente(self):
        # Costo collettori 250 EUR/m2:
        # CAPEX_delta 1100000, VAN 148051,77,
        # TIR 6,37 %, payback 14 -> CONVIENTE.
        n = self._bc(costo_coll_eur_mq=250.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            1100000.0, rel=REL)
        assert abs(n["van"] - 148051.77249563474) <= 1.0
        assert abs(n["tir"] - 6.367862596558265) <= 0.01
        assert n["payback"] == 14
        assert n["verdetto"] == "CONVIENTE"

    def test_area_zero_risparmio_negativo(self):
        # Area zero: Q_sol 0, backup 2500, gas
        # 2777,78, C_alt 247222,22 > C_base
        # 170000 -> dict neutro NON_CALCOLABILE.
        n = self._bc(area_mq=0.0)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_solare_in_eccesso_cappato_a_q_th(self):
        # Area 6000 m2: Q_sol grezzo 3600 >
        # Q_th 2500 -> Q_sol utile 2500, backup
        # 0, gas 0, C_alt 25000, risparmio
        # 145000.
        n = self._bc(area_mq=6000.0)
        assert n["valid"] is True
        assert n["calore_solare_mwh_a"] == pytest.approx(
            2500.0, rel=REL)
        assert n["calore_backup_mwh_a"] == pytest.approx(
            0.0, abs=1e-9)
        assert n["gas_backup_mwh_a"] == pytest.approx(
            0.0, abs=1e-9)
        assert n["risparmio_eur_a"] == pytest.approx(
            145000.0, rel=REL)

    def test_vite_corte_sostituzioni_entrambi(self):
        # Vita 10 anni per entrambi: sost [10]
        # per entrambi; flusso anno 10 = risparmio
        # - CAPEX alternativa + CAPEX chiller =
        # -1167222,22; VAN -985797,49, TIR
        # -6,87 %, payback None -> NON_CONVIENTE.
        n = self._bc(vita_chiller_anni=10, vita_ass_anni=10)
        assert n["valid"] is True
        assert n["anni_sost_chiller"] == [10]
        assert n["anni_sost_ass"] == [10]
        assert n["df_flussi"]["Flusso (€/anno)"].iloc[10] == \
            pytest.approx(-1167222.2222222222, rel=REL)
        assert abs(n["van"] - (-985797.48857125)) <= 1.0
        assert abs(n["tir"] - (-6.86832192148592)) <= 0.01
        assert n["payback"] is None
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_vite_diverse_sostituzioni(self):
        # Vita chiller 12 anni, assorbitore 8 anni:
        # sost chiller [12], assorbitore [8, 16];
        # VAN -1897245,59, TIR -41,06 %,
        # payback None -> NON_CONVIENTE.
        n = self._bc(vita_chiller_anni=12, vita_ass_anni=8)
        assert n["anni_sost_chiller"] == [12]
        assert n["anni_sost_ass"] == [8, 16]
        assert abs(n["van"] - (-1897245.5862995477)) <= 1.0
        assert abs(n["tir"] - (-41.06317462518023)) <= 0.01
        assert n["payback"] is None
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_domanda_zero_neutro(self):
        n = self._bc(domanda_freddo_mwh_a=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eta_sopra_uno_neutro(self):
        n = self._bc(eta_coll=1.2)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_eer_zero_neutro(self):
        n = self._bc(eer=0.0)
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
        n = self._bc(eta_coll=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(domanda_freddo_mwh_a=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(vita_ass_anni=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_zero_calcolabile(self):
        # WACC 0: VAN = somma flussi =
        # -1250000 + 82777,78 x 20 + 450000 =
        # 855555,56.
        n = self._bc(wacc_frac=0.0)
        assert n["van"] == pytest.approx(
            855555.5555555552, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_tir_none_caso_demo_senza_investimento(self):
        # CAPEX delta negativo e risparmio positivo:
        # tutti i flussi >= 0 -> TIR None.
        n = self._bc(costo_ass_eur_kw=100.0, fisso_ass_eur=0.0,
                     costo_coll_eur_mq=50.0, fisso_coll_eur=0.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] < 0.0
        assert n["tir"] is None
        assert n["payback"] == 0
        assert n["verdetto"] == "CONVIENTE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh721_neutro"]()
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
        n = _F["_mh721_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "domanda_freddo_mwh_a", "ore_eq",
                       "eer", "cop_ass", "area_mq",
                       "irraggiamento_kwh_mq_a",
                       "eta_coll", "eta_cald",
                       "potenza_freddo_kw",
                       "energia_el_mwh_a",
                       "calore_motore_mwh_a",
                       "calore_solare_mwh_a",
                       "calore_backup_mwh_a",
                       "gas_backup_mwh_a",
                       "costo_base_eur_a",
                       "costo_alt_eur_a",
                       "risparmio_eur_a",
                       "capex_chiller_eur",
                       "capex_alt_eur",
                       "capex_delta_eur",
                       "anni_sost_chiller",
                       "anni_sost_ass",
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
        assert len(b["df_tabella"]) == 38
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Potenza frigorifera (kW)" in voci
        assert "Elettricita' chiller (MWh/a)" in voci
        assert "Calore motore (MWh/a)" in voci
        assert "Calore solare utile (MWh/a)" in voci
        assert "Gas backup (MWh/a)" in voci
        assert "Costo annuo baseline (EUR/anno)" in voci
        assert "Costo annuo alternativa (EUR/anno)" in voci
        assert "Risparmio annuo (EUR/anno)" in voci
        assert "CAPEX alternativa (EUR)" in voci
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
            pytest.approx(RISPARMIO_DEMO + CAPEX_CHILLER_DEMO,
                          rel=REL)


class TestSensitivita:
    def _ing(self):
        return _F["mh721_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh721_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.9", "x1.0", "x1.1"]
        assert list(s.index) == ["x0.9", "x1.0", "x1.1"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh721_sensitivita"](self._ing())
        assert abs(s.loc["x1.0", "x1.0"] - VAN_DEMO) <= 1.0

    def test_sensitivita_crescente_con_prezzo_el(self):
        s = _F["mh721_sensitivita"](self._ing())
        for colonna in ("x0.9", "x1.0", "x1.1"):
            assert s.loc["x0.9", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.1", colonna]

    def test_sensitivita_crescente_con_eta_coll(self):
        s = _F["mh721_sensitivita"](self._ing())
        for riga in ("x0.9", "x1.0", "x1.1"):
            assert s.loc[riga, "x0.9"] < \
                s.loc[riga, "x1.0"] < \
                s.loc[riga, "x1.1"]

    def test_sensitivita_nessuna_colonna_degenere(self):
        s = _F["mh721_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_nessuna_colonna_costante(self):
        s = _F["mh721_sensitivita"](self._ing())
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3

    def test_sensitivita_angoli(self):
        s = _F["mh721_sensitivita"](self._ing())
        assert abs(s.loc["x0.9", "x0.9"] - (-388276.7481231045)) <= 1.0
        assert abs(s.loc["x0.9", "x1.1"] - 10513.982838175154) <= 1.0
        assert abs(s.loc["x1.1", "x0.9"] - (-14410.437846904948)) <= 1.0
        assert abs(s.loc["x1.1", "x1.1"] - 384380.29311437474) <= 1.0

    def test_sensitivita_con_sostituzioni_ricalcolate(self):
        # Con vite 10 anni per entrambi la griglia
        # deve includere la sostituzione anno 10:
        # il centro deve coincidere col VAN
        # del caso con vite 10 anni.
        ing = self._ing()
        ing["vita_chiller_anni"] = 10
        ing["vita_ass_anni"] = 10
        s = _F["mh721_sensitivita"](ing)
        assert abs(s.loc["x1.0", "x1.0"] - (-985797.48857125)) <= 1.0


class TestCsv:
    def _ing(self):
        return _F["mh721_demo"]()

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh721_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 43

    def test_csv_contiene_verdetto_e_risparmio(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh721_csv"](bc, self._ing())
        assert "verdetto;MARGINALE" in txt
        assert "risparmio_eur_a" in txt
        assert "costo_base_eur_a" in txt
        assert "costo_alt_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "domanda_freddo_mwh_a" in txt
        assert "potenza_freddo_kw" in txt
        assert "co2_evitata_t_a" in txt
        assert "eta_coll" in txt
        assert "calore_solare_mwh_a" in txt
        assert "capex_delta_eur" in txt
        assert "fisso_ass_eur" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh721_csv"](bc, self._ing())
        assert f"risparmio_eur_a;{bc['risparmio_eur_a']}" in txt
        assert f"costo_base_eur_a;{bc['costo_base_eur_a']}" in txt
        assert "domanda_freddo_mwh_a;2000.0" in txt
        assert "opex_solare_eur_a;10000.0" in txt
        assert f"capex_delta_eur;{bc['capex_delta_eur']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def721["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def721\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 26, ui_keys
        demo_keys = set(_F["mh721_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh721_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh721_demo():")
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
        ui_keys = set(re.findall(r'_def721\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W722 (26/10/2026) - tab721' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh721_num", "mh721_nneg", "mh721_pos",
                     "mh721_int_pos", "mh721_int_nneg",
                     "mh721_eta_valido", "mh721_potenza_freddo",
                     "mh721_energia_el", "mh721_calore_motore",
                     "mh721_calore_solare", "mh721_calore_backup",
                     "mh721_energia_gas_backup",
                     "mh721_costo_annuo", "mh721_risparmio",
                     "mh721_capex_chiller", "mh721_capex_alt",
                     "mh721_anni_sostituzione",
                     "mh721_flussi", "mh721_van_flussi",
                     "mh721_tir_flussi", "mh721_payback_flussi",
                     "mh721_verdetto", "mh721_co2_evitata",
                     "mh721_valida", "_mh721_neutro",
                     "mh721_calcola", "mh721_sensitivita",
                     "mh721_csv", "mh721_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_nessun_identificatore_futura_tab(self):
        assert "mh722" not in _helpers_src()
        assert "mh722" not in _ui_src()
        assert "st722" not in _ui_src()
        assert "tab722" not in _ui_src()

    def test_nessun_residuo_tab_precedente(self):
        # Niente residui della tab precedente
        # (mh720 / tab720 / st720) in helpers/UI:
        # il test puo' citare tab720 come tab
        # precedente, i frammenti no.
        assert "mh720" not in _helpers_src()
        assert "mh720" not in _ui_src()
        assert "st720" not in _ui_src()
        assert "tab720" not in _helpers_src()
        assert "tab720" not in _ui_src()

    def test_chain_riferimento_tab_precedente(self):
        # Questo file test fa riferimento alla
        # tab precedente tab720 (syngas)
        # come punto di confronto e la nuova tab
        # e' tab721.
        src = Path(__file__).read_text(encoding="utf-8")
        assert "tab720" in src
        assert "tab721" in src
        assert _ui_src().startswith("    with tab721:")

    def test_helpers_parse_ast(self):
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w722_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE721) == 1

    def test_blocco_with_tab721(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab721:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE721

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st721_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 31, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st721_") for k in keys)

    def test_chiavi_st_input_sono_27(self):
        """Le 27 chiavi di input/bottone (26 input +
        bottone calcola) sono tutte presenti; le
        altre 4 sono solo chiavi di
        visualizzazione (fig, heatmap, flussi, CSV)."""
        keys = re.findall(r'key="(st721_[a-z0-9_]+)"', _ui_src())
        attese = ["st721_domanda", "st721_ore",
                  "st721_eer", "st721_cop_ass",
                  "st721_area", "st721_irraggiamento",
                  "st721_eta_coll", "st721_eta_cald",
                  "st721_p_el", "st721_p_gas",
                  "st721_opex_chiller", "st721_opex_ass",
                  "st721_opex_solare", "st721_c_chiller",
                  "st721_fisso_chiller", "st721_c_coll",
                  "st721_fisso_coll", "st721_c_ass",
                  "st721_fisso_ass", "st721_vita_chiller",
                  "st721_vita_ass", "st721_vita_progetto",
                  "st721_wacc", "st721_tolleranza",
                  "st721_f_el", "st721_f_gas",
                  "st721_calcola"]
        assert len(attese) == 27
        for k in attese:
            assert k in keys, k

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg721" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg721") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg721")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Potenza frigorifera (kW)" in src
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
        assert "assorbitore" in src
        assert "collettori" in src
        assert "solare" in src
        assert "backup" in src

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Costo annuo baseline (chiller elettrico)" in src
        assert "Costo annuo alternativa (assorbitore solare)" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh721_csv" in src
        assert "raffrescamento_solare_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh721_sensitivita" in src
        assert "Heatmap" in src
        assert "Prezzo elettricità" in src
        assert "Rendimento collettori" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st721_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W722 (26/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab721:")
