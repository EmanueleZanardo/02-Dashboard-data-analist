"""Test nuova scheda UVAM: aggregare
flessibilita e venderla a Terna paga?
Repo path: tests/test_w912_uvam.py

Effetto ECONOMICO: un aggregatore o
BSP costruisce un portafoglio UVAM
(carichi flessibili piu accumulo piu
generazione distribuita) e offre
disponibilita sul Mercato dei
Servizi di Dispacciamento di Terna.
Il ricavo ha due gambe: il ricavo
di disponibilita (potenza offerta
per prezzo disponibilita per
disponibilita, pagato anche se non
si viene mai attivati) e il ricavo
di energia attivata pay as bid
(energia attivata per prezzo
energia). La potenza attivata
effettiva e il minimo tra potenza
attivata e potenza offerta. La quota
di fallimento e la frazione di
energia attivata che non viene
erogata (baseline contro misura):
l'energia mancata paga la penalita
per MWh mancato. I costi sono la
piattaforma piu i costi dei siti
(costo fisso per sito piu compenso
per MWh attivato). Il margine netto
annuo e ricavo disponibilita piu
ricavo energia meno penalita meno
costo anno: se e positivo, il
portafoglio genera cassa ogni anno;
se e zero o negativo, il
portafoglio non si ripaga mai e il
verdetto e NON_CALCOLABILE. Il VAN
e meno CAPEX piu margine per
l'annualita a tasso dato sulla
durata; la TIR e il tasso che
azzera il VAN (bisezione); il
payback e il primo anno in cui il
cumulato del margine raggiunge il
CAPEX. Il breakeven prezzo
disponibilita e (costo anno piu
penalita meno ricavo energia)
diviso (potenza offerta per
disponibilita): e il prezzo
disponibilita che azzera il
margine, NON il prezzo che azzera
il VAN (a margine zero il VAN resta
meno CAPEX). Il breakeven prezzo
energia e (costo anno piu penalita
meno ricavo disponibilita) diviso
energia attivata: e il prezzo
energia che azzera il margine. La
CO2 evitata e energia attivata per
fattore CO2 in t/anno: 0,35 t/MWh
per MWh danno t, senza divisioni
per 1000.
Demo: potenza offerta 5 MW, prezzo
disponibilita 30.000 EUR/MW/anno,
disponibilita 0,95, attivazioni
40/anno, durata attivazione 2 h,
potenza attivata 4 MW, prezzo
energia 180 EUR/MWh, quota
fallimento 0,05, penalita 250
EUR/MWh, costo piattaforma 60.000
EUR/anno, siti 25, costo sito 800
EUR/anno, compenso siti 40
EUR/MWh, CAPEX 150.000 EUR, tasso
0,05, durata 5 anni, tolleranza
0,10, fattore CO2 0,35 t/MWh.
Potenza attivata effettiva = minimo
tra 4 e 5 = 4 MW. Ricavo
disponibilita = 5 per 30.000 per
0,95 = 142.500 EUR. Energia
attivata = 40 per 2 per 4 = 320
MWh. Ricavo energia = 320 per 180
= 57.600 EUR. Energia mancata =
320 per 0,05 = 16 MWh. Penalita =
16 per 250 = 4.000 EUR. Costo siti
= 25 per 800 piu 320 per 40 =
32.800 EUR. Costo anno = 60.000
piu 32.800 = 92.800 EUR. Margine
netto annuo = 142.500 piu 57.600
meno 4.000 meno 92.800 = 103.300
EUR. Annualita 5 anni al 5 per
cento = 4,3294766706. VAN = meno
150.000 piu 103.300 per
4,3294766706 = 297.234,94 EUR
(CORREZIONE: il brief attendeva
297.235,14, il ricalcolo
indipendente da 297.234,94). TIR =
62,85 per cento. Payback = 2 anni
(cumulato anno 1 = 103.300 sotto
CAPEX, anno 2 = 206.600 sopra
CAPEX; frazionale 1,45 anni).
Breakeven prezzo disponibilita =
(92.800 piu 4.000 meno 57.600)
diviso (5 per 0,95) = 8.252,63
EUR/MW/anno. Breakeven prezzo
energia = None (la sola
disponibilita copre gia i costi).
CO2 evitata = 320 per 0,35 = 112
t/anno. Verdetto CONVIENTE.
Scenari: base potenza offerta 5,
energia attivata 320, ricavo
disponibilita 142.500, ricavo
energia 57.600, margine 103.300,
VAN 297.234,94, TIR 62,85 per
cento, payback 2 anni, breakeven
prezzo disponibilita 8.252,63,
breakeven prezzo energia None,
CONVIENTE; disponibilita piu 30
per cento (prezzo disponibilita
39.000) ricavo disponibilita
185.250, margine 146.050, VAN
482.320,07, TIR 93,81 per cento,
payback 2 anni, breakeven prezzo
disponibilita 8.252,63, CONVIENTE;
disponibilita meno 30 per cento
(prezzo disponibilita 21.000)
ricavo disponibilita 99.750,
margine 60.550, VAN 112.149,81,
TIR 29,12 per cento, payback 3
anni, breakeven prezzo
disponibilita 8.252,63, CONVIENTE;
attivazioni meno 50 per cento (20
attivazioni) energia attivata 160,
ricavo energia 28.800, margine
82.900, VAN 208.913,62, TIR 47,30
per cento, payback 2 anni,
breakeven prezzo disponibilita
12.547,37, CO2 56 t/anno,
CONVIENTE; disponibilita 0,80
ricavo disponibilita 120.000,
margine 80.800, VAN 199.821,71,
TIR 45,65 per cento, payback 2
anni, breakeven prezzo
disponibilita 9.800, CONVIENTE;
durata 3 anni energia attivata
320, margine 103.300, VAN
131.311,52, TIR 47,33 per cento,
payback 2 anni, breakeven prezzo
disponibilita 8.252,63, CONVIENTE.
Confronto: potenza attivata
effettiva 4 contro energia
attivata 320, ricavo disponibilita
142.500 contro ricavo energia
57.600, energia mancata 16 contro
penalita 4.000, costo siti 32.800
contro costo anno 92.800, margine
103.300 contro VAN 297.234,94, TIR
62,85 per cento contro payback 2
anni, breakeven prezzo
disponibilita 8.252,63 contro
breakeven prezzo energia None, CO2
112 t/anno.
Tolleranza in FRAZIONE (0,10 = 10 %
del CAPEX), usata diretta, NON
divisa per 100. Prezzo
disponibilita, prezzo energia,
attivazioni e quota di fallimento
medi annui costanti,
SEMPLIFICAZIONE DICHIARATA (il
prezzo disponibilita si forma in
asta MSD, le attivazioni dipendono
dalle esigenze di Terna, la quota
di fallimento dipende dalla
baseline e dai siti, qui valori
medi costanti); i flussi sono solo
sugli anni di durata,
SEMPLIFICAZIONE DICHIARATA. La CO2
evitata e energia attivata per
fattore CO2, SEMPLIFICAZIONE
DICHIARATA (l'energia attivata
evita l'accensione di picco a gas).
Verdetto principale: CONVIENTE.
Verdetto: NON_CALCOLABILE se il
margine netto annuo e zero o
negativo oppure se un input e
degenere (potenza offerta negativa,
prezzo disponibilita negativo,
disponibilita negativa o sopra 1,
attivazioni negative o non intere,
durata attivazione negativa,
potenza attivata negativa, prezzo
energia negativo, quota fallimento
negativa o sopra 1, penalita
negativa, costo piattaforma
negativo, siti negativi o non
interi, costo sito negativo,
compenso siti negativo, CAPEX
negativo, tasso negativo o sopra 1,
durata negativa o non intera,
tolleranza negativa o sopra 1,
fattore CO2 negativo); altrimenti
CONVIENTE se il VAN e maggiore di
0, MARGINALE se il VAN e minore o
uguale a 0 e il suo valore assoluto
e minore o uguale a tolleranza per
CAPEX, NON_CONVIENTE altrimenti.
La potenza attivata sopra la
potenza offerta NON e degenere: si
usa il minimo. La durata zero NON
e degenere: da VAN meno CAPEX, TIR
None, payback None e verdetto
NON_CONVIENTE. Il CAPEX zero NON
e degenere: da VAN positivo, TIR
None, payback 0 e verdetto
CONVIENTE. La potenza offerta zero
NON e degenere: da ricavi zero,
margine meno costo anno e verdetto
NON_CALCOLABILE, con breakeven
prezzo disponibilita None e
breakeven prezzo energia None. Il
prezzo energia zero NON e degenere:
da ricavo energia zero, margine
positivo e verdetto CONVIENTE.
Casi limite: potenza offerta zero
(ricavi 0, margine meno 80.000,
VAN meno 496.358,13,
NON_CALCOLABILE); prezzo
disponibilita zero (ricavo
disponibilita 0, margine meno
39.200, VAN meno 319.715,49,
NON_CALCOLABILE); prezzo energia
zero (ricavo energia 0, margine
45.700, VAN 47.857,08, CONVIENTE);
fallimento 1,0 (penalita 80.000,
margine 27.300, VAN meno
31.805,29, NON_CONVIENTE); durata
zero (VAN meno 150.000, TIR None,
payback None, NON_CONVIENTE);
CAPEX zero (VAN 447.234,94, TIR
None, payback 0, CONVIENTE);
disponibilita zero (ricavo
disponibilita 0, margine meno
39.200, VAN meno 319.715,49,
NON_CALCOLABILE); attivazioni zero
(energia attivata 0, margine
62.500, VAN 120.592,29,
CONVIENTE); compenso siti zero
(margine 116.100, VAN 352.652,24,
CONVIENTE); penalita zero
(margine 107.300, VAN 314.552,85,
CONVIENTE).
Distinzione esplicita: qui SOLO il
conto economico UVAM sul MSD di
Terna (portafoglio aggregato di
flessibilita offerto in MSD con
disponibilita piu energia attivata
pay as bid piu penalita su energia
mancata misurata contro baseline),
NIENTE VPP come concetto (la VPP e
l'aggregazione tecnica delle
risorse, l'UVAM e il meccanismo di
mercato italiano che la remunera
sul MSD), NIENTE FCR aFRR mFRR RR
come singoli servizi (sono
prodotti di bilanciamento con
regole proprie, qui il ricavo e
quello UVAM sul MSD), NIENTE
demand response come concetto
generico (la tab669 copre la
demand response del singolo sito
flessibile con fee dell'aggregatore
in percentuale sui ricavi e
penalita attesa per evento: qui il
portafoglio dell'aggregatore con
costo piattaforma, costo per sito
e compenso per MWh, potenza
offerta contro potenza attivata
con minimo, quota di fallimento su
energia mancata e due breakeven).
"""

import ast
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from w912_helpers import (
        demo_calcoli,
        mh907_annuity,
        mh907_be_prezzo_disp,
        mh907_be_prezzo_energia,
        mh907_calcola,
        mh907_co2,
        mh907_confronto,
        mh907_costo_anno,
        mh907_costo_siti,
        mh907_csv,
        mh907_demo,
        mh907_demo_calcoli,
        mh907_durata,
        mh907_e_attivata,
        mh907_e_mancata,
        mh907_fraz,
        mh907_intero,
        mh907_margine,
        mh907_nneg,
        mh907_num,
        mh907_p_attivata_eff,
        mh907_payback,
        mh907_payback_fraz,
        mh907_penalita,
        mh907_pos,
        mh907_ricavo_disp,
        mh907_ricavo_energia,
        mh907_scenario,
        mh907_sensibilita,
        mh907_tir,
        mh907_valida,
        mh907_van,
        mh907_verdetto,
    )
