# STATUS.md — 02-Dashboard-data-analist (Singularity Quant ETRM)

**Ultimo aggiornamento: 30/09/2026 sera CEST**

## Stato
- Dashboard Streamlit "Singularity Quant ETRM", live su https://czpox8o8x6arnxw96txnvt.streamlit.app/.
- Ultimi commit: 8a744d71 e 46371653.
- Test: 52/52 verdi; regressione: 19/19.

## Ultimi eventi verificati (30/09/2026)
- Nuova tab109 "Opzione americana": binomiale CRR, premio early-exercise, delta, convergenza a Black-76, export CSV.
- QA continuo orario attivo.

## Prossimi passi
- Nuove tab analitiche secondo roadmap delle dashboard.
- Mantenere la copertura test 52/52 + regressione a ogni modifica.

## Blocchi
- ATTENZIONE: una vecchia chiave ENTSO-E resta nella storia git del repo — va ruotata (il codice usa `st.secrets`, la chiave nel codice è stata rimossa nel commit a829e1d, ma la storia git la contiene ancora).
