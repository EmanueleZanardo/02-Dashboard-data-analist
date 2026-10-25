"""Test tab715 "🧂💧 Idrogeno in caverne saline: lo stoccaggio sotterraneo paga?"

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
volume caverna 500000 m3; pressione minima
60 bar; pressione massima 180 bar;
temperatura 300 K; costo caverna 30 EUR/m3;
costo fisso caverna 5000000 EUR; prezzo
cushion 2,5 EUR/kg; O&M caverna 800000
EUR/anno; capacita' serbatoio 30 MWh; costo
serbatoio 1500000 EUR; O&M serbatoio 30000
EUR/anno; vita in anni caverna 30; vita in
anni serbatoi 20; vita di progetto 30 anni;
WACC 0,06 (6 %); tolleranza 0,10 (10 % del
|CAPEX delta|); cicli annui 12; fattore rete
0,35 t/MWh.

- massa_lavoro_kg = 4849651.190762569
- massa_cushion_kg = 2424825.5953812846
- costo_cushion_eur = 6062063.988453211
- e_cap_mwh = 161638.87418811643
- n_tanks = 5388
- capex_cavern_eur = 26062063.98845321
- capex_tanks_eur = 8082000000.0
- capex_delta_eur = -8055937936.011547
- costo_base_eur_a = 161640000.0
- costo_alt_eur_a = 800000.0
- risparmio_eur_a = 160840000.0
- anni_sost_cavern = []
- anni_sost_tanks = [20]
- throughput_mwh_a = 1939666.4902573973
- co2_evitata_t_a = 678883.271590089
- van = 12789879181.110434
- tir = None
- payback = 0
- verdetto = 'CONVIENTE'

Scomposizione: massa lavoro 500000 x 120 x
100000 x 0,002016 / (8,314 x 300) =
4849651.190762569 kg; massa cushion 500000 x
60 x 100000 x 0,002016 / (8,314 x 300) =
2424825.5953812846 kg; E_cap 4849651.190762569
x 33,33 / 1000 = 161638.87418811643 MWh;
costo cushion 2424825.5953812846 x 2,5 =
6062063.988453211 EUR; CAPEX caverna 500000 x
30 + 6062063.988453211 + 5000000 =
26062063.98845321 EUR; n_serbatoi ceil(
161638.87418811643 / 30) = 5388 (5387 x 30 =
161610 < E_cap, 5388 x 30 = 161640);
CAPEX serbatoi 5388 x 1500000 = 8082000000.0
EUR; CAPEX delta 26062063.98845321 -
8082000000.0 = -8055937936.011547 EUR; C_base
5388 x 30000 = 161640000.0 EUR/anno; C_alt
800000.0 EUR/anno; risparmio 161640000.0 -
800000.0 = 160840000.0 EUR/anno; sostituzioni
caverna nessuna (vita 30, progetto 30),
serbatoi anno 20; flussi [-(-8055937936.011547),
160840000.0 x 30 con anno 20 =
8242840000.0]; VAN 12789879181.110437 a WACC
6 % su 30 anni; TIR None (tutti i flussi
>= 0: flusso anno 0 = -delta > 0, nessun
cambio di segno); payback 0 (cumulato anno 0
= 8055937936.011547 >= 0: la caverna costa
meno dei serbatoi gia' all'anno 0);
throughput 161638.87418811643 x 12 =
1939666.4902573973 MWh/anno; CO2
1939666.4902573973 x 0,35 = 678883.271590089
t/anno (informativa, basata sul throughput,
non differenziale: entrambi i rami stoccano
lo stesso idrogeno). VAN >= 0 -> CONVIENTE.
"""

import ast
import re
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _new_dir():
    p = Path(__file__).resolve().parent
    if (p / "w716_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w716_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w716_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w716_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w716_helpers.py: {missing}")
    return out


_F = _load("mh715_num", "mh715_nneg", "mh715_pos",
           "mh715_int_pos", "mh715_int_nneg",
           "mh715_massa_gas", "mh715_capacita_utile",
           "mh715_capex_cavern", "mh715_n_serbatoi",
           "mh715_capex_serbatoi",
           "mh715_costo_annuo_serbatoi",
           "mh715_risparmio", "mh715_anni_sostituzione",
           "mh715_flussi",
           "mh715_van_flussi", "mh715_tir_flussi",
           "mh715_payback_flussi", "mh715_verdetto",
           "mh715_throughput", "mh715_co2_evitata",
           "mh715_valida",
           "_mh715_neutro", "mh715_calcola",
           "mh715_sensitivita", "mh715_csv",
           "mh715_demo", "demo_calcoli")

TITLE715 = ("🧂💧 Idrogeno in caverne saline: "
            "lo stoccaggio sotterraneo paga?")

