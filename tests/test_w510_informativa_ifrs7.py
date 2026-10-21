"""Test tab510 '📋 Informativa IFRS 7 (coperture)': registry + funzioni pure."""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh510_num", "mh510_str", "mh510_data", "mh510_riga",
           "mh510_profilo", "mh510_nota", "mh510_riepilogo")

TITLE510 = "📋 Informativa IFRS 7 (coperture)"
TITLE509 = "🧾 Scritture contabili (IFRS 9)"


def _demo():
    return [
        {"id": "HR-2026-001", "fv_strumento": 23000.0,
         "delta_fv_base": 100000.0, "inefficacia_pnl": 2300.0,
         "riserva_oci_chiusura": 75000.0, "recycling_pnl": 20000.0,
         "nominale": 5000000.0, "scadenza": "2027-12-31",
         "prezzo_medio": 92.50},
        {"id": "HR-2026-002", "fv_strumento": -8500.0,
         "delta_fv_base": -40000.0, "inefficacia_pnl": -800.0,
         "riserva_oci_chiusura": -30000.0, "recycling_pnl": -5000.0,
         "nominale": 2000000.0, "scadenza": "2026-09-30",
         "prezzo_medio": 38.20},
        {"id": "HR-2026-003", "fv_strumento": 12000.0,
         "delta_fv_base": 60000.0, "inefficacia_pnl": 1200.0,
         "riserva_oci_chiusura": 48000.0, "recycling_pnl": 10000.0,
         "nominale": 1500000.0, "scadenza": "2028-12-15",
         "prezzo_medio": 95.00},
        {"id": "HR-2026-004", "fv_strumento": -3000.0,
         "delta_fv_base": -25000.0, "inefficacia_pnl": -500.0,
         "riserva_oci_chiusura": -20000.0, "recycling_pnl": -8000.0,
         "nominale": 800000.0, "scadenza": "2027-03-31",
         "prezzo_medio": 88.00},
    ]


class TestW510Validatori:
    def test_num_ok(self):
        assert _F["mh510_num"](2, "x") == 2.0

    def test_num_ko(self):
        for bad in (True, "2", None, float("nan"), float("inf")):
            with pytest.raises(ValueError):
                _F["mh510_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh510_str"]("  HR-1 ", "x") == "HR-1"

    def test_str_ko(self):
        for bad in (None, "", "   ", 5):
            with pytest.raises(ValueError):
                _F["mh510_str"](bad, "x")

    def test_data_ok(self):
        # le scadenze possono essere future o passate
        assert _F["mh510_data"]("2027-12-31") == "2027-12-31"
        assert _F["mh510_data"]("2020-01-01") == "2020-01-01"

    def test_data_ko(self):
        for bad in (None, "", "31/12/2027", "2027-13-01", "2027-02-30"):
            with pytest.raises(ValueError):
                _F["mh510_data"](bad)


class TestW510Riga:
    def _rel(self, **kw):
        d = dict(_demo()[0])
        d.update(kw)
        return d

    def test_riga_ok(self):
        r = _F["mh510_riga"](self._rel())
        assert r["id"] == "HR-2026-001"
        assert r["stato"] == "ATTIVA"
        assert r["bucket"] in ("<= 12 mesi", "1-5 anni")

    def test_riga_scaduta(self):
        r = _F["mh510_riga"](self._rel(scadenza="2026-09-30"))
        assert r["stato"] == "SCADUTA"
        assert r["bucket"] == "scaduta"

    def test_nominale_ko(self):
        with pytest.raises(ValueError):
            _F["mh510_riga"](self._rel(nominale=0.0))
        with pytest.raises(ValueError):
            _F["mh510_riga"](self._rel(nominale=-100.0))

    def test_prezzo_medio_ko(self):
        with pytest.raises(ValueError):
            _F["mh510_riga"](self._rel(prezzo_medio=0.0))

    def test_inefficacia_oltre_base_ko(self):
        with pytest.raises(ValueError):
            _F["mh510_riga"](self._rel(inefficacia_pnl=150000.0))

    def test_inefficacia_segno_opposto_ko(self):
        with pytest.raises(ValueError):
            _F["mh510_riga"](self._rel(inefficacia_pnl=-2300.0))

    def test_chiave_mancante_ko(self):
        d = self._rel()
        del d["nominale"]
        with pytest.raises(ValueError):
            _F["mh510_riga"](d)


