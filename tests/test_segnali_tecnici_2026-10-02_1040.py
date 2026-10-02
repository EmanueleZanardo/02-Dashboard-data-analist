"""Standalone test for calcola_segnali_tecnici - tab151 (no streamlit)."""
import ast
import numpy as np
import pandas as pd

src = open("app.py", encoding="utf-8").read()
tree = ast.parse(src)
ns = {"pd": pd, "np": np}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name == "calcola_segnali_tecnici":
        exec(compile(ast.Module(body=[node], type_ignores=[]), "nuova_helper.py", "exec"), ns)
calcola_segnali_tecnici = ns["calcola_segnali_tecnici"]

fails = []
def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)

def flat_hours(n_days, price, start="2025-01-01", tz=None):
    idx = pd.date_range(start, periods=n_days * 24, freq="h", tz=tz)
    return pd.Series(np.full(n_days * 24, price), index=idx, name="p")

def trend_hours(n_days, start_price=100.0, step=0.5, start="2025-01-01"):
    idx = pd.date_range(start, periods=n_days * 24, freq="h")
    daily = start_price + step * np.arange(n_days)
    return pd.Series(np.repeat(daily, 24), index=idx, name="p")

def vshape_hours(n_days=70, drop_day=35, drop_price=50.0, start="2025-01-01"):
    idx = pd.date_range(start, periods=n_days * 24, freq="h")
    vals = np.full(n_days, 100.0)
    vals[drop_day] = drop_price
    return pd.Series(np.repeat(vals, 24), index=idx, name="p")

SMALL = dict(rsi_period=2, macd_fast=2, macd_slow=3, macd_signal=2,
             sma_breve=2, sma_lunga=3, bb_period=3, bb_mult=2.0, orizzonte_gg=1)

# --- 1. serie piatta: nessun segnale, indicatori neutri ---
r = calcola_segnali_tecnici(flat_hours(120, 100.0))
check("piatto: valido e nessun errore", r["valido"] and r["errore"] is None)
check("piatto: n_giorni == 120", r["n_giorni"] == 120)
check("piatto: giorni_richiesti == 50", r["giorni_richiesti"] == 50)
u = r["ultimo"]
check("piatto: rsi == 50.0", u["rsi"] == 50.0)
check("piatto: macd == 0.0 e hist == 0.0", u["macd"] == 0.0 and u["hist"] == 0.0)
check("piatto: bb_pos == 50.0", u["bb_pos_pct"] == 50.0)
check("piatto: sma_breve == sma_lunga == 100.0", u["sma_breve"] == 100.0 and u["sma_lunga"] == 100.0)
check("piatto: 0 segnali", r["n_segnali"] == 0 and len(r["segnali"]) == 0)
check("piatto: stance tutte 0", r["stance"] == {"sma": 0, "rsi": 0, "macd": 0, "bb": 0})
check("piatto: punteggio 0 e verdetto NEUTRO", r["punteggio"] == 0 and "NEUTRO" in r["verdetto"])
check("piatto: riepilogo 4 righe, 0 segnali",
      list(r["riepilogo"]["Indicatore"]) == ["Medie mobili", "MACD", "RSI", "Bollinger"]
      and (r["riepilogo"]["N. segnali"] == 0).all())
check("piatto: colonne segnali giuste",
      list(r["segnali"].columns) == ["Data", "Indicatore", "Segnale", "Prezzo (EUR/MWh)",
                                     "Esito orizzonte (%)", "Esito valido"])

# --- 2. trend rialzista: RSI ipercomprato, MACD positivo ---
r = calcola_segnali_tecnici(trend_hours(120, step=0.5))
u = r["ultimo"]
check("up: rsi > 70", u["rsi"] > 70)
check("up: stance rsi -1, sma +1",
      r["stance"]["rsi"] == -1 and r["stance"]["sma"] == 1)
check("up: bb_pos > 50", u["bb_pos_pct"] > 50)

def accel_hours(n_days, a, b0, start="2025-01-01"):
    idx = pd.date_range(start, periods=n_days * 24, freq="h")
    daily = b0 + a * np.arange(n_days) ** 2
    return pd.Series(np.repeat(daily, 24), index=idx, name="p")

# su un trend lineare l'istogramma MACD tende a 0: il segno si testa su trend accelerati
r = calcola_segnali_tecnici(accel_hours(120, 0.02, 100.0))
check("up accelerato: hist > 0", r["ultimo"]["hist"] > 0)
check("up accelerato: stance macd +1", r["stance"]["macd"] == 1)

# --- 3. trend ribassista: RSI ipervenduto ---
r = calcola_segnali_tecnici(trend_hours(120, step=-0.5))
check("down: rsi < 30", r["ultimo"]["rsi"] < 30)
check("down: stance rsi +1", r["stance"]["rsi"] == 1)
r = calcola_segnali_tecnici(accel_hours(120, -0.02, 400.0))
check("down accelerato: hist < 0", r["ultimo"]["hist"] < 0)
check("down accelerato: stance macd -1", r["stance"]["macd"] == -1)

# --- 4. RSI esatto su serie note (parametri piccoli) ---
def daily_hours(vals, start="2025-01-01"):
    idx = pd.date_range(start, periods=len(vals) * 24, freq="h")
    return pd.Series(np.repeat(np.asarray(vals, dtype=float), 24), index=idx)
