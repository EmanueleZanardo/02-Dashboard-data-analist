"""Test tab728 "🔋🟡 Batterie zinco-aria: l'accumulo a basso costo paga contro LFP?"

Nuova tab tab728 (zinco-aria contro LFP, w729).
Business case di un accumulo zinco-aria
contro LFP che eroga la STESSA energia
utile per ciclo, con gli stessi cicli/anno
e gli stessi prezzi di carica e scarica:
due rami indipendenti, ognuno con il suo
rendimento di ciclo, CAPEX, O&M e vita in
cicli; anni effettivi = min(vita di
progetto, floor(vita in cicli / cicli
annui)); VAN, TIR, payback, LCOS, delta
VAN, verdetto zinco-aria.

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
potenza 1000 kW; capacita' 8000 kWh; DoD
0,90; rendimento zinco-aria 0,55; cicli
annui 250; prezzo di carica 60 EUR/MWh;
prezzo di scarica 140 EUR/MWh; O&M
zinco-aria 12 EUR/kWh/anno; CAPEX potenza
zinco-aria 150 EUR/kW; CAPEX energia
zinco-aria 80 EUR/kWh; vita di progetto 15
anni; vita in cicli zinco-aria 3000; WACC
0,06 (6 %); tolleranza 0,10 (10 % del
CAPEX); rendimento LFP 0,88; CAPEX potenza
LFP 200 EUR/kW; CAPEX energia LFP 180
EUR/kWh; O&M LFP 10 EUR/kWh/anno; vita in
cicli LFP 6000.

- e_utile_kwh_ciclo = 7200.0
- e_scaricata_kwh_anno = 1800000.0
- e_caricata_zn_kwh_anno = 3272727.2727272725
- costo_carica_zn_eur_anno = 196363.63636363635
- ricavo_scarica_eur_anno = 252000.0
- om_zn_eur_anno = 96000.0
- capex_zn_eur = 790000.0
- anni_effettivi_zn = 12
- netto_zn_eur_anno = -40363.63636363635
- van_zn = -1128402.4281391085
- tir_zn = None
- payback_zn = None
- lcos_zn_eur_mwh = 198.99831649831648
- e_caricata_lfp_kwh_anno = 2045454.5454545454
- costo_carica_lfp_eur_anno = 122727.27272727274
- om_lfp_eur_anno = 80000.0
- capex_lfp_eur = 1640000.0
- anni_effettivi_lfp = 15
- netto_lfp_eur_anno = 49272.727272727265
- van_lfp = -1161451.0044222174
- tir_lfp = -8.631086301146697
- payback_lfp = None
- lcos_lfp_eur_mwh = 173.36700336700338
- delta_van = 33048.57628310891
- verdetto = 'NON_CONVIENTE'

Scomposizione: E_utile 8000 x 0,90 = 7200,0
kWh/ciclo; E_scaricata 7200,0 x 250 =
1800000,0 kWh/anno; E_caricata zinco-aria
1800000,0 / 0,55 = 3272727,2727272725
kWh/anno; costo carica zinco-aria
3272727,2727272725 / 1000 x 60 =
196363,63636363635 EUR/anno; ricavo
scarica 1800000,0 / 1000 x 140 = 252000,0
EUR/anno; O&M zinco-aria 8000 x 12 =
96000,0 EUR/anno; netto zinco-aria
252000,0 - 196363,63636363635 - 96000,0 =
-40363,63636363635 EUR/anno; CAPEX
zinco-aria 1000 x 150 + 8000 x 80 =
790000,0 EUR; anni effettivi zinco-aria
min(15, 3000 / 250 = 12) = 12; flussi
zinco-aria: anno 0 -790000,0, anni 1-12
netto -40363,63636363635 (piatti); VAN
zinco-aria -1128402,4281391085 a WACC 6 %
su 12 anni; TIR zinco-aria None (tutti i
flussi negativi: nessun tasso azzera un
VAN sempre negativo); payback zinco-aria
None (il cumulato resta negativo);
LCOS zinco-aria (790000,0 / 12 + 96000,0 +
196363,63636363635) / (1800000,0 / 1000) =
198,99831649831648 EUR/MWh; E_caricata LFP
1800000,0 / 0,88 = 2045454,5454545454
kWh/anno; costo carica LFP
2045454,5454545454 / 1000 x 60 =
122727,27272727274 EUR/anno; O&M LFP 8000
x 10 = 80000,0 EUR/anno; netto LFP
252000,0 - 122727,27272727274 - 80000,0 =
49272,727272727265 EUR/anno; CAPEX LFP
1000 x 200 + 8000 x 180 = 1640000,0 EUR;
anni effettivi LFP min(15, 6000 / 250 = 24)
= 15; VAN LFP -1161451,0044222174 a WACC
6 % su 15 anni; TIR LFP
-8,631086301146697 % (il tasso che azzera
il VAN dei flussi LFP); payback LFP None
(il cumulato resta negativo: -1640000,0 +
15 x 49272,727272727265 < 0); LCOS LFP
(1640000,0 / 15 + 80000,0 +
122727,27272727274) / 1800,0 =
173,36700336700338 EUR/MWh; delta VAN
-1128402,4281391085 - (-1161451,0044222174)
= 33048,57628310891 EUR; verdetto
NON_CONVIENTE perche' VAN zinco-aria < 0 e
|VAN| 1128402,43 > tolleranza 0,10 x
790000,0 = 79000,0 EUR.
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
    if (p / "w729_helpers.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w729_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w729_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w729_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w729_helpers.py: {missing}")
    return out


_F = _load("mh728_num", "mh728_nneg", "mh728_pos",
           "mh728_int_pos", "mh728_frac_01",
           "mh728_frac_01_incl", "mh728_frac_toll",
           "mh728_e_utile", "mh728_e_scaricata",
           "mh728_e_caricata", "mh728_costo_carica",
           "mh728_ricavo_scarica", "mh728_om",
           "mh728_capex", "mh728_anni_effettivi",
           "mh728_netto", "mh728_flussi",
           "mh728_van_flussi", "mh728_tir_flussi",
           "mh728_payback_flussi", "mh728_lcos",
           "mh728_verdetto", "mh728_ramo",
           "mh728_valida", "_mh728_neutro",
           "mh728_calcola", "mh728_confronto",
           "mh728_csv", "mh728_demo", "demo_calcoli")

TITLE728 = ("🔋🟡 Batterie zinco-aria: l'accumulo "
            "a basso costo paga contro LFP?")

E_UTILE_DEMO = 7200.0
E_SCAR_DEMO = 1800000.0
E_CAR_ZN_DEMO = 3272727.2727272725
CC_ZN_DEMO = 196363.63636363635
RIC_DEMO = 252000.0
OM_ZN_DEMO = 96000.0
CAPEX_ZN_DEMO = 790000.0
ANNI_ZN_DEMO = 12
NETTO_ZN_DEMO = -40363.63636363635
VAN_ZN_DEMO = -1128402.4281391085
LCOS_ZN_DEMO = 198.99831649831648
E_CAR_LFP_DEMO = 2045454.5454545454
CC_LFP_DEMO = 122727.27272727274
OM_LFP_DEMO = 80000.0
CAPEX_LFP_DEMO = 1640000.0
ANNI_LFP_DEMO = 15
NETTO_LFP_DEMO = 49272.727272727265
VAN_LFP_DEMO = -1161451.0044222174
TIR_LFP_DEMO = -8.631086301146697
LCOS_LFP_DEMO = 173.36700336700338
DELTA_DEMO = 33048.57628310891
VERDETTO_DEMO = "NON_CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w729_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w729_ui.py").read_text(encoding="utf-8")


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh728_demo"]()
        d.update(kw)
        return _F["mh728_valida"](**d)

    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh728_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh728_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh728_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh728_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh728_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh728_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh728_pos"](0.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh728_int_pos"](2.5, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh728_int_pos"](15.0, "x") == 15

    def test_frac_01_rifiuta_zero_e_uno(self):
        with pytest.raises(ValueError):
            _F["mh728_frac_01"](0.0, "x")
        with pytest.raises(ValueError):
            _F["mh728_frac_01"](1.0, "x")

    def test_frac_01_incl_accetta_uno(self):
        assert _F["mh728_frac_01_incl"](1.0, "x") == 1.0

    def test_frac_01_incl_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh728_frac_01_incl"](0.0, "x")

    def test_frac_toll_accetta_zero_rifiuta_uno(self):
        assert _F["mh728_frac_toll"](0.0, "x") == 0.0
        with pytest.raises(ValueError):
            _F["mh728_frac_toll"](1.0, "x")
        with pytest.raises(ValueError):
            _F["mh728_frac_toll"](-0.01, "x")

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_pot_zero_non_valida(self):
        assert self._val(pot_kw=0.0)["valido"] is False

    def test_capacita_zero_non_valida(self):
        assert self._val(capacita_kwh=0.0)["valido"] is False

    def test_dod_zero_non_valida_dod_uno_valida(self):
        assert self._val(dod=0.0)["valido"] is False
        assert self._val(dod=1.0)["valido"] is True

    def test_rte_fuori_intervallo_non_validi(self):
        assert self._val(rte_zn=0.0)["valido"] is False
        assert self._val(rte_zn=1.0)["valido"] is False
        assert self._val(rte_lfp=0.0)["valido"] is False
        assert self._val(rte_lfp=1.0)["valido"] is False

    def test_cicli_zero_e_frazione_non_validi(self):
        assert self._val(cicli_anno=0)["valido"] is False
        assert self._val(cicli_anno=250.5)["valido"] is False

    def test_negativi_non_validi(self):
        for k in ("prezzo_carica_eur_mwh",
                  "prezzo_scarica_eur_mwh",
                  "om_zn_eur_kwh_anno",
                  "capex_kw_zn_eur_kw",
                  "capex_kwh_zn_eur_kwh",
                  "capex_kw_lfp_eur_kw",
                  "capex_kwh_lfp_eur_kwh",
                  "om_lfp_eur_kwh_anno"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_vita_zero_e_frazione_non_valide(self):
        assert self._val(vita_anni=0)["valido"] is False
        assert self._val(vita_anni=15.5)["valido"] is False

    def test_vita_cicli_zero_non_valide(self):
        assert self._val(vita_cicli_zn=0)["valido"] is False
        assert self._val(vita_cicli_lfp=0)["valido"] is False

    def test_wacc_zero_e_uno_non_validi(self):
        assert self._val(wacc_frac=0.0)["valido"] is False
        assert self._val(wacc_frac=1.0)["valido"] is False
        assert self._val(wacc_frac=0.06)["valido"] is True

    def test_tolleranza_uno_non_valida_zero_valida(self):
        assert self._val(tolleranza_frac=1.0)["valido"] is False
        assert self._val(tolleranza_frac=0.0)["valido"] is True

    def test_nan_non_valido(self):
        assert self._val(pot_kw=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(pot_kw=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(vita_anni=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(pot_kw="1000")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(prezzo_carica_eur_mwh=0.0)["valido"] is True
        assert self._val(prezzo_scarica_eur_mwh=0.0)["valido"] is True
        assert self._val(om_zn_eur_kwh_anno=0.0)["valido"] is True
        assert self._val(capex_kw_zn_eur_kw=0.0)["valido"] is True
        assert self._val(tolleranza_frac=0.0)["valido"] is True


class TestFunzioni:
    def test_e_utile_demo(self):
        assert _F["mh728_e_utile"](
            8000.0, 0.90) == pytest.approx(
            E_UTILE_DEMO, rel=REL)

    def test_e_scaricata_demo(self):
        assert _F["mh728_e_scaricata"](
            E_UTILE_DEMO, 250) == pytest.approx(
            E_SCAR_DEMO, rel=REL)

    def test_e_caricata_zn_demo(self):
        assert _F["mh728_e_caricata"](
            E_SCAR_DEMO, 0.55) == pytest.approx(
            E_CAR_ZN_DEMO, rel=REL)

    def test_e_caricata_lfp_demo(self):
        assert _F["mh728_e_caricata"](
            E_SCAR_DEMO, 0.88) == pytest.approx(
            E_CAR_LFP_DEMO, rel=REL)

    def test_costo_carica_zn_demo(self):
        assert _F["mh728_costo_carica"](
            E_CAR_ZN_DEMO, 60.0) == pytest.approx(
            CC_ZN_DEMO, rel=REL)

    def test_costo_carica_lfp_demo(self):
        assert _F["mh728_costo_carica"](
            E_CAR_LFP_DEMO, 60.0) == pytest.approx(
            CC_LFP_DEMO, rel=REL)

    def test_ricavo_scarica_demo(self):
        assert _F["mh728_ricavo_scarica"](
            E_SCAR_DEMO, 140.0) == pytest.approx(
            RIC_DEMO, rel=REL)

    def test_om_zn_demo(self):
        assert _F["mh728_om"](
            8000.0, 12.0) == pytest.approx(
            OM_ZN_DEMO, rel=REL)

    def test_om_lfp_demo(self):
        assert _F["mh728_om"](
            8000.0, 10.0) == pytest.approx(
            OM_LFP_DEMO, rel=REL)

    def test_capex_zn_demo(self):
        assert _F["mh728_capex"](
            1000.0, 150.0, 8000.0, 80.0) == pytest.approx(
            CAPEX_ZN_DEMO, rel=REL)

    def test_capex_lfp_demo(self):
        assert _F["mh728_capex"](
            1000.0, 200.0, 8000.0, 180.0) == pytest.approx(
            CAPEX_LFP_DEMO, rel=REL)

    def test_anni_effettivi_demo(self):
        assert _F["mh728_anni_effettivi"](15, 3000, 250) == 12
        assert _F["mh728_anni_effettivi"](15, 6000, 250) == 15

    def test_anni_effettivi_limitati_dai_cicli(self):
        assert _F["mh728_anni_effettivi"](15, 1000, 250) == 4
        assert _F["mh728_anni_effettivi"](15, 2500, 250) == 10
        assert _F["mh728_anni_effettivi"](15, 3750, 250) == 15

    def test_anni_effettivi_minimo_uno(self):
        assert _F["mh728_anni_effettivi"](15, 100, 250) == 1

    def test_anni_effettivi_none_se_cicli_o_vita_non_validi(self):
        assert _F["mh728_anni_effettivi"](15, 0, 250) is None
        assert _F["mh728_anni_effettivi"](15, 3000, 0) is None
        assert _F["mh728_anni_effettivi"](15, -100, 250) is None

    def test_netto_zn_demo(self):
        assert _F["mh728_netto"](
            RIC_DEMO, CC_ZN_DEMO, OM_ZN_DEMO) == pytest.approx(
            NETTO_ZN_DEMO, rel=REL)

    def test_netto_lfp_demo(self):
        assert _F["mh728_netto"](
            RIC_DEMO, CC_LFP_DEMO, OM_LFP_DEMO) == pytest.approx(
            NETTO_LFP_DEMO, rel=REL)

    def test_netto_puo_essere_negativo(self):
        assert _F["mh728_netto"](
            100000.0, 150000.0, 10000.0) == pytest.approx(
            -60000.0, rel=REL)

    def test_flussi_demo(self):
        flussi = _F["mh728_flussi"](CAPEX_ZN_DEMO, NETTO_ZN_DEMO,
                                     ANNI_ZN_DEMO)
        assert len(flussi) == ANNI_ZN_DEMO + 1
        assert flussi[0] == pytest.approx(-CAPEX_ZN_DEMO, rel=REL)
        assert all(f == pytest.approx(NETTO_ZN_DEMO, rel=REL)
                   for f in flussi[1:])

    def test_van_flussi_demo_zn(self):
        flussi = _F["mh728_flussi"](CAPEX_ZN_DEMO, NETTO_ZN_DEMO,
                                     ANNI_ZN_DEMO)
        assert abs(_F["mh728_van_flussi"](
            flussi, 0.06) - VAN_ZN_DEMO) <= 1.0

    def test_van_flussi_tasso_zero(self):
        flussi = _F["mh728_flussi"](CAPEX_ZN_DEMO, NETTO_ZN_DEMO,
                                     ANNI_ZN_DEMO)
        atteso = -CAPEX_ZN_DEMO + NETTO_ZN_DEMO * ANNI_ZN_DEMO
        assert _F["mh728_van_flussi"](
            flussi, 0.0) == pytest.approx(atteso, rel=1e-12)

    def test_van_flussi_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh728_van_flussi"]([100.0, 100.0], -0.01)

    def test_tir_none_flussi_tutti_negativi(self):
        flussi = _F["mh728_flussi"](CAPEX_ZN_DEMO, NETTO_ZN_DEMO,
                                     ANNI_ZN_DEMO)
        assert _F["mh728_tir_flussi"](flussi) is None

    def test_tir_none_tutti_flussi_non_negativi(self):
        assert _F["mh728_tir_flussi"](
            [0.0] + [NETTO_LFP_DEMO] * 15) is None

    def test_tir_none_nessun_cambio_segno_negativo(self):
        assert _F["mh728_tir_flussi"](
            [-1000.0] + [-100.0] * 10) is None

    def test_tir_esiste_caso_semplice_100_120(self):
        assert _F["mh728_tir_flussi"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_tir_caso_semplice_1000_500_500_zero(self):
        assert abs(_F["mh728_tir_flussi"](
            [-1000.0, 500.0, 500.0])) <= 1e-9

    def test_tir_lfp_demo(self):
        flussi = _F["mh728_flussi"](CAPEX_LFP_DEMO, NETTO_LFP_DEMO,
                                     ANNI_LFP_DEMO)
        tir = _F["mh728_tir_flussi"](flussi)
        assert tir is not None
        assert tir * 100.0 == pytest.approx(TIR_LFP_DEMO, rel=1e-9)

    def test_payback_demo_none(self):
        flussi = _F["mh728_flussi"](CAPEX_ZN_DEMO, NETTO_ZN_DEMO,
                                     ANNI_ZN_DEMO)
        assert _F["mh728_payback_flussi"](flussi) is None

    def test_payback_semplice_due(self):
        assert _F["mh728_payback_flussi"](
            [-1000.0, 500.0, 500.0, 500.0]) == 2

    def test_payback_zero_se_cumulato_anno_zero_non_negativo(self):
        assert _F["mh728_payback_flussi"](
            [0.0, 100.0]) == 0

    def test_payback_none_se_mai(self):
        assert _F["mh728_payback_flussi"](
            [-10000000.0] + [NETTO_LFP_DEMO] * 15) is None

    def test_lcos_zn_demo(self):
        assert _F["mh728_lcos"](
            CAPEX_ZN_DEMO, ANNI_ZN_DEMO, OM_ZN_DEMO,
            CC_ZN_DEMO, E_SCAR_DEMO) == pytest.approx(
            LCOS_ZN_DEMO, rel=REL)

    def test_lcos_lfp_demo(self):
        assert _F["mh728_lcos"](
            CAPEX_LFP_DEMO, ANNI_LFP_DEMO, OM_LFP_DEMO,
            CC_LFP_DEMO, E_SCAR_DEMO) == pytest.approx(
            LCOS_LFP_DEMO, rel=REL)

    def test_lcos_none_se_energia_zero(self):
        assert _F["mh728_lcos"](
            1000.0, 10, 100.0, 50.0, 0.0) is None

    def test_lcos_formula_indipendente(self):
        assert _F["mh728_lcos"](
            120000.0, 10, 5000.0, 10000.0,
            100000.0) == pytest.approx(
            (12000.0 + 5000.0 + 10000.0) / 100.0, rel=REL)

    def test_verdetto_conviente_demo_no(self):
        assert _F["mh728_verdetto"](
            VAN_ZN_DEMO, CAPEX_ZN_DEMO, 0.10,
            E_SCAR_DEMO, NETTO_ZN_DEMO,
            ANNI_ZN_DEMO) == VERDETTO_DEMO

    def test_verdetto_conviente_van_positivo(self):
        assert _F["mh728_verdetto"](
            1000.0, CAPEX_ZN_DEMO, 0.10,
            E_SCAR_DEMO, NETTO_LFP_DEMO,
            ANNI_ZN_DEMO) == "CONVIENTE"

    def test_verdetto_van_zero_marginale(self):
        assert _F["mh728_verdetto"](
            0.0, CAPEX_ZN_DEMO, 0.10,
            E_SCAR_DEMO, NETTO_LFP_DEMO,
            ANNI_ZN_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh728_verdetto"](
            -0.10 * CAPEX_ZN_DEMO, CAPEX_ZN_DEMO, 0.10,
            E_SCAR_DEMO, NETTO_LFP_DEMO,
            ANNI_ZN_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_oltre_limite(self):
        assert _F["mh728_verdetto"](
            -0.10 * CAPEX_ZN_DEMO - 1.0, CAPEX_ZN_DEMO, 0.10,
            E_SCAR_DEMO, NETTO_LFP_DEMO,
            ANNI_ZN_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_energia_zero(self):
        assert _F["mh728_verdetto"](
            1000.0, CAPEX_ZN_DEMO, 0.10, 0.0,
            NETTO_LFP_DEMO, ANNI_ZN_DEMO) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_netto_nan(self):
        assert _F["mh728_verdetto"](
            1000.0, CAPEX_ZN_DEMO, 0.10, E_SCAR_DEMO,
            float("nan"), ANNI_ZN_DEMO) == "NON_CALCOLABILE"

    def test_verdetto_non_calcolabile_anni_zero_e_none(self):
        assert _F["mh728_verdetto"](
            1000.0, CAPEX_ZN_DEMO, 0.10, E_SCAR_DEMO,
            NETTO_LFP_DEMO, 0) == "NON_CALCOLABILE"
        assert _F["mh728_verdetto"](
            1000.0, CAPEX_ZN_DEMO, 0.10, E_SCAR_DEMO,
            NETTO_LFP_DEMO, None) == "NON_CALCOLABILE"

    def test_ramo_zn_demo(self):
        r = _F["mh728_ramo"](
            E_SCAR_DEMO, 0.55, 60.0, 140.0, 12.0,
            8000.0, 1000.0, 150.0, 80.0, 15, 3000, 250, 0.06)
        assert r["e_caricata_kwh_anno"] == pytest.approx(
            E_CAR_ZN_DEMO, rel=REL)
        assert r["costo_carica_eur_anno"] == pytest.approx(
            CC_ZN_DEMO, rel=REL)
        assert r["ricavo_scarica_eur_anno"] == pytest.approx(
            RIC_DEMO, rel=REL)
        assert r["om_eur_anno"] == pytest.approx(
            OM_ZN_DEMO, rel=REL)
        assert r["capex_eur"] == pytest.approx(
            CAPEX_ZN_DEMO, rel=REL)
        assert r["anni_effettivi"] == ANNI_ZN_DEMO
        assert r["netto_eur_anno"] == pytest.approx(
            NETTO_ZN_DEMO, rel=REL)
        assert abs(r["van"] - VAN_ZN_DEMO) <= 1.0
        assert r["tir"] is None
        assert r["payback"] is None
        assert r["lcos_eur_mwh"] == pytest.approx(
            LCOS_ZN_DEMO, rel=REL)

    def test_ramo_lfp_demo(self):
        r = _F["mh728_ramo"](
            E_SCAR_DEMO, 0.88, 60.0, 140.0, 10.0,
            8000.0, 1000.0, 200.0, 180.0, 15, 6000, 250, 0.06)
        assert r["e_caricata_kwh_anno"] == pytest.approx(
            E_CAR_LFP_DEMO, rel=REL)
        assert r["capex_eur"] == pytest.approx(
            CAPEX_LFP_DEMO, rel=REL)
        assert r["anni_effettivi"] == ANNI_LFP_DEMO
        assert abs(r["van"] - VAN_LFP_DEMO) <= 1.0
        assert r["tir"] * 100.0 == pytest.approx(
            TIR_LFP_DEMO, rel=1e-9)

    def test_confronto_demo(self):
        rzn = _F["mh728_ramo"](
            E_SCAR_DEMO, 0.55, 60.0, 140.0, 12.0,
            8000.0, 1000.0, 150.0, 80.0, 15, 3000, 250, 0.06)
        rlf = _F["mh728_ramo"](
            E_SCAR_DEMO, 0.88, 60.0, 140.0, 10.0,
            8000.0, 1000.0, 200.0, 180.0, 15, 6000, 250, 0.06)
        df = _F["mh728_confronto"](E_SCAR_DEMO, rzn, rlf)
        assert list(df.columns) == ["Voce", "Zinco-aria",
                                    "LFP", "Differenza"]
        assert len(df) == 10
        riga = df[df["Voce"] == "CAPEX (EUR)"].iloc[0]
        assert riga["Zinco-aria"] == pytest.approx(
            CAPEX_ZN_DEMO, rel=REL)
        assert riga["LFP"] == pytest.approx(
            CAPEX_LFP_DEMO, rel=REL)
        assert riga["Differenza"] == pytest.approx(
            CAPEX_ZN_DEMO - CAPEX_LFP_DEMO, rel=REL)
        riga_van = df[df["Voce"] == "VAN (EUR)"].iloc[0]
        assert riga_van["Differenza"] == pytest.approx(
            DELTA_DEMO, rel=REL)
        riga_ric = df[df["Voce"] == "Ricavo scarica (EUR/anno)"].iloc[0]
        assert riga_ric["Differenza"] == pytest.approx(
            0.0, abs=1e-9)


class TestDemo:
    def _bc(self, **kw):
        d = _F["mh728_demo"]()
        d.update(kw)
        return _F["mh728_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["e_utile_kwh_ciclo"] == pytest.approx(
            E_UTILE_DEMO, rel=REL)
        assert c["e_scaricata_kwh_anno"] == pytest.approx(
            E_SCAR_DEMO, rel=REL)
        assert c["e_caricata_zn_kwh_anno"] == pytest.approx(
            E_CAR_ZN_DEMO, rel=REL)
        assert c["costo_carica_zn_eur_anno"] == pytest.approx(
            CC_ZN_DEMO, rel=REL)
        assert c["ricavo_scarica_eur_anno"] == pytest.approx(
            RIC_DEMO, rel=REL)
        assert c["om_zn_eur_anno"] == pytest.approx(
            OM_ZN_DEMO, rel=REL)
        assert c["capex_zn_eur"] == pytest.approx(
            CAPEX_ZN_DEMO, rel=REL)
        assert c["anni_effettivi_zn"] == ANNI_ZN_DEMO
        assert c["netto_zn_eur_anno"] == pytest.approx(
            NETTO_ZN_DEMO, rel=REL)
        assert abs(c["van_zn"] - VAN_ZN_DEMO) <= 1.0
        assert c["tir_zn"] is None
        assert c["payback_zn"] is None
        assert c["lcos_zn_eur_mwh"] == pytest.approx(
            LCOS_ZN_DEMO, rel=REL)
        assert c["e_caricata_lfp_kwh_anno"] == pytest.approx(
            E_CAR_LFP_DEMO, rel=REL)
        assert c["costo_carica_lfp_eur_anno"] == pytest.approx(
            CC_LFP_DEMO, rel=REL)
        assert c["om_lfp_eur_anno"] == pytest.approx(
            OM_LFP_DEMO, rel=REL)
        assert c["capex_lfp_eur"] == pytest.approx(
            CAPEX_LFP_DEMO, rel=REL)
        assert c["anni_effettivi_lfp"] == ANNI_LFP_DEMO
        assert c["netto_lfp_eur_anno"] == pytest.approx(
            NETTO_LFP_DEMO, rel=REL)
        assert abs(c["van_lfp"] - VAN_LFP_DEMO) <= 1.0
        assert abs(c["tir_lfp"] - TIR_LFP_DEMO) <= 0.01
        assert c["payback_lfp"] is None
        assert c["lcos_lfp_eur_mwh"] == pytest.approx(
            LCOS_LFP_DEMO, rel=REL)
        assert abs(c["delta_van"] - DELTA_DEMO) <= 1.0
        assert c["verdetto"] == VERDETTO_DEMO
        assert len(c["flussi_zn"]) == ANNI_ZN_DEMO + 1
        assert len(c["flussi_lfp"]) == ANNI_LFP_DEMO + 1

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()[
            "van_zn"] == _F["demo_calcoli"]()["van_zn"]
        assert _F["demo_calcoli"]()[
            "delta_van"] == _F["demo_calcoli"]()["delta_van"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        d = _F["mh728_demo"]()
        b = _F["mh728_calcola"](**d)
        coppie = [("e_utile_kwh_ciclo", E_UTILE_DEMO),
                  ("e_scaricata_kwh_anno", E_SCAR_DEMO),
                  ("e_caricata_zn_kwh_anno", E_CAR_ZN_DEMO),
                  ("costo_carica_zn_eur_anno", CC_ZN_DEMO),
                  ("ricavo_scarica_eur_anno", RIC_DEMO),
                  ("om_zn_eur_anno", OM_ZN_DEMO),
                  ("capex_zn_eur", CAPEX_ZN_DEMO),
                  ("netto_zn_eur_anno", NETTO_ZN_DEMO),
                  ("e_caricata_lfp_kwh_anno", E_CAR_LFP_DEMO),
                  ("costo_carica_lfp_eur_anno", CC_LFP_DEMO),
                  ("om_lfp_eur_anno", OM_LFP_DEMO),
                  ("capex_lfp_eur", CAPEX_LFP_DEMO),
                  ("netto_lfp_eur_anno", NETTO_LFP_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert abs(b["van_zn"] - VAN_ZN_DEMO) <= 1.0
        assert abs(b["van_lfp"] - VAN_LFP_DEMO) <= 1.0
        assert abs(b["delta_van"] - DELTA_DEMO) <= 1.0
        assert b["verdetto"] == VERDETTO_DEMO

    def test_demo_defaults(self):
        d = _F["mh728_demo"]()
        assert d["pot_kw"] == 1000.0
        assert d["capacita_kwh"] == 8000.0
        assert d["dod"] == 0.90
        assert d["rte_zn"] == 0.55
        assert d["cicli_anno"] == 250
        assert d["prezzo_carica_eur_mwh"] == 60.0
        assert d["prezzo_scarica_eur_mwh"] == 140.0
        assert d["om_zn_eur_kwh_anno"] == 12.0
        assert d["capex_kw_zn_eur_kw"] == 150.0
        assert d["capex_kwh_zn_eur_kwh"] == 80.0
        assert d["vita_anni"] == 15
        assert d["vita_cicli_zn"] == 3000
        assert d["wacc_frac"] == 0.06
        assert d["tolleranza_frac"] == 0.10
        assert d["rte_lfp"] == 0.88
        assert d["capex_kw_lfp_eur_kw"] == 200.0
        assert d["capex_kwh_lfp_eur_kwh"] == 180.0
        assert d["om_lfp_eur_kwh_anno"] == 10.0
        assert d["vita_cicli_lfp"] == 6000
        assert len(d) == 19

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("e_utile_kwh_ciclo",
                       "e_scaricata_kwh_anno",
                       "e_caricata_zn_kwh_anno",
                       "costo_carica_zn_eur_anno",
                       "ricavo_scarica_eur_anno",
                       "om_zn_eur_anno",
                       "capex_zn_eur",
                       "netto_zn_eur_anno",
                       "van_zn",
                       "lcos_zn_eur_mwh",
                       "e_caricata_lfp_kwh_anno",
                       "costo_carica_lfp_eur_anno",
                       "om_lfp_eur_anno",
                       "capex_lfp_eur",
                       "netto_lfp_eur_anno",
                       "van_lfp",
                       "tir_lfp",
                       "lcos_lfp_eur_mwh",
                       "delta_van"):
            assert repr(c[chiave]) in doc, chiave
        assert "tir_zn = None" in doc
        assert "payback_zn = None" in doc
        assert "payback_lfp = None" in doc
        assert "anni_effettivi_zn = 12" in doc
        assert "anni_effettivi_lfp = 15" in doc
        assert "verdetto = 'NON_CONVIENTE'" in doc

    def test_spread_alto_conviente(self):
        # Prezzo di scarica 400: netto zinco-aria
        # 427636,36, VAN 2795236,54, TIR 53,82 %,
        # payback 2 -> CONVIENTE.
        n = self._bc(prezzo_scarica_eur_mwh=400.0)
        assert n["valid"] is True
        assert n["netto_zn_eur_anno"] == pytest.approx(
            427636.36363636365, rel=REL)
        assert abs(n["van_zn"] - 2795236.5359602836) <= 1.0
        assert abs(n["tir_zn"] - 53.82272333103303) <= 0.01
        assert n["payback_zn"] == 2
        assert n["verdetto"] == "CONVIENTE"

    def test_spread_medio_marginale(self):
        # Prezzo di scarica 210: netto zinco-aria
        # 85636,36, VAN -72038,09, TIR 4,30 %,
        # payback 10 -> MARGINALE (|VAN| <=
        # 10 % di 790000 = 79000).
        n = self._bc(prezzo_scarica_eur_mwh=210.0)
        assert n["valid"] is True
        assert n["netto_zn_eur_anno"] == pytest.approx(
            85636.36363636365, rel=REL)
        assert abs(n["van_zn"] - (-72038.09165081038)) <= 1.0
        assert abs(n["tir_zn"] - 4.297648855796007) <= 0.01
        assert n["payback_zn"] == 10
        assert n["verdetto"] == "MARGINALE"

    def test_spread_200_non_conviente(self):
        # Prezzo di scarica 200: netto 67636,36,
        # VAN -222947,28 -> NON_CONVIENTE
        # (|VAN| > 79000).
        n = self._bc(prezzo_scarica_eur_mwh=200.0)
        assert n["valid"] is True
        assert abs(n["van_zn"] - (-222947.28)) <= 1.0
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_anni_limitati_dai_cicli_in_calcola(self):
        n = self._bc(vita_cicli_zn=1000)
        assert n["anni_effettivi_zn"] == 4
        assert len(n["flussi_zn"]) == 5
        m = self._bc(vita_cicli_lfp=2500)
        assert m["anni_effettivi_lfp"] == 10
        assert len(m["flussi_lfp"]) == 11

    def test_capex_zero_tir_none_payback_zero(self):
        # CAPEX zinco-aria zero e prezzo di
        # scarica 400: tutti i flussi zinco-aria
        # >= 0 -> TIR None, payback 0, VAN
        # 3585236,54 -> CONVIENTE.
        n = self._bc(capex_kw_zn_eur_kw=0.0,
                     capex_kwh_zn_eur_kwh=0.0,
                     prezzo_scarica_eur_mwh=400.0)
        assert n["valid"] is True
        assert n["capex_zn_eur"] == pytest.approx(0.0, abs=1e-9)
        assert n["tir_zn"] is None
        assert n["payback_zn"] == 0
        assert abs(n["van_zn"] - 3585236.5359602836) <= 1.0
        assert n["verdetto"] == "CONVIENTE"

    def test_pot_zero_neutro(self):
        n = self._bc(pot_kw=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["valid"] is False

    def test_dod_zero_neutro(self):
        n = self._bc(dod=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_rte_uno_neutro(self):
        n = self._bc(rte_zn=1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"
        n = self._bc(rte_lfp=1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_zero_e_uno_neutri(self):
        assert self._bc(wacc_frac=0.0)["verdetto"] == "NON_CALCOLABILE"
        assert self._bc(wacc_frac=1.0)["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_uno_neutro(self):
        n = self._bc(tolleranza_frac=1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_cicli_zero_neutro(self):
        n = self._bc(cicli_anno=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_cicli_zero_neutro(self):
        assert self._bc(vita_cicli_zn=0)["verdetto"] == "NON_CALCOLABILE"
        assert self._bc(vita_cicli_lfp=0)["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(pot_kw=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["netto_zn_eur_anno"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(pot_kw=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(vita_anni=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_stringa_neutro(self):
        n = self._bc(pot_kw="1000")
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh728_neutro"]()
        assert n["valid"] is False
        assert n["errore"] == ""
        assert list(n["df_confronto"].columns) == [
            "Voce", "Zinco-aria", "LFP", "Differenza"]
        assert len(n["df_confronto"]) == 0
        assert list(n["df_flussi"].columns) == ["Anno",
                                               "Flusso zinco-aria (EUR/anno)",
                                               "Cumulato zinco-aria (EUR)",
                                               "Flusso LFP (EUR/anno)",
                                               "Cumulato LFP (EUR)"]
        assert len(n["df_flussi"]) == 0
        assert list(n["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(n["df_tabella"]) == 0
        assert n["flussi_zn"] == []
        assert n["flussi_lfp"] == []
        assert n["tir_zn"] is None
        assert n["tir_lfp"] is None
        assert n["payback_zn"] is None
        assert n["payback_lfp"] is None
        assert n["lcos_zn_eur_mwh"] is None
        assert n["lcos_lfp_eur_mwh"] is None

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh728_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "pot_kw", "capacita_kwh",
                       "dod", "rte_zn", "cicli_anno",
                       "prezzo_carica_eur_mwh",
                       "prezzo_scarica_eur_mwh",
                       "om_zn_eur_kwh_anno",
                       "capex_kw_zn_eur_kw",
                       "capex_kwh_zn_eur_kwh",
                       "vita_anni", "vita_cicli_zn",
                       "wacc_frac", "tolleranza_frac",
                       "rte_lfp", "capex_kw_lfp_eur_kw",
                       "capex_kwh_lfp_eur_kwh",
                       "om_lfp_eur_kwh_anno",
                       "vita_cicli_lfp",
                       "e_utile_kwh_ciclo",
                       "e_scaricata_kwh_anno",
                       "e_caricata_zn_kwh_anno",
                       "costo_carica_zn_eur_anno",
                       "ricavo_scarica_eur_anno",
                       "om_zn_eur_anno",
                       "capex_zn_eur",
                       "anni_effettivi_zn",
                       "netto_zn_eur_anno",
                       "flussi_zn", "van_zn",
                       "tir_zn", "payback_zn",
                       "lcos_zn_eur_mwh",
                       "e_caricata_lfp_kwh_anno",
                       "costo_carica_lfp_eur_anno",
                       "om_lfp_eur_anno",
                       "capex_lfp_eur",
                       "anni_effettivi_lfp",
                       "netto_lfp_eur_anno",
                       "flussi_lfp", "van_lfp",
                       "tir_lfp", "payback_lfp",
                       "lcos_lfp_eur_mwh",
                       "delta_van", "verdetto",
                       "df_confronto", "df_flussi",
                       "df_tabella"):
            assert chiave in n, chiave
        assert n["errore"] == "errore di prova"
        assert n["tir_zn"] is None

    def test_business_case_dataframe_colonne(self):
        b = self._bc()
        assert b["valid"] is True
        assert list(b["df_tabella"].columns) == ["Voce",
                                                 "Valore"]
        assert len(b["df_tabella"]) == 39
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Energia utile per ciclo (kWh/ciclo)" in voci
        assert "VAN zinco-aria (EUR)" in voci
        assert "VAN LFP (EUR)" in voci
        assert "Delta VAN (EUR)" in voci
        assert "LCOS zinco-aria (EUR/MWh)" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso zinco-aria (EUR/anno)",
                                               "Cumulato zinco-aria (EUR)",
                                               "Flusso LFP (EUR/anno)",
                                               "Cumulato LFP (EUR)"]
        assert len(b["df_flussi"]) == ANNI_LFP_DEMO + 1
        assert b["df_flussi"]["Flusso zinco-aria (EUR/anno)"].iloc[0] == \
            pytest.approx(-CAPEX_ZN_DEMO, rel=REL)
        assert b["df_flussi"]["Flusso zinco-aria (EUR/anno)"].iloc[1] == \
            pytest.approx(NETTO_ZN_DEMO, rel=REL)
        assert list(b["df_confronto"].columns) == [
            "Voce", "Zinco-aria", "LFP", "Differenza"]
        assert len(b["df_confronto"]) == 10


class TestCsv:
    def _ing(self):
        return _F["mh728_demo"]()

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh728_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") == 45

    def test_csv_contiene_verdetto_e_costi(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh728_csv"](bc, self._ing())
        assert "verdetto;NON_CONVIENTE" in txt
        assert "costo_carica_zn_eur_anno" in txt
        assert "costo_carica_lfp_eur_anno" in txt
        assert "ricavo_scarica_eur_anno" in txt
        assert "van_zn_eur" in txt
        assert "van_lfp_eur" in txt
        assert "delta_van_eur" in txt
        assert "tir_zn_pct" in txt
        assert "payback_zn_anni" in txt
        assert "lcos_zn_eur_mwh" in txt
        assert "lcos_lfp_eur_mwh" in txt
        assert "pot_kw" in txt
        assert "e_utile_kwh_ciclo" in txt
        assert "capex_zn_eur" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh728_csv"](bc, self._ing())
        assert f"netto_zn_eur_anno;{bc['netto_zn_eur_anno']}" in txt
        assert f"e_scaricata_kwh_anno;{bc['e_scaricata_kwh_anno']}" in txt
        assert "pot_kw;1000.0" in txt
        assert "capex_kwh_zn_eur_kwh;80.0" in txt
        assert f"delta_van_eur;{bc['delta_van']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def728["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def728\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 19, ui_keys
        demo_keys = set(_F["mh728_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh728_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh728_demo():")
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
        ui_keys = set(re.findall(r'_def728\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W729 (26/10/2026) - tab728' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh728_num", "mh728_nneg", "mh728_pos",
                     "mh728_int_pos", "mh728_frac_01",
                     "mh728_frac_01_incl", "mh728_frac_toll",
                     "mh728_e_utile", "mh728_e_scaricata",
                     "mh728_e_caricata", "mh728_costo_carica",
                     "mh728_ricavo_scarica", "mh728_om",
                     "mh728_capex", "mh728_anni_effettivi",
                     "mh728_netto", "mh728_flussi",
                     "mh728_van_flussi", "mh728_tir_flussi",
                     "mh728_payback_flussi", "mh728_lcos",
                     "mh728_verdetto", "mh728_ramo",
                     "mh728_valida", "_mh728_neutro",
                     "mh728_calcola", "mh728_confronto",
                     "mh728_csv", "mh728_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_nessun_identificatore_futura_tab(self):
        assert "mh729" not in _helpers_src()
        assert "mh729" not in _ui_src()
        assert "st729" not in _ui_src()
        assert "tab729" not in _ui_src()

    def test_helpers_parse_ast(self):
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w729_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE728) == 1

    def test_blocco_with_tab728(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab728:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE728

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st728_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 22, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st728_") for k in keys)

    def test_chiavi_st_input_presenti(self):
        keys = re.findall(r'key="(st728_[a-z0-9_]+)"', _ui_src())
        attese = ["st728_pot", "st728_capacita",
                  "st728_dod", "st728_cicli",
                  "st728_rte_zn", "st728_om_zn",
                  "st728_capex_kw_zn", "st728_capex_kwh_zn",
                  "st728_vita_cicli_zn",
                  "st728_rte_lfp", "st728_om_lfp",
                  "st728_capex_kw_lfp", "st728_capex_kwh_lfp",
                  "st728_vita_cicli_lfp",
                  "st728_prezzo_carica", "st728_prezzo_scarica",
                  "st728_vita", "st728_wacc",
                  "st728_tolleranza", "st728_calcola"]
        assert len(attese) == 20
        for k in attese:
            assert k in keys, k

    def test_chiavi_st_niente_fstring_dinamiche(self):
        src = _ui_src()
        assert 'key=f"' not in src
        assert "key=f'" not in src

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg728" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg728") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg728")
        assert g < src.index("st.bar_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_sei_kpi_presenti(self):
        src = _ui_src()
        assert "VAN zinco-aria (EUR)" in src
        assert "TIR zinco-aria (%)" in src
        assert "Payback zinco-aria (anni)" in src
        assert "LCOS zinco-aria (EUR/MWh)" in src
        assert "VAN LFP (EUR)" in src
        assert "Delta VAN (EUR)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_distinzioni_presenti(self):
        src = _ui_src()
        assert "ferro-aria" in src
        assert "sodio-ione" in src
        assert "flusso redox" in src
        assert "LAES" in src
        assert "CAES" in src
        assert "tab717" in src

    def test_distinzioni_in_header_helpers(self):
        src = _helpers_src()
        assert "tab717" in src
        assert "sodio-ione" in src
        assert "flusso redox" in src
        assert "LAES" in src
        assert "CAES" in src

    def test_nota_didattica_presente(self):
        src = _ui_src()
        assert "NOTA DIDATTICA" in src
        assert "7200" in src
        assert "1.800.000" in src

    def test_grafico_bar_chart_presente(self):
        src = _ui_src()
        assert "st.bar_chart" in src
        assert "_dati728" in src
        assert '"Zinco-aria"' in src
        assert '"LFP"' in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh728_csv" in src
        assert "zinco_aria_contro_lfp.csv" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st728_show_flussi" in src
        assert "st.checkbox" in src

    def test_niente_em_dash_e_niente_nome(self):
        assert "—" not in _helpers_src()
        assert "—" not in _ui_src()
        assert "Emanuele" not in _helpers_src()
        assert "Emanuele" not in _ui_src()

    def test_ancora_helper_presente(self):
        assert "# W729 (26/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab728:")
