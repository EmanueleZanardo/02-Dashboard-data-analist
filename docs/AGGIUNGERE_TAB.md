# Come aggiungere una tab (workspace Price Analytics — Swissix)

Convenzione attuale (verificata il 04/10/2026 su `app.py`): le tab dello
Swissix sono **211**, dichiarate in un'unica chiamata `st.tabs()`.

## 1. Funzione di calcolo pura — `calcola_*`

Tutto il calcolo va in una **funzione pura di livello modulo**, senza
chiamate a Streamlit nel corpo. Convenzione:

- nome `calcola_<cosa>` (o `profilo_<cosa>` / `genera_<cosa>` per i derivati);
- input: Series/DataFrame pandas, parametri scalari; mai `st.*`;
- output: `dict` con chiavi `"ok"`/`"valido"`/`"errore"` + strutture
  (DataFrame/Series/scalari) — così la tab mostra un messaggio invece di
  crashare su input strani;
- NaN-safe: serie vuota / non numerica / troppo corta → strutture vuote,
  **mai eccezioni**;
- `@st.cache_data` è consentito solo sul decoratore (la funzione resta
  testabile senza Streamlit).

Esempi: `calcola_volatilita_intraday`, `calcola_regimi_prezzo`,
`calcola_riepilogo_periodo` (definiti prima della sezione workspace).

## 2. Dichiarazione della tab

In `app.py`, riga della dichiarazione (~riga 16241):

```python
tab1, tab2, ..., tab134, tab135 = st.tabs([
    "⏱️ Profilo giornaliero", ..., "📑 Report di periodo",
    "🆕 Nome nuova tab"])
```

- Aggiungi **sia** la variabile `tab135` **sia** il titolo nella lista,
  in coda, nello stesso ordine.
- Il titolo ha un'emoji + nome breve; resta sotto i ~25 caratteri.

## 3. Blocco UI — `with tab135:`

I blocchi `with tabN:` sono dopo la dichiarazione (da ~riga 27425 in poi).
Schema standard di una tab:

```python
with tab135:
    st.markdown("<h1>🆕 Nome tab</h1>", unsafe_allow_html=True)
    st.caption("Cosa calcola, in una riga.")
    # input utente (number_input, slider, radio...) con key univoche
    ris = calcola_nuova_cosa(prezzi, param1, param2)
    if ris["errore"]:
        st.error(ris["errore"])
    elif not ris["valido"]:
        st.warning("Parametri non validi.")
    else:
        # KPI con st.columns + grafici plotly + tabella + download CSV
```

- Le `key=` dei widget devono essere univoche in tutta l'app.
- Grafici con plotly; export con `st.download_button` (CSV `;` come
  separatore, vedi `genera_csv_report`).

## 4. Test — `tests/test_<nome>.py`

Ogni tab nuova arriva con un file di test in stile pytest (non legacy):

```python
from appfuncs import load

_F = load("calcola_nuova_cosa")
calcola_nuova_cosa = _F["calcola_nuova_cosa"]

def test_piatta():
    ...
```

- `tests/appfuncs.py` estrae la funzione da `app.py` via AST: niente
  Streamlit da avviare, esecuzione in secondi.
- Casi da coprire: serie piatta (valori attesi esatti), serie vuota /
  troppo corta (strutture vuote, niente eccezioni), un caso con numeri
  calcolabili a mano, determinismo (due chiamate → stesso risultato).
- Convenzione nomi: `test_<area>.py` o `test_nuove_tab.py` per gruppi
  di tab recenti; classi `Test<NomeFunzione>`.

I file legacy `tests/test_*_<data>_<ora>.py` (script standalone con
`raise SystemExit`) sono il formato storico del ciclo QA: `pytest` li
ignora via `tests/conftest.py`, `tests/run_all.py` li esegue come
sottoprocessi. Per tab nuove preferire il formato pytest.

## 5. Checklist prima del push

1. `python3 -m pytest tests/ -q` — tutto verde.
2. La tab non rompe le altre: nessuna variabile globale nuova, nessuna
   `key=` duplicata.
3. Nessun segreto nel codice (chiavi solo da `st.secrets`).
4. Aggiornare il conteggio tab nel `README.md` ("134 tab" → "135 tab") e
   l'elenco nel `<details>`.
5. Push via Contents API (vedi regole in `~/AGENTS.md`): GET SHA → PUT →
   verifica su `commits/main`. Mai `git push` HTTPS. Prima della PUT,
   `git fetch` e confronto dello SHA blob remoto: un altro agente lavora
   su `app.py` in parallelo.
