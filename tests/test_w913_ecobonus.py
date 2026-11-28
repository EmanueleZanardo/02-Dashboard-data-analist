"""Test nuova scheda Ecobonus: quanto
vale davvero lo sconto fiscale sul
retrofit energetico?
Repo path: tests/test_w913_ecobonus.py

Effetto ECONOMICO: un intervento di
retrofit energetico costa un CAPEX
e produce ogni anno un risparmio in
bolletta meno i costi di gestione
(OPEX): il margine annuo. Lo Stato
riconosce una detrazione fiscale
pari a una aliquota del CAPEX
(Ecobonus, qui fino al 110 per
cento): il credito di imposta si
incassa in quote annuali costanti
per un numero di anni di
detrazione, oppure si cede a un
terzo con uno sconto (haircut) e si
incassa subito il credito meno lo
sconto. In modalita diretta il
beneficio fiscale e il valore
attuale delle quote annuali; in
modalita cessione il beneficio
fiscale e l'incasso immediato al
netto dell'haircut. Il costo netto
e il CAPEX meno il beneficio
fiscale: e quanto resta davvero a
carico di chi investe dopo lo
sconto fiscale. Il VAN e meno
costo netto piu margine per
l'annualita a tasso dato sulla vita
utile; il VAN senza detrazione e
meno CAPEX piu margine per
l'annualita, cioe quanto varrebbe
lo stesso intervento senza nessuno
sconto fiscale. La TIR e il tasso
che azzera il VAN a costo netto
fissato al tasso inserito
(bisezione); il payback e il primo
anno in cui il cumulato del
margine raggiunge il costo netto.
Il breakeven aliquota e l'aliquota
che azzera il VAN nella modalita
selezionata (formula chiusa); il
breakeven risparmio e il risparmio
annuo che azzera il VAN a costo
netto dato (costo netto diviso
annualita piu OPEX). La CO2
evitata e kWh annui per fattore
CO2 diviso 1000 in t/anno.
Demo: CAPEX 60.000 EUR, aliquota
65 per cento, anni detrazione 10,
modalita diretta, haircut 10 per
cento, tasso 0,05, risparmio 4.500
EUR/anno, OPEX 200 EUR/anno, vita
20 anni, kWh 18.000 kWh/anno,
fattore CO2 0,25 kg/kWh,
tolleranza 0,10. Credito = 60.000
per 65 diviso 100 = 39.000 EUR.
Detrazione annua = 39.000 diviso
10 = 3.900 EUR. VA detrazione =
3.900 per 7,7217349292 = 30.114,77
EUR. Incasso cessione = 39.000 per
0,9 = 35.100 EUR. Beneficio
fiscale (diretta) = 30.114,77 EUR.
Costo netto = 60.000 meno
30.114,77 = 29.885,23 EUR. Margine
annuo = 4.500 meno 200 = 4.300
EUR. Annualita 20 anni al 5 per
cento = 12,4622103425. VAN = meno
29.885,23 piu 4.300 per
12,4622103425 = 23.702,27 EUR.
VAN senza detrazione = meno 60.000
piu 4.300 per 12,4622103425 =
meno 6.412,50 EUR (CORREZIONE:
nessuna, il brief attendeva
meno 6.412,50 e il ricalcolo
indipendente conferma). TIR =
13,18 per cento. Payback = 7 anni
(cumulato anno 6 = 25.800 sotto
costo netto, anno 7 = 30.100 sopra
costo netto; frazionale 6,95
anni). Breakeven aliquota =
13,84 per cento. Breakeven
risparmio = 2.598,07 EUR/anno
(CORREZIONE: il brief attendeva
2.598,12, il ricalcolo
indipendente da 2.598,07). CO2
evitata = 18.000 per 0,25 diviso
1000 = 4,5 t/anno. Verdetto
CONVIENTE.
Scenari: base CAPEX 60.000,
aliquota 65, credito 39.000, VA
detrazione 30.114,77, costo netto
29.885,23, margine 4.300, VAN
23.702,27, TIR 13,18 per cento,
payback 7 anni, breakeven aliquota
13,84, breakeven risparmio
2.598,07, CONVIENTE; aliquota 50
per cento (credito 30.000, VA
detrazione 23.165,20, costo netto
36.834,80, VAN 16.752,71,
CORREZIONE: il brief attendeva
16.752,70, il ricalcolo
indipendente da 16.752,71, TIR
9,91 per cento, payback 9 anni,
CONVIENTE); aliquota 110 per cento
(credito 66.000, VA detrazione
50.963,45, costo netto 9.036,55,
VAN 44.550,96, CORREZIONE: il
brief attendeva 44.550,95, il
ricalcolo indipendente da
44.550,96, TIR 47,56 per cento,
payback 3 anni, CONVIENTE);
cessione haircut 10 per cento
(incasso 35.100, costo netto
24.900, VAN 28.687,50, TIR 16,45
per cento, payback 6 anni,
breakeven aliquota 11,87,
CONVIENTE); risparmio meno 20 per
cento (risparmio 3.600, margine
3.400, VAN 12.486,28, TIR 9,54 per
cento, payback 9 anni, breakeven
aliquota 38,05, CONVIENTE); tasso
8 per cento (VA detrazione
26.169,32, costo netto 33.830,68,
VAN 8.387,35, TIR 11,19 per cento,
payback 8 anni, breakeven aliquota
44,17, CONVIENTE).
Confronto: credito 39.000 contro
detrazione annua 3.900, VA
detrazione 30.114,77 contro
incasso cessione 35.100,
beneficio fiscale 30.114,77 contro
costo netto 29.885,23, margine
4.300 contro VAN 23.702,27, VAN
senza detrazione meno 6.412,50
contro TIR 13,18 per cento,
payback 7 anni contro breakeven
aliquota 13,84, breakeven
risparmio 2.598,07 contro CO2 4,5
t/anno.
Tolleranza in FRAZIONE (0,10 = 10 %
del CAPEX), usata diretta, NON
divisa per 100. Credito, quote
annuali e margine medi annui
costanti, SEMPLIFICAZIONE
DICHIARATA (la detrazione si
incassa in quote annuali costanti;
la cessione e incasso immediato al
netto dell'haircut); i flussi sono
solo sugli anni di vita utile,
SEMPLIFICAZIONE DICHIARATA. La CO2
evitata e kWh per fattore CO2
diviso 1000, SEMPLIFICAZIONE
DICHIARATA (il fattore 0,25
dipende da fonte, ora e stagione).
La TIR azzera il VAN a costo netto
fissato al tasso inserito (il
costo netto non viene ricalcolato
al variare del tasso, come il
CAPEX resta fisso nella TIR della
scheda precedente).
Verdetto principale: CONVIENTE.
Verdetto: NON_CALCOLABILE se il
margine annuo e zero o negativo
oppure se un input e degenere
(CAPEX negativo, aliquota negativa
o sopra 110, anni detrazione minori
o uguali a 0 o non interi, modalita
diversa da diretta e cessione,
haircut negativo o sopra 100,
tasso negativo, risparmio
negativo, OPEX negativo, vita
negativa o non intera, kWh
negativi, fattore CO2 negativo,
tolleranza negativa o sopra 1);
altrimenti CONVIENTE se il VAN e
maggiore di 0, MARGINALE se il VAN
e minore o uguale a 0 e il suo
valore assoluto e minore o uguale
a tolleranza per CAPEX,
NON_CONVIENTE altrimenti.
La vita zero NON e degenere: da
VAN meno costo netto, TIR None,
payback None e verdetto
NON_CONVIENTE (NOTA: il brief del
ciclo elencava la vita minore o
uguale a zero tra i degeneri ma
elencava anche la vita zero tra i
casi limite con VAN meno costo
netto e verdetto NON_CONVIENTE:
prevale il caso limite concreto,
come la durata zero della scheda precedente,
e la vita negativa resta degenere).
Gli anni detrazione zero SONO
degeneri: divisione per zero nella
detrazione annua. Il CAPEX zero
NON e degenere: da credito zero,
beneficio zero, costo netto zero,
VAN positivo, TIR None, payback 0
e verdetto CONVIENTE. L'aliquota
zero NON e degenere: da credito
zero e VAN meno 6.412,50 con
verdetto NON_CONVIENTE.
Casi limite: aliquota zero (VAN
meno 6.412,50, NON_CONVIENTE);
CAPEX zero (VAN 53.587,50, TIR
None, payback 0, CONVIENTE);
risparmio zero (margine meno 200,
VAN meno 32.377,68,
NON_CALCOLABILE); vita zero (VAN
meno 29.885,23, TIR None, payback
None, NON_CONVIENTE); tasso zero
(VA detrazione 39.000, costo netto
21.000, VAN 65.000, CONVIENTE);
anni detrazione 1 (VA detrazione
37.142,86, costo netto 22.857,14,
VAN 30.730,36, CONVIENTE);
cessione haircut 100 per cento
(incasso zero, VAN meno 6.412,50,
NON_CONVIENTE); cessione haircut
zero (incasso 39.000, costo netto
21.000, VAN 32.587,50, CONVIENTE).
Distinzione esplicita: qui SOLO il
MECCANISMO FISCALE (detrazione in
quote annuali oppure cessione del
credito con haircut) sullo stesso
CAPEX di un retrofit energetico,
NIENTE fisica del retrofit (le tab
di cappotto, NZEB e pompa di calore
coprono il risparmio fisico in kWh
e in EUR: qui il risparmio annuo in
EUR e un input, e si valuta quanto
vale lo sconto fiscale su quel
CAPEX), NIENTE Conto Termico
(contributo in conto capitale
erogato dal GSE, non una
detrazione fiscale: qui il
beneficio e una detrazione o una
cessione del credito), NIENTE TEE
(titolo negoziabile sul mercato,
non una detrazione fiscale: la
tab906 copre i Certificati Bianchi;
qui il beneficio e fiscale, non un
titolo).
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w913_helpers import (
        demo_calcoli,
        mh908_aliquota,
        mh908_annuity,
        mh908_be_aliquota,
        mh908_be_risparmio,
        mh908_beneficio,
        mh908_calcola,
        mh908_co2,
        mh908_confronto,
        mh908_costo_netto,
        mh908_credito,
        mh908_csv,
        mh908_demo,
        mh908_demo_calcoli,
        mh908_detrazione_annua,
        mh908_durata,
        mh908_fraz,
        mh908_haircut,
        mh908_incasso_cessione,
        mh908_intero,
        mh908_intero_pos,
        mh908_margine,
        mh908_modalita,
        mh908_nneg,
        mh908_num,
        mh908_payback,
        mh908_payback_fraz,
        mh908_pos,
        mh908_scenario,
        mh908_sensibilita,
        mh908_tir,
        mh908_va_detrazione,
        mh908_valida,
        mh908_van,
        mh908_van_senza_detrazione,
        mh908_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w913_helpers", os.path.join(_hf, "w913_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh908_aliquota = _mod.mh908_aliquota
    mh908_annuity = _mod.mh908_annuity
    mh908_be_aliquota = _mod.mh908_be_aliquota
    mh908_be_risparmio = _mod.mh908_be_risparmio
    mh908_beneficio = _mod.mh908_beneficio
    mh908_calcola = _mod.mh908_calcola
    mh908_co2 = _mod.mh908_co2
    mh908_confronto = _mod.mh908_confronto
    mh908_costo_netto = _mod.mh908_costo_netto
    mh908_credito = _mod.mh908_credito
    mh908_csv = _mod.mh908_csv
    mh908_demo = _mod.mh908_demo
    mh908_demo_calcoli = _mod.mh908_demo_calcoli
    mh908_detrazione_annua = _mod.mh908_detrazione_annua
    mh908_durata = _mod.mh908_durata
    mh908_fraz = _mod.mh908_fraz
    mh908_haircut = _mod.mh908_haircut
    mh908_incasso_cessione = _mod.mh908_incasso_cessione
    mh908_intero = _mod.mh908_intero
    mh908_intero_pos = _mod.mh908_intero_pos
    mh908_margine = _mod.mh908_margine
    mh908_modalita = _mod.mh908_modalita
    mh908_nneg = _mod.mh908_nneg
    mh908_num = _mod.mh908_num
    mh908_payback = _mod.mh908_payback
    mh908_payback_fraz = _mod.mh908_payback_fraz
    mh908_pos = _mod.mh908_pos
    mh908_scenario = _mod.mh908_scenario
    mh908_sensibilita = _mod.mh908_sensibilita
    mh908_tir = _mod.mh908_tir
    mh908_va_detrazione = _mod.mh908_va_detrazione
    mh908_valida = _mod.mh908_valida
    mh908_van = _mod.mh908_van
    mh908_van_senza_detrazione = _mod.mh908_van_senza_detrazione
    mh908_verdetto = _mod.mh908_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w913_helpers.py")
_UI_PATH = _risolvi("w913_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh90" + "7"
_VECCHIO_TAB = "tab90" + "7"
_VECCHIO_ST = "st90" + "7_"
_VECCHIO_SIGLA = "uv" + "am"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO_SCALARI = {
    "credito_eur": 39000.0,
    "detrazione_annua_eur": 3900.0,
    "va_detrazione_eur": 30114.76622382079,
    "incasso_cessione_eur": 35100.0,
    "beneficio_fiscale_eur": 30114.76622382079,
    "costo_netto_eur": 29885.23377617921,
    "margine_eur_anno": 4300.0,
    "van_eur": 23702.270696742755,
    "van_senza_detrazione_eur": -6412.495527078034,
    "tir_frazione": 0.1317852825501411,
    "payback_anni": 7,
    "payback_fraz_anni": 6.950054366553305,
    "be_aliquota_pct": 13.840791795035543,
    "be_risparmio_eur_anno": 2598.0684769992527,
    "co2_t_anno": 4.5,
    "verdetto": "CONVIENTE",
}

_DEMO_INPUT = {
    "capex_eur": 60000.0,
    "aliquota_pct": 65.0,
    "anni_detr": 10,
    "modalita": "diretta",
    "haircut_pct": 10.0,
    "tasso_frazione": 0.05,
    "risparmio_eur_anno": 4500.0,
    "opex_eur_anno": 200.0,
    "vita_anni": 20,
    "kwh_anno": 18000.0,
    "fattore_co2_t_kwh": 0.25,
    "tol_frazione": 0.10,
}

_DEMO_SCENARI = [
    {"nome": "Base",
     "capex_eur": 60000.0, "aliquota_pct": 65.0,
     "anni_detr": 10, "modalita": "diretta",
     "haircut_pct": 10.0, "tasso_frazione": 0.05,
     "risparmio_eur_anno": 4500.0, "opex_eur_anno": 200.0,
     "vita_anni": 20, "kwh_anno": 18000.0,
     "fattore_co2_t_kwh": 0.25, "tol_frazione": 0.10,
     "credito_eur": 39000.0, "detrazione_annua_eur": 3900.0,
     "va_detrazione_eur": 30114.76622382079,
     "incasso_cessione_eur": 35100.0,
     "beneficio_fiscale_eur": 30114.76622382079,
     "costo_netto_eur": 29885.23377617921,
     "margine_eur_anno": 4300.0,
     "van_eur": 23702.270696742755,
     "van_senza_detrazione_eur": -6412.495527078034,
     "tir_frazione": 0.1317852825501411,
     "payback_anni": 7,
     "payback_fraz_anni": 6.950054366553305,
     "be_aliquota_pct": 13.840791795035543,
     "be_risparmio_eur_anno": 2598.0684769992527,
     "co2_t_anno": 4.5, "verdetto": "CONVIENTE"},
    {"nome": "Aliquota 50 %",
     "capex_eur": 60000.0, "aliquota_pct": 50.0,
     "anni_detr": 10, "modalita": "diretta",
     "haircut_pct": 10.0, "tasso_frazione": 0.05,
     "risparmio_eur_anno": 4500.0, "opex_eur_anno": 200.0,
     "vita_anni": 20, "kwh_anno": 18000.0,
     "fattore_co2_t_kwh": 0.25, "tol_frazione": 0.10,
     "credito_eur": 30000.0, "detrazione_annua_eur": 3000.0,
     "va_detrazione_eur": 23165.204787554452,
     "incasso_cessione_eur": 27000.0,
     "beneficio_fiscale_eur": 23165.204787554452,
     "costo_netto_eur": 36834.79521244555,
     "margine_eur_anno": 4300.0,
     "van_eur": 16752.70926047642,
     "van_senza_detrazione_eur": -6412.495527078034,
     "tir_frazione": 0.09909818857500197,
     "payback_anni": 9,
     "payback_fraz_anni": 8.566231444754779,
     "be_aliquota_pct": 13.840791795035543,
     "be_risparmio_eur_anno": 3155.71926648592,
     "co2_t_anno": 4.5, "verdetto": "CONVIENTE"},
    {"nome": "Aliquota 110 %",
     "capex_eur": 60000.0, "aliquota_pct": 110.0,
     "anni_detr": 10, "modalita": "diretta",
     "haircut_pct": 10.0, "tasso_frazione": 0.05,
     "risparmio_eur_anno": 4500.0, "opex_eur_anno": 200.0,
     "vita_anni": 20, "kwh_anno": 18000.0,
     "fattore_co2_t_kwh": 0.25, "tol_frazione": 0.10,
     "credito_eur": 66000.0, "detrazione_annua_eur": 6600.0,
     "va_detrazione_eur": 50963.4505326198,
     "incasso_cessione_eur": 59400.0,
     "beneficio_fiscale_eur": 50963.4505326198,
     "costo_netto_eur": 9036.549467380202,
     "margine_eur_anno": 4300.0,
     "van_eur": 44550.955005541764,
     "van_senza_detrazione_eur": -6412.495527078034,
     "tir_frazione": 0.4756468191600367,
     "payback_anni": 3,
     "payback_fraz_anni": 2.101523131948884,
     "be_aliquota_pct": 13.840791795035543,
     "be_risparmio_eur_anno": 925.1161085392508,
     "co2_t_anno": 4.5, "verdetto": "CONVIENTE"},
    {"nome": "Cessione haircut 10 %",
     "capex_eur": 60000.0, "aliquota_pct": 65.0,
     "anni_detr": 10, "modalita": "cessione",
     "haircut_pct": 10.0, "tasso_frazione": 0.05,
     "risparmio_eur_anno": 4500.0, "opex_eur_anno": 200.0,
     "vita_anni": 20, "kwh_anno": 18000.0,
     "fattore_co2_t_kwh": 0.25, "tol_frazione": 0.10,
     "credito_eur": 39000.0, "detrazione_annua_eur": 3900.0,
     "va_detrazione_eur": 30114.76622382079,
     "incasso_cessione_eur": 35100.0,
     "beneficio_fiscale_eur": 35100.0,
     "costo_netto_eur": 24900.0,
     "margine_eur_anno": 4300.0,
     "van_eur": 28687.504472921966,
     "van_senza_detrazione_eur": -6412.495527078034,
     "tir_frazione": 0.1644746074928003,
     "payback_anni": 6,
     "payback_fraz_anni": 5.790697674418604,
     "be_aliquota_pct": 11.874991716811175,
     "be_risparmio_eur_anno": 2198.040421048213,
     "co2_t_anno": 4.5, "verdetto": "CONVIENTE"},
    {"nome": "Risparmio meno 20 %",
     "capex_eur": 60000.0, "aliquota_pct": 65.0,
     "anni_detr": 10, "modalita": "diretta",
     "haircut_pct": 10.0, "tasso_frazione": 0.05,
     "risparmio_eur_anno": 3600.0, "opex_eur_anno": 200.0,
     "vita_anni": 20, "kwh_anno": 18000.0,
     "fattore_co2_t_kwh": 0.25, "tol_frazione": 0.10,
     "credito_eur": 39000.0, "detrazione_annua_eur": 3900.0,
     "va_detrazione_eur": 30114.76622382079,
     "incasso_cessione_eur": 35100.0,
     "beneficio_fiscale_eur": 30114.76622382079,
     "costo_netto_eur": 29885.23377617921,
     "margine_eur_anno": 3400.0,
     "van_eur": 12486.281388456762,
     "van_senza_detrazione_eur": -17628.484835364026,
     "tir_frazione": 0.09536862260115209,
     "payback_anni": 9,
     "payback_fraz_anni": 8.789774640052709,
     "be_aliquota_pct": 38.04949059814693,
     "be_risparmio_eur_anno": 2598.0684769992527,
     "co2_t_anno": 4.5, "verdetto": "CONVIENTE"},
    {"nome": "Tasso 8 %",
     "capex_eur": 60000.0, "aliquota_pct": 65.0,
     "anni_detr": 10, "modalita": "diretta",
     "haircut_pct": 10.0, "tasso_frazione": 0.08,
     "risparmio_eur_anno": 4500.0, "opex_eur_anno": 200.0,
     "vita_anni": 20, "kwh_anno": 18000.0,
     "fattore_co2_t_kwh": 0.25, "tol_frazione": 0.10,
     "credito_eur": 39000.0, "detrazione_annua_eur": 3900.0,
     "va_detrazione_eur": 26169.317455871646,
     "incasso_cessione_eur": 35100.0,
     "beneficio_fiscale_eur": 26169.317455871646,
     "costo_netto_eur": 33830.68254412836,
     "margine_eur_anno": 4300.0,
     "van_eur": 8387.351307903606,
     "van_senza_detrazione_eur": -17781.966147968036,
     "tir_frazione": 0.11185664713296944,
     "payback_anni": 8,
     "payback_fraz_anni": 7.867600591657758,
     "be_aliquota_pct": 44.16728871767298,
     "be_risparmio_eur_anno": 3645.729743114277,
     "co2_t_anno": 4.5, "verdetto": "CONVIENTE"},
]

_DEMO_CONFRONTO = {
    "credito_eur": 39000.0,
    "detrazione_annua_eur": 3900.0,
    "va_detrazione_eur": 30114.76622382079,
    "incasso_cessione_eur": 35100.0,
    "beneficio_fiscale_eur": 30114.76622382079,
    "costo_netto_eur": 29885.23377617921,
    "margine_eur_anno": 4300.0,
    "van_eur": 23702.270696742755,
    "van_senza_detrazione_eur": -6412.495527078034,
    "tir_frazione": 0.1317852825501411,
    "payback_anni": 7,
    "payback_fraz_anni": 6.950054366553305,
    "be_aliquota_pct": 13.840791795035543,
    "be_risparmio_eur_anno": 2598.0684769992527,
    "co2_t_anno": 4.5,
    "verdetto": "CONVIENTE",
}

_ORDINE_VALIDA = (
    "capex_eur", "aliquota_pct", "anni_detr", "modalita",
    "haircut_pct", "tasso_frazione", "risparmio_eur_anno",
    "opex_eur_anno", "vita_anni", "kwh_anno",
    "fattore_co2_t_kwh", "tol_frazione")


def _demo_kwargs(**over):
    kw = dict(mh908_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh908_num(3, "x"), 3.0)
        self.assertEqual(mh908_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh908_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh908_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh908_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh908_pos(0, "x")
        with self.assertRaises(ValueError):
            mh908_pos(-1, "x")
        self.assertEqual(mh908_pos(3, "x"), 3.0)

    def test_fraz_bordi(self):
        self.assertEqual(mh908_fraz(0, "x"), 0.0)
        self.assertEqual(mh908_fraz(1, "x"), 1.0)
        self.assertEqual(mh908_fraz(0.10, "x"), 0.10)
        with self.assertRaises(ValueError):
            mh908_fraz(-0.01, "x")
        with self.assertRaises(ValueError):
            mh908_fraz(1.01, "x")

    def test_durata_bordi(self):
        self.assertEqual(mh908_durata(0, "x"), 0)
        self.assertEqual(mh908_durata(20, "x"), 20)
        self.assertEqual(mh908_durata(20.0, "x"), 20)
        with self.assertRaises(ValueError):
            mh908_durata(-1, "x")
        with self.assertRaises(ValueError):
            mh908_durata(2.5, "x")
        with self.assertRaises(ValueError):
            mh908_durata(float("nan"), "x")

    def test_intero_bordi(self):
        self.assertEqual(mh908_intero(0, "x"), 0)
        self.assertEqual(mh908_intero(10, "x"), 10)
        self.assertEqual(mh908_intero(10.0, "x"), 10)
        with self.assertRaises(ValueError):
            mh908_intero(-1, "x")
        with self.assertRaises(ValueError):
            mh908_intero(2.5, "x")
        with self.assertRaises(ValueError):
            mh908_intero(float("nan"), "x")

    def test_intero_pos_bordi(self):
        self.assertEqual(mh908_intero_pos(1, "x"), 1)
        self.assertEqual(mh908_intero_pos(10, "x"), 10)
        self.assertEqual(mh908_intero_pos(10.0, "x"), 10)
        with self.assertRaises(ValueError):
            mh908_intero_pos(0, "x")
        with self.assertRaises(ValueError):
            mh908_intero_pos(-1, "x")
        with self.assertRaises(ValueError):
            mh908_intero_pos(2.5, "x")

    def test_aliquota_bordi(self):
        self.assertEqual(mh908_aliquota(0, "x"), 0.0)
        self.assertEqual(mh908_aliquota(65, "x"), 65.0)
        self.assertEqual(mh908_aliquota(110, "x"), 110.0)
        with self.assertRaises(ValueError):
            mh908_aliquota(-0.1, "x")
        with self.assertRaises(ValueError):
            mh908_aliquota(110.1, "x")

    def test_haircut_bordi(self):
        self.assertEqual(mh908_haircut(0, "x"), 0.0)
        self.assertEqual(mh908_haircut(10, "x"), 10.0)
        self.assertEqual(mh908_haircut(100, "x"), 100.0)
        with self.assertRaises(ValueError):
            mh908_haircut(-0.1, "x")
        with self.assertRaises(ValueError):
            mh908_haircut(100.1, "x")

    def test_modalita_bordi(self):
        self.assertEqual(mh908_modalita("diretta"), "diretta")
        self.assertEqual(mh908_modalita("cessione"), "cessione")
        for cattivo in ("Diretta", "sconto", "", None, 1, True):
            with self.assertRaises(ValueError):
                mh908_modalita(cattivo)


class TestFisica(unittest.TestCase):
    def test_credito(self):
        self.assertEqual(mh908_credito(60000.0, 65.0), 39000.0)
        self.assertEqual(mh908_credito(60000.0, 50.0), 30000.0)
        self.assertEqual(mh908_credito(60000.0, 110.0), 66000.0)
        self.assertEqual(mh908_credito(60000.0, 0.0), 0.0)
        self.assertEqual(mh908_credito(0.0, 65.0), 0.0)
        with self.assertRaises(ValueError):
            mh908_credito(-1.0, 65.0)
        with self.assertRaises(ValueError):
            mh908_credito(60000.0, 111.0)
        with self.assertRaises(ValueError):
            mh908_credito(60000.0, -1.0)

    def test_detrazione_annua(self):
        self.assertEqual(mh908_detrazione_annua(39000.0, 10),
                         3900.0)
        self.assertEqual(mh908_detrazione_annua(39000.0, 1),
                         39000.0)
        self.assertEqual(mh908_detrazione_annua(30000.0, 10),
                         3000.0)
        self.assertEqual(mh908_detrazione_annua(0.0, 10), 0.0)
        with self.assertRaises(ValueError):
            mh908_detrazione_annua(39000.0, 0)
        with self.assertRaises(ValueError):
            mh908_detrazione_annua(39000.0, -1)
        with self.assertRaises(ValueError):
            mh908_detrazione_annua(39000.0, 2.5)
        with self.assertRaises(ValueError):
            mh908_detrazione_annua(-1.0, 10)

    def test_va_detrazione(self):
        self.assertAlmostEqual(
            mh908_va_detrazione(3900.0, 0.05, 10),
            30114.76622382079, places=2)
        self.assertAlmostEqual(
            mh908_va_detrazione(3900.0, 0.0, 10),
            39000.0, places=2)
        self.assertAlmostEqual(
            mh908_va_detrazione(39000.0, 0.05, 1),
            37142.85714285718, places=2)
        self.assertAlmostEqual(
            mh908_va_detrazione(3900.0, 0.08, 10),
            26169.317455871646, places=2)
        self.assertAlmostEqual(
            mh908_va_detrazione(3000.0, 0.05, 10),
            23165.204787554452, places=2)
        self.assertEqual(mh908_va_detrazione(0.0, 0.05, 10),
                         0.0)

    def test_incasso_cessione(self):
        self.assertEqual(
            mh908_incasso_cessione(39000.0, 10.0), 35100.0)
        self.assertEqual(
            mh908_incasso_cessione(39000.0, 0.0), 39000.0)
        self.assertEqual(
            mh908_incasso_cessione(39000.0, 100.0), 0.0)
        self.assertEqual(
            mh908_incasso_cessione(30000.0, 10.0), 27000.0)
        self.assertEqual(
            mh908_incasso_cessione(39000.0, 30.0), 27300.0)
        with self.assertRaises(ValueError):
            mh908_incasso_cessione(39000.0, 101.0)
        with self.assertRaises(ValueError):
            mh908_incasso_cessione(-1.0, 10.0)

    def test_beneficio(self):
        self.assertAlmostEqual(
            mh908_beneficio("diretta", 30114.76622382079,
                            35100.0),
            30114.76622382079, places=2)
        self.assertEqual(
            mh908_beneficio("cessione", 30114.76622382079,
                            35100.0),
            35100.0)
        self.assertEqual(
            mh908_beneficio("cessione", 30114.76622382079, 0.0),
            0.0)
        self.assertEqual(
            mh908_beneficio("cessione", 30114.76622382079,
                            39000.0),
            39000.0)
        with self.assertRaises(ValueError):
            mh908_beneficio("sconto", 30114.77, 35100.0)

    def test_costo_netto(self):
        self.assertAlmostEqual(
            mh908_costo_netto(60000.0, 30114.76622382079),
            29885.23377617921, places=2)
        self.assertEqual(mh908_costo_netto(60000.0, 35100.0),
                         24900.0)
        self.assertEqual(mh908_costo_netto(60000.0, 39000.0),
                         21000.0)
        self.assertEqual(mh908_costo_netto(60000.0, 0.0),
                         60000.0)
        self.assertEqual(mh908_costo_netto(0.0, 0.0), 0.0)
        with self.assertRaises(ValueError):
            mh908_costo_netto(-1.0, 30114.77)

    def test_margine(self):
        self.assertEqual(mh908_margine(4500.0, 200.0), 4300.0)
        self.assertEqual(mh908_margine(3600.0, 200.0), 3400.0)
        self.assertEqual(mh908_margine(0.0, 200.0), -200.0)
        self.assertEqual(mh908_margine(4500.0, 0.0), 4500.0)
        self.assertEqual(mh908_margine(6000.0, 200.0), 5800.0)
        with self.assertRaises(ValueError):
            mh908_margine(-1.0, 200.0)
        with self.assertRaises(ValueError):
            mh908_margine(4500.0, -1.0)

    def test_annuity(self):
        self.assertAlmostEqual(mh908_annuity(20, 0.05),
                               12.462210342539992, places=9)
        self.assertAlmostEqual(mh908_annuity(10, 0.05),
                               7.721734929184818, places=9)
        self.assertAlmostEqual(mh908_annuity(20, 0.08),
                               9.818147407449294, places=9)
        self.assertAlmostEqual(mh908_annuity(10, 0.08),
                               6.710081398941448, places=9)
        self.assertEqual(mh908_annuity(20, 0.0), 20.0)
        self.assertEqual(mh908_annuity(0, 0.05), 0.0)
        self.assertEqual(mh908_annuity(0, 0.0), 0.0)
        self.assertAlmostEqual(mh908_annuity(1, 0.05),
                               0.9523809523809523, places=9)
        with self.assertRaises(ValueError):
            mh908_annuity(-1, 0.05)
        with self.assertRaises(ValueError):
            mh908_annuity(2.5, 0.05)

    def test_van(self):
        self.assertAlmostEqual(
            mh908_van(29885.23377617921, 4300.0, 20, 0.05),
            23702.270696742755, places=2)
        self.assertAlmostEqual(
            mh908_van(24900.0, 4300.0, 20, 0.05),
            28687.504472921966, places=2)
        self.assertAlmostEqual(
            mh908_van(60000.0, 4300.0, 20, 0.05),
            -6412.495527078034, places=2)
        self.assertEqual(mh908_van(29885.23377617921, 4300.0, 0,
                                   0.05),
                         -29885.23377617921)
        self.assertAlmostEqual(
            mh908_van(0.0, 4300.0, 20, 0.05),
            53587.504472921966, places=2)
        self.assertAlmostEqual(
            mh908_van(21000.0, 4300.0, 20, 0.0),
            65000.0, places=2)
        self.assertAlmostEqual(
            mh908_van(29885.23377617921, -200.0, 20, 0.05),
            -32377.67584468721, places=2)

    def test_van_senza_detrazione(self):
        self.assertAlmostEqual(
            mh908_van_senza_detrazione(60000.0, 4300.0, 20,
                                       0.05),
            -6412.495527078034, places=2)
        self.assertAlmostEqual(
            mh908_van_senza_detrazione(0.0, 4300.0, 20, 0.05),
            53587.504472921966, places=2)
        self.assertAlmostEqual(
            mh908_van_senza_detrazione(60000.0, 4300.0, 20,
                                       0.0),
            26000.0, places=2)
        self.assertEqual(
            mh908_van_senza_detrazione(60000.0, 4300.0, 0,
                                       0.05),
            -60000.0)
        # Il VAN con detrazione meno il VAN senza
        # detrazione e il valore attuale della
        # detrazione.
        self.assertAlmostEqual(
            mh908_van(29885.23377617921, 4300.0, 20, 0.05)
            - mh908_van_senza_detrazione(60000.0, 4300.0, 20,
                                         0.05),
            30114.76622382079, places=2)

    def test_tir(self):
        self.assertAlmostEqual(
            mh908_tir(29885.23377617921, 4300.0, 20),
            0.1317852825501411, places=4)
        self.assertAlmostEqual(
            mh908_tir(36834.79521244555, 4300.0, 20),
            0.09909818857500197, places=4)
        self.assertAlmostEqual(
            mh908_tir(9036.549467380202, 4300.0, 20),
            0.4756468191600367, places=4)
        self.assertAlmostEqual(
            mh908_tir(24900.0, 4300.0, 20),
            0.1644746074928003, places=4)
        self.assertAlmostEqual(
            mh908_tir(60000.0, 4300.0, 20),
            0.03704087395185435, places=4)
        self.assertAlmostEqual(
            mh908_tir(21000.0, 4300.0, 20),
            0.1993639485893, places=4)
        self.assertIsNone(mh908_tir(0.0, 4300.0, 20))
        self.assertIsNone(mh908_tir(29885.23377617921, 0.0, 20))
        self.assertIsNone(
            mh908_tir(29885.23377617921, -200.0, 20))
        self.assertIsNone(
            mh908_tir(29885.23377617921, 4300.0, 0))
        # Alla TIR il VAN a costo netto fissato e zero.
        tir = mh908_tir(29885.23377617921, 4300.0, 20)
        self.assertAlmostEqual(
            mh908_van(29885.23377617921, 4300.0, 20, tir),
            0.0, places=2)

    def test_payback(self):
        self.assertEqual(
            mh908_payback(29885.23377617921, 4300.0, 20), 7)
        self.assertEqual(
            mh908_payback(36834.79521244555, 4300.0, 20), 9)
        self.assertEqual(
            mh908_payback(9036.549467380202, 4300.0, 20), 3)
        self.assertEqual(mh908_payback(24900.0, 4300.0, 20), 6)
        self.assertEqual(mh908_payback(60000.0, 4300.0, 20), 14)
        self.assertEqual(mh908_payback(21000.0, 4300.0, 20), 5)
        self.assertEqual(mh908_payback(0.0, 4300.0, 20), 0)
        self.assertIsNone(
            mh908_payback(29885.23377617921, 0.0, 20))
        self.assertIsNone(
            mh908_payback(29885.23377617921, -200.0, 20))
        self.assertIsNone(
            mh908_payback(29885.23377617921, 4300.0, 0))
        # Margine troppo piccolo: mai entro la vita.
        self.assertIsNone(mh908_payback(60000.0, 2000.0, 20))
        self.assertEqual(mh908_payback(60000.0, 2000.0, 30),
                         30)

    def test_payback_fraz(self):
        self.assertAlmostEqual(
            mh908_payback_fraz(29885.23377617921, 4300.0, 20),
            6.950054366553305, places=9)
        self.assertAlmostEqual(
            mh908_payback_fraz(36834.79521244555, 4300.0, 20),
            8.566231444754779, places=9)
        self.assertAlmostEqual(
            mh908_payback_fraz(24900.0, 4300.0, 20),
            5.790697674418604, places=9)
        self.assertAlmostEqual(
            mh908_payback_fraz(60000.0, 4300.0, 20),
            13.953488372093023, places=9)
        self.assertEqual(
            mh908_payback_fraz(0.0, 4300.0, 20), 0.0)
        self.assertIsNone(
            mh908_payback_fraz(29885.23377617921, 0.0, 20))
        self.assertIsNone(
            mh908_payback_fraz(29885.23377617921, -200.0, 20))
        self.assertIsNone(
            mh908_payback_fraz(29885.23377617921, 4300.0, 0))
        # Payback mai raggiunto entro la vita:
        # frazionale None (formula legata a t).
        self.assertIsNone(
            mh908_payback_fraz(60000.0, 2000.0, 20))

    def test_be_aliquota(self):
        self.assertAlmostEqual(
            mh908_be_aliquota("diretta", 60000.0, 4300.0, 20,
                              10, 0.05, 10.0),
            13.840791795035543, places=2)
        self.assertAlmostEqual(
            mh908_be_aliquota("cessione", 60000.0, 4300.0, 20,
                              10, 0.05, 10.0),
            11.874991716811175, places=2)
        self.assertAlmostEqual(
            mh908_be_aliquota("diretta", 60000.0, 3400.0, 20,
                              10, 0.05, 10.0),
            38.04949059814693, places=2)
        self.assertAlmostEqual(
            mh908_be_aliquota("diretta", 60000.0, 4300.0, 20,
                              10, 0.08, 10.0),
            44.16728871767298, places=2)
        self.assertAlmostEqual(
            mh908_be_aliquota("diretta", 60000.0, 4300.0, 20,
                              1, 0.05, 10.0),
            11.221867172386549, places=2)
        self.assertAlmostEqual(
            mh908_be_aliquota("cessione", 60000.0, 4300.0, 20,
                              10, 0.05, 0.0),
            10.687492545130057, places=2)
        self.assertAlmostEqual(
            mh908_be_aliquota("cessione", 60000.0, 4300.0, 20,
                              10, 0.05, 30.0),
            15.267846493042939, places=2)
        # VAN ad aliquota zero gia positivo: 0,0.
        self.assertEqual(
            mh908_be_aliquota("diretta", 60000.0, 4300.0, 20,
                              10, 0.0, 10.0),
            0.0)
        self.assertEqual(
            mh908_be_aliquota("diretta", 0.0, 4300.0, 20,
                              10, 0.05, 10.0),
            0.0)
        # Nemmeno ad aliquota 110 il VAN diventa
        # positivo: None.
        self.assertIsNone(
            mh908_be_aliquota("diretta", 60000.0, -200.0, 20,
                              10, 0.05, 10.0))
        self.assertIsNone(
            mh908_be_aliquota("cessione", 60000.0, 4300.0, 20,
                              10, 0.05, 100.0))
        with self.assertRaises(ValueError):
            mh908_be_aliquota("sconto", 60000.0, 4300.0, 20,
                              10, 0.05, 10.0)
        with self.assertRaises(ValueError):
            mh908_be_aliquota("diretta", -1.0, 4300.0, 20,
                              10, 0.05, 10.0)
        # All'aliquota di breakeven il VAN e zero.
        be = mh908_be_aliquota("diretta", 60000.0, 4300.0, 20,
                               10, 0.05, 10.0)
        bc = mh908_calcola(**_demo_kwargs(aliquota_pct=be))
        self.assertAlmostEqual(bc["van_eur"], 0.0, places=2)
        be = mh908_be_aliquota("cessione", 60000.0, 4300.0, 20,
                               10, 0.05, 10.0)
        bc = mh908_calcola(**_demo_kwargs(modalita="cessione",
                                          aliquota_pct=be))
        self.assertAlmostEqual(bc["van_eur"], 0.0, places=2)

    def test_be_aliquota_invariante_aliquota_corrente(self):
        # Il breakeven aliquota e INVARIANTE
        # all'aliquota corrente.
        bc0 = demo_calcoli()
        bc = mh908_calcola(**_demo_kwargs(aliquota_pct=50.0))
        self.assertEqual(bc["be_aliquota_pct"],
                         bc0["be_aliquota_pct"])
        self.assertAlmostEqual(bc["be_aliquota_pct"], 13.84,
                               places=2)

    def test_be_risparmio(self):
        self.assertAlmostEqual(
            mh908_be_risparmio(29885.23377617921, 0.05, 20,
                               200.0),
            2598.0684769992527, places=2)
        self.assertAlmostEqual(
            mh908_be_risparmio(36834.79521244555, 0.05, 20,
                               200.0),
            3155.71926648592, places=2)
        self.assertAlmostEqual(
            mh908_be_risparmio(9036.549467380202, 0.05, 20,
                               200.0),
            925.1161085392508, places=2)
        self.assertAlmostEqual(
            mh908_be_risparmio(24900.0, 0.05, 20, 200.0),
            2198.040421048213, places=2)
        self.assertAlmostEqual(
            mh908_be_risparmio(60000.0, 0.05, 20, 200.0),
            5014.555231441477, places=2)
        self.assertEqual(
            mh908_be_risparmio(0.0, 0.05, 20, 200.0), 200.0)
        self.assertEqual(
            mh908_be_risparmio(21000.0, 0.0, 20, 200.0),
            1250.0)
        self.assertIsNone(
            mh908_be_risparmio(29885.23377617921, 0.05, 0,
                               200.0))
        with self.assertRaises(ValueError):
            mh908_be_risparmio(29885.23377617921, 0.05, -1,
                               200.0)
        # Al risparmio di breakeven il VAN e zero.
        be = mh908_be_risparmio(29885.23377617921, 0.05, 20,
                                200.0)
        bc = mh908_calcola(
            **_demo_kwargs(risparmio_eur_anno=be))
        self.assertAlmostEqual(bc["van_eur"], 0.0, places=2)

    def test_be_risparmio_invariante_risparmio_corrente(self):
        # Il breakeven risparmio e INVARIANTE
        # al risparmio corrente.
        bc0 = demo_calcoli()
        bc = mh908_calcola(
            **_demo_kwargs(risparmio_eur_anno=3600.0))
        self.assertEqual(bc["be_risparmio_eur_anno"],
                         bc0["be_risparmio_eur_anno"])
        self.assertAlmostEqual(
            bc["be_risparmio_eur_anno"], 2598.07, places=2)

    def test_co2(self):
        self.assertEqual(mh908_co2(18000.0, 0.25), 4.5)
        self.assertEqual(mh908_co2(0.0, 0.25), 0.0)
        self.assertEqual(mh908_co2(18000.0, 0.0), 0.0)
        self.assertEqual(mh908_co2(36000.0, 0.25), 9.0)
        self.assertEqual(mh908_co2(1000.0, 0.25), 0.25)
        with self.assertRaises(ValueError):
            mh908_co2(-1.0, 0.25)
        with self.assertRaises(ValueError):
            mh908_co2(18000.0, -0.1)

    def test_scenario_singolo(self):
        s = mh908_scenario("Aliquota 50 %", mh908_demo(),
                           {"aliquota_pct": 50.0})
        self.assertEqual(s["nome"], "Aliquota 50 %")
        self.assertEqual(s["aliquota_pct"], 50.0)
        self.assertAlmostEqual(s["van_eur"], 16752.71,
                               places=2)
        self.assertEqual(s["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["be_aliquota_pct"], 13.84,
                               places=2)
        s = mh908_scenario("Aliquota 110 %", mh908_demo(),
                           {"aliquota_pct": 110.0})
        self.assertAlmostEqual(s["van_eur"], 44550.96,
                               places=2)
        self.assertEqual(s["payback_anni"], 3)
        self.assertEqual(s["verdetto"], "CONVIENTE")
        s = mh908_scenario("Cessione haircut 10 %",
                           mh908_demo(),
                           {"modalita": "cessione"})
        self.assertAlmostEqual(s["incasso_cessione_eur"],
                               35100.0, places=9)
        self.assertAlmostEqual(s["van_eur"], 28687.50,
                               places=2)
        self.assertAlmostEqual(s["be_aliquota_pct"], 11.87,
                               places=2)
        s = mh908_scenario("Risparmio meno 20 %",
                           mh908_demo(),
                           {"risparmio_eur_anno": 3600.0})
        self.assertAlmostEqual(s["van_eur"], 12486.28,
                               places=2)
        self.assertAlmostEqual(s["be_aliquota_pct"], 38.05,
                               places=2)
        s = mh908_scenario("Tasso 8 %", mh908_demo(),
                           {"tasso_frazione": 0.08})
        self.assertAlmostEqual(s["van_eur"], 8387.35,
                               places=2)
        self.assertEqual(s["verdetto"], "CONVIENTE")
        with self.assertRaises(ValueError):
            mh908_scenario("", mh908_demo(),
                           {"aliquota_pct": 50.0})
        with self.assertRaises(ValueError):
            mh908_scenario("X", mh908_demo(),
                           {"vita_anni": -1})

    def test_scenario_cessione_haircut_100(self):
        s = mh908_scenario("Cessione haircut 100 %",
                           mh908_demo(),
                           {"modalita": "cessione",
                            "haircut_pct": 100.0})
        self.assertEqual(s["incasso_cessione_eur"], 0.0)
        self.assertEqual(s["beneficio_fiscale_eur"], 0.0)
        self.assertEqual(s["costo_netto_eur"], 60000.0)
        self.assertIsNone(s["be_aliquota_pct"])
        self.assertEqual(s["verdetto"], "NON_CONVIENTE")

    def test_confronto_formule(self):
        c = mh908_confronto(39000.0, 3900.0, 30114.76622382079,
                            35100.0, 30114.76622382079,
                            29885.23377617921, 4300.0,
                            23702.270696742755,
                            -6412.495527078034,
                            0.1317852825501411, 7,
                            6.950054366553305,
                            13.840791795035543,
                            2598.0684769992527, 4.5,
                            "CONVIENTE")
        self.assertEqual(c["credito_eur"], 39000.0)
        self.assertEqual(c["detrazione_annua_eur"], 3900.0)
        self.assertEqual(c["va_detrazione_eur"],
                         30114.76622382079)
        self.assertEqual(c["incasso_cessione_eur"], 35100.0)
        self.assertEqual(c["beneficio_fiscale_eur"],
                         30114.76622382079)
        self.assertEqual(c["costo_netto_eur"],
                         29885.23377617921)
        self.assertEqual(c["margine_eur_anno"], 4300.0)
        self.assertEqual(c["van_eur"], 23702.270696742755)
        self.assertEqual(c["van_senza_detrazione_eur"],
                         -6412.495527078034)
        self.assertEqual(c["tir_frazione"],
                         0.1317852825501411)
        self.assertEqual(c["payback_anni"], 7)
        self.assertEqual(c["payback_fraz_anni"],
                         6.950054366553305)
        self.assertEqual(c["be_aliquota_pct"],
                         13.840791795035543)
        self.assertEqual(c["be_risparmio_eur_anno"],
                         2598.0684769992527)
        self.assertEqual(c["co2_t_anno"], 4.5)
        self.assertEqual(c["verdetto"], "CONVIENTE")
        c = mh908_confronto(0.0, 0.0, 0.0, 0.0, 0.0, 60000.0,
                            4300.0, -6412.495527078034,
                            -6412.495527078034,
                            0.03704087395185435, 14,
                            13.953488372093023,
                            13.840791795035543,
                            5014.555231441477, 4.5,
                            "NON_CONVIENTE")
        self.assertEqual(c["tir_frazione"],
                         0.03704087395185435)
        self.assertEqual(c["payback_anni"], 14)
        self.assertEqual(c["verdetto"], "NON_CONVIENTE")
        with self.assertRaises(ValueError):
            mh908_confronto(39000.0, 3900.0,
                            30114.76622382079, 35100.0,
                            30114.76622382079,
                            29885.23377617921, 4300.0,
                            23702.270696742755,
                            -6412.495527078034,
                            0.1317852825501411, 7,
                            6.950054366553305,
                            13.840791795035543,
                            2598.0684769992527, 4.5,
                            "FORSE")
        with self.assertRaises(ValueError):
            mh908_confronto(39000.0, 3900.0,
                            30114.76622382079, 35100.0,
                            30114.76622382079,
                            29885.23377617921, 4300.0,
                            23702.270696742755,
                            -6412.495527078034,
                            0.1317852825501411, 7,
                            6.950054366553305,
                            13.840791795035543,
                            2598.0684769992527, -1.0,
                            "CONVIENTE")


class TestFinanza(unittest.TestCase):
    def test_verdetto_bordi(self):
        self.assertEqual(
            mh908_verdetto(100.0, 0.10, 60000.0, 4300.0),
            "CONVIENTE")
        self.assertEqual(
            mh908_verdetto(0.0, 0.10, 60000.0, 4300.0),
            "MARGINALE")
        self.assertEqual(
            mh908_verdetto(-6000.0, 0.10, 60000.0, 4300.0),
            "MARGINALE")
        self.assertEqual(
            mh908_verdetto(-6001.0, 0.10, 60000.0, 4300.0),
            "NON_CONVIENTE")
        self.assertEqual(
            mh908_verdetto(-6412.50, 0.10, 60000.0, 4300.0),
            "NON_CONVIENTE")
        # Con tolleranza zero ogni VAN negativo
        # e NON_CONVIENTE (VAN zero compreso nel
        # MARGINALE solo perche il valore assoluto
        # zero e minore o uguale a zero).
        self.assertEqual(
            mh908_verdetto(-1.0, 0.0, 60000.0, 4300.0),
            "NON_CONVIENTE")
        self.assertEqual(
            mh908_verdetto(0.0, 0.0, 60000.0, 4300.0),
            "MARGINALE")
        with self.assertRaises(ValueError):
            mh908_verdetto(100.0, 1.5, 60000.0, 4300.0)
        with self.assertRaises(ValueError):
            mh908_verdetto(100.0, 0.10, -1.0, 4300.0)

    def test_verdetto_none_non_calcolabile(self):
        self.assertEqual(
            mh908_verdetto(None, 0.10, 60000.0, 4300.0),
            "NON_CALCOLABILE")
        self.assertEqual(
            mh908_verdetto(None, 0.0, 0.0, 4300.0),
            "NON_CALCOLABILE")
        self.assertEqual(
            mh908_verdetto(100.0, 0.10, 60000.0, None),
            "NON_CALCOLABILE")

    def test_verdetto_margine_zero_negativo_non_calcolabile(self):
        self.assertEqual(
            mh908_verdetto(-29885.23, 0.10, 60000.0, 0.0),
            "NON_CALCOLABILE")
        self.assertEqual(
            mh908_verdetto(-32377.68, 0.10, 60000.0, -200.0),
            "NON_CALCOLABILE")
        self.assertEqual(
            mh908_verdetto(23702.27, 0.10, 60000.0, 4300.0),
            "CONVIENTE")

    def test_verdetto_capex_zero(self):
        # Con CAPEX zero la tolleranza non copre
        # nulla: ogni VAN negativo e NON_CONVIENTE.
        self.assertEqual(
            mh908_verdetto(-1.0, 0.10, 0.0, 4300.0),
            "NON_CONVIENTE")
        self.assertEqual(
            mh908_verdetto(0.0, 0.10, 0.0, 4300.0),
            "MARGINALE")

    def test_valida_demo_ok(self):
        demo = mh908_demo()
        val = mh908_valida(*[demo[k] for k in _ORDINE_VALIDA])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_anni_detr_zero_no_uno_ok(self):
        with self.assertRaises(ValueError):
            mh908_calcola(**_demo_kwargs(anni_detr=0))
        with self.assertRaises(ValueError):
            mh908_calcola(**_demo_kwargs(anni_detr=2.5))
        bc = mh908_calcola(**_demo_kwargs(anni_detr=1))
        self.assertEqual(bc["anni_detr"], 1)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_valida_vita_zero_ammesso_negativa_no(self):
        demo = mh908_demo()
        val = mh908_valida(*[dict(demo, vita_anni=0)[k]
                             for k in _ORDINE_VALIDA])
        self.assertTrue(val["valido"])
        bc = mh908_calcola(**_demo_kwargs(vita_anni=0))
        self.assertEqual(bc["vita_anni"], 0)
        self.assertAlmostEqual(bc["van_eur"], -29885.23,
                               places=2)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        with self.assertRaises(ValueError):
            mh908_calcola(**_demo_kwargs(vita_anni=-1))
        with self.assertRaises(ValueError):
            mh908_calcola(**_demo_kwargs(vita_anni=2.5))

    def test_valida_aliquota_sopra_110_no(self):
        with self.assertRaises(ValueError):
            mh908_calcola(**_demo_kwargs(aliquota_pct=111.0))
        bc = mh908_calcola(**_demo_kwargs(aliquota_pct=110.0))
        self.assertEqual(bc["aliquota_pct"], 110.0)
        bc = mh908_calcola(**_demo_kwargs(aliquota_pct=0.0))
        self.assertEqual(bc["aliquota_pct"], 0.0)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_valida_haircut_sopra_100_no(self):
        with self.assertRaises(ValueError):
            mh908_calcola(**_demo_kwargs(haircut_pct=101.0))
        bc = mh908_calcola(
            **_demo_kwargs(modalita="cessione",
                           haircut_pct=100.0))
        self.assertEqual(bc["haircut_pct"], 100.0)
        self.assertEqual(bc["incasso_cessione_eur"], 0.0)

    def test_valida_modalita(self):
        with self.assertRaises(ValueError):
            mh908_calcola(**_demo_kwargs(modalita="sconto"))
        with self.assertRaises(ValueError):
            mh908_calcola(**_demo_kwargs(modalita=1))
        bc = mh908_calcola(**_demo_kwargs(modalita="cessione"))
        self.assertEqual(bc["modalita"], "cessione")
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_valida_tasso_negativo_no_senza_tetto(self):
        with self.assertRaises(ValueError):
            mh908_calcola(**_demo_kwargs(tasso_frazione=-0.1))
        bc = mh908_calcola(**_demo_kwargs(tasso_frazione=0.0))
        self.assertEqual(bc["tasso_frazione"], 0.0)
        # Il brief pone come degenere solo il
        # tasso negativo: nessun tetto superiore
        # negli helper (il tetto 0,20 e solo
        # dello slider UI).
        bc = mh908_calcola(**_demo_kwargs(tasso_frazione=1.5))
        self.assertEqual(bc["tasso_frazione"], 1.5)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_valida_tolleranza_sopra_uno_no(self):
        with self.assertRaises(ValueError):
            mh908_calcola(**_demo_kwargs(tol_frazione=1.5))
        bc = mh908_calcola(**_demo_kwargs(tol_frazione=0.0))
        self.assertEqual(bc["tol_frazione"], 0.0)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(aliquota_pct=float("nan"))
        self.assertRaises(ValueError, mh908_calcola, **kw)
        kw = _demo_kwargs(tol_frazione=float("inf"))
        self.assertRaises(ValueError, mh908_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (
                ("capex_eur", -1),
                ("aliquota_pct", -1),
                ("haircut_pct", -1),
                ("tasso_frazione", -0.1),
                ("risparmio_eur_anno", -1),
                ("opex_eur_anno", -1),
                ("kwh_anno", -1),
                ("fattore_co2_t_kwh", -0.1),
                ("tol_frazione", -0.1)):
            with self.assertRaises(ValueError):
                mh908_calcola(**_demo_kwargs(**{campo: valore}))

    def test_valida_non_interi_no(self):
        with self.assertRaises(ValueError):
            mh908_calcola(**_demo_kwargs(anni_detr=2.5))
        with self.assertRaises(ValueError):
            mh908_calcola(**_demo_kwargs(vita_anni=2.5))

    def test_calcola_accetta_dict(self):
        bc = mh908_calcola(mh908_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(len(bc["scenari"]), 6)

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh908_calcola(dict(mh908_demo(),
                                aliquota_pct=999.0),
                           aliquota_pct=65.0)
        self.assertEqual(bc["aliquota_pct"], 65.0)

    def test_calcola_senza_scenari_anti_ricorsione(self):
        bc = mh908_calcola(_scenari=False, **mh908_demo())
        self.assertEqual(bc["scenari"], [])
        self.assertIsNone(bc["scenario_base"])
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(bc["van_eur"], 23702.27,
                               places=2)
        self.assertAlmostEqual(bc["be_aliquota_pct"], 13.84,
                               places=2)


class TestDemoCalcoli(unittest.TestCase):
    def test_demo_calcoli_vs_demo_scalari(self):
        bc = demo_calcoli()
        for chiave, atteso in _DEMO_SCALARI.items():
            with self.subTest(chiave=chiave):
                ottenuto = bc[chiave]
                if atteso is None or isinstance(atteso, (int, str)):
                    self.assertEqual(ottenuto, atteso)
                else:
                    self.assertLess(_rel(ottenuto, atteso), 1e-9)

    def test_demo_input_vs_attesi(self):
        bc = demo_calcoli()
        for chiave, atteso in _DEMO_INPUT.items():
            with self.subTest(chiave=chiave):
                self.assertEqual(bc[chiave], atteso)

    def test_demo_scenari(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["scenari"]), len(_DEMO_SCENARI))
        for i, atteso in enumerate(_DEMO_SCENARI):
            for chiave, valore in atteso.items():
                with self.subTest(scenario=i, chiave=chiave):
                    ottenuto = bc["scenari"][i][chiave]
                    if valore is None or isinstance(valore, (int, str)):
                        self.assertEqual(ottenuto, valore)
                    else:
                        self.assertLess(_rel(ottenuto, valore), 1e-9)

    def test_demo_confronto(self):
        bc = demo_calcoli()
        for chiave, valore in _DEMO_CONFRONTO.items():
            with self.subTest(chiave=chiave):
                ottenuto = bc["confronto"][chiave]
                if valore is None or isinstance(valore, (int, str)):
                    self.assertEqual(ottenuto, valore)
                else:
                    self.assertLess(_rel(ottenuto, valore), 1e-9)

    def test_demo_verdetto_principale(self):
        bc = demo_calcoli()
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertGreater(bc["van_eur"], 0.0)
        self.assertAlmostEqual(bc["tir_frazione"], 0.1318,
                               places=4)
        self.assertAlmostEqual(bc["be_aliquota_pct"], 13.84,
                               places=2)
        self.assertAlmostEqual(bc["be_risparmio_eur_anno"],
                               2598.07, places=2)
        self.assertEqual(bc["scenario_base"]["verdetto"],
                         "CONVIENTE")
        self.assertEqual(bc["payback_anni"], 7)
        self.assertAlmostEqual(bc["co2_t_anno"], 4.5,
                               places=2)
        # Senza detrazione lo stesso intervento
        # non converrebbe: lo sconto fiscale
        # ribalta il segno del VAN.
        self.assertLess(bc["van_senza_detrazione_eur"], 0.0)
        self.assertAlmostEqual(
            bc["van_senza_detrazione_eur"], -6412.50,
            places=2)

    def test_coerenza_fisica_e_costi(self):
        bc = demo_calcoli()
        self.assertAlmostEqual(
            bc["credito_eur"],
            bc["capex_eur"] * bc["aliquota_pct"] / 100.0)
        self.assertAlmostEqual(
            bc["detrazione_annua_eur"],
            bc["credito_eur"] / bc["anni_detr"])
        self.assertAlmostEqual(
            bc["va_detrazione_eur"],
            bc["detrazione_annua_eur"]
            * mh908_annuity(bc["anni_detr"],
                            bc["tasso_frazione"]))
        self.assertAlmostEqual(
            bc["incasso_cessione_eur"],
            bc["credito_eur"]
            * (1.0 - bc["haircut_pct"] / 100.0))
        self.assertAlmostEqual(
            bc["beneficio_fiscale_eur"],
            bc["va_detrazione_eur"])
        self.assertAlmostEqual(
            bc["costo_netto_eur"],
            bc["capex_eur"] - bc["beneficio_fiscale_eur"])
        self.assertAlmostEqual(
            bc["margine_eur_anno"],
            bc["risparmio_eur_anno"] - bc["opex_eur_anno"])
        self.assertAlmostEqual(
            bc["van_eur"],
            -bc["costo_netto_eur"] + bc["margine_eur_anno"]
            * mh908_annuity(bc["vita_anni"],
                            bc["tasso_frazione"]))
        self.assertAlmostEqual(
            bc["van_senza_detrazione_eur"],
            -bc["capex_eur"] + bc["margine_eur_anno"]
            * mh908_annuity(bc["vita_anni"],
                            bc["tasso_frazione"]))
        self.assertAlmostEqual(
            bc["be_risparmio_eur_anno"],
            bc["costo_netto_eur"]
            / mh908_annuity(bc["vita_anni"],
                            bc["tasso_frazione"])
            + bc["opex_eur_anno"])
        self.assertAlmostEqual(
            bc["co2_t_anno"],
            bc["kwh_anno"] * bc["fattore_co2_t_kwh"]
            / 1000.0)
        self.assertAlmostEqual(
            bc["payback_fraz_anni"],
            6.0 + (bc["costo_netto_eur"] - 6.0
                   * bc["margine_eur_anno"])
            / bc["margine_eur_anno"])
        conf = bc["confronto"]
        self.assertEqual(conf["van_eur"], bc["van_eur"])
        self.assertEqual(conf["tir_frazione"],
                         bc["tir_frazione"])
        self.assertEqual(conf["payback_anni"],
                         bc["payback_anni"])
        self.assertEqual(conf["verdetto"], bc["verdetto"])
        # Flussi: anno zero meno costo netto, poi
        # margine per ogni anno di vita utile; il
        # cumulato supera il costo netto al
        # settimo anno.
        fl = bc["df_flussi"]
        self.assertEqual(len(fl), 21)
        self.assertAlmostEqual(fl["Flusso (EUR)"].iloc[0],
                               -29885.23, places=2)
        self.assertEqual(fl["Flusso (EUR)"].iloc[1], 4300.0)
        self.assertAlmostEqual(
            fl["Cumulato (EUR)"].iloc[6], -4085.23, places=2)
        self.assertAlmostEqual(
            fl["Cumulato (EUR)"].iloc[7], 214.77, places=2)
        self.assertAlmostEqual(
            fl["Cumulato (EUR)"].iloc[20], 56114.77, places=2)
        # Beneficio contro costo: credito e
        # beneficio positivi, VAN senza
        # detrazione negativo, VAN positivo.
        bf = bc["df_beneficio_costo"]
        self.assertEqual(len(bf), 5)
        self.assertAlmostEqual(
            bf["Valore"].iloc[0], 39000.0, places=2)
        self.assertAlmostEqual(
            bf["Valore"].iloc[1], 30114.77, places=2)
        self.assertAlmostEqual(
            bf["Valore"].iloc[2], 29885.23, places=2)
        self.assertAlmostEqual(
            bf["Valore"].iloc[3], 23702.27, places=2)
        self.assertAlmostEqual(
            bf["Valore"].iloc[4], -6412.50, places=2)

    def test_scenari_ordinamento_e_invarianza(self):
        bc = demo_calcoli()
        base = bc["scenari"][0]
        # Piu aliquota migliora il caso e resta
        # CONVIENTE; il breakeven aliquota e
        # INVARIANTE all'aliquota corrente.
        self.assertGreater(
            bc["scenari"][2]["van_eur"], base["van_eur"])
        self.assertGreater(bc["scenari"][2]["van_eur"], 0.0)
        self.assertEqual(bc["scenari"][2]["verdetto"],
                         "CONVIENTE")
        self.assertEqual(
            bc["scenari"][2]["be_aliquota_pct"],
            base["be_aliquota_pct"])
        # Meno aliquota peggiora il caso ma resta
        # CONVIENTE, con payback piu lungo.
        self.assertLess(bc["scenari"][1]["van_eur"],
                        base["van_eur"])
        self.assertGreater(bc["scenari"][1]["van_eur"], 0.0)
        self.assertEqual(bc["scenari"][1]["verdetto"],
                         "CONVIENTE")
        self.assertEqual(bc["scenari"][1]["payback_anni"], 9)
        self.assertEqual(
            bc["scenari"][1]["be_aliquota_pct"],
            base["be_aliquota_pct"])
        # Cessione: incasso immediato vale piu
        # delle quote attualizzate al 5 per cento.
        self.assertGreater(bc["scenari"][3]["van_eur"],
                           base["van_eur"])
        self.assertEqual(bc["scenari"][3]["payback_anni"], 6)
        self.assertAlmostEqual(
            bc["scenari"][3]["be_aliquota_pct"], 11.87,
            places=2)
        # Risparmio meno 20 per cento: margine
        # piu basso ma caso ancora CONVIENTE.
        self.assertAlmostEqual(
            bc["scenari"][4]["margine_eur_anno"],
            3400.0, places=2)
        self.assertLess(bc["scenari"][4]["van_eur"],
                        base["van_eur"])
        self.assertEqual(bc["scenari"][4]["verdetto"],
                         "CONVIENTE")
        self.assertEqual(bc["scenari"][4]["payback_anni"], 9)
        # Tasso 8 per cento: VA detrazione piu
        # bassa ma caso ancora CONVIENTE.
        self.assertAlmostEqual(
            bc["scenari"][5]["va_detrazione_eur"],
            26169.32, places=2)
        self.assertLess(bc["scenari"][5]["van_eur"],
                        base["van_eur"])
        self.assertEqual(bc["scenari"][5]["verdetto"],
                         "CONVIENTE")
        self.assertEqual(bc["scenari"][5]["payback_anni"], 8)

    def test_sensibilita_valori(self):
        s = mh908_sensibilita(**mh908_demo())
        self.assertEqual(set(s.keys()),
                         {"aliq50", "aliq110", "cessione",
                          "risp_meno20", "tasso8", "aliq0",
                          "capex0", "risp0", "vita0", "tasso0",
                          "anni1", "cess_h100", "cess_h0",
                          "cess_h30", "opex0", "kwh0", "tol0",
                          "fatt0", "vita30", "risp6000",
                          "aliq80"})
        attesi = {
            "aliq50": (16752.71, 9.91, 9, 13.84, 3155.72,
                       "CONVIENTE"),
            "aliq110": (44550.96, 47.56, 3, 13.84, 925.12,
                        "CONVIENTE"),
            "cessione": (28687.50, 16.45, 6, 11.87, 2198.04,
                         "CONVIENTE"),
            "risp_meno20": (12486.28, 9.54, 9, 38.05, 2598.07,
                            "CONVIENTE"),
            "tasso8": (8387.35, 11.19, 8, 44.17, 3645.73,
                       "CONVIENTE"),
            "aliq0": (-6412.50, 3.70, 14, 13.84, 5014.56,
                      "NON_CONVIENTE"),
            "capex0": (53587.50, None, 0, 0.0, 200.0,
                       "CONVIENTE"),
            "risp0": (-32377.68, None, None, None, 2598.07,
                      "NON_CALCOLABILE"),
            "vita0": (-29885.23, None, None, None, None,
                      "NON_CONVIENTE"),
            "tasso0": (65000.0, 19.94, 5, 0.0, 1250.0,
                       "CONVIENTE"),
            "anni1": (30730.36, 18.14, 6, 11.22, 2034.12,
                      "CONVIENTE"),
            "cess_h100": (-6412.50, 3.70, 14, None, 5014.56,
                          "NON_CONVIENTE"),
            "cess_h0": (32587.50, 19.94, 5, 10.69, 1885.09,
                        "CONVIENTE"),
            "cess_h30": (20887.50, 11.72, 8, 15.27, 2823.93,
                         "CONVIENTE"),
            "opex0": (26194.71, 13.95, 7, 8.46, 2398.07,
                      "CONVIENTE"),
            "kwh0": (23702.27, 13.18, 7, 13.84, 2598.07,
                     "CONVIENTE"),
            "tol0": (23702.27, 13.18, 7, 13.84, 2598.07,
                     "CONVIENTE"),
            "fatt0": (23702.27, 13.18, 7, 13.84, 2598.07,
                      "CONVIENTE"),
            "vita30": (36216.31, 14.11, 7, 0.0, 2144.08,
                       "CONVIENTE"),
            "risp6000": (42395.59, 18.79, 6, 0.0, 2598.07,
                         "CONVIENTE"),
            "aliq80": (30651.83, 18.07, 6, 13.84, 2040.42,
                       "CONVIENTE"),
        }
        for nome, (van, tirp, pb, ba, br, vdc) in attesi.items():
            with self.subTest(variante=nome):
                self.assertAlmostEqual(s[nome]["van_eur"], van,
                                       places=2)
                if tirp is None:
                    self.assertIsNone(s[nome]["tir_frazione"])
                else:
                    self.assertAlmostEqual(
                        s[nome]["tir_frazione"] * 100.0, tirp,
                        places=2)
                self.assertEqual(s[nome]["payback_anni"], pb)
                if ba is None:
                    self.assertIsNone(
                        s[nome]["be_aliquota_pct"])
                else:
                    self.assertAlmostEqual(
                        s[nome]["be_aliquota_pct"],
                        ba, places=2)
                if br is None:
                    self.assertIsNone(
                        s[nome]["be_risparmio_eur_anno"])
                else:
                    self.assertAlmostEqual(
                        s[nome]["be_risparmio_eur_anno"],
                        br, places=2)
                self.assertEqual(s[nome]["verdetto"], vdc)
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van_eur", caso)
            self.assertIn("tir_frazione", caso)
            self.assertIn("payback_anni", caso)
            self.assertIn("confronto", caso)
            self.assertIn("scenari", caso)


class TestCasiLimite(unittest.TestCase):
    def test_aliquota_zero_non_conviente(self):
        bc = mh908_calcola(**_demo_kwargs(aliquota_pct=0.0))
        self.assertEqual(bc["credito_eur"], 0.0)
        self.assertEqual(bc["detrazione_annua_eur"], 0.0)
        self.assertEqual(bc["va_detrazione_eur"], 0.0)
        self.assertEqual(bc["beneficio_fiscale_eur"], 0.0)
        self.assertEqual(bc["costo_netto_eur"], 60000.0)
        self.assertEqual(bc["margine_eur_anno"], 4300.0)
        self.assertAlmostEqual(bc["van_eur"], -6412.50,
                               places=2)
        self.assertEqual(bc["van_eur"],
                         bc["van_senza_detrazione_eur"])
        self.assertAlmostEqual(bc["tir_frazione"], 0.0370,
                               places=4)
        self.assertEqual(bc["payback_anni"], 14)
        self.assertAlmostEqual(bc["payback_fraz_anni"], 13.95,
                               places=2)
        self.assertAlmostEqual(bc["be_aliquota_pct"], 13.84,
                               places=2)
        self.assertAlmostEqual(bc["be_risparmio_eur_anno"],
                               5014.56, places=2)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_capex_zero_conviente_payback_zero(self):
        bc = mh908_calcola(**_demo_kwargs(capex_eur=0.0))
        self.assertEqual(bc["credito_eur"], 0.0)
        self.assertEqual(bc["beneficio_fiscale_eur"], 0.0)
        self.assertEqual(bc["costo_netto_eur"], 0.0)
        self.assertEqual(bc["margine_eur_anno"], 4300.0)
        self.assertAlmostEqual(bc["van_eur"], 53587.50,
                               places=2)
        self.assertIsNone(bc["tir_frazione"])
        self.assertEqual(bc["payback_anni"], 0)
        self.assertEqual(bc["payback_fraz_anni"], 0.0)
        self.assertEqual(bc["be_aliquota_pct"], 0.0)
        self.assertAlmostEqual(bc["be_risparmio_eur_anno"],
                               200.0, places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_risparmio_zero_non_calcolabile(self):
        bc = mh908_calcola(
            **_demo_kwargs(risparmio_eur_anno=0.0))
        self.assertEqual(bc["margine_eur_anno"], -200.0)
        self.assertAlmostEqual(bc["van_eur"], -32377.68,
                               places=2)
        self.assertIsNone(bc["tir_frazione"])
        self.assertIsNone(bc["payback_anni"])
        self.assertIsNone(bc["payback_fraz_anni"])
        self.assertIsNone(bc["be_aliquota_pct"])
        self.assertAlmostEqual(bc["be_risparmio_eur_anno"],
                               2598.07, places=2)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_vita_zero_non_conviente(self):
        bc = mh908_calcola(**_demo_kwargs(vita_anni=0))
        self.assertEqual(bc["margine_eur_anno"], 4300.0)
        self.assertAlmostEqual(bc["van_eur"], -29885.23,
                               places=2)
        self.assertEqual(bc["van_senza_detrazione_eur"],
                         -60000.0)
        self.assertIsNone(bc["tir_frazione"])
        self.assertIsNone(bc["payback_anni"])
        self.assertIsNone(bc["payback_fraz_anni"])
        self.assertIsNone(bc["be_aliquota_pct"])
        self.assertIsNone(bc["be_risparmio_eur_anno"])
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertEqual(len(bc["df_flussi"]), 1)

    def test_tasso_zero_conviente(self):
        bc = mh908_calcola(**_demo_kwargs(tasso_frazione=0.0))
        self.assertEqual(bc["va_detrazione_eur"], 39000.0)
        self.assertEqual(bc["costo_netto_eur"], 21000.0)
        self.assertAlmostEqual(bc["van_eur"], 65000.0,
                               places=2)
        self.assertAlmostEqual(bc["van_senza_detrazione_eur"],
                               26000.0, places=2)
        self.assertAlmostEqual(bc["tir_frazione"], 0.1994,
                               places=4)
        self.assertEqual(bc["payback_anni"], 5)
        self.assertAlmostEqual(bc["payback_fraz_anni"], 4.88,
                               places=2)
        self.assertEqual(bc["be_aliquota_pct"], 0.0)
        self.assertAlmostEqual(bc["be_risparmio_eur_anno"],
                               1250.0, places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_anni_detr_uno_conviente(self):
        bc = mh908_calcola(**_demo_kwargs(anni_detr=1))
        self.assertEqual(bc["detrazione_annua_eur"], 39000.0)
        self.assertAlmostEqual(bc["va_detrazione_eur"],
                               37142.86, places=2)
        self.assertAlmostEqual(bc["costo_netto_eur"],
                               22857.14, places=2)
        self.assertAlmostEqual(bc["van_eur"], 30730.36,
                               places=2)
        self.assertAlmostEqual(bc["tir_frazione"], 0.1814,
                               places=4)
        self.assertEqual(bc["payback_anni"], 6)
        self.assertAlmostEqual(bc["payback_fraz_anni"], 5.32,
                               places=2)
        self.assertAlmostEqual(bc["be_aliquota_pct"], 11.22,
                               places=2)
        self.assertAlmostEqual(bc["be_risparmio_eur_anno"],
                               2034.12, places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_cessione_haircut_100_non_conviente(self):
        bc = mh908_calcola(
            **_demo_kwargs(modalita="cessione",
                           haircut_pct=100.0))
        self.assertEqual(bc["incasso_cessione_eur"], 0.0)
        self.assertEqual(bc["beneficio_fiscale_eur"], 0.0)
        self.assertEqual(bc["costo_netto_eur"], 60000.0)
        self.assertAlmostEqual(bc["van_eur"], -6412.50,
                               places=2)
        self.assertAlmostEqual(bc["tir_frazione"], 0.0370,
                               places=4)
        self.assertEqual(bc["payback_anni"], 14)
        self.assertIsNone(bc["be_aliquota_pct"])
        self.assertAlmostEqual(bc["be_risparmio_eur_anno"],
                               5014.56, places=2)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_cessione_haircut_zero_conviente(self):
        bc = mh908_calcola(
            **_demo_kwargs(modalita="cessione",
                           haircut_pct=0.0))
        self.assertEqual(bc["incasso_cessione_eur"], 39000.0)
        self.assertEqual(bc["beneficio_fiscale_eur"], 39000.0)
        self.assertEqual(bc["costo_netto_eur"], 21000.0)
        self.assertAlmostEqual(bc["van_eur"], 32587.50,
                               places=2)
        self.assertAlmostEqual(bc["tir_frazione"], 0.1994,
                               places=4)
        self.assertEqual(bc["payback_anni"], 5)
        self.assertAlmostEqual(bc["be_aliquota_pct"], 10.69,
                               places=2)
        self.assertAlmostEqual(bc["be_risparmio_eur_anno"],
                               1885.09, places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_opex_zero_e_vita_30(self):
        bc = mh908_calcola(**_demo_kwargs(opex_eur_anno=0.0))
        self.assertEqual(bc["margine_eur_anno"], 4500.0)
        self.assertAlmostEqual(bc["van_eur"], 26194.71,
                               places=2)
        self.assertAlmostEqual(bc["be_aliquota_pct"], 8.46,
                               places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh908_calcola(**_demo_kwargs(vita_anni=30))
        self.assertAlmostEqual(bc["van_eur"], 36216.31,
                               places=2)
        self.assertEqual(bc["be_aliquota_pct"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_kwh_zero_e_fattore_zero(self):
        bc = mh908_calcola(**_demo_kwargs(kwh_anno=0.0))
        self.assertEqual(bc["co2_t_anno"], 0.0)
        self.assertAlmostEqual(bc["van_eur"], 23702.27,
                               places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh908_calcola(
            **_demo_kwargs(fattore_co2_t_kwh=0.0))
        self.assertEqual(bc["co2_t_anno"], 0.0)
        self.assertAlmostEqual(bc["van_eur"], 23702.27,
                               places=2)

    def test_tolleranza_zero_demo_resta_conveniente(self):
        # Con VAN positivo la tolleranza non
        # decide nulla: il demo resta CONVIENTE
        # anche a tolleranza zero.
        bc = mh908_calcola(**_demo_kwargs(tol_frazione=0.0))
        self.assertAlmostEqual(bc["van_eur"], 23702.27,
                               places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_van_invarianze(self):
        # Il VAN non dipende dai kWh ne dal
        # fattore CO2: la CO2 non entra
        # nell'economia.
        bc = demo_calcoli()
        bc_c = mh908_calcola(**_demo_kwargs(kwh_anno=0.0))
        self.assertEqual(bc_c["van_eur"], bc["van_eur"])
        self.assertEqual(bc_c["co2_t_anno"], 0.0)
        # Il VAN non dipende dalla tolleranza.
        bc_t = mh908_calcola(**_demo_kwargs(tol_frazione=0.0))
        self.assertEqual(bc_t["van_eur"], bc["van_eur"])
        # Il VAN non dipende dall'haircut in
        # modalita diretta.
        bc_h = mh908_calcola(
            **_demo_kwargs(haircut_pct=50.0))
        self.assertEqual(bc_h["van_eur"], bc["van_eur"])

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh908_csv(bc, mh908_demo())
        for voce in ("capex_eur",
                     "aliquota_pct",
                     "anni_detr",
                     "modalita",
                     "haircut_pct",
                     "tasso_frazione",
                     "risparmio_eur_anno",
                     "opex_eur_anno",
                     "vita_anni",
                     "kwh_anno",
                     "fattore_co2_t_kwh",
                     "tol_frazione",
                     "credito_eur",
                     "detrazione_annua_eur",
                     "va_detrazione_eur",
                     "incasso_cessione_eur",
                     "beneficio_fiscale_eur",
                     "costo_netto_eur",
                     "margine_eur_anno",
                     "van_eur",
                     "van_senza_detrazione_eur",
                     "tir_frazione",
                     "payback_anni",
                     "payback_fraz_anni",
                     "be_aliquota_pct",
                     "be_risparmio_eur_anno",
                     "co2_t_anno",
                     "scenario_base_credito_eur",
                     "scenario_base_van_eur",
                     "scenario_base_verdetto",
                     "scenario_aliq50_van_eur",
                     "scenario_aliq50_verdetto",
                     "scenario_aliq110_van_eur",
                     "scenario_aliq110_verdetto",
                     "scenario_cessione_van_eur",
                     "scenario_cessione_verdetto",
                     "scenario_risp_meno20_van_eur",
                     "scenario_risp_meno20_verdetto",
                     "scenario_tasso8_van_eur",
                     "scenario_tasso8_verdetto",
                     "confronto_credito_eur",
                     "confronto_detrazione_annua_eur",
                     "confronto_va_detrazione_eur",
                     "confronto_incasso_cessione_eur",
                     "confronto_beneficio_fiscale_eur",
                     "confronto_costo_netto_eur",
                     "confronto_margine_eur_anno",
                     "confronto_van_eur",
                     "confronto_van_senza_detrazione_eur",
                     "confronto_tir_frazione",
                     "confronto_payback_anni",
                     "confronto_be_aliquota_pct",
                     "confronto_be_risparmio_eur_anno",
                     "confronto_co2_t_anno",
                     "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)
        self.assertIn("diretta", csv)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh908_csv(bc, mh908_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("capex_eur;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh908_demo_calcoli()["van_eur"],
                         demo_calcoli()["van_eur"])
        self.assertEqual(mh908_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_df_scenari_confronto_tabella_flussi(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_scenari"]), 6)
        self.assertEqual(len(bc["df_confronto"]), 16)
        self.assertEqual(len(bc["df_tabella"]), 28)
        self.assertEqual(len(bc["df_flussi"]), 21)
        self.assertEqual(len(bc["df_beneficio_costo"]), 5)
        self.assertEqual(
            list(bc["df_confronto"]["Voce"]),
            ["Credito (EUR)",
             "Detrazione annua (EUR/anno)",
             "VA detrazione (EUR)",
             "Incasso cessione (EUR)",
             "Beneficio fiscale (EUR)",
             "Costo netto (EUR)",
             "Margine annuo (EUR/anno)",
             "VAN (EUR)",
             "VAN senza detrazione (EUR)",
             "TIR (frazione)",
             "Payback (anni)",
             "Payback frazionale (anni)",
             "Breakeven aliquota (%)",
             "Breakeven risparmio (EUR/anno)",
             "CO2 evitata (t/anno)",
             "Verdetto"])
        self.assertAlmostEqual(
            bc["df_confronto"]["Valore"].iloc[0],
            39000.00, places=2)
        self.assertAlmostEqual(
            bc["df_confronto"]["Valore"].iloc[7],
            23702.27, places=2)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("CAPEX (EUR)", voci)
        self.assertIn("Aliquota (%)", voci)
        self.assertIn("Modalita", voci)
        self.assertIn("Credito (EUR)", voci)
        self.assertIn("Breakeven aliquota (%)", voci)
        self.assertIn("Breakeven risparmio (EUR/anno)", voci)
        self.assertIn("VAN (EUR)", voci)
        self.assertIn("VAN senza detrazione (EUR)", voci)
        self.assertIn("TIR (frazione)", voci)
        self.assertIn("Payback (anni)", voci)
        self.assertIn("CO2 evitata (t/anno)", voci)
        self.assertIn("Verdetto", voci)
        self.assertIn("VAN (EUR)",
                      set(bc["df_scenari"].columns))
        self.assertIn("TIR (%)",
                      set(bc["df_scenari"].columns))
        self.assertIn("Verdetto",
                      set(bc["df_scenari"].columns))
        self.assertIn("Payback (anni)",
                      set(bc["df_scenari"].columns))
        self.assertAlmostEqual(
            bc["df_scenari"]["VAN (EUR)"].iloc[0],
            23702.27, places=2)
        self.assertAlmostEqual(
            bc["df_scenari"]["TIR (%)"].iloc[0],
            13.18, places=2)
        self.assertEqual(
            list(bc["df_flussi"].columns),
            ["Anno", "Flusso (EUR)", "Cumulato (EUR)"])
        self.assertEqual(
            list(bc["df_beneficio_costo"].columns),
            ["Voce", "Valore"])

    def test_valida_rifiuta_stringhe_e_bool(self):
        kw = _demo_kwargs(capex_eur="60000.0")
        self.assertRaises(ValueError, mh908_calcola, **kw)
        kw = _demo_kwargs(capex_eur=True)
        self.assertRaises(ValueError, mh908_calcola, **kw)
        val = mh908_valida(*[kw[k] for k in _ORDINE_VALIDA])
        self.assertFalse(val["valido"])
        kw = _demo_kwargs(modalita=1)
        val = mh908_valida(*[kw[k] for k in _ORDINE_VALIDA])
        self.assertFalse(val["valido"])


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def908\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh908_demo().keys()), lette - set(mh908_demo().keys()))
        self.assertEqual(lette, set(mh908_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc908\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc908\["([^"]+)"\]', src))
        attese = set(mh908_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestConteggioTitoliPreApply(unittest.TestCase):
    def test_conteggio_titoli_pre_apply(self):
        # Conteggio titoli: forma PRE-apply. Prima
        # dell'apply di questa scheda la copia di
        # lavoro del repo ha 907 blocchi scheda;
        # l'apply bumpa questo assert al conteggio
        # post apply 908.
        if os.path.exists(_APP_WD):
            src = open(_APP_WD, encoding="utf-8", errors="ignore").read()
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 910)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab908:"), 1)
        self.assertTrue(src.startswith("    # W913"))

    def test_ui_tab908_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab908:"), 1)
        self.assertIn("def mh908_demo(", src_h)
        self.assertIn("def mh908_calcola(", src_h)
        self.assertIn("tab908", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Ecobonus: quanto vale davvero lo sconto fiscale sul retrofit energetico?", src)
        self.assertIn("🏛️💶 Ecobonus: quanto vale davvero lo sconto fiscale sul retrofit energetico?", src)
        self.assertNotIn(_VECCHIO_TAB, src)

    def test_helpers_senza_streamlit_e_senza_residui_vecchia_tab(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertNotIn(_IMP_STREAMLIT, src)
        self.assertNotIn(_VECCHIO_MH, src)

    def test_helpers_senza_costanti_di_modulo(self):
        src = open(_HELPERS_PATH, encoding="utf-8").read()
        tree = ast.parse(src)
        assegnazioni = [n for n in tree.body if isinstance(n, ast.Assign)]
        self.assertEqual(assegnazioni, [])

    def test_ui_senza_residui_vecchia_tab_e_chiavi_statiche(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertNotIn(_VECCHIO_MH, src)
        self.assertNotIn(_VECCHIO_ST, src)
        chiavi = re.findall(r'key="(st908_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st908_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertEqual(len(chiavi), 19)
        self.assertIn('key="st908_calcola"', src)
        self.assertIn('key="st908_csv"', src)
        self.assertIn('key="st908_csv_scenari"', src)
        self.assertIn('key="st908_modalita"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg908"), src.index(".paiac("))
        self.assertIn("st.stop()", src)

    def test_ui_tutti_gli_slider_minimo_zero(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        for m in re.finditer(r"st\.slider\(", src):
            finestra = src[m.start():m.start() + 400]
            self.assertIn("min_value=0", finestra)

    def test_ui_nessun_trattino_lungo(self):
        # Il titolo prescritto della scheda
        # contiene un trattino lungo nella riga
        # h1: quella riga e' esclusa dal controllo,
        # tutto il resto deve esserne privo.
        for percorso in (_HELPERS_PATH, _UI_PATH):
            src = open(percorso, encoding="utf-8").read()
            righe = [r for r in src.split("\n") if "<h1>" not in r]
            testo = "\n".join(righe)
            self.assertNotIn(chr(8212), testo)
            self.assertNotIn(chr(8211), testo)

    def test_ui_nessun_trattino_nelle_stringhe_mostrate(self):
        # Display string: nessun trattino lungo e
        # nessun meno ASCII dentro i letterali stringa
        # di UI e helper, salvo il nome del codec
        # "utf-8" (non e' testo mostrato) e salvo la
        # riga h1 col titolo prescritto (contiene
        # un trattino lungo).
        import textwrap as _tw
        for percorso in (_HELPERS_PATH, _UI_PATH):
            src = open(percorso, encoding="utf-8").read()
            if percorso == _UI_PATH:
                src = _tw.dedent(src)
            tree = ast.parse(src)
            for nodo in ast.walk(tree):
                if isinstance(nodo, ast.Constant) and isinstance(nodo.value, str):
                    if nodo.value == "utf-8":
                        continue
                    if "<h1>" in nodo.value:
                        continue
                    self.assertNotIn("-", nodo.value)
                    self.assertNotIn(chr(8212), nodo.value)
                    self.assertNotIn(chr(8211), nodo.value)

    def test_ui_nessun_residuo_sigla_vecchia(self):
        # Niente residui della sigla della scheda
        # precedente in helper e UI.
        for percorso in (_HELPERS_PATH, _UI_PATH):
            src = open(percorso, encoding="utf-8").read()
            self.assertNotIn(_VECCHIO_SIGLA, src.lower())
            self.assertNotIn(_VECCHIO_SIGLA.upper(), src)


if __name__ == "__main__":
    unittest.main()
