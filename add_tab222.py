"""Ciclo QA 05/10/2026 03:40 CEST - aggiunge tab222 'Oneri generali di sistema'.

Inserisce in app.py:
  1. helper calcola_oneri_generali prima di def calcola_oneri_dispacciamento;
  2. tab222 + titolo in coda alla dichiarazione st.tabs;
  3. blocco UI 'with tab222:' prima di '# Footer'.
Uso una tantum: python3 add_tab222.py (dalla dir del repo).
"""
import io
import re

P = "app.py"
src = io.open(P, encoding="utf-8").read()

HELPER = '''def calcola_oneri_generali(energia_mwh_annua, quota_fissa_eur_pod_anno,
                             quota_potenza_eur_kw_anno,
                             quota_energia_eur_mwh, potenza_kw,
                             n_pod=1, quota_asos_pct=85.0,
                             quote_mensili=None, energia_scenari=None):
    """Stima degli oneri generali di sistema per un prelievo in Italia (BT).

    Domanda operativa: "oltre la materia energia e il dispacciamento, quanto
    pesano gli oneri generali di sistema (ASOS + ARIM) in bolletta?" Voci
    (struttura TIT per la BT, delibera ARERA 654/2015/R/eel):
      - quota FISSA: euro/POD/anno;
      - quota POTENZA: euro/kW/anno sulla potenza impegnata;
      - quota ENERGIA: euro/MWh sull'energia prelevata.
    ASOS copre gli oneri generali del sistema elettrico (ex A3 e altri),
    ARIM i rimanenti oneri: si ripartisce ogni voce per quota_asos_pct
    (default 85%, indicativo -- varia con le delibere trimestrali ARERA).

    Formule:
      fissa   = n_pod x quota_fissa
      potenza = potenza_kw x quota_potenza
      energia = energia_mwh x quota_energia
      totale  = fissa + potenza + energia
      equivalente (€/MWh) = totale / energia

    Il mensile riparte la quota energia per quote_mensili (12 quote, default
    piatto) e fissa/potenza in dodicesimi. La sensitivita' ricalcola il
    totale al variare della quota energia (default: -30%/-15%/base/+15%/+30%).

    NaN-safe: parametri non numerici, energia <= 0, n_pod non intero >= 1,
    quota_asos_pct fuori [0,100], quote non 12/normalizzabili, scenari non
    validi -> errore pulito. Deterministico.

    Ritorna dict con 'errore', 'valido', 'verdetto', 'costo_quota_fissa',
    'costo_quota_potenza', 'costo_quota_energia', 'costo_totale_annuo',
    'quota_asos_eur', 'quota_arim_eur', 'equivalente_eur_mwh', 'quote_pct'
    (dict voce -> %), 'df_mensile', 'df_sensitivita'.
    """
    mesi = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu",
            "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
    col_m = ["Mese", "Energia (MWh)", "Quota fissa (\\u20ac)",
             "Quota potenza (\\u20ac)", "Quota energia (\\u20ac)",
             "Totale (\\u20ac)"]
    col_s = ["Scenario", "Quota energia (\\u20ac/MWh)",
             "Totale annuo (\\u20ac)", "Equivalente (\\u20ac/MWh)"]
    vuoto = {"errore": None, "valido": False, "verdetto": None,
             "costo_quota_fissa": 0.0, "costo_quota_potenza": 0.0,
             "costo_quota_energia": 0.0, "costo_totale_annuo": 0.0,
             "quota_asos_eur": 0.0, "quota_arim_eur": 0.0,
             "equivalente_eur_mwh": 0.0,
             "quote_pct": {"quota_fissa": 0.0, "quota_potenza": 0.0,
                           "quota_energia": 0.0},
             "df_mensile": pd.DataFrame(columns=col_m),
             "df_sensitivita": pd.DataFrame(columns=col_s)}

    def _err(msg):
        out = dict(vuoto)
        out["df_mensile"] = pd.DataFrame(columns=col_m)
        out["df_sensitivita"] = pd.DataFrame(columns=col_s)
        out["errore"] = msg
        return out

    def _num(x, nome):
        if isinstance(x, bool):
            raise ValueError(nome)
        v = float(x)
        if not np.isfinite(v):
            raise ValueError(nome)
        return v

    try:
        en = _num(energia_mwh_annua, "energia")
        qf = _num(quota_fissa_eur_pod_anno, "quota_fissa")
        qp = _num(quota_potenza_eur_kw_anno, "quota_potenza")
        qe = _num(quota_energia_eur_mwh, "quota_energia")
        pk = _num(potenza_kw, "potenza")
        ap = _num(quota_asos_pct, "quota_asos")
        if isinstance(n_pod, bool):
            raise ValueError("n_pod")
        npod = int(n_pod)
        if npod != n_pod or npod < 1:
            raise ValueError("n_pod")
        if en <= 0:
            raise ValueError("energia")
        if qf < 0 or qp < 0 or qe < 0 or pk < 0:
            raise ValueError("negativi")
        if ap < 0 or ap > 100:
            raise ValueError("asos")
        quote = None
        if quote_mensili is not None:
            quote = [_num(q, "quota") for q in quote_mensili]
            if len(quote) != 12:
                raise ValueError("quote_len")
            if any(q < 0 for q in quote) or sum(quote) <= 0:
                raise ValueError("quote_sum")
        scenari = None
        if energia_scenari is not None:
            scenari = [(str(lbl), _num(v, "scen")) for lbl, v in energia_scenari]
            if not scenari:
                raise ValueError("scenari")
    except (ValueError, TypeError):
        return _err("Parametri non validi: controlla valori numerici "
                    "(energia > 0, quote >= 0, n_pod intero >= 1, "
                    "quota ASOS 0-100%).")

    if quote is None:
        quote = [1.0 / 12.0] * 12
    else:
        tot_q = sum(quote)
        quote = [q / tot_q for q in quote]
    if scenari is None:
        scenari = [("-30%", qe * 0.70), ("-15%", qe * 0.85),
                   ("base", qe), ("+15%", qe * 1.15), ("+30%", qe * 1.30)]

    c_fissa = npod * qf
    c_pot = pk * qp
    c_en = en * qe
    totale = c_fissa + c_pot + c_en
    eq = totale / en
    c_asos = totale * ap / 100.0
    c_arim = totale - c_asos
    pct = {}
    for k, v in (("quota_fissa", c_fissa), ("quota_potenza", c_pot),
                 ("quota_energia", c_en)):
        pct[k] = (v / totale * 100.0) if totale > 0 else 0.0

    if eq < 10.0:
        verdetto = "TRASCURABILI: gli oneri generali incidono meno di 10 €/MWh."
    elif eq < 25.0:
        verdetto = "MODERATI: gli oneri generali valgono %.1f €/MWh -- voce da confrontare tra offerte." % eq
    else:
        verdetto = "RILEVANTI: %.1f €/MWh di oneri generali -- pesano piu' di molti spread di fornitura." % eq

    righe_m = []
    for i, m in enumerate(mesi):
        en_m = en * quote[i]
        qf_m = c_fissa / 12.0
        qp_m = c_pot / 12.0
        qe_m = en_m * qe
        righe_m.append((m, round(en_m, 1), round(qf_m, 2), round(qp_m, 2),
                        round(qe_m, 2), round(qf_m + qp_m + qe_m, 2)))
    df_m = pd.DataFrame(righe_m, columns=col_m)

    righe_s = []
    for lbl, qes in scenari:
        t = c_fissa + c_pot + en * qes
        righe_s.append((lbl, round(qes, 2), round(t, 2),
                        round(t / en, 3)))
    df_s = pd.DataFrame(righe_s, columns=col_s)

    out = dict(vuoto)
    out.update({
        "errore": None, "valido": True, "verdetto": verdetto,
        "costo_quota_fissa": c_fissa, "costo_quota_potenza": c_pot,
        "costo_quota_energia": c_en, "costo_totale_annuo": totale,
        "quota_asos_eur": c_asos, "quota_arim_eur": c_arim,
        "equivalente_eur_mwh": eq, "quote_pct": pct,
        "df_mensile": df_m, "df_sensitivita": df_s,
    })
    return out


'''

