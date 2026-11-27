"""Test nuova scheda CER: l'energia
condivisa paga?
Repo path: tests/test_w914_cer.py

Effetto ECONOMICO: una Comunita
Energetica Rinnovabile con impianto
fotovoltaico produce ogni anno
energia elettrica da un impianto in
kWp con una produzione specifica in
kWh/kWp/anno. Una quota della
produzione viene autoconsumata
fisicamente dai membri (risparmio
in bolletta al prezzo dell'energia
evitata); il resto viene immesso in
rete. Una quota dell'energia
immessa viene condivisa virtualmente
tra i membri e riceve la tariffa
premio del GSE in EUR/kWh;
l'energia immessa non condivisa
viene venduta con il ritiro
dedicato al prezzo di ritiro in
EUR/kWh. Il ricavo annuo e la somma
di risparmio in bolletta, ricavo
incentivo e ricavo ritiro. I costi
annui sono O&M per kWp piu gestione
della comunita: il margine annuo e
ricavo meno costi. Il VAN e meno
CAPEX piu margine per l'annualita a
tasso dato sulla vita utile; la TIR
e il tasso che azzera il VAN a
CAPEX fissato (bisezione); il
payback e il primo anno in cui il
cumulato del margine raggiunge il
CAPEX. Il breakeven incentivo e
l'incentivo che azzera il VAN
(formula chiusa, espresso anche in
EUR/MWh); il breakeven quota e la
quota condivisa che azzera il VAN
(formula chiusa, da margine lineare
nella quota). La CO2 evitata e kWh
annui prodotti per fattore CO2
diviso 1000 in t/anno.
Demo: potenza 200 kWp, produzione
specifica 1200 kWh/kWp/anno, quota
autoconsumo 0,20, prezzo energia
evitato 0,22 EUR/kWh, quota
condivisa 0,60, incentivo 0,11
EUR/kWh, prezzo ritiro 0,08
EUR/kWh, CAPEX 280.000 EUR, O&M 25
EUR/kWp/anno, gestione CER 3.000
EUR/anno, vita 20 anni, tasso 0,05,
tolleranza 0,10. E prod = 200 per
1200 = 240.000 kWh/anno. E auto =
240.000 per 0,20 = 48.000 kWh/anno.
Risparmio = 48.000 per 0,22 =
10.560 EUR/anno. E immessa =
240.000 meno 48.000 = 192.000
kWh/anno. E condivisa = 192.000 per
0,60 = 115.200 kWh/anno. Ricavo
incentivo = 115.200 per 0,11 =
12.672 EUR/anno. E resto = 192.000
meno 115.200 = 76.800 kWh/anno.
Ricavo ritiro = 76.800 per 0,08 =
6.144 EUR/anno. Ricavo = 10.560 piu
12.672 piu 6.144 = 29.376 EUR/anno.
Costi = 25 per 200 piu 3.000 =
8.000 EUR/anno. Margine = 29.376
meno 8.000 = 21.376 EUR/anno.
Annualita 20 anni al 5 per cento =
12,4622103425. VAN = meno 280.000
piu 21.376 per 12,4622103425 =
meno 13.607,79 EUR. TIR = 4,42 per
cento (CORREZIONE: il brief
attendeva circa 4,6 per cento, il
ricalcolo indipendente da 4,42 per
cento). Payback = 14 anni
(cumulato anno 13 = 277.888 sotto
CAPEX, anno 14 = 299.264 sopra
CAPEX; frazionale 13,10 anni).
Breakeven incentivo = 0,1195
EUR/kWh (119,48 EUR/MWh,
CORREZIONE: il brief attendeva
119,47 EUR/MWh, il ricalcolo
indipendente da 119,48 EUR/MWh).
Breakeven quota = 78,96 per cento
(CORREZIONE: il brief attendeva
78,94 per cento, il ricalcolo
indipendente da 78,96 per cento).
CO2 evitata = 240.000 per 0,25
diviso 1000 = 60 t/anno. Verdetto
MARGINALE.
Scenari: base potenza 200 kWp,
produzione 240.000 kWh, E auto
48.000 kWh, risparmio 10.560, E
condivisa 115.200 kWh, ricavo
incentivo 12.672, ricavo 29.376,
costi 8.000, margine 21.376, VAN
meno 13.607,79, TIR 4,42 per cento,
payback 14 anni, breakeven
incentivo 0,1195, breakeven quota
78,96 per cento, MARGINALE;
incentivo 0,13 EUR/kWh (ricavo
incentivo 14.976, ricavo 31.680,
margine 23.680, VAN 15.105,14, TIR
5,63 per cento, payback 12 anni,
breakeven incentivo 0,1195,
breakeven quota 47,37 per cento,
CONVIENTE); incentivo 0,08 EUR/kWh
(ricavo incentivo 9.216, ricavo
25.920, margine 17.920, VAN meno
56.677,19, TIR 2,48 per cento,
payback 16 anni, breakeven
incentivo 0,1195, breakeven quota
non definito, NON_CONVIENTE); quota
condivisa 0,80 (E condivisa
153.600 kWh, ricavo incentivo
16.896, E resto 38.400 kWh, ricavo
ritiro 3.072, ricavo 30.528,
margine 22.528, VAN 748,67, TIR
5,03 per cento, payback 13 anni,
breakeven incentivo 0,1096,
breakeven quota 78,96 per cento,
CONVIENTE); tasso 8 per cento (VAN
meno 70.127,28, TIR 4,42 per cento,
payback 14 anni, breakeven
incentivo 0,1720, breakeven quota
non definito, NON_CONVIENTE); CAPEX
1.000 EUR/kWp (CAPEX 200.000 EUR,
VAN 66.392,21, TIR 8,66 per cento,
payback 10 anni, breakeven
incentivo 0,0638, breakeven quota
0,00 per cento, CONVIENTE).
Confronto: E prod 240.000 contro E
auto 48.000, risparmio 10.560
contro E immessa 192.000, E
condivisa 115.200 contro ricavo
incentivo 12.672, E resto 76.800
contro ricavo ritiro 6.144, ricavo
29.376 contro costi 8.000, margine
21.376 contro VAN meno 13.607,79,
TIR 4,42 per cento contro payback
14 anni, breakeven incentivo 0,1195
EUR/kWh contro breakeven quota
78,96 per cento, CO2 60 t/anno.
Tolleranza in FRAZIONE (0,10 = 10 %
del CAPEX), usata diretta, NON
divisa per 100. Produzione, prezzi
e incentivo medi annui costanti,
SEMPLIFICAZIONE DICHIARATA (la
quota condivisa e un input:
l'energia condivisa e virtuale e si
calcola per fasce orarie, qui la
quota e un input); i flussi sono
solo sugli anni di vita utile,
SEMPLIFICAZIONE DICHIARATA. La CO2
evitata e kWh per fattore CO2
diviso 1000, SEMPLIFICAZIONE
DICHIARATA (il fattore 0,25
dipende da fonte, ora e stagione).
La TIR azzera il VAN a CAPEX
fissato (il CAPEX non viene
ricalcolato al variare del tasso).
Verdetto principale: MARGINALE.
Verdetto: NON_CALCOLABILE se il
margine annuo e zero o negativo
oppure se un input e degenere
(potenza negativa, produzione
specifica negativa, quota
autoconsumo negativa o sopra 1,
prezzo energia evitato negativo,
quota condivisa negativa o sopra 1,
incentivo negativo, prezzo ritiro
negativo, CAPEX negativo, O&M
negativo, gestione CER negativa,
vita negativa o non intera, tasso
negativo, tolleranza negativa o
sopra 1); altrimenti CONVIENTE se
il VAN e maggiore di 0, MARGINALE
se il VAN e minore o uguale a 0 e
il suo valore assoluto e minore o
uguale a tolleranza per CAPEX,
NON_CONVIENTE altrimenti.
La vita zero NON e degenere: da
VAN meno CAPEX, TIR None, payback
None e verdetto NON_CONVIENTE
(NOTA: il brief del ciclo elencava
la vita minore o uguale a zero tra
i degeneri ma elencava anche la
vita zero tra i casi limite con VAN
meno CAPEX e verdetto
NON_CONVIENTE: prevale il caso
limite concreto, come la durata
zero della scheda precedente, e la
vita negativa resta degenere).
La potenza zero NON e degenere: da
produzione zero, ricavo zero,
margine meno 3.000 e verdetto
NON_CALCOLABILE. Il CAPEX zero NON
e degenere: da VAN 266.392,21, TIR
None, payback 0 e verdetto
CONVIENTE. L'incentivo zero NON e
degenere: da ricavo incentivo zero
e VAN meno 171.528,92 con verdetto
NON_CONVIENTE.
Casi limite: potenza zero (margine
meno 3.000, VAN meno 317.386,63,
NON_CALCOLABILE); incentivo zero
(ricavo incentivo zero, margine
8.704, VAN meno 171.528,92,
NON_CONVIENTE); quota zero (E
condivisa zero, ricavo ritiro
15.360, VAN meno 56.677,19,
NON_CONVIENTE); quota 1,0 (E
condivisa 192.000 kWh, ricavo
incentivo 21.120, VAN 15.105,14,
CONVIENTE); CAPEX zero (VAN
266.392,21, TIR None, payback 0,
CONVIENTE); vita zero (VAN meno
280.000, TIR None, payback None,
NON_CONVIENTE); tasso zero (VAN
147.520, CONVIENTE); produzione
specifica zero (margine meno
8.000, VAN meno 379.697,68,
NON_CALCOLABILE); prezzo energia
evitato zero (risparmio zero, VAN
meno 145.208,73, NON_CONVIENTE);
prezzo ritiro zero (ricavo ritiro
zero, VAN meno 90.175,61,
NON_CONVIENTE).
Distinzione esplicita: qui SOLO il
MECCANISMO DI CONDIVISIONE
VIRTUALE piu TARIFFA PREMIO
sull'energia condivisa, NIENTE
fisica dell'impianto oltre la
produzione annua (le schede FV
dedicate coprono la produzione
fisica: qui la produzione annua in
kWh e un input), NIENTE
autoconsumo fisico dietro il
contatore da solo (solo risparmio
in bolletta, niente condivisione
virtuale e niente tariffa premio),
NIENTE vendita diretta al vicino
(prezzo bilaterale tra privati, non
tariffa premio del GSE
sull'energia condivisa), NIENTE
solo ritiro dedicato (solo vendita
dell'energia immessa, niente
premio), NIENTE certificato di
origine (titolo negoziabile sul
mercato, non incentivo: la scheda
dei Certificati Bianchi copre le
Garanzie di Origine), NIENTE Conto
Termico (contributo per il calore,
non per l'elettricita: la scheda
del Conto Termico copre il calore),
NIENTE detrazione fiscale (sconto
in dichiarazione dei redditi, non
incentivo del GSE: la scheda della
detrazione fiscale copre lo sconto
fiscale).
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w914_helpers import (
        demo_calcoli,
        mh909_annuity,
        mh909_be_incentivo,
        mh909_be_incentivo_mwh,
        mh909_be_quota,
        mh909_calcola,
        mh909_co2,
        mh909_confronto,
        mh909_costi,
        mh909_csv,
        mh909_demo,
        mh909_demo_calcoli,
        mh909_durata,
        mh909_e_auto,
        mh909_e_cond,
        mh909_e_immessa,
        mh909_e_prod,
        mh909_e_resto,
        mh909_fraz,
        mh909_intero,
        mh909_margine,
        mh909_nneg,
        mh909_num,
        mh909_payback,
        mh909_payback_fraz,
        mh909_pos,
        mh909_ricavo,
        mh909_ricavo_incentivo,
        mh909_ricavo_ritiro,
        mh909_risparmio_bolletta,
        mh909_scenario,
        mh909_sensibilita,
        mh909_tir,
        mh909_valida,
        mh909_van,
        mh909_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w914_helpers", os.path.join(_hf, "w914_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh909_annuity = _mod.mh909_annuity
    mh909_be_incentivo = _mod.mh909_be_incentivo
    mh909_be_incentivo_mwh = _mod.mh909_be_incentivo_mwh
    mh909_be_quota = _mod.mh909_be_quota
    mh909_calcola = _mod.mh909_calcola
    mh909_co2 = _mod.mh909_co2
    mh909_confronto = _mod.mh909_confronto
    mh909_costi = _mod.mh909_costi
    mh909_csv = _mod.mh909_csv
    mh909_demo = _mod.mh909_demo
    mh909_demo_calcoli = _mod.mh909_demo_calcoli
    mh909_durata = _mod.mh909_durata
    mh909_e_auto = _mod.mh909_e_auto
    mh909_e_cond = _mod.mh909_e_cond
    mh909_e_immessa = _mod.mh909_e_immessa
    mh909_e_prod = _mod.mh909_e_prod
    mh909_e_resto = _mod.mh909_e_resto
    mh909_fraz = _mod.mh909_fraz
    mh909_intero = _mod.mh909_intero
    mh909_margine = _mod.mh909_margine
    mh909_nneg = _mod.mh909_nneg
    mh909_num = _mod.mh909_num
    mh909_payback = _mod.mh909_payback
    mh909_payback_fraz = _mod.mh909_payback_fraz
    mh909_pos = _mod.mh909_pos
    mh909_ricavo = _mod.mh909_ricavo
    mh909_ricavo_incentivo = _mod.mh909_ricavo_incentivo
    mh909_ricavo_ritiro = _mod.mh909_ricavo_ritiro
    mh909_risparmio_bolletta = _mod.mh909_risparmio_bolletta
    mh909_scenario = _mod.mh909_scenario
    mh909_sensibilita = _mod.mh909_sensibilita
    mh909_tir = _mod.mh909_tir
    mh909_valida = _mod.mh909_valida
    mh909_van = _mod.mh909_van
    mh909_verdetto = _mod.mh909_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w914_helpers.py")
_UI_PATH = _risolvi("w914_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
# L'identificatore della scheda NUOVA e invece un
# letterale: la guard dell'apply richiede "tab909"
# in questo file (lezione w914: la costruzione
# dinamica faceva fallire l'apply).
_VECCHIO_MH = "mh90" + "8"
_VECCHIO_TAB = "tab90" + "8"
_VECCHIO_ST = "st90" + "8_"
_VECCHIO_SIGLA = "eco" + "bonus"
_NUOVO_TAB = "tab909"
_NUOVO_ST = "st90" + "9_"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO_SCALARI = {
    "e_prod_kwh": 240000.0,
    "e_auto_kwh": 48000.0,
    "risparmio_eur_anno": 10560.0,
    "e_immessa_kwh": 192000.0,
    "e_cond_kwh": 115200.0,
    "ricavo_incentivo_eur_anno": 12672.0,
    "e_resto_kwh": 76800.0,
    "ricavo_ritiro_eur_anno": 6144.0,
    "ricavo_eur_anno": 29376.0,
    "costi_eur_anno": 8000.0,
    "margine_eur_anno": 21376.0,
    "van_eur": -13607.791717865155,
    "tir_frazione": 0.04419804460453672,
    "payback_anni": 14,
    "payback_fraz_anni": 13.098802395209582,
    "be_incentivo_eur_kwh": 0.11947851053293021,
    "be_incentivo_eur_mwh": 119.47851053293022,
    "be_quota_frazione": 0.7895702106586043,
    "co2_t_anno": 60.0,
    "verdetto": "MARGINALE",
}

_DEMO_INPUT = {
    "potenza_kwp": 200.0,
    "produzione_specifica": 1200.0,
    "quota_autoconsumo": 0.20,
    "prezzo_energia_evitato": 0.22,
    "quota_condivisa": 0.60,
    "incentivo_eur_kwh": 0.11,
    "prezzo_ritiro_eur_kwh": 0.08,
    "capex_eur": 280000.0,
    "om_eur_kwp_anno": 25.0,
    "gestione_cer_eur_anno": 3000.0,
    "vita_anni": 20,
    "tasso_frazione": 0.05,
    "tol_frazione": 0.10,
}

_DEMO_SCENARI = [
    {"nome": "Base",
     "potenza_kwp": 200.0, "produzione_specifica": 1200.0,
     "quota_autoconsumo": 0.20,
     "prezzo_energia_evitato": 0.22,
     "quota_condivisa": 0.60,
     "incentivo_eur_kwh": 0.11,
     "prezzo_ritiro_eur_kwh": 0.08,
     "capex_eur": 280000.0, "om_eur_kwp_anno": 25.0,
     "gestione_cer_eur_anno": 3000.0, "vita_anni": 20,
     "tasso_frazione": 0.05, "tol_frazione": 0.10,
     "e_prod_kwh": 240000.0, "e_auto_kwh": 48000.0,
     "risparmio_eur_anno": 10560.0,
     "e_immessa_kwh": 192000.0, "e_cond_kwh": 115200.0,
     "ricavo_incentivo_eur_anno": 12672.0,
     "e_resto_kwh": 76800.0,
     "ricavo_ritiro_eur_anno": 6144.0,
     "ricavo_eur_anno": 29376.0, "costi_eur_anno": 8000.0,
     "margine_eur_anno": 21376.0,
     "van_eur": -13607.791717865155,
     "tir_frazione": 0.04419804460453672,
     "payback_anni": 14,
     "payback_fraz_anni": 13.098802395209582,
     "be_incentivo_eur_kwh": 0.11947851053293021,
     "be_incentivo_eur_mwh": 119.47851053293022,
     "be_quota_frazione": 0.7895702106586043,
     "co2_t_anno": 60.0, "verdetto": "MARGINALE"},
    {"nome": "Incentivo 0,13 EUR/kWh",
     "potenza_kwp": 200.0, "produzione_specifica": 1200.0,
     "quota_autoconsumo": 0.20,
     "prezzo_energia_evitato": 0.22,
     "quota_condivisa": 0.60,
     "incentivo_eur_kwh": 0.13,
     "prezzo_ritiro_eur_kwh": 0.08,
     "capex_eur": 280000.0, "om_eur_kwp_anno": 25.0,
     "gestione_cer_eur_anno": 3000.0, "vita_anni": 20,
     "tasso_frazione": 0.05, "tol_frazione": 0.10,
     "e_prod_kwh": 240000.0, "e_auto_kwh": 48000.0,
     "risparmio_eur_anno": 10560.0,
     "e_immessa_kwh": 192000.0, "e_cond_kwh": 115200.0,
     "ricavo_incentivo_eur_anno": 14976.0,
     "e_resto_kwh": 76800.0,
     "ricavo_ritiro_eur_anno": 6144.0,
     "ricavo_eur_anno": 31680.0, "costi_eur_anno": 8000.0,
     "margine_eur_anno": 23680.0,
     "van_eur": 15105.140911347,
     "tir_frazione": 0.05628173206963474,
     "payback_anni": 12,
     "payback_fraz_anni": 11.824324324324325,
     "be_incentivo_eur_kwh": 0.11947851053293021,
     "be_incentivo_eur_mwh": 119.47851053293022,
     "be_quota_frazione": 0.4737421263951626,
     "co2_t_anno": 60.0, "verdetto": "CONVIENTE"},
    {"nome": "Incentivo 0,08 EUR/kWh",
     "potenza_kwp": 200.0, "produzione_specifica": 1200.0,
     "quota_autoconsumo": 0.20,
     "prezzo_energia_evitato": 0.22,
     "quota_condivisa": 0.60,
     "incentivo_eur_kwh": 0.08,
     "prezzo_ritiro_eur_kwh": 0.08,
     "capex_eur": 280000.0, "om_eur_kwp_anno": 25.0,
     "gestione_cer_eur_anno": 3000.0, "vita_anni": 20,
     "tasso_frazione": 0.05, "tol_frazione": 0.10,
     "e_prod_kwh": 240000.0, "e_auto_kwh": 48000.0,
     "risparmio_eur_anno": 10560.0,
     "e_immessa_kwh": 192000.0, "e_cond_kwh": 115200.0,
     "ricavo_incentivo_eur_anno": 9216.0,
     "e_resto_kwh": 76800.0,
     "ricavo_ritiro_eur_anno": 6144.0,
     "ricavo_eur_anno": 25920.0, "costi_eur_anno": 8000.0,
     "margine_eur_anno": 17920.0,
     "van_eur": -56677.19066168336,
     "tir_frazione": 0.024757038099705725,
     "payback_anni": 16,
     "payback_fraz_anni": 15.625,
     "be_incentivo_eur_kwh": 0.11947851053293021,
     "be_incentivo_eur_mwh": 119.47851053293022,
     "be_quota_frazione": None,
     "co2_t_anno": 60.0, "verdetto": "NON_CONVIENTE"},
    {"nome": "Quota condivisa 0,80",
     "potenza_kwp": 200.0, "produzione_specifica": 1200.0,
     "quota_autoconsumo": 0.20,
     "prezzo_energia_evitato": 0.22,
     "quota_condivisa": 0.80,
     "incentivo_eur_kwh": 0.11,
     "prezzo_ritiro_eur_kwh": 0.08,
     "capex_eur": 280000.0, "om_eur_kwp_anno": 25.0,
     "gestione_cer_eur_anno": 3000.0, "vita_anni": 20,
     "tasso_frazione": 0.05, "tol_frazione": 0.10,
     "e_prod_kwh": 240000.0, "e_auto_kwh": 48000.0,
     "risparmio_eur_anno": 10560.0,
     "e_immessa_kwh": 192000.0, "e_cond_kwh": 153600.0,
     "ricavo_incentivo_eur_anno": 16896.0,
     "e_resto_kwh": 38400.0,
     "ricavo_ritiro_eur_anno": 3072.0,
     "ricavo_eur_anno": 30528.0, "costi_eur_anno": 8000.0,
     "margine_eur_anno": 22528.0,
     "van_eur": 748.6745967409224,
     "tir_frazione": 0.05031514257766381,
     "payback_anni": 13,
     "payback_fraz_anni": 12.428977272727273,
     "be_incentivo_eur_kwh": 0.10960888289969767,
     "be_incentivo_eur_mwh": 109.60888289969767,
     "be_quota_frazione": 0.7895702106586043,
     "co2_t_anno": 60.0, "verdetto": "CONVIENTE"},
    {"nome": "Tasso 8 %",
     "potenza_kwp": 200.0, "produzione_specifica": 1200.0,
     "quota_autoconsumo": 0.20,
     "prezzo_energia_evitato": 0.22,
     "quota_condivisa": 0.60,
     "incentivo_eur_kwh": 0.11,
     "prezzo_ritiro_eur_kwh": 0.08,
     "capex_eur": 280000.0, "om_eur_kwp_anno": 25.0,
     "gestione_cer_eur_anno": 3000.0, "vita_anni": 20,
     "tasso_frazione": 0.08, "tol_frazione": 0.10,
     "e_prod_kwh": 240000.0, "e_auto_kwh": 48000.0,
     "risparmio_eur_anno": 10560.0,
     "e_immessa_kwh": 192000.0, "e_cond_kwh": 115200.0,
     "ricavo_incentivo_eur_anno": 12672.0,
     "e_resto_kwh": 76800.0,
     "ricavo_ritiro_eur_anno": 6144.0,
     "ricavo_eur_anno": 29376.0, "costi_eur_anno": 8000.0,
     "margine_eur_anno": 21376.0,
     "van_eur": -70127.2810183639,
     "tir_frazione": 0.04419804460453672,
     "payback_anni": 14,
     "payback_fraz_anni": 13.098802395209582,
     "be_incentivo_eur_kwh": 0.17200189644515768,
     "be_incentivo_eur_mwh": 172.00189644515768,
     "be_quota_frazione": None,
     "co2_t_anno": 60.0, "verdetto": "NON_CONVIENTE"},
    {"nome": "CAPEX 1.000 EUR/kWp",
     "potenza_kwp": 200.0, "produzione_specifica": 1200.0,
     "quota_autoconsumo": 0.20,
     "prezzo_energia_evitato": 0.22,
     "quota_condivisa": 0.60,
     "incentivo_eur_kwh": 0.11,
     "prezzo_ritiro_eur_kwh": 0.08,
     "capex_eur": 200000.0, "om_eur_kwp_anno": 25.0,
     "gestione_cer_eur_anno": 3000.0, "vita_anni": 20,
     "tasso_frazione": 0.05, "tol_frazione": 0.10,
     "e_prod_kwh": 240000.0, "e_auto_kwh": 48000.0,
     "risparmio_eur_anno": 10560.0,
     "e_immessa_kwh": 192000.0, "e_cond_kwh": 115200.0,
     "ricavo_incentivo_eur_anno": 12672.0,
     "e_resto_kwh": 76800.0,
     "ricavo_ritiro_eur_anno": 6144.0,
     "ricavo_eur_anno": 29376.0, "costi_eur_anno": 8000.0,
     "margine_eur_anno": 21376.0,
     "van_eur": 66392.20828213484,
     "tir_frazione": 0.08656758590151292,
     "payback_anni": 10,
     "payback_fraz_anni": 9.3562874251497,
     "be_incentivo_eur_kwh": 0.0637544916505057,
     "be_incentivo_eur_mwh": 63.7544916505057,
     "be_quota_frazione": 0.0,
     "co2_t_anno": 60.0, "verdetto": "CONVIENTE"},
]

_DEMO_CONFRONTO = {
    "e_prod_kwh": 240000.0,
    "e_auto_kwh": 48000.0,
    "risparmio_eur_anno": 10560.0,
    "e_immessa_kwh": 192000.0,
    "e_cond_kwh": 115200.0,
    "ricavo_incentivo_eur_anno": 12672.0,
    "e_resto_kwh": 76800.0,
    "ricavo_ritiro_eur_anno": 6144.0,
    "ricavo_eur_anno": 29376.0,
    "costi_eur_anno": 8000.0,
    "margine_eur_anno": 21376.0,
    "van_eur": -13607.791717865155,
    "tir_frazione": 0.04419804460453672,
    "payback_anni": 14,
    "payback_fraz_anni": 13.098802395209582,
    "be_incentivo_eur_kwh": 0.11947851053293021,
    "be_incentivo_eur_mwh": 119.47851053293022,
    "be_quota_frazione": 0.7895702106586043,
    "co2_t_anno": 60.0,
    "verdetto": "MARGINALE",
}

_ORDINE_VALIDA = (
    "potenza_kwp", "produzione_specifica",
    "quota_autoconsumo", "prezzo_energia_evitato",
    "quota_condivisa", "incentivo_eur_kwh",
    "prezzo_ritiro_eur_kwh", "capex_eur",
    "om_eur_kwp_anno", "gestione_cer_eur_anno",
    "vita_anni", "tasso_frazione", "tol_frazione")


def _demo_kwargs(**over):
    kw = dict(mh909_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))

class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh909_num(3, "x"), 3.0)
        self.assertEqual(mh909_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh909_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh909_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh909_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh909_pos(0, "x")
        with self.assertRaises(ValueError):
            mh909_pos(-1, "x")
        self.assertEqual(mh909_pos(3, "x"), 3.0)

    def test_fraz_bordi(self):
        self.assertEqual(mh909_fraz(0, "x"), 0.0)
        self.assertEqual(mh909_fraz(1, "x"), 1.0)
        self.assertEqual(mh909_fraz(0.60, "x"), 0.60)
        with self.assertRaises(ValueError):
            mh909_fraz(-0.01, "x")
        with self.assertRaises(ValueError):
            mh909_fraz(1.01, "x")

    def test_durata_bordi(self):
        self.assertEqual(mh909_durata(0, "x"), 0)
        self.assertEqual(mh909_durata(20, "x"), 20)
        self.assertEqual(mh909_durata(20.0, "x"), 20)
        with self.assertRaises(ValueError):
            mh909_durata(-1, "x")
        with self.assertRaises(ValueError):
            mh909_durata(2.5, "x")
        with self.assertRaises(ValueError):
            mh909_durata(float("nan"), "x")

    def test_intero_bordi(self):
        self.assertEqual(mh909_intero(0, "x"), 0)
        self.assertEqual(mh909_intero(10, "x"), 10)
        self.assertEqual(mh909_intero(10.0, "x"), 10)
        with self.assertRaises(ValueError):
            mh909_intero(-1, "x")
        with self.assertRaises(ValueError):
            mh909_intero(2.5, "x")
        with self.assertRaises(ValueError):
            mh909_intero(float("nan"), "x")


class TestFisica(unittest.TestCase):
    def test_e_prod(self):
        self.assertEqual(mh909_e_prod(200.0, 1200.0), 240000.0)
        self.assertEqual(mh909_e_prod(0.0, 1200.0), 0.0)
        self.assertEqual(mh909_e_prod(200.0, 0.0), 0.0)
        self.assertEqual(mh909_e_prod(200.0, 1500.0), 300000.0)
        self.assertEqual(mh909_e_prod(100.0, 1200.0), 120000.0)
        with self.assertRaises(ValueError):
            mh909_e_prod(-1.0, 1200.0)
        with self.assertRaises(ValueError):
            mh909_e_prod(200.0, -1.0)

    def test_e_auto(self):
        self.assertEqual(mh909_e_auto(240000.0, 0.20), 48000.0)
        self.assertEqual(mh909_e_auto(240000.0, 0.0), 0.0)
        self.assertEqual(mh909_e_auto(240000.0, 1.0), 240000.0)
        self.assertEqual(mh909_e_auto(0.0, 0.20), 0.0)
        with self.assertRaises(ValueError):
            mh909_e_auto(240000.0, 1.01)
        with self.assertRaises(ValueError):
            mh909_e_auto(240000.0, -0.01)
        with self.assertRaises(ValueError):
            mh909_e_auto(-1.0, 0.20)

    def test_risparmio_bolletta(self):
        self.assertEqual(
            mh909_risparmio_bolletta(48000.0, 0.22), 10560.0)
        self.assertEqual(
            mh909_risparmio_bolletta(0.0, 0.22), 0.0)
        self.assertEqual(
            mh909_risparmio_bolletta(48000.0, 0.0), 0.0)
        self.assertEqual(
            mh909_risparmio_bolletta(240000.0, 0.22), 52800.0)
        self.assertEqual(
            mh909_risparmio_bolletta(48000.0, 0.30), 14400.0)
        with self.assertRaises(ValueError):
            mh909_risparmio_bolletta(48000.0, -0.01)

    def test_e_immessa(self):
        self.assertEqual(
            mh909_e_immessa(240000.0, 48000.0), 192000.0)
        self.assertEqual(
            mh909_e_immessa(240000.0, 0.0), 240000.0)
        self.assertEqual(
            mh909_e_immessa(240000.0, 240000.0), 0.0)
        self.assertEqual(mh909_e_immessa(0.0, 0.0), 0.0)
        with self.assertRaises(ValueError):
            mh909_e_immessa(-1.0, 48000.0)

    def test_e_cond(self):
        self.assertEqual(mh909_e_cond(192000.0, 0.60), 115200.0)
        self.assertEqual(mh909_e_cond(192000.0, 0.0), 0.0)
        self.assertEqual(mh909_e_cond(192000.0, 0.80), 153600.0)
        self.assertEqual(mh909_e_cond(192000.0, 1.0), 192000.0)
        self.assertEqual(mh909_e_cond(0.0, 0.60), 0.0)
        with self.assertRaises(ValueError):
            mh909_e_cond(192000.0, 1.01)
        with self.assertRaises(ValueError):
            mh909_e_cond(192000.0, -0.01)

    def test_ricavo_incentivo(self):
        self.assertEqual(
            mh909_ricavo_incentivo(115200.0, 0.11), 12672.0)
        self.assertEqual(
            mh909_ricavo_incentivo(115200.0, 0.13), 14976.0)
        self.assertEqual(
            mh909_ricavo_incentivo(115200.0, 0.08), 9216.0)
        self.assertEqual(
            mh909_ricavo_incentivo(115200.0, 0.0), 0.0)
        self.assertEqual(
            mh909_ricavo_incentivo(153600.0, 0.11), 16896.0)
        self.assertEqual(
            mh909_ricavo_incentivo(192000.0, 0.11), 21120.0)
        with self.assertRaises(ValueError):
            mh909_ricavo_incentivo(115200.0, -0.01)

    def test_e_resto(self):
        self.assertEqual(
            mh909_e_resto(192000.0, 115200.0), 76800.0)
        self.assertEqual(
            mh909_e_resto(192000.0, 0.0), 192000.0)
        self.assertEqual(
            mh909_e_resto(192000.0, 153600.0), 38400.0)
        self.assertEqual(
            mh909_e_resto(192000.0, 192000.0), 0.0)
        with self.assertRaises(ValueError):
            mh909_e_resto(-1.0, 115200.0)

    def test_ricavo_ritiro(self):
        self.assertEqual(
            mh909_ricavo_ritiro(76800.0, 0.08), 6144.0)
        self.assertEqual(
            mh909_ricavo_ritiro(192000.0, 0.08), 15360.0)
        self.assertEqual(
            mh909_ricavo_ritiro(38400.0, 0.08), 3072.0)
        self.assertEqual(mh909_ricavo_ritiro(0.0, 0.08), 0.0)
        self.assertEqual(
            mh909_ricavo_ritiro(76800.0, 0.0), 0.0)
        self.assertEqual(
            mh909_ricavo_ritiro(76800.0, 0.12), 9216.0)
        with self.assertRaises(ValueError):
            mh909_ricavo_ritiro(76800.0, -0.01)

    def test_ricavo(self):
        self.assertEqual(
            mh909_ricavo(10560.0, 12672.0, 6144.0), 29376.0)
        self.assertEqual(
            mh909_ricavo(10560.0, 14976.0, 6144.0), 31680.0)
        self.assertEqual(
            mh909_ricavo(10560.0, 0.0, 6144.0), 16704.0)
        self.assertEqual(
            mh909_ricavo(10560.0, 21120.0, 0.0), 31680.0)
        self.assertEqual(
            mh909_ricavo(10560.0, 12672.0, 0.0), 23232.0)
        self.assertEqual(mh909_ricavo(0.0, 0.0, 0.0), 0.0)
        with self.assertRaises(ValueError):
            mh909_ricavo(-1.0, 12672.0, 6144.0)

    def test_costi(self):
        self.assertEqual(
            mh909_costi(25.0, 200.0, 3000.0), 8000.0)
        self.assertEqual(
            mh909_costi(0.0, 200.0, 3000.0), 3000.0)
        self.assertEqual(
            mh909_costi(25.0, 200.0, 0.0), 5000.0)
        self.assertEqual(
            mh909_costi(25.0, 0.0, 3000.0), 3000.0)
        self.assertEqual(
            mh909_costi(25.0, 100.0, 3000.0), 5500.0)
        self.assertEqual(
            mh909_costi(50.0, 200.0, 3000.0), 13000.0)
        with self.assertRaises(ValueError):
            mh909_costi(-1.0, 200.0, 3000.0)
        with self.assertRaises(ValueError):
            mh909_costi(25.0, 200.0, -1.0)

    def test_margine(self):
        self.assertEqual(mh909_margine(29376.0, 8000.0), 21376.0)
        self.assertEqual(mh909_margine(31680.0, 8000.0), 23680.0)
        self.assertEqual(mh909_margine(16704.0, 8000.0), 8704.0)
        self.assertEqual(mh909_margine(0.0, 3000.0), -3000.0)
        self.assertEqual(mh909_margine(0.0, 8000.0), -8000.0)
        self.assertEqual(mh909_margine(29376.0, 3000.0), 26376.0)
        with self.assertRaises(ValueError):
            mh909_margine(-1.0, 8000.0)
        with self.assertRaises(ValueError):
            mh909_margine(29376.0, -1.0)

    def test_annuity(self):
        self.assertAlmostEqual(mh909_annuity(20, 0.05),
                               12.462210342539992, places=9)
        self.assertAlmostEqual(mh909_annuity(20, 0.08),
                               9.818147407449294, places=9)
        self.assertAlmostEqual(mh909_annuity(30, 0.05),
                               15.372451026418378, places=9)
        self.assertEqual(mh909_annuity(20, 0.0), 20.0)
        self.assertEqual(mh909_annuity(0, 0.05), 0.0)
        self.assertEqual(mh909_annuity(0, 0.0), 0.0)
        self.assertAlmostEqual(mh909_annuity(1, 0.05),
                               0.9523809523809523, places=9)
        with self.assertRaises(ValueError):
            mh909_annuity(-1, 0.05)
        with self.assertRaises(ValueError):
            mh909_annuity(2.5, 0.05)

    def test_van(self):
        self.assertAlmostEqual(
            mh909_van(280000.0, 21376.0, 20, 0.05),
            -13607.791717865155, places=2)
        self.assertAlmostEqual(
            mh909_van(280000.0, 23680.0, 20, 0.05),
            15105.140911347, places=2)
        self.assertAlmostEqual(
            mh909_van(280000.0, 17920.0, 20, 0.05),
            -56677.19066168336, places=2)
        self.assertAlmostEqual(
            mh909_van(280000.0, 22528.0, 20, 0.05),
            748.6745967409224, places=2)
        self.assertAlmostEqual(
            mh909_van(200000.0, 21376.0, 20, 0.05),
            66392.20828213484, places=2)
        self.assertEqual(mh909_van(280000.0, 21376.0, 0, 0.05),
                         -280000.0)
        self.assertAlmostEqual(
            mh909_van(0.0, 21376.0, 20, 0.05),
            266392.20828213484, places=2)
        self.assertAlmostEqual(
            mh909_van(280000.0, 21376.0, 20, 0.0),
            147520.0, places=2)
        self.assertAlmostEqual(
            mh909_van(280000.0, -3000.0, 20, 0.05),
            -317386.63102762, places=2)

    def test_tir(self):
        self.assertAlmostEqual(
            mh909_tir(280000.0, 21376.0, 20),
            0.04419804460453672, places=4)
        self.assertAlmostEqual(
            mh909_tir(280000.0, 23680.0, 20),
            0.05628173206963474, places=4)
        self.assertAlmostEqual(
            mh909_tir(280000.0, 17920.0, 20),
            0.024757038099705725, places=4)
        self.assertAlmostEqual(
            mh909_tir(280000.0, 22528.0, 20),
            0.05031514257766381, places=4)
        self.assertAlmostEqual(
            mh909_tir(200000.0, 21376.0, 20),
            0.08656758590151292, places=4)
        self.assertAlmostEqual(
            mh909_tir(280000.0, 8704.0, 20),
            -0.04154305719295642, places=4)
        self.assertAlmostEqual(
            mh909_tir(280000.0, 10816.0, 20),
            -0.023409260611920002, places=4)
        self.assertIsNone(mh909_tir(0.0, 21376.0, 20))
        self.assertIsNone(mh909_tir(280000.0, 0.0, 20))
        self.assertIsNone(mh909_tir(280000.0, -3000.0, 20))
        self.assertIsNone(mh909_tir(280000.0, 21376.0, 0))
        # Alla TIR il VAN a CAPEX fissato e zero.
        tir = mh909_tir(280000.0, 21376.0, 20)
        self.assertAlmostEqual(
            mh909_van(280000.0, 21376.0, 20, tir),
            0.0, places=2)

    def test_payback(self):
        self.assertEqual(
            mh909_payback(280000.0, 21376.0, 20), 14)
        self.assertEqual(
            mh909_payback(280000.0, 23680.0, 20), 12)
        self.assertEqual(
            mh909_payback(280000.0, 17920.0, 20), 16)
        self.assertEqual(
            mh909_payback(280000.0, 22528.0, 20), 13)
        self.assertEqual(
            mh909_payback(200000.0, 21376.0, 20), 10)
        self.assertEqual(
            mh909_payback(280000.0, 15232.0, 20), 19)
        self.assertEqual(mh909_payback(0.0, 21376.0, 20), 0)
        self.assertIsNone(
            mh909_payback(280000.0, 0.0, 20))
        self.assertIsNone(
            mh909_payback(280000.0, -3000.0, 20))
        self.assertIsNone(
            mh909_payback(280000.0, 21376.0, 0))
        # Margine troppo piccolo: mai entro la vita.
        self.assertIsNone(mh909_payback(280000.0, 8704.0, 20))
        self.assertEqual(mh909_payback(280000.0, 8704.0, 40),
                         33)

    def test_payback_fraz(self):
        self.assertAlmostEqual(
            mh909_payback_fraz(280000.0, 21376.0, 20),
            13.098802395209582, places=9)
        self.assertAlmostEqual(
            mh909_payback_fraz(280000.0, 23680.0, 20),
            11.824324324324325, places=9)
        self.assertAlmostEqual(
            mh909_payback_fraz(280000.0, 17920.0, 20),
            15.625, places=9)
        self.assertAlmostEqual(
            mh909_payback_fraz(280000.0, 22528.0, 20),
            12.428977272727273, places=9)
        self.assertAlmostEqual(
            mh909_payback_fraz(200000.0, 21376.0, 20),
            9.3562874251497, places=9)
        self.assertAlmostEqual(
            mh909_payback_fraz(280000.0, 15232.0, 20),
            18.38235294117647, places=9)
        self.assertEqual(
            mh909_payback_fraz(0.0, 21376.0, 20), 0.0)
        self.assertIsNone(
            mh909_payback_fraz(280000.0, 0.0, 20))
        self.assertIsNone(
            mh909_payback_fraz(280000.0, -3000.0, 20))
        self.assertIsNone(
            mh909_payback_fraz(280000.0, 21376.0, 0))
        # Payback mai raggiunto entro la vita:
        # frazionale None (formula legata a t).
        self.assertIsNone(
            mh909_payback_fraz(280000.0, 8704.0, 20))

    def test_be_incentivo(self):
        self.assertAlmostEqual(
            mh909_be_incentivo(280000.0, 10560.0, 6144.0,
                               8000.0, 115200.0, 20, 0.05),
            0.11947851053293021, places=4)
        self.assertAlmostEqual(
            mh909_be_incentivo(280000.0, 10560.0, 3072.0,
                               8000.0, 153600.0, 20, 0.05),
            0.10960888289969767, places=4)
        self.assertAlmostEqual(
            mh909_be_incentivo(280000.0, 10560.0, 6144.0,
                               8000.0, 115200.0, 20, 0.08),
            0.17200189644515768, places=4)
        self.assertAlmostEqual(
            mh909_be_incentivo(200000.0, 10560.0, 6144.0,
                               8000.0, 115200.0, 20, 0.05),
            0.0637544916505057, places=4)
        self.assertAlmostEqual(
            mh909_be_incentivo(280000.0, 10560.0, 0.0,
                               8000.0, 192000.0, 20, 0.05),
            0.10368710631975812, places=4)
        self.assertAlmostEqual(
            mh909_be_incentivo(280000.0, 10560.0, 6144.0,
                               8000.0, 115200.0, 20, 0.0),
            0.04597222222222222, places=4)
        self.assertAlmostEqual(
            mh909_be_incentivo(280000.0, 0.0, 6144.0,
                               8000.0, 115200.0, 20, 0.05),
            0.21114517719959688, places=4)
        self.assertAlmostEqual(
            mh909_be_incentivo(280000.0, 10560.0, 0.0,
                               8000.0, 115200.0, 20, 0.05),
            0.17281184386626355, places=4)
        # Valore negativo fissato a 0,0: CAPEX zero.
        self.assertEqual(
            mh909_be_incentivo(0.0, 10560.0, 6144.0,
                               8000.0, 115200.0, 20, 0.05),
            0.0)
        # E condivisa zero: None.
        self.assertIsNone(
            mh909_be_incentivo(280000.0, 10560.0, 15360.0,
                               8000.0, 0.0, 20, 0.05))
        # Vita zero: None.
        self.assertIsNone(
            mh909_be_incentivo(280000.0, 10560.0, 6144.0,
                               8000.0, 115200.0, 0, 0.05))
        with self.assertRaises(ValueError):
            mh909_be_incentivo(-1.0, 10560.0, 6144.0,
                               8000.0, 115200.0, 20, 0.05)
        # All'incentivo di breakeven il VAN e zero.
        bei = mh909_be_incentivo(280000.0, 10560.0, 6144.0,
                                 8000.0, 115200.0, 20, 0.05)
        bc = mh909_calcola(
            **_demo_kwargs(incentivo_eur_kwh=bei))
        self.assertAlmostEqual(bc["van_eur"], 0.0, places=2)

    def test_be_incentivo_invariante_incentivo_corrente(self):
        # Il breakeven incentivo e INVARIANTE
        # all'incentivo corrente.
        bc0 = demo_calcoli()
        bc = mh909_calcola(
            **_demo_kwargs(incentivo_eur_kwh=0.13))
        self.assertEqual(bc["be_incentivo_eur_kwh"],
                         bc0["be_incentivo_eur_kwh"])
        self.assertAlmostEqual(
            bc["be_incentivo_eur_kwh"], 0.1195, places=4)

    def test_be_incentivo_mwh(self):
        self.assertAlmostEqual(
            mh909_be_incentivo_mwh(0.11947851053293021),
            119.47851053293022, places=2)
        self.assertAlmostEqual(
            mh909_be_incentivo_mwh(0.10960888289969767),
            109.60888289969767, places=2)
        self.assertEqual(mh909_be_incentivo_mwh(0.0), 0.0)
        self.assertIsNone(mh909_be_incentivo_mwh(None))
        with self.assertRaises(ValueError):
            mh909_be_incentivo_mwh(-0.01)

    def test_be_quota(self):
        self.assertAlmostEqual(
            mh909_be_quota(280000.0, 10560.0, 192000.0, 0.08,
                           8000.0, 0.11, 20, 0.05),
            0.7895702106586043, places=4)
        self.assertAlmostEqual(
            mh909_be_quota(280000.0, 10560.0, 192000.0, 0.08,
                           8000.0, 0.13, 20, 0.05),
            0.4737421263951626, places=4)
        self.assertAlmostEqual(
            mh909_be_quota(280000.0, 10560.0, 192000.0, 0.0,
                           8000.0, 0.11, 20, 0.05),
            0.9426100574523466, places=4)
        self.assertAlmostEqual(
            mh909_be_quota(280000.0, 10560.0, 192000.0, 0.08,
                           5000.0, 0.11, 20, 0.05),
            0.26873687732527096, places=4)
        # Valore negativo fissato a 0,0: CAPEX 200.000.
        self.assertEqual(
            mh909_be_quota(200000.0, 10560.0, 192000.0, 0.08,
                           8000.0, 0.11, 20, 0.05),
            0.0)
        # Valore negativo fissato a 0,0: tasso zero.
        self.assertEqual(
            mh909_be_quota(280000.0, 10560.0, 192000.0, 0.08,
                           8000.0, 0.11, 20, 0.0),
            0.0)
        # Valore negativo fissato a 0,0: incentivo zero
        # (la quota non aiuta quando il premio e
        # sotto il ritiro dedicato).
        self.assertEqual(
            mh909_be_quota(280000.0, 10560.0, 192000.0, 0.08,
                           8000.0, 0.0, 20, 0.05),
            0.0)
        # Valore sopra 1: None (tasso 8 per cento).
        self.assertIsNone(
            mh909_be_quota(280000.0, 10560.0, 192000.0, 0.08,
                           8000.0, 0.11, 20, 0.08))
        # Denominatore zero: incentivo uguale al
        # prezzo ritiro.
        self.assertIsNone(
            mh909_be_quota(280000.0, 10560.0, 192000.0, 0.08,
                           8000.0, 0.08, 20, 0.05))
        # Vita zero: None.
        self.assertIsNone(
            mh909_be_quota(280000.0, 10560.0, 192000.0, 0.08,
                           8000.0, 0.11, 0, 0.05))
        with self.assertRaises(ValueError):
            mh909_be_quota(-1.0, 10560.0, 192000.0, 0.08,
                           8000.0, 0.11, 20, 0.05)
        # Alla quota di breakeven il VAN e zero.
        beq = mh909_be_quota(280000.0, 10560.0, 192000.0,
                             0.08, 8000.0, 0.11, 20, 0.05)
        bc = mh909_calcola(
            **_demo_kwargs(quota_condivisa=beq))
        self.assertAlmostEqual(bc["van_eur"], 0.0, places=2)

    def test_be_quota_invariante_quota_corrente(self):
        # Il breakeven quota e INVARIANTE
        # alla quota corrente.
        bc0 = demo_calcoli()
        bc = mh909_calcola(
            **_demo_kwargs(quota_condivisa=0.80))
        self.assertEqual(bc["be_quota_frazione"],
                         bc0["be_quota_frazione"])
        self.assertAlmostEqual(
            bc["be_quota_frazione"], 0.7896, places=4)

    def test_co2(self):
        self.assertEqual(mh909_co2(240000.0), 60.0)
        self.assertEqual(mh909_co2(0.0), 0.0)
        self.assertEqual(mh909_co2(300000.0), 75.0)
        self.assertEqual(mh909_co2(120000.0), 30.0)
        self.assertEqual(mh909_co2(1000.0), 0.25)
        with self.assertRaises(ValueError):
            mh909_co2(-1.0)

    def test_scenario_singolo(self):
        s = mh909_scenario("Incentivo 0,13 EUR/kWh",
                           mh909_demo(),
                           {"incentivo_eur_kwh": 0.13})
        self.assertEqual(s["nome"], "Incentivo 0,13 EUR/kWh")
        self.assertEqual(s["incentivo_eur_kwh"], 0.13)
        self.assertAlmostEqual(s["van_eur"], 15105.14,
                               places=2)
        self.assertEqual(s["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(s["be_incentivo_eur_kwh"],
                               0.1195, places=4)
        self.assertAlmostEqual(s["be_quota_frazione"], 0.4737,
                               places=4)
        s = mh909_scenario("Incentivo 0,08 EUR/kWh",
                           mh909_demo(),
                           {"incentivo_eur_kwh": 0.08})
        self.assertAlmostEqual(s["van_eur"], -56677.19,
                               places=2)
        self.assertEqual(s["payback_anni"], 16)
        self.assertIsNone(s["be_quota_frazione"])
        self.assertEqual(s["verdetto"], "NON_CONVIENTE")
        s = mh909_scenario("Quota condivisa 0,80",
                           mh909_demo(),
                           {"quota_condivisa": 0.80})
        self.assertAlmostEqual(s["e_cond_kwh"], 153600.0,
                               places=9)
        self.assertAlmostEqual(s["van_eur"], 748.67,
                               places=2)
        self.assertAlmostEqual(s["be_incentivo_eur_kwh"],
                               0.1096, places=4)
        s = mh909_scenario("Tasso 8 %", mh909_demo(),
                           {"tasso_frazione": 0.08})
        self.assertAlmostEqual(s["van_eur"], -70127.28,
                               places=2)
        self.assertEqual(s["verdetto"], "NON_CONVIENTE")
        s = mh909_scenario("CAPEX 1.000 EUR/kWp",
                           mh909_demo(),
                           {"capex_eur": 200000.0})
        self.assertAlmostEqual(s["van_eur"], 66392.21,
                               places=2)
        self.assertEqual(s["be_quota_frazione"], 0.0)
        self.assertEqual(s["verdetto"], "CONVIENTE")
        with self.assertRaises(ValueError):
            mh909_scenario("", mh909_demo(),
                           {"incentivo_eur_kwh": 0.13})
        with self.assertRaises(ValueError):
            mh909_scenario("X", mh909_demo(),
                           {"vita_anni": -1})

    def test_confronto_formule(self):
        c = mh909_confronto(240000.0, 48000.0, 10560.0,
                            192000.0, 115200.0, 12672.0,
                            76800.0, 6144.0, 29376.0, 8000.0,
                            21376.0, -13607.791717865155,
                            0.04419804460453672, 14,
                            13.098802395209582,
                            0.11947851053293021,
                            119.47851053293022,
                            0.7895702106586043, 60.0,
                            "MARGINALE")
        self.assertEqual(c["e_prod_kwh"], 240000.0)
        self.assertEqual(c["e_auto_kwh"], 48000.0)
        self.assertEqual(c["risparmio_eur_anno"], 10560.0)
        self.assertEqual(c["e_immessa_kwh"], 192000.0)
        self.assertEqual(c["e_cond_kwh"], 115200.0)
        self.assertEqual(c["ricavo_incentivo_eur_anno"],
                         12672.0)
        self.assertEqual(c["e_resto_kwh"], 76800.0)
        self.assertEqual(c["ricavo_ritiro_eur_anno"], 6144.0)
        self.assertEqual(c["ricavo_eur_anno"], 29376.0)
        self.assertEqual(c["costi_eur_anno"], 8000.0)
        self.assertEqual(c["margine_eur_anno"], 21376.0)
        self.assertEqual(c["van_eur"], -13607.791717865155)
        self.assertEqual(c["tir_frazione"],
                         0.04419804460453672)
        self.assertEqual(c["payback_anni"], 14)
        self.assertEqual(c["payback_fraz_anni"],
                         13.098802395209582)
        self.assertEqual(c["be_incentivo_eur_kwh"],
                         0.11947851053293021)
        self.assertEqual(c["be_incentivo_eur_mwh"],
                         119.47851053293022)
        self.assertEqual(c["be_quota_frazione"],
                         0.7895702106586043)
        self.assertEqual(c["co2_t_anno"], 60.0)
        self.assertEqual(c["verdetto"], "MARGINALE")
        c = mh909_confronto(0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                            0.0, 0.0, 0.0, 3000.0, -3000.0,
                            -317386.63102762, None, None,
                            None, None, None, None, 0.0,
                            "NON_CALCOLABILE")
        self.assertIsNone(c["tir_frazione"])
        self.assertIsNone(c["payback_anni"])
        self.assertIsNone(c["be_incentivo_eur_kwh"])
        self.assertIsNone(c["be_quota_frazione"])
        self.assertEqual(c["verdetto"], "NON_CALCOLABILE")
        with self.assertRaises(ValueError):
            mh909_confronto(240000.0, 48000.0, 10560.0,
                            192000.0, 115200.0, 12672.0,
                            76800.0, 6144.0, 29376.0, 8000.0,
                            21376.0, -13607.791717865155,
                            0.04419804460453672, 14,
                            13.098802395209582,
                            0.11947851053293021,
                            119.47851053293022,
                            0.7895702106586043, 60.0,
                            "FORSE")
        with self.assertRaises(ValueError):
            mh909_confronto(240000.0, 48000.0, 10560.0,
                            192000.0, 115200.0, 12672.0,
                            76800.0, 6144.0, 29376.0, 8000.0,
                            21376.0, -13607.791717865155,
                            0.04419804460453672, 14,
                            13.098802395209582,
                            0.11947851053293021,
                            119.47851053293022,
                            0.7895702106586043, -1.0,
                            "MARGINALE")

class TestFinanza(unittest.TestCase):
    def test_verdetto_bordi(self):
        self.assertEqual(
            mh909_verdetto(100.0, 0.10, 280000.0, 21376.0),
            "CONVIENTE")
        self.assertEqual(
            mh909_verdetto(0.0, 0.10, 280000.0, 21376.0),
            "MARGINALE")
        self.assertEqual(
            mh909_verdetto(-28000.0, 0.10, 280000.0, 21376.0),
            "MARGINALE")
        self.assertEqual(
            mh909_verdetto(-28001.0, 0.10, 280000.0, 21376.0),
            "NON_CONVIENTE")
        self.assertEqual(
            mh909_verdetto(-13607.79, 0.10, 280000.0, 21376.0),
            "MARGINALE")
        # Con tolleranza zero ogni VAN negativo
        # e NON_CONVIENTE (VAN zero compreso nel
        # MARGINALE solo perche il valore assoluto
        # zero e minore o uguale a zero).
        self.assertEqual(
            mh909_verdetto(-1.0, 0.0, 280000.0, 21376.0),
            "NON_CONVIENTE")
        self.assertEqual(
            mh909_verdetto(0.0, 0.0, 280000.0, 21376.0),
            "MARGINALE")
        with self.assertRaises(ValueError):
            mh909_verdetto(100.0, 1.5, 280000.0, 21376.0)
        with self.assertRaises(ValueError):
            mh909_verdetto(100.0, 0.10, -1.0, 21376.0)

    def test_verdetto_none_non_calcolabile(self):
        self.assertEqual(
            mh909_verdetto(None, 0.10, 280000.0, 21376.0),
            "NON_CALCOLABILE")
        self.assertEqual(
            mh909_verdetto(None, 0.0, 0.0, 21376.0),
            "NON_CALCOLABILE")
        self.assertEqual(
            mh909_verdetto(100.0, 0.10, 280000.0, None),
            "NON_CALCOLABILE")

    def test_verdetto_margine_zero_negativo_non_calcolabile(self):
        self.assertEqual(
            mh909_verdetto(-280000.0, 0.10, 280000.0, 0.0),
            "NON_CALCOLABILE")
        self.assertEqual(
            mh909_verdetto(-317386.63, 0.10, 280000.0, -3000.0),
            "NON_CALCOLABILE")
        self.assertEqual(
            mh909_verdetto(-13607.79, 0.10, 280000.0, 21376.0),
            "MARGINALE")

    def test_verdetto_capex_zero(self):
        # Con CAPEX zero la tolleranza non copre
        # nulla: ogni VAN negativo e NON_CONVIENTE.
        self.assertEqual(
            mh909_verdetto(-1.0, 0.10, 0.0, 21376.0),
            "NON_CONVIENTE")
        self.assertEqual(
            mh909_verdetto(0.0, 0.10, 0.0, 21376.0),
            "MARGINALE")

    def test_valida_demo_ok(self):
        demo = mh909_demo()
        val = mh909_valida(*[demo[k] for k in _ORDINE_VALIDA])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_vita_zero_ammesso_negativa_no(self):
        demo = mh909_demo()
        val = mh909_valida(*[dict(demo, vita_anni=0)[k]
                             for k in _ORDINE_VALIDA])
        self.assertTrue(val["valido"])
        bc = mh909_calcola(**_demo_kwargs(vita_anni=0))
        self.assertEqual(bc["vita_anni"], 0)
        self.assertAlmostEqual(bc["van_eur"], -280000.0,
                               places=2)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        with self.assertRaises(ValueError):
            mh909_calcola(**_demo_kwargs(vita_anni=-1))
        with self.assertRaises(ValueError):
            mh909_calcola(**_demo_kwargs(vita_anni=2.5))

    def test_valida_quote_sopra_uno_no(self):
        with self.assertRaises(ValueError):
            mh909_calcola(
                **_demo_kwargs(quota_autoconsumo=1.01))
        with self.assertRaises(ValueError):
            mh909_calcola(**_demo_kwargs(quota_condivisa=1.01))
        bc = mh909_calcola(**_demo_kwargs(quota_condivisa=1.0))
        self.assertEqual(bc["quota_condivisa"], 1.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh909_calcola(**_demo_kwargs(quota_condivisa=0.0))
        self.assertEqual(bc["quota_condivisa"], 0.0)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_valida_tasso_negativo_no_senza_tetto(self):
        with self.assertRaises(ValueError):
            mh909_calcola(**_demo_kwargs(tasso_frazione=-0.1))
        bc = mh909_calcola(**_demo_kwargs(tasso_frazione=0.0))
        self.assertEqual(bc["tasso_frazione"], 0.0)
        # Il brief pone come degenere solo il
        # tasso negativo: nessun tetto superiore
        # negli helper (il tetto 0,20 e solo
        # dello slider UI).
        bc = mh909_calcola(**_demo_kwargs(tasso_frazione=1.5))
        self.assertEqual(bc["tasso_frazione"], 1.5)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_valida_tolleranza_sopra_uno_no(self):
        with self.assertRaises(ValueError):
            mh909_calcola(**_demo_kwargs(tol_frazione=1.5))
        bc = mh909_calcola(**_demo_kwargs(tol_frazione=0.0))
        self.assertEqual(bc["tol_frazione"], 0.0)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(incentivo_eur_kwh=float("nan"))
        self.assertRaises(ValueError, mh909_calcola, **kw)
        kw = _demo_kwargs(tol_frazione=float("inf"))
        self.assertRaises(ValueError, mh909_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (
                ("potenza_kwp", -1),
                ("produzione_specifica", -1),
                ("quota_autoconsumo", -0.1),
                ("prezzo_energia_evitato", -0.1),
                ("quota_condivisa", -0.1),
                ("incentivo_eur_kwh", -0.1),
                ("prezzo_ritiro_eur_kwh", -0.1),
                ("capex_eur", -1),
                ("om_eur_kwp_anno", -1),
                ("gestione_cer_eur_anno", -1),
                ("tasso_frazione", -0.1),
                ("tol_frazione", -0.1)):
            with self.assertRaises(ValueError):
                mh909_calcola(**_demo_kwargs(**{campo: valore}))

    def test_valida_non_interi_no(self):
        with self.assertRaises(ValueError):
            mh909_calcola(**_demo_kwargs(vita_anni=2.5))

    def test_calcola_accetta_dict(self):
        bc = mh909_calcola(mh909_demo())
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertEqual(len(bc["scenari"]), 6)

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh909_calcola(dict(mh909_demo(),
                                incentivo_eur_kwh=999.0),
                           incentivo_eur_kwh=0.11)
        self.assertEqual(bc["incentivo_eur_kwh"], 0.11)

    def test_calcola_senza_scenari_anti_ricorsione(self):
        bc = mh909_calcola(_scenari=False, **mh909_demo())
        self.assertEqual(bc["scenari"], [])
        self.assertIsNone(bc["scenario_base"])
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertAlmostEqual(bc["van_eur"], -13607.79,
                               places=2)
        self.assertAlmostEqual(bc["be_incentivo_eur_kwh"],
                               0.1195, places=4)


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
        self.assertEqual(bc["verdetto"], "MARGINALE")
        self.assertLess(bc["van_eur"], 0.0)
        self.assertGreater(bc["van_eur"], -28000.0)
        self.assertAlmostEqual(bc["tir_frazione"], 0.0442,
                               places=4)
        self.assertAlmostEqual(bc["be_incentivo_eur_kwh"],
                               0.1195, places=4)
        self.assertAlmostEqual(bc["be_incentivo_eur_mwh"],
                               119.48, places=2)
        self.assertAlmostEqual(bc["be_quota_frazione"],
                               0.7896, places=4)
        self.assertEqual(bc["scenario_base"]["verdetto"],
                         "MARGINALE")
        self.assertEqual(bc["payback_anni"], 14)
        self.assertAlmostEqual(bc["co2_t_anno"], 60.0,
                               places=2)
        # Il VAN negativo e dentro la tolleranza:
        # MARGINALE, non NON_CONVIENTE.
        self.assertLessEqual(
            abs(bc["van_eur"]),
            bc["tol_frazione"] * bc["capex_eur"])

    def test_coerenza_fisica_e_costi(self):
        bc = demo_calcoli()
        self.assertAlmostEqual(
            bc["e_prod_kwh"],
            bc["potenza_kwp"] * bc["produzione_specifica"])
        self.assertAlmostEqual(
            bc["e_auto_kwh"],
            bc["e_prod_kwh"] * bc["quota_autoconsumo"])
        self.assertAlmostEqual(
            bc["risparmio_eur_anno"],
            bc["e_auto_kwh"]
            * bc["prezzo_energia_evitato"])
        self.assertAlmostEqual(
            bc["e_immessa_kwh"],
            bc["e_prod_kwh"] - bc["e_auto_kwh"])
        self.assertAlmostEqual(
            bc["e_cond_kwh"],
            bc["e_immessa_kwh"] * bc["quota_condivisa"])
        self.assertAlmostEqual(
            bc["ricavo_incentivo_eur_anno"],
            bc["e_cond_kwh"] * bc["incentivo_eur_kwh"])
        self.assertAlmostEqual(
            bc["e_resto_kwh"],
            bc["e_immessa_kwh"] - bc["e_cond_kwh"])
        self.assertAlmostEqual(
            bc["ricavo_ritiro_eur_anno"],
            bc["e_resto_kwh"]
            * bc["prezzo_ritiro_eur_kwh"])
        self.assertAlmostEqual(
            bc["ricavo_eur_anno"],
            bc["risparmio_eur_anno"]
            + bc["ricavo_incentivo_eur_anno"]
            + bc["ricavo_ritiro_eur_anno"])
        self.assertAlmostEqual(
            bc["costi_eur_anno"],
            bc["om_eur_kwp_anno"] * bc["potenza_kwp"]
            + bc["gestione_cer_eur_anno"])
        self.assertAlmostEqual(
            bc["margine_eur_anno"],
            bc["ricavo_eur_anno"] - bc["costi_eur_anno"])
        self.assertAlmostEqual(
            bc["van_eur"],
            -bc["capex_eur"] + bc["margine_eur_anno"]
            * mh909_annuity(bc["vita_anni"],
                            bc["tasso_frazione"]))
        self.assertAlmostEqual(
            bc["be_incentivo_eur_mwh"],
            bc["be_incentivo_eur_kwh"] * 1000.0)
        self.assertAlmostEqual(
            bc["co2_t_anno"],
            bc["e_prod_kwh"] * 0.25 / 1000.0)
        self.assertAlmostEqual(
            bc["payback_fraz_anni"],
            13.0 + (bc["capex_eur"] - 13.0
                    * bc["margine_eur_anno"])
            / bc["margine_eur_anno"])
        conf = bc["confronto"]
        self.assertEqual(conf["van_eur"], bc["van_eur"])
        self.assertEqual(conf["tir_frazione"],
                         bc["tir_frazione"])
        self.assertEqual(conf["payback_anni"],
                         bc["payback_anni"])
        self.assertEqual(conf["verdetto"], bc["verdetto"])
        # Flussi: anno zero meno CAPEX, poi
        # margine per ogni anno di vita utile; il
        # cumulato supera il CAPEX al
        # quattordicesimo anno.
        fl = bc["df_flussi"]
        self.assertEqual(len(fl), 21)
        self.assertAlmostEqual(fl["Flusso (EUR)"].iloc[0],
                               -280000.0, places=2)
        self.assertEqual(fl["Flusso (EUR)"].iloc[1], 21376.0)
        self.assertAlmostEqual(
            fl["Cumulato (EUR)"].iloc[13], -2112.0, places=2)
        self.assertAlmostEqual(
            fl["Cumulato (EUR)"].iloc[14], 19264.0, places=2)
        self.assertAlmostEqual(
            fl["Cumulato (EUR)"].iloc[20], 147520.0, places=2)
        # Ricavo contro costi: le tre gambe del
        # ricavo sommano al ricavo, il margine e
        # ricavo meno costi, il VAN e negativo ma
        # dentro la tolleranza.
        rc = bc["df_ricavo_costi"]
        self.assertEqual(len(rc), 7)
        self.assertAlmostEqual(
            rc["Valore"].iloc[0], 10560.0, places=2)
        self.assertAlmostEqual(
            rc["Valore"].iloc[1], 12672.0, places=2)
        self.assertAlmostEqual(
            rc["Valore"].iloc[2], 6144.0, places=2)
        self.assertAlmostEqual(
            rc["Valore"].iloc[3], 29376.0, places=2)
        self.assertAlmostEqual(
            rc["Valore"].iloc[4], 8000.0, places=2)
        self.assertAlmostEqual(
            rc["Valore"].iloc[5], 21376.0, places=2)
        self.assertAlmostEqual(
            rc["Valore"].iloc[6], -13607.79, places=2)

    def test_scenari_ordinamento_e_invarianza(self):
        bc = demo_calcoli()
        base = bc["scenari"][0]
        # Piu incentivo migliora il caso e diventa
        # CONVIENTE; il breakeven incentivo e
        # INVARIANTE all'incentivo corrente.
        self.assertGreater(
            bc["scenari"][1]["van_eur"], base["van_eur"])
        self.assertGreater(bc["scenari"][1]["van_eur"], 0.0)
        self.assertEqual(bc["scenari"][1]["verdetto"],
                         "CONVIENTE")
        self.assertEqual(
            bc["scenari"][1]["be_incentivo_eur_kwh"],
            base["be_incentivo_eur_kwh"])
        # Meno incentivo peggiora il caso e diventa
        # NON_CONVIENTE, con payback piu lungo e
        # breakeven quota non definito.
        self.assertLess(bc["scenari"][2]["van_eur"],
                        base["van_eur"])
        self.assertLess(bc["scenari"][2]["van_eur"], 0.0)
        self.assertEqual(bc["scenari"][2]["verdetto"],
                         "NON_CONVIENTE")
        self.assertEqual(bc["scenari"][2]["payback_anni"], 16)
        self.assertIsNone(
            bc["scenari"][2]["be_quota_frazione"])
        self.assertEqual(
            bc["scenari"][2]["be_incentivo_eur_kwh"],
            base["be_incentivo_eur_kwh"])
        # Quota 0,80: VAN appena positivo, il
        # breakeven quota e INVARIANTE alla quota
        # corrente.
        self.assertGreater(bc["scenari"][3]["van_eur"],
                           base["van_eur"])
        self.assertGreater(bc["scenari"][3]["van_eur"], 0.0)
        self.assertEqual(bc["scenari"][3]["verdetto"],
                         "CONVIENTE")
        self.assertEqual(bc["scenari"][3]["payback_anni"], 13)
        self.assertEqual(
            bc["scenari"][3]["be_quota_frazione"],
            base["be_quota_frazione"])
        # Tasso 8 per cento: VAN piu negativo, TIR
        # invariata (la TIR non dipende dal tasso
        # inserito).
        self.assertLess(bc["scenari"][4]["van_eur"],
                        base["van_eur"])
        self.assertEqual(bc["scenari"][4]["verdetto"],
                         "NON_CONVIENTE")
        self.assertEqual(bc["scenari"][4]["tir_frazione"],
                         base["tir_frazione"])
        self.assertEqual(bc["scenari"][4]["payback_anni"], 14)
        # CAPEX 1.000 EUR/kWp: VAN positivo, TIR
        # piu alta, breakeven quota a zero.
        self.assertGreater(bc["scenari"][5]["van_eur"],
                           base["van_eur"])
        self.assertEqual(bc["scenari"][5]["verdetto"],
                         "CONVIENTE")
        self.assertEqual(bc["scenari"][5]["payback_anni"], 10)
        self.assertEqual(
            bc["scenari"][5]["be_quota_frazione"], 0.0)

    def test_sensibilita_valori(self):
        s = mh909_sensibilita(**mh909_demo())
        self.assertEqual(set(s.keys()),
                         {"inc013", "inc008", "qc080",
                          "tasso8", "capex200k", "pot0",
                          "inc0", "qc0", "qc1", "capex0",
                          "vita0", "tasso0", "prod0", "pe0",
                          "pr0", "om0", "gest0", "vita30",
                          "qa0", "qa1", "prod1500"})
        attesi = {
            "inc013": (15105.14, 5.63, 12, 0.12, 0.47,
                       "CONVIENTE"),
            "inc008": (-56677.19, 2.48, 16, 0.12, None,
                       "NON_CONVIENTE"),
            "qc080": (748.67, 5.03, 13, 0.11, 0.79,
                      "CONVIENTE"),
            "tasso8": (-70127.28, 4.42, 14, 0.17, None,
                       "NON_CONVIENTE"),
            "capex200k": (66392.21, 8.66, 10, 0.06, 0.00,
                          "CONVIENTE"),
            "pot0": (-317386.63, None, None, None, None,
                     "NON_CALCOLABILE"),
            "inc0": (-171528.92, -4.15, None, 0.12, 0.00,
                     "NON_CONVIENTE"),
            "qc0": (-56677.19, 2.48, 16, None, 0.79,
                    "NON_CONVIENTE"),
            "qc1": (15105.14, 5.63, 12, 0.10, 0.79,
                    "CONVIENTE"),
            "capex0": (266392.21, None, 0, 0.00, 0.00,
                       "CONVIENTE"),
            "vita0": (-280000.0, None, None, None, None,
                      "NON_CONVIENTE"),
            "tasso0": (147520.0, 4.42, 14, 0.05, 0.00,
                       "CONVIENTE"),
            "prod0": (-379697.68, None, None, None, None,
                      "NON_CALCOLABILE"),
            "pe0": (-145208.73, -2.34, None, 0.21, None,
                    "NON_CONVIENTE"),
            "pr0": (-90175.61, 0.82, 19, 0.17, 0.94,
                    "NON_CONVIENTE"),
            "om0": (48703.26, 6.97, 11, 0.08, 0.00,
                    "CONVIENTE"),
            "gest0": (23778.84, 5.98, 12, 0.09, 0.27,
                      "CONVIENTE"),
            "vita30": (48601.51, 6.47, 14, 0.08, 0.05,
                       "CONVIENTE"),
            "qa0": (-86586.50, 1.00, 19, 0.16, None,
                    "NON_CONVIENTE"),
            "qa1": (278307.02, 15.03, 7, None, None,
                    "CONVIENTE"),
            "prod1500": (77914.68, 8.09, 10, 0.07, 0.00,
                         "CONVIENTE"),
        }
        for nome, (van, tirp, pb, bei, beq, vdc) in attesi.items():
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
                if bei is None:
                    self.assertIsNone(
                        s[nome]["be_incentivo_eur_kwh"])
                else:
                    self.assertAlmostEqual(
                        s[nome]["be_incentivo_eur_kwh"],
                        bei, places=2)
                if beq is None:
                    self.assertIsNone(
                        s[nome]["be_quota_frazione"])
                else:
                    self.assertAlmostEqual(
                        s[nome]["be_quota_frazione"],
                        beq, places=2)
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
        bc = mh909_calcola(**_demo_kwargs(potenza_kwp=0.0))
        self.assertEqual(bc["e_prod_kwh"], 0.0)
        self.assertEqual(bc["e_auto_kwh"], 0.0)
        self.assertEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertEqual(bc["e_immessa_kwh"], 0.0)
        self.assertEqual(bc["e_cond_kwh"], 0.0)
        self.assertEqual(bc["ricavo_eur_anno"], 0.0)
        self.assertEqual(bc["costi_eur_anno"], 3000.0)
        self.assertEqual(bc["margine_eur_anno"], -3000.0)
        self.assertAlmostEqual(bc["van_eur"], -317386.63,
                               places=2)
        self.assertIsNone(bc["tir_frazione"])
        self.assertIsNone(bc["payback_anni"])
        self.assertIsNone(bc["payback_fraz_anni"])
        self.assertIsNone(bc["be_incentivo_eur_kwh"])
        self.assertIsNone(bc["be_incentivo_eur_mwh"])
        self.assertIsNone(bc["be_quota_frazione"])
        self.assertEqual(bc["co2_t_anno"], 0.0)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_incentivo_zero_non_conviente(self):
        bc = mh909_calcola(
            **_demo_kwargs(incentivo_eur_kwh=0.0))
        self.assertEqual(bc["ricavo_incentivo_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["ricavo_eur_anno"], 16704.0,
                               places=2)
        self.assertEqual(bc["margine_eur_anno"], 8704.0)
        self.assertAlmostEqual(bc["van_eur"], -171528.92,
                               places=2)
        self.assertAlmostEqual(bc["tir_frazione"], -0.0415,
                               places=4)
        self.assertIsNone(bc["payback_anni"])
        self.assertIsNone(bc["payback_fraz_anni"])
        self.assertAlmostEqual(bc["be_incentivo_eur_kwh"],
                               0.1195, places=4)
        self.assertEqual(bc["be_quota_frazione"], 0.0)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_quota_zero_non_conviente(self):
        bc = mh909_calcola(**_demo_kwargs(quota_condivisa=0.0))
        self.assertEqual(bc["e_cond_kwh"], 0.0)
        self.assertEqual(bc["ricavo_incentivo_eur_anno"], 0.0)
        self.assertEqual(bc["e_resto_kwh"], 192000.0)
        self.assertEqual(bc["ricavo_ritiro_eur_anno"], 15360.0)
        self.assertAlmostEqual(bc["ricavo_eur_anno"], 25920.0,
                               places=2)
        self.assertEqual(bc["margine_eur_anno"], 17920.0)
        self.assertAlmostEqual(bc["van_eur"], -56677.19,
                               places=2)
        self.assertAlmostEqual(bc["tir_frazione"], 0.0248,
                               places=4)
        self.assertEqual(bc["payback_anni"], 16)
        self.assertAlmostEqual(bc["payback_fraz_anni"], 15.625,
                               places=2)
        self.assertIsNone(bc["be_incentivo_eur_kwh"])
        self.assertIsNone(bc["be_incentivo_eur_mwh"])
        self.assertAlmostEqual(bc["be_quota_frazione"],
                               0.7896, places=4)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_quota_uno_conviente(self):
        bc = mh909_calcola(**_demo_kwargs(quota_condivisa=1.0))
        self.assertEqual(bc["e_cond_kwh"], 192000.0)
        self.assertEqual(bc["ricavo_incentivo_eur_anno"],
                         21120.0)
        self.assertEqual(bc["e_resto_kwh"], 0.0)
        self.assertEqual(bc["ricavo_ritiro_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["ricavo_eur_anno"], 31680.0,
                               places=2)
        self.assertEqual(bc["margine_eur_anno"], 23680.0)
        self.assertAlmostEqual(bc["van_eur"], 15105.14,
                               places=2)
        self.assertAlmostEqual(bc["tir_frazione"], 0.0563,
                               places=4)
        self.assertEqual(bc["payback_anni"], 12)
        self.assertAlmostEqual(bc["be_incentivo_eur_kwh"],
                               0.1037, places=4)
        self.assertAlmostEqual(bc["be_incentivo_eur_mwh"],
                               103.69, places=2)
        self.assertAlmostEqual(bc["be_quota_frazione"],
                               0.7896, places=4)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_capex_zero_conviente_payback_zero(self):
        bc = mh909_calcola(**_demo_kwargs(capex_eur=0.0))
        self.assertEqual(bc["margine_eur_anno"], 21376.0)
        self.assertAlmostEqual(bc["van_eur"], 266392.21,
                               places=2)
        self.assertIsNone(bc["tir_frazione"])
        self.assertEqual(bc["payback_anni"], 0)
        self.assertEqual(bc["payback_fraz_anni"], 0.0)
        self.assertEqual(bc["be_incentivo_eur_kwh"], 0.0)
        self.assertEqual(bc["be_incentivo_eur_mwh"], 0.0)
        self.assertEqual(bc["be_quota_frazione"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_vita_zero_non_conviente(self):
        bc = mh909_calcola(**_demo_kwargs(vita_anni=0))
        self.assertEqual(bc["margine_eur_anno"], 21376.0)
        self.assertAlmostEqual(bc["van_eur"], -280000.0,
                               places=2)
        self.assertIsNone(bc["tir_frazione"])
        self.assertIsNone(bc["payback_anni"])
        self.assertIsNone(bc["payback_fraz_anni"])
        self.assertIsNone(bc["be_incentivo_eur_kwh"])
        self.assertIsNone(bc["be_incentivo_eur_mwh"])
        self.assertIsNone(bc["be_quota_frazione"])
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertEqual(len(bc["df_flussi"]), 1)

    def test_tasso_zero_conviente(self):
        bc = mh909_calcola(**_demo_kwargs(tasso_frazione=0.0))
        self.assertAlmostEqual(bc["van_eur"], 147520.0,
                               places=2)
        self.assertAlmostEqual(bc["tir_frazione"], 0.0442,
                               places=4)
        self.assertEqual(bc["payback_anni"], 14)
        self.assertAlmostEqual(bc["payback_fraz_anni"], 13.10,
                               places=2)
        self.assertAlmostEqual(bc["be_incentivo_eur_kwh"],
                               0.0460, places=4)
        self.assertAlmostEqual(bc["be_incentivo_eur_mwh"],
                               45.97, places=2)
        self.assertEqual(bc["be_quota_frazione"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_produzione_zero_non_calcolabile(self):
        bc = mh909_calcola(
            **_demo_kwargs(produzione_specifica=0.0))
        self.assertEqual(bc["e_prod_kwh"], 0.0)
        self.assertEqual(bc["ricavo_eur_anno"], 0.0)
        self.assertEqual(bc["costi_eur_anno"], 8000.0)
        self.assertEqual(bc["margine_eur_anno"], -8000.0)
        self.assertAlmostEqual(bc["van_eur"], -379697.68,
                               places=2)
        self.assertIsNone(bc["tir_frazione"])
        self.assertIsNone(bc["payback_anni"])
        self.assertIsNone(bc["payback_fraz_anni"])
        self.assertIsNone(bc["be_incentivo_eur_kwh"])
        self.assertIsNone(bc["be_quota_frazione"])
        self.assertEqual(bc["co2_t_anno"], 0.0)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_prezzo_evitato_zero_non_conviente(self):
        bc = mh909_calcola(
            **_demo_kwargs(prezzo_energia_evitato=0.0))
        self.assertEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["ricavo_eur_anno"], 18816.0,
                               places=2)
        self.assertEqual(bc["margine_eur_anno"], 10816.0)
        self.assertAlmostEqual(bc["van_eur"], -145208.73,
                               places=2)
        self.assertAlmostEqual(bc["tir_frazione"], -0.0234,
                               places=4)
        self.assertIsNone(bc["payback_anni"])
        self.assertIsNone(bc["payback_fraz_anni"])
        self.assertAlmostEqual(bc["be_incentivo_eur_kwh"],
                               0.2111, places=4)
        self.assertIsNone(bc["be_quota_frazione"])
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_prezzo_ritiro_zero_non_conviente(self):
        bc = mh909_calcola(
            **_demo_kwargs(prezzo_ritiro_eur_kwh=0.0))
        self.assertEqual(bc["ricavo_ritiro_eur_anno"], 0.0)
        self.assertAlmostEqual(bc["ricavo_eur_anno"], 23232.0,
                               places=2)
        self.assertEqual(bc["margine_eur_anno"], 15232.0)
        self.assertAlmostEqual(bc["van_eur"], -90175.61,
                               places=2)
        self.assertAlmostEqual(bc["tir_frazione"], 0.0082,
                               places=4)
        self.assertEqual(bc["payback_anni"], 19)
        self.assertAlmostEqual(bc["payback_fraz_anni"], 18.38,
                               places=2)
        self.assertAlmostEqual(bc["be_incentivo_eur_kwh"],
                               0.1728, places=4)
        self.assertAlmostEqual(bc["be_quota_frazione"],
                               0.9426, places=4)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_om_zero_e_gestione_zero_e_vita_30(self):
        bc = mh909_calcola(**_demo_kwargs(om_eur_kwp_anno=0.0))
        self.assertEqual(bc["costi_eur_anno"], 3000.0)
        self.assertEqual(bc["margine_eur_anno"], 26376.0)
        self.assertAlmostEqual(bc["van_eur"], 48703.26,
                               places=2)
        self.assertAlmostEqual(bc["be_incentivo_eur_kwh"],
                               0.0761, places=4)
        self.assertEqual(bc["be_quota_frazione"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh909_calcola(
            **_demo_kwargs(gestione_cer_eur_anno=0.0))
        self.assertEqual(bc["costi_eur_anno"], 5000.0)
        self.assertEqual(bc["margine_eur_anno"], 24376.0)
        self.assertAlmostEqual(bc["van_eur"], 23778.84,
                               places=2)
        self.assertAlmostEqual(bc["be_quota_frazione"],
                               0.2687, places=4)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh909_calcola(**_demo_kwargs(vita_anni=30))
        self.assertAlmostEqual(bc["van_eur"], 48601.51,
                               places=2)
        self.assertAlmostEqual(bc["be_quota_frazione"],
                               0.0511, places=4)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_quota_autoconsumo_zero_e_uno(self):
        bc = mh909_calcola(
            **_demo_kwargs(quota_autoconsumo=0.0))
        self.assertEqual(bc["e_auto_kwh"], 0.0)
        self.assertEqual(bc["risparmio_eur_anno"], 0.0)
        self.assertEqual(bc["e_immessa_kwh"], 240000.0)
        self.assertAlmostEqual(bc["van_eur"], -86586.50,
                               places=2)
        self.assertIsNone(bc["be_quota_frazione"])
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        bc = mh909_calcola(
            **_demo_kwargs(quota_autoconsumo=1.0))
        self.assertEqual(bc["e_auto_kwh"], 240000.0)
        self.assertEqual(bc["e_immessa_kwh"], 0.0)
        self.assertEqual(bc["e_cond_kwh"], 0.0)
        self.assertAlmostEqual(bc["van_eur"], 278307.02,
                               places=2)
        self.assertIsNone(bc["be_incentivo_eur_kwh"])
        self.assertIsNone(bc["be_quota_frazione"])
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_tolleranza_zero_demo_diventa_non_conviente(self):
        # Con VAN negativo e tolleranza zero il
        # demo MARGINALE diventa NON_CONVIENTE:
        # la tolleranza decide il verdetto, non
        # il VAN.
        bc = mh909_calcola(**_demo_kwargs(tol_frazione=0.0))
        self.assertAlmostEqual(bc["van_eur"], -13607.79,
                               places=2)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_van_invarianze(self):
        # Il VAN non dipende dalla tolleranza.
        bc = demo_calcoli()
        bc_t = mh909_calcola(**_demo_kwargs(tol_frazione=0.0))
        self.assertEqual(bc_t["van_eur"], bc["van_eur"])
        # Il VAN non dipende dalla CO2: la CO2
        # non entra nell'economia.
        self.assertEqual(bc["co2_t_anno"], 60.0)
        bc_p = mh909_calcola(
            **_demo_kwargs(produzione_specifica=1500.0))
        self.assertEqual(bc_p["co2_t_anno"], 75.0)
        self.assertNotEqual(bc_p["van_eur"], bc["van_eur"])

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh909_csv(bc, mh909_demo())
        for voce in ("potenza_kwp",
                     "produzione_specifica",
                     "quota_autoconsumo",
                     "prezzo_energia_evitato",
                     "quota_condivisa",
                     "incentivo_eur_kwh",
                     "prezzo_ritiro_eur_kwh",
                     "capex_eur",
                     "om_eur_kwp_anno",
                     "gestione_cer_eur_anno",
                     "vita_anni",
                     "tasso_frazione",
                     "tol_frazione",
                     "e_prod_kwh",
                     "e_auto_kwh",
                     "risparmio_eur_anno",
                     "e_immessa_kwh",
                     "e_cond_kwh",
                     "ricavo_incentivo_eur_anno",
                     "e_resto_kwh",
                     "ricavo_ritiro_eur_anno",
                     "ricavo_eur_anno",
                     "costi_eur_anno",
                     "margine_eur_anno",
                     "van_eur",
                     "tir_frazione",
                     "payback_anni",
                     "payback_fraz_anni",
                     "be_incentivo_eur_kwh",
                     "be_incentivo_eur_mwh",
                     "be_quota_frazione",
                     "co2_t_anno",
                     "scenario_base_e_prod_kwh",
                     "scenario_base_van_eur",
                     "scenario_base_verdetto",
                     "scenario_inc013_van_eur",
                     "scenario_inc013_verdetto",
                     "scenario_inc008_van_eur",
                     "scenario_inc008_verdetto",
                     "scenario_qc080_van_eur",
                     "scenario_qc080_verdetto",
                     "scenario_tasso8_van_eur",
                     "scenario_tasso8_verdetto",
                     "scenario_capex200k_van_eur",
                     "scenario_capex200k_verdetto",
                     "confronto_e_prod_kwh",
                     "confronto_e_auto_kwh",
                     "confronto_risparmio_eur_anno",
                     "confronto_e_immessa_kwh",
                     "confronto_e_cond_kwh",
                     "confronto_ricavo_incentivo_eur_anno",
                     "confronto_e_resto_kwh",
                     "confronto_ricavo_ritiro_eur_anno",
                     "confronto_ricavo_eur_anno",
                     "confronto_costi_eur_anno",
                     "confronto_margine_eur_anno",
                     "confronto_van_eur",
                     "confronto_tir_frazione",
                     "confronto_payback_anni",
                     "confronto_be_incentivo_eur_kwh",
                     "confronto_be_incentivo_eur_mwh",
                     "confronto_be_quota_frazione",
                     "confronto_co2_t_anno",
                     "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("MARGINALE", csv)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh909_csv(bc, mh909_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("potenza_kwp;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh909_demo_calcoli()["van_eur"],
                         demo_calcoli()["van_eur"])
        self.assertEqual(mh909_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_df_scenari_confronto_tabella_flussi(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_scenari"]), 6)
        self.assertEqual(len(bc["df_confronto"]), 20)
        self.assertEqual(len(bc["df_tabella"]), 33)
        self.assertEqual(len(bc["df_flussi"]), 21)
        self.assertEqual(len(bc["df_ricavo_costi"]), 7)
        self.assertEqual(
            list(bc["df_confronto"]["Voce"]),
            ["E prod (kWh/anno)",
             "E auto (kWh/anno)",
             "Risparmio bolletta (EUR/anno)",
             "E immessa (kWh/anno)",
             "E condivisa (kWh/anno)",
             "Ricavo incentivo (EUR/anno)",
             "E resto (kWh/anno)",
             "Ricavo ritiro (EUR/anno)",
             "Ricavo (EUR/anno)",
             "Costi (EUR/anno)",
             "Margine annuo (EUR/anno)",
             "VAN (EUR)",
             "TIR (frazione)",
             "Payback (anni)",
             "Payback frazionale (anni)",
             "Breakeven incentivo (EUR/kWh)",
             "Breakeven incentivo (EUR/MWh)",
             "Breakeven quota",
             "CO2 evitata (t/anno)",
             "Verdetto"])
        self.assertAlmostEqual(
            bc["df_confronto"]["Valore"].iloc[0],
            240000.00, places=2)
        self.assertAlmostEqual(
            bc["df_confronto"]["Valore"].iloc[11],
            -13607.79, places=2)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Potenza (kWp)", voci)
        self.assertIn("Produzione specifica (kWh/kWp/anno)", voci)
        self.assertIn("Quota condivisa", voci)
        self.assertIn("Incentivo (EUR/kWh)", voci)
        self.assertIn("E prod (kWh/anno)", voci)
        self.assertIn("E condivisa (kWh/anno)", voci)
        self.assertIn("Ricavo incentivo (EUR/anno)", voci)
        self.assertIn("Breakeven incentivo (EUR/kWh)", voci)
        self.assertIn("Breakeven incentivo (EUR/MWh)", voci)
        self.assertIn("Breakeven quota", voci)
        self.assertIn("VAN (EUR)", voci)
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
            -13607.79, places=2)
        self.assertAlmostEqual(
            bc["df_scenari"]["TIR (%)"].iloc[0],
            4.42, places=2)
        self.assertEqual(
            list(bc["df_flussi"].columns),
            ["Anno", "Flusso (EUR)", "Cumulato (EUR)"])
        self.assertEqual(
            list(bc["df_ricavo_costi"].columns),
            ["Voce", "Valore"])

    def test_valida_rifiuta_stringhe_e_bool(self):
        kw = _demo_kwargs(potenza_kwp="200.0")
        self.assertRaises(ValueError, mh909_calcola, **kw)
        kw = _demo_kwargs(potenza_kwp=True)
        self.assertRaises(ValueError, mh909_calcola, **kw)
        val = mh909_valida(*[kw[k] for k in _ORDINE_VALIDA])
        self.assertFalse(val["valido"])

class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def909\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh909_demo().keys()), lette - set(mh909_demo().keys()))
        self.assertEqual(lette, set(mh909_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc909\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc909\["([^"]+)"\]', src))
        attese = set(mh909_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestConteggioTitoliPreApply(unittest.TestCase):
    def test_conteggio_titoli_pre_apply(self):
        # Conteggio titoli: forma PRE-apply. Prima
        # dell'apply di questa scheda la copia di
        # lavoro del repo ha 908 blocchi scheda;
        # l'apply bumpa questo assert al conteggio
        # post apply 909.
        if os.path.exists(_APP_WD):
            src = open(_APP_WD, encoding="utf-8", errors="ignore").read()
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 909)
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
        nuova = (", " + ", ".join("tab%d" % n for n in range(906, 910))
                + " = st.tabs([")
        self.assertIn(nuova, src)
        vecchia = (", " + ", ".join("tab%d" % n for n in range(906, 909))
                + " = st.tabs([")
        self.assertNotIn(vecchia, src)


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with " + _NUOVO_TAB + ":"), 1)
        self.assertTrue(src.startswith("    # W914"))

    def test_ui_scheda_nuova_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with " + _NUOVO_TAB + ":"), 1)
        self.assertIn("def mh909_demo(", src_h)
        self.assertIn("def mh909_calcola(", src_h)
        self.assertIn(_NUOVO_TAB, src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("Comunità Energetica Rinnovabile (CER): l'energia condivisa paga?", src)
        self.assertIn("🤝☀️ Comunità Energetica Rinnovabile (CER): l'energia condivisa paga?", src)
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
        self.assertEqual(len(chiavi), 20)
        self.assertIn('key="' + _NUOVO_ST + 'calcola"', src)
        self.assertIn('key="' + _NUOVO_ST + 'csv"', src)
        self.assertIn('key="' + _NUOVO_ST + 'csv_scenari"', src)
        self.assertIn('key="' + _NUOVO_ST + 'quota_condivisa"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg909"), src.index(".paiac("))
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
