"""Test tab211 'Certificati Bianchi (TEE)': helper calcola_valore_tee —
TEE generati da un intervento di risparmio energetico, VAN/TIR/payback.

Stile pytest (vedi docs/AGGIUNGERE_TAB.md): la funzione viene estratta da
app.py via AST senza avviare Streamlit.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("calcola_valore_tee")
calcola_valore_tee = _F["calcola_valore_tee"]

APP = Path(__file__).parent.parent / "app.py"

# risparmio 1000 MWh elettrico, 5 anni, prezzo 300 €/TEE, istruttoria 2000,
# costo 150000, tasso 6%
BASE = dict(risparmio_mwh_anno=1000.0, vettore="elettrico",
            anni_vita_utile=5, prezzo_tee_eur=300.0, tasso_sconto_pct=6.0,
            costo_istruttoria_eur_anno=2000.0, costo_intervento_eur=150000.0)

TEE_1000_E = 1000.0 / 5.346          # 187.0549...
NETTO = TEE_1000_E * 300.0 - 2000.0  # 54116.47...
A5_6 = (1 - 1.06 ** -5) / 0.06        # 4.21236...
VAN_ATTESO = -150000.0 + NETTO * A5_6


class TestCasiBase:
    def test_numeri_a_mano(self):
        r = calcola_valore_tee(**BASE)
        assert r["errore"] is None and r["valido"] is True
        assert r["tee_annui"] == pytest.approx(TEE_1000_E)
        assert r["ricavo_lordo_annuo"] == pytest.approx(TEE_1000_E * 300.0)
        assert r["ricavo_netto_annuo"] == pytest.approx(NETTO)
        assert r["van"] == pytest.approx(VAN_ATTESO)
        assert r["van"] > 0
        assert r["verdetto"] == "CONVENIENTE"

    def test_payback_a_mano(self):
        # 2*NETTO < 150000 < 3*NETTO -> payback 3 anni
        r = calcola_valore_tee(**BASE)
        assert 2 * NETTO < 150000.0 < 3 * NETTO
        assert r["payback_anni"] == 3.0

    def test_tir_coerente(self):
        r = calcola_valore_tee(**BASE)
        tir = r["tir_pct"]
        assert tir is not None
        assert 23.0 < tir < 24.0
        # NPV(tir) deve azzerarsi: replica indipendente
        q = tir / 100.0
        npv = -150000.0 + sum(NETTO / (1.0 + q) ** k for k in range(1, 6))
        assert npv == pytest.approx(0.0, abs=1.0)

    def test_gas_fattore(self):
        r = calcola_valore_tee(**dict(BASE, vettore="gas"))
        assert r["valido"] is True
        assert r["fattore_mwh_per_tee"] == pytest.approx(11.63)
        assert r["tee_annui"] == pytest.approx(1000.0 / 11.63)

    def test_non_conveniente(self):
        # istruttoria > ricavo lordo -> flusso negativo -> VAN < 0
        r = calcola_valore_tee(**dict(BASE,
                                     costo_istruttoria_eur_anno=200000.0))
        assert r["valido"] is True
        assert r["ricavo_netto_annuo"] < 0
        assert r["van"] < 0
        assert r["verdetto"] == "NON CONVENIENTE"
        assert r["payback_anni"] is None
        assert r["tir_pct"] is None

    def test_costo_zero(self):
        r = calcola_valore_tee(**dict(BASE, costo_intervento_eur=0.0))
        assert r["valido"] is True
        assert r["van"] == pytest.approx(NETTO * A5_6)
        assert r["payback_anni"] == 0.0
        assert r["tir_pct"] is None  # senza esborso la TIR e' indefinita

    def test_tasso_zero(self):
        r = calcola_valore_tee(**dict(BASE, tasso_sconto_pct=0.0))
        assert r["valido"] is True
        assert r["van"] == pytest.approx(-150000.0 + NETTO * 5)

    def test_df_anni(self):
        r = calcola_valore_tee(**BASE)
        df = r["df"]
        assert len(df) == 6  # anno 0 + 5 anni
        assert list(df.columns) == ["Anno", "TEE generati", "Ricavo lordo (€)",
                                    "Costo istruttoria (€)", "Flusso netto (€)",
                                    "Flusso attualizzato (€)",
                                    "Cumulato attualizzato (€)"]
        assert df["Anno"].iloc[0] == 0
        assert df["Flusso netto (€)"].iloc[0] == -150000.0
        assert df["TEE generati"].iloc[1] == pytest.approx(187.05, abs=0.01)
        # il cumulato attualizzato finale deve coincidere col VAN
        assert df["Cumulato attualizzato (€)"].iloc[-1] == pytest.approx(
            r["van"], abs=2.0)

    def test_determinismo(self):
        a = calcola_valore_tee(**BASE)
        b = calcola_valore_tee(**BASE)
        assert a["van"] == b["van"] and a["tir_pct"] == b["tir_pct"]
        assert a["df"].equals(b["df"])


class TestInputInvalidi:
    @pytest.mark.parametrize("kwargs,atteso", [
        (dict(risparmio_mwh_anno=0), "Risparmio annuo"),
        (dict(risparmio_mwh_anno=float("nan")), "Tutti i parametri"),
        (dict(vettore="idrogeno"), "Vettore"),
        (dict(anni_vita_utile=0), "vita utile"),
        (dict(anni_vita_utile=21), "vita utile"),
        (dict(anni_vita_utile=2.5), "vita utile"),
        (dict(prezzo_tee_eur=0), "prezzo del TEE"),
        (dict(tasso_sconto_pct=-1), "tasso di sconto"),
        (dict(costo_istruttoria_eur_anno=-5), "istruttoria"),
        (dict(costo_intervento_eur=-1), "intervento"),
    ])
    def test_casi_invalidi(self, kwargs, atteso):
        params = dict(BASE)
        params.update(kwargs)
        r = calcola_valore_tee(**params)
        assert r["valido"] is False
        assert atteso.lower() in r["errore"].lower()


class TestRegistryTab211:
    def test_tab211_dichiarata(self):
        src = APP.read_text(encoding="utf-8")
        m = re.search(r"st\.tabs\(\[([^\]]*?)\]\)", src, re.S)
        titoli = eval("[" + m.group(1) + "]")
        assert len(titoli) == 262
        assert titoli[-1] == "🔌 Gruppo elettrogeno vs blackout"
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert len(dvars) == 262 and "tab211" in dvars
        withs = re.findall(r"    with (tab\d+):", src)
        assert len(withs) == 262 and "tab211" in withs
