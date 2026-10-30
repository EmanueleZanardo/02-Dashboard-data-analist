"""Test nuova scheda "Depuratore:
cogenerazione biogas + soffianti efficienti
battono rete + caldaia a gas?" (titolo
completo nel frammento UI).

Business case deterministico di un depuratore
guidato dai M3 DI REFLUI ALL'ANNO: i m3
guidano aerazione, pompaggi, biogas e calore
di digestione. Biogas = V x y_biogas x
pci_biogas; cogenerazione elettrica = Q_bio
x eta_el_chp e calore = Q_bio x eta_th_chp;
E_base = V x (e_aer + e_pomp); E_lordo_alt =
V x (e_aer x f_vsd + e_pomp) (soffianti
efficienti solo sull'aerazione); E_net_alt =
E_lordo_alt - E_chp; E_rete = max(0,
E_net_alt); E_exp = max(0, -E_net_alt);
Q_dig = V x q_dig; gas_base = Q_dig /
eta_cald; gas_alt = max(0, Q_dig - Q_chp) /
eta_cald (zero quando Q_chp copre o supera
Q_dig); C_base = E_base / 1000 x p_el +
gas_base / 1000 x p_gas + OM_base; C_alt =
E_rete / 1000 x p_el - E_exp / 1000 x p_exp
+ gas_alt / 1000 x p_gas + OM_alt;
risparmio = C_base - C_alt; CO2 evitata =
(E_base x 0,35 + gas_base x 0,20 - E_rete x
0,35 + E_exp x 0,35 - gas_alt x 0,20) /
1000 (fattori letterali; biogas biogenico,
CO2 neutra); flussi [-CAPEX, risparmio x
vita]; VAN, TIR, payback (primo anno con
cumulato >= 0); breakeven gas = (E_rete /
1000 x p_el - E_exp / 1000 x p_exp + OM_alt
- E_base / 1000 x p_el - OM_base) x 1000 /
(gas_base - gas_alt) EUR/MWh, None se
gas_base <= gas_alt o numeratore < 0,
SOGLIA MINIMA quando esiste. Nel demo il
breakeven e' None (numeratore -127.080 EUR:
l'alternativa vince anche a prezzo gas zero,
a p_gas = 0 il risparmio resta 127.080
EUR/anno). Verdetto: NON_CALCOLABILE se
input degenere (volume <= 0, aerazione o
pompaggi negativi, fattore soffianti fuori
[0, 1], resa biogas negativa, potere
calorifico <= 0, rendimenti cogenerazione
<= 0 o sopra 1, calore digestione negativo,
rendimento caldaia <= 0 o sopra 1, prezzi
<= 0, O&M negativi, CAPEX <= 0, WACC
negativo, vita <= 0, tolleranza negativa)
o se risparmio <= 0 (guard degenere: UI
salta KPI, grafico, tabella e CSV);
altrimenti CONVIENTE se VAN > 0, MARGINALE
se VAN negativa entro tolleranza % del
CAPEX, NON_CONVIENTE se VAN negativa oltre
la tolleranza. Guard UI IDENTICA agli
helper: nessuna divergenza di verdetto.
Tutti gli slider UI hanno minimo 0, quindi
i casi negativi sono NON RAGGIUNGIBILI via
slider, ma la guard li controlla comunque;
i casi = 0 raggiungibili via slider sono
bloccati in UI esattamente come negli
helper dove previsto (volume, potere
calorifico, rendimenti, rendimento caldaia,
prezzi, CAPEX, vita). Gli zeri ammessi in
entrambi (aerazione, pompaggi, fattore
soffianti 0 o 1, resa biogas, calore
digestione, O&M, WACC, tolleranza) non
creano divergenza: y_biogas = 0 resta
calcolabile in entrambi (NON_CONVIENTE nel
demo). WACC e tolleranza NON hanno tetto
superiore nel brief: gli helper li
ammettono sopra 20 % e sopra 100 % (gli
slider li limitano a 20 e 100, quindi
nessuna divergenza nel range raggiungibile).
NOTA CORREZIONE ESEMPIO BRIEF: la variante
breakeven suggerita come "f_vsd = 1 e niente
cogenerazione, con gas_alt minore di
gas_base" e' autocontraddittoria: senza
cogenerazione Q_chp = 0 e quindi gas_alt =
gas_base (denominatore nullo, breakeven
None), non gas_alt minore di gas_base. La
variante breakeven valida usata qui tiene
la cogenerazione e alza l'O&M alternativo:
f_vsd = 1 e OM_alt = 300.000 EUR/anno danno
breakeven 350,93 EUR/MWh (verifica di
pareggio nel test). La formula del
breakeven NON e' cambiata: e' quella del
brief, applicata alla lettera.
Distinzione esplicita: distinto dal centro
commerciale (m2 di superficie di vendita,
ore di apertura, banchi frigo, scale mobili:
qui niente superficie di vendita, niente
banchi frigo, niente scale mobili, niente
illuminazione), dall'officina (m2 di
capannone, portata di aria compressa, quota
di calore recuperato dal compressore VSD:
qui niente aria compressa, niente
compressore, niente recupero calore), dalla
chiesa (m2 di navata, ore di uso a
settimana, quota panche con mantenimento
antigelo: qui niente panche, niente zona
occupata a comfort, niente mantenimento
antigelo), dall'asilo (giorni di apertura,
mensa con pasti al giorno, lavanderia con kg
al giorno: qui niente mensa, niente pasti,
niente lavanderia), dall'albergo
(pernottamenti e camere: qui nessun
pernottamento, nessuna camera): qui driver
VOLUME REFLUI + BIOGAS + CALORE DIGESTIONE
+ SOFFIANTI.

Demo (depuratore): 5.000.000 m3/anno,
aerazione base 0,35 (1.750.000 kWh_e/anno)
e pompaggi 0,15 (750.000 kWh_e/anno),
fattore soffianti 0,75 (aerazione
alternativa 1.312.500 kWh_e/anno), resa
biogas 0,03 e potere calorifico 6
(Q_bio 900.000 kWh_th/anno), rendimenti
cogenerazione elettrico 0,38 (E_chp
342.000 kWh_e/anno) e termico 0,45 (Q_chp
405.000 kWh_th/anno), calore digestione
0,10 (500.000 kWh_th/anno), rendimento
caldaia 0,90 (gas base 555.555,56 e gas
alternativo 105.555,56 kWh/anno), prezzi
elettricita' 240, gas 100, export 80
EUR/MWh, O&M base 60.000, alt 120.000,
CAPEX 850.000, WACC 5 %, vita 15,
tolleranza 10 % del CAPEX. Valori calcolati
eseguendo mh815_demo_calcoli():
Q_bio 900.000, E_chp 342.000, Q_chp
405.000, E_base 2.500.000, E_lordo_alt
2.062.500, E_net_alt 1.720.500, E_rete
1.720.500, E_exp 0, Q_dig 500.000, gas_base
555.555,5555555555, gas_alt
105.555,5555555555, C_base 715.555,5555555555,
C_alt 543.475,5555555555, risparmio
172.080, CO2_base 986,1111111111111,
CO2_alt 623,2861111111111, CO2_evitata
362,825, VAN 936.131,555210116,
TIR 18,69688082013539 %, payback 5,
breakeven gas None (nessun prezzo non
negativo pareggia: l'alternativa vince anche
a gas zero), verdetto CONVIENTE.
"""

