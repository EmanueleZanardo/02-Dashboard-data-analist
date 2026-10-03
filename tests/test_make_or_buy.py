"""Test pytest tab177 'Autoproduzione vs acquisto' (make-or-buy orario).

Estrae calcola_make_or_buy da app.py via tests/appfuncs (niente Streamlit).
Casi: prezzo piatto (numeri esatti a mano), singolo spike con avviamento,
filtro min_up, casi di errore, determinismo, registry tab177.
"""
import numpy as np
import pandas as pd
import pytest

from appfuncs import load

_F = load("calcola_make_or_buy", "fascia_oraria", "ottimizza_dispatch")
calcola_make_or_buy = _F["calcola_make_or_buy"]


def serie_prezzi(valori, start="2026-01-05"):
    idx = pd.date_range(start, periods=len(valori), freq="h")
    return pd.Series(np.asarray(valori, dtype=float), index=idx)


def test_piatto_sempre_on():
    # 48h a 100 €/MWh, cm=80, P=1 MW, carico 5 MW: spark=20 sempre > 0
    p = serie_prezzi([100.0] * 48)
    r = calcola_make_or_buy(p, 5.0, 5.0, 5.0, costo_marginale=80.0,
                            mw_cogen=1.0, costo_avviamento=0.0,
                            min_up=1, min_down=1, breakeven=False)
    assert r["valido"]
    assert r["ore_on"] == 48
    assert r["energia_mwh"] == pytest.approx(48.0)
    assert r["risparmio_totale"] == pytest.approx(48 * 20.0)
    assert r["avviamenti"] == 1
    assert r["fattore_utilizzo_pct"] == pytest.approx(100.0)
    # quota sul costo di acquisto: 960 / (48*100*5)
    assert r["quota_risparmio_pct"] == pytest.approx(960.0 / 24000.0 * 100.0)
    assert len(r["df_blocchi"]) == 1
    assert r["df_blocchi"].iloc[0]["Ore"] == 48


def test_mai_conveniente():
    # prezzo sempre sotto il costo marginale -> mai ON
    p = serie_prezzi([50.0] * 72)
    r = calcola_make_or_buy(p, 5.0, 5.0, 5.0, costo_marginale=80.0,
                            mw_cogen=1.0, breakeven=False)
    assert r["valido"]
    assert r["ore_on"] == 0
    assert r["risparmio_totale"] == pytest.approx(0.0)
    assert r["avviamenti"] == 0
    assert len(r["df_blocchi"]) == 0


def test_singolo_spike_con_avviamento():
    # 23h a 50, 1h a 200, cm=80, avv=100: spark=-30 / +120
    # blocco di 1h: lordo 120 > 100 -> si accende, netto 20
    vals = [50.0] * 23 + [200.0]
    p = serie_prezzi(vals)
    r = calcola_make_or_buy(p, 5.0, 5.0, 5.0, costo_marginale=80.0,
                            mw_cogen=1.0, costo_avviamento=100.0,
                            min_up=1, min_down=1, breakeven=False)
    assert r["valido"]
    assert r["ore_on"] == 1
    assert r["avviamenti"] == 1
    assert r["risparmio_totale"] == pytest.approx(20.0)
    b = r["df_blocchi"].iloc[0]
    assert b["Risparmio lordo (EUR)"] == pytest.approx(120.0)
    assert b["Risparmio netto (EUR)"] == pytest.approx(20.0)


def test_spike_brevissimo_bloccato_da_min_up():
    # stesso spike ma in mezzo alla serie e min_up=4: il blocco di 1h
    # non e' ammesso -> resta spento
    vals = [50.0] * 10 + [200.0] + [50.0] * 13
    p = serie_prezzi(vals)
    r = calcola_make_or_buy(p, 5.0, 5.0, 5.0, costo_marginale=80.0,
                            mw_cogen=1.0, costo_avviamento=100.0,
                            min_up=4, min_down=1, breakeven=False)
    assert r["valido"]
    assert r["ore_on"] == 0
    assert r["risparmio_totale"] == pytest.approx(0.0)


