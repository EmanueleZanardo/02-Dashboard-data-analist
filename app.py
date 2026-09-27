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
    st.markdown("Analisi operativa del prezzo spot orario Swissix (CH): KPI, confronto con il periodo precedente, soglie di alert, profilo giornaliero, heatmap oraria, fasce F1/F2/F3, tabella dati, rischio & durata, arbitraggio batteria, base/peak mensile, simulatore costo fornitura, MtM hedging, spark spread, shaping curva, spread weekend, price capture, volatilità realizzata, confronto anno-su-anno, analisi prezzi negativi, spread intra-day, picchi di prezzo, profilo settimanale tipo, curva di durata, concentrazione del costo di fornitura, simulazione demand shifting, finestre di acquisto ottimali, stagionalità mensile, monitoraggio del budget energetico annuale, analisi di sensitività del costo al profilo di prelievo, Value-at-Risk Monte Carlo del costo di fornitura, classifica dei giorni di calendario più costosi per il profilo di prelievo, fasce tariffarie orarie ottimali derivate dal profilo di prezzo osservato ed export CSV.")

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
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12, tab13, tab14, tab15, tab16, tab17, tab18, tab19, tab20, tab21, tab22, tab23, tab24, tab25, tab26, tab27, tab28, tab29 = st.tabs(["⏱️ Profilo giornaliero", "🔥 Heatmap oraria", "⚡ Fasce F1/F2/F3", "📋 Tabella dati", "⚠️ Rischio & Durata", "🔋 Arbitraggio Batteria", "📊 Base/Peak mensile", "💰 Costo fornitura", "📈 MtM hedging", "🔥 Spark spread", "📐 Shaping curva", "📅 Weekend", "☀️ Price capture", "📉 Volatilità", "🗓️ YoY", "⬇️ Prezzi negativi", "↕️ Spread intra-day", "📍 Picchi di prezzo", "📆 Settimana tipo", "📉 Curva durata", "🎯 Concentrazione costo", "🔄 Shifting carico", "🎯 Finestre di acquisto", "🗓️ Stagionalità", "💼 Budget tracker", "🎚️ Sensitività profilo", "🎲 VaR costo (MC)", "🔝 Top giorni di costo", "🎛️ Fasce ottimali"])

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

# Footer
st.markdown("---")
st.markdown(f"<div style='text-align: center; color: #4B5563; font-size: 10px;'>Singularity OS V16 | Edu Mode: {st.session_state.edu_mode}</div>", unsafe_allow_html=True)
