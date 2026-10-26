"""Test tab723 "🔋♻️ Riciclo batterie al litio: il metallo recuperato paga lo smaltimento?"

Nuova tab tab723 (riciclo batterie, w724).
La tab723 replica la semantica economica
delle tab precedenti: flussi [-CAPEX,
margine annuo] piatti senza sostituzioni
(vita impianto = vita di progetto),
VAN/TIR (bisezione [-99 %, +500 %], None se
margine <= 0 o nessun cambio di segno incl.
tutti flussi >= 0)/payback (0 se cumulato
anno 0 >= 0), verdetto CONVIENTE (VAN >= 0)/
MARGINALE (VAN < 0 entro toll % del CAPEX;
CAPEX == 0 mai MARGINALE)/NON_CONVIENTE/
NON_CALCOLABILE (validazione fallita o
margine <= 0).

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
feedstock 10000 t/a; costo di trattamento
2500 EUR/t; opex fisso 5000000 EUR/anno;
CAPEX 80000000 EUR; vita di progetto 20
anni; WACC 0,06 (6 %); tolleranza 0,10 (10 %
del CAPEX); fattore CO2 3,5 t per t di
feedstock; litio contenuto 30 kg/t, recupero
0,85, prezzo 20 EUR/kg; cobalto 60 kg/t,
0,90, 30 EUR/kg; nichel 120 kg/t, 0,90, 18
EUR/kg; rame 100 kg/t, 0,95, 8 EUR/kg;
alluminio 150 kg/t, 0,90, 2 EUR/kg.

- ricavo_litio_eur_t = 510.0
- ricavo_cobalto_eur_t = 1620.0
- ricavo_nichel_eur_t = 1944.0
- ricavo_rame_eur_t = 760.0
- ricavo_alluminio_eur_t = 270.0
- ricavo_totale_eur_t = 5104.0
- ricavi_annui_eur_a = 51040000.0
- costo_annuo_eur_a = 30000000.0
- margine_annuo_eur_a = 21040000.0
- co2_evitata_t_a = 35000.0
- van = 161327142.43861294
- tir = 26.043217063298307
- payback = 4
- verdetto = 'CONVIENTE'

Scomposizione: litio 30 x 0,85 x 20 = 510,0
EUR/t; cobalto 60 x 0,90 x 30 = 1620,0 EUR/t;
nichel 120 x 0,90 x 18 = 1944,0 EUR/t; rame
100 x 0,95 x 8 = 760,0 EUR/t; alluminio
150 x 0,90 x 2 = 270,0 EUR/t; totale
510 + 1620 + 1944 + 760 + 270 = 5104,0
EUR/t; ricavi annui 10000 x 5104 = 51040000,0
EUR/anno; costo annuo 10000 x 2500 +
5000000 = 30000000,0 EUR/anno; margine
51040000,0 - 30000000,0 = 21040000,0
EUR/anno; flussi: anno 0 -80000000,0, anni
1-20 margine 21040000,0 (piatti, nessuna
sostituzione: vita impianto = vita
progetto); VAN 161327142.43861294 a WACC 6 %
su 20 anni; TIR 26.043217063298307 % (il tasso
che azzera il VAN dei flussi sopra); payback
4 (il cumulato diventa positivo all'anno 4:
-80000000,0 + 3 x 21040000,0 = -16880000,0
all'anno 3, poi + 21040000,0 = 4160000,0
all'anno 4); CO2 10000 x 3,5 = 35000,0 t/anno
(INFORMATIVA: non entra nel conto
economico); VAN >= 0 -> CONVIENTE.
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
    if (p / "w724_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w724_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w724_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w724_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w724_helpers.py: {missing}")
    return out


_F = _load("mh723_num", "mh723_nneg", "mh723_pos",
           "mh723_int_pos", "mh723_recupero_valida",
           "mh723_ricavo_per_t", "mh723_ricavi_annui",
           "mh723_costo_annuo", "mh723_margine",
           "mh723_flussi", "mh723_van_flussi",
           "mh723_tir_flussi", "mh723_payback_flussi",
           "mh723_verdetto", "mh723_co2_evitata",
           "mh723_tabella_metalli", "mh723_valida",
           "_mh723_neutro", "mh723_calcola",
           "mh723_sensitivita", "mh723_csv",
           "mh723_demo", "demo_calcoli")

TITLE723 = ("🔋♻️ Riciclo batterie al litio: il metallo "
            "recuperato paga lo smaltimento?")

RIC_LI_DEMO = 510.0
RIC_CO_DEMO = 1620.0
RIC_NI_DEMO = 1944.0
RIC_CU_DEMO = 760.0
RIC_AL_DEMO = 270.0
RIC_TOT_DEMO = 5104.0
RIC_ANN_DEMO = 51040000.0
COSTO_DEMO = 30000000.0
MARGINE_DEMO = 21040000.0
CO2_DEMO = 35000.0
VAN_DEMO = 161327142.43861294
TIR_DEMO = 26.043217063298307
PAYBACK_DEMO = 4
CAPEX_DEMO = 80000000.0
VITA_DEMO = 20
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w724_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w724_ui.py").read_text(encoding="utf-8")


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh723_demo"]()
        d.update(kw)
        return _F["mh723_valida"](**d)

    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh723_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh723_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh723_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh723_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh723_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh723_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh723_pos"](0.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh723_int_pos"](2.5, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh723_int_pos"](20.0, "x") == 20

    def test_recupero_rifiuta_sopra_uno(self):
        with pytest.raises(ValueError):
            _F["mh723_recupero_valida"](1.01, "x")

    def test_recupero_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh723_recupero_valida"](-0.01, "x")

    def test_recupero_accetta_estremi(self):
        assert _F["mh723_recupero_valida"](0.0, "x") == 0.0
        assert _F["mh723_recupero_valida"](1.0, "x") == 1.0

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_feedstock_zero_non_valido(self):
        assert self._val(feedstock_t_a=0.0)["valido"] is False

    def test_recuperi_fuori_intervallo_non_validi(self):
        for k in ("recupero_litio", "recupero_cobalto",
                  "recupero_nichel", "recupero_rame",
                  "recupero_alluminio"):
            assert self._val(**{k: 1.5})["valido"] is False, k
            assert self._val(**{k: -0.1})["valido"] is False, k

    def test_negativi_non_validi(self):
        for k in ("costo_trattamento_eur_t", "opex_fisso_eur_a",
                  "capex_eur", "wacc_frac", "tolleranza_frac",
                  "fattore_co2_t_t",
                  "contenuto_litio_kg_t", "prezzo_litio_eur_kg",
                  "contenuto_cobalto_kg_t",
                  "prezzo_cobalto_eur_kg",
                  "contenuto_nichel_kg_t", "prezzo_nichel_eur_kg",
                  "contenuto_rame_kg_t", "prezzo_rame_eur_kg",
                  "contenuto_alluminio_kg_t",
                  "prezzo_alluminio_eur_kg"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_vita_progetto_zero_non_valida(self):
        assert self._val(vita_progetto_anni=0)["valido"] is False

    def test_vita_progetto_non_intera_non_valida(self):
        assert self._val(vita_progetto_anni=20.5)["valido"] is False

    def test_tolleranza_sopra_uno_valida_brief(self):
        assert self._val(tolleranza_frac=1.5)["valido"] is True

    def test_wacc_senza_tetto_superiore(self):
        assert self._val(wacc_frac=1.5)["valido"] is True

    def test_nan_non_valido(self):
        assert self._val(recupero_litio=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(feedstock_t_a=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(vita_progetto_anni=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(recupero_litio="0.85")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(costo_trattamento_eur_t=0.0)["valido"] is True
        assert self._val(opex_fisso_eur_a=0.0)["valido"] is True
        assert self._val(capex_eur=0.0)["valido"] is True
        assert self._val(wacc_frac=0.0)["valido"] is True
        assert self._val(tolleranza_frac=0.0)["valido"] is True
        assert self._val(fattore_co2_t_t=0.0)["valido"] is True
        assert self._val(contenuto_litio_kg_t=0.0)["valido"] is True
        assert self._val(prezzo_litio_eur_kg=0.0)["valido"] is True


class TestFunzioni:
    def test_ricavo_per_t_demo(self):
        assert _F["mh723_ricavo_per_t"](
            30.0, 0.85, 20.0) == pytest.approx(RIC_LI_DEMO, rel=REL)
        assert _F["mh723_ricavo_per_t"](
            60.0, 0.90, 30.0) == pytest.approx(RIC_CO_DEMO, rel=REL)
        assert _F["mh723_ricavo_per_t"](
            120.0, 0.90, 18.0) == pytest.approx(RIC_NI_DEMO, rel=REL)
        assert _F["mh723_ricavo_per_t"](
            100.0, 0.95, 8.0) == pytest.approx(RIC_CU_DEMO, rel=REL)
        assert _F["mh723_ricavo_per_t"](
            150.0, 0.90, 2.0) == pytest.approx(RIC_AL_DEMO, rel=REL)

    def test_ricavo_per_t_recupero_zero(self):
        assert _F["mh723_ricavo_per_t"](
            30.0, 0.0, 20.0) == pytest.approx(0.0, abs=1e-9)

    def test_ricavo_per_t_recupero_uno(self):
        assert _F["mh723_ricavo_per_t"](
            30.0, 1.0, 20.0) == pytest.approx(600.0, rel=REL)

    def test_ricavo_per_t_recupero_fuori_intervallo_rifiutato(self):
        with pytest.raises(ValueError):
            _F["mh723_ricavo_per_t"](30.0, 1.2, 20.0)

    def test_ricavi_annui_demo(self):
        assert _F["mh723_ricavi_annui"](
            10000.0, RIC_TOT_DEMO) == pytest.approx(
            RIC_ANN_DEMO, rel=REL)

    def test_costo_annuo_demo(self):
        assert _F["mh723_costo_annuo"](
            10000.0, 2500.0, 5000000.0) == pytest.approx(
            COSTO_DEMO, rel=REL)

    def test_margine_demo(self):
        assert _F["mh723_margine"](
            RIC_ANN_DEMO, COSTO_DEMO) == pytest.approx(
            MARGINE_DEMO, rel=REL)

    def test_margine_puo_essere_negativo(self):
        assert _F["mh723_margine"](
            1000000.0, 2000000.0) == pytest.approx(
            -1000000.0, rel=REL)

    def test_flussi_demo_piatti_senza_sostituzioni(self):
        flussi = _F["mh723_flussi"](CAPEX_DEMO, MARGINE_DEMO,
                                     VITA_DEMO)
        assert len(flussi) == VITA_DEMO + 1
        assert flussi[0] == pytest.approx(-CAPEX_DEMO, rel=REL)
        assert all(f == pytest.approx(MARGINE_DEMO, rel=REL)
                   for f in flussi[1:])

    def test_van_flussi_demo(self):
        flussi = _F["mh723_flussi"](CAPEX_DEMO, MARGINE_DEMO,
                                     VITA_DEMO)
        assert abs(_F["mh723_van_flussi"](
            flussi, 0.06) - VAN_DEMO) <= 1.0

    def test_van_flussi_tasso_zero(self):
        flussi = _F["mh723_flussi"](CAPEX_DEMO, MARGINE_DEMO,
                                     VITA_DEMO)
        atteso = -CAPEX_DEMO + MARGINE_DEMO * VITA_DEMO
        assert _F["mh723_van_flussi"](
            flussi, 0.0) == pytest.approx(atteso, rel=1e-12)

    def test_van_flussi_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh723_van_flussi"]([100.0, 100.0], -0.01)

    def test_tir_demo(self):
        flussi = _F["mh723_flussi"](CAPEX_DEMO, MARGINE_DEMO,
                                     VITA_DEMO)
        tir = _F["mh723_tir_flussi"](flussi)
        assert tir is not None
        assert tir * 100.0 == pytest.approx(TIR_DEMO, rel=1e-9)

    def test_tir_none_tutti_flussi_non_negativi(self):
        assert _F["mh723_tir_flussi"](
            [1000.0] + [100.0] * 10) is None

    def test_tir_none_nessun_cambio_segno_negativo(self):
        assert _F["mh723_tir_flussi"](
            [-1000.0] + [-100.0] * 10) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh723_tir_flussi"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo_quattro(self):
        flussi = _F["mh723_flussi"](CAPEX_DEMO, MARGINE_DEMO,
                                     VITA_DEMO)
        assert _F["mh723_payback_flussi"](flussi) == PAYBACK_DEMO

    def test_payback_none_se_mai(self):
        assert _F["mh723_payback_flussi"](
            [-500000000.0] + [MARGINE_DEMO] * 20) is None

    def test_payback_zero_se_cumulato_anno_zero_non_negativo(self):
        assert _F["mh723_payback_flussi"](
            [0.0] + [MARGINE_DEMO] * 20) == 0

    def test_verdetto_conviente_demo(self):
        assert _F["mh723_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10,
            MARGINE_DEMO) == VERDETTO_DEMO

    def test_verdetto_van_zero_conviente(self):
        assert _F["mh723_verdetto"](
            0.0, CAPEX_DEMO, 0.10, MARGINE_DEMO) == "CONVIENTE"

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh723_verdetto"](
            -100.0, CAPEX_DEMO, 0.10,
            MARGINE_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh723_verdetto"](
            -0.10 * CAPEX_DEMO, CAPEX_DEMO, 0.10,
            MARGINE_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_oltre_limite(self):
        assert _F["mh723_verdetto"](
            -0.10 * CAPEX_DEMO - 1.0, CAPEX_DEMO, 0.10,
            MARGINE_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_margine_non_positivo(self):
        assert _F["mh723_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh723_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_positivo_conviente(self):
        assert _F["mh723_verdetto"](
            1000.0, 0.0, 0.10, MARGINE_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(self):
        assert _F["mh723_verdetto"](
            -1.0, 0.0, 0.10, MARGINE_DEMO) == "NON_CONVIENTE"

    def test_verdetto_capex_zero_mai_marginale(self):
        # Con CAPEX == 0 la tolleranza vale zero:
        # nessun VAN < 0 puo' essere MARGINALE.
        for van in (-1.0, -100.0, -1000000.0):
            assert _F["mh723_verdetto"](
                van, 0.0, 0.10, MARGINE_DEMO) == "NON_CONVIENTE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh723_verdetto"](100.0, CAPEX_DEMO, -0.01, MARGINE_DEMO)

    def test_co2_evitata_demo(self):
        assert _F["mh723_co2_evitata"](
            10000.0, 3.5) == pytest.approx(CO2_DEMO, rel=REL)

    def test_co2_evitata_zero_se_fattore_zero(self):
        assert _F["mh723_co2_evitata"](
            10000.0, 0.0) == pytest.approx(0.0, abs=1e-9)

    def test_tabella_metalli_demo(self):
        df = _F["mh723_tabella_metalli"]([
            ("Litio", 30.0, 0.85, 20.0),
            ("Cobalto", 60.0, 0.90, 30.0),
            ("Nichel", 120.0, 0.90, 18.0),
            ("Rame", 100.0, 0.95, 8.0),
            ("Alluminio", 150.0, 0.90, 2.0)])
        assert list(df.columns) == ["Metallo", "Contenuto (kg/t)",
                                    "Recupero", "Prezzo (€/kg)",
                                    "Ricavo (€/t)"]
        assert len(df) == 5
        assert df["Ricavo (€/t)"].tolist() == pytest.approx(
            [RIC_LI_DEMO, RIC_CO_DEMO, RIC_NI_DEMO, RIC_CU_DEMO,
             RIC_AL_DEMO], rel=REL)
        assert df["Ricavo (€/t)"].sum() == pytest.approx(
            RIC_TOT_DEMO, rel=REL)


class TestDemo:
    def _bc(self, **kw):
        d = _F["mh723_demo"]()
        d.update(kw)
        return _F["mh723_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["ricavo_litio_eur_t"] == pytest.approx(
            RIC_LI_DEMO, rel=REL)
        assert c["ricavo_cobalto_eur_t"] == pytest.approx(
            RIC_CO_DEMO, rel=REL)
        assert c["ricavo_nichel_eur_t"] == pytest.approx(
            RIC_NI_DEMO, rel=REL)
        assert c["ricavo_rame_eur_t"] == pytest.approx(
            RIC_CU_DEMO, rel=REL)
        assert c["ricavo_alluminio_eur_t"] == pytest.approx(
            RIC_AL_DEMO, rel=REL)
        assert c["ricavo_totale_eur_t"] == pytest.approx(
            RIC_TOT_DEMO, rel=REL)
        assert c["ricavi_annui_eur_a"] == pytest.approx(
            RIC_ANN_DEMO, rel=REL)
        assert c["costo_annuo_eur_a"] == pytest.approx(
            COSTO_DEMO, rel=REL)
        assert c["margine_annuo_eur_a"] == pytest.approx(
            MARGINE_DEMO, rel=REL)
        assert c["co2_evitata_t_a"] == pytest.approx(
            CO2_DEMO, rel=REL)
        assert abs(c["van"] - VAN_DEMO) <= 1.0
        assert abs(c["tir"] - TIR_DEMO) <= 0.01
        assert c["payback"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO
        assert c["flussi"][0] == pytest.approx(-CAPEX_DEMO, rel=REL)
        assert all(f == pytest.approx(MARGINE_DEMO, rel=REL)
                   for f in c["flussi"][1:])
        assert len(c["flussi"]) == VITA_DEMO + 1

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()[
            "van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()[
            "margine_annuo_eur_a"] == _F["demo_calcoli"]()[
            "margine_annuo_eur_a"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        d = _F["mh723_demo"]()
        b = _F["mh723_calcola"](**d)
        coppie = [("ricavo_litio_eur_t", RIC_LI_DEMO),
                  ("ricavo_cobalto_eur_t", RIC_CO_DEMO),
                  ("ricavo_nichel_eur_t", RIC_NI_DEMO),
                  ("ricavo_rame_eur_t", RIC_CU_DEMO),
                  ("ricavo_alluminio_eur_t", RIC_AL_DEMO),
                  ("ricavo_totale_eur_t", RIC_TOT_DEMO),
                  ("ricavi_annui_eur_a", RIC_ANN_DEMO),
                  ("costo_annuo_eur_a", COSTO_DEMO),
                  ("margine_annuo_eur_a", MARGINE_DEMO),
                  ("co2_evitata_t_a", CO2_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert abs(b["van"] - VAN_DEMO) <= 1.0
        assert abs(b["tir"] - TIR_DEMO) <= 0.01
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh723_demo"]()
        assert d["feedstock_t_a"] == 10000.0
        assert d["costo_trattamento_eur_t"] == 2500.0
        assert d["opex_fisso_eur_a"] == 5000000.0
        assert d["capex_eur"] == 80000000.0
        assert d["vita_progetto_anni"] == 20
        assert d["wacc_frac"] == 0.06
        assert d["tolleranza_frac"] == 0.10
        assert d["fattore_co2_t_t"] == 3.5
        assert d["contenuto_litio_kg_t"] == 30.0
        assert d["recupero_litio"] == 0.85
        assert d["prezzo_litio_eur_kg"] == 20.0
        assert d["contenuto_cobalto_kg_t"] == 60.0
        assert d["recupero_cobalto"] == 0.90
        assert d["prezzo_cobalto_eur_kg"] == 30.0
        assert d["contenuto_nichel_kg_t"] == 120.0
        assert d["recupero_nichel"] == 0.90
        assert d["prezzo_nichel_eur_kg"] == 18.0
        assert d["contenuto_rame_kg_t"] == 100.0
        assert d["recupero_rame"] == 0.95
        assert d["prezzo_rame_eur_kg"] == 8.0
        assert d["contenuto_alluminio_kg_t"] == 150.0
        assert d["recupero_alluminio"] == 0.90
        assert d["prezzo_alluminio_eur_kg"] == 2.0
        assert len(d) == 23

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("ricavo_litio_eur_t",
                       "ricavo_cobalto_eur_t",
                       "ricavo_nichel_eur_t",
                       "ricavo_rame_eur_t",
                       "ricavo_alluminio_eur_t",
                       "ricavo_totale_eur_t",
                       "ricavi_annui_eur_a",
                       "costo_annuo_eur_a",
                       "margine_annuo_eur_a",
                       "co2_evitata_t_a", "van"):
            assert repr(c[chiave]) in doc, chiave
        assert f"tir = {repr(c['tir'])}" in doc
        assert "payback = 4" in doc
        assert "verdetto = 'CONVIENTE'" in doc

    def test_prezzo_litio_dimezzato_conviente(self):
        # Prezzo litio 10 EUR/kg: ricavo litio 255,
        # totale 4849 EUR/t, margine 18490000,
        # VAN 132078843,33, TIR 22,73 %, payback 5
        # -> CONVIENTE (il caso non dipende dal
        # litio: cobalto e nichel dominano).
        n = self._bc(prezzo_litio_eur_kg=10.0)
        assert n["valid"] is True
        assert n["ricavo_litio_eur_t"] == pytest.approx(
            255.0, rel=REL)
        assert n["margine_annuo_eur_a"] == pytest.approx(
            18490000.0, rel=REL)
        assert abs(n["van"] - 132078843.33127153) <= 1.0
        assert abs(n["tir"] - 22.727926847002262) <= 0.01
        assert n["payback"] == 5
        assert n["verdetto"] == "CONVIENTE"

    def test_costo_trattamento_alto_non_conviente(self):
        # Costo trattamento 4000 EUR/t: costo
        # 45000000, margine 6040000, VAN
        # -10721675,84, TIR 4,29 %, payback 14
        # -> NON_CONVIENTE (fuori tolleranza).
        n = self._bc(costo_trattamento_eur_t=4000.0)
        assert n["valid"] is True
        assert n["margine_annuo_eur_a"] == pytest.approx(
            6040000.0, rel=REL)
        assert abs(n["van"] - (-10721675.839865873)) <= 1.0
        assert abs(n["tir"] - 4.292480699158712) <= 0.01
        assert n["payback"] == 14
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_costo_trattamento_marginale(self):
        # Costo trattamento 3970 EUR/t: margine
        # 6340000, VAN -7280699,47, TIR 4,85 %,
        # payback 13 -> MARGINALE (|VAN| <= 10 %
        # di CAPEX = 8000000).
        n = self._bc(costo_trattamento_eur_t=3970.0)
        assert n["valid"] is True
        assert n["margine_annuo_eur_a"] == pytest.approx(
            6340000.0, rel=REL)
        assert abs(n["van"] - (-7280699.474296295)) <= 1.0
        assert abs(n["tir"] - 4.853668779473817) <= 0.01
        assert n["payback"] == 13
        assert n["verdetto"] == "MARGINALE"

    def test_costo_trattamento_altissimo_neutro(self):
        # Costo trattamento 5000 EUR/t: costo
        # 55000000 > ricavi 51040000 -> margine
        # negativo -> dict neutro NON_CALCOLABILE.
        n = self._bc(costo_trattamento_eur_t=5000.0)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["margine_annuo_eur_a"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_capex_zero_tir_none_payback_zero(self):
        # CAPEX 0: tutti i flussi >= 0 -> TIR None,
        # payback 0, VAN 241327142,44 -> CONVIENTE.
        n = self._bc(capex_eur=0.0)
        assert n["valid"] is True
        assert n["tir"] is None
        assert n["payback"] == 0
        assert abs(n["van"] - 241327142.43861297) <= 1.0
        assert n["verdetto"] == "CONVIENTE"

    def test_capex_enorme_payback_none(self):
        # CAPEX 500000000: margine x 20 anni =
        # 420800000 < CAPEX -> payback None, VAN
        # -258672857,56, TIR -1,59 % ->
        # NON_CONVIENTE.
        n = self._bc(capex_eur=500000000.0)
        assert n["valid"] is True
        assert n["payback"] is None
        assert abs(n["van"] - (-258672857.5613871)) <= 1.0
        assert abs(n["tir"] - (-1.5890350093018841)) <= 0.01
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_feedstock_zero_neutro(self):
        n = self._bc(feedstock_t_a=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_recupero_sopra_uno_neutro(self):
        n = self._bc(recupero_cobalto=1.5)
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
        n = self._bc(recupero_litio=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["margine_annuo_eur_a"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(feedstock_t_a=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(vita_progetto_anni=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_zero_calcolabile(self):
        # WACC 0: VAN = somma flussi =
        # -80000000 + 21040000 x 20 = 340800000.
        n = self._bc(wacc_frac=0.0)
        assert n["van"] == pytest.approx(
            340800000.0, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh723_neutro"]()
        assert n["valid"] is False
        assert n["errore"] == ""
        assert list(n["df_metalli"].columns) == ["Metallo",
                                                 "Contenuto (kg/t)",
                                                 "Recupero",
                                                 "Prezzo (€/kg)",
                                                 "Ricavo (€/t)"]
        assert len(n["df_metalli"]) == 0
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
        n = _F["_mh723_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "feedstock_t_a",
                       "costo_trattamento_eur_t",
                       "opex_fisso_eur_a", "capex_eur",
                       "vita_progetto_anni", "wacc_frac",
                       "tolleranza_frac", "fattore_co2_t_t",
                       "ricavo_litio_eur_t",
                       "ricavo_cobalto_eur_t",
                       "ricavo_nichel_eur_t",
                       "ricavo_rame_eur_t",
                       "ricavo_alluminio_eur_t",
                       "ricavo_totale_eur_t",
                       "ricavi_annui_eur_a",
                       "costo_annuo_eur_a",
                       "margine_annuo_eur_a",
                       "co2_evitata_t_a", "flussi",
                       "van", "tir", "payback",
                       "verdetto", "df_metalli",
                       "df_flussi", "df_tabella"):
            assert chiave in n, chiave
        assert n["errore"] == "errore di prova"
        assert n["tir"] is None

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert b["valid"] is True
        assert list(b["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(b["df_tabella"]) == 19
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Feedstock (t/anno)" in voci
        assert "Ricavo totale (EUR/t)" in voci
        assert "Ricavi annui (EUR/anno)" in voci
        assert "Costo annuo (EUR/anno)" in voci
        assert "Margine annuo (EUR/anno)" in voci
        assert "CO2 evitata (t/anno)" in voci
        assert "VAN (EUR)" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(b["df_flussi"]) == VITA_DEMO + 1
        assert b["df_flussi"]["Flusso (€/anno)"].iloc[0] == \
            pytest.approx(-CAPEX_DEMO, rel=REL)
        assert b["df_flussi"]["Flusso (€/anno)"].iloc[1] == \
            pytest.approx(MARGINE_DEMO, rel=REL)
        assert b["df_flussi"]["Flusso (€/anno)"].iloc[20] == \
            pytest.approx(MARGINE_DEMO, rel=REL)
        assert list(b["df_metalli"].columns) == ["Metallo",
                                                 "Contenuto (kg/t)",
                                                 "Recupero",
                                                 "Prezzo (€/kg)",
                                                 "Ricavo (€/t)"]
        assert len(b["df_metalli"]) == 5


class TestSensitivita:
    def _ing(self):
        return _F["mh723_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh723_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.9", "x1.0", "x1.1"]
        assert list(s.index) == ["x0.9", "x1.0", "x1.1"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh723_sensitivita"](self._ing())
        assert abs(s.loc["x1.0", "x1.0"] - VAN_DEMO) <= 1.0

    def test_sensitivita_crescente_con_prezzo_litio(self):
        s = _F["mh723_sensitivita"](self._ing())
        for colonna in ("x0.9", "x1.0", "x1.1"):
            assert s.loc["x0.9", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.1", colonna]

    def test_sensitivita_decrescente_con_costo_trattamento(self):
        s = _F["mh723_sensitivita"](self._ing())
        for riga in ("x0.9", "x1.0", "x1.1"):
            assert s.loc[riga, "x0.9"] > \
                s.loc[riga, "x1.0"] > \
                s.loc[riga, "x1.1"]

    def test_sensitivita_nessuna_colonna_degenere(self):
        s = _F["mh723_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_nessuna_colonna_costante(self):
        s = _F["mh723_sensitivita"](self._ing())
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3

    def test_sensitivita_angoli(self):
        s = _F["mh723_sensitivita"](self._ing())
        assert abs(s.loc["x0.9", "x0.9"] - 184152285.66355774) <= 1.0
        assert abs(s.loc["x0.9", "x1.1"] - 126802679.57073148) <= 1.0
        assert abs(s.loc["x1.1", "x0.9"] - 195851605.30649433) <= 1.0
        assert abs(s.loc["x1.1", "x1.1"] - 138501999.21366808) <= 1.0

    def test_sensitivita_centro_con_vita_corta(self):
        # Con vita 10 anni il centro deve
        # coincidere col VAN del caso con vita
        # 10 anni (flussi piatti, nessun altro
        # effetto).
        ing = self._ing()
        ing["vita_progetto_anni"] = 10
        s = _F["mh723_sensitivita"](ing)
        b = _F["mh723_calcola"](**ing)
        assert abs(s.loc["x1.0", "x1.0"] - b["van"]) <= 1.0


class TestCsv:
    def _ing(self):
        return _F["mh723_demo"]()

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh723_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") == 38

    def test_csv_contiene_verdetto_e_margine(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh723_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "margine_annuo_eur_a" in txt
        assert "ricavi_annui_eur_a" in txt
        assert "costo_annuo_eur_a" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "feedstock_t_a" in txt
        assert "ricavo_totale_eur_t" in txt
        assert "co2_evitata_t_a" in txt
        assert "ricavo_cobalto_eur_t" in txt
        assert "ricavo_nichel_eur_t" in txt
        assert "capex_eur" in txt
        assert "fattore_co2_t_t" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh723_csv"](bc, self._ing())
        assert f"margine_annuo_eur_a;{bc['margine_annuo_eur_a']}" in txt
        assert f"ricavi_annui_eur_a;{bc['ricavi_annui_eur_a']}" in txt
        assert "feedstock_t_a;10000.0" in txt
        assert "opex_fisso_eur_a;5000000.0" in txt
        assert f"ricavo_totale_eur_t;{bc['ricavo_totale_eur_t']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def723["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def723\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 23, ui_keys
        demo_keys = set(_F["mh723_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh723_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh723_demo():")
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
        ui_keys = set(re.findall(r'_def723\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W724 (26/10/2026) - tab723' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh723_num", "mh723_nneg", "mh723_pos",
                     "mh723_int_pos", "mh723_recupero_valida",
                     "mh723_ricavo_per_t", "mh723_ricavi_annui",
                     "mh723_costo_annuo", "mh723_margine",
                     "mh723_flussi", "mh723_van_flussi",
                     "mh723_tir_flussi", "mh723_payback_flussi",
                     "mh723_verdetto", "mh723_co2_evitata",
                     "mh723_tabella_metalli", "mh723_valida",
                     "_mh723_neutro", "mh723_calcola",
                     "mh723_sensitivita", "mh723_csv",
                     "mh723_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_nessun_identificatore_futura_tab(self):
        assert "mh724" not in _helpers_src()
        assert "mh724" not in _ui_src()
        assert "st724" not in _ui_src()
        assert "tab724" not in _ui_src()

    def test_helpers_parse_ast(self):
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w724_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE723) == 1

    def test_blocco_with_tab723(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab723:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE723

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st723_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 28, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st723_") for k in keys)

    def test_chiavi_st_input_sono_24(self):
        """Le 24 chiavi di input/bottone (23 input +
        bottone calcola) sono tutte presenti; le
        altre 4 sono solo chiavi di
        visualizzazione (fig, heatmap, flussi, CSV)."""
        keys = re.findall(r'key="(st723_[a-z0-9_]+)"', _ui_src())
        attese = ["st723_feedstock", "st723_costo_trattamento",
                  "st723_opex_fisso", "st723_capex",
                  "st723_vita_progetto",
                  "st723_contenuto_litio", "st723_recupero_litio",
                  "st723_prezzo_litio",
                  "st723_contenuto_cobalto",
                  "st723_recupero_cobalto", "st723_prezzo_cobalto",
                  "st723_contenuto_nichel", "st723_recupero_nichel",
                  "st723_prezzo_nichel",
                  "st723_contenuto_rame", "st723_recupero_rame",
                  "st723_prezzo_rame",
                  "st723_contenuto_alluminio",
                  "st723_recupero_alluminio",
                  "st723_prezzo_alluminio",
                  "st723_wacc", "st723_tolleranza",
                  "st723_fattore_co2",
                  "st723_calcola"]
        assert len(attese) == 24
        for k in attese:
            assert k in keys, k

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg723" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg723") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg723")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "Ricavi annui (€/anno)" in src
        assert "Margine annuo (€/anno)" in src
        assert "VAN (€)" in src
        assert "CO2 evitata (t/anno)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_presente(self):
        src = _ui_src().lower()
        assert "second-life" in src
        assert "discarica" in src
        assert "minerale" in src
        assert "cobalto" in src
        assert "nichel" in src

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert '"Litio"' in src
        assert '"Cobalto"' in src
        assert '"Nichel"' in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh723_csv" in src
        assert "riciclo_batterie_business_case.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN" in src
        assert "mh723_sensitivita" in src
        assert "Heatmap" in src
        assert "Prezzo litio" in src
        assert "Costo di trattamento" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st723_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W724 (26/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab723:")
