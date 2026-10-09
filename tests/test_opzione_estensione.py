"""Test tab218 'Opzione di estensione contratto': helper calcola_opzione_estensione —
valutazione Black-76 di un diritto di estensione della fornitura (call sul
forward dell'anno 2, strike = prezzo di estensione pattuito).

Stile pytest (vedi docs/AGGIUNGERE_TAB.md): la funzione viene estratta da
app.py via AST senza avviare Streamlit.
"""

import math

import numpy as np
import pytest
import re
from pathlib import Path
from scipy.stats import norm

from appfuncs import load

_F = load("calcola_opzione_estensione", "_phi_std", "_fmt_mwh")
calcola_opzione_estensione = _F["calcola_opzione_estensione"]

APP = Path(__file__).parent.parent / "app.py"

DISC_1Y_5PCT = math.exp(-0.05)


def _black76_call(F, K, sig, T, r):
    """Valore atteso indipendente (scipy) per confronto."""
    disc = math.exp(-r * T)
    if sig <= 0 or T <= 0:
        return disc * max(F - K, 0.0), (1.0 if F > K else 0.0)
    d1 = (math.log(F / K) + 0.5 * sig ** 2 * T) / (sig * math.sqrt(T))
    d2 = d1 - sig * math.sqrt(T)
    return disc * (F * norm.cdf(d1) - K * norm.cdf(d2)), norm.cdf(d2)


class TestNumeriAMano:
    def test_volatilita_zero_intrinseco_scontato(self):
        # F=120, K=100, vol=0, T=1y, r=5%: premio = e^-0.05 * 20
        r = calcola_opzione_estensione(100.0, 1000.0, 120.0, vol_annua_pct=0.0,
                                       tasso_annuo_pct=5.0,
                                       giorni_a_decisione=365)
        assert r["errore"] is None and r["valido"] is True
        assert r["premio_equo_eur_mwh"] == pytest.approx(DISC_1Y_5PCT * 20.0)
        assert r["valore_tot_eur"] == pytest.approx(DISC_1Y_5PCT * 20.0 * 1000.0)
        assert r["intrinseco_eur_mwh"] == pytest.approx(20.0)
        assert r["prob_esercizio_pct"] == pytest.approx(100.0)

    def test_volatilita_zero_otm(self):
        # F=90 < K=100: valore nullo, prob 0
        r = calcola_opzione_estensione(100.0, 500.0, 90.0, vol_annua_pct=0.0,
                                       tasso_annuo_pct=5.0,
                                       giorni_a_decisione=365)
        assert r["valido"] is True
        assert r["premio_equo_eur_mwh"] == pytest.approx(0.0)
        assert r["valore_tot_eur"] == pytest.approx(0.0)
        assert r["prob_esercizio_pct"] == pytest.approx(0.0)

    def test_atm_black76(self):
        # F=K=100, sig=30%, T=1, r=5%: d1=0.15, d2=-0.15
        premio_att, prob_att = _black76_call(100.0, 100.0, 0.30, 1.0, 0.05)
        r = calcola_opzione_estensione(100.0, 2000.0, 100.0, vol_annua_pct=30.0,
                                       tasso_annuo_pct=5.0,
                                       giorni_a_decisione=365)
        assert r["valido"] is True
        assert r["premio_equo_eur_mwh"] == pytest.approx(premio_att, rel=1e-4)
        assert r["valore_tot_eur"] == pytest.approx(premio_att * 2000.0,
                                                   rel=1e-4)
        assert r["prob_esercizio_pct"] == pytest.approx(prob_att * 100.0,
                                                        abs=0.08)  # _phi_std: approx A-S
        # ATM: il premio e' tutto valore temporale
        assert r["intrinseco_eur_mwh"] == pytest.approx(0.0)

    def test_itm_con_volatilita(self):
        # F=130, K=100, sig=25%, T=0.5y, r=3%, V=1500
        premio_att, prob_att = _black76_call(130.0, 100.0, 0.25, 0.5, 0.03)
        r = calcola_opzione_estensione(100.0, 1500.0, 130.0, vol_annua_pct=25.0,
                                       tasso_annuo_pct=3.0,
                                       giorni_a_decisione=183)
        assert r["valido"] is True
        assert r["premio_equo_eur_mwh"] == pytest.approx(premio_att, rel=1e-4)
        assert r["valore_tot_eur"] == pytest.approx(premio_att * 1500.0,
                                                   rel=1e-4)
        assert r["prob_esercizio_pct"] == pytest.approx(prob_att * 100.0,
                                                        abs=0.08)  # _phi_std: approx A-S
        # il premio supera sempre l'intrinseco scontato
        assert r["premio_equo_eur_mwh"] >= math.exp(-0.03 * 0.5) * 30.0 - 1e-9

    def test_forward_breakeven(self):
        # breakeven ~ K + premio
        r = calcola_opzione_estensione(100.0, 1000.0, 120.0, vol_annua_pct=20.0,
                                       tasso_annuo_pct=4.0,
                                       giorni_a_decisione=365)
        assert r["forward_breakeven_eur_mwh"] == pytest.approx(
            round(100.0 + r["premio_equo_eur_mwh"], 2), abs=1e-9)


