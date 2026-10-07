"""Test tab249 'Preventivo allacciamento': registry + funzioni pure.

Funzioni pure estratte da app.py via AST con tests/appfuncs.py (niente Streamlit).
Verifica consistenza del registry (titoli/dvar/with coerenti) e l'allineamento
titolo-contenuto inclusa la tab249.
"""

import re
from pathlib import Path

import pytest

from appfuncs import load

_F = load("cnx249_quota_potenza", "cnx249_quota_distanza",
          "cnx249_preventivo", "cnx249_confronto_bt_mt",
          "cnx249_sensibilita")
cnx249_quota_potenza = _F["cnx249_quota_potenza"]
cnx249_quota_distanza = _F["cnx249_quota_distanza"]
cnx249_preventivo = _F["cnx249_preventivo"]
cnx249_confronto_bt_mt = _F["cnx249_confronto_bt_mt"]
cnx249_sensibilita = _F["cnx249_sensibilita"]

APP = Path(__file__).parent.parent / "app.py"


def _registry():
    src = APP.read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    withs = re.findall(r"    with (tab\d+):", src)
    return src, titoli, dvars, withs


class TestRegistryTab249:
    def test_tab249_dichiarata(self):
        src, titoli, dvars, withs = _registry()
        assert len(titoli) == len(dvars) == len(withs) == 281
        assert "🔌 Preventivo allacciamento" in titoli
        assert "tab249" in dvars
        assert "tab249" in withs
        assert titoli[dvars.index("tab249")] == "🔌 Preventivo allacciamento"
        assert titoli[-1] == "🛢️ Crack spread: margine raffinazione 3-2-1"
        keys = re.findall(r'key="(t249_[^"]+)"', src)
        assert len(keys) == len(set(keys)) >= 5

    def test_titoli_allineati_248_249(self):
        _, titoli, dvars, _ = _registry()
        assert titoli[dvars.index("tab248")] == "💲 Interessi moratori & ritardo pagamenti"
        assert titoli[dvars.index("tab249")] == "🔌 Preventivo allacciamento"

    def test_helper_definiti_prima_della_ui(self):
        src = APP.read_text(encoding="utf-8")
        i_ws = src.index("if workspace ==")
        for fn in ("cnx249_quota_potenza", "cnx249_quota_distanza",
                   "cnx249_preventivo", "cnx249_confronto_bt_mt",
                   "cnx249_sensibilita"):
            assert src.index(f"def {fn}(") < i_ws, fn


class TestCnx249QuotaPotenza:
    def test_base(self):
        r = cnx249_quota_potenza(15, 70.0)
        assert r == {"kw": 15.0, "tariffa_eur_kw": 70.0, "importo": 1050.0}

    def test_errori(self):
        with pytest.raises(ValueError):
            cnx249_quota_potenza(0, 70.0)
        with pytest.raises(ValueError):
            cnx249_quota_potenza(-5, 70.0)
        with pytest.raises(ValueError):
            cnx249_quota_potenza(15, -1.0)


class TestCnx249QuotaDistanza:
    def test_oltre_franchigia(self):
        r = cnx249_quota_distanza(300, 200, 10.0)
        assert r["metri_fatturabili"] == 100.0
        assert r["importo"] == 1000.0

    def test_entro_franchigia(self):
        r = cnx249_quota_distanza(150, 200, 10.0)
        assert r["metri_fatturabili"] == 0.0
        assert r["importo"] == 0.0

    def test_errori(self):
        with pytest.raises(ValueError):
            cnx249_quota_distanza(-10, 200, 10.0)
        with pytest.raises(ValueError):
            cnx249_quota_distanza(300, 200, -1.0)


