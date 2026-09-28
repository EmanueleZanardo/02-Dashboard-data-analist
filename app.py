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
    UserWarning 'Converting to PeriodArray/Index representation will drop timezone information'.
    Serie vuota o con indice non datetime (es. nessun dato nel periodo) -> DataFrame
    vuoto con le colonne giuste, senza AttributeError su idx.tz/idx.weekday."""
    colonne = ["Mese", "Base (€/MWh)", "Peak (€/MWh)", "Offpeak (€/MWh)",
               "Spread P-O (€/MWh)", "Spread %", "Ore peak"]
    idx = prezzi.index
    if not isinstance(idx, pd.DatetimeIndex) or len(prezzi) == 0:
        return pd.DataFrame(columns=colonne)
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
    return pd.DataFrame(righe, columns=colonne)

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

def calcola_volatilita(prezzi):
    """Volatilita' realizzata giornaliera dello spot orario (€/MWh).
    prezzi: Series oraria in €/MWh. I prezzi spot possono essere 0 o negativi,
    quindi la vol si misura sulle VARIAZIONI ORARIE di prezzo (diff €/MWh),
    non sui log-return (indefiniti su valori non positivi).
    Vol giorno = deviazione standard (ddof=1) delle variazioni orarie entro il
    giorno solare: misura quanto il prezzo "sfarfalla" ora per ora. E' diversa
    dal VaR del tab Rischio & Durata, che guarda la DISTRIBUZIONE dei livelli
    di prezzo: qui si guarda la VELOCITA' dei movimenti, utile per trading
    intraday e timing di arbitraggio batteria.
    NaN-safe: le ore con prezzo NaN vengono ignorate; <3 ore valide ->
    strutture vuote con le colonne giuste.
    Ritorna dict con 'giornaliera' (DataFrame: Giorno, Prezzo medio (€/MWh),
    Range (€/MWh), Vol (€/MWh)), 'profilo_orario' (Series: std delle
    variazioni orarie per ora 0-23) e 'per_mese' (DataFrame: Mese,
    Vol media (€/MWh), Range medio (€/MWh))."""
    p = prezzi.astype(float).dropna()
    cols_g = ["Giorno", "Prezzo medio (€/MWh)", "Range (€/MWh)", "Vol (€/MWh)"]
    cols_m = ["Mese", "Vol media (€/MWh)", "Range medio (€/MWh)"]
    vuoto = {
        "giornaliera": pd.DataFrame({c: [] for c in cols_g}),
        "profilo_orario": pd.Series(dtype=float),
        "per_mese": pd.DataFrame({c: [] for c in cols_m}),
    }
    if len(p) < 3:
        return vuoto
    idxn = p.index.tz_localize(None) if p.index.tz is not None else p.index
    diff = p.diff().dropna()
    if diff.empty:
        return vuoto
    idxd = diff.index.tz_localize(None) if diff.index.tz is not None else diff.index
    vol_g = diff.groupby(idxd.date).std(ddof=1)
    g_p = p.groupby(idxn.date)
    medio_g, range_g = g_p.mean(), g_p.max() - g_p.min()
    giorni = sorted(set(vol_g.index) | set(medio_g.index))
    righe = [{
        "Giorno": str(g),
        "Prezzo medio (€/MWh)": None if pd.isna(medio_g.get(g)) else round(float(medio_g.get(g)), 2),
        "Range (€/MWh)": None if pd.isna(range_g.get(g)) else round(float(range_g.get(g)), 2),
        "Vol (€/MWh)": None if pd.isna(vol_g.get(g)) else round(float(vol_g.get(g)), 2),
    } for g in giorni]
    prof_h = diff.groupby(idxd.hour).std(ddof=1).reindex(range(24)).round(2)
    mesi = pd.Series([str(g)[:7] for g in giorni], index=giorni)
    v_g, r_g = vol_g.reindex(giorni), range_g.reindex(giorni)
    righe_m = [{
        "Mese": m,
        "Vol media (€/MWh)": (None if v_g[mesi == m].isna().all()
                              else round(float(v_g[mesi == m].mean()), 2)),
        "Range medio (€/MWh)": (None if r_g[mesi == m].isna().all()
                                else round(float(r_g[mesi == m].mean()), 2)),
    } for m in sorted(set(mesi))]
    return {"giornaliera": pd.DataFrame(righe, columns=cols_g),
            "profilo_orario": prof_h,
            "per_mese": pd.DataFrame(righe_m, columns=cols_m)}

def calcola_yoy(prezzi):
    """Confronto anno-su-anno del prezzo medio mensile (€/MWh).
    Raggruppa lo spot orario per (anno, mese solare) e calcola la media
    mensile; il delta YoY confronta ogni mese con lo stesso mese dell'anno
    precedente, in €/MWh e in %.
    Utile per: capire se il mercato e' strutturalmente piu' caro o piu'
    economico dello scorso anno al netto della stagionalita' (budget,
    negoziazione contratti annuali), e per validare le curve forward
    (il forward sconta gia' questo delta?).
    NaN-safe: ore con prezzo NaN ignorate; mesi senza ore valide -> None.
    Con < 2 anni di dati il delta non e' calcolabile: 'delta' torna vuoto
    con le colonne giuste.
    Ritorna dict con 'tabella' (DataFrame: Mese + una colonna per anno con
    la media mensile €/MWh), 'delta' (DataFrame: Mese, 'Δ €/MWh', 'Δ %'
    tra gli ultimi due anni disponibili) e 'anni' (lista anni ordinata)."""
    MESI = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu",
            "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
    cols_d = ["Mese", "Δ €/MWh", "Δ %"]
    vuoto = {"tabella": pd.DataFrame(columns=["Mese"]),
             "delta": pd.DataFrame(columns=cols_d), "anni": []}
    p = prezzi.astype(float).dropna()
    if p.empty:
        return vuoto
    idxn = p.index.tz_localize(None) if p.index.tz is not None else p.index
    med = p.groupby([idxn.year, idxn.month]).mean()
    anni = sorted({y for y, _ in med.index})
    righe = []
    for m in range(1, 13):
        riga = {"Mese": MESI[m - 1]}
        for y in anni:
            v = med.get((y, m), np.nan)
            riga[str(y)] = None if pd.isna(v) else round(float(v), 2)
        righe.append(riga)
    tabella = pd.DataFrame(righe, columns=["Mese"] + [str(y) for y in anni])
    righe_d = []
    if len(anni) >= 2:
        y0, y1 = anni[-2], anni[-1]
        for m in range(1, 13):
            a = med.get((y0, m), np.nan)
            b = med.get((y1, m), np.nan)
            if pd.isna(a) or pd.isna(b):
                righe_d.append({"Mese": MESI[m - 1], "Δ €/MWh": None, "Δ %": None})
            else:
                d = b - a
                righe_d.append({"Mese": MESI[m - 1], "Δ €/MWh": round(float(d), 2),
                                "Δ %": (None if a == 0 else round(float(d / a * 100), 1))})
    return {"tabella": tabella,
            "delta": pd.DataFrame(righe_d, columns=cols_d),
            "anni": anni}

def calcola_prezzi_negativi(prezzi, soglia=0.0):
    """Analisi delle ore con prezzo sotto soglia (default: < 0, prezzi negativi).
    I prezzi negativi nascono dall'eccesso di produzione rinnovabile (soprattutto
    solare a mezzogiorno in primavera/estate) e dai vincoli di dispacciamento:
    chi immette energia quando il prezzo e' negativo CI PAGA per farlo.
    Utile per: valutare la cannibalizzazione del valore per rinnovabili e
    accumulatori, dimensionare strategie di curtailment (spegnimento), e capire
    in quali mesi/ore si concentrano le ore negative.
    NaN-safe: ore con prezzo NaN ignorate; se nessuna ora e' sotto soglia,
    conteggi a 0 e DataFrame vuoti con le colonne giuste.
    Ritorna dict con 'n_ore', 'tot_ore', 'quota_pct', 'minimo', 'somma',
    'media_neg' (media dei prezzi sotto soglia), 'mensile' (DataFrame Mese,
    'Ore sotto soglia', 'Minimo €/MWh'), 'profilo_orario' (DataFrame Ora,
    'Ore sotto soglia', 'Media €/MWh') e 'top' (DataFrame delle peggiori ore:
    Data, Ora, 'Prezzo €/MWh', ordinate dal piu' negativo)."""
    MESI = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu",
            "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
    cols_m = ["Mese", "Ore sotto soglia", "Minimo €/MWh"]
    cols_o = ["Ora", "Ore sotto soglia", "Media €/MWh"]
    cols_t = ["Data", "Ora", "Prezzo €/MWh"]
    vuoto = {"n_ore": 0, "tot_ore": 0, "quota_pct": 0.0, "minimo": None,
             "somma": 0.0, "media_neg": None,
             "mensile": pd.DataFrame(columns=cols_m),
             "profilo_orario": pd.DataFrame(columns=cols_o),
             "top": pd.DataFrame(columns=cols_t)}
    p = prezzi.astype(float).dropna()
    if p.empty:
        return vuoto
    sotto = p[p < soglia]
    n = int(len(sotto))
    out = dict(vuoto)
    out["tot_ore"] = int(len(p))
    out["n_ore"] = n
    out["quota_pct"] = round(n / len(p) * 100, 2)
    if n == 0:
        return out
    out["minimo"] = round(float(sotto.min()), 2)
    out["somma"] = round(float(sotto.sum()), 2)
    out["media_neg"] = round(float(sotto.mean()), 2)
    idxn = sotto.index.tz_localize(None) if sotto.index.tz is not None else sotto.index
    righe_m = []
    for m in range(1, 13):
        sel = sotto[(idxn.month == m)]
        righe_m.append({"Mese": MESI[m - 1],
                        "Ore sotto soglia": int(len(sel)),
                        "Minimo €/MWh": (None if sel.empty else round(float(sel.min()), 2))})
    out["mensile"] = pd.DataFrame(righe_m, columns=cols_m)
    righe_o = []
    for h in range(24):
        sel = sotto[(idxn.hour == h)]
        righe_o.append({"Ora": f"{h:02d}:00",
                        "Ore sotto soglia": int(len(sel)),
                        "Media €/MWh": (None if sel.empty else round(float(sel.mean()), 2))})
    out["profilo_orario"] = pd.DataFrame(righe_o, columns=cols_o)
    ordinato = sotto.sort_values()
    idxo = ordinato.index.tz_localize(None) if ordinato.index.tz is not None else ordinato.index
    out["top"] = pd.DataFrame({
        "Data": idxo.strftime("%Y-%m-%d"),
        "Ora": idxo.strftime("%H:00"),
        "Prezzo €/MWh": [round(float(v), 2) for v in ordinato.values]},
        columns=cols_t).head(20)
    return out

def calcola_spread_intraday(prezzi):
    """Spread intra-day giornaliero (max - min) del prezzo orario.

    Lo spread intra-day e' la misura diretta del valore della flessibilita':
    una batteria o un carico flessibile comprano nelle ore di minimo e
    rivendono in quelle di massimo, catturando il range giornaliero.
    L'helper calcola per ogni giorno il range (prezzo max - prezzo min) e
    le ore in cui si verificano il minimo e il massimo, piu' l'aggregato
    mensile (range medio e massimo del mese).

    NaN-safe: ore con prezzo NaN ignorate; i giorni senza dati validi sono
    esclusi dal conteggio. Ritorna dict con 'n_giorni', 'range_medio'
    (media dei range giornalieri), 'range_max' (range massimo) e 'data_max'
    (giorno del range massimo, "YYYY-MM-DD"), 'ora_min_freq'/'ora_max_freq'
    (ora piu' frequente di minimo/massimo, formato "HH:00"),
    'giornaliero' (DataFrame Data, 'Range €/MWh', 'Ora min', 'Ora max',
    ordinato per data) e 'mensile' (DataFrame Mese, 'Range medio €/MWh',
    'Range max €/MWh')."""
    MESI = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu",
            "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
    cols_g = ["Data", "Range €/MWh", "Ora min", "Ora max"]
    cols_m = ["Mese", "Range medio €/MWh", "Range max €/MWh"]
    vuoto = {"n_giorni": 0, "range_medio": None, "range_max": None,
             "data_max": None, "ora_min_freq": None, "ora_max_freq": None,
             "giornaliero": pd.DataFrame(columns=cols_g),
             "mensile": pd.DataFrame(columns=cols_m)}
    p = prezzi.astype(float).dropna()
    if p.empty:
        return vuoto
    idxn = p.index.tz_localize(None) if p.index.tz is not None else p.index
    date = idxn.date
    righe = []
    for giorno in sorted(set(date)):
        mask = date == giorno
        vals = p.values[mask]
        if len(vals) == 0:
            continue
        i_min = int(np.argmin(vals))
        i_max = int(np.argmax(vals))
        ore_str = idxn[mask].strftime("%H:00")
        righe.append({"Data": giorno.strftime("%Y-%m-%d"),
                      "Range €/MWh": round(float(vals[i_max] - vals[i_min]), 2),
                      "Ora min": ore_str[i_min],
                      "Ora max": ore_str[i_max],
                      "_mese": giorno.month})
    out = dict(vuoto)
    if not righe:
        return out
    df = pd.DataFrame(righe).sort_values("Data").reset_index(drop=True)
    out["n_giorni"] = int(len(df))
    out["range_medio"] = round(float(df["Range €/MWh"].mean()), 2)
    i_max_r = int(df["Range €/MWh"].idxmax())
    out["range_max"] = float(df.loc[i_max_r, "Range €/MWh"])
    out["data_max"] = df.loc[i_max_r, "Data"]
    out["ora_min_freq"] = df["Ora min"].mode().iloc[0]
    out["ora_max_freq"] = df["Ora max"].mode().iloc[0]
    out["giornaliero"] = df.drop(columns=["_mese"])
    righe_m = []
    for m in range(1, 13):
        sel = df[df["_mese"] == m]
        righe_m.append({"Mese": MESI[m - 1],
                        "Range medio €/MWh": (None if sel.empty else round(float(sel["Range €/MWh"].mean()), 2)),
                        "Range max €/MWh": (None if sel.empty else round(float(sel["Range €/MWh"].max()), 2))})
    out["mensile"] = pd.DataFrame(righe_m, columns=cols_m)
    return out

def calcola_picchi(prezzi, soglia=200.0):
    """Analisi dei picchi di prezzo (ore con prezzo >= soglia, default 200 €/MWh).

    I picchi sono le ore di scarsita' del mercato: un impianto flessibile
    (peaker a gas, batteria, domanda interrompibile) guadagna proprio in
    quelle ore. L'helper calcola quante ore superano la soglia, la quota sul
    totale, il prezzo massimo con data/ora, le soglie percentile P99 e P99.5
    dell'intera serie, e l'analisi dei cluster (ore consecutive sopra soglia:
    un picco di 1 ora vale meno di un cluster di 4 ore per un peaker).
    Aggiunge aggregati mensili, profilo orario e le 20 ore piu' care.

    NaN-safe: ore con prezzo NaN ignorate; se nessuna ora supera la soglia,
    conteggi a 0 e DataFrame vuoti con le colonne giuste. Ritorna dict con
    'n_ore', 'tot_ore', 'quota_pct', 'massimo', 'data_max' (Data, Ora),
    'p99', 'p995' (soglie percentile sulla serie completa), 'cluster_max_ore'
    (durata massima di ore consecutive sopra soglia), 'n_cluster',
    'mensile' (DataFrame Mese, 'Ore sopra soglia', 'Massimo €/MWh'),
    'profilo_orario' (DataFrame Ora, 'Ore sopra soglia') e 'top'
    (DataFrame Data, Ora, 'Prezzo €/MWh', ordinate dal piu' caro)."""
    MESI = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu",
            "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
    cols_m = ["Mese", "Ore sopra soglia", "Massimo €/MWh"]
    cols_o = ["Ora", "Ore sopra soglia"]
    cols_t = ["Data", "Ora", "Prezzo €/MWh"]
    vuoto = {"n_ore": 0, "tot_ore": 0, "quota_pct": 0.0, "massimo": None,
             "data_max": None, "p99": None, "p995": None,
             "cluster_max_ore": 0, "n_cluster": 0,
             "mensile": pd.DataFrame(columns=cols_m),
             "profilo_orario": pd.DataFrame(columns=cols_o),
             "top": pd.DataFrame(columns=cols_t)}
    p = prezzi.astype(float).dropna()
    if p.empty:
        return vuoto
    out = dict(vuoto)
    out["tot_ore"] = int(len(p))
    out["p99"] = round(float(p.quantile(0.99)), 2)
    out["p995"] = round(float(p.quantile(0.995)), 2)
    sopra = p[p >= soglia]
    idxn = p.index.tz_localize(None) if p.index.tz is not None else p.index
    righe_m, righe_o = [], []
    for m in range(1, 13):
        righe_m.append({"Mese": MESI[m - 1], "Ore sopra soglia": 0,
                        "Massimo €/MWh": None})
    out["mensile"] = pd.DataFrame(righe_m, columns=cols_m)
    for h in range(24):
        righe_o.append({"Ora": f"{h:02d}:00", "Ore sopra soglia": 0})
    out["profilo_orario"] = pd.DataFrame(righe_o, columns=cols_o)
    if sopra.empty:
        return out
    out["n_ore"] = int(len(sopra))
    out["quota_pct"] = round(len(sopra) / len(p) * 100, 2)
    i_max = int(np.argmax(sopra.values))
    out["massimo"] = round(float(sopra.values[i_max]), 2)
    ts_max = sopra.index[i_max]
    ts_max = ts_max.tz_localize(None) if ts_max.tz is not None else ts_max
    out["data_max"] = (ts_max.strftime("%Y-%m-%d"), ts_max.strftime("%H:00"))
    # Cluster: ore consecutive sopra soglia (differenze orarie dell'indice).
    sopra_ord = sopra.sort_index()
    diffs = sopra_ord.index.to_series().diff().dropna()
    ore_step = pd.Timedelta(hours=1)
    # Tolleranza: gap <= 1h + 1 minuto = stesso cluster (copre DST).
    confini = (diffs > ore_step + pd.Timedelta(minutes=1)).cumsum().tolist()
    if len(sopra_ord) == 1:
        confini = [0]
    else:
        confini = [0] + confini
    lunghezze = pd.Series(confini).value_counts()
    out["n_cluster"] = int(len(lunghezze))
    out["cluster_max_ore"] = int(lunghezze.max())
    idxs = sopra.index.tz_localize(None) if sopra.index.tz is not None else sopra.index
    righe_m = []
    for m in range(1, 13):
        sel = sopra[(idxs.month == m)]
        righe_m.append({"Mese": MESI[m - 1],
                        "Ore sopra soglia": int(len(sel)),
                        "Massimo €/MWh": (None if sel.empty else round(float(sel.max()), 2))})
    out["mensile"] = pd.DataFrame(righe_m, columns=cols_m)
    righe_o = []
    for h in range(24):
        sel = sopra[(idxs.hour == h)]
        righe_o.append({"Ora": f"{h:02d}:00", "Ore sopra soglia": int(len(sel))})
    out["profilo_orario"] = pd.DataFrame(righe_o, columns=cols_o)
    ord_desc = sopra.sort_values(ascending=False)
    idxo = ord_desc.index.tz_localize(None) if ord_desc.index.tz is not None else ord_desc.index
    out["top"] = pd.DataFrame({
        "Data": idxo.strftime("%Y-%m-%d"),
        "Ora": idxo.strftime("%H:00"),
        "Prezzo €/MWh": [round(float(v), 2) for v in ord_desc.values]},
        columns=cols_t).head(20)
    return out

def calcola_profilo_settimanale(prezzi, top_n=10):
    """Profilo settimanale tipo: prezzo medio per giorno-settimana x ora (7x24).

    La matrice giorno x ora e' lo strumento standard per pianificare i carichi
    flessibili: mostra dove l'energia costa di solito meno (tipicamente le notti
    del weekend) e dove di piu' (le serate feriali). A differenza del tab
    Weekend (media lun-ven vs sab-dom), qui ogni giorno ha il suo profilo
    orario completo, e le 'finestre' indicano le combinazioni giorno-ora piu'
    economiche del periodo.

    NaN-safe: ore con prezzo NaN ignorate; combinazioni giorno-ora senza dati
    (periodi parziali) restano NaN nella matrice e sono escluse dai min/max.
    Ritorna dict con 'n_ore' (ore valide), 'tot_ore', 'matrice' (DataFrame
    7x24 con indice nomi dei giorni e colonne 0-23, prezzi medi arrotondati),
    'media_giorno' (DataFrame Giorno, 'Prezzo €/MWh'), 'media_ora' (DataFrame
    Ora, 'Prezzo €/MWh'), 'giorno_min'/'giorno_max' (nome, valore),
    'ora_min'/'ora_max' (ora, valore), 'coppia_min'/'coppia_max'
    (nome giorno, ora, valore), 'ampiezza' (max - min delle medie di matrice)
    e 'finestre' (DataFrame Giorno, Ora, 'Prezzo €/MWh' con le top_n
    combinazioni piu' economiche)."""
    GIORNI = ["Lunedì", "Martedì", "Mercoledì", "Giovedì",
              "Venerdì", "Sabato", "Domenica"]
    cols_mg = ["Giorno", "Prezzo €/MWh"]
    cols_mo = ["Ora", "Prezzo €/MWh"]
    cols_f = ["Giorno", "Ora", "Prezzo €/MWh"]
    vuoto = {"n_ore": 0, "tot_ore": 0,
             "matrice": pd.DataFrame(index=GIORNI, columns=list(range(24))),
             "media_giorno": pd.DataFrame(columns=cols_mg),
             "media_ora": pd.DataFrame(columns=cols_mo),
             "giorno_min": None, "giorno_max": None,
             "ora_min": None, "ora_max": None,
             "coppia_min": None, "coppia_max": None,
             "ampiezza": None,
             "finestre": pd.DataFrame(columns=cols_f)}
    p = prezzi.astype(float).dropna()
    out = dict(vuoto)
    if p.empty:
        return out
    out["tot_ore"] = int(len(p))
    idxn = p.index.tz_localize(None) if p.index.tz is not None else p.index
    df = pd.DataFrame({"wd": idxn.weekday, "ora": idxn.hour,
                       "prezzo": p.values})
    out["n_ore"] = int(len(df))
    mat = (df.groupby(["wd", "ora"])["prezzo"].mean()
             .unstack("ora").reindex(index=range(7), columns=range(24))
             .round(2))
    mat.index = GIORNI
    out["matrice"] = mat
    s = mat.stack()
    if s.empty:
        return out
    out["ampiezza"] = round(float(s.max() - s.min()), 2)
    i_min, i_max = s.idxmin(), s.idxmax()
    out["coppia_min"] = (i_min[0], int(i_min[1]), round(float(s.loc[i_min]), 2))
    out["coppia_max"] = (i_max[0], int(i_max[1]), round(float(s.loc[i_max]), 2))
    mg = mat.mean(axis=1, skipna=True).round(2)
    mo = mat.mean(axis=0, skipna=True).round(2)
    out["media_giorno"] = (pd.DataFrame({"Giorno": mg.index,
                                        "Prezzo €/MWh": mg.values})
                           .reset_index(drop=True))
    out["media_ora"] = (pd.DataFrame({"Ora": mo.index,
                                      "Prezzo €/MWh": mo.values})
                        .reset_index(drop=True))
    gm, gx = mg.idxmin(), mg.idxmax()
    out["giorno_min"] = (gm, round(float(mg.loc[gm]), 2))
    out["giorno_max"] = (gx, round(float(mg.loc[gx]), 2))
    om, ox = int(mo.idxmin()), int(mo.idxmax())
    out["ora_min"] = (om, round(float(mo.loc[om]), 2))
    out["ora_max"] = (ox, round(float(mo.loc[ox]), 2))
    top = s.sort_values().head(max(1, int(top_n)))
    out["finestre"] = (pd.DataFrame(
        [{"Giorno": ix[0], "Ora": f"{int(ix[1]):02d}:00",
          "Prezzo €/MWh": round(float(v), 2)}
         for ix, v in top.items()], columns=cols_f)
        .reset_index(drop=True))
    return out

def calcola_curva_durata(prezzi, soglia=None):
    """Curva di durata (price duration curve): prezzi orari ordinati in modo
    decrescente, con l'asse x = numero di ore cumulative.

    E' lo strumento standard per leggere la distribuzione dei prezzi senza
    guardare le serie temporali: la parte sinistra mostra per quante ore
    l'energia e' costata cara (picchi), la parte destra per quante ore e'
    costata poco (valli). I percentili P95/P50/P5 indicano i livelli di
    prezzo superati rispettivamente dal 5%, 50% e 95% delle ore: P95 misura
    l'esposizione ai picchi, P50 e' il prezzo mediano, P5 il pavimento. La
    media del 10% di ore piu' care e del 10% piu' economiche misura
    l'ampiezza della distribuzione e serve per valutazioni di VaR
    semplificato e per dimensionare coperture e storage.

    NaN-safe: ore con prezzo NaN ignorate. Ritorna dict con 'n_ore',
    'tot_ore', 'curva' (DataFrame 'Ore cumulative', 'Prezzo €/MWh' in
    ordine decrescente), 'p95'/'p50'/'p5' (prezzi ai percentili 95/50/5),
    'ore_sopra_p95' (ore con prezzo > P95, circa il 5% del totale),
    'media_top10'/'media_bottom10' (media del 10% di ore piu' care /
    piu' economiche), 'decili' (DataFrame 'Decile', 'Prezzo €/MWh',
    'Ore cumulative') e 'ore_sopra_soglia' (None se soglia non data)."""
    cols_d = ["Decile", "Prezzo €/MWh", "Ore cumulative"]
    vuoto = {"n_ore": 0, "tot_ore": 0,
             "curva": pd.DataFrame(columns=["Ore cumulative", "Prezzo €/MWh"]),
             "p95": None, "p50": None, "p5": None,
             "ore_sopra_p95": 0, "media_top10": None, "media_bottom10": None,
             "decili": pd.DataFrame(columns=cols_d),
             "ore_sopra_soglia": None}
    p = prezzi.astype(float).dropna().sort_values(ascending=False)
    out = dict(vuoto)
    if p.empty:
        return out
    n = int(len(p))
    out["tot_ore"] = n
    out["n_ore"] = n
    out["curva"] = (pd.DataFrame(
        {"Ore cumulative": np.arange(1, n + 1),
         "Prezzo €/MWh": p.values.round(2)})
        .reset_index(drop=True))
    p95, p50, p5 = (round(float(p.quantile(q)), 2) for q in (0.95, 0.50, 0.05))
    out["p95"], out["p50"], out["p5"] = p95, p50, p5
    out["ore_sopra_p95"] = int((p > p95).sum())
    k = max(1, int(n * 0.1))
    out["media_top10"] = round(float(p.iloc[:k].mean()), 2)
    out["media_bottom10"] = round(float(p.iloc[-k:].mean()), 2)
    out["decili"] = (pd.DataFrame(
        [{"Decile": f"D{j}", "Prezzo €/MWh": round(float(p.quantile(j / 10)), 2),
          "Ore cumulative": int(j * n / 10)}
         for j in range(1, 11)], columns=cols_d)
        .reset_index(drop=True))
    if soglia is not None:
        out["ore_sopra_soglia"] = int((p > float(soglia)).sum())
    return out

def calcola_concentrazione_costo(prezzi, mw_f1, mw_f2, mw_f3):
    """Concentrazione del costo di fornitura nelle ore piu' care (curva di Lorenz del costo).

    Dato un profilo di carico (MW prelevati in ciascuna fascia F1/F2/F3), calcola
    il costo orario = prezzo spot x MW della fascia, ordina le ore per prezzo
    decrescente e cumula la quota di costo: mostra quanta parte della bolletta
    del periodo e' generata dalle ore piu' care. E' la metrica che motiva le
    coperture (hedging): se il 10% di ore piu' care genera il 40% del costo,
    coprire la coda destra riduce drasticamente il rischio di budget. A
    differenza del tab Curva durata (distribuzione dei PREZZI), qui pesa il
    profilo di CONSUMO del cliente.

    NaN-safe: ore con prezzo NaN ignorate. MW tutti a zero o serie vuota ->
    valori neutrali. Con prezzi negativi (costo orario < 0) le quote possono
    superare il 100% (documentato nel caption) e l'indice di Gini non e'
    definito (None), perche' la formula standard richiede valori non negativi.

    Ritorna dict con 'n_ore', 'mwh', 'totale' (costo €), 'quota_top10' /
    'quota_top5' (% del costo nel 10%/5% di ore piu' care, None se totale <= 0),
    'costo_top10' (€ nel 10% di ore piu' care), 'ore_50pct' (ore per coprire
    il 50% del costo, None se totale <= 0), 'gini' (0..1, None con costi
    negativi o totale <= 0), 'lorenz' (DataFrame 'Quota ore %', 'Quota costo %'
    cumulata sulle ore ordinate per prezzo decrescente) e 'decili' (DataFrame
    'Decile', 'Ore', 'Costo (€)', 'Quota costo %' per decile di prezzo;
    D1 = 10% di ore piu' care, D10 = 10% di ore piu' economiche)."""
    cols_l = ["Quota ore %", "Quota costo %"]
    cols_d = ["Decile", "Ore", "Costo (€)", "Quota costo %"]
    vuoto = {"n_ore": 0, "mwh": 0.0, "totale": 0.0,
             "quota_top10": None, "quota_top5": None, "costo_top10": 0.0,
             "ore_50pct": None, "gini": None,
             "lorenz": pd.DataFrame(columns=cols_l),
             "decili": pd.DataFrame(columns=cols_d)}
    p = prezzi.astype(float).dropna()
    out = dict(vuoto)
    if p.empty:
        return out
    mw_map = {"F1": float(mw_f1), "F2": float(mw_f2), "F3": float(mw_f3)}
    mw = p.index.map(fascia_oraria).map(mw_map).to_numpy(dtype=float)
    if (mw <= 0).all():
        return out
    costo = p.values * mw
    n = int(len(p))
    mwh = float(mw.sum())
    totale = float(costo.sum())
    out["n_ore"] = n
    out["mwh"] = round(mwh, 1)
    out["totale"] = round(totale, 2)
    order = np.argsort(-p.values, kind="stable")
    cs = costo[order]
    cum = np.cumsum(cs)
    q_ore = (np.arange(1, n + 1) / n * 100).round(1)
    q_costo = np.full(n, np.nan) if totale <= 0 else (cum / totale * 100).round(1)
    out["lorenz"] = (pd.DataFrame({"Quota ore %": q_ore, "Quota costo %": q_costo})
                     .reset_index(drop=True))
    k10 = max(1, int(n * 0.10))
    k5 = max(1, int(n * 0.05))
    out["costo_top10"] = round(float(cum[k10 - 1]), 2)
    if totale > 0:
        out["quota_top10"] = round(float(cum[k10 - 1] / totale * 100), 1)
        out["quota_top5"] = round(float(cum[k5 - 1] / totale * 100), 1)
        out["ore_50pct"] = int(min(n, np.searchsorted(cum, totale * 0.5) + 1))
    if totale > 0 and (costo >= 0).all():
        y = np.sort(costo)
        i = np.arange(1, n + 1, dtype=float)
        g = 2.0 * float(np.sum(i * y)) / (n * float(y.sum())) - (n + 1) / n
        out["gini"] = round(float(min(1.0, max(0.0, g))), 3)
    righe = []
    for j in range(10):
        a, b = int(j * n / 10), int((j + 1) * n / 10)
        c_dec = float(cs[a:b].sum())
        righe.append({"Decile": f"D{j + 1}",
                      "Ore": int(b - a),
                      "Costo (€)": round(c_dec, 2),
                      "Quota costo %": (round(c_dec / totale * 100, 1)
                                        if totale > 0 else None)})
    out["decili"] = pd.DataFrame(righe, columns=cols_d).reset_index(drop=True)
    return out

def calcola_shifting_carico(prezzi, mw_f1, mw_f2, mw_f3, pct):
    """Simulazione demand shifting: spostamento di una quota di energia dalle
    ore piu' care alle ore piu' economiche del periodo.

    Dato un profilo di carico (MW prelevati in ciascuna fascia F1/F2/F3) e una
    quota pct (%, 0..50, valori oltre vengono tagliati a 50), identifica le
    'ore fonte': le ore piu' care per COSTO orario (prezzo x MW) fino a
    cumulare pct% dei MWh totali. Gli stessi MWh vengono 'ricaricati' nelle
    'ore destinazione': le ore con prezzo €/MWh piu' basso del periodo,
    escluse le ore fonte, fino allo stesso ammontare di MWh. Il risparmio
    stimato e' (costo delle ore fonte) - (costo delle stesse MWh nelle ore
    destinazione): misura il valore economico della flessibilita' (demand
    response / load shifting) senza cambiare il consumo totale.

    NaN-safe: ore con prezzo NaN ignorate. MW tutti a zero o serie vuota ->
    valori neutrali. Con prezzi negativi le ore destinazione a prezzo
    negativo generano ricavo invece di costo (risparmio > costo fonte):
    documentato nel caption del tab.

    Ritorna dict con 'n_ore', 'mwh', 'totale' (costo € senza shifting),
    'pct' (quota effettiva 0..50), 'mwh_spostati', 'ore_fonte',
    'ore_dest', 'costo_fonte', 'costo_dest', 'risparmio' (€),
    'risparmio_pct' (% sul totale, None se totale <= 0), 'costo_dopo' (€),
    'mensile' (DataFrame 'Mese', 'MWh spostati', 'Costo prima (€)',
    'Costo dopo (€)', 'Risparmio (€)', 'Risparmio %')."""
    cols_m = ["Mese", "MWh spostati", "Costo prima (€)", "Costo dopo (€)",
              "Risparmio (€)", "Risparmio %"]
    vuoto = {"n_ore": 0, "mwh": 0.0, "totale": 0.0, "pct": 0.0,
             "mwh_spostati": 0.0, "ore_fonte": 0, "ore_dest": 0,
             "costo_fonte": 0.0, "costo_dest": 0.0,
             "risparmio": 0.0, "risparmio_pct": None, "costo_dopo": 0.0,
             "mensile": pd.DataFrame(columns=cols_m)}
    p = prezzi.astype(float).dropna()
    out = dict(vuoto)
    if p.empty:
        return out
    mw_map = {"F1": float(mw_f1), "F2": float(mw_f2), "F3": float(mw_f3)}
    mw = p.index.map(fascia_oraria).map(mw_map).to_numpy(dtype=float)
    if (mw <= 0).all():
        return out
    pct = max(0.0, min(50.0, float(pct)))
    pv = p.values
    costo = pv * mw
    n = int(len(p))
    mwh = float(mw.sum())
    totale = float(costo.sum())
    out["n_ore"] = n
    out["mwh"] = round(mwh, 1)
    out["totale"] = round(totale, 2)
    out["pct"] = pct

    order_desc = np.argsort(-costo, kind="stable")
    idx_fonte = set(order_desc[: (int(np.searchsorted(np.cumsum(mw[order_desc]),
                           mwh * pct / 100.0, side="left") + 1)
                           if pct > 0 else 0)])
    if pct <= 0 or not idx_fonte:
        out["costo_dopo"] = round(totale, 2)
        out["risparmio_pct"] = 0.0 if totale > 0 else None
    else:
        ore_fonte = sorted(idx_fonte)
        mwh_mov = float(mw[ore_fonte].sum())
        costo_f = float(costo[ore_fonte].sum())
        resto = np.array([i for i in range(n) if i not in idx_fonte], dtype=int)
        order_asc = resto[np.argsort(pv[resto], kind="stable")]
        cum_r = np.cumsum(mw[order_asc])
        j = int(min(len(order_asc),
                    np.searchsorted(cum_r, mwh_mov, side="left") + 1))
        ore_dest = order_asc[:j]
        costo_d = float((pv[ore_dest] * mw[ore_dest]).sum())
        risp = costo_f - costo_d
        out["mwh_spostati"] = round(mwh_mov, 1)
        out["ore_fonte"] = int(len(ore_fonte))
        out["ore_dest"] = int(j)
        out["costo_fonte"] = round(costo_f, 2)
        out["costo_dest"] = round(costo_d, 2)
        out["risparmio"] = round(risp, 2)
        out["costo_dopo"] = round(totale - risp, 2)
        out["risparmio_pct"] = (round(risp / totale * 100, 1)
                                if totale > 0 else None)
    righe = []
    for mese, grp in p.groupby(p.index.strftime("%Y-%m")):
        mw_g = grp.index.map(fascia_oraria).map(mw_map).to_numpy(dtype=float)
        if (mw_g <= 0).all() or pct <= 0:
            righe.append({"Mese": mese, "MWh spostati": 0.0,
                          "Costo prima (€)": round(float((grp.values * mw_g).sum()), 2),
                          "Costo dopo (€)": round(float((grp.values * mw_g).sum()), 2),
                          "Risparmio (€)": 0.0, "Risparmio %": 0.0})
            continue
        c_g = grp.values * mw_g
        nn = len(grp)
        tgt = float(mw_g.sum()) * pct / 100.0
        od = np.argsort(-c_g, kind="stable")
        kk = int(min(nn, np.searchsorted(np.cumsum(mw_g[od]), tgt, side="left") + 1))
        f_idx = set(od[:kk])
        mm = float(mw_g[od[:kk]].sum())
        cf = float(c_g[od[:kk]].sum())
        rest = np.array([i for i in range(nn) if i not in f_idx], dtype=int)
        oa = rest[np.argsort(grp.values[rest], kind="stable")]
        jj = int(min(len(oa), np.searchsorted(np.cumsum(mw_g[oa]), mm, side="left") + 1))
        cd = float((grp.values[oa[:jj]] * mw_g[oa[:jj]]).sum())
        cp = float(c_g.sum())
        rs = cf - cd
        righe.append({"Mese": mese, "MWh spostati": round(mm, 1),
                      "Costo prima (€)": round(cp, 2),
                      "Costo dopo (€)": round(cp - rs, 2),
                      "Risparmio (€)": round(rs, 2),
                      "Risparmio %": (round(rs / cp * 100, 1) if cp > 0 else None)})
    out["mensile"] = pd.DataFrame(righe, columns=cols_m).reset_index(drop=True)
    return out

def calcola_finestre_ottimali(prezzi, mw_f1, mw_f2, mw_f3, finestra_ore):
    """Finestra di acquisto ottimale per giorno di calendario.

    Per ogni giorno con almeno W ore valide (prezzo non-NaN), trova la finestra
    di W ore consecutive che minimizza il costo di acquisto (prezzo x MW di
    fascia del compratore): la finestra in cui concentrare gli acquisti
    flessibili / i carichi spostabili. Lo sconto % misura quanto la finestra
    ottimale batte la media giornaliera: il valore del 'timing' di acquisto.

    NaN-safe. Giorni con MWh nulli vengono saltati. Sconto None quando la
    media giornaliera non e' positiva (es. prezzi negativi dominanti). W viene
    tagliato all'intervallo 1..24. A parita' di costo vince la finestra con
    ora di inizio piu' bassa (argmin stabile = deterministico).

    Ritorna dict con 'n_giorni', 'w' (finestra effettiva), 'prezzo_finestra'
    (media €/MWh pesata sui MWh delle finestre, None se 0 MWh),
    'sconto_pct' (media semplice degli sconti % giornalieri validi, None se
    nessun giorno valido), 'mwh_finestra', 'ora_moda' (ora di inizio piu'
    frequente, None se nessun giorno), 'giornaliero' (DataFrame 'Giorno',
    'Finestra', 'Ora inizio', 'MWh finestra', '€/MWh finestra',
    'Sconto vs media giorno %', 'Costo giorno (€)', 'MWh giorno'),
    'mensile' (DataFrame 'Mese', 'Giorni', 'MWh finestra', '€/MWh finestra',
    'Sconto medio %'), 'distrib_ore' (DataFrame 'Ora', 'Giorni')."""
    w = int(np.clip(int(finestra_ore or 0), 1, 24))
    cols_g = ["Giorno", "Finestra", "Ora inizio", "MWh finestra",
              "€/MWh finestra", "Sconto vs media giorno %",
              "Costo giorno (€)", "MWh giorno"]
    cols_m = ["Mese", "Giorni", "MWh finestra", "€/MWh finestra",
              "Sconto medio %"]
    vuoto = {"n_giorni": 0, "w": w, "prezzo_finestra": None,
             "sconto_pct": None, "mwh_finestra": 0.0, "ora_moda": None,
             "giornaliero": pd.DataFrame(columns=cols_g),
             "mensile": pd.DataFrame(columns=cols_m),
             "distrib_ore": pd.DataFrame({"Ora": range(24),
                                          "Giorni": [0] * 24})}
    p = prezzi.astype(float).dropna()
    out = dict(vuoto)
    if p.empty:
        return out
    mw_map = {"F1": float(mw_f1), "F2": float(mw_f2), "F3": float(mw_f3)}
    raw = []
    for giorno, grp in p.groupby(p.index.floor("D")):
        pv = grp.values
        mw = grp.index.map(fascia_oraria).map(mw_map).to_numpy(dtype=float)
        nn = len(grp)
        if nn < w or (mw <= 0).all():
            continue
        costo_orario = pv * mw
        kernel = np.ones(w)
        costo_w = np.convolve(costo_orario, kernel, mode="valid")
        mwh_w = np.convolve(mw, kernel, mode="valid")
        start = int(np.argmin(costo_w))
        mm = float(mwh_w[start])
        if mm <= 0:
            continue
        cw = float(costo_w[start])
        tot_mwh = float(mw.sum())
        tot_costo = float(costo_orario.sum())
        pm_win = cw / mm
        pm_gio = tot_costo / tot_mwh if tot_mwh > 0 else None
        sconto = ((1.0 - pm_win / pm_gio) * 100.0
                  if (pm_gio is not None and pm_gio > 0) else None)
        ts0 = grp.index[start]
        ore_inizio = [int(x.hour) for x in grp.index[start:start + w]]
        raw.append({"giorno": giorno, "inizio": int(ts0.hour),
                    "finestra": f"{ore_inizio[0]:02d}:00-{ore_inizio[-1] + 1:02d}:00"
                                if ore_inizio[-1] < 23
                                else f"{ore_inizio[0]:02d}:00-24:00",
                    "mwh_win": mm, "costo_win": cw, "sconto": sconto,
                    "tot_mwh": tot_mwh, "tot_costo": tot_costo})
    if not raw:
        return out
    righe = []
    for r in raw:
        pm_win = r["costo_win"] / r["mwh_win"]
        pm_gio = r["tot_costo"] / r["tot_mwh"] if r["tot_mwh"] > 0 else None
        righe.append({
            "Giorno": r["giorno"].strftime("%Y-%m-%d"),
            "Finestra": r["finestra"], "Ora inizio": r["inizio"],
            "MWh finestra": round(r["mwh_win"], 1),
            "€/MWh finestra": round(pm_win, 2),
            "Sconto vs media giorno %": (round(r["sconto"], 1)
                                         if r["sconto"] is not None else None),
            "Costo giorno (€)": round(r["tot_costo"], 2),
            "MWh giorno": round(r["tot_mwh"], 1)})
    out["giornaliero"] = pd.DataFrame(righe, columns=cols_g).reset_index(drop=True)
    tot_mwh_win = sum(r["mwh_win"] for r in raw)
    tot_costo_win = sum(r["costo_win"] for r in raw)
    out["n_giorni"] = len(raw)
    out["mwh_finestra"] = round(tot_mwh_win, 1)
    out["prezzo_finestra"] = (round(tot_costo_win / tot_mwh_win, 2)
                              if tot_mwh_win > 0 else None)
    sconti = [r["sconto"] for r in raw if r["sconto"] is not None]
    out["sconto_pct"] = round(sum(sconti) / len(sconti), 1) if sconti else None
    out["ora_moda"] = int(pd.Series([r["inizio"] for r in raw]).mode().iloc[0])
    conteggi = pd.Series([r["inizio"] for r in raw]).value_counts()
    out["distrib_ore"] = pd.DataFrame(
        {"Ora": range(24),
         "Giorni": [int(conteggi.get(h, 0)) for h in range(24)]})
    mr = {}
    for r in raw:
        mese = r["giorno"].strftime("%Y-%m")
        d = mr.setdefault(mese, {"giorni": 0, "mwh": 0.0, "costo": 0.0,
                                 "sconti": []})
        d["giorni"] += 1
        d["mwh"] += r["mwh_win"]
        d["costo"] += r["costo_win"]
        if r["sconto"] is not None:
            d["sconti"].append(r["sconto"])
    righe_m = []
    for mese in sorted(mr):
        d = mr[mese]
        righe_m.append({
            "Mese": mese, "Giorni": d["giorni"],
            "MWh finestra": round(d["mwh"], 1),
            "€/MWh finestra": (round(d["costo"] / d["mwh"], 2)
                               if d["mwh"] > 0 else None),
            "Sconto medio %": (round(sum(d["sconti"]) / len(d["sconti"]), 1)
                               if d["sconti"] else None)})
    out["mensile"] = pd.DataFrame(righe_m, columns=cols_m).reset_index(drop=True)
    return out


def calcola_stagionalita(prezzi):
    """Profilo stagionale mensile (seasonality) del prezzo spot orario.

    Raggruppa le ore per mese solare (gennaio..dicembre, tutti gli anni
    insieme) e calcola prezzo medio, mediano, minimo, massimo e deviazione
    standard. Il FATTORE STAGIONALE = media_mese / media_annuale: sopra 1 il
    mese e' strutturalmente piu' caro della media (tipicamente i mesi
    invernali, domanda alta e rinnovabili basse), sotto 1 piu' economico
    (tipicamente primavera/estate). L'ampiezza stagionale (fattore max -
    fattore min, in punti) misura quanto e' marcata la stagionalita'.

    Utile per: allocazione mensile del budget energia, negoziazione di
    contratti a prezzo fisso (il fixed sconta la stagionalita' attesa),
    timing degli acquisti su forward mensili e validazione delle curve
    forward (il forward deve riflettere questo profilo).

    NaN-safe: ore con prezzo NaN ignorate. Mesi senza ore valide sono
    omessi dalla tabella. Con media annuale <= 0 (prezzi negativi
    dominanti) il fattore stagionale e' None. Con meno di 2 mesi validi,
    mese_piu_caro/economico e ampiezza tornano None.

    Ritorna dict con 'mensile' (DataFrame: Mese, Ore, 'Media €/MWh',
    'Mediana €/MWh', 'Min €/MWh', 'Max €/MWh', 'Dev.std €/MWh',
    'Fattore stagionale'), 'media_annuale' (float, None se serie vuota),
    'mese_piu_caro' e 'mese_piu_economico' (dict {'mese','fattore'} o None),
    'ampiezza_pp' (float o None)."""
    MESI = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu",
            "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
    cols = ["Mese", "Ore", "Media €/MWh", "Mediana €/MWh", "Min €/MWh",
            "Max €/MWh", "Dev.std €/MWh", "Fattore stagionale"]
    vuoto = {"mensile": pd.DataFrame(columns=cols), "media_annuale": None,
             "mese_piu_caro": None, "mese_piu_economico": None,
             "ampiezza_pp": None}
    p = prezzi.astype(float).dropna()
    if p.empty:
        return vuoto
    idxn = p.index.tz_localize(None) if p.index.tz is not None else p.index
    media_ann = float(p.mean())
    righe = []
    for m in range(1, 13):
        v = p[idxn.month == m]
        if v.empty:
            continue
        media_m = float(v.mean())
        fattore = (round(media_m / media_ann, 3)
                   if media_ann > 0 else None)
        righe.append({
            "Mese": MESI[m - 1], "Ore": int(len(v)),
            "Media €/MWh": round(media_m, 2),
            "Mediana €/MWh": round(float(v.median()), 2),
            "Min €/MWh": round(float(v.min()), 2),
            "Max €/MWh": round(float(v.max()), 2),
            "Dev.std €/MWh": round(float(v.std()), 2),
            "Fattore stagionale": fattore})
    out = dict(vuoto)
    if not righe:
        return out
    out["mensile"] = pd.DataFrame(righe, columns=cols).reset_index(drop=True)
    out["media_annuale"] = round(media_ann, 2)
    validi = [r for r in righe if r["Fattore stagionale"] is not None]
    if len(validi) >= 2:
        caro = max(validi, key=lambda r: r["Fattore stagionale"])
        econ = min(validi, key=lambda r: r["Fattore stagionale"])
        out["mese_piu_caro"] = {"mese": caro["Mese"],
                                "fattore": caro["Fattore stagionale"]}
        out["mese_piu_economico"] = {"mese": econ["Mese"],
                                     "fattore": econ["Fattore stagionale"]}
        out["ampiezza_pp"] = round(
            (caro["Fattore stagionale"] - econ["Fattore stagionale"]) * 100, 1)
    return out


def calcola_budget_tracker(prezzi, mw_f1, mw_f2, mw_f3, budget_annuo):
    """Monitoraggio del budget energetico annuale (budget tracker).

    Dato un budget annuale in € e il profilo di prelievo (MW per fascia
    F1/F2/F3), calcola il costo spot effettivo mese per mese sul periodo
    disponibile, la spesa cumulata giorno per giorno, il budget PRO-RATA
    TEMPORIS (budget x giorni trascorsi / 365) e la PROIEZIONE a fine anno
    (burn rate giornaliero x 365). L'INDICE DI CONSUMO = spesa effettiva /
    budget pro-rata x 100: sopra 100 il budget si brucia piu' in fretta del
    tempo che passa (allarme sforamento), sotto 100 si e' in anticipo sul
    piano di spesa.

    Utile per: controllo di gestione dell'energia, variance analysis
    mensile, allerta precoce di sforamento, negoziazione di integrazioni di
    budget con dati oggettivi.

    NaN-safe: ore con prezzo NaN ignorate. Con budget <= 0 o serie vuota
    ritorna il dict vuoto (colonne giuste, KPI a None/0).

    Ritorna dict con 'giorni' (int), 'mwh' (float), 'costo_tot' (float),
    'budget' (float), 'budget_prorata' (float), 'indice_consumo_pct' (float
    o None), 'burn_giorno' (float), 'proiezione_annua' (float),
    'scostamento' (float), 'scostamento_pct' (float o None), 'mensile'
    (DataFrame: Mese, Giorni, MWh, 'Costo €', '€/MWh medio',
    'Budget mensile €', 'Scostamento €') e 'cumulata' (DataFrame: Data,
    'Costo cumulato €', 'Budget pro-rata €')."""
    cols_m = ["Mese", "Giorni", "MWh", "Costo €", "€/MWh medio",
              "Budget mensile €", "Scostamento €"]
    cols_c = ["Data", "Costo cumulato €", "Budget pro-rata €"]
    budget = float(budget_annuo or 0.0)
    vuoto = {"giorni": 0, "mwh": 0.0, "costo_tot": 0.0, "budget": budget,
             "budget_prorata": 0.0, "indice_consumo_pct": None,
             "burn_giorno": 0.0, "proiezione_annua": 0.0, "scostamento": None,
             "scostamento_pct": None,
             "mensile": pd.DataFrame(columns=cols_m),
             "cumulata": pd.DataFrame(columns=cols_c)}
    p = prezzi.astype(float).dropna()
    out = dict(vuoto)
    if p.empty or budget <= 0:
        return out
    mw_map = {"F1": float(mw_f1), "F2": float(mw_f2), "F3": float(mw_f3)}
    idxn = p.index.tz_localize(None) if p.index.tz is not None else p.index
    mw = idxn.map(fascia_oraria).map(mw_map).to_numpy(dtype=float)
    costo = p.to_numpy(dtype=float) * mw
    mese_key = idxn.strftime("%Y-%m")
    righe = []
    for mese in sorted(set(mese_key)):
        mask = mese_key == mese
        gg = int(pd.DatetimeIndex(idxn[mask]).floor("D").nunique())
        mwh = float(mw[mask].sum())
        cst = float(costo[mask].sum())
        pm = round(cst / mwh, 2) if mwh > 0 else None
        bmens = round(budget / 12.0, 2)
        righe.append({"Mese": mese, "Giorni": gg, "MWh": round(mwh, 1),
                      "Costo €": round(cst, 2), "€/MWh medio": pm,
                      "Budget mensile €": bmens,
                      "Scostamento €": round(cst - bmens, 2)})
    out["mensile"] = pd.DataFrame(righe, columns=cols_m).reset_index(drop=True)
    giorni_ser = pd.DatetimeIndex(idxn).floor("D")
    giornaliero = pd.Series(costo).groupby(giorni_ser).sum().sort_index()
    n_giorni = int(len(giornaliero))
    cum = giornaliero.cumsum()
    prog = (np.arange(1, n_giorni + 1) / 365.0 * budget)
    out["cumulata"] = pd.DataFrame({
        "Data": [d.strftime("%Y-%m-%d") for d in cum.index],
        "Costo cumulato €": [round(float(v), 2) for v in cum.values],
        "Budget pro-rata €": [round(float(v), 2) for v in prog],
    }, columns=cols_c).reset_index(drop=True)
    out["giorni"] = n_giorni
    out["mwh"] = round(float(mw.sum()), 1)
    out["costo_tot"] = round(float(costo.sum()), 2)
    out["budget_prorata"] = round(budget * n_giorni / 365.0, 2)
    out["indice_consumo_pct"] = (
        round(out["costo_tot"] / out["budget_prorata"] * 100, 1)
        if out["budget_prorata"] > 0 else None)
    out["burn_giorno"] = (round(out["costo_tot"] / n_giorni, 2)
                          if n_giorni else 0.0)
    out["proiezione_annua"] = round(out["burn_giorno"] * 365.0, 2)
    out["scostamento"] = round(out["proiezione_annua"] - budget, 2)
    out["scostamento_pct"] = round(out["scostamento"] / budget * 100, 1)
    return out


def calcola_sensibilita_profilo(prezzi, mw_f1, mw_f2, mw_f3, delta_pct=10.0):
    """Analisi di sensitività del costo di fornitura al profilo di prelievo.

    Per ciascuna fascia F1/F2/F3 calcola di quanto varia il costo spot del
    periodo se la potenza prelevata in quella fascia cambia di +/-delta_pct %.
    Il costo e' lineare nei MW (somma oraria prezzo x MW della fascia), quindi
    Δcosto = costo_fascia x ±delta_pct/100 e' esatto, non un'approssimazione.
    Il COSTO MARGINALE (€ per 1 MW aggiuntivo in una fascia) e' il KPI
    operativo: dice dove costa di piu' aggiungere carico e dove conviene
    tagliare i prelievi. La fascia piu' sensibile e' quella con il costo
    assoluto piu' alto: un ±d% li' sposta piu' euro.

    Utile per: negoziare contratti per fasce, valutare spostamenti di carico,
    dimensionare interventi di efficienza (tagliare 1 MW in F1 vale X €/anno).

    NaN-safe: ore con prezzo NaN ignorate. Con serie vuota, tutti i MW a 0
    o delta_pct = 0 ritorna il dict vuoto (DataFrame con le colonne giuste,
    KPI a None/0).

    Ritorna dict con 'delta_pct' (float), 'costo_base' (float),
    'fascia_piu_sensibile' (str o None), 'costo_marginale' (dict fascia ->
    €/MW o None) e 'fasce' (DataFrame: Fascia, 'Costo fascia €',
    'Quota costo %', 'Δcosto +d% €', 'Δcosto -d% €', 'Costo marginale €/MW')."""
    cols = ["Fascia", "Costo fascia €", "Quota costo %",
            "Δcosto +d% €", "Δcosto -d% €", "Costo marginale €/MW"]
    dpct = abs(float(delta_pct or 0.0))
    d = dpct / 100.0
    vuoto = {"delta_pct": dpct, "costo_base": 0.0, "fascia_piu_sensibile": None,
             "costo_marginale": {},
             "fasce": pd.DataFrame(columns=cols)}
    p = prezzi.astype(float).dropna()
    mw_map = {"F1": float(mw_f1), "F2": float(mw_f2), "F3": float(mw_f3)}
    out = dict(vuoto)
    if p.empty or all(m <= 0 for m in mw_map.values()) or d <= 0:
        return out
    idxn = p.index.tz_localize(None) if p.index.tz is not None else p.index
    fasce = idxn.map(fascia_oraria)
    pv = p.to_numpy(dtype=float)
    costi, marg = {}, {}
    for b, mwb in mw_map.items():
        cb = float((pv[fasce == b] * mwb).sum()) if mwb > 0 else 0.0
        costi[b] = cb
        marg[b] = round(cb / mwb, 2) if mwb > 0 else None
    base = sum(costi.values())
    righe = []
    for b in ("F1", "F2", "F3"):
        righe.append({"Fascia": b,
                      "Costo fascia €": round(costi[b], 2),
                      "Quota costo %": (round(costi[b] / base * 100, 1)
                                        if base > 0 else None),
                      "Δcosto +d% €": round(costi[b] * d, 2),
                      "Δcosto -d% €": round(-costi[b] * d, 2),
                      "Costo marginale €/MW": marg[b]})
    out["fasce"] = pd.DataFrame(righe, columns=cols).reset_index(drop=True)
    out["costo_base"] = round(base, 2)
    attive = [b for b in ("F1", "F2", "F3") if mw_map[b] > 0]
    out["fascia_piu_sensibile"] = (max(attive, key=lambda b: costi[b])
                                   if attive else None)
    out["costo_marginale"] = marg
    return out


def calcola_var_costo(prezzi, mw_f1, mw_f2, mw_f3, n_scenari=1000,
                      soglia_euro=None, seed=42):
    """Value-at-Risk del COSTO di fornitura via Monte Carlo (block bootstrap).

    Simula n_scenari futuri di pari durata del periodo osservato ricampionando
    (con seed fisso -> risultati deterministici e riproducibili) blocchi
    circolari di 24 ore consecutive dalla serie dei prezzi spot: il ricampionamento
    per giornate intere preserva il profilo giornaliero tipico (picchi diurni,
    valli notturne). Per ciascuno scenario il costo del profilo di prelievo
    F1/F2/F3 e' la somma oraria prezzo_simulato x MW della fascia oraria.

    KPI: costo atteso (media degli scenari), P50/P75/P90/P95/P99. Il P95 e' il
    VaR del costo: nel 95% degli scenari il costo resta SOTTO questo livello
    (soglia di budget a rischio). Se e' impostata una soglia di allarme
    (soglia_euro), calcola anche la probabilità di sforamento.

    Differenza rispetto al tab Rischio & Durata: li' il VaR e' STORICO sulla
    distribuzione del prezzo orario; qui e' PROSPETTICO sul costo totale del
    profilo, quello che finisce davvero in bolletta.

    NaN-safe: ore con prezzo NaN ignorate. Con serie vuota, tutti i MW a 0 o
    n_scenari <= 0 ritorna il dict vuoto (DataFrame con le colonne giuste,
    KPI a None, array scenari vuoto).

    Ritorna dict con 'n_scenari' (int), 'ore' (int), 'mwh' (float),
    'costo_spot' (float: costo del profilo sui prezzi osservati),
    'costo_atteso', 'p50', 'p75', 'p90', 'p95', 'p99', 'costo_min',
    'costo_max' (float o None), 'soglia' (float o None),
    'prob_sforamento_pct' (float o None), 'percentili' (DataFrame:
    Percentile, 'Costo €') e 'scenari' (np.array dei costi per scenario)."""
    cols = ["Percentile", "Costo €"]
    vuoto = {"n_scenari": 0, "ore": 0, "mwh": 0.0, "costo_spot": None,
             "costo_atteso": None, "p50": None, "p75": None, "p90": None,
             "p95": None, "p99": None, "costo_min": None, "costo_max": None,
             "soglia": soglia_euro,
             "prob_sforamento_pct": None,
             "percentili": pd.DataFrame(columns=cols),
             "scenari": np.array([], dtype=float)}
    out = dict(vuoto)
    p = prezzi.astype(float).dropna()
    mw_map = {"F1": float(mw_f1), "F2": float(mw_f2), "F3": float(mw_f3)}
    n = int(n_scenari or 0)
    if p.empty or n <= 0 or all(m <= 0 for m in mw_map.values()):
        return out
    idxn = p.index.tz_localize(None) if p.index.tz is not None else p.index
    fasce = idxn.map(fascia_oraria).to_numpy()
    mw_prof = np.array([mw_map.get(b, 0.0) for b in fasce], dtype=float)
    pv = p.to_numpy(dtype=float)
    L = len(pv)
    blocco = max(1, min(24, L))
    rng = np.random.default_rng(int(seed))
    n_blocchi = int(np.ceil(L / blocco))
    ore_idx = np.arange(blocco)
    costi = np.empty(n, dtype=float)
    for s in range(n):
        starts = rng.integers(0, L, size=n_blocchi)
        path = pv[(starts[:, None] + ore_idx) % L].ravel()[:L]
        costi[s] = float((path * mw_prof).sum())
    out["n_scenari"] = n
    out["ore"] = L
    out["mwh"] = round(float(mw_prof.sum()), 2)
    out["costo_spot"] = round(float((pv * mw_prof).sum()), 2)
    out["costo_atteso"] = round(float(costi.mean()), 2)
    pct = {k: float(np.quantile(costi, k / 100.0))
           for k in (50, 75, 90, 95, 99)}
    for k, v in pct.items():
        out[f"p{k}"] = round(v, 2)
    out["costo_min"] = round(float(costi.min()), 2)
    out["costo_max"] = round(float(costi.max()), 2)
    out["percentili"] = pd.DataFrame(
        [{"Percentile": f"P{k}", "Costo €": round(v, 2)}
         for k, v in pct.items()], columns=cols).reset_index(drop=True)
    out["scenari"] = costi
    if soglia_euro is not None:
        out["prob_sforamento_pct"] = round(float((costi > soglia_euro).mean() * 100), 1)
    return out


def calcola_top_giorni_costo(prezzi, mw_f1, mw_f2, mw_f3, top_n=10):
    """Costo giornaliero del profilo di prelievo e classifica dei giorni piu' costosi.

    Aggrega il costo orario (prezzo spot x MW della fascia F1/F2/F3) per giorno
    di calendario: per ogni giorno calcola MWh prelevati, costo totale, prezzo
    medio ponderato e la fascia che ha generato piu' costo ('fascia dominante').
    Produce anche la classifica dei top_n giorni piu' costosi e una matrice
    calendario (settimane ISO x giorni Lun-Dom) per la heatmap del costo
    giornaliero.

    Differenza rispetto agli altri tab: Picchi guarda le ORE di prezzo estremo,
    Concentrazione costo la curva di Lorenz sulle ore, Settimana tipo il profilo
    MEDIO settimanale. Qui la granularita' e' il GIORNO di calendario: 'quanto
    mi e' costato il 15/09?' e' la domanda operativa per tesoreria, budget e
    verifica delle fatture del fornitore.

    NaN-safe: ore con prezzo NaN ignorate. Serie vuota o tutti i MW a zero ->
    KPI a None e DataFrame con le colonne giuste ma vuoti. Il raggruppamento
    giornaliero usa l'indice reso tz-naive (come in calcola_base_peak_mensile).

    Ritorna dict con 'n_giorni', 'mwh_tot', 'costo_tot', 'costo_medio_gg',
    'rapporto_max_medio' (None se media <= 0), 'quota_top10pct' (% del costo
    generata dal 10% di giorni piu' costosi, None se totale <= 0),
    'giorno_max_data', 'giorno_max_costo', 'top_n',
    'giorni' (DataFrame cronologico: Data, Giorno, MWh, Costo €,
    Prezzo medio €/MWh, Fascia dominante), 'top' (top_n righe di 'giorni'
    ordinate per costo decrescente) e 'calendario' (DataFrame pivot: righe
    settimane ISO 'YYYY-Www', colonne Lun..Dom, valori Costo € giornaliero;
    NaN dove il giorno non appartiene al periodo)."""
    cols_g = ["Data", "Giorno", "MWh", "Costo €", "Prezzo medio €/MWh", "Fascia dominante"]
    cols_cal = ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"]
    vuoto = {"n_giorni": 0, "mwh_tot": 0.0, "costo_tot": None,
             "costo_medio_gg": None, "rapporto_max_medio": None,
             "quota_top10pct": None, "giorno_max_data": None,
             "giorno_max_costo": None, "top_n": int(top_n or 0),
             "giorni": pd.DataFrame(columns=cols_g),
             "top": pd.DataFrame(columns=cols_g),
             "calendario": pd.DataFrame(columns=cols_cal)}
    out = dict(vuoto)
    p = prezzi.astype(float).dropna()
    mw_map = {"F1": float(mw_f1), "F2": float(mw_f2), "F3": float(mw_f3)}
    if p.empty or all(m <= 0 for m in mw_map.values()):
        return out
    idx = p.index
    idxn = idx.tz_localize(None) if idx.tz is not None else idx
    df = pd.DataFrame({"prezzo": p.to_numpy(dtype=float),
                       "fascia": list(idxn.map(fascia_oraria))}, index=idxn)
    df["mw"] = df["fascia"].map(mw_map)
    df["costo"] = df["prezzo"] * df["mw"]
    nomi_gg = list(cols_cal)
    righe = []
    for giorno, grp in df.groupby(idxn.date):
        mwh = float(grp["mw"].sum())
        costo = float(grp["costo"].sum())
        costo_fascia = grp.groupby("fascia")["costo"].sum()
        dom = str(costo_fascia.idxmax()) if len(costo_fascia) else None
        ts = pd.Timestamp(giorno)
        righe.append({
            "Data": ts.strftime("%d/%m/%Y"),
            "_dt": ts,
            "Giorno": nomi_gg[ts.weekday()],
            "MWh": round(mwh, 1),
            "Costo €": round(costo, 2),
            "Prezzo medio €/MWh": round(costo / mwh, 2) if mwh > 0 else None,
            "Fascia dominante": dom,
        })
    g = pd.DataFrame(righe).sort_values("_dt").reset_index(drop=True)
    n = len(g)
    costi = g["Costo €"].to_numpy(dtype=float)
    totale = float(costi.sum())
    medio = float(costi.mean())
    cmax = float(costi.max())
    imax = int(costi.argmax())
    k10 = max(1, int(round(n * 0.10)))
    quota10 = (float(np.sort(costi)[::-1][:k10].sum() / totale * 100)
               if totale > 0 else None)
    tn = max(1, int(top_n or 10))
    top = g.sort_values("Costo €", ascending=False).head(tn).reset_index(drop=True)
    # matrice calendario: righe = settimane ISO, colonne = Lun..Dom
    cal = g.copy()
    iso = cal["_dt"].dt.isocalendar()
    cal["week"] = iso["year"].astype(str) + "-W" + iso["week"].astype(str).str.zfill(2)
    cal["wd"] = cal["_dt"].dt.weekday
    piv = cal.pivot_table(index="week", columns="wd", values="Costo €", aggfunc="sum")
    piv = piv.reindex(columns=range(7))
    piv.columns = nomi_gg
    out.update({
        "n_giorni": n,
        "mwh_tot": round(float(g["MWh"].sum()), 1),
        "costo_tot": round(totale, 2),
        "costo_medio_gg": round(medio, 2),
        "rapporto_max_medio": round(cmax / medio, 2) if medio > 0 else None,
        "quota_top10pct": round(quota10, 1) if quota10 is not None else None,
        "giorno_max_data": g.loc[imax, "Data"],
        "giorno_max_costo": round(cmax, 2),
        "top_n": tn,
        "giorni": g.drop(columns=["_dt"]).reset_index(drop=True),
        "top": top.drop(columns=["_dt"]).reset_index(drop=True),
        "calendario": piv,
    })
    return out


def calcola_fasce_ottimali(prezzi, n_bande=3):
    """Fasce tariffarie OTTIMALI derivate dai dati: raggruppa le 24 ore in
    n_bande fasce che minimizzano la dispersione di prezzo dentro ogni fascia.

    A differenza delle fasce AEEGSI F1/F2/F3 (tab3, orari fissi per regolamento)
    e di Base/Peak/Offpeak EPEX (tab7, definizioni di mercato), qui le fasce
    nascono dal PROFILO ORARIO MEDIO osservato: serve a disegnare una tariffa
    time-of-use su misura o a decidere in quali ore conviene concentrare i
    carichi flessibili.

    Algoritmo: k-means 1-D deterministico (nessun seed casuale) sui prezzi medi
    orari. Centroidi iniziali sui quantili ordinati, iterazioni di Lloyd fino a
    stabilita' (max 100). n_bande viene clamped a [2, n_ore_con_dati].

    NaN-safe: le ore senza dati vengono escluse dal clustering (Banda = None).
    Serie vuota o un solo valore distinto -> KPI a None e DataFrame con le
    colonne giuste ma vuoti (o con una sola banda se tutto e' piatto).

    Ritorna dict con 'n_bande' (effettive), 'n_ore',
    'varianza_spiegata_pct' (1 - within_ss/total_ss: quota della variabilita'
    oraria catturata dalle fasce, None se totale_ss <= 0),
    'std_within_media' (std media ponderata dentro le fasce),
    'spread_bande' (differenza tra prezzo medio della fascia piu' cara e
    quella piu' economica, None con < 2 bande),
    'profilo' (DataFrame: Ora, Prezzo medio €/MWh, Banda) e
    'bande' (DataFrame: Banda, N. ore, Ore, Prezzo medio €/MWh,
    Scostamento vs media %)."""
    cols_p = ["Ora", "Prezzo medio €/MWh", "Banda"]
    cols_b = ["Banda", "N. ore", "Ore", "Prezzo medio €/MWh", "Scostamento vs media %"]
    vuoto = {"n_bande": 0, "n_ore": 0, "varianza_spiegata_pct": None,
             "std_within_media": None, "spread_bande": None,
             "profilo": pd.DataFrame(columns=cols_p),
             "bande": pd.DataFrame(columns=cols_b)}
    out = dict(vuoto)
    p = prezzi.astype(float).dropna()
    if p.empty:
        return out
    idx = p.index
    idxn = idx.tz_localize(None) if idx.tz is not None else idx
    ore = np.array([t.hour for t in idxn])
    vals = p.to_numpy(dtype=float)
    h_uni = np.arange(24)
    profilo = pd.Series(index=h_uni, dtype=float)
    for h in h_uni:
        m = vals[ore == h]
        if len(m):
            profilo[h] = float(m.mean())
    prof = profilo.dropna()
    n_ore = len(prof)
    if n_ore == 0:
        return out
    x = prof.to_numpy(dtype=float)
    ore_v = prof.index.to_numpy(dtype=int)
    n_distinti = len(np.unique(x))
    k = max(1, min(int(n_bande or 3), n_ore, n_distinti))
    out["n_ore"] = n_ore
    # k-means 1-D deterministico: centroidi iniziali sui quantili dei dati ordinati
    xs = np.sort(x)
    pos = np.linspace(0, len(xs) - 1, k)
    cent = np.array([xs[int(round(q))] for q in pos], dtype=float)
    labels = np.zeros(len(x), dtype=int)
    for _ in range(100):
        d = np.abs(x[:, None] - cent[None, :])
        new_labels = d.argmin(axis=1)
        new_cent = cent.copy()
        for j in range(k):
            mem = x[new_labels == j]
            if len(mem):
                new_cent[j] = mem.mean()
        if np.array_equal(new_labels, labels) and np.allclose(new_cent, cent):
            labels = new_labels
            cent = new_cent
            break
        labels, cent = new_labels, new_cent
    # riordina le bande per prezzo crescente (B1 = piu' economica)
    ordine = np.argsort(cent)
    mappa = {old: new for new, old in enumerate(ordine)}
    labels = np.array([mappa[l] for l in labels])
    cent = cent[ordine]
    total_ss = float(((x - x.mean()) ** 2).sum())
    within_ss = float(sum(((x[labels == j] - cent[j]) ** 2).sum() for j in range(k)))
    media = float(x.mean())
    righe_p = [{"Ora": int(h), "Prezzo medio €/MWh": round(float(v), 2),
                "Banda": f"B{b + 1}"} for h, v, b in zip(ore_v, x, labels)]
    df_p = pd.DataFrame(righe_p).sort_values("Ora").reset_index(drop=True)
    righe_b = []
    for j in range(k):
        mem = x[labels == j]
        ore_b = sorted(int(h) for h in ore_v[labels == j])
        righe_b.append({
            "Banda": f"B{j + 1}",
            "N. ore": len(mem),
            "Ore": ", ".join(f"{h:02d}" for h in ore_b),
            "Prezzo medio €/MWh": round(float(cent[j]), 2),
            "Scostamento vs media %": (round((float(cent[j]) / media - 1) * 100, 1)
                                       if media else None),
        })
    df_b = pd.DataFrame(righe_b)
    std_w = float(np.sqrt(sum(((x[labels == j] - cent[j]) ** 2).sum()
                              for j in range(k)) / len(x))) if len(x) else None
    out.update({
        "n_bande": k,
        "varianza_spiegata_pct": (round((1 - within_ss / total_ss) * 100, 1)
                                  if total_ss > 0 else None),
        "std_within_media": round(std_w, 2) if std_w is not None else None,
        "spread_bande": (round(float(cent[-1] - cent[0]), 2) if k >= 2 else None),
        "profilo": df_p,
        "bande": df_b,
    })
    return out


def calcola_autocorrelazione(prezzi, max_lag=168):
    """Autocorrelazione del prezzo spot orario ai lag 1..max_lag.

    Misura quanto il prezzo di oggi 'ricorda' il prezzo delle ore precedenti:
    e' la firma statistica della persistenza degli shock di prezzo e della
    stagionalita'. ACF(1) alta = prezzo appiccicoso (mean-reversion lenta);
    picchi a lag 24/168 = stagionalita' giornaliera/settimanale dominante;
    ACF che decade in fretta = mercato imprevedibile ora per ora.

    Metodo: correlazione di Pearson su coppie sovrapposte (vals[:-lag], vals[lag:]),
    NaN-safe (i NaN vengono scartati prima del calcolo). La significativita'
    usa la banda 95% classica +/- 1.96/sqrt(n_coppie) per ogni lag. lag_decay e'
    il primo lag in cui |ACF| scende sotto la banda (la 'memoria' del mercato
    in ore); None se l'autocorrelazione resta significativa oltre max_lag.

    Serie vuota, < 3 punti validi o prezzo perfettamente piatto (std = 0) ->
    KPI a None e DataFrame con le colonne giuste ma vuoto. max_lag viene
    clamped a [1, n - 1].

    Ritorna dict con 'max_lag' (effettivo), 'n' (punti validi),
    'acf_lag1', 'acf_lag24', 'acf_lag168' (None se lag fuori range),
    'lag_decay' (int o None) e 'df' (DataFrame: Lag (ore), ACF, Banda 95%,
    Significativo 95%)."""
    cols = ["Lag (ore)", "ACF", "Banda 95%", "Significativo 95%"]
    vuoto = {"max_lag": 0, "n": 0, "acf_lag1": None, "acf_lag24": None,
             "acf_lag168": None, "lag_decay": None,
             "df": pd.DataFrame(columns=cols)}
    try:
        p = prezzi.astype(float).dropna()
    except Exception:
        return dict(vuoto)
    n = len(p)
    try:
        ml = int(max_lag)
    except (TypeError, ValueError):
        ml = 0
    if n < 3 or ml < 1:
        return dict(vuoto)
    ml = min(ml, n - 1)
    vals = p.to_numpy(dtype=float)
    if float(np.std(vals)) == 0.0:
        return dict(vuoto, n=n, max_lag=ml)
    righe = []
    decay = None
    for lag in range(1, ml + 1):
        x, y = vals[:-lag], vals[lag:]
        n_c = len(x)
        band = 1.96 / np.sqrt(n_c) if n_c > 0 else float("nan")
        if n_c >= 2 and float(np.std(x)) > 0 and float(np.std(y)) > 0:
            acf = float(np.corrcoef(x, y)[0, 1])
        else:
            acf = float("nan")
        sig = (not np.isnan(acf)) and abs(acf) > band
        if decay is None and not np.isnan(acf) and abs(acf) < band:
            decay = lag
        righe.append({
            "Lag (ore)": lag,
            "ACF": None if np.isnan(acf) else round(acf, 4),
            "Banda 95%": None if np.isnan(band) else round(band, 4),
            "Significativo 95%": "Sì" if sig else "No",
        })
    df = pd.DataFrame(righe, columns=cols)

    def _at(lag):
        r = df.loc[df["Lag (ore)"] == lag, "ACF"]
        return float(r.iloc[0]) if (len(r) and r.iloc[0] is not None) else None

    return {"max_lag": ml, "n": n,
            "acf_lag1": _at(1), "acf_lag24": _at(24), "acf_lag168": _at(168),
            "lag_decay": decay, "df": df}


def calcola_stress_prezzo(prezzi, mw_f1, mw_f2, mw_f3, scenari):
    """Stress test deterministico del costo di fornitura sotto shock di prezzo.

    Per ogni scenario applica uno shock alla serie oraria dei prezzi e ricalcola
    il costo della fornitura (profilo F1/F2/F3, via calcola_costo_fornitura):
    e' il what-if 'cosa succede al mio costo se i prezzi schizzano?'.

    prezzi: Series oraria in €/MWh con indice datetime (i NaN vengono scartati).
    mw_f1/2/3: potenza prelevata (MW) per fascia. scenari: lista di dict con
      'nome' (str), 'tipo' ('add' = +€/MWh, 'pct' = +%), 'valore' (float),
      'solo_fascia' (None = tutte le ore, oppure 'F1'/'F2'/'F3' = shock solo
      sulle ore di quella fascia, es. picco F1).
    Scenari malformati (tipo/valore/fascia non validi) vengono scartati.
    Nota: con prezzi negativi uno shock 'pct' positivo rende il prezzo MENO
    negativo (scala il valore, non lo sposta): per shock simmetrici sui
    livelli usare 'add'.

    Ritorna dict con 'base' (dict di calcola_costo_fornitura o None),
    'df' (DataFrame: Scenario, Shock, Costo (€), Delta (€), Delta (%),
    Prezzo medio (€/MWh)), 'worst_nome' (scenario col delta % piu' alto),
    'worst_delta_pct', 'worst_delta_eur' (None se df vuoto) e 'n_scenari'.
    Serie vuota o senza scenari validi -> base a None e df vuoto."""
    cols = ["Scenario", "Shock", "Costo (€)", "Delta (€)", "Delta (%)",
            "Prezzo medio (€/MWh)"]
    vuoto = {"base": None, "df": pd.DataFrame(columns=cols),
             "worst_nome": None, "worst_delta_pct": None,
             "worst_delta_eur": None, "n_scenari": 0}
    try:
        p = prezzi.astype(float).dropna()
    except Exception:
        return dict(vuoto)
    if len(p) == 0:
        return dict(vuoto)
    try:
        base = calcola_costo_fornitura(p, float(mw_f1), float(mw_f2), float(mw_f3))
    except Exception:
        return dict(vuoto)
    try:
        fasce = pd.Index(p.index.map(fascia_oraria)).to_numpy()
    except Exception:
        return dict(vuoto)
    base_tot = base["totale"]
    righe = []
    for sc in (scenari or []):
        try:
            nome = str(sc.get("nome", "")).strip() or "Scenario"
            tipo = str(sc.get("tipo", "")).strip().lower()
            valore = float(sc.get("valore"))
            solo = sc.get("solo_fascia")
            if tipo not in ("add", "pct"):
                continue
            if not np.isfinite(valore):
                continue
            if solo is not None and str(solo) not in ("F1", "F2", "F3"):
                continue
        except (AttributeError, TypeError, ValueError):
            continue
        vals = p.to_numpy(dtype=float).copy()
        if solo is None:
            maschera = np.ones(len(vals), dtype=bool)
        else:
            maschera = (fasce == str(solo))
        if tipo == "add":
            vals[maschera] = vals[maschera] + valore
            shock = f"{valore:+g} €/MWh" + (f" su {solo}" if solo else "")
        else:
            vals[maschera] = vals[maschera] * (1.0 + valore / 100.0)
            shock = f"{valore:+g} %" + (f" su {solo}" if solo else "")
        p_sh = pd.Series(vals, index=p.index).dropna()
        if len(p_sh) == 0:
            continue
        try:
            r = calcola_costo_fornitura(p_sh, float(mw_f1), float(mw_f2), float(mw_f3))
        except Exception:
            continue
        delta = r["totale"] - base_tot
        delta_pct = (delta / base_tot * 100.0) if base_tot != 0 else float("nan")
        pm = r["ponderato"]
        righe.append({
            "Scenario": nome,
            "Shock": shock,
            "Costo (€)": round(r["totale"], 0),
            "Delta (€)": round(delta, 0),
            "Delta (%)": None if np.isnan(delta_pct) else round(delta_pct, 1),
            "Prezzo medio (€/MWh)": None if np.isnan(pm) else round(pm, 2),
        })
    df = pd.DataFrame(righe, columns=cols)
    out = dict(vuoto)
    out["base"] = base
    out["df"] = df
    out["n_scenari"] = len(df)
    if len(df) > 0:
        d_pct = pd.to_numeric(df["Delta (%)"], errors="coerce")
        if d_pct.notna().any():
            i = int(d_pct.idxmax())
            out["worst_nome"] = str(df.loc[i, "Scenario"])
            out["worst_delta_pct"] = float(d_pct.iloc[i])
            out["worst_delta_eur"] = float(df.loc[i, "Delta (€)"])
    return out


def calcola_forecast_prezzo(prezzi, n_settimane=8, backtest_settimane=4):
    """Forecast naive-stagionale del prezzo day-ahead del giorno successivo.

    Per ogni ora h del giorno target (il giorno dopo l'ultimo giorno con dati
    completi), la previsione e' la media dei prezzi registrati all'ora h nello
    stesso giorno della settimana nelle ultime n_settimane: cattura profilo
    giornaliero e stagionalita' settimanale senza parametri da stimare.
    Se per una coppia (ora, weekday) ci sono meno di 2 osservazioni, ripiega
    sulla media dell'ora h su tutto il training; in ultima istanza sulla media
    globale del training. Vengono riportati anche min/max del campione usato
    (banda di incertezza empirica).

    Backtest walk-forward: per ciascuno degli ultimi backtest_settimane
    giorni-target (l'ultimo giorno con dati e gli stessi weekday delle
    settimane precedenti) la previsione viene ricalcolata usando solo i dati
    precedenti al giorno target e confrontata col reale: MAE (errore medio
    assoluto), RMSE (penalizza gli errori grandi) e bias medio, definito come
    media(previsione - reale): bias positivo = il metodo tende a sovrastimare
    (previsione da correggere al ribasso).

    prezzi: Series oraria in €/MWh con indice datetime (i NaN vengono scartati).
    n_settimane: settimane di storia per la media stagionale (>=1, default 8).
    backtest_settimane: quante settimane indietro valutare (0 = nessun backtest).
    Giorni 'completi' = con almeno 20 osservazioni (tollera DST da 23/25 ore).
    Ritorna dict con 'data_target' (Timestamp o None), 'df_forecast'
    (Ora, Fascia, Previsione (€/MWh), Min/Max campione, N campioni),
    'df_backtest' (Data, MAE, RMSE, Bias), 'mae', 'rmse', 'bias' (medie sui
    giorni di backtest valutabili, None se nessuno) e deterministico a parita'
    di input. Serie vuota o senza un giorno completo -> target None e df vuoti."""
    cols_fc = ["Ora", "Fascia", "Previsione (€/MWh)", "Min campione (€/MWh)",
               "Max campione (€/MWh)", "N campioni"]
    cols_bt = ["Data", "MAE (€/MWh)", "RMSE (€/MWh)", "Bias (€/MWh)"]
    vuoto = {"data_target": None,
             "df_forecast": pd.DataFrame(columns=cols_fc),
             "df_backtest": pd.DataFrame(columns=cols_bt),
             "mae": None, "rmse": None, "bias": None}
    try:
        p = prezzi.astype(float).dropna()
    except Exception:
        return dict(vuoto)
    if len(p) == 0:
        return dict(vuoto)
    try:
        n_settimane = max(1, int(n_settimane))
        n_bt = max(0, int(backtest_settimane))
        giorni = p.index.normalize()
        conteggi = p.groupby(giorni).size()
        giorni_full = sorted(d for d, c in conteggi.items() if c >= 20)
    except Exception:
        return dict(vuoto)
    if not giorni_full:
        return dict(vuoto)
    set_full = set(giorni_full)

    def _previsione_giorno(p_train, target_day):
        wd = target_day.weekday()
        righe = []
        for h in range(24):
            try:
                f = fascia_oraria(target_day + pd.Timedelta(hours=h))
            except Exception:
                f = "?"
            camp = p_train[(p_train.index.weekday == wd) & (p_train.index.hour == h)]
            if len(camp) < 2:
                camp = p_train[p_train.index.hour == h]
            if len(camp) == 0:
                camp = p_train
            v = camp.to_numpy(dtype=float)
            righe.append({"Ora": f"{h:02d}:00", "Fascia": f,
                          "Previsione (€/MWh)": round(float(np.mean(v)), 2),
                          "Min campione (€/MWh)": round(float(np.min(v)), 2),
                          "Max campione (€/MWh)": round(float(np.max(v)), 2),
                          "N campioni": int(len(v))})
        return pd.DataFrame(righe, columns=cols_fc)

    last_full = giorni_full[-1]
    target = last_full + pd.Timedelta(days=1)
    df_fc = _previsione_giorno(p[p.index.normalize() < target], target)

    righe_bt, mae_t, rmse_t, bias_t = [], [], [], []
    for k in range(n_bt):
        bt_target = last_full - pd.Timedelta(weeks=k)
        if bt_target not in set_full:
            continue
        p_train = p[p.index.normalize() < bt_target]
        if len(p_train) == 0:
            continue
        fc = _previsione_giorno(p_train, bt_target)
        reali = p[p.index.normalize() == bt_target]
        reali_ora = reali.groupby(reali.index.hour).mean()
        fc_ore = fc["Ora"].str.slice(0, 2).astype(int)
        comuni = [h for h in range(24) if h in set(reali_ora.index)]
        if len(comuni) < 12:
            continue
        err = np.array([float(fc.loc[fc_ore == h, "Previsione (€/MWh)"].iloc[0])
                        - float(reali_ora.loc[h]) for h in comuni])
        m = float(np.mean(np.abs(err)))
        r2 = float(np.sqrt(np.mean(err ** 2)))
        b = float(np.mean(err))
        mae_t.append(m)
        rmse_t.append(r2)
        bias_t.append(b)
        righe_bt.append({"Data": bt_target.strftime("%Y-%m-%d"),
                         "MAE (€/MWh)": round(m, 2),
                         "RMSE (€/MWh)": round(r2, 2),
                         "Bias (€/MWh)": round(b, 2)})
    df_bt = pd.DataFrame(righe_bt, columns=cols_bt)
    out = dict(vuoto)
    out["data_target"] = target
    out["df_forecast"] = df_fc
    out["df_backtest"] = df_bt
    if mae_t:
        out["mae"] = round(float(np.mean(mae_t)), 2)
        out["rmse"] = round(float(np.mean(rmse_t)), 2)
        out["bias"] = round(float(np.mean(bias_t)), 2)
    return out


def calcola_rampe_prezzo(prezzi, soglia=10.0, top_n=50):
    """Rampa massima ora-su-ora del prezzo day-ahead.

    La 'rampa' e' la variazione del prezzo tra due ore consecutive: il segnale
    piu' diretto di quanto il mercato possa muoversi in fretta. Interessa a
    chi opera intraday (quanto puo' guadagnare/perdere una flessibilita'
    spostabile di un'ora), a chi dimensiona gli alert e a chi deve gestire il
    rischio di un profilo di prelievo concentrato in poche ore.

    Il calcolo usa le differenze prime della serie ordinata per tempo, ma
    scarta le coppie con distanza temporale > 120 minuti (buchi nei dati,
    cambi DST): senza questo filtro un buco di 6 ore sembrerebbe una rampa
    estrema. I duplicati di timestamp vengono scartati (primo valore).

    prezzi: Series oraria in €/MWh con indice datetime (i NaN vengono scartati).
    soglia: |delta| minimo (€/MWh) perche' una variazione conti come 'evento'
            (default 10.0). top_n: quanti eventi mostrare nella tabella.
    Ritorna dict con 'rampa_max_up' (max delta, None se non valutabile),
    'rampa_max_down' (min delta), 'media_abs' (media di |delta|),
    'n_up'/'n_down' (eventi oltre soglia), 'df_eventi' (Data e ora, Delta
    (€/MWh), Direzione, Prezzo prima/dopo), tutto deterministico a parita'
    di input. Serie con < 2 ore consecutive ravvicinate -> None e df vuoto."""
    cols_ev = ["Data e ora", "Delta (€/MWh)", "Direzione",
               "Prezzo prima (€/MWh)", "Prezzo dopo (€/MWh)"]
    vuoto = {"rampa_max_up": None, "rampa_max_down": None, "media_abs": None,
             "n_up": 0, "n_down": 0,
             "df_eventi": pd.DataFrame(columns=cols_ev)}
    try:
        p = prezzi.astype(float).dropna()
        p = p[~p.index.duplicated(keep="first")].sort_index()
    except Exception:
        return dict(vuoto)
    if len(p) < 2:
        return dict(vuoto)
    try:
        soglia = abs(float(soglia))
        top_n = max(1, int(top_n))
    except Exception:
        soglia, top_n = 10.0, 50
    try:
        delta_t = p.index.to_series().diff().dt.total_seconds() / 60.0
        d = p.diff()[delta_t.between(1, 120, inclusive="both").fillna(False)]
    except Exception:
        return dict(vuoto)
    if len(d) == 0:
        return dict(vuoto)
    v = d.to_numpy(dtype=float)
    out = dict(vuoto)
    out["media_abs"] = round(float(np.abs(v).mean()), 2)
    out["rampa_max_up"] = round(float(v.max()), 2)
    out["rampa_max_down"] = round(float(v.min()), 2)
    out["n_up"] = int((v >= soglia).sum())
    out["n_down"] = int((v <= -soglia).sum())
    ev = d[np.abs(d) >= soglia].sort_values(key=np.abs, ascending=False).head(top_n)
    righe = []
    for ts, dv in ev.items():
        try:
            dopo = float(p.loc[ts])
            prima = float(p.iloc[p.index.get_loc(ts) - 1])
        except Exception:
            prima, dopo = float("nan"), float("nan")
        righe.append({"Data e ora": ts.strftime("%Y-%m-%d %H:%M"),
                      "Delta (€/MWh)": round(float(dv), 2),
                      "Direzione": "▲ rialzo" if dv > 0 else "▼ ribasso",
                      "Prezzo prima (€/MWh)": round(prima, 2),
                      "Prezzo dopo (€/MWh)": round(dopo, 2)})
    out["df_eventi"] = pd.DataFrame(righe, columns=cols_ev)
    return out


def calcola_persistenza_soglia(prezzi, soglia=100.0):
    """Blocchi di ore consecutive con prezzo sopra una soglia.

    Per chi gestisce un impianto dispacciabile (o una flessibilita') non conta
    solo quanto spesso il prezzo supera il costo variabile, ma per quante ore
    consecutive resta sopra: un blocco di 6 ore giustifica un avviamento, sei
    ore isolate no. La soglia e' quindi il costo variabile (o strike)
    dell'analista; ogni 'blocco' e' una sequenza di ore consecutive con prezzo
    >= soglia.

    Il calcolo ordina la serie per tempo, scarta i duplicati di timestamp (primo
    valore) e interrompe un blocco quando: la distanza temporale tra due ore
    supera 120 minuti (buchi nei dati; i cambi DST restano dentro i blocchi
    perche' sono ore di mercato consecutive), oppure un'ora intermedia ha
    prezzo mancante (NaN): un blocco contiene solo ore osservate e consecutive.
    Deterministico a parita' di input.

    prezzi: Series oraria in €/MWh con indice datetime.
    soglia: prezzo minimo (€/MWh) perche' un'ora conti (default 100.0).
    Ritorna dict con 'soglia', 'n_ore_sopra', 'n_ore_totali', 'quota' (frazione
    di ore sopra soglia, None se non valutabile), 'n_blocchi', 'durata_max',
    'durata_media', 'durata_mediana' (ore; None se nessun blocco) e
    'df_blocchi' (Inizio, Fine, Durata (ore), Prezzo medio/max in €/MWh)."""
    cols_bl = ["Inizio", "Fine", "Durata (ore)",
               "Prezzo medio (€/MWh)", "Prezzo max (€/MWh)"]
    vuoto = {"soglia": None, "n_ore_sopra": 0, "n_ore_totali": 0, "quota": None,
             "n_blocchi": 0, "durata_max": None, "durata_media": None,
             "durata_mediana": None,
             "df_blocchi": pd.DataFrame(columns=cols_bl)}
    try:
        soglia = float(soglia)
    except Exception:
        return dict(vuoto)
    try:
        p0 = prezzi.astype(float)
        p0 = p0[~p0.index.duplicated(keep="first")].sort_index()
    except Exception:
        return dict(vuoto)
    valido = p0.notna().to_numpy()
    p = p0.dropna()
    n_tot = len(p)
    if n_tot == 0:
        return dict(vuoto)
    try:
        dt_min = p.index.to_series().diff().dt.total_seconds() / 60.0
        consecutiva = dt_min.between(1, 120, inclusive="both").fillna(False).to_numpy()
    except Exception:
        consecutiva = np.zeros(n_tot, dtype=bool)
    # ore osservate adiacenti nell'indice originale (nessun NaN in mezzo)
    pos_validi = np.flatnonzero(valido)
    adiacente = np.zeros(n_tot, dtype=bool)
    if n_tot > 1:
        adiacente[1:] = np.diff(pos_validi) == 1
    sopra = (p.to_numpy() >= soglia)
    idx = p.index
    vals = p.to_numpy()
    pos = np.flatnonzero(sopra)
    blocchi = []
    if len(pos):
        ini = prev = int(pos[0])
        for j in (int(x) for x in pos[1:]):
            if j == prev + 1 and bool(consecutiva[j]) and bool(adiacente[j]):
                prev = j
            else:
                blocchi.append((ini, prev))
                ini = prev = j
        blocchi.append((ini, prev))
    righe = []
    for a, b in blocchi:
        seg = vals[a:b + 1]
        righe.append({"Inizio": idx[a].strftime("%Y-%m-%d %H:%M"),
                      "Fine": idx[b].strftime("%Y-%m-%d %H:%M"),
                      "Durata (ore)": int(b - a + 1),
                      "Prezzo medio (€/MWh)": round(float(np.mean(seg)), 2),
                      "Prezzo max (€/MWh)": round(float(np.max(seg)), 2)})
    out = dict(vuoto)
    out["soglia"] = soglia
    out["n_ore_totali"] = n_tot
    n_sopra = int(sopra.sum())
    out["n_ore_sopra"] = n_sopra
    out["quota"] = n_sopra / n_tot
    out["n_blocchi"] = len(blocchi)
    if blocchi:
        dur = [b - a + 1 for a, b in blocchi]
        out["durata_max"] = int(max(dur))
        out["durata_media"] = float(np.mean(dur))
        out["durata_mediana"] = float(np.median(dur))
    out["df_blocchi"] = pd.DataFrame(righe, columns=cols_bl)
    return out


def calcola_spread_calendario(prezzi):
    """Prezzi base mensili e spread calendario (mese su mese).

    Il 'prezzo base mensile' e' la media di tutte le ore del mese: il
    riferimento piu' usato in ETRM per confrontare mesi tra loro. Lo 'spread
    calendario' e' la differenza tra il base di un mese e quello del mese
    precedente (M+1 - M): positivo = mese successivo piu' caro.

    Interessa a chi copre i costi (hedging: i mesi cari si comprano prima),
    a chi fa stagionalita' (quanto costa spostare consumi/produzione da un
    mese all'altro) e a chi valuta contratti indicizzati a media mensile.

    Il calcolo ordina la serie per tempo, scarta i duplicati di timestamp
    (primo valore) e le ore con prezzo mancante (NaN); gli spread vengono
    calcolati solo tra mesi di calendario consecutivi (un mese saltato per
    buchi nei dati non genera uno spread finto). Deterministico a parita'
    di input.

    prezzi: Series oraria in €/MWh con indice datetime.
    Ritorna dict con 'n_mesi', 'spread_medio'/'spread_max'/'spread_min'/
    'std_spread' (degli spread consecutivi, None se < 1 spread), 'quota_pos'
    (frazione di spread positivi, None se non valutabile), 'df_mesi'
    (Mese, Ore, Prezzo base medio (€/MWh)) e 'df_spread' (Coppia, Da, A,
    Spread in €/MWh)."""
    cols_m = ["Mese", "Ore", "Prezzo base medio (€/MWh)"]
    cols_s = ["Coppia", "Da (€/MWh)", "A (€/MWh)", "Spread (€/MWh)"]
    vuoto = {"n_mesi": 0, "spread_medio": None, "spread_max": None,
             "spread_min": None, "std_spread": None, "quota_pos": None,
             "df_mesi": pd.DataFrame(columns=cols_m),
             "df_spread": pd.DataFrame(columns=cols_s)}
    try:
        p = prezzi.astype(float).dropna()
        p = p[~p.index.duplicated(keep="first")].sort_index()
    except Exception:
        return dict(vuoto)
    if len(p) == 0:
        return dict(vuoto)
    try:
        idx = p.index
        try:
            idx = idx.tz_localize(None)  # mesi di calendario in ora locale
        except Exception:
            pass
        per = idx.to_period("M")
    except Exception:
        return dict(vuoto)
    try:
        mensili = p.groupby(per).agg(["mean", "size"])
    except Exception:
        return dict(vuoto)
    if len(mensili) == 0:
        return dict(vuoto)
    mensili = mensili.sort_index()
    periodi = list(mensili.index)
    mezzi = [float(mensili["mean"].iloc[i]) for i in range(len(periodi))]
    ore = [int(mensili["size"].iloc[i]) for i in range(len(periodi))]
    righe_m = [{"Mese": str(periodi[i]), "Ore": ore[i],
                "Prezzo base medio (€/MWh)": round(mezzi[i], 2)}
               for i in range(len(periodi))]
    righe_s, vals = [], []
    for i in range(1, len(periodi)):
        try:
            consecutivi = periodi[i] == periodi[i - 1] + 1
        except Exception:
            consecutivi = False
        if not consecutivi:
            continue
        spr = mezzi[i] - mezzi[i - 1]
        vals.append(spr)
        righe_s.append({"Coppia": f"{periodi[i - 1]} → {periodi[i]}",
                        "Da (€/MWh)": round(mezzi[i - 1], 2),
                        "A (€/MWh)": round(mezzi[i], 2),
                        "Spread (€/MWh)": round(spr, 2)})
    out = dict(vuoto)
    out["n_mesi"] = len(periodi)
    out["df_mesi"] = pd.DataFrame(righe_m, columns=cols_m)
    out["df_spread"] = pd.DataFrame(righe_s, columns=cols_s)
    if vals:
        out["spread_medio"] = round(float(np.mean(vals)), 2)
        out["spread_max"] = round(float(np.max(vals)), 2)
        out["spread_min"] = round(float(np.min(vals)), 2)
        if len(vals) > 1:
            out["std_spread"] = round(float(np.std(vals)), 2)
        else:
            out["std_spread"] = 0.0
        out["quota_pos"] = sum(1 for v in vals if v > 0) / len(vals)
    return out


def calcola_decomposizione_prezzo(prezzi):
    """Decomposizione deterministica del prezzo orario in trend + stagionalita'
    giornaliera + stagionalita' settimanale + residuo (stile STL semplificato).

    A cosa serve: separare quanto del prezzo e' struttura (trend di fondo,
    pattern dell'ora del giorno, pattern del giorno della settimana) da quanto
    e' rumore/shock. Utile per capire se un picco e' "normale" per quell'ora
    o un'anomalia da investigare, e per stimare quanta parte del prezzo e'
    strutturalmente prevedibile.

    Metodo (tutto deterministico a parita' di input):
    - trend: mediana mobile centrata su 168 ore (1 settimana); se la serie ha
      meno di 24 ore, trend piatto = media complessiva;
    - pattern giornaliero: media del detrended per ora del giorno (0-23),
      centrata a media zero (ore senza dati -> 0);
    - pattern settimanale: media del residuo-dopo-giornaliero per giorno della
      settimana (0=lun .. 6=dom), centrata (giorni senza dati -> 0);
    - residuo = prezzo - trend - pattern_giornaliero - pattern_settimanale.
    Gli orari con prezzo NaN e i timestamp duplicati (primo valore) vengono
    scartati prima del calcolo.

    prezzi: Series oraria in €/MWh con indice datetime.
    Ritorna dict con 'n_ore', 'quota_spiegata' (1 - var(residuo)/var(prezzo),
    None se la varianza del prezzo e' nulla), 'std_residuo', 'shock_max'
    (residuo con |.| massimo), 'shock_quando' (timestamp o None), 'trend' e
    'residuo' (Series orarie), 'pattern_giornaliero' (Series indicizzata
    0-23), 'pattern_settimanale' (Series indicizzata 0-6, lun-dom),
    'df_export' (DataFrame orario con Prezzo, Trend, Stag. giornaliera,
    Stag. settimanale, Residuo)."""
    cols = ["Data/ora", "Prezzo (€/MWh)", "Trend (€/MWh)",
            "Stag. giornaliera (€/MWh)", "Stag. settimanale (€/MWh)",
            "Residuo (€/MWh)"]
    vuoto = {"n_ore": 0, "quota_spiegata": None, "std_residuo": None,
             "shock_max": None, "shock_quando": None,
             "trend": pd.Series(dtype=float), "residuo": pd.Series(dtype=float),
             "pattern_giornaliero": pd.Series(dtype=float),
             "pattern_settimanale": pd.Series(dtype=float),
             "df_export": pd.DataFrame(columns=cols)}
    try:
        p = prezzi.astype(float).dropna()
        p = p[~p.index.duplicated(keep="first")].sort_index()
    except Exception:
        return dict(vuoto)
    if len(p) == 0:
        return dict(vuoto)
    try:
        if len(p) >= 24:
            w = min(168, len(p))
            trend = p.rolling(window=w, center=True,
                              min_periods=min(24, w)).median()
            trend = trend.ffill().bfill()
            if trend.isna().all():
                trend = pd.Series(float(p.mean()), index=p.index)
        else:
            trend = pd.Series(float(p.mean()), index=p.index)
        detr = (p - trend).dropna()
        if len(detr) == 0:
            return dict(vuoto)
        ore = detr.index.hour
        g_giorno = detr.groupby(ore).mean().reindex(range(24), fill_value=0.0)
        g_giorno = g_giorno - g_giorno.mean()
        detr2 = detr - ore.map(g_giorno).to_numpy()
        dow = detr2.index.dayofweek
        g_sett = detr2.groupby(dow).mean().reindex(range(7), fill_value=0.0)
        g_sett = g_sett - g_sett.mean()
        comp_g = p.index.hour.map(g_giorno).to_numpy()
        comp_s = p.index.dayofweek.map(g_sett).to_numpy()
        residuo = p - trend - comp_g - comp_s
    except Exception:
        return dict(vuoto)
    out = dict(vuoto)
    out["n_ore"] = len(p)
    out["trend"] = trend
    out["residuo"] = residuo
    out["pattern_giornaliero"] = g_giorno
    out["pattern_settimanale"] = g_sett
    try:
        var_tot = float(p.var())
        var_res = float(residuo.var())
        if var_tot > 0:
            out["quota_spiegata"] = round(max(0.0, 1.0 - var_res / var_tot), 4)
        out["std_residuo"] = round(float(residuo.std()), 2)
        if len(residuo):
            iq = residuo.abs().idxmax()
            out["shock_max"] = round(float(residuo.loc[iq]), 2)
            out["shock_quando"] = iq
    except Exception:
        pass
    try:
        df_e = pd.DataFrame({
            "Data/ora": p.index,
            "Prezzo (€/MWh)": p.values.round(2),
            "Trend (€/MWh)": trend.values.round(2),
            "Stag. giornaliera (€/MWh)": comp_g.round(2),
            "Stag. settimanale (€/MWh)": comp_s.round(2),
            "Residuo (€/MWh)": residuo.values.round(2),
        }, columns=cols)
        out["df_export"] = df_e
    except Exception:
        pass
    return out


def calcola_sequenze_prezzo(prezzi):
    """Analisi delle sequenze (run) di prezzo: rally = ore consecutive di rialzo,
    drawdown = ore consecutive di ribasso, flat = variazioni nulle.

    A cosa serve: capire quanto durano tipicamente i movimenti direzionali del
    prezzo orario e quanto ampi sono, per calibrare stop, target e timing di
    ingresso. Un rally/drawdown insolitamente lungo rispetto alla storia e'
    un segnale di anomalia; l'ampiezza media delle sequenze misura il
    momentum disponibile ora per ora.

    Metodo (tutto deterministico a parita' di input):
    - diff_i = p_i - p_{i-1}; segno +1 se > 0, -1 se < 0, 0 se nulla;
    - una sequenza e' una run massimale di diff consecutivi con lo stesso
      segno; durata = numero di diff nella run (ore di movimento);
    - ampiezza = prezzo all'ultimo indice della run - prezzo al primo indice
      della run (quindi > 0 per i rally, < 0 per i drawdown);
    - la 'run piu' lunga' e' quella con durata massima; a parita' di durata
      viene riportata la piu' vecchia (deterministico);
    - gli orari con prezzo NaN e i timestamp duplicati (primo valore) vengono
      scartati prima del calcolo.

    prezzi: Series oraria in euro/MWh con indice datetime.
    Ritorna dict con 'n_ore', 'n_rally', 'n_drawdown', 'n_flat',
    'rally_max_ore', 'rally_max_amp', 'rally_max_inizio', 'rally_max_fine',
    'drawdown_max_ore', 'drawdown_max_amp', 'drawdown_max_inizio',
    'drawdown_max_fine', 'durata_media_rally', 'durata_media_drawdown',
    'ampiezza_media_rally', 'ampiezza_media_drawdown', 'df_export'
    (DataFrame delle run con Tipo/Inizio/Fine/Durata/Ampiezza)."""
    cols = ["Tipo", "Inizio", "Fine", "Durata (ore)", "Ampiezza (€/MWh)"]
    vuoto = {"n_ore": 0, "n_rally": 0, "n_drawdown": 0, "n_flat": 0,
             "rally_max_ore": None, "rally_max_amp": None,
             "rally_max_inizio": None, "rally_max_fine": None,
             "drawdown_max_ore": None, "drawdown_max_amp": None,
             "drawdown_max_inizio": None, "drawdown_max_fine": None,
             "durata_media_rally": None, "durata_media_drawdown": None,
             "ampiezza_media_rally": None, "ampiezza_media_drawdown": None,
             "df_export": pd.DataFrame(columns=cols)}
    try:
        p = prezzi.astype(float).dropna()
        p = p[~p.index.duplicated(keep="first")].sort_index()
    except Exception:
        return dict(vuoto)
    if len(p) == 0:
        return dict(vuoto)
    out = dict(vuoto)
    out["n_ore"] = len(p)
    if len(p) < 2:
        return out
    try:
        diffs = p.diff().iloc[1:]
        idx = p.index
        segni = diffs.apply(lambda d: 1 if d > 0 else (-1 if d < 0 else 0))
        runs = []  # (tipo, i0, i1, durata, ampiezza)
        s0 = None
        j0 = None
        for j, s in enumerate(segni.tolist()):
            if s != s0:
                if s0 is not None:
                    i1 = j  # diffs j-1 e' l'ultima della run; prezzo all'indice j
                    i0 = j0  # prima diff della run; prezzo all'indice j0
                    amp = float(p.iloc[i1] - p.iloc[i0])
                    runs.append((s0, idx[i0], idx[i1], i1 - i0, amp))
                s0 = s
                j0 = j
        if s0 is not None:
            i1 = len(segni)
            i0 = j0
            amp = float(p.iloc[i1] - p.iloc[i0])
            runs.append((s0, idx[i0], idx[i1], i1 - i0, amp))
    except Exception:
        return dict(vuoto)
    rally = [r for r in runs if r[0] == 1]
    draw = [r for r in runs if r[0] == -1]
    flat = [r for r in runs if r[0] == 0]
    out["n_rally"] = len(rally)
    out["n_drawdown"] = len(draw)
    out["n_flat"] = len(flat)
    if rally:
        r_max = max(rally, key=lambda r: r[3])
        out["rally_max_ore"] = r_max[3]
        out["rally_max_amp"] = round(r_max[4], 2)
        out["rally_max_inizio"] = r_max[1]
        out["rally_max_fine"] = r_max[2]
        out["durata_media_rally"] = round(sum(r[3] for r in rally) / len(rally), 2)
        out["ampiezza_media_rally"] = round(sum(r[4] for r in rally) / len(rally), 2)
    if draw:
        d_max = max(draw, key=lambda r: r[3])
        out["drawdown_max_ore"] = d_max[3]
        out["drawdown_max_amp"] = round(d_max[4], 2)
        out["drawdown_max_inizio"] = d_max[1]
        out["drawdown_max_fine"] = d_max[2]
        out["durata_media_drawdown"] = round(sum(r[3] for r in draw) / len(draw), 2)
        out["ampiezza_media_drawdown"] = round(sum(r[4] for r in draw) / len(draw), 2)
    try:
        nomi = {1: "Rally", -1: "Drawdown", 0: "Flat"}
        righe = [{
            "Tipo": nomi[r[0]],
            "Inizio": r[1],
            "Fine": r[2],
            "Durata (ore)": r[3],
            "Ampiezza (€/MWh)": round(r[4], 2),
        } for r in runs]
        out["df_export"] = pd.DataFrame(righe, columns=cols)
    except Exception:
        pass
    return out


def calcola_valore_flessibilita(prezzi, mw_f1, mw_f2, mw_f3, mw_taglio, ore_top):
    """Valore economico della flessibilita' (curtailment / peak shaving):
    tagliare mw_taglio MW di carico nelle ore_top ore piu' care del periodo.

    Dato un profilo di carico (MW prelevati in ciascuna fascia F1/F2/F3), si
    ordinano le ore per COSTO orario (prezzo x MW) decrescente e si prendono
    le prime ore_top. In ciascuna ora selezionata il carico viene ridotto di
    min(mw_taglio, mw_ora) MW (non si taglia piu' del carico presente in
    quell'ora). Il risparmio stimato e' la somma di prezzo x MW tagliati
    sulle ore selezionate: e' il business case di un programma di demand
    response (interrompibilita', spegnimento dei carichi non prioritari
    nelle ore di picco).

    A cosa serve: quantificare in euro quanto vale la flessibilita' di un
    sito. A differenza dello shifting (che SPOSTA i consumi senza ridurli),
    qui il consumo si RIDUCE davvero nelle ore care: il risparmio e' netto,
    ma si rinuncia a produrre/consumare in quelle ore.

    Metodo (tutto deterministico a parita' di input):
    - ore ordinate per costo orario decrescente; a pari costo viene presa
      prima l'ora piu' vecchia (ordinamento stabile);
    - taglio_j = min(mw_taglio, mw_ora_j); 1 ora = 1 MWh per ogni MW tagliato;
    - risparmio_j = prezzo_j x taglio_j.

    prezzi: Series oraria in euro/MWh con indice datetime.
    mw_f1/mw_f2/mw_f3: MW del profilo per fascia. mw_taglio: MW tagliabili
    (>= 0). ore_top: numero di ore piu' care da includere (intero >= 0).

    NaN-safe: ore con prezzo NaN ignorate. Serie vuota, MW tutti a zero,
    mw_taglio o ore_top pari a zero -> valori neutrali (le statistiche di
    periodo sono comunque calcolate). Se tra le ore selezionate compaiono
    prezzi negativi, il taglio genera una perdita (si rinuncia a consumare
    quando si e' pagati per farlo): il risparmio puo' quindi risultare
    negativo.

    Ritorna dict con 'n_ore', 'mwh' (MWh totali del periodo), 'totale'
    (costo € senza taglio), 'ore_taglio' (ore con taglio effettivo > 0),
    'mwh_tagliati', 'risparmio' (€), 'risparmio_pct' (% sul totale, None se
    totale <= 0), 'prezzo_medio_taglio' (€/MWh medio ponderato sulle ore
    tagliate, None se nessun taglio), 'prezzo_medio_periodo',
    'mensile' (DataFrame 'Mese', 'Ore taglio', 'MWh tagliati',
    'Risparmio (€)', 'Risparmio %'), 'df_export' (DataFrame 'Data e ora',
    'Fascia', 'Prezzo (€/MWh)', 'Carico (MW)', 'Taglio (MW)',
    'Risparmio (€)').
    """
    cols_m = ["Mese", "Ore taglio", "MWh tagliati", "Risparmio (€)", "Risparmio %"]
    cols_e = ["Data e ora", "Fascia", "Prezzo (€/MWh)", "Carico (MW)",
              "Taglio (MW)", "Risparmio (€)"]
    vuoto = {"n_ore": 0, "mwh": 0.0, "totale": 0.0, "ore_taglio": 0,
             "mwh_tagliati": 0.0, "risparmio": 0.0, "risparmio_pct": None,
             "prezzo_medio_taglio": None, "prezzo_medio_periodo": None,
             "mensile": pd.DataFrame(columns=cols_m),
             "df_export": pd.DataFrame(columns=cols_e)}
    try:
        p = prezzi.astype(float).dropna()
        p = p[~p.index.duplicated(keep="first")].sort_index()
    except Exception:
        return dict(vuoto)
    if len(p) == 0:
        return dict(vuoto)
    out = dict(vuoto)
    out["n_ore"] = len(p)
    try:
        fasce = p.index.map(fascia_oraria)
    except Exception:
        return out
    mw_map = {"F1": max(0.0, float(mw_f1)), "F2": max(0.0, float(mw_f2)),
              "F3": max(0.0, float(mw_f3))}
    mw = fasce.map(mw_map).to_numpy(dtype=float)
    prezzi_v = p.to_numpy(dtype=float)
    costo_orario = prezzi_v * mw
    out["mwh"] = float(mw.sum())
    out["totale"] = float(costo_orario.sum())
    out["prezzo_medio_periodo"] = round(float(p.mean()), 2)
    try:
        k = max(0, int(ore_top))
        taglio = max(0.0, float(mw_taglio))
    except Exception:
        return out
    if k == 0 or taglio <= 0 or (mw <= 0).all():
        return out
    ordine = np.argsort(-costo_orario, kind="stable")[:k]
    sel_idx = p.index[ordine]
    sel_fasce = fasce[ordine]
    sel_mw = mw[ordine]
    sel_p = prezzi_v[ordine]
    tag_j = np.minimum(taglio, sel_mw)
    risp_j = sel_p * tag_j
    out["ore_taglio"] = int((tag_j > 0).sum())
    out["mwh_tagliati"] = round(float(tag_j.sum()), 3)
    out["risparmio"] = round(float(risp_j.sum()), 2)
    if out["totale"] > 0:
        out["risparmio_pct"] = round(out["risparmio"] / out["totale"] * 100, 2)
    if out["mwh_tagliati"] > 0:
        out["prezzo_medio_taglio"] = round(float(risp_j.sum() / tag_j.sum()), 2)
    try:
        mesi = sel_idx.to_period("M").astype(str)
        righe_m = []
        for m in sorted(set(mesi.tolist())):
            mm = mesi == m
            r_m = float(risp_j[mm].sum())
            righe_m.append({
                "Mese": m,
                "Ore taglio": int((tag_j[mm] > 0).sum()),
                "MWh tagliati": round(float(tag_j[mm].sum()), 3),
                "Risparmio (€)": round(r_m, 2),
                "Risparmio %": (round(r_m / out["totale"] * 100, 2)
                                if out["totale"] > 0 else None),
            })
        out["mensile"] = pd.DataFrame(righe_m, columns=cols_m)
        righe_e = [{
            "Data e ora": ts,
            "Fascia": fa,
            "Prezzo (€/MWh)": round(float(pr), 2),
            "Carico (MW)": round(float(c), 3),
            "Taglio (MW)": round(float(t), 3),
            "Risparmio (€)": round(float(r), 2),
        } for ts, fa, pr, c, t, r in zip(sel_idx, sel_fasce, sel_p, sel_mw,
                                         tag_j, risp_j)]
        out["df_export"] = pd.DataFrame(righe_e, columns=cols_e)
    except Exception:
        pass
    return out


def calcola_top_ore_costo(prezzi, mw_f1, mw_f2, mw_f3, top_n=10):
    """Classifica delle ore piu' costose del periodo (granularita' oraria).

    Dato un profilo di carico (MW prelevati in ciascuna fascia F1/F2/F3),
    calcola il costo orario (prezzo spot x MW della fascia) e classifica le
    ore per costo decrescente. Produce anche la distribuzione del costo per
    ora del giorno (0-23) e per fascia: utile per capire DOVE si concentra
    la bolletta (es. 'le 18:00-19:00 dei giorni feriali') e per decidere dove
    agire (shifting, curtailment, rinegoziazione delle fasce).

    Differenza rispetto agli altri tab: Top giorni di costo ragiona per
    GIORNO di calendario (domanda di tesoreria: 'quanto mi e' costato il
    15/09?'); Picchi guarda le ORE di prezzo estremo (non di costo);
    Valore flessibilita' mostra le ore migliori per il TAGLIO (risparmio
    netto del curtailment). Qui la domanda e' 'quali ore mi sono costate di
    piu', prezzo x carico': la classifica grezza del costo orario, senza
    ipotesi di taglio.

    NaN-safe: ore con prezzo NaN ignorate. Serie vuota o tutti i MW a zero ->
    KPI a None e DataFrame con le colonne giuste ma vuoti. Se il costo totale
    e' <= 0 (prezzi negativi prevalenti), le quote percentuali sono None.

    Ritorna dict con 'n_ore', 'mwh_tot', 'costo_tot', 'costo_medio_orario',
    'ora_max_data'/'ora_max_costo' (None se nessuna ora valida),
    'rapporto_max_medio' (None se medio <= 0), 'quota_top5pct' (% del costo
    generata dal 5% di ore piu' costose, None se totale <= 0),
    'ora_max_giorno' (ora 0-23 con il costo totale maggiore nel periodo),
    'top_n', 'top' (DataFrame: Data e ora, Fascia, Prezzo (€/MWh), Carico
    (MW), Costo (€), Quota % sul totale), 'per_ora' (DataFrame con tutte le
    24 ore: Ora, Ore osservate, Costo (€), Quota %) e 'per_fascia'
    (DataFrame: Fascia, Ore, MWh, Costo (€), Quota %)."""
    cols_t = ["Data e ora", "Fascia", "Prezzo (€/MWh)", "Carico (MW)",
              "Costo (€)", "Quota % sul totale"]
    cols_o = ["Ora", "Ore osservate", "Costo (€)", "Quota %"]
    cols_f = ["Fascia", "Ore", "MWh", "Costo (€)", "Quota %"]
    vuoto = {"n_ore": 0, "mwh_tot": 0.0, "costo_tot": None,
             "costo_medio_orario": None, "ora_max_data": None,
             "ora_max_costo": None, "rapporto_max_medio": None,
             "quota_top5pct": None, "ora_max_giorno": None,
             "top_n": max(1, int(top_n or 10)),
             "top": pd.DataFrame(columns=cols_t),
             "per_ora": pd.DataFrame(columns=cols_o),
             "per_fascia": pd.DataFrame(columns=cols_f)}
    try:
        p = prezzi.astype(float).dropna()
        p = p[~p.index.duplicated(keep="first")].sort_index()
    except Exception:
        return dict(vuoto)
    if len(p) == 0:
        return dict(vuoto)
    out = dict(vuoto)
    out["n_ore"] = len(p)
    try:
        fasce = p.index.map(fascia_oraria)
    except Exception:
        return out
    mw_map = {"F1": max(0.0, float(mw_f1)), "F2": max(0.0, float(mw_f2)),
              "F3": max(0.0, float(mw_f3))}
    try:
        idx = p.index
        idxn = idx.tz_localize(None) if idx.tz is not None else idx
        ore = idxn.hour.to_numpy()
    except Exception:
        return out
    mw = fasce.map(mw_map).to_numpy(dtype=float)
    pv = p.to_numpy(dtype=float)
    costo = pv * mw
    mwh = float(mw.sum())
    totale = float(costo.sum())
    medio = float(costo.mean())
    cmax = float(costo.max())
    out["mwh_tot"] = round(mwh, 1)
    out["costo_tot"] = round(totale, 2)
    out["costo_medio_orario"] = round(medio, 2)
    out["rapporto_max_medio"] = round(cmax / medio, 2) if medio > 0 else None
    if mwh <= 0:
        return out
    imax = int(np.argmax(costo))
    out["ora_max_data"] = p.index[imax]
    out["ora_max_costo"] = round(cmax, 2)
    k5 = max(1, int(round(len(costo) * 0.05)))
    q5 = (float(np.sort(costo)[::-1][:k5].sum() / totale * 100)
          if totale > 0 else None)
    out["quota_top5pct"] = round(q5, 1) if q5 is not None else None
    try:
        ordine = np.argsort(-costo, kind="stable")
        tn = out["top_n"]
        sel = ordine[:tn]
        quote = np.where(totale > 0, costo[sel] / totale * 100, np.nan)
        righe_t = [{
            "Data e ora": p.index[i],
            "Fascia": str(fasce[i]),
            "Prezzo (€/MWh)": round(float(pv[i]), 2),
            "Carico (MW)": round(float(mw[i]), 3),
            "Costo (€)": round(float(costo[i]), 2),
            "Quota % sul totale": (round(float(q), 2)
                                   if not np.isnan(q) else None),
        } for i, q in zip(sel.tolist(), quote)]
        out["top"] = pd.DataFrame(righe_t, columns=cols_t)
        righe_o = []
        for h in range(24):
            m = ore == h
            co = float(costo[m].sum())
            righe_o.append({
                "Ora": f"{h:02d}:00",
                "Ore osservate": int(m.sum()),
                "Costo (€)": round(co, 2),
                "Quota %": (round(co / totale * 100, 2)
                            if totale > 0 else None),
            })
        out["per_ora"] = pd.DataFrame(righe_o, columns=cols_o)
        out["ora_max_giorno"] = int(ore[np.argmax(costo)])
        righe_f = []
        for fa in ["F1", "F2", "F3"]:
            m = np.array([str(x) == fa for x in fasce])
            co = float(costo[m].sum())
            righe_f.append({
                "Fascia": fa,
                "Ore": int(m.sum()),
                "MWh": round(float(mw[m].sum()), 1),
                "Costo (€)": round(co, 2),
                "Quota %": (round(co / totale * 100, 2)
                            if totale > 0 else None),
            })
        out["per_fascia"] = pd.DataFrame(righe_f, columns=cols_f)
    except Exception:
        pass
    return out


def calcola_ohlc_giornaliero(prezzi):
    """Candele giornaliere OHLC del prezzo spot orario.

    Per ogni giorno di calendario: Apertura = prezzo dell'ora 00:00, Massimo
    e Minimo = estremi delle ore osservate, Chiusura = prezzo dell'ultima
    ora del giorno. Escursione = max - min (quanto si e' mosso il mercato in
    giornata), Corpo = close - open, Direzione = rialzo (close > open),
    ribasso (close < open), flat (close == open).

    Differenza rispetto agli altri tab: 'Rampe di prezzo' guarda la variazione
    ORA-su-ora (nervosismo ad alta frequenza); 'Sequenze' i rally/drawdown
    plurigiornalieri; qui la grana e' il GIORNO di mercato, la vista da
    trader per decidere il timing degli acquisti sulla borsa day-ahead.

    NaN-safe: ore con prezzo NaN ignorate. Serie vuota, indice non datetime,
    duplicato o tutti NaN -> KPI a None e DataFrame vuoto. Giorni con 23/25
    ore (DST) contribuiscono solo con le ore osservate. Il rapporto
    escursione-media/prezzo-medio e' None se il prezzo medio <= 0 (serie con
    molti prezzi negativi).

    Ritorna dict con 'n_giorni', 'escursione_media', 'escursione_max',
    'giorno_max_escursione' (datetime.date o None), 'quota_rialzo_pct',
    'quota_ribasso_pct', 'rapporto_esc_media_prezzo_medio' (None se prezzo
    medio <= 0), 'prezzo_medio', 'df' (DataFrame: Giorno, Ore,
    Apertura/ Massimo/ Minimo/ Chiusura (€/MWh), Escursione (€/MWh),
    Corpo (€/MWh), Direzione)."""
    cols = ["Giorno", "Ore", "Apertura (€/MWh)", "Massimo (€/MWh)",
            "Minimo (€/MWh)", "Chiusura (€/MWh)", "Escursione (€/MWh)",
            "Corpo (€/MWh)", "Direzione"]
    vuoto = {"n_giorni": 0, "escursione_media": None, "escursione_max": None,
             "giorno_max_escursione": None, "quota_rialzo_pct": None,
             "quota_ribasso_pct": None,
             "rapporto_esc_media_prezzo_medio": None, "prezzo_medio": None,
             "df": pd.DataFrame(columns=cols)}
    try:
        p = prezzi.astype(float).dropna()
        p = p[~p.index.duplicated(keep="first")].sort_index()
    except Exception:
        return dict(vuoto)
    if len(p) == 0:
        return dict(vuoto)
    try:
        idx = p.index
        if not isinstance(idx, pd.DatetimeIndex):
            return dict(vuoto)
        giorni = idx.floor("D")
    except Exception:
        return dict(vuoto)
    out = dict(vuoto)
    try:
        righe = []
        for g, grp in p.groupby(giorni):
            o = float(grp.iloc[0])
            h = float(grp.max())
            l = float(grp.min())
            c = float(grp.iloc[-1])
            corpo = c - o
            if corpo > 0:
                d = "rialzo"
            elif corpo < 0:
                d = "ribasso"
            else:
                d = "flat"
            righe.append({
                "Giorno": g.date() if hasattr(g, "date") else g,
                "Ore": len(grp),
                "Apertura (€/MWh)": round(o, 2),
                "Massimo (€/MWh)": round(h, 2),
                "Minimo (€/MWh)": round(l, 2),
                "Chiusura (€/MWh)": round(c, 2),
                "Escursione (€/MWh)": round(h - l, 2),
                "Corpo (€/MWh)": round(corpo, 2),
                "Direzione": d,
            })
    except Exception:
        return out
    if not righe:
        return out
    df = pd.DataFrame(righe, columns=cols)
    out["df"] = df
    out["n_giorni"] = len(df)
    esc = df["Escursione (€/MWh)"].to_numpy(dtype=float)
    corpi = df["Corpo (€/MWh)"].to_numpy(dtype=float)
    out["escursione_media"] = round(float(np.mean(esc)), 2)
    out["escursione_max"] = round(float(np.max(esc)), 2)
    out["giorno_max_escursione"] = df.loc[df["Escursione (€/MWh)"].idxmax(),
                                          "Giorno"]
    out["quota_rialzo_pct"] = round(float((corpi > 0).mean()) * 100, 1)
    out["quota_ribasso_pct"] = round(float((corpi < 0).mean()) * 100, 1)
    pm = float(p.mean())
    out["prezzo_medio"] = round(pm, 2)
    out["rapporto_esc_media_prezzo_medio"] = (
        round(float(np.mean(esc)) / pm, 3) if pm > 0 else None)
    return out


def calcola_drawdown(prezzi, soglia_eur=20.0):
    """Analisi drawdown (crolli dal picco) della serie oraria dei prezzi.

    DRAWDOWN = calo dal massimo corrente (running max) fino al punto di
    svolta piu' basso prima di un nuovo massimo: picco -> minimo (ore di
    calo) -> recupero al livello del picco (ore di recupero, None se non
    recuperato entro fine serie). Il recupero include l'ora del picco
    successivo: e' la prima ora in cui il prezzo torna di certo al livello
    del picco (nuovo massimo storico). E' la misura da risk manager: non quanto
    si muove il prezzo ora-su-ora (tab 'Rampe di prezzo') ne' le sequenze
    consecutive (tab 'Sequenze'), ma quanto perde un acquirente che ha
    comprato al picco e quanto tempo serve per tornare in pari.

    Differenza rispetto agli altri tab: 'Sequenze' conta le ore di fila in
    calo; 'Candele OHLC' guarda l'escursione giornaliera; qui ogni episodio
    e' ancorato a un PICCO e include il tempo di recupero — la domanda
    operativa per chi copre il rischio prezzo: "se compro male, quanto
    ci mette il mercato a tornare dove ho pagato?".

    NaN-safe: ore NaN ignorate. Serie vuota, indice non datetime,
    duplicato o tutti NaN -> KPI a None e DataFrame vuoto. Prezzi negativi:
    la profondita' in euro resta valida; la profondita' % e' None quando il
    picco <= 0 (denominatore non significativo). Giorni con 23/25 ore (DST)
    contribuiscono con le ore osservate (logica posizionale).

    Ritorna dict con 'n_ore', 'max_drawdown_eur', 'max_drawdown_pct' (None
    se picco <= 0), 'picco_max_drawdown' (Timestamp o None), 'n_episodi',
    'n_oltre_soglia' (episodi con profondita' >= soglia_eur),
    'tempo_medio_recupero_ore' (None se nessun recupero concluso),
    'drawdown_attuale_eur', 'picco_attuale_eur', 'picco_attuale_ts',
    'df' (episodi ordinati per profondita' decrescente: Picco, Picco (€/MWh),
    Minimo ora, Minimo (€/MWh), Recupero, Profondita' (€/MWh),
    Profondita' (%), Ore di calo, Ore di recupero)."""


    cols = ["Picco", "Picco (€/MWh)", "Minimo ora", "Minimo (€/MWh)",
            "Recupero", "Profondita' (€/MWh)", "Profondita' (%)",
            "Ore di calo", "Ore di recupero"]
    vuoto = {"n_ore": 0, "max_drawdown_eur": None, "max_drawdown_pct": None,
             "picco_max_drawdown": None, "n_episodi": 0, "n_oltre_soglia": 0,
             "tempo_medio_recupero_ore": None, "drawdown_attuale_eur": None,
             "picco_attuale_eur": None, "picco_attuale_ts": None,
             "df": pd.DataFrame(columns=cols)}
    try:
        p = prezzi.astype(float).dropna()
        p = p[~p.index.duplicated(keep="first")].sort_index()
    except Exception:
        return dict(vuoto)
    if len(p) == 0:
        return dict(vuoto)
    try:
        if not isinstance(p.index, pd.DatetimeIndex):
            return dict(vuoto)
    except Exception:
        return dict(vuoto)
    try:
        soglia_eur = float(soglia_eur)
    except Exception:
        return dict(vuoto)

    out = dict(vuoto)
    vals = p.to_numpy(dtype=float)
    idx = p.index
    n = len(p)
    runmax = np.maximum.accumulate(vals)
    dd = runmax - vals
    out["n_ore"] = n
    out["max_drawdown_eur"] = round(float(dd.max()), 2)
    out["picco_attuale_eur"] = round(float(runmax[-1]), 2)
    out["picco_attuale_ts"] = idx[int(np.argmax(runmax == runmax[-1]) if n else 0)] if n else None
    out["drawdown_attuale_eur"] = round(float(dd[-1]), 2)

    # Picchi: posizioni con nuovo massimo stretto. Per ogni picco i (tranne
    # l'ultimo) l'episodio va dal picco al minimo prima del picco
    # successivo; il recupero e' la prima ora con prezzo >= picco.
    picchi = [0] + [i for i in range(1, n) if vals[i] > runmax[i - 1]]
    episodi = []
    for k, pi in enumerate(picchi):
        fine = picchi[k + 1] if k + 1 < len(picchi) else n
        if fine - pi < 2:
            continue
        segmento = vals[pi:fine]
        rel_min = int(np.argmin(segmento))
        if rel_min == 0:
            continue  # mai sceso dopo il picco
        ti = pi + rel_min
        profondita = float(vals[pi] - vals[ti])
        if profondita <= 0:
            continue
        # recupero: prima ora dopo il minimo con prezzo >= picco.
        # Include l'ora del picco successivo (fine): e' la prima ora in cui
        # il prezzo torna di certo al livello del picco (nuovo massimo
        # storico). Prima era esclusa -> episodi di fatto recuperati
        # risultavano "aperti" e il tempo medio di recupero restava n.d.
        fine_rec = fine + 1 if k + 1 < len(picchi) else n
        rec_i = None
        for j in range(ti + 1, fine_rec):
            if vals[j] >= vals[pi]:
                rec_i = j
                break
        prof_pct = (round(profondita / vals[pi] * 100, 1)
                    if vals[pi] > 0 else None)
        episodi.append({
            "Picco": idx[pi],
            "Picco (€/MWh)": round(float(vals[pi]), 2),
            "Minimo ora": idx[ti],
            "Minimo (€/MWh)": round(float(vals[ti]), 2),
            "Recupero": idx[rec_i] if rec_i is not None else pd.NaT,
            "Profondita' (€/MWh)": round(profondita, 2),
            "Profondita' (%)": prof_pct,
            "Ore di calo": int(ti - pi),
            "Ore di recupero": int(rec_i - ti) if rec_i is not None else np.nan,
        })
    episodi.sort(key=lambda e: e["Profondita' (€/MWh)"], reverse=True)
    df_ep = pd.DataFrame(episodi, columns=cols)
    out["df"] = df_ep
    out["n_episodi"] = len(episodi)
    out["n_oltre_soglia"] = int((df_ep["Profondita' (€/MWh)"] >= soglia_eur).sum()) \
        if len(df_ep) else 0
    if out["max_drawdown_eur"] is not None and len(episodi):
        picco_dd = episodi[0]["Picco (€/MWh)"]
        out["picco_max_drawdown"] = episodi[0]["Picco"]
        out["max_drawdown_pct"] = (round(out["max_drawdown_eur"] / picco_dd * 100, 1)
                                   if picco_dd > 0 else None)
    rec = df_ep["Ore di recupero"].dropna() if len(df_ep) else pd.Series(dtype=float)
    out["tempo_medio_recupero_ore"] = (round(float(rec.mean()), 1)
                                       if len(rec) else None)
    return out


def calcola_mean_reversion(prezzi, min_coppie=50):
    """Mean reversion del prezzo orario via AR(1): x_t = a + b*x_{t-1} + e.

    Il coefficiente b misura la PERSISTENZA: b vicino a 1 = il prezzo di
    ieri sera conta ancora molto (shock lenti a rientrare); b vicino a 0
    = ogni ora riparte quasi da zero (shock rientrati in fretta).
    L'HALF-LIFE = -ln(2)/ln(b) e' il tempo in cui uno shock si dimezza:
    la domanda operativa "dopo un picco, quanto ci mette il prezzo a
    tornare verso la media?" — chiave per decidere se comprare subito
    o aspettare.

    Differenza rispetto agli altri tab: 'Autocorrelazione' mostra la
    memoria a ogni lag, 'Sequenze' conta le ore di fila in calo,
    'Decomposizione' separa trend e stagionalita'; qui un SOLO numero
    (half-life) riassume la velocita' di rientro degli shock, con la
    scomposizione per mese per vedere i cambi di regime.

    NaN-safe: ore NaN ignorate (coppie con un NaN scartate). Serie vuota,
    indice non datetime, duplicato, costante o < min_coppie coppie valide
    -> statistiche a None. Prezzi negativi: nessun problema (OLS su livelli,
    non su log). Giorni con 23/25 ore (DST): logica posizionale sulle ore
    osservate. b <= 0 o b >= 1 -> half-life None (non mean-reverting).

    Ritorna dict con 'n_ore', 'n_coppie', 'b', 'a', 'r2', 'half_life_ore',
    'std_residui', 'media', 'std', 'ultimo_prezzo', 'ultima_ora',
    'z_ultimo', 'regime' (molto rapida/rapida/moderata/lenta/molto
    lenta/assente), 'df_mesi' (Mese, Ore, AR(1), Half-life (ore), R2)."""

    cols_mesi = ["Mese", "Ore", "AR(1)", "Half-life (ore)", "R2"]
    vuoto = {"n_ore": 0, "n_coppie": 0, "b": None, "a": None, "r2": None,
             "half_life_ore": None, "std_residui": None, "media": None,
             "std": None, "ultimo_prezzo": None, "ultima_ora": None,
             "z_ultimo": None, "regime": "assente",
             "df_mesi": pd.DataFrame(columns=cols_mesi)}
    try:
        p = prezzi.astype(float).dropna()
        p = p[~p.index.duplicated(keep="first")].sort_index()
    except Exception:
        return dict(vuoto)
    if len(p) == 0:
        return dict(vuoto)
    try:
        if not isinstance(p.index, pd.DatetimeIndex):
            return dict(vuoto)
    except Exception:
        return dict(vuoto)

    def _fit_ar1(v):
        """OLS x_t su x_{t-1}; ritorna (b, a, r2, resid_std) o None."""
        if len(v) < 2:
            return None
        x_lag, x_lead = v[:-1], v[1:]
        mask = np.isfinite(x_lag) & np.isfinite(x_lead)
        x_lag, x_lead = x_lag[mask], x_lead[mask]
        if len(x_lag) < 2:
            return None
        var_lag = float(np.var(x_lag))
        if var_lag <= 0:
            return None  # serie costante
        ml_lag, ml_lead = float(np.mean(x_lag)), float(np.mean(x_lead))
        b = float(np.mean((x_lag - ml_lag) * (x_lead - ml_lead)) / var_lag)
        a = ml_lead - b * ml_lag
        resid = x_lead - (a + b * x_lag)
        ss_res = float(np.sum(resid ** 2))
        ss_tot = float(np.sum((x_lead - ml_lead) ** 2))
        r2 = (1.0 - ss_res / ss_tot) if ss_tot > 0 else None
        return b, a, r2, float(np.std(resid, ddof=1)) if len(resid) > 1 else 0.0

    def _half_life(b):
        if b is None or not (0.0 < b < 1.0):
            return None
        try:
            return float(-np.log(2.0) / np.log(b))
        except (ValueError, ZeroDivisionError):
            return None

    def _regime(hl):
        if hl is None:
            return "assente"
        if hl < 24:
            return "molto rapida"
        if hl < 72:
            return "rapida"
        if hl < 168:
            return "moderata"
        if hl < 720:
            return "lenta"
        return "molto lenta"

    out = dict(vuoto)
    vals = p.to_numpy(dtype=float)
    out["n_ore"] = len(vals)
    out["media"] = round(float(np.mean(vals)), 2)
    s = float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0
    out["std"] = round(s, 2)
    out["ultimo_prezzo"] = round(float(vals[-1]), 2)
    out["ultima_ora"] = p.index[-1]
    out["z_ultimo"] = (round((float(vals[-1]) - float(np.mean(vals))) / s, 2)
                       if s > 0 else None)

    fit = _fit_ar1(vals)
    if fit is None:
        return out
    b, a, r2, resid_std = fit
    n_coppie = int(np.sum(np.isfinite(vals[:-1]) & np.isfinite(vals[1:])))
    out["n_coppie"] = n_coppie
    if n_coppie < min_coppie:
        return out
    out["b"] = round(b, 4)
    out["a"] = round(a, 2)
    out["r2"] = round(r2, 3) if r2 is not None else None
    out["std_residui"] = round(resid_std, 2)
    hl = _half_life(b)
    out["half_life_ore"] = round(hl, 1) if hl is not None else None
    out["regime"] = _regime(hl)

    # Half-life per mese (cambi di regime): min 100 coppie valide
    righe = []
    for (anno, mese), grp in p.groupby([p.index.year, p.index.month]):
        gv = grp.to_numpy(dtype=float)
        ncp = int(np.sum(np.isfinite(gv[:-1]) & np.isfinite(gv[1:])))
        if ncp < 100:
            continue
        gf = _fit_ar1(gv)
        if gf is None:
            continue
        gb, _, gr2, _ = gf
        ghl = _half_life(gb)
        righe.append({
            "Mese": f"{anno:04d}-{mese:02d}",
            "Ore": len(gv),
            "AR(1)": round(gb, 4),
            "Half-life (ore)": round(ghl, 1) if ghl is not None else np.nan,
            "R2": round(gr2, 3) if gr2 is not None else np.nan,
        })
    out["df_mesi"] = pd.DataFrame(righe, columns=cols_mesi)
    return out


def calcola_strip_forward(prezzi, freq="ME", ora_peak_inizio=8, ora_peak_fine=20):
    """Strip forward impliciti dal day-ahead storico.

    Dallo storico dei prezzi orari calcola, per ogni periodo di consegna
    (mese / trimestre / anno), il prezzo "implicito" di un contratto
    forward su quel periodo:
      - BASE: media di tutte le ore del periodo
      - PEAK: media delle ore lun-ven dalle ore_peak_inizio alle ore_peak_fine
        (escluse), default 8:00-20:00
      - OFFPEAK: media di tutte le altre ore
      - SPREAD peak-offpeak e PREMIO peak vs base (%).

    Uso operativo: confrontare le quotazioni dei broker (che quotano strip
    mensili/trimestrali/annuali base e peak) con il valore "implicito"
    dello storico — se il forward quotato e' sopra lo strip implicito, il
    mercato prezza un premio di rischio; se sotto, un'opportunita'.

    Differenza rispetto agli altri tab: 'Base/Peak mensile' mostra i prezzi
    base/peak mese per mese come indicatore storico; qui il framing e'
    contrattuale (strip = prodotto forward scambiato sul mercato) con
    spread e premio peak vs base, su tre granularita' (mese/trimestre/anno).

    NaN-safe: ore NaN ignorate, ore duplicate rimosse (prima occorrenza).
    Serie vuota, indice non datetime -> n_strip 0 e df vuoto. Weekday-only
    peak con dati solo weekend -> Peak NaN sullo strip (non errore).
    Mesi DST con 23/25 ore: conteggio ore effettive, media sulle ore
    osservate. Base = 0 -> premio NaN (evita divisione per zero).
    freq deve essere 'ME', 'QE' o 'YE', altrimenti ValueError.

    Ritorna dict con 'freq', 'n_strip', 'n_ore', 'df' (colonne: 'Strip',
    'Ore', 'Base (€/MWh)', 'Peak (€/MWh)', 'Offpeak (€/MWh)',
    'Spread peak-offpeak (€/MWh)', 'Premio peak vs base (%)'),
    'base_medio', 'premio_peak_medio', 'spread_medio'."""

    cols = ["Strip", "Ore", "Base (€/MWh)", "Peak (€/MWh)",
            "Offpeak (€/MWh)", "Spread peak-offpeak (€/MWh)",
            "Premio peak vs base (%)"]
    vuoto = {"freq": freq, "n_strip": 0, "n_ore": 0,
             "df": pd.DataFrame(columns=cols), "base_medio": None,
             "premio_peak_medio": None, "spread_medio": None}
    if freq not in ("ME", "QE", "YE"):
        raise ValueError("freq deve essere 'ME', 'QE' o 'YE'")
    try:
        p = prezzi.astype(float)
        p = p[~p.index.duplicated(keep="first")].sort_index()
    except Exception:
        return dict(vuoto)
    if len(p) == 0:
        return dict(vuoto)
    try:
        if not isinstance(p.index, pd.DatetimeIndex):
            return dict(vuoto)
    except Exception:
        return dict(vuoto)
    if not (0 <= ora_peak_inizio < ora_peak_fine <= 24):
        raise ValueError("finestra peak non valida")

    idx = p.index
    is_peak = ((idx.dayofweek < 5)
               & (idx.hour >= ora_peak_inizio)
               & (idx.hour < ora_peak_fine))
    # Compatibilita' pandas: alias 'ME'/'QE'/'YE' (pandas>=2.2) con fallback
    # a 'M'/'Q'/'Y' per le versioni precedenti.
    _freq_fallback = {"ME": "M", "QE": "Q", "YE": "Y"}

    def _rs(s):
        try:
            return s.resample(freq)
        except ValueError:
            return s.resample(_freq_fallback[freq])

    # Media sulle ore valide (NaN ignorate): il count usa le ore osservate
    base = _rs(p).mean()
    ore = _rs(p).count()
    peak = _rs(p[is_peak]).mean().reindex(base.index)
    offp = _rs(p[~is_peak]).mean().reindex(base.index)

    if freq == "ME":
        labels = [f"{t.year:04d}-{t.month:02d}" for t in base.index]
    elif freq == "QE":
        labels = [f"{t.year:04d}-Q{t.quarter}" for t in base.index]
    else:
        labels = [f"{t.year:04d}" for t in base.index]

    righe = []
    for lab, b, pk, of, n in zip(labels, base.to_numpy(), peak.to_numpy(),
                                 offp.to_numpy(), ore.to_numpy()):
        if not np.isfinite(b) or n == 0:
            continue
        spread = pk - of if (np.isfinite(pk) and np.isfinite(of)) else np.nan
        premio = (pk - b) / b * 100.0 if (np.isfinite(pk) and b != 0) else np.nan
        righe.append({
            "Strip": lab,
            "Ore": int(n),
            "Base (€/MWh)": round(float(b), 2),
            "Peak (€/MWh)": round(float(pk), 2) if np.isfinite(pk) else np.nan,
            "Offpeak (€/MWh)": round(float(of), 2) if np.isfinite(of) else np.nan,
            "Spread peak-offpeak (€/MWh)": round(float(spread), 2) if np.isfinite(spread) else np.nan,
            "Premio peak vs base (%)": round(float(premio), 2) if np.isfinite(premio) else np.nan,
        })
    df = pd.DataFrame(righe, columns=cols)
    out = dict(vuoto)
    out["n_strip"] = len(df)
    out["n_ore"] = int(ore.sum())
    out["df"] = df
    if len(df):
        out["base_medio"] = round(float(df["Base (€/MWh)"].mean()), 2)
        prem = df["Premio peak vs base (%)"].dropna()
        spr = df["Spread peak-offpeak (€/MWh)"].dropna()
        out["premio_peak_medio"] = round(float(prem.mean()), 2) if len(prem) else None
        out["spread_medio"] = round(float(spr.mean()), 2) if len(spr) else None
    return out


def calcola_climatologia_prezzo(prezzi, soglia=100.0):
    """Climatologia del prezzo: probabilita' di superare una soglia per giorno della settimana e ora.

    Per chi compra/vende energia a termine (o programma flessibilita') conta
    sapere NON solo la media di prezzo, ma con che probabilita' il prezzo
    supera un livello critico (es. costo variabile, strike di un'opzione,
    prezzo dell'offerta da battere) in una data ora del giorno e in un dato
    giorno della settimana. Questa "climatologia" risponde alla domanda
    "a che ora e in che giorno e' piu' probabile che il prezzo superi X €/MWh?".

    Differenza rispetto agli altri tab: 'Persistenza sopra soglia' studia i
    BLOCCHI consecutivi sopra soglia (durata degli eventi); 'Picchi' elenca
    le singole ore estreme; qui si misura la FREQUENZA condizionata al
    calendario (matrice 7x24): una misura di rischio/probabilita', non di
    intensita'. Differisce anche da 'Settimana tipo' che mostra i prezzi
    MEDI: qui le probabilita' di superamento soglia.

    prezzi: Series oraria in €/MWh con indice datetime (tz-aware ok).
    soglia: livello critico in €/MWh (default 100.0); ore con prezzo >= soglia
      contano come "sopra soglia".
    NaN-safe: ore NaN escluse sia dal numeratore che dal denominatore.
    Serie vuota o indice non datetime -> matrice NaN e KPI a None.
    Mesi DST con 23/25 ore: probabilita' calcolate sulle ore osservate.

    Ritorna dict con 'soglia', 'n_ore' (ore osservate), 'quota' (frazione
    globale ore sopra soglia, None se non valutabile), 'matrice' (DataFrame
    7 righe Lun-Dom x 24 colonne ore, probabilita' in % 0-100, NaN dove non ci
    sono osservazioni), 'ore_osservate' (stessa forma, conteggi),
    'media_ora' (DataFrame Ora, Prob %), 'media_giorno' (DataFrame Giorno,
    Prob %), 'ora_picco' (ora, prob %), 'giorno_picco' (nome, prob %),
    'p_max', 'ore_p50' (celle con P>=50%), 'eccedenza_media' (€/MWh medi di
    max(prezzo-soglia,0) sulle ore osservate), 'eccedenza_max'."""

    GIORNI = ["Lunedi'", "Martedi'", "Mercoledi'", "Giovedi'",
              "Venerdi'", "Sabato", "Domenica"]
    cols_g = ["Giorno", "Probabilita' (%)"]
    cols_o = ["Ora", "Probabilita' (%)"]
    cols_t = ["Giorno", "Ora", "Probabilita' (%)", "Ore osservate"]
    mat_vuota = pd.DataFrame(index=GIORNI, columns=list(range(24)), dtype=float)
    cnt_vuota = pd.DataFrame(index=GIORNI, columns=list(range(24)), dtype=float)
    vuoto = {"soglia": None, "n_ore": 0, "quota": None,
             "matrice": mat_vuota, "ore_osservate": cnt_vuota,
             "media_ora": pd.DataFrame(columns=cols_o),
             "media_giorno": pd.DataFrame(columns=cols_g),
             "ora_picco": None, "giorno_picco": None, "p_max": None,
             "ore_p50": 0, "eccedenza_media": None, "eccedenza_max": None,
             "top_celle": pd.DataFrame(columns=cols_t)}
    try:
        soglia = float(soglia)
    except Exception:
        return dict(vuoto)
    try:
        p = prezzi.astype(float)
        p = p[~p.index.duplicated(keep="first")].sort_index()
    except Exception:
        return dict(vuoto)
    try:
        if not isinstance(p.index, pd.DatetimeIndex):
            return dict(vuoto)
    except Exception:
        return dict(vuoto)
    p = p.dropna()
    if len(p) == 0:
        return dict(vuoto)

    idxn = p.index.tz_localize(None) if p.index.tz is not None else p.index
    sopra = (p.values >= soglia).astype(float)
    df = pd.DataFrame({"wd": idxn.weekday, "ora": idxn.hour,
                       "sopra": sopra, "ecc": np.maximum(p.values - soglia, 0.0)})

    mat = ((df.groupby(["wd", "ora"])["sopra"].mean() * 100.0)
             .unstack("ora").reindex(index=range(7), columns=range(24)))
    cnt = (df.groupby(["wd", "ora"])["sopra"].size()
             .unstack("ora").reindex(index=range(7), columns=range(24)))
    mat.index = GIORNI
    cnt.index = GIORNI

    out = dict(vuoto)
    out["soglia"] = soglia
    out["n_ore"] = int(len(df))
    out["quota"] = round(float(sopra.mean()), 4)
    out["matrice"] = mat
    out["ore_osservate"] = cnt
    out["media_ora"] = (pd.DataFrame({"Ora": [f"{h:02d}:00" for h in range(24)],
                                      "Probabilita' (%)": [round(float(v), 1) if pd.notna(v) else float("nan")
                                                            for v in mat.mean(axis=0).to_numpy()]})
                        if mat.notna().any().any() else pd.DataFrame(columns=cols_o))
    mg = mat.mean(axis=1)
    out["media_giorno"] = (pd.DataFrame({"Giorno": GIORNI,
                                         "Probabilita' (%)": [round(float(v), 1) if pd.notna(v) else float("nan")
                                                               for v in mg.to_numpy()]})
                           if mg.notna().any() else pd.DataFrame(columns=cols_g))
    s = mat.stack().dropna()
    if not s.empty:
        imax = s.idxmax()
        out["p_max"] = round(float(s.max()), 1)
        out["ora_picco"] = (int(imax[1]), round(float(s.max()), 1))
        out["giorno_picco"] = (imax[0], round(float(s.max()), 1))
        out["ore_p50"] = int((s >= 50.0).sum())
        top = (pd.DataFrame({"Giorno": [i[0] for i in s.index],
                             "Ora": [f"{int(i[1]):02d}:00" for i in s.index],
                             "Probabilita' (%)": [round(float(v), 1) for v in s.to_numpy()],
                             "Ore osservate": [int(cnt.loc[i[0], i[1]]) for i in s.index]})
               .sort_values("Probabilita' (%)", ascending=False)
               .head(20).reset_index(drop=True))
        out["top_celle"] = top
    out["eccedenza_media"] = round(float(df["ecc"].mean()), 2)
    out["eccedenza_max"] = round(float(df["ecc"].max()), 2)
    return out


def calcola_stabilita_profilo(prezzi, min_ore_mese=360):
    """Stabilita' del profilo orario medio tra i mesi di calendario.

    Per ogni mese con abbastanza ore osservate calcola il profilo medio
    delle 24 ore (prezzo medio per ora del giorno), poi misura la
    correlazione di Pearson tra i profili mensili. Se la forma della
    giornata tipo e' stabile nel tempo, le strategie di shaping, le fasce
    time-of-use e le coperture sagomate restano valide; se la
    correlazione crolla, il profilo sta cambiando (stagionalita' forte,
    cambi strutturali di mix/prezzi) e vanno ricalibrate.

    Differenza rispetto agli altri tab: 'Settimana tipo', 'Stagionalita''
    e 'Fasce ottimali' mostrano o usano i profili MEDI; 'Autocorrelazione'
    misura la persistenza ora-su-ora; qui si misura la STABILITA' della
    FORMA della giornata mese-su-mese: non il livello dei prezzi (due
    mesi con livelli diversi ma stessa forma danno correlazione ~1) ma
    quanto la sagoma oraria resta uguale nel tempo.

    prezzi: Series oraria in €/MWh con indice datetime (tz-aware ok).
    min_ore_mese: ore osservate minime per includere un mese (default 360,
      circa meta' mese); mesi con qualche ora del giorno mai osservata
      (profilo incompleto) o con profilo a varianza nulla (correlazione
      non definita) sono esclusi.

    NaN-safe: ore NaN ignorate. Serie vuota, indice non datetime,
    duplicati o meno di 2 mesi validi -> KPI a None e DataFrame vuoti.
    Mesi DST con 23/25 ore contribuiscono con le ore osservate (logica
    posizionale per ora del giorno).

    Ritorna dict con 'n_mesi', 'mesi' (etichette YYYY-MM), 'min_ore_mese',
    'profili' (DataFrame mesi x 24, prezzi medi €/MWh per ora),
    'corr' (DataFrame correlazioni di Pearson mesi x mesi),
    'corr_media' (media fuori diagonale), 'corr_min' (minimo fuori
    diagonale), 'coppia_min' ((mese1, mese2) o None), 'mese_anomalo'
    (correlazione media piu' bassa verso gli altri mesi), 'ora_picco'
    (DataFrame Mese, Ora di picco, Prezzo medio, Ore osservate),
    'deriva_picco_ore' (max-min ora di picco tra i mesi), 'df_export'
    (uguale a ora_picco)."""

    cols_picco = ["Mese", "Ora di picco", "Prezzo medio (€/MWh)", "Ore osservate"]
    vuoto = {"n_mesi": 0, "mesi": [], "min_ore_mese": None,
             "profili": pd.DataFrame(),
             "corr": pd.DataFrame(),
             "corr_media": None, "corr_min": None, "coppia_min": None,
             "mese_anomalo": None,
             "ora_picco": pd.DataFrame(columns=cols_picco),
             "deriva_picco_ore": None,
             "df_export": pd.DataFrame(columns=cols_picco)}
    try:
        min_ore_mese = int(min_ore_mese)
    except Exception:
        return dict(vuoto)
    try:
        p = prezzi.astype(float)
        p = p[~p.index.duplicated(keep="first")].sort_index()
    except Exception:
        return dict(vuoto)
    try:
        if not isinstance(p.index, pd.DatetimeIndex):
            return dict(vuoto)
    except Exception:
        return dict(vuoto)
    p = p.dropna()
    if len(p) == 0:
        return dict(vuoto)

    idxn = p.index.tz_localize(None) if p.index.tz is not None else p.index
    per = idxn.to_period("M")
    ore = idxn.hour.to_numpy()
    v = p.to_numpy(dtype=float)
    profili, ore_mese = {}, {}
    for mp in sorted(set(per.tolist())):
        m = np.asarray(per == mp)
        n_ore = int(m.sum())
        if n_ore < min_ore_mese:
            continue
        hm = np.full(24, np.nan)
        for h in range(24):
            sel = v[m & (ore == h)]
            if sel.size:
                hm[h] = float(sel.mean())
        if np.isnan(hm).any():
            continue  # profilo incompleto: qualche ora mai osservata
        if float(np.std(hm)) == 0.0:
            continue  # profilo piatto: correlazione non definita
        etichetta = str(mp)
        profili[etichetta] = hm
        ore_mese[etichetta] = n_ore
    if len(profili) < 2:
        return dict(vuoto)

    mesi = sorted(profili)
    P = pd.DataFrame(profili, index=list(range(24))).T  # righe=mesi, colonne=ore
    C = P.T.corr()  # correlazione di Pearson tra mesi
    vals_c = C.to_numpy(dtype=float)
    mask_off = ~np.eye(len(mesi), dtype=bool)
    off = vals_c[mask_off]
    imin = int(np.nanargmin(off))
    ii, jj = np.where(mask_off)
    out = dict(vuoto)
    out["min_ore_mese"] = min_ore_mese
    out["n_mesi"] = len(mesi)
    out["mesi"] = mesi
    out["profili"] = P
    out["corr"] = C
    out["corr_media"] = round(float(np.nanmean(off)), 4)
    out["corr_min"] = round(float(off[imin]), 4)
    out["coppia_min"] = (mesi[int(ii[imin])], mesi[int(jj[imin])])
    media_vs_altri = (np.nan_to_num(vals_c, nan=0.0) * mask_off).sum(axis=1) / mask_off.sum(axis=1)
    out["mese_anomalo"] = mesi[int(np.nanargmin(media_vs_altri))]
    righe = []
    ore_picco = []
    for mm in mesi:
        hm = profili[mm]
        hp = int(np.argmax(hm))
        ore_picco.append(hp)
        righe.append({"Mese": mm, "Ora di picco": f"{hp:02d}:00",
                      "Prezzo medio (€/MWh)": round(float(hm.mean()), 2),
                      "Ore osservate": int(ore_mese[mm])})
    df_picco = pd.DataFrame(righe, columns=cols_picco)
    out["ora_picco"] = df_picco
    out["deriva_picco_ore"] = int(max(ore_picco) - min(ore_picco))
    out["df_export"] = df_picco
    return out


def calcola_confronto_fisso_indicizzato(prezzi, mw_f1, mw_f2, mw_f3, prezzo_fisso,
                                       spread_indicizzato=0.0, quota_fissa=1.0):
    """Confronto procurement: contratto a prezzo fisso (anche parziale) vs acquisto indicizzato allo spot.

    Il buyer d'energia chiede sempre: "conviene di piu' il fisso del fornitore
    o restare indicizzato allo spot?". Questo helper quantifica la risposta sul
    periodo di dati selezionato, con la stessa logica di costo di
    calcola_costo_fornitura (potenza per fascia F1/F2/F3).

    - indicizzato: costo_orario = (prezzo_spot + spread_indicizzato) * potenza_fascia
      (lo spread copre il margine del fornitore, es. 2-5 €/MWh)
    - fisso: costo_orario = prezzo_fisso * potenza_fascia
    - blended: quota_fissa * fisso + (1 - quota_fissa) * indicizzato
      (quota_fissa 100% = tutto fisso; 60% = hedging parziale)

    Differenza rispetto alla tab 'Costo fornitura': li' il confronto con la
    tariffa flat e' un semplice delta totale; qui si misura QUANTO fisso
    comprare (quota %), il prezzo di BREAK-EVEN (il prezzo fisso massimo che
    batterebbe ancora l'indicizzato), e il delta per mese e cumulato nel tempo.

    NaN-safe: ore con prezzo NaN escluse da tutti i totali. Serie vuota o
    indice non datetime -> KPI a None e DataFrame vuoti.
    Mesi DST con 23/25 ore: i conteggi mensili usano le ore osservate.

    Ritorna dict con 'mwh', 'totale_indicizzato', 'totale_fisso',
    'totale_blended', 'pmp_indicizzato' (prezzo medio ponderato indicizzato,
    spread incluso), 'pmp_blended', 'break_even' (prezzo fisso al
    pareggio con l'indicizzato), 'risparmio' (indicizzato - blended: quanto
    si risparmia col contratto, puo' essere negativo), 'risparmio_pct',
    'quota_ore_sotto' (frazione ore in cui spot+spread < prezzo_fisso),
    'df_mesi' (Mese, Costo indicizzato (€), Costo contratto (€),
    Delta contratto-indicizzato (€), PMP indicizzato (€/MWh), Ore osservate),
    'df_giorni' (Giorno, Delta cumulato contratto-indicizzato (€)),
    'mese_peggiore' ((etichetta mese, delta) o None: il mese in cui il
    contratto ha perso di piu' vs indicizzato)."""
    colonne_m = ["Mese", "Costo indicizzato (€)", "Costo contratto (€)",
                 "Delta contratto-indicizzato (€)", "PMP indicizzato (€/MWh)", "Ore osservate"]
    colonne_g = ["Giorno", "Delta cumulato contratto-indicizzato (€)"]
    vuoto = {"mwh": 0.0, "totale_indicizzato": None, "totale_fisso": None,
             "totale_blended": None, "pmp_indicizzato": None, "pmp_blended": None,
             "break_even": None, "risparmio": None, "risparmio_pct": None,
             "quota_ore_sotto": None, "df_mesi": pd.DataFrame(columns=colonne_m),
             "df_giorni": pd.DataFrame(columns=colonne_g), "mese_peggiore": None}
    try:
        pf = float(prezzo_fisso)
        sp = float(spread_indicizzato)
        q = max(0.0, min(1.0, float(quota_fissa)))
    except Exception:
        return dict(vuoto)
    try:
        p = prezzi.astype(float)
        p = p[~p.index.duplicated(keep="first")].sort_index()
        if not isinstance(p.index, pd.DatetimeIndex):
            return dict(vuoto)
    except Exception:
        return dict(vuoto)
    p = p.dropna()
    if len(p) == 0:
        return dict(vuoto)

    profilo = {"F1": float(mw_f1), "F2": float(mw_f2), "F3": float(mw_f3)}
    fasce = p.index.map(fascia_oraria)
    mw = fasce.map(profilo).to_numpy(dtype=float)
    spot = p.to_numpy(dtype=float)
    costo_idx = (spot + sp) * mw
    costo_fis = pf * mw
    costo_bl = q * costo_fis + (1.0 - q) * costo_idx
    delta = costo_bl - costo_idx  # >0: il contratto costa di piu' dell'indicizzato

    tot_idx = float(costo_idx.sum())
    tot_fis = float(costo_fis.sum())
    tot_bl = float(costo_bl.sum())
    mwh = float(mw.sum())
    pmp_idx = tot_idx / mwh if mwh > 0 else float("nan")
    pmp_bl = tot_bl / mwh if mwh > 0 else float("nan")
    risparmio = tot_idx - tot_bl
    risparmio_pct = risparmio / tot_idx * 100.0 if tot_idx != 0 else float("nan")
    quota_sotto = float(np.mean((spot + sp) < pf))

    idxn = p.index.tz_localize(None) if p.index.tz is not None else p.index
    mesi = idxn.to_period("M")
    righe = []
    for mp in sorted(set(mesi.tolist())):
        m = np.asarray(mesi == mp)
        n_ore = int(m.sum())
        e_mwh = float(mw[m].sum())
        ti = float(costo_idx[m].sum())
        tb = float(costo_bl[m].sum())
        pm = ti / e_mwh if e_mwh > 0 else float("nan")
        righe.append({"Mese": str(mp), "Costo indicizzato (€)": round(ti, 2),
                      "Costo contratto (€)": round(tb, 2),
                      "Delta contratto-indicizzato (€)": round(tb - ti, 2),
                      "PMP indicizzato (€/MWh)": (None if np.isnan(pm) else round(pm, 2)),
                      "Ore osservate": n_ore})
    df_mesi = pd.DataFrame(righe, columns=colonne_m)

    giorni = idxn.normalize()
    df_d = pd.DataFrame({"giorno": giorni, "delta": delta}).groupby("giorno")["delta"].sum()
    cum = float(0.0)
    righe_g = []
    for g, d in df_d.items():
        cum += float(d)
        righe_g.append({"Giorno": str(g.date()),
                        "Delta cumulato contratto-indicizzato (€)": round(cum, 2)})
    df_giorni = pd.DataFrame(righe_g, columns=colonne_g)

    mese_peggiore = None
    if len(df_mesi):
        r = df_mesi.loc[df_mesi["Delta contratto-indicizzato (€)"].idxmax()]
        mese_peggiore = (str(r["Mese"]), float(r["Delta contratto-indicizzato (€)"]))

    out = dict(vuoto)
    out.update({
        "mwh": mwh,
        "totale_indicizzato": round(tot_idx, 2),
        "totale_fisso": round(tot_fis, 2),
        "totale_blended": round(tot_bl, 2),
        "pmp_indicizzato": (None if np.isnan(pmp_idx) else round(pmp_idx, 2)),
        "pmp_blended": (None if np.isnan(pmp_bl) else round(pmp_bl, 2)),
        "break_even": (None if (np.isnan(pmp_idx)) else round(pmp_idx, 2)),
        "risparmio": round(risparmio, 2),
        "risparmio_pct": (None if np.isnan(risparmio_pct) else round(risparmio_pct, 2)),
        "quota_ore_sotto": round(quota_sotto, 4),
        "df_mesi": df_mesi,
        "df_giorni": df_giorni,
        "mese_peggiore": mese_peggiore,
    })
    return out


def calcola_valutazione_cap_floor(prezzi, mw_f1, mw_f2, mw_f3,
                                  cap_strike=None, floor_strike=None, spread=0.0):
    """Valutazione del premio equo di un CAP e/o un FLOOR sul prezzo orario.

    Strumento di structuring per il procurement: il buyer compra allo spot
    (+ spread del fornitore) ma si copre con un CAP a strike K (se lo spot
    supera K paga K) e/o un FLOOR a strike F (se scende sotto F paga F). Il
    helper calcola il PREMIO EQUO di ciascuna protezione in EUR/MWh sul
    profilo di carico F1/F2/F3, come media storica del payoff orario
    (approccio attuariale: nessun modello di volatilita', solo la storia
    dei prezzi del periodo selezionato).

    - cap:   payoff_orario = max(0, (spot + spread) - cap_strike) * MW_ora
    - floor: payoff_orario = max(0, floor_strike - (spot + spread)) * MW_ora
    - collar = cap + floor insieme; richiede floor_strike < cap_strike,
      altrimenti collar non valido (ritorna neutro con 'errore').

    Differenza dalle altre tab: 'Fisso vs indicizzato' confronta due prezzi
    di acquisto, 'Valore flessibilita'' taglia carico fisico; qui si PREZZA
    una protezione finanziaria — il premio che il fornitore dovrebbe chiedere
    per lo strike scelto — utile per negoziare lo strike o decidere se il
    premio offerto conviene.

    Strike None = protezione disattivata; almeno una deve essere attiva,
    altrimenti ritorna neutro con 'errore'.

    NaN-safe: ore con prezzo NaN escluse da tutti i totali. Serie vuota o
    indice non datetime -> KPI a None e DataFrame vuoti. Mesi DST con 23/25
    ore: i conteggi mensili usano le ore osservate.

    Ritorna dict con 'mwh', 'premio_cap_eur_mwh' (None se cap inattivo o
    mwh=0), 'premio_floor_eur_mwh', 'premio_cap_tot_eur',
    'premio_floor_tot_eur', 'ore_cap_pct' (frazione ore con payoff cap > 0,
    None se cap inattivo), 'ore_floor_pct', 'payout_medio_ora_cap' (EUR/h
    sulle sole ore esercitate, None se cap inattivo),
    'payout_medio_ora_floor', 'costo_netto_protetto' (EUR: costo spot+spread
    meno i payoff incassati), 'df_mesi' (Mese, Payout cap (EUR), Payout
    floor (EUR), Ore osservate, PMP netto (EUR/MWh)), 'df_giorni' (Giorno,
    Payout cap cumulato (EUR), Payout floor cumulato (EUR)), 'mese_max_cap'
    ((etichetta mese, payout) o None), 'errore' (None o stringa)."""
    colonne_m = ["Mese", "Payout cap (\u20ac)", "Payout floor (\u20ac)", "Ore osservate",
                 "PMP netto (\u20ac/MWh)"]
    colonne_g = ["Giorno", "Payout cap cumulato (\u20ac)", "Payout floor cumulato (\u20ac)"]
    vuoto = {"mwh": 0.0, "premio_cap_eur_mwh": None, "premio_floor_eur_mwh": None,
             "premio_cap_tot_eur": None, "premio_floor_tot_eur": None,
             "ore_cap_pct": None, "ore_floor_pct": None,
             "payout_medio_ora_cap": None, "payout_medio_ora_floor": None,
             "costo_netto_protetto": None,
             "df_mesi": pd.DataFrame(columns=colonne_m),
             "df_giorni": pd.DataFrame(columns=colonne_g),
             "mese_max_cap": None, "errore": None}

    def _strike(v):
        if v is None:
            return None
        x = float(v)
        if not np.isfinite(x):
            raise ValueError("strike non finito")
        return x

    try:
        cap = _strike(cap_strike)
        flr = _strike(floor_strike)
        sp = float(spread)
        if not np.isfinite(sp):
            raise ValueError("spread non finito")
    except Exception:
        out = dict(vuoto)
        out["errore"] = "Strike o spread non validi: inserisci valori numerici."
        return out
    if cap is None and flr is None:
        out = dict(vuoto)
        out["errore"] = ("Nessuna protezione attiva: imposta almeno uno strike "
                         "(cap e/o floor).")
        return out
    if cap is not None and flr is not None and flr >= cap:
        out = dict(vuoto)
        out["errore"] = ("Collar non valido: lo strike del floor deve essere "
                         "sotto lo strike del cap.")
        return out

    try:
        p = prezzi.astype(float)
        p = p[~p.index.duplicated(keep="first")].sort_index()
        if not isinstance(p.index, pd.DatetimeIndex):
            return dict(vuoto)
    except Exception:
        return dict(vuoto)
    p = p.dropna()
    if len(p) == 0:
        return dict(vuoto)

    profilo = {"F1": float(mw_f1), "F2": float(mw_f2), "F3": float(mw_f3)}
    fasce = p.index.map(fascia_oraria)
    mw = fasce.map(profilo).to_numpy(dtype=float)
    net = p.to_numpy(dtype=float) + sp
    mwh = float(mw.sum())

    pay_cap = np.maximum(0.0, net - cap) * mw if cap is not None else np.zeros_like(net)
    pay_flr = np.maximum(0.0, flr - net) * mw if flr is not None else np.zeros_like(net)
    tot_cap = float(pay_cap.sum())
    tot_flr = float(pay_flr.sum())

    def _pct(pay):
        return float(np.mean(pay > 0.0))

    def _medio_ora(pay, tot):
        n_ex = int((pay > 0.0).sum())
        return (tot / n_ex) if n_ex > 0 else 0.0

    premio_cap = (tot_cap / mwh) if (cap is not None and mwh > 0) else None
    premio_flr = (tot_flr / mwh) if (flr is not None and mwh > 0) else None
    netto = float(((net * mw) - pay_cap - pay_flr).sum())

    idxn = p.index.tz_localize(None) if p.index.tz is not None else p.index
    mesi = idxn.to_period("M")
    righe = []
    for mp in sorted(set(mesi.tolist())):
        m = np.asarray(mesi == mp)
        e_mwh = float(mw[m].sum())
        pm = float(((net * mw)[m].sum()) / e_mwh) if e_mwh > 0 else float("nan")
        righe.append({"Mese": str(mp), "Payout cap (\u20ac)": round(float(pay_cap[m].sum()), 2),
                      "Payout floor (\u20ac)": round(float(pay_flr[m].sum()), 2),
                      "Ore osservate": int(m.sum()),
                      "PMP netto (\u20ac/MWh)": (None if np.isnan(pm) else round(pm, 2))})
    df_mesi = pd.DataFrame(righe, columns=colonne_m)

    giorni = idxn.normalize()
    df_d = pd.DataFrame({"giorno": giorni, "pc": pay_cap, "pf": pay_flr}).groupby("giorno")[["pc", "pf"]].sum()
    cum_c = cum_f = 0.0
    righe_g = []
    for g, r in df_d.iterrows():
        cum_c += float(r["pc"])
        cum_f += float(r["pf"])
        righe_g.append({"Giorno": str(g.date()),
                        "Payout cap cumulato (\u20ac)": round(cum_c, 2),
                        "Payout floor cumulato (\u20ac)": round(cum_f, 2)})
    df_giorni = pd.DataFrame(righe_g, columns=colonne_g)

    mese_max_cap = None
    if cap is not None and len(df_mesi):
        r = df_mesi.loc[df_mesi["Payout cap (\u20ac)"].idxmax()]
        mese_max_cap = (str(r["Mese"]), float(r["Payout cap (\u20ac)"]))

    out = dict(vuoto)
    out.update({
        "mwh": mwh,
        "premio_cap_eur_mwh": (None if premio_cap is None else round(premio_cap, 4)),
        "premio_floor_eur_mwh": (None if premio_flr is None else round(premio_flr, 4)),
        "premio_cap_tot_eur": round(tot_cap, 2) if cap is not None else None,
        "premio_floor_tot_eur": round(tot_flr, 2) if flr is not None else None,
        "ore_cap_pct": round(_pct(pay_cap), 4) if cap is not None else None,
        "ore_floor_pct": round(_pct(pay_flr), 4) if flr is not None else None,
        "payout_medio_ora_cap": round(_medio_ora(pay_cap, tot_cap), 2) if cap is not None else None,
        "payout_medio_ora_floor": round(_medio_ora(pay_flr, tot_flr), 2) if flr is not None else None,
        "costo_netto_protetto": round(netto, 2),
        "df_mesi": df_mesi,
        "df_giorni": df_giorni,
        "mese_max_cap": mese_max_cap,
    })
    return out


def calcola_stima_bolletta(prezzi, mw_f1, mw_f2, mw_f3,
                           perdite_pct=10.4, dispacciamento=4.0, pcv_mese=11.0,
                           oneri=14.0, accisa=22.7, iva_pct=22.0):
    """Ricostruzione STIMATA della bolletta elettrica italiana per una fornitura
    a prezzo indicizzato (spot + spread = componente energia), partendo dal
    profilo di carico F1/F2/F3.

    Componenti (tutte parametrizzabili dall'utente):
    - Energia: prezzo orario (spot) * MW della fascia -> la materia energia
    - Perdite di rete: % sulla componente energia (default 10.4 % = BT)
    - Dispacciamento (corrispettivi Terna/disaccoppiamento): EUR/MWh
    - PCV (prezzo commercializzazione vendita): EUR/mese, spalmato sui mesi del periodo
    - Oneri di sistema (ASOS/ARIM ecc.): EUR/MWh
    - Accisa: EUR/MWh (default 22.7 = 0.0227 EUR/kWh, usi non domestici/non agevolati)
    - IVA: % sull'imponibile (default 22 %)

    Differenza dalle altre tab: 'Costo fornitura' e 'Fisso vs indicizzato'
    guardano solo la materia energia; qui si stima il TOTALE fattura con
    tutti gli oneri parafiscali, per rispondere a "quanto pago davvero?".

    NaN-safe: ore con prezzo NaN escluse. Serie vuota o indice non datetime
    -> totali a zero e DataFrame vuoti. Parametri non numerici o negativi
    -> 'errore'.

    Ritorna dict con 'errore', 'mwh', 'n_mesi', totali per voce ('energia_eur',
    'perdite_eur', 'disp_eur', 'pcv_eur', 'oneri_eur', 'accisa_eur',
    'imponibile_eur', 'iva_eur', 'totale_eur'), 'eur_mwh_allin',
    'quota_energia_pct' (energia / totale), 'extra_vs_energia'
    (totale - energia), 'df_mesi' (Mese, MWh, Energia (EUR), Perdite (EUR),
    Dispacciamento (EUR), PCV (EUR), Oneri (EUR), Accisa (EUR),
    Imponibile (EUR), IVA (EUR), Totale (EUR), EUR/MWh), 'df_giorni'
    (Giorno, Energia cumulata (EUR), Totale cumulato (EUR))."""
    colonne_m = ["Mese", "MWh", "Energia (\u20ac)", "Perdite (\u20ac)",
                 "Dispacciamento (\u20ac)", "PCV (\u20ac)", "Oneri (\u20ac)",
                 "Accisa (\u20ac)", "Imponibile (\u20ac)", "IVA (\u20ac)",
                 "Totale (\u20ac)", "\u20ac/MWh"]
    colonne_g = ["Giorno", "Energia cumulata (\u20ac)", "Totale cumulato (\u20ac)"]
    vuoto = {"errore": None, "mwh": 0.0, "n_mesi": 0,
             "energia_eur": 0.0, "perdite_eur": 0.0, "disp_eur": 0.0,
             "pcv_eur": 0.0, "oneri_eur": 0.0, "accisa_eur": 0.0,
             "imponibile_eur": 0.0, "iva_eur": 0.0, "totale_eur": 0.0,
             "eur_mwh_allin": None, "quota_energia_pct": None,
             "extra_vs_energia": 0.0,
             "df_mesi": pd.DataFrame(columns=colonne_m),
             "df_giorni": pd.DataFrame(columns=colonne_g)}

    try:
        pp = float(perdite_pct); dp = float(dispacciamento); pv = float(pcv_mese)
        on = float(oneri); ac = float(accisa); iv = float(iva_pct)
    except Exception:
        out = dict(vuoto); out["errore"] = "Parametri non validi: inserisci valori numerici."
        return out
    if any(not np.isfinite(x) for x in (pp, dp, pv, on, ac, iv)):
        out = dict(vuoto); out["errore"] = "Parametri non validi: inserisci valori numerici."
        return out
    if any(x < 0 for x in (pp, dp, pv, on, ac, iv)):
        out = dict(vuoto); out["errore"] = "I parametri non possono essere negativi."
        return out

    try:
        p = prezzi.astype(float)
        p = p[~p.index.duplicated(keep="first")].sort_index()
        if not isinstance(p.index, pd.DatetimeIndex):
            return dict(vuoto)
    except Exception:
        return dict(vuoto)
    p = p.dropna()
    if len(p) == 0:
        return dict(vuoto)

    profilo = {"F1": float(mw_f1), "F2": float(mw_f2), "F3": float(mw_f3)}
    fasce = p.index.map(fascia_oraria)
    mw = fasce.map(profilo).to_numpy(dtype=float)
    px = p.to_numpy(dtype=float)
    mwh = float(mw.sum())

    energia = px * mw
    perdite = energia * (pp / 100.0)
    disp = mw * dp
    oneri_v = mw * on
    accisa_v = mw * ac

    idxn = p.index.tz_localize(None) if p.index.tz is not None else p.index
    mesi = idxn.to_period("M")
    mesi_ord = sorted(set(mesi.tolist()))
    n_mesi = len(mesi_ord)
    pcv_m = (pv * n_mesi) if n_mesi else 0.0

    righe = []
    for mp in mesi_ord:
        m = np.asarray(mesi == mp)
        e_mwh = float(mw[m].sum())
        e_en = float(energia[m].sum()); e_pe = float(perdite[m].sum())
        e_dp = float(disp[m].sum()); e_on = float(oneri_v[m].sum())
        e_ac = float(accisa_v[m].sum())
        imp = e_en + e_pe + e_dp + pv + e_on + e_ac
        iva_m = imp * (iv / 100.0)
        tot_m = imp + iva_m
        righe.append({"Mese": str(mp), "MWh": round(e_mwh, 1),
                      "Energia (\u20ac)": round(e_en, 2), "Perdite (\u20ac)": round(e_pe, 2),
                      "Dispacciamento (\u20ac)": round(e_dp, 2), "PCV (\u20ac)": round(pv, 2),
                      "Oneri (\u20ac)": round(e_on, 2), "Accisa (\u20ac)": round(e_ac, 2),
                      "Imponibile (\u20ac)": round(imp, 2), "IVA (\u20ac)": round(iva_m, 2),
                      "Totale (\u20ac)": round(tot_m, 2),
                      "\u20ac/MWh": round(tot_m / e_mwh, 2) if e_mwh > 0 else None})
    df_mesi = pd.DataFrame(righe, columns=colonne_m)

    giorni = idxn.normalize()
    df_d = pd.DataFrame({"giorno": giorni, "en": energia,
                         "pe": perdite, "dp": disp, "on": oneri_v, "ac": accisa_v}
                        ).groupby("giorno")[["en", "pe", "dp", "on", "ac"]].sum()
    cum_en = cum_tot = 0.0
    righe_g = []
    # PCV spalmata pro-rata sui giorni osservati (pcv_m = pv * n_mesi)
    pcv_g = pcv_m / max(len(df_d), 1) if len(df_d) else 0.0
    for g, r in df_d.iterrows():
        cum_en += float(r["en"])
        imp_g = float(r["en"] + r["pe"] + r["dp"] + r["on"] + r["ac"]) + pcv_g
        cum_tot += imp_g * (1.0 + iv / 100.0)
        righe_g.append({"Giorno": str(g.date()),
                        "Energia cumulata (\u20ac)": round(cum_en, 2),
                        "Totale cumulato (\u20ac)": round(cum_tot, 2)})
    df_giorni = pd.DataFrame(righe_g, columns=colonne_g)

    energia_eur = float(energia.sum())
    perdite_eur = float(perdite.sum())
    disp_eur = float(disp.sum())
    oneri_eur = float(oneri_v.sum())
    accisa_eur = float(accisa_v.sum())
    imponibile = energia_eur + perdite_eur + disp_eur + pcv_m + oneri_eur + accisa_eur
    iva_eur = imponibile * (iv / 100.0)
    totale = imponibile + iva_eur

    out = dict(vuoto)
    out.update({
        "mwh": mwh, "n_mesi": n_mesi,
        "energia_eur": round(energia_eur, 2), "perdite_eur": round(perdite_eur, 2),
        "disp_eur": round(disp_eur, 2), "pcv_eur": round(pcv_m, 2),
        "oneri_eur": round(oneri_eur, 2), "accisa_eur": round(accisa_eur, 2),
        "imponibile_eur": round(imponibile, 2), "iva_eur": round(iva_eur, 2),
        "totale_eur": round(totale, 2),
        "eur_mwh_allin": round(totale / mwh, 2) if mwh > 0 else None,
        "quota_energia_pct": round(energia_eur / totale, 4) if totale > 0 else None,
        "extra_vs_energia": round(totale - energia_eur, 2),
        "df_mesi": df_mesi, "df_giorni": df_giorni,
    })
    return out


def calcola_margine_fornitore(prezzi, mw_f1, mw_f2, mw_f3, prezzo_offerta,
                              spread=0.0, perdite_pct=0.0, dispacciamento=4.0,
                              oneri=14.0):
    """Margine IMPLICITO del fornitore su un'offerta a prezzo fisso.

    Il fornitore offre prezzo_offerta EUR/MWh fisso; qui si stima quanto gli
    resta in tasca dopo i costi: il costo base e' lo spot ponderato sul
    profilo F1/F2/F3 dell'utente (stessa logica della tab 'Costo fornitura')
    piu' lo spread di acquisto e gli add-on passanti parametrizzabili
    (perdite di rete % sull'energia, dispacciamento e oneri in EUR/MWh).

    margine = ricavo offerta - costo totale
    prezzo di pareggio = costo totale / MWh (offerta a margine zero)

    Diverso dalle altre tab: 'Fisso vs indicizzato' confronta per il
    COMPRATORE due strategie di acquisto; qui la prospettiva e' quella del
    VENDITORE — strumento di negoziazione: se il margine implicito e' alto,
    c'e' spazio per trattare il prezzo.

    NaN-safe: ore con prezzo NaN escluse. Serie vuota o indice non datetime
    -> totali neutrali e DataFrame vuoti. prezzo_offerta <= 0 o parametri
    non numerici/negativi -> 'errore'.

    Ritorna dict con 'errore', 'mwh', 'n_mesi', 'costo_energia_eur',
    'costo_tot_eur', 'ricavo_offerta_eur', 'margine_eur',
    'margine_eur_mwh' (None se mwh=0), 'margine_pct' (None se ricavo=0),
    'pareggio_eur_mwh' (prezzo offerta a margine zero), 'df_mesi'
    (Mese, MWh, Costo energia (EUR), Add-on (EUR), Costo totale (EUR),
    Ricavo offerta (EUR), Margine (EUR), Margine (EUR/MWh)), 'df_giorni'
    (Giorno, Costo cumulato (EUR), Ricavo cumulato (EUR),
    Margine cumulato (EUR))."""
    colonne_m = ["Mese", "MWh", "Costo energia (\u20ac)", "Add-on (\u20ac)",
                 "Costo totale (\u20ac)", "Ricavo offerta (\u20ac)",
                 "Margine (\u20ac)", "Margine (\u20ac/MWh)"]
    colonne_g = ["Giorno", "Costo cumulato (\u20ac)", "Ricavo cumulato (\u20ac)",
                 "Margine cumulato (\u20ac)"]
    vuoto = {"errore": None, "mwh": 0.0, "n_mesi": 0,
             "costo_energia_eur": 0.0, "costo_tot_eur": 0.0,
             "ricavo_offerta_eur": 0.0, "margine_eur": 0.0,
             "margine_eur_mwh": None, "margine_pct": None,
             "pareggio_eur_mwh": None,
             "df_mesi": pd.DataFrame(columns=colonne_m),
             "df_giorni": pd.DataFrame(columns=colonne_g)}

    try:
        po = float(prezzo_offerta); sp = float(spread)
        pp = float(perdite_pct); dp = float(dispacciamento); on = float(oneri)
    except Exception:
        out = dict(vuoto); out["errore"] = "Parametri non validi: inserisci valori numerici."
        return out
    if any(not np.isfinite(x) for x in (po, sp, pp, dp, on)):
        out = dict(vuoto); out["errore"] = "Parametri non validi: inserisci valori numerici."
        return out
    if po <= 0 or any(x < 0 for x in (sp, pp, dp, on)):
        out = dict(vuoto); out["errore"] = "Prezzo offerta > 0 richiesto; gli altri parametri non possono essere negativi."
        return out

    try:
        p = prezzi.astype(float)
        p = p[~p.index.duplicated(keep="first")].sort_index()
        if not isinstance(p.index, pd.DatetimeIndex):
            return dict(vuoto)
    except Exception:
        return dict(vuoto)
    p = p.dropna()
    if len(p) == 0:
        return dict(vuoto)

    profilo = {"F1": float(mw_f1), "F2": float(mw_f2), "F3": float(mw_f3)}
    fasce = p.index.map(fascia_oraria)
    mw = fasce.map(profilo).to_numpy(dtype=float)
    px = p.to_numpy(dtype=float)
    mwh = float(mw.sum())

    energia = (px + sp) * mw
    perdite = energia * (pp / 100.0)
    addon = perdite + mw * (dp + on)
    costo_tot = energia + addon
    ricavo = mw * po
    margine = ricavo - costo_tot

    idxn = p.index.tz_localize(None) if p.index.tz is not None else p.index
    mesi = idxn.to_period("M")
    mesi_ord = sorted(set(mesi.tolist()))

    righe = []
    for mp in mesi_ord:
        m = np.asarray(mesi == mp)
        e_mwh = float(mw[m].sum())
        e_en = float(energia[m].sum()); e_ao = float(addon[m].sum())
        e_co = float(costo_tot[m].sum()); e_rv = float(ricavo[m].sum())
        e_ma = float(margine[m].sum())
        righe.append({"Mese": str(mp), "MWh": round(e_mwh, 1),
                      "Costo energia (\u20ac)": round(e_en, 2),
                      "Add-on (\u20ac)": round(e_ao, 2),
                      "Costo totale (\u20ac)": round(e_co, 2),
                      "Ricavo offerta (\u20ac)": round(e_rv, 2),
                      "Margine (\u20ac)": round(e_ma, 2),
                      "Margine (\u20ac/MWh)": round(e_ma / e_mwh, 2) if e_mwh > 0 else None})
    df_mesi = pd.DataFrame(righe, columns=colonne_m)

    giorni = idxn.normalize()
    df_d = pd.DataFrame({"giorno": giorni, "co": costo_tot, "rv": ricavo}
                        ).groupby("giorno")[["co", "rv"]].sum()
    cum_co = cum_rv = 0.0
    righe_g = []
    for g, r in df_d.iterrows():
        cum_co += float(r["co"]); cum_rv += float(r["rv"])
        righe_g.append({"Giorno": str(g.date()),
                        "Costo cumulato (\u20ac)": round(cum_co, 2),
                        "Ricavo cumulato (\u20ac)": round(cum_rv, 2),
                        "Margine cumulato (\u20ac)": round(cum_rv - cum_co, 2)})
    df_giorni = pd.DataFrame(righe_g, columns=colonne_g)

    costo_energia_eur = float(energia.sum())
    costo_tot_eur = float(costo_tot.sum())
    ricavo_eur = float(ricavo.sum())
    margine_eur = float(margine.sum())

    out = dict(vuoto)
    out.update({
        "mwh": mwh, "n_mesi": len(mesi_ord),
        "costo_energia_eur": round(costo_energia_eur, 2),
        "costo_tot_eur": round(costo_tot_eur, 2),
        "ricavo_offerta_eur": round(ricavo_eur, 2),
        "margine_eur": round(margine_eur, 2),
        "margine_eur_mwh": round(margine_eur / mwh, 2) if mwh > 0 else None,
        "margine_pct": round(margine_eur / ricavo_eur, 4) if ricavo_eur > 0 else None,
        "pareggio_eur_mwh": round(costo_tot_eur / mwh, 2) if mwh > 0 else None,
        "df_mesi": df_mesi, "df_giorni": df_giorni,
    })
    return out


def calcola_ponte_budget(prezzi, mw_f1, mw_f2, mw_f3, prezzo_budget, volume_budget_mwh):
    """Ponte budget -> consuntivo: scomposizione dello scostamento di costo.

    Confronta il costo effettivo (spot pesato sul profilo F1/F2/F3) con un
    budget definito da prezzo unitario e volume totale sul periodo, e
    scompone lo scostamento in tre driver che sommano ESATTAMENTE:

        scostamento = effetto prezzo + effetto volume + effetto mix

    - effetto prezzo = (p_lw - p_budget) * V_budget
      (quanto costano i prezzi diversi dal budget, a volumi di budget)
    - effetto volume = (V_eff - V_budget) * p_budget
      (quanto costano i volumi diversi dal budget, a prezzi di budget)
    - effetto mix    = (p_lw - p_budget) * (V_eff - V_budget)
      (interazione prezzo x volume: es. consumare di piu' proprio quando
      i prezzi sono sopra budget)

    dove p_lw e' il prezzo load-weighted effettivo (costo/MWh) e V_eff il
    volume effettivo. Il volume di budget viene ripartito sui mesi per
    giorni di calendario (pro-rata temporis), come si fa nei budget annuali.

    Diverso dalle altre tab: 'Budget tracker' mostra l'andamento cumulato
    contro una soglia ma non spiega il PERCHE'; 'Costo fornitura' mostra
    solo l'effettivo. Qui si risponde alla domanda del controller:
    "siamo sopra budget, ma per colpa dei prezzi, dei volumi o di entrambi?".

    NaN-safe: ore con prezzo NaN escluse. Serie vuota o indice non datetime
    -> totali neutrali e DataFrame vuoti. prezzo_budget <= 0, volume < 0 o
    parametri non numerici -> 'errore'.

    Ritorna dict con 'errore', 'mwh_eff', 'prezzo_lw' (None se mwh_eff=0),
    'costo_eff', 'costo_budget', 'scostamento', 'scostamento_pct'
    (None se costo_budget=0), 'eff_prezzo', 'eff_volume', 'eff_mix',
    'driver' ('prezzo'/'volume'/'mix', il contributo maggiore in valore
    assoluto, None se tutti nulli), 'df_mesi' (Mese, MWh effettivi,
    MWh budget, Prezzo LW (€/MWh), Costo effettivo (€), Costo budget (€),
    Scostamento (€), Effetto prezzo (€), Effetto volume (€), Effetto mix (€))."""
    colonne_m = ["Mese", "MWh effettivi", "MWh budget", "Prezzo LW (\u20ac/MWh)",
                 "Costo effettivo (\u20ac)", "Costo budget (\u20ac)", "Scostamento (\u20ac)",
                 "Effetto prezzo (\u20ac)", "Effetto volume (\u20ac)", "Effetto mix (\u20ac)"]
    vuoto = {"errore": None, "mwh_eff": 0.0, "prezzo_lw": None, "costo_eff": 0.0,
             "costo_budget": 0.0, "scostamento": 0.0, "scostamento_pct": None,
             "eff_prezzo": 0.0, "eff_volume": 0.0, "eff_mix": 0.0,
             "driver": None, "df_mesi": pd.DataFrame(columns=colonne_m)}

    try:
        pb = float(prezzo_budget); vb = float(volume_budget_mwh)
    except Exception:
        out = dict(vuoto); out["errore"] = "Parametri non validi: inserisci valori numerici."
        return out
    if not np.isfinite(pb) or not np.isfinite(vb):
        out = dict(vuoto); out["errore"] = "Parametri non validi: inserisci valori numerici."
        return out
    if pb <= 0 or vb < 0:
        out = dict(vuoto); out["errore"] = "Prezzo budget > 0 e volume budget >= 0 richiesti."
        return out

    try:
        p = prezzi.astype(float)
        p = p[~p.index.duplicated(keep="first")].sort_index()
        if not isinstance(p.index, pd.DatetimeIndex):
            return dict(vuoto)
    except Exception:
        return dict(vuoto)
    p = p.dropna()
    if len(p) == 0:
        return dict(vuoto)

    profilo = {"F1": float(mw_f1), "F2": float(mw_f2), "F3": float(mw_f3)}
    fasce = p.index.map(fascia_oraria)
    mw = fasce.map(profilo).to_numpy(dtype=float)
    px = p.to_numpy(dtype=float)
    costo_orario = px * mw
    mwh_eff = float(mw.sum())
    costo_eff = float(costo_orario.sum())
    p_lw = costo_eff / mwh_eff if mwh_eff > 0 else None
    costo_budget = pb * vb
    scost = costo_eff - costo_budget
    if p_lw is None:
        eff_p = eff_v = eff_m = 0.0
    else:
        eff_p = (p_lw - pb) * vb
        eff_v = (mwh_eff - vb) * pb
        eff_m = (p_lw - pb) * (mwh_eff - vb)

    idxn = p.index.tz_localize(None) if p.index.tz is not None else p.index
    giorni_totali = int(idxn.normalize().unique().shape[0])
    mesi = idxn.to_period("M")
    mesi_ord = sorted(set(mesi.tolist()))
    righe = []
    for mp in mesi_ord:
        m = np.asarray(mesi == mp)
        giorni_m = int(pd.DatetimeIndex(idxn[m]).normalize().unique().shape[0])
        vb_m = vb * giorni_m / giorni_totali if giorni_totali > 0 else 0.0
        mwh_m = float(mw[m].sum()); ce_m = float(costo_orario[m].sum())
        plw_m = ce_m / mwh_m if mwh_m > 0 else None
        cb_m = pb * vb_m
        if plw_m is None:
            ep_m = ev_m = em_m = 0.0
        else:
            ep_m = (plw_m - pb) * vb_m
            ev_m = (mwh_m - vb_m) * pb
            em_m = (plw_m - pb) * (mwh_m - vb_m)
        righe.append({"Mese": str(mp), "MWh effettivi": round(mwh_m, 1),
                      "MWh budget": round(vb_m, 1),
                      "Prezzo LW (\u20ac/MWh)": round(plw_m, 2) if plw_m is not None else None,
                      "Costo effettivo (\u20ac)": round(ce_m, 2),
                      "Costo budget (\u20ac)": round(cb_m, 2),
                      "Scostamento (\u20ac)": round(ce_m - cb_m, 2),
                      "Effetto prezzo (\u20ac)": round(ep_m, 2),
                      "Effetto volume (\u20ac)": round(ev_m, 2),
                      "Effetto mix (\u20ac)": round(em_m, 2)})
    df_mesi = pd.DataFrame(righe, columns=colonne_m)

    driver = None
    cand = [("prezzo", abs(eff_p)), ("volume", abs(eff_v)), ("mix", abs(eff_m))]
    if any(v > 0 for _, v in cand):
        driver = max(cand, key=lambda t: t[1])[0]

    out = dict(vuoto)
    out.update({
        "mwh_eff": mwh_eff,
        "prezzo_lw": round(p_lw, 2) if p_lw is not None else None,
        "costo_eff": round(costo_eff, 2),
        "costo_budget": round(costo_budget, 2),
        "scostamento": round(scost, 2),
        "scostamento_pct": round(scost / costo_budget, 4) if costo_budget > 0 else None,
        "eff_prezzo": round(eff_p, 2), "eff_volume": round(eff_v, 2),
        "eff_mix": round(eff_m, 2), "driver": driver, "df_mesi": df_mesi,
    })
    return out


def calcola_driver_costo(prezzi, mw_f1, mw_f2, mw_f3):
    """Driver del costo: scomposizione della varianza del costo giornaliero.

    Calcola il costo giornaliero di fornitura (spot orario pesato sul profilo
    F1/F2/F3, stessa logica della tab 'Costo fornitura') e ne scompone la
    varianza con un'ANOVA a due vie senza interazione (tipo I, sequenziale):

        Var(costo_giornaliero) = MESE + SETTIMANA|mese + RESIDUO

    - MESE: stagionalita' (quanto del costo e' spiegato dal mese di calendario)
    - SETTIMANA: pattern settimanale (lunedi' vs domenica, ...) al netto del mese
    - RESIDUO: tutto il resto (spike, eventi, rumore non di calendario)

    Le tre quote (eta^2) sommano ESATTAMENTE a 1 quando la varianza totale > 0.
    Risponde alla domanda del controller: "cosa muove il mio costo, la
    stagione o il giorno della settimana?".

    Differenza dalle altre tab: 'Stagionalita'' mostra i profili medi mensili
    ma non quantifica QUANTO spiegano; 'Settimana tipo' mostra il pattern
    settimanale dei prezzi ma non del COSTO (che dipende anche dal profilo
    di prelievo); 'Sensitivita' profilo' varia il profilo a prezzi fissi.
    Qui si misura, sui dati reali, il peso di ciascun driver di calendario.

    NaN-safe: ore con prezzo NaN escluse. Serie vuota o indice non datetime
    -> totali neutrali e DataFrame vuoti. Meno di 2 giorni -> varianza nulla,
    driver None.

    Ritorna dict con 'errore', 'giorni' (n. giorni di calendario),
    'costo_medio_giorno' (None se giorni=0), 'eta2_mese', 'eta2_settimana',
    'eta2_residuo' (quote in [0,1], somma 1 se varianza > 0), 'driver'
    ('mese'/'settimana'/'residuo', la quota maggiore; None se varianza nulla),
    'mese_max' ("YYYY-MM" del mese col costo medio piu' alto, None se n<1),
    'giorno_max' (nome italiano del weekday col costo medio piu' alto),
    'df_mesi' (Mese, Giorni, Costo medio (€/giorno), Costo totale (€),
    Scost. vs media (%)), 'df_settimana' (Giorno, Costo medio (€/giorno),
    Scost. vs media (%), ordinato lunedi'->domenica)."""
    colonne_m = ["Mese", "Giorni", "Costo medio (\u20ac/giorno)",
                 "Costo totale (\u20ac)", "Scost. vs media (%)"]
    colonne_s = ["Giorno", "Costo medio (\u20ac/giorno)", "Scost. vs media (%)"]
    nomi_wd = ["Luned\u00ec", "Marted\u00ec", "Mercoled\u00ec", "Gioved\u00ec",
               "Venerd\u00ec", "Sabato", "Domenica"]
    vuoto = {"errore": None, "giorni": 0, "costo_medio_giorno": None,
             "eta2_mese": 0.0, "eta2_settimana": 0.0, "eta2_residuo": 0.0,
             "driver": None, "mese_max": None, "giorno_max": None,
             "df_mesi": pd.DataFrame(columns=colonne_m),
             "df_settimana": pd.DataFrame(columns=colonne_s)}

    try:
        p = prezzi.astype(float)
        p = p[~p.index.duplicated(keep="first")].sort_index()
        if not isinstance(p.index, pd.DatetimeIndex):
            return dict(vuoto)
    except Exception:
        return dict(vuoto)
    p = p.dropna()
    if len(p) == 0:
        return dict(vuoto)

    try:
        profilo = {"F1": float(mw_f1), "F2": float(mw_f2), "F3": float(mw_f3)}
    except Exception:
        return dict(vuoto)
    fasce = p.index.map(fascia_oraria)
    mw_ora = fasce.map(profilo).to_numpy(dtype=float)
    costo_orario = p.to_numpy(dtype=float) * mw_ora  # EUR/ora

    giorni_idx = p.index.normalize()  # tz-safe: normalize conserva il tz
    d = pd.Series(costo_orario, index=giorni_idx).groupby(level=0).sum()
    d = d.sort_index()
    n = len(d)
    if n == 0:
        return dict(vuoto)

    mu = float(d.mean())
    ss_tot = float(((d - mu) ** 2).sum())

    mesi = d.index.month.to_numpy()
    wd = d.index.weekday.to_numpy()
    ym = d.index.strftime("%Y-%m").to_numpy()

    # Effetto MESE (between-month SS, one-way)
    mu_mese = d.groupby(ym).transform("mean")
    ss_mese = float((((mu_mese - mu) ** 2)).sum())

    # Effetto SETTIMANA al netto del mese: OLS a due vie senza interazione
    # (tipo I, sequenziale). Il fit additivo mese+weekday e' la proiezione
    # ortogonale -> SS_modello <= SS_totale sempre; la quota settimana e'
    # SS_modello - SS_mese (>= 0). Niente backfitting approssimato.
    y = d.to_numpy(dtype=float)
    ym_codes = pd.factorize(ym)[0]
    m_uniq = int(ym_codes.max()) + 1
    n_par = 1 + max(0, m_uniq - 1) + 6  # intercetta + dummy mese + dummy weekday
    X = np.zeros((n, n_par))
    X[:, 0] = 1.0
    for j in range(m_uniq - 1):
        X[:, 1 + j] = (ym_codes == j)
    for j in range(6):
        X[:, 1 + max(0, m_uniq - 1) + j] = (wd == j)
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    fitted = X @ coef
    ss_mod = float(((fitted - mu) ** 2).sum())
    ss_sett = max(0.0, min(ss_mod, ss_tot) - ss_mese)
    ss_sett = max(0.0, ss_sett)

    if ss_tot > 0:
        e_m = min(1.0, max(0.0, ss_mese / ss_tot))
        e_s = min(1.0, max(0.0, ss_sett / ss_tot))
        e_r = min(1.0, max(0.0, 1.0 - e_m - e_s))
        quote = [("mese", e_m), ("settimana", e_s), ("residuo", e_r)]
        driver = max(quote, key=lambda q: q[1])[0]
    else:
        e_m = e_s = e_r = 0.0
        driver = None

    # Tabelle di dettaglio
    g_mesi = d.groupby(ym)
    df_mesi = pd.DataFrame({
        "Mese": g_mesi.size().index,
        "Giorni": g_mesi.size().to_numpy(),
        "Costo medio (\u20ac/giorno)": g_mesi.mean().to_numpy().round(2),
        "Costo totale (\u20ac)": g_mesi.sum().to_numpy().round(2),
    })
    if mu != 0:
        df_mesi["Scost. vs media (%)"] = ((df_mesi["Costo medio (\u20ac/giorno)"] / mu - 1) * 100).round(1)
    else:
        df_mesi["Scost. vs media (%)"] = 0.0
    df_mesi = df_mesi[colonne_m].sort_values("Mese").reset_index(drop=True)

    g_wd = d.groupby(wd)
    media_wd = g_wd.mean().reindex(range(7))
    df_sett = pd.DataFrame({
        "Giorno": nomi_wd,
        "Costo medio (\u20ac/giorno)": media_wd.to_numpy().round(2),
    })
    if mu != 0:
        df_sett["Scost. vs media (%)"] = ((df_sett["Costo medio (\u20ac/giorno)"] / mu - 1) * 100).round(1)
    else:
        df_sett["Scost. vs media (%)"] = 0.0
    df_sett = df_sett[colonne_s]

    mese_max = df_mesi.loc[df_mesi["Costo medio (\u20ac/giorno)"].idxmax(), "Mese"] if n > 0 else None
    giorno_max = None
    if media_wd.notna().any():
        giorno_max = nomi_wd[int(media_wd.idxmax())]

    out = dict(vuoto)
    out.update({
        "giorni": n,
        "costo_medio_giorno": round(mu, 2),
        "eta2_mese": e_m, "eta2_settimana": e_s,
        "eta2_residuo": e_r,
        "driver": driver, "mese_max": mese_max, "giorno_max": giorno_max,
        "df_mesi": df_mesi, "df_settimana": df_sett,
    })
    return out


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
    st.markdown("Analisi operativa del prezzo spot orario Swissix (CH): KPI, confronto con il periodo precedente, soglie di alert, profilo giornaliero, heatmap oraria, fasce F1/F2/F3, tabella dati, rischio & durata, arbitraggio batteria, base/peak mensile, simulatore costo fornitura, MtM hedging, spark spread, shaping curva, spread weekend, price capture, volatilità realizzata, confronto anno-su-anno, analisi prezzi negativi, spread intra-day, picchi di prezzo, profilo settimanale tipo, curva di durata, concentrazione del costo di fornitura, simulazione demand shifting, finestre di acquisto ottimali, stagionalità mensile, monitoraggio del budget energetico annuale, analisi di sensitività del costo al profilo di prelievo, Value-at-Risk Monte Carlo del costo di fornitura, classifica dei giorni di calendario più costosi per il profilo di prelievo, fasce tariffarie orarie ottimali derivate dal profilo di prezzo osservato, autocorrelazione del prezzo spot (persistenza e stagionalità), stress test deterministico del costo di fornitura sotto shock di prezzo, previsione naive-stagionale del prezzo del giorno successivo con backtest di accuratezza, decomposizione stagionale del prezzo (trend + pattern giornaliero/settimanale + residuo) con export CSV.")

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
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12, tab13, tab14, tab15, tab16, tab17, tab18, tab19, tab20, tab21, tab22, tab23, tab24, tab25, tab26, tab27, tab28, tab29, tab30, tab31, tab32, tab33, tab34, tab35, tab36, tab37, tab38, tab39, tab40, tab41, tab42, tab43, tab44, tab45, tab46, tab47, tab48, tab49, tab50, tab51 = st.tabs(["⏱️ Profilo giornaliero", "🔥 Heatmap oraria", "⚡ Fasce F1/F2/F3", "📋 Tabella dati", "⚠️ Rischio & Durata", "🔋 Arbitraggio Batteria", "📊 Base/Peak mensile", "💰 Costo fornitura", "📈 MtM hedging", "🔥 Spark spread", "📐 Shaping curva", "📅 Weekend", "☀️ Price capture", "📉 Volatilità", "🗓️ YoY", "⬇️ Prezzi negativi", "↕️ Spread intra-day", "📍 Picchi di prezzo", "📆 Settimana tipo", "📉 Curva durata", "🎯 Concentrazione costo", "🔄 Shifting carico", "🎯 Finestre di acquisto", "🗓️ Stagionalità", "💼 Budget tracker", "🎚️ Sensitività profilo", "🎲 VaR costo (MC)", "🔝 Top giorni di costo", "🎛️ Fasce ottimali", "📈 Autocorrelazione", "🧪 Stress test", "🔮 Forecast prezzo", "⚡ Rampe di prezzo", "🔁 Persistenza sopra soglia", "📆 Spread calendario", "🧩 Decomposizione", "📊 Sequenze", "💡 Valore flessibilità", "🕐 Top ore di costo", "🕯️ Candele OHLC", "📉 Crolli & recuperi", "🔄 Mean reversion", "📦 Strip forward", "🌡️ Climatologia prezzo", "🔀 Stabilità profilo", "⚖️ Fisso vs indicizzato", "🛡️ Cap & Floor", "🧾 Stima bolletta", "🧮 Margine fornitore", "🌉 Ponte budget", "🧬 Driver del costo"])

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

    with tab14:
        titolo_vol = edu("Volatilità realizzata", "La VOLATILITÀ REALIZZATA misura quanto il prezzo 'sfarfalla' ora per ora: è la deviazione standard delle variazioni orarie di prezzo (€/MWh) calcolata giorno per giorno. A differenza del VaR del tab Rischio & Durata (che guarda la distribuzione dei LIVELLI di prezzo), la volatilità guarda la VELOCITÀ dei movimenti. Alta volatilità = opportunità per trading intraday e arbitraggio batteria, ma anche rischio di timing per chi vende sul mercato spot. Si misura sulle differenze di prezzo (non sui rendimenti logaritmici, indefiniti quando i prezzi sono 0 o negativi).")
        st.markdown(f"**{titolo_vol}**: deviazione standard delle variazioni orarie di prezzo, giorno per giorno.", unsafe_allow_html=True)

        vol = calcola_volatilita(prezzi)
        df_v = vol["giornaliera"]
        if df_v.empty or df_v["Vol (€/MWh)"].isna().all():
            st.warning("Dati insufficienti per calcolare la volatilità (servono almeno 3 ore valide).")
        else:
            v_s = df_v["Vol (€/MWh)"].dropna()
            media30 = float(v_s.tail(30).mean())
            ultimo = float(v_s.iloc[-1])
            g_max = df_v.loc[v_s.idxmax()]
            prof_h = vol["profilo_orario"]
            o_max = int(prof_h.idxmax())
            roll30 = v_s.rolling(30, min_periods=1).mean()
            v1, v2, v3, v4 = st.columns(4)
            render_kpi("Vol ultimo giorno (€/MWh)", f"{ultimo:,.2f}", v1)
            render_kpi("Vol media ultimi 30gg (€/MWh)", f"{media30:,.2f}", v2)
            render_kpi(f"🔺 Giorno più volatile ({g_max['Giorno']})", f"{g_max['Vol (€/MWh)']:,.2f}", v3)
            render_kpi(f"⏰ Ora più volatile ({o_max}:00)", f"{prof_h.loc[o_max]:,.2f}", v4)
            st.caption(f"📊 Nell'ultimo giorno il prezzo si è mosso in media di ±{ultimo:.2f} €/MWh da un'ora all'altra "
                       f"(media 30gg: ±{media30:.2f} €/MWh). Il giorno più volatile è stato il {g_max['Giorno']}.")

            fig_vol = go.Figure()
            fig_vol.add_trace(go.Bar(
                x=df_v["Giorno"], y=df_v["Vol (€/MWh)"], name="Vol giornaliera",
                marker_color="#8b5cf6",
                hovertemplate="Giorno: %{x}<br>Vol: %{y:,.2f} €/MWh<br>Range: %{customdata:,.2f} €/MWh<extra></extra>",
                customdata=df_v["Range (€/MWh)"]))
            fig_vol.add_trace(go.Scatter(
                x=df_v["Giorno"], y=roll30, name="Media mobile 30gg",
                mode="lines", line=dict(color="#eab308", width=2),
                hovertemplate="Giorno: %{x}<br>Media 30gg: %{y:,.2f} €/MWh<extra></extra>"))
            fig_vol.update_layout(template="plotly_dark", height=420,
                                  title="Volatilità realizzata giornaliera (con media mobile 30gg)",
                                  xaxis_title="Giorno", yaxis_title="Vol (€/MWh)")
            st.plotly_chart(fig_vol, use_container_width=True)

            st.markdown("**Profilo orario della volatilità** (std delle variazioni orarie per ora del giorno)")
            fig_ph_vol = go.Figure()
            fig_ph_vol.add_trace(go.Bar(
                x=[f"{h:02d}:00" for h in range(24)], y=prof_h.values, name="Vol per ora",
                marker_color="#3b82f6",
                hovertemplate="Ora: %{x}<br>Vol: %{y:,.2f} €/MWh<extra></extra>"))
            fig_ph_vol.update_layout(template="plotly_dark", height=350,
                                     title="A che ora il prezzo 'sfarfalla' di più",
                                     xaxis_title="Ora del giorno", yaxis_title="Vol (€/MWh)")
            st.plotly_chart(fig_ph_vol, use_container_width=True)

            st.markdown("**Riepilogo mensile**")
            st.dataframe(vol["per_mese"], use_container_width=True, hide_index=True)
            st.download_button(
                "⬇️ Esporta volatilità (CSV)",
                df_v.to_csv(index=False).encode("utf-8"),
                file_name=f"volatilita_{d0}_{d1}.csv",
                mime="text/csv",
                help="Scarica la tabella giornaliera: prezzo medio, range e volatilità realizzata.",
            )

    with tab15:
        titolo_yoy = edu("Confronto anno-su-anno", "Il CONFRONTO ANNO-SU-ANNO (YoY) confronta il prezzo medio di ogni mese con lo stesso mese dell'anno precedente. Serve a capire se il mercato è strutturalmente più caro o più economico rispetto a un anno fa, al netto della stagionalità: fondamentale per budget, negoziazione dei contratti annuali e per validare le curve forward (il forward sconta già questo delta?).")
        st.markdown(f"**{titolo_yoy}**: prezzo medio mensile per anno e delta YoY (€/MWh e %).", unsafe_allow_html=True)

        yoy = calcola_yoy(prezzi)
        if len(yoy["anni"]) < 2:
            st.warning("Servono almeno 2 anni di dati per il confronto YoY: seleziona un periodo personalizzato più lungo (es. gli ultimi 24 mesi).")
            if not yoy["tabella"].empty:
                st.markdown("**Medie mensili disponibili**")
                st.dataframe(yoy["tabella"], use_container_width=True, hide_index=True)
        else:
            anni = yoy["anni"]
            tab_y, dlt = yoy["tabella"], yoy["delta"]
            y0, y1 = anni[-2], anni[-1]
            p_clean = prezzi.astype(float).dropna()
            idx_py = p_clean.index.tz_localize(None) if p_clean.index.tz is not None else p_clean.index
            annuali = p_clean.groupby(idx_py.year).mean()
            m0, m1 = float(annuali.loc[y0]), float(annuali.loc[y1])
            dlt_v = dlt["Δ €/MWh"].dropna()
            if dlt_v.empty:
                st.warning("Nessun mese confrontabile tra i due anni (periodi non sovrapposti).")
            else:
                r_max = dlt.loc[dlt_v.idxmax()]
                r_min = dlt.loc[dlt_v.idxmin()]
                k1, k2, k3, k4 = st.columns(4)
                render_kpi(f"Media {y1} (€/MWh)", f"{m1:,.2f}", k1)
                render_kpi(f"Media {y0} (€/MWh)", f"{m0:,.2f}", k2)
                render_kpi("Delta annuo (€/MWh)", f"{m1 - m0:+,.2f}", k3)
                render_kpi(f"🔺 Max aumento YoY ({r_max['Mese']})", f"{r_max['Δ €/MWh']:+,.2f}", k4)
                st.caption(f"📊 Nel {y1} il prezzo medio è {m1:,.2f} €/MWh contro {m0:,.2f} €/MWh del {y0} "
                           f"({m1 - m0:+,.2f} €/MWh). Il mese con il maggior aumento è {r_max['Mese']} "
                           f"({r_max['Δ €/MWh']:+,.2f} €/MWh), quello con il maggior calo è {r_min['Mese']} "
                           f"({r_min['Δ €/MWh']:+,.2f} €/MWh).")

            colori_yoy = ["#3b82f6", "#eab308", "#10b981", "#8b5cf6", "#f97316"]
            fig_yoy = go.Figure()
            for i, y in enumerate(anni):
                vals = pd.to_numeric(tab_y[str(y)], errors="coerce")
                fig_yoy.add_trace(go.Scatter(
                    x=tab_y["Mese"], y=vals, name=str(y), mode="lines+markers",
                    line=dict(color=colori_yoy[i % len(colori_yoy)], width=2),
                    hovertemplate=f"Anno: {y}<br>Mese: %{{x}}<br>Media: %{{y:,.2f}} €/MWh<extra></extra>"))
            fig_yoy.update_layout(template="plotly_dark", height=420,
                                  title="Prezzo medio mensile per anno (€/MWh)",
                                  xaxis_title="Mese", yaxis_title="€/MWh")
            st.plotly_chart(fig_yoy, use_container_width=True)

            st.markdown(f"**Delta YoY: {y1} vs {y0}**")
            st.dataframe(dlt, use_container_width=True, hide_index=True)
            export_yoy = tab_y.merge(dlt, on="Mese", how="left")
            st.download_button(
                "⬇️ Esporta confronto YoY (CSV)",
                export_yoy.to_csv(index=False).encode("utf-8"),
                file_name=f"yoy_{d0}_{d1}.csv",
                mime="text/csv",
                help="Scarica medie mensili per anno e delta anno-su-anno (€/MWh e %).",
            )

    with tab16:
        titolo_neg = edu("Prezzi negativi", "I PREZZI NEGATIVI nascono dall'eccesso di produzione rinnovabile (soprattutto solare a mezzogiorno in primavera/estate) combinato con vincoli di dispacciamento: quando c'è più offerta che domanda e spegnere le centrali costa troppo, chi immette energia in rete CI PAGA per farlo. Per un produttore rinnovabile queste ore 'cannibalizzano' il valore; per una batteria sono opportunità di carica pagata. Il tab mostra quante ore sono sotto soglia, in quali mesi e ore del giorno si concentrano, e le peggiori ore del periodo.")
        st.markdown(f"**{titolo_neg}**: ore con prezzo sotto soglia, distribuzione mensile e oraria, peggiori ore.", unsafe_allow_html=True)

        soglia_neg = st.number_input("Soglia di analisi (€/MWh)", value=0.0, max_value=0.0, step=0.5,
                                     help="Ore conteggiate: quelle con prezzo < soglia. Il default 0,00 conta i prezzi strettamente negativi; abbassa la soglia (es. -5) per isolare solo le ore più estreme.")
        neg = calcola_prezzi_negativi(prezzi, soglia=soglia_neg)
        if neg["n_ore"] == 0:
            st.success(f"✅ Nel periodo selezionato non ci sono ore con prezzo sotto {soglia_neg:,.2f} €/MWh.")
            st.caption(f"Ore totali analizzate: {neg['tot_ore']}.")
        else:
            k1, k2, k3, k4 = st.columns(4)
            render_kpi("Ore sotto soglia", f"{neg['n_ore']}", k1)
            render_kpi("% ore periodo", f"{neg['quota_pct']:,.2f} %", k2)
            render_kpi("Prezzo minimo (€/MWh)", f"{neg['minimo']:,.2f}", k3)
            render_kpi("Media ore sotto soglia (€/MWh)", f"{neg['media_neg']:,.2f}", k4)
            st.caption(f"💡 Con 1 MW immesso costantemente in rete, le ore sotto soglia sarebbero costate "
                       f"{neg['somma']:,.2f} € in totale (somma dei prezzi negativi). Chi può fermare la produzione "
                       f"(curtailment) evita questa perdita.")

            fig_nm = go.Figure()
            fig_nm.add_trace(go.Bar(
                x=neg["mensile"]["Mese"], y=neg["mensile"]["Ore sotto soglia"],
                name="Ore sotto soglia", marker_color="#ef4444",
                hovertemplate="Mese: %{x}<br>Ore: %{y}<extra></extra>"))
            fig_nm.update_layout(template="plotly_dark", height=380,
                                 title="Ore sotto soglia per mese",
                                 xaxis_title="Mese", yaxis_title="Ore")
            st.plotly_chart(fig_nm, use_container_width=True)

            fig_no = go.Figure()
            fig_no.add_trace(go.Bar(
                x=neg["profilo_orario"]["Ora"], y=neg["profilo_orario"]["Ore sotto soglia"],
                name="Ore sotto soglia", marker_color="#f59e0b",
                hovertemplate="Ora: %{x}<br>Ore: %{y}<extra></extra>"))
            fig_no.update_layout(template="plotly_dark", height=380,
                                 title="Distribuzione per ora del giorno (solare? di solito a mezzogiorno)",
                                 xaxis_title="Ora", yaxis_title="Ore")
            st.plotly_chart(fig_no, use_container_width=True)

            st.markdown("**20 peggiori ore del periodo**")
            st.dataframe(neg["top"], use_container_width=True, hide_index=True)
            st.download_button(
                "⬇️ Esporta peggiori ore (CSV)",
                neg["top"].to_csv(index=False).encode("utf-8"),
                file_name=f"prezzi_negativi_{d0}_{d1}.csv",
                mime="text/csv",
                help="Scarica le 20 ore con i prezzi più bassi del periodo selezionato.",
            )

    with tab17:
        titolo_id = edu("Spread intra-day", "Lo SPREAD INTRA-DAY di un giorno è la differenza tra il suo prezzo massimo e il suo prezzo minimo (max − min). Per un energy analyst è la misura diretta del valore della flessibilità: una batteria o un carico flessibile possono 'comprare' nelle ore di minimo e 'vendere' in quelle di massimo, catturando questo range ogni giorno. Questo tab mostra quanto è ampio in media, in quali giorni è massimo, a che ora si verificano tipicamente minimo e massimo, e come varia per mese.")
        st.markdown(f"**{titolo_id}**: range giornaliero max−min (valore della flessibilità), ora del minimo e del massimo, distribuzione mensile.", unsafe_allow_html=True)
        sd = calcola_spread_intraday(prezzi)
        if sd["n_giorni"] == 0:
            st.info("Nessun dato giornaliero disponibile per il periodo selezionato.")
        else:
            k1, k2, k3, k4 = st.columns(4)
            render_kpi("Range medio giornaliero (€/MWh)", f"{sd['range_medio']:,.2f}", k1)
            render_kpi(edu("Range massimo (€/MWh)", "Il giorno con lo spread più ampio del periodo: massima opportunità di arbitraggio giornaliero per batterie e carichi flessibili."), f"{sd['range_max']:,.2f}<br><small>{sd['data_max']}</small>", k2)
            render_kpi("Ora del minimo (più frequente)", sd["ora_min_freq"], k3)
            render_kpi("Ora del massimo (più frequente)", sd["ora_max_freq"], k4)
            st.caption(f"💡 Giorni analizzati: {sd['n_giorni']}. Un impianto da 1 MW capace di catturare metà del range medio giornaliero ogni giorno vale circa {sd['range_medio'] / 2:,.2f} €/giorno di arbitraggio teorico.")

            fig_sd = go.Figure()
            fig_sd.add_trace(go.Bar(
                x=sd["giornaliero"]["Data"], y=sd["giornaliero"]["Range €/MWh"],
                name="Range giornaliero", marker_color="#22d3ee",
                hovertemplate="Data: %{x}<br>Range: %{y:.2f} €/MWh<extra></extra>"))
            fig_sd.add_hline(y=sd["range_medio"], line_dash="dash", line_color="#eab308",
                             annotation_text=f"Media: {sd['range_medio']:.0f} €/MWh", annotation_position="top left")
            fig_sd.update_layout(template="plotly_dark", height=400,
                                 title="Range giornaliero max−min (€/MWh)",
                                 xaxis_title="Data", yaxis_title="Range (€/MWh)")
            st.plotly_chart(fig_sd, use_container_width=True)

            col_s1, col_s2 = st.columns(2)
            with col_s1:
                fig_sm = go.Figure()
                fig_sm.add_trace(go.Bar(
                    x=sd["mensile"]["Mese"], y=sd["mensile"]["Range medio €/MWh"],
                    name="Range medio", marker_color="#38bdf8",
                    hovertemplate="Mese: %{x}<br>Media: %{y:.2f} €/MWh<extra></extra>"))
                fig_sm.update_layout(template="plotly_dark", height=360,
                                     title="Range medio mensile",
                                     xaxis_title="Mese", yaxis_title="Range medio (€/MWh)")
                st.plotly_chart(fig_sm, use_container_width=True)
            with col_s2:
                ore_min_c = sd["giornaliero"]["Ora min"].value_counts().sort_index()
                ore_max_c = sd["giornaliero"]["Ora max"].value_counts().sort_index()
                fig_so = go.Figure()
                fig_so.add_trace(go.Bar(x=ore_min_c.index, y=ore_min_c.values, name="Ore di minimo",
                                        marker_color="#34d399",
                                        hovertemplate="Ora: %{x}<br>Giorni: %{y}<extra></extra>"))
                fig_so.add_trace(go.Bar(x=ore_max_c.index, y=ore_max_c.values, name="Ore di massimo",
                                        marker_color="#f87171",
                                        hovertemplate="Ora: %{x}<br>Giorni: %{y}<extra></extra>"))
                fig_so.update_layout(template="plotly_dark", height=360,
                                     title="Distribuzione ore di minimo e massimo",
                                     xaxis_title="Ora", yaxis_title="Giorni",
                                     barmode="group")
                st.plotly_chart(fig_so, use_container_width=True)

            st.markdown("**20 giorni con lo spread più ampio**")
            top_sd = sd["giornaliero"].sort_values("Range €/MWh", ascending=False).head(20)
            st.dataframe(top_sd, use_container_width=True, hide_index=True)
            st.download_button(
                "⬇️ Esporta spread giornaliero (CSV)",
                sd["giornaliero"].to_csv(index=False).encode("utf-8"),
                file_name=f"spread_intraday_{d0}_{d1}.csv",
                mime="text/csv",
                help="Scarica il range giornaliero max−min con ore di minimo e massimo per ogni giorno del periodo selezionato.",
            )

    with tab18:
        titolo_id = edu("Picchi di prezzo", "Un PICCO è un'ora in cui il prezzo spot supera una soglia di scarsità (qui 200 €/MWh di default, modificabile). I picchi nascono da domanda alta e offerta scarsa (serate invernali senza vento, guasti alle centrali) ed è lì che un impianto flessibile — peaker a gas, batteria, domanda interrompibile — incassa i margini più alti. Questo tab conta le ore sopra soglia, misura la durata dei cluster (un picco di 4 ore consecutive vale molto più di 4 ore isolate) e confronta la soglia con i percentili P99/P99.5 della serie.")
        st.markdown(f"**{titolo_id}**: ore sopra soglia di scarsità, cluster consecutivi, percentili P99/P99.5 e le 20 ore più care.", unsafe_allow_html=True)
        soglia_pk = st.slider("🎯 Soglia di picco (€/MWh)", min_value=50, max_value=600, value=200, step=10,
                              help="Ore con prezzo maggiore o uguale a questa soglia contano come picchi.")
        pk = calcola_picchi(prezzi, soglia=float(soglia_pk))
        if pk["tot_ore"] == 0:
            st.info("Nessun dato disponibile per il periodo selezionato.")
        else:
            k1, k2, k3, k4 = st.columns(4)
            render_kpi(f"Ore sopra {soglia_pk} €/MWh", f"{pk['n_ore']:,}<br><small>{pk['quota_pct']:.2f}% delle ore</small>", k1)
            if pk["massimo"] is not None:
                render_kpi("Prezzo massimo (€/MWh)", f"{pk['massimo']:,.2f}<br><small>{pk['data_max'][0]} {pk['data_max'][1]}</small>", k2)
            else:
                render_kpi("Prezzo massimo (€/MWh)", "—", k2)
            render_kpi("Cluster più lungo (ore)", f"{pk['cluster_max_ore']}<br><small>{pk['n_cluster']} cluster totali</small>", k3)
            render_kpi(edu("Soglia P99.5 (€/MWh)", "Il prezzo superato solo nello 0,5% delle ore: se la soglia di picco scelta è molto sopra il P99.5, i picchi sono eventi davvero estremi; se è sotto, cattura anche eventi frequenti."), f"{pk['p995']:,.2f}<br><small>P99: {pk['p99']:,.2f}</small>", k4)
            st.caption(f"💡 Ore analizzate: {pk['tot_ore']:,}. Un peaker da 1 MW che cattura ogni ora sopra {soglia_pk} €/MWh avrebbe incassato ricavi spot concentrati in {pk['n_ore']} ore ({pk['quota_pct']:.2f}% del periodo).")

            col_p1, col_p2 = st.columns(2)
            with col_p1:
                fig_pm = go.Figure()
                fig_pm.add_trace(go.Bar(
                    x=pk["mensile"]["Mese"], y=pk["mensile"]["Ore sopra soglia"],
                    name="Ore sopra soglia", marker_color="#f59e0b",
                    hovertemplate="Mese: %{x}<br>Ore: %{y}<extra></extra>"))
                fig_pm.update_layout(template="plotly_dark", height=360,
                                     title=f"Ore sopra {soglia_pk} €/MWh per mese",
                                     xaxis_title="Mese", yaxis_title="Ore")
                st.plotly_chart(fig_pm, use_container_width=True)
            with col_p2:
                fig_po = go.Figure()
                fig_po.add_trace(go.Bar(
                    x=pk["profilo_orario"]["Ora"], y=pk["profilo_orario"]["Ore sopra soglia"],
                    name="Ore sopra soglia", marker_color="#ef4444",
                    hovertemplate="Ora: %{x}<br>Ore: %{y}<extra></extra>"))
                fig_po.update_layout(template="plotly_dark", height=360,
                                     title="Profilo orario dei picchi",
                                     xaxis_title="Ora", yaxis_title="Ore")
                st.plotly_chart(fig_po, use_container_width=True)

            st.markdown("**20 ore più care del periodo**")
            st.dataframe(pk["top"], use_container_width=True, hide_index=True)
            st.download_button(
                "⬇️ Esporta picchi (CSV)",
                pk["top"].to_csv(index=False).encode("utf-8"),
                file_name=f"picchi_prezzo_{d0}_{d1}.csv",
                mime="text/csv",
                help="Scarica le 20 ore con prezzo più alto del periodo selezionato.",
            )

    with tab19:
        titolo_sw = edu("Profilo settimanale tipo", "Il PROFILO SETTIMANALE TIPO è la media del prezzo spot per ogni combinazione giorno-della-settimana × ora (matrice 7×24): mostra a colpo d'occhio quando l'energia costa di solito meno (tipicamente le notti del weekend) e quando di più (le serate feriali). Un carico flessibile, una pompa di calore o una ricarica programmata spostano i consumi nelle caselle verdi; la manutenzione degli impianti si pianifica nelle ore rosse, quando fermarsi costa meno. A differenza del tab Weekend (media lun-ven vs sab-dom), qui ogni giorno ha il suo profilo orario completo.")
        st.markdown(f"**{titolo_sw}**: prezzo medio per giorno della settimana × ora, le finestre più economiche e il confronto tra i profili dei singoli giorni.", unsafe_allow_html=True)
        sw = calcola_profilo_settimanale(prezzi)
        if sw["tot_ore"] == 0:
            st.info("Nessun dato disponibile per il periodo selezionato.")
        else:
            k1, k2, k3, k4 = st.columns(4)
            render_kpi(edu("Giorno più economico", "Giorno della settimana con il prezzo medio più basso nel periodo: il candidato naturale per spostare i consumi flessibili."), f"{sw['giorno_min'][0]}<br><small>{sw['giorno_min'][1]:,.2f} €/MWh</small>", k1)
            render_kpi(edu("Giorno più caro", "Giorno della settimana con il prezzo medio più alto: conviene ridurre i consumi flessibili o coprirsi in anticipo."), f"{sw['giorno_max'][0]}<br><small>{sw['giorno_max'][1]:,.2f} €/MWh</small>", k2)
            render_kpi("Ora più economica (media)", f"{sw['ora_min'][0]:02d}:00<br><small>{sw['ora_min'][1]:,.2f} €/MWh</small>", k3)
            render_kpi("Ora più cara (media)", f"{sw['ora_max'][0]:02d}:00<br><small>{sw['ora_max'][1]:,.2f} €/MWh</small>", k4)
            st.caption(f"💡 Ore analizzate: {sw['n_ore']:,}. La combinazione più economica è {sw['coppia_min'][0]} ore {sw['coppia_min'][1]:02d}:00 ({sw['coppia_min'][2]:,.2f} €/MWh), la più cara {sw['coppia_max'][0]} ore {sw['coppia_max'][1]:02d}:00 ({sw['coppia_max'][2]:,.2f} €/MWh): ampiezza del pattern settimanale {sw['ampiezza']:,.2f} €/MWh.")

            fig_sw = go.Figure(data=go.Heatmap(
                z=sw["matrice"].values,
                x=[f"{h:02d}" for h in range(24)],
                y=list(sw["matrice"].index),
                colorscale="RdYlGn_r",
                hovertemplate="Giorno: %{y}<br>Ora: %{x}:00<br>Prezzo medio: %{z:.2f} €/MWh<extra></extra>",
                colorbar=dict(title="€/MWh")))
            fig_sw.update_layout(template="plotly_dark", height=380,
                                 title="Prezzo medio per giorno × ora (€/MWh)",
                                 xaxis_title="Ora del giorno", yaxis_title="")
            st.plotly_chart(fig_sw, use_container_width=True)

            col_s1, col_s2 = st.columns(2)
            with col_s1:
                giorno_sel = st.selectbox("📅 Giorno da confrontare", list(sw["matrice"].index),
                                          index=list(sw["matrice"].index).index("Sabato") if "Sabato" in list(sw["matrice"].index) else 0,
                                          help="Profilo orario del giorno scelto contro la media di tutte le ore del periodo.")
                fig_sg = go.Figure()
                fig_sg.add_trace(go.Scatter(x=list(range(24)), y=sw["media_ora"]["Prezzo €/MWh"].tolist(),
                                            mode="lines", name="Media tutte le ore",
                                            line=dict(dash="dash", color="#9ca3af"),
                                            hovertemplate="Ora: %{x}:00<br>Media: %{y:.2f} €/MWh<extra></extra>"))
                riga_g = sw["matrice"].loc[giorno_sel].tolist()
                fig_sg.add_trace(go.Scatter(x=list(range(24)), y=riga_g,
                                            mode="lines+markers", name=giorno_sel,
                                            line=dict(color="#38bdf8"),
                                            hovertemplate=f"{giorno_sel} " + "Ora: %{x}:00<br>Prezzo: %{y:.2f} €/MWh<extra></extra>"))
                fig_sg.update_layout(template="plotly_dark", height=360,
                                     title=f"Profilo orario: {giorno_sel} vs media",
                                     xaxis_title="Ora", yaxis_title="€/MWh")
                st.plotly_chart(fig_sg, use_container_width=True)
            with col_s2:
                st.markdown("**Media per giorno della settimana**")
                fig_sgd = go.Figure()
                fig_sgd.add_trace(go.Bar(
                    x=sw["media_giorno"]["Giorno"], y=sw["media_giorno"]["Prezzo €/MWh"],
                    marker_color="#38bdf8",
                    hovertemplate="Giorno: %{x}<br>Prezzo medio: %{y:.2f} €/MWh<extra></extra>"))
                fig_sgd.update_layout(template="plotly_dark", height=360,
                                      title="Prezzo medio per giorno",
                                      xaxis_title="", yaxis_title="€/MWh")
                st.plotly_chart(fig_sgd, use_container_width=True)

            st.markdown("**10 finestre giorno-ora più economiche**")
            st.dataframe(sw["finestre"], use_container_width=True, hide_index=True)
            st.download_button(
                "⬇️ Esporta finestre economiche (CSV)",
                sw["finestre"].to_csv(index=False).encode("utf-8"),
                file_name=f"finestre_economiche_{d0}_{d1}.csv",
                mime="text/csv",
                help="Scarica le 10 combinazioni giorno-ora con prezzo medio più basso del periodo selezionato.",
            )

    with tab20:
        titolo_cd = edu("Curva di durata", "La CURVA DI DURATA (price duration curve) ordina tutte le ore del periodo dal prezzo più alto al più basso: l'asse orizzontale è il numero di ore cumulative. A sinistra si legge per quante ore l'energia è costata cara (esposizione ai picchi), a destra per quante ore è costata poco (valli da sfruttare con carichi flessibili o storage). I percentili P95/P50/P5 indicano i livelli di prezzo superati rispettivamente dal 5%, 50% e 95% delle ore: sono la base per i ragionamenti di tipo VaR (value at risk) sul costo di fornitura. A differenza del tab Picchi (soglia fissa scelta dall'utente), qui i livelli P95/P50/P5 emergono dai dati.")
        st.markdown(f"**{titolo_cd}**: prezzi orari ordinati dal più alto al più basso, percentili e distribuzione per decili.", unsafe_allow_html=True)
        cd = calcola_curva_durata(prezzi, soglia=soglia)
        if cd["tot_ore"] == 0:
            st.info("Nessun dato disponibile per il periodo selezionato.")
        else:
            k1, k2, k3, k4 = st.columns(4)
            render_kpi(edu("P95 (€/MWh)", "Livello di prezzo superato solo dal 5% delle ore più care: misura l'esposizione ai picchi del periodo."), f"{cd['p95']:,.2f}<br><small>{cd['ore_sopra_p95']} h sopra ({cd['ore_sopra_p95']/cd['n_ore']*100:.1f} %)</small>", k1)
            render_kpi(edu("Mediana P50 (€/MWh)", "Prezzo mediano: metà delle ore costa di più, metà di meno. Più robusto della media contro i picchi."), f"{cd['p50']:,.2f}", k2)
            render_kpi(edu("P5 (€/MWh)", "Livello di prezzo superato dal 95% delle ore: il pavimento della distribuzione, interessante per carichi flessibili."), f"{cd['p5']:,.2f}", k3)
            render_kpi(edu("Media 10% più care", "Prezzo medio del decile più caro: dove concentrare coperture e hedging se si teme la coda destra."), f"{cd['media_top10']:,.2f}", k4)
            cap_cd = (f"💡 Ore analizzate: {cd['n_ore']:,}. "
                      f"Media 10% più economiche: {cd['media_bottom10']:,.2f} €/MWh.")
            # FIX 27/09: il rapporto confronta i DECILI (10%), non il 5%; con prezzi
            # negativi il rapporto non ha senso e viene omesso.
            b10 = cd["media_bottom10"]
            if b10 and b10 > 0:
                cap_cd += (f" Il 10% di ore più care costa in media "
                           f"{cd['media_top10']/b10:.1f}x rispetto al 10% più economico.")
            st.caption(cap_cd)

            fig_cd = go.Figure()
            fig_cd.add_trace(go.Scatter(
                x=cd["curva"]["Ore cumulative"], y=cd["curva"]["Prezzo €/MWh"],
                mode="lines", name="Prezzo per ora ordinata",
                line=dict(color="#38bdf8", width=2),
                fill="tozeroy", fillcolor="rgba(56, 189, 248, 0.12)",
                hovertemplate="Ore cumulative: %{x}<br>Prezzo: %{y:.2f} €/MWh<extra></extra>"))
            fig_cd.add_hline(y=cd["p95"], line_dash="dash", line_color="#ef4444",
                             annotation_text=f"P95 {cd['p95']:,.0f} €/MWh", annotation_position="top right")
            fig_cd.add_hline(y=cd["p50"], line_dash="dash", line_color="#eab308",
                             annotation_text=f"P50 {cd['p50']:,.0f} €/MWh", annotation_position="top right")
            fig_cd.add_hline(y=cd["p5"], line_dash="dash", line_color="#22c55e",
                             annotation_text=f"P5 {cd['p5']:,.0f} €/MWh", annotation_position="bottom right")
            if cd["ore_sopra_soglia"]:
                fig_cd.add_vline(x=cd["ore_sopra_soglia"], line_dash="dot", line_color="#f97316",
                                 annotation_text=f"Soglia alert: {cd['ore_sopra_soglia']} h", annotation_position="top left")
            fig_cd.update_layout(template="plotly_dark", height=420,
                                 title="Curva di durata del prezzo (€/MWh)",
                                 xaxis_title="Ore cumulative (dalla più cara alla più economica)",
                                 yaxis_title="Prezzo (€/MWh)",
                                 legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig_cd, use_container_width=True)

            st.markdown("**Prezzo per decile**")
            st.dataframe(cd["decili"], use_container_width=True, hide_index=True)
            st.download_button(
                "⬇️ Esporta curva di durata (CSV)",
                cd["curva"].to_csv(index=False).encode("utf-8"),
                file_name=f"curva_durata_{d0}_{d1}.csv",
                mime="text/csv",
                help="Scarica la curva di durata: ore cumulative e prezzo ordinato in modo decrescente.",
            )

    with tab21:
        titolo_cc = edu("Concentrazione del costo", "La CONCENTRAZIONE DEL COSTO mostra quanta parte della bolletta del periodo è generata dalle ore più care: si prende il tuo profilo di consumo (MW per fascia), si calcola il costo di ogni ora (prezzo spot × MW), si ordinano le ore dalla più cara alla più economica e si cumula la quota di costo (curva di Lorenz). Se il 10% di ore più care genera il 40% del costo, la coda destra è il rischio da coprire: è l'argomento quantitativo per proporre un hedging. A differenza del tab Curva durata (che guarda la distribuzione dei PREZZI), qui pesa il CONSUMO: due clienti con lo stesso spot possono avere concentrazioni molto diverse.")
        st.markdown(f"**{titolo_cc}**: quota di costo generata dalle ore più care, con il tuo profilo di carico.", unsafe_allow_html=True)

        cc1, cc2, cc3 = st.columns(3)
        with cc1:
            cc_f1 = st.number_input("Potenza in F1 (MW)", min_value=0.0, value=1.0, step=0.5, key="cc_f1",
                                    help="Ore di punta: lun–ven 08:00–19:00.")
        with cc2:
            cc_f2 = st.number_input("Potenza in F2 (MW)", min_value=0.0, value=1.0, step=0.5, key="cc_f2",
                                    help="Ore intermedie: lun–ven 07:00–08:00 e 19:00–23:00, sab 07:00–23:00.")
        with cc3:
            cc_f3 = st.number_input("Potenza in F3 (MW)", min_value=0.0, value=1.0, step=0.5, key="cc_f3",
                                    help="Ore fuori punta: notti, domeniche e festivi.")
        conc = calcola_concentrazione_costo(prezzi, cc_f1, cc_f2, cc_f3)
        if conc["n_ore"] == 0:
            st.info("Imposta una potenza maggiore di zero in almeno una fascia per calcolare la concentrazione del costo.")
        elif conc["totale"] <= 0:
            st.warning("Costo totale del periodo non positivo (prezzi negativi dominanti): le quote di concentrazione non sono significative.")
        else:
            g1, g2, g3, g4 = st.columns(4)
            render_kpi(edu("Quota costo nel 10% di ore più care", "Percentuale della bolletta generata dal decile di ore più care: più è alta, più conviene coprire (hedging) la coda destra invece di pagare lo spot."), f"{conc['quota_top10']:.1f} %<br><small>{conc['costo_top10']:,.0f} €</small>", g1)
            render_kpi(edu("Quota costo nel 5% di ore più care", "Quota di costo nel 5% di ore più care: misura l'esposizione agli spike estremi."), f"{conc['quota_top5']:.1f} %", g2)
            render_kpi(edu("Ore per il 50% del costo", "In quante ore (le più care) si concentra metà della bolletta: poche ore = rischio concentrato e copribile."), f"{conc['ore_50pct']:,} h<br><small>({conc['ore_50pct']/conc['n_ore']*100:.1f} % delle ore)</small>", g3)
            gini_txt = f"{conc['gini']:.3f}" if conc['gini'] is not None else "n.d."
            render_kpi(edu("Indice di Gini", "0 = costo perfettamente uniforme tra le ore, 1 = tutto il costo in un'ora sola. Sopra ~0.5 la bolletta è dominata dai picchi: forte caso per l'hedging."), gini_txt, g4)
            st.caption(f"💡 Profilo: F1 {cc_f1} MW, F2 {cc_f2} MW, F3 {cc_f3} MW — "
                       f"{conc['mwh']:,.0f} MWh per {conc['totale']:,.0f} € nel periodo "
                       f"({conc['n_ore']:,} ore).")

            col_l1, col_l2 = st.columns(2)
            with col_l1:
                fig_lz = go.Figure()
                fig_lz.add_trace(go.Scatter(
                    x=conc["lorenz"]["Quota ore %"], y=conc["lorenz"]["Quota costo %"],
                    mode="lines", name="Costo cumulato",
                    line=dict(color="#f59e0b", width=2.5),
                    fill="tozeroy", fillcolor="rgba(245, 158, 11, 0.12)",
                    hovertemplate="Ore: %{x:.1f} %<br>Costo cumulato: %{y:.1f} %<extra></extra>"))
                fig_lz.add_trace(go.Scatter(
                    x=[0, 100], y=[0, 100], mode="lines", name="Uguaglianza perfetta",
                    line=dict(color="#6b7280", width=1, dash="dash")))
                fig_lz.update_layout(template="plotly_dark", height=380,
                                     title="Curva di Lorenz del costo",
                                     xaxis_title="Quota di ore (dalla più cara, %)",
                                     yaxis_title="Quota di costo cumulata (%)",
                                     legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
                st.plotly_chart(fig_lz, use_container_width=True)
            with col_l2:
                fig_dc = go.Figure()
                fig_dc.add_trace(go.Bar(
                    x=conc["decili"]["Decile"], y=conc["decili"]["Quota costo %"],
                    name="Quota costo %", marker_color="#f59e0b",
                    hovertemplate="Decile: %{x}<br>Quota costo: %{y:.1f} %<br>Costo: %{customdata:,.0f} €<extra></extra>",
                    customdata=conc["decili"]["Costo (€)"]))
                fig_dc.update_layout(template="plotly_dark", height=380,
                                     title="Quota di costo per decile di prezzo (D1 = 10% ore più care)",
                                     xaxis_title="Decile", yaxis_title="Quota costo (%)")
                st.plotly_chart(fig_dc, use_container_width=True)

            st.markdown("**Dettaglio per decile di prezzo**")
            st.caption("D1 = 10% di ore più care · D10 = 10% di ore più economiche.")
            st.dataframe(conc["decili"], use_container_width=True, hide_index=True)
            st.download_button(
                "⬇️ Esporta concentrazione costo (CSV)",
                conc["decili"].to_csv(index=False).encode("utf-8"),
                file_name=f"concentrazione_costo_{d0}_{d1}.csv",
                mime="text/csv",
                help="Scarica il dettaglio per decile: ore, costo e quota di costo.",
            )

    with tab22:
        titolo_sh = edu("Shifting del carico", "Il DEMAND SHIFTING (spostamento del carico) è la capacità di muovere consumo dalle ore più care alle ore più economiche senza cambiare il totale consumato: tipico di chi ha carichi flessibili (pompe, cold storage, ricarica EV, batch industriali). Qui si simula: si prendono le ore più care per COSTO (prezzo × MW) fino al X% dei MWh del periodo e si 'ricaricano' gli stessi MWh nelle ore con prezzo più basso. Il risparmio stimato è il valore economico della flessibilità: il numero da portare al tavolo per valutare investimenti in storage o contratti di demand response. A differenza del tab Concentrazione (che MISURA il problema), qui si SIMULA la soluzione.")
        st.markdown(f"**{titolo_sh}**: quanto si risparmierebbe spostando parte del consumo dalle ore più care alle più economiche.", unsafe_allow_html=True)

        sh1, sh2, sh3, sh4 = st.columns(4)
        with sh1:
            sh_f1 = st.number_input("Potenza in F1 (MW)", min_value=0.0, value=1.0, step=0.5, key="sh_f1",
                                    help="Ore di punta: lun–ven 08:00–19:00.")
        with sh2:
            sh_f2 = st.number_input("Potenza in F2 (MW)", min_value=0.0, value=1.0, step=0.5, key="sh_f2",
                                    help="Ore intermedie: lun–ven 07:00–08:00 e 19:00–23:00, sab 07:00–23:00.")
        with sh3:
            sh_f3 = st.number_input("Potenza in F3 (MW)", min_value=0.0, value=1.0, step=0.5, key="sh_f3",
                                    help="Ore fuori punta: notti, domeniche e festivi.")
        with sh4:
            sh_pct = st.slider("Quota di energia spostata (%)", min_value=0, max_value=30, value=10, step=1, key="sh_pct",
                               help="Percentuale dei MWh del periodo spostata dalle ore più care a quelle più economiche (tetto 50% nell'helper).")
        sh = calcola_shifting_carico(prezzi, sh_f1, sh_f2, sh_f3, sh_pct)
        if sh["n_ore"] == 0:
            st.info("Imposta una potenza maggiore di zero in almeno una fascia per simulare lo shifting.")
        elif sh["pct"] == 0:
            st.info("Aumenta la quota di energia spostata (slider) per vedere il risparmio stimato.")
        else:
            s1, s2, s3, s4 = st.columns(4)
            render_kpi(edu("Risparmio stimato (€)", "Costo delle ore più care meno costo degli stessi MWh ricaricati nelle ore più economiche: il valore economico della flessibilità nel periodo."), f"{sh['risparmio']:,.0f} €", s1)
            rp = f"{sh['risparmio_pct']:.1f} %" if sh['risparmio_pct'] is not None else "n.d."
            render_kpi(edu("Risparmio %", "Risparmio rapportato al costo totale del periodo senza shifting: la leva percentuale del demand response."), rp, s2)
            render_kpi(edu("MWh spostati", "Energia spostata dalle ore più care (ore fonte) alle ore più economiche (ore destinazione): il consumo totale resta invariato."), f"{sh['mwh_spostati']:,.1f} MWh<br><small>{sh['ore_fonte']:,} h fonte → {sh['ore_dest']:,} h dest.</small>", s3)
            render_kpi(edu("Costo dopo shifting (€)", "Costo totale del periodo se si applicasse lo shifting simulato: costo attuale meno risparmio stimato."), f"{sh['costo_dopo']:,.0f} €", s4)
            st.caption(f"💡 {sh['mwh']:,.0f} MWh per {sh['totale']:,.0f} € senza shifting — "
                       f"ore fonte: costo {sh['costo_fonte']:,.0f} €, ore destinazione: costo {sh['costo_dest']:,.0f} €. "
                       "Con prezzi negativi, spostare verso ore a prezzo negativo genera ricavo (risparmio > costo fonte).")

            fig_sh = go.Figure()
            fig_sh.add_trace(go.Bar(
                x=sh["mensile"]["Mese"], y=sh["mensile"]["Risparmio (€)"],
                name="Risparmio €", marker_color="#22c55e",
                hovertemplate="Mese: %{x}<br>Risparmio: %{y:,.0f} €<br>MWh spostati: %{customdata:,.1f}<extra></extra>",
                customdata=sh["mensile"]["MWh spostati"]))
            fig_sh.update_layout(template="plotly_dark", height=380,
                                 title=f"Risparmio mensile da shifting ({sh['pct']:.0f}% dei MWh)",
                                 xaxis_title="Mese", yaxis_title="Risparmio (€)")
            st.plotly_chart(fig_sh, use_container_width=True)

            st.markdown("**Dettaglio mensile**")
            st.dataframe(sh["mensile"], use_container_width=True, hide_index=True)
            st.download_button(
                "⬇️ Esporta shifting carico (CSV)",
                sh["mensile"].to_csv(index=False).encode("utf-8"),
                file_name=f"shifting_carico_{d0}_{d1}.csv",
                mime="text/csv",
                help="Scarica il dettaglio mensile: MWh spostati, costo prima/dopo e risparmio.",
            )

    with tab23:
        titolo_fo = edu("Finestre di acquisto ottimali", "Il TIMING DI ACQUISTO è il valore di comprare (o consumare in modo flessibile) nelle ore più economiche: per ogni giorno il tab trova la finestra di W ore CONSECUTIVE che minimizza il costo di acquisto (prezzo × MW di fascia). Lo sconto % misura quanto quella finestra batte la media giornaliera: è il margine teorico di una strategia 'buy-the-dip' oraria per carichi flessibili (ricarica, pompaggi, batch). A differenza del tab Shifting (che SIMULA lo spostamento di energia), qui si MISURA il vantaggio di prezzo di ogni giorno: dove e quando conviene comprare.")
        st.markdown(f"**{titolo_fo}**: per ogni giorno, la finestra di ore consecutive più economica per acquistare.", unsafe_allow_html=True)

        fo1, fo2, fo3, fo4 = st.columns(4)
        with fo1:
            fo_f1 = st.number_input("Potenza in F1 (MW)", min_value=0.0, value=1.0, step=0.5, key="fo_f1",
                                    help="Ore di punta: lun–ven 08:00–19:00.")
        with fo2:
            fo_f2 = st.number_input("Potenza in F2 (MW)", min_value=0.0, value=1.0, step=0.5, key="fo_f2",
                                    help="Ore intermedie: lun–ven 07:00–08:00 e 19:00–23:00, sab 07:00–23:00.")
        with fo3:
            fo_f3 = st.number_input("Potenza in F3 (MW)", min_value=0.0, value=1.0, step=0.5, key="fo_f3",
                                    help="Ore fuori punta: notti, domeniche e festivi.")
        with fo4:
            fo_w = st.slider("Durata finestra (ore consecutive)", min_value=1, max_value=12, value=4, step=1, key="fo_w",
                             help="Numero di ore consecutive della finestra di acquisto ottimale.")
        fo = calcola_finestre_ottimali(prezzi, fo_f1, fo_f2, fo_f3, fo_w)
        if fo["n_giorni"] == 0:
            st.info("Imposta una potenza maggiore di zero in almeno una fascia per trovare le finestre ottimali.")
        else:
            f1, f2, f3, f4 = st.columns(4)
            pfin = f"{fo['prezzo_finestra']:,.2f} €/MWh" if fo["prezzo_finestra"] is not None else "n.d."
            render_kpi(edu("Prezzo medio in finestra", "Media €/MWh pesata sui MWh delle finestre ottimali di tutti i giorni: il prezzo che pagheresti comprando solo nelle finestre migliori."), pfin, f1)
            sc = f"{fo['sconto_pct']:.1f} %" if fo["sconto_pct"] is not None else "n.d."
            render_kpi(edu("Sconto medio vs media giornaliera", "Media degli sconti % giornalieri: quanto la finestra ottimale batte in media il prezzo medio del giorno. Il margine teorico del timing di acquisto."), sc, f2)
            render_kpi(edu("MWh in finestra", "Energia totale coperta dalle finestre ottimali nel periodo: i MWh su cui si applica lo sconto."), f"{fo['mwh_finestra']:,.1f} MWh<br><small>{fo['n_giorni']} giorni × {fo['w']} h</small>", f3)
            om = f"{fo['ora_moda']:02d}:00" if fo["ora_moda"] is not None else "n.d."
            render_kpi(edu("Ora di inizio più frequente", "L'ora in cui la finestra ottimale inizia più spesso: l'abitudine di acquisto da fissare in procedura."), om, f4)
            st.caption("💡 Lo sconto è 'n.d.' nei giorni con media giornaliera ≤ 0 (prezzi negativi dominanti): la finestra resta comunque quella a costo minimo.")

            fig_fo = go.Figure()
            fig_fo.add_trace(go.Bar(
                x=fo["distrib_ore"]["Ora"], y=fo["distrib_ore"]["Giorni"],
                name="Giorni", marker_color="#3b82f6",
                hovertemplate="Ora inizio: %{x}:00<br>Giorni: %{y}<extra></extra>"))
            fig_fo.update_layout(template="plotly_dark", height=360,
                                 title=f"Distribuzione ora di inizio della finestra ottimale ({fo['w']} h)",
                                 xaxis_title="Ora di inizio", yaxis_title="Giorni",
                                 xaxis=dict(tickmode="linear", dtick=2))
            st.plotly_chart(fig_fo, use_container_width=True)

            fig_fom = go.Figure()
            fig_fom.add_trace(go.Bar(
                x=fo["mensile"]["Mese"], y=fo["mensile"]["Sconto medio %"],
                name="Sconto %", marker_color="#22c55e",
                hovertemplate="Mese: %{x}<br>Sconto medio: %{y:.1f} %<br>€/MWh finestra: %{customdata:,.2f}<extra></extra>",
                customdata=fo["mensile"]["€/MWh finestra"].fillna(0)))
            fig_fom.update_layout(template="plotly_dark", height=360,
                                  title="Sconto medio mensile vs media giornaliera",
                                  xaxis_title="Mese", yaxis_title="Sconto medio (%)")
            st.plotly_chart(fig_fom, use_container_width=True)

            st.markdown("**Dettaglio giornaliero**")
            st.dataframe(fo["giornaliero"], use_container_width=True, hide_index=True)
            st.download_button(
                "⬇️ Esporta finestre di acquisto (CSV)",
                fo["giornaliero"].to_csv(index=False).encode("utf-8"),
                file_name=f"finestre_acquisto_{d0}_{d1}.csv",
                mime="text/csv",
                help="Scarica il dettaglio giornaliero: finestra ottimale, €/MWh, sconto vs media giorno.",
            )

    with tab24:
        titolo_stag = edu("Stagionalità mensile", "La STAGIONALITÀ è la componente prevedibile del prezzo legata al calendario: in inverno la domanda di riscaldamento spinge i prezzi su, in primavera/estate rinnovabili abbondanti e domanda bassa li spingono giù. Il fattore stagionale (media del mese / media annuale) misura questo effetto: sopra 1 il mese è strutturalmente più caro, sotto 1 più economico. A differenza del tab YoY (che confronta ANNI diversi) e del profilo settimanale (che confronta GIORNI della settimana), qui si misura il ciclo ANNUALE: serve per allocare il budget mese per mese, negoziare contratti a prezzo fisso e validare le curve forward mensili.")
        st.markdown(f"**{titolo_stag}**: prezzo medio per mese solare e fattore stagionale (media mese / media annuale).", unsafe_allow_html=True)

        stg = calcola_stagionalita(prezzi)
        if stg["mensile"].empty:
            st.info("Nessun dato valido nel periodo per calcolare la stagionalità.")
        else:
            s1, s2, s3, s4 = st.columns(4)
            caro = f"{stg['mese_piu_caro']['mese']}<br><small>×{stg['mese_piu_caro']['fattore']:.3f}</small>" if stg["mese_piu_caro"] else "n.d."
            render_kpi(edu("Mese più caro", "Il mese con il fattore stagionale più alto: strutturalmente il più caro dell'anno. Pianifica lì il picco di budget e la copertura forward."), caro, s1)
            econ = f"{stg['mese_piu_economico']['mese']}<br><small>×{stg['mese_piu_economico']['fattore']:.3f}</small>" if stg["mese_piu_economico"] else "n.d."
            render_kpi(edu("Mese più economico", "Il mese con il fattore stagionale più basso: strutturalmente il più economico. Finestra naturale per acquisti spot e consumi flessibili."), econ, s2)
            amp = f"{stg['ampiezza_pp']:.1f} pp" if stg["ampiezza_pp"] is not None else "n.d."
            render_kpi(edu("Ampiezza stagionale", "Differenza in punti tra fattore del mese più caro e più economico: quanto è marcata la stagionalità. Alta ampiezza = budget mensili molto diversi e forward con forte slope stagionale."), amp, s3)
            render_kpi(edu("Media annuale", "Prezzo medio su tutte le ore del periodo: il denominatore del fattore stagionale."), f"{stg['media_annuale']:,.2f} €/MWh", s4)
            st.caption("💡 Il fattore stagionale è 'n.d.' se la media annuale ≤ 0 (prezzi negativi dominanti): in quel caso la stagionalità perde senso come rapporto.")

            fig_stag = go.Figure()
            fig_stag.add_trace(go.Bar(
                x=stg["mensile"]["Mese"], y=stg["mensile"]["Media €/MWh"],
                name="Media €/MWh", marker_color="#3b82f6",
                hovertemplate="Mese: %{x}<br>Media: %{y:,.2f} €/MWh<br>Ore: %{customdata}<extra></extra>",
                customdata=stg["mensile"]["Ore"]))
            fig_stag.add_hline(y=stg["media_annuale"], line_dash="dash", line_color="#94a3b8",
                               annotation_text=f"Media annuale: {stg['media_annuale']:,.2f} €/MWh",
                               annotation_position="top left")
            fig_stag.update_layout(template="plotly_dark", height=360,
                                   title="Prezzo medio mensile (€/MWh)",
                                   xaxis_title="Mese", yaxis_title="Prezzo (€/MWh)")
            st.plotly_chart(fig_stag, use_container_width=True)

            fig_fatt = go.Figure()
            fig_fatt.add_trace(go.Scatter(
                x=stg["mensile"]["Mese"], y=stg["mensile"]["Fattore stagionale"],
                mode="lines+markers", name="Fattore stagionale",
                line=dict(color="#f59e0b", width=2.5),
                hovertemplate="Mese: %{x}<br>Fattore: ×%{y:.3f}<extra></extra>"))
            fig_fatt.add_hline(y=1.0, line_dash="dash", line_color="#94a3b8",
                               annotation_text="Fattore = 1.0 (media annuale)",
                               annotation_position="top left")
            fig_fatt.update_layout(template="plotly_dark", height=360,
                                   title="Fattore stagionale (media mese / media annuale)",
                                   xaxis_title="Mese", yaxis_title="Fattore",
                                   yaxis=dict(range=[0, max(1.3, float(stg["mensile"]["Fattore stagionale"].max()) * 1.1)]))
            st.plotly_chart(fig_fatt, use_container_width=True)

            st.markdown("**Dettaglio mensile**")
            st.dataframe(stg["mensile"], use_container_width=True, hide_index=True)
            st.download_button(
                "⬇️ Esporta stagionalità (CSV)",
                stg["mensile"].to_csv(index=False).encode("utf-8"),
                file_name=f"stagionalita_{d0}_{d1}.csv",
                mime="text/csv",
                help="Scarica il profilo stagionale mensile: media, mediana, min, max, deviazione standard e fattore stagionale.",
            )

    with tab25:
        titolo_bt = edu("Budget tracker", "Il BUDGET TRACKER confronta la spesa energetica effettiva (a prezzi spot, sul tuo profilo di prelievo F1/F2/F3) con il budget annuale stanziato. Il budget pro-rata temporis (budget × giorni trascorsi / 365) dice quanto avresti dovuto spendere 'in linea' col piano; l'indice di consumo (spesa / pro-rata × 100) segnala subito se stai sforando (>100) o sei in anticipo (<100). La proiezione a fine anno (burn rate giornaliero × 365) stima dove atterri se i prezzi restano questi: è la base oggettiva per chiedere un'integrazione di budget o per accelerare le coperture forward.")
        st.markdown(f"**{titolo_bt}**: spesa effettiva vs budget annuale, pro-rata temporis e proiezione a fine anno.", unsafe_allow_html=True)
        st.caption("Profilo di prelievo: quello impostato nel tab 💰 Costo fornitura (MW per fascia F1/F2/F3).")

        bt0, _ = st.columns([1, 2])
        with bt0:
            budget_in = st.number_input("Budget annuale (€)", min_value=0.0, value=1000000.0, step=50000.0,
                                       help="Budget annuale stanziato per l'energia elettrica: il tracker lo confronta con la spesa spot effettiva.")
        bt = calcola_budget_tracker(prezzi, mw_f1, mw_f2, mw_f3, budget_in)
        if budget_in <= 0:
            st.warning("Inserisci un budget annuale positivo per attivare il monitoraggio.")
        elif bt["mensile"].empty:
            st.info("Nessun dato valido nel periodo per il budget tracker.")
        else:
            b1, b2, b3, b4 = st.columns(4)
            render_kpi(edu("Speso nel periodo", "Costo spot effettivo sul periodo analizzato: somma oraria (prezzo × MW della fascia)."), f"{bt['costo_tot']:,.2f} €", b1)
            ind = bt["indice_consumo_pct"]
            ind_txt = f"{bt['budget_prorata']:,.2f} €<br><small>indice {ind:.1f}</small>" if ind is not None else f"{bt['budget_prorata']:,.2f} €"
            render_kpi(edu("Budget pro-rata", "Quota di budget 'dovuta' al tempo trascorso: budget × giorni / 365. L'indice di consumo (spesa / pro-rata × 100) dice se bruci il budget più in fretta (>100) o più piano (<100) del passare del tempo."), ind_txt, b2)
            render_kpi(edu("Proiezione fine anno", "Stima di spesa a fine anno se il burn rate giornaliero resta quello del periodo: spesa / giorni × 365."), f"{bt['proiezione_annua']:,.2f} €", b3)
            sc, scp = bt["scostamento"], bt["scostamento_pct"]
            segno = "🔴" if sc > 0 else ("🟢" if sc < 0 else "⚪")
            render_kpi(edu("Scostamento proiettato", "Proiezione meno budget: quanto sfori (rosso) o risparmi (verde) a fine anno ai prezzi correnti. Base oggettiva per integrazioni di budget o nuove coperture."), f"{segno} {sc:+,.2f} €<br><small>{scp:+.1f}%</small>", b4)
            st.caption("💡 Indice di consumo > 100 = spendi più in fretta del tempo che passa: valuta coperture forward o revisione del budget.")

            fig_bt = go.Figure()
            fig_bt.add_trace(go.Scatter(
                x=bt["cumulata"]["Data"], y=bt["cumulata"]["Costo cumulato €"],
                mode="lines", name="Spesa cumulata",
                line=dict(color="#3b82f6", width=2.5),
                hovertemplate="Data: %{x}<br>Spesa: %{y:,.2f} €<extra></extra>"))
            fig_bt.add_trace(go.Scatter(
                x=bt["cumulata"]["Data"], y=bt["cumulata"]["Budget pro-rata €"],
                mode="lines", name="Budget pro-rata",
                line=dict(color="#94a3b8", width=2, dash="dash"),
                hovertemplate="Data: %{x}<br>Pro-rata: %{y:,.2f} €<extra></extra>"))
            fig_bt.update_layout(template="plotly_dark", height=360,
                                 title="Spesa cumulata vs budget pro-rata (€)",
                                 xaxis_title="Data", yaxis_title="€")
            st.plotly_chart(fig_bt, use_container_width=True)

            fig_btm = go.Figure()
            fig_btm.add_trace(go.Bar(
                x=bt["mensile"]["Mese"], y=bt["mensile"]["Costo €"],
                name="Costo effettivo", marker_color="#3b82f6",
                hovertemplate="Mese: %{x}<br>Costo: %{y:,.2f} €<extra></extra>"))
            fig_btm.add_trace(go.Bar(
                x=bt["mensile"]["Mese"], y=bt["mensile"]["Budget mensile €"],
                name="Budget mensile", marker_color="#94a3b8",
                hovertemplate="Mese: %{x}<br>Budget: %{y:,.2f} €<extra></extra>"))
            fig_btm.update_layout(template="plotly_dark", height=360, barmode="group",
                                  title="Costo mensile vs budget mensile (€)",
                                  xaxis_title="Mese", yaxis_title="€")
            st.plotly_chart(fig_btm, use_container_width=True)

            st.markdown("**Dettaglio mensile**")
            st.dataframe(bt["mensile"], use_container_width=True, hide_index=True)
            st.download_button(
                "⬇️ Esporta budget tracker (CSV)",
                bt["mensile"].to_csv(index=False).encode("utf-8"),
                file_name=f"budget_tracker_{d0}_{d1}.csv",
                mime="text/csv",
                help="Scarica il dettaglio mensile: MWh, costo effettivo, €/MWh medio, budget mensile e scostamento.",
            )

    with tab26:
        titolo_sp = edu("Sensitività profilo", "La SENSITIVITÀ DEL PROFILO misura quanto il costo di fornitura reagisce a variazioni della potenza prelevata in ciascuna fascia F1/F2/F3. Il costo è lineare nei MW, quindi variare la potenza di ±d% in una fascia cambia il costo di ±(costo della fascia × d%): esatto, non stimato. Il COSTO MARGINALE (€ per 1 MW aggiuntivo in fascia) dice dove costa di più aggiungere carico e dove tagliare i prelievi rende di più; la fascia più sensibile è quella dove un ±d% sposta più euro. A differenza del tab Shifting (che simula lo spostamento di energia tra fasce), qui si misura l'impatto di CAMBIARE il profilo: utile per negoziare contratti per fasce, valutare interventi di efficienza e decidere dove concentrare la flessibilità.")
        st.markdown(f"**{titolo_sp}**: di quanto cambia il costo se la potenza in F1/F2/F3 varia di ±d%.", unsafe_allow_html=True)
        st.caption("Profilo di prelievo: quello impostato nel tab 💰 Costo fornitura (MW per fascia F1/F2/F3).")

        sp0, _ = st.columns([1, 2])
        with sp0:
            sp_d = st.slider("Variazione di potenza ±d% per fascia", min_value=1, max_value=50, value=10, step=1, key="sp_d",
                             help="Percentuale di variazione applicata alla potenza di ciascuna fascia, una alla volta.")
        sp = calcola_sensibilita_profilo(prezzi, mw_f1, mw_f2, mw_f3, sp_d)
        if sp["fasce"].empty:
            st.info("Imposta una potenza maggiore di zero in almeno una fascia (tab 💰 Costo fornitura) per l'analisi di sensitività.")
        else:
            s1, s2, s3, s4 = st.columns(4)
            fs_txt = sp["fascia_piu_sensibile"]
            fs = sp["fasce"].loc[sp["fasce"]["Fascia"] == fs_txt].iloc[0]
            render_kpi(edu("Fascia più sensibile", "La fascia dove un ±d% di potenza sposta più euro: è il punto di leva del tuo profilo. Concentra qui interventi di efficienza e flessibilità."), f"{fs_txt}<br><small>±{fs['Δcosto +d% €']:,.2f} €</small>", s1)
            for i, b in enumerate(("F1", "F2", "F3")):
                mg = sp["costo_marginale"][b]
                mg_txt = f"{mg:,.2f} €/MW" if mg is not None else "n.d."
                render_kpi(edu(f"Costo marginale {b}", f"Costo di 1 MW aggiuntivo prelevato in fascia {b} sul periodo: quanto paghi per aggiungere (o risparmi togliendo) 1 MW in questa fascia."), mg_txt, [s2, s3, s4][i])
            st.caption(f"💡 Costo base del periodo: {sp['costo_base']:,.2f} €. Il Δcosto è esatto: costo_fascia × ±{sp['delta_pct']:.0f}% (costo lineare nei MW).")

            fig_sp = go.Figure()
            fig_sp.add_trace(go.Bar(
                x=sp["fasce"]["Δcosto +d% €"], y=sp["fasce"]["Fascia"],
                orientation="h", name=f"+{sp['delta_pct']:.0f}% MW",
                marker_color="#ef4444",
                hovertemplate="Fascia: %{y}<br>Δcosto: +%{x:,.2f} €<extra></extra>"))
            fig_sp.add_trace(go.Bar(
                x=sp["fasce"]["Δcosto -d% €"], y=sp["fasce"]["Fascia"],
                orientation="h", name=f"-{sp['delta_pct']:.0f}% MW",
                marker_color="#22c55e",
                hovertemplate="Fascia: %{y}<br>Δcosto: %{x:,.2f} €<extra></extra>"))
            fig_sp.add_vline(x=0, line_color="#94a3b8", line_width=1)
            fig_sp.update_layout(template="plotly_dark", height=360, barmode="relative",
                                 title=f"Tornado di sensitività: Δcosto con ±{sp['delta_pct']:.0f}% di potenza per fascia (€)",
                                 xaxis_title="Δcosto (€)", yaxis_title="Fascia")
            st.plotly_chart(fig_sp, use_container_width=True)

            st.markdown("**Dettaglio per fascia**")
            st.dataframe(sp["fasce"], use_container_width=True, hide_index=True)
            st.download_button(
                "⬇️ Esporta sensitività profilo (CSV)",
                sp["fasce"].to_csv(index=False).encode("utf-8"),
                file_name=f"sensibilita_profilo_{d0}_{d1}.csv",
                mime="text/csv",
                help="Scarica il dettaglio per fascia: costo, quota %, Δcosto con ±d% e costo marginale €/MW.",
            )

    with tab27:
        titolo_vc = edu("VaR del costo di fornitura (Monte Carlo)", "Il VaR del COSTO (Value-at-Risk) stima il rischio di budget su un periodo futuro di pari durata: simula 1.000+ scenari di prezzo ricampionando giornate intere (24h) dai prezzi osservati, preservando il profilo giornaliero tipico, e calcola in ciascuno il costo del tuo profilo F1/F2/F3. Il P95 è il VaR: nel 95% degli scenari il costo resta SOTTO quel livello. A differenza del tab Rischio & Durata (VaR STORICO sul prezzo orario), qui il rischio è PROSPETTICO sul costo totale: quello che finisce davvero in bolletta. Con il seed fisso i risultati sono deterministici e riproducibili.")
        st.markdown(f"**{titolo_vc}**: quanto può costare il periodo futuro? Simula 1.000+ scenari di prezzo e trova la soglia di budget a rischio.", unsafe_allow_html=True)
        st.caption("Profilo di prelievo: quello impostato nel tab 💰 Costo fornitura (MW per fascia F1/F2/F3).")

        vc0, vc1 = st.columns([1, 1])
        with vc0:
            vc_n = st.slider("Scenari simulati", min_value=100, max_value=5000, value=1000, step=100, key="vc_n",
                             help="Numero di scenari Monte Carlo. 1.000 è il default; 5.000 dà percentili più stabili ma è più lento.")
        spot_tmp = calcola_var_costo(prezzi, mw_f1, mw_f2, mw_f3, n_scenari=100, seed=42)
        soglia_def = (spot_tmp["costo_spot"] * 1.2) if spot_tmp["costo_spot"] else 1000.0
        with vc1:
            vc_soglia = st.number_input("Soglia di allarme costo (€)", min_value=0.0, value=round(soglia_def, 2), step=100.0, key="vc_soglia",
                                        help="Budget di allarme: calcola la probabilità che il costo simulato lo superi. Default = 120% del costo spot del periodo.")
        vc = calcola_var_costo(prezzi, mw_f1, mw_f2, mw_f3, n_scenari=vc_n,
                               soglia_euro=vc_soglia, seed=42)
        if vc["costo_atteso"] is None:
            st.info("Imposta una potenza maggiore di zero in almeno una fascia (tab 💰 Costo fornitura) per la simulazione Monte Carlo.")
        else:
            v1, v2, v3, v4 = st.columns(4)
            render_kpi(edu("Costo atteso (media scenari)", "Media del costo del profilo su tutti gli scenari simulati: la stima centrale di quanto costerà il periodo futuro."), f"{vc['costo_atteso']:,.2f} €", v1)
            render_kpi(edu("P95 = VaR del costo", "Nel 95% degli scenari simulati il costo resta SOTTO questo livello: la soglia di budget a rischio (Value-at-Risk)."), f"{vc['p95']:,.2f} €", v2)
            render_kpi(edu("P99 (stress)", "Scenario estremo: solo l'1% degli scenari simulati costa di più. Utile per stress test di budget."), f"{vc['p99']:,.2f} €", v3)
            render_kpi(edu("Probabilità di sforamento", "Quota di scenari simulati in cui il costo supera la soglia di allarme impostata sopra."), f"{vc['prob_sforamento_pct']:.1f} %", v4)
            st.caption(f"💡 {vc['n_scenari']:,} scenari su {vc['ore']} ore ({vc['mwh']:,.0f} MWh). Costo spot del periodo osservato: {vc['costo_spot']:,.2f} €. Simulazione deterministica (seed 42): rieseguendola ottieni gli stessi numeri.")

            fig_vc = go.Figure()
            fig_vc.add_trace(go.Histogram(x=vc["scenari"], nbinsx=60, name="Scenari",
                                          marker_color="#3b82f6",
                                          hovertemplate="Costo: %{x:,.2f} €<br>Scenari: %{y}<extra></extra>"))
            fig_vc.add_vline(x=vc["costo_atteso"], line_color="#ffffff", line_width=2, line_dash="dash",
                             annotation_text="Atteso", annotation_position="top")
            fig_vc.add_vline(x=vc["p95"], line_color="#ef4444", line_width=2,
                             annotation_text="P95 (VaR)", annotation_position="top")
            fig_vc.add_vline(x=vc["soglia"], line_color="#f59e0b", line_width=2, line_dash="dot",
                             annotation_text="Soglia", annotation_position="top")
            fig_vc.update_layout(template="plotly_dark", height=380,
                                 title="Distribuzione del costo di fornitura simulato (€)",
                                 xaxis_title="Costo per scenario (€)", yaxis_title="N. scenari")
            st.plotly_chart(fig_vc, use_container_width=True)

            st.markdown("**Percentili del costo simulato**")
            st.dataframe(vc["percentili"], use_container_width=True, hide_index=True)
            st.download_button(
                "⬇️ Esporta percentili VaR costo (CSV)",
                vc["percentili"].to_csv(index=False).encode("utf-8"),
                file_name=f"var_costo_{d0}_{d1}.csv",
                mime="text/csv",
                help="Scarica i percentili P50/P75/P90/P95/P99 del costo di fornitura simulato.",
            )

    with tab28:
        titolo_tg = edu("Top giorni di costo", "La classifica dei GIORNI di calendario più costosi per il tuo profilo di prelievo F1/F2/F3: ogni giorno aggrega il costo orario (prezzo spot × MW della fascia). A differenza del tab Picchi (ore di prezzo estremo) e di Concentrazione costo (curva di Lorenz sulle ore), qui la granularità è il giorno: 'quanto mi è costato il 15/09?' è la domanda operativa per tesoreria, budget e verifica delle fatture del fornitore. La heatmap-calendario mostra a colpo d'occhio i giorni critici; la fascia dominante dice dove è nato il costo in ciascun giorno.")
        st.markdown(f"**{titolo_tg}**: quali giorni hanno pesato di più sulla bolletta del periodo?", unsafe_allow_html=True)
        st.caption("Profilo di prelievo: quello impostato nel tab 💰 Costo fornitura (MW per fascia F1/F2/F3).")

        tg_topn = st.slider("Giorni in classifica", min_value=3, max_value=31, value=10, key="tg_topn",
                            help="Quanti giorni mostrare nella classifica dei più costosi (barre orizzontali).")
        tg = calcola_top_giorni_costo(prezzi, mw_f1, mw_f2, mw_f3, top_n=tg_topn)
        if tg["costo_tot"] is None:
            st.info("Imposta una potenza maggiore di zero in almeno una fascia (tab 💰 Costo fornitura) per calcolare il costo giornaliero.")
        else:
            t1, t2, t3, t4 = st.columns(4)
            render_kpi(edu("Giorno più costoso", "Il giorno di calendario con il costo più alto per il tuo profilo nel periodo selezionato."), f"{tg['giorno_max_data']}", t1)
            render_kpi(edu("Costo del giorno peggiore", "Quanto è costato il giorno peggiore: il picco di esposizione giornaliera del periodo."), f"{tg['giorno_max_costo']:,.2f} €", t2)
            render_kpi(edu("Costo medio giornaliero", "Costo medio per giorno di calendario nel periodo: il riferimento per giudicare se un giorno è stato 'caro'."), f"{tg['costo_medio_gg']:,.2f} €", t3)
            q10_txt = f"{tg['quota_top10pct']:.1f} %" if tg["quota_top10pct"] is not None else "n.d."
            render_kpi(edu("Quota nel 10% di giorni peggiori", "Percentuale del costo totale generata dal 10% di giorni più costosi: misura la concentrazione temporale della spesa."), q10_txt, t4)
            rapp_txt = f"Il giorno peggiore costa {tg['rapporto_max_medio']:.1f}× la media giornaliera." if tg["rapporto_max_medio"] is not None else ""
            st.caption(f"💡 {tg['n_giorni']} giorni, {tg['mwh_tot']:,.0f} MWh, costo totale {tg['costo_tot']:,.2f} €. {rapp_txt}")

            top_df = tg["top"]
            fig_tg = go.Figure()
            fig_tg.add_trace(go.Bar(
                x=top_df["Costo €"],
                y=top_df["Data"] + " (" + top_df["Giorno"] + ")",
                orientation="h", marker_color="#f59e0b",
                hovertemplate="%{y}<br>Costo: %{x:,.2f} €<extra></extra>"))
            fig_tg.update_layout(template="plotly_dark", height=max(300, 42 * len(top_df)),
                                 title=f"Top {tg['top_n']} giorni più costosi (€)",
                                 xaxis_title="Costo giornaliero (€)",
                                 yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig_tg, use_container_width=True)

            cal = tg["calendario"]
            if len(cal):
                fig_cal = go.Figure(data=go.Heatmap(
                    z=cal.values, x=list(cal.columns), y=list(cal.index),
                    colorscale="YlOrRd",
                    hovertemplate="%{y} · %{x}<br>Costo: %{z:,.2f} €<extra></extra>",
                    colorbar=dict(title="€/giorno")))
                fig_cal.update_layout(template="plotly_dark", height=max(240, 36 * len(cal)),
                                      title="Calendario del costo giornaliero (€)")
                st.plotly_chart(fig_cal, use_container_width=True)

            st.markdown("**Classifica giorni per costo**")
            classifica = tg["giorni"].sort_values("Costo €", ascending=False).reset_index(drop=True)
            st.dataframe(classifica, use_container_width=True, hide_index=True)
            st.download_button(
                "⬇️ Esporta costo giornaliero (CSV)",
                classifica.to_csv(index=False).encode("utf-8"),
                file_name=f"top_giorni_costo_{d0}_{d1}.csv",
                mime="text/csv",
                help="Scarica la serie giornaliera ordinata per costo: data, giorno della settimana, MWh, costo, prezzo medio e fascia dominante.",
            )

    with tab29:
        titolo_fo = edu("Fasce tariffarie ottimali", "Le fasce F1/F2/F3 sono fissate dal regolamento e Base/Peak/Offpeak dal mercato: qui le fasce nascono DAI DATI. Un k-means 1-D deterministico (nessun caso, risultati riproducibili) raggruppa le 24 ore in N fasce che minimizzano la dispersione di prezzo dentro ogni fascia, usando il profilo orario medio del periodo selezionato. Serve a disegnare una tariffa time-of-use su misura, a quotare contratti con fasce personalizzate e a decidere in quali ore conviene concentrare i carichi flessibili: la VARIANZA SPIEGATA dice quanta della variabilità oraria le fasce catturano (più alta = fasce più rappresentative).")
        st.markdown(f"**{titolo_fo}**: raggruppa le 24 ore in N fasce omogenee per prezzo, derivate dal profilo osservato.", unsafe_allow_html=True)

        fo_nb = st.slider("Numero di fasce", min_value=2, max_value=5, value=3, key="fo_nb",
                          help="In quante fasce dividere le 24 ore. 3 è il default (analogo alle F1/F2/F3 ma con orari ottimizzati dai dati).")
        fo = calcola_fasce_ottimali(prezzi, n_bande=fo_nb)
        if fo["n_bande"] == 0:
            st.info("Nessun dato di prezzo nel periodo selezionato: impossibile calcolare le fasce ottimali.")
        else:
            f1, f2, f3, f4 = st.columns(4)
            sp_txt = f"{fo['spread_bande']:,.2f} €/MWh" if fo["spread_bande"] is not None else "n.d."
            render_kpi(edu("Spread fascia cara − economica", "Differenza tra il prezzo medio della fascia più cara e quella più economica: l'incentivo massimo a spostare i consumi nelle ore della fascia B1."), sp_txt, f1)
            vs_txt = f"{fo['varianza_spiegata_pct']:.1f} %" if fo["varianza_spiegata_pct"] is not None else "n.d."
            render_kpi(edu("Varianza oraria spiegata", "Quota della variabilità del profilo orario catturata dalle fasce (1 − dispersione interna / dispersione totale). Più è alta, più le fasce rappresentano bene il prezzo."), vs_txt, f2)
            sw_txt = f"{fo['std_within_media']:,.2f} €/MWh" if fo["std_within_media"] is not None else "n.d."
            render_kpi(edu("Dispersione dentro le fasce", "Deviazione standard media del prezzo dentro le fasce: misura l'omogeneità. Più è bassa, più ogni fascia ha un prezzo 'piatto'."), sw_txt, f3)
            b1 = fo["bande"].iloc[0]
            render_kpi(edu("Fascia più economica", "La fascia con il prezzo medio più basso: le ore in cui conviene concentrare i carichi flessibili."), f"{b1['Banda']}<br><small>{b1['Prezzo medio €/MWh']:,.2f} €/MWh · {b1['N. ore']} ore</small>", f4)
            if fo["n_bande"] < fo_nb:
                st.caption(f"⚠️ Solo {fo['n_bande']} fasce effettive: il profilo ha meno valori distinti del numero di fasce richiesto.")

            colori = ["#22c55e", "#eab308", "#f97316", "#ef4444", "#a855f7"]
            prof = fo["profilo"]
            fig_fo = go.Figure()
            for j, b in enumerate(fo["bande"]["Banda"]):
                ore_b = prof.loc[prof["Banda"] == b]
                fig_fo.add_trace(go.Bar(
                    x=ore_b["Ora"], y=ore_b["Prezzo medio €/MWh"], name=b,
                    marker_color=colori[j % len(colori)],
                    hovertemplate="Ora: %{x}:00<br>Prezzo medio: %{y:,.2f} €/MWh<br>Fascia: " + b + "<extra></extra>"))
            fig_fo.update_layout(template="plotly_dark", height=380, barmode="group",
                                 title=f"Profilo orario medio per fascia ottimale ({fo['n_ore']} ore con dati)",
                                 xaxis_title="Ora", yaxis_title="Prezzo medio (€/MWh)",
                                 xaxis=dict(tickmode="linear", dtick=1))
            st.plotly_chart(fig_fo, use_container_width=True)

            st.markdown("**Dettaglio fasce**")
            st.dataframe(fo["bande"], use_container_width=True, hide_index=True)
            st.download_button(
                "⬇️ Esporta fasce ottimali (CSV)",
                fo["bande"].to_csv(index=False).encode("utf-8"),
                file_name=f"fasce_ottimali_{d0}_{d1}.csv",
                mime="text/csv",
                help="Scarica le fasce: ore assegnate, prezzo medio e scostamento dalla media oraria.",
            )

    with tab30:
        titolo_acf = edu("Autocorrelazione dei prezzi", "Quanto il prezzo di un'ora 'ricorda' quello delle ore precedenti. ACF(1) vicina a 1 = prezzo appiccicoso: gli shock rientrano lentamente (mean-reversion lenta, i livelli di prezzo persistono). Picchi a lag 24 e 168 = stagionalità giornaliera e settimanale: il prezzo segue un ritmo prevedibile. ACF che decade subito sotto la banda tratteggiata = mercato imprevedibile ora per ora. Le barre sopra/sotto la banda sono statisticamente significative al 95 % (banda = ±1.96/√n). Utile per decidere l'orizzonte delle previsioni: se la memoria è lunga, i modelli di breve funzionano; se è corta, meglio strategie meno direzionali.")
        st.markdown(f"**{titolo_acf}**: persistenza degli shock di prezzo e firma della stagionalità, dai lag 1h fino a 2 settimane.", unsafe_allow_html=True)

        acf_maxl = st.slider("Lag massimo (ore)", min_value=24, max_value=336, value=168, step=24, key="acf_maxl",
                            help="Fino a quante ore indietro guardare. 168 = una settimana (cattura la stagionalità settimanale), 336 = due settimane.")
        acf_r = calcola_autocorrelazione(prezzi, max_lag=acf_maxl)
        if acf_r["n"] < 3:
            st.info("Dati insufficienti per calcolare l'autocorrelazione: servono almeno 3 prezzi orari validi nel periodo selezionato.")
        else:
            a1, a2, a3, a4 = st.columns(4)
            v1 = f"{acf_r['acf_lag1']:+.3f}" if acf_r["acf_lag1"] is not None else "n.d."
            render_kpi(edu("Persistenza a 1h", "Autocorrelazione al lag di 1 ora: quanto il prezzo dell'ora t+1 assomiglia a quello dell'ora t. Vicina a +1 = prezzo appiccicoso, vicino a 0 = ogni ora è una storia a sé."), v1, a1)
            v2 = f"{acf_r['acf_lag24']:+.3f}" if acf_r["acf_lag24"] is not None else "n.d."
            render_kpi(edu("Stagionalità 24h", "Autocorrelazione al lag di 24 ore: misura la regolarità giornaliera. Alta = la stessa ora del giorno costa sistematicamente simile (profilo giorno/notte stabile)."), v2, a2)
            v3 = f"{acf_r['acf_lag168']:+.3f}" if acf_r["acf_lag168"] is not None else "n.d."
            render_kpi(edu("Stagionalità 168h", "Autocorrelazione al lag di 168 ore (una settimana): misura il ritmo settimanale. Alta = la stessa ora dello stesso giorno della settimana si ripete (es. weekend sempre più economico)."), v3, a3)
            if acf_r["lag_decay"] is None:
                v4 = f"> {acf_r['max_lag']} h"
                t4 = "La correlazione resta significativa oltre il lag massimo: la memoria del mercato supera l'orizzonte osservato."
            else:
                v4 = f"{acf_r['lag_decay']} h"
                t4 = "Primo lag in cui l'autocorrelazione scende sotto la banda di significatività del 95 %: dopo queste ore il prezzo 'dimentica' il passato."
            render_kpi(edu("Memoria del mercato", t4), v4, a4)

            df_acf = acf_r["df"]
            fig_acf = go.Figure()
            colori_sig = ["#22c55e" if s == "Sì" else "#6b7280" for s in df_acf["Significativo 95%"]]
            fig_acf.add_trace(go.Bar(
                x=df_acf["Lag (ore)"], y=df_acf["ACF"], name="ACF",
                marker_color=colori_sig,
                hovertemplate="Lag: %{x} h<br>ACF: %{y:.4f}<extra></extra>"))
            fig_acf.add_trace(go.Scatter(
                x=df_acf["Lag (ore)"], y=df_acf["Banda 95%"], name="Banda +95%",
                mode="lines", line=dict(color="#f87171", dash="dash", width=1)))
            fig_acf.add_trace(go.Scatter(
                x=df_acf["Lag (ore)"], y=-df_acf["Banda 95%"], name="Banda −95%",
                mode="lines", line=dict(color="#f87171", dash="dash", width=1)))
            for lag_ref, nome in [(24, "24h"), (168, "168h")]:
                if lag_ref <= acf_r["max_lag"]:
                    fig_acf.add_vline(x=lag_ref, line_dash="dot", line_color="#60a5fa",
                                      annotation_text=nome, annotation_position="top right")
            fig_acf.update_layout(template="plotly_dark", height=420,
                                  title=f"Autocorrelazione del prezzo spot (n = {acf_r['n']:,} ore valide)",
                                  xaxis_title="Lag (ore)", yaxis_title="ACF",
                                  xaxis=dict(tickmode="linear", dtick=24))
            st.plotly_chart(fig_acf, use_container_width=True)
            st.caption("Verde = autocorrelazione significativa al 95 %; grigia = rumore. Le linee verticali tratteggiate blu marcano i lag giornaliero (24h) e settimanale (168h).")

            st.markdown("**Tabella autocorrelazione**")
            st.dataframe(df_acf, use_container_width=True, hide_index=True)
            st.download_button(
                "⬇️ Esporta autocorrelazione (CSV)",
                df_acf.to_csv(index=False).encode("utf-8"),
                file_name=f"autocorrelazione_{d0}_{d1}.csv",
                mime="text/csv",
                help="Scarica lag, ACF, banda di significatività 95 % e flag di significatività.",
            )

    with tab31:
        titolo_st = edu("Stress test del costo di fornitura", "What-if deterministico: cosa succede al costo della tua fornitura se i prezzi di mercato schizzano o crollano? A differenza del VaR (tab27), che è probabilistico ('con il 95 % di probabilità il costo resta sotto X'), qui applichi shock precisi e vedi l'impatto esatto: +30 % sui prezzi, +25 €/MWh sulle sole ore di picco F1, ecc. È lo strumento per dimensionare il budget di rischio e per decidere quanto conviene fissare il prezzo con un contratto forward: se lo shock peggiore fa saltare il budget, la copertura vale la pena.")
        st.markdown(f"**{titolo_st}**: applica shock di prezzo deterministici alla serie oraria e ricalcola il costo della fornitura sul tuo profilo di prelievo.", unsafe_allow_html=True)

        s1, s2, s3 = st.columns(3)
        with s1:
            st_mw_f1 = st.number_input("Prelievo in F1 (MW)", min_value=0.0, value=1.0, step=0.5, key="st_mw_f1",
                                       help="Ore di punta: lun–ven 08:00–19:00.")
        with s2:
            st_mw_f2 = st.number_input("Prelievo in F2 (MW)", min_value=0.0, value=1.0, step=0.5, key="st_mw_f2",
                                       help="Ore intermedie: lun–ven 07:00–08:00 e 19:00–23:00, sab 07:00–23:00.")
        with s3:
            st_mw_f3 = st.number_input("Prelievo in F3 (MW)", min_value=0.0, value=1.0, step=0.5, key="st_mw_f3",
                                       help="Ore fuori punta: notti, domeniche e festivi.")

        st.markdown("**Scala di scenari**")
        st_preset = st.radio("Scenario", ["Percentuale su tutte le ore", "Additivo €/MWh su tutte le ore",
                                          "Additivo €/MWh solo su F1 (picco)", "Personalizzato"],
                             horizontal=True, key="st_preset",
                             help="Le scale preset applicano una serie di shock a gradini; 'Personalizzato' costruisce la scala attorno al tuo shock.")
        if st_preset == "Personalizzato":
            t1, t2, t3 = st.columns(3)
            with t1:
                c_tipo = st.radio("Tipo di shock", ["Percentuale (%)", "Additivo (€/MWh)"], horizontal=True, key="st_ctipo",
                                  help="Percentuale: scala il prezzo (×1.3 = +30 %). Additivo: sposta il prezzo di un importo fisso.")
            with t2:
                c_amb = st.radio("Ore colpite", ["Tutte", "Solo F1", "Solo F2", "Solo F3"], horizontal=True, key="st_camb",
                                 help="Applica lo shock a tutte le ore o solo alle ore di una fascia (es. solo il picco F1).")
            with t3:
                if c_tipo == "Percentuale (%)":
                    c_mag = st.slider("Shock massimo", min_value=-50, max_value=200, value=50, step=5, key="st_cmag_pct",
                                      help="La scala verrà costruita a gradini tra −shock e +shock (5 punti + base).")
                else:
                    c_mag = st.slider("Shock massimo", min_value=-50, max_value=150, value=30, step=5, key="st_cmag_add",
                                      help="La scala verrà costruita a gradini tra −shock e +shock (5 punti + base).")

        if st_preset == "Percentuale su tutte le ore":
            scenari = [{"nome": f"{v:+.0f} %", "tipo": "pct", "valore": v, "solo_fascia": None}
                       for v in (-30, -15, 0, 15, 30, 60)]
        elif st_preset == "Additivo €/MWh su tutte le ore":
            scenari = [{"nome": f"{v:+.0f} €/MWh", "tipo": "add", "valore": v, "solo_fascia": None}
                       for v in (-20, -10, 0, 10, 25, 50)]
        elif st_preset == "Additivo €/MWh solo su F1 (picco)":
            scenari = [{"nome": f"{v:+.0f} €/MWh su F1", "tipo": "add", "valore": v, "solo_fascia": "F1"}
                       for v in (0, 10, 20, 30, 50)]
        else:
            t = "pct" if c_tipo == "Percentuale (%)" else "add"
            unit = " %" if t == "pct" else " €/MWh"
            solo = None if c_amb == "Tutte" else c_amb.replace("Solo ", "")
            mags = sorted(set([-c_mag, -c_mag / 2, 0, c_mag / 2, c_mag]))
            scenari = [{"nome": (f"{v:+g}{unit}" + (f" su {solo}" if solo else "")), "tipo": t,
                        "valore": v, "solo_fascia": solo} for v in mags]

        st_r = calcola_stress_prezzo(prezzi, st_mw_f1, st_mw_f2, st_mw_f3, scenari)
        base_r = st_r["base"]
        if base_r is None or base_r["mwh"] == 0:
            st.warning("Imposta una potenza maggiore di zero in almeno una fascia per calcolare lo stress test.")
        else:
            df_st = st_r["df"]
            c1, c2, c3, c4 = st.columns(4)
            render_kpi(edu("Costo base periodo", "Costo della fornitura ai prezzi osservati, senza shock: il punto di riferimento da cui si misurano tutti gli scenari."), f"{base_r['totale']:,.0f} €", c1)
            if st_r["worst_nome"] is None:
                render_kpi("Scenario peggiore", "n.d.", c2)
                render_kpi("Delta max (€)", "n.d.", c3)
                render_kpi("Delta max (%)", "n.d.", c4)
            else:
                render_kpi(edu("Scenario peggiore", "Lo scenario con l'aumento di costo percentuale più alto: è il caso da tenere d'occhio per il budget di rischio."), st_r["worst_nome"], c2)
                segno = "🔴" if st_r["worst_delta_eur"] > 0 else "🟢"
                render_kpi(f"{segno} Delta max (€)", f"{st_r['worst_delta_eur']:+,.0f} €", c3)
                render_kpi("Delta max (%)", f"{st_r['worst_delta_pct']:+.1f} %", c4)

            ord_st = df_st.sort_values("Delta (%)" if df_st["Delta (%)"].notna().any() else "Delta (€)").reset_index(drop=True)
            colori = ["#22c55e" if d < 0 else ("#ef4444" if d > 0 else "#6b7280") for d in ord_st["Delta (€)"]]
            fig_st = go.Figure()
            fig_st.add_trace(go.Bar(
                x=ord_st["Costo (€)"], y=ord_st["Scenario"], orientation="h", name="Costo scenario (€)",
                marker_color=colori,
                hovertemplate="Scenario: %{y}<br>Costo: %{x:,.0f} €<extra></extra>"))
            fig_st.add_vline(x=base_r["totale"], line_dash="dash", line_color="#fbbf24",
                             annotation_text="Base (no shock)", annotation_position="top right")
            fig_st.update_layout(template="plotly_dark", height=max(320, 60 * len(ord_st) + 80),
                                 title="Costo della fornitura per scenario di shock",
                                 xaxis_title="Costo (€)", yaxis_title="Scenario")
            st.plotly_chart(fig_st, use_container_width=True)
            st.caption("La linea gialla tratteggiata è il costo base senza shock. Verde = lo shock riduce il costo, rosso = lo aumenta.")

            st.markdown("**Tabella scenari**")
            st.dataframe(df_st, use_container_width=True, hide_index=True)
            st.download_button(
                "⬇️ Esporta stress test (CSV)",
                df_st.to_csv(index=False).encode("utf-8"),
                file_name=f"stress_test_{d0}_{d1}.csv",
                mime="text/csv",
                help="Scarica scenario, shock applicato, costo, delta in € e % e prezzo medio ponderato.",
            )

    with tab32:
        titolo_fc = edu("Forecast del prezzo del giorno successivo", "Previsione naive-stagionale: per ogni ora del giorno dopo l'ultimo giorno con dati completi, il prezzo previsto è la media storica di quell'ora nello stesso giorno della settimana (ultime 8 settimane di default). Cattura profilo giornaliero e stagionalità settimanale senza parametri da stimare. Il backtest walk-forward misura quanto questo metodo avrebbe sbagliato nelle ultime settimane usando solo i dati disponibili allora: MAE (errore medio assoluto), RMSE (penalizza gli errori grandi) e bias = media(previsione − reale), positivo = il metodo tende a sovrastimare. Se il bias è sistematico, la previsione va corretta di conseguenza prima di usarla per il budget.")
        st.markdown(f"**{titolo_fc}**: previsione oraria del prezzo per il giorno dopo l'ultimo con dati completi, con misura dell'accuratezza storica (backtest).", unsafe_allow_html=True)

        fc1, fc2 = st.columns(2)
        with fc1:
            fc_nw = st.slider("Settimane di storia per la media stagionale", min_value=1, max_value=26, value=8, key="fc_nw",
                              help="Quante settimane indietro guardare per la media di ogni (ora, giorno della settimana). Più settimane = stima più stabile, meno reattiva ai cambi di regime.")
        with fc2:
            fc_bt = st.slider("Settimane di backtest", min_value=0, max_value=12, value=4, key="fc_bt",
                              help="Su quante settimane indietro misurare l'accuratezza del metodo (walk-forward). 0 = nessun backtest.")

        fc = calcola_forecast_prezzo(prezzi, n_settimane=fc_nw, backtest_settimane=fc_bt)
        if fc["data_target"] is None:
            st.warning("Dati insufficienti per il forecast: serve almeno un giorno con dati orari.")
        else:
            df_fc = fc["df_forecast"]
            tgt = fc["data_target"]
            k1, k2, k3, k4 = st.columns(4)
            render_kpi(edu("Giorno previsto", "Il giorno dopo l'ultimo giorno con dati completi: la previsione copre le sue 24 ore."), tgt.strftime("%d/%m/%Y"), k1)
            render_kpi(edu("Prezzo medio previsto", "Media delle 24 previsioni orarie: il livello atteso del prezzo per il giorno previsto."), f"{df_fc['Previsione (€/MWh)'].mean():,.2f} €/MWh", k2)
            render_kpi(edu("MAE backtest", "Errore medio assoluto del metodo sulle settimane di backtest: di quanto, in media, la previsione si discosta dal prezzo reale."), (f"{fc['mae']:,.2f} €/MWh" if fc["mae"] is not None else "n.d."), k3)
            if fc["bias"] is None:
                render_kpi("Bias backtest", "n.d.", k4)
            else:
                segno = "🔴" if fc["bias"] > 0 else ("🟢" if fc["bias"] < 0 else "⚪")
                render_kpi(f"{segno} Bias backtest", f"{fc['bias']:+,.2f} €/MWh", k4)

            fig_fc = go.Figure()
            fig_fc.add_trace(go.Scatter(
                x=df_fc["Ora"], y=df_fc["Max campione (€/MWh)"], mode="lines",
                line=dict(width=0), showlegend=False, hoverinfo="skip"))
            fig_fc.add_trace(go.Scatter(
                x=df_fc["Ora"], y=df_fc["Min campione (€/MWh)"], mode="lines",
                line=dict(width=0), fill="tonexty", fillcolor="rgba(59,130,246,0.18)",
                name="Banda min–max campione",
                hovertemplate="Ora: %{x}<br>Min campione: %{y:.2f} €/MWh<extra></extra>"))
            fig_fc.add_trace(go.Scatter(
                x=df_fc["Ora"], y=df_fc["Previsione (€/MWh)"], mode="lines+markers",
                name="Previsione", line=dict(color="#3b82f6", width=2),
                hovertemplate="Ora: %{x}<br>Previsione: %{y:.2f} €/MWh<extra></extra>"))
            fig_fc.update_layout(template="plotly_dark", height=380,
                                 title=f"Previsione oraria — {tgt.strftime('%d/%m/%Y')}",
                                 xaxis_title="Ora", yaxis_title="€/MWh")
            st.plotly_chart(fig_fc, use_container_width=True)
            st.caption("La banda blu è l'intervallo min–max del campione storico usato per ciascuna ora: più è larga, meno la previsione è affidabile per quell'ora.")

            st.markdown("**Tabella previsione oraria**")
            st.dataframe(df_fc, use_container_width=True, hide_index=True)
            st.download_button(
                "⬇️ Esporta forecast (CSV)",
                df_fc.to_csv(index=False).encode("utf-8"),
                file_name=f"forecast_prezzo_{tgt.strftime('%Y%m%d')}.csv",
                mime="text/csv",
                help="Scarica ora, fascia, previsione, banda min–max del campione e numerosità per le 24 ore previste.",
            )

            if len(fc["df_backtest"]) > 0:
                st.markdown("**Backtest walk-forward**")
                st.dataframe(fc["df_backtest"], use_container_width=True, hide_index=True)
                if fc["rmse"] is not None:
                    st.caption(f"RMSE medio backtest: {fc['rmse']:,.2f} €/MWh. Un MAE molto inferiore alla volatilità oraria del periodo indica un metodo utile; un bias sistematico va sottratto dalla previsione prima dell'uso.")

    with tab33:
        titolo_ra = edu("Rampa massima ora-su-ora", "La 'rampa' è la variazione del prezzo tra due ore consecutive: misura quanto in fretta il mercato può muoversi. Un analista la usa per: (1) dimensionare le flessibilità intraday — se sposti un consumo di un'ora, quanto puoi guadagnare o perdere? (2) tarare gli alert di prezzo; (3) capire il rischio di un profilo di prelievo concentrato in poche ore. Le coppie con buchi > 2 ore nei dati (e i cambi DST) sono escluse, così un buco non viene scambiato per una rampa estrema.")
        st.markdown(f"**{titolo_ra}**: le variazioni più brusche del prezzo tra un'ora e la successiva nel periodo selezionato.", unsafe_allow_html=True)

        r1, r2 = st.columns(2)
        with r1:
            ra_soglia = st.slider("Soglia evento (€/MWh)", min_value=1.0, max_value=50.0, value=10.0, step=1.0, key="ra_soglia",
                                  help="Solo le variazioni con |delta| sopra questa soglia compaiono nella tabella eventi e nel conteggio.")
        with r2:
            ra_n = st.slider("N. eventi in tabella", min_value=5, max_value=50, value=15, key="ra_n",
                             help="Quante delle rampe più estreme (per |delta|) mostrare in tabella e grafico.")

        ra = calcola_rampe_prezzo(prezzi, soglia=ra_soglia, top_n=ra_n)
        if ra["rampa_max_up"] is None:
            st.warning("Dati insufficienti: servono almeno due ore consecutive con dati per calcolare le rampe.")
        else:
            df_ra = ra["df_eventi"]
            c1, c2, c3, c4 = st.columns(4)
            render_kpi(edu("Rampa max al rialzo", "Il salto positivo più grande tra due ore consecutive: il prezzo è salito di questo importo in un'ora sola."), f"+{ra['rampa_max_up']:,.2f} €/MWh", c1)
            render_kpi(edu("Rampa max al ribasso", "Il crollo più grande tra due ore consecutive: il prezzo è sceso di questo importo in un'ora sola."), f"{ra['rampa_max_down']:,.2f} €/MWh", c2)
            render_kpi(edu("Rampa media |Δ|", "Variazione assoluta media tra ore consecutive: il 'rumore di fondo' del mercato ora-su-ora."), f"{ra['media_abs']:,.2f} €/MWh", c3)
            render_kpi(edu("Eventi oltre soglia", "Quante rampe superano la soglia impostata, divise tra rialzi e ribassi."), f"{ra['n_up']} ▲ / {ra['n_down']} ▼", c4)

            if len(df_ra) > 0:
                ord_ra = df_ra.sort_values("Delta (€/MWh)").reset_index(drop=True)
                colori_ra = ["#ef4444" if d > 0 else "#22c55e" for d in ord_ra["Delta (€/MWh)"]]
                fig_ra = go.Figure()
                fig_ra.add_trace(go.Bar(
                    x=ord_ra["Delta (€/MWh)"], y=ord_ra["Data e ora"], orientation="h",
                    name="Rampa (€/MWh)", marker_color=colori_ra,
                    hovertemplate="Data e ora: %{y}<br>Delta: %{x:+.2f} €/MWh<extra></extra>"))
                fig_ra.update_layout(template="plotly_dark", height=max(320, 60 * len(ord_ra) + 80),
                                     title="Rampe più estreme nel periodo",
                                     xaxis_title="Variazione (€/MWh, + = rialzo, − = ribasso)",
                                     yaxis_title="Data e ora")
                st.plotly_chart(fig_ra, use_container_width=True)
                st.caption("Rosso = rialzo improvviso (prezzo salito in un'ora), verde = crollo improvviso.")

                st.markdown("**Tabella eventi**")
                st.dataframe(df_ra, use_container_width=True, hide_index=True)
                st.download_button(
                    "⬇️ Esporta rampe (CSV)",
                    df_ra.to_csv(index=False).encode("utf-8"),
                    file_name=f"rampe_prezzo_{d0}_{d1}.csv",
                    mime="text/csv",
                    help="Scarica data e ora, delta in €/MWh, direzione e prezzi prima/dopo per ogni evento oltre soglia.",
                )
            else:
                st.info("Nessuna rampa oltre la soglia nel periodo: abbassa la soglia per vederle.")

    with tab34:
        titolo_ps = edu("Persistenza sopra soglia", "Per chi gestisce un impianto dispacciabile (o una flessibilità) conta sapere non solo quanto spesso il prezzo supera il costo variabile, ma per quante ore consecutive resta sopra: un blocco di 6 ore giustifica un avviamento, sei ore isolate no. La soglia è il tuo costo variabile (o strike): ogni 'blocco' è una sequenza di ore osservate e consecutive con prezzo ≥ soglia. Buchi nei dati e ore con prezzo mancante interrompono i blocchi; i cambi DST no, perché sono ore di mercato consecutive.")
        st.markdown(f"**{titolo_ps}**: blocchi di ore consecutive con prezzo sopra la soglia nel periodo selezionato.", unsafe_allow_html=True)

        try:
            _pv = prezzi.values.astype(float)
            ps_max = float(np.nanmax(_pv))
            ps_med = float(np.nanmedian(_pv))
            if not np.isfinite(ps_max) or not np.isfinite(ps_med):
                raise ValueError("prezzi non validi")
            ps_hi = max(10.0, round(ps_max))
            ps_val = min(max(0.0, round(ps_med)), ps_hi)
        except Exception:
            ps_hi, ps_val = 200.0, 100.0
        ps_soglia = st.slider("Soglia (€/MWh)", min_value=0.0, max_value=ps_hi,
                              value=ps_val, step=5.0, key="ps_soglia",
                              help="Ore con prezzo ≥ soglia. Imposta il tuo costo variabile (o strike) per vedere i blocchi economicamente utili.")

        ps = calcola_persistenza_soglia(prezzi, soglia=ps_soglia)
        if ps["n_ore_totali"] == 0:
            st.warning("Dati insufficienti per calcolare la persistenza.")
        else:
            k1, k2, k3, k4 = st.columns(4)
            render_kpi(edu("Ore sopra soglia", "Quante ore del periodo hanno prezzo ≥ soglia, e che quota del totale rappresentano."), f"{ps['n_ore_sopra']:,} ({ps['quota'] * 100:.1f} %)", k1)
            render_kpi(edu("N. blocchi", "Quanti blocchi di ore consecutive sopra soglia ci sono nel periodo."), f"{ps['n_blocchi']:,}", k2)
            render_kpi(edu("Blocco più lungo", "La sequenza più lunga di ore consecutive sopra soglia: il tuo miglior 'run' economico."), f"{ps['durata_max']} h" if ps["durata_max"] else "—", k3)
            render_kpi(edu("Durata mediana", "Metà dei blocchi dura al massimo queste ore: la persistenza 'tipica'."), f"{ps['durata_mediana']:.0f} h" if ps["durata_mediana"] is not None else "—", k4)

            df_ps = ps["df_blocchi"]
            if len(df_ps):
                top_ps = df_ps.sort_values("Durata (ore)", ascending=False).head(20).iloc[::-1].copy()
                top_ps["_medio_txt"] = top_ps["Prezzo medio (€/MWh)"].map(lambda v: f"{v:.2f}")
                fig_ps = go.Figure()
                fig_ps.add_trace(go.Bar(
                    x=top_ps["Durata (ore)"], y=top_ps["Inizio"], orientation="h",
                    marker_color="#38bdf8", name="Durata (ore)",
                    customdata=np.stack([top_ps["Fine"].to_numpy(), top_ps["_medio_txt"].to_numpy()], axis=1),
                    hovertemplate="Inizio: %{y}<br>Fine: %{customdata[0]}<br>Durata: %{x} h<br>Prezzo medio: %{customdata[1]} €/MWh<extra></extra>"))
                fig_ps.update_layout(template="plotly_dark", height=max(320, 40 * len(top_ps) + 80),
                                     title="Blocchi più lunghi sopra soglia",
                                     xaxis_title="Durata (ore)", yaxis_title="Inizio blocco")
                st.plotly_chart(fig_ps, use_container_width=True)

                st.markdown("**Tabella blocchi**")
                st.dataframe(df_ps.sort_values("Durata (ore)", ascending=False),
                             use_container_width=True, hide_index=True)
                st.download_button(
                    "⬇️ Esporta blocchi (CSV)",
                    df_ps.to_csv(index=False).encode("utf-8"),
                    file_name=f"persistenza_soglia_{d0}_{d1}.csv",
                    mime="text/csv",
                    help="Scarica inizio, fine, durata in ore e prezzo medio/max di ogni blocco sopra soglia.",
                )
            else:
                st.info("Nessuna ora sopra la soglia nel periodo: abbassa la soglia per vedere i blocchi.")

    with tab35:
        titolo_sc = edu("Spread calendario", "Il prezzo base di un mese è la media di tutte le sue ore: il riferimento ETRM più usato per confrontare i mesi tra loro. Lo spread calendario è la differenza tra il base di un mese e quello del mese precedente (M+1 − M): positivo = mese successivo più caro. Serve a chi copre i costi (i mesi cari si comprano in anticipo), a chi valuta stagionalità e contratti indicizzati alla media mensile.")
        st.markdown(f"**{titolo_sc}**: prezzo base mensile e spread mese-su-mese nel periodo selezionato.", unsafe_allow_html=True)

        sc = calcola_spread_calendario(prezzi)
        if sc["n_mesi"] == 0:
            st.warning("Dati insufficienti per calcolare i prezzi base mensili.")
        else:
            s1, s2, s3, s4 = st.columns(4)
            render_kpi(edu("Mesi analizzati", "Quanti mesi di calendario hanno almeno un'ora di dati nel periodo."), f"{sc['n_mesi']}", s1)
            render_kpi(edu("Spread medio M/M+1", "Differenza media tra il base di un mese e quello del precedente: quanto costa in media 'spostarsi' di un mese."), f"{sc['spread_medio']:+,.2f} €/MWh" if sc["spread_medio"] is not None else "—", s2)
            render_kpi(edu("Spread max / min", "La transizione mese-su-mese più cara e quella più economica del periodo."), f"{sc['spread_max']:+,.0f} / {sc['spread_min']:+,.0f}" if sc["spread_max"] is not None else "—", s3)
            quota_txt = f"{sc['quota_pos'] * 100:.0f} % positivi" if sc["quota_pos"] is not None else "—"
            render_kpi(edu("Volatilità spread", "Deviazione std degli spread mensili e quota di transizioni al rialzo: quanto è irregolare la curva stagionale."), f"σ {sc['std_spread']:,.2f} · {quota_txt}" if sc["std_spread"] is not None else "—", s4)

            df_sc = sc["df_spread"]
            if len(df_sc):
                ord_sc = df_sc.reset_index(drop=True)
                colori_sc = ["#ef4444" if d > 0 else "#22c55e" for d in ord_sc["Spread (€/MWh)"]]
                fig_sc = go.Figure()
                fig_sc.add_trace(go.Bar(
                    x=ord_sc["Coppia"], y=ord_sc["Spread (€/MWh)"], orientation="v",
                    name="Spread (€/MWh)", marker_color=colori_sc,
                    hovertemplate="Coppia: %{x}<br>Spread: %{y:+.2f} €/MWh<extra></extra>"))
                fig_sc.update_layout(template="plotly_dark", height=380,
                                     title="Spread calendario mese-su-mese",
                                     xaxis_title="Coppia di mesi", yaxis_title="Spread (€/MWh, + = mese successivo più caro)")
                st.plotly_chart(fig_sc, use_container_width=True)
                st.caption("Rosso = mese successivo più caro (contango stagionale), verde = mese successivo più economico.")
            elif sc["n_mesi"] > 1:
                st.info("I mesi presenti non sono di calendario consecutivi: nessuno spread calcolabile.")

            st.markdown("**Confronto libero tra due mesi**")
            mesi_opts = list(sc["df_mesi"]["Mese"])
            cc0, cc1 = st.columns(2)
            m_a = cc0.selectbox("Mese A", mesi_opts, index=0, key="sc_mese_a")
            m_b = cc1.selectbox("Mese B", mesi_opts, index=min(1, len(mesi_opts) - 1), key="sc_mese_b")
            va = float(sc["df_mesi"].loc[sc["df_mesi"]["Mese"] == m_a, "Prezzo base medio (€/MWh)"].iloc[0])
            vb = float(sc["df_mesi"].loc[sc["df_mesi"]["Mese"] == m_b, "Prezzo base medio (€/MWh)"].iloc[0])
            delta_ab = vb - va
            st.metric(f"Spread {m_a} → {m_b}", f"{delta_ab:+,.2f} €/MWh",
                      delta=f"{va:,.2f} → {vb:,.2f} €/MWh", delta_color="off")

            st.markdown("**Tabella mesi**")
            st.dataframe(sc["df_mesi"], use_container_width=True, hide_index=True)
            if len(df_sc):
                st.markdown("**Tabella spread**")
                st.dataframe(df_sc, use_container_width=True, hide_index=True)
                st.download_button(
                    "⬇️ Esporta spread calendario (CSV)",
                    df_sc.to_csv(index=False).encode("utf-8"),
                    file_name=f"spread_calendario_{d0}_{d1}.csv",
                    mime="text/csv",
                    help="Scarica coppia di mesi, prezzi base e spread in €/MWh per ogni transizione mese-su-mese.",
                )

    with tab36:
        titolo_dc = edu("Decomposizione prezzo", "Separa il prezzo orario nelle sue componenti: trend di fondo (mediana mobile settimanale), pattern giornaliero (quali ore costano di più/meno), pattern settimanale (feriali vs weekend) e residuo (shock e rumore non spiegati). Serve a capire se un picco è 'normale' per quell'ora o un'anomalia da investigare, e quanta parte del prezzo è strutturalmente prevedibile.")
        st.markdown(f"**{titolo_dc}**: trend + stagionalità giornaliera/settimanale + residuo nel periodo selezionato.", unsafe_allow_html=True)

        dc = calcola_decomposizione_prezzo(prezzi)
        if dc["n_ore"] == 0:
            st.warning("Dati insufficienti per la decomposizione.")
        else:
            c1, c2, c3, c4 = st.columns(4)
            render_kpi(edu("Ore analizzate", "Numero di ore con prezzo valido usate nella decomposizione."), f"{dc['n_ore']}", c1)
            quota_dc = f"{dc['quota_spiegata'] * 100:.1f} %" if dc["quota_spiegata"] is not None else "—"
            render_kpi(edu("Quota varianza spiegata", "Frazione della variabilità del prezzo spiegata da trend + pattern giornaliero e settimanale: più è alta, più il prezzo è prevedibile dalla struttura."), quota_dc, c2)
            render_kpi(edu("Std residuo", "Ampiezza tipica degli shock non spiegati dalla struttura, in €/MWh."), f"{dc['std_residuo']:,.2f} €/MWh" if dc["std_residuo"] is not None else "—", c3)
            if dc["shock_quando"] is not None:
                try:
                    sq = pd.Timestamp(dc["shock_quando"]).strftime("%d/%m %H:00")
                except Exception:
                    sq = str(dc["shock_quando"])
                shock_txt = f"{dc['shock_max']:+,.2f} €/MWh · {sq}"
            else:
                shock_txt = "—"
            render_kpi(edu("Shock massimo", "Il residuo più grande in valore assoluto: l'ora più anomala del periodo rispetto alla struttura attesa."), shock_txt, c4)

            fig_dc1 = go.Figure()
            fig_dc1.add_trace(go.Scatter(x=prezzi.index, y=prezzi.values, mode="lines",
                                         name="Prezzo spot (€/MWh)", line=dict(color="#3b82f6", width=1)))
            fig_dc1.add_trace(go.Scatter(x=dc["trend"].index, y=dc["trend"].values, mode="lines",
                                         name="Trend di fondo", line=dict(color="#f59e0b", width=2.5)))
            fig_dc1.update_layout(template="plotly_dark", height=360, title="Prezzo orario e trend di fondo",
                                  xaxis_title="Data e Ora", yaxis_title="€/MWh", hovermode="x unified",
                                  legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig_dc1, use_container_width=True)

            pg_dc, ps_dc = st.columns(2)
            with pg_dc:
                fig_dc2 = go.Figure()
                fig_dc2.add_trace(go.Scatter(x=list(dc["pattern_giornaliero"].index),
                                             y=dc["pattern_giornaliero"].values, mode="lines+markers",
                                             name="Pattern giornaliero",
                                             line=dict(color="#22c55e", width=2), marker=dict(size=4)))
                fig_dc2.add_hline(y=0, line_dash="dash", line_color="#6b7280")
                fig_dc2.update_layout(template="plotly_dark", height=320, title="Pattern giornaliero",
                                      xaxis_title="Ora del giorno", yaxis_title="€/MWh vs media")
                st.plotly_chart(fig_dc2, use_container_width=True)
            with ps_dc:
                giorni_lbl = ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"]
                vals_ps = dc["pattern_settimanale"].values
                colori_ps = ["#ef4444" if v > 0 else "#22c55e" for v in vals_ps]
                fig_dc3 = go.Figure()
                fig_dc3.add_trace(go.Bar(x=giorni_lbl, y=vals_ps, marker_color=colori_ps,
                                         name="Pattern settimanale",
                                         hovertemplate="%{x}: %{y:+.2f} €/MWh<extra></extra>"))
                fig_dc3.update_layout(template="plotly_dark", height=320, title="Pattern settimanale",
                                      xaxis_title="Giorno", yaxis_title="€/MWh vs media")
                st.plotly_chart(fig_dc3, use_container_width=True)
            st.caption("Pattern centrati a media zero: valori positivi = ore/giorni strutturalmente più cari della media.")

            res_dc = dc["residuo"]
            sigma_dc = float(res_dc.std()) if len(res_dc) else 0.0
            fig_dc4 = go.Figure()
            fig_dc4.add_trace(go.Scatter(x=res_dc.index, y=res_dc.values, mode="lines",
                                         name="Residuo (€/MWh)", line=dict(color="#a78bfa", width=1)))
            if sigma_dc > 0:
                anom_dc = res_dc[res_dc.abs() > 2 * sigma_dc]
                if len(anom_dc):
                    fig_dc4.add_trace(go.Scatter(x=anom_dc.index, y=anom_dc.values, mode="markers",
                                                 name=f"Anomalie > 2σ ({len(anom_dc)})",
                                                 marker=dict(color="#ef4444", size=6)))
                fig_dc4.add_hline(y=2 * sigma_dc, line_dash="dash", line_color="#ef4444",
                                  annotation_text="+2σ", annotation_position="top left")
                fig_dc4.add_hline(y=-2 * sigma_dc, line_dash="dash", line_color="#ef4444",
                                  annotation_text="−2σ", annotation_position="bottom left")
            fig_dc4.add_hline(y=0, line_color="#6b7280")
            fig_dc4.update_layout(template="plotly_dark", height=340, title="Residuo: shock e rumore non spiegati",
                                  xaxis_title="Data e Ora", yaxis_title="Residuo (€/MWh)", hovermode="x unified",
                                  legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig_dc4, use_container_width=True)
            st.caption("Punti rossi = ore anomale (|residuo| oltre 2 deviazioni standard): candidati da investigare.")

            st.download_button(
                "⬇️ Esporta decomposizione (CSV)",
                dc["df_export"].to_csv(index=False).encode("utf-8"),
                file_name=f"decomposizione_prezzo_{d0}_{d1}.csv",
                mime="text/csv",
                help="Scarica la serie oraria con prezzo, trend, componenti stagionali e residuo.",
            )

    with tab37:
        titolo_sq = edu("Sequenze (rally & drawdown)", "Quante ore di fila il prezzo sale senza interruzioni (rally) o scende senza interruzioni (drawdown), e di quanto si muove in ciascuna sequenza. Serve a calibrare stop e target: un movimento direzionale insolitamente lungo rispetto alla storia è un'anomalia, mentre l'ampiezza media delle sequenze misura il momentum disponibile ora per ora.")
        st.markdown(f"**{titolo_sq}**: sequenze consecutive di rialzo e ribasso del prezzo orario nel periodo selezionato.", unsafe_allow_html=True)

        sq = calcola_sequenze_prezzo(prezzi)
        if sq["n_ore"] < 2:
            st.warning("Dati insufficienti per l'analisi delle sequenze.")
        else:
            c1, c2, c3, c4 = st.columns(4)
            render_kpi(edu("Sequenze totali", "Rally + drawdown + flat: quante sequenze consecutive di movimento compongono il periodo."), f"{sq['n_rally'] + sq['n_drawdown'] + sq['n_flat']}", c1)
            render_kpi(edu("Rally / Drawdown", "Quante sequenze di rialzo e di ribasso sono state rilevate nel periodo."), f"{sq['n_rally']} / {sq['n_drawdown']}", c2)
            if sq["rally_max_ore"] is not None:
                try:
                    rmi = pd.Timestamp(sq["rally_max_inizio"]).strftime("%d/%m %H:00")
                    rmf = pd.Timestamp(sq["rally_max_fine"]).strftime("%d/%m %H:00")
                    rally_txt = f"{sq['rally_max_ore']} ore · +{sq['rally_max_amp']:,.2f} €/MWh · {rmi}→{rmf}"
                except Exception:
                    rally_txt = f"{sq['rally_max_ore']} ore · +{sq['rally_max_amp']:,.2f} €/MWh"
            else:
                rally_txt = "—"
            render_kpi(edu("Rally più lungo", "La sequenza di rialzo più lunga del periodo: durata, ampiezza e intervallo."), rally_txt, c3)
            if sq["drawdown_max_ore"] is not None:
                try:
                    dmi = pd.Timestamp(sq["drawdown_max_inizio"]).strftime("%d/%m %H:00")
                    dmf = pd.Timestamp(sq["drawdown_max_fine"]).strftime("%d/%m %H:00")
                    draw_txt = f"{sq['drawdown_max_ore']} ore · {sq['drawdown_max_amp']:,.2f} €/MWh · {dmi}→{dmf}"
                except Exception:
                    draw_txt = f"{sq['drawdown_max_ore']} ore · {sq['drawdown_max_amp']:,.2f} €/MWh"
            else:
                draw_txt = "—"
            render_kpi(edu("Drawdown più lungo", "La sequenza di ribasso più lunga del periodo: durata, ampiezza e intervallo."), draw_txt, c4)

            fig_sq1 = go.Figure()
            fig_sq1.add_trace(go.Scatter(x=prezzi.index, y=prezzi.values, mode="lines",
                                         name="Prezzo spot (€/MWh)", line=dict(color="#3b82f6", width=1)))
            if sq["rally_max_ore"] is not None:
                fig_sq1.add_vrect(x0=sq["rally_max_inizio"], x1=sq["rally_max_fine"],
                                  fillcolor="#22c55e", opacity=0.15, layer="below",
                                  annotation_text="Rally più lungo", annotation_position="top left",
                                  line_width=0)
            if sq["drawdown_max_ore"] is not None:
                fig_sq1.add_vrect(x0=sq["drawdown_max_inizio"], x1=sq["drawdown_max_fine"],
                                  fillcolor="#ef4444", opacity=0.15, layer="below",
                                  annotation_text="Drawdown più lungo", annotation_position="top left",
                                  line_width=0)
            fig_sq1.update_layout(template="plotly_dark", height=380, title="Prezzo orario con sequenze direzionali più lunghe",
                                  xaxis_title="Data e Ora", yaxis_title="€/MWh", hovermode="x unified",
                                  legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig_sq1, use_container_width=True)

            df_exp = sq["df_export"]
            if len(df_exp):
                df_r = df_exp[df_exp["Tipo"] == "Rally"]["Durata (ore)"]
                df_d = df_exp[df_exp["Tipo"] == "Drawdown"]["Durata (ore)"]
                fig_sq2 = go.Figure()
                if len(df_r):
                    fig_sq2.add_trace(go.Histogram(x=df_r, name="Rally", marker_color="#22c55e",
                                                   opacity=0.75, xbins=dict(size=1)))
                if len(df_d):
                    fig_sq2.add_trace(go.Histogram(x=df_d, name="Drawdown", marker_color="#ef4444",
                                                   opacity=0.75, xbins=dict(size=1)))
                fig_sq2.update_layout(template="plotly_dark", height=330,
                                      title="Distribuzione delle durate delle sequenze",
                                      xaxis_title="Durata (ore)", yaxis_title="Numero di sequenze",
                                      barmode="overlay",
                                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
                st.plotly_chart(fig_sq2, use_container_width=True)
                st.caption("Movimenti di più ore sono meno frequenti: una sequenza in coda alla distribuzione destra è un'anomalia da investigare.")

                r_sq, d_sq = st.columns(2)
                with r_sq:
                    st.markdown(f"**Top rally per ampiezza** (media {sq['ampiezza_media_rally'] if sq['ampiezza_media_rally'] is not None else '—'} €/MWh, durata media {sq['durata_media_rally'] if sq['durata_media_rally'] is not None else '—'} ore)")
                    top_r = df_exp[df_exp["Tipo"] == "Rally"].sort_values("Ampiezza (€/MWh)", ascending=False).head(10)
                    st.dataframe(top_r, use_container_width=True, hide_index=True)
                with d_sq:
                    st.markdown(f"**Top drawdown per ampiezza** (media {sq['ampiezza_media_drawdown'] if sq['ampiezza_media_drawdown'] is not None else '—'} €/MWh, durata media {sq['durata_media_drawdown'] if sq['durata_media_drawdown'] is not None else '—'} ore)")
                    top_d = df_exp[df_exp["Tipo"] == "Drawdown"].sort_values("Ampiezza (€/MWh)").head(10)
                    st.dataframe(top_d, use_container_width=True, hide_index=True)

            st.download_button(
                "⬇️ Esporta sequenze (CSV)",
                sq["df_export"].to_csv(index=False).encode("utf-8"),
                file_name=f"sequenze_prezzo_{d0}_{d1}.csv",
                mime="text/csv",
                help="Scarica tutte le sequenze rilevate: tipo, inizio, fine, durata in ore e ampiezza in €/MWh.",
            )

    with tab38:
        titolo_vf = edu("Valore della flessibilità (curtailment)", "Il CURTAILMENT (taglio del carico, o peak shaving) è la forma più semplice di demand response: nelle ore più care spegni i carichi non prioritari invece di pagare lo spot. Questo tab calcola quanto varrebbe farlo: prende il tuo profilo di consumo (MW per fascia), ordina le ore del periodo per costo orario e simula il taglio di N MW nelle ore più care. A differenza dello shifting (che sposta i consumi), qui il consumo si riduce davvero: il risparmio è netto, ma rinunci a produrre in quelle ore. È il numero da portare al tavolo quando si negozia un contratto di interrompibilità.")
        st.markdown(f"**{titolo_vf}**: risparmio stimato tagliando il carico nelle ore più care del periodo.", unsafe_allow_html=True)

        vf1, vf2, vf3 = st.columns(3)
        with vf1:
            vf_f1 = st.number_input("Potenza in F1 (MW)", min_value=0.0, value=1.0, step=0.5, key="vf_f1",
                                    help="Ore di punta: lun–ven 08:00–19:00.")
        with vf2:
            vf_f2 = st.number_input("Potenza in F2 (MW)", min_value=0.0, value=1.0, step=0.5, key="vf_f2",
                                    help="Ore intermedie: lun–ven 07:00–08:00 e 19:00–23:00, sab 07:00–23:00.")
        with vf3:
            vf_f3 = st.number_input("Potenza in F3 (MW)", min_value=0.0, value=1.0, step=0.5, key="vf_f3",
                                    help="Ore fuori punta: notti, domeniche e festivi.")
        vf4, vf5 = st.columns(2)
        with vf4:
            vf_taglio = st.number_input("Potenza tagliabile (MW)", min_value=0.0, value=0.5, step=0.1, key="vf_taglio",
                                        help="Quanti MW puoi spegnere nelle ore di picco (carichi interrompibili). Il taglio non supera mai il carico presente in ciascuna ora.")
        with vf5:
            vf_ore = st.slider("Ore più care da tagliare", min_value=0, max_value=500, value=100, step=10, key="vf_ore",
                               help="Quante ore (le più care per costo orario = prezzo × MW) includere nella simulazione.")

        vf = calcola_valore_flessibilita(prezzi, vf_f1, vf_f2, vf_f3, vf_taglio, vf_ore)
        if vf["n_ore"] == 0:
            st.warning("Dati insufficienti per la simulazione.")
        elif vf["mwh"] <= 0:
            st.info("Imposta una potenza maggiore di zero in almeno una fascia per simulare il taglio del carico.")
        elif vf["ore_taglio"] == 0:
            st.info("Nessuna ora con taglio effettivo: aumenta la potenza tagliabile o il numero di ore.")
        else:
            c1, c2, c3, c4 = st.columns(4)
            pct_txt = f"{vf['risparmio_pct']:.2f} %" if vf["risparmio_pct"] is not None else "n.d."
            render_kpi(edu("Risparmio stimato", "Euro risparmiati tagliando la potenza impostata nelle ore più care del periodo, e quota percentuale sulla bolletta totale."), f"{vf['risparmio']:,.0f} €<br><small>{pct_txt} della bolletta</small>", c1)
            render_kpi(edu("Ore di taglio / MWh tagliati", "In quante ore (le più care) il taglio è effettivo e quanta energia viene rinunciata nel periodo."), f"{vf['ore_taglio']:,} h<br><small>{vf['mwh_tagliati']:,.1f} MWh tagliati</small>", c2)
            pmt = f"{vf['prezzo_medio_taglio']:,.2f} €/MWh" if vf["prezzo_medio_taglio"] is not None else "—"
            render_kpi(edu("Prezzo medio ore tagliate", "Prezzo medio ponderato delle ore in cui tagli: più è sopra la media del periodo, più il curtailment è selettivo ed efficace."), f"{pmt}<br><small>media periodo {vf['prezzo_medio_periodo']:,.2f} €/MWh</small>", c3)
            mens = vf["mensile"]
            if len(mens):
                bm = mens.loc[mens["Risparmio (€)"].idxmax()]
                mese_txt = f"{bm['Mese']}<br><small>{bm['Risparmio (€)']:,.0f} €</small>"
            else:
                mese_txt = "—"
            render_kpi(edu("Mese migliore", "Il mese in cui il curtailment rende di più: utile per concentrare lì i programmi di interrompibilità stagionali."), mese_txt, c4)
            st.caption(f"💡 Profilo: F1 {vf_f1} MW, F2 {vf_f2} MW, F3 {vf_f3} MW — taglio {vf_taglio} MW nelle {vf_ore} ore più care: {vf['mwh']:,.0f} MWh per {vf['totale']:,.0f} € nel periodo ({vf['n_ore']:,} ore).")

            col_v1, col_v2 = st.columns(2)
            with col_v1:
                fig_vf1 = go.Figure()
                fig_vf1.add_trace(go.Bar(x=mens["Mese"], y=mens["Risparmio (€)"], name="Risparmio",
                                         marker_color="#22c55e"))
                fig_vf1.update_layout(template="plotly_dark", height=330, title="Risparmio mensile da curtailment",
                                      xaxis_title="Mese", yaxis_title="€",
                                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
                st.plotly_chart(fig_vf1, use_container_width=True)
            with col_v2:
                df_tag = vf["df_export"][vf["df_export"]["Taglio (MW)"] > 0]
                fig_vf2 = go.Figure()
                fig_vf2.add_trace(go.Scatter(x=prezzi.index, y=prezzi.values, mode="lines",
                                             name="Prezzo spot (€/MWh)", line=dict(color="#3b82f6", width=1)))
                if len(df_tag):
                    fig_vf2.add_trace(go.Scatter(x=df_tag["Data e ora"], y=df_tag["Prezzo (€/MWh)"],
                                                 mode="markers", name="Ore tagliate",
                                                 marker=dict(color="#f59e0b", size=6, opacity=0.8),
                                                 hovertemplate="%{x}<br>%{y:.2f} €/MWh<extra></extra>"))
                fig_vf2.update_layout(template="plotly_dark", height=330, title="Prezzo orario con ore di taglio",
                                      xaxis_title="Data e Ora", yaxis_title="€/MWh", hovermode="x unified",
                                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
                st.plotly_chart(fig_vf2, use_container_width=True)
            st.caption("Le ore tagliate si concentrano sui picchi di prezzo: se vedi tagli sparsi anche a prezzi bassi, il tuo profilo carica molto in F3 e conviene alzare la potenza tagliabile.")

            st.markdown("**Top 15 ore per risparmio**")
            top_vf = vf["df_export"].sort_values("Risparmio (€)", ascending=False).head(15)
            st.dataframe(top_vf, use_container_width=True, hide_index=True)

            st.download_button(
                "⬇️ Esporta ore di taglio (CSV)",
                vf["df_export"].to_csv(index=False).encode("utf-8"),
                file_name=f"valore_flessibilita_{d0}_{d1}.csv",
                mime="text/csv",
                help="Scarica tutte le ore selezionate: data e ora, fascia, prezzo, carico, MW tagliati e risparmio in €.",
            )

    with tab39:
        titolo_to = edu("Top ore di costo", "La classifica delle ORE più care del periodo: per ogni ora il costo è prezzo spot × MW della fascia F1/F2/F3. Mentre 'Top giorni di costo' ragiona per giorno di calendario (domanda di tesoreria), qui vedi le singole ore — la domanda operativa per demand response, shifting e contratti di interrompibilità: 'a che ora mi sono costato di più?'")
        st.markdown(f"**{titolo_to}**: le ore più care del periodo per costo orario (prezzo × carico), con distribuzione per ora del giorno e per fascia.", unsafe_allow_html=True)

        to1, to2, to3 = st.columns(3)
        with to1:
            to_f1 = st.number_input("Potenza in F1 (MW)", min_value=0.0, value=1.0, step=0.5, key="to39_f1",
                                    help="Ore di punta: lun–ven 08:00–19:00.")
        with to2:
            to_f2 = st.number_input("Potenza in F2 (MW)", min_value=0.0, value=1.0, step=0.5, key="to39_f2",
                                    help="Ore intermedie: lun–ven 07:00–08:00 e 19:00–23:00, sab 07:00–23:00.")
        with to3:
            to_f3 = st.number_input("Potenza in F3 (MW)", min_value=0.0, value=1.0, step=0.5, key="to39_f3",
                                    help="Ore fuori punta: notti, domeniche e festivi.")
        to_top = st.slider("Numero di ore in classifica", min_value=5, max_value=100, value=20, step=5, key="to39_top",
                           help="Quante ore (le più care per costo orario) mostrare in tabella.")

        toc = calcola_top_ore_costo(prezzi, to_f1, to_f2, to_f3, to_top)
        if toc["n_ore"] == 0:
            st.warning("Dati insufficienti: nessuna ora con prezzo valido nel periodo.")
        elif toc["mwh_tot"] <= 0:
            st.info("Imposta una potenza maggiore di zero in almeno una fascia per calcolare il costo orario.")
        else:
            c1, c2, c3, c4 = st.columns(4)
            om_data = toc["ora_max_data"]
            om_txt = f"{om_data.strftime('%d/%m/%Y %H:%M')}<br><small>{toc['ora_max_costo']:,.2f} €</small>" if om_data is not None else "—"
            render_kpi(edu("Ora più costosa", "L'ora singola con il costo più alto (prezzo × MW della fascia): il tuo picco di spesa del periodo."), om_txt, c1)
            render_kpi(edu("Costo medio orario", "Costo orario medio del periodo: il benchmark contro cui confrontare ogni ora della classifica."), f"{toc['costo_medio_orario']:,.2f} €/h", c2)
            q5_txt = f"{toc['quota_top5pct']:.1f} %" if toc["quota_top5pct"] is not None else "n.d."
            render_kpi(edu("Quota del 5% di ore più care", "Che percentuale del costo totale è generata dal 5% di ore più costose: misura la concentrazione della bolletta."), f"{q5_txt}<br><small>del costo totale</small>", c3)
            rmm_txt = f"{toc['rapporto_max_medio']:.2f} ×" if toc["rapporto_max_medio"] is not None else "n.d."
            render_kpi(edu("Rapporto max/medio", "Quanto l'ora più costosa pesa rispetto all'ora media: più è alto, più c'è margine per shifting/curtailment."), rmm_txt, c4)
            st.caption(f"💡 Profilo: F1 {to_f1} MW, F2 {to_f2} MW, F3 {to_f3} MW — {toc['costo_tot']:,.0f} € totali su {toc['mwh_tot']:,.0f} MWh ({toc['n_ore']:,} ore). Ora del giorno più costosa in aggregato: {toc['ora_max_giorno']:02d}:00.")

            col_t1, col_t2 = st.columns(2)
            with col_t1:
                fig_to1 = go.Figure()
                fig_to1.add_trace(go.Bar(x=toc["per_ora"]["Ora"], y=toc["per_ora"]["Costo (€)"],
                                         name="Costo", marker_color="#f59e0b"))
                fig_to1.update_layout(template="plotly_dark", height=330, title="Costo per ora del giorno",
                                      xaxis_title="Ora", yaxis_title="€",
                                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
                st.plotly_chart(fig_to1, use_container_width=True)
            with col_t2:
                fig_to2 = go.Figure()
                fig_to2.add_trace(go.Bar(x=toc["per_fascia"]["Fascia"], y=toc["per_fascia"]["Quota %"],
                                         name="Quota %", marker_color="#3b82f6"))
                fig_to2.update_layout(template="plotly_dark", height=330, title="Quota di costo per fascia",
                                      xaxis_title="Fascia", yaxis_title="% del costo totale",
                                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
                st.plotly_chart(fig_to2, use_container_width=True)
            st.caption("Le barre per ora del giorno mostrano dove si concentra il costo: le ore alte sono i primi candidati per shifting del carico o curtailment.")

            st.markdown(f"**Top {toc['top_n']} ore più costose**")
            st.dataframe(toc["top"], use_container_width=True, hide_index=True)

            st.download_button(
                "⬇️ Esporta top ore (CSV)",
                toc["top"].to_csv(index=False).encode("utf-8"),
                file_name=f"top_ore_costo_{d0}_{d1}.csv",
                mime="text/csv",
                help="Scarica la classifica delle ore più care: data e ora, fascia, prezzo, carico, costo e quota % sul totale.",
            )

    with tab40:
        titolo_ohlc = edu("Candele giornaliere (OHLC)", "La CANDELA GIORNALIERA riassume in una figura le 24 ore di mercato: APERTURA (prezzo dell'ora 00:00), MASSIMO e MINIMO di giornata, CHIUSURA (prezzo dell'ultima ora). L'ESCURSIONE (max meno min) misura quanto il mercato si è mosso in giornata: escursioni alte = giornata nervosa, in cui il timing degli acquisti fa la differenza; escursioni basse = giornata piatta. La direzione (rialzo/ribasso/flat) dice se il mercato ha chiuso sopra, sotto o uguale all'apertura. È la vista da trader per pianificare gli acquisti sulla borsa day-ahead: comprare nelle ore del minimo e non sul picco.")
        st.markdown(f"**{titolo_ohlc}**: candele giornaliere del prezzo spot (apertura, massimo, minimo, chiusura) con escursione e direzione.", unsafe_allow_html=True)

        oh_soglia = st.slider("Evidenzia escursioni oltre (€/MWh)", min_value=0.0, max_value=100.0, value=25.0, step=1.0, key="oh40_soglia",
                              help="Giorni con escursione (massimo meno minimo) oltre questa soglia vengono evidenziati: giornate nervose in cui il timing degli acquisti conta di più.")

        oh = calcola_ohlc_giornaliero(prezzi)
        if oh["n_giorni"] == 0:
            st.warning("Dati insufficienti per le candele giornaliere.")
        else:
            c1, c2, c3, c4 = st.columns(4)
            render_kpi(edu("Escursione media", "Movimento medio intraday (massimo meno minimo di ogni giorno): quanto si muove tipicamente il mercato in una giornata."), f"{oh['escursione_media']:,.2f} €/MWh", c1)
            gm = oh["giorno_max_escursione"]
            gm_txt = gm.strftime("%d/%m/%Y") if gm is not None and hasattr(gm, "strftime") else "—"
            render_kpi(edu("Escursione massima", "Il giorno più nervoso del periodo: massima escursione (max meno min) osservata."), f"{oh['escursione_max']:,.2f} €/MWh<br><small>{gm_txt}</small>", c2)
            render_kpi(edu("Giorni rialzisti", "Quota di giorni con chiusura sopra l'apertura: sopra il 50% il mercato tende a salire in giornata."), f"{oh['quota_rialzo_pct']:.1f} %", c3)
            rem_txt = f"{oh['rapporto_esc_media_prezzo_medio'] * 100:.1f} %" if oh["rapporto_esc_media_prezzo_medio"] is not None else "n.d."
            render_kpi(edu("Escursione / prezzo medio", "L'escursione media in percentuale sul prezzo medio del periodo: misura la nervosità relativa del mercato."), f"{rem_txt}<br><small>prezzo medio {oh['prezzo_medio']:,.2f} €/MWh</small>", c4)

            df_oh = oh["df"]
            fig_ohlc = go.Figure()
            fig_ohlc.add_trace(go.Candlestick(
                x=df_oh["Giorno"], open=df_oh["Apertura (€/MWh)"],
                high=df_oh["Massimo (€/MWh)"], low=df_oh["Minimo (€/MWh)"],
                close=df_oh["Chiusura (€/MWh)"], name="OHLC giornaliero",
                increasing_line_color="#22c55e", decreasing_line_color="#ef4444"))
            fig_ohlc.update_layout(template="plotly_dark", height=420,
                                   title="Candele giornaliere del prezzo spot",
                                   xaxis_title="Giorno", yaxis_title="€/MWh",
                                   xaxis_rangeslider_visible=False)
            st.plotly_chart(fig_ohlc, use_container_width=True)
            st.caption("Candele verdi = chiusura sopra l'apertura (rialzo), rosse = sotto (ribasso). Il corpo va da apertura a chiusura, le ombre toccano massimo e minimo di giornata.")

            col_o1, col_o2 = st.columns(2)
            with col_o1:
                colori = ["#f59e0b" if e >= oh_soglia else "#3b82f6"
                          for e in df_oh["Escursione (€/MWh)"]]
                fig_o1 = go.Figure()
                fig_o1.add_trace(go.Bar(x=df_oh["Giorno"], y=df_oh["Escursione (€/MWh)"],
                                        name="Escursione", marker_color=colori,
                                        hovertemplate="Giorno: %{x}<br>Escursione: %{y:,.2f} €/MWh<extra></extra>"))
                fig_o1.add_hline(y=oh_soglia, line_dash="dot", line_color="#9ca3af")
                fig_o1.update_layout(template="plotly_dark", height=330,
                                     title="Escursione giornaliera (max − min)",
                                     xaxis_title="Giorno", yaxis_title="€/MWh",
                                     legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
                st.plotly_chart(fig_o1, use_container_width=True)
            with col_o2:
                fig_o2 = go.Figure()
                fig_o2.add_trace(go.Bar(x=["Rialzo", "Ribasso", "Flat"],
                                        y=[int((df_oh["Direzione"] == "rialzo").sum()),
                                           int((df_oh["Direzione"] == "ribasso").sum()),
                                           int((df_oh["Direzione"] == "flat").sum())],
                                        name="Giorni",
                                        marker_color=["#22c55e", "#ef4444", "#9ca3af"]))
                fig_o2.update_layout(template="plotly_dark", height=330,
                                     title="Direzione delle giornate",
                                     xaxis_title="", yaxis_title="Giorni",
                                     legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
                st.plotly_chart(fig_o2, use_container_width=True)
            n_alta = int((df_oh["Escursione (€/MWh)"] >= oh_soglia).sum())
            st.caption(f"💡 {n_alta} giorni su {oh['n_giorni']} con escursione ≥ {oh_soglia:.0f} €/MWh: giornate in cui il timing degli acquisti sulla borsa day-ahead conta di più.")

            st.markdown("**Candele giornaliere**")
            st.dataframe(df_oh, use_container_width=True, hide_index=True)

            st.download_button(
                "⬇️ Esporta candele OHLC (CSV)",
                df_oh.to_csv(index=False).encode("utf-8"),
                file_name=f"candele_ohlc_{d0}_{d1}.csv",
                mime="text/csv",
                help="Scarica le candele giornaliere: giorno, ore osservate, apertura, massimo, minimo, chiusura, escursione, corpo e direzione.",
            )

    with tab41:
        titolo_dd = edu("Crolli & recuperi (drawdown)", "Il DRAWDOWN misura quanto perde il mercato dal suo PICCO fino al punto più basso successivo: è il rischio di chi compra al momento sbagliato. Ogni episodio parte da un massimo storico (il 'picco'), scende fino al 'minimo' (ORE DI CALO) e poi risale fino a tornare al livello del picco (ORE DI RECUPERO). Se il recupero non arriva entro fine periodo, l'episodio resta 'aperto' — stai ancora sotto il prezzo pagato. Il TEMPO MEDIO DI RECUPERO dice quanto ci mette tipicamente il mercato a tornare in pari: è la metrica chiave per dimensionare la copertura e decidere se comprare subito o aspettare che il prezzo torni giù. Nota: 'Sequenze' conta le ore di fila in calo, 'Candele OHLC' l'escursione giornaliera; qui ogni crollo è ancorato al suo picco e include il recupero.")
        st.markdown(f"**{titolo_dd}**: crolli dal picco del prezzo spot (drawdown) con profondità, durata del calo e tempo di recupero.", unsafe_allow_html=True)

        dd_soglia = st.slider("Soglia episodio significativo (€/MWh)", min_value=0.0, max_value=100.0, value=20.0, step=5.0, key="dd41_soglia",
                              help="Solo gli episodi con profondità (picco meno minimo) pari o superiore a questa soglia vengono contati nel KPI 'Episodi significativi'.")

        dd = calcola_drawdown(prezzi, soglia_eur=dd_soglia)
        if dd["n_ore"] == 0:
            st.warning("Dati insufficienti per l'analisi dei drawdown.")
        else:
            c1, c2, c3, c4 = st.columns(4)
            render_kpi(edu("Max drawdown", "Il crollo peggiore del periodo: massima perdita dal picco al minimo successivo. È il 'worst case' di chi ha comprato nel momento peggiore."), f"{dd['max_drawdown_eur']:,.2f} €/MWh", c1)
            mddp_txt = f"{dd['max_drawdown_pct']:.1f} %" if dd["max_drawdown_pct"] is not None else "n.d."
            render_kpi(edu("Max drawdown %", "Lo stesso crollo in percentuale sul picco di partenza: misura la severità relativa. 'n.d.' quando il picco è ≤ 0 (prezzi negativi)."), f"{mddp_txt}<br><small>sul picco di partenza</small>", c2)
            nsg_txt = f"{dd['n_oltre_soglia']} di {dd['n_episodi']}"
            render_kpi(edu("Episodi significativi", f"Quanti episodi di crollo hanno profondità ≥ {dd_soglia:.0f} €/MWh: misura quanto spesso il mercato fa scivoloni seri."), f"{nsg_txt}<br><small>≥ {dd_soglia:.0f} €/MWh</small>", c3)
            tmr_txt = f"{dd['tempo_medio_recupero_ore']:.0f} ore" if dd["tempo_medio_recupero_ore"] is not None else "n.d."
            render_kpi(edu("Tempo medio di recupero", "Ore medie che il mercato impiega a tornare al livello del picco dopo un crollo: la domanda 'se compro male, quanto ci mette a tornare in pari?'. Conta solo gli episodi chiusi."), f"{tmr_txt}<br><small>episodi chiusi</small>", c4)
            if dd["drawdown_attuale_eur"] > 0:
                pa_ts = pd.Timestamp(dd["picco_attuale_ts"]).strftime("%d/%m %H:00") if dd["picco_attuale_ts"] is not None else "—"
                st.caption(f"⚠️ In questo momento il mercato è sotto il picco di {dd['picco_attuale_eur']:,.2f} €/MWh ({pa_ts}): drawdown attuale di {dd['drawdown_attuale_eur']:,.2f} €/MWh.")
            else:
                st.caption("✅ In questo momento il prezzo è al suo picco corrente: nessun drawdown in corso.")

            try:
                p_dd = prezzi.astype(float).dropna()
                p_dd = p_dd[~p_dd.index.duplicated(keep="first")].sort_index()
                runmax_dd = np.maximum.accumulate(p_dd.to_numpy(dtype=float))
                fig_dd1 = go.Figure()
                fig_dd1.add_trace(go.Scatter(x=p_dd.index, y=runmax_dd, mode="lines",
                                            name="Picco corrente", line=dict(color="#22c55e", width=1.5)))
                fig_dd1.add_trace(go.Scatter(x=p_dd.index, y=p_dd.to_numpy(dtype=float), mode="lines",
                                            name="Prezzo", line=dict(color="#3b82f6", width=1),
                                            fill="tonexty", fillcolor="rgba(239,68,68,0.18)"))
                fig_dd1.update_layout(template="plotly_dark", height=380,
                                      title="Prezzo e picco corrente (l'area rossa è il drawdown)",
                                      xaxis_title="Data", yaxis_title="€/MWh",
                                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
                st.plotly_chart(fig_dd1, use_container_width=True)
                st.caption("L'area rossa tra prezzo e picco corrente è il drawdown: quanto sei sotto il massimo. Più è profonda e lunga, più è costato comprare vicino al picco.")
            except Exception:
                st.info("Grafico drawdown non disponibile per questi dati.")

            df_dd = dd["df"]
            if len(df_dd):
                top_n_dd = min(15, len(df_dd))
                df_top = df_dd.head(top_n_dd).copy()
                colori_dd = ["#ef4444" if not pd.isna(x) else "#f59e0b" for x in df_top["Ore di recupero"]]
                fig_dd2 = go.Figure()
                fig_dd2.add_trace(go.Bar(
                    x=[pd.Timestamp(t).strftime("%d/%m %H:00") for t in df_top["Picco"]],
                    y=df_top["Profondita' (€/MWh)"],
                    name="Profondità",
                    marker_color=colori_dd,
                    hovertemplate="Picco: %{x}<br>Profondità: %{y:,.2f} €/MWh<extra></extra>"))
                fig_dd2.update_layout(template="plotly_dark", height=330,
                                      title=f"Top {top_n_dd} episodi per profondità di crollo",
                                      xaxis_title="Picco di partenza", yaxis_title="€/MWh",
                                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
                st.plotly_chart(fig_dd2, use_container_width=True)
                st.caption("Rosso = episodio chiuso (recuperato), arancione = ancora aperto (il mercato non è ancora tornato al picco).")
            else:
                st.info("Nessun episodio di crollo nel periodo: il prezzo non è mai sceso dopo un picco.")

            st.markdown("**Episodi di crollo (ordinati per profondità)**")
            st.dataframe(df_dd, use_container_width=True, hide_index=True)

            st.download_button(
                "⬇️ Esporta episodi drawdown (CSV)",
                df_dd.to_csv(index=False).encode("utf-8"),
                file_name=f"drawdown_{d0}_{d1}.csv",
                mime="text/csv",
                help="Scarica gli episodi di crollo: picco, minimo, recupero, profondità in €/MWh e %, ore di calo e di recupero.",
            )

    with tab42:
        titolo_mr = edu("Mean reversion (ritorno alla media)", "La MEAN REVERSION dice se il prezzo 'torna indietro' dopo uno shock. Il modello AR(1) lega ogni ora alla precedente: coefficiente b vicino a 1 = shock che rientrano lentamente, vicino a 0 = rientro rapido. L'HALF-LIFE e' il tempo in cui uno shock si dimezza: se e' 30 ore, un picco di +60 €/MWh sopra la media sara' ancora a +30 dopo 30 ore e a +15 dopo 60. Lo Z-SCORE dice quanto e' estremo il prezzo di adesso rispetto alla storia (oltre ±2 deviazioni standard = evento raro). Uso operativo: con half-life lunga conviene coprirsi subito sugli shock; con half-life corta conviene aspettare che il prezzo torni giu' da solo. La tabella mensile mostra i cambi di regime: la mean reversion non e' costante nel tempo.")
        st.markdown(f"**{titolo_mr}**: velocita' di rientro degli shock di prezzo (half-life) via AR(1) orario, z-score del prezzo corrente e half-life per mese.", unsafe_allow_html=True)

        mr = calcola_mean_reversion(prezzi)
        if mr["n_ore"] == 0 or mr["b"] is None:
            st.warning("Dati insufficienti per stimare la mean reversion (servono almeno 50 ore valide con variabilita').")
        else:
            c1, c2, c3, c4 = st.columns(4)
            hl_txt = f"{mr['half_life_ore']:,.0f} ore" if mr["half_life_ore"] is not None else "n.d."
            render_kpi(edu("Half-life shock", "Tempo in cui uno shock di prezzo si dimezza tornando verso la media. 'n.d.' se il prezzo non torna verso la media (coefficiente AR(1) fuori dall'intervallo 0-1)."), f"{hl_txt}<br><small>regime: {mr['regime']}</small>", c1)
            render_kpi(edu("Coefficiente AR(1)", "Persistenza oraria: quanto il prezzo di un'ora dipende da quella precedente. Vicino a 1 = mercato 'vischioso', vicino a 0 = mercato che dimentica in fretta."), f"{mr['b']:.3f}<br><small>R² = {mr['r2']:.3f}</small>", c2)
            z_txt = f"{mr['z_ultimo']:+.2f} σ" if mr["z_ultimo"] is not None else "n.d."
            z_ora = pd.Timestamp(mr["ultima_ora"]).strftime("%d/%m %H:00") if mr["ultima_ora"] is not None else "—"
            render_kpi(edu("Z-score prezzo corrente", "Quanto e' estremo il prezzo dell'ultima ora rispetto alla media storica, in deviazioni standard. Oltre ±2 = evento raro: possibile segnale di acquisto (z molto negativo) o di copertura (z molto positivo)."), f"{z_txt}<br><small>{mr['ultimo_prezzo']:,.2f} €/MWh ({z_ora})</small>", c3)
            render_kpi(edu("Rumore orario", "Deviazione standard dei residui AR(1): la parte di movimento orario NON spiegata dalla persistenza. E' il 'rumore' imprevedibile che resta anche conoscendo l'ora precedente."), f"{mr['std_residui']:,.2f} €/MWh<br><small>media {mr['media']:,.2f}</small>", c4)

            try:
                p_mr = prezzi.astype(float).dropna()
                p_mr = p_mr[~p_mr.index.duplicated(keep="first")].sort_index()
                v = p_mr.to_numpy(dtype=float)
                b_mr = mr["b"]
                fig_mr1 = go.Figure()
                fig_mr1.add_trace(go.Scatter(x=v[:-1], y=v[1:], mode="markers", name="Ore",
                                            marker=dict(color="#3b82f6", size=3, opacity=0.35),
                                            hovertemplate="Ora prec: %{x:,.1f}<br>Ora succ: %{y:,.1f}<extra></extra>"))
                x_line = np.array([v.min(), v.max()])
                fig_mr1.add_trace(go.Scatter(x=x_line, y=mr["a"] + b_mr * x_line, mode="lines",
                                            name=f"AR(1): b={b_mr:.3f}", line=dict(color="#ef4444", width=2)))
                fig_mr1.add_trace(go.Scatter(x=x_line, y=x_line, mode="lines", name="y = x (persistenza totale)",
                                            line=dict(color="#9ca3af", width=1, dash="dash")))
                fig_mr1.update_layout(template="plotly_dark", height=360,
                                      title="Prezzo ora t+1 contro ora t (la retta rossa sotto la diagonale = ritorno alla media)",
                                      xaxis_title="Prezzo ora t (€/MWh)", yaxis_title="Prezzo ora t+1 (€/MWh)",
                                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
                st.plotly_chart(fig_mr1, use_container_width=True)
                st.caption("Ogni punto è un'ora: se la nuvola segue la retta rossa (più piatta della diagonale), il mercato torna verso la media. Punti lontani dalla retta = shock imprevedibili.")
            except Exception:
                st.info("Grafico AR(1) non disponibile per questi dati.")

            try:
                if mr["half_life_ore"] is not None:
                    k = np.arange(0, 169)
                    dec = 100.0 * (b_mr ** k)
                    fig_mr2 = go.Figure()
                    fig_mr2.add_trace(go.Scatter(x=k, y=dec, mode="lines", name="Shock residuo",
                                                line=dict(color="#f59e0b", width=2),
                                                fill="tozeroy", fillcolor="rgba(245,158,11,0.15)",
                                                hovertemplate="Dopo %{x} ore: %{y:.1f}%<extra></extra>"))
                    fig_mr2.add_hline(y=50, line_dash="dash", line_color="#9ca3af",
                                      annotation_text="metà shock", annotation_position="top right")
                    fig_mr2.update_layout(template="plotly_dark", height=300,
                                          title="Decadimento di uno shock: quanto resta dopo N ore",
                                          xaxis_title="Ore dallo shock", yaxis_title="% dello shock iniziale",
                                          legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
                    st.plotly_chart(fig_mr2, use_container_width=True)
                    st.caption(f"Uno shock di prezzo oggi vale ancora il 50% dopo {mr['half_life_ore']:,.0f} ore: è la traduzione visiva dell'half-life.")
            except Exception:
                st.info("Grafico decadimento shock non disponibile per questi dati.")

            try:
                roll = p_mr.rolling(168, min_periods=48)
                z_roll = (p_mr - roll.mean()) / roll.std()
                z_roll = z_roll.replace([np.inf, -np.inf], np.nan).dropna()
                if len(z_roll):
                    fig_mr3 = go.Figure()
                    fig_mr3.add_trace(go.Scatter(x=z_roll.index, y=z_roll.to_numpy(), mode="lines",
                                                name="Z-score (media mobile 7gg)", line=dict(color="#8b5cf6", width=1)))
                    fig_mr3.add_hline(y=2, line_dash="dash", line_color="#ef4444",
                                      annotation_text="+2σ", annotation_position="top right")
                    fig_mr3.add_hline(y=-2, line_dash="dash", line_color="#22c55e",
                                      annotation_text="−2σ", annotation_position="bottom right")
                    fig_mr3.update_layout(template="plotly_dark", height=300,
                                          title="Z-score del prezzo (media mobile 7 giorni): quando esce dalle bande è un evento raro",
                                          xaxis_title="Data", yaxis_title="Deviazioni standard",
                                          legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
                    st.plotly_chart(fig_mr3, use_container_width=True)
                    st.caption("Sopra +2σ il prezzo è insolitamente caro (valuta la copertura), sotto −2σ è insolitamente economico (valuta l'acquisto).")
            except Exception:
                st.info("Grafico z-score non disponibile per questi dati.")

            df_mesi_mr = mr["df_mesi"]
            if len(df_mesi_mr):
                st.markdown("**Half-life per mese (cambi di regime)**")
                df_hl = df_mesi_mr.dropna(subset=["Half-life (ore)"])
                if len(df_hl):
                    fig_mr4 = go.Figure()
                    fig_mr4.add_trace(go.Bar(x=df_hl["Mese"], y=df_hl["Half-life (ore)"],
                                            name="Half-life", marker_color="#06b6d4",
                                            hovertemplate="%{x}<br>Half-life: %{y:.0f} ore<br>AR(1): %{customdata:.3f}<extra></extra>",
                                            customdata=df_hl["AR(1)"].to_numpy()))
                    fig_mr4.update_layout(template="plotly_dark", height=300,
                                          title="Half-life mensile: i mesi con barre alte 'dimenticano' gli shock lentamente",
                                          xaxis_title="Mese", yaxis_title="Ore",
                                          legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
                    st.plotly_chart(fig_mr4, use_container_width=True)
                st.dataframe(df_mesi_mr, use_container_width=True, hide_index=True)
                st.download_button(
                    "⬇️ Esporta mean reversion mensile (CSV)",
                    df_mesi_mr.to_csv(index=False).encode("utf-8"),
                    file_name=f"mean_reversion_mensile_{d0}_{d1}.csv",
                    mime="text/csv",
                    help="Scarica AR(1), half-life e R² per mese: la mappa dei cambi di regime del mercato.",
                )
            else:
                st.info("Serie troppo corta per la scomposizione mensile (servono mesi con almeno 100 ore valide).")

    with tab43:
        titolo_sf = edu("Strip forward impliciti", "Gli STRIP FORWARD sono i contratti standard scambiati sul mercato elettrico: un 'strip mensile base' e' il prezzo medio di tutte le ore di quel mese di consegna, uno 'strip peak' la media delle ore lun-ven 8:00-20:00, 'offpeak' il resto. I broker quotano questi strip per i mesi/trimestri/anni futuri. Qui li calcoliamo sullo storico day-ahead ('impliciti'): confrontare la quotazione del broker con lo strip implicito dice se il mercato sta prezzando un premio di rischio (quotazione sopra lo storico) o uno sconto. Lo SPREAD peak-offpeak e il PREMIO peak vs base misurano quanto costa di piu' l'energia nelle ore lavorative: piu' e' alto, piu' conviene spostare i consumi (shifting) o coprire il peak separatamente.")
        st.markdown(f"**{titolo_sf}**: prezzi forward impliciti per periodo di consegna (base / peak / offpeak) calcolati sullo storico day-ahead.", unsafe_allow_html=True)

        freq_map = {"Mensile": "ME", "Trimestrale": "QE", "Annuale": "YE"}
        freq_label = st.radio("Granularita' strip", list(freq_map.keys()), horizontal=True,
                              help="Mensile = 12 strip/anno (come le quotazioni M+1, M+2...), Trimestrale = Q1-Q4, Annuale = Cal.")
        sf = calcola_strip_forward(prezzi, freq=freq_map[freq_label])
        df_sf = sf["df"]
        if len(df_sf) == 0:
            st.warning("Dati insufficienti per calcolare gli strip (serve almeno uno strip con ore valide).")
        else:
            c1, c2, c3, c4 = st.columns(4)
            prem_txt = f"{sf['premio_peak_medio']:+.1f} %" if sf["premio_peak_medio"] is not None else "n.d."
            spr_txt = f"{sf['spread_medio']:,.2f} €/MWh" if sf["spread_medio"] is not None else "n.d."
            render_kpi(edu("Strip calcolati", "Numero di periodi di consegna (mesi/trimestri/anni) con dati sufficienti nello storico."), f"{sf['n_strip']}<br><small>{sf['n_ore']:,} ore totali</small>", c1)
            render_kpi(edu("Base medio", "Media dei prezzi base di tutti gli strip: il livello medio del mercato sul periodo analizzato."), f"{sf['base_medio']:,.2f} €/MWh", c2)
            render_kpi(edu("Premio peak medio", "Quanto costa in piu' (in %) l'energia peak rispetto al base, mediato sugli strip. Un premio alto = ore lavorative molto piu' care: candidati per shifting o coperture peak."), f"{prem_txt}<br><small>peak vs base</small>", c3)
            render_kpi(edu("Spread peak-offpeak medio", "Differenza media in €/MWh tra strip peak e offpeak: il valore economico di spostare 1 MWh dalle ore di punta alle ore fuori punta."), f"{spr_txt}<br><small>per MWh spostato</small>", c4)

            try:
                fig_sf1 = go.Figure()
                fig_sf1.add_trace(go.Bar(x=df_sf["Strip"], y=df_sf["Base (€/MWh)"], name="Base",
                                         marker_color="#3b82f6",
                                         hovertemplate="%{x}<br>Base: %{y:,.2f} €/MWh<extra></extra>"))
                fig_sf1.add_trace(go.Bar(x=df_sf["Strip"], y=df_sf["Peak (€/MWh)"], name="Peak",
                                         marker_color="#ef4444",
                                         hovertemplate="%{x}<br>Peak: %{y:,.2f} €/MWh<extra></extra>"))
                fig_sf1.add_trace(go.Bar(x=df_sf["Strip"], y=df_sf["Offpeak (€/MWh)"], name="Offpeak",
                                         marker_color="#22c55e",
                                         hovertemplate="%{x}<br>Offpeak: %{y:,.2f} €/MWh<extra></extra>"))
                fig_sf1.update_layout(template="plotly_dark", height=380, barmode="group",
                                      title="Strip forward impliciti: base vs peak vs offpeak",
                                      xaxis_title="Periodo di consegna", yaxis_title="Prezzo (€/MWh)",
                                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
                st.plotly_chart(fig_sf1, use_container_width=True)
                st.caption("Confronta queste barre con le quotazioni dei broker per gli stessi periodi: quotazione sopra la barra = premio di rischio del mercato.")
            except Exception:
                st.info("Grafico strip non disponibile per questi dati.")

            try:
                df_spr = df_sf.dropna(subset=["Spread peak-offpeak (€/MWh)"])
                if len(df_spr):
                    fig_sf2 = go.Figure()
                    fig_sf2.add_trace(go.Scatter(x=df_spr["Strip"], y=df_spr["Spread peak-offpeak (€/MWh)"],
                                                 mode="lines+markers", name="Spread peak-offpeak",
                                                 line=dict(color="#f59e0b", width=2),
                                                 fill="tozeroy", fillcolor="rgba(245,158,11,0.15)",
                                                 hovertemplate="%{x}<br>Spread: %{y:,.2f} €/MWh<extra></extra>"))
                    fig_sf2.update_layout(template="plotly_dark", height=280,
                                          title="Spread peak-offpeak per strip: dove conviene di piu' lo shifting",
                                          xaxis_title="Periodo di consegna", yaxis_title="€/MWh",
                                          legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
                    st.plotly_chart(fig_sf2, use_container_width=True)
                    st.caption("Picchi dello spread = periodi in cui spostare consumi dalle ore di punta rende di piu'.")
            except Exception:
                st.info("Grafico spread non disponibile per questi dati.")

            st.dataframe(df_sf, use_container_width=True, hide_index=True)
            st.download_button(
                "⬇️ Esporta strip forward (CSV)",
                df_sf.to_csv(index=False).encode("utf-8"),
                file_name=f"strip_forward_{freq_map[freq_label].lower()}_{d0}_{d1}.csv",
                mime="text/csv",
                help="Scarica base, peak, offpeak, spread e premio per ogni strip: il benchmark per confrontare le quotazioni dei broker.",
            )

    with tab44:
        titolo_cl = edu("Climatologia del prezzo", "La CLIMATOLOGIA del prezzo e' la probabilita' (calcolata sullo storico) che il prezzo orario superi un livello critico X in una data ora del giorno e in un dato giorno della settimana. E' la misura di RISCHIO/PROBABILITA', non di intensita': risponde a 'a che ora e in che giorno e' piu' probabile che il prezzo superi il mio costo variabile / lo strike / il prezzo dell'offerta da battere?'. A differenza del tab Persistenza (che studia i BLOCCHI consecutivi sopra soglia) e di Settimana tipo (che mostra i prezzi MEDI), qui ogni cella della matrice 7x24 e' una frequenza condizionata al calendario: utile per programmare flessibilita', dispacciamento e acquisti quando il mercato e' statisticamente favorevole.")
        st.markdown(f"**{titolo_cl}**: probabilita' che il prezzo superi la soglia, per giorno della settimana e ora.", unsafe_allow_html=True)

        soglia_cl = st.slider("Soglia critica (€/MWh)", min_value=0, max_value=500, value=100, step=5,
                              help="Livello di prezzo critico: costo variabile, strike di un'opzione, prezzo dell'offerta da battere. Un'ora conta come 'sopra soglia' se prezzo >= soglia.")
        cl = calcola_climatologia_prezzo(prezzi, soglia=float(soglia_cl))
        if cl["n_ore"] == 0:
            st.warning("Dati insufficienti per calcolare la climatologia (serie vuota).")
        else:
            c1, c2, c3, c4 = st.columns(4)
            ora_txt = f"{cl['ora_picco'][0]:02d}:00 — {cl['ora_picco'][1]:.0f}%" if cl["ora_picco"] else "n.d."
            gio_txt = f"{cl['giorno_picco'][0]} — {cl['giorno_picco'][1]:.0f}%" if cl["giorno_picco"] else "n.d."
            q_txt = f"{cl['quota']*100:.1f} %" if cl["quota"] is not None else "n.d."
            render_kpi(edu("Ora piu' probabile sopra soglia", "L'ora del giorno con la piu' alta probabilita' storica di superare la soglia: l'ora in cui il mercato e' statisticamente piu' caro."), ora_txt, c1)
            render_kpi(edu("Giorno piu' probabile sopra soglia", "Il giorno della settimana con la piu' alta probabilita' media di superare la soglia."), gio_txt, c2)
            render_kpi(edu("Quota ore sopra soglia", "Frazione di tutte le ore osservate con prezzo sopra la soglia: la frequenza incondizionata dell'evento."), q_txt, c3)
            render_kpi(edu("Eccedenza attesa media", "Media su tutte le ore osservate di max(prezzo - soglia, 0): quanto, in media per ora, il prezzo eccede la soglia quando la supera. Moltiplicato per i MW, e' il margine atteso per ora."), f"{cl['eccedenza_media']:,.2f} €/MWh", c4)

            try:
                mat = cl["matrice"]
                fig_cl1 = go.Figure(data=go.Heatmap(
                    z=mat.to_numpy(), x=[f"{h:02d}" for h in range(24)], y=mat.index.tolist(),
                    colorscale="Reds", zmin=0, zmax=100,
                    colorbar=dict(title="Prob. %"),
                    hovertemplate="Giorno: %{y}<br>Ora: %{x}:00<br>Probabilita': %{z:.1f}%<extra></extra>"))
                fig_cl1.update_layout(template="plotly_dark", height=380,
                                      title=f"Climatologia: probabilita' di prezzo >= {soglia_cl} €/MWh per giorno e ora",
                                      xaxis_title="Ora del giorno", yaxis_title="Giorno della settimana")
                st.plotly_chart(fig_cl1, use_container_width=True)
                st.caption("Celle rosse scure = combinazioni giorno/ora in cui il prezzo supera la soglia quasi sempre: finestre tipicamente care (o, per chi vende, finestre di margine).")
            except Exception:
                st.info("Heatmap climatologia non disponibile per questi dati.")

            try:
                mo = cl["media_ora"].dropna()
                mg = cl["media_giorno"].dropna()
                fig_cl2 = go.Figure()
                if len(mo):
                    fig_cl2.add_trace(go.Bar(x=mo["Ora"], y=mo["Probabilita' (%)"], name="Per ora",
                                             marker_color="#f59e0b",
                                             hovertemplate="Ora: %{x}<br>Probabilita': %{y:.1f}%<extra></extra>"))
                fig_cl2.update_layout(template="plotly_dark", height=300,
                                      title="Profilo orario: probabilita' sopra soglia per ora del giorno",
                                      xaxis_title="Ora", yaxis_title="Probabilita' (%)")
                st.plotly_chart(fig_cl2, use_container_width=True)
                if len(mg):
                    fig_cl3 = go.Figure()
                    fig_cl3.add_trace(go.Bar(x=mg["Giorno"], y=mg["Probabilita' (%)"], name="Per giorno",
                                             marker_color="#3b82f6",
                                             hovertemplate="Giorno: %{x}<br>Probabilita': %{y:.1f}%<extra></extra>"))
                    fig_cl3.update_layout(template="plotly_dark", height=300,
                                          title="Profilo settimanale: probabilita' sopra soglia per giorno",
                                          xaxis_title="Giorno", yaxis_title="Probabilita' (%)")
                    st.plotly_chart(fig_cl3, use_container_width=True)
            except Exception:
                st.info("Profili climatologia non disponibili per questi dati.")

            if cl["ore_p50"] is not None:
                st.markdown(f"**{cl['ore_p50']}** combinazioni giorno/ora hanno probabilita' >= 50% di superare la soglia.")
            df_cl_top = cl["top_celle"]
            if len(df_cl_top):
                st.markdown("**Top 20 combinazioni giorno/ora piu' probabili sopra soglia**")
                st.dataframe(df_cl_top, use_container_width=True, hide_index=True)
                st.download_button(
                    "⬇️ Esporta climatologia (CSV)",
                    df_cl_top.to_csv(index=False).encode("utf-8"),
                    file_name=f"climatologia_prezzo_{soglia_cl}_{d0}_{d1}.csv",
                    mime="text/csv",
                    help="Scarica le 20 combinazioni giorno/ora con la piu' alta probabilita' di superare la soglia.",
                )

    with tab45:
        titolo_sp = edu("Stabilità del profilo orario", "La STABILITA' DEL PROFILO misura quanto la FORMA della giornata tipo (il profilo medio delle 24 ore) resta uguale da un mese all'altro: per ogni mese si calcola il prezzo medio per ora del giorno e si misura la correlazione di Pearson tra i profili mensili. Correlazione vicina a 1 = la sagoma oraria non cambia (shaping, fasce time-of-use e coperture sagomate restano validi); correlazione che crolla = il profilo sta cambiando (stagionalità forte o cambi strutturali) e le strategie sagomate vanno ricalibrate. Nota: la correlazione ignora il LIVELLO dei prezzi — due mesi con livelli diversi ma stessa forma danno correlazione ~1. A differenza di 'Settimana tipo' e 'Stagionalità' (che mostrano i profili medi) e di 'Autocorrelazione' (persistenza ora-su-ora), qui la domanda è: 'la giornata tipo di domani avrà la stessa forma di quella di ieri?'.")
        st.markdown(f"**{titolo_sp}**: quanto la forma della giornata tipo resta stabile tra i mesi (correlazione dei profili orari medi mensili).", unsafe_allow_html=True)

        sp_min_ore = st.slider("Ore minime osservate per mese", min_value=100, max_value=720, value=360, step=20, key="sp45_min_ore",
                               help="Un mese entra nel confronto solo se ha almeno queste ore osservate (720 = mese intero). Mesi con ore mancanti in qualche fascia oraria o con profilo piatto sono esclusi comunque.")
        sp = calcola_stabilita_profilo(prezzi, min_ore_mese=int(sp_min_ore))
        if sp["n_mesi"] < 2:
            st.warning("Servono almeno 2 mesi con dati sufficienti per misurare la stabilità del profilo (aumenta il periodo o abbassa la soglia di ore minime).")
        else:
            c1, c2, c3, c4 = st.columns(4)
            render_kpi(edu("Correlazione media tra mesi", "Media delle correlazioni di Pearson tra i profili orari medi dei mesi: vicina a 1 = la forma della giornata tipo è stabile nel tempo, le strategie di shaping restano valide."), f"{sp['corr_media']:.3f}<br><small>Pearson sui profili 24h</small>", c1)
            cm1, cm2 = sp["coppia_min"]
            render_kpi(edu("Coppia meno correlata", "I due mesi con i profili orari più diversi tra loro: il punto di rottura della stabilità. Se la correlazione è bassa, il profilo è cambiato proprio tra questi due mesi."), f"{sp['corr_min']:.3f}<br><small>{cm1} vs {cm2}</small>", c2)
            render_kpi(edu("Mese più anomalo", "Il mese il cui profilo orario è in media più diverso da tutti gli altri: il candidato da analizzare per capire cosa è cambiato (stagione, mix, prezzi)."), f"{sp['mese_anomalo']}<br><small>profilo più diverso</small>", c3)
            render_kpi(edu("Deriva ora di picco", "Distanza in ore tra l'ora di picco più anticipata e quella più ritardata tra i mesi: dice se il momento più caro della giornata si sta spostando."), f"{sp['deriva_picco_ore']} ore<br><small>max-min ora di picco</small>", c4)

            try:
                C = sp["corr"]
                zmin_sp = min(0.0, float(sp["corr_min"]))
                fig_sp1 = go.Figure(data=go.Heatmap(
                    z=C.to_numpy(), x=C.columns.tolist(), y=C.index.tolist(),
                    colorscale="RdYlGn", zmin=zmin_sp, zmax=1.0,
                    colorbar=dict(title="Correlazione"),
                    hovertemplate="Mese: %{y} vs %{x}<br>Correlazione: %{z:.3f}<extra></extra>"))
                fig_sp1.update_layout(template="plotly_dark", height=420,
                                      title="Stabilità del profilo: correlazione tra i profili orari medi mensili",
                                      xaxis_title="Mese", yaxis_title="Mese")
                st.plotly_chart(fig_sp1, use_container_width=True)
                st.caption("Verde = mesi con la stessa forma di giornata tipo; celle gialle/rosse = il profilo è cambiato tra quei due mesi.")
            except Exception:
                st.info("Heatmap di correlazione non disponibile per questi dati.")

            try:
                P = sp["profili"]
                fig_sp2 = go.Figure()
                for mm in P.index:
                    fig_sp2.add_trace(go.Scatter(x=[f"{h:02d}:00" for h in range(24)], y=P.loc[mm].to_numpy(),
                                                 mode="lines+markers", name=str(mm),
                                                 hovertemplate="Ora: %{x}<br>Prezzo medio: %{y:,.2f} €/MWh<extra></extra>"))
                fig_sp2.update_layout(template="plotly_dark", height=360,
                                      title="Profili orari medi per mese (€/MWh)",
                                      xaxis_title="Ora del giorno", yaxis_title="€/MWh",
                                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
                st.plotly_chart(fig_sp2, use_container_width=True)
                st.caption("Se le curve si sovrappongono, la forma della giornata è stabile; curve che si discostano segnalano i mesi anomali.")
            except Exception:
                st.info("Profili mensili non disponibili per questi dati.")

            try:
                df_pk = sp["ora_picco"]
                ore_num = [int(str(x).split(":")[0]) for x in df_pk["Ora di picco"]]
                fig_sp3 = go.Figure()
                fig_sp3.add_trace(go.Bar(x=df_pk["Mese"], y=ore_num, marker_color="#f59e0b",
                                         hovertemplate="Mese: %{x}<br>Ora di picco: %{y}:00<extra></extra>"))
                fig_sp3.update_layout(template="plotly_dark", height=300,
                                      title="Ora di picco del prezzo medio per mese",
                                      xaxis_title="Mese", yaxis_title="Ora di picco")
                st.plotly_chart(fig_sp3, use_container_width=True)
            except Exception:
                st.info("Grafico ora di picco non disponibile per questi dati.")

            df_sp = sp["df_export"]
            if len(df_sp):
                st.markdown("**Ora di picco e prezzo medio per mese**")
                st.dataframe(df_sp, use_container_width=True, hide_index=True)
                st.download_button(
                    "⬇️ Esporta stabilità profilo (CSV)",
                    df_sp.to_csv(index=False).encode("utf-8"),
                    file_name=f"stabilita_profilo_{d0}_{d1}.csv",
                    mime="text/csv",
                    help="Scarica ora di picco, prezzo medio e ore osservate per mese.",
                )

    with tab46:
        titolo_fi = edu("Fisso vs indicizzato", "Confronta sul periodo selezionato il COSTO di un contratto a PREZZO FISSO (totale o parziale, con spread sul lato indicizzato) contro l'acquisto INDICIZZATO allo spot. Il helper calcola il break-even — il prezzo fisso massimo che batterebbe ancora lo spot — e il delta mese per mese e cumulato nel tempo. Diverso dalla tab 'Costo fornitura', dove la tariffa flat è un semplice delta totale: qui decidi QUANTA quota comprare a fisso e vedi QUANDO il contratto vince o perde.")
        st.markdown(f"**{titolo_fi}**: contratto a prezzo fisso (anche parziale) contro indicizzato spot sul tuo profilo F1/F2/F3.", unsafe_allow_html=True)

        fi1, fi2, fi3, fi4 = st.columns(4)
        with fi1:
            fi_prezzo = st.number_input("Prezzo fisso offerto (€/MWh)", min_value=0.0, value=100.0, step=1.0,
                                        key="fi46_prezzo",
                                        help="Prezzo fisso tutto incluso dell'offerta del fornitore (€/MWh).")
        with fi2:
            fi_spread = st.number_input("Spread indicizzato (€/MWh)", min_value=0.0, value=3.0, step=0.5,
                                        key="fi46_spread",
                                        help="Margine del fornitore sopra lo spot se resti indicizzato (es. 2-5 €/MWh).")
        with fi3:
            fi_quota = st.slider("Quota coperta a fisso (%)", min_value=0, max_value=100, value=100, step=5,
                                 key="fi46_quota",
                                 help="100% = tutto il profilo a prezzo fisso; meno di 100% = copertura parziale (hedging).")
        with fi4:
            st.markdown("<div style='padding-top: 28px;'></div>", unsafe_allow_html=True)
            st.caption(f"Profilo: F1 {float(mw_f1):.1f} MW, F2 {float(mw_f2):.1f} MW, F3 {float(mw_f3):.1f} MW — imposti le potenze nella tab 💰 Costo fornitura.")

        fi = calcola_confronto_fisso_indicizzato(prezzi, mw_f1, mw_f2, mw_f3, fi_prezzo,
                                                spread_indicizzato=fi_spread, quota_fissa=fi_quota / 100.0)
        if fi["mwh"] == 0:
            st.warning("Imposta una potenza maggiore di zero in almeno una fascia (tab 💰 Costo fornitura) per calcolare il confronto.")
        else:
            seg_fi = "🟢" if fi["risparmio"] > 0 else ("🔴" if fi["risparmio"] < 0 else "⚪")
            pct_fi = fi["risparmio_pct"]
            pct_txt = f" ({pct_fi:+.1f} %)" if pct_fi is not None else ""
            c1, c2, c3, c4 = st.columns(4)
            render_kpi(edu("Costo indicizzato totale", "Quanto costerebbe il profilo comprando tutto allo spot (più spread) nel periodo selezionato."), f"{fi['totale_indicizzato']:,.0f} €", c1)
            render_kpi(edu("Costo contratto (fisso + indicizzato)", "Costo totale con la quota coperta a fisso e il resto indicizzato allo spot."), f"{fi['totale_blended']:,.0f} €", c2)
            render_kpi(edu(f"{seg_fi} Risparmio del contratto", "Differenza indicizzato meno contratto: positivo = il contratto fa risparmiare; negativo = conviene restare indicizzati."), f"{fi['risparmio']:+,.0f} €{pct_txt}", c3)
            render_kpi(edu("Break-even del fisso", "Il prezzo fisso massimo che pareggerebbe l'indicizzato: se l'offerta è sotto questo valore, il fisso vince; se sopra, conviene l'indicizzato."), f"{fi['break_even']:,.2f} €/MWh", c4)
            st.caption(f"Energia {fi['mwh']:,.0f} MWh — prezzo medio ponderato indicizzato (spread incluso): {fi['pmp_indicizzato']:,.2f} €/MWh; "
                       f"contratto blended: {fi['pmp_blended']:,.2f} €/MWh. "
                       f"Spot+spread sotto il fisso in {fi['quota_ore_sotto']*100:.1f}% delle ore.")
            if fi["mese_peggiore"] is not None:
                mm, dv = fi["mese_peggiore"]
                st.caption(f"Mese peggiore per il contratto: {mm} (+{dv:,.0f} € vs indicizzato).")

            try:
                df_g = fi["df_giorni"]
                fig_fi1 = go.Figure()
                fig_fi1.add_trace(go.Scatter(x=df_g["Giorno"], y=df_g["Delta cumulato contratto-indicizzato (€)"],
                                             mode="lines", name="Delta cumulato",
                                             fill="tozeroy",
                                             hovertemplate="Giorno: %{x}<br>Delta cumulato: %{y:,.0f} €<extra></extra>"))
                fig_fi1.update_layout(template="plotly_dark", height=340,
                                      title="Delta cumulato contratto vs indicizzato (sopra lo zero = il contratto costa di più)",
                                      xaxis_title="Giorno", yaxis_title="€ cumulati")
                fig_fi1.add_hline(y=0, line_dash="dash", line_color="gray")
                st.plotly_chart(fig_fi1, use_container_width=True)
                st.caption("Curva che sale = nel periodo il fisso sta perdendo contro lo spot; curva che scende = il fisso sta vincendo. Il valore finale è il risparmio (negato).")
            except Exception:
                st.info("Curva cumulata non disponibile per questi dati.")

            try:
                df_m = fi["df_mesi"]
                colori = ["#22c55e" if v < 0 else "#ef4444" for v in df_m["Delta contratto-indicizzato (€)"]]
                fig_fi2 = go.Figure()
                fig_fi2.add_trace(go.Bar(x=df_m["Mese"], y=df_m["Delta contratto-indicizzato (€)"],
                                         marker_color=colori,
                                         hovertemplate="Mese: %{x}<br>Delta: %{y:,.0f} €<extra></extra>"))
                fig_fi2.update_layout(template="plotly_dark", height=300,
                                      title="Delta mensile contratto − indicizzato (verde = il contratto risparmia)",
                                      xaxis_title="Mese", yaxis_title="€")
                st.plotly_chart(fig_fi2, use_container_width=True)
            except Exception:
                st.info("Grafico mensile non disponibile per questi dati.")

            try:
                spot_fi = prezzi.dropna()
                fig_fi3 = go.Figure()
                fig_fi3.add_trace(go.Histogram(x=spot_fi.values, nbinsx=60, name="Ore spot",
                                                hovertemplate="Prezzo: %{x:,.0f} €/MWh<br>Ore: %{y}<extra></extra>"))
                fig_fi3.add_vline(x=fi_prezzo, line_dash="dash", line_color="#f59e0b",
                                  annotation_text=f"Fisso {fi_prezzo:.0f} €/MWh", annotation_position="top right")
                if fi["pmp_indicizzato"] is not None:
                    fig_fi3.add_vline(x=fi["pmp_indicizzato"], line_dash="dash", line_color="#3B82F6",
                                      annotation_text=f"PMP indicizzato {fi['pmp_indicizzato']:.0f} €/MWh",
                                      annotation_position="top left")
                fig_fi3.update_layout(template="plotly_dark", height=320,
                                      title="Distribuzione dei prezzi spot orari vs prezzo fisso",
                                      xaxis_title="€/MWh", yaxis_title="Ore")
                st.plotly_chart(fig_fi3, use_container_width=True)
                st.caption("Se la massa dell'istogramma sta a sinistra della linea arancione, lo spot batte spesso il fisso (e viceversa).")
            except Exception:
                st.info("Istogramma non disponibile per questi dati.")

            df_fi = fi["df_mesi"]
            if len(df_fi):
                st.markdown("**Dettaglio mensile**")
                st.dataframe(df_fi, use_container_width=True, hide_index=True)
                st.download_button(
                    "⬇️ Esporta fisso vs indicizzato (CSV)",
                    df_fi.to_csv(index=False).encode("utf-8"),
                    file_name=f"fisso_vs_indicizzato_{d0}_{d1}.csv",
                    mime="text/csv",
                    help="Scarica il confronto mensile fisso vs indicizzato.",
                )

    with tab47:
        titolo_cf = edu("Cap & Floor", "Prezza una PROTEZIONE sul prezzo spot: un CAP a strike K (se lo spot+spread supera K, paghi K) e/o un FLOOR a strike F (se scende sotto F, paghi F). Il helper calcola il PREMIO EQUO in €/MWh sul tuo profilo F1/F2/F3 come media storica del payoff orario — è il prezzo che il fornitore dovrebbe chiedere per la protezione: utile per negoziare lo strike o decidere se accettare il premio offerto. Diverso dalla tab 'Fisso vs indicizzato' (confronto tra due prezzi di acquisto) e da 'Valore flessibilità' (taglio fisico del carico): qui non cambi né prezzo base né consumi, compri solo un'assicurazione sul prezzo.")
        st.markdown(f"**{titolo_cf}**: premio equo di cap/floor sul profilo di carico (approccio attuariale sui prezzi storici).", unsafe_allow_html=True)

        cf0, cf1, cf2, cf3, cf4 = st.columns(5)
        with cf0:
            cf_cap_on = st.checkbox("CAP attivo", value=True, key="cf47_cap_on",
                                    help="Protezione contro i picchi: se lo spot+spread supera lo strike del cap, paghi lo strike.")
        with cf1:
            cf_cap = st.number_input("Strike cap (€/MWh)", min_value=0.0, value=120.0, step=5.0,
                                     key="cf47_cap", disabled=not cf_cap_on,
                                     help="Prezzo massimo che pagheresti con la protezione cap.")
        with cf2:
            cf_flr_on = st.checkbox("FLOOR attivo", value=False, key="cf47_flr_on",
                                    help="Protezione contro i crolli (utile se rivendi energia): se lo spot+spread scende sotto lo strike del floor, paghi lo strike.")
        with cf3:
            cf_flr = st.number_input("Strike floor (€/MWh)", min_value=0.0, value=40.0, step=5.0,
                                     key="cf47_flr", disabled=not cf_flr_on,
                                     help="Prezzo minimo garantito con la protezione floor.")
        with cf4:
            cf_spread = st.number_input("Spread sopra lo spot (€/MWh)", min_value=0.0, value=3.0, step=0.5,
                                        key="cf47_spread",
                                        help="Margine del fornitore sopra lo spot, incluso nel prezzo su cui scatta la protezione.")

        cf = calcola_valutazione_cap_floor(prezzi, mw_f1, mw_f2, mw_f3,
                                           cap_strike=cf_cap if cf_cap_on else None,
                                           floor_strike=cf_flr if cf_flr_on else None,
                                           spread=cf_spread)
        if cf["errore"]:
            st.warning(f"⚠️ {cf['errore']}")
        elif cf["mwh"] == 0:
            st.warning("Imposta una potenza maggiore di zero in almeno una fascia (tab 💰 Costo fornitura) per valutare le protezioni.")
        else:
            def _fmt_cf(v, fmt):
                return fmt.format(v) if v is not None else "—"
            k1, k2, k3, k4 = st.columns(4)
            render_kpi(edu("Premio equo CAP", "Quanto dovrebbe costare il cap in €/MWh sul tuo profilo: media storica del payoff orario. Se il fornitore chiede di più, la protezione è cara; se chiede di meno, è un affare."),
                       _fmt_cf(cf["premio_cap_eur_mwh"], "{:,.2f} €/MWh"), k1)
            render_kpi(edu("Premio equo FLOOR", "Quanto dovrebbe costare il floor in €/MWh sul tuo profilo: media storica del payoff orario."),
                       _fmt_cf(cf["premio_floor_eur_mwh"], "{:,.2f} €/MWh"), k2)
            tot_pay = (cf["premio_cap_tot_eur"] or 0.0) + (cf["premio_floor_tot_eur"] or 0.0)
            render_kpi(edu("Payoff totale nel periodo", "Somma dei payoff che le protezioni avrebbero pagato nel periodo selezionato: è il premio equo totale in euro."),
                       f"{tot_pay:,.0f} €", k3)
            ore_ex = []
            if cf["ore_cap_pct"] is not None:
                ore_ex.append(f"cap {cf['ore_cap_pct']*100:.1f}%")
            if cf["ore_floor_pct"] is not None:
                ore_ex.append(f"floor {cf['ore_floor_pct']*100:.1f}%")
            render_kpi(edu("Ore con esercizio", "Quota di ore in cui la protezione è scattata (payoff > 0)."),
                       ", ".join(ore_ex) if ore_ex else "—", k4)
            st.caption(f"Energia {cf['mwh']:,.0f} MWh — costo netto protetto (spot+spread meno payoff): {cf['costo_netto_protetto']:,.0f} €. "
                       f"Payoff medio per ora esercitata: cap {_fmt_cf(cf['payout_medio_ora_cap'], '{:,.0f} €/h')}, "
                       f"floor {_fmt_cf(cf['payout_medio_ora_floor'], '{:,.0f} €/h')}.")
            if cf["mese_max_cap"] is not None:
                mm, pv = cf["mese_max_cap"]
                st.caption(f"Mese con il payoff cap più alto: {mm} ({pv:,.0f} €).")

            try:
                spot_cf = (prezzi.dropna() + cf_spread).values
                fig_cf1 = go.Figure()
                fig_cf1.add_trace(go.Histogram(x=spot_cf, nbinsx=60, name="Ore (spot+spread)",
                                               hovertemplate="Prezzo: %{x:,.0f} €/MWh<br>Ore: %{y}<extra></extra>"))
                if cf_cap_on:
                    fig_cf1.add_vline(x=cf_cap, line_dash="dash", line_color="#ef4444",
                                      annotation_text=f"Cap {cf_cap:.0f} €/MWh", annotation_position="top right")
                if cf_flr_on:
                    fig_cf1.add_vline(x=cf_flr, line_dash="dash", line_color="#22c55e",
                                      annotation_text=f"Floor {cf_flr:.0f} €/MWh", annotation_position="top left")
                fig_cf1.update_layout(template="plotly_dark", height=320,
                                      title="Distribuzione dei prezzi orari (spot+spread) vs strike",
                                      xaxis_title="€/MWh", yaxis_title="Ore")
                st.plotly_chart(fig_cf1, use_container_width=True)
                st.caption("La coda a destra della linea rossa è ciò che il cap taglia; la coda a sinistra della linea verde è ciò che il floor rialza.")
            except Exception:
                st.info("Istogramma non disponibile per questi dati.")

            try:
                df_cm = cf["df_mesi"]
                fig_cf2 = go.Figure()
                if cf_cap_on:
                    fig_cf2.add_trace(go.Bar(x=df_cm["Mese"], y=df_cm["Payout cap (€)"],
                                             name="Payout cap", marker_color="#ef4444",
                                             hovertemplate="Mese: %{x}<br>Payout cap: %{y:,.0f} €<extra></extra>"))
                if cf_flr_on:
                    fig_cf2.add_trace(go.Bar(x=df_cm["Mese"], y=df_cm["Payout floor (€)"],
                                             name="Payout floor", marker_color="#22c55e",
                                             hovertemplate="Mese: %{x}<br>Payout floor: %{y:,.0f} €<extra></extra>"))
                fig_cf2.update_layout(template="plotly_dark", height=300, barmode="group",
                                      title="Payoff mensile delle protezioni (dove il premio equo si concentra)",
                                      xaxis_title="Mese", yaxis_title="€")
                st.plotly_chart(fig_cf2, use_container_width=True)
            except Exception:
                st.info("Grafico mensile non disponibile per questi dati.")

            try:
                df_cg = cf["df_giorni"]
                fig_cf3 = go.Figure()
                if cf_cap_on:
                    fig_cf3.add_trace(go.Scatter(x=df_cg["Giorno"], y=df_cg["Payout cap cumulato (€)"],
                                                 mode="lines", name="Cap cumulato", fill="tozeroy",
                                                 hovertemplate="Giorno: %{x}<br>Cap cumulato: %{y:,.0f} €<extra></extra>"))
                if cf_flr_on:
                    fig_cf3.add_trace(go.Scatter(x=df_cg["Giorno"], y=df_cg["Payout floor cumulato (€)"],
                                                 mode="lines", name="Floor cumulato", fill="tozeroy",
                                                 hovertemplate="Giorno: %{x}<br>Floor cumulato: %{y:,.0f} €<extra></extra>"))
                fig_cf3.update_layout(template="plotly_dark", height=300,
                                      title="Payoff cumulato nel tempo (il valore finale è il premio equo totale)",
                                      xaxis_title="Giorno", yaxis_title="€ cumulati")
                st.plotly_chart(fig_cf3, use_container_width=True)
            except Exception:
                st.info("Curva cumulata non disponibile per questi dati.")

            df_cf = cf["df_mesi"]
            if len(df_cf):
                st.markdown("**Dettaglio mensile**")
                st.dataframe(df_cf, use_container_width=True, hide_index=True)
                st.download_button(
                    "⬇️ Esporta cap & floor (CSV)",
                    df_cf.to_csv(index=False).encode("utf-8"),
                    file_name=f"cap_floor_{d0}_{d1}.csv",
                    mime="text/csv",
                    help="Scarica il payoff mensile di cap e floor.",
                )

    with tab48:
        titolo_bo = edu("Stima bolletta", "Ricostruzione STIMATA della bolletta elettrica italiana per una fornitura a prezzo indicizzato: parte dal costo della materia energia (spot x profilo F1/F2/F3) e aggiunge tutte le voci parafiscali — perdite di rete, dispacciamento, PCV, oneri di sistema, accisa e IVA. Serve a rispondere alla domanda \"quanto pago davvero?\": la materia energia e' spesso meno della meta' del totale. Diverso dalla tab 'Costo fornitura' (solo energia) e da 'Fisso vs indicizzato' (confronto di prezzi di acquisto): qui si sommano i costi che il fornitore gira in fattura oltre l'energia.")
        st.markdown(f"**{titolo_bo}**: dalla materia energia al totale fattura, con tutte le voci della bolletta italiana.", unsafe_allow_html=True)

        b0, b1, b2 = st.columns(3)
        with b0:
            bo_perd = st.number_input("Perdite di rete (% su energia)", min_value=0.0, value=10.4, step=0.1,
                                     key="bo48_perd",
                                     help="Perdite di rete: 10.4 % per la bassa tensione, 3.8 % media, 2.0 % alta.")
        with b1:
            bo_disp = st.number_input("Dispacciamento (€/MWh)", min_value=0.0, value=4.0, step=0.5,
                                     key="bo48_disp",
                                     help="Corrispettivi di dispacciamento (Terna) e sbilanciamento effettivo.")
        with b2:
            bo_pcv = st.number_input("PCV (€/mese)", min_value=0.0, value=11.0, step=1.0,
                                    key="bo48_pcv",
                                    help="Prezzo commercializzazione vendita: quota fissa mensile del fornitore.")
        b3, b4, b5 = st.columns(3)
        with b3:
            bo_oneri = st.number_input("Oneri di sistema (€/MWh)", min_value=0.0, value=14.0, step=1.0,
                                      key="bo48_oneri",
                                      help="Oneri generali di sistema (ASOS, ARIM e altre componenti parafiscali).")
        with b4:
            bo_acc = st.number_input("Accisa (€/MWh)", min_value=0.0, value=22.7, step=0.1,
                                    key="bo48_acc",
                                    help="Accisa sull'energia elettrica: 22.7 €/MWh = 0.0227 €/kWh (usi non agevolati).")
        with b5:
            bo_iva = st.number_input("IVA (%)", min_value=0.0, value=22.0, step=1.0,
                                    key="bo48_iva",
                                    help="IVA sull'imponibile: 22 % standard, 10 % per usi domestici agevolati.")

        bo = calcola_stima_bolletta(prezzi, mw_f1, mw_f2, mw_f3,
                                    perdite_pct=bo_perd, dispacciamento=bo_disp, pcv_mese=bo_pcv,
                                    oneri=bo_oneri, accisa=bo_acc, iva_pct=bo_iva)
        if bo["errore"]:
            st.warning(f"⚠️ {bo['errore']}")
        elif bo["mwh"] == 0:
            st.warning("Imposta una potenza maggiore di zero in almeno una fascia (tab 💰 Costo fornitura) per stimare la bolletta.")
        else:
            k1, k2, k3, k4 = st.columns(4)
            render_kpi(edu("Totale bolletta stimata", "Quanto pagheresti in totale nel periodo: energia + tutte le voci parafiscali + IVA."),
                       f"{bo['totale_eur']:,.0f} €", k1)
            render_kpi(edu("€/MWh all-in", "Costo medio per MWh consumato includendo tutto: e' il numero da confrontare con le offerte dei fornitori."),
                       f"{bo['eur_mwh_allin']:,.2f} €/MWh", k2)
            render_kpi(edu("Quota materia energia", "Percentuale del totale che e' vera energia: il resto sono oneri, accise e IVA."),
                       f"{bo['quota_energia_pct']*100:.1f} %" if bo["quota_energia_pct"] is not None else "—", k3)
            render_kpi(edu("Extra oltre l'energia", "Euro in piu' rispetto al solo costo della materia energia: misura il peso della parafiscalita'."),
                       f"{bo['extra_vs_energia']:,.0f} €", k4)
            st.caption(f"Energia {bo['mwh']:,.0f} MWh in {bo['n_mesi']} mesi — materia energia {bo['energia_eur']:,.0f} €, "
                       f"perdite {bo['perdite_eur']:,.0f} €, dispacciamento {bo['disp_eur']:,.0f} €, PCV {bo['pcv_eur']:,.0f} €, "
                       f"oneri {bo['oneri_eur']:,.0f} €, accisa {bo['accisa_eur']:,.0f} €, IVA {bo['iva_eur']:,.0f} €.")

            voci = [("Energia (€)", "#3b82f6"), ("Perdite (€)", "#f59e0b"),
                    ("Dispacciamento (€)", "#a855f7"), ("PCV (€)", "#64748b"),
                    ("Oneri (€)", "#ef4444"), ("Accisa (€)", "#ec4899"), ("IVA (€)", "#22c55e")]
            try:
                df_bm = bo["df_mesi"]
                fig_bo1 = go.Figure()
                for col_voce, colore in voci:
                    fig_bo1.add_trace(go.Bar(x=df_bm["Mese"], y=df_bm[col_voce], name=col_voce.replace(" (€)", ""),
                                             marker_color=colore,
                                             hovertemplate="Mese: %{x}<br>%{fullData.name}: %{y:,.0f} €<extra></extra>"))
                fig_bo1.update_layout(template="plotly_dark", height=340, barmode="stack",
                                      title="Bolletta mensile per voce (stacked)",
                                      xaxis_title="Mese", yaxis_title="€")
                st.plotly_chart(fig_bo1, use_container_width=True)
                st.caption("La parte blu e' la materia energia: tutto il resto e' parafiscalita' e IVA.")
            except Exception:
                st.info("Grafico mensile non disponibile per questi dati.")

            try:
                tot_voci = [(n.replace(" (€)", ""), bo[{"Energia (€)": "energia_eur", "Perdite (€)": "perdite_eur",
                                                       "Dispacciamento (€)": "disp_eur", "PCV (€)": "pcv_eur",
                                                       "Oneri (€)": "oneri_eur", "Accisa (€)": "accisa_eur",
                                                       "IVA (€)": "iva_eur"}[c]]) for c, n in voci]
                fig_bo2 = go.Figure(data=[go.Pie(labels=[t[0] for t in tot_voci], values=[t[1] for t in tot_voci],
                                                 hole=0.45, hovertemplate="%{label}: %{value:,.0f} € (%{percent})<extra></extra>")])
                fig_bo2.update_layout(template="plotly_dark", height=340,
                                      title="Ripartizione del totale per voce")
                st.plotly_chart(fig_bo2, use_container_width=True)
            except Exception:
                st.info("Ripartizione non disponibile per questi dati.")

            try:
                df_bg = bo["df_giorni"]
                fig_bo3 = go.Figure()
                fig_bo3.add_trace(go.Scatter(x=df_bg["Giorno"], y=df_bg["Energia cumulata (€)"],
                                             mode="lines", name="Energia cumulata",
                                             line=dict(color="#3b82f6"),
                                             hovertemplate="Giorno: %{x}<br>Energia: %{y:,.0f} €<extra></extra>"))
                fig_bo3.add_trace(go.Scatter(x=df_bg["Giorno"], y=df_bg["Totale cumulato (€)"],
                                             mode="lines", name="Bolletta cumulata", fill="tozeroy",
                                             line=dict(color="#22c55e"),
                                             hovertemplate="Giorno: %{x}<br>Totale: %{y:,.0f} €<extra></extra>"))
                fig_bo3.update_layout(template="plotly_dark", height=300,
                                      title="Cumulata nel tempo: energia vs bolletta totale",
                                      xaxis_title="Giorno", yaxis_title="€ cumulati")
                st.plotly_chart(fig_bo3, use_container_width=True)
                st.caption("La distanza tra le due curve e' il costo della parafiscalita' accumulato giorno per giorno.")
            except Exception:
                st.info("Curva cumulata non disponibile per questi dati.")

            df_bo = bo["df_mesi"]
            if len(df_bo):
                st.markdown("**Dettaglio mensile**")
                st.dataframe(df_bo, use_container_width=True, hide_index=True)
                st.download_button(
                    "⬇️ Esporta stima bolletta (CSV)",
                    df_bo.to_csv(index=False).encode("utf-8"),
                    file_name=f"stima_bolletta_{d0}_{d1}.csv",
                    mime="text/csv",
                    help="Scarica il dettaglio mensile della bolletta stimata.",
                )

    with tab49:
        titolo_mf = edu("Margine fornitore", "Margine IMPLICITO del fornitore su un'offerta a prezzo fisso: il ricavo dell'offerta meno il costo all-in stimato (spot ponderato sul tuo profilo F1/F2/F3 + spread + perdite, dispacciamento e oneri). Prospettiva del venditore, utile per negoziare: se il margine implicito e' alto, c'e' spazio per trattare. Diverso dalla tab 'Fisso vs indicizzato' (scelta del compratore) e da 'Stima bolletta' (totale fattura con IVA).")
        st.markdown(f"**{titolo_mf}**: quanto guadagna il fornitore sulla tua offerta a prezzo fisso.", unsafe_allow_html=True)

        m0, m1, m2 = st.columns(3)
        with m0:
            mf_prezzo = st.number_input("Prezzo offerta fornitore (€/MWh)", min_value=0.0, value=135.0, step=1.0,
                                        key="mf49_prezzo",
                                        help="Prezzo fisso offerto dal fornitore per tutta la fornitura.")
        with m1:
            mf_spread = st.number_input("Spread di acquisto (€/MWh)", min_value=0.0, value=2.0, step=0.5,
                                        key="mf49_spread",
                                        help="Markup che il fornitore paga sopra lo spot per approvvigionarsi.")
        with m2:
            mf_perd = st.number_input("Perdite di rete (% su energia)", min_value=0.0, value=0.0, step=0.1,
                                      key="mf49_perd",
                                      help="0 % se le perdite sono gia' incluse nel prezzo offerto; 10.4 % se la fornitura e' in bassa tensione e scorporate.")
        m3, m4 = st.columns(2)
        with m3:
            mf_disp = st.number_input("Dispacciamento (€/MWh)", min_value=0.0, value=4.0, step=0.5,
                                      key="mf49_disp",
                                      help="Corrispettivi di dispacciamento che il fornitore sostiene.")
        with m4:
            mf_oneri = st.number_input("Oneri di sistema (€/MWh)", min_value=0.0, value=14.0, step=1.0,
                                       key="mf49_oneri",
                                       help="Oneri generali di sistema a carico del fornitore sulla componente energia.")

        mf = calcola_margine_fornitore(prezzi, mw_f1, mw_f2, mw_f3, mf_prezzo,
                                       spread=mf_spread, perdite_pct=mf_perd,
                                       dispacciamento=mf_disp, oneri=mf_oneri)
        if mf["errore"]:
            st.warning(f"\u26a0\ufe0f {mf['errore']}")
        elif mf["mwh"] == 0:
            st.warning("Imposta una potenza maggiore di zero in almeno una fascia (tab \U0001F4B0 Costo fornitura) per calcolare il margine.")
        else:
            k1, k2, k3, k4 = st.columns(4)
            render_kpi(edu("Margine fornitore", "Quanto resta al fornitore per ogni MWh venduto: ricavo offerta meno costo all-in stimato."),
                       f"{mf['margine_eur_mwh']:,.2f} \u20ac/MWh" if mf["margine_eur_mwh"] is not None else "\u2014", k1)
            render_kpi(edu("Margine % sull'offerta", "Percentuale del prezzo offerto che e' margine del fornitore: misura il tuo spazio di trattativa."),
                       f"{mf['margine_pct']*100:.1f} %" if mf["margine_pct"] is not None else "\u2014", k2)
            render_kpi(edu("Margine totale", "Euro di margine implicito del fornitore sul periodo, ai tuoi volumi: quanto paghi sopra il costo stimato."),
                       f"{mf['margine_eur']:,.0f} \u20ac", k3)
            render_kpi(edu("Prezzo di pareggio", "Prezzo offerta a margine zero: sotto questo livello il fornitore ci rimette. E' il tuo obiettivo di trattativa."),
                       f"{mf['pareggio_eur_mwh']:,.2f} \u20ac/MWh" if mf["pareggio_eur_mwh"] is not None else "\u2014", k4)
            st.caption(f"{mf['mwh']:,.0f} MWh in {mf['n_mesi']} mesi — costo energia {mf['costo_energia_eur']:,.0f} \u20ac, "
                       f"costo totale {mf['costo_tot_eur']:,.0f} \u20ac, ricavo offerta {mf['ricavo_offerta_eur']:,.0f} \u20ac.")

            try:
                df_mm = mf["df_mesi"]
                fig_mf1 = go.Figure()
                fig_mf1.add_trace(go.Bar(x=df_mm["Mese"], y=df_mm["Costo totale (\u20ac)"], name="Costo totale",
                                         marker_color="#3b82f6",
                                         hovertemplate="Mese: %{x}<br>Costo: %{y:,.0f} \u20ac<extra></extra>"))
                fig_mf1.add_trace(go.Bar(x=df_mm["Mese"], y=df_mm["Margine (\u20ac)"], name="Margine fornitore",
                                         marker_color="#22c55e",
                                         hovertemplate="Mese: %{x}<br>Margine: %{y:,.0f} \u20ac<extra></extra>"))
                fig_mf1.update_layout(template="plotly_dark", height=340, barmode="stack",
                                      title="Ricavo offerta mensile: costo vs margine fornitore",
                                      xaxis_title="Mese", yaxis_title="\u20ac")
                st.plotly_chart(fig_mf1, use_container_width=True)
                st.caption("La parte verde e' quanto guadagna il fornitore ogni mese sulla tua offerta.")
            except Exception:
                st.info("Grafico mensile non disponibile per questi dati.")

            try:
                df_mg = mf["df_giorni"]
                fig_mf2 = go.Figure()
                fig_mf2.add_trace(go.Scatter(x=df_mg["Giorno"], y=df_mg["Costo cumulato (\u20ac)"],
                                             mode="lines", name="Costo cumulato",
                                             line=dict(color="#3b82f6"),
                                             hovertemplate="Giorno: %{x}<br>Costo: %{y:,.0f} \u20ac<extra></extra>"))
                fig_mf2.add_trace(go.Scatter(x=df_mg["Giorno"], y=df_mg["Ricavo cumulato (\u20ac)"],
                                             mode="lines", name="Ricavo offerta cumulato", fill="tonexty",
                                             line=dict(color="#22c55e"),
                                             hovertemplate="Giorno: %{x}<br>Ricavo: %{y:,.0f} \u20ac<extra></extra>"))
                fig_mf2.update_layout(template="plotly_dark", height=300,
                                      title="Cumulata nel tempo: costo vs ricavo offerta",
                                      xaxis_title="Giorno", yaxis_title="\u20ac cumulati")
                st.plotly_chart(fig_mf2, use_container_width=True)
                st.caption("La distanza tra le due curve e' il margine del fornitore accumulato giorno per giorno.")
            except Exception:
                st.info("Curva cumulata non disponibile per questi dati.")

            df_mf = mf["df_mesi"]
            if len(df_mf):
                st.markdown("**Dettaglio mensile**")
                st.dataframe(df_mf, use_container_width=True, hide_index=True)
                st.download_button(
                    "\u2b07\ufe0f Esporta margine fornitore (CSV)",
                    df_mf.to_csv(index=False).encode("utf-8"),
                    file_name=f"margine_fornitore_{d0}_{d1}.csv",
                    mime="text/csv",
                    help="Scarica il dettaglio mensile del margine implicito del fornitore.",
                )

    with tab50:
        titolo_pb = edu("Ponte budget-consuntivo", "Scomposizione dello scostamento tra costo effettivo e budget in tre driver che sommano esattamente: effetto PREZZO (prezzi diversi dal budget, a volumi di budget), effetto VOLUME (volumi diversi dal budget, a prezzi di budget) ed effetto MIX (interazione: consumare di piu' proprio quando i prezzi sono sopra budget). Il budget mensile e' ripartito per giorni di calendario.")
        st.markdown(f"**{titolo_pb}**: perche' sei sopra (o sotto) budget? Prezzi, volumi o entrambi.", unsafe_allow_html=True)

        b0, b1 = st.columns(2)
        with b0:
            pb_prezzo = st.number_input("Prezzo di budget (€/MWh)", min_value=0.0, value=110.0, step=1.0,
                                        key="pb50_prezzo",
                                        help="Prezzo unitario usato nel budget sul periodo selezionato.")
        with b1:
            pb_volume = st.number_input("Volume di budget (MWh sul periodo)", min_value=0.0, value=0.0, step=10.0,
                                        key="pb50_volume",
                                        help="Volume totale di budget sul periodo selezionato; ripartito sui mesi per giorni di calendario.")

        pb = calcola_ponte_budget(prezzi, mw_f1, mw_f2, mw_f3, pb_prezzo, pb_volume)
        if pb["errore"]:
            st.warning(f"\u26a0\ufe0f {pb['errore']}")
        elif pb["mwh_eff"] == 0:
            st.warning("Imposta una potenza maggiore di zero in almeno una fascia (tab \U0001F4B0 Costo fornitura) per calcolare il ponte.")
        else:
            k1, k2, k3, k4 = st.columns(4)
            render_kpi(edu("Costo budget", "Costo previsto: prezzo di budget per volume di budget sul periodo."),
                       f"{pb['costo_budget']:,.0f} \u20ac", k1)
            render_kpi(edu("Costo effettivo", "Costo reale: spot orario pesato sul tuo profilo F1/F2/F3."),
                       f"{pb['costo_eff']:,.0f} \u20ac", k2)
            render_kpi(edu("Scostamento", "Effettivo meno budget: positivo = sopra budget. La somma dei tre effetti lo spiega tutto."),
                       f"{pb['scostamento']:+,.0f} \u20ac" +
                       (f" ({pb['scostamento_pct']*100:+.1f} %)" if pb["scostamento_pct"] is not None else ""), k3)
            render_kpi(edu("Driver principale", "Il contributo piu' grande in valore assoluto tra prezzo, volume e mix."),
                       pb["driver"].upper() if pb["driver"] else "\u2014", k4)
            st.caption(f"{pb['mwh_eff']:,.0f} MWh effettivi a {pb['prezzo_lw']:,.2f} \u20ac/MWh (load-weighted) "
                       f"contro budget {pb_prezzo:,.2f} \u20ac/MWh.")

            try:
                fig_pb1 = go.Figure(go.Waterfall(
                    name="Ponte", orientation="v",
                    measure=["absolute", "relative", "relative", "relative", "total"],
                    x=["Budget", "Effetto prezzo", "Effetto volume", "Effetto mix", "Effettivo"],
                    y=[pb["costo_budget"], pb["eff_prezzo"], pb["eff_volume"], pb["eff_mix"], pb["costo_eff"]],
                    connector={"line": {"color": "#6b7280"}},
                    decreasing={"marker": {"color": "#22c55e"}},
                    increasing={"marker": {"color": "#ef4444"}},
                    totals={"marker": {"color": "#3b82f6"}},
                    hovertemplate="%{x}: %{y:,.0f} \u20ac<extra></extra>"))
                fig_pb1.update_layout(template="plotly_dark", height=340,
                                      title="Ponte budget \u2192 consuntivo: da dove viene lo scostamento",
                                      yaxis_title="\u20ac", showlegend=False)
                st.plotly_chart(fig_pb1, use_container_width=True)
                st.caption("Barre rosse = peggiorano lo scostamento, verdi = lo migliorano. La somma dei tre effetti centrali e' esattamente lo scostamento.")
            except Exception:
                st.info("Grafico waterfall non disponibile per questi dati.")

            try:
                df_pm = pb["df_mesi"]
                fig_pb2 = go.Figure()
                for col, colore in [("Effetto prezzo (\u20ac)", "#f59e0b"),
                                    ("Effetto volume (\u20ac)", "#8b5cf6"),
                                    ("Effetto mix (\u20ac)", "#06b6d4")]:
                    fig_pb2.add_trace(go.Bar(x=df_pm["Mese"], y=df_pm[col], name=col,
                                             marker_color=colore,
                                             hovertemplate="Mese: %{x}<br>" + col + ": %{y:,.0f} \u20ac<extra></extra>"))
                fig_pb2.update_layout(template="plotly_dark", height=320, barmode="relative",
                                      title="Driver dello scostamento per mese",
                                      xaxis_title="Mese", yaxis_title="\u20ac")
                st.plotly_chart(fig_pb2, use_container_width=True)
                st.caption("Ogni mese lo scostamento e' la somma dei tre effetti impilati (sopra/sotto lo zero).")
            except Exception:
                st.info("Grafico mensile non disponibile per questi dati.")

            df_pb = pb["df_mesi"]
            if len(df_pb):
                st.markdown("**Dettaglio mensile**")
                st.dataframe(df_pb, use_container_width=True, hide_index=True)
                st.download_button(
                    "\u2b07\ufe0f Esporta ponte budget (CSV)",
                    df_pb.to_csv(index=False).encode("utf-8"),
                    file_name=f"ponte_budget_{d0}_{d1}.csv",
                    mime="text/csv",
                    help="Scarica il dettaglio mensile del ponte budget-consuntivo.",
                )

    with tab51:
        titolo_dc = edu("Driver del costo", "Scompone la VARIANZA del costo giornaliero di fornitura (stessa logica della tab \U0001F4B0 Costo fornitura: spot orario pesato sul tuo profilo F1/F2/F3) in tre driver che sommano al 100%: MESE (stagionalita'), SETTIMANA (pattern lunedi'-domenica al netto del mese) e RESIDUO (spike, eventi, rumore non di calendario). Metodo: ANOVA a due vie senza interazione, quote eta-quadro sequenziali (OLS).")
        st.markdown(f"**{titolo_dc}**: cosa muove davvero il tuo costo — la stagione, il giorno della settimana, o il resto?", unsafe_allow_html=True)
        st.caption("Profilo di prelievo: quello impostato nel tab \U0001F4B0 Costo fornitura (MW per fascia F1/F2/F3).")

        dc = calcola_driver_costo(prezzi, mw_f1, mw_f2, mw_f3)
        if dc["giorni"] == 0:
            st.warning("Imposta una potenza maggiore di zero in almeno una fascia (tab \U0001F4B0 Costo fornitura) e seleziona un periodo con dati.")
        elif dc["giorni"] < 14:
            st.warning(f"Solo {dc['giorni']} giorni di dati: servono almeno 14 giorni per una scomposizione significativa.")
        elif dc["driver"] is None:
            st.info("Costo giornaliero costante sul periodo: nessuna varianza da scomporre.")
        else:
            nomi_driver = {"mese": "MESE \U0001F4C5", "settimana": "SETTIMANA \U0001F5D3\uFE0F", "residuo": "RESIDUO \U0001F3B2"}
            qmax = max(dc["eta2_mese"], dc["eta2_settimana"], dc["eta2_residuo"])
            k1, k2, k3, k4 = st.columns(4)
            render_kpi(edu("Costo medio giornaliero", "Costo medio al giorno sul periodo: spot orario pesato sul profilo F1/F2/F3."),
                       f"{dc['costo_medio_giorno']:,.0f} \u20ac", k1)
            render_kpi(edu("Driver principale", "Il driver che spiega la quota maggiore della varianza del costo giornaliero."),
                       f"{nomi_driver.get(dc['driver'], chr(8212))} ({qmax*100:.0f}%)", k2)
            render_kpi(edu("Residuo non spiegato", "Quota di varianza non legata al calendario: spike, eventi, rumore."),
                       f"{dc['eta2_residuo']*100:.1f} %", k3)
            render_kpi(edu("Mese piu' costoso", "Mese col costo medio giornaliero piu' alto nel periodo."),
                       dc["mese_max"] or chr(8212), k4)

            df_q = pd.DataFrame({
                "Driver": ["Mese (stagionalita')", "Settimana (lun-dom)", "Residuo (non calendario)"],
                "Quota %": [dc["eta2_mese"] * 100, dc["eta2_settimana"] * 100, dc["eta2_residuo"] * 100]})
            fig_q = px.bar(df_q, x="Quota %", y="Driver", orientation="h", text="Quota %",
                           title="Quanto spiega ciascun driver (eta\u00b2, somma 100%)")
            fig_q.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            fig_q.update_layout(xaxis_range=[0, max(10.0, df_q["Quota %"].max() * 1.25)])
            st.plotly_chart(fig_q, use_container_width=True)

            c1, c2 = st.columns(2)
            with c1:
                fig_m = px.bar(dc["df_mesi"], x="Mese", y="Costo medio (\u20ac/giorno)",
                               title="Costo medio giornaliero per mese",
                               text="Costo medio (\u20ac/giorno)")
                fig_m.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
                st.plotly_chart(fig_m, use_container_width=True)
            with c2:
                fig_s = px.bar(dc["df_settimana"], x="Giorno", y="Costo medio (\u20ac/giorno)",
                               title="Costo medio giornaliero per giorno della settimana",
                               text="Costo medio (\u20ac/giorno)")
                fig_s.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
                st.plotly_chart(fig_s, use_container_width=True)

            st.markdown("**Dettaglio mensile**")
            st.dataframe(dc["df_mesi"], use_container_width=True, hide_index=True)
            st.markdown("**Dettaglio settimanale**")
            st.dataframe(dc["df_settimana"], use_container_width=True, hide_index=True)
            st.download_button(
                "\u2b07\ufe0f Esporta driver del costo (CSV)",
                dc["df_mesi"].to_csv(index=False).encode("utf-8"),
                file_name=f"driver_costo_{d0}_{d1}.csv",
                mime="text/csv",
                help="Scarica il dettaglio mensile dei driver del costo.",
            )

# Footer

st.markdown("---")
st.markdown(f"<div style='text-align: center; color: #4B5563; font-size: 10px;'>Singularity OS V16 | Edu Mode: {st.session_state.edu_mode}</div>", unsafe_allow_html=True)
