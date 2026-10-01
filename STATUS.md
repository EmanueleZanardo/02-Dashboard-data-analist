# STATUS.md — 02-Dashboard-data-analist (Singularity Quant ETRM)

**Ultimo aggiornamento: 01/10/2026 ~02:00 CEST**

## Stato
- Dashboard Streamlit "Singularity Quant ETRM", live su https://czpox8o8x6arnxw96txnvt.streamlit.app/.
- Ultimo commit: b96f2680 (test tab116, 01/10 01:51 CEST).
- Test: 47/47 verdi (tests/test_helpers.py) + 30/30 check tab115 + 45/45 check tab116; regressione: 19/19.

## Ultimi eventi verificati (01/10/2026)
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