anchor = "def calcola_oneri_dispacciamento("
assert anchor in src, "anchor helper mancante"
src = src.replace(anchor, HELPER + anchor, 1)

# 2. dichiarazione tab
old_decl_tail = 'tab220, tab221 = st.tabs(['
assert old_decl_tail in src, "dichiarazione tabs non trovata"
src = src.replace(
    old_decl_tail,
    "tab220, tab221, tab222 = st.tabs([", 1)

old_title_tail = '"\\u26a1 Oneri di dispacciamento"])'
if old_title_tail not in src:
    old_title_tail = '"⚡ Oneri di dispacciamento"])'
assert old_title_tail in src, "titolo tab221 non trovato"
src = src.replace(
    old_title_tail,
    '"⚡ Oneri di dispacciamento", "💶 Oneri generali"])',
    1)

UI = '''
    with tab222:
        titolo_og = edu("Oneri generali di sistema", "Oltre la materia energia e il dispacciamento, la bolletta italiana addebita gli oneri generali di sistema: ASOS (oneri generali del sistema elettrico, ex componente A3 e simili) e ARIM (rimanenti oneri), strutturati per la BT in quota fissa (euro/POD/anno), quota potenza (euro/kW/anno) e quota energia (euro/MWh) secondo il TIT (delibera ARERA 654/2015/R/eel), con valori aggiornati trimestralmente. Questa tab stima il costo annuo, lo split ASOS/ARIM, l'equivalente in euro/MWh, la ripartizione mensile e la sensibilita' alla quota energia: utile per quantificare in negoziazione una voce che per i prelievi BT vale tipicamente 20-30 euro/MWh.")
        st.markdown(f"<h1>💶 {titolo_og}</h1>", unsafe_allow_html=True)
        st.caption("Quanto pesano ASOS + ARIM in bolletta? Stima annua di quota fissa + quota potenza + quota energia, con mensile e sensibilita'.")
        st.info("Le componenti cambiano ogni trimestre con le delibere ARERA: i default qui sotto sono INDICATIVI, inserisci i valori della delibera vigente o della tua bolletta per una stima precisa.")
        _profili_og = {
            "Piatto (1/12 al mese)": "piatto",
            "Estivo (picco lug-ago)": "estivo",
            "Invernale (picco gen-feb)": "invernale",
            "Doppia punta (est + inv)": "doppia_punta",
        }
        c1, c2 = st.columns(2)
        with c1:
            en222 = st.number_input("Energia annua prelevata (MWh)",
                                    min_value=0.0, value=1000.0, step=50.0,
                                    key="og222_energia")
            qe222 = st.number_input("Quota energia ASOS+ARIM (€/MWh)",
                                    min_value=0.0, value=27.00, step=0.50,
                                    key="og222_quotaen",
                                    help="Componente energia degli oneri generali (BT), da delibera ARERA vigente.")
            pr222 = st.selectbox("Profilo mensile dell'energia",
                                 list(_profili_og.keys()), key="og222_profilo",
                                 help="Serve a ripartire la quota energia mese per mese.")
        with c2:
            qf222 = st.number_input("Quota fissa (€/POD/anno)",
                                    min_value=0.0, value=0.00, step=1.0,
                                    key="og222_qfissa",
                                    help="Componente fissa degli oneri generali (BT).")
            qp222 = st.number_input("Quota potenza (€/kW/anno)",
                                    min_value=0.0, value=21.00, step=1.0,
                                    key="og222_qpot",
                                    help="Componente di potenza degli oneri generali (BT).")
            pk222 = st.number_input("Potenza impegnata (kW)",
                                    min_value=0.0, value=200.0, step=10.0,
                                    key="og222_potenza")
            np222 = st.number_input("Numero POD", min_value=1, value=1,
                                    step=1, key="og222_npod")
            ap222 = st.slider("Quota ASOS sul totale (%)", 0.0, 100.0, 85.0,
                              step=1.0, key="og222_asos",
                              help="ASOS copre gli oneri generali del sistema; ARIM i rimanenti.")
        ris222 = calcola_oneri_generali(
            float(en222), float(qf222), float(qp222), float(qe222),
            float(pk222), n_pod=int(np222), quota_asos_pct=float(ap222),
            quote_mensili=profilo_mensile_demo(_profili_og[pr222]))
        if ris222["errore"]:
            st.error(ris222["errore"])
        else:
            st.subheader(ris222["verdetto"])
            k1, k2, k3, k4 = st.columns(4)
            with k1:
                st.metric("Quota energia", "€ %,.0f" % ris222["costo_quota_energia"])
            with k2:
                st.metric("Quota potenza", "€ %,.0f" % ris222["costo_quota_potenza"])
            with k3:
                st.metric("ASOS / ARIM", "€ %,.0f / € %,.0f" % (ris222["quota_asos_eur"], ris222["quota_arim_eur"]))
            with k4:
                st.metric("Totale annuo", "€ %,.0f" % ris222["costo_totale_annuo"])
            st.caption("Equivalente: %.3f €/MWh sull'energia prelevata "
                       "(energia %.1f%% · potenza %.1f%% · fissa %.1f%%)." % (
                           ris222["equivalente_eur_mwh"],
                           ris222["quote_pct"]["quota_energia"],
                           ris222["quote_pct"]["quota_potenza"],
                           ris222["quote_pct"]["quota_fissa"]))
            import plotly.graph_objects as go
            fig222 = go.Figure()
            df_m222 = ris222["df_mensile"]
            fig222.add_trace(go.Bar(x=df_m222["Mese"],
                                    y=df_m222["Quota energia (€)"],
                                    name="Quota energia"))
            fig222.add_trace(go.Bar(x=df_m222["Mese"],
                                    y=df_m222["Quota potenza (€)"],
                                    name="Quota potenza"))
            fig222.add_trace(go.Bar(x=df_m222["Mese"],
                                    y=df_m222["Quota fissa (€)"],
                                    name="Quota fissa"))
            fig222.update_layout(title="Oneri generali mensili per componente",
                                 barmode="stack",
                                 xaxis_title="Mese", yaxis_title="€",
                                 height=360, margin=dict(l=40, r=20, t=50, b=40))
            st.plotly_chart(fig222, use_container_width=True, key="og222_bar")
            st.subheader("Dettaglio mensile")
            st.dataframe(df_m222, use_container_width=True, hide_index=True)
            st.subheader("Sensibilita' alla quota energia")
            df_s222 = ris222["df_sensitivita"]
            st.dataframe(df_s222, use_container_width=True, hide_index=True)
            st.download_button(
                "Scarica CSV oneri generali",
                data=df_m222.to_csv(index=False, sep=";").encode("utf-8"),
                file_name="oneri_generali_mensile.csv", mime="text/csv",
                key="og222_csv",
                help="Dettaglio mensile degli oneri generali di sistema.")
            st.caption("Stima indicativa: le componenti ARERA cambiano ogni trimestre; aggiorna i default con i valori della delibera vigente. "
                       "La quota potenza qui e' calcolata sulla potenza impegnata inserita.")
'''

marker = "# Footer"
assert marker in src, "marker footer mancante"
src = src.replace(marker, UI + "\n" + marker, 1)

io.open(P, "w", encoding="utf-8").write(src)
print("OK: tab222 inserita")