class TestCnx249Preventivo:
    def test_completo(self):
        # 15 kW x 70 = 1050; (300-200) m x 10 = 1000; onere 50 -> 2100 imponibile; IVA 10% = 210; tot 2310
        r = cnx249_preventivo(15, 300, 200, 70.0, 10.0, 50.0, 10.0)
        assert r["quota_potenza"] == 1050.0
        assert r["quota_distanza"] == 1000.0
        assert r["imponibile"] == 2100.0
        assert r["iva"] == 210.0
        assert r["totale"] == 2310.0
        assert r["costo_per_kw"] == pytest.approx(154.0)

    def test_distanza_zero(self):
        r = cnx249_preventivo(10, 50, 200, 70.0, 10.0, 50.0, 10.0)
        assert r["quota_distanza"] == 0.0
        assert r["totale"] == pytest.approx((700.0 + 50.0) * 1.10)

    def test_iva_zero(self):
        r = cnx249_preventivo(10, 300, 200, 70.0, 10.0, 50.0, 0.0)
        assert r["iva"] == 0.0
        assert r["totale"] == 1750.0

    def test_errori(self):
        with pytest.raises(ValueError):
            cnx249_preventivo(0, 300, 200, 70.0, 10.0)
        with pytest.raises(ValueError):
            cnx249_preventivo(10, 300, 200, 70.0, 10.0, -5.0)
        with pytest.raises(ValueError):
            cnx249_preventivo(10, 300, 200, 70.0, 10.0, 50.0, 150.0)


_BT = {"franchigia_m": 200.0, "tariffa_eur_kw": 70.0, "tariffa_eur_m": 10.0,
       "onere_amministrativo_eur": 50.0, "iva_pct": 10.0}
_MT = {"franchigia_m": 300.0, "tariffa_eur_kw": 55.0, "tariffa_eur_m": 15.0,
       "onere_amministrativo_eur": 150.0, "iva_pct": 10.0}


class TestCnx249ConfrontoBtMt:
    def test_bt_conviene_con_cabina(self):
        r = cnx249_confronto_bt_mt(15, 300, _BT, _MT, 15000.0)
        assert r["conveniente"] == "BT"
        assert r["preventivo_bt"]["totale"] == 2310.0
        assert r["investimento_mt"] == pytest.approx(
            r["preventivo_mt"]["totale"] + 15000.0)
        assert r["differenza"] == pytest.approx(
            r["investimento_mt"] - r["preventivo_bt"]["totale"])

    def test_mt_conviene_senza_cabina_e_quote_basse(self):
        mt_cheap = dict(_MT, tariffa_eur_kw=10.0, tariffa_eur_m=1.0,
                        onere_amministrativo_eur=0.0)
        r = cnx249_confronto_bt_mt(15, 300, _BT, mt_cheap, 0.0)
        assert r["conveniente"] == "MT"
        assert r["cabina_mt"] == 0.0

    def test_errori(self):
        with pytest.raises(ValueError):
            cnx249_confronto_bt_mt(15, 300, {"tariffa_eur_kw": 1.0}, _MT)
        with pytest.raises(ValueError):
            cnx249_confronto_bt_mt(15, 300, _BT, _MT, -100.0)
        with pytest.raises(ValueError):
            cnx249_confronto_bt_mt(15, 300, "bt", _MT)


class TestCnx249Sensibilita:
    def test_matrice(self):
        righe = cnx249_sensibilita([5.0, 10.0], [100.0, 300.0], 200, 70.0, 10.0,
                                   50.0, 10.0)
        assert len(righe) == 4
        d = {(r["kw"], r["metri"]): r["totale"] for r in righe}
        assert d[(5.0, 100.0)] == pytest.approx((350.0 + 0.0 + 50.0) * 1.10)
        assert d[(10.0, 300.0)] == pytest.approx((700.0 + 1000.0 + 50.0) * 1.10)

    def test_errori(self):
        with pytest.raises(ValueError):
            cnx249_sensibilita([5.0], [100.0, 200.0], 200, 70.0, 10.0)
        with pytest.raises(ValueError):
            cnx249_sensibilita([5.0, 0.0], [100.0, 200.0], 200, 70.0, 10.0)
        with pytest.raises(ValueError):
            cnx249_sensibilita([5.0, 10.0], [100.0, -5.0], 200, 70.0, 10.0)