MASSA_LAV_DEMO = 4849651.190762569
MASSA_CUS_DEMO = 2424825.5953812846
COSTO_CUS_DEMO = 6062063.988453211
E_CAP_DEMO = 161638.87418811643
N_TANKS_DEMO = 5388
CX_CAV_DEMO = 26062063.98845321
CX_TANK_DEMO = 8082000000.0
DELTA_DEMO = -8055937936.011547
C_BASE_DEMO = 161640000.0
C_ALT_DEMO = 800000.0
RISPARMIO_DEMO = 160840000.0
THR_DEMO = 1939666.4902573973
CO2_EV_DEMO = 678883.271590089
VAN_DEMO = 12789879181.110434
PAYBACK_DEMO = 0
VITA_DEMO = 30
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w716_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w716_ui.py").read_text(encoding="utf-8")


class TestValidatori:
    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh715_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh715_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh715_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh715_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh715_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh715_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh715_pos"](0.0, "x")

    def test_pos_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh715_pos"](-1.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh715_int_pos"](2.5, "x")

    def test_int_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh715_int_pos"](0, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh715_int_pos"](30.0, "x") == 30

    def test_int_nneg_accetta_zero(self):
        assert _F["mh715_int_nneg"](0, "x") == 0

    def test_int_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh715_int_nneg"](-1, "x")


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh715_demo"]()
        d.update(kw)
        return _F["mh715_valida"](**d)

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_volume_zero_non_valido(self):
        assert self._val(volume_m3=0.0)["valido"] is False

    def test_volume_negativo_non_valido(self):
        assert self._val(volume_m3=-1.0)["valido"] is False

    def test_p_min_zero_non_valido(self):
        assert self._val(p_min_bar=0.0)["valido"] is False

    def test_p_max_uguale_p_min_non_valido(self):
        assert self._val(p_max_bar=60.0)["valido"] is False

    def test_p_max_minore_p_min_non_valido(self):
        assert self._val(p_max_bar=50.0)["valido"] is False

    def test_temp_zero_non_valida(self):
        assert self._val(temp_k=0.0)["valido"] is False

    def test_temp_negativa_non_valida(self):
        assert self._val(temp_k=-10.0)["valido"] is False

    def test_tank_cap_zero_non_valido(self):
        assert self._val(tank_cap_mwh=0.0)["valido"] is False

    def test_negativi_non_validi(self):
        for k in ("c_cavern_eur_m3", "fisso_cavern_eur",
                  "prezzo_cushion_eur_kg", "om_cavern_eur_a",
                  "c_tank_eur", "om_tank_eur_a",
                  "wacc_frac", "cicli_anno", "f_rete_t_mwh"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_vita_anni_zero_non_valida(self):
        assert self._val(vita_anni_cavern=0)["valido"] is False
        assert self._val(vita_anni_tanks=0)["valido"] is False

    def test_vita_anni_non_intera_non_valida(self):
        assert self._val(vita_anni_cavern=29.5)["valido"] is False

    def test_vita_progetto_zero_non_valida(self):
        assert self._val(vita_progetto_anni=0)["valido"] is False

    def test_vita_progetto_non_intera_non_valida(self):
        assert self._val(vita_progetto_anni=29.5)["valido"] is False

    def test_tolleranza_negativa_non_valida(self):
        assert self._val(tolleranza_frac=-0.01)["valido"] is False

    def test_tolleranza_sopra_uno_valida_brief(self):
        # Brief tab715: tol >= 0 senza tetto
        # superiore (diversa dalla quota [0, 1]
        # di tab714).
        assert self._val(tolleranza_frac=1.5)["valido"] is True

    def test_wacc_senza_tetto_superiore(self):
        assert self._val(wacc_frac=1.5)["valido"] is True

    def test_nan_non_valido(self):
        assert self._val(p_max_bar=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(volume_m3=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(volume_m3=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(p_min_bar="60")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(c_cavern_eur_m3=0.0)["valido"] is True
        assert self._val(om_cavern_eur_a=0.0)["valido"] is True
        assert self._val(fisso_cavern_eur=0.0)["valido"] is True
        assert self._val(prezzo_cushion_eur_kg=0.0)["valido"] is True
        assert self._val(cicli_anno=0.0)["valido"] is True
        assert self._val(f_rete_t_mwh=0.0)["valido"] is True


class TestFisicaEconomia:
    def test_massa_lavoro_demo(self):
        assert _F["mh715_massa_gas"](
            500000.0, 120.0, 300.0) == pytest.approx(
            MASSA_LAV_DEMO, rel=REL)

    def test_massa_cushion_demo(self):
        assert _F["mh715_massa_gas"](
            500000.0, 60.0, 300.0) == pytest.approx(
            MASSA_CUS_DEMO, rel=REL)

    def test_massa_rifiuta_pressione_negativa(self):
        with pytest.raises(ValueError):
            _F["mh715_massa_gas"](500000.0, -1.0, 300.0)

    def test_massa_rifiuta_temp_zero(self):
        with pytest.raises(ValueError):
            _F["mh715_massa_gas"](500000.0, 60.0, 0.0)

    def test_massa_conversione_bar_pa(self):
        # 1 m3 a 1 bar e 300 K: 100000 x 0,002016
        # / (8,314 x 300) = 0,0808... kg; senza
        # il fattore 100000 la massa sarebbe
        # 100000 volte piu' piccola.
        atteso = 100000.0 * 0.002016 / (8.314 * 300.0)
        assert _F["mh715_massa_gas"](
            1.0, 1.0, 300.0) == pytest.approx(atteso, rel=REL)
        assert atteso > 0.08 and atteso < 0.081

    def test_capacita_utile_demo(self):
        assert _F["mh715_capacita_utile"](
            MASSA_LAV_DEMO) == pytest.approx(
            E_CAP_DEMO, rel=REL)

    def test_capacita_fattore_lhv(self):
        # 1000 kg x 33,33 / 1000 = 33,33 MWh.
        assert _F["mh715_capacita_utile"](
            1000.0) == pytest.approx(33.33, rel=REL)

    def test_capex_cavern_demo_cushion_incluso(self):
        # Senza il cushion il CAPEX sarebbe
        # 20000000, non 26062063,99: il cushion
        # DEVE essere dentro il CAPEX caverna.
        assert _F["mh715_capex_cavern"](
            500000.0, 30.0, MASSA_CUS_DEMO, 2.5,
            5000000.0) == pytest.approx(
            CX_CAV_DEMO, rel=REL)
        assert CX_CAV_DEMO - 20000000.0 == pytest.approx(
            COSTO_CUS_DEMO, rel=REL)

    def test_capex_cavern_senza_cushion(self):
        assert _F["mh715_capex_cavern"](
            500000.0, 30.0, 0.0, 2.5,
            5000000.0) == pytest.approx(20000000.0, rel=REL)

    def test_n_serbatoi_demo_ceil(self):
        assert _F["mh715_n_serbatoi"](
            E_CAP_DEMO, 30.0) == N_TANKS_DEMO
        # 5387 x 30 = 161610 < E_cap: floor
        # darebbe 5387, serve il ceil.
        assert 5387 * 30.0 < E_CAP_DEMO
        assert 5388 * 30.0 >= E_CAP_DEMO

    def test_n_serbatoi_esatto(self):
        assert _F["mh715_n_serbatoi"](60.0, 30.0) == 2

    def test_n_serbatoi_ceil_sopra_esatto(self):
        assert _F["mh715_n_serbatoi"](60.0001, 30.0) == 3

    def test_n_serbatoi_zero_se_energia_zero(self):
        assert _F["mh715_n_serbatoi"](0.0, 30.0) == 0

    def test_n_serbatoi_rifiuta_cap_zero(self):
        with pytest.raises(ValueError):
            _F["mh715_n_serbatoi"](E_CAP_DEMO, 0.0)

    def test_capex_serbatoi_demo(self):
        assert _F["mh715_capex_serbatoi"](
            N_TANKS_DEMO, 1500000.0) == pytest.approx(
            CX_TANK_DEMO, rel=REL)

    def test_costo_base_demo(self):
        assert _F["mh715_costo_annuo_serbatoi"](
            N_TANKS_DEMO, 30000.0) == pytest.approx(
            C_BASE_DEMO, rel=REL)

    def test_risparmio_demo(self):
        assert _F["mh715_risparmio"](
            C_BASE_DEMO, C_ALT_DEMO) == pytest.approx(
            RISPARMIO_DEMO, rel=REL)

    def test_risparmio_puo_essere_negativo(self):
        assert _F["mh715_risparmio"](
            10000.0, 15000.0) == pytest.approx(
            -5000.0, rel=REL)

    def test_anni_sostituzione_demo(self):
        assert _F["mh715_anni_sostituzione"](30, 30) == []
        assert _F["mh715_anni_sostituzione"](20, 30) == [20]

    def test_anni_sostituzione_multipli(self):
        assert _F["mh715_anni_sostituzione"](10, 30) == [10, 20]
        assert _F["mh715_anni_sostituzione"](15, 30) == [15]

    def test_anni_sostituzione_sotto_anno_vuota(self):
        assert _F["mh715_anni_sostituzione"](0.5, 30) == []

    def test_anni_sostituzione_esclude_vita_progetto(self):
        assert _F["mh715_anni_sostituzione"](30, 30) == []

    def test_throughput_demo(self):
        assert _F["mh715_throughput"](
            E_CAP_DEMO, 12.0) == pytest.approx(
            THR_DEMO, rel=REL)

    def test_co2_evitata_demo(self):
        assert _F["mh715_co2_evitata"](
            THR_DEMO, 0.35) == pytest.approx(
            CO2_EV_DEMO, rel=REL)
        assert CO2_EV_DEMO > 0.0

    def test_co2_evitata_zero_se_fattore_zero(self):
        assert _F["mh715_co2_evitata"](
            THR_DEMO, 0.0) == pytest.approx(0.0, abs=1e-9)

    def test_co2_evitata_zero_se_cicli_zero(self):
        assert _F["mh715_throughput"](
            E_CAP_DEMO, 0.0) == pytest.approx(0.0, abs=1e-9)


class TestFinanza:
    def test_van_flussi_demo(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 30
        flussi[20] += CX_TANK_DEMO
        assert abs(_F["mh715_van_flussi"](
            flussi, 0.06) - VAN_DEMO) <= 1.0

    def test_van_flussi_tasso_zero(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 30
        flussi[20] += CX_TANK_DEMO
        atteso = (-DELTA_DEMO + RISPARMIO_DEMO * 30
                  + CX_TANK_DEMO)
        assert _F["mh715_van_flussi"](
            flussi, 0.0) == pytest.approx(atteso, rel=1e-12)

    def test_van_flussi_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh715_van_flussi"]([100.0, 100.0], -0.01)

    def test_flussi_demo(self):
        flussi = _F["mh715_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CX_TANK_DEMO, CX_CAV_DEMO, [20], [], 30)
        assert len(flussi) == 31
        assert flussi[0] == pytest.approx(-DELTA_DEMO, rel=REL)
        assert flussi[1] == pytest.approx(RISPARMIO_DEMO, rel=REL)
        assert flussi[20] == pytest.approx(
            RISPARMIO_DEMO + CX_TANK_DEMO, rel=REL)

    def test_flussi_con_sostituzione_entrambi(self):
        # Semantica tab714: sostituzione alt
        # sottrae, sostituzione base aggiunge.
        flussi = _F["mh715_flussi"](
            DELTA_DEMO, RISPARMIO_DEMO,
            CX_TANK_DEMO, CX_CAV_DEMO, [15], [10, 20], 30)
        assert flussi[10] == pytest.approx(
            RISPARMIO_DEMO - CX_CAV_DEMO, rel=REL)
        assert flussi[15] == pytest.approx(
            RISPARMIO_DEMO + CX_TANK_DEMO, rel=REL)
        assert flussi[20] == pytest.approx(
            RISPARMIO_DEMO - CX_CAV_DEMO, rel=REL)

    def test_tir_none_tutti_flussi_non_negativi(self):
        assert _F["mh715_tir_flussi"](
            [0.0] + [RISPARMIO_DEMO] * 30) is None

    def test_tir_none_demo_tutti_flussi_non_negativi(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 30
        flussi[20] += CX_TANK_DEMO
        assert all(f >= 0.0 for f in flussi)
        assert _F["mh715_tir_flussi"](flussi) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh715_tir_flussi"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo_zero(self):
        flussi = [-DELTA_DEMO] + [RISPARMIO_DEMO] * 30
        flussi[20] += CX_TANK_DEMO
        assert _F["mh715_payback_flussi"](flussi) == PAYBACK_DEMO

    def test_payback_primo_anno_cumulato_non_negativo(self):
        assert _F["mh715_payback_flussi"](
            [-1000.0, 300.0, 300.0, 300.0, 300.0]) == 4
        assert -1000.0 + 300.0 * 3 < 0.0
        assert -1000.0 + 300.0 * 4 >= 0.0

    def test_payback_none_se_mai(self):
        assert _F["mh715_payback_flussi"](
            [-5000000000.0] + [RISPARMIO_DEMO] * 30) is None

    def test_payback_zero_se_cumulato_anno_zero_non_negativo(self):
        assert _F["mh715_payback_flussi"](
            [0.0] + [RISPARMIO_DEMO] * 30) == 0

    def test_verdetto_conviente_demo(self):
        assert _F["mh715_verdetto"](
            VAN_DEMO, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == VERDETTO_DEMO

    def test_verdetto_van_zero_conviente(self):
        assert _F["mh715_verdetto"](
            0.0, DELTA_DEMO, 0.10, RISPARMIO_DEMO) == "CONVIENTE"

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh715_verdetto"](
            -100.0, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh715_verdetto"](
            -805593793.6011547, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_ad_hoc(self):
        assert _F["mh715_verdetto"](
            -900000000.0, DELTA_DEMO, 0.10,
            RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_risparmio_non_positivo(
            self):
        assert _F["mh715_verdetto"](
            1000.0, DELTA_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh715_verdetto"](
            1000.0, DELTA_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_delta_zero_van_positivo_conviente(
            self):
        assert _F["mh715_verdetto"](
            1000.0, 0.0, 0.10, RISPARMIO_DEMO) == "CONVIENTE"

    def test_verdetto_delta_zero_van_negativo_non_conviente(
            self):
        assert _F["mh715_verdetto"](
            -1.0, 0.0, 0.10, RISPARMIO_DEMO) == "NON_CONVIENTE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh715_verdetto"](100.0, DELTA_DEMO, -0.01, RISPARMIO_DEMO)

    def test_verdetto_accetta_tolleranza_sopra_uno(self):
        assert _F["mh715_verdetto"](
            -100.0, DELTA_DEMO, 1.5,
            RISPARMIO_DEMO) == "MARGINALE"


class TestOrchestratore:
    def _bc(self, **kw):
        d = _F["mh715_demo"]()
        d.update(kw)
        return _F["mh715_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["massa_lavoro_kg"] == pytest.approx(
            MASSA_LAV_DEMO, rel=REL)
        assert c["massa_cushion_kg"] == pytest.approx(
            MASSA_CUS_DEMO, rel=REL)
        assert c["costo_cushion_eur"] == pytest.approx(
            COSTO_CUS_DEMO, rel=REL)
        assert c["e_cap_mwh"] == pytest.approx(
            E_CAP_DEMO, rel=REL)
        assert c["n_tanks"] == N_TANKS_DEMO
        assert c["capex_cavern_eur"] == pytest.approx(
            CX_CAV_DEMO, rel=REL)
        assert c["capex_tanks_eur"] == pytest.approx(
            CX_TANK_DEMO, rel=REL)
        assert c["capex_delta_eur"] == pytest.approx(
            DELTA_DEMO, rel=REL)
        assert c["costo_base_eur_a"] == pytest.approx(
            C_BASE_DEMO, rel=REL)
        assert c["costo_alt_eur_a"] == pytest.approx(
            C_ALT_DEMO, rel=REL)
        assert c["risparmio_eur_a"] == pytest.approx(
            RISPARMIO_DEMO, rel=REL)
        assert c["anni_sost_cavern"] == []
        assert c["anni_sost_tanks"] == [20]
        assert c["throughput_mwh_a"] == pytest.approx(
            THR_DEMO, rel=REL)
        assert c["co2_evitata_t_a"] == pytest.approx(
            CO2_EV_DEMO, rel=REL)
        assert abs(c["van"] - VAN_DEMO) <= 1.0
        assert c["tir"] is None
        assert c["payback"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()[
            "van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()[
            "risparmio_eur_a"] == _F["demo_calcoli"]()[
            "risparmio_eur_a"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        d = _F["mh715_demo"]()
        b = _F["mh715_calcola"](**d)
        coppie = [("massa_lavoro_kg", MASSA_LAV_DEMO),
                  ("massa_cushion_kg", MASSA_CUS_DEMO),
                  ("costo_cushion_eur", COSTO_CUS_DEMO),
                  ("e_cap_mwh", E_CAP_DEMO),
                  ("capex_cavern_eur", CX_CAV_DEMO),
                  ("capex_tanks_eur", CX_TANK_DEMO),
                  ("capex_delta_eur", DELTA_DEMO),
                  ("costo_base_eur_a", C_BASE_DEMO),
                  ("costo_alt_eur_a", C_ALT_DEMO),
                  ("risparmio_eur_a", RISPARMIO_DEMO),
                  ("throughput_mwh_a", THR_DEMO),
                  ("co2_evitata_t_a", CO2_EV_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert b["n_tanks"] == N_TANKS_DEMO
        assert abs(b["van"] - VAN_DEMO) <= 1.0
        assert b["tir"] is None
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh715_demo"]()
        assert d["volume_m3"] == 500000.0
        assert d["p_min_bar"] == 60.0
        assert d["p_max_bar"] == 180.0
        assert d["temp_k"] == 300.0
        assert d["c_cavern_eur_m3"] == 30.0
        assert d["fisso_cavern_eur"] == 5000000.0
        assert d["prezzo_cushion_eur_kg"] == 2.5
        assert d["om_cavern_eur_a"] == 800000.0
        assert d["tank_cap_mwh"] == 30.0
        assert d["c_tank_eur"] == 1500000.0
        assert d["om_tank_eur_a"] == 30000.0
        assert d["vita_anni_cavern"] == 30
        assert d["vita_anni_tanks"] == 20
        assert d["vita_progetto_anni"] == 30
        assert d["wacc_frac"] == 0.06
        assert d["tolleranza_frac"] == 0.10
        assert d["cicli_anno"] == 12.0
        assert d["f_rete_t_mwh"] == 0.35

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("massa_lavoro_kg",
                       "massa_cushion_kg",
                       "costo_cushion_eur",
                       "e_cap_mwh",
                       "capex_cavern_eur",
                       "capex_tanks_eur",
                       "capex_delta_eur",
                       "costo_base_eur_a",
                       "costo_alt_eur_a",
                       "risparmio_eur_a",
                       "throughput_mwh_a",
                       "co2_evitata_t_a", "van"):
            assert repr(c[chiave]) in doc, chiave
        assert repr(c["n_tanks"]) in doc
        assert "tir = None" in doc
        assert "payback = 0" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_delta_positivo_conviente(self):
        # Serbatoi da 10000 MWh e O&M 100000:
        # n = 17, CAPEX serbatoi 25500000, delta
        # 562063,99, C_base 1700000, risparmio
        # 900000; VAN 19777304,58, TIR 160,12 %,
        # payback 1.
        n = self._bc(tank_cap_mwh=10000.0, om_tank_eur_a=100000.0)
        assert n["valid"] is True
        assert n["n_tanks"] == 17
        assert n["capex_tanks_eur"] == pytest.approx(
            25500000.0, rel=REL)
        assert n["capex_delta_eur"] == pytest.approx(
            562063.9884532094, rel=REL)
        assert n["costo_base_eur_a"] == pytest.approx(
            1700000.0, rel=REL)
        assert n["risparmio_eur_a"] == pytest.approx(
            900000.0, rel=REL)
        assert abs(n["van"] - 19777304.583482414) <= 1.0
        assert abs(n["tir"] - 160.1241533768596) <= 0.01
        assert n["payback"] == 1
        assert n["verdetto"] == "CONVIENTE"

    def test_costo_fisso_marginale(self):
        # Costo fisso caverna 15000000, serbatoi
        # da 10000 MWh, O&M 55000: delta
        # 10562063,99, risparmio 135000, VAN
        # -752791,25 entro tolleranza 1056206,40
        # -> MARGINALE; payback 20 (sostituzione
        # serbatoi anno 20).
        n = self._bc(fisso_cavern_eur=15000000.0,
                     tank_cap_mwh=10000.0, om_tank_eur_a=55000.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            10562063.98845321, rel=REL)
        assert n["risparmio_eur_a"] == pytest.approx(
            135000.0, rel=REL)
        assert abs(n["van"] - (-752791.2474069891)) <= 1.0
        assert abs(n["tir"] - 5.575052373398247) <= 0.01
        assert n["verdetto"] == "MARGINALE"
        assert n["payback"] == 20

    def test_costo_fisso_non_conviente(self):
        # Costo fisso caverna 50000000, serbatoi
        # da 10000 MWh, O&M 55000: delta
        # 45562063,99, VAN -35752791,25 oltre
        # tolleranza 4556206,40 -> NON_CONVIENTE;
        # payback mai.
        n = self._bc(fisso_cavern_eur=50000000.0,
                     tank_cap_mwh=10000.0, om_tank_eur_a=55000.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            45562063.98845321, rel=REL)
        assert abs(n["van"] - (-35752791.24740699)) <= 1.0
        assert n["verdetto"] == "NON_CONVIENTE"
        assert n["payback"] is None

    def test_om_cavern_alto_non_calcolabile(self):
        # O&M caverna 200000000 > C_base
        # 161640000 -> risparmio negativo ->
        # dict neutro NON_CALCOLABILE.
        n = self._bc(om_cavern_eur_a=200000000.0)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_capex_delta_zero_mai_marginale(self):
        # Tutti i costi CAPEX a zero -> delta 0.
        n = self._bc(c_cavern_eur_m3=0.0, fisso_cavern_eur=0.0,
                     prezzo_cushion_eur_kg=0.0, c_tank_eur=0.0)
        assert n["valid"] is True
        assert n["capex_delta_eur"] == pytest.approx(
            0.0, abs=1e-6)
        assert n["verdetto"] == "CONVIENTE"
        assert n["verdetto"] != "MARGINALE"
        assert n["payback"] == 0
        assert n["tir"] is None

    def test_sostituzioni_entrambi(self):
        # Vita anni caverna 10 e serbatoi 15:
        # sostituzioni caverna 10, 20 e serbatoi
        # 15; flusso anno 10 = 134777936,01,
        # anno 15 = 8242840000, anno 20 =
        # 134777936,01; VAN 13619530404,13.
        n = self._bc(vita_anni_cavern=10, vita_anni_tanks=15)
        assert n["valid"] is True
        assert n["anni_sost_cavern"] == [10, 20]
        assert n["anni_sost_tanks"] == [15]
        assert n["df_flussi"]["Flusso (€/anno)"].iloc[10] == \
            pytest.approx(134777936.0115468, rel=REL)
        assert n["df_flussi"]["Flusso (€/anno)"].iloc[15] == \
            pytest.approx(8242840000.0, rel=REL)
        assert n["df_flussi"]["Flusso (€/anno)"].iloc[20] == \
            pytest.approx(134777936.0115468, rel=REL)
        assert abs(n["van"] - 13619530404.130957) <= 1.0

    def test_p_max_minore_p_min_neutro(self):
        n = self._bc(p_max_bar=50.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_p_min_zero_neutro(self):
        n = self._bc(p_min_bar=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_volume_zero_neutro(self):
        n = self._bc(volume_m3=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_temp_zero_neutro(self):
        n = self._bc(temp_k=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tank_cap_zero_neutro(self):
        n = self._bc(tank_cap_mwh=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_progetto_zero_neutro(self):
        n = self._bc(vita_progetto_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_anni_zero_neutro(self):
        n = self._bc(vita_anni_cavern=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_negativo_neutro(self):
        n = self._bc(wacc_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_negativa_neutro(self):
        n = self._bc(tolleranza_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(p_max_bar=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["risparmio_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(volume_m3=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(volume_m3=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_zero_calcolabile_conviente(self):
        # WACC 0: VAN = somma flussi = -delta +
        # risparmio x 30 + CAPEX serbatoi anno 20
        # = 20963137936,01.
        n = self._bc(wacc_frac=0.0)
        assert n["van"] == pytest.approx(
            20963137936.011547, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh715_neutro"]()
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
        n = _F["_mh715_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "volume_m3", "p_min_bar",
                       "p_max_bar",
                       "massa_lavoro_kg",
                       "massa_cushion_kg",
                       "e_cap_mwh", "n_tanks",
                       "capex_cavern_eur",
                       "capex_tanks_eur",
                       "capex_delta_eur",
                       "costo_base_eur_a",
                       "costo_alt_eur_a",
                       "risparmio_eur_a",
                       "anni_sost_cavern",
                       "anni_sost_tanks",
                       "throughput_mwh_a",
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
        assert "Capacita' utile (MWh)" in voci
        assert "Massa cushion (kg)" in voci
        assert "Costo cushion (EUR)" in voci
        assert "Numero serbatoi" in voci
        assert "CAPEX caverna (EUR)" in voci
        assert "CAPEX serbatoi (EUR)" in voci
        assert "CAPEX delta (EUR)" in voci
        assert "Costo annuo baseline (EUR/anno)" in voci
        assert "Costo annuo alternativa (EUR/anno)" in voci
        assert "Risparmio annuo (EUR/anno)" in voci
        assert "Throughput annua (MWh/anno)" in voci
        assert "CO2 evitata vs rete (t/anno)" in voci
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
            pytest.approx(RISPARMIO_DEMO + CX_TANK_DEMO, rel=REL)


class TestSensitivitaCsv:
    def _ing(self):
        return _F["mh715_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh715_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.9", "x1.0", "x1.1"]
        assert list(s.index) == ["x0.9", "x1.0", "x1.1"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh715_sensitivita"](self._ing())
        assert abs(s.loc["x1.0", "x1.0"] - VAN_DEMO) <= 1.0

    def test_sensitivita_decrescente_con_costo_caverna(self):
        s = _F["mh715_sensitivita"](self._ing())
        for colonna in ("x0.9", "x1.0", "x1.1"):
            assert s.loc["x0.9", colonna] > \
                s.loc["x1.0", colonna] > \
                s.loc["x1.1", colonna]

    def test_sensitivita_crescente_con_costo_serbatoio(self):
        s = _F["mh715_sensitivita"](self._ing())
        for riga in ("x0.9", "x1.0", "x1.1"):
            assert s.loc[riga, "x0.9"] < \
                s.loc[riga, "x1.0"] < \
                s.loc[riga, "x1.1"]

    def test_sensitivita_nessuna_colonna_degenere(self):
        s = _F["mh715_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_nessuna_colonna_costante(self):
        s = _F["mh715_sensitivita"](self._ing())
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3

    def test_sensitivita_angoli(self):
        s = _F["mh715_sensitivita"](self._ing())
        assert abs(s.loc["x0.9", "x0.9"] - 11731178600.841105) <= 1.0
        assert abs(s.loc["x0.9", "x1.1"] - 13851579761.379774) <= 1.0
        assert abs(s.loc["x1.1", "x0.9"] - 11728178600.841105) <= 1.0
        assert abs(s.loc["x1.1", "x1.1"] - 13848579761.379774) <= 1.0

    def test_sensitivita_con_sostituzioni_ricalcolate(self):
        # Con vita anni caverna 10 e serbatoi 15
        # la griglia deve includere le
        # sostituzioni: il centro deve coincidere
        # col VAN del caso con sostituzioni.
        ing = self._ing()
        ing["vita_anni_cavern"] = 10
        ing["vita_anni_tanks"] = 15
        s = _F["mh715_sensitivita"](ing)
        assert abs(s.loc["x1.0", "x1.0"] - 13619530404.130957) <= 1.0

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh715_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") >= 35

    def test_csv_contiene_verdetto_e_risparmio(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh715_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "risparmio_eur_a" in txt
        assert "costo_base_eur_a" in txt
        assert "costo_alt_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "volume_m3" in txt
        assert "e_cap_mwh" in txt
        assert "co2_evitata_t_a" in txt
        assert "p_min_bar" in txt
        assert "capex_cavern_eur" in txt
        assert "capex_delta_eur" in txt
        assert "n_tanks" in txt
        assert "throughput_mwh_a" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh715_csv"](bc, self._ing())
        assert f"risparmio_eur_a;{bc['risparmio_eur_a']}" in txt
        assert f"costo_base_eur_a;{bc['costo_base_eur_a']}" in txt
        assert "volume_m3;500000.0" in txt
        assert "om_cavern_eur_a;800000.0" in txt
        assert f"capex_delta_eur;{bc['capex_delta_eur']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def715["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def715\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 18, ui_keys
        demo_keys = set(_F["mh715_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh715_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh715_demo():")
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
        ui_keys = set(re.findall(r'_def715\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W716 (25/10/2026) - tab715' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh715_num", "mh715_nneg", "mh715_pos",
                     "mh715_int_pos", "mh715_int_nneg",
                     "mh715_massa_gas", "mh715_capacita_utile",
                     "mh715_capex_cavern", "mh715_n_serbatoi",
                     "mh715_capex_serbatoi",
                     "mh715_costo_annuo_serbatoi",
                     "mh715_risparmio", "mh715_anni_sostituzione",
                     "mh715_flussi",
                     "mh715_van_flussi", "mh715_tir_flussi",
                     "mh715_payback_flussi", "mh715_verdetto",
                     "mh715_throughput", "mh715_co2_evitata",
                     "mh715_valida",
                     "_mh715_neutro", "mh715_calcola",
                     "mh715_sensitivita", "mh715_csv",
                     "mh715_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_helpers_nessun_residuo_tab_precedente(self):
        # La tab precedente e' la tab714
        # (eolico offshore galleggiante): i
        # frammenti nuovi non devono contenere
        # i suoi identificatori di funzione.
        # (Il riferimento testuale "tab714" per
        # la semantica delle sostituzioni e'
        # voluto e documentato nell'header.)
        assert "mh714" not in _helpers_src()
        assert "mh714" not in _ui_src()
        assert "tab714" not in _ui_src()

    def test_chain_riferimento_tab_precedente(self):
        # Catena: questo file test fa riferimento
        # alla tab precedente tab714 come punto di
        # confronto (test residuo sopra) e la
        # nuova tab e' tab715.
        src = Path(__file__).read_text(encoding="utf-8")
        assert "tab714" in src
        assert "tab715" in src
        assert _ui_src().startswith("    with tab715:")

    def test_helpers_parse_ast(self):
        import textwrap
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w716_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE715) == 1

    def test_blocco_with_tab715(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab715:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE715

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st715_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 23, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st715_") for k in keys)

    def test_chiavi_st_input_sono_19(self):
        """Le 19 chiavi di input/bottone (18 input +
        bottone calcola) sono tutte presenti; le
        altre 4 sono solo chiavi di
        visualizzazione (fig, heatmap, flussi, CSV)."""
        keys = re.findall(r'key="(st715_[a-z0-9_]+)"', _ui_src())
        attese = ["st715_volume", "st715_p_min",
                  "st715_p_max", "st715_temp",
                  "st715_c_cavern", "st715_fisso_cavern",
                  "st715_prezzo_cushion", "st715_om_cavern",
                  "st715_tank_cap", "st715_c_tank",
                  "st715_om_tank", "st715_vita_cavern",
                  "st715_vita_tanks", "st715_vita_progetto",
                  "st715_wacc", "st715_tolleranza",
                  "st715_cicli", "st715_f_rete",
                  "st715_calcola"]
        assert len(attese) == 19
        for k in attese:
            assert k in keys, k

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg715" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg715") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg715")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Capacità utile (MWh)" in src
        assert "Risparmio annuo (€/anno)" in src
        assert "VAN (€)" in src
        assert "CO2 evitata vs rete (t/anno)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        assert "_ver715" in src
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_presente(self):
        src = _ui_src().lower()
        assert "cushion" in src
        assert "scala" in src
        assert "informative" in src
        assert "throughput" in src
        assert "costo affondato" in src

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert "Costo annuo baseline" in src
        assert "Costo annuo alternativa" in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh715_csv" in src
        assert "idrogeno_caverna_salina_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh715_sensitivita" in src
        assert "Heatmap" in src
        assert "Costo caverna" in src
        assert "Costo serbatoio" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st715_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W716 (25/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab715:")