import ast
import inspect
import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from w816_helpers import (
    demo_calcoli,
    mh815_breakeven_gas,
    mh815_c_alt,
    mh815_c_base,
    mh815_calcola,
    mh815_co2_alt,
    mh815_co2_base,
    mh815_co2_evitata,
    mh815_csv,
    mh815_demo,
    mh815_demo_calcoli,
    mh815_e_base,
    mh815_e_chp,
    mh815_e_exp,
    mh815_e_lordo_alt,
    mh815_e_net_alt,
    mh815_e_rete,
    mh815_eta,
    mh815_flussi,
    mh815_frazione,
    mh815_gas_alt,
    mh815_gas_base,
    mh815_int_pos,
    mh815_nneg,
    mh815_num,
    mh815_payback,
    mh815_pos,
    mh815_q_bio,
    mh815_q_chp,
    mh815_q_dig,
    mh815_risparmio,
    mh815_tir,
    mh815_valida,
    mh815_van,
    mh815_verdetto,
)

_DEMO = {
    "q_bio_kwh_th_anno": 900000.0,
    "e_chp_kwh_e_anno": 342000.0,
    "q_chp_kwh_th_anno": 405000.0,
    "e_base_kwh_e_anno": 2500000.0,
    "e_lordo_alt_kwh_e_anno": 2062500.0,
    "e_net_alt_kwh_e_anno": 1720500.0,
    "e_rete_kwh_e_anno": 1720500.0,
    "e_exp_kwh_e_anno": 0.0,
    "q_dig_kwh_th_anno": 500000.0,
    "gas_base_kwh_anno": 555555.5555555555,
    "gas_alt_kwh_anno": 105555.5555555555,
    "c_base_eur_anno": 715555.5555555555,
    "c_alt_eur_anno": 543475.5555555555,
    "risparmio_eur_anno": 172080.0,
    "co2_base_t_anno": 986.1111111111111,
    "co2_alt_t_anno": 623.2861111111111,
    "co2_evitata_t_anno": 362.825,
    "van": 936131.555210116,
    "tir": 18.69688082013539,
}


def _demo_kwargs():
    return dict(mh815_demo())


def _variante(**kw):
    d = _demo_kwargs()
    d.update(kw)
    return mh815_calcola(**d)


# ---------------------------------------------------------------- validatori
def test_num_accetta_int_float():
    assert mh815_num(3, "x") == 3.0
    assert mh815_num(2.5, "x") == 2.5


def test_num_rifiuta_bool_stringa_nan_inf():
    for bad in (True, False, "3", None, float("nan"), float("inf"),
                float("-inf")):
        with pytest.raises(ValueError):
            mh815_num(bad, "x")


def test_nneg_zero_ok_negativo_no():
    assert mh815_nneg(0, "x") == 0.0
    with pytest.raises(ValueError):
        mh815_nneg(-0.1, "x")


def test_pos_zero_no_negativo_no():
    with pytest.raises(ValueError):
        mh815_pos(0, "x")
    with pytest.raises(ValueError):
        mh815_pos(-1, "x")
    assert mh815_pos(0.5, "x") == 0.5


def test_frazione_limiti():
    assert mh815_frazione(0, "x") == 0.0
    assert mh815_frazione(1, "x") == 1.0
    assert mh815_frazione(0.75, "x") == 0.75
    with pytest.raises(ValueError):
        mh815_frazione(-0.01, "x")
    with pytest.raises(ValueError):
        mh815_frazione(1.01, "x")


def test_eta_limiti():
    assert mh815_eta(1, "x") == 1.0
    assert mh815_eta(0.38, "x") == 0.38
    assert mh815_eta(0.45, "x") == 0.45
    assert mh815_eta(0.90, "x") == 0.90
    with pytest.raises(ValueError):
        mh815_eta(0, "x")
    with pytest.raises(ValueError):
        mh815_eta(-0.1, "x")
    with pytest.raises(ValueError):
        mh815_eta(1.01, "x")


def test_int_pos_float_intero_ok_frazionario_no():
    assert mh815_int_pos(5.0, "x") == 5
    assert mh815_int_pos(15.0, "x") == 15
    with pytest.raises(ValueError):
        mh815_int_pos(5.5, "x")
    with pytest.raises(ValueError):
        mh815_int_pos(0, "x")


# ---------------------------------------------------------------- fisica base
def test_q_bio_chp():
    assert mh815_q_bio(5000000, 0.03, 6) == 900000.0
    assert mh815_q_bio(5000000, 0, 6) == 0.0
    with pytest.raises(ValueError):
        mh815_q_bio(0, 0.03, 6)
    with pytest.raises(ValueError):
        mh815_q_bio(5000000, -0.01, 6)
    with pytest.raises(ValueError):
        mh815_q_bio(5000000, 0.03, 0)
    assert mh815_e_chp(900000.0, 0.38) == pytest.approx(342000.0)
    assert mh815_e_chp(0.0, 0.38) == 0.0
    with pytest.raises(ValueError):
        mh815_e_chp(900000.0, 0)
    with pytest.raises(ValueError):
        mh815_e_chp(900000.0, 1.01)
    assert mh815_q_chp(900000.0, 0.45) == pytest.approx(405000.0)
    assert mh815_q_chp(0.0, 0.45) == 0.0
    with pytest.raises(ValueError):
        mh815_q_chp(900000.0, 0)


def test_e_base_lordo_netto_rete_exp():
    assert mh815_e_base(5000000, 0.35, 0.15) == 2500000.0
    assert mh815_e_base(5000000, 0, 0) == 0.0
    with pytest.raises(ValueError):
        mh815_e_base(5000000, -0.01, 0.15)
    with pytest.raises(ValueError):
        mh815_e_base(0, 0.35, 0.15)
    assert mh815_e_lordo_alt(5000000, 0.35, 0.75, 0.15) == 2062500.0
    assert mh815_e_lordo_alt(5000000, 0.35, 1, 0.15) == 2500000.0
    assert mh815_e_lordo_alt(5000000, 0.35, 0, 0.15) == 750000.0
    with pytest.raises(ValueError):
        mh815_e_lordo_alt(5000000, 0.35, 1.01, 0.15)
    assert mh815_e_net_alt(2062500.0, 342000.0) == 1720500.0
    assert mh815_e_net_alt(2062500.0, 2280000.0) == pytest.approx(-217500.0)
    assert mh815_e_rete(1720500.0) == 1720500.0
    assert mh815_e_rete(-217500.0) == 0.0
    assert mh815_e_exp(1720500.0) == 0.0
    assert mh815_e_exp(-217500.0) == 217500.0


