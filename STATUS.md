# STATUS.md — 02-Dashboard-data-analist (Singularity Quant ETRM)

**Ultimo aggiornamento: 01/10/2026 00:40 CEST**

## Stato
- Dashboard Streamlit "Singularity Quant ETRM", live su https://czpox8o8x6arnxw96txnvt.streamlit.app/.
- Ultimi commit: b373666 (test tab114), 25417e1 (README 113->114), ab2bbf0 (tab114 Stoccaggio estrinseco MC + LP sparsa).
- Test: 47/47 verdi (tests/test_helpers.py) + 30/30 nuovi check tab115; regressione: 19/19.

## Ultimi eventi verificati (01/10/2026)
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
