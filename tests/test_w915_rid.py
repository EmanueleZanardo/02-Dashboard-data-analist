"""Test nuova scheda RID: vendere
l'energia al GSE paga?
Repo path: tests/test_w915_rid.py

Effetto ECONOMICO: un impianto
fotovoltaico immette in rete tutta
l'energia prodotta in kWh/anno,
potenza in kWp per produzione
specifica in kWh/kWp/anno, senza
autoconsumo. Con il Ritiro Dedicato
il GSE ritira l'energia immessa e
riconosce il maggiore tra il prezzo
zonale orario e il prezzo minimo
garantito in EUR/kWh: qui il ricavo
unitario e il maggiore tra il prezzo
zonale medio annuo e il prezzo
minimo garantito, SEMPLIFICAZIONE
DICHIARATA (nel mondo reale il
confronto e orario per orario, qui
si usano i valori medi annui). Il
ricavo lordo e energia immessa per
prezzo unitario. Il GSE trattiene
un corrispettivo per il servizio in
frazione del ricavo lordo: il ricavo
netto e ricavo lordo meno
corrispettivo. I costi annui sono
O&M per kWp: il margine annuo e
ricavo netto meno costi. Il CAPEX e
CAPEX unitario per potenza. Il VAN
e meno CAPEX piu margine per
l'annualita a tasso dato sulla vita
utile; la TIR e il tasso che azzera
il VAN a CAPEX fissato (bisezione);
il payback e il primo anno in cui
il cumulato del margine raggiunge
il CAPEX. Il breakeven prezzo
zonale e il prezzo zonale che
azzera il VAN (formula chiusa,
espresso anche in EUR/MWh); il
breakeven PMG e il prezzo minimo
garantito che azzera il VAN
(formula chiusa). La CO2 evitata e
kWh annui immessi per fattore CO2
diviso 1000 in t/anno.
Demo: potenza 100 kWp, produzione
specifica 1200 kWh/kWp/anno,
prezzo zonale 0,095 EUR/kWh, PMG
0,090 EUR/kWh, corrispettivo GSE
0,005, O&M 20 EUR/kWp/anno, CAPEX
unitario 1100 EUR/kWp, vita 20
anni, tasso 0,05, tolleranza 0,10.
E immessa = 100 per 1200 =
120.000 kWh/anno. CAPEX = 1100
per 100 = 110.000 EUR. Prezzo
unitario = maggiore tra 0,095 e
0,090 = 0,095 EUR/kWh. Ricavo
lordo = 120.000 per 0,095 =
11.400 EUR/anno. Corrispettivo =
11.400 per 0,005 = 57 EUR/anno.
Ricavo netto = 11.400 meno 57 =
11.343 EUR/anno. Costi = 20 per
100 = 2.000 EUR/anno. Margine =
11.343 meno 2.000 = 9.343
EUR/anno. Annualita 20 anni al 5
per cento = 12,4622103425. VAN =
meno 110.000 piu 9.343 per
12,4622103425 = 6.434,43 EUR.
TIR = 5,68 per cento. Payback =
12 anni (cumulato anno 11 =
102.773 sotto CAPEX, anno 12 =
112.116 sopra CAPEX; frazionale
11,77 anni). Breakeven prezzo
zonale = 0,0907 EUR/kWh (90,68
EUR/MWh). Breakeven PMG = 0,0
EUR/kWh (il VAN e gia positivo
con PMG zero). CO2 evitata =
120.000 per 0,25 diviso 1000 =
30 t/anno. Verdetto MARGINALE
(il VAN positivo 6.434,43 resta
sotto il 10 per cento del CAPEX,
quindi MARGINALE per la regola
del brief e non CONVIENTE).
Scenari: base potenza 100 kWp, E
immessa 120.000 kWh, prezzo
unitario 0,095, ricavo lordo
11.400, corrispettivo 57, ricavo
netto 11.343, costi 2.000,
margine 9.343, VAN 6.434,43, TIR
5,68 per cento, payback 12 anni,
breakeven prezzo zonale 0,0907,
breakeven PMG 0,0, MARGINALE;
prezzo zonale 0,12 EUR/kWh
(prezzo unitario 0,12, ricavo
lordo 14.400, corrispettivo 72,
ricavo netto 14.328, margine
12.328, VAN 43.634,13, TIR 9,32
per cento, payback 9 anni,
breakeven prezzo zonale 0,0907,
breakeven PMG 0,0, CONVIENTE);
prezzo zonale 0,07 EUR/kWh
(prezzo unitario 0,09 per il
pavimento del PMG, ricavo lordo
10.800, corrispettivo 54, ricavo
netto 10.746, margine 8.746, VAN
meno 1.005,51, TIR 4,89 per
cento, payback 13 anni,
breakeven prezzo zonale 0,0907,
breakeven PMG 0,0907, MARGINALE);
PMG 0 (identico alla base, VAN
6.434,43, MARGINALE); CAPEX 800
EUR/kWp (CAPEX 80.000 EUR, VAN
36.434,43, TIR 9,92 per cento,
payback 9 anni, breakeven prezzo
zonale 0,0, breakeven PMG 0,0,
CONVIENTE); tasso 8 per cento
(VAN meno 18.269,05, TIR 5,68
per cento, payback 12 anni,
breakeven prezzo zonale 0,1106,
breakeven PMG 0,1106,
NON_CONVIENTE).
Confronto: RID ricavo lordo
11.400 contro PPA fisico 10.200
contro merchant 10.920, ricavo
netto RID 11.343 contro PPA
10.200 contro merchant 10.920,
margine RID 9.343 contro PPA
8.200 contro merchant 8.920, VAN
RID 6.434,43 contro PPA meno
7.809,88 contro merchant
1.162,92, TIR RID 5,68 per cento
contro PPA 4,15 per cento contro
merchant 5,12 per cento, payback
RID 12 anni contro PPA 14 anni
contro merchant 13 anni, tutti e
tre MARGINALE.
Tolleranza in FRAZIONE (0,10 = 10
per cento del CAPEX), usata
diretta, NON divisa per 100. Il
verdetto e CONVIENTE se il VAN e
maggiore di tolleranza per CAPEX,
MARGINALE se il valore assoluto
del VAN e minore o uguale a
tolleranza per CAPEX, NON
CONVIENTE altrimenti,
NON_CALCOLABILE se il margine e
zero o negativo oppure se potenza,
produzione specifica o vita sono
zero. Produzione, prezzi e
corrispettivo medi annui costanti,
SEMPLIFICAZIONE DICHIARATA (il
confronto tra prezzo zonale e PMG
e orario nel mondo reale, qui si
usano i valori medi annui); i
flussi sono solo sugli anni di
vita utile, SEMPLIFICAZIONE
DICHIARATA. La CO2 evitata e kWh
per fattore CO2 diviso 1000,
SEMPLIFICAZIONE DICHIARATA (il
fattore 0,25 dipende da fonte,
ora e stagione). Il PMG e un
PARAMETRO: i valori ufficiali sono
fissati annualmente da ARERA e
GSE. La TIR azzera il VAN a CAPEX
fissato (il CAPEX non viene
ricalcolato al variare del tasso).
Verdetto principale: MARGINALE.
Verdetto: NON_CALCOLABILE se il
margine annuo e zero o negativo
oppure se potenza, produzione
specifica o vita sono zero oppure
se un input e degenere (potenza
negativa, produzione specifica
negativa, prezzo zonale negativo,
PMG negativo, corrispettivo
negativo o sopra 1, O&M negativo,
CAPEX unitario negativo, vita
negativa o non intera, tasso
negativo, tolleranza negativa o
sopra 1); altrimenti CONVIENTE se
il VAN e maggiore di tolleranza
per CAPEX, MARGINALE se il valore
assoluto del VAN e minore o
uguale a tolleranza per CAPEX,
NON_CONVIENTE altrimenti.
La vita zero NON e degenere per
la validazione numerica: da VAN
meno CAPEX, TIR None, payback
None e verdetto NON_CALCOLABILE
per la guard degenere esplicita
(la vita negativa resta degenere).
La potenza zero NON e degenere
per la validazione numerica: da
energia zero, ricavo zero,
margine zero, CAPEX zero, VAN
zero e verdetto NON_CALCOLABILE.
Il CAPEX zero NON e degenere: da
VAN 116.434,43, TIR None, payback
0 e verdetto CONVIENTE. Il prezzo
zonale zero NON e degenere: con
PMG 0,09 il prezzo unitario resta
0,09, il margine e 8.746, il VAN
e meno 1.005,51 e il verdetto e
MARGINALE.
Casi limite: potenza zero (energia
zero, margine zero, CAPEX zero,
VAN zero, NON_CALCOLABILE);
prezzo zonale zero (prezzo
unitario 0,09, margine 8.746, VAN
meno 1.005,51, MARGINALE); PMG
zero e prezzo zero (prezzo
unitario zero, margine meno
2.000, VAN meno 134.924,42,
NON_CALCOLABILE); CAPEX zero
(VAN 116.434,43, TIR None,
payback 0, CONVIENTE); vita zero
(VAN meno 110.000, TIR None,
payback None, NON_CALCOLABILE);
tasso zero (VAN 76.860,
CONVIENTE); produzione specifica
zero (margine meno 2.000, VAN
meno 134.924,42, NON_CALCOLABILE);
O&M 113,43 EUR/kWp/anno (margine
zero, VAN meno 110.000,
NON_CALCOLABILE).
Distinzione esplicita: qui SOLO
il RITIRO DEDICATO del GSE
sull'energia immessa in rete,
NIENTE autoconsumo fisico
(l'energia autoconsumata non
viene immessa e non viene
ritirata: qui tutto viene
immesso, nessun autoconsumo),
NIENTE vendita diretta al vicino
(prezzo bilaterale tra privati,
non ritiro del GSE: il confronto
con il PPA fisico e solo un
termine di paragone, non il
meccanismo di questa scheda),
NIENTE scambio sul posto
(compensazione tra energia
immessa e prelevata, non vendita
dell'energia immessa: qui si
vende tutta l'energia immessa),
NIENTE tariffa premio per
l'energia condivisa (la scheda
della comunita energetica copre
la condivisione virtuale e la
tariffa premio: qui il beneficio
e il prezzo zonale con pavimento
PMG, non un premio), NIENTE
certificato di origine (titolo
negoziabile sul mercato, non
prezzo di ritiro: la scheda dei
Certificati Bianchi copre le
Garanzie di Origine; qui il
beneficio e il ricavo di vendita,
non un titolo), NIENTE Conto
Termico (contributo per il
calore, non per l'elettricita:
la scheda del Conto Termico copre
il calore; qui si misura
elettricita immessa, non calore),
NIENTE detrazione fiscale (sconto
in dichiarazione dei redditi, non
ricavo del GSE: la scheda della
detrazione fiscale copre lo
sconto fiscale; qui il beneficio
e il ricavo di vendita, non una
detrazione).
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w915_helpers import (
        demo_calcoli,
        mh910_alternativa,
        mh910_annuity,
        mh910_be_pmg,
        mh910_be_zonale,
        mh910_be_zonale_mwh,
        mh910_calcola,
        mh910_capex,
        mh910_co2,
        mh910_confronto,
        mh910_corrispettivo,
        mh910_costi,
        mh910_csv,
        mh910_demo,
        mh910_demo_calcoli,
        mh910_durata,
        mh910_e_immessa,
        mh910_fraz,
        mh910_intero,
        mh910_margine,
        mh910_nneg,
        mh910_num,
        mh910_payback,
        mh910_payback_fraz,
        mh910_pos,
        mh910_prezzo_unitario,
        mh910_ricavo_lordo,
        mh910_ricavo_netto,
        mh910_scenario,
        mh910_sensibilita,
        mh910_tir,
        mh910_valida,
        mh910_van,
        mh910_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w915_helpers", os.path.join(_hf, "w915_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh910_alternativa = _mod.mh910_alternativa
    mh910_annuity = _mod.mh910_annuity
    mh910_be_pmg = _mod.mh910_be_pmg
    mh910_be_zonale = _mod.mh910_be_zonale
    mh910_be_zonale_mwh = _mod.mh910_be_zonale_mwh
    mh910_calcola = _mod.mh910_calcola
    mh910_capex = _mod.mh910_capex
    mh910_co2 = _mod.mh910_co2
    mh910_confronto = _mod.mh910_confronto
    mh910_corrispettivo = _mod.mh910_corrispettivo
    mh910_costi = _mod.mh910_costi
    mh910_csv = _mod.mh910_csv
    mh910_demo = _mod.mh910_demo
    mh910_demo_calcoli = _mod.mh910_demo_calcoli
    mh910_durata = _mod.mh910_durata
    mh910_e_immessa = _mod.mh910_e_immessa
    mh910_fraz = _mod.mh910_fraz
    mh910_intero = _mod.mh910_intero
    mh910_margine = _mod.mh910_margine
    mh910_nneg = _mod.mh910_nneg
    mh910_num = _mod.mh910_num
    mh910_payback = _mod.mh910_payback
    mh910_payback_fraz = _mod.mh910_payback_fraz
    mh910_pos = _mod.mh910_pos
    mh910_prezzo_unitario = _mod.mh910_prezzo_unitario
    mh910_ricavo_lordo = _mod.mh910_ricavo_lordo
    mh910_ricavo_netto = _mod.mh910_ricavo_netto
    mh910_scenario = _mod.mh910_scenario
    mh910_sensibilita = _mod.mh910_sensibilita
    mh910_tir = _mod.mh910_tir
    mh910_valida = _mod.mh910_valida
    mh910_van = _mod.mh910_van
    mh910_verdetto = _mod.mh910_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w915_helpers.py")
_UI_PATH = _risolvi("w915_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
# L'identificatore della scheda NUOVA e invece un
# letterale: la guard dell'apply richiede "tab910"
# in questo file (lezione della scheda precedente:
# la costruzione dinamica faceva fallire l'apply).
_VECCHIO_MH = "mh90" + "9"
_VECCHIO_TAB = "tab90" + "9"
_VECCHIO_ST = "st90" + "9_"
_VECCHIO_SIGLA = "comunita " + "energetica"
_NUOVO_TAB = "tab910"
_NUOVO_ST = "st91" + "0_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO_SCALARI = {
    "e_immessa_kwh": 120000.0,
    "capex_eur": 110000.0,
    "prezzo_unitario_eur_kwh": 0.095,
    "ricavo_lordo_eur_anno": 11400.0,
    "corrispettivo_eur_anno": 57.0,
    "ricavo_netto_eur_anno": 11343.0,
    "costi_eur_anno": 2000.0,
    "margine_eur_anno": 9343.0,
    "van_eur": 6434.43123035114,
    "tir_frazione": 0.056804211536995886,
    "payback_anni": 12,
    "payback_fraz_anni": 11.773520282564487,
    "be_zonale_eur_kwh": 0.09067575034318293,
    "be_zonale_eur_mwh": 90.67575034318293,
    "be_pmg_eur_kwh": 0.0,
    "co2_t_anno": 30.0,
    "verdetto": "MARGINALE",
}

_DEMO_INPUT = {
    "potenza_kwp": 100.0,
    "produzione_specifica": 1200.0,
    "prezzo_zonale_eur_kwh": 0.095,
    "pmg_eur_kwh": 0.090,
    "corrispettivo_frazione": 0.005,
    "om_eur_kwp_anno": 20.0,
    "capex_eur_kwp": 1100.0,
    "vita_anni": 20,
    "tasso_frazione": 0.05,
    "tol_frazione": 0.10,
}

_DEMO_SCENARI = [
    {"nome": "Base",
     "potenza_kwp": 100.0, "produzione_specifica": 1200.0,
     "prezzo_zonale_eur_kwh": 0.095,
     "pmg_eur_kwh": 0.09,
     "corrispettivo_frazione": 0.005,
     "om_eur_kwp_anno": 20.0,
     "capex_eur_kwp": 1100.0, "vita_anni": 20,
     "tasso_frazione": 0.05, "tol_frazione": 0.10,
     "e_immessa_kwh": 120000.0, "capex_eur": 110000.0,
     "prezzo_unitario_eur_kwh": 0.095,
     "ricavo_lordo_eur_anno": 11400.0,
     "corrispettivo_eur_anno": 57.0,
     "ricavo_netto_eur_anno": 11343.0,
     "costi_eur_anno": 2000.0, "margine_eur_anno": 9343.0,
     "van_eur": 6434.43123035114,
     "tir_frazione": 0.056804211536995886,
     "payback_anni": 12,
     "payback_fraz_anni": 11.773520282564487,
     "be_zonale_eur_kwh": 0.09067575034318293,
     "be_zonale_eur_mwh": 90.67575034318293,
     "be_pmg_eur_kwh": 0.0, "co2_t_anno": 30.0,
     "verdetto": "MARGINALE"},
    {"nome": "Prezzo zonale 0,12 EUR/kWh",
     "potenza_kwp": 100.0, "produzione_specifica": 1200.0,
     "prezzo_zonale_eur_kwh": 0.12,
     "pmg_eur_kwh": 0.09,
     "corrispettivo_frazione": 0.005,
     "om_eur_kwp_anno": 20.0,
     "capex_eur_kwp": 1100.0, "vita_anni": 20,
     "tasso_frazione": 0.05, "tol_frazione": 0.10,
     "e_immessa_kwh": 120000.0, "capex_eur": 110000.0,
     "prezzo_unitario_eur_kwh": 0.12,
     "ricavo_lordo_eur_anno": 14400.0,
     "corrispettivo_eur_anno": 72.0,
     "ricavo_netto_eur_anno": 14328.0,
     "costi_eur_anno": 2000.0, "margine_eur_anno": 12328.0,
     "van_eur": 43634.129102833016,
     "tir_frazione": 0.0932216969947281,
     "payback_anni": 9,
     "payback_fraz_anni": 8.922777417261518,
     "be_zonale_eur_kwh": 0.09067575034318293,
     "be_zonale_eur_mwh": 90.67575034318293,
     "be_pmg_eur_kwh": 0.0, "co2_t_anno": 30.0,
     "verdetto": "CONVIENTE"},
    {"nome": "Prezzo zonale 0,07 EUR/kWh",
     "potenza_kwp": 100.0, "produzione_specifica": 1200.0,
     "prezzo_zonale_eur_kwh": 0.07,
     "pmg_eur_kwh": 0.09,
     "corrispettivo_frazione": 0.005,
     "om_eur_kwp_anno": 20.0,
     "capex_eur_kwp": 1100.0, "vita_anni": 20,
     "tasso_frazione": 0.05, "tol_frazione": 0.10,
     "e_immessa_kwh": 120000.0, "capex_eur": 110000.0,
     "prezzo_unitario_eur_kwh": 0.09,
     "ricavo_lordo_eur_anno": 10800.0,
     "corrispettivo_eur_anno": 54.0,
     "ricavo_netto_eur_anno": 10746.0,
     "costi_eur_anno": 2000.0, "margine_eur_anno": 8746.0,
     "van_eur": -1005.5083441452298,
     "tir_frazione": 0.04891951122212346,
     "payback_anni": 13,
     "payback_fraz_anni": 12.577178138577635,
     "be_zonale_eur_kwh": 0.09067575034318293,
     "be_zonale_eur_mwh": 90.67575034318293,
     "be_pmg_eur_kwh": 0.09067575034318293,
     "co2_t_anno": 30.0, "verdetto": "MARGINALE"},
    {"nome": "PMG 0",
     "potenza_kwp": 100.0, "produzione_specifica": 1200.0,
     "prezzo_zonale_eur_kwh": 0.095,
     "pmg_eur_kwh": 0.0,
     "corrispettivo_frazione": 0.005,
     "om_eur_kwp_anno": 20.0,
     "capex_eur_kwp": 1100.0, "vita_anni": 20,
     "tasso_frazione": 0.05, "tol_frazione": 0.10,
     "e_immessa_kwh": 120000.0, "capex_eur": 110000.0,
     "prezzo_unitario_eur_kwh": 0.095,
     "ricavo_lordo_eur_anno": 11400.0,
     "corrispettivo_eur_anno": 57.0,
     "ricavo_netto_eur_anno": 11343.0,
     "costi_eur_anno": 2000.0, "margine_eur_anno": 9343.0,
     "van_eur": 6434.43123035114,
     "tir_frazione": 0.056804211536995886,
     "payback_anni": 12,
     "payback_fraz_anni": 11.773520282564487,
     "be_zonale_eur_kwh": 0.09067575034318293,
     "be_zonale_eur_mwh": 90.67575034318293,
     "be_pmg_eur_kwh": 0.0, "co2_t_anno": 30.0,
     "verdetto": "MARGINALE"},
    {"nome": "CAPEX 800 EUR/kWp",
     "potenza_kwp": 100.0, "produzione_specifica": 1200.0,
     "prezzo_zonale_eur_kwh": 0.095,
     "pmg_eur_kwh": 0.09,
     "corrispettivo_frazione": 0.005,
     "om_eur_kwp_anno": 20.0,
     "capex_eur_kwp": 800.0, "vita_anni": 20,
     "tasso_frazione": 0.05, "tol_frazione": 0.10,
     "e_immessa_kwh": 120000.0, "capex_eur": 80000.0,
     "prezzo_unitario_eur_kwh": 0.095,
     "ricavo_lordo_eur_anno": 11400.0,
     "corrispettivo_eur_anno": 57.0,
     "ricavo_netto_eur_anno": 11343.0,
     "costi_eur_anno": 2000.0, "margine_eur_anno": 9343.0,
     "van_eur": 36434.43123035114,
     "tir_frazione": 0.0991607570491767,
     "payback_anni": 9,
     "payback_fraz_anni": 8.562560205501445,
     "be_zonale_eur_kwh": 0.0,
     "be_zonale_eur_mwh": 0.0,
     "be_pmg_eur_kwh": 0.0, "co2_t_anno": 30.0,
     "verdetto": "CONVIENTE"},
    {"nome": "Tasso 8 %",
     "potenza_kwp": 100.0, "produzione_specifica": 1200.0,
     "prezzo_zonale_eur_kwh": 0.095,
     "pmg_eur_kwh": 0.09,
     "corrispettivo_frazione": 0.005,
     "om_eur_kwp_anno": 20.0,
     "capex_eur_kwp": 1100.0, "vita_anni": 20,
     "tasso_frazione": 0.08, "tol_frazione": 0.10,
     "e_immessa_kwh": 120000.0, "capex_eur": 110000.0,
     "prezzo_unitario_eur_kwh": 0.095,
     "ricavo_lordo_eur_anno": 11400.0,
     "corrispettivo_eur_anno": 57.0,
     "ricavo_netto_eur_anno": 11343.0,
     "costi_eur_anno": 2000.0, "margine_eur_anno": 9343.0,
     "van_eur": -18269.048772201248,
     "tir_frazione": 0.056804211536995886,
     "payback_anni": 12,
     "payback_fraz_anni": 11.773520282564487,
     "be_zonale_eur_kwh": 0.110584111981127,
     "be_zonale_eur_mwh": 110.584111981127,
     "be_pmg_eur_kwh": 0.110584111981127,
     "co2_t_anno": 30.0, "verdetto": "NON_CONVIENTE"},
]

_DEMO_CONFRONTO = {
    "rid": {
        "nome": "RID", "e_immessa_kwh": 120000.0,
        "prezzo_unitario_eur_kwh": 0.095,
        "corrispettivo_frazione": 0.005,
        "ricavo_lordo_eur_anno": 11400.0,
        "corrispettivo_eur_anno": 57.0,
        "ricavo_netto_eur_anno": 11343.0,
        "costi_eur_anno": 2000.0, "capex_eur": 110000.0,
        "margine_eur_anno": 9343.0,
        "van_eur": 6434.43123035114,
        "tir_frazione": 0.056804211536995886,
        "payback_anni": 12,
        "payback_fraz_anni": 11.773520282564487,
        "verdetto": "MARGINALE"},
    "ppa": {
        "nome": "PPA fisico", "e_immessa_kwh": 120000.0,
        "prezzo_unitario_eur_kwh": 0.085,
        "corrispettivo_frazione": 0.0,
        "ricavo_lordo_eur_anno": 10200.0,
        "corrispettivo_eur_anno": 0.0,
        "ricavo_netto_eur_anno": 10200.0,
        "costi_eur_anno": 2000.0, "capex_eur": 110000.0,
        "margine_eur_anno": 8200.0,
        "van_eur": -7809.875191172061,
        "tir_frazione": 0.041474162284774116,
        "payback_anni": 14,
        "payback_fraz_anni": 13.414634146341463,
        "verdetto": "MARGINALE"},
    "merchant": {
        "nome": "Merchant", "e_immessa_kwh": 120000.0,
        "prezzo_unitario_eur_kwh": 0.091,
        "corrispettivo_frazione": 0.0,
        "ricavo_lordo_eur_anno": 10920.0,
        "corrispettivo_eur_anno": 0.0,
        "ricavo_netto_eur_anno": 10920.0,
        "costi_eur_anno": 2000.0, "capex_eur": 110000.0,
        "margine_eur_anno": 8920.0,
        "van_eur": 1162.9162554567301,
        "tir_frazione": 0.051243649327652865,
        "payback_anni": 13,
        "payback_fraz_anni": 12.331838565022421,
        "verdetto": "MARGINALE"},
}

_ORDINE_VALIDA = (
    "potenza_kwp", "produzione_specifica",
    "prezzo_zonale_eur_kwh", "pmg_eur_kwh",
    "corrispettivo_frazione", "om_eur_kwp_anno",
    "capex_eur_kwp", "vita_anni", "tasso_frazione",
    "tol_frazione")


def _demo_kwargs(**over):
    kw = dict(mh910_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))

class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh910_num(3, "x"), 3.0)
        self.assertEqual(mh910_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh910_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh910_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh910_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh910_pos(0, "x")
        with self.assertRaises(ValueError):
            mh910_pos(-1, "x")
        self.assertEqual(mh910_pos(3, "x"), 3.0)

    def test_fraz_bordi(self):
        self.assertEqual(mh910_fraz(0, "x"), 0.0)
        self.assertEqual(mh910_fraz(1, "x"), 1.0)
        self.assertEqual(mh910_fraz(0.005, "x"), 0.005)
        with self.assertRaises(ValueError):
            mh910_fraz(-0.01, "x")
        with self.assertRaises(ValueError):
            mh910_fraz(1.01, "x")

    def test_durata_bordi(self):
        self.assertEqual(mh910_durata(0, "x"), 0)
        self.assertEqual(mh910_durata(20, "x"), 20)
        self.assertEqual(mh910_durata(20.0, "x"), 20)
        with self.assertRaises(ValueError):
            mh910_durata(-1, "x")
        with self.assertRaises(ValueError):
            mh910_durata(2.5, "x")
        with self.assertRaises(ValueError):
            mh910_durata(float("nan"), "x")

    def test_intero_bordi(self):
        self.assertEqual(mh910_intero(0, "x"), 0)
        self.assertEqual(mh910_intero(10, "x"), 10)
        self.assertEqual(mh910_intero(10.0, "x"), 10)
        with self.assertRaises(ValueError):
            mh910_intero(-1, "x")
        with self.assertRaises(ValueError):
            mh910_intero(2.5, "x")
        with self.assertRaises(ValueError):
            mh910_intero(float("nan"), "x")


class TestFisica(unittest.TestCase):
    def test_e_immessa(self):
        self.assertEqual(mh910_e_immessa(100.0, 1200.0), 120000.0)
        self.assertEqual(mh910_e_immessa(0.0, 1200.0), 0.0)
        self.assertEqual(mh910_e_immessa(100.0, 0.0), 0.0)
        self.assertEqual(mh910_e_immessa(100.0, 1500.0), 150000.0)
        self.assertEqual(mh910_e_immessa(200.0, 1200.0), 240000.0)
        with self.assertRaises(ValueError):
            mh910_e_immessa(-1.0, 1200.0)
        with self.assertRaises(ValueError):
            mh910_e_immessa(100.0, -1.0)

    def test_capex(self):
        self.assertEqual(mh910_capex(100.0, 1100.0), 110000.0)
        self.assertEqual(mh910_capex(100.0, 800.0), 80000.0)
        self.assertEqual(mh910_capex(0.0, 1100.0), 0.0)
        self.assertEqual(mh910_capex(100.0, 0.0), 0.0)
        self.assertEqual(mh910_capex(200.0, 1100.0), 220000.0)
        with self.assertRaises(ValueError):
            mh910_capex(-1.0, 1100.0)
        with self.assertRaises(ValueError):
            mh910_capex(100.0, -1.0)

    def test_prezzo_unitario(self):
        self.assertEqual(mh910_prezzo_unitario(0.095, 0.090), 0.095)
        self.assertEqual(mh910_prezzo_unitario(0.07, 0.09), 0.09)
        self.assertEqual(mh910_prezzo_unitario(0.12, 0.09), 0.12)
        self.assertEqual(mh910_prezzo_unitario(0.0, 0.09), 0.09)
        self.assertEqual(mh910_prezzo_unitario(0.095, 0.0), 0.095)
        self.assertEqual(mh910_prezzo_unitario(0.0, 0.0), 0.0)
        self.assertEqual(mh910_prezzo_unitario(0.09, 0.09), 0.09)
        with self.assertRaises(ValueError):
            mh910_prezzo_unitario(-0.01, 0.09)
        with self.assertRaises(ValueError):
            mh910_prezzo_unitario(0.095, -0.01)

    def test_ricavo_lordo(self):
        self.assertEqual(mh910_ricavo_lordo(120000.0, 0.095), 11400.0)
        self.assertEqual(mh910_ricavo_lordo(120000.0, 0.12), 14400.0)
        self.assertEqual(mh910_ricavo_lordo(120000.0, 0.09), 10800.0)
        self.assertEqual(mh910_ricavo_lordo(0.0, 0.095), 0.0)
        self.assertEqual(mh910_ricavo_lordo(120000.0, 0.0), 0.0)
        with self.assertRaises(ValueError):
            mh910_ricavo_lordo(-1.0, 0.095)

    def test_corrispettivo(self):
        self.assertEqual(mh910_corrispettivo(11400.0, 0.005), 57.0)
        self.assertEqual(mh910_corrispettivo(14400.0, 0.005), 72.0)
        self.assertEqual(mh910_corrispettivo(10800.0, 0.005), 54.0)
        self.assertEqual(mh910_corrispettivo(11400.0, 0.0), 0.0)
        self.assertEqual(mh910_corrispettivo(0.0, 0.005), 0.0)
        self.assertEqual(mh910_corrispettivo(11400.0, 1.0), 11400.0)
        with self.assertRaises(ValueError):
            mh910_corrispettivo(11400.0, -0.01)
        with self.assertRaises(ValueError):
            mh910_corrispettivo(11400.0, 1.01)

    def test_ricavo_netto(self):
        self.assertEqual(mh910_ricavo_netto(11400.0, 57.0), 11343.0)
        self.assertEqual(mh910_ricavo_netto(14400.0, 72.0), 14328.0)
        self.assertEqual(mh910_ricavo_netto(10800.0, 54.0), 10746.0)
        self.assertEqual(mh910_ricavo_netto(0.0, 0.0), 0.0)
        with self.assertRaises(ValueError):
            mh910_ricavo_netto(-1.0, 57.0)

    def test_costi(self):
        self.assertEqual(mh910_costi(20.0, 100.0), 2000.0)
        self.assertEqual(mh910_costi(0.0, 100.0), 0.0)
        self.assertEqual(mh910_costi(113.43, 100.0), 11343.0)
        self.assertEqual(mh910_costi(20.0, 0.0), 0.0)
        self.assertEqual(mh910_costi(20.0, 200.0), 4000.0)
        self.assertEqual(mh910_costi(50.0, 100.0), 5000.0)
        with self.assertRaises(ValueError):
            mh910_costi(-1.0, 100.0)
        with self.assertRaises(ValueError):
            mh910_costi(20.0, -1.0)

    def test_margine(self):
        self.assertEqual(mh910_margine(11343.0, 2000.0), 9343.0)
        self.assertEqual(mh910_margine(14328.0, 2000.0), 12328.0)
        self.assertEqual(mh910_margine(10746.0, 2000.0), 8746.0)
        self.assertEqual(mh910_margine(0.0, 2000.0), -2000.0)
        self.assertEqual(mh910_margine(11343.0, 11343.0), 0.0)
        self.assertEqual(mh910_margine(0.0, 0.0), 0.0)
        with self.assertRaises(ValueError):
            mh910_margine(-1.0, 2000.0)
        with self.assertRaises(ValueError):
            mh910_margine(11343.0, -1.0)

    def test_annuity(self):
        self.assertAlmostEqual(mh910_annuity(20, 0.05),
                               12.462210342539992, places=9)
        self.assertAlmostEqual(mh910_annuity(20, 0.08),
                               9.818147407449294, places=9)
        self.assertAlmostEqual(mh910_annuity(30, 0.05),
                               15.372451026418378, places=9)
        self.assertEqual(mh910_annuity(20, 0.0), 20.0)
        self.assertEqual(mh910_annuity(0, 0.05), 0.0)
        self.assertEqual(mh910_annuity(0, 0.0), 0.0)
        self.assertAlmostEqual(mh910_annuity(1, 0.05),
                               0.9523809523809523, places=9)
        with self.assertRaises(ValueError):
            mh910_annuity(-1, 0.05)
        with self.assertRaises(ValueError):
            mh910_annuity(2.5, 0.05)

    def test_van(self):
        self.assertAlmostEqual(
            mh910_van(110000.0, 9343.0, 20, 0.05),
            6434.43123035114, places=2)
        self.assertAlmostEqual(
            mh910_van(110000.0, 12328.0, 20, 0.05),
            43634.129102833016, places=2)
        self.assertAlmostEqual(
            mh910_van(110000.0, 8746.0, 20, 0.05),
            -1005.5083441452298, places=2)
        self.assertAlmostEqual(
            mh910_van(80000.0, 9343.0, 20, 0.05),
            36434.43123035114, places=2)
        self.assertEqual(mh910_van(110000.0, 9343.0, 0, 0.05),
                         -110000.0)
        self.assertAlmostEqual(
            mh910_van(0.0, 9343.0, 20, 0.05),
            116434.43123035114, places=2)
        self.assertAlmostEqual(
            mh910_van(110000.0, 9343.0, 20, 0.0),
            76860.0, places=2)
        self.assertAlmostEqual(
            mh910_van(110000.0, -2000.0, 20, 0.05),
            -134924.42068508, places=2)
        self.assertEqual(mh910_van(0.0, 0.0, 20, 0.05), 0.0)

    def test_tir(self):
        self.assertAlmostEqual(
            mh910_tir(110000.0, 9343.0, 20),
            0.056804211536995886, places=4)
        self.assertAlmostEqual(
            mh910_tir(110000.0, 12328.0, 20),
            0.0932216969947281, places=4)
        self.assertAlmostEqual(
            mh910_tir(110000.0, 8746.0, 20),
            0.04891951122212346, places=4)
        self.assertAlmostEqual(
            mh910_tir(80000.0, 9343.0, 20),
            0.0991607570491767, places=4)
        self.assertAlmostEqual(
            mh910_tir(110000.0, 8200.0, 20),
            0.041474162284774116, places=4)
        self.assertAlmostEqual(
            mh910_tir(110000.0, 8920.0, 20),
            0.051243649327652865, places=4)
        self.assertIsNone(mh910_tir(0.0, 9343.0, 20))
        self.assertIsNone(mh910_tir(110000.0, 0.0, 20))
        self.assertIsNone(mh910_tir(110000.0, -2000.0, 20))
        self.assertIsNone(mh910_tir(110000.0, 9343.0, 0))
        # Alla TIR il VAN a CAPEX fissato e zero.
        tir = mh910_tir(110000.0, 9343.0, 20)
        self.assertAlmostEqual(
            mh910_van(110000.0, 9343.0, 20, tir),
            0.0, places=2)

    def test_payback(self):
        self.assertEqual(
            mh910_payback(110000.0, 9343.0, 20), 12)
        self.assertEqual(
            mh910_payback(110000.0, 12328.0, 20), 9)
        self.assertEqual(
            mh910_payback(110000.0, 8746.0, 20), 13)
        self.assertEqual(
            mh910_payback(80000.0, 9343.0, 20), 9)
        self.assertEqual(
            mh910_payback(110000.0, 8200.0, 20), 14)
        self.assertEqual(
            mh910_payback(110000.0, 8920.0, 20), 13)
        self.assertEqual(mh910_payback(0.0, 9343.0, 20), 0)
        self.assertIsNone(
            mh910_payback(110000.0, 0.0, 20))
        self.assertIsNone(
            mh910_payback(110000.0, -2000.0, 20))
        self.assertIsNone(
            mh910_payback(110000.0, 9343.0, 0))
        # Margine troppo piccolo: mai entro la vita.
        self.assertIsNone(mh910_payback(110000.0, 1000.0, 20))
        self.assertEqual(mh910_payback(110000.0, 1000.0, 200),
                         110)

    def test_payback_fraz(self):
        self.assertAlmostEqual(
            mh910_payback_fraz(110000.0, 9343.0, 20),
            11.773520282564487, places=9)
        self.assertAlmostEqual(
            mh910_payback_fraz(110000.0, 12328.0, 20),
            8.922777417261518, places=9)
        self.assertAlmostEqual(
            mh910_payback_fraz(110000.0, 8746.0, 20),
            12.577178138577635, places=9)
        self.assertAlmostEqual(
            mh910_payback_fraz(80000.0, 9343.0, 20),
            8.562560205501445, places=9)
        self.assertAlmostEqual(
            mh910_payback_fraz(110000.0, 8200.0, 20),
            13.414634146341463, places=9)
        self.assertAlmostEqual(
            mh910_payback_fraz(110000.0, 8920.0, 20),
            12.331838565022421, places=9)
        self.assertEqual(
            mh910_payback_fraz(0.0, 9343.0, 20), 0.0)
        self.assertIsNone(
            mh910_payback_fraz(110000.0, 0.0, 20))
        self.assertIsNone(
            mh910_payback_fraz(110000.0, -2000.0, 20))
        self.assertIsNone(
            mh910_payback_fraz(110000.0, 9343.0, 0))
        # Payback mai raggiunto entro la vita:
        # frazionale None (formula legata a t).
        self.assertIsNone(
            mh910_payback_fraz(110000.0, 1000.0, 20))

    def test_be_zonale(self):
        self.assertAlmostEqual(
            mh910_be_zonale(110000.0, 2000.0, 120000.0,
                            0.005, 0.09, 20, 0.05),
            0.09067575034318293, places=4)
        self.assertAlmostEqual(
            mh910_be_zonale(110000.0, 2000.0, 120000.0,
                            0.005, 0.09, 20, 0.08),
            0.110584111981127, places=4)
        self.assertAlmostEqual(
            mh910_be_zonale(110000.0, 11343.0, 120000.0,
                            0.005, 0.09, 20, 0.05),
            0.16892533158271392, places=4)
        # Valore minore o uguale al PMG fissato a
        # 0,0: CAPEX 80.000, tasso zero, vita 30.
        self.assertEqual(
            mh910_be_zonale(80000.0, 2000.0, 120000.0,
                            0.005, 0.09, 20, 0.05),
            0.0)
        self.assertEqual(
            mh910_be_zonale(110000.0, 2000.0, 120000.0,
                            0.005, 0.09, 20, 0.0),
            0.0)
        self.assertEqual(
            mh910_be_zonale(110000.0, 2000.0, 120000.0,
                            0.005, 0.09, 30, 0.05),
            0.0)
        # E immessa zero: None.
        self.assertIsNone(
            mh910_be_zonale(110000.0, 2000.0, 0.0,
                            0.005, 0.09, 20, 0.05))
        # Vita zero: None.
        self.assertIsNone(
            mh910_be_zonale(110000.0, 2000.0, 120000.0,
                            0.005, 0.09, 0, 0.05))
        # Corrispettivo 1,0: None.
        self.assertIsNone(
            mh910_be_zonale(110000.0, 2000.0, 120000.0,
                            1.0, 0.09, 20, 0.05))
        with self.assertRaises(ValueError):
            mh910_be_zonale(-1.0, 2000.0, 120000.0,
                            0.005, 0.09, 20, 0.05)
        # Al prezzo zonale di breakeven il VAN e zero.
        bez = mh910_be_zonale(110000.0, 2000.0, 120000.0,
                              0.005, 0.09, 20, 0.05)
        bc = mh910_calcola(
            **_demo_kwargs(prezzo_zonale_eur_kwh=bez))
        self.assertAlmostEqual(bc["van_eur"], 0.0, places=2)

    def test_be_zonale_invariante_prezzo_corrente(self):
        # Il breakeven prezzo zonale e INVARIANTE
        # al prezzo zonale corrente.
        bc0 = demo_calcoli()
        bc = mh910_calcola(
            **_demo_kwargs(prezzo_zonale_eur_kwh=0.12))
        self.assertEqual(bc["be_zonale_eur_kwh"],
                         bc0["be_zonale_eur_kwh"])
        self.assertAlmostEqual(
            bc["be_zonale_eur_kwh"], 0.0907, places=4)
        bc = mh910_calcola(
            **_demo_kwargs(prezzo_zonale_eur_kwh=0.07))
        self.assertEqual(bc["be_zonale_eur_kwh"],
                         bc0["be_zonale_eur_kwh"])

    def test_be_zonale_mwh(self):
        self.assertAlmostEqual(
            mh910_be_zonale_mwh(0.09067575034318293),
            90.67575034318293, places=2)
        self.assertAlmostEqual(
            mh910_be_zonale_mwh(0.110584111981127),
            110.584111981127, places=2)
        self.assertEqual(mh910_be_zonale_mwh(0.0), 0.0)
        self.assertIsNone(mh910_be_zonale_mwh(None))
        with self.assertRaises(ValueError):
            mh910_be_zonale_mwh(-0.01)

    def test_be_pmg(self):
        # Demo: VAN gia positivo con PMG zero.
        self.assertEqual(
            mh910_be_pmg(110000.0, 2000.0, 120000.0,
                         0.005, 0.095, 20, 0.05),
            0.0)
        self.assertAlmostEqual(
            mh910_be_pmg(110000.0, 2000.0, 120000.0,
                         0.005, 0.07, 20, 0.05),
            0.09067575034318293, places=4)
        self.assertAlmostEqual(
            mh910_be_pmg(110000.0, 2000.0, 120000.0,
                         0.005, 0.0, 20, 0.05),
            0.09067575034318293, places=4)
        self.assertAlmostEqual(
            mh910_be_pmg(110000.0, 2000.0, 120000.0,
                         0.005, 0.095, 20, 0.08),
            0.110584111981127, places=4)
        self.assertEqual(
            mh910_be_pmg(80000.0, 2000.0, 120000.0,
                         0.005, 0.095, 20, 0.05),
            0.0)
        self.assertEqual(
            mh910_be_pmg(110000.0, 2000.0, 120000.0,
                         0.005, 0.095, 20, 0.0),
            0.0)
        self.assertAlmostEqual(
            mh910_be_pmg(110000.0, 11343.0, 120000.0,
                         0.005, 0.095, 20, 0.05),
            0.16892533158271392, places=4)
        # E immessa zero: None.
        self.assertIsNone(
            mh910_be_pmg(110000.0, 2000.0, 0.0,
                         0.005, 0.095, 20, 0.05))
        # Vita zero: None.
        self.assertIsNone(
            mh910_be_pmg(110000.0, 2000.0, 120000.0,
                         0.005, 0.095, 0, 0.05))
        # Corrispettivo 1,0: None.
        self.assertIsNone(
            mh910_be_pmg(110000.0, 2000.0, 120000.0,
                         1.0, 0.095, 20, 0.05))
        with self.assertRaises(ValueError):
            mh910_be_pmg(-1.0, 2000.0, 120000.0,
                         0.005, 0.095, 20, 0.05)
        # Al PMG di breakeven il VAN e zero
        # (prezzo zonale 0,07 sotto il breakeven).
        bep = mh910_be_pmg(110000.0, 2000.0, 120000.0,
                           0.005, 0.07, 20, 0.05)
        bc = mh910_calcola(
            **_demo_kwargs(prezzo_zonale_eur_kwh=0.07,
                           pmg_eur_kwh=bep))
        self.assertAlmostEqual(bc["van_eur"], 0.0, places=2)

    def test_be_pmg_invariante_pmg_corrente(self):
        # Il breakeven PMG e INVARIANTE
        # al PMG corrente.
        bc0 = demo_calcoli()
        bc = mh910_calcola(**_demo_kwargs(pmg_eur_kwh=0.0))
        self.assertEqual(bc["be_pmg_eur_kwh"],
                         bc0["be_pmg_eur_kwh"])
        self.assertEqual(bc["be_pmg_eur_kwh"], 0.0)
        self.assertEqual(bc["van_eur"], bc0["van_eur"])

    def test_co2(self):
        self.assertEqual(mh910_co2(120000.0), 30.0)
        self.assertEqual(mh910_co2(0.0), 0.0)
        self.assertEqual(mh910_co2(150000.0), 37.5)
        self.assertEqual(mh910_co2(240000.0), 60.0)
        self.assertEqual(mh910_co2(1000.0), 0.25)
        with self.assertRaises(ValueError):
            mh910_co2(-1.0)

    def test_scenario_singolo(self):
        s = mh910_scenario("Prezzo zonale 0,12 EUR/kWh",
                           mh910_demo(),
                           {"prezzo_zonale_eur_kwh": 0.12})
        self.assertEqual(s["nome"], "Prezzo zonale 0,12 EUR/kWh")
        self.assertEqual(s["prezzo_zonale_eur_kwh"], 0.12)
        self.assertAlmostEqual(s["van_eur"], 43634.13,
                               places=2)
        self.assertEqual(s["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["be_zonale_eur_kwh"],
                               0.0907, places=4)
        self.assertEqual(s["be_pmg_eur_kwh"], 0.0)
        s = mh910_scenario("Prezzo zonale 0,07 EUR/kWh",
                           mh910_demo(),
                           {"prezzo_zonale_eur_kwh": 0.07})
        self.assertAlmostEqual(s["van_eur"], -1005.51,
                               places=2)
        self.assertEqual(s["payback_anni"], 13)
        self.assertAlmostEqual(s["be_pmg_eur_kwh"], 0.0907,
                               places=4)
        self.assertEqual(s["verdetto"], "MARGINALE")
        s = mh910_scenario("PMG 0", mh910_demo(),
                           {"pmg_eur_kwh": 0.0})
        self.assertAlmostEqual(s["van_eur"], 6434.43,
                               places=2)
        self.assertEqual(s["verdetto"], "MARGINALE")
        s = mh910_scenario("CAPEX 800 EUR/kWp", mh910_demo(),
                           {"capex_eur_kwp": 800.0})
        self.assertAlmostEqual(s["van_eur"], 36434.43,
                               places=2)
        self.assertEqual(s["be_zonale_eur_kwh"], 0.0)
        self.assertEqual(s["verdetto"], "CONVIENTE")
        s = mh910_scenario("Tasso 8 %", mh910_demo(),
                           {"tasso_frazione": 0.08})
        self.assertAlmostEqual(s["van_eur"], -18269.05,
                               places=2)
        self.assertEqual(s["verdetto"], "NON_CONVIENTE")
        with self.assertRaises(ValueError):
            mh910_scenario("", mh910_demo(),
                           {"prezzo_zonale_eur_kwh": 0.12})
        with self.assertRaises(ValueError):
            mh910_scenario("X", mh910_demo(),
                           {"vita_anni": -1})

    def test_alternativa_singola(self):
        a = mh910_alternativa("RID", 120000.0, 0.095, 0.005,
                              2000.0, 110000.0, 20, 0.05, 0.10)
        self.assertEqual(a["nome"], "RID")
        self.assertEqual(a["ricavo_lordo_eur_anno"], 11400.0)
        self.assertEqual(a["corrispettivo_eur_anno"], 57.0)
        self.assertEqual(a["ricavo_netto_eur_anno"], 11343.0)
        self.assertEqual(a["margine_eur_anno"], 9343.0)
        self.assertAlmostEqual(a["van_eur"], 6434.43, places=2)
        self.assertEqual(a["verdetto"], "MARGINALE")
        a = mh910_alternativa("PPA fisico", 120000.0, 0.085,
                              0.0, 2000.0, 110000.0, 20, 0.05,
                              0.10)
        self.assertEqual(a["ricavo_lordo_eur_anno"], 10200.0)
        self.assertEqual(a["corrispettivo_eur_anno"], 0.0)
        self.assertEqual(a["margine_eur_anno"], 8200.0)
        self.assertAlmostEqual(a["van_eur"], -7809.88,
                               places=2)
        self.assertEqual(a["payback_anni"], 14)
        self.assertEqual(a["verdetto"], "MARGINALE")
        a = mh910_alternativa("Merchant", 120000.0, 0.091,
                              0.0, 2000.0, 110000.0, 20, 0.05,
                              0.10)
        self.assertEqual(a["ricavo_lordo_eur_anno"], 10920.0)
        self.assertEqual(a["margine_eur_anno"], 8920.0)
        self.assertAlmostEqual(a["van_eur"], 1162.92,
                               places=2)
        self.assertEqual(a["payback_anni"], 13)
        self.assertEqual(a["verdetto"], "MARGINALE")
        with self.assertRaises(ValueError):
            mh910_alternativa("", 120000.0, 0.095, 0.005,
                              2000.0, 110000.0, 20, 0.05, 0.10)
        with self.assertRaises(ValueError):
            mh910_alternativa("RID", 120000.0, 0.095, 0.005,
                              2000.0, 110000.0, 20, 0.05, 0.10,
                              degenere="si")

    def test_confronto_formule(self):
        rid = mh910_alternativa("RID", 120000.0, 0.095,
                                0.005, 2000.0, 110000.0, 20,
                                0.05, 0.10)
        ppa = mh910_alternativa("PPA fisico", 120000.0,
                                0.085, 0.0, 2000.0, 110000.0,
                                20, 0.05, 0.10)
        mer = mh910_alternativa("Merchant", 120000.0, 0.091,
                                0.0, 2000.0, 110000.0, 20,
                                0.05, 0.10)
        c = mh910_confronto(rid, ppa, mer)
        self.assertEqual(c["rid"]["van_eur"],
                         6434.43123035114)
        self.assertEqual(c["ppa"]["van_eur"],
                         -7809.875191172061)
        self.assertEqual(c["merchant"]["van_eur"],
                         1162.9162554567301)
        self.assertEqual(c["rid"]["verdetto"], "MARGINALE")
        self.assertEqual(c["ppa"]["verdetto"], "MARGINALE")
        self.assertEqual(c["merchant"]["verdetto"], "MARGINALE")
        self.assertGreater(c["rid"]["van_eur"],
                           c["merchant"]["van_eur"])
        self.assertGreater(c["merchant"]["van_eur"],
                           c["ppa"]["van_eur"])
        with self.assertRaises(ValueError):
            mh910_confronto(ppa, rid, mer)
        with self.assertRaises(ValueError):
            mh910_confronto(rid, ppa, {"nome": "Altro"})
        with self.assertRaises(ValueError):
            mh910_confronto(rid, ppa, dict(mer, nome="Altro"))


class TestFinanza(unittest.TestCase):
    def test_verdetto_bordi(self):
        self.assertEqual(
            mh910_verdetto(11000.01, 0.10, 110000.0, 9343.0),
            "CONVIENTE")
        self.assertEqual(
            mh910_verdetto(11000.0, 0.10, 110000.0, 9343.0),
            "MARGINALE")
        self.assertEqual(
            mh910_verdetto(6434.43, 0.10, 110000.0, 9343.0),
            "MARGINALE")
        self.assertEqual(
            mh910_verdetto(0.0, 0.10, 110000.0, 9343.0),
            "MARGINALE")
        self.assertEqual(
            mh910_verdetto(-11000.0, 0.10, 110000.0, 9343.0),
            "MARGINALE")
        self.assertEqual(
            mh910_verdetto(-11000.01, 0.10, 110000.0, 9343.0),
            "NON_CONVIENTE")
        self.assertEqual(
            mh910_verdetto(-1005.51, 0.10, 110000.0, 8746.0),
            "MARGINALE")
        # Con tolleranza zero ogni VAN positivo e
        # CONVIENTE (soglia zero) e ogni VAN
        # negativo e NON_CONVIENTE.
        self.assertEqual(
            mh910_verdetto(6434.43, 0.0, 110000.0, 9343.0),
            "CONVIENTE")
        self.assertEqual(
            mh910_verdetto(-1.0, 0.0, 110000.0, 9343.0),
            "NON_CONVIENTE")
        self.assertEqual(
            mh910_verdetto(0.0, 0.0, 110000.0, 9343.0),
            "MARGINALE")
        with self.assertRaises(ValueError):
            mh910_verdetto(100.0, 1.5, 110000.0, 9343.0)
        with self.assertRaises(ValueError):
            mh910_verdetto(100.0, 0.10, -1.0, 9343.0)

    def test_verdetto_none_non_calcolabile(self):
        self.assertEqual(
            mh910_verdetto(None, 0.10, 110000.0, 9343.0),
            "NON_CALCOLABILE")
        self.assertEqual(
            mh910_verdetto(None, 0.0, 0.0, 9343.0),
            "NON_CALCOLABILE")
        self.assertEqual(
            mh910_verdetto(100.0, 0.10, 110000.0, None),
            "NON_CALCOLABILE")

    def test_verdetto_margine_zero_negativo_non_calcolabile(self):
        self.assertEqual(
            mh910_verdetto(-110000.0, 0.10, 110000.0, 0.0),
            "NON_CALCOLABILE")
        self.assertEqual(
            mh910_verdetto(-134924.42, 0.10, 110000.0, -2000.0),
            "NON_CALCOLABILE")
        self.assertEqual(
            mh910_verdetto(6434.43, 0.10, 110000.0, 9343.0),
            "MARGINALE")

    def test_verdetto_degenere_flag(self):
        self.assertEqual(
            mh910_verdetto(-110000.0, 0.10, 110000.0, 9343.0,
                           True),
            "NON_CALCOLABILE")
        self.assertEqual(
            mh910_verdetto(6434.43, 0.10, 110000.0, 9343.0,
                           False),
            "MARGINALE")
        self.assertEqual(
            mh910_verdetto(0.0, 0.10, 0.0, 0.0, True),
            "NON_CALCOLABILE")

    def test_verdetto_capex_zero(self):
        # Con CAPEX zero la tolleranza non copre
        # nulla: ogni VAN positivo e CONVIENTE,
        # ogni VAN negativo e NON_CONVIENTE.
        self.assertEqual(
            mh910_verdetto(1.0, 0.10, 0.0, 9343.0),
            "CONVIENTE")
        self.assertEqual(
            mh910_verdetto(0.0, 0.10, 0.0, 9343.0),
            "MARGINALE")
        self.assertEqual(
            mh910_verdetto(-1.0, 0.10, 0.0, 9343.0),
            "NON_CONVIENTE")

    def test_valida_demo_ok(self):
        demo = mh910_demo()
        val = mh910_valida(*[demo[k] for k in _ORDINE_VALIDA])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_vita_zero_ammesso_negativa_no(self):
        demo = mh910_demo()
        val = mh910_valida(*[dict(demo, vita_anni=0)[k]
                             for k in _ORDINE_VALIDA])
        self.assertTrue(val["valido"])
        bc = mh910_calcola(**_demo_kwargs(vita_anni=0))
        self.assertEqual(bc["vita_anni"], 0)
        self.assertAlmostEqual(bc["van_eur"], -110000.0,
                               places=2)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        with self.assertRaises(ValueError):
            mh910_calcola(**_demo_kwargs(vita_anni=-1))
        with self.assertRaises(ValueError):
            mh910_calcola(**_demo_kwargs(vita_anni=2.5))

    def test_valida_potenza_zero_ammesso_negativa_no(self):
        demo = mh910_demo()
        val = mh910_valida(*[dict(demo, potenza_kwp=0.0)[k]
                             for k in _ORDINE_VALIDA])
        self.assertTrue(val["valido"])
        bc = mh910_calcola(**_demo_kwargs(potenza_kwp=0.0))
        self.assertEqual(bc["e_immessa_kwh"], 0.0)
        self.assertEqual(bc["capex_eur"], 0.0)
        self.assertEqual(bc["margine_eur_anno"], 0.0)
        self.assertEqual(bc["van_eur"], 0.0)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        with self.assertRaises(ValueError):
            mh910_calcola(**_demo_kwargs(potenza_kwp=-1.0))

    def test_valida_corrispettivo_sopra_uno_no(self):
        with self.assertRaises(ValueError):
            mh910_calcola(
                **_demo_kwargs(corrispettivo_frazione=1.01))
        with self.assertRaises(ValueError):
            mh910_calcola(
                **_demo_kwargs(corrispettivo_frazione=-0.01))
        bc = mh910_calcola(
            **_demo_kwargs(corrispettivo_frazione=1.0))
        self.assertEqual(bc["ricavo_netto_eur_anno"], 0.0)
        self.assertEqual(bc["margine_eur_anno"], -2000.0)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        self.assertIsNone(bc["be_zonale_eur_kwh"])
        self.assertIsNone(bc["be_pmg_eur_kwh"])

    def test_valida_tasso_negativo_no_senza_tetto(self):
        with self.assertRaises(ValueError):
            mh910_calcola(**_demo_kwargs(tasso_frazione=-0.01))
        bc = mh910_calcola(**_demo_kwargs(tasso_frazione=0.5))
        self.assertAlmostEqual(bc["van_eur"], -91319.62,
                               places=2)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_valida_tolleranza_sopra_uno_no(self):
        with self.assertRaises(ValueError):
            mh910_calcola(**_demo_kwargs(tol_frazione=1.01))
        with self.assertRaises(ValueError):
            mh910_calcola(**_demo_kwargs(tol_frazione=-0.01))
        bc = mh910_calcola(**_demo_kwargs(tol_frazione=0.0))
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_valida_nan_no(self):
        demo = mh910_demo()
        val = mh910_valida(*[dict(demo, tasso_frazione=float("nan"))[k]
                             for k in _ORDINE_VALIDA])
        self.assertFalse(val["valido"])
        self.assertIn("tasso", val["errore"])

    def test_valida_negativi_no(self):
        demo = mh910_demo()
        for chiave in ("produzione_specifica",
                       "prezzo_zonale_eur_kwh", "pmg_eur_kwh",
                       "om_eur_kwp_anno", "capex_eur_kwp"):
            with self.subTest(chiave=chiave):
                val = mh910_valida(
                    *[dict(demo, **{chiave: -1.0})[k]
                      for k in _ORDINE_VALIDA])
                self.assertFalse(val["valido"])

    def test_valida_non_interi_no(self):
        with self.assertRaises(ValueError):
            mh910_calcola(**_demo_kwargs(vita_anni=2.5))
        with self.assertRaises(ValueError):
            mh910_calcola(**_demo_kwargs(vita_anni="20"))

    def test_calcola_accetta_dict(self):
        bc = mh910_calcola(mh910_demo())
        self.assertAlmostEqual(bc["van_eur"], 6434.43,
                               places=2)
        self.assertEqual(bc["verdetto"], "MARGINALE")

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh910_calcola(mh910_demo(),
                           prezzo_zonale_eur_kwh=0.12)
        self.assertAlmostEqual(bc["van_eur"], 43634.13,
                               places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_calcola_senza_scenari_anti_ricorsione(self):
        bc = mh910_calcola(_scenari=False, **mh910_demo())
        self.assertEqual(bc["scenari"], [])
        self.assertIsNone(bc["scenario_base"])
        self.assertAlmostEqual(bc["van_eur"], 6434.43,
                               places=2)
        self.assertEqual(len(bc["df_confronto"]), 3)

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
        for alt, atteso in _DEMO_CONFRONTO.items():
            for chiave, valore in atteso.items():
                with self.subTest(alternativa=alt, chiave=chiave):
                    ottenuto = bc["confronto"][alt][chiave]
                    if valore is None or isinstance(valore, (int, str)):
                        self.assertEqual(ottenuto, valore)
                    else:
                        self.assertLess(_rel(ottenuto, valore), 1e-9)
        # Ordinamento: RID sopra merchant sopra PPA.
        self.assertGreater(bc["confronto"]["rid"]["van_eur"],
                           bc["confronto"]["merchant"]["van_eur"])
        self.assertGreater(
            bc["confronto"]["merchant"]["van_eur"],
            bc["confronto"]["ppa"]["van_eur"])
        self.assertGreater(
            bc["confronto"]["rid"]["margine_eur_anno"],
            bc["confronto"]["merchant"]["margine_eur_anno"])
        self.assertGreater(
            bc["confronto"]["merchant"]["margine_eur_anno"],
            bc["confronto"]["ppa"]["margine_eur_anno"])
        self.assertEqual(bc["confronto"]["rid"]["verdetto"],
                         "MARGINALE")
        self.assertEqual(bc["confronto"]["ppa"]["verdetto"],
                         "MARGINALE")
        self.assertEqual(
            bc["confronto"]["merchant"]["verdetto"],
            "MARGINALE")

    def test_demo_verdetto_principale(self):
        bc = demo_calcoli()
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertGreater(bc["van_eur"], 0.0)
        self.assertLess(bc["van_eur"], 11000.0)
        self.assertAlmostEqual(bc["tir_frazione"], 0.0568,
                               places=4)
        self.assertAlmostEqual(bc["be_zonale_eur_kwh"],
                               0.0907, places=4)
        self.assertAlmostEqual(bc["be_zonale_eur_mwh"],
                               90.68, places=2)
        self.assertEqual(bc["be_pmg_eur_kwh"], 0.0)
        self.assertEqual(bc["scenario_base"]["verdetto"],
                         "MARGINALE")
        self.assertEqual(bc["payback_anni"], 12)
        self.assertAlmostEqual(bc["co2_t_anno"], 30.0,
                               places=2)
        # Il VAN positivo e sotto la tolleranza:
        # MARGINALE, non CONVIENTE.
        self.assertLessEqual(
            abs(bc["van_eur"]),
            bc["tol_frazione"] * bc["capex_eur"])

    def test_coerenza_fisica_e_costi(self):
        bc = demo_calcoli()
        self.assertAlmostEqual(
            bc["e_immessa_kwh"],
            bc["potenza_kwp"] * bc["produzione_specifica"])
        self.assertAlmostEqual(
            bc["capex_eur"],
            bc["capex_eur_kwp"] * bc["potenza_kwp"])
        self.assertAlmostEqual(
            bc["prezzo_unitario_eur_kwh"],
            max(bc["prezzo_zonale_eur_kwh"],
                bc["pmg_eur_kwh"]))
        self.assertAlmostEqual(
            bc["ricavo_lordo_eur_anno"],
            bc["e_immessa_kwh"]
            * bc["prezzo_unitario_eur_kwh"])
        self.assertAlmostEqual(
            bc["corrispettivo_eur_anno"],
            bc["ricavo_lordo_eur_anno"]
            * bc["corrispettivo_frazione"])
        self.assertAlmostEqual(
            bc["ricavo_netto_eur_anno"],
            bc["ricavo_lordo_eur_anno"]
            - bc["corrispettivo_eur_anno"])
        self.assertAlmostEqual(
            bc["costi_eur_anno"],
            bc["om_eur_kwp_anno"] * bc["potenza_kwp"])
        self.assertAlmostEqual(
            bc["margine_eur_anno"],
            bc["ricavo_netto_eur_anno"] - bc["costi_eur_anno"])
        self.assertAlmostEqual(
            bc["van_eur"],
            -bc["capex_eur"] + bc["margine_eur_anno"]
            * mh910_annuity(bc["vita_anni"],
                            bc["tasso_frazione"]))
        self.assertAlmostEqual(
            bc["be_zonale_eur_mwh"],
            bc["be_zonale_eur_kwh"] * 1000.0)
        self.assertAlmostEqual(
            bc["co2_t_anno"],
            bc["e_immessa_kwh"] * 0.25 / 1000.0)
        self.assertAlmostEqual(
            bc["payback_fraz_anni"],
            11.0 + (bc["capex_eur"] - 11.0
                    * bc["margine_eur_anno"])
            / bc["margine_eur_anno"])
        conf = bc["confronto"]
        self.assertEqual(conf["rid"]["van_eur"], bc["van_eur"])
        self.assertEqual(conf["rid"]["tir_frazione"],
                         bc["tir_frazione"])
        self.assertEqual(conf["rid"]["payback_anni"],
                         bc["payback_anni"])
        self.assertEqual(conf["rid"]["verdetto"], bc["verdetto"])
        # Flussi: anno zero meno CAPEX, poi
        # margine per ogni anno di vita utile; il
        # cumulato supera il CAPEX al
        # dodicesimo anno.
        fl = bc["df_flussi"]
        self.assertEqual(len(fl), 21)
        self.assertAlmostEqual(fl["Flusso (EUR)"].iloc[0],
                               -110000.0, places=2)
        self.assertEqual(fl["Flusso (EUR)"].iloc[1], 9343.0)
        self.assertAlmostEqual(
            fl["Cumulato (EUR)"].iloc[11], -7227.0, places=2)
        self.assertAlmostEqual(
            fl["Cumulato (EUR)"].iloc[12], 2116.0, places=2)
        self.assertAlmostEqual(
            fl["Cumulato (EUR)"].iloc[20], 76860.0, places=2)
        # Ricavo contro costi: il lordo meno il
        # corrispettivo da il netto, il margine e
        # netto meno costi, il VAN e positivo ma
        # dentro la tolleranza.
        rc = bc["df_ricavo_costi"]
        self.assertEqual(len(rc), 6)
        self.assertAlmostEqual(
            rc["Valore"].iloc[0], 11400.0, places=2)
        self.assertAlmostEqual(
            rc["Valore"].iloc[1], 57.0, places=2)
        self.assertAlmostEqual(
            rc["Valore"].iloc[2], 11343.0, places=2)
        self.assertAlmostEqual(
            rc["Valore"].iloc[3], 2000.0, places=2)
        self.assertAlmostEqual(
            rc["Valore"].iloc[4], 9343.0, places=2)
        self.assertAlmostEqual(
            rc["Valore"].iloc[5], 6434.43, places=2)

    def test_scenari_ordinamento_e_invarianza(self):
        bc = demo_calcoli()
        base = bc["scenari"][0]
        # Prezzo zonale 0,12: VAN positivo sopra la
        # tolleranza, CONVIENTE; il breakeven
        # prezzo zonale e INVARIANTE al prezzo
        # corrente.
        self.assertGreater(
            bc["scenari"][1]["van_eur"], base["van_eur"])
        self.assertGreater(bc["scenari"][1]["van_eur"], 11000.0)
        self.assertEqual(bc["scenari"][1]["verdetto"],
                         "CONVIENTE")
        self.assertEqual(
            bc["scenari"][1]["be_zonale_eur_kwh"],
            base["be_zonale_eur_kwh"])
        self.assertEqual(bc["scenari"][1]["payback_anni"], 9)
        # Prezzo zonale 0,07: il PMG fa da
        # pavimento a 0,09, il VAN resta dentro
        # la tolleranza, MARGINALE; il breakeven
        # PMG sale a 0,0907.
        self.assertLess(bc["scenari"][2]["van_eur"],
                        base["van_eur"])
        self.assertLess(bc["scenari"][2]["van_eur"], 0.0)
        self.assertEqual(bc["scenari"][2]["verdetto"],
                         "MARGINALE")
        self.assertEqual(bc["scenari"][2]["payback_anni"], 13)
        self.assertAlmostEqual(
            bc["scenari"][2]["be_pmg_eur_kwh"], 0.0907,
            places=4)
        self.assertEqual(
            bc["scenari"][2]["be_zonale_eur_kwh"],
            base["be_zonale_eur_kwh"])
        # PMG 0: identico alla base (il prezzo
        # zonale sta gia sopra il PMG).
        self.assertEqual(bc["scenari"][3]["van_eur"],
                         base["van_eur"])
        self.assertEqual(bc["scenari"][3]["verdetto"],
                         "MARGINALE")
        self.assertEqual(bc["scenari"][3]["be_pmg_eur_kwh"],
                         0.0)
        # CAPEX 800 EUR/kWp: VAN positivo sopra
        # la tolleranza, breakeven prezzo zonale
        # a zero (il PMG da solo basta).
        self.assertGreater(bc["scenari"][4]["van_eur"],
                           base["van_eur"])
        self.assertEqual(bc["scenari"][4]["verdetto"],
                         "CONVIENTE")
        self.assertEqual(bc["scenari"][4]["payback_anni"], 9)
        self.assertEqual(
            bc["scenari"][4]["be_zonale_eur_kwh"], 0.0)
        self.assertEqual(
            bc["scenari"][4]["be_pmg_eur_kwh"], 0.0)
        # Tasso 8 per cento: VAN piu negativo,
        # NON_CONVIENTE, TIR invariata (la TIR
        # non dipende dal tasso inserito).
        self.assertLess(bc["scenari"][5]["van_eur"],
                        base["van_eur"])
        self.assertEqual(bc["scenari"][5]["verdetto"],
                         "NON_CONVIENTE")
        self.assertEqual(bc["scenari"][5]["tir_frazione"],
                         base["tir_frazione"])
        self.assertEqual(bc["scenari"][5]["payback_anni"], 12)
        self.assertAlmostEqual(
            bc["scenari"][5]["be_zonale_eur_kwh"], 0.1106,
            places=4)

    def test_sensibilita_valori(self):
        s = mh910_sensibilita(**mh910_demo())
        self.assertEqual(set(s.keys()),
                         {"zon012", "zon007", "pmg0",
                          "capex800", "tasso8", "pot0",
                          "zon0", "pmg0zon0", "capex0",
                          "vita0", "tasso0", "prod0",
                          "om11343", "om0", "vita30",
                          "prod1500"})
        attesi = {
            "zon012": (43634.13, 9.32, 9, 0.09, 0.00,
                       "CONVIENTE"),
            "zon007": (-1005.51, 4.89, 13, 0.09, 0.09,
                       "MARGINALE"),
            "pmg0": (6434.43, 5.68, 12, 0.09, 0.00,
                     "MARGINALE"),
            "capex800": (36434.43, 9.92, 9, 0.00, 0.00,
                         "CONVIENTE"),
            "tasso8": (-18269.05, 5.68, 12, 0.11, 0.11,
                       "NON_CONVIENTE"),
            "pot0": (0.0, None, 0, None, None,
                     "NON_CALCOLABILE"),
            "zon0": (-1005.51, 4.89, 13, 0.09, 0.09,
                     "MARGINALE"),
            "pmg0zon0": (-134924.42, None, None, 0.09, 0.09,
                         "NON_CALCOLABILE"),
            "capex0": (116434.43, None, 0, 0.00, 0.00,
                       "CONVIENTE"),
            "vita0": (-110000.0, None, None, None, None,
                      "NON_CALCOLABILE"),
            "tasso0": (76860.0, 5.68, 12, 0.00, 0.00,
                       "CONVIENTE"),
            "prod0": (-134924.42, None, None, None, None,
                      "NON_CALCOLABILE"),
            "om11343": (-110000.0, None, None, 0.17, 0.17,
                        "NON_CALCOLABILE"),
            "om0": (31358.85, 8.17, 10, 0.00, 0.00,
                    "CONVIENTE"),
            "vita30": (33624.81, 7.53, 12, 0.00, 0.00,
                       "CONVIENTE"),
            "prod1500": (41774.14, 9.15, 10, 0.00, 0.00,
                         "CONVIENTE"),
        }
        for nome, (van, tirp, pb, bez, bep, vdc) in attesi.items():
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
                if bez is None:
                    self.assertIsNone(
                        s[nome]["be_zonale_eur_kwh"])
                else:
                    self.assertAlmostEqual(
                        s[nome]["be_zonale_eur_kwh"],
                        bez, places=2)
                if bep is None:
                    self.assertIsNone(
                        s[nome]["be_pmg_eur_kwh"])
                else:
                    self.assertAlmostEqual(
                        s[nome]["be_pmg_eur_kwh"],
                        bep, places=2)
                self.assertEqual(s[nome]["verdetto"], vdc)
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van_eur", caso)
            self.assertIn("tir_frazione", caso)
            self.assertIn("payback_anni", caso)
            self.assertIn("confronto", caso)
            self.assertIn("scenari", caso)


class TestCasiLimite(unittest.TestCase):
    def test_potenza_zero_non_calcolabile(self):
        bc = mh910_calcola(**_demo_kwargs(potenza_kwp=0.0))
        self.assertEqual(bc["e_immessa_kwh"], 0.0)
        self.assertEqual(bc["capex_eur"], 0.0)
        self.assertEqual(bc["ricavo_lordo_eur_anno"], 0.0)
        self.assertEqual(bc["ricavo_netto_eur_anno"], 0.0)
        self.assertEqual(bc["costi_eur_anno"], 0.0)
        self.assertEqual(bc["margine_eur_anno"], 0.0)
        self.assertEqual(bc["van_eur"], 0.0)
        self.assertIsNone(bc["tir_frazione"])
        self.assertEqual(bc["payback_anni"], 0)
        self.assertEqual(bc["payback_fraz_anni"], 0.0)
        self.assertIsNone(bc["be_zonale_eur_kwh"])
        self.assertIsNone(bc["be_zonale_eur_mwh"])
        self.assertIsNone(bc["be_pmg_eur_kwh"])
        self.assertEqual(bc["co2_t_anno"], 0.0)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_prezzo_zonale_zero_marginale(self):
        bc = mh910_calcola(
            **_demo_kwargs(prezzo_zonale_eur_kwh=0.0))
        self.assertEqual(bc["prezzo_unitario_eur_kwh"], 0.09)
        self.assertEqual(bc["ricavo_lordo_eur_anno"], 10800.0)
        self.assertEqual(bc["corrispettivo_eur_anno"], 54.0)
        self.assertEqual(bc["ricavo_netto_eur_anno"], 10746.0)
        self.assertEqual(bc["margine_eur_anno"], 8746.0)
        self.assertAlmostEqual(bc["van_eur"], -1005.51,
                               places=2)
        self.assertAlmostEqual(bc["tir_frazione"], 0.0489,
                               places=4)
        self.assertEqual(bc["payback_anni"], 13)
        self.assertAlmostEqual(bc["payback_fraz_anni"], 12.58,
                               places=2)
        self.assertAlmostEqual(bc["be_zonale_eur_kwh"],
                               0.0907, places=4)
        self.assertAlmostEqual(bc["be_pmg_eur_kwh"], 0.0907,
                               places=4)
        self.assertEqual(bc["verdetto"], "MARGINALE")

    def test_pmg_zero_e_prezzo_zero_non_calcolabile(self):
        bc = mh910_calcola(
            **_demo_kwargs(pmg_eur_kwh=0.0,
                           prezzo_zonale_eur_kwh=0.0))
        self.assertEqual(bc["prezzo_unitario_eur_kwh"], 0.0)
        self.assertEqual(bc["ricavo_lordo_eur_anno"], 0.0)
        self.assertEqual(bc["ricavo_netto_eur_anno"], 0.0)
        self.assertEqual(bc["costi_eur_anno"], 2000.0)
        self.assertEqual(bc["margine_eur_anno"], -2000.0)
        self.assertAlmostEqual(bc["van_eur"], -134924.42,
                               places=2)
        self.assertIsNone(bc["tir_frazione"])
        self.assertIsNone(bc["payback_anni"])
        self.assertIsNone(bc["payback_fraz_anni"])
        self.assertAlmostEqual(bc["be_zonale_eur_kwh"],
                               0.0907, places=4)
        self.assertAlmostEqual(bc["be_pmg_eur_kwh"], 0.0907,
                               places=4)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_capex_zero_conviente_payback_zero(self):
        bc = mh910_calcola(**_demo_kwargs(capex_eur_kwp=0.0))
        self.assertEqual(bc["capex_eur"], 0.0)
        self.assertEqual(bc["margine_eur_anno"], 9343.0)
        self.assertAlmostEqual(bc["van_eur"], 116434.43,
                               places=2)
        self.assertIsNone(bc["tir_frazione"])
        self.assertEqual(bc["payback_anni"], 0)
        self.assertEqual(bc["payback_fraz_anni"], 0.0)
        self.assertEqual(bc["be_zonale_eur_kwh"], 0.0)
        self.assertEqual(bc["be_zonale_eur_mwh"], 0.0)
        self.assertEqual(bc["be_pmg_eur_kwh"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_vita_zero_non_calcolabile(self):
        bc = mh910_calcola(**_demo_kwargs(vita_anni=0))
        self.assertEqual(bc["margine_eur_anno"], 9343.0)
        self.assertAlmostEqual(bc["van_eur"], -110000.0,
                               places=2)
        self.assertIsNone(bc["tir_frazione"])
        self.assertIsNone(bc["payback_anni"])
        self.assertIsNone(bc["payback_fraz_anni"])
        self.assertIsNone(bc["be_zonale_eur_kwh"])
        self.assertIsNone(bc["be_zonale_eur_mwh"])
        self.assertIsNone(bc["be_pmg_eur_kwh"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")
        self.assertEqual(len(bc["df_flussi"]), 1)

    def test_tasso_zero_conviente(self):
        bc = mh910_calcola(**_demo_kwargs(tasso_frazione=0.0))
        self.assertAlmostEqual(bc["van_eur"], 76860.0,
                               places=2)
        self.assertAlmostEqual(bc["tir_frazione"], 0.0568,
                               places=4)
        self.assertEqual(bc["payback_anni"], 12)
        self.assertAlmostEqual(bc["payback_fraz_anni"], 11.77,
                               places=2)
        self.assertEqual(bc["be_zonale_eur_kwh"], 0.0)
        self.assertEqual(bc["be_zonale_eur_mwh"], 0.0)
        self.assertEqual(bc["be_pmg_eur_kwh"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_produzione_zero_non_calcolabile(self):
        bc = mh910_calcola(
            **_demo_kwargs(produzione_specifica=0.0))
        self.assertEqual(bc["e_immessa_kwh"], 0.0)
        self.assertEqual(bc["ricavo_lordo_eur_anno"], 0.0)
        self.assertEqual(bc["ricavo_netto_eur_anno"], 0.0)
        self.assertEqual(bc["costi_eur_anno"], 2000.0)
        self.assertEqual(bc["margine_eur_anno"], -2000.0)
        self.assertAlmostEqual(bc["van_eur"], -134924.42,
                               places=2)
        self.assertIsNone(bc["tir_frazione"])
        self.assertIsNone(bc["payback_anni"])
        self.assertIsNone(bc["payback_fraz_anni"])
        self.assertIsNone(bc["be_zonale_eur_kwh"])
        self.assertIsNone(bc["be_zonale_eur_mwh"])
        self.assertIsNone(bc["be_pmg_eur_kwh"])
        self.assertEqual(bc["co2_t_anno"], 0.0)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_om_azzera_margine_non_calcolabile(self):
        bc = mh910_calcola(
            **_demo_kwargs(om_eur_kwp_anno=113.43))
        self.assertEqual(bc["costi_eur_anno"], 11343.0)
        self.assertEqual(bc["margine_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["van_eur"], -110000.0,
                               places=2)
        self.assertIsNone(bc["tir_frazione"])
        self.assertIsNone(bc["payback_anni"])
        self.assertIsNone(bc["payback_fraz_anni"])
        self.assertAlmostEqual(bc["be_zonale_eur_kwh"],
                               0.1689, places=4)
        self.assertAlmostEqual(bc["be_zonale_eur_mwh"],
                               168.93, places=2)
        self.assertAlmostEqual(bc["be_pmg_eur_kwh"], 0.1689,
                               places=4)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_om_zero_e_vita_30_e_produzione_1500(self):
        bc = mh910_calcola(**_demo_kwargs(om_eur_kwp_anno=0.0))
        self.assertEqual(bc["costi_eur_anno"], 0.0)
        self.assertEqual(bc["margine_eur_anno"], 11343.0)
        self.assertAlmostEqual(bc["van_eur"], 31358.85,
                               places=2)
        self.assertAlmostEqual(bc["tir_frazione"], 0.0817,
                               places=4)
        self.assertEqual(bc["payback_anni"], 10)
        self.assertEqual(bc["be_zonale_eur_kwh"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh910_calcola(**_demo_kwargs(vita_anni=30))
        self.assertAlmostEqual(bc["van_eur"], 33624.81,
                               places=2)
        self.assertAlmostEqual(bc["tir_frazione"], 0.0753,
                               places=4)
        self.assertEqual(bc["payback_anni"], 12)
        self.assertEqual(bc["be_zonale_eur_kwh"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh910_calcola(
            **_demo_kwargs(produzione_specifica=1500.0))
        self.assertEqual(bc["e_immessa_kwh"], 150000.0)
        self.assertEqual(bc["margine_eur_anno"], 12178.75)
        self.assertAlmostEqual(bc["van_eur"], 41774.14,
                               places=2)
        self.assertAlmostEqual(bc["tir_frazione"], 0.0915,
                               places=4)
        self.assertEqual(bc["payback_anni"], 10)
        self.assertAlmostEqual(bc["co2_t_anno"], 37.5,
                               places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_tolleranza_zero_demo_diventa_conviente(self):
        bc = mh910_calcola(**_demo_kwargs(tol_frazione=0.0))
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh910_calcola(**_demo_kwargs(tol_frazione=0.0,
                                          prezzo_zonale_eur_kwh=0.07))
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_van_invarianze(self):
        # Il VAN non dipende dal PMG quando il PMG
        # sta sotto il prezzo zonale, e non dipende
        # dal tasso per la TIR.
        bc0 = demo_calcoli()
        bc = mh910_calcola(**_demo_kwargs(pmg_eur_kwh=0.0))
        self.assertEqual(bc["van_eur"], bc0["van_eur"])
        self.assertEqual(bc["tir_frazione"],
                         bc0["tir_frazione"])
        bc = mh910_calcola(**_demo_kwargs(tasso_frazione=0.08))
        self.assertEqual(bc["tir_frazione"],
                         bc0["tir_frazione"])

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh910_csv(bc, mh910_demo())
        for voce in ("potenza_kwp", "e_immessa_kwh",
                     "prezzo_unitario_eur_kwh",
                     "ricavo_lordo_eur_anno",
                     "corrispettivo_eur_anno",
                     "ricavo_netto_eur_anno",
                     "margine_eur_anno", "van_eur",
                     "tir_frazione", "payback_anni",
                     "be_zonale_eur_kwh",
                     "be_zonale_eur_mwh",
                     "be_pmg_eur_kwh", "co2_t_anno",
                     "verdetto", "confronto_rid_van_eur",
                     "confronto_ppa_van_eur",
                     "confronto_merchant_van_eur",
                     "scenario_base_van_eur",
                     "scenario_zon012_van_eur",
                     "scenario_zon007_van_eur",
                     "scenario_pmg0_van_eur",
                     "scenario_capex800_van_eur",
                     "scenario_tasso8_van_eur"):
            self.assertIn(voce, csv)
        self.assertIn("6434.43", csv)
        self.assertIn("MARGINALE", csv)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh910_csv(bc, mh910_demo())
        righe = csv.strip().split("\n")
        self.assertEqual(righe[0], "voce;valore")
        self.assertTrue(all(";" in r for r in righe[1:]))

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(demo_calcoli()["van_eur"],
                         mh910_demo_calcoli()["van_eur"])
        self.assertEqual(demo_calcoli()["verdetto"],
                         mh910_demo_calcoli()["verdetto"])

    def test_df_scenari_confronto_tabella_flussi(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_scenari"]), 6)
        self.assertEqual(list(bc["df_scenari"]["Scenario"]),
                         ["Base", "Prezzo zonale 0,12 EUR/kWh",
                          "Prezzo zonale 0,07 EUR/kWh", "PMG 0",
                          "CAPEX 800 EUR/kWp", "Tasso 8 %"])
        self.assertEqual(len(bc["df_confronto"]), 3)
        self.assertEqual(list(bc["df_confronto"]["Alternativa"]),
                         ["RID", "PPA fisico", "Merchant"])
        self.assertEqual(len(bc["df_tabella"]), 27)
        self.assertEqual(len(bc["df_flussi"]), 21)
        self.assertEqual(len(bc["df_ricavo_costi"]), 6)

    def test_valida_rifiuta_stringhe_e_bool(self):
        demo = mh910_demo()
        val = mh910_valida(*[dict(demo, potenza_kwp="100")[k]
                             for k in _ORDINE_VALIDA])
        self.assertFalse(val["valido"])
        val = mh910_valida(*[dict(demo, vita_anni=True)[k]
                             for k in _ORDINE_VALIDA])
        self.assertFalse(val["valido"])


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def910\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh910_demo().keys()), lette - set(mh910_demo().keys()))
        self.assertEqual(lette, set(mh910_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc910\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc910\["([^"]+)"\]', src))
        attese = set(mh910_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestConteggioTitoliPreApply(unittest.TestCase):
    def test_conteggio_titoli_pre_apply(self):
        # Conteggio titoli: forma PRE-apply. Prima
        # dell'apply di questa scheda la copia di
        # lavoro del repo ha 909 blocchi scheda;
        # l'apply bumpa questo assert al conteggio
        # post apply 910.
        if os.path.exists(_APP_WD):
            src = open(_APP_WD, encoding="utf-8", errors="ignore").read()
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 910)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestCatenaPostApply(unittest.TestCase):
    def test_catena_finale_post_apply(self):
        # Coda della catena titoli post-apply: l'apply
        # ha appeso la scheda nuova in coda alla
        # catena lunga della copia di lavoro del repo.
        # (La forma pre-apply non e verificabile dopo
        # l'apply: la catena nuova e gia presente.)
        if not os.path.exists(_APP_WD):
            self.skipTest("nessuna copia di lavoro del repo trovata")
        src = open(_APP_WD, encoding="utf-8", errors="ignore").read()
        nuova = (", " + ", ".join("tab%d" % n for n in range(907, 911))
                + " = st.tabs([")
        self.assertIn(nuova, src)
        vecchia = (", " + ", ".join("tab%d" % n for n in range(907, 910))
                + " = st.tabs([")
        self.assertNotIn(vecchia, src)


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with " + _NUOVO_TAB + ":"), 1)
        self.assertTrue(src.startswith("    # W915"))

    def test_ui_scheda_nuova_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with " + _NUOVO_TAB + ":"), 1)
        self.assertIn("def mh910_demo(", src_h)
        self.assertIn("def mh910_calcola(", src_h)
        self.assertIn(_NUOVO_TAB, src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Ritiro Dedicato (RID): vendere l'energia al GSE paga?", src)
        self.assertIn("⚡🏛️ Ritiro Dedicato (RID): vendere l'energia al GSE paga?", src)
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
        chiavi = re.findall(r'key="(' + _NUOVO_ST + r'[^"]+)"', src)
        self.assertTrue(all(k.startswith(_NUOVO_ST) for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertEqual(len(chiavi), 17)
        self.assertIn('key="' + _NUOVO_ST + 'calcola"', src)
        self.assertIn('key="' + _NUOVO_ST + 'csv"', src)
        self.assertIn('key="' + _NUOVO_ST + 'csv_scenari"', src)
        self.assertIn('key="' + _NUOVO_ST + 'prezzo_zonale_eur_kwh"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg910"), src.index(".paiac("))
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