def test_q_dig_gas():
    assert mh815_q_dig(5000000, 0.10) == 500000.0
    assert mh815_q_dig(5000000, 0) == 0.0
    with pytest.raises(ValueError):
        mh815_q_dig(5000000, -0.01)
    assert mh815_gas_base(500000.0, 0.90) == pytest.approx(555555.5555555555)
    assert mh815_gas_base(0, 0.90) == 0.0
    with pytest.raises(ValueError):
        mh815_gas_base(500000.0, 0)
    with pytest.raises(ValueError):
        mh815_gas_base(500000.0, 1.01)
    assert mh815_gas_alt(500000.0, 405000.0, 0.90) == pytest.approx(105555.5555555555)
    assert mh815_gas_alt(500000.0, 540000.0, 0.90) == 0.0
    assert mh815_gas_alt(500000.0, 0.0, 0.90) == pytest.approx(555555.5555555555)
    with pytest.raises(ValueError):
        mh815_gas_alt(500000.0, -1, 0.90)


def test_c_base_c_alt_scomposizione():
    assert mh815_c_base(2500000.0, 240, 555555.5555555555, 100,
                        60000) == pytest.approx(715555.5555555555)
    assert mh815_c_alt(1720500.0, 240, 0, 80, 105555.5555555555, 100,
                       120000) == pytest.approx(543475.5555555555)
    assert mh815_c_alt(0, 240, 217500.0, 80, 0, 100,
                       120000) == pytest.approx(102600.0)
    with pytest.raises(ValueError):
        mh815_c_base(2500000.0, 0, 555555.5555555555, 100, 60000)
    with pytest.raises(ValueError):
        mh815_c_alt(1720500.0, 240, 0, 0, 105555.5555555555, 100, 120000)
    with pytest.raises(ValueError):
        mh815_c_base(2500000.0, 240, 555555.5555555555, 100, -1)


def test_risparmio_segno():
    assert mh815_risparmio(715555.5555555555, 543475.5555555555) == pytest.approx(172080.0)
    assert mh815_risparmio(543475.5555555555, 543475.5555555555) == pytest.approx(0.0, abs=1e-9)


def test_co2_base_alt_evitata():
    assert mh815_co2_base(2500000.0, 555555.5555555555) == pytest.approx(986.1111111111111)
    assert mh815_co2_alt(1720500.0, 105555.5555555555, 0) == pytest.approx(623.2861111111111)
    assert mh815_co2_alt(0, 0, 217500.0) == pytest.approx(-76.125)
    assert mh815_co2_evitata(2500000.0, 555555.5555555555,
                             1720500.0, 0,
                             105555.5555555555) == pytest.approx(362.825)
    assert mh815_co2_base(0, 0) == 0.0
    assert mh815_co2_alt(0, 0, 0) == 0.0
    with pytest.raises(ValueError):
        mh815_co2_base(2500000.0, -1)
    with pytest.raises(ValueError):
        mh815_co2_alt(-1, 0, 0)


def test_breakeven_demo_none_e_varianti():
    # Demo: numeratore negativo -> None:
    # l'alternativa vince anche a gas zero.
    assert mh815_demo_calcoli()["breakeven_gas_eur_mwh"] is None
    assert mh815_breakeven_gas(1720500.0, 240, 0, 80, 120000,
                               2500000.0, 60000, 555555.5555555555,
                               105555.5555555555) is None
    bc = _variante(om_alt=300000)
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(117.6)
    bc2 = _variante(f_vsd=1, om_alt=300000)
    assert bc2["breakeven_gas_eur_mwh"] == pytest.approx(350.9333333333334)
    assert _variante(y_biogas_m3_m3=0)["breakeven_gas_eur_mwh"] is None
    assert mh815_breakeven_gas(1720500.0, 240, 0, 80, 120000,
                               2500000.0, 60000, 555555.5555555555,
                               555555.5555555555) is None
    with pytest.raises(ValueError):
        mh815_breakeven_gas(1720500.0, 240, 0, 80, 120000,
                           2500000.0, 60000, -1,
                           105555.5555555555)


def test_breakeven_esempio_brief_senza_chp_e_none():
    # L'esempio del brief (f_vsd = 1, niente
    # cogenerazione) NON da' un breakeven: con
    # Q_chp = 0, gas_alt = gas_base, quindi
    # denominatore nullo e breakeven None, non
    # gas_alt minore di gas_base.
    bc = _variante(f_vsd=1, y_biogas_m3_m3=0)
    assert bc["gas_alt_kwh_anno"] == pytest.approx(bc["gas_base_kwh_anno"])
    assert bc["e_rete_kwh_e_anno"] == pytest.approx(bc["e_base_kwh_e_anno"])
    assert bc["breakeven_gas_eur_mwh"] is None


