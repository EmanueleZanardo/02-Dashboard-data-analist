"""Test tab223 (stile pytest): Componenti trasporto & misura.

Le funzioni sono pure (niente Streamlit nel corpo): estratte da app.py via
AST con tests/appfuncs.py.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("calcola_componenti_trasporto_misura", "profilo_mensile_demo")
calcola_componenti_trasporto_misura = _F["calcola_componenti_trasporto_misura"]
profilo_mensile_demo = _F["profilo_mensile_demo"]


class TestTrasportoMisuraBase:
    def test_numeri_a_mano(self):
        # BT default: fissa = 1 x (25+31+26) = 82
        # potenza = 200 x (25+31+0) = 11200
        # energia = 1000 x (0.85+0.75+0.40) = 2000
        # totale 13282 -> 13.282 euro/MWh -> PESANTI
        # trasmissione = 25 + 5000 + 850 = 5875
        # distribuzione = 31 + 6200 + 750 = 6981
        # misura = 26 + 0 + 400 = 426
        r = calcola_componenti_trasporto_misura(1000.0, 200.0)
        assert r["errore"] is None and r["valido"]
        assert r["costo_fissa"] == pytest.approx(82.0)
        assert r["costo_potenza"] == pytest.approx(11200.0)
        assert r["costo_energia"] == pytest.approx(2000.0)
        assert r["costo_totale_annuo"] == pytest.approx(13282.0)
        assert r["trasm_eur"] == pytest.approx(5875.0)
        assert r["distr_eur"] == pytest.approx(6981.0)
        assert r["misura_eur"] == pytest.approx(426.0)
        assert r["equivalente_eur_mwh"] == pytest.approx(13.282)
        assert "PESANTI" in r["verdetto"]
        assert sum(r["quote_pct"].values()) == pytest.approx(100.0)
        assert r["quote_pct"]["distribuzione"] == pytest.approx(
            6981.0 / 13282.0 * 100.0)

    def test_mt_e_contenuti_rilevanti(self):
        # MT default: fissa = 1 x (25+200+450) = 675
        # potenza = 500 x (25+28+0) = 26500
        # energia = 5000 x (0.75+0.55+0.30) = 8000 -> totale 35175 -> 7.035
        r = calcola_componenti_trasporto_misura(5000.0, 500.0, tensione="MT")
        assert r["errore"] is None and r["valido"]
        assert r["costo_fissa"] == pytest.approx(675.0)
        assert r["costo_totale_annuo"] == pytest.approx(35175.0)
        assert "RILEVANTI" in r["verdetto"]
        # solo quota energia: 1000 MWh, tutto a zero tranne distr_energia=4
        comp = {"tau1_fissa": 0.0, "tau2_potenza": 0.0, "tau3_energia": 0.0,
                "distr_fissa": 0.0, "distr_potenza": 0.0, "distr_energia": 4.0,
                "sigma1_fissa": 0.0, "sigma2_potenza": 0.0,
                "sigma3_energia": 0.0}
        r2 = calcola_componenti_trasporto_misura(1000.0, 0.0, comp=comp)
        assert r2["costo_totale_annuo"] == pytest.approx(4000.0)
        assert "CONTENUTI" in r2["verdetto"]

    def test_comp_parziale_usa_default(self):
        # comp parziale: solo tau3 custom, il resto default BT
        r = calcola_componenti_trasporto_misura(
            1000.0, 200.0, comp={"tau3_energia": 2.0})
        assert r["errore"] is None
        assert r["costo_energia"] == pytest.approx(
            1000.0 * (2.0 + 0.75 + 0.40))

    def test_mensile_e_sensitivita(self):
        quote = profilo_mensile_demo("estivo")
        r = calcola_componenti_trasporto_misura(1200.0, 100.0,
                                                quote_mensili=quote)
        assert len(r["df_mensile"]) == 12
        assert r["df_mensile"]["Totale (€)"].sum() == pytest.approx(
            r["costo_totale_annuo"], rel=1e-3)
        assert r["df_mensile"]["Energia (MWh)"].sum() == pytest.approx(
            1200.0, rel=1e-3)
        lug = r["df_mensile"].iloc[6]["Distribuzione (€)"]
        gen = r["df_mensile"].iloc[0]["Distribuzione (€)"]
        assert lug > gen  # profilo estivo: luglio > gennaio
        assert len(r["df_sensitivita"]) == 5
        base = r["df_sensitivita"].set_index("Scenario").loc["base"]
        assert base["Totale annuo (€)"] == pytest.approx(
            r["costo_totale_annuo"], rel=1e-6)
        assert base["Quota distr. energia (€/MWh)"] == pytest.approx(0.75)

    def test_input_non_validi(self):
        comp_ok = None
        casi = [
            dict(energia_mwh_annua=0.0, potenza_kw=200.0),       # energia zero
            dict(energia_mwh_annua=-5.0, potenza_kw=200.0),      # energia neg
            dict(energia_mwh_annua=1000.0, potenza_kw=-1.0),     # potenza neg
            dict(energia_mwh_annua=1000.0, potenza_kw=200.0,
                 n_pod=0),                                       # n_pod zero
            dict(energia_mwh_annua=1000.0, potenza_kw=200.0,
                 n_pod=1.5),                                     # n_pod non int
            dict(energia_mwh_annua=1000.0, potenza_kw=200.0,
                 tensione="AT"),                                 # tensione ko
            dict(energia_mwh_annua=1000.0, potenza_kw=200.0,
                 comp={"tau1_fissa": -1.0}),                     # comp negativa
            dict(energia_mwh_annua=1000.0, potenza_kw=200.0,
                 comp="x"),                                      # comp non dict
            dict(energia_mwh_annua=1000.0, potenza_kw=200.0,
                 quote_mensili=[1.0] * 11),                      # quote corte
            dict(energia_mwh_annua=1000.0, potenza_kw=200.0,
                 energia_scenari=[]),                            # scenari vuoti
            dict(energia_mwh_annua="x", potenza_kw=200.0),       # non numerico
        ]
        for kw in casi:
            r = calcola_componenti_trasporto_misura(**kw)
            assert r["errore"] is not None and not r["valido"], kw

    def test_determinismo(self):
        kw = dict(n_pod=2, tensione="MT")
        a = calcola_componenti_trasporto_misura(1000.0, 200.0, **kw)
        b = calcola_componenti_trasporto_misura(1000.0, 200.0, **kw)
        assert a["costo_totale_annuo"] == b["costo_totale_annuo"]
        assert a["verdetto"] == b["verdetto"]


# ------------------------------------------------------- registry
class TestRegistryTab223:
    def test_tab223_dichiarata(self):
        src = Path(__file__).parent.parent.joinpath("app.py").read_text(
            encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        assert len(titoli) == 247
        assert titoli[-1] == "🔄 Voltura e subentro"
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert "tab223" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert "tab223" in withs
        assert len(withs) == len(dvars) == 247
        keys = re.findall(r'key="(tm223_[^"]+)"', src)
        dyn_keys = re.findall(r'key=_pfx223 \+ "([^"]+)"', src)
        # le key dinamiche sono prefissate a runtime con tm223_bt_/tm223_mt_
        assert len(keys) == len(set(keys))
        assert len(dyn_keys) == len(set(dyn_keys)) >= 4