class TestW510Nota:
    def test_demo_totali(self):
        n = _F["mh510_nota"](_demo())
        assert n["n_relazioni"] == 4
        assert n["tot_nominale"] == 9300000.0
        assert n["tot_fv"] == 23500.0
        assert n["tot_inefficacia_pnl"] == 2200.0
        assert n["tot_riserva_oci"] == 73000.0
        assert n["tot_recycling"] == 17000.0

    def test_demo_verdetto_parziale(self):
        # HR-2026-002 scade 2026-09-30 (< 2026-10-17) => SCADUTA
        n = _F["mh510_nota"](_demo())
        assert n["n_scadute"] == 1
        assert n["verdetto"] == "NOTA_PARZIALE"

    def test_verdetto_completa(self):
        rels = [dict(r, scadenza="2028-06-30") for r in _demo()]
        n = _F["mh510_nota"](rels)
        assert n["n_scadute"] == 0
        assert n["verdetto"] == "NOTA_COMPLETA"

    def test_profilo_scadenze(self):
        n = _F["mh510_nota"](_demo())
        prof = n["profilo_scadenze"]
        buckets = {p["bucket"]: p for p in prof}
        assert "scaduta" in buckets
        assert buckets["scaduta"]["nominale"] == 2000000.0
        assert buckets["scaduta"]["n_relazioni"] == 1
        # somma nominale del profilo == totale
        assert abs(sum(p["nominale"] for p in prof)
                   - n["tot_nominale"]) < 1e-6
        # prezzo medio ponderato su una fascia con 2 relazioni
        rels = [
            {"id": "A", "fv_strumento": 0.0, "delta_fv_base": 0.0,
             "inefficacia_pnl": 0.0, "riserva_oci_chiusura": 0.0,
             "recycling_pnl": 0.0, "nominale": 1000000.0,
             "scadenza": "2027-06-30", "prezzo_medio": 100.0},
            {"id": "B", "fv_strumento": 0.0, "delta_fv_base": 0.0,
             "inefficacia_pnl": 0.0, "riserva_oci_chiusura": 0.0,
             "recycling_pnl": 0.0, "nominale": 3000000.0,
             "scadenza": "2027-06-30", "prezzo_medio": 50.0},
        ]
        n2 = _F["mh510_nota"](rels)
        pm = n2["profilo_scadenze"][0]["prezzo_medio_ponderato"]
        assert abs(pm - 62.5) < 1e-9

    def test_id_duplicati_ko(self):
        rels = _demo()[:2]
        rels[1] = dict(rels[1], id="HR-2026-001")
        with pytest.raises(ValueError):
            _F["mh510_nota"](rels)

    def test_lista_vuota_ko(self):
        with pytest.raises(ValueError):
            _F["mh510_nota"]([])

    def test_riepilogo_wrapper(self):
        assert _F["mh510_riepilogo"](_demo())["verdetto"] == "NOTA_PARZIALE"


def test_registry_tab510():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    line = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    titoli = re.findall(r'"([^"]+)"', line.split("st.tabs([", 1)[1])
    assert len(titoli) == 617
    assert TITLE510 in titoli
    assert src.count(TITLE510) == 3
    assert ", tab510, tab511, tab512, tab513, tab514, tab515, tab516, tab517, tab518, tab519, tab520, tab521, tab522, tab523, tab524, tab525, tab526, tab527, tab528, tab529, tab530, tab531, tab532, tab533, tab534, tab535, tab536, tab537, tab538, tab539, tab540, tab541, tab542, tab543, tab544, tab545, tab546, tab547, tab548, tab549, tab550, tab551, tab552, tab553, tab554, tab555, tab556, tab557, tab558, tab559, tab560, tab561, tab562, tab563, tab564, tab565, tab566, tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617 = st.tabs([" in src
    assert "    with tab510:" in src
    dvars = re.findall(r"tab\d+", line.split("= st.tabs", 1)[0])
    assert "tab510" in dvars
    withs = re.findall(r"    with (tab\d+):", src)
    assert "tab510" in withs
    assert len(withs) == len(dvars) == 617
    # ordine: tab510 dopo tab509
    _decl510 = [ln for ln in src.split("\n") if "= st.tabs([" in ln][0]
    assert _decl510.index(f'"{TITLE509}"') < _decl510.index(f'"{TITLE510}"')
    assert titoli[dvars.index("tab510")] == TITLE510


def test_chiavi_st510_uniche():
    src = Path(__file__).resolve().parent.parent.joinpath("app.py").read_text(encoding="utf-8")
    keys = re.findall(r'key="(st510_[^"]+)"', src) + re.findall(
        r'key=f"(st510_[^"]+)"', src)
    assert len(keys) == len(set(keys)) > 5
