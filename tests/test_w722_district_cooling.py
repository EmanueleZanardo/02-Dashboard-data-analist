"""Test tab722 "❄️🏙️ District cooling: il freddo centralizzato paga contro i chiller singoli?"

Tab precedente tab721 (raffrescamento solare,
w722); nuova tab tab722 (district cooling,
w723). La tab722 replica ESATTAMENTE la
semantica economica delle tab650-721:
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
domanda frigorifera 10000 MWh/a; ore
equivalenti 2500 h; COP centrale 5,5; COP
chiller singoli 3,5; perdite di rete 0,08;
prezzo elettricita' 250 EUR/MWh; opex
chiller singoli 150000 EUR/anno; opex
centrale 200000 EUR/anno; costo singolo
350 EUR/kW; costo fisso singoli 100000 EUR;
costo centrale 500 EUR/kW; costo fisso
centrale 300000 EUR; costo fisso rete
1500000 EUR; vita singoli 15 anni; vita
centrale 25 anni; vita di progetto 25 anni;
WACC 0,05 (5 %); tolleranza 0,10 (10 % del
|CAPEX_delta|); fattore elettrico 0,35
t/MWh.

- potenza_freddo_kw = 4000.0
- energia_singoli_mwh_a = 2857.1428571428573
- calore_centrale_mwh_a = 10869.565217391304
- energia_centrale_mwh_a = 1976.284584980237
- costo_base_eur_a = 864285.7142857143
- costo_alt_eur_a = 694071.1462450593
- risparmio_eur_a = 170214.568040655
- capex_singoli_eur = 1500000.0
- capex_alt_eur = 3800000.0
- capex_delta_eur = 2300000.0
- anni_sost_singoli = [15]
- anni_sost_centrale = []
- co2_evitata_t_a = 308.3003952569171
- van = 820520.3334346986
- tir = 7.95426428881052
- payback = 14
- verdetto = 'CONVIENTE'

Scomposizione: P_freddo 10000 x 1000 / 2500 =
4000.0 kW; E_singoli 10000 / 3,5 =
2857.1428571428573 MWh/a; Q_centrale 10000 /
(1 - 0,08) = 10869.565217391304 MWh/a (la
centrale produce anche le perdite di rete);
E_centrale 10869.565217391304 / 5,5 =
1976.284584980237 MWh/a; C_base
2857.1428571428573 x 250 + 150000 =
864285.7142857143 EUR/anno; C_alt
1976.284584980237 x 250 + 200000 =
694071.1462450593 EUR/anno; risparmio
864285.7142857143 - 694071.1462450593 =
170214.568040655 EUR/anno; CAPEX singoli
4000.0 x 350 + 100000 = 1500000.0 EUR;
CAPEX alternativa 4000.0 x 500 + 300000 +
1500000 = 3800000.0 EUR; CAPEX_delta
3800000.0 - 1500000.0 = 2300000.0 EUR;
sostituzioni: floor(15) = 15, multiplo 15
< 25 -> [15] per i singoli; floor(25) =
25, nessun multiplo < 25 -> [] per la
centrale; flussi: anno 0 -2300000.0,
anni 1-14 e 16-25 risparmio
170214.568040655, anno 15 risparmio +
CAPEX singoli = 1670214.568040655; VAN
820520.3334346986 a WACC 5 % su 25 anni;
TIR 7.95426428881052 % (il tasso che
azzera il VAN dei flussi sopra); payback
14 (il cumulato diventa positivo
all'anno 14: -2300000.0 + 13 x
170214.568040655 = -87210.620471485
all'anno 13, poi + 170214.568040655 =
83003.94756917 all'anno 14); CO2
(2857.1428571428573 - 1976.284584980237)
x 0,35 = 308.3003952569171 t/anno
(positiva e INFORMATIVA: la centrale
consuma meno elettricita' dei singoli);
VAN >= 0 -> CONVIENTE.

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
    if (p / "w723_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w723_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w723_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w723_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w723_helpers.py: {missing}")
    return out


_F = _load("mh722_num", "mh722_nneg", "mh722_pos",
           "mh722_int_pos", "mh722_int_nneg",
           "mh722_perdite_valida", "mh722_potenza_freddo",
           "mh722_energia_singoli", "mh722_calore_centrale",
           "mh722_energia_centrale",
           "mh722_costo_annuo", "mh722_risparmio",
           "mh722_capex_singoli", "mh722_capex_alt",
           "mh722_anni_sostituzione",
           "mh722_flussi", "mh722_van_flussi",
           "mh722_tir_flussi", "mh722_payback_flussi",
           "mh722_verdetto", "mh722_co2_evitata",
           "mh722_valida", "_mh722_neutro",
           "mh722_calcola", "mh722_sensitivita",
           "mh722_csv", "mh722_demo", "demo_calcoli")

TITLE722 = ("❄️🏙️ District cooling: il freddo centralizzato "
            "paga contro i chiller singoli?")

P_FR_DEMO = 4000.0
E_SINGOLI_DEMO = 2857.1428571428573
Q_CENTRALE_DEMO = 10869.565217391304
E_CENTRALE_DEMO = 1976.284584980237
C_BASE_DEMO = 864285.7142857143
C_ALT_DEMO = 694071.1462450593
RISPARMIO_DEMO = 170214.568040655
CAPEX_SINGOLI_DEMO = 1500000.0
CAPEX_ALT_DEMO = 3800000.0
DELTA_DEMO = 2300000.0
CO2_DEMO = 308.3003952569171
VAN_DEMO = 820520.3334346986
TIR_DEMO = 7.95426428881052
PAYBACK_DEMO = 14
VITA_DEMO = 25
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w723_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w723_ui.py").read_text(encoding="utf-8")


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh722_demo"]()
        d.update(kw)
        return _F["mh722_valida"](**d)

    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh722_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh722_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh722_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh722_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh722_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh722_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh722_pos"](0.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh722_int_pos"](2.5, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh722_int_pos"](25.0, "x") == 25

    def test_int_nneg_accetta_zero(self):
        assert _F["mh722_int_nneg"](0, "x") == 0

    def test_perdite_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh722_perdite_valida"](0.0, "x")

    def test_perdite_rifiuta_uno(self):
        with pytest.raises(ValueError):
            _F["mh722_perdite_valida"](1.0, "x")

    def test_perdite_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh722_perdite_valida"](1.2, "x")

    def test_perdite_accetta_intervallo_aperto(self):
        assert _F["mh722_perdite_valida"](0.08, "x") == 0.08
        assert _F["mh722_perdite_valida"](0.99, "x") == 0.99

    def test_perdite_zero_e_uno_non_valide(self):
        assert self._val(perdite_rete=0.0)["valido"] is False
        assert self._val(perdite_rete=1.0)["valido"] is False

    def test_cop_sopra_uno_validi(self):
        # COP sono coefficienti di
        # prestazione, non rendimenti: possono
        # superare 1 (COP 5,5 gia' nella demo).
        assert self._val(cop_centrale=7.0)["valido"] is True
        assert self._val(cop_singoli=6.0)["valido"] is True

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_domanda_zero_non_valida(self):
        assert self._val(domanda_freddo_mwh_a=0.0)["valido"] is False

    def test_ore_zero_non_valide(self):
        assert self._val(ore_eq=0.0)["valido"] is False

    def test_cop_zero_non_validi(self):
        assert self._val(cop_centrale=0.0)["valido"] is False
        assert self._val(cop_singoli=0.0)["valido"] is False

    def test_negativi_non_validi(self):
        for k in ("prezzo_el_eur_mwh",
                  "opex_singoli_eur_a",
                  "opex_centrale_eur_a",
                  "costo_singolo_eur_kw", "fisso_singolo_eur",
                  "costo_centrale_eur_kw",
                  "fisso_centrale_eur", "fisso_rete_eur",
                  "wacc_frac", "tolleranza_frac",
                  "fattore_el_t_mwh"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_vite_zero_non_valide(self):
        assert self._val(vita_singoli_anni=0)["valido"] is False
        assert self._val(vita_centrale_anni=0)["valido"] is False

    def test_vite_non_intere_non_valide(self):
        assert self._val(vita_singoli_anni=15.5)["valido"] is False
        assert self._val(vita_centrale_anni=25.5)["valido"] is False

    def test_vita_progetto_zero_non_valida(self):
        assert self._val(vita_progetto_anni=0)["valido"] is False

    def test_tolleranza_sopra_uno_valida_brief(self):
        assert self._val(tolleranza_frac=1.5)["valido"] is True

    def test_wacc_senza_tetto_superiore(self):
        assert self._val(wacc_frac=1.5)["valido"] is True

    def test_nan_non_valido(self):
        assert self._val(perdite_rete=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(domanda_freddo_mwh_a=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(vita_centrale_anni=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(perdite_rete="0.08")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(prezzo_el_eur_mwh=0.0)["valido"] is True
        assert self._val(costo_singolo_eur_kw=0.0)["valido"] is True
        assert self._val(fisso_rete_eur=0.0)["valido"] is True
        assert self._val(opex_centrale_eur_a=0.0)["valido"] is True
        assert self._val(wacc_frac=0.0)["valido"] is True
        assert self._val(tolleranza_frac=0.0)["valido"] is True
        assert self._val(fattore_el_t_mwh=0.0)["valido"] is True

class TestFunzioni:
    def test_potenza_freddo_demo(self):
        assert _F["mh722_potenza_freddo"](
            10000.0, 2500.0) == pytest.approx(P_FR_DEMO, rel=REL)

    def test_energia_singoli_demo(self):
        assert _F["mh722_energia_singoli"](
            10000.0, 3.5) == pytest.approx(E_SINGOLI_DEMO, rel=REL)

    def test_energia_singoli_cresce_con_cop_basso(self):
        assert _F["mh722_energia_singoli"](
            10000.0, 2.0) > _F["mh722_energia_singoli"](
            10000.0, 3.5)

    def test_calore_centrale_demo(self):
        assert _F["mh722_calore_centrale"](
            10000.0, 0.08) == pytest.approx(Q_CENTRALE_DEMO, rel=REL)

    def test_calore_centrale_cresce_con_perdite(self):
        assert _F["mh722_calore_centrale"](
            10000.0, 0.20) > _F["mh722_calore_centrale"](
            10000.0, 0.08)

    def test_calore_centrale_perdite_zero_rifiutato(self):
        with pytest.raises(ValueError):
            _F["mh722_calore_centrale"](10000.0, 0.0)

    def test_energia_centrale_demo(self):
        assert _F["mh722_energia_centrale"](
            Q_CENTRALE_DEMO, 5.5) == pytest.approx(
            E_CENTRALE_DEMO, rel=REL)

    def test_costo_annuo_demo(self):
        assert _F["mh722_costo_annuo"](
            E_SINGOLI_DEMO, 250.0, 150000.0) == pytest.approx(
            C_BASE_DEMO, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh722_risparmio"](
            C_BASE_DEMO, C_ALT_DEMO) == pytest.approx(
            RISPARMIO_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh722_risparmio"](
            100000.0, 150000.0) == pytest.approx(-50000.0, rel=REL)

    def test_capex_singoli_demo(self):
        assert _F["mh722_capex_singoli"](
            P_FR_DEMO, 350.0, 100000.0) == pytest.approx(
            CAPEX_SINGOLI_DEMO, rel=REL)

    def test_capex_alt_demo(self):
        assert _F["mh722_capex_alt"](
            P_FR_DEMO, 500.0, 300000.0,
            1500000.0) == pytest.approx(
            CAPEX_ALT_DEMO, rel=REL)

    def test_capex_delta_demo_non_clampato(self):
        delta = _F["mh722_capex_alt"](
            P_FR_DEMO, 500.0, 300000.0,
            1500000.0) - _F["mh722_capex_singoli"](
            P_FR_DEMO, 350.0, 100000.0)
        assert delta == pytest.approx(DELTA_DEMO, rel=REL)
        # Delta negativo possibile: centrale
        # piu' economica dei singoli.
        assert _F["mh722_capex_alt"](
            P_FR_DEMO, 100.0, 0.0, 0.0) - _F["mh722_capex_singoli"](
            P_FR_DEMO, 350.0, 100000.0) < 0.0

    def test_anni_sostituzione_demo(self):
        assert _F["mh722_anni_sostituzione"](15, 25) == [15]
        assert _F["mh722_anni_sostituzione"](25, 25) == []

    def test_anni_sostituzione_multipli(self):
        assert _F["mh722_anni_sostituzione"](10, 25) == [10, 20]
        assert _F["mh722_anni_sostituzione"](5, 25) == [5, 10, 15, 20]

    def test_anni_sostituzione_floor_non_intero(self):
        assert _F["mh722_anni_sostituzione"](10.5, 25) == [10, 20]

    def test_anni_sostituzione_sotto_anno_vuota(self):
        assert _F["mh722_anni_sostituzione"](0.5, 25) == []

    def test_anni_sostituzione_esclude_vita_progetto(self):
        assert _F["mh722_anni_sostituzione"](25, 25) == []
        assert _F["mh722_anni_sostituzione"](15, 25) == [15]

    def test_co2_evitata_demo(self):
        assert _F["mh722_co2_evitata"](
            E_SINGOLI_DEMO, E_CENTRALE_DEMO, 0.35) == \
            pytest.approx(CO2_DEMO, rel=REL)
        assert CO2_DEMO > 0.0

    def test_co2_evitata_puo_essere_negativa(self):
        assert _F["mh722_co2_evitata"](
            1000.0, 2000.0, 0.35) == pytest.approx(
            -350.0, rel=REL)

    def test_co2_evitata_zero_se_fattore_zero(self):
        assert _F["mh722_co2_evitata"](
            E_SINGOLI_DEMO, E_CENTRALE_DEMO, 0.0) == \
            pytest.approx(0.0, abs=1e-9)

    def test_van_flussi_demo(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 14 + \
            [RISPARMIO_DEMO + CAPEX_SINGOLI_DEMO] + \
            [RISPARMIO_DEMO] * 10
        assert len(flussi) == 26
        assert abs(_F["mh722_van_flussi"](
            flussi, 0.05) - VAN_DEMO) <= 1.0

    def test_van_flussi_tasso_zero(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 25
        atteso = -DELTA_DEMO + RISPARMIO_DEMO * 25
        assert _F["mh722_van_flussi"](
            flussi, 0.0) == pytest.approx(atteso, rel=1e-12)

    def test_van_flussi_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh722_van_flussi"]([100.0, 100.0], -0.01)

    def test_flussi_demo_con_sostituzioni(self):
        flussi = _F["mh722_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CAPEX_SINGOLI_DEMO, CAPEX_ALT_DEMO, [15], [], 25)
        assert len(flussi) == 26
        assert flussi[0] == pytest.approx(-DELTA_DEMO, rel=REL)
        assert flussi[1] == pytest.approx(RISPARMIO_DEMO, rel=REL)
        assert flussi[14] == pytest.approx(RISPARMIO_DEMO, rel=REL)
        assert flussi[15] == pytest.approx(
            RISPARMIO_DEMO + CAPEX_SINGOLI_DEMO, rel=REL)
        assert flussi[25] == pytest.approx(RISPARMIO_DEMO, rel=REL)

    def test_flussi_formula_sostituzione_centrale(self):
        flussi = _F["mh722_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CAPEX_SINGOLI_DEMO, CAPEX_ALT_DEMO, [], [10], 25)
        assert flussi[10] == pytest.approx(
            RISPARMIO_DEMO - CAPEX_ALT_DEMO, rel=REL)

    def test_flussi_formula_sostituzione_entrambi(self):
        flussi = _F["mh722_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CAPEX_SINGOLI_DEMO, CAPEX_ALT_DEMO, [10], [10], 25)
        assert flussi[10] == pytest.approx(
            RISPARMIO_DEMO - CAPEX_ALT_DEMO + CAPEX_SINGOLI_DEMO,
            rel=REL)

    def test_tir_demo(self):
        flussi = _F["mh722_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CAPEX_SINGOLI_DEMO, CAPEX_ALT_DEMO, [15], [], 25)
        tir = _F["mh722_tir_flussi"](flussi)
        assert tir is not None
        assert tir * 100.0 == pytest.approx(TIR_DEMO, rel=1e-9)

    def test_tir_none_tutti_flussi_non_negativi(self):
        assert _F["mh722_tir_flussi"](
            [1000.0] + [100.0] * 10) is None

    def test_tir_none_nessun_cambio_segno_negativo(self):
        # Tutti i flussi <= 0: nessun tasso azzera il VAN.
        assert _F["mh722_tir_flussi"](
            [-1000.0] + [-100.0] * 10) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh722_tir_flussi"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo_quattordici(self):
        flussi = _F["mh722_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CAPEX_SINGOLI_DEMO, CAPEX_ALT_DEMO, [15], [], 25)
        assert _F["mh722_payback_flussi"](flussi) == PAYBACK_DEMO

    def test_payback_none_se_mai(self):
        assert _F["mh722_payback_flussi"](
            [-5000000000.0] + [RISPARMIO_DEMO] * 25) is None

    def test_payback_zero_se_cumulato_anno_zero_non_negativo(self):
        assert _F["mh722_payback_flussi"](
            [0.0] + [RISPARMIO_DEMO] * 25) == 0

    def test_verdetto_conviente_demo(self):
        assert _F["mh722_verdetto"](
            VAN_DEMO, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == VERDETTO_DEMO

    def test_verdetto_van_zero_conviente(self):
        assert _F["mh722_verdetto"](
            0.0, DELTA_DEMO, 0.10, RISPARMIO_DEMO) == "CONVIENTE"

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh722_verdetto"](
            -100.0, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh722_verdetto"](
            -0.10 * abs(DELTA_DEMO), DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_oltre_limite(self):
        assert _F["mh722_verdetto"](
            -0.10 * abs(DELTA_DEMO) - 1.0, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_non_positivo(
            self):
        assert _F["mh722_verdetto"](
            1000.0, DELTA_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh722_verdetto"](
            1000.0, DELTA_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_delta_zero_van_positivo_conviente(
            self):
        assert _F["mh722_verdetto"](
            1000.0, 0.0, 0.10, RISPARMIO_DEMO) == "CONVIENTE"

    def test_verdetto_capex_delta_zero_van_negativo_non_conviente(
            self):
        assert _F["mh722_verdetto"](
            -1.0, 0.0, 0.10, RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh722_verdetto"](100.0, DELTA_DEMO, -0.01, RISPARMIO_DEMO)

class TestDemo:
    def _bc(self, **kw):
        d = _F["mh722_demo"]()
        d.update(kw)
        return _F["mh722_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["potenza_freddo_kw"] == pytest.approx(
            P_FR_DEMO, rel=REL)
        assert c["energia_singoli_mwh_a"] == pytest.approx(
            E_SINGOLI_DEMO, rel=REL)
        assert c["calore_centrale_mwh_a"] == pytest.approx(
            Q_CENTRALE_DEMO, rel=REL)
        assert c["energia_centrale_mwh_a"] == pytest.approx(
            E_CENTRALE_DEMO, rel=REL)
        assert c["costo_base_eur_a"] == pytest.approx(
            C_BASE_DEMO, rel=REL)
        assert c["costo_alt_eur_a"] == pytest.approx(
            C_ALT_DEMO, rel=REL)
        assert c["risparmio_eur_a"] == pytest.approx(
            RISPARMIO_DEMO, rel=REL)
        assert c["capex_singoli_eur"] == pytest.approx(
            CAPEX_SINGOLI_DEMO, rel=REL)
        assert c["capex_alt_eur"] == pytest.approx(
            CAPEX_ALT_DEMO, rel=REL)
        assert c["capex_delta_eur"] == pytest.approx(
            DELTA_DEMO, rel=REL)
        assert c["anni_sost_singoli"] == [15]
        assert c["anni_sost_centrale"] == []
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
        d = _F["mh722_demo"]()
        b = _F["mh722_calcola"](**d)
        coppie = [("potenza_freddo_kw", P_FR_DEMO),
                  ("energia_singoli_mwh_a", E_SINGOLI_DEMO),
                  ("calore_centrale_mwh_a", Q_CENTRALE_DEMO),
                  ("energia_centrale_mwh_a", E_CENTRALE_DEMO),
                  ("costo_base_eur_a", C_BASE_DEMO),
                  ("costo_alt_eur_a", C_ALT_DEMO),
                  ("risparmio_eur_a", RISPARMIO_DEMO),
                  ("capex_singoli_eur", CAPEX_SINGOLI_DEMO),
                  ("capex_alt_eur", CAPEX_ALT_DEMO),
                  ("capex_delta_eur", DELTA_DEMO),
                  ("co2_evitata_t_a", CO2_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert b["anni_sost_singoli"] == [15]
        assert b["anni_sost_centrale"] == []
        assert abs(b["van"] - VAN_DEMO) <= 1.0
        assert abs(b["tir"] - TIR_DEMO) <= 0.01
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh722_demo"]()
        assert d["domanda_freddo_mwh_a"] == 10000.0
        assert d["ore_eq"] == 2500.0
        assert d["cop_centrale"] == 5.5
        assert d["cop_singoli"] == 3.5
        assert d["perdite_rete"] == 0.08
        assert d["prezzo_el_eur_mwh"] == 250.0
        assert d["opex_singoli_eur_a"] == 150000.0
        assert d["opex_centrale_eur_a"] == 200000.0
        assert d["costo_singolo_eur_kw"] == 350.0
        assert d["fisso_singolo_eur"] == 100000.0
        assert d["costo_centrale_eur_kw"] == 500.0
        assert d["fisso_centrale_eur"] == 300000.0
        assert d["fisso_rete_eur"] == 1500000.0
        assert d["vita_singoli_anni"] == 15
        assert d["vita_centrale_anni"] == 25
        assert d["vita_progetto_anni"] == 25
        assert d["wacc_frac"] == 0.05
        assert d["tolleranza_frac"] == 0.10
        assert d["fattore_el_t_mwh"] == 0.35
        assert len(d) == 19

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("potenza_freddo_kw",
                       "energia_singoli_mwh_a",
                       "calore_centrale_mwh_a",
                       "energia_centrale_mwh_a",
                       "costo_base_eur_a",
                       "costo_alt_eur_a",
                       "risparmio_eur_a",
                       "capex_singoli_eur",
                       "capex_alt_eur",
                       "capex_delta_eur",
                       "co2_evitata_t_a", "van"):
            assert repr(c[chiave]) in doc, chiave
        assert repr(c["anni_sost_singoli"]) in doc
        assert repr(c["anni_sost_centrale"]) in doc
        assert f"tir = {repr(c['tir'])}" in doc
        assert "payback = 14" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_prezzo_el_basso_non_conviente(self):
        # Prezzo elettricita' 150 EUR/MWh: C_base
        # 578571,43, risparmio 82128,74, VAN
        # -420956,43, TIR 3,32 %, payback 15
        # -> NON_CONVIENTE.
        n = self._bc(prezzo_el_eur_mwh=150.0)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            82128.74082439311, rel=REL)
        assert abs(n["van"] - (-420956.4324054922)) <= 1.0
        assert abs(n["tir"] - 3.3180975171005085) <= 0.01
        assert n["payback"] == 15
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_prezzo_el_medio_conviente(self):
        # Prezzo elettricita' 200 EUR/MWh:
        # risparmio 126171,65, VAN 199781,95,
        # TIR 5,75 %, payback 15 -> CONVIENTE.
        n = self._bc(prezzo_el_eur_mwh=200.0)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            126171.65443252411, rel=REL)
        assert abs(n["van"] - 199781.9505146041) <= 1.0
        assert abs(n["tir"] - 5.751582047792279) <= 0.01
        assert n["payback"] == 15
        assert n["verdetto"] == "CONVIENTE"

    def test_cop_centrale_basso_risparmio_negativo(self):
        # COP centrale 3,0: E_centrale 3623,19,
        # C_alt 1105797,83 > C_base 864285,71 ->
        # risparmio negativo -> dict neutro
        # NON_CALCOLABILE.
        n = self._bc(cop_centrale=3.0)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_cop_centrale_medio_risparmio_negativo(self):
        # COP centrale 4,0: E_centrale 2717,39,
        # C_alt 879347,83 > C_base 864285,71 ->
        # risparmio -15062,11 -> dict neutro
        # NON_CALCOLABILE.
        n = self._bc(cop_centrale=4.0)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_perdite_alte_marginale(self):
        # Perdite di rete 0,20: Q_centrale 12500,
        # E_centrale 2272,73, risparmio 96103,90,
        # VAN -223991,37, TIR 4,12 %, payback 15
        # -> MARGINALE (|VAN| <= 10 % di delta).
        n = self._bc(perdite_rete=0.20)
        assert n["valid"] is True
        assert n["risparmio_eur_a"] == pytest.approx(
            96103.8961038962, rel=REL)
        assert abs(n["van"] - (-223991.36859430795)) <= 1.0
        assert abs(n["tir"] - 4.1239976844130375) <= 0.01
        assert n["payback"] == 15
        assert n["verdetto"] == "MARGINALE"

    def test_fisso_rete_alto_marginale(self):
        # Costo fisso rete 2350000 EUR:
        # CAPEX_delta 3150000, VAN -29479,67,
        # TIR 4,91 %, payback 15 -> MARGINALE.
        n = self._bc(fisso_rete_eur=2350000.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            3150000.0, rel=REL)
        assert abs(n["van"] - (-29479.66656530121)) <= 1.0
        assert abs(n["tir"] - 4.914742486163102) <= 0.01
        assert n["payback"] == 15
        assert n["verdetto"] == "MARGINALE"

    def test_vite_corte_sostituzioni_entrambi(self):
        # Vita 10 anni per entrambi: sost [10, 20]
        # per entrambi; flusso anno 10 e 20 =
        # risparmio - CAPEX alternativa + CAPEX
        # singoli = -2129785,43; VAN
        # -2179851,61, TIR -19,81 %, payback
        # None -> NON_CONVIENTE.
        n = self._bc(vita_singoli_anni=10, vita_centrale_anni=10)
        assert n["valid"] is True
        assert n["anni_sost_singoli"] == [10, 20]
        assert n["anni_sost_centrale"] == [10, 20]
        assert n["df_flussi"]["Flusso (€/anno)"].iloc[10] == \
            pytest.approx(-2129785.431959345, rel=REL)
        assert n["df_flussi"]["Flusso (€/anno)"].iloc[20] == \
            pytest.approx(-2129785.431959345, rel=REL)
        assert abs(n["van"] - (-2179851.607453403)) <= 1.0
        assert abs(n["tir"] - (-19.807527026740495)) <= 0.01
        assert n["payback"] is None
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_domanda_zero_neutro(self):
        n = self._bc(domanda_freddo_mwh_a=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_perdite_uno_neutro(self):
        n = self._bc(perdite_rete=1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_cop_zero_neutro(self):
        n = self._bc(cop_centrale=0.0)
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
        n = self._bc(perdite_rete=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(domanda_freddo_mwh_a=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(vita_centrale_anni=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_zero_calcolabile(self):
        # WACC 0: VAN = somma flussi =
        # -2300000 + 170214,57 x 25 + 1500000 =
        # 3455364,20.
        n = self._bc(wacc_frac=0.0)
        assert n["van"] == pytest.approx(
            3455364.201016375, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_tir_none_caso_demo_senza_investimento(self):
        # CAPEX delta negativo e risparmio positivo:
        # tutti i flussi >= 0 -> TIR None.
        n = self._bc(costo_centrale_eur_kw=100.0, fisso_centrale_eur=0.0,
                     fisso_rete_eur=0.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] < 0.0
        assert n["tir"] is None
        assert n["payback"] == 0
        assert n["verdetto"] == "CONVIENTE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh722_neutro"]()
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
        n = _F["_mh722_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "domanda_freddo_mwh_a", "ore_eq",
                       "cop_centrale", "cop_singoli",
                       "perdite_rete",
                       "potenza_freddo_kw",
                       "energia_singoli_mwh_a",
                       "calore_centrale_mwh_a",
                       "energia_centrale_mwh_a",
                       "costo_base_eur_a",
                       "costo_alt_eur_a",
                       "risparmio_eur_a",
                       "capex_singoli_eur",
                       "capex_alt_eur",
                       "capex_delta_eur",
                       "anni_sost_singoli",
                       "anni_sost_centrale",
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
        assert "Potenza frigorifera (kW)" in voci
        assert "Elettricita' chiller singoli (MWh/a)" in voci
        assert "Freddo centrale (MWh/a)" in voci
        assert "Elettricita' centrale (MWh/a)" in voci
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
            pytest.approx(RISPARMIO_DEMO + CAPEX_SINGOLI_DEMO,
                          rel=REL)

class TestSensitivita:
    def _ing(self):
        return _F["mh722_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh722_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.9", "x1.0", "x1.1"]
        assert list(s.index) == ["x0.9", "x1.0", "x1.1"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh722_sensitivita"](self._ing())
        assert abs(s.loc["x1.0", "x1.0"] - VAN_DEMO) <= 1.0

    def test_sensitivita_crescente_con_prezzo_el(self):
        s = _F["mh722_sensitivita"](self._ing())
        for colonna in ("x0.9", "x1.0", "x1.1"):
            assert s.loc["x0.9", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.1", colonna]

    def test_sensitivita_crescente_con_cop_centrale(self):
        s = _F["mh722_sensitivita"](self._ing())
        for riga in ("x0.9", "x1.0", "x1.1"):
            assert s.loc[riga, "x0.9"] < \
                s.loc[riga, "x1.0"] < \
                s.loc[riga, "x1.1"]

    def test_sensitivita_nessuna_colonna_degenere(self):
        s = _F["mh722_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_nessuna_colonna_costante(self):
        s = _F["mh722_sensitivita"](self._ing())
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3

    def test_sensitivita_angoli(self):
        s = _F["mh722_sensitivita"](self._ing())
        assert abs(s.loc["x0.9", "x0.9"] - (-186189.99271135384)) <= 1.0
        assert abs(s.loc["x0.9", "x1.1"] - 1079884.7976268393) <= 1.0
        assert abs(s.loc["x1.1", "x0.9"] - 279805.9158340751) <= 1.0
        assert abs(s.loc["x1.1", "x1.1"] - 1827230.6595807548) <= 1.0

    def test_sensitivita_con_sostituzioni_ricalcolate(self):
        # Con vite 10 anni per entrambi la griglia
        # deve includere le sostituzioni anni 10 e 20:
        # il centro deve coincidere col VAN
        # del caso con vite 10 anni.
        ing = self._ing()
        ing["vita_singoli_anni"] = 10
        ing["vita_centrale_anni"] = 10
        s = _F["mh722_sensitivita"](ing)
        assert abs(s.loc["x1.0", "x1.0"] - (-2179851.607453403)) <= 1.0


class TestCsv:
    def _ing(self):
        return _F["mh722_demo"]()

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh722_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") == 35

    def test_csv_contiene_verdetto_e_risparmio(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh722_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "risparmio_eur_a" in txt
        assert "costo_base_eur_a" in txt
        assert "costo_alt_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "domanda_freddo_mwh_a" in txt
        assert "potenza_freddo_kw" in txt
        assert "co2_evitata_t_a" in txt
        assert "perdite_rete" in txt
        assert "calore_centrale_mwh_a" in txt
        assert "capex_delta_eur" in txt
        assert "fisso_rete_eur" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh722_csv"](bc, self._ing())
        assert f"risparmio_eur_a;{bc['risparmio_eur_a']}" in txt
        assert f"costo_base_eur_a;{bc['costo_base_eur_a']}" in txt
        assert "domanda_freddo_mwh_a;10000.0" in txt
        assert "opex_centrale_eur_a;200000.0" in txt
        assert f"capex_delta_eur;{bc['capex_delta_eur']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def722["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def722\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 19, ui_keys
        demo_keys = set(_F["mh722_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh722_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh722_demo():")
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
        ui_keys = set(re.findall(r'_def722\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W723 (26/10/2026) - tab722' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh722_num", "mh722_nneg", "mh722_pos",
                     "mh722_int_pos", "mh722_int_nneg",
                     "mh722_perdite_valida", "mh722_potenza_freddo",
                     "mh722_energia_singoli", "mh722_calore_centrale",
                     "mh722_energia_centrale",
                     "mh722_costo_annuo", "mh722_risparmio",
                     "mh722_capex_singoli", "mh722_capex_alt",
                     "mh722_anni_sostituzione",
                     "mh722_flussi", "mh722_van_flussi",
                     "mh722_tir_flussi", "mh722_payback_flussi",
                     "mh722_verdetto", "mh722_co2_evitata",
                     "mh722_valida", "_mh722_neutro",
                     "mh722_calcola", "mh722_sensitivita",
                     "mh722_csv", "mh722_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_nessun_identificatore_futura_tab(self):
        assert "mh723" not in _helpers_src()
        assert "mh723" not in _ui_src()
        assert "st723" not in _ui_src()
        assert "tab723" not in _ui_src()

    def test_nessun_residuo_tab_precedente(self):
        # Niente residui della tab precedente
        # (mh721 / tab721 / st721) in helpers/UI:
        # il test puo' citare tab721 come tab
        # precedente, i frammenti no.
        assert "mh721" not in _helpers_src()
        assert "mh721" not in _ui_src()
        assert "st721" not in _ui_src()
        assert "tab721" not in _helpers_src()
        assert "tab721" not in _ui_src()

    def test_chain_riferimento_tab_precedente(self):
        # Questo file test fa riferimento alla
        # tab precedente tab721 (raffrescamento
        # solare) come punto di confronto e la
        # nuova tab e' tab722.
        src = Path(__file__).read_text(encoding="utf-8")
        assert "tab721" in src
        assert "tab722" in src
        assert _ui_src().startswith("    with tab722:")

    def test_helpers_parse_ast(self):
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w723_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE722) == 1

    def test_blocco_with_tab722(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab722:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE722

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st722_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 24, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st722_") for k in keys)

    def test_chiavi_st_input_sono_20(self):
        """Le 20 chiavi di input/bottone (19 input +
        bottone calcola) sono tutte presenti; le
        altre 4 sono solo chiavi di
        visualizzazione (fig, heatmap, flussi, CSV)."""
        keys = re.findall(r'key="(st722_[a-z0-9_]+)"', _ui_src())
        attese = ["st722_domanda", "st722_ore",
                  "st722_cop_centrale", "st722_cop_singoli",
                  "st722_perdite", "st722_p_el",
                  "st722_opex_singoli", "st722_opex_centrale",
                  "st722_c_singolo", "st722_fisso_singolo",
                  "st722_c_centrale", "st722_fisso_centrale",
                  "st722_fisso_rete", "st722_vita_singoli",
                  "st722_vita_centrale", "st722_vita_progetto",
                  "st722_wacc", "st722_tolleranza",
                  "st722_f_el",
                  "st722_calcola"]
        assert len(attese) == 20
        for k in attese:
            assert k in keys, k

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg722" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg722") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg722")
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
        assert "centrale" in src
        assert "perdite di rete" in src
        assert "assorbitore" in src
        assert "solare" in src
        assert "quinta generazione" in src
        assert "free-cooling" in src

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Costo annuo baseline (chiller singoli)" in src
        assert "Costo annuo alternativa (district cooling)" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh722_csv" in src
        assert "district_cooling_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh722_sensitivita" in src
        assert "Heatmap" in src
        assert "Prezzo elettricità" in src
        assert "COP centrale" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st722_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W723 (26/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab722:")