r = calcola_segnali_tecnici(daily_hours([10, 11, 12, 13, 14, 15]), **SMALL)
check("rsi: tutti guadagni -> 100", r["ultimo"]["rsi"] == 100.0)
r = calcola_segnali_tecnici(daily_hours([15, 14, 13, 12, 11, 10]), **SMALL)
check("rsi: tutte perdite -> 0", r["ultimo"]["rsi"] == 0.0)
# serie alternata lunga (default rp=14): RSI di Wilder oscilla attorno a 50
alt = pd.Series(np.repeat(np.tile([100.0, 101.0], 30), 24),
                index=pd.date_range("2025-01-01", periods=60 * 24, freq="h"))
r = calcola_segnali_tecnici(alt)
check("rsi: alternata lunga ~ 50", abs(r["ultimo"]["rsi"] - 50.0) < 3.0)

# --- 5. V-shape: segnale Bollinger BUY con esito +100% ---
r = calcola_segnali_tecnici(vshape_hours())
seg = r["segnali"]
bb = seg[(seg["Indicatore"] == "Bollinger") & (seg["Segnale"] == "BUY")]
check("vshape: 1 segnale Bollinger BUY", len(bb) == 1)
check("vshape: esito Bollinger == +100.0",
      bool(bb["Esito valido"].iloc[0]) and bb["Esito orizzonte (%)"].iloc[0] == 100.0)
check("vshape: prezzo segnale == 50.0", bb["Prezzo (EUR/MWh)"].iloc[0] == 50.0)
rsi_s = seg[seg["Indicatore"] == "RSI"]
check("vshape: almeno 1 segnale RSI", len(rsi_s) >= 1)
check("vshape: hit_rate_tot in [0,100]", 0.0 <= r["hit_rate_tot"] <= 100.0)

# --- 6. orizzonte oltre la fine -> esito non valido ---
r = calcola_segnali_tecnici(vshape_hours(), orizzonte_gg=60)
bb = r["segnali"][(r["segnali"]["Indicatore"] == "Bollinger") & (r["segnali"]["Segnale"] == "BUY")]
check("orizzonte lungo: esito non valido",
      len(bb) == 1 and not bool(bb["Esito valido"].iloc[0])
      and pd.isna(bb["Esito orizzonte (%)"].iloc[0]))

# --- 7. prezzo <= 0 saltato nel backtest ---
r = calcola_segnali_tecnici(vshape_hours(drop_price=-10.0))
bb = r["segnali"][(r["segnali"]["Indicatore"] == "Bollinger") & (r["segnali"]["Segnale"] == "BUY")]
check("prezzo negativo: esito non valido",
      len(bb) == 1 and not bool(bb["Esito valido"].iloc[0]))

# --- 8. errori puliti ---
check("errore: serie vuota",
      calcola_segnali_tecnici(pd.Series([], dtype=float))["errore"] is not None)
check("errore: non-Series",
      calcola_segnali_tecnici([1.0, 2.0, 3.0])["errore"] is not None)
s_bad = pd.Series([1.0, 2.0, 3.0], index=[0, 1, 2])
check("errore: indice non-datetime",
      calcola_segnali_tecnici(s_bad)["errore"] is not None)
r = calcola_segnali_tecnici(flat_hours(30, 100.0))
check("errore: serie troppo corta (30gg < 50)", r["errore"] is not None and "50" in r["errore"])
check("errore: rsi_period=1", calcola_segnali_tecnici(flat_hours(120, 100.0), rsi_period=1)["errore"] is not None)
check("errore: sma_breve >= sma_lunga",
      calcola_segnali_tecnici(flat_hours(120, 100.0), sma_breve=50, sma_lunga=20)["errore"] is not None)
check("errore: macd_fast >= macd_slow",
      calcola_segnali_tecnici(flat_hours(120, 100.0), macd_fast=26, macd_slow=12)["errore"] is not None)
check("errore: bb_mult fuori range",
      calcola_segnali_tecnici(flat_hours(120, 100.0), bb_mult=0.1)["errore"] is not None)
check("errore: orizzonte 0",
      calcola_segnali_tecnici(flat_hours(120, 100.0), orizzonte_gg=0)["errore"] is not None)
check("errore: param non numerico",
      calcola_segnali_tecnici(flat_hours(120, 100.0), rsi_period="x")["errore"] is not None)

# --- 9. determinismo ---
a = calcola_segnali_tecnici(vshape_hours())
b = calcola_segnali_tecnici(vshape_hours())
check("determinismo: segnali uguali", a["segnali"].equals(b["segnali"]))
check("determinismo: ultimo uguale", a["ultimo"] == b["ultimo"])

# --- 10. tz-aware e NaN ---
r = calcola_segnali_tecnici(flat_hours(70, 100.0, tz="Europe/Zurich"))
check("tz-aware: valido, 70 giorni", r["valido"] and r["n_giorni"] == 70)
s = vshape_hours()
s.iloc[100:110] = np.nan
r = calcola_segnali_tecnici(s)
check("NaN: tollerati", r["valido"] and r["n_giorni"] == 70)

# --- 11. registry: dichiarazione, UI, chiavi widget ---
appsrc = open("app.py", encoding="utf-8").read()
check("registry: tab151 dichiarata", "tab151 = st.tabs(" in appsrc)
check("registry: titolo presente", '"📈 Segnali tecnici"' in appsrc)
check("registry: blocco UI presente", "    with tab151:" in appsrc)
check("registry: helper chiamato nella UI",
      "calcola_segnali_tecnici(prezzi" in appsrc)
import re as _re
keys = _re.findall(r'key="(sg151_[a-z_]+)"', appsrc)
check("registry: chiavi widget uniche", len(keys) == len(set(keys)) and len(keys) >= 9)

print()
if fails:
    print("FAILURES:", len(fails))
    raise SystemExit(1)
print("TUTTI I CHECK VERDI")
