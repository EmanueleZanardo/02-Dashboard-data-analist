"""Standalone test for parse_csv_carico + calcola_analisi_carico_reale - tab116 (no streamlit)."""
import ast
import numpy as np
import pandas as pd

src = open("app.py", encoding="utf-8").read()
tree = ast.parse(src)
ns = {"pd": pd, "np": np}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in ("parse_csv_carico", "calcola_analisi_carico_reale"):
        exec(compile(ast.Module(body=[node], type_ignores=[]), "app.py", "exec"), ns)
parse_csv_carico = ns["parse_csv_carico"]
calcola_analisi_carico_reale = ns["calcola_analisi_carico_reale"]

fails = []
def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)

TZ = "Europe/Zurich"

# ---------- parse_csv_carico ----------
# 1. CSV base: timestamp,MW orari
csv1 = "timestamp,MW\n2026-09-28 00:00,1.0\n2026-09-28 01:00,2.0\n2026-09-28 02:00,3.0\n"
r = parse_csv_carico(csv1.encode("utf-8"))
check("base valido", r["valido"])
check("base 3 ore", r["righe_valide"] == 3)
check("base valori", list(r["carico"].values) == [1.0, 2.0, 3.0])
check("base tz Zurich", str(r["carico"].index.tz) == TZ)
check("base risoluzione 60", abs(r["risoluzione_min"] - 60.0) < 1e-9)

# 2. Punto e virgola + kW -> /1000
csv2 = "data;potenza_kw\n2026-09-28 00:00;1500\n2026-09-28 01:00;2500\n"
r2 = parse_csv_carico(csv2)
check("kw valido", r2["valido"])
check("kw /1000", abs(r2["carico"].iloc[0] - 1.5) < 1e-9 and abs(r2["carico"].iloc[1] - 2.5) < 1e-9)
check("kw unita", r2["unita_orig"] == "kW")

# 3. kWh orari -> MW identici
csv3 = "datetime,kwh\n2026-09-28 00:00,10\n2026-09-28 01:00,20\n"
r3 = parse_csv_carico(csv3)
check("kwh valido", r3["valido"])
check("kwh -> MW", abs(r3["carico"].iloc[0] - 10.0) < 1e-9)

# 4. Quartoraria -> ricampionata a ora (media)
rows = []
for h in range(24):
    for q in range(4):
        rows.append(f"2026-09-28 {h:02d}:{q*15:02d},4.0")
r4 = parse_csv_carico(("timestamp,MW\n" + "\n".join(rows) + "\n").encode())
check("15min valido", r4["valido"])
check("15min -> 24 ore", r4["righe_valide"] == 24)
check("15min media 4.0", abs(r4["carico"].iloc[0] - 4.0) < 1e-9)

# 5. Righe sporche: data invalida, potenza non numerica, duplicati, negativi
csv5 = ("timestamp,MW\n2026-09-28 00:00,1.0\nnonunadata,2.0\n2026-09-28 01:00,abc\n"
        "2026-09-28 00:00,9.0\n2026-09-28 02:00,-5.0\n")
r5 = parse_csv_carico(csv5)
check("sporco valido", r5["valido"])
check("sporco scartate=2", r5["righe_scartate"] == 2)
check("sporco duplicato: primo tenuto", abs(r5["carico"].iloc[0] - 1.0) < 1e-9)
check("sporco negativo azzerato", r5["negative_azzerate"] == 1 and abs(r5["carico"].iloc[-1] - 0.0) < 1e-9)

# 6. CSV invalido
check("vuoto invalido", not parse_csv_carico(b"")["valido"])
check("1 colonna invalido", not parse_csv_carico(b"a\n1\n2\n")["valido"])
check("no righe valide", not parse_csv_carico(b"timestamp,MW\nxx,yy\n")["valido"])

# 7. tz-aware -> convertito a Zurich
csv7 = "timestamp,MW\n2026-09-28 00:00+00:00,1.0\n2026-09-28 01:00+00:00,2.0\n"
r7 = parse_csv_carico(csv7)
check("tz convertito", r7["valido"] and str(r7["carico"].index.tz) == TZ)

