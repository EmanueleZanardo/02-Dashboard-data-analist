# Singularity Quant ETRM — Dashboard Energy Analyst

Dashboard Streamlit per analisi quantitativa del mercato elettrico svizzero
(Swissix) ed europeo: price analytics, spark spread, hedging, risk, scenari.

## Avvio locale

```bash
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml  # poi compila i valori
streamlit run app.py
```

Il terminale chiede la password (`APP_PASSWORD` dai secrets): nessun default
nel codice, per disegno.

## Dati reali vs dati sintetici

- **Dati reali**: workspace "Dati reali svizzeri (ENTSO-E)" e, nel workspace
  "Price Analytics (Swissix)", la sorgente **"ENTSO-E live"**. Richiedono
  `ENTSOE_API_KEY` nei secrets (chiave gratuita da
  https://transparency.entsoe.eu).
- **Dati sintetici**: tutto il resto mostra un banner giallo
  **"DEMO — dati sintetici"**. I numeri finti non devono mai sembrare reali:
  è anche una questione di credibilità del portfolio.

## Sicurezza / segreti

- Mai committare `.streamlit/secrets.toml` (è nel `.gitignore`).
- La vecchia chiave ENTSO-E finita nella storia git va **ruotata manualmente**
  da Emanuele su transparency.entsoe.eu (revoca + nuova chiave), poi
  aggiornata nei secrets del deploy. Gli agenti non toccano le chiavi.
- Nessun segreto hardcoded nel codice: le chiavi arrivano solo da
  `st.secrets`.

## Embed nel sito portfolio

`singularity/src/app/singularity/page.tsx` incorpora la dashboard via iframe.
L'URL non è più hardcoded: si imposta con la variabile d'ambiente
`NEXT_PUBLIC_STREAMLIT_URL` (fallback all'URL attuale).

## Test

```bash
python3 tests/test_helpers.py   # N check, 0 fail attesi
```

I test estraggono le funzioni pure `calcola_*` / `profilo_*` / `shock_*` da
`app.py` via AST e le eseguono senza avviare Streamlit.

## Struttura

- `app.py` — tutta la dashboard (8 workspace; lo Swissix ha 106 tab)
- `requirements.txt` — dipendenze pinnate
- `tests/` — test delle funzioni di calcolo
- `singularity/` — pagina Next.js di embed (portfolio)