class TestCurva:
    def test_curva_struttura_e_monotonia(self):
        r = calcola_opzione_estensione(100.0, 1000.0, 110.0, vol_annua_pct=30.0)
        df = r["df_curva"]
        assert list(df.columns) == ["Forward €/MWh", "Valore opzione €/MWh",
                                    "Intrinseco €/MWh"]
        assert len(df) == 101
        vals = df["Valore opzione €/MWh"].to_numpy()
        # monotona crescente nel forward
        assert bool(np.all(np.diff(vals) >= -1e-9))
        # il valore (scontato) domina sempre l'intrinseco scontato
        disc = math.exp(-0.03 * 1.0)  # default tasso 3%, T = 365gg
        assert bool(np.all(vals >= disc * df["Intrinseco €/MWh"].to_numpy()
                           - 1e-6))

    def test_curva_vol_zero_e_intrinseco(self):
        r = calcola_opzione_estensione(100.0, 1000.0, 120.0, vol_annua_pct=0.0,
                                       tasso_annuo_pct=5.0,
                                       giorni_a_decisione=365)
        df = r["df_curva"]
        vals = df["Valore opzione €/MWh"].to_numpy()
        fwd = df["Forward €/MWh"].to_numpy()
        att = np.round(DISC_1Y_5PCT * np.maximum(fwd - 100.0, 0.0), 4)
        assert np.allclose(vals, att, rtol=1e-6, atol=1e-4)


class TestInputNonValidi:
    @pytest.mark.parametrize("kwargs", [
        {"prezzo_estensione_eur_mwh": 0.0},
        {"prezzo_estensione_eur_mwh": -10.0},
        {"volume_annuo_mwh": 0.0},
        {"forward_anno2_eur_mwh": -5.0},
        {"vol_annua_pct": -1.0},
        {"giorni_a_decisione": 0},
        {"prezzo_estensione_eur_mwh": float("nan")},
        {"forward_anno2_eur_mwh": float("inf")},
        {"prezzo_estensione_eur_mwh": "100"},
        {"n_punti": 1},
    ])
    def test_errori(self, kwargs):
        base = dict(prezzo_estensione_eur_mwh=100.0, volume_annuo_mwh=1000.0,
                    forward_anno2_eur_mwh=120.0)
        base.update(kwargs)
        r = calcola_opzione_estensione(**base)
        assert r["valido"] is False
        assert isinstance(r["errore"], str) and r["errore"]


class TestDeterminismo:
    def test_due_chiamate_uguali(self):
        kw = dict(prezzo_estensione_eur_mwh=95.0, volume_annuo_mwh=2500.0,
                  forward_anno2_eur_mwh=112.0, vol_annua_pct=35.0,
                  tasso_annuo_pct=2.5, giorni_a_decisione=200)
        a = calcola_opzione_estensione(**kw)
        b = calcola_opzione_estensione(**kw)
        assert a["valore_tot_eur"] == b["valore_tot_eur"]
        assert a["prob_esercizio_pct"] == b["prob_esercizio_pct"]
        assert a["df_curva"].equals(b["df_curva"])


class TestRegistry:
    def test_tab218_dichiarata(self):
        import ast as _ast
        src = APP.read_text(encoding="utf-8")
        tree = _ast.parse(src)
        titoli = None
        for node in _ast.walk(tree):
            if (isinstance(node, _ast.Assign)
                    and isinstance(node.value, _ast.Call)
                    and getattr(getattr(node.value.func, "attr", ""),
                                "lower", lambda: "")() == "tabs"
                                and node.value.args and hasattr(node.value.args[0], "elts")):
                titoli = [t.value for t in node.value.args[0].elts]
        assert titoli is not None
        assert len(titoli) == 339
        assert titoli[217] == "🔁 Opzione di estensione"  # tab218 non piu' ultima
        assert titoli[-1] == "📉 Sortino ratio: il rendimento per unità di rischio al ribasso"
        m = re.search(r"((?:tab\d+, )+tab\d+) = st.tabs\(\[", src)
        assert m is not None
        vars_tab = [v.strip() for v in m.group(1).split(",")]
        assert len(vars_tab) == 339
        assert "tab217" in vars_tab
        withs = re.findall(r"^\s*with (tab\d+):", src, re.M)
        assert len(withs) == len(vars_tab) == 339
        assert "tab218" in withs
        # key widget univoche della tab218
        keys = re.findall(r'key="(oe218_[^"]+)"', src)
        assert len(keys) == len(set(keys)) == 7
