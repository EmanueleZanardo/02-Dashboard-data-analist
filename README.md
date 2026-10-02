# Singularity Quant ETRM — Dashboard Energy Analyst

Dashboard Streamlit per analisi quantitativa del mercato elettrico svizzero
(Swissix) ed europeo: price analytics, spark spread, hedging, risk, scenari.

**Live:** https://czpox8o8x6arnxw96txnvt.streamlit.app/
(redeploy automatico dal branch `main`)

## Workspace

1. 🎛️ Simulatore Strategico (Classico)
2. 🌍 Dati Reali Svizzeri (ENTSO-E)
3. 🤖 Autonomous AI & MARL
4. 🌍 Climate & Grid Intel
5. 📈 Exotics & Structuring
6. 🏛️ Enterprise Risk & XVA
7. 📈 Metodo STAR & Ottimizzazione
8. 📊 Price Analytics (Swissix) — 165 tab analitiche

### Price Analytics (Swissix)

Analisi operativa del prezzo spot orario Swissix (CH): KPI, confronto tra
periodi, alert di soglia, curva di carico, heatmap oraria, fasce F1/F2/F3,
tabella dati filtrabile ed export CSV. Moduli avanzati: Monte Carlo
(ventaglio di prezzo, rischio quanto, VaR del costo), hedging (MtM,
frontiera di fissazione, fixing advisor, margin call, test efficacia
hedge), drawdown MtM, attribuzione P&L, LCOS batteria, CVA controparte,
garanzie d'origine, ricavi da riserva, costo in franchi, spark/dark spread,
opzioni energetiche (Black-76, spark spread, swing, tolling, asiatiche…),
stoccaggio gas, PPA, idroelettrico, power-to-heat.

<details>
<summary>Elenco completo delle 165 tab dello Swissix</summary>

1. ⏱️ Profilo giornaliero
2. 🔥 Heatmap oraria
3. ⚡ Fasce F1/F2/F3
4. 📋 Tabella dati
5. ⚠️ Rischio & Durata
6. 🔋 Arbitraggio Batteria
7. 📊 Base/Peak mensile
8. 💰 Costo fornitura
9. 📈 MtM hedging
10. 🔥 Spark spread
11. 📐 Shaping curva
12. 📅 Weekend
13. ☀️ Price capture
14. 📉 Volatilità
15. 🗓️ YoY
16. ⬇️ Prezzi negativi
17. ↕️ Spread intra-day
18. 📍 Picchi di prezzo
19. 📆 Settimana tipo
20. 📉 Curva durata
21. 🎯 Concentrazione costo
22. 🔄 Shifting carico
23. 🎯 Finestre di acquisto
24. 🗓️ Stagionalità
25. 💼 Budget tracker
26. 🎚️ Sensitività profilo
27. 🎲 VaR costo (MC)
28. 🔝 Top giorni di costo
29. 🎛️ Fasce ottimali
30. 📈 Autocorrelazione
31. 🧪 Stress test
32. 🔮 Forecast prezzo
33. ⚡ Rampe di prezzo
34. 🔁 Persistenza sopra soglia
35. 📆 Spread calendario
36. 🧩 Decomposizione
37. 📊 Sequenze
38. 💡 Valore flessibilità
39. 🕐 Top ore di costo
40. 🕯️ Candele OHLC
41. 📉 Crolli & recuperi
42. 🔄 Mean reversion
43. 📦 Strip forward
44. 🌡️ Climatologia prezzo
45. 🔀 Stabilità profilo
46. ⚖️ Fisso vs indicizzato
47. 🛡️ Cap & Floor
48. 🧾 Stima bolletta
49. 🧮 Margine fornitore
50. 🌉 Ponte budget
51. 🧬 Driver del costo
52. 🎯 Hedge ratio
53. 📏 Shape premium
54. 💸 Sbilanciamento
55. 🏭 Costo CO₂
56. 🛡️ Expected Shortfall
57. ⚡ Potenza di picco
58. 🏭 Costo per turno
59. 🧲 Concentrazione per fascia
60. ⏰ Ora di punta
61. 🧠 Efficienza profilo
62. 🪟 Finestra ottimale
63. 💹 Margine per impianto
64. 🔌 Picchi coincidenti
65. 🔗 Correlazione impianti
66. 🪜 Curva di merito
67. 🗓️ Giorni tipo
68. 📐 Struttura a termine
69. 🚨 Giorni critici
70. 🪜 Tranche di acquisto
71. 📊 Distribuzione prezzi
72. ⏳ Timing del costo
73. 🚨 Anomalie di prezzo
74. 🎯 Backtest ordini limite
75. 📜 Take-or-pay
76. 🔋 Sizing batteria
77. 🔔 Alert personalizzati
78. ☀️ Autoconsumo FV
79. ➕ Nuovo carico
80. ⛽ Fuel switching
81. 🔥⚡ Power-to-heat
82. 🗻 Valore idro
83. 🤝 PPA vs merchant
84. ⚡ Carico interrompibile
85. 🔌 Tolling agreement
86. 🔧 Fermo impianto
87. 📊 Profilo di carico
88. 🧪 Shock di scenario
89. 🪫 Degrado batteria
90. ⚫ Dark spread
91. 🏗️ LCOE vs prezzo
92. 🔧 Payback efficienza
93. 💰 Opzioni sul prezzo
94. 🔀 Opzione spark spread
95. 🔛 Dispatch ottimale
96. 🏭 Dispatch di portafoglio
97. 🌀 Opzione swing
98. 📊 Greche opzioni
99. 🌀 Opzione asiatica
100. 🎯 Strategie opzionarie
101. 🗓️ Opzione Bermudiana
102. 🛡️ Opzione barriera
103. 🔭 Opzione lookback
104. 🪆 Opzione composta
105. 🪙 Opzione digitale
106. 🧭 Opzione chooser
107. ⏳ Opzione forward start
108. 🌡️ Opzione quanto
109. 🗽 Opzione americana
110. 🟣 Opzione rainbow
111. 🔌 Ricarica EV ottimale
112. 🔀 Spread transfrontaliero
113. 🛢️ Stoccaggio gas
114. 🛢️📈 Stoccaggio estrinseco
115. 🧾 Comparatore tariffe
116. 📤 Il mio carico
117. 🗓️ Calendario del costo
118. 🎯 Fixing advisor
119. 📉 Margin call
120. 📈 Frontiera di fissazione
121. 🎰 Ventaglio di prezzo
122. ⚡ Rischio quanto
123. 🕰️ Lag di indicizzazione
124. 💱 Costo in franchi
125. 🌱 Garanzie d'origine
126. ⚡ Ricavi da riserva
127. 🛡️ CVA controparte
128. 🔋 LCOS batteria
129. 📊 Attribuzione P&L
130. 📉 Drawdown MtM
131. 🧪 Test efficacia hedge
132. 🕐 Volatilità intraday
133. 🔀 Regimi di prezzo
134. 📑 Report di periodo
135. 📏 Premio di rischio
136. 🎄 Effetto festività
137. 🎯 Radar prezzo obiettivo
138. 📝 Riconciliazione fattura
139. 🔍 Qualità dati
140. 🔗 Beta gas-power
141. 🌊 Volatilità a termine
142. 🚨 Indice di stress di mercato
143. 📊 Efficienza del fixing
144. ⏳ Baricentro del costo
145. ⚡ Energia reattiva
146. ⚡ Potenza impegnata
147. 🔄 Rollover coperture
148. 🔋 Peak shaving
149. 🌀 Esponente di Hurst
150. 🎯 Tornado sensibilità
151. 📈 Segnali tecnici
152. ⚠️ Rischio orario
153. 👥 Profili tipo
154. 🎯 Accuratezza forecast
155. 🌡️ Normalizzazione climatica
156. 📏 EnPI energetico
157. 🌍 Impronta CO₂
158. 📍 Event study
159. ☀️ Business case rinnovabile
160. 💧 Idrogeno verde
161. 📦 Rischio volume
162. 💰 Prezzo fisso equo
163. 🏭 Costo per sito
164. ⚡ Elasticità domanda
165. 📊 Fattore di carico
</details>

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
- Nessun segreto hardcoded nel codice: le chiavi arrivano solo da
  `st.secrets`.
