# STATUS.md — 02-Dashboard-data-analist (Singularity Quant ETRM)

**Ultimo aggiornamento: 01/10/2026 04:50 CEST**

## Stato
- Dashboard Streamlit "Singularity Quant ETRM", live su https://czpox8o8x6arnxw96txnvt.streamlit.app/.
- Ultimo commit: cf523c1 (README tab119, 01/10 04:52 CEST).
- Test: 47/47 verdi (tests/test_helpers.py) + 48/48 check tab119; regressione: 19/19.

## Ultimi eventi verificati (01/10/2026)
- Nuova tab119 "📉 Margin call simulator": rischio di liquidità delle coperture forward — helper calcola_margin_call testato (48 check, 0 fail: 2 in sviluppo con fix del test, aritmetica nozionale 48000 e tolleranza arrotondamenti); walk-forward giornaliero su nozionale = MW×24h×fix×giorni, margine iniziale/manutenzione, chiamate che riportano l'equity al livello iniziale, costo di finanziamento del capitale immobilizzato; KPI MtM/call max/chiamate totali/giorni in call/margine max/costo finanziamento, grafico equity vs livelli margine, barre margin call, tabella + export CSV. Nessun bug, nessun segreto hardcoded.
- Nuova tab118 "🎯 Fixing advisor": segnale statistico per la decisione fissare-ora vs aspettare — helper calcola_fixing_advisor testato (37 check, 0 fail, dopo fix del ramo storia-piatta); punteggio 0-100 da percentile + trend normalizzato + volatilità + stagionalità, KPI, grafico prezzo vs media storica/recente, percentile rolling con soglie 40/60, stagionalità mensile + export CSV. Nessun bug, nessun segreto hardcoded.
- Nuova tab117 "🗓️ Calendario del costo": costo giornaliero di fornitura (prezzo spot × MW della fascia) in calendario — helper calcola_calendario_costo testato (37 check, 0 fail); KPI costo totale/medio giornaliero/σ giornaliera/giorno più caro/più economico/quota top-10% giorni, heatmap settimanale del costo, costo medio per giorno della settimana, tabella giornaliera + aggregazione mensile + export CSV. Nessun bug, nessun segreto hardcoded.
- QA 01:40 CEST: nessuna modifica al repo remoto da b96f2680; app.py compilava, nessun segreto hardcoded (chiavi solo via st.secrets).
- Nuova tab116 "📤 Il mio carico": caricamento CSV del profilo di carico reale dell'utente (auto-riconoscimento colonne, conversioni kW/kWh, ricampionamento sub-orario, normalizzazione tz) oppure profilo demo uffici; helper parse_csv_carico + calcola_analisi_carico_reale testati (45 check, 0 fail); KPI energia/picco/fattore di carico/costo a spot/prezzo medio/correlazione, curva di durata del carico, profilo orario, tabella + export CSV. Push in 4 commit (2e8e57d, b712344, e847ac1, b96f268), HEAD remoto verificato b96f268.
- Nuova tab115 "🧾 Comparatore tariffe": confronto di 6 strutture tariffarie (spot indicizzata, flat, F1/F2/F3, peak/off-peak, spot+spread, spot con cap) sullo stesso profilo di prelievo; helper calcola_confronto_tariffe testato (30 check, 0 fail); KPI migliore/risparmio vs peggiore, barre orizzontali, tabella + export CSV. Nessun bug, nessun segreto hardcoded.

## Ultimi eventi verificati (30/09/2026)
- Nuova tab114 "🛢️📈 Stoccaggio estrinseco": Monte Carlo sul valore dello stoccaggio gas (GBM mean-reverting, seed fisso, LP esatta per scenario), premio di flessibilità vs intrinseco, P10/P90, istogramma, export CSV. LP dello stoccaggio passata a matrici sparse (~4-5x più veloce, stesso ottimo 17.695 € verificato).
- Nuova tab109 "Opzione americana": binomiale CRR, premio early-exercise, delta, convergenza a Black-76, export CSV.
- QA continuo orario attivo.

## Prossimi passi
- Nuove tab analitiche secondo roadmap delle dashboard.
- Mantenere la copertura test (47/47 suite + check per-tab) a ogni modifica.

## Blocchi
- ATTENZIONE: una vecchia chiave ENTSO-E resta nella storia git del repo — va ruotata (il codice usa `st.secrets`, la chiave nel codice è stata rimossa nel commit a829e1d, ma la storia git la contiene ancora).