def test_cap_al_carico():
    # cogeneratore da 10 MW ma carico di 3 MW: energia cappata a 3 MW/h
    p = serie_prezzi([100.0] * 24)
    r = calcola_make_or_buy(p, 3.0, 3.0, 3.0, costo_marginale=80.0,
                            mw_cogen=10.0, costo_avviamento=0.0,
                            min_up=1, min_down=1, breakeven=False)
    assert r["valido"]
    assert r["energia_mwh"] == pytest.approx(24 * 3.0)
    assert r["risparmio_totale"] == pytest.approx(24 * 3.0 * 20.0)


def test_breakeven_piatto():
    # prezzo piatto 100, nessun attrito: break-even = 100
    p = serie_prezzi([100.0] * 48)
    r = calcola_make_or_buy(p, 5.0, 5.0, 5.0, costo_marginale=80.0,
                            mw_cogen=1.0, costo_avviamento=0.0,
                            min_up=1, min_down=1, breakeven=True)
    assert r["valido"]
    assert r["breakeven_cm"] == pytest.approx(100.0, abs=0.5)


def test_breakeven_mai():
    # prezzo sempre 50: neanche gratis conviene con avviamento alto
    p = serie_prezzi([50.0] * 48)
    r = calcola_make_or_buy(p, 5.0, 5.0, 5.0, costo_marginale=10.0,
                            mw_cogen=1.0, costo_avviamento=1e9,
                            min_up=1, min_down=1, breakeven=True)
    assert r["valido"]
    assert r["breakeven_cm"] is None


@pytest.mark.parametrize("kwargs,msg", [
    ({"costo_marginale": -5.0}, "cm negativo"),
    ({"mw_cogen": 0.0}, "potenza nulla"),
    ({"costo_avviamento": -1.0}, "avviamento negativo"),
    ({"min_up": 0}, "min_up zero"),
    ({"min_down": 2.5}, "min_down non intero"),
])
def test_errori_parametri(kwargs, msg):
    p = serie_prezzi([100.0] * 24)
    base = dict(mw_f1=5.0, mw_f2=5.0, mw_f3=5.0)
    base.update(kwargs)
    r = calcola_make_or_buy(p, breakeven=False, **base)
    assert not r["valido"] and r["errore"], msg


def test_errori_serie():
    p_vuota = pd.Series(dtype=float)
    r = calcola_make_or_buy(p_vuota, 5.0, 5.0, 5.0, breakeven=False)
    assert not r["valido"]
    r = calcola_make_or_buy(serie_prezzi([100.0] * 24), 0.0, 0.0, 0.0,
                            breakeven=False)
    assert not r["valido"]  # carico nullo
    r = calcola_make_or_buy("non una serie", 5.0, 5.0, 5.0, breakeven=False)
    assert not r["valido"]


def test_determinismo():
    rng = np.random.default_rng(7)
    p = serie_prezzi(60 + 40 * rng.random(168))
    kw = dict(mw_f1=4.0, mw_f2=3.0, mw_f3=2.0, costo_marginale=85.0,
              mw_cogen=2.0, costo_avviamento=500.0, min_up=4, min_down=2,
              breakeven=False)
    r1 = calcola_make_or_buy(p, **kw)
    r2 = calcola_make_or_buy(p, **kw)
    assert r1["valido"] and r2["valido"]
    assert r1["risparmio_totale"] == r2["risparmio_totale"]
    assert r1["ore_on"] == r2["ore_on"]
    pd.testing.assert_frame_equal(r1["df_ore"], r2["df_ore"])


def test_registry_tab179():
    import ast
    from pathlib import Path
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    # la dichiarazione st.tabs contiene 179 titoli, variabili tab1..tab179
    found = []

    class V(ast.NodeVisitor):
        def visit_Call(self, node):
            f = node.func
            if isinstance(f, ast.Attribute) and f.attr == "tabs" and node.args:
                arg = node.args[0]
                if isinstance(arg, ast.List):
                    found.append(len(arg.elts))
            self.generic_visit(node)

    V().visit(tree)
    assert found, "nessuna chiamata st.tabs trovata"
    assert found[-1] == 179, f"titoli dichiarati: {found[-1]}"
    assert "tab179" in src
    assert "with tab179:" in src
    assert "🕰️ Orologio del prezzo" in src
    # sequenza variabili senza buchi
    import re
    vars_ = sorted({int(m.group(1)) for m in re.finditer(r"\btab(\d+)\b", src)})
    assert vars_ == list(range(1, 180)), "buchi nella sequenza tabN"
