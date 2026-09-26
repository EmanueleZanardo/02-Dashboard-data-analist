import streamlit as st
import pandas as pd
import numpy as np
import calendar
import datetime
import time
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import norm, weibull_min
from plotly.subplots import make_subplots

# ==========================================
# 1. SETUP TERMINALE, CSS & EDU-TOOLTIPS
# ==========================================
st.set_page_config(page_title="Singularity Quant ETRM", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #030712; color: #F3F4F6; }
    h1, h2, h3 { font-family: 'JetBrains Mono', monospace; color: #60A5FA; }
    .metric-container { background: #111827; border: 1px solid #1F2937; border-top: 3px solid #3B82F6; padding: 15px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.5); }
    .metric-label { font-size: 11px; color: #9CA3AF; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;}
    .metric-val { font-size: 22px; color: #F9FAFB; font-family: 'JetBrains Mono', monospace; font-weight: bold; margin-top: 5px;}
    .chat-msg { background: #1F2937; padding: 10px; border-radius: 8px; margin-bottom: 10px; font-family: 'JetBrains Mono', monospace; font-size: 12px; border-left: 3px solid #10B981;}
    .stButton>button { width: 100%; font-family: 'JetBrains Mono', monospace; font-weight: bold; background: #1D4ED8; color: white; border: none; }
    .stButton>button:hover { background: #2563EB; }
    
    /* FIX: Impedisce al testo dei toggle (Edu Mode) di andare a capo */
    div[data-testid="stWidgetLabel"] p { white-space: nowrap; }
    
    /* TOOLTIP DIDATTICO CSS */
    .edu-tooltip { position: relative; display: inline-block; border-bottom: 1px dotted #3B82F6; cursor: help; color: #93C5FD; font-weight: 600;}
    .edu-tooltip .edu-tooltiptext { visibility: hidden; width: 280px; background-color: #1F2937; color: #F9FAFB; text-align: left; border-radius: 6px; padding: 12px; position: absolute; z-index: 999; bottom: 125%; left: 50%; margin-left: -140px; opacity: 0; transition: opacity 0.3s; font-size: 11px; box-shadow: 0px 10px 15px rgba(0,0,0,0.8); border: 1px solid #3B82F6; font-family: 'Inter', sans-serif; font-weight: normal;}
    .edu-tooltip:hover .edu-tooltiptext { visibility: visible; opacity: 1; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. MOTORE DI TRADUZIONE (i18n) & EDU HELPER
# ==========================================
if 'lang' not in st.session_state: st.session_state.lang = 'IT'
if 'edu_mode' not in st.session_state: st.session_state.edu_mode = True

T = {
    'IT': {
        'auth_title': 'Identificazione Biometrica / Hardware Key Richiesta',
        'auth_btn': 'Decripta Terminale',
        'ws1': '🎛️ Simulatore Strategico (Classico)',
        'ws2': '🌍 Dati Reali Svizzeri (ENTSO-E)',
        'ws3': '🤖 Autonomous AI & MARL',
        'ws4': '🌍 Climate & Grid Intel',
        'ws5': '📈 Exotics & Structuring',
        'ws6': '🏛️ Enterprise Risk & XVA',
        'ws7': '📈 Metodo STAR & Ottimizzazione',
        'ws8': '📊 Price Analytics (Swissix)',
        'prompt': 'Chiedi all\'AI',
        'market_params': '⚙️ Parametri di Mercato'
    },
    'EN': {
        'auth_title': 'Biometric Identification / Hardware Key Required',
        'auth_btn': 'Decrypt Terminal',
        'ws1': '🎛️ Strategic Simulator (Classic)',
        'ws2': '🌍 Swiss Real Data (ENTSO-E)',
        'ws3': '🤖 Autonomous AI & MARL',
        'ws4': '🌍 Climate & Grid Intel',
        'ws5': '📈 Exotics & Structuring',
        'ws6': '🏛️ Enterprise Risk & XVA',
        'ws7': '📈 STAR Method & Optimization',
        'ws8': '📊 Price Analytics (Swissix)',
        'prompt': 'Ask AI Copilot',
        'market_params': '⚙️ Market Parameters'
    },
    'FR': {
        'auth_title': 'Identification Biométrique / Clé Matérielle Requise',
        'auth_btn': 'Déchiffrer le Terminal',
        'ws1': '🎛️ Simulateur Stratégique (Classique)',
        'ws2': '🌍 Données Réelles Suisses (ENTSO-E)',
        'ws3': '🤖 IA Autonome & MARL',
        'ws4': '🌍 Climat & Réseau Intel',
        'ws5': '📈 Exotiques & Structuration',
        'ws6': '🏛️ Risque d\'Entreprise & XVA',
        'ws7': '📈 Méthode STAR & Optimisation',
        'ws8': '📊 Analyse des Prix (Swissix)',
        'prompt': 'Demander à l\'IA',
        'market_params': '⚙️ Paramètres du Marché'
    }
}

def _(key, default=None):
    return T.get(st.session_state.lang, {}).get(key, default or key)

def edu(term, explanation):
    if st.session_state.edu_mode:
        return f'<div class="edu-tooltip">{term}<span class="edu-tooltiptext"><b>💡 Lo Sapevi?</b><br><br>{explanation}</span></div>'
    return term

# ==========================================
# 3. AUTENTICAZIONE
# ==========================================
def get_app_password():
    """Password del terminale da st.secrets (APP_PASSWORD) — obbligatoria, MAI default nel codice."""
    try:
        return st.secrets.get("APP_PASSWORD", None)
    except Exception:
        return None

if 'authenticated' not in st.session_state: st.session_state.authenticated = False

if not st.session_state.authenticated:
    lang_sel = st.selectbox("🌐 Language / Lingua / Langue", ["IT", "EN", "FR"], index=["IT", "EN", "FR"].index(st.session_state.lang))
    if lang_sel != st.session_state.lang:
        st.session_state.lang = lang_sel
        st.rerun()
        
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        st.markdown("<h2 style='text-align: center; color: #3B82F6;'>💠 SINGULARITY OS</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>{_('auth_title')}</p>", unsafe_allow_html=True)
        pwd = st.text_input("Key (password del terminale)", type="password")
        app_pwd = get_app_password()
        if st.button(_('auth_btn')):
            if not app_pwd:
                st.error("⚠️ Terminale non configurato: imposta `APP_PASSWORD` in `.streamlit/secrets.toml`. Accesso disabilitato.")
            elif pwd == app_pwd:
                st.session_state.authenticated = True
                st.rerun()
            else: st.error("Access Denied.")
    st.stop()

# ==========================================
# 4. CORE DATA ENGINE & API ENTSO-E
# ==========================================
@st.cache_data(ttl=3600, show_spinner=False)
def scarica_dati_entsoe(api_key, start_date, end_date):
    from entsoe import EntsoePandasClient
    client = EntsoePandasClient(api_key=api_key)
    inizio_tz = pd.Timestamp(start_date, tz='Europe/Zurich')
    fine_tz = pd.Timestamp(end_date, tz='Europe/Zurich') + pd.Timedelta(days=1) - pd.Timedelta(hours=1)
    prezzi = client.query_day_ahead_prices('CH', start=inizio_tz, end=fine_tz)
    prezzi.name = "Prezzo Spot (€/MWh)"
    prezzi.index.name = "Data e Ora"
    return prezzi

# ---------- Helpers Price Analytics (ws8) ----------
def get_entsoe_key():
    """Chiave API ENTSO-E da st.secrets (mai hardcodata nel codice)."""
    try:
        return st.secrets.get("ENTSOE_API_KEY", None)
    except Exception:
        return None

@st.cache_data(ttl=1800, show_spinner=False)
def generate_mock_hourly(start_date, end_date):
    """Serie oraria sintetica ma realistica del prezzo Swissix (€/MWh):
    profilo giornaliero a doppia gobba, sconto weekend, trend e spike casuali (seed fisso)."""
    rng = np.random.default_rng(7)
    idx = pd.date_range(
        start=pd.Timestamp(start_date),
        end=pd.Timestamp(end_date) + pd.Timedelta(days=1) - pd.Timedelta(hours=1),
        freq="h", tz="Europe/Zurich",
    )
    ore = idx.hour.to_numpy()
    wd = idx.weekday.to_numpy()
    profilo_giornaliero = 25 * np.sin(2 * np.pi * (ore - 6) / 24) + 18 * np.sin(4 * np.pi * (ore - 9) / 24)
    sconto_weekend = np.where(wd < 5, 12.0, -18.0)
    trend = np.linspace(0, 15, len(idx))
    rumore = rng.normal(0, 9, len(idx))
    spike = np.where(rng.random(len(idx)) < 0.008, rng.uniform(60, 160, len(idx)), 0.0)
    prezzi = np.clip(95 + profilo_giornaliero + sconto_weekend + trend + rumore + spike, 5, None)
    s = pd.Series(prezzi, index=idx, name="Prezzo Spot (€/MWh)")
    s.index.name = "Data e Ora"
    return s

def fascia_oraria(ts):
    """Fasce orarie AEEGSI F1/F2/F3."""
    wd, h = ts.weekday(), ts.hour
    if wd == 6:
        return "F3"
    if wd == 5:
        return "F2" if 7 <= h < 23 else "F3"
    if 8 <= h < 19:
        return "F1"
    if (7 <= h < 8) or (19 <= h < 23):
        return "F2"
    return "F3"

def sposta_carico_f1_f3(prezzi, mw_f1, mw_f3, quota_pct):
    """Demand response: sposta una quota del carico F1 verso F3.
    quota_pct: % dell'energia F1 da spostare nelle ore fuori punta (0-100, clamped).
    Ritorna (mw_f1_nuovo, mw_f3_nuovo): l'energia totale resta invariata
    (i MWh tolti da F1 vengono ripartiti sulle ore F3).
    Se mancano ore F1 o F3 nel periodo, ritorna il profilo invariato."""
    q = max(0.0, min(100.0, float(quota_pct))) / 100.0
    fasce = prezzi.index.map(fascia_oraria)
    ore_f1 = int((fasce == "F1").sum())
    ore_f3 = int((fasce == "F3").sum())
    if q <= 0 or ore_f1 == 0 or ore_f3 == 0:
        return float(mw_f1), float(mw_f3)
    e_spostata = float(mw_f1) * q * ore_f1  # MWh spostati da F1 a F3
    return float(mw_f1) * (1 - q), float(mw_f3) + e_spostata / ore_f3

def calcola_base_peak_mensile(prezzi):
    """Analisi mensile Base/Peak/Offpeak (definizione standard EPEX: Peak = lun–ven 08:00–19:59).
    Ritorna un DataFrame con un rigo per mese: Mese, Base, Peak, Offpeak, Spread P-O, Spread %, Ore peak.
    Valori NaN-safe: mesi senza ore peak/offpeak riportano None nelle colonne derivate.
    Il raggruppamento mensile usa l'indice reso tz-naive per evitare il
    UserWarning 'Converting to PeriodArray/Index representation will drop timezone information'."""
    idx = prezzi.index
    mesi = (idx.tz_localize(None) if idx.tz is not None else idx).to_period("M")
    is_peak = (idx.weekday < 5) & (idx.hour >= 8) & (idx.hour < 20)
    df = pd.DataFrame({"prezzo": prezzi.values.astype(float), "peak": is_peak}, index=idx)
    righe = []
    for mese, grp in df.groupby(mesi):
        base = float(grp["prezzo"].mean())
        pk = grp.loc[grp["peak"], "prezzo"]
        op = grp.loc[~grp["peak"], "prezzo"]
        peak_mean = float(pk.mean()) if len(pk) else float("nan")
        off_mean = float(op.mean()) if len(op) else float("nan")
        spread = peak_mean - off_mean
        righe.append({
            "Mese": str(mese),
            "Base (€/MWh)": round(base, 2),
            "Peak (€/MWh)": None if np.isnan(peak_mean) else round(peak_mean, 2),
            "Offpeak (€/MWh)": None if np.isnan(off_mean) else round(off_mean, 2),
            "Spread P-O (€/MWh)": None if np.isnan(spread) else round(spread, 2),
            "Spread %": (None if (np.isnan(spread) or off_mean == 0)
                         else round(spread / off_mean * 100, 1)),
            "Ore peak": int(len(pk)),
        })
    return pd.DataFrame(righe)

def calcola_costo_fornitura(prezzi, mw_f1, mw_f2, mw_f3):
    """Costo di una fornitura con potenza costante per fascia oraria F1/F2/F3 (AEEGSI).
    prezzi: Series oraria in €/MWh. mw_f1/2/3: potenza prelevata (MW) nelle ore di ciascuna fascia.
    Costo orario = prezzo_spot * potenza_fascia. Ritorna un dict con:
      'totale' = costo totale (€), 'mwh' = energia totale prelevata (MWh),
      'ponderato' = prezzo medio ponderato (€/MWh, NaN se mwh == 0),
      'per_fascia' = DataFrame con Ore, MWh, Costo (€), Prezzo medio (€/MWh) per fascia."""
    profilo = {"F1": float(mw_f1), "F2": float(mw_f2), "F3": float(mw_f3)}
    df = pd.DataFrame({"prezzo": prezzi.values.astype(float), "fascia": prezzi.index.map(fascia_oraria)})
    df["mw"] = df["fascia"].map(profilo)
    df["costo"] = df["prezzo"] * df["mw"]
    per_fascia = (df.groupby("fascia")
                    .agg(ore=("costo", "size"), mwh=("mw", "sum"),
                         costo=("costo", "sum"), prezzo_medio=("prezzo", "mean"))
                    .reindex(["F1", "F2", "F3"]))
    # FIX: fascia senza ore -> ore/mwh/costo = 0 ma prezzo_medio resta NaN
    # (fillna(0) su tutto mostrava un falso "0.00 €/MWh" come prezzo medio)
    per_fascia = per_fascia.fillna({"ore": 0, "mwh": 0.0, "costo": 0.0})
    totale = float(df["costo"].sum())
    mwh = float(df["mw"].sum())
    ponderato = totale / mwh if mwh > 0 else float("nan")
    return {"totale": totale, "mwh": mwh, "ponderato": ponderato, "per_fascia": per_fascia}

def calcola_mtm(prezzi, contratti):
    """Mark-to-market di contratti forward a prezzo fisso contro lo spot realizzato del periodo.
    prezzi: Series oraria in €/MWh (indice tz-aware).
    contratti: lista di dict con chiavi: nome (str), lato ('Vendita'/'Acquisto'),
      prezzo_fisso (float, €/MWh), mw (float), inizio (date), fine (date, inclusa).
    Convenzione desk: VENDITA (short) guadagna se spot < prezzo fisso;
      ACQUISTO (long) guadagna se spot > prezzo fisso.
    MtM = segno * (prezzo_fisso - prezzo_medio_realizzato) * mw * ore_delivery.
    I contratti con delivery fuori dal periodo dati (o volume 0) riportano
    0 ore e MtM 0, senza errori.
    Ritorna (df_dettaglio, cumul_mtm): il DataFrame ha un rigo per contratto
    (Nome, Lato, Prezzo fisso, Volume, Ore delivery, Prezzo medio realizzato, MtM);
    cumul_mtm è la Series del MtM cumulato orario sommato su tutti i contratti."""
    idx = prezzi.index
    v = prezzi.values.astype(float)
    righe = []
    mtm_orario_tot = np.zeros(len(v))
    for c in contratti or []:
        nome = str(c.get("nome") or "Contratto")
        lato = "Vendita" if str(c.get("lato")) != "Acquisto" else "Acquisto"
        segno = 1.0 if lato == "Vendita" else -1.0
        mw = max(0.0, float(c.get("mw", 0) or 0))
        fisso = float(c.get("prezzo_fisso", 0) or 0)
        di, df_ = c.get("inizio"), c.get("fine")
        if di is None or df_ is None:
            mask = np.zeros(len(v), dtype=bool)
        else:
            t0 = pd.Timestamp(di)
            t1 = pd.Timestamp(df_) + pd.Timedelta(days=1) - pd.Timedelta(hours=1)
            if idx.tz is not None:
                t0, t1 = t0.tz_localize(idx.tz), t1.tz_localize(idx.tz)
            mask = (idx >= t0) & (idx <= t1)
        ore = int(np.asarray(mask).sum())
        if ore == 0 or mw == 0:
            righe.append({"Nome": nome, "Lato": lato,
                          "Prezzo fisso (€/MWh)": round(fisso, 2),
                          "Volume (MW)": mw, "Ore delivery": 0,
                          "Prezzo medio realizzato (€/MWh)": None,
                          "MtM (€)": 0.0})
            continue
        realizzato = float(v[np.asarray(mask)].mean())
        mtm = segno * (fisso - realizzato) * mw * ore
        mtm_orario_tot += np.where(np.asarray(mask), segno * (fisso - v) * mw, 0.0)
        righe.append({"Nome": nome, "Lato": lato,
                      "Prezzo fisso (€/MWh)": round(fisso, 2),
                      "Volume (MW)": mw, "Ore delivery": ore,
                      "Prezzo medio realizzato (€/MWh)": round(realizzato, 2),
                      "MtM (€)": round(mtm, 2)})
    df = pd.DataFrame(righe, columns=["Nome", "Lato", "Prezzo fisso (€/MWh)", "Volume (MW)",
                                      "Ore delivery", "Prezzo medio realizzato (€/MWh)", "MtM (€)"])
    cumul = pd.Series(np.cumsum(mtm_orario_tot), index=idx, name="MtM cumulato (€)")
    return df, cumul

def calcola_spark_spread(prezzi, gas_eur_mwh, eff_pct, co2_eur_t, ef_tco2_mwh=0.4):
    """Clean spark spread orario di una centrale a gas contro lo spot elettrico.
    prezzi: Series oraria in €/MWh (indice tz-aware). gas_eur_mwh: prezzo gas €/MWh termico.
    eff_pct: efficienza elettrica della centrale (%). co2_eur_t: prezzo CO2 €/t.
    ef_tco2_mwh: fattore di emissione tCO2 per MWh elettrico prodotto (default 0.4, CCGT).
    Spark spread = prezzo_elettrico - gas/efficienza - co2*ef.
    Positivo = la centrale gira in utile; negativo = meglio comprare sul mercato.
    Ritorna (serie_oraria, stats): la Series è in €/MWh; stats è un dict con
    medio, pct_ore_positive, best_ora, worst_ora, ore_totali (NaN-safe)."""
    eff = max(1.0, float(eff_pct)) / 100.0
    v = prezzi.values.astype(float)
    costo_gas = float(gas_eur_mwh) / eff
    costo_co2 = float(co2_eur_t) * float(ef_tco2_mwh)
    ss = pd.Series(v - costo_gas - costo_co2, index=prezzi.index, name="Spark spread (€/MWh)")
    validi = ss.dropna()
    stats = {
        "medio": float(validi.mean()) if len(validi) else float("nan"),
        "pct_ore_positive": float((validi > 0).mean() * 100) if len(validi) else 0.0,
        "best_ora": validi.idxmax() if len(validi) else None,
        "best_val": float(validi.max()) if len(validi) else float("nan"),
        "worst_ora": validi.idxmin() if len(validi) else None,
        "worst_val": float(validi.min()) if len(validi) else float("nan"),
        "ore_totali": int(len(validi)),
    }
    return ss, stats

def calcola_shape_fattori(prezzi):
    """Fattori di shape stagionale dallo spot storico (per costruire curve forward 'shaped').
    Ritorna un dict:
      'mensile': Series(1..12) con fattore = media(mese)/media(totale)
      'orario': DataFrame(1..12 x 0..23) con fattore = media(mese,ora)/media(mese)
      'media_storica': media globale dello spot (€/MWh)
    I mesi senza dati riportano NaN (il chiamante usa fallback 1.0, fattore neutro);
    su serie vuota ritorna fattori tutti-NaN senza errori."""
    v = prezzi.values.astype(float)
    idx = prezzi.index
    media = float(v.mean()) if len(v) else float("nan")
    fattori_m = pd.Series(index=range(1, 13), dtype=float)
    fattori_h = pd.DataFrame(index=range(1, 13), columns=range(24), dtype=float)
    if len(v) and not np.isnan(media) and media != 0:
        mese = idx.month.to_numpy()
        ora = idx.hour.to_numpy()
        df = pd.DataFrame({"prezzo": v, "mese": mese, "ora": ora})
        mm = df.groupby("mese")["prezzo"].mean()
        fattori_m.loc[mm.index] = (mm / media).values
        mh = df.groupby(["mese", "ora"])["prezzo"].mean().unstack("ora")
        for m in mh.index:
            if not np.isnan(mm.loc[m]) and mm.loc[m] != 0:
                fattori_h.loc[m, mh.columns] = (mh.loc[m] / mm.loc[m]).values
    return {"mensile": fattori_m, "orario": fattori_h, "media_storica": media}

def shaped_mensile(forward, fattori_mensili, ore_mese):
    """Prezzi forward mensili 'shaped': forward * fattore_m / media_ponderata(fattori, pesi=ore).
    La media dei prezzi shaped pesata per le ore di ciascun mese riproduce
    ESATTAMENTE il forward in input (renormalizzazione).
    Fattori NaN -> 1.0 (fallback neutro: mese senza storia = prezzo flat).
    forward: prezzo flat annuo (€/MWh); ore_mese: dict/Series mese(1..12) -> ore.
    Ritorna una Series indicizzata 1..12 in €/MWh."""
    f = fattori_mensili.reindex(range(1, 13)).astype(float).fillna(1.0)
    h = pd.Series(ore_mese, index=range(1, 13), dtype=float)
    w_avg = float((f * h).sum() / h.sum()) if h.sum() > 0 else 1.0
    if w_avg == 0:
        w_avg = 1.0
    return (float(forward) * f / w_avg).rename("Prezzo shaped (€/MWh)")

def calcola_spread_weekend(prezzi):
    """Analisi settimanale dello spread weekday (lun-ven) vs weekend (sab-dom).

    prezzi: Series oraria in €/MWh (indice tz-aware).
    Ritorna un DataFrame con un rigo per settimana (lunedi-domenica):
      Settimana (etichetta "dd/mm-dd/mm"), Inizio, Fine,
      Weekday (€/MWh) = media lun-ven, Weekend (€/MWh) = media sab-dom,
      Spread Wd-We (€/MWh) = weekday - weekend (positivo = sconto weekend),
      Spread % = spread / weekday * 100,
      Ore weekday, Ore weekend.
    Settimane con solo weekday o solo weekend (bordi del periodo) riportano
    None nelle colonne derivate; serie vuota -> DataFrame vuoto con le colonne giuste."""
    cols = ["Settimana", "Inizio", "Fine", "Weekday (€/MWh)", "Weekend (€/MWh)",
            "Spread Wd-We (€/MWh)", "Spread %", "Ore weekday", "Ore weekend"]
    v = prezzi.values.astype(float)
    idx = prezzi.index
    if len(v) == 0:
        return pd.DataFrame({c: [] for c in cols})
    wd = idx.weekday.to_numpy()
    is_we = wd >= 5
    date = idx.normalize()
    lunedi = date - pd.to_timedelta(date.weekday, unit="d")
    df = pd.DataFrame({"prezzo": v, "we": is_we}, index=idx)
    righe = []
    for lun, grp in df.groupby(lunedi):
        dom = lun + pd.Timedelta(days=6)
        wd_p = grp.loc[~grp["we"], "prezzo"]
        we_p = grp.loc[grp["we"], "prezzo"]
        wd_m = float(wd_p.mean()) if len(wd_p) else float("nan")
        we_m = float(we_p.mean()) if len(we_p) else float("nan")
        spread = wd_m - we_m
        righe.append({
            "Settimana": f"{lun.strftime('%d/%m')}-{dom.strftime('%d/%m')}",
            "Inizio": lun.date().isoformat(),
            "Fine": dom.date().isoformat(),
            "Weekday (€/MWh)": None if np.isnan(wd_m) else round(wd_m, 2),
            "Weekend (€/MWh)": None if np.isnan(we_m) else round(we_m, 2),
            "Spread Wd-We (€/MWh)": None if np.isnan(spread) else round(spread, 2),
            "Spread %": (None if (np.isnan(spread) or wd_m == 0)
                         else round(spread / wd_m * 100, 1)),
            "Ore weekday": int(len(wd_p)),
            "Ore weekend": int(len(we_p)),
        })
    return pd.DataFrame(righe, columns=cols)

def profilo_solare(prezzi, potenza_mw):
    """Profilo orario sintetico di generazione fotovoltaica (MW), deterministico.
    Curva a campana con picco a mezzogiorno solare; la durata del giorno varia
    per mese (min a dicembre, max a giugno), ore notturne = 0.
    potenza_mw: potenza di picco dell'impianto (MW, <=0 -> profilo nullo).
    Ritorna una Series (MW) indicizzata come `prezzi`."""
    idx = prezzi.index
    ore = idx.hour.to_numpy() + idx.minute.to_numpy() / 60.0
    mese = idx.month.to_numpy()
    # durata del giorno ~8.2h (dic) -> ~15.8h (giu)
    durata = 12.0 + 3.8 * np.sin(2 * np.pi * (mese - 3.2) / 12.0)
    alba, tramonto = 12.0 - durata / 2.0, 12.0 + durata / 2.0
    x = np.clip((ore - alba) / np.where(durata > 0, durata, 1.0), 0.0, 1.0)
    forma = np.sin(np.pi * x) ** 1.3
    forma = np.where((ore >= alba) & (ore <= tramonto), forma, 0.0)
    return pd.Series(max(0.0, float(potenza_mw)) * forma, index=idx, name="Generazione solare (MW)")

def calcola_price_capture(prezzi, gen_mw):
    """Price capture di un profilo di generazione contro lo spot orario.
    prezzi: Series oraria in €/MWh; gen_mw: Series oraria MW (indice allineabile).
    Prezzo catturato = Σ(prezzo_h × gen_h) / Σ(gen_h): il prezzo medio a cui
    l'impianto vende realmente; il Tasso di cattura = catturato / media base.
    Sconto cannibalizzazione = base - catturato (positivo = il profilo vale meno
    del base, tipico del solare che produce nelle ore diurne più economiche).
    NaN-safe: le ore con prezzo o generazione NaN vengono ignorate; energia
    nulla -> derivati None; serie vuota -> DataFrame mensile vuoto con le colonne giuste.
    Ritorna dict con base_medio, catturato, tasso_cattura, mwh, ricavo,
    sconto_can e per_mese (DataFrame: Mese, MWh, Ricavo (€), Catturato (€/MWh), Tasso %)."""
    cols = ["Mese", "MWh", "Ricavo (€)", "Catturato (€/MWh)", "Tasso %"]
    df = pd.DataFrame({"prezzo": prezzi.astype(float), "gen": gen_mw.astype(float)}).dropna()
    mwh = float(df["gen"].sum())
    base = float(df["prezzo"].mean()) if len(df) else float("nan")
    base_r = None if np.isnan(base) else round(base, 2)
    if mwh <= 0:
        return {"base_medio": base_r, "catturato": None, "tasso_cattura": None,
                "mwh": 0.0, "ricavo": 0.0, "sconto_can": None,
                "per_mese": pd.DataFrame({c: [] for c in cols})}
    ricavo = float((df["prezzo"] * df["gen"]).sum())
    catt = ricavo / mwh
    sconto = base - catt
    tasso = catt / base * 100 if base != 0 else float("nan")
    mesi = (df.index.tz_localize(None) if df.index.tz is not None else df.index).to_period("M")
    righe = []
    for mese, grp in df.groupby(mesi):
        gmwh = float(grp["gen"].sum())
        gric = float((grp["prezzo"] * grp["gen"]).sum())
        gcatt = gric / gmwh if gmwh > 0 else float("nan")
        gbase = float(grp["prezzo"].mean())
        righe.append({
            "Mese": str(mese),
            "MWh": round(gmwh, 1),
            "Ricavo (€)": round(gric, 2),
            "Catturato (€/MWh)": None if np.isnan(gcatt) else round(gcatt, 2),
            "Tasso %": (None if (np.isnan(gcatt) or gbase == 0)
                        else round(gcatt / gbase * 100, 1)),
        })
    return {"base_medio": base_r, "catturato": round(catt, 2),
            "tasso_cattura": None if np.isnan(tasso) else round(tasso, 1),
            "mwh": round(mwh, 1), "ricavo": round(ricavo, 2),
            "sconto_can": round(sconto, 2),
            "per_mese": pd.DataFrame(righe, columns=cols)}

# Impianti proxy: nome -> (costo marginale €/MWh, capacità MW, colore)
ASSETS = {
    "☀️ Solare Muttsee": (0.0, 50, "#eab308"),
    "💧 Idro Biasca": (5.0, 250, "#3b82f6"),
    "🏭 Gas WtE Giubiasco": (208.0, 100, "#ef4444"),
}

@st.cache_data(ttl=1800, show_spinner=False)
def generate_singularity_data():
    np.random.seed(42)
    days = 500
    dates = pd.date_range(end=datetime.date.today(), periods=days)
    base_drift = 0.0001
    prices = np.zeros(days); prices[0] = 50
    vol = np.zeros(days); vol[0] = 0.02
    for i in range(1, days):
        vol[i] = 0.02 + 0.8 * vol[i-1] + np.random.exponential(0.005) if np.random.rand() > 0.9 else 0.02 + 0.95 * vol[i-1]
        prices[i] = prices[i-1] * np.exp((base_drift - 0.5*vol[i]**2) + vol[i]*np.random.normal())
    df = pd.DataFrame({'Power_EUR': prices}, index=dates)
    df['Returns'] = df['Power_EUR'].pct_change().fillna(0)
    df['Gas_USD'] = 15 + df['Power_EUR']*0.15 + np.random.normal(0,1,days)
    df['EUR_USD'] = 1.05 + np.cumsum(np.random.normal(0, 0.001, days))
    df['CO2_EUA'] = 80 + np.cumsum(np.random.normal(0.02, 0.5, days))
    df['Wind_Speed_ms'] = weibull_min.rvs(2, loc=0, scale=8, size=days)
    df['Sentiment_NLP'] = np.clip(np.random.normal(0.1, 0.4, days), -1, 1)
    return df

df = generate_singularity_data()
ult = df.iloc[-1]

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Sistema Quantitativo Operativo. Come posso assisterti?"}]

# ==========================================
# 5. SIDEBAR & GLOBAL CONTROLS
# ==========================================
with st.sidebar:
    st.markdown("<h2>💠 SINGULARITY</h2>", unsafe_allow_html=True)
    
    col_l, col_e = st.columns([1, 1.5])
    with col_l:
        new_lang = st.selectbox("🌐 Lang", ["IT", "EN", "FR"], index=["IT", "EN", "FR"].index(st.session_state.lang))
        if new_lang != st.session_state.lang:
            st.session_state.lang = new_lang
            st.rerun()
    with col_e:
        st.session_state.edu_mode = st.toggle("🎓 Edu Mode", value=st.session_state.edu_mode, help="Attiva i tooltip esplicativi sui termini tecnici.")
    
    st.markdown("---")
    
    workspace = st.radio("🏢 WORKSPACES", [
        _('ws1'), _('ws2'), _('ws3'), _('ws4'), _('ws5'), _('ws6'), _('ws7'), _('ws8')
    ])
    
    st.markdown("---")
    st.markdown("### 💬 Copilot Quant LLM")
    for msg in st.session_state.messages:
        st.markdown(f"<div class='chat-msg'><b>{msg['role'].upper()}:</b> {msg['content']}</div>", unsafe_allow_html=True)
    
    if prompt := st.chat_input(_('prompt')):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": f"Elaborazione: '{prompt}'. Il modello indica delta-hedging."})
        st.rerun()

def render_kpi(title, value, col):
    col.markdown(f"<div class='metric-container'><div class='metric-label'>{title}</div><div class='metric-val'>{value}</div></div>", unsafe_allow_html=True)

# ==========================================
# WORKSPACE 1: SIMULATORE STRATEGICO
# ==========================================
if workspace == _('ws1'):
    st.markdown(f"<h1>{_('ws1')}</h1>", unsafe_allow_html=True)
    st.info("📌 **Nota Operativa:** Il grafico calcola i margini operativi lordi. Attiva o disattiva le centrali per sovrapporre le rette di profittabilità e confrontare i costi marginali (Punto di Break-Even).")

    chart_container = st.container()
    st.markdown("---")
    
    st.markdown(f"### 🎛️ Seleziona Livelli (Overlay Grafico)")
    t_col1, t_col2, t_col3, t_col4 = st.columns(4)
    show_gas = t_col1.toggle("🏭 Gas Naturale (CSS)", value=True)
    show_coal = t_col2.toggle("⛏️ Carbone (CDS)", value=True)
    show_hydro = t_col3.toggle("💧 Idroelettrica", value=False)
    show_solar = t_col4.toggle("☀️ Solare", value=False)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader(_('market_params'))
    
    param_cols = st.columns(4)
    with param_cols[0]:
        st.markdown("**Variabili Globali**")
        p_elec = st.number_input("Prezzo Energia Corrente (€/MWh)", min_value=0.0, max_value=400.0, value=100.0, step=1.0)
        
    costo_marginale_gas = 0
    if show_gas:
        with param_cols[1]:
            st.markdown("**Impostazioni Gas**")
            p_gas = st.number_input("Prezzo Gas (€/MWh)", value=40.0)
            p_co2_gas = st.number_input("Prezzo CO2 (€/tCO2)", value=80.0, key="co2_gas")
            eff_gas = st.number_input("Efficienza Gas (η)", value=0.50, step=0.01)
            costo_marginale_gas = (p_gas / eff_gas) + (p_co2_gas * 0.2 / eff_gas)

    costo_marginale_coal = 0
    if show_coal:
        with param_cols[2]:
            st.markdown("**Impostazioni Carbone**")
            p_coal = st.number_input("Prezzo Carbone (€/MWh)", value=20.0)
            p_co2_coal = st.number_input("Prezzo CO2 (€/tCO2)", value=80.0, key="co2_coal")
            eff_coal = st.number_input("Efficienza Carbone (η)", value=0.40, step=0.01)
            costo_marginale_coal = (p_coal / eff_coal) + (p_co2_coal * 0.34 / eff_coal)

    costo_marginale_hydro = 0
    if show_hydro:
        with param_cols[3]:
            st.markdown("**Impostazioni Idroelettrica**")
            costo_om_hydro = st.number_input("Costi O&M (€/MWh)", value=5.0)
            costo_marginale_hydro = costo_om_hydro
            
    costo_marginale_solar = 0 

    with chart_container:
        xmax = max(300.0, p_elec, costo_marginale_gas, costo_marginale_coal, costo_marginale_hydro) * 1.25
        prezzi_range = np.linspace(0, xmax, 150)
        fig_sim = go.Figure()
        
        fig_sim.add_hline(y=0, line_width=1, line_dash="solid", line_color="rgba(255,255,255,0.3)")
        colors = {"Gas": "#ef4444", "Coal": "#a8a29e", "Hydro": "#3b82f6", "Solar": "#eab308"}
        
        if show_gas:
            m_gas_arr = prezzi_range - costo_marginale_gas
            fig_sim.add_trace(go.Scatter(x=prezzi_range, y=m_gas_arr, mode='lines', name="Gas Naturale (CSS)", line=dict(color=colors["Gas"], width=3)))
            fig_sim.add_vline(x=costo_marginale_gas, line_dash="dot", line_color=colors["Gas"], annotation_text=f" BE Gas: {costo_marginale_gas:.1f} €", annotation_position="bottom right")
            
        if show_coal:
            m_coal_arr = prezzi_range - costo_marginale_coal
            fig_sim.add_trace(go.Scatter(x=prezzi_range, y=m_coal_arr, mode='lines', name="Carbone (CDS)", line=dict(color=colors["Coal"], width=3)))
            fig_sim.add_vline(x=costo_marginale_coal, line_dash="dot", line_color=colors["Coal"], annotation_text=f" BE Coal: {costo_marginale_coal:.1f} €", annotation_position="top right")

        if show_hydro:
            m_hydro_arr = prezzi_range - costo_marginale_hydro
            fig_sim.add_trace(go.Scatter(x=prezzi_range, y=m_hydro_arr, mode='lines', name="Idroelettrica", line=dict(color=colors["Hydro"], width=3)))
            fig_sim.add_vline(x=costo_marginale_hydro, line_dash="dot", line_color=colors["Hydro"], annotation_text=f" BE Idro: {costo_marginale_hydro:.1f} €", annotation_position="bottom right")

        if show_solar:
            m_solar_arr = prezzi_range - costo_marginale_solar
            fig_sim.add_trace(go.Scatter(x=prezzi_range, y=m_solar_arr, mode='lines', name="Solare", line=dict(color=colors["Solar"], width=3)))
            fig_sim.add_vline(x=costo_marginale_solar, line_dash="dot", line_color=colors["Solar"], annotation_text=" BE Solare: 0 €", annotation_position="top right")

        fig_sim.update_layout(
            title="Confronto Margini Operativi (Merit Order Simulation)",
            xaxis_title="Prezzo Elettricità (€/MWh)",
            yaxis_title="Margine (€/MWh)",
            template="plotly_dark",
            height=450,
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_sim, use_container_width=True)

    st.markdown("---")
    
    calc_cols = st.columns(2)
    with calc_cols[0]:
        st.markdown("### Modelli Matematici e Formule")
        if show_gas:
            st.markdown(f"**{edu('Clean Spark Spread (CSS)', 'Indica il profitto teorico di una centrale a gas dopo aver pagato il gas e i permessi per inquinare (CO2).')}**")
            st.markdown("$$CSS = P_{elec} - \\frac{P_{gas}}{\\eta} - \\frac{P_{CO_2} \\cdot E_f}{\\eta}$$")
        if show_coal:
            st.markdown(f"**{edu('Clean Dark Spread (CDS)', 'Il profitto teorico di una centrale a CARBONE. A causa del fattore di emissione elevato (0.34 contra 0.2 del gas), è molto sensibile ai prezzi della CO2.')}**")
            st.markdown("$$CDS = P_{elec} - \\frac{P_{coal}}{\\eta} - \\frac{P_{CO_2} \\cdot E_f}{\\eta}$$")
        if show_hydro:
            st.markdown(f"**{edu('Dispatching Idroelettrico', 'Si decide di far cadere l\'acqua dai bacini solo quando il prezzo di mercato copre l\'usura meccanica delle turbine (O&M)')}**")
            st.markdown("$$Margine = P_{elec} - O\\&M_{var}$$")
        if show_solar:
            st.markdown(f"**{edu('Merit Order (Rinnovabili)', 'Il solare ha un costo marginale (MC) pari a ZERO. Il sole è gratis.')}**")
            st.markdown("$$Margine = P_{elec}$$")

    with calc_cols[1]:
        st.markdown(f"### Analisi di Profitto Istantaneo")
        st.markdown(f"*Calcolato al Prezzo Corrente inserito: **{p_elec} €/MWh***")
        
        res_cols = st.columns(2)
        idx = 0
        
        if show_gas:
            margine = p_elec - costo_marginale_gas
            col_target = res_cols[idx % 2]
            color = "#10B981" if margine > 0 else "#EF4444"
            status = "🟢 ON (In-the-Money)" if margine > 0 else "🔴 OFF (Out-of-Money)"
            col_target.markdown(f"<div style='background:#1F2937; padding:10px; border-radius:8px; margin-bottom:10px; border-left:4px solid {color};'><b>Gas Naturale</b><br><span style='font-size:20px; font-weight:bold; color:{color};'>€ {margine:.2f}</span><br><span style='font-size:12px;'>AI Status: {status}</span></div>", unsafe_allow_html=True)
            idx += 1
            
        if show_coal:
            margine = p_elec - costo_marginale_coal
            col_target = res_cols[idx % 2]
            color = "#10B981" if margine > 0 else "#EF4444"
            status = "🟢 ON (In-the-Money)" if margine > 0 else "🔴 OFF (Out-of-Money)"
            col_target.markdown(f"<div style='background:#1F2937; padding:10px; border-radius:8px; margin-bottom:10px; border-left:4px solid {color};'><b>Carbone</b><br><span style='font-size:20px; font-weight:bold; color:{color};'>€ {margine:.2f}</span><br><span style='font-size:12px;'>AI Status: {status}</span></div>", unsafe_allow_html=True)
            idx += 1
            
        if show_hydro:
            margine = p_elec - costo_marginale_hydro
            col_target = res_cols[idx % 2]
            color = "#10B981" if margine > 0 else "#EF4444"
            status = "🟢 ON (In-the-Money)" if margine > 0 else "🔴 OFF (Out-of-Money)"
            col_target.markdown(f"<div style='background:#1F2937; padding:10px; border-radius:8px; margin-bottom:10px; border-left:4px solid {color};'><b>Idroelettrica</b><br><span style='font-size:20px; font-weight:bold; color:{color};'>€ {margine:.2f}</span><br><span style='font-size:12px;'>AI Status: {status}</span></div>", unsafe_allow_html=True)
            idx += 1
            
        if show_solar:
            margine = p_elec - costo_marginale_solar
            col_target = res_cols[idx % 2]
            color = "#10B981" if margine > 0 else "#EF4444"
            status = "🟢 ON (In-the-Money)" if margine > 0 else "🔴 OFF (Out-of-Money)"
            col_target.markdown(f"<div style='background:#1F2937; padding:10px; border-radius:8px; margin-bottom:10px; border-left:4px solid {color};'><b>Solare</b><br><span style='font-size:20px; font-weight:bold; color:{color};'>€ {margine:.2f}</span><br><span style='font-size:12px;'>AI Status: {status}</span></div>", unsafe_allow_html=True)
            idx += 1

# ==========================================
# WORKSPACE 2: DATI REALI SVIZZERI (ENTSO-E)
# ==========================================
elif workspace == _('ws2'):
    st.markdown(f"<h1>{_('ws2')}</h1>", unsafe_allow_html=True)
    
    desc_html = edu("API Ufficiale ENTSO-E", "ENTSO-E (European Network of Transmission System Operators for Electricity) è l'associazione europea dei gestori di rete. La loro piattaforma Transparency Platform (transparency.entsoe.eu) è la fonte dati primaria per ogni trader quantitativo, offrendo dati su produzione, consumi e blackout per tutta Europa.")
    st.markdown(f"Questa dashboard interroga l'{desc_html} per il mercato Day-Ahead Svizzero (Swissix).", unsafe_allow_html=True)
    
    st.subheader("⚙️ Console Timeframe")
    
    oggi = datetime.date.today()
    default_inizio = oggi - datetime.timedelta(days=7)

    col_inizio, col_fine, col_btn = st.columns([2, 2, 1])
    with col_inizio:
        data_inizio_selezionata = st.date_input("Data Inizio", value=default_inizio)
    with col_fine:
        data_fine_selezionata = st.date_input("Data Fine", value=oggi)
    with col_btn:
        st.write(""); st.write("")
        if st.button("🚀 Aggiorna API Cache"): scarica_dati_entsoe.clear()

    st.markdown("---")
    
    api_key = get_entsoe_key()
    if not api_key:
        st.warning("🔑 Chiave API ENTSO-E non configurata: aggiungi `ENTSOE_API_KEY` a `.streamlit/secrets.toml` oppure incollala qui sotto.")
        api_key = st.text_input("Chiave API ENTSO-E", type="password")
    if not api_key:
        st.stop()

    try:
        with st.spinner("⏳ Connessione a ENTSO-E in corso..."):
            prezzi_ch = scarica_dati_entsoe(api_key, data_inizio_selezionata, data_fine_selezionata).dropna()
            if prezzi_ch.empty:
                st.warning("ENTSO-E non ha restituito dati per il periodo selezionato.")
                st.stop()
            
            prezzo_spot_ch = prezzi_ch.iloc[-1]
            valore_integrale = prezzi_ch.sum()
            
            fig_entsoe = go.Figure()
            fig_entsoe.add_trace(go.Scatter(
                x=prezzi_ch.index, 
                y=prezzi_ch.values, 
                fill='tozeroy', 
                fillcolor='rgba(59, 130, 246, 0.2)',
                mode='lines',
                line=dict(color='#3b82f6', width=2),
                name="Prezzo Spot (€/MWh)"
            ))
            fig_entsoe.update_layout(
                title=f"Andamento Prezzo Spot & Integrale del Valore (Totale Baseload 1 MW: {valore_integrale:,.0f} €)",
                xaxis_title="Data e Ora", 
                yaxis_title="Prezzo (€/MWh)", 
                template="plotly_dark", 
                height=350,
                margin=dict(l=40, r=40, t=40, b=40)
            )
            st.plotly_chart(fig_entsoe, use_container_width=True)
            
            eff_ircd = 0.25; prezzo_gas_eu = 38.5; prezzo_co2_eu = 68.0  
            mc_gas = (prezzo_gas_eu / eff_ircd) + (prezzo_co2_eu * 0.2 / eff_ircd) 
            mc_hydro = 5.0
            mc_solar = 0.0

            margine_ircd = prezzo_spot_ch - mc_gas
            margine_hydro = prezzo_spot_ch - mc_hydro
            margine_solar = prezzo_spot_ch - mc_solar
            
            st.subheader("Margini Operativi Istantanei (Sull'ultima candela oraria)")
            col1, col2, col3 = st.columns(3)
            
            col1.metric(label="🏭 IRCD Giubiasco", value=f"€ {margine_ircd:.2f}", delta="Termovalorizzatore (Proxy Gas)", help="Margine per un impianto WtE (Waste-to-Energy)")
            col2.metric(label="💧 Centrale Biasca", value=f"€ {margine_hydro:.2f}", delta="Idroelettrico", help="Margine decurtato dai costi di O&M")
            col3.metric(label="☀️ Diga del Muttsee", value=f"€ {margine_solar:.2f}", delta="Solare d'Alta Quota", help="Impianto solare alpino, massima efficienza invernale.")
            
            st.markdown("---")

            titolo_mo = edu("Merit Order & Produzione Stimata", "Il Merit Order mette in fila le centrali dalla più economica (Rinnovabili) alla più costosa (Gas/Carbone). L'intersezione con la domanda determina il prezzo. Qui mostriamo anche la stima dell'energia prodotta nel timeframe calcolando quante ore la singola centrale è risultata 'In-The-Money' (Prezzo Spot > Costo Marginale).")
            st.markdown(f"### {titolo_mo}", unsafe_allow_html=True)

            cap_solar = 50   
            cap_hydro = 250  
            cap_gas = 100    
            tot_hours = len(prezzi_ch)
            
            prod_solar = cap_solar * (tot_hours * 0.30)
            ore_in_money_hydro = (prezzi_ch > mc_hydro).sum()
            prod_hydro = cap_hydro * ore_in_money_hydro
            ore_in_money_gas = (prezzi_ch > mc_gas).sum()
            prod_gas = cap_gas * ore_in_money_gas
            
            df_mo = pd.DataFrame({
                "Centrale": ["☀️ Solare (Muttsee)", "💧 Idro (Biasca)", "🏭 Gas WtE (Giubiasco)"],
                "Marginal_Cost": [mc_solar, mc_hydro, mc_gas],
                "Capacity": [cap_solar, cap_hydro, cap_gas],
                "Production": [prod_solar, prod_hydro, prod_gas],
                "Color": ["#eab308", "#3b82f6", "#ef4444"]
            }).sort_values(by="Marginal_Cost") 
            
            df_mo['Cum_Capacity'] = df_mo['Capacity'].cumsum()
            df_mo['X_Center'] = df_mo['Cum_Capacity'] - (df_mo['Capacity'] / 2)
            
            fig_mo = go.Figure()
            
            for i, row in df_mo.iterrows():
                fig_mo.add_trace(go.Bar(
                    x=[row['X_Center']],
                    y=[row['Marginal_Cost']],
                    width=[row['Capacity']],
                    marker_color=row['Color'],
                    name=row['Centrale'],
                    text=f"Prod. Stima:<br><b>{row['Production']:,.0f} MWh</b>",
                    textposition="outside",
                    hovertemplate=(
                        f"<b>{row['Centrale']}</b><br>" +
                        "Costo Marginale: %{y:.1f} €/MWh<br>" +
                        "Capacità: %{width} MW<br>" +
                        f"Prod. Timeframe: {row['Production']:,.0f} MWh<extra></extra>"
                    )
                ))
            
            avg_price = prezzi_ch.mean()
            fig_mo.add_hline(y=avg_price, line_dash="dot", line_color="white", 
                             annotation_text=f"Prezzo Medio Timeframe: {avg_price:.1f} €/MWh", 
                             annotation_position="top left")
            
            fig_mo.update_layout(
                title="Curva di Offerta Aggregata (Merit Order)",
                xaxis_title="Capacità Cumulata (MW)",
                yaxis_title="Costo Marginale (€/MWh)",
                template="plotly_dark",
                barmode='overlay',
                height=400,
                showlegend=True,
                margin=dict(t=50, b=50, l=50, r=50)
            )
            fig_mo.update_xaxes(range=[0, df_mo['Cum_Capacity'].max() + 50])
            fig_mo.update_yaxes(range=[0, max(mc_gas * 1.3, avg_price * 1.3)])
            
            st.plotly_chart(fig_mo, use_container_width=True)
            
    except Exception as e:
        st.error(f"Errore connessione ENTSO-E: {e}")

# ==========================================
# WORKSPACE 3: AUTONOMOUS AI & MARL
# ==========================================
elif workspace == _('ws3'):
    titolo_marl = edu("Multi-Agent Reinforcement Learning (MARL)", "Nel MARL, algoritmi (agenti) operano in un ambiente simulato, compiendo azioni (compra/vendi) e ricevendo una ricompensa (Profitto) o una penalità (Perdita). Col tempo, la rete neurale 'impara' le strategie ottimali senza programmazione esplicita.")
    st.markdown(f"<h1>🤖 {titolo_marl}</h1>", unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    render_kpi("Stato Agente AI", "🟢 ACTIVE", c1)
    render_kpi("Sharpe Ratio AI", "2.84", c2)
    render_kpi(edu("Flash Crash Prob", "Probabilità stimata dai Processi di Hawkes che si verifichi un crollo repentino dei prezzi guidato da algoritmi HFT."), f"1.4%", c3)
    render_kpi(edu("NLP Sentiment", "Natural Language Processing: algoritmo che legge le news di Reuters/Bloomberg e assegna uno score (-1 Bear, +1 Bull)."), f"{ult['Sentiment_NLP']:.2f}", c4)
    
    col_a, col_b = st.columns([2, 1])
    with col_a:
        epoches = np.arange(1000)
        np.random.seed(1234)
        reward_curve = -50 + 100 * np.log(epoches + 1) / np.log(1000) + np.random.normal(0, 5, 1000)
        fig_rl = px.line(x=epoches, y=reward_curve, title="Learning Curve dell'Agente Quantitativo")
        fig_rl.update_layout(template="plotly_dark", xaxis_title="Epoche di Addestramento", yaxis_title="Reward (PnL in €)")
        st.plotly_chart(fig_rl, use_container_width=True)
        
    with col_b:
        regime = "BULLISH" if ult['Sentiment_NLP'] > 0 else "BEARISH"
        st.markdown(f"<h3>Regime: {regime}</h3>", unsafe_allow_html=True)
        st.markdown(f"**{edu('Stat Arb Z-Score', 'Statistical Arbitrage: Z-Score misura di quante deviazioni standard lo spread tra due asset (es. Gas/Power) si è discostato dalla media storica.')}:** +2.4", unsafe_allow_html=True)
        
        np.random.seed(1235)
        heatmap_lat = np.random.normal(1.5, 0.2, (5, 5))
        fig_lat = px.imshow(heatmap_lat, color_continuous_scale="RdYlGn_r", title="Network Latency (ms)")
        fig_lat.update_layout(template="plotly_dark", height=200, margin=dict(l=0, r=0, t=30, b=0), xaxis_title="Gateway Node", yaxis_title="Exchange Node")
        st.plotly_chart(fig_lat, use_container_width=True)

# ==========================================
# WORKSPACE 4: CLIMATE & GRID INTEL
# ==========================================
elif workspace == _('ws4'):
    st.markdown(f"<h1>{_('ws4')}</h1>", unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    enso_html = edu("ENSO Index", "El Niño-Southern Oscillation. Fenomeno climatico nel Pacifico. I trader energetici lo osservano perché anomalie qui influenzano la rigidità degli inverni in Europa, e di conseguenza la domanda di gas e power.")
    render_kpi(enso_html, "1.2 (El Niño)", c1)
    
    vortex_html = edu("Polar Vortex", "Vortice Polare: se debole/instabile, l'aria gelida artica scivola verso l'Europa causando ondate di gelo estremo (es. Beast from the East).")
    render_kpi(vortex_html, "Stabile", c2)
    
    inertia_html = edu("Grid Inertia", "L'inerzia della rete. Mantenuta dalle enormi turbine rotanti delle centrali termiche. Con l'aumento di solare/eolico (che non hanno masse rotanti), l'inerzia crolla, rendendo la rete instabile. Molto importante per i trader di 'Ancillary Services'.")
    render_kpi(inertia_html, "CRITICA", c3)
    render_kpi("Dynamic Line Rating", "+15% Cap", c4)
    
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        titolo_wind = edu("Wind Power Curve", "Curva di potenza teorica di una turbina eolica. Mostra come i megawatt generati dipendano in modo non lineare (spesso cubico) dalla velocità del vento. Raggiunto il 'Rated Wind Speed', la potenza si appiattisce al massimo. Oltre il 'Cut-out Speed', la turbina si blocca per sicurezza, azzerando la produzione di colpo e causando picchi di prezzo in borsa.")
        st.markdown(f"### {titolo_wind}", unsafe_allow_html=True)
        
        wind_speeds = np.linspace(0, 30, 200)
        rated_power = 3000
        power = np.where(wind_speeds < 3, 0, 
                np.where(wind_speeds <= 12, rated_power * ((wind_speeds - 3) / 9)**3, 
                np.where(wind_speeds <= 25, rated_power, 0)))
        
        fig_wind = px.line(x=wind_speeds, y=power)
        fig_wind.update_layout(template="plotly_dark", xaxis_title="Velocità Vento (m/s)", yaxis_title="Potenza Generata (MW)")
        st.plotly_chart(fig_wind, use_container_width=True)
        
    with col_w2:
        titolo_hydro = edu("Hydro Reservoir Topography", "Rappresentazione topografica 3D del livello dell'acqua di un bacino idroelettrico alpino. Maggiore è il volume e l'altezza dell'acqua, maggiore è l'energia potenziale accumulata (State of Charge - SoC) pronta per essere convertita in MWh alla prima occasione profittevole.")
        st.markdown(f"### {titolo_hydro}", unsafe_allow_html=True)
        
        X, Y = np.meshgrid(np.linspace(-5, 5, 30), np.linspace(-5, 5, 30))
        Z = (X**2 * 0.8 + Y**2 * 1.2) * 5 + 400
        Z = np.clip(Z, 420, 600) 
        
        fig_hydro = go.Figure(data=[go.Surface(z=Z, colorscale="Blues", reversescale=True)])
        fig_hydro.update_layout(template="plotly_dark", height=300, margin=dict(l=0, r=0, t=0, b=0), scene=dict(xaxis_title="Latitudine (X)", yaxis_title="Longitudine (Y)", zaxis_title="Livello Acqua (m)"))
        st.plotly_chart(fig_hydro, use_container_width=True)

# ==========================================
# WORKSPACE 5: EXOTICS & STRUCTURING
# ==========================================
elif workspace == _('ws5'):
    st.markdown(f"<h1>{_('ws5')}</h1>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    render_kpi(edu("SABR Alpha", "Parametro del modello SABR (Stochastic Alpha Beta Rho) che governa il livello iniziale della volatilità stocastica."), "0.354", c1)
    render_kpi("SABR Beta", "0.500", c2)
    render_kpi(edu("Quanto Corr (ρ)", "Correlazione in un'opzione 'Quanto', un derivato in cui l'asset sottostante è in una valuta (es. Gas in USD) ma regolato in un'altra (EUR) ad un tasso fisso."), "-0.45", c3)
    
    col_e1, col_e2 = st.columns([1.5, 1])
    with col_e1:
        st.markdown("### Implied Volatility Smile")
        strikes = np.linspace(30, 150, 40)
        smile = 0.4 + 0.0001 * (strikes - 80)**2 - 0.002 * (strikes - 80)
        fig_sabr = px.line(x=strikes, y=smile*100)
        fig_sabr.add_vline(x=80, line_dash="dash", line_color="red")
        fig_sabr.update_layout(template="plotly_dark", xaxis_title="Strike Price (€/MWh)", yaxis_title="Implied Volatility (%)")
        st.plotly_chart(fig_sabr, use_container_width=True)
        
    with col_e2:
        st.markdown("### 3rd Order Greeks")
        st.markdown(f"🚀 **{edu('Speed', 'Variazione del Gamma rispetto a cambiamenti nel prezzo spot (Derivata terza del premio).')} (dGamma/dSpot):** -0.0014", unsafe_allow_html=True)
        st.markdown(f"🎨 **{edu('Color', 'Decadimento temporale del Gamma (dGamma/dTime).')} (dGamma/dTime):** +0.0251", unsafe_allow_html=True)
        st.markdown(f"🌪️ **{edu('Zomma', 'Sensibilità del Gamma ai cambiamenti di volatilità. Fondamentale per i portafogli Gamma-hedged.')} (dGamma/dVol):** +0.1042", unsafe_allow_html=True)

# ==========================================
# WORKSPACE 6: ENTERPRISE RISK & XVA
# ==========================================
elif workspace == _('ws6'):
    st.markdown(f"<h1>{_('ws6')}</h1>", unsafe_allow_html=True)
    
    msg_error = edu("SIMM MARGIN Breach", "Standard Initial Margin Model: calcolo standard ISDA. Margin Breach significa che le perdite stimate superano la garanzia (collaterale) versata in borsa, innescando una chiamata a margine immediata.")
    st.markdown(f"<div style='background-color:rgba(255, 75, 75, 0.15); color:#ff4b4b; padding:1rem; border:1px solid #ff4b4b; border-radius:0.5rem; margin-bottom:1rem;'>🚨 **{msg_error} WARNING:** ICE Endex.</div>", unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    render_kpi(edu("FRTB Expected Shortfall", "Fundamental Review of the Trading Book. L'Expected Shortfall (ES) ha sostituito il VaR per le banche. Calcola la perdita MEDIA nel peggiore X% dei casi (Coda della distribuzione)."), "€ 45.2 M", c1)
    render_kpi(edu("CVA", "Credit Valuation Adjustment: Sconto sul fair value di un derivato a causa del rischio che la controparte fallisca."), "€ 2.1 M", c2)
    render_kpi("DVA", "€ 0.5 M", c3)
    render_kpi("ESG Score", "12 / 100", c4)
    
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.markdown(f"### {edu('Liquidity Horizon', 'Sotto le nuove norme FRTB, non puoi assumere di vendere un asset istantaneamente. Il capitale da accantonare cresce in base a quanti giorni servono per liquidare il portafoglio in caso di crisi.')}", unsafe_allow_html=True)
        horizons = pd.DataFrame({"Asset Class": ["Power", "Gas", "Coal", "Carbon"], "Capital Charge": [15.2, 18.5, 8.4, 3.1]})
        fig_frtb = px.bar(horizons, x="Asset Class", y="Capital Charge")
        fig_frtb.update_layout(template="plotly_dark", height=300, xaxis_title="Classe di Asset", yaxis_title="Capitale Assorbito (M€)")
        st.plotly_chart(fig_frtb, use_container_width=True)
        
    with col_r2:
        st.markdown(f"### {edu('Wrong-Way Risk (WWR)', 'Si verifica quando l\'esposizione verso una controparte (EAD) aumenta in concomitanza con la probabilità di default (PD) della controparte stessa. Es: Compri opzioni Put su Enron da Enron stessa.')}", unsafe_allow_html=True)
        np.random.seed(1236)
        ead = np.random.lognormal(mean=2, sigma=0.5, size=100)
        pd_cpty = 0.01 + ead * 0.002 + np.random.normal(0, 0.01, 100)
        fig_wwr = px.scatter(x=ead, y=pd_cpty)
        fig_wwr.update_layout(template="plotly_dark", height=300, xaxis_title="Esposizione al Default - EAD (M€)", yaxis_title="Probabilità di Default - PD (%)")
        st.plotly_chart(fig_wwr, use_container_width=True)

# ==========================================
# WORKSPACE 7: METODO STAR & OTTIMIZZAZIONE
# ==========================================
elif workspace == _('ws7'):
    st.markdown("<h1>📈 Framework STAR & Metriche di Performance (Quant Trading)</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #9CA3AF;'>Approccio strutturato per la valorizzazione delle competenze tecniche e quantitative in ambito Energy Trading (es. DXT Commodities).</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Box della risposta corretta del test integrata come standard metodologico
    st.markdown("""
    <div style='background-color:rgba(16, 185, 129, 0.1); border:1px solid #10B981; border-radius:8px; padding:20px; margin-bottom:25px;'>
        <h3 style='color:#10B981; margin-top:0;'>✔️ Best Practice Recruiter (Metodo STAR con Metriche)</h3>
        <p style='color:#E5E7EB; font-size:16px; font-style:italic; margin-bottom:10px;'>
            "Sviluppato un modello in Python per l'analisi dello spark spread storico, riducendo i tempi di reportistica del 20%."
        </p>
        <p style='color:#9CA3AF; font-size:13px; margin:0;'>
            Questo approccio combina competenze tecniche specifiche (Python, spark spread), descrive un'azione concreta (sviluppato un modello) e quantifica il risultato (ridotto i tempi del 20%), che è il metodo più efficace per dimostrare valore nei mercati energetici.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("⚙️ Scomponi il tuo progetto con il Framework STAR")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown("""
        <div style='background:#111827; padding:15px; border-radius:8px; border:1px solid #1F2937; height: 100%;'>
            <h4 style='color:#60A5FA;'>🎯 1. Situation (Contesto)</h4>
            <p style='font-size:13px; color:#D1D5DB;'>Esigenza di monitorare in tempo reale i margini di guadagno (Spark/Dark Spreads) e l'esposizione al rischio sui mercati energetici europei ed elvetici.</p>
            <h4 style='color:#60A5FA;'>🧩 2. Task (Obiettivo)</h4>
            <p style='font-size:13px; color:#D1D5DB;'>Progettare un motore di calcolo quantitativo integrato ed efficiente per automatizzare i flussi di dati e l'analisi dei prezzi spot (es. ENTSO-E).</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_s2:
        st.markdown("""
        <div style='background:#111827; padding:15px; border-radius:8px; border:1px solid #1F2937; height: 100%;'>
            <h4 style='color:#60A5FA;'>⚡ 3. Action (Azione)</h4>
            <p style='font-size:13px; color:#D1D5DB;'>Sviluppo di un modello in Python strutturato in moduli interattivi (Streamlit/Plotly), integrando API di mercato e logiche di ottimizzazione del Merit Order.</p>
            <h4 style='color:#60A5FA;'>📊 4. Result (Risultato & Metriche)</h4>
            <p style='font-size:13px; color:#D1D5DB;'>Riduzione dei tempi di reportistica del 20%, abbattimento dei margini di errore umano e incremento della reattività decisionale di trading.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📊 Metriche di Impatto Quantificabili")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(label="Tempo di Reportistica", value="-20%", delta="Ottimizzazione", help="Riduzione del tempo impiegato per l'analisi dei dati.")
    m2.metric(label="Automazione Flussi", value="100%", delta="Real-time API", help="Integrazione diretta con le fonti dati di mercato.")
    m3.metric(label="Copertura Modelli", value="8 Workspaces", delta="Completo", help="Copertura da asset class classiche a XVA e Risk.")
    m4.metric(label="Efficienza Codice", value="Python / TS", delta="High Performance", help="Stack tecnologico solido e reattivo.")

# ==========================================
# WORKSPACE 8: PRICE ANALYTICS (SWISSIX DETTAGLIO)
# ==========================================
elif workspace == _('ws8'):
    st.markdown(f"<h1>{_('ws8')}</h1>", unsafe_allow_html=True)
    st.markdown("Analisi operativa del prezzo spot orario Swissix (CH): KPI, confronto con il periodo precedente, soglie di alert, profilo giornaliero, heatmap oraria, fasce F1/F2/F3, tabella dati, rischio & durata, arbitraggio batteria, base/peak mensile, simulatore costo fornitura, MtM hedging, spark spread, shaping curva, spread weekend, price capture ed export CSV.")

    # ---------- Controlli: sorgente, periodo, impianti ----------
    st.subheader("⚙️ Sorgente dati & Timeframe")
    c_src, c_per = st.columns([1, 2])
    with c_src:
        sorgente = st.radio("Sorgente dati", ["🧪 Mock (offline)", "🌐 ENTSO-E live"], index=0,
                            help="Mock: serie oraria sintetica ma realistica (profilo giornaliero + stagionalità settimanale). Live: prezzi day-ahead reali dalla Transparency Platform ENTSO-E.")
    with c_per:
        preset = st.radio("Periodo", ["7 giorni", "30 giorni", "90 giorni", "Personalizzato"], horizontal=True, index=1)
    oggi = datetime.date.today()
    if preset == "7 giorni":
        d0, d1 = oggi - datetime.timedelta(days=7), oggi
    elif preset == "30 giorni":
        d0, d1 = oggi - datetime.timedelta(days=30), oggi
    elif preset == "90 giorni":
        d0, d1 = oggi - datetime.timedelta(days=90), oggi
    else:
        cc0, cc1 = st.columns(2)
        d0 = cc0.date_input("Data inizio", oggi - datetime.timedelta(days=30))
        d1 = cc1.date_input("Data fine", oggi)
    if d0 > d1:
        st.error("La data di inizio deve precedere la data di fine.")
        st.stop()

    st.subheader("🏭 Impianti / Siti")
    assets_sel = st.multiselect(
        "Filtra impianti (le rette di costo marginale e la produzione stimata si aggiornano)",
        list(ASSETS.keys()),
        default=list(ASSETS.keys()),
    )

    soglia = st.number_input("🚨 Soglia di alert prezzo (€/MWh)", min_value=0.0, value=150.0, step=5.0,
                             help="Le ore con prezzo sopra la soglia vengono evidenziate nel grafico, conteggiate nei KPI e filtrabili in tabella.")

    # ---------- Caricamento dati ----------
    def carica(a, b):
        if sorgente == "🌐 ENTSO-E live":
            key = get_entsoe_key()
            if not key:
                st.warning("🔑 Chiave API ENTSO-E non configurata: aggiungi `ENTSOE_API_KEY` a `.streamlit/secrets.toml`.")
                st.stop()
            return scarica_dati_entsoe(key, a, b).dropna()
        return generate_mock_hourly(a, b).dropna()

    try:
        with st.spinner("⏳ Caricamento dati..."):
            prezzi = carica(d0, d1)
    except Exception as e:
        st.error(f"Errore nel caricamento dati: {e}")
        st.stop()
    if prezzi.empty:
        st.warning("Nessun dato disponibile per il periodo selezionato.")
        st.stop()

    # Periodo precedente (stessa durata) per variazione % e confronto
    d_prev1 = d0 - datetime.timedelta(days=1)
    d_prev0 = d_prev1 - (d1 - d0)
    try:
        prev = carica(d_prev0, d_prev1)
        var_pct = (prezzi.mean() - prev.mean()) / prev.mean() * 100 if prev.mean() != 0 else 0.0
    except Exception:
        prev = None
        var_pct = None

    # ---------- KPI ----------
    st.subheader("📌 KPI di periodo")
    medio = prezzi.mean()
    picco = prezzi.max()
    t_picco = prezzi.idxmax()
    ore_sopra = int((prezzi > soglia).sum())
    k1, k2, k3, k4 = st.columns(4)
    render_kpi("Prezzo medio (€/MWh)", f"{medio:,.2f}", k1)
    render_kpi("Prezzo mediano (€/MWh)", f"{prezzi.median():,.2f}", k2)
    render_kpi("Deviazione std (€/MWh)", f"{prezzi.std():,.2f}", k3)
    render_kpi("Variazione vs periodo prec.", f"{var_pct:+.1f} %" if var_pct is not None else "n/d", k4)
    k5, k6, k7, k8 = st.columns(4)
    render_kpi("Picco di prezzo (€/MWh)", f"{picco:,.2f}", k5)
    render_kpi("Data/ora del picco", t_picco.strftime("%d/%m %H:00"), k6)
    render_kpi(f"Ore sopra soglia ({soglia:.0f} €/MWh)", f"{ore_sopra} h ({ore_sopra/len(prezzi)*100:.1f} %)", k7)
    render_kpi("Valore baseload 1 MW (€)", f"{prezzi.sum():,.0f}", k8)

    # ---------- Grafico principale ----------
    st.subheader("📉 Prezzo spot orario")
    fig_px = go.Figure()
    fig_px.add_trace(go.Scatter(
        x=prezzi.index, y=prezzi.values, mode='lines', name="Prezzo spot (€/MWh)",
        line=dict(color='#3b82f6', width=1.5),
        fill='tozeroy', fillcolor='rgba(59, 130, 246, 0.15)',
    ))
    sopra = prezzi[prezzi > soglia]
    if not sopra.empty:
        fig_px.add_trace(go.Scatter(
            x=sopra.index, y=sopra.values, mode='markers',
            name=f"Sopra soglia ({len(sopra)} h)", marker=dict(color='#ef4444', size=5),
        ))
    fig_px.add_hline(y=soglia, line_dash="dash", line_color="#ef4444",
                     annotation_text=f"Soglia alert: {soglia:.0f} €/MWh", annotation_position="top left")
    for nome in assets_sel:
        mc, cap, col = ASSETS[nome]
        fig_px.add_hline(y=mc, line_dash="dot", line_color=col,
                         annotation_text=f"MC {nome}: {mc:.0f} €/MWh", annotation_position="top right")
    fig_px.add_vline(x=t_picco, line_dash="dot", line_color="#eab308",
                     annotation_text=f"Picco {picco:.0f} €/MWh", annotation_position="bottom right")
    mostra_confronto = st.toggle("Confronta con il periodo precedente (sovrapposto)", value=False,
                                 help="Sovrappone la serie del periodo precedente (stessa durata), allineata per ora relativa.")
    if mostra_confronto:
        if prev is not None and not prev.empty:
            n = min(len(prezzi), len(prev))
            fig_px.add_trace(go.Scatter(
                x=prezzi.index[:n], y=prev.values[-n:], mode='lines',
                name="Periodo precedente", line=dict(color='#9ca3af', width=1.5, dash='dash'),
            ))
        else:
            st.info("Periodo precedente non disponibile per il confronto.")
    fig_px.update_layout(
        template="plotly_dark", height=420,
        xaxis_title="Data e Ora", yaxis_title="Prezzo (€/MWh)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig_px, use_container_width=True)

    # ---------- Impianti: marginal cost & produzione stimata ----------
    if assets_sel:
        st.subheader("🏭 Marginal cost & produzione stimata (impianti selezionati)")
        righe = []
        for nome in assets_sel:
            mc, cap, col = ASSETS[nome]
            ore_itm = int((prezzi > mc).sum())
            prod = cap * ore_itm
            margine_medio = float((prezzi[prezzi > mc] - mc).mean()) if ore_itm else 0.0
            righe.append({
                "Impianto": nome,
                "Costo marginale (€/MWh)": round(mc, 1),
                "Capacità (MW)": cap,
                "Ore in-the-money": ore_itm,
                "Produzione stimata (MWh)": f"{prod:,.0f}",
                "Margine medio ITM (€/MWh)": round(margine_medio, 2),
            })
        st.dataframe(pd.DataFrame(righe), use_container_width=True, hide_index=True)

    # ---------- Tab di analisi ----------
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12, tab13 = st.tabs(["⏱️ Profilo giornaliero", "🔥 Heatmap oraria", "⚡ Fasce F1/F2/F3", "📋 Tabella dati", "⚠️ Rischio & Durata", "🔋 Arbitraggio Batteria", "📊 Base/Peak mensile", "💰 Costo fornitura", "📈 MtM hedging", "🔥 Spark spread", "📐 Shaping curva", "📅 Weekend", "☀️ Price capture"])

    with tab1:
        st.markdown("**Curva di carico giornaliera**: prezzo medio per ora del giorno (banda = ±1 deviazione std, linea tratteggiata = massimo).")
        prof = prezzi.groupby(prezzi.index.hour).agg(["mean", "std", "max"])
        fig_prof = go.Figure()
        fig_prof.add_trace(go.Scatter(x=prof.index, y=prof["mean"] + prof["std"], mode='lines',
                                      line=dict(width=0), showlegend=False, hoverinfo='skip'))
        fig_prof.add_trace(go.Scatter(x=prof.index, y=prof["mean"] - prof["std"], mode='lines',
                                      line=dict(width=0), fill='tonexty',
                                      fillcolor='rgba(59,130,246,0.2)', name='±1 std', hoverinfo='skip'))
        fig_prof.add_trace(go.Scatter(x=prof.index, y=prof["mean"], mode='lines+markers',
                                      name='Prezzo medio', line=dict(color='#3b82f6', width=3)))
        fig_prof.add_trace(go.Scatter(x=prof.index, y=prof["max"], mode='lines',
                                      name='Massimo', line=dict(color='#eab308', width=1.5, dash='dash')))
        fig_prof.update_layout(template="plotly_dark", height=380,
                               xaxis_title="Ora del giorno", yaxis_title="Prezzo (€/MWh)",
                               xaxis=dict(tickmode='linear', dtick=2))
        st.plotly_chart(fig_prof, use_container_width=True)

    with tab2:
        st.markdown("**Heatmap oraria**: ogni riga è un giorno, ogni colonna un'ora. I picchi di prezzo (rosso) saltano subito all'occhio.")
        df_hm = pd.DataFrame({"giorno": prezzi.index.date, "ora": prezzi.index.hour, "prezzo": prezzi.values})
        pivot = df_hm.pivot_table(index="giorno", columns="ora", values="prezzo", aggfunc="mean")
        fig_hm = px.imshow(pivot, color_continuous_scale="RdYlGn_r", aspect="auto",
                           title="Heatmap oraria del prezzo (€/MWh)",
                           labels=dict(x="Ora del giorno", y="Giorno", color="€/MWh"))
        fig_hm.update_layout(template="plotly_dark", height=max(350, min(700, 40 * len(pivot) + 80)))
        st.plotly_chart(fig_hm, use_container_width=True)

    with tab3:
        st.markdown(f"**Ripartizione per fascia oraria** {edu('F1/F2/F3', 'Fasce orarie AEEGSI: F1 = lun–ven 08:00–19:00 (ore di punta); F2 = lun–ven 07:00–08:00 e 19:00–23:00, sab 07:00–23:00; F3 = ore notturne, domeniche e festivi (fuori punta).')}", unsafe_allow_html=True)
        df_fx = pd.DataFrame({"prezzo": prezzi.values, "fascia": prezzi.index.map(fascia_oraria)})
        agg_fx = df_fx.groupby("fascia").agg(
            ore=("prezzo", "size"),
            prezzo_medio=("prezzo", "mean"),
            prezzo_max=("prezzo", "max"),
            valore_baseload_1MW=("prezzo", "sum"),
        ).reindex(["F1", "F2", "F3"])
        agg_show = agg_fx.copy()
        agg_show["prezzo_medio"] = agg_show["prezzo_medio"].round(2)
        agg_show["prezzo_max"] = agg_show["prezzo_max"].round(2)
        agg_show["valore_baseload_1MW"] = agg_show["valore_baseload_1MW"].round(0)
        st.dataframe(agg_show, use_container_width=True)
        fig_fx = px.bar(agg_fx.reset_index(), x="fascia", y="prezzo_medio", color="fascia",
                        color_discrete_map={"F1": "#ef4444", "F2": "#eab308", "F3": "#3b82f6"},
                        title="Prezzo medio per fascia oraria (€/MWh)", text_auto=".1f")
        fig_fx.update_layout(template="plotly_dark", height=350, showlegend=False,
                             xaxis_title="Fascia", yaxis_title="Prezzo medio (€/MWh)")
        st.plotly_chart(fig_fx, use_container_width=True)

    with tab4:
        st.markdown("**Tabella dati dettagliata**: clicca sulle intestazioni per ordinare.")
        df_tab = pd.DataFrame({
            "Data e Ora": prezzi.index,
            "Prezzo (€/MWh)": prezzi.values.round(2),
        })
        df_tab["Fascia"] = df_tab["Data e Ora"].map(fascia_oraria)
        df_tab["Sopra soglia"] = np.where(df_tab["Prezzo (€/MWh)"] > soglia, "🔴", "")
        solo_sopra = st.checkbox("Mostra solo le ore sopra soglia", value=False)
        df_view = df_tab[df_tab["Prezzo (€/MWh)"] > soglia] if solo_sopra else df_tab
        st.dataframe(df_view, use_container_width=True, hide_index=True)
        st.download_button(
            "⬇️ Esporta CSV",
            df_view.to_csv(index=False).encode("utf-8"),
            file_name=f"swissix_{d0}_{d1}{'_sopra_soglia' if solo_sopra else ''}.csv",
            mime="text/csv",
            help="Scarica i dati visualizzati in tabella (rispetta il filtro 'sopra soglia').",
        )

    with tab5:
        st.markdown("**Rischio downside**: VaR e Expected Shortfall sulla distribuzione oraria del prezzo (floor di ricavo atteso), max drawdown e curva di durata (prezzi ordinati dal più alto al più basso).")
        v = prezzi.values.astype(float)
        var95 = float(np.quantile(v, 0.05))
        var99 = float(np.quantile(v, 0.01))
        es95 = float(v[v <= var95].mean())
        picchi = np.maximum.accumulate(v)
        # FIX: prezzi live (ENTSO-E) possono essere 0 o negativi -> guardia contro divisione per zero/inf
        drawdown = np.zeros_like(v)
        mask_pos = picchi > 0
        with np.errstate(divide="ignore", invalid="ignore"):
            drawdown[mask_pos] = (v[mask_pos] - picchi[mask_pos]) / picchi[mask_pos] * 100
        drawdown = np.nan_to_num(drawdown, nan=0.0, posinf=0.0, neginf=-100.0)
        max_dd = float(drawdown.min())

        titolo_var = edu("VaR 95% (€/MWh)", "Value-at-Risk: nel 95% delle ore il prezzo è STATO SOPRA questo livello. Il restante 5% delle ore ha prezzi più bassi (rischio downside).")
        titolo_es = edu("Expected Shortfall 95%", "Media del prezzo nelle ore peggiori (il 5% sotto il VaR). Stima del ricavo atteso negli scenari di prezzo basso.")
        r1, r2, r3, r4 = st.columns(4)
        render_kpi(titolo_var, f"{var95:,.2f}", r1)
        render_kpi(titolo_es, f"{es95:,.2f}", r2)
        render_kpi("VaR 99% (€/MWh)", f"{var99:,.2f}", r3)
        render_kpi(edu("Max Drawdown", "Peggior ribasso percentuale picco-minimo del prezzo nel periodo. Misura il rischio di timing per le vendite spot."), f"{max_dd:+.1f} %", r4)

        col_d1, col_d2 = st.columns(2)
        with col_d1:
            dur = np.sort(v)[::-1]
            fig_dur = go.Figure()
            fig_dur.add_trace(go.Scatter(
                x=np.arange(1, len(dur) + 1), y=dur, mode='lines', name="Curva di durata",
                line=dict(color='#8b5cf6', width=2),
                fill='tozeroy', fillcolor='rgba(139, 92, 246, 0.15)',
            ))
            fig_dur.add_hline(y=var95, line_dash="dash", line_color="#ef4444",
                              annotation_text=f"VaR 95%: {var95:.0f} €/MWh", annotation_position="top left")
            fig_dur.update_layout(template="plotly_dark", height=380,
                                  xaxis_title="Ore (ordinate per prezzo decrescente)", yaxis_title="Prezzo (€/MWh)",
                                  title="Curva di durata del prezzo")
            st.plotly_chart(fig_dur, use_container_width=True)
        with col_d2:
            fig_dd = go.Figure()
            fig_dd.add_trace(go.Scatter(
                x=prezzi.index, y=drawdown, mode='lines', name="Drawdown %",
                line=dict(color='#ef4444', width=1.5),
                fill='tozeroy', fillcolor='rgba(239, 68, 68, 0.2)',
            ))
            fig_dd.update_layout(template="plotly_dark", height=380,
                                 xaxis_title="Data e Ora", yaxis_title="Drawdown (%)",
                                 title=f"Drawdown del prezzo (max {max_dd:.1f} %)")
            st.plotly_chart(fig_dd, use_container_width=True)

    with tab6:
        titolo_arb = edu("Arbitraggio batteria (energy arbitrage)", "Strategia di uno storage: CARICA (buy) nelle ore più economiche (tipicamente notte/F3) e SCARICA (sell) nelle ore di punta (F1). Il ricavo giornaliero dipende dallo spread max-min del giorno e dall'efficienza round-trip: ogni MWh scaricato è costato (prezzo_min / efficienza) in fase di carica.")
        st.markdown(f"**{titolo_arb}**: stima del ricavo di uno storage con 1 ciclo/giorno (carica all'ora più economica, scarica a quella più cara).", unsafe_allow_html=True)

        b1, b2, b3 = st.columns(3)
        with b1:
            cap_mwh = st.number_input("Capacità utile (MWh)", min_value=0.5, value=4.0, step=0.5,
                                      help="Energia immagazzinabile per ciclo completo.")
        with b2:
            pot_mw = st.number_input("Potenza (MW)", min_value=0.5, value=2.0, step=0.5,
                                     help="Potenza di carica/scarica: limita l'energia movimentabile nella finestra di prezzo.")
        with b3:
            eff = st.number_input("Efficienza round-trip (%)", min_value=50.0, max_value=100.0, value=85.0, step=1.0,
                                  help="Perdite di conversione: per scaricare 1 MWh devi averne caricati 1/efficienza.") / 100.0

        # 1 ciclo/giorno: energia movimentabile limitata da capacità e potenza (finestra 2h carica+scarica)
        e_ciclo = min(cap_mwh, pot_mw * 2.0)
        df_b = pd.DataFrame({"giorno": prezzi.index.date, "prezzo": prezzi.values.astype(float)})
        righe_b = []
        for giorno, grp in df_b.groupby("giorno"):
            if len(grp) < 4:
                continue  # giorni parziali ai bordi del periodo
            p_min, p_max = float(grp["prezzo"].min()), float(grp["prezzo"].max())
            spread = p_max - p_min / eff
            ricavo = max(0.0, spread) * e_ciclo
            righe_b.append({"Giorno": giorno, "Min (€/MWh)": round(p_min, 2), "Max (€/MWh)": round(p_max, 2),
                            "Spread netto (€/MWh)": round(max(0.0, spread), 2), "Ricavo (€)": round(ricavo, 2)})

        if not righe_b:
            st.warning("Dati insufficienti per la stima (servono giorni con almeno 4 ore).")
        else:
            df_arb = pd.DataFrame(righe_b)
            tot = float(df_arb["Ricavo (€)"].sum())
            medio_g = float(df_arb["Ricavo (€)"].mean())
            best = df_arb.loc[df_arb["Ricavo (€)"].idxmax()]
            giorni_ok = int((df_arb["Ricavo (€)"] > 0).sum())

            st.caption(f"Modello: 1 ciclo/giorno, energia per ciclo = min(capacità, potenza × 2h) = {e_ciclo:.1f} MWh. "
                       f"Il ciclo avviene solo se lo spread copre le perdite di efficienza.")
            a1, a2, a3, a4 = st.columns(4)
            render_kpi("Ricavo totale periodo (€)", f"{tot:,.0f}", a1)
            render_kpi("Ricavo medio/giorno (€)", f"{medio_g:,.1f}", a2)
            render_kpi("Miglior giorno (€)", f"{best['Ricavo (€)']:,.0f}", a3)
            render_kpi("Giorni profittevoli", f"{giorni_ok}/{len(df_arb)} ({giorni_ok/len(df_arb)*100:.0f} %)", a4)
            st.caption(f"📅 Miglior giorno: {best['Giorno'].strftime('%d/%m/%Y')} — min {best['Min (€/MWh)']:.0f} €/MWh → max {best['Max (€/MWh)']:.0f} €/MWh.")

            fig_arb = go.Figure()
            fig_arb.add_trace(go.Bar(
                x=df_arb["Giorno"], y=df_arb["Ricavo (€)"],
                marker_color=np.where(df_arb["Ricavo (€)"] > 0, "#10B981", "#EF4444"),
                name="Ricavo giornaliero (€)",
                hovertemplate="Giorno: %{x}<br>Ricavo: %{y:,.0f} €<extra></extra>",
            ))
            fig_arb.update_layout(template="plotly_dark", height=380,
                                  title=f"Ricavo giornaliero da arbitraggio (totale {tot:,.0f} € nel periodo)",
                                  xaxis_title="Giorno", yaxis_title="Ricavo (€)")
            st.plotly_chart(fig_arb, use_container_width=True)

            st.markdown("**Top 5 giorni per ricavo**")
            st.dataframe(df_arb.sort_values("Ricavo (€)", ascending=False).head(5),
                         use_container_width=True, hide_index=True)
            st.download_button(
                "⬇️ Esporta arbitraggio (CSV)",
                df_arb.to_csv(index=False).encode("utf-8"),
                file_name=f"battery_arbitrage_{d0}_{d1}.csv",
                mime="text/csv",
                help="Scarica la tabella giornaliera min/max/spread/ricavo.",
            )

    with tab7:
        titolo_bp = edu("Base/Peak mensile", "I prodotti standard del mercato elettrico: BASELOAD = prezzo medio di TUTTE le ore del mese; PEAK = media delle ore di punta (lun–ven 08:00–19:59); OFFPEAK = media delle restanti ore. Lo spread Peak–Offpeak mostra la premi al rischio di punta: è la metrica che guida acquisti/vendite a termine e il dimensionamento dei contratti PPA.")
        st.markdown(f"**{titolo_bp}**: medie mensili Base/Peak/Offpeak (definizione EPEX) e spread di punta.", unsafe_allow_html=True)
        df_bp = calcola_base_peak_mensile(prezzi)
        if df_bp.empty:
            st.warning("Dati insufficienti per l'analisi mensile.")
        else:
            ult_bp = df_bp.iloc[-1]
            b1, b2, b3, b4 = st.columns(4)
            render_kpi(f"Base ultimo mese ({ult_bp['Mese']})", f"{ult_bp['Base (€/MWh)']:,.2f} €/MWh", b1)
            render_kpi("Peak ultimo mese", f"{ult_bp['Peak (€/MWh)']:,.2f} €/MWh" if pd.notna(ult_bp['Peak (€/MWh)']) else "n/d", b2)
            render_kpi("Spread Peak–Offpeak", f"{ult_bp['Spread P-O (€/MWh)']:+,.2f} €/MWh" if pd.notna(ult_bp['Spread P-O (€/MWh)']) else "n/d", b3)
            render_kpi("Spread %", f"{ult_bp['Spread %']:+.1f} %" if pd.notna(ult_bp['Spread %']) else "n/d", b4)

            fig_bp = make_subplots(specs=[[{"secondary_y": True}]])
            for col, colore, nome in [("Base (€/MWh)", "#3b82f6", "Base"),
                                      ("Peak (€/MWh)", "#ef4444", "Peak"),
                                      ("Offpeak (€/MWh)", "#eab308", "Offpeak")]:
                fig_bp.add_trace(go.Bar(x=df_bp["Mese"], y=df_bp[col], name=nome,
                                        marker_color=colore, opacity=0.9,
                                        hovertemplate=f"{nome}: %{{y:,.1f}} €/MWh<extra></extra>"),
                                 secondary_y=False)
            fig_bp.add_trace(go.Scatter(x=df_bp["Mese"], y=df_bp["Spread P-O (€/MWh)"],
                                        name="Spread P-O", mode="lines+markers",
                                        line=dict(color="#10B981", width=2.5, dash="dash"),
                                        hovertemplate="Spread: %{y:,.1f} €/MWh<extra></extra>"),
                             secondary_y=True)
            fig_bp.update_layout(template="plotly_dark", height=400,
                                  title="Medie mensili Base/Peak/Offpeak + spread di punta",
                                  xaxis_title="Mese", barmode="group",
                                  legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            fig_bp.update_yaxes(title_text="Prezzo (€/MWh)", secondary_y=False)
            fig_bp.update_yaxes(title_text="Spread (€/MWh)", secondary_y=True)
            st.plotly_chart(fig_bp, use_container_width=True)

            st.dataframe(df_bp, use_container_width=True, hide_index=True)
            st.download_button(
                "⬇️ Esporta Base/Peak mensile (CSV)",
                df_bp.to_csv(index=False).encode("utf-8"),
                file_name=f"base_peak_mensile_{d0}_{d1}.csv",
                mime="text/csv",
                help="Scarica la tabella mensile Base/Peak/Offpeak/spread.",
            )

    with tab8:
        titolo_cf = edu("Simulatore costo fornitura", "Stima il costo di una fornitura elettrica alle quotazioni spot del periodo: imposti la potenza (MW) prelevata in ciascuna fascia F1/F2/F3 e la dashboard calcola costo totale, energia prelevata e prezzo medio ponderato. Utile per quotare contratti, confrontare profili di consumo e valutare se conviene spostare i carichi fuori punta.")
        st.markdown(f"**{titolo_cf}**: costo della fornitura = somma oraria (prezzo spot × potenza della fascia).", unsafe_allow_html=True)

        cf1, cf2, cf3, cf4 = st.columns(4)
        with cf1:
            mw_f1 = st.number_input("Potenza in F1 (MW)", min_value=0.0, value=1.0, step=0.5,
                                    help="Ore di punta: lun–ven 08:00–19:00.")
        with cf2:
            mw_f2 = st.number_input("Potenza in F2 (MW)", min_value=0.0, value=1.0, step=0.5,
                                    help="Ore intermedie: lun–ven 07:00–08:00 e 19:00–23:00, sab 07:00–23:00.")
        with cf3:
            mw_f3 = st.number_input("Potenza in F3 (MW)", min_value=0.0, value=1.0, step=0.5,
                                    help="Ore fuori punta: notti, domeniche e festivi.")
        with cf4:
            tariffa_flat = st.number_input("Tariffa flat di confronto (€/MWh)", min_value=0.0, value=95.0, step=1.0,
                                           help="Prezzo fisso di un'offerta concorrente: il simulatore mostra quanto si risparmia (o spende in più) con lo spot.")

        ris_cf = calcola_costo_fornitura(prezzi, mw_f1, mw_f2, mw_f3)
        if ris_cf["mwh"] == 0:
            st.warning("Imposta una potenza maggiore di zero in almeno una fascia per calcolare il costo.")
        else:
            costo_flat = ris_cf["mwh"] * tariffa_flat
            delta = ris_cf["totale"] - costo_flat
            delta_pct = delta / costo_flat * 100 if costo_flat != 0 else 0.0
            segno = "🟢" if delta < 0 else ("🔴" if delta > 0 else "⚪")

            c1, c2, c3, c4 = st.columns(4)
            render_kpi("Costo totale periodo (€)", f"{ris_cf['totale']:,.0f}", c1)
            render_kpi("Energia prelevata (MWh)", f"{ris_cf['mwh']:,.0f}", c2)
            render_kpi("Prezzo medio ponderato (€/MWh)", f"{ris_cf['ponderato']:,.2f}", c3)
            render_kpi(f"{segno} Delta vs tariffa flat", f"{delta:+,.0f} € ({delta_pct:+.1f} %)", c4)
            st.caption(f"Tariffa flat {tariffa_flat:,.2f} €/MWh su {ris_cf['mwh']:,.0f} MWh = {costo_flat:,.0f} €. "
                       f"Il prezzo medio ponderato è il costo diviso per l'energia: è il vero prezzo €/MWh pagato dal cliente.")

            st.markdown("**Costo giornaliero della fornitura**")
            df_cf_g = pd.DataFrame({"giorno": prezzi.index.date,
                                    "costo": (prezzi.values.astype(float)
                                              * prezzi.index.map(fascia_oraria).map({"F1": mw_f1, "F2": mw_f2, "F3": mw_f3}).to_numpy())})
            costo_g = df_cf_g.groupby("giorno")["costo"].sum()
            fig_cf = go.Figure()
            fig_cf.add_trace(go.Bar(
                x=costo_g.index, y=costo_g.values, name="Costo giornaliero (€)",
                marker_color="#10B981",
                hovertemplate="Giorno: %{x}<br>Costo: %{y:,.0f} €<extra></extra>",
            ))
            fig_cf.update_layout(template="plotly_dark", height=350,
                                 title=f"Costo giornaliero (totale {ris_cf['totale']:,.0f} € nel periodo)",
                                 xaxis_title="Giorno", yaxis_title="Costo (€)")
            st.plotly_chart(fig_cf, use_container_width=True)

            st.markdown("**Dettaglio per fascia oraria**")
            pf = ris_cf["per_fascia"].reset_index().rename(columns={
                "fascia": "Fascia", "ore": "Ore", "mwh": "MWh", "costo": "Costo (€)", "prezzo_medio": "Prezzo medio (€/MWh)"})
            pf["Costo (€)"] = pf["Costo (€)"].round(0)
            pf["Prezzo medio (€/MWh)"] = pf["Prezzo medio (€/MWh)"].round(2)
            pf["MWh"] = pf["MWh"].round(0)
            st.dataframe(pf, use_container_width=True, hide_index=True)
            st.download_button(
                "⬇️ Esporta costo fornitura (CSV)",
                pf.to_csv(index=False).encode("utf-8"),
                file_name=f"costo_fornitura_{d0}_{d1}.csv",
                mime="text/csv",
                help="Scarica il dettaglio per fascia oraria.",
            )

            titolo_dr = edu("Demand response: sposta carico da F1 a F3 (what-if)", "Parte dei consumi di punta (F1, ore care) viene spostata nelle ore fuori punta (F3, ore economiche). L'energia totale resta invariata: i MWh tolti dalla F1 vengono ripartiti sulle ore F3. Il simulatore ricalcola costo e prezzo medio ponderato: il risparmio è il business case per proporre al cliente un profilo di consumo ottimizzato.")
            st.markdown(f"**{titolo_dr}**: quanto si risparmia spostando parte dei consumi di punta in fuori punta?", unsafe_allow_html=True)
            shift_pct = st.slider("Quota del carico F1 spostata in F3 (%)", 0, 50, 0, step=5,
                                  help="Percentuale dell'energia F1 da spostare in F3: il profilo di potenza viene ricalcolato a energia totale invariata.")
            if shift_pct > 0:
                mw1s, mw3s = sposta_carico_f1_f3(prezzi, mw_f1, mw_f3, shift_pct)
                ris_s = calcola_costo_fornitura(prezzi, mw1s, mw_f2, mw3s)
                risparmio = ris_cf["totale"] - ris_s["totale"]
                pct_r = risparmio / ris_cf["totale"] * 100 if ris_cf["totale"] else 0.0
                s1, s2, s3 = st.columns(3)
                render_kpi("Costo con shift (€)", f"{ris_s['totale']:,.0f}", s1)
                render_kpi("Prezzo medio ponderato (€/MWh)", f"{ris_s['ponderato']:,.2f}", s2)
                segno_r = "🟢" if risparmio > 0 else ("🔴" if risparmio < 0 else "⚪")
                render_kpi(f"{segno_r} Risparmio stimato", f"{risparmio:+,.0f} € ({pct_r:+.1f} %)", s3)
                st.caption(f"Profilo shiftato: F1 {mw1s:.2f} MW, F2 {mw_f2:.2f} MW, F3 {mw3s:.2f} MW — "
                           f"energia totale {ris_s['mwh']:,.0f} MWh (invariata vs {ris_cf['mwh']:,.0f} MWh).")

    with tab9:
        titolo_mtm = edu("Mark-to-market dei contratti forward (hedging)", "Un contratto forward fissa OGGI il prezzo di una consegna futura. Il MtM dice quanto vale ORA quella copertura rispetto allo spot: se hai VENDUTO a 120 €/MWh e lo spot medio del periodo è stato 100, hai guadagnato 20 €/MWh (MtM positivo). Se hai ACQUISTATO a 120 e lo spot è stato 100, hai pagato più del mercato (MtM negativo). Qui il MtM è calcolato sullo spot del periodo selezionato: è il P&L 'realizzato' della copertura. Utile per valutare se le coperture in portafoglio hanno protetto o penalizzato rispetto allo spot.")
        st.markdown(f"**{titolo_mtm}**: P&L realizzato delle coperture a prezzo fisso contro lo spot del periodo.", unsafe_allow_html=True)

        n_contr = st.slider("Numero di contratti", 1, 4, 1, step=1,
                            help="Definisci fino a 4 contratti forward: lato, prezzo fisso, volume e finestra di consegna.")
        contratti = []
        cols_mtm = st.columns(n_contr)
        for i, col_m in enumerate(cols_mtm):
            with col_m:
                nome_m = st.text_input("Nome", f"Contratto {i+1}", key=f"mtm_nome_{i}")
                lato_m = st.selectbox("Lato", ["Vendita", "Acquisto"], key=f"mtm_lato_{i}",
                                      help="Vendita = hai venduto a termine (guadagni se lo spot scende); Acquisto = hai comprato a termine (guadagni se lo spot sale).")
                fisso_m = st.number_input("Prezzo fisso (€/MWh)", value=round(float(prezzi.mean()), 1),
                                          step=1.0, key=f"mtm_fisso_{i}")
                mw_m = st.number_input("Volume (MW)", min_value=0.0, value=1.0, step=0.5, key=f"mtm_mw_{i}")
                di_m = st.date_input("Inizio consegna", d0, min_value=d0, max_value=d1, key=f"mtm_di_{i}")
                df_m = st.date_input("Fine consegna", d1, min_value=d0, max_value=d1, key=f"mtm_df_{i}")
                if di_m > df_m:
                    st.warning(f"⚠️ {nome_m}: inizio consegna dopo la fine — contratto escluso dal calcolo.")
                else:
                    contratti.append({"nome": nome_m, "lato": lato_m, "prezzo_fisso": fisso_m,
                                      "mw": mw_m, "inizio": di_m, "fine": df_m})

        df_mtm, cumul_mtm = calcola_mtm(prezzi, contratti)
        if df_mtm.empty:
            st.info("Nessun contratto valido: controlla le date di consegna.")
        else:
            tot_mtm = float(df_mtm["MtM (€)"].sum())
            n_pos = int((df_mtm["MtM (€)"] > 0).sum())
            best_m = df_mtm.loc[df_mtm["MtM (€)"].idxmax()]
            worst_m = df_mtm.loc[df_mtm["MtM (€)"].idxmin()]
            m1, m2, m3, m4 = st.columns(4)
            segno_t = "🟢" if tot_mtm > 0 else ("🔴" if tot_mtm < 0 else "⚪")
            render_kpi(f"{segno_t} MtM totale (€)", f"{tot_mtm:+,.0f}", m1)
            render_kpi("Contratti in utile", f"{n_pos}/{len(df_mtm)}", m2)
            render_kpi("Miglior contratto", f"{best_m['Nome']}: {best_m['MtM (€)']:+,.0f} €", m3)
            render_kpi("Peggior contratto", f"{worst_m['Nome']}: {worst_m['MtM (€)']:+,.0f} €", m4)
            st.caption("MtM = segno(lato) × (prezzo fisso − prezzo medio realizzato) × volume × ore di consegna. "
                       "Positivo = la copertura ha battuto lo spot.")

            fig_mtm = go.Figure()
            fig_mtm.add_trace(go.Scatter(
                x=cumul_mtm.index, y=cumul_mtm.values, mode='lines', name="MtM cumulato (€)",
                line=dict(color='#10B981' if tot_mtm >= 0 else '#ef4444', width=2),
                fill='tozeroy', fillcolor='rgba(16,185,129,0.15)' if tot_mtm >= 0 else 'rgba(239,68,68,0.15)',
                hovertemplate="Data: %{x}<br>MtM cumulato: %{y:,.0f} €<extra></extra>",
            ))
            fig_mtm.add_hline(y=0, line_dash="dot", line_color="#9ca3af")
            fig_mtm.update_layout(template="plotly_dark", height=350,
                                  title=f"MtM cumulato dei contratti (totale {tot_mtm:+,.0f} €)",
                                  xaxis_title="Data e Ora", yaxis_title="MtM cumulato (€)")
            st.plotly_chart(fig_mtm, use_container_width=True)

            st.markdown("**Dettaglio contratti**")
            st.dataframe(df_mtm, use_container_width=True, hide_index=True)
            st.download_button(
                "⬇️ Esporta MtM hedging (CSV)",
                df_mtm.to_csv(index=False).encode("utf-8"),
                file_name=f"mtm_hedging_{d0}_{d1}.csv",
                mime="text/csv",
                help="Scarica il dettaglio per contratto: lato, prezzo fisso, volume, ore delivery, prezzo medio realizzato e MtM.",
            )

    with tab10:
        titolo_ss = edu("Spark spread (margine della centrale a gas)", "Lo SPARK SPREAD è il margine lordo di una centrale elettrica a gas: prezzo dell'elettricità MENO il costo del gas (prezzo_gas / efficienza) MENO il costo della CO2 (prezzo_CO2 × fattore di emissione). Spark spread positivo = la centrale gira in UTILE (meglio produrre che comprare sul mercato); negativo = conviene fermarla e comprare lo spot. È la metrica che decide il dispatch delle centrali termoelettriche e la convenienza delle coperture gas-power.")
        st.markdown(f"**{titolo_ss}**: margine orario di una centrale a gas contro lo spot del periodo.", unsafe_allow_html=True)

        s1, s2, s3, s4 = st.columns(4)
        with s1:
            gas_p = st.number_input("Prezzo gas (€/MWh termico)", min_value=0.0, value=35.0, step=1.0,
                                    help="Prezzo del gas combustibile (TTF o PSV).")
        with s2:
            eff_p = st.number_input("Efficienza centrale (%)", min_value=10.0, max_value=65.0, value=55.0, step=1.0,
                                    help="Efficienza elettrica: un CCGT moderno sta intorno al 55-60%.")
        with s3:
            co2_p = st.number_input("Prezzo CO2 (€/t)", min_value=0.0, value=70.0, step=1.0,
                                    help="Prezzo delle quote EUA (EU ETS).")
        with s4:
            ef_p = st.number_input("Fattore emissivo (tCO2/MWh el.)", min_value=0.0, max_value=1.0, value=0.4, step=0.05,
                                   help="Default 0.4 per un ciclo combinato (CCGT).")

        ss, ss_stats = calcola_spark_spread(prezzi, gas_p, eff_p, co2_p, ef_p)
        costo_fuel = gas_p / max(1.0, eff_p) * 100 + co2_p * ef_p
        st.caption(f"Costo marginale stimato della centrale: gas {gas_p/max(1.0, eff_p)*100:,.1f} €/MWh + CO2 {co2_p*ef_p:,.1f} €/MWh = **{costo_fuel:,.1f} €/MWh** — le ore con spot sopra questo livello hanno spark spread positivo.")

        k1, k2, k3, k4 = st.columns(4)
        segno_ss = "🟢" if ss_stats["medio"] > 0 else ("🔴" if ss_stats["medio"] < 0 else "⚪")
        render_kpi(f"{segno_ss} Spark spread medio (€/MWh)", f"{ss_stats['medio']:+,.2f}", k1)
        render_kpi("Ore in utile (%)", f"{ss_stats['pct_ore_positive']:.1f} %", k2)
        if ss_stats["best_ora"] is not None:
            render_kpi("Miglior ora", f"{ss_stats['best_val']:+,.1f} €/MWh", k3)
            render_kpi("Peggior ora", f"{ss_stats['worst_val']:+,.1f} €/MWh", k4)
            st.caption(f"📅 Miglior ora: {ss_stats['best_ora'].strftime('%d/%m/%Y %H:%M')} — Peggior ora: {ss_stats['worst_ora'].strftime('%d/%m/%Y %H:%M')}.")

        fig_ss = go.Figure()
        pos = ss[ss >= 0]
        neg = ss[ss < 0]
        fig_ss.add_trace(go.Bar(x=pos.index, y=pos.values, name="Spread ≥ 0",
                                marker_color="#10B981",
                                hovertemplate="Ora: %{x}<br>Spread: %{y:+,.1f} €/MWh<extra></extra>"))
        fig_ss.add_trace(go.Bar(x=neg.index, y=neg.values, name="Spread < 0",
                                marker_color="#EF4444",
                                hovertemplate="Ora: %{x}<br>Spread: %{y:+,.1f} €/MWh<extra></extra>"))
        fig_ss.add_hline(y=0, line_dash="dot", line_color="#9ca3af")
        fig_ss.update_layout(template="plotly_dark", height=380, barmode="overlay",
                             title=f"Spark spread orario (medio {ss_stats['medio']:+,.2f} €/MWh)",
                             xaxis_title="Data e Ora", yaxis_title="Spark spread (€/MWh)")
        st.plotly_chart(fig_ss, use_container_width=True)

        df_ss = pd.DataFrame({"Data e Ora": ss.index.strftime("%d/%m/%Y %H:%M"),
                              "Prezzo spot (€/MWh)": np.round(prezzi.values.astype(float), 2),
                              "Spark spread (€/MWh)": np.round(ss.values, 2)})
        st.markdown("**Top 5 ore per spark spread**")
        st.dataframe(df_ss.sort_values("Spark spread (€/MWh)", ascending=False).head(5),
                     use_container_width=True, hide_index=True)
        st.download_button(
            "⬇️ Esporta spark spread (CSV)",
            df_ss.to_csv(index=False).encode("utf-8"),
            file_name=f"spark_spread_{d0}_{d1}.csv",
            mime="text/csv",
            help="Scarica la serie oraria: prezzo spot e spark spread con i parametri impostati.",
        )

    with tab11:
        titolo_sh = edu("Shaping della curva forward", "Lo SHAPING trasforma un prezzo forward FLAT (es. un annuale quotato 95 €/MWh) in una curva mensile e oraria che riflette la stagionalità storica: i mesi invernali (domanda alta, prezzi alti) quotano sopra il flat, i mesi estivi sotto. Fattore mensile = media storica del mese / media totale; il prezzo shaped del mese = forward × fattore, rinormalizzato per ore così che la media ponderata riproduca esattamente il forward. È lo strumento con cui il desk quota contratti mensili/trimestrali e profili di consumo strutturati partendo da un unico prezzo annuale.")
        st.markdown(f"**{titolo_sh}**: da un forward flat annuale a una curva mensile/oraria che segue la stagionalità storica dello spot.", unsafe_allow_html=True)

        shape = calcola_shape_fattori(prezzi)
        f_m = shape["mensile"]
        mesi_vuoti = [m for m in range(1, 13) if pd.isna(f_m.loc[m])]
        if mesi_vuoti:
            nomi_m = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
            st.warning(f"⚠️ Storia insufficiente per i mesi {', '.join(nomi_m[m-1] for m in mesi_vuoti)}: usato fattore neutro 1.0 (prezzo flat). Allunga il periodo per una stagionalità affidabile.")

        sh1, sh2 = st.columns(2)
        with sh1:
            fwd = st.number_input("Prezzo forward annuo flat (€/MWh)", min_value=0.0,
                                  value=round(float(prezzi.mean()), 1), step=1.0,
                                  help="Prezzo quotato per il baseload annuale (es. da broker screen o EEX).")
        with sh2:
            anno_c = st.number_input("Anno di consegna", min_value=2026, max_value=2040,
                                     value=datetime.date.today().year + 1, step=1,
                                     help="Serve per contare le ore di ciascun mese (anni bisestili inclusi).")

        ore_m = {m: calendar.monthrange(int(anno_c), m)[1] * 24 for m in range(1, 13)}
        mesi_shape = shaped_mensile(fwd, f_m, ore_m)
        nomi_mesi = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
                     "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]
        df_shape = pd.DataFrame({
            "Mese": [nomi_mesi[m - 1] for m in range(1, 13)],
            "Ore": [ore_m[m] for m in range(1, 13)],
            "Fattore stagionale": f_m.reindex(range(1, 13)).fillna(1.0).round(3).values,
            "Prezzo shaped (€/MWh)": mesi_shape.round(2).values,
        })

        mese_max = df_shape.loc[df_shape["Prezzo shaped (€/MWh)"].idxmax()]
        mese_min = df_shape.loc[df_shape["Prezzo shaped (€/MWh)"].idxmin()]
        ampiezza = (mese_max["Prezzo shaped (€/MWh)"] - mese_min["Prezzo shaped (€/MWh)"])
        wavg_check = float((mesi_shape * pd.Series(ore_m, index=range(1, 13))).sum() / sum(ore_m.values()))
        s1, s2, s3, s4 = st.columns(4)
        render_kpi(f"🔺 Mese più caro ({mese_max['Mese'][:3]})", f"{mese_max['Prezzo shaped (€/MWh)']:,.2f} €/MWh", s1)
        render_kpi(f"🔻 Mese più economico ({mese_min['Mese'][:3]})", f"{mese_min['Prezzo shaped (€/MWh)']:,.2f} €/MWh", s2)
        render_kpi("Ampiezza stagionale", f"{ampiezza:,.2f} €/MWh ({ampiezza/fwd*100 if fwd else 0:.1f} %)", s3)
        render_kpi("✓ Media ponderata (check)", f"{wavg_check:,.2f} €/MWh", s4)
        st.caption("Check: la media dei prezzi shaped pesata per le ore dei mesi riproduce il forward in input — la curva è arbitraggio-neutra rispetto al flat.")

        fig_sh = go.Figure()
        fig_sh.add_trace(go.Bar(
            x=df_shape["Mese"], y=df_shape["Prezzo shaped (€/MWh)"], name="Prezzo shaped",
            marker_color="#8b5cf6",
            hovertemplate="Mese: %{x}<br>Shaped: %{y:,.2f} €/MWh<br>Fattore: %{customdata:.3f}<extra></extra>",
            customdata=df_shape["Fattore stagionale"],
        ))
        fig_sh.add_hline(y=fwd, line_dash="dash", line_color="#eab308",
                         annotation_text=f"Forward flat: {fwd:.1f} €/MWh", annotation_position="top left")
        fig_sh.update_layout(template="plotly_dark", height=400,
                             title=f"Curva forward shaped {int(anno_c)} (da stagionalità {d0} → {d1})",
                             xaxis_title="Mese", yaxis_title="Prezzo (€/MWh)")
        st.plotly_chart(fig_sh, use_container_width=True)

        st.dataframe(df_shape, use_container_width=True, hide_index=True)
        st.download_button(
            "⬇️ Esporta curva shaped (CSV)",
            df_shape.to_csv(index=False).encode("utf-8"),
            file_name=f"curva_shaped_{int(anno_c)}.csv",
            mime="text/csv",
            help="Scarica la curva mensile shaped: mese, ore, fattore stagionale, prezzo.",
        )

        st.markdown("**Profilo orario shaped per mese**")
        mese_sel = st.selectbox("Mese", nomi_mesi, index=datetime.date.today().month - 1)
        m_num = nomi_mesi.index(mese_sel) + 1
        fh = shape["orario"].loc[m_num].astype(float)
        if fh.isna().all():
            st.info(f"Nessuna storia oraria per {mese_sel}: profilo piatto.")
            prof_h = np.full(24, mesi_shape.loc[m_num])
        else:
            fh = fh.fillna(1.0)
            fh = fh / fh.mean()  # rinormalizza: media dei 24 fattori = 1
            prof_h = mesi_shape.loc[m_num] * fh.values
        fig_ph = go.Figure()
        fig_ph.add_trace(go.Scatter(x=list(range(24)), y=prof_h, mode='lines+markers',
                                    name=f"Profilo {mese_sel}", line=dict(color='#10B981', width=2.5)))
        fig_ph.add_hline(y=mesi_shape.loc[m_num], line_dash="dash", line_color="#9ca3af",
                         annotation_text=f"Media mese: {mesi_shape.loc[m_num]:.1f} €/MWh",
                         annotation_position="top left")
        fig_ph.update_layout(template="plotly_dark", height=350,
                             title=f"Profilo orario shaped — {mese_sel} {int(anno_c)}",
                             xaxis_title="Ora del giorno", yaxis_title="Prezzo (€/MWh)",
                             xaxis=dict(tickmode='linear', dtick=2))
        st.plotly_chart(fig_ph, use_container_width=True)

    with tab12:
        titolo_we = edu("Spread weekday/weekend", "Il mercato elettrico quota il WEEKEND come prodotto separato dal weekday: la domanda industriale crolla il sabato e la domenica e i prezzi sono tipicamente più bassi (SCONTO WEEKEND). Spread = media lun-ven MENO media sab-dom: positivo quando il weekend costa meno. Lo spread guida il pricing dei contratti con consumo weekend-intensivo e la quotazione dei prodotti Weekend Baseload.")
        st.markdown(f"**{titolo_we}**: medie settimanali lun-ven vs sab-dom e sconto weekend.", unsafe_allow_html=True)

        df_we = calcola_spread_weekend(prezzi)
        if df_we.empty:
            st.warning("Dati insufficienti per l'analisi settimanale.")
        else:
            df_we_v = df_we.dropna(subset=["Spread Wd-We (€/MWh)"])
            if df_we_v.empty:
                st.warning("Nessuna settimana completa (weekday + weekend) nel periodo.")
            else:
                sconto_m = float(df_we_v["Spread Wd-We (€/MWh)"].mean())
                sconto_p = float(df_we_v["Spread %"].mean())
                r_max = df_we_v.loc[df_we_v["Spread Wd-We (€/MWh)"].idxmax()]
                r_min = df_we_v.loc[df_we_v["Spread Wd-We (€/MWh)"].idxmin()]
                inv = int((df_we_v["Spread Wd-We (€/MWh)"] < 0).sum())
                w1, w2, w3, w4 = st.columns(4)
                render_kpi("Sconto medio weekend (€/MWh)", f"{sconto_m:+,.2f}", w1)
                render_kpi("Sconto medio weekend (%)", f"{sconto_p:+.1f} %", w2)
                render_kpi(f"🔺 Settimana max ({r_max['Settimana']})", f"{r_max['Spread Wd-We (€/MWh)']:+,.2f} €/MWh", w3)
                render_kpi(f"🔻 Settimana min ({r_min['Settimana']})", f"{r_min['Spread Wd-We (€/MWh)']:+,.2f} €/MWh", w4)
                st.caption(f"📅 Il weekend costa in media {sconto_m:+.2f} €/MWh ({sconto_p:+.1f} %) rispetto al weekday."
                           + (f" In {inv} settimane il weekend è risultato PIÙ CARO del weekday (spread negativo)." if inv else " Il weekend non è mai risultato più caro del weekday."))

                fig_we = go.Figure()
                fig_we.add_trace(go.Bar(
                    x=df_we_v["Settimana"], y=df_we_v["Weekday (€/MWh)"], name="Weekday (lun-ven)",
                    marker_color="#3b82f6",
                    hovertemplate="Settimana: %{x}<br>Weekday: %{y:,.2f} €/MWh<extra></extra>"))
                fig_we.add_trace(go.Bar(
                    x=df_we_v["Settimana"], y=df_we_v["Weekend (€/MWh)"], name="Weekend (sab-dom)",
                    marker_color="#10B981",
                    hovertemplate="Settimana: %{x}<br>Weekend: %{y:,.2f} €/MWh<extra></extra>"))
                fig_we.add_trace(go.Scatter(
                    x=df_we_v["Settimana"], y=df_we_v["Spread Wd-We (€/MWh)"], name="Spread Wd-We",
                    mode="lines+markers", line=dict(color="#eab308", width=2.5),
                    hovertemplate="Settimana: %{x}<br>Spread: %{y:+,.2f} €/MWh<extra></extra>"))
                fig_we.add_hline(y=0, line_dash="dot", line_color="#9ca3af")
                fig_we.update_layout(template="plotly_dark", height=420, barmode="group",
                                     title="Medie settimanali weekday vs weekend (sconto weekend)",
                                     xaxis_title="Settimana", yaxis_title="Prezzo (€/MWh)")
                st.plotly_chart(fig_we, use_container_width=True)

                st.dataframe(df_we, use_container_width=True, hide_index=True)
                st.download_button(
                    "⬇️ Esporta spread weekend (CSV)",
                    df_we.to_csv(index=False).encode("utf-8"),
                    file_name=f"spread_weekend_{d0}_{d1}.csv",
                    mime="text/csv",
                    help="Scarica la tabella settimanale: medie weekday/weekend, spread in €/MWh e in %.",
                )

    with tab13:
        titolo_pc = edu("Price capture", "Il PREZZO CATTURATO (capture price) è il prezzo medio a cui un impianto vende davvero la sua energia: media dei prezzi spot ponderata per le ore in cui l'impianto produce. Il TASSO DI CATTURA è il rapporto tra prezzo catturato e prezzo medio base: un solare che produce solo di giorno, quando i prezzi sono spesso più bassi, cattura tipicamente meno del 100%. Lo SCONTO CANNIBALIZZAZIONE è la differenza tra base e catturato: più è alta, più il profilo di produzione 'cannibalizza' il proprio valore. È la metrica chiave per valutare PPA e investimenti rinnovabili.")
        st.markdown(f"**{titolo_pc}**: quanto vale davvero un profilo solare sul mercato spot.", unsafe_allow_html=True)

        p_mw = st.number_input("☀️ Potenza di picco impianto solare (MW)", min_value=0.0, value=50.0, step=5.0,
                              help="Potenza nominale del parco fotovoltaico simulato (default 50 MW come Solare Muttsee del simulatore).")
        gen = profilo_solare(prezzi, p_mw)
        pc = calcola_price_capture(prezzi, gen)
        df_pm = pc["per_mese"]

        if p_mw <= 0 or df_pm.empty or pc["catturato"] is None:
            st.warning("Imposta una potenza di picco > 0 MW per calcolare il price capture.")
        else:
            tasso = pc["tasso_cattura"]
            tasso_txt = f"{tasso:.1f} %" if tasso is not None else "—"
            k1, k2, k3, k4 = st.columns(4)
            render_kpi("Prezzo catturato (€/MWh)", f"{pc['catturato']:,.2f}", k1)
            render_kpi("Tasso di cattura", tasso_txt, k2)
            render_kpi("Ricavo periodo (€)", f"{pc['ricavo']:,.0f}", k3)
            render_kpi("Sconto cannibalizzazione (€/MWh)", f"{pc['sconto_can']:+,.2f}", k4)
            st.caption(f"📊 Su {pc['mwh']:,.1f} MWh prodotti, il solare cattura in media {pc['catturato']:,.2f} €/MWh "
                       f"contro una media base di {pc['base_medio']:,.2f} €/MWh (tasso {tasso_txt}): "
                       f"lo sconto da profilo è di {pc['sconto_can']:+,.2f} €/MWh.")

            fig_pc = go.Figure()
            fig_pc.add_trace(go.Bar(
                x=df_pm["Mese"], y=df_pm["Catturato (€/MWh)"], name="Prezzo catturato",
                marker_color="#eab308",
                hovertemplate="Mese: %{x}<br>Catturato: %{y:,.2f} €/MWh<extra></extra>"))
            fig_pc.add_trace(go.Scatter(
                x=df_pm["Mese"], y=[pc["base_medio"]] * len(df_pm), name="Media base periodo",
                mode="lines", line=dict(color="#3b82f6", width=2, dash="dash"),
                hovertemplate="Base: %{y:,.2f} €/MWh<extra></extra>"))
            fig_pc.add_trace(go.Scatter(
                x=df_pm["Mese"], y=df_pm["Tasso %"], name="Tasso di cattura %", yaxis="y2",
                mode="lines+markers", line=dict(color="#10B981", width=2.5),
                hovertemplate="Mese: %{x}<br>Tasso: %{y:.1f} %<extra></extra>"))
            fig_pc.update_layout(template="plotly_dark", height=420,
                                 title="Price capture mensile del solare (vs media base)",
                                 xaxis_title="Mese", yaxis_title="Prezzo (€/MWh)",
                                 yaxis2=dict(title="Tasso di cattura (%)", overlaying="y", side="right"))
            st.plotly_chart(fig_pc, use_container_width=True)

            st.dataframe(df_pm, use_container_width=True, hide_index=True)
            st.download_button(
                "⬇️ Esporta price capture (CSV)",
                df_pm.to_csv(index=False).encode("utf-8"),
                file_name=f"price_capture_{d0}_{d1}.csv",
                mime="text/csv",
                help="Scarica la tabella mensile: MWh, ricavo, prezzo catturato e tasso di cattura.",
            )

# Footer
st.markdown("---")
st.markdown(f"<div style='text-align: center; color: #4B5563; font-size: 10px;'>Singularity OS V16 | Edu Mode: {st.session_state.edu_mode}</div>", unsafe_allow_html=True)
