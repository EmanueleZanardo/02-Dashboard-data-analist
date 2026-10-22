"""Test tab568 "Riclassifiche di attivita' finanziarie (IFRS 7.12B-12D)": registry + funzioni pure."""

import math
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from appfuncs import load as _load

_F = _load("mh568_num", "mh568_str", "mh568_categoria", "mh568_tipo",
           "mh568_riclassifica", "mh568_demo", "mh568_riepilogo")

TITLE568 = ("\U0001F4CA\U0001F224 Riclassifiche di attivit\xe0 finanziarie "
            "(IFRS 7.12B-12D)")


def _v(pid="RIC-1", descrizione="pos", tipo="DEBITO", ori="FVTPL_TRADING",
       des="COSTO_AMMORTIZZATO", data="2026-01-01", imp=10_000_000.0,
       fv=10_000_000.0, pnl=0.0, eir=5.0, sp="Cambio business model."):
    return _F["mh568_riclassifica"](pid, descrizione, tipo, ori, des, data,
                                    imp, fv, pnl, eir, sp)


class TestW568Validatori:
    def test_num_ok(self):
        assert _F["mh568_num"](2, "x") == 2.0
        assert _F["mh568_num"](-3.5, "x") == -3.5
        assert _F["mh568_num"](0, "x") == 0.0

    def test_num_ko(self):
        for bad in (True, "1", None, math.nan, math.inf):
            with pytest.raises(ValueError):
                _F["mh568_num"](bad, "x")

    def test_str_ok(self):
        assert _F["mh568_str"]("  abc ", "x") == "abc"

    def test_str_ko(self):
        for bad in ("", "   ", None, 5, b"a"):
            with pytest.raises(ValueError):
                _F["mh568_str"](bad, "x")

    def test_categoria_ok(self):
        assert _F["mh568_categoria"]("fvtpl_trading", "x") == "FVTPL_TRADING"
        assert _F["mh568_categoria"]("FVOCI", "x") == "FVOCI"
        assert _F["mh568_categoria"]("costo_ammortizzato",
                                     "x") == "COSTO_AMMORTIZZATO"

    def test_categoria_ko(self):
        for bad in ("XYZ", "", None, "FVPL"):
            with pytest.raises(ValueError):
                _F["mh568_categoria"](bad, "x")

    def test_tipo_ok(self):
        assert _F["mh568_tipo"]("debito", "x") == "DEBITO"
        assert _F["mh568_tipo"]("EQUITY", "x") == "EQUITY"

    def test_tipo_ko(self):
        for bad in ("OBBLIGAZIONE", "", None, 5):
            with pytest.raises(ValueError):
                _F["mh568_tipo"](bad, "x")


class TestW568Riclassifica:
    def test_hand_computed(self):
        r = _v(pid="RIC-001", imp=45_000_000.0, fv=45_000_000.0,
               pnl=2_300_000.0, eir=4.8)
        assert r["id"] == "RIC-001"
        assert r["tipo_strumento"] == "DEBITO"
        assert r["categoria_origine"] == "FVTPL_TRADING"
        assert r["categoria_destinazione"] == "COSTO_AMMORTIZZATO"
        assert r["importo"] == pytest.approx(45_000_000.0)
        assert r["fv_data"] == pytest.approx(45_000_000.0)
        assert r["impatto_pnl_evitato"] == pytest.approx(2_300_000.0)
        assert r["tasso_effettivo_pct"] == pytest.approx(4.8)

    def test_spiegazione_puo_essere_vuota(self):
        r = _v(sp="")
        assert r["spiegazione"] == ""

    def test_spiegazione_strip(self):
        r = _v(sp="  Cambio.  ")
        assert r["spiegazione"] == "Cambio."

    def test_input_ko(self):
        with pytest.raises(ValueError):
            _v(ori="XYZ")
        with pytest.raises(ValueError):
            _v(tipo="BOND")
        with pytest.raises(ValueError):
            _v(pid="")
        with pytest.raises(ValueError):
            _v(imp=math.nan)
        with pytest.raises(ValueError):
            _v(data="   ")


class TestW568Demo:
    def test_demo_shape(self):
        d = _F["mh568_demo"]()
        assert len(d) == 3
        assert all(set(r) >= {"importo", "fv_data", "spiegazione",
                              "tasso_effettivo_pct"} for r in d)

    def test_demo_verdetto(self):
        r = _F["mh568_riepilogo"](_F["mh568_demo"]())
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 3
        assert r["n_senza_spiegazione"] == 1
        # equity (RIC-003): riclassifica equity + spiegazione mancante
        # + EIR mancante per costo ammortizzato
        ids = [p["id"] for p in r["analizzate"] if p["anomalie"]]
        assert ids == ["RIC-003"]

    def test_demo_importo_totale(self):
        r = _F["mh568_riepilogo"](_F["mh568_demo"]())
        assert r["importo_totale"] == pytest.approx(60_700_000.0)


