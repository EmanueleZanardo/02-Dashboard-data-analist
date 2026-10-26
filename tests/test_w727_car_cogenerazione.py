"""Test tab727 "⚡🔥 Cogenerazione CAR: il risparmio di energia primaria paga i certificati?"

Nuova tab tab727 (cogenerazione CAR, w728).
Business case di un impianto di
cogenerazione ad alto rendimento (CAR)
con certificati bianchi: PES = 1 - 1 /
(eta_el / eta_el_ref + eta_th / eta_th_ref);
soglia CAR PES >= 10 % sopra 1.000 kW,
PES > 0 sotto 1.000 kW; certificati =
energia primaria risparmiata / 11,63
MWh/tep, zero se non CAR; margine annuo
piatto, VAN, TIR, payback, verdetto.

Demo calcolata eseguendo demo_calcoli() (e
ricontrollata a mano, riga per riga):
potenza elettrica 500 kW; ore annue 6000;
rendimento elettrico 0,38; rendimento
termico 0,47; riferimento elettrico 0,525;
riferimento termico 0,90; prezzo gas 45
EUR/MWh; prezzo elettricita' 130 EUR/MWh;
prezzo calore evitato 55 EUR/MWh; prezzo
certificato 250 EUR/cert; costo O&M 12
EUR/MWh; CAPEX specifico 1400 EUR/kW;
vita 12 anni; WACC 0,06 (6 %); tolleranza
0,10 (10 % del CAPEX).

- e_mwh = 3000.0
- f_mwh = 7894.736842105263
- q_mwh = 3710.5263157894738
- f_sep_mwh = 9837.092731829573
- pes = 0.197452229299363
- soglia_car = 0.0
- car = True
- ep_risp_mwh = 1942.3558897243092
- n_cert = 167.01254425832408
- costo_gas_eur_anno = 355263.15789473685
- ricavo_el_eur_anno = 390000.0
- ricavo_cal_eur_anno = 204078.94736842107
- ricavo_cert_eur_anno = 41753.13606458102
- costo_om_eur_anno = 36000.0
- margine_eur_anno = 244568.92553826526
- capex_eur = 700000.0
- van = 1350427.7043800438
- tir = 33.88521571986842
- payback = 3
- verdetto = 'CONVIENTE'

Scomposizione: E 500 x 6000 / 1000 = 3000,0
MWh/anno; F 3000,0 / 0,38 = 7894,736842105263
MWh/anno; Q 7894,736842105263 x 0,47 =
3710,5263157894738 MWh/anno; F_sep 3000,0 /
0,525 + 3710,5263157894738 / 0,90 =
9837,092731829573 MWh/anno; PES 1 -
7894,736842105263 / 9837,092731829573 =
0,197452229299363 (19,75 %); sotto 1000 kW
la soglia CAR e' 0,0, quindi CAR = True;
EP_risp 9837,092731829573 - 7894,736842105263
= 1942,3558897243092 MWh/anno; certificati
1942,3558897243092 / 11,63 =
167,01254425832408 cert/anno; costo gas
7894,736842105263 x 45 = 355263,15789473685
EUR/anno; ricavo elettricita' 3000,0 x 130 =
390000,0 EUR/anno; ricavo calore
3710,5263157894738 x 55 = 204078,94736842107
EUR/anno; ricavo certificati
167,01254425832408 x 250 = 41753,13606458102
EUR/anno; O&M 3000,0 x 12 = 36000,0
EUR/anno; margine 390000,0 + 204078,94736842107
+ 41753,13606458102 - 355263,15789473685 -
36000,0 = 244568,92553826526 EUR/anno;
CAPEX 500 x 1400 = 700000,0 EUR; flussi:
anno 0 -700000,0, anni 1-12 margine
244568,92553826526 (piatti); VAN
1350427,7043800438 a WACC 6 % su 12 anni;
TIR 33,88521571986842 % (il tasso che azzera
il VAN dei flussi sopra); payback 3 (il
cumulato diventa positivo all'anno 3:
-700000,0 + 2 x 244568,92553826526 =
-210862,14892346948 all'anno 2, poi +
244568,92553826526 = 33706,77661479578
all'anno 3); VAN >= 0 -> CONVIENTE.
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
    if (p / "w728_ui.py").exists():
        return p
    return Path.home() / "workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features/hidden_files"


def _load(*names):
    """Carica le funzioni pure da w728_helpers.py via AST
    (niente Streamlit)."""
    src = (_new_dir() / "w728_helpers.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    ns = {}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, str(_new_dir() / "w728_helpers.py"),
                         "exec"), ns)
            out[node.name] = ns[node.name]
    missing = [n for n in names if n not in out]
    if missing:
        raise AssertionError(
            f"funzioni non trovate in w728_helpers.py: {missing}")
    return out


_F = _load("mh727_num", "mh727_nneg", "mh727_pos",
           "mh727_int_pos", "mh727_frac_01",
           "mh727_frac_01_incl", "mh727_energia_el",
           "mh727_combustibile", "mh727_calore",
           "mh727_primaria_separata", "mh727_pes",
           "mh727_soglia_car", "mh727_is_car",
           "mh727_certificati", "mh727_costo_gas",
           "mh727_ricavo", "mh727_ricavo_cert",
           "mh727_costo_om", "mh727_margine",
           "mh727_capex", "mh727_flussi",
           "mh727_van_flussi", "mh727_tir_flussi",
           "mh727_payback_flussi", "mh727_verdetto",
           "mh727_confronto", "mh727_valida",
           "_mh727_neutro", "mh727_calcola",
           "mh727_sensitivita", "mh727_csv",
           "mh727_demo", "demo_calcoli")

TITLE727 = ("⚡🔥 Cogenerazione CAR: il risparmio "
            "di energia primaria paga i certificati?")

E_DEMO = 3000.0
F_DEMO = 7894.736842105263
Q_DEMO = 3710.5263157894738
FSEP_DEMO = 9837.092731829573
PES_DEMO = 0.197452229299363
SOGLIA_DEMO = 0.0
EPRISP_DEMO = 1942.3558897243092
NCERT_DEMO = 167.01254425832408
CGAS_DEMO = 355263.15789473685
REL_DEMO = 390000.0
RCAL_DEMO = 204078.94736842107
RCERT_DEMO = 41753.13606458102
COM_DEMO = 36000.0
MARG_DEMO = 244568.92553826526
CAPEX_DEMO = 700000.0
VAN_DEMO = 1350427.7043800438
TIR_DEMO = 33.88521571986842
PAYBACK_DEMO = 3
VITA_DEMO = 12
VERDETTO_DEMO = "CONVIENTE"

REL = 1e-9


def _helpers_src():
    return (_new_dir() / "w728_helpers.py").read_text(encoding="utf-8")


def _ui_src():
    return (_new_dir() / "w728_ui.py").read_text(encoding="utf-8")


class TestValidazione:
    def _val(self, **kw):
        d = _F["mh727_demo"]()
        d.update(kw)
        return _F["mh727_valida"](**d)

    def test_num_rifiuta_bool(self):
        with pytest.raises(ValueError):
            _F["mh727_num"](True, "x")

    def test_num_rifiuta_stringa(self):
        with pytest.raises(ValueError):
            _F["mh727_num"]("2.5", "x")

    def test_num_rifiuta_nan(self):
        with pytest.raises(ValueError):
            _F["mh727_num"](float("nan"), "x")

    def test_num_rifiuta_infinito(self):
        with pytest.raises(ValueError):
            _F["mh727_num"](float("inf"), "x")

    def test_nneg_rifiuta_negativo(self):
        with pytest.raises(ValueError):
            _F["mh727_nneg"](-0.1, "x")

    def test_nneg_accetta_zero(self):
        assert _F["mh727_nneg"](0.0, "x") == 0.0

    def test_pos_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh727_pos"](0.0, "x")

    def test_int_pos_rifiuta_frazione(self):
        with pytest.raises(ValueError):
            _F["mh727_int_pos"](2.5, "x")

    def test_int_pos_accetta_float_intero(self):
        assert _F["mh727_int_pos"](12.0, "x") == 12

    def test_frac_01_rifiuta_zero_e_uno(self):
        with pytest.raises(ValueError):
            _F["mh727_frac_01"](0.0, "x")
        with pytest.raises(ValueError):
            _F["mh727_frac_01"](1.0, "x")

    def test_frac_01_accetta_interno(self):
        assert _F["mh727_frac_01"](0.38, "x") == 0.38

    def test_frac_01_incl_accetta_uno(self):
        assert _F["mh727_frac_01_incl"](1.0, "x") == 1.0

    def test_frac_01_incl_rifiuta_zero(self):
        with pytest.raises(ValueError):
            _F["mh727_frac_01_incl"](0.0, "x")

    def test_demo_valida(self):
        v = self._val()
        assert v["valido"] is True
        assert v["errore"] == ""

    def test_pot_zero_non_valida(self):
        assert self._val(pot_el_kw=0.0)["valido"] is False

    def test_ore_zero_non_valide(self):
        assert self._val(ore_anno=0.0)["valido"] is False

    def test_rendimenti_fuori_intervallo_non_validi(self):
        assert self._val(eta_el=0.0)["valido"] is False
        assert self._val(eta_el=1.0)["valido"] is False
        assert self._val(eta_th=0.0)["valido"] is False
        assert self._val(eta_th=1.0)["valido"] is False
        assert self._val(eta_el_ref=0.0)["valido"] is False
        assert self._val(eta_th_ref=0.0)["valido"] is False

    def test_riferimento_uno_valido(self):
        assert self._val(eta_el_ref=1.0)["valido"] is True
        assert self._val(eta_th_ref=1.0)["valido"] is True

    def test_somma_rendimenti_uguale_uno_non_valida(self):
        assert self._val(eta_el=0.5, eta_th=0.5)["valido"] is False

    def test_somma_rendimenti_sopra_uno_non_valida(self):
        assert self._val(eta_el=0.6, eta_th=0.5)["valido"] is False

    def test_somma_rendimenti_sotto_uno_valida(self):
        assert self._val(eta_el=0.5, eta_th=0.49)["valido"] is True

    def test_negativi_non_validi(self):
        for k in ("prezzo_gas_eur_mwh",
                  "prezzo_el_eur_mwh",
                  "prezzo_cal_eur_mwh",
                  "prezzo_cert_eur",
                  "costo_om_eur_mwh",
                  "capex_spec_eur_kw",
                  "wacc_frac", "tolleranza_frac"):
            assert self._val(**{k: -0.01})["valido"] is False, k

    def test_vita_zero_non_valida(self):
        assert self._val(vita_anni=0)["valido"] is False

    def test_vita_non_intera_non_valida(self):
        assert self._val(vita_anni=12.5)["valido"] is False

    def test_tolleranza_sopra_uno_valida_brief(self):
        assert self._val(tolleranza_frac=1.5)["valido"] is True

    def test_wacc_senza_tetto_superiore(self):
        assert self._val(wacc_frac=1.5)["valido"] is True

    def test_nan_non_valido(self):
        assert self._val(pot_el_kw=float("nan"))["valido"] is False

    def test_inf_non_valido(self):
        assert self._val(pot_el_kw=float("inf"))["valido"] is False

    def test_bool_non_valido(self):
        assert self._val(vita_anni=True)["valido"] is False

    def test_stringa_non_valida_senza_eccezioni(self):
        v = self._val(pot_el_kw="500")
        assert v["valido"] is False
        assert v["errore"] != ""

    def test_zeri_ammessi_in_validazione(self):
        assert self._val(prezzo_gas_eur_mwh=0.0)["valido"] is True
        assert self._val(prezzo_el_eur_mwh=0.0)["valido"] is True
        assert self._val(prezzo_cal_eur_mwh=0.0)["valido"] is True
        assert self._val(prezzo_cert_eur=0.0)["valido"] is True
        assert self._val(costo_om_eur_mwh=0.0)["valido"] is True
        assert self._val(capex_spec_eur_kw=0.0)["valido"] is True
        assert self._val(wacc_frac=0.0)["valido"] is True
        assert self._val(tolleranza_frac=0.0)["valido"] is True


class TestFunzioni:
    def test_energia_el_demo(self):
        assert _F["mh727_energia_el"](
            500.0, 6000.0) == pytest.approx(
            E_DEMO, rel=REL)

    def test_combustibile_demo(self):
        assert _F["mh727_combustibile"](
            E_DEMO, 0.38) == pytest.approx(
            F_DEMO, rel=REL)

    def test_calore_demo(self):
        assert _F["mh727_calore"](
            F_DEMO, 0.47) == pytest.approx(
            Q_DEMO, rel=REL)

    def test_primaria_separata_demo(self):
        assert _F["mh727_primaria_separata"](
            E_DEMO, Q_DEMO, 0.525, 0.90) == pytest.approx(
            FSEP_DEMO, rel=REL)

    def test_pes_demo(self):
        assert _F["mh727_pes"](
            0.38, 0.47, 0.525, 0.90) == pytest.approx(
            PES_DEMO, rel=REL)

    def test_pes_uguale_uno_meno_f_su_fsep(self):
        pes = _F["mh727_pes"](0.38, 0.47, 0.525, 0.90)
        assert pes == pytest.approx(
            1.0 - F_DEMO / FSEP_DEMO, rel=1e-12)

    def test_pes_scenario_basso(self):
        assert _F["mh727_pes"](
            0.30, 0.40, 0.525, 0.90) == pytest.approx(
            0.015625, rel=REL)

    def test_soglia_car_sotto_1000(self):
        assert _F["mh727_soglia_car"](500.0) == 0.0
        assert _F["mh727_soglia_car"](999.0) == 0.0

    def test_soglia_car_sopra_1000(self):
        assert _F["mh727_soglia_car"](1000.0) == 0.10
        assert _F["mh727_soglia_car"](2000.0) == 0.10

    def test_is_car_piccola_pes_positivo(self):
        assert _F["mh727_is_car"](0.015625, 500.0) is True

    def test_is_car_piccola_pes_zero_no(self):
        assert _F["mh727_is_car"](0.0, 500.0) is False

    def test_is_car_piccola_pes_negativo_no(self):
        assert _F["mh727_is_car"](-0.05, 500.0) is False

    def test_is_car_grande_soglia_10(self):
        assert _F["mh727_is_car"](0.10, 1000.0) is True
        assert _F["mh727_is_car"](0.099, 1000.0) is False
        assert _F["mh727_is_car"](0.015625, 2000.0) is False

    def test_certificati_demo(self):
        assert _F["mh727_certificati"](
            EPRISP_DEMO, True) == pytest.approx(
            NCERT_DEMO, rel=REL)

    def test_certificati_zero_se_non_car(self):
        assert _F["mh727_certificati"](
            EPRISP_DEMO, False) == 0.0
        assert _F["mh727_certificati"](
            634.9206349206361, False) == 0.0

    def test_certificati_zero_se_risparmio_non_positivo(self):
        assert _F["mh727_certificati"](0.0, True) == 0.0
        assert _F["mh727_certificati"](-100.0, True) == 0.0

    def test_certificati_fattore_tep(self):
        assert _F["mh727_certificati"](
            11.63, True) == pytest.approx(1.0, rel=REL)

    def test_costo_gas_demo(self):
        assert _F["mh727_costo_gas"](
            F_DEMO, 45.0) == pytest.approx(
            CGAS_DEMO, rel=REL)

    def test_ricavo_el_demo(self):
        assert _F["mh727_ricavo"](
            E_DEMO, 130.0) == pytest.approx(
            REL_DEMO, rel=REL)

    def test_ricavo_cal_demo(self):
        assert _F["mh727_ricavo"](
            Q_DEMO, 55.0) == pytest.approx(
            RCAL_DEMO, rel=REL)

    def test_ricavo_cert_demo(self):
        assert _F["mh727_ricavo_cert"](
            NCERT_DEMO, 250.0) == pytest.approx(
            RCERT_DEMO, rel=REL)

    def test_costo_om_demo(self):
        assert _F["mh727_costo_om"](
            E_DEMO, 12.0) == pytest.approx(
            COM_DEMO, rel=REL)

    def test_margine_demo(self):
        assert _F["mh727_margine"](
            REL_DEMO, RCAL_DEMO, RCERT_DEMO,
            CGAS_DEMO, COM_DEMO) == pytest.approx(
            MARG_DEMO, rel=REL)

    def test_margine_puo_essere_negativo(self):
        assert _F["mh727_margine"](
            100000.0, 50000.0, 0.0,
            200000.0, 10000.0) == pytest.approx(
            -60000.0, rel=REL)

    def test_capex_demo(self):
        assert _F["mh727_capex"](
            500.0, 1400.0) == pytest.approx(
            CAPEX_DEMO, rel=REL)

    def test_flussi_demo(self):
        flussi = _F["mh727_flussi"](CAPEX_DEMO, MARG_DEMO,
                                     VITA_DEMO)
        assert len(flussi) == VITA_DEMO + 1
        assert flussi[0] == pytest.approx(-CAPEX_DEMO, rel=REL)
        assert all(f == pytest.approx(MARG_DEMO, rel=REL)
                   for f in flussi[1:])

    def test_van_flussi_demo(self):
        flussi = _F["mh727_flussi"](CAPEX_DEMO, MARG_DEMO,
                                     VITA_DEMO)
        assert abs(_F["mh727_van_flussi"](
            flussi, 0.06) - VAN_DEMO) <= 1.0

    def test_van_flussi_tasso_zero(self):
        flussi = _F["mh727_flussi"](CAPEX_DEMO, MARG_DEMO,
                                     VITA_DEMO)
        atteso = -CAPEX_DEMO + MARG_DEMO * VITA_DEMO
        assert _F["mh727_van_flussi"](
            flussi, 0.0) == pytest.approx(atteso, rel=1e-12)

    def test_van_flussi_rifiuta_tasso_negativo(self):
        with pytest.raises(ValueError):
            _F["mh727_van_flussi"]([100.0, 100.0], -0.01)

    def test_tir_demo(self):
        flussi = _F["mh727_flussi"](CAPEX_DEMO, MARG_DEMO,
                                     VITA_DEMO)
        tir = _F["mh727_tir_flussi"](flussi)
        assert tir is not None
        assert tir * 100.0 == pytest.approx(TIR_DEMO, rel=1e-9)

    def test_tir_none_tutti_flussi_non_negativi(self):
        assert _F["mh727_tir_flussi"](
            [0.0] + [MARG_DEMO] * 12) is None

    def test_tir_none_nessun_cambio_segno_negativo(self):
        assert _F["mh727_tir_flussi"](
            [-1000.0] + [-100.0] * 10) is None

    def test_tir_esiste_caso_semplice(self):
        assert _F["mh727_tir_flussi"]([-100.0, 120.0]) == pytest.approx(
            0.2, rel=1e-9)

    def test_payback_demo_tre(self):
        flussi = _F["mh727_flussi"](CAPEX_DEMO, MARG_DEMO,
                                     VITA_DEMO)
        assert _F["mh727_payback_flussi"](flussi) == PAYBACK_DEMO

    def test_payback_none_se_mai(self):
        assert _F["mh727_payback_flussi"](
            [-10000000.0] + [MARG_DEMO] * 12) is None

    def test_payback_zero_se_cumulato_anno_zero_non_negativo(self):
        assert _F["mh727_payback_flussi"](
            [0.0] + [MARG_DEMO] * 12) == 0

    def test_verdetto_conviente_demo(self):
        assert _F["mh727_verdetto"](
            VAN_DEMO, CAPEX_DEMO, 0.10,
            MARG_DEMO) == VERDETTO_DEMO

    def test_verdetto_van_zero_conviente(self):
        assert _F["mh727_verdetto"](
            0.0, CAPEX_DEMO, 0.10, MARG_DEMO) == "CONVIENTE"

    def test_verdetto_marginale_ad_hoc(self):
        assert _F["mh727_verdetto"](
            -100.0, CAPEX_DEMO, 0.10,
            MARG_DEMO) == "MARGINALE"

    def test_verdetto_marginale_al_limite(self):
        assert _F["mh727_verdetto"](
            -0.10 * CAPEX_DEMO, CAPEX_DEMO, 0.10,
            MARG_DEMO) == "MARGINALE"

    def test_verdetto_non_conviente_oltre_limite(self):
        assert _F["mh727_verdetto"](
            -0.10 * CAPEX_DEMO - 1.0, CAPEX_DEMO, 0.10,
            MARG_DEMO) == "NON_CONVIENTE"

    def test_verdetto_non_calcolabile_marg_non_positivo(self):
        assert _F["mh727_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, 0.0) == "NON_CALCOLABILE"
        assert _F["mh727_verdetto"](
            1000.0, CAPEX_DEMO, 0.10, -50.0) == "NON_CALCOLABILE"

    def test_verdetto_capex_zero_van_positivo_conviente(self):
        assert _F["mh727_verdetto"](
            1000.0, 0.0, 0.10, MARG_DEMO) == "CONVIENTE"

    def test_verdetto_capex_zero_van_negativo_non_conviente(self):
        assert _F["mh727_verdetto"](
            -1.0, 0.0, 0.10, MARG_DEMO) == "NON_CONVIENTE"

    def test_verdetto_capex_zero_mai_marginale(self):
        for van in (-1.0, -100.0, -1000000.0):
            assert _F["mh727_verdetto"](
                van, 0.0, 0.10, MARG_DEMO) == "NON_CONVIENTE"

    def test_verdetto_capex_negativo_mai_marginale(self):
        assert _F["mh727_verdetto"](
            -1.0, -20000.0, 0.10, MARG_DEMO) == "NON_CONVIENTE"

    def test_verdetto_rifiuta_tolleranza_negativa(self):
        with pytest.raises(ValueError):
            _F["mh727_verdetto"](100.0, CAPEX_DEMO, -0.01,
                                 MARG_DEMO)

    def test_confronto_demo(self):
        df = _F["mh727_confronto"](
            E_DEMO, Q_DEMO, F_DEMO, FSEP_DEMO,
            EPRISP_DEMO, CGAS_DEMO, REL_DEMO,
            RCAL_DEMO, RCERT_DEMO, COM_DEMO, MARG_DEMO)
        assert list(df.columns) == ["Voce", "Produzione separata",
                                    "Cogenerazione", "Differenza"]
        assert len(df) == 9
        voci = df["Voce"].tolist()
        assert "Energia primaria (MWh/anno)" in voci
        assert "Ricavo certificati CAR (EUR/anno)" in voci
        assert "Margine annuo (EUR/anno)" in voci
        riga_prim = df[df["Voce"] == "Energia primaria (MWh/anno)"].iloc[0]
        assert riga_prim["Produzione separata"] == pytest.approx(
            FSEP_DEMO, rel=REL)
        assert riga_prim["Cogenerazione"] == pytest.approx(
            F_DEMO, rel=REL)
        assert riga_prim["Differenza"] == pytest.approx(
            EPRISP_DEMO, rel=REL)
        riga_cert = df[df["Voce"] == "Ricavo certificati CAR (EUR/anno)"].iloc[0]
        assert riga_cert["Produzione separata"] == pytest.approx(
            0.0, abs=1e-9)
        assert riga_cert["Cogenerazione"] == pytest.approx(
            RCERT_DEMO, rel=REL)
        riga_marg = df[df["Voce"] == "Margine annuo (EUR/anno)"].iloc[0]
        assert riga_marg["Cogenerazione"] == pytest.approx(
            MARG_DEMO, rel=REL)


class TestDemo:
    def _bc(self, **kw):
        d = _F["mh727_demo"]()
        d.update(kw)
        return _F["mh727_calcola"](**d)

    def test_demo_calcoli_end_to_end(self):
        c = _F["demo_calcoli"]()
        assert c["valid"] is True
        assert c["errore"] == ""
        assert c["e_mwh"] == pytest.approx(E_DEMO, rel=REL)
        assert c["f_mwh"] == pytest.approx(F_DEMO, rel=REL)
        assert c["q_mwh"] == pytest.approx(Q_DEMO, rel=REL)
        assert c["f_sep_mwh"] == pytest.approx(FSEP_DEMO, rel=REL)
        assert c["pes"] == pytest.approx(PES_DEMO, rel=REL)
        assert c["soglia_car"] == pytest.approx(SOGLIA_DEMO, abs=1e-9)
        assert c["car"] is True
        assert c["ep_risp_mwh"] == pytest.approx(EPRISP_DEMO, rel=REL)
        assert c["n_cert"] == pytest.approx(NCERT_DEMO, rel=REL)
        assert c["costo_gas_eur_anno"] == pytest.approx(
            CGAS_DEMO, rel=REL)
        assert c["ricavo_el_eur_anno"] == pytest.approx(
            REL_DEMO, rel=REL)
        assert c["ricavo_cal_eur_anno"] == pytest.approx(
            RCAL_DEMO, rel=REL)
        assert c["ricavo_cert_eur_anno"] == pytest.approx(
            RCERT_DEMO, rel=REL)
        assert c["costo_om_eur_anno"] == pytest.approx(
            COM_DEMO, rel=REL)
        assert c["margine_eur_anno"] == pytest.approx(
            MARG_DEMO, rel=REL)
        assert c["capex_eur"] == pytest.approx(CAPEX_DEMO, rel=REL)
        assert abs(c["van"] - VAN_DEMO) <= 1.0
        assert abs(c["tir"] - TIR_DEMO) <= 0.01
        assert c["payback"] == PAYBACK_DEMO
        assert c["verdetto"] == VERDETTO_DEMO
        assert c["flussi"][0] == pytest.approx(-CAPEX_DEMO, rel=REL)
        assert all(f == pytest.approx(MARG_DEMO, rel=REL)
                   for f in c["flussi"][1:])
        assert len(c["flussi"]) == VITA_DEMO + 1

    def test_demo_calcoli_deterministico(self):
        assert _F["demo_calcoli"]()[
            "van"] == _F["demo_calcoli"]()["van"]
        assert _F["demo_calcoli"]()[
            "margine_eur_anno"] == _F["demo_calcoli"]()[
            "margine_eur_anno"]

    def test_demo_inputs_ricostruiscono_demo_calcoli(self):
        d = _F["mh727_demo"]()
        b = _F["mh727_calcola"](**d)
        coppie = [("e_mwh", E_DEMO),
                  ("f_mwh", F_DEMO),
                  ("q_mwh", Q_DEMO),
                  ("f_sep_mwh", FSEP_DEMO),
                  ("pes", PES_DEMO),
                  ("ep_risp_mwh", EPRISP_DEMO),
                  ("n_cert", NCERT_DEMO),
                  ("costo_gas_eur_anno", CGAS_DEMO),
                  ("ricavo_el_eur_anno", REL_DEMO),
                  ("ricavo_cal_eur_anno", RCAL_DEMO),
                  ("ricavo_cert_eur_anno", RCERT_DEMO),
                  ("costo_om_eur_anno", COM_DEMO),
                  ("margine_eur_anno", MARG_DEMO),
                  ("capex_eur", CAPEX_DEMO)]
        for chiave, atteso in coppie:
            assert b[chiave] == pytest.approx(atteso,
                                              rel=REL), chiave
        assert abs(b["van"] - VAN_DEMO) <= 1.0
        assert abs(b["tir"] - TIR_DEMO) <= 0.01
        assert b["payback"] == PAYBACK_DEMO
        assert b["verdetto"] == VERDETTO_DEMO
        assert b["car"] is True

    def test_demo_defaults(self):
        d = _F["mh727_demo"]()
        assert d["pot_el_kw"] == 500.0
        assert d["ore_anno"] == 6000.0
        assert d["eta_el"] == 0.38
        assert d["eta_th"] == 0.47
        assert d["eta_el_ref"] == 0.525
        assert d["eta_th_ref"] == 0.90
        assert d["prezzo_gas_eur_mwh"] == 45.0
        assert d["prezzo_el_eur_mwh"] == 130.0
        assert d["prezzo_cal_eur_mwh"] == 55.0
        assert d["prezzo_cert_eur"] == 250.0
        assert d["costo_om_eur_mwh"] == 12.0
        assert d["capex_spec_eur_kw"] == 1400.0
        assert d["vita_anni"] == 12
        assert d["wacc_frac"] == 0.06
        assert d["tolleranza_frac"] == 0.10
        assert len(d) == 15

    def test_docstring_riporta_repr_demo_calcoli(self):
        """I numeri nel docstring devono matchare
        demo_calcoli() entro 1e-9 relativo: confronto
        automatico dei repr contro la demo eseguita."""
        c = _F["demo_calcoli"]()
        doc = __doc__
        for chiave in ("e_mwh", "f_mwh", "q_mwh",
                       "f_sep_mwh", "pes", "ep_risp_mwh",
                       "n_cert", "costo_gas_eur_anno",
                       "ricavo_el_eur_anno",
                       "ricavo_cal_eur_anno",
                       "ricavo_cert_eur_anno",
                       "costo_om_eur_anno",
                       "margine_eur_anno", "capex_eur",
                       "van"):
            assert repr(c[chiave]) in doc, chiave
        assert f"tir = {repr(c['tir'])}" in doc
        assert "payback = 3" in doc
        assert "verdetto = 'CONVIENTE'" in doc
        assert "car = True" in doc

    def test_non_car_2000kw_pes_basso(self):
        # 2000 kW, rendimenti 0,30 / 0,40: PES
        # 1,56 % < 10 % -> NON CAR, certificati
        # zero anche con EP_risp positiva
        # (634,92 MWh/anno), margine 496000
        # senza ricavi da certificati, VAN
        # 1358386,59, TIR 14,06 %, payback 6.
        n = self._bc(pot_el_kw=2000.0, eta_el=0.30,
                     eta_th=0.40)
        assert n["valid"] is True
        assert n["car"] is False
        assert n["pes"] == pytest.approx(0.015625, rel=REL)
        assert n["soglia_car"] == pytest.approx(0.10, rel=REL)
        assert n["ep_risp_mwh"] == pytest.approx(
            634.9206349206361, rel=REL)
        assert n["n_cert"] == pytest.approx(0.0, abs=1e-9)
        assert n["ricavo_cert_eur_anno"] == pytest.approx(
            0.0, abs=1e-9)
        assert n["margine_eur_anno"] == pytest.approx(
            496000.0, rel=REL)
        assert abs(n["van"] - 1358386.5944301249) <= 1.0
        assert abs(n["tir"] - 14.061083229345444) <= 0.01
        assert n["payback"] == 6
        assert n["verdetto"] == "CONVIENTE"

    def test_piccola_pes_positivo_car(self):
        # Stessi rendimenti bassi ma 500 kW:
        # PES 1,56 % > 0 -> CAR (piccola
        # cogenerazione), certificati positivi.
        n = self._bc(eta_el=0.30, eta_th=0.40)
        assert n["valid"] is True
        assert n["car"] is True
        assert n["pes"] == pytest.approx(0.015625, rel=REL)
        assert n["soglia_car"] == pytest.approx(0.0, abs=1e-9)
        assert n["n_cert"] > 0.0

    def test_capex_4300_marginale(self):
        # CAPEX specifico 4300: CAPEX 2150000,
        # VAN -99572,30, TIR 5,15 %, payback 9
        # -> MARGINALE (|VAN| <= 10 % di
        # 2150000 = 215000).
        n = self._bc(capex_spec_eur_kw=4300.0)
        assert n["valid"] is True
        assert n["capex_eur"] == pytest.approx(
            2150000.0, rel=REL)
        assert abs(n["van"] - (-99572.29561995617)) <= 1.0
        assert abs(n["tir"] - 5.145474988580132) <= 0.01
        assert n["payback"] == 9
        assert n["verdetto"] == "MARGINALE"

    def test_capex_5000_non_conviente(self):
        # CAPEX specifico 5000: CAPEX 2500000,
        # VAN -449572,30, TIR 2,56 %, payback 11
        # -> NON_CONVIENTE (|VAN| > 10 % di
        # 2500000 = 250000).
        n = self._bc(capex_spec_eur_kw=5000.0)
        assert n["valid"] is True
        assert abs(n["van"] - (-449572.2956199562)) <= 1.0
        assert abs(n["tir"] - 2.557622907556546) <= 0.01
        assert n["payback"] == 11
        assert n["verdetto"] == "NON_CONVIENTE"

    def test_gas_100_marg_negativo_neutro(self):
        # Prezzo gas 100: costo gas 789473,68 >
        # ricavi -> margine negativo -> neutro.
        n = self._bc(prezzo_gas_eur_mwh=100.0)
        assert n["valid"] is False
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["margine_eur_anno"] == 0.0
        assert n["tir"] is None
        assert n["payback"] is None

    def test_capex_zero_tir_none_payback_zero(self):
        # CAPEX specifico 0: tutti i flussi >= 0
        # -> TIR None, payback 0, VAN 2050427,70
        # -> CONVIENTE.
        n = self._bc(capex_spec_eur_kw=0.0)
        assert n["valid"] is True
        assert n["capex_eur"] == pytest.approx(0.0, abs=1e-9)
        assert n["tir"] is None
        assert n["payback"] == 0
        assert abs(n["van"] - 2050427.7043800435) <= 1.0
        assert n["verdetto"] == "CONVIENTE"

    def test_pot_zero_neutro(self):
        n = self._bc(pot_el_kw=0.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_rendimenti_somma_uno_neutro(self):
        n = self._bc(eta_el=0.5, eta_th=0.5)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_rendimento_uno_neutro(self):
        n = self._bc(eta_el=1.0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_vita_zero_neutro(self):
        n = self._bc(vita_anni=0)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_negativo_neutro(self):
        n = self._bc(wacc_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_tolleranza_negativa_neutro(self):
        n = self._bc(tolleranza_frac=-0.01)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_nan_neutro(self):
        n = self._bc(pot_el_kw=float("nan"))
        assert n["verdetto"] == "NON_CALCOLABILE"
        assert n["margine_eur_anno"] == 0.0

    def test_inf_neutro(self):
        n = self._bc(pot_el_kw=float("inf"))
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_bool_neutro(self):
        n = self._bc(vita_anni=True)
        assert n["verdetto"] == "NON_CALCOLABILE"

    def test_wacc_zero_calcolabile(self):
        # WACC 0: VAN = somma flussi =
        # -700000 + 244568,92553826526 x 12 =
        # 2234827,1064591827.
        n = self._bc(wacc_frac=0.0)
        assert n["van"] == pytest.approx(
            2234827.1064591827, rel=REL)
        assert n["verdetto"] == "CONVIENTE"

    def test_vita_8_calcolabile(self):
        # Vita 8 anni: VAN 818722,60, TIR
        # 30,88 %, payback 3 -> CONVIENTE.
        n = self._bc(vita_anni=8)
        assert n["valid"] is True
        assert abs(n["van"] - 818722.600162993) <= 1.0
        assert abs(n["tir"] - 30.880494878716547) <= 0.01
        assert n["payback"] == 3
        assert n["verdetto"] == "CONVIENTE"

    def test_dict_neutro_dataframe_colonne(self):
        n = _F["_mh727_neutro"]()
        assert n["valid"] is False
        assert n["errore"] == ""
        assert list(n["df_confronto"].columns) == [
            "Voce", "Produzione separata",
            "Cogenerazione", "Differenza"]
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
        assert n["car"] is False

    def test_dict_neutro_chiavi_complete(self):
        n = _F["_mh727_neutro"]("errore di prova")
        for chiave in ("valid", "errore",
                       "pot_el_kw", "ore_anno",
                       "eta_el", "eta_th",
                       "eta_el_ref", "eta_th_ref",
                       "prezzo_gas_eur_mwh",
                       "prezzo_el_eur_mwh",
                       "prezzo_cal_eur_mwh",
                       "prezzo_cert_eur",
                       "costo_om_eur_mwh",
                       "capex_spec_eur_kw",
                       "vita_anni", "wacc_frac",
                       "tolleranza_frac",
                       "e_mwh", "f_mwh", "q_mwh",
                       "f_sep_mwh", "pes",
                       "soglia_car", "car",
                       "ep_risp_mwh", "n_cert",
                       "costo_gas_eur_anno",
                       "ricavo_el_eur_anno",
                       "ricavo_cal_eur_anno",
                       "ricavo_cert_eur_anno",
                       "costo_om_eur_anno",
                       "margine_eur_anno",
                       "capex_eur", "flussi",
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
        assert len(b["df_tabella"]) == 32
        voci = b["df_tabella"]["Voce"].tolist()
        assert "Potenza elettrica (kW)" in voci
        assert "Energia elettrica (MWh/anno)" in voci
        assert "PES (frazione)" in voci
        assert "Certificati CAR (cert/anno)" in voci
        assert "Margine annuo (EUR/anno)" in voci
        assert "VAN (EUR)" in voci
        assert list(b["df_flussi"].columns) == ["Anno",
                                               "Flusso (€/anno)",
                                               "Cumulato (€)"]
        assert len(b["df_flussi"]) == VITA_DEMO + 1
        assert b["df_flussi"]["Flusso (€/anno)"].iloc[0] == \
            pytest.approx(-CAPEX_DEMO, rel=REL)
        assert b["df_flussi"]["Flusso (€/anno)"].iloc[1] == \
            pytest.approx(MARG_DEMO, rel=REL)
        assert b["df_flussi"]["Flusso (€/anno)"].iloc[12] == \
            pytest.approx(MARG_DEMO, rel=REL)
        assert list(b["df_confronto"].columns) == [
            "Voce", "Produzione separata",
            "Cogenerazione", "Differenza"]
        assert len(b["df_confronto"]) == 9


class TestSensitivita:
    def _ing(self):
        return _F["mh727_demo"]()

    def test_sensitivita_dimensioni(self):
        s = _F["mh727_sensitivita"](self._ing())
        assert s.shape == (3, 3)
        assert list(s.columns) == ["x0.9", "x1.0", "x1.1"]
        assert list(s.index) == ["x0.9", "x1.0", "x1.1"]

    def test_sensitivita_centro_uguale_van_demo(self):
        s = _F["mh727_sensitivita"](self._ing())
        assert abs(s.loc["x1.0", "x1.0"] - VAN_DEMO) <= 1.0

    def test_sensitivita_crescente_con_ore(self):
        s = _F["mh727_sensitivita"](self._ing())
        for riga in ("x0.9", "x1.0", "x1.1"):
            assert s.loc[riga, "x0.9"] < \
                s.loc[riga, "x1.0"] < \
                s.loc[riga, "x1.1"]

    def test_sensitivita_crescente_con_prezzo_cert(self):
        s = _F["mh727_sensitivita"](self._ing())
        for colonna in ("x0.9", "x1.0", "x1.1"):
            assert s.loc["x0.9", colonna] < \
                s.loc["x1.0", colonna] < \
                s.loc["x1.1", colonna]

    def test_sensitivita_nessuna_colonna_degenere(self):
        s = _F["mh727_sensitivita"](self._ing())
        assert (s.values != 0.0).all()

    def test_sensitivita_nessuna_colonna_costante(self):
        s = _F["mh727_sensitivita"](self._ing())
        for colonna in s.columns:
            assert len(set(s[colonna].tolist())) == 3
        for riga in s.index:
            assert len(set(s.loc[riga].tolist())) == 3

    def test_sensitivita_angoli(self):
        s = _F["mh727_sensitivita"](self._ing())
        assert abs(s.loc["x0.9", "x0.9"] - 1113880.274031205) <= 1.0
        assert abs(s.loc["x0.9", "x1.1"] - 1516964.7793714742) <= 1.0
        assert abs(s.loc["x1.1", "x0.9"] - 1176889.5938528723) <= 1.0
        assert abs(s.loc["x1.1", "x1.1"] - 1593976.1702646227) <= 1.0

    def test_sensitivita_centro_con_vita_corta(self):
        # Con vita 8 anni il centro deve
        # coincidere col VAN del caso con vita
        # 8 anni (flussi piatti, nessun altro
        # effetto).
        ing = self._ing()
        ing["vita_anni"] = 8
        s = _F["mh727_sensitivita"](ing)
        b = _F["mh727_calcola"](**ing)
        assert abs(s.loc["x1.0", "x1.0"] - b["van"]) <= 1.0


class TestCsv:
    def _ing(self):
        return _F["mh727_demo"]()

    def test_csv_separatore_punto_virgola(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh727_csv"](bc, self._ing())
        assert txt.startswith("voce;valore")
        assert txt.count(";") == 36

    def test_csv_contiene_verdetto_e_costi(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh727_csv"](bc, self._ing())
        assert "verdetto;CONVIENTE" in txt
        assert "margine_eur_anno" in txt
        assert "costo_gas_eur_anno" in txt
        assert "ricavo_cert_eur_anno" in txt
        assert "n_cert" in txt
        assert "pes" in txt
        assert "tir_pct" in txt
        assert "payback_anni" in txt
        assert "pot_el_kw" in txt
        assert "e_mwh" in txt
        assert "capex_eur" in txt
        assert "ep_risp_mwh" in txt

    def test_csv_valori_demo(self):
        bc = _F["demo_calcoli"]()
        txt = _F["mh727_csv"](bc, self._ing())
        assert f"margine_eur_anno;{bc['margine_eur_anno']}" in txt
        assert f"e_mwh;{bc['e_mwh']}" in txt
        assert "pot_el_kw;500.0" in txt
        assert "capex_spec_eur_kw;1400.0" in txt
        assert f"n_cert;{bc['n_cert']}" in txt


class TestDemoUiKeysRegression:
    def test_ui_keys_sottoinsieme_demo_keys(self):
        """Ogni chiave _def727["..."] usata in UI deve
        esistere nel demo dict (regressione tab675)."""
        ui_keys = set(re.findall(r'_def727\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert len(ui_keys) == 15, ui_keys
        demo_keys = set(_F["mh727_demo"]().keys())
        assert ui_keys <= demo_keys, ui_keys - demo_keys
        assert ui_keys == demo_keys, ui_keys ^ demo_keys

    def test_ui_keys_parser_conteggio_parentesi(self):
        """Verifica ui_keys ⊆ demo_keys col parser a
        conteggio parentesi sul corpo di mh727_demo
        (mai regex con graffa non-greedy sul dict demo)."""
        src = _helpers_src()
        start = src.index("def mh727_demo():")
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
        ui_keys = set(re.findall(r'_def727\["([A-Za-z0-9_]+)"\]',
                                 _ui_src()))
        assert ui_keys <= demo_keys, ui_keys - demo_keys


class TestStruttura:
    def test_header_helpers_presente(self):
        assert '# W728 (26/10/2026) - tab727' in _helpers_src()

    def test_helpers_definiti(self):
        src = _helpers_src()
        for nome in ("mh727_num", "mh727_nneg", "mh727_pos",
                     "mh727_int_pos", "mh727_frac_01",
                     "mh727_frac_01_incl", "mh727_energia_el",
                     "mh727_combustibile", "mh727_calore",
                     "mh727_primaria_separata", "mh727_pes",
                     "mh727_soglia_car", "mh727_is_car",
                     "mh727_certificati", "mh727_costo_gas",
                     "mh727_ricavo", "mh727_ricavo_cert",
                     "mh727_costo_om", "mh727_margine",
                     "mh727_capex", "mh727_flussi",
                     "mh727_van_flussi", "mh727_tir_flussi",
                     "mh727_payback_flussi", "mh727_verdetto",
                     "mh727_confronto", "mh727_valida",
                     "_mh727_neutro", "mh727_calcola",
                     "mh727_sensitivita", "mh727_csv",
                     "mh727_demo", "demo_calcoli"):
            assert f"def {nome}(" in src

    def test_helpers_non_importano_streamlit(self):
        assert "streamlit" not in _helpers_src()

    def test_helpers_nessuna_costante_di_modulo(self):
        tree = ast.parse(_helpers_src())
        for nodo in tree.body:
            assert not isinstance(nodo, ast.Assign), \
                "assegnamento a livello modulo vietato"

    def test_nessun_identificatore_futura_tab(self):
        assert "mh728" not in _helpers_src()
        assert "mh728" not in _ui_src()
        assert "st728" not in _ui_src()
        assert "tab728" not in _ui_src()

    def test_helpers_parse_ast(self):
        ast.parse(_helpers_src())
        ast.parse(textwrap.dedent(_ui_src()))
        ast.parse((_new_dir() / "w728_test.py")
                  .read_text(encoding="utf-8"))

    def test_titolo_presente_una_volta(self):
        assert _ui_src().count(TITLE727) == 1

    def test_blocco_with_tab727(self):
        src = _ui_src()
        assert src.split("\n")[0] == "    with tab727:"

    def test_h1_estraibile_e_uguale_titolo(self):
        m = re.search(r"<h1>(.*?)</h1>", _ui_src())
        assert m is not None
        assert m.group(1) == TITLE727

    def test_chiavi_st_univoche(self):
        keys = re.findall(r'key="(st727_[a-z0-9_]+)"', _ui_src())
        assert len(keys) == 20, keys
        assert len(set(keys)) == len(keys)
        assert all(k.startswith("st727_") for k in keys)

    def test_chiavi_st_input_sono_16(self):
        """Le 16 chiavi di input/bottone (15 input +
        bottone calcola) sono tutte presenti; le
        altre 4 sono solo chiavi di
        visualizzazione (fig, heatmap, flussi, CSV)."""
        keys = re.findall(r'key="(st727_[a-z0-9_]+)"', _ui_src())
        attese = ["st727_pot", "st727_ore",
                  "st727_eta_el", "st727_eta_th",
                  "st727_eta_el_ref", "st727_eta_th_ref",
                  "st727_prezzo_gas", "st727_prezzo_el",
                  "st727_prezzo_cal", "st727_prezzo_cert",
                  "st727_costo_om", "st727_capex_spec",
                  "st727_vita", "st727_wacc",
                  "st727_tolleranza", "st727_calcola"]
        assert len(attese) == 16
        for k in attese:
            assert k in keys, k

    def test_chiavi_st_niente_fstring_dinamiche(self):
        src = _ui_src()
        assert 'key=f"' not in src
        assert "key=f'" not in src

    def test_guard_degenere_presente(self):
        src = _ui_src()
        assert "_deg727" in src
        assert '"NON_CALCOLABILE"' in src
        assert "st.stop()" in src

    def test_guard_prima_dei_kpi(self):
        src = _ui_src()
        assert src.index("_deg727") < src.index(".metric(")

    def test_guard_prima_di_grafico_tabella_csv(self):
        src = _ui_src()
        g = src.index("_deg727")
        assert g < src.index("st.plotly_chart")
        assert g < src.index("st.dataframe")
        assert g < src.index("st.download_button")

    def test_quattro_kpi_presenti(self):
        src = _ui_src()
        assert "PES (%)" in src
        assert "Certificati CAR (cert/anno)" in src
        assert "Margine annuo (€/anno)" in src
        assert "VAN (€)" in src

    def test_verdetto_colorato_presente(self):
        src = _ui_src()
        for v in ("CONVIENTE", "MARGINALE", "NON_CONVIENTE",
                  "NON CALCOLABILE"):
            assert v in src

    def test_nota_didattica_presente(self):
        src = _ui_src().lower()
        assert "trigenerazione" in src
        assert "biomassa" in src
        assert "garanzie di origine" in src
        assert "11,63" in src
        assert "pes" in src

    def test_grafico_plotly_presente(self):
        src = _ui_src()
        assert "st.plotly_chart" in src
        assert "plotly.graph_objects" in src
        assert '"Ricavo elettricita\'"' in src
        assert '"Ricavo calore"' in src
        assert '"Margine annuo"' in src

    def test_csv_separatore_e_filename(self):
        src = _ui_src()
        assert "mh727_csv" in src
        assert "cogenerazione_car.csv" in src

    def test_sensitivita_heatmap_presente(self):
        src = _ui_src()
        assert "Sensitività del VAN (€)" in src
        assert "mh727_sensitivita" in src
        assert "Heatmap" in src
        assert "Fattore prezzo certificato" in src
        assert "Fattore ore annue" in src

    def test_flussi_opzionali_presente(self):
        src = _ui_src()
        assert "st727_show_flussi" in src
        assert "st.checkbox" in src

    def test_ancora_helper_presente(self):
        assert "# W728 (26/10/2026)" in _helpers_src()

    def test_frammenti_coerenti_con_apply(self):
        assert _ui_src().startswith("    with tab727:")