except ModuleNotFoundError:
    import importlib.util as _ilu
    _hf = os.path.expanduser(
        "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
        "/hidden_files")
    _spec = _ilu.spec_from_file_location(
        "w912_helpers", os.path.join(_hf, "w912_helpers.py"))
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    demo_calcoli = _mod.demo_calcoli
    mh907_annuity = _mod.mh907_annuity
    mh907_be_prezzo_disp = _mod.mh907_be_prezzo_disp
    mh907_be_prezzo_energia = _mod.mh907_be_prezzo_energia
    mh907_calcola = _mod.mh907_calcola
    mh907_co2 = _mod.mh907_co2
    mh907_confronto = _mod.mh907_confronto
    mh907_costo_anno = _mod.mh907_costo_anno
    mh907_costo_siti = _mod.mh907_costo_siti
    mh907_csv = _mod.mh907_csv
    mh907_demo = _mod.mh907_demo
    mh907_demo_calcoli = _mod.mh907_demo_calcoli
    mh907_durata = _mod.mh907_durata
    mh907_e_attivata = _mod.mh907_e_attivata
    mh907_e_mancata = _mod.mh907_e_mancata
    mh907_fraz = _mod.mh907_fraz
    mh907_intero = _mod.mh907_intero
    mh907_margine = _mod.mh907_margine
    mh907_nneg = _mod.mh907_nneg
    mh907_num = _mod.mh907_num
    mh907_p_attivata_eff = _mod.mh907_p_attivata_eff
    mh907_payback = _mod.mh907_payback
    mh907_payback_fraz = _mod.mh907_payback_fraz
    mh907_penalita = _mod.mh907_penalita
    mh907_pos = _mod.mh907_pos
    mh907_ricavo_disp = _mod.mh907_ricavo_disp
    mh907_ricavo_energia = _mod.mh907_ricavo_energia
    mh907_scenario = _mod.mh907_scenario
    mh907_sensibilita = _mod.mh907_sensibilita
    mh907_tir = _mod.mh907_tir
    mh907_valida = _mod.mh907_valida
    mh907_van = _mod.mh907_van
    mh907_verdetto = _mod.mh907_verdetto

_HERE = os.path.dirname(os.path.abspath(__file__))
_HF_FALLBACK = os.path.expanduser(
    "~/workspace/goals/energy-analyst-dashboard-qa-bugfix-and-new-features"
    "/hidden_files")


def _risolvi(nome):
    p = os.path.join(_HERE, nome)
    if not os.path.exists(p):
        p = os.path.join(_HF_FALLBACK, nome)
    return p


_HELPERS_PATH = _risolvi("w912_helpers.py")
_UI_PATH = _risolvi("w912_ui.py")

# Identificatori della scheda precedente, costruiti
# dinamicamente cosi' che nessun letterale della
# scheda precedente compaia in questo file: i test
# di struttura li usano solo come assertNotIn.
_VECCHIO_MH = "mh90" + "6"
_VECCHIO_TAB = "tab90" + "6"
_VECCHIO_ST = "st90" + "6_"
_VECCHIO_SIGLA = "certificati" + "bianchi"
_IMP_STREAMLIT = "import " + "streamlit"

# Copia di lavoro del repo usata per il conteggio
# titoli (vedi test conteggio).
_APP_WD = os.path.expanduser(
    "~/workspace/repo-dashboard/Dashboard-data-analist/app.py")

_DEMO_SCALARI = {
    "p_attivata_eff_mw": 4.0,
    "e_attivata_mwh": 320.0,
    "ricavo_disp_eur_anno": 142500.0,
    "ricavo_energia_eur_anno": 57600.0,
    "e_mancata_mwh": 16.0,
    "penalita_eur": 4000.0,
    "costo_siti_eur_anno": 32800.0,
    "costo_anno_eur": 92800.0,
    "margine_eur_anno": 103300.0,
    "van_eur": 297234.94007616397,
    "tir_frazione": 0.6285485254602656,
    "payback_anni": 2,
    "payback_fraz_anni": 1.452081316553727,
    "be_prezzo_disp_eur_mw_anno": 8252.631578947368,
    "be_prezzo_energia_eur_mwh": None,
    "co2_t_anno": 112.0,
    "verdetto": "CONVIENTE",
}

_DEMO_INPUT = {
    "p_offerta_mw": 5.0,
    "prezzo_disp_eur_mw_anno": 30000.0,
    "disponibilita_frazione": 0.95,
    "n_attivazioni_anno": 40,
    "durata_attivazione_h": 2.0,
    "p_attivata_mw": 4.0,
    "prezzo_energia_eur_mwh": 180.0,
    "quota_fallimento_frazione": 0.05,
    "penalita_eur_mwh": 250.0,
    "costo_piattaforma_eur_anno": 60000.0,
    "n_siti": 25,
    "costo_sito_eur_anno": 800.0,
    "compenso_siti_eur_mwh": 40.0,
    "capex_eur": 150000.0,
    "tasso_frazione": 0.05,
    "durata_anni": 5,
    "tol_frazione": 0.10,
    "fattore_co2_t_mwh": 0.35,
}

_DEMO_SCENARI = [
    {"nome": "Base",
     "p_offerta_mw": 5.0, "prezzo_disp_eur_mw_anno": 30000.0,
     "disponibilita_frazione": 0.95, "n_attivazioni_anno": 40,
     "durata_attivazione_h": 2.0, "p_attivata_mw": 4.0,
     "prezzo_energia_eur_mwh": 180.0,
     "quota_fallimento_frazione": 0.05,
     "penalita_eur_mwh": 250.0,
     "costo_piattaforma_eur_anno": 60000.0, "n_siti": 25,
     "costo_sito_eur_anno": 800.0,
     "compenso_siti_eur_mwh": 40.0, "capex_eur": 150000.0,
     "tasso_frazione": 0.05, "durata_anni": 5,
     "tol_frazione": 0.10, "fattore_co2_t_mwh": 0.35,
     "p_attivata_eff_mw": 4.0, "e_attivata_mwh": 320.0,
     "ricavo_disp_eur_anno": 142500.0,
     "ricavo_energia_eur_anno": 57600.0, "e_mancata_mwh": 16.0,
     "penalita_eur": 4000.0, "costo_siti_eur_anno": 32800.0,
     "costo_anno_eur": 92800.0, "margine_eur_anno": 103300.0,
     "van_eur": 297234.94007616397,
     "tir_frazione": 0.6285485254602656,
     "payback_anni": 2,
     "payback_fraz_anni": 1.452081316553727,
     "be_prezzo_disp_eur_mw_anno": 8252.631578947368,
     "be_prezzo_energia_eur_mwh": None,
     "co2_t_anno": 112.0, "verdetto": "CONVIENTE"},
    {"nome": "Disponibilita piu 30 %",
     "p_offerta_mw": 5.0, "prezzo_disp_eur_mw_anno": 39000.0,
     "disponibilita_frazione": 0.95, "n_attivazioni_anno": 40,
     "durata_attivazione_h": 2.0, "p_attivata_mw": 4.0,
     "prezzo_energia_eur_mwh": 180.0,
     "quota_fallimento_frazione": 0.05,
     "penalita_eur_mwh": 250.0,
     "costo_piattaforma_eur_anno": 60000.0, "n_siti": 25,
     "costo_sito_eur_anno": 800.0,
     "compenso_siti_eur_mwh": 40.0, "capex_eur": 150000.0,
     "tasso_frazione": 0.05, "durata_anni": 5,
     "tol_frazione": 0.10, "fattore_co2_t_mwh": 0.35,
     "p_attivata_eff_mw": 4.0, "e_attivata_mwh": 320.0,
     "ricavo_disp_eur_anno": 185250.0,
     "ricavo_energia_eur_anno": 57600.0, "e_mancata_mwh": 16.0,
     "penalita_eur": 4000.0, "costo_siti_eur_anno": 32800.0,
     "costo_anno_eur": 92800.0, "margine_eur_anno": 146050.0,
     "van_eur": 482320.0677456317,
     "tir_frazione": 0.9380561273969079,
     "payback_anni": 2,
     "payback_fraz_anni": 1.0270455323519343,
     "be_prezzo_disp_eur_mw_anno": 8252.631578947368,
     "be_prezzo_energia_eur_mwh": None,
     "co2_t_anno": 112.0, "verdetto": "CONVIENTE"},
    {"nome": "Disponibilita meno 30 %",
     "p_offerta_mw": 5.0, "prezzo_disp_eur_mw_anno": 21000.0,
     "disponibilita_frazione": 0.95, "n_attivazioni_anno": 40,
     "durata_attivazione_h": 2.0, "p_attivata_mw": 4.0,
     "prezzo_energia_eur_mwh": 180.0,
     "quota_fallimento_frazione": 0.05,
     "penalita_eur_mwh": 250.0,
     "costo_piattaforma_eur_anno": 60000.0, "n_siti": 25,
     "costo_sito_eur_anno": 800.0,
     "compenso_siti_eur_mwh": 40.0, "capex_eur": 150000.0,
     "tasso_frazione": 0.05, "durata_anni": 5,
     "tol_frazione": 0.10, "fattore_co2_t_mwh": 0.35,
     "p_attivata_eff_mw": 4.0, "e_attivata_mwh": 320.0,
     "ricavo_disp_eur_anno": 99750.0,
     "ricavo_energia_eur_anno": 57600.0, "e_mancata_mwh": 16.0,
     "penalita_eur": 4000.0, "costo_siti_eur_anno": 32800.0,
     "costo_anno_eur": 92800.0, "margine_eur_anno": 60550.0,
     "van_eur": 112149.81240669632,
     "tir_frazione": 0.29118555746784813,
     "payback_anni": 3,
     "payback_fraz_anni": 2.477291494632535,
     "be_prezzo_disp_eur_mw_anno": 8252.631578947368,
     "be_prezzo_energia_eur_mwh": None,
     "co2_t_anno": 112.0, "verdetto": "CONVIENTE"},
    {"nome": "Attivazioni meno 50 %",
     "p_offerta_mw": 5.0, "prezzo_disp_eur_mw_anno": 30000.0,
     "disponibilita_frazione": 0.95, "n_attivazioni_anno": 20,
     "durata_attivazione_h": 2.0, "p_attivata_mw": 4.0,
     "prezzo_energia_eur_mwh": 180.0,
     "quota_fallimento_frazione": 0.05,
     "penalita_eur_mwh": 250.0,
     "costo_piattaforma_eur_anno": 60000.0, "n_siti": 25,
     "costo_sito_eur_anno": 800.0,
     "compenso_siti_eur_mwh": 40.0, "capex_eur": 150000.0,
     "tasso_frazione": 0.05, "durata_anni": 5,
     "tol_frazione": 0.10, "fattore_co2_t_mwh": 0.35,
     "p_attivata_eff_mw": 4.0, "e_attivata_mwh": 160.0,
     "ricavo_disp_eur_anno": 142500.0,
     "ricavo_energia_eur_anno": 28800.0, "e_mancata_mwh": 8.0,
     "penalita_eur": 2000.0, "costo_siti_eur_anno": 26400.0,
     "costo_anno_eur": 86400.0, "margine_eur_anno": 82900.0,
     "van_eur": 208913.61599529517,
     "tir_frazione": 0.4729565130811352,
     "payback_anni": 2,
     "payback_fraz_anni": 1.8094089264173703,
     "be_prezzo_disp_eur_mw_anno": 12547.368421052632,
     "be_prezzo_energia_eur_mwh": None,
     "co2_t_anno": 56.0, "verdetto": "CONVIENTE"},
    {"nome": "Disponibilita 0,80",
     "p_offerta_mw": 5.0, "prezzo_disp_eur_mw_anno": 30000.0,
     "disponibilita_frazione": 0.80, "n_attivazioni_anno": 40,
     "durata_attivazione_h": 2.0, "p_attivata_mw": 4.0,
     "prezzo_energia_eur_mwh": 180.0,
     "quota_fallimento_frazione": 0.05,
     "penalita_eur_mwh": 250.0,
     "costo_piattaforma_eur_anno": 60000.0, "n_siti": 25,
     "costo_sito_eur_anno": 800.0,
     "compenso_siti_eur_mwh": 40.0, "capex_eur": 150000.0,
     "tasso_frazione": 0.05, "durata_anni": 5,
     "tol_frazione": 0.10, "fattore_co2_t_mwh": 0.35,
     "p_attivata_eff_mw": 4.0, "e_attivata_mwh": 320.0,
     "ricavo_disp_eur_anno": 120000.0,
     "ricavo_energia_eur_anno": 57600.0, "e_mancata_mwh": 16.0,
     "penalita_eur": 4000.0, "costo_siti_eur_anno": 32800.0,
     "costo_anno_eur": 92800.0, "margine_eur_anno": 80800.0,
     "van_eur": 199821.71498697047,
     "tir_frazione": 0.4564810259655998,
     "payback_anni": 2,
     "payback_fraz_anni": 1.8564356435643565,
     "be_prezzo_disp_eur_mw_anno": 9800.0,
     "be_prezzo_energia_eur_mwh": None,
     "co2_t_anno": 112.0, "verdetto": "CONVIENTE"},
    {"nome": "Durata 3 anni",
     "p_offerta_mw": 5.0, "prezzo_disp_eur_mw_anno": 30000.0,
     "disponibilita_frazione": 0.95, "n_attivazioni_anno": 40,
     "durata_attivazione_h": 2.0, "p_attivata_mw": 4.0,
     "prezzo_energia_eur_mwh": 180.0,
     "quota_fallimento_frazione": 0.05,
     "penalita_eur_mwh": 250.0,
     "costo_piattaforma_eur_anno": 60000.0, "n_siti": 25,
     "costo_sito_eur_anno": 800.0,
     "compenso_siti_eur_mwh": 40.0, "capex_eur": 150000.0,
     "tasso_frazione": 0.05, "durata_anni": 3,
     "tol_frazione": 0.10, "fattore_co2_t_mwh": 0.35,
     "p_attivata_eff_mw": 4.0, "e_attivata_mwh": 320.0,
     "ricavo_disp_eur_anno": 142500.0,
     "ricavo_energia_eur_anno": 57600.0, "e_mancata_mwh": 16.0,
     "penalita_eur": 4000.0, "costo_siti_eur_anno": 32800.0,
     "costo_anno_eur": 92800.0, "margine_eur_anno": 103300.0,
     "van_eur": 131311.52143397054,
     "tir_frazione": 0.47333796416748397,
     "payback_anni": 2,
     "payback_fraz_anni": 1.452081316553727,
     "be_prezzo_disp_eur_mw_anno": 8252.631578947368,
     "be_prezzo_energia_eur_mwh": None,
     "co2_t_anno": 112.0, "verdetto": "CONVIENTE"},
]