class TestW568Riepilogo:
    def test_significative_soglia_bassa(self):
        rs = [_v(pid="A", imp=40_000_000.0, fv=40_000_000.0),
              _v(pid="B", imp=30_000_000.0, fv=30_000_000.0)]
        r = _F["mh568_riepilogo"](rs, soglia_eur=50_000_000.0)
        assert r["verdetto"] == "RICLASSIFICHE_SIGNIFICATIVE"
        assert r["n_anomalie"] == 0

    def test_disclosure_adeguata(self):
        rs = [_v(pid="A", imp=12_000_000.0, fv=12_000_000.0)]
        r = _F["mh568_riepilogo"](rs, soglia_eur=50_000_000.0)
        assert r["verdetto"] == "DISCLOSURE_ADEGUATA"

    def test_nessuna_riclassifica(self):
        r = _F["mh568_riepilogo"]([_v(imp=0.0, fv=1.0)])
        assert r["verdetto"] == "NESSUNA_RICLASSIFICA"

    def test_anomalia_stessa_categoria(self):
        r = _F["mh568_riepilogo"]([_v(ori="FVOCI", des="FVOCI")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert any("nessuna riclassifica" in a.lower()
                   for p in r["analizzate"] for a in p["anomalie"])

    def test_anomalia_equity(self):
        r = _F["mh568_riepilogo"]([_v(tipo="EQUITY")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert any("capitale" in a.lower()
                   for p in r["analizzate"] for a in p["anomalie"])

    def test_anomalia_spiegazione_mancante(self):
        r = _F["mh568_riepilogo"]([_v(sp="")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_senza_spiegazione"] == 1

    def test_anomalia_eir_mancante(self):
        # destinazione COSTO_AMMORTIZZATO con EIR 0 -> 7.12D(c)
        r = _F["mh568_riepilogo"]([_v(eir=0.0)])
        assert any("EIR" in a for p in r["analizzate"]
                   for a in p["anomalie"])

    def test_eir_non_richiesto_per_fvtpl(self):
        r = _F["mh568_riepilogo"](
            [_v(ori="FVOCI", des="FVTPL_TRADING", eir=0.0)])
        assert r["n_anomalie"] == 0
        assert r["analizzate"][0]["completa"]

    def test_anomalia_mismatch_fv(self):
        # 10% di scarto tra importo e FV alla data
        r = _F["mh568_riepilogo"]([_v(imp=10_000_000.0, fv=9_000_000.0)])
        assert any("5%" in a for p in r["analizzate"]
                   for a in p["anomalie"])

    def test_mismatch_sotto_soglia_ok(self):
        # 2% di scarto: nessuna anomalia di allineamento
        r = _F["mh568_riepilogo"]([_v(imp=10_000_000.0, fv=9_800_000.0)])
        assert r["n_anomalie"] == 0

    def test_anomalia_id_duplicato(self):
        r = _F["mh568_riepilogo"]([_v(pid="RIC-X"), _v(pid="ric-x")])
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"
        assert r["n_anomalie"] == 1

    def test_anomalie_prevalgono_su_significative(self):
        rs = [_v(pid="RIC-X", imp=80_000_000.0, fv=80_000_000.0),
              _v(pid="RIC-X", imp=10_000_000.0, fv=10_000_000.0)]
        r = _F["mh568_riepilogo"](rs, soglia_eur=50_000_000.0)
        assert r["verdetto"] == "ANOMALIE_DA_VERIFICARE"

    def test_lista_vuota(self):
        with pytest.raises(ValueError):
            _F["mh568_riepilogo"]([])

    def test_soglia_ko(self):
        for bad in (0.0, -100.0):
            with pytest.raises(ValueError):
                _F["mh568_riepilogo"](_F["mh568_demo"](),
                                      soglia_eur=bad)


class TestW568Registry:
    def test_titolo_presente(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert f'"{TITLE568}"' in src

    def test_conteggio_tab(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        m = re.search(r"= st\.tabs\(\[(.*?)\]\)", src, re.S)
        titles = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))
        assert len(titles) == 644
        assert TITLE568 in titles

    def test_chain_tab_var(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        assert ", tab567, tab568, tab569, tab570, tab571, tab572, tab573, tab574, tab575, tab576, tab577, tab578, tab579, tab580, tab581, tab582, tab583, tab584, tab585, tab586, tab587, tab588, tab589, tab590, tab591, tab592, tab593, tab594, tab595, tab596, tab597, tab598, tab599, tab600, tab601, tab602, tab603, tab604, tab605, tab606, tab607, tab608, tab609, tab610, tab611, tab612, tab613, tab614, tab615, tab616, tab617, tab618, tab619, tab620, tab621, tab622, tab623, tab624, tab625, tab626, tab627, tab628, tab629, tab630, tab631, tab632, tab633, tab634, tab635, tab636, tab637, tab638, tab639, tab640, tab641, tab642, tab643, tab644 = st.tabs([" in src
        assert "with tab568:" in src

    def test_chiavi_univoche(self):
        src = Path(__file__).resolve().parent.parent.joinpath(
            "app.py").read_text(encoding="utf-8")
        keys = set(re.findall(r"st568_[a-z0-9_]+", src))
        assert len(keys) >= 11, keys