- ⚠️ **Rotazione chiave ENTSO-E**: una vecchia chiave resta nella storia git
  del repo — va ruotata manualmente su transparency.entsoe.eu
  (revoca + nuova chiave) e aggiornata nei secrets del deploy. Gli agenti
  non toccano le chiavi e nessun valore di chiave va mai scritto in file,
  README o chat.

## Deploy su Streamlit Cloud

- Il deploy punta al branch `main` di questo repo: ogni push su `main`
  fa ripartire l'app in automatico (qualche minuto).
- I secrets di produzione si impostano nella dashboard di Streamlit Cloud
  (App → Settings → Secrets), **mai** in file committati:
  `ENTSOE_API_KEY` e `APP_PASSWORD`.
- Dopo aver ruotato una chiave, aggiornarla lì e riavviare l'app
  (Reboot app).

## Embed nel sito portfolio

`singularity/src/app/singularity/page.tsx` incorpora la dashboard via iframe.
L'URL non è più hardcoded: si imposta con la variabile d'ambiente
`NEXT_PUBLIC_STREAMLIT_URL` (fallback all'URL attuale).

## Test

```bash
python3 -m pytest tests/ -q        # test pytest-style (funzioni pure, senza Streamlit)
python3 tests/run_all.py           # TUTTA la suite: pytest-style + legacy standalone
python3 tests/test_helpers.py      # esempio di file legacy: N check, 0 fail attesi
```

- I file `tests/test_*.py` in stile pytest estraggono le funzioni pure
  `calcola_*` / `profilo_*` da `app.py` via AST (modulo `tests/appfuncs.py`)
  e le eseguono senza avviare Streamlit.
- I file legacy `tests/test_*_<data>_<ora>.py` e `tests/test_helpers.py`
  sono script standalone in stile QA (contano check/fail e terminano con
  `SystemExit`): `pytest` li ignora (vedi `tests/conftest.py`), `run_all.py`
  li esegue come sottoprocessi.
- Dettagli sul ciclo di QA in `docs/`.

## Struttura

- `app.py` — tutta la dashboard (funzioni pure `calcola_*`/`profilo_*` +
  8 workspace Streamlit; lo Swissix ha 152 tab)
- `requirements.txt` — dipendenze pinnate
- `tests/` — test delle funzioni di calcolo (`appfuncs.py`, `conftest.py`,
  `run_all.py`, file `test_*.py`)
- `docs/` — documentazione operativa (struttura progetto, come aggiungere
  una tab, ciclo QA)
- `.streamlit/secrets.toml.example` — template dei secrets (mai committare
  il file reale)
- `singularity/` — pagina Next.js di embed (portfolio)
