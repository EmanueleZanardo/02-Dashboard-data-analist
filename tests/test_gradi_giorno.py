"""Test tab207 'Gradi giorno': helper calcola_gradi_giorno —
gradi giorno mensili (HDD/CDD) da temperature medie mensili e stima del
fabbisogno termico annuo.

Stile pytest (vedi docs/AGGIUNGERE_TAB.md): la funzione viene estratta da
app.py via AST senza avviare Streamlit.
"""

from appfuncs import load

_F = load("calcola_gradi_giorno")
calcola_gradi_giorno = _F["calcola_gradi_giorno"]

_GIORNI_ANNUI = 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30 + 31


def test_caso_a_mano():
    # 12 mesi a 10.0 C, base riscaldamento 18 -> HDD = 8 * 365 = 2920.0
    r = calcola_gradi_giorno([10.0] * 12, 18.0, 24.0, 2.5)
    assert r["errore"] is None and r["valido"] is True
    assert abs(r["hdd_annuo"] - 8.0 * _GIORNI_ANNUI) < 1e-9
    assert r["hdd_annuo"] == 2920.0
    assert r["cdd_annuo"] == 0.0  # 10.0 < base raffrescamento 24
    assert abs(r["stima_kwh_termici"] - 2920.0 * 2.5) < 1e-9
    assert len(r["hdd_mensili"]) == 12 and len(r["cdd_mensili"]) == 12
    df = r["df_mensile"]
    assert list(df.columns) == ["Mese", "HDD", "CDD"]
    assert len(df) == 12
    assert abs(df["HDD"].sum() - 2920.0) < 1e-6
    assert df["CDD"].sum() == 0.0


def test_cdd_solo():
    # mesi caldi: con base 18 / base_raff 24, temp 30 -> solo CDD
    r = calcola_gradi_giorno([30.0] * 12, 18.0, 24.0, 1.0)
    assert r["errore"] is None
    assert r["hdd_annuo"] == 0.0
    assert abs(r["cdd_annuo"] - 6.0 * _GIORNI_ANNUI) < 1e-9


def test_lista_corta_da_errore_senza_eccezioni():
    r = calcola_gradi_giorno([10.0] * 11, 18.0, 24.0, 2.5)
    assert r["errore"] is not None and r["valido"] is False


def test_nan_e_non_numerici_danno_errore_senza_eccezioni():
    r = calcola_gradi_giorno([10.0] * 11 + [float("nan")], 18.0, 24.0, 2.5)
    assert r["errore"] is not None and r["valido"] is False
    r2 = calcola_gradi_giorno([10.0] * 11 + ["x"], 18.0, 24.0, 2.5)
    assert r2["errore"] is not None and r2["valido"] is False
    r3 = calcola_gradi_giorno(None, 18.0, 24.0, 2.5)
    assert r3["errore"] is not None and r3["valido"] is False


def test_determinismo():
    temps = [2.5, 4.0, 8.0, 11.5, 16.0, 20.0,
             22.5, 22.0, 18.0, 13.0, 7.0, 3.0]
    a = calcola_gradi_giorno(temps, 18.0, 24.0, 2.5)
    b = calcola_gradi_giorno(temps, 18.0, 24.0, 2.5)
    assert a["errore"] == b["errore"] == None  # noqa: E711
    assert a["hdd_annuo"] == b["hdd_annuo"]
    assert a["cdd_annuo"] == b["cdd_annuo"]
    assert a["stima_kwh_termici"] == b["stima_kwh_termici"]
    assert a["hdd_mensili"] == b["hdd_mensili"]
    assert a["cdd_mensili"] == b["cdd_mensili"]
    assert a["df_mensile"].equals(b["df_mensile"])