def test_breakeven_verifica_pareggio_su_variante():
    # La variante valida tiene la cogenerazione
    # e alza l'O&M alternativo (f_vsd = 1,
    # OM_alt 300.000): il pareggio esiste.
    be = _variante(f_vsd=1, om_alt=300000)["breakeven_gas_eur_mwh"]
    assert be == pytest.approx(350.9333333333334)
    bc = _variante(f_vsd=1, om_alt=300000, p_gas=be)
    assert bc["c_base_eur_anno"] == pytest.approx(bc["c_alt_eur_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"


def test_breakeven_soglia_minima_su_variante():
    be = _variante(f_vsd=1, om_alt=300000)["breakeven_gas_eur_mwh"]
    bc_alto = _variante(f_vsd=1, om_alt=300000, p_gas=be + 1)
    bc_basso = _variante(f_vsd=1, om_alt=300000, p_gas=be - 1)
    assert bc_alto["c_alt_eur_anno"] < bc_alto["c_base_eur_anno"]
    assert bc_basso["c_alt_eur_anno"] > bc_basso["c_base_eur_anno"]
    assert bc_alto["risparmio_eur_anno"] > 0.0
    assert bc_alto["verdetto"] == "NON_CONVIENTE"
    assert bc_basso["verdetto"] == "NON_CALCOLABILE"


# ---------------------------------------------------------------- finanza base
def test_flussi_lunghezza_e_primo():
    fl = mh815_flussi(850000, 172080.0, 15)
    assert len(fl) == 16
    assert fl[0] == -850000
    assert all(f == 172080.0 for f in fl[1:])


def test_van_demo_e_zero_wacc():
    bc = mh815_demo_calcoli()
    assert bc["van"] == pytest.approx(936131.555210116)
    assert mh815_van([-850000] + [172080.0] * 15,
                     0) == pytest.approx(1731200.0)
    assert mh815_van([-100] + [50] * 2, 0) == 0.0


def test_tir_demo():
    bc = mh815_demo_calcoli()
    assert bc["tir"] == pytest.approx(18.69688082013539)
    assert mh815_tir([-850000] + [172080.0] * 15) == \
        pytest.approx(0.1869688082013539)
    tir = mh815_tir([-850000] + [172080.0] * 15)
    npv = sum(f / (1.0 + tir) ** i
              for i, f in enumerate([-850000] + [172080.0] * 15))
    assert npv == pytest.approx(0.0, abs=1e-2)


def test_payback_regola_maggiore_uguale():
    assert mh815_payback([-850000] + [172080.0] * 15) == 5
    assert mh815_payback([-850000] + [-1000.0] * 15) is None
    assert mh815_payback([-100] + [50] * 2) == 2


def test_verdetto():
    assert mh815_verdetto(172080.0, 936131.555210116, 850000,
                          10.0) == "CONVIENTE"
    assert mh815_verdetto(172080.0, -1500.0, 850000,
                          10.0) == "MARGINALE"
    assert mh815_verdetto(172080.0, -85000.0, 850000, 10.0) == "MARGINALE"
    assert mh815_verdetto(172080.0, -85000.01, 850000, 10.0) == "NON_CONVIENTE"
    assert mh815_verdetto(172080.0, 0.0, 850000, 10.0) == "MARGINALE"
    assert mh815_verdetto(0.0, 936131.56, 850000,
                          10.0) == "NON_CALCOLABILE"
    assert mh815_verdetto(-7920.0, -932206.89, 850000,
                          10.0) == "NON_CALCOLABILE"
    assert mh815_verdetto(None, 936131.56, 850000,
                          10.0) == "NON_CALCOLABILE"
    with pytest.raises(ValueError):
        mh815_verdetto(float("nan"), 936131.56, 850000, 10.0)
    with pytest.raises(ValueError):
        mh815_verdetto(172080.0, 936131.56, 0, 10.0)
    with pytest.raises(ValueError):
        mh815_verdetto(172080.0, 936131.56, 850000, -1)


def test_valida_demo_ok():
    v = mh815_valida(**_demo_kwargs())
    assert v["valido"] is True
    assert v["errore"] == ""


def test_valida_rifiuta_stringa_nan_inf_bool():
    for campo, bad in (("volume_m3_anno", "5000000"),
                       ("volume_m3_anno", float("nan")),
                       ("volume_m3_anno", float("inf")),
                       ("volume_m3_anno", True),
                       ("p_gas", None),
                       ("y_biogas_m3_m3", "0.03")):
        d = _demo_kwargs()
        d[campo] = bad
        assert mh815_valida(**d)["valido"] is False


def test_valida_rifiuta_range():
    for campo, valore in (("volume_m3_anno", 0),
                          ("volume_m3_anno", -10),
                          ("e_aer_kwh_m3", -0.1),
                          ("e_pomp_kwh_m3", -0.1),
                          ("f_vsd", -0.1),
                          ("f_vsd", 1.01),
                          ("y_biogas_m3_m3", -0.01),
                          ("pci_biogas_kwh_th_m3", 0),
                          ("pci_biogas_kwh_th_m3", -1),
                          ("eta_el_chp", 0),
                          ("eta_el_chp", 1.01),
                          ("eta_th_chp", 0),
                          ("eta_th_chp", 1.01),
                          ("q_dig_kwh_th_m3", -0.01),
                          ("eta_cald", 0),
                          ("eta_cald", 1.01),
                          ("p_el", 0),
                          ("p_el", -1),
                          ("p_gas", 0),
                          ("p_gas", -1),
                          ("p_exp", 0),
                          ("p_exp", -1),
                          ("om_base", -100),
                          ("om_alt", -100),
                          ("capex", 0),
                          ("capex", -1),
                          ("wacc_pct", -0.1),
                          ("vita_anni", 0), ("vita_anni", 2.5),
                          ("tolleranza_pct", -1)):
        d = _demo_kwargs()
        d.update({campo: valore})
        assert mh815_valida(**d)["valido"] is False


def test_valida_accetta_limiti_e_nessun_tetto_wacc_tolleranza():
    d = _demo_kwargs()
    d.update({"e_aer_kwh_m3": 0,
              "e_pomp_kwh_m3": 0,
              "f_vsd": 0,
              "y_biogas_m3_m3": 0,
              "q_dig_kwh_th_m3": 0,
              "om_base": 0, "om_alt": 0,
              "wacc_pct": 0,
              "tolleranza_pct": 0})
    assert mh815_valida(**d)["valido"] is True
    d["f_vsd"] = 1
    d["eta_el_chp"] = 1
    d["eta_th_chp"] = 1
    d["eta_cald"] = 1
    # Il brief non impone tetti superiori a WACC
    # e tolleranza: gli helper li ammettono.
    d["wacc_pct"] = 60
    d["tolleranza_pct"] = 200
    assert mh815_valida(**d)["valido"] is True


def test_demo_dict():
    d = mh815_demo()
    assert d["volume_m3_anno"] == 5000000
    assert d["e_aer_kwh_m3"] == 0.35
    assert d["e_pomp_kwh_m3"] == 0.15
    assert d["f_vsd"] == 0.75
    assert d["y_biogas_m3_m3"] == 0.03
    assert d["pci_biogas_kwh_th_m3"] == 6
    assert d["eta_el_chp"] == 0.38
    assert d["eta_th_chp"] == 0.45
    assert d["q_dig_kwh_th_m3"] == 0.10
    assert d["eta_cald"] == 0.90
    assert d["p_el"] == 240
    assert d["p_gas"] == 100
    assert d["p_exp"] == 80
    assert d["om_base"] == 60000
    assert d["om_alt"] == 120000
    assert d["capex"] == 850000
    assert d["wacc_pct"] == 5.0
    assert d["vita_anni"] == 15
    assert d["tolleranza_pct"] == 10.0


def test_demo_costanti_vs_demo_calcoli():
    bc = mh815_demo_calcoli()
    for chiave, atteso in _DEMO.items():
        got = bc[chiave]
        if atteso == 0.0:
            assert got == pytest.approx(0.0, abs=1e-12)
        else:
            assert got == pytest.approx(atteso, rel=1e-9), chiave
    assert bc["payback"] == 5
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["valid"] is True
    assert bc["breakeven_gas_eur_mwh"] is None
    assert demo_calcoli()["van"] == bc["van"]


def test_demo_calcoli_fisica_economia():
    bc = mh815_demo_calcoli()
    assert bc["c_base_eur_anno"] == pytest.approx(715555.5555555555)
    assert bc["c_alt_eur_anno"] == pytest.approx(543475.5555555555)
    assert bc["risparmio_eur_anno"] == pytest.approx(172080.0)
    assert bc["co2_base_t_anno"] == pytest.approx(986.1111111111111)
    assert bc["co2_alt_t_anno"] == pytest.approx(623.2861111111111)
    assert bc["co2_evitata_t_anno"] == pytest.approx(362.825)
    assert bc["q_bio_kwh_th_anno"] == pytest.approx(900000.0)
    assert bc["e_chp_kwh_e_anno"] == pytest.approx(342000.0)
    assert bc["q_chp_kwh_th_anno"] == pytest.approx(405000.0)
    assert bc["e_base_kwh_e_anno"] == pytest.approx(2500000.0)
    assert bc["e_lordo_alt_kwh_e_anno"] == pytest.approx(2062500.0)
    assert bc["e_net_alt_kwh_e_anno"] == pytest.approx(1720500.0)
    assert bc["e_rete_kwh_e_anno"] == pytest.approx(1720500.0)
    assert bc["e_exp_kwh_e_anno"] == pytest.approx(0.0, abs=1e-12)
    assert bc["q_dig_kwh_th_anno"] == pytest.approx(500000.0)
    assert bc["gas_base_kwh_anno"] == pytest.approx(555555.5555555555)
    assert bc["gas_alt_kwh_anno"] == pytest.approx(105555.5555555555)


def test_demo_flussi_e_cumulato():
    bc = mh815_demo_calcoli()
    assert bc["flussi"][0] == -850000
    assert len(bc["flussi"]) == 16
    assert all(f == pytest.approx(172080.0) for f in bc["flussi"][1:])
    righe = bc["df_flussi"]
    assert righe.iloc[0]["Anno"] == 0
    assert righe.iloc[0]["Cumulato (EUR)"] == -850000
    assert righe.iloc[4]["Cumulato (EUR)"] == pytest.approx(-161680.0)
    assert righe.iloc[5]["Cumulato (EUR)"] == pytest.approx(10400.0)
    assert righe.iloc[15]["Cumulato (EUR)"] == pytest.approx(1731200.0)


def test_demo_tabella_righe():
    bc = mh815_demo_calcoli()
    mappa = {r["Voce"]: r["Valore"]
             for _, r in bc["df_tabella"].iterrows()}
    assert mappa["Biogas energetico (kWh_th/anno)"] == pytest.approx(900000.0)
    assert mappa["Elettricita' cogenerazione (kWh_e/anno)"] == pytest.approx(342000.0)
    assert mappa["Calore cogenerazione (kWh_th/anno)"] == pytest.approx(405000.0)
    assert mappa["Elettricita' base (kWh_e/anno)"] == pytest.approx(2500000.0)
    assert mappa["Elettricita' lorda alternativa (kWh_e/anno)"] == pytest.approx(2062500.0)
    assert mappa["Prelievo da rete (kWh_e/anno)"] == pytest.approx(1720500.0)
    assert mappa["Export in rete (kWh_e/anno)"] == pytest.approx(0.0, abs=1e-12)
    assert mappa["Calore digestione (kWh_th/anno)"] == pytest.approx(500000.0)
    assert mappa["Gas baseline (kWh/anno)"] == pytest.approx(555555.5555555555)
    assert mappa["Gas alternativo (kWh/anno)"] == pytest.approx(105555.5555555555)
    assert mappa["Costo baseline (EUR/anno)"] == pytest.approx(715555.5555555555)
    assert mappa["Costo alternativo (EUR/anno)"] == pytest.approx(543475.5555555555)
    assert mappa["Risparmio (EUR/anno)"] == pytest.approx(172080.0)
    assert mappa["CO2 evitata (t/anno)"] == pytest.approx(362.825)
    assert mappa["Payback (anni)"] == 5
    assert mappa["Verdetto"] == "CONVIENTE"
    assert mappa["Breakeven prezzo gas (EUR/MWh)"] is None


def test_demo_coerenza_interna():
    bc = mh815_demo_calcoli()
    assert bc["c_base_eur_anno"] - bc["c_alt_eur_anno"] == \
        pytest.approx(bc["risparmio_eur_anno"])
    assert bc["q_bio_kwh_th_anno"] == pytest.approx(
        bc["volume_m3_anno"] * bc["y_biogas_m3_m3"]
        * bc["pci_biogas_kwh_th_m3"])
    assert bc["e_chp_kwh_e_anno"] == pytest.approx(
        bc["q_bio_kwh_th_anno"] * bc["eta_el_chp"])
    assert bc["q_chp_kwh_th_anno"] == pytest.approx(
        bc["q_bio_kwh_th_anno"] * bc["eta_th_chp"])
    assert bc["e_base_kwh_e_anno"] == pytest.approx(
        bc["volume_m3_anno"] * (bc["e_aer_kwh_m3"] + bc["e_pomp_kwh_m3"]))
    assert bc["e_lordo_alt_kwh_e_anno"] == pytest.approx(
        bc["volume_m3_anno"] * (bc["e_aer_kwh_m3"] * bc["f_vsd"]
                                + bc["e_pomp_kwh_m3"]))
    assert bc["e_net_alt_kwh_e_anno"] == pytest.approx(
        bc["e_lordo_alt_kwh_e_anno"] - bc["e_chp_kwh_e_anno"])
    assert bc["e_rete_kwh_e_anno"] == pytest.approx(
        max(0.0, bc["e_net_alt_kwh_e_anno"]))
    assert bc["e_exp_kwh_e_anno"] == pytest.approx(
        max(0.0, -bc["e_net_alt_kwh_e_anno"]))
    assert bc["q_dig_kwh_th_anno"] == pytest.approx(
        bc["volume_m3_anno"] * bc["q_dig_kwh_th_m3"])
    assert bc["gas_base_kwh_anno"] == pytest.approx(
        bc["q_dig_kwh_th_anno"] / bc["eta_cald"])
    assert bc["gas_alt_kwh_anno"] == pytest.approx(
        max(0.0, bc["q_dig_kwh_th_anno"] - bc["q_chp_kwh_th_anno"])
        / bc["eta_cald"])
    assert bc["co2_evitata_t_anno"] == pytest.approx(
        bc["co2_base_t_anno"] - bc["co2_alt_t_anno"])
    assert bc["c_base_eur_anno"] == pytest.approx(
        bc["e_base_kwh_e_anno"] / 1000.0 * bc["p_el"]
        + bc["gas_base_kwh_anno"] / 1000.0 * bc["p_gas"]
        + bc["om_base"])
    assert bc["c_alt_eur_anno"] == pytest.approx(
        bc["e_rete_kwh_e_anno"] / 1000.0 * bc["p_el"]
        - bc["e_exp_kwh_e_anno"] / 1000.0 * bc["p_exp"]
        + bc["gas_alt_kwh_anno"] / 1000.0 * bc["p_gas"]
        + bc["om_alt"])


def test_demo_contro_riconteggio_indipendente():
    vol, eaer, epom, fvs = 5000000, 0.35, 0.15, 0.75
    ybio, pci = 0.03, 6
    eel, eth = 0.38, 0.45
    qdigm, etac = 0.10, 0.90
    pel, pg, pex = 240, 100, 80
    omb, oma, cx = 60000, 120000, 850000
    wacc, vita = 5.0, 15
    qbio = vol * ybio * pci
    echp = qbio * eel
    qchp = qbio * eth
    eb = vol * (eaer + epom)
    elor = vol * (eaer * fvs + epom)
    enet = elor - echp
    eret = max(0.0, enet)
    eexp = max(0.0, -enet)
    qdig = vol * qdigm
    gasb = qdig / etac
    gasa = max(0.0, qdig - qchp) / etac
    cb = eb / 1000.0 * pel + gasb / 1000.0 * pg + omb
    ca = eret / 1000.0 * pel - eexp / 1000.0 * pex + gasa / 1000.0 * pg + oma
    risp = cb - ca
    co2b = (eb * 0.35 + gasb * 0.20) / 1000.0
    co2a = (eret * 0.35 + gasa * 0.20 - eexp * 0.35) / 1000.0
    co2 = co2b - co2a
    r = wacc / 100.0
    van = -cx + sum(risp / (1 + r) ** t for t in range(1, vita + 1))
    bc = mh815_demo_calcoli()
    assert bc["q_bio_kwh_th_anno"] == pytest.approx(qbio)
    assert bc["e_chp_kwh_e_anno"] == pytest.approx(echp)
    assert bc["q_chp_kwh_th_anno"] == pytest.approx(qchp)
    assert bc["e_base_kwh_e_anno"] == pytest.approx(eb)
    assert bc["e_lordo_alt_kwh_e_anno"] == pytest.approx(elor)
    assert bc["e_net_alt_kwh_e_anno"] == pytest.approx(enet)
    assert bc["e_rete_kwh_e_anno"] == pytest.approx(eret)
    assert bc["e_exp_kwh_e_anno"] == pytest.approx(eexp)
    assert bc["q_dig_kwh_th_anno"] == pytest.approx(qdig)
    assert bc["gas_base_kwh_anno"] == pytest.approx(gasb)
    assert bc["gas_alt_kwh_anno"] == pytest.approx(gasa)
    assert bc["c_base_eur_anno"] == pytest.approx(cb)
    assert bc["c_alt_eur_anno"] == pytest.approx(ca)
    assert bc["risparmio_eur_anno"] == pytest.approx(risp)
    assert bc["co2_base_t_anno"] == pytest.approx(co2b)
    assert bc["co2_alt_t_anno"] == pytest.approx(co2a)
    assert bc["co2_evitata_t_anno"] == pytest.approx(co2)
    assert bc["van"] == pytest.approx(van)
    assert bc["breakeven_gas_eur_mwh"] is None


def test_demo_verdetto_coerente_con_risparmio_e_van():
    bc = mh815_demo_calcoli()
    assert bc["risparmio_eur_anno"] > 0.0
    assert bc["van"] > 0.0
    assert bc["verdetto"] == "CONVIENTE"
    assert bc["tir"] is not None and bc["tir"] > bc["wacc_pct"]
    assert bc["payback"] == 5


# ---------------------------------------------------------------- varianti
def test_variante_senza_cogenerazione_non_convinte():
    # Resa biogas zero = niente cogenerazione:
    # il caso resta calcolabile ma diventa
    # NON_CONVIENTE; breakeven None perche'
    # gas_alt = gas_base.
    bc = _variante(y_biogas_m3_m3=0)
    assert bc["q_bio_kwh_th_anno"] == 0.0
    assert bc["e_chp_kwh_e_anno"] == 0.0
    assert bc["q_chp_kwh_th_anno"] == 0.0
    assert bc["gas_alt_kwh_anno"] == pytest.approx(bc["gas_base_kwh_anno"])
    assert bc["risparmio_eur_anno"] == pytest.approx(45000.0)
    assert bc["van"] == pytest.approx(-382915.3882818734)
    assert bc["tir"] == pytest.approx(-2.7522279510630514)
    assert bc["payback"] is None
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_senza_soffianti_non_convinte():
    # Fattore soffianti 1 = niente risparmio
    # dalle soffianti: il caso diventa
    # NON_CONVIENTE, breakeven None per
    # numeratore negativo.
    bc = _variante(f_vsd=1)
    assert bc["e_lordo_alt_kwh_e_anno"] == pytest.approx(2500000.0)
    assert bc["risparmio_eur_anno"] == pytest.approx(67080.0)
    assert bc["van"] == pytest.approx(-153732.538798846)
    assert bc["payback"] == 13
    assert bc["breakeven_gas_eur_mwh"] is None
    assert bc["verdetto"] == "NON_CONVIENTE"


def test_variante_export_in_rete():
    # Resa biogas 0,20: la cogenerazione supera
    # il carico lordo, quindi prelievo zero,
    # export positivo e gas alternativo zero.
    bc = _variante(y_biogas_m3_m3=0.20)
    assert bc["q_bio_kwh_th_anno"] == pytest.approx(6000000.0)
    assert bc["e_chp_kwh_e_anno"] == pytest.approx(2280000.0)
    assert bc["q_chp_kwh_th_anno"] == pytest.approx(2700000.0)
    assert bc["e_net_alt_kwh_e_anno"] == pytest.approx(-217500.0)
    assert bc["e_rete_kwh_e_anno"] == 0.0
    assert bc["e_exp_kwh_e_anno"] == pytest.approx(217500.0)
    assert bc["gas_alt_kwh_anno"] == 0.0
    assert bc["risparmio_eur_anno"] == pytest.approx(612955.5555555555)
    assert bc["van"] == pytest.approx(5512269.059269671)
    assert bc["payback"] == 2
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_gas_alt_zero_senza_export():
    # Resa biogas 0,04: Q_chp 540.000 sopra
    # Q_dig 500.000, quindi gas_alt zero, ma
    # il carico lordo resta sopra E_chp: niente
    # export, solo prelievo ridotto.
    bc = _variante(y_biogas_m3_m3=0.04)
    assert bc["q_chp_kwh_th_anno"] == pytest.approx(540000.0)
    assert bc["gas_alt_kwh_anno"] == 0.0
    assert bc["e_rete_kwh_e_anno"] == pytest.approx(1606500.0)
    assert bc["e_exp_kwh_e_anno"] == pytest.approx(0.0, abs=1e-12)
    assert bc["risparmio_eur_anno"] == pytest.approx(209995.5555555555)
    assert bc["van"] == pytest.approx(1329682.0562044205)
    assert bc["payback"] == 5
    assert bc["verdetto"] == "CONVIENTE"


def test_variante_capex_marginale_e_non_convinte():
    bc = _variante(capex=1900000)
    assert bc["risparmio_eur_anno"] == pytest.approx(172080.0)
    assert bc["van"] == pytest.approx(-113868.44478988402)
    assert bc["payback"] == 12
    assert bc["verdetto"] == "MARGINALE"
    bc2 = _variante(capex=2500000)
    assert bc2["van"] == pytest.approx(-713868.444789884)
    assert bc2["payback"] == 15
    assert bc2["verdetto"] == "NON_CONVIENTE"


def test_variante_om_alt_alto_non_calcolabile():
    # O&M alt 300.000: risparmio negativo negli
    # helper (calcolabile, non solleva), verdetto
    # NON_CALCOLABILE; stessa guard della UI.
    # Breakeven qui ESISTE (117,60 EUR/MWh).
    bc = _variante(om_alt=300000)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] == pytest.approx(-7920.0)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"]
    assert bc["payback"] is None
    assert bc["tir"] is None
    assert bc["breakeven_gas_eur_mwh"] == pytest.approx(117.6)


def test_variante_wacc_zero_e_vita_diversa():
    bc = _variante(wacc_pct=0)
    assert bc["van"] == pytest.approx(1731200.0)
    assert bc["verdetto"] == "CONVIENTE"
    bc2 = _variante(vita_anni=10)
    assert len(bc2["flussi"]) == 11
    assert bc2["van"] == pytest.approx(478756.14661412226)
    assert bc2["payback"] == 5
    assert bc2["verdetto"] == "CONVIENTE"


def test_variante_prezzo_el_alto_resta_convinte():
    # Elettricita' a 400 EUR/MWh: il risparmio
    # cresce perche' l'alternativa preleva meno
    # elettricita' della base.
    bc = _variante(p_el=400)
    assert bc["risparmio_eur_anno"] == pytest.approx(296800.0)
    assert bc["van"] == pytest.approx(2230682.505731999)
    assert bc["payback"] == 3
    assert bc["verdetto"] == "CONVIENTE"


def test_monotonia_prezzo_gas_crescente():
    base = mh815_demo_calcoli()["risparmio_eur_anno"]
    alto = _variante(p_gas=101)["risparmio_eur_anno"]
    basso = _variante(p_gas=99)["risparmio_eur_anno"]
    assert alto > base > basso
    assert alto - base == pytest.approx(450.0, abs=1e-2)
    assert base - basso == pytest.approx(450.0, abs=1e-2)


def test_monotonia_f_vsd_decrescente_risparmio_cresce():
    assert _variante(f_vsd=0.50)["risparmio_eur_anno"] > \
        mh815_demo_calcoli()["risparmio_eur_anno"]
    assert _variante(f_vsd=1.0)["risparmio_eur_anno"] < \
        mh815_demo_calcoli()["risparmio_eur_anno"]


def test_demo_deterministica_due_chiamate():
    a = mh815_demo_calcoli()
    b = mh815_demo_calcoli()
    assert a["van"] == b["van"]
    assert a["tir"] == b["tir"]
    assert a["flussi"] == b["flussi"]


def test_demo_chiavi_attese():
    assert set(mh815_demo().keys()) == {
        "volume_m3_anno", "e_aer_kwh_m3", "e_pomp_kwh_m3",
        "f_vsd", "y_biogas_m3_m3", "pci_biogas_kwh_th_m3",
        "eta_el_chp", "eta_th_chp", "q_dig_kwh_th_m3",
        "eta_cald", "p_el", "p_gas", "p_exp",
        "om_base", "om_alt",
        "capex", "wacc_pct", "vita_anni",
        "tolleranza_pct"}


# ---------------------------------------------------------------- degenere
def test_degenere_tutti_i_campi_sollevano():
    for kw in ({"volume_m3_anno": 0},
               {"volume_m3_anno": -10},
               {"e_aer_kwh_m3": -0.1},
               {"e_pomp_kwh_m3": -0.1},
               {"f_vsd": -0.1}, {"f_vsd": 1.01},
               {"y_biogas_m3_m3": -0.01},
               {"pci_biogas_kwh_th_m3": 0},
               {"pci_biogas_kwh_th_m3": -1},
               {"eta_el_chp": 0}, {"eta_el_chp": 1.01},
               {"eta_th_chp": 0}, {"eta_th_chp": 1.01},
               {"q_dig_kwh_th_m3": -0.01},
               {"eta_cald": 0}, {"eta_cald": 1.01},
               {"p_el": 0}, {"p_el": -1},
               {"p_gas": 0}, {"p_gas": -1},
               {"p_exp": 0}, {"p_exp": -1},
               {"om_base": -100},
               {"om_alt": -100},
               {"capex": 0}, {"capex": -1},
               {"wacc_pct": -1},
               {"vita_anni": 0}, {"vita_anni": 2.5},
               {"tolleranza_pct": -1}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh815_valida(**d)["valido"] is False


def test_degenere_stringa_nan_inf():
    for kw in ({"volume_m3_anno": "5000000"},
               {"volume_m3_anno": float("nan")},
               {"p_gas": float("inf")},
               {"capex": True},
               {"y_biogas_m3_m3": "0.03"}):
        with pytest.raises(ValueError):
            _variante(**kw)
        d = _demo_kwargs()
        d.update(kw)
        assert mh815_valida(**d)["valido"] is False


def test_zeri_ammessi_non_sollevano_e_nessuna_divergenza():
    # Zeri ammessi in entrambi (helper e UI):
    # aerazione, pompaggi, fattore 0 e 1, resa
    # biogas, calore digestione, O&M, WACC,
    # tolleranza. Qui si verifica che non
    # sollevano e restano calcolabili.
    for kw in ({"e_aer_kwh_m3": 0},
               {"e_pomp_kwh_m3": 0},
               {"f_vsd": 0},
               {"f_vsd": 1},
               {"y_biogas_m3_m3": 0},
               {"q_dig_kwh_th_m3": 0},
               {"om_base": 0},
               {"om_alt": 0},
               {"wacc_pct": 0},
               {"tolleranza_pct": 0}):
        bc = _variante(**kw)
        assert bc["valid"] is True
        assert bc["verdetto"] in ("CONVIENTE", "MARGINALE",
                                  "NON_CONVIENTE", "NON_CALCOLABILE")


def test_risparmio_nonpositivo_non_sollevela_ma_non_calcolabile():
    bc = _variante(om_alt=300000)
    assert bc["valid"] is True
    assert bc["risparmio_eur_anno"] <= 0.0
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["flussi"]


def test_pareggio_esatto_tolleranza_float():
    # A pareggio esatto (prezzo gas = breakeven
    # della variante f_vsd = 1, OM_alt 300.000)
    # il risparmio e' zero (circa 0.0, quindi
    # guard NON_CALCOLABILE): in nessun caso
    # CONVIENTE.
    be = _variante(f_vsd=1, om_alt=300000)["breakeven_gas_eur_mwh"]
    bc = _variante(f_vsd=1, om_alt=300000, p_gas=be)
    assert bc["risparmio_eur_anno"] == pytest.approx(0.0, abs=1e-6)
    assert bc["verdetto"] == "NON_CALCOLABILE"
    assert bc["verdetto"] != "CONVIENTE"
    bc2 = _variante(f_vsd=1, om_alt=300000, p_gas=be + 1)
    assert bc2["risparmio_eur_anno"] == pytest.approx(450.0, abs=1e-2)
    # Risparmio positivo ma piccolo: VAN negativa oltre
    # la tolleranza, quindi NON_CONVIENTE (non CONVIENTE).
    assert bc2["verdetto"] == "NON_CONVIENTE"


# ---------------------------------------------------------------- CSV
def test_csv_sep_e_righe():
    bc = mh815_demo_calcoli()
    testo = mh815_csv(bc, _demo_kwargs())
    assert ";" in testo
    assert "voce;valore" in testo
    assert f"c_base_eur_anno;{bc['c_base_eur_anno']}" in testo
    assert f"c_alt_eur_anno;{bc['c_alt_eur_anno']}" in testo
    assert f"risparmio_eur_anno;{bc['risparmio_eur_anno']}" in testo
    assert "verdetto;CONVIENTE" in testo
    assert "breakeven_gas_eur_mwh" in testo
    assert "co2_evitata_t_anno" in testo
    assert "q_bio_kwh_th_anno" in testo
    assert "e_chp_kwh_e_anno" in testo
    assert "e_rete_kwh_e_anno" in testo
    assert "e_exp_kwh_e_anno" in testo
    assert "q_dig_kwh_th_anno" in testo
    assert "gas_alt_kwh_anno" in testo


def test_csv_valori_coerenti_con_calcola():
    bc = mh815_demo_calcoli()
    testo = mh815_csv(bc, _demo_kwargs())
    assert f"van_eur;{bc['van']}" in testo
    assert f"e_chp_kwh_e_anno;{bc['e_chp_kwh_e_anno']}" in testo
    assert f"gas_base_kwh_anno;{bc['gas_base_kwh_anno']}" in testo
    assert f"q_bio_kwh_th_anno;{bc['q_bio_kwh_th_anno']}" in testo


def test_csv_contiene_tutte_le_chiavi_input():
    bc = mh815_demo_calcoli()
    testo = mh815_csv(bc, _demo_kwargs())
    for chiave in _demo_kwargs():
        assert f"{chiave};" in testo


# ------------------------------------------------------- test strutturali
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _leggi(nome):
    qui = os.path.dirname(os.path.abspath(__file__))
    p = os.path.join(qui, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    with open(p, encoding="utf-8") as f:
        return f.read()


def _vietati():
    # Token della scheda precedente, costruiti
    # per concatenazione: questo stesso file non li contiene
    # come sottostringhe contigue.
    return ["mh" + "81" + "4", "st" + "81" + "4",
            "tab" + "81" + "4", "w" + "81" + "5",
            "mh" + "81" + "3", "tab" + "81" + "3"]


def test_ast_helpers_parsabile():
    ast.parse(_leggi("w816_helpers.py"))


def test_ast_ui_dedentata_parsabile():
    src = textwrap.dedent(_leggi("w816_ui.py"))
    ast.parse(src)
    assert src.startswith("# W816")
    assert "with tab815:" in src


def test_ui_apre_scheda_attesa_una_volta():
    """Il frammento UI apre la scheda attesa, una sola volta."""
    src = _leggi("w816_ui.py")
    m = re.search(r"with tab(\d+):", src)
    assert m is not None
    assert m.group(1) == "815"
    assert src.count("with tab815:") == 1


def test_ui_titolo_atteso():
    src = _leggi("w816_ui.py")
    titolo = ("Depuratore: cogenerazione biogas + "
              "soffianti efficienti battono rete + "
              "caldaia a gas?")
    assert src.count(titolo) == 2


def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab():
    src = _leggi("w816_helpers.py")
    assert "streamlit" not in src
    assert all(t not in src for t in _vietati())


def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche():
    src = _leggi("w816_ui.py")
    assert all(t not in src for t in _vietati())
    chiavi = re.findall(r'key="([^"]+)"', src)
    assert chiavi
    assert all(c.startswith("st815_") for c in chiavi)
    assert len(chiavi) == len(set(chiavi))
    assert len(chiavi) == 29
    assert "key=f" not in src and "key = f" not in src


def test_ui_guard_prima_output():
    src = _leggi("w816_ui.py")
    assert "st.stop()" in src
    assert src.count("st.stop()") >= 4
    assert src.index("st.stop()") < src.index("st.bar_chart")
    assert src.index("st.stop()") < src.index("st.dataframe")
    assert src.index("st.stop()") < src.index("st.download_button")
    assert "risparmio_eur_anno\"] <= 0.0" in src


def test_ui_guard_degenere_identica_helper():
    """La guard UI della scheda dichiara NON_CALCOLABILE
    per gli stessi casi degeneri degli helper:
    volume <= 0, potere calorifico <= 0, rendimenti
    <= 0 o sopra 1, rendimento caldaia <= 0 o sopra 1,
    prezzi <= 0, CAPEX <= 0, vita <= 0 (nessuna
    divergenza helper-vs-UI, a differenza di schede
    precedenti)."""
    src = _leggi("w816_ui.py")
    assert "float(_vol815) <= 0.0" in src
    assert "float(_pci815) <= 0.0" in src
    assert "float(_etael815) <= 0.0" in src
    assert "float(_etael815) > 1.0" in src
    assert "float(_etath815) <= 0.0" in src
    assert "float(_etacald815) <= 0.0" in src
    assert "float(_etacald815) > 1.0" in src
    assert "float(_pel815) <= 0.0" in src
    assert "float(_pg815) <= 0.0" in src
    assert "float(_pexp815) <= 0.0" in src
    assert "float(_cx815) <= 0.0" in src
    assert "int(_vita815) <= 0" in src
    assert "Verdetto: NON_CALCOLABILE" in src


def test_ui_chiamata_calcola_keyword_uguali_firma():
    """La chiamata UI a calcola usa come keyword
    esattamente i parametri della firma helper."""
    src = textwrap.dedent(_leggi("w816_ui.py"))
    albero = ast.parse(src)
    chiamate = []
    for nodo in ast.walk(albero):
        if isinstance(nodo, ast.Call):
            func = nodo.func
            if isinstance(func, ast.Name) and func.id == "mh815_calcola":
                chiamate.append({kw.arg for kw in nodo.keywords})
    assert len(chiamate) == 1
    attesi = set(inspect.signature(mh815_calcola).parameters.keys())
    assert chiamate[0] == attesi


def test_test_senza_residui_vecchia_tab():
    src = _leggi("w816_test.py")
    assert all(t not in src for t in _vietati())


class TestDemoUiKeysRegression:
    """Regressione sweep chiavi demo vs UI: ogni chiave
    _def815[...] letta dalla UI deve esistere nel dict demo."""

    def test_ui_keys_subset_demo_keys(self):
        src = _leggi("w816_ui.py")
        usate = set(re.findall(r'_def815\["([^"]+)"\]', src))
        assert usate
        assert len(usate) == 19
        assert usate <= set(mh815_demo().keys())
