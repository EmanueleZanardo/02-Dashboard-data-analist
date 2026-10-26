"""Test tab480 '📞 Margin call: variazione margine e buffer di liquidità': registry + funzioni pure."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh480_num", "mh480_mtm_linea", "mh480_mtm_totale",
           "mh480_margine_richiesto", "mh480_equity", "mh480_call_margine",
           "mh480_shock_mtm", "mh480_copertura_liquidita", "mh480_verdetto")

TITLE482 = "🗓️ Ladder delle scadenze: profilo temporale di volumi, MtM e DV01"
TITLE480 = "📞 Margin call: variazione margine e buffer di liquidità"
TITLE479 = "🏦 Costo del margine: il capitale fermo al clearing"

# Demo deterministica: conto margini dopo una giornata avversa.
# TTF gas 250'000 MWh long: 95.00 -> 92.50  => MtM -625'000
# Power DE 120'000 MWh short: 110.00 -> 112.00 => MtM -240'000
# CO2 EUA 500'000 t long: 75.00 -> 76.50 => MtM +750'000
# MtM totale -115'000; IM unitari 4.20/6.50/3.00 => IM 3'330'000;
# collaterale postato 3'200'000 => equity 3'085'000;
# call 245'000; buffer libero 200'000 => copertura ~0.8163 => CALL IMMINENTE.
LINEE_DEMO = [
    {"nome": "TTF gas", "qta_mwh": 250000.0, "segno": 1.0,
     "prezzo_ieri": 95.00, "prezzo_oggi": 92.50},
    {"nome": "Power baseload DE", "qta_mwh": 120000.0, "segno": -1.0,
     "prezzo_ieri": 110.00, "prezzo_oggi": 112.00},
    {"nome": "CO2 EUA", "qta_mwh": 500000.0, "segno": 1.0,
     "prezzo_ieri": 75.00, "prezzo_oggi": 76.50},
]
IM_DEMO = [1050000.0, 780000.0, 1500000.0]
COLL_DEMO = 3200000.0
LIBERO_DEMO = 200000.0
SHOCK_DEMO = 5.0
MTM_DEMO = -115000.0
IMTOT_DEMO = 3330000.0
EQUITY_DEMO = 3085000.0
CALL_DEMO = 245000.0
COP_DEMO = 0.8163265306122449
VERD_DEMO = 'CALL IMMINENTE'
SHOCKMTM_DEMO = -3740750.0


class TestRegistry481:
    def test_conteggi(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        withs = re.findall(r"    with (tab\d+):", src)
        assert len(titoli) == len(dvars) == len(withs) == 730

    def test_ultima_tab(self):
        import re
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
        titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
        dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
        assert TITLE482 in titoli
        assert TITLE480 in titoli  # membership (non [-2]: la posizione scorre a ogni ciclo)
        assert "tab482" in dvars

    def test_ui_indentata(self):
        src = (Path(__file__).resolve().parent.parent / "app.py"
               ).read_text(encoding="utf-8")
        assert "    with tab480:" in src


class TestNum480:
    def test_ok(self):
        assert _F["mh480_num"](3.5, "x") == 3.5
        assert _F["mh480_num"](7, "x") == 7.0

    def test_bool_rifiutato(self):
        with pytest.raises(ValueError):
            _F["mh480_num"](True, "x")

    def test_nan_inf_rifiutati(self):
        with pytest.raises(ValueError):
            _F["mh480_num"](float("nan"), "x")
        with pytest.raises(ValueError):
            _F["mh480_num"](float("inf"), "x")

    def test_stringa_rifiutata(self):
        with pytest.raises(ValueError):
            _F["mh480_num"]("3.5", "x")


class TestMtmLinea480:
    def test_demo_long_perdita(self):
        assert _F["mh480_mtm_linea"](250000.0, 1.0, 95.00, 92.50) == -625000.0

    def test_demo_short_perdita(self):
        assert _F["mh480_mtm_linea"](120000.0, -1.0, 110.00, 112.00) == -240000.0

    def test_demo_long_profitto(self):
        assert _F["mh480_mtm_linea"](500000.0, 1.0, 75.00, 76.50) == 750000.0

    def test_prezzo_invariato(self):
        assert _F["mh480_mtm_linea"](1000.0, 1.0, 50.0, 50.0) == 0.0

    def test_segno_invalido(self):
        with pytest.raises(ValueError):
            _F["mh480_mtm_linea"](1000.0, 0.5, 50.0, 51.0)

    def test_qta_negativa(self):
        with pytest.raises(ValueError):
            _F["mh480_mtm_linea"](-10.0, 1.0, 50.0, 51.0)

    def test_prezzo_negativo(self):
        with pytest.raises(ValueError):
            _F["mh480_mtm_linea"](1000.0, 1.0, -50.0, 51.0)


class TestMtmTotale480:
    def test_demo(self):
        agg = _F["mh480_mtm_totale"](LINEE_DEMO)
        assert agg["totale"] == MTM_DEMO
        assert agg["n_linee"] == 3

    def test_quote_sommano_uno(self):
        agg = _F["mh480_mtm_totale"](LINEE_DEMO)
        assert abs(sum(r["quota"] for r in agg["righe"]) - 1.0) < 1e-12

    def test_ordine_quote(self):
        agg = _F["mh480_mtm_totale"](LINEE_DEMO)
        q = {r["nome"]: r["quota"] for r in agg["righe"]}
        assert q["CO2 EUA"] > q["TTF gas"] > q["Power baseload DE"]

    def test_linea_zero_quota_zero(self):
        ln = [dict(LINEE_DEMO[0]),
              {"nome": "zero", "qta_mwh": 0.0, "segno": 1.0,
               "prezzo_ieri": 10.0, "prezzo_oggi": 10.0}]
        agg = _F["mh480_mtm_totale"](ln)
        z = [r for r in agg["righe"] if r["nome"] == "zero"][0]
        assert z["mtm"] == 0.0 and z["quota"] == 0.0

    def test_vuota(self):
        with pytest.raises(ValueError):
            _F["mh480_mtm_totale"]([])

    def test_chiave_mancante(self):
        with pytest.raises(ValueError):
            _F["mh480_mtm_totale"]([{"nome": "x", "qta_mwh": 1.0}])


class TestMargineRichiesto480:
    def test_demo(self):
        assert _F["mh480_margine_richiesto"](IM_DEMO) == IMTOT_DEMO

    def test_vuota(self):
        with pytest.raises(ValueError):
            _F["mh480_margine_richiesto"]([])

    def test_negativo(self):
        with pytest.raises(ValueError):
            _F["mh480_margine_richiesto"]([100.0, -5.0])


class TestEquityCall480:
    def test_equity_demo(self):
        assert _F["mh480_equity"](COLL_DEMO, MTM_DEMO) == EQUITY_DEMO

    def test_equity_zero_collaterale(self):
        assert _F["mh480_equity"](0.0, -115000.0) == -115000.0

    def test_call_demo(self):
        assert _F["mh480_call_margine"](IMTOT_DEMO, EQUITY_DEMO) == CALL_DEMO

    def test_call_zero_quando_equity_sufficiente(self):
        assert _F["mh480_call_margine"](3330000.0, 3330000.0) == 0.0
        assert _F["mh480_call_margine"](3330000.0, 4000000.0) == 0.0


class TestShock480:
    def test_demo(self):
        ln = [{"qta_mwh": l["qta_mwh"], "prezzo_oggi": l["prezzo_oggi"]}
              for l in LINEE_DEMO]
        assert _F["mh480_shock_mtm"](ln, SHOCK_DEMO) == SHOCKMTM_DEMO

    def test_shock_zero(self):
        ln = [{"qta_mwh": l["qta_mwh"], "prezzo_oggi": l["prezzo_oggi"]}
              for l in LINEE_DEMO]
        assert _F["mh480_shock_mtm"](ln, 0.0) == 0.0

    def test_shock_negativo(self):
        ln = [{"qta_mwh": 1.0, "prezzo_oggi": 100.0}]
        with pytest.raises(ValueError):
            _F["mh480_shock_mtm"](ln, -2.0)

    def test_vuota(self):
        with pytest.raises(ValueError):
            _F["mh480_shock_mtm"]([], 5.0)


class TestCopertura480:
    def test_demo(self):
        assert abs(_F["mh480_copertura_liquidita"](LIBERO_DEMO, CALL_DEMO)
                   - COP_DEMO) < 1e-12

    def test_nessuna_call_inf(self):
        assert _F["mh480_copertura_liquidita"](200000.0, 0.0) == float("inf")

    def test_libero_zero(self):
        assert _F["mh480_copertura_liquidita"](0.0, 245000.0) == 0.0

    def test_negativo(self):
        with pytest.raises(ValueError):
            _F["mh480_copertura_liquidita"](-1.0, 245000.0)


class TestVerdetto480:
    def test_demo(self):
        assert _F["mh480_verdetto"](CALL_DEMO, COP_DEMO) == VERD_DEMO

    def test_nessuna_call(self):
        assert _F["mh480_verdetto"](0.0, 0.5) == "NESSUNA CALL"

    def test_liquida(self):
        assert _F["mh480_verdetto"](100.0, 2.0) == "LIQUIDA"
        assert _F["mh480_verdetto"](100.0, float("inf")) == "LIQUIDA"
        assert _F["mh480_verdetto"](100.0, 1.5) == "LIQUIDA"

    def test_attenzione(self):
        assert _F["mh480_verdetto"](100.0, 1.2) == "ATTENZIONE"
        assert _F["mh480_verdetto"](100.0, 1.0) == "ATTENZIONE"

    def test_call_imminente(self):
        assert _F["mh480_verdetto"](100.0, 0.99) == "CALL IMMINENTE"
        assert _F["mh480_verdetto"](100.0, 0.0) == "CALL IMMINENTE"

    def test_negativo(self):
        with pytest.raises(ValueError):
            _F["mh480_verdetto"](-1.0, 1.0)