_DEMO_CONFRONTO = {
    "p_attivata_eff_mw": 4.0,
    "e_attivata_mwh": 320.0,
    "ricavo_disp_eur_anno": 142500.0,
    "ricavo_energia_eur_anno": 57600.0,
    "e_mancata_mwh": 16.0,
    "penalita_eur": 4000.0,
    "costo_siti_eur_anno": 32800.0,
    "costo_anno_eur": 92800.0,
    "margine_eur_anno": 103300.0,
    "van_eur": 297234.94007616397,
    "tir_frazione": 0.6285485254602656,
    "payback_anni": 2,
    "be_prezzo_disp_eur_mw_anno": 8252.631578947368,
    "be_prezzo_energia_eur_mwh": None,
    "co2_t_anno": 112.0,
    "verdetto": "CONVIENTE",
}

_ORDINE_VALIDA = (
    "p_offerta_mw", "prezzo_disp_eur_mw_anno",
    "disponibilita_frazione", "n_attivazioni_anno",
    "durata_attivazione_h", "p_attivata_mw",
    "prezzo_energia_eur_mwh", "quota_fallimento_frazione",
    "penalita_eur_mwh", "costo_piattaforma_eur_anno",
    "n_siti", "costo_sito_eur_anno",
    "compenso_siti_eur_mwh", "capex_eur", "tasso_frazione",
    "durata_anni", "tol_frazione", "fattore_co2_t_mwh")


def _demo_kwargs(**over):
    kw = dict(mh907_demo())
    kw.update(over)
    return kw


def _rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


class TestValidatori(unittest.TestCase):
    def test_num_accetta_int_float(self):
        self.assertEqual(mh907_num(3, "x"), 3.0)
        self.assertEqual(mh907_num(2.5, "x"), 2.5)

    def test_num_rifiuta_bool_stringa_nan_inf(self):
        for cattivo in (True, "3", float("nan"), float("inf"), None):
            with self.assertRaises(ValueError):
                mh907_num(cattivo, "x")

    def test_nneg_zero_ok_negativo_no(self):
        self.assertEqual(mh907_nneg(0, "x"), 0.0)
        with self.assertRaises(ValueError):
            mh907_nneg(-0.1, "x")

    def test_pos_zero_no_negativo_no(self):
        with self.assertRaises(ValueError):
            mh907_pos(0, "x")
        with self.assertRaises(ValueError):
            mh907_pos(-1, "x")
        self.assertEqual(mh907_pos(3, "x"), 3.0)

    def test_fraz_bordi(self):
        self.assertEqual(mh907_fraz(0, "x"), 0.0)
        self.assertEqual(mh907_fraz(1, "x"), 1.0)
        self.assertEqual(mh907_fraz(0.10, "x"), 0.10)
        with self.assertRaises(ValueError):
            mh907_fraz(-0.01, "x")
        with self.assertRaises(ValueError):
            mh907_fraz(1.01, "x")

    def test_durata_bordi(self):
        self.assertEqual(mh907_durata(0, "x"), 0)
        self.assertEqual(mh907_durata(5, "x"), 5)
        self.assertEqual(mh907_durata(5.0, "x"), 5)
        with self.assertRaises(ValueError):
            mh907_durata(-1, "x")
        with self.assertRaises(ValueError):
            mh907_durata(2.5, "x")
        with self.assertRaises(ValueError):
            mh907_durata(float("nan"), "x")

    def test_intero_bordi(self):
        self.assertEqual(mh907_intero(0, "x"), 0)
        self.assertEqual(mh907_intero(40, "x"), 40)
        self.assertEqual(mh907_intero(25.0, "x"), 25)
        with self.assertRaises(ValueError):
            mh907_intero(-1, "x")
        with self.assertRaises(ValueError):
            mh907_intero(2.5, "x")
        with self.assertRaises(ValueError):
            mh907_intero(float("nan"), "x")