# 8. Euristica kW su nome generico (valori > 500)
csv8 = "time,value\n2026-09-28 00:00,1200\n2026-09-28 01:00,800\n"
r8 = parse_csv_carico(csv8)
check("euristica kw", r8["valido"] and abs(r8["carico"].iloc[0] - 1.2) < 1e-9 and r8["nota_conversione"] != "")

# 9. Determinismo
ra = parse_csv_carico(csv1.encode())
rb = parse_csv_carico(csv1.encode())
check("deterministico", ra["carico"].equals(rb["carico"]))

# ---------- calcola_analisi_carico_reale ----------
idx = pd.date_range("2026-09-28", periods=3, freq="h", tz=TZ)
car = pd.Series([1.0, 2.0, 3.0], index=idx)
prz = pd.Series([10.0, 20.0, 30.0], index=idx)
a = calcola_analisi_carico_reale(car, prz)
check("analisi valido", a["valido"])
check("energia=6", abs(a["energia_mwh"] - 6.0) < 1e-9)
check("ore=3", a["ore"] == 3)
check("picco=3", abs(a["picco_mw"] - 3.0) < 1e-9)
check("minimo=1", abs(a["minimo_mw"] - 1.0) < 1e-9)
check("fattore carico 66.67", abs(a["fattore_carico_pct"] - 200/3) < 1e-9)
check("costo=140", abs(a["costo_spot_eur"] - 140.0) < 1e-9)
check("prezzo medio 23.33", abs(a["prezzo_medio_pagato"] - 140/6) < 1e-9)
check("correlazione=1", abs(a["correlazione"] - 1.0) < 1e-9)
check("ore sopra 90% = 1", a["ore_sopra_90pct"] == 1)
check("quota base 50%", abs(a["quota_base_pct"] - 50.0) < 1e-9)
check("top10 = 90/140", abs(a["quota_costo_top10_pct"] - 90/140*100) < 1e-9)
check("curva durata desc", list(a["curva_durata"]) == [3.0, 2.0, 1.0])
check("df 3 righe", len(a["df"]) == 3 and abs(a["df"]["Costo orario (EUR)"].sum() - 140.0) < 1e-9)

# 10. tz mismatch naive vs aware -> allineato
car_n = pd.Series([1.0, 2.0, 3.0], index=pd.date_range("2026-09-28", periods=3, freq="h"))
b = calcola_analisi_carico_reale(car_n, prz)
check("tz mismatch ok", b["valido"] and abs(b["energia_mwh"] - 6.0) < 1e-9)

# 11. nessuna ora in comune -> invalido
prz2 = pd.Series([10.0], index=pd.date_range("2026-10-01", periods=1, freq="h", tz=TZ))
check("no overlap invalido", not calcola_analisi_carico_reale(car, prz2)["valido"])

# 12. carico costante -> correlazione None
cc = pd.Series([2.0, 2.0, 2.0], index=idx)
d = calcola_analisi_carico_reale(cc, prz)
check("costante valido", d["valido"])
check("costante corr None", d["correlazione"] is None)
check("costante fc=100", abs(d["fattore_carico_pct"] - 100.0) < 1e-9)

# 13. energia zero / vuoto -> invalido
cz = pd.Series([0.0, 0.0], index=idx[:2])
check("zero invalido", not calcola_analisi_carico_reale(cz, prz)["valido"])
check("vuoto invalido", not calcola_analisi_carico_reale(pd.Series([], dtype=float), prz)["valido"])

# 14. NaN scartati
cn = pd.Series([1.0, float("nan"), 3.0], index=idx)
e = calcola_analisi_carico_reale(cn, prz)
check("nan scartati", e["valido"] and e["ore"] == 2 and abs(e["energia_mwh"] - 4.0) < 1e-9)

print("FAILURES:", fails if fails else "none")
raise SystemExit(1 if fails else 0)