class TestFisica(unittest.TestCase):
    def test_p_attivata_eff_minimo(self):
        self.assertEqual(mh907_p_attivata_eff(4.0, 5.0), 4.0)
        self.assertEqual(mh907_p_attivata_eff(5.0, 5.0), 5.0)
        self.assertEqual(mh907_p_attivata_eff(10.0, 5.0), 5.0)
        self.assertEqual(mh907_p_attivata_eff(0.0, 5.0), 0.0)
        self.assertEqual(mh907_p_attivata_eff(4.0, 0.0), 0.0)
        with self.assertRaises(ValueError):
            mh907_p_attivata_eff(-1.0, 5.0)
        with self.assertRaises(ValueError):
            mh907_p_attivata_eff(4.0, -1.0)

    def test_ricavo_disp(self):
        self.assertEqual(mh907_ricavo_disp(5.0, 30000.0, 0.95),
                         142500.0)
        self.assertEqual(mh907_ricavo_disp(5.0, 39000.0, 0.95),
                         185250.0)
        self.assertEqual(mh907_ricavo_disp(5.0, 21000.0, 0.95),
                         99750.0)
        self.assertEqual(mh907_ricavo_disp(5.0, 30000.0, 0.80),
                         120000.0)
        self.assertEqual(mh907_ricavo_disp(0.0, 30000.0, 0.95),
                         0.0)
        self.assertEqual(mh907_ricavo_disp(5.0, 0.0, 0.95), 0.0)
        self.assertEqual(mh907_ricavo_disp(5.0, 30000.0, 0.0),
                         0.0)
        with self.assertRaises(ValueError):
            mh907_ricavo_disp(-1.0, 30000.0, 0.95)
        with self.assertRaises(ValueError):
            mh907_ricavo_disp(5.0, 30000.0, 1.5)

    def test_e_attivata(self):
        self.assertEqual(mh907_e_attivata(40, 2.0, 4.0), 320.0)
        self.assertEqual(mh907_e_attivata(20, 2.0, 4.0), 160.0)
        self.assertEqual(mh907_e_attivata(40, 2.0, 5.0), 400.0)
        self.assertEqual(mh907_e_attivata(0, 2.0, 4.0), 0.0)
        self.assertEqual(mh907_e_attivata(40, 0.0, 4.0), 0.0)
        with self.assertRaises(ValueError):
            mh907_e_attivata(-1, 2.0, 4.0)
        with self.assertRaises(ValueError):
            mh907_e_attivata(40.5, 2.0, 4.0)

    def test_ricavo_energia(self):
        self.assertEqual(mh907_ricavo_energia(320.0, 180.0),
                         57600.0)
        self.assertEqual(mh907_ricavo_energia(160.0, 180.0),
                         28800.0)
        self.assertEqual(mh907_ricavo_energia(0.0, 180.0), 0.0)
        self.assertEqual(mh907_ricavo_energia(320.0, 0.0), 0.0)
        with self.assertRaises(ValueError):
            mh907_ricavo_energia(-1.0, 180.0)

    def test_e_mancata_e_penalita(self):
        self.assertEqual(mh907_e_mancata(320.0, 0.05), 16.0)
        self.assertEqual(mh907_e_mancata(320.0, 1.0), 320.0)
        self.assertEqual(mh907_e_mancata(0.0, 0.05), 0.0)
        self.assertEqual(mh907_penalita(16.0, 250.0), 4000.0)
        self.assertEqual(mh907_penalita(320.0, 250.0), 80000.0)
        self.assertEqual(mh907_penalita(16.0, 0.0), 0.0)
        with self.assertRaises(ValueError):
            mh907_e_mancata(320.0, 1.5)
        with self.assertRaises(ValueError):
            mh907_penalita(-1.0, 250.0)

    def test_costo_siti_e_costo_anno(self):
        self.assertEqual(
            mh907_costo_siti(25, 800.0, 320.0, 40.0), 32800.0)
        self.assertEqual(
            mh907_costo_siti(25, 800.0, 160.0, 40.0), 26400.0)
        self.assertEqual(
            mh907_costo_siti(25, 800.0, 320.0, 0.0), 20000.0)
        self.assertEqual(
            mh907_costo_siti(25, 0.0, 320.0, 40.0), 12800.0)
        self.assertEqual(
            mh907_costo_siti(0, 800.0, 320.0, 40.0), 12800.0)
        self.assertEqual(mh907_costo_anno(60000.0, 32800.0),
                         92800.0)
        self.assertEqual(mh907_costo_anno(0.0, 32800.0),
                         32800.0)
        with self.assertRaises(ValueError):
            mh907_costo_siti(-1, 800.0, 320.0, 40.0)
        with self.assertRaises(ValueError):
            mh907_costo_anno(-1.0, 32800.0)

    def test_margine(self):
        self.assertEqual(
            mh907_margine(142500.0, 57600.0, 4000.0, 92800.0),
            103300.0)
        self.assertEqual(
            mh907_margine(185250.0, 57600.0, 4000.0, 92800.0),
            146050.0)
        self.assertEqual(
            mh907_margine(0.0, 57600.0, 4000.0, 92800.0),
            -39200.0)
        self.assertEqual(
            mh907_margine(142500.0, 0.0, 4000.0, 92800.0),
            45700.0)
        self.assertEqual(
            mh907_margine(142500.0, 57600.0, 80000.0, 92800.0),
            27300.0)

    def test_annuity(self):
        self.assertAlmostEqual(mh907_annuity(5, 0.05),
                               4.3294766706308225, places=9)
        self.assertAlmostEqual(mh907_annuity(3, 0.05),
                               2.723248029370478, places=9)
        self.assertEqual(mh907_annuity(5, 0.0), 5.0)
        self.assertEqual(mh907_annuity(0, 0.05), 0.0)
        self.assertEqual(mh907_annuity(0, 0.0), 0.0)
        self.assertAlmostEqual(mh907_annuity(5, 0.10),
                               3.79078676940845, places=9)
        with self.assertRaises(ValueError):
            mh907_annuity(-1, 0.05)
        with self.assertRaises(ValueError):
            mh907_annuity(2.5, 0.05)

    def test_van(self):
        self.assertAlmostEqual(
            mh907_van(150000.0, 103300.0, 5, 0.05),
            297234.94007616397, places=2)
        self.assertAlmostEqual(
            mh907_van(150000.0, 146050.0, 5, 0.05),
            482320.0677456317, places=2)
        self.assertAlmostEqual(
            mh907_van(150000.0, 60550.0, 5, 0.05),
            112149.81240669632, places=2)
        self.assertAlmostEqual(
            mh907_van(150000.0, 103300.0, 3, 0.05),
            131311.52143397054, places=2)
        self.assertEqual(mh907_van(150000.0, 103300.0, 0, 0.05),
                         -150000.0)
        self.assertAlmostEqual(
            mh907_van(0.0, 103300.0, 5, 0.05),
            447234.94007616397, places=2)
        self.assertAlmostEqual(
            mh907_van(150000.0, 103300.0, 5, 0.0),
            366500.0, places=2)
        self.assertAlmostEqual(
            mh907_van(150000.0, -80000.0, 5, 0.05),
            -496358.1336504658, places=2)

    def test_tir(self):
        self.assertAlmostEqual(mh907_tir(150000.0, 103300.0, 5),
                               0.6285485254602656, places=4)
        self.assertAlmostEqual(mh907_tir(150000.0, 146050.0, 5),
                               0.9380561273969079, places=4)
        self.assertAlmostEqual(mh907_tir(150000.0, 60550.0, 5),
                               0.29118555746784813, places=4)
        self.assertAlmostEqual(mh907_tir(150000.0, 103300.0, 3),
                               0.47333796416748397, places=4)
        self.assertAlmostEqual(mh907_tir(150000.0, 27300.0, 5),
                               -0.030635194546337174, places=4)
        self.assertIsNone(mh907_tir(0.0, 103300.0, 5))
        self.assertIsNone(mh907_tir(150000.0, 0.0, 5))
        self.assertIsNone(mh907_tir(150000.0, -39200.0, 5))
        self.assertIsNone(mh907_tir(150000.0, 103300.0, 0))
        # Alla TIR il VAN e zero.
        tir = mh907_tir(150000.0, 103300.0, 5)
        self.assertAlmostEqual(
            mh907_van(150000.0, 103300.0, 5, tir), 0.0, places=2)

    def test_payback(self):
        self.assertEqual(mh907_payback(150000.0, 103300.0, 5), 2)
        self.assertEqual(mh907_payback(150000.0, 146050.0, 5), 2)
        self.assertEqual(mh907_payback(150000.0, 60550.0, 5), 3)
        self.assertEqual(mh907_payback(150000.0, 45700.0, 5), 4)
        self.assertEqual(mh907_payback(150000.0, 103300.0, 3), 2)
        self.assertEqual(mh907_payback(0.0, 103300.0, 5), 0)
        self.assertIsNone(mh907_payback(150000.0, 0.0, 5))
        self.assertIsNone(mh907_payback(150000.0, -39200.0, 5))
        self.assertIsNone(mh907_payback(150000.0, 103300.0, 0))
        # Margine troppo piccolo: mai entro la durata.
        self.assertIsNone(mh907_payback(150000.0, 27300.0, 5))
        self.assertEqual(mh907_payback(150000.0, 27300.0, 6), 6)

    def test_payback_fraz(self):
        self.assertAlmostEqual(
            mh907_payback_fraz(150000.0, 103300.0, 5),
            1.452081316553727, places=9)
        self.assertAlmostEqual(
            mh907_payback_fraz(150000.0, 146050.0, 5),
            1.0270455323519343, places=9)
        self.assertAlmostEqual(
            mh907_payback_fraz(150000.0, 27300.0, 5),
            5.4945054945054945, places=9)
        self.assertEqual(mh907_payback_fraz(0.0, 103300.0, 5),
                         0.0)
        self.assertIsNone(mh907_payback_fraz(150000.0, 0.0, 5))
        self.assertIsNone(
            mh907_payback_fraz(150000.0, -39200.0, 5))
        self.assertIsNone(
            mh907_payback_fraz(150000.0, 103300.0, 0))

    def test_be_prezzo_disp(self):
        self.assertAlmostEqual(
            mh907_be_prezzo_disp(92800.0, 4000.0, 57600.0,
                                 5.0, 0.95),
            8252.631578947368, places=2)
        self.assertAlmostEqual(
            mh907_be_prezzo_disp(86400.0, 2000.0, 28800.0,
                                 5.0, 0.95),
            12547.368421052632, places=2)
        self.assertAlmostEqual(
            mh907_be_prezzo_disp(92800.0, 4000.0, 57600.0,
                                 5.0, 0.80),
            9800.0, places=2)
        self.assertAlmostEqual(
            mh907_be_prezzo_disp(92800.0, 4000.0, 0.0,
                                 5.0, 0.95),
            20378.947368421053, places=2)
        self.assertIsNone(
            mh907_be_prezzo_disp(92800.0, 4000.0, 57600.0,
                                 0.0, 0.95))
        self.assertIsNone(
            mh907_be_prezzo_disp(92800.0, 4000.0, 57600.0,
                                 5.0, 0.0))
        # Numeratore negativo: la sola energia copre
        # gia i costi, il breakeven non esiste.
        self.assertIsNone(
            mh907_be_prezzo_disp(32800.0, 4000.0, 57600.0,
                                 5.0, 0.95))
        with self.assertRaises(ValueError):
            mh907_be_prezzo_disp(-1.0, 4000.0, 57600.0, 5.0,
                                 0.95)
        # Al prezzo disponibilita di breakeven il
        # margine e zero e il verdetto e
        # NON_CALCOLABILE.
        be = mh907_be_prezzo_disp(92800.0, 4000.0, 57600.0,
                                  5.0, 0.95)
        bc = mh907_calcola(
            **_demo_kwargs(prezzo_disp_eur_mw_anno=be))
        self.assertAlmostEqual(bc["margine_eur_anno"], 0.0,
                               places=2)
        self.assertAlmostEqual(bc["van_eur"], -150000.0,
                               places=2)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_be_prezzo_energia(self):
        self.assertIsNone(
            mh907_be_prezzo_energia(92800.0, 4000.0,
                                    142500.0, 320.0))
        self.assertAlmostEqual(
            mh907_be_prezzo_energia(92800.0, 4000.0, 0.0,
                                    320.0),
            302.5, places=2)
        self.assertAlmostEqual(
            mh907_be_prezzo_energia(92800.0, 80000.0,
                                    142500.0, 320.0),
            94.6875, places=2)
        self.assertIsNone(
            mh907_be_prezzo_energia(92800.0, 4000.0,
                                    142500.0, 0.0))
        with self.assertRaises(ValueError):
            mh907_be_prezzo_energia(-1.0, 4000.0, 142500.0,
                                    320.0)
        # Al prezzo energia di breakeven (caso con
        # prezzo disponibilita zero) il margine e
        # zero e il verdetto e NON_CALCOLABILE.
        be = mh907_be_prezzo_energia(92800.0, 4000.0, 0.0,
                                     320.0)
        bc = mh907_calcola(
            **_demo_kwargs(prezzo_disp_eur_mw_anno=0.0,
                           prezzo_energia_eur_mwh=be))
        self.assertAlmostEqual(bc["margine_eur_anno"], 0.0,
                               places=2)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_be_disp_invariante_prezzo_corrente(self):
        # Il breakeven prezzo disponibilita e
        # INVARIANTE al prezzo disponibilita corrente.
        bc0 = demo_calcoli()
        bc = mh907_calcola(
            **_demo_kwargs(prezzo_disp_eur_mw_anno=39000.0))
        self.assertEqual(bc["be_prezzo_disp_eur_mw_anno"],
                         bc0["be_prezzo_disp_eur_mw_anno"])
        self.assertAlmostEqual(
            bc["be_prezzo_disp_eur_mw_anno"], 8252.63,
            places=2)

    def test_be_energia_invariante_prezzo_corrente(self):
        # Il breakeven prezzo energia e INVARIANTE
        # al prezzo energia corrente.
        bc0 = mh907_calcola(
            **_demo_kwargs(prezzo_disp_eur_mw_anno=0.0))
        bc = mh907_calcola(
            **_demo_kwargs(prezzo_disp_eur_mw_anno=0.0,
                           prezzo_energia_eur_mwh=100.0))
        self.assertEqual(bc["be_prezzo_energia_eur_mwh"],
                         bc0["be_prezzo_energia_eur_mwh"])
        self.assertAlmostEqual(
            bc["be_prezzo_energia_eur_mwh"], 302.5, places=2)

    def test_co2(self):
        self.assertEqual(mh907_co2(320.0, 0.35), 112.0)
        self.assertEqual(mh907_co2(160.0, 0.35), 56.0)
        self.assertEqual(mh907_co2(0.0, 0.35), 0.0)
        self.assertEqual(mh907_co2(320.0, 0.0), 0.0)
        self.assertEqual(mh907_co2(1000.0, 0.35), 350.0)
        with self.assertRaises(ValueError):
            mh907_co2(-1.0, 0.35)
        with self.assertRaises(ValueError):
            mh907_co2(320.0, -0.1)

    def test_scenario_singolo(self):
        s = mh907_scenario("Disponibilita piu 30 %",
                           mh907_demo(),
                           {"prezzo_disp_eur_mw_anno": 39000.0})
        self.assertEqual(s["nome"], "Disponibilita piu 30 %")
        self.assertEqual(s["prezzo_disp_eur_mw_anno"], 39000.0)
        self.assertAlmostEqual(s["van_eur"], 482320.07,
                               places=2)
        self.assertEqual(s["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(
            s["be_prezzo_disp_eur_mw_anno"], 8252.63, places=2)
        self.assertIsNone(s["be_prezzo_energia_eur_mwh"])
        s = mh907_scenario("Disponibilita meno 30 %",
                           mh907_demo(),
                           {"prezzo_disp_eur_mw_anno": 21000.0})
        self.assertAlmostEqual(s["van_eur"], 112149.81,
                               places=2)
        self.assertEqual(s["payback_anni"], 3)
        self.assertEqual(s["verdetto"], "CONVIENTE")
        s = mh907_scenario("Attivazioni meno 50 %",
                           mh907_demo(),
                           {"n_attivazioni_anno": 20})
        self.assertAlmostEqual(s["e_attivata_mwh"], 160.0,
                               places=9)
        self.assertAlmostEqual(s["van_eur"], 208913.62,
                               places=2)
        self.assertAlmostEqual(
            s["be_prezzo_disp_eur_mw_anno"], 12547.37,
            places=2)
        s = mh907_scenario("Disponibilita 0,80", mh907_demo(),
                           {"disponibilita_frazione": 0.80})
        self.assertAlmostEqual(s["van_eur"], 199821.71,
                               places=2)
        self.assertAlmostEqual(
            s["be_prezzo_disp_eur_mw_anno"], 9800.0, places=2)
        s = mh907_scenario("Durata 3 anni", mh907_demo(),
                           {"durata_anni": 3})
        self.assertAlmostEqual(s["van_eur"], 131311.52,
                               places=2)
        self.assertEqual(s["verdetto"], "CONVIENTE")
        with self.assertRaises(ValueError):
            mh907_scenario("", mh907_demo(),
                           {"prezzo_disp_eur_mw_anno": 39000.0})
        with self.assertRaises(ValueError):
            mh907_scenario("X", mh907_demo(),
                           {"durata_anni": -1})

    def test_scenario_p_offerta_zero(self):
        s = mh907_scenario("Potenza offerta 0", mh907_demo(),
                           {"p_offerta_mw": 0.0})
        self.assertEqual(s["p_attivata_eff_mw"], 0.0)
        self.assertEqual(s["e_attivata_mwh"], 0.0)
        self.assertEqual(s["ricavo_disp_eur_anno"], 0.0)
        self.assertEqual(s["margine_eur_anno"], -80000.0)
        self.assertIsNone(s["be_prezzo_disp_eur_mw_anno"])
        self.assertIsNone(s["be_prezzo_energia_eur_mwh"])
        self.assertEqual(s["verdetto"], "NON_CALCOLABILE")

    def test_confronto_formule(self):
        c = mh907_confronto(4.0, 320.0, 142500.0, 57600.0,
                            16.0, 4000.0, 32800.0, 92800.0,
                            103300.0, 297234.94007616397,
                            0.6285485254602656, 2,
                            8252.631578947368, None, 112.0,
                            "CONVIENTE")
        self.assertEqual(c["p_attivata_eff_mw"], 4.0)
        self.assertEqual(c["e_attivata_mwh"], 320.0)
        self.assertEqual(c["ricavo_disp_eur_anno"], 142500.0)
        self.assertEqual(c["ricavo_energia_eur_anno"], 57600.0)
        self.assertEqual(c["e_mancata_mwh"], 16.0)
        self.assertEqual(c["penalita_eur"], 4000.0)
        self.assertEqual(c["costo_siti_eur_anno"], 32800.0)
        self.assertEqual(c["costo_anno_eur"], 92800.0)
        self.assertEqual(c["margine_eur_anno"], 103300.0)
        self.assertEqual(c["van_eur"], 297234.94007616397)
        self.assertEqual(c["tir_frazione"],
                         0.6285485254602656)
        self.assertEqual(c["payback_anni"], 2)
        self.assertEqual(c["be_prezzo_disp_eur_mw_anno"],
                         8252.631578947368)
        self.assertIsNone(c["be_prezzo_energia_eur_mwh"])
        self.assertEqual(c["co2_t_anno"], 112.0)
        self.assertEqual(c["verdetto"], "CONVIENTE")
        c = mh907_confronto(0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                            20000.0, 80000.0, -80000.0,
                            -496358.1336504658, None, None,
                            None, None, 0.0, "NON_CALCOLABILE")
        self.assertIsNone(c["tir_frazione"])
        self.assertIsNone(c["payback_anni"])
        self.assertIsNone(c["be_prezzo_disp_eur_mw_anno"])
        self.assertIsNone(c["be_prezzo_energia_eur_mwh"])
        self.assertEqual(c["verdetto"], "NON_CALCOLABILE")
        with self.assertRaises(ValueError):
            mh907_confronto(4.0, 320.0, 142500.0, 57600.0,
                            16.0, 4000.0, 32800.0, 92800.0,
                            103300.0, 297234.94007616397,
                            0.6285485254602656, 2,
                            8252.631578947368, None, 112.0,
                            "FORSE")
        with self.assertRaises(ValueError):
            mh907_confronto(4.0, 320.0, -1.0, 57600.0,
                            16.0, 4000.0, 32800.0, 92800.0,
                            103300.0, 297234.94007616397,
                            0.6285485254602656, 2,
                            8252.631578947368, None, 112.0,
                            "CONVIENTE")


class TestFinanza(unittest.TestCase):
    def test_verdetto_bordi(self):
        self.assertEqual(
            mh907_verdetto(100.0, 0.10, 150000.0, 103300.0),
            "CONVIENTE")
        self.assertEqual(
            mh907_verdetto(0.0, 0.10, 150000.0, 103300.0),
            "MARGINALE")
        self.assertEqual(
            mh907_verdetto(-15000.0, 0.10, 150000.0, 103300.0),
            "MARGINALE")
        self.assertEqual(
            mh907_verdetto(-15001.0, 0.10, 150000.0, 103300.0),
            "NON_CONVIENTE")
        self.assertEqual(
            mh907_verdetto(-50000.0, 0.10, 150000.0, 103300.0),
            "NON_CONVIENTE")
        # Con tolleranza zero ogni VAN negativo
        # e NON_CONVIENTE (VAN zero compreso nel
        # MARGINALE solo perche il valore assoluto
        # zero e minore o uguale a zero).
        self.assertEqual(
            mh907_verdetto(-1.0, 0.0, 150000.0, 103300.0),
            "NON_CONVIENTE")
        self.assertEqual(
            mh907_verdetto(0.0, 0.0, 150000.0, 103300.0),
            "MARGINALE")
        with self.assertRaises(ValueError):
            mh907_verdetto(100.0, 1.5, 150000.0, 103300.0)
        with self.assertRaises(ValueError):
            mh907_verdetto(100.0, 0.10, -1.0, 103300.0)

    def test_verdetto_none_non_calcolabile(self):
        self.assertEqual(
            mh907_verdetto(None, 0.10, 150000.0, 103300.0),
            "NON_CALCOLABILE")
        self.assertEqual(
            mh907_verdetto(None, 0.0, 0.0, 103300.0),
            "NON_CALCOLABILE")
        self.assertEqual(
            mh907_verdetto(100.0, 0.10, 150000.0, None),
            "NON_CALCOLABILE")

    def test_verdetto_margine_zero_negativo_non_calcolabile(self):
        self.assertEqual(
            mh907_verdetto(-150000.0, 0.10, 150000.0, 0.0),
            "NON_CALCOLABILE")
        self.assertEqual(
            mh907_verdetto(-319715.49, 0.10, 150000.0, -39200.0),
            "NON_CALCOLABILE")
        self.assertEqual(
            mh907_verdetto(297234.94, 0.10, 150000.0, 103300.0),
            "CONVIENTE")

    def test_verdetto_capex_zero(self):
        # Con CAPEX zero la tolleranza non copre
        # nulla: ogni VAN negativo e NON_CONVIENTE.
        self.assertEqual(
            mh907_verdetto(-1.0, 0.10, 0.0, 103300.0),
            "NON_CONVIENTE")
        self.assertEqual(
            mh907_verdetto(0.0, 0.10, 0.0, 103300.0),
            "MARGINALE")

    def test_valida_demo_ok(self):
        demo = mh907_demo()
        val = mh907_valida(*[demo[k] for k in _ORDINE_VALIDA])
        self.assertTrue(val["valido"])
        self.assertEqual(val["errore"], "")

    def test_valida_durata_intervallo(self):
        with self.assertRaises(ValueError):
            mh907_calcola(**_demo_kwargs(durata_anni=-1))
        with self.assertRaises(ValueError):
            mh907_calcola(**_demo_kwargs(durata_anni=2.5))
        bc = mh907_calcola(**_demo_kwargs(durata_anni=0))
        self.assertEqual(bc["durata_anni"], 0)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        bc = mh907_calcola(**_demo_kwargs(durata_anni=3))
        self.assertEqual(bc["durata_anni"], 3)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_valida_p_offerta_zero_ammesso(self):
        demo = mh907_demo()
        val = mh907_valida(*[dict(demo, p_offerta_mw=0.0)[k]
                             for k in _ORDINE_VALIDA])
        self.assertTrue(val["valido"])
        bc = mh907_calcola(**_demo_kwargs(p_offerta_mw=0.0))
        self.assertEqual(bc["p_attivata_eff_mw"], 0.0)
        self.assertEqual(bc["e_attivata_mwh"], 0.0)
        self.assertIsNone(bc["be_prezzo_disp_eur_mw_anno"])
        self.assertIsNone(bc["be_prezzo_energia_eur_mwh"])
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_valida_prezzo_disp_zero_ammesso(self):
        demo = mh907_demo()
        val = mh907_valida(
            *[dict(demo, prezzo_disp_eur_mw_anno=0.0)[k]
              for k in _ORDINE_VALIDA])
        self.assertTrue(val["valido"])
        bc = mh907_calcola(
            **_demo_kwargs(prezzo_disp_eur_mw_anno=0.0))
        self.assertEqual(bc["ricavo_disp_eur_anno"], 0.0)
        self.assertAlmostEqual(
            bc["be_prezzo_energia_eur_mwh"], 302.5, places=2)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_valida_prezzo_energia_zero_ammesso(self):
        demo = mh907_demo()
        val = mh907_valida(
            *[dict(demo, prezzo_energia_eur_mwh=0.0)[k]
              for k in _ORDINE_VALIDA])
        self.assertTrue(val["valido"])
        bc = mh907_calcola(
            **_demo_kwargs(prezzo_energia_eur_mwh=0.0))
        self.assertEqual(bc["ricavo_energia_eur_anno"], 0.0)
        self.assertIsNone(bc["be_prezzo_energia_eur_mwh"])
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_valida_capex_zero_ammesso(self):
        demo = mh907_demo()
        val = mh907_valida(*[dict(demo, capex_eur=0.0)[k]
                             for k in _ORDINE_VALIDA])
        self.assertTrue(val["valido"])
        bc = mh907_calcola(**_demo_kwargs(capex_eur=0.0))
        self.assertEqual(bc["payback_anni"], 0)
        self.assertIsNone(bc["tir_frazione"])
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_valida_tasso_sopra_uno_no(self):
        with self.assertRaises(ValueError):
            mh907_calcola(**_demo_kwargs(tasso_frazione=1.5))
        bc = mh907_calcola(**_demo_kwargs(tasso_frazione=0.0))
        self.assertEqual(bc["tasso_frazione"], 0.0)
        bc = mh907_calcola(**_demo_kwargs(tasso_frazione=1.0))
        self.assertEqual(bc["tasso_frazione"], 1.0)

    def test_valida_tolleranza_sopra_uno_no(self):
        with self.assertRaises(ValueError):
            mh907_calcola(**_demo_kwargs(tol_frazione=1.5))
        bc = mh907_calcola(**_demo_kwargs(tol_frazione=0.0))
        self.assertEqual(bc["tol_frazione"], 0.0)

    def test_valida_nan_no(self):
        kw = _demo_kwargs(prezzo_disp_eur_mw_anno=float("nan"))
        self.assertRaises(ValueError, mh907_calcola, **kw)
        kw = _demo_kwargs(tol_frazione=float("inf"))
        self.assertRaises(ValueError, mh907_calcola, **kw)

    def test_valida_negativi_no(self):
        for campo, valore in (
                ("p_offerta_mw", -1),
                ("prezzo_disp_eur_mw_anno", -1),
                ("disponibilita_frazione", -0.1),
                ("disponibilita_frazione", 1.5),
                ("n_attivazioni_anno", -1),
                ("durata_attivazione_h", -1),
                ("p_attivata_mw", -1),
                ("prezzo_energia_eur_mwh", -1),
                ("quota_fallimento_frazione", -0.1),
                ("quota_fallimento_frazione", 1.5),
                ("penalita_eur_mwh", -1),
                ("costo_piattaforma_eur_anno", -1),
                ("n_siti", -1),
                ("costo_sito_eur_anno", -1),
                ("compenso_siti_eur_mwh", -1),
                ("capex_eur", -1),
                ("tasso_frazione", -0.1),
                ("tol_frazione", -0.1),
                ("fattore_co2_t_mwh", -0.1)):
            with self.assertRaises(ValueError):
                mh907_calcola(**_demo_kwargs(**{campo: valore}))

    def test_valida_non_interi_no(self):
        with self.assertRaises(ValueError):
            mh907_calcola(**_demo_kwargs(n_attivazioni_anno=2.5))
        with self.assertRaises(ValueError):
            mh907_calcola(**_demo_kwargs(n_siti=2.5))

    def test_calcola_accetta_dict(self):
        bc = mh907_calcola(mh907_demo())
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertEqual(len(bc["scenari"]), 6)

    def test_calcola_keyword_vince_su_dict(self):
        bc = mh907_calcola(dict(mh907_demo(),
                                prezzo_disp_eur_mw_anno=999.0),
                           prezzo_disp_eur_mw_anno=30000.0)
        self.assertEqual(bc["prezzo_disp_eur_mw_anno"], 30000.0)

    def test_calcola_senza_scenari_anti_ricorsione(self):
        bc = mh907_calcola(_scenari=False, **mh907_demo())
        self.assertEqual(bc["scenari"], [])
        self.assertIsNone(bc["scenario_base"])
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        self.assertAlmostEqual(bc["van_eur"], 297234.94,
                               places=2)
        self.assertAlmostEqual(
            bc["be_prezzo_disp_eur_mw_anno"], 8252.63,
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
        self.assertAlmostEqual(bc["tir_frazione"], 0.6285,
                               places=4)
        self.assertAlmostEqual(
            bc["be_prezzo_disp_eur_mw_anno"], 8252.63, places=2)
        self.assertIsNone(bc["be_prezzo_energia_eur_mwh"])
        self.assertEqual(bc["scenario_base"]["verdetto"],
                         "CONVIENTE")
        self.assertEqual(bc["payback_anni"], 2)
        self.assertAlmostEqual(bc["co2_t_anno"], 112.0,
                               places=2)

    def test_coerenza_fisica_e_costi(self):
        bc = demo_calcoli()
        self.assertAlmostEqual(
            bc["p_attivata_eff_mw"],
            min(bc["p_attivata_mw"], bc["p_offerta_mw"]))
        self.assertAlmostEqual(
            bc["e_attivata_mwh"],
            bc["n_attivazioni_anno"]
            * bc["durata_attivazione_h"]
            * bc["p_attivata_eff_mw"])
        self.assertAlmostEqual(
            bc["ricavo_disp_eur_anno"],
            bc["p_offerta_mw"]
            * bc["prezzo_disp_eur_mw_anno"]
            * bc["disponibilita_frazione"])
        self.assertAlmostEqual(
            bc["ricavo_energia_eur_anno"],
            bc["e_attivata_mwh"]
            * bc["prezzo_energia_eur_mwh"])
        self.assertAlmostEqual(
            bc["e_mancata_mwh"],
            bc["e_attivata_mwh"]
            * bc["quota_fallimento_frazione"])
        self.assertAlmostEqual(
            bc["penalita_eur"],
            bc["e_mancata_mwh"] * bc["penalita_eur_mwh"])
        self.assertAlmostEqual(
            bc["costo_siti_eur_anno"],
            bc["n_siti"] * bc["costo_sito_eur_anno"]
            + bc["e_attivata_mwh"]
            * bc["compenso_siti_eur_mwh"])
        self.assertAlmostEqual(
            bc["costo_anno_eur"],
            bc["costo_piattaforma_eur_anno"]
            + bc["costo_siti_eur_anno"])
        self.assertAlmostEqual(
            bc["margine_eur_anno"],
            bc["ricavo_disp_eur_anno"]
            + bc["ricavo_energia_eur_anno"]
            - bc["penalita_eur"] - bc["costo_anno_eur"])
        self.assertAlmostEqual(
            bc["van_eur"],
            -bc["capex_eur"] + bc["margine_eur_anno"]
            * mh907_annuity(bc["durata_anni"],
                            bc["tasso_frazione"]))
        self.assertAlmostEqual(
            bc["be_prezzo_disp_eur_mw_anno"],
            (bc["costo_anno_eur"] + bc["penalita_eur"]
             - bc["ricavo_energia_eur_anno"])
            / (bc["p_offerta_mw"]
               * bc["disponibilita_frazione"]))
        self.assertAlmostEqual(
            bc["co2_t_anno"],
            bc["e_attivata_mwh"]
            * bc["fattore_co2_t_mwh"])
        self.assertAlmostEqual(
            bc["payback_fraz_anni"],
            bc["capex_eur"] / bc["margine_eur_anno"])
        conf = bc["confronto"]
        self.assertEqual(conf["van_eur"], bc["van_eur"])
        self.assertEqual(conf["tir_frazione"],
                         bc["tir_frazione"])
        self.assertEqual(conf["payback_anni"],
                         bc["payback_anni"])
        self.assertEqual(conf["verdetto"], bc["verdetto"])
        # Flussi: anno zero meno CAPEX, poi margine
        # per ogni anno di durata; il cumulato
        # supera il CAPEX al secondo anno.
        fl = bc["df_flussi"]
        self.assertEqual(len(fl), 6)
        self.assertEqual(fl["Flusso (EUR)"].iloc[0], -150000.0)
        self.assertEqual(fl["Flusso (EUR)"].iloc[1], 103300.0)
        self.assertEqual(fl["Cumulato (EUR)"].iloc[1], -46700.0)
        self.assertEqual(fl["Cumulato (EUR)"].iloc[2], 56600.0)
        self.assertEqual(fl["Cumulato (EUR)"].iloc[5], 366500.0)
        # Ricavi contro costi: disponibilita ed
        # energia positivi, penalita e costo anno
        # negativi, margine uguale alla somma.
        rc = bc["df_ricavi_costi"]
        self.assertEqual(len(rc), 5)
        self.assertAlmostEqual(
            rc["Valore"].iloc[0] + rc["Valore"].iloc[1]
            + rc["Valore"].iloc[2] + rc["Valore"].iloc[3],
            rc["Valore"].iloc[4])

    def test_scenari_ordinamento_e_invarianza(self):
        bc = demo_calcoli()
        base = bc["scenari"][0]
        # Piu prezzo disponibilita migliora il caso
        # e resta CONVIENTE; il breakeven prezzo
        # disponibilita e INVARIANTE al prezzo
        # disponibilita corrente.
        self.assertGreater(
            bc["scenari"][1]["van_eur"], base["van_eur"])
        self.assertGreater(bc["scenari"][1]["van_eur"], 0.0)
        self.assertEqual(bc["scenari"][1]["verdetto"],
                         "CONVIENTE")
        self.assertEqual(
            bc["scenari"][1]["be_prezzo_disp_eur_mw_anno"],
            base["be_prezzo_disp_eur_mw_anno"])
        self.assertIsNone(
            bc["scenari"][1]["be_prezzo_energia_eur_mwh"])
        # Meno prezzo disponibilita peggiora il caso
        # ma resta CONVIENTE, con payback piu lungo.
        self.assertLess(bc["scenari"][2]["van_eur"],
                        base["van_eur"])
        self.assertGreater(bc["scenari"][2]["van_eur"], 0.0)
        self.assertEqual(bc["scenari"][2]["verdetto"],
                         "CONVIENTE")
        self.assertEqual(bc["scenari"][2]["payback_anni"], 3)
        self.assertEqual(
            bc["scenari"][2]["be_prezzo_disp_eur_mw_anno"],
            base["be_prezzo_disp_eur_mw_anno"])
        # Attivazioni meno 50 per cento dimezzano
        # l'energia attivata e la CO2 ma il caso
        # resta CONVIENTE.
        self.assertAlmostEqual(bc["scenari"][3]["e_attivata_mwh"],
                               160.0, places=9)
        self.assertAlmostEqual(bc["scenari"][3]["co2_t_anno"],
                               56.0, places=2)
        self.assertLess(bc["scenari"][3]["van_eur"],
                        base["van_eur"])
        self.assertEqual(bc["scenari"][3]["verdetto"],
                         "CONVIENTE")
        self.assertEqual(bc["scenari"][3]["payback_anni"], 2)
        # Disponibilita 0,80: ricavo disponibilita
        # piu basso ma caso ancora CONVIENTE.
        self.assertAlmostEqual(
            bc["scenari"][4]["ricavo_disp_eur_anno"],
            120000.0, places=2)
        self.assertAlmostEqual(
            bc["scenari"][4]["be_prezzo_disp_eur_mw_anno"],
            9800.0, places=2)
        self.assertEqual(bc["scenari"][4]["verdetto"],
                         "CONVIENTE")
        # Durata 3 anni: VAN ancora positivo e
        # verdetto CONVIENTE.
        self.assertGreater(bc["scenari"][5]["van_eur"], 0.0)
        self.assertEqual(bc["scenari"][5]["verdetto"],
                         "CONVIENTE")
        self.assertEqual(bc["scenari"][5]["payback_anni"], 2)

    def test_sensibilita_valori(self):
        s = mh907_sensibilita(**mh907_demo())
        self.assertEqual(set(s.keys()),
                         {"disp_piu30", "disp_meno30",
                          "att_meno50", "disp_080",
                          "durata_3", "p_offerta_0",
                          "prezzo_disp_0", "prezzo_energia_0",
                          "fall_100", "durata_0", "capex_0",
                          "disp_0", "att_0", "comp_0",
                          "pen_0", "piatt_0", "csito_0",
                          "tasso_0", "tasso_10", "tol_0",
                          "co2_0"})
        attesi = {
            "disp_piu30": (482320.07, 93.81, 2, 8252.63, None,
                           "CONVIENTE"),
            "disp_meno30": (112149.81, 29.12, 3, 8252.63, None,
                            "CONVIENTE"),
            "att_meno50": (208913.62, 47.30, 2, 12547.37, None,
                           "CONVIENTE"),
            "disp_080": (199821.71, 45.65, 2, 9800.00, None,
                         "CONVIENTE"),
            "durata_3": (131311.52, 47.33, 2, 8252.63, None,
                         "CONVIENTE"),
            "p_offerta_0": (-496358.13, None, None, None, None,
                            "NON_CALCOLABILE"),
            "prezzo_disp_0": (-319715.49, None, None, 8252.63,
                              302.50, "NON_CALCOLABILE"),
            "prezzo_energia_0": (47857.08, 15.90, 4, 20378.95,
                                 None, "CONVIENTE"),
            "fall_100": (-31805.29, -3.06, None, 24252.63,
                         94.69, "NON_CONVIENTE"),
            "durata_0": (-150000.0, None, None, 8252.63, None,
                         "NON_CONVIENTE"),
            "capex_0": (447234.94, None, 0, 8252.63, None,
                        "CONVIENTE"),
            "disp_0": (-319715.49, None, None, None, 302.50,
                       "NON_CALCOLABILE"),
            "att_0": (120592.29, 30.77, 3, 16842.11, None,
                      "CONVIENTE"),
            "comp_0": (352652.24, 72.30, 2, 5557.89, None,
                       "CONVIENTE"),
            "pen_0": (314552.85, 65.83, 2, 7410.53, None,
                      "CONVIENTE"),
            "piatt_0": (557003.54, 105.93, 1, None, None,
                        "CONVIENTE"),
            "csito_0": (383824.47, 77.54, 2, 4042.11, None,
                        "CONVIENTE"),
            "tasso_0": (366500.0, 62.85, 2, 8252.63, None,
                        "CONVIENTE"),
            "tasso_10": (241588.27, 62.85, 2, 8252.63, None,
                         "CONVIENTE"),
            "tol_0": (297234.94, 62.85, 2, 8252.63, None,
                      "CONVIENTE"),
            "co2_0": (297234.94, 62.85, 2, 8252.63, None,
                      "CONVIENTE"),
        }
        for nome, (van, tirp, pb, bd, be, vdc) in attesi.items():
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
                if bd is None:
                    self.assertIsNone(
                        s[nome]["be_prezzo_disp_eur_mw_anno"])
                else:
                    self.assertAlmostEqual(
                        s[nome]["be_prezzo_disp_eur_mw_anno"],
                        bd, places=2)
                if be is None:
                    self.assertIsNone(
                        s[nome]["be_prezzo_energia_eur_mwh"])
                else:
                    self.assertAlmostEqual(
                        s[nome]["be_prezzo_energia_eur_mwh"],
                        be, places=2)
                self.assertEqual(s[nome]["verdetto"], vdc)
        for caso in s.values():
            self.assertIn("verdetto", caso)
            self.assertIn("van_eur", caso)
            self.assertIn("tir_frazione", caso)
            self.assertIn("payback_anni", caso)
            self.assertIn("confronto", caso)
            self.assertIn("scenari", caso)


class TestCasiLimite(unittest.TestCase):
    def test_p_offerta_zero_non_calcolabile(self):
        bc = mh907_calcola(**_demo_kwargs(p_offerta_mw=0.0))
        self.assertEqual(bc["p_attivata_eff_mw"], 0.0)
        self.assertEqual(bc["e_attivata_mwh"], 0.0)
        self.assertEqual(bc["ricavo_disp_eur_anno"], 0.0)
        self.assertEqual(bc["ricavo_energia_eur_anno"], 0.0)
        self.assertEqual(bc["costo_siti_eur_anno"], 20000.0)
        self.assertEqual(bc["costo_anno_eur"], 80000.0)
        self.assertEqual(bc["margine_eur_anno"], -80000.0)
        self.assertAlmostEqual(bc["van_eur"], -496358.13,
                               places=2)
        self.assertIsNone(bc["tir_frazione"])
        self.assertIsNone(bc["payback_anni"])
        self.assertIsNone(bc["payback_fraz_anni"])
        self.assertIsNone(bc["be_prezzo_disp_eur_mw_anno"])
        self.assertIsNone(bc["be_prezzo_energia_eur_mwh"])
        self.assertEqual(bc["co2_t_anno"], 0.0)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_prezzo_disp_zero_non_calcolabile(self):
        bc = mh907_calcola(
            **_demo_kwargs(prezzo_disp_eur_mw_anno=0.0))
        self.assertEqual(bc["ricavo_disp_eur_anno"], 0.0)
        self.assertEqual(bc["margine_eur_anno"], -39200.0)
        self.assertAlmostEqual(bc["van_eur"], -319715.49,
                               places=2)
        self.assertIsNone(bc["tir_frazione"])
        self.assertIsNone(bc["payback_anni"])
        self.assertAlmostEqual(
            bc["be_prezzo_disp_eur_mw_anno"], 8252.63,
            places=2)
        self.assertAlmostEqual(
            bc["be_prezzo_energia_eur_mwh"], 302.5, places=2)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_prezzo_energia_zero_conviente(self):
        bc = mh907_calcola(
            **_demo_kwargs(prezzo_energia_eur_mwh=0.0))
        self.assertEqual(bc["ricavo_energia_eur_anno"], 0.0)
        self.assertEqual(bc["margine_eur_anno"], 45700.0)
        self.assertAlmostEqual(bc["van_eur"], 47857.08,
                               places=2)
        self.assertAlmostEqual(bc["tir_frazione"], 0.1590,
                               places=4)
        self.assertEqual(bc["payback_anni"], 4)
        self.assertAlmostEqual(bc["payback_fraz_anni"], 3.28,
                               places=2)
        self.assertAlmostEqual(
            bc["be_prezzo_disp_eur_mw_anno"], 20378.95,
            places=2)
        self.assertIsNone(bc["be_prezzo_energia_eur_mwh"])
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_fallimento_uno_non_conviente(self):
        bc = mh907_calcola(
            **_demo_kwargs(quota_fallimento_frazione=1.0))
        self.assertEqual(bc["e_mancata_mwh"], 320.0)
        self.assertEqual(bc["penalita_eur"], 80000.0)
        self.assertEqual(bc["margine_eur_anno"], 27300.0)
        self.assertAlmostEqual(bc["van_eur"], -31805.29,
                               places=2)
        self.assertAlmostEqual(bc["tir_frazione"], -0.0306,
                               places=4)
        self.assertIsNone(bc["payback_anni"])
        self.assertAlmostEqual(bc["payback_fraz_anni"], 5.49,
                               places=2)
        self.assertAlmostEqual(
            bc["be_prezzo_disp_eur_mw_anno"], 24252.63,
            places=2)
        self.assertAlmostEqual(
            bc["be_prezzo_energia_eur_mwh"], 94.69, places=2)
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")

    def test_durata_zero_non_conviente(self):
        bc = mh907_calcola(**_demo_kwargs(durata_anni=0))
        self.assertEqual(bc["margine_eur_anno"], 103300.0)
        self.assertEqual(bc["van_eur"], -150000.0)
        self.assertIsNone(bc["tir_frazione"])
        self.assertIsNone(bc["payback_anni"])
        self.assertIsNone(bc["payback_fraz_anni"])
        self.assertEqual(bc["verdetto"], "NON_CONVIENTE")
        self.assertEqual(len(bc["df_flussi"]), 1)

    def test_capex_zero_conviente_payback_zero(self):
        bc = mh907_calcola(**_demo_kwargs(capex_eur=0.0))
        self.assertEqual(bc["margine_eur_anno"], 103300.0)
        self.assertAlmostEqual(bc["van_eur"], 447234.94,
                               places=2)
        self.assertIsNone(bc["tir_frazione"])
        self.assertEqual(bc["payback_anni"], 0)
        self.assertEqual(bc["payback_fraz_anni"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_disponibilita_zero_non_calcolabile(self):
        bc = mh907_calcola(
            **_demo_kwargs(disponibilita_frazione=0.0))
        self.assertEqual(bc["ricavo_disp_eur_anno"], 0.0)
        self.assertEqual(bc["margine_eur_anno"], -39200.0)
        self.assertAlmostEqual(bc["van_eur"], -319715.49,
                               places=2)
        self.assertIsNone(bc["tir_frazione"])
        self.assertIsNone(bc["payback_anni"])
        self.assertIsNone(bc["be_prezzo_disp_eur_mw_anno"])
        self.assertAlmostEqual(
            bc["be_prezzo_energia_eur_mwh"], 302.5, places=2)
        self.assertEqual(bc["verdetto"], "NON_CALCOLABILE")

    def test_attivazioni_zero_conviente(self):
        bc = mh907_calcola(**_demo_kwargs(n_attivazioni_anno=0))
        self.assertEqual(bc["e_attivata_mwh"], 0.0)
        self.assertEqual(bc["ricavo_energia_eur_anno"], 0.0)
        self.assertEqual(bc["penalita_eur"], 0.0)
        self.assertEqual(bc["costo_siti_eur_anno"], 20000.0)
        self.assertEqual(bc["costo_anno_eur"], 80000.0)
        self.assertEqual(bc["margine_eur_anno"], 62500.0)
        self.assertAlmostEqual(bc["van_eur"], 120592.29,
                               places=2)
        self.assertAlmostEqual(bc["tir_frazione"], 0.3077,
                               places=4)
        self.assertEqual(bc["payback_anni"], 3)
        self.assertEqual(bc["payback_fraz_anni"], 2.4)
        self.assertAlmostEqual(
            bc["be_prezzo_disp_eur_mw_anno"], 16842.11,
            places=2)
        self.assertIsNone(bc["be_prezzo_energia_eur_mwh"])
        self.assertEqual(bc["co2_t_anno"], 0.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_compenso_siti_zero_e_penalita_zero(self):
        bc = mh907_calcola(
            **_demo_kwargs(compenso_siti_eur_mwh=0.0))
        self.assertEqual(bc["costo_siti_eur_anno"], 20000.0)
        self.assertEqual(bc["costo_anno_eur"], 80000.0)
        self.assertEqual(bc["margine_eur_anno"], 116100.0)
        self.assertAlmostEqual(bc["van_eur"], 352652.24,
                               places=2)
        self.assertAlmostEqual(
            bc["be_prezzo_disp_eur_mw_anno"], 5557.89,
            places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh907_calcola(**_demo_kwargs(penalita_eur_mwh=0.0))
        self.assertEqual(bc["penalita_eur"], 0.0)
        self.assertEqual(bc["margine_eur_anno"], 107300.0)
        self.assertAlmostEqual(bc["van_eur"], 314552.85,
                               places=2)
        self.assertAlmostEqual(
            bc["be_prezzo_disp_eur_mw_anno"], 7410.53,
            places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_piattaforma_zero_e_costo_sito_zero(self):
        bc = mh907_calcola(
            **_demo_kwargs(costo_piattaforma_eur_anno=0.0))
        self.assertEqual(bc["costo_anno_eur"], 32800.0)
        self.assertEqual(bc["margine_eur_anno"], 163300.0)
        self.assertAlmostEqual(bc["van_eur"], 557003.54,
                               places=2)
        self.assertEqual(bc["payback_anni"], 1)
        self.assertIsNone(bc["be_prezzo_disp_eur_mw_anno"])
        self.assertIsNone(bc["be_prezzo_energia_eur_mwh"])
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh907_calcola(
            **_demo_kwargs(costo_sito_eur_anno=0.0))
        self.assertEqual(bc["costo_siti_eur_anno"], 12800.0)
        self.assertEqual(bc["costo_anno_eur"], 72800.0)
        self.assertEqual(bc["margine_eur_anno"], 123300.0)
        self.assertAlmostEqual(bc["van_eur"], 383824.47,
                               places=2)
        self.assertAlmostEqual(
            bc["be_prezzo_disp_eur_mw_anno"], 4042.11,
            places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_p_attivata_sopra_offerta_minimo(self):
        bc = mh907_calcola(**_demo_kwargs(p_attivata_mw=10.0))
        self.assertEqual(bc["p_attivata_eff_mw"], 5.0)
        self.assertEqual(bc["e_attivata_mwh"], 400.0)
        self.assertEqual(bc["ricavo_energia_eur_anno"], 72000.0)
        self.assertEqual(bc["margine_eur_anno"], 113500.0)
        self.assertAlmostEqual(bc["van_eur"], 341395.60,
                               places=2)
        self.assertAlmostEqual(bc["tir_frazione"], 0.7040,
                               places=4)
        self.assertEqual(bc["payback_anni"], 2)
        self.assertAlmostEqual(
            bc["be_prezzo_disp_eur_mw_anno"], 6105.26,
            places=2)
        self.assertEqual(bc["co2_t_anno"], 140.0)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_tasso_zero_e_dieci(self):
        bc = mh907_calcola(**_demo_kwargs(tasso_frazione=0.0))
        self.assertAlmostEqual(bc["van_eur"], 366500.0,
                               places=2)
        self.assertAlmostEqual(bc["tir_frazione"], 0.6285,
                               places=4)
        self.assertEqual(bc["verdetto"], "CONVIENTE")
        bc = mh907_calcola(**_demo_kwargs(tasso_frazione=0.10))
        self.assertAlmostEqual(bc["van_eur"], 241588.27,
                               places=2)
        self.assertAlmostEqual(bc["tir_frazione"], 0.6285,
                               places=4)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_tolleranza_zero_demo_resta_conveniente(self):
        # Con VAN positivo la tolleranza non
        # decide nulla: il demo resta CONVIENTE
        # anche a tolleranza zero.
        bc = mh907_calcola(**_demo_kwargs(tol_frazione=0.0))
        self.assertAlmostEqual(bc["van_eur"], 297234.94,
                               places=2)
        self.assertEqual(bc["verdetto"], "CONVIENTE")

    def test_van_invarianze(self):
        # Il VAN non dipende dal fattore CO2: la
        # CO2 non entra nell'economia.
        bc = demo_calcoli()
        bc_c = mh907_calcola(
            **_demo_kwargs(fattore_co2_t_mwh=0.0))
        self.assertEqual(bc_c["van_eur"], bc["van_eur"])
        self.assertEqual(bc_c["co2_t_anno"], 0.0)
        # Il VAN non dipende dalla tolleranza.
        bc_t = mh907_calcola(**_demo_kwargs(tol_frazione=0.0))
        self.assertEqual(bc_t["van_eur"], bc["van_eur"])

    def test_csv_contiene_voci(self):
        bc = demo_calcoli()
        csv = mh907_csv(bc, mh907_demo())
        for voce in ("p_offerta_mw",
                     "prezzo_disp_eur_mw_anno",
                     "disponibilita_frazione",
                     "n_attivazioni_anno",
                     "durata_attivazione_h",
                     "p_attivata_mw",
                     "prezzo_energia_eur_mwh",
                     "quota_fallimento_frazione",
                     "penalita_eur_mwh",
                     "costo_piattaforma_eur_anno",
                     "n_siti",
                     "costo_sito_eur_anno",
                     "compenso_siti_eur_mwh",
                     "capex_eur",
                     "tasso_frazione",
                     "durata_anni",
                     "tol_frazione",
                     "fattore_co2_t_mwh",
                     "p_attivata_eff_mw",
                     "e_attivata_mwh",
                     "ricavo_disp_eur_anno",
                     "ricavo_energia_eur_anno",
                     "e_mancata_mwh",
                     "penalita_eur",
                     "costo_siti_eur_anno",
                     "costo_anno_eur",
                     "margine_eur_anno",
                     "van_eur",
                     "tir_frazione",
                     "payback_anni",
                     "payback_fraz_anni",
                     "be_prezzo_disp_eur_mw_anno",
                     "be_prezzo_energia_eur_mwh",
                     "co2_t_anno",
                     "scenario_base_p_attivata_eff_mw",
                     "scenario_base_van_eur",
                     "scenario_base_verdetto",
                     "scenario_disp_piu30_van_eur",
                     "scenario_disp_piu30_verdetto",
                     "scenario_disp_meno30_van_eur",
                     "scenario_disp_meno30_verdetto",
                     "scenario_att_meno50_van_eur",
                     "scenario_att_meno50_verdetto",
                     "scenario_disp_080_van_eur",
                     "scenario_disp_080_verdetto",
                     "scenario_durata_3_van_eur",
                     "scenario_durata_3_verdetto",
                     "confronto_p_attivata_eff_mw",
                     "confronto_e_attivata_mwh",
                     "confronto_ricavo_disp_eur_anno",
                     "confronto_ricavo_energia_eur_anno",
                     "confronto_e_mancata_mwh",
                     "confronto_penalita_eur",
                     "confronto_costo_siti_eur_anno",
                     "confronto_costo_anno_eur",
                     "confronto_margine_eur_anno",
                     "confronto_van_eur",
                     "confronto_tir_frazione",
                     "confronto_payback_anni",
                     "confronto_be_prezzo_disp_eur_mw_anno",
                     "confronto_be_prezzo_energia_eur_mwh",
                     "confronto_co2_t_anno",
                     "verdetto"):
            self.assertIn(voce, csv)
        self.assertIn("CONVIENTE", csv)

    def test_csv_separatore_punto_virgola(self):
        bc = demo_calcoli()
        csv = mh907_csv(bc, mh907_demo())
        self.assertIn("voce;valore", csv.splitlines()[0])
        self.assertIn("p_offerta_mw;", csv)

    def test_demo_calcoli_alias_uguale(self):
        self.assertEqual(mh907_demo_calcoli()["van_eur"],
                         demo_calcoli()["van_eur"])
        self.assertEqual(mh907_demo_calcoli()["verdetto"],
                         demo_calcoli()["verdetto"])

    def test_df_scenari_confronto_tabella_flussi(self):
        bc = demo_calcoli()
        self.assertEqual(len(bc["df_scenari"]), 6)
        self.assertEqual(len(bc["df_confronto"]), 16)
        self.assertEqual(len(bc["df_tabella"]), 35)
        self.assertEqual(len(bc["df_flussi"]), 6)
        self.assertEqual(len(bc["df_ricavi_costi"]), 5)
        self.assertEqual(
            list(bc["df_confronto"]["Voce"]),
            ["Potenza attivata effettiva (MW)",
             "Energia attivata (MWh/anno)",
             "Ricavo disponibilita (EUR/anno)",
             "Ricavo energia (EUR/anno)",
             "Energia mancata (MWh/anno)",
             "Penalita (EUR/anno)",
             "Costo siti (EUR/anno)",
             "Costo anno (EUR/anno)",
             "Margine netto annuo (EUR/anno)",
             "VAN (EUR)",
             "TIR (frazione)",
             "Payback (anni)",
             "Breakeven prezzo disponibilita (EUR/MW/anno)",
             "Breakeven prezzo energia (EUR/MWh)",
             "CO2 evitata (t/anno)",
             "Verdetto"])
        self.assertAlmostEqual(
            bc["df_confronto"]["Valore"].iloc[0],
            4.00, places=2)
        self.assertAlmostEqual(
            bc["df_confronto"]["Valore"].iloc[9],
            297234.94, places=2)
        voci = set(bc["df_tabella"]["Voce"])
        self.assertIn("Potenza offerta (MW)", voci)
        self.assertIn("Prezzo disponibilita (EUR/MW/anno)", voci)
        self.assertIn("Energia attivata (MWh/anno)", voci)
        self.assertIn("Breakeven prezzo disponibilita (EUR/MW/anno)", voci)
        self.assertIn("Breakeven prezzo energia (EUR/MWh)", voci)
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
            297234.94, places=2)
        self.assertAlmostEqual(
            bc["df_scenari"]["TIR (%)"].iloc[0],
            62.85, places=2)
        self.assertEqual(
            list(bc["df_flussi"].columns),
            ["Anno", "Flusso (EUR)", "Cumulato (EUR)"])
        self.assertEqual(
            list(bc["df_ricavi_costi"].columns),
            ["Voce", "Valore"])

    def test_valida_rifiuta_stringhe_e_bool(self):
        kw = _demo_kwargs(p_offerta_mw="5.0")
        self.assertRaises(ValueError, mh907_calcola, **kw)
        kw = _demo_kwargs(p_offerta_mw=True)
        self.assertRaises(ValueError, mh907_calcola, **kw)
        val = mh907_valida(*[kw[k] for k in _ORDINE_VALIDA])
        self.assertFalse(val["valido"])


class TestDemoUiKeysRegression(unittest.TestCase):
    def test_ui_chiavi_def_subset_demo(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r'_def907\["([^"]+)"\]', src))
        self.assertTrue(lette <= set(mh907_demo().keys()), lette - set(mh907_demo().keys()))
        self.assertEqual(lette, set(mh907_demo().keys()))

    def test_ui_chiavi_bc_subset_calcola(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        lette = set(re.findall(r"_bc907\['([^']+)'\]", src))
        lette |= set(re.findall(r'_bc907\["([^"]+)"\]', src))
        attese = set(mh907_demo_calcoli().keys())
        self.assertTrue(lette <= attese, lette - attese)


class TestConteggioTitoliPreApply(unittest.TestCase):
    def test_conteggio_titoli_pre_apply(self):
        # Conteggio titoli: forma PRE-apply. Prima
        # dell'apply di questa scheda la copia di
        # lavoro del repo ha 906 blocchi scheda;
        # l'apply bumpa questo assert al conteggio
        # post apply 907.
        if os.path.exists(_APP_WD):
            src = open(_APP_WD, encoding="utf-8", errors="ignore").read()
            self.assertEqual(len(re.findall(r"with tab\d+:", src)), 907)
        else:
            self.skipTest("nessuna copia di lavoro del repo trovata")


class TestStrutturaUI(unittest.TestCase):
    def test_ui_apre_scheda_attesa_una_volta(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertEqual(src.count("with tab907:"), 1)
        self.assertTrue(src.startswith("    # W912"))

    def test_ui_tab907_count_form(self):
        src_ui = open(_UI_PATH, encoding="utf-8").read()
        src_h = open(_HELPERS_PATH, encoding="utf-8").read()
        self.assertEqual(src_ui.count("with tab907:"), 1)
        self.assertIn("def mh907_demo(", src_h)
        self.assertIn("def mh907_calcola(", src_h)
        self.assertIn("tab907", src_ui)

    def test_ui_titolo_atteso(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertIn("UVAM sul MSD di Terna: aggregare flessibilità e venderla a Terna paga?", src)
        self.assertIn("⚡🏛️ UVAM sul MSD di Terna: aggregare flessibilità e venderla a Terna paga?", src)
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
        chiavi = re.findall(r'key="(st907_[^"]+)"', src)
        self.assertTrue(all(k.startswith("st907_") for k in chiavi))
        self.assertEqual(len(chiavi), len(set(chiavi)))
        self.assertEqual(len(chiavi), 25)
        self.assertIn('key="st907_calcola"', src)
        self.assertIn('key="st907_csv"', src)
        self.assertIn('key="st907_csv_scenari"', src)

    def test_ui_guard_prima_output(self):
        src = open(_UI_PATH, encoding="utf-8").read()
        self.assertLess(src.index("_deg907"), src.index(".paiac("))
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
